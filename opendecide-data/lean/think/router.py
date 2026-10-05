"""A17 phase B router: which questions leave C1's one-pass answer and go to the think path. CPU only, numpy only.

Fit ONLY on our own dev splits (gate_dev.SPLITS, data/<split>.jsonl). Never on OHS-1/2/3, Nimble, the Decision Index,
ejs-5, JevBench or the sealed suite: every input path and task key is checked (see _guard_path, _dev_key).

Features (one row + C1's one-pass probabilities; never the source/set/track/benchmark fields, so blanking them leaves
routing unchanged): top probability, margin (top-1 minus top-2), normalised entropy, yes/no row, log option count,
log card length, log text length, log question length, digit density, and simple question-type cues (maths, code,
negation, causal, time/comparison), plus (1 - top) x maths cue / code cue / digit density.
Target "thinking helps on this item": y = (think_ok - c1_ok + 1) / 2, i.e. 1 = think fixes C1, 0.5 = no change,
0 = think breaks C1. A logistic model with these fractional targets estimates E[y | x], so 2p - 1 is the expected
accuracy gain of routing that item. think_ok uses the A17-B0b fallback: an unparsed think answer keeps C1's answer.
The think answers come from the L4 (bench/think_check/think_rows.py, 1,024-token budget, the A17-B0b think path):
`tasks` writes the exact task list and commands, it runs nothing.
Sampling (L4 time): every dev row with C1 top < 0.8 (stratum "lo", weight 1) plus a fixed hash sample of the rows
with top >= 0.8 (stratum "hi", share --hi-share, weight 1 / share). All estimates are weighted back to the full dev set.
Fit / confirm: 60/40 by sha256 of the group id (common.split_of), so paired rows stay together.
Model: L2 logistic regression (IRLS, standardised features, l2 fixed a priori = 1.0). Threshold: the score whose
weighted routed share on dev-fit is closest to --route-share (default 10%), but never routing an item with expected
gain <= --min-gain (default 0), so the share can come out below 10%.

  python think/router.py tasks [--hi-share 0.10]     # think/data/router/think_tasks_dev.jsonl + commands
  python think/router.py commands                    # print the L4 commands again
  python think/router.py fit --think think/data/router/think_out_dev.jsonl   # -> think/data/router/router.json
  python think/router.py route --rows R.jsonl --c1 P.jsonl --out D.jsonl [--model router.json]
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
LEAN = HERE.parent
sys.path.insert(0, str(HERE))
from common import conf_features, gold_key, keys, read_jsonl, sha256_file, split_of, write_jsonl  # noqa: E402

OUT = HERE / "data" / "router"
C1 = "q35_4b_main500k"
TAU_B0B = 0.8  # A17-B0b fixed rule, kept as the comparison
FORBIDDEN = ("ohs", "nimble", "decision_index", "external_quarantine", "ejs", "jevbench", "jev_", "sealed", "prep89",
             "c_spec/sealed_brief", "longbench", "v154")
L2 = 1.0
# L4 VM (HANDOFF.md): od-l4, us-central1-a, venv ~/od, lean at ~/lean; think_rows.py lives next to its outputs.
VM, ZONE, PY, REMOTE = "od-l4", "us-central1-a", "~/od/bin/python", "~/think_check"
L4_SEC_PER_ITEM = 7.0  # A17-B0c: 6.98 s per item at batch 16, 1,024 tokens (bench/think_check/out_ohs.jsonl)


def dev_splits() -> list:
    """gate_dev.SPLITS read from the source (no import: gate_dev pulls in heavy modules)."""
    tree = ast.parse((LEAN / "gate_dev.py").read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "SPLITS" for t in node.targets):
            return ast.literal_eval(node.value).split(",")
    raise RuntimeError("gate_dev.SPLITS not found")


def _guard_path(p) -> Path:
    s = str(p).lower()
    bad = [f for f in FORBIDDEN if f in s]
    if bad:
        raise SystemExit(f"refused: {p} matches a never-fit name {bad} (router inputs are our dev splits only)")
    return Path(p)


def _dev_key(split: str, rid: str) -> str:
    return f"dev|{split}|{rid}"


# ---------------------------------------------------------------------------------------------------- features
_W = re.compile(r"[A-Za-z]+")
_MATH = re.compile(r"\d\s*[\+\-\*/×÷=^]\s*\d|\d\s*%|\b(calculate|compute|how many|how much|total|sum|average|mean|"
                   r"percent(age)?|probability|ratio|solve|equation|integer|remainder|digits?)\b", re.I)
_CODE = re.compile(r"```|\bdef \w+\(|\breturn\b|print\(|\bfunction\b|=>|\bassert\b|\bfor \w+ in\b|\[\s*\d+\s*:\s*\d*\s*\]")
_NEG = re.compile(r"\b(not|never|no|none|except|unless|without|neither|nor)\b", re.I)
_CAUSAL = re.compile(r"\b(cause[sd]?|because|effect|if|then|would|implies|therefore|consequently|due to)\b", re.I)
_TIME = re.compile(r"\b(before|after|earlier|later|date|year|deadline|until|since|more than|less than|at least|"
                   r"at most|older|younger|larger|smaller)\b", re.I)
_NUM = re.compile(r"\d+(?:[.,]\d+)*")
FEATURES = ["top", "margin", "entropy", "is_noul", "log_n_options", "log_card", "log_text", "log_question",
            "digit_density", "cue_math", "cue_code", "cue_neg", "cue_causal", "cue_time",
            "unsure_x_math", "unsure_x_code", "unsure_x_digits"]


def _text(row) -> str:
    return f"{row.get('state') or ''}\n{row.get('instructions') or ''}\n" + "\n".join(row.get("options") or [])


def cues(row) -> dict:
    t, q = _text(row), row.get("instructions") or ""
    nums = len(_NUM.findall(t))
    words = len(_W.findall(t)) + nums
    return {"digit_density": min(1.0, nums / (words + 1.0)), "cue_math": float(bool(_MATH.search(t))),
            "cue_code": float(bool(_CODE.search(t))), "cue_neg": float(bool(_NEG.search(q))),
            "cue_causal": float(bool(_CAUSAL.search(t))), "cue_time": float(bool(_TIME.search(t)))}


def numeric_options(row) -> bool:
    opts = row.get("options") or []
    return len(opts) >= 2 and all(re.fullmatch(r"\s*[-+$]?\d[\d,]*(\.\d+)?\s*%?\s*\w{0,8}\s*", o or "") for o in opts)


def think_type(row) -> str:
    """Policy choice (A17): maths-like -> short step-by-step + vote; everything else -> capped thinking."""
    c = cues(row)
    if numeric_options(row) or (c["cue_math"] and c["digit_density"] >= 0.03):
        return "math"
    return "code" if c["cue_code"] else "other"


def policy_for(row) -> str:
    return "short_cot" if think_type(row) == "math" else "capped_think"


def features(row, probs: dict) -> dict:
    cf = conf_features(row, probs or {})
    f = {"top": cf["top"], "margin": cf["margin"], "entropy": cf["entropy"],
         "is_noul": float(row["qtype"] == "noul"), "log_n_options": math.log(max(cf["n_options"], 1)),
         "log_card": math.log1p(len(row.get("card") or "")), "log_text": math.log1p(len(row.get("state") or "")),
         "log_question": math.log1p(len(row.get("instructions") or ""))}
    f.update(cues(row))
    u = 1.0 - cf["top"]  # interactions: "unsure AND maths/code-like" (FAST_THINK_PLAN 1a routing rule)
    f.update(unsure_x_math=u * f["cue_math"], unsure_x_code=u * f["cue_code"], unsure_x_digits=u * f["digit_density"])
    return f


def vec(f: dict) -> list:
    return [float(f[k]) for k in FEATURES]


def c1_ok(row, probs) -> float:
    """gate_dev.score rule: right only when the gold key is the unique arg-max."""
    ks, g = keys(row), gold_key(row)
    p = {k: float((probs or {}).get(k, 0.0)) for k in ks}
    best = max(p.values())
    return float([k for k, v in p.items() if v == best] == [g])


def c1_key(row, probs):
    ks = keys(row)
    p = [float((probs or {}).get(k, 0.0)) for k in ks]
    return ks[max(range(len(ks)), key=lambda i: (p[i], -i))]


# ---------------------------------------------------------------------------------------------------- dev data
def _hshare(key: str, salt="think-router-hi") -> float:
    return int(hashlib.sha256(f"{salt}:{key}".encode()).hexdigest()[:12], 16) / float(16 ** 12)


def load_dev(splits=None, data_dir=None, preds_root=None, model=C1) -> list:
    """[{key, split, row, probs}] for every dev row that has a C1 one-pass prediction."""
    data_dir, preds_root = Path(data_dir or LEAN / "data"), Path(preds_root or LEAN)
    out = []
    for sp in splits or dev_splits():
        rows = list(read_jsonl(_guard_path(data_dir / f"{sp}.jsonl")))
        probs = {r["id"]: r["probs"] for r in read_jsonl(_guard_path(preds_root / f"preds_{sp}" / f"{model}.jsonl"))}
        for r in rows:
            if r["id"] in probs:
                out.append({"key": _dev_key(sp, r["id"]), "split": sp, "row": r, "probs": probs[r["id"]]})
    return out


def stratum(item, hi_share: float):
    """('lo', 1.0) | ('hi', 1/share) | (None, 0) when the hi row is not sampled."""
    top = conf_features(item["row"], item["probs"])["top"]
    if top < TAU_B0B:
        return "lo", 1.0
    return ("hi", 1.0 / hi_share) if _hshare(item["key"]) < hi_share else (None, 0.0)


def cmd_tasks(a):
    items = load_dev()
    tasks, local, n = [], [], defaultdict(lambda: defaultdict(int))
    for it in items:
        st, w = stratum(it, a.hi_share)
        n[it["split"]][st or "unsampled"] += 1
        if st is None:
            continue
        row = {k: v for k, v in it["row"].items() if k != "gold"}  # gold never leaves the laptop
        tasks.append({"key": it["key"], "row": row})
        local.append({"key": it["key"], "stratum": st, "weight": w,
                      "part": split_of(it["row"].get("group_id") or it["row"]["id"])})
    OUT.mkdir(parents=True, exist_ok=True)
    tf = OUT / "think_tasks_dev.jsonl"
    write_jsonl(tf, tasks)
    write_jsonl(OUT / "think_tasks_dev_local.jsonl", local)
    man = {"splits": dev_splits(), "c1": C1, "hi_share": a.hi_share, "tau_lo": TAU_B0B, "tasks": len(tasks),
           "tasks_sha256": sha256_file(tf), "per_split": {s: dict(v) for s, v in n.items()},
           "est_l4_hours": round(len(tasks) * L4_SEC_PER_ITEM / 3600, 1), "commands": commands()}
    (OUT / "tasks_manifest.json").write_text(json.dumps(man, indent=2) + "\n")
    print(json.dumps({k: man[k] for k in ("tasks", "tasks_sha256", "est_l4_hours", "per_split")}, indent=1))
    print("\n".join(man["commands"]))


def commands() -> list:
    """The exact L4 steps (run by the orchestrator, never by this script). think_rows.py = the A17-B0b think path."""
    loc = "opendecide-data/lean/think/data/router"
    return [
        f"gcloud compute instances start {VM} --zone {ZONE}",
        f"gcloud compute ssh {VM} --zone {ZONE} --command 'mkdir -p {REMOTE}'",
        f"gcloud compute scp bench/think_check/think_rows.py {loc}/think_tasks_dev.jsonl {VM}:{REMOTE}/ --zone {ZONE}",
        f"gcloud compute ssh {VM} --zone {ZONE} --command 'cd {REMOTE} && sha256sum think_tasks_dev.jsonl && "
        f"nohup {PY} think_rows.py --tasks think_tasks_dev.jsonl --out think_out_dev.jsonl --budget 1024 --bs 16 "
        f"> think_dev.log 2>&1 &'",
        f"gcloud compute ssh {VM} --zone {ZONE} --command 'tail -2 {REMOTE}/think_dev.log'   # poll until RUN DONE",
        f"gcloud compute scp {VM}:{REMOTE}/think_out_dev.jsonl {loc}/ --zone {ZONE}",
        f"gcloud compute instances stop {VM} --zone {ZONE}",
        f"opendecide-data/.venv/bin/python opendecide-data/lean/think/router.py fit --think {loc}/think_out_dev.jsonl",
    ]


def cmd_commands(a):
    print("\n".join(commands()))


# ---------------------------------------------------------------------------------------------------- model
def _sig(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -40, 40)))


def fit_logistic(X, y, w, l2=L2, iters=100):
    """Weighted L2 logistic regression with fractional targets, by IRLS (Newton). Intercept not penalised."""
    X, y, w = np.asarray(X, float), np.asarray(y, float), np.asarray(w, float)
    w = w / w.mean()
    Xb = np.hstack([np.ones((len(X), 1)), X])
    R = l2 * np.eye(Xb.shape[1])
    R[0, 0] = 0.0
    b = np.zeros(Xb.shape[1])
    for _ in range(iters):
        p = _sig(Xb @ b)
        g = Xb.T @ (w * (p - y)) + R @ b
        H = (Xb * (w * p * (1 - p))[:, None]).T @ Xb + R + 1e-9 * np.eye(len(b))
        step = np.linalg.solve(H, g)
        b -= step
        if np.max(np.abs(step)) < 1e-10:
            break
    return b


def pick_threshold(s, w, share) -> tuple:
    """(threshold t, weighted share routed with score >= t): the t whose share is closest to `share`; on a tie the
    higher t (fewer routed). Tied scores are routed together, so the share is not always exactly `share`."""
    s, w = np.asarray(s, float), np.asarray(w, float)
    o = np.argsort(s, kind="stable")
    ss, cw = s[o], np.concatenate([[0.0], np.cumsum(w[o])])
    u = np.unique(ss)
    shares = (cw[-1] - cw[np.searchsorted(ss, u, side="left")]) / cw[-1]
    d = np.abs(shares - share)
    best = np.where(d <= d.min() + 1e-12)[0][-1]
    return float(u[best]), float(shares[best])


class Router:
    def __init__(self, m: dict):
        self.m = m
        self.mu, self.sd = np.array(m["mean"]), np.array(m["std"])
        self.b = np.array([m["intercept"]] + m["coef"])

    def score(self, row, probs) -> float:
        """Estimated E[y]: 0.5 + expected accuracy gain / 2."""
        z = (np.array(vec(features(row, probs))) - self.mu) / self.sd
        return float(_sig(self.b[0] + z @ self.b[1:]))

    def decide(self, row, probs) -> dict:
        s = self.score(row, probs)
        r = s >= self.m["threshold"]
        return {"route": bool(r), "score": round(s, 6), "gain_est": round(2 * s - 1, 6),
                "think_type": think_type(row), "policy": policy_for(row) if r else "fast"}


def think_ok_of(row, probs, th: dict) -> float:
    """A17-B0b: the think answer when parsed, else C1's answer (fallback)."""
    pk = (th or {}).get("pred_key")
    if pk is None:
        return c1_ok(row, probs)
    return float(pk == gold_key(row))


