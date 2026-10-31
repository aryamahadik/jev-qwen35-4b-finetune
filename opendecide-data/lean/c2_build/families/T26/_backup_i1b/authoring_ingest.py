"""c2_build/families/T26/authoring_ingest.py: the T26 pool stage after the Haiku AUTHORING answers came back (G0_SPEC.md
section 4; C2_DATA_SPEC 6.3 G-SL, G-LEX, G3-H; PREREG A37 (b) and A38).

What it does (after A38 only; every write goes through the kit's guarded writers):
  1. rebuilds the authoring batches in memory (author_tasks.build) and checks them against TASKS.json and key/;
  2. loads every returned answer file (chunker.load_answers) and reports the items still unanswered;
  3. lints every piece: the kit's G-SL (gsl.lint_template / lint_freeform / lint_values) plus the closed checks of
     G0 section 4 and the author spec; a failing piece is dropped with its reasons;
  4. dedups each pool (normalised text; packs by company name and by label);
  5. admits the survivors into a T26 LexiconRegistry (Haiku forms, unit tests only; extraction comes later);
  6. writes the G-LEX extraction reads (2 for question wordings, 3 for precedence paraphrases: one chunk file per read,
     so each form appears in separate chunks) and the G3-H round-trip items for every Mode F document under
     haiku/extract/. No label is set here: golds come only from solver A and solver B (A37 b), and Haiku output
     never sets a label.

  ../.venv/bin/python -m families.T26.authoring_ingest          (from lean/c2_build)
"""
from __future__ import annotations

import hashlib
import json
import random
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, gsl, paths  # noqa: E402
from c2_kit import polarity as PO  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.lexicon import LexiconRegistry, question_sem  # noqa: E402
from c2_kit.plugin import ContractError  # noqa: E402
from families.T26 import author_tasks as AT  # noqa: E402
from families.T26 import fixtures as FX  # noqa: E402
from families.T26 import plugin as P  # noqa: E402

import negcount  # noqa: E402  (c_src/common, on sys.path through c2_kit.paths)

FAMILY = P.FAMILY
ROOT = P.HERE / "haiku" / "author"            # the authoring tasks (written by author_tasks.py)
EXTRACT = P.HERE / "haiku" / "extract"        # the pool-stage extraction tasks written here
ORCH = EXTRACT / "orchestrator"               # lint log, survivors, registry: orchestrator only (never a Haiku file)
LABEL_WORDS = tuple(P.T26Plugin.LABEL_WORDS)
EXC = P.T26Plugin.GSL_EXCEPTIONS
NAME_ALLOW = P.T26Plugin.NAME_ALLOW
SKIN_DECL = {"REQUESTER": "name", "COUNTERPARTY": "name", "CHANGE": "category", "REQ_ID": "id"}
POOLS = ("pack", "skin", "skin_heldout", "freeform", "freeform_heldout", "attack", "wording", "precedence")
FREE_FIELDS = ("REQUESTER", "COUNTERPARTY", "CHANGE", "REQ_ID")
OUTCOME_RE = re.compile(r"\b(?:appl(?:y|ies|ied|ying)|reject(?:s|ed|ing|ion)?|escalat(?:e|es|ed|ing|ion))\b"
                        r"|\bhold(?:s|ing)? back\b|\bheld back\b", re.I)
TITLE_RE = re.compile(r"sender domain|signed addendum|call-?\s?back|addendum|approver|form version|version register",
                      re.I)
OPTION_RE = re.compile(r"every listed check passes|apply the change|reject the request", re.I)
INJECT_RE = re.compile(r"ignore (?:all |the |any |your )?(?:previous|prior|above)|system (?:override|prompt)|"
                       r"developer mode|you are now|as an ai\b|\boverride\b", re.I)
CAP_RE = re.compile(r"[A-Z][A-Za-z]*(?: [A-Z][A-Za-z]*){1,2}")
LABEL_RE = re.compile(r"[a-z0-9-]{5,18}")
WORD_NEG = {"yn_not_apply": (1, 1), "yn_dneg_apply": (2, 2)}      # (k_all, k_syn) the form needs (G0 H14)
PLACEHOLDER_ONLY = re.compile(r"\{[A-Z][A-Z0-9_]*\}")


