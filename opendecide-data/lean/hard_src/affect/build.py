"""Build the v0.11 HARD 'affect' items (teacher-authored; no external model, no external dataset).

Families: fine-grained emotion (10-28 defined labels), which-participant-expresses-X, stance toward a named
target (favor / against / neither), service-request intents for invented services, and yes/no variants.

Writes
  lean/data/v11_parts/hard/affect.jsonl        rows with gold
  lean/data/v11_parts/hard/affect.blind.jsonl  identical rows without "gold"
Deterministic (seed 20261001); re-runnable:
  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python lean/hard_src/affect/build.py
"""
from __future__ import annotations

import hashlib
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import (EMO, EMO_ORDER, STANCE, STANCE_ORDER, SERVICES, NONE_LABEL, EMO_Q, WHO_Q, STANCE_Q,  # noqa: E402
                    INTENT_Q, YN_EMO_Q, YN_STANCE_Q, YN_INTENT_Q, NEG_Q, poss)

SEED = 20261001
DOMAIN = "affect"
OUT = HERE.parents[1] / "data" / "v11_parts" / "hard"
BATCHES = ["items_emo1", "items_emo2", "items_who", "items_stance", "items_intent", "items_yn"]
NONE_INTENT_DEF = "the message asks for something that none of the listed intents covers."


def load_items():
    items = []
    for b in BATCHES:
        items.extend(__import__(b).ITEMS)
    keys = [it["key"] for it in items]
    dup = [k for k, n in Counter(keys).items() if n > 1]
    assert not dup, f"duplicate keys {dup}"
    return items


def words(s):
    return len(re.findall(r"\S+", s))


def call_id(instr, state, options, card):
    blob = json.dumps([instr, state, options, card], ensure_ascii=False)
    return "c_" + hashlib.sha1(blob.encode()).hexdigest()[:12]


class Phraser:
    """Deterministic, balanced assignment of question templates (seeded shuffled cycles)."""

    def __init__(self, name, pool):
        self.rng = random.Random(f"{SEED}:{name}")
        self.pool = list(pool)
        self.queue = []

    def next(self, ok=lambda t: True):
        for _ in range(3 * len(self.pool)):
            if not self.queue:
                self.queue = self.pool[:]
                self.rng.shuffle(self.queue)
            t = self.queue.pop()
            if ok(t):
                return t
        raise RuntimeError("no acceptable template")


def cap(s):
    return s[0].upper() + s[1:]


def apply_subs(state, subs, key):
    for old, new in subs:
        n = state.count(old)
        assert n == 1, f"{key}: substitution target found {n} times: {old[:70]!r}"
        state = state.replace(old, new)
    return state


def intent_def(service, label):
    return dict(SERVICES[service])[label]


def emo_options(it):
    rng = random.Random(f"{SEED}:emo:{it['key']}")
    req = [it["gold"]]
    if it["twin"]:
        req.append(it["twin"]["gold"])
    req += it["near"]
    req = [k for k in dict.fromkeys(req) if k != "neutral"]
    n = it["n"] or rng.randint(10, 28)
    n = max(n, len(req) + 1)
    pool = [k for k in EMO_ORDER if k not in req and k != "neutral"]
    labs = req + rng.sample(pool, n - 1 - len(req))
    rng.shuffle(labs)
    return labs + ["neutral"]


