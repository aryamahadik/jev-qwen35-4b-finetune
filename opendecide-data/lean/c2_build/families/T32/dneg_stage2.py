"""families/T32/dneg_stage2.py: F8 yn_dneg_broken re-authoring, fix iteration 2 (steps before and after the Haiku authoring run).

  tasks   write the authoring task files: haiku/dneg_i2/tasks/<task_id>.md (self-contained: instructions, items, answer
          contract, answer path) + the chunk json / manifest / key of authoring.reauthor_dneg_batch (REAUTHOR_FORMS brief).
          Answers go to haiku/dneg_i2/answers/<task_id>.json. Nothing is answered here.
  admit   (stage 2) read the authoring answers, run the wording admission (authoring.check_wording(..., polarity=True): the
          polarity rule P1-P3 and the F8 truth-evaluation frame; duplicates; the lexicon unit test), then write the G-LEX
          task files for TWO independent Haiku reads (glex-r1, glex-r2) to haiku/dneg_i2/glex_tasks/<task_id>.md
          (chunks, key and answers in haiku/dneg_i2/glex/), and haiku/dneg_i2/candidates.json.
  apply_supplement(kit): used by run_pilot_i2.py's loader and dneg_stage3.py: adds the admitted forms of
          haiku/dneg_i2/pool_supplement.json to the kit's lexicon and wording skins (pilot_loaders.py is not edited).

  ../.venv/bin/python -B families/T32/dneg_stage2.py tasks|admit [--root DIR]      (from lean/c2_build; --root: tests)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

FAMILY = "T32"
QFORM = "yn_dneg_broken"
ROOT = HERE / "haiku" / "dneg_i2"
SUPPLEMENT = ROOT / "pool_supplement.json"
CONTRACT_AUTHOR = ('Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array '
                   'with one object per item, in item order: {"qid": "<the item\'s qid>", "wordings": ["<question 1>", ...]} '
                   '(the list holds exactly the number of questions the item asks for). Exactly the keys qid and wordings. '
                   'Valid JSON only; no text before or after the array.')
CONTRACT_GLEX = ('Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array '
                 'with one object per item: {"qid": "<the item\'s qid>", "meaning": "<one CHOICE copied exactly from that '
                 'item\'s choices>"}. Exactly the keys qid and meaning. Valid JSON only; no text before or after the array.')


def _write(root: Path, files: dict) -> None:
    from c2_kit import paths
    if Path(root) == ROOT:
        paths.write_files(root, files)
        return
    for rel, text in files.items():
        p = Path(root) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")


def task_md(chunk: dict, title: str, contract: str) -> str:
    n = len(chunk["items"])
    return (f"# {title} {chunk['task_id']} (family {FAMILY})\n\nANSWER FILE (write your whole answer here, and nowhere "
            f"else, with the Write tool):\n{chunk['answer_file']}\n\nThis task file is the only file you may open. Do not "
            "open, list or search any other file or folder, do not run shell commands and do not use the web.\n\n"
            f"Items: {n}. Answers expected: {n} (one per item, each with that item's qid).\n\n## Instructions\n\n"
            f"{chunk['instructions']}\n\n## Answer contract\n\n{contract}\n\n## Items (JSON; answer every item exactly once, "
            f"keyed by its qid)\n\n{json.dumps(chunk['items'], ensure_ascii=False, indent=1)}\n")


def _write_md(root: Path, sub: str, batch, title: str, contract: str) -> list:
    out = []
    for c in batch.chunks:
        p = Path(root) / sub / f"{c['task_id']}.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(task_md(c, title, contract), encoding="utf-8")
        out.append(str(p))
    return out



def _A():
    import importlib
    return importlib.import_module("families.T32.authoring")


def tasks(root: Path = ROOT) -> list:
    A = _A()
    b = A.reauthor_dneg_batch(root)
    _write(root, b.files())
    return _write_md(root, "tasks", b, "F8 yn_dneg_broken authoring task", CONTRACT_AUTHOR)


def _registry():
    import importlib
    from c2_kit.lexicon import LexiconRegistry
    FV = importlib.import_module("families.T32.freeze_v2")
    return LexiconRegistry.from_json(FV.load_pools()["lexicon"].to_json())


def _add_candidates(reg, cands: list) -> list:
    """Adds the candidate forms to `reg` (a copy); returns their form ids."""
    from c2_kit.lexicon import question_sem
    sem = question_sem(FAMILY, QFORM)
    ids = []
    for c in cands:
        f = reg.add(c["text"], sem, slots=dict(c["slots"]), source="haiku", family=FAMILY,
                    haiku_task_id=c["haiku_task_id"], haiku_prompt_sha=c["haiku_prompt_sha"])
        ids.append(f.form_id)
    return ids


def glex_batches(reg, fids: list, root: Path = ROOT) -> list:
    """[(read, TaskBatch)]: the two independent G-LEX reads of the candidate forms (deterministic: stage 3 rebuilds them)."""
    from c2_kit import chunker
    import importlib
    X = importlib.import_module("families.T32.extract")
    out = []
    for inst, read in enumerate(("glex-r1", "glex-r2")):
        items = [(fid, {"text": it["text"], "choices": it["choices"] + [X.NONE_OF_THESE]})
                 for fid, it in X.glex_items(reg, fids, f"t32-dneg-i2-{read}", inst)]
        gb = chunker.make_batch("extract_lex", FAMILY, items, seed=f"t32-dneg-i2-{read}", prompt=X.GLEX_PROMPT)
        out.append((read, X._finish(gb, Path(root) / "glex")))
    return out


def admit(root: Path = ROOT) -> dict:
    from c2_kit import chunker
    from c2_kit.lexicon import question_sem
    import importlib
    A, X = _A(), importlib.import_module("families.T32.extract")
    b = A.reauthor_dneg_batch(root)
    raw = {}
    for c in b.chunks:
        ap = Path(c["answer_file"])
        if not ap.exists():
            raise SystemExit(f"no authoring answer yet: {ap}")
        raw[c["task_id"]] = json.loads(ap.read_text(encoding="utf-8"))
    got, probs = chunker.load_answers(b, raw)
    inv = chunker.item_by_internal(b)
    reg = _registry()
    sem = question_sem(FAMILY, QFORM)
    template = next(f for f in reg.forms.values() if f.sem_id == sem)
    slots = dict(template.slots)
    seen = {" ".join(f.text.casefold().split()) for f in reg.forms.values()}
    tid_of = {c["task_id"]: c for c in b.chunks}
    cands, rejected = [], []
    for iid in sorted(inv):
        a = got.get(iid)
        texts = a.get("wordings") if isinstance(a, dict) else None
        if not isinstance(texts, list):
            probs.append(f"{iid}: no wordings list")
            continue

        tid = b.task_of[next(q for q, i in b.key.items() if i == iid)]
        for t in texts:
            norm = " ".join(str(t).casefold().split())
            pr = A.check_wording(QFORM, t, polarity=True) if isinstance(t, str) else ["not a string"]
            if not pr and norm in seen:
                pr = ["duplicate of an existing wording"]
            if pr:
                rejected.append({"iid": iid, "text": t, "problems": pr})
                continue
            seen.add(norm)
            cands.append({"iid": iid, "text": t.strip(), "slots": [list(s) for s in slots.items()],
                          "haiku_task_id": tid, "haiku_prompt_sha": tid_of[tid]["prompt_sha"]})
    ids = _add_candidates(reg, [{**c, "slots": dict(c["slots"])} for c in cands])
    unit = {fid: reg.unit_test(fid) for fid in ids}
    keep = [c for c, fid in zip(cands, ids) if unit[fid]]
    rejected += [{"iid": c["iid"], "text": c["text"], "problems": ["lexicon unit test failed"]}
                 for c, fid in zip(cands, ids) if not unit[fid]]
    (Path(root)).mkdir(parents=True, exist_ok=True)
    (Path(root) / "candidates.json").write_text(json.dumps({"candidates": keep, "rejected": rejected,
                                                            "answer_problems": probs}, indent=1, ensure_ascii=False))
    reg2 = _registry()
    fids = _add_candidates(reg2, [{**c, "slots": dict(c["slots"])} for c in keep])
    out = {"candidates": len(keep), "rejected": len(rejected), "answer_problems": probs, "glex_tasks": []}
    if not fids:
        return out
    for read, gb in glex_batches(reg2, fids, root):
        _write(Path(root) / "glex", gb.files())
        out["glex_tasks"] += _write_md(root, "glex_tasks", gb, f"G-LEX read {read} task", CONTRACT_GLEX)
    return out


def apply_supplement(kit, path: Path = SUPPLEMENT) -> int:
    """Adds the admitted dneg wordings of the supplement to kit.plugin.lexicon and kit.ctx (wording skins); returns how
    many were added (0 when there is no supplement). The plugin's wording-pool caches are reset."""
    if not Path(path).exists():
        return 0
    from c2_kit.plugin import KitCtx
    import pilot_loaders as PL
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    reg = kit.plugin.lexicon
    n = 0
    for f in d["forms"]:
        lf = reg.add(f["text"], f["sem"], slots=dict(f["slots"]), source="haiku", family=FAMILY,
                     haiku_task_id=f["haiku_task_id"], haiku_prompt_sha=f["haiku_prompt_sha"])
        for read, sem in f["extractions"]:
            reg.record_extraction(lf.form_id, read, sem)
        n += 1
    ws = PL.question_wording_skins(FAMILY, type(kit.plugin), reg)
    kit.ctx = KitCtx(skins={**kit.ctx.skins, **ws}, lexicon=reg)
    for attr in ("_screened", "_by_setting", "_form_cache", "_pool_cache", "_pair_cache"):
        getattr(kit.plugin, attr).clear()
    kit.plugin.dneg_ok = kit.plugin._clean_wordings(QFORM)
    return n


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=("tasks", "admit"))
    ap.add_argument("--root", default=str(ROOT))
    a = ap.parse_args(argv)
    r = tasks(Path(a.root)) if a.cmd == "tasks" else admit(Path(a.root))
    print(json.dumps(r, indent=1, ensure_ascii=False)[:3000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