def _norm(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split()).rstrip(".?!")


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def _braces(text: str) -> bool:
    """A brace that is not one of the slots (plain text: no other braces, G0 section 4)."""
    return bool(re.search(r"[{}]", K.PH_RE.sub("", text)))


def _gsl_template(sk) -> list:
    return [f"G-SL {v.rule}: {v.detail}" for v in gsl.lint_template(
        sk, label_words=LABEL_WORDS, exceptions=EXC, name_allow=NAME_ALLOW)]


# ------------------------------------------------------------------------------------------------ G-SL and closed checks

def lint_skin(text, register: str) -> list:
    """Mode T request message (G0 section 4): the four slots once each, plain text, the G-SL word and name lint."""
    if not isinstance(text, str) or not text.strip():
        return ["not a non-empty text"]
    probs = ["braces outside the four slots"] if _braces(text) else []
    sk = K.make_skin(f"skin-{register}", FAMILY, text, SKIN_DECL, kind="skin", register=register, escape="text",
                     author_mode="T")
    return probs + _gsl_template(sk)


def lint_attack(text, slot: str) -> list:
    """Attack line (G0 section 4): one line, exactly the one slot the item names, no digit, date, address, name or
    label word, no stock injection phrasing (the G-SL attack role plus the closed checks)."""
    if not isinstance(text, str) or not text.strip():
        return ["not a non-empty text"]
    t = text.strip()
    probs = []
    if "\n" in t:
        probs.append("not one line")
    if _braces(t):
        probs.append("braces outside the slot")
    sk = K.make_skin("attack", FAMILY, t, {slot: "name"}, kind="attack", register="note", escape="text",
                     author_mode="T")
    probs += _gsl_template(sk)
    words = {w.lower() for w in re.findall(r"[A-Za-z]+", K.PH_RE.sub(" ", t))}
    hit = sorted(words & gsl._label_forms(LABEL_WORDS))
    if hit:
        probs.append(f"label word {hit}")
    if re.search(r"hold(?:s|ing)? back|held back", t, re.I):
        probs.append("label phrase 'hold back'")
    m = INJECT_RE.search(t)
    if m:
        probs.append(f"stock injection phrasing {m.group()!r}")
    return probs


def lint_wording(text, qform: str) -> list:
    """Question wording (G0 section 4): one question line, {REQ_ID} once and no other slot, negation by negcount
    (H14), yn_clears keeps its scope (H1), ch_* wordings name no outcome, option or check title (G0 section 4)."""
    if not isinstance(text, str) or not text.strip():
        return ["not a non-empty text"]
    t = text.strip()
    probs = []
    if "\n" in t:
        probs.append("not one line")
    if not t.endswith("?"):
        probs.append("does not end with a question mark")
    n = len(t.split())
    if not 6 <= n <= 25:
        probs.append(f"{n} words (author spec 6-25)")
    if _braces(t):
        probs.append("braces outside {REQ_ID}")
    sk = K.make_skin(f"wording-{qform}", FAMILY, t, {"REQ_ID": "id"}, kind="wording", register="question",
                     escape="text", author_mode="T", qform=qform)
    probs += _gsl_template(sk)
    c = negcount.count(K.PH_RE.sub("REF", t))
    want = WORD_NEG.get(qform, (0, 0))
    if (c.k_all, c.k_syn) != want:
        probs.append(f"negation k_all {c.k_all} k_syn {c.k_syn}, form needs {want[0]} / {want[1]}")
    low = t.lower()
    if qform == "yn_clears" and "whose record is provided" not in low:
        probs.append("yn_clears must say 'whose record is provided' (G0 H1)")
    if qform in ("ch_verdict", "ch_failing"):
        if OUTCOME_RE.search(t):
            probs.append("names an outcome (ch_* wordings name none)")
        if OPTION_RE.search(t):
            probs.append("names an option text")
        if TITLE_RE.search(t):
            probs.append("names a check title")
    if qform == "yn_fails" and re.search(r"verif|not provided", low):
        probs.append("mentions unverifiable checks (yn_fails counts only failing checks)")
    return probs


