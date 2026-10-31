"""Reviewer R2 for F1 (gen3_rule_chain): blind-solve record, shortcut hunt, ambiguity hunt, coherence hunt and the F1
gate (SPEC 8.1, 8.3, 8.4, 8.5).

Read-only on the family's rows. Nothing here labels a row: the gold comes from the generator (rc_core / rc_numeric),
the second opinion from builder E's decide2 (golden_src/gen3/v3_rule_chain.py), and the blind answers from R2 reading
rendered rows only (state, card, question, options). decide2's parsers are used here only to READ the rendered text
(which outcome the question names, whether a document is missing, which flags are set); every probe compares a cheap
reader's answer with the stored gold.

  export_blind(seed, out_dir)    key-separated blind export (rows as the trainer prints them; the key file apart)
  blind_compare(answers, rows)   R2's blind answers (rid -> option text) against the stored gold
  shortcut_hunt(train, dev)      every cheap feature that could predict the gold on its own (SPEC 4.7, 8.4): metadata
                                 strata, the outcome the question names, surface cues of the case file (a missing
                                 document, a set exclusion flag, a recorded decision, an attack plant), cue readers,
                                 option position / length / kind heuristics for choice rows, amount-bin readers, F1b
                                 claim-shape cues, lengths and counts, the best single n-gram (chosen on one latent
                                 half, scored on the other), the TF-IDF probes, the generator's named solvers and
                                 decide2's mechanism-ablation solvers (abstaining where the ablation does not change
                                 the outcome)
  readings(rows_by_part)         decide2's alternative readings plus R2's own (outcome-label wording, the position of
                                 an amended limit under a 'placed later' precedence rule)
  coherence_hunt(rows)           facts that contradict each other (claim received before the fault / delivery /
                                 prescription / enrolment it is about, zero-valued eligibility quantities)
  decide2_check(rows, rels)      decide2 agreement plus the structure rules under decide2
  gate(...)                      the F1 gate table

Run from lean/:
  PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python yn2b/r2_rule_chain_review.py --gate [--write]
  PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python yn2b/r2_rule_chain_review.py --export SEED OUT_DIR   (blind export)
"""
from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import json
import random
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

