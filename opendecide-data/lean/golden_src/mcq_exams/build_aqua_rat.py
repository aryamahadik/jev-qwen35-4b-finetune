"""REJECTED IN STRICT REVIEW (29 Sep 2026) -- this builder refuses to run; raw/defs deleted, MANIFEST record removed.
Reason: gold keys not reliably right. MathQA annotators wrote their programs knowing the AQuA key, so the program check
is not independent (e.g. divide(subtract(37, 5), subtract(37, 5)) = 1 to reach a wrong key). Even with every
consistency check below tightened (0.5% tolerance, no degenerate program steps, rationale must reach the gold value,
every problem number used, broken texts dropped; 5,103 rows), hand-solving found 7 of 112 kept rows wrong or ill-posed
(fresh sample: 6 of 40), e.g. 'x^2 - (x-2)^2 = 32, greater segment?' keyed 7 (is 9); 'average of 3 readings 6 V,
0-10 V meter, smallest reading?' keyed 2 (is 0); 'if p/q = 3/4 then 3p+4q = ?' keyed 25/4 (undetermined).

Build golden rows for aqua_rat (AQuA-RAT: algebraic word problems with 5 answer choices; Ling et al., ACL 2017),
TRAIN split only, restricted to problems whose gold answer passes strict consistency checks.

Source : GitHub google-deepmind/AQuA @ 26b64ed1f22208c6742f47df547dfd65088ec30d, train.json only (97,467 problems;
         dev.json/test.json never read). README: 'This dataset has been fully crowdsourced' (GMAT/GRE-style problems
         written by crowd workers, each with a human rationale and the correct option).
Licence: Apache-2.0 (LICENSE file in that repo: 'Copyright 2017 Google Inc. Licensed under the Apache License, Version
         2.0').
Verify : AQuA golds are noisy (wrong keys, broken problems). A problem is kept only when all of these checks agree
         with its key:
         (1) MathQA (allenai; math-qa.github.io/math-QA/data/MathQA.zip, sha256 pinned; Apache-2.0 per the official
             AI2 card huggingface.co/datasets/allenai/math_qa, 'The dataset is licensed under the Apache License,
             Version 2.0') re-annotated AQuA problems with executable operation programs written by other crowd
             workers. The problem must match a MathQA TRAIN problem (normalised text; items matching MathQA dev, test
             or challenge_test are dropped), MathQA's key letter must equal AQuA's, and the program, executed by
             mathqa_eval.py, must give the gold option's value (0.5% relative tolerance; 2% when the problem asks for
             an approximate / closest value) and no other option's value. REVIEWER NOTE: MathQA annotators saw the
             AQuA key, and some programs were bent to reach a wrong key (e.g. divide(subtract(37, 5), subtract(37, 5))
             = 1, or a stray '- 3'), so this is a consistency filter, not an independent verification; programs with a
             degenerate step (x - x, x / x) are rejected.
         (2) the AQuA rationale's own final answer letter must equal the key, and the rationale must reach the gold
             value (the gold choice text or the gold number appears in it).
         (3) every number in the problem text appears in the rationale or in the program (catches problems whose
             text lost or mistyped a number, e.g. '2x-y-z=400' solved as 40).
         (4) no visibly broken text: a quantity replaced by a stray '$' ('he take $ seconds') or dropped ('completes
             of a job').
         Reviewer spot checks: about 10% of keys wrong or ill-posed before (2)-(4) and the tighter tolerance, still
         about 6-15% after them (see the REJECTED note above).
         Only MathQA's programs are used (as a filter); every row text is AQuA's original.
Rows   : state = the problem text (original casing; UTF-8-read-as-cp1252 mojibake such as 'Ã·' undone, rows where it
         cannot be undone dropped); options = the five answer choices without their 'A)' prefixes
         (original order); gold = the keyed choice. Each row has its own definitions file (defs/aqua_rat__<qid>.json).
Dedupe : exact normalised problems and near-duplicates with numbers masked (3-gram Jaccard >= 0.8; crowd variants of
         one seed problem that only change the numbers); rows with duplicate choice texts or choices cut in the source
         ('and 20', 'of these') dropped; doubled letter prefixes ('A)A)7') stripped; decontamination vs
         forbidden label-NLI, local train/dev/eval files, round-1 golden parts and JevBench public.
Sample : 7,000 rows, round-robin over MathQA's problem categories (general, physics, gain, geometry, probability,
         other) so rate/geometry/probability problems are not swamped by 'general'.
Edge   : units (quantities with units in the problem or choices), numeric otherwise.
Deterministic (seed 20261203).
"""
import collections
import json
import random
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAMILY, HERE, UNITS, append_manifest, clean, decon, fetch, near_dup_filter,  # noqa: E402
                     norm, option_defs, qid_of, show_samples, summary, write_outputs)
