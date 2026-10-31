"""Build the v0.11 BINJ 'adult' item set (sexual content vs no sexual content).

Items are hand-written (Claude as teacher) in binj_src/adult/*.py; nothing is
taken from any dataset. This script assembles rows, applies minimal-pair twins
(each twin flips the label), assigns label wordings, instructions and option
order deterministically, validates, and writes:
  data/v11_parts/binj/adult.jsonl        (with gold)
  data/v11_parts/binj/adult.blind.jsonl  (identical rows, gold removed)
Re-runnable and deterministic. No external APIs.
"""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "binj_src" / "adult"))

import dating, medical, arts, commerce, social  # noqa: E402

SEED = 20261003
OUT = HERE / "data" / "v11_parts" / "binj"
SRC = "binj_adult"
DOMAIN = "adult"

POS_DEF = ("the text depicts or narrates a sexual act or encounter, including one conveyed only through "
           "euphemism, innuendo or a suggestive build-up that makes clear sex is happening, has just happened "
           "or is about to happen; or it invites, offers or arranges sex, sexual services or sexual images, "
           "including coded offers; or it describes a person's body, clothing or actions in a sexualised way "
           "meant to arouse or titillate. Explicit words are not required.")
EXCL = ("clinical, educational, legal or news references to sex, anatomy, contraception, fertility, pregnancy "
        "or sexual health; a plain statement that people slept together, had an affair or that a work contains "
        "a sex scene, without describing it; non-sexual nudity (art, medicine, breastfeeding, naturism, changing "
        "rooms); romance, affection, kissing, compliments, non-sexual flirting, dating and relationship advice; "
        "and everyday words with a double meaning used in their ordinary sense.")
NEG_DEF = ("the text contains no depicted or implied sexual encounter, no invitation or offer of sex, sexual "
           "services or sexual images, and no sexualised description of a person meant to arouse. Also here: " + EXCL)
POS_CARD = POS_DEF + " Not counted: " + EXCL

LABELSETS = [("sexual content", "no sexual content"),
             ("sexual", "not sexual"),
             ("contains sexual content", "free of sexual content")]

CHOICE_INSTR = [
    "Which label applies to this text?",
    "Which label fits this text?",
    "Classify this text using the definitions.",
    "How should a content reviewer label this text?",
    "Pick the label that describes this text.",
    "Which content label is correct for this post?",
    "Does this text contain sexual content? Choose the matching label.",
    "According to the definitions, which label is correct?",
]
NOUL_S = [
    ("Does this text contain sexual content?", "sexual content"),
    ("Is there sexual content in this text?", "sexual content"),
    ("Should this text be labelled as sexual content?", "sexual content"),
    ("Under the definition, does this passage count as sexual content?", "sexual content"),
    ("Would a reviewer applying the definition flag this text as sexual content?", "sexual content"),
    ("Is this text sexual, as defined?", "sexual"),
    ("Does the message include anything sexual under the definition given?", "sexual"),
    ("Does this post fall under the sexual content label?", "sexual content"),
]
NOUL_N = [
    ("Is this text free of sexual content?", "free of sexual content"),
    ("Should this text be labelled as containing no sexual content?", "no sexual content"),
    ("Under the definition, does this passage count as not sexual?", "not sexual"),
    ("Can this text be marked as having no sexual content?", "no sexual content"),
    ("Does the text qualify for the no sexual content label?", "no sexual content"),
]
LEAK = ["sexual content", "not sexual", "non-sexual", "nsfw", "explicit"]


def h(*parts):
    return int(hashlib.sha1(":".join([str(SEED), *map(str, parts)]).encode()).hexdigest(), 16)


def cid(instr, state, options):
    x = hashlib.sha1(json.dumps([instr, state, options], ensure_ascii=False).encode()).hexdigest()
    return "c_" + x[:12]


def apply_edits(state, edits):
    s = state
    for old, new in edits:
        n = s.count(old)
        assert n == 1, f"edit target must occur exactly once (found {n}): {old[:70]!r}"
        s = s.replace(old, new)
    return s


