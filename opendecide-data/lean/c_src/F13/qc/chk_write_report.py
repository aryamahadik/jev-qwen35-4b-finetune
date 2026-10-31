"""check:F13 (c-lanes-v3, independent checker): MERGE checker gate results into qc/QC_REPORT.json.
Keeps every builder key; adds "checker" {utc, pool_sha256 of the 6 out files, per-gate pass / files / failed parts},
"checker_pass", "checker_failed_gates". A gate file whose pool_sha256 differs from the file on disk counts as stale (fail).
G8 (A19.1 adopted): choice part gated by G8v3 (p > 0.009); yes/no part report-only; old raw share reported.
G5 (A24): run only if every script gate passes; otherwise recorded as deferred.
Usage: chk_write_report.py [--g5 qc/g5.json]"""
import hashlib
import json
import sys
import time
from pathlib import Path

F13 = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F13")
QC, OUT = F13 / "qc", F13 / "out"
FILES = ["candidates_r1.jsonl", "qc_sample.jsonl", "mixdev_S5.jsonl", "relations_candidates_r1.jsonl",
         "relations_qc_sample.jsonl", "relations_mixdev_S5.jsonl"]


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


SHA = {f: sha(OUT / f) for f in FILES}


def load(name):
    p = QC / name
    if not p.exists():
        return None, f"{name} missing"
    d = json.loads(p.read_text())
    pool = d.get("pool_sha256")
    src = Path(d.get("file") or d.get("pool") or "").name
    if pool and src in SHA and pool != SHA[src]:
        return d, f"{name} stale (pool {pool[:8]} != disk {SHA[src][:8]})"
    return d, None


def failed_parts(d):
    for k in ("pass_parts",):
        if isinstance(d.get(k), dict):
            return [p for p, v in d[k].items() if not v]
    out = []
    for part in ("yes_no", "choice"):
        if isinstance(d.get(part), dict):
            out += [f"{part}.{k}" for k, v in d[part].items() if isinstance(v, dict) and v.get("pass") is False]
    if "n_fail_choice" in d:
        out += [f"{k}={d[k]}" for k in ("n_fail_choice", "n_fail_yes_no_raw_multi_card", "n_fail_yes_no_card_adjusted")
                if d.get(k)]
    if "G15_pass" in d:
        out += [k for k in ("G15_pass", "G18") if not (d[k] if isinstance(d[k], bool) else d[k].get("pass", True))]
    if "exact_duplicates" in d:
        out += [k for k in ("exact_duplicates", "near_dup_pairs_outside_twin_sets",
                            "structure_hash_collisions_across_groups", "missing_structure_hash", "missing_format_style")
                if d.get(k)]
    return out


def gate(files, judge=None):
    res = {"files": [], "pass": True, "failed_parts": []}
    for f in files:
        d, err = load(f)
        res["files"].append(f)
        if err:
            res["pass"] = False; res["failed_parts"].append(err); continue
        ok, fp = judge(d) if judge else (bool(d.get("pass")), failed_parts(d))
        if not ok:
            res["pass"] = False
            res["failed_parts"].append({f: fp[:20]})
    return res


def g8_judge(d):
    parts = d.get("parts", {})
    ch = parts.get("choice")
    ok = bool(ch and ch.get("pass"))
    info = {p: {"verdict": v["test"].get("verdict"), "p": v["test"].get("p"), "K": v["test"].get("K"),
                "share": v["real"]["share"]} for p, v in parts.items()}
    return ok, ([] if ok else ["choice G8v3 p <= 0.009"]) + [{"report": info, "old_rule": d.get("old_rule")}]


def main():
    g5path = sys.argv[sys.argv.index("--g5") + 1] if "--g5" in sys.argv else None
    G = {
        "G6": gate(["g6_qc_sample.json"]),
        "G7": gate(["g7_candidates_r1.json", "g7_qc_sample.json"]),
        "G8": gate(["g8v3_candidates_r1.json"], g8_judge),
        "G10": gate(["g10_candidates_r1.json", "g10_qc_sample.json"]),
        "G11": gate(["g11_candidates_r1.json", "g11_qc_sample.json", "g11_mixdev_S5.json"]),
        "G12": gate(["g12_candidates_r1.json", "g12_qc_sample.json", "g12_mixdev_S5.json"]),
        "G15": gate(["g15_g18_candidates_r1.json", "g15_g18_qc_sample.json", "g15_g18_mixdev_S5.json"],
                    lambda d: (bool(d.get("G15_pass")), [] if d.get("G15_pass") else ["G15"])),
        "G18": gate(["g15_g18_candidates_r1.json", "g15_g18_qc_sample.json", "g15_g18_mixdev_S5.json"],
                    lambda d: ((lambda g: bool(g if isinstance(g, bool) else g.get("pass")))(d.get("G18")),
                               [] if (d.get("G18") is True or (isinstance(d.get("G18"), dict) and d["G18"].get("pass")))
                               else ["G18"])),
    }
    # G8 detail (report-only parts and old raw share) kept even when the choice part passes
    d8, _ = load("g8v3_candidates_r1.json")
    if d8:
        G["G8"]["report"] = g8_judge(d8)[1][-1]
    script_ok = all(v["pass"] for v in G.values())
    if g5path and script_ok:
        g5 = json.loads(Path(g5path).read_text())
        G["G5"] = {"files": [Path(g5path).name], "pass": bool(g5.get("pass")),
                   "clearly_wrong": g5.get("clearly_wrong"), "ambiguous": g5.get("ambiguous"), "n": g5.get("n")}
    else:
        G["G5"] = {"pass": False, "status": "G5 deferred (A24): script gates failed" if not script_ok else "G5 not run"}
    rep = json.loads((QC / "QC_REPORT.json").read_text())
    rep["checker"] = {"utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "agent": "check:F13 (c-lanes-v3)",
                      "pool_sha256": SHA, "g8_rule": "A19.1 adopted: choice G8v3 p > 0.009; yes/no report-only",
                      "gates": G}
    rep["checker_failed_gates"] = [k for k, v in G.items() if not v["pass"]]
    rep["checker_pass"] = not rep["checker_failed_gates"]
    (QC / "QC_REPORT.json").write_text(json.dumps(rep, indent=1, default=str))
    print(json.dumps({"checker_pass": rep["checker_pass"], "failed": rep["checker_failed_gates"]}))


if __name__ == "__main__":
    main()
