#!/usr/bin/env python
"""f7_v1_adapter.py: derives the F7 sidecar meta (the f7_precheck contract) for F7 v1, which was built before the
contract existed and ships no sidecar.

F7 v1 = data/v14_parts/f7_train.jsonl (2,030 ladders x 5 rows) + f7_probe.jsonl (598 ladders x 3 rows), built by
golden_src/gen3/gen3_nested_negation.py. This adapter never imports that generator or its lexicon. It reads the rows'
own meta (kind, sense, truth_cplus, claim, frame, rung, spec / pack, n_items / n_x, x_holds / target_is_gold) and
data/v14_parts/f7_defs.json (the generator's dumped wording tables), and it rebuilds each row's logical form from a
hand-written reading of every v1 claim template (LAYERS below: the negation layers between the claim and its base fact
P, outer to inner). The precheck then re-evaluates that LF on its own; a reading error shows up there as LF != gold.

What cannot be derived from v1 is left out on purpose (the precheck reports it as missing): no antonym_gold (v1 has no
item-21 antonym label sets), no curated lexicon file, no holdout spec, no devx, no blind read. State negations are not
listed as cues (v1 never placed them on purpose); the rows are tagged with item 19 instead.

Writes (new files, into --out-dir, default the session scratchpad given on the command line):
  v1_meta.jsonl, v1_probe_meta.jsonl, v1_decide2_preds.jsonl (v1's own decide2, golden_src/gen3/v3_nested_negation.py,
  run with the golden base rows; NOT an independent decide2).

  cd opendecide-data/lean && PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python yn2b/f7_v1_adapter.py --out-dir <dir>
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

LEAN = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
D = LEAN / "data" / "v14_parts" / "f7_v1_backup"   # F7 v1 lives here since v2 was written (round-3 repair)

SYN, AFF, LEX, TRU = "syntactic", "affixal", "lexical", "truth_frame"
NONX, IMPL, IMPL_Y = "NONX", "IMPLICIT", "IMPLICIT_Y"   # resolved per row (non- / -free affix, or an antonym word)
NOT_ = ("not", SYN, "not")
# (C+ layers, C- layers), outer -> inner; each layer = (lexeme, class, surface) or a marker resolved per row
LAYERS = {
    "m_plain": ([], [NOT_]),
    "m_only_other": ([("other than", LEX, "other than")], [NOT_, ("other than", LEX, "other than")]),
    "m_any_other": ([("other than", LEX, "other than")], [NOT_, ("other than", LEX, "other than")]),
    "m_fails": ([], [("fail", LEX, "fails")]),
    "m_non": ([("non-", AFF, "non-")], [NOT_, ("non-", AFF, "non-")]),
    "m_none_of": ([("none", SYN, "none"), ("other than", LEX, "other than")], [("other than", LEX, "other than")]),
    "pm_solely": ([("other than", LEX, "other than")], [NOT_, ("other than", LEX, "other than")]),
    "pm_outside": ([("outside", LEX, "outside"), ("except", LEX, "except")],
                   [NOT_, ("outside", LEX, "outside"), ("except", LEX, "except")]),
    "p_plain": ([], [NOT_]),
    "p_only_non": ([NONX], [NOT_, NONX]),
    "p_free": ([("free of", LEX, "free of")], [NOT_, ("free of", LEX, "free of")]),
    "p_any": ([], [NOT_]),
    "p_lacks": ([], [("lack", LEX, "lacks")]),
    "p_none": ([], [("none", SYN, "none")]),
    "p_xfree": ([("-free", AFF, "XFREE")], [NOT_, ("-free", AFF, "XFREE")]),
    "p_only_y": ([IMPL_Y], [NOT_, IMPL_Y]),
    "p_un": ([("un-", AFF, "UNX")], [NOT_, ("un-", AFF, "UNX")]),
    "pp_solely": ([NONX], [NOT_, NONX]),
    "pp_devoid": ([("devoid of", LEX, "devoid of")], [NOT_, ("devoid of", LEX, "devoid of")]),
    "w_only_non": ([NONX], [NOT_, NONX]),
    "w_free": ([("free of", LEX, "free of")], [NOT_, ("free of", LEX, "free of")]),
    "w_any": ([], [NOT_]),
    "w_lacks": ([], [("lack", LEX, "lacks")]),
    "w_every": ([IMPL_Y], [NOT_, IMPL_Y]),
    "w_none": ([("none", SYN, "none")], []),
    "w_xfree": ([("-free", AFF, "XFREE")], [NOT_, ("-free", AFF, "XFREE")]),
    "w_only_x": ([], [NOT_]),
    "w_named": ([NONX], [NOT_, NONX]),
    "pw_solely": ([NONX], [NOT_, NONX]),
    "pw_devoid": ([("devoid of", LEX, "devoid of")], [NOT_, ("devoid of", LEX, "devoid of")]),
    "pw_without": ([("without", SYN, "without")], [NOT_, ("without", SYN, "without")]),
}
# outer frames: (lexeme, class, surface) of a negating frame; distractor frames: [(lexeme, class, surface, position,
# distance)]
NEG_FRAME_CUE = {"n1": ("deny", LEX, "deny"), "n2": ("refute", LEX, "refute"), "n3": ("dispute", LEX, "dispute"),
                 "n4": ("false", TRU, "false"), "n5": ("untrue", TRU, "untrue"),
                 "n6": ("error to accept", TRU, "error to accept"), "n7": ("reject", LEX, "reject"),
                 "n8": ("unfounded", TRU, "unfounded"), "pn1": ("thrown out", LEX, "thrown out"),
                 "pn2": ("baseless", TRU, "baseless"), "pn3": ("contest", LEX, "contest")}
DIST_FRAME_CUES = {"d1": [("without", SYN, "Without", "outer_frame", "same_sentence")],
                   "d2": [("nothing", SYN, "Nothing", "separate_sentence", "next_sentence")],
                   "d3": [("no", SYN, "no", "outer_frame", "same_sentence"),
                          ("un-", AFF, "unread", "outer_frame", "same_sentence")],
                   "d4": [("not", SYN, "not", "separate_sentence", "next_sentence")],
                   "d5": [("not", SYN, "Not", "outer_frame", "same_sentence")],
                   "d6": [("no", SYN, "no", "outer_frame", "same_sentence")],
                   "ds": [("not", SYN, "not", "outer_frame", "same_sentence")]}
FRAME_FAMILY = {**{f"a{i}": "affirm" for i in range(1, 7)},
                **{f: "verb_negate" for f in ("n1", "n2", "n3", "n7")},
                **{f: "truth_negate" for f in ("n4", "n5", "n6", "n8")},
                **{f: "distract_clause" for f in ("d1", "d3", "d5", "d6", "ds")},
                **{f: "distract_sentence" for f in ("d2", "d4")},
                "pa1": "probe_affirm", "pa2": "probe_affirm", "pn1": "probe_verb_negate", "pn3": "probe_verb_negate",
                "pn2": "probe_truth_negate"}
LOOKALIKE_RE = re.compile(r"\b(?:under|universal|universe|unique|uniform|union|unit|units|understand\w*|discuss\w*|"
                          r"interest\w*|display\w*|nonetheless|notabl[ey]|not\s+only|nothing\s+but)\b", re.I)
NEG_WORD_RE = re.compile(r"\b(?:not|no|never|none|without|nothing|neither|nor)\b|n't\b", re.I)
QUOTE_RE = re.compile(r"\"[^\"\n]{1,120}\"")
STATE_NEG_RE = re.compile(r"\b(?:not|no|never|none|nothing|nobody|nowhere|neither|nor|without|cannot)\b|n't\b", re.I)
EXCLUSION_RE = re.compile(r"\b(?:except|excluding|other than|apart from|but not)\b", re.I)


def label_cue(label):
    """The negation a label name carries (non-X, not X, no X, unX), or IMPLICIT for an affirmative antonym word."""
    lab = label.strip()
    low = lab.lower()
    if low.startswith("non-"):
        return ("non-", AFF, lab)
    if low.startswith("not "):
        return ("not", SYN, "not")
    if low.startswith("no "):
        return ("no", SYN, "no")
    if low.startswith("un") and len(low) > 5 and low not in ("under", "unit", "united"):
        return ("un-", AFF, lab)
    return IMPL


def nonx_cue(term):
    t = term.strip()
    if t.lower().startswith("non-"):
        return ("non-", AFF, t)
    if t.lower().endswith("-free"):
        return ("-free", AFF, t)
    return IMPL


def resolve(layer, row, defs):
    m = row["meta"]
    if layer in (NONX, IMPL_Y):
        if m["fmt"] == "card":
            spec = defs["spec"][m["spec"]]
            return nonx_cue(spec["nonx"]) if layer == NONX else IMPL
        pk = defs["packs"][m["pack"]]
        if layer == NONX:
            return nonx_cue(pk["nonx"])
        return IMPL  # y: an affirmative synonym of non-X
    lex, cls, surf = layer
    if surf == "XFREE":
        surf = (defs["spec"][m["spec"]]["xfree"] if m["fmt"] == "card" else defs["packs"][m["pack"]]["xfree"])
    if surf == "UNX":
        surf = defs["spec"][m["spec"]]["un_x"]
    return (lex, cls, surf)


def base_P(row):
    """(the CORE child lf, truth_P) from the row's own latent fields."""
    m = row["meta"]
    if m["fmt"] == "card" and m.get("card_kind") == "property":
        return {"op": "ATOM", "id": "x_holds", "val": bool(m["x_holds"])}
    if m["fmt"] == "card":
        return {"op": "ATOM", "id": "gold_is_target", "val": bool(m["target_is_gold"])}
    sem, n, nx = m["sem"], m["n_items"], m["n_x"]
    if sem == "nameNotX":
        return {"op": "ATOM", "id": "named_is_x", "val": not m["truth_cplus"]}
    atoms = [{"op": "ATOM", "id": f"item{i}_is_x", "val": i < nx} for i in range(n)]
    k = n if sem == "allX" else 1
    return {"op": "ATLEAST", "k": k, "children": atoms}