def build():
    items = load_items()
    ph = {name: Phraser(name, pool) for name, pool in
          [("emo", EMO_Q), ("who", WHO_Q), ("stance", STANCE_Q), ("intent", INTENT_Q), ("yemo", YN_EMO_Q),
           ("ystance", YN_STANCE_Q), ("yintent", YN_INTENT_Q), ("nemo", NEG_Q["emo"]),
           ("nstance", NEG_Q["stance"]), ("nintent", NEG_Q["intent"])]}
    rows = []
    n = 0

    def emit(it, state, gold, instr, options, card, qtype, role, twin_of=None):
        nonlocal n
        n += 1
        rid = f"r_hard_{DOMAIN}_{n}"
        meta = {"domain": DOMAIN, "difficulty": it["diff"]}
        if twin_of:
            meta = {"domain": DOMAIN, "twin_of": twin_of, "difficulty": it["diff"]}
        rows.append({
            "id": rid,
            "group_id": f"g:hard_{DOMAIN}:{it['key']}",
            "call_id": call_id(instr, state, options, card),
            "split": "train",
            "track": "HARD",
            "source": f"hard_{DOMAIN}",
            "state": state,
            "qtype": qtype,
            "instructions": instr,
            "options": options,
            "gold": gold,
            "role": role,
            "card": card,
            "meta": meta,
        })
        return rid

    for it in items:
        kind, tw = it["kind"], it.get("twin")
        if kind == "emo":
            options = emo_options(it)
            card = "\n".join(f"- {k}: {EMO[k]}" for k in options)
            tmpl = it["q"] or ph["emo"].next()
            instr = cap(tmpl.format(t=it["t"]))
            bid = emit(it, it["state"], it["gold"], instr, options, card, "choice", "choice")
            if tw:
                assert tw["gold"] != it["gold"] and tw["gold"] in options, it["key"]
                st = apply_subs(it["state"], tw["subs"], it["key"])
                ins = cap((tw["q"] or tmpl).format(t=tw["t"] or it["t"]))
                emit(it, st, tw["gold"], ins, options, card, "choice", "choice", twin_of=bid)
        elif kind == "who":
            people = list(it["people"])
            random.Random(f"{SEED}:who:{it['key']}").shuffle(people)
            options = people + [NONE_LABEL]
            card = "\n".join(f"- {k}: {EMO[k]}" for k in [it["emo"]] + it["extra"])
            card += f"\n- {NONE_LABEL}: none of the listed people expresses {it['emo']} as defined above."
            tmpl = it["q"] or ph["who"].next()
            instr = cap(tmpl.format(e=it["emo"]))
            bid = emit(it, it["state"], it["gold"], instr, options, card, "choice", "choice")
            if tw:
                assert tw["gold"] != it["gold"] and tw["gold"] in options, it["key"]
                st = apply_subs(it["state"], tw["subs"], it["key"])
                emit(it, st, tw["gold"], cap(tw["q"]) if tw["q"] else instr, options, card, "choice", "choice",
                     twin_of=bid)
        elif kind == "stance":
            options = list(STANCE_ORDER)
            random.Random(f"{SEED}:stance:{it['key']}").shuffle(options)
            card = "\n".join(f"- {k}: {STANCE[k]}" for k in options)
            named = it["t"] != "the author"
            tmpl = it["q"] or ph["stance"].next(ok=lambda t: (not named) or "{t" in t)
            instr = cap(tmpl.format(t=it["t"], tp=poss(it["t"]), x=it["x"]))
            bid = emit(it, it["state"], it["gold"], instr, options, card, "choice", "choice")
            if tw:
                assert tw["gold"] != it["gold"], it["key"]
                st = apply_subs(it["state"], tw["subs"], it["key"])
                t2 = tw["t"] or it["t"]
                ins = cap((tw["q"] or tmpl).format(t=t2, tp=poss(t2), x=tw["x"] or it["x"]))
                emit(it, st, tw["gold"], ins, options, card, "choice", "choice", twin_of=bid)
        elif kind == "intent":
            labs = list(it["intents"])
            random.Random(f"{SEED}:intent:{it['key']}").shuffle(labs)
            options = labs + ([NONE_LABEL] if it["none"] else [])
            card = "\n".join(f"- {k}: {intent_def(it['service'], k)}" for k in labs)
            if it["none"]:
                card += f"\n- {NONE_LABEL}: {NONE_INTENT_DEF}"
            tmpl = it["q"] or ph["intent"].next()
            instr = cap(tmpl.format(s=it["service"]))
            bid = emit(it, it["state"], it["gold"], instr, options, card, "choice", "choice")
            if tw:
                assert tw["gold"] != it["gold"] and tw["gold"] in options, it["key"]
                st = apply_subs(it["state"], tw["subs"], it["key"])
                emit(it, st, tw["gold"], cap(tw["q"]) if tw["q"] else instr, options, card, "choice", "choice",
                     twin_of=bid)
        elif kind == "yn":
            fam, neg = it["fam"], it["neg"]
            role = "neg" if neg else "aff"
            pk = ("n" if neg else "y") + fam
            if fam == "emo":
                card = "\n".join(f"- {k}: {EMO[k]}" for k in [it["lab"]] + it["extra"])
                fmt = dict(t=it["t"], e=it["lab"])
            elif fam == "stance":
                card = "\n".join(f"- {k}: {STANCE[k]}" for k in STANCE_ORDER)
                fmt = dict(t=it["t"], tp=poss(it["t"]), x=it["x"], c=it["lab"])
            else:
                card = "\n".join(f"- {k}: {intent_def(it['service'], k)}" for k in [it["lab"]] + it["extra"])
                fmt = dict(s=it["service"], i=it["lab"])
            tmpl = it["q"] or ph[pk].next()
            instr = cap(tmpl.format(**fmt))
            g = (1 - it["truth"]) if neg else it["truth"]
            bid = emit(it, it["state"], g, instr, None, card, "noul", role)
            if tw:
                assert tw["gold"] in (0, 1) and tw["gold"] != it["truth"], it["key"]
                st = apply_subs(it["state"], tw["subs"], it["key"])
                g2 = (1 - tw["gold"]) if neg else tw["gold"]
                emit(it, st, g2, cap(tw["q"]) if tw["q"] else instr, None, card, "noul", role, twin_of=bid)
        else:
            raise ValueError(kind)
    return items, rows


