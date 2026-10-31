"""Build the v0.11 BINJ 'offensive' set (offensive vs not offensive, with definitions).

Items are hand-written (Claude as teacher) in binj_src/offensive/items_{not,off}.py.
All texts are invented; no external datasets or APIs are used.
This script assembles rows, applies minimal-pair twins (label flipped), assigns
choice / yes-no formats deterministically (seed below), validates, and writes:
  data/v11_parts/binj/offensive.jsonl        (with gold)
  data/v11_parts/binj/offensive.blind.jsonl  (identical rows, gold removed)
Re-runnable and deterministic.
"""
import difflib
import hashlib
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "binj_src" / "offensive"))

import items_not, items_off  # noqa: E402

SEED = 20261102
DOMAIN = "offensive"
SRC = "binj_offensive"
OUT = HERE / "data" / "v11_parts" / "binj"

# ------------------------------------------------------------------ definitions
DEFS = {
    "A": {
        "offensive": "the post itself is rude, insulting, demeaning or hateful toward a person or a group, whether openly or through sarcasm, coded language, stereotypes, 'jokes', or praise that carries a put-down. Quoting, reporting, discussing or condemning such language does not make a post offensive, and neither do swearing that targets no one, forceful disagreement with ideas or actions, or jokes at the author's own expense.",
        "not offensive": "nothing in the author's own voice insults, demeans or expresses contempt for a person or group. Posts that quote or report an insult in order to criticise it, counter-speech, reclaimed in-group terms used by members of that group, strong but civil disagreement, untargeted profanity, self-directed dark humour and discussions of slurs or insulting words all belong here.",
    },
    "B": {
        "offensive": "the author attacks someone: insults, belittles or dehumanises an individual (including another user) or a group defined by traits such as race, nationality, religion, gender, sexuality, disability, age, class, appearance or occupation, or expresses contempt for them, even when the wording is polite, indirect, or framed as a compliment, a question or a joke.",
        "not offensive": "the author attacks no one. A post can mention slurs, repeat what someone else said in order to object to it, swear, argue hard, criticise a policy, product, company or decision, or make fun of the author themself, and still not be offensive.",
    },
    "C": {
        "offensive": "a moderator applying a civility policy would flag the post because its author degrades, mocks, insults or shows hatred toward a person or group. Dog whistles, stereotypes presented as 'just noticing', condescension and backhanded compliments count when they are aimed at a person or group; words that are only mentioned, quoted or reported do not.",
        "not offensive": "a moderator applying a civility policy would leave the post up because its author does not degrade, mock or insult any person or group. Reported speech, counter-speech, reclaimed terms, civil disagreement, profanity used only for emphasis and self-mockery fall here, even when the post contains harsh or taboo words.",
    },
}

OPTION_VARIANTS = [
    ["offensive", "not offensive"],
    ["not offensive", "offensive"],
    ["offensive", "non-offensive"],
    ["non-offensive", "offensive"],
]

CHOICE_TMPL = [
    "Is {t} offensive or not offensive?",
    "Which label fits {t}?",
    "How should a moderator label {t}?",
    "Classify {t} using the definitions.",
    "Pick the correct label for {t}.",
    "Under the definitions given, which label applies to {t}?",
    "An annotator is labelling {t}. Which label is correct?",
    "Which of the two labels best describes {t}?",
]

YN_TMPL = {
    "off": [
        "Is {t} offensive?",
        "Does {t} count as offensive under the definition?",
        "Should {t} be labelled offensive?",
        "Would a moderator applying the definition mark {t} as offensive?",
        "Does {t} meet the definition of offensive?",
        "Is 'offensive' the correct label for {t}?",
        "According to the definition, is {t} offensive?",
    ],
    "not": [
        "Is {t} not offensive?",
        "Should {t} be labelled not offensive?",
        "Does {t} fall under 'not offensive' as defined?",
        "Is 'not offensive' the correct label for {t}?",
        "Would an annotator following the definition mark {t} as not offensive?",
        "Can {t} be classed as not offensive?",
        "Does {t} qualify as not offensive under the definition?",
    ],
}


