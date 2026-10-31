"""Reviewer R2 for F5 (gen3_lead_score): blind-solve record, shortcut hunt and the final gate table (SPEC 8.4, 8.5).

Read-only on the family's rows. Nothing here labels a row: the gold comes from the generator's decide(), the second
opinion from D's decide2 (golden_src/gen3/v3_lead_score.py), and the blind answers from R2 reading rendered rows.

  blind_compare(answers, rows)     R2's blind answers (rid -> answer) against the stored gold
  shortcut_hunt(train, dev)        every cheap feature that could predict the gold on its own (SPEC 8.4):
                                   metadata strata, length / event counts, recorded numbers on judge rows, the best
                                   single word n-gram (chosen on one half of the latents, scored on the other), the
                                   attack plant's direction, the named shortcut solvers, and TF-IDF probes
  gate(...)                        the F5 gate table (counts, decide2 agreement, blind solve, shortcuts, tests)

Run from lean/:  ../.venv/bin/python yn2b/r2_lead_score_review.py --shortcuts | --gate [--write]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

YN2B = Path(__file__).resolve().parent
LEAN = YN2B.parent
GEN3 = LEAN / "golden_src" / "gen3"
for _p in (str(GEN3), str(LEAN), str(YN2B)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
sys.dont_write_bytecode = True

KEY = "gen3_lead_score"
RAW = LEAN / "data" / "v14_parts" / "yn2b_raw"
CAP = 0.60           # SPEC 4.7 / 8.4: no single shortcut above 60%
BLIND_FILE = YN2B / "r2_lead_score_blind.json"
GATE_FILE = YN2B / "r2_lead_score_gate.json"


# ------------------------------------------------------------------------------------------------ io
def sha256(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load(part: str) -> list[dict]:
    p = RAW / (f"{KEY}.jsonl" if part == "train" else f"dev/{KEY}.jsonl")
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]


def load_rels(part: str) -> list[dict]:
    p = RAW / ("relations" if part == "train" else "dev/relations") / f"{KEY}.jsonl"
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]


# ------------------------------------------------------------------------------------------------ blind solve
def blind_compare(answers: dict, rows: list[dict]) -> dict:
    """answers: rid -> R2's answer (option text, or yes/no). Rows missing from `rows` are reported as stale."""
    by = {r["rid"]: r for r in rows}
    out = {"n": 0, "agree": 0, "misses": [], "stale": []}
    parts = defaultdict(lambda: [0, 0])
    for rid, a in answers.items():
        r = by.get(rid)
        if r is None:
            out["stale"].append(rid)
            continue
        ok = a == r["gold"]
        out["n"] += 1
        out["agree"] += ok
        part = "dev_" + r["meta"]["dev_kind"] if r["meta"]["dev_kind"] else "train"
        parts[part][0] += ok
        parts[part][1] += 1
        if not ok:
            out["misses"].append({"rid": rid, "r2": a, "gold": r["gold"], "view": r["meta"]["view"],
                                  "qkind": r["meta"]["qkind"]})
    out["acc"] = round(out["agree"] / max(1, out["n"]), 4)
    out["by_part"] = {k: {"agree": v[0], "n": v[1]} for k, v in sorted(parts.items())}
    return out


# ------------------------------------------------------------------------------------------------ targets, features
def arch_of(r: dict) -> str:
    s = r["state"]
    if "Weighted total:" in s:
        return "weighted"
    if "gates are checked in order" in s:
        return "gated"
    if "Levels by the number of criteria met" in s:
        return "bant"
    return "points"


def target(r: dict):
    """yes/no rows and JB rows: 1 = yes (JB: the gold is the yes-description, options[0]); score rows: level index."""
    q = r["meta"]["qkind"]
    if q == "yn":
        return int(r["gold"] == "yes")
    if q == "jb":
        return int(r["gold"] == r["options"][0])
    return r["options"].index(r["gold"])


