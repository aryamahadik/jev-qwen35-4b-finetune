"""t37b/builder.py: the T37b partner builder (C2_DATA_SPEC 3.18, 4.2; G0_LITE_T37B.md v2 + G0_LITE_T37B_A1.md; A37 b, f).

Flow for one block (train: 1,400 complements + 600 equiv; dev: 300 complements on gate-dev rows, held-out frames):
  0. pool = author_pool.load_pool()                                                the frozen, admitted equiv paraphrase
                                                                                    pool (Haiku-written slot templates)
  1. bases, rep = select.eligible(pool_rows, pool_rels, old_ids=..., ...)        program; counts every drop
  2. plan, rep = select.plan_block(bases, equiv_pool=pool.choices(), ...)         kinds, frames, cues, antonym pairs and
                                                                                    paraphrases never read the gold; it
                                                                                    only balances which bases enter (A1-5)
  3. cands = build_candidates(plan, records=pool.records)                         every partner is written by the
     program (syntactic / implicit from program A's strings, antonym / option framing from the closed lists, equiv by
     filling the pool template); polarity programs A and B must both return the planned relation
  4. pol_a, pol_b = polarity_batches(cands, seed=..., judged=pool.judged)         2 independent Haiku judgements per
                                                                                    distinct question pair not yet read
     blind_base, blind_partner = blind_batches(cands, seed=...)                    blind Haiku solver, base and partner
                                                                                    in separate batches
  5. decide(cand, *polarity_of(...), ...) -> keep / drop / review; review_items(...) go to Claude; any doubt drops
                                                                                    (a blind base answer against the human
                                                                                    gold drops the unit, A1-1)
  6. rows, rels, report = finalize(kept, token_fn=...)                             partner rows + relation edges; a row
                                                                                    over 2,000 tokens drops its unit (A1-6);
                                                                                    trim_block keeps the floors / caps
  7. write_block(...) / write_dev(...)                                             refuse before A38 (paths guard) and
                                                                                    while g0_problems() is non-empty
Gold: complement = 1 - base gold, equiv = base gold. Haiku only writes paraphrase templates (pool) or flags: a
disagreement drops the pair, never relabels it (A37 b). The tests run every step in memory with stand-in answers.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

_C2_BUILD = Path(__file__).resolve().parents[1]
if str(_C2_BUILD) not in sys.path:
    sys.path.insert(0, str(_C2_BUILD))

from c2_kit import chunker, g5h, paths  # noqa: E402
from c2_kit import rows as R  # noqa: E402
from c2_kit.distractors import uhash  # noqa: E402
from t37b import polarity as PA  # noqa: E402
from t37b import polarity_b as PB  # noqa: E402
from t37b import select as SEL  # noqa: E402
from t37b import sources as SRC  # noqa: E402

HERE = Path(__file__).resolve().parent
FAMILY = "T37b"
SOURCE = "c2_t37b"
G0_LITE = HERE / "G0_LITE_T37B.md"
G0_SHA256 = "9733b721fcab18c1bbfaf15567d99e6a52433fd7918c221963a8b3eb46da9cd4"   # frozen G0_LITE_T37B.md v2
G0_HAIKU_TASK = "c2-data-stage-a/amb:t37b"      # the one blind Haiku ambiguity pass (61 points; G0 section 5)
G0_HAIKU_POINTS = HERE / "haiku" / "ambiguity" / "amb_t37b_points.json"
# G0 v3 = G0 v2 (the frozen page above, untouched; the Haiku pool and every Haiku task record are bound to its sha) +
# Amendment 1 (14 Oct 2026, the fixes of the stage-B pilot verdict; spec 6.4 step 6). Neither file may change.
G0_AMENDMENT = HERE / "G0_LITE_T37B_A1.md"
G0_AMENDMENT_SHA256 = "05fe8a3843bdb85bb1e0ab5a5016e3c8cd28ca5960c8d6bec05c4a20c45d179d"   # set when the amendment text is final
GEN_VERSION = "t37b builder 2.1 (14 Oct 2026)"
HAIKU_KINDS = ("equiv",)                         # Haiku-written wording (pool templates; author_pool.py)
PROGRAM_KINDS = ("syntactic", "implicit", "antonym", "option_framing")
# Known dev / eval negation frames named in the specs (C_DATA_SPEC 3 F5 note, v14 near-miss template): a partner that
# hits one is dropped here; the full G13 method-8 check (dev_negwords, dev dneg frames, F5 probe templates) runs on
# template_strings() seed-first and on the candidates, through c_build/decontam_g13.py (never read by this module).
LOCAL_BANS = (r"\bbe rejected\b", r"\bIs it wrong to answer\b", r"\bonly non-", r"\bShould the statement that\b",
              r"\bIs the correct answer\b")

POLARITY_PROMPT = (
    "Each item holds two yes/no questions, question_a and question_b, that will be asked about the same text with "
    "the same definitions. Reply 'same' if a correct yes to question_a always goes with a correct yes to question_b "
    "and a correct no with a correct no; 'opposite' if a correct yes to one always goes with a correct no to the "
    "other; 'unclear' if neither holds for certain or a question is ungrammatical. Reply with JSON: a list of objects "
    "{\"qid\": <qid>, \"relation\": \"same\" | \"opposite\" | \"unclear\"}.")
BLIND_PROMPT = (
    "Each item is a text, a yes/no question and the definitions of yes and no for that question. Read the text and "
    "answer the question by the definitions. Reply with JSON: a list of objects {\"qid\": <qid>, \"answer\": "
    "\"yes\" | \"no\"}.")


def sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def relation_of(kind: str) -> str:
    return "opposite" if kind in SRC.OPPOSITE_KINDS else "same"


# ------------------------------------------------------------------------------------------------ partners (program)

def _surface(item, options) -> str | None:
    """One of program A's strings, picked label-blind by a hash of the plan id (G0 H16)."""
    opts = sorted(options)
    return opts[min(len(opts) - 1, int(uhash("t37b-surface", item.pid) * len(opts)))] if opts else None


