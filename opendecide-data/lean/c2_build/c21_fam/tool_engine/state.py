"""Simulated tool world pieces shared by T54/T55: tool schemas, argument values, knowledge-state vocabulary, and the
effect LEDGER with the five-option two-world simulation (T55 B2).

Records are plain dicts (JSON-serialisable) so solver A reads the same structure that is exported.
"""
from . import util

# ---- closed vocabularies (all ids are on the frozen allow-list; see names.py) ---------------------------------
VERBS_T54 = ["get", "list", "find", "search", "count", "read", "check", "create", "add", "update", "set", "rename",
             "move", "copy", "remove", "delete", "cancel", "close", "open", "archive", "restore", "assign", "merge",
             "send", "schedule", "reserve", "release", "approve", "reject", "export", "import", "sync", "lock",
             "unlock", "tag", "lookup"]
VERBS_T55 = [v for v in VERBS_T54 if v not in ("open", "reject", "import", "lock", "unlock", "tag")]
ROLES_T54 = ["id", "key", "name", "count", "limit", "offset", "date_from", "date_to", "when", "amount", "quantity",
             "status", "label", "note", "reason", "query", "scope", "mode", "target", "source", "destination",
             "priority", "owner", "version"]
ROLES_T55 = ["id", "key", "name", "count", "limit", "offset", "amount", "quantity", "status", "label", "note",
             "reason", "query", "scope", "mode", "target", "owner", "version", "idempotency_key"]
ROLE_TYPE = {"id": "str", "key": "str", "name": "str", "count": "int", "limit": "int", "offset": "int",
             "date_from": "date", "date_to": "date", "when": "date", "amount": "num", "quantity": "int",
             "status": "enum", "label": "str", "note": "str", "reason": "str", "query": "str", "scope": "enum",
             "mode": "enum", "target": "str", "source": "str", "destination": "str", "priority": "int",
             "owner": "str", "version": "str", "idempotency_key": "str"}
READ_VERBS = {"get", "list", "find", "search", "count", "read", "check", "lookup"}
# synonym classes -> substitutable tools (same entity, same schema) share an equivalence group
SYNONYMS = [("get", "read", "lookup"), ("find", "search"), ("remove", "delete"), ("create", "add"),
            ("update", "set")]
DEFAULT_IDEMPOTENT = {"set", "close", "archive", "restore", "lock", "unlock", "approve", "reject", "release",
                      "cancel", "open", "tag"}
VERB_PHRASE = {  # one-line descriptions (own wording; entity filled in)
    "get": "Retrieves one {e} record", "list": "Lists {e} records", "find": "Finds {e} records matching a query",
    "search": "Searches {e} records by text", "count": "Counts {e} records", "read": "Reads one {e} record",
    "check": "Checks the state of a {e}", "create": "Creates a {e} record", "add": "Adds a {e} record",
    "update": "Changes fields of a {e} record", "set": "Sets a field of a {e} record",
    "rename": "Renames a {e} record", "move": "Moves a {e} record", "copy": "Copies a {e} record",
    "remove": "Removes a {e} record", "delete": "Deletes a {e} record", "cancel": "Cancels a {e}",
    "close": "Closes a {e}", "open": "Opens a {e}", "archive": "Archives a {e} record",
    "restore": "Restores a {e} record", "assign": "Assigns a {e} record to an owner",
    "merge": "Merges two {e} records", "send": "Sends a {e}", "schedule": "Schedules a {e}",
    "reserve": "Reserves a {e}", "release": "Releases a {e}", "approve": "Approves a {e}",
    "reject": "Rejects a {e}", "export": "Exports {e} records", "import": "Imports {e} records",
    "sync": "Syncs {e} records", "lock": "Locks a {e}", "unlock": "Unlocks a {e}", "tag": "Tags a {e} record",
    "lookup": "Looks up one {e} record",
}
# verb -> parameter template [(slot, required)] ; slot = "ENTITY_ID" (the <entity>_id parameter), "FIELD" (an
# <field-noun> parameter) or a generic role id
VERB_PARAMS = {
    "get": [("ENTITY_ID", True)], "read": [("ENTITY_ID", True)], "lookup": [("ENTITY_ID", True)],
    "list": [("limit", False), ("offset", False), ("status", False)],
    "find": [("query", True), ("limit", False)], "search": [("query", True), ("limit", False)],
    "count": [("status", False), ("query", False)], "check": [("ENTITY_ID", True), ("mode", False)],
    "create": [("name", True), ("FIELD", False)], "add": [("name", True), ("FIELD", False)],
    "update": [("ENTITY_ID", True), ("FIELD", True)], "set": [("ENTITY_ID", True), ("status", True)],
    "rename": [("ENTITY_ID", True), ("name", True)], "move": [("ENTITY_ID", True), ("destination", True)],
    "copy": [("ENTITY_ID", True), ("destination", False)], "remove": [("ENTITY_ID", True)],
    "delete": [("ENTITY_ID", True)], "cancel": [("ENTITY_ID", True), ("reason", False)],
    "close": [("ENTITY_ID", True), ("reason", False)], "open": [("ENTITY_ID", True)],
    "archive": [("ENTITY_ID", True)], "restore": [("ENTITY_ID", True)],
    "assign": [("ENTITY_ID", True), ("owner", True)], "merge": [("source", True), ("target", True)],
    "send": [("ENTITY_ID", True), ("destination", True)], "schedule": [("ENTITY_ID", True), ("when", True)],
    "reserve": [("ENTITY_ID", True), ("quantity", True)], "release": [("ENTITY_ID", True)],
    "approve": [("ENTITY_ID", True), ("note", False)], "reject": [("ENTITY_ID", True), ("reason", True)],
    "export": [("scope", True), ("mode", False)], "import": [("source", True), ("mode", False)],
    "sync": [("scope", False), ("mode", False)], "lock": [("ENTITY_ID", True)], "unlock": [("ENTITY_ID", True)],
    "tag": [("ENTITY_ID", True), ("label", True)],
}
SOURCES = ("user_turn", "prior_tool_output", "card_default", "none", "missing_result")


