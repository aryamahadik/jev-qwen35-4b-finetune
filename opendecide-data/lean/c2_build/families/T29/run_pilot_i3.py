"""c2_build/families/T29/run_pilot_i3.py: the T29 pilot of fix iteration 3 (A44 a), into pilot_i3/.

A copy of run_pilot_i2.py (same pilot code: pilot.run_family with the family folder presented as one whose "pilot" folder is
"pilot_i3"; same loader pilot_loaders._t29 plus the pools/dneg/ supplement; same seeds and bars) with one addition: A44 (a) says
a family's pilot excludes its zed_orch/a43f_quarantine.json forms, so the pilot equals what full generation will produce. The
T29 form ids listed there are removed from the lexicon registry the plugin and the kit context use, and every wording skin that
names one is dropped from the skin pool (generation never draws them; the plugin's double-negation form stays off when none
is left). It never answers a Haiku task and never runs a model.

  ../.venv/bin/python -B families/T29/run_pilot_i3.py [--dry-run] [--n 1000] [--g6]        (from lean/c2_build)
Run it under two PYTHONHASHSEED values and compare rows_sha256 / relations_sha256 (--dry-run prints them instead of writing).
"""
from __future__ import annotations

import argparse
import contextlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import dataclasses  # noqa: E402
import time  # noqa: E402

import pilot as PI  # noqa: E402
import pilot_loaders as PL  # noqa: E402

OUT = "pilot_i3"
QUARANTINE = C2_BUILD / "zed_orch" / "a43f_quarantine.json"


def with_dneg(kit):
    """The kit plus the pools/dneg/ supplement (fix iteration 2): its lexicon_merged.json replaces redo2's registry and its
    wordings.jsonl adds the admitted double-negation wording skins. pilot_loaders._t29 does not read it (pinned), so this
    driver does. No supplement folder (before stage 3): the kit is returned unchanged. Pool files are sha-checked."""
    pool = Path(PL.family_dir("T29")) / "pools" / "dneg"
    if not (pool / "MANIFEST.json").is_file():
        return kit
    from families.T29 import plugin as P
    man = PL.safe_json(pool / "MANIFEST.json")
    PL.check_shas(pool, man["pool_files"], ("wordings.jsonl", "lexicon_merged.json"))
    reg = PL.LexiconRegistry.from_json(PL.safe_json(pool / "lexicon_merged.json"))
    skins = dict(kit.ctx.skins)
    for w in PL.safe_jsonl(pool / "wordings.jsonl"):
        if w.get("status", "admitted") == "admitted" and PL.admitted(reg, w["form_id"]):
            sid = f"T29-WD-{w['form_id']}"
            skins[sid] = PL.wording_skin("T29", sid, w, reg)
    return dataclasses.replace(kit, plugin=P.T29Plugin(lexicon=reg), ctx=PL.KitCtx(skins=skins, lexicon=reg),
                               loader=kit.loader + " + pools/dneg/ (run_pilot_i3)", pools=kit.pools + " + pools/dneg/")


def quarantined_ids() -> set:
    return set(json.loads(QUARANTINE.read_text()).get("T29", []))


def without_quarantine(kit):
    """A44 (a): drop the a43f-quarantined T29 forms (registry, wording skins) and rebuild the plugin's pool-derived state."""
    bad = quarantined_ids()
    regs = {id(r): r for r in (getattr(kit.plugin, "lexicon", None), getattr(kit.ctx, "lexicon", None)) if r is not None}
    gone = set()
    for reg in regs.values():
        for fid in sorted(bad & set(reg.forms)):
            del reg.forms[fid]
            gone.add(fid)
        reg._rx.clear()
    skins = {sid: s for sid, s in kit.ctx.skins.items() if not (bad & set(getattr(s, "lexicon_ids", ()) or ()))}
    dropped = len(kit.ctx.skins) - len(skins)
    kit.plugin._forms_cache.clear()
    if hasattr(kit.plugin, "_prec_cache"):
        del kit.plugin._prec_cache
    from families.T29 import plugin as P
    kit.plugin.dneg_ok = kit.plugin._clean_forms(P.DNEG_FORM)
    print(f"T29 a43f quarantine: {len(gone)} forms removed from the registry, {dropped} wording skins dropped "
          f"(listed {len(bad)}); dneg wording available: {kit.plugin.dneg_ok}", file=sys.stderr, flush=True)
    return dataclasses.replace(kit, ctx=PL.KitCtx(skins=skins, lexicon=kit.ctx.lexicon))


