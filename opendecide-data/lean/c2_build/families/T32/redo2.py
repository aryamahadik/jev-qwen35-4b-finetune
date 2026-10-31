"""families/T32/redo2.py: the T32 Mode F REDO2 round (G0_SPEC v2.1 R13 and section 7; C2_DATA_SPEC 3.0, 6.3;
PREREG A37 (b), A38). After A38 only: every write goes through paths.write_files / write_json / write_jsonl.

Why (Stage A admit, pools/MANIFEST.json): 12 of 120 round-1 Mode F intros survived. The round-1 briefs gave OWNER as a
bare name, so 67 intros named OWNER only as a participant and the G3-H read (owner = the person the text says saved or
shared the chat) returned NONE; four registers described the intro instead of being it. Two fixed round-1 checks also
dropped 9 intros whatever their wording: authoring.check_freeform swaps in the owner "Kofi" and then refuses any text
that still holds facts["OWNER"] (an item whose OWNER is Kofi can never pass), and SKIN_BANNED holds "release" while
vocab.TOPICS holds "the quarterly release". authoring.py and vocab.py are NOT edited. This round:

  1. states the saver role in every item brief (G0 v2.1 R13: OWNER is the member the text says saved, exported or
     shared the chat) and asks for the intro itself, never a description of one;
  2. uses as sample facts only names and topics that pass the fixed checks: at build, every item's facts must pass
     check_freeform (and the stricter lint below) on the register's own shape sentence, so the swap-probe owner and
     a topic holding a SKIN_BANNED word never reach Haiku;
  3. lints every intro STRICTER than round 1 before G3-H: authoring.check_freeform (unchanged) + the intro read as a
     Mode T skin (its two fact spans become {OWNER} / {TOPIC}) through authoring.check_skin (unchanged: the G-SL
     skin role, the family extras, the fill / parse round trip) + a role lint (OWNER right next to a save or share
     word; no word that describes a text or places OWNER in the chat) + dedup by template against round 1, the
     admitted Mode T skins and this round;
  4. reads G3-H with the round-1 contract unchanged (extract.G3H_PROMPT, extract.G3H_FIELDS, g3h.compare) and the 98%
     bar per template, template = register within this round. Round-1 quarantines stand: no round-1 intro is revived.

  stage    when                              writes (under haiku/redo2/)
  build    now (2 tasks: training, held-out) author/{chunks,key,manifest,prompts,answers/README.txt}, REDO2_TASKS.json
  extract  after both authoring answers      lint_log.json, pool/{intros,g3h_expected}.jsonl, extract/, REDO2_TASKS.json
  score    after the extraction answers      g3h_result.json, pool/{freeform_pass,freeform_held_pass}.jsonl

  ../../.venv/bin/python -m families.T32.redo2 build|extract|score [--write]      (from lean/c2_build; dry run default)

Nothing here sets or reads a gold label; Haiku answers only drop intros. Merging the passing intros into pools/ is a
later freeze decision (not done here).
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, paths  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from families.T32 import authoring as A  # noqa: E402
from families.T32 import extract as X  # noqa: E402
from families.T32 import plugin as P  # noqa: E402
from families.T32 import vocab as V  # noqa: E402

FAMILY = "T32"
ROUND = "redo2"
ROOT = HERE / "haiku" / "redo2"
AUTHOR_ROOT = ROOT / "author"
EXTRACT_ROOT = ROOT / "extract"
POOL_ROOT = ROOT / "pool"
SEED = "t32-redo2-v1"
ROUND1_INTROS = HERE / "haiku" / "extract" / "pool" / "freeform.jsonl"     # round-1 lint survivors (dedup only)
MODE_T_SKINS = (HERE / "pools" / "skins.jsonl", HERE / "pools" / "skins_held.jsonl")

TRAIN_REGS = ("family_chat", "landlord_tenant", "freelance_client", "team_chat", "flatmates", "club_volunteers",
              "support_thread")            # every round-1 training register except email_digest (12/12 admitted)
HELD_REGS = ("sms_export", "forum_thread")   # 0 held-out intros were admitted in round 1
ITEMS_PER_REGISTER, PER_ITEM = 4, 3
REG_TOPICS = {   # vocab.TOPICS keys that fit the register's settings (the value is swapped at fill anyway)
    "family_chat": ("family_reunion", "anniversary_party", "summer_holiday", "garden_project"),
    "landlord_tenant": ("lease_renewal", "flat_repairs", "move_out_checklist", "house_move"),
    "freelance_client": ("brand_refresh", "website_launch", "video_project", "fundraising_drive"),
    "team_chat": ("office_move", "hiring_push", "website_launch", "video_project"),
    "flatmates": ("spring_cleanup", "flat_repairs", "move_out_checklist", "garden_project"),
    "club_volunteers": ("fair_planning", "club_anniversary", "fundraising_drive", "spring_cleanup"),
    "support_thread": ("house_move", "website_launch", "lease_renewal", "office_move"),
    "sms_export": ("summer_holiday", "flat_repairs", "anniversary_party", "fair_planning"),
    "forum_thread": ("garden_project", "club_anniversary", "spring_cleanup", "family_reunion"),
}
REG_ROLE = {"family_chat": ("saved", "shared"), "landlord_tenant": ("saved", "forwarded"),
            "freelance_client": ("saved", "shared"), "team_chat": ("exported", "shared"),
            "flatmates": ("saved", "shared"), "club_volunteers": ("shared", "forwarded"),
            "support_thread": ("shared", "forwarded"), "sms_export": ("backed up", "saved"),
            "forum_thread": ("posted", "shared")}
REG_FORMAT = {   # register -> (what the text is, one shape sentence with <OWNER> / <TOPIC>); every shape passes lint()
    "family_chat": ("one or two plain sentences at the top of a family group chat, written by the family member who "
                    "saved or shared it", "Family chat about <TOPIC>, saved by <OWNER> for the family."),
    "landlord_tenant": ("one or two sentences at the top of messages between tenants and their landlord or letting "
                        "agent, as copied into a rental record",
                        "Messages with the letting agent about <TOPIC>, forwarded by <OWNER> for the rental file."),
    "freelance_client": ("one sentence at the top of a freelancer and client message thread, as pasted into a "
                         "project log", "Client thread on <TOPIC>, saved to the project log by <OWNER>."),
    "team_chat": ("the top of a work team's channel export: two short parts on separate rows, the channel with its "
                  "topic, then who exported it; or one sentence", "Team channel: <TOPIC>\nExported by <OWNER>."),
    "flatmates": ("a casual sentence at the top of a flatmates' group chat, as the flatmate who saved it would "
                  "write it",
                  "Our flat chat about <TOPIC>, saved by <OWNER>."),
    "club_volunteers": ("a short sentence at the top of a club or volunteer committee group chat, as shared with the "
                        "committee", "Committee chat on <TOPIC>, shared with the volunteers by <OWNER>."),
    "support_thread": ("the top of a chat attached to a help-desk case: one sentence, or two or three 'Field: value' "
                       "pairs, one per row (no case number)", "Attached chat: <TOPIC>\nShared by: <OWNER>"),
    "sms_export": ("the top of a text-message thread backed up from a phone: one or two short parts, one per row",
                   "Text thread on <TOPIC>\nBacked up by <OWNER> from a phone."),
    "forum_thread": ("the top of a neighbourhood or hobby forum post that reposts the chat: a short opening with "
                     "the topic, then a sentence on the next row",
                     "Reposted chat: <TOPIC>\nPosted here by <OWNER> for the forum."),
}

# ================================================================================================ role lint (stricter)
ROLE_VERBS = ("saved", "exported", "shared", "forwarded", "posted", "reposted", "backed up", "copied", "pasted",
              "uploaded", "attached", "passed on")
_VERB_RE = "|".join(re.escape(v).replace(r"\ ", r"[ \t]+") for v in ROLE_VERBS)
ROLE_BEFORE = re.compile(r"(?i)\b(?:" + _VERB_RE + r")\b(?:[ \t]+(?:[A-Za-z'-]+|\{TOPIC\})){0,6}?[ \t]+by:?[ \t]+$")
ROLE_AFTER = re.compile(r"(?i)^[ \t]+(?:(?:has|just)[ \t]+)?(?:" + _VERB_RE + r")\b")
DESCRIBE_WORDS = {"header", "headers", "heading", "headline", "title", "titled", "subject", "description",
                  "described", "describes", "caption", "intro", "introduction", "entry", "line", "lines", "note",
                  "notes", "list", "listed", "listing", "lists", "mention", "mentions", "mentioned", "mentioning",
                  "named", "naming", "names", "appear", "appears", "appeared", "appearing", "include", "includes",
                  "included", "including", "member", "members", "participant", "participants", "contact", "source"}


def role_lint(template: str) -> list:
    """Problems of one intro template ({OWNER} / {TOPIC} in place of the facts) under the redo2 role rule."""
    i = template.find("{OWNER}")
    if i < 0:
        return ["no {OWNER} span"]
    p = []
    before, after = template[:i], template[i + len("{OWNER}"):]
    if after.startswith(("'s", "’s")):
        p.append("OWNER written as a possessive")
    elif not (ROLE_BEFORE.search(before) or ROLE_AFTER.match(after)):
        p.append("OWNER is not right next to a save or share word (the text must say OWNER saved or shared the chat)")
    bad = {w.lower() for w in A._words(template)} & DESCRIBE_WORDS
    if bad:
        p.append(f"describes the text or OWNER's place in the chat {sorted(bad)}")
    return p


def to_template(text: str, facts: dict) -> str:
    """The intro with its OWNER and TOPIC spans replaced by {OWNER} / {TOPIC} (each fact exactly once)."""
    spans = []
    for name, (a, b) in ((n, s[0]) for n, s in K.locate(text, facts).items() if len(s) == 1):
        spans.append((a, b, name))
    if len(spans) != len(facts):
        raise ValueError("a fact does not appear exactly once")
    out = text
    for a, b, name in sorted(spans, reverse=True):
        out = out[:a] + "{" + name + "}" + out[b:]
    return out


def lint(register: str, text, facts: dict, sid: str = "probe-r2", task_id: str = "probe",
         prompt_sha: str = "0" * 64) -> tuple:
    """(template or None, problems): check_freeform (unchanged) + check_skin on the template (unchanged) + role_lint."""
    sk, pr = A.check_freeform(register, text, facts, sid=sid, task_id=task_id, prompt_sha=prompt_sha)
    if pr:
        return None, ["mode F: " + x for x in pr]
    try:
        tpl = to_template(text, facts)
    except ValueError as e:
        return None, [f"template: {e}"]
    _sk2, q = A.check_skin(register, tpl, sid=sid + "-t")
    pr = ["as skin: " + x for x in q] + ["role: " + x for x in role_lint(tpl)]
    return (None if pr else tpl), pr


def _norm(t: str) -> str:
    return " ".join(t.casefold().split())


# ================================================================================================ build (authoring)
PROMPT = (
    "You write short free-form intros for a dataset. Each intro sits at the top of an exported group chat; a program "
    "prints the chat itself after your intro and a blank line. Your text IS the intro: write the words a reader sees "
    "there, never a description of them.\n"
    "Each item gives a register (the kind of text) and two facts:\n"
    "  OWNER  the first name of the chat member who saved, exported or shared this chat;\n"
    "  TOPIC  what the chat is about: a lower-case phrase that already starts with 'the'.\n"
    "Every intro must say who saved or shared the chat: put the OWNER name right next to a save or share word, as in "
    "'saved by <OWNER>', 'shared by <OWNER>', 'exported by <OWNER>', 'forwarded by <OWNER>', 'posted by <OWNER>', "
    "'backed up by <OWNER>', 'Shared by: <OWNER>', '<OWNER> saved ...', '<OWNER> shared ...', '<OWNER> exported ...' "
    "or '<OWNER> posted ...'. A reader who asks 'who saved or shared this chat?' must find the name at once. An intro "
    "that only places the name in the chat ('chat with <OWNER>', '<OWNER> is in this chat', 'listing <OWNER>', a bare "
    "'from <OWNER>') is rejected.\n"
    "Copy both facts EXACTLY as given (same spelling and letter case, including the topic's 'the'), written so that "
    "any other first name and any other 'the ...' topic could stand in their place; they are the only name and topic "
    "you write. The intro is background only: a reader must learn nothing from it about who promised what or how "
    "anything went. In your answer, write the real OWNER name and TOPIC phrase, never <OWNER> or <TOPIC>.")
RULES = [
    "Each fact appears exactly once, verbatim. Never write 'the', 'a' or 'an' right before the topic (it already "
    "starts with 'the') and never start a sentence or a line with the topic. Words must stand between the two facts "
    "(never the topic at the end of a line and the name at the start of the next one).",
    "The OWNER name stands right next to its save or share word in every intro (at most a few words between that "
    "word and 'by'); never write it with 's.",
    "Write the intro itself, never words about it or about who is in the chat: none of header, heading, title, "
    "subject, description, caption, intro, entry, line, note, list, mention, named, listed, appears, includes, member, "
    "participant, contact, source.",
    "Add no fact: never mention a task, a job, an event, a promise, an agreement, a request, a date, a deadline, an "
    "extension, a result, who did what, or how many people or messages there are. Never use these words in any form: "
    "promise, commitment, commit, agree, agreement, deadline, task, job, event, extension, release, retract, owe, "
    "outcome, result, status, verdict, honour, honor, fulfil, delay, postponed, decided, decision, request, deliver.",
    "Write no name other than the OWNER, no place, company or brand, no digit, no amount, and " + A.NO_FACT_WORDS
    + ".",
    "No quantity or frequency word (all, every, each, some, any, both, either, several, many, few, more, most, only, "
    "always, never, usually, whole, entire, single, extra, another, total).",
    "No modal (must, may, might, can, could, should, will, would, need, have to, able, allowed, required), no hedge "
    "(maybe, perhaps, probably, likely, think, believe, seems, appears, almost) and no condition word (if, unless, "
    "except, otherwise, instead, provided).",
    "No status word (" + A.STATUS_WORDS + ") and no negation of any kind (not, n't, no, never, nothing, none, nobody, "
    "without, nor, neither).",
    "No capitalised word except at the start of a sentence or line, right after a colon, or the OWNER name; 'I' is "
    "fine. No line may start with 'Members:', 'Chat log' or 'Chat export'.",
    "At most 3 lines and 25 words; most intros 8 to 16 words. No blank line, no bullet, no placeholder and no curly "
    "brace.",
    "The intros of an item differ from each other in structure and wording, not only in one or two words.",
]
OUTPUT = (
    "OUTPUT. Write ONLY the answer file named in this task file's \"answer_file\" field (the same path is repeated at "
    "the end of these instructions), with the Write tool: one JSON array with exactly one object per item, in item "
    "order. Each object has exactly two keys: {\"qid\": \"<the item's qid, copied exactly>\", \"intros\": [\"<intro "
    "1>\", \"<intro 2>\", \"<intro 3>\"]} (exactly " + str(PER_ITEM) + " strings per item). Valid JSON only: escape "
    "an inner double quote as \\\" and write a newline inside an intro as \\n; no comments, no markdown fence, no "
    "text before or after the array. Read no other file and run no other tool.")
FULL_PROMPT = PROMPT + "\n\nRULES (every item):\n" + "\n".join(f"R{i + 1}. {r}" for i, r in enumerate(RULES)) + \
    "\n\n" + OUTPUT


def _fill(shape: str, owner: str, topic: str) -> str:
    return shape.replace("<OWNER>", owner).replace("<TOPIC>", topic)


def safe_values() -> tuple:
    """(names, topic keys, excluded {value: reason}): sample facts that pass every fixed check on a neutral role
    sentence. The swap-probe owner of check_freeform and any topic holding a SKIN_BANNED word drop out here."""
    names, topics, excluded = [], [], {}
    for n in A.FREE_NAMES:
        _t, pr = lint("flatmates", f"Group chat about the house move, saved by {n}.", {"OWNER": n,
                                                                                     "TOPIC": "the house move"})
        (excluded.__setitem__(n, pr) if pr else names.append(n))
    for k in sorted(V.TOPICS):
        t = V.TOPICS[k]
        _t, pr = lint("flatmates", f"Group chat about {t}, saved by Priya.", {"OWNER": "Priya", "TOPIC": t})
        (excluded.__setitem__(t, pr) if pr else topics.append(k))
    return tuple(names), tuple(topics), excluded


AUTHOR_TASKS = (("free", TRAIN_REGS, 0), ("free_held", HELD_REGS, len(TRAIN_REGS) * ITEMS_PER_REGISTER))


def items(regs: tuple = TRAIN_REGS + HELD_REGS, offset: int = 0) -> list:
    """[(internal id, item)]: 4 items per register, 3 intros each; owners cycle over the safe names from `offset`."""
    names, topics, _ex = safe_values()
    out, k = [], offset
    for reg in regs:
        fmt, shape = REG_FORMAT[reg]
        for j in range(ITEMS_PER_REGISTER):
            tkey = REG_TOPICS[reg][j]
            if tkey not in topics:
                raise SystemExit(f"redo2 topic {tkey} fails the fixed checks")
            owner, verb = names[k % len(names)], REG_ROLE[reg][j % len(REG_ROLE[reg])]
            k += 1
            facts = {"OWNER": owner, "TOPIC": V.TOPICS[tkey]}
            brief = (f"Write {PER_ITEM} different intros in the register '{reg}' ({fmt}) that fit {A._fit(reg)}. "
                     f"OWNER {owner} is the chat member who {verb} this chat: every intro says so in words, with "
                     f"the name right next to a save or share word (for example '{verb} by {owner}' or '{owner} "
                     f"{verb} ...'), never only as a person in the chat. Answer field: \"intros\" (a list of "
                     f"{PER_ITEM} strings).")
            rules = [f"Rules R1-R{len(RULES)} of the instructions apply.",
                     "Shape to vary (the facts go where <OWNER> and <TOPIC> stand; write your own wording): " + shape]
            out.append((f"r2|{reg}|{j}", {"brief": brief, "register": reg, "facts": facts, "rules": rules}))
    return out


def self_check(its: list | None = None) -> list:
    """Every item's own shape, filled with its facts, must pass lint(): no fixed check can refuse the facts."""
    probs = []
    for iid, it in its or items():
        reg, f = it["register"], it["facts"]
        _t, pr = lint(reg, _fill(REG_FORMAT[reg][1], f["OWNER"], f["TOPIC"]), f)
        if pr:
            probs.append(f"{iid}: shape fails {pr}")
    return probs