def group_of(r: dict) -> str:
    return "score" if r["meta"]["qkind"] == "score" else "yesno"   # yes/no + JB: the same binary target


def _crm(state: str, key: str):
    m = re.search(re.escape(key) + r"[\"']?\s*[:,|=]\s*\"?([^\"\n|]+?)\"?\s*(?:\||,?\n|$)", state)
    if not m:
        m = re.search(re.escape(key) + r"[^\n]*?Value: ([^\n]+)", state)
    return m.group(1).strip().rstrip(".") if m else None


def cat_features(r: dict) -> dict:
    m = r["meta"]
    s = r["state"]
    f = {k: str(m.get(k)) for k in ("fmt", "tpl", "pack", "tier", "len_bin", "card_style", "view", "plant_dir",
                                    "plant_channel", "n_shortcut_wrong", "levels", "judge", "dev_kind")}
    f["arch"] = arch_of(r)
    f["K"] = str(len(r["options"])) if m["qkind"] == "score" else "-"
    f["opts"] = "|".join(r["options"]) if m["qkind"] == "jb" else "-"
    f["has_record"] = str("Recorded score" in s)
    f["amendment"] = str(bool(re.search(r"Amendment \d+, effective", s)))
    f["override"] = str("Override, applied after" in s)
    f["customer_yes"] = str(bool(re.search(r"Current customer\W+yes", s)))
    f["unsub_rule"] = str("Unsubscribes:" in s)
    f["rep_exception"] = str("except that a rep note" in s or "with one exception" in s)
    f["reported_speech"] = str(bool(re.search(r"\bMy [A-Za-z ]+? (?:says|wants this live by)", s)))
    f["decoy_budget_note"] = str("Call notes: the prospect has" in s)
    f["lookalike_email"] = str(bool(re.search(r"@[a-z]+-[a-z]+\.(?:example|test)", s)))
    return f


def num_features(r: dict) -> dict:
    s = r["state"]
    out = {"len": len(s), "n_events": r["meta"].get("n_events") or 0, "n_lines": s.count("\n"),
           "n_msgs": len(re.findall(r"(?:\] |\| |wrote: \"|Subject: )", s)), "n_calls": s.count("Call notes"),
           "n_digits": len(re.findall(r"\d", s))}
    mm = re.search(r"(-?\d+) (?:points|weighted points|of \d+ (?:criteria met|gates passed))", r["instructions"])
    if mm:
        out["rec_score"] = int(mm.group(1))
    return out


def judge_features(r: dict) -> dict:
    """Recorded-number cues on judge rows (read with decide2's rubric parser, never with gold): the recorded level's
    position, whether it is the lowest level, whether the recorded level is the one the recorded score maps to (points,
    weighted, bant), whether the reason's parts add up to the recorded total and whether its met/passed count equals
    the recorded count."""
    import v3_lead_score as v3
    s = r["state"]
    try:
        doc = v3.parse_state(s)
        R = v3.parse_rubric(doc.title, doc.rules, doc.scoring_date)
    except v3.ParseError:
        return {}
    rec_s, rec_l, reason = doc.crm.get("Recorded score"), doc.crm.get("Recorded level"), doc.crm.get("Score reason")
    if rec_l is None or rec_l not in R.levels:
        return {}
    out = {"rec_level_index": str(R.levels.index(rec_l)), "rec_level_lowest": str(rec_l == R.levels[0])}
    ms = re.match(r"(-?\d+)", rec_s or "")
    n = int(ms.group(1)) if ms else None
    if n is not None and R.archetype in ("points", "weighted") and R.level_bands:
        band = next((i for i, (lo, hi) in enumerate(R.level_bands) if n >= lo and (hi is None or n <= hi)), None)
        out["rec_level_is_score_band"] = str(band == R.levels.index(rec_l))
    if n is not None and R.archetype == "bant" and n in R.count_levels:
        out["rec_level_is_score_band"] = str(R.count_levels[n] == R.levels.index(rec_l))
    nums = [int(x) for x in re.findall(r"[a-z]+ (-?\d+)", reason or "")]
    if n is not None and nums and R.archetype == "points":
        out["reason_sums_to_score"] = str(sum(nums) == n)
    mets = re.findall(r"\b(met|not met|passed|failed)\b", reason or "")
    if n is not None and mets and R.archetype in ("bant", "gated"):
        out["reason_counts_score"] = str(sum(x in ("met", "passed") for x in mets) == n)
    return out