def program_partner(item) -> str | None:
    """Every T37b partner is written by the program (G0 S12, H40): syntactic and implicit from program A's exact
    strings, antonym and option framing from the closed lists, equiv by filling the admitted pool template."""
    q = item.base.row["instructions"]
    e = item.base.entry
    if item.kind == "syntactic":
        return _surface(item, PA.syntactic_targets(q, e, item.frame)) if item.frame else None
    if item.kind == "implicit":
        ts = PA.implicit_targets(q, e)
        if item.cue not in SRC.IMPLICIT_CUES:
            return None
        return _surface(item, [t for t in ts if (" fail to " in t) == (item.cue == "fail to")])
    if item.kind == "antonym":
        if item.variant is None:
            return None
        p, a = e.antonyms[item.variant]
        rx = re.compile(r"(?<![\w-])" + re.escape(p) + r"(?![\w-])")
        return rx.sub(a, q) if len(rx.findall(q)) == 1 else None
    if item.kind == "option_framing":
        rx, fn = SRC.OPTION_FRAMES[e.option_frame]
        return re.sub(rx, fn, q) if len(re.findall(rx, q)) == 1 else None
    if item.kind == "equiv":
        vals = SRC.slot_values(e, q)
        text = item.meta.get("para_text")
        if vals is None or not text or sorted(SRC.placeholders(text)) != sorted(vals):
            return None
        return SRC.fill(text, vals)
    raise ValueError(f"unknown kind {item.kind!r}")


def pair_of(item, question: str | None) -> tuple:
    """The question pair the polarity judges read: a pool paraphrase is read once as a slot template against the
    entry's template (G0 H41); every other partner as (base question, partner question)."""
    if item.kind == "equiv" and item.meta.get("para_text"):
        return SRC.pool_template(item.base.entry)[0], item.meta["para_text"]
    return item.base.row["instructions"], question


def pair_key(qa: str, qb: str) -> str:
    return "pair:" + sha(f"{qa}\x1f{qb}")[:20]


def answer_text(ans) -> str | None:
    if isinstance(ans, dict):
        ans = ans.get("question")
    if not isinstance(ans, str):
        return None
    t = " ".join(ans.split())
    return t or None


