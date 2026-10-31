"""families/T23/haiku/redo2/build_redo2.py: the T23 REDO-2 Haiku task files for the stage-A pool-review blockers B1-B4
(G0_SPEC.md v3 section 10). A new file: it imports haiku_author, haiku_extract, plugin and the kit read-only and edits
none of them; it never writes pools/ and never sets, edits or reads a label. Every write goes through c2_kit.paths
(A38 guard, never-open guard), only under haiku/redo2/.

Stage A  ("tasks"; written now)
  glex  B1  two independent G-LEX reads (extractors glex-r2read0, glex-r2read1) of every v1-ADMITTED question form that
            keeps the v3 frame rule. Each form is filled as a row fills it (G0 section 10 B1): one pack of
            plugin.DOMAINS gives DOC and TERM_LABEL, CASE_ID is CASE-dddd, CANDIDATE a version id (v1 / rev-A / PFX-123),
            never one value in two slots and never a person's name. Prompt = haiku_extract.LEX_PROMPT + LEX_TAIL (the v1
            prompt, sha checked), choices = the 13 v1 meanings. v1-rejected forms are final and never re-read; forms that
            break the frame rule are excluded before any read (G0 section 10 B3/B4).
  g3h   B2  one G3-H read of every loader-admitted Mode F note (172) under the v3 ITEM schema (the item's name alone, no
            leading article or possessive), new qids. The compare later is g3h.compare with plugin.extract_fields
            (field names and kinds identical; only the item describe and the prompt sentence about it are new).
  dneg  B3  author_wording: 9 new double-negation wordings per positive yes/no form (27), under the v3 rule (un-negated
            frame, two syntactic negations inside the asked clause, no word with a "no" meaning).
Stage B  ("dneg-reads"; after the stage-A dneg answer exists): the v1 loader check (haiku_author.check_wording with
  double=True, unchanged) + the v3 frame rule + the no-"no"-word rule + dedup against every v1 text -> added to the v1
  registry (unit tests; a new form that breaks any form's unit test is dropped) -> 2 G-LEX reads, same prompt, choices
  and fill as stage A (extractors glex-r2read0 / glex-r2read1 on new forms).
Stage C  ("results"; after every answer exists): records only, into results/ (never pools/). Admission (G0 v3): a form
  is admitted iff it keeps the frame rule, no read on record (v1 or redo2) picks another meaning or is invalid, and both
  redo2 reads exist. An answer outside the item's choices is an invalid read (sem None: rejects, the kit rule). G3-H:
  the redo2 read replaces the v1 read for every note; exact compare; per-note and per-register reports, the template
  unit is the pool freeze's call (unchanged).

Run from lean/:
  ../.venv/bin/python c2_build/families/T23/haiku/redo2/build_redo2.py tasks [--write]    (default: dry run)
  ../.venv/bin/python c2_build/families/T23/haiku/redo2/build_redo2.py check              (disk == rebuild)
  ../.venv/bin/python c2_build/families/T23/haiku/redo2/build_redo2.py dneg-reads [--write]
  ../.venv/bin/python c2_build/families/T23/haiku/redo2/build_redo2.py results [--write]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent                  # .../families/T23/haiku/redo2
T23_DIR = HERE.parents[1]                               # .../families/T23
C2_BUILD = T23_DIR.parents[1]                           # .../lean/c2_build
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, paths  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.lexicon import LexiconError, LexiconRegistry, question_sem  # noqa: E402
from families.T23 import haiku_author as A  # noqa: E402
from families.T23 import haiku_extract as HX  # noqa: E402
from families.T23 import plugin as P  # noqa: E402
import negcount  # noqa: E402  (c_src/common, on sys.path via c2_kit.paths)

FAMILY = "T23"
SEED = "t23-redo2-v1"
V1_LEXICON = T23_DIR / "pools" / "lexicon.json"
V1_LEX_BATCH = T23_DIR / "haiku" / "extract" / "manifest" / "T23-extract_lex-cfe6eb2d.json"
LEX_MAX, G3H_MAX, DNEG_MAX = 50, 40, 30
R2_EXTRACTORS = ("glex-r2read0", "glex-r2read1")
POSITIVE = ("yn_version", "yn_claim", "yn_outcome")
N_DNEG = 9                                              # per positive form: 3x the G0 floor of 3 admitted

# ------------------------------------------------------------------------------------------------ G0 v3 rules
_AUX = r"(?:is|are|was|were|am|do|does|did|would|could|can|should|shall|will|has|have|had|must|might|may|need)"
FRAME_RULES = (   # G0 section 10 B3/B4: no wording negates its question frame
    ("fronted_negative_auxiliary",
     re.compile(r"^(?:[^,?]*,\s*)?(?:" + _AUX + r"n't|won't|can't|shan't|ain't|" + _AUX + r"\s+not|cannot)\b", re.I)),
    ("negated_it_frame", re.compile(r"\b" + _AUX + r"\s+it\s+not\b|\b\w+n't\s+it\b|\bcannot\s+it\b", re.I)),
    ("tag_question", re.compile(r",\s*(?:\w+n't|" + _AUX + r")\s+(?:it|that|this|they|there)\s*\?\s*$"
                                r"|,\s*(?:right|correct|true|no|yes)\s*\?\s*$", re.I)),
)
NO_WORDS = ("outside", "beyond", "exceed", "exceeds", "exceeded", "exceeding", "over", "above", "differ", "differs",
            "different", "depart", "departs", "contradict", "contradicts", "conflict", "conflicts", "against", "other",
            "besides", "else", "fail", "fails", "lack", "lacks", "without", "unless", "except", "refuse", "reject",
            "deny", "short")


def frame_problems(text: str) -> list:
    t = text.replace("’", "'").replace("‘", "'")
    return [name for name, rx in FRAME_RULES if rx.search(t)]


def k_syn(text: str) -> int:
    return negcount.count(K.PH_RE.sub("X", text)).k_syn


def no_word_hits(text: str) -> list:
    words = set(re.findall(r"[a-z']+", K.PH_RE.sub(" ", text).lower()))
    return [w for w in NO_WORDS if w in words]


def v3_problems(text: str) -> list:
    """G0 v3 shape problems of one wording: the frame rule for every form; for a double negation (k_syn 2) also the
    no-'no'-word rule."""
    out = [f"frame: {p}" for p in frame_problems(text)]
    if k_syn(text) >= 2:
        out += [f"double negation with a 'no' word: {w}" for w in no_word_hits(text)]
    return out


# ------------------------------------------------------------------------------------------------ registry + fill
def v1_registry() -> LexiconRegistry:
    """The frozen v1 registry (pools/lexicon.json, read-only): forms, v1 extractions, unit tests rerun."""
    return LexiconRegistry.from_json(json.loads(V1_LEXICON.read_text(encoding="utf-8")))


def _h(*parts) -> int:
    return int(hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()[:12], 16)


def fill_values(text: str) -> dict:
    """Row-like slot values for one form (G0 section 10 B1), seeded by the form text (label-blind): one pack of
    plugin.DOMAINS for DOC + TERM_LABEL, CASE_ID CASE-dddd, CANDIDATE in the plugin's yes/no id formats."""
    dom = P.DOMAIN_KEYS[_h(SEED, "dom", text) % len(P.DOMAIN_KEYS)]
    pack = P.DOMAINS[dom]
    u = _h(SEED, "idfmt", text) % 1000 / 1000
    k = 1 + _h(SEED, "k", text) % 4
    cand = (f"v{k}" if u < 0.4 else f"rev-{'ABCD'[k - 1]}" if u < 0.7
            else f"{pack.prefix}-{100 + _h(SEED, 'code', text) % 900}")
    vals = {"DOC": pack.doc, "TERM_LABEL": pack.term, "CASE_ID": f"CASE-{1000 + _h(SEED, 'case', text) % 9000}",
            "CANDIDATE": cand}
    assert len(set(vals.values())) == len(vals)
    return {"domain": dom, "values": vals}


