"""Plug point for the T66 pipeline: `checked.adapter(solver_b=hook.solver_b)`.

`solver_b(bview)` takes ONLY the b-view of a row (schema.b_view): head, rendered text, options. It returns
    {"status": "ok"|"abstain"|"error", "label": "YES"|"NO"|"BREAKING"|"SAFE"|None, "letter": option letter of the label (read from the rendered options) | None, "why": short reason}
Nothing else of the record is ever touched."""
from . import merge_b, msg_b, semver_b
from . import textparse as tp

_HEADS = {"MERGE": (merge_b.solve, ("YES", "NO")), "SEMVER": (semver_b.solve, ("BREAKING", "SAFE")), "MSG": (msg_b.solve, ("YES", "NO"))}


def _res(status, label=None, letter=None, why=""):
    return {"status": status, "label": label, "letter": letter, "why": why}


def solver_b(bview):
    try:
        head = bview["head"]
        rendered = bview["rendered"]
        entry = _HEADS.get(head)
        if entry is None:
            return _res("error", why="unknown head")
        fn, vocab = entry
        opts = tp.parse_options(rendered, bview.get("options"))
        if sorted(t for _l, t in opts) != sorted(vocab):
            return _res("error", why="options are not %s" % "/".join(vocab))
        context = rendered.get("context")
        if not context:
            return _res("error", why="no context")
        label, why = fn(context)
        if label is None:
            return _res("abstain", why=why)
        return _res("ok", label, tp.letter_of(opts, label), why)
    except tp.ParseError as e:
        return _res("abstain", why="parse: %s" % e)
    except Exception as e:                                                  # noqa: BLE001 - never raise into the pipeline
        return _res("error", why="%s" % type(e).__name__)