def label_name(y, options):
    """Return the option string for label y (1 offensive / 0 not) within options."""
    if y == 1:
        return "offensive"
    return [o for o in options if o != "offensive"][0]


def def_key(opt):
    return "not offensive" if opt in ("not offensive", "non-offensive") else "offensive"


def cid(instr, state, options):
    h = hashlib.sha1(json.dumps([instr, state, options], ensure_ascii=False).encode()).hexdigest()
    return "c_" + h[:12]


def apply_edits(state, edits):
    s = state
    for old, new in edits:
        n = s.count(old)
        if n != 1:
            raise ValueError(f"edit target found {n} times: {old[:60]!r}")
        s = s.replace(old, new)
    return s


def words(s):
    return len(re.findall(r"\S+", s))


def main():
    rng = random.Random(SEED)
    base = [dict(it) for it in items_not.ITEMS] + [dict(it) for it in items_off.ITEMS]
    keys = [it["k"] for it in base]
    assert len(keys) == len(set(keys)), "duplicate slugs"

    # --- format assignment: 30% yes/no, stratified by label
    for y, n_yn in ((0, 26), (1, 25)):
        grp = [it for it in base if it["y"] == y]
        pick = set(it["k"] for it in rng.sample(grp, n_yn))
        yn_items = [it for it in grp if it["k"] in pick]
        rng.shuffle(yn_items)
        for i, it in enumerate(yn_items):
            it["fmt"] = "yn"
            it["ask"] = "off" if i % 2 == 0 else "not"
        for it in grp:
            it.setdefault("fmt", "choice")

    rng.shuffle(base)
    rows = []
    n = 0
    ov_i = 0
    for it in base:
        twin_state = None
        if "tw" in it:
            twin_state = apply_edits(it["s"], it["tw"])
        elif "tw_full" in it:
            twin_state = it["tw_full"]
        dkey = rng.choice("ABC")
        t = it["t"]
        if it["fmt"] == "choice":
            options = list(OPTION_VARIANTS[ov_i % len(OPTION_VARIANTS)])
            ov_i += 1
            instr = rng.choice(CHOICE_TMPL).format(t=t)
            card = "\n".join(f"- {o}: {DEFS[dkey][def_key(o)]}" for o in options)
        else:
            options = None
            ask = it["ask"]
            instr = rng.choice(YN_TMPL[ask]).format(t=t)
            lab = "offensive" if ask == "off" else "not offensive"
            card = f"- {lab}: {DEFS[dkey][lab]}"

        def mk(state, y, twin_of=None):
            nonlocal n
            n += 1
            rid = f"r_binj_{DOMAIN}_{n}"
            if options is not None:
                gold = label_name(y, options)
                qtype, role = "choice", "choice"
            else:
                gold = 1 if ((it["ask"] == "off") == (y == 1)) else 0
                qtype, role = "noul", "aff"
            meta = {"domain": DOMAIN}
            if twin_of:
                meta["twin_of"] = twin_of
            row = {
                "id": rid,
                "group_id": f"g:{SRC}:{it['k']}",
                "call_id": cid(instr, state, options),
                "split": "train",
                "track": "BINJ",
                "source": SRC,
                "state": state,
                "qtype": qtype,
                "instructions": instr,
                "options": options,
                "gold": gold,
                "role": role,
                "card": card,
                "meta": meta,
            }
            rows.append(row)
            row["_y"] = y  # internal, stripped before writing
            return rid

        bid = mk(it["s"], it["y"])
        if twin_state is not None:
            mk(twin_state, 1 - it["y"], twin_of=bid)

    validate(rows)
    OUT.mkdir(parents=True, exist_ok=True)
    full = OUT / f"{DOMAIN}.jsonl"
    blind = OUT / f"{DOMAIN}.blind.jsonl"
    with full.open("w") as f:
        for r in rows:
            r = {k: v for k, v in r.items() if k != "_y"}
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with blind.open("w") as f:
        for r in rows:
            r = {k: v for k, v in r.items() if k not in ("_y", "gold")}
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    report(rows)
    print("wrote", full, "and", blind)


