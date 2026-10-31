"""dx_def_literal: reviewer R's devx renderer + parse-back for F6 `gen3_def_literal` (yn2b/SPEC.md sections 5 F6, 6).

Latents: yn2b/f6_devx_latents.json (gen3_def_literal.export_latents("devx", 100): held-out packs and terms, devx seed
stream and name pool). Labels: dl_core.decide only. Everything a reader sees here (term names, clause names, fact
phrasings, definition sentences, questions, cards, options, file layouts) was written for devx from the latent schema
(dl_core's docstring) and the SPEC, not from the training renderers.

Views (one row per latent): yes/no "is" / "outside" questions (definition in the card), judge yes/no on a register
entry (definition in the card), choice "which condition stops it" (each condition is an option), JB-letter (the
definition in the state). Formats: memo (prose lines), sheet (key: value lines), json (canonical JSON).
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import mv_core as mv  # noqa: E402
import dx_common as dx  # noqa: E402
import dl_core  # noqa: E402  (the shared decide(); never its renderers)

KEY = "gen3_def_literal"
LATENTS = mv.LEAN / "yn2b" / "f6_devx_latents.json"
FMTS = ("memo", "sheet", "json")
FMT_META = {"memo": "prose", "sheet": "kv", "json": "json"}

# ------------------------------------------------------------------------------------------------ packs (devx wording)
PACK = {  # entity noun, clause word, rule-book title pattern
    "tenancy": {"clause": "House Rule", "book": "Occupancy Rules of {org}", "file": "occupancy file"},
    "safety": {"clause": "Site Code section", "book": "{org} Site Code", "file": "incident file"},
    "customs": {"clause": "Tariff entry", "book": "Harbour Customs import schedule", "file": "import file"},
    "insurance": {"clause": "Cover item", "book": "{org} home policy wording", "file": "claim file"},
    "procurement": {"clause": "Tender rule", "book": "County Purchasing Office tender rules", "file": "tender file"},
}
TERMS = {  # term id -> devx name (real-word terms keep a real word; invented terms get an invented label)
    "safety:cat2": "Grade II event", "safety:lti": "time-loss injury", "safety:near_miss": "close call",
    "safety:fall": "height fall", "tenancy:guest": "visitor", "tenancy:lodger": "boarder",
    "tenancy:sched2": "Block C resident", "tenancy:household": "family occupant",
    "procurement:framework_b": "Panel 3 tender", "insurance:s4_escape": "Peril 7 water damage",
    "customs:class4_fibre": "Heading 52 fibre",
}
REGIMES = {
    "the council tax rules": "the municipal rates office's guidance",
    "the landlords' association handbook": "a landlords' trade guide",
    "the national health and safety regulator's guidance": "the national workplace inspectorate's leaflets",
    "the city's housing licence rules": "the city housing permit scheme",
    "the insurer's incident categories": "an insurer's claim categories",
    "the trade union's site handbook": "a union's site guide",
    "the chamber of commerce's membership rules": "a business association's membership rules",
    "the building code": "the construction standards",
    "the Inland Freight Code": "the inland haulage code",
    "the Market Inspectors' Handbook": "the market inspectors' guide",
    "the tax office's size bands": "the revenue office's size bands",
    "general usage among loss adjusters": "common practice among claims assessors",
    "the national weather service's storm scale": "the weather bureau's storm scale",
    "the Regional Trade Convention": "a regional trade agreement",
}
NEUTRAL = {
    "tenancy": ("The home is a two-bedroom flat on the second floor.", "Rent is paid monthly by standing order.",
                "A boiler service was carried out last spring.", "The tenancy began on a fixed-term agreement."),
    "safety": ("The site was working a normal day shift.", "The weather was dry and mild.",
               "The area had been walked by the supervisor that morning.", "The site manager was away that week."),
    "customs": ("The goods travelled by road from the border crossing.", "The importer has used this route before.",
                "The paperwork was lodged online.", "The lorry arrived during normal opening hours."),
    "insurance": ("The policy renews every January.", "The home is a terraced house.",
                  "The policyholder phoned the claims line first.", "Photos of the damage are on file."),
    "procurement": ("The tender was advertised publicly.", "Questions from bidders were answered in writing.",
                    "The evaluation panel has three members.", "The contract would run for two years."),
}

# attr specs: num (label, subject, unit), date (label, verb phrase), flag (label, true clause, false clause),
# cat (label, subject)
A = {
    "tenancy": {
        "age": ("num", "Age", "the occupant's age", "years"),
        "mail": ("flag", "Post delivered here", "the occupant receives post at the home",
                 "the occupant does not receive post at the home"),
        "months": ("num", "Time living at the home", "the time the occupant has lived at the home", "months"),
        "moved_in": ("date", "Move-in date", "the occupant moved in"),
        "nights": ("num", "Nights a week spent there", "the number of nights a week the occupant sleeps there", ""),
        "on_lease": ("flag", "Named on the lease", "the occupant is named on the lease",
                     "the occupant is not named on the lease"),
        "own_room": ("flag", "Own bedroom", "the occupant has a bedroom of their own",
                     "the occupant has no bedroom of their own"),
        "relation": ("cat", "Relation to the tenant", "the occupant's relation to the tenant"),
        "rent_share": ("num", "Share of the rent paid", "the share of the rent the occupant pays", "%"),
        "vehicle": ("flag", "Vehicle kept at the home", "the occupant keeps a vehicle at the home",
                    "the occupant keeps no vehicle at the home"),
    },
    "safety": {
        "contractor": ("flag", "Contractor involved", "the person hurt was a contractor",
                       "the person hurt was not a contractor"),
        "date": ("date", "Date of the incident", "the incident happened"),
        "days_off": ("num", "Days off work", "the number of days the injured person was off work", "days"),
        "first_aid": ("flag", "First aid given", "first aid was given at the scene",
                      "no first aid was given at the scene"),
        "height": ("num", "Height of the drop", "the height of the drop involved", "m"),
        "hours_lost": ("num", "Working hours lost", "the number of working hours lost", "hours"),
        "location": ("cat", "Place", "the place where it happened"),
        "powered": ("flag", "Powered equipment", "powered equipment was involved",
                    "no powered equipment was involved"),
        "ppe": ("flag", "Protective equipment worn", "the worker wore the required protective equipment",
                "the worker did not wear the required protective equipment"),
        "reported": ("num", "Reported after", "the delay before the incident was reported", "hours"),
        "witnesses": ("num", "Witnesses", "the number of witnesses", ""),
    },
    "customs": {
        "arrival": ("date", "Arrival date", "the consignment arrived"),
        "certificate": ("flag", "Certificate of origin", "a certificate of origin came with the consignment",
                        "no certificate of origin came with the consignment"),
        "chilled": ("flag", "Shipped chilled", "the consignment was shipped chilled",
                    "the consignment was not shipped chilled"),
        "form": ("cat", "Form of the goods", "the form of the goods"),
        "moisture": ("num", "Moisture content", "the moisture content", "%"),
        "net_weight": ("num", "Net weight", "the net weight", "kg"),
        "origin": ("cat", "Place of loading", "the place of loading"),
        "packing": ("cat", "Packing", "the packing"),
        "predeclared": ("flag", "Declared before arrival", "the consignment was declared before it arrived",
                        "the consignment was not declared before it arrived"),
        "sealed": ("flag", "Seals intact", "the seals were intact on arrival", "the seals were not intact on arrival"),
        "storage": ("num", "Days in storage", "the time the consignment spent in storage", "days"),
        "value": ("num", "Declared value", "the declared value", "dollars"),
    },
    "insurance": {
        "amount": ("num", "Amount claimed", "the amount claimed", "dollars"),
        "business": ("flag", "Business use", "the home was used for business", "the home was not used for business"),
        "cause": ("cat", "Cause", "the cause of the water"),
        "date": ("date", "Date of loss", "the loss happened"),
        "depth": ("num", "Water depth inside", "the depth of water inside", "cm"),
        "ground": ("flag", "Ground floor only", "the damage was confined to the ground floor",
                   "the damage was not confined to the ground floor"),
        "maintained": ("flag", "Upkeep up to date", "the home's upkeep was up to date",
                       "the home's upkeep was not up to date"),
        "prior": ("num", "Earlier claims", "the number of earlier claims on the policy", ""),
        "rain": ("num", "Rainfall that day", "the rainfall recorded that day", "mm"),
        "reported": ("num", "Days until reported", "the number of days before the loss was reported", "days"),
        "sudden": ("flag", "Sudden escape", "the water escaped suddenly", "the water did not escape suddenly"),
        "unoccupied": ("num", "Days empty before the loss", "the number of days the home had stood empty", "days"),
    },
    "procurement": {
        "certified": ("flag", "Quality certificate", "the bidder holds a quality certificate",
                      "the bidder holds no quality certificate"),
        "early": ("num", "Days before the deadline", "the number of days the bid arrived before the deadline",
                  "days"),
        "insurance": ("num", "Liability cover", "the bidder's liability cover", "dollars"),
        "local": ("flag", "Based in the region", "the bidder is based in the region",
                  "the bidder is not based in the region"),
        "lots": ("num", "Lots bid for", "the number of lots the bid covers", ""),
        "sector": ("cat", "Sector", "the bidder's sector"),
        "signed": ("flag", "Bid form signed", "the bid form is signed", "the bid form is not signed"),
        "staff": ("num", "Headcount", "the bidder's headcount", "people"),
        "submitted": ("date", "Submitted on", "the bid was submitted"),
        "value": ("num", "Contract value", "the contract value", "dollars"),
        "years": ("num", "Years trading", "the bidder's time in business", "years"),
    },
}
NUM_OP = {">=": "at least", ">": "more than", "<=": "at most", "<": "less than"}
DATE_OP = {"<": "before", "<=": "on or before", ">": "after", ">=": "on or after"}
NUM_OP_R = {v: k for k, v in NUM_OP.items()}
DATE_OP_R = {v: k for k, v in DATE_OP.items()}
NOT_RECORDED = "not recorded"


def cap(s: str) -> str:
    return s[:1].upper() + s[1:]


SINGULAR = {"years": "year", "months": "month", "days": "day", "hours": "hour", "people": "person",
            "dollars": "dollar"}


def unit_txt(n, unit: str) -> str:
    t = dx.num_text(n)
    if not unit:
        return t
    if unit == "%":
        return t + unit
    return f"{t} {SINGULAR.get(unit, unit) if n == 1 else unit}"


def cond_text(pack: str, c: dict) -> str:
    sp = A[pack][c["attr"]]
    k = c["kind"]
    if k == "num":
        return f"{sp[2]} is {NUM_OP[c['op']]} {unit_txt(c['limit'], sp[3])}"
    if k == "date":
        return f"{sp[2]} {DATE_OP[c['op']]} {dx.long_date(dx.day_of_2026(c['limit']))}"
    if k == "flag":
        return sp[2] if c["want"] else sp[3]
    if k == "cat":
        vs = list(c["values"])
        return f"{sp[2]} is {vs[0]}" if len(vs) == 1 else f"{sp[2]} is one of {dx.join_list(vs, 'or')}"
    raise ValueError(k)


def parse_cond(pack: str, s: str) -> dict:
    s = s.strip()
    for attr, sp in A[pack].items():
        k = sp[0]
        if k == "flag":
            if s == sp[2]:
                return {"attr": attr, "kind": "flag", "want": True}
            if s == sp[3]:
                return {"attr": attr, "kind": "flag", "want": False}
        elif k == "num":
            m = re.fullmatch(re.escape(sp[2]) + r" is (at least|more than|at most|less than) (.+)", s)
            if m:
                try:
                    v = _parse_unit(m.group(2), sp[3])
                except ValueError:
                    continue
                return {"attr": attr, "kind": "num", "op": NUM_OP_R[m.group(1)], "limit": v}
        elif k == "date":
            m = re.fullmatch(re.escape(sp[2]) + r" (before|on or before|after|on or after) (\d{1,2} [A-Z][a-z]+ \d{4})",
                             s)
            if m:
                return {"attr": attr, "kind": "date", "op": DATE_OP_R[m.group(1)],
                        "limit": dx.doy_2026(dx.parse_long_date(m.group(2)))}
        elif k == "cat":
            m = re.fullmatch(re.escape(sp[2]) + r" is one of (.+)", s)
            if m:
                return {"attr": attr, "kind": "cat", "values": dx.split_list(m.group(1), "or")}
            m = re.fullmatch(re.escape(sp[2]) + r" is (.+)", s)
            if m:
                return {"attr": attr, "kind": "cat", "values": [m.group(1)]}
    raise ValueError(f"unparsed condition ({pack}): {s!r}")


def _parse_unit(s: str, unit: str):
    """Inverse of unit_txt (exact): the value must re-render to the same text."""
    if unit == "%":
        if not s.endswith("%"):
            raise ValueError(s)
        body = s[:-1]
    elif unit:
        body, _, u = s.partition(" ")
        if u not in (unit, SINGULAR.get(unit, unit)):
            raise ValueError(s)
    else:
        body = s
    if not re.fullmatch(r"[\d,]+(?:\.\d+)?", body):
        raise ValueError(s)
    v = _int(body)
    if unit_txt(v, unit) != s:
        raise ValueError(f"non-canonical value text {s!r}")
    return v


def _int(s: str):
    v = dx.parse_num(s)
    return int(v) if v.denominator == 1 else v


def value_text(pack: str, attr: str, v) -> str:
    sp = A[pack][attr]
    if v is None:
        return NOT_RECORDED
    if sp[0] == "num":
        return unit_txt(v, sp[3])
    if sp[0] == "date":
        return dx.long_date(dx.day_of_2026(v))
    if sp[0] == "flag":
        return "yes" if v else "no"
    return str(v)


def parse_value(pack: str, attr: str, s: str):
    sp = A[pack][attr]
    s = s.strip()
    if s == NOT_RECORDED:
        return None
    if sp[0] == "num":
        return _parse_unit(s, sp[3])
    if sp[0] == "date":
        return dx.doy_2026(dx.parse_long_date(s))
    if sp[0] == "flag":
        return {"yes": True, "no": False}[s]
    return s


def fact_sentence(pack: str, attr: str, v) -> str:
    sp = A[pack][attr]
    if v is None:
        return f"Not recorded in the file: {sp[1].lower()}."
    if sp[0] == "num":
        return f"{cap(sp[2])}: {unit_txt(v, sp[3])}."
    if sp[0] == "date":
        return f"{cap(sp[2])} on {dx.long_date(dx.day_of_2026(v))}."
    if sp[0] == "flag":
        return cap(sp[2] if v else sp[3]) + "."
    return f"{cap(sp[2])}: {v}."


def parse_fact_sentence(pack: str, line: str):
    """(attr, value) of a memo fact line, or None if the line is not a fact line."""
    for attr, sp in A[pack].items():
        if line == f"Not recorded in the file: {sp[1].lower()}.":
            return attr, None
        if sp[0] in ("num", "cat"):
            pre = f"{cap(sp[2])}: "
            if line.startswith(pre) and line.endswith("."):
                return attr, parse_value(pack, attr, line[len(pre):-1])
        elif sp[0] == "date":
            pre = f"{cap(sp[2])} on "
            if line.startswith(pre) and line.endswith("."):
                return attr, dx.doy_2026(dx.parse_long_date(line[len(pre):-1]))
        else:
            if line == cap(sp[2]) + ".":
                return attr, True
            if line == cap(sp[3]) + ".":
                return attr, False
    return None


# ------------------------------------------------------------------------------------------------ the definition
def clause_name(f: dict) -> str:
    return f"{PACK[f['pack']]['clause']} {f['clause_no']}"


def term(f: dict) -> str:
    return TERMS[f["term"]]


def definition_text(f: dict) -> str:
    """The operative definition as one line (dl_core.definition_parts: the outside rule is written in when r_card)."""
    d = dl_core.definition_parts(f)
    pk, ent, T = f["pack"], f["entity"], term(f)
    els = [cond_text(pk, c) for c in d["elements"]]
    lead = "all of these hold" if d["joiner"] == "all" else "at least one of these holds"
    parts = [f"{cap(article(ent))} {ent} is a '{T}' only if {lead}: "
             + "; ".join(f"({'abcd'[i]}) {e}" for i, e in enumerate(els)) + "."]
    if d["deem"] is not None:
        parts.append(f"Even if those conditions are not met, the {ent} is still a '{T}' when "
                     f"{cond_text(pk, d['deem'][0])}, as long as no exclusion applies.")
    for j, (trig, unless, _) in enumerate(d["exclusions"], 1):
        s = f"Exclusion {j}: it is not a '{T}' if {cond_text(pk, trig)}"
        s += f", unless {cond_text(pk, unless)}." if unless is not None else "."
        parts.append(s)
    parts.append(READING)
    return " ".join(parts)


READING = ("A condition is met only when the file records the fact it depends on; a fact the file does not record "
           "is not established (this applies to exclusions and 'unless' parts too). Only this text decides; other "
           "rule books and everyday usage do not.")


def article(w: str) -> str:
    return dx.article(w)


def parse_definition(pack: str, text: str) -> dict:
    """-> {"elements", "joiner", "exclusions" [(trigger, unless)], "deem"} from definition_text output."""
    if not text.endswith(READING):
        raise ValueError("definition reading sentence missing")
    body = text[: -len(READING)].strip()
    m = re.match(r"An? [a-z]+ is a '([^']+)' only if (all of these hold|at least one of these holds): (.+?)\.(?= Even if| Exclusion \d|$)",
                 body)
    if not m:
        raise ValueError("definition head not found")
    joiner = "all" if m.group(2) == "all of these hold" else "any"
    items = re.split(r"; (?=\([a-d]\) )", m.group(3))
    els = []
    for i, it in enumerate(items):
        mm = re.fullmatch(r"\(([a-d])\) (.+)", it)
        if not mm or mm.group(1) != "abcd"[i]:
            raise ValueError(f"element {i} malformed: {it!r}")
        els.append(parse_cond(pack, mm.group(2)))
    rest = body[m.end():].strip()
    deem = None
    md = re.match(r"Even if those conditions are not met, the [a-z]+ is still a '[^']+' when (.+?), as long as no "
                  r"exclusion applies\.", rest)
    if md:
        deem = parse_cond(pack, md.group(1))
        rest = rest[md.end():].strip()
    exc = []
    for mx in re.finditer(r"Exclusion (\d+): it is not a '[^']+' if (.+?)\.(?= Exclusion \d+:|$)", rest):
        s = mx.group(2)
        if ", unless " in s:
            a, b = s.split(", unless ", 1)
            exc.append((parse_cond(pack, a), parse_cond(pack, b)))
        else:
            exc.append((parse_cond(pack, s), None))
    left = re.sub(r"Exclusion (\d+): it is not a '[^']+' if (.+?)\.(?= Exclusion \d+:|$)", "", rest).strip()
    if left:
        raise ValueError(f"unparsed definition text: {left[:80]!r}")
    return {"elements": els, "joiner": joiner, "exclusions": exc, "deem": deem}


# ------------------------------------------------------------------------------------------------ the file (state)
def subject_line(f: dict) -> tuple[str, str]:
    pk, item, org = f["pack"], f["item"], f["org"]
    return {"tenancy": ("Occupant", f"{item}, living in a home let by {org}"),
            "safety": ("Incident", f"an incident on a {org} site, reported by {item}"),
            "customs": ("Consignment", f"{item}, shipped by {org}"),
            "insurance": ("Loss", f"water damage at a home insured with {org}, reported by {item}"),
            "procurement": ("Bid", f"a bid from {item}")}[pk]


def background(f: dict, rng) -> list:
    """Usage remark, the outside rule as background (r_facts) and neutral sentences, in a latent-fixed order."""
    pk, ent, T = f["pack"], f["entity"], term(f)
    out = [f"{f['bg_from']} remarked that most people would {'call' if f['usage']['verdict'] else 'not call'} this "
           f"{ent} a '{T}'."]
    if f.get("r_facts"):
        o = f["outside"]
        reg = REGIMES.get(o["regime"], "another rule book")
        verb = "never counts" if o["effect"] == "excl" else "always counts"
        out.append(f"Under {reg}, {article(ent)} {ent} where {cond_text(pk, o['cond'])} {verb} as a '{T}'.")
    pool = list(NEUTRAL[pk])
    rng.shuffle(pool)
    out += pool[: len(f["neutral"])]
    rng.shuffle(out)
    return out


def record_line(f: dict) -> str | None:
    if f.get("record") is None:
        return None
    T = term(f)
    return f"The register lists this {f['entity']} as {'a' if f['record'] else 'not a'} '{T}'."


def render_state(f: dict, fmt: str, rng, definition: bool, rule_note: bool) -> str:
    pk = f["pack"]
    lab, subj = subject_line(f)
    book = PACK[pk]["book"].format(org=f["org"])
    cl = clause_name(f)
    opened = dx.long_date(dx.day_of_2026(f["opened"]))
    inforce = dx.long_date(dx.day_of_2026(f["in_force"]))
    bg = background(f, rng)
    rec = record_line(f)
    note = f"Logged by {f['officer']} on {opened}."
    deftxt = definition_text(f) if definition else None
    rule = (f"{cl} of the {book} (in force from {inforce}) decides whether the {f['entity']} is a '{term(f)}'. "
            + READING) if rule_note else None
    if fmt == "json":
        obj = {"file": {"reference": f["ref"], "kind": PACK[pk]["file"], lab.lower(): subj, "opened": opened,
                        "rule_book": book},
               "facts": {A[pk][a][1]: value_text(pk, a, f["values"][a]) for a in f["order"]},
               "background": bg, "register": rec, "file_notes": [note],
               "definition": {"clause": cl, "in_force_from": inforce, "text": deftxt} if definition else None,
               "rule": rule}
        return mv.render_json(obj)
    if fmt == "sheet":
        lines = [f"File reference: {f['ref']}", f"File type: {PACK[pk]['file']}", f"{lab}: {subj}",
                 f"Opened: {opened}", f"Rule book: {book}", "", "Facts on file:"]
        lines += [f"- {A[pk][a][1]}: {value_text(pk, a, f['values'][a])}" for a in f["order"]]
        lines += ["", "Background:"] + [f"- {b}" for b in bg]
        if rec:
            lines += ["", f"Register: {rec}"]
        lines += ["", f"File note: {note}"]
        if definition:
            lines += ["", f"Definition ({cl}, in force from {inforce}): {deftxt}"]
        if rule_note:
            lines += ["", f"Rule: {rule}"]
        return "\n".join(lines)
    # memo: prose lines
    lines = [f"{PACK[pk]['file'].upper()} {f['ref']}", f"This file concerns {subj}. It was opened on {opened}; "
             f"the rule book is the {book}.", "", "What the file records:"]
    lines += [fact_sentence(pk, a, f["values"][a]) for a in f["order"]]
    lines += ["", "Other notes:"] + bg
    if rec:
        lines += [rec]
    lines += [note]
    if definition:
        lines += ["", f"{cl} (in force from {inforce}) reads: {deftxt}"]
    if rule_note:
        lines += ["", rule]
    return "\n".join(lines)


def parse_state(text: str, fmt: str) -> dict:
    """-> {"pack", "values" (shown attrs), "order", "record", "definition" (text or None), "clause"}."""
    out = {"record": None, "definition": None}
    if fmt == "json":
        o = json.loads(text)
        pk = _pack_of_book(o["file"]["rule_book"])
        lab2attr = {sp[1]: a for a, sp in A[pk].items()}
        out["pack"] = pk
        out["order"] = [lab2attr[k] for k in o["facts"]]
        out["values"] = {lab2attr[k]: parse_value(pk, lab2attr[k], v) for k, v in o["facts"].items()}
        if o.get("register"):
            out["record"] = _parse_record(o["register"])
        if o.get("definition"):
            out["definition"] = o["definition"]["text"]
        return out
    lines = text.split("\n")
    if fmt == "sheet":
        book = next(ln for ln in lines if ln.startswith("Rule book: "))[len("Rule book: "):]
        pk = _pack_of_book(book)
        lab2attr = {sp[1]: a for a, sp in A[pk].items()}
        i = lines.index("Facts on file:") + 1
        out["pack"], out["order"], out["values"] = pk, [], {}
        while i < len(lines) and lines[i].startswith("- "):
            k, v = lines[i][2:].split(": ", 1)
            a = lab2attr[k]
            out["order"].append(a)
            out["values"][a] = parse_value(pk, a, v)
            i += 1
        for ln in lines:
            if ln.startswith("Register: "):
                out["record"] = _parse_record(ln[len("Register: "):])
            m = re.match(r"Definition \((.+?), in force from .+?\): (.+)$", ln)
            if m:
                out["definition"] = m.group(2)
        return out
    # memo
    m = re.search(r"the rule book is the (.+)\.$", lines[1])
    pk = _pack_of_book(m.group(1))
    i = lines.index("What the file records:") + 1
    out["pack"], out["order"], out["values"] = pk, [], {}
    while i < len(lines) and lines[i]:
        r = parse_fact_sentence(pk, lines[i])
        if r is None:
            raise ValueError(f"memo fact line not parsed: {lines[i]!r}")
        out["order"].append(r[0])
        out["values"][r[0]] = r[1]
        i += 1
    for ln in lines:
        if ln.startswith("The register lists this "):
            out["record"] = _parse_record(ln)
        m = re.match(r".+? \(in force from .+?\) reads: (.+)$", ln)
        if m:
            out["definition"] = m.group(1)
    return out


def _pack_of_book(book: str) -> str:
    for pk, p in PACK.items():
        pat = re.escape(p["book"]).replace(re.escape("{org}"), ".+")
        if re.fullmatch(pat, book):
            return pk
    raise ValueError(f"unknown rule book {book!r}")


def _parse_record(s: str) -> bool:
    m = re.fullmatch(r"The register lists this [a-z]+ as (a|not a) '[^']+'\.", s)
    if not m:
        raise ValueError(f"register line {s!r}")
    return m.group(1) == "a"


# ------------------------------------------------------------------------------------------------ questions
def q_text(kind: str, f: dict, wording: str | None = None) -> str:
    ent, T, cl = f["entity"], term(f), clause_name(f)
    if kind == "is":
        return f"Taking {cl} exactly as worded in the definitions, is this {ent} a '{T}'?"
    if kind == "not":
        return f"Taking {cl} exactly as worded in the definitions, does this {ent} fall outside the '{T}' category?"
    if kind == "judge":
        return f"Does {cl}, as worded in the definitions, support the register's listing of this {ent}?"
    if kind == "judge_n":
        return f"Does the register's listing of this {ent} conflict with {cl} as worded in the definitions?"
    if kind == "jb":
        if wording == "fallback":
            return f"Statement: this {ent} is a '{T}' under {cl}. Applying the definition in the file, which option fits?"
        return f"Applying the definition of {cl} set out in the file, which statement holds for this {ent}?"
    if kind == "choice":
        return (f"{cl} makes {article(ent)} {ent} a '{T}' only if every requirement below is met and no exclusion "
                f"below applies. Which listed condition keeps this {ent} from being a '{T}'?")
    raise ValueError(kind)


Q_PATTERNS = (("is", r"Taking (.+?) exactly as worded in the definitions, is this [a-z]+ a '[^']+'\?"),
              ("not", r"Taking (.+?) exactly as worded in the definitions, does this [a-z]+ fall outside the '[^']+' category\?"),
              ("judge", r"Does (.+?), as worded in the definitions, support the register's listing of this [a-z]+\?"),
              ("judge_n", r"Does the register's listing of this [a-z]+ conflict with (.+?) as worded in the definitions\?"),
              ("jb", r"Statement: this [a-z]+ is a '[^']+' under (.+?)\. Applying the definition in the file, which option fits\?"),
              ("jb", r"Applying the definition of (.+?) set out in the file, which statement holds for this [a-z]+\?"),
              ("choice", r"(.+?) makes an? [a-z]+ a '[^']+' only if every requirement below is met and no exclusion "
                         r"below applies\. Which listed condition keeps this [a-z]+ from being a '[^']+'\?"))


def parse_question(s: str) -> tuple[str, str]:
    for kind, pat in Q_PATTERNS:
        m = re.fullmatch(pat, s)
        if m:
            return kind, m.group(1)
    raise ValueError(f"question not recognised: {s!r}")


def yn_defs(kind: str, f: dict) -> dict:
    ent, T, cl = f["entity"], term(f), clause_name(f)
    d = {cl: definition_text(f)}
    met = f"the {ent} is a '{T}' under {cl} as worded above"
    unmet = f"the {ent} is not a '{T}' under {cl} (this includes a file that does not establish what {cl} requires)"
    same = f"the register's listing is what {cl} gives for the facts on file"
    diff = f"the register's listing differs from what {cl} gives for the facts on file"
    d.update({"is": {"yes": met, "no": unmet}, "not": {"yes": unmet, "no": met},
              "judge": {"yes": same, "no": diff}, "judge_n": {"yes": diff, "no": same}}[kind])
    return d


def jb_descs(f: dict) -> tuple[str, str]:
    ent, T, cl = f["entity"], term(f), clause_name(f)
    return f"This {ent} is a '{T}' under {cl}.", f"This {ent} is not a '{T}' under {cl}."


NONE_OPT = "None of them: every requirement is met and no exclusion applies"


def choice_options(f: dict) -> list[tuple[str, tuple]]:
    """[(option text, failing-condition tag)] for every requirement and exclusion (dl_core tags)."""
    d = dl_core.definition_parts(f)
    pk = f["pack"]
    out = [(f"Requirement: {cond_text(pk, c)}", ("el", i)) for i, c in enumerate(d["elements"])]
    for j, (trig, unless, tag) in enumerate(d["exclusions"]):
        s = f"Exclusion: not a '{term(f)}' if {cond_text(pk, trig)}"
        if unless is not None:
            s += f", unless {cond_text(pk, unless)}"
        out.append((s, tag))
    return out


# ------------------------------------------------------------------------------------------------ load + plan
N_EXPORT = 160   # export_latents is prefix-stable: its first 100 are yn2b/f6_devx_latents.json (tested)


def export(n: int = N_EXPORT) -> list:
    import gen3_def_literal as g3   # imported for its latent export only (never its renderers)
    return g3.export_latents("devx", n)


def load() -> list:
    data = export()
    items = []
    for x in data:
        f = x["facts"]
        assert set(f["values"]) == set(f["order"]), x["latent_id"]
        for q, want in x["decisions"].items():
            g, _ = dl_core.decide(f, q)
            assert (list(g) if isinstance(g, tuple) else g) == want, (x["latent_id"], q, g, want)
        items.append(dx.Item(x["latent_id"], x["tier"], f["pack"], "def", f, None, x["truth"],
                             {"decisions": x["decisions"]}))
    return items


LAST_PLAN_REPORT: dict = {}


def plan(items: list, rng) -> list:
    """judge rows for latents with a register record; 25 choice rows among the choice-defined latents; 15 JB rows;
    the rest yes/no. Polarity and format are chosen to balance yes/no gold per tier, format, template, pack and
    polarity (dx.Balancer)."""
    bal, rot = dx.Balancer(rng), dx.Rotor(rng)
    items = sorted(items, key=lambda it: it.lid)
    # latents are taken in export order (the devx stream); counts per view are fixed, and the yes/no pool takes
    # latents until its truth values are balanced (the export is prefix-stable, so more latents are available)
    judge = [it for it in items if it.facts.get("record") is not None][:20]
    rest = [it for it in items if it.facts.get("record") is None]
    choice_ok = [it for it in rest if "choice" in it.extra["decisions"]]
    c_none = [it for it in choice_ok if it.extra["decisions"]["choice"] == "none"]
    c_fail = [it for it in choice_ok if it.extra["decisions"]["choice"] != "none"]
    choice = c_none[:6] + c_fail[:18]        # 'none' gold at 25% (SPEC 4.2 / 4.6: about 1/K)
    left = [it for it in rest if it not in choice]
    truth = {it.lid: bool(dl_core.decide(it.facts, "is")[0]) for it in left}
    jb, yn, cnt = [], [], Counter()
    for it in left:                           # JB: 15 rows, truth 8/7, tiers in export order
        if len(jb) < 15 and cnt[("jb", truth[it.lid])] < (8 if truth[it.lid] else 7):
            jb.append(it)
            cnt[("jb", truth[it.lid])] += 1
    for it in left:                           # yes/no: 41 rows, truth 21/20
        if it in jb or len(yn) >= 41:
            continue
        if cnt[("yn", truth[it.lid])] < (21 if truth[it.lid] else 20):
            yn.append(it)
            cnt[("yn", truth[it.lid])] += 1
    order = None
    out = []
    for it in choice:
        out.append((it, {"q": "choice", "fmt": rot.pick("fmt", FMTS, ("choice",)), "tpl": "choice"}))
    units, meta = [], []
    for it in jb:
        t = bool(dl_core.decide(it.facts, "jb")[0])
        units.append([({"qk": "jb", "tpl": "jb", "fmt": fmt, "tier": it.tier, "pack": it.pack, "pol": 0,
                        "tier_jb": (it.tier, "jb")}, t) for fmt in FMTS])
        meta.append((it, [("jb", fmt) for fmt in FMTS]))
    for group, kinds in ((judge, ("judge", "judge_n")), (yn, ("is", "not"))):
        for it in group:
            cands, cm = [], []
            for k in kinds:
                g = bool(dl_core.decide(it.facts, k)[0])
                for fmt in FMTS:
                    cands.append(({"qk": "yn", "tpl": k, "pol": int(k in ("not", "judge_n")), "fmt": fmt,
                                   "tier": it.tier, "pack": it.pack, "fmt_x_tpl": (fmt, k)}, g))
                    cm.append((k, fmt))
            units.append(cands)
            meta.append((it, cm))
    pick = dx.balance_assign(units, rng)
    for (it, cm), i, cands in zip(meta, pick, units):
        k, fmt = cm[i]
        bal.add(*cands[i])
        out.append((it, {"q": k, "fmt": fmt, "tpl": k}))
    LAST_PLAN_REPORT.clear()
    LAST_PLAN_REPORT.update({"views": dict(Counter(v["q"] for _, v in out)), "balance": bal.report()})
    out.sort(key=lambda x: x[0].lid)
    return out


# ------------------------------------------------------------------------------------------------ render
def render(it: dx.Item, view: dict, fb, rng) -> mv.RowSpec:
    f, q, fmt = it.facts, view["q"], view["fmt"]
    edge = tuple(t for t in dl_core.edge_tags(f) if t in mv.EDGE_TAGS)
    if q in ("is", "not", "judge", "judge_n"):
        g, _ = dl_core.decide(f, q)
        state = render_state(f, fmt, rng, definition=False, rule_note=False)
        return mv.RowSpec("base", "yn", state, q_text(q, f), "yes" if g else "no", FMT_META[fmt], "dx6_" + fmt,
                          "dx6." + q, defs=yn_defs(q, f), polarity=int(q in ("not", "judge_n")),
                          judge=q.startswith("judge"), edge=edge, role="neg" if q in ("not", "judge_n") else "aff")
    if q == "jb":
        t, _ = dl_core.decide(f, "jb")
        y, n = jb_descs(f)
        opts, gold, wording = fb.jb(y, n, bool(t), rng, stratum=("dx6",))
        state = render_state(f, fmt, rng, definition=True, rule_note=False)
        return mv.RowSpec("jb", "jb", state, q_text("jb", f, wording), gold, FMT_META[fmt], "dx6_" + fmt,
                          "dx6.jb" + ("f" if wording == "fallback" else ""), options=opts, polarity=0, edge=edge)
    if q == "choice":
        tag, _ = dl_core.decide(f, "choice")
        opts = choice_options(f)
        by_tag = {t: o for o, t in opts}
        others = [o for o, t in opts]
        if tag == "none":
            options = fb.place(NONE_OPT, others, rng, stratum=("dx6", "choice", len(opts) + 1), none_option=NONE_OPT,
                               none_is_gold=True)
            gold = NONE_OPT
        else:
            gold = by_tag[tuple(tag)]
            options = fb.place(gold, [o for o in others if o != gold], rng, stratum=("dx6", "choice", len(opts) + 1),
                               none_option=NONE_OPT)
        state = render_state(f, fmt, rng, definition=False, rule_note=True)
        return mv.RowSpec("base", "choice", state, q_text("choice", f), gold, FMT_META[fmt], "dx6_" + fmt,
                          "dx6.choice", options=options, none_option=NONE_OPT, edge=edge)
    raise ValueError(q)


# ------------------------------------------------------------------------------------------------ parse-back
FMT_OF_RENDERER = {"dx6_" + k: k for k in FMTS}


def detect_fmt(state: str) -> str:
    if state.startswith("{"):
        return "json"
    if state.startswith("File reference: "):
        return "sheet"
    return "memo"


def parse(g: dict) -> dict:
    """Facts, definition and question rebuilt from the golden row's text (state, instructions, options, card)."""
    fmt = detect_fmt(g["state"])
    st = parse_state(g["state"], fmt)
    pk = st["pack"]
    kind, cl = parse_question(g["instructions"])
    out = {"pack": pk, "kind": kind, "values": st["values"], "order": st["order"], "record": st["record"]}
    if kind in ("is", "not", "judge", "judge_n"):
        cd = mv.card_defs(g["card"])
        out["definition"] = parse_definition(pk, cd[cl])
        low = {k.lower(): v for k, v in cd.items()}
        out["yes_def"], out["no_def"] = low["yes"], low["no"]
    elif kind == "jb":
        out["definition"] = parse_definition(pk, st["definition"])
        out["options"] = list(g["options"])
    else:
        els, exc, opt_tag = [], [], {}
        for o in g["options"]:
            if o == NONE_OPT:
                opt_tag[o] = "none"
                continue
            m = re.fullmatch(r"Requirement: (.+)", o)
            if m:
                els.append(parse_cond(pk, m.group(1)))
                opt_tag[o] = ("el_text", m.group(1))
                continue
            m = re.fullmatch(r"Exclusion: not a '[^']+' if (.+)", o)
            if not m:
                raise ValueError(f"option {o!r}")
            s = m.group(1)
            a, b = (s.split(", unless ", 1) + [None])[:2]
            exc.append((parse_cond(pk, a), parse_cond(pk, b) if b else None))
            opt_tag[o] = ("ex_text", s)
        out["definition"] = {"elements": els, "joiner": "all", "exclusions": exc, "deem": None}
        out["options"] = list(g["options"])
        out["opt_tag"] = opt_tag
    return out