from mathqa_eval import evaluate  # noqa: E402

KEY = "aqua_rat"
SEED = 20261203
N_ROWS = 7000
CACHE = HERE / "cache" / KEY
COMMIT = "26b64ed1f22208c6742f47df547dfd65088ec30d"
GH = f"https://raw.githubusercontent.com/google-deepmind/AQuA/{COMMIT}/"
FILES = {
    "train.json": (GH + "train.json", "35b70c7cb1660c34d302bb932dfd3656ce3d05e8c982c797767fec31d7d1e0ba"),
    "LICENSE": (GH + "LICENSE", "189bff4f09eccdbc1790f7a9085ddd031ddf050f27929608fa4ba8a57e14a7c3"),
    "MathQA.zip": ("https://math-qa.github.io/math-QA/data/MathQA.zip",
                   "7344f30456a7aef3176d4866cc953b35b41bec44eda6b00cdbcfde2876b2f07a"),
}
LICENCE = (f"Apache-2.0 (https://github.com/google-deepmind/AQuA/blob/{COMMIT}/LICENSE: 'Copyright 2017 Google Inc. "
           "Licensed under the Apache License, Version 2.0'); verification filter MathQA Apache-2.0 "
           "(huggingface.co/datasets/allenai/math_qa README 'Licensing Information')")
INSTR = "Which answer choice is the correct answer to this math word problem?"


def demojibake(t):
    """Some AQuA texts are UTF-8 read as cp1252 ('Câ€™s', 'Ã·', 'âˆš'); undo it. None if it cannot be undone."""
    for _ in range(3):  # some texts were mangled twice ('Ã¢â‚¬â„¢')
        if not re.search(r"[âÃÂ]", t):
            return t
        try:
            t = t.encode("cp1252").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            return None
    return None if re.search(r"[âÃÂ]", t) else t


def key_text(t):
    return re.sub(r"[^a-z0-9]", "", t.lower())


def opt_text(o):
    # some choices carry the letter prefix twice ('A)A)7'): strip every leading prefix (reviewer fix)
    return clean(re.sub(r"^(?:\s*[A-E]\s*\)\s*)+", "", o))


FRAGMENT = re.compile(r"(?i)^(and|or|of|to|by|with)\b")  # choices cut in the source ('and 20', 'of these')


def opt_value(o):
    t = o.replace(",", "")
    m = re.fullmatch(r"[^\d\-]*(-?\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)[^\d]*", t)
    if m and float(m.group(2)) != 0:
        return float(m.group(1)) / float(m.group(2))
    ns = re.findall(r"-?\d+(?:\.\d+)?", t)
    return float(ns[0]) if len(ns) == 1 else None


def final_letter(rat):
    t = rat.strip()
    m = re.findall(r"(?i)(?:answer|ans|option|choice|correct)[^A-Za-z0-9]{0,15}(?:is|:|=|-)?\s*\(?([A-E])\)?\b", t)
    if m:
        return m[-1].upper()
    m = re.search(r"\b([A-E])\s*$", t)
    return m.group(1) if m else None


APPROX = re.compile(r"(?i)approx|nearly|\babout\b|closest|nearest|≈|\bround")
BROKEN = re.compile(r"(?i)\b(completes|complete|completed|does|did|finishes|finished|spends|spent|gets|got|takes|took|is|"
                    r"are|was|were|has|had|sold|sells|buys|bought|reads|read|paints|painted|eats|ate)\s+of\s+(a|an|the|"
                    r"his|her|their|its|it)\b|\$\s+(?=[A-Za-z])")
NUM = re.compile(r"(?<![\w.])-?\d[\d,]*(?:\.\d+)?(?:\s*/\s*\d+(?:\.\d+)?)?")


