"""Assemble the v0.11b BINJ training block (balanced two-option judgments with minimal-pair twins).

Inputs (data/v11_parts/binj/), one set per domain (adult, consistency, intent, offensive):
  <domain>.jsonl        teacher-written rows with gold (Claude-authored; no external model, no external dataset)
  <domain>.agreed.json  ids where an independent blind solve agreed with the gold (after review)

Steps per domain
  1. keep only agreed ids; drop a twin when its base was dropped and a base when its twin was dropped
  2. rebalance the underlying label to exactly 50/50 by dropping extra rows of the larger class; only rows outside
     twin pairs are dropped, chosen deterministically (largest qtype cell first, then over-used gold position / yes-no
     answer, then a hash of the id)
  3. meta cut to the schema: {"domain", "twin_of"?}. consistency's meta.error names the error type of an
     inconsistent row (it gives away the gold), so it is dropped along with genre/frame; counts go to the summary.
Checks (any failure -> exit 1, nothing written)
  schema, ids / call_ids unique (and no call_id shared with train_v11 or the dev sets checked below), twins intact
  and label-flipping (a twin's question may differ only by naming its own, renamed author), exact 50/50 per domain,
  no label words in the text, no card wording / instruction phrasing / yes-no asked label tied to one label (exact
  binomial vs a fair coin, p < 0.01 fails), no near-duplicates (normalized token overlap > 0.8) inside the block or
  against train_v11 / hard_dev / taskbank_dev / dev_claims / dev_negwords. State length vs label is reported
  (length_auc; 0.5 = no cue), not enforced.
  Intended minimal pairs are not near-duplicates: rows sharing a group_id (a base and its twin; for consistency,
  summaries of one shared source) are compared on the part that differs and only flagged when the label is the same.
Writes data/v11_parts/binj_train.jsonl and data/v11_parts/binj_train_summary.json. CPU only; deterministic.
"""
import hashlib
import json
import math
import re
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE / "data"
SRC_DIR = D / "v11_parts" / "binj"
OUT = D / "v11_parts" / "binj_train.jsonl"
SUMMARY = D / "v11_parts" / "binj_train_summary.json"
DOMAINS = ["adult", "consistency", "intent", "offensive"]
NEAR = 0.8
ALPHA = 0.01
# other data checked for near-duplicates / call_id clashes (dev_nc and every ohs file are never opened)
OTHER = ["train_v11.jsonl", "hard_dev.jsonl", "taskbank_dev.jsonl", "dev_claims.jsonl", "dev_negwords.jsonl"]

# label names; POS = the side the model over-uses for adult/intent/offensive ("flag"), and "inconsistent" for
# consistency (the model's bias there is the other way: too lenient). Balance is checked on this 0/1 label.
POS = {"adult": {"sexual content", "sexual", "contains sexual content"},
       "offensive": {"offensive"},
       "intent": {"intended to offend", "deliberately offensive", "meant to offend"},
       "consistency": {"factually inconsistent"}}
NEG = {"adult": {"no sexual content", "not sexual", "free of sexual content"},
       "offensive": {"not offensive", "non-offensive"},
       "intent": {"not intended to offend", "not deliberately offensive", "not meant to offend"},
       "consistency": {"factually consistent"}}
POS_NAME = {"adult": "sexual", "offensive": "offensive", "intent": "intended", "consistency": "inconsistent"}
NEG_NAME = {"adult": "not_sexual", "offensive": "not_offensive", "intent": "not_intended", "consistency": "consistent"}
LEAK = {
    "adult": re.compile(r"sexual content|\bnot sexual\b|non-sexual|\bnsfw\b|\bexplicit\b", re.I),
    "offensive": re.compile(r"\boffensive\b|\binoffensive\b|non-offensive", re.I),
    "intent": re.compile(r"intended to offend|meant to offend|deliberately offensive", re.I),
    "consistency": re.compile(r"\b(in)?consisten(t|cy)\b|\bfaithful\b|\bhallucinat", re.I),
}
BANNED = re.compile(r"social bias frames|trueteacher|btzsc|hatecheck", re.I)
SUM_HEADS = ["Summary:", "Generated summary:", "Summary to check:", "Model-written summary:",
             "Claim:", "Claim to verify:", "Statement:"]
KEYS = ["id", "group_id", "call_id", "split", "track", "source", "state", "qtype", "instructions", "options", "gold",
        "role", "card", "meta"]

