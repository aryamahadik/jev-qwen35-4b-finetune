"""T59 rendering + finalisation: scene -> text (card, tools, conversation, planned step, question, options), line-level span map (kind per
line, used by the pair-integrity gate K14), option order with a balanced gold position, name-id collection, G10 decision spans.
Labels come from SOLVER A only (t59_solver_a via t59_scene.derive_case). CODE ONLY.
"""
import hashlib
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_ROOT, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from tool_engine import render, state, util, wording  # noqa: E402
import t59_scene as sc  # noqa: E402
import t59_solver_a as sa  # noqa: E402
import t59_wording as tw  # noqa: E402

ROLES_T59 = ("id", "key", "name", "count", "limit", "offset", "date_from", "date_to", "when", "amount", "quantity", "status", "label", "note",
             "reason", "query", "scope", "mode", "target", "source", "destination", "priority", "owner", "version")
PROGS_REPO = ("git", "rm", "mv", "cp", "mkdir", "touch")
EXPOSURE = {True: "Visible outside the team.", False: "Visible inside the team only."}
EXPOSURE_FIXED = "Delivers outside the team."
OUTPUT_KEYS = {"status", "code", "retry_after", "field", "detail", "count", "items", "total", "key", "committed", "files", "id", "size",
               "path"}


def ln(kind, text):
    return dict(kind=kind, text=text)


def _stable_order(gid, key):
    return hashlib.sha256(("%s|%s" % (gid, key)).encode()).hexdigest()


def _fill(rec, tpl, slots):
    used = wording.template_slots(tpl)
    out = wording.fill(tpl, slots)
    rec["slots"].update({k: slots[k] for k in used if k in ("id", "value", "q", "amount", "cap", "price", "role", "pid", "size", "list",
                                                           "H", "cap_n", "win", "lose")})
    return out


# ======================================================================================================================
# tools
# ======================================================================================================================
def _tool(tid, verb, noun, rng, tail="", idem=None, field_nouns=(), role_default=None):      # no placeholder field name: a FIELD param needs a drawn noun
    t = state.build_tool(tid, verb, noun, list(field_nouns), set(ROLES_T59), rng, idempotent=idem)
    if tail:
        t["desc"] = state.VERB_PHRASE[verb].format(e=noun) + ". " + tail
    if role_default is not None:
        for p in t["params"]:
            if p.get("role") and p["name"] == role_default[0]:
                p["default"] = role_default[1]
    return t


def tool_lines(ctx, scene, rng):
    """-> [(order_key, kind, line_text)] for the Tools block (tool world) and the used (verb, param roles) for the names guard."""
    ent, op, fx, tl, t = scene["ent"], scene["op"], scene["fx"], scene["tools"], scene["t"]
    noun = ent["noun"]
    out = []
    used_verbs, used_roles = set(), set()

    def add(order_key, kind, tool):
        out.append((order_key, kind, "- " + render.render_tool_line(tool)))
        used_verbs.add(tool["verb"])
        for p in tool["params"]:
            if p.get("role"):
                used_roles.add(p["role"].split(".", 1)[1])

    trig = scene["trigger"]
    cap_present = scene["t"].get("cap_present", True) if trig == "T5" else True
    # the write tool
    if cap_present:
        tail = EXPOSURE_FIXED if op["ext_fixed"] else EXPOSURE[bool(fx["external"])]
        rd = None
        if trig == "T1" and t.get("default") is not None:
            rd = (op["param"]["role"], t["default"])
        w = _tool("tw", op["verb"], noun, rng, tail=tail, idem=fx["idempotent"], field_nouns=(ent["fa"],), role_default=rd)
        if fx["keyed"]:
            w["params"].append(dict(name="key", role="param.key", required=False, type="str", default=None))
            w["desc"] += " Accepts a key that makes a repeated call a no-op."
        if trig == "T6" and scene["t"]["cls"] == "invalid_named":
            pass
        add("write", "tool_write", w)
    # undo tool of the primary op
    if fx["undo"] and op["undo_verb"] and cap_present:
        u = _tool("tu", op["undo_verb"], noun, rng, tail="Works within %d days of the change." % fx["undo"]["window"], idem=True)
        add("undo", "tool_undo", u)
    # T5 substitute (+ its undo tool)
    if trig == "T5" and scene["t"]["subs"]:
        s = scene["t"]["subs"][0]
        add("sub", "tool_sub", _tool("ts", s["verb"], noun, rng, tail=EXPOSURE[False], idem=sc.OPS[s["verb"]]["idem"], field_nouns=(ent["fa"],)))
        if s.get("undo") and s.get("undo_verb"):
            add("subundo", "tool_undo", _tool("tsu", s["undo_verb"], noun, rng,
                                              tail="Works within %d days of the change." % s["undo"]["window"], idem=True))
    # reads
    # a read-only call on the target's noun is listed only where the scene says so (`tools.read_list`, `read_get`, `read_auth`): T6 and T7 rows
    # list one only when it is the intended read path / resolver (Opus ruling Q2 follow-up FU5; see read_path_problems)
    if tl.get("read_list"):
        add("list", "tool_read_list", _tool("tl", "list", noun, rng))
    if trig == "T8":
        add("find", "tool_read_find", _tool("tf", "find", noun, rng))
    need_get = (trig in ("T1", "T3", "T5")) or (trig in ("T6", "T7") and (tl.get("read_get") or t.get("tool_kind") == "read")) \
        or bool(tl.get("read_auth"))
    if need_get:
        if tl.get("read_auth"):
            add("get", "tool_read_auth", _tool("tg", "get", noun, rng, tail="Reads the current value of a field; this value is authoritative.",
                                               idem=True))
        else:
            add("get", "tool_read_get", _tool("tg", "get", noun, rng))
    if tl.get("equiv") and cap_present:
        eq = state.make_equivalent(w, "te", [tl["equiv"]["verb"]], rng)
        if eq is None:
            raise ValueError("no equivalent for %s" % op["verb"])
        add("equiv", "tool_equiv", eq)
    if t.get("prereq") and scene["world"] == "tool":
        pn = ent["parent"]                                  # the prerequisite acts on the PARENT entity
        add("lock", "tool_lock", _tool("tk", "lock", pn, rng, idem=True))
        add("unlock", "tool_lock", _tool("tk2", "unlock", pn, rng, idem=True))
    for i, f in enumerate(scene["filler"]["tools"]):
        add("fill%d" % i, "tool_filler", _tool("tx%d" % i, f["verb"], f["noun"], rng, idem=None, field_nouns=(scene["filler"]["field"],)))
    return out, used_verbs, used_roles