def tol(x, approx=False):
    return max((0.02 if approx else 0.005) * abs(x), 1e-9)


def numbers(t):
    """Numbers in a text; a fraction 'a/b' gives a/b, a and b."""
    out = []
    for m in NUM.finditer(t):
        s = m.group(0).replace(",", "").replace(" ", "")
        try:
            if "/" in s:
                x, y = s.split("/")
                if float(y) != 0:
                    out.append(float(x) / float(y))
                out += [float(x), float(y)]
            else:
                out.append(float(s))
        except ValueError:
            pass
    return out


def program_literals(formula):
    return [float(x) for x in re.findall(r"(?<![\w.])-?\d+(?:\.\d+)?(?![\w.])", re.sub(r"const_\w+", "", formula))]


def degenerate(formula):
    """True if the program has a step op(X, X) with op subtract/divide (a forced result such as x/x = 1)."""
    s = re.sub(r"\s+", "", formula.strip().rstrip("|"))
    for m in re.finditer(r"(subtract|divide)\(", s):
        i, depth, j = m.end(), 0, m.end()
        while j < len(s):  # split the two top-level arguments
            c = s[j]
            if c == "(":
                depth += 1
            elif c == ")":
                if depth == 0:
                    break
                depth -= 1
            elif c == "," and depth == 0:
                a, rest = s[i:j], j + 1
                k, d2 = rest, 0
                while k < len(s):
                    if s[k] == "(":
                        d2 += 1
                    elif s[k] == ")":
                        if d2 == 0:
                            break
                        d2 -= 1
                    k += 1
                if a == s[rest:k]:
                    return True
                break
            j += 1
    return False


def near(x, y, approx):
    return abs(x - y) <= tol(y, approx)


