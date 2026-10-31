"""Glue between the L-K families and the shared CHECK-AT-GENERATION pipeline (tool_engine/row_pipeline.py; OWNER RULE, plan 16.1
step 2). CODE ONLY: nothing is written, no model is called, nothing generated is executed.

  * `make_adapter(...)` builds the pipeline's FamilyAdapter and REFUSES (SolverBRequired) when solver B or the rendered-text parser is
    missing: solver B is a separate program written by a separate session (G1); there is NO default and NO fallback to solver A.
  * A12 rows carry non-ASCII characters by design (diacritics, homoglyphs, U+200B). The pipeline's format probe is ASCII-only, so
    `a12_format_probe()` swaps it, for the duration of a run, for a probe that accepts exactly the characters of the row's declared
    transform (and nothing else). Other families' runs (other processes) are untouched.
  * Answer checks on an A12 row run on its CANONICAL view (the recorded inverse applied), so solver B parses the same text a clean row
    has; the inverse itself and the decision-span survival are family invariants (K27).
  * `TestDoubleSolverB` / `test_double_render_b` are for CPU tests ONLY (they call solver A, so they are not independent).
"""
import contextlib

from tool_engine import row_pipeline as rp, util
from . import klevers


class SolverBRequired(RuntimeError):
    """No solver B (or no rendered-text parser) was supplied: the pipeline will not run (G1: B is a separate program)."""


def canonical_view(rec):
    """The row as a clean row would be: the recorded A12 inverse applied to the context and the full text. Rows without `a12` are
    returned unchanged (same object)."""
    a = rec.get("a12")
    if not a:
        return rec
    ops = [tuple(o) for o in a["ops"]]
    r = rec["rendered"]
    ctx = klevers.invert(r["context"], ops)
    out = dict(rec)
    out["rendered"] = dict(r, context=ctx, text=ctx + "\n\n" + r["question"] + "\n" + r["options_text"])
    # skeptic fix: the canonical copy is CLEAN. It used to keep `a12`, and the adapter's solver-B wrappers canonicalise again, so for every
    # insertion transform (spacing, zero_width, bidi) the inverse was applied twice and deleted real characters of the text B read.
    out["a12"] = None
    out["a12_inverted"] = a
    return out


# What solver B and its rendered-text parser may see (G1: B is a separate program that reads the RENDERED row, never the spec). The pipeline
# hands over a sanitised copy: no scene / case / trace / gold / gold_letter / lines / tags (trigger, edit, ctl, card_mode, levels ...) / ids.
# `sub_block` (T59: trigger id, T60: head) is kept because the ROW_SCHEMA documents it as an input; it carries no label (K5 / K8).
B_VIEW_FIELDS = ("family", "sub_block")
B_VIEW_RENDERED = ("context", "question", "options_text", "text")
B_VIEW_OPTION = ("letter", "label", "text")


def solver_b_view(rec):
    v = {k: rec[k] for k in B_VIEW_FIELDS if k in rec}
    v["options"] = [{k: o[k] for k in B_VIEW_OPTION} for o in rec["options"]]
    v["rendered"] = {k: rec["rendered"][k] for k in B_VIEW_RENDERED}
    return v


def _full_record_double(fn):
    """True only for the CPU test doubles below (they call solver A and need the full record)."""
    return getattr(fn, "needs_full_record", False) is True


def wrap_solver_b(solver_b):
    if _full_record_double(solver_b):
        return lambda rec: solver_b(canonical_view(rec))
    return lambda rec: solver_b(solver_b_view(canonical_view(rec)))


def wrap_render_b(render_b):
    if _full_record_double(render_b):
        return lambda rec: render_b(canonical_view(rec))
    return lambda rec: render_b(solver_b_view(canonical_view(rec)))


def make_adapter(family, gen, gold_a, solver_b, render_b, allowlist, forbidden, code_files, lint_outputs,
                 extra_checks=(), pair_check=None, extra_rows=None, check_extra_row=None, gates=None, pool_path=None,
                 abstain_is_drop=True, plan_kwargs=None):
    if solver_b is None or render_b is None:
        raise SolverBRequired("%s: solver B and its rendered-text parser must be supplied by the solver-B session" % family)
    return rp.FamilyAdapter(
        family, gen, gold_a=gold_a, solver_b=wrap_solver_b(solver_b), render_b=wrap_render_b(render_b), allowlist=allowlist,
        lint_outputs=lint_outputs, forbidden=forbidden, abstain_is_drop=abstain_is_drop, extra_checks=extra_checks,
        pair_check=pair_check, code_files=code_files, extra_rows=extra_rows, check_extra_row=check_extra_row, gates=gates,
        pool_path=pool_path, plan_kwargs=plan_kwargs)


@contextlib.contextmanager
def a12_format_probe():
    """Scoped replacement of rp.format_probe_row: ASCII-only for every row except a row tagged lever.a12, which may contain exactly the
    characters of its transform (recorded in rec['a12']['transform'])."""
    orig = rp.format_probe_row

    def patched(rec, forbidden, allow_non_ascii=False):
        a = rec.get("a12")
        if not a:
            return orig(rec, forbidden, allow_non_ascii)
        bad = orig(rec, forbidden, True)
        allowed = klevers.allowed_nonascii([a["transform"]])
        extra = {c for c in rec["rendered"]["text"] if ord(c) > 127 and c not in allowed}
        if extra:
            bad.append("non_ascii_off_transform")
        return bad

    rp.format_probe_row = patched
    try:
        yield
    finally:
        rp.format_probe_row = orig


def run_checked_k(ad, total, seed, stamper, standin=False, ctx=None, **kw):
    """rp.run_checked with an explicit L-K context (the pipeline's default context only knows L-T families)."""
    if ctx is None:
        raise ValueError("pass ctx=gen.Ctx(...): the L-K families build their own name source")
    with a12_format_probe():
        return rp.run_checked(ad, total, seed, stamper, standin=standin, ctx=ctx, **kw)


# ---- test doubles (CPU tests only; they are NOT independent of solver A) ----------------------------------------------------
class _BRes(object):
    def __init__(self, label, letter, abstain=False, reason=None):
        self.label, self.letter, self.abstain, self.reason = label, letter, abstain, reason


class TestDoubleSolverB(object):
    """Calls solver A. Named so it cannot be mistaken for solver B."""
    __test__ = False
    needs_full_record = True

    def __init__(self, gold_a, flip_ids=()):
        self.gold_a, self.flip_ids = gold_a, set(flip_ids)

    def __call__(self, rec):
        lab = self.gold_a(rec)
        if rec["row_id"] in self.flip_ids:
            lab = [o["label"] for o in rec["options"] if o["label"] != lab][0]
        letter = next((o["letter"] for o in rec["options"] if o["label"] == lab), None)
        return _BRes(lab, letter)


def test_double_render_b(rec):
    return ("letter", rec["gold_letter"])
test_double_render_b.__test__ = False
test_double_render_b.needs_full_record = True


def derived_perturbed_row(clean, new_context, a12, row_suffix="x"):
    """A perturbed twin of a kept clean row: same record, context / text replaced, `a12` and `twin_of` set. The caller has already
    verified the inverse."""
    import copy
    r = copy.deepcopy(clean)
    r["row_id"] = clean["row_id"] + "~" + row_suffix
    r["twin_of"] = clean["row_id"]
    r["lever_tag"] = "lever.a12"
    r["a12"] = a12
    r["rendered"]["context"] = new_context
    r["rendered"]["text"] = new_context + "\n\n" + clean["rendered"]["question"] + "\n" + clean["rendered"]["options_text"]
    r.pop("stamp", None)
    return r
