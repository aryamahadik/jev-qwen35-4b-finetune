"""oc1.costmodel: USD per 1,000 decisions from MEASURED numbers, vs utilisation (10-100%), vs price tiers, vs Jev.

  usd_per_1k(rate_usd_h, decisions_per_h, util)  = rate / (dph x util) x 1000
  compute_floor(rate, ms_per_decision)           = what the GPU seconds alone cost (100% busy, no idle, no batching gap)
  breakeven_util(rate, dph, jev_usd_per_1k)      = the utilisation above which one GPU beats Jev's price
  cost_at_qps(rate, qps)                         = a dedicated GPU kept for a steady `qps`: rate / (qps x 3.6) per 1K

Price tiers (fetched 17 Oct 2026; the sources are first-party price pages unless marked third-party):
  Modal on-demand        H100 USD 0.001097/s = 3.95/h (modal.com/pricing); region selection x1.15-1.75; the public page lists
                         NO reserved or spot tier (committed spend only through AWS/GCP marketplaces or Enterprise)
  Lambda on-demand       H100 SXM 4.29/h, PCIe 3.29/h (lambda.ai/pricing); reserved = "contact us" (no public price);
                         1-Click Clusters H100 6.16/GPU-h at 16 GPUs
  RunPod secure/community  H100 SXM 3.99 / 2.69, PCIe 2.89 / 1.99, NVL 3.19 / 2.59 per hour (runpod.io/pricing);
                         serverless H100 4.79/h; no spot, reserved = "contact sales"
  third-party (blog aggregators, mid-2026, approximate): CoreWeave 8xH100 on-demand 6.155/GPU-h and spot 2.464/GPU-h;
                         AWS p5.48xlarge ~12.29/GPU-h; GCP A3 ~11.06/GPU-h; Lambda 1-yr reserved estimated at ~20% off
Jev: PREREG_FINAL.md 11.4 reference USD 0.061 per 1K (OpenRouter list prices on measured token counts); the research
finding quotes ~0.034 per 1K. Both are carried; the reader picks.
"""
from __future__ import annotations

UTILS = (0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00)
JEV_USD_PER_1K = {"prereg_11.4_reference": 0.061, "research_finding": 0.034}
CONTAINER_EXTRA_USD_H = 0.445  # 4 cores + 32 GiB next to the GPU (modal rates 0.0473/core/h, 0.008/GiB/h)

PRICES = [
    {"name": "Modal H100 on-demand (any region)", "usd_h": 3.95 + CONTAINER_EXTRA_USD_H, "kind": "on-demand",
     "src": "https://modal.com/pricing (USD 0.001097/s) + CPU/memory at billing rates", "first_party": True},
    {"name": "Modal H100 on-demand (broad US region x1.15)", "usd_h": (3.95 + CONTAINER_EXTRA_USD_H) * 1.15,
     "kind": "on-demand", "src": "https://modal.com/pricing (region selection 1.15-1.75x)", "first_party": True},
    {"name": "Modal H100 on-demand (narrow region x1.75)", "usd_h": (3.95 + CONTAINER_EXTRA_USD_H) * 1.75,
     "kind": "on-demand", "src": "https://modal.com/pricing (region selection 1.15-1.75x)", "first_party": True},
    {"name": "Lambda H100 SXM 1x on-demand", "usd_h": 4.29, "kind": "on-demand", "src": "https://lambda.ai/pricing",
     "first_party": True},
    {"name": "Lambda H100 PCIe 1x on-demand", "usd_h": 3.29, "kind": "on-demand", "src": "https://lambda.ai/pricing",
     "first_party": True},
    {"name": "RunPod H100 SXM secure cloud", "usd_h": 3.99, "kind": "on-demand", "src": "https://www.runpod.io/pricing",
     "first_party": True},
    {"name": "RunPod H100 SXM community cloud", "usd_h": 2.69, "kind": "on-demand", "src": "https://www.runpod.io/pricing",
     "first_party": True},
    {"name": "RunPod H100 PCIe community cloud", "usd_h": 1.99, "kind": "on-demand", "src": "https://www.runpod.io/pricing",
     "first_party": True},
    {"name": "CoreWeave H100 spot (third-party figure)", "usd_h": 2.464, "kind": "spot",
     "src": "https://www.thundercompute.com/blog/coreweave-alternatives (aggregator; 8xHGX 19.71/h / 8)",
     "first_party": False},
    {"name": "Lambda H100 SXM 1-yr reserved (estimate: -20%)", "usd_h": round(4.29 * 0.8, 3), "kind": "reserved-estimate",
     "src": "estimate from the aggregator's 20% 1-year discount; Lambda lists no public reserved price",
     "first_party": False},
    {"name": "AWS p5 H100 on-demand (third-party figure)", "usd_h": 12.29, "kind": "on-demand",
     "src": "aggregator, p5.48xlarge ~98.32/h / 8", "first_party": False},
]


def usd_per_1k(rate_usd_h: float, decisions_per_h: float, util: float = 1.0) -> float:
    if not decisions_per_h or util <= 0:
        return float("nan")
    return rate_usd_h / (decisions_per_h * util) * 1000.0