def main():
    if "--force-rejected" not in sys.argv:
        sys.exit("aqua_rat was REJECTED in strict review (noisy gold keys, see the module docstring); not building.")
    paths = {n: fetch(u, CACHE / n, s) for n, (u, s) in FILES.items()}
    aq = [json.loads(l) for l in open(paths["train.json"], encoding="utf-8")]  # TRAIN ONLY
    zf = zipfile.ZipFile(paths["MathQA.zip"])
    mq = {sp: json.loads(zf.read(f"{sp}.json")) for sp in ("train", "dev", "test", "challenge_test")}
    heldout_keys = {key_text(r["Problem"]) for sp in ("dev", "test", "challenge_test") for r in mq[sp]}
    progs = collections.defaultdict(list)
    for r in mq["train"]:
        progs[key_text(r["Problem"])].append(r)

    stats = collections.Counter()
    recs = []
    for i, a in enumerate(aq):
        k = key_text(a["question"])
        if k in heldout_keys:
            stats["in_mathqa_heldout"] += 1
            continue
        if k not in progs:
            stats["no_mathqa_program"] += 1
            continue
        opts = [opt_text(o) for o in a["options"]]
        if len(opts) != 5 or [o.strip()[:1] for o in a["options"]] != list("ABCDE") or not all(opts):
            stats["bad_options"] += 1
            continue
        if len({o.lower() for o in opts}) < 5:
            stats["dup_options"] += 1
            continue
        if any(FRAGMENT.match(o) for o in opts):
            stats["fragment_options"] += 1
            continue
        g = "ABCDE".index(a["correct"])
        vals = [opt_value(o) for o in opts]
        if vals[g] is None:
            stats["gold_not_numeric"] += 1
            continue
        approx = bool(APPROX.search(a["question"]))
        ok, prog = False, None
        for p in progs[k]:
            if p["correct"].upper() != a["correct"]:
                continue
            if degenerate(p["annotated_formula"]):
                continue
            v = evaluate(p["annotated_formula"])
            if v is None or not near(v, vals[g], approx):
                continue
            if any(o is not None and j != g and near(v, o, approx) for j, o in enumerate(vals)):
                continue
            ok, cat, prog = True, p["category"], p
            break
        if not ok:
            stats["program_disagrees"] += 1
            continue
        if final_letter(a["rationale"]) != a["correct"]:
            stats["rationale_disagrees"] += 1
            continue
        rat_nums = numbers(a["rationale"])
        if not (opts[g].strip() in a["rationale"] or any(near(x, vals[g], approx) for x in rat_nums)):
            stats["rationale_misses_gold_value"] += 1
            continue
        avail = rat_nums + program_literals(prog["annotated_formula"])
        if not all(any(abs(x - y) <= 1e-6 * max(1.0, abs(y)) for y in avail) for x in numbers(a["question"])):
            stats["problem_number_unused"] += 1
            continue
        if BROKEN.search(a["question"]):
            stats["broken_text"] += 1
            continue
        q = demojibake(clean(a["question"]))
        opts = [demojibake(o) for o in opts]
        if q is None or None in opts:
            stats["broken_encoding"] += 1
            continue
        if not (20 <= len(q) <= 1500):
            stats["length"] += 1
            continue
        if len(set(opts)) < 5:
            stats["dup_options"] += 1
            continue
        recs.append({"rid": f"aqua_train_{i}", "state": q, "options": opts, "gold": opts[g], "cat": cat,
                     "correct": a["correct"]})
    print(f"train problems={len(aq)} verified={len(recs)} drops={dict(stats)}")

    recs = near_dup_filter(recs, lambda r: r["state"], thresh=0.8, strip_numbers=True)
    print(f"after near-dup (numbers masked): {len(recs)}")
    hits = decon({r["rid"]: [r["state"]] for r in recs})
    recs = [r for r in recs if r["rid"] not in hits]
    print(f"after decon: {len(recs)}")

    rng = random.Random(SEED)
    pools = collections.defaultdict(list)
    for r in recs:
        pools[r["cat"]].append(r)
    for c in sorted(pools):
        rng.shuffle(pools[c])
    chosen, cats = [], sorted(pools)
    while len(chosen) < N_ROWS and any(pools.values()):
        for c in cats:
            if pools[c] and len(chosen) < N_ROWS:
                chosen.append(pools[c].pop())
    print("category mix:", dict(collections.Counter(r["cat"] for r in chosen)))

    rows, defs = [], {}
    for r in chosen:
        qid = qid_of(r["rid"])
        defs[qid] = option_defs(r["state"], r["options"], kind="math")
        edge = "units" if (UNITS.search(r["state"]) or any(UNITS.search(o) for o in r["options"])) else "numeric"
        rows.append({
            "key": KEY, "rid": r["rid"], "state": r["state"], "instructions": INSTR, "options": r["options"],
            "gold": r["gold"], "soft": None,
            "meta": {"dataset": "AQuA-RAT (github google-deepmind/AQuA)", "config": "train.json; 5-way answer choice; gold consistency-checked: executed MathQA train "
                     "program (0.5% tol., no degenerate steps), AQuA rationale letter + value, every problem number used",
                     "revision": f"git:{COMMIT}; sha256:{FILES['train.json'][1]}; MathQA.zip sha256:{FILES['MathQA.zip'][1]}",
                     "licence": LICENCE, "split": "train",
                     "orig_label": {"correct": r["correct"], "mathqa_category": r["cat"]},
                     "family": FAMILY, "edge": edge, "defs": qid, "seed": SEED}})
    rng.shuffle(rows)
    write_outputs(KEY, rows, defs)
    s = summary(KEY, rows)
    show_samples(rows, defs, n=5, seed=11)
    append_manifest({
        "key": KEY, "family": FAMILY, "dataset": "AQuA-RAT (github google-deepmind/AQuA), train.json",
        "licence": LICENCE, "rows": len(rows), "qtype": "choice (5 answer choices; per-row option definitions)",
        "yesno_share": 0.0, "edge_tags": sorted(k for k in s["edges"] if k),
        "notes": ("crowd-written GMAT/GRE-style algebra word problems; only problems whose key agrees with a MathQA "
                  "annotator's executed program (0.5% tolerance, no degenerate steps; MathQA annotators saw the key, so "
                  "this is a consistency filter; MathQA train only, its dev/test/challenge items dropped), with the "
                  "AQuA rationale's final letter and value, and whose every number is used by the rationale or program "
                  "(broken texts dropped); reviewer hand-check: about 4% of kept keys still wrong or ill-posed; "
                  "numbers-masked near-duplicate variants removed; "
                  "round-robin over MathQA categories; options are the original five choices, gold position "
                  f"{dict(sorted(s['pos'].items()))}.")})


if __name__ == "__main__":
    main()