def filled_text(reg: LexiconRegistry, fid: str) -> tuple:
    f = reg.forms[fid]
    fv = fill_values(f.text)
    used = {n: fv["values"][n] for n, _ in f.slots}
    slots = {n: (S.id_slot(used[n]) if kind == "id" else S.name_slot(used[n])) for n, kind in f.slots}
    txt = reg.render(fid, slots)
    if "{" in txt or "}" in txt:
        raise ValueError(f"{fid}: unfilled slot in {txt!r}")
    people = [c for c in P.CUSTOMERS + ("Dana Okafor", "INV-20419") if c in txt]
    if people:
        raise ValueError(f"{fid}: placeholder value {people} in {txt!r}")
    return txt, {"domain": fv["domain"], "values": used}


def glex_items(reg: LexiconRegistry, fids: list, read: int, tag: str) -> list:
    """[(form id, {"text", "choices"})]: the same filled text on both reads; the 13 meanings in a seeded order per read."""
    meanings = [s.meaning for s in reg.sems.values() if s.kind == "question"]
    out = []
    for fid in sorted(fids):
        txt, _ = filled_text(reg, fid)
        ch = sorted(meanings, key=lambda m: hashlib.sha256(f"{SEED}|{tag}|choices-r{read}|{fid}|{m}".encode())
                    .hexdigest())
        out.append((fid, {"text": txt, "choices": ch}))
    return out