# ------------------------------------------------------------------------------------------------ candidates

@dataclass
class Candidate:
    item: object                         # select.PlanItem
    question: str | None
    author: str                          # haiku | program
    haiku_task_id: str | None = None
    haiku_prompt_sha: str | None = None
    rel_a: str | None = None
    rel_b: str | None = None
    problems: list = field(default_factory=list)
    pair: tuple = ()                     # the question pair the polarity judges read (pair_of)

    @property
    def ok(self) -> bool:
        return not self.problems and self.rel_a == self.rel_b == relation_of(self.item.kind)


def local_ban_hits(text: str) -> list:
    return [b for b in LOCAL_BANS if re.search(b, text or "", re.I)]


def check_candidate(item, question: str | None, *, author: str, frames: tuple, task_id=None, prompt_sha=None):
    c = Candidate(item, question, author, task_id, prompt_sha, pair=pair_of(item, question))
    if not question:
        c.problems.append("no partner question")
        return c
    want = relation_of(item.kind)
    base_q = item.base.row["instructions"]
    c.rel_a, pa = PA.classify_a(base_q, question, item.kind, item.base.entry, frames)
    c.rel_b, pb = PB.classify_b(base_q, question, item.kind, item.base.entry, frames)
    c.problems += pa + pb
    if c.rel_a != want or c.rel_b != want:
        c.problems.append(f"polarity programs read {c.rel_a!r} / {c.rel_b!r}, the plan wants {want!r}")
    if item.kind == "syntactic" and PA.frame_of(question, frames) != item.frame:
        c.problems.append("the partner does not use the planned frame")
    if item.kind == "implicit" and item.cue not in question:
        c.problems.append("the partner does not use the planned cue")
    hits = local_ban_hits(question) + (local_ban_hits(c.pair[1]) if item.kind == "equiv" and c.pair else [])
    if hits:
        c.problems.append(f"dev / eval frame hit {hits}")
    if item.kind == "syntactic" and item.frame in SRC.FRAMES_EXCLUDED.get(item.base.entry.key, ()):
        c.problems.append("the planned frame is excluded for this entry")
    return c


def build_candidates(plan: list, *, mode: str = "train", records: dict | None = None) -> list:
    """One candidate per plan item; every partner is program-written (program_partner). records: {template_id: pool
    record} of the admitted pool (author_pool.Pool.records), so an equiv partner names the Haiku task (haiku_task_id,
    haiku_prompt_sha) that wrote its paraphrase template."""
    frames = SRC.FRAMES_DEV if mode == "dev" else SRC.FRAMES_TRAIN
    out = []
    for it in plan:
        q = program_partner(it)
        if it.kind in HAIKU_KINDS:
            rec = (records or {}).get(it.meta.get("para"), {})
            out.append(check_candidate(it, q, author="haiku", frames=frames, task_id=rec.get("haiku_task_id"),
                                       prompt_sha=rec.get("haiku_prompt_sha")))
        else:
            out.append(check_candidate(it, q, author="program", frames=frames))
    return out


# ------------------------------------------------------------------------------------------------ partner rows

def partner_card(item) -> tuple:
    """(card text, defs_style) for the partner row."""
    yes, no = item.base.defs
    if item.kind == "equiv" or item.kind == "option_framing":
        return item.base.row["card"], "card_kept"
    if item.base.entry.card == "own":
        y2, n2 = SRC.COMPLEMENT_CARDS[item.base.entry.key]
        return f"- yes: {y2}\n- no: {n2}", "card_own_complement"
    if not SEL.swap_safe((yes, no)):
        raise ValueError(f"{item.base.entry.key}: definitions name an answer word and cannot be swapped")
    return f"- yes: {no}\n- no: {yes}", "card_swapped"


def wording_id(item) -> str:
    if item.kind == "syntactic":
        return f"t37b:frame:{item.frame}"
    if item.kind == "implicit":
        return f"t37b:cue:{item.cue}"
    if item.kind == "antonym":
        p, a = item.base.entry.antonyms[item.variant]
        return f"t37b:antonym:{p}>{a}"
    if item.kind == "option_framing":
        return f"t37b:option:{item.base.entry.option_frame}"
    return f"t37b:equiv:{item.meta.get('para')}"