def wording_problems(text, qform: str) -> list:
    """The admission check of a NEW or re-authored question wording (Stage B fix F3, G0 R3): lint_wording plus the kit's
    polarity rule (c2_kit.polarity P1-P3; a yes/no wording must read with its form's declared polarity). The frozen
    pools_v2 rebuild keeps calling lint_wording unchanged (freeze_v2 rebuilds the pools from the answers byte for byte),
    so no frozen form can change; every wording of the frozen pool passes this check as well (test_fix_i1)."""
    probs = lint_wording(text, qform)
    if isinstance(text, str) and text.strip():
        probs += [f"polarity {p}" for p in PO.form_problems(P.T26Plugin, qform, text.strip())]
    return probs


def lint_precedence(text) -> list:
    """Precedence paraphrase (G0 section 4): one line, one sentence with no full stop, question or exclamation mark,
    {X} exactly once and never the last token; the G-SL wording lint for the rest."""
    if not isinstance(text, str) or not text.strip():
        return ["not a non-empty text"]
    t = text.strip()
    probs = []
    if "\n" in t:
        probs.append("not one line")
    if re.search(r"[.?!]", t):
        probs.append("a full stop, question mark or exclamation mark (the card adds the full stop)")
    if t.count("{X}") != 1:
        probs.append("{X} must appear exactly once")
    else:
        after = t[t.index("{X}") + 3:]
        if not re.search(r"[A-Za-z]", after):
            probs.append("{X} is the last word")
    n = len(t.split())
    if not 15 <= n <= 60:
        probs.append(f"{n} words (author spec 15-60)")
    if _braces(t.replace("{X}", "")):
        probs.append("braces outside {X}")
    sk = K.make_skin("precedence", FAMILY, t, {"X": "name"}, kind="wording", register="policy", escape="text",
                     author_mode="T")
    return probs + _gsl_template(sk)


def lint_freeform(text, facts: dict) -> list:
    """Mode F document (G0 section 4): every fact verbatim, no other number, date, id, URL, currency, label word or
    negation cue outside the facts (gsl.lint_freeform), and no braces."""
    if not isinstance(text, str) or not text.strip():
        return ["not a non-empty text"]
    probs = ["braces in a Mode F document"] if _braces(text) else []
    fills = {k: facts[k] for k in FREE_FIELDS}
    return probs + [f"G-SL {v.rule}: {v.detail}" for v in gsl.lint_freeform(text, fills, label_words=LABEL_WORDS)]


def lint_pack(cp, label) -> list:
    """Pack (G0 section 4): counterparty 2-3 capitalised ASCII words with no negation cue or label word; domain label
    5-18 chars of a-z 0-9 with at most one hyphen, >= 4 letters incl. a consonant; a look-alike exists for every S3
    suffix (so an S11 edit always exists); both pass the kit's slot lint."""
    if not isinstance(cp, str) or not isinstance(label, str):
        return ["counterparty and domain_label are text"]
    probs = []
    if not CAP_RE.fullmatch(cp):
        probs.append("counterparty: 2-3 capitalised ASCII words")
    if negcount.count(cp).k_all:
        probs.append("negation cue in counterparty")
    if {w.lower() for w in re.findall(r"[A-Za-z]+", cp)} & gsl._label_forms(LABEL_WORDS):
        probs.append("label word in counterparty")
    if not LABEL_RE.fullmatch(label):
        probs.append("domain_label: 5-18 chars of a-z, 0-9, hyphen")
    else:
        if not label[0].isalpha() or not label[-1].isalnum():
            probs.append("domain_label: starts with a letter, ends with a letter or digit")
        if label.count("-") > 1:
            probs.append("domain_label: at most one hyphen")
        letters = [ch for ch in label if ch.isalpha()]
        if len(letters) < 4 or not any(ch not in "aeiou" for ch in letters):
            probs.append("domain_label: >= 4 letters incl. a consonant")
    if probs:
        return probs
    try:
        S.name_slot(cp)
    except S.SlotError as e:
        return [f"counterparty is not a name slot: {e}"]
    probs += [f"G-SL {v.rule}: {v.detail}" for v in gsl.lint_values({"COUNTERPARTY": S.name_slot(cp)})]
    for suffix in P.TLDS:
        dom = f"{label}.{suffix}"
        try:
            S.id_slot(dom)
        except S.SlotError:
            probs.append(f"{dom} is not a registered-domain id")
            continue
        try:
            P.lookalike(dom, random.Random(f"T26|lookalike|{dom}"))
        except (ContractError, IndexError, ValueError) as e:
            probs.append(f"no look-alike for {dom} (S11): {type(e).__name__}")
    return probs


