"""c2_build/families/T29/extract.py: the T29 Haiku EXTRACTION round after the authoring round (haiku/author/).

Runs after A38 only. Every write goes through paths.write_files / write_jsonl / write_json, which refuse before A38.
Steps (C2_DATA_SPEC 6.3 and 6.4; G0_SPEC 2 and 5; PREREG A37 (b), A38):
  1. collect  the 33 authoring answers. authoring.build_tasks() rebuilds the same deterministic batches and keys as the
              files on disk; chunker.load_answers maps every answer to its item. Nothing is written here.
  2. lint     G-SL per piece (failing pieces are dropped, each with its reasons):
              - Mode T skins, attack lines and question wordings: gsl.lint_template (roles skin, attack, wording);
              - Mode F documents: gsl.lint_freeform (every slot value verbatim, no number, date, id, currency sign,
                gold-label word or negation cue outside the values), plus each slot value exactly once (the brief says
                "exactly once"), plus the spec's outside-slot word lists through gsl._word_hits (relative time,
                quantity, quantifier, modal, hedge, status, operator, name, date, gold-label words and phrases);
              - lexicon clauses (comparator, precedence, confirmation): the wording role of gsl.lint_template, the
                gold-label words and phrases (the precedence tier word "forbidden" is allowed), and the B20 surface
                rules of the confirmation bank (explicit: no question, no negation, no condition word; mention: no
                agreement or instruction word). check_row does not lint clause text, so this is the G-SL pass for it;
              - packs and action names: name_slot / id_slot, gsl.lint_values, and the brief's structure rules.
  3. dedup    exact duplicates of the normalised text inside each pool (packs: org domain; action names: the name);
              the first copy is kept.
  4. lex      the surviving lexicon forms (comparators, precedence, confirmation phrases, question wordings) go into a
              LexiconRegistry with their declared meanings. Haiku source, with task id and prompt sha. Then the unit
              test (lexicon.unit_test). A form that fails is dropped with its problems.
  5. tasks    G-LEX extraction: one independent read per batch. Reads glex-r1 and glex-r2 cover every form; glex-r3
              covers the precedence forms (3/3). Each read is its own batch, so each read is its own chunk file.
              G3-H: one extraction read per surviving Mode F document (G0_SPEC 2: "G-SL fact-lock + G3-H").
  6. write    haiku/extract/: tasks/, answers/ (empty until the agents write), chunks/, prompts/, key/, manifest/,
              TASKS.json; pool/ (the survivors, orchestrator side); lint_log.json (the drop reasons).

  ../.venv/bin/python -m families.T29.extract            (from lean/c2_build: dry run, prints counts, writes nothing)
  ../.venv/bin/python -m families.T29.extract --write    (after A38: writes the files above)
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, gsl, paths  # noqa: E402
from c2_kit import lexicon as LX  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.skin import make_skin  # noqa: E402
from families.T29 import authoring as A  # noqa: E402
from families.T29 import plugin as P  # noqa: E402

FAMILY = "T29"
VERSION = "v1"
ROOT = HERE / "haiku" / "extract"
LABEL = tuple(P.T29Plugin.LABEL_WORDS)
LABEL_NO_TIER = tuple(w for w in LABEL if w != "forbidden")     # the precedence line must name the tier "forbidden"
NAME_ALLOW = tuple(P.T29Plugin.NAME_ALLOW)
SLOT_KIND = {"REQUESTER": "name", "REASON": "category", "ACTION": "id", "TARGET": "id"}
MODE_F_WORDS = {"name"}
OUTSIDE_WORDS = {"number", "relative_time", "quantity", "quantifier", "modal", "hedge", "status", "operator", "date",
                 "name", "gold_label"}
AGREEMENT = re.compile(r"(?<![a-z])(?:yes|yeah|yep|sure|okay|ok|fine|confirmed|confirm|agreed|agree|do it|run it|"
                       r"go ahead|please continue|proceed)(?![a-z])", re.I)
CONDITION = re.compile(r"(?<![a-z])(?:if|unless|once|when|whenever|provided|providing|after|as long as|only if|"
                       r"except|otherwise)(?![a-z])", re.I)
ENV_CLASS = {"production", "staging", "sandbox", "development", "test", "testing", "personal", "public", "internal",
             "finance", "support", "platform", "sales", "legal", "research"}
SNAKE = re.compile(r"[a-z]+(?:_[a-z]+){1,3}")
DOMAIN_EX = re.compile(r"[a-z]+(?:-[a-z]+)?\.example")
LOOKALIKE = re.compile(r"[a-z][a-z-]*\.(?:example|test)")
PREFIX = re.compile(r"[A-Z]{2,4}")
PERSON = re.compile(r"[A-Z][a-z]+ [A-Z][a-z]+")

WORD_ID = re.compile(r"t29-v1-word-(?P<qf>.+)-\d{2}$")
WORDHELD_ID = re.compile(r"t29-v1-wordheld-(?P<qf>.+)$")
CMP_ID = re.compile(r"t29-v1-cmp-(?P<sem>cmp\.[a-z]+)-(?P<typ>count|cents)$")
PREC_ID = re.compile(r"t29-v1-prec-(?P<i>\d+)$")
CONF_ID = re.compile(r"t29-v1-conf-(?P<i>\d+)$")
ACT_ID = re.compile(r"t29-v1-act-(?P<effect>[a-z]+)-(?P<tone>routine|drastic)$")

PREC_SEM = P.PREC_SEM
CONF_SEMS = ("conf.t29.explicit", "conf.t29.mention")
QUESTION_MEANING = {
    "ch_verdict": "asks which outcome the policy gives for the call, picked from a list shown after the question",
    "ch_rule": "asks which numbered rule decides the outcome for the call",
    "yn_go": "asks whether the agent may run the call straight away, with no further step first",
    "yn_not_go": "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
    "yn_go_framed": "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
    "yn_ask": "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
    "yn_ask_framed": "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
    "yn_refuse": "asks whether the agent must turn the call down outright, because the policy bars it",
    "yn_permitted": "asks whether the policy allows the call at all, straight away or after the user confirms it",
    "yn_not_forbidden": "asks whether the policy does NOT bar the call",
}
SEMS = (
    ("cmp.gt", "comparator", "strictly more than the bound: the bound itself does not count"),
    ("cmp.ge", "comparator", "the bound or more: the bound itself counts"),
    ("cmp.lt", "comparator", "strictly less than the bound: the bound itself does not count"),
    ("cmp.le", "comparator", "the bound or less: the bound itself counts"),
    ("prec.t29.forbid_confirm_default", "precedence",
     "forbidden rules beat needs-confirmation rules, which beat the default"),
    ("prec.t29.confirm_over_forbid", "precedence",
     "needs-confirmation rules beat forbidden rules, which beat the default"),
    ("prec.t29.first_listed", "precedence", "the first listed rule that applies decides the outcome"),
    ("conf.t29.explicit", "confirmation",
     "the user clearly and unconditionally tells the agent to run the named call on the named target"),
    ("conf.t29.mention", "confirmation",
     "the user only asks about or refers to the named call and does not agree to it"),
)


def _ans(fmt: str) -> str:
    return ("Answer format: one JSON array with one object per item (every item answered once):\n" + fmt +
            "\nCopy each qid exactly.\n")


AGENT_RULES = ("How to work: this task file is the only file you may open. Do not open, list or search any other file "
               "or folder. Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given "
               "at the top of this file, with the Write tool. Inside JSON strings, write a double quote as \\\" and a "
               "line break as \\n.\n")
GLEX_PROMPT = AGENT_RULES + """
TASK: READ EACH TEXT ALONE and pick the ONE CHOICE whose meaning the text expresses. Each item gives a TEXT (one short
phrase or sentence, with its values already filled in) and CHOICES (a list of meanings).

