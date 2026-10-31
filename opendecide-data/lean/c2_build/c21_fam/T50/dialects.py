"""T50 policy-card BODY dialects (A15, K29). Pure functions; no I/O, no randomness.

The card body is rendered in one of 7 dialects inside C2's fixed scaffold (scaffold sha unchanged):
  trained (5)            dialect.json  dialect.ts  dialect.yaml  dialect.md_table  dialect.prose
  held out, dev only (2) dialect.xml   dialect.cli_help

Every dialect renders the SAME facts (every value of the dict that T50.cards.make_card builds, lists in full) and
nothing else: no hand-picked names, only the card's own values, the generic slot labels (the card's own keys such as
`protected_branches`) and a little generic structure (JSON `properties`, XML `item`, "The ... is ..." in prose).
`extract_slots(dialect, text)` parses a rendering back into the card's dict; `facts_equal` is the K29 round-trip check.

Card values the card body carries (all 16 keys of the card dict): card_id, display_name, allowed_roots,
workspace_root, protected_branches, trusted_remotes, trusted_registries, trusted_hosts, context_lists (contained /
shared / production), database_lists (same lanes; the `sql.lane:` fact is shown by the card), ask_on_soft,
unknown_cmd_policy, sudo_policy, sudo_listed, hook_policy (hooks_must_not_be_skipped, skip_without_failure,
own_config_paths: the `card.own_config:` fact is shown by the card), digest_pin_requirement. A card with a key outside
this list, a missing key or a value that cannot round-trip (whitespace, quotes, commas, a trailing dot, the word
"none") is REFUSED with ValueError instead of being silently cut.

SCAFFOLD. C2's fixed prompt scaffold belongs to L-0 and is NOT available to L-A. `STUB_SCAFFOLD` below is a clearly
marked stand-in with a single {{CARD_BODY}} placeholder so the plumbing and the K29 assert can be tested. When L-0
delivers the real scaffold, K29 calls `scaffold_sha_ok(prompt, scaffold=REAL_SCAFFOLD)` on every rendered prompt (must be
100%); nothing here depends on the stub's text.
"""
import json
import math
import re
import xml.etree.ElementTree as ET

from LA_COMMON.canon import canon, sha_text, stable_fraction

TRAINED_DIALECTS = ("dialect.json", "dialect.ts", "dialect.yaml", "dialect.md_table", "dialect.prose")
HELDOUT_DIALECTS = ("dialect.xml", "dialect.cli_help")
ALL_DIALECTS = TRAINED_DIALECTS + HELDOUT_DIALECTS

STR, BOOL, LIST, MAP_STR, MAP_LIST = "str", "bool", "list", "map:str", "map:list"
SCHEMA = {                                    # order = the order of the card dict built by T50.cards.make_card
    "card_id": STR, "display_name": STR, "allowed_roots": LIST, "workspace_root": STR, "protected_branches": LIST,
    "trusted_remotes": MAP_STR, "trusted_registries": LIST, "trusted_hosts": LIST,
    "context_lists": MAP_LIST, "database_lists": MAP_LIST, "ask_on_soft": BOOL, "unknown_cmd_policy": STR,
    "sudo_policy": STR, "sudo_listed": LIST,
    "hook_policy": {"hooks_must_not_be_skipped": BOOL, "skip_without_failure": STR, "own_config_paths": LIST},
    "digest_pin_requirement": STR,
}
_ATOM = re.compile(r"[A-Za-z0-9_./@+~-]*[A-Za-z0-9_/@+~-]\Z")      # no whitespace, quote, comma, '|', '<'; no trailing dot
_KEY = re.compile(r"[a-z][a-z0-9_]*\Z")
_NONE = "none"                                                        # how the flat dialects write an empty list

# generic words the renderers add around the card's own values (the K29 'nothing else' test checks against this set)
STRUCTURE_WORDS = frozenset("""
id title type object properties const declare policy card slot value this is are the and none true false item entry
key usage gate options default str list bool
""".split())


# ------------------------------------------------------------------------------------------------ validation
def _atom(v, what):
    if not isinstance(v, str) or not _ATOM.match(v) or v == _NONE:
        raise ValueError("value of %s cannot be rendered round-trip safely: %r" % (what, v))
    return v


