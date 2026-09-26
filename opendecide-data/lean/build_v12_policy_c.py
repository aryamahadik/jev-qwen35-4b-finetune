"""Build the v0.12 HARD 'policy_c' item set (policy enforcement on concrete cases).

Items are hand-written (Claude as teacher) in hard_src_v12/policy_c/*.py. This script
assembles rows, applies minimal-pair twins, shuffles option order deterministically
(seed 20261001; ordered scales keep their order; 'none of these' stays last),
validates, and writes:
  data/v12_parts/hard/policy_c.jsonl        (with gold)
  data/v12_parts/hard/policy_c.blind.jsonl  (identical rows, gold removed)
Re-runnable and deterministic. No external APIs.
"""
import hashlib
import json
import random
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "hard_src_v12" / "policy_c"))

import forum, housing, school, workplace, desk  # noqa: E402

SEED = 20261001
OUT = HERE / "data" / "v12_parts" / "hard"
SRC = "hard_policy_c"
LAST = {"none of these"}


def cid(instr, state, options):
    h = hashlib.sha1(json.dumps([instr, state, options], ensure_ascii=False).encode()).hexdigest()
    return "c_" + h[:12]


def card_text(pairs):
    return "\n".join(f"- {a}: {b}" for a, b in pairs)


def apply_edits(state, edits):
    s = state
    for old, new in edits:
        n = s.count(old)
        assert n == 1, f"edit target must occur exactly once (found {n}): {old[:60]!r}"
        s = s.replace(old, new)
    return s


def build():
    items = forum.ITEMS + housing.ITEMS + school.ITEMS + workplace.ITEMS + desk.ITEMS
    keys = [it["key"] for it in items]
    assert len(keys) == len(set(keys)), "duplicate item keys"
    rows, n = [], 0
    for it in items:
        gid = f"g:{SRC}:{it['key']}"
        if it["qtype"] == "choice":
            opts = list(it["options"])
            if not it["ordered"]:
                rng = random.Random(f"{SEED}:{it['key']}")
                head = [o for o in opts if o[0] not in LAST]
                tail = [o for o in opts if o[0] in LAST]
                rng.shuffle(head)
                opts = head + tail
            options = [o[0] for o in opts]
            card = card_text(opts)
        else:
            options, card = None, card_text(it["card"])
        n += 1
        base_id = f"r_{SRC}_{n}"
        base = {
            "id": base_id, "group_id": gid,
            "call_id": cid(it["instructions"], it["state"], options),
            "split": "train", "track": "HARD", "source": SRC,
            "state": it["state"], "qtype": it["qtype"],
            "instructions": it["instructions"], "options": options,
            "gold": it["gold"], "role": it["role"], "card": card,
            "meta": {"domain": "policy_c", "difficulty": it["difficulty"]},
        }
        rows.append(base)
        tw = it.get("twin")
        if tw:
            st = apply_edits(it["state"], tw["edits"])
            ins = tw["instructions"] or it["instructions"]
            n += 1
            rows.append({**base,
                         "id": f"r_{SRC}_{n}", "call_id": cid(ins, st, options),
                         "state": st, "instructions": ins, "gold": tw["gold"],
                         "meta": {"domain": "policy_c", "twin_of": base_id,
                                  "difficulty": it["difficulty"]}})
    return rows


