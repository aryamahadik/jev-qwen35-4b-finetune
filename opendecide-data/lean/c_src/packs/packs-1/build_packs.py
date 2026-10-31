#!/usr/bin/env python3
"""packs-1 builder: Claude-written domain packs (C_DATA_SPEC v4 2.1, step 3) for the industry-and-operations quarter.

Input:  src/*.pack.txt   (Claude-written pack text in the compact format below; one '@@ <slug>' block per pack)
        persona_draw.json (O*NET persona seeds drawn by program, draw_personas.py)
Output: packs.jsonl       (one JSON object per pack, stable id 'p1-<slug>'; every sub-object has a stable id)
        lint_report.json  (counts and lint results; no pack text)

Program-made parts (fixed seed, never Claude-chosen): the person-name pool of each pack (drawn from the
Claude-written first/last name lists below) and the ID pool (SEM-31 alphabet: no I, L or O; look-alike pairs at
Damerau-Levenshtein 1 that never swap a confusable pair; fixed width per register).

Pack text format (one field per line; '#' starts a comment line):
  @@ <slug>
  persona: <O*NET-SOC code from persona_draw.json>
  sector: <sector> / <sub-sector>
  setting: <2-4 sentences>
  org: <invented organisation name> | <what it is>
  role: <the deciding role as the pack's text names it>
  roles: a ; b ; ...                       sites: a ; b ; ...            partners: a ; b ; ...
  item: <singular> | <plural>
  entity: <type> | <plural> | <ID prefix> | name1, name2, ...
  attr: <name> | num | <unit> | <decimals> | <lo>..<hi> [| signed]
  attr: <name> | int | <unit> | <lo>..<hi>
  attr: <name> | cat | v1, v2, ...         attr: <name> | ord | lowest, ..., highest
  attr: <name> | bool | event|state | alias1, alias2, ...
  attr: <name> | date                      attr: <name> | tags | t1, t2, ... (<= 10)
  convert: 1 <U1> = <k> <U2> ; ...
  jargon: word = meaning ; word = meaning
  doc: <document type> > section, section, ...
  status: s1, s2, ...                      outcomes: o1, o2, ... (one line per outcome set)
  conseq: bad: text ; ok: text ; ...       label: word = natural predicate ; ...
  actions: a, b, ...                       objects: a, b, ...
  sources: a ; b ; ...                     scope: <dimension> | v1, v2, ...
  inert: a ; b ; ...                       affixed: word, word, ...
  scale: <name> | lowest, ..., highest
"""
from __future__ import annotations

import hashlib
import json
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[2]
sys.path.insert(0, str(LEAN))
from c_src.common import negcount  # noqa: E402

SEED = 20261003
PACK_VERSION = "1.1"
AGENT = "packs-1"
QUARTER = "industry_and_operations"

# Claude-written name lists (program draws each pack's person pool from these).
FIRST = """Adaeze Aiko Alder Amara Anselm Ardith Arvid Asha Basil Benedetta Bertil Bisi Bram Calla Caspian Cedra Chidi
Cosmin Dagny Dario Delphine Desmond Dilnoza Dorian Ebba Edric Eleni Elio Emeka Enzo Esra Evander Fenna Ferran Folake
Gaspard Gerda Giulia Goran Halvard Hana Hector Hester Idris Ilse Imani Iver Jalen Janek Jovana Juno Kalani Kasimir
Keziah Kiran Klaas Kofi Leandro Lena Linnea Lorcan Maelis Magnus Malia Marek Marisol Matthias Mireille Moana Nadia
Nalani Nasser Nikolai Noor Oisin Olamide Orla Osei Pavla Pedro Petra Quentin Quilla Radek Rania Reuben Rhiannon Rosalind
Rustam Saoirse Sefa Selin Signe Sindri Soraya Stellan Sunniva Tadeo Tamsin Teodor Thandiwe Tobiah Tomasz Ulla Usman
Valeska Vasco Vesna Wendell Wilhelmina Xiomara Yannick Yara Yusuf Zainab Zdenek Zora Anouk Bao Chiara Dov Eitan Farida
Gunnar Hiroko Ines Jorun Kwame Lucan Meruyert Niamh Oren Priya Rafferty Sabine Tariq Ulf Viveka Wren Yevgenia Zuri""".split()
LAST = """Abernathy Achterberg Adeyemi Albescu Alcott Ambrose Andrade Arkwright Asante Bagshaw Balogun Barreto Beaumont
Bellweather Bergqvist Birkeland Blackwood Bramwell Brennan Bruckner Caddell Calloway Castellan Chaudhry Cieslak Coakley
Corcoran Dahlberg Dalca Delacroix Desai Dimitriou Doherty Drummond Duarte Eberhardt Ekwueme Ellery Esposito Fairbairn
Falkenrath Fennimore Ferreira Fitzalan Fonseca Galloway Garnier Gethin Grieve Gustavsen Haddad Halloran Hartigan
Haverkamp Hedlund Holloway Huxtable Ibarra Ingersoll Iwasaki Jablonski Jardine Jovanovic Kaczmarek Kapoor Keane
Kettering Kowalczyk Kristiansen Lachance Landry Larkspur Lindqvist Lombardo Lucero Madsen Magnusson Malakar Marchetti
Mbeki Merriweather Molnar Montague Mwangi Nakashima Navarro Nkemelu Northcott Novak Nyberg Oduya Okonkwo Olafsen Ostrowski
Pacheco Palmquist Pemberton Petrakis Quayle Quintero Radcliffe Ramaswamy Ravensworth Rezaei Rinaldi Rowntree Sadowski
Salazar Sandoval Schuyler Sefton Silvestri Skovgaard Solberg Stanchev Strand Szabo Tadesse Takahashi Thorsby Toivonen
Trevelyan Underhill Urquhart Valdivia Vandermeer Varga Vasquez Wainwright Wakefield Westergaard Whitlock Winterbottom
Yamaguchi Yilmaz Zabala Zielinski Zoltan Okafor Brandt Castillo Dunmore Ekström Halvorsen""".split()

