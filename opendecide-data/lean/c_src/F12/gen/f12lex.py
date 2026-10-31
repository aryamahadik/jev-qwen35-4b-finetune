"""F12 pack lexicon and tool catalogs (G0 spec F12.G0.v7 sections 2, 6.3; program-built from Claude-written packs-1).

Each F12 pack = one packs-1 pack (setting, entity types, ID pools, attributes, roles, scope dimension, status values,
persona seed) plus F12's closed action lexicon. Every tool is program-composed (capability = action x object, params
from the pack's attributes); no public tool dataset text is used (3.G). Pack review (6.3) runs in `review()`.
"""
from __future__ import annotations

import hashlib
import json
import random
import re
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
CSRC = HERE.parents[1]
PACKS1 = CSRC / "packs" / "packs-1" / "packs.jsonl"

# closed action lexicon: change / operation verbs only (NG-53); pairwise no synonym or hypernym pair (NG-45)
ACTIONS = {
    "assign": ("assign", "assigns", "assigned", "assigning"),
    "archive": ("archive", "archives", "archived", "archiving"),
    "cancel": ("cancel", "cancels", "cancelled", "cancelling"),
    "transfer": ("transfer", "transfers", "transferred", "transferring"),
    "rename": ("rename", "renames", "renamed", "renaming"),
    "reschedule": ("reschedule", "reschedules", "rescheduled", "rescheduling"),
    "flag": ("flag", "flags", "flagged", "flagging"),
    "approve": ("approve", "approves", "approved", "approving"),
    "suspend": ("suspend", "suspends", "suspended", "suspending"),
    "restore": ("restore", "restores", "restored", "restoring"),
    "dispatch": ("dispatch", "dispatches", "dispatched", "dispatching"),
    "split": ("split", "splits", "split", "splitting"),
    "renew": ("renew", "renews", "renewed", "renewing"),
}
READ = ("look up", "looks up", "looked up", "looking up")  # the one plain retrieval verb of every pack (R5-03)
OTHER_ID_ACTIONS = {"assign", "transfer"}  # these tools also need the other entity type's ID (a reference param)
RANK = re.compile(r"\b(supervisor|assistant|senior|junior|lead|head|manager|chief|deputy|trainee|admin|"
                  r"principal|director|officer|superintendent|coordinator|controller)\b", re.I)
MARKERS = {"not recorded", "unknown", "none", "-", "n/a", "tbd", "?", "null"}
UNIT_OK = re.compile(r"^[A-Za-z][A-Za-z/]*$")
STRING_PARAMS = ("reason", "remark")
STRING_VALUES = ["crew not available", "access road blocked", "client asked for it", "parts arrive late",
                 "duplicate entry found", "site closed for works", "budget moved to next quarter",
                 "safety review pending", "storm warning issued", "permit not yet issued", "staff on leave",
                 "equipment under repair", "new contract signed", "audit finding raised", "supplier changed terms"]
NAMES_BAD = re.compile(r"[\"':;|<>&\\]")


