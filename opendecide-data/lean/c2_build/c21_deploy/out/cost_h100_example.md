# Cost (cost_calc.py)

One H100 80GB (Modal, reference) at $4.3952/h, 325,826 decisions/h (N traffic-like dev mix (speed/workloads/N.jsonl, 660 calls)). $ per 1,000 decisions by utilisation:

| utilisation | $/1K |
|---|---|
| 10% | 0.13489 |
| 20% | 0.06745 |
| 30% | 0.04496 |
| 40% | 0.03372 |
| 50% | 0.02698 |
| 59% | 0.02286 |
| 60% | 0.02248 |
| 70% | 0.01927 |
| 80% | 0.01686 |
| 90% | 0.01499 |
| 100% | 0.01349 |

Break-even:

| Jev unit | Jev $/1K | break-even util | load at break-even (dec/s) |
|---|---|---|---|
| jev_measured_usd_per_1k | 0.0234 | 0.5765 | 52.17 |
| jev_list_price_x_tokens | 0.02339 | 0.5766 | 52.19 |

Claim: At 50% utilisation on one H100 80GB (Modal, reference) (Modal (not used for new work), list price $4.395/h, 325,826 decisions/h sustained on: N traffic-like dev mix (speed/workloads/N.jsonl, 660 calls); author-run n=1320) OpenDecide costs $0.0270 per 1,000 decisions; more expensive than Jev's $0.0234 (jev measured usd per 1k; break-even 58% utilisation); more expensive than Jev's $0.0234 (jev list price x tokens; break-even 58% utilisation). Hosting cost only; no operations cost.