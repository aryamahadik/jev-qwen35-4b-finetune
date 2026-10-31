"""oc1.plan: the run plan and its cost estimate per phase (USD), against the USD 5.00 cap.

Every duration below is an ESTIMATE from measured numbers where we have them:
  * S1 boot 175.7 s (SPEED-2, eu-north), 152.3 s (S2): ~150-175 s per boot, Triton cache warm after the first boot
  * S1 throughput: P at c=16 = 174.8 s for 8,143 calls (6.08M tokens); S c=16 = 124K decisions/h (660 calls = 19 s)
  * B1a: C1 fast path 14.1 ms p50 / 19.2 ms p95 batch 1 on an H100 (HF + CUDA graphs); S1 server p50 45 ms on the heavy S set
  * CPU phases of 17 Oct (preflight 80 s, inspect 3 x 30 s, export 79 s) cost ~USD 0.02 in `modal billing report`
Money model: container seconds x rate; rate = (H100 3.95 + 4 cores x 0.0473 + 32 GiB x 0.008) x region multiplier; the
governor uses the conservative multipliers (any 1.0, broad US 1.25, narrow 1.75). Image pulls/builds were not visible in
the billing report (first app: CPU USD 0.0043 for the failed-import container).
"""
from __future__ import annotations

import json

from . import common as C
from . import configs as K

GPU_CPU, GPU_MEM_GIB = 4.0, 32.0        # S1 used 4 cores / 32 GiB (hosting/sglang_host.py)


def gpu_rate(region: str = "any") -> float:
    return C.container_rate_usd_h("H100", GPU_CPU, GPU_MEM_GIB, region)


def default_plan(region: str = "any", configs=None, e2e: bool = True, vision: bool = True, voice: bool = True,
                 jev_sample_n: int = 200, jev_interleaved_n: int = 100) -> dict:
    names = configs or ["s1", "chunk_off", "gdn_flashinfer", "fp8_careful", "fp8_w8a8_online", "graph_off", "radix_off", "sched_big"]
    levels = [{"name": "qps3", "qps": 3, "duration_s": 40, "wait_ms": 0},
              {"name": "qps10", "qps": 10, "duration_s": 40, "wait_ms": 0, "keep_records": True},
              {"name": "qps25", "qps": 25, "duration_s": 40, "wait_ms": 0},
              {"name": "qps10_wait2", "qps": 10, "duration_s": 40, "wait_ms": 2},
              {"name": "qps10_wait5", "qps": 10, "duration_s": 40, "wait_ms": 5},
              {"name": "qps25_wait2", "qps": 25, "duration_s": 40, "wait_ms": 2},
              {"name": "qps25_wait5", "qps": 25, "duration_s": 40, "wait_ms": 5},
              {"name": "qps10_newconn30", "qps": 10, "duration_s": 30, "wait_ms": 0, "new_conn_frac": 0.3},
              {"name": "qps45_overload", "qps": 45, "duration_s": 30, "wait_ms": 0, "shed_at": 1000000},
              {"name": "qps45_shed24", "qps": 45, "duration_s": 30, "wait_ms": 0, "shed_at": 24}]
    return {
        "version": 1, "region": region, "gpu": "H100!", "rate_usd_h": round(gpu_rate(region), 4), "configs": names,
        "require_region_prefix": "us",     # the e2e comparison with Jev needs a US container (laptop RTT ~40 ms; eu-north was 131 ms)
        "boot_timeout_s": 420, "measure_timeout_s": 1500,
        "params": {"sub_n": 2500, "parity_conc": 16, "lat_n": 320, "lat_s": 140, "lat_warm": 20, "lat_rounds": 40,
                   "tp_conc": [16, 64], "prefix_n": 800, "prefix_conc": 8},
        "e2e": {"enabled": e2e, "est_s": 560, "levels": levels, "jev_sample_n": jev_sample_n,
                "jev_interleaved_n": jev_interleaved_n, "workers": 64, "front_seconds": 700},
        "vision": {"enabled": vision, "est_s": 150, "caps": [None, 256, 128, 64], "upscale": [1024, 2048, 4096], "upscale_n": 24,
                   "n_per_suite": 100},
        "voice_c1": {"enabled": voice, "est_s": 100},
    }


# seconds per piece (estimates, see the module docstring)
PIECES = {
    "boot": 160, "stop": 20, "warm": 15,
    "parity_full": 150, "parity_sub": 55, "latency": 30, "throughput": 70, "prefix": 30, "score_readout": 95,
    "vision": 150, "voice_c1": 100, "e2e": 560,
}


def block_seconds(cfg: K.Config, plan: dict) -> float:
    t = cfg.est_boot_s + PIECES["stop"] + PIECES["warm"]
    for m in cfg.measures:
        if m in PIECES and m not in ("vision", "voice_c1", "e2e"):
            t += PIECES[m]
        elif m in ("vision", "voice_c1", "e2e") and plan.get(m, {}).get("enabled", True):
            t += plan[m]["est_s"] if m != "e2e" else PIECES["e2e"]
    return t


