"""Row assembly: decorate a sampled record, render one row in one style, run solver A, parse it back (G3), run
solver B, compare, and run fmt1 loader_check (G15). Returns the row (spec 2.4 format) or a reject reason."""
from __future__ import annotations

import hashlib
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(LEAN / "c_src" / "formats" / "formats-1"))

import canon as CN  # noqa: E402
import core as C  # noqa: E402
import f4lex as L  # noqa: E402
import parse_f4 as PF  # noqa: E402
import render_f4 as R  # noqa: E402
import solve_a as A  # noqa: E402
import solver_b as B  # noqa: E402
from fmt1 import card as fcard  # noqa: E402
from fmt1 import pool as fpool  # noqa: E402

REG_MEMO_TITLES = sorted({r["memo_title"] for r in fpool._load("registers.jsonl")})
WORDINGS = [json.loads(x) for x in (LEAN / "c_src/formats/formats-2/wordings/family_pools.jsonl").read_text()
            .splitlines() if x.strip()]
F4_WORDINGS = [w for w in WORDINGS if w["family"] == "F4"]


def decorate(rec: C.Record, rng: random.Random, *, allow_cues=True):
    """Rendering choices for rules (quantifier, exception word, cues, phrase variants)."""
    for r in rec.rules:
        st = dict(r.style)
        st.setdefault("quant", rng.choice(("every", "every", "each", "any", "all")))
        st.setdefault("excw", "unless" if rng.random() < 0.7 else "except")
        for i, c in enumerate(r.conds):
            if c[0] == "lit" and allow_cues:
                if c[2] and rng.random() < 0.1:
                    st.setdefault(f"cue{i}", "pos0")
                elif not c[2] and rng.random() < 0.3:
                    st.setdefault(f"cue{i}", "neg0" if rng.random() < 0.6 else "neg1")
            elif c[0] != "lit":
                n = {"cmp": len(L.CMP_PHRASES.get(c[2], ())) if c[0] == "cmp" else 0, "rng": 2, "dcmp": 2,
                     "win": 2}[c[0]]
                st.setdefault(f"ph{i}", rng.randrange(max(1, n)))
        if r.form == "link" and allow_cues and r.pcond and not r.pcond[1] and rng.random() < 0.3:
            st.setdefault("pcue", "neg0")
        r.style = st


def lexicon_for(cp) -> dict:
    """The card lexicon handed to the parser (data only)."""
    pack = cp.pack
    titles = set(L.FALLBACK_TITLES) | {d[:1].upper() + d[1:] for d in pack["docs"]}
    return {
        "ids": list(cp.ids), "types": [list(t) for t in cp.types], "umbrella": list(cp.umbrella),
        "preds": list(cp.preds), "qtys": [{"name": q["name"], "unit": q["unit"], "dec": q["dec"]} for q in cp.qtys],
        "dattrs": [a for a, _ in cp.dattrs],
        "links": [{"active": l["active"], "passive": l["passive"]} for l in cp.links],
        "sources": list(cp.sources[0]) + list(cp.sources[1]), "titles": sorted(titles),
        "docs": list(pack["docs"]), "background": list(pack["background"]), "memo_titles": REG_MEMO_TITLES,
        "example_ids": list(L.EXAMPLE_IDS), "example_preds": list(getattr(cp, "example_preds", ()) or ()),
        "role": pack["role"], "wordings": [w["text"] for w in F4_WORDINGS],
        "q_prefixes": sorted({r["q_prefix"] for r in fpool._load("registers.jsonl") if r["q_prefix"]}),
    }


def g3_check(rec, card, row, fields, style, lexd, a_res):
    """Parse back, compare canonical structures and solver B with solver A. Returns (ok, why, info)."""
    skin = fpool.skin(style["skin"])
    try:
        cn_p, info = PF.parse_row(fields, style, skin, lexd)
    except (PF.ParseError, ValueError, KeyError, IndexError) as e:
        return False, "parse:" + (str(e) or type(e).__name__)[:40], None
    cn_g = CN.canon_of(rec, card, row)
    eq, diff = CN.canon_equal(cn_g, cn_p)
    if not eq:
        return False, "canon:" + ",".join(diff), None
    try:
        bres = B.solve(cn_p)
    except B.Budget:
        return False, "b_budget", None
    except (ValueError, KeyError, IndexError) as e:
        return False, "b_error:" + str(e)[:40], None
    if not bres["ok"]:
        return False, "b:" + bres["why"], None
    gold_a = row["gold_canon"]
    if str(bres["gold"]) != str(gold_a):
        return False, "b_gold", None
    if bres["pivots"] != a_res["pivots"]:
        return False, "b_pivots", {"a": a_res["pivots"], "b": bres["pivots"]}
    if "pairs" in bres:
        for k, v in bres["pairs"].items():
            if str(v) != str(gold_a):
                return False, "b_pair_" + k, None
    return True, None, {"frame": info["frame"], "wording": info["wording"], "hash": CN.structure_hash(cn_p)}