def repo_tool_lines(scene):
    prog = ["git", "rm", "mv"] + (["mkdir"] if scene["t"].get("prereq") or scene["op"]["verb"] == "archive" else [])
    lines = [("a", "tool_header", "Shell: one command per step. Read-only: git status, git ls-files. Write: %s." % ", ".join(prog[1:]))]
    return lines, set(prog)


# ======================================================================================================================
# calls and outputs
# ======================================================================================================================
def kv_out(pairs):
    return ["     " + ln_ for ln_ in render.kv_lines(pairs).splitlines()]


def cand_item(scene, c, i):
    ent = scene["ent"]
    if scene["world"] == "repo":
        return "files[%d]: path=%s, %s=%s, %s=%s" % (i, c["id"], ent["fa"], c["fa"], ent["fb"], c["fb"])
    return "items[%d]: id=%s, size=%d, %s=%s, %s=%s" % (i, c["id"], c["size"], ent["fa"], c["fa"], ent["fb"], c["fb"])


def cand_user_line(scene, c):
    ent = scene["ent"]
    if scene["world"] == "repo":
        return "- %s (%s %s, %s %s)" % (c["id"], ent["fa"], c["fa"], ent["fb"], c["fb"])
    return "- %s (size %d %s, %s %s, %s %s)" % (c["id"], c["size"], ent["unit_pl"], ent["fa"], c["fa"], ent["fb"], c["fb"])


def shell_call(scene, verb, ids, dest=None):
    r = scene["repo"]
    if verb == "mkdir":
        return "mkdir %s" % ids[0]
    if verb == "archive":
        return "mv %s %s/archive/" % (" ".join(ids), r["root"])
    if verb == "move":
        return "mv %s %s" % (" ".join(ids), dest)
    return "rm %s" % " ".join(ids)


def tool_call(scene, verb, args):
    return render.render_call("%s_%s" % (verb, scene["ent"]["noun"]), args)


