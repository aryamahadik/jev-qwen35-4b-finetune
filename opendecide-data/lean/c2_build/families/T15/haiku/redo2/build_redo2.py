"""families/T15/haiku/redo2/build_redo2.py: builds the T15 REDO-2 Haiku task files for the four design-level pool
blockers of freeze-v1 (G0_SPEC.md v1.2: section 3 items 2-3 and section 6 rulings R1-R4).

Writes ONLY under haiku/redo2/ (paths.write_files, A38 guard). Edits no pinned lean/*.py, no c_build file, no other T15
file, never pools/ (freeze-v1 MANIFEST untouched) and never an answer. Haiku answers only flag: nothing here sets or
reads a label or a gold.

  plan    print the summary (writes nothing)
  check   rebuild every file in memory and compare it byte for byte with haiku/redo2/ on disk (writes nothing)
  write   write the files (refuses when REDO2_INDEX.json already exists)

Run from lean/:  ../.venv/bin/python c2_build/families/T15/haiku/redo2/build_redo2.py plan|check|write

Stage redo2-a (this file):
  1. v1 loader rejects: the 23 wording / comparator answers haiku_author turned down as "duplicate or fixture copy" are
     re-checked one by one (every other loader check must pass). A cross-chunk duplicate is RE-AUTHORED. A text equal to
     a fixtures.py text (R2) RE-ENTERS when it passes its unit test in the full v1 registry and breaks no v1 form's unit
     test; otherwise it is re-authored. -> plan/v1_load_rejects.json
  2. author_wording: the re-authored v1 items (same item ids, plan, style hint) + R3 replacements for the 8 v1 forms
     that G-LEX rejected or whose unit test failed (v1 verdicts are final: NEW texts under NEW item ids, same form,
     held-out flag and style hint). Each item lists the texts already written for its form and split (R1 dedup).
  3. author_lexicon: R2 plain everyday comparator phrasings (5 per meaning, new item ids), each item listing the texts
     already in use for its meaning; plus any fixture-equal comparator that failed its unit test (none expected).
  4. extract_lex: two independent G-LEX reads (r2a-A, r2a-B) of the forms that re-enter in step 1, with the v1 prompt
     and closed meaning lists (fixtures.py) and R4 rendering (each slot a distinct value of its role).
  5. R4 role check (program, report only) of every v1 question form -> plan/role_check_v1.json
Stage redo2-b (after the redo2-a authoring answers exist; NOT built here): load the answers with the haiku_author checks
(R2: "duplicate or fixture copy" counts only for a duplicate of a pool candidate), dedup against every v1 form text
(admitted or not) and every re-entered text, unit-test in the full v1 registry plus the re-entered forms (drop a form
that fails or breaks another), then G-LEX reads r2b-A / r2b-B of the survivors with the same prompt and rendering.
Freeze-v2 (NOT built here): supplement pools/redo2/ = freeze-v1 + the redo-v1 skin / attack answers + redo2 forms
admitted 2/2, counted against glex_admit.G0_TARGETS (never lowered). pools/*.json and pools/MANIFEST.json stay as they
are.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
T15 = HERE.parents[1]
C2_BUILD = T15.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, paths  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.lexicon import LexiconRegistry, question_sem  # noqa: E402
from families.T15 import fixtures as FX  # noqa: E402
from families.T15 import haiku_author as HA  # noqa: E402
from families.T15 import plugin as P  # noqa: E402
import negcount  # noqa: E402  (c_src/common, put on sys.path by c2_kit.paths)

F = "T15"
R2 = HERE
SEED = "t15-redo2-v1"
POOLS = T15 / "pools"
EXTRACT_V1 = T15 / "haiku" / "extract"
DUP = "duplicate or fixture copy"
CMP_FIXTURES = frozenset(t for _, t, _ in FX.COMPARATORS)
N_CANON = 5                       # R2: plain everyday phrasings asked per comparator meaning

# ------------------------------------------------------------------------------------------------ R3 briefs
# G0 v1.2 S7 / S12 and section 3 item 2: the surface each complement form needs. Other forms keep the v1 rule.
R3_RULE = {
    "yn_ineligible": "Use NO negation word: use the word 'ineligible' (for example 'is {SUBJECT} ineligible for "
                     "{PROG}'). Never 'disqualified', and never 'not', 'fail', 'lack', 'deny', 'refuse' or 'rule out'.",
    "yn_fails": "Use exactly ONE negation: the words 'fail to qualify' or 'fails to qualify'. Never 'fail to be "
                "eligible', and no other negation word.",
    "yn_may_not": "Use exactly ONE negation, with {ASKED} as the subject of the verb: '{ASKED} may not claim {SUBJECT}' "
                  "or '{ASKED} does not get to claim {SUBJECT}'. Never 'is not the person who', never 'fail', 'win', "
                  "'barred', 'a different person' or 'unclaimed', and no other negation word.",
}
R3_EXAMPLES = {"yn_ineligible": ("Is Mia Lund ineligible for Kestrel Aid?", (0, 0)),
               "yn_fails": ("Does Mia Lund fail to qualify for Kestrel Aid?", (1, 0)),
               "yn_may_not": ("Is it true that Omar Lund may not claim Mia for Kestrel Aid?", (1, 1))}

WORDING_NOTE = (
    "\n\nREDO NOTE (every rule above still holds). Each item also lists questions that already exist for its meaning. "
    "Your question must differ from every listed one. It must also not be a listed question with words only added or "
    "removed after its last placeholder (for example a listed question plus 'under these rules' at the end): a "
    "program cannot tell such a pair apart and drops it.")

CMP_RULE4_V1 = ('4. Makes plain whether a value exactly equal to the bound passes. Never use "up to", "within", '
                '"between", "and", "around", "about", "roughly", "upwards of" or "or so".')
CMP_RULE4_R2 = ('4. Plain everyday wording: the kind of phrase a short printed rule card most often uses, whose ordinary '
                'meaning settles whether a value exactly equal to the bound passes. Never use "strictly", "up to", '
                '"within", "between", "and", "around", "about", "roughly", "upwards of" or "or so".')
CMP_END_V1 = "Every phrase must differ from every other phrase you write, and from the example in the item."
CMP_END_R2 = ("Every phrase must differ from every other phrase you write, and from every phrase the item lists as "
              "already in use.")
CANON_BRIEF = ("Write the plainest everyday phrase with this meaning, in your own words: at most three ordinary words "
               "besides the placeholder.")


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _dump(o) -> str:
    return json.dumps(o, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


def _norm_w(text: str) -> str:
    return " ".join(text.split())


def _norm_c(text: str) -> str:
    return " ".join(text.split()).rstrip(".")


def _check_g0() -> str:
    g0 = (T15 / "G0_SPEC.md").read_bytes()
    sha = _sha(g0)
    if sha != P.T15Plugin.G0_SHA256:
        raise SystemExit("G0_SPEC.md does not match the plugin pin")
    txt = " ".join(g0.decode("utf-8").split())
    for need in ("FROZEN v1.2", "R1 ", "R2 ", "R3 ", "R4 ", '"ineligible", never "disqualified"'):
        if need not in txt:
            raise SystemExit(f"G0_SPEC.md v1.2 text missing: {need!r}")
    for q, (example, want) in R3_EXAMPLES.items():
        c = negcount.count(example)
        if (c.k_all, c.k_syn) != want or want != HA.NEG_EXACT[q]:
            raise SystemExit(f"R3 rule for {q}: negcount {(c.k_all, c.k_syn)} != {want}")
    return sha


def v1_registry() -> LexiconRegistry:
    return LexiconRegistry.from_json(json.loads((POOLS / "lexicon.json").read_text(encoding="utf-8")))


def unit_in_v1(sem: str, text: str, slots: dict) -> dict:
    """Add one form to the full v1 registry (247 forms, admitted or not): its own unit test and every v1 form's."""
    reg = v1_registry()
    before = {fid: f.unit_ok for fid, f in reg.forms.items()}
    try:
        f = reg.add(text, sem, slots=dict(slots), source="haiku", family=F, haiku_task_id="redo2-check",
                    haiku_prompt_sha="redo2-check")
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "form_id": None, "problems": [f"registry add: {str(e)[:160]}"], "breaks": []}
    reg.unit_test_all()
    breaks = sorted(fid for fid, ok in before.items() if ok and not reg.forms[fid].unit_ok)
    ok = bool(reg.forms[f.form_id].unit_ok) and not breaks
    return {"ok": ok, "form_id": f.form_id, "problems": list(reg.forms[f.form_id].unit_problems[:2]), "breaks": breaks}


