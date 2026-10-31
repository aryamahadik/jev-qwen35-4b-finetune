"""build_devx.py: reviewer R's devx build (yn2b/SPEC.md section 6; 8.1 parse-back; 8.5 blind solve).

500 rows: F1 gen3_rule_chain, F2 gen3_tool_guard, F3 gen3_state_track, F5 gen3_lead_score, F6 gen3_def_literal, 100
each, from dev_holdout-distribution latents (each family's devx export), rendered by golden_src/gen3/dx_*.py (new
renderers and question wordings written from the latent schemas and the SPEC only). Labels come from each family's
shared decide(); every row's gold is re-derived from its assembled text by R's own parse-back (100% required, else the
build stops). mv_core.run_checks runs on each family's devx part (report only: devx is report-only data).

  ../.venv/bin/python yn2b/build_devx.py                       # build + checks, print the report (writes nothing)
  ../.venv/bin/python yn2b/build_devx.py --write [--overwrite]  # also write yn2b_raw/dev/<key>__devx.jsonl, defs,
                                                                 # MANIFEST records and yn2b/devx_report.json
  ../.venv/bin/python yn2b/build_devx.py --blind-out DIR        # write the gold-free blind sheets (50 rows / family)
  ../.venv/bin/python yn2b/build_devx.py --score-blind yn2b/devx_blind_answers.json [--write]
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import sys
from pathlib import Path

LEAN = Path(__file__).resolve().parents[1]
GEN3 = LEAN / "golden_src" / "gen3"
if str(GEN3) not in sys.path:
    sys.path.insert(0, str(GEN3))
import mv_core as mv  # noqa: E402
import dx_common as dx  # noqa: E402

MODULES = {"gen3_rule_chain": "dx_rule_chain", "gen3_tool_guard": "dx_tool_guard",
           "gen3_state_track": "dx_state_track", "gen3_lead_score": "dx_lead_score",
           "gen3_def_literal": "dx_def_literal"}
REPORT = LEAN / "yn2b" / "devx_report.json"
BLIND = LEAN / "yn2b" / "devx_blind.json"
N_BLIND = 50


def module(key: str):
    return importlib.import_module(MODULES[key])


def build(keys, check_tz=True) -> dict:
    out = {}
    for k in keys:
        out[k] = dx.build_family(module(k), check_tz=check_tz)
    return out


def family_report(b: dx.Built) -> dict:
    ch = b.checks
    failed = [k for k, v in ch.items() if isinstance(v, dict) and v.get("ok") is False]
    return {"rows": len(b.rows), "summary": dx.summary(b.rows), "parse_back": b.agree,
            "checks_ok": ch.get("ok"), "checks_failed": failed,
            "checks": {k: ch[k] for k in failed}, "plan": b.plan_report,
            "rejects": dict(b.fb.rejects)}


def blind_sheets(built: dict, n=N_BLIND) -> dict:
    return {k: dx.blind_sheet(b.golden, n, f"devx-blind:{k}") for k, b in built.items()}


def score_blind(built: dict, answers: dict) -> dict:
    """answers: {family key: {golden id: answer}} (yes/no rows: "yes"/"no"; choice rows: the option text)."""
    out = {}
    for k, ans in answers.items():
        gold = {g["id"]: g for g in built[k].golden}
        rows, hit, miss = 0, 0, []
        for gid, a in ans.items():
            g = gold[gid]
            want = ("yes" if g["gold"] == 1 else "no") if g["qtype"] == "noul" else g["gold"]
            rows += 1
            if a == want:
                hit += 1
            else:
                miss.append({"id": gid, "answer": a, "gold": want, "tpl": g["meta"]["tpl"], "tier": g["meta"]["tier"]})
        out[k] = {"rows": rows, "agree": hit, "share": round(hit / max(1, rows), 4), "misses": miss}
    return out


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--families", default=",".join(MODULES), help="comma list of family keys")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--blind-out", default="", help="directory for gold-free blind sheets (outside data/)")
    ap.add_argument("--score-blind", default="", help="answers JSON to score against gold")
    a = ap.parse_args(argv)
    keys = [k for k in a.families.split(",") if k]
    built = build(keys)
    rep = {k: family_report(b) for k, b in built.items()}
    print(json.dumps({k: {"rows": v["rows"], "parse_back": {x: v["parse_back"][x] for x in
                                                            ("rows", "agree", "disagree", "proj_mismatch")},
                          "yes_share": v["summary"]["yes_share_yn_jb"], "qkind": v["summary"]["qkind"],
                          "checks_failed": v["checks_failed"]} for k, v in rep.items()}, indent=1))
    if a.blind_out:
        d = Path(a.blind_out)
        d.mkdir(parents=True, exist_ok=True)
        for k, sheet in blind_sheets(built).items():
            (d / f"blind_{k}.json").write_text(json.dumps(sheet, indent=1, ensure_ascii=False))
        print("blind sheets written to", d)
    blind = None
    if a.score_blind:
        answers = json.loads(Path(a.score_blind).read_text())
        blind = score_blind(built, {k: v for k, v in answers.items() if k in built})
        print(json.dumps({k: {x: v[x] for x in ("rows", "agree", "share")} for k, v in blind.items()}, indent=1))
    if a.write:
        written = {}
        for k, b in built.items():
            written.update(b.fb.write(parts=("devx",), tool="golden_src/gen3/" + MODULES[k] + ".py",
                                      overwrite=a.overwrite))
        full = {"families": rep, "written": {mv._rel(Path(p)): s for p, s in written.items()}}
        if REPORT.exists() and not a.overwrite:
            raise SystemExit(f"{REPORT} exists; pass --overwrite")
        REPORT.write_text(json.dumps(full, indent=1, default=str) + "\n")
        mv.manifest_append({"tool": "yn2b/build_devx.py", "key": "devx", "part": "devx_report",
                            "path": mv._rel(REPORT), "rows": sum(v["rows"] for v in rep.values()),
                            "sha256": sha(REPORT)})
        print("wrote", mv._rel(REPORT))
        if blind is not None:
            if BLIND.exists() and not a.overwrite:
                raise SystemExit(f"{BLIND} exists; pass --overwrite")
            BLIND.write_text(json.dumps({"answers_file": a.score_blind, "answers_sha256": sha(Path(a.score_blind)),
                                         "results": blind}, indent=1) + "\n")
            mv.manifest_append({"tool": "yn2b/build_devx.py", "key": "devx", "part": "devx_blind",
                                "path": mv._rel(BLIND), "rows": sum(v["rows"] for v in blind.values()),
                                "sha256": sha(BLIND)})
            print("wrote", mv._rel(BLIND))
    return built, rep


if __name__ == "__main__":
    main()
