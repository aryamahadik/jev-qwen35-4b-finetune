"""TEACH-0 scorer (PREREG A36): Claude teachers vs Jev vs C1 on the 2,000-row dev sample T; report-only.
  ../.venv/bin/python teach0/score.py      -> teach0/REPORT.md + report.json
Teacher answers: teach0/answers/<model>.json = [{qid, answer, confidence}] (from the agents). Accuracy uses gate_dev's
scoring (argmax, ties wrong). A teacher's answer string IS its argmax; an answer not in the options is wrong. Yes/no
Brier uses the stated confidence (p_yes = c for "yes", 1 - c for "no", clamped to [0, 1])."""
import json, random, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parent
sys.path.insert(0, str(LEAN)); sys.path.insert(0, str(LEAN / "hosting"))
import gate_dev  # noqa: E402  (read-only scoring)
import speed_bench as sb  # noqa: E402

AUTHORED = {"hard_dev", "pg_dev"}  # possibly LLM-authored: reported, not in the decision subset
BOOTS, SEED = 10000, 0


def load_jsonl(p):
    return [json.loads(l) for l in open(p)] if Path(p).exists() else []


def teacher_probs(row, a):
    ans, c = str(a.get("answer", "")).strip(), min(1.0, max(0.0, float(a.get("confidence", 0.5))))
    if row["qtype"] == "noul":
        if ans.lower() not in ("yes", "no"):
            return None, None
        yes = ans.lower() == "yes"
        acc_p = {"yes": 1.0 if yes else 0.0, "no": 0.0 if yes else 1.0}
        py = c if yes else 1.0 - c
        return acc_p, {"yes": py, "no": 1.0 - py}
    if ans not in row["options"]:
        return None, None
    return {o: (1.0 if o == ans else 0.0) for o in row["options"]}, None


