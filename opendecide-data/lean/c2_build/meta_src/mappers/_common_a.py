"""_common_a.py: shared machinery of the group-A metadata mappers (A42-D 8; openalex, musicbrainz, worldbank, usgs).

A TASK is one question template x one field mapping (a threshold, a category value, a bucket scheme). Its gold is a
program function of upstream metadata fields shown in the state; Haiku and Claude never label. Rows follow the G-block
convention (id, group_id, domain, card_id, state, instructions, qtype, options, card) plus the C2 fields (source, gold,
role, meta.source / task_id / domain / card_id / twin_of / twin_kind / licence / c2).

Design rules (all by construction):
  - yes/no heads (qtype "noul", gold 1/0) and choice heads (qtype "choice", gold = option text); no abstain option;
  - per-task yes share drawn from 0.40-0.60, records sampled per class so each task is balanced, choice gold classes
    stratified, gold position planned (i mod k) for unordered sets, natural order for ordinal bucket sets;
  - A43 (f): every wording passes c2_kit.polarity.problems (no contracted negative frame, no negation over a negative
    predicate, declared polarity = read polarity); no negated frame over a negated proposition is ever generated;
  - complement twins (A42-D 7): about 12% of the yes/no base rows of a task with both polarities get a twin on the same
    state with the opposite-polarity wording and gold 1 - gold (meta.twin_of, meta.twin_kind = "complement");
  - card-free rows (card is null) carry a self-contained question; carded rows put the rule text in `card`;
  - one row per record where supply allows (global used count), no (instructions, state) duplicate.
"""
from __future__ import annotations

import hashlib
import json
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

BUILD = Path(__file__).resolve().parents[2]
if str(BUILD) not in sys.path:
    sys.path.insert(0, str(BUILD))
from c2_kit import polarity  # noqa: E402  (read-only)

SEED = 20261013
NEGS = [r"fewer", r"less", r"below", r"before", r"earlier than", r"lacks?", r"lacking",
        r"without", r"shallower than", r"smaller", r"lower than", r"younger than", r"weaker than", r"shorter than"]
STYLES = ["kv", "json", "yaml", "table", "bullets", "inline"]


def h(*a) -> int:
    return int(hashlib.sha256("|".join(map(str, a)).encode()).hexdigest()[:16], 16)


def rng(*a) -> random.Random:
    return random.Random(h(SEED, *a))


class Task:
    """kind "yn": pred(rec) -> bool, pos / neg wording lists (neg may be empty), fmt dict for {slots}.
    kind "ch": label(rec) -> option text, options (all classes), q wordings, ordered (bucket scheme in natural order),
    k (options shown when unordered)."""

    def __init__(self, tid, kind, need, *, pred=None, label=None, pos=(), neg=(), q=(), fmt=None, card=None,
                 options=None, ordered=False, k=4, elig=None, n=None, extras=3, why=""):
        self.tid, self.kind, self.need = tid, kind, list(need)
        self.pred, self.label = pred, label
        self.pos, self.neg, self.q = list(pos), list(neg), list(q)
        self.fmt, self.card, self.options = fmt or {}, card, options
        self.ordered, self.k, self.elig, self.n, self.extras, self.why = ordered, k, elig, n, extras, why

    def wording_texts(self):
        out = []
        for pol, lst in ((1, self.pos), (-1, self.neg)):
            for w in lst:
                out.append((pol, w.format(**self.fmt)))
        return out


def render_state(style, header, items, r):
    """items: [(key, label, value)] in display order."""
    if style == "kv":
        body = "\n".join(f"{lab}: {val}" for _, lab, val in items)
    elif style == "json":
        body = "{\n" + ",\n".join(f'  "{k}": {json.dumps(v) if not re.fullmatch(r"-?\d+(\.\d+)?", v) else v}'
                                  for k, _, v in items) + "\n}"
    elif style == "yaml":
        body = "\n".join(f"{k}: {v}" for k, _, v in items)
    elif style == "table":
        body = "| Field | Value |\n| --- | --- |\n" + "\n".join(f"| {lab} | {val} |" for _, lab, val in items)
    elif style == "bullets":
        body = "\n".join(f"- {lab} = {val}" for _, lab, val in items)
    else:
        body = "; ".join(f"{lab} {val}" for _, lab, val in items) + "."
    return f"{header}\n{body}"