def lex_prompt() -> str:
    p = HX.LEX_PROMPT + HX.LEX_TAIL
    v1 = json.loads(V1_LEX_BATCH.read_text(encoding="utf-8"))["prompt_sha"]
    if chunker.sha(p) != v1:
        raise ValueError("haiku_extract.LEX_PROMPT + LEX_TAIL no longer equals the v1 G-LEX prompt")
    return p


def glex_batches(reg: LexiconRegistry, fids: list, tag: str) -> list:
    out = []
    for r, ext in enumerate(R2_EXTRACTORS):
        items = glex_items(reg, fids, r, tag)
        b = chunker.make_batch("extract_lex", FAMILY, items, seed=f"{SEED}|{tag}|read{r}", prompt=lex_prompt(),
                               max_items=LEX_MAX)
        out.append((ext, b))
    return out


def b1_partition(reg: LexiconRegistry) -> dict:
    """{reread, excluded_frame, v1_rejected}: v1-admitted forms that keep the frame rule are re-read."""
    reread, excluded, rejected = [], {}, []
    for fid, f in sorted(reg.forms.items()):
        st = reg.status(fid)
        probs = v3_problems(f.text)
        if probs:
            excluded[fid] = {"v1_status": st, "problems": probs, "text": f.text}
        elif st == "rejected":
            rejected.append(fid)
        elif st == "admitted":
            reread.append(fid)
        else:
            raise ValueError(f"{fid}: v1 status {st} (expected admitted or rejected)")
    return {"reread": reread, "excluded_frame": excluded, "v1_rejected": rejected}


# ------------------------------------------------------------------------------------------------ G3-H (B2)
ITEM_DESCRIBE = ("the product or service the case is about: its name exactly as the note writes it, without a leading "
                 "article or possessive (a, an, the, my, our, your, his, her, their, its)")
G3H_PROMPT = (
    "You are reading short case notes for a synthetic dataset. Each item gives one note (a short piece of free text) and "
    "a schema with four fields; each field's describe says what its value is. For each item, copy out the value of each "
    "field exactly as the note writes it, with its capitals, spelling and punctuation, and nothing else. For the field "
    "item, copy only the name of the product or service: leave out a word in front of it such as a, an, the, my, our, "
    "your, his, her, their or its (a note about 'our garden hose' gives the item 'garden hose'). If a field's value is "
    "not in the note, write null. Do not answer any question in the note and do not explain.")


def g3h_fields() -> list:
    """plugin.extract_fields with the v3 item describe (same names and kinds, so g3h.compare is unchanged)."""
    out = []
    for f in P.T23.extract_fields(None, None):
        out.append(g3h.Field(f.name, f.kind, ITEM_DESCRIBE if f.name == "item" else f.describe, f.params, f.choices,
                             f.ordered))
    assert [(f.name, f.kind) for f in out] == [(f.name, f.kind) for f in P.T23.extract_fields(None, None)]
    return out


