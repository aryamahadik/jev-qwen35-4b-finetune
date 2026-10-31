"""families/T24/extract_stage.py: the T24 lint, dedup and extraction-task stage (G0_SPEC section 3; C2_DATA_SPEC 6.2 item 2,
6.3 G-SL, G-LEX, G3-H). A new file; every write goes through paths.write_files, which refuses before A38.

  1. authoring.load(): the 24 Haiku authoring answers -> pieces (packs, lexicon forms, question wordings, skins, Mode F
     documents).
  2. Lint, piece by piece: the family checkers (authoring.check_pack / check_skin / check_freeform / check_form /
     check_wording), the G-SL linters (gsl.lint_template for skins and wordings, gsl.lint_freeform for Mode F, gsl.lint_values
     for the sample values), and the hard rules of each authoring prompt (rule_problems below). A failing piece is dropped
     with its reason in LINT_LOG.json.
  3. Dedup on normalised text (packs on prefix and title). Lexicon forms and wordings also go through LexiconRegistry.add
     (duplicate text) and the unit test over the whole registry (ambiguity). A failing form is dropped and the registry
     rebuilt until nothing else fails.
  4. G-LEX read tasks: every surviving clause form and question wording is read by two independent Haiku extractors; the
     window forms (the precedence and window rules, lexicon kind "window") by three. Each read is its own batch (own seed,
     own qids, own order), so the reads of one form sit in separate chunk files and never share an agent. The closed list
     of meanings for a question wording is authoring.Q_MEANING, the meaning each wording was asked to carry (see
     QUESTION_CHOICES). Haiku only flags: a form is admitted only from the extraction answers (lexicon.record_extraction,
     a later step).
  5. G3-H read tasks: one read per surviving Mode F document (g3h.extraction_item, field "customer", as
     P.T24Plugin.extract_fields). The expected value per document is in pieces.json (orchestrator only).

Outputs under haiku/extract/ (paths.write_files): chunks/, prompts/, key/ and manifest/ (chunker.TaskBatch.files), plus
TASKS.json (the task list the orchestrator spawns from), LINT_LOG.json (every drop and its reason), pieces.json (the
survivors, orchestrator only), registry_pre_glex.json (the registry before extraction) and answers/README.txt.

  ../../.venv/bin/python -I families/T24/extract_stage.py [--dry]     (from lean/c2_build; --dry writes nothing)
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, gsl, lexicon, paths  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.lexicon import LexiconRegistry, question_sem  # noqa: E402
from families.T24 import authoring as A  # noqa: E402
from families.T24 import fixtures as FX  # noqa: E402
from families.T24 import plugin as P  # noqa: E402

OUT = HERE / "haiku" / "extract"
FAMILY = P.FAMILY
VERSION = "v1"
WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’-]*")
CAP_RE = re.compile(r"[A-Za-z][A-Za-z'’-]*")

NUM_WORDS = {w.lower() for w in gsl.CORE.get("number", set()) | gsl.EXTENDED.get("number", set())}
DATE_WORDS = {w.lower() for w in set(gsl.MONTHS) | set(gsl.WEEKDAYS) if w != "May"}     # "may" is a modal: "May" only
DATE_CAP_RE = re.compile(r"\bMay\b")
FORM_HEDGES = ("about", "around", "roughly", "nearly", "almost", "approximately", "usually")       # LEX_PROMPT rule 4
WORDING_HEDGES = ("maybe", "probably", "seems", "seem", "likely", "think")                        # WORDING_PROMPT rule 1
WORDING_TIME = ("today", "now", "currently", "already", "yet", "soon", "later")                  # WORDING_PROMPT rule 1
FREE_TIME = ("today", "tomorrow", "now", "soon", "later", "earlier", "yesterday", "recently")    # FREEFORM rule 3
GENDER = ("he", "she", "his", "her", "him", "hers", "himself", "herself")                         # FREEFORM rule 2
OLD_NEW_RE = re.compile(r"\b(new|old|revised|updated)\s+(rules?|policy|policies|versions?|terms)\b", re.I)
OLD_NEW_STATE_RE = re.compile(r"\b(rules?|policy|policies|versions?)\s+(has|have|was|were|been)\s+(been\s+)?"
                              r"(updated|changed|revised)\b", re.I)

GLEX_PROMPT = """TASK: name the meaning of each text. Each item gives "text" (one line: a clause of an invented
customer-service policy, or a question about the outcome for one case) and "choices" (the possible meanings for that kind
of text). For each item, pick the ONE choice whose meaning the text states, read exactly as written.

