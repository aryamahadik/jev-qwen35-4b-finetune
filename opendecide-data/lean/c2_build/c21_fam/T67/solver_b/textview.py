"""Splits the rendered context into its blocks and reads each one back into plain fields (card, session notes, table card, user turn, artifact) and reads the
lettered options. Pure string work."""
import re


class Unparsable(Exception):
    pass


def _blocks(lines):
    """Index lines into paragraphs separated by blank lines, but keep the artifact (which starts at 'Proposed ...') as one tail."""
    out, cur = [], []
    for ln in lines:
        if ln.strip() == "":
            if cur:
                out.append(cur)
                cur = []
        else:
            cur.append(ln)
    if cur:
        out.append(cur)
    return out


def split_context(ctx):
    """-> dict(card=[lines], session=[lines]|None, table=[lines]|None, user=[lines], artifact_head=str, artifact_label=str, artifact=str)."""
    if not ctx:
        raise Unparsable("empty context")
    m = re.search(r"^Proposed (call|write): (.*)$", ctx, re.M)
    if not m:
        raise Unparsable("no proposed call")
    head_end = m.start()
    before, after = ctx[:head_end], ctx[head_end:]
    paras = _blocks(before.split("\n"))
    out = dict(card=None, session=None, table=None, user=None)
    for p in paras:
        first = p[0]
        if first.startswith("Policy card "):
            out["card"] = p
        elif first.startswith("Session notes"):
            out["session"] = p
        elif first.startswith("Table card"):
            out["table"] = p
        elif first.startswith("User:"):
            out["user"] = p
    if out["card"] is None or out["user"] is None:
        raise Unparsable("missing card or user turn")
    alines = after.split("\n")
    out["artifact_head"] = alines[0]
    out["artifact_label"] = alines[1] if len(alines) > 1 else ""
    out["artifact"] = "\n".join(alines[2:])
    out["call"] = m.group(2)
    out["call_kind"] = m.group(1)
    return out


def _csv(v):
    v = v.strip()
    if v in ("", "none"):
        return []
    return [x.strip() for x in v.split(",") if x.strip()]


def parse_card(lines):
    card = dict(name=lines[0][len("Policy card "):], lists={}, ask_on_soft=False, checksum_required=None, tag_ok=False, lock_review=False)
    for ln in lines[1:]:
        if ln.startswith("tags from trusted sources are acceptable"):
            card["tag_ok"] = True
            continue
        if ": " not in ln:
            continue
        k, v = ln.split(": ", 1)
        if k == "soft blocks are raised to ASK":
            card["ask_on_soft"] = v.strip().lower() == "yes"
        elif k == "fetched scripts need a checksum":
            card["checksum_required"] = v.strip().lower() == "yes"
        elif k == "migration lock review":
            card["lock_review"] = v.strip().lower() == "on"
        else:
            card["lists"][k] = _csv(v)
    return card


def lane_of(card, name):
    """Which lane list of the card holds `name` -> "contained" | "shared" | "production" | None."""
    for lane in ("contained", "shared", "production"):
        for key in ("%s contexts" % lane, "%s databases" % lane):
            if name in card["lists"].get(key, ()):
                return lane
    return None


def lane_for(card, name, env_lane):
    """Lane of the workspace / context / database: from the card lists; the `Environment:` line of the user turn, when present, must agree with it
    (a conflict is a renderer defect and B abstains); the line alone is used when the name is in no list."""
    lane = lane_of(card, name)
    if lane is not None and env_lane is not None and lane != env_lane:
        raise Unparsable("lane conflict between the card lists and the Environment line")
    lane = lane or env_lane
    if lane is None:
        raise Unparsable("lane of %s" % "the workspace")
    return lane


def parse_session(lines):
    """Session notes -> dict(created=[...], already={context: [...]}, not_yet={context: [...]}, required=[(job, path)], failed={job}, has_objects, has_required)."""
    out = dict(created=[], already={}, not_yet={}, required=[], failed=set(), has_objects=False, has_required=False)
    if not lines:
        return out
    for ln in lines[1:]:
        if ln.startswith("created by the agent this session:"):
            out["created"] = _csv(ln.split(":", 1)[1])
            continue
        m = re.match(r"^objects already in (\S+): (.*)$", ln)
        if m:
            out["already"][m.group(1)] = _csv(m.group(2))
            out["has_objects"] = True
            continue
        m = re.match(r"^objects not yet in (\S+): (.*)$", ln)
        if m:
            out["not_yet"][m.group(1)] = _csv(m.group(2))
            out["has_objects"] = True
            continue
        if ln.startswith("required checks:"):
            out["has_required"] = True
            for item in _csv(ln.split(":", 1)[1]):
                mm = re.match(r"^(\S+) \(in (\S+)\)$", item)
                if not mm:
                    raise Unparsable("required check without its workflow path")
                out["required"].append((mm.group(1), mm.group(2)))
            continue
        m = re.match(r"^last run of (\S+): failed$", ln)
        if m:
            out["failed"].add(m.group(1))
    return out


def parse_table(lines):
    out = dict(table=None, rows=None, backup=None)
    if not lines:
        return out
    for ln in lines[1:]:
        if ln.startswith("table:"):
            out["table"] = ln.split(":", 1)[1].strip()
        elif ln.startswith("approximate rows:"):
            digits = re.sub(r"[^0-9]", "", ln.split(":", 1)[1])
            out["rows"] = int(digits) if digits else None
        elif ln.startswith("backup:"):
            out["backup"] = ln.split(":", 1)[1].strip().lower() == "yes"
    return out


def parse_user(lines):
    """-> (text, env_lane): the user turn without the Environment line, and the lane named there (or None)."""
    env = None
    body = []
    for i, ln in enumerate(lines):
        if i == 0:
            ln = ln[len("User:"):].strip()
        m = re.match(r"^Environment:\s*(\w+)\.?\s*$", ln)
        if m:
            env = m.group(1).lower()
            continue
        body.append(ln)
    if env == "dev":
        env = "contained"
    return "\n".join(body), env


def _label(t):
    return t.split(":", 1)[0].strip() if ": " in t else t.strip()


def option_table(rendered, options):
    """-> {letter: label}. The lettered lines of the RENDERED options text are the source; the structured `options` list of the b-view is used only as a
    cross-check (a mismatch between the two is unparsable) or, when the rendered text carries no lettered line, as the source."""
    from_text = {}
    for ln in (rendered.get("options_text") or "").split("\n"):
        m = re.match(r"^([A-Z])\) (.*)$", ln)
        if m:
            from_text[m.group(1)] = _label(m.group(2))
    from_list = {o["letter"]: _label(o["text"]) for o in (options or ())}
    if from_text and from_list and from_text != from_list:
        raise Unparsable("rendered options and option list differ")
    return from_text or from_list


def mentions(text, phrase):
    return re.search(r"(?<![A-Za-z])%s(?![A-Za-z])" % re.escape(phrase), text, re.I) is not None


def names_target(text, target):
    if not target:
        return False
    return re.search(r"(?<![A-Za-z0-9_./#-])%s(?![A-Za-z0-9_/#-])(?!\.[A-Za-z0-9])" % re.escape(target), text) is not None
