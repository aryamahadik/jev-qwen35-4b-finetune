"""families/T12/freeze_v2.py: T12 pool freeze-v2 (G0_SPEC.md v2.1 section 2; C2_DATA_SPEC 6.2 item 2, 6.3, 6.4 steps 3-4).

Why this file exists. freeze-v1 (pools/, pool_freeze.py) reads only haiku/author/answers and haiku/extract/answers, and
`pool_freeze.py freeze` rewrites pools/. The count-percent comparator redo (haiku/redo2: one author task and two G-LEX
reads, build_redo2.py) therefore has no ingest path: build_redo2.py only plans, lints and dry-runs ("The pool re-freeze
reads plan/admit_r2.json; it is not done here"). This script is that re-freeze. It changes nothing that exists: v1
(pools/), every answer file, every plan file and all pinned code stay byte for byte as they are; it writes only
pools_v2/.

  check    in memory only: validate every answer file of every round, rebuild v1, merge the redo2 pieces, record every
           G-LEX and G3-H vote, apply every gate, and print the status (READY or SHORT) and every shortfall. Writes
           nothing.
  freeze   the same, then write families/T12/pools_v2/ (the nine pool files, MANIFEST.json, VALIDATION_REPORT.json)
           through paths.write_files. Refuses when pools_v2/MANIFEST.json already exists and when a blocking problem
           exists (v1 not reproduced, a v1 input invalid, a rebuild mismatch).

Run from lean/c2_build:
  ../.venv/bin/python -B families/T12/freeze_v2.py check|freeze  [--exclude-task <task id>]...
  --exclude-task: a task id whose file-access audit failed; that answer file is ignored whole (the orchestrator's
  ignore list; empty for this round).

What it does, in order (no label is set anywhere; Haiku answers only flag):
  1. Contract check of EVERY answer file of every round (v1 author, v1 extract, redo2 author, redo2 extract; there is no
     round-1 redo for T12, and any other haiku/redo* directory is a blocker, never silently skipped). A file is valid
     only when it is UTF-8 JSON (no duplicate key), a list of objects with exactly the contract keys (qid + pack |
     texts | meaning | clerk + dept), every qid in the task's own chunk, none repeated, every item answered once, a
     texts list of exactly the asked length with string entries, a G-LEX meaning copied exactly from the item's choices,
     and the task, chunk, prompt, key and manifest files on disk equal to the rebuilt task. An invalid file is
     rejected whole and never edited; its pieces and votes are not used.
  2. v1 is rebuilt in memory (pool_freeze.build) and must reproduce the frozen pools/ files (bytes and the sha256s of
     pools/manifest.json), every v1 extract answer sha and the record/ shas. The v1 pieces carry over unchanged.
  3. The redo2 author answer goes through the SAME lint, dedup and unit-test rules as build_redo2.py lint (authoring.
     check_comparator, the v2.1 count-percent rules, dedup against every v1 text, unit tests inside the combined v1
     registry).
  4. G-LEX: a fresh registry holds every v1 form and every redo2 form that passed step 3, with NO votes. Votes are then
     recorded from the valid read files only: the v1 reads first, the redo2 reads after (they also re-read the v1
     count form, so it gets 4 reads and any dissent rejects it). Admission is the kit rule
     (lexicon.LexiconRegistry.status): unit test passes and 2 distinct extractors (3 for precedence and window) all
     pick the declared sem; one other pick rejects for good. A form with fewer reads stays pending and is never used.
  5. G3-H: every Mode F note is compared with its facts (g3h.compare), one template per note (as in freeze-v1), template
     report at 98%; a note with no valid read is dropped as unanswered.
  6. The G0 targets of pool_freeze.G0_TARGETS (imported, never lowered) are applied to the merged pool, plus the plugin
     checks that matter for the redo: 500 sampled specs raise no ContractError, and every admitted count-percent form
     renders and parses back through the price condition for every percent value.

READY means: every G0 minimum met, the G-LEX gate passes on every form the pool uses, every G3-H note kept passes, the
plugin checks pass, and no blocking problem. Otherwise SHORT, with the exact shortfalls. G13-seed (6.4 step 4) and row
generation are not run here.

How the generator loads pools_v2. Nothing in the family code (plugin.py, solver_b.py, authoring.py) reads a pool path, so
there is no path to refresh: T12Plugin takes its lexicon as the constructor argument and reads its packs from the module
constant plugin.PACKS. pool_freeze.POOLS still names pools/ and only guards freeze-v1. g13_c2.py reads
families/<F>/pools/ (it is an existing c_build-side file and is not edited here). To use pools_v2 either
  (a) from families.T12 import freeze_v2 as FZ
      pools = FZ.load_pools()                    # Skin objects, a LexiconRegistry of the ADMITTED forms, packs
      ctx = FZ.make_ctx(pools)                   # KitCtx shaped like fixtures.ctx()
      with FZ.packs_installed(pools):            # sets plugin.PACKS for the block
          plugin = P.T12Plugin(lexicon=ctx.lexicon)
          ... pipeline.build_unit(plugin, plugin.sample(seed, sampler), ctx) ...
  (b) promote by directory move once the owner rules it: pools/ -> pools_v1/, pools_v2/ -> pools/ (then g13_c2 sees it).
Keep v1 untouched until then.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True       # importing build_redo2 and the kit must not leave __pycache__ files behind

import argparse
import contextlib
import hashlib
import importlib.util
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker as CH  # noqa: E402
from c2_kit import g3h  # noqa: E402
from c2_kit import lexicon as L  # noqa: E402
from c2_kit import paths  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.plugin import ContractError, KitCtx  # noqa: E402
from families.T12 import authoring as A  # noqa: E402
from families.T12 import extract_build as EB  # noqa: E402
from families.T12 import extract_record as XR  # noqa: E402
from families.T12 import plugin as P  # noqa: E402
from families.T12 import pool_freeze as PF  # noqa: E402
from families.T12 import solver_b as SB  # noqa: E402

F = "T12"
VERSION = "freeze-v2"
POOLS_V1 = PF.POOLS
POOLS_V2 = HERE / "pools_v2"
HAIKU = HERE / "haiku"
G0 = HERE / "G0_SPEC.md"
G0_TARGETS = PF.G0_TARGETS                    # the v1 targets, imported and never changed
LEX_POOLS = PF.LEX_POOLS                      # wordings, comparators, precedence
ITEM_POOLS = ("packs", "skins", "attacks", "documents", "wordings", "comparators", "precedence")
KNOWN_ROUNDS = ("redo2",)                     # haiku/redo2 is the only redo round T12 has
CONTRACT_KEYS = {"author_pack": ("pack",), "author_skin": ("texts",), "author_wording": ("texts",),
                 "author_freeform": ("texts",), "author_lexicon": ("texts",), "extract_lex": ("meaning",),
                 "extract_g3h": ("clerk", "dept")}
PCT_VALUES = (1, 3, 5, 2, 4)                  # training and S5 percent tolerances (G0 R5)
DRY_SEEDS = 100                               # x 5 samplers = 500 specs for the plugin dry run


# ------------------------------------------------------------------------------------------------ small helpers
def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: Path) -> str:
    return sha_bytes(Path(p).read_bytes())


def rel(p) -> str:
    p = Path(p).resolve()
    try:
        return p.relative_to(C2_BUILD).as_posix()
    except ValueError:
        return str(p)


def dump(obj) -> str:
    """The text paths.write_json writes (so a hash can be taken before anything is written)."""
    return json.dumps(obj, ensure_ascii=False, indent=1) + "\n"


def _no_dup_pairs(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise ValueError(f"duplicate JSON key {k!r}")
        out[k] = v
    return out


def _build_redo2():
    """haiku/redo2/build_redo2.py as a module (it is a script, not a package member)."""
    spec = importlib.util.spec_from_file_location("t12_build_redo2", HAIKU / "redo2" / "build_redo2.py")
    br = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(br)
    return br


# ------------------------------------------------------------------------------------------------ answer contract
def _value_problems(kind: str, qid: str, a: dict, item: dict, per: int | None) -> list:
    if kind == "author_pack":
        return [] if isinstance(a["pack"], dict) else [f"{qid}: pack is not an object"]
    if kind in ("author_skin", "author_wording", "author_freeform", "author_lexicon"):
        t = a["texts"]
        if not isinstance(t, list):
            return [f"{qid}: texts is not a list"]
        if per is not None and len(t) != per:
            return [f"{qid}: {len(t)} texts, {per} asked"]
        if not all(isinstance(x, str) for x in t):
            return [f"{qid}: a text is not a string"]
        return []
    if kind == "extract_lex":
        m = a["meaning"]
        if not isinstance(m, str):
            return [f"{qid}: meaning is not a string"]
        if m not in item.get("choices", ()):
            return [f"{qid}: meaning is not one of the item's choices (copied exactly)"]
        return []
    if kind == "extract_g3h":
        return [f"{qid}: {k} is not text" for k in ("clerk", "dept") if not isinstance(a[k], str)]
    return [f"{qid}: unknown task kind {kind}"]


def validate_answer(kind: str, data: bytes, items: dict, per: int | None = None) -> tuple:
    """(answers {qid: object without qid} or None, problems). items: {qid: item} the file must answer, once each.
    The whole file is rejected on any problem: nothing is repaired or partly used."""
    if kind not in CONTRACT_KEYS:
        return None, [f"unknown task kind {kind!r}"]
    try:
        obj = json.loads(data.decode("utf-8"), object_pairs_hook=_no_dup_pairs)
    except (UnicodeDecodeError, ValueError) as e:
        return None, [f"not valid UTF-8 JSON ({str(e)[:90]})"]
    if not isinstance(obj, list):
        return None, ["the top level is not a JSON list"]
    want = {"qid", *CONTRACT_KEYS[kind]}
    out, probs = {}, []
    for i, a in enumerate(obj):
        if not isinstance(a, dict):
            probs.append(f"entry {i} is not an object")
            continue
        if set(a) != want:
            probs.append(f"entry {i}: keys {sorted(a)} != {sorted(want)}")
            continue
        qid = a["qid"]
        if not isinstance(qid, str) or qid not in items:
            probs.append(f"entry {i}: qid {qid!r} is not in this task's chunk")
            continue
        if qid in out:
            probs.append(f"qid {qid} answered twice")
            continue
        probs += _value_problems(kind, qid, a, items[qid], per)
        out[qid] = {k: v for k, v in a.items() if k != "qid"}
    missing = len(set(items) - set(out))
    if missing:
        probs.append(f"{missing} item(s) unanswered")
    return (None if probs else out), probs


def files_differ(root: Path, files: dict, skip: tuple = ()) -> list:
    """Relative paths whose bytes on disk differ from the rebuilt text (the agent answered another task)."""
    return [r for r, text in sorted(files.items())
            if r not in skip and (not (Path(root) / r).is_file() or (Path(root) / r).read_text(encoding="utf-8") != text)]


def read_answer_file(rnd: str, kind: str, task_id: str, path: Path, items: dict, excluded: set, per: int | None = None,
                     task_diff: list | None = None) -> tuple:
    """(answers or None, record). The record is what VALIDATION_REPORT.json lists for the file."""
    path = Path(path)
    rec = {"round": rnd, "task_id": task_id, "kind": kind, "file": rel(path), "sha256": None,
           "n_expected": len(items), "n_answered": 0, "status": "valid", "problems": []}
    if task_id in excluded:
        rec.update(status="excluded", problems=["file-access audit failed: answers ignored"])
        if path.is_file():
            rec["sha256"] = sha_file(path)
        return None, rec
    if not path.is_file():
        rec.update(status="missing", problems=["answer file missing (task not answered)"])
        return None, rec
    data = path.read_bytes()
    rec["sha256"] = sha_bytes(data)
    ans, probs = validate_answer(kind, data, items, per)
    if task_diff:
        probs = probs + [f"task file {x} on disk differs from the rebuilt task" for x in task_diff[:3]]
        ans = None
    if ans is None:
        rec.update(status="invalid", problems=probs)
        return None, rec
    rec["n_answered"] = len(ans)
    return ans, rec


def _items_of(batch: CH.TaskBatch, tid: str) -> dict:
    return {it["qid"]: it for c in batch.chunks if c["task_id"] == tid for it in c["items"]}


# ------------------------------------------------------------------------------------------------ pool files
def pool_file_objs(items: dict, lex_adm: dict, quar: list) -> dict:
    """{file name: object} exactly as pool_freeze.freeze writes them (the nine pool files)."""
    out = {}
    for stem, rows in sorted(items.items()):
        out[f"{stem}.json"] = {"family": PF.FAMILY, "pool": stem, "g0_sha256": P.G0_SHA256_AUTHORED,
                               "n": len(rows), "items": rows}
    out["lexicon.json"] = lex_adm
    out["quarantine.json"] = {"family": PF.FAMILY, "n": len(quar), "items": quar}
    return out


def pool_file_texts(items: dict, lex_adm: dict, quar: list) -> dict:
    return {name: dump(obj) for name, obj in pool_file_objs(items, lex_adm, quar).items()}


def v1_integrity(b1: dict, out1: dict) -> dict:
    """The v1 rebuild reproduces the frozen pools/ (bytes, manifest sha256s, answer shas, record shas)."""
    probs = []
    man_path = POOLS_V1 / "manifest.json"
    man = json.loads(man_path.read_text(encoding="utf-8"))
    texts = pool_file_texts(b1["items"], b1["lex_adm"], b1["quar"])
    for name, text in texts.items():
        disk = POOLS_V1 / name
        if not disk.is_file():
            probs.append(f"pools/{name} is missing")
        elif disk.read_text(encoding="utf-8") != text:
            probs.append(f"pools/{name}: the rebuild differs from the frozen file")
        if man["pool_files"].get(name, {}).get("sha256") != sha_bytes(text.encode("utf-8")):
            probs.append(f"pools/{name}: sha256 differs from pools/manifest.json")
    on_disk = {p.name for p in POOLS_V1.glob("*.json")}
    if on_disk != set(texts) | {"manifest.json"}:
        probs.append(f"pools/ holds {sorted(on_disk ^ (set(texts) | {'manifest.json'}))} unexpectedly or lacks them")
    if man["admitted_counts"] != {k: len(v) for k, v in b1["items"].items()}:
        probs.append("admitted counts differ from pools/manifest.json")
    if json.loads(json.dumps(b1["shortfalls"])) != man["shortfalls"]:
        probs.append("the v1 shortfall rows differ from pools/manifest.json")
    for name, sha in man["extraction_answers"]["sha256"].items():
        p = EB.EXTRACT / "answers" / name
        if not p.is_file() or sha_file(p) != sha:
            probs.append(f"v1 extraction answer {name} changed since freeze-v1")
    for name, sha in man["record"].items():
        p = EB.EXTRACT / name
        if not p.is_file() or sha_file(p) != sha:
            probs.append(f"haiku/extract/{name} changed since freeze-v1")
    if man["g0_sha256"] != P.G0_SHA256_AUTHORED or sha_file(G0) != P.G0_SHA256_AUTHORED:
        probs.append("G0_SPEC.md sha256 differs from the plugin pin or from freeze-v1")
    if out1["files"]["problems"]:
        probs += [f"v1 extract task: {x}" for x in out1["files"]["problems"][:3]]
    return {"ok": not probs, "problems": probs, "version": man["version"], "manifest_sha256": sha_file(man_path)}


def targets_unchanged() -> list:
    """Problems if a G0 target differs from the one freeze-v1 recorded in its manifest (no target is lowered)."""
    man = json.loads((POOLS_V1 / "manifest.json").read_text(encoding="utf-8"))
    v1 = {(r["pool"], r["metric"]): (r["target"], r["op"]) for r in man["shortfalls"] if r["target"] is not None}
    mine = {(t["pool"], t["metric"]): (t["target"], t["op"]) for t in G0_TARGETS}
    probs = []
    for k, v in v1.items():
        if k in mine and mine[k] != v:
            probs.append(f"target {k} is {mine[k]}, freeze-v1 recorded {v}")
    return probs


# ------------------------------------------------------------------------------------------------ redo2 lint (build_redo2)
def lint_redo2(br, rb: CH.TaskBatch, got: dict, answer_sha: str) -> dict:
    """build_redo2.run_lint on an already validated author answer (got: {internal id: {"texts": [...]}})."""
    pieces, kept = br.lint_pieces(rb, got)
    base = json.loads(br.PENDING_LEX.read_text(encoding="utf-8"))
    kept, unit_drops = br.combined_unit(kept, base)
    drop = {p["pid"]: p for p in unit_drops}
    for p in pieces:
        if p["pid"] in drop:
            p.update(problems=drop[p["pid"]]["problems"], stage="unit")
    for p in kept:
        p["form_id"] = EB._fid(p["sem"], p["text"])
    by = Counter((p["sem"], p["stage"] or "kept") for p in pieces)
    return {"family": F, "stage": "redo2-a lint", "task_id": rb.chunks[0]["task_id"], "answer_sha256": answer_sha,
            "g0_sha256": P.G0_SHA256_AUTHORED,
            "counts": {f"{s}/{k}": v for (s, k), v in sorted(by.items())},
            "kept": [{k: p[k] for k in ("pid", "sem", "text", "form_id", "task_id", "prompt_sha")} for p in kept],
            "pieces": pieces}


def redo_extract_files(br, b: CH.TaskBatch) -> dict:
    """The files of one redo2 G-LEX read batch as build_redo2.extract_files writes them (prompt, chunks, key, manifest,
    task files); the agent answered exactly these."""
    files = dict(b.files())
    for c in b.chunks:
        tid = c["task_id"]
        files[f"tasks/{tid}.md"] = EB.task_markdown("extract_lex", b, c, br.EXTRACT / b.answer_path(tid)).replace(
            "# T12 extraction task", "# T12 REDO-2 extraction task", 1)
    return files


def redo_piece(p: dict, held: bool = False) -> dict:
    """A lint piece of the redo2 author task as the piece dict pool_freeze works on."""
    return {"typ": "cmp", "pool": "comparators", "pid": p["pid"], "iid": p["pid"].rsplit("|", 1)[0], "held": held,
            "tid": p.get("task_id"), "prompt_sha": p.get("prompt_sha"), "value": p["text"], "text": p["text"],
            "item": None, "problems": list(p["problems"])}


# ------------------------------------------------------------------------------------------------ registry and votes
def build_registry_v2(reg1, redo_kept: list, br):
    """A fresh T12 registry: every v1 form WITHOUT its votes, plus the kept redo2 forms; unit tests run."""
    j = reg1.to_json()
    reg = L.LexiconRegistry(F)
    for s in j["sems"]:
        reg.declare(s["sem_id"], s["kind"], s["meaning"])
    for x in j["forms"]:
        f = reg.add(x["text"], x["sem_id"], slots=x["slots"], source=x["source"], family=x["family"],
                    haiku_task_id=x["haiku_task_id"], haiku_prompt_sha=x["haiku_prompt_sha"], held_out=x["held_out"])
        if f.form_id != x["form_id"]:
            raise SystemExit(f"form id drift {x['form_id']} -> {f.form_id}")
    for a, b in j["antonyms"]:
        reg.declare_antonym(a, b)
    for p in redo_kept:
        f = br._add(reg, p)
        if f.form_id != p["form_id"]:
            raise SystemExit(f"form id drift {p['form_id']} -> {f.form_id}")
    reg.unit_test_all()
    return reg


def record_votes(reg, batch: CH.TaskBatch, answers: dict, problems: list, label: str) -> Counter:
    """reg.record_extraction for every answered item of one G-LEX read batch. answers: {task_id: {qid: {"meaning"}}}
    from the VALID files only; extractor id = the task id (one task per chunk), so reads are independent."""
    c = Counter()
    for chunk in batch.chunks:
        tid = chunk["task_id"]
        if tid not in answers:
            c["task_without_valid_answer"] += 1
            continue
        for it in chunk["items"]:
            qid = it["qid"]
            fid = batch.key[qid]
            if fid not in reg.forms:
                problems.append(f"{label}: form {fid} is not in the registry (read ignored)")
                continue
            if qid not in answers[tid]:
                continue
            f = reg.forms[fid]
            meaning = answers[tid][qid]["meaning"]
            sem = reg.meaning_to_sem(f.kind, meaning)
            c["agrees" if sem == f.sem_id else "other_meaning"] += 1
            try:
                reg.record_extraction(fid, tid, sem)
            except L.LexiconError as e:
                problems.append(f"{label}: {str(e)[:100]}")
    return c


def g3h_results(res1: dict, answers: dict) -> tuple:
    """(template report, per-note detail). One template per note (a Mode F note is its own skin, as in freeze-v1).
    answers: {task_id: {qid: {"clerk", "dept"}}} from the valid files only; a note with no valid read is unanswered."""
    fields = EB.g3h_fields()
    b = res1["g3h"]
    by_iid = {}
    for chunk in b.chunks:
        if chunk["task_id"] in answers:
            for it in chunk["items"]:
                if it["qid"] in answers[chunk["task_id"]]:
                    by_iid[b.key[it["qid"]]] = answers[chunk["task_id"]][it["qid"]]
    results, detail = [], {}
    for iid in sorted(res1["g3h_expected"]):
        if iid not in by_iid:
            ok, diffs = False, ["unanswered"]
        else:
            ok, diffs = g3h.compare(res1["g3h_expected"][iid], by_iid[iid], fields)
        results.append((iid, iid, ok))
        detail[iid] = {"ok": ok, "diffs": diffs}
    return g3h.template_report(results), detail


# ------------------------------------------------------------------------------------------------ plugin checks
def plugin_checks(reg) -> dict:
    """What the redo exists for: the plugin samples percent cards without a ContractError, and every admitted count
    form renders into the price condition and parses back to its own sem and value (build_redo2.admit's checks)."""
    plugin = P.T12Plugin(lexicon=reg)
    errs, n_pct, used = Counter(), 0, Counter()
    for seed in range(DRY_SEEDS):
        for smp in ("S1", "S2", "S3", "S4", "S5"):
            try:
                sp = plugin.sample(seed, smp)
            except ContractError as e:
                errs[str(e)[:80]] += 1
                continue
            if sp.structure.get("tol_kind") == "pct":
                n_pct += 1
                used[sp.slots["TOL_CMP"].value[1]] += 1
    trip, n_forms = [], 0
    for fid, f in sorted(reg.forms.items()):
        if f.kind != "comparator" or dict(f.slots).get("X") != "count" or reg.status(fid) != "admitted":
            continue
        n_forms += 1
        for v in PCT_VALUES:
            clause = f.text.replace("{X}", S.render(S.count_slot(v, P.U_PCT)))
            cond = P.COND_TPL["price_pct"].replace("{TOL_CMP}", clause)
            m = SB.COND_PCT_RE.fullmatch(cond)
            try:
                got = reg.parse_exact(m["c"], {"X": SB.PERCENT}, admitted_only=True) if m else None
            except L.LexiconError as e:
                got = str(e)
            if not (isinstance(got, tuple) and got[0] == f.sem_id and got[2] == {"X": v}):
                trip.append({"form_id": fid, "value": v, "condition": cond, "parsed": str(got)})
    return {"specs": DRY_SEEDS * 5, "contract_errors": dict(errs), "percent_cards": n_pct,
            "tol_forms_used": len(used), "count_forms_round_tripped": n_forms,
            "percent_values": list(PCT_VALUES), "round_trip_failures": trip,
            "pass": not errs and not trip and n_forms > 0}


# ------------------------------------------------------------------------------------------------ assemble
def assemble(exclude: tuple = (), v1: dict | None = None) -> dict:
    """Everything in memory. v1: a pool_freeze.build() result to reuse (tests). Nothing is written."""
    excluded = set(exclude)
    blockers, notes = [], []
    br = _build_redo2()
    b1 = v1 if v1 is not None else PF.build()
    out1 = b1["out"]
    res1 = out1["res"]
    integrity = v1_integrity(b1, out1)
    if not integrity["ok"]:
        blockers.append("freeze-v1 is not reproduced: " + "; ".join(integrity["problems"][:3]))
    blockers += targets_unchanged()

    # --- round directories (nothing is silently skipped)
    rounds = sorted(p.name for p in HAIKU.glob("redo*") if p.is_dir())
    unknown_rounds = [r for r in rounds if r not in KNOWN_ROUNDS]
    if unknown_rounds:
        blockers.append(f"haiku/{unknown_rounds} exist but this script does not ingest them")

    records, ans_by_task = [], {}

    def take(rec, ans):
        records.append(rec)
        if ans is not None:
            ans_by_task[rec["task_id"]] = ans
        return ans

    # --- 1. contract: v1 author answers (A.build rebuilds the tasks the agents answered)
    for label, pool, held, per, b in A.build():
        tid = b.chunks[0]["task_id"]
        files = dict(b.files())
        files[f"tasks/{tid}.md"] = A.task_markdown(b, b.chunks[0], A.answer_path(A.ROOT, b, tid), per)
        ans, rec = read_answer_file("v1", b.kind, tid, A.answer_path(A.ROOT, b, tid), _items_of(b, tid), excluded, per,
                                    files_differ(A.ROOT, files))
        rec.update(label=label, pool=pool, held_out=held)
        take(rec, ans)
        if rec["status"] != "valid":
            blockers.append(f"v1 author answer {tid} ({label}) is {rec['status']}: pools cannot be reproduced")
    # --- 1b. contract: v1 extract answers (G-LEX reads and the G3-H read; their files were checked by XR.check_files)
    for group, read, b in XR.batches(res1):
        for c in b.chunks:
            tid = c["task_id"]
            ans, rec = read_answer_file("v1", b.kind, tid, EB.EXTRACT / b.answer_path(tid), _items_of(b, tid), excluded)
            rec.update(label=f"{group}-r{read}", pool=group, held_out=False)
            take(rec, ans)
            if rec["status"] in ("invalid", "missing"):
                blockers.append(f"v1 extract answer {tid} ({group}-r{read}) is {rec['status']}")
            elif rec["status"] == "excluded":
                notes.append(f"v1 extract answer {tid} ({group}-r{read}) is excluded (audit failed): its votes are "
                             "not counted")

    # --- 1c. contract: redo2 author answer, then (if usable) its two G-LEX reads
    rb = br.author_batch()
    rtid = rb.chunks[0]["task_id"]
    a_files, _row = br.author_files(rb)
    ans, rec = read_answer_file("redo2", rb.kind, rtid, br.AUTHOR / rb.answer_path(rtid), _items_of(rb, rtid), excluded,
                                br.N_PER, files_differ(br.AUTHOR, a_files))
    rec.update(label="lex-cmp-count", pool="comparators", held_out=False)
    take(rec, ans)
    lint, redo_batches = None, []
    if ans is not None:
        got = {rb.key[q]: x for q, x in ans.items()}
        lint = lint_redo2(br, rb, got, rec["sha256"])
        redo_batches = br.glex_batches(lint)
        for r, b in redo_batches:
            diff = files_differ(br.EXTRACT, redo_extract_files(br, b), skip=("answers/README.txt",))
            for c in b.chunks:
                tid = c["task_id"]
                a2, rec2 = read_answer_file("redo2", b.kind, tid, br.EXTRACT / b.answer_path(tid), _items_of(b, tid),
                                            excluded, None, diff)
                rec2.update(label=f"comparator-count-r{r}", pool="comparators", held_out=False)
                take(rec2, a2)
                if rec2["status"] != "valid":
                    notes.append(f"redo2 G-LEX read {tid} is {rec2['status']}: its forms keep fewer than 2 reads")
    else:
        notes.append(f"the redo2 author answer is {rec['status']}: no redo2 form exists, so its G-LEX reads are not used")
        chunk_dir = br.EXTRACT / "chunks"
        for p in sorted(chunk_dir.glob("*.json")) if chunk_dir.is_dir() else []:
            ch = json.loads(p.read_text(encoding="utf-8"))
            tid = ch["task_id"]
            _a, rec2 = read_answer_file("redo2", "extract_lex", tid, br.EXTRACT / "answers" / f"{tid}.json",
                                        {it["qid"]: it for it in ch["items"]}, excluded)
            rec2.update(label="comparator-count (unused)", pool="comparators", held_out=False, status="unused")
            records.append(rec2)

    # --- stray answer files (listed, never used)
    known = {Path(r["file"]).name for r in records}
    stray = []
    for d in (A.ROOT / "answers", EB.EXTRACT / "answers", br.AUTHOR / "answers", br.EXTRACT / "answers"):
        for p in sorted(d.glob("*.json")) if d.is_dir() else []:
            if p.name not in known:
                stray.append(rel(p))

    # --- 2/3. redo2 pieces: lint, dedup and unit-test results become pieces of the merged pool
    redo_pieces = [redo_piece(p) for p in (lint["pieces"] if lint else [])]
    redo_kept = [p for p in redo_pieces if not p["problems"]]
    stage_of = {p["pid"]: p["stage"] for p in (lint["pieces"] if lint else [])}
    redo_dups = [p for p in redo_pieces if p["problems"] and stage_of[p["pid"]] == "dedup"]
    redo_dropped = [p for p in redo_pieces if p["problems"] and stage_of[p["pid"]] != "dedup"]
    kept_lint = lint["kept"] if lint else []

    # --- 4. G-LEX: fresh registry, no votes, then the valid reads in order (v1 first, redo2 after)
    reg2 = build_registry_v2(res1["reg"], kept_lint, br)
    vote_problems, vote_counts = [], {}
    for group, read, b in XR.batches(res1):
        if group == "g3h":
            continue
        valid = {c["task_id"]: ans_by_task[c["task_id"]] for c in b.chunks if c["task_id"] in ans_by_task}
        vote_counts[f"v1:{group}-r{read}"] = dict(record_votes(reg2, b, valid, vote_problems, f"v1 {group}-r{read}"))
    for r, b in redo_batches:
        valid = {c["task_id"]: ans_by_task[c["task_id"]] for c in b.chunks if c["task_id"] in ans_by_task}
        vote_counts[f"redo2:comparator-count-r{r}"] = dict(record_votes(reg2, b, valid, vote_problems,
                                                                        f"redo2 r{r}"))
    notes += [f"vote: {x}" for x in vote_problems]
    if vote_problems:
        blockers.append(f"{len(vote_problems)} G-LEX vote problem(s): {vote_problems[0]}")

    # --- 5. G3-H from the valid v1 read files
    g_tasks = {c["task_id"] for c in res1["g3h"].chunks}
    g_rep, g_detail = g3h_results(res1, {t: x for t, x in ans_by_task.items() if t in g_tasks})
    if not excluded and g_detail != out1["g3h_detail"]:
        blockers.append("G3-H recomputed from the validated answers differs from the freeze-v1 record")

    # --- merged pool: v1 pieces unchanged, redo2 comparator pieces appended
    task_redo = {"task": "lex-cmp-count (redo2)", "task_id": rtid, "pool": "comparators", "held_out": False,
                 "pieces": len(lint["pieces"]) if lint else 0, "task_problems": [] if lint else list(rec["problems"])}
    res2 = dict(res1)
    res2.update(reg=reg2, kept=list(res1["kept"]) + redo_kept, dropped=list(res1["dropped"]) + redo_dropped,
                dups=list(res1["dups"]) + redo_dups, tasks=list(res1["tasks"]) + [task_redo])
    out2 = {"res": res2, "g3h_detail": g_detail, "g3h_rep": g_rep, "loaded": out1["loaded"], "files": out1["files"]}
    adm2, quar2 = PF.piece_status(out2)
    items2 = PF.pool_items(out2, adm2)
    tasks2 = PF.task_table(out2, adm2)
    short_rows = PF.shortfalls(items2, tasks2, out2)
    lex_adm2 = PF.lexicon_admitted(reg2)

    # --- carry-over proof: nothing of v1 changed except what a re-read rejected
    carry = {}
    for stem in ITEM_POOLS:
        v1_rows, v2_rows = b1["items"][stem], items2[stem]
        if stem == "comparators":
            v2_v1 = [r for r in v2_rows if r["pid"] in {x["pid"] for x in v1_rows}]
            dropped_v1 = [x["pid"] for x in v1_rows if x["pid"] not in {r["pid"] for r in v2_rows}]
            carry[stem] = {"v1_items_kept_unchanged_in_order": v2_v1 == [x for x in v1_rows if x["pid"] not in dropped_v1],
                           "v1_items_dropped_by_reread": dropped_v1, "added": len(v2_rows) - len(v2_v1)}
        else:
            carry[stem] = {"identical_to_v1": json.dumps(v1_rows, sort_keys=True) == json.dumps(v2_rows, sort_keys=True)}
    for stem, c in carry.items():
        if not (c.get("identical_to_v1") or c.get("v1_items_kept_unchanged_in_order")):
            blockers.append(f"pool {stem}: v1 pieces were changed by the merge")

    # --- gates
    used_forms = sorted(r["form_id"] for pool in LEX_POOLS for r in items2.get(pool, []))
    glex_used = reg2.gate(used_forms)
    wrong_sem = [r["form_id"] for r in items2["wordings"]
                 if r["sem_id"] != L.question_sem(F, r["qform"]) or reg2.forms[r["form_id"]].sem_id != r["sem_id"]]
    kind_count = {}
    for fid, f in reg2.forms.items():
        kind_count.setdefault(f.kind, Counter())[reg2.status(fid)] += 1
    plug = plugin_checks(reg2)
    contract = {"files": len(records), "valid": sum(1 for r in records if r["status"] == "valid"),
                "not_valid": [{"task_id": r["task_id"], "round": r["round"], "status": r["status"]}
                              for r in records if r["status"] != "valid"]}
    g3h_gate = {"gate": "G3-H", "bar": g3h.PASS_RATE, "template": "one note = one template (as freeze-v1)",
                "notes": len(g_detail), "notes_ok": sum(1 for d in g_detail.values() if d["ok"]),
                "quarantined": sorted(g_rep["quarantined"]),
                "kept_notes_all_pass": all(g_detail[f"g3h|{p['pid']}"]["ok"] for p in adm2.get("freeform", [])),
                "aggregate_rate": round(100.0 * sum(1 for d in g_detail.values() if d["ok"]) / max(1, len(g_detail)), 2),
                "by_register_info_only": PF._g3h_by_register({"g3h_detail": g_detail})}
    gates = {"G-LEX": {"used_forms": len(used_forms), "pass": glex_used["pass"] and not wrong_sem,
                       "not_admitted": glex_used["not_admitted"], "unknown": glex_used["unknown"],
                       "wording_sem_mismatch": wrong_sem,
                       "registry_status_by_kind": {k: dict(sorted(v.items())) for k, v in sorted(kind_count.items())},
                       "rule": "unit test + 2/2 independent reads (3/3 precedence and window); one other pick rejects"},
             "G3-H": g3h_gate, "plugin": plug, "contract": contract}

    short = [f"{r['pool']}: {r['metric']}: value {r['value']}, target {r['op']} {r['target']}"
             for r in short_rows if r["met"] is False]
    if not gates["G-LEX"]["pass"]:
        short.append("G-LEX: a form the pool uses is not admitted")
    if not g3h_gate["kept_notes_all_pass"]:
        short.append("G3-H: a kept note does not pass")
    if not plug["pass"]:
        short.append(f"plugin checks fail: contract errors {plug['contract_errors']}, "
                     f"round-trip failures {len(plug['round_trip_failures'])}")
    ready = not blockers and not short
    return {"b1": b1, "out1": out1, "out2": out2, "reg2": reg2, "integrity": integrity, "records": records,
            "stray": stray, "unknown_rounds": unknown_rounds, "lint": lint, "redo_pieces": redo_pieces,
            "redo_batches": redo_batches, "items": items2, "adm": adm2, "quar": quar2, "tasks": tasks2,
            "short_rows": short_rows, "lex_adm": lex_adm2, "carry": carry, "gates": gates, "votes": vote_counts,
            "short": short, "blockers": blockers, "notes": notes, "ready": ready, "excluded": sorted(excluded),
            "reads": reads_table(reg2, redo_batches, lint)}


def reads_table(reg, redo_batches: list, lint: dict | None) -> dict:
    """Per redo2 form: the reads on record and the status (the provenance of every added comparator)."""
    out = {}
    for p in (lint["kept"] if lint else []):
        f = reg.forms[p["form_id"]]
        out[p["form_id"]] = {"text": f.text, "sem": f.sem_id, "status": reg.status(p["form_id"]),
                             "reads": [list(e) for e in f.extractions]}
    return out


# ------------------------------------------------------------------------------------------------ files
def validation_report(a: dict) -> dict:
    recs = a["records"]
    by = Counter((r["round"], r["status"]) for r in recs)
    return {"family": F, "version": VERSION,
            "contract": "UTF-8 JSON list without duplicate keys; objects with exactly qid + " + " | ".join(
                f"{'+'.join(v)} ({k})" for k, v in CONTRACT_KEYS.items()) +
                        "; qids from the task's own chunk, none repeated, all answered; texts: exactly the asked "
                        "number of strings; G-LEX meaning copied exactly from the item's choices; the rebuilt task, "
                        "chunk, prompt, key and manifest files equal the files on disk",
            "summary": {f"{r}/{s}": n for (r, s), n in sorted(by.items())},
            "files_total": len(recs), "files_valid": sum(1 for r in recs if r["status"] == "valid"),
            "files_not_valid": [r for r in recs if r["status"] != "valid"],
            "excluded_by_orchestrator": a["excluded"],
            "audit": "no file-access audit output or agent transcript exists on disk for any T12 answer (v1 or redo); "
                     "the orchestrator's ignore list of failed audits is " + json.dumps(a["excluded"]),
            "stray_files_not_used": a["stray"], "unrecognised_round_dirs": a["unknown_rounds"], "files": recs}


def manifest_obj(a: dict, files: dict) -> dict:
    items = a["items"]
    qc = Counter(q["stage"] for q in a["quar"])
    g0_sha = sha_file(G0)
    added = [{"form_id": p["form_id"], "text": p["text"], "sem_id": p["sem"], "task_id": p["task_id"],
              "prompt_sha": p["prompt_sha"], "status": a["reads"][p["form_id"]]["status"],
              "reads": a["reads"][p["form_id"]]["reads"]}
             for p in (a["lint"]["kept"] if a["lint"] else [])]
    if a["ready"]:
        status = ("READY: every G0 minimum met and the G-LEX gate passes (every form the pool uses is admitted 2/2, "
                  "3/3 for precedence). G13-seed and row generation not run.")
    elif a["blockers"]:
        status = "BLOCKED: " + "; ".join(a["blockers"][:3])
    else:
        status = "SHORT: " + "; ".join(a["short"]) + ". Targets are not lowered. G13-seed and row generation not run."
    return {
        "family": F, "version": VERSION, "ready": a["ready"], "status": status,
        "supersedes": {"path": "families/T12/pools/manifest.json", "version": a["integrity"]["version"],
                       "sha256": a["integrity"]["manifest_sha256"]},
        "v1_integrity": {"reproduced_by_rebuild": a["integrity"]["ok"], "problems": a["integrity"]["problems"]},
        "how_to_load": ("The family code reads no pool path (T12Plugin(lexicon=...) takes the registry; plugin.PACKS is a "
                        "module constant), so there is no path to refresh. Use families.T12.freeze_v2.load_pools() / "
                        "make_ctx() / packs_installed(), or, after an owner ruling, move pools/ to pools_v1/ and "
                        "pools_v2/ to pools/ (g13_c2.py reads families/T12/pools/). Keep v1 untouched until then."),
        "g0": {"path": "families/T12/G0_SPEC.md", "sha256": g0_sha, "matches_plugin_pin": g0_sha == P.G0_SHA256_AUTHORED,
               "version": "v2.1"},
        "answer_files": {"total": len(a["records"]), "by_round_status": validation_report(a)["summary"],
                         "not_valid": a["gates"]["contract"]["not_valid"], "excluded": a["excluded"],
                         "audit": validation_report(a)["audit"], "detail": "VALIDATION_REPORT.json"},
        "redo2": {"author_task": a["lint"]["task_id"] if a["lint"] else None,
                  "author_answer_sha256": a["lint"]["answer_sha256"] if a["lint"] else None,
                  "lint_counts": a["lint"]["counts"] if a["lint"] else None,
                  "reads": a["votes"], "added_forms": added},
        "gates": a["gates"],
        "counts": {"admitted": {k: len(v) for k, v in items.items()}, "detail": PF.counts(items),
                   "lexicon_forms_admitted": len(a["lex_adm"]["forms"])},
        "targets_g0": G0_TARGETS, "targets_unchanged_vs_v1": not targets_unchanged(),
        "shortfall_rows": a["short_rows"], "shortfalls": a["short"],
        "problems": {"blocking": a["blockers"], "notes": a["notes"]},
        "carry_over_from_v1": a["carry"],
        "quarantined": {"total": len(a["quar"]), "by_stage": dict(sorted(qc.items())), "file": "quarantine.json"},
        "tasks": a["tasks"],
        "no_rows_generated": True, "no_labels_set": True,
        "sha256": {name: sha_bytes(text.encode("utf-8")) for name, text in sorted(files.items())},
        "note_manifest": "sha256 of every other file in pools_v2/ (this file is not hashed)"}


def build_files(a: dict) -> dict:
    files = pool_file_texts(a["items"], a["lex_adm"], a["quar"])
    files["VALIDATION_REPORT.json"] = dump(validation_report(a))
    files["MANIFEST.json"] = dump(manifest_obj(a, files))
    return files


def summary_out(a: dict, files: dict, written: bool) -> dict:
    man = json.loads(files["MANIFEST.json"])
    cover = next((r["value"] for r in a["short_rows"] if r["metric"].startswith("comparator forms cover")), None)
    g3 = {k: v for k, v in a["gates"]["G3-H"].items() if k != "by_register_info_only"}
    return {"status": man["status"], "ready": a["ready"], "written": written, "shortfalls": a["short"],
            "blockers": a["blockers"], "notes": a["notes"], "answer_files": man["answer_files"]["by_round_status"],
            "not_valid_files": man["answer_files"]["not_valid"], "counts": man["counts"]["admitted"],
            "comparator_coverage": cover, "reads_recorded": a["votes"],
            "gates": {"G-LEX": a["gates"]["G-LEX"], "G3-H": g3, "plugin": a["gates"]["plugin"]},
            "v1_reproduced": a["integrity"]["ok"], "quarantine_by_stage": man["quarantined"]["by_stage"],
            "targets_unchanged_vs_v1": man["targets_unchanged_vs_v1"], "files": sorted(files)}


def run(write: bool, exclude: tuple = (), v1: dict | None = None) -> dict:
    if write and (POOLS_V2 / "MANIFEST.json").exists():
        raise SystemExit("pools_v2/MANIFEST.json already exists: refusing to re-freeze")
    a = assemble(exclude=exclude, v1=v1)
    if write and a["blockers"]:
        raise SystemExit("blocking problems, nothing written: " + "; ".join(a["blockers"][:4]))
    files = build_files(a)
    if write:
        paths.write_files(POOLS_V2, files)
    return summary_out(a, files, write)


# ------------------------------------------------------------------------------------------------ loading pools_v2
def _skin_id(pool: str, pid: str) -> str:
    """A stable, unique skin id from the pool piece id: skin|chat|0|CLERK+DEPT|0 -> T12-SK-chat-0-CLERK_DEPT-0."""
    tag = {"skins": "SK", "documents": "MF", "attacks": "AT"}[pool]
    return f"T12-{tag}-" + "-".join(pid.split("|")[1:]).replace("+", "_")


def load_pools(root: Path = POOLS_V2) -> dict:
    """The pool files of a freeze as objects: {"skins"/"documents"/"attacks": {skin id: Skin}, "wordings": [admitted
    wording records], "comparators": [...], "precedence": [...], "packs": [plugin pack dicts], "lexicon": LexiconRegistry
    of the ADMITTED forms (use reg.status / reg.gate), "manifest": dict}. Every skin is re-linted through the authoring
    checks it passed at the pool stage; a failure raises."""
    root = Path(root)

    def j(name):
        return json.loads((root / name).read_text(encoding="utf-8"))
    skins, docs, attacks = {}, {}, {}
    for r in j("skins.json")["items"]:
        sid = _skin_id("skins", r["pid"])
        sk, pr = A.check_skin(r["text"], r["register"], tuple(r["slots"]), held_out=r["held_out"], skin_id=sid,
                              n_probe=0, task_id=r["task_id"], prompt_sha=r["prompt_sha"])
        if pr:
            raise ValueError(f"{r['pid']}: {pr[:2]}")
        skins[sid] = sk
    for r in j("documents.json")["items"]:
        sid = _skin_id("documents", r["pid"])
        sk, pr = A.check_freeform(r["text"], dict(r["facts"]), r["register"], held_out=r["held_out"], skin_id=sid,
                                  n_probe=0, task_id=r["task_id"], prompt_sha=r["prompt_sha"])
        if pr:
            raise ValueError(f"{r['pid']}: {pr[:2]}")
        docs[sid] = sk
    for r in j("attacks.json")["items"]:
        sid = _skin_id("attacks", r["pid"])
        sk, pr = A.check_attack(r["text"], skin_id=sid, n_probe=0, task_id=r["task_id"], prompt_sha=r["prompt_sha"])
        if pr:
            raise ValueError(f"{r['pid']}: {pr[:2]}")
        attacks[sid] = sk
    packs = []
    for r in j("packs.json")["items"]:
        v = dict(r["value"])
        v.update(vendors=tuple(v["vendors"]), items=tuple(tuple(it) for it in v["items"]), clerks=tuple(v["clerks"]),
                 approvers=tuple(v["approvers"]))
        packs.append(v)
    return {"skins": skins, "documents": docs, "attacks": attacks, "wordings": j("wordings.json")["items"],
            "comparators": j("comparators.json")["items"], "precedence": j("precedence.json")["items"], "packs": packs,
            "lexicon": L.LexiconRegistry.from_json(j("lexicon.json")), "manifest": j("MANIFEST.json")}


def make_ctx(pools: dict | None = None) -> KitCtx:
    """The generator's KitCtx for a pool set (default pools_v2/): narrative skins, Mode F notes, pressure lines and one
    wording skin per ADMITTED wording (kind "wording", lexicon_ids = its form id), with the registry that holds only
    admitted forms. Same shape as fixtures.ctx()."""
    pools = pools or load_pools()
    sk = {**pools["skins"], **pools["documents"], **pools["attacks"]}
    for w in pools["wordings"]:
        sid = f"T12-WD-{w['form_id']}"
        sk[sid] = K.make_skin(sid, F, w["text"], {"INVOICE_ID": "id"}, kind="wording", register="question",
                              qform=w["qform"], held_out=w["held_out"], lexicon_ids=(w["form_id"],),
                              haiku_task_id=w["task_id"], haiku_prompt_sha=w["prompt_sha"])
    return KitCtx(skins=sk, lexicon=pools["lexicon"])


@contextlib.contextmanager
def packs_installed(pools: dict | None = None):
    """plugin.PACKS = the pool's packs for the block (the plugin reads its packs from that module constant)."""
    pools = pools or load_pools()
    with A._packs_patched(tuple(pools["packs"])):
        yield


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=("check", "freeze"))
    ap.add_argument("--exclude-task", action="append", default=[], help="a task id whose audit failed (repeatable)")
    a = ap.parse_args(argv)
    out = run(write=(a.cmd == "freeze"), exclude=tuple(a.exclude_task))
    print(json.dumps(out, indent=1, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
