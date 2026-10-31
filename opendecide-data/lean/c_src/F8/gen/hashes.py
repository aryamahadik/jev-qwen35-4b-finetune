"""Render hash and problem hash (G0 spec 2 'Two hashes', F8-AMB-24).

render_view(S): the structure as rendered (every number with its representation, entity and line order, world,
question, rules), names kept; the G3 parse must reproduce it exactly (check 1). Inert sentences are not part of the
view (they carry no structure; G0 5 check 1 is run on everything the parser can attribute).
problem_hash(S): exact values as reduced rationals, names abstracted to role ids, unordered lists sorted, inert facts and
representation excluded, world, unknown ranges, target, comparator, direction and threshold included, polarity and
negation excluded (meta.structure_hash; G12, G13 method 6).
"""
from __future__ import annotations

import hashlib
import json
from fractions import Fraction as Fr

from numfmt import chance_text


def ctext(v, rep, den):
    """A chance as the text the row shows (representation as rendered); None stays None."""
    if v is None:
        return None
    return chance_text(Fr(v), rep, den)


def _f(x):
    if isinstance(x, Fr):
        return "F:" + (str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}")
    if isinstance(x, dict):
        return {str(k): _f(v) for k, v in sorted(x.items(), key=lambda kv: str(kv[0]))}
    if isinstance(x, (list, tuple)):
        return [_f(v) for v in x]
    if isinstance(x, float):
        raise TypeError("float in a hashed view")
    return x


def _cond(c):
    if not c:
        return None
    return {"conn": c["conn"], "parts": [{k: p[k] for k in sorted(p) if k in ("t", "f", "name", "v", "op", "w", "q")}
                                         for p in c["parts"]]}


def rules_view(S: dict) -> dict:
    R = S["rules"]
    out = {}
    if R.get("scorecard") and (S["form"] in ("tier", "yn_thr", "inv", "yn_act", "rank_top", "rank_order")):
        sc = R["scorecard"]
        out["sc"] = {"F": sc["F"], "M": sc["M"],
                     "lines": [{"cond": _cond(l["cond"]), "pts": l["pts"], "unless": _cond(l.get("unless"))}
                               for l in sc["lines"]]}
    if S["form"] == "tier":
        out["tiers"] = list(R["tiers"])
        out["cuts"] = list(R["cuts"])
        out["only_if"] = {R["tiers"][int(k)]: _cond(v) for k, v in R["only_if"].items()}
        out["overrides"] = [[_cond(o["cond"]), R["tiers"][o["tier"]]] for o in R["overrides"]]
    if R.get("arules"):
        out["arules"] = {a: _cond(c) for a, c in R["arules"].items()}
    if S["form"] == "inv":
        r = R["inv"]
        out["inv"] = {"kind": r["kind"], "action": r.get("action"), "q": r.get("q"), "op": r.get("op"),
                      "v": r.get("v"), "w": r.get("w")}
    if S["form"] == "bin":
        out["bins"] = list(R["bins"])
        out["bin_conv"] = R["bin_conv"]
    if S["form"] == "mat":
        m = R.get("mat") or {}
        out["mat"] = {k: m.get(k) for k in ("lik_edges", "lik_conv", "imp_edges", "grid", "ratings", "lik_names",
                                            "imp_names", "impact")}
    return out


def ent_view(e: dict) -> dict:
    v = {"id": e["id"]}
    if "pts" in e:
        p = e["pts"]
        st = p.get("stated", {})
        v["pts"] = {"b": {f: x for f, x in p["b"].items() if st.get(f, True)}, "c": dict(p["c"]),
                    "a": dict(p["a"]), "arng": {k: list(x) for k, x in (p.get("arng") or {}).items()}}
    if e.get("bay"):
        b = e["bay"]
        bv = {"form": b["form"], "hyps": list(b["hyps"]), "signs": list(b["signs"]),
              "sig": dict(b["sig"])}
        if b["form"] == "rates":
            den = b["rep"]["lik_den"]
            dl = list(den) if isinstance(den, list) else [den] * len(b["hyps"])
            bl = b["rep"].get("base_list") or [(b["rep"]["base"], b["rep"]["base_den"])] * len(b["base"])
            ll = b["rep"].get("lik_list") or [(b["rep"]["lik"], dl[j]) for j in range(len(b["hyps"]))]
            bv.update({"base": [ctext(x, *bl[j]) for j, x in enumerate(b["base"])],
                       "lik": {s: [ctext(x, *ll[j]) if x is not None else None for j, x in enumerate(vec)]
                               for s, vec in b["lik"].items()},
                       "rng": {k: list(x) for k, x in b["rng"].items()},
                       "rngshow": sorted((b.get("rngshow") or {}).keys())})
        elif b["form"] == "counts":
            bv["cnt"] = {s: [list(r) for r in x] for s, x in b["cnt"].items()}
        elif b["form"] == "nE":
            bv["ne"] = {s: list(x) for s, x in b["ne"].items()}
        else:
            bv["joint"] = {s: list(x) for s, x in b["joint"].items()}
        v["bay"] = bv
    if e.get("outs"):
        v["outs"] = [{"ev": o["ev"], "p": ctext(o["p"], o.get("prep"), o.get("pden")), "a": o["a"],
                      "prng": list(o["prng"]) if o.get("prng") else None,
                      "arng": list(o["arng"]) if o.get("arng") else None} for o in e["outs"]]
    if e.get("cost") is not None:
        v["cost"] = [e["cost"], e.get("cost_word") if e.get("cost_word") == "None" else None]
    if e.get("action") is not None:
        v["action"] = e["action"]
    if e.get("ch") is not None:
        c = e["ch"]
        v["ch"] = {"p": ctext(c["p"], c.get("rep"), c.get("den")), "ev": c.get("ev"), "amt": c.get("amt"),
                   "rng": list(c["rng"]) if c.get("rng") else None}
    if e.get("en") is not None:
        n = e["en"]
        v["en"] = {"n": n["n"], "p": ctext(n["p"], n["rep"], n["den"]), "ev": n["ev"]}
    if e.get("mat") is not None:
        m = e["mat"]
        v["mat"] = {"lik": ctext(m["lik"], m["rep"], m.get("den")), "amt": m["amt"]}
    return v