YN2B = Path(__file__).resolve().parent
LEAN = YN2B.parent
GEN3 = LEAN / "golden_src" / "gen3"
for _p in (str(GEN3), str(LEAN), str(YN2B)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
sys.dont_write_bytecode = True

KEY = "gen3_rule_chain"
RAW = LEAN / "data" / "v14_parts" / "yn2b_raw"
TRAIN_PATH = RAW / f"{KEY}.jsonl"
DEV_PATH = RAW / "dev" / f"{KEY}.jsonl"
CAP = 0.60           # SPEC 4.7 / 8.4: no single shortcut above 60% (question-only TF-IDF: 55%)
MIN_COV = 0.10       # a reader is flagged when it answers at least this share of its group's rows
SMALL_LATENTS = 50   # a dev-only reader value from fewer latents than this is reported as small-sample when the
#                      same reader is at or below CAP on train (one latent's rows are views of one item)
BLIND_FILE = YN2B / "r2_rule_chain_blind.json"
GATE_FILE = YN2B / "r2_rule_chain_gate.json"
MANIFEST = GEN3 / "MANIFEST_yn2b.jsonl"
DEFS_DIR = None      # None: data/v14_parts/yn2b_defs; set_defs_dir() points the review at a scratch build
FALLBACK = ["yes, this holds", "no, this does not hold"]
NONE_OPTS = ("None of the clauses listed", "None of the outcomes listed")
GEN_FILES = ("gen3_rule_chain.py", "rc_core.py", "rc_render.py", "rc_skins.py", "rc_numeric.py", "rc_repair.py")
# outcome labels whose wording would not describe every exclusion they stand for (R2 ambiguity hunt): (skin, flag)
# -> (word in the exclusion outcome's label that misfits, why). The first build said 'refund refused - damage excluded
# from the warranty' (a clearance-stock exclusion is not damage) and 'not covered - use excluded by the formulary' (a
# vacation supply is not a use); rc_skins now says 'item excluded' / 'fill excluded', so this check finds 0 rows.
EXCL_LABEL_MISFIT = {("warranty_returns", "clearance"): (" damage ", "a clearance-stock exclusion is not 'damage'"),
                     ("pharmacy_formulary", "vacation"): (" use ", "a vacation supply is not a 'use'")}


# ------------------------------------------------------------------------------------------------ io
def sha256(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def read_jsonl(p: Path) -> list[dict]:
    return [json.loads(x) for x in Path(p).read_text().splitlines() if x.strip()]


def _v3():
    import v3_rule_chain as v3
    return v3


def _mv():
    import mv_core as mv
    return mv


def set_defs_dir(path) -> None:
    """Read cards from another defs dir (a scratch build), for this module and for decide2's F1b card reader."""
    global DEFS_DIR
    DEFS_DIR = Path(path) if path else None
    mv = _mv()
    _v3().set_card_lookup((lambda q: mv.load_defs(KEY, q, DEFS_DIR)) if DEFS_DIR else None)
    _CACHE.clear()


def load_defs(r: dict):
    return _mv().load_defs(r["key"], r["meta"].get("defs"), DEFS_DIR)


# ------------------------------------------------------------------------------------------------ blind solve
def printed(r: dict) -> str:
    """The row as the trainer prints it (decoder_io cygnet layout, text first): state, the yes/no card as
    'Definitions:', the question, the options (choice options with their card lines). No gold, no meta."""
    mv = _mv()
    g = mv.to_golden(r, load_defs(r))
    lines = [r["state"].rstrip(), ""]
    defs = {}
    if g["qtype"] == "noul":
        if g["card"]:
            lines += ["Definitions:", g["card"], ""]
        opts = ["yes", "no"]
    else:
        opts = g["options"]
        defs = mv.card_defs(g["card"])
    lines += [r["instructions"].rstrip(), "", "Options:"]
    lines += [f"  {i}. {o}" + (f": {defs[o]}" if o in defs else "") for i, o in enumerate(opts)]
    return "\n".join(lines)


def export_blind(seed: int, out_dir: Path, n_train: int = 60, n_dev: int = 40, paths: dict | None = None) -> dict:
    """60 random train + 40 random dev_holdout rows, shuffled, as blind_rows.txt (bid headers only) and key.json
    (bid -> rid, gold) in out_dir (scratch, never data/). R2 answers from blind_rows.txt before opening key.json."""
    paths = paths or {"train": TRAIN_PATH, "dev": DEV_PATH}
    tr, dv = read_jsonl(paths["train"]), read_jsonl(paths["dev"])
    dh = [r for r in dv if r["meta"].get("dev_kind") == "holdout"]
    rng = random.Random(seed)
    items = [("T%02d" % i, r) for i, r in enumerate(rng.sample(tr, n_train))] + \
            [("D%02d" % i, r) for i, r in enumerate(rng.sample(dh, n_dev))]
    rng.shuffle(items)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "blind_rows.txt").write_text("\n\n".join(f"=================== {b} ===================\n{printed(r)}"
                                                       for b, r in items) + "\n")
    key = {b: {"rid": r["rid"], "gold": r["gold"], "options": r["options"]} for b, r in items}
    (out_dir / "key.json").write_text(json.dumps(key, indent=1))
    return {"items": len(items), "train_sha256": sha256(paths["train"]), "dev_sha256": sha256(paths["dev"])}


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


# ------------------------------------------------------------------------------------------------ text reading
_CACHE: dict = {}
POS_FAMILIES = ("pos", "jdg", "jbf", "jbq")      # 'yes' / the first JB option = the named outcome holds


def is_f1b(r: dict) -> bool:
    return r["meta"]["pack"].startswith("nb_")


def read_f1a(r: dict) -> dict | None:
    """What a reader sees in an F1a row (parsed with decide2's text parsers; no labels): the document, the case, the
    question family, the outcome code the question (or the recorded decision) names, and surface cues."""
    if is_f1b(r):
        return None
    k = r["rid"] + "|" + hashlib.sha1(r["state"].encode()).hexdigest()[:8]
    if k in _CACHE:
        return _CACHE[k]
    v3 = _v3()
    try:
        sp, doc, case = v3.parse_f1a(r["state"])
        q, g = v3.classify_question(r["instructions"], doc.v)
    except Exception:          # noqa: BLE001  (decide2 undefined rows are reported by decide2_check)
        _CACHE[k] = None
        return None
    v = doc.v
    named = None
    if q in ("jdg", "jinv"):
        named = case.decision
    elif q == "jbq":
        m = re.search(r'"([^"]+)"', r["options"][0])
        named = m[1] if m else None
    elif isinstance(g, dict) and g.get("out"):
        named = g["out"]
    X = v.code_by_text.get(named) if named else None
    excl_flags = [f for f, x in v.flags.items() if x["role"] == "excl" and case.flags.get(f)]
    exc_flags = [f for f, x in v.flags.items() if x["role"] == "exc" and case.flags.get(f)]
    excexc_flags = [f for f, x in v.flags.items() if x["role"] == "excexc" and case.flags.get(f)]
    waiver_targets = {c.d.get("target") for c in doc.of("exc")}
    out = {"sp": sp, "doc": doc, "case": case, "q": q, "g": g, "X": X, "skin": v.key,
           "doc_missing": not case.docs, "excl_flags": excl_flags, "exc_flags": exc_flags,
           "excexc_flags": excexc_flags, "has_decision": case.decision is not None,
           "has_amend": bool(doc.of("amend", "amend_row")), "has_withdrawn": bool(doc.of("amend_w")),
           "business": doc.counting == "business", "n_holidays": len(doc.holidays),
           "n_exc": len(doc.of("exc", "pexc")), "has_pexc": bool(doc.of("pexc")),
           "has_exc_to_exc": any(t in {c.key for c in doc.of("exc", "pexc")} for t in waiver_targets),
           "prec": "+".join(doc.prec) or ("named" if doc.named_prec else "none"),
           "n_clauses": len(doc.clauses), "has_linked": "linked" in case.shown,
           "amount": float(case.amount.v) if case.amount is not None else None,
           "elig": float(case.elig.v) if case.elig is not None else None}
    _CACHE[k] = out
    return out


def solve(r: dict, readings: dict | None = None):
    v3 = _v3()
    try:
        return v3.solve(r, readings)
    except Exception:          # noqa: BLE001
        return None


# ------------------------------------------------------------------------------------------------ targets
def group_of(r: dict) -> str:
    return "binary" if r["meta"]["qkind"] in ("yn", "jb") else "choice"


def target(r: dict):
    """binary: yes / no (a JB row: its first option); choice: the gold option's position."""
    if group_of(r) == "binary":
        return "yes" if (r["gold"] == "yes" or (r["meta"]["qkind"] == "jb" and r["gold"] == r["options"][0])) \
            else "no"
    return str(r["options"].index(r["gold"]))


def holds_answer(r: dict, info: dict, holds: bool | None):
    """Map 'the named outcome holds' (True / False) to the row's option (yes/no, or a JB option)."""
    if holds is None or info is None or info["q"] is None:
        return None
    q = info["q"]
    if q in ("pos", "inv", "jdg", "jinv"):
        return "yes" if holds == (q in ("pos", "jdg")) else "no"
    if q in ("jbf", "jbq"):
        return r["options"][0] if holds else r["options"][1]
    return None


def cat_features(r: dict) -> dict:
    m = r["meta"]
    f = {k: str(m.get(k)) for k in ("fmt", "tpl", "renderer", "pack", "tier", "card_style", "view", "plant_dir",
                                     "polarity", "judge", "n_shortcut_wrong", "role", "len_bin", "plant_channel",
                                     "plant_tpl", "plant_spoof")}
    f["K"] = str(len(r["options"]))
    f["jb_fallback"] = str(r["options"] == FALLBACK)
    f["none_offered"] = str(any(o in NONE_OPTS for o in r["options"]))
    f["source"] = "F1b" if is_f1b(r) else "F1a"
    i = read_f1a(r)
    if i:
        f["q_family"] = str(i["q"])
        f["named_code"] = str(i["X"])
        f["named_code_x_tpl"] = f"{i['X']}|{m['tpl']}"
        f["skin_x_named"] = f"{i['skin']}|{i['X']}"
        f["doc_missing"] = str(i["doc_missing"])
        f["excl_flag"] = str(bool(i["excl_flags"]))
        f["exc_flag"] = str(bool(i["exc_flags"]))
        f["excexc_flag"] = str(bool(i["excexc_flags"]))
        f["has_decision"] = str(i["has_decision"])
        f["has_amend"] = str(i["has_amend"])
        f["has_withdrawn"] = str(i["has_withdrawn"])
        f["business"] = str(i["business"])
        f["has_exc_to_exc"] = str(i["has_exc_to_exc"])
        f["has_pexc"] = str(i["has_pexc"])
        f["prec"] = i["prec"]
        f["has_linked"] = str(i["has_linked"])
        f["named_x_doc_missing"] = f"{i['X']}|{i['doc_missing']}"
        f["named_x_excl_flag"] = f"{i['X']}|{bool(i['excl_flags'])}"
        f["style"] = str(i["doc"].style)
    if is_f1b(r):
        f.update(f1b_features(r))
    for t in (m.get("edge") or "").split(","):
        if t:
            f["edge:" + t] = "1"
    return f


# ------------------------------------------------------------------------------------------------ F1b cues
_OPS = ("rose by at least", "rose by at most", "rose by more than", "rose by less than", "fell by at least",
        "fell by at most", "fell by more than", "fell by less than", "at least", "at most", "more than", "less than",
        "about", "exactly")


def _claim_text(r: dict) -> str:
    s = r["state"]
    for rx in (r'"claim": "([^"]+)"', r"(?:^|\n)claim: (.+)", r"(?:^|\n)Claim: (.+)", r"\| claim \| (.+?) \|",
               r"(?:^|\n)## Claim\n+(.+)", r"The claim (?:is|reads|under check)[^:]*: (.+)"):
        m = re.search(rx, s)
        if m:
            return m.group(1)
    m = re.findall(r"[^.\n]*(?:more than|less than|at least|at most|about|exactly|rose by|fell by)[^.\n]*\.", s)
    return m[-1] if m else ""


def _nums(t: str) -> list:
    return [x.replace(",", "") for x in re.findall(r"\d[\d,]*(?:\.\d+)?", t)]


def f1b_features(r: dict) -> dict:
    c = _claim_text(r)
    op = next((o for o in _OPS if o in c), "other")
    cn = _nums(c)
    ev = r["state"].replace(c, "") if c else r["state"]
    en = _nums(ev)
    fig = cn[-1] if cn else None
    return {"nb_op": op, "nb_claim_fig_printed": str(fig in en if fig else None),
            "nb_claim_fig_is_last": str(bool(fig) and bool(en) and fig == en[-1]),
            "nb_revision": str("revised" in r["state"]), "nb_n_evidence": str(min(4, r["state"].count("As of ")))}


# ------------------------------------------------------------------------------------------------ numeric features
def num_features(r: dict) -> dict:
    s, q = r["state"], r["instructions"]
    out = {"len": len(s), "len_q": len(q), "n_lines": s.count("\n") + 1, "n_digits": len(re.findall(r"\d", s))}
    i = read_f1a(r)
    if i:
        out.update(n_clauses=i["n_clauses"], n_exc=i["n_exc"], n_holidays=i["n_holidays"],
                   n_excl_flags=len(i["excl_flags"]), n_exc_flags=len(i["exc_flags"]))
        if i["amount"] is not None:
            out["amount"] = i["amount"]
        if i["elig"] is not None:
            out["elig_value"] = i["elig"]
    return out


NUM_KEYS = ("len", "len_q", "n_lines", "n_digits", "n_clauses", "n_exc", "n_holidays", "n_excl_flags", "n_exc_flags",
            "amount", "elig_value")


# ------------------------------------------------------------------------------------------------ probes (generic)
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


def card_text(r: dict) -> str:
    d = load_defs(r) or {}
    return " ".join(f"{k}: {v}" for k, v in d.items())


def _text(r, field):
    if field == "state":
        return r["state"]
    if field == "card":
        return card_text(r)
    return r["instructions"] + " || " + " | ".join(r["options"])


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
    """SPEC 8.4 TF-IDF 1-2-gram logistic regression: fit on train rows, score on test rows. The yes/no card and the
    choice option lines are part of what the model reads, so 'state+question' includes them."""
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
    except ImportError:          # pragma: no cover
        return None
    if len({target(r) for r in train}) < 2 or not test:
        return None

    def txt(r):
        if field == "question":
            return r["instructions"]
        return r["state"] + "\n" + card_text(r) + "\n" + r["instructions"] + "\n" + " | ".join(r["options"])
    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=200000, sublinear_tf=True)
    X = vec.fit_transform([txt(r) for r in train])
    clf = LogisticRegression(max_iter=3000, C=1.0)
    clf.fit(X, [target(r) for r in train])
    pred = clf.predict(vec.transform([txt(r) for r in test]))
    yt = [target(r) for r in test]
    maj = Counter(target(r) for r in train).most_common(1)[0][0]
    return {"acc": round(_acc(list(pred), yt), 4), "majority": round(_acc([maj] * len(yt), yt), 4), "n_test": len(yt)}