def _conform_value(name, kind, v):
    if isinstance(kind, dict):
        if not isinstance(v, dict) or set(v) != set(kind):
            raise ValueError("%s must have exactly the fields %s" % (name, sorted(kind)))
        return {f: _conform_value(name + "." + f, k, v[f]) for f, k in kind.items()}
    if kind == STR:
        return _atom(v, name)
    if kind == BOOL:
        if not isinstance(v, bool):
            raise ValueError("%s must be a bool, got %r" % (name, v))
        return v
    if kind == LIST:
        if not isinstance(v, (list, tuple)):
            raise ValueError("%s must be a list" % name)
        return [_atom(x, name) for x in v]
    if kind in (MAP_STR, MAP_LIST):
        if not isinstance(v, dict) or not v:
            raise ValueError("%s must be a non-empty mapping" % name)
        sub = STR if kind == MAP_STR else LIST
        out = {}
        for k, x in v.items():
            if not isinstance(k, str) or not _KEY.match(k):
                raise ValueError("%s has a key that cannot round-trip: %r" % (name, k))
            out[k] = _conform_value(name + "." + k, sub, x)
        return out
    raise AssertionError(kind)


def conform(card):
    """Validated copy of the card in SCHEMA key order. ValueError if keys differ from the 16 known card keys."""
    if not isinstance(card, dict) or set(card) != set(SCHEMA):
        extra = sorted(set(card) - set(SCHEMA)) if isinstance(card, dict) else "?"
        miss = sorted(set(SCHEMA) - set(card)) if isinstance(card, dict) else "?"
        raise ValueError("card keys differ from the dialect schema (unknown %s, missing %s)" % (extra, miss))
    return {k: _conform_value(k, kind, card[k]) for k, kind in SCHEMA.items()}


def facts_equal(card, extracted):
    """K29 round trip: every slot value of the card equals the extracted one (type strict, list order strict)."""
    try:
        return canon(conform(card)) == canon(conform(extracted))
    except (ValueError, TypeError):
        return False


def fact_diff(card, extracted):
    """Names of the slots that differ (debugging aid; [] when facts_equal)."""
    a, b = conform(card), extracted
    return [k for k in SCHEMA if canon(a[k]) != canon(b.get(k))]


# ------------------------------------------------------------------------------------------------ flat helpers
def _kind_of(path):
    parts = path.split(".")
    top = SCHEMA.get(parts[0])
    if top is None:
        raise ValueError("unknown slot %r" % path)
    if len(parts) == 1:
        if isinstance(top, dict) or top in (MAP_STR, MAP_LIST):
            raise ValueError("slot %r needs a sub-key" % path)
        return top
    if len(parts) != 2:
        raise ValueError("bad slot path %r" % path)
    if isinstance(top, dict):
        if parts[1] not in top:
            raise ValueError("unknown field %r" % path)
        return top[parts[1]]
    if top == MAP_STR:
        return STR
    if top == MAP_LIST:
        return LIST
    raise ValueError("slot %r has no sub-keys" % parts[0])


def _flatten(card):
    """[(dotted path, kind, value)] in card order; the leaves of the 14 slots other than card_id / display_name too."""
    out = []
    for k, kind in SCHEMA.items():
        v = card[k]
        if isinstance(kind, dict):
            out += [("%s.%s" % (k, f), kind[f], v[f]) for f in kind]
        elif kind in (MAP_STR, MAP_LIST):
            sub = STR if kind == MAP_STR else LIST
            out += [("%s.%s" % (k, f), sub, x) for f, x in v.items()]
        else:
            out.append((k, kind, v))
    return out


def _unflatten(pairs):
    """pairs: [(dotted path, python value)] -> card dict (validated)."""
    d = {}
    for path, val in pairs:
        _kind_of(path)
        parts = path.split(".")
        if len(parts) == 1:
            d[parts[0]] = val
        else:
            d.setdefault(parts[0], {})[parts[1]] = val
    return conform(d)


