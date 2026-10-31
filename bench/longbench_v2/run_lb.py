"""Run ONE OpenDecide model on LongBench v2 in longjev's "Jev keeps 8K tokens" protocol (L4 runner, once per model).

  # on od-l4 ONLY after the owner's OK; one model per call; nothing else on the GPU
  cd ~/bench/longbench_v2 && HF_HOME=$HOME/hf HF_HUB_OFFLINE=1 ~/od/bin/python run_lb.py \\
      --model ~/lean/models/q35_4b_main500k --base Qwen/Qwen3.5-4B \\
      --revision 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a --choice-readout 2view \\
      --items ~/bench/external_quarantine/longbench_v2/kit/lb_items.jsonl
  # CPU tests (no GPU, no weights): a tiny random model with the adapter's real tokenizer and prompt layout
  opendecide-data/.venv/bin/python bench/longbench_v2/run_lb.py --fake-model --model <adapter dir> \\
      --base Qwen/Qwen3.5-4B --choice-readout 2view --items <synthetic kit>/lb_items.jsonl --out <dir>

Per item (lb_select.py): chunk -> one yes/no relevance read per chunk with this model -> keep 8K of this model's tokens
-> the four-option question over the kept text, read with --choice-readout (C1's committed A5 readout: 2view = given
order + exact reversal, averaged; yes/no rows are always one read). The model is loaded with
decoder_io.load(base, adapter=..., revision=...) (layout, style and PRISM-X from the adapter's own files) and merged,
as run_v154.py does. This script never reads gold labels and prints counts and timings only.

Writes <out>/preds.jsonl (per item: kept chunk ids, budget, token counts, A-D probabilities, predicted letter,
timings), <out>/chunk_scores.jsonl (per item: P(yes) and our token count per chunk; reused by cascade_lb.py),
<out>/manifest.json (model + data + code sha256, settings, timings). On REAL data a ledger
(runs/LEDGER.jsonl next to this script) refuses a second run of the same adapter; --resume only continues the SAME
interrupted run (same settings), it never re-reads finished items.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import platform
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lb_lib as lb  # noqa: E402
import lb_select as sel  # noqa: E402

LEDGER = HERE / "runs" / "LEDGER.jsonl"


def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def gpu_users():
    try:
        out = subprocess.run(["nvidia-smi", "--query-compute-apps=pid,process_name,used_memory", "--format=csv,noheader"],
                             capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception:
        return None
    return out or ""


def adapter_files_sha(model_dir: Path) -> dict:
    return {p.name: lb.sha256_file(p) for p in sorted(model_dir.iterdir()) if p.is_file()}


def tiny_model(tok):
    """run_v154.tiny_model: a random 1-layer Qwen3 with the real vocabulary (CPU); answers are noise."""
    import torch
    from transformers import Qwen3Config, Qwen3ForCausalLM
    torch.manual_seed(0)
    cfg = Qwen3Config(vocab_size=len(tok), hidden_size=32, intermediate_size=64, num_hidden_layers=1,
                      num_attention_heads=2, num_key_value_heads=1, head_dim=16, max_position_embeddings=65536,
                      tie_word_embeddings=False)
    return Qwen3ForCausalLM(cfg).eval()


def load_reader(dio, model_dir, base, revision, fake):
    """(model, tok, info, dev). GPU: decoder_io.load + merge_and_unload (run_v154.py). Fake: layout/style from the
    adapter's train_meta, real tokenizer, tiny random model on CPU."""
    if not fake:
        model, tok, info = dio.load(base, "cuda", adapter=str(model_dir), revision=revision, return_info=True)
        model = model.merge_and_unload()
        model.eval()
        return model, tok, info, "cuda"
    from transformers import AutoTokenizer
    info = sel.set_prompt_layout(dio, model_dir, base, revision)
    info = {**info, "layout": dio.LAYOUT, "style": dio.STYLE,
            "prism_x": (Path(model_dir) / "prism_x.json").exists(),
            "note": "fake-model: layout/style from train_meta, tiny random model, PRISM-X not exercised"}
    tok = AutoTokenizer.from_pretrained(str(model_dir))
    tok.padding_side = "right"
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    return tiny_model(tok), tok, info, "cpu"


def prism_active(dio, model) -> bool:
    pxm = dio._prism_x()
    return bool(pxm is not None and pxm.active_for(dio._parts(model)[0]))


