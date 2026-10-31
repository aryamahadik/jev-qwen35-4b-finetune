"""reads/fast_read.py: fast C1 reads on the L4 VM (od-l4b) through an SGLang server, same input/output files as
`od_gcp.py predict` and `od_gcp.py label`. NEW file (A49 f); nothing pinned is edited.

What it is: the A35 / SPEED-2 arm S1 (hosting/sglang_host.py, SGLang 0.5.20, merged BF16 C1, fp32 LM head, hybrid prefix
cache, no speculation) minus Modal. The server is launched with sglang_host.server_cmd (the same flags) and its resolved
args are checked with sglang_host.check_server_args. Reads use the A18.2 readout built by hosting/fastcore/readout.py
(= decoder_io byte for byte): prompt text, candidate ids, 2view probability average for choice rows (given order + exact
reversal), single read for yes/no rows, T = 1.0. SGLang returns candidate log-probabilities of one prefill-only pass;
the per-letter logit is their logsumexp (sglang_host.parse_generate_response). C1 output is a routing / selection signal
only, never a label (A49 f).

Layout on the VM: this file anywhere; lean root ~/lean (decoder_io.py, shard_golden.py, hosting/ copied there, models/
q35_4b_main500k = the adapter folder with its tokenizer + train_meta); merged checkpoint ~/models/q35_4b_main500k_merged
(reads/export_merged.py); SGLang venv ~/sgl; run this file with ~/od/bin/python (C1's pinned transformers 5.17 /
tokenizers 0.23.2 stack, which tokenizes the prompts).

  fast_read.py serve   [--model DIR] [--sgl-python ~/sgl/bin/python] [--extra-args "..."]   # start SGLang, wait, check
  fast_read.py stop
  fast_read.py predict --name q35_4b_main500k --splits gblock_a42d_c1read [--tag _fast] [--limit N]
        # data/<split>.jsonl -> preds_<split>/<name><tag>.jsonl + .meta.json  (od_gcp.py predict --tta-choice format)
  fast_read.py label   --shards-dir data/c2_replay_shards [--shard i] [--out DIR]
        # shards -> <shards-dir>/labels_<name>/shard_NNN.jsonl + .meta.json  (od_gcp.py label --tta-choice format;
        # the settings dict is identical to the HF path's, so shard_golden / replay_sample / mix_c2 accept it)
  fast_read.py parity  --split gblock_a42d_c1read --ref preds_gblock_a42d_c1read/q35_4b_main500k.jsonl --n 2000 --seed S
        # the A49 (f) bar: argmax agreement >= 99.5% and |d p(label)| <= 0.02 on >= 99% of rows

Paths are relative to --root (default: the lean root). Reads are deterministic given the server (one prefill pass per
sequence, no sampling); the output order is the input order.
"""
from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import os
import pathlib
import random
import signal
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _find_lean() -> Path:
    for c in (os.environ.get("OD_LEAN"), HERE.parents[1], Path.home() / "lean"):
        if c and (Path(c) / "decoder_io.py").exists() and (Path(c) / "hosting").exists():
            return Path(c).resolve()
    raise SystemExit("fast_read: no lean root with decoder_io.py and hosting/ (set OD_LEAN)")


# On the VM /root/lean (hosting's container path) exists but is unreadable: Path.exists() raises PermissionError there.
_orig_exists = pathlib.Path.exists


def _safe_exists(self, *a, **k):
    try:
        return _orig_exists(self, *a, **k)
    except PermissionError:
        return False


pathlib.Path.exists = _safe_exists

LEAN = _find_lean()
sys.path.insert(0, str(LEAN))
sys.path.insert(0, str(LEAN / "hosting"))

C1 = "q35_4b_main500k"
BASE = "Qwen/Qwen3.5-4B"
REVISION = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
SGL_HOST, SGL_PORT = "127.0.0.1", 30000