def build_table(items, think: dict, local: dict):
    """Rows that have a think answer: features, target, weight, part, split."""
    T = []
    for it in items:
        k = it["key"]
        if k not in think or k not in local:
            continue
        r, p = it["row"], it["probs"]
        c, t = c1_ok(r, p), think_ok_of(r, p, think[k])
        T.append({"key": k, "split": it["split"], "x": vec(features(r, p)), "c1": c, "th": t,
                  "y": (t - c + 1.0) / 2.0, "w": local[k]["weight"], "part": local[k]["part"],
                  "top": conf_features(r, p)["top"], "noul": r["qtype"] == "noul", "parsed": think[k].get("pred_key") is not None,
                  "think_tokens": think[k].get("think_tokens")})
    return T


def evaluate(T, route, n_boot=1000, seed=0) -> dict:
    """Weighted (back to the full dev set) routing share and accuracy, C1 alone vs C1 + think on routed rows."""
    if not T:
        return {"n": 0}
    w = np.array([t["w"] for t in T])
    c1 = np.array([t["c1"] for t in T])
    sy = np.array([t["th"] if r else t["c1"] for t, r in zip(T, route)])
    rt = np.array(route, float)
    d = sy - c1
    rep = {"n": len(T), "weighted_n": round(float(w.sum()), 1), "route_share": round(float((w * rt).sum() / w.sum()), 4),
           "c1_acc": round(100 * float((w * c1).sum() / w.sum()), 2),
           "system_acc": round(100 * float((w * sy).sum() / w.sum()), 2),
           "gain_pts": round(100 * float((w * d).sum() / w.sum()), 2),
           "routed_fixed": int(((d > 0) & (rt > 0)).sum()), "routed_broken": int(((d < 0) & (rt > 0)).sum()),
           "routed_gain_per_item_pts": round(100 * float((w * d * rt).sum() / max((w * rt).sum(), 1e-9)), 2)}
    rng = np.random.default_rng(seed)
    bs = []
    for _ in range(n_boot):
        i = rng.integers(0, len(T), len(T))
        bs.append(100 * float((w[i] * d[i]).sum() / w[i].sum()))
    rep["gain_ci95"] = [round(float(np.percentile(bs, 2.5)), 2), round(float(np.percentile(bs, 97.5)), 2)]
    per = defaultdict(lambda: [0.0, 0.0, 0.0])
    for t, r, dd in zip(T, route, d):
        per[t["split"]][0] += t["w"]
        per[t["split"]][1] += t["w"] * float(r)
        per[t["split"]][2] += t["w"] * dd
    rep["per_split"] = {s: {"route_share": round(v[1] / v[0], 4), "gain_pts": round(100 * v[2] / v[0], 2)}
                        for s, v in sorted(per.items())}
    return rep