# ------------------------------------------------------------------------------------------------ step 1
def v1_load_rejects() -> tuple:
    """({iid: record}, {pool: {iid: v1 text}} of every loaded v1 candidate) for the wording and comparator pools."""
    out, loaded = {}, {}
    for name, check, norm, fixtures in (("wordings", HA.check_wording, _norm_w, frozenset(HA.QSTRINGS)),
                                        ("comparators", HA.check_comparator, _norm_c, CMP_FIXTURES)):
        b, plan, ans, probs = HA.load_answers_for(name)
        if probs:
            raise SystemExit(f"v1 {name} answers do not load cleanly: {probs[:3]}")
        seen, first, kept = set(), {}, {}
        for iid, a in sorted(ans.items()):                     # the loader's own order (haiku_author._loop)
            text = a.get("text") if isinstance(a, dict) else None
            tid = HA._task_of(b, iid)
            obj, v = check(iid, text, plan[iid], tid, b.prompt_sha, seen)
            if not v:
                first.setdefault(norm(text).lower(), iid)
                kept[iid] = norm(text)
                continue
            _, alone = check(iid, text, plan[iid], tid, b.prompt_sha, set())
            other = [p for p in alone if p != DUP]
            nt = norm(text) if isinstance(text, str) else None
            fixture = nt in fixtures
            dup_of = first.get(nt.lower()) if nt else None
            if v != [DUP] or other or not (fixture or dup_of):
                raise SystemExit(f"unplanned v1 reject {iid}: {v} / {other}")
            meta = plan[iid]
            sem = question_sem(F, meta["qform"]) if name == "wordings" else meta["sem"]
            rec = {"pool": name, "v1_task": tid, "v1_qid": {v_: k for k, v_ in b.key.items()}[iid], "text": nt,
                   "sem": sem, "slots": dict(meta["slots"]), "held_out": bool(meta.get("held_out", False)),
                   "why_v1": ("fixture text" if fixture else f"duplicate of {dup_of} (another chunk)"),
                   "other_loader_problems": other}
            if fixture and not dup_of:
                u = unit_in_v1(sem, nt, meta["slots"])
                rec["unit_test_in_full_v1_registry"] = u
                rec["decision"] = "re-enter (R2): G-LEX r2a reads" if u["ok"] else "re-author (fixture text fails " \
                                                                                    "its unit test in the v1 registry)"
                rec["form_id"] = u["form_id"]
            else:
                rec["decision"] = "re-author (cross-chunk duplicate)"
            out[iid] = rec
        loaded[name] = kept
    return out, loaded


