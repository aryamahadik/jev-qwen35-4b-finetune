#!/usr/bin/env python3
"""A42-D 12 G-proxy builder, wave 8 (16 Oct 2026). CPU only, no model. NEVER TRAINED ON.

Replaces gp_wwpdb and gp_eurostat (A48 e: their names appear in G-block texts) with gp_unicode, gp_iana_ports and gp_hgnc,
keeping gp_ourairports. Reuses build.py (the 15 Oct builder: sampling, row format, polarity audit) as a library; only the
loaders and the task lists below are new. Same design: every task has question VARIANTS, gold = the variant predicate on the
record fields the state shows (program gold, nothing relabelled), no negation word in any instruction, card rows carry a
swap-safe two-line card, card-free rows put the rule in the question, cluster = meta.source_doc.
Run from lean/c2_build:  nice -n 10 ../../.venv/bin/python -B meta_src/gproxy/build_w8.py
"""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build as B  # noqa: E402
from build import V, fmt_num, pb  # noqa: E402
from c2_kit import polarity  # noqa: E402

B.SEED = "gproxy-v2-16oct2026"
B.SNAPSHOT = "2026-10-16"
B.SCALE = 1.0
B.SRC_SCALE = {"gp_ourairports": 1.0, "gp_unicode": 0.8, "gp_hgnc": 1.0}   # gp_iana_ports dropped: its registry name appears in G-block raw text (A48 e)

GC = {"Lu": "Letter, uppercase", "Ll": "Letter, lowercase", "Lt": "Letter, titlecase", "Lm": "Letter, modifier", "Lo": "Letter, other",
      "Mn": "Mark, nonspacing", "Mc": "Mark, spacing combining", "Me": "Mark, enclosing", "Nd": "Number, decimal digit",
      "Nl": "Number, letter", "No": "Number, other", "Pc": "Punctuation, connector", "Pd": "Punctuation, dash",
      "Ps": "Punctuation, open", "Pe": "Punctuation, close", "Pi": "Punctuation, initial quote", "Pf": "Punctuation, final quote",
      "Po": "Punctuation, other", "Sm": "Symbol, math", "Sc": "Symbol, currency", "Sk": "Symbol, modifier", "So": "Symbol, other",
      "Zs": "Separator, space", "Zl": "Separator, line", "Zp": "Separator, paragraph", "Cc": "Other, control", "Cf": "Other, format"}


# ------------------------------------------------------------------------------------------------------------ unicode
def load_unicode() -> list:
    recs = []
    for ln in (HERE / "raw/unicode/UnicodeData.txt").read_text(encoding="utf-8").splitlines():
        p = ln.split(";")
        if len(p) < 15 or p[1].startswith("<") or p[2] not in GC:
            continue
        cp = int(p[0], 16)
        if p[2] in ("Cc", "Cf"):
            continue
        recs.append({"key": p[0], "doc": "unicode:U+" + p[0], "cp": cp, "hex": p[0], "name": p[1], "gc": p[2], "ccc": int(p[3]),
                     "bidi": p[4], "decomp": p[5], "num": p[8], "mirror": p[9], "upper": p[12], "lower": p[13]})
    return recs


def unicode_state(r: dict) -> str:
    return (f"Unicode character record (UnicodeData).\nCode point: U+{r['hex']}\nName: {r['name']}\n"
            f"General category: {r['gc']} ({GC[r['gc']]})\nCanonical combining class: {r['ccc']}\nBidirectional class: {r['bidi']}\n"
            f"Decomposition mapping: {r['decomp'] or 'empty'}\nNumeric value: {r['num'] or 'empty'}\nMirrored: {r['mirror']}\n"
            f"Simple uppercase mapping: {r['upper'] or 'empty'}\nSimple lowercase mapping: {r['lower'] or 'empty'}")


def has_word(field: str, w: str):
    return lambda r: re.search(r"(?<![A-Z0-9])" + w + r"(?![A-Z0-9])", r[field].upper()) is not None


