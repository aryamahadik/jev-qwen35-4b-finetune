"""The 2B -> 4B cascade rule (FINETUNE_PLAN.md 5.3 budget rule; A5 item 5) of ONE pair of models, for their exact
OHS-3 primary readouts, from their DEV reads only. CPU; reads stored dev predictions of the 9 gate splits; no OHS file
is opened. Its --json is the config's cascade.tau_fit_log: ohs3_lib.check_fit_logs (ohs3_preflight.py and every real
OHS-3 cascade run) checks that cascade.tau / w_big / route_on equal its config_values, that its two T fit logs are the
config's models.<small/big>.T_fit_log files, and that every input is a dev read. The cascade is never fitted on OHS-3.

  python prep89/cascade_rule_fit.py --small-t-log prep89/t_fit_<2B>.json --big-t-log prep89/t_fit_<4B>.json \\
      --route-on raw|primary [--w-big 1.0] [--load-tests SMALL_SUMMARY,BIG_SUMMARY] [--json OUT]

  --small-t-log / --big-t-log  each model's t_rule_check.py --json (with --model): it names the model, its yes/no
      read, its choice read (and the < 10 options read for 2view_ge10) and its shipped T, i.e. the model's exact A5
      primary readout. This tool rebuilds that readout from the same dev reads and applies the same T.
  --load-tests  the two DEV load tests (load_test_c1.py summary.json, --model-key 2b and 4b, same config, one H100):
      the inference cost ratio of 5.3's use rule = the 4B's / the 2B's sustained decisions per hour. Without them the
      use rule is "not measured" and the check says TODO (cascade.run must then stay false).

Rule (fixed before any OHS-3 run; the numbers are FINETUNE_PLAN 5.3's):
  rows        the 9 gate splits; dev-select / dev-confirm = gate_dev.half(group_id).
  readouts    each model's A5 primary readout before T (t_rule_check.primary_raw), then its T (ohs3_lib.apply_T =
              calibrate.scaled), as served.
  routing     a row goes to the 4B when the top of the 2B's routing probabilities (normalised over the row's answers)
              is < tau (ohs3_lib.cascade_routed, the served rule). route_on raw = before T (5.3: "route on the raw 2B
              max probability"), primary = after T (A5 item 5); identical when the 2B's T is 1.00.
  answer      ohs3_lib.cascade_answer (the served and offline cascade's function; w_big blend on routed rows).
  tau(b)      the routing top at rank floor(b x n) of dev-select sorted ascending (cascade_sim.py's rule), for each
              budget b in 0.30, 0.40, ..., 0.80.
  choice      the SMALLEST budget whose one-sided 95% lower bound of (cascade - 4B alone) accuracy on dev-select is
              > -0.5 pp. Bound: paired cluster bootstrap over group_id, 10,000 resamples, numpy default_rng(0) per
              budget, 5th percentile. No budget passes -> no cascade (chosen = null; the check FAILs).
  confirm     dev-confirm is reported ONCE, at the chosen budget only (accuracy of the cascade, the 4B, the 2B; the
              paired difference with its two-sided 95% bootstrap interval; the routed share).
  use rule    serve the cascade only if cost_ratio + routed share on dev-confirm < 0.85 (5.3: "measured 2B/4B inference
              cost ratio + routed fraction < about 0.85"); cost_ratio from --load-tests only.
Accuracy = gate_dev.score's rule (the gold is the unique top answer). Prints aggregate numbers only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

PREP = Path(__file__).resolve().parent
sys.path.insert(0, str(PREP))
import ohs3_lib as L  # noqa: E402
import t_rule_check as TR  # noqa: E402  (its reads, splits, halves and root)

BUDGETS = (0.3, 0.4, 0.5, 0.6, 0.7, 0.8)
LB_MIN_PP = -0.5
USE_MAX = 0.85
N_BOOT = 10_000
ROUTE_ON = L.ROUTE_ON


def t_log(path):
    """A t_rule_check.py --json: the model, its reads and its shipped T (refuses anything else)."""
    p = Path(path)
    d = json.loads(p.read_text())
    if "ship" not in d or "args" not in d or "provenance" not in d:
        raise SystemExit(f"{path}: not a t_rule_check.py --json log (re-run t_rule_check.py with --model --json)")
    if not d["args"].get("model"):
        raise SystemExit(f"{path}: the T log names no model (re-run t_rule_check.py with --model)")
    if d["provenance"].get("choice_readout") == "proxy":
        raise SystemExit(f"{path}: its choice read is a NAME+NAME2 average (a proxy), not a served readout")
    a = d["args"]
    return {"path": str(path), "sha256": L.sha256_file(p), "model": a["model"],
            "noul": a["noul"].split("+"), "choice": a["choice"].split("+"),
            "lt10": a["choice_lt10"].split("+") if a.get("choice_lt10") else None,
            "T": {"noul": float(d["ship"]["T_noul"]), "choice": float(d["ship"]["T_choice"])},
            "choice_readout": d["provenance"]["choice_readout"]}


def correct(r, p):
    """gate_dev.score's accuracy rule: the gold is the unique top answer."""
    keys, ps = L.cascade_norm(r, p)
    g = ("yes" if r["gold"] == 1 else "no") if r["qtype"] == "noul" else r["gold"]
    best = max(ps)
    return float([k for k, v in zip(keys, ps) if v == best] == [g])