# ------------------------------------------------------------------------------------------------ steps 2-3
def _taken_rule(texts: list) -> str:
    return ("Already written for this meaning (write none of these again, and none of them with words only added or "
            "removed at the end): " + " | ".join(texts))


def wording_items(rejects: dict, loaded: dict) -> tuple:
    v1_items = dict(HA._wording_items()[0])
    v1_plan = HA.build_batches()["wordings"][1]
    lex = json.loads((POOLS / "lexicon.json").read_text(encoding="utf-8"))
    by_text = {t: iid for iid, t in loaded["wordings"].items()}
    qstrings = frozenset(HA.QSTRINGS)

    def taken(q: str, held: bool) -> list:
        ts = {t for iid, t in loaded["wordings"].items()
              if v1_plan[iid]["qform"] == q and v1_plan[iid]["held_out"] == held}
        ts |= {r["text"] for r in rejects.values() if r["pool"] == "wordings" and r["sem"] == question_sem(F, q)
               and r["held_out"] == held}
        return sorted(t for t in ts if t not in qstrings)        # fixture texts may not appear in an authoring item

    def rules(q: str, iid_src: str, held: bool) -> list:
        neg, style = v1_items[iid_src]["rules"]
        if not style.startswith("Style hint:"):
            raise SystemExit(f"v1 item {iid_src}: unexpected rules {v1_items[iid_src]['rules']}")
        return [R3_RULE.get(q, neg), style, _taken_rule(taken(q, held))]

    items, plan = [], {}
    for iid, r in sorted(rejects.items()):
        if r["pool"] != "wordings" or not r["decision"].startswith("re-author"):
            continue
        q, held = v1_plan[iid]["qform"], v1_plan[iid]["held_out"]
        it = dict(v1_items[iid])
        it["rules"] = rules(q, iid, held)
        items.append((iid, it))
        plan[iid] = dict(v1_plan[iid], redo2="retry", supersedes_v1_answer={"task": r["v1_task"], "qid": r["v1_qid"]},
                         v1_problem=r["why_v1"], r3_rule=q in R3_RULE)
    # R3 replacements: one NEW item per v1 form that G-LEX rejected or whose unit test failed
    nxt = {q: sum(HA.WORDING_PLAN[q]) for q in HA.WORDING_PLAN}
    bad = [f for f in lex["forms"] if f["kind"] == "question" and f["status"] != "admitted"]
    for f in sorted(bad, key=lambda f: f["form_id"]):
        q = f["sem_id"].split(".", 2)[2]
        src = by_text.get(f["text"])
        if src is None or v1_plan[src]["qform"] != q or v1_plan[src]["held_out"] != f["held_out"]:
            raise SystemExit(f"cannot place v1 form {f['form_id']}")
        iid = f"t15a.wording.{q}.{nxt[q]:03d}"
        nxt[q] += 1
        if iid in v1_items:
            raise SystemExit(f"new item id {iid} exists in v1")
        it = dict(v1_items[src])
        it["rules"] = rules(q, src, f["held_out"])
        items.append((iid, it))
        plan[iid] = {"role": "wording", "qform": q, "held_out": f["held_out"], "slots": dict(v1_plan[src]["slots"]),
                     "redo2": "replacement", "replaces_v1_form": f["form_id"], "v1_item": src,
                     "v1_status": f["status"], "v1_extractions": f["extractions"], "r3_rule": q in R3_RULE}
    return items, plan


