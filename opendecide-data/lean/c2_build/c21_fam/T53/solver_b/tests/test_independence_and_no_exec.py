"""Solver B must not import any solver-A / shared-expander module, and must never execute a rendered string (K16)."""
import ast
import os

_B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_FAM_ROOT = os.path.dirname(os.path.dirname(_B))
_FORBIDDEN_IMPORTS = ("T50.solver_a", "T50.rules", "T50.verdict", "T50.build", "T50.generator", "T50.intents",
                      "T53.engine", "T53.destination", "T53.generator", "T53.registry", "T51.model", "T51.generator",
                      "LA_COMMON", "tool_engine", "GEN", "shlex", "bashlex", "subprocess", "socket", "urllib.request",
                      "http", "requests")
_FORBIDDEN_CALLS = ("eval", "exec", "system", "popen", "Popen", "run", "call", "check_output", "spawn")
# the harness modules (agree.py, run_all.py) legitimately import the lane generator; they are not solver B proper
_HARNESS = ("agree.py", "run_all.py")


def _b_modules():
    out = []
    for root, dirs, files in os.walk(_B):
        dirs[:] = [d for d in dirs if d not in ("tests", "__pycache__")]
        for fn in files:
            if fn.endswith(".py") and fn not in _HARNESS and fn != "__init__.py":
                out.append(os.path.join(root, fn))
    # solver B of T50 / T53 also uses each other's shared B modules: scan those too
    return out


def test_no_solver_a_or_shared_expander_imports():
    for p in _b_modules():
        tree = ast.parse(open(p).read())
        for n in ast.walk(tree):
            names = []
            if isinstance(n, ast.Import):
                names = [a.name for a in n.names]
            elif isinstance(n, ast.ImportFrom):
                names = [(n.module or "")]
            for nm in names:
                for bad in _FORBIDDEN_IMPORTS:
                    assert not (nm == bad or nm.startswith(bad + ".")), (p, nm)


def test_no_execution_calls():
    for p in _b_modules():
        tree = ast.parse(open(p).read())
        for n in ast.walk(tree):
            if isinstance(n, ast.Call):
                f = n.func
                nm = f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else "")
                assert nm not in _FORBIDDEN_CALLS, (p, nm, n.lineno)
