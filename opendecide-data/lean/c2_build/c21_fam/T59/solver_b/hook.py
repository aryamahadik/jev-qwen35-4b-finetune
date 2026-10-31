"""T59 solver B plug-points for the family pipeline (t59_checked.adapter(solver_b=hook.solver_b, render_b=hook.render_b)).

`view` = {family, sub_block, options: [{letter, label, text}], rendered: {context, question, options_text, text}} and nothing else.
solver_b recomputes the label from the rendered CONTEXT (card + tools + conversation + planned step), then maps it to a letter through
the TEXT of the options (the given `label` field of an option is never read). render_b recovers the gold letter the same way
(rendered text -> label -> option text), and abstains when the options cannot be classified or the context cannot be parsed.
No file is opened, nothing is executed, no model or network is touched (G1).
"""
try:                                    # normal case: loaded as a package module
    from . import parse as _parse, rules as _rules
except ImportError:                     # loaded as a stand-alone file next to its siblings
    import parse as _parse              # noqa: E402
    import rules as _rules              # noqa: E402


_STRUCT_TRIGGERS = {"t6": ("T6",), "t3": ("T3",), "t7": ("T7",), "readings": ("T2", "T4", "T8"), "single": ("T1", "T5")}


class Result(object):
    __slots__ = ("label", "letter", "abstain", "reason", "rule")

    def __init__(self, label=None, letter=None, abstain=False, reason=None, rule=None):
        self.label = label
        self.letter = letter
        self.abstain = abstain
        self.reason = reason
        self.rule = rule

    def __repr__(self):
        return "Result(label=%r, letter=%r, abstain=%r, reason=%r)" % (self.label, self.letter, self.abstain, self.reason)


def _context_of(view):
    r = view["rendered"]
    ctx = r.get("context")
    if ctx:
        return ctx
    text = r["text"]
    i = text.rfind("\n\nQuestion:")
    return text[:i] if i >= 0 else text


def _options_text_of(view):
    r = view["rendered"]
    ot = r.get("options_text")
    if ot:
        return ot
    text = r["text"]
    i = text.rfind("\nA) ")
    return text[i + 1:] if i >= 0 else ""


def solve(view):
    """-> Result."""
    try:
        facts = _parse.parse_context(_context_of(view))
        dec = _rules.decide(facts)
    except _rules.Abstain as e:
        return Result(abstain=True, reason="abstain:" + str(e))
    except Exception as e:                                          # noqa: BLE001 - an unparsable row is an abstain, never a guess
        return Result(abstain=True, reason="abstain:error:" + type(e).__name__)
    sb = view.get("sub_block") if hasattr(view, "get") else None
    if sb is not None and dec.detail in _STRUCT_TRIGGERS and sb not in _STRUCT_TRIGGERS[dec.detail]:
        # the trigger id is a documented input (no label in it); a structure that contradicts it means a parse or wording gap: abstain
        return Result(abstain=True, reason="abstain:structure_vs_sub_block")
    opts = _parse.parse_options(_options_text_of(view))
    if opts is None:
        return Result(abstain=True, reason="abstain:options_unclassified")
    return Result(label=dec.label, letter=opts[dec.label], abstain=False, reason=dec.rule, rule=dec.rule)


def solver_b(view):
    return solve(view)


def render_b(view):
    """-> ("letter", X) or ("abstain", why)."""
    res = solve(view)
    if res.abstain:
        return ("abstain", res.reason)
    return ("letter", res.letter)