def comparator_items(rejects: dict, loaded: dict) -> tuple:
    v1_items = dict(HA._cmp_items()[0])
    v1_plan = HA.build_batches()["comparators"][1]
    in_use = {}
    for iid, t in loaded["comparators"].items():
        in_use.setdefault(v1_plan[iid]["sem"], set()).add(t)
    for r in rejects.values():
        if r["pool"] == "comparators":
            in_use.setdefault(r["sem"], set()).add(r["text"])
    items, plan = [], {}
    for iid, r in sorted(rejects.items()):                     # fixture-equal comparators failing a unit test
        if r["pool"] == "comparators" and r["decision"].startswith("re-author"):
            it = dict(v1_items[iid])
            it["rules"] = list(it["rules"]) + [_taken_rule(sorted(in_use[r["sem"]]))]
            items.append((iid, it))
            plan[iid] = dict(v1_plan[iid], redo2="retry", v1_problem=r["why_v1"])
    for sem, (ph, meaning, _example) in HA.CMP_MEANING.items():
        for k in range(N_CANON):
            iid = f"t15a.cmp.{sem}.{HA.N_CMP + k:03d}"
            if iid in v1_items:
                raise SystemExit(f"new item id {iid} exists in v1")
            items.append((iid, {"brief": CANON_BRIEF, "meaning": meaning,
                                "slots": {ph: "an amount of money" if ph == "X" else "a count with its unit"},
                                "rules": ["Place {%s} wherever it reads best." % ph,
                                          _taken_rule(sorted(in_use[sem]))]}))
            plan[iid] = {"role": "lexicon", "kind": "comparator", "sem": sem,
                         "slots": {ph: "cents" if ph == "X" else "count"}, "redo2": "canonical (R2)"}
    return items, plan


def cmp_prompt_r2() -> str:
    p = HA.CMP_PROMPT
    if CMP_RULE4_V1 not in p or CMP_END_V1 not in p:
        raise SystemExit("haiku_author.CMP_PROMPT changed: the R2 edit no longer applies")
    return p.replace(CMP_RULE4_V1, CMP_RULE4_R2).replace(CMP_END_V1, CMP_END_R2)


# ------------------------------------------------------------------------------------------------ step 4 (R4)
def role_values() -> dict:
    """R4: one distinct value per role, taken from the frozen v1 pools (training packs and names)."""
    names = json.loads((POOLS / "names.json").read_text(encoding="utf-8"))["pools"]
    packs = json.loads((POOLS / "packs.json").read_text(encoding="utf-8"))["packs"]
    gate = next(p["programme"] for p in packs if p["kind"] == "household" and not p["held_out"])
    credit = next(p["programme"] for p in packs if p["kind"] == "credit" and not p["held_out"])
    vals = {"applicant": f"{names['female'][0]} {names['last'][0]}", "asked": f"{names['male'][0]} {names['last'][1]}",
            "child": names["children"][0], "gate_programme": gate, "credit_programme": credit}
    if len(set(vals.values())) != len(vals):
        raise SystemExit("R4 role values are not distinct")
    for v in vals.values():
        S.name_slot(v)
    return vals