Rules:
1. Use only the TEXT and its CHOICES. Do not guess beyond the words, and do not add a condition, a default or any
   fact from outside the text.
2. Copy the chosen CHOICE exactly, character for character, from that item's own list. Never write a new meaning.
3. Answer every item exactly once.
""" + _ans('[{"qid": "<qid of the item>", "meaning": "<the chosen choice, copied exactly>"}, ...]')

G3H_PROMPT = AGENT_RULES + """
TASK: READ ONE DOCUMENT and extract two fields from it. Each item gives a TEXT (a short free-form document) and a SCHEMA
with two fields:
- requester: the full personal name of the person who asks for the work, copied exactly as written in the TEXT.
- reason: the piece of work the request belongs to. Its CHOICES are listed in the schema. Copy the one choice the TEXT
  names, exactly as written in the choices. If the TEXT names none of the choices, write NONE.

Rules: copy exactly; do not correct spelling; do not infer anything; answer every item exactly once.
""" + _ans('[{"qid": "<qid of the item>", "requester": "<name copied as written>", "reason": "<one choice, or NONE>"}, '
           '...]')

G3H_FIELDS = (
    g3h.Field("requester", "name", "the person who makes the request, as written in the document"),
    g3h.Field("reason", "category", "the piece of work the request belongs to",
              S.category_slot("audit", P.REASONS).params),
)


# ------------------------------------------------------------------------------------------------ helpers

def _norm(t) -> str:
    return " ".join(str(t).casefold().split())


def _reasons(viols) -> list:
    return [f"{v.rule}: {v.detail}" for v in viols]


# ------------------------------------------------------------------------------------------------ 1. collect

def collect(tasks: list) -> tuple:
    """({group: [piece dict]}, {group: authored count}). Pieces are the outputs of the 33 authoring answers."""
    groups = {g: [] for g in ("skins", "attack", "freeform", "lexicon", "packs", "actions")}
    for t in tasks:
        data = json.loads(t.answer_file().read_text(encoding="utf-8"))
        out, probs = chunker.load_answers(t.batch, {t.task_id: data})
        if probs:
            raise SystemExit(f"{t.name}: answers do not map to their items: {probs[:3]}")
        by_int = chunker.item_by_internal(t.batch)
        for iid in sorted(out):
            a, it = out[iid], by_int[iid]
            base = {"task": t.name, "task_id": t.task_id, "prompt_sha": t.batch.prompt_sha, "item": iid,
                    "held_out": bool(t.held_out)}
            if t.name in ("pack-a", "pack-b"):
                groups["packs"].append({**base, "pid": iid, "pack": a["pack"]})
            elif t.name == "actions":
                m = ACT_ID.match(iid)
                for k, name in enumerate(a["names"]):
                    groups["actions"].append({**base, "pid": f"{iid}#{k:02d}", "text": name,
                                              "effect": m.group("effect"), "tone": m.group("tone")})
            elif t.kind == "author_skin":
                group = "attack" if t.name == "attack" else "skins"
                role = "attack" if t.name == "attack" else "skin"
                reg = it["register"]
                escape = reg if reg in ("json", "yaml") else "text"
                decl = {s: SLOT_KIND[s] for s in it["slots"]}
                for k, text in enumerate(a["texts"]):
                    groups[group].append({**base, "pid": f"{iid}#{k:02d}", "text": text, "role": role, "decl": decl,
                                          "register": reg, "escape": escape})
            elif t.kind == "author_freeform":
                groups["freeform"].append({**base, "pid": iid, "text": a["text"], "facts": it["facts"],
                                           "register": it["register"]})
            elif t.kind == "author_wording":
                m = WORD_ID.match(iid) or WORDHELD_ID.match(iid)
                qf = m.group("qf")
                for k, text in enumerate(a["wordings"]):
                    groups["lexicon"].append({**base, "pid": f"{iid}#{k:02d}", "text": text, "lexkind": "question",
                                              "qform": qf, "sem": LX.question_sem(FAMILY, qf),
                                              "slots": {"ACTION": "id", "TARGET": "id"}, "role": "wording"})
            elif t.kind == "author_lexicon":
                if CMP_ID.match(iid):
                    m = CMP_ID.match(iid)
                    lexkind, sem, typ = "comparator", m.group("sem"), m.group("typ")
                    slots = {"X": typ}
                elif PREC_ID.match(iid):
                    lexkind, sem, slots = "precedence", PREC_SEM, {}
                elif CONF_ID.match(iid):
                    i = int(CONF_ID.match(iid).group("i"))
                    lexkind, sem, slots = "confirmation", A.CONF_ITEMS[i][0], {"ACT": "id", "TGT": "id"}
                else:
                    raise SystemExit(f"unknown lexicon item {iid}")
                for k, text in enumerate(a["forms"]):
                    groups["lexicon"].append({**base, "pid": f"{iid}#{k:02d}", "text": text, "lexkind": lexkind,
                                              "sem": sem, "slots": slots, "role": "wording"})
            else:
                raise SystemExit(f"unhandled task {t.name}")
    authored = {g: len(v) for g, v in groups.items()}
    return groups, authored


# ------------------------------------------------------------------------------------------------ 2. lint (G-SL)

def _template_skin(p: dict, role: str):
    return make_skin(p["pid"], FAMILY, p["text"], p["decl"], kind=role, register=p["register"], escape=p["escape"],
                     author_mode="T", held_out=p.get("held_out", False))


def lint_skin(p: dict) -> list:
    return _reasons(gsl.lint_template(_template_skin(p, p["role"]), label_words=LABEL, exceptions={},
                                      name_allow=NAME_ALLOW))


def _mask(text: str, occ: dict) -> str:
    """The text with every verbatim slot value replaced by the marker (the outside-slot part only)."""
    spans = sorted((a, b) for sp in occ.values() for a, b in sp)
    parts, pos = [], 0
    for a, b in spans:
        if a < pos:
            continue
        parts += [text[pos:a], gsl._MARK]
        pos = b
    parts.append(text[pos:])
    return "".join(parts)


def lint_freeform(p: dict) -> list:
    text, facts = p["text"], p["facts"]
    fills = {"REQUESTER": facts["REQUESTER"], "REASON": facts["REASON"]}
    out = _reasons(gsl.lint_freeform(text, fills, label_words=LABEL))
    occ = K.locate(text, fills)
    for name, spans in occ.items():
        if len(spans) != 1:
            out.append(f"exact_once: {name} occurs {len(spans)} time(s); the brief says once")
    # G0_SPEC 2: Mode F is the G-SL fact-lock (lint_freeform above). The full outside-slot word lists (modal,
    # quantifier, status, ...) are for Mode T narratives only, so Mode F gets the name check alone: a second
    # personal name would add a fact the brief does not give.
    out += _reasons(gsl._word_hits(_mask(text, occ), MODE_F_WORDS, LABEL, {}, NAME_ALLOW))
    return out


def lint_freeform_word_list(p: dict) -> list:
    """Informational only (never a drop): the Mode T outside-slot word lists applied to a Mode F document. The
    documents this flags are held back from the pool and listed in lint_log.json for the orchestrator's decision."""
    text, facts = p["text"], p["facts"]
    fills = {"REQUESTER": facts["REQUESTER"], "REASON": facts["REASON"]}
    return _reasons(gsl._word_hits(_mask(text, K.locate(text, fills)), OUTSIDE_WORDS, LABEL, {}, NAME_ALLOW))


