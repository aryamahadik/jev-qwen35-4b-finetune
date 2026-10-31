"""Build golden v14 rows for "boardgameqa" (BoardgameQA: reasoning with contradictory information; Kazemi et al.,
NeurIPS 2023 Datasets & Benchmarks).

Source : official release https://storage.googleapis.com/gresearch/BoardgameQA/BoardgameQA.zip (Google Research),
         sha256 recorded in meta. ONLY the 15 */train.json files are read (valid.json / test.json never opened).
Licence: CC BY, stated in the official paper (arXiv:2306.07934, footnote 1 on the release: "Available at:
         https://storage.googleapis.com/gresearch/BoardgameQA/BoardgameQA.zip. License: CC BY.").
Texts  : program-generated defeasible theories (facts, rules, pairwise rule preferences) rendered with manually
         written templates; the label (proved / disproved / unknown) is computed by construction and checked with a
         defeasible solver (paper Sec. 4) - no model involvement.
Task   : 3-way yes / no / unknown for the question about the game (proved -> yes, disproved -> no,
         unknown -> unknown). Variants used: Main depth 1-3, Binary depth 1-3 (proved/disproved only),
         Zero/Low/High/Easy/Difficult conflict, Knowledge light/heavy, Some/Many distractors.
Selection: seed 20261132, round-robin over variants per label, quotas proved 2,700 / disproved 2,700 /
         unknown 2,600, dedupe of normalised states.
"""
import json
import random
import re
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as C  # noqa: E402

KEY = "boardgameqa"
SEED = 20261132
URL = "https://storage.googleapis.com/gresearch/BoardgameQA/BoardgameQA.zip"
LICENCE = ("CC BY (official paper arXiv:2306.07934, release footnote: 'Available at: https://storage.googleapis.com/"
           "gresearch/BoardgameQA/BoardgameQA.zip. License: CC BY.')")
CACHE = C.CACHE_ROOT / "boardgameqa"
QUOTA = {"proved": 2700, "disproved": 2700, "unknown": 2600}
GOLD = {"proved": "yes", "disproved": "no", "unknown": "unknown"}
OPTIONS = ["yes", "no", "unknown"]
INSTRUCTIONS = ("Using only the game state, the rules and the rule preferences (plus everyday knowledge a rule may "
                "rely on), is the answer to the question yes, no, or unknown?")
DEFS = {
    "yes": "Chaining the stated facts through the rules proves the statement asked about; when two rules conflict, "
           "the preferred rule wins if its condition is proved, and otherwise the other rule stands.",
    "no": "The same reasoning proves the opposite of the statement asked about, for example because a preferred "
          "rule overrides the rule that would have proved it.",
    "unknown": "Neither the statement nor its opposite can be proved: some fact the answer depends on is not given "
               "and cannot be derived, so the game state leaves the question open.",
}
QRE = re.compile(r"Based on the game state and the rules and preferences, (.*)$", re.S)
RULE_SPLIT = re.compile(r"\s*(?=Rule\d+: )")


def build_state(x):
    m = QRE.search(x["example"])
    assert m, x["example"][-200:]
    q = m.group(1).strip()
    q = q[0].upper() + q[1:]
    rules = [r.strip() for r in RULE_SPLIT.split(x["rules"].strip()) if r.strip()]
    prefs = [p.strip() + "." for p in x["preferences"].strip().split(".") if p.strip()]
    lines = ["Game state (facts):", C.clean(x["facts"]), "", "Rules of the game:"] + rules + \
            ["", "Rule preferences:"] + (prefs if prefs else ["(none)"]) + ["", f"Question: {q}"]
    return "\n".join(lines), q


def depth_of(variant):
    m = re.search(r"depth(\d)", variant)
    return int(m.group(1)) if m else None


def edge_of(x, q, variant):
    if x["label"] == "unknown":
        return "missing_info"
    if "conflicting" in x["proof"]:
        return "conflicting_evidence"
    if re.search(r"\bnot\b", q):
        return "negation"
    if (depth_of(variant) or 0) >= 2:
        return "multi_hop"
    if "Knowledge" in variant:
        return "implicit"
    return None


def main():
    z = C.fetch(URL, CACHE / "BoardgameQA.zip")
    sha = C.sha256_file(z)
    data = {}
    with zipfile.ZipFile(z) as zf:
        for n in sorted(zf.namelist()):
            if n.endswith("/train.json"):
                data[n.split("/")[1]] = json.loads(zf.read(n))
    print(f"zip sha256 {sha[:16]}..., train files {len(data)}, rows {sum(len(v) for v in data.values())}")

    seen = set()
    pools = defaultdict(lambda: defaultdict(list))
    for variant, rows in data.items():
        for i, x in enumerate(rows):
            st, q = build_state(x)
            k = C.norm(st)
            if k in seen:
                continue
            seen.add(k)
            pools[x["label"]][variant].append(dict(x, state=st, q=q, variant=variant, idx=i))
    rng = random.Random(SEED)
    picked = []
    for lab, byvar in pools.items():
        vars_ = sorted(byvar)
        for v in vars_:
            rng.shuffle(byvar[v])
        ptr = Counter()
        got = 0
        while got < QUOTA[lab]:
            progressed = False
            for v in vars_:
                if got >= QUOTA[lab]:
                    break
                if ptr[v] < len(byvar[v]):
                    picked.append(byvar[v][ptr[v]])
                    ptr[v] += 1
                    got += 1
                    progressed = True
            if not progressed:
                break
    rng.shuffle(picked)

    out = []
    for x in picked:
        out.append({
            "key": KEY,
            "rid": f"boardgameqa_{x['variant']}_train_{x['idx']}",
            "state": x["state"],
            "instructions": INSTRUCTIONS,
            "options": OPTIONS,
            "gold": GOLD[x["label"]],
            "soft": None,
            "meta": {"dataset": URL, "config": x["variant"], "revision": f"zip sha256 {sha}", "licence": LICENCE,
                     "split": "train", "orig_label": x["label"], "family": C.FAMILY,
                     "edge": edge_of(x, x["q"], x["variant"]), "depth": depth_of(x["variant"]),
                     "goal": x["goal"]},
        })
    C.validate_rows(KEY, out, {None: DEFS})
    C.write_rows(KEY, out)
    C.write_defs(KEY, DEFS)
    C.report(KEY, out)
    print("per variant:", dict(Counter(r["meta"]["config"] for r in out)))
    e = Counter(r["meta"]["edge"] for r in out)
    C.append_manifest({
        "key": KEY, "family": C.FAMILY, "dataset": "BoardgameQA (15 variants, train)", "licence": LICENCE,
        "rows": len(out), "qtype": "choice (yes / no / unknown)", "yesno_share": None,
        "edge_tags": sorted(k for k in e if k),
        "notes": "Program-generated defeasible reasoning with exact labels: conflicting rules resolved by preferences "
                 "(exceptions that override defaults), missing information -> unknown, world-knowledge hops "
                 "(e.g. Montreal is in Canada), distractors, depth 1-3.",
    })
    if "--show" in sys.argv:
        C.show_samples(out, 5)


if __name__ == "__main__":
    main()
