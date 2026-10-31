"""Build + validate data/v11_parts/hard/nli_a.jsonl (and .blind.jsonl).

Deterministic, CPU only, no external calls. Items are hand-written in items*.py (Claude as teacher).
Seed 20261001 drives the per-item shuffles (statement order, three-way label order).
Every member of a minimal set (family F01..F28) and its twins share one group_id, because they are
variants of one underlying passage/statement pair.
Run:  .venv/bin/python lean/hard_src/nli_a/build.py
"""
import collections
import hashlib
import itertools
import json
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import items1, items2, items3, items4  # noqa: E402
from common import CARD_YN, L3, D3, FOLLOW, DEF_F  # noqa: E402

SEED = 20261001
DOMAIN = "nli_a"
OUT_DIR = os.path.abspath(os.path.join(HERE, "..", "..", "data", "v11_parts", "hard"))
OUT = os.path.join(OUT_DIR, f"{DOMAIN}.jsonl")
OUT_BLIND = os.path.join(OUT_DIR, f"{DOMAIN}.blind.jsonl")

ITEMS = items1.ITEMS + items2.ITEMS + items3.ITEMS + items4.ITEMS
NUMW = {3: "three", 4: "four", 5: "five"}
COUNTW = {0: "none of them", 1: "exactly one", 2: "exactly two", 3: "exactly three", 4: "exactly four"}


def words(s):
    return len(re.findall(r"\S+", s))


def call_id(instr, state, options, card):
    blob = json.dumps([instr, state, options, card], ensure_ascii=False, sort_keys=True)
    return "c_" + hashlib.sha1(blob.encode("utf-8")).hexdigest()[:12]


def apply_subs(text, subs, strict=True):
    for old, new in subs:
        n = text.count(old)
        if strict:
            assert n == 1, f"twin substring occurs {n} times: {old[:70]!r}"
        elif n > 1:
            raise AssertionError(f"card substring occurs {n} times: {old[:70]!r}")
        text = text.replace(old, new)
    return text


def count_label(k, n):
    return f"all {NUMW[n]}" if k == n and n > 1 else COUNTW[k]


def subset_label(s, n):
    s = sorted(s)
    if not s:
        return "none of them"
    if len(s) == n:
        return f"all {NUMW[n]}"
    if len(s) == 1:
        return f"{s[0]} only"
    return (", ".join(str(x) for x in s[:-1]) + f" and {s[-1]} only")


def subset_options(n):
    opts = []
    for r in range(0, n + 1):
        for comb in itertools.combinations(range(1, n + 1), r):
            opts.append((subset_label(comb, n), comb))
    return opts


def render(it, idx):
    """Return (state, options, card, gold_fn) where gold_fn maps a gold spec to the row gold."""
    rng = random.Random(SEED * 1000 + idx)
    k = it["kind"]
    if k == "yn":
        state = f"{it['passage']}\n\n{it['lab']}: {it['stmt']}"
        return state, None, CARD_YN, lambda g: g
    if k == "c3":
        order = list(L3.values())
        rng.shuffle(order)
        state = f"{it['passage']}\n\n{it['lab']}: {it['stmt']}"
        card = "\n".join(f"- {o}: {D3[o]}" for o in order)
        return state, order, card, lambda g: L3[g]
    if k in ("sc", "cnt", "sub"):
        n = len(it["stmts"])
        perm = list(range(n))
        rng.shuffle(perm)                      # perm[new_pos] = original index
        pos = {orig: p + 1 for p, orig in enumerate(perm)}  # original index -> new 1-based number
        shown = [it["stmts"][o] for o in perm]
        state = it["passage"] + "\n\n" + it["head"] + "\n" + "\n".join(f"{i}. {s}" for i, s in enumerate(shown, 1))
        head_line = f"- {FOLLOW}: {DEF_F}"
        if k == "sc":
            options = [f"statement {i}" for i in range(1, n + 1)] + ["none of these"]
            card = "\n".join([head_line] + [f"- statement {i}: \"{s}\"" for i, s in enumerate(shown, 1)]
                             + ["- none of these: none of the numbered statements follows from the passage."])
            return state, options, card, lambda g: "none of these" if g == 0 else f"statement {pos[g - 1]}"
        if k == "cnt":
            options = [count_label(c, n) for c in range(0, n + 1)]
            defs = []
            for c in range(0, n + 1):
                lab = count_label(c, n)
                if c == 0:
                    d = "no numbered statement follows from the passage."
                elif c == n:
                    d = "every numbered statement follows from the passage."
                else:
                    d = f"{c} of the {n} numbered statements follow from the passage and the rest do not."
                defs.append(f"- {lab}: {d}")
            card = "\n".join([head_line] + defs)
            return state, options, card, lambda g: count_label(g, n)
        opts = subset_options(n)
        options = [o for o, _ in opts]
        defs = []
        for lab, comb in opts:
            if not comb:
                d = "no numbered statement follows from the passage."
            elif len(comb) == n:
                d = "every numbered statement follows from the passage."
            else:
                rest = [x for x in range(1, n + 1) if x not in comb]
                a = ", ".join(str(x) for x in comb)
                b = ", ".join(str(x) for x in rest)
                d = (f"statement{'s' if len(comb) > 1 else ''} {a} follow{'' if len(comb) > 1 else 's'} from the "
                     f"passage and statement{'s' if len(rest) > 1 else ''} {b} do{'' if len(rest) > 1 else 'es'} not.")
            defs.append(f"- {lab}: {d}")
        card = "\n".join([head_line] + defs)
        return state, options, card, lambda g: subset_label(tuple(pos[x - 1] for x in g), n)
    if k == "ent":
        options = [o for o, _ in it["opts"]]
        lines = ([f"- {FOLLOW}: {DEF_F}"] if it["follow_line"] else []) + [f"- {o}: {d}" for o, d in it["opts"]]
        return it["passage"], options, "\n".join(lines), lambda g: g
    raise ValueError(k)


