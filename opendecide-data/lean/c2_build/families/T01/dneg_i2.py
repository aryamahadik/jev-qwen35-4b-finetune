"""families/T01/dneg_i2.py: the double-negation wordings of fix iteration 2 (G10 double_negation_share; G0_SPEC_v4 12.1).

The frozen pools_v2/ hold no wording for the six yn_dneg_* forms, so T01.dneg_ok is False for every one of them, the sampler
asks the positive form and G10 double_negation_share is 0% (bar >= 2% of yes/no rows). This module is the shared part of the
three steps that put Haiku-authored wordings into the pools without editing a frozen pool file:

  write-tasks   (CLI here) the gold-free, polarity-aware authoring task files under haiku/dneg_i2/tasks/: haiku_dneg's brief
                (explicit outer frame "is it not the case / true that", the second negation on the clause's own positive
                word, no contraction, no word of lateness / blocking / denial / lack) for the six forms, 32 items per form =
                4x the 8 admitted wordings per form that G0 asks for. Each item has its own angle (frame x lead-in), its own
                inner phrasing and its own slot set, so the 32 wordings of a form differ. Answers: haiku/dneg_i2/answers/.
  dneg_stage2   admits the authoring answers (haiku_dneg.check_wording: shape, word bans, exact negcount (2, 2), polarity
                P1-P4 in strict frames, G-SL) and writes the G-LEX task files, two independent reads, to haiku/dneg_i2/glex_tasks/.
  dneg_stage3   records the reads, keeps the wordings with G-LEX 2/2, freezes pools_v2/dneg_i2_supplement.json (+ its freeze
                record), then runs the family tests, determinism, the pilot into pilot_i2/ and G6 at 6,000 rows.

run_pilot_i2.py patches freeze_v2.make_ctx with make_ctx_i2 here, so pilot_loaders (not edited) gets the supplement.
No Haiku, no model and no network is used by any of this code.

  ../../.venv/bin/python -B -m families.T01.dneg_i2 write-tasks        (from lean/c2_build)
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
from c2_kit import skin as K  # noqa: E402
from c2_kit.lexicon import LexiconRegistry, question_sem  # noqa: E402
from families.T01 import extract as E  # noqa: E402
from families.T01 import fixtures as FX  # noqa: E402
from families.T01 import freeze_v2 as FV  # noqa: E402
from families.T01 import haiku_author as A  # noqa: E402
from families.T01 import haiku_dneg as HD  # noqa: E402
from families.T01 import plugin as P  # noqa: E402

FAMILY = "T01"
VERSION = "v1-i2"
ROOT = A.HERE / "haiku" / "dneg_i2"            # tasks/, answers/, glex_tasks/, stage2_report.json, stage3_report.json
FORMS = HD.FORMS                                # the six yn_dneg_* forms
MIN_ADMITTED = 8                                # per form (G0 target, never lowered)
CANDIDATE_MULT = 4                              # 4x candidates per needed wording
N_PER_FORM = MIN_ADMITTED * CANDIDATE_MULT      # 32 items (one wording each) per form
ITEMS_PER_CHUNK = 24                            # 192 items -> 8 task files
SEED = f"t01-dneg-{VERSION}"
POOLS_DIR = FV.POOLS_V2
SUPPLEMENT = "dneg_i2_supplement.json"
FREEZE = "DNEG_I2_FREEZE.json"
GLEX_READS = ("glex-i2-r1", "glex-i2-r2")       # two independent reads (extractor ids)
FROZEN_FILES = tuple(FV.POOL_FILES) + ("MANIFEST.json",)

FRAMES = ("is it not the case that", "is it not true that")
LEADS = ("", "Under the card's rule,", "According to the rule card,", "Going by the record,")
ANGLES = [(f, l) for l in LEADS for f in FRAMES]            # 8 combos: item i uses ANGLES[i % 8]
OLD_RULE7 = "7. Follow the item's style hint for the opening."
PROMPT = A.WORDING_PROMPT.replace(OLD_RULE7, "7. Follow the item's angle for the opening (the outer frame and the lead-in, if any).")
assert PROMPT != A.WORDING_PROMPT

INNER = {   # qform -> 4 phrasings of the second negation (item i uses INNER[q][(i // 8) % 4]); meaning stays that of the form
    "yn_dneg_over": ("'... is not over the stay limit'", "'... is not above the stay limit'",
                     "'... is not beyond the stay limit'", "'... does not exceed the stay limit'"),
    "yn_dneg_timely": ("'... was not filed in time'", "'... was not filed on or before the final day'",
                       "'... was not submitted in time'", "'... was not filed by the final day of the filing period'"),
    "yn_dneg_covered": ("'... is not covered'", "'... is not covered under the cover rule'",
                        "'... is not a covered loss'", "'... is not one that the policy covers'"),
    "yn_dneg_quotes": ("'... does not need written quotes'", "'... does not call for written quotes'",
                       "'... does not require written quotes'", "'... does not have to get written quotes'"),
    "yn_dneg_cash_report": ("'no cash report is required'", "'no cash report is needed'",
                            "'no cash report is called for'", "'no cash report is due'"),
    "yn_dneg_on_time": ("'... was not on time'", "'... was not counted as received on time'",
                        "'... was not on time under the receipt rule'", "'... was not received on time under the receipt rule'"),
}


def angle_of(i: int) -> tuple:
    return ANGLES[i % len(ANGLES)]


def items() -> tuple:
    """([(internal id, item)], plan): 32 items per form. Gold-free: an item carries the form's meaning and construction
    rules (haiku_dneg.DNEG_BRIEF), its angle, its inner phrasing and its placeholders; never an answer."""
    its, plan = [], {}
    for q in FORMS:
        kind = P.KIND_OF[q]
        meaning, rules = HD.DNEG_BRIEF[q]
        for i in range(N_PER_FORM):
            slots = A.SLOT_SETS[kind][(i // len(ANGLES) + i) % len(A.SLOT_SETS[kind])]
            frame, lead = angle_of(i)
            inner = INNER[q][(i // len(ANGLES)) % len(INNER[q])]
            ph = ", ".join("{" + s + "}" for s in slots)
            refer = (f" Refer to the record as {A.KIND_NOUN[kind]} when you use {{REF}}." if "REF" in slots else "")
            angle = (f"Angle: use the outer frame \"{frame}\"" +
                     (f" and open the sentence with \"{lead}\" before it." if lead else " and open the sentence with it (no lead-in)."))
            iid = f"t01d2.wording.{q}.{i:03d}"
            its.append((iid, {"brief": meaning, "slots": list(slots),
                              "rules": rules + [angle, f"Inner phrasing to aim for (vary the nouns, keep the meaning): {inner}.",
                                                f"Placeholders: exactly {ph}, each once.{refer}"]}))
            plan[iid] = {"role": "wording", "qform": q, "kind": kind, "slots": list(slots), "held_out": False,
                         "frame": frame, "lead": lead, "inner": (i // len(ANGLES)) % len(INNER[q])}
    return its, plan


def build_batch() -> tuple:
    """(TaskBatch, plan): in memory, nothing written."""
    its, plan = items()
    b = chunker.make_batch("author_wording", FAMILY, its, seed=f"{SEED}|wordings", prompt=PROMPT,
                           max_items=ITEMS_PER_CHUNK, forbid_strings=HD.FORBID)
    return b, plan


def write_tasks(root: Path = ROOT) -> list:
    """Chunks, key, manifest, plan, one self-contained task file per chunk (tasks/<id>.md: instructions, answer format,
    items, exact answer-file path) and TASKS.json, via the kit's guarded writers."""
    root = Path(root)
    b, plan = build_batch()
    files = dict(b.files())
    files[f"plan/{b.batch_id}.json"] = json.dumps({"batch_id": b.batch_id, "name": "wordings_dneg_i2", "kind": b.kind,
                                                   "plan": plan}, indent=1, sort_keys=True) + "\n"
    tasks = []
    for c in b.chunks:
        tid = c["task_id"]
        ans = str(root / b.answer_path(tid))
        tfile = f"tasks/{tid}.md"
        files[tfile] = A.task_file_text(b, c, ans)
        tasks.append({"task_file": str(root / tfile), "answer_file": ans, "kind": b.kind, "batch": "wordings_dneg_i2",
                      "batch_id": b.batch_id, "task_id": tid, "n_items": len(c["items"]), "prompt_sha": b.prompt_sha,
                      "audit_allowed_read": [str(root / tfile)], "audit_allowed_write": [ans]})
    paths.write_files(root, files)
    paths.write_json(root / "TASKS.json", {
        "family": FAMILY, "version": VERSION, "n_tasks": len(tasks), "tasks": tasks, "forms": list(FORMS),
        "candidates_per_form": N_PER_FORM, "min_admitted_per_form": MIN_ADMITTED, "g0_sha256": P.T01.G0_SHA256,
        "contract": "one JSON list, one {\"qid\", \"text\"} object per item of the task file, written to its answer_file",
        "next": "one fresh Haiku agent per task file, then: python -B -m families.T01.dneg_stage2"})
    for t in tasks:
        Path(t["answer_file"]).parent.mkdir(parents=True, exist_ok=True)
    return tasks


