"""Reviewer R2 for F4 (gen3_polarity_ladder): blind-solve record, shortcut hunt, ambiguity hunt and the F4 gate
(yn2b/SPEC.md 8.1, 8.3, 8.4, 8.5).

Read-only on the family's rows. Nothing here labels a row: the gold comes from the generator (truth(P) XOR the
frame's flips, golden_src/gen3/gen3_polarity_ladder.py), the second opinion from builder C's decide2
(golden_src/gen3/v3_polarity_ladder.py), and the blind answers from R2 reading rendered rows only (state, card,
question, options). Text parsing reuses decide2's PARSERS (parse_frame, classify_p, card_parts); it never calls a
labelling function for a probe.

  printed / export_blind / blind_compare   the blind protocol (rows shown as the trainer prints them; key kept apart)
  shortcut_hunt(train, dev)                every cheap feature that could predict the answer on its own (SPEC 4.7,
                                           8.4): visible metadata strata, frame words, naive negation counting,
                                           lengths and numbers, the best single n-gram (chosen on one latent half,
                                           scored on the other), the TF-IDF probes, F4(a) label cues (label listed
                                           first, label-definition overlap with the text, label name in the text,
                                           per-label prior, card-neighbour structure) and the distractor cues the
                                           F4(b) states inherit (tool-output verdicts, logged verdicts, everyday
                                           usage, outside rules, recorded classifications, recorded decisions,
                                           agent records), scored both against the answer and against truth(P)
  ambiguity_hunt(rows)                     frame wordings with a second reading (SPEC 8.5c) and the readings F4(b)
                                           inherits from its source families
  decide2_check(rows, rels)                decide2 agreement, mv_core.verify_labels and the structure rules
  gate(...)                                the F4 gate table (yn2b/r2_polarity_ladder_gate.json)

Run from lean/:
  PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python yn2b/r2_polarity_ladder_review.py --export <dir> --seed N
  PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python yn2b/r2_polarity_ladder_review.py --gate [--write]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
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

KEY = "gen3_polarity_ladder"
RAW = LEAN / "data" / "v14_parts" / "yn2b_raw"
TRAIN_PATH = RAW / f"{KEY}.jsonl"
DEV_PATH = RAW / "dev" / f"{KEY}.jsonl"
REL_PATHS = {"train": RAW / "relations" / f"{KEY}.jsonl", "dev": RAW / "dev" / "relations" / f"{KEY}.jsonl"}
DEFS_DIR = LEAN / "data" / "v14_parts" / "yn2b_defs"
BLIND_FILE = YN2B / "r2_polarity_ladder_blind.json"
GATE_FILE = YN2B / "r2_polarity_ladder_gate.json"
MANIFEST = GEN3 / "MANIFEST_yn2b.jsonl"
GEN_FILES = ("gen3_polarity_ladder.py", "pl_frames.py", "pl_sources.py")
CAP = 0.60          # SPEC 4.7 / 8.4: no single shortcut above 60%
CAP_Q = 0.55        # SPEC 8.4: question-only TF-IDF
MIN_N = 40          # a cue / reader / subgroup is flagged only when it answers at least this many rows
SOURCE_DECIDE2 = {"f1": "v3_rule_chain", "f1b": "v3_rule_chain", "f2": "v3_tool_guard", "f3": "v3_state_track",
                  "f6": "v3_def_literal"}


# ================================================================================================ io
def sha256(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def read_jsonl(p: Path) -> list[dict]:
    return [json.loads(x) for x in Path(p).read_text().splitlines() if x.strip()]


def load_card(r: dict, defs_dir: Path | None = None) -> dict:
    """The row's card file (key order = card order), {} when it has none."""
    if r.get("_defs") is not None:
        return r["_defs"]
    q = (r.get("meta") or {}).get("defs")
    if not q:
        return {}
    p = Path(defs_dir or DEFS_DIR) / f"{KEY}__{q}.json"
    return json.loads(p.read_text()) if p.exists() else {}


def shown_card(r: dict, defs_dir: Path | None = None) -> dict:
    """The card as the model sees it: {} when card_style is none."""
    return {} if (r.get("meta") or {}).get("card_style") == "none" else load_card(r, defs_dir)


def _v3():
    import v3_polarity_ladder as v3
    return v3


def _mv():
    import mv_core as mv
    return mv


# ================================================================================================ blind solve
def printed(r: dict, defs_dir: Path | None = None) -> str:
    """The row as the trainer prints it (decoder_io cygnet layout, text first): state, the yes/no card as
    'Definitions:', the question, the options. No gold, no meta."""
    mv = _mv()
    g = mv.to_golden(r, load_card(r, defs_dir) or None)
    lines = [r["state"].rstrip(), ""]
    if g.get("card"):
        lines += ["Definitions:", g["card"], ""]
    lines += [r["instructions"].rstrip(), "", "Options:", "  0. yes", "  1. no"]
    return "\n".join(lines)


def export_blind(seed: int, out_dir: Path, n_train: int = 60, n_dev: int = 40, paths: dict | None = None,
                 defs_dir: Path | None = None) -> dict:
    """n_train random train + n_dev random dev_holdout rows, shuffled, as blind_rows.txt (bid headers only) and
    key.json (bid -> rid, gold) in out_dir (scratch, never data/). R2 answers from blind_rows.txt and freezes the
    answer file (sha256) before key.json is opened."""
    paths = paths or {"train": TRAIN_PATH, "dev": DEV_PATH}
    tr, dv = read_jsonl(paths["train"]), read_jsonl(paths["dev"])
    dh = [r for r in dv if r["meta"].get("dev_kind") == "holdout"]
    rng = random.Random(seed)
    items = [("T%02d" % i, r) for i, r in enumerate(rng.sample(tr, n_train))] + \
            [("D%02d" % i, r) for i, r in enumerate(rng.sample(dh, n_dev))]
    rng.shuffle(items)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "blind_rows.txt").write_text("\n\n".join(f"=================== {b} ===================\n"
                                                       f"{printed(r, defs_dir)}" for b, r in items) + "\n")
    (out_dir / "key.json").write_text(json.dumps({b: {"rid": r["rid"], "gold": r["gold"]} for b, r in items},
                                                 indent=1))
    return {"items": len(items), "train_sha256": sha256(paths["train"]), "dev_sha256": sha256(paths["dev"])}


