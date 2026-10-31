"""T67 user turns: the four consent cells (neither / operation only / target only / both). The naming forms are wording-pool forms (>= 50 wordings each,
none above 2%); the surface word of an operation comes from the closed OP_WORD lexicon. Spans of the operation word and the target in the user turn
carry the G10 role AUTHORITY (T67-B10). The GV12 two-way round trip (nothing added, nothing removed) is checked by `naming_check`: the operation word
and the target occur in the turn exactly when the cell names them, and no OTHER lexicon operation word or known target occurs."""
import re

OP_WORD = {"delete": "delete", "replace": "replace", "create": "create", "update": "update", "make_public": "make public", "open_access": "open up",
           "expose": "expose", "grant": "grant access on", "remove_protection": "remove the protection on", "disable": "turn off", "install": "use",
           "run_script": "run the script at", "apply": "apply", "migrate": "run the migration on", "inject_key": "add a login key to"}
FORMS = {"neither": "T67-U-NEITHER", "op": "T67-U-OP", "target": "T67-U-TARGET", "both": "T67-U-BOTH"}
FORM_SLOTS = {"T67-U-NEITHER": [], "T67-U-OP": ["op_word"], "T67-U-TARGET": ["target"], "T67-U-BOTH": ["op_word", "target"],
              "T67-Q-GATE": ["ask"], "T67-Q-REASON": ["ask"], "T67-Q-TIER": ["ask"]}
CELLS = ("neither", "op", "target", "both")


def make_turn(picker, cell, decisive):
    """-> (text, wording_id, naming, slots)."""
    if decisive is None:
        cell = "neither"
    slots = {}
    if cell in ("op", "both"):
        slots["op_word"] = OP_WORD[decisive["op"]]
    if cell in ("target", "both"):
        slots["target"] = decisive["target"]
    wid, text = picker.render(FORMS[cell], **slots)
    naming = {"ops": {decisive["op"]} if cell in ("op", "both") else set(), "targets": {decisive["target"]} if cell in ("target", "both") else set()}
    return text, wid, naming, slots, cell


def naming_check(text, cell, decisive, known_targets=()):
    """GV12 two-way round trip on the rendered user turn: -> list of problems."""
    bad = []
    names_op = cell in ("op", "both")
    names_tgt = cell in ("target", "both")
    for ref, word in OP_WORD.items():
        present = re.search(r"(?<![A-Za-z])%s(?![A-Za-z])" % re.escape(word), text) is not None
        want = names_op and decisive is not None and ref == decisive["op"]
        if present and not want:
            if not (decisive is not None and word in OP_WORD[decisive["op"]]):
                bad.append("extra_op:" + ref)
        if want and not present:
            bad.append("missing_op")
    for t in known_targets:
        present = t in text
        want = names_tgt and decisive is not None and t == decisive["target"]
        if present and not want and names_tgt and decisive is not None and t in decisive["target"]:
            continue                                       # a target that is a substring of the named one (workflow path inside 'path#job')
        if present != want:
            bad.append("target_%s:%s" % ("extra" if present else "missing", t))
    return bad
