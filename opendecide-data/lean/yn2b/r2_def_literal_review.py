"""Reviewer R2 for F6 (gen3_def_literal): blind-solve record, shortcut hunt, coherence hunt and the F6 gate
(SPEC 8.1, 8.3, 8.4, 8.5).

Read-only on the family's rows. Nothing here labels a row: the gold comes from the generator's decide()
(golden_src/gen3/dl_core.py), the second opinion from builder A's decide2 (golden_src/gen3/v3_def_literal.py), and the
blind answers from R2 reading rendered rows only (state, card, question, options).

  blind_compare(answers, rows)   R2's blind answers (rid -> option text) against the stored gold
  shortcut_hunt(train, dev)      every cheap feature that could predict the gold on its own (SPEC 4.7, 8.4): metadata
                                 strata, text cues of the definition (joiner, exclusions, deeming clause, 'not
                                 recorded'), the distractors a careless reader obeys (everyday usage, the outside
                                 rule in the background, the attack plant, the register's record), lengths, the best
                                 single n-gram (chosen on one latent half, scored on the other), the TF-IDF probes,
                                 option position / length heuristics for choice rows, and the generator's named
                                 shortcut solvers
  coherence_hunt(rows)           facts that contradict each other (the ambiguity hunt, SPEC 8.5c): a JB definition in
                                 force after a date fact, months-at-the-property vs move-in date, an age below a
                                 duration, minors on a lease, an event dated after the file was opened, a filler date
                                 before the event, a JB fallback pair under a question that names no claim
  decide2_check(rows, rels)      decide2 agreement plus the structure rules under decide2
  gate(...)                      the F6 gate table

Run from lean/:
  PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python yn2b/r2_def_literal_review.py --gate [--write]
"""
from __future__ import annotations

import argparse
import datetime as dt
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

KEY = "gen3_def_literal"
RAW = LEAN / "data" / "v14_parts" / "yn2b_raw"
TRAIN_PATH = RAW / f"{KEY}.jsonl"
DEV_PATH = RAW / "dev" / f"{KEY}.jsonl"
REL_PATHS = {"train": RAW / "relations" / f"{KEY}.jsonl", "dev": RAW / "dev" / "relations" / f"{KEY}.jsonl"}
CAP = 0.60           # SPEC 4.7 / 8.4: no single shortcut above 60% (question-only TF-IDF: 55%)
BLIND_FILE = YN2B / "r2_def_literal_blind.json"
GATE_FILE = YN2B / "r2_def_literal_gate.json"
MANIFEST = GEN3 / "MANIFEST_yn2b.jsonl"
FALLBACK = ["yes, this holds", "no, this does not hold"]
EVERY = "Every condition is satisfied"


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


# ------------------------------------------------------------------------------------------------ text reading
def _v3():
    import v3_def_literal as v3
    return v3


def card_of(r: dict) -> dict:
    """The row's definitions (yes/no card or choice option lines), {} when the row has none (JB)."""
    if r.get("_defs") is not None:
        return r["_defs"]
    q = r["meta"].get("defs")
    if not q:
        return {}
    p = LEAN / "data" / "v14_parts" / "yn2b_defs" / f"{KEY}__{q}.json"
    return json.loads(p.read_text()) if p.exists() else {}


def definition_text(r: dict) -> str | None:
    """The operative definition as the row shows it: the yes/no card's clause line, or the JB state's governing
    definition. Choice rows show only option lines (None)."""
    if r["meta"]["qkind"] == "yn":
        c = card_of(r)
        ks = [k for k in c if k not in ("yes", "no")]
        return c[ks[0]] if ks else None
    if r["meta"]["qkind"] == "jb":
        m = re.search(r"\(in force from [^)]*\): ((?:A|An) .+? A fact the file does not record counts as not "
                      r"established\.)", r["state"])
        return m.group(1) if m else None
    return None


_USAGE = None