def lint_lexicon(p: dict) -> list:
    kind = p["lexkind"]
    out = _reasons(gsl.lint_template(_template_skin(dict(p, register="lexicon", escape="text", decl=p["slots"]),
                                                    "wording"),
                                     label_words=LABEL, exceptions={}, name_allow=NAME_ALLOW))
    text = p["text"]
    lit = K.PH_RE.sub(" ", text)
    mark = K.PH_RE.sub(gsl._MARK, text)
    if kind in ("precedence", "confirmation"):
        labels = LABEL_NO_TIER if kind == "precedence" else LABEL
        out += _reasons(gsl._word_hits(mark, {"gold_label"}, labels, {}, ()))
    if kind == "confirmation":
        if p["sem"] == "conf.t29.explicit":
            if "?" in text:
                out.append("explicit: a question mark (B20: no question)")
            if gsl.negcount.k_all(lit):
                out.append("explicit: a negation cue (B20: no negation)")
            for m in CONDITION.finditer(lit):
                out.append(f"explicit: condition word {m.group()!r} (B20: no condition)")
        else:
            for m in AGREEMENT.finditer(lit):
                out.append(f"mention: agreement or instruction word {m.group()!r} (B20)")
    return out


def lint_pack(pk: dict) -> list:
    keys = ("org_name", "org_domain", "lookalike_domains", "partner_domains", "target_prefix", "people")
    missing = [k for k in keys if k not in pk]
    if missing:
        return [f"shape: missing {missing}"]
    out = []
    dom, look, part = pk["org_domain"], pk["lookalike_domains"], pk["partner_domains"]
    people, prefix = pk["people"], pk["target_prefix"]
    if not (isinstance(dom, str) and DOMAIN_EX.fullmatch(dom)):
        out.append(f"brief: org_domain {dom!r} is not lowercase letters (one hyphen at most) + .example")
    if not (isinstance(look, list) and len(look) == 2 and len(set(look)) == 2 and dom not in look):
        out.append("brief: lookalike_domains must be exactly two distinct domains, none equal to org_domain")
    else:
        out += [f"brief: lookalike {d!r} has the wrong shape" for d in look if not LOOKALIKE.fullmatch(str(d))]
    if not (isinstance(part, list) and len(part) == 2 and len(set(part)) == 2 and dom not in part):
        out.append("brief: partner_domains must be exactly two distinct domains, none equal to org_domain")
    else:
        out += [f"brief: partner {d!r} must end in .example" for d in part if not DOMAIN_EX.fullmatch(str(d))]
    if not (isinstance(prefix, str) and PREFIX.fullmatch(prefix)):
        out.append(f"brief: target_prefix {prefix!r} is not 2-4 capital letters")
    if not (isinstance(people, list) and len(people) == 4 and len(set(people)) == 4):
        out.append("brief: people must be exactly four distinct names")
    else:
        out += [f"brief: person {n!r} is not first + family name, letters only" for n in people
                if not PERSON.fullmatch(str(n))]
    slots = {}
    try:
        slots["org_name"] = S.name_slot(pk["org_name"])
        for i, n in enumerate(people if isinstance(people, list) else []):
            slots[f"person{i}"] = S.name_slot(n)
        for i, d in enumerate([dom] + (look if isinstance(look, list) else []) +
                              (part if isinstance(part, list) else []) + [prefix]):
            slots[f"id{i}"] = S.id_slot(d)
    except (S.SlotError, TypeError) as e:
        out.append(f"slot: {e}")
        return out
    out += _reasons(gsl.lint_values(slots))
    return out


