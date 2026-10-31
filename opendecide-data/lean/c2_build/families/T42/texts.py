"""families/T42/texts.py: the fixed program text of T42 rows (rules, question wordings, option wording). Plain
constants shared by the renderer and the parser; the semantics (what a label means) live in G0_SPEC.md.

Rules are printed in `instructions` (counted twice by the 800-token budget), so they are short. The wordings are
the question forms of the lexicon (G-LEX admission); they carry no digit, label word or name other than "Python".
"""
RULES = {
    "ch_output": ("Python 3.12, no input, fixed hash seed. Answer with the exact text the program prints, or "
                  "`raises` and the class name (for example `raises KeyError`) when it ends with an uncaught exception."),
    "ch_return": ("Python 3.12, no input, fixed hash seed. Answer with repr(result) exactly as Python shows it, or "
                  "`raises` and the class name (for example `raises KeyError`) when the code ends with an uncaught "
                  "exception."),
    "ch_equiv": ("Python 3.12. Both functions take the arguments their annotations name and return a value or raise. "
                 "Outcomes are equal when both return equal values (and leave the arguments equal) or both raise the "
                 "same class. An ordinary input is a non-empty collection of distinct values or a text of three or "
                 "more letters, with integers above one. An edge input is anything else: an empty, single or "
                 "two-item collection, repeated items, zero, one, negative numbers, a text with capitals, digits or "
                 "spaces. SAME: equal outcomes on every input. DIFFERS_TYPICAL: the outcomes differ on many ordinary "
                 "inputs. DIFFERS_EDGE: equal on ordinary inputs, different on some edge input."),
}
WORDINGS = {
    "ch_output": ("What does this Python program print when it runs?",
                  "Which output does running this Python program produce?",
                  "Run the program in your head: what is shown on the screen?"),
    "ch_return": ("What value does `result` hold after this Python code has run?",
                  "After the code finishes, which value is stored in `result`?",
                  "What is the final value of `result` in this Python code?"),
    "ch_equiv": ("How do the functions `f` and `g` relate?",
                 "Compare `f` and `g`: which option describes them?",
                 "Which option describes how `g` relates to `f` on the inputs their annotations allow?"),
}
QUESTION_MEANINGS = {
    "ch_output": "asks which text the program prints, or which uncaught exception it raises",
    "ch_return": "asks which value the variable result holds after the code runs, or which uncaught exception it raises",
    "ch_equiv": "asks whether two functions are the same, differ on ordinary inputs, or differ only on edge inputs",
}
LABELS = ("SAME", "DIFFERS_TYPICAL", "DIFFERS_EDGE")
SEPARATOR = "---"