def unicode_tasks() -> list:
    T = []
    L = lambda r: r["gc"][0] == "L"
    T.append(dict(id="U.letter", n=44, elig=lambda r: True, variants=[
        V("Is the general category of this character a letter category (it begins with L)?", L,
          ("Is this character a letter?", "The general category begins with L.", "The general category begins with M, N, P, S or Z.")),
        V("Is the general category of this character a mark, number, punctuation, symbol or separator category?", lambda r: not L(r),
          ("Is this character a non-letter?", "The general category begins with M, N, P, S or Z.", "The general category begins with L."))]))
    for code, lab in (("Lu", "Lu"), ("Ll", "Ll"), ("Nd", "Nd"), ("So", "So"), ("Po", "Po"), ("Mn", "Mn"), ("Lo", "Lo"), ("Sm", "Sm")):
        T.append(dict(id=f"U.gc{code}", n=26, elig=lambda r: True, variants=[
            V(f"Is the general category of this character {lab}?", lambda r, c=code: r["gc"] == c, None)]))
    for t in ("007F", "00FF", "07FF", "FFFF", "1FFFF"):
        tv = int(t, 16)
        T.append(dict(id=f"U.cp{t}", n=26, elig=lambda r: True, variants=[
            V(f"Is the code point above U+{t}?", lambda r, tv=tv: r["cp"] > tv,
              ("Is this code point a high code point?", f"The code point is above U+{t}.", f"The code point is U+{t} or lower.")),
            V(f"Is the code point U+{t} or lower?", lambda r, tv=tv: r["cp"] <= tv,
              ("Is this code point a low code point?", f"The code point is U+{t} or lower.", f"The code point is above U+{t}."))]))
    T.append(dict(id="U.mirror", n=30, elig=lambda r: True, variants=[V("Is the mirrored property of this character Y?", lambda r: r["mirror"] == "Y", None)]))
    T.append(dict(id="U.numeric", n=34, elig=lambda r: True, variants=[
        V("Does this record have a numeric value?", lambda r: bool(r["num"]),
          ("Does this character stand for a number?", "The numeric value field is filled.", "The numeric value field is empty."))]))
    T.append(dict(id="U.decomp", n=34, elig=lambda r: True, variants=[
        V("Does this record have a decomposition mapping?", lambda r: bool(r["decomp"]),
          ("Can this character be split into parts?", "The decomposition mapping field is filled.", "The decomposition mapping field is empty."))]))
    T.append(dict(id="U.upper", n=30, elig=lambda r: True, variants=[
        V("Does this record have a simple uppercase mapping?", lambda r: bool(r["upper"]), None)]))
    T.append(dict(id="U.lower", n=30, elig=lambda r: True, variants=[
        V("Does this record have a simple lowercase mapping?", lambda r: bool(r["lower"]), None)]))
    T.append(dict(id="U.ccc", n=30, elig=lambda r: True, variants=[
        V("Is the canonical combining class above 0?", lambda r: r["ccc"] > 0,
          ("Does this character combine with a base character?", "The canonical combining class is above 0.", "The canonical combining class is 0."))]))
    for b in ("L", "R", "AL", "EN", "ON"):
        T.append(dict(id=f"U.bidi{b}", n=24, elig=lambda r: True, variants=[
            V(f"Is the bidirectional class of this character {b}?", lambda r, b=b: r["bidi"] == b, None)]))
    for w in ("LATIN", "GREEK", "CYRILLIC", "ARABIC", "CJK", "CAPITAL", "SMALL", "SIGN", "LETTER"):
        T.append(dict(id=f"U.word{w}", n=24, elig=lambda r: True, variants=[
            V(f"Does the character name contain the word {w}?", has_word("name", w), None)]))
    T.append(dict(id="U.namelen", n=30, elig=lambda r: True, variants=[
        V("Is the character name longer than 24 characters?", lambda r: len(r["name"]) > 24, None),
        V("Is the character name 24 characters or shorter?", lambda r: len(r["name"]) <= 24, None)]))
    T.append(dict(id="U.digitcp", n=26, elig=lambda r: r["cp"] <= 0xFFFF, variants=[
        V("Is this a decimal digit (general category Nd) with a code point at or below U+FFFF?", lambda r: r["gc"] == "Nd", None)]))
    return T


