"""families/T46/vocab.py: the T46 renderers (state layouts, rules block, codes). Program text only; solver B has its own
parsers (solver_b.py imports nothing from here).

An item is a dict {key, s (the printed value), slot (the spec slot it comes from), group (request | figures | checks),
kind (str | money | count | flag)}; every layout returns (text, spans) with one span per printed value.
"""
from __future__ import annotations

from c2_kit.distractors import uhash
from c2_kit.skin import Span

from . import tables as T


class _Out:
    def __init__(self):
        self.parts, self.n, self.spans = [], 0, []

    def add(self, t: str) -> "_Out":
        self.parts.append(t)
        self.n += len(t)
        return self

    def val(self, t: str, slot: str) -> "_Out":
        self.spans.append(Span("state", self.n, self.n + len(t), slot, "value"))
        return self.add(t)

    def done(self):
        return "".join(self.parts), self.spans


def _jv(it: dict, out: _Out) -> None:
    if it["kind"] == "str":
        out.add('"').val(it["s"], it["slot"]).add('"')
    else:
        out.val(it["s"], it["slot"])           # money / count / flag print as bare JSON literals


def _toml_v(it: dict, out: _Out) -> None:
    _jv(it, out)


GROUPS = (("request", "figures", "checks"), ("record", "numbers", "flags"), ("subject", "amounts", "checks"),
          ("case", "values", "tests"), ("meta", "metrics", "signals"))
COMMENTS = ("", "# record", "# request record", "# case", "# extract")
WORDS = ("amber", "birch", "cedar", "dune", "ember", "fern", "grove", "heron", "iris", "juniper", "kelp", "lotus",
         "maple", "nectar", "olive", "pine", "quartz", "reed", "sage", "thistle",
         "agate", "basalt", "cobalt", "dahlia", "elm", "flint", "garnet", "hazel", "ivy", "jade", "kiln", "larch",
         "marble", "nickel", "opal", "pewter", "quill", "russet", "slate", "tallow")
TICKET_HEADS = ("Ticket extract (checks are answered yes or no)", "Ticket extract: the checks below say yes or no",
                "Ticket extract, checks answered with yes or no")
N_VARIANTS = len(WORDS)


