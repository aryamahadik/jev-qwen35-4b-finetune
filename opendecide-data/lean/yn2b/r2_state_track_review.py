"""Reviewer R2 for F3 (gen3_state_track): blind-solve record, shortcut hunt and the F3 gate (SPEC 8.1, 8.4, 8.5).

Read-only on the family's rows. Nothing here labels a row: the gold comes from the generator's decide() (through the
fixed machines in gen3_state_track.MACH), the second opinion from builder B's decide2 (golden_src/gen3/
v3_state_track.py), and the blind answers from R2 reading rendered rows only (state, question, options, card).

  blind_compare(answers, rows)   R2's blind answers (rid -> option text) against the stored gold
  shortcut_hunt(train, dev)      every cheap feature that could predict the gold on its own (SPEC 4.7, 8.4): metadata
                                 strata, lengths and counts, question cue words, option position / length / numeric
                                 rank and "value named in the last event" heuristics for choice rows, the best single
                                 n-gram (chosen on one latent half, scored on the other), the attack plant's
                                 direction, the generator's named shortcut solvers, and the TF-IDF probes
  decide2_check(rows, rels)      decide2 agreement plus the structure rules under decide2 (contrast twins flip, equiv
                                 keeps, complement inverts, attack keeps)
  gate(...)                      the F3 gate table

Run from lean/:
  PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python yn2b/r2_state_track_review.py --gate [--write]
  (--train/--dev point the review at other row files, e.g. a scratch build; --write only with the default paths)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

YN2B = Path(__file__).resolve().parent
LEAN = YN2B.parent
GEN3 = LEAN / "golden_src" / "gen3"
for _p in (str(GEN3), str(LEAN), str(YN2B)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
sys.dont_write_bytecode = True

KEY = "gen3_state_track"
RAW = LEAN / "data" / "v14_parts" / "yn2b_raw"
TRAIN_PATH = RAW / f"{KEY}.jsonl"
DEV_PATH = RAW / "dev" / f"{KEY}.jsonl"
REL_PATHS = {"train": RAW / "relations" / f"{KEY}.jsonl", "dev": RAW / "dev" / "relations" / f"{KEY}.jsonl"}
CAP = 0.60           # SPEC 4.7 / 8.4: no single shortcut above 60% (question-only TF-IDF: 55%)
BLIND_FILE = YN2B / "r2_state_track_blind.json"
GATE_FILE = YN2B / "r2_state_track_gate.json"
MANIFEST = GEN3 / "MANIFEST_yn2b.jsonl"


# ------------------------------------------------------------------------------------------------ io
def sha256(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def read_jsonl(p: Path) -> list[dict]:
    return [json.loads(x) for x in Path(p).read_text().splitlines() if x.strip()]


# ------------------------------------------------------------------------------------------------ blind solve
def blind_compare(answers: dict, rows: list[dict]) -> dict:
    """answers: rid -> R2's blind answer (an option text). Rids missing from `rows` are reported as stale."""
    by = {r["rid"]: r for r in rows}
    out = {"n": 0, "agree": 0, "misses": [], "stale": [], "by_part": {}}
    parts = defaultdict(lambda: [0, 0])
    for rid, a in sorted(answers.items()):
        r = by.get(rid)
        if r is None:
            out["stale"].append(rid)
            continue
        if a not in r["options"]:
            raise ValueError(f"{rid}: blind answer {a!r} is not an option")
        p = "dev_" + r["meta"]["dev_kind"] if r["meta"].get("dev_kind") else "train"
        ok = a == r["gold"]
        out["n"] += 1
        out["agree"] += ok
        parts[p][0] += ok
        parts[p][1] += 1
        if not ok:
            out["misses"].append({"rid": rid, "blind": a, "gold": r["gold"], "pack": r["meta"]["pack"]})
    out["rate"] = round(out["agree"] / max(1, out["n"]), 4)
    out["by_part"] = {p: {"agree": a, "n": n} for p, (a, n) in sorted(parts.items())}
    return out