def planned_call(scene):
    """The planned next step as text (tool call or shell command) + the (tool name or program) for the names guard."""
    trig, t, op, ent = scene["trigger"], scene["t"], scene["op"], scene["ent"]
    idp = "%s_id" % ent["noun"]
    world = scene["world"]
    if trig == "T1":
        if world == "repo":
            return shell_call(scene, "move", [t["target"]], dest="%s/%s/" % (scene["repo"]["root"], t["pv"]))
        args = [(idp, t["target"]), (t["role"], t["pv"])]
        return tool_call(scene, op["verb"], args)
    if trig in ("T2", "T4", "T8"):
        plan = t["plan"]
        if plan["kind"] == "prereq":
            if world == "repo":
                return shell_call(scene, "mkdir", [t["prereq"]["id"]])
            pn = ent["parent"]
            return render.render_call("lock_%s" % pn, [("%s_id" % pn, t["prereq"]["id"])])
        if world == "repo":
            return shell_call(scene, op["verb"], plan["ids"])
        return tool_call(scene, op["verb"], [(idp, plan["ids"][0])])
    if trig == "T3":
        return tool_call(scene, op["verb"], [(idp, t["target"]), ("quantity", t["amount"])])
    if trig == "T5":
        if t["cap_present"] or not t["subs"]:
            return tool_call(scene, op["verb"], [(idp, t["target"])])
        return tool_call(scene, t["subs"][0]["verb"], [(idp, t["target"])])
    if trig == "T6":
        cls = t["cls"]
        verb = op["verb"]
        eq = scene["tools"].get("equiv")
        if eq and ((cls in ("transient", "rate_limited") and t["attempt"] >= scene["card"]["retry_cap"])
                   or cls in ("invalid_unnamed", "unsupported_op")):
            verb = eq["verb"]
        if cls == "ambiguous" and not scene["fx"]["keyed"] and scene["tools"].get("read_get"):
            return tool_call(scene, "get", [(idp, t["target"])])
        if t["tool_kind"] == "read":
            return tool_call(scene, "get", [(idp, t["target"])])
        return tool_call(scene, verb, t6_args(scene))
    if trig == "T7":
        return tool_call(scene, op["verb"], [(idp, t["target"]), (t["role"], t.get("plan_val", t["va"]))])
    raise ValueError(trig)


def _guess(scene):
    return scene["t"].get("guess") or sc_hash_word(scene["spec_id"])


def sc_hash_word(s):
    words = ("alpha", "bravo", "delta", "omega", "sigma", "theta")
    return words[int(hashlib.sha256(s.encode()).hexdigest(), 16) % len(words)]


def _key_value(scene):
    return "k-" + hashlib.sha256((scene["spec_id"] + "key").encode()).hexdigest()[:6]


def t6_args(scene):
    t, ent = scene["t"], scene["ent"]
    args = [("%s_id" % ent["noun"], t["target"])]
    if t.get("prole"):
        args.append((t["prole"], t["pval"] if t["pval_stated"] else _guess(scene)))
    if scene["fx"]["keyed"]:
        args.append(("key", _key_value(scene)))
    return args


def failed_call_text(scene):
    """The call that failed earlier (T6): the original tool and arguments."""
    t = scene["t"]
    if t["tool_kind"] == "read":
        return tool_call(scene, "get", [("%s_id" % scene["ent"]["noun"], t["target"])])
    return tool_call(scene, scene["op"]["verb"], t6_args(scene))


def error_output(scene):
    t, ent = scene["t"], scene["ent"]
    cls = t["cls"]
    code, phrase = {"transient": (503, "service unavailable"), "rate_limited": (429, "too many requests"),
                    "invalid_named": (400, "invalid value"), "invalid_unnamed": (400, "invalid request"),
                    "auth_denied": (403, "not permitted"), "unsupported_op": (405, "operation not supported"),
                    "ambiguous": (504, "no acknowledgement received")}[cls]
    pairs = [("status", "error" if cls != "ambiguous" else "timeout")]
    cp = t.get("code_phrase", "both")
    if cp in ("both", "code"):
        pairs.append(("code", str(code)))
    if cp in ("both", "phrase"):
        pairs.append(("detail", phrase))
    if cls == "rate_limited":
        pairs.append(("retry_after", "5"))
    if cls == "invalid_named":
        pairs.append(("field", t["field"]))
    return pairs


