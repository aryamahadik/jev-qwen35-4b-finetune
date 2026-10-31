"""Uniform adapter over the four own evaluators so the family solvers are language-agnostic.

  program(lang, files)  -> Program with .fresh(fn) -> instance|None ; .invoke(inst, fn, args) -> ('ok', plain) | ('exc', name)
  run_tests(lang, files, only=None, mode=...) -> {'outcomes': {id: outcome}, 'exit': int, 'collected': n}
Every function raises common.Unsupported / common.Timeout when the rendered text is outside the modelled subset.
"""
from .common import Budget, Unsupported


def program(lang, files, budget=None):
    if lang == "python":
        from .pyeval import PyProgram
        return PyProgram(files, budget)
    if lang in ("javascript", "typescript"):
        from .jseval import JsProgram
        return JsProgram(files, budget)
    if lang == "go":
        from .goeval import GoProgram
        return GoProgram(files, budget)
    if lang == "bash":
        from .sheval import ShProgram
        return ShProgram(files, budget)
    raise Unsupported("language " + lang)


def run_tests(lang, files, only=None, mode="native", budget=None):
    """mode 'native': the language-native runner as the agent would run it (pytest / node --test / go test / bash runner).
    mode 'plain' (python only): import and call every test_* function (the T42c TFAIL2 harness)."""
    if lang == "python":
        from .pyeval import run_python_tests
        return run_python_tests(files, "plain" if mode == "plain" else "pytest", only, budget)
    if lang in ("javascript", "typescript"):
        from .jseval import run_js_tests
        return run_js_tests(files, only, budget)
    if lang == "go":
        from .goeval import run_go_tests
        return run_go_tests(files, only, budget)
    if lang == "bash":
        from .sheval import run_sh_tests
        return run_sh_tests(files, only, budget)
    raise Unsupported("language " + lang)


def is_test_path(lang, path):
    base = path.rsplit("/", 1)[-1]
    if lang == "python":
        return base.startswith("test_") and base.endswith(".py") or base.endswith("_test.py") or base == "conftest.py"
    if lang in ("javascript", "typescript"):
        return ".test." in base
    if lang == "go":
        return base.endswith("_test.go")
    if lang == "bash":
        return base.startswith("test_") and base.endswith(".sh")
    return False