def _finish(batch: chunker.TaskBatch, root: Path) -> chunker.TaskBatch:
    out = []
    for c in batch.chunks:
        ans = str(Path(root) / batch.answer_path(c["task_id"]))
        if paths.never_open(ans):
            raise chunker.ChunkError(f"answer path is on the never-open list: {ans}")
        out.append({"task_id": c["task_id"], "kind": c["kind"], "answer_file": ans,
                    "instructions": batch.prompt + f"\n\nANSWER FILE (write exactly this path): {ans}",
                    "prompt_sha": c["prompt_sha"], "items": c["items"]})
    batch.chunks = out
    return batch


def author_batches() -> list:
    """[(label, TaskBatch)]: training registers and held-out registers in separate tasks (as round 1 did), one chunk
    each, the same prompt."""
    out = []
    for label, regs, offset in AUTHOR_TASKS:
        its = items(regs, offset)
        probs = self_check(its)
        if probs:
            raise SystemExit("redo2 self-check failed: " + "; ".join(probs[:5]))
        b = chunker.make_batch("author_freeform", FAMILY, its, seed=f"{SEED}|{label}", prompt=FULL_PROMPT,
                               forbid_strings=A.FORBID_ALL)
        if len(b.chunks) != 1:
            raise SystemExit(f"redo2 authoring {label}: {len(b.chunks)} chunks (one task)")
        out.append((label, _finish(b, AUTHOR_ROOT)))
    return out


