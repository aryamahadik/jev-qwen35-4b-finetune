"""Before / after gate table for the T27 G11 fix round (counts and ids only, no row text).
  report_gates.py [--old GEN_REPORT.json] [--new GEN_REPORT.json] [--cand candidates_c2.jsonl] [--out FILE]
defaults: old = data/c2_parts/T27/qc/GEN_REPORT.json (or qc/_superseded_r2/ after install), new = gen_root/T27/qc/GEN_REPORT.json.

A gate that a report does not hold (a candidates-only validation run has no G11, G6, G7 or A50 entry) is shown as "not run"
and its detail fields are null, never as a passing zero: G11 `templates_over_bar` is null unless the report holds an
evaluated G11 (the key is present). When the candidates file is given, the wording shares counted from it are reported
separately under `candidates_file_only` (derived from the rows, not the G11 gate) so a candidates-only run still shows them."""
import argparse, json, sys
from collections import Counter, defaultdict
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2 = HERE.parents[1]
LEAN = C2.parent
DST = LEAN / "data" / "c2_parts" / "T27"
G11_BAR = 0.02
NOT_RUN = "not run"
GATES = ["full_size", "G2", "G3", "G4", "G-SL", "G-LEX", "G-TW", "G15", "schema", "options", "G7", "G10", "overlay", "spec_3_0",
         "G11", "G12", "G6", "G6_A50"]


def verdict(rep, g):
    if rep is None:
        return None
    gt = rep["gates"].get(g) or rep["gates"].get({"G7": "G7"}.get(g, g))
    return (gt or {}).get("verdict")


def g11_evaluated(x) -> bool:
    """True when the report holds an evaluated G11 (gen_full_c2.g11_shares writes `templates_over_bar`, a dict, even when empty)."""
    return isinstance(x, dict) and isinstance(x.get("templates_over_bar"), dict)


def detail(rep, g, cand_stats=None):
    if rep is None:
        return None
    x = rep["gates"].get(g) or {}
    if g == "G11":
        if not g11_evaluated(x):
            out = {"evaluated": False, "max_template_share": None, "templates_over_bar": None, "skins_over_6_rows": None,
                   "note": "G11 not run in this report (candidates-only run?)"}
            if cand_stats is not None:
                out["candidates_file_only"] = cand_stats
            return out
        return {"evaluated": True, "max_template_share": x.get("max_template_share"),
                "templates_over_bar": len(x["templates_over_bar"]),
                "skins_over_6_rows": (x.get("report_3_0") or {}).get("skins_over_6_rows")}
    if g == "G6_A50":
        return {"worst_cell": x.get("worst_cell"), "failing_cells": x.get("failing_cells"), "seed_bases": x.get("seed_bases")}
    if g == "G6":
        return {"fails": x.get("fails")}
    if g == "G7":
        return {"fails": x.get("fails") if "fails" in x else None, "note": (x.get("note") or "")[:120]}
    return None


def wording_stats(rows) -> dict:
    """Wording shares from the candidate rows themselves (not the G11 gate): per question form and overall."""
    n = len(rows)
    by = defaultdict(Counter)
    for r in rows:
        by[r["meta"]["qform"]][r["meta"]["wording_id"]] += 1
    dist = {q: {"rows": sum(c.values()), "wordings": len(c), "min": min(c.values()), "max": max(c.values()),
                "max_share": round(max(c.values()) / n, 4)} for q, c in sorted(by.items())}
    allc = Counter()
    for c in by.values():
        allc.update(c)
    return {"n_rows": n, "distribution": dist, "max_wording_share": round(max(allc.values()) / n, 4),
            "wordings_over_2pct": sum(1 for v in allc.values() if v / n > G11_BAR),
            "wordings_over_2pct_by_qform": {q: sum(1 for v in c.values() if v / n > G11_BAR) for q, c in sorted(by.items())}}


def show(v) -> str:
    return NOT_RUN if v is None else str(v)


def build(old_path, new_path, cand_path) -> dict:
    old = json.loads(Path(old_path).read_text())
    new = json.loads(Path(new_path).read_text()) if Path(new_path).is_file() else None
    out = {"old_report": str(old_path), "new_report": str(new_path) if new else None, "table": {}}
    stats = None
    if cand_path and Path(cand_path).is_file():
        stats = wording_stats([json.loads(l) for l in open(cand_path)])
    cand_g11 = None if stats is None else {"max_wording_share": stats["max_wording_share"],
                                           "wordings_over_2pct": stats["wordings_over_2pct"],
                                           "wordings_over_2pct_by_qform": stats["wordings_over_2pct_by_qform"],
                                           "note": "counted from the candidate rows, not the G11 gate"}
    for g in GATES:
        out["table"][g] = {"before": verdict(old, g), "after": verdict(new, g), "before_detail": detail(old, g),
                           "after_detail": detail(new, g, cand_g11)}
    for k in ("program_pass", "program_failing", "program_pass_a50", "program_failing_a50", "n_candidates", "seeds"):
        out[k] = {"before": old.get(k), "after": (new or {}).get(k)}
    if stats is not None:
        out["new_wording_distribution"] = stats["distribution"]
        out["new_max_wording_share"] = stats["max_wording_share"]
        out["new_wordings_over_2pct"] = stats["wordings_over_2pct"]
        out["new_wordings_over_2pct_by_qform"] = stats["wordings_over_2pct_by_qform"]
    return out


def lines(out) -> list:
    w = max(len(g) for g in GATES)
    res = []
    for g, v in out["table"].items():
        d = v["after_detail"]
        res.append(f"{g:<{w}}  before {show(v['before']):<8} after {show(v['after']):<8} {d or ''}")
    for k in ("program_pass", "program_failing", "program_pass_a50", "program_failing_a50"):
        res.append(f"{k} {out[k]}")
    if "new_wording_distribution" in out:
        res.append(f"{json.dumps(out['new_wording_distribution'])} max share {out['new_max_wording_share']} "
                   f"wordings over 2%: {out['new_wordings_over_2pct']}")
    return res


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--old", default=str(DST / "qc" / "_superseded_r2" / "GEN_REPORT.json"
                                         if (DST / "qc" / "_superseded_r2").exists() else DST / "qc" / "GEN_REPORT.json"))
    ap.add_argument("--new", default=str(HERE / "gen_root" / "T27" / "qc" / "GEN_REPORT.json"))
    ap.add_argument("--cand", default=str(HERE / "gen_root" / "T27" / "out" / "candidates_c2.jsonl"))
    ap.add_argument("--out", default=str(HERE / "report_gates.json"))
    a = ap.parse_args(argv)
    out = build(a.old, a.new, a.cand)
    Path(a.out).write_text(json.dumps(out, indent=1, default=str))
    print("\n".join(lines(out)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