# ------------------------------------------------------------------------------------------------ single-feature probes
def _halves(rows):
    """Two halves by latent (twins never straddle), deterministic."""
    a, b = [], []
    for r in rows:
        h = int(hashlib.sha256(r["meta"]["latent_id"].encode()).hexdigest(), 16)
        (a if h % 2 else b).append(r)
    return a, b


def _fit_cat(xs, ys):
    by = defaultdict(Counter)
    for x, y in zip(xs, ys):
        by[x][y] += 1
    glob = Counter(ys).most_common(1)[0][0]
    return {x: c.most_common(1)[0][0] for x, c in by.items()}, glob


def _acc(pred, ys):
    return sum(p == y for p, y in zip(pred, ys)) / max(1, len(ys))


def cat_probe(train, test, feat) -> dict:
    """Accuracy of 'predict the majority gold of this feature value' (fit on train, scored on test and in-sample)."""
    xs = [feat(r) for r in train]
    ys = [target(r) for r in train]
    tab, glob = _fit_cat(xs, ys)
    xt = [feat(r) for r in test]
    yt = [target(r) for r in test]
    return {"in_sample": round(_acc([tab[x] for x in xs], ys), 4),
            "held_out": round(_acc([tab.get(x, glob) for x in xt], yt), 4) if test else None,
            "values": len(tab)}


def _best_threshold(xs, ys):
    """The best single cut (x >= t -> class a else b) for a binary target."""
    pts = sorted(set(xs))
    best = (0.0, None, None)
    for t in pts:
        for hi in (0, 1):
            pred = [hi if x >= t else 1 - hi for x in xs]
            a = _acc(pred, ys)
            if a > best[0]:
                best = (a, t, hi)
    return best


def num_probe(train, test, key) -> dict | None:
    tr = [(num_features(r).get(key), target(r)) for r in train]
    tr = [(x, y) for x, y in tr if x is not None]
    te = [(num_features(r).get(key), target(r)) for r in test]
    te = [(x, y) for x, y in te if x is not None]
    if len(tr) < 20 or len({y for _, y in tr}) != 2:
        return None
    a, t, hi = _best_threshold([x for x, _ in tr], [y for _, y in tr])
    held = _acc([hi if x >= t else 1 - hi for x, _ in te], [y for _, y in te]) if te else None
    return {"in_sample": round(a, 4), "held_out": None if held is None else round(held, 4), "cut": t, "n": len(tr)}


_TOK = re.compile(r"[a-z]+|\d+")


def ngrams(text: str, n_max: int = 3) -> set:
    w = _TOK.findall(text.lower())
    out = set()
    for n in range(1, n_max + 1):
        out |= {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}
    return out