def blind_compare(answers: dict, rows: list[dict]) -> dict:
    """answers: rid -> R2's blind answer ('yes' / 'no'). Rids missing from `rows` are reported as stale."""
    by = {r["rid"]: r for r in rows}
    out = {"n": 0, "agree": 0, "misses": [], "stale": []}
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
            out["misses"].append({"rid": rid, "blind": a, "gold": r["gold"], "renderer": r["meta"]["renderer"],
                                  "tpl": r["meta"]["tpl"]})
    out["rate"] = round(out["agree"] / max(1, out["n"]), 4)
    out["by_part"] = {p: {"agree": a, "n": n} for p, (a, n) in sorted(parts.items())}
    return out


# ================================================================================================ text reading
_CACHE: dict = {}


def read(r: dict) -> dict | None:
    """What a reader sees, parsed with decide2's text parsers (no labels): the frame, its switch words and flips,
    the proposition P and its kind. None when the text cannot be parsed (decide2_check reports such rows)."""
    k = (r["rid"], hashlib.sha1((r["state"] + r["instructions"]).encode()).hexdigest()[:10])
    if k in _CACHE:
        return _CACHE[k]
    v3 = _v3()
    try:
        fr = v3.parse_frame(r["instructions"])
        pr = v3.classify_p(fr.d)
    except Exception:            # noqa: BLE001
        _CACHE[k] = None
        return None
    sw = dict(fr.switches)
    out = {"frame": fr.name, "family": fr.family, "flips": fr.flips, "inner": fr.inner or "-",
           "act": sw.get("act", "-"), "ask": sw.get("ask", "-"), "P": fr.d, "kind": pr.kind,
           "groups": dict(pr.groups)}
    _CACHE[k] = out
    return out


def truth_of(r: dict) -> bool | None:
    """truth(P) recovered from the program gold and the parsed flips (analysis only: it scores cues against P)."""
    i = read(r)
    if i is None:
        return None
    return (r["gold"] == "yes") ^ (i["flips"] % 2 == 1)


def is_a(r: dict) -> bool:
    return r["meta"]["pack"] == "a"


def a_card(r: dict, defs_dir: Path | None = None) -> dict | None:
    """(a) rows: the quoted label L, the listed labels in card order and their definitions."""
    if not is_a(r):
        return None
    i = read(r)
    card = shown_card(r, defs_dir)
    if i is None or not card:
        return None
    parts = _v3().card_parts(card)
    labels = list(parts["extra"])
    return {"L": i["groups"].get("L"), "labels": labels, "defs": parts["extra"], "task": parts["task"]}


_W = re.compile(r"[a-z0-9]+")
_STOP = {"the", "a", "an", "of", "and", "or", "to", "in", "on", "for", "by", "with", "is", "are", "as", "at", "it",
         "its", "be", "this", "that", "not", "no", "such", "from", "any", "than", "but", "was", "were", "has", "had"}


def words(s: str) -> set:
    return {w for w in _W.findall(s.lower()) if w not in _STOP}


def jacc(a: str, b: str) -> float:
    wa, wb = words(a), words(b)
    return len(wa & wb) / max(1, len(wa | wb))


# ---- naive negation counting (the reader that ignores what P says and what each switch means)
NEGATORS = re.compile(r"\b(not|no|cannot|never|nothing|false|untrue)\b", re.I)
NEG_LEXICON = re.compile(
    r"\b(not|no|cannot|never|nothing|false|untrue|unsound|unjustified|unwarranted|unfounded|unmet|improper|improperly|"
    r"rejected|reject|refused|dismissed|denied|deny|excluded|blocked|stop|fail|misfire|defeat|defeated|overturn|"
    r"overturned|contradict|contradicted|changed|removed|dropped|strike|variance|break down|fall short|turned away|"
    r"give up|leave unmet|rule against|returned for revision)\b", re.I)


def naive_answers(r: dict) -> dict:
    q = r["instructions"]
    n1 = len(NEGATORS.findall(q))
    n2 = len(NEG_LEXICON.findall(q))
    return {"neg_parity_explicit": "yes" if n1 % 2 == 0 else "no",
            "neg_parity_lexicon": "yes" if n2 % 2 == 0 else "no",
            "any_negation_means_no": "no" if n2 else "yes"}


# ---- F4(b) distractor cues the copied states carry (each returns 'pos' / 'neg' / None, from the text alone)
_TOOL_ALLOW = re.compile(r"verdict ALLOW|approved to run|no issues found|is cleared to run|may proceed|ok to run", re.I)
_TOOL_BLOCK = re.compile(r"verdict BLOCK|must be blocked|must not run|should be blocked|is not allowed to run|"
                         r"denied by|rejected by the", re.I)
_GLOG = re.compile(r'"?guardrail_log"?\s*[:=]\s*"?(ALLOW|BLOCK)|guardrail (?:log|logged)[^.\n]*?\b(ALLOW|BLOCK)\b')
_USAGE_POS = re.compile(r"would (?:ordinarily )?call [^.\n]*?'[^']+'|would put [^.\n]*? down as|"
                        r"people would call|would call what happened", re.I)
_USAGE_NEG = re.compile(r"would not (?:ordinarily )?call|nobody would|would not put|nobody (?:informally )?calls|"
                        r"would not call", re.I)
_OUTSIDE = re.compile(r"Under (?:the |general |an? )?[^,\n]{3,80}?, (?:an? |the )?[a-z]+ (?:that|who|which) .+? is "
                      r"(not )?treated as (?:an? )?'[^']+'")
