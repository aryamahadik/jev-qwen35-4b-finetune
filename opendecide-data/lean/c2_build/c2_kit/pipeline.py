"""c2_kit/pipeline.py: one relation unit through every program gate, in memory (C2_DATA_SPEC 6.4 steps 5 and 7).

build_unit(plugin, spec, ctx) renders the base row and every relation partner the plugin proposes, and checks:
  G2      solver B on the parsed row == solver A, on every row                                  (100%)
  G3      plugin.parse(row) == plugin.canonical(spec), on every row                             (100%)
  G4      metamorphic proposals: solver A on the transformed spec == the predicted answer, and the transformed row
          passes G2 / G3 too                                                                    (100%)
  G-SL    gsl.check_row on every row                                                            (100%)
  G-LEX   every lexicon form a row uses is admitted; its wording is an admitted question form of its qform; and, for a
          plugin with POLARITY_CHECK, a yes/no wording reads with its form's polarity (c2_kit.polarity)  (100%)
  G-TW    relations.RelationEmitter checks on every twin / complement / equiv / inv            (100%)
  G15     formats-1 loader_check on every row (run_g15=False skips it for speed in unit tests)   (100%)
  schema  rows.validate_row; distractors.check_named on choice rows
Any failure drops the whole unit (UnitResult.ok False, problems tagged by gate): a generator bug is fixed in the
generator, never by editing rows. overlay_report() measures the spec 4.1 shares over many units.
Nothing is written: callers write rows only through paths.write_jsonl, which refuses before A38.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from . import gsl, polarity
from . import rows as R
from . import slots as S
from .distractors import abstain_cells, abstain_report, check_named, position_counts, rank_counts
from .lexicon import question_sem
from .plugin import ContractError, KitCtx, Spec, choose_forms
from .relations import GTWError, RelationEmitter, affected
from .skin import RenderError

RENDER_ERRORS = (RenderError, S.SlotError, ContractError, ValueError, KeyError)


@dataclass
class UnitResult:
    ok: bool
    rows: list = field(default_factory=list)
    rels: list = field(default_factory=list)
    problems: list = field(default_factory=list)      # (gate, detail)
    rendered: list = field(default_factory=list)


def check_rendered(plugin, spec: Spec, rr, ctx: KitCtx, *, run_g15: bool = True) -> list:
    probs = []
    gold = plugin.solve_a(spec)
    if rr.answer != gold:
        probs.append(("G2", f"row gold {rr.answer!r} != solver A {gold!r}"))
    try:
        view = plugin.parse(rr.row, ctx)
    except Exception as e:  # noqa: BLE001  (any parser failure is a G3 failure)
        probs.append(("G3", f"parse failed: {type(e).__name__}: {e}"))
        view = None
    if view is not None:
        want = plugin.canonical_for(spec, rr.row["meta"]["c2"]["author_mode"])
        facts = {k: v for k, v in view.items() if k != "options"}
        if facts != want:
            keys = sorted(k for k in set(facts) | set(want) if facts.get(k) != want.get(k))
            probs.append(("G3", f"parsed facts differ from the generator's on {keys}"))
        try:
            b = plugin.solve_b(view)
        except Exception as e:  # noqa: BLE001
            probs.append(("G2", f"solver B failed: {type(e).__name__}: {e}"))
        else:
            if b != gold:
                probs.append(("G2", f"solver B {b!r} != solver A {gold!r}"))
            if rr.row["qtype"] == "choice":
                keys = view.get("options")
                if not isinstance(keys, list) or len(keys) != len(rr.row["options"]):
                    probs.append(("G2", "parse() did not read the option texts back to keys"))
                elif len(set(map(repr, keys))) != len(keys):
                    probs.append(("G2", "two option texts parse to one key"))
                elif keys[rr.row["options"].index(rr.row["gold"])] != b:
                    probs.append(("G2", "the gold option text does not parse to solver B's answer"))
    probs += lex_problems(spec, rr, ctx)
    probs += polarity.row_problems(plugin, spec, rr, ctx)
    for v in gsl.check_row(rr, ctx, plugin, spec):
        probs.append(("G-SL", f"{v.rule}: {v.detail}"))
    for p in R.validate_row(rr.row):
        probs.append(("schema", p))
    if rr.option_set is not None:
        probs += [("options", p) for p in check_named(rr.option_set)]
    if run_g15:
        res = R.g15_check(rr.row)
        if not res["ok"]:
            probs += [("G15", p) for p in res["problems"]]
    return probs


def lex_problems(spec: Spec, rr, ctx: KitCtx) -> list:
    """G-LEX on one row: every lexicon form it uses is admitted, and its wording is an admitted question form whose
    meaning is the wording's question form."""
    if ctx.lexicon is None:
        return [("G-LEX", "no lexicon registry in the kit context")]
    probs = []
    g = ctx.lexicon.gate(rr.row["meta"]["c2"]["lexicon_ids"])
    if not g["pass"]:
        probs.append(("G-LEX", f"forms not admitted: {sorted(g['not_admitted']) + g['unknown']}"))
    if rr.wording_id:
        wd = ctx.skin(rr.wording_id)
        want = question_sem(spec.family, wd.qform)
        if wd.qform != spec.qform or not any(
                f in ctx.lexicon.forms and ctx.lexicon.forms[f].sem_id == want and ctx.lexicon.forms[f].text == wd.text
                and ctx.lexicon.status(f) == "admitted" for f in wd.lexicon_ids):
            probs.append(("G-LEX", f"wording {wd.skin_id} is not an admitted {want} form"))
    return probs


