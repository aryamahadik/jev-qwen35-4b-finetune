"""Build + validate data/v11_parts/hard/policy_a.jsonl (and .blind.jsonl).

Deterministic, CPU only, no external calls. Items are hand-written in items*.py
(Claude as teacher). Seed 20261001 is used only for the optional option shuffle.
Run:  .venv/bin/python lean/hard_src/policy_a/build.py
"""
import collections
import hashlib
import json
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import items1, items2, items3, items4, items5, items6  # noqa: E402

SEED = 20261001
DOMAIN = "policy_a"
OUT_DIR = os.path.abspath(os.path.join(HERE, "..", "..", "data", "v11_parts", "hard"))
OUT = os.path.join(OUT_DIR, f"{DOMAIN}.jsonl")
OUT_BLIND = os.path.join(OUT_DIR, f"{DOMAIN}.blind.jsonl")

ITEMS = items1.ITEMS + items2.ITEMS + items3.ITEMS + items4.ITEMS + items5.ITEMS + items6.ITEMS


def words(s):
    return len(re.findall(r"\S+", s))


def call_id(instr, state, options, card):
    blob = json.dumps([instr, state, options, card], ensure_ascii=False, sort_keys=True)
    return "c_" + hashlib.sha1(blob.encode("utf-8")).hexdigest()[:12]


def apply_subs(state, subs):
    for old, new in subs:
        n = state.count(old)
        assert n == 1, f"twin substring occurs {n} times: {old[:60]!r}"
        state = state.replace(old, new)
    return state


def make_row(n, gidx, it, state, gold, instr, options, twin_of=None):
    meta = {"domain": DOMAIN, "difficulty": it["diff"]}
    if twin_of:
        meta["twin_of"] = twin_of
    row = {
        "id": f"r_hard_{DOMAIN}_{n}",
        "group_id": f"g:hard_{DOMAIN}:{gidx:03d}",
        "call_id": call_id(instr, state, options, it["card"]),
        "split": "train",
        "track": "HARD",
        "source": f"hard_{DOMAIN}",
        "state": state,
        "qtype": it["qtype"],
        "instructions": instr,
        "options": options,
        "gold": gold,
        "role": it["role"],
        "card": it["card"],
        "meta": meta,
    }
    return row


def build():
    rows = []
    n = 0
    for gidx, it in enumerate(ITEMS, 1):
        options = it["options"]
        if options is not None and it.get("shuffle"):
            rng = random.Random(SEED * 1000 + gidx)
            head = [o for o in options if o != "none of these"]
            rng.shuffle(head)
            options = head + (["none of these"] if "none of these" in options else [])
        n += 1
        base = make_row(n, gidx, it, it["state"], it["gold"], it["q"], options)
        rows.append(base)
        if it["twin"]:
            subs, tgold = it["twin"][0], it["twin"][1]
            tq = it["twin"][2] if len(it["twin"]) > 2 else it["q"]
            n += 1
            rows.append(make_row(n, gidx, it, apply_subs(it["state"], subs), tgold, tq, options,
                                 twin_of=base["id"]))
    return rows


REQ = {"id", "group_id", "call_id", "split", "track", "source", "state", "qtype", "instructions",
       "options", "gold", "role", "card", "meta"}