def lint_action(p: dict) -> list:
    name = p["text"]
    if not isinstance(name, str) or not SNAKE.fullmatch(name):
        return ["shape: snake_case, 2-4 lowercase letter words joined by underscores"]
    out = []
    bad = sorted(set(name.split("_")) & ENV_CLASS)
    if bad:
        out.append(f"brief: names an environment, team or data class ({bad})")
    try:
        S.id_slot(name)
    except S.SlotError as e:
        out.append(f"slot: {e}")
    return out


def lint_all(groups: dict) -> tuple:
    """(survivors {group: [piece]}, drops [{pid, group, task_id, reasons}])."""
    checks = {"skins": lint_skin, "attack": lint_skin, "freeform": lint_freeform, "lexicon": lint_lexicon,
              "packs": lint_pack, "actions": lint_action}
    surv, drops = {g: [] for g in groups}, []
    for g, pieces in groups.items():
        for p in pieces:
            arg = p["pack"] if g == "packs" else p
            reasons = checks[g](arg)
            if reasons:
                drops.append({"pid": p["pid"], "group": g, "task_id": p["task_id"], "reasons": reasons})
            else:
                surv[g].append(p)
    return surv, drops


# ------------------------------------------------------------------------------------------------ 3. dedup

def dedup_all(surv: dict) -> tuple:
    """Exact duplicates inside each pool (the first copy is kept). Packs: org domain. Action names: the name."""
    key = {"skins": lambda p: _norm(p["text"]), "attack": lambda p: _norm(p["text"]),
           "freeform": lambda p: _norm(p["text"]), "lexicon": lambda p: _norm(p["text"]),
           "packs": lambda p: _norm(p["pack"].get("org_domain", "")),
           "actions": lambda p: _norm(p["text"])}
    kept, drops = {}, []
    for g, pieces in surv.items():
        seen, out = {}, []
        for p in pieces:
            k = key[g](p)
            if k in seen:
                drops.append({"pid": p["pid"], "group": g, "task_id": p["task_id"],
                              "reasons": [f"duplicate of {seen[k]}"]})
            else:
                seen[k] = p["pid"]
                out.append(p)
        kept[g] = out
    return kept, drops