# SEM-31 alphabet (F13): no I, L or O; substitutions never swap a confusable pair.
ID_LETTERS = "ABCDEFGHJKMNPQRSTUVWXYZ"
ID_DIGITS = "0123456789"
CONFUSABLE = {frozenset(p) for p in [("0", "D"), ("1", "7"), ("2", "Z"), ("5", "S"), ("6", "G"), ("8", "B")]}

# Marker-collision and record-status words (MARKERS.md table, F10 R4-02, F8 record-status lint, F7 3.1 markers).
COLLISION = set("""unknown null none no false true yes tbd na record records recorded recording unrecorded list lists
listed listing unlisted stated unstated missing blank pending known unknown available unavailable applicable
inapplicable specified unspecified determined undetermined log logs logged logging logbook documented registered
reported absent present partial maybe""".split())
COLLISION_PHRASES = ["not recorded", "not listed", "on file", "not checked", "not provided", "n/a"]
# F7 U03 banned factor stems (Boolean factors are never a risk, plan, possibility, request, schedule or expectation).
# v1.1 (review fix): stems in any form, applied to Boolean names and their aliases.
F7_BANNED = re.compile(r"\b(risk(s|y|ier|iest|ed|ing)?|possib\w*|request\w*|schedul\w*|plan|plans|planned|planning|"
                       r"expect\w*)\b", re.I)
# F8-R4-06 record-status words in any form (v1.1 review fix): "record" and "log" in every form, plus the closed list.
# Names: error. Every other pack text (setting, meanings, consequences, ...): error too, since packs feed rendered rows.
REC_LOG = re.compile(r"\b(un)?record\w*|\blog(s|ged|ging|ger|gers|book|books|sheet|sheets)?\b", re.I)
F8_STATUS = re.compile(REC_LOG.pattern + r"|\bon file\b|\bdocumented\b|\bregistered\b|\breported\b", re.I)
# Inert fact types (v1.1 review fix): unique across packs-1 (no cross-pack boilerplate) and disjoint from the pack's
# own case vocabulary (F7 U01 / M4, F13 SEM-62: names no case attribute, value, status, outcome, label or decision verb).
INERT_STOP = set("""a an the was were is are be been got get gets new of to in on at by for from with and its it into
onto up out off over one two some more fresh first another""".split())
DATE_WORDS = set("""monday tuesday wednesday thursday friday saturday sunday today yesterday tomorrow week weeks weekly
month months monthly year years yearly annual daily morning evening night weekend date dated deadline""".split())
NAME_RX = re.compile(r"[A-Za-z0-9]")
# Words that start like a negating affix but do not negate their stem (warnings skip them).
AFFIX_OK = set("""unit units union uniform uniforms under underside underground underpass undercoat underlay unload unloaded
unloading unpack unpacked unlock unlocked unroll unwind unwound unified unique universal distribution distributor
dispatch dispatcher dispatched district display displays distance disc discs disk dish dishes dispenser discharge
discharged discount mission mist misting mister dissolved dissolve unseat unclip unbolt undercut unsold""".split())
# Negative-implicative stems that F1/F5 readers treat as negation in a name (never in names; declare affixed words).
NEG_STEMS = set("""failed fails rejected refused refusal declined denied without lacks lacking lack omitted
neglected cannot never""".split())