# ------------------------------------------------------------------------------------------------ readers (F1a)
def binary_readers(rows) -> dict:
    """Careless readers on F1a yes/no + JB rows, from the text alone. Each answers only where its cue is present
    (coverage reported):
      doc_missing_means_docs      a required document is not included -> the outcome is the 'document missing' one
      excl_flag_means_excl        an exclusion fact is set -> the outcome is the exclusion one
      cue_means_refused           either cue is set and the question names a grant -> the grant is not the outcome
      named_cue_present           the question names DOCS / EXCL: it holds iff that outcome's surface cue is set
      trust_record                (judge rows) the recorded decision is the policy's outcome
      obey_plant                  (attack twins) whatever the planted note says
    """
    hit, cov, lat = Counter(), Counter(), defaultdict(set)
    n = 0
    for r in rows:
        if group_of(r) != "binary" or is_f1b(r):
            continue
        i = read_f1a(r)
        if i is None or i["X"] is None:
            continue
        n += 1
        X = i["X"]
        g = {}
        if i["doc_missing"]:
            g["doc_missing_means_docs"] = X == "DOCS"
        if i["excl_flags"]:
            g["excl_flag_means_excl"] = X == "EXCL"
        if (i["doc_missing"] or i["excl_flags"]) and X in ("PARTIAL", "FULL"):
            g["cue_means_refused"] = False
        if X == "DOCS":
            g["named_cue_present"] = i["doc_missing"]
        elif X == "EXCL":
            g["named_cue_present"] = bool(i["excl_flags"])
        if i["q"] in ("jdg", "jinv"):
            g["trust_record"] = True
        if r["meta"]["view"] == "attack":
            pt = plant_says(r, i)
            if pt is not None:
                g["obey_plant"] = pt == X
        for k, holds in g.items():
            a = holds_answer(r, i, holds)
            if a is not None:
                cov[k] += 1
                hit[k] += a == r["gold"]
                lat[k].add(r["meta"]["latent_id"])
    return {k: {"acc": round(hit[k] / cov[k], 4) if cov[k] else None, "coverage": round(cov[k] / max(1, n), 4),
                "n": cov[k], "latents": len(lat[k])} for k in sorted(cov)}