def _task_rows(stage: str, kind: str, b: chunker.TaskBatch, root: Path, per_item: int) -> list:
    rows = []
    for c in b.chunks:
        tid = c["task_id"]
        r, w = b.allowed(str(root), tid)
        rows.append({"stage": stage, "kind": kind, "task_id": tid, "batch_id": b.batch_id,
                     "task_file": str(root / b.chunk_path(tid)), "answer_file": c["answer_file"],
                     "n_items": len(c["items"]), "planned_outputs": per_item * len(c["items"]),
                     "prompt_sha": b.prompt_sha, "allowed_read": sorted(r), "allowed_write": sorted(w)})
    return rows


def _verify(b: chunker.TaskBatch, root: Path) -> None:
    m = json.loads((root / "manifest" / f"{b.batch_id}.json").read_text(encoding="utf-8"))
    k = json.loads((root / "key" / f"{b.batch_id}.json").read_text(encoding="utf-8"))["key"]
    mine = b.manifest()
    if mine["tasks"] != m["tasks"] or mine["prompt_sha"] != m["prompt_sha"] or k != b.key:
        raise SystemExit(f"{b.batch_id}: rebuilt batch differs from the manifest / key on disk")


def _index(rows: list, extra: dict | None = None) -> dict:
    return {"family": FAMILY, "round": ROUND, "seed": SEED, "g0_sha256": P.T32.G0_SHA256,
            "note": ("Mode F redo2 (G0 v2.1 R13, section 7). Stage 'author' runs now; stage 'extract' (G3-H, round-1 "
                     "contract) is built by `python -m families.T32.redo2 extract --write` once both authoring answers "
                     "exist; `score` applies the 98% bar per register within this round. Haiku answers only drop "
                     "intros; no label exists here."),
            "tasks": rows, **(extra or {})}