rj = lambda p: [json.loads(l) for l in open(p)]
hid = lambda s: hashlib.sha1(s.encode()).hexdigest()
toks = lambda s: re.findall(r"[a-z0-9]+", s.lower())


def asked(r):
    """yes/no rows: the label the question asks about is the first card line (intent adds the other label's
    definition as a second line for contrast)"""
    return r["card"].split("\n")[0][2:].split(": ", 1)[0]


def binom_p(k, n):
    """two-sided exact binomial p-value for k of n under p = 0.5"""
    k = max(k, n - k)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k, n + 1)) / 2 ** n)


def label(r, d):
    """1 = POS side, 0 = NEG side, whatever the question wording."""
    if r["qtype"] == "choice":
        return int(r["gold"] in POS[d])
    a = asked(r)
    return r["gold"] if a in POS[d] else 1 - r["gold"]


def overlap(a, b):
    """normalized token overlap: shared distinct lower-cased word tokens / distinct tokens of the shorter text"""
    return len(a & b) / max(1, min(len(a), len(b)))


def split_summary(state):
    """consistency rows: (summary or claim, rest of the state)"""
    pat = r"(^|\n\n)(" + "|".join(re.escape(h) for h in SUM_HEADS) + r")\n(.*?)(?=\n\n|$)"
    m = list(re.finditer(pat, state, re.S))
    assert m, "no summary header"
    m = m[-1]
    return m.group(3), state[:m.start()] + "\n\n" + state[m.end():]


# ------------------------------------------------------------------------------------------------ assemble
def load(d):
    rows = rj(SRC_DIR / f"{d}.jsonl")
    agreed = set(json.load(open(SRC_DIR / f"{d}.agreed.json")))
    byid = {r["id"]: r for r in rows}
    assert agreed <= set(byid), f"{d}: agreed ids not in rows"
    drop_disagree = set(byid) - agreed
    drop_pair = set()
    for r in rows:
        t = r["meta"].get("twin_of")
        if t and (t in drop_disagree or r["id"] in drop_disagree):
            drop_pair |= {t, r["id"]}
    drop_pair -= drop_disagree
    kept = [r for r in rows if r["id"] not in drop_disagree | drop_pair]
    return rows, kept, sorted(drop_disagree), sorted(drop_pair)


def rebalance(kept, d):
    lab = {r["id"]: label(r, d) for r in kept}
    paired = {r["meta"]["twin_of"] for r in kept if "twin_of" in r["meta"]} | \
             {r["id"] for r in kept if "twin_of" in r["meta"]}
    dropped = []
    while True:
        c = Counter(lab[r["id"]] for r in kept)
        if c[1] == c[0]:
            break
        big = 1 if c[1] > c[0] else 0
        cell = Counter((r["qtype"], lab[r["id"]]) for r in kept)
        pos0 = Counter(r["options"].index(r["gold"]) for r in kept if r["qtype"] == "choice")
        yes = Counter(r["gold"] for r in kept if r["qtype"] == "noul")
        cand = [r for r in kept if lab[r["id"]] == big and r["id"] not in paired]
        assert cand, f"{d}: cannot rebalance without breaking a twin pair"

        def key(r):
            # prefer the qtype whose cell for this label is most over-full relative to the other label
            skew = cell[(r["qtype"], big)] - cell[(r["qtype"], 1 - big)]
            if r["qtype"] == "choice":
                sub = pos0[r["options"].index(r["gold"])] - pos0[1 - r["options"].index(r["gold"])]
            else:
                sub = yes[r["gold"]] - yes[1 - r["gold"]]
            return (-skew, -sub, hid(r["id"]))

        r = min(cand, key=key)
        kept = [x for x in kept if x["id"] != r["id"]]
        dropped.append(r["id"])
    return kept, dropped


def clean(r, d):
    m = {"domain": d}
    if "twin_of" in r["meta"]:
        m["twin_of"] = r["meta"]["twin_of"]
    return {**{k: r[k] for k in KEYS if k != "meta"}, "meta": m}