def synonym_class(verb):
    for cls in SYNONYMS:
        if verb in cls:
            return cls
    return (verb,)


def group_id(verb, entity):
    return "g:%s:%s" % (synonym_class(verb)[0], entity)


def build_tool(tid, verb, entity, field_nouns, allowed_roles, rng, idempotent=None, group=None, desc_tail="",
               drop_optional_prob=0.0):
    """One tool dict. Parameter names: role params keep the role word; ENTITY_ID -> '<entity>_id'; FIELD -> a field
    noun. Declared defaults are attached to some optional params (used by the strict_ask/defaults_ok card contrast)."""
    params = []
    fi = 0
    for slot, required in VERB_PARAMS[verb]:
        if not required and rng.random() < drop_optional_prob:
            continue
        if slot == "ENTITY_ID":
            p = {"name": "%s_id" % entity, "role": None, "required": required, "type": "str"}
        elif slot == "FIELD":
            fn = field_nouns[fi % len(field_nouns)]
            fi += 1
            p = {"name": fn, "role": None, "required": required, "type": "str"}
        else:
            if slot not in allowed_roles:
                continue
            p = {"name": slot, "role": "param." + slot, "required": required, "type": ROLE_TYPE[slot]}
        p["default"] = None
        params.append(p)
    rw = "read" if verb in READ_VERBS else "write"
    if idempotent is None:
        idempotent = (verb in DEFAULT_IDEMPOTENT) if rw == "write" else True
    return {"tid": tid, "verb": verb, "entity": entity, "name": "%s_%s" % (verb, entity), "rw": rw,
            "idempotent": bool(idempotent), "group": group or group_id(verb, entity), "params": params,
            "desc": (VERB_PHRASE[verb].format(e=entity) + (" " + desc_tail if desc_tail else "")).strip()}


def make_equivalent(tool, tid, verb_choices, rng):
    """A substitutable tool: same entity and schema, a synonymous verb (different surface name), same group."""
    cls = [v for v in synonym_class(tool["verb"]) if v != tool["verb"] and v in verb_choices]
    if not cls:
        return None
    v = rng.choice(cls)
    t = dict(tool)
    t["params"] = [dict(p) for p in tool["params"]]
    t.update({"tid": tid, "verb": v, "name": "%s_%s" % (v, tool["entity"]),
              "desc": VERB_PHRASE[v].format(e=tool["entity"])})
    t["group"] = tool["group"]
    return t


_STEM_DENY = {"get", "set", "add", "run", "use", "try", "ask", "fix", "do", "go", "let", "make", "new", "old", "ok", "no", "not",
              "see", "has", "had", "was", "are", "you", "our", "its", "who", "how", "why", "tag", "now", "wait", "stop", "send", "read",
              "list", "find", "open", "move", "copy", "sync", "lock"}


