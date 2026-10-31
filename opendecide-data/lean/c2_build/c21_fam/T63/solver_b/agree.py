"""In-memory agreement harness for T63 solver B (the ONLY file of this package that imports the generator side).

    PYTHONDONTWRITEBYTECODE=1 python3 -B agree.py --rows 2000 --seeds 1,2,3 --out SCRATCH/report.json [--log agreement_log.json] [--pool real|test]

Builds rows IN MEMORY with the family generator (stand-in mode: FIXTURE stdlib export and FIXTURE licence table, flagged non-production; B runs with
fixture=True, allow_fixture=True, build-stage evidence only), hands solver B only `schema.b_view(rec)`, compares B's label with the record's gold and B's letter with the gold letter. Nothing is written but the JSON reports
named on the command line; no row text, row id or package name goes into the counts-only log."""
import argparse
import collections
import json
import os
import sys

FAM = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if FAM not in sys.path:
    sys.path.insert(0, FAM)
sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
POOL = os.path.join(os.path.dirname(HERE), "pools", "wording_pool.json")
BARS = {"K1": "T63-K1: solver A = solver B on 100% of kept rows; a block with > 2% disagreement returns to the generator"}
_BUILD = os.path.dirname(FAM)                                          # .../c2_build
LIC_TABLE_FILE = os.path.join(_BUILD, "zed_orch", "c21", "l0", "T63_LIC_TABLE.json")
LIC_RECORD_FILE = os.path.join(_BUILD, "zed_orch", "c21", "l0", "T63_LIC_TABLE_RECORD.json")
LIC_USE_IDS = ["LC-USE-%d" % i for i in range(1, 6)]
LIC_DIST_IDS = ["LC-DIST-%d" % i for i in range(1, 4)]


def load_fixture_sources():
    """-> (export_set_obj, export_data_dict, table_obj). The export data dict is captured while the dry run builds its fixture (no module opened)."""
    from T63 import dryrun, lic
    captured = []
    orig = dryrun.exists.ExportSet

    def spy(data):
        captured.append(data)
        return orig(data)

    dryrun.exists.ExportSet = spy
    try:
        ex = dryrun.fixture_exports()
    finally:
        dryrun.exists.ExportSet = orig
    return ex, captured[0]["exports"], lic.fixture_table()


def load_real_lic_table():
    """-> (LicTable object for the generator, plain dict for B, recorded sha). The REAL hashed T63-LIC-TABLE (Opus 5.5 high, separate session) and its
    L-0 record. B's plain table is read straight from the table file (cells "dep|project|LC-USE-n|LC-DIST-n" -> label), NOT from the generator's table
    object; B's sha is the one the L-0 record states, NOT one read off a row."""
    from T63 import lic
    with open(LIC_TABLE_FILE) as f:
        data = json.load(f)
    with open(LIC_RECORD_FILE) as f:
        rec = json.load(f)
    tb = lic.LicTable(data)
    plain = {}
    for k, cell in data["cells"].items():
        dep, proj, use, dist = k.split("|")
        plain[(dep, proj, use, dist)] = cell["label"]
    if tb.fixture or rec.get("sha256") != tb.sha:
        raise SystemExit("the LIC table file, its L-0 record and the loaded table disagree (or it is a fixture): stop")
    return tb, plain, rec["sha256"]


def table_to_plain(tb, rows):
    """Plain {(dep, project, usage_id, distribution_id): label} for every dep / project licence id that appears on a RENDERED card of `rows`."""
    deps, projs = set(), set()
    for r in rows:
        if r["head"] == "LIC":
            for ln in r["rendered"]["context"].split("\n"):
                if ln.startswith("Dependency licence: "):
                    deps.add(ln.split(": ", 1)[1].strip())
                elif ln.startswith("Project licence: "):
                    projs.add(ln.split(": ", 1)[1].strip())
    out = {}
    for d in sorted(deps):
        for p in sorted(projs):
            for u in LIC_USE_IDS:
                for s in LIC_DIST_IDS:
                    try:
                        out[(d, p, u, s)] = tb.label(d, p, u, s)
                    except Exception:                                        # noqa: BLE001 - a cell outside the fixture table
                        pass
    return out


def build_rows(total, seed, pool, ex, tb):
    from LP_COMMON import pipeline as pl
    from T63 import checked
    kw = {"pool_path": POOL} if pool == "real" else {}
    rows, summary, _log, _rep = checked.run(total, seed, pl.TestDoubleHook(), standin=True, exports=ex, table=tb, solver_b=None, **kw)
    return rows, summary


