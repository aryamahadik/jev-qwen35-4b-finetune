"""families/T40/world.py: draws a T40 head A / head B world (registry, request, earlier results, proposed call) for a
TARGET label (label-first; solver A in resolver.py always has the last word, a draw that misses is redrawn).

draw(rng, head, label, sampler) -> (structure, slots) where slots = {NAME: token}; the plugin turns tokens into slots
(kind "name" when the token holds a space, else "glob"). Every value that can change in a twin or a metamorphic
relation is a slot: USER (skin), CALLEE, A<i> (call argument), L<i> (request clause value), PV (provider clause),
RK<i> / RV<i> (earlier-result key / value). The registry, purposes and labels are structure (program text).

Prevalence neutralisation: a surface feature that only some labels force (a duplicated tool, an off-menu tool, a
qualified call name) is also drawn on the other labels so that its rate in yes and no rows is equal (neutral_p).
"""
from __future__ import annotations

import random

from . import pools as P
from .schema import type_string

HEAD_A = ("VALID", "NONEXISTENT_TOOL", "BAD_ARGS", "TYPE_VIOLATION", "OFF_MENU", "BORROWED_SIGNATURE",
          "UNGROUNDED_VALUE", "AMBIGUOUS_PROVIDER")
HEAD_B = ("CALL", "ASK_FOLLOWUP", "CANNOT_ANSWER")
OPENERS = ("Please", "Could you", "I need you to", "Go ahead and", "Can you")
SHAPES = {  # sampler -> (n_tools range, p results, p crowd (second domain), p decoy result)
    "S1": ((3, 4), 0.15, 0.0, 0.2), "S2": ((4, 6), 0.65, 0.15, 0.3), "S3": ((6, 8), 0.3, 0.5, 0.2),
    "S4": ((5, 6), 0.3, 0.2, 0.2), "S5": ((3, 8), 0.4, 0.3, 0.25)}
P_COLLIDE, P_OFFMENU, P_QUAL = 0.25, 0.5, 0.4
P_COLL_B = {"CALL": 0.3, "ASK_FOLLOWUP": 0.1, "CANNOT_ANSWER": 0.4}
N_FAULTS_A, N_NO_B = 7, 2


def neutral_p(p: float, forcing_share: float) -> float:
    """Rate for rows that do NOT force a feature so that rows overall show it at p (forcing_share of them force it)."""
    return max(0.0, min(1.0, (p - forcing_share) / (1.0 - forcing_share)))


def token_slot_kind(tok: str) -> str:
    return "name" if " " in tok else "glob"


# ----------------------------------------------------------------------------------------------- values

def gen_value(rng: random.Random, ptype: str, schema: dict) -> str:
    if ptype == "city":
        return rng.choice(P.CITIES)
    if ptype == "path":
        return rng.choice(P.PATHS)
    if ptype == "slug":
        return rng.choice(P.SLUGS)
    if ptype.startswith("text("):
        return rng.choice(P.TEXTS[ptype[5:-1]])
    if ptype == "email":
        return f"{rng.choice(P.FIRST)}.{rng.choice(P.LAST)}@{rng.choice(P.ORGS)}.example"
    if ptype == "date":
        return f"2026-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}"
    if schema["type"] == "integer":
        return str(rng.randint(schema["minimum"], schema["maximum"]))
    if schema["type"] == "number":
        return f"{rng.uniform(schema['minimum'], schema['maximum']):.1f}"
    if "enum" in schema:
        return rng.choice(schema["enum"])
    if "pattern" in schema:
        return schema["pattern"][1:schema["pattern"].index("[")] + str(rng.randint(1000, 99999))
    raise ValueError(ptype)


def fresh_value(rng, ptype, schema, avoid: set) -> str | None:
    """A valid value of the type that is not in `avoid` (None when the type has no spare value)."""
    if "enum" in schema:
        rest = [e for e in schema["enum"] if e not in avoid]
        return rng.choice(rest) if rest else None
    for _ in range(40):
        v = gen_value(rng, ptype, schema)
        if v not in avoid:
            return v
    return None


