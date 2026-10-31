"""families/T35/solver_b.py: T35 solver B, written from G0_SPEC.md (not from plugin.py).

parse(row, ctx) reads the RENDERED row back into the canonical facts:
  - the rules block by this module's own readers, one per container: the robots.txt text (RFC 9309 grouping: a run
    of User-agent lines opens a group, Allow / Disallow lines join the open group, blank lines are ignored), the
    markdown table (grouped by its group column) and the JSON export (json.loads; keys user_agents, type, pattern);
  - the fetch request block (token, URL, printed path, optional status) by its own regular expression; the status
    text maps to its key through this module's own table;
  - the card (row.card on yes/no rows, the instructions before the question on choice rows) by six full-text
    patterns (full, compact and short card, each with and without the status item); its two precedence sentences through the lexicon registry (admitted forms
    only: G-LEX vouches for each paraphrase's meaning);
  - the narrative skin (Mode T) through skin.parse_skin; Mode F narrative facts are left to G3-H;
  - the question through its wording template (its admitted meaning is the question form);
  - on choice rows, every option text back to its key ("allow:<pattern>", "disallow:<pattern>" or "none").
Facts that appear twice (token in a wording and in the request) must read the same, and the printed path must equal
the path this module cuts from the URL.

solve_b(view) decides by brute force: the applying lines are found by scanning every group; every applying line is
compiled to a regular expression and tried on the decoded path (re.match, prefix); the matches are compared pairwise
by pattern length with an explicit rule (longer wins; at equal length Allow beats Disallow). The fetch status and the
question map through lookup tables. Imports no solver-A code (plugin.check_independence).
"""
from __future__ import annotations

import json
import re

from c2_kit import skin as K
from c2_kit import slots as S

PURPOSE_SET = {"indexing": ["search indexing"], "archiving": ["web archiving"], "prices": ["price comparison"],
               "accessibility": ["accessibility checks"], "links": ["link checking"],
               "research": ["academic research"], "previews": ["link previews"]}
PURPOSE_SCHEMA = S.category_slot("indexing", PURPOSE_SET).schema
SCHEMA = {"SITE": ("name", ()), "OPERATOR": ("name", ()), "PURPOSE": PURPOSE_SCHEMA, "UA": ("id", ())}
NARRATIVE = ("SITE", "OPERATOR", "PURPOSE")
STATUS_KEY = {"200 OK": "200", "401 Unauthorized": "401", "403 Forbidden": "403", "404 Not Found": "404",
              "410 Gone": "410", "500 Internal Server Error": "500", "502 Bad Gateway": "502",
              "503 Service Unavailable": "503", "no response (server unreachable)": "unreachable"}
STATUS_RULE = {"200": "use_lines", "401": "fetch_all", "403": "fetch_all", "404": "fetch_all", "410": "fetch_all",
               "500": "fetch_none", "502": "fetch_none", "503": "fetch_none", "unreachable": "fetch_none"}
EFFECT_WORD = {"Allow": "allow", "Disallow": "disallow"}
UNRESERVED = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~")
NONE_OPTION = "No applying line matches (so the crawler may fetch the URL)"
QUESTION = {"yn_fetch": lambda ok: 1 if ok else 0, "yn_double_neg": lambda ok: 1 if ok else 0,
            "yn_skip": lambda ok: 0 if ok else 1,
            "yn_not_allowed": lambda ok: 0 if ok else 1, "yn_prevented": lambda ok: 0 if ok else 1}
WANT_SEMS = ("prec.robots_longest", "prec.robots_tie_allow")

CLOSED = ("The file is the robots.txt of the URL's site, and the file, the request and these rules are complete: "
          "nothing else changes the answer.")