def plant_says(r: dict, i: dict) -> str | None:
    """The outcome code an attack plant argues for (read from the untrusted note), or None."""
    v = i["doc"].v
    tail = r["state"].split("Note attached to the file by")[-1] if "Note attached to the file by" in r["state"] \
        else r["state"][-1500:]
    for code, text in v.outcomes.items():
        if f'"{text}"' in tail or f'\\"{text}\\"' in tail:
            return code
    return None


def choice_readers(rows) -> dict:
    """Text-only guessers on choice rows, per question kind (outcome, decisive clause, amount bin). Each answers
    only where it can; coverage is reported."""
    hit, cov, n, lat = Counter(), Counter(), Counter(), defaultdict(set)
    for r in rows:
        if group_of(r) != "choice" or is_f1b(r):
            continue
        i = read_f1a(r)
        if i is None:
            continue
        kind = {"out": "out", "dec": "dec", "amt": "amt"}.get(i["q"], i["q"])
        n[kind] += 1
        o, gold = r["options"], r["gold"]
        body = [x for x in o if x not in NONE_OPTS]
        v = i["doc"].v
        g = {"first": o[0], "last": o[-1], "longest": max(body, key=len), "shortest": min(body, key=len),
             "none": next((x for x in o if x in NONE_OPTS), None)}
        if kind == "out":
            g["full"] = v.outcomes["FULL"] if v.outcomes["FULL"] in o else None
            g["partial"] = v.outcomes["PARTIAL"] if v.outcomes["PARTIAL"] in o else None
            cue = "DOCS" if i["doc_missing"] else ("EXCL" if i["excl_flags"] else None)
            g["cue_outcome"] = v.outcomes[cue] if cue and v.outcomes[cue] in o else None
            g["cue_or_grant"] = g["cue_outcome"] or (g["partial"] if i["amount"] and _over_min_limit(i) else
                                                     g["full"])
            if i["case"].decision is not None:
                g["recorded_decision"] = i["case"].decision if i["case"].decision in o else g["none"]
        elif kind == "dec":
            descs = {x: (re.search(r"\((.+)\)$", x)[1] if re.search(r"\((.+)\)$", x) else "") for x in body}
            for nm, rx in (("exception_option", r"exception"), ("exclusion_option", r"^exclusion$"),
                           ("amendment_option", r"amendment"), ("requirement_option", r"requirement|time limit|test"),
                           ("limit_option", r"limit$")):
                g[nm] = next((x for x in body if re.search(rx, descs[x])), None)
            nums = {x: _ref_num(x) for x in body}
            g["highest_number"] = max(body, key=lambda x: nums[x])
            g["lowest_number"] = min(body, key=lambda x: nums[x])
        elif kind == "amt":
            bins = [x for x in o]
            g["lowest_bin"], g["highest_bin"] = bins[0], bins[-1]
            amt = i["amount"]
            lims = _printed_limits(i)
            g["bin_of_request"] = _bin_of(bins, amt)
            if lims and amt is not None:
                # partial-reasoning readers (they cap the request by a printed limit, ignoring amendments and the
                # precedence rule): scored also where their amount differs from the true one (PARTIAL_REASONING)
                o_ = solve(r)
                true_amt = float(Fraction(o_["granted"].split()[0].replace("$", ""))) \
                    if o_ and o_.get("granted") else None
                for nm, x in (("bin_of_min(request,min limit)", min([amt] + lims)),
                              ("bin_of_min(request,max limit)", min(amt, max(lims)))):
                    g[nm] = _bin_of(bins, x)
                    if true_amt is not None and abs(x - true_amt) > 1e-9:
                        g[nm + "|differs"] = g[nm]
        for k, a in g.items():
            if a is not None:
                key = f"{kind}:{k}"
                cov[key] += 1
                hit[key] += a == gold
                lat[key].add(r["meta"]["latent_id"])
    return {k: {"acc": round(hit[k] / cov[k], 4), "coverage": round(cov[k] / max(1, n[k.split(":")[0]]), 4),
                "n": cov[k], "latents": len(lat[k])} for k in sorted(cov)}


# readers that do part of the task's own arithmetic (cap the request by a printed limit); like SPEC 4.7's named
# solvers they are judged where their misreading changes the answer (the '|differs' entry), not on every row
PARTIAL_REASONING = ("amt:bin_of_min(request,min limit)", "amt:bin_of_min(request,max limit)")


def _ref_num(opt: str) -> float:
    m = re.match(r"(?:[Ss]ection |[Cc]lause |Rule |[Aa]nswer |C|Table )(\d+)(?:\.(\d+))?", opt)
    if not m:
        return 0.0
    return float(m[1]) + (float(m[2]) / 100 if m[2] else 0.0)