CPU_DONE = [    # (name, actual USD from `modal billing report` where known, status): the build phase of 17 Oct
    "preflight, 3 SGLang source inspections, C1 merged export (identical to S1's), CPU dry run of the Python side, voice CPU smoke "
    "test, network probe in 3 regions",
]


def estimate(plan: dict, spent_so_far: float | None = None) -> dict:
    """spent_so_far = the ledger (conservative; the billing report read about 40% lower for the same CPU phases)."""
    if spent_so_far is None:
        try:
            spent_so_far = C.Budget(persist=False).spent() if False else C.Budget().spent()
        except Exception:  # noqa: BLE001
            spent_so_far = 0.1
    rate = plan["rate_usd_h"]
    rows, gpu_s = [], C.CONTAINER_OVERHEAD_S
    for name in plan["configs"]:
        cfg = K.CONFIGS[name]
        s = block_seconds(cfg, plan)
        gpu_s += s
        rows.append({"phase": f"H100 block: {name}", "seconds": round(s), "usd": round(s / 3600 * rate, 3), "priority": cfg.priority,
                     "measures": cfg.measures})
    voice_gpu = {"phase": "voice TTS+ASR on GPU (L4; H100 would cost ~USD 0.35)", "seconds": 420,
                 "usd": round(C.container_cost_usd(420, C.container_rate_usd_h("L4", 4, 16, "any")), 3)}
    fixed = [{"phase": CPU_DONE[0], "usd": round(spent_so_far, 3), "status": "done (ledger, conservative)"}]
    session_usd = round(gpu_s / 3600 * rate, 3)
    total = round(session_usd + voice_gpu["usd"] + spent_so_far + 0.10 + 0.05, 3)
    # what the in-container gate will actually do: run blocks in order while spent + block estimate <= stop-launch
    spent = spent_so_far + voice_gpu["usd"] + 0.10 + 0.05 + C.CONTAINER_OVERHEAD_S / 3600 * rate
    run, skipped = [], []
    for r in rows:
        c = r["usd"]
        if spent + c <= C.STOP_LAUNCH_USD:
            run.append(r["phase"].replace("H100 block: ", ""))
            spent += c
        else:
            skipped.append(r["phase"].replace("H100 block: ", ""))
    return {"rate_usd_h": rate, "session_seconds": round(gpu_s), "session_usd": session_usd, "blocks": rows, "voice_gpu": voice_gpu,
            "gate_simulation": {"blocks_expected_to_run": run, "blocks_expected_to_be_skipped": skipped,
                                "expected_total_usd": round(spent, 3)},
            "fixed": fixed, "openrouter_jev_usd_max": 0.10, "volume_storage_usd_est": 0.05,
            "total_usd_if_every_block_runs": total, "cap_usd": C.CAP_USD, "stop_launch_usd": C.STOP_LAUNCH_USD,
            "fits_stop_launch": total <= C.STOP_LAUNCH_USD,
            "note": "the in-container gate drops trailing blocks when spent + block estimate > stop-launch"}


def render(plan: dict) -> str:
    e = estimate(plan)
    lines = [f"H100 session at USD {e['rate_usd_h']:.2f}/h (region {plan['region']}), {len(plan['configs'])} blocks:"]
    for r in e["blocks"]:
        lines.append(f"  {r['phase']:34s} {r['seconds']:5d} s  USD {r['usd']:.2f}   {','.join(r['measures'])}")
    lines.append(f"  session total {e['session_seconds']} s = USD {e['session_usd']:.2f}")
    lines.append(f"  {e['voice_gpu']['phase']}: USD {e['voice_gpu']['usd']:.2f}  (to run BEFORE the session)")
    for f in e["fixed"]:
        lines.append(f"  {f['phase']}: USD {f['usd']:.2f} ({f['status']})")
    lines.append(f"  OpenRouter Jev sample <= USD {e['openrouter_jev_usd_max']:.2f}; Volume storage ~USD {e['volume_storage_usd_est']:.2f}")
    g = e["gate_simulation"]
    lines.append(f"  gate simulation: run {', '.join(g['blocks_expected_to_run'])}; skipped {', '.join(g['blocks_expected_to_be_skipped']) or '-'}; "
                 f"expected total USD {g['expected_total_usd']:.2f}")
    lines.append(f"  TOTAL if every block runs: USD {e['total_usd_if_every_block_runs']:.2f}  (stop-launch {C.STOP_LAUNCH_USD}, cap {C.CAP_USD})")
    return "\n".join(lines)


if __name__ == "__main__":
    p = default_plan()
    print(render(p))