def unicode_pair_tasks() -> list:
    a = lambda r: True
    E, F = "The {} field is empty.", "The {} field is filled."
    bmp = lambda r: r["cp"] <= 0xFFFF
    L = lambda r: r["gc"][0] == "L"
    nonL = "The general category begins with M, N, P, S or Z."
    return [
        pb("U.pb.list_num", 12, a, "Does this record list a numeric value?", lambda r: bool(r["num"]), F.format("numeric value"), E.format("numeric value")),
        pb("U.pb.show_dec", 12, a, "Does this record show a decomposition mapping?", lambda r: bool(r["decomp"]), F.format("decomposition mapping"), E.format("decomposition mapping")),
        pb("U.pb.give_low", 12, a, "Does this record give a lowercase mapping?", lambda r: bool(r["lower"]), F.format("simple lowercase mapping"), E.format("simple lowercase mapping")),
        pb("U.pb.state_up", 12, a, "Does this record state an uppercase mapping?", lambda r: bool(r["upper"]), F.format("simple uppercase mapping"), E.format("simple uppercase mapping")),
        pb("U.pb.name_latin", 12, a, "Does the name include the word LATIN?", has_word("name", "LATIN"), "The name contains the word LATIN.", "The word LATIN is absent from the name."),
        pb("U.pb.name_sign", 12, a, "Does the name contain the word SIGN?", has_word("name", "SIGN"), "The name contains the word SIGN.", "The word SIGN is absent from the name."),
        pb("U.pb.use_mirror", 12, a, "Does this character use a mirrored glyph in right-to-left text?", lambda r: r["mirror"] == "Y", "The mirrored field is Y.", "The mirrored field is N."),
        pb("U.pb.is_listed_num", 12, a, "Is a numeric value listed for this character?", lambda r: bool(r["num"]), F.format("numeric value"), E.format("numeric value")),
        pb("U.pb.is_given_dec", 12, a, "Is a decomposition given for this character?", lambda r: bool(r["decomp"]), F.format("decomposition mapping"), E.format("decomposition mapping")),
        pb("U.pb.is_loc_bmp", 12, a, "Is this code point located in the Basic Multilingual Plane?", bmp, "The code point is U+FFFF or lower.", "The code point is above U+FFFF."),
        pb("U.pb.is_listed_let", 12, a, "Is this character listed as a letter?", L, "The general category begins with L.", nonL),
        pb("U.pb.is_given_ccc", 12, a, "Is a nonzero combining class given for this character?", lambda r: r["ccc"] > 0, "The canonical combining class is above 0.", "The canonical combining class is 0."),
        pb("U.pb.is_shown_low", 12, a, "Is a lowercase mapping shown for this character?", lambda r: bool(r["lower"]), F.format("simple lowercase mapping"), E.format("simple lowercase mapping")),
        pb("U.pb.has_been_num", 12, a, "Has this character been given a numeric value?", lambda r: bool(r["num"]), F.format("numeric value"), E.format("numeric value")),
        pb("U.pb.has_been_dec", 12, a, "Has this character been assigned a decomposition?", lambda r: bool(r["decomp"]), F.format("decomposition mapping"), E.format("decomposition mapping")),
        pb("U.pb.has_been_up", 12, a, "Has this character been given an uppercase mapping?", lambda r: bool(r["upper"]), F.format("simple uppercase mapping"), E.format("simple uppercase mapping")),
        pb("U.pb.can_low", 12, a, "Can this character map to a lowercase form?", lambda r: bool(r["lower"]), F.format("simple lowercase mapping"), E.format("simple lowercase mapping")),
        pb("U.pb.could_num", 12, a, "Could this character carry a numeric value?", lambda r: bool(r["num"]), F.format("numeric value"), E.format("numeric value")),
        pb("U.pb.will_bmp", 12, a, "Will this character appear in the Basic Multilingual Plane?", bmp, "The code point is U+FFFF or lower.", "The code point is above U+FFFF."),
        pb("U.pb.can_mirror", 12, a, "Can this character be mirrored in right-to-left text?", lambda r: r["mirror"] == "Y", "The mirrored field is Y.", "The mirrored field is N."),
        pb("U.pb.can_combine", 12, a, "Can this character combine with a preceding letter?", lambda r: r["gc"][0] == "M", "The general category begins with M.", "The general category begins with L, N, P, S or Z."),
    ]


# ------------------------------------------------------------------------------------------------------------ iana ports
def load_iana() -> list:
    recs, seen = [], set()
    with open(HERE / "raw/iana/service-names-port-numbers.csv", encoding="utf-8", newline="") as f:
        for i, r in enumerate(csv.DictReader(f)):
            pn = r["Port Number"].strip()
            if not pn.isdigit() or r["Transport Protocol"] not in ("tcp", "udp", "sctp", "dccp"):
                continue
            ref = r["Reference"].strip()
            key = f"{pn}|{r['Transport Protocol']}|{r['Service Name']}|{i}"
            m = re.fullmatch(r"(\d{4})-(\d\d)-(\d\d)", r["Registration Date"].strip())
            m2 = re.fullmatch(r"(\d{4})-(\d\d)-(\d\d)", r["Modification Date"].strip())
            recs.append({"key": key, "doc": f"iana:{pn}", "port": int(pn), "proto": r["Transport Protocol"], "svc": r["Service Name"].strip(),
                         "desc": r["Description"].strip(), "reg": r["Registration Date"].strip() if m else "", "regy": int(m.group(1)) if m else None,
                         "mod": r["Modification Date"].strip() if m2 else "", "mody": int(m2.group(1)) if m2 else None,
                         "ref": ref, "rfc": "RFC" in ref.upper(), "notes": bool(r["Assignment Notes"].strip())})
    return recs


def iana_state(r: dict) -> str:
    return (f"IANA service name and port number registry entry.\nService name: {r['svc'] or 'empty'}\nPort number: {r['port']}\n"
            f"Transport protocol: {r['proto']}\nDescription: {r['desc'] or 'empty'}\nRegistration date: {r['reg'] or 'empty'}\n"
            f"Modification date: {r['mod'] or 'empty'}\nReference: {r['ref'] or 'empty'}")