_RECORD = re.compile(r"[Rr]ecorded classification(?: for this file)?[\"']?\s*[:=]?\s*[\"']?(not )?(?:a |an )?'")
_DECISION = re.compile(r"decision recorded: ([^\n\"]+)|recorded decision[^:\n]*: ([^\n\"]+)", re.I)


def b_cues(r: dict) -> dict:
    """Distractor cues of an F4(b) state (from the text alone)."""
    s = r["state"]
    out = {}
    allow, block = bool(_TOOL_ALLOW.search(s)), bool(_TOOL_BLOCK.search(s))
    out["tool_says"] = "pos" if allow and not block else "neg" if block and not allow else (
        "both" if allow else None)
    m = _GLOG.search(s)
    out["logged_verdict"] = None if not m else ("pos" if "ALLOW" in m.group(0) else "neg")
    up, un = bool(_USAGE_POS.search(s)), bool(_USAGE_NEG.search(s))
    out["usage_says"] = "neg" if un else "pos" if up else None
    m = _OUTSIDE.search(s)
    out["outside_says"] = None if not m else ("neg" if m.group(1) else "pos")
    m = _RECORD.search(s)
    out["record_says"] = None if not m else ("neg" if m.group(1) else "pos")
    m = _DECISION.search(s)
    if m:
        d = (m.group(1) or m.group(2) or "").lower()
        out["decision_says"] = "neg" if any(w in d for w in ("refused", "rejected", "denied", "not ", "declined")) \
            else "pos"
    else:
        out["decision_says"] = None
    out["agent_record"] = "yes" if re.search(r"[Aa]gent record|agent_record\"?: \{|agent_record\"?: \[", s) else None
    return out


def b_p_features(r: dict) -> dict:
    """Features of P's own wording (F4(b)): the outcome class named (F1), the F3 predicate and comparator."""
    i = read(r)
    if i is None or is_a(r):
        return {}
    P = i["P"]
    out = {}
    if i["kind"] == "f1.outcome":
        x = i["groups"].get("x", "").lower()
        out["f1_outcome_class"] = ("refused" if any(w in x for w in ("refused", "rejected", "not covered", "no "))
                                   else "granted" if any(w in x for w in ("paid", "granted", "covered", "approved",
                                                                          "full", "capped", "limit"))
                                   else "other")
    if i["kind"] == "f3.state":
        cmp_ = next((c for c in ("at least", "fewer than", "less than", "below", "more than", "exactly", "is in status",
                                 "is approved", "is on for", "is in the", "content", "holds the confirmed")
                     if c in P), "other")
        out["f3_pred"] = cmp_
        m = re.search(r"\b(\d+(?:\.\d+)?)\b", P.replace(",", ""))
        out["f3_has_number"] = "yes" if m else "no"
    return out


# ================================================================================================ features
VISIBLE_META = ("fmt", "tpl", "renderer", "pack", "card_style", "len_bin", "polarity", "role", "view", "judge")
HIDDEN_META = ("tier", "n_shortcut_wrong", "edge", "plant_dir", "none_option", "levels")


def cat_features(r: dict, defs_dir: Path | None = None) -> dict:
    m = r["meta"]
    f = {k: str(m.get(k)) for k in VISIBLE_META + HIDDEN_META}
    f["fmt"] = str(m.get("fmt")).split(":")[0]
    f["quad"] = m["tpl"].split(".")[0]
    f["cell"] = m["tpl"].split(".")[1]
    f["source_kind"] = "a" if is_a(r) else "b"
    f["coarse_pack"] = m["pack"].split(".")[0]
    i = read(r)
    if i:
        f.update(frame=i["frame"], family=i["family"], inner=i["inner"], act=i["act"], ask=i["ask"], p_kind=i["kind"])
        f["renderer_x_cell"] = f"{m['renderer']}|{f['cell']}"
        f["frame_x_inner"] = f"{i['frame']}|{i['inner']}"
    a = a_card(r, defs_dir)
    if a:
        f["a_label"] = f"{m['renderer']}|{a['L']}"
        f["a_n_labels"] = str(len(a["labels"]))
        f["a_L_pos"] = str(a["labels"].index(a["L"])) if a["L"] in a["labels"] else "?"
        f["a_L_pos_x_n"] = f"{f['a_L_pos']}/{f['a_n_labels']}"
    if not is_a(r):
        for k, v in b_cues(r).items():
            if v is not None:
                f["cue_" + k] = f"{m['renderer']}|{v}"
        for k, v in b_p_features(r).items():
            f[k] = f"{m['renderer']}|{v}"
    for t in (m.get("edge") or "").split(","):
        if t:
            f["edge:" + t] = "1"
    return f


def report_only(key: str) -> bool:
    """Tags a model cannot read (tier, shortcut counts, edge tags): reported, never flagged."""
    return key in HIDDEN_META or key.startswith("edge:")


def _nums(t: str) -> list:
    return [float(x.replace(",", "")) for x in re.findall(r"\d[\d,]*(?:\.\d+)?", t)]


def num_features(r: dict, defs_dir: Path | None = None) -> dict:
    s, q = r["state"], r["instructions"]
    card = shown_card(r, defs_dir)
    out = {"len_state": len(s), "len_q": len(q), "n_lines": s.count("\n") + 1, "n_digits_q": len(re.findall(r"\d", q)),
           "n_card_lines": len(card), "len_card": sum(len(k) + len(v) for k, v in card.items()),
           "n_neg_explicit": len(NEGATORS.findall(q)), "n_neg_lexicon": len(NEG_LEXICON.findall(q))}
    i = read(r)
    if i:
        out["len_P"] = len(i["P"])
        ns = _nums(i["P"])
        if ns:
            out["p_number"] = ns[-1]
    a = a_card(r, defs_dir)
    if a:
        out["a_n_labels"] = len(a["labels"])
    return out


