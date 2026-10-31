"""T59 solver B, part 1: a deterministic STRING-SIDE parser of the RENDERED row (context, question, options).

It recovers, from the text only: the policy-card slots (mode, stakes threshold H and unit, defaults, read-first, retry cap, precedence),
the tool list (verb, noun, parameters with optionality and declared defaults, read/write, idempotent, exposure, undo window, key, authority),
the repo environment line, the user turns (request, stated values, option lists, delegation, qualifier, cap statement, notes, prerequisite,
tree state, candidate lists), the call history with outputs, and the planned next step.
No file is read at run time, nothing in the text is executed, no model is called (G1). Stdlib only.

Everything the label needs is a FACT recovered here; the decision itself is in rules.py (G0-lite section 3.2).
"""
import re

VERBS_READ = ("get", "list", "find", "lookup", "check", "read")
VERBS_CREATE = ("create", "add")
# action phrases that may appear in a request (the closed list of the G0-lite verb names); longest first
REQ_VERBS = ("set the status of", "delete", "remove", "archive", "cancel", "send", "export", "move", "reserve", "schedule", "rename",
             "create", "add", "update", "restore", "release", "lock", "get", "list")
REQ_VERB_TOOL = {"set the status of": "set"}

CALL_RE = re.compile(r"^(?P<name>[a-z][a-z0-9]*_[a-z0-9_]*)\((?P<args>.*)\)$")
ARG_RE = re.compile(r'(\w+)="([^"]*)"')
ID_RE = re.compile(r"[a-z]{2,4}-\d+")
PATH_RE = re.compile(r"/[^\s,()]*[^\s.,()?]")


# ----------------------------------------------------------------------------------------------------------------------
# small value classes
# ----------------------------------------------------------------------------------------------------------------------
class Tool(object):
    __slots__ = ("name", "verb", "noun", "params", "access", "idempotent", "desc", "external", "internal", "undo_window", "authoritative",
                 "accepts_key", "role_params")

    def __init__(self):
        self.params = []
        self.undo_window = None
        self.external = False
        self.internal = False
        self.authoritative = False
        self.accepts_key = False
        self.idempotent = False

    def sig(self):
        """Parameter signature used for the 'same schema' test (name, type, optional)."""
        return tuple((p["name"], p["type"], p["optional"]) for p in self.params)


class Call(object):
    __slots__ = ("raw", "kind", "name", "verb", "noun", "args", "prog", "paths", "count", "out_lines", "out", "has_output")

    def __init__(self, raw):
        self.raw = raw
        self.kind = None          # 'tool' | 'shell'
        self.name = None
        self.verb = None
        self.noun = None
        self.args = {}
        self.prog = None
        self.paths = []
        self.count = None         # the '(N files)' suffix of a repo step
        self.out_lines = []
        self.out = {}
        self.has_output = False


class Facts(object):
    def __init__(self):
        self.world = None
        self.card = {"mode": None, "H": None, "unit": None, "defaults": None, "read_first": None, "retry": None, "prec": None,
                     "prec_cap": None, "title": None}
        self.tools = {}
        self.shell = {"read": [], "write": []}
        self.users = []
        self.user_lists = []       # list-entry lines (the user's candidate list)
        self.history = []
        self.planned = None
        self.planned_raw = None
        self.request = {}
        self.values = {}           # role -> stated value (user value lines)
        self.value_roles_order = []
        self.cands = {}            # role -> [candidates]
        self.deleg = []            # delegation roles (as written)
        self.qual = None           # ('one', field, q) | ('both', fa, fb, q)
        self.cap = None            # {'price':, 'cap':}
        self.notes = []            # [(fact, value)]
        self.prereq = None         # ('lock', parent, pid) | ('mkdir', path)
        self.tree = None           # 'clean' | 'untracked'
        self.expect = False        # "there should be just one X for that"
        self.size = None           # 'It holds N <unit>s.'
        self.unknown_user = []
        self.errors = []           # parse problems (strings); a non-empty list may force an abstain


# ----------------------------------------------------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------------------------------------------------
def _clean_tok(s):
    return s.strip().rstrip(".,;?!").strip()


