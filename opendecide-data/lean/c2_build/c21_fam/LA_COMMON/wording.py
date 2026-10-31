"""Wording-pool interface (Haiku writes the pools later; this code only defines forms, slots, roles and the
renderer that turns a form + slot values into a turn with exact decision_spans).

A pool file is JSON: {"version": ..., "is_stub": false, "forms": {form_id: [template, ...]},
                      "lexicon": {lex_id: [surface, ...]}}.
Templates use {slot}. Slot roles come from the form definition (so the pool author cannot change which spans
carry AUTHORITY). K11: >= 50 wordings per form, no wording used > 2% of the family's rows.
The STUB pool below exists so unit tests and the 20-example dry run can run; it has 3 wordings per form, so
K11 correctly FAILS on it, and `refuse_stub()` stops any row job from using it.
"""
import json
import re

from .canon import sha_obj
from .spans import make_span, ROLE_AUTHORITY, ROLE_ENTITY, ROLE_NUMBER, ROLE_NEGATION

_SLOT = re.compile(r"\{([a-z_0-9]+)\}")

FORMS = {}   # form_id -> {"family": ..., "slots": {slot: [roles]}, "doc": ...}


def register_form(form_id, family, slots, doc=""):
    FORMS[form_id] = {"family": family, "slots": {k: sorted(v) for k, v in slots.items()}, "doc": doc}


class PoolError(Exception):
    pass


class WordingPool:
    def __init__(self, data):
        self.version = data.get("version", "0")
        self.is_stub = bool(data.get("is_stub"))
        self.forms = data["forms"]
        self.lexicon = data.get("lexicon", {})
        self.sha = sha_obj(data)

    @classmethod
    def load(cls, path):
        with open(path, "r", encoding="utf-8") as f:
            return cls(json.load(f))

    def validate(self, min_per_form=50):
        """K11 part 1. Returns a list of problems (names only)."""
        bad = []
        for fid, meta in FORMS.items():
            tpls = self.forms.get(fid, [])
            if len(tpls) < min_per_form:
                bad.append("K11: form %s has %d wordings (< %d)" % (fid, len(tpls), min_per_form))
            if len(set(tpls)) != len(tpls):
                bad.append("K11: form %s has duplicate wordings" % fid)
            for t in tpls:
                slots = set(_SLOT.findall(t))
                if not slots <= set(meta["slots"]):
                    bad.append("form %s: wording uses unknown slot(s) %s" % (fid, sorted(slots - set(meta["slots"]))))
                    break
                req = {s for s in meta["slots"] if not s.startswith("opt_")}
                if not req <= slots:
                    bad.append("form %s: wording lacks required slot(s) %s" % (fid, sorted(req - slots)))
                    break
        return bad

    def lex(self, lex_id, rng):
        opts = self.lexicon.get(lex_id)
        if not opts:
            raise PoolError("lexicon entry %r missing" % lex_id)
        return rng.choice(opts)


def render_form(pool, form_id, values, rng, turn_idx=0):
    """-> (text, spans, wording_index). values: {slot: text}. Spans have exact character offsets."""
    meta = FORMS[form_id]
    tpls = pool.forms.get(form_id)
    if not tpls:
        raise PoolError("no wordings for form %s" % form_id)
    wi = rng.randrange(len(tpls))
    tpl = tpls[wi]
    out, spans, pos = [], [], 0
    for m in _SLOT.finditer(tpl):
        out.append(tpl[pos:m.start()])
        slot = m.group(1)
        txt = values[slot]
        start = sum(len(x) for x in out)
        out.append(txt)
        roles = meta["slots"].get(slot, [])
        if roles:
            spans.append(make_span(turn_idx, slot, start, start + len(txt), roles))
        pos = m.end()
    out.append(tpl[pos:])
    return "".join(out), spans, wi


def refuse_stub(pool):
    if pool.is_stub:
        raise PoolError("stub wording pool: not allowed for row jobs")


def stub_pool():
    """3 plain wordings per registered form, for unit tests / dry run only."""
    forms, lex = {}, {}
    for fid, meta in FORMS.items():
        slots = sorted(s for s in meta["slots"] if not s.startswith("opt_"))
        body = " ".join("{%s}" % s for s in slots)
        forms[fid] = ["Please handle this: " + body + ".", "Note: " + body + " (stub).", "Task " + body + "."]
    return WordingPool({"version": "stub", "is_stub": True, "forms": forms, "lexicon": lex})
