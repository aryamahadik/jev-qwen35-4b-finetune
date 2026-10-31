"""c2_kit/g5h.py: G5-H, two blind Haiku reads + Claude adjudication (C2_DATA_SPEC 6.3 G5 -> G5-H; A37 e).

Design (spec 6.3; bar unchanged from round 1):
  - Two independent Haiku blind solvers read the same 300 rows per family (400 for T32): make_reads() builds two
    batches with different seeds, so the two readers see different orders, opaque ids and chunk splits. The
    orchestrator gives the two batches to different agents. Free-form (Mode F) rows also get one Haiku read of 100%
    of them (make_freeform_read()).
  - Readers see exactly what the model sees: text, question, options, definitions. Never gold, never meta.
  - score(): every row where a reader disagrees with gold (or gave no valid answer) goes to the Claude adjudication
    queue, plus 30 seeded rows where both readers agreed with gold (controls). The adjudicator gets queue and controls
    mixed, with opaque ids (adjudication_items()), and flags each row: gold_ok / wrong_gold / ambiguous.
    Adjudication only flags: rows are never relabelled.
  - Template rule: a skin or wording whose rows disagree with gold on > 3% of its read rows is quarantined.
  - finalize(): PASS iff every queued and control row is adjudicated, 0 confirmed wrong golds and ambiguous <= 1% of
    the rows read. A confirmed wrong gold is a generator bug (fix the generator, regenerate; never patch rows).
    Ambiguous rows and every row of a quarantined template are dropped.
"""
from __future__ import annotations

import re

from . import chunker
from .distractors import uhash

N_READ = {"T32": 400}
N_READ_DEFAULT = 300
N_CONTROL = 30
QUARANTINE_ABOVE = 0.03
AMBIGUOUS_MAX = 0.01
VERDICTS = ("gold_ok", "wrong_gold", "ambiguous")


def n_read(family: str) -> int:
    return N_READ.get(family, N_READ_DEFAULT)


def read_item(row: dict) -> dict:
    it = {"kind": "yes/no" if row["qtype"] == "noul" else "choice", "text": row["state"],
          "question": row["instructions"]}
    if row["qtype"] == "choice":
        it["options"] = list(row["options"])
    if row.get("card"):
        it["definitions"] = row["card"]
    return it


def sample_rows(rows: list, n: int, seed: str) -> list:
    return sorted(rows, key=lambda r: uhash(seed, "g5h", r["id"]))[:n]


def make_reads(rows: list, family: str, *, seed: str, prompt: str) -> tuple:
    items = [(r["id"], read_item(r)) for r in rows]
    a = chunker.make_batch("blind_read", family, items, seed=f"{seed}|reader-A", prompt=prompt)
    b = chunker.make_batch("blind_read", family, items, seed=f"{seed}|reader-B", prompt=prompt)
    return a, b


def make_freeform_read(rows: list, family: str, *, seed: str, prompt: str):
    ff = [r for r in rows if r["meta"]["c2"]["author_mode"] == "F"]
    return chunker.make_batch("blind_read", family, [(r["id"], read_item(r)) for r in ff], seed=f"{seed}|ff",
                              prompt=prompt)


def normalize_answer(item: dict, ans):
    """1 / 0 for yes/no items, the option text for choice items, None when the answer is not valid."""
    if isinstance(ans, dict):
        ans = ans.get("answer")
    if not isinstance(ans, str):
        return None
    a = ans.strip()
    if item["kind"] == "yes/no":
        w = re.sub(r"[^a-z]", "", a.lower())
        return {"yes": 1, "no": 0}.get(w)
    opts = item["options"]
    if a in opts:
        return a
    hits = [o for o in opts if o.casefold() == a.casefold()]
    if len(hits) == 1:
        return hits[0]
    m = re.fullmatch(r"\(?([A-Ia-i])[).:]?", a)
    if m:
        i = ord(m.group(1).upper()) - 65
        return opts[i] if i < len(opts) else None
    return None


