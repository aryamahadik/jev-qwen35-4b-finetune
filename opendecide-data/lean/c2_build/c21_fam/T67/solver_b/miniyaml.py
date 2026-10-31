"""Own tokenizer / parser for the block-YAML subset that appears in rendered manifests and workflows.

Handles: documents split by a line `---`; block mappings; block sequences (`- key: value` items and `- scalar` items); single-quoted, double-quoted and plain
scalars (kept as strings unless they read as true / false / null / an integer); `{}` and `[]`; simple flow lists; anchors (`key: &name` + nested block) and
aliases (`key: *name`); full-line comments and trailing ` # ` comments. Keys are always strings (the key `on` stays "on"). No tags, no multi-line scalars.
Nothing is evaluated; the text is only tokenised.
"""
import copy
import re


class YamlGap(Exception):
    """The text uses a construct this subset parser does not handle."""


_INT = r"^-?[0-9]+$"


def _strip_trailing_comment(s):
    out, q = [], None
    i = 0
    while i < len(s):
        ch = s[i]
        if q:
            out.append(ch)
            if ch == q:
                if q == "'" and i + 1 < len(s) and s[i + 1] == "'":
                    out.append("'")
                    i += 1
                else:
                    q = None
        else:
            if ch in ("'", '"') and (not out or out[-1] in " [{,:" ):
                q = ch
                out.append(ch)
            elif ch == "#" and (not out or out[-1] == " "):
                break
            else:
                out.append(ch)
        i += 1
    return "".join(out).rstrip()


def scalar(tok):
    t = tok.strip()
    if t.startswith("'") and t.endswith("'") and len(t) >= 2:
        return t[1:-1].replace("''", "'")
    if t.startswith('"') and t.endswith('"') and len(t) >= 2:
        return t[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    if t in ("true", "True"):
        return True
    if t in ("false", "False"):
        return False
    if t in ("null", "~", "Null", ""):
        return None
    if re.match(_INT, t):
        return int(t)
    return t


def _split_flow(inner):
    parts, cur, q, depth = [], [], None, 0
    for ch in inner:
        if q:
            cur.append(ch)
            if ch == q:
                q = None
        elif ch in ("'", '"'):
            q = ch
            cur.append(ch)
        elif ch in "[{":
            depth += 1
            cur.append(ch)
        elif ch in "]}":
            depth -= 1
            cur.append(ch)
        elif ch == "," and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    if "".join(cur).strip():
        parts.append("".join(cur))
    return parts


def flow(tok):
    t = tok.strip()
    if t == "{}":
        return {}
    if t == "[]":
        return []
    if t.startswith("[") and t.endswith("]"):
        return [flow(p) for p in _split_flow(t[1:-1])]
    if t.startswith("{") and t.endswith("}"):
        d = {}
        for p in _split_flow(t[1:-1]):
            k, sep, v = p.partition(":")
            if not sep:
                raise YamlGap("flow map")
            d[str(scalar(k))] = flow(v)
        return d
    return scalar(t)


def split_key(s):
    """-> (key, rest) when `s` starts a `key: value` / `key:` mapping entry, else None."""
    if s.startswith("'"):
        i = 1
        while i < len(s):
            if s[i] == "'":
                if i + 1 < len(s) and s[i + 1] == "'":
                    i += 2
                    continue
                break
            i += 1
        else:
            return None
        key = s[1:i].replace("''", "'")
        rest = s[i + 1:]
        if rest.startswith(":") and (len(rest) == 1 or rest[1] == " "):
            return key, rest[1:].strip()
        return None
    if s.startswith(('"', "[", "{", "&", "*", "|", ">")):
        return None
    m = re.match(r"^([^\s:][^:]*?):(?:\s+(.*))?$", s)
    if not m:
        return None
    return m.group(1).strip(), (m.group(2) or "").strip()


class _P(object):
    def __init__(self, lines):
        self.lines = lines          # [(indent, text)]
        self.anchors = {}

    def block(self, i, indent):
        ind, txt = self.lines[i]
        if txt == "-" or txt.startswith("- "):
            return self.seq(i, ind)
        return self.map(i, ind)

    def seq(self, i, ind):
        out = []
        n = len(self.lines)
        while i < n and self.lines[i][0] == ind and (self.lines[i][1] == "-" or self.lines[i][1].startswith("- ")):
            txt = self.lines[i][1]
            rest = txt[1:].strip()
            if rest == "":
                if i + 1 < n and self.lines[i + 1][0] > ind:
                    val, i = self.block(i + 1, self.lines[i + 1][0])
                else:
                    val, i = None, i + 1
                out.append(val)
                continue
            sub = ind + (len(txt) - len(txt[1:].lstrip()))
            if split_key(rest) is not None and not rest.startswith(("'", '"')) or (rest.startswith("'") and split_key(rest) is not None):
                self.lines[i] = (sub, rest)
                val, i = self.map(i, sub)
                out.append(val)
            else:
                out.append(flow(rest))
                i += 1
        return out, i

    def map(self, i, ind):
        out = {}
        n = len(self.lines)
        while i < n and self.lines[i][0] == ind and not (self.lines[i][1] == "-" or self.lines[i][1].startswith("- ")):
            txt = self.lines[i][1]
            kv = split_key(txt)
            if kv is None:
                raise YamlGap("not a mapping entry")
            key, rest = kv
            anchor = None
            if rest.startswith("&"):
                anchor, _, rest = rest[1:].partition(" ")
                rest = rest.strip()
            if rest.startswith("*"):
                name = rest[1:].strip()
                if name not in self.anchors:
                    raise YamlGap("unknown alias")
                out[key] = copy.deepcopy(self.anchors[name])
                i += 1
                continue
            if rest == "":
                if i + 1 < n and (self.lines[i + 1][0] > ind or (self.lines[i + 1][0] == ind and (self.lines[i + 1][1] == "-" or self.lines[i + 1][1].startswith("- ")))):
                    val, i = self.block(i + 1, self.lines[i + 1][0])
                else:
                    val, i = None, i + 1
            else:
                val, i = flow(rest), i + 1
            if anchor:
                self.anchors[anchor] = copy.deepcopy(val)
            out[key] = val
        return out, i


def parse_documents(text):
    """-> list of parsed documents (values). Raises YamlGap on constructs outside the subset."""
    docs, cur = [], []
    for raw in text.split("\n"):
        if raw.rstrip() == "---":
            docs.append(cur)
            cur = []
            continue
        body = raw.rstrip()
        if not body.strip() or body.lstrip().startswith("#"):
            continue
        stripped = _strip_trailing_comment(body.lstrip())
        if not stripped:
            continue
        cur.append((len(body) - len(body.lstrip()), stripped))
    docs.append(cur)
    out = []
    for lines in docs:
        if not lines:
            continue
        p = _P(lines)
        val, i = p.block(0, lines[0][0])
        if i != len(lines):
            raise YamlGap("trailing lines")
        out.append(val)
    return out