def _author_rows(batches: list) -> list:
    return [r for _label, b in batches for r in _task_rows("author", "author_freeform", b, AUTHOR_ROOT, PER_ITEM)]


def build(write: bool) -> dict:
    batches = author_batches()
    rows = _author_rows(batches)
    _names, _topics, excluded = safe_values()
    its = [it for _label, b in batches for c in b.chunks for it in c["items"]]
    counts = {"items": len(its), "planned_intros": PER_ITEM * len(its),
              "items_by_register": dict(Counter(it["register"] for it in its)),
              "owners_used": sorted({it["facts"]["OWNER"] for it in its}),
              "topics_used": sorted({it["facts"]["TOPIC"] for it in its}),
              "sample_values_excluded_by_fixed_checks": excluded}
    if write:
        files = {}
        for _label, b in batches:
            files.update(b.files())
        files["answers/README.txt"] = ("Haiku answer files for the redo2 authoring tasks (see ../../REDO2_TASKS.json). "
                                       "Written only by the task agents.\n")
        paths.write_files(AUTHOR_ROOT, files)
        paths.write_json(ROOT / "REDO2_TASKS.json", _index(rows))
    return {"counts": counts, "tasks": rows, "written": write}


# ================================================================================================ extract (G3-H build)
def _round1_templates() -> set:
    seen = set()
    if ROUND1_INTROS.exists():
        for line in ROUND1_INTROS.read_text(encoding="utf-8").splitlines():
            d = json.loads(line)
            try:
                seen.add(_norm(to_template(d["out"], d["facts"])))
            except ValueError:
                seen.add(_norm(d["out"]))
    for p in MODE_T_SKINS:
        if p.exists():
            seen |= {_norm(json.loads(line)["text"]) for line in p.read_text(encoding="utf-8").splitlines()}
    return seen