def partner_row(c: Candidate, *, mode: str = "train", seed: int = 20261013, git_sha: str = "uncommitted") -> dict:
    if not c.ok:
        raise ValueError(f"candidate {c.item.pid} did not pass the polarity programs: {c.problems}")
    b = c.item.base.row
    kind = c.item.kind
    rel = "complement" if relation_of(kind) == "opposite" else "equiv"
    gold = 1 - b["gold"] if rel == "complement" else b["gold"]
    card, defs_style = partner_card(c.item)
    pid = f"{SOURCE}:{sha(b['id'] + '|' + kind + '|' + c.question)[:16]}"
    bm = b.get("meta") or {}
    haiku = c.author == "haiku"
    meta = {"family": FAMILY, "spec_id": f"{FAMILY}.G0lite.{G0_SHA256[:8]}+A1.{G0_AMENDMENT_SHA256[:8]}",
            "card_id": f"{FAMILY}:{c.item.base.entry.key}",
            "domain_pack": None, "sampler": "T37B-dev" if mode == "dev" else "T37B", "gen_version": GEN_VERSION,
            "git_sha": git_sha, "seed": seed, "structure_hash": sha(b["id"] + "|" + kind)[:16], "difficulty_bin": None,
            "crowd_pg": None, "depth": 0, "deep": False, "format_style": f"replay/{b['source']}",
            "wording_id": wording_id(c.item), "defs_style": defs_style, "twin_of": b["id"], "twin_kind": rel,
            "text_source": b["source"],
            "licence": f"{bm.get('licence') or 'the base row licence'} (text and definitions of {b['source']}); "
                       f"question wording: {R.LICENCE}",
            "edge": [], "qform": kind, "dev_only": mode == "dev",
            "c2": {"author_mode": "T", "skin_id": None, "register": "replay",
                   "lexicon_ids": [], "haiku_task_id": c.haiku_task_id if haiku else None,
                   "haiku_prompt_sha": c.haiku_prompt_sha if haiku else None, "twin_kind": rel, "twin_of": b["id"],
                   "closed_world": False},
            "t37b": {"base_id": b["id"], "base_source": b["source"], "entry": c.item.base.entry.key, "kind": kind,
                     "frame": c.item.frame, "cue": c.item.cue, "template": c.item.template, "author": c.author,
                     "polarity_a": c.rel_a, "polarity_b": c.rel_b, "base_gold": b["gold"]}}
    return {"id": pid, "group_id": b["group_id"], "call_id": b["call_id"], "source": SOURCE, "state": b["state"],
            "qtype": "noul", "instructions": c.question, "options": None, "gold": gold, "role": rel, "card": card,
            "meta": meta}


def relation_edge(row: dict) -> dict:
    t = row["meta"]["t37b"]
    return {"a": t["base_id"], "b": row["id"], "type": row["role"]}


def validate_partner(row: dict, base: dict, *, training: bool = False) -> list:
    """Schema problems: the C2 row checks (rows.validate_row; the licence names the base source's licence instead of
    CC0 alone, because the text is the base row's), plus the T37b unit rules."""
    probs = [p for p in R.validate_row(row, training=training) if p != "meta.licence"]
    m = row.get("meta") or {}
    if not str(m.get("licence", "")).endswith(f"question wording: {R.LICENCE}"):
        probs.append("licence must name the base licence and the question-wording licence")
    for k in ("state", "group_id", "call_id"):
        if row.get(k) != base.get(k):
            probs.append(f"{k} differs from the base row")
    want = 1 - base["gold"] if row.get("role") == "complement" else base["gold"]
    if row.get("gold") != want:
        probs.append(f"gold {row.get('gold')} != {want} ({row.get('role')} of base gold {base['gold']})")
    if m.get("twin_of") != base["id"] or (m.get("t37b") or {}).get("base_id") != base["id"]:
        probs.append("twin_of / base_id do not name the base")
    if row.get("role") == "complement" and SEL.parse_card(row.get("card")) is None:
        probs.append("partner card is not '- yes: ... / - no: ...'")
    return probs