def g3h_batch() -> tuple:
    ff, probs = A.load_freeform()
    if len(ff) != 172:
        raise ValueError(f"expected the 172 loader-admitted Mode F notes, got {len(ff)}")
    fields = g3h_fields()
    items, expected = [], {}
    for sid in sorted(ff):
        sk = ff[sid]
        facts = dict(sk.brief)
        items.append((sid, g3h.extraction_item(sk.text, fields)))
        expected[sid] = {"register": sk.register, "expected": {"customer": facts["CUSTOMER"], "org": facts["ORG"],
                                                               "item": facts["ITEM"], "case_id": facts["CASE_ID"]}}
    b = chunker.make_batch("extract_g3h", FAMILY, items, seed=f"{SEED}|g3h", prompt=G3H_PROMPT + HX.G3H_TAIL,
                           max_items=G3H_MAX)
    return b, expected


# ------------------------------------------------------------------------------------------------ dneg authoring (B3)
DNEG_RULES = """

Double negation (this applies to EVERY item in this task). Each item names a plain yes/no question. Write a question \
with the SAME meaning, but with exactly two negations, each 'not' or n't, that cancel each other out: a reader who \
works through both negations must land on the plain question, never on its opposite.
A. The opening carries no negation. Never begin with a word ending in n't (Isn't, Doesn't, Wouldn't, Can't ...), and \
never write 'is it not', 'does it not', 'would it not', 'isn't it' or a tag ending such as ', isn't it?' or ', right?'. \
A negative opening asks the reader to confirm what follows, so it flips the meaning.
B. Both negations sit inside the part that is asked about, in the shape the item names:
   shape 1: an opening without negation (such as 'Is it the case that', 'Is it so that', 'Does it hold that' or \
'Would the card say that'), then 'it is not the case that', then a clause whose verb carries the second negation.
   shape 2: the first 'not' right after the subject, the second inside a 'that ...' part that follows a noun (a \
version, a claim, a case; never the word 'one').
   In the item patterns, OPENING and VERB stand for words you choose (an opening without negation; a verb such as \
govern, decide, support, back, fall, sit or stay); write real words, never the words OPENING or VERB.
C. No other word with a 'no' meaning anywhere: never outside, beyond, exceed, over, above, differ, different, depart, \
contradict, conflict, against, other, besides, else, fail, lack, without, unless, except, refuse, reject, deny, short.
D. Every question you write is different: follow each item's style hint, vary the opening and the verbs, and never \
reuse a sentence with a single word changed."""

DNEG_PLAIN = {
    "yn_version": "is {CANDIDATE} the version that governs this case? (yes only when {CANDIDATE} governs it)",
    "yn_claim": "does the governing version support the claim to check in the case record? (yes only when the claim "
                "states the value the governing version sets)",
    "yn_outcome": "is this case within the {TERM_LABEL} set by the governing version? (yes when the case's quantity is "
                  "at most that value)",
}
DNEG_SHAPE = {
    ("yn_version", 1): "Shape 1. Pattern: OPENING it is not the case that {CANDIDATE} does not VERB ...?",
    ("yn_version", 2): "Shape 2. Pattern: Is {CANDIDATE} not a version that does not VERB ...?",
    ("yn_claim", 1): "Shape 1. Pattern: OPENING it is not the case that the governing version does not VERB the claim ...?",
    ("yn_claim", 2): "Shape 2. Pattern: Is the claim to check not a claim that the governing version does not VERB ...?",
    ("yn_outcome", 1): "Shape 1. Pattern: OPENING it is not the case that this case does not VERB within the "
                       "{TERM_LABEL} ...?",
    ("yn_outcome", 2): "Shape 2. Pattern: Is this case not a case that does not VERB within the {TERM_LABEL} ...?",
}
DNEG_NEED = {"yn_version": "Include {CANDIDATE} exactly once.", "yn_claim": "Mention the claim to check (or the claim "
             "in the case record).", "yn_outcome": "Include {TERM_LABEL}."}


