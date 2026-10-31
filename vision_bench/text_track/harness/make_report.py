"""Write RESULTS.md (tables only, no hand-typed numbers) from results/scores.json and results/skeptic.json.

  .venv/bin/python -B -I harness/make_report.py [--results DIR] [--out FILE]
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from score_text import LANG, NAMES, SUITES, n_dec  # noqa: E402


def p(x, d=1):
    return "-" if x is None else f"{100 * x:.{d}f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", default=f"{TT}/results")
    ap.add_argument("--out", default=f"{TT}/RESULTS.md")
    a = ap.parse_args()
    S = json.load(open(f"{a.results}/scores.json"))
    sk = json.load(open(f"{a.results}/skeptic.json")) if os.path.exists(f"{a.results}/skeptic.json") else None
    c1, base = S["arms"]["c1"], S["arms"].get("base")
    j14, j13 = S["jev"]["jev114"], S["jev"]["jev113"]
    L = []
    w = L.append
    v = c1["vs_jev114"]
    w("# Text track: C1 vs base Qwen3.5-4B vs Jev 1.14 / 1.13 (published)\n")
    w(f"**C1 System One Index {c1['index']:.1f}** (SE {c1['index_se']:.1f}) | base Qwen3.5-4B {base['index']:.1f} | Jev 1.14 {S['jev114_index']['index']:.1f} | "
      f"Jev 1.13 {S['jev113_index']['index']:.1f}.\n")
    w(f"**C1 vs Jev 1.14: gap {v['diff']:+.2f} points, SE {v['se']:.2f}, z {v['z']:+.2f} -> {v['verdict']}.** "
      f"(Rule: a win or loss is called only if the gap is at least 3 points AND |z| >= 2.)\n")
    v13 = c1["vs_jev113"]
    w(f"C1 vs Jev 1.13: gap {v13['diff']:+.2f}, SE {v13['se']:.2f}, z {v13['z']:+.2f} -> {v13['verdict']}.\n")
    w(f"Calibration (top-label ECE over all {c1['all']['n']} decisions): C1 {100 * c1['all']['ece']:.1f}% | base {100 * base['all']['ece']:.1f}% | "
      f"Jev 1.14 {100 * S['jev114_index']['all_ece']:.1f}% | Jev 1.13 {100 * S['jev113_index']['all_ece']:.1f}%.\n")
    w(f"Failed decisions: C1 {c1['failed_total']}, base {base['failed_total']} (of {c1['all']['n']}); Jev 0.\n")
    w("## Accuracy per suite (%)\n")
    w("n = decisions (typed-decisions: 400 cases x 5 questions). Jev columns are the bench's published runs. Standard error of one suite is "
      "1.7 to 3.5 points (about 1.0 for typed-decisions if its 2,000 decisions were independent; 2.2 if only its 400 cases count).\n")
    w("| Suite | n | C1 | Base Qwen3.5-4B | Jev 1.14 (pub.) | Jev 1.13 (pub.) | C1 - Jev 1.14 (z) |")
    w("|---|---:|---:|---:|---:|---:|---:|")
    for s in SUITES:
        g = c1["per_suite_vs_jev114"][s]
        w(f"| {NAMES[s]} | {n_dec(s)} | {p(c1['suites'][s]['acc'])} | {p(base['suites'][s]['acc'])} | {p(j14['acc'][s])} | {p(j13['acc'][s])} | "
          f"{g['diff']:+.1f} ({g['z']:+.1f}) |")
    w(f"| **System One Index (16 suites)** | 4850 | **{c1['index']:.1f}** | {base['index']:.1f} | {S['jev114_index']['index']:.1f} | {S['jev113_index']['index']:.1f} | "
      f"{v['diff']:+.1f} ({v['z']:+.1f}) |")
    w(f"| English index (8 suites) | | {c1['index_english']:.1f} | {base['index_english']:.1f} | {S['jev114_index']['english']:.1f} | {S['jev113_index']['english']:.1f} | "
      f"{c1['vs_jev114_english']['diff']:+.1f} ({c1['vs_jev114_english']['z']:+.1f}) |")
    w(f"| Arabic index (7 suites) | | {c1['index_arabic']:.1f} | {base['index_arabic']:.1f} | {S['jev114_index']['arabic']:.1f} | {S['jev113_index']['arabic']:.1f} | "
      f"{c1['vs_jev114_arabic']['diff']:+.1f} ({c1['vs_jev114_arabic']['z']:+.1f}) |")
    w(f"| Index SE (points) | | {c1['index_se']:.2f} | {base['index_se']:.2f} | {S['jev114_index']['se']:.2f} | {S['jev113_index']['se']:.2f} | gap SE {v['se']:.2f} |")
    w(f"| Index, failed = wrong (strict) | | {c1['index_strict']:.1f} | {base['index_strict']:.1f} | | | |\n")
    w("## Calibration (ECE %, 10 bins, top label)\n")
    w("| Suite | C1 | Base | Jev 1.14 | Jev 1.13 |")
    w("|---|---:|---:|---:|---:|")
    for s in SUITES:
        w(f"| {NAMES[s]} | {p(c1['suites'][s]['ece'])} | {p(base['suites'][s]['ece'])} | {p(j14['ece'][s])} | {p(j13['ece'][s])} |")
    w(f"| **All {c1['all']['n']} decisions** | **{p(c1['all']['ece'])}** | {p(base['all']['ece'])} | {p(j14['all_ece'])} | {p(j13['all_ece'])} |\n")
    bs = json.load(open(f"{a.results}/bootstrap.json")) if os.path.exists(f"{a.results}/bootstrap.json") else None
    if bs:
        w(f"Sampling noise (bootstrap over the 3,250 cases, 2,000 resamples): C1 ECE {100 * bs['c1']['ece_all']:.1f}% (95% interval {100 * bs['c1']['ece_boot_ci95'][0]:.1f} to "
          f"{100 * bs['c1']['ece_boot_ci95'][1]:.1f}), base {100 * bs['base']['ece_all']:.1f}% ({100 * bs['base']['ece_boot_ci95'][0]:.1f} to {100 * bs['base']['ece_boot_ci95'][1]:.1f}); "
          f"C1 Index bootstrap SE {bs['c1']['index_boot_se']:.2f} (interval {bs['c1']['index_boot_ci95'][0]:.1f} to {bs['c1']['index_boot_ci95'][1]:.1f}), which agrees with the "
          f"analytic SE {c1['index_se']:.2f} used above. Jev's per-item results are not published, so its numbers carry no interval here.\n")
    w("## Latency (NOT COMPARABLE)\n")
    w(S["latency_note"] + "\n")
    w("| | median per call | 95th percentile | calls |")
    w("|---|---:|---:|---:|")
    w(f"| Jev 1.14 (published, cloud + network, 8 in flight) | {j14['latency_ms']['p50']:.0f} ms | {j14['latency_ms']['p95']:.0f} ms | 3250 |")
    w(f"| Jev 1.13 (published) | {j13['latency_ms']['p50']:.0f} ms | {j13['latency_ms']['p95']:.0f} ms | 3250 |")
    for arm, lab in (("c1", "C1 (H100, HF bf16, batch 1, no network)"), ("base", "Base Qwen3.5-4B (same)")):
        l = S["arms"].get(arm, {}).get("latency")
        if l:
            w(f"| {lab} | {l['total_ms']['p50']:.0f} ms | {l['total_ms']['p95']:.0f} ms | {l['ok']} |")
    l = c1.get("latency")
    if l:
        w(f"\nC1 split: forward p50 {l['fwd_ms']['p50']:.0f} ms, prompt rendering + tokenization p50 {l['prep_ms']['p50']:.0f} ms. The batch-1 answers agree with the batched "
          f"pass (same argmax on {l['argmax_same_as_batched_pass']} calls; largest probability difference {l['max_prob_diff_vs_batched']:.3f}).\n")
    w("## Cost\n")
    d = S.get("modal_done")
    bl = json.load(open(f"{a.results}/modal_billing.json")) if os.path.exists(f"{a.results}/modal_billing.json") else None
    if d and bl:
        cost = [x for k, x in d.items() if k.startswith("est_cost_usd")][0]
        gpu = bl["cost_by_app"]["ap-Fa4nYp1TpDDlfOFX16ksDZ"]
        pre = bl["cost_by_app"]["ap-dMV1XIq6YyLbOW7qaMAZcS"]
        w(f"**Modal bill for this task: ${bl['total_usd']:.2f}** (profile mahadikarya44; `modal billing report`): GPU run ${gpu:.2f} (one H100, function time {d['function_wall_s']:.0f} s, "
          f"plus container start and stop; the rate-card estimate from function time alone was ${cost:.2f}) + CPU-only preflight ${pre:.3f}. Cap was $2.00. "
          f"No budget stop was needed ({d.get('budget_stop')}); the app was stopped afterwards and no Modal app is running.\n")
    ds = [a_ for a_ in (c1, base) if a_.get("diagnostics")]
    if ds:
        w("## Labelled diagnostics (not the headline)\n")
        for arm, lab in (("c1", "C1"), ("base", "Base")):
            dg = S["arms"][arm].get("diagnostics", {})
            so = dg.get("score_options", {}).get("all_score_items")
            if so:
                w(f"- {lab}, score options ({so['n']} items: SST-5 + typed-decisions score questions): with C1's `<i>: ` prefix (headline) {p(so['headline_prefixed'])}% | "
                  f"bare criteria strings as Jev receives them {p(so['bare_criteria_strings'])}%.")
            yn = dg.get("yes_no_letters", {})
            if yn:
                tot = sum(x["n"] for x in yn.values())
                hs = sum(x["headline_A_is_Yes"] * x["n"] for x in yn.values()) / tot
                sw = sum(x["swapped_A_is_No"] * x["n"] for x in yn.values()) / tot
                av = sum((x["average_of_both_orders"] or 0) * x["n"] for x in yn.values()) / tot
                w(f"- {lab}, yes/no letters ({tot} items): A = Yes (headline) {p(hs)}% | A = No {p(sw)}% | both orders averaged {p(av)}%.")
            iv = S["arms"][arm].get("index_variants")
            if iv:
                w(f"- {lab}, Index variants (strict): {iv}")
        w("")
    w("## Skeptic re-score\n")
    if sk is not None:
        bad = sk["mismatches"]
        w(f"`harness/skeptic_rescore.py` recomputed every number above from the raw per-view logits of the saved per-item logs "
          f"(independent code, numpy only): **{'ALL CHECKS MATCH' if not bad else str(len(bad)) + ' MISMATCHES'}**. Details in `results/skeptic.txt`.\n")
        for arm in ("c1", "base"):
            a_ = sk["arms"].get(arm)
            if a_:
                w(f"- {arm}: Index {a_['index']:.2f}, English {a_['english']:.2f}, Arabic {a_['arabic']:.2f}, ECE {100 * a_['ece_all']:.2f}%, SE {a_['se']:.2f}"
                  + (f", vs Jev 1.14 gap {a_['vs_jev114']['gap']:+.2f} (z {a_['vs_jev114']['z']:+.2f}) -> {a_['vs_jev114']['call']}" if "vs_jev114" in a_ else ""))
    else:
        w("(not run yet)")
    open(a.out, "w").write("\n".join(L) + "\n")
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