def _usage_table():
    """Every everyday-usage / outside-knowledge statement template of the packs with the verdict it implies
    (dl_packs is pure surface data)."""
    global _USAGE
    if _USAGE is None:
        import dl_packs as dp
        rows = []
        for p in dp.PACKS.values():
            for tpl, v in p.usage:
                rx = re.escape(tpl).replace(re.escape("{item}"), ".+?").replace(re.escape("{at}"), ".+?") \
                    .replace(re.escape("{t}"), ".+?")
                rows.append((re.compile(rx), v))
            for t in p.terms:
                for _, us in t.items:
                    for s, v in us:
                        rows.append((re.compile(re.escape(s)), v))
        _USAGE = rows
    return _USAGE


_OUTSIDE = re.compile(r"Under [^,]+, (?:a|an) [a-z]+ (?:that|who) .+? is (not )?treated as (?:an? )?'[^']+'\.")


def text_cues(r: dict) -> dict:
    """Cues a reader can see without applying the definition: the usage verdict (True = 'it is one', None = absent),
    the outside rule's verdict, the register's record, 'not recorded' facts, the definition's shape."""
    s = r["state"]
    out = {"usage": None, "outside": None, "record": None, "missing": bool(re.search(
        r"not recorded|The file does not record", s))}
    for rx, v in _usage_table():
        if rx.search(s):
            out["usage"] = v
            break
    m = _OUTSIDE.search(s)
    if m:
        out["outside"] = m.group(1) is None
    m = re.search(r"recorded classification: (not )?|records the [a-z]+ as (not )?|Recorded classification for this "
                  r"file: (not )?", s)
    if m:
        out["record"] = not any(m.groups())
    d = definition_text(r)
    if d is None and r["meta"]["qkind"] == "choice":
        out.update(joiner="all", n_excl=sum(o.startswith("Exclusion - ") for o in r["options"]),
                   n_el=sum(o.startswith("Requirement - ") for o in r["options"]), deem=False,
                   unless=any(", unless " in o for o in r["options"]))
    elif d:
        out.update(joiner="all" if "all of the following hold" in d else "any",
                   n_excl=len(re.findall(r" It is (?:also )?not (?:an? )?'[^']+' if |; nor if ", d)),
                   n_el=len(re.findall(r"\([a-j]\) ", d)), deem="also counts as" in d, unless=", unless " in d)
    return out


def question_info(r: dict) -> dict:
    """The question family (is / judge / jb / choice) and polarity, read with decide2's question parser (parsing
    only; decide2 labels nothing here)."""
    try:
        q = _v3().parse_question(r["instructions"])
        return {"family": q["family"], "neg": q["neg"]}
    except Exception:
        return {"family": None, "neg": None}


_CLAIM = re.compile(r"\b(?:is the [a-z]+ (?:an? )?'[^']+'(?! or not)|does the [a-z]+ (?:not )?count as|does the [a-z]+ "
                    r"(?:not )?qualify as|should the [a-z]+ (?:not )?be classed as)", re.I)


def states_claim(q: str) -> bool:
    """Does the question itself state the claim that 'yes, this holds' / 'no, this does not hold' answer? ('Which
    statement fits ...?' does not; 'Is the bid a 'small business' ...?' does.) Read from the text, independently of
    the generator's template lists."""
    return bool(_CLAIM.search(q))


def answer_if_applies(r: dict, applies: bool | None, cues: dict | None = None, qi: dict | None = None):
    """The row's answer if the term applied (True) or not (False): the reader-heuristic -> answer bridge."""
    if applies is None:
        return None
    qi = qi or question_info(r)
    k = r["meta"]["qkind"]
    if k == "jb":
        return r["options"][0] if applies else r["options"][1]
    if k != "yn" or qi["family"] is None:
        return None
    if qi["family"] == "is":
        yes = applies != qi["neg"]
    else:
        rec = (cues or text_cues(r))["record"]
        if rec is None:
            return None
        yes = (rec == applies) != qi["neg"]
    return "yes" if yes else "no"


# ------------------------------------------------------------------------------------------------ features
def group_of(r: dict) -> str:
    return "binary" if r["meta"]["qkind"] in ("yn", "jb") else "choice"


def target(r: dict):
    """binary: yes / no (a JB row's first option is the 'it is one' statement); choice: the gold option's position."""
    if group_of(r) == "binary":
        return "yes" if (r["gold"] == "yes" or (r["meta"]["qkind"] == "jb" and r["gold"] == r["options"][0])) \
            else "no"
    return str(r["options"].index(r["gold"]))


