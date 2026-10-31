"""A55 (e): the L2 top-up, a draw of MORE SEEDS from the BYTE-IDENTICAL passing generator. It changes no existing row, no code and no
pool. Nothing here runs a G13 check, and the sealed mode reads nothing it writes.

  record  FAM   write the generator identity (plugin / family code, pool files, quarantine sources, Haiku prompt shas) next to the
                QC record: qc/GENERATOR_IDENTITY_A55.json and QC_REPORT["generator_identity_a55"] (a55_rebuild_mixdev --write does
                the same). Run it once per family that may be topped up, while the generator is known to be the passing one.
  check   FAM   the pre-flight of ruling (e): the seed base (733,000,000, fallback 743,000,000) is disjoint from every recorded
                base and redraw class (the tool derives them from the family's GEN_REPORT / QC_REPORT / G6 logs and the ruling's
                list), and the generator identity equals the record. With --rederive it also re-derives the original candidates
                (a54_verify_candidates) and demands a byte-identical digest.
  generate FAM --n X [--root DIR] [--dry-run]
                the top-up: gen_full_c2.run at seed base 733,000,000 (candidates; the QC and mixdev bases are the next two blocks
                and unused), X rows, no QC build (G6 carries over), no mixdev. Into its OWN part
                data/c2_parts/<FAM>/topup_a55/root/<FAM>/{out,qc} (the same layout, so qc_full_c2.py --root and the other tools work
                unchanged); the original part is not touched (its digest is re-checked at the end). Gates on the top-up rows:
                G2 G3 G4 G-SL G-LEX G-TW G15 schema options (pilot.program_gates), G12 exact against the top-up AND the existing
                rows (the existing row is kept), G10 (report only), and the Haiku tasks: G5-H on a seeded min(300, X) rows + every
                free-form row, G3-H on every free-form row (the 30 agreed controls and the Sonnet / Opus cascade come from
                qc_full_c2.py score | adjudicate | finalize --root). On old + top-up together: G7 (pilot.g7) and G11 (skin and
                template <= 2%). G8 on old + new is the orchestrator's step (c_src/common/g8_aflite.py, as for every family).
  merge   FAM   [--dry-run] the combined view (original rows + the kept top-up rows) in a separate root, for the consumers
  decision FAM  print the logged decision (A55_TOPUP_DECISION.json: E, X) and refuse when the decision says no top-up, or when X
                differs from --n.

A top-up that fails a gate is discarded whole and its seeds are never reused (`generate` writes nothing when a program gate fails;
a part that was written and later fails stays under topup_a55/ as evidence and `discard` renames it _discarded_<utc>).
Run from lean/c2_build:  ../../.venv/bin/python -B zed_orch/a55_topup.py check T24 [--rederive]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2B = HERE.parent
for _p in (str(C2B), str(HERE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
sys.dont_write_bytecode = True

import a55_common as C  # noqa: E402
import c2io  # noqa: E402
import gen_full_c2 as G  # noqa: E402
import pilot  # noqa: E402
from c2_kit import g5h, paths  # noqa: E402

DECISION = HERE / "g13_attr" / "A55_TOPUP_DECISION.json"
# the seed classes the ruling lists as recorded (base of each block; every block also has its redraw class base + j * stride)
RULING_BASES = (900_000, 2_000_000, 3_000_000, 4_000_000, 11_000_000, 12_000_000, 13_000_000, 39_000_000, 40_000_000, 41_000_000,
                46_000_000, 47_000_000, 48_000_000, 127_000_000, 128_000_000, 129_000_000, 250_000_000, 251_000_000, 252_000_000)
MAX_REDRAW_J = 60                                # gen_full_c2.Redraw.MAX


def topup_root(fam: str) -> Path:
    return C.PARTS / fam / "topup_a55" / "root"


# ================================================================================================ seeds
def _walk_ints(o, keys=("candidates", "qc", "mixdev", "seed_bases", "bases", "seed_base")):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in keys:
                if isinstance(v, int):
                    yield v
                elif isinstance(v, list):
                    yield from (x for x in v if isinstance(x, int))
            if isinstance(v, (dict, list)):
                yield from _walk_ints(v, keys)
    elif isinstance(o, list):
        for v in o:
            if isinstance(v, (dict, list)):
                yield from _walk_ints(v, keys)


def recorded_bases(fam: str | None = None) -> dict:
    """{base: [where it is recorded]}: the ruling's list plus every seed base found in the GEN_REPORT / QC_REPORT / G6 logs of every
    family part (a base used by any family counts: the classes are program-wide)."""
    out: dict = {b: ["ruling A55 (e) list"] for b in RULING_BASES}
    for d in sorted(p for p in C.PARTS.iterdir() if p.is_dir()):
        qc = d / "qc"
        for name in ("GEN_REPORT.json", "QC_REPORT.json", "G6_A50.json"):
            f = qc / name
            if not f.is_file():
                continue
            try:
                j = json.loads(f.read_text(encoding="utf-8"))
            except ValueError:
                continue
            for b in _walk_ints(j.get("seeds", j) if name == "GEN_REPORT.json" else j):
                if b >= 100_000:
                    out.setdefault(b, []).append(f"{d.name}/{name}")
    return out


def seed_intervals(base: int, stride: int = C.REDRAW_STRIDE) -> list:
    return [(base + j * stride, base + j * stride + C.SEED_SPAN) for j in range(0, MAX_REDRAW_J + 1)]


def overlaps(a: list, b: list) -> list:
    return [(x, y) for x in a for y in b if x[0] < y[1] and y[0] < x[1]]


def choose_base(fam: str, base: int | None = None) -> dict:
    """733,000,000 unless it is in use, then the pre-declared 743,000,000; both must be divisible by 32 and disjoint (every redraw
    class included) from every recorded base. A base that is not disjoint is refused, never nudged."""
    rec = recorded_bases(fam)
    rec_iv = [iv for b in rec for iv in seed_intervals(b)]
    tried = []
    for cand in ([base] if base else [C.TOPUP_SEED_BASE, C.TOPUP_SEED_FALLBACK]):
        if cand % 32:
            raise SystemExit(f"seed base {cand} is not divisible by 32")
        clash = overlaps(seed_intervals(cand), rec_iv)
        tried.append({"base": cand, "clashes": len(clash)})
        if not clash:
            return {"base": cand, "tried": tried, "recorded_bases": len(rec), "bases": [cand, cand + C.SEED_SPAN, cand + 2 * C.SEED_SPAN]}
    raise SystemExit(f"{fam}: no top-up seed base is disjoint from the recorded classes: {tried}")


# ================================================================================================ identity
def record_identity(fam: str) -> dict:
    ident = C.generator_identity(fam)
    L = G.layout(fam)
    rec = {"recorded_utc": C.utc(), **{k: ident[k] for k in ("code_sha256", "pools_sha256", "quarantine_sources_sha256",
                                                              "haiku_prompt_shas_sha256")}}
    flat = {**{k: ident[k] for k in ("family", "quarantine_sources", "quarantine_sources_sha256", "haiku_prompt_shas",
                                     "haiku_prompt_shas_sha256", "code_sha256", "pools_sha256")},
            "code": sorted([k, v] for k, v in ident["code"].items()), "pools": sorted([k, v] for k, v in ident["pools"].items())}
    paths.write_json(L["qc"] / "GENERATOR_IDENTITY_A55.json", {**rec, "identity": flat})      # file names as list items (the writer refuses '_' keys)
    q = json.loads(L["qcrep"].read_text())
    q["generator_identity_a55"] = rec
    paths.write_json(L["qcrep"], q)
    return rec


def check_identity(fam: str) -> dict:
    L = G.layout(fam)
    q = json.loads(L["qcrep"].read_text())
    rec = q.get("generator_identity_a55") or (q.get("a55") or {}).get("generator_identity")
    if not rec:
        return {"ok": False, "why": "no generator_identity_a55 record in QC_REPORT (run: a55_topup.py record FAM)"}
    full = L["qc"] / "GENERATOR_IDENTITY_A55.json"
    now = C.generator_identity(fam)
    if full.is_file():
        old = json.loads(full.read_text())["identity"]
        old = {**old, "code": dict(old["code"]), "pools": dict(old["pools"])}
        diff = C.identity_diff(old, now)
    else:
        diff = [k for k in ("code_sha256", "pools_sha256", "quarantine_sources_sha256", "haiku_prompt_shas_sha256")
                if rec.get(k) != now[k]]
    return {"ok": not diff, "diff": diff[:20], "recorded_utc": rec.get("recorded_utc")}


def rederive(fam: str) -> dict:
    import a54_verify_candidates as V
    r = V.main([fam])[fam]
    return {k: r[k] for k in ("digest_equals_untouched", "final_rows_missing_now", "final_rows_changed", "training_rows_unchanged",
                              "digest_now", "seconds")}


def check(fam: str, base: int | None = None, rederive_: bool = False) -> dict:
    out = {"family": fam, "seed": choose_base(fam, base), "identity": check_identity(fam)}
    if rederive_:
        out["rederive"] = rederive(fam)
    out["ok"] = out["identity"]["ok"] and (not rederive_ or out["rederive"]["training_rows_unchanged"])
    return out


# ================================================================================================ decision
def logged_decision(fam: str) -> dict:
    d = json.loads(DECISION.read_text())["decision"].get(fam)
    if d is None:
        raise SystemExit(f"{fam}: no logged decision in {DECISION.name} (run a55_measure.py --decide first)")
    return d


# ================================================================================================ generate
def _key(r):
    import hashlib
    return hashlib.sha256(json.dumps([r.get("card"), r["state"], r["instructions"], r.get("options")], ensure_ascii=False).encode()).hexdigest()


def generate(fam: str, n: int, *, root: Path | None = None, dry: bool = False, base: int | None = None, skip_old: bool = False,
             allow_unlogged: bool = False, log=print) -> dict:
    if fam in C.NO_L2:
        raise SystemExit(f"{fam}: no L2 (ruling (f))")
    t0 = time.time()
    if not allow_unlogged:
        d = logged_decision(fam)
        if not d.get("topup"):
            raise SystemExit(f"{fam}: the logged decision is NO top-up ({d.get('why')})")
        if int(d["X"]) != int(n):
            raise SystemExit(f"{fam}: X is fixed by the logged decision ({d['X']}) and is never changed; got --n {n}")
    seed = choose_base(fam, base)
    ident = check_identity(fam)
    if not ident["ok"] and not allow_unlogged:
        raise SystemExit(f"{fam}: generator identity differs from the QC record: {ident}")
    root = Path(root).resolve() if root else topup_root(fam)
    L0 = G.layout(fam)
    gen0 = json.loads(L0["gen"].read_text())
    ob = (gen0["seeds"]["candidates"], gen0["seeds"]["qc"], gen0["seeds"]["mixdev"])
    old_rows = C.read_jsonl(L0["cand"])
    old_digest_before = C.sha_file(L0["cand"])
    res = {"family": fam, "n_requested": n, "seed": seed, "identity": ident, "root": str(root)}
    # ---- the existing candidates: byte-identical re-derivation, and their infos for the old + new gates -------------------
    old_infos = None
    if not skip_old:
        cap = {}
        orig_bp = G.pilot.build_pilot

        def spy(*a, **k):
            r = orig_bp(*a, **k)
            cap.setdefault("b", r)
            return r
        G.pilot.build_pilot = spy
        try:
            G.run(fam, dry=True, no_qc=True, seed_bases=ob, log=lambda m: None)
        finally:
            G.pilot.build_pilot = orig_bp
        rederived = [i.row for i in cap["b"].infos]
        gen_rows = C.read_jsonl(L0["gendir"] / c2io.CAND)
        same = G.rows_digest(rederived) == G.rows_digest(gen_rows)
        res["rederive"] = {"rows": len(rederived), "digest": G.rows_digest(rederived), "equals_untouched_generated_file": same}
        if not same:
            raise SystemExit(f"{fam}: the original candidates do not re-derive byte-identical: NO top-up")
        keep_ids = {r["id"] for r in old_rows}
        old_infos = [i for i in cap["b"].infos if i.row["id"] in keep_ids]
        res["rederive"]["kept_rows"] = len(old_infos)
        log(f"{fam}: original candidates re-derived byte-identical ({len(rederived)} rows) {round(time.time() - t0)}s")
    old_keys = {_key(r) for r in old_rows}
    # ---- the top-up build ------------------------------------------------------------------------------------------------
    cap2 = {}
    orig_bp, orig_dd, orig_nread, orig_mix = G.pilot.build_pilot, G.dedup_exact, g5h.n_read, G.MIXDEV_N

    def spy2(*a, **k):
        r = orig_bp(*a, **k)
        cap2["b"] = r
        return r

    def dedup_old_and_new(b):
        rep = orig_dd(b)
        drop = {i.row["id"] for i in b.infos if _key(i.row) in old_keys}
        if drop:
            b.infos = [i for i in b.infos if i.row["id"] not in drop]
            b.rels = [x for x in b.rels if x["a"] not in drop and x["b"] not in drop]
        rep["exact_duplicates_vs_existing_dropped"] = len(drop)
        rep["rows_after"] = len(b.infos)
        rep["bar"] = "G12 on old + top-up: exact duplicates 0 (the existing row is kept; MinHash near-duplicates: the batch step)"
        res["g12_vs_existing"] = {"dropped": len(drop)}
        return rep
    G.pilot.build_pilot, G.dedup_exact, g5h.n_read, G.MIXDEV_N = spy2, dedup_old_and_new, (lambda f: min(300, n)), 0
    try:
        rep = G.run(fam, n=n, dry=dry, no_qc=True, root=root, seed_bases=tuple(seed["bases"]), log=log)
    finally:
        G.pilot.build_pilot, G.dedup_exact, g5h.n_read, G.MIXDEV_N = orig_bp, orig_dd, orig_nread, orig_mix
    b = cap2["b"]
    gates = rep["gates"]
    prog = {g: gates[g]["verdict"] for g in pilot.PROGRAM_GATES if g in gates}
    res["top_up"] = {"rows": len(b.infos), "units": len(b.units), "seed_base": seed["base"], "program_gates": prog,
                     "program_pass": rep["program_pass"], "program_failing": rep["program_failing"],
                     "G12": gates.get("G12"), "G10_report_only": (gates.get("G10") or {}).get("verdict"),
                     "mode_f_rows": rep["mode_f_rows"], "haiku_tasks": rep["haiku_tasks"],
                     "candidate_problems": rep["candidate_problems"], "written": rep["written"]}
    ok_prog = all(v == "pass" for v in prog.values()) and gates.get("G12", {}).get("verdict") == "pass" and not rep["candidate_problems"]
    res["top_up"]["program_gates_all_pass"] = bool(ok_prog)
    # ---- old + top-up together: G7 and G11 ------------------------------------------------------------------------------
    if old_infos is not None:
        both = list(old_infos) + list(b.infos)
        plugin_kit = None
        g7 = pilot.g7(both)
        g11 = G.g11_shares([types.SimpleNamespace(row=i.row) for i in both], None)
        res["old_plus_topup"] = {"rows": len(both), "G7": {k: g7.get(k) for k in ("verdict", "n_tests", "n_yes_no_rows", "n_choice_rows")},
                                 "G11": {k: g11[k] for k in ("verdict", "max_template_share", "templates_over_bar")},
                                 "G8": "not run here (as for every family): the orchestrator runs c_src/common/g8_aflite.py on old + top-up"}
        res["old_plus_topup_pass"] = g7.get("verdict") != "fail" and g11["verdict"] == "pass"
    res["original_part_digest_unchanged"] = C.sha_file(L0["cand"]) == old_digest_before
    res["seconds"] = round(time.time() - t0, 1)
    res["ok"] = bool(ok_prog and res["original_part_digest_unchanged"] and res.get("old_plus_topup_pass", True))
    if not dry and rep["written"]:
        out = root / fam / "out" / c2io.CAND
        res["part"] = {"file": str(out.relative_to(C.LEAN)), "sha256": C.sha_file(out), "rows": len(C.read_jsonl(out))}
        if not res["ok"]:
            res["WARNING"] = "a gate failed: this part is discarded whole (a55_topup.py discard FAM); its seeds are never reused"
    return res


def merge(fam: str, write: bool = False) -> dict:
    """The combined view for the consumers (final G13, select, mix): original rows (byte-identical, same order) followed by the
    top-up rows kept after the top-up's own QC, in a SEPARATE root data/c2_parts/<FAM>/topup_a55/merged_root/<FAM>/ (the original part
    and the top-up part are not touched). Needs the top-up QC finalized (qc_full_c2.py FAM finalize --root <topup root>)."""
    L0, Lt = G.layout(fam), G.layout(fam, topup_root(fam))
    if not Lt["cand"].is_file() or not Lt["qcrep"].is_file():
        raise SystemExit(f"{fam}: no top-up part")
    qt = json.loads(Lt["qcrep"].read_text())
    if not qt.get("pass") or qt.get("stage") != "final":
        raise SystemExit(f"{fam}: the top-up QC is not final / not passed (stage {qt.get('stage')}, pass {qt.get('pass')})")
    old, new = C.read_jsonl(L0["cand"]), C.read_jsonl(Lt["cand"])
    ids = {r["id"] for r in old}
    clash = [r["id"] for r in new if r["id"] in ids]
    if clash:
        raise SystemExit(f"{fam}: {len(clash)} top-up ids already exist in the original part")
    rels = C.read_jsonl(L0["rel"]) + (C.read_jsonl(Lt["rel"]) if Lt["rel"].is_file() else [])
    out = {"family": fam, "original_rows": len(old), "topup_rows": len(new), "merged_rows": len(old) + len(new),
           "original_sha256": C.sha_file(L0["cand"]), "topup_sha256": C.sha_file(Lt["cand"]), "written": False}
    if write:
        mr = topup_root(fam).parent / "merged_root"
        Lm = G.layout(fam, mr)
        paths.write_jsonl(Lm["cand"], old + new)
        paths.write_jsonl(Lm["rel"], rels)
        man = {"family": fam, "parents": [], "generator": "A55 merged view: original part + top-up part",
               "parts": {"original": {"sha256": out["original_sha256"], "rows": len(old)}, "topup": {"sha256": out["topup_sha256"], "rows": len(new)}},
               "files": {c2io.CAND: {"sha256": C.sha_file(Lm["cand"]), "rows": len(old) + len(new)},
                         c2io.REL: {"sha256": C.sha_file(Lm["rel"]), "rows": len(rels)}}}
        paths.write_json(Lm["man"], man)
        paths.write_json(Lm["qcrep"], {"pass": True, "stage": "final", "family": fam, "note": "A55 merged view; the QC records are the "
                                       "original part's and the top-up part's", "files": man["files"]})
        out.update({"written": True, "root": str(mr.relative_to(C.LEAN)), "merged_sha256": man["files"][c2io.CAND]["sha256"]})
    return out


def discard(fam: str) -> dict:
    d = C.PARTS / fam / "topup_a55"
    if not d.exists():
        return {"discarded": False}
    new = C.PARTS / fam / f"topup_a55_discarded_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    d.rename(new)
    return {"discarded": True, "moved_to": str(new.relative_to(C.LEAN))}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=("record", "check", "generate", "decision", "discard", "merge"))
    ap.add_argument("family")
    ap.add_argument("--n", type=int)
    ap.add_argument("--root", default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--base", type=int, default=None)
    ap.add_argument("--rederive", action="store_true")
    ap.add_argument("--skip-old", action="store_true", help="TEST ONLY: skip the old-candidates re-derivation and the old + new gates")
    ap.add_argument("--allow-unlogged", action="store_true", help="TEST ONLY: ignore the logged decision / identity record")
    a = ap.parse_args(argv)
    if a.cmd == "record":
        r = record_identity(a.family)
    elif a.cmd == "check":
        r = check(a.family, a.base, a.rederive)
    elif a.cmd == "decision":
        r = logged_decision(a.family)
    elif a.cmd == "discard":
        r = discard(a.family)
    elif a.cmd == "merge":
        r = merge(a.family, write=not a.dry_run)
    else:
        r = generate(a.family, a.n, root=a.root, dry=a.dry_run, base=a.base, skip_old=a.skip_old, allow_unlogged=a.allow_unlogged,
                     log=lambda m: print(m, file=sys.stderr, flush=True))
    print(json.dumps(r, indent=1, default=str))


if __name__ == "__main__":
    main()
