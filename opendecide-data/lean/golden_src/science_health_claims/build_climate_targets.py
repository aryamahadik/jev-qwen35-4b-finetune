"""Build raw rows for climate_targets (Climate Policy Radar national climate targets training dataset; Juhasz et al.,
"Identifying Climate Targets in National Laws and Policies using Machine Learning", arXiv:2404.02822, 2024).

Source : HF ClimatePolicyRadar/national-climate-targets pinned to revision e811996454164cadb4d608f6b4d9db0eaf843ae1,
         data/train-00000-of-00001.parquet (the only split; the dataset has no test split).
Licence: CC BY 4.0 (dataset card, "## License: Our dataset is licensed as CC by 4.0"; the underlying Climate Change
         Laws of the World data is also CC BY per LSE Grantham's CCLW terms).
Texts  : passages from national climate laws, policies and UNFCCC submissions (Climate Policy Radar database).
         Passages machine-translated with the Google Cloud Translation API (translated=True) are DROPPED (not
         human-written English).
Labels : multi-label target types annotated by three domain experts (inter-annotator agreement monitored, post-hoc
         review): Net zero (NZT), Reduction (GHG emissions reduction), Other (any other target, e.g. renewables).
         A target = an aim to achieve a specific outcome that is quantifiable and has a deadline. The card says
         annotator 2's labels combine 'sampling negatives' with post-hoc error fixes, so annotator-2 NEGATIVES are
         dropped (they may be unreviewed sampled negatives); annotator-2 positives are kept.
Questions (each passage used once; yes/no):
  any : "Does this passage set a climate or energy target, i.e. a specific quantified outcome with a deadline?"
        yes = any target label; no = no target.
  nzt : "Does this passage set a net-zero target?"  yes = NZT; no = reduction-only / other-only passages (hard: a
        target of another type) or no target.
  red : "Does this passage set a greenhouse-gas emissions reduction target?"  yes = Reduction (and not NZT);
        no = other-only passages (hard: e.g. renewable-energy or efficiency targets) or no target. NZT passages are
        never used for 'red' because the taxonomy separates the two labels.
Text   : single PDF line breaks inside a paragraph are joined with a space (no other edits).
Dedupe : exact/near-duplicate passages; decontamination (label-NLI, local train/dev/eval, JevBench public).
Review fix (strict reviewer, 29 Sep): (1) the source has overlapping passage windows (one passage a sub-span of
         another, word Jaccard ~0.77, so the 0.85 near-dup filter missed them): passages sharing >= 50% of their
         8-word shingles with an earlier kept passage are now dropped, and when a contained passage carries a target
         label that its container lacks, BOTH are dropped (the container's label is then incomplete). (2) An audit of
         the 'any' negatives found unlabelled targets ("adopt an ambitious goal to reduce its GHG emissions in 2030
         ... by 20%", "100% diffusion of LED by FY2030"); a 'none' passage is no longer used as an 'any' negative when
         it both names a target/goal/commitment and has a quantity tied to a year.
Deterministic (seed 20261118). CPU only.
"""
import collections
import random
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _shc_common as C  # noqa: E402

KEY = "climate_targets"
SEED = 20261118
REV = "e811996454164cadb4d608f6b4d9db0eaf843ae1"
URL = f"https://huggingface.co/datasets/ClimatePolicyRadar/national-climate-targets/resolve/{REV}/"
FILES = {"data/train-00000-of-00001.parquet": "8a33acdaf21c7975f501fa12cde892a0a77088725bb1c9d11517137c3f8a9018",
         "README.md": "78b3431633b6e1e3eb882ea66a5a3122d3fe6cad0e33a0241e214c5e2a79537f"}
LICENCE = (f"CC BY 4.0 (dataset card https://huggingface.co/datasets/ClimatePolicyRadar/national-climate-targets/"
           f"blob/{REV}/README.md, '## License: Our dataset is licensed as CC by 4.0')")
