"""transfer/T19/redo3_reads.py: T19 redo round 3, step 2: load the redo3 authoring answer, run the family's lint and
dedup on its candidates, and build the G-LEX read tasks for the lint-clean ones (G0_SPEC.md v1.1 section 6 and its
sha256 unchanged; C2_DATA_SPEC 6.2, 6.3; PREREG A37 (b), A38). Haiku writes text only and reads only to flag; nothing
here sets, edits or chooses a label or a read's answer, no target is lowered and no bar is loosened.

Inputs (read only): haiku/redo3/REDO3_INDEX.json, the task file and haiku/redo3/answers/<task>.json, pools_v2/ (the
frozen admitted lexicon, wordings and quarantine), the round 1 and redo2 answers (for dedup).

Steps
  1. answer   the answer file is checked against its contract (freeze_v2.check_answer: one JSON array, one
              {"qid", "texts"} object per item, exactly 3 texts, nothing else) plus: the 3 texts of an item differ.
              An invalid file is rejected whole, never repaired. An audit-failed task would not be opened at all
              (AUDIT_FAILED is empty this round).
  2. lint     per candidate, as redo2.lint_candidate does for wordings: haiku_author.check_wording (G-SL role wording,
              exact negation counts for yn_not_compliant, "checklist" and "audit date", one question line, no fixture
              copy, exact dedup), freeze.wording_problems ({SITE} once, no other slot) and redo2.phrase_problems (key
              phrase 'not compliant with'). Stricter only, from the item rules: 8-30 words; the candidate's assigned
              opening; the fixed ending of R6; no digit; no capital letter besides the first and the placeholder.
              Dedup (exact, normalised) against every round 1 wording (admitted, rejected or duplicate), every
              pools_v2 wording and quarantined form, every redo2 candidate, the fixture questions, and the
              candidates before it in this answer.
  3. G-LEX    one LexiconRegistry: the frozen admitted lexicon pools_v2/lexicon.json plus every lint-clean candidate
              (source haiku). A candidate whose add or unit test fails in the combined registry is dropped and logged;
              the registry is rebuilt until it is stable. A frozen form that stops passing its unit test stops the run.
  4. reads    2 independent G-LEX reads (question wordings: 2/2; T19 has no precedence or window forms). Each read is its
              own batch with its own seed and a NEW extractor id; each is one chunk file and so one task file. Items
              are the lint-clean candidates, {SITE} = 'Larch Street depot' (redo2's R4), extract_build.PROMPT_LEX and
              the closed meaning list unchanged. The reads of unkept candidates cost nothing and are harmless: the
              keep rule of REDO3_INDEX.json (at most 1 piece for the cell, first admitted candidate of the first item
              that has one) is applied after the reads.

Every write goes through paths.write_files (refuses before A38 and on never-open paths) and is written once.

  cd lean && ../.venv/bin/python c2_build/transfer/T19/redo3_reads.py lint     in memory: answer check + lint + G-LEX registry
  cd lean && ../.venv/bin/python c2_build/transfer/T19/redo3_reads.py tasks    in memory: the read tasks
  cd lean && ../.venv/bin/python c2_build/transfer/T19/redo3_reads.py write    write haiku/redo3/reads/...
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, paths  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.lexicon import LexiconError, LexiconRegistry, question_sem  # noqa: E402
from c2_kit.paths import never_open  # noqa: E402
from transfer.T19 import extract_build as EX  # noqa: E402
from transfer.T19 import freeze as FZ  # noqa: E402
from transfer.T19 import freeze_v2 as F2  # noqa: E402
from transfer.T19 import haiku_author as HA  # noqa: E402
from transfer.T19 import plugin as P  # noqa: E402
from transfer.T19 import redo2 as RD  # noqa: E402
from transfer.T19 import redo3 as R3  # noqa: E402

FAMILY = P.FAMILY
VERSION = "redo3-reads-v1"
QFORM = R3.QFORM
CELL = R3.CELL
ROOT = R3.ROOT
XROOT = ROOT / "reads"
INDEX = ROOT / "REDO3_INDEX.json"
POOLS_V2 = F2.POOLS_V2_PREV   # the baseline freeze (see redo3.py): the lexicon the reads are built beside
SAMPLE_SITE = RD.SAMPLE_SITE                      # redo2's R4: {SITE} is filled with this name in the G-LEX items
# New extractor ids and seeds (the round 1 reads used haiku-glex-question-r{1,2}; redo2 haiku-glex-question-redo2-r{1,2})
GLEX_READS = (("glex-question-redo3-r1", "haiku-glex-question-redo3-r1", "t19-redo3-glex-question-r1"),
              ("glex-question-redo3-r2", "haiku-glex-question-redo3-r2", "t19-redo3-glex-question-r2"))
AUDIT_FAILED: tuple = ()                          # the harness's list for this round: []; nothing is ignored
ENDING = " is {SITE} not compliant with its checklist on the audit date?"        # R6 (redo3.SHAPE), stricter only


def _sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _norm(s) -> str:
    return " ".join(str(s).split()).lower()


# ------------------------------------------------------------------------------------------------ 1. the answer

def task() -> dict:
    """The one redo3 authoring task, from REDO3_INDEX.json. The task file on disk must equal the task that redo3.py
    rebuilds now (so the answer is judged against the text the agent was given)."""
    idx = _read(INDEX)
    if len(idx["tasks"]) != 1:
        raise SystemExit(f"redo3 holds one task, found {len(idx['tasks'])}")
    t = dict(idx["tasks"][0])
    built = R3.build()[0]
    disk = Path(t["task_file"]).read_text(encoding="utf-8")
    if disk != built["text"] or _sha(disk) != t["task_sha256"]:
        raise SystemExit("the redo3 task file on disk differs from redo3.build(): the answer cannot be judged")
    t["order"] = list(idx["order"])
    t["gap"] = idx["b_authoring"]["gap"]
    return t


def load_answer(t: dict, raw=None) -> tuple:
    """({qid: [candidates]}, problems). An invalid answer is rejected whole (never repaired). `raw`: the parsed
    answer, for tests."""
    if t["name"] in AUDIT_FAILED:
        return {}, [f"{t['name']}: file-access audit failed, answer not opened"]
    if raw is None:
        f = Path(t["answer_file"])
        if not f.is_file() or f.stat().st_size <= 2:
            return {}, [f"{t['name']}: no answer file"]
        try:
            raw = _read(f)
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            return {}, [f"{t['name']}: answer file is not JSON ({str(e)[:80]})"]
    probs = F2.check_answer(raw, {"field": "texts", "qids": t["qids"], "n_cand": t["n_candidates"]})
    if not probs:
        if len(raw) != t["n_items"]:
            probs.append(f"{len(raw)} entries, want {t['n_items']}")
        for a in raw:
            texts = a["texts"]
            if len({_norm(x) for x in texts}) != len(texts):
                probs.append(f"{a['qid']}: the {len(texts)} texts are not all different")
            probs += [f"{a['qid']}: candidate {j} is empty" for j, x in enumerate(texts) if not x.strip()]
    if probs:
        return {}, [f"{t['name']}: {p}" for p in probs]
    return {a["qid"]: list(a["texts"]) for a in raw}, []


# ------------------------------------------------------------------------------------------------ 2. lint and dedup

def seen_texts() -> set:
    """Normalised text of every question wording written so far in the family, whatever became of it (never
    re-voted): round 1 answers (admitted, rejected or duplicate) and the fixture questions, the pools_v2 wordings
    and quarantined forms, every redo2 candidate."""
    out = set(RD.seen_wordings())
    out |= {_norm(w["text"]) for w in _read(POOLS_V2 / "wordings.json")}
    q = _read(POOLS_V2 / "quarantine.json")
    for src in q.values():
        for f in src.get("forms_not_admitted", []):
            out.add(_norm(f["text"]))
        drops = src.get("lexicon_drops_before_reads", [])
        for f in drops if isinstance(drops, list) else []:
            if isinstance(f, dict) and f.get("text"):
                out.add(_norm(f["text"]))
    for p in sorted((HERE / "haiku" / "redo2" / "answers").glob("T19-redo2-wordings-*.json")):
        for a in _read(p):
            out |= {_norm(x) for x in a["texts"]}
    return out


def _opening(frame: str) -> str:
    m = re.fullmatch(r"open with '(.+)'", frame)
    if not m:
        raise SystemExit(f"opening frame not understood: {frame!r}")
    return m.group(1)


def extra_problems(text: str, opening: str) -> list:
    """Item-rule checks that are stricter than the loaders' (never looser)."""
    out = []
    n = len(text.split())
    if not 8 <= n <= 30:
        out.append(f"{n} words (8-30)")
    if not text.startswith(opening + " "):
        out.append(f"does not open with {opening!r}")
    if not text.endswith(ENDING):
        out.append("does not end with the fixed shape (R6)")
    if re.search(r"\d", text):
        out.append("digit")
    if re.search(r"[A-Z]", K.PH_RE.sub("x", text)[1:]):
        out.append("capital letter inside the sentence")
    return out