def evaluate(rows, run_b, schema):
    stats = {"rows": 0, "labelled": 0, "agree": 0, "disagree": 0, "abstain": 0, "error": 0, "letter_mismatch": 0, "b1_xcheck_diff": 0}
    by_sub = collections.defaultdict(lambda: collections.Counter())
    classes = collections.Counter()
    abst = collections.Counter()
    paths = collections.Counter()                                         # which B rule branch decided, by sub-block and gold label (coverage)
    samples = []                                                          # private (scratch) triage info: row index only, no text
    for idx, rec in enumerate(rows):
        view = schema.b_view(rec)
        res = run_b(view)
        sb = rec["sub_block"]
        stats["rows"] += 1
        by_sub[sb]["rows"] += 1
        if res.get("status") == "ok" and res.get("label") is not None:
            paths["%s | %s | gold %s" % (sb, (res.get("reason") or "").split(":")[0], rec["gold"])] += 1
            stats["labelled"] += 1
            by_sub[sb]["labelled"] += 1
            if res["label"] == rec["gold"]:
                stats["agree"] += 1
                by_sub[sb]["agree"] += 1
                if res.get("letter") != rec["gold_letter"]:
                    stats["letter_mismatch"] += 1
                    by_sub[sb]["letter_mismatch"] += 1
            else:
                stats["disagree"] += 1
                by_sub[sb]["disagree"] += 1
                classes["%s: B=%s gold=%s via %s" % (sb, res["label"], rec["gold"], (res.get("reason") or "").split(":")[0])] += 1
                samples.append((idx, sb, rec["gold"], res["label"], res.get("reason")))
            if res.get("xcheck") is False:
                stats["b1_xcheck_diff"] += 1
        else:
            key = "error" if res.get("status") == "error" else "abstain"
            stats[key] += 1
            by_sub[sb][key] += 1
            abst["%s: %s" % (sb, res.get("reason"))] += 1
    return stats, by_sub, classes, abst, samples, paths


