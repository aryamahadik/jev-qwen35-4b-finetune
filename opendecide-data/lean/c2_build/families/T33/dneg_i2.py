"""families/T33/dneg_i2.py: the double-negation wordings of fix iteration 2 (G10 double_negation_share; G0_SPEC section 9 G2).

The frozen pools hold no wording for the two double-negation forms (yn_dneg_step_ok, yn_dneg_all_supported), so the
sampler asks the positive form instead and G10 double_negation_share is 0%. This module is the shared part of the
three steps that put Haiku-authored wordings into the pools without editing a frozen pool file:

  write-tasks   (this module's CLI) the authoring task files under haiku/dneg_i2/tasks/: the family's existing
                double-negation items (haiku_author.dneg_items) with the polarity-aware brief (explicit outer frame, a
                `not` on meeting the criterion / before every, no contracted opening, no word with a negative meaning of
                its own), 6 items x 6 wordings = 36 candidates per form (4.5x the 8 admitted wordings per form that
                G0 asks for), each item with its own angle so the wordings differ.
  dneg_stage2   admits the authoring answers (shape, word bans, negation count, polarity rules P1-P4, lexicon unit test,
                G-SL) and writes the G-LEX task files, two independent reads, under haiku/dneg_i2/glex_tasks/.
  dneg_stage3   records the reads, keeps the wordings that pass G-LEX 2/2 (>= 8 per form), appends them to
                pools/dneg_i2_supplement.json (append-and-freeze: pools/DNEG_I2_FREEZE.json holds its sha256 and the
                shas of the frozen pool files, which are never edited) and runs the pilot.

run_pilot_i2.py patches haiku_author.load_ctx with load_ctx_i2 here, so pilot_loaders (not edited) gets the supplement.
No Haiku, no model and no network is used by any of this code.

  ../../.venv/bin/python -B -m families.T33.dneg_i2 write-tasks        (from lean/c2_build)
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, paths  # noqa: E402
from c2_kit.lexicon import LexiconRegistry  # noqa: E402
from families.T33 import haiku_author as H  # noqa: E402
from families.T33 import plugin as T  # noqa: E402

VERSION = "v1-i2"
ROOT = H.HAIKU / "dneg_i2"                       # tasks/, glex_tasks/, stage2_report.json, stage3_report.json
FORMS = tuple(T.DNEG_FALLBACK)                   # yn_dneg_step_ok, yn_dneg_all_supported
ITEMS_PER_FORM = 6                               # x H.FORMS_PER_ITEM (6) = 36 candidates per form
ITEMS_PER_CHUNK = 3                              # 12 items -> 4 chunks
MIN_ADMITTED = 8                                 # per form (TARGETS["wording"], never lowered)
SUPPLEMENT = "dneg_i2_supplement.json"
FREEZE = "DNEG_I2_FREEZE.json"
FROZEN_FILES = ("skins.json", "lexicon.json", "packs.json", "voices.json")
_BASE_LOAD = H.load_ctx                          # the frozen-pools loader, captured before any patch

ANGLES = {
    "yn_dneg_step_ok": (
        'Open with the frame "is it not true that".',
        'Open with the frame "is it not the case that".',
        'Put a short lead-in such as "in the log," before the frame.',
        "Use the verb meet in the inner clause (does not meet).",
        "Use the verb satisfy in the inner clause (does not satisfy).",
        "Use the verb reach, clear or pass in the inner clause, and keep the word criterion."),
    "yn_dneg_all_supported": (
        'Open with the frame "is it not true that" and use the words not every.',
        'Open with the frame "is it not the case that" and use the words not all.',
        'Put a short lead-in such as "going by the log," before the frame.',
        "Say backed up in the inner clause.",
        "Say supported in the inner clause.",
        "Say borne out in the inner clause."),
}


# G-SL grammar: the word right after the count {STEP} must be of, in or on (or the question mark), so "step {STEP} does
# not meet" is dropped whatever its polarity. The base brief's clause shape says "step {STEP} does not meet"; this note
# settles the conflict for Haiku (found while fabricating answers for the stage tests: every such wording failed G-SL).
SLOT_NOTE = {
    "yn_dneg_step_ok": ('Always write the step as "step {STEP} of the log" or "step {STEP} in the log" (so {STEP} is '
                        'followed directly by of or in, never by does), e.g. "... that step {STEP} of the log does '
                        'not meet its success criterion".'),
    "yn_dneg_all_supported": "",
}


def items() -> list:
    """[(internal id, item)] of the two forms: haiku_author's own double-negation items (polarity-aware briefs) at
    ITEMS_PER_FORM per form, each with its angle appended to the brief."""
    old = H.WORDING_ITEMS
    H.WORDING_ITEMS = {q: ITEMS_PER_FORM for q in FORMS}
    try:
        base = H.dneg_items()
    finally:
        H.WORDING_ITEMS = old
    out = []
    for iid, it in base:
        _t, _w, qf, j = iid.split("|")
        out.append((iid, {**it, "brief": " ".join(x for x in (it["brief"], ANGLES[qf][int(j)], SLOT_NOTE[qf]) if x)}))
    return out


def build_batch(tasks_root: Path) -> chunker.TaskBatch:
    b = chunker.make_batch("author_wording", H.F, items(), seed=f"{H.F}-author-{VERSION}-wordings-dneg",
                           prompt=H.PROMPTS["wordings"], max_items=ITEMS_PER_CHUNK, forbid_strings=H.FORBID)
    for c in b.chunks:
        c["instructions"] = H.PROMPTS["wordings"]
        c["answer_format"] = H.ANSWER_TEXTS
        c["answer_file"] = str(Path(tasks_root) / b.answer_path(c["task_id"]))
    return b


def write_tasks(root: Path = ROOT) -> list:
    """Write the authoring chunks under <root>/tasks/ (the kit's guarded writer). Returns the task list."""
    tasks_root = Path(root) / "tasks"
    b = build_batch(tasks_root)
    files = dict(b.files())
    tasks = H.task_list([("wordings", b)], tasks_root)
    files["TASKS.json"] = json.dumps({"family": H.F, "version": VERSION, "n_tasks": len(tasks), "tasks": tasks,
                                      "batches": {"wordings": b.batch_id}, "forms": list(FORMS),
                                      "candidates_per_form": ITEMS_PER_FORM * H.FORMS_PER_ITEM,
                                      "min_admitted_per_form": MIN_ADMITTED}, indent=1) + "\n"
    paths.write_files(tasks_root, files)
    for t in tasks:                                          # the answer folder exists before the authoring runs
        Path(t["answer_file"]).parent.mkdir(parents=True, exist_ok=True)
    return tasks


# ------------------------------------------------------------------------------------------------ the supplement
def _sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def frozen_shas(frozen_dir: Path = H.POOLS) -> dict:
    """The shas of the frozen pool files, checked against the pool MANIFEST (they must be what was frozen)."""
    frozen_dir = Path(frozen_dir)
    man = json.loads((frozen_dir / "MANIFEST.json").read_text(encoding="utf-8"))["sha256"]
    got = {k: hashlib.sha256((frozen_dir / k).read_bytes()).hexdigest() for k in FROZEN_FILES}
    bad = [k for k in FROZEN_FILES if got[k] != man[k]]
    if bad:
        raise RuntimeError(f"frozen pool files changed since the freeze: {bad}")
    return got


def freeze_supplement(skins_json: list, forms_json: list, extra: dict, *, sems_json: list = (),
                      pools_dir: Path = H.POOLS, frozen_dir: Path = H.POOLS) -> str:
    """Append-and-freeze: write pools_dir/dneg_i2_supplement.json and DNEG_I2_FREEZE.json once. A second call with
    the same content is a no-op ("unchanged"); with other content it raises (a frozen file is never rewritten)."""
    sup = {"family": H.F, "version": VERSION, "kind": "append-only supplement to the frozen pools (G0_SPEC section 9)",
           "skins": sorted(skins_json, key=lambda s: s["skin_id"]),
           "lexicon_sems": sorted(sems_json, key=lambda x: x["sem_id"]),
           "lexicon_forms": sorted(forms_json, key=lambda f: f["form_id"]), **extra}
    text = json.dumps(sup, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    pools_dir = Path(pools_dir)
    sp = pools_dir / SUPPLEMENT
    if sp.is_file():
        if sp.read_text(encoding="utf-8") == text:
            return "unchanged"
        raise RuntimeError(f"{sp} is frozen and the new content differs (append-and-freeze never rewrites)")
    fz = {"supplement": SUPPLEMENT, "supplement_sha256": _sha(text), "frozen_pools_sha256": frozen_shas(frozen_dir),
          "n_skins": len(sup["skins"]), "n_forms": len(sup["lexicon_forms"]),
          "per_form": extra.get("per_form", {})}
    paths.write_files(pools_dir, {SUPPLEMENT: text, FREEZE: json.dumps(fz, indent=1) + "\n"})
    return "written"


def read_supplement(pools_dir: Path = H.POOLS, frozen_dir: Path = H.POOLS):
    """The frozen supplement or None when there is none; raises when its sha or the frozen files' shas drifted."""
    pools_dir = Path(pools_dir)
    sp, fp = pools_dir / SUPPLEMENT, pools_dir / FREEZE
    if not sp.is_file():
        return None
    fz = json.loads(fp.read_text(encoding="utf-8"))
    if _sha(sp.read_text(encoding="utf-8")) != fz["supplement_sha256"]:
        raise RuntimeError("the supplement differs from its freeze record")
    if frozen_shas(frozen_dir) != fz["frozen_pools_sha256"]:
        raise RuntimeError("the frozen pool files differ from the ones the supplement was frozen against")
    return json.loads(sp.read_text(encoding="utf-8"))


def merge(ctx, sup: dict):
    """A KitCtx holding the base ctx plus the supplement (lexicon forms with their reads, wording skins)."""
    base = ctx.lexicon.to_json()
    have = {f["form_id"] for f in base["forms"]}
    clash = sorted(f["form_id"] for f in sup["lexicon_forms"] if f["form_id"] in have)
    if clash:
        raise RuntimeError(f"supplement forms already in the frozen lexicon: {clash[:3]}")
    # the frozen lexicon predates the double-negation question forms: their sems are declared by the supplement
    sems = base["sems"] + [x for x in sup.get("lexicon_sems", ()) if x["sem_id"] not in {s["sem_id"] for s in base["sems"]}]
    reg = LexiconRegistry.from_json({**base, "sems": sems, "forms": base["forms"] + list(sup["lexicon_forms"])})
    skins = dict(ctx.skins)
    new = H.skins_from_json(sup["skins"])
    if set(skins) & set(new):
        raise RuntimeError("supplement skins already in the frozen skins")
    skins.update(new)
    return H.KitCtx(skins=skins, lexicon=reg)


def load_ctx_i2(root: Path = H.POOLS, *, pools_dir: Path | None = None) -> tuple:
    """haiku_author.load_ctx() plus the frozen supplement, if there is one: (KitCtx, packs, voices)."""
    ctx, packs, voices = _BASE_LOAD(root)
    sup = read_supplement(pools_dir or root, root)
    return (merge(ctx, sup) if sup else ctx), packs, voices


def main(argv=None) -> int:
    cmd = (argv or sys.argv[1:] or ["write-tasks"])[0]
    if cmd != "write-tasks":
        print("usage: python -B -m families.T33.dneg_i2 write-tasks", file=sys.stderr)
        return 2
    print(json.dumps(write_tasks(), indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