def cat_features(r: dict) -> dict:
    m = r["meta"]
    f = {k: str(m.get(k)) for k in ("fmt", "tpl", "renderer", "pack", "tier", "card_style", "view", "plant_dir",
                                     "polarity", "judge", "n_shortcut_wrong", "role")}
    c = text_cues(r)
    qi = question_info(r)
    f["K"] = str(len(r["options"]))
    f["jb_fallback"] = str(r["options"] == FALLBACK)
    f["q_neg"] = str(qi["neg"])
    f["usage_says"] = str(c["usage"])
    f["outside_says"] = str(c["outside"])
    f["record"] = str(c["record"])
    f["missing"] = str(c["missing"])
    f["joiner"] = str(c.get("joiner"))
    f["n_excl"] = str(c.get("n_excl"))
    f["n_el"] = str(c.get("n_el"))
    f["deem"] = str(c.get("deem"))
    f["unless"] = str(c.get("unless"))
    f["real_word"] = str("hc:real_word_redefined" in (m.get("edge") or ""))
    f["term"] = (re.search(r"'([^']+)'", r["instructions"]) or re.search(r"'([^']+)'", r["state"]) or
                 re.search(r"x", "x")).group(0)
    for t in (m.get("edge") or "").split(","):
        if t:
            f["edge:" + t] = "1"
    return f


EDGE_KEYS = ("edge:exception", "edge:exc:allow_deny", "edge:exc:deny_allow", "edge:exc:near_miss",
             "edge:missing_info", "edge:missing_info:decisive", "edge:missing_info:irrelevant",
             "edge:hc:boundary_exact", "edge:hc:boundary_off1", "edge:hc:exception_to_exception",
             "edge:hc:outside_knowledge_ignored", "edge:hc:real_word_redefined", "edge:multi_hop", "edge:temporal",
             "edge:negation")


def num_features(r: dict) -> dict:
    s, q = r["state"], r["instructions"]
    d = definition_text(r) or ""
    return {"len": len(s), "len_q": len(q), "len_def": len(d), "n_lines": s.count("\n") + 1,
            "n_missing": len(re.findall(r"not recorded|The file does not record", s)),
            "n_background": len(re.findall(r"background\.\d+:|^- ", s, re.M))}


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
    te = [(num_features(r).get(key), target(r)) for r in test]
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
    if field == "state":
        return r["state"]
    if field == "card":
        return " ".join(v for k, v in card_of(r).items())
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
    """SPEC 8.4 TF-IDF 1-2-gram logistic regression: fit on train rows, score on test rows. The yes/no card is part
    of what the model reads, so 'state+question' includes it."""
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
        return r["state"] + "\n" + _text(r, "card") + "\n" + r["instructions"] + "\n" + " | ".join(r["options"])
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
    """The generator's named shortcut solvers (meta.shortcut_hits: 1 = the solver gives gold; absent = its cue is not
    in the row, it abstains)."""
    acc = defaultdict(lambda: [0, 0])
    for r in rows:
        for k, v in (r["meta"].get("shortcut_hits") or {}).items():
            acc[k][0] += v
            acc[k][1] += 1
    return {k: {"acc": round(h / n, 4), "n": n} for k, (h, n) in sorted(acc.items())}


def reader_heuristics(rows) -> dict:
    """Careless readers on binary rows, from the text alone: obey the everyday-usage statement, obey the outside rule
    in the background, trust the register's record (judge rows), 'not recorded' means it does not apply, any stated
    exclusion means it does not apply, a deeming clause means it applies, OR-definitions apply / AND-definitions do
    not. Each answers only where its cue is present; coverage is reported."""
    hit, cov = Counter(), Counter()
    for r in rows:
        if group_of(r) != "binary":
            continue
        c, qi = text_cues(r), question_info(r)
        guesses = {"obey_usage": c["usage"], "obey_outside_rule": c["outside"],
                   "missing_means_not": False if c["missing"] else None,
                   "exclusion_means_not": False if c.get("n_excl") else None,
                   "deeming_means_is": True if c.get("deem") else None,
                   "or_is_and_not": {"any": True, "all": False}.get(c.get("joiner"))}
        if r["meta"]["qkind"] == "yn" and qi["family"] == "judge" and c["record"] is not None:
            guesses["trust_record"] = c["record"]
        for k, applies in guesses.items():
            a = answer_if_applies(r, applies, c, qi)
            if a is not None:
                cov[k] += 1
                hit[k] += a == r["gold"]
    n = sum(1 for r in rows if group_of(r) == "binary")
    return {k: {"acc": round(hit[k] / cov[k], 4) if cov[k] else None, "coverage": round(cov[k] / max(1, n), 4)}
            for k in sorted(cov)}