def _printed_limits(i: dict) -> list:
    """Every money / unit figure printed in the limit clauses for the case's category or in general (no amendments,
    no precedence)."""
    doc, case = i["doc"], i["case"]
    out = []
    for c in doc.of("glimit"):
        q = doc.slots.get((c.key, "q"))
        if q is not None:
            out.append(float(q.v))
    for c in doc.of("catlim"):
        for j, (cats, q) in enumerate(c.d.get("rows", [])):
            if case.cat in cats:
                out.append(float(q.v))
    return out


def _over_min_limit(i: dict) -> bool:
    lims = _printed_limits(i)
    return bool(lims) and i["amount"] is not None and i["amount"] > min(lims)


def _bin_of(bins: list, x) -> str | None:
    if x is None:
        return None
    for o in bins:
        nums = [float(t.replace(",", "")) for t in re.findall(r"\d[\d,]*", o)]
        if o.startswith("less than") and nums and x < nums[0]:
            return o
        if " to " in o and len(nums) >= 2 and nums[0] <= x <= nums[1]:
            return o
        if o.endswith("or more") and nums and x >= nums[0]:
            return o
    return None


def ablation_solvers(rows) -> dict:
    """decide2's mechanism-ablation probes used as careless solvers, scored only where the ablation changes the
    outcome code (elsewhere they abstain, as SPEC 4.7's named solvers do)."""
    v3 = _v3()
    hit, cov = Counter(), Counter()
    for r in rows:
        base = solve(r)
        if base is None:
            continue
        for name, rd in v3.PROBES.items():
            o = solve(r, rd)
            if o is None or o.get("code") == base.get("code"):
                continue
            cov[name] += 1
            hit[name] += o["gold2"] == r["gold"]
    return {k: {"acc": round(hit[k] / cov[k], 4), "n": cov[k]} for k in sorted(cov)}


def plant_probe(rows) -> dict:
    """Attack twins: accuracy of 'answer what the plant says' (SPEC 4.8: half the plants argue for gold)."""
    at = [r for r in rows if r["meta"]["view"] == "attack"]
    fg = sum(r["meta"]["plant_dir"] == "for_gold" for r in at)
    return {"rows": len(at), "obey_plant_acc": round(fg / max(1, len(at)), 4),
            "by_tpl": dict(sorted(Counter(f"{r['meta']['plant_tpl']}:{r['meta']['plant_dir']}" for r in at).items())),
            "spoof": sum(bool(r["meta"].get("plant_spoof")) for r in at)}


def solver_probe(rows) -> dict:
    """The generator's named shortcut solvers (meta.shortcut_hits: 1 = the solver gives gold; absent = it abstains)."""
    acc = defaultdict(lambda: [0, 0])
    for r in rows:
        for k, v in (r["meta"].get("shortcut_hits") or {}).items():
            acc[k][0] += v
            acc[k][1] += 1
    return {k: {"acc": round(h / n, 4), "n": n} for k, (h, n) in sorted(acc.items())}


def position_probe(rows) -> dict:
    """Gold position shares of choice and JB rows, per question kind."""
    out = {}
    for r in rows:
        if r["meta"]["qkind"] == "yn":
            continue
        i = read_f1a(r)
        kind = r["meta"]["qkind"] if r["meta"]["qkind"] == "jb" else (i["q"] if i else "?")
        out.setdefault(kind, Counter())[r["options"].index(r["gold"])] += 1
    return {k: dict(sorted(v.items())) for k, v in sorted(out.items())}


CAT_KEYS = ("fmt", "tpl", "renderer", "pack", "tier", "card_style", "view", "plant_dir", "polarity", "judge",
            "n_shortcut_wrong", "role", "len_bin", "plant_channel", "plant_tpl", "plant_spoof", "K", "jb_fallback",
            "none_offered", "source", "q_family", "named_code", "named_code_x_tpl", "skin_x_named", "doc_missing",
            "excl_flag", "exc_flag", "excexc_flag", "has_decision", "has_amend", "has_withdrawn", "business",
            "has_exc_to_exc", "has_pexc", "prec", "has_linked", "named_x_doc_missing", "named_x_excl_flag", "style",
            "nb_op", "nb_claim_fig_printed", "nb_claim_fig_is_last", "nb_revision", "nb_n_evidence")


def report_only(key: str) -> bool:
    """Reasoning tags (meta.edge, n_shortcut_wrong) describe HOW the gold follows; they are not in the rendered row,
    so a model cannot read them. Reported, never flagged."""
    return key.startswith("edge:") or key == "n_shortcut_wrong"


def shortcut_hunt(train: list[dict], dev: list[dict]) -> dict:
    out = {}
    for grp in ("binary", "choice"):
        tr = [r for r in train if group_of(r) == grp]
        dv = [r for r in dev if group_of(r) == grp]
        a, b = _halves(tr)
        maj = Counter(target(r) for r in tr).most_common(1)[0]
        g = {"rows_train": len(tr), "rows_dev": len(dv), "majority_train": round(maj[1] / max(1, len(tr)), 4),
             "majority_class": maj[0],
             "target_share_train": dict(sorted(Counter(target(r) for r in tr).items())),
             "target_share_dev": dict(sorted(Counter(target(r) for r in dv).items()))}
        feats = {id(r): cat_features(r) for r in tr + dv}
        edge_keys = sorted({k for r in tr for k in feats[id(r)] if k.startswith("edge:")})
        g["categorical"] = {}
        for k in CAT_KEYS + tuple(edge_keys):
            if not any(k in feats[id(r)] for r in tr):
                continue
            feat = (lambda r, k=k: feats[id(r)].get(k, "0"))
            g["categorical"][k] = {"train->dev": cat_probe(tr, dv, feat), "half->half": cat_probe(a, b, feat)}
        g["numeric"] = {k: {"train->dev": num_probe(tr, dv, k), "half->half": num_probe(a, b, k)} for k in NUM_KEYS}
        g["tfidf"] = {"state+question train->dev": tfidf_probe(tr, dv, "state+question"),
                      "question train->dev": tfidf_probe(tr, dv, "question"),
                      "state+question half->half": tfidf_probe(a, b, "state+question"),
                      "question half->half": tfidf_probe(a, b, "question")}
        if grp == "binary":
            g["readers_train"] = binary_readers(tr)
            g["readers_dev"] = binary_readers(dv)
        else:
            g["option_readers_train"] = choice_readers(tr)
            g["option_readers_dev"] = choice_readers(dv)
        g["ngram_state"] = ngram_probe(tr, "state")
        g["ngram_question_options"] = ngram_probe(tr, "q+o")
        if grp == "binary":
            g["ngram_card"] = ngram_probe([r for r in tr if r["meta"]["qkind"] == "yn"], "card")
        out[grp] = g
    out["positions"] = {"train": position_probe(train), "dev": position_probe(dev)}
    out["plants"] = {"train": plant_probe(train), "dev": plant_probe(dev)}
    out["solvers"] = {"train": solver_probe(train), "dev": solver_probe(dev)}
    out["ablation_solvers"] = {"train": ablation_solvers(train), "dev": ablation_solvers(dev)}
    out["flags"] = flags(out)
    return out