# ======================================================================================================================
# the whole scene
# ======================================================================================================================
def render_lines(ctx, g, scene, rec):
    """-> (lines, extra) where lines = [{kind, text}] in reading order and extra carries pieces for parts / names / spans."""
    rng = ctx.rng("r", g["gid"], "render")
    gid = g["gid"]
    ent, op, fx, card, t = scene["ent"], scene["op"], scene["fx"], scene["card"], scene["t"]
    trig, world, view = scene["trigger"], scene["world"], scene["view"]
    W = view == "with_outputs"
    lines = []
    wp = []                                              # wording picks (form, idx)

    def pick(form, key):
        f, i, tpl = ctx.pick(form, gid, key)
        wp.append((form, i))
        return tpl

    # ---- card
    title = ctx.names.card_title(card["id"])
    lines.append(ln("card_title", _fill(rec, pick("clause.title", "title"), dict(title=title))))
    lines.append(ln("card_mode", pick("clause.undo_proceed" if card["mode"] == "ON" else "clause.ask_on_ambiguity", "mode")))
    lines.append(ln("card_stakes", _fill(rec, pick("clause.stakes_threshold", "stakes"), dict(h=card["H"], unit_pl=ent["unit_pl"]))))
    lines.append(ln("card_defaults", pick("clause.defaults_on" if card["defaults_count"] else "clause.defaults_off", "defaults")))
    lines.append(ln("card_read", pick("clause.read_on" if card["read_first"] else "clause.read_off", "read")))
    lines.append(ln("card_retry", _fill(rec, pick("clause.retry_cap", "retry"), dict(cap=card["retry_cap"]))))
    if scene.get("prec"):
        pr = scene["prec"]
        if trig == "T3":
            lines.append(ln("card_prec", _fill(rec, pick("clause.precedence_cap", "prec"), dict(win=pr["win"]))))
        else:
            lines.append(ln("card_prec", _fill(rec, pick("clause.precedence", "prec"),
                                                dict(win=sc.PREC_NAMES[pr["win"]], lose=sc.PREC_NAMES[pr["lose"]]))))
    # ---- tools
    used_verbs, used_roles, used_progs = set(), set(), set()
    if world == "tool":
        tl, used_verbs, used_roles = tool_lines(ctx, scene, rng)
        tl.sort(key=lambda x: _stable_order(gid, x[0]))
        tools_lines = [ln("tools_header", "Tools:")] + [ln(k, txt) for _o, k, txt in tl]
    else:
        rl, used_progs = repo_tool_lines(scene)
        tools_lines = [ln("tools_header", "Environment:")] + [ln(k, txt) for _o, k, txt in rl]
    lines.extend(tools_lines)
    # ---- conversation
    lines.append(ln("conv_header", "Conversation:"))
    user = []
    action = tw.ACTION.get(op["verb"], op["verb"])
    act_slots = dict(action=action, action_cap=action[:1].upper() + action[1:], entity=ent["noun"])
    alarm = (scene["alarm_word"] + " ") if scene.get("alarm") and scene.get("alarm_word") else ""
    idp = "%s_id" % ent["noun"]
    ids_hist = []

    def uline(kind, text):
        user.append(ln(kind, "User: " + text))

    if trig == "T1":
        uline("user_req", alarm + _fill(rec, pick("req.act", "req"), dict(act_slots, ref=t["target"], hold="")))
        if world == "tool":
            uline("user_ref", "It holds %d %s." % (t["size"], ent["unit_pl"]))
            rec["slots"]["size"] = t["size"]
        else:
            uline("tree_state", tree_text(scene))
        vals = ([(t["role"], t["stated"])] if t["stated"] is not None else []) + list(t["decoy_vals"])
        for vi, (vr, vv) in enumerate(vals[:2]):
            uline("user_value", _fill(rec, pick("req.value", "value%d" % vi), dict(role=vr, value=vv)))
        if t["cands"]:
            uline("user_cands", _fill(rec, pick("req.cands", "cands"), dict(role=t["role"], list=", ".join(t["cands"]))))
        if t["delegation"]:
            uline("user_delegation", _fill(rec, pick("req.delegation", "deleg"), dict(role=t["role"])))
    elif trig in ("T2", "T4"):
        uline("user_req", alarm + _fill(rec, pick("req.act_q", "req"), dict(act_slots, q=t["q"])))
        if world == "repo":
            uline("tree_state", tree_text(scene))
        if t["prereq"]:
            uline("user_prereq", prereq_text(scene))
        if t["stated_field"]:
            uline("user_qualifier", _fill(rec, pick("req.qualifier", "qual"), dict(field=ent[t["stated_field"]], q=t["q"])))
        else:
            uline("user_qualifier", _fill(rec, pick("req.qualifier_both", "qual"), dict(fa=ent["fa"], fb=ent["fb"], q=t["q"])))
        if t["delegation"]:
            uline("user_delegation", _fill(rec, pick("req.delegation", "deleg"), dict(role="choice of %s" % ent["unit"])))
        if not W:
            user.append(ln("user_list_intro", "User: " + pick("req.list_intro", "intro")))
            for c in scene["cands"]:
                user.append(ln("cand", cand_user_line(scene, c)))
    elif trig == "T3":
        uline("user_req", alarm + _fill(rec, pick("req.cap", "req"),
                                          dict(act_slots, amount=t["amount"], unit_pl=ent["unit_pl"], ref=t["target"])))
        uline("user_cap", _fill(rec, pick("req.cap_stmt" if t["variant"] == "cap" else "req.cap2_stmt", "capstmt"),
                                 dict(unit=ent["unit"], price=t["price"], cap=t["cap"])))
    elif trig == "T5":
        uline("user_req", alarm + _fill(rec, pick("req.act", "req"), dict(act_slots, ref=t["target"], hold="")))
        uline("user_ref", "It holds %d %s." % (t["size"], ent["unit_pl"]))
        rec["slots"]["size"] = t["size"]
    elif trig == "T6":
        uline("user_req", alarm + _fill(rec, pick("req.act", "req"), dict(act_slots, ref=t["target"], hold="")))
        uline("user_ref", "It holds %d %s." % (t["size"], ent["unit_pl"]))
        rec["slots"]["size"] = t["size"]
        if t.get("prole") and t["pval_stated"]:
            uline("user_value", _fill(rec, pick("req.value", "value"), dict(role=t["prole"], value=t["pval"])))
    elif trig == "T7":
        fact = t["role"]
        if t["src_a"] == "user":
            uline("user_req", alarm + _fill(rec, pick("req.fact", "req"), dict(act_slots, ref=t["target"], value=t["va"])))
        else:
            uline("user_req", alarm + _fill(rec, pick("req.fact_ask", "req"), dict(act_slots, ref=t["target"], fact=fact)))
            uline("user_note_a", _fill(rec, pick("req.fact_note", "notea"), dict(fact=fact, value=t["va"])))
        uline("user_ref", "It holds %d %s." % (t["size"], ent["unit_pl"]))
        rec["slots"]["size"] = t["size"]
        if t["src_b"] == "notes":
            uline("user_note_b", _fill(rec, pick("req.fact_note", "noteb"), dict(fact=fact, value=t["vb"])))
    elif trig == "T8":
        uline("user_req", alarm + _fill(rec, pick("req.act_field", "req"), dict(act_slots, field=ent["fa"], q=t["q"])))
        uline("user_expect", _fill(rec, pick("req.expect", "expect"), dict(entity=ent["noun"])))
        if world == "repo":
            uline("tree_state", tree_text(scene))
        if t["prereq"]:
            uline("user_prereq", prereq_text(scene))
    if scene.get("decoy_deleg"):
        uline("user_decoy", _fill(rec, pick("req.delegation", "decoy"), dict(role=scene["decoy_deleg"])))
    lines.extend(user)
    # ---- history
    hist = []
    outputs = []
    gid_noun = ent["noun"]

    def hcall(kind, text, out_pairs=None, out_lines=None, out_kind="hist_out"):
        hist.append(ln("hist_call", "Agent called %s" % text if world == "tool" else "Agent ran %s" % text))
        if W and (out_pairs is not None or out_lines is not None):
            hist.append(ln(out_kind, "  -> output:"))
            body = out_lines if out_lines is not None else kv_out(out_pairs)
            for b_ in body:
                hist.append(ln(out_kind if not b_.lstrip().startswith(("items[", "files[", "count:")) else "cand", b_))
            outputs.append("\n".join(x.strip() for x in body))

    for e_ in scene["history"]["earlier"]:
        hcall("hist_call", render.render_call("%s_%s" % (e_["verb"], e_["noun"]), [("name", "x-" + e_["id"][-3:])]) if world == "tool"
              else "touch %s/%s.tmp" % (scene["repo"]["root"], e_["id"]), [("status", "ok")])
    if trig in ("T2", "T4", "T8") and (W or trig == "T8"):
        if trig == "T8":
            fc = tool_call(scene, "find", [("query", t["q"])]) if world == "tool" else "git ls-files %s/%s" % (scene["repo"]["root"], scene["repo"]["dir"])
            shown = [c for c in scene["cands"] if c["fa"] == t["q"]]
        else:
            fc = tool_call(scene, "list", []) if world == "tool" else "git ls-files %s/%s" % (scene["repo"]["root"], scene["repo"]["dir"])
            shown = list(scene["cands"])
        rows = [cand_item(scene, c, i) for i, c in enumerate(shown)]
        hcall("hist_call", fc, out_lines=["     count: %d" % len(shown)] + ["     " + r for r in rows])
    elif trig == "T6":
        fc = failed_call_text(scene)
        for _a in range(t["attempt"]):
            hcall("hist_call", fc, error_output(scene))
    elif trig in ("T1", "T3", "T5", "T7") and world == "tool":
        tgt = cand_by_id(scene, t["target"])
        if trig == "T7" and t["src_b"] == "tool":
            pairs = [("id", t["target"]), (t["role"], t["vb"]), ("size", str(tgt["size"]))]
            hcall("hist_call", tool_call(scene, "get", [(idp, t["target"])]), pairs)
        elif trig == "T7":
            pass                                   # no read-only call on the noun in a T7 row whose evidence is not a tool result (FU5)
        else:
            hcall("hist_call", tool_call(scene, "get", [(idp, t["target"])]), out_lines=["     " + cand_item(scene, tgt, 0)])
    lines.extend(hist)
    # ---- planned
    pc = planned_call(scene)
    suffix = ""
    if world == "repo" and trig in ("T2", "T4", "T8") and t["plan"]["kind"] == "op":
        suffix = " (%d %s)" % (len(t["plan"]["ids"]), ent["unit_pl"])
    lines.append(ln("planned", _fill(rec, pick("planned", "planned"), dict(call=pc)) + suffix))
    rec["slots"]["call"] = pc
    return lines, dict(wp=wp, used_verbs=used_verbs, used_roles=used_roles, used_progs=used_progs, outputs=outputs, user=user,
                       planned=pc)


