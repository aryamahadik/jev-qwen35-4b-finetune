"""Build packs-3 domain packs (C_DATA_SPEC v4 2.1, step 3 of section 11). Quarter: public sector and civic.

Claude-authored content lives in src/authored/batch_*.py (compact DSL, one dict per pack). This program parses it,
adds the program-made parts (persona seed from the fixed O*NET draw, name pools, ID pools with look-alike pairs, an F12
tool set derived from the pack lexicon, generic inert fact types), runs the pack lints and writes:
  packs-3.jsonl            one pack per line, stable id "pk3-<key>"
  packs-3.lint.json        per-pack lint issues and family-readiness flags (no row text)
CPU only, deterministic (seeds derive from the pack id). Usage:
  ../../../../.venv/bin/python src/build_packs.py [--out-dir DIR]
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                                    # c_src/packs/packs-3
sys.path.insert(0, str(HERE))
import lints  # noqa: E402
import banks  # noqa: E402

SCHEMA_VERSION = "packs-3/v1.1"   # v1.1: review fixes (bool label values, R3-SC3 clusters)
AREAS = {"municipal services", "permits", "transport", "parks", "libraries", "courts admin", "standards",
         "procurement", "civic records", "civic programs"}
GIVEN = ("Amara Ines Tomas Priya Kofi Mei Lucas Hana Omar Sofia Dmitri Aiyana Rafael Nadia Kenji Zara Mateo Leila "
         "Jonas Ama Viktor Rosa Tariq Elena Samir Ingrid Diego Yuki Felix Noor Pablo Grace Arjun Chloe Emeka Maya "
         "Henrik Fatima Luis Anya Kwame Iris Marco Selin Hugo Thandiwe Ravi Clara Bilal Esme Andrei Lina Tobias "
         "Ayesha Bruno Freya Idris Paula Stefan Mira Joaquin Wren Hamid Greta Nikhil Alma Caleb Sana Oskar Daria "
         "Emil Rania Teo Isla Musa Vera Adrian Keira Malik Petra Ruben Signe Jamal Beatriz Leon Ada Imran Nell "
         "Ciro Ebba Dante Lucia Farid Hedda Omari Ruth Sven Ximena Yusuf Zofia Abel Bianca Cyrus Dalia Ezra Flora "
         "Gideon Hiba Ivo Jana Kai Lotte Milan Nina Otto Pia Quentin Rhea Silas Tessa Uriel Vida Wade Yara").split()
ONSET = ["b", "br", "c", "cr", "d", "dr", "f", "fr", "g", "gr", "h", "k", "m", "n", "p", "pr", "r", "s", "st", "t",
         "tr", "v", "w", "z", "th", "sh", "ch", "gl", "pl", "sl"]
VOWEL = ["a", "e", "i", "o", "u", "a", "e", "o", "ai", "ea"]
CODA = ["", "", "n", "r", "l", "s", "m", "nd", "rt", "ll", "th", "ck", "rn"]
END = ["ton", "by", "well", "ford", "wick", "more", "dale", "son", "ley", "holt", "mere", "stad", "an", "er", "is"]
ORG_SUFFIX = ["Works", "Services", "Supply", "Group", "Partners", "Co", "Associates", "Contracting", "Systems",
              "Trades", "Holdings", "Collective", "Studio", "Logistics"]
PLACE_SUFFIX = ["Street", "Road", "Lane", "Avenue", "Way", "Crescent", "Square", "Terrace", "Green", "Row", "Close",
                "Parade"]
ID_LETTERS = "ABCDEFGHJKMNPQRSTUVWXYZ"           # never I, L or O (F13 SEM-31)
CONFUSABLE = {frozenset("17"), frozenset("0D"), frozenset("2Z"), frozenset("5S"), frozenset("6G"), frozenset("8B")}
GENERIC_INERT = ["office opening hours", "public counter location", "general enquiries line", "mailing address for "
                 "correspondence", "staff training calendar", "accessibility arrangements at the counter",
                 "translation and interpreting help", "records retention schedule", "privacy notice reference",
                 "website section for forms", "visitor parking at the office", "complaints procedure contact"]
CHANNELS = ["letter", "email", "text message", "phone call"]
ACTION_LEX = {
    "find": ("search", ["search", "find", "look for"]),
    "get": ("look up", ["look up", "fetch", "retrieve"]),
    "lodge": ("lodge", ["lodge", "submit", "file"]),
    "update": ("update", ["update", "edit"]),
    "book": ("book", ["book", "reserve"]),
    "assign": ("assign", ["assign", "allocate"]),
    "decide": ("record a decision on", ["decide", "rule on"]),
    "notify": ("notify", ["notify", "send a notice about"]),
    "renew": ("renew", ["renew", "extend"]),
    "pause": ("pause", ["pause", "put on hold"]),
    "export": ("export", ["export", "download"]),
    "quote": ("estimate", ["estimate", "quote"]),
}


def seed_for(*parts) -> random.Random:
    return random.Random(hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest())


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


# ------------------------------------------------------------------------------------------------ DSL parsing
def parse_range(r: str):
    a, b = r.split("-", 1) if not r.startswith("-") else ("-" + r[1:].split("-", 1)[0], r[1:].split("-", 1)[1])
    num = float if ("." in a or "." in b) else int
    return num(a), num(b)


def parse_field(spec: str, money: dict) -> dict:
    parts = spec.strip().split(":")
    name, typ = parts[0].strip(), parts[1].strip()
    f = {"name": name, "type": typ}
    rest = parts[2:]
    pol = "nb"
    if rest and rest[-1] in ("hb", "lb", "nb"):
        pol = rest.pop()
    signed = False
    if rest and rest[-1] == "signed":
        signed = True
        rest.pop()
    if typ == "int":
        f.update(unit=rest[0], range=list(parse_range(rest[1])), places=0)
    elif typ == "dec":
        f.update(unit=rest[0], places=int(rest[1]), range=list(parse_range(rest[2])))
    elif typ == "pct":
        f.update(unit="percent", places=int(rest[0]), range=list(parse_range(rest[1])))
    elif typ == "amt":
        f.update(unit=money["currency"], places=money["places"], range=list(parse_range(rest[0])),
                 sign="signed" if signed else "non-negative")
    elif typ == "date":
        f.update(range=rest[0] if rest else "2019-2027")
    elif typ == "bool":
        pass
    elif typ in ("enum", "status"):
        vals = [v.strip() for v in ":".join(rest).split("/")]
        if typ == "status":
            f["values"] = [v.split("=")[0].strip() for v in vals]
            f["polarity"] = {v.split("=")[0].strip(): {"g": "good", "b": "bad", "n": "neutral"}[v.split("=")[1].strip()]
                             for v in vals}
        else:
            f["values"] = vals
    elif typ == "text":
        f.update(length=[2, 160])
    else:
        raise ValueError(f"unknown field type {typ} in {spec}")
    if typ in ("int", "dec", "pct", "amt"):
        f["direction"] = {"hb": "high is bad", "lb": "low is bad", "nb": "neither"}[pol]
    return f


def parse_pack(a: dict) -> dict:
    cur, places, side = a["money"].split("|")[:3]
    date_side = a["money"].split("|")[3] if a["money"].count("|") >= 3 else "must act"
    money = {"currency": cur, "places": int(places), "decider_side": side, "decider_date_side": date_side}
    ents = []
    for e in a["ent"]:
        name, plural, idk, prefix, fields = [x.strip() for x in e.split("|", 4)]
        ents.append({"name": name, "plural": plural, "id_key": idk, "id_prefix": prefix,
                     "fields": [parse_field(x, money) for x in fields.split(";") if x.strip()]})
    sdim, svals = a["scope"].split("|")
    p = {
        "key": a["key"], "area": a["area"], "title": a["title"], "jurisdiction": a["juris"], "org": a["org"],
        "setting": " ".join(a["setting"].split()), "decider_role": a["decider"],
        "roles": [r.strip() for r in a["roles"].split(";")],
        "money": money, "entity_types": ents,
        "scope_dimension": {"name": sdim.strip(), "values": [v.strip() for v in svals.split("/")]},
        "document_types": [{"name": d.split("=")[0].strip(), "current_is": {"g": "not bad", "b": "bad"}[d.split("=")[1].strip()]}
                           for d in a["docs"].split(";")],
        "item_kind": {"plural": a["item"].split("|")[0].strip(),
                      "holder_roles": [{"role": h.split("=")[0].strip(),
                                        "holding_is": {"g": "not bad", "b": "bad"}[h.split("=")[1].strip()]}
                                       for h in a["item"].split("|")[1].split(",")]},
        "boolean_facts": [], "predicates": [], "links": [], "affixed_words": [],
        "events": [], "hypotheses": [], "actions": [], "consequences": [],
        "outcome_sets": [[o.strip() for o in s.split("/")] for s in a["outcomes"]],
        "label_words": [], "jargon_candidates": [j.strip() for j in a["jargon"].split(",")],
        "disjoint_fillers": [x.strip() for x in a["fillers"].split(";")],
        "level_names": [x.strip() for x in a["levels"].split("/")],
        "inert_fact_types": [x.strip() for x in a["inert"].split(";")],
    }
    by_phrase = {}
    for i, b in enumerate(a["bools"]):
        parts = b.split("|")
        kind = {"e": "event", "s": "state"}[parts[0].strip()]
        ph = parts[1].strip()
        pre = None
        if ">" in ph:
            ph, pre = [x.strip() for x in ph.split(">", 1)]
        aliases = [x.strip() for x in parts[2].split(",")] if len(parts) > 2 and parts[2].strip() else []
        by_phrase[ph] = i
        p["boolean_facts"].append({"id": f"b{i+1:02d}", "phrase": ph, "kind": kind, "presupposes_phrase": pre,
                                   "concept_set": aliases})
    for bf in p["boolean_facts"]:
        pre = bf.pop("presupposes_phrase")
        bf["presupposes"] = None
        if pre:
            if pre not in by_phrase:
                bf["presupposes"] = "?" + pre
            else:
                bf["presupposes"] = p["boolean_facts"][by_phrase[pre]]["id"]
    for x in a["preds"].split(";"):
        nm, rest = x.split("=", 1)
        pole, *cue = rest.split("|")
        p["predicates"].append({"predicate": nm.strip(), "adverse_pole": {"t": "true", "f": "false"}[pole.strip()],
                                "implicit_cue_for_false": cue[0].strip() if cue else None})
    for x in a["links"].split(";"):
        act, pas = x.split("/")
        p["links"].append({"active": act.strip(), "passive": pas.strip()})
    for x in a["affix"].split(";"):
        pos, neg = x.split("/")
        p["affixed_words"].append({"base": pos.strip(), "negated": neg.strip()})
    pol_map = {"a": "adverse", "f": "favourable", "n": "neutral", "p": "protective", "b": "bad", "o": "not bad"}
    for key, out in (("events", "events"), ("hyps", "hypotheses"), ("acts", "actions"), ("cons", "consequences")):
        for x in a[key].split(";"):
            ph, tag = x.rsplit("=", 1)
            out_tag = pol_map[tag.strip()]
            if key == "acts":
                p[out].append({"phrase": ph.strip(), "protective": out_tag == "protective"})
            elif key == "cons":
                p[out].append({"phrase": ph.strip(), "tag": out_tag})
            else:
                p[out].append({"phrase": ph.strip(), "polarity": out_tag})
    for x in a["labels"]:
        w, pred = x.split("=", 1)
        m = re.match(r"\s*([a-z_]+)\s*(>=|<=|==|!=|>|<|in)\s*(.+)$", pred)
        if not m:
            raise ValueError(f"bad label predicate {x}")
        fld, op, val = m.groups()
        val = val.strip()
        if op == "in":
            val = [v.strip() for v in val.split("/")]
        elif val in ("true", "false"):
            val = val == "true"                       # JSON boolean for bool fields (review fix 1)
        else:
            try:
                val = float(val) if "." in val else int(val)
            except ValueError:
                pass
        p["label_words"].append({"word": w.strip(), "field": fld, "op": op, "value": val})
    g, h, s, rk = a["register"].split("|")
    p["register"] = {"greeting": g.strip(), "header": h.strip(), "sign_off": s.strip(),
                     "report_kinds": [x.strip() for x in rk.split("/")]}
    t, u = a["sources"].split("|")
    p["source_names"] = {"trusted": [x.strip() for x in t.split(";")], "untrusted": [x.strip() for x in u.split(";")]}
    p["tool_actions"] = [x.strip() for x in a.get("actions", "find;get;lodge;update;book;assign;decide;notify").split(";")]
    p["large_tool_set"] = bool(a.get("large_tools", False))
    return p


# ------------------------------------------------------------------------------------------------ program parts
def gen_surname(rng):
    while True:
        if rng.random() < 0.6:
            w = rng.choice(ONSET) + rng.choice(VOWEL) + rng.choice(CODA) + rng.choice(END)
        else:
            w = "".join(rng.choice(ONSET) + rng.choice(VOWEL) for _ in range(2)) + rng.choice(CODA)
        if 4 <= len(w) <= 10:
            return w.capitalize()


def name_pool(rng, k, make, min_dist, banned=()):
    out = []
    tries = 0
    while len(out) < k and tries < 20000:
        tries += 1
        c = make(rng)
        lc = c.lower()
        if len(lc) < 4 or len(lc) > 26 or c in banned:
            continue
        if lints.word_issues(c, mech=True):
            continue
        if any(lints.levenshtein(lc, o.lower()) < min_dist for o in out):
            continue
        out.append(c)
    return out


def make_names(pid):
    rng = seed_for(pid, "names")
    persons = name_pool(rng, 40, lambda r: f"{r.choice(GIVEN)} {gen_surname(r)}", 3)
    orgs = name_pool(rng, 14, lambda r: f"{gen_surname(r)} {r.choice(ORG_SUFFIX)}", 3)
    places = name_pool(rng, 14, lambda r: f"{gen_surname(r)} {r.choice(PLACE_SUFFIX)}", 3)
    return {"persons": persons, "organisations": orgs, "places": places}


def ok_sub(a, b):
    return frozenset((a, b)) not in CONFUSABLE and a != b


def make_ids(pid, prefix, n_ids, n_pairs, width=4):
    rng = seed_for(pid, "ids", prefix)
    ids, pairs = [], []
    used = set()

    def fresh():
        while True:
            x = "".join(rng.choice("0123456789") for _ in range(width))
            if x[0] != "0" and x not in used:
                return x

    while len(pairs) < n_pairs:
        base = fresh()
        if rng.random() < 0.5:
            i = rng.randrange(width - 1)
            if base[i] == base[i + 1]:
                continue
            alt = base[:i] + base[i + 1] + base[i] + base[i + 2:]
            kind = "transposition"
        else:
            i = rng.randrange(1, width)
            d = rng.choice([c for c in "0123456789" if ok_sub(base[i], c)])
            alt = base[:i] + d + base[i + 1:]
            kind = "substitution"
        if alt in used or alt[0] == "0" or alt == base:
            continue
        used |= {base, alt}
        pairs.append([f"{prefix}-{base}", f"{prefix}-{alt}", kind])
    while len(used) < n_ids:
        used.add(fresh())
    ids = sorted(f"{prefix}-{x}" for x in used)
    return {"format": f"{prefix}-NNNN", "regex": f"^{prefix}-[0-9]{{{width}}}$", "width": len(prefix) + 1 + width,
            "pool": ids, "look_alike_pairs": pairs}


def param_from_field(f, required, pack):
    t = f["type"]
    p = {"name": f["name"], "required": required}
    if t == "int":
        p.update(type="integer", min=f["range"][0], max=f["range"][1], unit=f["unit"])
    elif t in ("dec", "pct"):
        p.update(type="decimal", min=f["range"][0], max=f["range"][1], places=max(1, f["places"]), unit=f["unit"])
    elif t == "amt":
        if f["places"] >= 1:
            p.update(type="decimal", places=f["places"])
        else:
            p.update(type="integer")
        p.update(min=f["range"][0], max=f["range"][1], unit=f["unit"])
    elif t == "date":
        p.update(type="date")
    elif t == "bool":
        p.update(type="boolean")
    elif t in ("enum", "status"):
        p.update(type="enum", members=list(f["values"]))
    elif t == "text":
        p.update(type="string", min_length=2, max_length=160)
    return p


def make_tools(pack):
    pid = pack["id"]
    rng = seed_for(pid, "tools")
    ents = pack["entity_types"]
    dim = pack["scope_dimension"]
    roles = [pack["decider_role"]] + pack["roles"]
    tools = []

    def add(action, ent, params, scope=None, pre=None, troles=None, returns=None, variant=None):
        obj = ent["plural"] if action in ("find", "export") else ent["name"]
        nm = f"{action}_{slug(obj)}" + (f"_{variant}" if variant else "")
        if any(t["name"] == nm for t in tools):
            return
        tools.append({
            "tool_id": f"{pid}-t{len(tools)+1:02d}", "name": nm,
            "capability": {"action": action, "object": ent["name"]},
            "description": f"{ACTION_LEX[action][0].capitalize()} {ent['plural'] if action in ('find', 'export') else 'a ' + ent['name']}"
                           + (f" ({variant.replace('_', ' ')})" if variant else ""),
            "scope": scope or {}, "precondition": pre, "roles": troles or [],
            "cost_tier": rng.choice([1, 1, 2, 2, 3]), "preferred": rng.random() < 0.25,
            "params": params, "constraints": [], "returns": returns or []})

    idp = lambda e, req=True: {"name": e["id_key"], "type": "id", "required": req,
                               "format": pack["id_schemes"][e["id_key"]]["format"]}
    for ei, e in enumerate(ents):
        flds = e["fields"]
        cats = [f for f in flds if f["type"] in ("enum", "status")]
        nums = [f for f in flds if f["type"] in ("int", "dec", "amt", "pct")]
        dates = [f for f in flds if f["type"] == "date"]
        stat = [f for f in flds if f["type"] == "status"]
        acts = pack["tool_actions"]
        sc = {dim["name"]: rng.sample(dim["values"], k=max(1, len(dim["values"]) // 2))} if rng.random() < 0.35 else None
        if "find" in acts:
            fp = [param_from_field(f, False, pack) for f in (cats[:1] + dates[:1])]
            add("find", e, fp, returns=[[e["id_key"], e["name"]]], scope=sc)
        if "get" in acts:
            add("get", e, [idp(e)])
        if "lodge" in acts and ei == 0:
            fp = [param_from_field(f, True, pack) for f in (nums[:1] + cats[:1])] + \
                 [param_from_field(f, False, pack) for f in dates[:1]]
            add("lodge", e, fp, returns=[[e["id_key"], e["name"]]], troles=roles[1:3])
        if "update" in acts and (nums or cats):
            f = (nums + cats)[0]
            add("update", e, [idp(e), param_from_field(f, True, pack)])
        bookable = any(w in e["name"] for w in ("visit", "session", "hearing", "inspection", "appointment", "booking",
                                                 "slot", "class", "shift", "call", "run", "trip", "sitting", "exam",
                                                 "interview", "deployment", "event", "meeting", "tour", "audit"))
        if "book" in acts and dates and bookable:
            pre = {"field": stat[0]["name"], "equals": [v for v in stat[0]["values"] if stat[0]["polarity"][v] != "bad"][0]} if stat else None
            add("book", e, [idp(e), param_from_field(dates[0], True, pack)], pre=pre)
        if "assign" in acts and ei == 0:
            add("assign", e, [idp(e), {"name": "assignee_role", "type": "enum", "required": True,
                                       "members": roles[:4]}], troles=[roles[0]])
        if "decide" in acts and ei == 0:
            add("decide", e, [idp(e), {"name": "decision", "type": "enum", "required": True,
                                       "members": pack["outcome_sets"][0]}], troles=[roles[0]])
        if "notify" in acts and ei == 0:
            add("notify", e, [idp(e), {"name": "channel", "type": "enum", "required": False, "members": CHANNELS,
                                       "default": "letter"}])
        if "renew" in acts and ei == 0:
            add("renew", e, [idp(e), {"name": "term_months", "type": "integer", "required": True, "min": 1, "max": 36,
                                      "unit": "months"}])
        if "pause" in acts and stat:
            add("pause", e, [idp(e)], pre={"field": stat[0]["name"], "equals": stat[0]["values"][0]})
        if "export" in acts and ei == 0 and dates:
            add("export", e, [param_from_field(dates[0], True, pack),
                              {"name": "file_format", "type": "enum", "required": False, "members": ["csv", "pdf"],
                               "default": "csv"}], scope={dim["name"]: list(dim["values"])})
        if "quote" in acts and ei == 0 and nums:
            add("quote", e, [param_from_field(nums[0], True, pack)])
    for t in tools:
        t["compact_profile"] = is_compact(t)
    clusters = []

    def build_cluster(cap_action, e):
        """One near-miss cluster around (cap_action, e); mutates tools. Returns the cluster record."""
        base = plain_tool(tools, cap_action, e)
        if base is None:
            return None
        bparams = base["params"]
        bnames = {p["name"] for p in bparams}
        members = {}

        def consider(t):
            if t is base or not is_compact(t):
                return
            c = nm_components(t, base, dim)
            if len(c) == 1:
                members[t["tool_id"]] = c[0]

        for t in tools:
            consider(t)
        queues = {"scope": [], "role": [], "precondition": [], "needed parameter": []}
        for v in dim["values"]:
            queues["scope"].append(dict(params=bparams, scope={dim["name"]: [v]}, variant=slug(v)))
        for r in roles:
            queues["role"].append(dict(params=bparams, troles=[r], variant="for_" + slug(r)))
        pfs = [f for f in e["fields"] if f["type"] == "status"] + [f for f in e["fields"] if f["type"] == "enum"]
        for pi, pf in enumerate(pfs[:2]):
            for v in pf["values"]:
                queues["precondition"].append(dict(params=bparams, pre={"field": pf["name"], "equals": v},
                                                   variant=("when_" if pi == 0 else "when_" + slug(pf["name"]) + "_")
                                                   + slug(v)))
        for f in e["fields"]:
            if f["name"] not in bnames and f["type"] != "text":
                queues["needed parameter"].append(dict(params=[param_from_field(f, True, pack)],
                                                       variant="by_" + f["name"]))
        order = ["scope", "role", "precondition", "needed parameter"]
        k = 0

        def short():
            return len(members) < CLUSTER_MIN or len(members) - may_fit(members, tools) < SUPPLY_MIN

        while short() and any(queues.values()) and len(tools) < TOOLS_MAX:
            q = queues[order[k % len(order)]]
            k += 1
            if not q:
                continue
            spec = q.pop(0)
            n0 = len(tools)
            add(cap_action, e, json.loads(json.dumps(spec["params"])), scope=spec.get("scope"),
                pre=spec.get("pre"), troles=spec.get("troles"), variant=spec["variant"])
            if len(tools) > n0:
                tools[-1]["compact_profile"] = is_compact(tools[-1])
                consider(tools[-1])
        comp = {}
        for c in members.values():
            comp[c] = comp.get(c, 0) + 1
        return {"capability": {"action": cap_action, "object": e["name"]},
                "base_tool_id": base["tool_id"],
                "member_tool_ids": sorted(members),
                "member_components": {tid: members[tid] for tid in sorted(members)},
                "members_by_component": dict(sorted(comp.items())),
                "n_compact_members": len(members),
                "near_miss_supply_min": len(members) - may_fit(members, tools)}

    if pack["large_tool_set"]:
        # F12 G0 R3-SC3 (review fix 2): >= 2 clusters, each one capability (a, o) plus >= CLUSTER_MIN own-pack
        # compact-profile tools, each exactly one fit component (action, object, scope, precondition, role) or one
        # needed parameter away from requests the plain (a, o) tool fits, with a worst-case near-miss supply
        # >= SUPPLY_MIN. Existing tools count when they qualify; purpose-built scope / role / precondition /
        # needed-value variants of (a, o) fill the rest, round-robin, never past TOOLS_MAX tools. Cluster 1 is
        # (find, first entity type); cluster 2 is the first of (get, 2nd/3rd/4th/1st entity type) that reaches the
        # minimums (a trial build is rolled back when it does not).
        c1 = build_cluster("find", ents[0])
        if c1:
            clusters.append(c1)
        cands = [("get", x) for x in ents[1:]] + [("get", ents[0])]
        for ci, (ca, x) in enumerate(cands):
            snap, state = json.loads(json.dumps(tools)), rng.getstate()
            c2 = build_cluster(ca, x)
            ok = c2 and c2["n_compact_members"] >= CLUSTER_MIN and c2["near_miss_supply_min"] >= SUPPLY_MIN
            if ok or ci == len(cands) - 1:
                if c2:
                    clusters.append(c2)
                break
            tools[:] = snap
            rng.setstate(state)
    for t in tools:
        t["compact_profile"] = is_compact(t)
    return tools, clusters


CLUSTER_MIN = 24        # F12 G0 R3-SC3: >= 24 own-pack compact-profile tools per near-miss cluster
SUPPLY_MIN = 19         # F12 G0 R3-SC3: >= 19 near-misses per cluster intent on a 20-60 row
TOOLS_MAX = 60          # F12 G0 R3-SC3: S1 / S6 packs hold 30-60 tools


def is_compact(t):
    return len(t["params"]) <= 2 and len(t["scope"]) <= 1 and not t["constraints"]


def plain_tool(tools, action, ent):
    nm = f"{action}_{slug(ent['plural'] if action in ('find', 'export') else ent['name'])}"
    for t in tools:
        if t["name"] == nm:
            return t
    return None


def may_fit(members, tools):
    """Worst case per request: in each restricting group at most one variant can fit the request (one scope value,
    one role, one value of each precondition field, one extra named value), so it is no near-miss on that row."""
    by_id = {t["tool_id"]: t for t in tools}
    groups = set()
    for tid, c in members.items():
        if c == "precondition":
            groups.add(("precondition", by_id[tid]["precondition"]["field"]))
        elif c in ("scope", "role", "needed parameter"):
            groups.add((c,))
    return len(groups)


def nm_components(t, base, dim):
    """Fit components on which tool t can fail for a request that the plain base tool fits (F12 A59 / R2-13)."""
    c = []
    if t["capability"]["action"] != base["capability"]["action"]:
        c.append("action")
    if t["capability"]["object"] != base["capability"]["object"]:
        c.append("object")
    allowed = lambda s: set(s.get(dim["name"], dim["values"]))
    if not allowed(t["scope"]) >= allowed(base["scope"]) or set(t["scope"]) - {dim["name"]}:
        c.append("scope")
    if t["precondition"] and t["precondition"] != base["precondition"]:
        c.append("precondition")
    if t["roles"] and (not base["roles"] or not set(t["roles"]) >= set(base["roles"])):
        c.append("role")
    if not c:
        need = lambda x: sorted(p["name"] for p in x["params"] if p.get("required"))
        if need(t) != need(base):
            c.append("needed parameter")
    return c


def param_lexicon(pack):
    """F12 R1-13: every param name belongs to exactly one entity type. Fields belong to their entity; ID keys to their
    entity; the generic tool params (assignee_role, decision, channel, term_months, file_format) belong to the first
    entity type, the only one whose tools use them."""
    lex, clash = {}, []
    ents = pack["entity_types"]
    for e in ents:
        lex[e["id_key"]] = {"entity": e["name"], "kind": "id key"}
        for f in e["fields"]:
            if f["name"] in lex:
                clash.append(f["name"])
            lex[f["name"]] = {"entity": e["name"], "kind": "field"}
    for t in pack["tools"]:
        for prm in t["params"]:
            if prm["name"] not in lex:
                lex[prm["name"]] = {"entity": ents[0]["name"], "kind": "tool param"}
            if prm["name"] in {"assignee_role", "decision", "channel", "term_months", "file_format"} and \
                    t["capability"]["object"] != ents[0]["name"]:
                clash.append(prm["name"])
    return lex, sorted(set(clash))


# ------------------------------------------------------------------------------------------------ checks
def check_pack(p: dict) -> dict:
    iss = []

    def W(slot, s, **kw):
        for i in lints.word_issues(s, **kw):
            iss.append(f"{slot}: '{s}' -> {i}")

    def P(slot, s):
        for i in lints.phrase_issues(s):
            iss.append(f"{slot}: '{s}' -> {i}")

    fnames = []
    for e in p["entity_types"]:
        W("entity", e["name"]); W("entity_plural", e["plural"])
        if set(e["id_prefix"]) & set("ILO") or not re.fullmatch(r"[A-Z]{2,4}", e["id_prefix"]):
            iss.append(f"id_prefix: {e['id_prefix']} -> bad letters")
        for f in e["fields"]:
            fnames.append(f["name"])
            W("field_name", f["name"].replace("_", " "), mech=False)
            if f["type"] in ("enum", "status"):
                if not 2 <= len(f["values"]) <= 10:
                    iss.append(f"field {f['name']}: {len(f['values'])} values (need 2-10)")
                if len(set(v.lower() for v in f["values"])) != len(f["values"]):
                    iss.append(f"field {f['name']}: duplicate values")
                for v in f["values"]:
                    W(f"value[{f['name']}]", v)
            if f["type"] in ("int", "dec", "amt", "pct"):
                lo, hi = f["range"]
                if not lo < hi:
                    iss.append(f"field {f['name']}: bad range")
                if f["type"] == "amt" and f["sign"] == "non-negative" and lo < 0:
                    iss.append(f"field {f['name']}: negative min on non-negative amount")
    if len(set(fnames)) != len(fnames):
        iss.append("field names repeat across entity types")
    idks = [e["id_key"] for e in p["entity_types"]]
    if len(set(idks)) != len(idks) or set(idks) & set(fnames):
        iss.append("id keys repeat or collide with field names")
    if len({e["id_prefix"] for e in p["entity_types"]}) != len(p["entity_types"]):
        iss.append("id prefixes repeat")
    dim = p["scope_dimension"]
    W("scope_dimension", dim["name"])
    if dim["name"] in fnames or slug(dim["name"]) in fnames or slug(dim["name"]) in {"assignee_role", "decision",
                                                                                      "channel", "term_months",
                                                                                      "file_format"}:
        iss.append("scope dimension name equals a param name")
    for v in dim["values"]:
        W("scope_value", v)
    for d in p["document_types"]:
        W("document", d["name"])
    W("item_kind", p["item_kind"]["plural"])
    for h in p["item_kind"]["holder_roles"]:
        W("holder_role", h["role"])
    for r in [p["decider_role"]] + p["roles"]:
        W("role", r)
    for s in p["outcome_sets"]:
        for o in s:
            W("outcome", o)
    for b in p["boolean_facts"]:
        W("boolean_fact", b["phrase"], mech=False, factor=True)
        if b["presupposes"] and b["presupposes"].startswith("?"):
            iss.append(f"boolean {b['id']}: presupposed phrase not found")
        for c in b["concept_set"]:
            P("concept", c)
    for pr in p["predicates"]:
        W("predicate", pr["predicate"], mech=False)
    for l in p["links"]:
        P("link", l["active"]); P("link", l["passive"])
    for aw in p["affixed_words"]:
        W("affix_base", aw["base"], mech=False)
        W("affix_neg", aw["negated"], mech=False, allow_affix=True)
    for k in ("events", "hypotheses", "actions", "consequences"):
        for x in p[k]:
            P(k, x["phrase"])
    for j in p["jargon_candidates"]:
        W("jargon", j)
    for x in p["disjoint_fillers"]:
        P("filler", x)
    for x in p["level_names"]:
        W("level", x)
    for x in p["inert_fact_types"]:
        P("inert", x)
    for x in (p["register"]["greeting"], p["register"]["header"], p["register"]["sign_off"]):
        P("register", x)
    for x in p["source_names"]["trusted"] + p["source_names"]["untrusted"]:
        P("source", x)
    # label words: natural predicates over the pack's own fields
    fmap = {f["name"]: f for e in p["entity_types"] for f in e["fields"]}
    for lw in p["label_words"]:
        W("label_word", lw["word"])
        f = fmap.get(lw["field"])
        if not f:
            iss.append(f"label {lw['word']}: unknown field {lw['field']}")
            continue
        if f["type"] != "bool" and isinstance(lw["value"], bool):
            iss.append(f"label {lw['word']}: boolean value on non-bool field {lw['field']}")
            continue
        if f["type"] in ("enum", "status"):
            vals = lw["value"] if isinstance(lw["value"], list) else [lw["value"]]
            if any(v not in f["values"] for v in vals):
                iss.append(f"label {lw['word']}: value not in {lw['field']}")
        elif f["type"] in ("int", "dec", "amt", "pct"):
            if not isinstance(lw["value"], (int, float)) or not f["range"][0] < lw["value"] < f["range"][1]:
                iss.append(f"label {lw['word']}: threshold outside range of {lw['field']}")
        elif f["type"] == "bool":
            if not isinstance(lw["value"], bool) or lw["op"] not in ("==", "!="):
                iss.append(f"label {lw['word']}: bool field {lw['field']} needs a JSON boolean value with == or !=")
        else:
            iss.append(f"label {lw['word']}: field type {f['type']} has no natural predicate")
    # counts (minimums chosen so every family's stated pack needs can be met)
    mins = {"entity_types": 3, "document_types": 4, "boolean_facts": 6, "predicates": 6, "links": 4,
            "affixed_words": 3, "events": 4, "hypotheses": 3, "actions": 3, "consequences": 6, "label_words": 12,
            "jargon_candidates": 8, "disjoint_fillers": 8, "level_names": 4, "outcome_sets": 2, "roles": 4}
    for k, m in mins.items():
        if len(p[k]) < m:
            iss.append(f"count {k}={len(p[k])} < {m}")
    if len(dim["values"]) < 3:
        iss.append("scope values < 3")
    nums = [f for f in fmap.values() if f["type"] in ("int", "dec", "amt", "pct")]
    cats = [f for f in fmap.values() if f["type"] in ("enum", "status")]
    if len(nums) < 5:
        iss.append(f"numeric fields {len(nums)} < 5")
    if len(cats) < 3:
        iss.append(f"category fields {len(cats)} < 3")
    if not any(f["type"] == "status" for f in fmap.values()):
        iss.append("no status field")
    if not any(f["type"] == "amt" for f in fmap.values()):
        iss.append("no amount field")
    if not any(f["type"] == "date" for f in fmap.values()):
        iss.append("no date field")
    acts = {x["phrase"] for x in p["actions"]}
    if not any(x["protective"] for x in p["actions"]):
        iss.append("no protective action")
    if len({tuple(s) for s in p["outcome_sets"]}) < 2:
        iss.append("outcome sets not distinct")
    clash = p.pop("_param_clash", [])
    if clash:
        iss.append(f"param names on two entity types: {clash}")
    for t in p["tools"]:
        for k in t["scope"]:
            if k in p["param_lexicon"]:
                iss.append(f"tool {t['name']}: scope dimension is also a param name")
    neg_link = [l for l in p["links"] if l["active"] == l["passive"]]
    if neg_link:
        iss.append("link active equals passive")
    return {"issues": iss}


def readiness(p: dict) -> dict:
    fmap = {f["name"]: f for e in p["entity_types"] for f in e["fields"]}
    ids0 = p["id_schemes"][p["entity_types"][0]["id_key"]]
    return {
        "F1": len(p["boolean_facts"]) >= 6 and len(p["outcome_sets"]) >= 2,
        "F2": any(f["type"] == "amt" for f in fmap.values()),
        "F3": len(p["item_kind"]["holder_roles"]) >= 2 and any(f["type"] == "status" for f in fmap.values()),
        "F4": len(p["predicates"]) >= 6 and len(p["links"]) >= 4,
        "F5": len(p["affixed_words"]) >= 3,
        "F7": len(p["boolean_facts"]) >= 6 and len(p["disjoint_fillers"]) >= 8 and len(p["level_names"]) >= 4,
        "F8": len(p["events"]) >= 4 and len(p["hypotheses"]) >= 3 and len(p["actions"]) >= 3,
        "F10": len(p["label_words"]) >= 12 and len(p["jargon_candidates"]) >= 8,
        "F12": (12 <= len(p["tools"]) <= (TOOLS_MAX if p["large_tool_set"] else 30)
                and sum(t["compact_profile"] for t in p["tools"]) >= 10),
        # F12 G0 R3-SC3 (review fix 2): 30-60 tools, >= 2 clusters, each >= 24 compact one-component near-misses and a
        # worst-case near-miss supply >= 19 per cluster intent
        "F12_large": (30 <= len(p["tools"]) <= TOOLS_MAX and len(p["tool_clusters"]) >= 2
                      and all(c["n_compact_members"] >= CLUSTER_MIN and c["near_miss_supply_min"] >= SUPPLY_MIN
                              for c in p["tool_clusters"])),
        "F13": (len(p["scope_dimension"]["values"]) >= 3 and len(ids0["pool"]) >= 60 and len(p["document_types"]) >= 4
                and len(p["inert_fact_types"]) >= 10 and len(p["outcome_sets"]) >= 2),
    }


STOP = set("a an the of to in on at for by with is are was were be been this that its it as into out off "
           "new old staff office room lobby desk team city county public day hall front main has have had "
           "was one two all any each".split())


def domain_tokens(p: dict) -> set:
    parts = []
    for e in p["entity_types"]:
        for f in e["fields"]:
            parts.append(f["name"].replace("_", " "))
            parts += f.get("values", [])
    for k in ("events", "hypotheses", "actions", "consequences"):
        parts += [x["phrase"] for x in p[k]]
    for b in p["boolean_facts"]:
        parts.append(b["phrase"])
        parts += b["concept_set"]
    parts += [d["name"] for d in p["document_types"]] + [x["predicate"] for x in p["predicates"]]
    toks = set()
    for x in parts:
        for t in lints.tokens(x):
            for q in t.split("-"):
                if q not in STOP and len(q) > 2:
                    toks.add(q)
                    toks.add(q.rstrip("s"))
    return toks


def post_pass(packs: list) -> None:
    """Cross-pack diversity (G11): unique fillers (also disjoint from the pack's own domain words), balanced generic
    inert fact types, unique jargon candidates, and a fixed held-out hint (10 packs, lowest sha256 rank)."""
    fbank = banks.split_bank(banks.FILLER_BANK)
    seed_for("packs-3", "fillers").shuffle(fbank)
    used, bank_i = set(), 0
    for p in packs:
        dom = domain_tokens(p)
        keep, src = [], {"authored": 0, "bank": 0}
        cands = list(p["disjoint_fillers"])
        for f in cands:
            ft = {q.rstrip("s") for t in lints.tokens(f) for q in t.split("-") if q not in STOP and len(q) > 2}
            if f in used or ft & dom:
                continue
            keep.append(f); used.add(f); src["authored"] += 1
        crng = seed_for(p["id"], "filler-combo")
        while len(keep) < 8:
            if bank_i < len(fbank):
                f = fbank[bank_i]; bank_i += 1
            else:
                f = crng.choice(banks.FILLER_OBJECTS) + " " + crng.choice(banks.FILLER_ACTIONS).format(
                    loc=crng.choice(banks.FILLER_PLACES))
            ft = {q.rstrip("s") for t in lints.tokens(f) for q in t.split("-") if q not in STOP and len(q) > 2}
            if f in used or ft & dom or lints.phrase_issues(f):
                continue
            keep.append(f); used.add(f); src["bank"] += 1
        p["disjoint_fillers"] = keep
        p["disjoint_fillers_source"] = src
    ibank = banks.split_bank(banks.INERT_BANK)
    seed_for("packs-3", "inert").shuffle(ibank)
    uses = {x: 0 for x in ibank}
    for p in packs:
        need = max(0, 12 - len(p["inert_fact_types"]))
        pool = sorted([x for x in ibank if x not in p["inert_fact_types"]], key=lambda x: (uses[x], ibank.index(x)))
        add = pool[:need]
        for x in add:
            uses[x] += 1
        p["inert_fact_types"] = p["inert_fact_types"] + add
    seenj = set()
    for p in packs:
        rng = seed_for(p["id"], "jargon")
        new = []
        for j in p["jargon_candidates"]:
            jj = j
            while jj in seenj or any(lints.word_issues(jj)):
                head = gen_surname(rng).lower()
                jj = head + (" " + j.split(" ", 1)[1] if " " in j else "")
            seenj.add(jj); new.append(jj)
        p["jargon_candidates"] = new
    ranked = sorted(packs, key=lambda q: hashlib.sha256(q["id"].encode()).hexdigest())
    held = {q["id"] for q in ranked[:10]}
    for p in packs:
        p["heldout_hint"] = p["id"] in held


SEED_FIELDS = ("title", "jurisdiction", "org", "decider_role")


def load_authored():
    packs = []
    for f in sorted((HERE / "authored").glob("batch_*.py")):
        spec = importlib.util.spec_from_file_location(f.stem, f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for a in mod.PACKS:
            a["_batch"] = f.name
            packs.append(a)
    return packs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default=str(ROOT))
    ap.add_argument("--only", default=None)
    args = ap.parse_args()
    draws = json.load(open(HERE / "persona_draws.json"))
    dmap = {d["draw"]: d for d in draws["draws"]}
    authored = load_authored()
    if args.only:
        authored = [a for a in authored if a["key"] in args.only.split(",")]
    out, lint = [], {}
    seen_keys, seen_draws = set(), set()
    for a in authored:
        if a["key"] in seen_keys:
            raise SystemExit(f"duplicate key {a['key']}")
        seen_keys.add(a["key"])
        if a["draw"] in seen_draws:
            raise SystemExit(f"duplicate persona draw {a['draw']} ({a['key']})")
        seen_draws.add(a["draw"])
        p = parse_pack(a)
        pid = f"pk3-{slug(a['key'])}"
        d = dmap[a["draw"]]
        pack = {"id": pid, "pack_id": pid, "schema": SCHEMA_VERSION, "quarter": "public sector and civic", **p}
        pack["persona_seed"] = d["onet_code"]
        pack["persona"] = {"onet_code": d["onet_code"], "title": d["title"], "major_group": d["major_group"],
                           "draw": d["draw"], "draw_seed": draws["seed"]}
        pack["parents"] = [{"name": "O*NET 31.0 Database: occupation titles (occupation_data.csv)",
                            "names": ["O*NET", "O*NET 31.0 Database", "gd_onet_occupation"],
                            "use": "persona seed: one main occupation title, never alternate titles or SOC direct match",
                            "licence": "CC BY 4.0", "record": "https://www.onetcenter.org/license_db.html"}]
        pack["licence"] = "CC0 1.0 (Claude-written pack content); persona title O*NET 31.0 CC BY 4.0 (credit in notices)"
        pack["names"] = make_names(pid)
        pack["id_schemes"] = {}
        for i, e in enumerate(pack["entity_types"]):
            pack["id_schemes"][e["id_key"]] = make_ids(pid, e["id_prefix"], 64 if i == 0 else 24, 16 if i == 0 else 6)
        pack["tools"], pack["tool_clusters"] = make_tools(pack)
        pack["param_lexicon"], pack["_param_clash"] = param_lexicon(pack)
        pack["_batch"] = a["_batch"]
        out.append(pack)
    post_pass(out)
    for pack in out:
        pid = pack["id"]
        chk = check_pack(pack)
        pack["family_ready"] = readiness(pack)
        lint[pid] = {"batch": pack.pop("_batch"), "issues": chk["issues"], "family_ready": pack["family_ready"],
                     "n_tools": len(pack["tools"])}
    # cross-pack: setting ROUGE-L < 0.7 (G11 Claude seeds) and distinct titles
    cross = []
    for i in range(len(out)):
        for j in range(i + 1, len(out)):
            r = lints.rouge_l(out[i]["setting"], out[j]["setting"])
            if r >= 0.5:
                cross.append([out[i]["id"], out[j]["id"], round(r, 3)])
            # G11 (review fix 3): every short seed field also stays under ROUGE-L 0.7 pairwise
            for fld in SEED_FIELDS:
                r = lints.rouge_l(out[i][fld], out[j][fld])
                if r >= 0.7:
                    msg = f"G11 seed ROUGE-L {fld} {round(r, 3)} >= 0.7 with "
                    lint[out[i]["id"]]["issues"].append(msg + out[j]["id"])
                    lint[out[j]["id"]]["issues"].append(msg + out[i]["id"])
    od = Path(args.out_dir)
    with open(od / "packs-3.jsonl", "w") as fh:
        for pk in out:
            fh.write(json.dumps(pk, ensure_ascii=False, sort_keys=False) + "\n")
    json.dump({"n_packs": len(out), "packs_with_issues": sum(bool(v["issues"]) for v in lint.values()),
               "setting_rouge_l_ge_0.5": cross, "per_pack": lint}, open(od / "packs-3.lint.json", "w"), indent=1)
    n_iss = sum(len(v["issues"]) for v in lint.values())
    print(f"packs={len(out)} issues={n_iss} packs_with_issues={sum(bool(v['issues']) for v in lint.values())} "
          f"rougeL>=0.5 pairs={len(cross)}")
    for k, v in lint.items():
        for i in v["issues"]:
            print(k, "|", i)


if __name__ == "__main__":
    main()