def build():
    rows = []
    fam_ids = {}
    for it in ITEMS:
        fam_ids.setdefault(it["fam"], len(fam_ids) + 1)
    n = 0
    for idx, it in enumerate(ITEMS, 1):
        state, options, card, gold_fn = render(it, idx)
        qtype = "noul" if it["kind"] == "yn" else "choice"
        role = it.get("role", "aff") if qtype == "noul" else "choice"
        gid = f"g:hard_{DOMAIN}:{it['fam'].lower()}"

        def emit(st, cd, gold, instr, twin_of=None):
            nonlocal n
            n += 1
            meta = {"domain": DOMAIN, "difficulty": it["diff"]}
            if twin_of:
                meta["twin_of"] = twin_of
            rows.append({
                "id": f"r_hard_{DOMAIN}_{n}", "group_id": gid, "call_id": call_id(instr, st, options, cd),
                "split": "train", "track": "HARD", "source": f"hard_{DOMAIN}", "state": st, "qtype": qtype,
                "instructions": instr, "options": options, "gold": gold, "role": role, "card": cd, "meta": meta,
            })
            return rows[-1]["id"]

        base_id = emit(state, card, gold_fn(it["gold"]), it["q"])
        if it["twin"]:
            subs, tg = it["twin"][0], it["twin"][1]
            tq = it["twin"][2] if len(it["twin"]) > 2 else it["q"]
            emit(apply_subs(state, subs), apply_subs(card, subs, strict=False), gold_fn(tg), tq, twin_of=base_id)
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
        if set(r) != REQ:
            errs.append(f"{r['id']}: keys {sorted(set(r) ^ REQ)}")
        if r["split"] != "train" or r["track"] != "HARD" or r["source"] != f"hard_{DOMAIN}":
            errs.append(f"{r['id']}: split/track/source")
        if not re.fullmatch(rf"r_hard_{DOMAIN}_\d+", r["id"]):
            errs.append(f"{r['id']}: id format")
        w = words(r["state"])
        if not 80 <= w <= 450:
            errs.append(f"{r['id']}: state words {w}")
        if "{" in r["state"] or "}" in r["state"]:
            errs.append(f"{r['id']}: unfilled template slot")
        if not r["card"] or not all(l.startswith("- ") and ": " in l for l in r["card"].split("\n")):
            errs.append(f"{r['id']}: bad card")
        m = r["meta"]
        if m.get("domain") != DOMAIN or m.get("difficulty") not in (1, 2, 3) or set(m) - {"domain", "difficulty", "twin_of"}:
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
           "twin_share_of_base": round(len(twins) / len(base), 3),
           "groups (minimal sets)": len({r["group_id"] for r in rows})}
    for label, rs in (("base", base), ("all", rows)):
        out[f"qtype_{label}"] = dict(collections.Counter(r["qtype"] for r in rs))
    yn = [r for r in rows if r["qtype"] == "noul"]
    out["noul_gold"] = dict(collections.Counter(r["gold"] for r in yn))
    out["noul_roles"] = dict(collections.Counter(r["role"] for r in yn))
    ch = [r for r in rows if r["qtype"] == "choice"]
    g = collections.Counter(r["gold"] for r in ch)
    out["choice_gold_top"] = g.most_common(8)
    out["choice_gold_max_share"] = round(g.most_common(1)[0][1] / len(ch), 3)
    pos = collections.Counter(r["options"].index(r["gold"]) for r in ch)
    out["choice_gold_position"] = dict(sorted(pos.items()))
    out["option_count_hist"] = dict(sorted(collections.Counter(len(r["options"]) for r in ch).items()))
    out["option_count_hist_base"] = dict(sorted(collections.Counter(
        len(r["options"]) for r in base if r["qtype"] == "choice").items()))
    out["distinct_wordings"] = {q: len({r["instructions"] for r in rows if r["qtype"] == q}) for q in ("noul", "choice")}
    out["difficulty_base"] = dict(sorted(collections.Counter(r["meta"]["difficulty"] for r in base).items()))
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
            f.write(json.dumps({k: v for k, v in r.items() if k != "gold"}, ensure_ascii=False) + "\n")
    print(json.dumps(rep, indent=1, ensure_ascii=False))
    print("wrote", OUT, "and", OUT_BLIND)


if __name__ == "__main__":
    main()
