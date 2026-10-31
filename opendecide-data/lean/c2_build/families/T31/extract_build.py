"""families/T31/extract_build.py: the T31 pool-stage lint, dedup and G-LEX extraction tasks (C2_DATA_SPEC 6.3 and 6.4
step 3; G0_SPEC.md section 7).

  check   load the authoring answers (haiku_author.load), lint the packs and names with gsl.lint_values, dedup,
          unit-test every lexicon form, and build the extraction reads in memory. Nothing is written.
  build   the same, then write the reads under haiku/extract/ through paths.write_files (after A38 only), plus the
          drop log and TASKS.json. Refuses to rewrite an existing haiku/extract/.

Run from lean/:  ../.venv/bin/python c2_build/families/T31/extract_build.py check|build

Scope. G-SL (skins, wordings, attack lines, Mode F texts) runs inside haiku_author.load(); this module adds
gsl.lint_values on every pack value and name, and dedups the pools. Every lexicon form still in play (question wordings
and band paraphrases) gets its unit test, then one extraction read per independent Haiku task: 2/2 (T31 has no
precedence or window form, so no 3/3 read). Each read is its own batch with its own seed, so a form sits in two
different chunks and two different choice orders. G3-H is not built here: G0 section 7 and C2_DATA_SPEC 6.4 put it at
the pilot (step 5) and full generation (step 7), not at pool stage (step 3).

Haiku answers only flag. Nothing here, and nothing in the reads, sets a label: an admitted form's semantic id comes from
the registry's own declaration, and a read that names no listed meaning rejects the form (G-LEX).
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

_C2_BUILD = Path(__file__).resolve().parents[2]
if str(_C2_BUILD) not in sys.path:
    sys.path.insert(0, str(_C2_BUILD))

from c2_kit import chunker as CH  # noqa: E402
from c2_kit import gsl, paths  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from families.T31 import haiku_author as HA  # noqa: E402

F = "T31"
SEED = "t31-glex-v1"
HERE = Path(__file__).resolve().parent
EXTRACT = HERE / "haiku" / "extract"
READS = ("read0", "read1")                 # 2/2 (no precedence or window form in T31)
CHUNK = 50                                 # <= 50 items per chunk (chunker.MAX_ITEMS)

EXTRACT_PROMPT = (
    "Each item gives one phrase or question and a list of meanings. Pick the ONE meaning in the list that the phrase "
    "or question expresses exactly, reading its words. If no meaning in the list fits exactly, answer null. Do not "
    "answer the question, and do not judge whether any statement is true.")
EXTRACT_TAIL = (
    "\n\nOUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON "
    "array with one object per item: {\"qid\": \"<the item's qid>\", \"choice\": \"<the chosen meaning copied exactly, "
    "or null>\"}. Valid JSON only; no text before or after the array. Do not open, list or search any other file, and "
    "run no other tool.")


def _norm(text: str) -> str:
    return " ".join(text.casefold().split())


# ------------------------------------------------------------------------------------------------ lint and dedup

def lint_pools(pools: dict) -> list:
    """gsl.lint_values on every pack value and name. Returns [(piece, reason)] for each failing piece."""
    bad = []
    for n in pools["names"]:
        v = gsl.lint_values({"NAME": S.name_slot(n)})
        if v:
            bad.append((f"name|{n}", "; ".join(f"{x.rule}: {x.detail}" for x in v)))
    for p in pools["packs_appr"]:
        vals = [("process", p["process"], S.name_slot)] + [("item", x, S.name_slot) for x in p["items"]] + \
               [("role", x, S.name_slot) for x in p["roles"]]
        why = []
        for label, val, mk in vals:
            v = gsl.lint_values({label: mk(val)})
            if v:
                why.append(f"{label} {val!r}: " + "; ".join(f"{x.rule}: {x.detail}" for x in v))
        if why:
            bad.append((f"pack|appr|{p['process']}", "; ".join(why[:3])))
    for p in pools["packs_agent"]:
        vals = [("scope", x, S.id_slot) for x in p["scopes"]] + [("task", x, S.name_slot) for x in p["tasks"]] + \
               [("agent", x, S.id_slot) for x in p["agents"]]
        why = []
        for label, val, mk in vals:
            v = gsl.lint_values({label: mk(val)})
            if v:
                why.append(f"{label} {val!r}: " + "; ".join(f"{x.rule}: {x.detail}" for x in v[:2]))
        if why:
            bad.append((f"pack|agent|{p['scopes'][0]}", "; ".join(why[:3])))
    # the fixed sample fills the loader lints skins with: they must pass the value lint too
    for track in ("appr", "agent"):
        sample = HA._sample_slots(track)
        v = gsl.lint_values(sample)
        if v:
            bad.append((f"sample_fill|{track}", "; ".join(f"{x.rule}: {x.detail}" for x in v)))
    return bad


def _drop_pieces(pools: dict, keep_ids: set, bucket: str) -> None:
    for pid in list(pools[bucket]):
        if pid not in keep_ids:
            del pools[bucket][pid]


def dedup(pools: dict) -> list:
    """Exact-text dedup (casefold, whitespace folded) across skins and attack lines, and exact dedup of packs and names.
    The first piece in sorted id order is kept. Returns [(piece, reason)]."""
    dropped = []
    for bucket in ("skins", "attacks"):
        seen: dict = {}
        keep = set()
        for pid in sorted(pools[bucket]):
            k = _norm(pools[bucket][pid].text)
            if k in seen:
                dropped.append((f"{bucket}|{pid}", f"duplicate text of {seen[k]}"))
            else:
                seen[k] = pid
                keep.add(pid)
        _drop_pieces(pools, keep, bucket)
    for bucket in ("packs_appr", "packs_agent"):
        seen_p: set = set()
        keep_list = []
        for p in pools[bucket]:
            k = json.dumps(p, sort_keys=True)
            if k in seen_p:
                dropped.append((f"{bucket}|{p.get('process') or p.get('scopes', [''])[0]}", "duplicate pack"))
            else:
                seen_p.add(k)
                keep_list.append(p)
        pools[bucket] = keep_list
    seen_n: dict = {}
    keep_names = []
    for n in pools["names"]:
        k = _norm(n)
        if k in seen_n:
            dropped.append((f"name|{n}", f"duplicate of {seen_n[k]} (case-folded)"))
        else:
            seen_n[k] = n
            keep_names.append(n)
    pools["names"] = keep_names
    return dropped


# ------------------------------------------------------------------------------------------------ G-LEX reads

def lexicon_review(reg) -> tuple:
    """(ok form ids, [(form id, reason)]): every form in the registry goes through its unit test first. A form that
    fails its unit test can never be admitted (G-LEX), so it gets no extraction task."""
    ok, bad = [], []
    for fid in sorted(reg.forms):
        if reg.unit_test(fid):
            ok.append(fid)
        else:
            bad.append((fid, "; ".join(reg.forms[fid].unit_problems[:2])))
    return ok, bad


# realistic fills for the extraction read (the kit's first lexicon sample is $0.00, which reads oddly). Gold-free:
# these are display values, and the meaning a read picks does not depend on them.
SAMPLE_FILL = {"CANDIDATE": ("name", "Dana Okafor"), "REQ_AGENT": ("id", "billing-agent"),
               "REQ_SCOPE": ("id", "invoices.approve"), "REQ_ID": ("id", "REQ-1001"), "X": ("cents", 120000)}


def _sample_vals(f) -> dict:
    vals = {}
    for name, kind in f.slots:
        if name not in SAMPLE_FILL or SAMPLE_FILL[name][0] != kind:
            raise CH.ChunkError(f"{f.form_id}: no realistic fill for slot {name} ({kind})")
        k, v = SAMPLE_FILL[name]
        vals[name] = S.name_slot(v) if k == "name" else S.id_slot(v) if k == "id" else S.cents_slot(v)
    return vals


def extraction_items(reg, fids: list, seed: str) -> list:
    """[(form id, {"text", "choices"})]: the form filled with SAMPLE_FILL and every meaning of its kind in a seeded
    order (the same item shape as lexicon.lexicon_items, with realistic fills)."""
    out = []
    for fid in sorted(fids):
        f = reg.forms[fid]
        txt = reg.render(fid, _sample_vals(f))
        mean = sorted((s.meaning for s in reg.sems.values() if s.kind == f.kind),
                      key=lambda m: hashlib.sha256(f"{seed}|{fid}|{m}".encode()).hexdigest())
        out.append((fid, {"text": txt, "choices": mean}))
    return out


def extraction_batches(reg, fids: list) -> list:
    """[(read name, TaskBatch)]: one make_batch per independent read, each with its own seed."""
    out = []
    for read in READS:
        seed = f"{SEED}|{read}"
        items = extraction_items(reg, fids, seed)
        b = CH.make_batch("extract_lex", F, items, seed=seed, prompt=EXTRACT_PROMPT + EXTRACT_TAIL, max_items=CHUNK)
        out.append((read, b))
    return out


def _task_md(b: CH.TaskBatch, chunk: dict, answer: Path, read: str) -> str:
    n = len(chunk["items"])
    return (f"# T31 G-LEX extraction task {chunk['task_id']} ({read})\n\n"
            f"ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):\n{answer}\n\n"
            f"Task kind: extract_lex; items: {n}; answers expected: {n} (one per item, answer field \"choice\").\n\n"
            "This task file is the only file you may open. Do not open, list or search any other file or folder.\n\n"
            f"## Instructions\n\n{b.prompt}\n\n"
            "Answer format: [{\"qid\": \"<qid>\", \"choice\": \"<one meaning, copied exactly, or null>\"}, ...]\n\n"
            "## Items (JSON; answer every item once, keyed by its qid)\n\n"
            + json.dumps(chunk["items"], ensure_ascii=False, indent=1) + "\n")


def build_files(reg, fids: list, pool_drops: list, lex_bad: list, counts: dict) -> tuple:
    """({relative path under haiku/extract: text}, [task rows]) for every read chunk, the drop log and TASKS.json."""
    files, tasks = {}, []
    for read, b in extraction_batches(reg, fids):
        files.update(b.files())
        for c in b.chunks:
            tid = c["task_id"]
            answer = EXTRACT / b.answer_path(tid)
            text = _task_md(b, c, answer, read)
            for iid in b.key.values():             # a task file never names an internal (form) id
                if iid in text:
                    raise CH.ChunkError(f"{tid}: task file names an internal id")
            files[f"tasks/{tid}.md"] = text
            reads, writes = b.allowed(str(EXTRACT), tid)
            tasks.append({"task": f"glex-{read}", "task_id": tid, "batch_id": b.batch_id, "kind": "extract_lex",
                          "read": read, "n_items": len(c["items"]), "prompt_sha": b.prompt_sha,
                          "task_file": str(EXTRACT / f"tasks/{tid}.md"), "answer_file": str(answer),
                          "allowed_read": sorted(reads | {str(EXTRACT / f"tasks/{tid}.md")}),
                          "allowed_write": sorted(writes)})
    drops = {"pool_drops": [{"piece": p, "reason": r} for p, r in pool_drops],
             "lexicon_unit_fail": [{"form": f, "reason": r} for f, r in lex_bad],
             "counts": counts}
    files["POOL_DROPS.json"] = json.dumps(drops, ensure_ascii=False, indent=1) + "\n"
    manifest = {"family": F, "seed": SEED, "kind": "extract_lex", "reads": list(READS), "n_tasks": len(tasks),
                "forms_for_admission": len(fids), "required_reads_per_form": 2, "g3h": "not at pool stage (6.4)",
                "tasks": tasks,
                "answer_format": "[{\"qid\": ..., \"choice\": <meaning copied exactly, or null>}]"}
    files["TASKS.json"] = json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"
    return files, tasks


def run(write: bool) -> dict:
    if write and EXTRACT.exists() and any(EXTRACT.iterdir()):
        raise SystemExit("haiku/extract already holds files: refusing to rewrite the reads (keys would no longer match)")
    res = HA.load()
    pools, drops = res["pools"], res["drops"]

    # 1. lint: the loader's G-SL pass (skins, wordings, attacks, Mode F) already dropped its failures into res["drops"]
    loader_drop_pieces = []
    answer_problems = []
    for tid, iid, why in drops:
        if iid == "*":
            answer_problems.append({"task": tid, "why": why})
        else:
            loader_drop_pieces.append({"piece": f"{tid}|{iid}", "reason": why})
    value_bad = lint_pools(pools)
    pool_drops = [(d["piece"], d["reason"]) for d in loader_drop_pieces]
    pool_drops += [(p, r) for p, r in value_bad]

    # 2. dedup (skins and attacks by text, packs and names exactly)
    pool_drops += dedup(pools)

    # 3. lexicon: unit test every form; the band and wording forms are the pieces that need admission
    reg = pools["lexicon"]
    fids, lex_bad = lexicon_review(reg)
    forms_by_kind = Counter(reg.forms[f].kind for f in fids)
    strict = sum(1 for f in fids if reg.forms[f].required == 3)
    counts = {
        "tasks_loaded": len(res["missing"]) == 0,
        "tasks_missing": len(res["missing"]),
        "skins_T": sum(s.author_mode == "T" for s in pools["skins"].values()),
        "skins_F": sum(s.author_mode == "F" for s in pools["skins"].values()),
        "attacks": len(pools["attacks"]),
        "wordings": len(pools["wordings"]),
        "band_forms": sum(1 for f in reg.forms.values() if f.kind == "comparator"),
        "packs_appr": len(pools["packs_appr"]),
        "packs_agent": len(pools["packs_agent"]),
        "names": len(pools["names"]),
        "loader_lint_dropped_pieces": len(loader_drop_pieces),
        "value_lint_dropped": len(value_bad),
        "dedup_dropped": len(pool_drops) - len(loader_drop_pieces) - len(value_bad),
        "answer_problems": len(answer_problems),
        "lexicon_forms_total": len(reg.forms),
        "lexicon_unit_fail": len(lex_bad),
        "forms_for_admission": len(fids),
        "forms_for_admission_by_kind": dict(forms_by_kind),
        "forms_needing_3_of_3": strict,
        "extraction_reads_per_form": 2,
        "extraction_items": 2 * len(fids),
        "g3h_items": 0,
    }
    files, tasks = build_files(reg, fids, pool_drops, lex_bad, counts)
    counts["extract_chunk_tasks"] = len(tasks)
    # the counts above are written into POOL_DROPS.json, so refresh that file with the final numbers
    drops_obj = json.loads(files["POOL_DROPS.json"])
    drops_obj["counts"] = counts
    files["POOL_DROPS.json"] = json.dumps(drops_obj, ensure_ascii=False, indent=1) + "\n"
    if write:
        paths.write_files(EXTRACT, files)
    return {"counts": counts, "tasks": tasks, "pool_drops": pool_drops, "lex_bad": lex_bad,
            "answer_problems": answer_problems, "written": write}


def main(argv: list) -> int:
    cmd = argv[1] if len(argv) > 1 else "check"
    if cmd not in ("check", "build"):
        print(__doc__)
        return 2
    out = run(write=(cmd == "build"))
    print(json.dumps({"mode": cmd, "counts": out["counts"], "n_tasks": len(out["tasks"]),
                      "extract_dir": str(EXTRACT), "written": out["written"]}, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
