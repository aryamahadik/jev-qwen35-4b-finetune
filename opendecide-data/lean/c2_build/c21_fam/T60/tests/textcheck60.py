"""BUILD-SKEPTIC cross-check (not solver B): recompute the T60 label from the RENDERED TEXT ONLY.

It never reads rec["scene"], t60_rule.py or t60_oracle.py: it parses `rec["rendered"]["text"]` with regular expressions written from
ROW_SCHEMA.md and applies the rules of G0-lite section 3 again. A mismatch with the stored gold means the text does not carry a fact the
gold uses (a rendering or ambiguity defect), which is exactly what solver B's K1 / K2 would drop at creation. It is a regression guard for
the generator; the real solver B stays a separate program from a separate session (G1).
"""
import posixpath
import re

ORD = ("first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth")
IRREV_PHRASES = ("cannot be undone", "reaches people outside the team", "the file was made in this session and is not tracked")


def h1(text):
    lines = text.split("\n")
    card = "\n".join(lines[:lines.index("Main thread facts:")])
    s_min = int(re.search(r"(\d+)\s+(?:or more\s+)?steps", card).group(1))
    toks = [int(x) for x in re.findall(r"(\d+)\s+(?:or more\s+|or fewer\s+)?tokens", card)]
    v_min, r_max = toks[0], toks[1]
    b_max = int(re.search(r"(\d+)\s+(?:or fewer\s+)?facts?", card).group(1))
    steps = len(re.findall(r"^  \d+\. ", text, re.M))
    volume = sum(int(x) for x in re.findall(r"^- reads \S+ \((\d+) tokens\)", text, re.M))
    result = int(re.search(r"^- returns a summary of the findings \((\d+) tokens\)", text, re.M).group(1))
    needs = re.search(r"^- needs from the main thread: (.*)$", text, re.M).group(1)
    n_needs = 0 if needs.strip() == "nothing" else len(needs.split(", "))
    writes = {posixpath.normpath(x) for x in re.search(r"^- writes: (.*)$", text, re.M).group(1).split(", ")}
    incoming = re.search(r"^- input from pending main steps: (.*)$", text, re.M).group(1).strip()
    touched, pend_writes = set(), set()
    for m in re.finditer(r"^- (m\d+): reads (.*?); writes (.*)$", text, re.M):
        touched |= {posixpath.normpath(x) for x in m.group(2).split(", ")} | {posixpath.normpath(x) for x in m.group(3).split(", ")}
        pend_writes |= {posixpath.normpath(x) for x in m.group(3).split(", ")}
    files = [posixpath.normpath(x) for x in re.findall(r"^- reads (\S+) \(\d+ tokens\)", text, re.M)]
    fed = incoming != "none" or any(f in pend_writes for f in files)                       # an explicit pending feed, or a file a pending step still writes
    ok = (steps >= s_min or volume >= v_min) and n_needs <= b_max and result <= r_max and not (writes & touched) and not fed
    return "DELEGATE" if ok else "DO_HERE"


def h3(text):
    lines = text.split("\n")
    card = "\n".join(lines[:lines.index("Order given in the request:")])
    high = int(re.search(r"changes (\d+) or more", card).group(1))
    n_min = int(re.search(r"(\d+)\s+(?:or more\s+)?steps", card).group(1))
    seg_order = text[text.index("Order given in the request:"):text.index("Steps:")]
    stated = []
    for m in re.finditer(r"[Ss]tep (s\d+) has to come before step (s\d+)|[Dd]o step (s\d+) before step (s\d+)", seg_order):
        g = m.groups()
        stated.append((g[0] or g[2], g[1] or g[3]))
    seg_steps = text[text.index("Steps:"):text.index("Data flow")]
    steps = re.findall(r"^- (s\d+): .* \(changes (\d+) \S+; (.*)\)$", seg_steps, re.M)
    if "the steps are numbered in the order in which they are to be carried out" in seg_order:           # a numbered list states the order as listed
        ids = [x[0] for x in steps]
        stated = [(ids[i], ids[i + 1]) for i in range(len(ids) - 1)]
    seg_flow = text[text.index("Data flow"):text.index("\n\nQuestion:")]
    edges = [(a, b) for b, a in re.findall(r"^- (s\d+) uses (?:a value derived from )?the output of (s\d+)", seg_flow, re.M)]

    def irrev(mag, eff):
        if int(mag) >= high or any(p in eff for p in IRREV_PHRASES):
            return True
        w = re.search(r"can be undone for (\d+) more days", eff)
        if w:                                              # a window that expires before the step runs is no undo path
            d = re.search(r"the step runs in (\d+) days", eff)
            return int(w.group(1)) - (int(d.group(1)) if d else 0) < 1
        return False

    r1 = any(irrev(mag, eff) for _sid, mag, eff in steps)
    r2 = len(steps) >= n_min
    reach = set(stated)
    changed = True
    while changed:
        changed = False
        for (a, b) in list(reach):
            for (c, d) in list(reach):
                if b == c and (a, d) not in reach:
                    reach.add((a, d))
                    changed = True
    r3 = any(e not in reach for e in edges)
    return "PLAN" if (r1 and r2 and r3) else "ACT"