def lint(t: dict, cands: dict) -> list:
    """[{qid, j, text, ok, reasons}] in the keep order (items in `order`, candidates in written order). Dedup is
    exact and normalised, against seen_texts() and the clean candidates before it."""
    seen = seen_texts()
    rows = []
    for q in t["order"]:
        frames = t["openings"][q]
        for j, cand in enumerate(cands.get(q, [])):
            tmp = set(seen)
            try:
                obj, v = HA.check_wording(f"{q}|c{j}", cand, {"qform": QFORM}, t["name"], t["prompt_sha256"], tmp)
                text = obj[1] if obj is not None else " ".join(str(cand).split())
                if obj is not None:
                    v = v + FZ.wording_problems(text) + RD.phrase_problems(QFORM, text)
                v = v + extra_problems(text, _opening(frames[j]))
            except Exception as e:  # noqa: BLE001  (a malformed candidate is dropped, never fixed)
                text, v = " ".join(str(cand).split()), [f"unusable: {str(e)[:100]}"]
            rows.append({"qid": q, "j": j, "key": f"{q}|c{j}", "text": text, "ok": not v, "reasons": v})
            if not v:
                seen.add(_norm(text))
    return rows


# ------------------------------------------------------------------------------------------------ 3. G-LEX registry

def glex_registry(rows: list, t: dict) -> tuple:
    """(registry, {candidate key: form id}, drops): pools_v2/lexicon.json (the frozen admitted forms) plus every
    lint-clean candidate; rebuilt until stable (as redo2.glex_registry, whose base is the v1 lexicon)."""
    base = _read(POOLS_V2 / "lexicon.json")
    pending = [r for r in rows if r["ok"]]
    drops = []
    while True:
        reg = LexiconRegistry.from_json(base)
        base_ids = set(reg.forms)
        added = []
        for r in pending:
            try:
                fo = reg.add(r["text"], question_sem(FAMILY, QFORM), slots={"SITE": "name"}, source="haiku",
                             family=FAMILY, haiku_task_id=t["name"], haiku_prompt_sha=t["prompt_sha256"])
            except LexiconError as e:
                drops.append({**r, "reasons": [f"G-LEX add: {e}"]})
                continue
            added.append((r, fo.form_id))
        res = reg.unit_test_all()
        broken = sorted(f for f in base_ids if not res[f])
        if broken:
            raise SystemExit(f"frozen lexicon forms fail their unit test beside the redo3 forms: {broken[:3]}")
        bad = {fid for _r, fid in added if not res[fid]}
        if not bad:
            return reg, {r["key"]: fid for r, fid in added}, drops
        drops += [{**r, "reasons": [f"G-LEX unit: {x}" for x in reg.forms[fid].unit_problems[:2]]}
                  for r, fid in added if fid in bad]
        pending = [r for r, fid in added if fid not in bad]


