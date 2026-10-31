"""Build the v0.11 BINJ 'consistency' items (teacher-authored; no external model, no external dataset).

Task: is a summary (or claim) factually consistent with its source text? Two labels, precise definitions in the card.
Source texts, summaries and minimal-pair twins are written by the teacher (Claude) in items*.txt; every person,
organisation, product and place is invented.

Writes
  lean/data/v11_parts/binj/consistency.jsonl        rows with gold
  lean/data/v11_parts/binj/consistency.blind.jsonl  identical rows without "gold" (and without meta.error)
Deterministic; re-runnable (CPU only):
  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python lean/binj_src/consistency/build.py
"""
from __future__ import annotations

import hashlib
import json
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[1]
OUT = LEAN / "data" / "v11_parts" / "binj"
SEED = 20261102
DOMAIN = "consistency"
N_BASE = 170
N_TWIN = 68          # 40% of base items
NOUL_FRAC = 0.30

CONS = "factually consistent"
INCONS = "factually inconsistent"
DEFS = {
    CONS: ("every statement in the summary or claim is supported by the source text: names, numbers, units, dates, "
           "who did or said what, the direction of any change, how certain or conditional a statement is, and how "
           "broadly it applies all match the source. Rewording, compression, leaving details out, and conclusions "
           "the source directly entails (such as simple arithmetic on its figures) are allowed; nothing may be "
           "added that the source does not state or entail."),
    INCONS: ("at least one statement in the summary or claim is contradicted by the source or cannot be verified "
             "from it, even if it sounds plausible or might be true in the real world. Typical errors: a wrong or "
             "swapped name, number, unit or date; a reversed trend or comparison; a flipped negation; a statement "
             "credited to the wrong person; a hedged, tentative or conditional claim stated as certain; a claim "
             "widened or narrowed in scope (for example 'some' turned into 'all'); an added cause or explanation; "
             "or any detail the source does not contain."),
}

CHOICE_Q = [
    "Is the {obj} factually consistent with the source?",
    "Judge the {obj} against the source text.",
    "How should this {obj} be labeled for factual consistency?",
    "Does the {obj} stay faithful to the facts in the source?",
    "Check the {obj} against the document. Which label applies?",
    "Which label fits the {obj}, going only by what the source says?",
    "A fact-checker compares the {obj} with the source. What should they conclude?",
    "Rate the factual consistency of the {obj} with respect to the source.",
]
YES_Q = {  # yes/no question about one label; gold 1 when that label is correct
    CONS: [
        "Is the {obj} factually consistent with the source?",
        "Is everything the {obj} says supported by the source?",
        "Should this {obj} be labeled factually consistent?",
        "Would a careful fact-checker accept the {obj} as factually consistent with the source text?",
        "Does the {obj} count as factually consistent under the definition?",
        "Can every statement in the {obj} be verified from the source?",
        "Is the {obj} faithful to the source, with nothing contradicted or unsupported?",
    ],
    INCONS: [
        "Is the {obj} factually inconsistent with the source?",
        "Does the {obj} contain anything the source contradicts or does not support?",
        "Should this {obj} be flagged as factually inconsistent?",
        "Would the {obj} be labeled factually inconsistent?",
        "Does the {obj} misstate or go beyond the source in any way?",
        "Is there a factual inconsistency between the {obj} and the source?",
        "Does the {obj} count as factually inconsistent under the definition?",
    ],
}

GENERIC_SRC = ["Source article:", "Source document:", "Document:", "Original text:", "Source:", "Text:"]
SUM_HEAD = {"summary": ["Summary:", "Generated summary:", "Summary to check:", "Model-written summary:", "Summary:"],
            "claim": ["Claim:", "Claim to verify:", "Statement:"]}


def genre_header(genre: str) -> str:
    g = genre.lower()
    if "abstract" in g:
        return "Abstract:"
    if "ticket" in g or "chat" in g:
        return "Support thread:"
    if "meeting" in g or "minutes" in g:
        return "Meeting notes:"
    if "email" in g or "memo" in g:
        return "Email:"
    if "report" in g or "release notes" in g or "postmortem" in g:
        return "Report:"
    if "transcript" in g:
        return "Transcript:"
    return "Article:"