def _flat_value(kind, raw, sep):
    raw = raw.strip()
    if kind == STR:
        return raw
    if kind == BOOL:
        if raw not in ("true", "false"):
            raise ValueError("bad boolean %r" % raw)
        return raw == "true"
    return [] if raw == _NONE else [x.strip() for x in raw.split(sep)]


def _bool_text(b):
    return "true" if b else "false"


def _list_text(v, sep):
    return sep.join(v) if v else _NONE


# ------------------------------------------------------------------------------------------------ json (JSON schema)
def _jv(v, ind=0):
    if isinstance(v, bool):
        return _bool_text(v)
    if isinstance(v, str):
        return json.dumps(v)
    if isinstance(v, list):
        return "[" + ", ".join(json.dumps(x) for x in v) + "]"
    pad = "  " * (ind + 1)
    return "{\n" + ",\n".join("%s%s: %s" % (pad, json.dumps(k), _jv(x, ind + 1)) for k, x in v.items()) + "\n" + "  " * ind + "}"


def _r_json(card):
    props = [("\"%s\": {\"const\": %s}" % (k, _jv(card[k], 2))) for k in SCHEMA if k not in ("card_id", "display_name")]
    return ("{\n  \"$id\": %s,\n  \"title\": %s,\n  \"type\": \"object\",\n  \"properties\": {\n    %s\n  }\n}"
            % (json.dumps(card["card_id"]), json.dumps(card["display_name"]), ",\n    ".join(props)))


def _x_json(text):
    obj = json.loads(text)
    props = obj["properties"]
    d = {"card_id": obj["$id"], "display_name": obj["title"]}
    d.update({k: v["const"] for k, v in props.items()})
    return conform(d)


# ------------------------------------------------------------------------------------------------ ts (type-literal signature)
def _tsv(v, ind=0):
    if isinstance(v, bool):
        return _bool_text(v)
    if isinstance(v, str):
        return json.dumps(v)
    if isinstance(v, list):
        return "[" + ", ".join(json.dumps(x) for x in v) + "]"
    pad = "  " * (ind + 1)
    return "{\n" + "".join("%s%s: %s;\n" % (pad, k, _tsv(x, ind + 1)) for k, x in v.items()) + "  " * ind + "}"


def _r_ts(card):
    return "declare const policy_card: %s;" % _tsv(card)


_TS_TOK = re.compile(r'\s*(?:(?P<str>"[^"\\]*")|(?P<punct>[{}\[\]:;,])|(?P<id>[A-Za-z_][A-Za-z0-9_]*))')


def _x_ts(text):
    toks, pos = [], 0
    text = text.rstrip()
    while pos < len(text):
        m = _TS_TOK.match(text, pos)
        if not m:
            raise ValueError("ts: cannot tokenise at %d" % pos)
        toks.append((m.lastgroup, m.group(m.lastgroup)))
        pos = m.end()
    i = 0

    def peek():
        return toks[i] if i < len(toks) else (None, None)

    def take(kind=None, val=None):
        nonlocal i
        k, v = peek()
        if k is None or (kind and k != kind) or (val and v != val):
            raise ValueError("ts: unexpected %r at token %d" % (v, i))
        i += 1
        return v

    def value():
        k, v = peek()
        if k == "str":
            take()
            return json.loads(v)
        if k == "id" and v in ("true", "false"):
            take()
            return v == "true"
        if v == "[":
            take()
            out = []
            while peek()[1] != "]":
                out.append(value())
                if peek()[1] == ",":
                    take()
            take("punct", "]")
            return out
        if v == "{":
            take()
            out = {}
            while peek()[1] != "}":
                key = take("id")
                take("punct", ":")
                out[key] = value()
                if peek()[1] in (";", ","):
                    take()
            take("punct", "}")
            return out
        raise ValueError("ts: bad value %r" % (v,))

    take("id", "declare")
    take("id", "const")
    take("id")
    take("punct", ":")
    d = value()
    if peek()[1] == ";":
        take()
    if i != len(toks):
        raise ValueError("ts: trailing tokens")
    return conform(d)


