"""Generator gen_logic_negation (family nli_logic_reasoning): short realistic texts whose yes/no answer hinges on
logic and language edge cases - negation and double negation, lexical negation (un-/in-/non-), quantifiers (all,
some, none, most, a majority, at least / exactly / at most n, all but one), set membership with closed vs open lists,
exceptives ('all except', 'no ... except'), 'only' (exclusive and focus-shifted), conditionals (if, only if, if and
only if, even if, unless, contrapositives, converses, chains), disjunction, De Morgan scope ('not both' vs 'neither',
'may not use both' vs 'may not use either'), deontic negation ('need not' vs 'must not'), comparatives ('not fewer
than' is not 'more than'), superlatives, reported speech vs asserted fact (claimed / discovered / denied / admitted /
falsely / correctly, claim vs official record), hypotheticals (if vs since, counterfactuals, plans, may vs will),
aspect ('still', 'no longer', 'not yet'), 'almost' vs 'barely', negation-scope ambiguity resolved in the text
('not ... because', 'all ... not'), policies with exceptions to exceptions, numeric thresholds at the boundary and
with unit conversion, calendar exceptions, and sarcasm markers whose meaning the text defines.

Construction (no dataset is read, no model is called; every template and word list is Claude-written):
  * 44 schemas in ln_schemas_a/b/c.py, each with several surface variants and 8-30 realistic frames.
  * Every schema emits a FACT-FLIP TWIN pair: the same question over two texts that differ in one decisive fact or
    word, with opposite answers; rows carry meta.twin_of = rid of the partner.
  * Every row also carries its logical form (meta.logic: premises, goal, integer variables).  ln_engine.decide
    enumerates all worlds consistent with the premises; gold is 'yes' iff the goal holds in all of them.  The
    template's own label (computed separately) must agree for every row, question types without an 'unknown'
    reading must be determined, and the written file is re-checked from meta.logic after writing.
Output: data/v14_parts/raw/gen_logic_negation.jsonl, defs/gen_logic_negation__<qid>.json, MANIFEST record.
Deterministic (seed 20261201), CPU only.
"""
import hashlib
import json
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "nli_logic_reasoning"))
import _common as C  # noqa: E402
import ln_engine as E  # noqa: E402
import ln_schemas_a as SA  # noqa: E402
import ln_schemas_b  # noqa: E402,F401  (registers schemas)
import ln_schemas_c  # noqa: E402,F401  (registers schemas)

KEY = "gen_logic_negation"
SEED = 20261201
TARGET_PAIRS = 12600  # 25,200 rows
LICENCE = "CC0 1.0 (Claude-written templates, word lists and program; no third-party text or labels)"
DETERMINED = {"true", "violate", "meets", "policy", "meaning"}
DEFS = {
    "certain": {
        "yes": "The text guarantees the statement: it must be true given only what is written, reading 'if A, B' as "
               "silent about cases without A and treating claims, plans, possibilities and counterfactuals as unconfirmed.",
        "no": "The statement is not guaranteed: the text contradicts it or leaves it open, for example an unverified "
              "claim, the converse of a rule, a mere possibility or plan, or a case the text never settles.",
    },
    "true": {
        "yes": "Given the facts stated in the text, the answer is yes once negation, double negation, quantifiers, "
               "exceptions, 'almost'-type words and time words are read exactly as written.",
        "no": "Given the facts stated in the text, the answer is no once negation, double negation, quantifiers, "
              "exceptions, 'almost'-type words and time words are read exactly as written; the text settles it.",
    },
    "violate": {
        "yes": "The action breaks the rule read literally: it does something the rule forbids or omits something it "
               "requires, with 'only', 'not', 'both' or 'either' and any stated exception applied exactly as written.",
        "no": "The rule read literally does not forbid the action: it is permitted, merely optional ('need not'), "
              "covered by a stated exception, or outside the people or cases the rule restricts.",
    },
    "meets": {
        "yes": "The case satisfies the stated requirement exactly: boundaries as worded ('at least 5' includes 5, "
               "'under 5' excludes 5), units converted, every 'and' condition met, at least one 'or' condition met.",
        "no": "The case fails the stated requirement: a boundary or unit-converted limit is missed, an 'and' "
              "condition is absent, no 'or' condition holds, too few conditions hold, or an 'exactly' count differs.",
    },
    "policy": {
        "yes": "Applying the policy exactly as written gives yes: the general rule allows or applies to this case, or "
               "an exception does so and no further stated exception overrides it.",
        "no": "Applying the policy exactly as written gives no: the general rule or an exception rules the case out, "
              "and no stated exception to that exception restores it.",
    },
    "meaning": {
        "yes": "The writer's intended meaning is that the statement holds: a message carrying the stated sarcasm "
               "marker means the opposite of its literal words, and an unmarked message means what it literally says.",
        "no": "The writer's intended meaning is that the statement does not hold, after reversing only messages that "
              "carry the stated sarcasm marker; a marker applies only to its own message.",
    },
}