def lint_answers(batches: list, raw: dict, seen: set | None = None) -> tuple:
    """(pieces, problems). batches: [(label, TaskBatch)]; raw: {task_id: the parsed answer array}. Pieces keep their
    problems; ok pieces go to G3-H."""
    seen = set(seen or ())
    pieces, probs = [], []
    for _label, b in batches:
        tids = {c["task_id"] for c in b.chunks}
        p2, pr = _lint_batch(b, {t: a for t, a in raw.items() if t in tids}, seen)
        pieces += p2
        probs += pr
    return pieces, probs


def _lint_batch(b: chunker.TaskBatch, raw: dict, seen: set) -> tuple:
    got, probs = chunker.load_answers(b, raw)
    inv = chunker.item_by_internal(b)
    pieces = []
    for iid in sorted(inv):
        it = inv[iid]
        a = got.get(iid)
        texts = a.get("intros") if isinstance(a, dict) else None
        if not isinstance(texts, list):
            probs.append(f"{iid}: no intros list")
            texts = []
        if len(texts) != PER_ITEM:
            probs.append(f"{iid}: {len(texts)} intros (asked {PER_ITEM})")
        reg = it["register"]
        for n, text in enumerate(texts[:PER_ITEM]):
            pid = f"{iid}|{n}"
            tpl, pr = lint(reg, text, it["facts"], sid=pid, task_id=b.chunks[0]["task_id"],
                           prompt_sha=b.prompt_sha)
            if tpl is not None:
                key = _norm(tpl)
                if key in seen:
                    pr = ["dedup: template already in round 1, the Mode T skins or this round"]
                    tpl = None
                else:
                    seen.add(key)
            pieces.append({"iid": pid, "register": reg, "facts": it["facts"],
                           "settings": list(A.REGISTER_SETTINGS.get(reg, A.ALL_SETTINGS)),
                           "held_out": reg in A.HELD_REGISTERS, "raw": text, "out": text if tpl else None,
                           "template": tpl, "ok": tpl is not None, "problems": pr,
                           "task_id": b.chunks[0]["task_id"], "prompt_sha": b.prompt_sha, "round": ROUND})
    return pieces, probs


