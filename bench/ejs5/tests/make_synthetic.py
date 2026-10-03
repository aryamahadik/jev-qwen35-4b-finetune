"""A SYNTHETIC stand-in for the ejs-5 benchmark folder (no real item is read or copied; only the author's CODE file
run_public_bench.py is copied so the AST readers see the real task specs).

  python tests/make_synthetic.py <dir>

Writes public_{route,triage,score,gate}.json (made-up texts and labels, class-balanced, commits shared across tasks),
commit_dates.json (half the commits from 2026-06-01 on, one commit without a date), public_raw.json (three made-up
published models with known accuracies, one unanswered row) and public_summary.json computed with the author's own
summarize(), so the published-numbers check of score_ejs5.py passes on it.
"""
from __future__ import annotations

import json
import random
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import ejs5lib as E  # noqa: E402

REAL_CODE = E.QUAR / "run_public_bench.py"
SIZES = {"route": 20, "triage": 16, "score": 24, "gate": 20}
ACC = {"jev": 0.70, "gpt": 0.75, "opus": 0.80}


def sid(k):
    return f"{0x5e000000 + k:08x}"


def make(d, seed=7):
    d = Path(d)
    d.mkdir(parents=True, exist_ok=True)
    shutil.copy(REAL_CODE, d / "run_public_bench.py")
    spec = E.bench_spec(d / "run_public_bench.py")
    rng = random.Random(seed)
    labels = {"route": list(spec["TASKS"]["route"]["criteria"]), "triage": list(spec["TASKS"]["triage"]["criteria"]),
              "score": list(spec["LEVELS"]), "gate": ["yes", "no"]}
    pool = list(range(48))  # 48 synthetic commits, many used by more than one task
    tasks = {}
    for t, n in SIZES.items():
        ks = rng.sample(pool, n)
        labs = [labels[t][i % len(labels[t])] for i in range(n)]
        rng.shuffle(labs)
        rows = []
        for k, lab in zip(ks, labs):
            words = " ".join(f"token{rng.randint(0, 999)}" for _ in range(rng.randint(8, 60)))
            r = {"id": sid(k), "label": lab,
                 "text": f"SYNTHETIC test item {t}-{k}: a made-up change to a fictional widget. {words}"}
            if t == "score":
                r["churn"] = rng.randint(1, 900)
            rows.append(r)
        tasks[t] = rows
        (d / spec["TASKS"][t]["file"]).write_text(json.dumps(rows, indent=1))
    ids = sorted({r["id"] for rows in tasks.values() for r in rows})
    dates = {}
    for i, x in enumerate(ids):
        if i == 0:
            continue  # one commit without a date (as in the real file)
        dates[x] = "2026-07-15T10:00:00Z" if i % 2 else "2025-11-03T09:30:00Z"
    (d / "commit_dates.json").write_text(json.dumps(dates, indent=1))
    raw, summ = {}, []
    summarize = E.author_functions(d / "run_public_bench.py")["summarize"]
    for m, key in E.PUBLISHED.items():
        for t in E.TASKS:
            recs = []
            for j, r in enumerate(tasks[t]):
                rec = {"id": r["id"], "label": r["label"], "latency_s": 0.4, "error": None}
                if m == "jev" and t == "score" and j == 0:
                    rec["error"] = "HTTP 500: synthetic"  # unanswered: counts wrong
                else:
                    ok = rng.random() < ACC[m]
                    wrong = [x for x in labels[t] if x != r["label"]]
                    rec |= {"pred": r["label"] if ok else rng.choice(wrong), "confidence": round(rng.random(), 3),
                            "cost": 1e-5}
                recs.append(rec)
            raw[f"{t}|{key}"] = recs
            summ.append(summarize(E.PUBLISHED_SUMMARY_NAME[m], t, recs, tasks[t]))
    (d / "public_raw.json").write_text(json.dumps(raw, indent=1))
    (d / "public_summary.json").write_text(json.dumps(summ, indent=1))
    return {"dir": str(d), "n_rows": sum(SIZES.values()), "n_commits": len(ids), "sizes": SIZES}


if __name__ == "__main__":
    print(make(sys.argv[1] if len(sys.argv) > 1 else HERE / "synthetic"))