def dneg_items() -> tuple:
    items, plan = [], {}
    for qi, q in enumerate(POSITIVE):
        allowed = "Allowed placeholders: " + ", ".join("{" + s + "}" for s in A.WORDING_SLOTS[q]) + "."
        for i in range(N_DNEG):
            shape = 1 + (i + qi) % 2
            style = A.STYLE_TRAIN[(i + 2 * qi) % len(A.STYLE_TRAIN)]
            iid = f"t23r2.wording.{q}.dneg.{i:03d}"
            items.append((iid, {"brief": f"Plain question: {DNEG_PLAIN[q]} Write it with the double negation of the "
                                         f"rules above, in shape {shape}.",
                                "slots": dict(A.WORDING_SLOTS[q]),
                                "rules": [DNEG_SHAPE[(q, shape)],
                                          "Exactly two negation words, each 'not' or n't, both inside the asked part "
                                          "(none in the opening); no other negation word and no word with a 'no' "
                                          "meaning.", DNEG_NEED[q], allowed, f"Style hint: {style}."]}))
            plan[iid] = {"role": "wording", "qform": q, "held_out": False, "double": True, "shape": shape}
    return items, plan


def dneg_batch() -> tuple:
    items, plan = dneg_items()
    b = chunker.make_batch("author_wording", FAMILY, items, seed=f"{SEED}|dneg", prompt=A.WORDING_PROMPT + DNEG_RULES,
                           max_items=DNEG_MAX, forbid_strings=A.QSTRINGS)
    return b, plan


# ------------------------------------------------------------------------------------------------ task files
def _task_rows(b, *, stage: str, blocker: str, read: str | None, text_fn) -> tuple:
    files, rows = dict(b.files()), []
    for c in b.chunks:
        tid = c["task_id"]
        ans = str(HERE / b.answer_path(tid))
        tfile = f"tasks/{tid}.md"
        files[tfile] = text_fn(b, c, ans)
        rows.append({"task_file": str(HERE / tfile), "answer_file": ans, "kind": b.kind, "stage": stage,
                     "blocker": blocker, "read": read, "batch_id": b.batch_id, "task_id": tid,
                     "n_items": len(c["items"]), "prompt_sha": b.prompt_sha,
                     "audit_allowed_read": [str(HERE / tfile)], "audit_allowed_write": [ans]})
    return files, rows


def _guard(files: dict, rows: list) -> None:
    for f in list(files) + [r["answer_file"] for r in rows]:
        if paths.never_open(HERE / f):
            raise paths.NeverOpen(f"task path on the never-open list: {f}")


