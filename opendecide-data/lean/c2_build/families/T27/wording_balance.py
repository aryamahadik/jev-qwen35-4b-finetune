"""T27 G11 generator fix, round 2 (PREREG A52 d; 16 Oct 2026): label-blind LEAST-LOADED wording choice per question form.

Why. G11 (spec 6.3) allows no wording above 2% of the family. The T27 full generation drew each wording by
`KitCtx.pick` = min over the stratum of uhash(row_key, "wording", skin_id): a seeded random draw per row. With W wordings
of one question form and R rows of that form, a random draw puts about R/W +- sqrt(R/W) rows on each wording, so the
largest wording sits 2-3 standard deviations above the mean (yn_beyond: 13 wordings, 523 rows, mean 40, max 60 = 2.5%).
Choosing the least-loaded wording keeps max - min of the rows per wording within the heaviest unit (4 rows), so the share
is the stratum mean + at most 4 rows. A balanced draw cannot beat the mean: ch_next has 17 usable training wordings for
1,256 rows (mean 73.9 = 3.08%), which is why new wordings are also needed (see diag_g11.py).

Rule (everything below is label-blind: it reads no gold, no option, no text):
  * stratum = (stream, qform). stream = seed // 1,000,000, so every build (candidates 7xM, QC, the A50 builds 11M/12M/13M,
    redraw offsets) has its own counters and the result does not depend on which build ran first in a process.
  * a base row (T27Plugin._pick_wording) books `1 + the rows its relations will emit` (complement, twin, equiv, inv,
    premise_removal: the unit size, a function of the spec only) to the chosen wording; a complement partner
    (pipeline.build_unit -> ctx.pick) books 1.
  * pick = the wording of the stratum with the smallest booked load; ties by the old uhash order (so an empty stratum
    reproduces the old behaviour). The pick is memoised per (row_key, qform): a repeated render of one row (G15, G-TW
    re-render) gets the same wording.
  * held-out wordings (sampler S5, mixdev only) keep the old min-hash draw, so mixdev_S5.jsonl is unchanged.
Independence of the label: a row's wording is a function of the rows booked before it (earlier seeds), never of its own
gold, so P(wording | gold) is the same for both golds (G6 / G7 see the same independence as before).

Used as: T27Plugin.ctx_for / _pick_wording delegate to ctx_for() / pick_wording() below (installed into plugin.py by
zed_orch/t27_fix_r2/install_code.py; until then zed_orch/t27_fix_r2/overlay.py patches the class in memory).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from c2_kit.distractors import uhash
from c2_kit.plugin import KitCtx

EMIT_KINDS = ("complement", "twin", "equiv", "inv", "premise_removal")   # relation kinds that add a row to the unit
STREAM = 1_000_000                                                       # seeds one build may use (gen_full_c2.SEED_SPAN)


def stream_of(row_key: str) -> int:
    """seed // 1,000,000 of a row key 'FAM|seed|sampler|qform' (0 when the key has another shape)."""
    try:
        return int(str(row_key).split("|")[1]) // STREAM
    except (IndexError, ValueError):
        return 0


class WordingBalancer:
    """Booked rows per (stream, qform, wording). One instance per plugin instance."""

    def __init__(self):
        self.load: dict = {}
        self.memo: dict = {}
        self.weight = 1                       # rows the NEXT pick books (set by pick_wording around one base pick)

    def choose(self, cands: list, row_key: str, qform: str | None):
        by_id = {s.skin_id: s for s in cands}
        mk = (row_key, qform)
        sid = self.memo.get(mk)
        if sid in by_id:
            return by_id[sid]
        lo = self.load.setdefault((stream_of(row_key), qform), {})
        best = min(cands, key=lambda s: (lo.get(s.skin_id, 0), uhash(row_key, "wording", s.skin_id)))
        lo[best.skin_id] = lo.get(best.skin_id, 0) + self.weight
        self.memo[mk] = best.skin_id
        return best

    def loads(self) -> dict:
        return {f"{k[0]}|{k[1]}": dict(v) for k, v in self.load.items()}


@dataclass
class BalancedKitCtx(KitCtx):
    """KitCtx whose pick() balances the (training) wordings; every other kind and every held-out pick is KitCtx.pick."""
    balancer: Any = None

    def pick(self, family: str, kind: str, row_key: str, *, register: str | None = None, qform: str | None = None,
             exclude: tuple = (), held_out: bool = False):
        if kind != "wording" or held_out or self.balancer is None:
            return super().pick(family, kind, row_key, register=register, qform=qform, exclude=exclude,
                                held_out=held_out)
        c = [s for s in self.skins.values() if s.family == family and s.kind == kind and not s.held_out
             and (register is None or s.register == register) and (qform is None or s.qform == qform)
             and s.skin_id not in exclude]
        if not c:
            raise LookupError(f"no {kind} for {family} (register={register}, qform={qform}, held_out={held_out})")
        return self.balancer.choose(c, row_key, qform)


def balancer_of(plugin) -> WordingBalancer:
    b = getattr(plugin, "_wording_balancer", None)
    if b is None:
        b = plugin._wording_balancer = WordingBalancer()
    return b


def ctx_for(plugin, spec, ctx):
    """T27Plugin.ctx_for with a balanced pick: the same skins as before (wordings that break the polarity rule and carrier
    skins that do not fit the spec are removed), in a BalancedKitCtx that shares the plugin's balancer."""
    bad = plugin.quarantined_wordings(ctx)
    fam = plugin.FAMILY
    skins = {sid: s for sid, s in ctx.skins.items() if sid not in bad
             and (not (s.family == fam and s.kind == "skin") or plugin.fits(s, spec))}
    return BalancedKitCtx(skins=skins, lexicon=ctx.lexicon, balancer=balancer_of(plugin))


def unit_rows(plugin, spec) -> int:
    """Rows the unit of a base row will hold: the base plus one per emitting relation (a function of the spec)."""
    return 1 + sum(1 for p in plugin.relations(spec) if p.kind in EMIT_KINDS)


def pick_wording(plugin, ctx, spec, key: str, held: bool):
    """T27Plugin._pick_wording: S5 prefers held-out wordings (old min-hash draw); training rows book the unit size."""
    bad = tuple(plugin.quarantined_wordings(ctx))
    if held:
        try:
            return ctx.pick(plugin.FAMILY, "wording", key, qform=spec.qform, held_out=True, exclude=bad)
        except LookupError:
            pass
    bal = getattr(ctx, "balancer", None)
    if bal is None:
        return ctx.pick(plugin.FAMILY, "wording", key, qform=spec.qform, exclude=bad)
    if (key, spec.qform) in bal.memo:                 # a repeated render of the same row: same wording, no new booking
        return ctx.pick(plugin.FAMILY, "wording", key, qform=spec.qform, exclude=bad)
    bal.weight = unit_rows(plugin, spec)
    try:
        return ctx.pick(plugin.FAMILY, "wording", key, qform=spec.qform, exclude=bad)
    finally:
        bal.weight = 1


def apply(plugin_cls) -> None:
    """In-memory install of the two delegating methods (what plugin.py holds after install_code.py)."""
    if getattr(plugin_cls, "_wording_balance_applied", False):
        return
    plugin_cls.ctx_for = lambda self, spec, ctx: ctx_for(self, spec, ctx)
    plugin_cls._pick_wording = lambda self, ctx, spec, key, held: pick_wording(self, ctx, spec, key, held)
    plugin_cls._wording_balance_applied = True
