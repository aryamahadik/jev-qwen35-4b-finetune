"""A55 (d2, d3): Haiku authoring and G-LEX admission of the DEV-ONLY rule / clause forms (T24, T06, T07) and question wordings (T25).

Ruling A55 (d2): for each rule or clause kind used by the family's dev rows Haiku authors 8 forms and >= 4 must be admitted. A form
carries ONE meaning (sem), so the unit here is the sem (a kind with several sems = several units; the kind is reported). Admission
takes all of: the G-LEX unit test; 2/2 extraction agreement (3/3 for the kinds precedence and window); a form text equal to no pool
entry of the family (training or held out); 0 hits from g13_ohs4_check run through g13_c2.run_checker (counts only; a hit removes the
form). A unit with fewer than 4 admitted forms keeps its training forms in dev (its hits bind). (d3): T25, 8 wordings per question
form, admission G-LEX 2/2, text equal to no T25 pool wording, 0 run_checker hits; >= 4 per form.

Nothing here edits a pool, a plugin or a file the sealed mode reads; everything lives in zed_orch/a55_dev/<FAM>/ :

  plan/   <batch>.json                orchestrator only (internal ids)
  tasks/  <task_id>.md                self-contained Haiku authoring task files (answer path first)    -> HAIKU
  chunks/ prompts/ key/ manifest/     chunker files (key/ is orchestrator only)
  answers/<task_id>.json              written by Haiku
  TASKS.json                          the list of tasks (+ allowed read / write for the file-access audit)
  ADMITTED.json  PROBLEMS.json        after `admit`: lint, pool dedup, unit test, run_checker counts
  extract/{tasks,chunks,prompts,key,manifest,answers}, extract/TASKS.json    after `glex`: the G-LEX reads             -> HAIKU
  FROZEN.json                         after `score`: the admitted forms + the sha256 the A55 addendum logs

  ../.venv/bin/python -B c2_build/zed_orch/a55_devforms.py plan  T24 T06 T07 T25      counts only, writes nothing
  ... write T24 ...        author tasks      ... admit T24 ...   (answers read)      ... glex T24 ...  G-LEX read tasks
  ... score T24 ...        (extract answers read) -> FROZEN.json
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2B = HERE.parent
for _p in (str(C2B), str(HERE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
sys.dont_write_bytecode = True

import a55_common as C  # noqa: E402
import a55_overlay as OV  # noqa: E402
import gen_full_c2 as G  # noqa: E402
import g13_c2 as X  # noqa: E402
from c2_kit import chunker, paths  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit.lexicon import STRICT_KINDS, question_sem  # noqa: E402

VERSION = "a55v1"
HOW_MANY = C.HOW_MANY
MIN_ADMITTED = C.MIN_ADMITTED_PER_UNIT
OPENINGS_PER_UNIT = 6

GLEX_PROMPT = """TASK: name the meaning of each text. Each item gives "text" (one line of a made-up policy, notice, advertisement
small print or reading test, or a question about it) and "choices" (the possible meanings for that kind of text). For each
item, pick the ONE choice whose meaning the text states, read exactly as written.

Rules:
1. Read the whole text. Words such as "not", "do not qualify", "fail to", "instead", "both dates included", "at least",
   "exactly", "more than", "below", "only" and "other than" change the meaning, so take them into account.
2. Copy the chosen choice exactly, character for character, from that item's "choices" list. Never write a meaning that is
   not in the list, and never leave an item unanswered.
3. This task file is the only file you may open. Do not open, list or search any other file or folder.
4. Write your whole answer, and nothing else, as one JSON array to the ANSWER FILE named at the top of this file, with the
   Write tool:
   [{"qid": "<qid of the item>", "meaning": "<the chosen choice, copied exactly>"}, ...]
   One object per item, each qid copied exactly.