def bad_value(rng, ptype, schema, good: str):
    """(token, is_bare, kind) of a value that breaks the parameter's schema; is_bare: printed without quotes."""
    opts = []
    t = schema["type"]
    if t in ("integer", "number"):
        lo, hi = schema["minimum"], schema["maximum"]
        opts.append(("range", str(hi + rng.randint(1, 9)) if t == "integer" else f"{hi * 2 + 0.5:.1f}", True))
        if lo >= 1:
            opts.append(("range", str(lo - 1), True))
        opts.append(("quoted_number", good, False))
    elif "enum" in schema:
        opts.append(("enum", rng.choice([b for b in P.BAD_ENUM if b not in schema["enum"]]), False))
    elif schema.get("format") == "email":
        opts.append(("format", good.replace("@", "."), False))
    elif schema.get("format") == "date":
        opts.append(("format", rng.choice(("2026-13-40", "14/03/2026", "2026-02-31")), False))
    elif "pattern" in schema:
        pre = schema["pattern"][1:schema["pattern"].index("[")]
        opts.append(("pattern", pre.upper().rstrip("_") + "-" + str(rng.randint(1000, 99999)), False))
    if t == "string":
        opts.append(("number_for_string", str(rng.randint(2, 99)), True))
    kind, tok, bare = rng.choice(opts)
    return tok, bare, kind


def typo(rng, s: str) -> str:
    """A near-miss of an identifier that is a different string (drop or swap a letter in the first word-ish part)."""
    idx = [i for i in range(1, len(s) - 1) if s[i].isalpha() and s[i + 1].isalpha() and s[i] != s[i + 1]]
    if not idx:
        return s + "x"
    i = rng.choice(idx)
    return s[:i] + s[i + 1] + s[i] + s[i + 2:] if rng.random() < 0.5 else s[:i] + s[i + 1:]


# ----------------------------------------------------------------------------------------------- registry

def make_tool(domain: str, row: tuple, provider: str, style: str) -> dict:
    verb, noun, purpose, pspec = row
    params = []
    for p in P.parse_params(pspec):
        sch = P.type_schema(p["type"])
        params.append({"name": P.words_to_name(p["words"], style, param=True), "label": p["label"], "req": p["req"],
                       "schema": sch, "ptype": p["type"]})
    ns = domain
    return {"provider": provider, "name": P.tool_name(verb, noun, style, ns), "purpose": purpose, "menu": True,
            "params": params, "domain": domain}


def callee_of(t: dict) -> str:
    return f"{t['provider']}::{t['name']}"