def claim_layers(row, defs):
    """The claim's negation layers (outer -> inner) and its role: cplus / cminus / rewrite."""
    m = row["meta"]
    kind, rung = m["kind"], m["rung"]
    cp, cm = LAYERS[kind]
    fr = defs["frames"][m["frame"]]
    if rung == "rewrite":
        claim = m["claim"]
        if m["fmt"] == "card" and m.get("card_kind") == "property":
            spec = defs["spec"][m["spec"]]
            return ([] if m["sense"] else [label_cue(spec["neg_label"])]), "rewrite"
        if m["fmt"] == "card":
            if m["sense"]:
                return [], "rewrite"
            if "a different listed label from" in claim:
                return [("different from", LEX, "different")], "rewrite"
            return [IMPL], "rewrite"
        sem = m["sem"]
        if sem in ("someX", "allX"):
            return [], "rewrite"
        pk = defs["packs"][m["pack"]]
        return ([IMPL] if pk.get("y") else [nonx_cue(pk["nonx"])]), "rewrite"
    use_minus = rung == "dneg" or (rung == "neg" and fr["pol"] == 1)
    return [resolve(x, row, defs) for x in (cm if use_minus else cp)], ("cminus" if use_minus else "cplus")


def build(row, defs):
    m = row["meta"]
    fr = defs["frames"][m["frame"]]
    cues, outer = [], []
    if fr["kind"] == "neg":
        lex, cls, surf = NEG_FRAME_CUE[m["frame"]]
        cues.append({"lexeme": lex, "cls": cls, "position": "outer_frame", "scoping": True,
                     "distance": "same_sentence", "surface": surf})
        outer.append(("NOT", len(cues) - 1))
    elif fr["kind"] == "distractor":
        for lex, cls, surf, pos, dist in DIST_FRAME_CUES[m["frame"]]:
            cues.append({"lexeme": lex, "cls": cls, "position": pos, "scoping": False, "distance": dist,
                         "surface": surf})
            outer.append(("DIST", len(cues) - 1))
    layers, role = claim_layers(row, defs)
    inner = []
    for L in layers:
        if L == IMPL:
            inner.append(("NOT", None))
            continue
        lex, cls, surf = L
        cues.append({"lexeme": lex, "cls": cls, "position": "inner_claim", "scoping": True, "distance": "same_clause",
                     "surface": surf})
        inner.append(("NOT", len(cues) - 1))
    # card-line distractors (item 18): a negation word in a card definition line that does not decide the answer
    card_dist = []
    claim_l = (m.get("claim") or "").lower()
    target = (m.get("target_label") or "").lower()
    for ln in (row.get("card") or "").split("\n"):
        mm = re.match(r"^\s*-\s*([^:]{1,120}):\s*(.*)$", ln)
        if not mm:
            continue
        key, body = mm.group(1).strip().lower(), mm.group(2)
        if key in ("yes", "no", "rule"):
            continue
        deciding = (key == target) if m["fmt"] == "card" and m.get("card_kind") == "multi" else (key in claim_l)
        if m["fmt"] == "card" and m.get("card_kind") == "property":
            deciding = True
        if deciding:
            continue
        for w in NEG_WORD_RE.finditer(QUOTE_RE.sub(" ", body)):
            cues.append({"lexeme": w.group(0).lower().replace("n't", "n't"), "cls": SYN, "position": "card_def",
                         "scoping": False, "distance": "other_field", "surface": w.group(0)})
            card_dist.append(len(cues) - 1)
    # look-alikes in the question (pseudo-negations: under, universal, discuss, ...)
    q = row["instructions"]
    for w in LOOKALIKE_RE.finditer(QUOTE_RE.sub(" ", q)):
        pos = "inner_claim" if w.group(0).lower() in claim_l else "outer_frame"
        cues.append({"lexeme": w.group(0).lower(), "cls": "lookalike", "position": pos, "scoping": False,
                     "distance": "same_clause", "surface": w.group(0)})
    node = {"op": "CORE", "child": base_P(row)}
    for op, ci in reversed(inner):
        node = {"op": "NOT", "cue": ci, "child": node}
    for op, ci in reversed(outer):
        node = {"op": op, "cue": ci, "child": node}
        if op == "DIST" and m["frame"] == "ds":   # 'Given that <coll> was not submitted by <other>': a presupposed
            node.update(mode="presupposed",        # side fact, true by construction (the record names its submitter)
                        side={"op": "ATOM", "id": "other_is_not_the_submitter", "val": True})
    for ci in card_dist:
        node = {"op": "DIST", "cue": ci, "child": node}
    return node, cues, role