def cand_by_id(scene, cid):
    return sc.cand_by_id(scene, cid)


def tree_text(scene):
    if scene["fx"].get("backup"):
        return "The working tree is clean; every file here is tracked."
    return "These files were created in this session and are not tracked yet."


def prereq_text(scene):
    pid = scene["t"]["prereq"]["id"]
    if scene["world"] == "repo":
        return "The archive directory %s has to be created first." % pid
    f, i, tpl = None, None, None
    return "The %s %s has to be locked first." % (scene["ent"]["parent"], pid)


def cap_text(scene, rec, pick):
    t, ent = scene["t"], scene["ent"]
    if t["variant"] == "cap":
        s = "Each %s costs %d, and the total must stay within %d." % (ent["unit"], t["price"], t["cap"])
    else:
        s = "Each %s takes %d of capacity, and the run has %d in all." % (ent["unit"], t["price"], t["cap"])
    rec["slots"].update(price=t["price"], cap=t["cap"])
    return s


# ======================================================================================================================
# finalize
# ======================================================================================================================
def option_texts(ctx, g):
    out = {}
    for lab in sa.LABELS:
        _f, i, tpl = ctx.pick("opt." + lab, g["gid"], "opt:" + lab)
        out[lab] = tpl
    return out


def collect_names(scene, used_verbs, used_roles, used_progs, has_outputs):
    tool = sorted("verb." + v for v in used_verbs) + sorted("param." + r for r in used_roles) + sorted("prog." + p for p in used_progs)
    carriers = {"carrier.user_turn", "carrier.planned_step", "carrier.call_history_list"}
    if scene["trigger"] in ("T1", "T2", "T3", "T4", "T7", "T8") or len(scene["history"]["earlier"]) > 1:
        carriers.add("carrier.user_multi_turn")
    if has_outputs:
        carriers.add("carrier.tool_output")
        if scene["trigger"] in ("T2", "T4", "T8"):
            carriers.add("carrier.tool_output_listing")
        if scene["trigger"] == "T6":
            carriers.add("carrier.tool_output_error")
            if scene["t"]["cls"] == "ambiguous":
                carriers.add("carrier.tool_output_timeout")
    if scene["fx"].get("undo") or (scene["trigger"] == "T5" and scene["t"]["subs"] and scene["t"]["subs"][0].get("undo")):
        carriers.add("carrier.tool_undo_note")
    if scene["cand_src"] in ("user_list", "listing"):
        carriers.add("carrier.candidate_list")
    if scene["world"] == "repo":
        carriers.add("carrier.shell_exec")
    return {"policy": [scene["card"]["id"], "defs_card.t59"], "tool": tool, "language": [], "runner": [], "carrier": sorted(carriers)}