def g3h_batch(pieces: list) -> chunker.TaskBatch | None:
    ok = [p for p in pieces if p["ok"]]
    if not ok:
        return None
    its = [(p["iid"], g3h.extraction_item(p["out"], list(X.G3H_FIELDS))) for p in ok]
    b = chunker.make_batch("extract_g3h", FAMILY, its, seed=f"{SEED}|g3h-r1", prompt=X.G3H_PROMPT)
    return _finish(b, EXTRACT_ROOT)


def _load_author_answers(batches: list) -> dict:
    raw = {}
    for c in (c for _label, b in batches for c in b.chunks):
        ap = Path(c["answer_file"])
        try:
            raw[c["task_id"]] = json.loads(ap.read_text(encoding="utf-8"))
        except FileNotFoundError:
            raise SystemExit(f"no authoring answer yet: {ap}") from None
        except json.JSONDecodeError as e:
            raise SystemExit(f"authoring answer is not valid JSON ({ap}): {e}") from None
    return raw


def _authored() -> tuple:
    batches = author_batches()
    for _label, b in batches:
        _verify(b, AUTHOR_ROOT)
    pieces, probs = lint_answers(batches, _load_author_answers(batches), _round1_templates())
    return batches, pieces, probs


def extract(write: bool) -> dict:
    batches, pieces, probs = _authored()
    gb = g3h_batch(pieces)
    rows = _author_rows(batches)
    if gb is not None:
        rows += _task_rows("extract", "extract_g3h", gb, EXTRACT_ROOT, 1)
    reasons = Counter(r[:90] for p in pieces for r in p["problems"])
    counts = {"answer_problems": probs, "intros": len(pieces), "lint_ok": sum(p["ok"] for p in pieces),
              "lint_ok_by_register": dict(Counter(p["register"] for p in pieces if p["ok"])),
              "lint_dropped_by_register": dict(Counter(p["register"] for p in pieces if not p["ok"])),
              "drop_reasons": dict(reasons.most_common()),
              "g3h_items": 0 if gb is None else len(gb.key), "g3h_tasks": 0 if gb is None else len(gb.chunks)}
    if write:
        if gb is not None:
            files = dict(gb.files())
            files["answers/README.txt"] = ("Haiku answer files for the redo2 G3-H read (see ../../REDO2_TASKS.json). "
                                           "Written only by the task agents.\n")
            paths.write_files(EXTRACT_ROOT, files)
        paths.write_jsonl(POOL_ROOT / "intros.jsonl", pieces)
        paths.write_jsonl(POOL_ROOT / "g3h_expected.jsonl",
                          [{"pid": p["iid"], "register": p["register"], "expect": X.g3h_expect(p)}
                           for p in pieces if p["ok"]])
        paths.write_json(ROOT / "lint_log.json", {"counts": counts, "drops": [
            {"pid": p["iid"], "register": p["register"], "raw": p["raw"], "reasons": p["problems"]}
            for p in pieces if not p["ok"]]})
        paths.write_json(ROOT / "REDO2_TASKS.json", _index(rows))
    return {"counts": counts, "tasks": rows, "written": write}