def ngram_probe(rows, field: str = "state", min_df: float = 0.02, top: int = 8) -> dict:
    """The best single n-gram (presence -> majority gold), chosen on one latent half and scored on the other (both
    directions; no selection on the scored half). Also reports the in-sample maximum for transparency."""
    a, b = _halves(rows)
    res = {}
    for name, (fit, ev) in {"a->b": (a, b), "b->a": (b, a)}.items():
        docs = [ngrams(r[field] if field != "q+o" else r["instructions"] + " " + " ".join(r["options"]))
                for r in fit]
        ys = [target(r) for r in fit]
        df = Counter(g for d in docs for g in d)
        n = len(docs)
        cands = [g for g, c in df.items() if min_df * n <= c <= (1 - min_df) * n]
        scored = []
        for g_ in cands:
            xs = [g_ in d for d in docs]
            tab, glob = _fit_cat(xs, ys)
            scored.append((_acc([tab[x] for x in xs], ys), g_, tab, glob))
        scored.sort(key=lambda t: (-t[0], t[1]))
        best = scored[0] if scored else (0.0, None, {}, None)
        edocs = [ngrams(r[field] if field != "q+o" else r["instructions"] + " " + " ".join(r["options"]))
                 for r in ev]
        ey = [target(r) for r in ev]
        held = _acc([best[2].get(best[1] in d, best[3]) for d in edocs], ey) if best[1] else None
        res[name] = {"chosen": best[1], "fit_acc": round(best[0], 4), "held_out": None if held is None else
                     round(held, 4), "top_in_sample": [(round(s, 4), g_) for s, g_, _, _ in scored[:top]]}
    res["held_out_mean"] = round(sum(v["held_out"] or 0 for v in res.values() if isinstance(v, dict)) / 2, 4)
    return res


def tfidf_probe(train, test, field: str) -> dict | None:
    """SPEC 8.4 TF-IDF 1-2-gram logistic regression: fit on train rows, score on test rows."""
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
    except ImportError:          # pragma: no cover
        return None
    if len({target(r) for r in train}) < 2 or not test:
        return None

    def txt(r):
        return r["instructions"] if field == "question" else (r["state"] + "\n" + r["instructions"] if
                                                              field == "state+question" else r["state"])
    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=200000, sublinear_tf=True)
    X = vec.fit_transform([txt(r) for r in train])
    clf = LogisticRegression(max_iter=2000, C=1.0)
    clf.fit(X, [target(r) for r in train])
    pred = clf.predict(vec.transform([txt(r) for r in test]))
    yt = [target(r) for r in test]
    maj = Counter(target(r) for r in train).most_common(1)[0][0]
    return {"acc": round(_acc(list(pred), yt), 4), "majority": round(_acc([maj] * len(yt), yt), 4), "n_test": len(yt)}


def plant_probe(rows) -> dict:
    """Attack twins: 'answer what the plant says' accuracy (SPEC 4.8: 50/50 direction)."""
    at = [r for r in rows if r["meta"]["view"] == "attack"]
    fg = sum(r["meta"]["plant_dir"] == "for_gold" for r in at)
    return {"rows": len(at), "obey_plant_acc": round(fg / max(1, len(at)), 4)}


def solver_probe(rows) -> dict:
    acc = defaultdict(lambda: [0, 0])
    for r in rows:
        for k, v in (r["meta"].get("shortcut_hits") or {}).items():
            acc[k][0] += v
            acc[k][1] += 1
    return {k: {"acc": round(h / n, 4), "n": n} for k, (h, n) in sorted(acc.items())}


CAT_KEYS = ("fmt", "tpl", "pack", "tier", "len_bin", "card_style", "view", "plant_dir", "plant_channel",
            "n_shortcut_wrong", "levels", "judge", "arch", "K", "opts", "has_record", "amendment", "override",
            "customer_yes", "unsub_rule", "rep_exception", "reported_speech", "decoy_budget_note", "lookalike_email")
NUM_KEYS = ("len", "n_events", "n_lines", "n_msgs", "n_calls", "n_digits", "rec_score")