def parsed_facts(p: dict) -> dict:
    d = p["definition"]
    return {"pack": p["pack"], "elements": d["elements"], "joiner": d["joiner"],
            "exclusions": [{"trigger": t, "unless": u} for t, u in d["exclusions"]], "deem": d["deem"],
            "outside": None, "r_card": False, "values": dict(p["values"]), "order": list(p["order"]),
            "record": p["record"]}


def relabel(p: dict, g: dict):
    f = parsed_facts(p)
    k = p["kind"]
    if k in ("is", "not", "judge", "judge_n"):
        v, _ = dl_core.decide(f, k)
        if mv.is_undefined(v):
            raise ValueError("decide undefined on parsed facts")
        return "yes" if v else "no"
    if k == "jb":
        v, _ = dl_core.decide(f, "jb")
        return p["options"][0] if v else p["options"][1]
    tag, _ = dl_core.decide(f, "choice")
    if mv.is_undefined(tag):
        raise ValueError("choice undefined on parsed facts")
    if tag == "none":
        return NONE_OPT
    kind, i = tag
    pk = p["pack"]
    if kind == "el":
        want = cond_text(pk, f["elements"][i])
        return next(o for o, t in p["opt_tag"].items() if t == ("el_text", want))
    x = f["exclusions"][i]
    want = cond_text(pk, x["trigger"]) + (f", unless {cond_text(pk, x['unless'])}" if x["unless"] else "")
    return next(o for o, t in p["opt_tag"].items() if t == ("ex_text", want))


