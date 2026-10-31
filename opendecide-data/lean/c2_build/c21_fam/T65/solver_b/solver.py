"""Solver B: label of one T65 row from its b-view. Method: AST dataflow (see engine.py), not a witness run and not the spec."""
from . import rules as R
from .engine import Engine, Unsupported
from .parse import ParseGap, parse_options, source_param, split_context


def _ok(label, letter, cls, note=""):
    return {"status": "ok", "label": label, "letter": letter, "cls": cls, "reason": note}


def _abstain(reason, cls=None):
    return {"status": "abstain", "label": None, "letter": None, "cls": cls, "reason": reason}


def option_class(text):
    """Class id an option text of a CWE head row names (by stem), or None when it names none or several."""
    low = text.lower()
    hits = [cid for cid, stems in R.WORD_STEMS if any(s in low for s in stems)]
    return hits[0] if len(hits) == 1 else None


def solve(bview):
    try:
        head = bview["head"]
        r = bview["rendered"]
        opts = parse_options(r["options_text"])
        if [(o["letter"], o["text"]) for o in bview["options"]] != opts:
            return _abstain("options text differs from the option list")
        preamble, code = split_context(r["context"])
    except (ParseGap, KeyError, TypeError) as e:
        return _abstain("parse gap: %s" % e)
    hint = bview.get("sub_block")
    hint = hint if hint in R.CLASSES else None
    if head == "VULN":
        if sorted(t for _l, t in opts) != ["NO", "YES"]:
            return _abstain("VULN options are not YES / NO")
        if "Answer YES for the flawed function" not in preamble:
            return _abstain("definitions card missing")
        group = (bview.get("witness_inputs") or {}).get("class_group")
        try:
            param = source_param(preamble)
        except ParseGap as e:
            return _abstain("parse gap: %s" % e)
        if hint in R.DYNAMIC and param is None:
            return _abstain("dynamic class without a source note")
        if group is not None and hint is not None and (group == "dynamic") != (hint in R.DYNAMIC):
            return _abstain("class group contradicts the sub-block")
        try:
            eng = Engine(code, attacker_param=param if hint in R.DYNAMIC else None, question=r.get("question")).run()
        except Unsupported as e:
            return _abstain("unsupported: %s" % e, hint)
        except SyntaxError:
            return _abstain("code does not parse", hint)
        flawed = eng.flaws
        if hint is not None:
            if hint in flawed:
                label = "YES"
            elif flawed:
                return _abstain("flaw of another class: " + ",".join(sorted(flawed)), hint)
            elif hint not in eng.evidence:
                return _abstain("no operation of the class found", hint)
            else:
                label = "NO"
        else:
            label = "YES" if flawed else "NO"
        letter = next(l for l, t in opts if t == label)
        return _ok(label, letter, hint if label == "YES" else None)
    if head == "CWE":
        if len(opts) != 4:
            return _abstain("CWE options are not four")
        try:
            eng = Engine(code, attacker_param=None, question=r.get("question")).run()
        except Unsupported as e:
            return _abstain("unsupported: %s" % e)
        except SyntaxError:
            return _abstain("code does not parse")
        if len(eng.flaws) != 1:
            return _abstain("flaw classes found: %d" % len(eng.flaws))
        cls = next(iter(eng.flaws))
        match = [(l, t) for l, t in opts if option_class(t) == cls]
        if len(match) != 1:
            return _abstain("class %s not named by exactly one option" % cls, cls)
        return _ok(match[0][1], match[0][0], cls)
    return _abstain("unknown head")
