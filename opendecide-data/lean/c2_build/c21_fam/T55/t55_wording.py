"""T55 SEED wordings (Claude-authored; a handful per form). The >= 50 per question form come from the Haiku reword pass
(reword-only, slot round trip, drop-only). Error surface tokens (codes, phrases, status-class tokens) are our own
vocabulary; no wording or code table is copied from any API reference or benchmark."""
from tool_engine.wording import WordingPool

OPTION_TEXT = {
    "RETRY": ["Repeat the same call", "Issue the identical call again"],
    "FIX_ARGS": ["Repeat the call with corrected arguments", "Correct the argument and call again"],
    "SWITCH_TOOL": ["Use a different listed tool for the same goal", "Switch to the equivalent listed tool"],
    "ASK": ["Ask the user", "Stop and ask the user or a reviewer"],
    "STOP": ["Give up on this goal and report", "Stop here and report that the goal cannot be met"],
    "RETRY_KEYED": ["Repeat the write with the same idempotency key", "Send the same write again, same key"],
    "READ_BACK": ["Read the state back first", "Check whether the write took effect before doing anything else"],
    "RETRY_PLAIN": ["Repeat the write as a new attempt", "Send the write again as a fresh call"],
    "NO_RETRY": ["Do not repeat the write, the effect is confirmed", "Leave it, the effect is already there"],
    "ACCEPT": ["Use the result as it is", "Accept the result"],
    "CONTINUE_ALT": ["Continue by another permitted path", "Take a different permitted route to the goal"],
    "ESCALATE": ["Stop acting and ask for a human decision", "Escalate to the user"],
    "RETRY_SAME": ["Repeat the denied action", "Try the denied action again"],
    "KEEP_POLLING": ["Keep polling, the repeats are legitimate waiting", "Poll again"],
    "BREAK_LOOP_ALT": ["Break the loop and change approach", "Stop repeating and use another approach"],
}
QUESTION = {
    "b1_classic": ["What should the agent do after this error?", "Which is the right next move after the failed call?"],
    "b4_blind_retry": ["What should the agent do after this error?", "Which is the right next move after the failed call?"],
    "b2_ambig_write": ["What should the agent do about the write whose outcome is unknown?", "How should the agent handle this write?"],
    "b3_implicit": ["What should the agent do with this result?", "Is this result usable, and if not, what next?"],
    "b5_deny_escalate": ["What should the agent do after this denial?", "Which is the right move after the denial?"],
    "b6_loop_poll": ["What should the agent do next?", "Which is the right move for this repeating call?"],
}
CARD_TEXT = {
    "card.t55.retry_cap2": ["Recovery policy: a call that failed for a temporary reason may be repeated while fewer than 2 attempts "
                            "have been made. Reads may be repeated freely within that cap. A write is repeated only when it is idempotent "
                            "or carries an idempotency key. When the outcome of a write is unknown: if the operation is idempotent or a key "
                            "was sent, repeat it with the same key; otherwise, if a read tool for the object is listed, read the state back "
                            "first; otherwise ask. After a read-back, never repeat an effect that is present; repeat a missing one as a new call."],
    "card.t55.retry_cap3": ["Recovery policy: a call that failed for a temporary reason may be repeated while fewer than 3 attempts "
                            "have been made. Reads may be repeated freely within that cap. A write is repeated only when it is idempotent "
                            "or carries an idempotency key. When the outcome of a write is unknown: if the operation is idempotent or a key "
                            "was sent, repeat it with the same key; otherwise, if a read tool for the object is listed, read the state back "
                            "first; otherwise ask. After a read-back, never repeat an effect that is present; repeat a missing one as a new call."],
    "card.t55.escalate_table_ask": ["Escalation table: quota exhausted -> {quota}; unsupported operation -> {unsupp}; target destroyed -> stop."],
    "card.t55.escalate_table_stop": ["Escalation table: quota exhausted -> {quota}; unsupported operation -> {unsupp}; target destroyed -> stop."],
    "card.t55.denial_consec_total": ["Denial policy: after a denied action, continue by another permitted path when one exists. Escalate to the user "
                                     "after {kc} consecutive denials or {kt} denials in total. A goal that a fixed rule blocks is stopped."],
    "card.t55.denial_window": ["Denial policy: after a denied action, continue by another permitted path when one exists. Escalate to the user "
                               "after {kc} consecutive denials or {kw} denials among the last {w} calls. A goal that a fixed rule blocks is stopped."],
}
CARD_B6_EXTRA = ["Polling policy: repeating a call is legitimate while its state keeps advancing (progress rises, status makes a declared "
                 "transition, or a counter grows). Polling budget: {pcap} calls. Loop limit: {lim} calls in a row without advance. "
                 "Declared transitions: {trans}. This goal {nw} wait."]
