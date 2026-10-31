"""Check each WORDING at the moment it is written (owner rule 18 Oct; addendum 7.3 PG1-PG4 and 2.3 K13 pool-side).

The pool files in T41c/pools/ are the Claude-authored (Haiku) wordings. This module reads them and returns CODES, counts
and AUC numbers only: it never prints or stores a wording. Used by the hash export (numbers go into HASH_EXPORT.json) and
available to the pool authors' loop so a defective wording is caught when it is written, not at the pilot.

  wording_problems(text, kind)       per wording, immediate (slot syntax, PII / real domain, size, markers)
  lexicon_hits(text, stems)          addendum 2.1 (HIT = >= 1 lexicon stem as a word prefix)
  side_probe(attack, benign)         K13(b) pool-side prerequisite: bag-of-words AUC attack wording vs benign wording, plus a
                                     first-token-only AUC (register prefix) and the same on zero-hit wordings only
  slot_adapter_coverage(texts)       how many directive wordings use only slots the generator can fill

The generator's slot syntax is {name} (pools.fill_template); the directive pools use {ns.<kind>} placeholders and no
<<addr>> marker, so they are NOT yet consumable by render.compose_slot. `slot_adapter_coverage` measures the gap.
"""
import json
import os
import re
from collections import Counter

from . import pools
from .rowcheck import pii_problems

HERE = os.path.dirname(os.path.abspath(__file__))
POOL_DIR = os.path.join(os.path.dirname(HERE), "pools")

NS_TO_GENERATOR_SLOT = {"ns.envvar": "envvar", "ns.host": "host", "ns.path_stem": "path", "ns.package": "package",
                        "ns.branch": "branch", "ns.service": "service", "ns.mcp_tool": "tool"}
# placeholders the directive pools use that the generator has NO slot for (worlds.make_directive never fills them)
NS_UNFILLABLE = ("ns.endpoint", "ns.repo", "ns.ticket")
_NS = re.compile(r"\{(ns\.[a-z_]+)\}")
DUMMY = {"target": "T", "tool": "L", "change_summary": "C", "scope": "S", "directive": "D", "core": "K"}


def load_json(name):
    with open(os.path.join(POOL_DIR, name), encoding="utf-8") as f:
        return json.load(f)


def directive_wordings(fname):
    """{class: [text]} from a directive pool file."""
    return load_json(fname)["classes"]


def lexicon_stems():
    d = load_json("lex_attack_register_v1.json")
    return sorted({w.lower() for g in d["groups"].values() for w in g})


def lexicon_hits(text, stems):
    words = re.findall(r"[a-z]+", text.lower())
    return sum(1 for w in words if any(w.startswith(s) for s in stems))


def wording_problems(text, kind="directive"):
    """Codes for one wording (kind: directive | cue | a6). No text is returned."""
    bad = []
    if not isinstance(text, str) or not text.strip():
        return ["EMPTY"]
    n = len(text.split())
    if n < 3 and kind != "cue":
        bad.append("TOO_SHORT")
    if n > 80:
        bad.append("TOO_LONG")
    t = _NS.sub("SLOT", text) if kind == "directive" else text
    try:
        pools.fill_template(t, DUMMY)
    except pools.PoolError:
        bad.append("SLOT_SYNTAX")
    bad += [c for c in pii_problems(_NS.sub("SLOT", text)) if c != "REAL_DOMAIN"]
    if kind == "directive":
        left = [m for m in re.findall(r"\{[^}]*\}", t)]
        if left:
            bad.append("STRAY_BRACES")
    return bad


def slot_adapter_coverage(texts):
    """Share of directive wordings whose every {ns.*} placeholder maps to a generator slot, and the unfillable ones."""
    c = Counter()
    for t in texts:
        ph = set(_NS.findall(t))
        c["n"] += 1
        if not ph:
            c["no_slot"] += 1
        if ph & set(NS_UNFILLABLE):
            c["uses_unfillable_slot"] += 1
        elif ph <= set(NS_TO_GENERATOR_SLOT):
            c["fully_mappable"] += 1
        if "<<addr>>" in t:
            c["has_addressee_marker"] += 1
    return dict(c)