def choice_heuristics(rows) -> dict:
    """Accuracy of text-only guessers on choice rows. Each guesser answers only when it can; coverage is reported."""
    names = ("first", "last", "second_last", "longest", "shortest", "every_condition", "first_exclusion",
             "first_requirement", "not_recorded_requirement", "outside_rule_attr", "unless_exclusion")
    hit, cov = Counter(), Counter()
    import dl_packs as dp
    for r in rows:
        o, gold = r["options"], r["gold"]
        body = [x for x in o if x != EVERY]
        guess = {"first": o[0], "last": o[-1], "second_last": o[-2] if len(o) > 1 else None,
                 "longest": max(body, key=len), "shortest": min(body, key=len), "every_condition": EVERY,
                 "first_exclusion": next((x for x in o if x.startswith("Exclusion - ")), None),
                 "first_requirement": next((x for x in o if x.startswith("Requirement - ")), None),
                 "unless_exclusion": next((x for x in o if x.startswith("Exclusion - ") and ", unless " in x), None)}
        pack = dp.PACKS[r["meta"]["pack"]]
        missing = set()
        for a in pack.attrs:
            if re.search(rf"(?:^|\n|\"|\.){re.escape(a.label)}\"?: \"?not recorded", r["state"]) or \
                    f"The file does not record {a.what}." in r["state"]:
                missing.add(a.id)
        m = _OUTSIDE.search(r["state"])
        for x in body:
            if not x.startswith("Requirement - "):
                continue
            vp = x.split(f"the {pack.entity} ", 1)[-1]
            aid = _attr_of_vp(pack, vp)
            if aid in missing and guess.get("not_recorded_requirement") is None:
                guess["not_recorded_requirement"] = x
        if m:
            vp_o = re.search(r"(?:that|who) (.+?) is (?:not )?treated as", m.group(0)).group(1)
            ao = _attr_of_vp(pack, vp_o)
            for x in body:
                if _attr_of_vp(pack, x.split(f"the {pack.entity} ", 1)[-1].split(", unless ")[0]) == ao:
                    guess["outside_rule_attr"] = x
                    break
        for k in names:
            if guess.get(k) is not None:
                cov[k] += 1
                hit[k] += guess[k] == gold
    n = len(rows)
    return {k: {"acc": round(hit[k] / cov[k], 4) if cov[k] else None, "coverage": round(cov[k] / max(1, n), 4),
                "acc_over_all": round(hit[k] / max(1, n), 4)} for k in names}


def _attr_of_vp(pack, vp: str):
    try:
        return _v3().parse_vp(_v3().CATS[pack.id], vp).attr
    except Exception:
        return None


CAT_KEYS = ("fmt", "tpl", "renderer", "pack", "tier", "card_style", "view", "plant_dir", "polarity", "judge",
            "n_shortcut_wrong", "role", "K", "jb_fallback", "q_neg", "usage_says", "outside_says", "record", "missing",
            "joiner", "n_excl", "n_el", "deem", "unless", "real_word", "term") + EDGE_KEYS