def shortcut_hunt(train: list[dict], dev: list[dict]) -> dict:
    out = {}
    for grp in ("yesno", "score"):
        tr = [r for r in train if group_of(r) == grp]
        dv = [r for r in dev if group_of(r) == grp]
        a, b = _halves(tr)
        maj = Counter(target(r) for r in tr).most_common(1)[0]
        g = {"rows_train": len(tr), "rows_dev": len(dv), "majority_train": round(maj[1] / len(tr), 4)}
        g["categorical"] = {}
        for k in CAT_KEYS:
            feat = (lambda r, k=k: cat_features(r)[k])
            g["categorical"][k] = {"train->dev": cat_probe(tr, dv, feat), "half->half": cat_probe(a, b, feat)}
        if grp == "yesno":
            g["numeric"] = {k: {"train->dev": num_probe(tr, dv, k), "half->half": num_probe(a, b, k)}
                            for k in NUM_KEYS}
            jr = [r for r in tr if r["meta"]["judge"]]
            jd = [r for r in dv if r["meta"]["judge"]]
            ja, jb = _halves(jr)
            keys = sorted({k for r in jr for k in judge_features(r)})
            g["judge_record_cues"] = {k: {"train->dev": cat_probe(jr, jd, lambda r, k=k: judge_features(r).get(k)),
                                          "half->half": cat_probe(ja, jb, lambda r, k=k: judge_features(r).get(k)),
                                          "n": sum(k in judge_features(r) for r in jr)} for k in keys}
        g["ngram_state"] = ngram_probe(tr, "state")
        g["ngram_question_options"] = ngram_probe(tr, "q+o")
        g["tfidf"] = {"state+question train->dev": tfidf_probe(tr, dv, "state+question"),
                      "question train->dev": tfidf_probe(tr, dv, "question"),
                      "state+question half->half": tfidf_probe(a, b, "state+question"),
                      "question half->half": tfidf_probe(a, b, "question")}
        out[grp] = g
    out["plants"] = {"train": plant_probe(train), "dev": plant_probe(dev)}
    out["solvers"] = {"train": solver_probe(train), "dev": solver_probe(dev)}
    out["flags"] = flags(out)
    return out


def flags(rep: dict) -> list:
    """Every probe whose held-out accuracy exceeds CAP (for score rows: exceeds CAP too; chance there is ~1/K)."""
    bad = []
    for grp in ("yesno", "score"):
        g = rep[grp]
        for k, v in g["categorical"].items():
            for how, x in v.items():
                if x.get("held_out") is not None and x["held_out"] > CAP:
                    bad.append((grp, "cat:" + k, how, x["held_out"]))
        for k, v in (g.get("numeric") or {}).items():
            for how, x in v.items():
                if x and x.get("held_out") is not None and x["held_out"] > CAP:
                    bad.append((grp, "num:" + k, how, x["held_out"]))
        for k, v in (g.get("judge_record_cues") or {}).items():
            for how, x in v.items():
                if isinstance(x, dict) and x.get("held_out") is not None and x["held_out"] > CAP:
                    bad.append((grp, "judge:" + k, how, x["held_out"]))
        for nm in ("ngram_state", "ngram_question_options"):
            if g[nm]["held_out_mean"] > CAP:
                bad.append((grp, nm, "half->half", g[nm]["held_out_mean"]))
        for k, x in g["tfidf"].items():
            lim = 0.55 if k.startswith("question") and grp == "yesno" else CAP
            if x and x["acc"] > lim:
                bad.append((grp, "tfidf:" + k, "", x["acc"]))
    for part, s in rep["solvers"].items():
        for k, x in s.items():
            if x["acc"] > CAP:
                bad.append(("solver", k, part, x["acc"]))
    for part, p in rep["plants"].items():
        if p["rows"] and abs(p["obey_plant_acc"] - 0.5) > 0.1:
            bad.append(("plants", "obey_plant", part, p["obey_plant_acc"]))
    return bad


