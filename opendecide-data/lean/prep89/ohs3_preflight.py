"""Pre-GO checklist for the one OHS-3 run (Mac, CPU, no network, no paid call). Prints PASS / FAIL / TODO lines and
the sha256 values the PREREG_OHS3 model amendment must quote.

  ../.venv/bin/python prep89/ohs3_preflight.py --config prep89/ohs3_config.json
  ../.venv/bin/python prep89/ohs3_preflight.py --config prep89/ohs3_config.template.json --template   (today: shows TODOs)

Never reads OHS-3 item text: it hashes the frozen files and checks git state only.
"""
from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ohs3_jev_collect as C  # noqa: E402
import ohs3_lib as L  # noqa: E402

FREEZE = ["PREREG_OHS3.md", "score_ohs3.py", "run_jev.py", "batchcal.py", "calibrate.py", "decoder_io.py", "prism_x.py",
          "writeblock.py", "hosting/modal_direct_host.py", "hosting/client_bench.py",
          "prep89/ohs3_lib.py", "prep89/ohs3_backends.py", "prep89/ohs3_od_run.py", "prep89/ohs3_serve.py",
          "prep89/ohs3_timing.py", "prep89/ohs3_jev_collect.py", "prep89/ohs3_final_table.py", "prep89/ohs3_cascade.py",
          "prep89/modal_ohs3_host.py", "prep89/load_test_c1.py", "prep89/t_rule_check.py", "prep89/cascade_rule_fit.py"]


L4_CODE = ["decoder_io.py", "prism_x.py", "writeblock.py", "calibrate.py", "batchcal.py", "prep89/ohs3_lib.py",
           "prep89/ohs3_backends.py", "prep89/ohs3_od_run.py"]