NUM_KEYS = ("len_state", "len_q", "n_lines", "n_digits_q", "n_card_lines", "len_card", "n_neg_explicit",
            "n_neg_lexicon", "len_P", "p_number", "a_n_labels")


# ================================================================================================ probes
def gold_t(r: dict):
    return r["gold"]


def truth_t(r: dict):
    t = truth_of(r)
    return None if t is None else ("P" if t else "notP")


def _halves(rows):
    """Two halves by latent (both rows of a unit stay together), deterministic."""
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
    return {x: sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[0][0] for x, c in by.items()}, glob


def cat_probe(train, test, feat, target=gold_t) -> dict:
    """'Predict the majority target of this feature value': fit on train (rows with the feature), scored in-sample
    and on test (rows with the feature)."""
    tr = [(feat(r), target(r)) for r in train]
    tr = [(x, y) for x, y in tr if x is not None and y is not None]
    te = [(feat(r), target(r)) for r in test]
    te = [(x, y) for x, y in te if x is not None and y is not None]
    if not tr or len({y for _, y in tr}) < 2:
        return {"in_sample": None, "held_out": None, "values": 0, "n": len(tr), "n_test": len(te)}
    tab, glob = _fit_cat([x for x, _ in tr], [y for _, y in tr])
    return {"in_sample": round(_acc([tab[x] for x, _ in tr], [y for _, y in tr]), 4),
            "held_out": round(_acc([tab.get(x, glob) for x, _ in te], [y for _, y in te]), 4) if te else None,
            "values": len(tab), "n": len(tr), "n_test": len(te)}


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


def num_probe(train, test, key, target=gold_t, defs_dir=None) -> dict | None:
    tr = [(num_features(r, defs_dir).get(key), target(r)) for r in train]
    tr = [(x, y) for x, y in tr if x is not None and y is not None]
    te = [(num_features(r, defs_dir).get(key), target(r)) for r in test]
    te = [(x, y) for x, y in te if x is not None and y is not None]
    if len(tr) < 20 or len({y for _, y in tr}) != 2:
        return None
    a, t, hi, lo = _best_cut([x for x, _ in tr], [y for _, y in tr])
    held = _acc([hi if x >= t else lo for x, _ in te], [y for _, y in te]) if te else None
    return {"in_sample": round(a, 4), "held_out": None if held is None else round(held, 4), "cut": t, "n": len(tr),
            "n_test": len(te)}


_TOK = re.compile(r"[a-z]+|\d+")


def ngrams(text: str, n_max: int = 3) -> set:
    w = _TOK.findall(text.lower())
    out = set()
    for n in range(1, n_max + 1):
        out |= {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}
    return out


def _text(r, field, defs_dir=None):
    if field == "state":
        return r["state"]
    if field == "card":
        return " ".join(f"{k}: {v}" for k, v in shown_card(r, defs_dir).items())
    if field == "P":
        i = read(r)
        return i["P"] if i else ""
    return r["instructions"]


def ngram_probe(rows, field="state", target=gold_t, min_df=0.02, top=5, defs_dir=None) -> dict:
    """The best single n-gram (presence -> majority target), chosen on one latent half and scored on the other
    (both directions; no selection on the scored half)."""
    rows = [r for r in rows if target(r) is not None]
    a, b = _halves(rows)
    res = {}
    for name, (fit, ev) in {"a->b": (a, b), "b->a": (b, a)}.items():
        docs = [ngrams(_text(r, field, defs_dir)) for r in fit]
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
        edocs = [ngrams(_text(r, field, defs_dir)) for r in ev]
        ey = [target(r) for r in ev]
        held = _acc([best[2].get(best[1] in d, best[3]) for d in edocs], ey) if best[1] else None
        res[name] = {"chosen": best[1], "fit_acc": round(best[0], 4),
                     "held_out": None if held is None else round(held, 4),
                     "top_in_sample": [(round(s, 4), g_) for s, g_, _, _ in scored[:top]]}
    res["held_out_mean"] = round(sum(v["held_out"] or 0 for v in res.values() if isinstance(v, dict)) / 2, 4)
    return res


def tfidf_probe(train, test, field, target=gold_t, defs_dir=None) -> dict | None:
    """SPEC 8.4 TF-IDF 1-2-gram logistic regression, fit on train rows, scored on test rows. 'state+question' is
    everything the model reads: the state, the shown card, the question and the options."""
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
    except ImportError:          # pragma: no cover
        return None
    train = [r for r in train if target(r) is not None]
    test = [r for r in test if target(r) is not None]
    if len({target(r) for r in train}) < 2 or not test:
        return None

    def txt(r):
        if field == "question":
            return r["instructions"]
        if field == "P":
            return _text(r, "P")
        return (r["state"] + "\n" + _text(r, "card", defs_dir) + "\n" + r["instructions"] + "\n" +
                " | ".join(r["options"]))
    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=200000, sublinear_tf=True)
    X = vec.fit_transform([txt(r) for r in train])
    clf = LogisticRegression(max_iter=3000, C=1.0)
    clf.fit(X, [target(r) for r in train])
    pred = clf.predict(vec.transform([txt(r) for r in test]))
    yt = [target(r) for r in test]
    maj = Counter(target(r) for r in train).most_common(1)[0][0]
    return {"acc": round(_acc(list(pred), yt), 4), "majority": round(_acc([maj] * len(yt), yt), 4),
            "n_train": len(train), "n_test": len(yt)}