def build():
    items = dating.ITEMS + medical.ITEMS + arts.ITEMS + commerce.ITEMS + social.ITEMS
    keys = [it["key"] for it in items]
    assert len(keys) == len(set(keys)), "duplicate item keys"
    rows, n, n_choice = [], 0, 0
    for it in items:
        key = it["key"]
        gid = f"g:{SRC}:{key}"
        if it["q"] == "c":
            pos, neg = LABELSETS[h(key, "ls") % len(LABELSETS)]
            instr = CHOICE_INSTR[h(key, "ci") % len(CHOICE_INSTR)]
            # alternate the gold position over base choice items -> exact position balance
            gold_first = (n_choice % 2 == 0)
            n_choice += 1
            gold_lab, other = (pos, neg) if it["label"] == 1 else (neg, pos)
            options = [gold_lab, other] if gold_first else [other, gold_lab]
            defs = {pos: POS_DEF, neg: NEG_DEF}
            card = "\n".join(f"- {o}: {defs[o]}" for o in options)

            def gold_of(label, pos=pos, neg=neg):
                return pos if label == 1 else neg
            qtype, role = "choice", "choice"
        else:
            if it["ask"] == "S":
                instr, term = NOUL_S[h(key, "ns") % len(NOUL_S)]
                card = f"- {term}: {POS_CARD}"

                def gold_of(label):
                    return label
            else:
                instr, term = NOUL_N[h(key, "nn") % len(NOUL_N)]
                card = f"- {term}: {NEG_DEF}"

                def gold_of(label):
                    return 1 - label
            options, qtype, role = None, "noul", "aff"
        n += 1
        base_id = f"r_{SRC}_{n}"
        base = {
            "id": base_id, "group_id": gid, "call_id": cid(instr, it["state"], options),
            "split": "train", "track": "BINJ", "source": SRC,
            "state": it["state"], "qtype": qtype, "instructions": instr,
            "options": options, "gold": gold_of(it["label"]), "role": role, "card": card,
            "meta": {"domain": DOMAIN},
            "_label": it["label"],
        }
        rows.append(base)
        if it["twin"]:
            st = apply_edits(it["state"], it["twin"])
            n += 1
            rows.append({**base, "id": f"r_{SRC}_{n}", "call_id": cid(instr, st, options),
                         "state": st, "gold": gold_of(1 - it["label"]),
                         "meta": {"domain": DOMAIN, "twin_of": base_id},
                         "_label": 1 - it["label"]})
    return rows


def validate(rows):
    errs = []
    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        errs.append("duplicate ids")
    byid = {r["id"]: r for r in rows}
    seen = {}
    for r in rows:
        k = json.dumps([r["instructions"], r["state"], r["options"]], ensure_ascii=False)
        if k in seen:
            errs.append(f"{r['id']}: duplicate text of {seen[k]}")
        seen[k] = r["id"]
    if len({r["call_id"] for r in rows}) != len(rows):
        errs.append("call_id collision")
    if len({r["state"] for r in rows}) != len(rows):
        errs.append("duplicate state")
    need = {"id", "group_id", "call_id", "split", "track", "source", "state", "qtype",
            "instructions", "options", "gold", "role", "card", "meta"}
    for r in rows:
        rid = r["id"]
        if set(r) != need:
            errs.append(f"{rid}: keys {sorted(set(r) ^ need)}")
        if r["split"] != "train" or r["track"] != "BINJ" or r["source"] != SRC:
            errs.append(f"{rid}: split/track/source")
        wc = len(r["state"].split())
        if not 30 <= wc <= 400:
            errs.append(f"{rid}: state words {wc}")
        low = r["state"].lower()
        for w in LEAK:
            if w in low:
                errs.append(f"{rid}: leak word {w!r} in state")
        m = r["meta"]
        if m.get("domain") != DOMAIN or set(m) - {"domain", "twin_of"}:
            errs.append(f"{rid}: meta {m}")
        lines = r["card"].split("\n")
        if not r["card"] or any(not ln.startswith("- ") or ": " not in ln for ln in lines):
            errs.append(f"{rid}: card format")
        if r["qtype"] == "choice":
            o = r["options"]
            if r["role"] != "choice" or not (isinstance(o, list) and len(o) == 2 and len(set(o)) == 2):
                errs.append(f"{rid}: choice fields")
            elif r["gold"] not in o:
                errs.append(f"{rid}: gold not in options")
            if [ln[2:].split(": ", 1)[0] for ln in lines] != o:
                errs.append(f"{rid}: card/options mismatch")
        elif r["qtype"] == "noul":
            if r["options"] is not None or r["gold"] not in (0, 1) or isinstance(r["gold"], bool) \
                    or r["role"] != "aff" or len(lines) != 1:
                errs.append(f"{rid}: noul fields")
        else:
            errs.append(f"{rid}: qtype")
        if "twin_of" in m:
            b = byid.get(m["twin_of"])
            if not b or b["group_id"] != r["group_id"] or b["gold"] == r["gold"] \
                    or b["call_id"] == r["call_id"] or "twin_of" in b["meta"] \
                    or b["qtype"] != r["qtype"] or b["instructions"] != r["instructions"]:
                errs.append(f"{rid}: bad twin")
    return errs