# ------------------------------------------------------------------------------------------------ 4. read tasks

def _batch(items: list, seed: str):
    n = len(items)
    chunks = max(1, math.ceil(n / chunker.MAX_ITEMS))
    return chunker.make_batch("extract_lex", FAMILY, items, seed=seed, prompt=EX.PROMPT_LEX,
                              max_items=math.ceil(n / chunks))


def build(raw=None) -> dict:
    """The whole step in memory: answer check, lint, registry, the 2 reads and their files. `raw` (tests only):
    the parsed answer."""
    t = task()
    cands, probs = load_answer(t, raw)
    out = {"task": t, "answer_problems": probs, "lint": [], "reg": None, "fid_of": {}, "lex_drops": [], "reads": [],
           "files": {}, "tasks": []}
    if probs:
        return out
    rows = lint(t, cands)
    reg, fid_of, drops = glex_registry(rows, t)
    out.update(lint=rows, reg=reg, fid_of=fid_of, lex_drops=drops)
    fids = sorted(fid_of.values())
    if not fids:
        return out
    for label, extractor, seed in GLEX_READS:
        items = []
        for fid, it in reg.lexicon_items(fids, seed=seed):
            items.append((fid, {"text": reg.render(fid, {"SITE": S.name_slot(SAMPLE_SITE)}),
                                "choices": it["choices"]}))
        b = _batch(items, seed)
        out["reads"].append({"label": label, "extractor_id": extractor, "batch": b})
        out["files"].update(b.files())
        out["files"][f"plan/{b.batch_id}.json"] = json.dumps(
            {"batch_id": b.batch_id, "label": label, "kind": "extract_lex", "extractor_id": extractor},
            indent=1, sort_keys=True) + "\n"
        for c in b.chunks:
            tid = c["task_id"]
            ans = str(XROOT / b.answer_path(tid))
            tfile = f"tasks/{tid}.md"
            text = EX.task_markdown("extract_lex", b, c, Path(ans))
            probs = []
            if any(iid in text for iid in b.key.values()) or "t19a." in text:
                probs.append("names an internal id")
            if any(r["key"] in text for r in rows):
                probs.append("names a candidate key")
            for p in (ans, str(XROOT / tfile)):
                if never_open(p):
                    probs.append(f"never-open path {p}")
            if ans not in text:
                probs.append("answer path missing from the task text")
            if probs:
                raise chunker.ChunkError(f"{tid}: {probs}")
            out["files"][tfile] = text
            out["tasks"].append({"task": label, "task_id": tid, "kind": "extract_lex", "batch_id": b.batch_id,
                                 "extractor_id": extractor, "task_file": str(XROOT / tfile), "answer_file": ans,
                                 "n_items": len(c["items"]), "outputs_expected": len(c["items"]),
                                 "prompt_sha": b.prompt_sha, "task_sha256": _sha(text),
                                 "allowed_read": [str(XROOT / tfile)], "allowed_write": [ans]})
    out["files"]["key/glex_forms.json"] = json.dumps(
        {r["key"]: {"form_id": fid_of.get(r["key"]), "qid": r["qid"], "j": r["j"], "qform": QFORM, "text": r["text"]}
         for r in rows if r["ok"]}, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
    out["files"]["LINT.json"] = json.dumps(
        {"family": FAMILY, "version": VERSION, "task": t["name"], "answer_sha256": _sha(
            Path(t["answer_file"]).read_text(encoding="utf-8")) if raw is None else None,
         "keep_rule": _read(INDEX)["keep_rule"], "order": t["order"],
         "candidates": [{k: r[k] for k in ("qid", "j", "text", "ok", "reasons")} for r in rows],
         "lexicon_drops": [{k: r[k] for k in ("qid", "j", "text", "reasons")} for r in drops]},
        indent=1, ensure_ascii=False) + "\n"
    out["files"]["TASKS.json"] = json.dumps({
        "family": FAMILY, "version": VERSION, "stage": "redo3 reads", "sample_site": SAMPLE_SITE,
        "prompts": "extract_build.PROMPT_LEX, unchanged; closed meaning list unchanged", "n_tasks": len(out["tasks"]),
        "outputs_expected": sum(x["outputs_expected"] for x in out["tasks"]),
        "reads_per_form": len(GLEX_READS), "bar": "2/2 distinct new extractors; any dissent rejects for good",
        "lexicon_drops": [{k: r[k] for k in ("qid", "j", "text", "reasons")} for r in drops],
        "tasks": out["tasks"]}, ensure_ascii=False, indent=1) + "\n"
    out["files"]["answers/README.txt"] = ("T19 redo3 read answers: one <task_id>.json per task (see ../TASKS.json). "
                                          "Written only by the task agents.\n")
    return out


def write(res: dict) -> list:
    clash = [rel for rel, text in res["files"].items()
             if (XROOT / rel).exists() and (XROOT / rel).read_text(encoding="utf-8") != text]
    if clash:
        raise SystemExit(f"files already exist with other content (written once): {clash[:5]}")
    return [str(p) for p in paths.write_files(XROOT, res["files"])]


def summary(res: dict) -> dict:
    rows = res["lint"]
    return {"answer_problems": res["answer_problems"],
            "candidates": len(rows), "lint_clean": sum(r["ok"] for r in rows),
            "lint_dropped": [{k: r[k] for k in ("qid", "j", "text", "reasons")} for r in rows if not r["ok"]],
            "lexicon_drops": [{k: r[k] for k in ("qid", "j", "reasons")} for r in res["lex_drops"]],
            "forms_to_read": len(res["fid_of"]),
            "reads": [{"label": g["label"], "extractor_id": g["extractor_id"], "batch": g["batch"].batch_id,
                       "chunks": len(g["batch"].chunks)} for g in res["reads"]],
            "tasks": [{k: x[k] for k in ("task_id", "extractor_id", "n_items", "task_file", "answer_file")}
                      for x in res["tasks"]]}


def main(argv=None) -> int:
    cmd = (argv or sys.argv[1:] or ["lint"])[0]
    res = build()
    if cmd in ("lint", "tasks"):
        print(json.dumps(summary(res), indent=1, ensure_ascii=False))
        return 0 if not res["answer_problems"] else 1
    if cmd == "write":
        if res["answer_problems"]:
            raise SystemExit(f"answer problems, no read is built: {res['answer_problems']}")
        for p in write(res):
            print(p)
        return 0
    raise SystemExit("usage: redo3_reads.py lint|tasks|write")


if __name__ == "__main__":
    sys.exit(main())