# ------------------------------------------------------------------------------------------------ 4. lexicon

def build_registry(lex_pieces: list) -> tuple:
    """(registry, form drops). Each surviving form is added as a Haiku source; then the unit test runs."""
    reg = LX.LexiconRegistry(FAMILY)
    for sem, kind, meaning in SEMS:
        reg.declare(sem, kind, meaning)
    for qf, meaning in QUESTION_MEANING.items():
        reg.declare(LX.question_sem(FAMILY, qf), "question", meaning)
    reg.declare_antonym(LX.question_sem(FAMILY, "yn_refuse"), LX.question_sem(FAMILY, "yn_permitted"))
    drops = []
    for p in sorted(lex_pieces, key=lambda p: p["pid"]):
        try:
            reg.add(p["text"], p["sem"], slots=p["slots"], source="haiku", family=FAMILY,
                    haiku_task_id=p["task_id"], haiku_prompt_sha=p["prompt_sha"], held_out=p["held_out"])
        except LX.LexiconError as e:
            drops.append({"pid": p["pid"], "group": "lexicon", "task_id": p["task_id"], "reasons": [f"form: {e}"]})
    reg.unit_test_all()
    return reg, drops


# ------------------------------------------------------------------------------------------------ 5. tasks

def glex_items(reg: LX.LexiconRegistry, ids: list, seed: str, instance: int) -> list:
    """Gold-free extraction items, as lexicon.lexicon_items builds them, with two changes: the filled instance is
    the `instance`-th sample whose slot values are pairwise distinct (so an action and a target never read as one
    thing), and the choices are the kind's meanings in a seeded order. Each read uses another instance."""
    out = []
    for fid in sorted(ids):
        f = reg.forms[fid]
        combos = reg._samples(f)
        distinct = [c for c in combos if len({v.value for v in c.values()}) == len(c)] or combos
        vals = distinct[instance % len(distinct)]
        txt = reg.render(fid, vals)
        mean = sorted((s.meaning for s in reg.sems.values() if s.kind == f.kind),
                      key=lambda m: hashlib.sha256(f"{seed}|{fid}|{m}".encode()).hexdigest())
        out.append((fid, {"text": txt, "choices": mean}))
    return out