# ------------------------------------------------------------------------------------------------ gate
def gate(blind: dict | None = None, tests: dict | None = None) -> dict:
    import mv_core as mv
    import v3_lead_score as v3
    tr, dv = load("train"), load("dev")
    rels_tr, rels_dv = load_rels("train"), load_rels("dev")
    out = {"inputs": {"train": {"rows": len(tr), "sha256": sha256(RAW / f"{KEY}.jsonl")},
                      "dev": {"rows": len(dv), "sha256": sha256(RAW / "dev" / f"{KEY}.jsonl")}}}
    c = lambda rows, f: dict(sorted(Counter(f(r) for r in rows).items()))  # noqa: E731
    out["counts"] = {p: {"rows": len(rows), "by_qkind": c(rows, lambda r: r["meta"]["qkind"]),
                         "by_view": c(rows, lambda r: r["meta"]["view"]),
                         "by_dev_kind": c(rows, lambda r: str(r["meta"]["dev_kind"])),
                         "yes_share_yn": round(sum(r["gold"] == "yes" for r in rows if r["meta"]["qkind"] == "yn")
                                               / max(1, sum(r["meta"]["qkind"] == "yn" for r in rows)), 4)}
                     for p, rows in (("train", tr), ("dev", dv))}
    ag = {}
    for p, rows, rels in (("train", tr, rels_tr), ("dev", dv, rels_dv)):
        a = v3.agreement(rows)
        st = v3.structure_under_decide2(rows, rels, a["answers"])
        vl = mv.verify_labels(rows, v3.decide2_row_safe)
        ag[p] = {"rows": a["rows"], "agree": a["agree"], "disagree": len(a["disagreements"]),
                 "examples": a["disagreements"][:5], "verify_labels_ok": vl["ok"],
                 "structure": {k: (len(v) if isinstance(v, list) else v) for k, v in st.items()}}
    out["decide2"] = ag
    out["mv_core_checks"] = {p: {k: v.get("ok") for k, v in mv.run_checks(rows, rels).items() if isinstance(v, dict)}
                             for p, rows, rels in (("train", tr, rels_tr), ("dev", dv, rels_dv))}
    out["self_check"] = {}
    try:
        import gen3_lead_score as g
        out["self_check"] = {p: g.self_check_all(rows)["ok"] for p, rows in (("train", tr), ("dev", dv))}
    except Exception as e:          # pragma: no cover
        out["self_check"] = {"error": repr(e)}
    out["readings"] = reading_sensitivity(tr + dv)
    out["shortcuts"] = shortcut_hunt(tr, dv)
    out["blind"] = blind
    out["tests"] = tests
    return out


READINGS = ({"gate_score": "consecutive"}, {"disq_zero_score": True}, {"judge_reason": True},
            {"unsub_before_cap": True}, {"any_budget_counts": True}, {"any_target_counts": True},
            {"any_problem_counts": True})


def reading_sensitivity(rows: list[dict]) -> dict:
    """How many golds change under each alternative reading decide2 knows (0 = the item never depends on it)."""
    import v3_lead_score as v3
    base = {r["rid"]: v3.decide2_row(r) for r in rows}
    out = {}
    for rd in READINGS:
        k = ",".join(f"{a}={b}" for a, b in rd.items())
        try:
            ch = [r["rid"] for r in rows if v3.decide2_row(r, rd) != base[r["rid"]]]
        except KeyError:
            out[k] = None
            continue
        out[k] = {"changed": len(ch), "examples": ch[:8]}
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--shortcuts", action="store_true")
    ap.add_argument("--gate", action="store_true")
    ap.add_argument("--write", action="store_true", help="write the gate JSON and a MANIFEST record")
    a = ap.parse_args(argv)
    if a.shortcuts:
        rep = shortcut_hunt(load("train"), load("dev"))
        print(json.dumps(rep, indent=1, default=str)[:20000])
    if a.gate:
        blind = json.loads(BLIND_FILE.read_text()) if BLIND_FILE.exists() else None
        rep = gate(blind)
        txt = json.dumps(rep, indent=1, default=str)
        print(txt[:6000])
        if a.write:
            GATE_FILE.write_text(txt + "\n")
            import mv_core as mv
            mv.manifest_append({"tool": "yn2b/r2_lead_score_review.py", "key": KEY, "part": "r2_gate",
                                "path": str(GATE_FILE.relative_to(LEAN)), "rows": rep["counts"]["train"]["rows"]
                                + rep["counts"]["dev"]["rows"], "sha256": sha256(GATE_FILE),
                                "inputs": rep["inputs"]})


if __name__ == "__main__":
    main()