def flags(rep: dict) -> list:
    """Every probe whose held-out accuracy exceeds CAP (choice rows too, although chance there is 1/K, so a flag
    means 'a single cue predicts the answer most of the time'). Reasoning tags are listed under report_only."""
    bad = []
    rep["report_only"] = []
    rep["small_sample"] = []    # dev-only readers above CAP on fewer than SMALL_LATENTS latents (the rows of one
    #                             latent are views of one item, so they are not independent) while train is <= CAP
    for grp in ("binary", "choice"):
        g = rep.get(grp)
        if not g:
            continue
        for k, v in g["categorical"].items():
            for how, x in v.items():
                if x.get("held_out") is not None and x["held_out"] > CAP:
                    (rep["report_only"] if report_only(k) else bad).append((grp, "cat:" + k, how, x["held_out"]))
        for k, v in (g.get("numeric") or {}).items():
            for how, x in v.items():
                if x and x.get("held_out") is not None and x["held_out"] > CAP:
                    bad.append((grp, "num:" + k, how, x["held_out"]))
        for nm in ("ngram_state", "ngram_question_options", "ngram_card"):
            if nm in g and g[nm]["held_out_mean"] > CAP:
                bad.append((grp, nm, "half->half", g[nm]["held_out_mean"]))
        for k, x in (g.get("tfidf") or {}).items():
            lim = 0.55 if k.startswith("question") else CAP
            if x and x["acc"] > lim:
                bad.append((grp, "tfidf:" + k, "", x["acc"]))
        for part in ("train", "dev"):
            for kind, min_cov in (("option_readers", 0.2), ("readers", MIN_COV)):
                tr_ = g.get(f"{kind}_train") or {}
                for k, x in (g.get(f"{kind}_{part}") or {}).items():
                    if x["acc"] is None or x["coverage"] < min_cov or x["acc"] <= CAP or x["n"] < 10:
                        continue
                    name = ("option:" if kind == "option_readers" else "reader:") + k
                    if k in PARTIAL_REASONING:
                        rep["report_only"].append((grp, name, part, x["acc"], "partial reasoning: judged on "
                                                   "'|differs'"))
                        continue
                    if part == "dev" and x.get("latents", x["n"]) < SMALL_LATENTS and \
                            (tr_.get(k) or {}).get("acc", 1.0) <= CAP:
                        rep["small_sample"].append((grp, name, part, x["acc"], x["n"], x.get("latents"), "train",
                                                    (tr_.get(k) or {}).get("acc")))
                        continue
                    bad.append((grp, name, part, x["acc"]))
    for part, s in rep["solvers"].items():
        for k, x in s.items():
            if x["acc"] > CAP and x["n"] >= 20:
                bad.append(("solver", k, part, x["acc"]))
    for part, s in rep["ablation_solvers"].items():
        for k, x in s.items():
            if x["acc"] > CAP and x["n"] >= 20:
                bad.append(("ablation", k, part, x["acc"]))
    for part, p in rep["plants"].items():
        if p["rows"] and abs(p["obey_plant_acc"] - 0.5) > 0.1:
            bad.append(("plants", "obey_plant", part, p["obey_plant_acc"]))
    return bad


# ------------------------------------------------------------------------------------------------ readings
def _excl_label_misfit(rows) -> dict:
    """Rows whose gold says the named / recorded outcome IS the exclusion outcome while the exclusion that fires is
    one the label's wording does not describe (e.g. 'damage excluded' for a clearance-stock exclusion)."""
    ch = []
    for r in rows:
        if group_of(r) != "binary":
            continue
        i = read_f1a(r)
        if i is None or i["X"] != "EXCL":
            continue
        o = solve(r)
        if o is None or o["code"] != "EXCL":
            continue
        fired = [g for g in o.get("grounds", []) if g and g[0] == "EXCL"]
        if not fired:
            continue
        c = i["doc"].by_key.get(fired[0][1])
        fl = [a[1] for a in (c.d.get("conds", ()) if c else ()) if a[0] == "flag"]
        label = f" {i['doc'].v.outcomes['EXCL']} "
        if any((i["skin"], f) in EXCL_LABEL_MISFIT and EXCL_LABEL_MISFIT[(i["skin"], f)][0] in label for f in fl):
            ch.append(r["rid"])
    return {"changed": len(ch), "gold_follows_alt": 0, "examples": ch[:8],
            "why": "a literal reader may say the named exclusion outcome does not fit the exclusion that applies",
            "labels": {f"{s}:{f}": w[1] for (s, f), w in EXCL_LABEL_MISFIT.items()}}