# ------------------------------------------------------------------------------------------------ Haiku checks

def polarity_items(cands: list, judged: dict | None = None) -> list:
    """One item per DISTINCT question pair of the passing candidates that is not read yet (G0 H41): the item holds
    only the two questions, so equal pairs are one judgement. Internal id = pair_key."""
    seen, items = set(), []
    for c in cands:
        if not c.ok or not c.pair:
            continue
        k = pair_key(*c.pair)
        if k in seen or k in (judged or {}):
            continue
        seen.add(k)
        items.append((k, {"question_a": c.pair[0], "question_b": c.pair[1]}))
    return items


def polarity_batches(cands: list, *, seed: str, judged: dict | None = None) -> tuple:
    """Two independent polarity judgements (different seeds -> different orders, ids and chunks; two agents)."""
    items = polarity_items(cands, judged)
    if not items:
        return None, None
    a = chunker.make_batch("polarity", FAMILY, items, seed=f"{seed}|polarity-A", prompt=POLARITY_PROMPT)
    b = chunker.make_batch("polarity", FAMILY, items, seed=f"{seed}|polarity-B", prompt=POLARITY_PROMPT)
    return a, b


def polarity_of(c, answers_a: dict | None, answers_b: dict | None, judged: dict | None = None) -> tuple:
    """(judgement A, judgement B) of a candidate's pair: from the two batches' answers ({pair_key: answer}) or from
    the pool's admitted reads (judged: {pair_key: (A, B)})."""
    k = pair_key(*c.pair) if c.pair else None
    if k in (judged or {}):
        return tuple(judged[k])
    return (answers_a or {}).get(k), (answers_b or {}).get(k)


def blind_batches(cands: list, *, seed: str, mode: str = "train") -> tuple:
    """The blind solver reads every base and every partner, in two separate batches (never both of a pair in one
    chunk), exactly as the model sees them: text, question, definitions. Never gold, never meta."""
    ok = [c for c in cands if c.ok]
    if not ok:
        return None, None
    base = [(c.item.pid, g5h.read_item(c.item.base.row)) for c in ok]
    part = [(c.item.pid, g5h.read_item(partner_row(c, mode=mode))) for c in ok]
    a = chunker.make_batch("blind_read", FAMILY, base, seed=f"{seed}|blind-base", prompt=BLIND_PROMPT)
    b = chunker.make_batch("blind_read", FAMILY, part, seed=f"{seed}|blind-partner", prompt=BLIND_PROMPT)
    return a, b


def norm_relation(ans) -> str | None:
    if isinstance(ans, dict):
        ans = ans.get("relation")
    a = str(ans or "").strip().lower()
    return a if a in ("same", "opposite", "unclear") else None


def norm_yesno(ans) -> int | None:
    if isinstance(ans, dict):
        ans = ans.get("answer")
    a = str(ans or "").strip().lower().rstrip(".")
    return {"yes": 1, "no": 0}.get(a)


def decide(c: Candidate, pol_a, pol_b, blind_base, blind_partner, review: str | None = None) -> tuple:
    """(verdict, reason): keep | drop | review. Haiku answers only flag; nothing is relabelled."""
    want = relation_of(c.item.kind)
    if not c.ok:
        return "drop", "polarity programs"
    if norm_relation(pol_a) != want or norm_relation(pol_b) != want:
        return "drop", f"polarity judgements {norm_relation(pol_a)!r} / {norm_relation(pol_b)!r} (want {want!r})"
    yb, yp = norm_yesno(blind_base), norm_yesno(blind_partner)
    if yb is not None and yb != c.item.base.row["gold"]:
        # G0 amendment A1-1 (fix F1): a blind solver that answers the BASE against its human gold drops the unit, however
        # consistent its two answers are (pilot: a wrong human base gold passed a consistent blind pair twice). It only
        # drops: no label is set or changed, and no Claude review can keep such a unit.
        return "drop", "blind solver disagrees with the human base gold"
    consistent = yb is not None and yp is not None and ((yb != yp) if want == "opposite" else (yb == yp))
    if consistent:
        return "keep", "programs, judgements and blind solver agree"
    if review is None:
        return "review", "blind solver gave an inconsistent pair"
    return ("keep", "Claude review: exact") if review == "keep" else ("drop", "Claude review: doubt")


