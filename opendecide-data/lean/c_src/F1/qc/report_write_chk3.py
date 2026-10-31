"""check:F1 (c-lanes-v3) independent checker, check round 3 report on the pass-B pools (no row text)."""
import json, hashlib, os, shutil, time
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def rows(p): return sum(1 for _ in open(p))
T0 = max(os.path.getmtime("out/candidates_r1.jsonl"), os.path.getmtime("out/qc_sample.jsonl"))
def J(p, fresh=False):
    if fresh and (not os.path.exists(p) or os.path.getmtime(p) < T0): return None
    try: return json.load(open(p))
    except Exception: return None
if os.path.exists("qc/QC_REPORT.json") and not os.path.exists("qc/QC_REPORT_r3pre.json"):
    shutil.copy("qc/QC_REPORT.json", "qc/QC_REPORT_r3pre.json")
pools = {f"out/{n}": {"sha256": sha(f"out/{n}"), "rows": rows(f"out/{n}")} for n in
         ["candidates_r1.jsonl", "candidates_r1.rel.jsonl", "candidates_r1.sidecar.jsonl", "qc_sample.jsonl",
          "qc_sample.rel.jsonl", "qc_sample.sidecar.jsonl", "mixdev_S5.jsonl", "mixdev_S5.sidecar.jsonl"]}
man = J("out/MANIFEST.json")
man_ok = all(man["files"][k.split("/")[1]]["sha256"] == v["sha256"] for k, v in pools.items())
G = {}
g6 = J("qc/g6_r2_qc_sample.json", True)
G["G6"] = {"pass": None if g6 is None else bool(g6.get("pass")), "file": "qc/g6_r2_qc_sample.json",
           "rule": "5-fold CV grouped by card; each view <= chance + 2 pp; (d) metadata = model-visible only"}
if g6:
    G["G6"]["best"] = {p: {k: (v.get("best") if isinstance(v, dict) else None) for k, v in g6.get(p, {}).items()
                           if isinstance(v, dict) and "best" in v} for p in ("yes_no", "choice")}
    G["G6"]["chance"] = {p: g6.get(p, {}).get("chance") or g6.get(p, {}).get("bar") for p in ("yes_no", "choice")}
g7 = {n: J(f"qc/g7_{n}.json", True) for n in ("candidates_r1", "qc_sample")}
G["G7"] = {"pass": None if None in g7.values() else all(v.get("pass") for v in g7.values()),
           "files": [f"qc/g7_{n}.json" for n in g7]}
for n, v in g7.items():
    if v: G["G7"][n] = {k: (len(v[k]) if isinstance(v.get(k), list) else v.get(k)) for k in v
                        if k in ("pass", "yn_literal_fail", "yn_card_fail", "choice_fail")}
g8 = J("qc/g8_candidates_r1.json", True); g8v3 = J("qc/g8v3_candidates_r1.json", True)
e = {"rule_source": "A19.1 adopted (c_build/g8v2/A19_ADOPTED): choice part judged by G8v3 (p > 0.009); yes/no part "
     "does not gate (report raw share and G8v3 p only)"}
if g8:
    gb = g8.get("grouped_by_card", {})
    e["old_raw_spec"] = {"file": "qc/g8_candidates_r1.json", "rule": "predictable share < 10%",
                         "grouped_by_card": {k: gb.get(k) for k in ("predictable_share", "yes_no_share", "choice_share")},
                         "instance_level_share": g8.get("instance_level", {}).get("predictable_share"),
                         "pass_spec": gb.get("predictable_share", 1) < 0.10}
if g8v3:
    P = g8v3["parts"]
    def part(p):
        t = P[p].get("test", {}); r = P[p].get("real", {})
        return {"n_rows": P[p].get("n_rows"), "share": r.get("share"), "acc": r.get("acc"), "p": t.get("p"),
                "K": t.get("K"), "verdict": t.get("verdict"), "pass": P[p].get("pass")}
    e["g8v3"] = {"file": "qc/g8v3_candidates_r1.json", "pool_sha256": g8v3.get("pool_sha256"),
                 "tool_sha256": g8v3.get("tool_sha256"), "choice": part("choice"), "yes_no_report_only": part("yes_no"),
                 "old_rule": g8v3.get("old_rule")}
    e["pass"] = bool(P["choice"].get("pass")) and g8v3.get("pool_sha256") == pools["out/candidates_r1.jsonl"]["sha256"]