USER_REQUEST = {
    "act": ["Please {action} the {entity}{clauses}.", "I need to {action} the {entity}{clauses}.",
            "Could you {action} the {entity}{clauses}?"],
    "poll": ["Please wait for the {entity} {ref} to finish.", "Let me know when the {entity} {ref} is done."],
    "denied": ["Please finish the {entity} task."],
}
ACTION = {"get": "get", "list": "list", "find": "find", "search": "search for", "count": "count", "read": "read",
          "check": "check", "create": "create", "add": "add", "update": "update", "set": "set", "rename": "rename",
          "move": "move", "copy": "copy", "remove": "remove", "delete": "delete", "cancel": "cancel", "close": "close",
          "archive": "archive", "restore": "restore", "assign": "assign", "merge": "merge", "send": "send",
          "schedule": "schedule", "reserve": "reserve", "release": "release", "approve": "approve",
          "export": "export", "sync": "sync", "lookup": "look up"}
# error surface vocabulary (own): status-class tokens, codes and phrases per class. invalid_named_arg and
# invalid_unnamed share every token (only the `field` line tells them apart, G0-lite B4)
CLASS_GROUP = {"transient_unavailable": "temp", "rate_limited": "rate", "auth_denied": "auth", "invalid_named_arg": "arg",
               "invalid_unnamed": "arg", "unsupported_op": "unsup", "quota_exhausted": "quota", "irrecoverable": "fatal"}
STATUS_TOKEN = {"temp": "error_temp", "rate": "error_rate", "auth": "error_auth", "arg": "error_arg", "unsup": "error_unsup",
                "quota": "error_quota", "fatal": "error_fatal"}
CODES = {"temp": ["E101", "E108", "E115"], "rate": ["E201", "E208", "E215"], "auth": ["E301", "E308", "E315"],
         "arg": ["E401", "E408", "E415"], "unsup": ["E501", "E508", "E515"], "quota": ["E601", "E608", "E615"],
         "fatal": ["E701", "E708", "E715"]}
PHRASES = {"temp": ["temporarily unavailable", "dependency timed out", "backend not ready"],
           "rate": ["request rate exceeded", "too many calls in the window", "rate cap reached"],
           "auth": ["credentials not accepted", "permission missing for this operation", "access denied"],
           "arg": ["argument rejected", "request failed validation", "malformed argument"],
           "unsup": ["operation not supported", "unsupported operation for this object"],
           "quota": ["usage quota exhausted", "allowance used up"],
           "fatal": ["target no longer exists", "object permanently removed", "goal cannot be met"]}


def seed_pool():
    p = WordingPool()
    for lab, ts in OPTION_TEXT.items():
        p.add("opt.%s" % lab, ts)
    for sb, ts in QUESTION.items():
        p.add("q.%s" % sb, ts)
    for cid, ts in CARD_TEXT.items():
        p.add("card.%s" % cid, ts)
    p.add("card.b6", CARD_B6_EXTRA)
    for k, ts in USER_REQUEST.items():
        p.add("req.%s" % k, ts)
    for g, ts in PHRASES.items():
        p.add("phrase.%s" % g, ts)
    return p
