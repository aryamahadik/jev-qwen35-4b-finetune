"""G10 balance (C_DATA_SPEC v4 8 G10), independent re-run on public-2's rows and reserve (gated) and dev (reported).
Family = public dataset (source). Bin = meta.difficulty_bin (None on every public row: one bin).
Yes/no:  dataset yes rate 50 +/- 2 pp; every dataset x wording x bin x negation-count cell (k_all of the question
         text = instructions, c_src/common/negcount.py) 50 +/- 2 pp. A cell whose size makes +/- 2 pp unreachable
         (odd n < 25) is reported separately and must sit at the closest reachable rate (|yes - n/2| = 0.5).
Choice:  gold position uniform per option bucket k (stored order; chi-square p > 0.01) per dataset and pooled;
         'longest option is gold' (every displayed option, ties split 1/m) within +/- 2 pp of mean 1/k per dataset;
         abstain options wrong on >= 50% of the rows that show them (per dataset and pooled);
         'attack present' uncorrelated with the label: no public-2 row carries an attack (checked: no attack meta).
"""
import sys
from collections import Counter, defaultdict

from scipy.stats import chisquare

from qclib import ABSTAIN, DATASETS, LEAN, load_all, write_gate

sys.path.insert(0, str(LEAN / "c_src" / "common"))
import negcount  # noqa: E402

TOL = 0.02


def gl(r):
    L = [len(o) for o in r["options"]]
    return 1.0 / L.count(max(L)) if len(r["gold"]) == max(L) else 0.0


def check(rows):
    out, fails = {}, []
    for ds in DATASETS:
        R = [r for r in rows if r["source"] == ds]
        yn = [r for r in R if r["qtype"] == "noul"]
        ch = [r for r in R if r["qtype"] == "choice"]
        d = {"rows": len(R), "yes_no": len(yn), "choice": len(ch)}
        if yn:
            y = sum(r["gold"] for r in yn)
            d["yes_rate"] = round(y / len(yn), 4)
            if abs(y / len(yn) - .5) > TOL:
                fails.append(f"{ds}: yes rate {y}/{len(yn)}")
            cells = defaultdict(lambda: [0, 0])
            for r in yn:
                k = negcount.count(r["instructions"]).k_all
                c = cells[(r["meta"]["wording_id"], str(r["meta"].get("difficulty_bin")), k)]
                c[0] += 1
                c[1] += int(r["gold"])
            off, small = {}, {}
            for (w, b, k), (n, yy) in cells.items():
                if abs(yy / n - .5) <= TOL:
                    continue
                if n % 2 == 1 and n < 25 and abs(yy - n / 2) == .5:
                    small[f"{w}|bin={b}|k_all={k}"] = [yy, n]
                else:
                    off[f"{w}|bin={b}|k_all={k}"] = [yy, n]
            d["cells"] = len(cells)
            d["cells_k_all_dist"] = dict(Counter(k for (_, _, k) in cells))
            d["cells_off_2pp"] = off
            d["cells_odd_small_at_closest_rate"] = small
            if off:
                fails.append(f"{ds}: {len(off)} wording x bin x k_all cells off 50 +/- 2 pp")
        if ch:
            S = sum(gl(r) for r in ch)
            E = sum(1 / len(r["options"]) for r in ch)
            d["gold_longest_rate"] = round(S / len(ch), 4)
            d["gold_longest_expected"] = round(E / len(ch), 4)
            d["gold_longest_diff_pp"] = round(100 * (S - E) / len(ch), 2)
            if abs(S - E) / len(ch) > TOL:
                fails.append(f"{ds}: longest-is-gold {d['gold_longest_diff_pp']} pp")
            byfr = defaultdict(lambda: [0.0, 0.0, 0])
            for r in ch:
                f = byfr[r["meta"]["framing"]]
                f[0] += gl(r)
                f[1] += 1 / len(r["options"])
                f[2] += 1
            d["gold_longest_diff_pp_by_framing"] = {k: round(100 * (a - b) / n, 2) for k, (a, b, n) in byfr.items()}
            pos = defaultdict(Counter)
            for r in ch:
                pos[len(r["options"])][r["options"].index(r["gold"])] += 1
            d["gold_position_chi2_p_by_k"] = {}
            for k, c in sorted(pos.items()):
                obs = [c[i] for i in range(k)]
                p = float(chisquare(obs).pvalue) if sum(obs) >= k else 1.0
                d["gold_position_chi2_p_by_k"][str(k)] = {"n": sum(obs), "p": round(p, 4)}
                if p <= 0.01:
                    fails.append(f"{ds}: gold position k={k} chi2 p={p:.4f}")
            ab = [r for r in ch if any(o in ABSTAIN for o in r["options"])]
            abg = sum(r["gold"] in ABSTAIN for r in ab)
            d["abstain_rows"] = len(ab)
            d["abstain_wrong_rate"] = round(1 - abg / len(ab), 4) if ab else None
            if ab and abg / len(ab) > .5:
                fails.append(f"{ds}: abstain gold {abg}/{len(ab)}")
        out[ds] = d
    ch = [r for r in rows if r["qtype"] == "choice"]
    pos = defaultdict(Counter)
    for r in ch:
        pos[len(r["options"])][r["options"].index(r["gold"])] += 1
    out["pooled_gold_position_chi2_p_by_k"] = {}
    for k, c in sorted(pos.items()):
        obs = [c[i] for i in range(k)]
        p = float(chisquare(obs).pvalue) if sum(obs) >= k else 1.0
        out["pooled_gold_position_chi2_p_by_k"][str(k)] = {"n": sum(obs), "p": round(p, 4)}
        if p <= 0.01:
            fails.append(f"pooled: gold position k={k} chi2 p={p:.4f}")
    attack = sum(1 for r in rows if any("attack" in k or "inject" in k for k in r["meta"]))
    out["rows_with_attack_meta"] = attack
    return out, fails


def main():
    data = load_all()
    nums, fails = {}, []
    for name, rows in (("rows_r1", data["rows_r1"]), ("reserve_r1", data["reserve_r1"]),
                       ("rows_plus_reserve", data["rows_r1"] + data["reserve_r1"]), ("dev_mt_r1", data["dev_mt_r1"])):
        o, f = check(rows)
        nums[name] = o
        if name in ("rows_r1", "reserve_r1"):
            fails += [f"{name}: {x}" for x in f]
        else:
            nums[f"{name}_report_only_misses"] = f
    ok = not fails
    write_gate("G10", ok, nums, fails=fails)
    print("G10", ok, fails[:10])


if __name__ == "__main__":
    main()