def h2(text):
    head = text.split("Remaining plan:")[0]
    counts_recovery = not re.search(r"do not count|does not count", head)
    plan_seg = text.split("Remaining plan:\n")[1].split("Context transcript:")[0]
    steps = {}
    for line in plan_seg.strip().split("\n"):
        m = re.match(r"\[(done|todo)\] step (\d+)(?: \(only if step (\d+) fails\))?: (\w+) the (\w+)(?: using (.*))?$", line)
        assert m, line
        status, k, host, _verb, _ent, refs = m.groups()
        steps[k] = dict(status=status, host=host, refs=refs.split(" and ") if refs else [])
    tr = text.split("Context transcript:\n")[1].split("\n\nQuestion:")[0]
    tr = re.split(r"\n(?:The f|F)act in question", tr)[0]
    events, cur = [], None
    for line in tr.split("\n"):
        m = re.match(r"\((\d+)\) (.*)$", line)
        if m:
            cur = [int(m.group(1)), m.group(2), []]
            events.append(cur)
        else:
            cur[2].append(line.strip())
    facts = []
    for n, first, rest in events:
        if first.startswith("User: As a reminder"):
            continue
        m = re.match(r"User: The (\w+) for the (\w+) is (.*?)\.(?: \(.*\))?$", first)
        if m:
            facts.append(dict(type="V", handle=m.group(1), entity=m.group(2), value=m.group(3), turn=n))
            continue
        m = re.match(r"User: Let us go with (.*?) as the (\w+) of the (\w+)(?: \(.*\))?\.$", first)
        if m:
            facts.append(dict(type="D", handle=m.group(2), entity=m.group(3), value=m.group(1), turn=n))
            continue
        m = re.match(r"Agent called (\w+?)_(\w+)\((.*)\)$", first)
        assert m, first
        verb, ent, args = m.groups()
        if verb == "check":
            continue
        out = [x for x in rest if x != "-> output:"]
        key, val = out[0].split(": ", 1)
        val = re.sub(r" \(a \w+ value\)$", "", val)
        if verb == "get":
            facts.append(dict(type="R", handle=key, entity=ent, value=val, turn=n))
        elif verb == "create":
            facts.append(dict(type="S", handle=key, entity=ent, value=val, turn=n))
        elif verb == "export":
            facts.append(dict(type="P", handle="path", entity=ent, value=val, turn=n))
        elif verb == "read":
            facts.append(dict(type="C", handle=key, entity=ent, value=val, turn=n, art=re.search(r'source="(.*)"', args).group(1)))
    qline = [x for x in text.split("\n\nQuestion:")[0].split("\n") if "act in question" in x][-1]
    qturn = int(re.search(r"\(turn (\d+),", qline).group(1))
    target = [f for f in facts if f["turn"] == qturn][0]

    def current(f):
        later = [x for x in facts if (x["handle"], x["entity"], x["type"], x.get("art")) == (f["handle"], f["entity"], f["type"], f.get("art"))
                 and x["turn"] > f["turn"]]
        return later[-1] if later else f

    gets = [f for f in facts if f["type"] == "R"]
    role_desc = ((r"the value given for the (\w+)", "V"), (r"the value returned for the (\w+)", "R"), (r"the value we agreed for the (\w+)", "D"),
                 (r"the key recorded for the (\w+)", "S"), (r"the saved location for the (\w+)", "P"))

    def lookup(ref):
        for pat, t in role_desc:                          # L2
            m = re.fullmatch(pat, ref)
            if m:
                c = [f for f in facts if f["entity"] == m.group(1) and f["type"] == t]
                return [current(c[-1])] if c else []
        m = re.fullmatch(r"the (\w+) record fetched by a get call", ref)       # L3: get_<entity> calls only
        if m:
            k = ORD.index(m.group(1))
            return [current(gets[k])] if k < len(gets) else []
        m = re.fullmatch(r"the saved location of the (\w+) snapshot", ref)      # L4 pointer
        if m:
            c = [f for f in facts if f["entity"] == m.group(1) and f["type"] == "P"]
            return [c[-1]] if c else []
        m = re.fullmatch(r"the value derived in step s?(\d+)", ref)             # L4 chain
        if m:
            return ("via", m.group(1))
        m = re.fullmatch(r"the (\w+)", ref)                                      # L1 handle
        c = [f for f in facts if f["handle"] == m.group(1) and f["type"] != "C"]
        return [current(c[-1])] if c else []

    def takes(step):
        out = []
        for r in step["refs"]:
            x = lookup(r)
            if isinstance(x, tuple):
                if steps[x[1]]["status"] == "todo":
                    out += takes(steps[x[1]])
            else:
                out += x
        return out

    if current(target) is not target:
        return "DROP"
    for _k, s in steps.items():
        if s["status"] != "todo":
            continue
        if s["host"] is not None and not (counts_recovery and steps[s["host"]]["status"] == "todo"):
            continue
        if any(f is target for f in takes(s)):
            return "KEEP"
    return "DROP"


def recompute(rec):
    text = rec["rendered"]["text"]
    return {"h1": h1, "h2": h2, "h3": h3}[rec["hd"]](text)
