"""T57 check-at-generation adapter (OWNER RULE 18 Oct, plan 16.1 step 2). Wires LC_COMMON/checked.py to this family: solver A labels
(sandbox witnesses), solver B (a separate program, stdlib only) must reproduce the label of every row, the names guard, the token rule,
the format probe and the G13 stamp boundary run at the moment a row is made, before it can enter a pool.

CODE ONLY: nothing is written, no model is called, nothing generated is executed. `run_checked` refuses to start without a stamp hook
(`StampServiceRequired`) and, for a production run, without the row-start guard pins and without a real executor (the SimExecutor is
for tests and the dry run only)."""
from LC_COMMON import sandbox_iface as S
from LC_COMMON.checked import RowChecker, StampServiceRequired  # noqa: F401

from .build import build_rows
from .solver_b import hook


def make_checker(stamp_hook, standin=False, **kw):
    return RowChecker("T57", lambda row, pk: hook.check_row(row, pk), stamp_hook, hook.BLOCK_DROP_LIMIT, standin=standin, **kw)


def run_checked(n_target, executor, picker, stamp_hook, seed=0, standin=False, **kw):
    """-> (kept_rows, summary, checker). Every kept row carries a `stamp`. `standin=True` is for tests and the dry run only."""
    if not standin and isinstance(executor, S.SimExecutor):
        raise ValueError("a production run needs the real executor (od-sbx1), not the SimExecutor")
    checker = make_checker(stamp_hook, standin)
    out = build_rows(n_target, executor, picker, seed=seed, checker=checker, **kw)
    rows = out[0]
    return rows, checker.summary(rows), checker