# ------------------------------------------------------------------------------------------------ checks
def check_schema(rows, errs, renamed):
    byid = {r["id"]: r for r in rows}
    if len(byid) != len(rows):
        errs.append("duplicate ids")
    if len({r["call_id"] for r in rows}) != len(rows):
        errs.append("duplicate call_ids")
    seen = {}
    for r in rows:
        k = json.dumps([r["instructions"], r["state"], r["options"]], ensure_ascii=False)
        if k in seen:
            errs.append(f"{r['id']}: same (instructions, state, options) as {seen[k]}")
        seen[k] = r["id"]
    for r in rows:
        rid, d = r["id"], r["meta"].get("domain")
        if list(r) != KEYS:
            errs.append(f"{rid}: keys {list(r)}")
            continue
        if d not in DOMAINS or r["source"] != f"binj_{d}" or r["split"] != "train" or r["track"] != "BINJ":
            errs.append(f"{rid}: domain/source/split/track")
        if set(r["meta"]) - {"domain", "twin_of"}:
            errs.append(f"{rid}: meta keys {sorted(r['meta'])}")
        for f in ("id", "group_id", "call_id", "state", "instructions", "card"):
            if not isinstance(r[f], str) or not r[f].strip():
                errs.append(f"{rid}: empty {f}")
        if not r["group_id"].startswith(f"g:binj_{d}:"):
            errs.append(f"{rid}: group_id prefix")
        lines = r["card"].split("\n")
        if any(not l.startswith("- ") or ": " not in l[2:] for l in lines):
            errs.append(f"{rid}: card format")
        if r["qtype"] == "choice":
            o = r["options"]
            if r["role"] != "choice" or not isinstance(o, list) or len(o) != 2 or len(set(o)) != 2:
                errs.append(f"{rid}: choice fields")
                continue
            if r["gold"] not in o:
                errs.append(f"{rid}: gold not in options")
            if not ((o[0] in POS[d] and o[1] in NEG[d]) or (o[1] in POS[d] and o[0] in NEG[d])):
                errs.append(f"{rid}: options are not one POS and one NEG label {o}")
            if [l[2:].split(": ", 1)[0] for l in lines] != o:
                errs.append(f"{rid}: card lines do not match options")
        elif r["qtype"] == "noul":
            if r["options"] is not None or r["role"] != "aff" or isinstance(r["gold"], bool) or r["gold"] not in (0, 1):
                errs.append(f"{rid}: noul fields")
            terms = [l[2:].split(": ", 1)[0] for l in lines]
            if asked(r) not in POS[d] | NEG[d] or len(lines) > 2 or \
                    (len(lines) == 2 and not ({terms[0], terms[1]} & POS[d] and {terms[0], terms[1]} & NEG[d])):
                errs.append(f"{rid}: noul card {terms}")
        else:
            errs.append(f"{rid}: qtype {r['qtype']}")
    for r in rows:
        t = r["meta"].get("twin_of")
        if not t:
            continue
        b = byid.get(t)
        if b is None:
            errs.append(f"{r['id']}: twin_of {t} missing")
            continue
        d = r["meta"]["domain"]
        if "twin_of" in b["meta"] or b["group_id"] != r["group_id"] or b["qtype"] != r["qtype"] \
                or b["options"] != r["options"] or b["card"] != r["card"]:
            errs.append(f"{r['id']}: twin differs from base outside the text")
        if b["instructions"] != r["instructions"]:
            # allowed only when the question names the author and the twin changed who the author is
            w3 = lambda x: {w for w in toks(x) if len(w) >= 3}  # ignore possessive 's and short function words
            ib, it_ = w3(b["instructions"]), w3(r["instructions"])
            if not ((ib - it_) <= set(toks(b["state"])) and (it_ - ib) <= set(toks(r["state"]))):
                errs.append(f"{r['id']}: twin instructions differ beyond the named author")
            else:
                renamed.append(r["id"])
        if label(b, d) == label(r, d) or b["gold"] == r["gold"] or b["state"] == r["state"]:
            errs.append(f"{r['id']}: twin does not flip the label")
    bases_with_twin = Counter(r["meta"]["twin_of"] for r in rows if "twin_of" in r["meta"])
    if bases_with_twin and max(bases_with_twin.values()) > 1:
        errs.append("a base has more than one twin")


def check_balance(rows, errs):
    for d in DOMAINS:
        c = Counter(label(r, d) for r in rows if r["meta"]["domain"] == d)
        if c[1] != c[0]:
            errs.append(f"{d}: label balance {dict(c)}")


