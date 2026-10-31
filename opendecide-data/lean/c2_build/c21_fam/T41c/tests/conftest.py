import os
import sys

import pytest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INFRA = os.path.join(os.path.dirname(os.path.dirname(HERE)), "c21_infra")
for p in (HERE, INFRA):
    if p not in sys.path:
        sys.path.insert(0, p)


@pytest.fixture(scope="session")
def pool():
    from t41c import pools
    return pools.make_test_pool(per_cell=12)


@pytest.fixture(scope="session")
def heldout():
    from t41c import planner
    return planner.draw_heldout()


@pytest.fixture(scope="session")
def plan2000(heldout):
    from t41c import planner
    specs, rep = planner.plan_specs(2000, heldout=heldout)
    return specs


@pytest.fixture(scope="session")
def built2000(plan2000, pool):
    from t41c import build
    rows, rep = build.build_rows(plan2000, pool)
    return rows, rep


@pytest.fixture(scope="session")
def ho_built(heldout, pool):
    from t41c import build, planner
    specs, rep = planner.plan_heldout(heldout=heldout)
    rows, brep = build.build_rows(specs, pool)
    return specs, rows, brep