def tracked_clean(rel):
    if L.git("ls-files", "--error-unmatch", rel).returncode != 0:
        return "untracked"
    return "clean" if L.git("diff", "--quiet", "HEAD", "--", rel).returncode == 0 else "modified"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--template", action="store_true", help="report TODOs instead of failing on placeholders")
    a = ap.parse_args(argv)
    res = []

    def put(status, what, info=""):
        res.append((status, what, info))
        L.blind_print(f"{status:5s} {what}" + (f"  [{info}]" if info else ""))

    st = L.frozen_status(L.LEAN)
    put("PASS" if all(v is True for v in st.values()) else "FAIL", "OHS-3 files match PREREG_OHS3 frozen sha256", st)
    for fn in L.FROZEN_OHS3:
        s = tracked_clean(f"data/{fn}")
        put("PASS" if s == "clean" else "FAIL", f"data/{fn} committed and unchanged", s)
    for rel in FREEZE:
        s = tracked_clean(rel)
        put("PASS" if s == "clean" else "TODO", f"{rel} committed (sha256 {L.sha256_file(L.LEAN / rel)[:16]})", s)
    try:
        cfg = L.load_config(a.config, require_complete=not a.template)
        ph = L.placeholders({k: v for k, v in cfg.items() if not k.startswith("_")})
        put("TODO" if ph else "PASS", "config complete", f"{len(ph)} placeholders" if ph else cfg["_sha256"])
    except SystemExit as e:
        put("FAIL", "config complete", str(e)[:300])
        cfg = None
    if cfg is not None:
        rel = os.path.relpath(Path(a.config).resolve(), L.LEAN)
        s = tracked_clean(rel)
        put("PASS" if s == "clean" else "TODO", f"config {rel} committed", s)
        put("INFO", "config sha256 for the amendment", cfg["_sha256"])
        man = {"made_utc": L.utc(), "config": rel, "config_sha256": cfg["_sha256"],
               "files": {f: L.sha256_file(L.LEAN / f) for f in L4_CODE if (L.LEAN / f).exists()}}
        man["files"][rel] = cfg["_sha256"]
        for k, m in cfg["models"].items():  # the L4 run re-checks the T values against the same T fit log (sha256)
            tl = m.get("T_fit_log")
            if m.get("run_on_ohs3") is True and isinstance(tl, str) and not L.PLACEHOLDER.match(tl) \
                    and (L.LEAN / tl).exists():
                man["files"][tl] = L.sha256_file(L.LEAN / tl)
        if not a.template:
            (L.PREP / "ohs3_code_manifest.json").write_text(json.dumps(man, indent=1))
            put("INFO", "wrote prep89/ohs3_code_manifest.json (copy it to the L4 with the code)", len(man["files"]))
        for k, m in cfg["models"].items():
            if m.get("run_on_ohs3") is not True:
                continue
            name = m["name"]
            # the one local copy of each model: 4B-E in backups/gcp_models, C1 / C4 (Modal-trained) in backups/modal_models
            found = [p for p in (L.REPO / "backups" / d / name / "adapter_model.safetensors"
                                 for d in ("gcp_models", "modal_models")) if p.exists()]
            if found:
                for local in found:
                    sha = L.sha256_file(local)
                    put("PASS" if sha == m["adapter_sha256"] else "FAIL",
                        f"{k} {name}: local backup adapter sha256 = config ({local.parent.parent.name})", sha[:16])
            else:
                put("TODO", f"{k} {name}: no local backup; check the sha256 on the L4/Volume copy", m["adapter_sha256"][:16])
            if m.get("prism_x"):  # the PRISM-X weights are part of the served 2B
                for local in found:
                    try:
                        sha = L.check_prism_x_file(m, local.parent)
                        put("PASS", f"{k} {name}: local prism_x.safetensors sha256 = config.prism_x_sha256", sha[:16])
                    except SystemExit as e:
                        put("FAIL", f"{k} {name}: local prism_x.safetensors sha256 = config.prism_x_sha256", str(e)[:200])
            pd = L.LEAN / f"preds_{L.SPLIT}"
            exists = [p.name for p in pd.glob(f"{name}*")] if pd.exists() else []
            put("PASS" if not exists and not L.completed_runs(L.LEAN, name) else "FAIL",
                f"{k} {name}: never run on OHS-3 (rule 4)", exists[:3])
            if not a.template:
                logp = m.get("T_fit_log")
                ok_log = bool(logp) and (L.LEAN / logp).exists()
                put("PASS" if ok_log and tracked_clean(logp) == "clean" else "TODO",
                    f"{k}: T fit log exists and is committed (the dev-select evidence for T)",
                    f"{logp}: {tracked_clean(logp) if ok_log else 'missing'}")
        dec = cfg.get("decisions", {})
        if dec.get("od_scored_run") == "L4_batch":
            put("NOTE", "D1 = L4_batch: the amendment must say the H100 timing replay's outputs are used only for the "
                        "parity check, never scored (rule 4)")
        if dec.get("jev_timing") == "run1_via_harness":
            put("NOTE", "D2 = run1_via_harness: the amendment must say Jev run 1 is collected by ohs3_timing.py "
                        "(concurrency 1, run_jev.py's request objects) instead of run_jev.py")
        casc = cfg.get("cascade") or {}
        if casc.get("run") is True and not a.template:
            tl = casc.get("tau_fit_log")
            ok_tl = bool(tl) and (L.LEAN / tl).exists()
            put("PASS" if ok_tl and tracked_clean(tl) == "clean" else "TODO",
                "cascade: tau fit log exists and is committed (dev-select evidence for tau / w_big / route_on)",
                f"{tl}: {tracked_clean(tl) if ok_tl else 'missing'}")
            put("NOTE", "cascade: the amendment must name tau, w_big, route_on, whether the cascade is scored offline "
                        "(ohs3_cascade.py) or by its served pass (D1 = served_h100), and that a served cascade pass "
                        "re-reads OHS-3 with the 2B (every row) and the 4B (routed rows) as parts of the cascade only: "
                        "those reads are never scored as the 2B or the 4B (parity with their own runs is checked)")
        if not a.template:  # the dev-only evidence of every pre-registered T and cascade value (ohs3_lib.check_fit_logs):
            # each model that runs or is part of the cascade: T == its t_rule_check.py log; the cascade: tau / w_big /
            # route_on == its cascade_rule_fit.py log (same T logs, use rule passed); dev reads re-hashed here
            fk = [k for k, mm in cfg["models"].items() if mm.get("run_on_ohs3") is True]
            fk += ["cascade"] if casc.get("run") is True else []
            for r_ in L.check_fit_logs(cfg, fk, rehash=True):
                put(*r_)
        for k, mm in cfg["models"].items():
            if mm.get("run_on_ohs3") is True and mm.get("prism_x"):
                put("INFO", f"{k}: PRISM-X {mm['prism_x']} -> served eagerly (no CUDA graphs): name 'eager' in the "
                            "speed claim for this system")
        head = (cfg.get("speed") or {}).get("headline_system", "4b")
        put("INFO", "speed headline system (its pass is the S1 claim; only it may collect a scored Jev run)", head)
        reg = (cfg.get("hosting") or {}).get("region", "any")
        cst = cfg.get("cost") or {}
        if isinstance(cst.get("od_usd_per_hour"), (int, float)):
            put("INFO", "C1/C2 OD rate = od_usd_per_hour x region multiplier",
                f"{cst['od_usd_per_hour']} x {L.region_multiplier(reg)} ({reg}) = "
                f"{round(cst['od_usd_per_hour'] * L.region_multiplier(reg), 2)} $/h")
        if cst.get("od_decisions_per_hour_sustained") == "load_test":
            put("NOTE", "C1 throughput = prep89/load_test_c1.py (dev rows, length-matched to the timing pass's logged "
                        "token counts; config cost.load_test); run it with --then-load-test in the timing session")
    pd = L.LEAN / f"preds_{L.SPLIT}"
    jev = [p.name for p in pd.glob("jev*")] if pd.exists() else []
    put("PASS" if not jev else "INFO", "no Jev OHS-3 files yet (or a resumable partial run)", jev)
    C.load_env_file()
    put("PASS" if os.environ.get("OPENROUTER_API_KEY") else "FAIL", "OpenRouter key present (value not shown)")
    put("PASS" if not os.environ.get("TYPESAFE_API_KEY") else "FAIL", "no TYPESAFE_API_KEY (OHS-2 used OpenRouter)")
    put("INFO", "typesafe-sdk version", importlib.metadata.version("typesafe-sdk"))
    put("INFO", "Jev cost estimate (2 scored runs + 1 timing pass)", json.dumps(C.cost_estimate(runs=3)))
    n_fail = sum(s == "FAIL" for s, _, _ in res)
    n_todo = sum(s == "TODO" for s, _, _ in res)
    L.blind_print(f"\n{n_fail} FAIL, {n_todo} TODO" + ("  -> NOT READY" if n_fail or n_todo else "  -> READY for GO"))
    return 1 if n_fail or (n_todo and not a.template) else 0


if __name__ == "__main__":
    sys.exit(main())