Rules:
1. Read the whole text. Words such as "not", "do not qualify", "fail to", "instead", "both dates included", "at least",
   "exactly", "more than" and "below" change the meaning, so take them into account.
2. Copy the chosen choice exactly, character for character, from that item's "choices" list. Never write a meaning that is
   not in the list, and never leave an item unanswered.
3. This task file and its prompt are the only files you may open. Do not open, list or search any other file or folder.
4. Write your whole answer, and nothing else, as one JSON array to answers/<task_id>.json (the task_id is in the chunk file;
   the answers folder sits beside the chunks folder), with the Write tool:
   [{"qid": "<qid of the item>", "meaning": "<the chosen choice, copied exactly>"}, ...]
   One object per item, each qid copied exactly.
"""

G3H_PROMPT = """TASK: read each free-form document and return one field from it. Each item gives "text" (a short document a
customer or a support agent wrote about a case) and "schema" (the one field to return, with its description).

Rules:
1. Use only the document text. For the field "customer", return the full name of the person who raised the case, copied
   character for character from the document (the spelling, capitals and spacing as written). If the document names no such
   person, return null.
2. Answer every item once.
3. This task file and its prompt are the only files you may open. Do not open, list or search any other file or folder.
4. Write your whole answer, and nothing else, as one JSON array to answers/<task_id>.json (the task_id is in the chunk file;
   the answers folder sits beside the chunks folder), with the Write tool:
   [{"qid": "<qid of the item>", "customer": "<the name exactly as written, or null>"}, ...]
   One object per item, each qid copied exactly.