REQ = ["id", "group_id", "call_id", "split", "track", "source", "state", "qtype", "instructions", "options", "gold",
       "role", "card", "meta"]
BANNED_SOURCES = re.compile(r"\b(?:legalbench|lexglue|cuad|maud|scone|hatecheck|pubmedqa|vitaminc|goemotions|"
                            r"tweet_eval|rotten_tomatoes|sms_spam|ag_news|enron|climatebert|imdb|sst-2|btzsc)\b", re.I)


def validate(items, rows):
    errs = []
    ids, cids = set(), Counter()
    kind_of = {f"g:hard_{DOMAIN}:{it['key']}": it["kind"] for it in items}
    for r in rows:
        rid = r["id"]
        if list(r.keys()) != REQ:
            errs.append((rid, "keys"))
        if rid in ids:
            errs.append((rid, "dup id"))
        ids.add(rid)
        cids[r["call_id"]] += 1
        if r["split"] != "train" or r["track"] != "HARD" or r["source"] != f"hard_{DOMAIN}":
            errs.append((rid, "split/track/source"))
        w = words(r["state"])
        if not 80 <= w <= 450:
            errs.append((rid, f"state words {w}"))
        if BANNED_SOURCES.search(r["state"] + r["instructions"] + r["card"]):
            errs.append((rid, "banned source name"))
        if r["qtype"] == "choice":
            o = r["options"]
            if not (isinstance(o, list) and 3 <= len(o) <= 28 and len(set(o)) == len(o)):
                errs.append((rid, "options"))
            if kind_of[r["group_id"]] == "emo" and not 10 <= len(o) <= 28:
                errs.append((rid, "emotion label count"))
            if any(": " in x for x in o):
                errs.append((rid, "': ' in option"))
            if r["gold"] not in o:
                errs.append((rid, "gold not in options"))
            if r["role"] != "choice":
                errs.append((rid, "role"))
            if kind_of[r["group_id"]] in ("emo", "stance", "intent"):
                card_labels = [ln[2:].split(": ", 1)[0] for ln in r["card"].split("\n")]
                if card_labels != o:
                    errs.append((rid, "card labels != options"))
        elif r["qtype"] == "noul":
            if r["options"] is not None or r["gold"] not in (0, 1) or r["role"] not in ("aff", "neg"):
                errs.append((rid, "noul fields"))
        else:
            errs.append((rid, "qtype"))
        if not r["card"] or not all(ln.startswith("- ") and ": " in ln for ln in r["card"].split("\n")):
            errs.append((rid, "card format"))
        m = r["meta"]
        if m.get("domain") != DOMAIN or m.get("difficulty") not in (1, 2, 3):
            errs.append((rid, "meta"))
        if "twin_of" in m and m["twin_of"] not in ids:
            errs.append((rid, "twin_of unknown"))
    dup_c = [c for c, k in cids.items() if k > 1]
    if dup_c:
        errs.append(("-", f"duplicate call_ids {dup_c}"))
    by_id = {r["id"]: r for r in rows}
    for r in rows:
        t = r["meta"].get("twin_of")
        if t:
            b = by_id[t]
            if b["group_id"] != r["group_id"] or b["call_id"] == r["call_id"] or b["gold"] == r["gold"]:
                errs.append((r["id"], "twin relation"))
    # balance: no choice gold label above 40% overall or within a family
    choice = [r for r in rows if r["qtype"] == "choice"]
    gc = Counter(r["gold"] for r in choice)
    if max(gc.values()) / len(choice) > 0.4:
        errs.append(("-", "choice gold imbalance"))
    for fam in ("emo", "who", "stance", "intent"):
        fr = [r for r in choice if kind_of[r["group_id"]] == fam]
        fc = Counter(r["gold"] for r in fr)
        if fr and max(fc.values()) / len(fr) > 0.4:
            errs.append(("-", f"{fam} gold imbalance {fc.most_common(3)}"))
    return errs


