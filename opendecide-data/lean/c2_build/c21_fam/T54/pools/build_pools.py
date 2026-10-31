"""T54 TOOL-NEED/PICK reword pools (lane L-T). Program expansion of Claude-written parts; drop-only Haiku-style
round trip against the seed template of each form (slot set, numbers, negation count). No labels, no gold, no
benchmark text; entity/field/value names enter only through {slot} placeholders filled from namespace.py.

Run: python3 build_pools.py   (writes wording_pool_v1.json and pool_manifest.json next to this file)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FAM = os.path.dirname(HERE)
ROOT = os.path.dirname(FAM)
for p in (ROOT, FAM):
    if p not in sys.path:
        sys.path.insert(0, p)

from tool_engine import wording_expand as X  # noqa: E402
import t54_wording as SEEDS  # noqa: E402

REQ_PREFIX = ["", "Thanks. ", "Okay. ", "Quick question. ", "Right. ", "Hello. ", "One more thing. "]
Q_PREFIX = ["", "Given this turn, ", "In this turn, ", "Looking at the context, ", "Based on the turn so far, ",
            "At this point, ", "Considering the conversation, "]

# ---- option texts (one form per label). Parts are alternatives joined by single spaces. ----
OPT = {
    "CALL": [
        [["Call", "Make the call to", "Run", "Issue a call to"], ["the listed tool", "the tool from the list", "the matching listed tool"],
         ["with the values given", "using the values given", "with the values supplied"]],
        [["Make", "Place"], ["the tool call now", "the listed call now"],
         [", all values are available", ", every value is on hand", ", every value is available", "; all the values are in place"]],
    ],
    "ASK": [
        [["Ask", "Prompt", "Query"], [" the user", " the person", " the user directly"],
         [" for the missing value", " for the value that is missing", " for the value still missing"]],
        [["Stop and ask", "Pause and ask", "Halt and ask"], [" the user", " the user or a reviewer"],
         [" for the value that is missing", " for the missing value"]],
        [["Stop", "Pause", "Halt"], [" here and ask", " and request"], [" the user", " the user directly"], [" for the missing value"]],
    ],
    "NO_TOOL": [
        [["Say", "State", "Report"], [" that no listed tool", " that none of the listed tools"],
         [" can do this", " is able to do this", " can handle this"]],
        [["Tell the user", "Let the user know", "Inform the user"], [" the listed tools", " the available tools"],
         [" cannot do this", " cannot handle this", " cannot carry this out"]],
        [["Explain", "Report"], [" that the listed tools", " that the tool list"], [" does not cover this", " does not handle this"]],
        [["Say", "State", "Report"], [" that no listed tool fits this request", " that no listed tool matches this request"],
         [", so nothing is called"]],
    ],
    "ANSWER": [
        [["Answer", "Reply", "Respond"], [" directly", " straight away", " from the context"],
         [", no tool is needed", ", and no tool is needed", " with no tool needed"]],
        [["Reply", "Answer"], [" from what is already stated", " from the stated facts", " from what the conversation already holds"],
         [", without a tool", ", without any tool call", ", without calling a tool"]],
        [["Give the answer now", "Answer now", "Respond now"], [", using what the conversation holds", ", using only the stated facts"],
         [" and make no call", " with no call made"]],
    ],
    "RESULT_MISSING": [
        [["Say", "State", "Report"], [" the earlier result is missing", " the earlier result is absent", " the earlier output is missing"],
         [" and do not guess the value", " and do not guess that value", " and do not fill in the value"]],
        [["Report", "Say", "State"], [" that the earlier result never arrived", " that the earlier output never came back"],
         [", so the value is unknown", ", so the value stays unknown", ", so the value is still unknown"]],
        [["Explain", "Tell the user"], [" that the earlier result is missing, so"],
         [" the value must not be guessed", " the value must not be made up", " the value is not to be guessed"]],
    ],
    "WRITE": [
        [["Make", "Issue", "Send", "Place"], [" the write call", " the write request", " the write"], [" now", " straight away", " at once"]],
        [["Perform", "Execute"], [" the write call", " the write step"], [" now", " immediately", " right away"]],
        [["Make", "Issue"], [" one write call"], [" now, before anything else"]],
    ],
    "READ_FIRST": [
        [["Read", "Check", "Look at", "Inspect"], [" the current state", " the present state", " the state as it stands"],
         [" first", " before anything else"]],
        [["Call", "Run", "Make"], [" a read tool", " a read call", " a listing or read tool"],
         [" first", " before the write", " to see the current state"]],
    ],
    "DONE_NO_CALL": [
        [["Make no call", "Send no call", "Issue no call"], [", the wanted state already holds", ", the state you want is already in place",
                                                              ", the wanted state is already present"]],
        [["No call is needed", "No call is required", "No write is needed"],
         [", the state is already as wanted", ", the state already matches what is wanted", ", the wanted state already holds"]],
        [["Make no write", "Issue no write"], [", the wanted state is already established", ", the state is already set", ", the state already matches"],
         [" and leave it as it is", ""]],
        [["The write is not needed", "A call is not needed", "The call is not needed"],
         [", since the wanted state already holds", ", because the state is already as wanted"],
         [", so the state stays as it is", ", so it is left as it is"]],
        [["Leave it: no write is needed", "Leave it: no call is needed"], [", the wanted state already holds", ", the state is already as wanted"],
         [" and say so", ""]],
    ],
    "GROUNDED": [
        [["Every value", "All values", "Each value"], [" in the call", " in the proposed call", " in the call as proposed"],
         [" is grounded in the conversation", " has a source in the conversation", " traces back to the conversation"]],
        [["All supplied values", "Every supplied value"], [" have a source in the conversation", " are grounded in the conversation",
                                                          " come from the conversation"]],
        [["The call is grounded", "The proposed call is grounded"], [" throughout", " in every value"],
         [", since each value comes from the conversation", ", because every value has a source"]],
        [["Each argument", "Every argument"], [" is backed by the conversation", " has a source in the conversation"],
         [", so the call is grounded", ", so nothing is made up", ", so the call stands"]],
    ],
    "UNGROUNDED": [
        [["At least one value", "One value", "Some value"], [" in the call has no grounding", " in the call has no source"],
         [" in the conversation", " anywhere in the conversation", ""]],
        [["Some supplied value", "At least one supplied value"], [" has no source in the conversation", " has no grounding in the conversation"],
         [", so the call is ungrounded", ", so the call stands ungrounded", ", so the call is grounded in part only"]],
        [["Some", "One"], [" supplied value in the call has no source"], [" in the conversation", " anywhere in the conversation", " in the transcript"],
         [", so the call is ungrounded", ", so the call stands ungrounded"]],
        [["At least one value", "One value", "A value"], [" in the call is not grounded in the conversation"],
         [", so the call is ungrounded", ", so the call stands ungrounded", " and so the call is ungrounded"]],
    ],
}

# ---- card texts (policy sentences; negation counts are matched to the seed template) ----
CARD = {
    "strict_ask": [
        [["Tool-use policy:", "Policy:", "Tool rule:", "Calling rule:", "Rule for tool use:", "Tool policy:", "Policy for tools:"],
         ["when a required value was not given and cannot be found in the conversation, ask for it.",
          "when a required value is not given and cannot be found in the conversation, it must be asked for."],
         ["Never fill a value in yourself, even when the tool lists a default.", "Never fill in a value yourself, even if the tool lists a default."],
         [" Asking beats guessing.", " Guessing is out of bounds.", ""]],
    ],
    "defaults_ok": [
        [["Tool-use policy:", "Policy:", "Tool rule:", "Calling rule:", "Rule for tool use:", "Tool policy:", "Policy for tools:"],
         ["when a required value was not given but the tool lists a default for it, use the default.",
          "when a required value is not given but the tool lists a default for it, the default is used."],
         ["When there is no default and no source, ask.", "With no default and no source, ask."],
         [" The default is the fallback.", " Defaults are a fallback only.", ""]],
    ],
    "read_before_write": [
        [["Write policy:", "Policy for writes:", "Write rule:", "Rule for writes:", "Writes policy:"],
         ["a write marked idempotent may be issued without reading first.", "a write marked idempotent may go ahead without a prior read."],
         ["Any other write whose current state is unknown must be preceded by a read, when a read tool is listed;",
          "Any other write with an unknown current state needs a read first, when a read tool is listed;"],
         ["with no read tool, ask.", "with no read tool available, ask."],
         [" A state already shown to hold needs no write.", " A state already shown to hold means no write is needed."]],
    ],
    "parallel_ok": [
        [["Batching policy:", "Policy for batching:", "Batching rule:", "Rule for grouping calls:", "Batch rule:"],
         ["calls that do not use each other's output may be issued together in one step.",
          "calls that have no use for each other's output may go out together in one step."],
         [" A call that needs another call's output waits for it.", " A call that depends on another call's output waits for that output.",
          " A call whose arguments come from another call's output waits for that output."],
         ["", " Independent calls go out together.", " Dependent calls wait their turn."]],
    ],
}

# ---- question forms ----
QCORE = {
    "s1_need4": ["What should the agent do next?", "Which is the right next move for the agent?", "What is the agent's next move?",
                 "What must the agent do next?", "What step should the agent take next?", "Which action comes next for the agent?",
                 "What is the right next step for the agent?", "What should the agent do now?", "Which move should the agent make next?"],
    "s2_pick": ["Which listed tool, with its arguments, is the right call?", "Pick the call that fits the request.",
                "Which listed tool and argument set fits the request?", "Which listed tool, with its arguments, fits the request?",
                "Which of the listed calls is the right one?", "Which listed call fits what was asked?",
                "Which listed tool should be called, with these arguments?", "Pick the listed call that fits the request."],
    "s4_precond": ["Is the write needed, given what is known?", "Given what is known, is the write needed?",
                   "Does the known state call for a write?", "Is a write needed, given the known state?",
                   "Given the known state, does a write need to happen?", "Is the write still needed, given what is known?",
                   "What does the known state say about the write?", "Should the write go ahead, given what is known?"],
    "s5_argground": ["Is every value in the proposed call grounded in the conversation?",
                     "Are all the values in the proposed call grounded in the conversation?",
                     "Does every value in the proposed call come from the conversation?",
                     "Is each value in the proposed call backed by the conversation?",
                     "Do all values in the proposed call come from the conversation?",
                     "Is every supplied value in the proposed call grounded in the conversation?",
                     "Does each value in this call have a source in the conversation?",
                     "Is each value in the proposed call traceable to the conversation?"],
    "s6_parseq": ["Which set of calls may be issued together in the next step?", "Which calls are ready to go out together now?",
                  "Which group of calls can go out together in the next step?", "Which calls may be sent together at the next step?",
                  "Which set of calls is ready to issue together now?", "Which calls can be made together in the next step?",
                  "Which bundle of calls may go out together next?", "Which calls can be issued at once in the next step?"],
}

QCORE["s3_limit"] = QCORE["s1_need4"]  # same question as S1 after a deletion (G0-lite section 1)

# ---- request / user-turn forms ----
REQ = {
    "act": ["Please {action} the {entity}{clauses}.", "I need to {action} the {entity}{clauses}.", "Could you {action} the {entity}{clauses}?",
            "Would you {action} the {entity}{clauses} for me?", "I would like you to {action} the {entity}{clauses}.",
            "Kindly {action} the {entity}{clauses}.", "Can you {action} the {entity}{clauses}, please?",
            "Go ahead and {action} the {entity}{clauses}."],
    "fetch": ["What is the {field} of the {entity}{refpart}{clauses}?", "Which {field} does the {entity}{refpart} have{clauses}?",
              "What {field} does the {entity}{refpart} have{clauses}?", "Tell me the {field} of the {entity}{refpart}{clauses}.",
              "Can you tell me the {field} of the {entity}{refpart}{clauses}?", "I need the {field} of the {entity}{refpart}{clauses}.",
              "Please give me the {field} of the {entity}{refpart}{clauses}.", "What is the {field} for the {entity}{refpart}{clauses}?"],
    "fetch_ref": ["What is the {field} of the same {entity} as before{clauses}?", "Which {field} does the same {entity} as before have{clauses}?",
                  "What {field} does the same {entity} as before have{clauses}?", "Tell me the {field} of the same {entity} as before{clauses}.",
                  "Can you tell me the {field} of the same {entity} as before{clauses}?", "I need the {field} of the same {entity} as before{clauses}.",
                  "Please give me the {field} of the same {entity} as before{clauses}.", "What is the {field} for the same {entity} as before{clauses}?"],
    "info": ["Which {field} did I give for that {entity}?", "What {field} did I say that {entity} has?",
             "Which {field} did I mention for that {entity}?", "What {field} did I tell you that {entity} has?",
             "Do you remember which {field} I gave for that {entity}?", "Which {field} was it that I gave for that {entity}?",
             "Can you recall the {field} I gave for that {entity}?", "What {field} did I set for that {entity} earlier?"],
    "info_card": ["What is the default {field} for the {entity}?", "Which default {field} applies to the {entity}?",
                  "What default {field} does the {entity} use?", "Which default {field} is set for the {entity}?",
                  "Tell me the default {field} for the {entity}.", "Can you tell me the default {field} for the {entity}?",
                  "What is the standard {field} for a {entity}?", "Which default {field} does a {entity} get?"],
    "reference": ["Now {action} the {entity}{clauses}, using the same {pname} as before.",
                  "Now {action} the {entity}{clauses}, with the same {pname} as before.",
                  "Next, {action} the {entity}{clauses}, keeping the same {pname} as earlier.",
                  "Once more, {action} the {entity}{clauses}, with the {pname} we used before.",
                  "Repeat the step: {action} the {entity}{clauses}, with the same {pname} as before.",
                  "Now go ahead and {action} the {entity}{clauses}, reusing the same {pname}.",
                  "Please {action} the {entity}{clauses} again, with the same {pname} as before.",
                  "Now {action} the {entity}{clauses} once more, with the same {pname} as last time."],
    "state_write": ["Make sure the {entity} {ref} ends up with {pname} {value}.", "I want the {entity} {ref} to have {pname} {value}.",
                    "Make sure the {entity} {ref} is set to {pname} {value}.", "I want the {entity} {ref} to end up with {pname} {value}.",
                    "Check that the {entity} {ref} ends up with {pname} {value}.", "I need the {entity} {ref} to have {pname} {value}.",
                    "Please make the {entity} {ref} carry {pname} {value}.", "See that the {entity} {ref} ends up with {pname} {value}."],
    "plan": ["Do the following: {steps}.", "Carry out these steps: {steps}.", "Work through these steps in order: {steps}.",
             "Here are the steps, in order: {steps}.", "Complete the steps listed here: {steps}.", "Follow these steps: {steps}.",
             "Please do these steps: {steps}.", "Run through the following steps: {steps}."],
}
FACT = ["For the record, the {entity} {ref} has {field} {value}.", "Note that the {entity} {ref} carries {field} {value}.",
        "For your notes, the {entity} {ref} has {field} {value}.", "Just so you know, the {entity} {ref} carries {field} {value}.",
        "Be aware that the {entity} {ref} has {field} {value}.", "It is on record that the {entity} {ref} has {field} {value}.",
        "The {entity} {ref} is recorded with {field} {value}.", "Our records show the {entity} {ref} with {field} {value}."]
FACT_PREFIX = ["", "Context: ", "Background: ", "Noted: ", "Recap: ", "Log: ", "Memo: "]
CARDNOTE = ["Card note: the default {field} for a {entity} is {value}.", "Default: {field} of a {entity} is {value}.",
            "Card note: a {entity} has the default {field} {value}.", "Card note: the default {field} of a {entity} is {value}.",
            "Default for a {entity}: {field} is {value}.", "Note on the card: the default {field} for a {entity} is {value}.",
            "Card line: the default {field} for a {entity} is {value}.", "Default setting: {field} of a {entity} is {value}."]
CARDNOTE_PREFIX = ["", "Reminder. ", "Policy line. ", "Config. ", "Note. ", "Setup. ", "Summary. "]


def candidates_for(form):
    kind, _, key = form.partition(".")
    if form.startswith("opt."):
        return list(X.expand_parts(OPT[form[4:]]))
    if form.startswith("card.card.t54."):
        return list(X.expand_parts(CARD[form[len("card.card.t54."):]]))
    if form.startswith("q."):
        return list(X.expand_prefix_core(Q_PREFIX, QCORE[form[2:]]))
    if form.startswith("req."):
        return list(X.expand_prefix_core(REQ_PREFIX, REQ[form[4:]]))
    if form == "fact.text":
        return list(X.expand_prefix_core(FACT_PREFIX, FACT))
    if form == "card.note":
        return list(X.expand_prefix_core(CARDNOTE_PREFIX, CARDNOTE))
    raise KeyError(form)


def main():
    seed_pools = SEEDS.seed_pool().pools
    out, stats = {}, {}
    for form in sorted(seed_pools):
        seed0 = seed_pools[form][0]
        kept, st = X.build_form(seed0, candidates_for(form), form)
        out[form] = kept
        stats[form] = st
    with open(os.path.join(HERE, "wording_pool_v1.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    manifest = {
        "family": "T54", "pool": "wording_pool_v1", "forms": len(out),
        "min_per_form": min(len(v) for v in out.values()), "total_wordings": sum(len(v) for v in out.values()),
        "pool_sha256": X.pool_sha(out), "seed_module": "T54/t54_wording.py",
        "round_trip": "tool_engine.wording.reword_ok against the seed0 of each form; drop-only",
        "per_form": {k: {"count": len(out[k]), **stats[k]} for k in sorted(out)},
    }
    with open(os.path.join(HERE, "pool_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    print("forms", len(out), "min", manifest["min_per_form"], "total", manifest["total_wordings"], "sha", manifest["pool_sha256"][:16])


if __name__ == "__main__":
    main()