def build_source(src, *, domain, licence, licence_url=None, dataset_url=None, headers, recs, rid_of, fields_of, group_of, tasks, seed_tag, per_task=(10, 15), ch_range=(22, 30),
                 twin_share=0.12):
    """Returns (rows, relations, report). recs: list of raw records; fields_of(rec) -> {key: (label, value or None)}."""
    used = Counter()
    rows, rels, rep = [], [], {"dropped_tasks": [], "task_rows": {}}
    seen_sig = set()
    flds = {rid_of(r): fields_of(r) for r in recs}
    for ti, t in enumerate(tasks):
        R = rng(src, t.tid, seed_tag)
        n_t = t.n or (R.randint(*ch_range) if t.kind == 'ch' else R.randint(*per_task))
        elig = [r for r in recs if all(flds[rid_of(r)].get(k) and flds[rid_of(r)][k][1] is not None for k in t.need)
                and (t.elig(r) if t.elig else True)]
        chosen = []  # (rec, gold_value)
        if t.kind == "yn":
            yes = [r for r in elig if t.pred(r)]
            no = [r for r in elig if not t.pred(r)]
            share = R.choice([0.4, 0.44, 0.48, 0.5, 0.5, 0.52, 0.56, 0.6])
            ny = min(int(round(n_t * share)), len(yes))
            nn = min(n_t - int(round(n_t * share)), len(no))
            if min(len(yes), len(no)) < 8:
                rep["dropped_tasks"].append((t.tid, f"pools yes={len(yes)} no={len(no)}"))
                continue
            for pool, m, g in ((yes, ny, 1), (no, nn, 0)):
                pool = sorted(pool, key=lambda r: (used[rid_of(r)], h(seed_tag, t.tid, rid_of(r))))[:m]
                chosen += [(r, g) for r in pool]
        else:
            by = defaultdict(list)
            for r in elig:
                by[t.label(r)].append(r)
            classes = [c for c in (t.options or sorted(by)) if len(by.get(c, [])) >= 3]
            if len(classes) < 3:
                rep["dropped_tasks"].append((t.tid, f"classes {dict((c, len(v)) for c, v in by.items())}"))
                continue
            per = max(3, n_t // len(classes))
            for c in classes:
                pool = sorted(by[c], key=lambda r: (used[rid_of(r)], h(seed_tag, t.tid, rid_of(r))))[:per]
                chosen += [(r, c) for r in pool]
        order = sorted(range(len(chosen)), key=lambda i: h(seed_tag, t.tid, "ord", rid_of(chosen[i][0])))
        chosen = [chosen[i] for i in order]
        cls_all = [c for c in (t.options or []) if True]
        n_twin_budget = int(round(twin_share * len(chosen))) if (t.kind == "yn" and t.pos and t.neg) else 0
        twins_done = 0
        task_rows = 0
        for i, (r, g) in enumerate(chosen):
            rid = rid_of(r)
            F = flds[rid]
            RR = rng(src, t.tid, rid, "row")
            pool = [k for k in F if k not in t.need and F[k][1] is not None and group_of(k) not in {group_of(x) for x in t.need}]
            ex = RR.sample(pool, min(t.extras + RR.randint(0, 1), len(pool)))
            keys = sorted(set(t.need) | set(ex), key=lambda k: list(F).index(k))
            if RR.random() < 0.5:
                RR.shuffle(keys)
            items = [(k, F[k][0], F[k][1]) for k in keys]
            style = STYLES[h(seed_tag, t.tid, rid, "style") % len(STYLES)]
            state = render_state(style, RR.choice(headers), items, r)
            base = {"source": src, "domain": domain}
            if t.kind == "yn":
                pol = 1 if (not t.neg or RR.random() < 0.8) else -1
                lst = t.pos if pol == 1 else t.neg
                wi = RR.randrange(len(lst))
                text = lst[wi].format(**t.fmt)
                gold = g if pol == 1 else 1 - g
                instr, qtype, opts = text, "noul", None
            else:
                wi = RR.randrange(len(t.q))
                instr, qtype = t.q[wi].format(**t.fmt), "choice"
                if t.ordered:
                    opts = list(t.options)
                else:
                    others = [c for c in t.options if c != g]
                    RR.shuffle(others)
                    k = min(t.k, len(t.options))
                    opts = others[:k - 1]
                    opts.insert(i % k, g)
                gold, pol = g, 0
            sig = (instr, state)
            if sig in seen_sig:
                continue
            seen_sig.add(sig)
            used[rid] += 1
            rowid = f"c2_md:{src}:{h(seed_tag, t.tid, rid) % (16 ** 12):012x}"
            t.full = f"{src}:{t.tid}"
            meta = {"family": "MD", "source": src, "task_id": t.full, "domain": domain, "card_id": t.full if t.card else None,
                    "gold_field": ",".join(t.need), "gold_method": "upstream_metadata_program", "record_id": rid,
                    "licence": licence, "licence_url": licence_url, "dataset_url": dataset_url,
                    "gen_version": "c2-md-mappers 1.0 (15 Oct 2026, group A)", "seed": SEED,
                    "twin_of": None, "twin_kind": None, "upstream_id": rid, "style": style,
                    "polarity": pol, "wording_idx": wi, "gold_basis": t.why,
                    "c2": {"author_mode": "T", "skin_id": f"md-{style}", "register": style,
                           "lexicon_ids": [f"{t.tid}#w{wi}"], "haiku_task_id": None, "haiku_prompt_sha": None,
                           "twin_kind": None, "twin_of": None, "closed_world": True}}
            row = {"id": rowid, "group_id": rowid, "call_id": rowid, "source": src, "domain": domain, "card_id": meta["card_id"],
                   "state": state, "instructions": instr, "qtype": qtype, "options": opts, "gold": gold,
                   "role": "base", "card": t.card or "", "meta": meta}
            rows.append(row)
            task_rows += 1
            if twins_done < n_twin_budget and RR.random() < min(1.0, 1.6 * twin_share):
                lst2 = t.neg if pol == 1 else t.pos
                wi2 = RR.randrange(len(lst2))
                text2 = lst2[wi2].format(**t.fmt)
                tid2 = f"c2_md:{src}:{h(seed_tag, t.tid, rid, 'tw') % (16 ** 12):012x}"
                m2 = json.loads(json.dumps(meta))
                m2.update({"twin_of": rowid, "twin_kind": "complement", "polarity": -pol, "wording_idx": wi2})
                m2["c2"].update({"twin_of": rowid, "twin_kind": "complement", "lexicon_ids": [f"{t.tid}#w{wi2}" + ("n" if pol == 1 else "p")]})
                row2 = dict(row, id=tid2, group_id=rowid, instructions=text2, gold=1 - gold, role="twin", meta=m2)
                rows.append(row2)
                rels.append({"a": rowid, "b": tid2, "type": "complement"})
                twins_done += 1
                task_rows += 1
        rep["task_rows"][t.tid] = task_rows
    return rows, rels, rep


def check_wordings(tasks):
    probs = []
    for t in tasks:
        for pol, txt in t.wording_texts():
            for p in polarity.problems(txt, pol, negatives=NEGS):
                probs.append((t.tid, txt, p))
        if t.kind == "ch":
            for w in t.q:
                txt = w.format(**t.fmt)
                if re.search(r"\b(not|n't|never)\b", txt, re.I):
                    probs.append((t.tid, txt, "choice wording negated"))
    return probs


def audit(rows, rels, tasks, rep):
    """Source-level checks reported in the MANIFEST (bars of A42-D 8.2 and the by-construction rules)."""
    n = len(rows)
    base = [r for r in rows if r["role"] == "base"]
    yn = [r for r in rows if r["qtype"] == "noul"]
    ch = [r for r in rows if r["qtype"] == "choice"]
    per_task = Counter(r["meta"]["task_id"] for r in rows)
    out = {"rows": n, "base": len(base), "twins": n - len(base), "tasks": len(per_task),
           "tasks_range_ok": 40 <= len(per_task) <= 80, "max_rows_per_task": max(per_task.values()),
           "card_free_share": round(sum(1 for r in rows if not r["card"]) / n, 4),
           "yes_no_share": round(len(yn) / n, 4),
           "yes_share": round(sum(r["gold"] for r in yn) / max(1, len(yn)), 4),
           "polarity_neg_share": round(sum(1 for r in yn if r["meta"]["polarity"] == -1) / max(1, len(yn)), 4)}
    ys = defaultdict(list)
    for r in yn:
        ys[r["meta"]["task_id"]].append(r["gold"])
    out["task_yes_share_range"] = [round(min(sum(v) / len(v) for v in ys.values()), 3), round(max(sum(v) / len(v) for v in ys.values()), 3)]
    pos = Counter()
    for r in ch:
        pos[r["options"].index(r["gold"])] += 1
    out["choice_gold_position"] = dict(sorted(pos.items()))
    out["choice_gold_strictly_longest_share"] = round(sum(1 for r in ch if sorted((len(o) for o in r["options"]), reverse=True)[0] == len(r["gold"]) and sum(1 for o in r["options"] if len(o) == len(r["gold"])) == 1) / max(1, len(ch)), 3) if ch else None
    out["choice_mean_k"] = round(sum(len(r["options"]) for r in ch) / max(1, len(ch)), 2) if ch else None
    # twin exactness (program): twin gold = 1 - base gold, same state
    byid = {r["id"]: r for r in rows}
    bad = [r["id"] for r in rows if r["role"] == "twin" and (byid[r["meta"]["twin_of"]]["gold"] != 1 - r["gold"] or byid[r["meta"]["twin_of"]]["state"] != r["state"])]
    out["twin_violations"] = len(bad)
    ids = [r["id"] for r in rows]
    out["id_duplicates"] = len(ids) - len(set(ids))
    out["state_instruction_duplicates"] = n - len({(r["instructions"], r["state"]) for r in rows})
    out["records_used_more_than_once"] = sum(1 for c in Counter(r["meta"]["upstream_id"] for r in base).values() if c > 1)
    out["dropped_tasks"] = rep["dropped_tasks"]
    return out


# ---------------------------------------------------------------------------------------------- wording sets / factories
COUNT_POS = ["Is the number of {things} {n} or more?", "Does the record show at least {n} {things}?",
             "Is the {thing} count at least {n}?", "Does the entry list {n} or more {things}?"]
COUNT_NEG = ["Is the number of {things} fewer than {n}?", "Does the record show fewer than {n} {things}?",
             "Is the {thing} count below {n}?", "Does the entry list fewer than {n} {things}?"]
YEAR_POS = ["Was it {verb} in {n} or later?", "Is the {what} year {n} or later?", "Does the {what} year fall in {n} or after?"]
YEAR_NEG = ["Was it {verb} before {n}?", "Is the {what} year earlier than {n}?", "Does the {what} year fall before {n}?"]
EQ_POS = ["Is the {what} '{v}'?", "Is the recorded {what} {v}?", "Does the record give '{v}' as the {what}?"]
EQ_NEG = ["Is it true that the {what} is not '{v}'?", "Is it true that the record does not give '{v}' as the {what}?"]
HAS_POS = ["Does the record include {what}?", "Is {what} recorded for this entry?", "Does this entry carry {what}?"]
HAS_NEG = ["Is it true that the record has no {what}?", "Is it true that no {what} is recorded for this entry?"]
CONCEPT_POS = ["Does this entry count as {c} under the card?", "Under the card, is this entry {c}?", "Is this entry {c} by the card's rule?"]
CONCEPT_NEG = ["Is it true that this entry does not count as {c} under the card?",
               "Is it true that the card's rule does not make this entry {c}?"]
CHOICE_Q = ["Which {what} applies to this entry?", "Which {what} does this entry fall in?", "Pick the {what} for this entry."]


def ge_task(tid, need, get, thr, pos=None, neg=None, fmt=None, card=None, elig=None, why="", n=None):
    return Task(tid, "yn", need, pred=lambda r, g=get, t=thr: g(r) >= t, pos=pos or COUNT_POS, neg=neg or COUNT_NEG,
                fmt=dict(fmt or {}, n=thr), card=card, elig=elig, why=why or f">= {thr}", n=n)


def eq_task(tid, need, get, val, what, fmt=None, card=None, elig=None, why="", pos=None, neg=None, n=None):
    return Task(tid, "yn", need, pred=lambda r, g=get, v=val: g(r) == v, pos=pos or EQ_POS, neg=neg or EQ_NEG,
                fmt=dict(fmt or {}, v=val, what=what), card=card, elig=elig, why=why or f"== {val}", n=n)


def bool_task(tid, need, pred, what_pos, pos, neg, fmt=None, card=None, elig=None, why="", n=None):
    return Task(tid, "yn", need, pred=pred, pos=pos, neg=neg, fmt=fmt or {}, card=card, elig=elig, why=why, n=n)


def concept_task(tid, need, pred, concept, card, elig=None, why="", fmt=None, n=None):
    return Task(tid, "yn", need, pred=pred, pos=CONCEPT_POS, neg=CONCEPT_NEG, fmt=dict(fmt or {}, c=concept),
                card=card, elig=elig, why=why, n=n)


def yn_card(yes_rule, no_rule):
    return f"- yes: Yes if {yes_rule}.\n- no: No if {no_rule}."


def ch_card(defs):
    return "\n".join(f"- {k}: {v}" for k, v in defs)


def bucket_task(tid, need, label, options, what, defs=None, card=None, elig=None, why="", ordered=True, k=4, n=None, q=None, fmt=None):
    card = card if card is not None else (ch_card(defs) if defs else None)
    return Task(tid, "ch", need, label=label, options=list(options), ordered=ordered, k=k, q=q or CHOICE_Q,
                fmt=dict(fmt or {}, what=what), card=card, elig=elig, why=why, n=n)


def write_source(name, outdir, rows, rels, tasks, rep, extra_manifest):
    """rows.jsonl, relations.jsonl, MANIFEST.json, tasks.json, noise-gate task files (13 seeded rows per task)."""
    outdir.mkdir(parents=True, exist_ok=True)

    def dump(p, objs):
        with open(p, "w") as f:
            for o in objs:
                f.write(json.dumps(o, ensure_ascii=False, sort_keys=True) + "\n")
    dump(outdir / "rows.jsonl", rows)
    dump(outdir / "relations.jsonl", rels)
    by = defaultdict(list)
    for r in rows:
        by[r["meta"]["task_id"]].append(r)
    tinfo = []
    for t in tasks:
        if getattr(t, 'full', None) in by:
            tinfo.append({"task_id": t.full, "kind": t.kind, "need": t.need, "gold_basis": t.why, "carded": bool(t.card),
                          "rows": len(by[t.full]), "n_wordings": len(t.pos) + len(t.neg) + len(t.q)})
    (outdir / "tasks.json").write_text(json.dumps(tinfo, indent=1))
    # noise gate: seeded 13 base-or-twin rows per task, blind items (gold-free) via the TEACH-0 chunker
    from c2_kit import chunker, g5h
    items, pick = [], {}
    for tid, rr in sorted(by.items()):
        sel = sorted(rr, key=lambda r: h("noise13", name, r["id"]))[:13]
        for r in sel:
            items.append((r["id"], g5h.read_item(r)))
            pick.setdefault(tid, []).append(r["id"])
    prompt = NOISE_PROMPT
    b = chunker.make_batch("blind_read", f"MD_{name}", items, seed=f"noise13-{name}", prompt=prompt)
    import shutil
    ng, orch = outdir / "noise_gate", outdir / "noise_gate_orch"
    for d in (ng, orch):
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)
    for rel, text in b.files().items():
        p = (orch if rel.startswith(("key/", "manifest/")) else ng) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text if isinstance(text, str) else json.dumps(text))
    (ng / "answers").mkdir()
    (orch / "SEEDED_PICK.json").write_text(json.dumps(pick))
    import hashlib as _h
    man = {"source": name, "rule": "A42-D 8.4: 13 seeded rows per task, blind Haiku read; a task is dropped if >= 2 of 13 are clearly wrong "
           "(Haiku disagrees with gold AND the Sonnet/Opus check confirms wrong or ambiguous; rows are never edited)",
           "files": {n: {"sha256": _h.sha256((outdir / n).read_bytes()).hexdigest(), "rows": sum(1 for _ in open(outdir / n))}
                     for n in ("rows.jsonl", "relations.jsonl")},
           "noise_gate": {"items": len(items), "tasks": len(pick), "rows_per_task": 13, "haiku_dir": str(ng), "orchestrator_dir": str(orch), "chunks": len(b.chunks), "batch_id": b.batch_id, "prompt_sha": b.prompt_sha, "answers_go_to": str(ng / "answers")},
           "audit": audit(rows, rels, tasks, rep)}
    man.update(extra_manifest)
    (outdir / "MANIFEST.json").write_text(json.dumps(man, indent=1))
    return man


NOISE_PROMPT = ("You are given a chunk of up to 50 items. Each item has a record (text), a question, optional options and optional "
                "definitions. Answer every item from the record and the definitions only: for yes/no items answer yes or no; "
                "for choice items answer with the option text exactly as written. Do not use outside knowledge. If the record "
                "does not settle the question, answer with your best reading and add a short note. Write your answers to the "
                "answer file named in the task, as a JSON object mapping each task id to {\"answer\": ...}.")