def make_tasks(reg: LX.LexiconRegistry, freeform: list) -> tuple:
    """(batches [(read label, kind, batch)], counts). Each read is its own batch, so its own chunk files."""
    ok = sorted(fid for fid, f in reg.forms.items() if f.unit_ok)
    prec = [fid for fid in ok if reg.forms[fid].kind == "precedence"]
    batches = []
    for instance, (label, ids) in enumerate((("glex-r1", ok), ("glex-r2", ok), ("glex-r3", prec))):
        items = glex_items(reg, ids, f"t29-extract-{VERSION}-{label}", instance)
        batches.append((label, "extract_lex",
                        chunker.make_batch("extract_lex", FAMILY, items,
                                           seed=f"t29-extract-{VERSION}-{label}", prompt=GLEX_PROMPT)))
    g3_items = [(p["pid"], g3h.extraction_item(p["text"], list(G3H_FIELDS))) for p in freeform]
    batches.append(("g3h-r1", "extract_g3h",
                    chunker.make_batch("extract_g3h", FAMILY, g3_items, seed=f"t29-extract-{VERSION}-g3h-r1",
                                       prompt=G3H_PROMPT)))
    counts = {"forms_unit_ok": len(ok), "forms_unit_fail": len(reg.forms) - len(ok),
              "forms_needing_admission_by_kind": dict(Counter(reg.forms[f].kind for f in ok)),
              "reads_per_form": {"comparator": 2, "question": 2, "confirmation": 2, "precedence": 3},
              "glex_items": {label: sum(len(c["items"]) for c in b.chunks) for label, _k, b in batches[:3]},
              "g3h_items": len(g3_items)}
    return batches, counts


