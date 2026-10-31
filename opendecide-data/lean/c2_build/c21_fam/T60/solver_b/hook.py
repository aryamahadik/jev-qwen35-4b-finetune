"""T60 solver B plug points (G1: a PROGRAM, no LLM, no files read at run time, stdlib only).

    <T60 checked module>.adapter(solver_b=hook.solver_b, render_b=hook.render_b)

`view` = {family, sub_block, options:[{letter,label,text}], rendered:{context,question,options_text,text}} (the pipeline's b-view and nothing
else). solver_b recomputes the LABEL from the facts in the rendered context and takes its LETTER from the TEXT of view['options'] (the `label`
field of an option is never read). render_b returns ("letter", X) where X is the letter of the option whose rendered TEXT (options_text lines)
says what the recomputed label says, or ("abstain", why). Unparsable rows abstain; B never guesses."""
try:
    from . import t60b_h1, t60b_h2, t60b_h3
    from .t60b_text import ParseGap, Result, detect_head, letters_from_options, options_from_rendered
except ImportError:                                                  # loaded as a top-level module from this folder
    import t60b_h1
    import t60b_h2
    import t60b_h3
    from t60b_text import ParseGap, Result, detect_head, letters_from_options, options_from_rendered

_SOLVERS = {"h1": t60b_h1.solve, "h2": t60b_h2.solve, "h3": t60b_h3.solve}


def solve_label(view):
    """-> (head, label, parsed facts). Raises ParseGap when the rendered row cannot be parsed."""
    head = detect_head(view)
    ctx = view["rendered"]["context"]
    label, parsed = _SOLVERS[head](ctx)
    return head, label, parsed


def parse_view(view):
    """The facts B recovers from the rendered row (for the K1 / K14 round-trip checks: card numbers, brief or risk facts, order statements, plan
    statuses, references, the fact quote). -> {"head": ..., "label": ..., "parsed": {...}}; raises ParseGap when the row cannot be parsed."""
    head, label, parsed = solve_label(view)
    return {"head": head, "label": label, "parsed": parsed}


def solver_b(view):
    try:
        head, label, parsed = solve_label(view)
        letters = letters_from_options(head, view.get("options") or [])
    except ParseGap as e:
        return Result(abstain=True, reason="parse_gap:" + e.why)
    except (KeyError, TypeError, ValueError, IndexError, AttributeError) as e:      # malformed view / unforeseen text shape: abstain
        return Result(abstain=True, reason="parse_error:" + type(e).__name__)
    return Result(label=label, letter=letters[label], abstain=False, reason=None, parsed=parsed)


def render_b(view):
    try:
        head, label, _parsed = solve_label(view)
        letters = letters_from_options(head, options_from_rendered(view["rendered"]["options_text"]))
    except ParseGap as e:
        return ("abstain", "parse_gap:" + e.why)
    except (KeyError, TypeError, ValueError, IndexError, AttributeError) as e:
        return ("abstain", "parse_error:" + type(e).__name__)
    return ("letter", letters[label])