# ================================================================================================ score (G3-H bar)
def score_reads(pieces: list, gb: chunker.TaskBatch, raw: dict) -> dict:
    """g3h.compare per intro against the generator facts; template = register within this round (98% bar)."""
    got, probs = chunker.load_answers(gb, raw)
    ok_pieces = [p for p in pieces if p["ok"]]
    res, per = [], {}
    for p in ok_pieces:
        a = got.get(p["iid"])
        ok, diffs = (False, ["unanswered"]) if a is None else g3h.compare(X.g3h_expect(p), a, list(X.G3H_FIELDS))
        per[p["iid"]] = {"ok": ok, "diffs": diffs}
        res.append((f"{ROUND}:{p['register']}", p["iid"], ok))
    rep = g3h.template_report(res)
    passed = [p for p in ok_pieces if p["iid"] not in set(rep["drop_rows"])]
    return {"answer_problems": probs, "per_intro": per, "report": rep, "passed": passed}


def _pool_row(p: dict) -> dict:
    return {"id": p["iid"], "family": FAMILY, "kind": "freeform", "register": p["register"],
            "settings": p["settings"], "held_out": p["held_out"], "text": p["out"], "facts": p["facts"],
            "task_id": p["task_id"], "prompt_sha": p["prompt_sha"], "g3h": "pass", "round": ROUND}