"""


def dev_dir(fam: str) -> Path:
    return OV.dev_dir(fam)


@contextlib.contextmanager
def open_kit(fam: str):
    """The family's kit exactly as gen_full_c2 opens it (the loader patch of its latest runner). The registry is the kit's own
    object: forms added to it live only for the duration of the call."""
    with G.loader_patch(fam):
        with G.PL.open_family(fam) as kit:
            yield kit


def norm(t: str) -> str:
    return " ".join(t.casefold().split())


def _leaves(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values():
            yield from _leaves(v)
    elif isinstance(x, (list, tuple)):
        for v in x:
            yield from _leaves(v)


def pool_texts(fam: str, kit=None) -> set:
    """Normalised text of every pool entry of the family: every string leaf of its pool files (training and held out), the
    registry's form texts and the skins' texts."""
    out = set()
    fdir = C2B / "families" / fam
    for rel in C.generator_identity(fam)["pools"]:
        p = fdir / rel
        try:
            txt = p.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        try:
            objs = [json.loads(ln) for ln in txt.splitlines() if ln.strip()] if p.suffix == ".jsonl" else \
                [json.loads(txt)] if p.suffix == ".json" else [txt]
        except ValueError:
            continue
        for o in objs:
            out |= {norm(s) for s in _leaves(o) if len(s.split()) >= 2}
    if kit is not None:
        out |= {norm(f.text) for f in kit.ctx.lexicon.forms.values()}
        out |= {norm(s.text) for s in kit.ctx.skins.values() if getattr(s, "text", None)}
    return out


def openings(texts: list, k: int = OPENINGS_PER_UNIT) -> list:
    """The k most common 3-word openings of the given texts (placeholders kept as written)."""
    c = Counter(" ".join(t.split()[:3]) for t in texts if len(t.split()) >= 3)
    return [o for o, _n in c.most_common(k)]


# ================================================================================================ adapters
class Adapter:
    fam = ""
    unit_kind = "sem"                        # "sem" (rule forms) | "qform" (wordings)
    chunk_kind = "author_lexicon"
    answer_field = "forms"                   # "forms" (a list per item) | "text" (one string per item)
    max_items = 50

    def mod(self, name):
        return importlib.import_module(f"families.{self.fam}.{name}")

    # -- to override
    prompt = ""
    answer_format = ""
    forbid: tuple = ()

    def units(self, reg) -> list:
        raise NotImplementedError

    def items(self, reg, unit_texts: dict) -> tuple:
        raise NotImplementedError

    def lint(self, meta: dict, text: str, seen: set) -> list:
        raise NotImplementedError

    # -- shared
    def sem_of(self, unit: str) -> str:
        return unit if self.unit_kind == "sem" else question_sem(self.fam, unit)

    def slots(self, reg, meta: dict) -> dict:
        sem = self.sem_of(meta["unit"])
        for f in reg.forms.values():
            if f.sem_id == sem and not f.held_out:
                return dict(f.slots)
        raise KeyError(f"{self.fam}: no pool form of {sem} to copy the slot kinds from")

    def required_reads(self, reg, unit: str) -> int:
        return 3 if reg.sems[self.sem_of(unit)].kind in STRICT_KINDS else 2

    def texts_of(self, ans: dict) -> list:
        o = ans.get(self.answer_field)
        if self.answer_field == "text":
            return [o] if isinstance(o, str) else []
        return [x for x in o] if isinstance(o, list) else []


def _lex_units(reg) -> list:
    """Every non-question sem with at least one training form (the decoy sems that have no form are not drawn)."""
    have = {f.sem_id for f in reg.forms.values() if not f.held_out}
    return sorted(s.sem_id for s in reg.sems.values() if s.kind != "question" and s.sem_id in have)


def _train_texts(reg, sem: str) -> list:
    return [f.text for f in reg.forms.values() if f.sem_id == sem and not f.held_out]


def _fit(kind: str, item: dict, rules_extra: str, forbid: tuple) -> dict:
    """Add the 'do not open with' rule when the chunker accepts it (no forbidden string in the text)."""
    it = json.loads(json.dumps(item))
    it["rules"] = list(it.get("rules", [])) + [rules_extra]
    try:
        chunker.check_item(kind, it, forbid_strings=forbid)
        return it
    except chunker.ChunkError:
        return item


class T24A(Adapter):
    fam = "T24"
    unit_kind = "sem"

    @property
    def prompt(self):
        return self.mod("authoring").LEX_PROMPT

    answer_format = "forms"

    @property
    def forbid(self):
        return self.mod("authoring").FORBID

    def units(self, reg):
        return _lex_units(reg)

    def items(self, reg, unit_texts):
        A = self.mod("authoring")
        items, plan = [], {}
        for sem in self.units(reg):
            key = "amt.pos" if sem in ("t24.amt.ge", "t24.amt.gt") else "amt.neg" if sem in ("t24.amt.le", "t24.amt.lt") else sem
            styles = A.LEX_STYLES[key] if key in A.LEX_STYLES else A.LEX_STYLES["t24.win"]
            if key.startswith("amt."):          # one positive + one negative surface for every comparator
                styles = (A.LEX_STYLES["amt.pos"][0], A.LEX_STYLES["amt.neg"][0])
            op = openings(unit_texts[sem])
            for i, style in enumerate(styles[:2]):
                it = A._lex_item(sem, style)
                it["brief"]["how_many"] = HOW_MANY // 2
                it["rules"][0] = f"{HOW_MANY // 2} forms"
                it = _fit(self.chunk_kind, it, "dev-only: never start a form with any of these openings (the program already "
                          "has them): " + "; ".join(f"'{o}'" for o in op), self.forbid) if op else it
                iid = f"t24-{VERSION}-lex-{sem}-{i}"
                items.append((iid, it))
                plan[iid] = {"unit": sem, "kind": reg.sems[sem].kind, "style": i}
        return items, plan

    def lint(self, meta, text, seen):
        A, E = self.mod("authoring"), self.mod("extract_stage")
        probs = A.check_form(text, meta["unit"]) if isinstance(text, str) else ["not a string"]
        if not probs:
            probs = E.form_rule_problems(text)
        return probs


class T07A(Adapter):
    fam = "T07"
    unit_kind = "sem"

    @property
    def prompt(self):
        return self.mod("authoring").LEX_PROMPT

    answer_format = "forms"

    @property
    def forbid(self):
        return self.mod("authoring").FORBID

    def units(self, reg):
        return _lex_units(reg)

    def items(self, reg, unit_texts):
        A, P = self.mod("authoring"), self.mod("plugin")
        items, plan = [], {}
        for sem in self.units(reg):
            dim, _op, kind, meaning = P.SEMS[sem]
            op = openings(unit_texts[sem])
            for s_i, style in enumerate(A.LEX_STYLES):
                it = {"brief": {"how_many": HOW_MANY // 2, "style": style, "x_stands_for": A.LEX_SUBJECT[dim],
                                "example": A.CANON_FORMS[sem][s_i]},
                      "meaning": meaning + "; edge case: " + A.LEX_EDGE[sem],
                      "slots": {"X": A.LEX_SUBJECT[dim]},
                      "rules": [f"{HOW_MANY // 2} sentences", "{X} exactly once", "one sentence each, ending with a full stop"]}
                if op:
                    it = _fit(self.chunk_kind, it, "dev-only: never start a sentence with any of these openings (the program "
                              "already has them): " + "; ".join(f"'{o}'" for o in op), self.forbid)
                iid = f"t07-{VERSION}-lex-{sem}-{s_i}"
                items.append((iid, it))
                plan[iid] = {"unit": sem, "kind": kind, "style": s_i}
        return items, plan

    def lint(self, meta, text, seen):
        return self.mod("authoring").lint_form(meta["unit"], text) if isinstance(text, str) else ["not a string"]


class T06A(Adapter):
    fam = "T06"
    unit_kind = "sem"
    answer_field = "text"
    max_items = 28

    @property
    def prompt(self):
        return self.mod("haiku_author").NOTICE_PROMPT

    answer_format = "notice"

    @property
    def forbid(self):
        return self.mod("haiku_author").QSTRINGS

    def units(self, reg):
        H = self.mod("haiku_author")
        return [s for s in _lex_units(reg) if s in H.NOTICE_MEANING]

    def items(self, reg, unit_texts):
        H = self.mod("haiku_author")
        items, plan = [], {}
        for sem in self.units(reg):
            kind, meaning, example = H.NOTICE_MEANING[sem]
            slots = {"P": "count"} if kind == "window" else {}
            op = openings(unit_texts[sem])
            for i in range(HOW_MANY):
                it = {"brief": f"Write a returns notice with this meaning. Example of the shape (do not copy it): \"{example}\"",
                      "meaning": meaning, "slots": slots,
                      "rules": [f"Shape hint: {H.NOTICE_SHAPES[kind][i % len(H.NOTICE_SHAPES[kind])]}."]}
                if op:
                    it = _fit(self.chunk_kind, it, "dev-only: never start the notice with any of these openings (the program "
                              "already has them): " + "; ".join(f"'{o}'" for o in op), self.forbid)
                iid = f"t06-{VERSION}-notice-{sem}-{i:02d}"
                items.append((iid, it))
                plan[iid] = {"unit": sem, "kind": kind, "slots": slots}
        return items, plan

    def lint(self, meta, text, seen):
        if not isinstance(text, str) or not text.strip():
            return ["no text"]
        text = " ".join(text.split())
        return self.mod("haiku_author").notice_problems(meta["unit"], text)


class T25A(Adapter):
    fam = "T25"
    unit_kind = "qform"
    chunk_kind = "author_wording"
    answer_field = "text"
    max_items = 28

    @property
    def prompt(self):
        return self.mod("haiku_author").WORDING_PROMPT

    answer_format = "wording"

    @property
    def forbid(self):
        return self.mod("haiku_author").FORBID_LEX

    def units(self, reg):
        return sorted(self.mod("haiku_author").WORDING_PLAN)

    def items(self, reg, unit_texts):
        H = self.mod("haiku_author")
        items, plan = [], {}
        for qf in self.units(reg):
            meaning, neg_rule = H.WORDING_BRIEF[qf]
            styles = H.DNEG_STYLES if qf == "yn_claim_dneg" else H.STYLES
            for i in range(HOW_MANY):
                with_attr = i % 2 == 0
                iid = f"t25-{VERSION}-wording-{qf}-{i:02d}"
                items.append((iid, {"brief": meaning, "slots": {"ATTR": "name"} if with_attr else {},
                                    "rules": [neg_rule, f"Style hint: {styles[i % len(styles)]}."]}))
                plan[iid] = {"unit": qf, "qform": qf, "attr": with_attr}
        return items, plan

    def lint(self, meta, text, seen):
        H = self.mod("haiku_author")
        obj, v = H.check_wording("x", text, meta, "x", "x", seen)
        return list(v)

    def slots(self, reg, meta):
        return {"ATTR": "name"} if meta["attr"] else {}


ADAPTERS = {"T24": T24A, "T06": T06A, "T07": T07A, "T25": T25A}


# ================================================================================================ task files
def task_file_text(adapter: Adapter, b, chunk: dict, answer_abs: str, title: str, answer_format: str) -> str:
    n = len(chunk["items"])
    return "\n".join([
        f"# {title} {chunk['task_id']} (family {adapter.fam}, kind {b.kind})", "",
        "Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool "
        "to exactly this path (nothing else, no other file):", "", f"ANSWER FILE: {answer_abs}", "",
        f"The answer is one JSON list with exactly {n} objects, one per item below, each carrying that item's qid.", "",
        "## Instructions", "", b.prompt.rstrip(), "", "## Answer format", "", answer_format, "",
        f"## Items ({n}; one JSON object per line)", "", "```json",
        "[\n" + ",\n".join(json.dumps(it, ensure_ascii=False) for it in chunk["items"]) + "\n]", "```", ""])


AUTHOR_FORMAT = {
    "forms": '[{"qid": "<qid of the item>", "forms": ["<form 1>", "<form 2>", ...]}, ...]  (give exactly the number of forms each item asks for)',
    "notice": '[{"qid": "<qid of the item>", "text": "<the notice>"}, ...]',
    "wording": '[{"qid": "<qid of the item>", "text": "<the question>"}, ...]',
}


def build_batch(fam: str, kit=None):
    """(adapter, batch, plan, reg-free info) for the author tasks of `fam`. Needs the kit only for the registry (units,
    training openings)."""
    ad = ADAPTERS[fam]()
    own = kit is None
    ctx_mgr = open_kit(fam) if own else contextlib.nullcontext(kit)
    with ctx_mgr as k:
        reg = k.ctx.lexicon
        units = ad.units(reg)
        unit_texts = {u: _train_texts(reg, ad.sem_of(u)) for u in units}
        items, plan = ad.items(reg, unit_texts)
        unit_info = {u: {"sem": ad.sem_of(u), "kind": reg.sems[ad.sem_of(u)].kind, "required_reads": ad.required_reads(reg, u),
                         "training_forms": len(unit_texts[u])} for u in units}
    b = chunker.make_batch(ad.chunk_kind, fam, items, seed=f"{fam}-a55-dev-author-{VERSION}", prompt=ad.prompt,
                           max_items=ad.max_items, forbid_strings=ad.forbid)
    return ad, b, plan, unit_info


def plan_counts(fam: str) -> dict:
    ad, b, plan, ui = build_batch(fam)
    return {"family": fam, "units": len(ui), "items": len(b.key), "tasks": len(b.chunks),
            "outputs_asked": len(b.key) * (1 if ad.answer_field == "text" else HOW_MANY // 2),
            "by_kind": dict(Counter(u["kind"] for u in ui.values())), "units_detail": ui}


def write_author(fam: str, root: Path | None = None) -> dict:
    root = root or dev_dir(fam)
    ad, b, plan, ui = build_batch(fam)
    files = dict(b.files())
    files[f"plan/{b.batch_id}.json"] = json.dumps({"batch_id": b.batch_id, "family": fam, "ruling": "A55 (d2/d3)", "plan": plan,
                                                   "units": ui}, indent=1, sort_keys=True) + "\n"
    tasks = []
    for c in b.chunks:
        tid = c["task_id"]
        ans = root / b.answer_path(tid)
        tf = root / f"tasks/{tid}.md"
        txt = task_file_text(ad, b, c, str(ans), f"A55 dev-only authoring task", AUTHOR_FORMAT[ad.answer_format])
        files[f"tasks/{tid}.md"] = txt
        tasks.append({"task_id": tid, "task_file": str(tf), "answer_file": str(ans), "kind": b.kind, "batch_id": b.batch_id,
                      "n_items": len(c["items"]), "prompt_sha": b.prompt_sha, "task_sha256": C.sha_text(txt),
                      "audit_allowed_read": [str(tf)], "audit_allowed_write": [str(ans)]})
    files["answers/README.txt"] = "Haiku answer files: one <task_id>.json per task file in ../tasks/.\n"
    files["TASKS.json"] = json.dumps({"family": fam, "ruling": "A55 (draft)", "version": VERSION, "n_tasks": len(tasks),
                                      "batch_id": b.batch_id, "prompt_sha": b.prompt_sha, "tasks": tasks,
                                      "units": ui, "per_unit_authored": HOW_MANY, "per_unit_needed": MIN_ADMITTED},
                                     indent=1) + "\n"
    paths.write_files(root, files)
    return {"family": fam, "tasks": [t["task_id"] for t in tasks], "items": len(b.key), "dir": str(root.relative_to(C.LEAN))}


# ================================================================================================ admit
def default_checker(recs: list) -> dict:
    return X.run_checker(X.G13_OHS4_TOOL, "--rows", recs)


def ohs4_counts(fam: str, reg, cands: list, checker=default_checker) -> dict:
    """g13_ohs4_check through g13_c2.run_checker on every candidate form (the text as written, with {X} placeholders, and the text
    rendered with the kit's sample values). Counts only: returns {"status", "records", "hit_forms": [form ids]}; a status other than
    'scanned' stops the admission (nothing is admitted unchecked)."""
    recs, back = [], {}
    for c in cands:
        fid = c["form_id"]
        for tag, t in (("raw", X.SLOT_RE.sub("{X}", c["text"])), ("sample", None)):
            if t is None:
                try:
                    t = reg.render(fid, reg._samples(reg.forms[fid])[0])
                except Exception:  # noqa: BLE001
                    continue
            rid = f"a55|{fam}|{fid}|{tag}"
            recs.append({"id": rid, "call_id": rid, "state": t})
            back[rid] = fid
    if not recs:
        return {"status": "scanned", "records": 0, "hit_ids": 0, "hit_forms": []}
    r = checker(recs)
    if r.get("status") != "scanned":
        raise SystemExit(f"{fam}: g13_ohs4_check did not scan ({r.get('status')}); nothing is admitted unchecked")
    hit = sorted({back[i] for i in r.get("hit_ids", []) if i in back})
    return {"status": r["status"], "records": len(recs), "hit_ids": len(r.get("hit_ids", [])), "hit_forms": hit}


def _matching_forms(reg, text, schema) -> list:
    out = []
    for f in reg.forms.values():
        try:
            m = reg._regex(f, {}, True).fullmatch(text.strip())
        except Exception:  # noqa: BLE001
            m = None
        if m:
            out.append(f)
    return out


def admit(fam: str, root: Path | None = None, checker=default_checker, skip_tasks=()) -> dict:
    root = root or dev_dir(fam)
    tasks = json.loads((root / "TASKS.json").read_text())
    with open_kit(fam) as kit:
        ad, b, plan, ui = build_batch(fam, kit)
        reg = kit.ctx.lexicon
        if b.batch_id != tasks["batch_id"]:
            raise SystemExit(f"{fam}: the batch id changed since the tasks were written ({b.batch_id} != {tasks['batch_id']})")
        raw, missing = {}, []
        for c in b.chunks:
            f = root / b.answer_path(c["task_id"])
            if c["task_id"] in skip_tasks or not f.is_file():          # an agent whose file-access audit failed is ignored
                missing.append(c["task_id"])
                continue
            try:
                raw[c["task_id"]] = json.loads(f.read_text(encoding="utf-8"))
            except ValueError:
                missing.append(c["task_id"] + " (not JSON)")
        got, probs = chunker.load_answers(b, raw)
        pool = pool_texts(fam, kit)
        old_ok = {fid: f.unit_ok for fid, f in reg.forms.items()}
        pieces, rej = [], []
        seen, lint_seen = set(), set()
        for iid in sorted(got):
            meta = plan[iid]
            for j, t in enumerate(ad.texts_of(got[iid])):
                pid = f"{iid}#{j}"
                if isinstance(t, str):
                    t = " ".join(t.split()) if ad.answer_field == "text" else t
                why = ad.lint(meta, t, lint_seen) if isinstance(t, str) else ["not a string"]
                if not why and norm(t) in pool:
                    why = ["text equals a pool entry of the family"]
                if not why and norm(t) in seen:
                    why = ["duplicate dev text"]
                if why:
                    rej.append({"piece_id": pid, "unit": meta["unit"], "stage": "lint/pool", "reasons": why[:3]})
                    continue
                seen.add(norm(t))
                pieces.append({"piece_id": pid, "iid": iid, "unit": meta["unit"], "text": t, "meta": meta})
        task_of = {b.key[it["qid"]]: c["task_id"] for c in b.chunks for it in c["items"]}
        cands = []
        for p in pieces:
            sem = ad.sem_of(p["unit"])
            slots = ad.slots(reg, p["meta"])
            try:
                f = reg.add(p["text"], sem, slots=slots, source="haiku", family=fam, haiku_task_id=task_of[p["iid"]],
                            haiku_prompt_sha=b.prompt_sha, held_out=True)
            except Exception as e:  # noqa: BLE001
                rej.append({"piece_id": p["piece_id"], "unit": p["unit"], "stage": "registry", "reasons": [str(e)[:120]]})
                continue
            cands.append({"form_id": f.form_id, "unit": p["unit"], "sem_id": sem, "kind": reg.sems[sem].kind, "text": p["text"],
                          "slots": slots, "haiku_task_id": task_of[p["iid"]], "haiku_prompt_sha": b.prompt_sha,
                          "piece_id": p["piece_id"], **({"qform": p["unit"]} if ad.unit_kind == "qform" else {})})
        # G-LEX unit test of every new form; an old form that stops passing because of a new one drops the new form that matches it
        for c in cands:
            reg.unit_test(c["form_id"])
        dropped = {c["form_id"] for c in cands if not reg.forms[c["form_id"]].unit_ok}
        for c in cands:
            if c["form_id"] in dropped:
                rej.append({"piece_id": c["piece_id"], "unit": c["unit"], "stage": "unit_test",
                            "reasons": reg.forms[c["form_id"]].unit_problems[:2]})
        new_ids = {c["form_id"] for c in cands}
        for _ in range(3):
            broke = []
            new_kinds = {reg.forms[i].kind for i in new_ids if i in reg.forms}
            for fid, f in list(reg.forms.items()):
                if fid in new_ids or fid in dropped or not old_ok.get(fid) or f.kind not in new_kinds:
                    continue
                if not reg.unit_test(fid):
                    broke.append(fid)
            if not broke:
                break
            culprits = set()
            for fid in broke:
                f = reg.forms[fid]
                for vals in reg._samples(f):
                    schema = {k: v.schema for k, v in vals.items()}
                    try:
                        txt = reg.render(fid, vals)
                    except Exception:  # noqa: BLE001
                        continue
                    culprits |= {m.form_id for m in _matching_forms(reg, txt, schema)
                                 if m.form_id in new_ids and m.form_id not in dropped and m.sem_id != f.sem_id}
            if not culprits:
                raise SystemExit(f"{fam}: an existing form fails its unit test and no new form is the cause: {broke[:3]}")
            dropped |= culprits
            for c in cands:
                if c["form_id"] in culprits:
                    rej.append({"piece_id": c["piece_id"], "unit": c["unit"], "stage": "breaks_existing_form", "reasons": ["ambiguity"]})
        cands = [c for c in cands if c["form_id"] not in dropped]
        chk = ohs4_counts(fam, reg, cands, checker)
        hit = set(chk["hit_forms"])
        for c in cands:
            if c["form_id"] in hit:
                rej.append({"piece_id": c["piece_id"], "unit": c["unit"], "stage": "run_checker", "reasons": ["g13_ohs4_check hit"]})
        cands = [c for c in cands if c["form_id"] not in hit]
        per = {u: {"authored": sum(1 for p in plan.values() if p["unit"] == u) * (1 if ad.answer_field == "text" else HOW_MANY // 2),
                   "candidates": sum(1 for c in cands if c["unit"] == u),
                   "rejected": dict(Counter(r["stage"] for r in rej if r["unit"] == u))} for u in ui}
    rep = {"family": fam, "created_utc": C.utc(), "batch_id": b.batch_id, "prompt_sha": b.prompt_sha, "answer_files_missing": missing,
           "load_problems": probs[:20], "n_candidates": len(cands), "n_rejected": len(rej), "run_checker": {k: v for k, v in chk.items()},
           "units": per}
    paths.write_json(root / "ADMITTED.json", {"report": rep, "candidates": cands, "rejected": rej})
    return rep


# ================================================================================================ G-LEX reads
def _read_plan(fam: str, reg, cands: list, ad: Adapter) -> dict:
    """{read id: [form ids]}: reads r1, r2 cover every candidate; r3 the forms of the strict kinds (precedence, window)."""
    plan = {"r1": [c["form_id"] for c in cands], "r2": [c["form_id"] for c in cands]}
    strict = [c["form_id"] for c in cands if reg.sems[c["sem_id"]].kind in STRICT_KINDS]
    if strict:
        plan["r3"] = strict
    return plan


def _register(reg, cands: list, fam: str, held_out: bool = True) -> None:
    for c in cands:
        reg.add(c["text"], c["sem_id"], slots=dict(c["slots"]), source="haiku", family=fam,
                haiku_task_id=c["haiku_task_id"], haiku_prompt_sha=c["haiku_prompt_sha"], held_out=held_out)
    for c in cands:
        reg.unit_test(c["form_id"])


def _read_batches(reg, plan: dict, fam: str) -> dict:
    out = {}
    for rd, fids in plan.items():
        items = reg.lexicon_items(fids, seed=f"a55-{fam}-{rd}")
        out[rd] = chunker.make_batch("extract_lex", fam, items, seed=f"{fam}-a55-glex-{rd}-{VERSION}", prompt=GLEX_PROMPT, max_items=50)
    return out


def write_glex(fam: str, root: Path | None = None) -> dict:
    root = root or dev_dir(fam)
    adm = json.loads((root / "ADMITTED.json").read_text())
    cands = adm["candidates"]
    ex = root / "extract"
    with open_kit(fam) as kit:
        reg = kit.ctx.lexicon
        ad = ADAPTERS[fam]()
        _register(reg, cands, fam)
        plan = _read_plan(fam, reg, cands, ad)
        batches = _read_batches(reg, plan, fam)
    files, tasks = {}, []
    for rd, b in batches.items():
        files.update(b.files())
        for c in b.chunks:
            tid = c["task_id"]
            ans, tf = ex / b.answer_path(tid), ex / f"tasks/{tid}.md"
            txt = task_file_text(ad, b, c, str(ans), "A55 G-LEX read", '[{"qid": "<qid of the item>", "meaning": "<the chosen choice, copied exactly>"}, ...]')
            files[f"tasks/{tid}.md"] = txt
            tasks.append({"read": rd, "task_id": tid, "batch_id": b.batch_id, "task_file": str(tf), "answer_file": str(ans),
                          "n_items": len(c["items"]), "prompt_sha": b.prompt_sha, "task_sha256": C.sha_text(txt),
                          "audit_allowed_read": [str(tf)], "audit_allowed_write": [str(ans)]})
    files["answers/README.txt"] = "Haiku G-LEX answer files: one <task_id>.json per task file in ../tasks/.\n"
    files["TASKS.json"] = json.dumps({"family": fam, "ruling": "A55 (d2/d3)", "version": VERSION, "forms_for_admission": len(cands),
                                      "reads": {rd: len(v) for rd, v in plan.items()}, "required_reads_per_form":
                                      "2 (3 for the kinds precedence and window)", "n_tasks": len(tasks), "tasks": tasks}, indent=1) + "\n"
    paths.write_files(ex, files)
    return {"family": fam, "reads": {rd: len(v) for rd, v in plan.items()}, "tasks": len(tasks)}


# ================================================================================================ score and freeze
def score(fam: str, root: Path | None = None, skip_tasks=()) -> dict:
    root = root or dev_dir(fam)
    ex = root / "extract"
    adm = json.loads((root / "ADMITTED.json").read_text())
    cands = adm["candidates"]
    etasks = json.loads((ex / "TASKS.json").read_text())
    with open_kit(fam) as kit:
        reg = kit.ctx.lexicon
        ad = ADAPTERS[fam]()
        _register(reg, cands, fam)
        plan = _read_plan(fam, reg, cands, ad)
        batches = _read_batches(reg, plan, fam)
        votes, problems, missing = 0, [], []
        for rd, b in batches.items():
            raw = {}
            for c in b.chunks:
                tid = c["task_id"]
                f = ex / b.answer_path(tid)
                if tid in skip_tasks or not f.is_file():
                    missing.append(tid)
                    continue
                try:
                    raw[tid] = json.loads(f.read_text(encoding="utf-8"))
                except ValueError:
                    missing.append(tid + " (not JSON)")
            got, probs = chunker.load_answers(b, raw)
            problems += probs[:10]
            tid_of = {b.key[q]: b.task_of[q] for q in b.key}
            for fid, a in got.items():
                m = a.get("meaning") if isinstance(a, dict) else None
                tid = tid_of[fid]
                reg.record_extraction(fid, f"haiku:{tid}", reg.meaning_to_sem(reg.forms[fid].kind, m) if isinstance(m, str) else None)
                votes += 1
        status = {c["form_id"]: reg.status(c["form_id"]) for c in cands}
        units: dict = {}
        for c in cands:
            u = units.setdefault(c["unit"], {"sem": c["sem_id"], "kind": c["kind"], "required_reads": reg.forms[c["form_id"]].required,
                                             "candidates": 0, "admitted": 0, "rejected": 0, "pending": 0})
            u["candidates"] += 1
            st = status[c["form_id"]]
            u["admitted" if st == "admitted" else "rejected" if st in ("rejected", "unit_fail") else "pending"] += 1
        for u in units.values():
            u["used"] = u["admitted"] >= MIN_ADMITTED
        forms = []
        for c in cands:
            if status[c["form_id"]] != "admitted":
                continue
            f = reg.forms[c["form_id"]]
            forms.append({**{k: c[k] for k in ("form_id", "unit", "sem_id", "kind", "text", "slots", "haiku_task_id", "haiku_prompt_sha")},
                          **({"qform": c["qform"]} if "qform" in c else {}), "extractions": [list(e) for e in f.extractions]})
    kinds: dict = {}
    for u, d in units.items():
        k = kinds.setdefault(d["kind"], {"units": 0, "units_used": 0, "admitted_forms": 0})
        k["units"] += 1
        k["units_used"] += int(d["used"])
        k["admitted_forms"] += d["admitted"]
    fr = {"family": fam, "ruling": "A55 (d2/d3)", "created_utc": C.utc(), "min_admitted_per_unit": MIN_ADMITTED, "units": units,
          "kinds": kinds, "forms": sorted(forms, key=lambda f: f["form_id"]), "votes": votes, "answer_files_missing": missing,
          "load_problems": problems, "run_checker": adm["report"]["run_checker"],
          "note": "unit = a sem (rule forms) or a question form (wordings); a unit with fewer than 4 admitted forms keeps its "
                  "training forms in dev (used: false)"}
    fr["self_sha256"] = C.sha_text(json.dumps({k: v for k, v in fr.items() if k != "created_utc"}, sort_keys=True))
    if missing:
        fr["INCOMPLETE"] = True
    paths.write_json(root / "FROZEN.json", fr)
    fr["file_sha256"] = C.sha_file(root / "FROZEN.json")
    return {k: fr[k] for k in ("family", "units", "kinds", "votes", "answer_files_missing", "self_sha256", "file_sha256")}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=("plan", "write", "admit", "glex", "score"))
    ap.add_argument("families", nargs="+")
    ap.add_argument("--audit-failed", nargs="*", default=[], metavar="TASK_ID",
                    help="admit / score: answers of an agent whose file-access audit failed are ignored")
    a = ap.parse_args(argv)
    fn = {"plan": plan_counts, "write": write_author, "admit": admit, "glex": write_glex, "score": score}[a.cmd]
    for f in a.families:
        if f not in ADAPTERS:
            raise SystemExit(f"{f}: dev-only forms are authored for {sorted(ADAPTERS)}")
        kw = {"skip_tasks": tuple(a.audit_failed)} if a.cmd in ("admit", "score") else {}
        print(json.dumps(fn(f, **kw), default=str, indent=1))


if __name__ == "__main__":
    main()