CARD_BODY = {
    "full": ('Robots rules (they decide this request):\n'
             '1. Group: a group applies if one of its User-agent values equals the crawler\'s product token, '
             'ignoring case (equal, not just a prefix). All applying groups are combined. If none applies, the "*" '
             'group applies; if there is none, no group applies. The lines of the applying groups are the applying '
             'lines; no other line counts.\n'
             '2. Path: the URL from the first "/" after the host, query included (the path to check). Decode each '
             '"%XX" that encodes an ASCII letter, digit, "-", ".", "_" or "~"; keep every other "%XX" as written.\n'
             '3. Match: a line matches if its pattern matches the start of the path. "*" matches any run of '
             'characters (even empty, even "/"); a final "$" means the path must end there; every other character '
             'must match exactly, case-sensitive.\n'
             '4. @LONGEST@\n'
             '5. @TIE@\n'
             '6. If no applying line matches, the crawler may fetch the URL.\n'),
    "compact": ('Robots rules:\n'
                '1. Group: a group applies if a User-agent value equals the crawler\'s token, ignoring case (equal, '
                'not a prefix); all applying groups are combined. If none applies, the "*" group applies; if there is '
                'none, no group applies. Their lines are the applying lines; no other line counts.\n'
                '2. Path: the URL from the first "/" after the host, query included. Decode each "%XX" for an ASCII '
                'letter, digit, "-", ".", "_" or "~"; keep every other "%XX" as written.\n'
                '3. Match: a line matches if its pattern matches the start of the path: "*" matches any run (even '
                'empty, even "/"); a final "$" means the path must end there; every other character must match '
                'exactly, case-sensitive.\n'
                '4. @LONGEST@\n'
                '5. @TIE@\n'
                '6. If no applying line matches, the crawler may fetch the URL.\n'),
    "short": ('Robots rules, short form:\n'
              '- Group: the groups whose User-agent value equals the crawler\'s token (case ignored; all combined), '
              'else the "*" group, else none; only their lines apply.\n'
              '- Path: the URL from the first "/" after the host, query included; decode "%XX" only for ASCII '
              'letters, digits, "-", ".", "_" and "~".\n'
              '- Match: a pattern matches the start of the path; "*" is any run ("/" and empty included); a final '
              '"$" means the path ends there; case matters.\n'
              '- @LONGEST@\n'
              '- @TIE@\n'
              '- No applying line matches: may fetch.\n'),
}
CARD_STATUS = {
    "full": ('7. robots.txt fetch status, which overrides items 1-6: 2xx or none shown: use the lines. 4xx: the '
             'crawler may fetch any URL on the site. 5xx or no response: it may fetch none.\n'),
    "compact": ('7. robots.txt fetch status overrides items 1-6: 2xx or none shown: use the lines; 4xx: it may fetch '
                'any URL; 5xx or no response: it may fetch none.\n'),
    "short": ('- robots.txt status (overrides the lines): 4xx: may fetch any URL; 5xx or no response: may fetch '
              'none; 2xx or none shown: use the lines.\n'),
}


def _card_rx(text: str) -> re.Pattern:
    body = re.escape(text).replace("@LONGEST@", "(?P<longest>[^\\n]+?)").replace("@TIE@", "(?P<tie>[^\\n]+?)")
    return re.compile(body)


CARD_RES = tuple((st, with_status, _card_rx(CARD_BODY[st] + (CARD_STATUS[st] if with_status else "") + CLOSED))
                 for st in CARD_BODY for with_status in (False, True))
RAW_RE = re.compile(r"robots\.txt of the site:\n=== begin robots\.txt ===\n(?P<body>.*?)\n=== end robots\.txt ===",
                    re.S)
TABLE_RE = re.compile(r"robots\.txt of the site, one table row per line \(rows with the same group number form one "
                      r"group\):\n\| group \| line \| value \|\n\|---\|---\|---\|\n(?P<body>(?:\|[^\n]*\|\n?)+?)"
                      r"(?=\n\nFetch request:)")
JSON_RE = re.compile(r"robots\.txt of the site, as parsed into JSON by the site's tools:\n(?P<body>\{.*?\})"
                     r"(?=\n\nFetch request:)", re.S)
REQUEST_RE = re.compile(r"Fetch request:\n- crawler product token: (?P<ua>[^\n]+)\n- URL: (?P<url>[^\n]+)\n"
                        r"- path to check \(query included\): (?P<path>[^\n]+)"
                        r"(?:\n- robots\.txt fetch status: (?P<status>[^\n]+))?(?=\n\n|$)")
LINE_RE = re.compile(r"(?P<field>User-agent|Allow|Disallow): (?P<value>\S+)")
TABLE_ROW_RE = re.compile(r"\| (?P<g>\d+) \| (?P<field>User-agent|Allow|Disallow) \| (?P<value>\S+) \|")


class ParseError(ValueError):
    pass


def _one(rx, text, what):
    ms = list(rx.finditer(text))
    if len(ms) != 1:
        raise ParseError(f"{len(ms)} {what}(s) in the row")
    return ms[0]


def _agent(v: str) -> str:
    return "*" if v == "*" else S.parse("id", v)


def _pattern(v: str) -> str:
    return S.parse("glob", v, (), "raw")