DATASET = "ClimatePolicyRadar/national-climate-targets"
QUESTIONS = {
    "any": "Does this passage set a climate or energy target, i.e. a specific quantified outcome with a deadline?",
    "nzt": "Does this passage set a net-zero target?",
    "red": "Does this passage set a greenhouse-gas emissions reduction target?",
}
DEFS = {
    "any": {
        "yes": "The passage commits to at least one target that meets all three tests: an aim to achieve a specific "
               "outcome (emissions, renewable share, efficiency, forest cover, etc.), a quantified level or amount, "
               "and a deadline or time frame (a target year, 'within two years', 'by the end of the plan period').",
        "no": "No statement in the passage meets all three tests: it only gives general goals without a number or "
              "without a deadline, describes measures, institutions or past data, or reports projections that are "
              "not commitments.",
    },
    "nzt": {
        "yes": "The passage commits to a net-zero target: balancing greenhouse-gas emissions with removals by a "
               "deadline (net zero, carbon or climate neutrality, zero net emissions), economy-wide or for a sector.",
        "no": "The passage has no net-zero commitment: it has no target, or only other target types such as a "
              "percentage cut in emissions, a renewable-energy share or an efficiency goal.",
    },
    "red": {
        "yes": "The passage commits to a quantified reduction of greenhouse-gas emissions by a deadline, economy-wide "
               "or for a sector (e.g. '30% below 1990 levels by 2030', 'x% below business-as-usual by 2025').",
        "no": "The passage has no greenhouse-gas emissions reduction target: it has no target, or only other target "
              "types such as renewable-energy shares, energy-efficiency, forest-cover or access goals.",
    },
}


TARGET_WORD = re.compile(r"\b(targets?|goals?|commit\w*|pledg\w*|objectives?|aims?)\b", re.I)
QTY_YEAR = re.compile(r"\d+(\.\d+)?\s?(%|per ?cent|percent|MW|GW|TWh|GWh|mil)[^.]{0,80}\b(by|in|until|before)\s+"
                      r"(the end of\s+)?(FY\s?)?(19|20)\d\d|\b(by|until|before)\s+(FY\s?)?(19|20)\d\d[^.]{0,80}"
                      r"\d+(\.\d+)?\s?(%|per ?cent|percent|MW|GW)", re.I)


def shingles(t, k=8):
    w = C.words(t)
    return {hash(tuple(w[i:i + k])) for i in range(len(w) - k + 1)}


def containment_filter(recs, stats):
    """Drop passages that overlap an earlier kept passage (>= 50% of the smaller one's 8-word shingles); when the
    smaller passage has a target label the larger lacks (>= 80% containment), drop both."""
    sh = [shingles(r["text"]) for r in recs]
    labs = [{k for k in ("nzt", "red", "oth") if r[k]} for r in recs]
    owner = {}
    drop = set()
    for i, s in enumerate(sh):
        cands = {}
        for h in s:
            j = owner.get(h)
            if j is not None:
                cands[j] = cands.get(j, 0) + 1
        for j, n in cands.items():
            m = min(len(s), len(sh[j])) or 1
            if n / m >= 0.5:
                drop.add(i)
                small, big = (i, j) if len(s) <= len(sh[j]) else (j, i)
                if n / m >= 0.8 and not labs[small] <= labs[big]:
                    drop.add(j)
                    stats["drop_container_label_conflict"] += 1
        if i not in drop:
            for h in s:
                owner.setdefault(h, i)
    stats["drop_overlapping_window"] += len(drop)
    return [r for i, r in enumerate(recs) if i not in drop]


