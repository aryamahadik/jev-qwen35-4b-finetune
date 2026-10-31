"""package_di_lang.py: apply the A46 drops, re-balance by seeded down-sampling, run the format gates, write the DI-LANG package.

  python -B package_di_lang.py --dest <dir> [--deny <REPLAY_DENY_A46-style json>] [--unscreened <json>] [--g15]

--dest is the package root: <dest>/out/{candidates_c2.jsonl, candidates_c2.relations.jsonl, mixdev_S5.jsonl, MANIFEST.json}, <dest>/qc/QC_REPORT.json.
Drops only (A46): ids named in --deny / --unscreened are removed; no row is relabelled; balance is by seeded down-sampling (A49 c).
Stage-aware: the QC_REPORT keeps pass=false until the pending gates (G13 on the candidates, A46 complete, C1 crowd selection, pilot) have records.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path[:0] = [str(HERE), str(ROOT.parents[2])]
import di_lang_lib as L  # noqa: E402
from c2_kit import rows as R  # noqa: E402

WORK = ROOT / "work" / "build"
HOVER_MAX, SARC_MAX = 2400, 1200
SARC_C_MAX_SHARE = 0.40
TOK_MEAN_MAX, TOK_CAP = 800, 2000
UTC = "2026-10-17"


def sha_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def jl(p):
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]


def write_jl(p, rows):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    Path(p).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def balance(rows, drops: Counter):
    """Seeded down-sampling: per source, yes share of the yes/no rows in 45-55% (target 50%); iSarcasm task C <= 40% of the source; caps."""
    out = []
    for src, cap in (("c2_di_hover", HOVER_MAX), ("c2_di_isarcasm", SARC_MAX)):
        rr = [r for r in rows if r["source"] == src]
        yn = [r for r in rr if r["qtype"] == "noul"]
        ch = [r for r in rr if r["qtype"] == "choice"]
        y = sorted([r for r in yn if r["gold"] == 1], key=lambda r: L.uh("bal", r["id"]))
        n = sorted([r for r in yn if r["gold"] == 0], key=lambda r: L.uh("bal", r["id"]))
        m = min(len(y), len(n))
        for r in y[m:] + n[m:]:
            drops[f"{src}:balance_down_sample_yes_share"] += 1
        y, n = y[:m], n[:m]
        ch = sorted(ch, key=lambda r: L.uh("balc", r["id"]))
        if src == "c2_di_isarcasm":
            while ch and len(ch) / (len(ch) + len(y) + len(n)) > SARC_C_MAX_SHARE - 0.005:
                ch.pop()
                drops[f"{src}:balance_down_sample_taskC_share"] += 1
        keep = y + n + ch
        if len(keep) > int(cap * 1.5):                       # candidates <= 1.5 x each source's max (A61 c 10); the max itself binds after the crowd selection
            keep = sorted(keep, key=lambda r: L.uh("cap", r["id"]))[:int(cap * 1.5)]
            drops[f"{src}:cap_1.5x"] += len(y + n + ch) - int(cap * 1.5)
        out += keep
    return out


def gates(cands, dev):
    rep = {}
    probs = defaultdict(list)
    for nm, rs in (("candidates", cands), ("dev", dev)):
        for r in rs:
            r2 = json.loads(json.dumps(r))
            r2["meta"]["licence"] = R.LICENCE          # validate_row pins the family licence; this block carries a per-source licence string
            for p in R.validate_row(r2, training=(nm == "candidates")):
                probs[p].append(r["id"])
            if r["qtype"] == "choice":
                if sorted(r["options"]) != sorted(set(r["options"])) or r["gold"] not in r["options"] or len(r["options"]) != 2:
                    probs["choice options"].append(r["id"])
                if len(set(L.ws(o).lower() for o in r["options"])) != 2:
                    probs["choice options differ only in case/space"].append(r["id"])
            if "\n" in "".join(r["options"] or []):
                probs["option newline"].append(r["id"])
    rep["G_schema_validate_row"] = {"problems": {k: len(v) for k, v in probs.items()}, "pass": not probs}
    allr = cands + dev
    ids = Counter(r["id"] for r in allr)
    content = Counter((r["state"], r["instructions"], tuple(r["options"] or [])) for r in allr)
    rec = Counter(r["meta"]["source_record_id"] for r in allr)
    calls = Counter(r["call_id"] for r in allr)
    rep["G12"] = {"duplicate_ids": sum(c > 1 for c in ids.values()), "exact_duplicate_content": sum(c > 1 for c in content.values()),
                  "records_with_more_than_one_row": sum(c > 1 for c in rec.values()), "duplicate_call_ids": sum(c > 1 for c in calls.values()),
                  "near_duplicates": "claims / tweets de-duplicated before selection (word-5-gram Jaccard >= 0.85; drops in BUILD_REPORT)",
                  "hover_groups_shared_by_train_and_dev": len({r["meta"]["hpqa_id"] for r in cands if "hpqa_id" in r["meta"]} &
                                                                {r["meta"]["hpqa_id"] for r in dev if "hpqa_id" in r["meta"]})}
    rep["G12"]["pass"] = all(rep["G12"][k] == 0 for k in ("duplicate_ids", "exact_duplicate_content", "records_with_more_than_one_row",
                                                          "duplicate_call_ids", "hover_groups_shared_by_train_and_dev"))
    toks = [R.approx_tokens(r) for r in cands]
    byb = defaultdict(list)
    for r in cands:
        byb[r["source"]].append(R.approx_tokens(r))
    rep["token_caps"] = {"rows_over_2000": sum(t > TOK_CAP for t in toks), "block_mean": round(sum(toks) / max(1, len(toks)), 1),
                         "block_max": max(toks, default=0), "by_source_mean": {k: round(sum(v) / len(v), 1) for k, v in byb.items()},
                         "pass": all(t <= TOK_CAP for t in toks) and sum(toks) / max(1, len(toks)) <= TOK_MEAN_MAX,
                         "note": "chars/3 estimate, instructions counted twice (spec 3.0); the mixer re-checks with the real tokenizer"}
    wd = Counter(r["meta"]["wording_id"] for r in cands)
    w_by = {s: Counter(r["meta"]["wording_id"] for r in cands if r["source"] == s) for s in {r["source"] for r in cands}}
    rep["wording"] = {"distinct": len(wd), "max_share_block": round(max(wd.values()) / max(1, len(cands)), 4),
                      "max_share_within_task": {t: round(max(c.values()) / sum(c.values()), 4) for t, c in
                                                {tk: Counter(r["meta"]["wording_id"] for r in cands if r["meta"]["task_id"] == tk)
                                                 for tk in {r["meta"]["task_id"] for r in cands}}.items()},
                      "counts": dict(wd), "pass": len(wd) >= 4 and max(wd.values()) / max(1, len(cands)) <= 0.35}
    yn = [r for r in cands if r["qtype"] == "noul"]
    ys = {s: round(sum(r["gold"] for r in yn if r["source"] == s) / max(1, sum(1 for r in yn if r["source"] == s)), 4) for s in {r["source"] for r in yn}}
    rep["G10_yes_share"] = {"by_source": ys, "pass": all(0.45 <= v <= 0.55 for v in ys.values())}
    ch = [r for r in cands if r["qtype"] == "choice"]
    pos = Counter(r["meta"]["gold_pos"] for r in ch)
    iso = [r for r in cands if r["source"] == "c2_di_isarcasm"]
    rep["balance_other"] = {"isarcasm_taskC_share": round(len(ch) / max(1, len(iso)), 4), "taskC_gold_position": dict(pos),
                            "pass": (len(ch) / max(1, len(iso)) <= SARC_C_MAX_SHARE) and (not ch or abs(pos[0] / len(ch) - 0.5) <= 0.05)}
    cards = Counter(r["meta"]["card_id"] for r in cands if r["meta"].get("card_id"))
    rep["rows_per_card"] = {"max": max(cards.values(), default=0), "cards": len(cards), "pass": max(cards.values(), default=0) <= 64}
    rep["caps"] = {"hover_candidates": sum(r["source"] == "c2_di_hover" for r in cands), "isarcasm_candidates": sum(r["source"] == "c2_di_isarcasm" for r in cands),
                   "rule": "candidates <= 1.5 x max per source (hover 3,600; isarcasm 1,800); final <= 2,400 / 1,200 after the crowd selection",
                   "pass": all(sum(r["source"] == s for r in cands) <= int(c * 1.5) for s, c in (("c2_di_hover", HOVER_MAX), ("c2_di_isarcasm", SARC_MAX)))}
    rep["dev_rows"] = {"hover": sum(r["source"] == "c2_di_hover" for r in dev), "isarcasm": sum(r["source"] == "c2_di_isarcasm" for r in dev),
                       "all_dev_only_S5": all(r["meta"]["dev_only"] and r["meta"]["sampler"] == "S5" for r in dev)}
    return rep


def g15(rows):
    bad = []
    for r in rows:
        x = R.g15_check(r)
        if not x.get("ok"):
            bad.append({"id": r["id"], "problems": x.get("problems")})
    return {"rows": len(rows), "failed": len(bad), "failed_ids": [b["id"] for b in bad][:20], "pass": not bad}


def g6_report(cands):
    """Report-only partial-input baselines (A61 c 7): 5-fold CV accuracy of claim-only (HoVer) and length + lexicon (iSarcasm task A) vs the majority share."""
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import cross_val_score
    from sklearn.pipeline import make_pipeline
    out = {}

    def run(name, X, y, vec):
        y = np.array(y)
        pipe = make_pipeline(vec, LogisticRegression(max_iter=1000, C=1.0))
        acc = cross_val_score(pipe, X, y, cv=5, scoring="accuracy")
        out[name] = {"n": len(y), "majority_share": round(max(y.mean(), 1 - y.mean()), 4), "cv_acc": round(float(acc.mean()), 4)}

    hv = [r for r in cands if r["source"] == "c2_di_hover"]
    if hv:
        run("hover_claim_only", [r["state"].split("\n\nPassages:")[0] for r in hv], [r["gold"] for r in hv], TfidfVectorizer(ngram_range=(1, 2), min_df=2))
    ta = [r for r in cands if r["meta"].get("task_kind") == "A"]
    if ta:
        run("isarcasm_A_lexicon", [r["state"] for r in ta], [r["gold"] for r in ta], TfidfVectorizer(ngram_range=(1, 2), min_df=2))
        lens = np.array([[len(r["state"]), len(r["state"].split()), r["state"].count("!"), r["state"].count("?"), sum(c.isupper() for c in r["state"])]
                         for r in ta], dtype=float)
        y = np.array([r["gold"] for r in ta])
        acc = cross_val_score(make_pipeline(__import__("sklearn.preprocessing", fromlist=["x"]).StandardScaler(), LogisticRegression(max_iter=1000)), lens, y, cv=5)
        out["isarcasm_A_length"] = {"n": len(y), "majority_share": round(max(y.mean(), 1 - y.mean()), 4), "cv_acc": round(float(acc.mean()), 4)}
    tc = [r for r in cands if r["meta"].get("task_kind") == "C"]
    if tc:
        longer_is_plain = sum(1 for r in tc if len(r["gold"]) < len([o for o in r["options"] if o != r["gold"]][0])) / len(tc)
        out["isarcasm_C_shorter_option_is_gold_rate"] = round(longer_is_plain, 4)
    out["note"] = "report only; never admits or drops a row (A61 c 7)"
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dest", required=True)
    ap.add_argument("--deny", nargs="*", default=[])
    ap.add_argument("--unscreened", nargs="*", default=[])
    ap.add_argument("--g15", action="store_true")
    ap.add_argument("--g6", action="store_true")
    a = ap.parse_args()
    dest = Path(a.dest)
    cands, dev = jl(WORK / "candidates_raw.jsonl"), jl(WORK / "dev_raw.jsonl")
    deny = set()
    for f in a.deny:
        deny |= set(json.loads(Path(f).read_text())["drop_ids"])
    uns = set()
    for f in a.unscreened:
        uns |= set(json.loads(Path(f).read_text())["drop_ids"])
    drops = Counter()
    n0, d0 = len(cands), len(dev)
    drops["a46_confirmed_candidates"] = sum(r["id"] in deny for r in cands)
    drops["a46_confirmed_dev"] = sum(r["id"] in deny for r in dev)
    drops["a46_unscreened_candidates"] = sum(r["id"] in uns and r["id"] not in deny for r in cands)
    drops["a46_unscreened_dev"] = sum(r["id"] in uns and r["id"] not in deny for r in dev)
    cands = [r for r in cands if r["id"] not in deny and r["id"] not in uns]
    dev = [r for r in dev if r["id"] not in deny and r["id"] not in uns]
    cands = balance(cands, drops)
    cands.sort(key=lambda r: r["id"])
    dev.sort(key=lambda r: r["id"])
    out = dest / "out"
    write_jl(out / "candidates_c2.jsonl", cands)
    write_jl(out / "candidates_c2.relations.jsonl", [])
    write_jl(out / "mixdev_S5.jsonl", dev)
    rep = gates(cands, dev)
    if a.g15:
        rep["G15"] = g15(cands + dev)
    if a.g6:
        rep["G6_report_only"] = g6_report(cands)
    files = {n: {"sha256": sha_file(out / n), "rows": len(jl(out / n))} for n in ("candidates_c2.jsonl", "candidates_c2.relations.jsonl")}
    man = {"family": "DI-LANG", "block": "DI-LANG (A61 b: HoVer + iSarcasmEval English)", "generator": "zed_orch/di_train/DI-LANG/scripts/build_di_lang.py + package_di_lang.py",
           "seed": L.SEED, "parents": [
               {"source": "c2_di_hover", "rows_in": sum(r["source"] == "c2_di_hover" for r in cands), "licence": L.HOVER_LICENCE.split(" (text, claims")[0]},
               {"source": "c2_di_isarcasm", "rows_in": sum(r["source"] == "c2_di_isarcasm" for r in cands), "licence": L.SARC_LICENCE.split(" (text and labels")[0]}],
           "files": files, "mixdev": {"mixdev_S5.jsonl": {"sha256": sha_file(out / "mixdev_S5.jsonl"), "rows": len(dev)}}}
    (out / "MANIFEST.json").write_text(json.dumps(man, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    qc = {"pass": False, "stage": "packaged (round 1); not admitted until the pending gates below have records", "family": "DI-LANG", "fix_iterations": 0,
          "passed_utc": None, "note": "pass is false on purpose (as GB / MD at this stage): G13 on the candidates, the A46 cascade, the C1 crowd selection and the joint DI pilot "
                                      "have not completed. The gates in 'gates_run' did run; none is waived or loosened.",
          "gates_run": rep, "drops": dict(drops), "rows": {"candidates_in": n0, "candidates_out": len(cands), "dev_in": d0, "dev_out": len(dev)},
          "pending": ["G13 seed + candidates + final (A61 e; not run by this step)", "A46 cascade complete (Haiku reads -> Sonnet -> Opus confirm)",
                      "C1 crowd read on the L4 fast path and seeded selection (A61 c 10)", "joint DI pilot (A61 c 11)",
                      "A61 c 1 G1 provenance (provenance/LICENCE_RECORD.json)", "A61 a 5 deny-list (orchestrator)", "A61 a 7 name check on the final mix"],
          "files": {n: {"sha256": v["sha256"]} for n, v in files.items()}}
    (dest / "qc").mkdir(parents=True, exist_ok=True)
    (dest / "qc" / "QC_REPORT.json").write_text(json.dumps(qc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"rows": qc["rows"], "drops": dict(drops), "gates": {k: (v.get("pass") if isinstance(v, dict) else v) for k, v in rep.items()}}, indent=1))


if __name__ == "__main__":
    main()