def evaluate(n):
    op = n["op"]
    if op == "ATOM":
        return n["val"]
    if op == "NOT":
        return not evaluate(n["child"])
    if op in ("DIST", "CORE"):
        return evaluate(n["child"])
    s = sum(evaluate(c) for c in n["children"])
    return s >= n["k"]


def depth_of(n):
    d = 0
    while n["op"] != "CORE":
        d += n["op"] == "NOT"
        n = n["child"]
    return d, evaluate(n["child"])


def phen_tags(row, lf, cues, depth, role):
    m = row["meta"]
    sc = [c for c in cues if c["scoping"]]
    cls = [c["cls"] for c in sc]
    neg = [c for c in cues if c["cls"] != "lookalike"]
    dist = [c for c in cues if not c["scoping"] and c["cls"] != "lookalike"]
    fr = m["frame"]
    t = set()
    if depth == 0 and not [c for c in neg if c["position"] not in ("card_def", "state")]:
        t.add(1)
    if depth == 1:
        if any(c["cls"] == SYN and c["position"] == "inner_claim" for c in sc) and fr.startswith(("a", "pa", "d")):
            t.add(2)
        if TRU in cls:
            t.add(3)
        if sc and all(c == LEX for c in cls):
            t.add(4)
        if AFF in cls:
            t.add(5)
    if depth == 2 and len(sc) == 2:
        t.add(6 if len(set(cls)) == 2 else 7)
    if depth == 3 and len(set(cls)) >= 2:
        t.add(8)
    if depth == 4:
        t.add(9)
    if depth >= 2 and any(c["position"] == "outer_frame" and c["cls"] in (LEX, TRU) for c in sc) and \
            any(c["position"] != "outer_frame" for c in sc):
        t.add(10)
    if dist:
        t.add(15)
        if depth >= 1:
            t.add(16)
        if depth == 0 and len(dist) >= 2:
            t.add(17)
    if any(c["position"] == "card_def" and not c["scoping"] for c in cues):
        t.add(18)
    if STATE_NEG_RE.search(row.get("state") or ""):
        t.add(19)
    if any(c["cls"] == "lookalike" for c in cues):
        t.add(20)
    kind = m["kind"]
    if kind in ("m_only_other", "m_any_other", "m_none_of", "pm_solely", "pm_outside"):
        t.add(22)
        t.add(31)
    if m["fmt"] == "card" and m.get("card_kind") == "multi" and depth >= 1:
        tl = (m.get("target_label") or "").lower()
        for ln in (row.get("card") or "").split("\n"):
            mm = re.match(r"^\s*-\s*([^:]{1,120}):\s*(.*)$", ln)
            if mm and mm.group(1).strip().lower() == tl and EXCLUSION_RE.search(mm.group(2)):
                t.add(23)
    if kind in ("m_only_other", "pm_solely") and depth >= 1:
        t.add(24)
    claim = (m.get("claim") or "").lower()
    if role != "rewrite" and re.search(r"\bnot every\b|\bnone of\b|\bwithout a single\b", claim):
        t.add(26)
    if kind in ("p_only_non", "pp_solely", "w_only_non", "pw_solely") and any(c["position"] == "outer_frame"
                                                                              for c in sc):
        t.add(27)
    return sorted(t)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--no-decide2", action="store_true")
    a = ap.parse_args(argv)
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    defs = json.loads((D / "f7_defs.json").read_text())
    defs["spec"] = {s["id"]: s for s in defs["prop_specs"]}
    stats = Counter()
    bases_needed = set()
    for part, fn, mfn in (("train", "f7_train.jsonl", "v1_meta.jsonl"), ("probe", "f7_probe.jsonl", "v1_probe_meta.jsonl")):
        rows = [json.loads(line) for line in open(D / fn, encoding="utf-8") if line.strip()]
        metas = []
        for r in rows:
            m = r["meta"]
            lf, cues, role = build(r, defs)
            depth, truth_P = depth_of(lf)
            gold = int(evaluate(lf))
            if gold != r["gold"]:
                stats[f"{part}_lf_gold_mismatch"] += 1
            has_null = '"cue": null' in json.dumps(lf)
            qneg = [c for c in cues if c["cls"] != "lookalike" and c["position"] not in ("card_def", "state")]
            if m["rung"] == "distractor":
                rung = "D"
            elif m["rung"] == "rewrite" and has_null and not qneg and depth % 2 == 1:
                rung = "AR"
            elif depth == 0 and not qneg:
                rung = "R0"
            else:
                rung = f"N{depth}"
            src = m.get("derived_source") or f"pack:{m.get('pack')}"
            meta = {"id": r["id"], "ladder_id": m["latent_id"], "rung": rung, "lf": lf, "truth_P": truth_P,
                    "depth": depth, "n_cues": len(cues),
                    "n_distractor": sum(1 for c in cues if not c["scoping"] and c["cls"] != "lookalike"),
                    "cues": cues, "phen": phen_tags(r, lf, cues, depth, role),
                    "frame_family": FRAME_FAMILY[m["frame"]], "frame_id": m["frame"],
                    "ladder_kind": "card" if m["fmt"] == "card" else "record", "source": src,
                    "dev_kind": "train" if part == "train" else "holdout", "card_style": m["card_style"],
                    "gold": r["gold"], "v1_rung": m["rung"], "v1_kind": m["kind"]}
            if m["fmt"] == "card" and m.get("card_kind") == "multi":
                meta["quoted_label"] = m.get("target_label")
            metas.append(meta)
            stats[f"{part}_rows"] += 1
            stats[f"{part}_rung_{rung}"] += 1
            if m.get("derived_from"):
                bases_needed.add(m["derived_from"])
        with open(out / mfn, "w", encoding="utf-8") as f:
            for x in metas:
                f.write(json.dumps(x, ensure_ascii=False) + "\n")
    if not a.no_decide2:
        # Retired (arbiter round 2 disclosure): golden_src/gen3/v3_nested_negation.py is now the independent v2 decide2
        # (decide2_row(row, ctx)); it does not read v1 rows, and the old decide2_row(row, base) no longer exists.
        raise SystemExit("f7_v1_adapter: the v1 decide2 path is retired (v3_nested_negation.py is the v2 decide2); "
                         "run with --no-decide2")
    if False:  # the old v1 decide2 path, kept for the record
        bases = {}
        with open(D / "golden_train.jsonl", encoding="utf-8") as f:
            for line in f:
                i = line.find('"id": "')
                rid = line[i + 7:line.find('"', i + 7)] if i >= 0 else None
                if rid in bases_needed:
                    bases[rid] = json.loads(line)
        sys.path.insert(0, str(LEAN / "golden_src" / "gen3"))
        import v3_nested_negation as v3
        with open(out / "v1_decide2_preds.jsonl", "w", encoding="utf-8") as fo:
            for fn in ("f7_train.jsonl", "f7_probe.jsonl"):
                for line in open(D / fn, encoding="utf-8"):
                    if not line.strip():
                        continue
                    r = json.loads(line)
                    g2 = v3.decide2_row(r, bases.get(r["meta"].get("derived_from")))
                    fo.write(json.dumps({"id": r["id"], "gold": g2}) + "\n")
                    stats["decide2_agree" if g2 == r["gold"] else "decide2_disagree"] += 1
        stats["bases_found"] = len(bases)
    print(json.dumps(dict(sorted(stats.items())), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
