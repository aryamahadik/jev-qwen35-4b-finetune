"""families/T01/haiku/redo2/build_redo2.py: the T01 redo2 Haiku tasks (G0_SPEC.md v3, section 8 rulings H42-H47).

New tasks only: nothing existing is edited, no answer is written here, and Haiku never sees a gold, an option or a row.
Inputs are the frozen pools (families/T01/pools/), the authoring plan (haiku_author.build_batches) and the extraction
prompt (extract.GLEX_PROMPT). Every write goes through c2_kit.paths.write_files / write_json (refuses before A38).

  packs      author_pack      H46: the 18 packs that failed (same setting, name style and held-out flag) + 6 spares,
                              in two one-chunk batches: surname and vendor initials A-L in one, M-Z in the other, so
                              the two agents cannot collide; the 372 taken names and 186 taken vendors are listed
  wordings   author_wording   H42 / H44: the 12 short wording slots (7 failed the family check, 5 G-LEX rejections),
                              an a and a b item each; ch_deadline asks for the "final" date ("last" is CORE relative
                              time); the collision-prone forms get a construction rule away from their sibling form
  freeform   author_freeform  H47: the 2 documents dropped for the word "order" (same facts), an a and a b item each
  glex-r1b   extract_lex      H45: confirmation read of every admitted form (334) with realistic fills
  glex-r2b   extract_lex      H45: a second confirmation read, other realistic fills
  glex-r3b   extract_lex      H45: a third confirmation read of the window forms (35), other realistic fills

Run from lean/c2_build:
  ../../.venv/bin/python families/T01/haiku/redo2/build_redo2.py            (dry run: counts, writes nothing)
  ../../.venv/bin/python families/T01/haiku/redo2/build_redo2.py --write    (writes tasks/, chunks/, key/, plan/ ...)
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent                     # families/T01/haiku/redo2
T01_DIR = ROOT.parents[1]                                  # families/T01
C2_BUILD = T01_DIR.parents[1]                              # lean/c2_build
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, gsl, paths  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.lexicon import LexiconRegistry  # noqa: E402
from families.T01 import extract as E  # noqa: E402
from families.T01 import haiku_author as A  # noqa: E402
from families.T01 import plugin as P  # noqa: E402

FAMILY = "T01"
VERSION = "redo2-v1"
POOLS = T01_DIR / "pools"
UNIT_DAY = ("day", "days")
LEX_CHUNK = 25

# ------------------------------------------------------------------------------------------------ failed slots
FAILED_PACKS = ("t01a.pack.010", "t01a.pack.017", "t01a.pack.022", "t01a.pack.030", "t01a.pack.038", "t01a.pack.044",
                "t01a.pack.046", "t01a.pack.051", "t01a.pack.054", "t01a.pack.055", "t01a.pack.057", "t01a.pack.064",
                "t01a.pack.065", "t01a.pack.069", "t01a.pack.073", "t01a.pack.074", "t01a.pack.076", "t01a.pack.079")
N_SPARE_PACKS = 6
# wording slots: (failed item, why it failed)
FAILED_WORDINGS = (
    ("t01a.wording.ch_deadline.000", "check: 'last' (CORE relative time)"),
    ("t01a.wording.ch_deadline.004", "check: 'last' (CORE relative time)"),
    ("t01a.wording.ch_deadline.011", "check: 'last' (CORE relative time)"),
    ("t01a.wording.ch_receipt_day.007", "check: duplicate or fixture copy"),
    ("t01a.wording.yn_cash_no_report.000", "check: duplicate or fixture copy"),
    ("t01a.wording.yn_quotes.000", "check: duplicate or fixture copy"),
    ("t01a.wording.yn_quotes_without.004", "check: 'May' read as a month"),
    ("t01a.wording.yn_fail_time.004", "G-LEX rejected q.t01.yn_fail_time#bb8679bb (read as yn_not_timely)"),
    ("t01a.wording.yn_fail_time.006", "G-LEX rejected q.t01.yn_fail_time#959903e0 (read as yn_not_timely)"),
    ("t01a.wording.yn_not_over.003", "G-LEX rejected q.t01.yn_not_over#c88e5043 (read as yn_within)"),
    ("t01a.wording.yn_not_timely.003", "G-LEX rejected q.t01.yn_not_timely#9ec291d6 (read as yn_fail_time)"),
    ("t01a.wording.yn_not_timely.005", "G-LEX rejected q.t01.yn_not_timely#59a265cb (read as yn_fail_time)"),
)
FAILED_FREEFORM = ("t01a.free.email.031", "t01a.free.memo.070")

# ------------------------------------------------------------------------------------------------ prompts (additions)
_STATUS = sorted((gsl.CORE["status"] | gsl.EXTENDED["status"]) - {w for w in A.FORBID_ALL if " " not in w})
PACK_EXTRA = """