def norm_tokens(s: str):
    return [t for t in re.split(r"[\s\-_/.,;:()'\"]+", s.lower()) if t]


def collisions(s: str):
    low = " " + s.lower() + " "
    hits = [t for t in norm_tokens(s) if t in COLLISION]
    hits += [p for p in COLLISION_PHRASES if f" {p} " in low or low.strip() == p]
    if s.strip() in {"-", "?", "--", "x", "X", "Y", "N", "0"}:
        hits.append(s.strip())
    return hits


def split_list(v: str, sep: str):
    return [x.strip() for x in v.split(sep) if x.strip()]


def parse_range(r: str):
    m = re.fullmatch(r"\s*(-?[\d.]+)\s*\.\.\s*(-?[\d.]+)\s*", r)
    if not m:
        raise ValueError(f"bad range {r!r}")
    return float(m.group(1)), float(m.group(2))


def parse_blocks(text: str, fname: str):
    packs, cur = [], None
    for ln, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("@@"):
            cur = {"_slug": line[2:].strip(), "_file": fname, "_line": ln, "_fields": []}
            packs.append(cur)
            continue
        if cur is None or ":" not in line:
            raise ValueError(f"{fname}:{ln}: line outside a pack or without 'key:'")
        k, v = line.split(":", 1)
        cur["_fields"].append((k.strip(), v.strip(), ln))
    return packs


