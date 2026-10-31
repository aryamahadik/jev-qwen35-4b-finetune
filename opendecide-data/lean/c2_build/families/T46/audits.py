"""families/T46/audits.py: the A42-D 3.3 reseed audit, the held-out checks and the shape audits of T46.

  reseed_audit(plugin, ctx, specs, frac, seed)   a seeded `frac` of the specs is regenerated from the same plan (workflow,
                                                 arm, card, display, class, special type) with independent facts (phrasing,
                                                 flags, numbers, names, note, field order); the new row is rendered, parsed
                                                 and solved by B. Label flips (class changed, or B != A) <= 1%; with < 100
                                                 audited rows: 0.
  heldout_check(plugin, n)                       training samplers never draw the dev workflow skin, a dev layout, a dev
                                                 name or a dev gloss; S5 does.
  state_leak_check(rows)                         no label word of any set, and no class word, in any `state` field.
"""
from __future__ import annotations

import random

from . import haiku_author as HA
from . import tables as T


def reseed_audit(plugin, ctx, specs, frac: float = 0.03, seed: int = 20261015) -> dict:
    R = random.Random(seed)
    k = max(1, int(round(frac * len(specs))))
    pick = R.sample(range(len(specs)), min(k, len(specs)))
    flips, b_flips, errs, none = [], [], [], 0
    for n, i in enumerate(pick):
        sp = specs[i]
        ns = plugin.reseed(sp, 777 + n)
        if ns is None:
            none += 1
            continue
        try:
            if plugin.solve_class(ns) != sp.structure["cls"]:
                flips.append((sp.seed, sp.sampler))
                continue
            rr = plugin.render(ns, plugin.ctx_for(ns, ctx))
            if plugin.solve_b(plugin.parse(rr.row, ctx)) != plugin.solve_a(ns):
                b_flips.append((sp.seed, sp.sampler))
        except Exception as e:  # noqa: BLE001
            errs.append(f"{type(e).__name__}: {str(e)[:80]}")
    n = len(pick)
    limit = 0 if n < 100 else int(0.01 * n)
    return {"audited": n, "no_draw": none, "flips": len(flips), "b_flips": len(b_flips), "errors": len(errs),
            "limit": limit, "pass": len(flips) <= limit and not b_flips and not errs, "examples": flips[:3],
            "error_examples": errs[:3]}


def heldout_check(plugin, n: int = 300) -> dict:
    train_hits = s5_hits = s5_dev_wf = 0
    for sampler in ("S1", "S2", "S3", "S4", "S5"):
        for seed in range(n if sampler != "S5" else n // 2):
            try:
                sp = plugin.sample(6_000_000 + seed, sampler)
            except Exception:  # noqa: BLE001
                continue
            hit = sp.structure["wf"] in T.DEV_WORKFLOWS or sp.structure["dev"]
            if sampler == "S5":
                s5_hits += bool(hit)
                s5_dev_wf += sp.structure["wf"] in T.DEV_WORKFLOWS
            else:
                train_hits += bool(hit)
    return {"train_samplers_dev_rows": train_hits, "s5_dev_rows": s5_hits, "s5_dev_workflow_rows": s5_dev_wf,
            "pass": train_hits == 0 and s5_hits > 0 and s5_dev_wf > 0}


def state_leak_check(rows) -> dict:
    words = set()
    for t in HA.ALL_LABEL_STRINGS:
        words.add(t)
    bad = []
    for r in rows:
        low = r["state"].lower()
        for w in words:
            if " " in w or "_" in w:
                continue
            import re
            if re.search(r"(?<![a-z0-9_])" + re.escape(w) + r"(?![a-z0-9_])", low):
                bad.append((r["id"], w))
                break
    return {"rows": len(rows), "leaks": len(bad), "examples": bad[:3], "pass": not bad}


def g5h_sample(rows, n: int, seed: str) -> list:
    """The G5-H read order of T46 (A59 (e)): the first `n` rows of the returned order hold >= 30 Arabic rows and >= 120 rows without
    printed meanings (when the candidates have that many), the rest in the kit's seeded order (g5h.sample_rows)."""
    from c2_kit import g5h
    base = g5h.sample_rows(rows, len(rows), seed)
    ar = [r for r in base if (r.get("meta") or {}).get("lang_state") == "ar"][:30]
    taken = {r["id"] for r in ar}
    nodef_have = sum(1 for r in ar if not (r["meta"].get("t46") or {}).get("defs"))
    nodef = [r for r in base if r["id"] not in taken and not (r["meta"].get("t46") or {}).get("defs")][:max(0, 120 - nodef_have)]
    taken |= {r["id"] for r in nodef}
    rest = [r for r in base if r["id"] not in taken]
    return ar + nodef + rest
