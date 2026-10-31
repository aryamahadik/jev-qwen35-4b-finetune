"""NEAR head of solver B: parse the RENDERED context (definitions block, registry legend, project card, snapshot table in any of the five
formats, proposed command) and apply the definitions-block rule (G0-lite 2.1 + T63-M1 + T63-B7). Stdlib only."""
import csv
import io
import json

from . import rel
from .common import Abstain, norm_ws

AGE_RANK = {"under 30 days": 0, "under 1 year": 1, "1-4 years": 2, "over 4 years": 3}
DL_RANK = {"low": 0, "mid": 1, "high": 2}
ESTABLISHED_MIN_AGE = 2
ESTABLISHED_DL = 2
COLUMNS = ("name", "registry", "publisher", "age", "downloads", "fork_of")

# Clauses the rendered definitions block must still state (checked on the lower-cased, whitespace-normalised text). If one is missing the
# rendered rule is not the rule B implements, so B abstains instead of labelling by a rule the row does not show.
REQUIRED_DEFS = (
    "established when its age is 1-4 years or over 4 years and its downloads are high",
    "newer than another when its age is a younger class; the same class is not newer",
    "a lookalike when the same registry lists an established package whose name differs from it by exactly one of:",
    "one letter dropped, one letter added, one letter replaced by a neighbouring keyboard letter, two adjacent letters swapped, a changed "
    "separator (- _ . or none), a look-alike character swap (rn and m, l and 1, o and 0), or a scope prefix added or removed",
    "and the publishers differ; and neither package is a fork of the other; and the proposed package is newer",
    "a confusion is a name the card reserves for the internal registry that is proposed from another registry when a bare install resolves "
    "to that registry (the first registry in the resolve order that lists the name) or the install names it, and the publisher is not the "
    "project org",
    "answer yes for a lookalike or a confusion, otherwise no",
)


def check_definitions(context):
    cut = context.find("\n\nRegistries:")
    head = context if cut < 0 else context[:cut]
    flat = norm_ws(head).lower()
    for clause in REQUIRED_DEFS:
        if clause not in flat:
            raise Abstain("defs_mismatch")


# ---- parsing --------------------------------------------------------------------------------------------------------------------
def _lines_after(context, prefix):
    for ln in context.split("\n"):
        if ln.startswith(prefix):
            return ln[len(prefix):]
    raise Abstain("missing:" + prefix.strip())


def parse_legend(context):
    raw = _lines_after(context, "Registries: ")
    out = {}
    for part in raw.split("; "):
        left, sep, right = part.partition(" = ")
        if not sep or not right.endswith(")") or " (" not in right:
            raise Abstain("legend")
        host, _s, eco = right[:-1].rpartition(" (")
        out[left.strip()] = {"host": host.strip(), "eco": eco.strip()}
    if not out:
        raise Abstain("legend")
    return out


def _csv_list(s):
    s = s.strip()
    return [] if s.lower() == "none" or s == "" else [x.strip() for x in s.split(",")]


def parse_card(context):
    return {
        "reserved": _csv_list(_lines_after(context, "reserved internal names: ")),
        "internal": (lambda v: None if v.strip().lower() == "none" else v.strip())(_lines_after(context, "internal registry: ")),
        "order": _csv_list(_lines_after(context, "a bare install resolves in this order: ")),
        "org": _lines_after(context, "project org: ").strip(),
    }


def _rows_to_entries(header, rows):
    header = [h.strip() for h in header]
    if sorted(header) != sorted(COLUMNS):
        raise Abstain("table_header")
    pos = {c: header.index(c) for c in COLUMNS}
    out = []
    for r in rows:
        if len(r) != len(header):
            raise Abstain("table_row")
        cells = [str(c).strip() for c in r]
        age, dl = cells[pos["age"]], cells[pos["downloads"]]
        if age not in AGE_RANK or dl not in DL_RANK:
            raise Abstain("table_value")
        fork = cells[pos["fork_of"]]
        out.append({"name": cells[pos["name"]], "registry": cells[pos["registry"]], "publisher": cells[pos["publisher"]],
                    "age": AGE_RANK[age], "dl": DL_RANK[dl], "fork_of": None if fork in ("-", "") else fork})
    if not out:
        raise Abstain("table_empty")
    return out