class Reader:
    """One model behind the kit: token counts, the MAX_LEN guard, PRISM-X span checks, guarded reads."""

    def __init__(self, dio, model, tok, dev, choice_readout, batch_size, token_budget):
        self.dio, self.model, self.tok, self.dev = dio, model, tok, dev
        self.ro = dio.Readout(tok)
        self.choice_readout, self.batch_size, self.token_budget = choice_readout, batch_size, token_budget
        self.px = prism_active(dio, model)

    def prompt_tokens(self, row) -> int:
        return len(self.tok(self.ro.prompt(row), add_special_tokens=False)["input_ids"])

    def readable(self, row) -> bool:
        if self.px:  # PRISM-X must find the token-role spans in the exact chat text, or the row is not read
            import prism_x
            try:
                prism_x.row_char_spans(row, None, self.ro.prompt(row))
            except Exception:
                return False
        return True

    def read(self, rows):
        """Reads rows; a batch that raises (e.g. out of memory) is retried row by row; rows that still fail -> None."""
        import torch
        try:
            return lb.read_rows(self.dio, self.model, self.ro, rows, self.dev, self.choice_readout, self.batch_size,
                                self.token_budget)
        except Exception as exc:  # noqa: BLE001
            if self.dev == "cuda":
                torch.cuda.empty_cache()
            print(json.dumps({"read_retry": {"rows": len(rows), "error": type(exc).__name__}}), flush=True)
        out = []
        for r in rows:
            try:
                out.append(lb.read_rows(self.dio, self.model, self.ro, [r], self.dev, self.choice_readout, 1,
                                        self.token_budget)[0])
            except Exception:  # noqa: BLE001
                if self.dev == "cuda":
                    torch.cuda.empty_cache()
                out.append(None)
        return out


def sync(dev):
    if dev == "cuda":
        import torch
        torch.cuda.synchronize()


def score_chunks(reader, item, max_len):
    """Steps 1-3: chunks (sizes = our tokens) and P(yes) per chunk; a chunk whose prompt is over the reader's window or
    that fails to read gets score 0 and is listed as failed (longjev: a failed chunk request scores 0)."""
    chunks_r, rows = sel.prepare(item, reader.tok)
    ptoks = [reader.prompt_tokens(r) for r in rows]
    ok = [i for i, (r, n) in enumerate(zip(rows, ptoks)) if n <= max_len and reader.readable(r)]
    reads = reader.read([rows[i] for i in ok]) if ok else []
    rel = [0.0] * len(rows)
    failed = sorted(set(range(len(rows))) - set(ok))
    read_tokens = sum(ptoks[i] for i in ok)
    for i, rd in zip(ok, reads):
        if rd is None:
            failed.append(i)
        else:
            rel[i] = rd["p_yes"]
    return chunks_r, rel, sorted(failed), read_tokens


def final_read(reader, item, chunks_r, kept, max_len):
    """Steps 5-7 and the answer: the kept text in document order, the too-long retry, one A5 read of the question."""
    row, used, drops = sel.assemble(item, chunks_r, kept, reader.prompt_tokens, max_len)
    rec = {"kept": sorted(used), "n_kept": len(used), "too_long_drops": drops,
           "kept_tokens": sum(chunks_r[i].est_tokens for i in used),
           "kept_chars": sum(len(chunks_r[i].text) for i in used)}
    if row is None or not reader.readable(row):
        return {**rec, "final_failed": "too_long" if row is None else "prism_x_spans", "p1": None, "p": None,
                "pred": None, "pred_1view": None, "final_prompt_tokens": None}
    rec["final_prompt_tokens"] = reader.prompt_tokens(row)
    rd = reader.read([row])[0]
    if rd is None:
        return {**rec, "final_failed": "read_error", "p1": None, "p": None, "pred": None, "pred_1view": None}
    return {**rec, "final_failed": None, "p1": rd["p1"], "p": rd["p"], "pred": lb.argmax_letter(rd["p"]),
            "pred_1view": lb.argmax_letter(rd["p1"])}


def check_items(items_path: Path):
    meta = json.loads((items_path.parent / "lb_meta.json").read_text())
    sha = lb.sha256_file(items_path)
    if sha != meta["files"]["lb_items.jsonl"]:
        raise SystemExit(f"{items_path}: sha256 differs from lb_meta.json (re-run convert.py)")
    real = bool(meta["real"]) and meta["data_sha256"] == lb.DATA_SHA256
    return meta, sha, real