def render_r4(reg: LexiconRegistry, fid: str, rv: dict) -> str:
    f = reg.forms[fid]
    slots = dict(f.slots)
    claim = "ASKED" in slots or f.sem_id == question_sem(F, "ch_claimant")
    v = {}
    for name, kind in slots.items():
        if kind == "cents":
            v[name] = S.cents_slot(250000)
        elif kind == "count":
            v[name] = S.count_slot(6, ("month", "months"))
        elif name == "ASKED":
            v[name] = S.name_slot(rv["asked"])
        elif name == "SUBJECT":
            v[name] = S.name_slot(rv["child"] if claim else rv["applicant"])
        elif name == "PROG":
            v[name] = S.name_slot(rv["credit_programme"] if claim else rv["gate_programme"])
        else:
            raise SystemExit(f"no R4 value for slot {name} of {fid}")
    return reg.render(fid, v)


def read_registry(forms: list) -> LexiconRegistry:
    reg = LexiconRegistry(F)
    for sem, meaning in FX.CMP_MEANINGS:
        reg.declare(sem, "comparator", meaning)
    for qf, meaning in FX.QUESTION_MEANINGS.items():
        reg.declare(question_sem(F, qf), "question", meaning)
    for r in forms:
        reg.add(r["text"], r["sem"], slots=r["slots"], source="haiku", family=F, haiku_task_id=r["v1_task"],
                haiku_prompt_sha=r["v1_prompt_sha"], held_out=r["held_out"])
    return reg


def read_items(reg: LexiconRegistry, rv: dict, seed: str) -> list:
    out = []
    for fid in sorted(reg.forms):
        f = reg.forms[fid]
        mean = sorted((s.meaning for s in reg.sems.values() if s.kind == f.kind),
                      key=lambda m: _sha(f"{seed}|{fid}|{m}".encode()))
        out.append((fid, {"text": render_r4(reg, fid, rv), "choices": mean}))
    return out


# ------------------------------------------------------------------------------------------------ step 5 (R4)
PROG_POS = {"for", "to", "from", "entering", "concerning", "regarding"}


def role_check_v1() -> dict:
    """Each placeholder of every v1 question form in its role position (program check, report only). Gate forms: PROG
    is the object of for / to / from / entering / concerning / regarding, SUBJECT is not (unless 'applying' follows).
    Claim forms: SUBJECT is the object of claim / claiming / 'claim on', PROG follows 'for', and ASKED stands before the
    first claim word or after 'from' ('a different person from ASKED')."""
    lex = json.loads((POOLS / "lexicon.json").read_text(encoding="utf-8"))
    rows, flags = [], []
    for f in lex["forms"]:
        if f["kind"] != "question":
            continue
        toks = re.findall(r"\{[A-Z_]+\}|[A-Za-z']+", f["text"])
        pos = {w[1:-1]: i for i, w in enumerate(toks) if w.startswith("{")}

        def prev(n, toks=toks, pos=pos):
            return toks[pos[n] - 1].lower() if pos[n] > 0 else "^"

        def nxt(n, toks=toks, pos=pos):
            return toks[pos[n] + 1].lower() if pos[n] + 1 < len(toks) else "$"

        claim = "ASKED" in f["slots"] or f["sem_id"] == question_sem(F, "ch_claimant")
        probs = []
        if prev("PROG") not in PROG_POS | {"^"}:
            probs.append(f"PROG after {prev('PROG')!r}")
        if claim:
            if prev("SUBJECT") not in ("claim", "claiming", "on"):
                probs.append(f"SUBJECT after {prev('SUBJECT')!r}")
            if "ASKED" in pos:
                ci = min((i for i, w in enumerate(toks) if w.lower().startswith("claim")), default=len(toks))
                if not (pos["ASKED"] < ci or prev("ASKED") == "from"):
                    probs.append("ASKED after the claim word")
        elif prev("SUBJECT") in PROG_POS and nxt("SUBJECT") != "applying":
            probs.append(f"SUBJECT after {prev('SUBJECT')!r}")
        row = {"form_id": f["form_id"], "status": f["status"], "held_out": f["held_out"], "text": f["text"],
               "track": "claim" if claim else "gate", "flags": probs}
        rows.append(row)
        if probs:
            flags.append(row)
    adm = [r for r in rows if r["status"] == "admitted"]
    return {"rule": role_check_v1.__doc__.split("\n")[0].strip() + " (see build_redo2.role_check_v1)",
            "n_question_forms": len(rows), "n_admitted": len(adm),
            "admitted_flagged": sum(1 for r in adm if r["flags"]),
            "flagged": flags, "forms": rows}


