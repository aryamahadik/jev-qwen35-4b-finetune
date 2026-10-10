"""(d) Score OHS-3 with score_ohs3.py (unchanged) and build the final table vs Jev for every win condition.

  ../.venv/bin/python prep89/ohs3_final_table.py --config prep89/ohs3_config.json --go \\
      [--timing logs/ohs3/timing/ohs3_timing/summary.json] [--models q35_4b_pxE_cal,q35_4b_pxE_1v_cal,...] \\
      [--timing-extra 2b=logs/ohs3/timing/ohs3_timing_2b/summary.json,cascade=logs/ohs3/timing/ohs3_timing_cascade/summary.json] \\
      [--load-test logs/ohs3/load_test/ohs3_timing_c1/summary.json]
  dry run: ... --root prep89/dryrun/root --config prep89/dryrun/config_dryrun.json --allow-deviation

Step 1 runs score_ohs3.py once for all OpenDecide configurations (every model ever run on OHS-3 is reported, rule 4),
with the two Jev runs, --half all, 10,000 resamples (the PREREG settings; real mode refuses --allow-deviation).
Step 2 writes results_ohs3/final_table.{json,md}: the headline model (the first --models entry = the pre-registered
primary configuration of the shipped 4B) against Jev on
  accuracy (micro, macro; PREREG "beats"/"matches"), Brier on yes/no, consistency (complement violation, option-order
  drift), speed (S1 p50 with CI, S2 p95; from ohs3_timing.py), cost (C1 at the pre-registered utilisation and at
  100%, C2 as-run, C3 JevBench formula), and the conditions OHS-3 does not measure (hijack/injection, JevBench),
plus every secondary endpoint, Jev's run-to-run numbers, missing answers and non-pinned rows. Aggregates only.
--timing must be the HEADLINE system's pass (speed.headline_system; checked by the system name in the summary);
--timing-extra adds the other systems' passes (2B, cascade) as descriptive speed rows. C1 uses the all-in $/h times
the hosting.region multiplier, and the sustained throughput of the dev load test (--load-test, when
cost.od_decisions_per_hour_sustained = "load_test"; the summary must be for this config and the headline system,
and valid: length match and token check passed) or the pre-registered number. Token rows: both systems' measured
input/output tokens per call on the OHS-3 calls (from the timing pass).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ohs3_lib as L  # noqa: E402


def num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def load_test_dph(cfg, load_test, head_system):
    """(sustained decisions per hour or None, why): from the pre-registered number, or from the dev load test's summary
    when cost.od_decisions_per_hour_sustained = "load_test" (it must be for this config, the headline system, valid)."""
    dph = cfg["cost"].get("od_decisions_per_hour_sustained")
    if dph != "load_test":
        return (dph if num(dph) else None), "pre-registered number"
    if not load_test:
        return None, "cost says load_test but no --load-test summary was given"
    bad = []
    if load_test.get("config_sha256") != cfg["_sha256"]:
        bad.append("load test made under another config")
    if load_test.get("system") != head_system:
        bad.append(f"load test of {load_test.get('system')}, headline system is {head_system}")
    if not load_test.get("valid_for_c1"):
        bad.append("load test not valid for C1: " + "; ".join(load_test.get("invalid_reasons") or []))
    if bad:
        return None, "; ".join(bad)
    return load_test.get("sustained_decisions_per_hour"), (f"dev load test {load_test.get('name')} (KS "
                                                           f"{(load_test.get('match') or {}).get('ks')}, at concurrency "
                                                           f"{load_test.get('sustained_at_concurrency')})")


def cost_block(cfg, timing, od_meta, load_test=None):
    c = cfg["cost"]
    out = {}
    jev_tok = (timing or {}).get("jev", {}).get("input_tokens_per_call_mean")
    jev_out = (((timing or {}).get("jev", {}).get("tokens") or {}).get("output_tokens") or {}).get("mean") or 0
    jev_1k = ((jev_tok * c["jev_usd_per_m_input"] + jev_out * float(c.get("jev_usd_per_m_output") or 0)) / 1e3
              if jev_tok else None)  # $ per 1,000 calls (one decision each)
    head = (cfg.get("speed") or {}).get("headline_system", "4b")
    dph, why = load_test_dph(cfg, load_test, head)
    base, util = c.get("od_usd_per_hour"), c.get("utilisation_for_claim")
    region = (cfg.get("hosting") or {}).get("region", "any")
    mult = L.region_multiplier(region)
    rate = base * mult if num(base) else None
    if num(dph) and num(rate):
        od100 = rate / dph * 1000
        odu = od100 / util if num(util) and util > 0 else None
        out["C1"] = {"od_usd_per_1k_at_100pct": od100, "od_usd_per_1k_at_claim_util": odu, "claim_utilisation": util,
                     "jev_usd_per_1k_list": jev_1k, "od_decisions_per_hour_sustained": dph, "throughput_source": why,
                     "od_rate_usd_h": rate, "od_rate_base_usd_h": base, "region": region, "region_multiplier": mult,
                     "verdict": None if odu is None or jev_1k is None else ("cheaper" if odu < jev_1k else "not cheaper"),
                     "note": "OD = all-in $/h x region multiplier / sustained decisions per hour (dev load test); Jev = "
                             "list price x measured tokens (OHS-3 timing run usage)"}
    else:
        out["C1"] = {"verdict": None, "jev_usd_per_1k_list": jev_1k, "throughput_source": why,
                     "note": "needs the sustained throughput (dev load test) and the timing run"}
    run_s = None
    if timing and timing.get("wall", {}).get("first_utc") and cfg["decisions"].get("od_scored_run") == "served_h100":
        import datetime as dt
        f = lambda s: dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")  # noqa: E731
        run_s = (f(timing["wall"]["last_utc"]) - f(timing["wall"]["first_utc"])).total_seconds()
        rate_c2 = rate  # the served H100's all-in rate in its region
    elif od_meta:
        run_s = od_meta.get("read_s_this_session")
        rate_c2 = c.get("l4_usd_per_hour")
    else:
        rate_c2 = None
    if run_s is not None and num(rate_c2):
        n = (od_meta or {}).get("rows") or L.OHS3_CALLS
        out["C2"] = {"od_usd_per_1k_as_run": run_s / 3600 * rate_c2 / n * 1000, "run_s": run_s, "rate_usd_h": rate_c2,
                     "jev_usd_per_1k_list": jev_1k,
                     "note": "OD: wall time of the scored run x hourly rate / rows; L4 batch time if D1 = L4_batch "
                             "(resumed sessions: this session only)"}
    c3o, c3j = c.get("c3_od_usd_per_1k"), c.get("c3_jev_usd_per_1k")
    out["C3"] = {"od_usd_per_1k": c3o, "jev_usd_per_1k": c3j, "source": c.get("c3_source"),
                 "verdict": ("cheaper" if c3o < c3j else "not cheaper") if num(c3o) and num(c3j) else None}
    out["tokens_ohs3"] = {"od": ((timing or {}).get("od") or {}).get("tokens"),
                          "jev": ((timing or {}).get("jev") or {}).get("tokens"),
                          "token_priced_usd_per_1k_calls": (timing or {}).get("token_priced_usd_per_1k_calls")}
    return out


def drift_by_twin_kind(root, head, jev_tags):
    """Descriptive (no CI): option-order drift split by how the _perm twin was made, reversed or rotated
    (PREREG_OHS3: 149 reversed, 155 rotated). With the A5 2-view readout (given order + exact reversal) a reversed
    twin is read in the same two orders as its base row, so its drift is ~0 by construction; the rotated twins are
    the informative part. Same drift rule as score_ohs3.py (its own decision(): a tie or a missing answer = drift);
    Jev = mean of its runs per pair. Reads the options lists of the scored rows; prints and writes rates only."""
    sys.path.insert(0, str(L.LEAN))
    import score_ohs3 as S  # read-only import (main() is not run)
    rows = {r["id"]: r for r in L.read_jsonl(root / "data" / f"{L.SPLIT}.jsonl")}
    pd = root / f"preds_{L.SPLIT}"

    def load(n):
        p = pd / f"{n}.jsonl"
        return {o["id"]: o["probs"] for o in L.read_jsonl(p)} if p.exists() else None

    P_od, P_jev = load(head), {t: load(t) for t in jev_tags}
    P_jev = {t: v for t, v in P_jev.items() if v is not None}
    out = {}
    for rel in L.read_jsonl(root / "data" / f"{L.SPLIT}_relations.jsonl"):
        if rel["type"] != "equiv":
            continue
        a, b = rows[rel["a"]], rows[rel["b"]]
        if a["qtype"] != "choice" or b["qtype"] != "choice":
            continue
        base, twin = (b, a) if a["id"].endswith("_perm") else (a, b)
        o, t = base["options"], twin["options"]
        n = len(o)
        kind = ("reversed" if t == o[::-1] else
                "rotated" if any(t == o[k:] + o[:k] for k in range(1, n)) else "other")

        def drift(P):
            da, db = S.decision(base, P.get(base["id"])), S.decision(twin, P.get(twin["id"]))
            return float(da is None or db is None or da != db)

        d = out.setdefault(kind, {"pairs": 0, "od": 0.0, "jev_mean": 0.0, "jev_runs": {t_: 0.0 for t_ in P_jev}})
        d["pairs"] += 1
        if P_od is not None:
            d["od"] += drift(P_od)
        for tg, P in P_jev.items():
            v = drift(P)
            d["jev_runs"][tg] += v
            d["jev_mean"] += v / len(P_jev)
    for d in out.values():
        k = d["pairs"]
        d["od"] = d["od"] / k if P_od is not None else None
        d["jev_mean"] = d["jev_mean"] / k if P_jev else None
        d["jev_runs"] = {t_: v / k for t_, v in d["jev_runs"].items()}
    return out


def speed_rows(add, timing, label):
    p = timing["paired"]
    add(f"speed (faster than Jev){label}", "S1 end-to-end p50 per call (ms)", timing["od"]["client_ms"]["p50"],
        timing["jev"]["client_ms"]["p50"], p["p50"]["diff_jev_minus_od_ms"], p["p50"]["ci95"],
        timing["S1_faster"]["verdict"], timing["S1_faster"]["verdict"] == "faster",
        f"needs CI above 0 AND p95 lower; complete={timing['S1_faster']['complete']}; failures OD "
        f"{timing['od']['failed_calls']} / Jev {timing['jev']['failed_calls']}; served path {timing['od'].get('paths')}")
    add(f"speed (faster than Jev){label}", "S2 end-to-end p95 per call (ms)", timing["od"]["client_ms"]["p95"],
        timing["jev"]["client_ms"]["p95"], p["p95"]["diff_jev_minus_od_ms"], p["p95"]["ci95"],
        "lower" if p["p95"]["diff_jev_minus_od_ms"] > 0 else "not lower", p["p95"]["diff_jev_minus_od_ms"] > 0,
        "descriptive")


def build(score, timing, cfg, head, jev_coll, od_meta, extra_timing=None, load_test=None):
    M = score["models"][head]
    P, Sx = M["primary"], M["secondary"]
    rows = []

    def add(cond, metric, od, jev, diff, ci, verdict, win, note=""):
        rows.append({"condition": cond, "metric": metric, "od": od, "jev": jev, "diff_od_better_positive": diff,
                     "ci95": ci, "verdict": verdict, "win": win, "note": note})

    for k, lab in (("micro", "accuracy micro, 1,852 base rows (pp)"), ("macro", "accuracy macro, 13 tasks (pp)")):
        v = P[k]
        add("accuracy >= Jev", lab, v["od"], v["jev"], v["diff"], v["ci95"], v["verdict"]["label"],
            v["verdict"]["label"] == "beats" or (v["verdict"]["matches"] and v["diff"] >= 0),
            f"Holm p {v['p_holm']:.4f}; PREREG primary")
    v = P["brier_yesno"]
    add("calibration", "Brier, 716 yes/no base rows", v["od"], v["jev"], v["diff"], v["ci95"], v["verdict"]["label"],
        v["verdict"]["label"] == "beats", "PREREG primary; diff = Jev - OD")
    for k, lab in (("complement_violation", "complement violation, 300 _neg pairs"),
                   ("option_order_drift", "option-order drift, 304 _perm pairs")):
        v = Sx.get(k)
        if v:
            add("consistency", lab, v["od"], v["jev"], v["diff"], v["ci95"], v["verdict"], v["verdict"] == "od_better",
                f"BH q {v['q_bh']}; diff = Jev - OD")
    if timing and "paired" in timing:
        speed_rows(add, timing, "")
    else:
        add("speed (faster than Jev)", "S1/S2", None, None, None, None, "not measured", None, "no timing summary given")
    extra_rows = []

    def add_extra(cond, metric, od, jev, diff, ci, verdict, win, note=""):  # other systems: descriptive, never a win
        extra_rows.append({"condition": cond, "metric": metric, "od": od, "jev": jev, "diff_od_better_positive": diff,
                           "ci95": ci, "verdict": verdict, "win": None, "won_if_headline": win, "note": note})

    for key, tsum in sorted((extra_timing or {}).items()):
        if "paired" in tsum:
            speed_rows(add_extra, tsum, f", {key} ({tsum.get('model')}; not the headline)")
        if (tsum.get("od") or {}).get("cascade"):
            cs = tsum["od"]["cascade"]
            add_extra(f"cascade routing, {key}", "routed share of rows (served pass)", cs["routed_share"], None, None,
                      None, f"{cs['routed_rows']}/{cs['rows']} rows", None,
                      f"client p50 routed {cs['client_ms_routed_calls'].get('p50')} ms vs not routed "
                      f"{cs['client_ms_not_routed_calls'].get('p50')} ms")
    cost = cost_block(cfg, timing, od_meta, load_test)
    c1 = cost["C1"]
    add("cost (cheaper than Jev)", f"C1 $/1K decisions at {c1.get('claim_utilisation')} utilisation",
        c1.get("od_usd_per_1k_at_claim_util"), c1.get("jev_usd_per_1k_list"), None, None, c1.get("verdict"),
        None if c1.get("verdict") is None else c1["verdict"] == "cheaper",
        f"{c1.get('note', '')}; throughput: {c1.get('throughput_source')}; rate {c1.get('od_rate_usd_h')} $/h "
        f"({c1.get('region')} x{c1.get('region_multiplier')})")
    tk = cost["tokens_ohs3"]
    if tk["od"] and tk["jev"]:
        add("cost (cheaper than Jev)", "input tokens per call on the OHS-3 calls (mean)",
            tk["od"]["input_tokens"].get("mean"), tk["jev"]["input_tokens"].get("mean"), None, None, "descriptive", None,
            f"counted on OD {tk['od']['input_tokens'].get('calls_with_count')}/{tk['od'].get('calls_answered')}, Jev "
            f"{tk['jev']['input_tokens'].get('calls_with_count')}/{tk['jev'].get('calls_answered')} answered calls; "
            f"OD all reads / identity read = {tk['od'].get('all_reads_over_first_view')}; output tokens per call: OD "
            f"{tk['od']['output_tokens'].get('mean')}, Jev {tk['jev']['output_tokens'].get('mean')}; token-priced $/1K "
            f"calls (descriptive): {tk.get('token_priced_usd_per_1k_calls')}")
    c3 = cost["C3"]
    add("cost (cheaper than Jev)", "C3 JevBench v1.5.4 formula $/1K", c3["od_usd_per_1k"], c3["jev_usd_per_1k"], None,
        None, c3["verdict"], None if c3["verdict"] is None else c3["verdict"] == "cheaper", "secondary")
    add("hijack / injection resistance", "not measured on OHS-3 (no attack rows)", None, None, None, None, "n/a", None,
        "evidence elsewhere: logs/gate4b/look_ship1.txt (g) jagged/OPI vs REF; ledger E0 jagged audit vs Jev")
    add("JevBench", "no submission (owner rule)", None, None, None, None, "n/a", None,
        "public-item runs are development results (A5 item 3)")
    measured = [r for r in rows if r["win"] is not None]
    return {"headline_model": head, "rows": rows, "extra_system_rows": extra_rows, "cost": cost,
            "all_measured_won": all(r["win"] for r in measured),
            "not_won": [f"{r['condition']}: {r['metric']}" for r in measured if not r["win"]],
            "secondary": {k: {kk: v[kk] for kk in ("od", "jev", "diff", "ci95", "q_bh", "verdict") if kk in v}
                          for k, v in Sx.items()},
            "mcnemar": M["mcnemar"], "descriptive": M["descriptive"],
            "od_answers": M["od_answers"], "jev": score["jev"], "deviations": score["deviations"],
            "jev_collection": jev_coll, "models_reported": sorted(score["models"]),
            "other_models_primary": {m: {k: {"od": v["od"], "diff": v["diff"], "ci95": v["ci95"],
                                             "verdict": v["verdict"]["label"]} for k, v in r["primary"].items()}
                                     for m, r in score["models"].items() if m != head}}


def fmt(x, nd=3):
    if x is None:
        return "-"
    if isinstance(x, list):
        return "[" + ", ".join(fmt(v, nd) for v in x) + "]"
    if isinstance(x, float):
        return f"{x:.{nd}f}"
    return str(x)


def markdown(T, real):
    L_ = [f"# OHS-3 final table: {T['headline_model']} vs Jev" + ("" if real else " (DRY RUN, synthetic data)"), ""]
    if T["deviations"]:
        L_ += [f"**Deviations recorded by score_ohs3.py:** {T['deviations']}", ""]
    L_ += ["| Win condition | Metric | OpenDecide | Jev | Diff (+ = OD better) | 95% CI | Verdict | Won |",
           "|---|---|---|---|---|---|---|---|"]
    for r in T["rows"]:
        won = "-" if r["win"] is None else ("yes" if r["win"] else "no")
        L_.append(f"| {r['condition']} | {r['metric']} | {fmt(r['od'])} | {fmt(r['jev'])} | "
                  f"{fmt(r['diff_od_better_positive'])} | {fmt(r['ci95'])} | {r['verdict']} | {won} |")
    for r in T.get("extra_system_rows") or []:
        L_.append(f"| {r['condition']} | {r['metric']} | {fmt(r['od'])} | {fmt(r['jev'])} | "
                  f"{fmt(r['diff_od_better_positive'])} | {fmt(r['ci95'])} | {r['verdict']} | n/a (not the headline) |")
    L_ += ["", f"**All measured win conditions won:** {T['all_measured_won']}."]
    fe = T.get("dev_fit_evidence")
    if isinstance(fe, list):
        L_ += ["", "**Dev-only evidence of the pre-registered T and cascade values:** "
               + "; ".join(f"{x['status']} {x['check'].split(':')[0]}" for x in fe) + "."]
    if T["not_won"]:
        L_ += ["Not won: " + "; ".join(T["not_won"]) + "."]
    L_ += ["", "## Secondary endpoints (BH family)", "", "| Endpoint | OD | Jev | Diff | 95% CI | q | Verdict |",
           "|---|---|---|---|---|---|---|"]
    for k, v in T["secondary"].items():
        vd = v.get("verdict")
        vd = vd["label"] if isinstance(vd, dict) else vd
        L_.append(f"| {k} | {fmt(v.get('od'))} | {fmt(v.get('jev'))} | {fmt(v.get('diff'))} | {fmt(v.get('ci95'))} | "
                  f"{fmt(v.get('q_bh'), 4)} | {vd} |")
    for k, v in T["mcnemar"].items():
        L_.append(f"| McNemar {k} | b={v['od_right_jev_wrong']} | c={v['od_wrong_jev_right']} | | | {fmt(v['q_bh'], 4)} | "
                  f"{v['verdict']} |")
    J = T["jev"]
    L_ += ["", "## Jev runs", ""]
    for n, v in J["per_run"].items():
        L_.append(f"- {n}: micro {fmt(v['micro_pct'], 2)}, macro {fmt(v['macro_pct'], 2)}, Brier {fmt(v['brier_yesno'], 4)}, "
                  f"missing base {v['missing_base']} / twin {v['missing_twin']}, rows not from {L.PINNED_JEV}: "
                  f"{v['rows_not_pinned_model']}")
    if "run_agreement" in J:
        L_.append(f"- run-to-run agreement: decision {fmt(J['run_agreement']['decision'], 4)}, correctness "
                  f"{fmt(J['run_agreement']['correctness'], 4)}")
    dk = T.get("drift_by_twin_kind") or {}
    if dk:
        L_ += ["", "## Option-order drift by twin kind (descriptive, no CI)", "",
               "With the 2-view readout a reversed twin is read in its base row's two orders, so its drift is ~0 by "
               "construction; the rotated twins are the informative comparison.", "",
               "| Twin kind | Pairs | OD drift | Jev drift (mean of runs) |", "|---|---|---|---|"]
        for k, v in sorted(dk.items()):
            L_.append(f"| {k} | {v['pairs']} | {fmt(v['od'])} | {fmt(v['jev_mean'])} |")
    oa = T["od_answers"]
    L_ += [f"- OpenDecide answers: missing base {oa['missing_base']}, twin {oa['missing_twin']}, ties {oa['tie_base']}",
           "", "## Every OpenDecide configuration run on OHS-3 (rule 4)", ""]
    for m in T["models_reported"]:
        L_.append(f"- {m}" + (" (headline)" if m == T["headline_model"] else ""))
    for m, r in T["other_models_primary"].items():
        L_.append(f"  - {m}: " + "; ".join(f"{k} {fmt(v['od'])} (diff {fmt(v['diff'])}, {v['verdict']})" for k, v in r.items()))
    return "\n".join(L_) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=str(L.LEAN))
    ap.add_argument("--config", required=True)
    ap.add_argument("--models", default=None, help="comma list; default: <4b name>_cal, <4b>_1v_cal, and every other "
                                                    "model/cascade the config runs")
    ap.add_argument("--timing", default=None, help="summary.json of ohs3_timing.py: the HEADLINE system's pass")
    ap.add_argument("--timing-extra", default=None, help="key=summary.json,... other systems' passes (descriptive rows)")
    ap.add_argument("--load-test", default=None, help="summary.json of load_test_c1.py (C1 throughput)")
    ap.add_argument("--boot", type=int, default=10000)
    ap.add_argument("--allow-deviation", action="store_true", help="dry run only")
    ap.add_argument("--skip-score", action="store_true", help="reuse results_ohs3/score_ohs3_all.json")
    ap.add_argument("--go", action="store_true")
    a = ap.parse_args(argv)
    root = Path(a.root).resolve()
    real = L.is_real_ohs3(root)
    cfg = L.load_config(a.config, require_complete=True)
    if real:
        if not a.go:
            raise SystemExit("REAL scoring needs --go")
        if a.allow_deviation or a.boot != 10000:
            raise SystemExit("the reported run uses the PREREG settings: no --allow-deviation, --boot 10000")
        L.require_frozen(root)
    if a.models:
        models = [x for x in a.models.split(",") if x]
    else:
        ms = cfg["models"]
        models = [f"{ms['4b']['name']}_cal", f"{ms['4b']['name']}_1v_cal"]
        models += [f"{m['name']}_cal" for k, m in ms.items() if k != "4b" and m.get("run_on_ohs3") is True]
        if (cfg.get("cascade") or {}).get("run") is True:
            models.append(f"{cfg['cascade']['name']}_cal")
    out_score = root / f"results_{L.SPLIT}" / "score_ohs3_all.json"
    if not a.skip_score:
        cmd = [str(L.PY), str(L.LEAN / "score_ohs3.py"), "--root", str(root), "--split", L.SPLIT, "--half", "all",
               "--boot", str(a.boot), "--jev", ",".join(cfg["jev"]["scored_tags"]), "--out", str(out_score)]
        for m in models:
            cmd += ["--model", m]
        if a.allow_deviation:
            cmd.append("--allow-deviation")
        logf = root / "logs" / "ohs3" / "score_ohs3_stdout.txt"
        logf.parent.mkdir(parents=True, exist_ok=True)
        with open(logf, "w") as f:
            rc = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT).returncode
        if rc != 0:
            raise SystemExit(f"score_ohs3.py exited {rc}; see {logf}")
        L.blind_print(f"score_ohs3.py: {len(models)} configurations scored -> {out_score} (stdout {logf.name})")
    score = json.loads(out_score.read_text())
    timing = json.loads(Path(a.timing).read_text()) if a.timing else None
    head_sys = (cfg.get("speed") or {}).get("headline_system", "4b")
    head_name = cfg["cascade"]["name"] if head_sys == "cascade" else cfg["models"][head_sys]["name"]
    if timing is not None and timing.get("model") != head_name:
        raise SystemExit(f"--timing is the pass of {timing.get('model')}, but the headline system ({head_sys}) is "
                         f"{head_name}: give its pass as --timing and the others as --timing-extra")
    extra = {}
    for kv in [x for x in (a.timing_extra or "").split(",") if x]:
        k, pth = kv.split("=", 1)
        extra[k] = json.loads(Path(pth).read_text())
    load_test = json.loads(Path(a.load_test).read_text()) if a.load_test else None
    jev_coll = {}
    for t in cfg["jev"]["scored_tags"]:
        p = root / "logs" / "ohs3" / f"jev_collect_{t}.json"
        if p.exists():
            jev_coll[t] = {k: v for k, v in json.loads(p.read_text()).items() if k != "latency_ms_success_attempt"}
    head = models[0]
    mp = root / f"preds_{L.SPLIT}" / f"{head[:-4] if head.endswith('_cal') else head}.meta.json"
    od_meta = json.loads(mp.read_text()) if mp.exists() else None
    T = build(score, timing, cfg, head, jev_coll, od_meta, extra, load_test)
    T["drift_by_twin_kind"] = drift_by_twin_kind(root, head, cfg["jev"]["scored_tags"])
    # the dev-only evidence of every pre-registered T and cascade rule (t_rule_check.py / cascade_rule_fit.py logs)
    keys = [k for k, m in cfg["models"].items() if m.get("run_on_ohs3") is True]
    keys += ["cascade"] if (cfg.get("cascade") or {}).get("run") is True else []
    T["dev_fit_evidence"] = ([{"status": st, "check": w, "detail": d} for st, w, d in L.check_fit_logs(cfg, keys)]
                             if real else "dry run: the dry config's values are dummies (no fit logs)")
    T.update(real=real, config_sha256=cfg["_sha256"], score_file=str(out_score), timing_file=a.timing, utc=L.utc())
    od = root / f"results_{L.SPLIT}"
    (od / "final_table.json").write_text(json.dumps(T, indent=1, default=str))
    (od / "final_table.md").write_text(markdown(T, real))
    for r in T["rows"]:
        L.blind_print(f"  {r['condition'][:28]:28s} {r['metric'][:44]:44s} OD {fmt(r['od'])} Jev {fmt(r['jev'])} "
                      f"-> {r['verdict']} (won: {r['win']})")
    for k, v in sorted(T["drift_by_twin_kind"].items()):
        L.blind_print(f"  drift, {k} twins: {v['pairs']} pairs, OD {fmt(v['od'])}, Jev {fmt(v['jev_mean'])}")
    L.blind_print(f"all measured win conditions won: {T['all_measured_won']}; wrote {od}/final_table.md")
    return T


if __name__ == "__main__":
    main()