def build_pack(blk, personas, errs):
    slug = blk["_slug"]
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
        errs.append(f"{slug}: slug format")
    pid = f"p1-{slug}"
    p = {"id": pid, "pack_version": PACK_VERSION, "agent": AGENT, "quarter": QUARTER}
    lists = {k: [] for k in ["entity", "attr", "convert", "jargon", "doc", "outcomes", "conseq", "label", "scale",
                             "inert", "sources", "affixed"]}
    single = {}
    for k, v, ln in blk["_fields"]:
        if k in ("entity", "attr", "doc", "outcomes", "scale"):
            lists[k].append(v)
        elif k in ("convert", "jargon", "conseq", "label", "inert", "sources"):
            lists[k].extend(split_list(v, " ; "))
        elif k == "affixed":
            lists[k].extend(split_list(v, ","))
        else:
            if k in single:
                errs.append(f"{slug}: duplicate key {k}")
            single[k] = v
    need = ["persona", "sector", "setting", "org", "role", "roles", "sites", "partners", "item", "status", "actions",
            "objects", "scope"]
    for k in need:
        if k not in single:
            errs.append(f"{slug}: missing {k}")
            single.setdefault(k, "")
    code = single["persona"]
    if code not in personas:
        errs.append(f"{slug}: persona {code} not in the draw")
    per = personas.get(code, {})
    sec = split_list(single["sector"], " / ")
    org = split_list(single["org"], " | ")
    item = split_list(single["item"], " | ")
    p.update({
        "sector": sec[0] if sec else "", "sub_sector": sec[1] if len(sec) > 1 else "",
        "setting": single["setting"],
        "org": {"name": org[0] if org else "", "kind": org[1] if len(org) > 1 else ""},
        "persona_seed": {"onet_code": code, "onet_title": per.get("onet_title"), "onet_group": per.get("group"),
                         "source": "O*NET 31.0 Occupation Data (main titles), CC BY 4.0"},
        "deciding_role": single["role"],
        "roles": split_list(single["roles"], " ; "),
        "sites": split_list(single["sites"], " ; "),
        "partner_orgs": split_list(single["partners"], " ; "),
        "item_kind": {"singular": item[0] if item else "", "plural": item[1] if len(item) > 1 else ""},
    })
    ents = []
    for i, e in enumerate(lists["entity"], 1):
        parts = split_list(e, " | ")
        if len(parts) != 4:
            errs.append(f"{slug}: entity line needs 4 parts: {e[:40]}")
            continue
        ents.append({"eid": f"{pid}:e{i:02d}", "type": parts[0], "plural": parts[1], "id_prefix": parts[2],
                     "names": split_list(parts[3], ",")})
    p["entity_types"] = ents
    attrs = []
    for i, a in enumerate(lists["attr"], 1):
        parts = [x.strip() for x in a.split(" | ")]
        name, typ = parts[0], parts[1] if len(parts) > 1 else ""
        d = {"aid": f"{pid}:a{i:02d}", "name": name, "type": typ}
        try:
            if typ == "num":
                d["unit"], d["decimals"] = parts[2], int(parts[3])
                d["range"] = list(parse_range(parts[4]))
                d["signed"] = len(parts) > 5 and parts[5] == "signed"
                d["nonneg"] = not d["signed"]
                d["grid"] = 10 ** (-d["decimals"])
            elif typ == "int":
                d["unit"] = parts[2]
                lo, hi = parse_range(parts[3])
                d["range"], d["decimals"], d["nonneg"], d["signed"], d["grid"] = [int(lo), int(hi)], 0, lo >= 0, lo < 0, 1
            elif typ in ("cat", "ord", "tags"):
                d["values"] = split_list(parts[2], ",")
                if typ == "ord":
                    d["ordered"] = "ascending"
            elif typ == "bool":
                d["kind"] = parts[2]
                d["aliases"] = split_list(parts[3], ",") if len(parts) > 3 else []
                # F1 R8: the field a phrasing of this Boolean presupposes. packs-1 declares none (every Boolean is
                # an independent event or state of the case); generators keep their own phrasings to that.
                d["presupposes"] = None
            elif typ == "date":
                pass
            else:
                errs.append(f"{slug}: attr {name}: unknown type {typ}")
        except (IndexError, ValueError) as ex:
            errs.append(f"{slug}: attr {name}: {ex}")
        attrs.append(d)
    p["attributes"] = attrs
    p["unit_conversions"] = lists["convert"]
    units = sorted({a["unit"] for a in attrs if a.get("unit")})
    p["units"] = units
    jar = []
    for i, j in enumerate(lists["jargon"], 1):
        if " = " not in j:
            errs.append(f"{slug}: jargon without ' = ': {j[:30]}")
            continue
        w, m = j.split(" = ", 1)
        jar.append({"jid": f"{pid}:j{i:02d}", "term": w.strip(), "meaning": m.strip()})
    p["jargon"] = jar
    docs = []
    for i, dline in enumerate(lists["doc"], 1):
        if " > " not in dline:
            errs.append(f"{slug}: doc without ' > '")
            continue
        n, s = dline.split(" > ", 1)
        docs.append({"did": f"{pid}:d{i:02d}", "type": n.strip(), "sections": split_list(s, ",")})
    p["document_types"] = docs
    p["status_values"] = split_list(single["status"], ",")
    p["outcome_sets"] = [{"oid": f"{pid}:o{i:02d}", "outcomes": split_list(o, ",")}
                         for i, o in enumerate(lists["outcomes"], 1)]
    cons = []
    for i, c in enumerate(lists["conseq"], 1):
        m = re.match(r"(bad|ok):\s*(.+)", c)
        if not m:
            errs.append(f"{slug}: conseq tag: {c[:30]}")
            continue
        cons.append({"cid": f"{pid}:c{i:02d}", "tag": "bad" if m.group(1) == "bad" else "not_bad", "text": m.group(2)})
    p["consequences"] = cons
    labs = []
    for i, l in enumerate(lists["label"], 1):
        if " = " not in l:
            errs.append(f"{slug}: label without ' = ': {l[:30]}")
            continue
        w, m = l.split(" = ", 1)
        labs.append({"lid": f"{pid}:l{i:02d}", "word": w.strip(), "natural_predicate": m.strip()})
    p["label_words"] = labs
    p["actions"] = split_list(single["actions"], ",")
    p["objects"] = split_list(single["objects"], ",")
    p["source_names"] = lists["sources"]
    sc = split_list(single["scope"], " | ")
    p["scope_dimension"] = {"name": sc[0] if sc else "", "values": split_list(sc[1], ",") if len(sc) > 1 else []}
    p["inert_fact_types"] = lists["inert"]
    p["affixed_negatives"] = lists["affixed"]
    scales = []
    for i, s in enumerate(lists["scale"], 1):
        parts = split_list(s, " | ")
        if len(parts) != 2:
            errs.append(f"{slug}: scale format")
            continue
        scales.append({"sid": f"{pid}:s{i:02d}", "name": parts[0], "levels": split_list(parts[1], ","),
                       "order": "ascending (usual rank = position)"})
    p["ordered_scales"] = scales
    return p


def dl1(a, b):
    """True when a and b are at Damerau-Levenshtein distance exactly 1 (same length: substitution or transposition)."""
    if len(a) != len(b) or a == b:
        return False
    diff = [i for i in range(len(a)) if a[i] != b[i]]
    if len(diff) == 1:
        return True
    return len(diff) == 2 and diff[1] == diff[0] + 1 and a[diff[0]] == b[diff[1]] and a[diff[1]] == b[diff[0]]


