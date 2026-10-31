"""cost_calc.py: cost inputs -> $/1K decisions, break-even utilisation and the GO #2 cost-claim sentence (CPU, stdlib).

  cost_calc.py --inputs inputs/cost_inputs.json [--out out/cost.json] [--md out/cost.md] [--check]

Formulas (the repo's own, oc1.costmodel / speed_bench.cost_table):
  usd_per_1k(rate_usd_h, dph, util) = rate / (dph * util) * 1000        (util = share of the instance's sustained saturated
                                                                         throughput that is actually used)
  breakeven_util(rate, dph, jev)    = (rate / dph * 1000) / jev          (above this utilisation one instance beats Jev's price)
  load_for_util(dph, util)          = dph * util / 3600 decisions per second
Claim rule (plan section 6, v3): a cost claim ALWAYS states the utilisation it assumes, the GPU and price it uses, the call mix
the throughput was measured on, and which Jev unit it compares with. The generator refuses (claim_ready false, reasons listed)
when any of those is missing, when an input is not-measured, or when the price is not tagged third-party with a fetch date.
Jev units carried side by side because they differ: Jev measured $/1K (author-run, our client run), and Jev list price per
M input tokens times tokens per decision (list: $0.042 per M input, output free, docs verified 18 Oct 2026).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

UTILS = (0.1, 0.2, 0.3, 0.4, 0.5, 0.59, 0.6, 0.7, 0.8, 0.9, 1.0)


def usd_per_1k(rate_usd_h: float, dph: float, util: float = 1.0) -> float:
    if not dph or util <= 0:
        return float("nan")
    return rate_usd_h / (dph * util) * 1000.0


def breakeven_util(rate_usd_h: float, dph: float, jev_usd_per_1k: float) -> float:
    return usd_per_1k(rate_usd_h, dph, 1.0) / jev_usd_per_1k


def load_for_util(dph: float, util: float) -> float:
    """decisions per second needed to keep one instance at `util`."""
    return dph * util / 3600.0


def jev_units(j: dict) -> dict:
    """{label: (usd_per_1k, tag dict)} for the Jev units that are present and not null."""
    out = {}
    m = j.get("usd_per_1k_measured")
    if m and m.get("value") is not None:
        out["jev_measured_usd_per_1k"] = (float(m["value"]), m)
    lp, tk = j.get("usd_per_m_input_tokens"), j.get("tokens_per_decision")
    if lp and tk and lp.get("value") is not None and tk.get("value") is not None:
        out["jev_list_price_x_tokens"] = (float(lp["value"]) * float(tk["value"]) / 1e6 * 1000.0, {"tag": "modelled", "from": "list price x tokens per decision"})
    return out


def compute(inp: dict) -> dict:
    o, j = inp["ours"], inp["jev"]
    rate, dph = o["rate_usd_h"]["value"], o["sustained_dph"]["value"]
    res = {"ours": {"gpu": o.get("gpu"), "host": o.get("host"), "mix": o.get("mix"), "rate_usd_h": o["rate_usd_h"],
                    "sustained_dph": o["sustained_dph"]}, "claim_blockers": []}
    if rate is None:
        res["claim_blockers"].append("ours.rate_usd_h is not-measured (fetch the GCP list price on the claim day; tag third-party)")
    if dph is None:
        res["claim_blockers"].append("ours.sustained_dph is not-measured (capacity_ladder.py on the L4 box)")
    ju = jev_units(j)
    if not ju:
        res["claim_blockers"].append("jev: no usable unit (usd_per_1k_measured, or usd_per_m_input_tokens with tokens_per_decision)")
    res["jev_units"] = {k: {"usd_per_1k": round(v[0], 5), **{kk: vv for kk, vv in v[1].items() if kk in ("tag", "n", "source", "from")}}
                        for k, v in ju.items()}
    if rate is None or dph is None:
        res["table"], res["breakeven"] = None, None
        res["claim"] = None
        res["claim_ready"] = False
        return res
    res["table"] = {f"{int(u * 100)}%": round(usd_per_1k(rate, dph, u), 5) for u in UTILS}
    res["usd_per_1k_at_100pct"] = round(usd_per_1k(rate, dph, 1.0), 5)
    res["breakeven"] = {k: {"util": round(breakeven_util(rate, dph, v[0]), 4),
                            "load_dec_per_s_at_breakeven": round(load_for_util(dph, breakeven_util(rate, dph, v[0])), 2)}
                        for k, v in ju.items()}
    res["capacity_dec_per_s_at_100pct"] = round(dph / 3600.0, 2)
    # the sentence
    cu = inp.get("claim_utilisation", {})
    u = cu.get("value")
    if u is None:
        res["claim_blockers"].append("claim_utilisation is not set: a cost claim must name the utilisation it assumes")
    if o["rate_usd_h"]["tag"] != "third-party":
        res["claim_blockers"].append("ours.rate_usd_h must be tagged third-party (price page + fetch date)")
    if o["sustained_dph"]["tag"] != "author-run":
        res["claim_blockers"].append("ours.sustained_dph must be author-run (with n)")
    if not o.get("mix"):
        res["claim_blockers"].append("ours.mix (the call mix the throughput was measured on) is missing")
    res["claim_ready"] = not res["claim_blockers"]
    if res["claim_ready"]:
        ours = usd_per_1k(rate, dph, u)
        parts = [f"At {int(round(u * 100))}% utilisation on one {o.get('gpu')} ({o.get('host')}, list price ${rate:.4g}/h, "
                 f"{int(dph):,} decisions/h sustained on: {o['mix']}; author-run n={o['sustained_dph']['n']}) OpenDecide costs "
                 f"${ours:.4f} per 1,000 decisions"]
        for k, v in ju.items():
            rel = "cheaper" if ours < v[0] else "more expensive"
            parts.append(f"{rel} than Jev's ${v[0]:.4f} ({k.replace('_', ' ')}; break-even {100 * breakeven_util(rate, dph, v[0]):.0f}% utilisation)")
        res["claim"] = "; ".join(parts) + ". Hosting cost only; no operations cost."
    else:
        res["claim"] = None
    return res


def render_md(r: dict, inp: dict) -> str:
    L = ["# Cost (cost_calc.py)", ""]
    if r["table"]:
        L += [f"One {r['ours']['gpu']} at ${r['ours']['rate_usd_h']['value']}/h, {int(r['ours']['sustained_dph']['value']):,} decisions/h "
              f"({r['ours']['mix']}). $ per 1,000 decisions by utilisation:", "",
              C.md_table(["utilisation", "$/1K"], [[k, v] for k, v in r["table"].items()]), ""]
        L += ["Break-even:", "", C.md_table(["Jev unit", "Jev $/1K", "break-even util", "load at break-even (dec/s)"],
              [[k, r["jev_units"][k]["usd_per_1k"], v["util"], v["load_dec_per_s_at_breakeven"]] for k, v in r["breakeven"].items()]), ""]
    else:
        L += ["Not computable yet: " + "; ".join(r["claim_blockers"]), ""]
    L += ["Claim: " + (r["claim"] or "NOT READY - " + "; ".join(r["claim_blockers"]))]
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--inputs", default=str(C.ROOT / "inputs" / "cost_inputs.json"))
    ap.add_argument("--out"), ap.add_argument("--md")
    ap.add_argument("--check", action="store_true", help="only check the tags of the inputs file")
    a = ap.parse_args(argv)
    inp = json.loads(Path(a.inputs).read_text())
    bad = C.check_tagged(inp)
    if bad:
        print("untagged or badly tagged inputs:\n  " + "\n  ".join(bad), file=sys.stderr)
        return 2
    if a.check:
        print("inputs ok")
        return 0
    r = compute(inp)
    r["tag"] = C.tag("modelled", source="cost_calc.py arithmetic on the tagged inputs")
    r["utc"] = C.utc()
    if a.out:
        C.write_json(a.out, r)
    md = render_md(r, inp)
    if a.md:
        Path(a.md).parent.mkdir(parents=True, exist_ok=True)
        Path(a.md).write_text(md)
    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