Extra rules for this round (a program rejects a pack that breaks one; these come on top of the rules above):
6. Every person's name and every vendor name you write must be NEW: never one from the TAKEN list at the end of these \
instructions, and never the same name twice anywhere in your answer.
7. Each item gives an initials range. In that pack, every person's SURNAME and the FIRST word of every vendor name \
start with a letter inside that range.
8. Name shape: each word of a person's name is one capital letter followed by lower-case letters only: no inner \
capital (as in McKay, DeVries or LeBlanc), no apostrophe (as in O'Brien), no accent; a hyphen inside a surname is fine \
(as in Smith-Jones). Vendor names are 2-3 words, each one capital letter followed by lower-case letters only: no \
hyphen, apostrophe, ampersand or digit.
9. Never use a month or weekday name or its short form in any value, also not as a first name or surname: January, \
February, March, April, May, June, July, August, September, October, November, December, Jan, Feb, Mar, Apr, Jun, \
Jul, Aug, Sep, Sept, Oct, Nov, Dec, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, Mon, Tue, Tues, \
Wed, Thu, Thur, Thurs, Fri, Sat, Sun. Never a number word or ordinal: zero to twenty, thirty, forty, fifty, sixty, \
seventy, eighty, ninety, hundred, thousand, million, billion, dozen, first to tenth, twice, thrice, half.
10. Never use any of these status or outcome words in any value, also not as a name (so never a name such as Grant or \
Block): """ + ", ".join(_STATUS) + """.
11. Never use a negation word in any value: no, not, none, nobody, nothing, nowhere, never, neither, nor, without, \
cannot, lack, fail, deny, refuse, decline, neglect, omit, prevent, hardly, scarcely, barely, few, except, unless, \
false, and the phrases "free of" and "other than" (also inside a longer word form such as "failure" or "declining").
12. Never write the letter sequence "ohs" or the letter sequence "jev" anywhere inside any value, in any letter case \
(so never names such as Mohsen or Jevtic).
13. The "cash" topic never contains the word "report".

