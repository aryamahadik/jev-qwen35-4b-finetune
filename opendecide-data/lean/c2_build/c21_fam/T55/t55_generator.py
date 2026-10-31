"""T55 RECOVER-ESCALATE generator (CODE ONLY: no rows are written; `generate_in_memory` returns records for unit tests
and the 20-example dry run). Clean-room: built from G0_LITE.md + G0_APPROVALS only. Labels come from SOLVER A only
(t55_solver_a.gold_label); text is rendered from the structured record (t55_render)."""
import collections
import copy
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_ROOT, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from tool_engine import invariants, names as names_mod, perturb, state, util  # noqa: E402
import t55_solver_a as sa  # noqa: E402
import t55_wording as tw  # noqa: E402

FAMILY = "T55"
SUB_BLOCKS = ("b1_classic", "b4_blind_retry", "b2_ambig_write", "b3_implicit", "b5_deny_escalate", "b6_loop_poll")
SIZES = {"b1_classic": 900, "b4_blind_retry": 400, "b2_ambig_write": 600, "b3_implicit": 500, "b5_deny_escalate": 300,
         "b6_loop_poll": 300}
TOTAL = 3000
ARCHETYPES = ("arch.records", "arch.schedule", "arch.messages", "arch.files", "arch.jobs", "arch.inventory",
              "arch.accounts", "arch.tickets", "arch.metrics", "arch.queue")
ARCH_VERBS = {
    "arch.records": ["get", "list", "find", "create", "update", "delete", "count", "archive", "restore", "merge"],
    "arch.schedule": ["schedule", "cancel", "list", "get", "reserve", "release", "move", "check", "close", "lookup"],
    "arch.messages": ["send", "list", "get", "search", "archive", "delete", "read", "restore", "export", "lookup"],
    "arch.files": ["read", "list", "copy", "move", "rename", "delete", "find", "export", "check", "lookup"],
    "arch.jobs": ["create", "cancel", "check", "list", "get", "close", "approve", "sync", "assign", "lookup"],
    "arch.inventory": ["count", "reserve", "release", "add", "remove", "update", "list", "find", "get", "set"],
    "arch.accounts": ["get", "create", "update", "close", "assign", "lookup", "list", "set", "check", "approve"],
    "arch.tickets": ["create", "assign", "close", "list", "search", "update", "approve", "get", "cancel", "lookup"],
    "arch.metrics": ["get", "list", "count", "export", "sync", "check", "find", "lookup", "set", "read"],
    "arch.queue": ["add", "remove", "list", "count", "get", "cancel", "merge", "move", "check", "release"],
}
READ_V = sorted(v for v in state.READ_VERBS if v in state.VERBS_T55)      # sorted: a set's iteration order differs between processes
IDEM_V = [v for v in sorted(state.DEFAULT_IDEMPOTENT) if v in state.VERBS_T55 and v not in state.READ_VERBS]
PLAIN_V = [v for v in state.VERBS_T55 if v not in state.READ_VERBS and v not in state.DEFAULT_IDEMPOTENT]

# ---- entries ---------------------------------------------------------------------------------------------------
# cell codes: B1 rule path (r1, r2eq, r2noeq, r4v, r4nv, r5eq, r5noeq, r6, r7eq, r7ask, r7stop, r8eq, r8ask, r8stop, r9)
ENTRIES = {
    "b1_classic": [
        dict(name="p_att_sw", size=2, rows=140, edit="attempt", cells=("r1", "r2eq"), labels=("RETRY", "SWITCH_TOOL")),
        dict(name="p_class", size=2, rows=100, edit="class", cells=("r4v", "r5eq"), labels=("FIX_ARGS", "SWITCH_TOOL")),
        dict(name="p_eq_ask", size=2, rows=60, edit="eq", cells=("r8eq", "r8ask"), labels=("SWITCH_TOOL", "ASK")),
        dict(name="p_esc", size=2, rows=50, edit="card", cells=("r7ask", "r7stop"), labels=("ASK", "STOP")),
        dict(name="p_val", size=2, rows=50, edit="value", cells=("r4v", "r4nv"), labels=("FIX_ARGS", "ASK")),
        dict(name="s_retry", size=1, rows=110, cells=("r1",), labels=("RETRY",)),
        dict(name="s_fix", size=1, rows=105, cells=("r4v",), labels=("FIX_ARGS",)),
        dict(name="s_sw_a", size=1, rows=15, cells=("r7eq",), labels=("SWITCH_TOOL",)),
        dict(name="s_sw_b", size=1, rows=15, cells=("r8eq",), labels=("SWITCH_TOOL",)),
        dict(name="s_ask_a", size=1, rows=35, cells=("r2noeq",), labels=("ASK",)),
        dict(name="s_ask_b", size=1, rows=35, cells=("r5noeq",), labels=("ASK",)),
        dict(name="s_ask_c", size=1, rows=55, cells=("r6",), labels=("ASK",)),
        dict(name="s_ask_d", size=1, rows=20, cells=("r8ask",), labels=("ASK",)),
        dict(name="s_stop_a", size=1, rows=35, cells=("r7stop",), labels=("STOP",)),
        dict(name="s_stop_b", size=1, rows=30, cells=("r8stop",), labels=("STOP",)),
        dict(name="s_stop_c", size=1, rows=45, cells=("r9",), labels=("STOP",)),
    ],
    # B4: X appends the named-argument detail, Y has none; V = corrected value in context, E = equivalent tool listed
    "b4_blind_retry": [
        dict(name="b4_TT", size=2, rows=240, V=True, E=True, labels=("FIX_ARGS", "SWITCH_TOOL")),
        dict(name="b4_TF", size=2, rows=80, V=True, E=False, labels=("FIX_ARGS", "ASK")),
        dict(name="b4_FT", size=2, rows=40, V=False, E=True, labels=("ASK", "SWITCH_TOOL")),
        dict(name="b4_FF", size=2, rows=40, V=False, E=False, labels=("ASK", "ASK")),
    ],
    "b2_ambig_write": [
        dict(name="p_key", size=2, rows=120, edit="key", labels=("RETRY_KEYED", "READ_BACK")),
        dict(name="p_rp", size=2, rows=120, edit="readpath", labels=("READ_BACK", "ASK")),
        dict(name="p_com", size=2, rows=150, edit="committed", labels=("NO_RETRY", "RETRY_PLAIN")),
        dict(name="s_keyed", size=1, rows=90, labels=("RETRY_KEYED",)),
        dict(name="s_read", size=1, rows=30, labels=("READ_BACK",)),
        dict(name="s_ask", size=1, rows=90, labels=("ASK",)),
    ],
    # B3: (violating row, benign ACCEPT twin of the same result shape); a = attempt index
    "b3_implicit": [
        dict(name="p_retry", size=2, rows=80, labels=("RETRY", "ACCEPT"), a=1, kind="data_read"),
        dict(name="p_fix_first", size=2, rows=40, labels=("FIX_ARGS", "ACCEPT"), a=1, kind="arg"),
        dict(name="p_fix_rec", size=2, rows=40, labels=("FIX_ARGS", "ACCEPT"), a=2, kind="arg"),
        dict(name="p_switch", size=2, rows=60, labels=("SWITCH_TOOL", "ACCEPT"), a=2, kind="data_read_eq"),
        dict(name="p_ask_wf", size=2, rows=50, labels=("ASK", "ACCEPT"), a=1, kind="write"),
        dict(name="p_ask_wr", size=2, rows=10, labels=("ASK", "ACCEPT"), a=2, kind="write"),
        dict(name="p_ask_rr", size=2, rows=40, labels=("ASK", "ACCEPT"), a=2, kind="data_read_noeq"),
        dict(name="s_retry", size=1, rows=40, labels=("RETRY",), a=1, kind="data_read"),
        dict(name="s_fix_first", size=1, rows=25, labels=("FIX_ARGS",), a=1, kind="arg"),
        dict(name="s_fix_rec", size=1, rows=25, labels=("FIX_ARGS",), a=2, kind="arg"),
        dict(name="s_switch", size=1, rows=40, labels=("SWITCH_TOOL",), a=2, kind="data_read_eq"),
        dict(name="s_ask_wf", size=1, rows=15, labels=("ASK",), a=1, kind="write"),
        dict(name="s_ask_wr", size=1, rows=15, labels=("ASK",), a=2, kind="write"),
        dict(name="s_ask_rr", size=1, rows=20, labels=("ASK",), a=2, kind="data_read_noeq"),
    ],
    "b5_deny_escalate": [
        dict(name="p_consec", size=2, rows=140, edit="consec", labels=("CONTINUE_ALT", "ESCALATE")),
        dict(name="p_second", size=2, rows=30, edit="second", labels=("CONTINUE_ALT", "ESCALATE")),
        dict(name="s_cont", size=1, rows=35, labels=("CONTINUE_ALT",)),
        dict(name="s_esc_noalt", size=1, rows=25, labels=("ESCALATE",), why="noalt"),
        dict(name="s_esc_thr", size=1, rows=25, labels=("ESCALATE",), why="thr"),
        dict(name="s_stop", size=1, rows=45, labels=("STOP",)),
    ],
    "b6_loop_poll": [
        dict(name="p_prog_b", size=2, rows=70, edit="progress", labels=("KEEP_POLLING", "BREAK_LOOP_ALT")),
        dict(name="p_prog_e", size=2, rows=50, edit="progress", labels=("KEEP_POLLING", "ESCALATE")),
        dict(name="p_prog_s", size=2, rows=40, edit="progress", labels=("KEEP_POLLING", "STOP")),
        dict(name="s_keep", size=1, rows=40, labels=("KEEP_POLLING",), why="stale_lt_L"),
        dict(name="s_break", size=1, rows=40, labels=("BREAK_LOOP_ALT",)),
        dict(name="s_esc_cap", size=1, rows=15, labels=("ESCALATE",), why="cap"),
        dict(name="s_esc_noalt", size=1, rows=20, labels=("ESCALATE",), why="noalt"),
        dict(name="s_stop", size=1, rows=25, labels=("STOP",)),
    ],
}
LABEL_MIX = {
    "b1_classic": {"RETRY": .20, "FIX_ARGS": .20, "SWITCH_TOOL": .20, "ASK": .25, "STOP": .15},
    "b4_blind_retry": {"FIX_ARGS": .40, "SWITCH_TOOL": .35, "ASK": .25},          # spec Y-STOP 10% folded into ASK (see notes)
    "b2_ambig_write": {"RETRY_KEYED": .25, "READ_BACK": .25, "ASK": .25, "NO_RETRY": .125, "RETRY_PLAIN": .125},
    "b3_implicit": {"ACCEPT": .32, "RETRY": .16, "FIX_ARGS": .18, "SWITCH_TOOL": .14, "ASK": .20},
    "b5_deny_escalate": {"CONTINUE_ALT": .40, "ESCALATE": .45, "STOP": .15},
    "b6_loop_poll": {"KEEP_POLLING": .40, "BREAK_LOOP_ALT": .25, "ESCALATE": .20, "STOP": .15},
}
# channel combinations for the error class (code / phrase / hint): 30% single, 40% double, 30% triple (P-9)
CHAN_COMBOS = [("code",), ("phrase",), ("hint",), ("code", "phrase"), ("code", "hint"), ("phrase", "hint"),
               ("code", "phrase", "hint")]
