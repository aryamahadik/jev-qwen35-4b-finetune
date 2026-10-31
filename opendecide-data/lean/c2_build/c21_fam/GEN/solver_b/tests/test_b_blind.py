"""CT-G1-B-blind: solver B imports nothing from solver A, is stdlib-only, and never reads the fields it must not see."""
import ast
import os
import sys

B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCAL = {"bcommon", "b_arith", "b_logic", "b_causal", "b_temporal", "b_table", "b_main", "b_questions"}
FORBIDDEN_KEYS = {"spec", "label_letter", "option_meta", "render_map", "decision_spans", "pair_id", "wording",
                  "difficulty", "trap_type", "pool_sha", "spec_sha"}


def _modules():
    return sorted(f for f in os.listdir(B) if f.endswith(".py"))


def _stdlib(name):
    root = name.split(".")[0]
    return root in sys.stdlib_module_names


def test_imports_are_stdlib_or_b_local():
    for fn in _modules():
        tree = ast.parse(open(os.path.join(B, fn)).read())
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            for n in names:
                root = n.split(".")[0]
                assert _stdlib(n) or root in LOCAL, "%s imports %s" % (fn, n)


def test_no_forbidden_row_fields_are_read():
    for fn in _modules():
        src = open(os.path.join(B, fn)).read()
        tree = ast.parse(src)
        doc_nodes = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef)):
                body = node.body
                if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant) and isinstance(body[0].value.value, str):
                    doc_nodes.add(id(body[0].value))
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in doc_nodes:
                assert node.value not in FORBIDDEN_KEYS, "%s reads %r" % (fn, node.value)


def test_entry_point_reads_only_allowed_fields():
    tree = ast.parse(open(os.path.join(B, "b_main.py")).read())
    keys = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name) and node.value.id == "view" and isinstance(node.slice, ast.Constant):
            keys.add(node.slice.value)
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "get"
                and isinstance(node.func.value, ast.Name) and node.func.value.id == "view" and node.args and isinstance(node.args[0], ast.Constant)):
            keys.add(node.args[0].value)
    assert keys <= {"form", "k", "carrier", "stem", "options"}, keys
    assert {"form", "stem", "options"} <= keys