NUM_KEYS = ("len", "len_q", "len_def", "n_lines", "n_missing", "n_background")


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
        g["categorical"] = {}
        for k in CAT_KEYS:
            feat = (lambda r, k=k: feats[id(r)].get(k, "0"))
            g["categorical"][k] = {"train->dev": cat_probe(tr, dv, feat), "half->half": cat_probe(a, b, feat)}
        g["numeric"] = {k: {"train->dev": num_probe(tr, dv, k), "half->half": num_probe(a, b, k)} for k in NUM_KEYS}
        g["tfidf"] = {"state+question train->dev": tfidf_probe(tr, dv, "state+question"),
                      "question train->dev": tfidf_probe(tr, dv, "question"),
                      "state+question half->half": tfidf_probe(a, b, "state+question"),
                      "question half->half": tfidf_probe(a, b, "question")}
        if grp == "binary":
            g["readers_train"] = reader_heuristics(tr)
            g["readers_dev"] = reader_heuristics(dv)
        else:
            g["option_heuristics_train"] = choice_heuristics(tr)
            g["option_heuristics_dev"] = choice_heuristics(dv)
        g["ngram_state"] = ngram_probe(tr, "state")
        g["ngram_question_options"] = ngram_probe(tr, "q+o")
        if grp == "binary":
            g["ngram_card"] = ngram_probe([r for r in tr if r["meta"]["qkind"] == "yn"], "card")
        out[grp] = g
    out["plants"] = {"train": plant_probe(train), "dev": plant_probe(dev)}
    out["solvers"] = {"train": solver_probe(train), "dev": solver_probe(dev)}
    out["flags"] = flags(out)
    return out


# Reasoning tags: the generator's own description of HOW the gold follows (meta.edge, e.g. exc:allow_deny = "an
# exclusion applies", which means 'no' by definition; n_shortcut_wrong). They are not in the rendered row, so a model
# cannot read them; SPEC 4.6 asks for three equal exception groups, not for each group to be gold-balanced. Reported,
# never flagged.
def report_only(key: str) -> bool:
    return key.startswith("edge:") or key == "n_shortcut_wrong"


def flags(rep: dict) -> list:
    """Every probe whose held-out accuracy exceeds CAP. For choice rows the bar is CAP too, although chance there is
    1/K, so a flag means 'a single cue predicts the answer most of the time'. Reasoning tags (report_only) are
    listed under rep['report_only'] instead."""
    bad = []
    rep["report_only"] = []
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
            for k, x in (g.get(f"option_heuristics_{part}") or {}).items():
                if x["acc"] is not None and x["coverage"] >= 0.2 and x["acc"] > CAP:
                    bad.append((grp, "option:" + k, part, x["acc"]))
            for k, x in (g.get(f"readers_{part}") or {}).items():
                if x["acc"] is not None and x["coverage"] >= 0.1 and x["acc"] > CAP:
                    bad.append((grp, "reader:" + k, part, x["acc"]))
    for part, s in rep["solvers"].items():
        for k, x in s.items():
            if x["acc"] > CAP and x["n"] >= 20:
                bad.append(("solver", k, part, x["acc"]))
    for part, p in rep["plants"].items():
        if p["rows"] and abs(p["obey_plant_acc"] - 0.5) > 0.1:
            bad.append(("plants", "obey_plant", part, p["obey_plant_acc"]))
    return bad


# ------------------------------------------------------------------------------------------------ coherence hunt
_DATE = r"\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4}"
FILLER_DATE_LABELS = ("site visit date", "review start date", "visit date")


def _d(s: str) -> dt.date:
    return dt.datetime.strptime(s, "%d %B %Y").date()


