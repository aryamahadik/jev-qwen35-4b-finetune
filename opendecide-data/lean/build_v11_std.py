"""Assemble the v0.11c STD training block (standard-doctrine items, Claude-authored, blind-solved).

Inputs (data/v11_parts/std/), one set per domain (every <domain>.agreed.json found there; today: evidence, hate,
hearsay, trademark). Written by std_src/<domain>.py (hate was written directly); no external model, no dataset text.
  <domain>.jsonl         teacher-written rows with gold
  <domain>.agreed.json   ids where an independent blind solve agreed with the gold (after review)
  <domain>.solver.jsonl  the blind answers (only used to report agreement before review)

Steps per domain
  1. keep only agreed ids, then drop orphan twins: rows linked by meta.twin_of (evidence triples, hate / hearsay
     minimal pairs) or meta.base_id (trademark yes/no probes that reuse a choice item's state and derive their gold
     from it) form one set, and a set is kept whole or dropped whole.
  2. meta cut to {"domain", "twin_of"?, "base_id"?, "kind"?}. Dropped because they are tied to the gold (not seen by
     the model, but kept out of training rows on principle): evidence meta.twin_of (the base of every triple is the
     SUPPORTS row, so "no twin_of" = SUPPORTS), trademark difficulty / boundary / family (e.g. difficulty 1 is mostly
     arbitrary or fanciful), hearsay difficulty; item / edit are redundant with group_id. evidence keeps "kind"
     (calc / contrastive: every triple has all three labels). Rows are otherwise unchanged (ids and call_ids kept, so
     the block stays traceable to the agreed / solver files).
Checks (any failure -> exit 1, nothing written)
  schema    key order, fixed fields, id / group_id prefixes, card "- <option>: <definition>" lines (= options for
            choice), noul gold int 0/1, ids unique, same (instructions, state, options) -> same call_id and different
            text -> different call_id, no id / call_id shared with the other data listed below
  structure evidence triples (same claim, instructions, options and card; golds are exactly S / R / N), hate and
            hearsay twins flip the label and differ in the text, trademark probes share the base's state and group
            and their gold equals (base gold == asked category)
  balance   underlying label per domain (evidence 3 classes, hate / hearsay 2, trademark 5 choice classes + yes/no
            probes) within tolerance, noul yes share (binomial p >= 0.01), choice gold position (chi-square vs
            uniform, p >= 0.01)
  leakage   label words in the state (per-domain list), dataset names, choice instructions that name only some
            options ("hateful or not?") pointing at the gold above chance (binomial), and no surface cue tied to the
            target: instructions, card, option order, asked label (noul)
            and every kept meta key are tested against the target within each (domain, qtype) with a permutation
            chi-square test (p < 0.01 fails). State length vs label is reported (one-vs-rest AUC; a warning
            when it is outside 0.3-0.7), not enforced.
  near-dups normalized token overlap (distinct shared tokens / distinct tokens of the shorter text) > 0.8 fails:
            across groups inside the block, inside a group for rows outside a twin set with the same target, and
            against every other train / dev / eval file below (candidates via shared word 5-grams); an exact
            normalized state match with any of them and any shared 12-word run with an eval file also fail (the
            v0.11c mixer drops such rows silently). Held-out files (data/ohs*, lean/ohs*, results_ohs, preds_ohs,
            bench) are never opened here; build_train_v11c.py runs its own 12-gram check against them.
Writes data/v11_parts/std_train.jsonl and data/v11_parts/std_train_summary.json. CPU only; deterministic.
  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python build_v11_std.py
"""
import json
import math
import random
import re
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE / "data"
SRC_DIR = D / "v11_parts" / "std"
OUT = D / "v11_parts" / "std_train.jsonl"
SUMMARY = D / "v11_parts" / "std_train_summary.json"
NEAR = 0.8
ALPHA = 0.01
N_PERM = 4000
SEED = 20261120
KEYS = ["id", "group_id", "call_id", "split", "track", "source", "state", "qtype", "instructions", "options", "gold",
        "role", "card", "meta"]

TRAIN_OTHER = ["train_v11.jsonl", "v11_parts/binj_train.jsonl", "pg_train.jsonl", "ohr_train.jsonl", "lah_train.jsonl",
               "judge_train.jsonl", "debate_train.jsonl"]