def stage_a() -> tuple:
    reg = v1_registry()
    part = b1_partition(reg)
    files, rows = {}, []
    lex = glex_batches(reg, part["reread"], "b1")
    for ext, b in lex:
        f, r = _task_rows(b, stage="A", blocker="B1", read=ext, text_fn=HX.task_text)
        files.update(f)
        rows += r
    g3, expected = g3h_batch()
    f, r = _task_rows(g3, stage="A", blocker="B2", read="g3h-r2", text_fn=HX.task_text)
    files.update(f)
    rows += r
    db, dplan = dneg_batch()
    f, r = _task_rows(db, stage="A", blocker="B3/B4", read=None, text_fn=A.task_file_text)
    files.update(f)
    rows += r
    fills = {}
    for fid in part["reread"]:
        txt, fv = filled_text(reg, fid)
        fills[fid] = {"text": txt, **fv}
    status_v1 = Counter(reg.status(f) for f in reg.forms)
    per_form = Counter(reg.forms[f].sem_id.split(".")[-1] for f in part["reread"])
    files["plan/b1_partition.json"] = json.dumps({
        "rule": "G0 v3 section 10 B1/B3/B4: v1-admitted forms that keep the frame rule are re-read 2x with the row "
                "fill; v1 rejections are final (never re-read); frame-rule breaks are excluded before any read",
        "v1_status": dict(sorted(status_v1.items())), "n_reread": len(part["reread"]),
        "reread_per_qform": dict(sorted(per_form.items())), "excluded_frame": part["excluded_frame"],
        "v1_rejected": part["v1_rejected"], "reread": part["reread"]}, ensure_ascii=False, indent=1) + "\n"
    files["plan/b1_fills.json"] = json.dumps(fills, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    files["plan/g3h_expected.json"] = json.dumps(expected, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    files["plan/dneg_plan.json"] = json.dumps({"batch_id": db.batch_id, "plan": dplan}, ensure_ascii=False, indent=1,
                                              sort_keys=True) + "\n"
    files["TASKS.json"] = json.dumps({
        "family": FAMILY, "version": SEED, "stage": "A", "g0_sha256": P.T23.G0_SHA256_V3, "n_tasks": len(rows),
        "batches": {"glex-r2read0": lex[0][1].batch_id, "glex-r2read1": lex[1][1].batch_id, "g3h-r2": g3.batch_id,
                    "dneg": db.batch_id},
        "counts": {"b1_reread_forms": len(part["reread"]), "b1_excluded_frame": len(part["excluded_frame"]),
                   "b1_v1_rejected_not_reread": len(part["v1_rejected"]), "g3h_notes": len(expected),
                   "dneg_items": len(dplan)},
        "notes": ["NEW items, new opaque ids, new answer paths; no v1 task, answer, key, pool or pinned file changes.",
                  "One fresh Haiku agent per task_file: it reads only that file and writes only its answer_file "
                  "(audit with audit_allowed_read / audit_allowed_write). key/ and plan/ are orchestrator-only.",
                  "glex-r2read0 and glex-r2read1 are independent reads: never give both reads' tasks to one agent.",
                  "Next: after the dneg answer exists run `build_redo2.py dneg-reads --write` (stage B: 2 G-LEX reads "
                  "of the new wordings); after every answer exists run `build_redo2.py results --write` (stage C).",
                  "Labels: none. Haiku answers only flag; every gold still comes from solver A = solver B."],
        "tasks": rows}, ensure_ascii=False, indent=1) + "\n"
    _guard(files, rows)
    return files, rows


# ------------------------------------------------------------------------------------------------ stage B (dneg reads)
def _load_raw(b) -> tuple:
    raw, probs = {}, []
    for c in b.chunks:
        f = HERE / b.answer_path(c["task_id"])
        if not f.is_file():
            probs.append(f"{c['task_id']}: no answer file")
            continue
        try:
            raw[c["task_id"]] = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            probs.append(f"{c['task_id']}: answer is not JSON ({e})")
    return raw, probs


def dneg_forms() -> tuple:
    """(registry v1 + accepted new double-negation forms, [new form ids], drops {iid: reasons}, load problems)."""
    b, plan = dneg_batch()
    raw, probs = _load_raw(b)
    if probs:
        raise FileNotFoundError("; ".join(probs))
    ans, p2 = chunker.load_answers(b, raw)
    v1 = v1_registry()
    if not all(f.unit_ok for f in v1.forms.values()):
        raise ValueError("a v1 form fails its unit test")
    seen = {" ".join(f.text.split()).lower() for f in v1.forms.values()}      # dedup against every v1 text
    task_of = {iid: b.task_of[qid] for qid, iid in b.key.items()}
    drops, ok = {}, []
    for iid in sorted(plan):
        a = ans.get(iid)
        text = a.get("text") if isinstance(a, dict) else None
        obj, v = A.check_wording(iid, text, plan[iid], task_of[iid], b.prompt_sha, seen)   # v1 loader, double=True
        if obj and not v:
            v = v3_problems(obj[1])
            if k_syn(obj[1]) != 2:
                v.append("not a double negation (k_syn != 2)")
        if v:
            drops[iid] = v
        else:
            ok.append((iid, obj))

    def build(accepted: list) -> tuple:
        r = v1_registry()
        fids = [r.add(text, question_sem(FAMILY, q), slots=dict(decl), family=FAMILY, source="haiku",
                      haiku_task_id=tid, haiku_prompt_sha=psha, held_out=held).form_id
                for q, text, decl, held, _d, tid, psha in accepted]
        return r, fids, r.unit_test_all()

    accepted = []
    for iid, obj in ok:          # a new form that fails its own unit test or breaks any other form's is dropped
        try:
            _r, fids, res = build(accepted + [obj])
        except LexiconError as e:
            drops[iid] = [f"registry: {e}"]
            continue
        bad = [fid for fid, passed in res.items() if not passed]
        if bad:
            drops[iid] = [f"unit test fails for {bad[:3]}"]
            continue
        accepted.append(obj)
    reg, new, _res = build(accepted)
    return reg, new, drops, p2


def stage_b() -> tuple:
    reg, new, drops, p2 = dneg_forms()
    files, rows = {}, []
    lex = glex_batches(reg, new, "b3") if new else []
    for ext, b in lex:
        f, r = _task_rows(b, stage="B", blocker="B3/B4", read=ext, text_fn=HX.task_text)
        files.update(f)
        rows += r
    files["plan/dneg_load.json"] = json.dumps({
        "new_forms": {fid: {"text": reg.forms[fid].text, "sem": reg.forms[fid].sem_id,
                            "fill": filled_text(reg, fid)[0]} for fid in new},
        "dropped": drops, "load_problems": p2,
        "per_qform": dict(sorted(Counter(reg.forms[f].sem_id.split(".")[-1] for f in new).items()))},
        ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    files["TASKS_B.json"] = json.dumps({
        "family": FAMILY, "version": SEED, "stage": "B", "g0_sha256": P.T23.G0_SHA256_V3, "n_tasks": len(rows),
        "batches": {ext: b.batch_id for ext, b in lex}, "n_new_forms": len(new), "n_dropped": len(drops),
        "notes": ["Two independent G-LEX reads of the new double-negation wordings: v1 prompt, 13 choices, B1 fill.",
                  "One fresh Haiku agent per task_file; never both reads to one agent."],
        "tasks": rows}, ensure_ascii=False, indent=1) + "\n"
    _guard(files, rows)
    return files, rows


# ------------------------------------------------------------------------------------------------ stage C (results)
def _record(reg: LexiconRegistry, lex: list, problems: list) -> dict:
    """Record every redo2 read; -> {form id: [(extractor, sem or None, choice)]}. An answer outside the item's own
    choices is an invalid read (sem None)."""
    out = {}
    for ext, b in lex:
        raw, probs = _load_raw(b)
        if probs:
            raise FileNotFoundError("; ".join(probs))
        ans, p2 = chunker.load_answers(b, raw)
        problems += [f"{ext}: {p}" for p in p2]
        items = chunker.item_by_internal(b)
        for fid in sorted(items):
            a = ans.get(fid)
            choice = a.get("choice") if isinstance(a, dict) else None
            sem = (reg.meaning_to_sem("question", choice) if isinstance(choice, str) and choice in items[fid]["choices"]
                   else None)
            reg.record_extraction(fid, ext, sem)
            out.setdefault(fid, []).append((ext, sem, choice))
    return out


def stage_c() -> dict:
    reg = v1_registry()
    part = b1_partition(reg)
    problems = []
    r2 = _record(reg, glex_batches(reg, part["reread"], "b1"), problems)
    reg_b, new, drops, _p = dneg_forms()
    r2b = _record(reg_b, glex_batches(reg_b, new, "b3"), problems) if new else {}
    status = {}
    for fid in sorted(reg.forms):
        if fid in part["excluded_frame"]:
            status[fid] = "excluded_frame"
        elif fid in part["v1_rejected"]:
            status[fid] = "rejected_v1"
        elif len({e for e, _s, _c in r2.get(fid, [])}) < 2:
            status[fid] = "pending_read_missing"
        else:
            status[fid] = reg.status(fid)
    for fid in new:
        status[fid] = reg_b.status(fid) if len({e for e, _s, _c in r2b.get(fid, [])}) == 2 else "pending_read_missing"
    forms = {**{f: reg.forms[f] for f in reg.forms}, **{f: reg_b.forms[f] for f in new}}
    admitted = [f for f, s in status.items() if s == "admitted"]
    per_form = Counter(forms[f].sem_id.split(".")[-1] for f in admitted)
    per_form_train = Counter(forms[f].sem_id.split(".")[-1] for f in admitted if not forms[f].held_out)
    dneg = Counter(forms[f].sem_id.split(".")[-1] for f in admitted if k_syn(forms[f].text) == 2)
    lex_out = {"rule": "G0 v3 section 10: admitted iff frame rule kept, every read on record (v1 + redo2) picks the "
                       "form's meaning, both redo2 reads present; an invalid read rejects (kit rule)",
               "status_counts": dict(sorted(Counter(status.values()).items())),
               "admitted_per_qform": dict(sorted(per_form.items())),
               "admitted_per_qform_training": dict(sorted(per_form_train.items())),
               "double_negation_admitted": dict(sorted(dneg.items())),
               "g0_targets": {"total": ">= 30", "per_form": ">= 6", "double_negation_per_positive_form": ">= 3"},
               "status": status, "dneg_dropped_at_load": drops, "answer_problems": problems,
               "reads": {f: [[e, s, c] for e, s, c in v] for f, v in sorted({**r2, **r2b}.items())},
               "texts": {f: forms[f].text for f in sorted(status)}}
    gb, expected = g3h_batch()
    raw, probs = _load_raw(gb)
    if probs:
        raise FileNotFoundError("; ".join(probs))
    ans, p3 = chunker.load_answers(gb, raw)
    fields = P.T23.extract_fields(None, None)
    rows, by_note, by_reg = [], [], []
    for sid in sorted(expected):
        ok, diffs = g3h.compare(expected[sid]["expected"], ans.get(sid, {}), fields) if sid in ans else \
            (False, ["no answer"])
        rows.append({"sid": sid, "register": expected[sid]["register"], "ok": ok, "diffs": diffs})
        by_note.append((sid, sid, ok))
        by_reg.append((expected[sid]["register"], sid, ok))
    g3h_out = {"rule": "G0 v3 section 10 B2: the redo2 read replaces the v1 read for every note; exact compare "
                       "(g3h.compare, plugin.extract_fields); 98% bar unchanged; template unit = the pool freeze's call",
               "n": len(rows), "pass": sum(r["ok"] for r in rows), "answer_problems": p3,
               "template_report_per_note": g3h.template_report(by_note),
               "template_report_per_register": g3h.template_report(by_reg), "rows": rows}
    return {"results/glex_redo2.json": lex_out, "results/g3h_redo2.json": g3h_out,
            "results/lexicon_redo2_new_forms.json": reg_b.to_json()}


# ------------------------------------------------------------------------------------------------ CLI
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=("tasks", "check", "dneg-reads", "results"))
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args(argv)
    if a.cmd in ("tasks", "check"):
        files, rows = stage_a()
        if a.cmd == "check":
            diffs = [rel for rel, text in sorted(files.items())
                     if not (HERE / rel).is_file() or (HERE / rel).read_text(encoding="utf-8") != text]
            print(json.dumps({"files": len(files), "diffs": diffs}, indent=1))
            return 1 if diffs else 0
        if a.write:
            if (HERE / "TASKS.json").exists():
                old = json.loads((HERE / "TASKS.json").read_text(encoding="utf-8"))
                if old.get("version") == SEED and (HERE / "TASKS.json").read_text(encoding="utf-8") != \
                        files["TASKS.json"]:
                    raise SystemExit("TASKS.json on disk differs from the rebuild: refusing to overwrite stage A")
            paths.write_files(HERE, files)
            paths.check_path(HERE / "answers").mkdir(exist_ok=True)
        print(json.dumps({"written": a.write, "n_tasks": len(rows), "by_kind": dict(Counter(r["kind"] for r in rows)),
                          "tasks": [{k: r[k] for k in ("task_file", "answer_file", "kind", "blocker", "n_items")}
                                    for r in rows]}, indent=1))
        return 0
    if a.cmd == "dneg-reads":
        files, rows = stage_b()
        if a.write:
            paths.write_files(HERE, files)
        print(json.dumps({"written": a.write, "n_tasks": len(rows),
                          "tasks": [{k: r[k] for k in ("task_file", "answer_file", "kind", "n_items")} for r in rows]},
                         indent=1))
        return 0
    out = stage_c()
    if a.write:
        for rel, obj in out.items():
            paths.write_json(HERE / rel, obj)
    print(json.dumps({"written": a.write, "glex": {k: out["results/glex_redo2.json"][k] for k in
                                                   ("status_counts", "admitted_per_qform_training",
                                                    "double_negation_admitted")},
                      "g3h": {k: out["results/g3h_redo2.json"][k] for k in ("n", "pass")}}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