def ledger_check(real, adapter_sha, out, resume):
    if not real or not LEDGER.exists():
        return
    for e in lb.read_jsonl(LEDGER):
        if e.get("adapter_sha256") == adapter_sha and e.get("data_sha256") == lb.DATA_SHA256:
            if resume and e.get("out") == str(out):
                continue
            raise SystemExit(f"STOP (run once per model): the ledger already has a LongBench v2 run of this adapter: "
                             f"{e.get('name')} {e.get('event')} {e.get('utc')} -> {e.get('out')}")


def ledger_append(real, rec):
    if not real:
        return
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with open(LEDGER, "a") as f:
        f.write(json.dumps(rec) + "\n")


def default_lean():
    return sel.default_lean()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True, help="adapter dir (train_meta.json, adapter, prism_x.* if any)")
    ap.add_argument("--base", required=True)
    ap.add_argument("--revision", default=None, help="exact Hugging Face commit of the base")
    ap.add_argument("--items", required=True, help="convert.py's lb_items.jsonl (lb_meta.json next to it)")
    ap.add_argument("--choice-readout", required=True, choices=["2view", "single"],
                    help="the model's committed readout for choice rows (C1: 2view)")
    ap.add_argument("--name", default=None)
    ap.add_argument("--out", default=None, help="default: runs/lb2_<name> next to this script")
    ap.add_argument("--lean", default=default_lean())
    ap.add_argument("--sets", default="all_proxy,all_own", help="items to run: union of these lb_lib.SETS")
    ap.add_argument("--control", action="store_true",
                    help="SECONDARY: also read the items that fit (control_proxy) WHOLE, longjev's 'direct' arm")
    ap.add_argument("--control-max-len", type=int, default=32768,
                    help="decoder_io.MAX_LEN for the control reads (runtime override; the 8K arm uses the default)")
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--token-budget", type=int, default=12000)
    ap.add_argument("--limit", type=int, default=0, help="synthetic data only: first N items")
    ap.add_argument("--fake-model", action="store_true")
    ap.add_argument("--allow-shared-gpu", action="store_true")
    ap.add_argument("--resume", action="store_true", help="continue THIS interrupted run (same out, same settings)")
    a = ap.parse_args(argv)

    model_dir = Path(a.model).expanduser().resolve()
    items_path = Path(a.items).expanduser().resolve()
    lean = Path(a.lean).expanduser().resolve()
    meta_items, items_sha, real = check_items(items_path)
    if real and a.limit:
        raise SystemExit("--limit is for synthetic data only: the real test runs whole, once")
    if real and a.fake_model:
        raise SystemExit("--fake-model on REAL items is not allowed (use synthetic items)")
    name = a.name or model_dir.name
    out = Path(a.out).expanduser().resolve() if a.out else HERE / "runs" / f"lb2_{name}{'_fake' if a.fake_model else ''}"
    sets = tuple(a.sets.split(","))
    for s in sets:
        if s not in lb.SETS:
            raise SystemExit(f"unknown set {s}; known: {list(lb.SETS)}")
    afiles = adapter_files_sha(model_dir)
    adapter_sha = afiles.get("adapter_model.safetensors")
    if real and not adapter_sha:
        raise SystemExit(f"{model_dir}: no adapter_model.safetensors, so the once-per-model ledger cannot key this run")
    settings = {"protocol": "longjev jev@8000 (lb_lib.py)", "budget": lb.BUDGET, "chunk_tokens": lb.CHUNK_TOKENS,
                "chars_per_token": lb.CHARS_PER_TOKEN, "cap_tokens": lb.CAP_TOKENS, "jev_proxy_cpt": lb.JEV_PROXY_CPT,
                "gap_tokens": lb.GAP_TOKENS, "too_long_retries": sel.TOO_LONG_RETRIES, "sets": list(sets),
                "control": a.control, "control_max_len": a.control_max_len if a.control else None,
                "choice_readout": a.choice_readout, "noul_readout": "single", "batch_size": a.batch_size,
                "token_budget": a.token_budget, "base": a.base, "revision": a.revision, "adapter_sha256": adapter_sha,
                "items_sha256": items_sha, "data_sha256": meta_items["data_sha256"], "limit": a.limit,
                "fake_model": a.fake_model}
    settings_sha = lb.sha256_text(json.dumps(settings, sort_keys=True))
    ledger_check(real, adapter_sha, out, a.resume)
    done = set()
    if out.exists():
        if not a.resume:
            raise SystemExit(f"{out} exists (a run of this model was started); --resume continues it, nothing re-runs")
        old = json.loads((out / "manifest.json").read_text())
        if old.get("settings_sha256") != settings_sha:
            raise SystemExit("--resume: settings differ from the interrupted run; refusing")
        if old.get("status") == "complete":
            raise SystemExit(f"{out}: this run is complete; it is not run again")
        done = {r["id"] for r in lb.read_jsonl(out / "preds.jsonl")} if (out / "preds.jsonl").exists() else set()
    mode = "fake-model" if a.fake_model else "gpu"
    users = None
    if mode == "gpu":
        users = gpu_users()
        if users is None:
            raise SystemExit("nvidia-smi not found: no GPU here (use --fake-model for CPU checks)")
        if users and not a.allow_shared_gpu:
            raise SystemExit("the GPU is in use, refusing to start:\n" + users)

    all_items = lb.read_jsonl(items_path)
    items = [it for it in all_items if any(lb.in_set(it, s) for s in sets)]
    if a.limit:
        items = items[: a.limit]
    controls = [it for it in all_items if lb.in_set(it, "control_proxy")] if a.control else []
    if a.limit and controls:
        controls = controls[: a.limit]

    sys.path.insert(0, str(lean))
    import torch
    import decoder_io as dio
    t_load = time.time()
    model, tok, info, dev = load_reader(dio, model_dir, a.base, a.revision, a.fake_model)
    reader = Reader(dio, model, tok, dev, a.choice_readout, a.batch_size, a.token_budget)
    if info.get("prism_x") and not reader.px and not a.fake_model:
        raise SystemExit("the adapter has PRISM-X files but no control plane is active after load")
    tok_sha = lb.sha256_file(model_dir / "tokenizer.json") if (model_dir / "tokenizer.json").exists() else None
    if tok_sha and meta_items.get("tokenizer_json_sha256") and tok_sha != meta_items["tokenizer_json_sha256"]:
        raise SystemExit("this adapter's tokenizer differs from the one convert.py counted with (own-token sets)")
    max_len = dio.MAX_LEN
    out.mkdir(parents=True, exist_ok=True)
    manifest = {
        "name": name, "mode": mode, "status": "running", "settings": settings, "settings_sha256": settings_sha,
        "model_dir": str(model_dir), "adapter_files_sha256": afiles, "load": info, "prism_x_active": reader.px,
        "items": str(items_path), "items_meta": {k: meta_items[k] for k in ("data_sha256", "real", "data_revision",
                                                                              "counts", "sets")},
        "n_items": len(items), "n_control": len(controls), "max_len": max_len,
        "code_sha256": {"run_lb.py": lb.sha256_file(__file__), "lb_lib.py": lb.sha256_file(lb.__file__),
                        "lb_select.py": lb.sha256_file(sel.__file__), "decoder_io.py": lb.sha256_file(dio.__file__),
                        "prism_x.py": lb.sha256_file(lean / "prism_x.py") if (lean / "prism_x.py").exists() else None},
        "host": platform.node(), "python": sys.version.split()[0], "torch": torch.__version__,
        "started_utc": utc(), "resumed_with_done": len(done), "longjev_commit": lb.LONGJEV_COMMIT,
    }
    try:
        import transformers
        manifest["transformers"] = transformers.__version__
    except Exception:  # noqa: BLE001
        pass
    if mode == "gpu":
        manifest["gpu"] = torch.cuda.get_device_name(0)
        manifest["gpu_users_before_load"] = users
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))
    ledger_append(real, {"event": "start", "name": name, "adapter_sha256": adapter_sha, "data_sha256": lb.DATA_SHA256,
                         "settings_sha256": settings_sha, "out": str(out), "utc": utc()})
    if mode == "gpu":
        dio.warmup(model, reader.ro, max_tokens=8192, batch_sizes=(1,))
    manifest["load_and_warmup_s"] = round(time.time() - t_load, 1)
    print(json.dumps({"run_lb": {"name": name, "mode": mode, "items": len(items), "done": len(done),
                                 "control": len(controls), "layout": dio.LAYOUT, "style": dio.STYLE,
                                 "prism_x": reader.px, "readout": a.choice_readout}}), flush=True)

    tot = {"score_s": 0.0, "final_s": 0.0, "rel_prompt_tokens": 0, "chunks": 0, "failed_chunks": 0, "final_failed": 0}
    with open(out / "preds.jsonl", "a") as fp, open(out / "chunk_scores.jsonl", "a") as fc:
        for k, it in enumerate(items):
            if it["id"] in done:
                continue
            sync(dev)
            t0 = time.perf_counter()
            chunks_r, rel, failed, read_tokens = score_chunks(reader, it, max_len)
            sync(dev)
            t1 = time.perf_counter()
            kept, budget = sel.keep(it, chunks_r, rel)
            fin = final_read(reader, it, chunks_r, kept, max_len)
            sync(dev)
            t2 = time.perf_counter()
            rec = {"id": it["id"], "arm": "keep8k", "sets": [s for s in lb.SETS if lb.in_set(it, s)],
                   "n_chunks": len(chunks_r), "failed_chunks": len(failed), "budget": budget,
                   "context_tokens_own": sum(c.est_tokens for c in chunks_r), **fin,
                   "rel_prompt_tokens_read": read_tokens, "score_s": round(t1 - t0, 3), "final_s": round(t2 - t1, 3)}
            # chunk scores first: preds.jsonl marks an item done (--resume), so a stop between the two writes re-runs
            # the item instead of leaving it without the chunk scores cascade_lb.py needs
            fc.write(json.dumps({"id": it["id"], "p_yes": rel, "tokens": [c.est_tokens for c in chunks_r],
                                 "failed": failed}) + "\n")
            fc.flush()
            fp.write(json.dumps(rec) + "\n")
            fp.flush()
            tot["score_s"] += t1 - t0
            tot["final_s"] += t2 - t1
            tot["rel_prompt_tokens"] += read_tokens
            tot["chunks"] += len(chunks_r)
            tot["failed_chunks"] += len(failed)
            tot["final_failed"] += fin["final_failed"] is not None
            if (k + 1) % 10 == 0 or k + 1 == len(items):
                print(json.dumps({"progress": f"{k + 1}/{len(items)}", "chunks": tot["chunks"],
                                  "score_s": round(tot["score_s"], 1), "final_s": round(tot["final_s"], 1)}), flush=True)
        if controls:  # SECONDARY: longjev's "direct" arm (inputs that fit go to the model whole)
            dio.MAX_LEN = a.control_max_len
            for it in controls:
                if it["id"] + "#control" in done:
                    continue
                sync(dev)
                t0 = time.perf_counter()
                row = lb.final_row(it, it["context"])
                n = reader.prompt_tokens(row)
                rd = reader.read([row])[0] if n <= a.control_max_len and reader.readable(row) else None
                sync(dev)
                rec = {"id": it["id"] + "#control", "item": it["id"], "arm": "direct", "sets": ["control_proxy"],
                       "final_prompt_tokens": n, "final_failed": None if rd else "too_long_or_error",
                       "p1": rd and rd["p1"], "p": rd and rd["p"], "pred": rd and lb.argmax_letter(rd["p"]),
                       "pred_1view": rd and lb.argmax_letter(rd["p1"]), "final_s": round(time.perf_counter() - t0, 3)}
                fp.write(json.dumps(rec) + "\n")
                fp.flush()
            dio.MAX_LEN = max_len
    manifest.update({"status": "complete", "finished_utc": utc(), "totals_this_session": {
        **{k: (round(v, 1) if isinstance(v, float) else v) for k, v in tot.items()},
        "rel_tokens_per_s": round(tot["rel_prompt_tokens"] / tot["score_s"], 1) if tot["score_s"] else None}})
    if mode == "gpu":
        manifest["max_memory_gb"] = round(torch.cuda.max_memory_allocated() / 2 ** 30, 2)
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))
    ledger_append(real, {"event": "complete", "name": name, "adapter_sha256": adapter_sha,
                         "data_sha256": lb.DATA_SHA256, "settings_sha256": settings_sha, "out": str(out), "utc": utc()})
    print(json.dumps({"done": str(out), **manifest["totals_this_session"]}), flush=True)
    print(f"score: python {HERE / 'score_lb.py'} --run {out} --kit {items_path.parent}")
    return out


if __name__ == "__main__":
    main()