# ------------------------------------------------------------------------------------------------ G-LEX (stage 2 / 3)
def glex_registry(cands: list) -> tuple:
    """(registry, form ids {cand index: form id}, drops). Every question sem of the frozen lexicon plus the six double-
    negation sems are declared (so a read chooses among all question meanings); one form per candidate."""
    full = FV.read_json(POOLS_DIR / "lexicon_registry.json")
    reg = LexiconRegistry(FAMILY)
    for s in full["sems"]:
        reg.declare(s["sem_id"], s["kind"], s["meaning"])
    for qf, meaning in FX.DNEG_MEANINGS.items():
        if question_sem(FAMILY, qf) not in reg.sems:
            reg.declare(question_sem(FAMILY, qf), "question", meaning)
    fids, drops = {}, []
    for k, c in enumerate(cands):
        try:
            f = reg.add(c["text"], question_sem(FAMILY, c["qform"]), slots=c["slots"], source="haiku", family=FAMILY,
                        haiku_task_id=c["task_id"], haiku_prompt_sha=c["prompt_sha"])
        except Exception as e:  # noqa: BLE001
            drops.append({"iid": c["iid"], "reason": f"form: {str(e)[:100]}"})
            continue
        if not reg.unit_test(f.form_id):
            drops.append({"iid": c["iid"], "reason": f"lexicon unit test: {f.unit_problems[:1]}"})
            continue
        fids[k] = f.form_id
    return reg, fids, drops


