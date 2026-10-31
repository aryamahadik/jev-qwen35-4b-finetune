"""T55 RECOVER-ESCALATE reword pools (lane L-T). Program expansion of Claude-written parts; drop-only round trip
against the seed template of each form (slot set, numbers, negation count). No labels, no gold, no benchmark text.
Error vocabulary is this family's own; slots ({quota}, {kc}, {pcap}, ...) are filled from the row record.

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
import t55_wording as SEEDS  # noqa: E402

REQ_PREFIX = ["", "Thanks. ", "Okay. ", "Quick question. ", "Right. ", "Hello. ", "One more thing. "]
Q_PREFIX = ["", "Given this turn, ", "In this turn, ", "Looking at the context, ", "Based on the turn so far, ",
            "At this point, ", "Considering the conversation, "]
CARD_CAP = 120

# ---- option texts ----
OPT = {
    "RETRY": [
        [["Repeat", "Issue", "Send", "Make"], [" the same call", " the identical call", " the same request"], [" again", " once more", ""]],
        [["Issue", "Send"], [" the identical call again", " the same call once more", " the same call one more time"]],
        [["Retry", "Try again with"], [" the same call", " the identical call"], [" as it stands", " exactly as before", " as it was"]],
    ],
    "FIX_ARGS": [
        [["Repeat", "Send", "Make"], [" the call", " the request"],
         [" with corrected arguments", " with the arguments corrected", " with fixed arguments", " with the argument repaired"]],
        [["Correct the argument and call again", "Fix the arguments and call again", "Repair the arguments and call once more"]],
        [["Correct", "Fix", "Repair"], [" the arguments", " the bad argument"], [" and call again", " and make the call again", " and retry the call"]],
        [["Correct the argument", "Fix the argument", "Adjust the argument"], [" and retry the call with corrected values"]],
        [["Correct", "Fix"], [" the arguments"], [" and send the call again", " and repeat the call"]],
    ],
    "SWITCH_TOOL": [
        [["Use", "Switch to", "Choose"], [" a different listed tool", " another listed tool", " an equivalent listed tool"],
         [" for the same goal", " to reach the same goal", " for this goal"]],
        [["Switch to the equivalent listed tool", "Move to the equivalent listed tool", "Call the equivalent listed tool instead"]],
        [["Use", "Try"], [" the other listed tool that fits the goal"], [" instead", " in its place"]],
        [["Use", "Switch to"], [" a listed tool that does the same job"], [" for the goal", " for the same aim"]],
        [["Pick", "Select"], [" a listed alternative"], [" for the same goal", " that serves the same goal", " for this same goal", " to finish the goal"]],
        [["Use", "Switch to"], [" the listed equivalent"], [" for the same goal", " that does the same job", " for the goal"]],
    ],
    "ASK": [
        [["Ask", "Prompt", "Query", "Request input from"], [" the user", " the person", " the user directly"]],
        [["Stop and ask", "Pause and ask", "Halt and ask"], [" the user", " the user or a reviewer", " a human reviewer"]],
        [["Ask", "Refer this to"], [" the user or a reviewer", " a human reviewer", " the user for a decision"]],
        [["Hand the question to"], [" the user", " a reviewer", " the user or a reviewer"]],
        [["Ask", "Pass this to"], [" the user for a decision", " a human reviewer for a decision", " the user or a human reviewer"]],
        [["Stop and ask"], [" the user what to do", " the user how to proceed", " a reviewer what to do", " a reviewer how to proceed"]],
        [["Ask", "Query", "Prompt"], [" the user what to do next", " the user how to proceed", " a human reviewer how to proceed"]],
        [["Ask the user", "Ask a reviewer"], [" before any more calls"]],
    ],
    "STOP": [
        [["Give up on this goal", "Abandon this goal", "Drop this goal"], [" and report", " and report the outcome", " and tell the user"]],
        [["Stop here", "Stop work on this goal", "End this goal"], [" and report", " and say the goal failed", " and state the outcome"]],
        [["Stop", "Halt"], [" the goal here", " the work on this goal"], [" and report that it is unreachable", " and report the failure",
                                                                         " and state that the goal is out of reach"]],
        [["Report that the goal is unreachable", "State that the goal is out of reach", "Say the goal is unreachable"],
         [", then stop", ", and stop", ", and end here"]],
        [["Stop here and report that the goal"], [" cannot be met", " is out of reach"]],
        [["Give up", "Stop", "End the attempt"], [" on this goal", " on the goal"], [" and report", " and tell the user"]],
    ],
    "RETRY_KEYED": [
        [["Repeat", "Resend", "Retry"], [" the write", " the write request"], [" with the same idempotency key", " using the same idempotency key",
                                                                             " under the same idempotency key"]],
        [["Send", "Issue"], [" the same write again", " the identical write again"],
         [", with the same idempotency key", ", using the same key", ", keeping the same idempotency key"]],
        [["Repeat the write, keeping the same idempotency key", "Resend the write under the same idempotency key",
          "Retry the write using the same key"]],
        [["Repeat", "Resend"], [" the write"], [" with its original idempotency key", " with the idempotency key it used before",
                                               " with the same key as the first attempt"]],
        [["Send the same write again", "Send the write again", "Resend the same write"],
         [" with the same key", " under the same key", " with the same idempotency key as before"]],
        [["Repeat the write under its existing key", "Repeat the write with the key already sent"]],
        [["Resend the write with the same key", "Retry the write with its idempotency key"]],
    ],
    "READ_BACK": [
        [["Read", "Check", "Look up", "Fetch"], [" the state back", " the current state back", " the object's state"], [" first", " before anything else", " before any retry"]],
        [["Check whether the write took effect", "Find out whether the write took effect", "Verify whether the write took effect"],
         [" before anything else", " before doing anything else", " first"]],
        [["Read the object back", "Read the state back", "Check the stored state"], [" to see whether the write committed",
                                                                                   " to learn whether the write took effect"]],
    ],
    "RETRY_PLAIN": [
        [["Repeat", "Resend", "Retry"], [" the write", " the write request"], [" as a new attempt", " as a fresh attempt", " as a new call"]],
        [["Send the write again", "Issue the write again"], [" as a fresh call", " as a new call", " as a new attempt"]],
        [["Send", "Issue"], [" the write again"], [" as a fresh call", " as a new request"]],
        [["Write it again", "Repeat the write call"], [" as a new attempt", " as a fresh attempt", " as a new try"]],
        [["Retry the write"], [" as a new call", " as a fresh call", " as a separate new attempt", " as an independent attempt"]],
        [["Send the write again", "Repeat the write"], [" once more as a new attempt", " once more as a fresh call", " once more as a new request"]],
        [["Retry the write", "Resend the write call"], [" as an entirely new attempt", " as an entirely fresh call"]],
        [["Send the write as a new attempt", "Send the write as a fresh call"]],
        [["Retry the write call"], [" as a new call", " as a fresh call"]],
        [["Send it again as a fresh call", "Send it again as a new attempt"]],
    ],
    "NO_RETRY": [
        [["Do not repeat the write", "Do not resend the write", "Do not send the write again"],
         [", the effect is confirmed", ", the effect is confirmed already", ", the effect is confirmed in place"]],
        [["Do not repeat the write", "Do not retry the write"], [", since the effect is already there", ", because the effect is confirmed"],
         [" and leave it", ""]],
        [["Leave the write alone", "Let the write stand"], [", the effect is confirmed"],
         [", and do not repeat it", ", and do not retry it", ", and do not send it again"]],
        [["The effect is confirmed", "The effect is already there"], [", so the write is not repeated", ", so the write is not sent again"]],
        [["Do not repeat the write", "Do not resend the write", "Do not send the write again"],
         [" because the effect is already confirmed", " because the effect is already in place", " because the effect exists already"], [".", ""]],
        [["Do not repeat the write; the effect is confirmed", "Do not repeat it; the effect is already there"]],
        [["Leave it: do not repeat the write", "Leave it: do not retry the write"], [", the effect is confirmed"]],
        [["No repeat is needed; the effect is confirmed", "No repeat is needed, the effect is already there"]],
    ],
    "ACCEPT": [
        [["Use", "Accept", "Keep", "Take"], [" the result", " the returned result", " the output"], [" as it is", " exactly as returned", " as delivered"]],
        [["Accept the result", "Accept the output as delivered", "Accept it as it stands"]],
        [["Take the result as it is", "Keep the result as it is"], [", since it is well formed", ", since it looks right", ", since it checks out"]],
        [["Accept it", "Use it as the answer"], [" as it stands", " as delivered"]],
        [["Carry on with the result as it is"]],
        [["Accept the output", "Accept the returned result"], [" as it is", " as delivered", " exactly as returned"]],
        [["Leave the result alone", "Accept whatever came back"], [" and move on", " and continue"]],
    ],
    "CONTINUE_ALT": [
        [["Continue", "Carry on", "Proceed"], [" by another permitted path", " by a different permitted path", " through another permitted route"]],
        [["Take a different permitted route to the goal", "Take another permitted path to the goal",
          "Choose a different permitted route toward the goal"]],
        [["Continue", "Proceed"], [" toward the goal by another permitted path", " toward the goal by a different allowed path",
                                   " toward the goal another way that is permitted"]],
        [["Use a different permitted path", "Use another permitted route"], [" to reach the goal", " to finish the goal", " for the same goal"]],
        [["Take the other permitted route", "Use the other allowed path"], [" to the goal", " for the goal"], [" and continue"]],
        [["Continue", "Carry on", "Proceed"], [" with a permitted alternative", " with a permitted alternative path", " with an allowed alternative"]],
        [["Choose a permitted alternative and continue", "Pick an allowed alternative and carry on"], [" toward the goal", " to finish the goal"]],
        [["Continue by another permitted path", "Carry on by a different allowed path"], [" when one exists", " when one is available"]],
        [["Take another route that is permitted", "Take a different allowed route"], [" and continue the goal", " and finish the goal"]],
        [["Keep going by another permitted path"]],
    ],
    "ESCALATE": [
        [["Stop acting", "Halt all action", "Pause the work"], [" and ask for a human decision", " and ask a person to decide",
                                                             " and request a human decision"]],
        [["Escalate", "Escalate this"], [" to the user", " to a human reviewer", " to the user for a decision"]],
        [["Stop here", "Stop acting for now"], [" and hand the decision to a person", " and hand the decision to the user",
                                               " and ask a human to decide"]],
        [["Pass the decision to the user", "Pass the decision to a human reviewer"], [" and stop acting", " and pause the work"]],
        [["Ask for a human decision and stop", "Ask a human to decide and stop acting"], [" now", " at this point"]],
        [["Stop acting", "Pause all action"], [", escalate to the user", ", escalate to a human reviewer", ", and escalate the decision"]],
        [["Escalate to the user and stop acting", "Escalate to a human and stop acting", "Escalate the decision and pause the work"]],
        [["Ask a person for a decision", "Ask a human reviewer for a decision", "Request a decision from a person"],
         [" and stop acting", " before doing anything else"]],
        [["Hand this to a person", "Hand this to a human reviewer"], [" for a decision and stop", " to decide and stop acting", " for a decision, then stop"]],
    ],
    "RETRY_SAME": [
        [["Repeat", "Retry"], [" the denied action", " the action that was denied", " the blocked action"]],
        [["Try the denied action again", "Try the blocked action again", "Try the same denied action once more"]],
        [["Send the denied action again", "Send the denied call once more", "Make the denied call again"]],
        [["Repeat", "Retry"], [" the call that was denied", " the same denied call", " the same call that was refused"]],
        [["Repeat the refused action", "Retry the refused action", "Repeat the rejected action"], [" as it stands", " unchanged", " exactly as before"]],
        [["Try the action that was denied again", "Try the call that was refused once more"], [" with the same arguments", " with the same values"]],
        [["Repeat", "Retry", "Re-run"], [" the denied action", " the denied step", " the denied call"], [" as it was", " unchanged", " exactly as first sent"]],
    ],
    "KEEP_POLLING": [
        [["Keep polling", "Continue polling", "Poll again", "Keep checking"],
         [", the repeats are legitimate waiting", ", since repeats are normal while waiting", ", because the repeats are a legitimate wait"]],
        [["Keep polling", "Carry on polling"], [" because the state is still moving", " since the state keeps advancing",
                                                " while the status is still changing"]],
        [["Keep polling the status", "Keep checking the status", "Poll the status again"], [" while the wait is legitimate",
                                                                                          " while the wait is still valid", " until the state changes"]],
        [["Poll again", "Check again", "Keep checking"], [", the wait is legitimate", ", this wait is still legitimate", ", the wait is still valid"]],
        [["Keep polling", "Poll again"], [", the state is advancing", ", progress is still rising", ", the counter is still growing",
                                         ", the status is still changing"]],
        [["Keep polling", "Poll again"], [", since each repeat is a legitimate wait"], [" until the goal completes", " until the state settles"]],
        [["Keep polling"], [" until the state settles", " until the goal is reached"]],
        [["Poll again"], [" until the goal is reached"]],
    ],
    "BREAK_LOOP_ALT": [
        [["Break the loop", "Stop the loop", "End the repetition"], [" and change approach", " and change the approach", " and try another approach"]],
        [["Stop repeating and use another approach", "Stop repeating and switch approach",
          "Stop the repetition and use a different approach"]],
        [["Break the loop", "Stop the loop"], [" and use another approach", " and switch to another method", " and try a different method"]],
        [["Stop repeating the call", "Stop the repeated call"], [" and change approach", " and use another method", " and switch to a different approach"]],
        [["Change approach", "Switch approach", "Change method"], [" and break the loop", " to end the repetition", " to stop the repeats"]],
        [["Stop repeating", "Break out of the repetition"], [" and try a different method", " and change the plan", " and use a new approach"]],
        [["Use a different approach instead of the repeat", "Use another approach in place of the repeat",
          "Switch to another approach in place of the loop"]],
        [["Break the loop", "Stop the loop"], [" and change the approach used", " and move to a new approach"]],
        [["End the loop", "Stop the loop"], [" and adopt a different approach", " and take another approach"]],
    ],
}

# ---- question forms (the seed0 of each form must match the cores below in meaning) ----
QCORE = {
    "b1_classic": ["What should the agent do after this error?", "Which is the right next move after the failed call?",
                   "What is the right move for the agent after this error?", "After this error, what should the agent do?",
                   "What should the agent do once this call has failed?", "Which move should the agent make after the failed call?",
                   "What is the right next step after this error?", "How should the agent respond to this error?",
                   "What should the agent do now that this call has failed?"],
    "b2_ambig_write": ["What should the agent do about the write whose outcome is unknown?", "How should the agent handle this write?",
                       "What is the right move for a write whose outcome is unknown?",
                       "How should the agent treat this write, since its outcome is unknown?",
                       "What should the agent do with a write whose result is unknown?",
                       "How should the agent handle a write that may have committed already?",
                       "What is the right move for a write whose commit status is unknown?",
                       "What should the agent do about a write that may already have taken effect?"],
    "b3_implicit": ["What should the agent do with this result?", "Which move fits this result?", "How should the agent treat this result?",
                    "What should the agent do with the result it just received?", "Which is the right next move on this result?",
                    "How should the agent handle this result?", "What is the right move with this result?",
                    "Should the agent use this result as it is, or do something else?",
                    "Is this result fit to use, and what should follow?"],
    "b5_deny_escalate": ["What should the agent do after this denial?", "Which is the right move after the denial?",
                         "What should the agent do after being denied?", "How should the agent proceed after this denial?",
                         "Which move comes after this denied action?", "What is the right next step after the denial?",
                         "What should the agent do after the denied step?", "Which path should the agent take after this denial?"],
    "b6_loop_poll": ["What should the agent do next?", "Which is the right move for this repeating call?",
                     "What should the agent do about this repeated call?", "Which move suits this repeating call?",
                     "How should the agent handle this call that keeps repeating?", "What is the right next move for this repeated call?",
                     "Which move fits a call that is being repeated?", "What should the agent do with this run of repeated calls?"],
}
QCORE["b4_blind_retry"] = QCORE["b1_classic"]

# ---- card texts ----
def _n(parts, n):
    """Plain-text number substitution (the cap number is literal text in the seed, not a slot)."""
    return [[[a.replace("#N#", str(n)) for a in alts] for alts in spec] for spec in parts]


CARD = {
    "retry_cap2": _n([[
        ["Recovery policy:", "Retry policy:", "Recovery rule:", "Policy for recovery:", "Error recovery policy:"],
        ["a call that failed for a temporary reason may be repeated while fewer than #N# attempts have been made.",
         "a call that failed for a temporary reason may be retried while fewer than #N# attempts have been made."],
        ["Reads may be repeated freely within that cap.", "Reads can be repeated freely within that cap."],
        ["A write is repeated only when it is idempotent or carries an idempotency key.",
         "A write is repeated only if it is idempotent or carries an idempotency key."],
        ["When the outcome of a write is unknown:", "When a write's outcome is unknown:"],
        ["if the operation is idempotent or a key was sent, repeat it with the same key;",
         "if the operation is idempotent or a key was sent, repeat it with that same key;"],
        ["otherwise, if a read tool for the object is listed, read the state back first; otherwise ask.",
         "otherwise, when a read tool for the object is listed, read the state back first; otherwise ask."],
        ["After a read-back, never repeat an effect that is present; repeat a missing one as a new call.",
         "After a read-back, an effect that is present is never repeated; a missing one is repeated as a new call."],
    ]], 2),
    "retry_cap3": _n([[
        ["Recovery policy:", "Retry policy:", "Recovery rule:", "Policy for recovery:", "Error recovery policy:"],
        ["a call that failed for a temporary reason may be repeated while fewer than #N# attempts have been made.",
         "a call that failed for a temporary reason may be retried while fewer than #N# attempts have been made."],
        ["Reads may be repeated freely within that cap.", "Reads can be repeated freely within that cap."],
        ["A write is repeated only when it is idempotent or carries an idempotency key.",
         "A write is repeated only if it is idempotent or carries an idempotency key."],
        ["When the outcome of a write is unknown:", "When a write's outcome is unknown:"],
        ["if the operation is idempotent or a key was sent, repeat it with the same key;",
         "if the operation is idempotent or a key was sent, repeat it with that same key;"],
        ["otherwise, if a read tool for the object is listed, read the state back first; otherwise ask.",
         "otherwise, when a read tool for the object is listed, read the state back first; otherwise ask."],
        ["After a read-back, never repeat an effect that is present; repeat a missing one as a new call.",
         "After a read-back, an effect that is present is never repeated; a missing one is repeated as a new call."],
    ]], 3),
    "escalate_table": [[
        ["Escalation table:", "Escalation rule table:", "Escalation map:", "Escalation rules:", "Escalation table for this card:"],
        ["quota exhausted -> {quota};", "quota exhaustion -> {quota};", "exhausted quota -> {quota};"],
        ["unsupported operation -> {unsupp};", "unsupported op -> {unsupp};", "unsupported action -> {unsupp};"],
        ["target destroyed -> stop.", "target destroyed -> stop, the goal ends.", "destroyed target -> stop."],
    ]],
    "denial_consec_total": [[
        ["Denial policy:", "Policy for denials:", "Denial rule:", "Rule after denials:", "Denial handling policy:"],
        ["after a denied action, continue by another permitted path when one exists.",
         "after a denied action, take another permitted path when one exists.",
         "when an action is denied, continue by a different permitted path if one exists."],
        ["Escalate to the user after {kc} consecutive denials or {kt} denials in total.",
         "Escalate to the user once there are {kc} consecutive denials or {kt} denials in total.",
         "Escalate to the user after {kc} denials in a row or {kt} denials in total."],
        ["A goal that a fixed rule blocks is stopped.", "A goal blocked by a fixed rule is stopped.",
         "A goal that a fixed rule blocks ends there."],
    ]],
    "denial_window": [[
        ["Denial policy:", "Policy for denials:", "Denial rule:", "Rule after denials:", "Denial handling policy:"],
        ["after a denied action, continue by another permitted path when one exists.",
         "after a denied action, take another permitted path when one exists.",
         "when an action is denied, continue by a different permitted path if one exists."],
        ["Escalate to the user after {kc} consecutive denials or {kw} denials among the last {w} calls.",
         "Escalate to the user once there are {kc} consecutive denials or {kw} denials within the last {w} calls.",
         "Escalate to the user after {kc} denials in a row or {kw} denials among the last {w} calls."],
        ["A goal that a fixed rule blocks is stopped.", "A goal blocked by a fixed rule is stopped.",
         "A goal that a fixed rule blocks ends there."],
    ]],
    "b6": [[
        ["Polling policy:", "Polling rule:", "Polling policy for this goal:", "Policy for repeated polling:"],
        ["repeating a call is legitimate while its state keeps advancing",
         "repeating a call is legitimate while the state keeps moving forward",
         "a repeated call is legitimate while its state keeps advancing"],
        [" (progress rises, status makes a declared transition, or a counter grows).",
         " (progress rises, status makes a declared transition, or a counter increases)."],
        [" Polling budget: {pcap} calls.", " The polling budget is {pcap} calls."],
        [" Loop limit: {lim} calls in a row without advance.", " Loop limit: {lim} calls in a row with no advance."],
        [" Declared transitions: {trans}.", " The declared transitions are {trans}."],
        [" This goal {nw} wait.", " For this goal, the wait {nw}."],
    ]],
}
CARD_CAP_FORMS = {"card.card.t55.retry_cap2", "card.card.t55.retry_cap3"}

# ---- user request forms ----
REQ = {
    "act": ["Please {action} the {entity}{clauses}.", "I need to {action} the {entity}{clauses}.", "Could you {action} the {entity}{clauses}?",
            "Would you {action} the {entity}{clauses} for me?", "Kindly {action} the {entity}{clauses}.",
            "Can you {action} the {entity}{clauses}, please?", "Go ahead and {action} the {entity}{clauses}.",
            "Please go ahead and {action} the {entity}{clauses}."],
    "poll": ["Please wait for the {entity} {ref} to finish.", "Let me know when the {entity} {ref} is done.",
             "Wait for the {entity} {ref} to finish.", "Keep an eye on the {entity} {ref} until it finishes.",
             "Tell me when the {entity} {ref} has finished.", "Let me know once the {entity} {ref} is done.",
             "Please watch the {entity} {ref} until it completes.", "Hold on until the {entity} {ref} finishes."],
    "denied": ["Please finish the {entity} task.", "Finish the {entity} task.", "Can you finish the {entity} task?",
               "I need the {entity} task finished.", "Please complete the {entity} task.", "Complete the {entity} task, please.",
               "Get the {entity} task done.", "I want the {entity} task finished."],
}

# ---- error surface vocabulary (own words; no negation unless the seed has it; no second person) ----
PHRASE = {
    "temp": [[["the service", "the backend", "the dependency", "the upstream component", "the worker pool", "the storage tier",
               "the remote endpoint"],
              ["temporarily unavailable", "timed out", "still starting", "busy and unavailable", "down for a moment",
               "unresponsive for now", "slow to respond"]],
             [["service was temporarily unavailable", "backend timed out", "dependency timed out", "backend still starting"]]],
    "rate": [[["request rate", "call rate", "call volume", "traffic", "the request volume", "the per-window rate", "the call count"],
              ["exceeded", "over the limit", "too high for the window", "above the cap", "past the cap"]],
             [["too many calls in the window", "rate cap reached", "rate limit hit", "calls over the window cap",
               "too many requests in this window", "calls exceeded the window cap", "rate ceiling reached", "request window full",
               "rate cap reached for this window", "calls in the window exceeded the cap", "rate limit reached in this window",
               "too many requests this window"]],
             [["too many calls", "too many requests", "excess calls"], ["in the window", "for this window", "within the window"]]],
    "auth": [[["credentials", "the token", "the key", "the session credentials", "the access token"], ["not accepted"]],
             [["credentials", "the session credentials"],
              ["were not accepted", "were not honored", "are not valid here", "are not recognised"]],
             [["the token", "the key", "the access token", "the session token"],
              ["was not accepted", "was not honored", "is not valid here", "is not recognised"]],
             [["access denied", "permission not granted for this operation", "this operation is not permitted",
               "the caller is not authorised for this operation", "no permission for this operation",
               "permission is not on file for this operation"]],
             [["the operation is not allowed for this caller", "this caller is not allowed to act here",
               "access is not granted for this object", "the object is not visible to this caller",
               "the caller holds no grant for this object", "the grant is not in place for this object"]],
             [["sign-in", "authentication", "the authorisation check"], ["was not accepted", "did not pass", "did not succeed"]],
             [["access", "the caller's access"], ["was not granted", "was not allowed", "is not permitted"]]],
    "arg": [[["argument", "the argument", "the value", "the field value", "the request argument", "the parameter"],
             ["rejected", "refused", "failed validation", "is malformed", "is invalid", "fails to parse", "failed the format check"]],
            [["request failed validation", "malformed argument", "argument rejected by the checker",
              "the request was rejected at validation", "invalid request payload", "a malformed argument was sent",
              "the request fails to parse", "argument failed type checking"]]],
    "unsup": [[["operation", "this operation", "the requested operation", "that operation", "the action", "this action"],
               ["not supported", "not available here", "not implemented", "not offered for this object"]],
              [["no handler exists for this operation", "no such operation is offered here", "no route covers this operation"]],
              [["the object does not offer this operation", "the object does not support this operation",
                "the target does not accept this operation"]],
              [["this operation cannot be carried out on this object"]],
              [["this object cannot run that operation", "the object cannot run this action",
                "that action cannot be run on this object"]],
              [["this endpoint does not handle that operation", "the endpoint does not handle this operation",
                "the handler does not cover this operation", "the service does not offer that action",
                "the component does not cover this action", "the adapter does not expose this operation",
                "the tool does not expose this operation", "the tool does not offer this action"]],
              [["the call is not supported on this object", "that call is not supported here",
                "this request is not supported for this target", "the request is not supported on this endpoint"]],
              [["operations of this kind are not supported here", "this kind of operation is not implemented",
                "this sort of operation is not supported here", "this kind of action is not offered here"]]],
    "quota": [[["usage quota", "the usage quota", "the allowance", "the monthly allowance", "the call budget", "the usage allowance"],
               ["exhausted", "used up", "spent", "at its limit", "fully consumed"]],
              [["allowance used up", "allowance spent", "quota spent", "quota used up", "budget fully consumed",
                "allowance fully used up for this period", "the quota for this period is spent", "usage quota fully used",
                "usage quota reached", "quota reached for this period", "monthly quota spent", "allowance fully consumed for this period"]],
              [["usage quota exhausted for this period", "allowance exhausted for this period", "call budget used up for this period",
                "usage budget spent for this period", "monthly quota used up", "monthly allowance exhausted",
                "the period budget is fully consumed", "the period quota is exhausted", "the period allowance is used up",
                "the period quota is spent"]]],
    "fatal": [[["target", "the target", "the object", "that object", "the record", "the item"],
               ["no longer exists", "no longer available", "is no longer there", "no longer holds data",
                "has been deleted and is no longer there"]],
              [["object permanently removed, and no copy remains", "record permanently removed, with no copy left",
                "item permanently removed, with no backup left", "target permanently removed, with no copy left",
                "object gone for good, with no copy left"]],
              [["goal cannot be met", "the goal cannot be met on this target", "the goal cannot be completed on this target",
                "the goal cannot be reached from this state", "this goal cannot be met"]],
              [["the target is no longer part of the goal", "the record is no longer in scope", "the item is no longer in scope",
                "the object is no longer in scope", "the target is no longer in the state", "the record is no longer in the state",
                "the item is no longer in the state"]],
              [["the target is no longer reachable", "the record is no longer reachable", "the object is no longer reachable"]]],
}


def _phrase_candidates(parts):
    return list(X.expand_parts(parts))


def candidates_for(form):
    if form.startswith("opt."):
        return list(X.expand_parts(OPT[form[4:]]))
    if form.startswith("q."):
        return list(X.expand_prefix_core(Q_PREFIX, QCORE[form[2:]]))
    if form.startswith("card.card.t55."):
        key = form[len("card.card.t55."):]
        if key == "escalate_table_ask" or key == "escalate_table_stop":
            return list(X.expand_parts(CARD["escalate_table"]))
        return list(X.expand_parts(CARD[key]))
    if form == "card.b6":
        return list(X.expand_parts(CARD["b6"]))
    if form.startswith("req."):
        return list(X.expand_prefix_core(REQ_PREFIX, REQ[form[4:]]))
    if form.startswith("phrase."):
        return _phrase_candidates(PHRASE[form[7:]])
    raise KeyError(form)


def main():
    seed_pools = SEEDS.seed_pool().pools
    out, stats = {}, {}
    short = []
    for form in sorted(seed_pools):
        seed0 = seed_pools[form][0]
        cap = CARD_CAP if form in CARD_CAP_FORMS else None
        try:
            kept, st = X.build_form(seed0, candidates_for(form), form, max_keep=cap)
        except ValueError as e:
            short.append(str(e))
            continue
        out[form] = kept
        stats[form] = st
    if short:
        raise SystemExit("SHORT FORMS:\n  " + "\n  ".join(short))
    with open(os.path.join(HERE, "wording_pool_v1.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    manifest = {
        "family": "T55", "pool": "wording_pool_v1", "forms": len(out),
        "min_per_form": min(len(v) for v in out.values()), "total_wordings": sum(len(v) for v in out.values()),
        "pool_sha256": X.pool_sha(out), "seed_module": "T55/t55_wording.py",
        "round_trip": "tool_engine.wording.reword_ok against the seed0 of each form; drop-only",
        "per_form": {k: {"count": len(out[k]), **stats[k]} for k in sorted(out)},
    }
    with open(os.path.join(HERE, "pool_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    print("forms", len(out), "min", manifest["min_per_form"], "total", manifest["total_wordings"], "sha", manifest["pool_sha256"][:16])


if __name__ == "__main__":
    main()