# ------------------------------------------------------------------------------------------------ loading

def _meta(iid: str) -> dict:
    """Internal ids are t26|<tag>|...: the pool-stage tags (register, tone, qform, slot) are read from them."""
    parts = iid.split("|")
    if parts[1] in ("skin", "skin_ho", "free", "free_ho"):
        return {"register": parts[2], "tone": parts[3]}
    if parts[1] == "wording":
        return {"qform": parts[2]}
    if parts[1] == "attack":
        return {"slot": parts[2]}
    return {}


def rebuild_and_check() -> tuple:
    """(batches by pool, index rows). The rebuilt authoring tasks must match TASKS.json and the key files on disk."""
    built = AT.build()
    batches = {pool: b for pool, b, _ in built}
    rows = AT.index(built)
    tasks = json.loads((ROOT / "TASKS.json").read_text(encoding="utf-8"))
    if rows != tasks["tasks"]:
        raise SystemExit("rebuilt authoring tasks differ from TASKS.json: refusing to ingest")
    for pool, b in batches.items():
        key = json.loads((ROOT / "key" / f"{b.batch_id}.json").read_text(encoding="utf-8"))["key"]
        if key != b.key:
            raise SystemExit(f"key file for pool {pool} differs from the rebuilt batch: refusing to ingest")
    return batches, tasks


def load_pieces(batches: dict, tasks: dict) -> tuple:
    """(pieces, coverage): every returned answer as a piece (value, pool, internal id, task, item); coverage says how
    many items of each pool came back and which tasks are still missing an answer file."""
    pieces, coverage = [], {}
    for pool in POOLS:
        b = batches[pool]
        raw, missing = {}, []
        for t in tasks["tasks"]:
            if t["pool"] != pool:
                continue
            tid = Path(t["task_file"]).stem
            ans = ROOT / "answers" / f"{tid}.json"
            if not ans.exists():
                missing.append(tid)
                continue
            raw[tid] = json.loads(ans.read_text(encoding="utf-8"))
        got, probs = chunker.load_answers(b, raw)
        items = chunker.item_by_internal(b)
        task_of = {b.key[q]: b.task_of[q] for q in b.key}
        coverage[pool] = {"items": len(b.key), "answered": len(got), "missing_tasks": missing,
                          "problems": probs, "tasks": sum(1 for t in tasks["tasks"] if t["pool"] == pool)}
        for iid, a in sorted(got.items()):
            item = {k: v for k, v in items[iid].items() if k != "qid"}
            pieces.append({"pool": pool, "internal_id": iid, "task_id": task_of[iid],
                           "prompt_sha": b.prompt_sha, "item": item, "answer": a, "problems": [], "meta": _meta(iid)})
    return pieces, coverage


# ------------------------------------------------------------------------------------------------ the lint pass

def _value(piece: dict):
    a = piece["answer"]
    if piece["pool"] == "pack":
        return a.get("counterparty"), a.get("domain_label")
    return a.get("text")


