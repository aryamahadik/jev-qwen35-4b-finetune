"""Build + validate data/v11_parts/hard/clinical.jsonl (and clinical.blind.jsonl).

Deterministic, CPU only, no external calls. Items are hand-written in items_*.py (Claude as teacher).
Seed 20261001 is recorded for reproducibility; option lists keep their authored (protocol) order, because
several items depend on list order ("first criterion in listed order", "pathway listed first").
Run:  .venv/bin/python lean/hard_src/clinical/build.py
"""
import collections
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import importlib  # noqa: E402

MODULES = ["items_onc", "items_trials", "items_p1s", "items_preauth", "items_benefits", "items_triage"]

SEED = 20261001
DOMAIN = "clinical"
OUT_DIR = os.path.abspath(os.path.join(HERE, "..", "..", "data", "v11_parts", "hard"))
OUT = os.path.join(OUT_DIR, f"{DOMAIN}.jsonl")
OUT_BLIND = os.path.join(OUT_DIR, f"{DOMAIN}.blind.jsonl")


def load_items():
    items = []
    for m in MODULES:
        try:
            mod = importlib.import_module(m)
        except ModuleNotFoundError as e:
            if e.name == m:
                print(f"(module {m} not written yet)")
                continue
            raise
        items += mod.ITEMS
    return items


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


def make_row(n, gidx, it, state, gold, instr, twin_of=None):
    meta = {"domain": DOMAIN, "difficulty": it["diff"]}
    if twin_of:
        meta["twin_of"] = twin_of
    return {
        "id": f"r_hard_{DOMAIN}_{n}",
        "group_id": f"g:hard_{DOMAIN}:{gidx:03d}",
        "call_id": call_id(instr, state, it["options"], it["card"]),
        "split": "train",
        "track": "HARD",
        "source": f"hard_{DOMAIN}",
        "state": state,
        "qtype": it["qtype"],
        "instructions": instr,
        "options": it["options"],
        "gold": gold,
        "role": it["role"],
        "card": it["card"],
        "meta": meta,
    }


def build(items):
    rows, n = [], 0
    for gidx, it in enumerate(items, 1):
        n += 1
        base = make_row(n, gidx, it, it["state"], it["gold"], it["q"])
        rows.append(base)
        tw = it["twin"]
        if tw:
            n += 1
            rows.append(make_row(n, gidx, it, apply_subs(it["state"], tw["subs"]), tw["gold"],
                                 tw["q"] or it["q"], twin_of=base["id"]))
    return rows


REQ = {"id", "group_id", "call_id", "split", "track", "source", "state", "qtype", "instructions",
       "options", "gold", "role", "card", "meta"}


def validate(rows):
    errs = []
    ids = [r["id"] for r in rows]
    if len(set(ids)) != len(ids):
        errs.append("duplicate ids")
    for c, k in collections.Counter(r["call_id"] for r in rows).items():
        if k > 1:
            errs.append(f"duplicate call_id {c}")
    byid = {r["id"]: r for r in rows}
    for r in rows:
        rid = r["id"]
        if set(r) != REQ:
            errs.append(f"{rid}: keys {sorted(set(r) ^ REQ)}")
        if r["split"] != "train" or r["track"] != "HARD" or r["source"] != f"hard_{DOMAIN}":
            errs.append(f"{rid}: split/track/source")
        w = words(r["state"])
        if not 80 <= w <= 450:
            errs.append(f"{rid}: state words {w}")
        lines = r["card"].split("\n") if r["card"] else []
        if not lines or not all(l.startswith("- ") and ": " in l for l in lines):
            errs.append(f"{rid}: bad card")
        m = r["meta"]
        if m.get("domain") != DOMAIN or m.get("difficulty") not in (1, 2, 3):
            errs.append(f"{rid}: meta")
        if r["qtype"] == "choice":
            o = r["options"]
            if not isinstance(o, list) or not 3 <= len(o) <= 28 or len(set(o)) != len(o):
                errs.append(f"{rid}: options {o}")
            elif r["gold"] not in o:
                errs.append(f"{rid}: gold not in options")
            else:
                heads = [l[2:].split(": ", 1)[0] for l in lines]
                if heads != o:
                    errs.append(f"{rid}: card lines do not match options one-to-one")
                if any(": " in x for x in o):
                    errs.append(f"{rid}: option label contains ': '")
            if r["role"] != "choice":
                errs.append(f"{rid}: role")
        elif r["qtype"] == "noul":
            if r["options"] is not None or r["gold"] not in (0, 1):
                errs.append(f"{rid}: noul fields")
        else:
            errs.append(f"{rid}: qtype")
        if "twin_of" in m:
            b = byid.get(m["twin_of"])
            if b is None or b["group_id"] != r["group_id"] or b["call_id"] == r["call_id"] or b["gold"] == r["gold"]:
                errs.append(f"{rid}: twin relation broken")
            elif "twin_of" in b["meta"]:
                errs.append(f"{rid}: twin of a twin")
        # crude leakage check: a choice gold label (other than generic ones) should not be quoted in the state
        if r["qtype"] == "choice" and r["gold"] != "none of these" and len(r["gold"]) > 8:
            if r["gold"].lower() in r["state"].lower():
                errs.append(f"{rid}: gold label appears verbatim in state ({r['gold']})")
    return errs


def report(rows):
    base = [r for r in rows if "twin_of" not in r["meta"]]
    twins = [r for r in rows if "twin_of" in r["meta"]]
    out = collections.OrderedDict()
    out["rows"] = len(rows)
    out["base_items"] = len(base)
    out["twins"] = len(twins)
    out["twin_rate"] = round(len(twins) / max(1, len(base)), 3)
    out["base_by_qtype"] = dict(collections.Counter(r["qtype"] for r in base))
    out["rows_by_qtype"] = dict(collections.Counter(r["qtype"] for r in rows))
    yn = [r for r in rows if r["qtype"] == "noul"]
    out["yesno_gold"] = dict(collections.Counter("yes" if r["gold"] == 1 else "no" for r in yn))
    ch = [r for r in rows if r["qtype"] == "choice"]
    gc = collections.Counter(r["gold"] for r in ch)
    out["choice_top_golds"] = gc.most_common(6)
    out["choice_max_gold_share"] = round(gc.most_common(1)[0][1] / len(ch), 3) if ch else 0
    pos = collections.Counter(r["options"].index(r["gold"]) for r in ch)
    out["choice_gold_position"] = dict(sorted(pos.items()))
    out["option_count_hist"] = dict(sorted(collections.Counter(len(r["options"]) for r in ch).items()))
    out["difficulty"] = dict(sorted(collections.Counter(r["meta"]["difficulty"] for r in base).items()))
    out["distinct_questions"] = {
        "noul": len({r["instructions"] for r in yn}), "choice": len({r["instructions"] for r in ch})}
    wc = [words(r["state"]) for r in rows]
    out["state_words_min_mean_max"] = [min(wc), round(sum(wc) / len(wc)), max(wc)]
    return out


def main():
    items = load_items()
    rows = build(items)
    errs = validate(rows)
    for e in errs:
        print("ERR", e)
    rep = report(rows)
    print(json.dumps(rep, indent=1, ensure_ascii=False))
    if errs:
        sys.exit(1)
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(OUT_BLIND, "w", encoding="utf-8") as f:
        for r in rows:
            b = {k: v for k, v in r.items() if k != "gold"}
            f.write(json.dumps(b, ensure_ascii=False) + "\n")
    print("wrote", OUT, "and", OUT_BLIND)


if __name__ == "__main__":
    main()