def coherence_hunt(rows: list[dict]) -> dict:
    """Facts that contradict each other or the question (SPEC 8.5c: any reading under which the gold is wrong is a
    template fix). Read from the rendered text through decide2's state parser (parsing only).
      jb_fallback_no_claim     JB fallback options ('yes, this holds') under a question that states no claim
      jb_in_force_after_fact   a JB governing definition in force after a date fact or the opening of the file
      months_vs_move_in        months at the property and move-in date both shown and more than 1 month apart (or
                               the move-in date after the file was opened)
      duration_over_age        a duration (years of membership / in the region / in the academy) longer than the
                               age allows (membership > age - 5, residence > age, academy > age - 4)
      minor_adult_fact         an occupant under 16 named on the lease, paying rent, parking a vehicle, or the
                               tenant's spouse / carer / lodger
      event_after_opened       a date fact after the date the file was opened
      filler_date_before_opened a neutral filler date (site visit, review start, visit) before the file was opened
      hours_vs_days_off        an incident with days off work but fewer working hours lost than one working day per
                               day off beyond the first (8 h)
    Each check lists whether the clashing attribute is one the definition uses (then a reader could take the other
    fact and reach the other answer)."""
    v3 = _v3()
    out = defaultdict(lambda: {"rows": 0, "decisive": 0, "rids": []})

    def add(name, r, decisive):
        x = out[name]
        x["rows"] += 1
        x["decisive"] += int(bool(decisive))
        if len(x["rids"]) < 12:
            x["rids"].append(r["rid"])
    for r in rows:
        if r["options"] == FALLBACK and not states_claim(r["instructions"]):
            add("jb_fallback_no_claim", r, True)
        try:
            o = v3.solve(r)
        except Exception:
            continue
        facts = o["facts"]
        doc = v3.parse_state(r["state"])
        used = set()
        if "defn" in o:
            d = o["defn"]
            used = {c.attr for c in d.elements} | {t.attr for t, _ in d.exclusions} | \
                   {u.attr for _, u in d.exclusions if u} | ({d.deem.attr} if d.deem else set())
        elif "conds" in o:
            used = {c.attr for _, c, _ in o["conds"]} | {u.attr for _, _, u in o["conds"] if u}
        dates = {k: v for k, v in facts.items() if isinstance(v, dt.date)}
        if o["kind"] == "jb" and o.get("in_force"):
            late = [k for k, v in dates.items() if v < o["in_force"]]
            if late or (doc.opened and doc.opened < o["in_force"]):
                add("jb_in_force_after_fact", r, any(k in used for k in late))
        pack = o["pack"]
        opened = doc.opened
        if opened is None:
            m = re.search(r"(?:opened on|Opened on) (" + _DATE + ")", r["state"])
            opened = _d(m.group(1)) if m else None
        if opened:
            after = [k for k, v in dates.items() if v > opened]
            if after:
                add("event_after_opened", r, any(k in used for k in after))
            for lab in FILLER_DATE_LABELS:
                m = re.search(rf"(?:{lab}\"?: \"?|The {lab} is )({_DATE})", r["state"])
                if m and _d(m.group(1)) < opened:
                    add("filler_date_before_opened", r, False)
        if pack == "tenancy" and facts.get("months") is not None and facts.get("moved_in") is not None:
            ref = opened or dt.date(2026, 12, 31)
            implied = (ref.year - facts["moved_in"].year) * 12 + ref.month - facts["moved_in"].month
            if facts["moved_in"] > ref or abs(implied - facts["months"]) > 1:
                add("months_vs_move_in", r, {"months", "moved_in"} & used)
        age = facts.get("age")
        if age is not None:
            lim = {"membership": age - 5, "residence": age, "academy": age - 4}
            bad = [k for k, L in lim.items() if facts.get(k) is not None and facts[k] > L
                   and pack in ("club", "sports")]
            if bad:
                add("duration_over_age", r, ({"age"} | set(bad)) & used)
            if pack == "tenancy" and age < 16:
                bad = [k for k in ("on_lease", "vehicle") if facts.get(k) is True]
                if facts.get("rent_share"):
                    bad.append("rent_share")
                if facts.get("relation") in ("spouse", "carer", "lodger"):
                    bad.append("relation")
                if bad:
                    add("minor_adult_fact", r, ({"age"} | set(bad)) & used)
        if pack == "safety" and facts.get("days_off") and facts.get("hours_lost") is not None:
            if facts["hours_lost"] < 8 * (facts["days_off"] - 1):
                add("hours_vs_days_off", r, {"days_off", "hours_lost"} & used)
    return {k: dict(v) for k, v in sorted(out.items())}


# ------------------------------------------------------------------------------------------------ decide2
def decide2_check(rows: list[dict], rels: list[dict]) -> dict:
    """decide2 agreement, undecided rows, and the structure rules under decide2 (SPEC 8.3)."""
    import mv_core as mv
    v3 = _v3()
    ans, mism, und = {}, [], []
    for r in rows:
        a = v3.decide2_row(r)
        ans[r["rid"]] = a
        if mv.is_undefined(a):
            und.append({"rid": r["rid"], "diagnosis": v3.diagnose(r)})
        elif a != r["gold"]:
            mism.append({"rid": r["rid"], "gold": r["gold"], "decide2": a, "diagnosis": v3.diagnose(r)})
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
    n = len(rows)
    return {"rows": n, "agree": n - len(mism) - len(und), "disagree": len(mism), "undefined": len(und),
            "rate": round((n - len(mism) - len(und)) / max(1, n), 6), "mismatches": mism[:50],
            "undefined_rows": und[:50], "structure": dict(sorted(st.items())), "structure_violations": bad[:20]}


