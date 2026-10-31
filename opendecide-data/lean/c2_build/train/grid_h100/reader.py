"""grid_h100.reader: the read client. Runs under C1's PINNED35 stack (/opt/fastpath/bin/python: transformers 5.17 / tokenizers 0.23.2, the
stack that tokenised the training and the gate reads), talks to the local SGLang server over plain HTTP, and writes the pred files in the
od_gcp.py predict format (preds_<split>/<name><tag>.jsonl + .meta.json) with the fields gate_dev.pipeline_check and grid_elig read.

One long-lived process (`serve`) for the whole job:
  init     C1's tokenizer + full Readout (hosting.sglang_host.load_c1_tokenizer), the P7 prompt-sha check of that tokenizer against the
           recorded train / gate / S1 render (c2_build/logs/p7_prompt_sha_check.json: every probe view's sha256 and the token-id digest
           must be equal), the data files' sha256 against the plan's manifest, and ALL read sets tokenised once (the 19 models read the
           same token ids);
  run      one command per model (cmd_<k>.json -> res_<k>.json): the batch-1 latency run on the fresh server (d9_latency.measure, workload S,
           c = 1), then every set of the plan. A model is one clean job: same tokenizer, same readout, same server arguments.
Readout (A18.2): choice rows with views 2 are read in the given order and the exact reversal and averaged in probability space; yes/no rows
once; T = 1.0 / 1.0; a seeded permuted view (perm seed 1, decoder_io.view_perms) is ONE view, no averaging. SGLang returns the candidate log-
probabilities of one prefill pass (hosting/sglang_host.build_generate_body / parse_generate_response), the per-letter logit is their logsumexp.
"""
from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _setup_paths():
    from . import common as C
    for d in (C.LEAN, C.LEAN / "hosting"):
        if str(d) not in sys.path:
            sys.path.insert(0, str(d))
    return C


C = _setup_paths()
import sglang_host as SH  # noqa: E402  (no Modal in the fastpath venv: sglang_host guards the import)
from fastcore import readout as R  # noqa: E402

dio = R.dio


class Http:
    """Thread-local keep-alive client of the local SGLang server (stdlib only)."""

    def __init__(self, host="127.0.0.1", port=C.PORT, timeout=900.0):
        self.host, self.port, self.timeout = host, port, timeout
        self.local = threading.local()

    def _conn(self, fresh=False):
        c = getattr(self.local, "c", None)
        if c is None or fresh:
            if c is not None:
                c.close()
            c = http.client.HTTPConnection(self.host, self.port, timeout=self.timeout)
            self.local.c = c
        return c

    def request(self, method, path, obj=None):
        body = None if obj is None else json.dumps(obj).encode()
        hdr = {"Content-Type": "application/json"} if body else {}
        for attempt in range(3):
            try:
                c = self._conn(fresh=attempt > 0)
                c.request(method, path, body=body, headers=hdr)
                r = c.getresponse()
                data = r.read()
                if r.status != 200:
                    raise RuntimeError(f"SGLang {method} {path}: HTTP {r.status}: {data[:400]!r}")
                return json.loads(data) if data and data[:1] in b"[{" else data.decode()
            except (ConnectionError, http.client.HTTPException, OSError) as e:
                if attempt == 2:
                    raise RuntimeError(f"SGLang unreachable: {type(e).__name__}: {e}") from e
                time.sleep(1.0 + attempt)


def sha256_file(p) -> str:
    return C.sha256_file(p)


# ------------------------------------------------------------------ prompt-sha check (P7)
def prompt_check(c1_dir, recorded: dict, tok=None, ro=None) -> dict:
    """The S1 client's rendering of the P7 probe views (32 views of 16 rows, incl. a 15k-token row) from this tokenizer folder, against the
    recorded train-path render: every view's prompt sha256 and the token-id digest must be equal. Returns the record (ok / problems)."""
    from . import servers
    P = servers.serving_mod("prompt_sha_check")
    if tok is None:
        tok, ro, _ = SH.load_c1_tokenizer(c1_dir)
    vr, vp = P.views_of(P.probe_rows())
    names = [f"{r['id']}:{'rev' if p is not None else 'given'}" for r, p in zip(vr, vp)]
    texts = dio.prompt_texts(ro, vr, vp)
    shas = dict(zip(names, P.shas(texts)))
    ids = []
    for r, p, t in zip(vr, vp, texts):
        it = R.WorkItem(q=0, view=0, perm=p, text=t, groups=ro.cand(r), row=r)
        R.tokenize_items(tok, [it])
        ids.append(it.ids)
    want = recorded.get("prompt_sha256") or {}
    bad = [n for n in names if shas.get(n) != want.get(n)]
    probs = []
    if set(want) != set(names):
        probs.append(f"probe views differ from the record ({len(set(want) ^ set(names))} names)")
    if bad:
        probs.append(f"rendered prompt sha256 differs from the train / gate record on {len(bad)} of {len(names)} views, first {bad[:3]}")
    dig = C.canon_sha(ids)
    if recorded.get("token_ids_digest") and dig != recorded["token_ids_digest"]:
        probs.append("token-id digest differs from the record")
    return {"ok": not probs, "problems": probs, "views": len(names), "prompt_sha256_digest": C.canon_sha(shas),
            "recorded_prompt_sha256_digest": recorded.get("prompt_sha256_digest"), "token_ids_digest": dig,
            "chat_template_sha": hashlib.sha256((getattr(tok, "chat_template", None) or "").encode()).hexdigest()}