def review_items(cands: list, blind: dict) -> list:
    """Claude review queue for inconsistent pairs: both rows (with gold), the programs' readings and both blind
    answers. Verdict per item: 'keep' only when the partner question is certainly the planned relation and the gold
    follows; anything else is 'drop'."""
    out = []
    for c in cands:
        b = c.item.base.row
        p = partner_row(c)
        out.append((c.item.pid, {"base": {k: b[k] for k in ("state", "instructions", "card", "gold")},
                                 "partner": {k: p[k] for k in ("instructions", "card", "gold")},
                                 "kind": c.item.kind, "programs": [c.rel_a, c.rel_b],
                                 "blind": blind.get(c.item.pid)}))
    return out


MAX_ROW_TOKENS = 2000            # spec 3.0: every new row <= 2,000 rendered tokens (instructions counted twice)


def finalize(kept: list, *, mode: str = "train", seed: int = 20261013, n_complement: int = SEL.N_COMPLEMENT,
             n_equiv: int = SEL.N_EQUIV, run_g15: bool = True, trim: bool = True, max_tokens: int | None = MAX_ROW_TOKENS,
             token_fn=None) -> tuple:
    """(rows, rels, report) for the kept candidates; any row problem (schema, G15, length) drops that whole unit (never a
    fix-up); then select.trim_block cuts the training block back to its floors and caps (G0 H48). trim=False only for
    the in-memory exactness tests (the report's pass flag still checks the floors and caps).

    Length (G0 amendment A1-6): a partner row over max_tokens rendered tokens (spec 3.0) drops its unit. token_fn(rows)
    -> [tokens] is the pinned tokenizer's count (pilot.real_tokens / c_build/mixer.token_counts); None counts with the
    conservative rows.approx_tokens (3 characters per token), so a build that does not pass the real counter only
    over-drops. max_tokens=None skips the check."""
    if mode != "train":
        max_tokens = None                                   # T37b-dev rows are never trained (spec 2.2 / S15)
    built, dropped = [], []
    rows_ = [partner_row(c, mode=mode, seed=seed) for c in kept]
    toks = ([] if not rows_ or max_tokens is None else
            list(token_fn(rows_)) if token_fn else [R.approx_tokens(r) for r in rows_])
    for k, (c, r) in enumerate(zip(kept, rows_)):
        probs = validate_partner(r, c.item.base.row)
        if toks and toks[k] > max_tokens:
            probs.append(f"length: {toks[k]} rendered tokens > {max_tokens} (spec 3.0)")
        if run_g15:
            g = R.g15_check(r)
            probs += [f"G15: {p}" for p in g["problems"]] if not g["ok"] else []
        if probs:
            dropped.append((c.item.pid, probs))
            continue
        built.append((c.item, r))
    trimmed = []
    if mode == "train" and trim:
        keep_items, trimmed = SEL.trim_block([it for it, _ in built])
        keep_ids = {it.pid for it in keep_items}
        built = [(it, r) for it, r in built if it.pid in keep_ids]
    final = [it for it, _ in built]
    rows = [r for _, r in built]
    rels = [relation_edge(r) for r in rows]
    rep = SEL.plan_report(final, n_complement=n_complement if mode == "train" else SEL.N_DEV,
                          n_equiv=n_equiv if mode == "train" else 0, mode=mode)
    rep["trimmed"] = trimmed
    rep["length_dropped"] = [(pid, p) for pid, ps in dropped for p in ps if p.startswith("length:")]
    yn = [r["gold"] for r in rows]
    frames = Counter(r["meta"]["t37b"]["frame"] for r in rows if r["meta"]["t37b"]["frame"])
    rep.update({"yes_rate": (sum(yn) / len(yn)) if yn else None, "dropped_at_finalize": dropped,
                "frames": dict(sorted(frames.items()))})
    if mode == "dev" and any(f not in SRC.FRAMES_DEV for f in rep["frames"]):
        rep["pass"] = False
    if mode == "train" and any(f not in SRC.FRAMES_TRAIN for f in rep["frames"]):
        rep["pass"] = False
    return rows, rels, rep


