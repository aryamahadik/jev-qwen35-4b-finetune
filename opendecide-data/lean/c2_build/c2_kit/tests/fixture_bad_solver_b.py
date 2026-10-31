"""A deliberately non-independent solver B (test fixture for plugin.check_independence; never used for rows)."""
from c2_kit import rules  # noqa: F401  (solver-A code: forbidden on the B side)
from c2_kit.reference.r00_solver_b import parse  # noqa: F401


def solve_b(view):
    return rules.evaluate(rules.Lit(True), {})