def parse_call(raw):
    """A planned step or a history call, tool style `name(arg="v", ...)` or shell style `prog a b (N files)`."""
    c = Call(raw)
    s = raw.strip()
    m = CALL_RE.match(s)
    if m:
        c.kind = "tool"
        c.name = m.group("name")
        c.verb, c.noun = c.name.split("_", 1)
        c.args = dict(ARG_RE.findall(m.group("args")))
        return c
    m = re.match(r"^(.*?)\s*\((\d+) files?\)$", s)
    if m:
        c.count = int(m.group(2))
        s = m.group(1)
    toks = s.split()
    if toks:
        c.kind = "shell"
        c.prog = toks[0]
        c.paths = [t for t in toks[1:] if t.startswith("/")]
        c.verb = toks[0]
        c.name = toks[0]
        if toks[0] == "git":
            c.verb = "git"
    return c


def _parse_output_line(c, line):
    t = line.strip()
    c.out_lines.append(t)
    m = re.match(r"^(?:items|files)\[(\d+)\]:\s*(.*)$", t)
    if m:
        ent = {}
        for part in m.group(2).split(", "):
            if "=" in part:
                k, v = part.split("=", 1)
                ent[k.strip()] = v.strip()
        c.out.setdefault("entities", []).append(ent)
        return
    m = re.match(r"^(\w+):\s*(.*)$", t)
    if m:
        c.out[m.group(1)] = m.group(2)


# ----------------------------------------------------------------------------------------------------------------------
# card
# ----------------------------------------------------------------------------------------------------------------------
def _card_line(f, line):
    low = line.lower()
    card = f.card
    m = re.match(r"^(?:policy card|card) (\S+?)\.$", line, re.I)
    if m:
        card["title"] = m.group(1)
        return True
    if "proceed with the most likely value" in low:
        card["mode"] = "ON"
        return True
    if re.match(r"^ask (?:when|whenever) a required value", low):
        card["mode"] = "OFF"
        return True
    m = re.search(r"(\d+) or more (\S+) (?:counts as|is high)", line)
    if m:
        card["H"] = int(m.group(1))
        card["unit"] = m.group(2)
        return True
    if "default" in low and "tool schema" in low:
        card["defaults"] = not re.search(r"not count|does not|doesn't", low)
        return True
    if "read-only call" in low:
        off = re.search(r"not required|does not require|need not|no need", low)
        card["read_first"] = not off
        return True
    m = re.search(r"(?:up to|at most) (\d+) times", low)
    if m:
        card["retry"] = int(m.group(1))
        return True
    if re.search(r"disagree|different values|cannot both hold", low):
        return _precedence(f, line)
    return False


SRC_NAMES = (("the user's message", "user"), ("the tool result", "tool"), ("the project notes", "notes"))


def _src(s):
    s = s.strip().lower()
    for nm, k in SRC_NAMES:
        if s == nm or s.endswith(nm):
            return k
    return None


def _precedence(f, line):
    low = line.lower().rstrip(".")
    if "requested amount" in low and "stated cap" in low:
        m = re.search(r"the (amount|cap) wins$", low)
        if m:
            f.card["prec_cap"] = m.group(1)
            return True
        return False
    m = re.match(r"^when (.+?) and (.+?) disagree, (.+?) wins$", low)
    if m:
        a, b, w = _src(m.group(1)), _src(m.group(2)), _src(m.group(3))
        if a and b and w:
            f.card["prec"] = (w, b if w == a else a)
            return True
    m = re.match(r"^if (.+?) and (.+?) give different values, take the one from (.+?)$", low)
    if m:
        a, b, w = _src(m.group(1)), _src(m.group(2)), _src(m.group(3))
        if a and b and w:
            f.card["prec"] = (w, b if w == a else a)
            return True
    return False


# ----------------------------------------------------------------------------------------------------------------------
# tools
# ----------------------------------------------------------------------------------------------------------------------
TOOL_RE = re.compile(r"^- (?P<name>[a-z][a-z0-9]*_[a-z0-9_]*)\((?P<params>.*?)\)\s*\[(?P<flags>[^\]]*)\]\s*--\s*(?P<desc>.*)$")
PARAM_RE = re.compile(r"^(?P<n>\w+):\s*(?P<t>\w+)(?P<opt>\?)?(?:\s*=\s*(?P<d>.+))?$")


