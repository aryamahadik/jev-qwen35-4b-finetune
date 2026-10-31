"""A55 (d2, d3): the dev-only overlay of the S5 mixdev rebuild (the a54_heldout_overlay pattern).

The overlay is ACTIVE ONLY INSIDE the mixdev rebuild tool (`with a55_overlay.patched(fam, report): ...`). It edits no pool,
no plugin file and nothing the sealed mode reads: it adds the FROZEN dev-only forms of zed_orch/a55_dev/<FAM>/FROZEN.json
to the lexicon registry of the opened kit IN MEMORY (reg.add, held_out=True, the G-LEX unit test and the stored extraction
votes, so each form is `admitted`), and shadows ONE method of the plugin INSTANCE so the S5 sampler draws them:

  T24  admitted_forms(sem)       dev forms of a sem when >= 4 are admitted, else the training forms
  T06  _policy_clause(sem, rng)  same (the notice form of a policy sem)
  T07  nothing to shadow         T07Plugin._form_ids already takes the held-out forms of a sem for S5 when it has any, so the
                                 overlay only adds forms for the sems with >= 4 admitted and clears the plugin's cache
  T25  _pick_wording(ctx, spec, key)   dev wording skins (held_out=True) for a question form with >= 4 admitted, else training

A sem (rule forms) or a question form (wordings) with fewer than 4 admitted dev forms keeps its training forms in dev; its hits
bind (ruling (d2)/(d3)). The instance shadows are removed on exit; the registry additions die with the kit.
The sha256 of this file goes into the A55 addendum.
"""
from __future__ import annotations