def _raw_groups(body: str) -> list:
    groups, open_rules = [], False
    for ln in body.split("\n"):
        if not ln:
            continue
        m = LINE_RE.fullmatch(ln)
        if not m:
            raise ParseError(f"robots.txt line {ln!r}")
        if m["field"] == "User-agent":
            if not groups or open_rules:
                groups.append({"agents": [], "lines": []})
                open_rules = False
            groups[-1]["agents"].append(_agent(m["value"]))
        else:
            if not groups:
                raise ParseError("a rule line before any User-agent line")
            groups[-1]["lines"].append([EFFECT_WORD[m["field"]], _pattern(m["value"])])
            open_rules = True
    return groups


def _table_groups(body: str) -> list:
    by_num: dict = {}
    order = []
    for ln in body.strip("\n").split("\n"):
        m = TABLE_ROW_RE.fullmatch(ln)
        if not m:
            raise ParseError(f"table row {ln!r}")
        g = int(m["g"])
        if g not in by_num:
            if order and g != order[-1] + 1:
                raise ParseError("group numbers are not consecutive")
            by_num[g] = {"agents": [], "lines": []}
            order.append(g)
        elif g != order[-1]:
            raise ParseError("a group's rows are split")
        grp = by_num[g]
        if m["field"] == "User-agent":
            if grp["lines"]:
                raise ParseError("a User-agent row after a rule row in one group")
            grp["agents"].append(_agent(m["value"]))
        else:
            grp["lines"].append([EFFECT_WORD[m["field"]], _pattern(m["value"])])
    return [by_num[g] for g in order]


def _json_groups(body: str) -> list:
    data = json.loads(body)
    if set(data) != {"groups"}:
        raise ParseError("JSON export keys")
    out = []
    for g in data["groups"]:
        if set(g) != {"user_agents", "lines"}:
            raise ParseError("JSON group keys")
        out.append({"agents": [_agent(a) for a in g["user_agents"]],
                    "lines": [[EFFECT_WORD[x["type"]], _pattern(x["pattern"])] for x in g["lines"]]})
    return out


def _cut_path(url: str) -> str:
    """From the first "/" after the host; a URL without one is refused (G0 H4: the generator never writes one)."""
    after = url.split("://", 1)[1]
    slash = after.find("/")
    if slash < 0 or any(c in after[:slash] for c in "?#"):
        raise ParseError(f"URL {url!r} has no path after its host")
    return after[slash:]


def parse(row: dict, ctx) -> dict:
    state = row["state"]
    req = _one(REQUEST_RE, state, "fetch request block")
    found = [(rx, reader) for rx, reader in ((RAW_RE, _raw_groups), (TABLE_RE, _table_groups),
                                             (JSON_RE, _json_groups)) if rx.search(state)]
    if len(found) != 1:
        raise ParseError(f"{len(found)} rules blocks in the row")
    rx, reader = found[0]
    blk = _one(rx, state, "rules block")
    groups = reader(blk["body"])
    if not groups or any(not g["agents"] or not g["lines"] for g in groups):
        raise ParseError("every group needs User-agent lines and rule lines")
    if state[blk.end():req.start()] != "\n\n":
        raise ParseError("rules block and request are not separated by one blank line")
    head = state[:blk.start()]
    if not head.endswith("\n\n"):
        raise ParseError("narrative and rules block are not separated by one blank line")
    narrative = head[:-2]
    crawler = S.parse("id", req["ua"])
    url = S.parse("url", req["url"])
    path = S.parse("glob", req["path"], (), "raw")
    if path != _cut_path(url):
        raise ParseError(f"printed path {path!r} is not the URL's path {_cut_path(url)!r}")
    status = None
    if req["status"] is not None:
        if req["status"] not in STATUS_KEY:
            raise ParseError(f"unknown fetch status {req['status']!r}")
        status = STATUS_KEY[req["status"]]
    skin = ctx.skin(row["meta"]["c2"]["skin_id"])
    told = {}
    if skin.author_mode == "T":
        told = K.parse_skin(skin, narrative, SCHEMA)
        missing = [k for k in NARRATIVE if k not in told]
        if missing:
            raise ParseError(f"skin lacks the narrative slots {missing}")
    if row["qtype"] == "noul":               # yes/no rows: the card is the row's definitions block (G0 M21)
        card, question = row.get("card") or "", row["instructions"]
        if "\n\n" in question:
            raise ParseError("a yes/no row's instructions hold more than the question")
    else:                                    # choice rows: card, blank line, question
        if row.get("card"):
            raise ParseError("a choice row carries a definitions block")
        card, sep, question = row["instructions"].partition("\n\n")
        if not sep:
            raise ParseError("card and question are not separated")
    hits = [(m, ws) for st, ws, rx_ in CARD_RES for m in [rx_.fullmatch(card)] if m]
    if len(hits) != 1:
        raise ParseError("card text matches none of the card texts of the G0-lite spec")
    if hits[0][1] != (status is not None):          # the status item stands on a card exactly when the request shows a status
        raise ParseError("the card's status item and the request's status line disagree")
    sems = []
    for part in ("longest", "tie"):
        sem, _form, _vals = ctx.lexicon.parse_exact(hits[0][0][part], {}, admitted_only=True)
        sems.append(sem)
    wording = ctx.skin(row["meta"]["wording_id"])
    asked = K.match_template(wording.text, question, SCHEMA)
    for k, v in list(told.items()) + list(asked.items()):
        if k == "UA" and v != crawler:
            raise ParseError(f"token reads {v!r} in the text but {crawler!r} in the request")
    view = {"groups": groups, "crawler": crawler, "url": url, "path": path, "status": status,
            "longest_rule": sems[0], "tie_rule": sems[1], "qform": wording.qform}
    if skin.author_mode == "T":
        view.update(site=told["SITE"], operator=told["OPERATOR"], purpose=told["PURPOSE"])
    if row["qtype"] == "choice":
        present = {f"{e}:{p}" for g in groups for e, p in g["lines"]}
        view["options"] = [_option_key(t, present) for t in row["options"]]
    return view