# ------------------------------------------------------------------------------------------------ features
def group_of(r: dict) -> str:
    q = r["meta"]["qkind"]
    return "binary" if q in ("yn", "jb") else q


def target(r: dict):
    """binary: yes / no (a JB row's first option is the yes statement); choice and score: the gold option's position."""
    if group_of(r) == "binary":
        return "yes" if (r["gold"] == "yes" or (r["meta"]["qkind"] == "jb" and r["gold"] == r["options"][0])) \
            else "no"
    return str(r["options"].index(r["gold"]))


_NEG = ("other than", "fewer than", "not ", "still", "unable", " off ", "unapproved", "anything other", "missed",
        "someone other", "within its sla", "no longer")


def cat_features(r: dict) -> dict:
    m = r["meta"]
    q = r["instructions"].lower()
    f = {k: str(m.get(k)) for k in ("fmt", "tpl", "renderer", "pack", "tier", "len_bin", "card_style", "view",
                                     "plant_dir", "polarity", "judge", "n_shortcut_wrong", "none_option", "levels")}
    f["K"] = str(len(r["options"]))
    f["at_end"] = str("at the end" in q)
    f["neg_cue"] = str(any(w in q for w in _NEG))
    f["has_record"] = str("agent record" in r["state"].lower() or '"agent_record": {' in r["state"])
    f["jb_fallback"] = str(r["options"] == ["yes, this holds", "no, this does not hold"])
    for t in (m.get("edge") or "").split(","):
        if t:
            f["edge:" + t] = "1"
    return f


EDGE_KEYS = ("edge:hc:revert", "edge:hc:expiry", "edge:hc:decoy_id", "edge:hc:resend_once", "edge:hc:guard_fail_noop",
             "edge:hc:display_order", "edge:hc:tz_window", "edge:temporal", "edge:multi_hop", "edge:numeric",
             "edge:hc:partial_batch", "edge:hc:boundary_exact", "edge:hc:business_days")
_NUM = re.compile(r"(?<![\d:.-])\d[\d,]*(?:\.\d+)?(?![\d:])")