def validate(rows):
    errs = []
    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        errs.append("duplicate ids")
    byid = {r["id"]: r for r in rows}
    text2cid = {}
    for r in rows:
        k = json.dumps([r["instructions"], r["state"], r["options"]], ensure_ascii=False)
        if k in text2cid and text2cid[k] != r["call_id"]:
            errs.append(f"{r['id']}: same text, different call_id")
        text2cid.setdefault(k, r["call_id"])
    if len(set(text2cid.values())) != len(text2cid):
        errs.append("call_id collision across different texts")
    need = {"id", "group_id", "call_id", "split", "track", "source", "state", "qtype",
            "instructions", "options", "gold", "role", "card", "meta"}
    for r in rows:
        rid = r["id"]
        if set(r) != need:
            errs.append(f"{rid}: keys {sorted(set(r) ^ need)}")
        if r["split"] != "train" or r["track"] != "HARD" or r["source"] != SRC:
            errs.append(f"{rid}: split/track/source")
        wc = len(r["state"].split())
        if not 80 <= wc <= 450:
            errs.append(f"{rid}: state words {wc}")
        m = r["meta"]
        if m.get("domain") != "policy_c" or m.get("difficulty") not in (1, 2, 3):
            errs.append(f"{rid}: meta")
        if set(m) - {"domain", "difficulty", "twin_of"}:
            errs.append(f"{rid}: extra meta keys")
        if not r["card"] or any(not ln.startswith("- ") or ": " not in ln for ln in r["card"].split("\n")):
            errs.append(f"{rid}: card format")
        if r["qtype"] == "choice":
            o = r["options"]
            if r["role"] != "choice":
                errs.append(f"{rid}: role")
            if not (isinstance(o, list) and 3 <= len(o) <= 28 and len(set(o)) == len(o)):
                errs.append(f"{rid}: options {len(o) if o else o}")
            elif r["gold"] not in o:
                errs.append(f"{rid}: gold not in options")
            names = [ln[2:].split(": ", 1)[0] for ln in r["card"].split("\n")]
            if names != o:
                errs.append(f"{rid}: card/options mismatch")
            if "none of these" in o and o[-1] != "none of these":
                errs.append(f"{rid}: none-of-these not last")
        elif r["qtype"] == "noul":
            if r["options"] is not None or r["gold"] not in (0, 1) or isinstance(r["gold"], bool):
                errs.append(f"{rid}: noul fields")
            if r["role"] not in ("aff", "neg"):
                errs.append(f"{rid}: role")
        else:
            errs.append(f"{rid}: qtype")
        if "twin_of" in m:
            b = byid.get(m["twin_of"])
            if not b or b["group_id"] != r["group_id"] or b["gold"] == r["gold"] \
                    or b["call_id"] == r["call_id"] or "twin_of" in b["meta"]:
                errs.append(f"{rid}: bad twin")
    # balance and variety
    for qt in ("choice", "noul"):
        rs = [r for r in rows if r["qtype"] == qt]
        if qt == "choice":
            top, c = Counter(r["gold"] for r in rs).most_common(1)[0]
            if c / len(rs) > 0.40:
                errs.append(f"choice gold '{top}' share {c/len(rs):.2f}")
            pos = Counter(r["options"].index(r["gold"]) for r in rs)
            if pos.most_common(1)[0][1] / len(rs) > 0.40:
                errs.append(f"choice gold position skew {pos}")
        else:
            y = sum(r["gold"] for r in rs) / len(rs)
            if not 0.40 <= y <= 0.60:
                errs.append(f"noul yes share {y:.2f}")
        if len({r["instructions"] for r in rs}) < 6:
            errs.append(f"{qt}: fewer than 6 phrasings")
    return errs


def main():
    rows = build()
    errs = validate(rows)
    if errs:
        print("VALIDATION FAILED:")
        for e in errs:
            print("  ", e)
        sys.exit(1)
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "policy_c.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(OUT / "policy_c.blind.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps({k: v for k, v in r.items() if k != "gold"}, ensure_ascii=False) + "\n")
    base = [r for r in rows if "twin_of" not in r["meta"]]
    twins = [r for r in rows if "twin_of" in r["meta"]]
    ch = [r for r in rows if r["qtype"] == "choice"]
    nl = [r for r in rows if r["qtype"] == "noul"]
    summ = {
        "rows": len(rows), "base_items": len(base), "twins": len(twins),
        "twin_rate": round(len(twins) / len(base), 3),
        "base_noul": sum(r["qtype"] == "noul" for r in base),
        "base_choice": sum(r["qtype"] == "choice" for r in base),
        "rows_noul": len(nl), "rows_choice": len(ch),
        "noul_yes": sum(r["gold"] for r in nl), "noul_no": sum(1 - r["gold"] for r in nl),
        "option_count_hist_rows": dict(sorted(Counter(len(r["options"]) for r in ch).items())),
        "option_count_hist_base": dict(sorted(Counter(len(r["options"]) for r in base if r["qtype"] == "choice").items())),
        "choice_gold_top": Counter(r["gold"] for r in ch).most_common(3),
        "choice_gold_position": dict(sorted(Counter(r["options"].index(r["gold"]) for r in ch).items())),
        "difficulty": dict(sorted(Counter(r["meta"]["difficulty"] for r in base).items())),
        "distinct_instructions": {qt: len({r["instructions"] for r in rows if r["qtype"] == qt}) for qt in ("choice", "noul")},
        "state_words": [min(len(r["state"].split()) for r in rows), max(len(r["state"].split()) for r in rows)],
    }
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    main()