class _Dir:
    """The family dir as run_family sees it: dir / "pilot" is the iteration's folder."""

    def __init__(self, base: Path):
        self.base = base

    def __truediv__(self, name):
        return self.base / (OUT if name == "pilot" else name)

    def __fspath__(self):
        return str(self.base)

    def __str__(self):
        return str(self.base)


def g6_at_size(n: int) -> int:
    """zed_orch/g6_at_size.py with this driver's loader (so the supplement and the quarantine are in the build)."""
    t0 = time.time()
    with PL.open_family("T29") as kit:
        b = PI.build_pilot(kit, n, run_g15=False)
        g6, g7, g10 = PI.g6(b.infos), PI.g7(b.infos), PI.g10(b.infos, b.units, kit.plugin)
    cells = {}
    for part in ("yes_no", "choice"):
        p = g6.get(part) or {}
        if p.get("n"):
            cells[part] = {"n": p["n"], "chance": p["chance"], "max": max(
                (p[v][m], v, m) for v in p if isinstance(p[v], dict) and "lr" in p[v] for m in ("lr", "gbt"))}
    out = {"family": "T29", "n_rows": len(b.infos), "seconds": round(time.time() - t0), "seed_base": PI.SEED_BASE,
           "G6_verdict": g6["verdict"], "G6_fails": g6["fails"], "G6_cells_max": cells,
           "G7_verdict": g7.get("verdict"), "G10_verdict": g10.get("verdict"),
           "G10_fails": {k: v for k, v in (g10.get("checks") or {}).items() if v.get("verdict") == "fail"},
           "G10_checks": {k: v.get("value") for k, v in (g10.get("checks") or {}).items()}}
    dest = Path(PL.family_dir("T29")) / OUT
    dest.mkdir(exist_ok=True)
    (dest / f"G6_AT_{n}.json").write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps({k: out[k] for k in ("family", "n_rows", "G6_verdict", "G7_verdict", "G10_verdict", "seconds")}))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--n", type=int, default=PI.N_ROWS)
    ap.add_argument("--g6", action="store_true",
                    help="A43 G6 at --n rows: in-memory build, G15 off, G6/G7/G10; writes pilot_i3/G6_AT_<n>.json")
    ap.add_argument("--gates", default="", help="comma list of gate names whose full report is printed (e.g. G6,G10)")
    a = ap.parse_args(argv)
    orig = PL.open_family

    @contextlib.contextmanager
    def patched(fid):
        with orig(fid) as kit0:
            kit = without_quarantine(with_dneg(kit0))
            kit.dir = _Dir(kit.dir)
            yield kit

    PL.open_family = patched
    if a.g6:
        try:
            return g6_at_size(a.n)
        finally:
            PL.open_family = orig
    try:
        rep = PI.run_family("T29", a.n, write=not a.dry_run, run_g15=True,
                            log=lambda m: print(m, file=sys.stderr, flush=True))
    finally:
        PL.open_family = orig
    for g in [x for x in a.gates.split(",") if x]:
        print(f"=== {g}\n" + json.dumps(rep["gates"][g], indent=1, ensure_ascii=False, default=str))
    print(json.dumps({"summary": rep["summary"], "gate_lines": rep["gate_lines"],
                      "rows_sha256": rep["files"]["rows_sha256"], "relations_sha256": rep["files"]["relations_sha256"],
                      "n_rows": rep["files"]["n_rows"], "written": rep["written"]}, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
