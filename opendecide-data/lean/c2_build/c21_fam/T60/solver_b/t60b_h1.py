"""T60 solver B, head H1 DELEGATE-OR-DO (G0_LITE section 3.2, ROW_SCHEMA H1). String side: parse the card numbers and the brief out of the
rendered row, then apply the four-predicate rule.

DELEGATE iff SIZE (steps >= S or read tokens >= V) and BRIEF (needs <= B) and BOUND (result <= R) and FREE (no written path occurs in a
pending main step's reads or writes [SHARED], no file the subtask reads is a path a pending main step writes [FED], and the incoming list is none).
Paths are compared after collapsing ./ and ../ segments. Otherwise DO_HERE."""
import re

try:
    from .t60b_text import ParseGap, Rx, clause, lines_of, norm_path, one_number, split_paths, strip_notes
except ImportError:                                                  # loaded as a top-level module from this folder
    from t60b_text import ParseGap, Rx, clause, lines_of, norm_path, one_number, split_paths, strip_notes

_RE_PENDING = Rx(r"^-\s*(m\d+):\s*reads\s+(.*?);\s*writes\s+(.*)$")
_RE_FACT = Rx(r"^-\s*the\s+(\S+)\s+is\s+(.*)$")
_RE_STEP = Rx(r"^\s+(\d+)\.\s+(.*\S)\s*$")
_RE_FILE = Rx(r"^-\s*reads\s+(.+?)\s+\((\d+)\s+tokens?\)\s*$")
_RE_RESULT = Rx(r"^-\s*returns\s+.*\((\d+)\s+tokens?\)\s*$")
_RE_NEED = Rx(r"^-\s*needs from the main thread:\s*(.*)$")
_RE_WRITES = Rx(r"^-\s*writes:\s*(.*)$")
_RE_INCOMING = Rx(r"^-\s*input from pending main steps:\s*(.*)$")


def parse_card(card_text):
    t = " ".join(card_text.split())
    first = clause(t, "First", "Second")
    second = clause(t, "Second", "Third")
    third = clause(t, "Third", "Fourth")
    return {
        "S": one_number(r"(\d+)\s+(?:or more\s+)?steps", first, "S"),
        "V": one_number(r"(\d+)\s+(?:or more\s+)?tokens", first, "V"),
        "B": one_number(r"(\d+)\s+(?:or fewer\s+)?facts", second, "B"),
        "R": one_number(r"(\d+)\s+(?:or fewer\s+)?tokens", third, "R"),
    }


def parse(context):
    ls = strip_notes(lines_of(context))
    try:
        i_facts = next(i for i, ln in enumerate(ls) if ln.strip() == "Main thread facts:")
        i_pend = next(i for i, ln in enumerate(ls) if ln.strip() == "Main thread pending steps:")
        i_cand = next(i for i, ln in enumerate(ls) if ln.strip().startswith("Candidate subtask"))
    except StopIteration:
        raise ParseGap("h1_sections_missing")
    if not (i_facts < i_pend < i_cand):
        raise ParseGap("h1_sections_order")
    card = parse_card("\n".join(ls[:i_facts]))
    facts = []
    for ln in ls[i_facts + 1:i_pend]:
        if not ln.strip():
            continue
        m = _RE_FACT.match(ln)
        if not m:
            raise ParseGap("h1_fact_line")
        facts.append((m.group(1), m.group(2)))
    pending = []
    for ln in ls[i_pend + 1:i_cand]:
        if not ln.strip():
            continue
        m = _RE_PENDING.match(ln)
        if not m:
            raise ParseGap("h1_pending_line")
        pending.append({"id": m.group(1), "reads": split_paths(m.group(2)), "writes": split_paths(m.group(3))})
    steps, files, result, needs, writes, incoming = [], [], None, None, None, None
    for ln in ls[i_cand + 1:]:
        if not ln.strip() or ln.strip() == "- steps:":
            continue
        m = _RE_STEP.match(ln)
        if m:
            steps.append(m.group(2))
            continue
        m = _RE_FILE.match(ln)
        if m:
            files.append((m.group(1), int(m.group(2))))
            continue
        m = _RE_RESULT.match(ln)
        if m:
            result = int(m.group(1))
            continue
        m = _RE_NEED.match(ln)
        if m:
            needs = split_paths(m.group(1))
            needs = [re.sub(r"^the\s+", "", n) for n in needs]
            continue
        m = _RE_WRITES.match(ln)
        if m:
            writes = split_paths(m.group(1))
            continue
        m = _RE_INCOMING.match(ln)
        if m:
            incoming = split_paths(m.group(1))
            continue
        raise ParseGap("h1_brief_line")
    if result is None or needs is None or writes is None or incoming is None:
        raise ParseGap("h1_brief_field_missing")
    return {"card": card, "facts": facts, "pending": pending, "steps": steps, "files": files, "result": result, "needs": needs,
            "writes": writes, "incoming": incoming}


def predicates(p):
    c = p["card"]
    read_tokens = sum(t for _, t in p["files"])                    # every `- reads` line counts, a fed file included
    size = len(p["steps"]) >= c["S"] or read_tokens >= c["V"]
    brief = len(p["needs"]) <= c["B"]
    bound = p["result"] <= c["R"]
    touched, produced = set(), set()
    for m in p["pending"]:
        touched.update(norm_path(x) for x in m["reads"])
        touched.update(norm_path(x) for x in m["writes"])
        produced.update(norm_path(x) for x in m["writes"])
    # paths are compared after collapsing ./ and ../ segments (norm_path)
    shared = any(norm_path(w) in touched for w in p["writes"])                  # SHARED: a subtask write is read or written by a pending main step
    fed = any(norm_path(f) in produced for f, _t in p["files"])                 # FED: a subtask read is what a pending main step still has to WRITE
    free = (not shared) and (not fed) and not p["incoming"]
    return {"size": size, "brief": brief, "bound": bound, "free": free, "shared_write": shared, "fed": fed, "pending_dep": bool(p["incoming"])}


def decide(p):
    pr = predicates(p)
    return "DELEGATE" if (pr["size"] and pr["brief"] and pr["bound"] and pr["free"]) else "DO_HERE"


def solve(context):
    p = parse(context)
    return decide(p), p