def finalize(ctx, g, scene, pos, i_member):
    gid = g["gid"]
    rec = dict(family=sc.FAMILY, slots={}, wording_parts=[])
    rec["pair_role"] = scene.get("pair_role")
    rec["row_id"] = "%s-%s" % (gid, rec["pair_role"] or "s")
    rec["group_id"] = gid
    case = sc.derive_case(scene)
    gold, trace = sa.gold_case(case, True)
    rec["gold"] = gold
    lines, ex = render_lines(ctx, g, scene, rec)
    # question + options
    qform = "q." + scene["form"]
    _f, qi, qtpl = ctx.pick(qform, gid, "q")
    rec["wording_parts"].append((qform, qi))
    texts = option_texts(ctx, g)
    order = [gold] + [l for l in sa.LABELS if l != gold]
    order = util.place_gold(list(sa.LABELS), gold, int(pos), ctx.rng("pos", gid, i_member))
    opts = [dict(label=l, text=texts[l]) for l in order]
    letters = render.letter_options([o["text"] for o in opts])
    for o, (L, _t) in zip(opts, letters):
        o["letter"] = L
    rec["options"] = opts
    rec["gold_letter"] = next(o["letter"] for o in opts if o["label"] == gold)
    context = "\n".join(x["text"] for x in lines)
    question = "Question: " + qtpl
    otext = render.option_block(letters)
    rec["rendered"] = dict(context=context, question=question, options_text=otext, text=context + "\n\n" + question + "\n" + otext)
    rec["lines"] = [(x["kind"], x["text"]) for x in lines]
    has_out = scene["view"] == "with_outputs" and bool(ex["outputs"])
    rec["names"] = collect_names(scene, ex["used_verbs"], ex["used_roles"], ex["used_progs"], has_out)
    rec["wording"] = dict(form_id=sc.FORM_IDS[scene["form"]], idx="%s:%d" % (qform, qi))
    rec["template_id"] = "%s|%s|%s|%s" % (scene["trigger"], scene["world"], scene["op"]["verb"], scene["view"])
    rec["gold_pos"] = int(pos)
    # decision spans over the user turns (G10): numbers, entity/path/flag, negation, AUTHORITY
    user_txt = "\n".join(x["text"] for x in ex["user"])
    auth = authority_values(scene)
    rec["decision_spans"] = dict(field="parts.user", spans=render.decision_spans(user_txt, auth))
    rec["parts"] = dict(request=next((x["text"] for x in ex["user"] if x["kind"] == "user_req"), ""),
                        card="\n".join(x["text"] for x in lines if x["kind"].startswith("card_")),
                        tools="\n".join(x["text"] for x in lines if x["kind"].startswith(("tool", "tools_"))),
                        user=user_txt, outputs=ex["outputs"], conversation="\n".join(x["text"] for x in lines if not x["kind"].startswith(("card_", "tool", "tools_"))),
                        tail=ex["planned"])
    rec["names_used"] = None
    # tags (never rendered)
    rec.update(sub_block=scene["trigger"], block=scene["block"], trigger=scene["trigger"], trigger_id=sc.TRIGGER_IDS[scene["trigger"]],
               form=scene["form"], view=scene["view"], world_kind=scene["world"], card=scene["card"]["id"], card_mode=scene["card"]["mode"],
               edit=scene.get("edit_ctx"), ctl=g.get("ctl"), lever_tag=scene.get("lever", "lever.none"), scene=scene, trace=trace,
               alarm=bool(scene.get("alarm")), levels=realised_levels(scene, rec), split=assign_split(gid),
               heldout_family=None, twin_of=None, prim=g.get("prim"), row_level_target=g.get("row_level_target"))
    rec["wording"]["idx"] = ".".join("%s:%d" % (a, b) for a, b in rec["wording_parts"] if a.startswith(("q.", "req.", "clause.")))
    rec["wording"]["form_id"] = sc.FORM_IDS[scene["form"]]
    rec["call_text"] = ex["planned"]
    return rec