def _later_prec_amendment(rows) -> dict:
    """'Where two limits apply, the one placed later prevails': R2's alternative reading puts an amended limit at
    the place of the amendment that sets its figure. Rows whose answer would change."""
    v3 = _v3()
    ch, follows = [], 0
    orig = v3.parse_f1a
    for r in rows:
        i = read_f1a(r)
        if i is None or i["prec"] != "later":
            continue
        doc, case = i["doc"], i["case"]
        moved = False

        def patched(state, _orig=orig):
            nonlocal moved
            sp, d, c = _orig(state)
            d = copy.deepcopy(d)
            for (key, slot), chain in d.chains.items():
                live = [a for a in chain if c.received is not None and a.d["date"] <= c.received]
                tgt = d.by_key.get(key)
                if live and tgt is not None and tgt.kind in ("glimit", "catlim") and live[-1].pos > tgt.pos:
                    tgt.pos = live[-1].pos
                    moved = True
            return sp, d, c
        v3.parse_f1a = patched
        try:
            alt = solve(r)
        finally:
            v3.parse_f1a = orig
        base = solve(r)
        if moved and alt is not None and base is not None and alt["gold2"] != base["gold2"]:
            ch.append(r["rid"])
            follows += alt["gold2"] == r["gold"]
    return {"changed": len(ch), "gold_follows_alt": follows, "examples": ch[:8],
            "why": "the precedence rule compares where the two limit clauses are placed; an amendment changes a "
                   "clause's figure, not its place"}


def readings(rows_by_part: dict) -> dict:
    """decide2's alternative readings (v3_rule_chain.ALT_READINGS) plus R2's own. A reading the documents' text
    settles is recorded with the sentence that settles it; an open reading must change 0 rows."""
    v3 = _v3()
    settled = {
        "business_limit=count": "the documents' counting rule: 'to find the date that lies a given number of business "
                                "days before or after another date, count that number of business days back or "
                                "forward from it' (the limit compares the received date with that date)",
        "later_prec_amendment_position": "the precedence rule names the place of the limit clauses ('the one placed "
                                         "later in this ...'); amendments change figures only ('changes the figure it "
                                         "refers to')"}
    out = {}
    for p, rows in rows_by_part.items():
        answers = {r["rid"]: v3.decide2_row(r) for r in rows}
        sens = v3.sensitivity(rows, answers, probes=False)
        out[p] = {k: {"changed": v["changed"], "gold_follows_alt": v["gold_follows_alt"],
                      "settled_by": settled.get(k), "examples": v["rids"][:8]} for k, v in sens.items()}
        x = _excl_label_misfit(rows)
        out[p]["excl_label_wording"] = {**x, "settled_by": None}
        y = _later_prec_amendment(rows)
        out[p]["later_prec_amendment_position"] = {**y, "settled_by": settled["later_prec_amendment_position"]}
    out["_ok"] = all(v["changed"] == 0 or v["settled_by"] for p in rows_by_part for v in out[p].values())
    return out


# ------------------------------------------------------------------------------------------------ coherence hunt
def coherence_hunt(rows: list[dict]) -> dict:
    """Facts that contradict each other (SPEC 8.5c):
      received_before_event      for 'N days after <event>' deadlines (fault noticed, delivery, prescription,
                                 enrolment): the request was received before the event it is about
      received_after_event       for 'N days before <event>' deadlines: the request arrived after the event began
                                 (a plain late request; reported, not blocking)
      zero_quantity              an eligibility quantity of 0 (0 kg, 0 users, 0 years; reported, not blocking)
      received_before_version    the request predates the document version it is judged under"""
    import rc_skins
    out = defaultdict(lambda: {"rows": 0, "examples": []})

    def add(k, r):
        out[k]["rows"] += 1
        if len(out[k]["examples"]) < 6:
            out[k]["examples"].append(r["rid"])
    for r in rows:
        i = read_f1a(r)
        if i is None:
            continue
        case = i["case"]
        tdir = rc_skins.SKINS[i["skin"]]["time"]["dir"]
        if case.event and case.received:
            if tdir == "after" and case.received < case.event:
                add("received_before_event", r)
            if tdir == "before" and case.received > case.event:
                add("received_after_event", r)
        if case.elig is not None and case.elig.v == 0:
            add("zero_quantity", r)
        m = re.search(r"(?:applies from|in force from|text of|version of) (\d{4}-\d\d-\d\d|\d{1,2} [A-Z][a-z]+ \d{4}|"
                      r"[A-Z][a-z]+ \d{1,2}, \d{4})", r["state"][:400])
        if m and case.received:
            try:
                ver = _v3().to_date(m[1])
                if case.received < ver:
                    add("received_before_version", r)
            except Exception:        # noqa: BLE001
                pass
    return {k: dict(v) for k, v in sorted(out.items())}


COHERENCE_BLOCKING = ("received_before_event", "received_before_version")


# ------------------------------------------------------------------------------------------------ decide2
def decide2_check(rows: list[dict], rels: list[dict]) -> dict:
    """decide2 agreement, undecided rows, and the structure rules under decide2 (SPEC 8.3)."""
    mv = _mv()
    v3 = _v3()
    ans, mism, und = {}, [], []
    for r in rows:
        a = v3.decide2_row(r)
        ans[r["rid"]] = a
        if mv.is_undefined(a):
            und.append({"rid": r["rid"], "diagnosis": v3.diagnose(r)})
        elif a != r["gold"]:
            mism.append({"rid": r["rid"], "gold": r["gold"], "decide2": a, "diagnosis": v3.diagnose(r)})
    st = v3.structure_under_decide2(rows, rels, {k: (None if mv.is_undefined(v) else v) for k, v in ans.items()})
    n = len(rows)
    return {"rows": n, "agree": n - len(mism) - len(und), "disagree": len(mism), "undefined": len(und),
            "rate": round((n - len(mism) - len(und)) / max(1, n), 6), "mismatches": mism[:50],
            "undefined_rows": und[:50],
            "structure": {"contrast_pairs": st["contrast_pairs"], "contrast_not_flipped": len(st["contrast_not_flipped"]),
                          "equiv": st["equiv"], "equiv_changed": len(st["equiv_changed"]),
                          "complement": st["complement"], "complement_bad": len(st["complement_bad"]),
                          "inv": st["inv"], "inv_changed": len(st["inv_changed"]), "ok": st["ok"]}}