# ------------------------------------------------------------------------------------------------ task files
ANSWER_SHAPE = {"author_wording": '{"qid": "<QID>", "text": "<the question>"}',
                "author_lexicon": '{"qid": "<QID>", "text": "<the phrase>"}',
                "extract_lex": '{"qid": "<QID>", "meaning": "<one choice of that item, copied exactly, or NONE>"}'}
KEYS = {"author_wording": '"qid" and "text"', "author_lexicon": '"qid" and "text"',
        "extract_lex": '"qid" and "meaning"'}


def task_text(b, c, ans: str, title: str) -> str:
    n = len(c["items"])
    shape = ["["] + [f"  {ANSWER_SHAPE[b.kind].replace('<QID>', it['qid'])}" + ("," if i < n - 1 else "")
                     for i, it in enumerate(c["items"])] + ["]"]
    return "\n".join([
        f"# Haiku REDO-2 {title} task {c['task_id']} (family {F}, kind {b.kind}): {n} item(s)", "",
        "THIS ONE FILE IS YOUR WHOLE TASK. Read all of it, write the answer file with the Write tool, then stop.",
        "Do not open, search or list any other file or folder. Run no other tool. Create no other file. Do not put the "
        "answer in chat.", "", "Write your answer to exactly this path (nothing else, no other file):", "",
        f"    {ans}", "", "## Answer contract (exact)", "",
        "The answer file holds ONE JSON list and nothing else: no text before or after it, no comment, no code fence, "
        "no wrapper object.",
        f"The list has exactly {n} object(s), one per item below, every qid exactly once (any order). Each object has "
        f"exactly two keys, {KEYS[b.kind]}. This is the literal shape of the file (replace each <...>):", "", *shape, "",
        "\"qid\" is copied character for character from its item. The other value is a non-empty JSON string (escape a "
        "double quote as \\\"). No other keys, no null, no skipped qid, no qid used twice, no qid that is not listed "
        "in the items below.", "", "## Instructions (complete)", "", b.prompt, "",
        f"## Items ({n}; one JSON object per line)", "", "```json",
        "[\n" + ",\n".join(json.dumps(it, ensure_ascii=False) for it in c["items"]) + "\n]", "```", ""])