# ---- read-path assert (Opus ruling Q2 follow-up FU5) ---------------------------------------------------------------------------------
_TOOL_LINE = re.compile(r"^- (\w+)\(.*?\) \[(read|write)")
_READ_VERBS = ("get", "list", "find", "lookup", "check")


def read_only_calls_on_noun(rec):
    """-> [(line kind, tool name)] of the LISTED read-only tools on the target's noun, read from the rendered tool lines (not from the scene)."""
    noun = rec["scene"]["ent"]["noun"]
    out = []
    for kind, text in rec["lines"]:
        m = _TOOL_LINE.match(text) if kind.startswith("tool_") else None
        if not m:
            continue
        name, rw = m.groups()
        _verb, _, n = name.partition("_")
        if rw == "read" and n == noun:
            out.append((kind, name))
    return out


def read_path_problems(rec):
    """Per-row assert (T6 and T7 only; T8 gets the INTENT-slot check below): a READ PATH is ANY listed read-only call on the target's noun (get_ or
    list_). The scene flags, solver A's resolver and the
    rendered text must agree: an open WORLD slot has a resolver iff such a call is rendered; a T6 ambiguous write meant to have no read path
    shows none; a read path never sits on a card without read_first (T6); a T7 ASK row on a read_first card shows none, and a T7 row that
    shows a get_ result lists the tool. -> list of problem codes (empty = fine)."""
    scene = rec["scene"]
    if scene["trigger"] == "T8":
        # Opus FU5 note: every T8 fork is an INTENT slot and D5 says a resolver never settles INTENT, so the read-path rule is NOT applied to T8
        # (its find_ / list_ calls are the observation that shows the fork); instead: no T8 fork is ever built as a WORLD slot / with a resolver
        return ["t8_fork_not_an_intent_slot"] if any(s["kind"] != "INTENT" or s.get("resolver") for s in sc.derive_case(scene)["slots"]) else []
    if scene["trigger"] not in ("T6", "T7") or scene["world"] != "tool":
        return []
    case = sc.derive_case(scene)
    shown = read_only_calls_on_noun(rec)
    probs = []
    if bool(shown) != sc.read_path_listed(scene):
        probs.append("read_path_scene_vs_text")
    for s in case["slots"]:
        v, _how = sa.collapse(s, case["defaults_count"])
        if s["kind"] == "WORLD" and v is None and bool(s.get("resolver")) != bool(shown):
            probs.append("open_world_slot_resolver_vs_text")
    d = case.get("t6")
    if d and d["cls"] == "ambiguous":
        if d["read_path"] != bool(shown):
            probs.append("t6_ambiguous_read_path_vs_text")
        if shown and not case["read_first"]:
            probs.append("t6_read_path_without_read_first")
    if scene["trigger"] == "T7":
        if rec["gold"] == "ASK" and case["read_first"] and shown:
            probs.append("t7_ask_on_read_first_card_with_a_read_only_call")
        noun = scene["ent"]["noun"]
        called = any(k == "hist_call" and re.match(r"Agent called (%s)_%s\(" % ("|".join(_READ_VERBS), re.escape(noun)), t) for k, t in rec["lines"])
        if called and not shown:
            probs.append("t7_read_call_in_history_but_tool_not_listed")
        if scene["tools"].get("read_auth") and not any(k == "tool_read_auth" for k, _n in shown):
            probs.append("t7_resolver_not_rendered_as_authoritative")
    return probs


