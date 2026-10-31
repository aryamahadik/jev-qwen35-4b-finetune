"""families/T24/balance_check.py: the ch_v2 gold-role balance of a run of seeds, in memory (G0 v2.2 section 2 Balance;
PILOT_VERDICT F3). The role is the outcome under the revised version; a row's option bucket is its option count k (2:
pos / neg; 3: pos / alt / neg, when either version holds a condition clause).

  bases      every ch_v2 base row the samplers draw
  equiv      the equiv partners of those bases (same facts: the same role again; EQUIV_RATE of the bases)
  twins      the minimal-edit twins of ch_v2 bases (plugin.twin; TWIN_RATE of the bases, when a candidate exists)
  all        bases + equiv + twins: the choice rows of a run, which is what G6 and G10 see

Also P(the outcome changes | role) over the bases (G0 Balance: 0.45-0.55 for pos and neg). No gate runs and nothing is
written; render and the pipeline add no further drop (0 units dropped in the pilot).

  ../../.venv/bin/python -B families/T24/balance_check.py [n_seeds]        (from lean/c2_build)
"""
from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit.distractors import uhash  # noqa: E402
from families.T24 import plugin as T  # noqa: E402


def option_bucket(spec) -> int:
    return 3 if "alt" in (set(spec.structure["v1"]) | set(spec.structure["v2"])) else 2


def choice_role_report(plugin, n_seeds: int = 1500, samplers=T.TRAIN_SAMPLERS, seed0: int = 0) -> dict:
    """Role counts by option bucket for bases, equiv partners, twins and all choice rows, plus P(change | role)."""
    cnt = {w: collections.Counter() for w in ("bases", "equiv", "twins")}
    chg = collections.Counter()
    for seed in range(seed0, seed0 + n_seeds):
        for smp in samplers:
            spec = plugin.sample(seed, smp)
            if spec.qform != "ch_v2":
                continue
            k, role = option_bucket(spec), T.outcome_a(spec, 2)
            cnt["bases"][(k, role)] += 1
            chg[(k, role, int(T.outcome_a(spec, 1) != T.outcome_a(spec, 2)))] += 1
            if uhash(T.FAMILY, "equiv", spec.sampler, spec.seed) < T.EQUIV_RATE:
                cnt["equiv"][(k, role)] += 1
            if uhash(T.FAMILY, "twin", spec.sampler, spec.seed) < T.TWIN_RATE:
                prop = plugin.twin(spec)
                if prop is not None:
                    cnt["twins"][(k, prop.expect)] += 1
    out = {}
    for which in ("bases", "equiv", "twins", "all"):
        c = cnt["bases"] + cnt["equiv"] + cnt["twins"] if which == "all" else cnt[which]
        out[which] = {}
        for k in (2, 3):
            tot = sum(v for (kk, _r), v in c.items() if kk == k)
            out[which][k] = {"n": tot, **{r: round(c[(k, r)] / tot, 4) if tot else None
                                          for r in (("pos", "neg") if k == 2 else T.ROLES)}}
    out["p_change_given_role"] = {
        f"{k}/{r}": round(chg[(k, r, 1)] / max(1, chg[(k, r, 0)] + chg[(k, r, 1)]), 4)
        for k in (2, 3) for r in (("pos", "neg") if k == 2 else T.ROLES)}
    out["p_change_given_role_any_k"] = {
        r: round(sum(chg[(k, r, 1)] for k in (2, 3)) / max(1, sum(chg[(k, r, c)] for k in (2, 3) for c in (0, 1))), 4)
        for r in T.ROLES}
    return out


def main(argv=None) -> int:
    n = int((argv or sys.argv[1:] or [1500])[0])
    print(json.dumps(choice_role_report(_plugin(), n), indent=1))
    return 0


def _plugin():
    """The plugin over the frozen pool and its lexicon (the sampler needs the admitted clause forms)."""
    import pilot_loaders as PL
    with PL.open_family("T24") as kit:
        return kit.plugin


if __name__ == "__main__":
    raise SystemExit(main())