def id_stem(stem):
    """First letters of an entity noun for composed ids, never an English word / imperative verb (the output lint and the
    models would otherwise read 'set-5577' as a command)."""
    if not stem:
        return "x"
    for cand in (stem[:3], stem[1:4], stem[2:5], stem[:2] + "x"):
        if cand not in _STEM_DENY:
            return cand
    return "x" + stem[:2]


def gen_value(rng, ptype, stem):
    """A plain argument value string by type. `stem` is a noun used to make ids look entity-specific."""
    if ptype == "int":
        return str(rng.randrange(2, 90))
    if ptype == "num":
        return "%d.%02d" % (rng.randrange(1, 900), rng.randrange(100))
    if ptype == "date":
        return "2026-%02d-%02d" % (rng.randrange(1, 13), rng.randrange(1, 29))
    if ptype == "enum":
        return rng.choice(["alpha", "bravo", "delta", "omega", "sigma", "theta"])
    if ptype == "bool":
        return rng.choice(["true", "false"])
    return "%s-%d" % (id_stem(stem), rng.randrange(100, 9999))


# ---- ledger (T55 B2) -----------------------------------------------------------------------------------------
class Ledger:
    """Effect ledger. `commit(effect, request_id, dedup)` appends an effect unless the same request is re-sent and
    dedup holds (an idempotency key was offered, or the operation is idempotent). A fresh request id (a NEW attempt)
    always appends."""

    def __init__(self):
        self.entries = []          # list of (effect, request_id)

    def commit(self, effect, request_id, dedup):
        if dedup and any(e == effect and r == request_id for e, r in self.entries):
            return False
        self.entries.append((effect, request_id))
        return True

    def count(self, effect):
        return sum(1 for e, _ in self.entries if e == effect)


AMBIG_ACTIONS = ("RETRY_KEYED", "READ_BACK", "RETRY_PLAIN", "ASK", "NO_RETRY")
# relative cost of a safe action: no call < one more call < a read plus a conditional call < a human round trip.
# RETRY_PLAIN is cheaper than RETRY_KEYED so that, once a read-back has PROVED the write absent, the plain retry wins
# (the rule table's step 2); a keyed retry is only ever the cheapest action when plain retry is unsafe.
AMBIG_COST = {"NO_RETRY": 0.0, "RETRY_PLAIN": 1.0, "RETRY_KEYED": 1.1, "READ_BACK": 2.0, "ASK": 3.0}


def effects_after(action, committed, idem, key_offered, read_path):
    """Number of effects of the original write in the ledger after `action`, in the world where the original write
    did (committed=True) or did not (False) commit. None when the action is unavailable (READ_BACK without a read path)."""
    led = Ledger()
    dedup_orig = bool(idem or key_offered)
    if committed:
        led.commit("e", "req0", dedup_orig)
    if action == "NO_RETRY":
        pass
    elif action == "RETRY_PLAIN":
        led.commit("e", "req-new", False)                  # a new attempt: never deduplicated
    elif action == "RETRY_KEYED":
        led.commit("e", "req0", dedup_orig)                # same request again: deduplicated only when key/idempotent
    elif action == "READ_BACK":
        if not read_path:
            return None
        if led.count("e") == 0:                            # the read shows absence -> one clean retry follows
            led.commit("e", "req-new", False)
    elif action == "ASK":
        if led.count("e") == 0:                            # a human settles it, exactly one effect
            led.commit("e", "req-new", False)
    else:
        raise ValueError(action)
    return led.count("e")


def ambiguous_write_simulated_gold(idem, key_offered, read_path, committed, step):
    """Gold by simulation: the cheapest available action that leaves exactly one effect in EVERY world consistent
    with the visible facts. Step 1: both worlds are consistent. Step 2: the read-back has revealed the world."""
    worlds = (True, False) if step == 1 else (bool(committed),)
    best, best_cost = None, None
    for a in AMBIG_ACTIONS:
        outs = [effects_after(a, w, idem, key_offered, read_path) for w in worlds]
        if any(o is None for o in outs) or any(o != 1 for o in outs):
            continue
        c = AMBIG_COST[a]
        if best is None or c < best_cost:
            best, best_cost = a, c
    return best