def snake(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def words(key: str) -> str:
    return key.replace("_", " ")


def rng_for(*parts) -> random.Random:
    return random.Random(int(hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()[:16], 16))


def fmt_dec(v) -> str:
    """No trailing zero after the decimal point, no exponent (NG-04)."""
    d = Decimal(str(v))
    s = format(d.normalize(), "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s


def load_src():
    return [json.loads(l) for l in open(PACKS1)]


def _idfmt(ids):
    m = [re.match(r"^([A-Z]+-)([A-Z0-9]+)$", i) for i in ids]
    if not all(m):
        return None
    pre = {x.group(1) for x in m}
    n = {len(x.group(2)) for x in m}
    if len(pre) != 1 or len(n) != 1:
        return None
    return pre.pop(), n.pop()


def build_pack(src: dict):
    """F12 pack from one packs-1 pack, or (None, reason)."""
    pid = src["id"]
    r = rng_for("f12pack", pid)
    ets = []
    for et, pool in zip(src["entity_types"], src["id_pool"]):
        f = _idfmt(pool["ids"])
        if not f:
            return None, "id format"
        key = snake(et["type"])
        names = [n for n in et["names"] if not NAMES_BAD.search(n) and n.lower() not in MARKERS]
        look = [tuple(p) for p in pool.get("lookalike_pairs", []) if all(x in pool["ids"] for x in p)]
        ets.append({"key": key, "word": et["type"], "plural": et["plural"], "idkey": key + "_id",
                    "namekey": key + "_name", "prefix": f[0], "n": f[1], "ids": list(pool["ids"]),
                    "lookalikes": look, "names": names})
    if len(ets) < 2:
        return None, "entity types"
    ets = ets[:2]
    w0, w1 = ets[0]["word"], ets[1]["word"]
    if w0 in w1 or w1 in w0 or ets[0]["plural"] in w1 or ets[1]["plural"] in w0 or w0 == ets[1]["plural"]:
        return None, "nested objects"
    if len(ets[0]["lookalikes"]) < 2 or len(ets[1]["lookalikes"]) < 2:
        return None, "lookalikes"
    if min(len(e["names"]) for e in ets) < 4:
        return None, "names"
    dim = src["scope_dimension"]
    dkey = snake(dim["name"])
    dvals = [v for v in dim["values"] if not NAMES_BAD.search(v)]
    if len(dvals) < 3:
        return None, "scope values"
    status = [v for v in src["status_values"] if not NAMES_BAD.search(v) and v.lower() not in MARKERS]
    if len(status) < 4:
        return None, "status"
    roles = [x for x in src["roles"] if not RANK.search(x) and not NAMES_BAD.search(x)]
    roles = [x for x in roles if not any(x != y and (x in y or y in x) for y in roles)]
    # params from attributes (each param name = one field of one entity type, R1-13)
    params = {}
    lex_words = {w0, w1, ets[0]["plural"], ets[1]["plural"], dim["name"], "status"}
    tcount = {}
    for i, a in enumerate(src["attributes"]):
        k = snake(a["name"])
        tg = "num" if a["type"] in ("int", "num") else a["type"]
        et = tcount.get(tg, 0) % 2
        if not k or k in (dkey, "status") or k.endswith("_id") or k.endswith("_name") or k in params:
            continue
        if any(w in a["name"] for w in (w0, w1)):
            continue
        spec = None
        if a["type"] in ("int", "num"):
            u = a.get("unit")
            if u is not None and (not UNIT_OK.match(u) or u.lower() in ("days", "weeks", "day", "week")):
                continue
            lo, hi = a.get("range") or [0, 100]
            places = int(a.get("decimals") or 0)
            if lo < 0:
                continue
            if a["type"] == "int" or places == 0:
                lo, hi = int(lo), int(hi)
                if hi - lo < 6:
                    continue
                spec = {"type": "integer", "unit": u, "lo": lo, "hi": hi}
            else:
                places = min(places, 2)
                spec = {"type": "decimal", "unit": u, "lo": Decimal(fmt_dec(lo)), "hi": Decimal(fmt_dec(hi)),
                        "places": places}
        elif a["type"] == "cat":
            vals = [v for v in a.get("values", []) if not NAMES_BAD.search(v) and v.lower() not in MARKERS]
            if len(vals) < 3 or len(set(v.lower() for v in vals)) != len(vals):
                continue
            spec = {"type": "enum", "members": vals}
        elif a["type"] == "bool":
            spec = {"type": "boolean"}
        elif a["type"] == "date":
            spec = {"type": "date"}
        if spec:
            spec.update({"name": k, "et": et, "kind": "set"})
            params[k] = spec
            tcount[tg] = tcount.get(tg, 0) + 1
    for et, sk in enumerate(STRING_PARAMS):
        if sk not in params:
            params[sk] = {"name": sk, "type": "string", "et": et, "kind": "set", "minlen": 3, "maxlen": 40}
    for et, e in enumerate(ets):
        params[e["idkey"]] = {"name": e["idkey"], "type": "id", "et": et, "kind": "reference",
                              "prefix": e["prefix"], "n": e["n"]}
    by_et = {0: {}, 1: {}}
    for k, s in params.items():
        by_et[s["et"]].setdefault(s["type"], []).append(k)
    for et in (0, 1):
        nset = sum(len(v) for t, v in by_et[et].items() if t != "id")
        if not (by_et[et].get("integer") or by_et[et].get("decimal")) or nset < 4:
            return None, f"param inventory et{et}"
    # enum members and units must not collide with lexicon words (NG-08, NG-57 later)
    for s in params.values():
        for m in s.get("members", []):
            if m.lower() in {x.lower() for x in lex_words} or m in dvals or m in status:
                return None, "enum collides"
    # actions: no action word inside an object / dimension / param word (one verb maps to one action, 6.3)
    blob = " ".join([w0, w1, ets[0]["plural"], ets[1]["plural"], dim["name"]] + [words(k) for k in params]
                    + dvals + status + [m for s in params.values() for m in s.get("members", [])]
                    + roles + ets[0]["names"] + ets[1]["names"])
    acts = [a for a in ACTIONS if not any(re.search(r"\b" + re.escape(f) + r"\b", blob, re.I) for f in ACTIONS[a])]
    if re.search(r"\blook(s|ed|ing)? up\b", blob, re.I):
        return None, "read verb in lexicon"
    if len(acts) < 9:
        return None, "actions"
    r.shuffle(acts)
    pk = {"id": pid, "sha": src.get("pack_sha256"), "persona_seed": src["persona_seed"]["onet_code"],
          "onet_title": src["persona_seed"]["onet_title"], "etypes": ets,
          "dim": {"key": dkey, "words": dim["name"], "values": dvals}, "status": status, "roles": roles,
          "params": params, "by_et": by_et, "actions": acts, "people": src.get("people", [])}
    return pk, None


# ---------------------------------------------------------------------------------------------------------- tools
def _param(pk, name, rnd, required, *, tight=None, compact=False):
    s = pk["params"][name]
    p = {"name": name, "type": s["type"], "required": required, "default": None}
    t = s["type"]
    if t == "id":
        p.update(prefix=s["prefix"], n=s["n"])
    elif t in ("integer", "decimal"):
        p["unit"] = s["unit"]
        if t == "decimal":
            p["places"] = s["places"]
        lo, hi = s["lo"], s["hi"]
        span = hi - lo
        if tight == "max":
            hi = lo + (span * 3) // 5 if t == "integer" else Decimal(fmt_dec((lo + span * Decimal("0.6")).quantize(
                Decimal(1).scaleb(-s["places"]))))
        mode = rnd.choice(["both", "min", "max"]) if not compact else rnd.choice(["min", "max"])
        incl_lo, incl_hi = rnd.random() < 0.6, rnd.random() < 0.6
        p["min"] = (lo, incl_lo) if mode in ("both", "min") else None
        p["max"] = (hi, incl_hi) if mode in ("both", "max") else None
        if tight == "max":
            p["min"], p["max"] = None, (hi, True)
    elif t == "date":
        y0 = 2026
        mode = rnd.choice(["both", "min", "max"]) if not compact else rnd.choice(["min", "max"])
        p["min"] = (f"{y0}-01-01", rnd.random() < 0.6) if mode in ("both", "min") else None
        p["max"] = (f"{y0}-12-31", rnd.random() < 0.6) if mode in ("both", "max") else None
    elif t == "enum":
        p["members"] = list(s["members"])
        if not required and rnd.random() < 0.6:
            p["default"] = p["members"][0]
    elif t == "string":
        p["minlen"], p["maxlen"] = s["minlen"], s["maxlen"]
    elif t == "boolean":
        if not required:
            p["default"] = "no"
    return p