def glex_batches(reg: LexiconRegistry, form_ids: list) -> list:
    """[(read label, TaskBatch)]: one batch per read, so each read has its own chunk files (another filled instance and
    another choice order per read: extract.glex_items)."""
    out = []
    for instance, label in enumerate(GLEX_READS):
        seed = f"t01-dneg-i2-{label}"
        out.append((label, chunker.make_batch("extract_lex", FAMILY, E.glex_items(reg, form_ids, seed, instance),
                                              seed=seed, prompt=E.GLEX_PROMPT, max_items=E.LEX_CHUNK)))
    return out


# ------------------------------------------------------------------------------------------------ the supplement
def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def frozen_shas(frozen_dir: Path = POOLS_DIR) -> dict:
    frozen_dir = Path(frozen_dir)
    return {n: _sha((frozen_dir / n).read_bytes()) for n in FROZEN_FILES if (frozen_dir / n).is_file()}


def freeze_supplement(sup: dict, *, pools_dir: Path = POOLS_DIR, frozen_dir: Path = POOLS_DIR) -> str:
    """Append-and-freeze: write pools_dir/dneg_i2_supplement.json and DNEG_I2_FREEZE.json once. Same content again is a
    no-op ("unchanged"); other content raises (a frozen file is never rewritten)."""
    text = json.dumps(sup, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    pools_dir = Path(pools_dir)
    sp = pools_dir / SUPPLEMENT
    if sp.is_file():
        if sp.read_text(encoding="utf-8") == text:
            return "unchanged"
        raise RuntimeError(f"{sp} is frozen and the new content differs (append-and-freeze never rewrites)")
    fz = {"supplement": SUPPLEMENT, "supplement_sha256": _sha(text.encode()), "frozen_pools_sha256": frozen_shas(frozen_dir),
          "n_wordings": len(sup["wordings"]), "per_form": sup.get("per_form", {})}
    paths.write_files(pools_dir, {SUPPLEMENT: text, FREEZE: json.dumps(fz, indent=1) + "\n"})
    return "written"


def read_supplement(pools_dir: Path = POOLS_DIR, frozen_dir: Path | None = None):
    """The frozen supplement, or None when there is none; raises when its sha or the frozen pool files' shas drifted."""
    pools_dir = Path(pools_dir)
    sp, fp = pools_dir / SUPPLEMENT, pools_dir / FREEZE
    if not sp.is_file():
        return None
    fz = json.loads(fp.read_text(encoding="utf-8"))
    if _sha(sp.read_bytes()) != fz["supplement_sha256"]:
        raise RuntimeError("the supplement differs from its freeze record")
    if frozen_shas(frozen_dir or POOLS_DIR) != fz["frozen_pools_sha256"]:
        raise RuntimeError("the frozen pool files differ from the ones the supplement was frozen against")
    return json.loads(sp.read_text(encoding="utf-8"))


def merge(ctx, sup: dict):
    """A KitCtx holding `ctx` plus the supplement: the six double-negation sems, the admitted forms with their G-LEX reads,
    and one wording skin per form (same id scheme as freeze_v2.make_ctx)."""
    from c2_kit.plugin import KitCtx
    base = ctx.lexicon.to_json()
    have = {f["form_id"] for f in base["forms"]}
    clash = sorted(f["form_id"] for f in sup["lexicon_forms"] if f["form_id"] in have)
    if clash:
        raise RuntimeError(f"supplement forms already in the frozen lexicon: {clash[:3]}")
    sems = base["sems"] + [x for x in sup["lexicon_sems"] if x["sem_id"] not in {s["sem_id"] for s in base["sems"]}]
    reg = LexiconRegistry.from_json({**base, "sems": sems, "forms": base["forms"] + list(sup["lexicon_forms"])})
    reg.unit_test_all()
    skins = dict(ctx.skins)
    for w in sup["wordings"]:
        sid = f"T01-WD-{w['form_id']}"
        if sid in skins:
            raise RuntimeError(f"supplement skin {sid} already in the frozen skins")
        skins[sid] = K.make_skin(sid, FAMILY, w["text"], dict(w["slots"]), kind="wording", register="question",
                                 qform=w["qform"], held_out=False, lexicon_ids=(w["form_id"],),
                                 haiku_task_id=w["task_id"], haiku_prompt_sha=w["prompt_sha"])
    return KitCtx(skins=skins, lexicon=reg)


_BASE_MAKE_CTX = FV.make_ctx                    # the frozen-pools context builder, captured before any patch


def make_ctx_i2(pools=None, *, pools_dir: Path = POOLS_DIR):
    """freeze_v2.make_ctx plus the frozen supplement, if there is one."""
    ctx = _BASE_MAKE_CTX(pools)
    sup = read_supplement(pools_dir)
    return merge(ctx, sup) if sup else ctx


def main(argv=None) -> int:
    cmd = (argv or sys.argv[1:] or ["write-tasks"])[0]
    if cmd == "plan":
        b, plan = build_batch()
        print(json.dumps({"n_items": len(plan), "chunks": [len(c["items"]) for c in b.chunks]}))
        return 0
    if cmd != "write-tasks":
        print("usage: python -B -m families.T01.dneg_i2 write-tasks | plan", file=sys.stderr)
        return 2
    print(json.dumps([t["task_file"] for t in write_tasks()], indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
