"""T63 renderers and parse-backs (render round trip). Contexts are plain text assembled from fixed definition cards (defs_card.t63.*),
the seeded snapshot / listing / card, and a query line. The question wording and the lettered options are added by rows.py.

Parse-backs (`parse_*`) rebuild the decisive part of the spec from the RENDERED text with their own code; the round trip must equal the
spec and SOLVER A on the parsed spec must equal the stored gold. This is the generator's render-fidelity check, NOT solver B (a separate
session writes B from ROW_SCHEMA.md).
"""
import csv
import io
import json
import re

from . import config as C

AGE_TEXT = {"A0": "under 30 days", "A1": "under 1 year", "A2": "1-4 years", "A3": "over 4 years"}
DL_TEXT = {"D0": "low", "D1": "mid", "D2": "high"}
TEXT_AGE = {v: k for k, v in AGE_TEXT.items()}
TEXT_DL = {v: k for k, v in DL_TEXT.items()}
VERB = {"pip": "install", "npm": "install", "cargo": "add", "go": "get"}

NEAR_DEFS = (
    "Definitions. A package is established when its age is 1-4 years or over 4 years and its downloads are high. A package is newer than "
    "another when its age is a younger class; the same class is not newer.\n"
    "The proposed package is a LOOKALIKE when the same registry lists an established package whose name differs from it by exactly one of: "
    "one letter dropped, one letter added, one letter replaced by a neighbouring keyboard letter, two adjacent letters swapped, a changed "
    "separator (- _ . or none), a look-alike character swap (rn and m, l and 1, o and 0), or a scope prefix added or removed; and the "
    "publishers differ; and neither package is a fork of the other; and the proposed package is newer.\n"
    "A CONFUSION is a name the card reserves for the internal registry that is proposed from another registry when a bare install resolves "
    "to that registry (the first registry in the resolve order that lists the name) or the install names it, and the publisher is not the "
    "project org.\n"
    "Answer YES for a lookalike or a confusion, otherwise NO.")

EXISTS_DEFS = (
    "Definitions. A name exists in a module when attribute access on the module works, including names the module re-exports; only public "
    "names (no leading underscore) count. A list marked complete for a range names every entry in that range; a name inside the range that "
    "is not listed does not exist. Answer YES if the name exists, otherwise NO.")

LIC_DEFS = (
    "Definitions. This is a policy table for a coding agent, not legal advice. COMPATIBLE: the dependency may be used under these terms "
    "without further review. REVIEW: a human licence review is needed first. INCOMPATIBLE: the dependency may not be used under these terms.")


# ---- NEAR ---------------------------------------------------------------------------------------------------------------------------
def _entry_row(e):
    return [e["name"], e["registry"], e["publisher"], AGE_TEXT[e["age"]], DL_TEXT[e["dl"]], e.get("fork_of") or "-"]


COLS = ["name", "registry", "publisher", "age", "downloads", "fork_of"]


def render_table(entries, fmt):
    rows = [_entry_row(e) for e in entries]
    if fmt == "TBL-CSV":
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator="\n")
        w.writerow(COLS)
        w.writerows(rows)
        return buf.getvalue().rstrip("\n")
    if fmt == "TBL-TSV":
        return "\n".join("\t".join(r) for r in [COLS] + rows)
    if fmt == "TBL-PIPE":
        return "\n".join(" | ".join(r) for r in [COLS] + rows)
    if fmt == "TBL-JSON":
        return json.dumps([dict(zip(COLS, r)) for r in rows], indent=1)
    if fmt == "TBL-KV":
        return "\n\n".join("\n".join("%s: %s" % (c, v) for c, v in zip(COLS, r)) for r in rows)
    raise ValueError(fmt)