def num_features(r: dict) -> dict:
    s, q = r["state"], r["instructions"]
    ids = re.findall(r"\b(?:SO|TCK|RES|SKU|DESK|ACC|BK|FF|DOC)-\d+\b", q)
    tid = ids[0] if ids else None
    q_nums = [float(x.replace(",", "")) for x in _NUM.findall(re.sub(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", "", q))
              if not re.fullmatch(r"\d{4}", x)]
    return {"len": len(s), "len_q": len(q), "n_events": r["meta"].get("n_events") or 0,
            "n_rules": len(re.findall(r"\bR\d+\.? \(in force from", s)),
            "target_mentions": s.count(tid) if tid else 0,
            "q_number": q_nums[0] if q_nums else None,
            "n_lines": s.count("\n") + 1}


def _halves(rows):
    """Two halves by latent (all views of a latent stay together), deterministic."""
    a, b = [], []
    for r in rows:
        h = int(hashlib.sha256(r["meta"]["latent_id"].encode()).hexdigest(), 16)
        (a if h % 2 else b).append(r)
    return a, b


def _acc(pred, ys):
    return sum(p == y for p, y in zip(pred, ys)) / max(1, len(ys))


def _fit_cat(xs, ys):
    by = defaultdict(Counter)
    for x, y in zip(xs, ys):
        by[x][y] += 1
    glob = Counter(ys).most_common(1)[0][0]
    return {x: c.most_common(1)[0][0] for x, c in by.items()}, glob


def cat_probe(train, test, feat) -> dict:
    """'Predict the majority gold of this feature value': fit on train, scored in-sample and on test."""
    xs, ys = [feat(r) for r in train], [target(r) for r in train]
    if not ys:
        return {"in_sample": None, "held_out": None, "values": 0}
    tab, glob = _fit_cat(xs, ys)
    xt, yt = [feat(r) for r in test], [target(r) for r in test]
    return {"in_sample": round(_acc([tab[x] for x in xs], ys), 4),
            "held_out": round(_acc([tab.get(x, glob) for x in xt], yt), 4) if test else None, "values": len(tab)}


def _best_cut(xs, ys):
    pts = sorted(set(xs))
    labs = sorted(set(ys))
    best = (0.0, None, None, None)
    for t in pts:
        for hi in labs:
            for lo in labs:
                if hi == lo:
                    continue
                a = _acc([hi if x >= t else lo for x in xs], ys)
                if a > best[0]:
                    best = (a, t, hi, lo)
    return best


def num_probe(train, test, key) -> dict | None:
    tr = [(num_features(r).get(key), target(r)) for r in train]
    tr = [(x, y) for x, y in tr if x is not None]
    te = [(num_features(r).get(key), target(r)) for r in test]
    te = [(x, y) for x, y in te if x is not None]
    if len(tr) < 20 or len({y for _, y in tr}) != 2:
        return None
    a, t, hi, lo = _best_cut([x for x, _ in tr], [y for _, y in tr])
    held = _acc([hi if x >= t else lo for x, _ in te], [y for _, y in te]) if te else None
    return {"in_sample": round(a, 4), "held_out": None if held is None else round(held, 4), "cut": t, "n": len(tr)}


_TOK = re.compile(r"[a-z]+|\d+")


def ngrams(text: str, n_max: int = 3) -> set:
    w = _TOK.findall(text.lower())
    out = set()
    for n in range(1, n_max + 1):
        out |= {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}
    return out


def _text(r, field):
    return r["state"] if field == "state" else r["instructions"] + " || " + " | ".join(r["options"])


def ngram_probe(rows, field: str = "state", min_df: float = 0.02, top: int = 6) -> dict:
    """The best single n-gram (presence -> majority gold), chosen on one latent half and scored on the other (both
    directions; no selection on the scored half)."""
    a, b = _halves(rows)
    res = {}
    for name, (fit, ev) in {"a->b": (a, b), "b->a": (b, a)}.items():
        docs = [ngrams(_text(r, field)) for r in fit]
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
        edocs = [ngrams(_text(r, field)) for r in ev]
        ey = [target(r) for r in ev]
        held = _acc([best[2].get(best[1] in d, best[3]) for d in edocs], ey) if best[1] else None
        res[name] = {"chosen": best[1], "fit_acc": round(best[0], 4),
                     "held_out": None if held is None else round(held, 4),
                     "top_in_sample": [(round(s, 4), g_) for s, g_, _, _ in scored[:top]]}
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
        return r["instructions"] if field == "question" else r["state"] + "\n" + r["instructions"]
    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=200000, sublinear_tf=True)
    X = vec.fit_transform([txt(r) for r in train])
    clf = LogisticRegression(max_iter=3000, C=1.0)
    clf.fit(X, [target(r) for r in train])
    pred = clf.predict(vec.transform([txt(r) for r in test]))
    yt = [target(r) for r in test]
    maj = Counter(target(r) for r in train).most_common(1)[0][0]
    return {"acc": round(_acc(list(pred), yt), 4), "majority": round(_acc([maj] * len(yt), yt), 4), "n_test": len(yt)}


def plant_probe(rows) -> dict:
    """Attack twins: accuracy of 'answer what the plant says' (SPEC 4.8: half the plants argue for gold)."""
    at = [r for r in rows if r["meta"]["view"] == "attack"]
    fg = sum(r["meta"]["plant_dir"] == "for_gold" for r in at)
    return {"rows": len(at), "obey_plant_acc": round(fg / max(1, len(at)), 4),
            "by_tpl": dict(Counter(f"{r['meta']['plant_tpl']}:{r['meta']['plant_dir']}" for r in at))}


def solver_probe(rows) -> dict:
    """The generator's named shortcut solvers (meta.shortcut_hits: 1 = the solver gives gold; absent = its trap is
    not in the row, it abstains)."""
    acc = defaultdict(lambda: [0, 0])
    for r in rows:
        for k, v in (r["meta"].get("shortcut_hits") or {}).items():
            acc[k][0] += v
            acc[k][1] += 1
    return {k: {"acc": round(h / n, 4), "n": n} for k, (h, n) in sorted(acc.items())}


# ---- choice rows: option heuristics (text only)
_AMT = re.compile(r"-?[\d,]+(?:\.\d+)?")


def _opt_num(o: str):
    m = _AMT.search(o)
    if not m or re.search(r"[A-Za-z]{3,}", o.replace("units", "").replace("unit", "").replace("versions", "")
                          .replace("version", "")[:m.start()]):
        return None
    try:
        return float(m.group(0).replace(",", ""))
    except ValueError:
        return None


def _events(r):
    """Parsed events (time, position, text) via decide2's renderer parser (parsing only; decide2 labels nothing
    here). None when the row does not parse."""
    try:
        import v3_state_track as v3
        s = v3.Solver(r)
        return s.doc
    except Exception:
        return None


def choice_heuristics(rows) -> dict:
    """Accuracy of text-only guessers on choice rows (mirror rows' 'None of these' counts as an option). Each
    guesser answers only when it can; its coverage is reported."""
    names = ("first", "last", "longest", "shortest", "num_max", "num_min", "num_median", "most_frequent_in_state",
             "in_last_listed_event", "in_last_timed_event", "starting_value", "nobody_or_none")
    hit, cov = Counter(), Counter()
    for r in rows:
        o, gold = r["options"], r["gold"]
        guess = {"first": o[0], "last": o[-1], "longest": max(o, key=len), "shortest": min(o, key=len)}
        nums = [(_opt_num(x), x) for x in o]
        if all(v is not None for v, _ in nums):
            srt = sorted(nums)
            guess.update(num_max=srt[-1][1], num_min=srt[0][1], num_median=srt[len(srt) // 2][1])
        cnt = {x: r["state"].count(x) for x in o if x != "None of these"}
        if cnt and max(cnt.values()) > 0:
            guess["most_frequent_in_state"] = max(cnt, key=lambda x: (cnt[x], -o.index(x)))
        guess["nobody_or_none"] = next((x for x in o if x in ("nobody", "None of these", "no access")), None)
        doc = _events(r)
        if doc is not None:
            lst = sorted(doc.events, key=lambda e: e.pos)
            tim = sorted(doc.events, key=lambda e: e.t)
            for nm, seq in (("in_last_listed_event", lst), ("in_last_timed_event", tim)):
                for e in reversed(seq):
                    m = [x for x in o if x != "None of these" and x in e.text]
                    if len(m) == 1:
                        guess[nm] = m[0]
                        break
            for _, f in doc.entities:
                m = [x for x in o if x in f.values()]
                if len(m) == 1:
                    guess["starting_value"] = m[0]
                    break
        for k in names:
            if guess.get(k) is not None:
                cov[k] += 1
                hit[k] += guess[k] == gold
    n = len(rows)
    return {k: {"acc": round(hit[k] / cov[k], 4) if cov[k] else None, "coverage": round(cov[k] / max(1, n), 4),
                "acc_over_all": round(hit[k] / max(1, n), 4)} for k in names}


CAT_KEYS = ("fmt", "tpl", "renderer", "pack", "tier", "len_bin", "card_style", "view", "plant_dir", "polarity",
            "judge", "n_shortcut_wrong", "none_option", "levels", "K", "at_end", "neg_cue", "has_record",
            "jb_fallback") + EDGE_KEYS
NUM_KEYS = ("len", "len_q", "n_events", "n_rules", "target_mentions", "q_number", "n_lines")


def shortcut_hunt(train: list[dict], dev: list[dict]) -> dict:
    out = {}
    for grp in ("binary", "choice", "score"):
        tr = [r for r in train if group_of(r) == grp]
        dv = [r for r in dev if group_of(r) == grp]
        a, b = _halves(tr)
        maj = Counter(target(r) for r in tr).most_common(1)[0]
        g = {"rows_train": len(tr), "rows_dev": len(dv), "majority_train": round(maj[1] / max(1, len(tr)), 4),
             "majority_class": maj[0],
             "target_share_train": dict(sorted(Counter(target(r) for r in tr).items())),
             "target_share_dev": dict(sorted(Counter(target(r) for r in dv).items()))}
        g["categorical"] = {}
        for k in CAT_KEYS:
            feat = (lambda r, k=k: cat_features(r).get(k, "0"))
            g["categorical"][k] = {"train->dev": cat_probe(tr, dv, feat), "half->half": cat_probe(a, b, feat)}
        if grp == "binary":
            g["numeric"] = {k: {"train->dev": num_probe(tr, dv, k), "half->half": num_probe(a, b, k)}
                            for k in NUM_KEYS}
            g["tfidf"] = {"state+question train->dev": tfidf_probe(tr, dv, "state+question"),
                          "question train->dev": tfidf_probe(tr, dv, "question"),
                          "state+question half->half": tfidf_probe(a, b, "state+question"),
                          "question half->half": tfidf_probe(a, b, "question")}
        else:
            g["option_heuristics_train"] = choice_heuristics(tr) if grp == "choice" else None
            g["option_heuristics_dev"] = choice_heuristics(dv) if grp == "choice" else None
        g["ngram_state"] = ngram_probe(tr, "state")
        g["ngram_question_options"] = ngram_probe(tr, "q+o")
        out[grp] = g
    out["plants"] = {"train": plant_probe(train), "dev": plant_probe(dev)}
    out["solvers"] = {"train": solver_probe(train), "dev": solver_probe(dev)}
    out["flags"] = flags(out)
    return out


def flags(rep: dict) -> list:
    """Every probe whose held-out accuracy exceeds CAP. For choice and score rows the bar is CAP too, although chance
    there is 1/K, so a flag means 'a single cue predicts the answer most of the time'."""
    bad = []
    for grp in ("binary", "choice", "score"):
        g = rep[grp]
        for k, v in g["categorical"].items():
            for how, x in v.items():
                if x.get("held_out") is not None and x["held_out"] > CAP:
                    bad.append((grp, "cat:" + k, how, x["held_out"]))
        for k, v in (g.get("numeric") or {}).items():
            for how, x in v.items():
                if x and x.get("held_out") is not None and x["held_out"] > CAP:
                    bad.append((grp, "num:" + k, how, x["held_out"]))
        for nm in ("ngram_state", "ngram_question_options"):
            if g[nm]["held_out_mean"] > CAP:
                bad.append((grp, nm, "half->half", g[nm]["held_out_mean"]))
        for k, x in (g.get("tfidf") or {}).items():
            lim = 0.55 if k.startswith("question") else CAP
            if x and x["acc"] > lim:
                bad.append((grp, "tfidf:" + k, "", x["acc"]))
        for part in ("train", "dev"):
            for k, x in (g.get(f"option_heuristics_{part}") or {}).items():
                if x["acc"] is not None and x["coverage"] >= 0.2 and x["acc"] > CAP:
                    bad.append((grp, "option:" + k, part, x["acc"]))
    for part, s in rep["solvers"].items():
        for k, x in s.items():
            if x["acc"] > CAP:
                bad.append(("solver", k, part, x["acc"]))
    for part, p in rep["plants"].items():
        if p["rows"] and abs(p["obey_plant_acc"] - 0.5) > 0.1:
            bad.append(("plants", "obey_plant", part, p["obey_plant_acc"]))
    return bad


# ------------------------------------------------------------------------------------------------ decide2
def decide2_check(rows: list[dict], rels: list[dict]) -> dict:
    """decide2 agreement, undecided rows, and the structure rules under decide2 (SPEC 8.3)."""
    import v3_state_track as v3
    ans, notes, mism, und = {}, Counter(), [], []
    for r in rows:
        ex = v3.explain_row(r)
        a = ex["answer"]
        ans[r["rid"]] = a
        for n in ex.get("notes", ()):
            notes[n] += 1
        if a is v3.UNDEFINED:
            und.append({"rid": r["rid"], "error": ex.get("error")})
        elif a != r["gold"]:
            mism.append({"rid": r["rid"], "gold": r["gold"], "decide2": a, "notes": ex.get("notes")})
    by = {r["rid"]: r for r in rows}

    def yes(rid):
        r = by[rid]
        a = ans[rid]
        return a == "yes" if r["options"] == ["yes", "no"] else a == r["options"][0]
    st = Counter()
    bad = []
    for x in rels:
        if x["a"] not in by or x["b"] not in by:
            continue
        t = x["type"]
        ok = (ans[x["a"]] == ans[x["b"]]) if t in ("equiv", "inv") else (yes(x["a"]) != yes(x["b"]))
        st[t + (":ok" if ok else ":bad")] += 1
        if not ok:
            bad.append(x)
    for r in rows:
        tw = r["meta"].get("twin_of")
        if r["meta"]["view"] == "contrast" and tw in by:
            ok = ans[r["rid"]] != ans[tw] and r["gold"] != by[tw]["gold"]
            st["contrast_flips:" + ("ok" if ok else "bad")] += 1
            if not ok:
                bad.append({"type": "contrast", "a": tw, "b": r["rid"]})
    return {"rows": len(rows), "agree": len(rows) - len(mism) - len(und), "disagree": len(mism),
            "undefined": len(und), "rate": round((len(rows) - len(mism) - len(und)) / max(1, len(rows)), 6),
            "mismatches": mism[:50], "undefined_rows": und[:50], "replay_notes": dict(sorted(notes.items())),
            "structure": dict(sorted(st.items())), "structure_violations": bad[:20]}


def readings(paths: dict) -> dict:
    """decide2's alternative readings: rows whose answer would change under the other reading. A reading the rules
    now state explicitly (the R2 rule sentences) is no longer open to the reader even when rows still depend on it;
    readings tied to surfaces the generator no longer emits must change 0 rows."""
    import v3_state_track as v3
    sens = v3.readings_sensitivity(paths)
    stated = {"clear_over_quarantine": "InventoryR2.CLEAR", "rehold_same_person": "BookingsR2.REHOLD",
              "revert_of_resolve": "TicketsR2.RES_REVERT", "same_as_before_excluded": "DialogueR2.SAME_EXCLUDED",
              "override_overlap": "FlagsR2.OVERLAP"}
    gone = ("restore_not_in_trash", "other_booking_self", "assistant_request", "customer_proposal")
    out = {}
    for k, v in sens.items():
        out[k] = {"primary": v["primary"], "alt": v["alt"], "rows_changed": v["rows_changed"],
                  "gold_follows": v["gold_follows"], "settled_by": stated.get(k) or ("not generated" if k in gone
                                                                                    else None),
                  "examples": [c["rid"] for c in v["rows"][:6]]}
    out["_ok"] = all(sens[k]["rows_changed"] == 0 for k in gone) and \
        all(sens[k]["gold_follows"] in (None, "primary") for k in stated)
    return out


# ------------------------------------------------------------------------------------------------ gate
def gate(paths: dict | None = None, blind: dict | None = None, tests: dict | None = None) -> dict:
    import mv_core as mv
    paths = paths or {"train": TRAIN_PATH, "dev": DEV_PATH}
    rel_paths = {p: Path(paths[p]).parent / "relations" / Path(paths[p]).name for p in paths}
    rows = {p: read_jsonl(paths[p]) for p in paths}
    rels = {p: read_jsonl(rel_paths[p]) if rel_paths[p].exists() else [] for p in paths}
    out = {"written": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "inputs": {p: {"path": str(Path(paths[p]).resolve().relative_to(LEAN)) if str(Path(paths[p]).resolve())
                          .startswith(str(LEAN)) else str(paths[p]), "rows": len(rows[p]), "sha256": sha256(paths[p])}
                      for p in paths},
           "tools": {"generator_sha256": sha256(GEN3 / "gen3_state_track.py"),
                     "sim_sha256": sha256(GEN3 / "gen3_state_track_sim.py"),
                     "decide2_sha256": sha256(GEN3 / "v3_state_track.py"),
                     "review_sha256": sha256(Path(__file__))}}
    c = lambda rs, f: dict(sorted(Counter(f(r) for r in rs).items()))  # noqa: E731
    out["counts"] = {p: {"rows": len(rs), "latents": len({r["meta"]["latent_id"] for r in rs}),
                         "by_qkind": c(rs, lambda r: r["meta"]["qkind"] + (":judge" if r["meta"]["judge"] else "")),
                         "by_view": c(rs, lambda r: r["meta"]["view"]), "by_pack": c(rs, lambda r: r["meta"]["pack"]),
                         "by_tier": c(rs, lambda r: r["meta"]["tier"]),
                         "by_dev_kind": c(rs, lambda r: str(r["meta"]["dev_kind"])),
                         "yes_share_yn": round(sum(r["gold"] == "yes" for r in rs if r["meta"]["qkind"] == "yn")
                                               / max(1, sum(r["meta"]["qkind"] == "yn" for r in rs)), 4),
                         "relations": c(rels[p], lambda x: x["type"])}
                     for p, rs in rows.items()}
    out["decide2"] = {p: decide2_check(rows[p], rels[p]) for p in rows}
    out["readings"] = readings(paths)
    out["mv_core_checks"] = {}
    for p in rows:
        chk = mv.run_checks(rows[p], rels[p])
        out["mv_core_checks"][p] = {k: v.get("ok") for k, v in chk.items() if isinstance(v, dict) and "ok" in v}
    out["shortcuts"] = shortcut_hunt(rows["train"], rows["dev"])
    out["blind"] = blind
    out["tests"] = tests
    out["verdict"] = verdict(out)
    return out


def verdict(g: dict) -> dict:
    why = []
    for p, d in g["decide2"].items():
        if d["disagree"] or d["undefined"]:
            why.append(f"decide2 {p}: {d['disagree']} disagree, {d['undefined']} undefined")
        if any(k.endswith(":bad") for k in d["structure"]):
            why.append(f"structure {p}: {d['structure']}")
    if not g["readings"].get("_ok"):
        why.append("readings: an ambiguous surface is still generated")
    for p, ch in g["mv_core_checks"].items():
        failed = [k for k, v in ch.items() if v is False and not (p == "dev" and k == "artefacts")]
        if failed:
            why.append(f"mv_core {p}: {failed}")
    if g["shortcuts"]["flags"]:
        why.append(f"shortcuts above {CAP}: {g['shortcuts']['flags'][:6]}")
    b = g.get("blind") or {}
    final = b.get("final") or {}
    if final and (final.get("rate", 0) < 0.97 or final.get("open_generator_bugs")):
        why.append(f"blind solve {final.get('rate')} with {final.get('open_generator_bugs')} open bugs")
    if not final:
        why.append("no blind solve on the final build")
    t = g.get("tests") or {}
    if t and t.get("failed"):
        why.append(f"tests failed: {t['failed']}")
    return {"green": not why, "reasons": why}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--gate", action="store_true")
    ap.add_argument("--shortcuts", action="store_true")
    ap.add_argument("--train", default=str(TRAIN_PATH))
    ap.add_argument("--dev", default=str(DEV_PATH))
    ap.add_argument("--tests", default=None, help="JSON {passed, failed, command} of the pytest run to record")
    ap.add_argument("--write", action="store_true", help="write the gate JSON and append MANIFEST records")
    ap.add_argument("--candidate", action="store_true",
                    help="with --write and non-default --train/--dev: record the gate of a candidate build that is not "
                         "yet in data/ (marked candidate; the files are identified by sha256)")
    a = ap.parse_args(argv)
    paths = {"train": Path(a.train), "dev": Path(a.dev)}
    if a.shortcuts:
        rep = shortcut_hunt(read_jsonl(paths["train"]), read_jsonl(paths["dev"]))
        print(json.dumps(rep, indent=1, default=str)[:20000])
        return 0
    blind = json.loads(BLIND_FILE.read_text()) if BLIND_FILE.exists() else None
    if blind:
        rows = read_jsonl(paths["train"]) + read_jsonl(paths["dev"])
        for rnd in blind.get("rounds", []):
            if rnd.get("build") == "final":
                rnd["recheck"] = blind_compare({x["rid"]: x["blind"] for x in rnd["items"]}, rows)
    tests = json.loads(a.tests) if a.tests else None
    g = gate(paths, blind, tests)
    default = paths == {"train": TRAIN_PATH, "dev": DEV_PATH}
    if not default:
        g["candidate"] = {"note": "gate of a candidate build outside data/; rerun --gate --write on the written rows "
                                  "(the build is deterministic, so the sha256 values must match)",
                          "written_rows_sha256": {p: sha256(q) if q.exists() else None
                                                  for p, q in (("train", TRAIN_PATH), ("dev", DEV_PATH))}}
    txt = json.dumps(g, indent=1, ensure_ascii=False, default=str)
    print(json.dumps({"decide2": {p: {k: v[k] for k in ("rows", "agree", "disagree", "undefined", "structure")}
                                  for p, v in g["decide2"].items()},
                      "readings": {k: (v["rows_changed"], v["gold_follows"], v["settled_by"]) if isinstance(v, dict)
                                   else v for k, v in g["readings"].items()},
                      "mv_core": g["mv_core_checks"], "shortcut_flags": g["shortcuts"]["flags"],
                      "verdict": g["verdict"]}, indent=1, default=str))
    if a.write:
        if not default and not a.candidate:
            print("--write needs the default row paths (or --candidate)", file=sys.stderr)
            return 2
        txt = json.dumps(g, indent=1, ensure_ascii=False, default=str)
        GATE_FILE.write_text(txt + "\n")
        part = "r2_gate" if default else "r2_gate_candidate"
        recs = [{"written": g["written"], "tool": "yn2b/r2_state_track_review.py", "key": KEY, "part": part,
                 "path": str(GATE_FILE.relative_to(LEAN)), "rows": sum(v["rows"] for v in g["inputs"].values()),
                 "sha256": sha256(GATE_FILE), "inputs": g["inputs"], "tools": g["tools"],
                 "green": g["verdict"]["green"]}]
        if BLIND_FILE.exists():
            recs.append({"written": g["written"], "tool": "yn2b/r2_state_track_review.py", "key": KEY,
                         "part": "r2_blind", "path": str(BLIND_FILE.relative_to(LEAN)), "sha256": sha256(BLIND_FILE),
                         "rows": sum(len(r["items"]) for r in blind.get("rounds", [])),
                         "inputs": {p: v["sha256"] for p, v in g["inputs"].items()}})
        with MANIFEST.open("a") as f:
            for rec in recs:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print("wrote", GATE_FILE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
