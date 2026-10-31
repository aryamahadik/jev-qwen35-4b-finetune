"""Counts-only probe of the F3 pool for cue design + MiniLM truncation/case checks (no row text printed)."""
import json, os, re, sys, collections
sys.dont_write_bytecode = True
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/common")
import g8_aflite as T  # noqa: E402
import numpy as np  # noqa: E402

fam = sys.argv[1] if len(sys.argv) > 1 else "F3"
pool = T.LEAN / f"c_src/{fam}/out/candidates_r1.jsonl"
rows, sha = T.load_pool(pool); views = T.pool_views(fam, rows)
out = {"family": fam, "pool_sha256": sha, "n_rows": len(rows)}
PAIRS = [("must", "has to"), ("allowed", "permitted"), ("can", "may"), ("does", "would"), ("is", "would be"),
         ("the", "this"), ("any", "every"), ("before", "prior to"), ("after", "following"), ("only", "solely")]
yes = [i for i, r in enumerate(rows) if T.part_of(r) == "yes_no" and int(r["gold"]) == 1]
ch = [i for i, r in enumerate(rows) if T.part_of(r) == "choice"]
cov = {}
for a, b in PAIRS:
    rx = re.compile(rf"\b{a}\b")
    cov[a] = {"yes_q": round(sum(bool(rx.search(" ".join(views[i][0][0]))) for i in yes) / max(1, len(yes)), 3),
              "gold_opt": round(sum(bool(rx.search(views[i][1][T.labels_of(T.ADAPTERS[fam], rows[i])[0]]))
                                    for i in ch) / max(1, len(ch)), 3)}
out["swap_coverage"] = cov
ks = collections.Counter(len(views[i][1]) for i in ch); out["k_hist"] = dict(sorted(ks.items()))
ow = [len(o.split()) for i in ch for o in views[i][1]]
out["opt_words"] = {"mean": round(float(np.mean(ow)), 2), "p10": float(np.percentile(ow, 10)),
                    "p90": float(np.percentile(ow, 90)), "share_ge2": round(float(np.mean(np.array(ow) >= 2)), 3)}
st_chunks = [len(views[i][0][2]) for i in yes]; out["state_chunks_yes"] = dict(collections.Counter(st_chunks))
qw = [len(" ".join(v[0][0]).split()) for v in views]
out["q_words"] = {"p50": float(np.percentile(qw, 50)), "p99": float(np.percentile(qw, 99)), "max": int(max(qw))}
# truncation: MiniLM max_seq_length; share of embedded texts longer than it (tokens beyond are invisible)
from transformers import AutoTokenizer  # noqa: E402
tok = AutoTokenizer.from_pretrained(T.MODEL)
texts = list(dict.fromkeys(T.all_texts(views)))
lens = np.array([len(x) for x in tok(texts, add_special_tokens=True)["input_ids"]])
by = {"q": [], "card": [], "state": [], "opt": []}
for segs, opts in views:
    for name, seg in zip(("q", "card", "state"), segs):
        by[name] += seg
    by["opt"] += opts or []
tl = dict(zip(texts, lens.tolist()))
out["do_lower_case"] = bool(getattr(tok, "do_lower_case", None)) if hasattr(tok, "do_lower_case") else str(
    tok.backend_tokenizer.normalizer)[:120]
out["truncation_256"] = {k: {"n": len(v), "share_over_256": round(float(np.mean([tl[t] > 256 for t in v])), 4),
                             "share_over_128": round(float(np.mean([tl[t] > 128 for t in v])), 4)}
                         for k, v in by.items() if v}
print(json.dumps(out))
(T.LEAN / f"c_build/g8v2/verify_stats/probe_{fam}.json").write_text(json.dumps(out, indent=1))
