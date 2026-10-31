"""warm_pool_sim.py: warm-pool / keep-alive design and cost model (CPU, stdlib). Everything it prints is tagged "modelled".

What it answers (L-D output 1): for a load trace, how much do a warm floor (min_warm instances) and a keep-alive window
(idle_timeout_s before the last instances scale down) cost, and how many requests meet a cold start (the measured 131 s on
the Modal H100; the L4/GCP number comes from cold_start_probe.py and replaces it in the inputs file).

Model (a fluid approximation, one tick = dt seconds):
  * arrivals per tick ~ Poisson(lambda(t) dt); an instance serves cap_dph/3600 decisions per second when ready;
  * unserved decisions wait in one FIFO backlog; the wait of a tick's arrivals = (time until an instance is ready) +
    backlog / (ready capacity) -- this is the delay ADDED by queueing and cold starts, on top of the normal service time;
  * scale-up: when the load estimate (mean arrivals of the last 10 s) exceeds up_util x total (ready + booting) capacity, or
    the backlog is non-empty, start instances (each is ready after cold_start_s and is billed from the start);
  * scale-down: when the load estimate would still fit in (W-1) instances at down_util, for idle_timeout_s in a row, drop one
    instance, never below min_warm;
  * cost = billed instance-seconds x rate_usd_h / 3600 (boot time is billed; per-second billing with min_billed_s per start).
It is NOT a queueing-theory proof: the batch-size dependence of capacity is handled in batching_plan.py. Use it to compare
policies on the same trace and to find the load where scale-to-zero stops being sensible. The inputs it needs are all in
inputs/*.json with their tags; swapping the H100 numbers for the L4 ones is a one-line change in the inputs file.

  warm_pool_sim.py --inputs inputs/warm_pool_inputs.json --scenario all --days 7 --out out/warm_pool.json --md out/warm_pool.md
  warm_pool_sim.py --selftest
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402


# ------------------------------------------------------------------ traces
def rate_fn(spec: dict):
    """lambda(t) in decisions per second from a scenario spec."""
    kind = spec["kind"]
    if kind == "constant":
        r = float(spec["rate_per_s"])
        return lambda t: r
    if kind == "diurnal":   # sinusoid between trough and peak, period in hours, peak at hour `peak_hour`
        pk, tr, per, ph = float(spec["peak_per_s"]), float(spec["trough_per_s"]), float(spec.get("period_h", 24)), float(spec.get("peak_hour", 14))
        return lambda t: tr + (pk - tr) * 0.5 * (1 + math.cos(2 * math.pi * ((t / 3600.0) - ph) / per))
    if kind == "onoff":     # bursts: on_rate for on_s, off_rate for off_s
        on, off, a, b = float(spec["on_per_s"]), float(spec.get("off_per_s", 0.0)), float(spec["on_s"]), float(spec["off_s"])
        return lambda t: on if (t % (a + b)) < a else off
    if kind == "workweek":  # diurnal on weekdays, `weekend_factor` on days 5 and 6 of each week
        base = rate_fn({**spec, "kind": "diurnal"})
        wf = float(spec.get("weekend_factor", 0.3))
        return lambda t: base(t) * (wf if int(t // 86400) % 7 in (5, 6) else 1.0)
    raise ValueError(f"unknown trace kind {kind}")


def poisson(rng: random.Random, mean: float) -> int:
    if mean <= 0:
        return 0
    if mean > 30:
        return max(0, int(round(rng.gauss(mean, math.sqrt(mean)))))
    l, k, p = math.exp(-mean), 0, 1.0
    while True:
        p *= rng.random()
        if p <= l:
            return k
        k += 1


# ------------------------------------------------------------------ simulation
def simulate(spec: dict, inst: dict, policy: dict, days: float = 7.0, dt: float = 5.0, seed: int = 0) -> dict:
    """One scenario x one policy. inst: cap_dph, rate_usd_h, cold_start_s, min_billed_s. policy: min_warm, idle_timeout_s,
    max_instances, up_util, down_util."""
    rng = random.Random(seed)
    lam = rate_fn(spec)
    cap_s = inst["cap_dph"] / 3600.0                      # decisions per second per ready instance
    boot = float(inst["cold_start_s"])
    min_warm, max_n = int(policy["min_warm"]), int(policy.get("max_instances", 64))
    idle_to, up_u, dn_u = float(policy["idle_timeout_s"]), float(policy.get("up_util", 0.8)), float(policy.get("down_util", 0.8))
    min_billed = float(inst.get("min_billed_s", 60.0))
    T = days * 86400.0
    steps = int(T / dt)
    ready = min_warm                                       # the warm floor exists at t=0
    booting = []                                           # ready-at times
    born = [0.0] * ready                                   # start times of live instances (for min billing)
    billed = 0.0                                           # billed instance-seconds of ended instances
    backlog = 0.0
    arrivals_hist: list = []
    low_for = 0.0
    served = total = 0.0
    ready_s = 0.0
    cold_arr = 0.0
    waits: list = []                                       # (wait_s, weight)
    n_starts = 0
    for i in range(steps):
        t = i * dt
        # boots finishing
        if booting:
            done = [b for b in booting if b <= t]
            if done:
                booting = [b for b in booting if b > t]
                ready += len(done)
        a = poisson(rng, lam(t) * dt)
        total += a
        arrivals_hist.append(a)
        if len(arrivals_hist) > max(1, int(10.0 / dt)):
            arrivals_hist.pop(0)
        est = sum(arrivals_hist) / (len(arrivals_hist) * dt)             # decisions per second over ~10 s
        if a and ready == 0:
            cold_arr += a
        # scale up
        live = ready + len(booting)
        need = math.ceil(est / (up_u * cap_s)) if est > 0 else 0
        need = max(need, min_warm, 1 if (backlog > 0 or a > 0) else 0)
        if need > live:
            for _ in range(min(need - live, max_n - live)):
                booting.append(t + boot)
                born.append(t)
                n_starts += 1
        # serve
        backlog += a
        cap_now = ready * cap_s * dt
        s = min(backlog, cap_now)
        backlog -= s
        served += s
        ready_s += ready * dt
        if a:
            if ready > 0:
                w = backlog / (ready * cap_s)
            else:
                nxt = min(booting) if booting else t + boot
                w = max(0.0, nxt - t) + backlog / cap_s
            waits.append((w, a))
        # scale down (only ready instances, never below the floor; booting ones are kept)
        if ready > min_warm and est <= dn_u * (ready - 1) * cap_s and backlog == 0:
            low_for += dt
            if low_for >= idle_to:
                ready -= 1
                low_for = 0.0
                life = t - born.pop(0)
                billed += max(life, min_billed)
        else:
            low_for = 0.0
    # close the books at T
    for b in born:
        billed += max(T - b, min_billed) if T - b > 0 else min_billed
    ws = sorted(waits)
    tot_w = sum(w for _, w in ws) or 1.0

    def wq(q):
        if not ws:
            return 0.0
        acc, tgt = 0.0, q * tot_w
        for v, w in ws:
            acc += w
            if acc >= tgt:
                return v
        return ws[-1][0]

    cost = billed * inst["rate_usd_h"] / 3600.0
    return {"policy": policy, "served": round(served), "arrivals": round(total), "unserved_at_end": round(backlog),
            "cost_usd": round(cost, 4), "usd_per_1k": round(cost / served * 1000.0, 5) if served else None,
            "instance_hours_billed": round(billed / 3600.0, 3),
            "billed_utilisation": round(served / (billed * cap_s), 4) if billed else None,
            "ready_utilisation": round(served / (ready_s * cap_s), 4) if ready_s else None,
            "cold_start_hit_share": round(cold_arr / total, 6) if total else 0.0,
            "n_instance_starts": n_starts,
            "added_wait_s": {"p50": round(wq(0.5), 3), "p95": round(wq(0.95), 3), "p99": round(wq(0.99), 3),
                             "max": round(ws[-1][0], 3) if ws else 0.0}}


def default_policies(floor_choices=(0, 1), timeouts=(0, 60, 300, 900, 1800, 3600, 7200)) -> list:
    out = []
    for mw in floor_choices:
        for to in (timeouts if mw == 0 else (0,)):     # with a warm floor the timeout only matters above the floor
            out.append({"min_warm": mw, "idle_timeout_s": to, "max_instances": 64, "up_util": 0.8, "down_util": 0.8})
    return out


def inst_values(inputs: dict, name: str) -> dict:
    spec = inputs["instances"][name]
    miss = [k for k in ("cap_dph", "rate_usd_h", "cold_start_s") if spec[k]["value"] is None]
    if miss:
        raise SystemExit(f"instance {name!r}: {', '.join(miss)} are not-measured (value null). Fill them from the measurement "
                         f"(capacity_ladder.py -> cap_dph, cold_start_probe.py -> cold_start_s, the price page -> rate_usd_h), "
                         f"or run with --instance of a profile that has them.")
    inst = {k: spec[k]["value"] for k in ("cap_dph", "rate_usd_h", "cold_start_s")}
    inst["min_billed_s"] = spec.get("min_billed_s", {}).get("value", 60.0)
    return inst


def run_all(inputs: dict, scenarios: list, days: float, dt: float, seed: int, instance: str) -> dict:
    inst = inst_values(inputs, instance)
    pols = inputs.get("policies") or default_policies()
    res = {}
    for sc in scenarios:
        res[sc["name"]] = {"spec": sc, "runs": [simulate(sc, inst, p, days, dt, seed) for p in pols]}
    return res


def ski_rental(inst: dict) -> dict:
    """Dollar-optimal keep-alive window in the classic ski-rental argument: keeping an idle instance for T seconds costs
    rate*T; releasing it and restarting later costs rate*cold_start_s of boot time. The 2-competitive window is T = cold_start_s.
    Dollars only: the user-visible cost of a cold start (a request waits ~cold_start_s) is what the warm floor pays for."""
    return {"window_s": inst["cold_start_s"], "idle_cost_usd_per_h": inst["rate_usd_h"],
            "note": "dollar-optimal window = cold start length; a warm floor is a latency decision, not a dollar one"}


def render_md(out: dict) -> str:
    ins = out["inputs"]["instances"][out["instance"]]
    lines = [f"# Warm-pool model ({out['tag']['tag']}; instance {out['instance']}; seed {out['seed']}, {out['days']} days, dt {out['dt_s']} s)",
             "", "Instance inputs: " + json.dumps({k: (v.get('value'), v['tag'] + (f" n={v['n']}" if 'n' in v else "")) for k, v in ins.items() if isinstance(v, dict) and 'tag' in v}),
             ""]
    for name, r in out["scenarios"].items():
        lines += [f"## {name}", "", f"`{json.dumps(r['spec'])}`", ""]
        rows = []
        for x in r["runs"]:
            p = x["policy"]
            rows.append([p["min_warm"], p["idle_timeout_s"], x["usd_per_1k"], x["cost_usd"], x["billed_utilisation"],
                         f"{100 * x['cold_start_hit_share']:.3f}%", x["n_instance_starts"], x["added_wait_s"]["p95"],
                         x["added_wait_s"]["p99"], x["added_wait_s"]["max"]])
        lines += [C.md_table(["min_warm", "idle_timeout_s", "$/1K", "cost $", "billed util", "cold-hit share", "starts",
                              "added wait p95 s", "p99 s", "max s"], rows), ""]
    return "\n".join(lines)


def selftest() -> None:
    inst = {"cap_dph": 36000.0, "rate_usd_h": 1.0, "cold_start_s": 100.0, "min_billed_s": 0.0}   # 10 dec/s
    # constant 5 dec/s, floor 1: ~1 instance billed all the time, utilisation about 0.5, no cold hits
    r = simulate({"kind": "constant", "rate_per_s": 5}, inst, {"min_warm": 1, "idle_timeout_s": 0}, days=0.5, dt=5, seed=1)
    assert 0.45 < r["billed_utilisation"] < 0.55 and r["cold_start_hit_share"] == 0.0, r
    assert abs(r["instance_hours_billed"] - 12.0) < 0.01, r
    # zero floor, bursts: cold hits happen, floor removes them
    sp = {"kind": "onoff", "on_per_s": 5, "on_s": 600, "off_s": 3000}
    r0 = simulate(sp, inst, {"min_warm": 0, "idle_timeout_s": 60}, days=1, dt=5, seed=2)
    r1 = simulate(sp, inst, {"min_warm": 1, "idle_timeout_s": 0}, days=1, dt=5, seed=2)
    assert r0["cold_start_hit_share"] > 0 and r1["cold_start_hit_share"] == 0, (r0, r1)
    assert r0["cost_usd"] < r1["cost_usd"], (r0, r1)
    assert r0["added_wait_s"]["max"] >= 90, r0
    print("selftest ok")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--inputs", default=str(C.ROOT / "inputs" / "warm_pool_inputs.json"))
    ap.add_argument("--scenario", default="all", help="scenario name from the inputs file, or all")
    ap.add_argument("--instance", default="h100_modal_reference", help="instance profile in the inputs file")
    ap.add_argument("--days", type=float, default=7.0)
    ap.add_argument("--dt", type=float, default=5.0)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out"), ap.add_argument("--md")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        selftest()
        return 0
    inputs = json.loads(Path(a.inputs).read_text())
    bad = C.check_tagged(inputs)
    if bad:
        raise SystemExit("inputs are not fully tagged:\n  " + "\n  ".join(bad))
    inst = inst_values(inputs, a.instance)
    sc = [s for s in inputs["scenarios"] if a.scenario in ("all", s["name"])]
    if not sc:
        raise SystemExit("no such scenario")
    scen = run_all(inputs, sc, a.days, a.dt, a.seed, a.instance)
    out = {"tag": C.tag("modelled", source="warm_pool_sim.py fluid model", seed=a.seed,
                        inputs_sha256=hashlib.sha256(json.dumps(inputs, sort_keys=True).encode()).hexdigest()[:16]),
           "instance": a.instance, "seed": a.seed, "days": a.days, "dt_s": a.dt, "inputs": inputs, "ski_rental": ski_rental(inst),
           "scenarios": scen, "utc": C.utc(),
           "caveat": "fluid approximation; the load scenarios are ASSUMED (tag assumed), the instance numbers carry their own tags"}
    if a.out:
        C.write_json(a.out, out)
    md = render_md(out)
    if a.md:
        Path(a.md).parent.mkdir(parents=True, exist_ok=True)
        Path(a.md).write_text(md)
    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