def iana_tasks() -> list:
    T = []
    for t in (1023, 5000, 10000, 30000, 49151):
        T.append(dict(id=f"I.port{t}", n=34, elig=lambda r: True, variants=[
            V(f"Is the port number above {t}?", lambda r, t=t: r["port"] > t,
              ("Is this a high port number?", f"The port number is above {t}.", f"The port number is {t} or lower.")),
            V(f"Is the port number {t} or lower?", lambda r, t=t: r["port"] <= t,
              ("Is this a low port number?", f"The port number is {t} or lower.", f"The port number is above {t}."))]))
    T.append(dict(id="I.tcp", n=40, elig=lambda r: r["proto"] in ("tcp", "udp"), variants=[
        V("Is the transport protocol of this entry tcp?", lambda r: r["proto"] == "tcp",
          ("Is this entry a connection-oriented entry?", "The transport protocol field is tcp.", "The transport protocol field is udp.")),
        V("Is the transport protocol of this entry udp?", lambda r: r["proto"] == "udp",
          ("Is this entry a datagram entry?", "The transport protocol field is udp.", "The transport protocol field is tcp."))]))
    T.append(dict(id="I.svc", n=40, elig=lambda r: True, variants=[
        V("Does this entry have a service name?", lambda r: bool(r["svc"]),
          ("Does this entry name a service?", "The service name field is filled.", "The service name field is empty."))]))
    T.append(dict(id="I.desc", n=24, elig=lambda r: True, variants=[V("Does this entry have a description?", lambda r: bool(r["desc"]), None)]))
    T.append(dict(id="I.reserved", n=30, elig=lambda r: True, variants=[V("Is the description of this entry Reserved?", lambda r: r["desc"].lower() == "reserved", None),
                                                                           V("Is the description of this entry Unassigned?", lambda r: r["desc"].lower() == "unassigned", None)]))
    T.append(dict(id="I.reg", n=34, elig=lambda r: True, variants=[
        V("Does this entry have a registration date?", lambda r: bool(r["reg"]),
          ("Is this entry a dated registration?", "The registration date field is filled.", "The registration date field is empty."))]))
    for y in (2000, 2005, 2010, 2015):
        T.append(dict(id=f"I.regy{y}", n=26, elig=lambda r: r["regy"] is not None, variants=[
            V(f"Was this entry registered after {y}?", lambda r, y=y: r["regy"] > y,
              ("Is this entry a recent registration?", f"The registration date is after {y}.", f"The registration date is {y} or earlier.")),
            V(f"Was this entry registered in {y} or earlier?", lambda r, y=y: r["regy"] <= y,
              ("Is this entry an older registration?", f"The registration date is {y} or earlier.", f"The registration date is after {y}."))]))
    for y in (2015, 2020, 2023):
        T.append(dict(id=f"I.mody{y}", n=24, elig=lambda r: r["mody"] is not None, variants=[
            V(f"Was this entry last modified after {y}?", lambda r, y=y: r["mody"] > y, None),
            V(f"Was this entry last modified in {y} or earlier?", lambda r, y=y: r["mody"] <= y, None)]))
    T.append(dict(id="I.rfc", n=30, elig=lambda r: True, variants=[
        V("Does the reference of this entry cite an RFC?", lambda r: r["rfc"],
          ("Is this entry backed by an RFC?", "The reference field cites an RFC.", "The reference field is empty or cites a document other than an RFC."))]))
    T.append(dict(id="I.svclen", n=28, elig=lambda r: bool(r["svc"]), variants=[
        V("Is the service name longer than 8 characters?", lambda r: len(r["svc"]) > 8, None),
        V("Is the service name 8 characters or shorter?", lambda r: len(r["svc"]) <= 8, None)]))
    T.append(dict(id="I.hyphen", n=26, elig=lambda r: bool(r["svc"]), variants=[V("Does the service name contain a hyphen?", lambda r: "-" in r["svc"], None)]))
    for w in ("server", "protocol", "service", "data"):
        T.append(dict(id=f"I.word{w}", n=22, elig=lambda r: bool(r["desc"]), variants=[
            V(f"Does the description contain the word {w}?", lambda r, w=w: re.search(r"\b" + w + r"\b", r["desc"].lower()) is not None, None)]))
    T.append(dict(id="I.sctp", n=14, elig=lambda r: True, variants=[V("Is the transport protocol of this entry sctp or dccp?", lambda r: r["proto"] in ("sctp", "dccp"), None)]))
    return T