def _tool_line(f, line):
    m = TOOL_RE.match(line)
    if not m:
        return False
    t = Tool()
    t.name = m.group("name")
    t.verb, t.noun = t.name.split("_", 1)
    for part in re.split(r",\s*", m.group("params")):
        part = part.strip()
        if not part:
            continue
        pm = PARAM_RE.match(part)
        if not pm:
            f.errors.append("tool_param")
            continue
        t.params.append({"name": pm.group("n"), "type": pm.group("t"), "optional": bool(pm.group("opt")),
                         "default": pm.group("d").strip() if pm.group("d") else None})
    flags = [x.strip() for x in m.group("flags").split(",")]
    t.access = "read" if "read" in flags else "write"
    t.idempotent = "idempotent" in flags
    t.desc = m.group("desc")
    d = t.desc
    t.external = bool(re.search(r"outside (?:of )?the (?:team|thread)", d))
    t.internal = bool(re.search(r"inside the team only", d))
    w = re.search(r"Works within (\d+) days? of the change", d) or re.search(r"\b(\d+) days?\b", d)
    t.undo_window = int(w.group(1)) if w else None
    t.authoritative = "authoritative" in d.lower()
    t.accepts_key = bool(re.search(r"Accepts a key", d)) or any(p["name"] == "key" for p in t.params)
    f.tools[t.name] = t
    return True


def _shell_line(f, line):
    m = re.match(r"^Shell: one command per step\. Read-only: (.*?)\. Write: (.*?)\.$", line)
    if not m:
        return False
    f.shell["read"] = [x.strip() for x in m.group(1).split(",")]
    f.shell["write"] = [x.strip() for x in m.group(2).split(",")]
    return True


# ----------------------------------------------------------------------------------------------------------------------
# user turns
# ----------------------------------------------------------------------------------------------------------------------
def _user_request(f, text):
    """Recover the request from the first user line (alarm / wrapper sentences before or after are ignored)."""
    r = {"raw": text}
    vp = "|".join(re.escape(v) for v in REQ_VERBS)
    # amount form: 'reserve 7 units of the X id'
    m = re.search(r"\b(?P<v>%s)\b (?P<n>\d+) (?P<u>\w+) of the (?P<e>\w+) (?P<ref>[a-z]{2,4}-\d+)" % vp, text, re.I)
    if m:
        r.update(form="cap", verb=m.group("v").lower(), amount=int(m.group("n")), unit=m.group("u"), noun=m.group("e"), ref=m.group("ref"))
        return r
    m = re.search(r"\b(?P<v>%s)\b (?:the status of )?(?:the )(?P<e>\w+) whose (?P<f>\w+) is (?P<q>[^\s,.?]+)" % vp, text, re.I)
    if m:
        r.update(form="field", verb=m.group("v").lower(), noun=m.group("e"), field=m.group("f"), q=m.group("q"))
        return r
    m = re.search(r"\b(?P<v>%s)\b (?:the status of )?(?:the )(?P<e>\w+) for (?P<q>[^\s,.?]+)" % vp, text, re.I)
    if m:
        r.update(form="for", verb=m.group("v").lower(), noun=m.group("e"), q=m.group("q"))
        return r
    m = re.search(r"\b(?P<v>%s)\b (?:the status of )?(?:the )(?P<e>\w+) (?P<ref>[a-z]{2,4}-\d+)(?: \(.*?\))? (?:to the right (?P<fact>\w+)|using the correct (?P<fact2>\w+)|to (?P<val>[^\s,?]+?))(?:[.,?]|$|\s)" % vp, text, re.I)
    if m:
        fact = m.group("fact") or m.group("fact2")
        if fact:
            r.update(form="fact_ask", verb=m.group("v").lower(), noun=m.group("e"), ref=m.group("ref"), fact=fact)
        else:
            r.update(form="fact", verb=m.group("v").lower(), noun=m.group("e"), ref=m.group("ref"), value=m.group("val"))
        return r
    m = re.search(r"\b(?P<v>%s)\b (?:the status of )?(?:the )(?P<e>\w+) (?P<ref>[a-z]{2,4}-\d+)" % vp, text, re.I)
    if m:
        r.update(form="plain", verb=m.group("v").lower(), noun=m.group("e"), ref=m.group("ref"))
        hm = re.search(r"\((\d+) \w+ in it\)|\(it holds (\d+) \w+\)", text)
        if hm:
            r["size"] = int(hm.group(1) or hm.group(2))
        return r
    m = re.search(r"\b(?P<v>%s)\b (?:the )?(?P<e>file) (?P<p>/[^\s,?]*[^\s.,?])" % vp, text, re.I)
    if m:
        r.update(form="path", verb=m.group("v").lower(), noun=m.group("e"), ref=m.group("p"))
        return r
    m = re.search(r"\b(?P<v>%s)\b (?:the )?(?P<e>file) for (?P<q>[^\s,.?]+)" % vp, text, re.I)
    if m:
        r.update(form="for", verb=m.group("v").lower(), noun=m.group("e"), q=m.group("q"))
        return r
    return None