# ------------------------------------------------------------------------------------------------ parsing
def parse(path: Path):
    groups, cur, item = [], None, None
    for raw in path.read_text().split("\n"):
        line = raw.rstrip()
        if line.startswith("# ") and cur is None:
            continue
        if line.startswith("### "):
            key, genre = [x.strip() for x in line[4:].split("|")]
            cur = dict(key=key, genre=genre, src=[], items=[])
            groups.append(cur)
            item = None
            continue
        m = re.match(r"^@@(>?) ([CI]) (\w+)$", line)
        if m:
            twin, lab, tag = m.groups()
            if twin:
                assert item is not None and item["twin"] is None, f"twin without base in {cur['key']}"
                assert lab != item["label"], f"twin must flip the label in {cur['key']}"
                item["twin"] = dict(label=lab, tag=tag, text=[])
                target = item["twin"]
            else:
                item = dict(label=lab, tag=tag, text=[], twin=None)
                cur["items"].append(item)
                target = item
            cur["_target"] = target
            continue
        if cur is None:
            continue
        if "_target" in cur:
            if line.strip():
                cur["_target"]["text"].append(line.strip())
        else:
            cur["src"].append(line)
    for g in groups:
        g.pop("_target", None)
        g["src"] = "\n".join(g["src"]).strip()
        for it in g["items"]:
            it["text"] = " ".join(it["text"])
            if it["twin"]:
                it["twin"]["text"] = " ".join(it["twin"]["text"])
    return groups


def nwords(s: str) -> int:
    return len(re.findall(r"\S+", s))


def call_id(instr, state, options, card):
    blob = json.dumps([instr, state, options, card], ensure_ascii=False)
    return "c_" + hashlib.sha1(blob.encode()).hexdigest()[:12]


def err_group(tag: str) -> str:
    return "number/unit/date" if tag in ("number", "date", "unit") else tag


class Cycler:
    def __init__(self, items, rng):
        self.items, self.rng, self.pool = list(items), rng, []

    def next(self):
        if not self.pool:
            self.pool = list(self.items)
            self.rng.shuffle(self.pool)
        return self.pool.pop()