# ---- readers: each answers 'yes'/'no' (or truth 'P'/'notP') where its cue is present
def a_readers(rows, defs_dir=None) -> dict:
    """F4(a) label cues, scored against truth(P) (L is the human gold) on every (a) row:
      listed_first      L is the first label the card lists
      overlap_def       L's card definition shares the most words with the text (Jaccard)
      label_in_text     L's name words occur in the text more than any other listed label's
      nn_mutual         L and its nearest card neighbour (definition overlap) are each other's nearest neighbour
      nn_of_other       L is the nearest card neighbour of some other listed label
    and, with the parsed flips, against the answer (the same accuracy: flips are exact)."""
    hit, cov = Counter(), Counter()
    for r in rows:
        a = a_card(r, defs_dir)
        t = truth_of(r)
        if not a or t is None or a["L"] not in a["labels"]:
            continue
        L, labs, D, s = a["L"], a["labels"], a["defs"], r["state"]
        preds = {"listed_first": labs[0] == L}
        ov = {o: jacc(D[o], s) for o in labs}
        top = [o for o, v in ov.items() if v == max(ov.values())]
        if len(top) == 1:
            preds["overlap_def"] = top[0] == L
        sw = words(s)
        nm = {o: len(words(o) & sw) for o in labs}
        topn = [o for o, v in nm.items() if v == max(nm.values())]
        if max(nm.values()) > 0 and len(topn) == 1:
            preds["label_in_text"] = topn[0] == L

        def nn(x):
            others = [o for o in labs if o != x]
            return max(others, key=lambda o: (jacc(D[x], D[o]), o)) if others else None
        if len(labs) >= 2:
            n1 = nn(L)
            preds["nn_mutual"] = n1 is not None and nn(n1) == L
            preds["nn_of_other"] = any(nn(o) == L for o in labs if o != L)
        for k, p in preds.items():
            cov[k] += 1
            hit[k] += (p == t)
    return {k: {"acc": round(hit[k] / cov[k], 4), "n": cov[k]} for k in sorted(cov)}


def b_readers(rows) -> dict:
    """F4(b) distractor cues, scored against truth(P) where the cue is present and bears on P's kind:
      tool_says (f2.may: a tool output that says ALLOW / BLOCK), logged_verdict (f2.verdict: the logged verdict is
      ALLOW), usage_says / outside_says (f6.term: everyday usage / an outside rule book says it is the term),
      record_says (f6.term: the register says it is), decision_says (f1.record: the recorded decision grants).
    'follow' = the cue's direction is P's truth; its accuracy is reported (|acc - 0.5| matters, either direction
    is a learnable shortcut)."""
    rel = {"tool_says": ("f2.may",), "logged_verdict": ("f2.verdict",), "usage_says": ("f6.term",),
           "outside_says": ("f6.term",), "record_says": ("f6.term",), "decision_says": ("f1.record",)}
    hit, cov = Counter(), Counter()
    for r in rows:
        if is_a(r):
            continue
        t = truth_of(r)
        if t is None:
            continue
        c = b_cues(r)
        for k, kinds in rel.items():
            v = c.get(k)
            if v not in ("pos", "neg") or r["meta"]["renderer"] not in kinds:
                continue
            cov[k] += 1
            hit[k] += ((v == "pos") == t)
    return {k: {"follow_acc": round(hit[k] / cov[k], 4), "n": cov[k],
                "best_direction_acc": round(max(hit[k], cov[k] - hit[k]) / cov[k], 4)} for k in sorted(cov)}


def naive_probe(rows) -> dict:
    out = {}
    hit, n = Counter(), Counter()
    for r in rows:
        for k, a in naive_answers(r).items():
            n[k] += 1
            hit[k] += a == r["gold"]
    for k in sorted(n):
        out[k] = {"acc": round(hit[k] / n[k], 4), "n": n[k]}
    return out


def solver_probe(rows) -> dict:
    """The generator's named shortcut solvers (meta.shortcut_hits: 1 = the solver gives gold; absent = abstains)."""
    acc = defaultdict(lambda: [0, 0])
    for r in rows:
        for k, v in (r["meta"].get("shortcut_hits") or {}).items():
            acc[k][0] += v
            acc[k][1] += 1
    return {k: {"acc": round(h / n, 4), "n": n} for k, (h, n) in sorted(acc.items())}


def balance_tables(rows) -> dict:
    """Yes share per visible stratum and truth(P) share per (renderer) and per (a) label (report)."""
    ys = defaultdict(lambda: [0, 0])
    ts = defaultdict(lambda: [0, 0])
    for r in rows:
        f = cat_features(r)
        for k in ("quad", "tpl", "renderer", "family", "fmt", "card_style", "len_bin", "polarity", "source_kind"):
            ys[f"{k}={f.get(k)}"][0] += r["gold"] == "yes"
            ys[f"{k}={f.get(k)}"][1] += 1
        t = truth_of(r)
        if t is not None:
            for k in ("renderer", "a_label", "coarse_pack"):
                if k in f:
                    ts[f"{k}={f[k]}"][0] += t
                    ts[f"{k}={f[k]}"][1] += 1
    worst = lambda d, mn: sorted(((round(a / n, 4), n, k) for k, (a, n) in d.items() if n >= mn),  # noqa: E731
                                 key=lambda x: -abs(x[0] - 0.5))[:12]
    return {"yes_share_extremes": worst(ys, 20), "truth_share_extremes": worst(ts, 20)}