def params(v: int) -> dict:
    """Cosmetic parameters of layout variant v (0..39): every variant is a distinct skin of the layout (G11: no skin
    above 2% of the family; a G5-H quarantine of one skin then costs a small share). Variants v and v + 20 share the
    cosmetics and differ in the field order (the plan's order salt)."""
    v = v % 20
    return {"sep": v % 2, "ind": 2 + 2 * ((v // 2) % 2), "grp": GROUPS[(v // 4) % 5], "cmt": COMMENTS[(v // 3) % 5],
            "q": (v // 5) % 2, "sp": (v // 7) % 2, "head": TICKET_HEADS[v % 3], "bullet": "- " if v % 4 else "* "}


def groups_of(items: list, names: tuple) -> list:
    gs = []
    for g, label in zip(("request", "figures", "checks"), names):
        sub = [it for it in items if it["group"] == g]
        if sub:
            gs.append((label, sub))
    return gs


def _q(it: dict, out: _Out, quote: bool) -> None:
    if it["kind"] == "str" and quote:
        out.add('"').val(it["s"], it["slot"]).add('"')
    else:
        out.val(it["s"], it["slot"])


def state_text(layout: str, items: list, variant: int = 0) -> tuple:
    out = _Out()
    p = params(variant)
    nl = "\n"
    if layout == "json":
        col = ": " if p["sep"] == 0 else ":"
        if variant % 3 == 0:
            out.add("{" + nl + " " * p["ind"])
            glue = "," + nl + " " * p["ind"]
        else:
            out.add("{")
            glue = ", " if p["sep"] == 0 else ","
        for i, it in enumerate(items):
            out.add(("" if i == 0 else glue) + f'"{it["key"]}"{col}')
            _jv(it, out)
        out.add((nl if variant % 3 == 0 else "") + "}")
    elif layout == "json_nested":
        col = ": " if p["sep"] == 0 else ":"
        ind = " " * p["ind"]
        out.add("{" + nl)
        gs = groups_of(items, p["grp"])
        for gi, (g, sub) in enumerate(gs):
            out.add(f'{ind}"{g}"{col}{{' + nl)
            for i, it in enumerate(sub):
                out.add(f'{ind * 2}"{it["key"]}"{col}')
                _jv(it, out)
                out.add("," + nl if i < len(sub) - 1 else nl)
            out.add(ind + "}" + ("," + nl if gi < len(gs) - 1 else nl))
        out.add("}")
    elif layout in ("yaml", "kv_colon"):
        if layout == "yaml":
            out.add("---" + nl)
        if p["cmt"]:
            out.add(p["cmt"] + nl)
        for i, it in enumerate(items):
            out.add(f'{it["key"]}: ')
            _q(it, out, layout == "yaml" and p["q"] == 1)
            out.add(nl if i < len(items) - 1 else "")
    elif layout == "yaml_nested":
        out.add("---" + nl)
        if p["cmt"]:
            out.add(p["cmt"] + nl)
        ind = " " * p["ind"]
        gs = groups_of(items, p["grp"])
        for gi, (g, sub) in enumerate(gs):
            out.add(f"{g}:" + nl)
            for i, it in enumerate(sub):
                out.add(f'{ind}{it["key"]}: ')
                _q(it, out, p["q"] == 1)
                out.add(nl if not (gi == len(gs) - 1 and i == len(sub) - 1) else "")
    elif layout == "kv_equals":
        if p["cmt"]:
            out.add(p["cmt"] + nl)
        eq = "=" if p["sp"] == 0 else " = "
        for i, it in enumerate(items):
            out.add(f'{it["key"]}{eq}').val(it["s"], it["slot"])
            out.add(nl if i < len(items) - 1 else "")
    elif layout == "kv_pipe":
        if p["cmt"]:
            out.add(p["cmt"] + nl)
        width = max(len(it["key"]) for it in items) if p["sp"] else 0
        for i, it in enumerate(items):
            out.add(f'{it["key"].ljust(width)} | ').val(it["s"], it["slot"])
            out.add(nl if i < len(items) - 1 else "")
    elif layout == "ticket":
        out.add(p["head"] + nl)
        for i, it in enumerate(items):
            lab = it["key"].replace("_", " ")
            out.add(f'{p["bullet"]}{lab}: ').val(it["s"], it["slot"])
            out.add(nl if i < len(items) - 1 else "")
    elif layout == "toml":
        out.add("[record]" + nl)
        if p["cmt"]:
            out.add(p["cmt"] + nl)
        eq = " = " if p["sp"] == 0 else "="
        for i, it in enumerate(items):
            out.add(f'{it["key"]}{eq}')
            _jv(it, out)
            out.add(nl if i < len(items) - 1 else "")
    elif layout == "xml":
        out.add("<record>" + nl)
        ind = " " * p["ind"]
        for it in items:
            out.add(f'{ind}<{it["key"]}>').val(it["s"], it["slot"]).add(f'</{it["key"]}>' + nl)
        out.add("</record>")
    else:
        raise ValueError(f"layout {layout!r}")
    return out.done()


def printed_flag(layout: str, value: bool) -> str:
    if layout == "ticket":
        return "yes" if value else "no"
    return "true" if value else "false"


def money_text(cents: int) -> str:
    return f"{cents // 100}.{cents % 100:02d}"


# ------------------------------------------------------------------------------------------------ codes
CONSONANTS = "BCDFGHJKLMNPQRSTVWXZ"


def code_map(key: str, style: str) -> dict:
    """{class: code}: four distinct codes of lengths 1, 2, 3, 4 assigned to the classes by a seeded permutation
    (distinct lengths keep the gold's length rank uniform)."""
    lens = sorted((1, 2, 3, 4), key=lambda n: uhash(key, "codelen", n))
    out, used = {}, set()
    for c, n in zip(T.CLASSES, lens):
        for j in range(50):
            if style == "alpha":
                t = "".join(CONSONANTS[int(uhash(key, "code", c, j, k) * len(CONSONANTS))] for k in range(n))
            else:
                t = str(1 + int(uhash(key, "code", c, j, 0) * 9)) + "".join(
                    str(int(uhash(key, "code", c, j, k) * 10)) for k in range(1, n))
            if t not in used:
                used.add(t)
                out[c] = t
                break
        else:
            raise ValueError("no code")
    return out


# ------------------------------------------------------------------------------------------------ rules block
def cond_text(kind: str, name: str, *, active_value: bool = True, limit: str = "", inclusive: bool = False) -> str:
    if kind == "flag":
        return f"{name} is {'true' if active_value else 'false'}"
    return f"{name} is {'at least' if inclusive else 'above'} {limit}"


def rules_block(*, policy: dict | None, labels: dict, defs: dict | None, order_keys: list) -> str:
    """policy: {"lines": [(cls, [cond texts])], "default_cls", "ignore": [names]} or None; labels: {cls: printed label};
    defs: {cls: gloss text} or None; order_keys: the classes in the order the meanings are listed."""
    out = []
    if policy:
        out.append("Policy: apply the numbered lines in order; the first line that applies decides.")
        for i, (cls, conds) in enumerate(policy["lines"], 1):
            out.append(f'{i}. {labels[cls]} if {" or ".join(conds)}.')
        out.append(f'Otherwise: {labels[policy["default_cls"]]}.')
        if policy["ignore"]:
            out.append("Never counted: " + ", ".join(policy["ignore"]) + ".")
    if defs:
        out.append("Meanings:")
        for cls in order_keys:
            out.append(f"- {labels[cls]}: {defs[cls]}")
    out.append(T.CLOSED_WORLD)
    return "\n".join(out)


def question_line(label: str) -> str:
    return f"Proposed action: {label}"