def _user_line(f, text, first):
    t = text.strip()
    low = t.lower()
    if first and not f.request:
        req = _user_request(f, t)
        if req:
            f.request = req
            # a request line may also carry the hold count and nothing else of interest
            return
    # a request line is the first user line; wrapper sentences/alarms are part of it
    m = re.match(r"^it (?:holds|has) (\d+) (\S+?)\.?$", t, re.I)
    if m:
        f.size = int(m.group(1))
        return
    if re.match(r"^the working tree is clean", low):
        f.tree = "clean"
        return
    if re.match(r"^these files were created in this session", low):
        f.tree = "untracked"
        return
    m = re.match(r"^the archive directory (\S+) has to be created first\.?$", t, re.I)
    if m:
        f.prereq = ("mkdir", m.group(1).rstrip("."))
        return
    m = re.match(r"^the (\w+)(?: ([a-z]{2,4}-\d+))? has to be locked first\.?$", t, re.I)
    if m:
        f.prereq = ("lock", m.group(1), m.group(2))
        return
    m = re.match(r"^lock the (\w+) ([a-z]{2,4}-\d+) before the change\.?$", t, re.I)
    if m:
        f.prereq = ("lock", m.group(1), m.group(2))
        return
    if re.match(r"^(?:there should be just one|i expect a single)\b", low):
        f.expect = True
        return
    m = re.match(r"^(?:here is what i have|these are the records):?$", low)
    if m:
        return
    m = re.match(r"^i mean the one whose (\w+) or whose (\w+) is (\S+?)\.?$", t, re.I)
    if m:
        f.qual = ("both", m.group(1), m.group(2), m.group(3))
        return
    m = re.match(r"^the one i mean has (\S+?) as its (\w+) or as its (\w+)\.?$", t, re.I)
    if m:
        f.qual = ("both", m.group(2), m.group(3), m.group(1))
        return
    m = re.match(r"^i mean the one whose (\w+) is (\S+?)\.?$", t, re.I)
    if m:
        f.qual = ("one", m.group(1), m.group(2))
        return
    m = re.match(r"^the one i mean has (\S+?) as its (\w+)\.?$", t, re.I)
    if m:
        f.qual = ("one", m.group(2), m.group(1))
        return
    m = re.match(r"^(?:each|every) (\S+) costs (\d+)(?:, and the total must stay within|; keep the total within) (\d+)\.?$", t, re.I)
    if m:
        f.cap = {"price": int(m.group(2)), "cap": int(m.group(3)), "unit": m.group(1)}
        return
    m = re.match(r"^(?:each|every) (\S+) takes (\d+) of capacity(?:, and the run has|; the whole run has) (\d+)(?: in all)?\.?$", t, re.I)
    if m:
        f.cap = {"price": int(m.group(2)), "cap": int(m.group(3)), "unit": m.group(1)}
        return
    m = re.match(r"^the project notes list the (\w+) as (\S+?)\.?$", t, re.I)
    if m:
        f.notes.append((m.group(1), m.group(2)))
        return
    m = re.match(r"^according to the project notes, the (\w+) is (\S+?)\.?$", t, re.I)
    if m:
        f.notes.append((m.group(1), m.group(2)))
        return
    m = re.match(r"^(?:options for the (.+?)|the (.+?) is one of): (.+?)\.?$", t, re.I)
    if m:
        role = (m.group(1) or m.group(2)).strip()
        f.cands[role] = [x.strip() for x in m.group(3).rstrip(".").split(",")]
        return
    m = re.match(r"^either one is fine for the (.+?)\.?$", t, re.I)
    if not m:
        m = re.match(r"^i am happy with either choice for the (.+?)\.?$", t, re.I)
    if m:
        f.deleg.append(m.group(1).strip())
        return
    m = re.match(r"^the (\w+) is (\S+?)\.?$", t, re.I)
    if m:
        f.values[m.group(1)] = m.group(2)
        f.value_roles_order.append(m.group(1))
        return
    m = re.match(r"^use (\S+?) as the (\w+)\.?$", t, re.I)
    if m:
        f.values[m.group(2)] = m.group(1)
        f.value_roles_order.append(m.group(2))
        return
    f.unknown_user.append(t)