def lint_all(pieces: list) -> list:
    """Attach the problems of every piece (G-SL, closed checks, pack checks). Returns the same list."""
    for p in pieces:
        pool, item, meta = p["pool"], p["item"], p["meta"]
        if pool == "pack":
            cp, label = _value(p)
            p["problems"] = lint_pack(cp, label)
        elif pool in ("skin", "skin_heldout"):
            p["problems"] = lint_skin(_value(p), item["register"])
        elif pool == "attack":
            p["problems"] = lint_attack(_value(p), item["slots"][0].strip("{}"))
        elif pool in ("freeform", "freeform_heldout"):
            p["problems"] = lint_freeform(_value(p), item["facts"])
        elif pool == "wording":
            p["problems"] = lint_wording(_value(p), meta["qform"])
        elif pool == "precedence":
            p["problems"] = lint_precedence(_value(p))
        else:
            raise SystemExit(f"unknown pool {pool}")
    return pieces


def dedup_pass(pieces: list) -> list:
    """Dedup inside each pool (normalised text, so a case-only or punctuation-only copy is a copy). A wording or a
    precedence paraphrase that equals a fixture stand-in (never training text) is dropped too. Packs: company names and
    labels must differ from each other and from the placeholder packs. Pieces already dropped are not counted again."""
    seen = defaultdict(dict)
    stand_in = {_norm(t) for _, _, t in FX.WORDINGS} | {_norm(t) for t in FX.PREC_FORMS}
    placeholder_names = {_norm(cp) for cp, _ in P.PACKS} | {_norm(lb) for _, lb in P.PACKS}
    for p in pieces:
        if p["problems"]:
            continue
        pool = p["pool"]
        if pool == "pack":
            cp, lb = _value(p)
            keys = (_norm(cp), _norm(lb))
            if keys[0] in placeholder_names or keys[1] in placeholder_names:
                p["problems"].append("dedup: equals a placeholder pack")
                continue
            if keys[0] in seen[("pack", "cp")] or keys[1] in seen[("pack", "lb")]:
                p["problems"].append("dedup: company name or label repeats")
                continue
            seen[("pack", "cp")][keys[0]] = p["internal_id"]
            seen[("pack", "lb")][keys[1]] = p["internal_id"]
            continue
        key = _norm(_value(p))
        group = {"skin_heldout": "skin", "freeform_heldout": "freeform"}.get(pool, pool)
        if pool in ("wording", "precedence") and key in stand_in:
            p["problems"].append("dedup: a copy of a fixture stand-in")
            continue
        if key in seen[group]:
            p["problems"].append(f"dedup: repeats {seen[group][key]}")
            continue
        seen[group][key] = p["internal_id"]
    # a wording text that two different question forms share is ambiguous: drop every copy
    by_text = defaultdict(list)
    for p in pieces:
        if p["pool"] == "wording" and not p["problems"]:
            by_text[_norm(_value(p))].append(p)
    for group in by_text.values():
        if len({p["meta"]["qform"] for p in group}) > 1:
            for p in group:
                p["problems"].append("dedup: the same text under two question forms")
    return pieces


def designate_held_out_packs(pieces: list, n: int = 6) -> list:
    """Pack pool freeze: the held-out packs (never drawn by samplers S1-S4) are the n kept packs with the smallest
    seeded hash of their internal id (seed T26|pack-heldout). Returns the kept pack pieces."""
    kept = [p for p in pieces if p["pool"] == "pack" and not p["problems"]]
    order = sorted(kept, key=lambda p: _sha(f"T26|pack-heldout|{p['internal_id']}"))
    held = {p["internal_id"] for p in order[:n]}
    for p in kept:
        p["held_out"] = p["internal_id"] in held
    return kept


# ------------------------------------------------------------------------------------------------ registry (G-LEX)