def shortcut_hunt(train: list[dict], dev: list[dict], defs_dir: Path | None = None) -> dict:
    out = {"rows_train": len(train), "rows_dev": len(dev),
           "yes_share_train": round(sum(r["gold"] == "yes" for r in train) / max(1, len(train)), 4),
           "yes_share_dev": round(sum(r["gold"] == "yes" for r in dev) / max(1, len(dev)), 4)}
    a, b = _halves(train)
    feats = {id(r): cat_features(r, defs_dir) for r in train + dev}
    keys = sorted({k for r in train for k in feats[id(r)]})
    out["categorical"] = {}
    for k in keys:
        feat = (lambda r, k=k: feats[id(r)].get(k))
        e = {"gold half->half": cat_probe(a, b, feat), "gold b->a": cat_probe(b, a, feat),
             "gold train->dev": cat_probe(train, dev, feat),
             "truth half->half": cat_probe(a, b, feat, truth_t), "truth b->a": cat_probe(b, a, feat, truth_t)}
        out["categorical"][k] = e
    out["numeric"] = {k: {"gold half->half": num_probe(a, b, k, defs_dir=defs_dir),
                          "gold train->dev": num_probe(train, dev, k, defs_dir=defs_dir),
                          "truth half->half": num_probe(a, b, k, truth_t, defs_dir)} for k in NUM_KEYS}
    out["ngram"] = {"state": ngram_probe(train, "state", defs_dir=defs_dir),
                    "question": ngram_probe(train, "question", defs_dir=defs_dir),
                    "card": ngram_probe(train, "card", defs_dir=defs_dir),
                    "P->truth": ngram_probe(train, "P", truth_t, defs_dir=defs_dir),
                    "state->truth": ngram_probe(train, "state", truth_t, defs_dir=defs_dir)}
    out["tfidf"] = {"state+question train->dev": tfidf_probe(train, dev, "all", defs_dir=defs_dir),
                    "question train->dev": tfidf_probe(train, dev, "question"),
                    "state+question half->half": tfidf_probe(a, b, "all", defs_dir=defs_dir),
                    "question half->half": tfidf_probe(a, b, "question"),
                    "P->truth half->half": tfidf_probe(a, b, "P", truth_t),
                    "state->truth half->half": tfidf_probe(a, b, "all", truth_t, defs_dir)}
    sub = {"a": [r for r in train if is_a(r)], "b": [r for r in train if not is_a(r)]}
    out["subgroup_tfidf"] = {}
    for g, rows in sub.items():
        ga, gb = _halves(rows)
        out["subgroup_tfidf"][g] = {"state+question half->half": tfidf_probe(ga, gb, "all", defs_dir=defs_dir),
                                    "state->truth half->half": tfidf_probe(ga, gb, "all", truth_t, defs_dir)}
    out["readers"] = {"naive_train": naive_probe(train), "naive_dev": naive_probe(dev),
                      "a_truth_train": a_readers(train, defs_dir), "b_truth_train": b_readers(train),
                      "b_truth_dev": b_readers(dev)}
    out["solvers"] = {"train": solver_probe(train), "dev": solver_probe(dev)}
    out["balance"] = {"train": balance_tables(train), "dev": balance_tables(dev)}
    out["flags"] = flags(out)
    return out


def flags(rep: dict) -> list:
    """Every probe above CAP on held-out rows (MIN_N rows at least); question-only TF-IDF above CAP_Q. Hidden tags
    (tier, n_shortcut_wrong, edge) go to report_only."""
    bad = []
    rep["report_only"] = []
    for k, v in rep["categorical"].items():
        for how, x in v.items():
            if x.get("held_out") is not None and x["held_out"] > CAP and x.get("n_test", 0) >= MIN_N:
                (rep["report_only"] if report_only(k) else bad).append(("cat", k, how, x["held_out"], x["n_test"]))
    for k, v in rep["numeric"].items():
        for how, x in v.items():
            if x and x.get("held_out") is not None and x["held_out"] > CAP and x.get("n_test", 0) >= MIN_N:
                bad.append(("num", k, how, x["held_out"], x["n_test"]))
    for k, v in rep["ngram"].items():
        if v["held_out_mean"] > CAP:
            bad.append(("ngram", k, "half->half", v["held_out_mean"]))
    for k, x in rep["tfidf"].items():
        lim = CAP_Q if k.startswith("question") else CAP
        if x and x["acc"] > lim:
            bad.append(("tfidf", k, "", x["acc"]))
    for g, d in rep["subgroup_tfidf"].items():
        for k, x in d.items():
            if x and x["acc"] > CAP:
                bad.append(("tfidf", f"{g}:{k}", "", x["acc"]))
    for part in ("naive_train", "naive_dev"):
        for k, x in rep["readers"][part].items():
            if x["acc"] > CAP:
                bad.append(("reader", k, part, x["acc"]))
    for k, x in rep["readers"]["a_truth_train"].items():
        if x["n"] >= MIN_N and abs(x["acc"] - 0.5) > CAP - 0.5:
            bad.append(("a_reader", k, "train", x["acc"], x["n"]))
    for part in ("b_truth_train", "b_truth_dev"):
        for k, x in rep["readers"][part].items():
            if x["n"] >= MIN_N and x["best_direction_acc"] > CAP:
                bad.append(("b_cue", k, part, x["best_direction_acc"], x["n"]))
    for part, s in rep["solvers"].items():
        for k, x in s.items():
            if x["acc"] > CAP and x["n"] >= MIN_N:
                bad.append(("solver", k, part, x["acc"], x["n"]))
    return bad


# ================================================================================================ ambiguity hunt
# Frame wordings with a second reading under which the gold flips (SPEC 8.5c). Each entry: a regex on the rendered
# question, the second reading, and which rows it affects. The first build had two in training frames; the fixed
# pl_frames words them so that the second reading is gone (the regexes then find 0 rows).
AMBIG_FRAMES = {
    "gk2_clear": (re.compile(r"would it be (?:im)?proper to clear this case\?$"),
                  "'clear this case' read as 'close / dismiss the case' (= stop it) instead of 'let it proceed'"),
    "cf1_flag_warranted": (re.compile(r"flagged this file with the note that .+ is that flag (?:un)?warranted\?$"),
                           "'is that flag warranted' read as 'does the file have a compliance problem' instead of "
                           "'is the flagged note true' (they differ when P itself states that something is in order)"),
}
# Readings that were examined and kept (the card and the format note settle them; listed with their row counts).
KEPT_READINGS = {
    "nothing_supports_strict": (re.compile(r"nothing supports the idea that"),
                                "dev_holdout only: 'nothing supports the idea that P' read strictly (a P that fails "
                                "on one rule still has some supporting facts). Kept: every F4 P is a program decision "
                                "that the material establishes or rules out, and the held-out frames are report-only"),
    "proof_of_a_human_label": (re.compile(r"demand for proof that|is it established that|Read strictly, does the "
                                          r"material given show"),
                               "(a) rows: 'proof' / 'established' / 'read strictly' of a human judgement label. Kept: "
                               "the card defines the statement as 'L fits better than any other listed label', so "
                               "proof of the statement is proof of that comparison"),
}