else:
    e["pass"] = None
G["G8"] = e
for n in ("candidates_r1", "qc_sample"):
    d = J(f"qc/g10_{n}.json"); C = d.get("checks", d)
    G.setdefault("G10", {"files": [], "failed": {}})["files"].append(f"qc/g10_{n}.json")
    G["G10"]["failed"][n] = d.get("failed")
    G["G10"].setdefault("pool_pass", {})[n] = d.get("pass")
    det = {}
    for k in d.get("failed", []):
        v = C.get(k, {})
        if k == "longest_option_gold":
            det[k] = {g: v["groups"][g] for g in v.get("outside_2pp_n_ge_100", [])}
        elif k == "role_rate":
            det[k] = {g: v["cells"][g] for g in v.get("outside_2pp_n_ge_200", [])}
        else:
            det[k] = {kk: vv for kk, vv in v.items() if kk != "pass"}
    G["G10"].setdefault("detail", {})[n] = det
G["G10"]["pass"] = all(G["G10"]["pool_pass"].values())
g11 = J("qc/g11_candidates_r1.json"); G["G11"] = {"pass": g11.get("pass"), "file": "qc/g11_candidates_r1.json",
    "wordings_per_card_min": g11.get("wordings_per_card_min", (g11.get("stats") or {}).get("wordings_per_card_min"))}
g12 = J("qc/g12.json"); G["G12"] = {"pass": g12["pass"], "file": "qc/g12.json", "rows": g12["rows"],
    "exact_duplicate_rows": g12["exact_duplicate_rows"], "near_dup_pairs_outside_group": g12["near_dup_pairs_outside_group"]}
g15 = J("qc/g15_g18.json"); G["G15"] = {"pass": g15["G15"]["pass"], "file": "qc/g15_g18.json"}
G["G18"] = {"pass": g15["G18"]["pass"], "file": "qc/g15_g18.json"}
sr = J("tmp/sealed_results.json"); sm = {n: J(f"tmp/{n}.sealedqc.jsonl.summary.json") for n in ("candidates_r1", "qc_sample", "mixdev_S5")}
G["sealed_check"] = {"pass": all(sr[n]["rc"] == 0 and sr[n]["rows_hit"] == 0 for n in sm) and
                     all(sm[n]["input_sha256"] == pools[f"out/{n}.jsonl"]["sha256"] for n in sm),
                     "rows_hit": {n: sr[n]["rows_hit"] for n in sm}, "note": "summaries' input_sha256 = current pools"}
G["G5"] = {"pass": None, "status": "G5 deferred (A24): script gates fail", "earlier_read": "qc/g5.json (older pools)"}
script = ["G6", "G7", "G8", "G10", "G11", "G12", "G15", "G18", "sealed_check"]
failed = [g for g in script if G[g]["pass"] is False]
pending = [g for g in script if G[g]["pass"] is None]
R = {"family": "F1", "round": 1, "checker": "check:F1 (workflow c-lanes-v3), independent, check round 3",
     "pools": pools, "manifest_matches_pools": man_ok, "manifest_written_utc": man.get("written_utc"),
     "gates": G, "failed_gates": failed + (["G5 (deferred, A24)"] if failed else []), "pending_gates": pending,
     "g5_rule": "A24: G5 only after every script gate passes; pass needs 0 clearly wrong, ambiguous <= 6",
     "pass": False if (failed or pending) else None,
     "previous_report": "qc/QC_REPORT_r3pre.json (04:29Z report on the older pools)",
     "updated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
json.dump(R, open("qc/QC_REPORT.json", "w"), indent=1)
print(json.dumps({"failed": failed, "pending": pending, "manifest_ok": man_ok, "G8": {k: e.get(k) for k in ("pass",)},
                  "pass": R["pass"]}))
