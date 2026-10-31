"""families/T44/texts.py: fixed program text of T44 SEQ-CHECK rows (rules, wordings, algebra-block layouts, section
headers). Plain constants shared by the renderer (plugin.py) and the independent parser (solver_b.py). The semantics
(what a label means) live in G0_SPEC.md.

Rules sit in `instructions` (counted twice by the 800-token budget), so they are short. Wordings are the question forms
of the lexicon (G-LEX admission); they carry no label word. Label words (G-SL): invalid, valid, applicable, reached.
"""
import re

HEAD_VERDICT, HEAD_NEXT = "ch_verdict", "ch_next"
V_INVALID, V_GOAL, V_VALID = "INVALID", "GOAL_NOT_REACHED", "VALID"
V_STEP = "STEP_{k}_NOT_APPLICABLE"
STEP_RE = re.compile(r"STEP_(\d+)_NOT_APPLICABLE")
VERDICT_BASE = (V_INVALID, V_GOAL, V_VALID)

_CORE = ("A tool line lists what a call needs (needs, requires, when, pre), adds (adds, gives, gains, add) and removes "
         "(removes, drops, clears, loses, del). A call runs only if every needed fact is true and every needed `not` "
         "fact is false; it then removes its removed facts and adds its added facts. Other facts keep their value. "
         "Only the Start facts are true at first.")
RULES = {
    HEAD_VERDICT: (_CORE + " Check the plan in order. INVALID: a step names an unlisted tool, has the wrong number of "
                   "arguments, or has an argument that is not an object of the parameter's type. Else "
                   "STEP_k_NOT_APPLICABLE: step k is the first whose needs fail (the plan stops there). Else "
                   "GOAL_NOT_REACHED: every step runs but the Goal does not hold at the end. Else VALID."),
    HEAD_NEXT: (_CORE + " The calls so far all ran in order. Choose the call that is applicable now and starts a "
                "shortest sequence of calls that makes the whole Goal true."),
}
WORDINGS = {
    HEAD_VERDICT: ("Which verdict fits this plan?",
                   "What happens when this plan is run?",
                   "How does this plan fare against the goal?",
                   "Which option describes the outcome of running the plan?"),
    HEAD_NEXT: ("Which call starts a shortest route to the goal?",
                "What is the best call to make from here?",
                "Which of these calls should the agent make from this state?",
                "Which option begins a shortest way to the goal?"),
}
QUESTION_MEANINGS = {
    HEAD_VERDICT: "asks whether a plan is malformed, fails at some step, runs but misses the goal, or works",
    HEAD_NEXT: "asks which listed call can come next on a shortest sequence of calls that reaches the goal",
}
LABEL_WORDS = ("invalid", "valid", "applicable", "reached")

# section headers (each alone at the start of its line / block)
H_TOOLS, H_OBJECTS, H_START, H_GOAL = "Tools:", "Objects:", "Start:", "Goal:"
H_PLAN, H_CALLS = "Plan:", "Calls so far:"
NOTHING, NONE_YET = "(nothing)", "(none)"

# algebra-block layouts (registers): how each tool is written. A tool entry is
#   PREFIX + signature + SIG_SEP + clauses; a clause is LABEL + " " + items joined by ITEM_SEP; clauses are joined by
#   CLAUSE_SEP; an empty clause is left out; the entry may end with SUFFIX. multiline: CLAUSE_SEP starts a new line.
REGISTERS = {
    "semi":     dict(prefix="- ", sig_sep=": ", labels=("needs", "adds", "removes"), clause_sep="; ", item_sep=", ", suffix=""),
    "dash":     dict(prefix="", sig_sep=" -- ", labels=("requires", "gives", "drops"), clause_sep=" | ", item_sep=", ", suffix=""),
    "lines":    dict(prefix="", sig_sep=":", labels=("needs", "adds", "removes"), clause_sep="\n  ", item_sep=", ", suffix=""),
    "when":     dict(prefix="* ", sig_sep=" ", labels=("when", "gives", "clears"), clause_sep=", then ", item_sep=", ", suffix=""),
    "bracket":  dict(prefix="[tool] ", sig_sep=" ", labels=("pre:", "add:", "del:"), clause_sep=" ", item_sep=", ", suffix=""),
    "numbered": dict(prefix="{i}) ", sig_sep=" : ", labels=("needs", "adds", "drops"), clause_sep=" / ", item_sep=", ", suffix=""),
    "pipes":    dict(prefix="| ", sig_sep=" | ", labels=("needs", "adds", "removes"), clause_sep=" | ", item_sep=", ", suffix=" |"),
    "hoare":    dict(prefix="", sig_sep=" ~ ", labels=("pre", "gains", "loses"), clause_sep=" ; ", item_sep=" & ", suffix=""),
    "colon":    dict(prefix="", sig_sep=" :: ", labels=("requires", "gains", "loses"), clause_sep=" || ", item_sep=", ", suffix=""),
}
TRAIN_REGISTERS = ("semi", "dash", "lines", "when", "bracket", "numbered", "pipes")
HELD_OUT_REGISTERS = ("hoare", "colon")
LABEL_TOKENS = sorted({w for r in REGISTERS.values() for w in r["labels"]})