def settings_for(views: int) -> dict:
    """The label settings dict of od_gcp.py label: views 2 = --tta-choice (the A5 readout: replay second pass, G-block,
    G-proxy, pilot dev reads); views 1 = no TTA (the C2 crowd read: one view, given option order, c2_select)."""
    return {"name": C1, "base": BASE, "revision": REVISION, "layout": "schema_branch_mark", "perm_seed": None,
            "tta": False, "tta_choice": views == 2, "tta_noul": False, "merged": True}


def sha256_file(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


# ------------------------------------------------------------------ SGLang server (start / stop / check)

def _sh():
    import sglang_host as SH
    return SH


class Http:
    """Thread-local keep-alive client of the local SGLang server (stdlib only; the ~/od venv has no httpx)."""

    def __init__(self, host=SGL_HOST, port=SGL_PORT, timeout=900.0):
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

    def alive(self):
        try:
            self._conn(fresh=True).request("GET", "/health")
            return self._conn().getresponse().status == 200
        except Exception:  # noqa: BLE001
            return False


def cmd_serve(a):
    SH = _sh()
    model = Path(a.model).expanduser()
    if not (model / "merge_manifest.json").exists():
        raise SystemExit(f"{model}: no merge_manifest.json (run reads/export_merged.py first)")
    man = json.loads((model / "merge_manifest.json").read_text())
    if man["adapter_sha256"] != SH.C1_ADAPTER_SHA256:
        raise SystemExit("merged checkpoint is not C1 (adapter sha256 differs from the pin)")
    cmd = SH.server_cmd(str(model), fp8=False, port=a.port, max_running_requests=a.max_running,
                        max_mamba_cache_size=a.max_mamba, mem_fraction_static=a.mem_fraction or None,
                        chunked_prefill_size=a.chunked_prefill or None, python=str(Path(a.sgl_python).expanduser()))
    cmd += a.extra_args.split()
    log = open(Path(a.log).expanduser(), "ab")
    p = subprocess.Popen(cmd, env=SH.server_env(), stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    Path(a.pidfile).expanduser().write_text(str(p.pid))
    print(f"launched SGLang pid {p.pid}: {' '.join(cmd)}", flush=True)
    cl = Http(port=a.port)
    t0 = time.time()
    while time.time() - t0 < a.boot_timeout:
        if p.poll() is not None:
            raise SystemExit(f"SGLang exited rc={p.returncode} during boot; see {a.log}")
        if cl.alive():
            break
        time.sleep(5)
    else:
        raise SystemExit(f"SGLang not up in {a.boot_timeout} s; see {a.log}")
    info = cl.request("GET", "/server_info")
    want = SH.want_server_args(str(model), False, {"max_running_requests": a.max_running,
                                                    "max_mamba_cache_size": a.max_mamba})
    problems, warnings = SH.check_server_args(info, want)
    out = {"boot_s": round(time.time() - t0, 1), "problems": problems, "warnings": warnings,
           "server_args": SH.args_subset(info)}
    print(json.dumps(out, indent=1, default=str), flush=True)
    if problems:
        os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        raise SystemExit("server args differ from S1 on parity-critical settings: refusing")
    Path(a.pidfile).expanduser().with_suffix(".args.json").write_text(json.dumps(out, default=str, indent=1))


def cmd_stop(a):
    pf = Path(a.pidfile).expanduser()
    if pf.exists():
        pid = int(pf.read_text())
        try:
            os.killpg(os.getpgid(pid), signal.SIGTERM)
            print("stopped SGLang pid", pid)
        except ProcessLookupError:
            print("SGLang pid", pid, "already gone")
        pf.unlink()


# ------------------------------------------------------------------ the reader

class Reader:
    """rows -> {id: probs} through the running server. Thread pool of chunks; each chunk = tokenize, one /generate call
    for all its sequences (SGLang batches across concurrent chunks itself), parse, combine."""

    def __init__(self, port=SGL_PORT, adapter=None, workers=12, chunk=8, log=print, views=2):
        SH = _sh()
        self.SH, self.log = SH, log
        from fastcore import readout as R
        self.R, self.dio = R, R.dio
        adapter = Path(adapter or LEAN / "models" / C1)
        self.tok, self.ro, self.info = SH.load_c1_tokenizer(adapter)
        if (self.dio.LAYOUT, self.dio.STYLE) != ("schema_branch_mark", "cygnet"):
            raise SystemExit(f"layout/style {(self.dio.LAYOUT, self.dio.STYLE)} is not C1's")
        if self.dio.MAX_LEN != SH.MAX_LEN:
            raise SystemExit("decoder_io.MAX_LEN differs from sglang_host's: context length would be wrong")
        self.http = Http(port=port)
        self.workers, self.chunk, self.views = workers, chunk, views
        self.stats = {"rows": 0, "reads": 0, "tokens": 0, "cached_tokens": 0}
        self.lock = threading.Lock()

    def _read_chunk(self, rows, views=False):
        R, SH = self.R, self.SH
        named = [(str(i), r) for i, r in enumerate(rows)]
        items = R.build_items(self.ro, named, choice_views=self.views, render=True)
        R.tokenize_items(self.tok, items)
        long = [it.n_tokens for it in items if it.n_tokens >= SH.CONTEXT_LEN]
        if long:
            raise RuntimeError(f"prompt of {max(long)} tokens is over the context length")
        rid = f"fr-{threading.get_ident()}-{time.time_ns()}"
        body = SH.build_generate_body(items, rid)
        resp = self.http.request("POST", "/generate", body)
        logits, meta = SH.parse_generate_response(items, resp, body["rid"])
        answers, usage = R.combine(named, items, logits, None, return_views=views)
        with self.lock:
            self.stats["rows"] += len(rows)
            self.stats["reads"] += len(items)
            self.stats["tokens"] += usage["input_tokens"]
            self.stats["cached_tokens"] += meta.get("cached_tokens") or 0
        return [answers[n] for n, _ in named]

    def read(self, rows, progress_every=50, views=False):
        """Answers (API v1 dicts, with usage) in row order."""
        chunks = [rows[i:i + self.chunk] for i in range(0, len(rows), self.chunk)]
        out = [None] * len(chunks)
        t0, done = time.time(), [0]

        def run(k):
            out[k] = self._read_chunk(chunks[k], views)
            with self.lock:
                done[0] += 1
                if progress_every and done[0] % progress_every == 0:
                    el = time.time() - t0
                    s = self.stats
                    self.log(f"  {s['rows']}/{len(rows)} rows, {s['reads']} reads, {s['reads'] / el:.1f} reads/s, "
                             f"{s['rows'] / el:.1f} rows/s, {el:.0f}s", flush=True)

        with ThreadPoolExecutor(self.workers) as ex:
            list(ex.map(run, range(len(chunks))))
        return [a for ch in out for a in ch]

    @staticmethod
    def probs(ans):
        return ans["probabilities"] if ans["type"] == "choice" else {"yes": ans["probabilities"]["yes"],
                                                                      "no": ans["probabilities"]["no"]}


# ------------------------------------------------------------------ predict / label (od_gcp.py file formats)

def read_rows(root, split):
    return [json.loads(l) for l in open(root / "data" / f"{split}.jsonl") if l.strip()]


def engine_meta(rd, sec):
    st = dict(rd.stats)
    args = {}
    pf = Path("~/jobs/sglang.pid").expanduser().with_suffix(".args.json")
    if pf.exists():
        args = json.loads(pf.read_text()).get("server_args", {})
    return {"engine": "sglang", "sglang_version": args.get("version"), "server_args": args, "reads": st["reads"],
            "input_tokens": st["tokens"], "cached_tokens": st["cached_tokens"], "read_sec": round(sec, 1),
            "reads_per_sec": round(st["reads"] / max(sec, 1e-9), 2), "rows_per_sec": round(st["rows"] / max(sec, 1e-9), 2),
            "fast_read_sha256": sha256_file(__file__), "ref": "A49 (f) fast path; C1 output is never a label"}


def cmd_predict(a):
    root = Path(a.root).resolve()
    rd = Reader(a.port, root / "models" / a.name, a.workers, a.chunk, views=a.views)
    name = (a.name + a.tag).replace("/", "__")
    for s in a.splits.split(","):
        rows = read_rows(root, s)
        if a.limit:
            rows = rows[:a.limit]
        t = time.time()
        ans = rd.read(rows)
        sec = time.time() - t
        pd = root / f"preds_{s}"
        pd.mkdir(parents=True, exist_ok=True)
        with open(pd / f"{name}.jsonl", "w") as f:
            for r, x in zip(rows, ans):
                f.write(json.dumps({"id": r["id"], "model": name, "probs": rd.probs(x)}) + "\n")
        meta = {"name": name, "rows": len(rows), "layout": rd.dio.LAYOUT, "style": rd.dio.STYLE, "base": BASE,
                "host": "gcp", "tta": False, "tta_choice": a.views == 2, "tta_noul": False, "perm_seed": None,
                "load": rd.info, "sec": round(sec), **engine_meta(rd, sec)}
        (pd / f"{name}.meta.json").write_text(json.dumps(meta, indent=2, default=str))
        print(f"{s}: {len(rows)} rows in {sec:.0f}s ({meta['reads_per_sec']} reads/s); wrote preds_{s}/{name}.jsonl",
              flush=True)


def cmd_label(a):
    import shard_golden as sg
    root = Path(a.root).resolve()
    sd = Path(a.shards_dir) if Path(a.shards_dir).is_absolute() else root / a.shards_dir
    shards = sg.shard_files(sd)
    if not shards:
        raise SystemExit(f"no shards in {sd}")
    out_dir = Path(a.out) if a.out else sd / f"labels_{C1}{a.tag}"
    out_dir.mkdir(parents=True, exist_ok=True)
    SETTINGS = settings_for(a.views)
    for sp in shards:  # one label set never mixes settings
        lp, mp = sg.label_paths(out_dir, sp)
        if sg.shard_done(sp, lp, mp) and json.loads(Path(mp).read_text()).get("settings") != SETTINGS:
            raise SystemExit(f"{mp} was labelled with other settings")
    if a.shard is not None:
        shards = [shards[a.shard]]
    reuse, reuse_sha = {}, None  # labels of byte-identical read inputs from the HF path (same C1, same A5 readout)
    if a.reuse:
        reuse = {x["id"]: x["probs"] for x in sg.read_jsonl(Path(a.reuse))}
        reuse_sha = sha256_file(a.reuse)
    rd = Reader(a.port, root / "models" / C1, a.workers, a.chunk, views=a.views)
    for sp in shards:
        lp, mp = sg.label_paths(out_dir, sp)
        if sg.shard_done(sp, lp, mp):
            print(f"{sp.name}: done, skipped", flush=True)
            continue
        mp.unlink(missing_ok=True)  # a stale meta must never vouch for a new label file
        rd.stats = {"rows": 0, "reads": 0, "tokens": 0, "cached_tokens": 0}
        rows = sg.read_jsonl(sp)
        todo = [r for r in rows if r["id"] not in reuse]
        t = time.time()
        ans = iter(rd.read(todo, progress_every=200))
        sec = time.time() - t
        probs = [reuse[r["id"]] if r["id"] in reuse else rd.probs(next(ans)) for r in rows]
        sg.write_atomic(lp, [json.dumps({"id": r["id"], "model": C1, "probs": p}) for r, p in zip(rows, probs)])
        sg.write_json_atomic(mp, {"shard": sp.name, "rows": len(rows), "shard_sha256": sg._sha_file(sp),
                                  "settings": SETTINGS, "style": "cygnet", "sec": round(sec, 1),
                                  "rows_per_sec": round(len(rows) / max(sec, 1e-9), 3),
                                  "load": {**rd.info, "base_commit": None}, "finished_unix": time.time(),
                                  "engine_fast_read": {**engine_meta(rd, sec), "rows_read": len(todo),
                                                       "rows_reused_from_hf_labels": len(rows) - len(todo),
                                                       "reuse_file_sha256": reuse_sha}})
        print(f"{sp.name}: {len(rows)} rows in {sec:.0f}s", flush=True)


# ------------------------------------------------------------------ parity (A49 f)

def argmax(p):
    return max(p, key=p.get)


def compare(ref, got):
    """[(ref probs, fast probs)] -> metrics. label = the reference's argmax answer (the G-block rows carry no gold)."""
    n = len(ref)
    agree = sum(argmax(r) == argmax(g) for r, g in zip(ref, got))
    d_label = [abs(r[argmax(r)] - g[argmax(r)]) for r, g in zip(ref, got)]
    d_max = [max(abs(r[k] - g[k]) for k in r) for r, g in zip(ref, got)]
    q = lambda xs, f: sorted(xs)[min(len(xs) - 1, int(f * len(xs)))]  # noqa: E731
    return {"n": n, "argmax_agree": round(agree / n, 5), "n_disagree": n - agree,
            "frac_dlabel_le_0.02": round(sum(x <= 0.02 for x in d_label) / n, 5),
            "frac_dmax_le_0.02": round(sum(x <= 0.02 for x in d_max) / n, 5),
            "dlabel_p50_p99_max": [round(q(d_label, .5), 5), round(q(d_label, .99), 5), round(max(d_label), 5)],
            "dmax_p50_p99_max": [round(q(d_max, .5), 5), round(q(d_max, .99), 5), round(max(d_max), 5)]}


def cmd_parity(a):
    root = Path(a.root).resolve()
    rows = read_rows(root, a.split)
    refp = {}
    for l in open(root / a.ref):
        if l.strip():
            x = json.loads(l)
            refp[x["id"]] = x["probs"]
    idx = sorted(random.Random(a.seed).sample(range(len(rows)), a.n))
    sample = [rows[i] for i in idx]
    rd = Reader(a.port, root / "models" / C1, a.workers, a.chunk)
    t = time.time()
    ans = rd.read(sample, views=True)
    sec = time.time() - t
    got = [rd.probs(x) for x in ans]
    ref = [refp[r["id"]] for r in sample]
    bad = [r["id"] for r, g in zip(sample, got) if set(refp[r["id"]]) != set(g)]
    if bad:
        raise SystemExit(f"option keys differ from the reference on {len(bad)} rows, e.g. {bad[:3]}")
    out = {"split": a.split, "split_sha256": sha256_file(root / "data" / f"{a.split}.jsonl"),
           "ref": a.ref, "ref_sha256": sha256_file(root / a.ref), "seed": a.seed, "n": a.n,
           "sample_ids_sha256": hashlib.sha256("\n".join(r["id"] for r in sample).encode()).hexdigest(),
           "label_definition": "reference (HF path) argmax answer; the G-block rows carry no gold",
           "views": "choice rows are read in both option orders (given + exact reversal) and averaged, as the reference",
           "all": compare(ref, got)}
    for t_ in ("choice", "noul"):
        sel = [i for i, r in enumerate(sample) if r["qtype"] == t_]
        out[t_] = compare([ref[i] for i in sel], [got[i] for i in sel])
    # near-tie check: reference margin (top1 - top2) of the disagreeing rows
    dis = []
    for r, rf, g in zip(sample, ref, got):
        if argmax(rf) != argmax(g):
            s = sorted(rf.values(), reverse=True)
            dis.append({"id": r["id"], "qtype": r["qtype"], "ref_margin": round(s[0] - s[1], 4),
                        "fast_margin": round(sorted(g.values(), reverse=True)[0] - sorted(g.values(), reverse=True)[1], 4)})
    out["disagreements"] = dis[:60]
    # per-view self-consistency of the fast path on choice rows (the two orders should mostly agree with the average)
    vagree = [argmax(x["view_probabilities"][0]) == argmax(x["view_probabilities"][1]) for x in ans
              if x["type"] == "choice" and "view_probabilities" in x]
    out["fast_view0_view1_argmax_agree"] = round(sum(vagree) / max(1, len(vagree)), 4)
    ok = out["all"]["argmax_agree"] >= 0.995 and out["all"]["frac_dlabel_le_0.02"] >= 0.99
    out["bar"] = {"argmax_agree>=0.995": out["all"]["argmax_agree"] >= 0.995,
                  "frac_dlabel_le_0.02>=0.99": out["all"]["frac_dlabel_le_0.02"] >= 0.99, "PASS": ok}
    out["throughput"] = engine_meta(rd, sec)
    out["utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    Path(a.out).expanduser().write_text(json.dumps(out, indent=1, default=str))
    if a.save_preds:
        with open(Path(a.save_preds).expanduser(), "w") as f:
            for r, g in zip(sample, got):
                f.write(json.dumps({"id": r["id"], "model": C1, "probs": g}) + "\n")
    print(json.dumps({k: out[k] for k in ("all", "choice", "noul", "bar", "throughput")}, indent=1, default=str))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=str(LEAN))
    ap.add_argument("--port", type=int, default=SGL_PORT)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("serve")
    s.add_argument("--model", default="~/models/q35_4b_main500k_merged")
    s.add_argument("--sgl-python", default="~/sgl/bin/python")
    s.add_argument("--log", default="~/jobs/sglang_server.log")
    s.add_argument("--pidfile", default="~/jobs/sglang.pid")
    s.add_argument("--max-running", type=int, default=32)
    s.add_argument("--max-mamba", type=int, default=128)
    s.add_argument("--mem-fraction", type=float, default=0.0)
    s.add_argument("--chunked-prefill", type=int, default=0)
    s.add_argument("--boot-timeout", type=int, default=1200)
    s.add_argument("--extra-args", default="")
    t = sub.add_parser("stop")
    t.add_argument("--pidfile", default="~/jobs/sglang.pid")
    for nm in ("predict", "label", "parity"):
        p = sub.add_parser(nm)
        p.add_argument("--workers", type=int, default=12)
        p.add_argument("--chunk", type=int, default=8)
        if nm != "parity":
            p.add_argument("--views", type=int, choices=(1, 2), default=2,
                           help="2 = choice rows read in both orders (A5, --tta-choice); 1 = given order only (crowd)")
        if nm == "predict":
            p.add_argument("--name", default=C1)
            p.add_argument("--splits", required=True)
            p.add_argument("--tag", default="")
            p.add_argument("--limit", type=int, default=0)
        if nm == "label":
            p.add_argument("--shards-dir", required=True)
            p.add_argument("--shard", type=int, default=None)
            p.add_argument("--out", default="")
            p.add_argument("--tag", default="")
            p.add_argument("--reuse", default="", help="jsonl {id, probs}: HF-path labels to keep instead of reading")
        if nm == "parity":
            p.add_argument("--split", required=True)
            p.add_argument("--ref", required=True)
            p.add_argument("--n", type=int, default=2000)
            p.add_argument("--seed", type=int, required=True)
            p.add_argument("--out", default="~/jobs/parity.json")
            p.add_argument("--save-preds", default="")
    a = ap.parse_args(argv)
    {"serve": cmd_serve, "stop": cmd_stop, "predict": cmd_predict, "label": cmd_label, "parity": cmd_parity}[a.cmd](a)


if __name__ == "__main__":
    main()
