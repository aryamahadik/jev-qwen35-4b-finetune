"""T54 SEED wordings (Claude-authored; a handful per form). The >= 50 wordings per question form come from the Haiku
reword pass (rewording only, slot round trip, drop-only). Hash with WordingPool.export_sha() at EVERY change."""
from tool_engine.wording import WordingPool

# imperative action phrase per verb (closed 36-verb list)
ACTION = {
    "get": "get", "list": "list", "find": "find", "search": "search for", "count": "count", "read": "read",
    "check": "check", "create": "create", "add": "add", "update": "update", "set": "set", "rename": "rename",
    "move": "move", "copy": "copy", "remove": "remove", "delete": "delete", "cancel": "cancel", "close": "close",
    "open": "open", "archive": "archive", "restore": "restore", "assign": "assign", "merge": "merge", "send": "send",
    "schedule": "schedule", "reserve": "reserve", "release": "release", "approve": "approve", "reject": "reject",
    "export": "export", "import": "import", "sync": "sync", "lock": "lock", "unlock": "unlock", "tag": "tag",
    "lookup": "look up",
}
OPTION_TEXT = {
    "CALL": ["Call the listed tool with the values given", "Make the tool call now, all values are available"],
    "ASK": ["Ask the user for the missing value", "Stop and ask the user for the value that is missing"],
    "NO_TOOL": ["Say that no listed tool can do this", "Tell the user the listed tools cannot do this"],
    "ANSWER": ["Answer directly, no tool is needed", "Reply from what is already stated, without a tool"],
    "RESULT_MISSING": ["Say the earlier result is missing and do not guess the value",
                       "Report that the earlier result never arrived; do not invent the value"],
    "WRITE": ["Make the write call now", "Issue the write call now"],
    "READ_FIRST": ["Read the current state first", "Call a read tool first to see the current state"],
    "DONE_NO_CALL": ["Make no call, the wanted state already holds", "No call is needed, the state is already as wanted"],
    "GROUNDED": ["Every value in the call is grounded in the conversation", "All supplied values have a source in the conversation"],
    "UNGROUNDED": ["At least one value in the call has no grounding", "Some supplied value has no source in the conversation"],
}
CARD_TEXT = {
    "card.t54.strict_ask": [
        "Tool-use policy: when a required value was not given and cannot be found in the conversation, ask for it. "
        "Never fill a value in yourself, even when the tool lists a default.",
        "Policy: a required value that is neither stated nor found earlier must be asked for. Listed defaults are not used."],
    "card.t54.defaults_ok": [
        "Tool-use policy: when a required value was not given but the tool lists a default for it, use the default. "
        "When there is no default and no source, ask.",
        "Policy: a listed default may stand in for a required value nobody gave. With no default and no source, ask."],
    "card.t54.read_before_write": [
        "Write policy: a write marked idempotent may be issued without reading first. Any other write whose current "
        "state is unknown must be preceded by a read, when a read tool is listed; with no read tool, ask. A state "
        "already shown to hold needs no write.",
        "Write policy: idempotent writes may go straight ahead. For a write that is not idempotent, check the state "
        "with a read tool first when one is listed, otherwise ask. If the wanted state is already shown, do nothing."],
    "card.t54.parallel_ok": [
        "Batching policy: calls that do not use each other's output may be issued together in one step. A call that "
        "needs another call's output waits for it.",
        "Batching policy: independent calls go out together. A call whose arguments come from another call's output "
        "must wait for that output."],
}
QUESTION = {
    "s1_need4": ["What should the agent do next?", "Which is the right next move for the agent?"],
    "s2_pick": ["Which listed tool, with its arguments, is the right call?", "Pick the call that fits the request."],
    "s3_limit": ["What should the agent do next?", "Which is the right next move for the agent?"],
    "s4_precond": ["Is the write needed, given what is known?", "What should the agent do about the write?"],
    "s5_argground": ["Is every value in the proposed call grounded in the conversation?",
                     "Do all values in the proposed call come from the conversation?"],
    "s6_parseq": ["Which set of calls may be issued together in the next step?",
                  "Which calls are ready to go out together now?"],
}
REQUEST = {
    "act": ["Please {action} the {entity}{clauses}.", "I need to {action} the {entity}{clauses}.",
            "{action_cap} the {entity}{clauses}, please.", "Could you {action} the {entity}{clauses}?"],
    "fetch": ["What is the {field} of the {entity}{refpart}{clauses}?", "Which {field} does the {entity}{refpart} have{clauses}?"],
    "fetch_ref": ["What is the {field} of the same {entity} as before{clauses}?",
                  "Which {field} does the same {entity} as before have{clauses}?"],
    "info": ["Which {field} did I give for that {entity}?", "What {field} did I say that {entity} has?"],
    "info_card": ["What is the default {field} for the {entity}?", "Which default {field} applies to the {entity}?"],
    "reference": ["Now {action} the {entity}{clauses}, using the same {pname} as before.",
                  "{action_cap} the {entity} again{clauses}, with the same {pname} as last time."],
    "state_write": ["Make sure the {entity} {ref} ends up with {pname} {value}.",
                    "I want the {entity} {ref} to have {pname} {value}."],
    "plan": ["Do the following: {steps}.", "Carry out these steps: {steps}."],
}
FACT_TEXT = ["For the record, the {entity} {ref} has {field} {value}.", "Note that the {entity} {ref} carries {field} {value}."]
CARD_NOTE = ["Card note: the default {field} for a {entity} is {value}.", "Default: {field} of a {entity} is {value}."]


def seed_pool():
    p = WordingPool()
    for lab, ts in OPTION_TEXT.items():
        p.add("opt.%s" % lab, ts)
    for cid, ts in CARD_TEXT.items():
        p.add("card.%s" % cid, ts)
    for sb, ts in QUESTION.items():
        p.add("q.%s" % sb, ts)
    for k, ts in REQUEST.items():
        p.add("req.%s" % k, ts)
    p.add("fact.text", FACT_TEXT)
    p.add("card.note", CARD_NOTE)
    return p