def load_rows(sm, bg, route_on):
    """Every row of the 9 dev splits with both models' primary readouts (after T) and the 2B's routing top."""
    out = []
    for sp in TR.SPLITS:
        if sp.startswith("ohs"):
            raise SystemExit("cascade_rule_fit: dev splits only")
        Ps = TR.primary_raw(sp, sm["noul"], sm["choice"], sm["lt10"])
        Pb = TR.primary_raw(sp, bg["noul"], bg["choice"], bg["lt10"])
        for r in TR.data_rows(sp):
            s_raw = Ps[r["id"]]
            s_fin = L.apply_T(s_raw, r, sm["T"])
            b_fin = L.apply_T(Pb[r["id"]], r, bg["T"])
            top = max(L.cascade_norm(r, s_raw if route_on == "raw" else s_fin)[1])
            out.append({"split": sp, "half": TR.G.half(r["group_id"]), "group": r["group_id"], "row": r,
                        "s": s_fin, "b": b_fin, "top": top, "ok_s": correct(r, s_fin), "ok_b": correct(r, b_fin)})
    return out


def evaluate(rows, tau, w_big):
    """Per row: routed (top < tau, the served rule) and the cascade's correctness (ohs3_lib.cascade_answer)."""
    res = []
    for x in rows:
        rt = x["top"] < float(tau)
        p = L.cascade_answer(x["row"], x["s"], x["b"] if rt else None, rt, w_big)
        res.append((rt, correct(x["row"], p)))
    return res


def cluster_boot(rows, diffs, seed=0, n_boot=N_BOOT, chunk=500):
    """Bootstrap of the mean paired difference over groups (rows of one group move together)."""
    gi, sums, ns = {}, [], []
    for x, d in zip(rows, diffs):
        j = gi.setdefault(x["group"], len(gi))
        if j == len(sums):
            sums.append(0.0)
            ns.append(0)
        sums[j] += d
        ns[j] += 1
    S, N = np.array(sums), np.array(ns, dtype=float)
    rng = np.random.default_rng(seed)
    out = []
    for k in range(0, n_boot, chunk):
        idx = rng.integers(0, len(S), size=(min(chunk, n_boot - k), len(S)))
        out.append(S[idx].sum(1) / N[idx].sum(1))
    return np.concatenate(out) * 100