def build_registry(pieces: list) -> LexiconRegistry:
    """The T26 pool registry: the declared sems and decoy readings (plugin.declare_lexicon), then every surviving Haiku
    precedence paraphrase and question wording as a form (source haiku, with its task id and prompt sha). Unit tests run
    here; extraction is recorded later, from the G-LEX reads."""
    reg = P.declare_lexicon(LexiconRegistry(FAMILY))
    added, refused = Counter(), []
    for p in pieces:
        if p["problems"] or p["pool"] not in ("wording", "precedence"):
            continue
        text = _value(p)
        try:
            if p["pool"] == "precedence":
                reg.add(text.strip(), P.PREC_SEM, slots={"X": "name"}, source="haiku", family=FAMILY,
                        haiku_task_id=p["task_id"], haiku_prompt_sha=p["prompt_sha"])
                added["precedence"] += 1
            else:
                qf = p["meta"]["qform"]
                reg.add(text.strip(), question_sem(FAMILY, qf), slots={"REQ_ID": "id"}, source="haiku", family=FAMILY,
                        haiku_task_id=p["task_id"], haiku_prompt_sha=p["prompt_sha"])
                added[f"question:{qf}"] += 1
        except Exception as e:  # a registry refusal is logged and the piece is dropped, never patched
            refused.append({"internal_id": p["internal_id"], "reason": str(e)})
            p["problems"].append(f"registry: {e}")
    reg.unit_test_all()
    return reg, added, refused


def lex_status(reg: LexiconRegistry) -> dict:
    out = {}
    for fid, f in sorted(reg.forms.items()):
        out[fid] = {"sem": f.sem_id, "kind": f.kind, "unit_ok": f.unit_ok, "status": reg.status(fid),
                    "unit_problems": f.unit_problems[:3]}
    return out


# ------------------------------------------------------------------------------------------------ extraction tasks

LEX_PROMPT = """You are reading short texts for a dataset. This task file is your whole task. It has: answer_file (the
exact path you must write), instructions (these lines), and items. Each item has a qid, a text and a list of choices.
TASK: for each item, read the text on its own and pick the ONE choice whose meaning the text states, exactly.
Copy that choice character for character as the meaning. If the text states none of the choices, write NONE.
Do not guess from the wording of a choice; judge the text. Do not open, search or write any other file.
Write ONE JSON array to answer_file with the Write tool and nothing else: one object per item, every qid exactly once,
in the form {"qid": "<qid>", "meaning": "<one choice exactly, or NONE>"}."""

G3H_PROMPT = """You are reading short free-form messages for a dataset. This task file is your whole task. It has:
answer_file (the exact path you must write), instructions (these lines), and items. Each item has a qid, a text and a
schema of fields.
TASK: for each item, read the text only and give the value of every field in the schema, as the text states it.
Copy names, the company and the reference exactly as they appear in the text, character for character. For the change
field, return the entry of its choices that matches the text's action; if none matches the text's wording, copy the
text's own words for the action. Write null for a field the text does not state. Do not guess and do not add fields.
Do not open, search or write any other file.
Write ONE JSON array to answer_file with the Write tool and nothing else: one object per item, every qid exactly once,
in the form {"qid": "<qid>", "requester": "...", "counterparty": "...", "change": "...", "req_id": "..."} with one key
per field name of the schema."""


def _finalize(batch, pool: str, prompt: str) -> chunker.TaskBatch:
    """Chunk files in the authoring layout: answer_file, pool and the instructions, so the agent reads only its chunk."""
    for i, c in enumerate(batch.chunks):
        ans = str(EXTRACT / batch.answer_path(c["task_id"]))
        batch.chunks[i] = {"task_id": c["task_id"], "kind": c["kind"], "pool": pool, "prompt_sha": c["prompt_sha"],
                           "answer_file": ans, "instructions": prompt.split("\n"), "items": c["items"]}
        blob = json.dumps(batch.chunks[i], ensure_ascii=False)
        if any(iid in blob for iid in batch.key.values()):
            raise chunker.ChunkError("an extraction task file names an internal id")
    return batch