# ---- opaque tool names (repair r1, G0 8 "max lexical overlap" <= 1/k + 5 pp; G6 / G7 / G8): a tool's name is an
# invented code name that shares no word with the pack's lexicon (actions, objects, fields, values, names), so no
# request word can match a tool name; the capability lives only in the tool's description (SEM-01, SEM-03).
_NC, _NV = "bdfgklmnprstvz", "aeiou"
_PW = {}


def _pack_words(pk):
    if pk["id"] not in _PW:
        _PW[pk["id"]] = set(re.findall(r"[a-z]+", json.dumps(pk, default=str).lower())) | {"look", "up", "for", "tool", "none"}
    return _PW[pk["id"]]


def tname(pk, dname, k=0):
    """Deterministic code name for the tool whose descriptive key is `dname` (k = collision retry)."""
    r = rng_for("f12name", pk["id"], dname, k)
    bw = _pack_words(pk)
    for _ in range(200):
        ws = ["".join(r.choice(_NC) + r.choice(_NV) for _ in range(r.choice((2, 3)))) for _ in range(2)]
        if not (set(ws) & bw) and ws[0] != ws[1]:
            return "_".join(ws)
    raise AssertionError("tname")


def code_names(pk, tools):
    taken = set()
    for t in tools:
        dn = t.get("dname") or t["name"]
        k = 0
        n = tname(pk, dn, k)
        while n in taken:
            k += 1
            n = tname(pk, dn, k)
        t["dname"], t["name"] = dn, n
        taken.add(n)
    return tools