def build() -> tuple:
    g0_sha = _check_g0()
    rejects, loaded = v1_load_rejects()

    w_items, w_plan = wording_items(rejects, loaded)
    bw = chunker.make_batch("author_wording", F, w_items, seed=f"{SEED}|wordings", prompt=HA.WORDING_PROMPT +
                            WORDING_NOTE, max_items=45, forbid_strings=HA.QSTRINGS)
    c_items, c_plan = comparator_items(rejects, loaded)
    bc = chunker.make_batch("author_lexicon", F, c_items, seed=f"{SEED}|comparators", prompt=cmp_prompt_r2(),
                            max_items=48, forbid_strings=HA.QSTRINGS)

    # G-LEX r2a reads of the re-entering forms (R1, R4)
    v1_tasks = json.loads((EXTRACT_V1 / "TASKS.json").read_text(encoding="utf-8"))
    v1_psha = v1_tasks["tasks"][0]["prompt_sha"]
    if {t["prompt_sha"] for t in v1_tasks["tasks"]} != {v1_psha}:
        raise SystemExit("v1 reads used more than one prompt")
    read_prompt = (EXTRACT_V1 / "prompts" / f"{v1_psha[:16]}.txt").read_text(encoding="utf-8")
    if _sha(read_prompt.encode("utf-8")) != v1_psha:
        raise SystemExit("v1 G-LEX prompt file does not match its sha")
    author_psha = {"wordings": HA.build_batches()["wordings"][0].prompt_sha,
                   "comparators": HA.build_batches()["comparators"][0].prompt_sha}
    reenter = [dict(r, iid=i, v1_prompt_sha=author_psha[r["pool"]]) for i, r in sorted(rejects.items())
               if r["decision"].startswith("re-enter")]
    rreg = read_registry(reenter)
    for r in reenter:
        if r["form_id"] not in rreg.forms:
            raise SystemExit(f"form id drift for {r['iid']}")
    rv = role_values()
    reads = []
    for name in ("r2a-A", "r2a-B"):
        items = read_items(rreg, rv, seed=f"{SEED}|glex-{name}")
        reads.append((name, chunker.make_batch("extract_lex", F, items, seed=f"{SEED}|glex-{name}",
                                               prompt=read_prompt)))
    if reads[0][1].batch_id == reads[1][1].batch_id:
        raise SystemExit("the two reads share a batch id")

    files, tasks = {}, []
    for kind, name, b, title, plan in (("author_wording", "wordings", bw, "authoring", w_plan),
                                       ("author_lexicon", "comparators", bc, "authoring", c_plan),
                                       ("extract_lex", reads[0][0], reads[0][1], "G-LEX extraction (read r2a-A)", None),
                                       ("extract_lex", reads[1][0], reads[1][1], "G-LEX extraction (read r2a-B)", None)):
        files.update(b.files())
        if plan is not None:
            files[f"plan/{b.batch_id}.json"] = _dump({"batch_id": b.batch_id, "name": name, "kind": kind,
                                                      "plan": plan})
        for c in b.chunks:
            tid = c["task_id"]
            ans = str(R2 / b.answer_path(tid))
            tf = f"tasks/{tid}.md"
            files[tf] = task_text(b, c, ans, title)
            tasks.append({"task_file": str(R2 / tf), "answer_file": ans, "kind": kind, "name": name,
                          "batch_id": b.batch_id, "task_id": tid, "n_items": len(c["items"]),
                          "prompt_sha": b.prompt_sha, "stage": "redo2-a",
                          "audit_allowed_read": [str(R2 / tf)], "audit_allowed_write": [ans]})

    role = role_check_v1()
    if role["admitted_flagged"]:
        raise SystemExit(f"R4 role check flags {role['admitted_flagged']} admitted v1 form(s): decide before reads")
    files["plan/v1_load_rejects.json"] = _dump(rejects)
    files["plan/role_check_v1.json"] = _dump(role)
    files["plan/glex_reads_r2a.json"] = _dump({
        "rule": "G-LEX 2/2 (G0 v1.2 R1): a form is admitted only when both independent reads pick its declared sense; "
                "NONE, an unlisted text, a missing answer or another sense rejects it for good (no re-vote).",
        "prompt": "the v1 G-LEX prompt, byte for byte", "prompt_sha256": v1_psha,
        "meanings": "fixtures.CMP_MEANINGS and fixtures.QUESTION_MEANINGS (the v1 closed lists, unchanged)",
        "meaning_to_sem": {m: s for s, m in FX.CMP_MEANINGS} | {m: question_sem(F, q)
                                                                 for q, m in FX.QUESTION_MEANINGS.items()},
        "rendering_R4": {"values": rv, "cents": "$2,500.00 (250000 cents)", "count": "6 months",
                         "gate track": "SUBJECT = applicant, PROG = gate_programme",
                         "claim track": "ASKED = asked, SUBJECT = child, PROG = credit_programme"},
        "extractor_ids": {n: f"read-{n}" for n, _ in reads},
        "reads": {n: b.batch_id for n, b in reads},
        "forms": {r["form_id"]: {"item": r["iid"], "pool": r["pool"], "sem_id": r["sem"], "text": r["text"],
                                 "held_out": r["held_out"], "haiku_task_id": r["v1_task"],
                                 "haiku_prompt_sha": r["v1_prompt_sha"]} for r in reenter}})

    dec = Counter(r["decision"].split(" (")[0] for r in rejects.values())
    w_by = Counter(p["qform"] + ("|held" if p["held_out"] else "") for p in w_plan.values())
    summary = {
        "family": F, "version": "redo2-a", "seed": SEED, "g0_sha256": g0_sha, "g0_version": "v1.2 (R1-R4)",
        "n_tasks": len(tasks), "by_kind": dict(Counter(t["kind"] for t in tasks)),
        "items": {"author_wording": len(w_items), "author_lexicon": len(c_items),
                  "extract_lex_per_read": len(rreg.forms)},
        "v1_load_rejects": {"n": len(rejects), "decisions": dict(dec)},
        "author_wording_by_form": dict(sorted(w_by.items())),
        "author_wording_kinds": dict(Counter(p["redo2"] for p in w_plan.values())),
        "author_lexicon_kinds": dict(Counter(p["redo2"] for p in c_plan.values())),
        "role_check_v1": {k: role[k] for k in ("n_question_forms", "n_admitted", "admitted_flagged")}
                         | {"flagged_not_admitted": [r["text"] for r in role["flagged"]]},
        "rulings": {
            "R1": "G-LEX 2/2 is per form: forms authored or re-entered after freeze-v1 get their own two independent "
                  "reads (v1 prompt, v1 meaning lists); v1 reads and verdicts stay final; new forms must pass their "
                  "unit test in the full v1 registry and break none; the merge is a supplement freeze-v2 "
                  "(pools/redo2/), never a rewrite of freeze-v1.",
            "R2": "fixtures.py texts are test stand-ins, never pool items: a Haiku text equal to one is a valid "
                  "candidate under every other check; plain everyday comparator phrasings are asked for.",
            "R3": "briefs name the complement surface: 'ineligible' (never 'disqualified'), 'fail(s) to qualify' "
                  "(never 'fail to be eligible'), 'may not claim' / 'does not get to claim' (never 'is not the person "
                  "who'); v1 rejections stay rejected; replacements are new texts under new item ids.",
            "R4": "redo2 G-LEX items render each slot with a distinct value of its role; the v1 admissions stand, "
                  "backed by the program role check (0 admitted v1 question forms flagged).",
        },
        "notes": [
            "Haiku answers only flag. No label or gold is set or read here; pools/ and every v1 file are untouched.",
            "Each task: one fresh Haiku agent that reads only its task_file and writes only its answer_file; audit "
            "with audit.audit_jsonl(transcript, allowed_read=audit_allowed_read, allowed_write=audit_allowed_write). "
            "A failed audit discards that answer.",
            "r2a-A and r2a-B are independent reads (two different agents); extractor ids read-r2a-A / read-r2a-B "
            "(plan/glex_reads_r2a.json maps each choice text to its sem id).",
            "A retry answer (plan redo2 = 'retry') supersedes the v1 answer of the same item id, which the v1 loader "
            "had turned down; it never overwrites the v1 answer file.",
            "Stage redo2-b and freeze-v2 are described in build_redo2.py's docstring; neither is built here. "
            "glex_admit.py freeze refuses to re-freeze over freeze-v1 by design.",
        ],
        "tasks": tasks,
    }
    files["REDO2_INDEX.json"] = json.dumps(summary, ensure_ascii=False, indent=1) + "\n"
    return files, summary