DEV_OTHER = ["dev.jsonl", "devp.jsonl", "devp_card.jsonl", "devzs.jsonl", "devzs_card.jsonl", "devzs2.jsonl",
             "devzs2_card.jsonl", "dev_hc.jsonl", "pg_dev.jsonl", "debate_dev.jsonl", "dev_nc.jsonl",
             "taskbank_dev.jsonl", "hard_dev.jsonl", "dev_negwords.jsonl", "dev_claims.jsonl"]
EVAL_OTHER = ["eval.jsonl", "eval_card.jsonl", "eval_jagged.jsonl", "eval_opi.jsonl", "eval_long.jsonl",
              "eval_multi.jsonl", "eval_hc.jsonl"]
assert not any(Path(f).name.startswith("ohs") for f in TRAIN_OTHER + DEV_OTHER + EVAL_OTHER)

# ------------------------------------------------------------------------------------------------ domain rules
EV_S, EV_R, EV_N = "SUPPORTS", "REFUTES", "NOT ENOUGH INFO"
HATE_POS = {"hateful", "hate speech"}
HATE_NEG = {"not hateful", "non-hateful", "not hate speech"}
TM_SCALE = ["generic", "descriptive", "suggestive", "arbitrary", "fanciful"]
CLASSES = {"evidence": [EV_S, EV_R, EV_N], "hate": ["hateful", "not hateful"],
           "hearsay": ["hearsay", "not hearsay"], "trademark": TM_SCALE}
LEAK = {
    "evidence": re.compile(r"support|refut|not enough|enough info|insufficient", re.I),
    "hate": re.compile(r"hateful|hate speech|non-hateful", re.I),
    "hearsay": re.compile(r"hearsay|truth of the matter|verbal act|non-?assertive|implied assertion|"
                          r"\brule 80[1-7]|\b80[1-7]\([a-d]\)", re.I),
    "trademark": re.compile(r"generic|descripti|describ|suggest|arbitrar|fanci|distinctive", re.I),
}
BANNED = re.compile(r"legalbench|hatecheck|vitaminc|\bbtzsc\b|trueteacher|social bias frames", re.I)
META_KEEP = {"evidence": {"domain", "kind"}, "hate": {"domain", "twin_of"}, "hearsay": {"domain", "twin_of"},
             "trademark": {"domain", "base_id"}}

rj = lambda p: [json.loads(l) for l in open(p)]
toks = lambda s: re.findall(r"[a-z0-9]+", s.lower())
card_names = lambda r: [l[2:].split(": ", 1)[0] for l in r["card"].split("\n")]


def hate_asked(r):
    """hate yes/no rows: the card holds one line, the label the question asks about"""
    return card_names(r)[0]


def tm_asked(r):
    found = [c for c in TM_SCALE if re.search(rf"\b{c}\b", r["instructions"], re.I)]
    assert len(found) == 1, (r["id"], r["instructions"])
    return found[0]


def underlying(r, d, byid):
    """the domain class of the item, whatever the question form"""
    if d == "evidence":
        return r["gold"]
    if d == "hate":
        if r["qtype"] == "choice":
            return "hateful" if r["gold"] in HATE_POS else "not hateful"
        pos = hate_asked(r) in HATE_POS
        return "hateful" if (r["gold"] == 1) == pos else "not hateful"
    if d == "hearsay":
        return "hearsay" if r["gold"] == 1 else "not hearsay"
    if r["qtype"] == "choice":
        return r["gold"]
    return byid[r["meta"]["base_id"]]["gold"]


def target(r, d):
    """what the model is trained to output: the gold option class for choice rows, yes/no for noul rows"""
    if r["qtype"] == "noul":
        return "yes" if r["gold"] == 1 else "no"
    if d == "hate":
        return "hateful" if r["gold"] in HATE_POS else "not hateful"
    return r["gold"]


# ------------------------------------------------------------------------------------------------ stats helpers
def chi2_stat(xs, ys):
    n = len(xs)
    cx, cy, cxy = Counter(xs), Counter(ys), Counter(zip(xs, ys))
    return sum((cxy[(a, b)] - cx[a] * cy[b] / n) ** 2 / (cx[a] * cy[b] / n) for a in cx for b in cy)