# ------------------------------------------------------------------------------------------------ yaml
def _r_yaml(card):
    out = []

    def emit(key, v, ind):
        pad = "  " * ind
        if isinstance(v, dict):
            out.append("%s%s:" % (pad, key))
            for k2, x in v.items():
                emit(k2, x, ind + 1)
        elif isinstance(v, list):
            if not v:
                out.append("%s%s: []" % (pad, key))
            else:
                out.append("%s%s:" % (pad, key))
                out.extend("%s  - %s" % (pad, json.dumps(x)) for x in v)
        else:
            out.append("%s%s: %s" % (pad, key, _tsv(v)))
    for k in SCHEMA:
        emit(k, card[k], 0)
    return "\n".join(out)


def _yaml_scalar(tok):
    tok = tok.strip()
    if tok in ("true", "false"):
        return tok == "true"
    if tok == "[]":
        return []
    if len(tok) >= 2 and tok[0] == '"' and tok[-1] == '"':
        return json.loads(tok)
    raise ValueError("yaml: bad scalar %r" % tok)


def _x_yaml(text):
    lines = [ln for ln in text.split("\n") if ln.strip()]
    pos = 0

    def indent(ln):
        return len(ln) - len(ln.lstrip(" "))

    def block(ind):
        nonlocal pos
        out = {}
        while pos < len(lines) and indent(lines[pos]) == ind and not lines[pos].lstrip().startswith("- "):
            m = re.fullmatch(r" *([A-Za-z_][A-Za-z0-9_]*):(?: (.*))?", lines[pos])
            if not m:
                raise ValueError("yaml: bad line %r" % lines[pos])
            key, rest = m.group(1), m.group(2)
            pos += 1
            if rest:
                out[key] = _yaml_scalar(rest)
            elif pos < len(lines) and indent(lines[pos]) > ind:
                child = indent(lines[pos])
                if lines[pos].lstrip().startswith("- "):
                    items = []
                    while pos < len(lines) and indent(lines[pos]) == child and lines[pos].lstrip().startswith("- "):
                        items.append(_yaml_scalar(lines[pos].lstrip()[2:]))
                        pos += 1
                    out[key] = items
                else:
                    out[key] = block(child)
            else:
                raise ValueError("yaml: empty value for %s" % key)
        return out
    d = block(0)
    if pos != len(lines):
        raise ValueError("yaml: unparsed lines from %d" % pos)
    return conform(d)


# ------------------------------------------------------------------------------------------------ md_table
def _r_md(card):
    rows = ["| slot | value |", "| --- | --- |", "| card_id | %s |" % card["card_id"], "| display_name | %s |" % card["display_name"]]
    for path, kind, v in _flatten(card):
        if path in ("card_id", "display_name"):
            continue
        rows.append("| %s | %s |" % (path, _bool_text(v) if kind == BOOL else _list_text(v, ", ") if kind == LIST else v))
    return "\n".join(rows)


def _x_md(text):
    lines = [ln for ln in text.split("\n") if ln.strip()]
    if lines[:2] != ["| slot | value |", "| --- | --- |"]:
        raise ValueError("md_table: bad header")
    pairs = []
    for ln in lines[2:]:
        m = re.fullmatch(r"\| (\S+) \| (.+) \|", ln)
        if not m:
            raise ValueError("md_table: bad row %r" % ln)
        path = m.group(1)
        pairs.append((path, _flat_value(_kind_of(path), m.group(2), ", ")))
    return _unflatten(pairs)


# ------------------------------------------------------------------------------------------------ prose
def _r_prose(card):
    sents = ["This is the policy card %s (%s)." % (card["display_name"], card["card_id"])]
    for path, kind, v in _flatten(card):
        if path in ("card_id", "display_name"):
            continue
        subject = "The " + path.replace(".", " ")
        if kind == STR:
            sents.append("%s is %s." % (subject, v))
        elif kind == BOOL:
            sents.append("%s is %s." % (subject, _bool_text(v)))
        elif not v:
            sents.append("%s is %s." % (subject, _NONE))
        elif len(v) == 1:
            sents.append("%s is %s." % (subject, v[0]))
        else:
            sents.append("%s are %s." % (subject, ", ".join(v[:-1]) + " and " + v[-1]))
    return " ".join(sents)