def readings(rows_by_part: dict) -> dict:
    """decide2's alternative readings (v3_def_literal.sensitivity): rows whose answer would change. A reading the
    definition text settles ('A fact the file does not record counts as not established') is recorded with the
    sentence that settles it; an open reading must change 0 rows."""
    v3 = _v3()
    settled = {"unrecorded_negative=holds": "the definition's closing sentence: 'A fact the file does not record "
                                            "counts as not established.'",
               "absent_attribute=not_established": "decide2 refuses rows that hide a used attribute (0 rows)",
               "distractor:obey_outside_rule": "the card / question: 'everyday usage and other rule books do not "
                                               "change this', 'Applying only the definition'"}
    out = {}
    for p, rows in rows_by_part.items():
        answers = {r["rid"]: v3.decide2_row(r) for r in rows}
        sens = v3.sensitivity(rows, answers)
        out[p] = {k: {"changed": v["changed"], "gold_follows_alt": v.get("gold_follows_alt"),
                      "settled_by": settled.get(k), "examples": v["rids"][:8]} for k, v in sens.items()}
        out[p].update(unless_scope(rows))
    out["_ok"] = all(v["changed"] == 0 or v["settled_by"] for p in rows_by_part for v in out[p].values())
    return out


OLD_EXCLUSION_LIST = re.compile(r"; nor if the [a-z]+ ")


def unless_scope(rows: list[dict]) -> dict:
    """R2's own readings of the 'unless' scope in multi-exclusion definitions: an 'unless' that also rescues the
    exclusions after it (carries forward), or a last 'unless' that also rescues the ones before it. The rows whose
    answer would change are counted; the readings are settled only when every definition prints one sentence per
    exclusion (no '...; nor if ...' list), so an 'unless' cannot reach past its own sentence."""
    v3 = _v3()
    ch = {"unless_carries_forward": [], "trailing_unless_governs_all": []}
    old = 0
    for r in rows:
        d_txt = definition_text(r) or ""
        old += bool(OLD_EXCLUSION_LIST.search(d_txt))
        if r["meta"]["qkind"] == "choice":
            continue
        try:
            o = v3.solve(r)
        except Exception:
            continue
        d, f, oc = o["defn"], o["facts"], o["outcome"]
        if len(d.exclusions) < 2:
            continue
        path_ok = oc.elements_ok or bool(oc.deem_ok)
        cur, fwd = None, []
        for t, u in d.exclusions:
            cur = u or cur
            fwd.append(t.holds(f) and not (cur.holds(f) if cur else False))
        last = d.exclusions[-1][1]
        back = [t.holds(f) and not ((u or last).holds(f) if (u or last) else False) for t, u in d.exclusions]
        for name, ex in (("unless_carries_forward", fwd), ("trailing_unless_governs_all", back)):
            if (path_ok and not any(ex)) != oc.applies:
                ch[name].append(r["rid"])
    settled = "one sentence per exclusion ('It is not T if A, unless B. It is also not T if C.')" if old == 0 else None
    return {k: {"changed": len(v), "gold_follows_alt": 0, "settled_by": settled, "examples": v[:8],
                "definitions_in_old_list_form": old} for k, v in ch.items()}