def perm_p(xs, ys, rng):
    """permutation p-value of the chi-square statistic for independence of cue xs and target ys"""
    if len(set(xs)) < 2 or len(set(ys)) < 2:
        return None
    obs = chi2_stat(xs, ys)
    ys = list(ys)
    hits = 0
    for _ in range(N_PERM):
        rng.shuffle(ys)
        hits += chi2_stat(xs, ys) >= obs - 1e-9
    return (hits + 1) / (N_PERM + 1)


def binom_p(k, n, p=0.5):
    """two-sided exact binomial p-value"""
    pk = [math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(n + 1)]
    return min(1.0, sum(x for x in pk if x <= pk[k] * (1 + 1e-9)))


def gof_uniform_p(counts, k):
    """chi-square goodness of fit vs uniform over k cells (closed-form survival function)"""
    n = sum(counts)
    e = n / k
    x = sum((c - e) ** 2 / e for c in counts + [0] * (k - len(counts)))
    df = k - 1
    if df % 2 == 0:  # sf = exp(-x/2) * sum_{i < df/2} (x/2)^i / i!
        return math.exp(-x / 2) * sum((x / 2) ** i / math.factorial(i) for i in range(df // 2))
    # odd df: sf = erfc(sqrt(x/2)) + exp(-x/2) * sum_{i=1}^{(df-1)/2} x^(i-1/2) / (2^(i-1/2) Gamma(i+1/2))
    s = math.erfc(math.sqrt(x / 2))
    for i in range(1, (df - 1) // 2 + 1):
        s += math.exp(-x / 2) * (x / 2) ** (i - 0.5) / math.gamma(i + 0.5)
    return min(1.0, s)


def auc(pos, neg):
    return sum((x > y) + 0.5 * (x == y) for x in pos for y in neg) / (len(pos) * len(neg))


def overlap(a, b):
    return len(a & b) / max(1, min(len(a), len(b)))


# ------------------------------------------------------------------------------------------------ assemble
def link_sets(rows):
    """connected components over twin_of / base_id links (a row without links is its own set)"""
    parent = {r["id"]: r["id"] for r in rows}

    def find(k):
        while parent[k] != k:
            parent[k] = parent[parent[k]]
            k = parent[k]
        return k

    for r in rows:
        for key in ("twin_of", "base_id"):
            t = r["meta"].get(key)
            if t:
                assert t in parent, f"{r['id']}: {key} {t} not in rows"
                parent[find(r["id"])] = find(t)
    comp = defaultdict(list)
    for r in rows:
        comp[find(r["id"])].append(r["id"])
    return {i: tuple(sorted(c)) for c in comp.values() for i in c}


def load(d):
    rows = rj(SRC_DIR / f"{d}.jsonl")
    agreed = set(json.load(open(SRC_DIR / f"{d}.agreed.json")))
    byid = {r["id"]: r for r in rows}
    assert len(byid) == len(rows), f"{d}: duplicate ids in input"
    assert agreed <= set(byid), f"{d}: agreed ids not in rows: {sorted(agreed - set(byid))[:5]}"
    sets = link_sets(rows)
    drop_dis = set(byid) - agreed
    drop_orphan = {i for i in byid if i not in drop_dis and any(j in drop_dis for j in sets[i])}
    kept = [r for r in rows if r["id"] not in drop_dis | drop_orphan]
    solver = {}
    p = SRC_DIR / f"{d}.solver.jsonl"
    if p.exists():
        solver = {x["id"]: x.get("answer") for x in rj(p)}
    before = sum(solver.get(i) == byid[i]["gold"] for i in byid)
    return rows, kept, sorted(drop_dis), sorted(drop_orphan), sets, f"{before}/{len(rows)}"


def clean(r, d):
    return {**{k: r[k] for k in KEYS if k != "meta"},
            "meta": {k: v for k, v in r["meta"].items() if k in META_KEEP[d]}}


# ------------------------------------------------------------------------------------------------ checks
def check_schema(rows, errs):
    byid = {r["id"]: r for r in rows}
    if len(byid) != len(rows):
        errs.append("duplicate ids")
    text2cid, cid2text = {}, {}
    for r in rows:
        k = json.dumps([r["instructions"], r["state"], r["options"]], ensure_ascii=False)
        if text2cid.setdefault(k, r["call_id"]) != r["call_id"]:
            errs.append(f"{r['id']}: same text, different call_id")
        if cid2text.setdefault(r["call_id"], k) != k:
            errs.append(f"{r['id']}: call_id {r['call_id']} shared by different texts")
    if len(text2cid) != len(rows):
        errs.append("duplicate (instructions, state, options) texts")
    for r in rows:
        rid, d = r["id"], r["meta"].get("domain")
        if list(r) != KEYS:
            errs.append(f"{rid}: keys {list(r)}")
            continue
        if d not in CLASSES or r["source"] != f"std_{d}" or r["split"] != "train" or r["track"] != "STD":
            errs.append(f"{rid}: domain/source/split/track")
            continue
        if not re.fullmatch(rf"r_std_{d}_\d+", rid) or not r["group_id"].startswith(f"g:std_{d}:") \
                or not re.fullmatch(r"c_[0-9a-f]{12}", r["call_id"]):
            errs.append(f"{rid}: id / group_id / call_id format")
        if set(r["meta"]) - META_KEEP[d]:
            errs.append(f"{rid}: meta keys {sorted(r['meta'])}")
        for f in ("state", "instructions", "card"):
            if not isinstance(r[f], str) or not r[f].strip() or r[f] != r[f].strip():
                errs.append(f"{rid}: empty or untrimmed {f}")
        if "{" in r["state"] or "}" in r["state"]:
            errs.append(f"{rid}: unfilled slot in state")
        lines = r["card"].split("\n")
        if any(not l.startswith("- ") or ": " not in l[2:] for l in lines):
            errs.append(f"{rid}: card format")
        names = card_names(r)
        if r["qtype"] == "choice":
            o = r["options"]
            if r["role"] != "choice" or not isinstance(o, list) or len(o) < 2 or len(set(o)) != len(o):
                errs.append(f"{rid}: choice fields")
                continue
            if any(": " in x for x in o):
                errs.append(f"{rid}: option contains ': '")
            if r["gold"] not in o:
                errs.append(f"{rid}: gold not in options")
            if names != o:
                errs.append(f"{rid}: card lines do not match options")
            ok = {"evidence": sorted(o) == sorted(CLASSES["evidence"]),
                  "hate": len(o) == 2 and len(set(o) & HATE_POS) == 1 and len(set(o) & HATE_NEG) == 1,
                  "trademark": o in (TM_SCALE, TM_SCALE[::-1]),
                  "hearsay": False}[d]
            if not ok:
                errs.append(f"{rid}: options {o}")
        elif r["qtype"] == "noul":
            if r["options"] is not None or r["role"] != "aff" or isinstance(r["gold"], bool) or r["gold"] not in (0, 1):
                errs.append(f"{rid}: noul fields")
            if d == "hate" and (len(names) != 1 or names[0] not in HATE_POS | HATE_NEG):
                errs.append(f"{rid}: hate noul card {names}")
            if d == "trademark" and (names != TM_SCALE or "base_id" not in r["meta"]):
                errs.append(f"{rid}: trademark noul card/base")
            if d == "hearsay" and "hearsay" not in names:
                errs.append(f"{rid}: hearsay card")
            if d == "evidence":
                errs.append(f"{rid}: evidence rows are choice only")
        else:
            errs.append(f"{rid}: qtype {r['qtype']}")


def check_structure(raw, errs, stats):
    """raw = uncleaned kept rows of every domain (the links live in the original meta)"""
    byid = {r["id"]: r for r in raw}
    grp = defaultdict(list)
    for r in raw:
        grp[r["group_id"]].append(r)
    for d in CLASSES:
        rs = [r for r in raw if r["meta"]["domain"] == d]
        st = Counter()
        if d == "evidence":
            for g, m in grp.items():
                if not g.startswith("g:std_evidence:"):
                    continue
                claim = {x["state"].split("\n\nEvidence:\n", 1)[0] for x in m}
                same = {json.dumps([x["instructions"], x["options"], x["card"]]) for x in m}
                if len(m) != 3 or len(claim) != 1 or len(same) != 1 or sorted(x["gold"] for x in m) != sorted(CLASSES[d]) \
                        or len({x["state"] for x in m}) != 3 or any(not x["state"].startswith("Claim:\n") for x in m):
                    errs.append(f"{g}: not a clean S/R/N triple")
                st["triples"] += 1
        for r in rs:
            t = r["meta"].get("twin_of")
            if t and d in ("hate", "hearsay"):
                b = byid.get(t)
                if b is None:
                    errs.append(f"{r['id']}: twin_of {t} missing")
                    continue
                if "twin_of" in b["meta"] or b["group_id"] != r["group_id"] or b["qtype"] != r["qtype"] \
                        or b["options"] != r["options"] or b["card"] != r["card"]:
                    errs.append(f"{r['id']}: twin differs from its base outside the text")
                if underlying(b, d, byid) == underlying(r, d, byid) or b["state"] == r["state"]:
                    errs.append(f"{r['id']}: twin does not flip the label with a changed text")
                st["twin_pairs"] += 1
                st["twin_pairs_with_changed_question"] += b["instructions"] != r["instructions"]
            if d == "trademark" and r["qtype"] == "noul":
                b = byid.get(r["meta"]["base_id"])
                if b is None or b["qtype"] != "choice" or b["state"] != r["state"] or b["group_id"] != r["group_id"]:
                    errs.append(f"{r['id']}: probe does not reuse its base item")
                    continue
                if r["gold"] != int(b["gold"] == tm_asked(r)):
                    errs.append(f"{r['id']}: probe gold != (base gold == asked category)")
                st["probes"] += 1
                st["probes_asking_base_gold"] += r["gold"]
        if d in ("hate", "hearsay"):
            bases = [r for r in rs if "twin_of" not in r["meta"]]
            if Counter(x["meta"]["twin_of"] for x in rs if "twin_of" in x["meta"]).most_common(1)[0][1] > 1:
                errs.append(f"{d}: a base has more than one twin")
            st["rows_without_twin"] = sum(1 for b in bases if not any(x["meta"].get("twin_of") == b["id"] for x in rs))
        if d == "trademark":
            fam = [g for g, m in grp.items() if g.startswith("g:std_trademark:")
                   and len({x["state"] for x in m}) > 1]
            st["groups_with_several_items"] = len(fam)
            for g in fam:
                seen = Counter(x["state"] for x in grp[g] if x["qtype"] == "choice")
                if max(seen.values()) > 1:
                    errs.append(f"{g}: two choice rows share one state")
        stats[d]["structure"] = dict(st)


def check_balance(rows, byid_all, errs, stats):
    for d in CLASSES:
        rs = [r for r in rows if r["meta"]["domain"] == d]
        ch = [r for r in rs if r["qtype"] == "choice"]
        nl = [r for r in rs if r["qtype"] == "noul"]
        und = Counter(underlying(r, d, byid_all) for r in rs)
        tgt_ch = Counter(target(r, d) for r in ch)
        b = {"underlying_label": dict(und)}
        if len(CLASSES[d]) == 2:
            k = und[CLASSES[d][0]]
            share = k / len(rs)
            pb = binom_p(k, len(rs))
            b["underlying_share_" + CLASSES[d][0].replace(" ", "_")] = round(share, 3)
            if not 0.45 <= share <= 0.55 or pb < ALPHA:
                errs.append(f"{d}: underlying label balance {dict(und)}")
        if ch:
            cnt = [tgt_ch[c] for c in CLASSES[d]]
            mean = sum(cnt) / len(cnt)
            b["choice_gold"] = dict(zip(CLASSES[d], cnt))
            if max(cnt) - min(cnt) > max(2, 0.1 * mean):
                errs.append(f"{d}: choice gold imbalance {dict(zip(CLASSES[d], cnt))}")
            k = len(ch[0]["options"])
            pos = Counter(r["options"].index(r["gold"]) for r in ch)
            p = gof_uniform_p([pos[i] for i in range(k)], k)
            b["choice_gold_position"] = {str(i + 1): pos[i] for i in range(k)}
            b["choice_gold_position_p"] = round(p, 4)
            if p < ALPHA:
                errs.append(f"{d}: gold position skew {dict(pos)} (p={p:.4f})")
        if nl:
            y = sum(r["gold"] for r in nl)
            pb = binom_p(y, len(nl))
            b["noul_yes_no"] = {"yes": y, "no": len(nl) - y}
            if pb < ALPHA or not 0.4 <= y / len(nl) <= 0.6:
                errs.append(f"{d}: noul yes share {y}/{len(nl)}")
            if d == "hate":
                b["noul_asked"] = dict(Counter(hate_asked(r) for r in nl))
            if d == "trademark":
                b["noul_asked"] = dict(Counter(tm_asked(r) for r in nl))
        stats[d]["balance"] = b


def check_leak(rows, byid_all, errs, stats):
    rng = random.Random(SEED)
    one_named = defaultdict(list)  # domain -> [(gold is a named option, share of options named)]
    for r in rows:
        d = r["meta"]["domain"]
        m = LEAK[d].search(r["state"])
        if m:
            errs.append(f"{r['id']}: label word in state: {m.group(0)!r}")
        if BANNED.search(r["state"]) or BANNED.search(r["instructions"]) or BANNED.search(r["card"]):
            errs.append(f"{r['id']}: dataset name in text")
        if r["qtype"] == "choice":
            named = [o for o in r["options"] if re.search(rf"(?<![\w-]){re.escape(o)}(?![\w-])", r["instructions"], re.I)]
            # an option inside another named option ("hateful" in "not hateful") does not count on its own
            named = [o for o in named if not any(o != p and o in p for p in named)]
            if named and len(named) < len(r["options"]):  # e.g. "Is the post hateful or not?"
                one_named[d].append((r["gold"] in named, len(named) / len(r["options"])))
    for d, v in one_named.items():
        # choice instructions that name only some options must not point at the gold more often than chance
        shares = {s for _, s in v}
        k, n = sum(g for g, _ in v), len(v)
        p = binom_p(k, n, shares.pop()) if len(shares) == 1 else 0.0
        stats[d]["choice_instructions_naming_some_options"] = {"rows": n, "gold_is_named": k, "p": round(p, 4)}
        if p < ALPHA:
            errs.append(f"{d}: choice instructions that name some options point at the gold ({k}/{n}, p={p:.4f})")
    for d in CLASSES:
        rs = [r for r in rows if r["meta"]["domain"] == d]
        tests = {}
        for qt in ("choice", "noul"):
            q = [r for r in rs if r["qtype"] == qt]
            if not q:
                continue
            y = [target(r, d) for r in q]
            cues = {"instructions": [r["instructions"] for r in q], "card": [r["card"] for r in q]}
            if qt == "choice":
                cues["option_order"] = [json.dumps(r["options"]) for r in q]
            if qt == "noul" and d == "hate":
                cues["asked_label"] = [hate_asked(r) for r in q]
            if qt == "noul" and d == "trademark":
                cues["asked_label"] = [tm_asked(r) for r in q]
            for k in sorted({k for r in q for k in r["meta"]} - {"domain"}):
                cues[f"meta.{k}"] = [("has" if k in ("twin_of", "base_id") and k in r["meta"] else
                                      str(r["meta"].get(k))) for r in q]
            if d == "hate":  # the underlying label (not just the yes/no answer) must not follow the question form
                cues["underlying_vs_instructions"] = None
            for name, xs in cues.items():
                if xs is None:
                    xs, yy = [r["instructions"] for r in q], [underlying(r, d, byid_all) for r in q]
                else:
                    yy = y
                p = perm_p(xs, yy, rng)
                tests[f"{qt}:{name}"] = {"distinct": len(set(xs)), "p": None if p is None else round(p, 4)}
                if p is not None and p < ALPHA:
                    errs.append(f"{d}: {qt} cue {name} predicts the target (permutation p={p:.4f})")
        # length cue: words in the state, one-vs-rest AUC per underlying class (reported only)
        words = defaultdict(list)
        for r in rs:
            words[underlying(r, d, byid_all)].append(len(r["state"].split()))
        la = {c: round(auc(words[c], [w for o in words if o != c for w in words[o]]), 3) for c in CLASSES[d]
              if words[c] and len(words) > 1}
        if len(CLASSES[d]) == 2:
            la = {CLASSES[d][0]: la[CLASSES[d][0]]}
        stats[d]["leak"] = {"label_words_in_state": sum(bool(LEAK[d].search(r["state"])) for r in rs),
                            "cue_tests": tests, "length_auc_one_vs_rest": la,
                            "mean_state_words": {c: round(sum(v) / len(v), 1) for c, v in words.items()}}
        if d in stats and "choice_instructions_naming_some_options" in stats[d]:
            stats[d]["leak"]["choice_instructions_naming_some_options"] = \
                stats[d].pop("choice_instructions_naming_some_options")


def check_near_dups(rows, raw_sets, byid_all, errs, stats):
    info = {r["id"]: set(toks(r["state"])) for r in rows}
    exact = defaultdict(set)
    for r in rows:
        exact[" ".join(toks(r["state"]))].add(r["group_id"])
    for k, g in exact.items():
        if len(g) > 1:
            errs.append(f"same state text in different groups {sorted(g)}")
    cross = {}
    same_grp = defaultdict(list)
    linked = defaultdict(list)
    for a, b in combinations(rows, 2):
        ov = overlap(info[a["id"]], info[b["id"]])
        da = a["meta"]["domain"]
        if a["group_id"] != b["group_id"]:
            key = da if da == b["meta"]["domain"] else "cross_domain"
            if ov > cross.get(key, (0,))[0]:
                cross[key] = (round(ov, 3), a["id"], b["id"])
            if ov > NEAR:
                errs.append(f"near-duplicate across groups {a['id']} {b['id']} {ov:.2f}")
        elif raw_sets[a["id"]] == raw_sets[b["id"]]:
            linked[da].append(ov)
        else:
            same_grp[da].append(ov)
            if ov > NEAR and target(a, da) == target(b, da) and a["qtype"] == b["qtype"]:
                errs.append(f"near-duplicate inside group, same target {a['id']} {b['id']} {ov:.2f}")
    med = lambda v: round(sorted(v)[len(v) // 2], 3)
    stats["near_dup_within_block"] = {
        "max_overlap_across_groups": {k: {"overlap": v[0], "pair": [v[1], v[2]]} for k, v in sorted(cross.items())},
        "linked_rows_overlap_min_median_max": {d: [round(min(v), 3), med(v), round(max(v), 3)]
                                               for d, v in sorted(linked.items())},
        "same_group_unlinked_overlap_max": {d: round(max(v), 3) for d, v in sorted(same_grp.items())},
    }


def check_other(rows, errs, stats):
    """near-duplicates, exact matches, 12-word runs (eval) and id / call_id clashes against the other data"""
    sh = lambda t, n: {" ".join(t[i:i + n]) for i in range(max(1, len(t) - n + 1))}
    index = defaultdict(list)
    info, exact, g12 = {}, {}, defaultdict(set)
    for r in rows:
        t = toks(r["state"])
        info[r["id"]] = set(t)
        exact.setdefault(" ".join(t), r["id"])
        for s in sh(t, 5):
            index[s].append(r["id"])
        if len(t) >= 12:
            for s in sh(t, 12):
                g12[s].add(r["id"])
    ours_c, ours_i = {r["call_id"] for r in rows}, {r["id"] for r in rows}
    per_file = {}
    for f in TRAIN_OTHER + DEV_OTHER + EVAL_OTHER:
        p = D / f
        if not p.exists():
            per_file[f] = "missing"
            errs.append(f"{f}: missing (cannot check overlap)")
            continue
        mx, n, clash, seen, hits12 = (0.0, None), 0, 0, set(), 0
        for line in open(p):
            o = json.loads(line)
            n += 1
            if o.get("call_id") in ours_c or o.get("id") in ours_i:
                clash += 1
            s = o.get("state")
            if not isinstance(s, str):
                s = json.dumps(s, ensure_ascii=False) if s is not None else ""
            h = hash(s)
            if h in seen:
                continue
            seen.add(h)
            t = toks(s)
            j = " ".join(t)
            if j in exact:
                errs.append(f"exact state match with {f}:{o.get('id')} -> {exact[j]}")
            if f in EVAL_OTHER and len(t) >= 12:
                shared = {i for s12 in sh(t, 12) for i in g12.get(s12, ())}
                if shared:
                    hits12 += 1
                    errs.append(f"shared 12-word run with {f}:{o.get('id')} -> {sorted(shared)[:3]}")
            cand = {i for s5 in sh(t, 5) for i in index.get(s5, ())}
            if not cand:
                continue
            ot = set(t)
            for i in sorted(cand):
                ov = overlap(info[i], ot)
                if ov > mx[0]:
                    mx = (ov, f"{i} ~ {o.get('id')}")
                if ov > NEAR:
                    errs.append(f"near-duplicate of {f}:{o.get('id')} -> {i} {ov:.2f}")
        if clash:
            errs.append(f"{f}: {clash} id/call_id clashes")
        per_file[f] = {"rows": n, "distinct_states": len(seen), "max_overlap": round(mx[0], 3), "at": mx[1]}
        if f in EVAL_OTHER:
            per_file[f]["states_sharing_12_word_run"] = hits12
    stats["near_dup_vs_other_data"] = per_file


# ------------------------------------------------------------------------------------------------ main
def main():
    domains = sorted(p.name[: -len(".agreed.json")] for p in SRC_DIR.glob("*.agreed.json"))
    assert set(domains) <= set(CLASSES), f"no rules for domains {set(domains) - set(CLASSES)}"
    out, raw_kept, raw_sets, report = [], [], {}, {"domains": {}}
    for d in domains:
        rows, kept, drop_dis, drop_orphan, sets, before = load(d)
        raw_kept += kept
        raw_sets.update({r["id"]: sets[r["id"]] for r in kept})
        out += [clean(r, d) for r in kept]
        report["domains"][d] = {
            "input_rows": len(rows),
            "solver_agreement_before_review": before,
            "agreed": len(rows) - len(drop_dis),
            "dropped_disagreed": drop_dis,
            "dropped_orphan_twins": drop_orphan,
            "kept": len(kept),
            "groups": len({r["group_id"] for r in kept}),
            "linked_sets": len({sets[r["id"]] for r in kept if len(sets[r["id"]]) > 1}),
            "qtype": dict(Counter(r["qtype"] for r in kept)),
            "distinct_instructions": {qt: len({r["instructions"] for r in kept if r["qtype"] == qt})
                                      for qt in ("choice", "noul") if any(r["qtype"] == qt for r in kept)},
            "distinct_cards": len({r["card"] for r in kept}),
            "meta_keys_dropped": sorted({k for r in kept for k in r["meta"]} - META_KEEP[d]),
        }
    byid_all = {r["id"]: r for r in out}
    errs, stats = [], {d: {} for d in domains}
    check_schema(out, errs)
    check_structure(raw_kept, errs, stats)
    check_balance(out, byid_all, errs, stats)
    check_leak(out, byid_all, errs, stats)
    glob_stats = {}
    check_near_dups(out, raw_sets, byid_all, errs, glob_stats)
    check_other(out, errs, glob_stats)
    for d in domains:
        report["domains"][d]["checks"] = stats[d]
    report["rows"] = len(out)
    report["rows_by_domain"] = dict(Counter(r["meta"]["domain"] for r in out))
    # length cue: reported, not enforced (a class whose states are much longer or shorter than the rest)
    warns = [f"{d}: state length separates '{c}' from the other classes (one-vs-rest AUC {a})"
             for d in domains for c, a in stats[d]["leak"]["length_auc_one_vs_rest"].items() if abs(a - 0.5) > 0.2]
    report["checks"] = {**glob_stats, "warnings": warns, "errors": errs}
    print(json.dumps(report, indent=1))
    if errs:
        print(f"VALIDATION FAILED ({len(errs)} errors); nothing written")
        sys.exit(1)
    OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out))
    SUMMARY.write_text(json.dumps(report, indent=1) + "\n")
    print("wrote", OUT, len(out), "rows")


if __name__ == "__main__":
    main()