def compute_floor(rate_usd_h: float, ms_per_decision: float) -> float:
    """USD per 1K decisions when the GPU is busy 100% of the time at `ms_per_decision` per decision."""
    return rate_usd_h * (ms_per_decision / 3.6e6) * 1000.0


def breakeven_util(rate_usd_h: float, decisions_per_h: float, jev_usd_per_1k: float) -> float:
    """Utilisation above which usd_per_1k(rate, dph, u) < Jev's price (may exceed 1.0 = never at this throughput)."""
    return rate_usd_h / (decisions_per_h * jev_usd_per_1k / 1000.0)


def cost_at_qps(rate_usd_h: float, qps: float) -> float:
    return rate_usd_h / (qps * 3.6) if qps > 0 else float("nan")


def always_on_monthly(rate_usd_h: float, hours: float = 730.0) -> float:
    """What min_containers=1 (one warm GPU container, no scale-to-zero) costs per month at this rate."""
    return rate_usd_h * hours


def breakeven_qps(rate_usd_h: float, jev_usd_per_1k: float) -> float:
    """Sustained requests/s above which one always-on GPU is cheaper than Jev's per-call price (needs capacity >= this)."""
    return rate_usd_h / (jev_usd_per_1k / 1000.0) / 3600.0


def utilisation_at_qps(qps: float, decisions_per_h: float) -> float:
    return qps * 3600.0 / decisions_per_h if decisions_per_h else float("nan")


def table(throughput: dict, prices=PRICES, utils=UTILS, jev=JEV_USD_PER_1K) -> dict:
    """throughput {config: sustained decisions/h} -> per config and price tier: USD/1K at each utilisation, the
    utilisation at which it beats each Jev reference, and the compute floor when ms/decision is also given."""
    out = {}
    for cfg, t in throughput.items():
        dph = t["dph"] if isinstance(t, dict) else t
        rows = []
        for p in prices:
            rows.append({"price": p["name"], "usd_h": round(p["usd_h"], 3), "kind": p["kind"],
                         "first_party": p["first_party"], "src": p["src"],
                         "always_on_usd_month": round(always_on_monthly(p["usd_h"]), 0),
                         "breakeven_qps_vs_jev": {k: round(breakeven_qps(p["usd_h"], v), 2) for k, v in jev.items()},
                         "usd_per_1k": {f"{int(u * 100)}%": round(usd_per_1k(p["usd_h"], dph, u), 5) for u in utils},
                         "breakeven_util_vs_jev": {k: round(breakeven_util(p["usd_h"], dph, v), 3) for k, v in jev.items()}})
        out[cfg] = {"decisions_per_h": dph, "tiers": rows}
        if isinstance(t, dict) and t.get("ms_per_decision"):
            out[cfg]["compute_floor_usd_per_1k"] = {p["name"]: round(compute_floor(p["usd_h"], t["ms_per_decision"]), 5)
                                                    for p in prices if p["first_party"]}
    return out


def render(tab: dict, price_name_contains: str = "Modal H100 on-demand (any") -> str:
    """Plain-text table: rows = config, columns = utilisation, for one price tier."""
    lines = []
    for cfg, d in tab.items():
        row = next((r for r in d["tiers"] if price_name_contains in r["price"]), d["tiers"][0])
        cells = " ".join(f"{k}:{v:.4f}" for k, v in row["usd_per_1k"].items())
        be = " ".join(f"{k}:{v:.2f}" for k, v in row["breakeven_util_vs_jev"].items())
        lines.append(f"{cfg:28s} {d['decisions_per_h']:>9.0f}/h  {cells}  | beats Jev at util {be}")
    return "\n".join(lines)


def hedge_estimate(lat_ms: list, hedge_after_ms: float, seed: int = 0, n: int = 20000) -> dict:
    """Analytic/Monte-Carlo estimate (NOT a measurement) of a hedged request to a second, independent replica: send
    the duplicate after `hedge_after_ms`, take the first answer. Draws two independent latencies from the empirical
    distribution `lat_ms`. Returns p50/p95/p99 plain vs hedged and the extra-request share."""
    import random
    rng = random.Random(seed)
    xs = sorted(lat_ms)
    if not xs:
        return {"n": 0}
    plain, hedged, extra = [], [], 0
    for _ in range(n):
        a = xs[rng.randrange(len(xs))]
        if a <= hedge_after_ms:
            plain.append(a)
            hedged.append(a)
            continue
        b = xs[rng.randrange(len(xs))]
        extra += 1
        plain.append(a)
        hedged.append(min(a, hedge_after_ms + b))
    q = lambda v, f: sorted(v)[min(len(v) - 1, int(f * len(v)))]  # noqa: E731
    return {"hedge_after_ms": hedge_after_ms, "extra_request_share": round(extra / n, 4),
            "plain": {f"p{int(f * 100)}": round(q(plain, f), 1) for f in (0.5, 0.95, 0.99)},
            "hedged": {f"p{int(f * 100)}": round(q(hedged, f), 1) for f in (0.5, 0.95, 0.99)},
            "note": "simulation from the measured single-replica distribution, replicas assumed independent"}