TAKEN (already used; never write any of these as a person's name or a vendor name):
"""

WORDING_EXTRA = """

Extra rules for this round (a program rejects a question that breaks one; these come on top of the rules above):
8. Never use any of these words: last, later, next, earlier, previously, lately, soon, upcoming, overdue, past, ago, \
yet, already, now, today, tonight, tomorrow, yesterday, currently, recently, immediately, daily, weekly, morning, \
evening, night. For the final day that is still in time, say "final" or "latest".
9. No hedge words: maybe, perhaps, probably, possibly, likely, seem, seems, appear, appears, think, believe, assume, \
suppose, roughly, nearly, almost.
10. Never start the question with the word "May" (a program reads it as the month); use another opening.
11. Each item lists questions that already exist for its meaning. Write a NEW question: never copy one of them, and \
never repeat a question you write for another item."""

FREEFORM_EXTRA = """

Extra rule for this round (a program rejects a note that breaks it; it comes on top of the rules above):
7. Outside the exact PERSON, REF and TOPIC texts, never write any of these words or their plural forms: order, \
deadline, due, limit, window, period, cutoff, office, calendar, week, weekday, business day, working day, clock, hour, \
minute, date, day, rule, policy, quote, report, threshold, travel, trip, visa, stay, insurance, insurer, claim, \
purchase, vendor, supplier, cash, money, bank, teller, ledger, notice, court, appeal, filing, loss, damage, peril. \
If the TOPIC contains one of these words, write it only inside the TOPIC itself, exactly once."""

# H42 / H44: brief fixes and construction rules (meaning unchanged: these are the G0 section 8 meanings)
BRIEF_FIX = {
    "ch_deadline": ("A multiple-choice question (the options, shown separately, are dates): what is the final date on "
                    "which the document can still be filed in time? Ask for the final day that is still in time (say "
                    "'final date' or 'latest date'), never the first late day.",
                    [A.NO_NEG, "Say 'final' or 'latest' for that date; never 'last', 'later', 'next' or 'earlier'."]),
}
STEER = {   # H42: away from the sibling construction the G-LEX readers chose
    "yn_fail_time": "Make the person the one who fails, in the active voice: '... did the person fail to file the "
                    "{ACTION} ...'. Never 'fail to be filed', never 'not'.",
    "yn_fail_time+PERSON": "Make {PERSON} the one who fails, in the active voice: '... did {PERSON} fail to file the "
                           "{ACTION} ...'. Never 'fail to be filed', never 'not'.",
    "yn_not_timely": "Make the document the subject and negate 'filed in time' with 'not': for example 'Is it true that "
                     "the {ACTION} ... was not filed in time?'. Never 'did not file', never 'fail'.",
    "yn_not_over": "Use the exact words 'not over the stay limit'. Never 'not exceed', 'not above', 'not beyond' or "
                   "'not more than'.",
}


def _h(*parts) -> int:
    return int(hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()[:12], 16)


def _jsonl(path: Path) -> list:
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


# ------------------------------------------------------------------------------------------------ packs (H46)
def pack_batches() -> list:
    kept = _jsonl(POOLS / "packs.jsonl")
    taken = sorted({n for p in kept for n in p["pack"]["people"]})
    taken_v = sorted({v for p in kept for v in p["pack"]["vendors"]} | set(P.VENDORS))
    taken = sorted(set(taken) | set(P.PEOPLE) | set(P.RESERVE_PEOPLE) | {"Dana Okafor"})
    prompt = (A.PACK_PROMPT + PACK_EXTRA + "People: " + "; ".join(taken) + ".\nVendors: " + "; ".join(taken_v) + ".")
    orig = dict(A._pack_items()[0])
    orig_plan = A._pack_items()[1]
    slots = [(iid, orig[iid]["brief"], orig_plan[iid]["held_out"], iid) for iid in FAILED_PACKS]
    for k in range(N_SPARE_PACKS):
        i = 80 + k
        brief = f"Setting: {A.SETTINGS[i % len(A.SETTINGS)]}. Name style: {A.NAME_STYLES[(i * 3) % len(A.NAME_STYLES)]}."
        slots.append((f"t01a.pack.spare{k}", brief, None, None))
    out = []
    for part, (lo, hi) in enumerate((("A", "L"), ("M", "Z"))):
        items, plan = [], {}
        for j, (iid, brief, held, replaces) in enumerate(slots):
            if j % 2 != part:
                continue
            nid = "t01r2.pack." + iid.rsplit(".", 1)[1]
            items.append((nid, {"brief": f"{brief} Initials range: {lo} to {hi} (every surname and the first word of "
                                         f"every vendor name start with a letter from {lo} to {hi})."}))
            plan[nid] = {"role": "pack", "replaces": replaces, "held_out": held, "spare": replaces is None,
                         "initials": f"{lo}-{hi}"}
        b = chunker.make_batch("author_pack", FAMILY, items, seed=f"t01-{VERSION}|packs|{lo}{hi}", prompt=prompt,
                               max_items=len(items), forbid_strings=A.FORBID_ALL)
        out.append((f"packs_{lo}{hi}", b, plan))
    return out


# ------------------------------------------------------------------------------------------------ wordings (H42, H44)
def wording_batch() -> tuple:
    orig_items, orig_plan = A._wording_items()
    orig = dict(orig_items)
    admitted = Counter()
    by_q = {}
    for r in _jsonl(POOLS / "wordings.jsonl"):
        by_q.setdefault(r["qform"], []).append(r["text"])
        admitted[r["qform"]] += 1
    items, plan = [], {}
    for iid, why in FAILED_WORDINGS:
        q = orig_plan[iid]["qform"]
        kind = orig_plan[iid]["kind"]
        i = int(iid.rsplit(".", 1)[1])
        meaning, rules = BRIEF_FIX.get(q, A.WORDING_BRIEF[q])
        place = orig[iid]["rules"][-2]                         # the placeholder rule of the failed item
        copy_fail = "duplicate" in why or "fixture" in why
        for v, style_i in (("a", (i + 1) % len(A.STYLES) if copy_fail else i % len(A.STYLES)),
                           ("b", (i + 4) % len(A.STYLES))):
            style = A.STYLES[style_i].replace("{RULE}", A.RULE_NAME[kind])
            sk = q + "+PERSON" if "PERSON" in orig[iid]["slots"] and q + "+PERSON" in STEER else q
            extra = ([STEER[sk]] if sk in STEER else [])
            # a fixture question text may never reach a Haiku item (chunker forbid strings): such texts are left out
            exist = sorted(t for t in by_q.get(q, []) if not any(s.lower() in t.lower() for s in A.QSTRINGS))
            rr = list(rules) + extra + [place, f"Style hint: {style}.",
                                        "Questions that already exist for this meaning (they may use other "
                                        "placeholders; yours uses exactly the placeholders named above; write a NEW "
                                        "one and never copy one): " + " | ".join(exist)]
            nid = f"t01r2.wording.{q}.{i:03d}{v}"
            items.append((nid, {"brief": meaning, "slots": list(orig[iid]["slots"]), "rules": rr}))
            plan[nid] = {"role": "wording", "qform": q, "kind": kind, "slots": list(orig_plan[iid]["slots"]),
                         "held_out": False, "replaces": iid, "variant": v, "why_replaced": why}
    b = chunker.make_batch("author_wording", FAMILY, items, seed=f"t01-{VERSION}|wordings",
                           prompt=A.WORDING_PROMPT + WORDING_EXTRA, max_items=len(items), forbid_strings=A.QSTRINGS)
    return "wordings", b, plan


# ------------------------------------------------------------------------------------------------ freeform (H47)
def freeform_batch() -> tuple:
    orig_items, orig_plan = A._freeform_items()
    orig = dict(orig_items)
    items, plan = [], {}
    for iid in FAILED_FREEFORM:
        for v in ("a", "b"):
            nid = f"t01r2.free.{iid.split('.', 2)[2]}{v}"
            items.append((nid, dict(orig[iid])))
            plan[nid] = dict(orig_plan[iid], replaces=iid, variant=v)
    b = chunker.make_batch("author_freeform", FAMILY, items, seed=f"t01-{VERSION}|freeform",
                           prompt=A.FREEFORM_PROMPT + FREEFORM_EXTRA, max_items=len(items), forbid_strings=A.FORBID_ALL)
    return "freeform", b, plan


# ------------------------------------------------------------------------------------------------ G-LEX (H45)
def frozen_registry() -> LexiconRegistry:
    return LexiconRegistry.from_json(json.loads((POOLS / "lexicon_registry.json").read_text(encoding="utf-8")))


def realistic_values(reg, fid: str, read: str, people, actions, perils) -> tuple:
    """(values, forms) for one form and one read: pack people, filing nouns and perils, the kind's own reference,
    card-range day counts (N < M), waiting periods and thresholds, label-blind date and amount forms."""
    f = reg.forms[fid]
    kind = P.KIND_OF[f.sem_id.split(".", 2)[2]] if f.kind == "question" else None
    vals, forms = {}, {}
    pair = (P.ROLL_PAIRS + P.ROLL_PAIRS_S5)[_h(read, fid, "pair") % len(P.ROLL_PAIRS + P.ROLL_PAIRS_S5)]
    for name, _k in f.slots:
        h = _h(read, fid, name)
        if name == "PERSON":
            vals[name] = S.name_slot(people[h % len(people)])
        elif name == "REF":
            vals[name] = S.id_slot(f"{P.REF_PREFIX[kind]}-{1000 + h % 9000}")
        elif name in ("REF_DATE", "DAY"):
            vals[name] = S.date_slot(P.DATE_LO + dt.timedelta(days=h % P.DATE_SPAN))
            forms[name] = S.FREE_FORMS["date"][(h // 7) % len(S.FREE_FORMS["date"])]
        elif name == "ACTION":
            vals[name] = S.name_slot(actions[h % len(actions)])
        elif name == "PERIL":
            vals[name] = S.name_slot(perils[h % len(perils)])
        elif f.sem_id == "win.rolling_cap" and name in ("N", "M"):
            vals[name] = S.count_slot(pair[0] if name == "N" else pair[1], UNIT_DAY)
        elif f.sem_id == "win.later_anchor" and name == "N":
            ns = P.ANCHOR_N + P.ANCHOR_N_S5
            vals[name] = S.count_slot(ns[h % len(ns)], UNIT_DAY)
        elif f.sem_id == "win.wait_after" and name == "W":
            vals[name] = S.count_slot(P.WAIT_DAYS[h % len(P.WAIT_DAYS)], UNIT_DAY)
        elif f.kind == "comparator" and name == "X":
            th = sorted(set(P.PURCHASE_THRESHOLDS) | set(P.CASH_THRESHOLDS))
            vals[name] = S.cents_slot(th[h % len(th)])
            forms[name] = S.FREE_FORMS["cents"][(h // 7) % len(S.FREE_FORMS["cents"])]
        else:
            raise ValueError(f"{fid}: no realistic value for slot {name}")
    if len({str(v.value) for v in vals.values()}) != len(vals):
        raise ValueError(f"{fid}: slot values are not distinct")
    return vals, forms


def glex_batches(reg) -> list:
    packs = _jsonl(POOLS / "packs.jsonl")
    people = sorted({n for p in packs for n in p["pack"]["people"]})
    actions = sorted({p["pack"]["filing"]["action"] for p in packs})
    perils = sorted({x for p in packs for x in p["pack"]["perils"]})
    admitted = sorted(fid for fid in reg.forms if reg.status(fid) == "admitted")
    win = [fid for fid in admitted if reg.forms[fid].kind == "window"]
    out = []
    for read, ids in (("glex-r1b", admitted), ("glex-r2b", admitted), ("glex-r3b", win)):
        seed = f"t01-{VERSION}-{read}"
        items, plan = [], {}
        for fid in ids:
            f = reg.forms[fid]
            vals, forms = realistic_values(reg, fid, read, people, actions, perils)
            txt = reg.render(fid, vals, forms)
            mean = sorted((s.meaning for s in reg.sems.values() if s.kind == f.kind),
                          key=lambda m: hashlib.sha256(f"{seed}|{fid}|{m}".encode()).hexdigest())
            items.append((fid, {"text": txt, "choices": mean}))
            plan[fid] = {"read": read, "kind": f.kind, "sem_id": f.sem_id, "filled": txt}
        b = chunker.make_batch("extract_lex", FAMILY, items, seed=seed, prompt=E.GLEX_PROMPT, max_items=LEX_CHUNK)
        out.append((read, b, plan))
    return out


# ------------------------------------------------------------------------------------------------ task files
CONTRACT = {
    "author_pack": ('{"qid": "<the item\'s qid>", "pack": {"people": [6 names], "topics": {"rolling": "...", "anchor": '
                    '"...", "waiting": "...", "purchase": "...", "cash": "...", "notice": "..."}, "filing": {"action": '
                    '"...", "event_a": "... date", "event_b": "... date"}, "perils": [3 phrases], "vendors": [3 names]}}',
                    ("qid", "pack")),
    "author_wording": ('{"qid": "<the item\'s qid>", "text": "<the question, ending with ?>"}', ("qid", "text")),
    "author_freeform": ('{"qid": "<the item\'s qid>", "text": "<the note; \\n for a line break>"}', ("qid", "text")),
    "extract_lex": ('{"qid": "<the item\'s qid>", "meaning": "<the chosen choice, copied exactly>"}', ("qid", "meaning")),
}


def task_text(b, chunk: dict, label: str, task_file: Path, answer_file: Path) -> str:
    n = len(chunk["items"])
    shape, keys = CONTRACT[b.kind]
    items = "\n".join(json.dumps(it, ensure_ascii=False) for it in chunk["items"])
    return "\n".join([
        f"REDO2 TASK {chunk['task_id']}  (family {FAMILY}, kind {b.kind}, {label}, {n} items)", "",
        "This one text file is your whole task. Read all of it, then write the answer file, then stop.",
        "Do not open, list, search or write any other file or folder. Create no other file. Do not put the answer in "
        "chat;", "when the answer file is written, reply with the single word DONE.", "",
        f"TASK FILE (this file)                 : {task_file}",
        f"ANSWER FILE (write exactly this path) : {answer_file}", "",
        "=== ANSWER CONTRACT (exact) ===",
        "Write ONE JSON array to the ANSWER FILE with the Write tool, and nothing else in that file: no markdown fence, "
        "no", "comment, no wrapper object, no extra text before or after the array.",
        f"- The array has exactly {n} objects, one for each of the {n} items below, every qid exactly once (any order).",
        f"- Each object has exactly these keys and no others: {', '.join(repr(k) for k in keys)}.",
        "- \"qid\": the item's qid, copied character for character. It is an opaque label; read nothing into it.",
        "- Inside a JSON string write a double quote as \\\" and a line break as \\n. Valid JSON only.",
        "- Not allowed: any other key (such as \"note\", \"reason\" or \"confidence\"); a skipped qid; a qid used "
        "twice; a qid", "  that is not in the items below.",
        f"Shape of one object: {shape}", "",
        "=== INSTRUCTIONS ===", b.prompt.rstrip(), "",
        f"=== ITEMS ({n}; one JSON object per line; every item needs one answer object carrying its qid) ===", items, ""])


def build() -> dict:
    reg = frozen_registry()
    groups = []
    for name, b, plan in pack_batches():
        groups.append((name, "author", b, plan))
    name, b, plan = wording_batch()
    groups.append((name, "author", b, plan))
    name, b, plan = freeform_batch()
    groups.append((name, "author", b, plan))
    for read, b, plan in glex_batches(reg):
        groups.append((read, "extract", b, plan))
    files, tasks = {}, []
    for label, stage, b, plan in groups:
        files.update(b.files())
        files[f"plan/{b.batch_id}.json"] = json.dumps({"batch_id": b.batch_id, "label": label, "kind": b.kind,
                                                       "plan": plan}, indent=1, sort_keys=True,
                                                      ensure_ascii=False) + "\n"
        for c in b.chunks:
            tid = c["task_id"]
            tf, af = ROOT / "tasks" / f"{tid}.txt", ROOT / b.answer_path(tid)
            files[f"tasks/{tid}.txt"] = task_text(b, c, label, tf, af)
            tasks.append({"task_file": str(tf), "answer_file": str(af), "kind": b.kind, "stage": stage, "label": label,
                          "batch_id": b.batch_id, "task_id": tid, "n_items": len(c["items"]),
                          "outputs_expected": len(c["items"]), "prompt_sha": b.prompt_sha,
                          "audit_allowed_read": [str(tf)], "audit_allowed_write": [str(af)]})
    for t in tasks:
        for p in (t["task_file"], t["answer_file"]):
            if paths.never_open(p):
                raise SystemExit(f"never-open path in the task list: {p}")
    return {"files": files, "tasks": tasks, "reg": reg, "groups": groups}


INGEST = {   # orchestrator side (needs an ingestion step; nothing here admits anything)
    "audit": "audit.audit_jsonl per agent transcript with the task's audit_allowed_read / audit_allowed_write; a failed "
             "audit discards that agent's answers. Map answers with chunker.load_answers(batch, {task_id: answer}) "
             "using key/<batch_id>.json; plan/<batch_id>.json holds the per-item meta.",
    "glex-r1b|glex-r2b|glex-r3b": "H45: on the frozen registry (pools/lexicon_registry.json) record each answer with "
                                  "reg.record_extraction(form_id, read, reg.meaning_to_sem(kind, meaning)); an answer "
                                  "that is not one of the item's choices records None (rejects). A form is used only "
                                  "if reg.status == admitted AND it has every confirmation read (r1b, r2b; + r3b for "
                                  "window forms); a missing answer leaves the form unused, never admitted.",
    "packs_AL|packs_MZ": "H46: haiku_author.validate_pack + extract.lint_pack, then the cross-pack check against the "
                         "62 kept packs (no person or vendor repeats, case-insensitive). Each failed slot takes its own "
                         "replacement (plan 'replaces'); if that fails, the first passing spare (sorted id) takes the "
                         "slot and its held_out flag. At most one pack per failed slot; unused spares are not kept.",
    "wordings": "H42/H44: haiku_author.check_wording with the plan meta (qform, kind, slots; the 'seen' set seeded with "
                "every admitted wording text); variant a first, b only if a fails; at most one per failed slot. A kept "
                "text then needs two realistic-fill G-LEX reads (2/2; built after these answers return) before use.",
    "freeform": "H47: haiku_author.check_freeform with the plan facts; variant a first, b only if a fails; then one "
                "g3h-r1 read (g3h.extraction_item with extract._g3h_fields) and g3h.compare against the facts.",
}


def main(argv: list) -> int:
    res = build()
    counts = Counter((t["label"], t["kind"]) for t in res["tasks"])
    items = Counter()
    for t in res["tasks"]:
        items[t["label"]] += t["n_items"]
    summary = {"tasks": len(res["tasks"]), "tasks_by_label": {f"{a}|{k}": n for (a, k), n in sorted(counts.items())},
               "items_by_label": dict(sorted(items.items())), "files": len(res["files"])}
    print(json.dumps(summary, indent=1))
    if "--write" in argv:
        man = {"family": FAMILY, "version": VERSION, "g0_sha256": P.T01.G0_SHA256, "n_tasks": len(res["tasks"]),
               "outputs_expected": sum(t["outputs_expected"] for t in res["tasks"]),
               "builder": str(Path(__file__).resolve()),
               "builder_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "registry_sha256": res["reg"].sha256(), "ingest": INGEST, "tasks": res["tasks"]}
        res["files"]["TASKS.json"] = json.dumps(man, indent=1, ensure_ascii=False) + "\n"
        res["files"]["answers/README.txt"] = ("Haiku answer files: one <task_id>.json per redo2 task (see ../TASKS.json). "
                                              "Written only by the task agents.\n")
        paths.write_files(ROOT, res["files"])
        print(f"written under {ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
