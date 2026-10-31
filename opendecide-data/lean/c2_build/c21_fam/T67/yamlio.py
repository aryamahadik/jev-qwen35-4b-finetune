"""YAML emitter (block style, plus anchors / aliases and neutral comments) and the round-trip parser used by the validators.

The emitter writes only what the renderers need: mappings, sequences, scalars (str, int, bool, None). Strings that a YAML 1.1 loader would read as
another type (yes / no / on / off / null / numbers) or that carry YAML syntax are single-quoted. Round trip: `parse(dump(x)) == x` is a CPU test.
The parser is PyYAML `safe_load` (MIT) as the G0-lite's "YAML parser"; the workflow key `on` is read back by PyYAML as the boolean True (YAML 1.1) and
`normalise_keys` turns it back into the string "on". No document is ever executed, applied or sent anywhere.
"""
import re

try:                                                          # tool-only dependency (MIT); the validators report it as unavailable otherwise
    import yaml as _yaml
except ImportError:                                           # pragma: no cover
    _yaml = None

_SAFE = re.compile(r"^[A-Za-z_][A-Za-z0-9_./@:-]*$")
_RESERVED = {"yes", "no", "on", "off", "true", "false", "null", "~", "y", "n"}


class Anchored(object):
    """A mapping emitted once with `&name` and afterwards as `*name` (resolves to the same content)."""

    def __init__(self, name, value):
        self.name, self.value = name, value


def scalar(v):
    if v is None:
        return "null"
    if v is True:
        return "true"
    if v is False:
        return "false"
    if isinstance(v, int):
        return str(v)
    s = str(v)
    if s and _SAFE.match(s) and s.lower() not in _RESERVED and not re.match(r"^[0-9]", s) and ": " not in s:
        return s
    return "'" + s.replace("'", "''") + "'"


def key_text(k):
    if k is True:
        return "on"
    return scalar(k) if k != "on" else "on"


def dump(obj, indent=2, comments=None, rng=None, flow=False):
    """Block YAML text. comments: list of neutral comment strings inserted before random top-level sequence items (rng required)."""
    seen = set()
    lines = []
    _emit(obj, 0, indent, lines, seen, comments or [], rng, flow, top=True)
    return "\n".join(lines) + "\n"


def _emit(v, level, ind, lines, seen, comments, rng, flow, top=False, inline_key=None):
    pad = " " * level
    if isinstance(v, Anchored):
        if v.name in seen:
            lines[-1] = lines[-1] + " *" + v.name if inline_key is not None else lines[-1]
            return
        seen.add(v.name)
        # the anchor goes on the key line
        lines[-1] = lines[-1] + " &" + v.name
        _emit(v.value, level + ind, ind, lines, seen, comments, rng, flow)
        return
    if isinstance(v, dict):
        if not v:
            if inline_key is not None:
                lines[-1] = lines[-1] + " {}"
            else:
                lines.append(pad + "{}")
            return
        for k, val in v.items():
            if isinstance(val, Anchored) and val.name in seen:
                lines.append("%s%s: *%s" % (pad, key_text(k), val.name))
                continue
            if isinstance(val, (dict, list, Anchored)) and (val.value if isinstance(val, Anchored) else val) not in ({}, []):
                lines.append("%s%s:" % (pad, key_text(k)))
                _emit(val, level + ind if not isinstance(val, list) else level + ind, ind, lines, seen, comments, rng, flow, inline_key=k)
            elif isinstance(val, (dict, list)):
                lines.append("%s%s: %s" % (pad, key_text(k), "{}" if isinstance(val, dict) else "[]"))
            else:
                lines.append("%s%s: %s" % (pad, key_text(k), scalar(val)))
        return
    if isinstance(v, list):
        if flow and all(not isinstance(x, (dict, list)) for x in v) and inline_key is not None:
            lines[-1] = lines[-1] + " [" + ", ".join(scalar(x) for x in v) + "]"
            return
        for x in v:
            if comments and rng is not None and top and rng.random() < 0.3:
                lines.append(pad + "# " + rng.choice(comments))
            if isinstance(x, dict) and x:
                first = True
                for k, val in x.items():
                    lead = pad + "- " if first else pad + "  "
                    first = False
                    if isinstance(val, Anchored) and val.name in seen:
                        lines.append("%s%s: *%s" % (lead, key_text(k), val.name))
                    elif isinstance(val, (dict, list, Anchored)) and (val.value if isinstance(val, Anchored) else val) not in ({}, []):
                        lines.append("%s%s:" % (lead, key_text(k)))
                        _emit(val, level + 2 + (ind if not isinstance(val, list) else ind), ind, lines, seen, comments, rng, flow, inline_key=k)
                    elif isinstance(val, (dict, list)):
                        lines.append("%s%s: %s" % (lead, key_text(k), "{}" if isinstance(val, dict) else "[]"))
                    else:
                        lines.append("%s%s: %s" % (lead, key_text(k), scalar(val)))
            elif isinstance(x, list):
                lines.append(pad + "-")
                _emit(x, level + ind, ind, lines, seen, comments, rng, flow)
            else:
                lines.append(pad + "- " + (scalar(x) if not isinstance(x, dict) else "{}"))
        return
    lines.append(pad + scalar(v))


def available():
    return _yaml is not None


def parse(text):
    """-> list of documents (separated by '---')."""
    if _yaml is None:
        raise RuntimeError("PyYAML is not installed (validator unavailable)")
    return [normalise_keys(d) for d in _yaml.safe_load_all(text) if d is not None]


def normalise_keys(x):
    if isinstance(x, dict):
        return {("on" if k is True else k): normalise_keys(v) for k, v in x.items()}
    if isinstance(x, list):
        return [normalise_keys(i) for i in x]
    return x