# ------------------------------------------------------------------------------------------------ build
def main():
    rng = random.Random(SEED)
    groups = []
    for p in sorted(HERE.glob("items*.txt")):
        groups.extend(parse(p))
    keys = [g["key"] for g in groups]
    assert len(keys) == len(set(keys)), "duplicate source keys"
    bases = [(g, it) for g in groups for it in g["items"]]
    assert len(bases) == N_BASE, f"expected {N_BASE} base items, got {len(bases)}"
    lab = Counter(it["label"] for _, it in bases)
    assert lab["C"] == lab["I"] == N_BASE // 2, f"base labels not 50/50: {lab}"

    # ---- twin selection: 34 C->I twins and 34 I->C twins, balancing error types
    base_err = Counter(err_group(it["tag"]) for _, it in bases if it["label"] == "I")
    c2i = [(g, it) for g, it in bases if it["label"] == "C" and it["twin"]]
    i2c = [(g, it) for g, it in bases if it["label"] == "I" and it["twin"]]
    rng.shuffle(c2i)
    rng.shuffle(i2c)
    need = N_TWIN // 2
    assert len(c2i) >= need and len(i2c) >= need, (len(c2i), len(i2c))
    sel = set()
    cnt = Counter(base_err)
    pool = list(c2i)
    for _ in range(need):  # new inconsistent rows: pick the least represented error type
        best = min(pool, key=lambda x: (cnt[err_group(x[1]["twin"]["tag"])], 0))
        pool.remove(best)
        sel.add(id(best[1]))
        cnt[err_group(best[1]["twin"]["tag"])] += 1
    fixc = Counter()
    pool = list(i2c)
    for _ in range(need):  # new consistent rows: spread fixes over the error types they repair
        best = min(pool, key=lambda x: fixc[err_group(x[1]["tag"])])
        pool.remove(best)
        sel.add(id(best[1]))
        fixc[err_group(best[1]["tag"])] += 1

    # ---- per-group framing (shared by a base and its twin)
    frame_of = {}
    for g in groups:
        obj = "claim" if rng.random() < 0.2 else "summary"
        src_h = genre_header(g["genre"]) if rng.random() < 0.5 else rng.choice(GENERIC_SRC)
        sum_h = rng.choice(SUM_HEAD[obj])
        first = "summary" if rng.random() < 0.15 else "source"
        frame_of[g["key"]] = dict(obj=obj, src_h=src_h, sum_h=sum_h, first=first)

    # ---- qtype assignment: 30% noul per label, balanced asked-label
    noul_ids = set()
    for L in ("C", "I"):
        ids = [id(it) for _, it in bases if it["label"] == L]
        rng.shuffle(ids)
        k = round(len(ids) * NOUL_FRAC)
        noul_ids.update(ids[:k])
    ask_cyc = {L: Cycler([CONS, CONS, INCONS, INCONS], random.Random(SEED + ord(L))) for L in ("C", "I")}
    choice_cyc = Cycler(CHOICE_Q, random.Random(SEED + 1))
    yes_cyc = {k: Cycler(v, random.Random(SEED + 2 + i)) for i, (k, v) in enumerate(YES_Q.items())}
    order_cyc = Cycler([0, 1], random.Random(SEED + 9))

    rows, n = [], 0

    def state_for(g, text):
        f = frame_of[g["key"]]
        a = f"{f['src_h']}\n{g['src']}"
        b = f"{f['sum_h']}\n{text}"
        return a + "\n\n" + b if f["first"] == "source" else b + "\n\n" + a

    def make(g, it, twin_of=None, spec=None):
        nonlocal n
        n += 1
        f = frame_of[g["key"]]
        gold_label = CONS if it["label"] == "C" else INCONS
        state = state_for(g, it["text"])
        if spec is None:
            if id(it) in noul_ids:
                asked = ask_cyc[it["label"]].next()
                spec = dict(qtype="noul", asked=asked, instr=yes_cyc[asked].next().format(obj=f["obj"]))
            else:
                opts = [CONS, INCONS] if order_cyc.next() == 0 else [INCONS, CONS]
                spec = dict(qtype="choice", options=opts, instr=choice_cyc.next().format(obj=f["obj"]))
        if spec["qtype"] == "choice":
            options = spec["options"]
            card = "\n".join(f"- {o}: {DEFS[o]}" for o in options)
            gold, role = gold_label, "choice"
        else:
            options = None
            card = f"- {spec['asked']}: {DEFS[spec['asked']]}"
            gold, role = int(spec["asked"] == gold_label), "aff"
        meta = {"domain": DOMAIN, "genre": g["genre"], "frame": f["obj"]}
        if it["label"] == "I":
            meta["error"] = it["tag"]
        if twin_of:
            meta["twin_of"] = twin_of
        row = {
            "id": f"r_binj_{DOMAIN}_{n}",
            "group_id": f"g:binj_{DOMAIN}:{g['key']}",
            "call_id": call_id(spec["instr"], state, options, card),
            "split": "train",
            "track": "BINJ",
            "source": f"binj_{DOMAIN}",
            "state": state,
            "qtype": spec["qtype"],
            "instructions": spec["instr"],
            "options": options,
            "gold": gold,
            "role": role,
            "card": card,
            "meta": meta,
        }
        rows.append(row)
        return row, spec

    for g in groups:
        for it in g["items"]:
            base_row, spec = make(g, it)
            if it["twin"] and id(it) in sel:
                make(g, it["twin"], twin_of=base_row["id"], spec=spec)

    validate(rows, groups)
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / f"{DOMAIN}.jsonl", "w") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(OUT / f"{DOMAIN}.blind.jsonl", "w") as fh:
        for r in rows:
            b = {k: v for k, v in r.items() if k != "gold"}
            b["meta"] = {k: v for k, v in r["meta"].items() if k != "error"}
            fh.write(json.dumps(b, ensure_ascii=False) + "\n")
    report(rows, groups)


# ------------------------------------------------------------------------------------------------ checks
KEYS = ["id", "group_id", "call_id", "split", "track", "source", "state", "qtype", "instructions", "options", "gold",
        "role", "card", "meta"]
LEAK = re.compile(r"\b(in)?consisten(t|cy)\b|\bfaithful\b|\bhallucinat", re.I)


def validate(rows, groups):
    errs = []
    ids = [r["id"] for r in rows]
    cids = [r["call_id"] for r in rows]
    if len(set(ids)) != len(ids):
        errs.append("dup ids")
    if len(set(cids)) != len(cids):
        errs.append("dup call_ids")
    for g in groups:
        w = nwords(g["src"])
        if not 120 <= w <= 400:
            errs.append(f"{g['key']}: source {w} words")
        if LEAK.search(g["src"]):
            errs.append(f"{g['key']}: label word in source")
        for it in g["items"]:
            for t in [it] + ([it["twin"]] if it["twin"] else []):
                if LEAK.search(t["text"]):
                    errs.append(f"{g['key']}: label word in summary")
                s = len(re.findall(r"[.!?](\s|$)", t["text"]))
                if not 1 <= s <= 3:
                    errs.append(f"{g['key']}: summary has {s} sentences")
    for r in rows:
        if list(r) != KEYS:
            errs.append(f"{r['id']}: keys")
        w = nwords(r["state"])
        if not 30 <= w <= 400:
            errs.append(f"{r['id']}: state {w} words")
        lines = [l for l in r["card"].split("\n") if l.strip()]
        if any(not l.startswith("- ") or ": " not in l[2:] for l in lines):
            errs.append(f"{r['id']}: card format")
        if r["qtype"] == "choice":
            if r["role"] != "choice" or r["gold"] not in r["options"] or len(r["options"]) != 2:
                errs.append(f"{r['id']}: choice fields")
            if [l[2:].split(": ")[0] for l in lines] != r["options"]:
                errs.append(f"{r['id']}: card/options order")
        elif r["qtype"] == "noul":
            if r["options"] is not None or r["gold"] not in (0, 1) or isinstance(r["gold"], bool) or r["role"] != "aff":
                errs.append(f"{r['id']}: noul fields")
            if len(lines) != 1:
                errs.append(f"{r['id']}: noul card lines")
        else:
            errs.append(f"{r['id']}: qtype")
    by_id = {r["id"]: r for r in rows}
    for r in rows:
        t = r["meta"].get("twin_of")
        if t:
            b = by_id[t]
            if b["group_id"] != r["group_id"] or b["qtype"] != r["qtype"] or b["instructions"] != r["instructions"]:
                errs.append(f"{r['id']}: twin mismatch")
            if b["gold"] == r["gold"]:
                errs.append(f"{r['id']}: twin does not flip gold")
    if errs:
        print("\n".join(errs))
        sys.exit(1)