def _canon_cond(c):
    if c is None:
        return None
    c = dict(c)
    if c.get("kind") == "cat":
        c["values"] = tuple(c["values"])
    return tuple(sorted(c.items()))


def project(it: dx.Item) -> dict:
    """The decision-relevant facts of a latent: the applied definition (outside rule written in when r_card), the
    shown values and the register record."""
    f = it.facts
    d = dl_core.definition_parts(f)
    return {"elements": tuple(sorted(_canon_cond(c) for c in d["elements"])), "joiner": d["joiner"],
            "exclusions": tuple(sorted((_canon_cond(t), _canon_cond(u)) for t, u, _ in d["exclusions"])),
            "deem": _canon_cond(d["deem"][0]) if d["deem"] else None,
            "values": tuple((a, f["values"][a]) for a in f["order"]), "record": f.get("record")}


def project_parsed(p: dict) -> dict:
    d = p["definition"]
    out = {"elements": tuple(sorted(_canon_cond(c) for c in d["elements"])), "joiner": d["joiner"],
           "exclusions": tuple(sorted((_canon_cond(t), _canon_cond(u)) for t, u in d["exclusions"])),
           "deem": _canon_cond(d["deem"]), "values": tuple((a, p["values"][a]) for a in p["order"]),
           "record": p["record"]}
    return out


def project_for_row(it: dx.Item, g: dict) -> dict:
    return project(it)