def make_id_pool(pid, ents, rs):
    """Per entity type: 32 IDs '<prefix>-<4 chars>' (fixed width per register), 8 look-alike pairs at DL 1."""
    pool = []
    for e in ents:
        pre = e["id_prefix"].upper()
        ids, pairs = [], []
        seen = set()

        def fresh():
            while True:
                body = "".join(rs.choice(ID_DIGITS if k != 1 else ID_LETTERS + ID_DIGITS) for k in range(4))
                s = f"{pre}-{body}"
                if s not in seen:
                    return s
        while len(ids) < 16:
            s = fresh()
            seen.add(s)
            ids.append(s)
        for base in ids[:8]:
            body = base.split("-", 1)[1]
            for _ in range(200):
                k = rs.randrange(4)
                if rs.random() < 0.3 and k < 3 and body[k] != body[k + 1]:
                    nb = body[:k] + body[k + 1] + body[k] + body[k + 2:]
                else:
                    alph = ID_LETTERS + ID_DIGITS if k == 1 else ID_DIGITS
                    c = rs.choice(alph)
                    if c == body[k] or frozenset((c, body[k])) in CONFUSABLE:
                        continue
                    nb = body[:k] + c + body[k + 1:]
                if any(frozenset((x, y)) in CONFUSABLE for x, y in zip(body, nb) if x != y):
                    continue
                s = f"{pre}-{nb}"
                if s not in seen and dl1(body, nb):
                    seen.add(s)
                    pairs.append([base, s])
                    break
        while len(ids) + len(pairs) < 32:
            s = fresh()
            seen.add(s)
            ids.append(s)
        allids = ids + [b for _, b in pairs]
        rs.shuffle(allids)
        pool.append({"eid": e["eid"], "register": e["type"], "width": len(allids[0]), "ids": allids,
                     "lookalike_pairs": pairs})
    return pool


def check_id_pool(p, errs):
    pid = p["id"]
    pres = [e["id_prefix"] for e in p["entity_types"]]
    if len(set(pres)) != len(pres):
        errs.append(f"{pid}: entity ID prefixes repeat")
    total = 0
    for reg in p["id_pool"]:
        ids = reg["ids"]
        total += len(ids)
        if len(set(ids)) != len(ids) or len({len(x) for x in ids}) != 1:
            errs.append(f"{pid}: id pool {reg['register']} not unique or not fixed width")
        if any(ch in "ILO" for x in ids for ch in x):
            errs.append(f"{pid}: id pool {reg['register']} uses I, L or O")
        for a, b in reg["lookalike_pairs"]:
            if not dl1(a, b) or any(frozenset((x, y)) in CONFUSABLE for x, y in zip(a, b) if x != y):
                errs.append(f"{pid}: look-alike pair {a}/{b} breaks SEM-31")
        if len(reg["lookalike_pairs"]) < 6:
            errs.append(f"{pid}: id pool {reg['register']} has < 6 look-alike pairs")
    if total < 60:
        errs.append(f"{pid}: id pool total {total} < 60 (F13 X7)")


