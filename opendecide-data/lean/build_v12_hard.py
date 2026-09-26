"""v0.12 HARD items (2B weak spots, chosen on dev only): merge the per-family files into one train and one dev file, check them.
Same checks as build_v11_hard.py; inputs in data/v12_parts/hard/, outputs data/v12_parts/hard12_*. The 12-gram check also
covers every current train/dev file (v0.11 hard, std, binj, the 2B mix, all dev sets), and ids must not clash with them.
OHS-2 task families (stance, tables, patents, medical abstracts, RCT roles, science claims, evidence inference, DDI,
moral stories) were excluded at authoring time.


Inputs, one set per domain key in data/v12_parts/hard/:
  <key>.jsonl          authored items with gold (written by Claude as teacher, no external data or model calls)
  <key>.agreed.json    ids where an independent blind solve agreed with gold (after review)
  <key>.solver.jsonl   the blind solver's answers (used here only to report the agreement rate)

Steps (deterministic, seed 20261001, CPU only; re-run with
  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python build_v11_hard.py):
  1. Keep agreed ids only. Twins (meta.twin_of) are all-or-nothing: if the base or the twin is dropped for any
     reason, both go, so no orphan twins remain.
  2. Adversarial checks, and every flagged item is removed (with its twin partner):
     - schema: keys, types, qtype/role/gold/options/card consistency, unique ids, call_id <-> text consistency,
       no id or call_id clash with the other v11 parts or train_v07;
     - gold leakage: an explicit answer line ("Answer: ...") in the state, or the gold option stated in the state as
       someone's claim (draft / suggested / logged / ticked ... lines). A claim that equals gold is kept only when
       it carries no signal, meaning a twin in the same group repeats the same claim line with a different gold,
       or when the item is listed in CLAIM_REVIEWED with the reason it was reviewed as not a leak;
     - near-duplicates: word-trigram overlap coefficient > 0.8 on normalized state+instructions+options between
       items of different groups (anywhere in the hard set);
     - contamination: any shared 12-word run (per field: state, instructions, options, card) with
       data/train_v07.jsonl, data/eval_card.jsonl or data/eval_jagged.jsonl.
  3. Split: about 10% of groups per domain go to dev. The split unit is a family: groups joined when they share
     a group_id (so twins never split) or when two items of different groups have trigram overlap > 0.5 (the same
     rulebook or passage re-used). This keeps shared scenario text from straddling train and dev.
  4. Relations: equiv / complement only between yes/no items of the same group that share state and card
     and are NOT twins (a twin flips gold with an edited state, so it is neither equiv nor complement).
     Roles aff/para/dneg are positive and neg is negative; the same polarity with the same gold gives equiv,
     and opposite polarity with golds summing to 1 gives complement.
  5. Balance report per domain (yes-rate, none-of-these rate, gold position, gold-is-longest-option rate,
     leave-one-out majority guess from the option set alone) and a JSON summary.

Held-out rules respected: this script never opens data/ohs*.jsonl, data/ohs_parts/, ohs/ or ../bench.

Outputs (data/v12_parts/): hard12_train.jsonl, hard12_dev.jsonl, hard12_relations.jsonl (train), hard12_dev_relations.jsonl,
hard12_dropped.jsonl (id, domain, reasons), hard12_summary.json.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import scipy.sparse as sp

SEED = 20261001
HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
PARTS = DATA / "v12_parts"
HARD = PARTS / "hard"
V11 = DATA / "v11_parts"
REFS = [DATA / f for f in ("train_v07.jsonl", "eval_card.jsonl", "eval_jagged.jsonl", "train_2b_kd.jsonl", "dev.jsonl", "devzs.jsonl",
        "devp_card.jsonl", "pg_dev.jsonl", "dev_nc.jsonl", "taskbank_dev.jsonl", "hard_dev.jsonl", "dev_negwords.jsonl",
        "dev_claims.jsonl")] + [V11 / f for f in ("hard_train.jsonl", "hard_dev.jsonl", "std_train.jsonl", "binj_train.jsonl")]
DEV_FRAC = 0.10
NEAR_DUP = 0.8
FAMILY_LINK = 0.5
NGRAM = 12
NONE = "none of these"

KEYS = ["id", "group_id", "call_id", "split", "track", "source", "state", "qtype", "instructions", "options", "gold",
        "role", "card", "meta"]
ROLE_SIGN = {"aff": 1, "para": 1, "dneg": 1, "neg": -1}

# Gold-claim flags that were read one by one and judged not to be leaks (id -> reason).
CLAIM_REVIEWED = {}

# Task families shared with the held-out OHS-1 parts (named in PREREG_OHS.md). Taxonomy-level overlap only: no OHS
# item or source-dataset text is used, and the 12-gram check cannot see those sources (they are never opened).
OHS_FAMILY_NOTE = {
    "nli_c": "OHS-1 negation: negation-heavy NLI (ScoNe / This-is-not-a-dataset style); not an OHS-2 family",
    "intent_c": "OHS-1 negation: HateCheck-like contrasts (quoting, reclaimed terms); not an OHS-2 family",
    "policy_c": "OHS-1 negation: hateful-conduct exceptions mirror HateCheck functionalities; not an OHS-2 family",
    "affect_c": "OHS-1 emo_intent: emotion labels (own label sets, not GoEmotions); not an OHS-2 family",
}

CUE = re.compile(
    r"\b(suggest(?:ed|s|ion)?|draft|logged|ticked|self-assess\w*|propos(?:ed|es|al)|provisional|preliminary|"
    r"auto-?tag\w*|tagged it|requested route|recommend(?:s|ed|ation)?|told the \w+|rated it|classed|put it down|"
    r"asks for the|bot|verdict|label it|calls? it|isn.t (?:she|he|it|this) an?|"
    r"should be (?:rated|classed|tagged|labelled|labeled|a|an))\b", re.I)
RULE_LINE = re.compile(
    r"(→|->|\bmeans\b|\bif\b|\bunless\b|\bwhere\b|\bmust\b|\bshall\b|\bis classified as\b|\bare treated as\b|"
    r"\bapplies\b|\botherwise\b|^\s*(?:[•·]|\(\w+\)|\d+[.)]|[A-Z][\w.-]*\s*\d*[.:)]\s))")
ANSWER_LINE = re.compile(
    r"^\s*(?:the\s+)?(?:answer|correct (?:answer|label|option|choice)|gold(?: label)?|expected (?:answer|label)|"
    r"final (?:answer|label))\s*[:=]", re.I | re.M)


def h(*parts) -> str:
    return hashlib.sha256(":".join([str(SEED), *map(str, parts)]).encode()).hexdigest()


def words(t: str) -> list[str]:
    return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).split()


def mentions(opt: str, text: str) -> bool:
    return re.search(r"(?<![A-Za-z0-9])" + re.escape(opt) + r"(?![A-Za-z0-9])", text, re.I) is not None


def text_key(r: dict) -> str:
    return json.dumps([r["state"], r["instructions"], r["options"], r.get("card")], ensure_ascii=False)


# ------------------------------------------------------------------------------------------------ loading
def load_domains():
    doms = {}
    for p in sorted(HARD.glob("*.jsonl")):
        if p.name.endswith((".blind.jsonl", ".solver.jsonl")):
            continue
        key = p.name[:-len(".jsonl")]
        agreed_p = HARD / f"{key}.agreed.json"
        if not agreed_p.exists():
            raise SystemExit(f"missing {agreed_p}")
        rows = [json.loads(l) for l in p.open() if l.strip()]
        solver_p = HARD / f"{key}.solver.jsonl"
        solver = {}
        if solver_p.exists():
            for l in solver_p.open():
                if l.strip():
                    s = json.loads(l)
                    solver[s["id"]] = s.get("answer")
        doms[key] = dict(rows=rows, agreed=set(json.load(agreed_p.open())), solver=solver)
    return doms


def same_answer(a, g) -> bool:
    return str(a).strip().lower() == str(g).strip().lower()


# ------------------------------------------------------------------------------------------------ checks
def schema_errors(r: dict, key: str) -> list[str]:
    e = []
    if set(r) != set(KEYS):
        e.append(f"keys:{sorted(set(r) ^ set(KEYS))}")
        return e
    for k in ["id", "group_id", "call_id", "track", "source", "state", "instructions", "role", "card"]:
        if not isinstance(r[k], str) or not r[k].strip():
            e.append(f"empty:{k}")
    if e:
        return e
    if not r["id"].startswith("r_") or not r["call_id"].startswith("c_") or not r["group_id"].startswith("g:"):
        e.append("id_prefix")
    if r["split"] not in ("train", "dev"):
        e.append("split")
    if not isinstance(r["meta"], dict) or r["meta"].get("domain") != key:
        e.append("meta.domain")
    lines = [l for l in r["card"].split("\n") if l.strip()]
    if not lines or any(not l.startswith("- ") or ": " not in l[2:] for l in lines):
        e.append("card_format")
    if r["qtype"] == "choice":
        o = r["options"]
        if r["role"] != "choice":
            e.append("role")
        if not isinstance(o, list) or not (2 <= len(o) <= 255) or any(not isinstance(x, str) or not x.strip() for x in o):
            e.append("options")
        elif len(set(o)) != len(o) or len({x.lower() for x in o}) != len(o):
            e.append("dup_options")
        elif r["gold"] not in o:
            e.append("gold_not_in_options")
        elif NONE in o and o[-1] != NONE:
            e.append("none_not_last")
    elif r["qtype"] == "noul":
        if r["options"] is not None:
            e.append("noul_options")
        if r["gold"] not in (0, 1) or isinstance(r["gold"], bool):
            e.append("noul_gold")
        if r["role"] not in ROLE_SIGN:
            e.append("role")
    else:
        e.append("qtype")
    return e


def claim_lines(r: dict) -> list[tuple[str, list[str]]]:
    """Lines of the state that attribute a label to someone (draft / suggested / logged ...), with the options named."""
    out = []
    if r["qtype"] != "choice":
        return out
    opts = [o for o in r["options"] if o != NONE]
    for line in r["state"].split("\n"):
        if not CUE.search(line) or RULE_LINE.search(line):
            continue
        named = [o for o in opts if mentions(o, line)]
        if named and len(named) < len(opts):
            out.append((line.strip(), named))
    return out


def trigram_sets(rows):
    sets = []
    for r in rows:
        w = words(r["state"] + " " + r["instructions"] + " " + " ".join(r["options"] or []))
        sets.append({" ".join(w[i:i + 3]) for i in range(max(1, len(w) - 2))})
    return sets


def overlap_matrix(rows):
    sets = trigram_sets(rows)
    voc, ri, ci = {}, [], []
    for i, s in enumerate(sets):
        for x in s:
            ri.append(i)
            ci.append(voc.setdefault(x, len(voc)))
    m = sp.csr_matrix((np.ones(len(ri), dtype=np.int32), (ri, ci)), shape=(len(sets), len(voc)))
    inter = (m @ m.T).toarray().astype(np.float64)
    size = np.array([len(s) for s in sets], dtype=np.float64)
    return inter / np.minimum(size[:, None], size[None, :])


def ngram_hits(rows) -> dict[str, list[str]]:
    """id -> list of '<ref file>:<ref source>:<field>' for every shared 12-word run."""
    grams = defaultdict(set)
    for r in rows:
        for fld in ("state", "instructions", "options", "card"):
            v = r.get(fld)
            w = words(" ".join(v) if isinstance(v, list) else v)
            for i in range(len(w) - NGRAM + 1):
                grams[" ".join(w[i:i + NGRAM])].add(r["id"])
    hits = defaultdict(set)
    for ref in REFS:
        with ref.open() as f:
            for l in f:
                x = json.loads(l)
                for fld in ("state", "instructions", "options", "card"):
                    v = x.get(fld)
                    w = words(" ".join(v) if isinstance(v, list) else (v if isinstance(v, str) else ""))
                    for i in range(len(w) - NGRAM + 1):
                        g = " ".join(w[i:i + NGRAM])
                        if g in grams:
                            for rid in grams[g]:
                                hits[rid].add(f"{ref.name}:{x.get('source')}:{fld}")
    return {k: sorted(v) for k, v in hits.items()}


def outside_ids():
    """ids and call_ids used by train_v07 and the other v11 parts (call_id -> text key where cheap)."""
    ids, cids = set(), set()
    files = [DATA / "train_v07.jsonl", DATA / "train_2b_kd.jsonl"] + [p for p in sorted(V11.glob("*.jsonl"))
                                           if "relations" not in p.name and p.name != "taskbank_rows_raw.jsonl"]
    pat_id = re.compile(r'"id":\s*"([^"]+)"')
    pat_cid = re.compile(r'"call_id":\s*"([^"]+)"')
    for p in files:
        with p.open() as f:
            for l in f:
                m = pat_id.search(l)
                if m:
                    ids.add(m.group(1))
                m = pat_cid.search(l)
                if m:
                    cids.add(m.group(1))
    return ids, cids


# ------------------------------------------------------------------------------------------------ main
def main():
    doms = load_domains()
    drop = defaultdict(list)  # id -> reasons
    all_rows, dom_of = [], {}
    report = {}
    for key, d in doms.items():
        rows = d["rows"]
        ids = [r["id"] for r in rows]
        solved = [i for i in ids if i in d["solver"]]
        agree_before = sum(same_answer(d["solver"][i], r["gold"]) for r, i in zip(rows, ids) if i in d["solver"])
        report[key] = dict(
            n_items=len(rows),
            agreement_before_review=f"{agree_before}/{len(solved)} ({agree_before / max(1, len(solved)):.3f})",
            n_agreed_after_review=len(d["agreed"] & set(ids)),
        )
        for r in rows:
            dom_of[r["id"]] = key
            if r["id"] not in d["agreed"]:
                drop[r["id"]].append("not_agreed")
        all_rows.extend(rows)
    byid = {}
    for r in all_rows:
        if r["id"] in byid:
            drop[r["id"]].append("duplicate_id")
        byid[r["id"]] = r

    # schema
    for r in all_rows:
        for e in schema_errors(r, dom_of[r["id"]]):
            drop[r["id"]].append(f"schema:{e}")
    for r in all_rows:
        tw = r["meta"].get("twin_of") if isinstance(r.get("meta"), dict) else None
        if tw is not None:
            b = byid.get(tw)
            if b is None:
                drop[r["id"]].append("schema:twin_base_missing")
            elif b["group_id"] != r["group_id"]:
                drop[r["id"]].append("schema:twin_other_group")
            elif b["gold"] == r["gold"]:
                drop[r["id"]].append("schema:twin_same_gold")
    cid_text = {}
    for r in all_rows:
        t = text_key(r)
        if r["call_id"] in cid_text and cid_text[r["call_id"]] != t:
            drop[r["id"]].append("schema:call_id_reused_for_other_text")
        cid_text.setdefault(r["call_id"], t)
    text_cid = defaultdict(set)
    for r in all_rows:
        text_cid[text_key(r)].add(r["call_id"])
    for r in all_rows:
        if len(text_cid[text_key(r)]) > 1:
            drop[r["id"]].append("schema:same_text_two_call_ids")
    o_ids, o_cids = outside_ids()
    for r in all_rows:
        if r["id"] in o_ids:
            drop[r["id"]].append("schema:id_clash_outside")
        if r["call_id"] in o_cids:
            drop[r["id"]].append("schema:call_id_clash_outside")

    # gold leakage
    leak_log = []
    claim_stats = defaultdict(Counter)
    for r in all_rows:
        key = dom_of[r["id"]]
        if ANSWER_LINE.search(r["state"]):
            drop[r["id"]].append("leak:answer_line")
            leak_log.append(dict(id=r["id"], kind="answer_line", verdict="dropped"))
        for line, named in claim_lines(r):
            if r["gold"] not in named:
                claim_stats[key]["claim_names_distractor"] += 1
                continue
            claim_stats[key]["claim_names_gold"] += 1
            sib = [x for x in all_rows if x["group_id"] == r["group_id"] and x["id"] != r["id"]
                   and line in x["state"] and x["gold"] != r["gold"]]
            if sib:
                verdict = f"kept: twin {sib[0]['id']} repeats the claim with gold '{sib[0]['gold']}'"
            elif r["id"] in CLAIM_REVIEWED:
                verdict = "kept: reviewed, " + CLAIM_REVIEWED[r["id"]]
            else:
                verdict = "dropped"
                drop[r["id"]].append("leak:gold_claimed_in_state")
            leak_log.append(dict(id=r["id"], kind="gold_claim", gold=r["gold"], line=line[:200], verdict=verdict))

    # near-duplicates (all items, across groups) and families for the split
    ov = overlap_matrix(all_rows)
    n = len(all_rows)
    gid = np.array([r["group_id"] for r in all_rows])
    cross = gid[:, None] != gid[None, :]
    iu = np.triu_indices(n, 1)
    cross_ov = np.where(cross[iu], ov[iu], 0.0)
    near = []
    for k in np.nonzero(cross_ov > NEAR_DUP)[0]:
        a, b = all_rows[iu[0][k]], all_rows[iu[1][k]]
        loser = max(a["id"], b["id"])
        drop[loser].append(f"near_duplicate:{min(a['id'], b['id'])}:{cross_ov[k]:.3f}")
        near.append(dict(a=a["id"], b=b["id"], overlap=round(float(cross_ov[k]), 3)))
    rowmax = np.where(cross, ov, 0.0).max(axis=1)
    max_cross = defaultdict(float)
    for i, r in enumerate(all_rows):
        max_cross[dom_of[r["id"]]] = max(max_cross[dom_of[r["id"]]], float(rowmax[i]))

    # 12-gram contamination
    hits = ngram_hits(all_rows)
    for rid, where in hits.items():
        drop[rid].append("ngram12:" + ",".join(where[:3]))

    # twin closure: base and twin are all-or-nothing
    changed = True
    while changed:
        changed = False
        for r in all_rows:
            tw = r["meta"].get("twin_of")
            if tw is None or tw not in byid:
                continue
            for x, y in ((r["id"], tw), (tw, r["id"])):
                if drop.get(x) and not drop.get(y):
                    drop[y].append(f"twin_partner_dropped:{x}")
                    changed = True

    kept = [r for r in all_rows if not drop.get(r["id"])]
    kept_idx = [i for i, r in enumerate(all_rows) if not drop.get(r["id"])]

    # families: same group, or cross-group overlap > FAMILY_LINK, within a domain
    parent = {r["group_id"]: r["group_id"] for r in kept}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    kset = set(kept_idx)
    for k in np.nonzero(cross_ov > FAMILY_LINK)[0]:
        i, j = iu[0][k], iu[1][k]
        if i in kset and j in kset and dom_of[all_rows[i]["id"]] == dom_of[all_rows[j]["id"]]:
            parent[find(all_rows[i]["group_id"])] = find(all_rows[j]["group_id"])
    split_of = {}
    fam_report = {}
    for key in doms:
        groups = sorted({r["group_id"] for r in kept if dom_of[r["id"]] == key})
        fams = defaultdict(list)
        for g in groups:
            fams[find(g)].append(g)
        target = round(DEV_FRAC * len(groups))
        order = sorted(fams.values(), key=lambda gs: h("hard_dev", key, min(gs)))
        dev_groups = []
        for gs in order:
            if len(dev_groups) >= target:
                break
            if len(dev_groups) + len(gs) <= target:
                dev_groups.extend(gs)
        for g in groups:
            split_of[g] = "dev" if g in set(dev_groups) else "train"
        fam_report[key] = dict(groups=len(groups), families=len(fams), largest_family=max(map(len, fams.values())),
                               dev_groups=len(dev_groups), dev_target=target)

    out_rows = []
    for r in sorted(kept, key=lambda x: (dom_of[x["id"]], int(re.sub(r"\D", "", x["id"].rsplit("_", 1)[-1]) or 0))):
        r = {k: r[k] for k in KEYS}
        r["split"] = split_of[r["group_id"]]
        out_rows.append(r)
    train = [r for r in out_rows if r["split"] == "train"]
    dev = [r for r in out_rows if r["split"] == "dev"]
    assert not ({r["group_id"] for r in train} & {r["group_id"] for r in dev})

    # cross-split overlap after the split (information)
    pos = {r["id"]: i for i, r in enumerate(all_rows)}
    tr_i = np.array([pos[r["id"]] for r in train])
    dv_i = np.array([pos[r["id"]] for r in dev])
    max_train_dev = float(ov[np.ix_(dv_i, tr_i)].max()) if len(dv_i) and len(tr_i) else 0.0

    # relations
    rels = {"train": [], "dev": []}
    rel_errors = []
    for part, rows in (("train", train), ("dev", dev)):
        byg = defaultdict(list)
        for r in rows:
            if r["qtype"] == "noul":
                byg[r["group_id"]].append(r)
        for g, rs in byg.items():
            for i in range(len(rs)):
                for j in range(i + 1, len(rs)):
                    a, b = rs[i], rs[j]
                    if a["meta"].get("twin_of") == b["id"] or b["meta"].get("twin_of") == a["id"]:
                        continue
                    if a["state"] != b["state"] or a["card"] != b["card"]:
                        continue
                    sa, sb = ROLE_SIGN[a["role"]], ROLE_SIGN[b["role"]]
                    if sa == sb and a["gold"] == b["gold"]:
                        typ = "equiv"
                    elif sa != sb and a["gold"] + b["gold"] == 1:
                        typ = "complement"
                    else:
                        rel_errors.append((a["id"], b["id"]))
                        continue
                    rels[part].append({"type": typ, "a": a["id"], "b": b["id"], "track": part})

    # balance
    def balance(rows):
        ch = [r for r in rows if r["qtype"] == "choice"]
        nu = [r for r in rows if r["qtype"] == "noul"]
        relpos = Counter()
        longest = expected = 0.0
        for r in ch:
            o = r["options"]
            p = o.index(r["gold"]) / max(1, len(o) - 1)
            relpos["first" if p == 0 else "last" if p == 1 else "middle"] += 1
            if r["gold"] != NONE:
                oo = [x for x in o if x != NONE]
                ls = sorted(len(x) for x in oo)
                if len(oo) > 1 and ls[-1] > ls[-2]:
                    expected += 1 / len(oo)
                    longest += len(r["gold"]) == ls[-1]
        sets = defaultdict(list)
        for r in ch:
            sets[tuple(sorted(r["options"]))].append(r["gold"])
        loo_n = loo_hit = 0
        loo_chance = 0.0
        for opts, golds in sets.items():
            if len(golds) < 3:
                continue
            c = Counter(golds)
            for g in golds:
                c[g] -= 1
                guess = max(sorted(c), key=lambda x: c[x])
                loo_hit += guess == g
                loo_n += 1
                loo_chance += 1 / len(opts)
                c[g] += 1
        neg = [r for r in nu if r["role"] == "neg"]
        return dict(
            n=len(rows), choice=len(ch), noul=len(nu),
            yes_rate=round(sum(r["gold"] for r in nu) / max(1, len(nu)), 3),
            neg_items=len(neg), neg_yes=sum(r["gold"] for r in neg),
            none_gold_rate=round(sum(r["gold"] == NONE for r in ch) / max(1, len(ch)), 3),
            gold_position=dict(relpos),
            options_min_max=[min((len(r["options"]) for r in ch), default=0), max((len(r["options"]) for r in ch), default=0)],
            gold_is_unique_longest=f"{int(longest)} vs {expected:.1f} expected",
            option_set_majority_guess=f"{loo_hit}/{loo_n} vs chance {loo_chance:.1f}" if loo_n else "no repeated option sets",
            difficulty=dict(sorted(Counter(r["meta"].get("difficulty") for r in rows).items())),
            twins=sum("twin_of" in r["meta"] for r in rows),
        )

    for key in doms:
        rows_k = [r for r in out_rows if dom_of[r["id"]] == key]
        dropped_k = {i: v for i, v in drop.items() if v and dom_of.get(i) == key}
        rep = report[key]
        rep.update(
            kept=len(rows_k), kept_train=sum(r["split"] == "train" for r in rows_k),
            kept_dev=sum(r["split"] == "dev" for r in rows_k),
            dropped={i: v for i, v in sorted(dropped_k.items())},
            balance=balance(rows_k),
            split_families=fam_report[key],
            claims_in_state=dict(claim_stats[key]),
            max_cross_group_overlap=round(max_cross.get(key, 0.0), 3),
        )
        if key in OHS_FAMILY_NOTE:
            rep["heldout_family_overlap"] = OHS_FAMILY_NOTE[key]

    PARTS.mkdir(parents=True, exist_ok=True)

    def dump(name, rows):
        with (PARTS / name).open("w") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

    dump("hard12_train.jsonl", train)
    dump("hard12_dev.jsonl", dev)
    dump("hard12_relations.jsonl", rels["train"])
    dump("hard12_dev_relations.jsonl", rels["dev"])
    dump("hard12_dropped.jsonl", [dict(id=i, domain=dom_of.get(i), reasons=v) for i, v in sorted(drop.items()) if v])

    summary = dict(
        seed=SEED, dev_frac=DEV_FRAC, near_dup_threshold=NEAR_DUP, family_link_threshold=FAMILY_LINK, ngram=NGRAM,
        refs=[str(p) for p in REFS],
        totals=dict(input=len(all_rows), kept=len(out_rows), train=len(train), dev=len(dev),
                    dropped=sum(1 for v in drop.values() if v),
                    relations_train=dict(Counter(x["type"] for x in rels["train"])),
                    relations_dev=dict(Counter(x["type"] for x in rels["dev"])),
                    relation_errors=rel_errors,
                    near_duplicates_over_threshold=near,
                    ngram12_hits=hits,
                    max_train_dev_overlap=round(max_train_dev, 3)),
        leak_review=leak_log,
        domains=report,
    )
    (PARTS / "hard12_summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False))

    print(f"input {len(all_rows)}  kept {len(out_rows)}  train {len(train)}  dev {len(dev)}  "
          f"relations train {len(rels['train'])} dev {len(rels['dev'])}")
    print(f"near-dups>{NEAR_DUP}: {len(near)}  12-gram hits: {len(hits)}  max train-dev overlap {max_train_dev:.3f}")
    for key, rep in report.items():
        b = rep["balance"]
        print(f"{key:18s} in {rep['n_items']:3d} agree {rep['agreement_before_review']:>16s} "
              f"agreed {rep['n_agreed_after_review']:3d} kept {rep['kept']:3d} (train {rep['kept_train']}, dev "
              f"{rep['kept_dev']}) yes {b['yes_rate']:.2f} none {b['none_gold_rate']:.2f} "
              f"setguess {b['option_set_majority_guess']} dropped {list(rep['dropped'])}")
    for x in leak_log:
        print("leak-check", x["id"], x["kind"], x["verdict"][:90])


if __name__ == "__main__":
    main()