def ambiguity_hunt(rows: list[dict]) -> dict:
    out = {"frames": {}, "kept": {}}
    for k, (rx, why) in AMBIG_FRAMES.items():
        hit = [r for r in rows if rx.search(r["instructions"])]
        out["frames"][k] = {"rows": len(hit), "why": why, "examples": [r["rid"] for r in hit[:6]]}
    for k, (rx, why) in KEPT_READINGS.items():
        hit = [r for r in rows if rx.search(r["instructions"]) and
               (k != "proof_of_a_human_label" or is_a(r))]
        if k == "nothing_supports_strict":
            hit = [r for r in hit if truth_of(r) is False]
        out["kept"][k] = {"rows": len(hit), "why": why}
    out["frames_ok"] = all(v["rows"] == 0 for v in out["frames"].values())
    return out


def f3_count_revert_reading(rows: list[dict], sources: dict) -> dict:
    """Inherited F3 reading (outside F4's files): a revert of a cycle count. The rule says 'a cycle count's on-hand
    number goes back to what it was just before the count. Later events keep their effect.' F3's generator and F3's
    decide2 both set on-hand back to the pre-count number (the specific clause); the other reading keeps later
    receipts / shipments (on-hand += before - counted). Counts the F4(b) rows on F3 stock states whose truth(P)
    changes under that reading (F3's own decide2, patched only inside this function)."""
    import v3_state_track as st
    cls = getattr(st, "StockSim", None) or getattr(st, "InventorySim", None)
    if cls is None:
        return {"error": "F3 stock simulator class not found"}
    want = {}
    for r in rows:
        s = sources.get(r["meta"]["latent_id"]) or {}
        if s.get("kind") == "b" and s.get("src_key") == "gen3_state_track":
            want[s["src_rid"]] = r
    import mv_core as mv
    src_rows = {}
    for part in ("train", "dev"):
        for r in mv.read_raw("gen3_state_track", part)[0]:
            if r["rid"] in want and re.search(r"Cycle count|Shelf count|count sku=", r["state"]):
                src_rows[r["rid"]] = r
    orig = cls.apply

    def alt(self, e, kind, g):
        if kind == "revert":
            ref = g["ref"]
            rec = self.log.get(ref)
            if rec and rec[0] == "count" and ref in self.done and ref not in self.reverted:
                sku = rec[1]["sku"]
                cur = self.on[sku]
                ok = orig(self, e, kind, g)
                self.on[sku] = max(0, cur + rec[1]["before"] - rec[1].get("counted", rec[1]["before"]))
                return ok
        res = orig(self, e, kind, g)
        if kind == "count" and res and e.eid in self.log:
            self.log[e.eid][1]["counted"] = int(g["n"])
        return res
    changed, n = [], 0
    try:
        for rid, r in src_rows.items():
            a0 = st.decide2_row(r)
            cls.apply = alt
            try:
                a1 = st.decide2_row(r)
            finally:
                cls.apply = orig
            n += 1
            if a0 != a1:
                changed.append({"f4_rid": want[rid]["rid"], "src_rid": rid, "src_gold": r["gold"],
                                "primary": str(a0), "alt": str(a1)})
    finally:
        cls.apply = orig
    return {"f4_rows_on_stock_states_with_a_count": n, "truth_changes_under_alt": len(changed),
            "gold_follows": "primary (the clause names the cycle count: on-hand goes back to the pre-count number)",
            "rows": changed}


# ================================================================================================ decide2
def decide2_check(rows: list[dict], rels: list[dict]) -> dict:
    v3 = _v3()
    mv = _mv()
    ag = v3.agreement(rows)
    st = v3.structure_under_decide2(rows, rels, ag["answers"])
    vl = mv.verify_labels(rows, v3.decide2_row)
    return {"rows": ag["rows"], "agree": ag["agree"], "rate": ag["rate"],
            "disagreements": ag["disagreements"][:20], "verify_labels": vl,
            "structure": {"complement": st["complement"], "equiv": st["equiv"],
                          "complement_not_inverted": len(st["complement_not_inverted"]),
                          "equiv_changed": len(st["equiv_changed"]), "unknown_rel": len(st["unknown_rel"]),
                          "same_state_broken": len(st["same_state_broken"])},
            "ok": ag["agree"] == ag["rows"] and vl["ok"] and not st["complement_not_inverted"] and
            not st["equiv_changed"] and not st["unknown_rel"] and not st["same_state_broken"]}


def mv_checks(rows, rels) -> dict:
    rep = _mv().run_checks(rows, rels)
    return {k: v.get("ok") for k, v in rep.items() if isinstance(v, dict) and "ok" in v and k != "summary"}


# ================================================================================================ gate
def counts(rows: list[dict]) -> dict:
    c = lambda f: dict(sorted(Counter(f(r) for r in rows).items()))  # noqa: E731
    return {"rows": len(rows), "latents": len({r["meta"]["latent_id"] for r in rows}),
            "yes_share": round(sum(r["gold"] == "yes" for r in rows) / max(1, len(rows)), 4),
            "by_source_kind": c(lambda r: "a" if is_a(r) else "b"), "by_view": c(lambda r: r["meta"]["view"]),
            "by_polarity": c(lambda r: r["meta"]["polarity"]), "by_tier": c(lambda r: r["meta"]["tier"]),
            "by_renderer": c(lambda r: r["meta"]["renderer"]),
            "by_family": c(lambda r: (read(r) or {}).get("family")),
            "by_dev_kind": c(lambda r: str(r["meta"].get("dev_kind"))),
            "by_card_style": c(lambda r: r["meta"]["card_style"])}