def check_leak(rows, errs, stats):
    for r in rows:
        d = r["meta"]["domain"]
        if LEAK[d].search(r["state"]):
            errs.append(f"{r['id']}: label word in state: {LEAK[d].search(r['state']).group(0)!r}")
        if BANNED.search(r["state"]) or BANNED.search(r["instructions"]):
            errs.append(f"{r['id']}: banned dataset name")
    for d in DOMAINS:
        rs = [r for r in rows if r["meta"]["domain"] == d]
        # no surface cue may predict the label: every card wording, every instruction phrasing and, for yes/no rows,
        # the answer within each asked label are tested against a fair coin (exact binomial, p < ALPHA fails)
        cues = {"card": defaultdict(Counter), "instruction": defaultdict(Counter), "noul_answer": defaultdict(Counter)}
        for r in rs:
            cues["card"][r["card"]][label(r, d)] += 1
            cues["instruction"][(r["qtype"], r["instructions"])][label(r, d)] += 1
            if r["qtype"] == "noul":
                cues["noul_answer"][asked(r)][r["gold"]] += 1
        minp = {}
        for kind, groups in cues.items():
            best = (1.0, None)
            for k, c in groups.items():
                n = sum(c.values())
                p = binom_p(max(c.values()), n)
                if p < best[0]:
                    best = (p, f"{str(k)[:80]} {dict(c)}")
                if p < ALPHA:
                    errs.append(f"{d}: {kind} cue {str(k)[:80]!r} -> labels {dict(c)} (p={p:.4f})")
            minp[kind] = {"distinct": len(groups), "min_p": round(best[0], 4), "at": best[1]}
        wc = defaultdict(list)
        for r in rs:
            wc[label(r, d)].append(len(r["state"].split()))
        auc = sum((x > y) + 0.5 * (x == y) for x in wc[1] for y in wc[0]) / (len(wc[1]) * len(wc[0]))
        stats[d] = {"label_cue_tests": minp, "length_auc": round(auc, 3),
                    "mean_state_words": {POS_NAME[d]: round(sum(wc[1]) / len(wc[1]), 1),
                                         NEG_NAME[d]: round(sum(wc[0]) / len(wc[0]), 1)}}


def compare_text(r):
    """(shared-context key, text that differs): consistency rows of one source differ only in the summary"""
    if r["meta"]["domain"] == "consistency":
        s, rest = split_summary(r["state"])
        return rest, s
    return None, r["state"]