def _option_key(text: str, present: set) -> str:
    if text == NONE_OPTION:
        return "none"
    m = re.fullmatch(r"(Allow|Disallow): (\S+)", text)
    if not m:
        raise ParseError(f"option {text!r}")
    key = f"{EFFECT_WORD[m[1]]}:{m[2]}"
    if key not in present:
        raise ParseError(f"option {text!r} is not a line of the file")
    return key


# ------------------------------------------------------------------------------------------------ solver B

def _unescape(path: str) -> str:
    def one(m):
        ch = chr(int(m.group(1), 16))
        return ch if ch in UNRESERVED else m.group(0)
    return re.sub(r"%([0-9A-Fa-f]{2})", one, path)


def _compile(pattern: str) -> re.Pattern:
    end = pattern.endswith("$")
    body = pattern[:-1] if end else pattern
    return re.compile("".join(".*" if c == "*" else re.escape(c) for c in body) + (r"\Z" if end else ""), re.S)


def _lines_for(groups: list, crawler: str) -> list:
    me = crawler.casefold()
    own = [g for g in groups if any(a != "*" and a.casefold() == me for a in g["agents"])]
    if own:
        return [ln for g in own for ln in g["lines"]]
    return [ln for g in groups if "*" in g["agents"] for ln in g["lines"]]


def _beats(cand: tuple, best) -> bool:
    """The explicit pairwise rule on (length, effect, pattern): a longer pattern wins; at equal length an Allow line
    beats a Disallow line; anything else keeps the current best."""
    if best is None or cand[0] > best[0]:
        return True
    return cand[0] == best[0] and cand[1] == "allow" and best[1] == "disallow"


def _decider(view: dict):
    """(may fetch, deciding line or None) by brute force over every applying line."""
    if (view["longest_rule"], view["tie_rule"]) != WANT_SEMS:
        raise ParseError("the card states precedence sentences this solver does not know")
    rule = STATUS_RULE["200" if view["status"] is None else view["status"]]
    if rule == "fetch_all":
        return True, "status"
    if rule == "fetch_none":
        return False, "status"
    subject = _unescape(_cut_path(view["url"]))
    best, rivals = None, []
    for eff, pat in _lines_for(view["groups"], view["crawler"]):
        if not _compile(pat).match(subject):
            continue
        cand = (len(pat), eff, pat)
        if _beats(cand, best):
            best, rivals = cand, []
        elif cand[0] == best[0] and eff == best[1]:
            rivals.append(cand)
    if best is None:
        return True, None
    return best[1] == "allow", (best, rivals)


def solve_b(view: dict):
    ok, how = _decider(view)
    if view["qform"] in QUESTION:
        return QUESTION[view["qform"]](ok)
    if view["qform"] != "ch_line":
        raise ParseError(f"unknown question form {view['qform']!r}")
    if how == "status":
        raise ParseError("a line question on a row whose fetch status decides")
    if how is None:
        return "none"
    best, rivals = how
    if rivals:
        raise ParseError("two lines of the winning effect share the longest length")
    return f"{best[1]}:{best[2]}"
