"""T60 SEED wordings (Claude-authored, a handful per form). The >= 50 wordings per question form AND per card clause (K14) come from the
program expansion in pools/build_pools.py (parts x alternatives, drop-only slot round trip) and are later extended by the Haiku reword pass
(reword only; two-way slot round trip, GV12: numbers, handles, ordinals, statuses, negations and ORDER statements survive verbatim and
nothing decision-bearing is added). Hash the pool at EVERY change (export v1.1). No labels, no gold, no benchmark text; entity, field,
path and step names enter only through {slot} placeholders filled from namespace.py.
"""
from tool_engine.wording import WordingPool

OPTION_TEXT = {
    "DELEGATE": ["Hand the subtask to a separate worker with a brief", "Delegate the subtask to a separate worker"],
    "DO_HERE": ["Do the subtask here in this thread", "Carry out the subtask in the main thread"],
    "KEEP": ["Keep this fact in the summary", "Carry this fact over into the summary"],
    "DROP": ["Drop this fact from the summary", "Leave this fact out of the summary"],
    "PLAN": ["Write out a plan before acting", "Draw up a plan first, then act"],
    "ACT": ["Act now without a plan", "Go ahead and act now, no plan first"],
}
QUESTION = {
    "h1": ["Should the agent hand this subtask to a separate worker, or do it itself in this thread?",
           "Is it better to delegate this subtask to a separate worker, or to do it here in the main thread?"],
    "h2": ["At the context summary, should this fact be kept in the summary or dropped?",
           "When the context is summarised, is this fact kept or dropped?"],
    "h3": ["Should the agent write out a plan before acting, or act now?",
           "Is a plan needed before the agent acts, or can it act now?"],
}
CLAUSE = {
    "d_size": ["Hand a subtask to a separate worker only when ALL four conditions hold. First: it has at least {s} steps or reads at least "
               "{v} tokens in all.",
               "Delegate a subtask only when all four conditions hold. First: it has at least {s} steps, or it reads at least {v} tokens."],
    "d_brief": ["Second: the worker needs at most {b} facts from the main thread.", "Second: no more than {b} facts from the main thread are needed."],
    "d_bound": ["Third: the worker returns at most {r} tokens.", "Third: its result is at most {r} tokens long."],
    "d_free": ["Fourth: it writes no resource the main thread also uses, and it does not depend on a pending main step. Otherwise do it in "
               "this thread.",
               "Fourth: it shares no written resource with the main thread and needs no pending main step. Otherwise do it here."],
    "k_rule": ["Keep a fact in the summary if a step still to run will take it from the conversation context.",
               "A fact belongs in the summary when a step that has not run yet takes it from the conversation context."],
    "k_recover_on": ["Steps that only run if something fails (rollback, retry, read-back) count as steps still to run.",
                     "A step that runs only on failure (rollback, retry, read-back) counts as a step still to run."],
    "k_recover_off": ["Steps that only run if something fails (rollback, retry, read-back) do not count as steps still to run.",
                      "A step that runs only on failure (rollback, retry, read-back) does not count as a step still to run."],
    "p_r1": ["Write a plan first only when ALL three conditions hold. First: some step is high stakes, meaning it cannot be undone, "
             "reaches outside the team, or changes {h} or more {unit_pl}.",
             "Plan before acting only when all three conditions hold. First: some step is high stakes (it cannot be undone, reaches "
             "outside the team, or changes {h} or more {unit_pl})."],
    "p_r2": ["Second: the task has at least {n} steps.", "Second: there are at least {n} steps in the task."],
    "p_r3": ["Third: the request does not say in what order the steps must run. Otherwise act.",
             "Third: the order of the steps is not given in the request. Otherwise act."],
    "title": ["Policy card {title}.", "Card {title}."],
}
TASK = {
    "h1": ["The agent is working on the {entity} {ref}. The main thread holds these facts and has these steps still pending.",
           "The main thread is busy with the {entity} {ref}. It holds the facts below and has pending steps."],
    "h2_task": ["Task: finish the work on the {entity} {ref}.", "The task is to finish the work on the {entity} {ref}."],
    "h3_goal": ["Goal: {verb_phrase}.", "The request: {verb_phrase}."],
}
ORDER = {"line": ["Do step {a} before step {b}.", "Step {a} has to come before step {b}."]}
PLAN_LINE = {"todo": ["[todo] step {sid}: {text}"], "done": ["[done] step {sid}: {text}"]}
QUOTE = ["Fact in question ({where}): {text}", "The fact in question ({where}): {text}"]


def seed_pool():
    p = WordingPool()
    for lab, ts in OPTION_TEXT.items():
        p.add("opt.%s" % lab, ts)
    for k, ts in QUESTION.items():
        p.add("q.%s" % k, ts)
    for k, ts in CLAUSE.items():
        p.add("clause.%s" % k, ts)
    for k, ts in TASK.items():
        p.add("task.%s" % k, ts)
    p.add("order.line", ORDER["line"])
    p.add("quote", QUOTE)
    return p