# ------------------------------------------------------------------ the reader
class SetData:
    """One read set, tokenised: rows, and per fixed chunk of rows the work items (q = index within the chunk)."""

    def __init__(self, spec, rows, chunks, tokens):
        self.spec, self.rows, self.chunks, self.tokens = spec, rows, chunks, tokens


def read_rows(path) -> list:
    return [json.loads(l) for l in open(C.safe_path(path)) if l.strip()]


def items_for_row(ro, row, views: int, perm):
    groups = ro.cand(row)
    flat = [t for g in groups for t in g]
    sizes = [len(g) for g in groups]
    perms = [perm] if perm is not None else R.views_for(row, views)
    return [R.WorkItem(q=0, view=vi, perm=p, text=None, groups=groups, flat=flat, sizes=sizes, row=row) for vi, p in enumerate(perms)]


def probs_of(ans: dict) -> dict:
    return ans["probabilities"] if ans["type"] == "choice" else {"yes": ans["probabilities"]["yes"], "no": ans["probabilities"]["no"]}


class GridReader:
    def __init__(self, c1_dir, data_dir, specs, manifest=None, recorded_check=None, port=C.PORT, workers=16, chunk=8, log=print,
                 http=None):
        self.c1_dir, self.data_dir, self.specs = Path(c1_dir), Path(data_dir), specs
        self.manifest, self.recorded_check = manifest or {}, recorded_check
        self.workers, self.chunk, self.log = workers, chunk, log
        self.http = http or Http(port=port)
        self.sets = []
        self.init_info = {}

    # -- init
    def init(self) -> dict:
        t0 = time.time()
        if (dio.MAX_LEN != SH.MAX_LEN):
            raise SystemExit("reader: decoder_io.MAX_LEN differs from sglang_host's: the context length would be wrong")
        self.tok, self.ro, self.info = SH.load_c1_tokenizer(self.c1_dir)
        if (dio.LAYOUT, dio.STYLE) != (C.LAYOUT, C.STYLE):
            raise SystemExit(f"reader: layout / style {(dio.LAYOUT, dio.STYLE)} is not C1's")
        self.load_info = {**self.info, "prism_x": False,
                          "chat_template_sha": hashlib.sha256((getattr(self.tok, "chat_template", None) or "").encode()).hexdigest()}
        self.init_info["tokenizer_s"] = round(time.time() - t0, 1)
        if self.recorded_check is not None:
            chk = prompt_check(self.c1_dir, self.recorded_check, self.tok, self.ro)
            self.init_info["prompt_check"] = chk
            if not chk["ok"]:
                raise SystemExit("reader: the prompt-sha check failed: " + "; ".join(chk["problems"]))
        for s in self.specs:
            self.sets.append(self._prepare(s))
        self.init_info.update({"sets": len(self.sets), "rows": sum(len(s.rows) for s in self.sets),
                               "tokens": sum(s.tokens for s in self.sets), "init_s": round(time.time() - t0, 1)})
        return self.init_info

    def _prepare(self, spec) -> SetData:
        C.check_names(spec["split"])
        path = self.data_dir / spec["file"]
        want = (self.manifest.get(spec["file"]) or {}).get("sha256")
        if want and sha256_file(path) != want:
            raise SystemExit(f"reader: {spec['file']} differs from the plan's manifest (sha256)")
        rows = read_rows(path)
        perms = dio.view_perms(rows, spec["perm_seed"]) if spec["perm_seed"] is not None else [None] * len(rows)
        per_row = [items_for_row(self.ro, r, spec["views"], p) for r, p in zip(rows, perms)]
        flat = [it for items in per_row for it in items]
        R.render_items(self.ro, flat)
        for i in range(0, len(flat), 2000):
            R.tokenize_items(self.tok, flat[i:i + 2000])
        long = [it.n_tokens for it in flat if it.n_tokens >= SH.CONTEXT_LEN]
        if long:
            raise SystemExit(f"reader: a prompt of {max(long)} tokens is over the context length ({spec['split']})")
        chunks = []
        for i in range(0, len(rows), self.chunk):
            its = []
            for j, items in enumerate(per_row[i:i + self.chunk]):
                for it in items:
                    it.q = j
                    its.append(it)
            chunks.append((i, rows[i:i + self.chunk], its))
        return SetData(spec, rows, chunks, sum(it.n_tokens for it in flat))

    # -- one read of a chunk
    def _read_chunk(self, rows, items, stats, lock):
        named = [(str(j), r) for j, r in enumerate(rows)]
        body = SH.build_generate_body(items, f"gr-{threading.get_ident()}-{time.time_ns()}")
        resp = self.http.request("POST", "/generate", body)
        logits, meta = SH.parse_generate_response(items, resp, body["rid"])
        answers, usage = R.combine(named, items, logits, None)
        with lock:
            stats["rows"] += len(rows)
            stats["reads"] += len(items)
            stats["tokens"] += usage["input_tokens"]
            stats["cached_tokens"] += meta.get("cached_tokens") or 0
        return [probs_of(answers[n]) for n, _ in named]

    def read_set(self, sd: SetData, progress_every: int = 0) -> tuple:
        out = [None] * len(sd.chunks)
        stats = {"rows": 0, "reads": 0, "tokens": 0, "cached_tokens": 0}
        lock, done, t0 = threading.Lock(), [0], time.time()

        def run(k):
            _, rows, items = sd.chunks[k]
            out[k] = self._read_chunk(rows, items, stats, lock)
            with lock:
                done[0] += 1
                if progress_every and done[0] % progress_every == 0:
                    self.log(f"  {sd.spec['split']}{sd.spec['tag']}: {stats['rows']}/{len(sd.rows)} rows, {time.time() - t0:.0f}s")

        with ThreadPoolExecutor(self.workers) as ex:
            list(ex.map(run, range(len(sd.chunks))))
        probs = [p for ch in out for p in ch]
        if len(probs) != len(sd.rows):
            raise RuntimeError(f"{sd.spec['split']}: {len(probs)} answers for {len(sd.rows)} rows")
        return probs, stats, time.time() - t0

    # -- latency (d9_latency.measure: one decision at a time, tokenise + POST + parse + combine in the timed call)
    def latency(self, label: str, meta: dict, n: int, warmup: int, workload_dir, workload: str = "S", seed: int = 0) -> dict:
        from . import servers
        D9 = servers.serving_mod("d9_latency")
        requests, wsha = D9.load_workload(workload, Path(workload_dir))

        def read_one(row):
            named = [("0", row)]
            items = R.build_items(self.ro, named, choice_views=1, render=True)
            R.tokenize_items(self.tok, items)
            body = SH.build_generate_body(items, f"lat-{time.time_ns()}")
            resp = self.http.request("POST", "/generate", body)
            logits, _ = SH.parse_generate_response(items, resp, body["rid"])
            return R.combine(named, items, logits, None)[0]["0"]

        m = {"workload": workload, "workload_sha256": wsha, "views": 1, "flushed": True, "port": self.http.port,
             "reader_sha256": sha256_file(__file__), **meta}
        return D9.measure(read_one, lambda q: R.parse_v1(q), requests, n, warmup, label, m, seed)

    # -- one model
    def run_model(self, cmd: dict) -> dict:
        t0 = time.time()
        name, out_dir = cmd["read_name"], Path(cmd["out_dir"])
        C.check_names(name)
        res = {"read_name": name, "sets": {}, "latency": None}
        if cmd.get("latency"):
            lc = cmd["latency"]
            res["latency"] = self.latency(lc["label"], lc["meta"], lc["n"], lc["warmup"], lc["workload_dir"], lc.get("workload", "S"),
                                          lc.get("seed", 0))
        env = cmd["env_meta"]
        for sd in self.sets:
            sp = sd.spec
            probs, stats, sec = self.read_set(sd, progress_every=cmd.get("progress_every", 0))
            pname = name + sp["tag"]
            pdir = out_dir / sp["pred_dir"]
            C.write_jsonl(pdir / f"{pname}.jsonl", ({"id": r["id"], "model": pname, "probs": p} for r, p in zip(sd.rows, probs)))
            meta = {"name": pname, "rows": len(sd.rows), "layout": dio.LAYOUT, "style": dio.STYLE, "base": C.BASE, "host": C.HOST_TAG,
                    "gpu": env["gpu"], "torch": env["torch"], "cuda": env["cuda"], "sec": round(sec), "tta": False,
                    "tta_choice": sp["views"] == 2, "tta_noul": False, "perm_seed": sp["perm_seed"], "load": self.load_info,
                    "engine": "sglang", "sglang_version": env.get("sglang_version"), "server_args": env.get("server_args"),
                    "reads": stats["reads"], "input_tokens": stats["tokens"], "cached_tokens": stats["cached_tokens"],
                    "read_sec": round(sec, 1), "reads_per_sec": round(stats["reads"] / max(sec, 1e-9), 2),
                    "rows_per_sec": round(stats["rows"] / max(sec, 1e-9), 2),
                    "grid_h100": {**cmd.get("provenance", {}), "split": sp["split"], "job": sp["job"],
                                  "data_sha256": (self.manifest.get(sp["file"]) or {}).get("sha256"),
                                  "reader_sha256": sha256_file(__file__)}}
            C.write_json(pdir / f"{pname}.meta.json", meta)
            res["sets"][sp["split"] + sp["tag"]] = {"rows": len(sd.rows), "sec": round(sec, 1), "sha256": sha256_file(pdir / f"{pname}.jsonl"),
                                  "input_tokens": stats["tokens"], "cached_tokens": stats["cached_tokens"],
                                  "reads_per_sec": meta["reads_per_sec"]}
            self.log(f"{name}: {pname} {len(sd.rows)} rows in {sec:.0f}s")
        res["wall_s"] = round(time.time() - t0, 1)
        return res

    # -- parity: read arbitrary rows (views 1 or 2) and return probs
    def read_rows_now(self, rows: list, views: int) -> list:
        out = [None] * ((len(rows) + self.chunk - 1) // self.chunk)
        stats = {"rows": 0, "reads": 0, "tokens": 0, "cached_tokens": 0}
        lock = threading.Lock()

        def run(k):
            part = rows[k * self.chunk:(k + 1) * self.chunk]
            named = [(str(j), r) for j, r in enumerate(part)]
            items = R.build_items(self.ro, named, choice_views=views, render=True)
            R.tokenize_items(self.tok, items)
            out[k] = self._read_chunk(part, items, stats, lock)

        with ThreadPoolExecutor(self.workers) as ex:
            list(ex.map(run, range(len(out))))
        return [p for ch in out for p in ch]


# ------------------------------------------------------------------ the daemon
def _atomic(path: Path, obj):
    C.write_json(path, obj)


def serve(spec: dict, log=print) -> int:
    """Control-file loop: spec["ctl_dir"]/cmd_<k>.json -> res_<k>.json; ready.json after init; quit file ends it."""
    ctl = Path(spec["ctl_dir"])
    ctl.mkdir(parents=True, exist_ok=True)
    gr = GridReader(spec["c1_dir"], spec["data_dir"], spec["sets"], spec.get("manifest"), spec.get("recorded_check"),
                    spec.get("port", C.PORT), spec.get("workers", 16), spec.get("chunk", 8), log=log)
    try:
        info = gr.init()
    except BaseException as e:  # noqa: BLE001 - the orchestrator reads ready.json and stops
        _atomic(ctl / "ready.json", {"ok": False, "error": f"{type(e).__name__}: {e}"[:3000]})
        return 3
    _atomic(ctl / "ready.json", {"ok": True, "info": info})
    k = 0
    while not (ctl / "quit").exists():
        f = ctl / f"cmd_{k}.json"
        if not f.exists():
            time.sleep(0.5)
            continue
        cmd = json.loads(f.read_text())
        try:
            if cmd.get("op") == "read_rows":                 # the parity check: arbitrary rows, given views, probs back as a jsonl file
                t1 = time.time()
                rows = read_rows(cmd["rows_file"])
                probs = gr.read_rows_now(rows, int(cmd["views"]))
                C.write_jsonl(cmd["out"], ({"id": r["id"], "model": cmd.get("name", "served"), "probs": p} for r, p in zip(rows, probs)))
                res = {"ok": True, "rows": len(rows), "sec": round(time.time() - t1, 1), "sha256": sha256_file(cmd["out"])}
            else:
                res = gr.run_model(cmd)
            res["ok"] = True
        except BaseException as e:  # noqa: BLE001
            res = {"ok": False, "error": f"{type(e).__name__}: {e}"[:3000], "read_name": cmd.get("read_name")}
        _atomic(ctl / f"res_{k}.json", res)
        k += 1
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=["serve"])
    ap.add_argument("--spec", required=True)
    a = ap.parse_args(argv)
    return serve(json.loads(Path(a.spec).read_text()), log=lambda s: print(s, flush=True))


if __name__ == "__main__":
    sys.exit(main())