def load_test_ratio(paths):
    """cost ratio 2B/4B per decision = the 4B's / the 2B's sustained decisions per hour, from two DEV load tests."""
    sm, bg = (json.loads(Path(p).read_text()) for p in paths)
    info = {}
    for tag, d, p in (("small", sm, paths[0]), ("big", bg, paths[1])):
        ok = (d.get("dev_only") is True and d.get("kind") == "model" and d.get("sustained_decisions_per_hour")
              and (d.get("token_check") or {}).get("pass") is True)
        info[tag] = {"path": str(p), "sha256": L.sha256_file(p), "model": d.get("model"), "system": d.get("system"),
                     "config_sha256": d.get("config_sha256"), "region": (d.get("c1") or {}).get("region"),
                     "gpu": (d.get("endpoint_health") or {}).get("gpu"),
                     "rate_usd_h": (d.get("c1") or {}).get("rate_usd_h_effective"),
                     "sustained_decisions_per_hour": d.get("sustained_decisions_per_hour"), "usable": bool(ok)}
    if not (info["small"]["usable"] and info["big"]["usable"]):
        raise SystemExit(f"--load-tests: both must be DEV load tests of a single model with a sustained rate and a "
                         f"passed token check: {info}")
    for k in ("region", "gpu", "rate_usd_h"):  # one cost basis: same GPU type, region and $/h for both models
        if info["small"][k] != info["big"][k]:
            raise SystemExit(f"--load-tests: the two load tests differ in {k} ({info['small'][k]} vs {info['big'][k]})")
    ratio = info["big"]["sustained_decisions_per_hour"] / info["small"]["sustained_decisions_per_hour"]
    return ratio, info


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--small-t-log", required=True)
    ap.add_argument("--big-t-log", required=True)
    ap.add_argument("--route-on", required=True, choices=ROUTE_ON)
    ap.add_argument("--w-big", type=float, default=1.0)
    ap.add_argument("--load-tests", default=None, help="SMALL_SUMMARY,BIG_SUMMARY (dev load tests)")
    ap.add_argument("--root", default=None, help="a tree with data/ and preds_<split>/ (tests); default lean/")
    ap.add_argument("--json", default=None)
    a = ap.parse_args(argv)
    if a.root:
        TR.set_root(a.root)
    if not 0 <= a.w_big <= 1:
        raise SystemExit("--w-big must be in [0, 1]")
    sm, bg = t_log(a.small_t_log), t_log(a.big_t_log)
    if sm["model"] == bg["model"]:
        raise SystemExit("small and big are the same model")
    rows = load_rows(sm, bg, a.route_on)
    sel = [x for x in rows if x["half"] == "select"]
    conf = [x for x in rows if x["half"] == "confirm"]
    tops = sorted(x["top"] for x in sel)
    acc = lambda xs, k: 100 * sum(x[k] for x in xs) / len(xs)  # noqa: E731
    budgets, chosen = [], None
    for b in BUDGETS:
        tau = tops[int(b * len(tops))]
        ev = evaluate(sel, tau, a.w_big)
        diffs = [c - x["ok_b"] for (rt, c), x in zip(ev, sel)]
        bs = cluster_boot(sel, diffs)
        rec = {"budget": b, "tau": tau, "select_routed_share": round(sum(rt for rt, _ in ev) / len(sel), 4),
               "select_acc_cascade": round(100 * sum(c for _, c in ev) / len(sel), 3),
               "select_diff_vs_big_pp": round(100 * sum(diffs) / len(sel), 3),
               "select_lb95_one_sided_pp": round(float(np.percentile(bs, 5)), 3)}
        rec["passes"] = rec["select_lb95_one_sided_pp"] > LB_MIN_PP
        budgets.append(rec)
        if chosen is None and rec["passes"]:
            chosen = rec
    res = {"rule": "FINETUNE_PLAN 5.3 budget rule (cascade_rule_fit.py docstring)", "dev_only": True,
           "splits": TR.SPLITS, "rows": {"select": len(sel), "confirm": len(conf)},
           "small": {k: sm[k] for k in ("model", "path", "sha256", "choice_readout", "T")} | {"t_log_sha256": sm["sha256"]},
           "big": {k: bg[k] for k in ("model", "path", "sha256", "choice_readout", "T")} | {"t_log_sha256": bg["sha256"]},
           "route_on": a.route_on, "w_big": a.w_big, "budgets_tried": list(BUDGETS), "lb_min_pp": LB_MIN_PP,
           "n_boot": N_BOOT, "select": budgets, "alone_select": {"small": round(acc(sel, "ok_s"), 3),
                                                                 "big": round(acc(sel, "ok_b"), 3)},
           "chosen": None, "confirm": None, "config_values": None,
           "reads": {n: TR.read_info(n)["sha256"] for n in sorted(set(sm["noul"] + sm["choice"] + (sm["lt10"] or [])
                                                                       + bg["noul"] + bg["choice"] + (bg["lt10"] or [])))},
           "tool": {"path": "prep89/cascade_rule_fit.py", "sha256": L.sha256_file(Path(__file__))}}
    if chosen:
        ev = evaluate(conf, chosen["tau"], a.w_big)
        diffs = [c - x["ok_b"] for (rt, c), x in zip(ev, conf)]
        bs = cluster_boot(conf, diffs)
        share = sum(rt for rt, _ in ev) / len(conf)
        res["chosen"] = {"budget": chosen["budget"], "tau": chosen["tau"]}
        res["confirm"] = {"acc_cascade": round(100 * sum(c for _, c in ev) / len(conf), 3),
                          "acc_big": round(acc(conf, "ok_b"), 3), "acc_small": round(acc(conf, "ok_s"), 3),
                          "diff_vs_big_pp": round(100 * sum(diffs) / len(conf), 3),
                          "ci95_pp": [round(float(np.percentile(bs, 2.5)), 3), round(float(np.percentile(bs, 97.5)), 3)],
                          "routed_share": round(share, 4), "reported_once": True}
        res["config_values"] = {"tau": chosen["tau"], "w_big": a.w_big, "route_on": a.route_on}
        if a.load_tests:
            ratio, info = load_test_ratio(a.load_tests.split(","))
            if (info["small"]["model"], info["big"]["model"]) != (sm["model"], bg["model"]):
                raise SystemExit(f"--load-tests are of {info['small']['model']} / {info['big']['model']}, not "
                                 f"{sm['model']} / {bg['model']}")
            res["use_rule"] = {"cost_ratio": round(ratio, 4), "routed_share_confirm": round(share, 4),
                               "sum": round(ratio + share, 4), "max": USE_MAX, "pass": ratio + share < USE_MAX,
                               "load_tests": info}
        else:
            res["use_rule"] = {"cost_ratio": None, "routed_share_confirm": round(share, 4), "max": USE_MAX,
                               "pass": None, "note": "not measured: needs the 2B and 4B DEV load tests (--load-tests)"}
    else:
        res["use_rule"] = {"pass": False, "note": "no budget passed the select bound: serve the 4B alone"}
    for b in budgets:
        print(f"budget {b['budget']:.0%}: tau {b['tau']:.4f}, select routed {b['select_routed_share']:.3f}, cascade - 4B "
              f"{b['select_diff_vs_big_pp']:+.2f} pp (one-sided 95% LB {b['select_lb95_one_sided_pp']:+.2f}) "
              f"{'PASS' if b['passes'] else 'fail'}")
    if chosen:
        c = res["confirm"]
        print(f"CHOSEN budget {chosen['budget']:.0%}, tau {chosen['tau']:.6f} (route_on {a.route_on}, w_big {a.w_big}); "
              f"dev-confirm (once): cascade {c['acc_cascade']:.2f} vs 4B {c['acc_big']:.2f} ({c['diff_vs_big_pp']:+.2f} pp, "
              f"95% [{c['ci95_pp'][0]:+.2f}, {c['ci95_pp'][1]:+.2f}]), routed {c['routed_share']:.3f}")
    else:
        print("NO CASCADE: no budget passed the dev-select bound (serve the 4B alone)")
    u = res["use_rule"]
    print(f"use rule (cost ratio + routed < {USE_MAX}): {u.get('pass')} "
          f"{'(cost ratio ' + str(u.get('cost_ratio')) + ')' if u.get('cost_ratio') is not None else u.get('note', '')}")
    if a.json:
        Path(a.json).write_text(json.dumps(res, indent=1) + "\n")
    return res


if __name__ == "__main__":
    main()