def main(argv: list) -> int:
    cmd = argv[1] if len(argv) > 1 else "plan"
    files, summary = build()
    if cmd == "plan":
        print(json.dumps({k: v for k, v in summary.items() if k != "tasks"}, indent=1, ensure_ascii=False))
        return 0
    if cmd == "write":
        if (R2 / "REDO2_INDEX.json").exists():
            raise SystemExit("haiku/redo2/REDO2_INDEX.json already exists: refusing to overwrite")
        paths.write_files(R2, files)
        (R2 / "answers").mkdir(exist_ok=True)
        print(json.dumps({k: v for k, v in summary.items() if k != "tasks"}, indent=1, ensure_ascii=False))
        return 0
    if cmd != "check":
        print(__doc__)
        return 2
    diffs = [rel for rel, text in sorted(files.items())
             if not (R2 / rel).is_file() or (R2 / rel).read_text(encoding="utf-8") != text]
    extra = sorted(str(p.relative_to(R2)) for p in R2.rglob("*") if p.is_file()
                   and p.parent.name != "answers" and p.name != "build_redo2.py" and "__pycache__" not in p.parts
                   and str(p.relative_to(R2)) not in files)
    print(json.dumps({"files": len(files), "differ_or_missing": diffs, "extra_on_disk": extra}, indent=1))
    return 0 if not diffs and not extra else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