def task_text(root: Path, batch, chunk: dict, read: str) -> str:
    ans = root / batch.answer_path(chunk["task_id"])
    items = json.dumps(chunk["items"], ensure_ascii=False, indent=1)
    n = len(chunk["items"])
    return (f"# T29 extraction task {chunk['task_id']}\n\n"
            f"ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):\n{ans}\n\n"
            f"Task kind: {chunk['kind']}; read: {read}; items: {n}; outputs expected: {n}.\n\n"
            f"{batch.prompt.rstrip()}\n\nITEMS (JSON; answer every item, keyed by its qid):\n{items}\n")


def files_for(root: Path, batches: list) -> tuple:
    """({relative path: text} for paths.write_files, manifest)."""
    out, rows = {}, []
    for read, kind, b in batches:
        out.update(b.files())
        for c in b.chunks:
            tid = c["task_id"]
            rel = f"tasks/{tid}.md"
            text = task_text(root, b, c, read)
            out[rel] = text
            allowed_read = {str(root / rel)} | b.allowed(str(root), tid)[0]
            rows.append({"read": read, "kind": kind, "task_id": tid, "batch_id": b.batch_id,
                         "task_file": str(root / rel), "answer_file": str(root / b.answer_path(tid)),
                         "prompt_sha": b.prompt_sha, "n_items": len(c["items"]),
                         "outputs_expected": len(c["items"]), "allowed_read": sorted(allowed_read),
                         "allowed_write": [str(root / b.answer_path(tid))]})
    manifest = {"family": FAMILY, "version": VERSION, "stage": "extract", "n_tasks": len(rows),
                "outputs_expected": sum(r["outputs_expected"] for r in rows), "tasks": rows}
    out["TASKS.json"] = json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"
    out["answers/README.txt"] = ("Haiku answer files: one <task_id>.json per extraction task (see ../TASKS.json). Written "
                                 "only by the task agents.\n")
    return out, manifest


# ------------------------------------------------------------------------------------------------ run