def _templates(row: dict) -> list:
    out = [row["meta"]["c2"]["skin_id"]]
    if row["meta"].get("wording_id"):
        out.append(row["meta"]["wording_id"])
    return out


def score(rows: list, items: dict, answers_a: dict, answers_b: dict | None = None, *, seed: str,
          n_control: int = N_CONTROL, template_of=_templates) -> dict:
    """rows: the read rows; items: {row id: item as read} (chunker.item_by_internal); answers_*: {row id: raw}."""
    per, queue, agreed, tpl = {}, [], [], {}
    for r in rows:
        rid, it = r["id"], items[r["id"]]
        gold = r["gold"]
        reads = [normalize_answer(it, answers_a.get(rid))]
        if answers_b is not None:
            reads.append(normalize_answer(it, answers_b.get(rid)))
        ok = [x is not None and x == gold for x in reads]
        per[rid] = {"reads": reads, "agree_gold": ok}
        bad = not all(ok)
        (queue if bad else agreed).append(rid)
        for t in template_of(r):
            d = tpl.setdefault(t, {"n": 0, "disagree": 0})
            d["n"] += 1
            d["disagree"] += bad
    for d in tpl.values():
        d["rate"] = d["disagree"] / d["n"]
    control = sorted(agreed, key=lambda i: uhash(seed, "control", i))[:n_control]
    quarantined = sorted(t for t, d in tpl.items() if d["rate"] > QUARANTINE_ABOVE)
    return {"gate": "G5-H", "n_read": len(rows), "readers": 1 if answers_b is None else 2, "per_row": per,
            "queue": queue, "control": control, "templates": tpl, "quarantined": quarantined}


def adjudication_items(rows_by_id: dict, result: dict, *, seed: str) -> tuple:
    """([(aid, item)], key {aid: row id}): queue and controls mixed and shuffled; the adjudicator sees the program's
    answer (it flags gold) but not which rows the readers disputed."""
    ids = sorted(set(result["queue"]) | set(result["control"]), key=lambda i: uhash(seed, "adj", i))
    out, key = [], {}
    for n, rid in enumerate(ids):
        r = rows_by_id[rid]
        it = read_item(r)
        it["program_answer"] = ("yes" if r["gold"] == 1 else "no") if r["qtype"] == "noul" else r["gold"]
        aid = f"a{n:04d}"
        key[aid] = rid
        out.append((aid, it))
    return out, key


def finalize(rows_by_id: dict, result: dict, verdicts: dict) -> dict:
    """verdicts: {row id: gold_ok | wrong_gold | ambiguous} (Claude, flag only)."""
    need = set(result["queue"]) | set(result["control"])
    missing = sorted(need - set(verdicts))
    bad_v = sorted(i for i, v in verdicts.items() if v not in VERDICTS)
    wrong = sorted(i for i, v in verdicts.items() if v == "wrong_gold")
    amb = sorted(i for i, v in verdicts.items() if v == "ambiguous")
    rate = len(amb) / result["n_read"] if result["n_read"] else 0.0
    q = set(result["quarantined"])
    drop = sorted(set(amb) | {rid for rid, r in rows_by_id.items() if q & set(_templates(r))})
    ok = not missing and not bad_v and not wrong and rate <= AMBIGUOUS_MAX
    return {"gate": "G5-H", "pass": ok, "n_read": result["n_read"], "queued": len(result["queue"]),
            "controls": len(result["control"]), "missing_verdicts": missing, "invalid_verdicts": bad_v,
            "wrong_gold": wrong, "generator_bug": bool(wrong), "ambiguous": amb, "ambiguous_rate": rate,
            "bar": {"wrong_gold": 0, "ambiguous_max": AMBIGUOUS_MAX, "quarantine_above": QUARANTINE_ABOVE},
            "quarantined_templates": sorted(q), "drop_rows": drop}