def score(write: bool) -> dict:
    _batches, pieces, _probs = _authored()
    gb = g3h_batch(pieces)
    if gb is None:
        raise SystemExit("no intro passed the redo2 lint: nothing to score")
    _verify(gb, EXTRACT_ROOT)
    raw = {}
    for c in gb.chunks:
        ap = Path(c["answer_file"])
        try:
            raw[c["task_id"]] = json.loads(ap.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            raise SystemExit(f"G3-H answer {ap}: {e}") from None
    out = score_reads(pieces, gb, raw)
    if out["answer_problems"]:
        raise SystemExit("G3-H answer problems: " + "; ".join(out["answer_problems"][:10]))
    rep = out["report"]
    train = [p for p in out["passed"] if not p["held_out"]]
    held = [p for p in out["passed"] if p["held_out"]]
    counts = {"g3h_intros": len(out["per_intro"]), "g3h_mismatch": sum(not v["ok"] for v in out["per_intro"].values()),
              "templates": {k: [v["ok"], v["n"], round(v["rate"], 3), v["quarantined"]]
                            for k, v in rep["templates"].items()},
              "quarantined": rep["quarantined"], "pass_training": len(train), "pass_held_out": len(held)}
    if write:
        paths.write_json(ROOT / "g3h_result.json", {"counts": counts, "bar": rep["bar"], "per_intro": out["per_intro"],
                                                    "template_rule": "register within round redo2; round-1 "
                                                                     "quarantines stand"})
        paths.write_jsonl(POOL_ROOT / "freeform_pass.jsonl", [_pool_row(p) for p in train])
        paths.write_jsonl(POOL_ROOT / "freeform_held_pass.jsonl", [_pool_row(p) for p in held])
    return {"counts": counts, "written": write}


def main(argv: list) -> int:
    stage = argv[0] if argv and not argv[0].startswith("-") else "build"
    write = "--write" in argv
    fn = {"build": build, "extract": extract, "score": score}.get(stage)
    if fn is None:
        print("usage: python -m families.T32.redo2 build|extract|score [--write]")
        return 2
    res = fn(write)
    print(json.dumps({k: v for k, v in res.items() if k != "tasks"}, indent=1, ensure_ascii=False, default=str))
    for t in res.get("tasks", []):
        print(f"{t['stage']}: {t['task_file']} -> {t['answer_file']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