def _forms_for(spec: Spec, base_forms: dict, row_key: str, changed: set) -> dict:
    forms = dict(base_forms)
    fresh = choose_forms(spec, row_key + "|twin")
    for name, slot in spec.all_slots().items():
        if name not in forms or (name in changed and forms[name] not in S.forms(slot)):
            forms[name] = fresh[name]
    for name in list(forms):
        if name not in spec.all_slots():
            del forms[name]
    return forms


def build_unit(plugin, spec: Spec, ctx: KitCtx, *, row_key: str | None = None, run_g15: bool = True,
               skin=None, wording=None) -> UnitResult:
    key = row_key or f"{spec.family}|{spec.seed}|{spec.sampler}|{spec.qform}"
    if callable(getattr(plugin, "ctx_for", None)):        # a family whose skins have slot layouts (T27) narrows the
        ctx = plugin.ctx_for(spec, ctx)                   # pool, so an equiv partner never picks a skin that cannot fit
    res = UnitResult(ok=False)
    try:
        forms = choose_forms(spec, key)
        rr = plugin.render(spec, ctx, skin=skin, wording=wording, forms=forms)
    except RENDER_ERRORS as e:
        res.problems.append(("render", f"base: {type(e).__name__}: {e}"))
        return res
    res.rendered.append(rr)
    res.problems += check_rendered(plugin, spec, rr, ctx, run_g15=run_g15)
    if res.problems:
        return res
    em = RelationEmitter(plugin)
    em.base(rr)
    sk = ctx.skin(rr.skin_id)
    wd = ctx.skin(rr.wording_id) if rr.wording_id else None
    for prop in plugin.relations(spec):
        try:
            if prop.kind == "complement":
                s2 = spec.replace(qform=prop.qform)
                w2 = ctx.pick(spec.family, "wording", key, qform=prop.qform, held_out=bool(wd and wd.held_out))
                r2 = plugin.render(s2, ctx, skin=sk, wording=w2, forms=rr.forms)
                gate_probs = check_rendered(plugin, s2, r2, ctx, run_g15=run_g15)
                if not gate_probs:
                    em.complement(rr, r2, spec)
            elif prop.kind in ("twin", "premise_removal"):
                s2 = plugin.derive(prop.spec)
                f2 = _forms_for(s2, rr.forms, key, affected(s2, {prop.changed_slot}))
                r2 = plugin.render(s2, ctx, skin=sk, wording=wd, forms=f2)
                gate_probs = check_rendered(plugin, s2, r2, ctx, run_g15=run_g15)
                if not gate_probs and prop.kind == "twin":
                    em.twin(rr, r2, spec, s2, prop.changed_slot, prop.expect)
                elif not gate_probs:
                    em.premise_removal(rr, r2, spec, s2, prop.changed_slot, prop.expect)
            elif prop.kind == "equiv":
                s2 = prop.spec or spec
                sk2 = ctx.pick(spec.family, "skin", key + "|equiv", register=prop.register, exclude=(sk.skin_id,),
                               held_out=sk.held_out)
                r2 = plugin.render(s2, ctx, skin=sk2, wording=wd, forms=rr.forms)
                gate_probs = check_rendered(plugin, s2, r2, ctx, run_g15=run_g15)
                if not gate_probs:
                    em.equiv(rr, r2, spec, s2)
            elif prop.kind == "inv":
                at = ctx.skin(prop.attack) if prop.attack else ctx.pick(spec.family, "attack", key)
                r2 = plugin.render(spec, ctx, skin=sk, wording=wd, forms=rr.forms, attack=at)
                gate_probs = check_rendered(plugin, spec, r2, ctx, run_g15=run_g15)
                if not gate_probs:
                    em.inv(rr, r2, spec)
            else:  # metamorphic (G4): checked, never emitted
                s2 = plugin.derive(prop.spec)
                want = plugin.solve_a(spec) if prop.expect in (None, "same") else prop.expect
                got = plugin.solve_a(s2)
                gate_probs = [] if got == want else [("G4", f"{prop.note or 'metamorphic'}: {got!r} != {want!r}")]
                f2 = _forms_for(s2, rr.forms, key, set(s2.all_slots()))
                r2 = plugin.render(s2, ctx, skin=sk, wording=wd, forms=f2)
                gate_probs += [("G4", f"{g}: {p}") for g, p in check_rendered(plugin, s2, r2, ctx, run_g15=False)]
            res.problems += [(g, f"{prop.kind}: {p}") for g, p in gate_probs]
        except GTWError as e:
            res.problems.append(("G-TW", str(e)))
        except RENDER_ERRORS as e:
            res.problems.append(("render", f"{prop.kind}: {type(e).__name__}: {e}"))
        except LookupError as e:
            res.problems.append(("ctx", f"{prop.kind}: {e}"))
    if res.problems:
        return res
    try:
        res.rows, res.rels = em.finalize()
    except GTWError as e:
        res.problems.append(("G-TW", str(e)))
        return res
    for r in res.rows:
        res.problems += [("schema", f"{r['id']}: {p}") for p in R.validate_row(r)]
    res.rendered = [em.rows[i] for i in em.order]
    res.ok = not res.problems
    return res