def parse_snapshot(context):
    start = context.find("Snapshot (")
    if start < 0:
        raise Abstain("no_snapshot")
    close = context.find("):\n", start)
    word = context[start + len("Snapshot ("):close].strip().lower()
    end = context.find("\n\nProposed command:", close)
    if close < 0 or end < 0:
        raise Abstain("snapshot_bounds")
    body = context[close + 3:end]
    try:
        if word == "csv":
            rows = list(csv.reader(io.StringIO(body)))
            return _rows_to_entries(rows[0], rows[1:])
        if word == "tsv":
            rows = [ln.split("\t") for ln in body.split("\n")]
            return _rows_to_entries(rows[0], rows[1:])
        if word == "pipe":
            rows = [[c.strip() for c in ln.split("|")] for ln in body.split("\n")]
            return _rows_to_entries(rows[0], rows[1:])
        if word == "json":
            recs = json.loads(body)
            if not isinstance(recs, list) or not recs or not all(isinstance(x, dict) for x in recs):
                raise Abstain("json_shape")
            header = list(recs[0].keys())
            return _rows_to_entries(header, [[x.get(h, "") for h in header] if set(x.keys()) == set(header) else [] for x in recs])
        if word == "kv":
            blocks = [b for b in body.split("\n\n") if b.strip()]
            recs = []
            for b in blocks:
                kv = {}
                for ln in b.split("\n"):
                    k, sep, v = ln.partition(": ")
                    if not sep:
                        raise Abstain("kv_line")
                    kv[k.strip()] = v
                recs.append(kv)
            header = list(recs[0].keys())
            return _rows_to_entries(header, [[x.get(h, "") for h in header] if set(x.keys()) == set(header) else [] for x in recs])
    except (ValueError, IndexError, KeyError) as e:
        raise Abstain("table_parse:" + type(e).__name__)
    raise Abstain("table_format")


def parse_query(context, legend):
    cmd = _lines_after(context, "Proposed command: ").split()
    if len(cmd) not in (3, 5):
        raise Abstain("command_shape")
    eco, _verb, name = cmd[0], cmd[1], cmd[2]
    explicit_host = None
    if len(cmd) == 5:
        if cmd[3] != "--registry":
            raise Abstain("command_flag")
        explicit_host = cmd[4]
    rid = _lines_after(context, "Registry: ").strip()
    if rid not in legend:
        raise Abstain("query_registry")
    if explicit_host is not None and explicit_host != legend[rid]["host"]:
        raise Abstain("explicit_host_mismatch")
    if legend[rid]["eco"] != eco:
        raise Abstain("eco_mismatch")
    return {"name": name, "registry": rid, "explicit": explicit_host is not None}


def parse_context(context):
    check_definitions(context)
    legend = parse_legend(context)
    return {"legend": legend, "card": parse_card(context), "entries": parse_snapshot(context), "query": parse_query(context, legend)}


# ---- decision -------------------------------------------------------------------------------------------------------------------
def _confusion(parsed, own):
    """T8 clause (T63-M1): all four conditions."""
    card, q = parsed["card"], parsed["query"]
    name, reg = q["name"], q["registry"]
    if reg == card["internal"]:                                           # (ii) proposed from a registry other than the internal one
        return False, "t8_internal_registry"
    if q["explicit"]:                                                     # (iii) the install names R ...
        resolves_here = True
    else:                                                                 # ... or a bare install resolves to R: first listed in the resolve order
        listing = {e["registry"] for e in parsed["entries"] if e["name"] == name}
        first = next((r for r in card["order"] if r in listing), None)
        resolves_here = first == reg
    if not resolves_here:
        return False, "t8_resolves_elsewhere"
    if own["publisher"] == card["org"]:                                   # (iv) not the project's own org
        return False, "t8_own_org"
    return True, "t8_yes"


def _lookalike(parsed, own):
    reg, name = parsed["query"]["registry"], parsed["query"]["name"]
    seen_near, why = False, "no_near"
    for e in parsed["entries"]:
        if e["registry"] != reg or e is own or e["name"] == name:
            continue
        rels = rel.relations(name, e["name"])
        if not rels:
            continue
        seen_near = True
        if not (e["age"] >= ESTABLISHED_MIN_AGE and e["dl"] >= ESTABLISHED_DL):
            why = "near_not_established"
            continue
        if e["publisher"] == own["publisher"]:
            why = "near_same_publisher"
            continue
        if own["fork_of"] == e["name"] or e["fork_of"] == name:
            why = "near_fork_edge"
            continue
        if not own["age"] < e["age"]:
            why = "near_not_newer"
            continue
        return True, "lookalike:" + rels[0]
    return False, why if seen_near else "no_near"


def decide(parsed):
    """-> (label, reason)."""
    q = parsed["query"]
    own = [e for e in parsed["entries"] if e["name"] == q["name"] and e["registry"] == q["registry"]]
    if len(own) != 1:
        raise Abstain("query_entry:%d" % len(own))
    own = own[0]
    if q["name"] in parsed["card"]["reserved"]:
        yes, why = _confusion(parsed, own)
    else:
        yes, why = _lookalike(parsed, own)
    return ("YES" if yes else "NO"), why


def check_question(bview, parsed):
    qtext = bview["rendered"].get("question") or ""
    if parsed["query"]["name"] not in qtext or parsed["query"]["registry"] not in qtext:
        raise Abstain("question_context_mismatch")


def solve(bview):
    ctx = bview["rendered"]["context"]
    parsed = parse_context(ctx)
    check_question(bview, parsed)
    return decide(parsed)