def parse_table(text, fmt):
    if fmt == "TBL-CSV":
        rows = list(csv.reader(io.StringIO(text)))
    elif fmt == "TBL-TSV":
        rows = [ln.split("\t") for ln in text.split("\n")]
    elif fmt == "TBL-PIPE":
        rows = [ln.split(" | ") for ln in text.split("\n")]
    elif fmt == "TBL-JSON":
        d = json.loads(text)
        rows = [COLS] + [[r[c] for c in COLS] for r in d]
    elif fmt == "TBL-KV":
        rows = [COLS]
        for blk in text.split("\n\n"):
            kv = dict(ln.split(": ", 1) for ln in blk.split("\n"))
            rows.append([kv[c] for c in COLS])
    else:
        raise ValueError(fmt)
    if rows[0] != COLS:
        raise ValueError("header")
    out = []
    for r in rows[1:]:
        out.append({"name": r[0], "registry": r[1], "publisher": r[2], "age": TEXT_AGE[r[3]], "dl": TEXT_DL[r[4]],
                    "fork_of": None if r[5] == "-" else r[5]})
    return out


def fmt_word(fmt):
    return fmt.split("-", 1)[1].lower()


def render_near_context(spec, fmt):
    regs = spec["registries"]
    legend = "Registries: " + "; ".join("%s = %s (%s)" % (r["id"], r["host"], r["eco"]) for r in regs)
    card = spec["card"]
    card_txt = "\n".join([
        "Project card %s" % card["display"],
        "reserved internal names: %s" % (", ".join(card["reserved"]) if card["reserved"] else "none"),
        "internal registry: %s" % (card["internal_registry"] or "none"),
        "a bare install resolves in this order: %s" % ", ".join(card["resolve_order"]),
        "project org: %s" % card["own_org"]])
    q = spec["query"]
    eco = next(r for r in regs if r["id"] == q["registry"])["eco"]
    host = next(r for r in regs if r["id"] == q["registry"])["host"]
    cmd = "%s %s %s" % (eco, VERB[eco], q["name"]) + (" --registry %s" % host if q["explicit"] else "")
    query_txt = "Proposed command: %s\nRegistry: %s" % (cmd, q["registry"])
    return "\n\n".join([NEAR_DEFS, legend, card_txt, "Snapshot (%s):\n%s" % (fmt_word(fmt), render_table(spec["entries"], fmt)), query_txt])


_CARD = re.compile(r"Project card (.+)\nreserved internal names: (.*)\ninternal registry: (.*)\na bare install resolves in this order: (.*)\nproject org: (.*)")


def parse_near_context(text, fmt):
    legend = re.search(r"^Registries: (.*)$", text, re.M).group(1)
    regs = []
    for part in legend.split("; "):
        m = re.match(r"(R\d) = (\S+) \((\w+)\)$", part)
        regs.append({"id": m.group(1), "host": m.group(2), "eco": m.group(3)})
    m = _CARD.search(text)
    card = {"display": m.group(1), "reserved": [] if m.group(2) == "none" else m.group(2).split(", "),
            "internal_registry": None if m.group(3) == "none" else m.group(3), "resolve_order": m.group(4).split(", "), "own_org": m.group(5)}
    tm = re.search(r"Snapshot \(%s\):\n(.*)\n\nProposed command: " % re.escape(fmt_word(fmt)), text, re.S)
    entries = parse_table(tm.group(1), fmt)
    qm = re.search(r"Proposed command: (\w+) (\w+) (\S+)( --registry (\S+))?\nRegistry: (R\d)$", text, re.M)
    q = {"name": qm.group(3), "registry": qm.group(6), "explicit": bool(qm.group(4))}
    host = next(r for r in regs if r["id"] == q["registry"])["host"]
    if q["explicit"] and qm.group(5) != host:
        raise ValueError("explicit registry host differs from the query registry")
    return {"registries": regs, "entries": entries, "card": card, "query": q}


# ---- EXISTS -----------------------------------------------------------------------------------------------------------------------
def _listing_block(reg, listing, rng_):
    head = 'Registry index for %s (%s), complete for package names from "%s" to "%s":' % (reg["id"], reg["host"], rng_[0], rng_[1])
    return head + "\n" + "\n".join("- " + n for n in listing)