def lint(p, errs, warns):
    pid = p["id"]
    mins = {"roles": 6, "sites": 6, "partner_orgs": 6, "entity_types": 2, "jargon": 8, "document_types": 4,
            "status_values": 4, "outcome_sets": 2, "consequences": 8, "label_words": 12, "actions": 6, "objects": 6,
            "source_names": 6, "inert_fact_types": 10, "affixed_negatives": 2, "ordered_scales": 2}
    for k, n in mins.items():
        if len(p[k]) < n:
            errs.append(f"{pid}: {k} {len(p[k])} < {n}")
    if len(p["scope_dimension"]["values"]) < 3:
        errs.append(f"{pid}: scope values < 3")
    at = p["attributes"]
    by = lambda t: [a for a in at if a["type"] in t]  # noqa: E731
    for t, n in [(("num", "int"), 4), (("cat", "ord"), 3), (("bool",), 3), (("date",), 1), (("tags",), 1)]:
        if len(by(t)) < n:
            errs.append(f"{pid}: attrs of type {t} {len(by(t))} < {n}")
    if len(at) < 13:
        errs.append(f"{pid}: attributes {len(at)} < 13")
    for e in p["entity_types"]:
        if len(e["names"]) < 8:
            errs.append(f"{pid}: entity {e['type']} names {len(e['names'])} < 8")
        if not re.fullmatch(r"[A-HJKMNP-Z]{2,3}", e["id_prefix"]):
            errs.append(f"{pid}: id prefix {e['id_prefix']} breaks SEM-31")
    for a in at:
        if a["type"] in ("num", "int"):
            lo, hi = a.get("range", [0, 0])
            if not lo < hi:
                errs.append(f"{pid}: {a['name']} range")
        if a["type"] in ("cat", "ord", "tags"):
            vals = a.get("values", [])
            if len(vals) < 3 or len(set(v.lower() for v in vals)) != len(vals):
                errs.append(f"{pid}: {a['name']} values {len(vals)} or duplicates")
            if a["type"] == "tags" and len(vals) > 10:
                errs.append(f"{pid}: {a['name']} tags > 10")
        if a["type"] == "bool":
            if a.get("kind") not in ("event", "state"):
                errs.append(f"{pid}: {a['name']} bool kind")
            for s in [a["name"]] + a.get("aliases", []):
                if F7_BANNED.search(s):
                    errs.append(f"{pid}: {s!r} ({a['aid']}) uses an F7 banned factor stem")
            if len(a.get("aliases", [])) < 2:
                errs.append(f"{pid}: {a['name']} has < 2 aliases")
    # Collision and negation lint on every name-like string (names, values, units, statuses, outcomes, levels, words).
    names = [a["name"] for a in at] + [v for a in at for v in a.get("values", [])] + p["units"]
    names += p["status_values"] + [o for s in p["outcome_sets"] for o in s["outcomes"]]
    names += [l for s in p["ordered_scales"] for l in s["levels"]] + [s["name"] for s in p["ordered_scales"]]
    names += [e["type"] for e in p["entity_types"]] + [e["plural"] for e in p["entity_types"]]
    names += [d["type"] for d in p["document_types"]] + [s for d in p["document_types"] for s in d["sections"]]
    names += [l["word"] for l in p["label_words"]] + [j["term"] for j in p["jargon"]]
    names += [p["item_kind"]["singular"], p["item_kind"]["plural"], p["scope_dimension"]["name"]]
    names += p["scope_dimension"]["values"] + p["actions"] + p["objects"]
    names += [n for e in p["entity_types"] for n in e["names"]] + p["sites"] + p["partner_orgs"] + p["roles"]
    # v1.1 (review fix): Boolean aliases, source names, inert fact types, the org name and the deciding role too.
    names += [al for a in at for al in a.get("aliases", [])] + p["source_names"] + p["inert_fact_types"]
    names += [p["org"]["name"], p["deciding_role"]]
    affixed = [w.lower() for w in p["affixed_negatives"]]
    for s in names:
        c = collisions(s)
        if c:
            errs.append(f"{pid}: collision word {c} in name {s!r}")
        if REC_LOG.search(s):
            errs.append(f"{pid}: record-status word {REC_LOG.search(s).group(0)!r} in name {s!r} (F8-R4-06)")
        nc = negcount.count(s)
        if nc.k_all or nc.k_syn:
            errs.append(f"{pid}: negation in name {s!r}")
        if any(t in affixed for t in norm_tokens(s)):
            errs.append(f"{pid}: declared affixed word used in name {s!r}")
        for t in norm_tokens(s):
            if (t.startswith(("un", "non", "dis", "mis")) or t.endswith("less")) and t not in AFFIX_OK:
                warns.append(f"{pid}: check affix {t!r} in {s!r}")
            if t in NEG_STEMS:
                errs.append(f"{pid}: negative stem {t!r} in name {s!r}")
    for w in p["affixed_negatives"]:
        if not re.match(r"(un|in|im|ir|il|non-?|dis|mis)", w.lower()):
            errs.append(f"{pid}: affixed word {w!r} has no negating prefix")
    anames = sorted((a["name"] for a in at), key=len, reverse=True)
    for l in p["label_words"]:
        pred = l["natural_predicate"]
        hit = [n for n in anames if pred.startswith(n + " ")]
        if not hit:
            errs.append(f"{pid}: label {l['word']!r} predicate names no attribute at its start")
            continue
        a = next(x for x in at if x["name"] == hit[0])
        rest = pred[len(hit[0]) + 1:]
        if a["type"] in ("cat", "ord"):
            m = re.fullmatch(r"is (.+)", rest)
            vals = re.split(r" or ", m.group(1)) if m else []
            if not m or any(v not in a["values"] for v in vals):
                errs.append(f"{pid}: label {l['word']!r} predicate values not in {a['name']!r}")
        elif a["type"] == "tags":
            m = re.fullmatch(r"include (.+)", rest)
            vals = re.split(r" or ", m.group(1)) if m else []
            if not m or any(v not in a["values"] for v in vals):
                errs.append(f"{pid}: label {l['word']!r} predicate tags not in {a['name']!r}")
        elif a["type"] == "bool":
            want = "occurred" if a["kind"] == "event" else "is in place"
            if rest != want:
                errs.append(f"{pid}: label {l['word']!r} predicate should read '{want}'")
        elif a["type"] in ("num", "int"):
            m = re.fullmatch(r"(above|under) (-?[\d.]+)", rest)
            m2 = re.fullmatch(r"(above|under) (.+)", rest)
            if m:
                v = float(m.group(2))
                if not a["range"][0] <= v <= a["range"][1]:
                    errs.append(f"{pid}: label {l['word']!r} threshold outside the range of {a['name']!r}")
            elif not (m2 and m2.group(2) in anames):
                errs.append(f"{pid}: label {l['word']!r} numeric predicate form")
    lw = [l["word"].lower() for l in p["label_words"]]
    if len(set(lw)) != len(lw):
        errs.append(f"{pid}: duplicate label words")
    for txt in [flat_text(p)]:
        if re.search(r"\((cut|unused|not used|gone|none|dropped)\)|\w-free\b", txt):
            errs.append(f"{pid}: placeholder text left in pack")
        for m in F8_STATUS.finditer(txt):
            errs.append(f"{pid}: record-status word {m.group(0)!r} in pack text (F8-R4-06)")
    # Inert fact types: disjoint from the pack's case vocabulary; no digits or date words (F7 U01/M4, F13 SEM-62).
    vocab = set()
    for s in ([a["name"] for a in at] + [v for a in at for v in a.get("values", [])]
              + [al for a in at for al in a.get("aliases", [])] + p["status_values"]
              + [o for s in p["outcome_sets"] for o in s["outcomes"]] + [l["word"] for l in p["label_words"]]
              + [lv for s in p["ordered_scales"] for lv in s["levels"]] + [j["term"] for j in p["jargon"]]
              + [n for e in p["entity_types"] for n in e["names"]] + p["scope_dimension"]["values"] + p["actions"]):
        vocab.update(t for t in norm_tokens(s) if t not in INERT_STOP)
    for s in p["inert_fact_types"]:
        toks = [t for t in norm_tokens(s) if t not in INERT_STOP]
        hit = sorted({t for t in toks if t in vocab or t.rstrip("s") in vocab or t + "s" in vocab})
        if hit:
            errs.append(f"{pid}: inert {s!r} shares case words {hit}")
        if re.search(r"\d", s) or any(t in DATE_WORDS for t in toks):
            errs.append(f"{pid}: inert {s!r} has a number or date word")
    for j in p["jargon"]:
        if not re.fullmatch(r"[a-z]{5,10}", j["term"]):
            errs.append(f"{pid}: jargon {j['term']!r} is not one lower-case 5-10 letter coined word")
    for k in ("roles", "sites", "partner_orgs", "actions", "objects", "inert_fact_types", "source_names"):
        lst = [x.lower() for x in p[k]]
        if len(set(lst)) != len(lst):
            errs.append(f"{pid}: duplicates in {k}")


