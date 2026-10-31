"""Plug point for the T67 pipeline: `solver_b(bview)` -> dict(status="ok"|"abstain"|"error", label=..., letter=...).

B touches only the b-view fields (rendered text, options, witness_inputs, head). It reads the rendered context, recovers the card, the session notes or table
card, the user turn and the proposed file, maps the file's items to effects, applies the G0-lite table and returns the component the question asks for:
GATE -> ALLOW / ASK / BLOCK, REASON -> the reason word, TIER -> soft / hard / na. `letter` is the lettered option whose text carries that word."""
from . import ci, effects as E, k8s, minisql, plan, r10 as R10, sqlrules
from . import tables as T
from . import textview as V

DEFAULT_LOCK_TABLE = dict(T.LOCK_DRAFT)
SPACE = {"GATE": T.LABELS, "REASON": T.REASONS, "TIER": T.TIERS}


def _carrier_from_text(sec):
    call = sec["call"]
    if sec["call_kind"] == "write":
        return "CI_WORKFLOW"
    if call.startswith("terraform "):
        return "PLAN_JSON"
    if call.startswith("kubectl "):
        return "K8S_MANIFEST"
    if call.startswith("psql "):
        return "MIGRATION_SQL"
    raise V.Unparsable("carrier")


def triple(bview, lock_table=None, r10=R10.rule):
    rendered = bview["rendered"]
    sec = V.split_context(rendered.get("context") or rendered.get("text") or "")
    carrier = _carrier_from_text(sec)
    declared = (bview.get("witness_inputs") or {}).get("carrier")
    if declared and declared != carrier:
        raise V.Unparsable("carrier mismatch")
    card = V.parse_card(sec["card"])
    session = V.parse_session(sec["session"])
    user_text, env_lane = V.parse_user(sec["user"])
    if carrier == "PLAN_JSON":
        ws, items = plan.parse(sec["artifact"])
        effs = plan.effects(ws, items, card, session, env_lane)
    elif carrier == "K8S_MANIFEST":
        verb, ctx_name = k8s.parse_call(sec["call"])
        items = k8s.parse(sec["artifact"])
        effs = k8s.effects(verb, ctx_name, items, card, session, env_lane)
    elif carrier == "CI_WORKFLOW":
        path = sec["call"].strip()
        doc = ci.parse(sec["artifact"])
        effs = ci.effects(doc, card, session, path)
    else:
        db = sqlrules.parse_call(sec["call"])
        table = V.parse_table(sec["table"])
        units = minisql.group_forms(minisql.parse(sec["artifact"]))
        effs = sqlrules.effects(units, card, table, db, env_lane, lock_table or DEFAULT_LOCK_TABLE, r10)
    res = E.resolve(effs, card, user_text)
    return carrier, res


def make_solver_b(lock_table=None, r10=R10.rule):
    def solver_b(bview):
        try:
            head = T.HEADS.get(bview.get("head"))
            if head is None:
                return dict(status="abstain", label=None, letter=None, why="head")
            carrier, res = triple(bview, lock_table, r10)
            value = {"GATE": res["label"], "REASON": res["reason"], "TIER": res["tier"]}[head]
            opts = V.option_table(bview["rendered"], bview.get("options"))
            if set(opts.values()) != set(SPACE[head]):
                return dict(status="abstain", label=None, letter=None, why="options do not match the head")
            letters = [k for k, v in opts.items() if v == value]
            if len(letters) != 1:
                return dict(status="abstain", label=None, letter=None, why="option")
            return dict(status="ok", label=value, letter=letters[0], triple=(res["label"], res["reason"], res["tier"]), carrier=carrier,
                        rules=sorted(set(e.rule for e in res["live"])), cleared=sorted(set(e.rule for e in res["cleared"])))
        except V.Unparsable as e:
            return dict(status="abstain", label=None, letter=None, why=str(e))
        except Exception as e:                                       # noqa: BLE001 - any failure of B on a row is an error status, never a guess
            return dict(status="error", label=None, letter=None, why=type(e).__name__)
    return solver_b


solver_b = make_solver_b()


def naming_report(bview):
    """GV12 / T67-B10 helper (B's parse of the user turn): which operation words of the closed lexicon occur in the turn, and which of the file's own item
    names (addresses, workflow path / jobs, tables, databases) occur. -> dict(ops=[...], targets=[...])."""
    sec = V.split_context(bview["rendered"].get("context") or bview["rendered"].get("text") or "")
    user_text, _ = V.parse_user(sec["user"])
    ops = sorted(k for k, ph in T.OP_PHRASE.items() if V.mentions(user_text, ph))
    names = set()
    carrier = _carrier_from_text(sec)
    if carrier == "PLAN_JSON":
        names |= set(i["address"] for i in plan.parse(sec["artifact"])[1])
    elif carrier == "K8S_MANIFEST":
        names |= set(i["address"] for i in k8s.parse(sec["artifact"]))
    elif carrier == "CI_WORKFLOW":
        doc = ci.parse(sec["artifact"])
        path = sec["call"].strip()
        names |= {path} | set("%s#%s" % (path, j) for j in doc["jobs"])
    else:
        names |= {sqlrules.parse_call(sec["call"]), V.parse_table(sec["table"])["table"]}
    return dict(ops=ops, targets=sorted(n for n in names if n and V.names_target(user_text, n)))