def build_registry(rng, domain: str, style: str, sampler: str, target_row: tuple | None = None, exclude_row: tuple | None = None):
    """(tools, target index, second domain or None). The target tool comes first before shuffling."""
    (lo, hi), _, p_crowd, _ = SHAPES[sampler]
    n = rng.randint(lo, hi)
    provs = P.DOMAINS[domain][0]
    rows = [r for r in P.DOMAINS[domain][1] if r != exclude_row]      # A45: the CANNOT_ANSWER phantom row is kept out of the registry
    rng.shuffle(rows)
    tools = [make_tool(domain, rows[0], rng.choice(provs), style)]
    d2 = None
    pool = [(domain, r) for r in rows[1:]]
    if p_crowd and rng.random() < p_crowd:
        d2 = rng.choice([d for d in P.DOMAINS if d != domain and (d in P.HELD_OUT_DOMAINS) == (domain in P.HELD_OUT_DOMAINS)])
        pool = pool[: max(1, n // 2)] + [(d2, r) for r in P.DOMAINS[d2][1]]
        rng.shuffle(pool)
    for d, r in pool:
        if len(tools) >= n:
            break
        t = make_tool(d, r, rng.choice(P.DOMAINS[d][0]), style)
        if t["name"] in {x["name"] for x in tools} or t["purpose"] in {x["purpose"] for x in tools}:
            continue
        tools.append(t)
    return tools, 0, d2


def dup_tool(rng, tools: list, idx: int) -> int:
    """Add a copy of tools[idx] under another provider of its domain; returns the copy's index."""
    t = tools[idx]
    others = [p for p in P.DOMAINS[t["domain"]][0] if p != t["provider"]]
    c = dict(t, provider=rng.choice(others), params=[dict(p) for p in t["params"]])
    tools.append(c)
    return len(tools) - 1


# ----------------------------------------------------------------------------------------------- the draw

class Draft:
    def __init__(self):
        self.slots: dict = {}
        self.n = {"L": 0, "A": 0, "AN": 0, "MN": 0, "RK": 0, "RV": 0}

    def add(self, prefix: str, tok: str) -> str:
        self.n[prefix] += 1
        name = f"{prefix}{self.n[prefix]}"
        self.slots[name] = tok
        return name


def cap(s: str) -> str:
    return s[:1].upper() + s[1:]


def draw(rng: random.Random, head: str, label: str, sampler: str, want_twin: bool = False, domain: str | None = None,
         style: str | None = None) -> tuple:
    """One world for the target label. Returns (structure, slots). want_twin: head A only; the draw must carry a
    one-slot twin or ValueError is raised (the caller redraws)."""
    train = sampler != "S5"
    # A45: domain and style come from the design cell (shared by a whole label group, cycled over the sampler's pool), so each
    # card (sampler, head, domain) holds every label equally often; None keeps the old random draw (tests, other callers)
    domain = domain or rng.choice([d for d in P.DOMAINS if (d in P.HELD_OUT_DOMAINS) != train])
    style = style or rng.choice(P.TRAIN_STYLES if train else P.HELD_OUT_STYLES)
    _, p_res, _, p_decoy = SHAPES[sampler]
    # A45: a CANNOT_ANSWER request names a real tool of the SAME domain that the registry leaves out (a random one of the domain's
    # rows), so its words are in-domain vocabulary exactly as in CALL / ASK_FOLLOWUP requests (it used to name another domain's tool,
    # and those foreign words were a bag-of-words tell for CANNOT_ANSWER)
    phantom_row = None
    if head == "B" and label == "CANNOT_ANSWER" and rng.random() >= 0.5:
        phantom_row = rng.choice(P.DOMAINS[domain][1])
    tools, ti, d2 = build_registry(rng, domain, style, sampler, exclude_row=phantom_row)
    T = tools[ti]
    dr = Draft()
    # --- surface features some labels force (a collision of the target, an off-menu tool): drawn on the others too
    forced_coll = label == "AMBIGUOUS_PROVIDER" or (head == "B" and label == "ASK_FOLLOWUP" and rng.random() < 1 / 3)
    ask_ambig = head == "B" and label == "ASK_FOLLOWUP" and forced_coll
    share = {"A": 1 / N_FAULTS_A, "B": 0.25}[head]
    if head == "B":
        want_coll = forced_coll or rng.random() < P_COLL_B[label]
    else:
        want_coll = forced_coll or rng.random() < (P_COLLIDE if label == "VALID" else neutral_p(P_COLLIDE, share))
    if want_coll:
        dup_tool(rng, tools, ti)
    elif rng.random() < 0.2 and len(tools) > 2:      # a collision on a distractor tool (never the target)
        dup_tool(rng, tools, rng.randrange(1, len(tools)))
    while len(tools) > 8:                              # a registry excerpt holds at most 8 tools
        drop = [t for t in tools if t["name"] != T["name"]]
        tools.remove(rng.choice(drop))
    collides = sum(1 for t in tools if t["name"] == T["name"]) > 1
    off_target = label == "OFF_MENU" or (head == "B" and label == "CANNOT_ANSWER" and phantom_row is None)
    for t in tools:
        t["menu"] = True
    p_off = P_OFFMENU if (head == "B" or label == "VALID") else neutral_p(P_OFFMENU, 1 / N_FAULTS_A)
    if head == "B" and label == "CANNOT_ANSWER":
        p_off = 0.0
    if off_target:
        for t in tools:
            if t is T or (head == "B" and t["purpose"] == T["purpose"]):
                t["menu"] = False
    elif rng.random() < p_off:
        cand = [t for t in tools[1:] if t["name"] != T["name"]]
        if cand:
            rng.choice(cand)["menu"] = False
    rng.shuffle(tools)
    ti = next(i for i, t in enumerate(tools) if t is T)
    for t in tools:
        t["mslot"] = dr.add("MN", "yes" if t.pop("menu") else "no")
    # --- the supplied parameters and where each value comes from
    req = [p for p in T["params"] if p["req"]]
    opt = [p for p in T["params"] if not p["req"]]
    extra = 1 if (head == "B" and label == "ASK_FOLLOWUP" and not ask_ambig) else 0     # keeps the clause count label-neutral
    supplied = list(req) + rng.sample(opt, min(len(opt), rng.choice((0, 1, 1, 2)) + extra))
    supplied.sort(key=lambda p: T["params"].index(p))
    tokens = {p["name"]: gen_value(rng, p["ptype"], p["schema"]) for p in T["params"]}
    from_res = {p["name"] for p in supplied if p["ptype"].startswith("id(") and rng.random() < max(p_res, 0.3 if sampler == "S2" else p_res)}
    if label == "TYPE_VIOLATION" and head == "A":
        from_res = set()
    missing = wrong_key = None
    if head == "B" and label == "ASK_FOLLOWUP" and not ask_ambig:
        missing = rng.choice(req)["name"]
        if missing in {p["name"] for p in supplied if p["ptype"].startswith("id(")} and rng.random() < 0.4:
            wrong_key = missing
            from_res.add(missing)
    request = {"opener": rng.choice(OPENERS), "purpose": T["purpose"], "clauses": [], "provider": None}
    phantom = None
    if head == "B" and label == "CANNOT_ANSWER" and not off_target:
        out_ids = {t["purpose"] for t in tools}
        if phantom_row is not None and phantom_row[2] not in out_ids:
            phantom = make_tool(domain, phantom_row, "phantom", style)
            request["purpose"] = phantom["purpose"]
        else:
            request["purpose"] = rng.choice(P.UNSUPPORTED)
    src_params = supplied
    if phantom is not None:
        src_params = [p for p in phantom["params"] if p["req"]]
        tokens = {p["name"]: gen_value(rng, p["ptype"], p["schema"]) for p in phantom["params"]}
    elif request["purpose"] != T["purpose"]:
        gen = (("details", "body"), ("topic", "subject"), ("notes", "note"), ("context", "title"))
        picks = rng.sample(gen, min(len(gen), max(1, len(supplied))))
        src_params = [{"name": n, "label": n, "ptype": f"text({pool})", "schema": {"type": "string"}} for n, pool in picks]
        tokens = {n: rng.choice(P.TEXTS[pool]) for n, pool in picks}
    results: list = []
    res_fields: list = []
    clause_of: dict = {}
    for p in src_params:
        if p["name"] == missing and wrong_key is None:
            continue
        if p["name"] in from_res:
            res_fields.append((p["name"], tokens[p["name"]], p["name"] == wrong_key))
            continue
        clause_of[p["name"]] = dr.add("L", tokens[p["name"]])
        request["clauses"].append({"label": cap(p["label"]), "slot": clause_of[p["name"]]})
    if request["purpose"] == T["purpose"] and rng.random() < 0.25:       # a decoy clause for an unused optional param
        spare = [p for p in opt if p not in supplied]
        if spare:
            p = rng.choice(spare)
            request["clauses"].append({"label": cap(p["label"]), "slot": dr.add("L", tokens[p["name"]])})
    if missing is not None and wrong_key is None:       # the omitted clause is replaced by an unrelated one (clause count neutral)
        mine = {p["label"].lower() for p in T["params"]}
        others = [p for t in tools if t is not T for p in t["params"] if p["label"].lower() not in mine]
        if others:
            p = rng.choice(others)
            request["clauses"].append({"label": cap(p["label"]), "slot": dr.add("L", gen_value(rng, p["ptype"], p["schema"]))})
    rng.shuffle(request["clauses"])
    if head == "A":
        want_provider = collides and rng.random() < 0.6
    elif label == "CALL":
        want_provider = collides
    elif label == "ASK_FOLLOWUP":
        want_provider = (not ask_ambig) and rng.random() < 0.6
    else:
        want_provider = rng.random() < 0.4
    if want_provider and (head == "B" or request["purpose"] == T["purpose"]):
        request["provider"] = dr.add("L", T["provider"])
    if res_fields:
        fields = []
        for name, tok, bad_key in res_fields:
            key = typo(rng, name) if bad_key else name
            fields.append({"key": dr.add("RK", key), "val": dr.add("RV", tok)})
        results.append({"tool": rng.choice(("lookup_record", "find_item", "fetch_entry", "resolve_ref")), "fields": fields})
    if rng.random() < p_decoy:
        dk = rng.choice(("note_ref", "trace_tag", "batch_label", "audit_mark"))
        results.append({"tool": "fetch_meta", "fields": [{"key": dr.add("RK", dk),
                                                           "val": dr.add("RV", rng.choice(P.TEXTS["note"]))}]})
    rng.shuffle(results)
    ledger = {dr.slots[f["val"]] for r in results for f in r["fields"]} | {dr.slots[c["slot"]] for c in request["clauses"]}
    if request["provider"]:
        ledger.add(dr.slots[request["provider"]])
    call = twin = None
    if head == "A":
        call, twin = build_call(rng, label, T, tools, ti, supplied, tokens, clause_of, ledger, dr, collides, style,
                                want_twin)
        if want_twin and twin is None:
            raise ValueError("no one-slot twin for this draw")
    structure = {"head": head, "style": style, "pack": domain, "tools": tools, "request": request, "results": results,
                 "call": call, "twin": twin}
    return structure, dr.slots


def _arg(dr, name: str, tok: str, bare: bool) -> dict:
    return {"nslot": dr.add("AN", name), "slot": dr.add("A", tok), "bare": bare}


def build_call(rng, label, T, tools, ti, supplied, tokens, clause_of, ledger, dr, collides, style, want_twin):
    """The proposed call for a head A label; returns (call, twin). twin = {"slot", "alt", "alt_label"}: the ONE slot
    value that flips the label, and the label it flips to, both from the construction. Single-fault constructions."""
    qualified = collides or rng.random() < P_QUAL
    callee = callee_of(T) if qualified else T["name"]
    twin = None
    pnames = [p["name"] for p in T["params"]]
    all_pnames = {p["name"] for t in tools for p in t["params"]}
    args = [_arg(dr, p["name"], tokens[p["name"]], p["schema"]["type"] in ("integer", "number")) for p in supplied]
    pof = {p["name"]: p for p in T["params"]}
    known = {t["name"] for t in tools} | {callee_of(t) for t in tools}

    def bad_callee(v: float) -> str:
        if v < 0.5:
            bad = typo(rng, T["name"])
            bad = f"{T['provider']}::{bad}" if qualified else bad
        elif v < 0.75:
            provs = [p for p in P.DOMAINS[T["domain"]][0] if p != T["provider"]]
            bad = f"{rng.choice(provs)}::{T['name']}" if not collides else f"vendorx::{T['name']}"
        else:
            other = rng.choice([d for d in P.DOMAINS if d != T["domain"] and (d in P.HELD_OUT_DOMAINS) == (T["domain"] in P.HELD_OUT_DOMAINS)])
            row = rng.choice(P.DOMAINS[other][1])
            bad = P.tool_name(row[0], row[1], style, other)
            if qualified:
                bad = f"{rng.choice(P.DOMAINS[other][0])}::{bad}"
        while bad in known:
            bad += "x"
        return bad

    if label == "AMBIGUOUS_PROVIDER":
        callee = T["name"]
        twin = {"slot": "CALLEE", "alt": callee_of(T), "alt_label": "VALID"}
    elif label == "OFF_MENU":
        twin = {"slot": T["mslot"], "alt": "yes", "alt_label": "VALID"}
    elif label == "NONEXISTENT_TOOL":
        bad = bad_callee(rng.random())
        twin = {"slot": "CALLEE", "alt": callee, "alt_label": "VALID"}
        callee = bad
    elif label == "BORROWED_SIGNATURE":
        mine = set(pnames)
        ys = [t for i, t in enumerate(tools) if i != ti and t["name"] != T["name"]
              and any(p["name"] not in mine for p in t["params"])]
        if not ys:
            raise ValueError("no sibling tool to borrow from")
        names = [p["name"] for p in rng.choice(ys)["params"] if p["name"] not in mine]
        args = args[:min(len(args), len(names))]
        for a, n in zip(args, names):
            dr.slots[a["nslot"]] = n
    elif label == "BAD_ARGS":
        reqs = [a for a in args if dr.slots[a["nslot"]] in {p["name"] for p in T["params"] if p["req"]}]
        v = rng.random()
        if v < 0.25 and reqs and not want_twin:
            args.remove(rng.choice(reqs))
        elif v < 0.5 and not want_twin:
            base = dr.slots[rng.choice(args)["nslot"]]
            nm = typo(rng, base)
            if nm in all_pnames:
                nm = base + "Extra"
            args.append(_arg(dr, nm, rng.choice(sorted(ledger)), False))
            rng.shuffle(args)
        else:
            a = rng.choice(args)
            good = dr.slots[a["nslot"]]
            nm = typo(rng, good)
            if nm in all_pnames:
                nm = good + "Extra"
            dr.slots[a["nslot"]] = nm
            twin = {"slot": a["nslot"], "alt": good, "alt_label": "VALID"}
    elif label == "TYPE_VIOLATION":
        grounded_bad = not want_twin and rng.random() < 0.5      # the request states the bad value too: no twin
        order = rng.sample(args, len(args))
        pick = None
        for a in order:
            name = dr.slots[a["nslot"]]
            p = pof[name]
            good = dr.slots[a["slot"]]
            for _ in range(8):
                tok, bare, _kind = bad_value(rng, p["ptype"], p["schema"], good)
                if grounded_bad and clause_of.get(name):
                    pick = (a, name, good, tok, bare)
                    break
                if bare == a["bare"]:                        # same printing: restoring the value restores validity
                    pick = (a, name, good, tok, bare)
                    break
            if pick:
                break
        if pick is None:
            raise ValueError("no type violation with a restorable twin")
        a, name, good, tok, bare = pick
        if grounded_bad and clause_of.get(name):
            a["bare"] = bare
            dr.slots[clause_of[name]] = tok
            dr.slots[a["slot"]] = tok
        else:
            twin = {"slot": a["slot"], "alt": good, "alt_label": "VALID"}
            dr.slots[a["slot"]] = tok
    elif label == "UNGROUNDED_VALUE":
        spare = [p for p in T["params"] if p["name"] not in {dr.slots[a["nslot"]] for a in args}]
        done = False
        if spare and rng.random() < 0.3 and not want_twin:
            p = rng.choice(spare)
            tok = fresh_value(rng, p["ptype"], p["schema"], ledger)
            if tok is not None:
                args.append(_arg(dr, p["name"], tok, p["schema"]["type"] in ("integer", "number")))
                args.sort(key=lambda a: pnames.index(dr.slots[a["nslot"]]))
                done = True
        if not done:
            a = rng.choice(args)
            p = pof[dr.slots[a["nslot"]]]
            good = dr.slots[a["slot"]]
            tok = fresh_value(rng, p["ptype"], p["schema"], ledger | {good})
            if tok is None:
                raise ValueError("no spare value")
            dr.slots[a["slot"]] = tok
            twin = {"slot": a["slot"], "alt": good, "alt_label": "VALID"}
    elif label == "VALID":
        opts = []
        for a in args:
            p = pof[dr.slots[a["nslot"]]]
            tok = fresh_value(rng, p["ptype"], p["schema"], ledger | {dr.slots[a["slot"]]})
            if tok is not None:
                opts.append({"slot": a["slot"], "alt": tok, "alt_label": "UNGROUNDED_VALUE"})
            btok, bbare, _k = bad_value(rng, p["ptype"], p["schema"], dr.slots[a["slot"]])
            if bbare == a["bare"]:             # same printing: the swap changes one slot only
                opts.append({"slot": a["slot"], "alt": btok, "alt_label": "TYPE_VIOLATION"})
            nm = typo(rng, dr.slots[a["nslot"]])
            if nm not in all_pnames:
                opts.append({"slot": a["nslot"], "alt": nm, "alt_label": "BAD_ARGS"})
        opts.append({"slot": "CALLEE", "alt": bad_callee(rng.random()), "alt_label": "NONEXISTENT_TOOL"})
        opts.append({"slot": T["mslot"], "alt": "no", "alt_label": "OFF_MENU"})
        if qualified and collides:
            opts.append({"slot": "CALLEE", "alt": T["name"], "alt_label": "AMBIGUOUS_PROVIDER"})
        twin = rng.choice(opts)
    dr.slots["CALLEE"] = callee
    return {"callee": "CALLEE", "args": args}, twin