def label_of(r):
    if r["qtype"] == "choice":
        return r["gold"]
    asked = r["card"][2:].split(": ")[0]
    return asked if r["gold"] == 1 else (INCONS if asked == CONS else CONS)


def overlap(summary: str, source: str) -> float:
    tok = lambda s: re.findall(r"[a-z0-9]+", s.lower())
    src = set(tok(source))
    t = tok(summary)
    return sum(x in src for x in t) / max(1, len(t))


def report(rows, groups):
    base = [r for r in rows if "twin_of" not in r["meta"]]
    twins = [r for r in rows if "twin_of" in r["meta"]]
    src_of = {g["key"]: g["src"] for g in groups}
    print(f"rows {len(rows)}  base {len(base)}  twins {len(twins)}  sources {len(groups)}")
    for name, rs in [("all", rows), ("base", base), ("twins", twins)]:
        lab = Counter(label_of(r) for r in rs)
        print(f"  {name:5s} labels: {dict(lab)}")
    ch = [r for r in rows if r["qtype"] == "choice"]
    nu = [r for r in rows if r["qtype"] == "noul"]
    print(f"qtype: choice {len(ch)}  noul {len(nu)}  (base: choice {sum(r['qtype']=='choice' for r in base)}, "
          f"noul {sum(r['qtype']=='noul' for r in base)})")
    print(f"choice gold: {dict(Counter(r['gold'] for r in ch))}  gold at position 0: "
          f"{sum(r['options'][0]==r['gold'] for r in ch)}/{len(ch)}")
    print(f"noul gold: {dict(Counter(r['gold'] for r in nu))}  asked label: "
          f"{dict(Counter(r['card'][2:].split(': ')[0] for r in nu))}")
    for asked in (CONS, INCONS):
        sub = [r for r in nu if r["card"][2:].startswith(asked)]
        print(f"  asked {asked}: yes {sum(r['gold'] for r in sub)}/{len(sub)}; "
              f"phrasings {len(set(r['instructions'] for r in sub))}")
    print(f"choice phrasings: {len(set(r['instructions'] for r in ch))}")
    errs = Counter(r["meta"]["error"] for r in rows if "error" in r["meta"])
    print(f"error types (inconsistent rows): {dict(sorted(errs.items(), key=lambda x: -x[1]))}")
    print(f"frames: {dict(Counter(r['meta']['frame'] for r in rows))}")
    sw = [nwords(g["src"]) for g in groups]
    stw = [nwords(r["state"]) for r in rows]
    print(f"source words min/med/max {min(sw)}/{sorted(sw)[len(sw)//2]}/{max(sw)}; "
          f"state words min/med/max {min(stw)}/{sorted(stw)[len(stw)//2]}/{max(stw)}")
    ov = defaultdict(list)
    for r in rows:
        key = r["group_id"].split(":")[-1]
        m = re.search(r"\n\n(" + "|".join(re.escape(h) for hs in SUM_HEAD.values() for h in hs) + r")\n(.*)$",
                      r["state"], re.S)
        summ = m.group(2) if m else r["state"].split("\n")[1]
        ov[label_of(r)].append(overlap(summ, src_of[key]))
    for k, v in ov.items():
        print(f"  mean summary-token overlap with source, {k}: {sum(v)/len(v):.3f}")
    print(f"genres: {len(set(r['meta']['genre'] for r in rows))}")


if __name__ == "__main__":
    main()