def cmd_fit(a):
    tp = _guard_path(a.think)
    splits = set(dev_splits())
    think = {}
    for r in read_jsonl(tp):
        k = r["key"]
        if not k.startswith("dev|") or k.split("|")[1] not in splits:
            raise SystemExit(f"refused: think output key {k!r} is not one of our dev splits")
        think[k] = r
    local = {r["key"]: r for r in read_jsonl(OUT / "think_tasks_dev_local.jsonl")}
    T = build_table(load_dev(), think, local)
    fit = [t for t in T if t["part"] == "dev_fit"]
    con = [t for t in T if t["part"] == "dev_confirm"]
    if len(fit) < 50:
        raise SystemExit(f"only {len(fit)} dev-fit rows with think answers; run the L4 step first")
    X = np.array([t["x"] for t in fit])
    w = np.array([t["w"] for t in fit])
    mu = (w[:, None] * X).sum(0) / w.sum()
    sd = np.sqrt((w[:, None] * (X - mu) ** 2).sum(0) / w.sum())
    sd[sd < 1e-9] = 1.0
    b = fit_logistic((X - mu) / sd, [t["y"] for t in fit], w, l2=a.l2)
    s_fit = _sig(np.hstack([np.ones((len(fit), 1)), (X - mu) / sd]) @ b)
    thr_q, _ = pick_threshold(s_fit, w, a.route_share)
    thr = max(thr_q, float(np.nextafter(0.5 + a.min_gain / 2.0, 1.0)))
    m = {"features": FEATURES, "mean": mu.tolist(), "std": sd.tolist(), "intercept": float(b[0]),
         "coef": b[1:].tolist(), "threshold": thr, "threshold_quantile": thr_q, "route_share_target": a.route_share,
         "min_gain": a.min_gain, "l2": a.l2, "c1": C1, "target": "(think_ok - c1_ok + 1) / 2, A17-B0b fallback",
         "fit_on": sorted(splits), "inputs": {"think": str(tp), "think_sha256": sha256_file(tp)}}
    R = Router(m)
    rep = {}
    for name, part in (("dev_fit", fit), ("dev_confirm", con)):
        sc = [float(_sig(R.b[0] + ((np.array(t["x"]) - mu) / sd) @ R.b[1:])) for t in part]
        rep[name] = {"router": evaluate(part, [s >= thr for s in sc]),
                     "b0b_top_lt_0.8": evaluate(part, [t["top"] < TAU_B0B for t in part]),
                     "think_all_sampled": evaluate(part, [True] * len(part))}
    m["report"] = rep
    m["coef_by_feature"] = {f: round(c, 4) for f, c in zip(FEATURES, b[1:])}
    out = Path(a.model)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(m, indent=2) + "\n")
    brief = {p: {k: rep[p]["router"].get(k) for k in ("n", "route_share", "c1_acc", "system_acc", "gain_pts", "gain_ci95")}
             for p in rep}
    print(json.dumps({"threshold": round(thr, 4), **brief}, indent=1))
    print(f"wrote {out}")