def pct(a, b):
    return round(100.0 * a / b, 3) if b else None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=1500, help="rows requested per seed (the generator oversamples by 15%%)")
    ap.add_argument("--seeds", default="1,2")
    ap.add_argument("--out", default=None)
    ap.add_argument("--shas", action="store_true", help="write SHAS.json (sha256 of every file in this folder except SHAS.json) and exit")
    ap.add_argument("--log", default=None, help="counts-only agreement log kept in the repo (no ids, names or text)")
    ap.add_argument("--pool", choices=("real", "test"), default="real")
    ap.add_argument("--lic-fixture", action="store_true", help="LIC rows from the FIXTURE table (build-stage); default: the REAL hashed T63-LIC-TABLE, fixture=False")
    ap.add_argument("--no-b2-sources", action="store_true", help="diagnostic: run EX-B2 / LIC without their sources (must abstain)")
    a = ap.parse_args(argv)
    if a.shas:
        return write_shas()
    if not a.out:
        ap.error("--out is required")
    from T63 import schema
    from T63.solver_b import hook
    ex, export_data, tb = load_fixture_sources()
    real_plain = real_sha = None
    if not a.lic_fixture:
        tb, real_plain, real_sha = load_real_lic_table()
    tot = {"rows": 0, "labelled": 0, "agree": 0, "disagree": 0, "abstain": 0, "error": 0, "letter_mismatch": 0, "b1_xcheck_diff": 0}
    by_sub = collections.defaultdict(collections.Counter)
    by_head = collections.defaultdict(collections.Counter)
    classes, abst, paths = collections.Counter(), collections.Counter(), collections.Counter()
    per_seed, private = [], []
    for seed in [int(s) for s in a.seeds.split(",")]:
        rows, summary = build_rows(a.rows, seed, a.pool, ex, tb)
        if a.no_b2_sources:
            table = None
        else:
            table = table_to_plain(tb, rows) if a.lic_fixture else real_plain
        exports = None if a.no_b2_sources else export_data
        table_sha = None if table is None else (_table_sha(rows) if a.lic_fixture else real_sha)

        def run_b(view, _t=table, _e=exports, _ts=table_sha):
            # EX-B1 / EX-B2: the sources are FIXTURES (the L-0 export does not exist yet), so B is told so and explicitly allowed to use them: BUILD-STAGE
            # ONLY (production B refuses fixtures, Opus ruling Q3a). LIC: the REAL hashed table, fixture=False, its sha is the one the L-0 record states
            # (with --lic-fixture the old fixture shortcut applies: the sha is taken from the first LIC witness). The sha is mandatory in every mode.
            fx = a.lic_fixture or view.get("head") != "LIC"
            return hook.evaluate(view, exports=_e, export_sha=ex.sha if _e is not None else None, table=_t, table_sha=_ts, fixture=fx, allow_fixture=fx)

        st, bs, cl, ab, smp, pth = evaluate(rows, run_b, schema)
        per_seed.append({"seed": seed, "rows": st["rows"], "kept_by_pipeline": summary.get("kept"), "agree": st["agree"], "disagree": st["disagree"],
                         "abstain": st["abstain"], "error": st["error"]})
        for k in tot:
            tot[k] += st[k]
        for sb, c in bs.items():
            by_sub[sb].update(c)
            head = {"NEAR": "NEAR", "LIC": "LIC"}.get(sb, "EXISTS")
            by_head[head].update(c)
        classes.update(cl)
        abst.update(ab)
        paths.update(pth)
        private += [(seed,) + s for s in smp]
    report = {"bar": BARS["K1"], "evidence": ("BUILD-STAGE ONLY for EX-B1 / EX-B2: FIXTURE stdlib export (the L-0 image-record export does not exist yet), B run "
                                              "with fixture=True, allow_fixture=True (G0-lite :172); LIC: " +
                                              ("FIXTURE licence table (--lic-fixture)" if a.lic_fixture else
                                               "the REAL hashed T63-LIC-TABLE, content sha %s (L-0 record), B run with fixture=False" % real_sha) +
                                              "; not production K1 until the L-0 export exists"), "pool": a.pool, "seeds": a.seeds, "rows_requested_per_seed": a.rows, "totals": dict(tot),
              "agree_pct_of_labelled": pct(tot["agree"], tot["labelled"]), "agree_pct_of_all": pct(tot["agree"], tot["rows"]),
              "per_seed": per_seed, "by_sub_block": {}, "by_head": {}, "disagreement_classes": dict(classes), "abstain_reasons": dict(abst),
              "rule_paths": dict(paths)}
    for name, src, dst in (("sub", by_sub, "by_sub_block"), ("head", by_head, "by_head")):
        for k, c in sorted(src.items()):
            report[dst][k] = {"rows": c["rows"], "labelled": c["labelled"], "agree": c["agree"], "disagree": c["disagree"], "abstain": c["abstain"],
                              "error": c["error"], "letter_mismatch": c["letter_mismatch"],
                              "agree_pct_labelled": pct(c["agree"], c["labelled"]), "agree_pct_all": pct(c["agree"], c["rows"])}
    with open(a.out, "w") as f:
        json.dump(dict(report, private_triage=private[:400]), f, indent=1, sort_keys=True)
    if a.log:
        with open(a.log, "w") as f:
            json.dump(report, f, indent=1, sort_keys=True)
    print(json.dumps({k: report[k] for k in ("totals", "agree_pct_of_labelled", "agree_pct_of_all", "by_head")}, indent=1, sort_keys=True))
    print("classes:", json.dumps(report["disagreement_classes"], indent=1, sort_keys=True))
    print("abstain:", json.dumps(report["abstain_reasons"], indent=1, sort_keys=True))
    print("paths:", json.dumps(report["rule_paths"], indent=0, sort_keys=True))
    return 0


def write_shas():
    import hashlib
    out = {}
    for base, dirs, files in os.walk(HERE):
        dirs[:] = sorted(d for d in dirs if d != "__pycache__" and not d.startswith("."))
        for fn in sorted(files):
            rel_path = os.path.relpath(os.path.join(base, fn), HERE)
            if rel_path == "SHAS.json" or fn.endswith(".pyc") or fn == ".DS_Store":
                continue
            with open(os.path.join(base, fn), "rb") as f:
                out[rel_path] = hashlib.sha256(f.read()).hexdigest()
    with open(os.path.join(HERE, "SHAS.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
        f.write("\n")
    print("SHAS.json:", len(out), "files")
    return 0


def _table_sha(rows):
    for r in rows:
        if r["head"] == "LIC":
            return r["witness_inputs"].get("table_sha")
    return None


if __name__ == "__main__":
    sys.exit(main())