def overlay_report(units: list, plugin) -> dict:
    """Spec 4.1 shares over passed units (complement >= 20% of yes/no rows, >= 30% non-syntactic, twins 20-25%,
    equiv 5-10%, attack about 5% of agent-tier rows) + abstain (overall and per (k, shown) cell), gold-position and
    gold-rank (ordered sets) balance."""
    rows = [r for u in units if u.ok for r in u.rows]
    rels = [x for u in units if u.ok for x in u.rels]
    yn = [r for r in rows if r["qtype"] == "noul"]
    comp_ids = {x["a"] for x in rels if x["type"] == "complement"} | {x["b"] for x in rels if x["type"] == "complement"}
    by_id = {r["id"]: r for r in rows}
    comp_partners = [by_id[x["b"]] for x in rels if x["type"] == "complement"]
    nonsyn = sum(1 for r in comp_partners
                 if plugin.QFORMS[r["meta"]["qform"]].complement_kind not in (None, "syntactic")
                 or plugin.QFORMS[by_id[_partner(rels, r["id"])]["meta"]["qform"]].complement_kind
                 not in (None, "syntactic"))
    n = len(rows) or 1
    sets = [rr.option_set for u in units if u.ok for rr in u.rendered if rr.option_set is not None]
    return {"rows": len(rows), "yes_no": len(yn),
            "complement_share_of_yes_no": (len(comp_ids & {r["id"] for r in yn}) / len(yn)) if yn else None,
            "complement_pairs": len(comp_partners),
            "non_syntactic_share_of_pairs": (nonsyn / len(comp_partners)) if comp_partners else None,
            "twin_share": sum(1 for r in rows if r["meta"]["twin_kind"] == "minimal_edit") / n,
            "equiv_share": sum(1 for r in rows if r["meta"]["twin_kind"] == "equiv") / n,
            "attack_share": sum(1 for r in rows if r["meta"]["twin_kind"] == "attack") / n,
            "yes_rate": (sum(r["gold"] for r in yn) / len(yn)) if yn else None,
            "abstain": abstain_report(sets), "abstain_cells": abstain_cells(sets),
            "gold_positions": position_counts(sets), "gold_ranks": rank_counts(sets)}


def _partner(rels: list, rid: str) -> str:
    for x in rels:
        if x["type"] == "complement" and x["b"] == rid:
            return x["a"]
    raise KeyError(rid)