import contextlib
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2B = HERE.parent
for _p in (str(C2B), str(HERE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
sys.dont_write_bytecode = True

import pilot_loaders as PL  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit.lexicon import question_sem  # noqa: E402

MIN_ADMITTED = 4
RULE_FAMILIES = ("T24", "T06", "T07")
WORDING_FAMILIES = ("T25",)
FAMS = RULE_FAMILIES + WORDING_FAMILIES


def dev_dir(fam: str) -> Path:
    """c2_build/zed_orch/a55_dev/<FAM>/: outside the family folder, because the families' own tests and freeze validators police that
    folder (T24 test_tests_write_no_file lists its entries; T06 test_freeze_v2 flags a stray haiku/*/answers round)."""
    return HERE / "a55_dev" / fam


def load_frozen(fam: str, root: Path | None = None) -> dict | None:
    p = (root or dev_dir(fam)) / "FROZEN.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None


def _add_forms(reg, fam: str, forms: list) -> dict:
    """reg.add every frozen form (held_out=True), unit-test it and record its stored extractions. Returns {unit: [form ids]}."""
    ids: dict = {}
    for f in forms:
        sem = f["sem_id"]
        fo = reg.add(f["text"], sem, slots=dict(f["slots"]), source="haiku", family=fam, haiku_task_id=f["haiku_task_id"],
                     haiku_prompt_sha=f["haiku_prompt_sha"], held_out=True)
        if fo.form_id != f["form_id"]:
            raise RuntimeError(f"{fam}: dev form id drift {f['form_id']} -> {fo.form_id}")
        ids.setdefault(sem, []).append(fo.form_id)
    for fids in ids.values():
        for fid in fids:
            reg.unit_test(fid)
    for f in forms:
        for ex, sem in f["extractions"]:
            reg.record_extraction(f["form_id"], ex, sem)
    for sem, fids in ids.items():
        bad = [fid for fid in fids if reg.status(fid) != "admitted"]
        if bad:
            raise RuntimeError(f"{fam}: frozen dev forms not admitted in the registry: {bad[:3]}")
        fids.sort()
    return ids


def add_to_kit(fam: str, kit, root: Path | None = None) -> dict:
    """Add the frozen dev-only items of `fam` to the opened kit (in memory) and shadow the plugin hook. Returns the record
    {"frozen_sha256", "units_used", "units_skipped", "forms"}; {} when the family has no overlay or nothing is frozen."""
    if fam not in FAMS:
        return {}
    fr = load_frozen(fam, root)
    if fr is None:
        return {"frozen": False}
    if fr.get("INCOMPLETE"):
        raise RuntimeError(f"{fam}: FROZEN.json is INCOMPLETE (G-LEX answers missing: {fr.get('answer_files_missing')}); score again first")
    plugin, ctx = kit.plugin, kit.ctx
    reg = ctx.lexicon
    used = {u for u, d in fr["units"].items() if d.get("used")}
    forms = [f for f in fr["forms"] if f.get("unit", f["sem_id"]) in used]
    rec = {"frozen": True, "frozen_sha256": fr.get("self_sha256"), "units_used": sorted(used),
           "units_skipped": sorted(set(fr["units"]) - used), "forms": len(forms)}
    shadows = getattr(kit, "_a55_shadows", None)
    if shadows is None:
        shadows = []
        try:
            kit._a55_shadows = shadows                  # FamilyKit is a plain dataclass: an extra attribute is fine
        except Exception:                                # noqa: BLE001
            pass

    def shadow(name, fn):
        had = name in plugin.__dict__
        old = plugin.__dict__.get(name)
        setattr(plugin, name, fn)
        shadows.append((name, had, old))

    if fam in RULE_FAMILIES:
        ids = _add_forms(reg, fam, forms)
        if fam == "T24":
            orig = plugin.admitted_forms

            def admitted_forms(sem, _o=orig, _ids=ids):
                dev = _ids.get(sem)
                return list(dev) if dev and len(dev) >= MIN_ADMITTED else _o(sem)
            shadow("admitted_forms", admitted_forms)
            plugin._form_cache = {}
        elif fam == "T06":
            orig = plugin._policy_clause
            mod = sys.modules[type(plugin).__module__]

            def _policy_clause(sem, rng, _o=orig, _ids=ids, _mod=mod):
                dev = _ids.get(sem)
                if dev and len(dev) >= MIN_ADMITTED:
                    fid = dev[0] if rng is None else rng.choice(dev)
                    return reg.clause(fid, bind={"P": "P_DAYS"} if sem in _mod.WINDOWED else {})
                return _o(sem, rng)
            shadow("_policy_clause", _policy_clause)
        elif fam == "T07":
            if hasattr(plugin, "_fids"):
                plugin._fids.clear()
        rec["dev_forms_by_unit"] = {s: len(v) for s, v in sorted(ids.items())}
        return rec
    # ---- T25: dev-only question wordings --------------------------------------------------------------------------------
    ids = {}
    for f in forms:
        qf = f["qform"]
        fo = reg.add(f["text"], question_sem(fam, qf), slots=dict(f["slots"]), source="haiku", family=fam,
                     haiku_task_id=f["haiku_task_id"], haiku_prompt_sha=f["haiku_prompt_sha"], held_out=True)
        if fo.form_id != f["form_id"]:
            raise RuntimeError(f"{fam}: dev wording id drift {f['form_id']} -> {fo.form_id}")
        ids.setdefault(qf, []).append((fo.form_id, f))
    for lst in ids.values():
        for fid, _f in lst:
            reg.unit_test(fid)
    for lst in ids.values():
        for fid, f in lst:
            for ex, sem in f["extractions"]:
                reg.record_extraction(fid, ex, sem)
    n = 0
    for qf, lst in sorted(ids.items()):
        for fid, f in sorted(lst):
            if reg.status(fid) != "admitted":
                raise RuntimeError(f"{fam}: frozen dev wording not admitted: {fid}")
            sid = f"{fam}-WD-{fid}"
            ctx.skins[sid] = K.make_skin(sid, fam, f["text"], dict(reg.forms[fid].slots), kind="wording", register="question",
                                         qform=qf, held_out=True, lexicon_ids=(fid,), haiku_task_id=f["haiku_task_id"],
                                         haiku_prompt_sha=f["haiku_prompt_sha"])
            n += 1
    dev_q = {qf for qf, lst in ids.items() if len(lst) >= MIN_ADMITTED}
    orig = plugin._pick_wording

    def _pick_wording(ctx_, spec, key, _o=orig, _q=dev_q):
        if spec.sampler in plugin.HELD_OUT_SAMPLERS and spec.qform in _q:
            return ctx_.pick(fam, "wording", key, qform=spec.qform, held_out=True)
        return _o(ctx_, spec, key)
    shadow("_pick_wording", _pick_wording)
    rec["dev_forms_by_unit"] = {qf: len(lst) for qf, lst in sorted(ids.items())}
    rec["skins_added"] = n
    return rec


def remove_shadows(kit) -> None:
    for name, had, old in reversed(getattr(kit, "_a55_shadows", [])):
        if had:
            setattr(kit.plugin, name, old)
        else:
            kit.plugin.__dict__.pop(name, None)
    if hasattr(kit, "_a55_shadows"):
        kit._a55_shadows.clear()


@contextlib.contextmanager
def patched(fam: str, report: dict | None = None, root: Path | None = None):
    """Wrap pilot_loaders.open_family so the kit of `fam` opens with the frozen dev-only items added (compose with the A54
    overlay by entering it inside / outside this one). Inactive for any other family, with A55_NO_OVERLAY=1, or when
    nothing is frozen."""
    if fam not in FAMS or os.environ.get("A55_NO_OVERLAY") == "1":
        yield
        return
    orig = PL.open_family

    @contextlib.contextmanager
    def opened(fid):
        with orig(fid) as kit:
            try:
                if fid == fam:
                    r = add_to_kit(fam, kit, root)
                    if report is not None:
                        report.update(r)
                yield kit
            finally:
                if fid == fam:
                    remove_shadows(kit)
    PL.open_family = opened
    try:
        yield
    finally:
        PL.open_family = orig