def lex_batches(reg: LexiconRegistry, fids_by_kind: dict) -> list:
    """Independent G-LEX reads: 2 for question wordings, 3 for precedence paraphrases. Each read is a separate batch
    with its own seed (its own qids, item order and choice order), so no two reads share an agent or a chunk."""
    out = []
    plan = [("question", "glex-question", 2), ("precedence", "glex-precedence", 3)]
    for kind, name, reads in plan:
        fids = sorted(fids_by_kind.get(kind, []))
        if not fids:
            continue
        for r in range(1, reads + 1):
            seed = f"t26-{name}-read{r}-v1"
            items = reg.lexicon_items(fids, seed=seed)
            b = chunker.make_batch("extract_lex", FAMILY, items, seed=seed, prompt=LEX_PROMPT, max_items=50)
            out.append((f"{name}-read{r}", _finalize(b, f"{name}-read{r}", LEX_PROMPT)))
    return out


FIELDS_G3H = (g3h.Field("requester", "name", "the person who sent the request, as written"),
              g3h.Field("counterparty", "name", "the company the request comes from, as written"),
              g3h.Field("change", "category", "the change the request asks for",
                        S.category_slot("bank_details", P.CHANGE_SET).params),
              g3h.Field("req_id", "id", "the request reference, as written"))


def g3h_batch(freeform_pieces: list) -> tuple:
    """One G3-H round-trip item per surviving Mode F document: the text and the field schema only. The expected values
    stay in the key file (orchestrator side), as plugin.extract_view would give them."""
    surface_to_key = {s: k for k, surfs in P.CHANGE_SET.items() for s in surfs}
    items, expected = [], {}
    for p in freeform_pieces:
        f = p["item"]["facts"]
        iid = p["internal_id"]
        items.append((iid, g3h.extraction_item(p["answer"]["text"], list(FIELDS_G3H))))
        expected[iid] = {"requester": S.canonical(S.name_slot(f["REQUESTER"])),
                         "counterparty": S.canonical(S.name_slot(f["COUNTERPARTY"])),
                         "change": surface_to_key[f["CHANGE"]],
                         "req_id": S.canonical(S.id_slot(f["REQ_ID"]))}
    b = chunker.make_batch("extract_g3h", FAMILY, items, seed="t26-g3h-freeform-v1", prompt=G3H_PROMPT, max_items=50)
    return _finalize(b, "g3h-freeform", G3H_PROMPT), expected


# ------------------------------------------------------------------------------------------------ main

def _write(batch: chunker.TaskBatch) -> None:
    paths.write_files(EXTRACT, batch.files())