BAD_TEXT = re.compile(r"[{}]|\s{2,}|\.\.(?!\.)|\s[,.;:?]|,,|\bthe the\b|\ba a\b|\ban an\b")


def lint(s, what):
    assert s == s.strip(), (what, s)
    for line in s.split("\n"):
        assert not BAD_TEXT.search(line.replace("  ", "  ")), (what, line)
    assert s[0].isupper() or s[0].isdigit() or s[0] in "\"'", (what, s)


def norm(s):
    return " ".join(re.findall(r"[a-z0-9]+", s.lower()))


def src_revision():
    h = hashlib.sha256()
    for f in ("gen_logic_negation.py", "ln_engine.py", "ln_schemas_a.py", "ln_schemas_b.py", "ln_schemas_c.py"):
        h.update((HERE / f).read_bytes())
    return h.hexdigest()[:16]


def check_item(it, name):
    res = E.decide(it["prem"], it["goal"], it["ints"])
    assert res != "X", (name, "inconsistent premises", it["state"])
    eng = "yes" if res == "T" else "no"
    if eng != it["gold"]:
        raise AssertionError(f"[{name}] template gold {it['gold']} != engine {eng} ({res})\n{it['state']}\n{it['q']}")
    if it["qid"] in DETERMINED and res not in ("T", "F"):
        raise AssertionError(f"[{name}] undetermined answer for qid {it['qid']}\n{it['state']}\n{it['q']}")
    return res


MASK_WORDS = sorted(set(E.FIRST) | set(E.PLACES) | set(E.STREETS) | set(E.COMPANIES) | set(E.RESTAURANTS)
                    | {t.split(" ", 1)[1] for t in E.TEAMS} | set(E.MONTHS) | set(E.WEEKDAYS), key=len, reverse=True)
MASK_RE = re.compile(r"\b(" + "|".join(re.escape(w) for w in MASK_WORDS) + r")\b")
SKELETON_CAP = 8  # at most this many rows may share a text skeleton (names, places, numbers masked)
# where the masked number or date is itself the decisive fact, a looser cap applies
SKELETON_CAP_BY = {"calendar_exception": 40, "count_quant": 16, "thresholds": 16, "quantifier_word_swap": 16}


def skeleton(s):
    s = re.sub(r"\d[\d,:.]*", "#", s)
    s = MASK_RE.sub("X", s)
    return re.sub(r"\b(he|she|his|her|him)\b", "P", s)