def _list_entry(f, line):
    """A user candidate list entry: tool `- id (size N unit, fa X, fb Y)`; repo `- /path (fa X, fb Y)`."""
    m = re.match(r"^- (?P<id>[a-z]{2,4}-\d+) \(size (?P<size>\d+) (?P<u>\S+?), (?P<rest>.*)\)$", line)
    if m:
        ent = {"id": m.group("id"), "size": int(m.group("size"))}
        for part in m.group("rest").split(", "):
            kv = part.split(" ", 1)
            if len(kv) == 2:
                ent[kv[0]] = kv[1]
        return ent
    m = re.match(r"^- (?P<id>/\S+?) \((?P<rest>.*)\)$", line)
    if m:
        ent = {"id": m.group("id"), "size": 1}
        for part in m.group("rest").split(", "):
            kv = part.split(" ", 1)
            if len(kv) == 2:
                ent[kv[0]] = kv[1]
        return ent
    return None


# ----------------------------------------------------------------------------------------------------------------------
# the whole row
# ----------------------------------------------------------------------------------------------------------------------
def parse_context(context):
    f = Facts()
    lines = context.split("\n")
    i, n = 0, len(lines)
    # --- card + tools until 'Conversation:'
    section = "card"
    conv_start = None
    lines = [l.rstrip() for l in lines]
    for idx, line in enumerate(lines):
        if line.strip() == "Conversation:":
            conv_start = idx
            break
        if line.strip() == "Tools:":
            f.world = "tool"
            section = "tools"
            continue
        if line.strip() == "Environment:":
            f.world = "repo"
            section = "env"
            continue
        if section == "card":
            if not _card_line(f, line):
                f.errors.append("card_line")
        elif section == "tools":
            if not _tool_line(f, line):
                f.errors.append("tool_line")
        elif section == "env":
            if not _shell_line(f, line):
                f.errors.append("env_line")
    if conv_start is None:
        f.errors.append("no_conversation")
        return f
    # --- conversation
    cur = None
    first_user = True
    for line in lines[conv_start + 1:]:
        if not line.strip():
            continue
        if line.startswith("User: "):
            _user_line(f, line[6:], first_user)
            first_user = False
            f.users.append(line[6:])
            cur = None
            continue
        if line.startswith("- "):
            ent = _list_entry(f, line)
            if ent is not None:
                f.user_lists.append(ent)
            else:
                f.errors.append("list_entry")
            continue
        m = re.match(r"^Agent (?:called|ran) (.*)$", line)
        if m:
            cur = parse_call(m.group(1))
            f.history.append(cur)
            continue
        if re.match(r"^\s*-> output:\s*$", line):
            if cur is not None:
                cur.has_output = True
            continue
        if line.startswith("     ") and cur is not None:
            _parse_output_line(cur, line)
            continue
        m = re.match(r"^(?:Planned next step|The agent plans this next step):\s*(.*)$", line)
        if m:
            f.planned_raw = m.group(1)
            f.planned = parse_call(m.group(1))
            cur = None
            continue
        if re.match(r"^(?:Earlier step \d+ is done|Step \d+ finished earlier)\.?$", line):
            continue
        f.errors.append("conv_line")
    return f


# ----------------------------------------------------------------------------------------------------------------------
# options (letter recovery from the TEXT of the options)
# ----------------------------------------------------------------------------------------------------------------------
def classify_option(text):
    """-> 'ASK' | 'PROCEED' | None, from the option text only."""
    t = text.strip().lower()
    no_ask = bool(re.search(r"\bwithout (?:asking|checking|pausing)", t))
    if no_ask and re.match(r"^(?:carry on|go ahead|continue|proceed)\b", t):
        return "PROCEED"
    if re.match(r"^(?:stop|pause|halt)\b", t) and ("ask" in t or "question" in t) and not no_ask:
        return "ASK"
    # looser fall-backs
    if no_ask:
        return "PROCEED"
    if re.search(r"\bask(?:ing)? the (?:user|person|requester)\b|\bquestion to the\b", t) and not no_ask:
        return "ASK"
    return None


OPT_LINE_RE = re.compile(r"^([A-Z])\) (.*)$")


def parse_options(options_text, options=None):
    """-> {label: letter} read from the rendered option lines (the given `label` fields are never used)."""
    out = {}
    lines = [l for l in options_text.split("\n") if l.strip()]
    for l in lines:
        m = OPT_LINE_RE.match(l)
        if not m:
            return None
        lab = classify_option(m.group(2))
        if lab is None or lab in out:
            return None
        out[lab] = m.group(1)
    if set(out) != {"ASK", "PROCEED"}:
        return None
    return out
