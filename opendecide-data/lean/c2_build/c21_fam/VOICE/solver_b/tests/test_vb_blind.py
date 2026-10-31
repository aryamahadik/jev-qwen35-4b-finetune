"""CT-V-G1-no-llm / blind: solver B imports nothing from solver A and is stdlib-only; no network, no subprocess, no file writes."""
import ast
import os
import sys

B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCAL = {"vb_tables", "vb_numbers", "vb_denorm", "vb_hyp", "vb_check", "vb_wer"}
BANNED_STDLIB = {"subprocess", "socket", "urllib", "http", "requests", "shutil", "os", "pathlib"}


def test_imports_are_stdlib_or_b_local_and_harmless():
    for fn in sorted(f for f in os.listdir(B) if f.endswith(".py")):
        tree = ast.parse(open(os.path.join(B, fn)).read())
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            for n in names:
                root = n.split(".")[0]
                assert root in sys.stdlib_module_names or root in LOCAL, "%s imports %s" % (fn, n)
                assert root not in BANNED_STDLIB, "%s imports %s" % (fn, n)


def test_no_file_writes_or_calls_to_exec():
    for fn in sorted(f for f in os.listdir(B) if f.endswith(".py")):
        src = open(os.path.join(B, fn)).read()
        for bad in ("open(", "exec(", "eval(", "__import__"):
            assert bad not in src, "%s uses %s" % (fn, bad)
