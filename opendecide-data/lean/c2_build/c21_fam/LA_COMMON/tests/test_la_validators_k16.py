import glob
import os

from LA_COMMON import validators as v
from LA_COMMON.expander import shape
from LA_COMMON.shellmodel import SqlStmt
from T50 import gates as g50
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
FAM = os.path.dirname(os.path.dirname(HERE))


def _code_files():
    out = []
    for d in ("LA_COMMON", "T50", "T51", "T53"):
        out += [p for p in glob.glob(os.path.join(FAM, d, "*.py"))]
    return out


def test_sqlglot_reads_every_statement_kind_like_the_spec():
    for kind in ("select", "insert", "update", "delete", "drop", "truncate", "alter", "grant", "ctas"):
        for pred in (True, False):
            st = SqlStmt(kind, "tbl_a", has_predicate=pred)
            info = v.sql_info(st.text())
            assert v.sql_matches(st, info), (kind, pred, info)


def test_availability_is_reported_honestly():
    a = v.availability()
    assert set(a) == {"tree_sitter_bash", "mvdan_sh_shfmt", "sqlglot"} and a["sqlglot"] is True
    if not a["tree_sitter_bash"]:
        assert v.tree_sitter_shape("git status") is None
    if not a["mvdan_sh_shfmt"]:
        assert v.mvdan_shape("git status") is None
        assert v.shapes_agree(shape("git status"), None) is None


def test_shape_agreement_logic_on_synthetic_validator_output():
    mine = shape("git 'push' --force $V")
    good = [{"name": "git", "args": ["'push'", "--force", "$V"]}]
    assert v.shapes_agree(mine, good) is True
    assert v.shapes_agree(mine, [{"name": "git", "args": ["push", "--force", "$V"]}]) is False


@pytest.mark.skipif(not v.tree_sitter_available(), reason="tree-sitter-bash not installed on this Mac (checked 18 Oct 2026)")
def test_tree_sitter_agrees_with_our_shape():
    for text in ["git push origin main", "T=/a; rm -rf $T", "echo hi | sh", "rm -f /srv/{a,b}.log && git status"]:
        assert v.shapes_agree(shape(text), v.tree_sitter_shape(text)) is True


@pytest.mark.skipif(not v.shfmt_available(), reason="shfmt (mvdan/sh) not installed on this Mac (checked 18 Oct 2026)")
def test_mvdan_agrees_with_our_shape():
    for text in ["git push origin main", "T=/a; rm -rf $T", "echo hi | sh"]:
        assert v.shapes_agree(shape(text), v.mvdan_shape(text)) is True


def test_k16_no_execution_scan_is_clean_on_all_lane_code():
    files = [p for p in _code_files() if "/tests/" not in p]
    r = g50.k16_scan(files)
    assert r["pass"], r["violations"]
    assert r["files"] >= 25


def test_k16_scan_has_power(tmp_path):
    bad = tmp_path / "bad.py"
    bad.write_text("import subprocess, shlex\nsubprocess.run(['sh', '-c', x], shell=True)\neval(x)\nos.system(y)\n")
    r = g50.k16_scan([str(bad)])
    assert not r["pass"] and len(r["violations"]) >= 4
    ok = tmp_path / "validators.py"
    ok.write_text("import subprocess\nsubprocess.run(['shfmt'], input=b'', shell=False)\n")
    assert g50.k16_scan([str(ok)])["pass"]
    no = tmp_path / "validators.py"
    no.write_text("import subprocess\nsubprocess.run(['shfmt'], input=b'')\n")
    assert not g50.k16_scan([str(no)])["pass"]


CONTROL_FLOW_TEXTS = ["until git fetch origin; do git status; done", "if git diff --quiet; then git push origin x1; fi",
                      "for f in /srv/a/x.log /srv/a/y.log; do rm -f \"$f\"; done", "ls && (cd /srv/a && git status)"]


def test_control_flow_markers_compare_like_for_like_on_synthetic_validator_output():
    for text in CONTROL_FLOW_TEXTS:
        mine = shape(text)
        assert any(s.get("opaque") == "control_flow" for s in mine)
        theirs = [{"name": s["name"], "args": s["args"]} if "name" in s else s for s in mine]
        assert v.shapes_agree(mine, theirs) is True
        # a validator that lists the body commands instead of one marker, or a parse error, never agrees
        assert v.shapes_agree(mine, [{"name": "git", "args": ["status"]}]) is False
        assert v.shapes_agree(mine, v.PARSE_ERROR) is False
    assert v.shapes_agree(shape("git status"), [{"opaque": "control_flow"}]) is False


@pytest.mark.skipif(not v.tree_sitter_available(), reason="tree-sitter-bash not installed on this Mac (checked 18 Oct 2026)")
def test_tree_sitter_agrees_on_control_flow_and_flags_syntax_errors():
    for text in CONTROL_FLOW_TEXTS:
        assert v.shapes_agree(shape(text), v.tree_sitter_shape(text)) is True, text
    assert v.shapes_agree(shape("git push origin main"), v.tree_sitter_shape("if then fi ((")) is False