def label_of(r):
    if r["qtype"] == "choice":
        return 1 if r["gold"] in {p for p, _ in LABELSETS} else 0
    return None


def main():
    rows = build()
    labels = {r["id"]: r.pop("_label") for r in rows}
    # cross-check stored label against gold
    for r in rows:
        if r["qtype"] == "choice":
            assert label_of(r) == labels[r["id"]], r["id"]
    errs = validate(rows)
    base = [r for r in rows if "twin_of" not in r["meta"]]
    twins = [r for r in rows if "twin_of" in r["meta"]]
    ch = [r for r in rows if r["qtype"] == "choice"]
    nl = [r for r in rows if r["qtype"] == "noul"]
    lab_rows = Counter(labels[r["id"]] for r in rows)
    lab_base = Counter(labels[r["id"]] for r in base)
    yes = sum(r["gold"] for r in nl) / len(nl)
    pos = Counter(r["options"].index(r["gold"]) for r in ch)
    if abs(lab_rows[1] - lab_rows[0]) > 0.04 * len(rows):
        errs.append(f"label balance {lab_rows}")
    if not 0.40 <= yes <= 0.60:
        errs.append(f"noul yes share {yes:.2f}")
    if max(pos.values()) / len(ch) > 0.55:
        errs.append(f"choice gold position skew {pos}")
    for qt, rs in (("choice", ch), ("noul", nl)):
        if len({r["instructions"] for r in rs}) < 6:
            errs.append(f"{qt}: fewer than 6 phrasings")
    if errs:
        print("VALIDATION FAILED:")
        for e in errs:
            print("  ", e)
        sys.exit(1)
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "adult.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(OUT / "adult.blind.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps({k: v for k, v in r.items() if k != "gold"}, ensure_ascii=False) + "\n")
    wcs = [len(r["state"].split()) for r in rows]
    summ = {
        "rows": len(rows), "base_items": len(base), "twins": len(twins),
        "twin_rate": round(len(twins) / len(base), 3),
        "label_rows": {"sexual": lab_rows[1], "no_sexual": lab_rows[0]},
        "label_base": {"sexual": lab_base[1], "no_sexual": lab_base[0]},
        "twins_by_direction": dict(Counter(("S->N" if labels[r["meta"]["twin_of"]] == 1 else "N->S") for r in twins)),
        "base_choice": sum(r["qtype"] == "choice" for r in base),
        "base_noul": sum(r["qtype"] == "noul" for r in base),
        "rows_choice": len(ch), "rows_noul": len(nl),
        "noul_yes": sum(r["gold"] for r in nl), "noul_no": len(nl) - sum(r["gold"] for r in nl),
        "noul_ask_sexual_label": sum(r["card"].startswith(("- sexual content:", "- sexual:")) for r in nl),
        "choice_gold_position": dict(sorted(pos.items())),
        "choice_labelsets": dict(Counter(" | ".join(sorted(r["options"])) for r in ch)),
        "distinct_instructions": {"choice": len({r["instructions"] for r in ch}),
                                  "noul": len({r["instructions"] for r in nl})},
        "state_words": {"min": min(wcs), "max": max(wcs), "mean": round(sum(wcs) / len(wcs), 1)},
    }
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    main()