def main():
    rng = random.Random(SEED)
    wsum = sum(w for _, w, _ in SA.SCHEMAS)
    scale = TARGET_PAIRS / wsum
    rev = f"gen-v1 seed {SEED} src-sha256:{src_revision()}"
    rows, seen = [], set()
    skel = Counter()
    stats = Counter()
    fails = Counter()
    engine_res = Counter()
    full = {}

    def run(name, fn, quota, start):
        n, tries = start, 0
        while n < quota and tries < max(200, (quota - start) * 60):
            tries += 1
            pair = fn(rng)
            if not pair:
                fails[name] += 1
                continue
            a, b = pair
            assert a["q"] == b["q"] and a["qid"] == b["qid"], (name, a["q"], b["q"])
            assert {a["gold"], b["gold"]} == {"yes", "no"}, (name, a["gold"], b["gold"], a["state"])
            ka, kb = norm(a["state"]), norm(b["state"])
            if ka == kb or ka in seen or kb in seen:
                fails[name + ":dup"] += 1
                continue
            sa, sb = skeleton(a["state"]), skeleton(b["state"])
            need = Counter([sa, sb])
            cap_ = SKELETON_CAP_BY.get(name, SKELETON_CAP)
            if any(skel[k] + c > cap_ for k, c in need.items()):
                fails[name + ":skel"] += 1
                continue
            for it in (a, b):
                lint(it["state"], name)
                lint(it["q"], name)
                assert it["q"].endswith("?"), it["q"]
                engine_res[check_item(it, name)] += 1
            seen.update((ka, kb))
            skel.update(need)
            base = f"{KEY}_{name}_{n:05d}"
            rids = [base + "_a", base + "_b"]
            for j, it in enumerate((a, b)):
                rows.append({
                    "key": KEY, "rid": rids[j], "state": it["state"], "instructions": it["q"],
                    "options": ["yes", "no"], "gold": it["gold"], "soft": None,
                    "meta": {"dataset": "generated (golden_src/gen/gen_logic_negation.py)", "config": name,
                             "revision": rev, "licence": LICENCE, "split": "train", "orig_label": it["gold"],
                             "family": C.FAMILY, "edge": it["edge"], "defs": it["qid"], "twin_of": rids[1 - j],
                             "template": f"{name}:{it['var']}", "generator_seed": SEED,
                             "logic": E.to_json({"p": it["prem"], "g": it["goal"], "ints": it["ints"]})},
                })
            n += 1
        return n

    # pass 1: weighted quotas
    for name, w, fn in SA.SCHEMAS:
        quota = max(1, round(w * scale))
        n = run(name, fn, quota, 0)
        stats[name] = n
        full[name] = n >= quota
        if n < quota:
            print(f"  [pass1] {name}: {n}/{quota} pairs (fails {fails[name]}, dups {fails[name + ':dup']}, "
                  f"skeleton cap {fails[name + ':skel']})")
    # pass 2: top up from schemas that still have headroom, in proportion to their weights
    deficit = TARGET_PAIRS - sum(stats.values())
    rounds = 0
    while deficit > 0 and rounds < 4:
        rounds += 1
        open_s = [(name, w, fn) for name, w, fn in SA.SCHEMAS if full[name]]
        if not open_s:
            break
        ws = sum(w for _, w, _ in open_s)
        for name, w, fn in open_s:
            extra = max(1, round(deficit * w / ws))
            before = stats[name]
            stats[name] = run(name, fn, before + extra, before)
            full[name] = stats[name] >= before + extra
        deficit = TARGET_PAIRS - sum(stats.values())
        print(f"  [pass2 round {rounds}] total pairs {sum(stats.values())}, deficit {deficit}")
    print("pairs per schema:", dict(stats))
    print("engine outcomes:", dict(engine_res))
    rng.shuffle(rows)
    C.validate_rows(KEY, rows, DEFS)
    C.write_rows(KEY, rows)
    for qid, d in DEFS.items():
        C.write_defs(KEY, d, qid)
    recheck()
    share = C.report(KEY, rows)
    templates = Counter(r["meta"]["template"] for r in rows)
    qids = Counter(r["meta"]["defs"] for r in rows)
    print(f"[{KEY}] schemas {len(stats)}, distinct schema:variant surface templates {len(templates)}")
    print(f"[{KEY}] qids: {dict(qids)}")
    e = Counter(r["meta"]["edge"] for r in rows)
    C.append_manifest({
        "key": KEY, "family": C.FAMILY,
        "dataset": "generated: logic and language edge cases (negation, quantifiers, conditionals, exceptions, "
                   "reported speech, hypotheticals, sarcasm markers) with fact-flip twins",
        "licence": LICENCE, "rows": len(rows), "qtype": "yesno", "yesno_share": round(share, 4),
        "edge_tags": sorted(k for k in e if k),
        "notes": f"{len(stats)} Claude-written schemas, {len(templates)} schema:variant surface templates, hundreds of "
                 "realistic frames (HR, refunds, shipping, pharmacy, travel, school, sport, housing, finance). Every row "
                 "has a fact-flip twin (meta.twin_of) and a logical form (meta.logic) re-decided by a world-enumeration "
                 "checker; template label and checker must agree. Six question types with their own defs "
                 "(certain/true/violate/meets/policy/meaning); 'no' covers 'not guaranteed' only for qid 'certain'.",
    })
    if "--show" in sys.argv:
        C.show_samples(rows, 12)


def recheck():
    """Re-read the written file and re-decide every row from its stored logical form; check twin links."""
    p = C.RAW_DIR / f"{KEY}.jsonl"
    rows = [json.loads(line) for line in open(p)]
    by = {r["rid"]: r for r in rows}
    per_q = defaultdict(int)
    for r in rows:
        lg = r["meta"]["logic"]
        res = E.decide(lg["p"], lg["g"], {k: tuple(v) for k, v in lg["ints"].items()})
        assert ("yes" if res == "T" else "no") == r["gold"], r["rid"]
        if r["meta"]["defs"] in DETERMINED:
            assert res in ("T", "F"), r["rid"]
        t = by[r["meta"]["twin_of"]]
        assert t["meta"]["twin_of"] == r["rid"] and t["gold"] != r["gold"] and t["instructions"] == r["instructions"]
        per_q[r["meta"]["defs"]] += 1
    print(f"[recheck] {len(rows)} rows re-decided from meta.logic; twins consistent; per qid {dict(per_q)}")


if __name__ == "__main__":
    main()