def render_view(S: dict) -> dict:
    v = {"form": S["form"], "world": S["world"], "mode": S.get("mode") if any(e.get("outs") for e in S["ents"])
         else None, "q": S["q"], "case": S["ents"][S["case"]]["id"] if S.get("case") is not None and
         S["form"] not in ("rank_top", "rank_order", "inv", "dec") else None,
         "ents": [ent_view(e) for e in S["ents"]], "rules": rules_view(S)}
    if S["form"] == "yn_thr":
        th = S["thr"]
        tr = th.get("trep") or {}
        v["thr"] = {"op": th["op"], "T": th["T"], "neg": th["neg"], "w": S.get("cmp_word"),
                    "Ttext": ctext(th["T"], tr["rep"], tr.get("denom")) if tr.get("rep") else None}
    if S["form"] == "yn_act":
        v["act"] = dict(S["act"])
    if S["form"] == "rank_top":
        v["hl"] = S["hl"]
    if S["form"] == "rank_order" and S.get("subset"):
        v["subset"] = {"X": S["subset"]["X"], "pos": list(S["subset"]["pos"])}
    if S["form"] == "dec":
        v["dec_case"] = S.get("dec_case")
    return _f(v)


def render_hash(S: dict) -> str:
    return hashlib.sha256(json.dumps(render_view(S), sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def _names(S: dict) -> list:
    """Every name-like string of the structure, in a canonical first-appearance order."""
    seen = []

    def add(x):
        if isinstance(x, str) and x not in seen:
            seen.append(x)
    R = S["rules"]
    for ln in (R.get("scorecard") or {}).get("lines", []):
        for c in (ln["cond"], ln.get("unless")):
            for p in (c or {}).get("parts", []):
                add(p.get("f"))
                add(p.get("name"))
                if p.get("t") == "cat":
                    add(p.get("v"))
    for a, c in (R.get("arules") or {}).items():
        add(a)
        for p in c["parts"]:
            add(p.get("f"))
            add(p.get("name"))
            if p.get("t") == "cat":
                add(p.get("v"))
    for t in R.get("tiers") or []:
        add(t)
    if R.get("mat"):
        for t in R["mat"]["ratings"] + R["mat"]["lik_names"] + R["mat"]["imp_names"]:
            add(t)
    for e in S["ents"]:
        add(e["id"])
        add(e.get("action"))
        if e.get("bay"):
            for h in e["bay"]["hyps"]:
                add(h)
            for s in e["bay"]["signs"]:
                add(s)
        for o in e.get("outs") or []:
            add(o["ev"])
        for k in ("ch", "en"):
            if e.get(k):
                add(e[k].get("ev"))
        if e.get("pts"):
            for f in e["pts"]["b"]:
                add(f)
            for c, val in e["pts"]["c"].items():
                add(c)
                add(val)
            for a in e["pts"]["a"]:
                add(a)
    return seen


def problem_hash(S: dict) -> str:
    """Names abstracted to role ids; unordered lists sorted; representation, inert facts, negation excluded."""
    v = render_view(S)
    roles = {n: f"N{i}" for i, n in enumerate(_names(S))}
    drop = {"prep", "pden", "rep", "den", "base_rep", "lik_rep", "lik_den", "w", "neg", "rngshow"}
    keep_order = S["form"] in ("rank_top", "dec")             # the tie rule reads ID order (XF05)

    def strip(o):
        if isinstance(o, dict):
            return {roles.get(k, k): strip(val) for k, val in o.items() if k not in drop}
        if isinstance(o, list):
            return [strip(x) for x in o]
        if isinstance(o, str):
            return roles.get(o, o)
        return o
    pv = strip(v)
    if isinstance(pv.get("ents"), list):
        if keep_order:
            nums = [int(e["id"].rsplit("-", 1)[-1]) for e in S["ents"]]
            idx = sorted(range(len(nums)), key=lambda i: nums[i])
            pv["ents"] = [pv["ents"][i] for i in idx]
            for x in pv["ents"]:
                x.pop("id", None)
        elif S["form"] != "rank_order":
            for x in pv["ents"]:
                x.pop("id", None)
            pv["ents"] = sorted(pv["ents"], key=lambda x: json.dumps(x, sort_keys=True))
    return hashlib.sha256(json.dumps(pv, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def first_diff(a, b, path=""):
    """Path and values of the first difference between two views (debugging aid for the G3 report)."""
    if type(a) != type(b):
        return f"{path}: {repr(a)[:80]} | {repr(b)[:80]}"
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if a.get(k) != b.get(k):
                return first_diff(a.get(k), b.get(k), path + "/" + str(k))
        return None
    if isinstance(a, list):
        if len(a) != len(b):
            return f"{path}: len {len(a)} | {len(b)}"
        for i, (x, y) in enumerate(zip(a, b)):
            if x != y:
                return first_diff(x, y, path + f"[{i}]")
        return None
    return None if a == b else f"{path}: {repr(a)[:80]} | {repr(b)[:80]}"