def iana_pair_tasks() -> list:
    a = lambda r: True
    F, E = "The {} field is filled.", "The {} field is empty."
    return [
        pb("I.pb.list_svc", 12, a, "Does this entry list a service name?", lambda r: bool(r["svc"]), F.format("service name"), E.format("service name")),
        pb("I.pb.give_desc", 12, a, "Does this entry give a description?", lambda r: bool(r["desc"]), F.format("description"), E.format("description")),
        pb("I.pb.state_reg", 12, a, "Does this entry state a registration date?", lambda r: bool(r["reg"]), F.format("registration date"), E.format("registration date")),
        pb("I.pb.cite_rfc", 12, a, "Does this entry cite an RFC reference?", lambda r: r["rfc"], "The reference field cites an RFC.", "The reference field is empty or cites a document other than an RFC."),
        pb("I.pb.show_mod", 12, a, "Does this entry show a modification date?", lambda r: bool(r["mod"]), F.format("modification date"), E.format("modification date")),
        pb("I.pb.is_listed_reg", 12, a, "Is a registration date listed for this entry?", lambda r: bool(r["reg"]), F.format("registration date"), E.format("registration date")),
        pb("I.pb.is_given_svc", 12, a, "Is a service name given for this port?", lambda r: bool(r["svc"]), F.format("service name"), E.format("service name")),
        pb("I.pb.is_shown_ref", 12, a, "Is a reference shown for this entry?", lambda r: bool(r["ref"]), F.format("reference"), E.format("reference")),
        pb("I.pb.is_loc_sys", 12, a, "Is this port number located in the system range?", lambda r: r["port"] <= 1023, "The port number is 1023 or lower.", "The port number is above 1023."),
        pb("I.pb.is_listed_tcp", 12, lambda r: r["proto"] in ("tcp", "udp"), "Is this entry listed under the tcp protocol?", lambda r: r["proto"] == "tcp", "The transport protocol field is tcp.", "The transport protocol field is udp."),
        pb("I.pb.has_been_mod", 12, lambda r: r["mody"] is not None, "Has this entry been modified after 2020?", lambda r: r["mody"] > 2020, "The modification date is after 2020.", "The modification date is 2020 or earlier."),
        pb("I.pb.has_been_reg", 12, lambda r: r["regy"] is not None, "Has this entry been registered after 2010?", lambda r: r["regy"] > 2010, "The registration date is after 2010.", "The registration date is 2010 or earlier."),
        pb("I.pb.has_been_given", 12, a, "Has this entry been given a service name?", lambda r: bool(r["svc"]), F.format("service name"), E.format("service name")),
        pb("I.pb.can_unpriv", 12, a, "Can this port number be used by an unprivileged process?", lambda r: r["port"] > 1023, "The port number is above 1023.", "The port number is 1023 or lower."),
        pb("I.pb.will_dyn", 12, a, "Will this port number fall in the dynamic range?", lambda r: r["port"] >= 49152, "The port number is 49152 or higher.", "The port number is below 49152."),
        pb("I.pb.could_id", 12, a, "Could this entry identify a service?", lambda r: bool(r["svc"]), F.format("service name"), E.format("service name")),
        pb("I.pb.can_cite", 12, a, "Can this entry point to an RFC?", lambda r: r["rfc"], "The reference field cites an RFC.", "The reference field is empty or cites a document other than an RFC."),
    ]