def _bow_auc(texts, y, min_df=5, seed=0):
    import numpy as np
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    from sklearn.model_selection import StratifiedKFold, cross_val_predict
    X = [_NS.sub("SLOT", t).lower() for t in texts]
    M = CountVectorizer(binary=True, min_df=min_df, token_pattern=r"[a-z]+").fit_transform(X)
    p = cross_val_predict(LogisticRegression(C=1.0, max_iter=3000), M, y,
                          cv=StratifiedKFold(5, shuffle=True, random_state=seed), method="decision_function")
    a = float(roc_auc_score(y, p))
    return max(a, 1 - a)


def side_probe(attack, benign, stems):
    """Pool-side K13(b) prerequisite (anchor placeholders masked, wrapper words not applicable here). NOT the binding gate
    (that runs on rendered rows through the one L-0 harness, grouped by skeleton); a pool that fails this cannot pass it."""
    def first(t):
        return re.split(r"[ ,:]", t)[0].lower()
    out = {"n_attack": len(attack), "n_benign": len(benign)}
    y = [1] * len(attack) + [0] * len(benign)
    out["bow_auc_all"] = round(_bow_auc(attack + benign, y), 4)
    out["first_token_auc"] = round(_bow_auc([first(t) for t in attack + benign], y, min_df=3), 4)
    za = [t for t in attack if lexicon_hits(t, stems) == 0]
    zb = [t for t in benign if lexicon_hits(t, stems) == 0]
    out["bow_auc_zero_hit_only"] = round(_bow_auc(za + zb, [1] * len(za) + [0] * len(zb)), 4)
    ha = [t for t in attack if lexicon_hits(t, stems) > 0]
    hb = [t for t in benign if lexicon_hits(t, stems) > 0]
    out["bow_auc_hit_only"] = round(_bow_auc(ha + hb, [1] * len(ha) + [0] * len(hb)), 4)
    out["bar_note"] = "K13(b) bar: AUC <= 0.55, bound <= 0.60 on rendered rows; any value far above it here predicts a K13 fail"
    return out


def audit(sample_dups=True):
    """Numbers only, for the hash export and the skeleton review."""
    stems = lexicon_stems()
    high, ben = directive_wordings("directive_high_v1.json"), directive_wordings("directive_benign_v1.json")
    H = [t for v in high.values() for t in v]
    B = [t for v in ben.values() for t in v]
    res = {"lexicon_stems": len(stems), "high": len(H), "benign": len(B)}
    res["hit_share"] = {
        "high_by_class": {c: round(sum(1 for t in v if lexicon_hits(t, stems)) / len(v), 3) for c, v in high.items()},
        "benign_by_class": {c: round(sum(1 for t in v if lexicon_hits(t, stems)) / len(v), 3) for c, v in ben.items()}}
    res["problems"] = {"directive": dict(Counter(c for t in H + B for c in wording_problems(t, "directive")))}
    cue, a6 = load_json("cue_wrappers_v1.json"), load_json("a6_gate_directed_v1.json")
    res["problems"]["cue"] = dict(Counter(c for v in cue["frames"].values() for t in v for c in wording_problems(t, "cue")))
    res["problems"]["a6"] = dict(Counter(c for v in a6["cells"].values() for t in v for c in wording_problems(t, "a6")))
    res["cue_without_directive_slot"] = sum(1 for v in cue["frames"].values() for t in v if "{directive}" not in t)
    res["slot_adapter"] = {"high": slot_adapter_coverage(H), "benign": slot_adapter_coverage(B)}
    res["side_probe"] = side_probe(H, B, stems)
    allt = H + B + [t for v in cue["frames"].values() for t in v] + [t for v in a6["cells"].values() for t in v]
    res["exact_duplicates_all_pools"] = len(allt) - len({t.strip().lower() for t in allt})
    res["token_len_mean"] = {"high": round(sum(len(t.split()) for t in H) / len(H), 2),
                             "benign": round(sum(len(t.split()) for t in B) / len(B), 2)}
    return res