def main():
    samp = json.loads((HERE / "sample.json").read_text())
    key = json.loads((HERE / "key" / "key.json").read_text())
    rows = {}
    for sp in gate_dev.SPLITS.split(","):
        for l in open(LEAN / "data" / f"{sp}.jsonl"):
            r = json.loads(l); r["split"] = sp; rows[r["id"]] = r
    T = samp["S"] + samp["U"]
    only = sys.argv[sys.argv.index("--rows-of") + 1] if "--rows-of" in sys.argv else None
    S, U = set(samp["S"]), set(samp["U"])
    models = {}
    jev = {r["id"]: r["probs"] for r in load_jsonl(LEAN / "speed/speed2_20261013/JEV/answers_S.jsonl")}
    jev.update({r["id"]: r["probs"] for r in load_jsonl(HERE / "jev_U/JEV/answers_S.jsonl")})
    models["Jev"] = {i: (jev.get(i), jev.get(i)) for i in T}
    c1 = sb.load_stored("q35_4b_main500k_pre_served")
    models["C1"] = {i: (c1.get(i), c1.get(i)) for i in T}
    for f in sorted((HERE / "answers").glob("*.json")):
        ans = {a["qid"]: a for a in json.loads(f.read_text())}
        m = {}
        for qid, k in key.items():
            a = ans.get(qid)
            m[k["id"]] = teacher_probs(rows[k["id"]], a) if a else (None, None)
        models[f.stem] = m
    if only:  # restrict every model to the rows this teacher answered (paired subset; A36 addendum)
        T = [i for i in T if models[only][i][0] is not None or i in {key[q]["id"] for q in
             json.loads((HERE / "subsets" / f"{only}_qids.json").read_text())}]
        S, U = S & set(T), U & set(T)
    ok = {name: {i: gate_dev.score(rows[i], m[i][0])[0] for i in T} for name, m in models.items()}
    brier = {}
    for name, m in models.items():
        b = [(float(m[i][1]["yes"]) - rows[i]["gold"]) ** 2 for i in T
             if rows[i]["qtype"] == "noul" and m[i][1] is not None]
        nn = sum(1 for i in T if rows[i]["qtype"] == "noul")
        brier[name] = (sum(b) / len(b) if b else None, len(b), nn)
    subsets = {"T": T, "S": [i for i in T if i in S], "U": [i for i in T if i in U],
               "public (decision)": [i for i in T if rows[i]["split"] not in AUTHORED],
               "authored (hard_dev, pg_dev)": [i for i in T if rows[i]["split"] in AUTHORED],
               "yes/no": [i for i in T if rows[i]["qtype"] == "noul"],
               "choice": [i for i in T if rows[i]["qtype"] == "choice"]}
    for sp in gate_dev.SPLITS.split(","):
        subsets[f"split {sp}"] = [i for i in T if rows[i]["split"] == sp]
    acc = {s: {n: 100.0 * sum(ok[n][i] for i in ids) / len(ids) for n in models} for s, ids in subsets.items() if ids}
    rng = random.Random(SEED)

    def boot(ids, a, b):
        d = [ok[a][i] - ok[b][i] for i in ids]
        n = len(d); pt = 100.0 * sum(d) / n; xs = []
        for _ in range(BOOTS):
            xs.append(100.0 * sum(d[rng.randrange(n)] for _ in range(n)) / n)
        xs.sort()
        return pt, xs[int(0.025 * BOOTS)], xs[int(0.975 * BOOTS) - 1]

    pub = subsets["public (decision)"]
    teachers = [n for n in models if n not in ("Jev", "C1")]
    diffs = {t: {"vs Jev": boot(pub, t, "Jev"), "vs C1": boot(pub, t, "C1")} for t in teachers}
    diffs["C1"] = {"vs Jev": boot(pub, "C1", "Jev")}
    verdict = {}
    for t in teachers:
        pt, lo, hi = diffs[t]["vs Jev"]
        verdict[t] = "PROCEED (a)" if pt >= 5.0 and lo > 0 else ("MARGINAL (b)" if pt > 0 else "STOP (c)")
    cover = {n: sum(1 for i in T if models[n][i][0] is not None) for n in models}
    names = list(models)
    L = ["# TEACH-0 report (PREREG A36): Claude teachers vs Jev vs C1, 2,000 dev rows", "",
         f"Sample T sha {samp['T_sha256'][:16]}: {len(T)} rows scored (S {len(S)} + U {len(U)}){' = the rows of ' + only if only else ''}. Answered rows: "
         + ", ".join(f"{n} {cover[n]}" for n in names) + ". Missing or invalid answers count as wrong.", "",
         "## Accuracy (%)", "", "| subset | n | " + " | ".join(names) + " |", "|---|---|" + "---|" * len(names)]
    for s, ids in subsets.items():
        if ids:
            L.append(f"| {s} | {len(ids)} | " + " | ".join(f"{acc[s][n]:.1f}" for n in names) + " |")
    L += ["", "## Yes/no Brier (lower is better; teachers from stated confidence)", "",
          "| model | Brier | rows with a probability / yes-no rows |", "|---|---|---|"]
    for n in names:
        b, k, nn = brier[n]
        L.append(f"| {n} | {'-' if b is None else f'{b:.3f}'} | {k} / {nn} |")
    L += ["", "## Decision (public-source subset, paired bootstrap 95% CI, 10,000 draws)", "",
          "| model | diff vs Jev (pt) | 95% CI | diff vs C1 (pt) | 95% CI | A36 verdict |", "|---|---|---|---|---|---|"]
    for t in teachers:
        pj, lj, hj = diffs[t]["vs Jev"]; pc, lc, hc = diffs[t]["vs C1"]
        L.append(f"| {t} | {pj:+.1f} | [{lj:+.1f}, {hj:+.1f}] | {pc:+.1f} | [{lc:+.1f}, {hc:+.1f}] | **{verdict[t]}** |")
    pj, lj, hj = diffs["C1"]["vs Jev"]
    L.append(f"| C1 (context) | {pj:+.1f} | [{lj:+.1f}, {hj:+.1f}] | - | - | - |")
    (HERE / (f"REPORT_{only}.md" if only else "REPORT.md")).write_text("\n".join(L) + "\n")
    (HERE / (f"report_{only}.json" if only else "report.json")).write_text(json.dumps({"acc": acc, "brier": brier, "diffs": diffs, "verdict": verdict,
                                                   "cover": cover}, indent=1))
    print("\n".join(L))


if __name__ == "__main__":
    main()