def _x_prose(text):
    sents = re.split(r"\.(?: +|\Z)", text.strip())
    if sents and sents[-1] == "":
        sents.pop()
    m = re.fullmatch(r"This is the policy card (\S+) \((\S+)\)", sents[0]) if sents else None
    if not m:
        raise ValueError("prose: bad first sentence")
    pairs = [("display_name", m.group(1)), ("card_id", m.group(2))]
    for s in sents[1:]:
        m = re.fullmatch(r"The (\S+)(?: (\S+))? (?:is|are) (.+)", s)
        if not m:
            raise ValueError("prose: bad sentence %r" % s)
        path = m.group(1) + ("." + m.group(2) if m.group(2) else "")
        kind = _kind_of(path)
        raw = m.group(3)
        if kind == LIST and " and " in raw:
            head, last = raw.rsplit(" and ", 1)
            raw = ",".join(head.split(", ") + [last])
        pairs.append((path, _flat_value(kind, raw, ",")))
    return _unflatten(pairs)


# ------------------------------------------------------------------------------------------------ xml (held out)
def _r_xml(card):
    out = ['<policy_card card_id="%s" display_name="%s">' % (card["card_id"], card["display_name"])]

    def items(v, pad):
        return ["%s<item>%s</item>" % (pad, x) for x in v]

    for k, kind in SCHEMA.items():
        if k in ("card_id", "display_name"):
            continue
        v = card[k]
        if isinstance(kind, dict):
            out.append("  <%s>" % k)
            for f, fk in kind.items():
                if fk == LIST:
                    out += ["    <%s>" % f] + items(v[f], "      ") + ["    </%s>" % f] if v[f] else ["    <%s/>" % f]
                else:
                    out.append("    <%s>%s</%s>" % (f, _bool_text(v[f]) if fk == BOOL else v[f], f))
            out.append("  </%s>" % k)
        elif kind == MAP_STR:
            out.append("  <%s>" % k)
            out += ['    <entry key="%s">%s</entry>' % (a, b) for a, b in v.items()]
            out.append("  </%s>" % k)
        elif kind == MAP_LIST:
            out.append("  <%s>" % k)
            for a, b in v.items():
                out += ['    <entry key="%s">' % a] + items(b, "      ") + ["    </entry>"] if b else ['    <entry key="%s"/>' % a]
            out.append("  </%s>" % k)
        elif kind == LIST:
            out += ["  <%s>" % k] + items(v, "    ") + ["  </%s>" % k] if v else ["  <%s/>" % k]
        else:
            out.append("  <%s>%s</%s>" % (k, _bool_text(v) if kind == BOOL else v, k))
    out.append("</policy_card>")
    return "\n".join(out)


def _x_xml(text):
    root = ET.fromstring(text)
    if root.tag != "policy_card":
        raise ValueError("xml: bad root")

    def leaf(el, kind):
        if kind == BOOL:
            return _flat_value(BOOL, el.text or "", ",")
        if kind == STR:
            return (el.text or "").strip()
        return [(c.text or "").strip() for c in el if c.tag == "item"]
    d = {"card_id": root.get("card_id"), "display_name": root.get("display_name")}
    for el in root:
        kind = SCHEMA.get(el.tag)
        if kind is None:
            raise ValueError("xml: unknown slot %r" % el.tag)
        if isinstance(kind, dict):
            d[el.tag] = {c.tag: leaf(c, kind[c.tag]) for c in el}
        elif kind in (MAP_STR, MAP_LIST):
            d[el.tag] = {c.get("key"): leaf(c, STR if kind == MAP_STR else LIST) for c in el if c.tag == "entry"}
        else:
            d[el.tag] = leaf(el, kind)
    return conform(d)


# ------------------------------------------------------------------------------------------------ cli_help (held out)
def _r_cli(card):
    rows = []
    for p, kind, v in _flatten(card):
        if p in ("card_id", "display_name"):
            continue
        val = _bool_text(v) if kind == BOOL else _list_text(v, ",") if kind == LIST else v
        rows.append("  --%s <%s>  [default: %s]" % (p.replace("_", "-"), kind.upper(), val))
    return "Usage: gate [OPTIONS]\n\nPolicy card: %s (%s)\n\nOptions:\n%s" % (card["display_name"], card["card_id"], "\n".join(rows))