CHAN_W = {0: 10, 1: 10, 2: 10, 3: 13.34, 4: 13.33, 5: 13.33, 6: 30}
# B5 cards: published settings (3 consecutive / 20 total ; 3 consecutive / 10 of the last 50) plus variants
B5_CARDS_CT = [(kc, kt) for kc in (2, 3, 4) for kt in (10, 20, 30)]
B5_CARDS_W = [(kc, kt) for kc in (2, 3, 4) for kt in (None, 20)]
ESC_OPTIONS = ("ASK", "STOP")


class Ctx:
    def __init__(self, seed="t55-v1", standin=False, pool=None, names_src=None):
        self.seed = seed
        self.names = names_src or names_mod.NameSource(FAMILY, seed=seed, standin=standin)
        self.pool = pool or tw.seed_pool()
        self.pool.balanced = True                       # every wording of a form is used equally often (see WordingPool)

    def rng(self, *parts):
        return util.rng_for(self.seed, *parts)

    def pick(self, form_id, gid, key, fallback=None):
        return self.pool.pick(form_id, self.rng("w", gid, key), fallback, key=(gid, key))


# =============================================================================================================
# plan
# =============================================================================================================
def alloc_entries(n_rows, entries):
    if not any(e["size"] == 1 for e in entries):               # pair-only sub-block (B4): allocate whole groups
        return util.largest_remainder(n_rows // 2, {e["name"]: e["rows"] / 2.0 for e in entries})
    raw = util.largest_remainder(n_rows, {e["name"]: e["rows"] for e in entries})
    groups, left = {}, 0
    for e in entries:
        gcount = raw[e["name"]] // e["size"]
        groups[e["name"]] = gcount
        left += raw[e["name"]] - gcount * e["size"]
    singles = [e for e in entries if e["size"] == 1]
    if singles and left:                                   # rounding leftovers go to the single-row entries, pro rata
        extra = util.largest_remainder(left, {e["name"]: e["rows"] for e in singles})
        for k, v in extra.items():
            groups[k] += v
    return groups


def build_plan(total=TOTAL, seed="t55-plan-v1"):
    sizes = util.largest_remainder(total, SIZES)
    plan = []
    for sb in SUB_BLOCKS:
        alloc = alloc_entries(sizes[sb], ENTRIES[sb])
        for e in ENTRIES[sb]:
            for i in range(alloc[e["name"]]):
                plan.append(dict(gid="%s-%s-%05d" % (sb[:2], e["name"], i), sub_block=sb, entry=e["name"], spec=e))
    util.rng_for(seed, "order").shuffle(plan)
    # balanced gold positions per (sub-block, label)
    by_key = collections.defaultdict(list)
    for g in plan:
        for i in range(g["spec"]["size"]):
            by_key[(g["sub_block"], g["spec"]["labels"][i])].append((g["gid"], i))
    pos_of = {}
    for key, items in by_key.items():
        k = len(OPTION_LABELS[key[0]])
        for (gid_, i), pv in zip(items, util.balanced_cycle(len(items), k, util.rng_for(seed, "pos", *key))):
            pos_of[(gid_, i)] = pv
    for g in plan:
        g["pos"] = [pos_of[(g["gid"], i)] for i in range(g["spec"]["size"])]
    # channels for the explicit-error rows (B1, B4): the 30 / 40 / 30 channel mix holds INSIDE every entry (an entry fixes the label or
    # the label pair of its rows, so a mix balanced only over the sub-block would drift between entries by chance)
    for sb in ("b1_classic", "b4_blind_retry"):
        for ent in ENTRIES[sb]:
            errg = [g for g in plan if g["sub_block"] == sb and g["entry"] == ent["name"]]
            cnt = util.largest_remainder(len(errg), {i: CHAN_W[i] for i in range(7)})
            seq = [i for i in range(7) for _ in range(cnt[i])]
            util.rng_for(seed, "chan", sb, ent["name"]).shuffle(seq)
            for g, c in zip(errg, seq):
                g["chan"] = CHAN_COMBOS[c]
    # B5 card kind: window cards on 40% of the groups, balanced; configs cycled so no config exceeds its share
    b5 = [g for g in plan if g["sub_block"] == "b5_deny_escalate"]
    wcount = int(round(0.4 * len(b5)))
    kinds = [True] * wcount + [False] * (len(b5) - wcount)
    util.rng_for(seed, "b5kind").shuffle(kinds)
    cfg_w = util.balanced_cycle(sum(kinds), len(B5_CARDS_W), util.rng_for(seed, "b5w"))
    cfg_c = util.balanced_cycle(len(b5) - sum(kinds), len(B5_CARDS_CT), util.rng_for(seed, "b5c"))
    iw = ic = 0
    for g, w in zip(b5, kinds):
        if w:
            g["b5"] = dict(window=True, kc=B5_CARDS_W[cfg_w[iw]][0], kt=B5_CARDS_W[cfg_w[iw]][1], kw=10, W=50)
            iw += 1
        else:
            g["b5"] = dict(window=False, kc=B5_CARDS_CT[cfg_c[ic]][0], kt=B5_CARDS_CT[cfg_c[ic]][1], kw=None, W=None)
            ic += 1
    # published settings must be present in every B5 plan of >= 20 groups
    if len(b5) >= 20:
        if not any((not g["b5"]["window"]) and g["b5"]["kc"] == 3 and g["b5"]["kt"] == 20 for g in b5):
            b5[0]["b5"] = dict(window=False, kc=3, kt=20, kw=None, W=None)
        if not any(g["b5"]["window"] and g["b5"]["kc"] == 3 and g["b5"]["kt"] is None for g in b5):
            b5[1]["b5"] = dict(window=True, kc=3, kt=None, kw=10, W=50)
    vt_i = collections.Counter()
    for g in plan:
        if g["sub_block"] == "b3_implicit":
            kk = g["spec"].get("kind") == "arg"
            g["vt"] = vt_i[kk]
            vt_i[kk] += 1
    # card caps, escalation-table values, tool-list size and polling-call style: balanced INSIDE every entry (same reason as the channels)
    for sb in SUB_BLOCKS:
        for ent in ENTRIES[sb]:
            gs_ = [g for g in plan if g["sub_block"] == sb and g["entry"] == ent["name"]]
            n_ = len(gs_)
            for key, vals in (("R_cap", (2, 3)), ("esc_q", ESC_OPTIONS), ("esc_u", ESC_OPTIONS), ("n_tools", tuple(range(3, 13))),
                              ("identical_calls", (True, False))):
                for g, c in zip(gs_, util.balanced_cycle(n_, len(vals), util.rng_for(seed, "attr", key, sb, ent["name"]))):
                    g[key] = vals[c]
    return plan


OPTION_LABELS = {"b1_classic": sa.B1_LABELS, "b4_blind_retry": sa.B1_LABELS, "b2_ambig_write": sa.B2_LABELS,
                 "b3_implicit": sa.B3_LABELS, "b5_deny_escalate": sa.B5_LABELS, "b6_loop_poll": sa.B6_LABELS}


# =============================================================================================================
# world
# =============================================================================================================
# Target verbs are drawn ONLY from verbs that have a synonym on the list, for every kind and every label, so that "an
# equivalent tool is listed" never correlates with the verb. Idempotent / keyed writes are set by the tool's explicit flag.
TARGET_READ_V = ["get", "read", "lookup", "find", "search"]
TARGET_WRITE_V = ["create", "add", "update", "set", "remove", "delete"]


def _kind_verbs(kind):
    return {"read": TARGET_READ_V, "idem": TARGET_WRITE_V, "key": TARGET_WRITE_V, "plain": TARGET_WRITE_V}[kind]


def build_world(ctx, rng, key, n_tools, kind="read", want_eq=False, want_rp=False, key_param=True, arch=None,
                force_verbs=None):
    """Tools: t0 = target (kind read | idem | key | plain), te = equivalent tool (if want_eq), tr = read tool on the
    target entity (if want_rp), plus distractors that never create an unwanted equivalent / read path."""
    arch = arch or rng.choice(ARCHETYPES)
    pool_v = ARCH_VERBS[arch]
    has_req = lambda v: any(r for _s, r in state.VERB_PARAMS[v])           # noqa: E731
    has_syn = lambda v: any(x != v and x in state.VERBS_T55 for x in state.synonym_class(v))   # noqa: E731
    if force_verbs:
        cand = [v for v in force_verbs if v in state.VERBS_T55 and (has_syn(v) or not want_eq)]
    else:
        cand = [v for v in _kind_verbs(kind) if has_req(v) and has_syn(v)]
    if not cand:
        raise RuntimeError("no verb with a synonym for kind %s" % kind)
    vs = [v for v in cand if v in pool_v] or cand
    ents = ctx.names.draw_nouns("noun_entity", 4, key, rng)
    fields = ctx.names.draw_nouns("noun_field", 2, key + "/f", rng)
    verb = rng.choice(vs)
    ent0 = ents[0]
    roles = set(state.ROLES_T55) - {"idempotency_key"}
    t0 = state.build_tool("t0", verb, ent0, fields, roles, rng, idempotent=(kind in ("read", "idem")))
    t0["idempotent"] = kind in ("read", "idem")
    for p in t0["params"]:
        p["default"] = None
    if t0["rw"] == "write" and key_param:
        t0["params"].append({"name": "idempotency_key", "role": "param.idempotency_key", "required": False,
                             "type": "str", "default": None})
    tools, taken = [t0], {t0["name"]}
    te = tr = None
    if want_eq:
        te = state.make_equivalent(t0, "te", set(state.VERBS_T55), rng)
        if te is None:
            raise RuntimeError("target verb %r has no synonym" % verb)
        tools.append(te)
        taken.add(te["name"])
    if want_rp and t0["rw"] == "write":
        for rv in rng.sample(["get", "read", "lookup", "check", "list"], 5):
            tr = state.build_tool("tr", rv, ent0, fields, roles, rng)
            if tr["name"] not in taken:
                tr["rw"], tr["idempotent"] = "read", True
                for p in tr["params"]:
                    p["default"] = None
                tools.append(tr)
                taken.add(tr["name"])
                break
    syn = {t0["group"]} | ({te["group"]} if te else set())
    guard = 0
    while len(tools) < n_tools and guard < 400:
        guard += 1
        v = rng.choice(state.VERBS_T55)
        e = rng.choice(ents[1:])
        if ("%s_%s" % (v, e)) in taken or state.group_id(v, e) in syn:
            continue
        d = state.build_tool("d%d" % len(tools), v, e, fields, roles, rng)
        for p in d["params"]:
            p["default"] = None
        if d["rw"] == "write" and rng.random() < 0.5:
            d["params"].append({"name": "idempotency_key", "role": "param.idempotency_key", "required": False,
                                "type": "str", "default": None})
        tools.append(d)
        taken.add(d["name"])
    return dict(arch=arch, ents=ents, fields=fields, tools=tools, t0=t0, te=te, tr=tr)


def make_call(rng, t0, key_offered=False, extra_args=None):
    args = []
    for p in t0["params"]:
        if p["required"]:
            args.append((p["name"], state.gen_value(rng, p["type"], t0["entity"])))
    if key_offered:
        args.append(("idempotency_key", "k-%d" % rng.randrange(1000, 9999)))
    return args


def _base(ctx, g, rowspec, role, view="view.with_outputs"):
    cid_ret = "card.t55.retry_cap%d" % g["R_cap"]
    cid_esc = "card.t55.escalate_table_%s" % g["esc_q"].lower()
    return dict(family=FAMILY, sub_block=g["sub_block"], entry=g["entry"], group_id=g["gid"], pair_role=role,
                edit=rowspec.get("edit"), view=view, R_cap=g["R_cap"],
                escalation={"quota_exhausted": g["esc_q"], "unsupported_op": g["esc_u"]},
                cards=[cid_ret, cid_esc], card=cid_ret, perturb_cell=None)


def _user_vals(call_args, t0, skip=()):
    return [(k, v) for k, v in call_args if k != "idempotency_key" and k not in skip]


# =============================================================================================================
# B1 / B4
# =============================================================================================================
B1_CELLS = {
    # cell -> (class, wants a, eq, value_available, esc override, tool kind options)
    "r1": dict(cls=("transient_unavailable", "rate_limited"), a="lt", eq=None, kinds=("read", "idem", "key")),
    "r2eq": dict(cls=("transient_unavailable", "rate_limited"), a="ge", eq=True, kinds=("read", "idem", "key")),
    "r2noeq": dict(cls=("transient_unavailable", "rate_limited"), a="ge", eq=False, kinds=("read", "idem", "key")),
    "r4v": dict(cls=("invalid_named_arg",), eq=None, v=True, kinds=("read", "idem", "key")),
    "r4nv": dict(cls=("invalid_named_arg",), eq=None, v=False, kinds=("read", "idem", "key")),
    "r5eq": dict(cls=("invalid_unnamed",), eq=True, kinds=("read", "idem", "key")),
    "r5noeq": dict(cls=("invalid_unnamed",), eq=False, kinds=("read", "idem", "key")),
    "r6": dict(cls=("auth_denied",), eq=None, kinds=("read", "idem", "key")),
    "r7eq": dict(cls=("unsupported_op",), eq=True, kinds=("read", "idem", "key")),
    "r7ask": dict(cls=("unsupported_op",), eq=False, esc_u="ASK", kinds=("read", "idem", "key")),
    "r7stop": dict(cls=("unsupported_op",), eq=False, esc_u="STOP", kinds=("read", "idem", "key")),
    "r8eq": dict(cls=("quota_exhausted",), eq=True, kinds=("read", "idem", "key")),
    "r8ask": dict(cls=("quota_exhausted",), eq=False, esc_q="ASK", kinds=("read", "idem", "key")),
    "r8stop": dict(cls=("quota_exhausted",), eq=False, esc_q="STOP", kinds=("read", "idem", "key")),
    "r9": dict(cls=("irrecoverable",), eq=None, kinds=("read", "idem", "key")),
}


def _err(cls, chan, rng, field=None):
    grp = tw.CLASS_GROUP[cls]
    e = dict(**{"class": cls}, group=grp, channels=list(chan), code=rng.choice(tw.CODES[grp]),
             phrase_idx=rng.randrange(len(tw.PHRASES[grp])), field=field)
    if cls == "rate_limited":
        e["retry_after"] = rng.choice([2, 5, 10, 30, 60])
    return e


def b1_scenario(ctx, g, rng, cell, a=None, kind=None, eq=None, value=None, esc_q=None, esc_u=None, world=None,
                chan=None, cls=None):
    """One explicit-error row for a rule path. A world can be passed to build twins that share the tool list."""
    c = B1_CELLS[cell]
    want_eq = c["eq"] if eq is None else eq
    if want_eq is None:
        want_eq = False
    kind = kind or rng.choice(("read", "key") if want_eq else c["kinds"])
    w = world or build_world(ctx, rng, g["gid"], g["n_tools"], kind=kind, want_eq=True if want_eq else False,
                             want_rp=False, key_param=True)
    cls = cls or rng.choice(c["cls"])
    rec = _base(ctx, g, g["spec"], None)
    esc_q = esc_q or c.get("esc_q") or g["esc_q"]
    esc_u = esc_u or c.get("esc_u") or g["esc_u"]
    rec["escalation"] = {"quota_exhausted": esc_q, "unsupported_op": esc_u}
    rec["cards"] = ["card.t55.retry_cap%d" % g["R_cap"], "card.t55.escalate_table_%s" % esc_q.lower()]
    rec["card"] = rec["cards"][0]
    t0 = w["t0"]
    call_args = make_call(rng, t0, key_offered=(kind == "key"))
    rec.update(tools=copy.deepcopy(w["tools"]), archetype=w["arch"], lists=dict(n=len(w["tools"])))
    if not want_eq:
        rec["tools"] = [t for t in rec["tools"] if t["tid"] != "te"]
    elif not any(t["tid"] == "te" for t in rec["tools"]):
        raise RuntimeError("equivalent tool missing")
    rng.shuffle(rec["tools"])
    rec["call"] = dict(tool_tid="t0", name=t0["name"], args=call_args)
    R = g["R_cap"]
    if a is None:
        if c.get("a") == "lt":
            a = rng.randint(1, R - 1)
        elif c.get("a") == "ge":
            a = rng.choice([R, R + 1])
        else:
            a = rng.choice([1, 1, 2])
    rec["attempt"] = a
    field = None
    user_vals = _user_vals(call_args, t0)
    if cls == "invalid_named_arg":
        req = [k for k, _v in call_args if k != "idempotency_key"]
        if not req:
            raise RuntimeError("no argument to name")
        field = rng.choice(req)
        v_av = c.get("v", True) if value is None else value
        if v_av:                                   # the call carries a malformed variant; the user stated the right value
            bad = dict(call_args)[field] + "x"
            call_args = [(k, bad if k == field else v) for k, v in call_args]
            rec["call"]["args"] = call_args
            user_vals = _uv_with_field(user_vals, field, bad)
        else:                                      # the user never stated it: the agent guessed
            user_vals = [(k, v) for k, v in user_vals if k != field]
            rec["decoy_clauses"] = [_decoy_clause(rng, w["t0"])]
    rec["user_values"] = user_vals
    rec["error"] = _err(cls, chan or g["chan"], rng, field=field)
    rec["flags_b1"] = dict(kind=kind, cell=cell)
    return rec, w


def _decoy_clause(rng, t0):
    """One ambient clause of the same shape as an argument clause, on a role the tool does not have: it keeps the request
    length (and the number of value spans) equal whether or not the user stated the named argument."""
    own = {p["name"] for p in t0["params"]}
    role = rng.choice([r for r in state.ROLES_T55 if r not in own and r != "idempotency_key"])
    return (role, state.gen_value(rng, state.ROLE_TYPE[role], t0["entity"]))


def _uv_with_field(user_vals, field, bad_value):
    """The user states the CORRECT value (bad_value without its trailing 'x') for the named field."""
    return [(k, v) for k, v in user_vals if k != field] + [(field, bad_value[:-1])]


def _tool_by(rec, tid):
    return next(t for t in rec["tools"] if t["tid"] == tid)


def _replace_eq_tool(rec, w, rng):
    """Remove the equivalent tool but keep the tool count and the rw mix: a tool for ANOTHER entity of the same rw takes
    its place (the number of tools must not tell whether an equivalent exists)."""
    te = next(t for t in rec["tools"] if t["tid"] == "te")
    rec["tools"] = [t for t in rec["tools"] if t["tid"] != "te"]
    taken = {t["name"] for t in rec["tools"]}
    for _ in range(80):
        v = rng.choice(TARGET_READ_V if te["rw"] == "read" else TARGET_WRITE_V)
        e = rng.choice(w["ents"][1:])
        if "%s_%s" % (v, e) in taken or state.group_id(v, e) == te["group"]:
            continue
        d = state.build_tool("dx", v, e, w["fields"], set(state.ROLES_T55) - {"idempotency_key"}, rng)
        for p in d["params"]:
            p["default"] = None
        d["idempotent"] = te["idempotent"]
        if d["rw"] != te["rw"]:
            continue
        rec["tools"].insert(rng.randrange(len(rec["tools"]) + 1), d)
        return
    raise RuntimeError("no replacement tool")


def build_b1(ctx, g):
    spec, rng = g["spec"], ctx.rng("b", g["gid"], g.get("attempt", 0))
    cells = spec["cells"]
    if spec["size"] == 1:
        rec, _w = b1_scenario(ctx, g, rng, cells[0])
        return [rec], _w
    e = spec["edit"]
    a_cell, b_cell = cells
    if e == "attempt":
        # same error, same tool list; only the attempt index (history length) differs: a < cap vs a >= cap
        kind = rng.choice(("read", "key"))
        a_rec, w = b1_scenario(ctx, g, rng, "r1", kind=kind, eq=True)
        cls = a_rec["error"]["class"]
        b_rec = copy.deepcopy(a_rec)
        b_rec["attempt"] = rng.choice([g["R_cap"], g["R_cap"] + 1])
    elif e == "class":
        kind = rng.choice(("read", "key"))
        a_rec, w = b1_scenario(ctx, g, rng, "r4v", kind=kind, eq=True)
        b_rec = copy.deepcopy(a_rec)
        b_rec["error"] = dict(b_rec["error"], **{"class": "invalid_unnamed"}, field=None)
        a_rec["attempt"] = b_rec["attempt"] = 1
    elif e == "eq":
        kind = rng.choice(("read", "key"))
        a_rec, w = b1_scenario(ctx, g, rng, "r8eq", kind=kind, esc_q="ASK", eq=True)
        b_rec = copy.deepcopy(a_rec)
        _replace_eq_tool(b_rec, w, rng)
    elif e == "card":
        kind = rng.choice(("read", "idem", "key"))
        a_rec, w = b1_scenario(ctx, g, rng, "r7ask", kind=kind, eq=False, esc_u="ASK")
        b_rec = copy.deepcopy(a_rec)
        b_rec["escalation"] = dict(b_rec["escalation"], unsupported_op="STOP")
        b_rec["cards"] = [b_rec["cards"][0], "card.t55.escalate_table_%s" % b_rec["escalation"]["quota_exhausted"].lower()]
    elif e == "value":
        kind = rng.choice(("read", "idem", "key"))
        a_rec, w = b1_scenario(ctx, g, rng, "r4v", kind=kind, eq=False)
        b_rec = copy.deepcopy(a_rec)
        f = b_rec["error"]["field"]
        b_rec["user_values"] = [(k, v) for k, v in b_rec["user_values"] if k != f]
        b_rec["decoy_clauses"] = [_decoy_clause(rng, _tool_by(b_rec, "t0"))]
    else:
        raise RuntimeError(e)
    a_rec["pair_role"], b_rec["pair_role"] = "a", "b"
    return [a_rec, b_rec], w


def build_b4(ctx, g):
    spec, rng = g["spec"], ctx.rng("b", g["gid"], g.get("attempt", 0))
    kind = rng.choice(("read", "key") if spec["E"] else ("read", "idem", "key"))
    x, w = b1_scenario(ctx, g, rng, "r4v", kind=kind, eq=spec["E"], value=spec["V"])
    x["sub_block"] = "b4_blind_retry"
    y = copy.deepcopy(x)
    y["error"] = dict(y["error"], **{"class": "invalid_unnamed"}, field=None)     # the edit touches ONLY the detail field
    x["attempt"] = y["attempt"] = 1
    x["pair_role"], y["pair_role"] = "a", "b"
    return [x, y], w


# =============================================================================================================
# B2 AMBIGUOUS-WRITE
# =============================================================================================================
def b2_scenario(ctx, g, rng, *, idem, kf, rp, step, committed, n_tools=None):
    kind = "idem" if idem else ("key" if kf else "plain")
    w = build_world(ctx, rng, g["gid"], n_tools or g["n_tools"], kind=kind, want_eq=False, want_rp=bool(rp), key_param=True)
    t0 = w["t0"]
    if kf and not any(p["name"] == "idempotency_key" for p in t0["params"]):
        t0["params"].append({"name": "idempotency_key", "role": "param.idempotency_key", "required": False,
                             "type": "str", "default": None})
    t0["idempotent"] = bool(idem)
    call_args = make_call(rng, t0, key_offered=bool(kf))
    rec = _base(ctx, g, g["spec"], None)
    rec.update(tools=shuffle(rng, copy.deepcopy(w["tools"])), archetype=w["arch"], lists=dict(n=len(w["tools"])))
    rec["call"] = dict(tool_tid="t0", name=t0["name"], args=call_args)
    rec["step"] = step
    rec["attempt"] = 1
    rec["world_committed"] = bool(committed)                      # hidden in step 1; shown by the read-back in step 2
    if step == 2:
        tr = next(t for t in rec["tools"] if t["tid"] == "tr")
        rec["readback"] = dict(tool=tr["name"], committed=bool(committed))
    rec["user_values"] = _user_vals(call_args, t0)
    rec["flags_b2"] = dict(kind=kind)
    dec = next((t for t in rec["tools"] if t["rw"] == "read" and t["entity"] != t0["entity"]), None)
    rec["decoy_read_tid"] = dec["tid"] if dec else None
    return rec, w


def shuffle(rng, xs):
    xs = list(xs)
    rng.shuffle(xs)
    return xs


def build_b2(ctx, g):
    spec, rng = g["spec"], ctx.rng("b", g["gid"], g.get("attempt", 0))
    name = spec["name"]
    com = rng.random() < 0.5
    if name == "p_key":
        a, w = b2_scenario(ctx, g, rng, idem=False, kf=True, rp=True, step=1, committed=com)
        b = copy.deepcopy(a)
        b["call"]["args"] = [(k, v) for k, v in b["call"]["args"] if k != "idempotency_key"]          # edit: key not offered
        a["pair_role"], b["pair_role"] = "a", "b"
        return [a, b], w
    if name == "p_rp":
        a, w = b2_scenario(ctx, g, rng, idem=False, kf=False, rp=True, step=1, committed=com)
        b = copy.deepcopy(a)
        b["tools"] = [t for t in b["tools"] if t["tid"] != "tr"]                                       # edit: no read path
        a["pair_role"], b["pair_role"] = "a", "b"
        return [a, b], w
    if name == "p_com":
        plain = rng.random() < 0.7
        a, w = b2_scenario(ctx, g, rng, idem=(False if plain else rng.random() < 0.5), kf=(False if plain else rng.random() < 0.5),
                           rp=True, step=2, committed=True)
        b = copy.deepcopy(a)
        b["world_committed"] = False
        b["readback"] = dict(a["readback"], committed=False)                                           # edit: the read-back result
        a["pair_role"], b["pair_role"] = "a", "b"
        return [a, b], w
    if name == "s_keyed":
        mode = rng.choice(["kf", "kf", "idem", "both"])
        rec, w = b2_scenario(ctx, g, rng, idem=mode in ("idem", "both"), kf=mode in ("kf", "both"), rp=rng.random() < 0.5,
                             step=1, committed=com)
        return [rec], w
    if name == "s_read":
        rec, w = b2_scenario(ctx, g, rng, idem=False, kf=False, rp=True, step=1, committed=com)
        return [rec], w
    rec, w = b2_scenario(ctx, g, rng, idem=False, kf=False, rp=False, step=1, committed=com)
    return [rec], w


# =============================================================================================================
# B3 IMPLICIT-ERROR
# =============================================================================================================
def b3_scenario(ctx, g, rng, spec, vtype, violating):
    kind = spec["kind"]
    rw_read = kind.startswith("data_read")
    want_eq = kind in ("data_read_eq",)
    base_kind = "read" if rw_read else ("read" if (kind == "arg" and rng.random() < 0.5) else "plain")
    items_type = vtype in ("empty_when_count_stated", "id_not_in_prior_list", "parts_total_mismatch",
                           "duplicate_in_unique_list", "order_violation")
    fv = None
    if base_kind == "read":
        fv = None                       # same verb distribution for every violation type (a verb must not proxy the type)
    w = build_world(ctx, rng, g["gid"], g["n_tools"], kind=base_kind, want_eq=want_eq, want_rp=False, key_param=False,
                    force_verbs=fv)
    t0 = w["t0"]
    field = w["fields"][0]
    ctx_verb = {"empty_when_count_stated": "count", "id_not_in_prior_list": "list", "scale_mismatch": "get",
                "stale_echo": "list"}.get(vtype)
    if ctx_verb:                                    # the earlier call whose output the invariant is read against
        tc = None
        for cv in [ctx_verb] + [x for x in ("read", "lookup", "check", "get", "list") if x != ctx_verb]:
            cand_tc = state.build_tool("tc", cv, t0["entity"], w["fields"], set(state.ROLES_T55) - {"idempotency_key"}, rng)
            if cand_tc["name"] != t0["name"] and state.group_id(cv, t0["entity"]) != t0["group"] and \
                    cand_tc["name"] not in {x["name"] for x in w["tools"]}:
                tc = cand_tc
                break
        tc["rw"], tc["idempotent"] = "read", True
        for p_ in tc["params"]:
            p_["default"] = None
        w["tools"].append(tc)
    cause = "arg" if kind == "arg" else "data"
    base = invariants.make_base(vtype, rng, t0["entity"], field, cause)
    result, ctx_ = invariants.materialise(base, violating)
    # declarations the invariants rely on are visible in the tool description
    decl = []
    if vtype == "negative_value" or base.get("vtype") == "negative_value":
        decl.append("Returns %s, never negative." % field)
    if vtype == "duplicate_in_unique_list":
        decl.append("Items are unique.")
    if vtype == "order_violation":
        decl.append("Items are sorted %sending by %s." % ("asc" if base["dir"] == "asc" else "desc", field))
    if decl:
        t0["desc"] = (t0["desc"] + " " + " ".join(decl)).strip()
    if ctx_.get("call_args"):                     # the tool schema carries exactly the arguments the context talks about
        t0["params"] = [{"name": k, "role": ("param." + k) if k in state.ROLES_T55 else None, "required": True,
                         "type": "str", "default": None} for k in ctx_["call_args"]]
    rec = _base(ctx, g, spec, None)
    rec.update(tools=shuffle(rng, copy.deepcopy(w["tools"])), archetype=w["arch"], lists=dict(n=len(w["tools"])))
    rec["call"] = dict(tool_tid="t0", name=t0["name"], args=make_call(rng, t0))
    rec["attempt"] = spec["a"]
    rec["result"], rec["ctx"] = result, ctx_
    rec["b3"] = dict(vtype=vtype, base=base, field=field, violating=violating)
    # the call's own arguments are part of the context the cause is read from
    if ctx_.get("call_args"):
        rec["call"]["args"] = [(k, str(v)) for k, v in ctx_["call_args"].items()]
    rec["user_values"] = []
    return rec, w


def build_b3(ctx, g):
    spec, rng = g["spec"], ctx.rng("b", g["gid"], g.get("attempt", 0))
    pool = list(invariants.ARG_CAPABLE) if spec["kind"] == "arg" else list(perturb.TRAIN_TYPES)
    vtype = pool[g["vt"] % len(pool)]
    viol, w = b3_scenario(ctx, g, rng, spec, vtype, True)
    if spec["size"] == 1:
        return [viol], w
    twin = copy.deepcopy(viol)
    twin["result"], twin["ctx"] = invariants.materialise(viol["b3"]["base"], False)
    twin["b3"] = dict(viol["b3"], violating=False)
    twin["call"] = copy.deepcopy(viol["call"])
    if twin["ctx"].get("call_args"):
        twin["call"]["args"] = [(k, str(v)) for k, v in twin["ctx"]["call_args"].items()]
    viol["pair_role"], twin["pair_role"] = "a", "b"
    return [viol, twin], w


# =============================================================================================================
# B5 DENY-ESCALATE
# =============================================================================================================
def b5_scenario(ctx, g, rng, *, n_c, n_t, n_w, alt, hard):
    c = g["b5"]
    w = build_world(ctx, rng, g["gid"], min(g["n_tools"], 8), kind="plain", want_eq=False, want_rp=False, key_param=False)
    t0 = w["t0"]
    rec = _base(ctx, g, g["spec"], None, view="view.primary")
    cid = "card.t55.denial_window" if c["window"] else "card.t55.denial_consec_total"
    rec["cards"], rec["card"] = [cid], cid
    rec.update(tools=shuffle(rng, copy.deepcopy(w["tools"])), archetype=w["arch"], lists=dict(n=len(w["tools"])))
    rec["call"] = dict(tool_tid="t0", name=t0["name"], args=make_call(rng, t0))
    rec["card_b5"] = dict(K_c=c["kc"], K_t=c["kt"], K_w=c["kw"], W=c["W"], window=c["window"])
    rec["denials"] = dict(n_c=n_c, n_t=n_t, n_w=(n_w if c["window"] else None), alt_exists=alt, goal_blocked_hard=hard)
    rec["user_values"] = []
    rec["attempt"] = 1
    return rec, w


def _counters(rng, c, *, n_c, second=None, hit_second=False):
    """Consistent counters: n_c <= n_w <= n_t. `second` = ('t'|'w', value) pins the secondary counter."""
    kt, kw, window = c["kt"], c["kw"], c["window"]
    n_t_hi = (kt - 1) if kt else 40
    n_w_hi = (kw - 1) if window else 0
    if second and second[0] == "t":
        n_t = second[1]
    else:
        lo = max(n_c, 0)
        n_t = rng.randint(lo, max(lo, n_t_hi))
    if window:
        if second and second[0] == "w":
            n_w = second[1]
        else:
            n_w = rng.randint(n_c, max(n_c, n_w_hi))
        n_t = max(n_t, n_w)
        if kt and not (second and second[0] == "t") and n_t >= kt:
            n_t = kt - 1
            n_w = min(n_w, n_t)
    else:
        n_w = None
    n_t = max(n_t, n_c)
    return n_t, n_w


def build_b5(ctx, g):
    spec, rng = g["spec"], ctx.rng("b", g["gid"], g.get("attempt", 0))
    c = g["b5"]
    kc, kt, kw, window = c["kc"], c["kt"], c["kw"], c["window"]
    name = spec["name"]
    if name == "p_consec":
        n_c_a = kc - 1
        nt, nw = _counters(rng, c, n_c=kc)                              # shared secondary counters (below their thresholds)
        nt = min(nt, (kt - 1) if kt else nt)
        a, w = b5_scenario(ctx, g, rng, n_c=n_c_a, n_t=max(nt, n_c_a), n_w=(max(nw, n_c_a) if window else None), alt=True, hard=False)
        b = copy.deepcopy(a)
        b["denials"] = dict(a["denials"], n_c=kc,
                            n_t=max(a["denials"]["n_t"], kc), n_w=(max(a["denials"]["n_w"], kc) if window else None))
        if kt and b["denials"]["n_t"] >= kt:
            raise RuntimeError("secondary counter would trip")
        if window and b["denials"]["n_w"] >= kw:
            raise RuntimeError("window counter would trip")
        a["pair_role"], b["pair_role"] = "a", "b"
        return [a, b], w
    if name == "p_second":
        n_c = rng.randint(0, kc - 1)
        if window:
            n_w_a = kw - 1
            n_t_a = max(n_w_a, rng.randint(n_w_a, (kt - 1) if kt else n_w_a + 6))
            a, w = b5_scenario(ctx, g, rng, n_c=n_c, n_t=n_t_a, n_w=n_w_a, alt=True, hard=False)
            b = copy.deepcopy(a)
            b["denials"] = dict(a["denials"], n_w=kw, n_t=max(n_t_a, kw))
            if kt and b["denials"]["n_t"] >= kt:
                b["denials"]["n_t"] = kt - 1
                if b["denials"]["n_t"] < kw:
                    raise RuntimeError("window and total thresholds conflict")
        else:
            a, w = b5_scenario(ctx, g, rng, n_c=n_c, n_t=kt - 1, n_w=None, alt=True, hard=False)
            b = copy.deepcopy(a)
            b["denials"] = dict(a["denials"], n_t=kt)
        a["pair_role"], b["pair_role"] = "a", "b"
        return [a, b], w
    # singles
    if name == "s_cont":
        n_c = rng.randint(0, kc - 1)
        nt, nw = _counters(rng, c, n_c=n_c)
        rec, w = b5_scenario(ctx, g, rng, n_c=n_c, n_t=nt, n_w=nw, alt=True, hard=False)
        return [rec], w
    if name == "s_stop":
        n_c = rng.randint(0, kc - 1)
        nt, nw = _counters(rng, c, n_c=n_c)
        rec, w = b5_scenario(ctx, g, rng, n_c=n_c, n_t=nt, n_w=nw, alt=rng.random() < 0.5, hard=True)
        return [rec], w
    if spec.get("why") == "noalt":
        n_c = rng.randint(0, kc - 1)
        nt, nw = _counters(rng, c, n_c=n_c)
        rec, w = b5_scenario(ctx, g, rng, n_c=n_c, n_t=nt, n_w=nw, alt=False, hard=False)
        return [rec], w
    # s_esc_thr: a threshold is hit (consecutive, total or window); a hard block does not matter when escalating
    which = rng.choice(["c", "second"])
    if which == "c" or (not kt and not window):
        n_c = rng.randint(kc, kc + 2)
        nt, nw = _counters(rng, c, n_c=n_c)
        nt = max(nt, n_c)
        nw = max(nw, n_c) if window else None
    elif window:
        n_c = rng.randint(0, kc - 1)
        nw = rng.randint(kw, kw + 3)
        nt = max(nw + rng.randint(0, 3), nw)
    else:
        n_c = rng.randint(0, kc - 1)
        nt, nw = rng.randint(kt, kt + 4), None
    rec, w = b5_scenario(ctx, g, rng, n_c=n_c, n_t=nt, n_w=nw, alt=rng.random() < 0.5, hard=rng.random() < 0.3)
    return [rec], w


# =============================================================================================================
# B6 LOOP-POLL
# =============================================================================================================
STATUS_CHAIN = ["queued", "running", "finishing", "done"]
TRANSITIONS = [(STATUS_CHAIN[i], STATUS_CHAIN[i + 1]) for i in range(len(STATUS_CHAIN) - 1)]
NOISE_STATUS = {"queued": "queued", "running": "running", "finishing": "finishing", "pending": "pending",
                "active": "active"}


def _obs_from_pattern(rng, pattern, fields, trans):
    """Observations (len(pattern)+1) whose per-step advance flags equal `pattern`."""
    n = len(pattern) + 1
    obs = [dict() for _ in range(n)]
    prog = rng.randint(5, 30)
    cnt = rng.randint(1, 9)
    st_chain = [trans[0][0]]
    for a, b in trans:
        st_chain.append(b)
    si = 0
    for i in range(n):
        if i > 0:
            adv = pattern[i - 1]
            if "progress" in fields:
                prog = prog + rng.randint(3, 15) if adv else (prog if rng.random() < 0.7 else prog - rng.randint(0, 2))
            if "counter" in fields:
                cnt = cnt + 1 if adv else cnt
            if "status" in fields:
                if adv and si + 1 < len(st_chain):
                    si += 1
        if "progress" in fields:
            obs[i]["progress"] = prog
        if "counter" in fields:
            obs[i]["counter"] = cnt
        if "status" in fields:
            obs[i]["status"] = st_chain[si]
    return obs


def b6_scenario(ctx, g, rng, *, pattern, calls_used, alt, non_waitable, P_cap, L, fields=None, identical=None):
    w = build_world(ctx, rng, g["gid"], min(g["n_tools"], 8), kind="read", want_eq=alt, want_rp=False, key_param=False)
    t0 = w["t0"]
    if not any(p["name"] == "limit" for p in t0["params"]):
        t0["params"].append({"name": "limit", "role": "param.limit", "required": False, "type": "int", "default": None})
    fields = fields or rng.sample(["progress", "counter", "status"], rng.randint(1, 3))
    # a declared-transition card; status steps only advance along it
    k = rng.randint(2, 3)
    start = rng.randint(0, len(TRANSITIONS) - k)
    trans = TRANSITIONS[start:start + k]                                        # a consecutive declared chain
    # status needs enough declared transitions for the number of advances
    n_adv = sum(1 for x in pattern if x)
    if "status" in fields and n_adv > len(trans):
        fields = [f for f in fields if f != "status"] or ["progress"]
    obs = _obs_from_pattern(rng, pattern, fields, trans)
    rec = _base(ctx, g, g["spec"], None)
    rec.update(tools=shuffle(rng, copy.deepcopy([t for t in w["tools"] if t["tid"] != "te"] + ([w["te"]] if w["te"] else []))),
               archetype=w["arch"], lists=dict(n=len(w["tools"])))
    base_args = make_call(rng, t0)
    ident = g["identical_calls"] if identical is None else identical
    calls = []
    for i in range(len(obs)):
        args = list(base_args)
        if not ident:                                  # cosmetic variation only: an incidental optional argument changes
            args.append(("limit", str(10 + 5 * i)))
        calls.append(args)
    rec["call"] = dict(tool_tid="t0", name=t0["name"], args=base_args)
    rec["card_b6"] = dict(P_cap=P_cap, L=L, transitions=[list(t) for t in trans], non_waitable=non_waitable)
    rec["poll"] = dict(obs=obs, calls=calls, calls_used=calls_used, alt_exists=bool(alt), fields=list(fields))
    rec["user_values"] = []
    rec["attempt"] = 1
    return rec, w


def build_b6(ctx, g):
    spec, rng = g["spec"], ctx.rng("b", g["gid"], g.get("attempt", 0))
    name = spec["name"]
    P_cap = rng.choice([8, 10, 12, 14])
    L = rng.choice([3, 4])
    m = rng.randint(L + 1, 6)                                         # window of m calls (>= L+1 so a loop is possible)
    n_steps = m - 1

    def pat_adv(last_true=True):
        return [rng.random() < 0.8 for _ in range(n_steps - 1)] + [True]

    def pat_stale(stale):
        prefix = [rng.random() < 0.6 for _ in range(n_steps - stale)]
        if prefix:
            prefix[-1] = True                                         # so the trailing stale run is exactly `stale`
        return prefix + [False] * stale

    cu_lt = rng.randint(m, P_cap - 1) if P_cap - 1 >= m else m
    if name.startswith("p_prog"):
        alt = name == "p_prog_b"
        non_w = name == "p_prog_s"
        a, w = b6_scenario(ctx, g, rng, pattern=pat_adv(), calls_used=cu_lt, alt=alt, non_waitable=non_w, P_cap=P_cap, L=L,
                           identical=g["identical_calls"])
        b = copy.deepcopy(a)
        stale = rng.randint(L, n_steps)
        pat_b = pat_stale(stale)
        b["poll"] = dict(a["poll"], obs=_obs_from_pattern(rng, pat_b, a["poll"]["fields"], [tuple(t) for t in a["card_b6"]["transitions"]]))
        a["pair_role"], b["pair_role"] = "a", "b"
        return [a, b], w
    if name == "s_keep":
        if rng.random() < 0.5:
            rec, w = b6_scenario(ctx, g, rng, pattern=pat_adv(), calls_used=cu_lt, alt=rng.random() < 0.5,
                                 non_waitable=rng.random() < 0.3, P_cap=P_cap, L=L)
        else:
            rec, w = b6_scenario(ctx, g, rng, pattern=pat_stale(rng.randint(1, L - 1)), calls_used=cu_lt,
                                 alt=rng.random() < 0.5, non_waitable=rng.random() < 0.3, P_cap=P_cap, L=L)
        return [rec], w
    if name == "s_break":
        rec, w = b6_scenario(ctx, g, rng, pattern=pat_stale(rng.randint(L, n_steps)), calls_used=rng.randint(m, P_cap + 3),
                             alt=True, non_waitable=rng.random() < 0.5, P_cap=P_cap, L=L)
        return [rec], w
    if name == "s_stop":
        rec, w = b6_scenario(ctx, g, rng, pattern=pat_stale(rng.randint(L, n_steps)), calls_used=rng.randint(m, P_cap + 3),
                             alt=False, non_waitable=True, P_cap=P_cap, L=L)
        return [rec], w
    if spec.get("why") == "cap":
        rec, w = b6_scenario(ctx, g, rng, pattern=pat_adv(), calls_used=rng.randint(P_cap, P_cap + 4), alt=rng.random() < 0.5,
                             non_waitable=rng.random() < 0.5, P_cap=P_cap, L=L)
        return [rec], w
    rec, w = b6_scenario(ctx, g, rng, pattern=pat_stale(rng.randint(L, n_steps)), calls_used=rng.randint(m, P_cap + 3),
                         alt=False, non_waitable=False, P_cap=P_cap, L=L)
    return [rec], w


# =============================================================================================================
# driver
# =============================================================================================================
BUILDERS = {"b1_classic": build_b1, "b4_blind_retry": build_b4, "b2_ambig_write": build_b2, "b3_implicit": build_b3,
            "b5_deny_escalate": build_b5, "b6_loop_poll": build_b6}
MAX_ATTEMPTS = 12


def generate_group(ctx, g):
    last = None
    for attempt in range(MAX_ATTEMPTS):
        g["attempt"] = attempt
        try:
            return _generate_group_once(ctx, g)
        except (sa.SpecError, sa.OutOfBlock, RuntimeError, AssertionError) as e:
            if isinstance(e, AssertionError) and "disagree" in str(e):
                raise
            last = e
            ctx.rejected = getattr(ctx, "rejected", 0) + 1
            ctx.reject_log = getattr(ctx, "reject_log", collections.Counter())
            ctx.reject_log[(g["sub_block"], g["entry"], type(e).__name__, str(e)[:60])] += 1
    raise RuntimeError("group %s rejected %d times: %s" % (g["gid"], MAX_ATTEMPTS, last))


def _generate_group_once(ctx, g):
    import t55_render as rd
    recs, _w = BUILDERS[g["sub_block"]](ctx, g)
    out = []
    spec = g["spec"]
    for i, r in enumerate(recs):
        out.append(rd.finalize(ctx, g, r, int(g["pos"][i])))
    want = tuple(spec["labels"])
    got = tuple(r["gold"] for r in out)
    if g["sub_block"] == "b4_blind_retry":
        want = tuple(spec["labels"])
    if got != want:
        raise AssertionError("solver A disagree: %s %s gave %s, entry intends %s" % (g["gid"], spec["name"], got, want))
    return out


def generate_in_memory(total=20, seed="t55-dry", standin=True, ctx=None):
    ctx = ctx or Ctx(seed=seed, standin=standin)
    plan = build_plan(total=total, seed=seed)
    recs = []
    for g in plan:
        recs.extend(generate_group(ctx, g))
    return recs