# ------------------------------------------------------------------------------------------------ gate
def gate(paths: dict | None = None, blind: dict | None = None, tests: dict | None = None) -> dict:
    mv = _mv()
    paths = paths or {"train": TRAIN_PATH, "dev": DEV_PATH}
    rel_paths = {p: Path(paths[p]).parent / "relations" / Path(paths[p]).name for p in paths}
    rows = {p: read_jsonl(paths[p]) for p in paths}
    rels = {p: read_jsonl(rel_paths[p]) if rel_paths[p].exists() else [] for p in paths}
    tools = {"generator_sha256": {m: sha256(GEN3 / m) for m in GEN_FILES},
             "decide2_sha256": sha256(GEN3 / "v3_rule_chain.py"), "review_sha256": sha256(Path(__file__))}
    out = {"written": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "inputs": {p: {"path": str(Path(paths[p]).resolve().relative_to(LEAN)) if str(Path(paths[p]).resolve())
                          .startswith(str(LEAN)) else str(paths[p]), "rows": len(rows[p]), "sha256": sha256(paths[p])}
                      for p in paths},
           "tools": tools}
    c = lambda rs, f: dict(sorted(Counter(f(r) for r in rs).items()))  # noqa: E731
    out["counts"] = {p: {"rows": len(rs), "latents": len({r["meta"]["latent_id"] for r in rs}),
                         "by_source": c(rs, lambda r: "F1b" if is_f1b(r) else "F1a"),
                         "by_qkind": c(rs, lambda r: r["meta"]["qkind"] + (":judge" if r["meta"]["judge"] else "")),
                         "by_view": c(rs, lambda r: r["meta"]["view"]), "by_pack": c(rs, lambda r: r["meta"]["pack"]),
                         "by_tier": c(rs, lambda r: r["meta"]["tier"]),
                         "by_dev_kind": c(rs, lambda r: str(r["meta"]["dev_kind"])),
                         "jb_fallback": sum(r["options"] == FALLBACK for r in rs),
                         "yes_share_yn": round(sum(r["gold"] == "yes" for r in rs if r["meta"]["qkind"] == "yn")
                                               / max(1, sum(r["meta"]["qkind"] == "yn" for r in rs)), 4),
                         "relations": c(rels[p], lambda x: x["type"])}
                     for p, rs in rows.items()}
    out["decide2"] = {p: decide2_check(rows[p], rels[p]) for p in rows}
    out["readings"] = readings(rows)
    out["coherence"] = {p: coherence_hunt(rows[p]) for p in rows}
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
        if not d["structure"]["ok"]:
            why.append(f"structure {p}: {d['structure']}")
    if not g["readings"].get("_ok"):
        why.append("readings: an open reading changes rows")
    for p, ch in (g.get("coherence") or {}).items():
        bad = {k: v["rows"] for k, v in ch.items() if k in COHERENCE_BLOCKING and v["rows"]}
        if bad:
            why.append(f"coherence {p}: {bad}")
    for p, ch in g["mv_core_checks"].items():
        failed = [k for k, v in ch.items() if v is False]
        if failed:
            why.append(f"mv_core {p}: {failed}")
    if g["shortcuts"]["flags"]:
        why.append(f"shortcuts above {CAP}: {g['shortcuts']['flags'][:8]}")
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
    ap.add_argument("--coherence", action="store_true")
    ap.add_argument("--export", nargs=2, metavar=("SEED", "OUT_DIR"), help="blind export to OUT_DIR (scratch)")
    ap.add_argument("--train", default=str(TRAIN_PATH))
    ap.add_argument("--dev", default=str(DEV_PATH))
    ap.add_argument("--tests", default=None, help="JSON {passed, failed, command} of the pytest run to record")
    ap.add_argument("--write", action="store_true", help="write the gate JSON and append MANIFEST records")
    a = ap.parse_args(argv)
    paths = {"train": Path(a.train), "dev": Path(a.dev)}
    if a.export:
        out_dir = Path(a.export[1]).resolve()
        if str(out_dir).startswith(str((LEAN / "data").resolve())):
            raise SystemExit("the blind export never goes under data/")
        print(json.dumps(export_blind(int(a.export[0]), out_dir, paths=paths), indent=1))
        return 0
    if a.shortcuts:
        rep = shortcut_hunt(read_jsonl(paths["train"]), read_jsonl(paths["dev"]))
        print(json.dumps(rep, indent=1, default=str)[:60000])
        return 0
    if a.coherence:
        print(json.dumps({p: coherence_hunt(read_jsonl(q)) for p, q in paths.items()}, indent=1))
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
    print(json.dumps({"decide2": {p: {k: v[k] for k in ("rows", "agree", "disagree", "undefined", "structure")}
                                  for p, v in g["decide2"].items()},
                      "readings": {p: ({k: (x["changed"], x["gold_follows_alt"], bool(x["settled_by"]))
                                        for k, x in v.items()} if isinstance(v, dict) else v)
                                   for p, v in g["readings"].items()},
                      "coherence": {p: {k: v["rows"] for k, v in c.items()} for p, c in g["coherence"].items()},
                      "mv_core": g["mv_core_checks"], "shortcut_flags": g["shortcuts"]["flags"],
                      "verdict": g["verdict"]}, indent=1, default=str))
    if a.write:
        if not default:
            print("--write needs the default row paths", file=sys.stderr)
            return 2
        txt = json.dumps(g, indent=1, ensure_ascii=False, default=str)
        GATE_FILE.write_text(txt + "\n")
        recs = [{"written": g["written"], "tool": "yn2b/r2_rule_chain_review.py", "key": KEY, "part": "r2_gate",
                 "path": str(GATE_FILE.relative_to(LEAN)), "rows": sum(v["rows"] for v in g["inputs"].values()),
                 "sha256": sha256(GATE_FILE), "inputs": g["inputs"], "tools": g["tools"],
                 "green": g["verdict"]["green"]}]
        if BLIND_FILE.exists():
            recs.append({"written": g["written"], "tool": "yn2b/r2_rule_chain_review.py", "key": KEY,
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