def validate(rows):
    errs = []
    ids = [r["id"] for r in rows]
    if len(set(ids)) != len(ids):
        errs.append("duplicate ids")
    cids = collections.Counter(r["call_id"] for r in rows)
    for c, k in cids.items():
        if k > 1:
            errs.append(f"duplicate call_id {c}")
    byid = {r["id"]: r for r in rows}
    for r in rows:
        if set(r) != REQ:
            errs.append(f"{r['id']}: keys {sorted(set(r) ^ REQ)}")
        if r["split"] != "train" or r["track"] != "HARD" or r["source"] != f"hard_{DOMAIN}":
            errs.append(f"{r['id']}: split/track/source")
        w = words(r["state"])
        if not 80 <= w <= 450:
            errs.append(f"{r['id']}: state words {w}")
        if not r["card"] or not all(l.startswith("- ") and ": " in l for l in r["card"].split("\n")):
            errs.append(f"{r['id']}: bad card")
        m = r["meta"]
        if m.get("domain") != DOMAIN or m.get("difficulty") not in (1, 2, 3):
            errs.append(f"{r['id']}: meta")
        if r["qtype"] == "choice":
            o = r["options"]
            if not isinstance(o, list) or not 3 <= len(o) <= 28 or len(set(o)) != len(o):
                errs.append(f"{r['id']}: options {o}")
            if r["gold"] not in o:
                errs.append(f"{r['id']}: gold not in options")
            if r["role"] != "choice":
                errs.append(f"{r['id']}: role")
            card_opts = [l[2:].split(": ", 1)[0] for l in r["card"].split("\n")]
            missing = [x for x in o if x not in card_opts]
            if missing:
                errs.append(f"{r['id']}: options missing from card {missing}")
        elif r["qtype"] == "noul":
            if r["options"] is not None or r["gold"] not in (0, 1) or isinstance(r["gold"], bool):
                errs.append(f"{r['id']}: noul fields")
            if r["role"] not in ("aff", "neg"):
                errs.append(f"{r['id']}: role")
        else:
            errs.append(f"{r['id']}: qtype")
        if "twin_of" in m:
            b = byid.get(m["twin_of"])
            if b is None or b["group_id"] != r["group_id"] or b["gold"] == r["gold"] or b["call_id"] == r["call_id"]:
                errs.append(f"{r['id']}: twin linkage")
    return errs


def report(rows):
    base = [r for r in rows if "twin_of" not in r["meta"]]
    twins = [r for r in rows if "twin_of" in r["meta"]]
    out = {"rows": len(rows), "base_items": len(base), "twins": len(twins),
           "twin_share_of_base": round(len(twins) / len(base), 3)}
    for label, rs in (("base", base), ("all", rows)):
        out[f"qtype_{label}"] = dict(collections.Counter(r["qtype"] for r in rs))
    yn = [r for r in rows if r["qtype"] == "noul"]
    out["noul_gold"] = dict(collections.Counter(r["gold"] for r in yn))
    out["noul_roles"] = dict(collections.Counter(r["role"] for r in yn))
    ch = [r for r in rows if r["qtype"] == "choice"]
    g = collections.Counter(r["gold"] for r in ch)
    out["choice_gold_top"] = g.most_common(6)
    out["choice_gold_max_share"] = round(g.most_common(1)[0][1] / len(ch), 3)
    pos = collections.Counter(r["options"].index(r["gold"]) for r in ch)
    out["choice_gold_position"] = dict(sorted(pos.items()))
    out["option_count_hist"] = dict(sorted(collections.Counter(len(r["options"]) for r in ch).items()))
    out["option_count_hist_base"] = dict(sorted(collections.Counter(len(r["options"]) for r in base if r["qtype"] == "choice").items()))
    out["distinct_wordings"] = {q: len({r["instructions"] for r in rows if r["qtype"] == q}) for q in ("noul", "choice")}
    out["difficulty"] = dict(sorted(collections.Counter(r["meta"]["difficulty"] for r in base).items()))
    wc = [words(r["state"]) for r in rows]
    out["state_words"] = {"min": min(wc), "max": max(wc), "mean": round(sum(wc) / len(wc), 1)}
    return out


def main():
    rows = build()
    errs = validate(rows)
    rep = report(rows)
    if rep["choice_gold_max_share"] > 0.40:
        errs.append(f"choice gold imbalance {rep['choice_gold_max_share']}")
    yes = rep["noul_gold"].get(1, 0) / max(1, sum(rep["noul_gold"].values()))
    if not 0.40 <= yes <= 0.60:
        errs.append(f"noul gold imbalance {yes:.2f}")
    if min(rep["distinct_wordings"].values()) < 6:
        errs.append("fewer than 6 wordings for a question type")
    if errs:
        print("\n".join(errs))
        sys.exit(1)
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(OUT_BLIND, "w", encoding="utf-8") as f:
        for r in rows:
            b = {k: v for k, v in r.items() if k != "gold"}
            f.write(json.dumps(b, ensure_ascii=False) + "\n")
    print(json.dumps(rep, indent=1, ensure_ascii=False))
    print("wrote", OUT, "and", OUT_BLIND)


if __name__ == "__main__":
    main()
