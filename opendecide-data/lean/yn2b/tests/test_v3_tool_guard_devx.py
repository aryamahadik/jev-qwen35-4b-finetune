"""F2 decide2 (v3_tool_guard) on reviewer R's devx surface (1 Oct re-check, yn2b/decide2_rechecks_1oct.md).

The devx reader (section 6b of v3_tool_guard.py) was written from the rendered devx rows only. These tests pin:
  * every devx F2 row is read and agrees with the gold (SPEC 8.1 for devx; a third program next to R's parse-back);
  * no train / dev row takes the devx path, so the frozen train / dev behaviour cannot move;
  * an unknown JSON layout is UNDEFINED (it used to escape decide2_row as KeyError 'assistant').
"""
import json
import sys
from pathlib import Path

import pytest

LEAN = Path(__file__).resolve().parents[2]
GEN3 = LEAN / "golden_src" / "gen3"
sys.dont_write_bytecode = True
if str(GEN3) not in sys.path:
    sys.path.insert(0, str(GEN3))

import v3_tool_guard as v  # noqa: E402


def _rows(path):
    if not path.exists():
        pytest.skip(f"{path} not written")
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


def test_devx_rows_are_read_and_agree():
    rows = _rows(v.DEVX_PATH)
    res = v.agreement(rows)
    assert res["rows"] == len(rows) == 100
    assert res["undefined"] == 0, [d["error"][:100] for d in res["undefined_rows"][:5]]
    assert res["disagree"] == 0, res["disagreements"][:5]


def test_devx_layouts_parse_to_the_same_kind_of_facts():
    seen = set()
    for r in _rows(v.DEVX_PATH):
        f = v.parse_state(r["state"])
        assert f.dialect == "dx2" and f.rules and f.session.get("time") and f.session.get("uid")
        seen.add(r["meta"]["fmt"])  # report-side only
    assert seen == {"json", "markdown", "prose"}


@pytest.mark.parametrize("path", [v.TRAIN_PATH, v.DEV_PATH], ids=["train", "dev"])
def test_train_and_dev_never_take_the_devx_path(path):
    for r in _rows(path):
        assert v.dx_sections(r["state"]) is None, r["rid"]


def test_unknown_json_layout_is_undefined_not_a_crash():
    state = json.dumps({"policy": ["Rule 1: something"], "catalog": [], "proposed": {}})
    row = {"rid": "x", "state": state, "instructions": "Under the policy, may the proposed call run?",
           "options": ["yes", "no"], "gold": "yes"}
    assert v.decide2_row(row) is v.UNDEFINED


def test_devx_answers_do_not_depend_on_a_reading_switch():
    rows = _rows(v.DEVX_PATH)
    out = v.sensitivity(rows)
    assert all(x["changed"] == 0 for x in out.values()), {k: x["changed"] for k, x in out.items()}
    assert v.READING == v.READING_DEFAULT
