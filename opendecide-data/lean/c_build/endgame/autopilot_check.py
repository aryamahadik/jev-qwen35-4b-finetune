"""Read-only endgame status: per family PASS / NOT and the next RUNBOOK step (c_build/endgame/RUNBOOK.md).

Reads only: each family's out/candidates_r1 (+ relations) sha256, qc/QC_REPORT.json (pass + the sha binding, with the
mixer's own qc_binding rule), the crowd shard/label files (crowd_select.crowd_complete), crowd_r1/select_<F>.json,
logs/decontam_counts/<F>.json, the mixer outputs, the round-1 config, the pre-smoke / pre-read / relay records. It never
opens sealed_nd/, OHS-3, preds_ohs*, bench/longbench_v2 or any Jev output, starts nothing and spends nothing.

  cd lean && ../.venv/bin/python c_build/endgame/autopilot_check.py          (<= 40 lines)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CB = HERE.parent
LEAN = CB.parent
DATA = LEAN / "data"
sys.path.insert(0, str(CB))
import crowd_select as cs  # noqa: E402
import mixer  # noqa: E402
import decontam_g13  # noqa: E402
from mixio import sha256_file  # noqa: E402

FAMS = cs.FAMS + ["COMMIT"]
DECONTAM = LEAN / "logs/decontam_counts"
CONFIG = LEAN / "runs/q35_4b_c_r1.json"
INIT_SHA = "507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078"


def jload(p: Path):
    try:
        return json.loads(p.read_text())
    except Exception:  # noqa: BLE001
        return None


def family(fam: str) -> tuple[bool, str, str]:
    """(pass_all, status, next step) for one family."""
    f = cs.fam_files(fam)
    if not f["cand"].exists():
        return False, "no candidates_r1.jsonl", "lane: build (c-lanes-v3)"
    qc = jload(f["qc"]) if f["qc"].exists() else None
    if qc is None:
        return False, "no QC_REPORT.json", "lane: QC"
    if qc.get("pass") is not True:
        return False, f"QC pass={qc.get('pass')}", "lane: repair + QC"
    files = {f["cand"].name: f["cand"]} | ({f["rel"].name: f["rel"]} if f["rel"] else {})
    bind = mixer.qc_binding(qc, files)
    if bind:
        return False, "QC sha binding: " + bind[0][:60], "lane: re-run QC on the files on disk"
    sd = cs.CROWD_DIR / fam
    if not (sd / "shards.json").exists():
        return False, "QC PASS; no crowd shards", "RUNBOOK A (crowd read)"
    miss = cs.crowd_complete(fam)
    if miss:
        return False, "crowd: " + miss[0].split(": ", 1)[-1][:50], "RUNBOOK A3-A5 (crowd read / fetch)"
    if not (DECONTAM / f"{fam}.json").exists():
        return False, "crowd done; no G13 counts log", "RUNBOOK B (decontam_g13.py --fam, counts-only)"
    g13 = decontam_g13.log_problems([fam])
    if g13:
        return False, g13[0].split(": ", 1)[-1][:58], "RUNBOOK B (G13: re-run / owner items)"
    sel = jload(cs.OUT / f"select_{fam}.json")
    if sel is None:
        return False, "decontam done; no selection", "RUNBOOK C1 (crowd_select select)"
    if sel.get("candidates_sha256") != sha256_file(f["cand"]):
        return False, "selection is stale (candidates changed)", "RUNBOOK A (re-read) + C1"
    if not (sel.get("report") or {}).get("pass"):
        return False, "selection checks fail", "RUNBOOK C1 (owner review)"
    return True, "QC, crowd, decontam, selection", "ready for mixer --final"


def public() -> list[str]:
    out = []
    for rows_rel, res_rel in zip(mixer.PUBLIC_FILES, mixer.PUBLIC_RESERVE):
        b = rows_rel.split("/")[0]
        base = LEAN / "c_src/public"
        qc = jload(base / b / mixer.PUBLIC_QC)
        if qc is None:
            out.append(f"{b}: no QC record")
            continue
        files = {Path(x).name: base / x for x in (rows_rel, res_rel) if (base / x).exists()}
        bind = mixer.qc_binding(qc, files)
        out.append(f"{b}: {'PASS' if qc.get('pass') is True and not bind else 'NOT'}"
                   + ("" if not bind else f" ({bind[0][:50]})"))
    return out


def endgame() -> list[tuple[str, bool, str]]:
    """(item, ok, next step) for the train side, in RUNBOOK order."""
    man = jload(DATA / "c_parts/c_mix_r1_manifest.json")
    tr = DATA / "c_parts/c_train_r1.jsonl"
    mix_ok = bool(man) and tr.exists() and sha256_file(tr) == man["files"]["c_train_r1.jsonl"]["sha256"]
    cfg = jload(CONFIG) or {}
    fill = sorted(k for k, v in cfg.items() if isinstance(v, str) and v.startswith("FILL"))
    copy = jload(HERE / "COPY_RECORD.json") or {}
    smoke = jload(LEAN / "logs/pilot/speed_h100_mt8192_log_every-1.json")
    smoke_ok = bool(smoke) and not smoke.get("oom") and smoke.get("probe_ok") and (smoke.get("steps_run") or 0) >= 30
    pre = jload(LEAN / "c_build/preread/PREREAD_MANIFEST.json") or {}
    r1 = {t: (LEAN / f"logs/relay_q35_4b_c_r1_{t}.json").exists() for t in ("stopped_at_100", "stopped_at_300", "final")}
    chk = jload(HERE / "logs/r1_check_first100.json") or {}
    import re
    try:
        waived = set(re.findall(r"^[>\s*-]*OWNER-WAIVER r1-preflight ([a-z0-9_]+):", (LEAN / "PREREG_FINAL.md").read_text(),
                                re.M))
    except OSError:
        waived = set()
    return [
        ("tools: G13 counts-only decontam script", any((LEAN / p).exists() for p in ("c_build/decontam_g13.py",
                                                                                   "decontam_g13.py")),
         "BLOCKER: write it (RUNBOOK B spec)"),
        ("tools: gate_c.py (recipe 6.1)", (HERE / "gate_c.py").exists() or (LEAN / "gate_c.py").exists() or (CB / "gate_c.py").exists()
         or "gate_c" in waived,
         "BLOCKER: write + CPU-test it (RUNBOOK E spec)"),
        ("init adapter on aryamhd (sha 507d1c29)", copy.get("aryamhd", {}).get("q35_4b_main500k_init") == INIT_SHA,
         "RUNBOOK D0"),
        ("tools: recipe-5 stop-rule driver (B6) or owner waiver",
         ((HERE / "snap_monitor.py").exists() and (jload(HERE / "logs/snap_monitor_cputest.json") or {}).get("pass") is True)
         or "snapmon" in waived, "BLOCKER B6: write + CPU-test snap_monitor.py (RUNBOOK D5 contract) or owner waiver"),
        ("FAM-1 step-0 record on C1 (B8; A23: exists + reported, report-only)",
         isinstance((jload(HERE / "logs/fam1_step0_c1.json") or {}).get("wall_min"), (int, float)),
         "BLOCKER B8: L4 FAM-1 step-0 read (recipe 5); A23: controls need not pass"),
        ("G13 shared seeds (packs, formats) + final mix", not decontam_g13.log_problems(["packs", "formats",
                                                                                         "final_mix_r1"]),
         "RUNBOOK B (decontam_g13.py --set packs / --set formats / --final)"),
        ("sealed scorer CLI (B5) or owner waiver", __import__("score_nd_cli").verify(HERE / "SCORE_ND_CLI.json") is None
         or "score_nd_cli" in waived,
         "BLOCKER B5 (partial): sealed agent confirms the prediction format + printed fields (score_nd_cli.py confirm)"),
        ("pre-smoke (A20 d) on the partial mix", smoke_ok,
         "RUNBOOK P1 (p1_presmoke.sh: jaypatil-duke credit, after spend_guard GO)"),
        ("C1 pre-reads (A21 d)", bool(pre.get("complete")), "RUNBOOK P2-L4 (Google L4; P2-Modal needs an amendment)"),
        ("mixer --final output (sha matches manifest)", mix_ok, "RUNBOOK C2"),
        ("round-1 config filled (no FILL)", not fill, f"RUNBOOK C3 (fill {len(fill)} keys)"),
        ("round 1: segment 0-100 done", r1["stopped_at_100"], "RUNBOOK D (r1_chain.sh, after preflight GO)"),
        ("round 1: first-100 check GO", chk.get("decision") == "GO", "RUNBOOK D3"),
        ("round 1: segment 100-300 done", r1["stopped_at_300"], "RUNBOOK D4"),
        ("round 1: final", r1["final"], "RUNBOOK D5-D6"),
    ]


def main():
    rows = []
    for fam in FAMS:
        try:
            ok, status, nxt = family(fam)
        except SystemExit as e:
            ok, status, nxt = False, f"refused: {str(e)[:50]}", "lane: fix MANIFEST / relations"
        except Exception as e:  # noqa: BLE001
            ok, status, nxt = False, f"check error {type(e).__name__}", "inspect"
        rows.append((fam, ok, status, nxt))
        print(f"{fam:7s} {'PASS' if ok else 'NOT ':4s}  {status[:58]:58s} -> {nxt}")
    print("public  " + "; ".join(public()))
    n = sum(r[1] for r in rows)
    print(f"families ready for the mix: {n}/{len(rows)}")
    first = None
    for item, ok, nxt in endgame():
        print(f"  [{'x' if ok else ' '}] {item}" + ("" if ok else f"  -> {nxt}"))
        if not ok and first is None and not item.startswith("tools"):
            first = nxt
    nf = next((r for r in rows if not r[1] and "RUNBOOK" in r[3]), None)
    print("NEXT: " + (f"{nf[0]}: {nf[3]}" if nf else (first or "all done: RUNBOOK E (6.3 gate)")))


if __name__ == "__main__":
    main()