def main():
    rng = random.Random(SEED)
    cache = C.CACHE / KEY
    paths = {f: C.fetch(URL + f, cache / Path(f).name, sha) for f, sha in FILES.items()}
    df = pd.read_parquet(paths["data/train-00000-of-00001.parquet"])
    stats = collections.Counter()
    stats["all"] = len(df)
    recs, seen = [], set()
    for i, r in enumerate(df.to_dict("records")):
        nzt, red, oth = int(r["annotation_NZT"]), int(r["annotation_Reduction"]), int(r["annotation_Other"])
        if bool(r["translated"]):
            stats["drop_machine_translated"] += 1
            continue
        if int(r["annotation_agent"]) == 2 and nzt + red + oth == 0:
            stats["drop_annotator2_negative"] += 1
            continue
        # PDF line breaks inside a paragraph -> spaces (paragraph breaks kept); no other change to the text
        t = C.clean(re.sub(r"(?<!\n)\n(?!\n)", " ", str(r["text"])))
        if len(t.split()) < 8:
            stats["drop_short"] += 1
            continue
        n = C.norm(t)
        if n in seen:
            stats["drop_dup"] += 1
            continue
        seen.add(n)
        recs.append({"rid": f"cpr-nct-{i:04d}", "text": t, "nzt": nzt, "red": red, "oth": oth,
                     "agent": int(r["annotation_agent"]), "geo": r.get("geography"), "region": r.get("region")})
    hits = C.decon({r["rid"]: [r["text"]] for r in recs}, cache_name=KEY)
    recs = [r for r in recs if r["rid"] not in hits]
    rng.shuffle(recs)
    recs = C.near_dup_filter(recs, lambda r: r["text"], thresh=0.85)
    recs = containment_filter(recs, stats)
    stats["usable"] = len(recs)

    nzt_pos = [r for r in recs if r["nzt"]]
    red_pos = [r for r in recs if r["red"] and not r["nzt"]]
    oth_only = [r for r in recs if r["oth"] and not r["nzt"] and not r["red"]]
    red_only = [r for r in recs if r["red"] and not r["nzt"] and not r["oth"]]
    none = [r for r in recs if not (r["nzt"] or r["red"] or r["oth"])]
    used = set()

    def take(pool, n):
        out = []
        for r in pool:
            if len(out) >= n:
                break
            if r["rid"] not in used:
                used.add(r["rid"])
                out.append(r)
        return out

    assign = []  # (rec, qid, gold, kind)
    # nzt: all NZT passages as yes; negatives: ~40% reduction-only, ~25% other-only, rest none
    y = take(nzt_pos, len(nzt_pos))
    assign += [(r, "nzt", "yes", "nzt") for r in y]
    n_red = take(red_only, int(len(y) * 0.40))
    n_oth = take(oth_only, int(len(y) * 0.25))
    n_none = take(none, len(y) - len(n_red) - len(n_oth))
    assign += [(r, "nzt", "no", "reduction-only") for r in n_red] + [(r, "nzt", "no", "other-only") for r in n_oth] \
        + [(r, "nzt", "no", "none") for r in n_none]
    # red: remaining reduction passages as yes; negatives ~45% other-only, rest none
    y = take(red_pos, len(red_pos))
    assign += [(r, "red", "yes", "reduction") for r in y]
    n_oth = take(oth_only, int(len(y) * 0.45))
    n_none = take(none, len(y) - len(n_oth))
    assign += [(r, "red", "no", "other-only") for r in n_oth] + [(r, "red", "no", "none") for r in n_none]
    # any: remaining positives (other-only) as yes, remaining none as no, balanced
    y = [r for r in oth_only if r["rid"] not in used]
    n = [r for r in none if r["rid"] not in used]
    amb = [r for r in n if TARGET_WORD.search(r["text"]) and QTY_YEAR.search(r["text"])]
    stats["drop_any_negative_ambiguous"] += len(amb)
    n = [r for r in n if not (TARGET_WORD.search(r["text"]) and QTY_YEAR.search(r["text"]))]
    y, n = C.balance_yes(y, n, rng, lo=0.45, hi=0.55)
    for r in y + n:
        used.add(r["rid"])
    assign += [(r, "any", "yes", "other") for r in y] + [(r, "any", "no", "none") for r in n]

    rows = []
    for r, qid, gold, kind in assign:
        e = "long_context" if len(r["text"]) > 1600 else C.edge(r["text"], order=("units", "numeric", "temporal"))
        rows.append({
            "key": KEY, "rid": r["rid"], "state": r["text"], "instructions": QUESTIONS[qid], "options": C.YN,
            "gold": gold, "soft": None,
            "meta": {"dataset": DATASET, "config": "data/train-00000-of-00001.parquet (translated=False)",
                     "revision": f"hf:{REV}; sha256:{FILES['data/train-00000-of-00001.parquet']}",
                     "licence": LICENCE, "split": "train",
                     "orig_label": {"NZT": r["nzt"], "Reduction": r["red"], "Other": r["oth"],
                                    "annotation_agent": r["agent"], "row_kind": kind, "geography": r["geo"]},
                     "family": C.FAMILY, "edge": e, "defs": qid},
        })
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, DEFS)
    st = C.summary(KEY, rows)
    print("stats:", dict(stats), "| decon:", len(hits))
    print("row kinds:", dict(collections.Counter((x["meta"]["defs"], x["meta"]["orig_label"]["row_kind"]) for x in rows)))
    C.show_samples(rows, n=5, seed=6)
    C.append_manifest(C.manifest_record(
        KEY, DATASET + ", train (only split), human-written (non-translated) passages", LICENCE, rows, "yesno",
        "Expert-annotated climate targets in national laws/policies: any target / net-zero / emissions-reduction "
        "yes/no, with hard negatives that contain a target of another type; machine-translated passages and "
        "annotator-2 sampled negatives dropped; overlapping passage windows dropped (both when labels conflict); "
        "'none' passages naming a target with a quantity+year not used as 'any' negatives.", st))


if __name__ == "__main__":
    main()
