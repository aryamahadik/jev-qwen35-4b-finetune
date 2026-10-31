"""families/T43/texts.py: the fixed program text of T43 rows (rules, question wordings, option wording, layouts).

Rules are printed in `instructions` (counted twice by the 800-token budget), so they are short. The wordings carry no
digit, no label word (see LABEL_WORDS in plugin.py) and no name other than "Python".
"""
DOC = ("Python 3.12. A docstring `Equals <expr>.` is that function's exact intended result; a function named in an "
       "expression stands for its own docstring. ")
RULES = {
    "loc_line": DOC + "Exactly one numbered line differs from a version that matches every docstring. Answer with that line.",
    "loc_line_n": DOC + "At most one numbered line differs from a version that matches every docstring. Answer with that line, "
                        "or none when the code already matches.",
    "loc_func": DOC + "Exactly one function differs from a version that matches every docstring. Answer with that function.",
    "loc_func_n": DOC + "At most one function differs from a version that matches every docstring. Answer with that function, "
                        "or none when the code already matches.",
    "pv": DOC + "The patch is a unified diff. After it, run the tests and compare every function with its "
                "docstring on all inputs. Fixes: tests pass, no function differs. Does not fix: a test fails. Passes the "
                "target test but wrong: tests pass, yet a function differs.",
    "pv_d": DOC + "The patch is a unified diff; it applies only if every hunk's context and removed lines equal "
                  "the file at the stated line number (no offset). If it applies, run the tests and compare every function with "
                  "its docstring on all inputs. Fixes: tests pass, no function differs. Does not fix: a test fails. "
                  "Passes the target test but wrong: tests pass, yet a function differs.",
}
WORDINGS = {
    "loc_line": ("Which numbered line holds the bug?", "Which numbered line has to change so that the tests are green?",
                 "Name the numbered line that deviates from its docstring."),
    "loc_line_n": ("Which numbered line holds the bug, if any?", "Which numbered line has to change so that the tests are green, if any?",
                   "Name the numbered line that deviates from its docstring, if there is such a line."),
    "loc_func": ("Which function holds the bug?", "Which function has to change so that the tests are green?",
                 "Name the function that deviates from its docstring."),
    "loc_func_n": ("Which function holds the bug, if any?", "Which function has to change so that the tests are green, if any?",
                   "Name the function that deviates from its docstring, if there is such a function."),
    "pv": ("Judge the patch below.", "How does the patch below behave on the code above?", "What does the patch below do to the program?"),
    "pv_d": ("Judge the patch below, including whether it can be used on this file.",
             "How does the patch below behave on the code above, if it can be used at all?",
             "What does the patch below do to the program, if anything?"),
}
QUESTION_MEANINGS = {
    "loc_line": "asks which numbered line of the code deviates from its docstring",
    "loc_line_n": "asks which numbered line of the code deviates from its docstring, or none when no line does",
    "loc_func": "asks which function of the module deviates from its docstring",
    "loc_func_n": "asks which function of the module deviates from its docstring, or none when no function does",
    "pv": "asks how a unified-diff patch that applies behaves: it repairs the code, leaves a test failing, or passes the tests but leaves wrong behaviour",
    "pv_d": "asks how a unified-diff patch behaves, including that it may not apply to the shown file",
}
OPT = {"A": "fixes the bug", "B": "does not fix the bug", "C": "passes the target test but is still wrong", "D": "does not apply"}
NONE_TEXT = {"ll": "none: no line differs", "lf": "none: no function differs"}
TITLES = {"code": "Source", "tests": "Tests", "run": "Test run", "patch": "Patch"}
FILE = "module.py"
