"""LongBench v2 data.json -> the kit's item files (in the git-ignored quarantine folder). Prints counts only.

  # real data (pinned revision, sha256 checked); the tokenizer is the scorer's (Qwen3.5-2B and -4B share it)
  opendecide-data/.venv/bin/python bench/longbench_v2/convert.py \\
      --data bench/external_quarantine/longbench_v2/hf_2b48e494/data.json \\
      --tokenizer backups/modal_models/q35_4b_main500k
  # synthetic data (tests): --data bench/longbench_v2/synthetic/data.json --out <dir> --synthetic

Writes to --out (default bench/external_quarantine/longbench_v2/kit/):
  lb_items.jsonl   one line per item: id, split, difficulty, length, domain, sub_domain, set flags, own token counts,
                   question, choice_A..D, context.  NO gold label (run_lb.py reads only this file).
  lb_gold.jsonl    id -> gold letter (score_lb.py only).
  lb_index.jsonl   id, split, difficulty, length, domain, sub_domain and set flags only (no text, no gold).
  lb_meta.json     counts, data sha256, file sha256, set sizes and sha256 of each set's sorted ids.
Rows in OUR format (decoder_io: state = selected context, instructions = question, options = the four choices in A-D
order, letters A-D) are built from these items by lb_lib.final_row once the context is selected (lb_select.py).
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lb_lib as lb  # noqa: E402

FIELDS = ("_id", "domain", "sub_domain", "difficulty", "length", "question", "choice_A", "choice_B", "choice_C",
          "choice_D", "answer", "context")


def own_chunk_tokens(items, tokenizer_dir):
    """Per item: our tokenizer's count of every longjev chunk (the 'context_tokens' longjev sums after recalibrate)."""
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(str(tokenizer_dir))
    out = {}
    for it in items:
        chunks = lb.chunk_state(it["context"])
        if lb.estimate(it["context"]) > lb.CAP_TOKENS:  # not chosen: in no set, not counted (saves ~10 CPU minutes)
            out[it["_id"]] = {"n_chunks": len(chunks), "chunk_tokens_sum": None}
            continue
        ids = tok([c.text for c in chunks], add_special_tokens=False)["input_ids"]
        out[it["_id"]] = {"n_chunks": len(chunks), "chunk_tokens_sum": int(sum(len(x) for x in ids))}
    return out, lb.sha256_file(Path(tokenizer_dir) / "tokenizer.json")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", required=True)
    ap.add_argument("--tokenizer", required=True, help="adapter dir with tokenizer.json (own-token counts)")
    ap.add_argument("--out", default=str(lb.QUARANTINE / "kit"))
    ap.add_argument("--synthetic", action="store_true", help="synthetic test data: skip the real-data sha256 checks")
    a = ap.parse_args(argv)
    data, out = Path(a.data).resolve(), Path(a.out).resolve()
    sha = lb.sha256_file(data)
    real = sha == lb.DATA_SHA256
    if not real and not a.synthetic:
        raise SystemExit(f"{data}: sha256 {sha} is not the pinned LongBench v2 data.json ({lb.DATA_SHA256}); "
                         "pass --synthetic for test data")
    if real and a.synthetic:
        raise SystemExit("--synthetic given for the REAL data file")
    if real and not out.is_relative_to(lb.QUARANTINE):
        raise SystemExit(f"real items must stay under {lb.QUARANTINE}")
    items = json.loads(data.read_text(encoding="utf-8"))
    for it in items:
        miss = [f for f in FIELDS if f not in it]
        if miss:
            raise SystemExit(f"an item lacks fields {miss}")
        if it["answer"] not in lb.LETTERS:
            raise SystemExit("an item's answer is not one of A-D")
    if real and len(items) != lb.DATA_N:
        raise SystemExit(f"expected {lb.DATA_N} items, found {len(items)}")
    dev = lb.dev_ids(items)
    own, tok_sha = own_chunk_tokens(items, a.tokenizer)
    out.mkdir(parents=True, exist_ok=True)
    metas = {}
    with open(out / "lb_items.jsonl", "w", encoding="utf-8") as fi, open(out / "lb_gold.jsonl", "w") as fg, \
            open(out / "lb_index.jsonl", "w") as fx:
        for it in items:
            f = lb.item_flags(it, dev, own[it["_id"]]["chunk_tokens_sum"])
            f["n_chunks"] = own[it["_id"]]["n_chunks"]
            f["dup_options"] = len({it[f"choice_{L}"].strip() for L in lb.LETTERS}) < 4
            metas[it["_id"]] = f
            rec = {"id": it["_id"], **{k: it[k] for k in ("difficulty", "length", "domain", "sub_domain")}, **f,
                   **{k: it[k] for k in ("question", "choice_A", "choice_B", "choice_C", "choice_D", "context")}}
            fi.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fg.write(json.dumps({"id": it["_id"], "gold": it["answer"]}) + "\n")
            fx.write(json.dumps({"id": it["_id"], **{k: it[k] for k in ("difficulty", "length", "domain", "sub_domain")},
                                 **f}) + "\n")
    sets = {}
    for name in lb.SETS:
        ids = sorted(i for i, m in metas.items() if lb.in_set(m, name))
        sets[name] = {"n": len(ids), "ids_sha256": lb.sha256_text("\n".join(ids))}
    chosen = [m for m in metas.values() if m["chosen"]]
    counts = {
        "n_items": len(items), "dev": sum(m["split"] == "dev" for m in metas.values()), "chosen": len(chosen),
        "long_proxy_dev": sets["dev_proxy"]["n"], "long_proxy_test": sets["test_proxy"]["n"],
        "fit_proxy": sets["control_proxy"]["n"], "long_own_dev": sets["dev_own"]["n"],
        "long_own_test": sets["test_own"]["n"], "union_long": sum(m.get("long_proxy") or m.get("long_own")
                                                                    for m in metas.values()),
        "dup_option_items_in_union": sum((m.get("long_proxy") or m.get("long_own")) and m["dup_options"]
                                         for m in metas.values()),
        "chunks_union": sum(m["n_chunks"] for m in metas.values() if m.get("long_proxy") or m.get("long_own")),
        "difficulty_test_proxy": dict(Counter(it["difficulty"] for it in items if lb.in_set(metas[it["_id"]], "test_proxy"))),
        "length_test_proxy": dict(Counter(it["length"] for it in items if lb.in_set(metas[it["_id"]], "test_proxy"))),
    }
    if real:
        got = {"chosen": counts["chosen"], "long_dev": counts["long_proxy_dev"], "long_test": counts["long_proxy_test"],
               "fit": counts["fit_proxy"]}
        if got != lb.EXPECT_PROXY:
            raise SystemExit(f"reconstructed item set drifted: {got} != {lb.EXPECT_PROXY}")
    meta = {"data": str(data), "data_sha256": sha, "real": real, "data_repo": lb.DATA_REPO,
            "data_revision": lb.DATA_REVISION if real else None, "tokenizer": str(a.tokenizer),
            "tokenizer_json_sha256": tok_sha, "longjev_commit": lb.LONGJEV_COMMIT,
            "rules": {"cap_tokens": lb.CAP_TOKENS, "chars_per_token": lb.CHARS_PER_TOKEN,
                      "jev_proxy_chars_per_token": lb.JEV_PROXY_CPT, "fit_margin": lb.FIT_MARGIN,
                      "max_budget": lb.MAX_BUDGET, "dev_size": lb.DEV_SIZE, "chunk_tokens": lb.CHUNK_TOKENS},
            "counts": counts, "sets": sets,
            "files": {"lb_items.jsonl": lb.sha256_file(out / "lb_items.jsonl"),
                      "lb_gold.jsonl": lb.sha256_file(out / "lb_gold.jsonl"),
                      "lb_index.jsonl": lb.sha256_file(out / "lb_index.jsonl")},
            "convert_py_sha256": lb.sha256_file(__file__), "lb_lib_sha256": lb.sha256_file(lb.__file__)}
    (out / "lb_meta.json").write_text(json.dumps(meta, indent=2))
    print(json.dumps({"convert": {"real": real, "out": str(out), **counts}}, indent=1))
    return meta


if __name__ == "__main__":
    main()