REQ = ["id", "group_id", "call_id", "split", "track", "source", "state", "qtype",
       "instructions", "options", "gold", "role", "card", "meta"]
BANNED = ["social bias frames", "trueteacher", "btzsc", "hatecheck"]


def validate(rows):
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids)), "dup ids"
    assert len({r["call_id"] for r in rows}) == len(rows), "dup call_ids"
    assert len({r["state"] for r in rows}) == len(rows), "dup states"
    byid = {r["id"]: r for r in rows}
    for r in rows:
        for k in REQ:
            assert k in r, (r["id"], k)
        assert r["split"] == "train" and r["track"] == "BINJ" and r["source"] == SRC
        assert r["meta"]["domain"] == DOMAIN
        w = words(r["state"])
        assert 30 <= w <= 400, (r["id"], w)
        low = r["state"].lower()
        for b in BANNED:
            assert b not in low, (r["id"], b)
        if re.search(r"\boffensive\b|\binoffensive\b|non-offensive", low):
            raise AssertionError(f"label word in state: {r['id']}")
        if r["qtype"] == "choice":
            assert isinstance(r["options"], list) and len(r["options"]) == 2
            assert r["gold"] in r["options"] and r["role"] == "choice"
            lines = r["card"].split("\n")
            assert len(lines) == 2 and all(l.startswith("- ") for l in lines)
            assert (r["gold"] == "offensive") == (r["_y"] == 1)
        else:
            assert r["qtype"] == "noul" and r["options"] is None
            assert r["gold"] in (0, 1) and r["role"] == "aff"
            assert r["card"].startswith("- ") and "\n" not in r["card"]
        tw = r["meta"].get("twin_of")
        if tw:
            b = byid[tw]
            assert b["group_id"] == r["group_id"] and b["_y"] != r["_y"]
            assert b["instructions"] == r["instructions"] and b["options"] == r["options"]
            assert b["gold"] != r["gold"]


def report(rows):
    y = Counter("offensive" if r["_y"] else "not offensive" for r in rows)
    base = [r for r in rows if "twin_of" not in r["meta"]]
    twins = [r for r in rows if "twin_of" in r["meta"]]
    print("rows", len(rows), "base", len(base), "twins", len(twins))
    print("label balance (all rows):", dict(y))
    print("label balance (base):", dict(Counter("offensive" if r["_y"] else "not offensive" for r in base)))
    print("qtype (all):", dict(Counter(r["qtype"] for r in rows)), " qtype (base):", dict(Counter(r["qtype"] for r in base)))
    ch = [r for r in rows if r["qtype"] == "choice"]
    print("choice gold:", dict(Counter(r["gold"] for r in ch)),
          " gold position:", dict(Counter(r["options"].index(r["gold"]) for r in ch)))
    yn = [r for r in rows if r["qtype"] == "noul"]
    print("yes/no gold:", dict(Counter(r["gold"] for r in yn)),
          " asked label:", dict(Counter("offensive" if "not offensive" not in r["card"] else "not offensive" for r in yn)))
    print("distinct instructions: choice", len({r["instructions"].split(' {')[0] for r in ch}),
          " yn", len({r["instructions"] for r in yn}))
    wc = sorted(words(r["state"]) for r in rows)
    print("state words min/median/max:", wc[0], wc[len(wc) // 2], wc[-1],
          " >150 words:", sum(w > 150 for w in wc))
    byid = {r["id"]: r for r in rows}
    ratios = sorted(difflib.SequenceMatcher(None, byid[r["meta"]["twin_of"]]["state"], r["state"]).ratio() for r in twins)
    print("twin similarity min/median/max: %.2f %.2f %.2f" % (ratios[0], ratios[len(ratios) // 2], ratios[-1]))


if __name__ == "__main__":
    main()