def leak_report(items, rows):
    """Rows whose state contains the gold label as a whole word (manual review list; not an error)."""
    kind_of = {f"g:hard_{DOMAIN}:{it['key']}": it["kind"] for it in items}
    out = []
    for r in rows:
        k = kind_of[r["group_id"]]
        if r["qtype"] == "choice" and k in ("emo", "stance", "intent") and r["gold"] != NONE_LABEL:
            if re.search(r"\b" + re.escape(r["gold"]) + r"\b", r["state"], re.I):
                out.append((r["id"], r["gold"]))
    return out


def summary(items, rows):
    kind_of = {f"g:hard_{DOMAIN}:{it['key']}": it["kind"] for it in items}
    base = [r for r in rows if "twin_of" not in r["meta"]]
    twins = [r for r in rows if "twin_of" in r["meta"]]
    choice = [r for r in rows if r["qtype"] == "choice"]
    noul = [r for r in rows if r["qtype"] == "noul"]
    gc = Counter(r["gold"] for r in choice)
    fam_gold = {}
    for fam in ("emo", "who", "stance", "intent"):
        fr = [r for r in choice if kind_of[r["group_id"]] == fam]
        fc = Counter(r["gold"] for r in fr)
        fam_gold[fam] = {"rows": len(fr), "max_share": round(max(fc.values()) / len(fr), 3),
                         "top": fc.most_common(6)}
    return {
        "rows": len(rows),
        "base_items": len(base),
        "twins": len(twins),
        "twin_rate": round(len(twins) / len(base), 3),
        "base_by_family": dict(Counter(kind_of[r["group_id"]] for r in base)),
        "base_by_qtype": dict(Counter(r["qtype"] for r in base)),
        "rows_by_qtype": dict(Counter(r["qtype"] for r in rows)),
        "twins_by_qtype": dict(Counter(r["qtype"] for r in twins)),
        "yes_no_gold": dict(Counter(r["gold"] for r in noul)),
        "yes_no_roles": dict(Counter(r["role"] for r in noul)),
        "choice_gold_max_share": round(max(gc.values()) / len(choice), 3),
        "choice_gold_by_family": fam_gold,
        "option_count_hist_rows": dict(sorted(Counter(len(r["options"]) for r in choice).items())),
        "option_count_hist_base": dict(sorted(Counter(len(r["options"]) for r in base if r["options"]).items())),
        "difficulty_rows": dict(sorted(Counter(r["meta"]["difficulty"] for r in rows).items())),
        "distinct_instructions": {
            "choice": len(set(r["instructions"] for r in choice)),
            "noul": len(set(r["instructions"] for r in noul)),
        },
        "state_words": {"min": min(words(r["state"]) for r in rows), "max": max(words(r["state"]) for r in rows),
                        "mean": round(sum(words(r["state"]) for r in rows) / len(rows), 1)},
    }


def main():
    items, rows = build()
    errs = validate(items, rows)
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / f"{DOMAIN}.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(OUT / f"{DOMAIN}.blind.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps({k: v for k, v in r.items() if k != "gold"}, ensure_ascii=False) + "\n")
    s = summary(items, rows)
    print(json.dumps(s, indent=1))
    lk = leak_report(items, rows)
    if lk:
        print("REVIEW (gold label word appears in state):", lk)
    if errs:
        print("ERRORS:")
        for e in errs:
            print(" ", e)
        sys.exit(1)
    print("OK: schema valid")


if __name__ == "__main__":
    main()