def render_exists_context(spec):
    sub = spec["sub"]
    if sub == "EX-A1":
        blocks = [(spec["registry"]["id"], _listing_block(spec["registry"], spec["listing"], spec["range"]))]
        if spec.get("other"):
            o = spec["other"]
            blocks.append((o["registry"]["id"], _listing_block(o["registry"], o["listing"], o["range"])))
        return "\n\n".join([EXISTS_DEFS] + [b for _i, b in sorted(blocks)])      # sorted by registry id: block order carries no label
    if sub == "EX-A2":
        lines = ["Library %s version %s, complete export list:" % (spec["library"], spec["version"])]
        for m in sorted(spec["exports"]):
            lines.append("module %s: %s" % (m, ", ".join(spec["exports"][m])))
        return "\n\n".join([EXISTS_DEFS, "\n".join(lines)])
    if sub in ("EX-B1", "EX-B2"):
        if spec["view"] == "B2":
            return EXISTS_DEFS
        scope = "complete" if spec["range"] is None else 'complete for names from "%s" to "%s"' % tuple(spec["range"])
        head = "Exports of %s module %s in the pinned toolchain image, %s:" % (LANG_WORD[spec["lang"]], spec["module"], scope)
        return "\n\n".join([EXISTS_DEFS, head + "\n" + "\n".join("- " + n for n in spec["shown"])])
    raise ValueError(sub)


LANG_WORD = {"python": "Python 3.12", "node": "Node 24", "go": "Go 1.26"}


def parse_exists_context(text, sub):
    if sub == "EX-A1":
        blocks = re.findall(r'Registry index for (R\d) \((\S+)\), complete for package names from "([^"]*)" to "([^"]*)":\n((?:- .*\n?)+)', text)
        out = []
        for rid, host, lo, hi, body in blocks:
            out.append({"registry": {"id": rid, "host": host}, "range": [lo, hi], "listing": [ln[2:] for ln in body.strip("\n").split("\n")]})
        return out
    if sub == "EX-A2":
        m = re.search(r"Library (\S+) version (\S+), complete export list:\n((?:module .*\n?)+)", text)
        exports = {}
        for ln in m.group(3).strip("\n").split("\n"):
            mm = re.match(r"module (\S+): (.*)$", ln)
            exports[mm.group(1)] = mm.group(2).split(", ")
        return {"library": m.group(1), "version": m.group(2), "exports": exports}
    m = re.search(r"Exports of (.+?) module (\S+) in the pinned toolchain image, (complete|complete for names from \"([^\"]*)\" to \"([^\"]*)\"):\n((?:- .*\n?)+)", text)
    if not m:
        return None
    return {"lang_word": m.group(1), "module": m.group(2), "range": None if m.group(3) == "complete" else [m.group(4), m.group(5)],
            "shown": [ln[2:] for ln in m.group(6).strip("\n").split("\n")]}


# ---- LIC ---------------------------------------------------------------------------------------------------------------------------
def render_lic_context(spec):
    card = "\n".join(["Licence card", "Dependency licence: %s" % spec["dep"], "Project licence: %s" % spec["project"],
                      "Usage: %s" % C.LIC_USE[spec["use"]], "Distribution: %s" % C.LIC_DIST[spec["dist"]]])
    return "\n\n".join([LIC_DEFS, card])


def parse_lic_context(text):
    m = re.search(r"Licence card\nDependency licence: (\S+)\nProject licence: (\S+)\nUsage: (.+)\nDistribution: (.+)$", text)
    use = {v: k for k, v in C.LIC_USE.items()}[m.group(3)]
    dist = {v: k for k, v in C.LIC_DIST.items()}[m.group(4)]
    return {"dep": m.group(1), "project": m.group(2), "use": use, "dist": dist}