def _x_cli(text):
    lines = text.split("\n")
    m = re.fullmatch(r"Policy card: (\S+) \((\S+)\)", lines[2]) if len(lines) > 4 and lines[0] == "Usage: gate [OPTIONS]" else None
    if not m or lines[4] != "Options:":
        raise ValueError("cli_help: bad header")
    pairs = [("display_name", m.group(1)), ("card_id", m.group(2))]
    for ln in lines[5:]:
        m = re.fullmatch(r"  --(\S+) <(STR|LIST|BOOL)> +\[default: (.+)\]", ln)
        if not m:
            raise ValueError("cli_help: bad option line %r" % ln)
        path = m.group(1).replace("-", "_")
        kind = _kind_of(path)
        if kind.upper() != m.group(2):
            raise ValueError("cli_help: type tag mismatch for %s" % path)
        pairs.append((path, _flat_value(kind, m.group(3), ",")))
    return _unflatten(pairs)


_RENDER = {"dialect.json": _r_json, "dialect.ts": _r_ts, "dialect.yaml": _r_yaml, "dialect.md_table": _r_md,
           "dialect.prose": _r_prose, "dialect.xml": _r_xml, "dialect.cli_help": _r_cli}
_EXTRACT = {"dialect.json": _x_json, "dialect.ts": _x_ts, "dialect.yaml": _x_yaml, "dialect.md_table": _x_md,
            "dialect.prose": _x_prose, "dialect.xml": _x_xml, "dialect.cli_help": _x_cli}


def render_card_body(dialect, card):
    """The policy-card body text for `card` (dict from T50.cards.make_card) in `dialect`."""
    if dialect not in _RENDER:
        raise ValueError("unknown dialect %r" % (dialect,))
    return _RENDER[dialect](conform(card))


def extract_slots(dialect, text):
    """Parse a rendering back into the card's dict (all 16 keys). ValueError if the text is not a valid rendering."""
    if dialect not in _EXTRACT:
        raise ValueError("unknown dialect %r" % (dialect,))
    try:
        return _EXTRACT[dialect](text)
    except (KeyError, TypeError, IndexError, json.JSONDecodeError, ET.ParseError) as e:
        raise ValueError("%s: cannot parse (%s: %s)" % (dialect, type(e).__name__, e))


# ------------------------------------------------------------------------------------------------ assignment per group
def is_heldout_dialect(dialect):
    return dialect in HELDOUT_DIALECTS


def heldout_tag(dialect):
    """The `heldout_family` tag a spec must carry when it uses `dialect` (None for a trained dialect)."""
    return dialect if dialect in HELDOUT_DIALECTS else None


def dialect_for_group(group_id, split, heldout_family=None, allow_heldout_dev=False):
    """One dialect per spec GROUP (pair / quad): every member of the group calls this with the same group_id.

    train               -> a TRAINED dialect (uniform by hash, so each holds about 20% of groups; K29 band 12-25%).
    dev, tagged         -> heldout_family in ("dialect.xml", "dialect.cli_help") gets exactly that dialect.
    dev, other tag      -> a TRAINED dialect (a spec held out for another reason does not also change the dialect).
    dev, untagged       -> a TRAINED dialect; with allow_heldout_dev=True any of the 7 (then the caller MUST tag the spec
                           with heldout_tag(dialect), or the 40-row held-out budget of section 9 is exceeded).
    A train spec carrying any heldout_family, or a held-out dialect tag on a non-dev spec, raises ValueError (GV9)."""
    if split not in ("train", "dev"):
        raise ValueError("split must be 'train' or 'dev', got %r" % (split,))
    if heldout_family in HELDOUT_DIALECTS:
        if split != "dev":
            raise ValueError("a spec tagged %s must be a dev spec" % heldout_family)
        return heldout_family
    if heldout_family is not None and split != "dev":
        raise ValueError("a train spec cannot carry heldout_family %r" % (heldout_family,))
    pool = ALL_DIALECTS if (split == "dev" and heldout_family is None and allow_heldout_dev) else TRAINED_DIALECTS
    return pool[min(int(stable_fraction("dialect.group", split, group_id) * len(pool)), len(pool) - 1)]


