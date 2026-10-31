"""Tiny dry run: 20 IN-MEMORY T53 examples for unit tests (never written to disk). 1 provenance quad (4), 2 destination
pairs (4: one lookalike, one transport), 3 grid rows (3), 1 soft twin pair (2), 1 hard twin pair (2), 3 other channel rows (3),
1 credential-use pair (2) = 20."""
from .blocks import build_cell, plan
from .registry import Registry


def select_dry_cells(cells=None):
    cells = cells if cells is not None else plan()

    def first(pred, k=1):
        return [c for c in cells if pred(c)][:k]

    sel = []
    sel += first(lambda c: c.kind == "a_quad" and c.extras["sub"] == "conf_trusted")
    sel += first(lambda c: c.kind == "b_pair" and c.extras["cue"] == "homograph")
    sel += first(lambda c: c.kind == "b_pair" and c.extras["cue"] == "plain_http")
    sel += first(lambda c: c.kind == "c_row" and c.extras["klass"] == "confidential" and c.extras["vis"] == "unknown")
    sel += first(lambda c: c.kind == "c_row" and c.extras["klass"] == "secret")
    sel += first(lambda c: c.kind == "c_row" and c.extras["klass"] == "public")
    sel += first(lambda c: c.kind == "d_soft_twin")
    sel += first(lambda c: c.kind == "d_hard_twin" and c.extras["channel"] == "credential_in_url")
    sel += first(lambda c: c.kind == "d_ask_mcp_unlisted")
    sel += first(lambda c: c.kind == "d_ask_pkg_trusted")
    sel += first(lambda c: c.kind == "d_allow_conf_priv" and c.extras["channel"] == "mcp_call")
    sel += first(lambda c: c.kind == "e_pair")
    return sel


def build_dry():
    reg = Registry()
    drops = []
    specs = []
    for c in select_dry_cells():
        specs += build_cell(c, drops, None, reg)
    return specs, drops, reg