"""


def norm(t: str) -> str:
    return " ".join(t.casefold().split())


def cap_mid(text: str, allowed: set) -> list:
    """Capitalised words that do not start a sentence, line, list item or label (and are not allowed)."""
    out = []
    for m in CAP_RE.finditer(text):
        w = m.group()
        if w[0].islower() or w == "I" or w in allowed:
            continue
        pre = text[:m.start()].rstrip(" \t")
        if not pre or pre[-1] in ".!?:\n-\"'(":
            continue
        out.append(w)
    return out


def form_rule_problems(text: str) -> list:
    """LEX_PROMPT hard rules that the family checkers do not already enforce."""
    probs = []
    low = K.PH_RE.sub(" ", text).lower()
    toks = re.findall(r"[a-z]+", low)
    h = [t for t in toks if t in FORM_HEDGES]
    if h:
        probs.append(f"hedge {h[0]!r} (rule 4)")
    if '"' in text:
        probs.append("double quote character (rule 4)")
    if re.search(r"\b(a|an)\s*\{", text, re.I):
        probs.append("a/an directly before a placeholder (rule 2)")
    if re.search(r"\{N\}\s+days?\b", text):
        probs.append("'days' after {N} (rule 2)")
    n = [t for t in toks if t in NUM_WORDS]
    if n:
        probs.append(f"number word {n[0]!r} (rule 3)")
    d = [t for t in toks if t in DATE_WORDS]
    if d:
        probs.append(f"month or weekday {d[0]!r} (rule 3)")
    if DATE_CAP_RE.search(K.PH_RE.sub(" ", text)):
        probs.append("month 'May' (rule 3)")
    return probs


def wording_rule_problems(text: str) -> list:
    """WORDING_PROMPT hard rules that the family checkers do not already enforce."""
    probs = []
    n = len(WORD_RE.findall(text))
    if not 8 <= n <= 30:
        probs.append(f"{n} words, want 8-30 (rule 1)")
    low = text.lower()
    toks = re.findall(r"[a-z]+", low)
    h = [t for t in toks if t in WORDING_HEDGES]
    if h:
        probs.append(f"hedge {h[0]!r} (rule 1)")
    tm = [t for t in toks if t in WORDING_TIME]
    if tm:
        probs.append(f"time word {tm[0]!r} (rule 1)")
    if "this case" not in low and "the case" not in low:
        probs.append("no 'this case' or 'the case' (rule 2)")
    if re.search(r"\b(new|old) policy\b", low) or {"update", "updated", "draft"} & set(toks):
        probs.append("new/old policy, update or draft (rule 3)")
    caps = [t for t in CAP_RE.findall(text)[1:] if t[0].isupper() and t != "I"]
    if caps:
        probs.append(f"capital letter after the first word: {caps[0]!r} (rule 6)")
    return probs


def skin_rule_problems(text: str) -> list:
    """SKIN_PROMPT rule 7 (adjacency only: the words new, old, revised, updated next to rules or versions)."""
    if OLD_NEW_RE.search(text) or OLD_NEW_STATE_RE.search(text):
        return ["new/old/revised/updated rules or versions (rule 7)"]
    return []


def freeform_rule_problems(text: str, customer: str) -> list:
    """FREEFORM_PROMPT hard rules that lint_freeform does not already enforce."""
    probs = []
    n = len(WORD_RE.findall(text))
    if not 25 <= n <= 80:
        probs.append(f"{n} words, want 25-80 (rule 1)")
    cnt = len(re.findall(re.escape(customer), text))
    if cnt != 1:
        probs.append(f"customer name written {cnt} times, want exactly once (rule 2)")
    toks = re.findall(r"[a-z]+", text.lower())
    g = [t for t in toks if t in GENDER]
    if g:
        probs.append(f"gendered pronoun {g[0]!r} (rule 2)")
    tm = [t for t in toks if t in FREE_TIME]
    if tm:
        probs.append(f"time word {tm[0]!r} (rule 3)")
    name_toks = set(CAP_RE.findall(customer))
    caps = cap_mid(text, name_toks)
    if caps:
        probs.append(f"capitalised word mid-sentence {caps[0]!r} (rule 2 and 6)")
    probs += skin_rule_problems(text)
    return probs


def slots_for(sem: str) -> dict:
    return FX.AMT_SLOTS if sem.startswith("t24.amt.") else FX.SLOT_KINDS[sem]


# The closed list for question kind: the meaning each wording was asked to carry (authoring.Q_MEANING). The fixture
# meanings (FX.QUESTION_MEANINGS) are not used: yn_same, yn_not_change and yn_fail_change there state the same answer
# rule, so a blind reader could not tell them apart. Q_MEANING keeps the surface difference (which negation or verb).
QUESTION_CHOICES = {qf: re.sub(r"\s*\(e\.g\.[^)]*\)", "", A.Q_MEANING[qf]).strip() for qf in P.T24Plugin.QFORMS}


def declare_all(reg: LexiconRegistry) -> None:
    for sem, kind, meaning in FX.SEMS:
        reg.declare(sem, kind, meaning)
    for qf in P.T24Plugin.QFORMS:
        reg.declare(question_sem(FAMILY, qf), "question", QUESTION_CHOICES[qf])


def build(forms: list, wordings: list):
    """A registry of the surviving forms (Haiku source) and the rejects of LexiconRegistry.add (duplicate text etc.)."""
    reg = LexiconRegistry("T24-haiku")
    declare_all(reg)
    by_fid, rej = {}, []
    for p in forms + wordings:
        sem = p["sem"] if "sem" in p else question_sem(FAMILY, p["qform"])
        slots = {} if reg.sems[sem].kind == "question" else slots_for(sem)
        try:
            f = reg.add(p["text"], sem, slots=slots, source="haiku", family=FAMILY, haiku_task_id=p["task_id"],
                        haiku_prompt_sha=p["prompt_sha"], held_out=bool(p["held_out"]))
            by_fid[f.form_id] = p
        except lexicon.LexiconError as e:
            rej.append((p, f"add: {e}"))
    return reg, by_fid, rej


def admit_filter(forms: list, wordings: list, drop) -> tuple:
    """Rebuild and unit-test until no form fails. Returns (registry, {form id: piece}, forms, wordings)."""
    while True:
        reg, by_fid, rej = build(forms, wordings)
        fails = {}
        for p, why in rej:
            fails[id(p)] = (p, why)
        for fid in sorted(reg.forms):
            if not reg.unit_test(fid):
                p = by_fid[fid]
                why = reg.forms[fid].unit_problems[0] if reg.forms[fid].unit_problems else "failed"
                fails[id(p)] = (p, "unit test: " + why)
        if not fails:
            return reg, by_fid, forms, wordings
        for p, why in fails.values():
            drop(p["pool"], p, why)
        gone = set(fails)
        forms = [p for p in forms if id(p) not in gone]
        wordings = [p for p in wordings if id(p) not in gone]


def main(argv: list) -> int:
    dry = "--dry" in argv
    pools, load_probs = A.load(A.ROOT)
    if load_probs:
        print("\n".join(load_probs))
        return 1
    log: list = []

    def drop(pool, p, reason):
        log.append({"pool": pool, "task_id": p["task_id"], "iid": p["iid"], "reason": reason})

    stats = {k: {"in": len(v), "kept": 0, "dropped": 0} for k, v in pools.items()}
    kept = {"packs": [], "skins": [], "freeform": [], "forms": [], "wordings": []}

    # ---- packs (G0 3.4): R2 format, check_domain, prefix and title dedup
    seen_pre, seen_title = set(), set()
    for p in pools.get("packs", []):
        dom, probs = A.check_pack(p["pack"])
        if not probs:
            pre, title = dom.prefix.upper(), norm(dom.title)
            if pre in seen_pre:
                probs = [f"duplicate prefix {pre}"]
            elif title in seen_title:
                probs = ["duplicate title"]
        if probs:
            drop("packs", p, "; ".join(probs))
            continue
        seen_pre.add(pre)
        seen_title.add(title)
        kept["packs"].append(dict(p, pool="packs"))

    # ---- skins (Mode T, G0 3.2): check_skin = G-SL lint_template + the T24 skin rules; then rule 7; then dedup
    seen = set()
    for p in pools.get("skins", []):
        probs = A.check_skin(p["text"], p["register"], p["slots"], held_out=p["held_out"]) + skin_rule_problems(p["text"])
        if not probs and norm(p["text"]) in seen:
            probs = ["duplicate text"]
        if probs:
            drop("skins", p, "; ".join(probs))
            continue
        seen.add(norm(p["text"]))
        kept["skins"].append(dict(p, pool="skins"))

    # ---- Mode F documents (G0 3.2): lint_freeform (customer verbatim, no number, date, id or negation outside it), rules
    seen = set()
    for p in pools.get("freeform", []):
        probs = A.check_freeform(p["text"], p["customer"]) + freeform_rule_problems(p["text"], p["customer"])
        if not probs and norm(p["text"]) in seen:
            probs = ["duplicate text"]
        if probs:
            drop("freeform", p, "; ".join(probs))
            continue
        seen.add(norm(p["text"]))
        kept["freeform"].append(dict(p, pool="freeform"))

    # ---- clause forms (G0 3.1): check_form (shape, slots, digits, label words, unit test) + LEX_PROMPT rules; dedup
    seen = set()
    for pool in ("lexicon:window", "lexicon:comparator", "lexicon:other"):
        for p in pools.get(pool, []):
            probs = A.check_form(p["text"], p["sem"]) + form_rule_problems(p["text"])
            if not probs and norm(p["text"]) in seen:
                probs = ["duplicate form text"]
            if probs:
                drop(pool, p, "; ".join(probs))
                continue
            seen.add(norm(p["text"]))
            kept["forms"].append(dict(p, pool=pool))

    # ---- question wordings (G0 3.3): check_wording (R16 counts, G-SL lint_template) + WORDING_PROMPT rules; dedup
    seen = set()
    for p in pools.get("wordings", []):
        probs = A.check_wording(p["text"], p["qform"]) + wording_rule_problems(p["text"])
        if not probs and norm(p["text"]) in seen:
            probs = ["duplicate wording"]
        if probs:
            drop("wordings", p, "; ".join(probs))
            continue
        seen.add(norm(p["text"]))
        kept["wordings"].append(dict(p, pool="wordings"))

    # ---- G-SL lint_values on the sample values the registry renders (program-supplied; a check of the generators)
    value_problems = {}
    for kind in ("name", "id", "category", "cents", "date", "count"):
        s = S.sample_slots(kind)[0]
        value_problems[kind] = [v.rule + ": " + v.detail for v in gsl.lint_values({"v": s})]

    # ---- registry: admit-by-unit-test (ambiguity over the whole registry)
    reg, by_fid, forms, wordings = admit_filter(kept["forms"], kept["wordings"], drop)
    kept["forms"], kept["wordings"] = forms, wordings

    # ---- G-LEX read tasks: 2 independent reads per form, 3 for window kind (precedence and window rules)
    fids = sorted(reg.forms)
    plan = {1: fids, 2: fids, 3: [f for f in fids if reg.forms[f].kind in lexicon.STRICT_KINDS]}
    batches = []
    for r, fl in plan.items():
        items = reg.lexicon_items(fl, seed=f"t24-glex-{VERSION}-read{r}")
        b = chunker.make_batch("extract_lex", FAMILY, items, seed=f"t24-glex-{VERSION}-read{r}", prompt=GLEX_PROMPT)
        batches.append((f"glex-read{r}", b))

    # ---- G3-H read tasks: one read per surviving Mode F document, the plugin's own field schema
    fields = P.T24Plugin().extract_fields(None)
    g3_items = [(p["iid"], g3h.extraction_item(p["text"], fields)) for p in kept["freeform"]]
    b3 = chunker.make_batch("extract_g3h", FAMILY, g3_items, seed=f"t24-g3h-{VERSION}-free", prompt=G3H_PROMPT)
    batches.append(("g3h-free", b3))

    # ---- pieces, log, tasks
    by_pool = collections.Counter()
    reasons = collections.Counter()
    for row in log:
        by_pool[row["pool"]] += 1
        reasons[re.sub(r"\d+", "N", row["reason"].split(";")[0].split(":")[0])[:80]] += 1
    for k, v in stats.items():
        v["dropped"] = by_pool.get(k, 0)
    survivors = {"packs": len(kept["packs"]), "skins": len(kept["skins"]), "freeform": len(kept["freeform"]),
                 "lexicon_forms": len(kept["forms"]), "wordings": len(kept["wordings"])}

    tasks = []
    files: dict = {}
    for label, b in batches:
        files.update(b.files())
        for c in b.chunks:
            tid = c["task_id"]
            reads, writes = b.allowed(str(OUT), tid)
            tasks.append({"task_id": tid, "kind": b.kind, "read": label, "n_items": len(c["items"]),
                          "task_file": str(OUT / b.chunk_path(tid)), "answer_file": str(OUT / b.answer_path(tid)),
                          "prompt_file": str(OUT / b.prompt_path()), "allowed_read": sorted(reads),
                          "allowed_write": sorted(writes), "batch_id": b.batch_id, "seed": b.seed,
                          "prompt_sha": b.prompt_sha})
    tasks_by_kind = collections.Counter(t["kind"] for t in tasks)
    per_read = collections.Counter(t["read"] for t in tasks)
    per_read_items = collections.Counter()
    for label, b in batches:
        per_read_items[label] = sum(len(c["items"]) for c in b.chunks)

    counts = {
        "pieces_authored": sum(len(v) for v in pools.values()),
        "pieces_by_pool_in": {k: v["in"] for k, v in stats.items()},
        "lint_dropped_total": len(log),
        "lint_dropped_by_pool": dict(by_pool),
        "survivors": survivors,
        "forms_needing_admission": {"clause_forms": len([f for f in reg.forms.values() if f.kind != "question"]),
                                    "question_wordings": len([f for f in reg.forms.values() if f.kind == "question"]),
                                    "window_3_of_3": len([f for f in reg.forms.values() if f.kind in lexicon.STRICT_KINDS]),
                                    "two_of_two": len([f for f in reg.forms.values()
                                                       if f.kind not in lexicon.STRICT_KINDS])},
        "glex_items_per_read": {label: per_read_items[label] for label, _ in batches if label.startswith("glex")},
        "g3h_items": per_read_items["g3h-free"],
        "survivors_detail": {
            "skins_by_register": dict(collections.Counter(p["register"] for p in kept["skins"])),
            "skins_held_out": sum(1 for p in kept["skins"] if p["held_out"]),
            "freeform_by_held_out": dict(collections.Counter(bool(p["held_out"]) for p in kept["freeform"])),
            "wordings_by_qform": dict(sorted(collections.Counter(
                f"{p['qform']}|{'held' if p['held_out'] else 'train'}" for p in kept["wordings"]).items())),
            "forms_by_sem": dict(sorted(collections.Counter(p["sem"] for p in kept["forms"]).items())),
        },
        "tasks": {"total": len(tasks), "by_kind": dict(tasks_by_kind), "by_read": dict(per_read)},
        "registry_status": dict(collections.Counter(reg.status(f) for f in reg.forms)),
        "value_lint_problems": {k: v for k, v in value_problems.items() if v},
        "g0_sha256": P.G0_SHA256_AUTHORED,
        "g0_ambiguity_pass": P.T24Plugin.G0_AMBIGUITY_PASS["task_id"],
        "question_choices": "authoring.Q_MEANING (fixture QUESTION_MEANINGS not used: see QUESTION_CHOICES)",
    }
    manifest = {"family": FAMILY, "version": VERSION, "counts": counts, "tasks": tasks}
    pieces = {"survivors": kept}
    registry = reg.to_json()

    print(json.dumps(counts, indent=1, ensure_ascii=False))
    if dry:
        for row in log:
            print(f"DROP {row['pool']:18s} {row['task_id']:34s} {row['reason'][:220]}")
        return 0

    files["TASKS.json"] = json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"
    files["LINT_LOG.json"] = json.dumps({"dropped": log, "reasons": dict(reasons)}, ensure_ascii=False, indent=1) + "\n"
    files["pieces.json"] = json.dumps(pieces, ensure_ascii=False, indent=1) + "\n"
    files["registry_pre_glex.json"] = json.dumps(registry, ensure_ascii=False, indent=1) + "\n"
    files["answers/README.txt"] = ("Extraction answer files: one <task_id>.json per task in TASKS.json (the chunk files "
                                   "name the task_id). Written only by the task agents; a read is admitted only from "
                                   "these answers (lexicon.record_extraction / G3-H compare).\n")
    paths.write_files(OUT, files)
    print(f"wrote {len(files)} files under {OUT}; {len(tasks)} tasks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