def by_dname(tools, dname):
    return next((t for t in tools if (t.get("dname") or t["name"]) == dname), None)


def make_tools(pk: dict, big: bool, chain: bool) -> list[dict]:
    """The pack's fixed tool set (A65). big: S1 / S6 packs (30-60 tools, near-miss clusters); else 12-30."""
    rnd = rng_for("f12tools", pk["id"], big, chain)
    tools, names = [], set()
    ets = pk["etypes"]
    dv = pk["dim"]["values"]

    def add(t):
        if t["name"] in names:
            return None
        names.add(t["name"])
        t.setdefault("scope", None)
        t.setdefault("pre", None)
        t.setdefault("roles", list(pk["roles"]))
        t.setdefault("cost", 1 + rnd.randrange(3))
        t.setdefault("pref", rnd.random() < 0.5)
        t.setdefault("returns", [])
        t["compact"] = (len(t["params"]) <= 2 and (t["scope"] is None or len(t["scope"]) >= 1))
        tools.append(t)
        return t

    def set_params(et, k, rr):
        pool = [n for n, s in pk["params"].items() if s["et"] == et and s["kind"] == "set"]
        rr.shuffle(pool)
        return pool[:k]

    acts = pk["actions"][: (13 if big else 9)]
    # read tools (one per entity type; plus a second variant on big packs)
    for et in (0, 1):
        e = ets[et]
        add({"name": f"look_up_{e['key']}", "a": "look up", "o": et, "vid": "base",
             "params": [_param(pk, e["idkey"], rnd, True)]})
    # base tools: action x object
    for a in acts:
        for et in (0, 1):
            e = ets[et]
            sp = set_params(et, 3, rng_for("sp", pk["id"], a, et))
            req = [e["idkey"]] + sp[:1]
            if a in OTHER_ID_ACTIONS:
                req.append(ets[1 - et]["idkey"])
            opt = sp[1:2] if not big else []
            ps = [_param(pk, n, rnd, True, compact=big) for n in req] + [_param(pk, n, rnd, False, compact=big)
                                                                        for n in opt]
            add({"name": f"{snake(a)}_{e['key']}", "a": a, "o": et, "vid": "base", "params": ps})
    # variants on cluster capabilities: scope, precondition, role and parameter variants (near-miss supply)
    n_clusters = 4 if big else 2
    caps = [(a, et) for a in acts[:n_clusters] for et in (0, 1)][: n_clusters]
    for ci, (a, et) in enumerate(caps):
        e = ets[et]
        base = next(t for t in tools if t["a"] == a and t["o"] == et and t["vid"] == "base")
        k = 2
        subsets = []
        for i in range(len(dv)):
            subsets.append([dv[i]])
        for i in range(len(dv)):
            for j in range(i + 1, len(dv)):
                subsets.append([dv[i], dv[j]])
        rnd.shuffle(subsets)
        for sub in subsets[: (6 if big else 2)]:
            add({"name": f"{snake(a)}_{e['key']}_{k}", "a": a, "o": et, "vid": f"scope:{'+'.join(sub)}",
                 "scope": sorted(sub, key=dv.index), "params": [dict(p) for p in base["params"]]})
            k += 1
        for st in pk["status"][: (5 if big else 2)]:
            add({"name": f"{snake(a)}_{e['key']}_{k}", "a": a, "o": et, "vid": f"pre:{st}", "pre": st,
                 "params": [dict(p) for p in base["params"]]})
            k += 1
        if len(pk["roles"]) >= 3:
            for rr in range(3 if big else 1):
                sub = sorted(rnd.sample(pk["roles"], k=max(1, len(pk["roles"]) // 2)), key=pk["roles"].index)
                add({"name": f"{snake(a)}_{e['key']}_{k}", "a": a, "o": et, "vid": f"roles:{'+'.join(sub)}",
                     "roles": sub, "params": [dict(p) for p in base["params"]]})
                k += 1
        # parameter variants: needs one more (or another) set param
        extra = set_params(et, 3, rng_for("xp", pk["id"], a, et))
        for x in extra[1:3]:
            if any(p["name"] == x for p in base["params"]):
                continue
            ps = [dict(p) for p in base["params"] if p["required"]] + [_param(pk, x, rnd, True, compact=True)]
            if len(ps) > 3:
                continue
            add({"name": f"{snake(a)}_{e['key']}_{k}", "a": a, "o": et, "vid": f"param:{x}", "params": ps})
            k += 1
        # a tighter-limit variant (non-accepted value near-miss)
        num = [p for p in base["params"] if p["type"] in ("integer", "decimal") and p["required"]]
        if num:
            n0 = num[0]["name"]
            ps = [dict(p) if p["name"] != n0 else _param(pk, n0, rnd, True, tight="max") for p in base["params"]]
            add({"name": f"{snake(a)}_{e['key']}_{k}", "a": a, "o": et, "vid": f"limit:{n0}", "params": ps})
            k += 1
    # providers (POL-CHAIN on packs only): look up <other> by this entity's ID, returns the other ID (R3-06)
    if chain:
        for et in (0, 1):
            e, o = ets[et], ets[1 - et]
            add({"name": f"look_up_{o['key']}_for_{e['key']}", "a": "look up", "o": 1 - et, "vid": "provider",
                 "params": [_param(pk, e["idkey"], rnd, True)], "returns": [o["idkey"]]})
    lim = 60 if big else 30
    if len(tools) > lim:  # drop variants from the end; read tools, base tools and providers stay
        keep = [t for t in tools if t["vid"] in ("base", "provider")]
        var = [t for t in tools if t["vid"] not in ("base", "provider")]
        var = var[: max(0, lim - len(keep))]
        ids = {id(t) for t in keep + var}
        tools = [t for t in tools if id(t) in ids]
    return code_names(pk, tools)


def review(pk: dict, tools: list[dict]) -> list[str]:
    """Pack review (6.3): lexicon and tool-model rules; returns problems (empty = pass)."""
    bad = []
    ets = pk["etypes"]
    dimk = pk["dim"]["key"]
    pn = set(pk["params"])
    if dimk in pn or "status" in pn:
        bad.append("dimension or precondition key is a param name (NG-11, NG-52)")
    for t in tools:
        for p in t["params"]:
            if p["required"] and p["default"] is not None:
                bad.append(f"{t['name']}: required with default")
            if p["type"] == "decimal" and not p.get("places"):
                bad.append(f"{t['name']}: decimal without places")
        if t["a"] == "look up" and any(pk["params"][p["name"]]["kind"] == "set" for p in t["params"]):
            bad.append(f"{t['name']}: set param on a read tool")
        if len({p["name"] for p in t["params"]}) != len(t["params"]):
            bad.append(f"{t['name']}: duplicate param")
    if len(tools) < 12:
        bad.append("fewer than 12 tools")
    words_all = [e["word"] for e in ets]
    for a in pk["actions"]:
        for f in ACTIONS[a]:
            if any(re.search(r"\b" + re.escape(f) + r"\b", w) for w in words_all):
                bad.append(f"action form {f} inside an object word")
    return bad


def all_packs():
    out, rej = [], {}
    for s in load_src():
        pk, why = build_pack(s)
        if pk:
            out.append(pk)
        else:
            rej[s["id"]] = why
    return out, rej


if __name__ == "__main__":
    ps, rej = all_packs()
    print("packs ok", len(ps), "rejected", len(rej))
    import collections
    print(collections.Counter(rej.values()).most_common(10))
    for pk in ps[:3]:
        for big in (False, True):
            tl = make_tools(pk, big, big)
            print(pk["id"], big, len(tl), review(pk, tl)[:3])