def template_strings() -> dict:
    """Every Claude-written T37b template piece, for the G13 seed-first method-8 check (before any row exists). The
    admitted Haiku paraphrase templates go through G13 from the frozen pool (author_pool.pool_strings)."""
    from t37b import author_pool as AP          # noqa: PLC0415  (author_pool imports this module)
    return {"frames_train": list(SRC.FRAMES_TRAIN), "frames_dev": list(SRC.FRAMES_DEV),
            "cues": list(SRC.IMPLICIT_CUES), "complement_cards": [t for v in SRC.COMPLEMENT_CARDS.values() for t in v],
            "antonyms": [f"{p} / {a}" for e in SRC.ENTRIES for p, a in e.antonyms],
            "pool_templates": [SRC.pool_template(e)[0] for e in SRC.ENTRIES if SRC.pool_template(e)],
            "prompts": [AP.AUTHOR_POOL_PROMPT, AP.POOL_POLARITY_PROMPT, POLARITY_PROMPT, BLIND_PROMPT]}


def require_g0() -> None:
    """G0 H1: a writer refuses while g0_problems() is non-empty (the build halts; it is not only reported)."""
    probs = g0_problems()
    if probs:
        raise RuntimeError(f"T37b G0-lite check failed, nothing written: {probs}")


def write_block(rows: list, rels: list, *, name: str = "t37b_r1", prereg_text: str | None = None) -> list:
    """The training writer: lean/data/c2_parts/<name>.jsonl and <name>_relations.jsonl through the kit's guarded
    writer, which refuses before A38 (A37 f) and on any never-open path; refuses on a G0 problem first."""
    paths.require_a38(prereg_text)
    require_g0()
    return [paths.write_jsonl(paths.C2_PARTS / f"{name}.jsonl", rows, prereg_text=prereg_text),
            paths.write_jsonl(paths.C2_PARTS / f"{name}_relations.jsonl", rels, prereg_text=prereg_text)]


def write_dev(base_rows: list, partner_rows: list, rels: list, *, prereg_text: str | None = None) -> list:
    """T37b-dev (G0 H9, H49): data/c2_t37b_dev.jsonl holds the dev bases AND their partners (gate_c2 reads both rows
    of a pair) and data/c2_t37b_dev_relations.jsonl the {a: base, b: partner, type} edges. Never trained."""
    paths.require_a38(prereg_text)
    require_g0()
    if any(not (r.get("meta") or {}).get("dev_only") for r in partner_rows):
        raise ValueError("every T37b-dev partner row is meta.dev_only")
    data = paths.LEAN / "data"
    return [paths.write_jsonl(data / "c2_t37b_dev.jsonl", list(base_rows) + list(partner_rows),
                              prereg_text=prereg_text),
            paths.write_jsonl(data / "c2_t37b_dev_relations.jsonl", rels, prereg_text=prereg_text)]


def g0_problems() -> list:
    """The G0-lite spec (v2) and its Amendment 1 exist, are one page each (<= 200 lines) and match their frozen
    sha256s (G0 v3 = both files)."""
    probs = []
    for path, want, name in ((G0_LITE, G0_SHA256, "G0-lite spec"), (G0_AMENDMENT, G0_AMENDMENT_SHA256,
                                                                    "G0-lite amendment 1")):
        if not path.is_file():
            probs.append(f"{name} missing")
            continue
        n = len(path.read_text(encoding="utf-8").splitlines())
        if n > 200:
            probs.append(f"{name} has {n} lines")
        if hashlib.sha256(path.read_bytes()).hexdigest() != want:
            probs.append(f"{name} changed since it was frozen")
    return probs


def summary_json(report: dict) -> str:
    return json.dumps(report, indent=1, sort_keys=True, default=str)