def run(write: bool) -> dict:
    tasks = A.build_tasks()
    probs = A.check(tasks)
    if probs:
        raise SystemExit("authoring check failed: " + "; ".join(probs[:5]))
    groups, authored = collect(tasks)
    surv, lint_drops = lint_all(groups)
    surv, dup_drops = dedup_all(surv)
    fw_flags = {p["pid"]: lint_freeform_word_list(p) for p in surv["freeform"]}
    fw_flags = {k: v for k, v in fw_flags.items() if v}
    reg, form_drops = build_registry(surv["lexicon"])
    batches, task_counts = make_tasks(reg, surv["freeform"])
    files, manifest = files_for(ROOT, batches)

    lint_by = Counter(d["group"] for d in lint_drops)
    dup_by = Counter(d["group"] for d in dup_drops)
    reason_rules = Counter(r.split(":", 1)[0] for d in lint_drops for r in d["reasons"])
    counts = {
        "pieces_authored": sum(authored.values()),
        "pieces_authored_by_group": authored,
        "lint_dropped_by_group": dict(lint_by),
        "lint_dropped_total": len(lint_drops),
        "lint_drop_reasons_by_rule": dict(reason_rules.most_common()),
        "dedup_dropped_by_group": dict(dup_by),
        "dedup_dropped_total": len(dup_drops),
        "survivors_by_group": {g: len(v) for g, v in surv.items()},
        "mode_f_word_list_flags_informational": len(fw_flags),
        "lexicon_form_drops": len(form_drops),
        "lexicon_forms_in_registry": len(reg.forms),
        "forms_by_kind": dict(Counter(f.kind for f in reg.forms.values())),
        "forms_unit_fail": len([f for f in reg.forms.values() if not f.unit_ok]),
        "forms_needing_admission": task_counts["forms_unit_ok"],
        "forms_needing_admission_by_kind": task_counts["forms_needing_admission_by_kind"],
        "reads_per_form": task_counts["reads_per_form"],
        "glex_items_per_read": task_counts["glex_items"],
        "g3h_items": task_counts["g3h_items"],
        "tasks": manifest["n_tasks"],
        "task_outputs_expected": manifest["outputs_expected"],
    }
    if write:
        paths.write_files(ROOT, files)
        paths.write_jsonl(ROOT / "pool" / "skins.jsonl", [_pool_row(p) for p in surv["skins"]])
        paths.write_jsonl(ROOT / "pool" / "attack.jsonl", [_pool_row(p) for p in surv["attack"]])
        paths.write_jsonl(ROOT / "pool" / "freeform.jsonl", [_pool_row(p) for p in surv["freeform"]])
        paths.write_jsonl(ROOT / "pool" / "packs.jsonl", [_pool_row(p) for p in surv["packs"]])
        paths.write_jsonl(ROOT / "pool" / "actions.jsonl", [_pool_row(p) for p in surv["actions"]])
        paths.write_jsonl(ROOT / "pool" / "lexicon_forms.jsonl", [_pool_row(p) for p in surv["lexicon"]])
        paths.write_json(ROOT / "pool" / "lexicon_registry.json", reg.to_json())
        paths.write_json(ROOT / "lint_log.json", {"counts": counts, "lint_drops": lint_drops,
                                                  "dedup_drops": dup_drops, "form_drops": form_drops,
                                                  "mode_f_word_list_flags_informational": fw_flags})
    return {"counts": counts, "tasks": [{"task_file": r["task_file"], "answer_file": r["answer_file"],
                                         "kind": r["kind"], "read": r["read"]} for r in manifest["tasks"]],
            "written": write}


def _pool_row(p: dict) -> dict:
    return {k: v for k, v in p.items() if not k.startswith("_")}


def main(argv: list) -> int:
    write = "--write" in argv
    res = run(write)
    print(json.dumps(res["counts"], indent=1, ensure_ascii=False))
    print(f"tasks: {len(res['tasks'])}; written: {res['written']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
