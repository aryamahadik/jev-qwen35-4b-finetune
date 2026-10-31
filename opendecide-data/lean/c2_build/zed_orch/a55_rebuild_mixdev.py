"""A55 (d): rebuild ONLY a family's S5 mixdev (spec 7.1) under the dev-only overlay and the d1 rule; candidates stay untouched.

The A54 method extended (a54_rebuild_mixdev.py is not edited): same mixdev seed base (GEN_REPORT seeds.mixdev), 150 rows, same S5
frames / skins / registers / packs, the G5-H / G3-H quarantined templates stay out, exclusions and dead-qform redraws as
gen_full_c2.run. On top of that:

  d1  every dev unit is checked against the family's candidates (a55_common.CandIndex): a numeral-bearing state line equal to a
      candidate line (declared rule), an opaque id token that also occurs in the candidates, and (level "item", the default)
      a numeral-bearing A53 item shared with the candidates that A53 would not waive. A colliding unit is redrawn from its own
      seeded stream (seed + j * D1_STRIDE, j = 1 .. 16; the sampler and the seed's block position and card are kept); the
      first redraw that passes every gate and collides with nothing replaces it; after 16 tries the unit stays as drawn and its
      hits bind. The solver recomputes every gold. Nothing reads a G13 log or the binding-unit list.
  d2  / d3  (families T24 T06 T07 / T25) the frozen dev-only forms or wordings through a55_overlay (active only here).
              If the overlay breaks the A53 precondition, it is reverted for that family and d1 is kept.

Checks after each rebuild (the ruling's list): generator files unchanged (sha256 before / after), the A53 precondition (0
shared), the dev-row program checks (every dev unit passed G2 solver B / G3 / G4 / G-SL / G-LEX / G-TW / G15 / schema in
pipeline.build_unit; the written rows are re-checked with solver B and the schema), and, with --verify-candidates, the training
digests (a54_verify_candidates: the candidates re-derive byte-identical). The old mixdev goes to
data/c2_parts/<FAM>/out/_superseded_a55/ (a copy in zed_orch/g13_attr/_backup/a55/<FAM>/); the new sha256 goes into QC_REPORT
(the old one as mixdev_pre_a55), MANIFEST, GEN_REPORT and DROPS.

Run from lean/c2_build:
  ../../.venv/bin/python -B zed_orch/a55_rebuild_mixdev.py T23 --check-only [--out-dir DIR] [--level item|line] [--no-d1]
  ../../.venv/bin/python -B zed_orch/a55_rebuild_mixdev.py T23 --write [--verify-candidates]
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2B = HERE.parent
for _p in (str(C2B), str(HERE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
sys.dont_write_bytecode = True

import a54_heldout_overlay as OV54  # noqa: E402
import a55_common as C  # noqa: E402
import a55_overlay as OV55  # noqa: E402
import gen_full_c2 as G  # noqa: E402
import qc_full_c2 as Q  # noqa: E402
import g13_c2 as X  # noqa: E402
from c2_kit import paths, pipeline  # noqa: E402
from c2_kit import rows as R  # noqa: E402


# ================================================================================================ the d1 build
def build_mixdev_d1(kit, n: int, seed_base: int, cand: "C.CandIndex | None", level: str = "item", tries: int = C.D1_TRIES,
                    stride: int = C.D1_STRIDE) -> tuple:
    """gen_full_c2.build_mixdev with the d1 redraw. cand None = no d1 (identical to build_mixdev). Returns (rows, report)."""
    plugin, ctx = kit.plugin, kit.ctx
    held = tuple(plugin.HELD_OUT_SAMPLERS)
    if not held:
        return [], {"note": "no held-out sampler"}
    rows, drops, k = [], Counter(), 0
    st = Counter()
    tries_hist = Counter()
    while len(rows) < n and k < 40 * n:
        seed, sampler = seed_base + k // len(held), held[k % len(held)]
        k += 1
        first = None
        for j in range(0, (tries if cand is not None else 0) + 1):
            try:
                res = pipeline.build_unit(plugin, plugin.sample(seed + j * stride, sampler), ctx, run_g15=True)
            except Exception as e:  # noqa: BLE001
                if j == 0:
                    drops[type(e).__name__] += 1
                    break                                      # an original draw that raises is dropped, as in A54
                st["redraw_exception"] += 1
                st["redraw_exception:" + type(e).__name__] += 1
                continue
            if not res.ok:
                if j == 0:
                    for g in {g for g, _ in res.problems}:
                        drops[g] += 1
                    break                                      # an original draw that fails a gate is dropped, as in A54
                st["redraw_failed_gate"] += 1
                continue
            col = [cand.collisions(r, level) for r in res.rows] if cand is not None else []
            hit = any(C.CandIndex.hit(c) for c in col)
            if j == 0:
                first = (res, col)
                st["units"] += 1
                if cand is not None:
                    for key in ("line", "id", "item"):
                        st[f"unit_{key}_hits_before"] += int(any(c[key] for c in col))
                    st["units_colliding_before"] += int(hit)
                if not hit:
                    break
                continue
            if not hit:
                first = (res, col)
                st["redrawn_ok"] += 1
                tries_hist[j] += 1
                break
        else:
            if first is not None:
                st["kept_colliding_after_tries"] += 1
        if first is None:
            continue
        res, col = first
        if cand is not None:
            for key in ("line", "id", "item"):
                st[f"unit_{key}_hits_after"] += int(any(c[key] for c in col))
            st["units_colliding_after"] += int(any(C.CandIndex.hit(c) for c in col))
        rows += res.rows
    rows = rows[:n]
    not_dev = sum(1 for r in rows if not (r["meta"].get("dev_only") or r["meta"].get("sampler") in held))
    rep = {"rows": len(rows), "attempts": k, "drops": dict(drops), "not_dev_only": not_dev, "seed_base": seed_base,
           "held_out_samplers": list(held)}
    if cand is not None:
        rep["d1"] = {"level": level, "tries": tries, "stride": stride, **dict(st), "redraw_tries_histogram": dict(sorted(tries_hist.items()))}
    return rows, rep


def verify_dev_rows(plugin, ctx, rows: list) -> dict:
    """Post-hoc check of the written dev rows: solver B on the parsed row equals the gold (G2, 100%), the schema and G15."""
    bad = Counter()
    for r in rows:
        try:
            view = plugin.parse(r, ctx)
            b = plugin.solve_b(view)
            if r["qtype"] == "choice":
                keys = view.get("options")
                ok = isinstance(keys, list) and len(keys) == len(r["options"]) and keys[r["options"].index(r["gold"])] == b
            else:
                ok = b == r["gold"]
            if not ok:
                bad["G2"] += 1
        except Exception:  # noqa: BLE001
            bad["G2_exception"] += 1
        if R.validate_row(r):
            bad["schema"] += 1
        if not R.g15_check(r)["ok"]:
            bad["G15"] += 1
    return {"rows": len(rows), "failures": dict(bad), "pass": not bad}


def precondition(fam: str, mix_rows: list) -> dict:
    """The A53 precondition exactly as a54_rebuild_mixdev.precondition computes it (imported, not copied)."""
    import a54_rebuild_mixdev as RB54
    return RB54.precondition(fam, mix_rows)


def collision_report(cand: "C.CandIndex", rows: list) -> dict:
    """Rows of a mixdev that still hit each d1 tier against the candidates (counts only)."""
    c = Counter()
    for r in rows:
        col = cand.collisions(r, "item")
        for k in ("line", "id", "item"):
            c[k] += int(bool(col[k]))
        c["any"] += int(C.CandIndex.hit(col))
    return {"dev_rows": len(rows), **{f"rows_{k}": v for k, v in c.items()}}


# ================================================================================================ one family
def rebuild(fam: str, *, level: str = "item", d1: bool = True, overlay: bool = True, tries: int = C.D1_TRIES, write: bool = False,
            out_dir: Path | None = None, force: bool = False, verify_candidates: bool = False, dev_root: Path | None = None,
            log=print) -> dict:
    if fam not in C.FAMILIES:
        raise SystemExit(f"{fam}: not an A55 family {C.FAMILIES}")
    t0 = time.time()
    L = G.layout(fam)
    gen = json.loads(L["gen"].read_text())
    mix_base = gen["seeds"]["mixdev"]
    src = G.quarantine_sources(fam)
    banned = set().union(*map(set, src.values()))
    drops = json.loads((L["qc"] / "DROPS.json").read_text())
    quarantined = set(drops.get("quarantined_templates") or [])
    ident0 = C.generator_identity(fam)
    cand = C.CandIndex(fam) if d1 else None
    cand_for_report = cand or C.CandIndex(fam)
    old_rows = C.read_jsonl(L["mixdev"]) if L["mixdev"].exists() else []
    res = {"family": fam, "level": level if d1 else None, "d1": d1, "mixdev_seed_base": mix_base}

    froot = (Path(dev_root) / fam) if dev_root else None          # analysis only: a scratch copy of dev_a55
    if dev_root and write:
        raise SystemExit("--dev-root is for analysis (--check-only): a real rebuild reads zed_orch/a55_dev/<FAM>/FROZEN.json")

    def one(use_overlay: bool) -> tuple:
        ov54, ov55 = {}, {}
        with G.loader_patch(fam), OV54.patched(fam, None, ov54), (OV55.patched(fam, ov55, root=froot) if use_overlay else _null()):
            with G.PL.open_family(fam) as kit0:
                kit, xrep = G.apply_exclusions(kit0, banned)
                rd = G.Redraw(kit.plugin, xrep["dead_qforms"]) if (fam not in G.FALLBACK_FAMILIES and xrep["dead_qforms"]) else None
                try:
                    mix_rows, mix_rep = build_mixdev_d1(kit, G.MIXDEV_N, mix_base, cand, level, tries)
                finally:
                    if rd:
                        rd.restore()
                _k, _r, kmix, _o = Q.apply_drops([], [], mix_rows, set(), quarantined)
                pre = precondition(fam, kmix)
                dev_chk = verify_dev_rows(kit.plugin, kit.ctx, kmix)
        return mix_rows, mix_rep, kmix, pre, dev_chk, ov54, ov55

    use_ov = overlay and fam in OV55.FAMS and OV55.load_frozen(fam, froot) is not None
    mix_rows, mix_rep, kmix, pre, dev_chk, ov54, ov55 = one(use_ov)
    res["overlay"] = ov55 if use_ov else {"active": False, "why": "no overlay for this family" if fam not in OV55.FAMS
                                           else ("disabled" if not overlay else "nothing frozen yet (zed_orch/a55_dev/%s/FROZEN.json)" % fam)}
    if use_ov and not pre["ok"]:
        res["overlay_reverted_precondition_failed"] = pre
        log(f"{fam}: A53 precondition fails with the overlay: d2/d3 reverted, d1 kept")
        mix_rows, mix_rep, kmix, pre, dev_chk, ov54, ov55 = one(False)
        res["overlay"] = {"active": False, "why": "reverted (A53 precondition)"}
    res.update({"mixdev_built": len(mix_rows), "mixdev_after_quarantine": len(kmix), "attempts": mix_rep.get("attempts"),
                "drops": mix_rep.get("drops"), "not_dev_only": mix_rep.get("not_dev_only"), "a53_precondition": pre,
                "d1_stats": mix_rep.get("d1"), "dev_row_checks": dev_chk,
                "a54_overlay": ov54, "wording_ids_mixdev": len({r["meta"]["wording_id"] for r in kmix}),
                "seconds": round(time.time() - t0, 1)})
    res["collisions_old_mixdev"] = collision_report(cand_for_report, old_rows) if old_rows else None
    res["collisions_new_mixdev"] = collision_report(cand_for_report, kmix)
    dump = lambda r: json.dumps(r, sort_keys=True, ensure_ascii=False)  # noqa: E731
    res["rows_identical_to_old_mixdev"] = sum(1 for a, b in zip(map(dump, kmix), map(dump, old_rows)) if a == b)
    res["generator_unchanged"] = not C.identity_diff(ident0, C.generator_identity(fam))
    res["new_mixdev_sha256"] = C.sha_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in kmix))
    if out_dir is not None:
        d = Path(out_dir) / fam
        d.mkdir(parents=True, exist_ok=True)
        (d / "mixdev_S5.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in kmix), encoding="utf-8")
        res["out_file"] = str(d / "mixdev_S5.jsonl")
    ok = pre["ok"] and dev_chk["pass"] and res["generator_unchanged"] and not (mix_rep.get("not_dev_only"))
    res["ok_to_write"] = bool(ok)
    if not write or (not ok and not force):
        res["written"] = False
        return res
    # ---- write: back up first, then the mixdev files, MANIFEST, GEN_REPORT, DROPS and QC_REPORT ----------------------
    old_sha = C.sha_file(L["mixdev"]) if L["mixdev"].exists() else None
    sup = L["out"] / C.SUPERSEDED
    n_prev = 0
    if sup.exists():
        n_prev = sum(1 for p in sup.iterdir() if p.is_dir()) + 1
        sup = sup / f"rebuild_{n_prev + 1}"
    sup.mkdir(parents=True, exist_ok=True)
    files = [L["mixdev"], L["gendir"] / "mixdev_S5.jsonl", L["man"], L["qcrep"], L["gen"], L["qc"] / "DROPS.json"]
    for f in files:
        if f.exists():
            shutil.copy2(f, sup / (f.name if f.parent.name != "_generated" else "generated_" + f.name))
    bk = C.backup_files(fam, files, tag=time.strftime("%Y%m%dT%H%M%S", time.gmtime()))
    res["backup"] = {"superseded_dir": str(sup.relative_to(C.LEAN)), "zed_orch_backup_dir": str(Path(bk[0][1]).parent.relative_to(C.LEAN)) if bk else None,
                     "files": [(Path(a).name, sh[:12]) for a, _b, sh in bk]}
    paths.write_jsonl(L["gendir"] / "mixdev_S5.jsonl", mix_rows)
    paths.write_jsonl(L["mixdev"], kmix)
    new_sha = C.sha_file(L["mixdev"])
    man = json.loads(L["man"].read_text())
    man["mixdev"] = {"mixdev_S5.jsonl": {"sha256": new_sha, "rows": len(kmix)}}
    paths.write_json(L["man"], man)
    gen["mixdev"] = {**G._clean({k: v for k, v in mix_rep.items()}), "a54_rebuilt": bool(gen.get("mixdev", {}).get("a54_rebuilt")),
                     "a55_rebuilt": True}
    paths.write_json(L["gen"], gen)
    drops["mixdev_after"] = len(kmix)
    paths.write_json(L["qc"] / "DROPS.json", drops)
    qrec = json.loads(L["qcrep"].read_text())
    prev = qrec.get("mixdev", {}).get("mixdev_S5.jsonl") or {}
    qrec["mixdev_pre_a55"] = {"sha256": prev.get("sha256") or old_sha, "rows": prev.get("rows") or len(old_rows)}
    qrec["mixdev"] = {"mixdev_S5.jsonl": {"sha256": new_sha, "rows": len(kmix)}}
    ov_sha = C.sha_file(HERE / "a55_overlay.py")
    qrec["a55"] = {"recorded_utc": C.utc(), "d1_level": level if d1 else None, "overlay_active": bool(res["overlay"].get("frozen")),
                   "overlay_sha256": ov_sha, "rebuild_tool_sha256": C.sha_file(Path(__file__)), "common_sha256": C.sha_file(HERE / "a55_common.py"),
                   "frozen_sha256": res["overlay"].get("frozen_sha256"), "d1_stats": mix_rep.get("d1"),
                   "a53_precondition_ok": pre["ok"], "generator_identity_code_sha256": ident0["code_sha256"],
                   "generator_identity_pools_sha256": ident0["pools_sha256"]}
    qrec["a55_note"] = ("A55 (draft, 17 Oct): mixdev rebuilt dev-only (d1 numerals / ids" + (", d2/d3 forms" if res["overlay"].get("frozen") else "")
                        + "); candidates unchanged; recorded " + C.utc())
    paths.write_json(L["qcrep"], qrec)
    res["written"] = True
    res["mixdev_sha256_before"], res["mixdev_sha256_after"] = old_sha, new_sha
    if verify_candidates:
        import a54_verify_candidates as V
        vr = V.main([fam])[fam]
        res["training_digests"] = {k: vr[k] for k in ("digest_equals_untouched", "final_rows_missing_now", "final_rows_changed",
                                                       "training_rows_unchanged", "digest_now")}
        if not vr["training_rows_unchanged"]:
            res["WARNING"] = "candidates digest changed: revert from " + str(sup)
        else:
            import a55_topup as T
            res["generator_identity_recorded"] = T.record_identity(fam)        # the L2 identity record (ruling (e))
    return res


class _null:
    def __enter__(self):
        return None

    def __exit__(self, *a):
        return False


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("families", nargs="+")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check-only", action="store_true", help="the default: build and report, write nothing under data/")
    ap.add_argument("--level", choices=("item", "line"), default="item")
    ap.add_argument("--no-d1", action="store_true", help="no collision redraw (overlay only)")
    ap.add_argument("--no-overlay", action="store_true")
    ap.add_argument("--tries", type=int, default=C.D1_TRIES)
    ap.add_argument("--out-dir", default=None, help="also write <DIR>/<FAM>/mixdev_S5.jsonl (analysis copy)")
    ap.add_argument("--dev-root", default=None, help="ANALYSIS: parent folder holding <FAM>/FROZEN.json (e.g. the simulated ones)")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--verify-candidates", action="store_true")
    a = ap.parse_args(argv)
    for f in a.families:
        r = rebuild(f, level=a.level, d1=not a.no_d1, overlay=not a.no_overlay, tries=a.tries, write=a.write and not a.check_only,
                    out_dir=a.out_dir, force=a.force, verify_candidates=a.verify_candidates,
                    dev_root=Path(a.dev_root).resolve() if a.dev_root else None)
        print(json.dumps(r, default=str), flush=True)


if __name__ == "__main__":
    main()