def gate(paths: dict | None = None, blind: dict | None = None, tests: dict | None = None,
         defs_dir: Path | None = None) -> dict:
    paths = paths or {"train": TRAIN_PATH, "dev": DEV_PATH}
    tr, dv = read_jsonl(paths["train"]), read_jsonl(paths["dev"])
    rels = {p: read_jsonl(REL_PATHS[p]) for p in ("train", "dev")}
    srcs = json.loads((YN2B / "f4_sources.json").read_text())["latents"]
    g = {"written": datetime.now(timezone.utc).isoformat(timespec="seconds"),
         "inputs": {p: {"path": str(Path(paths[p]).relative_to(LEAN)), "rows": len(x), "sha256": sha256(paths[p])}
                    for p, x in (("train", tr), ("dev", dv))},
         "tools": {"generator_sha256": {f: sha256(GEN3 / f) for f in GEN_FILES},
                   "decide2_sha256": sha256(GEN3 / "v3_polarity_ladder.py"),
                   "review_sha256": sha256(Path(__file__))},
         "counts": {"train": counts(tr), "dev": counts(dv)}}
    g["decide2"] = {"train": decide2_check(tr, rels["train"]), "dev": decide2_check(dv, rels["dev"])}
    g["mv_core_checks"] = {"train": mv_checks(tr, rels["train"]), "dev": mv_checks(dv, rels["dev"])}
    g["shortcuts"] = shortcut_hunt(tr, dv, defs_dir)
    g["ambiguity"] = {"train": ambiguity_hunt(tr), "dev": ambiguity_hunt(dv),
                      "inherited_f3_count_revert": f3_count_revert_reading(tr + dv, srcs)}
    g["blind"] = blind
    g["tests"] = tests
    g["verdict"] = verdict(g)
    return g


def verdict(g: dict) -> dict:
    why = []
    for p in ("train", "dev"):
        if not g["decide2"][p]["ok"]:
            why.append(f"decide2 {p}: {g['decide2'][p]['agree']}/{g['decide2'][p]['rows']}")
        bad = [k for k, v in g["mv_core_checks"][p].items() if v is False and not (p == "dev" and k == "artefacts")]
        if bad:
            why.append(f"mv_core {p}: {bad}")
        if not g["ambiguity"][p]["frames_ok"]:
            why.append(f"ambiguous frame wordings in {p}: "
                       f"{ {k: v['rows'] for k, v in g['ambiguity'][p]['frames'].items() if v['rows']} }")
    if g["shortcuts"]["flags"]:
        why.append(f"shortcut flags: {g['shortcuts']['flags']}")
    b = g.get("blind") or {}
    fin = (b.get("final") or {})
    if not fin:
        why.append("no blind-solve record")
    else:
        if fin.get("rate", 0) < 0.97:
            why.append(f"blind solve {fin.get('agree')}/{fin.get('n')} < 97%")
        if fin.get("unexplained_misses"):
            why.append(f"unexplained blind misses: {fin['unexplained_misses']}")
        if fin.get("open_generator_bugs"):
            why.append(f"open generator bugs: {fin['open_generator_bugs']}")
    t = g.get("tests") or {}
    if not t or t.get("failed", 1) != 0:
        why.append(f"tests: {t}")
    return {"green": not why, "reasons": why}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--export", default="", help="write a blind sample (blind_rows.txt + key.json) to this dir")
    ap.add_argument("--seed", type=int, default=20261011)
    ap.add_argument("--gate", action="store_true", help="compute the gate (prints the verdict)")
    ap.add_argument("--write", action="store_true", help="with --gate: write yn2b/r2_polarity_ladder_gate.json")
    ap.add_argument("--tests", default="", help="JSON file with the test-run record to embed")
    a = ap.parse_args(argv)
    if a.export:
        print(json.dumps(export_blind(a.seed, Path(a.export)), indent=1))
    if a.gate:
        blind = json.loads(BLIND_FILE.read_text()) if BLIND_FILE.exists() else None
        tests = json.loads(Path(a.tests).read_text()) if a.tests else None
        g = gate(blind=blind, tests=tests)
        print(json.dumps({"verdict": g["verdict"], "flags": g["shortcuts"]["flags"],
                          "decide2": {p: (g["decide2"][p]["agree"], g["decide2"][p]["rows"]) for p in g["decide2"]},
                          "ambiguity": {p: g["ambiguity"][p] for p in ("train", "dev")}}, indent=1, default=str))
        if a.write:
            GATE_FILE.write_text(json.dumps(g, indent=1, default=str) + "\n")
            print("wrote", GATE_FILE, sha256(GATE_FILE))
            mv = _mv()
            inputs = {p: g["inputs"][p]["sha256"] for p in ("train", "dev")}
            mv.manifest_append({"written": g["written"], "tool": "yn2b/r2_polarity_ladder_review.py", "key": KEY,
                                "part": "r2_gate", "path": str(GATE_FILE.relative_to(LEAN)),
                                "rows": sum(g["inputs"][p]["rows"] for p in ("train", "dev")),
                                "sha256": sha256(GATE_FILE), "inputs": inputs, "green": g["verdict"]["green"]},
                               MANIFEST)
            if BLIND_FILE.exists():
                mv.manifest_append({"written": g["written"], "tool": "yn2b/r2_polarity_ladder_review.py", "key": KEY,
                                    "part": "r2_blind", "path": str(BLIND_FILE.relative_to(LEAN)),
                                    "sha256": sha256(BLIND_FILE),
                                    "rows": sum(r["n"] for r in (blind or {}).get("rounds", [])),
                                    "inputs": inputs}, MANIFEST)
    return 0


if __name__ == "__main__":
    sys.exit(main())