# ------------------------------------------------------------------------------------------------------------ hgnc
def load_hgnc() -> list:
    recs = []
    with open(HERE / "raw/hgnc/hgnc_complete_set.txt", encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if r["status"] != "Approved" or not r["location"].strip():
                continue
            m = re.fullmatch(r"(\d{4})-(\d\d)-(\d\d)", r["date_approved_reserved"].strip())
            if not m:
                continue
            loc = r["location"].strip()
            cm = re.match(r"(\d{1,2}|X|Y)([pq])", loc)
            recs.append({"key": r["hgnc_id"], "doc": "hgnc:" + r["hgnc_id"], "id": r["hgnc_id"], "sym": r["symbol"], "name": r["name"], "lg": r["locus_group"],
                         "lt": r["locus_type"], "loc": loc, "chrom": cm.group(1) if cm else None, "arm": cm.group(2) if cm else None,
                         "appr": r["date_approved_reserved"].strip(), "apy": int(m.group(1)),
                         "alias": r["alias_symbol"].replace("|", ", "), "prev": r["prev_symbol"].replace("|", ", "),
                         "grp": r["gene_group"].replace("|", ", "), "ens": r["ensembl_gene_id"], "entrez": r["entrez_id"], "omim": r["omim_id"].replace("|", ", "),
                         "uni": r["uniprot_ids"].replace("|", ", ")})
    return recs


def hgnc_state(r: dict) -> str:
    z = lambda x: x or "empty"
    return (f"HGNC gene record (HGNC complete set).\nHGNC ID: {r['id']}\nSymbol: {r['sym']}\nName: {r['name']}\nLocus group: {r['lg']}\n"
            f"Locus type: {r['lt']}\nChromosomal location: {r['loc']}\nDate approved: {r['appr']}\nAlias symbols: {z(r['alias'])}\n"
            f"Previous symbols: {z(r['prev'])}\nGene group: {z(r['grp'])}\nEnsembl gene ID: {z(r['ens'])}\nEntrez ID: {z(r['entrez'])}\n"
            f"OMIM ID: {z(r['omim'])}\nUniProt IDs: {z(r['uni'])}")


def hgnc_tasks() -> list:
    T = []
    T.append(dict(id="H.protein", n=44, elig=lambda r: True, variants=[
        V("Is the locus group of this gene protein-coding gene?", lambda r: r["lg"] == "protein-coding gene",
          ("Is this gene a protein-coding gene?", "The locus group is protein-coding gene.", "The locus group is pseudogene, non-coding RNA or other.")),
        V("Is the locus group of this gene pseudogene, non-coding RNA or other?", lambda r: r["lg"] != "protein-coding gene",
          ("Is this gene a gene of another kind?", "The locus group is pseudogene, non-coding RNA or other.", "The locus group is protein-coding gene."))]))
    for lg in ("pseudogene", "non-coding RNA"):
        T.append(dict(id="H.lg." + lg.replace(" ", "_"), n=26, elig=lambda r: True, variants=[V(f"Is the locus group of this gene {lg}?", lambda r, lg=lg: r["lg"] == lg, None)]))
    for lt in ("gene with protein product", "RNA, long non-coding", "RNA, micro", "RNA, transfer", "pseudogene"):
        T.append(dict(id="H.lt." + re.sub(r"\W+", "_", lt), n=22, elig=lambda r: True, variants=[V(f"Is the locus type of this gene {lt}?", lambda r, lt=lt: r["lt"] == lt, None)]))
    for c in ("1", "7", "11", "17", "X"):
        T.append(dict(id=f"H.chr{c}", n=24, elig=lambda r: r["chrom"] is not None, variants=[
            V(f"Is this gene located on chromosome {c}?", lambda r, c=c: r["chrom"] == c, None)]))
    T.append(dict(id="H.arm", n=34, elig=lambda r: r["arm"] is not None, variants=[
        V("Is this gene located on the short arm (p) of its chromosome?", lambda r: r["arm"] == "p",
          ("Is this gene on a short chromosome arm?", "The chromosomal location has the arm letter p.", "The chromosomal location has the arm letter q.")),
        V("Is this gene located on the long arm (q) of its chromosome?", lambda r: r["arm"] == "q",
          ("Is this gene on a long chromosome arm?", "The chromosomal location has the arm letter q.", "The chromosomal location has the arm letter p."))]))
    for y in (1995, 2005, 2010, 2015, 2020):
        T.append(dict(id=f"H.apy{y}", n=26, elig=lambda r: True, variants=[
            V(f"Was this gene approved after {y}?", lambda r, y=y: r["apy"] > y,
              ("Is this gene a recent approval?", f"The date approved is after {y}.", f"The date approved is {y} or earlier.")),
            V(f"Was this gene approved in {y} or earlier?", lambda r, y=y: r["apy"] <= y,
              ("Is this gene an older approval?", f"The date approved is {y} or earlier.", f"The date approved is after {y}."))]))
    for fld, lab in (("alias", "alias symbols"), ("prev", "previous symbols"), ("grp", "gene group"), ("ens", "Ensembl gene ID"), ("omim", "OMIM ID"), ("uni", "UniProt IDs"), ("entrez", "Entrez ID")):
        T.append(dict(id=f"H.has_{fld}", n=28, elig=lambda r: True, variants=[
            V(f"Does this record have a value for {lab}?", lambda r, f=fld: bool(r[f]),
              (f"Does this gene have {lab} on file?", f"The {lab} field is filled.", f"The {lab} field is empty."))]))
    for w in ("protein", "kinase", "receptor", "family", "like"):
        T.append(dict(id=f"H.word{w}", n=22, elig=lambda r: True, variants=[
            V(f"Does the gene name contain the word {w}?", lambda r, w=w: re.search(r"\b" + w + r"\b", r["name"].lower()) is not None, None)]))
    T.append(dict(id="H.symlen", n=30, elig=lambda r: True, variants=[
        V("Is the gene symbol longer than 5 characters?", lambda r: len(r["sym"]) > 5, None),
        V("Is the gene symbol 5 characters or shorter?", lambda r: len(r["sym"]) <= 5, None)]))
    T.append(dict(id="H.linc", n=26, elig=lambda r: True, variants=[V("Does the gene symbol start with LINC?", lambda r: r["sym"].startswith("LINC"), None)]))
    return T


def hgnc_pair_tasks() -> list:
    a = lambda r: True
    F, E = "The {} field is filled.", "The {} field is empty."
    g = lambda f, lab: (lambda r: bool(r[f]))
    return [
        pb("H.pb.list_alias", 12, a, "Does this record list an alias symbol?", g("alias", ""), F.format("alias symbols"), E.format("alias symbols")),
        pb("H.pb.give_ens", 12, a, "Does this record give an Ensembl identifier?", g("ens", ""), F.format("Ensembl gene ID"), E.format("Ensembl gene ID")),
        pb("H.pb.cite_omim", 12, a, "Does this record cite an OMIM identifier?", g("omim", ""), F.format("OMIM ID"), E.format("OMIM ID")),
        pb("H.pb.show_uni", 12, a, "Does this record show a UniProt identifier?", g("uni", ""), F.format("UniProt IDs"), E.format("UniProt IDs")),
        pb("H.pb.name_kinase", 12, a, "Does the gene name mention the word kinase?", lambda r: re.search(r"\bkinase\b", r["name"].lower()) is not None, "The name contains the word kinase.", "The word kinase is absent from the name."),
        pb("H.pb.sym_linc", 12, a, "Does the symbol start with the letters LINC?", lambda r: r["sym"].startswith("LINC"), "The symbol starts with LINC.", "The symbol starts with other letters."),
        pb("H.pb.is_listed_prev", 12, a, "Is a previous symbol listed for this gene?", g("prev", ""), F.format("previous symbols"), E.format("previous symbols")),
        pb("H.pb.is_given_grp", 12, a, "Is a gene group given for this gene?", g("grp", ""), F.format("gene group"), E.format("gene group")),
        pb("H.pb.is_shown_entrez", 12, a, "Is an Entrez identifier shown for this gene?", g("entrez", ""), F.format("Entrez ID"), E.format("Entrez ID")),
        pb("H.pb.is_loc_chr", 12, lambda r: r["chrom"] is not None, "Is this gene located on chromosome 1?", lambda r: r["chrom"] == "1", "The chromosomal location starts with 1p or 1q.", "The chromosomal location starts with another chromosome."),
        pb("H.pb.is_listed_pc", 12, a, "Is this gene listed as a protein-coding gene?", lambda r: r["lg"] == "protein-coding gene", "The locus group is protein-coding gene.", "The locus group is pseudogene, non-coding RNA or other."),
        pb("H.pb.has_been_appr", 12, a, "Has this gene been approved after 2005?", lambda r: r["apy"] > 2005, "The date approved is after 2005.", "The date approved is 2005 or earlier."),
        pb("H.pb.has_been_grp", 12, a, "Has this gene been given a gene group?", g("grp", ""), F.format("gene group"), E.format("gene group")),
        pb("H.pb.has_been_alias", 12, a, "Has this gene been assigned an alias symbol?", g("alias", ""), F.format("alias symbols"), E.format("alias symbols")),
        pb("H.pb.can_encode", 12, a, "Can this gene encode a protein?", lambda r: r["lg"] == "protein-coding gene", "The locus group is protein-coding gene.", "The locus group is pseudogene, non-coding RNA or other."),
        pb("H.pb.could_produce", 12, a, "Could this gene produce a protein?", lambda r: r["lt"] == "gene with protein product", "The locus type is gene with protein product.", "The locus type is another type."),
        pb("H.pb.will_link", 12, a, "Will this record link to an OMIM entry?", g("omim", ""), F.format("OMIM ID"), E.format("OMIM ID")),
        pb("H.pb.can_match", 12, a, "Can this gene match a UniProt entry?", g("uni", ""), F.format("UniProt IDs"), E.format("UniProt IDs")),
    ]


# ------------------------------------------------------------------------------------------------------------ lexical-pair bases
def lex_pair_tasks(src: str) -> list:
    """Card-only bases whose core carries one of the four realised held-out lexical pairs (possess/lack, lodged/unlodged,
    ratified/unratified, redeemed/unredeemed). The card defines the meaning, so every base and twin stays determinate."""
    F, E = "The {} field is filled.", "The {} field is empty."
    if src == "A":
        return [
            pb("A.lx.possess", 12, lambda r: True, "Does this airport possess an IATA code?", lambda r: bool(r["iata"]), F.format("IATA code"), E.format("IATA code")),
            pb("A.lx.lodged", 12, lambda r: True, "Is an IATA code lodged for this airport?", lambda r: bool(r["iata"]), F.format("IATA code"), E.format("IATA code")),
            pb("A.lx.ratified", 12, lambda r: True, "Is scheduled service ratified for this airport?", lambda r: r["sched"] == "yes", "The record lists scheduled service as yes.", "The record lists scheduled service as no."),
            pb("A.lx.redeemed", 12, lambda r: True, "Is a field elevation redeemed for this airport?", lambda r: r["elev"] is not None, "The field elevation is given.", "The field elevation is unknown.")]
    if src == "U":
        return [
            pb("U.lx.possess", 12, lambda r: True, "Does this character possess a lowercase mapping?", lambda r: bool(r["lower"]), F.format("simple lowercase mapping"), E.format("simple lowercase mapping")),
            pb("U.lx.lodged", 12, lambda r: True, "Is a decomposition lodged for this character?", lambda r: bool(r["decomp"]), F.format("decomposition mapping"), E.format("decomposition mapping")),
            pb("U.lx.ratified", 12, lambda r: True, "Is this character ratified as a letter?", lambda r: r["gc"][0] == "L", "The general category begins with L.", "The general category begins with M, N, P, S or Z."),
            pb("U.lx.redeemed", 12, lambda r: True, "Is a numeric value redeemed for this character?", lambda r: bool(r["num"]), F.format("numeric value"), E.format("numeric value"))]
    if src == "I":
        return [
            pb("I.lx.possess", 12, lambda r: True, "Does this entry possess a service name?", lambda r: bool(r["svc"]), F.format("service name"), E.format("service name")),
            pb("I.lx.lodged", 12, lambda r: True, "Is a registration date lodged for this entry?", lambda r: bool(r["reg"]), F.format("registration date"), E.format("registration date")),
            pb("I.lx.ratified", 12, lambda r: True, "Is this entry ratified by an RFC?", lambda r: r["rfc"], "The reference field cites an RFC.", "The reference field is empty or cites a document other than an RFC."),
            pb("I.lx.redeemed", 12, lambda r: True, "Is a reference redeemed for this entry?", lambda r: bool(r["ref"]), F.format("reference"), E.format("reference"))]
    return [
        pb("H.lx.possess", 12, lambda r: True, "Does this gene possess an alias symbol?", lambda r: bool(r["alias"]), F.format("alias symbols"), E.format("alias symbols")),
        pb("H.lx.lodged", 12, lambda r: True, "Is an Ensembl identifier lodged for this gene?", lambda r: bool(r["ens"]), F.format("Ensembl gene ID"), E.format("Ensembl gene ID")),
        pb("H.lx.ratified", 12, lambda r: True, "Is this gene ratified after 2005?", lambda r: r["apy"] > 2005, "The date approved is after 2005.", "The date approved is 2005 or earlier."),
        pb("H.lx.redeemed", 12, lambda r: True, "Is a gene group redeemed for this gene?", lambda r: bool(r["grp"]), F.format("gene group"), E.format("gene group"))]


# ------------------------------------------------------------------------------------------------------------ main
def main():
    dropped, stats = [], Counter()
    rows = []
    rows += B.build_source("gp_ourairports", B.airport_tasks() + B.airport_pair_tasks() + lex_pair_tasks("A"), B.load_airports(), lambda it: B.airport_state(it["rec"]), dropped, stats)
    rows += B.build_source("gp_unicode", unicode_tasks() + unicode_pair_tasks() + lex_pair_tasks("U"), load_unicode(), lambda it: unicode_state(it["rec"]), dropped, stats)
    rows += B.build_source("gp_hgnc", hgnc_tasks() + hgnc_pair_tasks() + lex_pair_tasks("H"), load_hgnc(), lambda it: hgnc_state(it["rec"]), dropped, stats)
    rows.sort(key=lambda r: B.H("order", r["id"]))
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids)), "duplicate ids"
    B.OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(B.OUT, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    per, clusters = defaultdict(Counter), defaultdict(set)
    for r in rows:
        c = per[r["source"]]
        c["rows"] += 1
        c["yes"] += r["gold"]
        c["card_free"] += r["card"] is None
        clusters[r["source"]].add(r["meta"]["source_doc"])
    pol_bad, neg_words = [], re.compile(r"\b(not|no|never|n't|without|neither|nor)\b|n't", re.I)
    for r in rows:
        probs = polarity.problems(r["instructions"], +1)
        rd = polarity.read(r["instructions"])
        if probs or rd.k_syn or rd.lexical or rd.frame not in ("plain", "explicit") or neg_words.search(r["instructions"]):
            pol_bad.append({"id": r["id"], "text": r["instructions"], "problems": probs, "frame": rd.frame})
    n = len(rows)
    rep = {"seed": B.SEED, "snapshot": B.SNAPSHOT, "rows": n, "yes_share": round(sum(r["gold"] for r in rows) / n, 4),
           "card_free_share": round(sum(r["card"] is None for r in rows) / n, 4),
           "per_source": {s: {"rows": c["rows"], "share_of_rows": round(c["rows"] / n, 4), "yes_share": round(c["yes"] / c["rows"], 4),
                              "card_free_share": round(c["card_free"] / c["rows"], 4), "clusters": len(clusters[s])} for s, c in sorted(per.items())},
           "tasks": len({r["meta"]["task"] for r in rows}), "stats": dict(stats), "variants_dropped_by_polarity": dropped,
           "polarity_or_negation_failures": pol_bad[:20], "n_polarity_or_negation_failures": len(pol_bad),
           "note": "no final hash recorded: the Haiku noise check (A42-D 12.3) comes first"}
    B.REPORT.write_text(json.dumps(rep, indent=1) + "\n")
    print(json.dumps({k: rep[k] for k in ("rows", "yes_share", "card_free_share", "per_source", "tasks", "stats", "n_polarity_or_negation_failures")}, indent=1))
    if dropped:
        print("DROPPED", json.dumps(dropped)[:1500])
    if pol_bad:
        print("POL", json.dumps(pol_bad[:8])[:1500])


if __name__ == "__main__":
    main()