def check_near_dups(rows, errs, stats):
    info = {}
    for r in rows:
        ctx, diff = compare_text(r)
        info[r["id"]] = (set(toks(r["state"])), set(toks(diff)), ctx)
    # consistency: rows of one group must share the same source text
    grp_ctx = defaultdict(set)
    for r in rows:
        if r["meta"]["domain"] == "consistency":
            grp_ctx[r["group_id"]].add(info[r["id"]][2])
    for g, v in grp_ctx.items():
        if len(v) != 1:
            errs.append(f"{g}: rows of one consistency group do not share a source")
    same_grp_max, cross_max, contrast_pairs = 0.0, 0.0, 0
    twin_ov = []
    for a, b in combinations(rows, 2):
        if a["group_id"] == b["group_id"]:
            ov = overlap(info[a["id"]][1], info[b["id"]][1])
            twin = a["meta"].get("twin_of") == b["id"] or b["meta"].get("twin_of") == a["id"]
            if twin:
                twin_ov.append(ov)
                continue
            da = a["meta"]["domain"]
            if ov > NEAR:
                if label(a, da) == label(b, da):
                    errs.append(f"near-duplicate (same group, same label) {a['id']} {b['id']} {ov:.2f}")
                else:
                    contrast_pairs += 1
            same_grp_max = max(same_grp_max, ov)
        else:
            ov = overlap(info[a["id"]][0], info[b["id"]][0])
            cross_max = max(cross_max, ov)
            if ov > NEAR:
                errs.append(f"near-duplicate {a['id']} {b['id']} {ov:.2f}")
    stats["near_dup_within_block"] = {
        "max_overlap_across_groups": round(cross_max, 3),
        "max_overlap_same_group_non_twin": round(same_grp_max, 3),
        "same_group_opposite_label_contrast_pairs_over_0.8": contrast_pairs,
        "twin_pair_overlap_min_median_max": [round(min(twin_ov), 3), round(sorted(twin_ov)[len(twin_ov) // 2], 3),
                                              round(max(twin_ov), 3)] if twin_ov else None,
    }


def check_other(rows, errs, stats):
    """near-duplicates and call_id clashes against train_v11 and the dev sets (candidates via shared word 5-grams)"""
    sh = lambda t: {" ".join(t[i:i + 5]) for i in range(max(1, len(t) - 4))}
    index = defaultdict(list)
    info = {}
    for r in rows:
        t = toks(r["state"])
        info[r["id"]] = set(t)
        for s in sh(t):
            index[s].append(r["id"])
    ours = {r["call_id"] for r in rows}
    per_file = {}
    for f in OTHER:
        p = D / f
        if not p.exists():
            per_file[f] = "missing"
            continue
        mx, n, clash = 0.0, 0, 0
        for line in open(p):
            o = json.loads(line)
            n += 1
            if o.get("call_id") in ours:
                clash += 1
            t = toks(o.get("state") or "")
            cand = {i for s in sh(t) for i in index.get(s, ())}
            if not cand:
                continue
            ot = set(t)
            for i in cand:
                ov = overlap(info[i], ot)
                mx = max(mx, ov)
                if ov > NEAR:
                    errs.append(f"near-duplicate of {f}:{o.get('id')} -> {i} {ov:.2f}")
        if clash:
            errs.append(f"{f}: {clash} call_id clashes")
        per_file[f] = {"rows": n, "max_overlap": round(mx, 3)}
    stats["near_dup_vs_other_data"] = per_file


# ------------------------------------------------------------------------------------------------ main
def main():
    out, report = [], {"domains": {}}
    for d in DOMAINS:
        rows, kept, drop_dis, drop_pair = load(d)
        kept, drop_bal = rebalance(kept, d)
        kept = [clean(r, d) for r in kept]
        out.extend(kept)
        ch = [r for r in kept if r["qtype"] == "choice"]
        nl = [r for r in kept if r["qtype"] == "noul"]
        lab = Counter(label(r, d) for r in kept)
        errors = Counter(r["meta"]["error"] for r in rows
                         if "error" in r["meta"] and r["id"] in {k["id"] for k in kept})
        report["domains"][d] = {
            "input_rows": len(rows),
            "dropped_disagreed": drop_dis,
            "dropped_partner_of_disagreed": drop_pair,
            "dropped_to_rebalance": drop_bal,
            "kept": len(kept),
            "label": {POS_NAME[d]: lab[1], NEG_NAME[d]: lab[0]},
            "label_by_qtype": {qt: {POS_NAME[d]: sum(label(r, d) == 1 for r in rs),
                                    NEG_NAME[d]: sum(label(r, d) == 0 for r in rs)}
                               for qt, rs in (("choice", ch), ("noul", nl))},
            "twin_pairs": sum("twin_of" in r["meta"] for r in kept),
            "choice_gold_position": {"first": sum(r["options"][0] == r["gold"] for r in ch),
                                     "second": sum(r["options"][1] == r["gold"] for r in ch)},
            "noul_answer": {"yes": sum(r["gold"] == 1 for r in nl), "no": sum(r["gold"] == 0 for r in nl)},
            "noul_asked": dict(Counter(asked(r) for r in nl)),
            "distinct_instructions": {"choice": len({r["instructions"] for r in ch}),
                                      "noul": len({r["instructions"] for r in nl})},
        }
        if errors:
            report["domains"][d]["error_types_of_inconsistent_rows"] = dict(errors.most_common())
    errs, stats, renamed = [], {}, []
    check_schema(out, errs, renamed)
    check_balance(out, errs)
    check_leak(out, errs, stats)
    check_near_dups(out, errs, stats)
    check_other(out, errs, stats)
    report["rows"] = len(out)
    for d in DOMAINS:
        report["domains"][d]["checks"] = stats.pop(d)
    report["checks"] = {**stats, "twins_whose_question_names_a_renamed_author": renamed, "errors": errs}
    print(json.dumps(report, indent=1))
    if errs:
        print(f"VALIDATION FAILED ({len(errs)} errors); nothing written")
        sys.exit(1)
    OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out))
    SUMMARY.write_text(json.dumps(report, indent=1) + "\n")
    print("wrote", OUT, len(out), "rows")


if __name__ == "__main__":
    main()