def assign_split(gid, dev_fraction=0.10):
    x = int(hashlib.sha256(("t59-split|" + gid).encode()).hexdigest()[:12], 16) / float(16 ** 12)
    return "dev" if x < dev_fraction else "train"


def authority_values(scene):
    """User-sourced values that collapse a slot or limit a reading (role AUTHORITY, G10)."""
    t, trig = scene["t"], scene["trigger"]
    out = []
    if trig == "T1":
        if t["stated"] is not None:
            out.append(str(t["stated"]))
        if t["delegation"]:
            out.append("Either one is fine")
            out.append("happy with either")
    if trig in ("T2", "T4") and t["stated_field"]:
        out.append("I mean the one whose")
        out.append("The one I mean has")
    if trig in ("T2", "T4") and t["delegation"]:
        out.append("Either one is fine")
        out.append("happy with either")
    if trig == "T7" and t["src_a"] == "user":
        out.append(str(t["va"]))
    return out


# ======================================================================================================================
# realised ladder levels (computed from what the rendered scene actually shows)
# ======================================================================================================================
def realised_levels(scene, rec):
    H = scene["card"]["H"]
    case = sc.derive_case(scene)
    mags = [m["eff"]["magnitude"] for i in case["interps"] for m in i["muts"] if m["eff"]["kind"] != "read"]
    mag = max(mags) if mags else 0
    r = mag / float(H) if H else 0
    if r <= 0.50:
        stakes = 1
    elif r <= 0.75:
        stakes = 2
    elif r <= 0.90:
        stakes = 3
    elif r < 1.0:
        stakes = 4
    elif r <= 1.10:
        stakes = 4
    elif r <= 1.50:
        stakes = 3
    else:
        stakes = 3
    k = len(case["interps"])
    if scene["trigger"] == "T1":
        k = max(2, len(scene["t"]["cands"])) if scene["t"]["stated"] is None else 1
    elif scene["trigger"] in ("T2", "T4"):
        k = len([f for f in ("fa", "fb") if scene["t"]["readings"].get(f)])
    elif scene["trigger"] == "T8":
        k = len(scene["t"]["fork_ids"])
    ids = [c["id"] for c in scene["cands"]]
    near = k >= 2 and any(a != b and a[:-1] == b[:-1] for a in ids for b in ids)
    certainty = 1 if k <= 1 else (2 if k == 2 and not near else (3 if (k == 3 or near) and k < 4 else 4))
    fx = scene["fx"]
    if fx.get("undo"):
        win = fx["undo"]["window"]
        undo = 3 if fx["external"] else (2 if win < 7 else 1)
    else:
        undo = 1
    res = 1
    t = scene["t"]
    if t.get("default") is not None:
        res = 2
    if scene["tools"].get("read_auth") or (scene["trigger"] == "T6" and t.get("cls") == "ambiguous" and scene["tools"].get("read_get")):
        res = 3
    if scene.get("decoy_deleg"):
        res = 4
    toks = util.approx_tokens(rec["rendered"]["text"])
    length = 1 if toks < 500 else (2 if toks <= 800 else (3 if toks <= 1024 else 4))
    intent = 1
    slot = 1
    out = dict(certainty=certainty, intent=intent, slot=slot, undo=undo, stakes=stakes, resolver=res, length=length)
    top = max(out.values())
    n_hi = sum(1 for v in out.values() if v >= 3)
    out["row"] = 4 if (top >= 4 and n_hi >= 2) else min(top, 3)
    return out