# ------------------------------------------------------------------------------------------------ gate
def gate(paths: dict | None = None, blind: dict | None = None, tests: dict | None = None) -> dict:
    import mv_core as mv
    paths = paths or {"train": TRAIN_PATH, "dev": DEV_PATH}
    rel_paths = {p: Path(paths[p]).parent / "relations" / Path(paths[p]).name for p in paths}
    rows = {p: read_jsonl(paths[p]) for p in paths}
    rels = {p: read_jsonl(rel_paths[p]) if rel_paths[p].exists() else [] for p in paths}
    tools = {"generator_sha256": {m: sha256(GEN3 / m) for m in ("gen3_def_literal.py", "dl_core.py", "dl_sample.py",
                                                                 "dl_render.py", "dl_packs.py")},
             "decide2_sha256": sha256(GEN3 / "v3_def_literal.py"), "review_sha256": sha256(Path(__file__))}
    out = {"written": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "inputs": {p: {"path": str(Path(paths[p]).resolve().relative_to(LEAN)) if str(Path(paths[p]).resolve())
                          .startswith(str(LEAN)) else str(paths[p]), "rows": len(rows[p]), "sha256": sha256(paths[p])}
                      for p in paths},
           "tools": tools}
    c = lambda rs, f: dict(sorted(Counter(f(r) for r in rs).items()))  # noqa: E731
    out["counts"] = {p: {"rows": len(rs), "latents": len({r["meta"]["latent_id"] for r in rs}),
                         "by_qkind": c(rs, lambda r: r["meta"]["qkind"] + (":judge" if r["meta"]["judge"] else "")),
                         "by_view": c(rs, lambda r: r["meta"]["view"]), "by_pack": c(rs, lambda r: r["meta"]["pack"]),
                         "by_tier": c(rs, lambda r: r["meta"]["tier"]),
                         "by_dev_kind": c(rs, lambda r: str(r["meta"]["dev_kind"])),
                         "jb_fallback": sum(r["options"] == FALLBACK for r in rs),
                         "yes_share_yn": round(sum(r["gold"] == "yes" for r in rs if r["meta"]["qkind"] == "yn")
                                               / max(1, sum(r["meta"]["qkind"] == "yn" for r in rs)), 4),
                         "every_condition_share_choice": round(
                             sum(r["gold"] == EVERY for r in rs if r["meta"]["qkind"] == "choice")
                             / max(1, sum(r["meta"]["qkind"] == "choice" for r in rs)), 4),
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


COHERENCE_BLOCKING = ("jb_fallback_no_claim", "jb_in_force_after_fact", "months_vs_move_in", "duration_over_age",
                      "minor_adult_fact", "event_after_opened", "filler_date_before_opened", "hours_vs_days_off")


def verdict(g: dict) -> dict:
    why = []
    for p, d in g["decide2"].items():
        if d["disagree"] or d["undefined"]:
            why.append(f"decide2 {p}: {d['disagree']} disagree, {d['undefined']} undefined")
        if any(k.endswith(":bad") for k in d["structure"]):
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
    ap.add_argument("--coherence", action="store_true")
    ap.add_argument("--train", default=str(TRAIN_PATH))
    ap.add_argument("--dev", default=str(DEV_PATH))
    ap.add_argument("--tests", default=None, help="JSON {passed, failed, command} of the pytest run to record")
    ap.add_argument("--write", action="store_true", help="write the gate JSON and append MANIFEST records")
    a = ap.parse_args(argv)
    paths = {"train": Path(a.train), "dev": Path(a.dev)}
    if a.shortcuts:
        rep = shortcut_hunt(read_jsonl(paths["train"]), read_jsonl(paths["dev"]))
        print(json.dumps(rep, indent=1, default=str)[:40000])
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
                      "readings": g["readings"], "coherence": {p: {k: (v["rows"], v["decisive"]) for k, v in c.items()}
                                                               for p, c in g["coherence"].items()},
                      "mv_core": g["mv_core_checks"], "shortcut_flags": g["shortcuts"]["flags"],
                      "verdict": g["verdict"]}, indent=1, default=str))
    if a.write:
        if not default:
            print("--write needs the default row paths", file=sys.stderr)
            return 2
        txt = json.dumps(g, indent=1, ensure_ascii=False, default=str)
        GATE_FILE.write_text(txt + "\n")
        recs = [{"written": g["written"], "tool": "yn2b/r2_def_literal_review.py", "key": KEY, "part": "r2_gate",
                 "path": str(GATE_FILE.relative_to(LEAN)), "rows": sum(v["rows"] for v in g["inputs"].values()),
                 "sha256": sha256(GATE_FILE), "inputs": g["inputs"], "tools": g["tools"],
                 "green": g["verdict"]["green"]}]
        if BLIND_FILE.exists():
            recs.append({"written": g["written"], "tool": "yn2b/r2_def_literal_review.py", "key": KEY,
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