def dialect_shares(group_ids, split="train", **kw):
    """{dialect: share of groups} (K29 helper)."""
    counts = {d: 0 for d in ALL_DIALECTS}
    for g in group_ids:
        counts[dialect_for_group(g, split, **kw)] += 1
    n = max(1, len(group_ids))
    return {d: c / n for d, c in counts.items()}


# ------------------------------------------------------------------------------------------------ token cost (K29 report)
def est_tokens(text):
    """Stand-in estimator (chars / 3.6), the same one-liner as T50/gates.py; the real tokenizer is L-0's."""
    return int(math.ceil(len(text) / 3.6))


def token_cost_by_dialect(cards, dialects=ALL_DIALECTS):
    """{dialect: mean estimated tokens of the card BODY over `cards`} (K29 'token cost per dialect reported')."""
    cards = list(cards)
    if not cards:
        raise ValueError("no cards")
    return {d: sum(est_tokens(render_card_body(d, c)) for c in cards) / len(cards) for d in dialects}


def token_cost_report(cards):
    """{dialect: {mean_tokens, pct_over_json}}; the design expects verbose dialects at +5..15% over JSON (report only)."""
    mean = token_cost_by_dialect(cards)
    base = mean["dialect.json"]
    return {d: {"mean_tokens": round(m, 2), "pct_over_json": round(100.0 * (m / base - 1.0), 1)} for d, m in mean.items()}


# ------------------------------------------------------------------------------------------------ scaffold
PLACEHOLDER = "{{CARD_BODY}}"
STUB_SCAFFOLD = (
    "[[STUB SCAFFOLD: this is NOT C2's real fixed scaffold. L-0 owns the real one; K29 re-runs the scaffold-sha assert "
    "with it.]]\n"
    "You review one proposed agent action against the policy card and answer ALLOW, ASK or BLOCK.\n"
    "<policy_card>\n" + PLACEHOLDER + "\n</policy_card>\n"
    "[[END STUB SCAFFOLD]]"
)


def scaffold_sha(scaffold=STUB_SCAFFOLD):
    """sha256 of the scaffold text WITH the placeholder (this is the value K29 pins)."""
    return sha_text(scaffold)


SCAFFOLD_SHA = scaffold_sha(STUB_SCAFFOLD)


def _split_scaffold(scaffold):
    parts = scaffold.split(PLACEHOLDER)
    if len(parts) != 2:
        raise ValueError("scaffold must hold exactly one %s placeholder" % PLACEHOLDER)
    return parts


def wrap_in_scaffold(body, scaffold=STUB_SCAFFOLD):
    pre, post = _split_scaffold(scaffold)
    if PLACEHOLDER in body:
        raise ValueError("card body contains the placeholder")
    return pre + body + post


def unwrap_from_scaffold(prompt, scaffold=STUB_SCAFFOLD):
    """The body inside the prompt, or None if the text outside the body is not byte-identical to the scaffold."""
    pre, post = _split_scaffold(scaffold)
    if len(prompt) < len(pre) + len(post) or not prompt.startswith(pre) or not prompt.endswith(post):
        return None
    return prompt[len(pre):len(prompt) - len(post)]


def scaffold_sha_ok(prompt, scaffold=STUB_SCAFFOLD, body=None):
    """K29 assert: the prompt is the scaffold with a body substituted, i.e. putting the placeholder back where the body
    was gives a text whose sha equals the scaffold's sha. With `body` given, the prompt must equal the wrap exactly."""
    inner = unwrap_from_scaffold(prompt, scaffold)
    if inner is None or inner == "":
        return False
    if body is not None and inner != body:
        return False
    pre, post = _split_scaffold(scaffold)
    restored = prompt[:len(pre)] + PLACEHOLDER + prompt[len(prompt) - len(post):]      # the body put back as a placeholder
    return sha_text(restored) == scaffold_sha(scaffold)


def render_prompt(dialect, card, scaffold=STUB_SCAFFOLD):
    """Convenience: the card body in `dialect` inside the scaffold."""
    return wrap_in_scaffold(render_card_body(dialect, card), scaffold)