def run() -> dict:
    batches, tasks = rebuild_and_check()
    pieces, coverage = load_pieces(batches, tasks)
    lint_all(pieces)
    dedup_pass(pieces)
    held = designate_held_out_packs(pieces)
    reg, added, refused = build_registry(pieces)

    by_pool = defaultdict(lambda: {"answered": 0, "kept": 0, "dropped": 0, "reasons": Counter()})
    for p in pieces:
        d = by_pool[p["pool"]]
        d["answered"] += 1
        if p["problems"]:
            d["dropped"] += 1
            for msg in p["problems"]:
                d["reasons"][msg.split(":", 1)[0] if msg.startswith(("G-SL", "dedup", "registry")) else msg] += 1
        else:
            d["kept"] += 1

    surv = [p for p in pieces if not p["problems"]]
    wording_ok = [p for p in surv if p["pool"] == "wording"]
    prec_ok = [p for p in surv if p["pool"] == "precedence"]
    fids_by_kind = {"question": [], "precedence": []}
    for fid, f in reg.forms.items():
        if f.unit_ok:
            fids_by_kind["question" if f.kind == "question" else "precedence"].append(fid)
    lex = lex_batches(reg, fids_by_kind)
    freeform_ok = [p for p in surv if p["pool"] in ("freeform", "freeform_heldout")]
    g3, g3_expected = g3h_batch(freeform_ok)

    # write the chunk files (each independent read is its own chunk file)
    for _name, b in lex:
        _write(b)
    _write(g3)
    task_rows = []
    for name, b in lex:
        for c in b.chunks:
            task_rows.append({"task_file": str(EXTRACT / b.chunk_path(c["task_id"])), "answer_file": c["answer_file"],
                              "kind": b.kind, "pool": c["pool"], "batch_id": b.batch_id, "n_items": len(c["items"]),
                              "prompt_sha": b.prompt_sha})
    for c in g3.chunks:
        task_rows.append({"task_file": str(EXTRACT / g3.chunk_path(c["task_id"])), "answer_file": c["answer_file"],
                          "kind": g3.kind, "pool": c["pool"], "batch_id": g3.batch_id, "n_items": len(c["items"]),
                          "prompt_sha": g3.prompt_sha})
    counts_tasks = {}
    for t in task_rows:
        counts_tasks[t["pool"]] = counts_tasks.get(t["pool"], 0) + t["n_items"]
    paths.write_json(EXTRACT / "TASKS.json", {"family": FAMILY, "version": "v1", "n_tasks": len(task_rows),
                                              "items_per_pool": counts_tasks, "tasks": task_rows})

    # orchestrator-only files: the lint log, the survivors, the registry, and the G3-H expected values
    log = {"coverage": {k: {kk: vv for kk, vv in v.items()} for k, v in coverage.items()},
           "per_pool": {k: {"answered": v["answered"], "kept": v["kept"], "dropped": v["dropped"],
                            "drop_reasons": dict(v["reasons"].most_common())} for k, v in by_pool.items()},
           "dropped": [{"pool": p["pool"], "internal_id": p["internal_id"], "task_id": p["task_id"],
                        "problems": p["problems"]} for p in pieces if p["problems"]],
           "registry_refused": refused}
    paths.write_json(ORCH / "lint_log.json", log)
    paths.write_json(ORCH / "survivors.json", [{"pool": p["pool"], "internal_id": p["internal_id"],
                                                "task_id": p["task_id"], "prompt_sha": p["prompt_sha"],
                                                "meta": p["meta"], "held_out": p.get("held_out"),
                                                "value": _value(p)} for p in surv])
    paths.write_json(ORCH / "registry.json", {"registry": reg.to_json(), "lex_status": lex_status(reg),
                                              "forms_needing_admission": fids_by_kind})
    paths.write_json(ORCH / "g3h_expected.json", g3_expected)

    summary = {
        "answer_files": {p: {"tasks_returned": coverage[p]["tasks"] - len(coverage[p]["missing_tasks"]),
                             "tasks_total": coverage[p]["tasks"], "missing_tasks": coverage[p]["missing_tasks"],
                             "items": coverage[p]["items"], "answered": coverage[p]["answered"]} for p in POOLS},
        "per_pool": {k: {"answered": v["answered"], "kept": v["kept"], "dropped": v["dropped"],
                         "drop_reasons": dict(v["reasons"].most_common())} for k, v in by_pool.items()},
        "packs": {"kept": len(held), "held_out": sum(1 for p in held if p.get("held_out")),
                  "training": sum(1 for p in held if not p.get("held_out"))},
        "skins_by_register_tone": {f"{r}|{t}": n for (r, t), n in Counter(
            (p["meta"]["register"], p["meta"]["tone"]) for p in surv if p["pool"] in ("skin", "skin_heldout")).items()},
        "wordings_pending_by_form": dict(Counter(p["meta"]["qform"] for p in wording_ok)),
        "precedence_pending": len(prec_ok),
        "registry": {"forms": len(reg.forms), "added": dict(added), "refused": len(refused),
                     "unit_ok": sum(1 for f in reg.forms.values() if f.unit_ok),
                     "unit_fail": sum(1 for f in reg.forms.values() if f.unit_ok is False),
                     "forms_needing_admission": {k: len(v) for k, v in fids_by_kind.items()}},
        "extraction_tasks": [{"pool": t["pool"], "kind": t["kind"], "n_items": t["n_items"]} for t in task_rows],
        "g3h_items": len(g3_expected),
        "lex_reads": {"question_reads": 2, "precedence_reads": 3},
        "tasks_written": task_rows,
    }
    return summary


def main(argv=None) -> int:
    summary = run()
    print(json.dumps(summary, indent=1, default=str, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