def flat_text(p):
    out = []

    def walk(o, key=""):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("id", "aid", "eid", "jid", "did", "oid", "cid", "lid", "sid", "persona_seed", "people",
                         "id_pool", "provenance", "agent", "quarter", "pack_version"):
                    continue
                walk(v, k)
        elif isinstance(o, list):
            for v in o:
                walk(v, key)
        elif isinstance(o, str):
            out.append(o)
    walk(p)
    return " ".join(out)


def main():
    draw = json.loads((HERE / "persona_draw.json").read_text())
    personas = {d["onet_code"]: d for d in draw["drawn"]}
    for g in draw["groups"]:
        for s in g["spares"]:
            personas.setdefault(s["onet_code"], {**s, "group": g["group"], "spare": True})
    errs, warns, packs = [], [], []
    srcs = sorted((HERE / "src").glob("*.pack.txt"))
    for f in srcs:
        for blk in parse_blocks(f.read_text(), f.name):
            packs.append((blk, build_pack(blk, personas, errs)))
    seen_ids, seen_persona, seen_org = set(), {}, {}
    out = []
    for blk, p in packs:
        if p["id"] in seen_ids:
            errs.append(f"{p['id']}: duplicate id")
        seen_ids.add(p["id"])
        code = p["persona_seed"]["onet_code"]
        if code in seen_persona:
            errs.append(f"{p['id']}: persona {code} also used by {seen_persona[code]}")
        seen_persona[code] = p["id"]
        on = p["org"]["name"].lower()
        if on in seen_org:
            errs.append(f"{p['id']}: org name reused from {seen_org[on]}")
        seen_org[on] = p["id"]
        lint(p, errs, warns)
        rs = random.Random(int(hashlib.sha256(f"{SEED}:{p['id']}".encode()).hexdigest(), 16))
        firsts = rs.sample(FIRST, 24)
        lasts = rs.sample(LAST, 24)
        p["people"] = [f"{a} {b}" for a, b in zip(firsts, lasts)]
        p["id_pool"] = make_id_pool(p["id"], p["entity_types"], rs)
        check_id_pool(p, errs)
        p["provenance"] = {
            "author": "Claude (packs-1 agent), written for C round 1 after A15/A16",
            "licence": "CC0 1.0 (Claude-written pack; persona title from O*NET, CC BY 4.0, credited)",
            "parents": ["gd_onet_occupation"],
            "program_parts": ["people (drawn from the builder's Claude-written name lists, fixed seed)",
                              "id_pool (SEM-31 alphabet, look-alike pairs, fixed seed)", "persona_seed (draw_personas.py)"],
            "source_file": blk["_file"], "seed": SEED}
        p["pack_sha256"] = hashlib.sha256(json.dumps({k: v for k, v in p.items() if k != "pack_sha256"},
                                                     sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        out.append(p)
    # Diversity (G11): ROUGE-L F between every pair of packs' flattened value text (word level, LCS).
    toks = [norm_tokens(flat_text(p)) for p in out]
    worst = (0.0, None, None)
    if "--no-rouge" not in sys.argv:
        for i in range(len(toks)):
            for j in range(i + 1, len(toks)):
                r = rouge_l(toks[i], toks[j])
                if r > worst[0]:
                    worst = (r, out[i]["id"], out[j]["id"])
                if r >= 0.7:
                    errs.append(f"ROUGE-L {r:.2f} between {out[i]['id']} and {out[j]['id']}")
    seen_j = {}
    for p in out:
        for j in p["jargon"]:
            if j["term"] in seen_j:
                errs.append(f"{p['id']}: jargon {j['term']!r} also in {seen_j[j['term']]}")
            seen_j.setdefault(j["term"], p["id"])
    # v1.1 (review fix): no inert fact type is shared by two packs (cross-pack boilerplate is a surface cue).
    seen_i = {}
    for p in out:
        for s in p["inert_fact_types"]:
            k = s.lower()
            if k in seen_i:
                errs.append(f"{p['id']}: inert {s!r} also in {seen_i[k]}")
            seen_i.setdefault(k, p["id"])
    out.sort(key=lambda p: p["id"])
    with open(HERE / "packs.jsonl", "w") as fh:
        for p in out:
            fh.write(json.dumps(p, ensure_ascii=False) + "\n")
    rep = {"packs": len(out), "errors": errs, "warnings": warns, "rouge_l_max": round(worst[0], 4),
           "rouge_l_max_pair": [worst[1], worst[2]], "src_files": [f.name for f in srcs]}
    (HERE / "lint_report.json").write_text(json.dumps(rep, indent=1) + "\n")
    print(f"packs {len(out)}; errors {len(errs)}; warnings {len(warns)}; rouge_l_max {worst[0]:.3f}")
    for e in errs[:80]:
        print("ERR", e)
    for w in warns[:40]:
        print("WARN", w)
    return 1 if errs else 0


def lcs_len(a, b):
    """LCS length by the bit-parallel method (Hyyro 2004); equals the dynamic-programming LCS."""
    if not a or not b:
        return 0
    masks = {}
    for i, t in enumerate(b):
        masks[t] = masks.get(t, 0) | (1 << i)
    full = (1 << len(b)) - 1
    v = full
    for t in a:
        m = masks.get(t, 0)
        u = v & m
        v = ((v + u) | (v - u)) & full
    return len(b) - bin(v).count("1")


def lcs_dp(a, b):
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b, 1):
            cur.append(prev[j - 1] + 1 if x == y else max(prev[j], cur[j - 1]))
        prev = cur
    return prev[-1]


def rouge_l(a, b):
    lcs = lcs_len(a, b)
    if lcs == 0:
        return 0.0
    p, r = lcs / len(a), lcs / len(b)
    return 2 * p * r / (p + r)


if __name__ == "__main__":
    sys.exit(main())
