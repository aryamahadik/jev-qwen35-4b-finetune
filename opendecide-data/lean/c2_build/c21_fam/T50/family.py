"""Whole-family build (IN MEMORY): plan -> specs -> overlays. Used by the dry run and by every set-level gate; it writes nothing.

Per-row creation checks (addendum section 11) that are CPU-only live here: a failed row drops its WHOLE group (pair / quad contrast
integrity) and a replacement group from the same cell with a new seed is drawn (a NEW spec, GV5; at most 2 attempts per slot; a slot
still empty is reported as a short cell). The G13 stamp and the L-0b manifest stamp are not CPU-only and are not run here.
"""
import re
from collections import Counter, defaultdict

from LA_COMMON.wording import stub_pool

from . import blocks, overlays
from .generator import DropLedger, GeneratorDefect, build_cell, render_turns

MAX_ATTEMPTS = 2
PII = re.compile(r"[\w.+-]+@[A-Za-z][\w-]*\.[A-Za-z][\w.-]*|\b\d{3}-\d{2}-\d{4}\b|\b\+?\d[\d ()-]{9,}\d\b")
RESERVED_TLDS = (".test", ".example", ".invalid", ".internal")        # generated hosts use RFC 2606 reserved TLDs: not an e-mail address of a person


def has_pii(text):
    for m in PII.finditer(text or ""):
        g = m.group(0)
        if "@" in g and g.lower().rstrip(".").endswith(RESERVED_TLDS):
            continue
        return True
    return False
TOKEN_CAP = 1536                      # K12 per-row cap (the mean and the 1,024 share are set-level)


class Family:
    def __init__(self, specs, ledger, cells, report):
        self.specs, self.ledger, self.cells, self.report = specs, ledger, cells, report

    def rows(self):
        return [(s, r) for s in self.specs for r in s.renderings if r.get("roundtrip", True)]

    def row_dicts(self):
        """Every row as the dict `generator.spec_rows` builds (dialect, card body, overlay fields included). In memory only."""
        from .generator import spec_rows
        return [d for s in self.specs for d in spec_rows(s)]


def _group_bad(specs):
    return any(not r.get("roundtrip", True) for s in specs for r in s.renderings)


def _row_checks(specs, ledger):
    """Per-row checks of section 11 that are CPU-only and need the rendered turns: K12 cap (1,536 tokens) and the PII scrub. A failing row
    drops its WHOLE group (pair / quad contrast integrity)."""
    from .gates import est_tokens, row_text
    bad = set()
    for s in specs:
        for r in s.renderings:
            if est_tokens(row_text(s, r)) > TOKEN_CAP:
                bad.add(s.group)
                ledger.add(s.spec_id, "K12:cap")
            if has_pii(r["text"]) or any(has_pii(t.text) for t in s.user_turns):
                bad.add(s.group)
                ledger.add(s.spec_id, "PII")
    if bad:
        ledger.add("groups", "group_drop:row_checks:%d" % len(bad))
    return [s for s in specs if s.group not in bad]


def build_all(cells=None, pool=None, with_overlays=True, alias_late=None, quiet=False):
    cells = cells if cells is not None else blocks.plan(alias_late)
    ledger = DropLedger()
    specs, short, defects = [], [], []
    generated_rows = 0
    for cell in cells:
        ok = None
        for attempt in range(MAX_ATTEMPTS + 1):
            if attempt:
                cell.extras["attempt"] = attempt
            try:
                ss = build_cell(cell, ledger, pool)
            except GeneratorDefect as e:
                defects.append((cell.block, cell.intent, cell.extras.get("g") or cell.tag, str(e)[:140]))
                continue
            generated_rows += sum(len(s.renderings) for s in ss)
            if _group_bad(ss):
                ledger.add(ss[0].group, "group_drop:K1")
                continue
            ok = ss
            break
        if ok is None:
            short.append((cell.block, cell.intent, cell.tag))
            continue
        specs += ok
    # per-row turn text: stub pool unless a real pool is given (dry run only; row jobs refuse a stub)
    p = pool or stub_pool()
    for s in specs:
        render_turns(s, p)
    specs = _row_checks(specs, ledger)
    report = {"cells": len(cells), "short_cells": short, "defects": defects, "generated_rows": generated_rows}
    if with_overlays:
        report["a6"] = {b: len(v) for b, v in overlays.apply_cues(specs, ledger).items()}
        report["a12"] = overlays.apply_perturbation(specs)
        report["a15"] = overlays.apply_dialects(specs)
        report["a10"] = overlays.apply_wrappers(specs)
        from . import ladder
        report["ladder"] = ladder.assign_ladder(specs)
        report["heldout"] = overlays.tag_heldout(specs)
    return Family(specs, ledger, cells, report)