def load_router(path=None) -> Router:
    return Router(json.loads(Path(path or OUT / "router.json").read_text()))


def cmd_route(a):
    R = load_router(a.model)
    probs = {r["id"]: r["probs"] for r in read_jsonl(a.c1)}
    out, n = [], defaultdict(int)
    for row in read_jsonl(a.rows):
        p = probs.get(row["id"])
        if p is None:
            raise SystemExit(f"no C1 prediction for {row['id']}")
        d = {"id": row["id"], **R.decide(row, p), "c1_key": c1_key(row, p)}
        n[d["policy"]] += 1
        out.append(d)
    write_jsonl(a.out, out)
    print(json.dumps({"rows": len(out), "routed": sum(d["route"] for d in out), "by_policy": dict(n)}))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("tasks")
    p.add_argument("--hi-share", type=float, default=0.10)
    p.set_defaults(func=cmd_tasks)
    sub.add_parser("commands").set_defaults(func=cmd_commands)
    p = sub.add_parser("fit")
    p.add_argument("--think", required=True)
    p.add_argument("--model", default=str(OUT / "router.json"))
    p.add_argument("--route-share", type=float, default=0.10)
    p.add_argument("--min-gain", type=float, default=0.0)
    p.add_argument("--l2", type=float, default=L2)
    p.set_defaults(func=cmd_fit)
    p = sub.add_parser("route")
    p.add_argument("--rows", required=True)
    p.add_argument("--c1", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--model", default=None)
    p.set_defaults(func=cmd_route)
    a = ap.parse_args(argv)
    a.func(a)


if __name__ == "__main__":
    main()
