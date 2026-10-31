"""T54 TOOL-NEED/PICK generator (CODE ONLY: no rows are written by this module; `generate_in_memory` returns records
for unit tests and the 20-example dry run only). Clean-room: built from G0_LITE.md + G0_APPROVALS only.

Pipeline per G0-lite 3.1: a structured scenario record -> label by SOLVER A (t54_solver_a.gold_label) -> text rendered
from the record. Haiku (later) only rewords wording pools. No LLM writes a label.

Names: ids come from the frozen allow-list (guard in finalize), display names from namespace.py via NameSource.
"""
import collections
import copy
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_ROOT, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from tool_engine import dag as dagmod  # noqa: E402
from tool_engine import names as names_mod  # noqa: E402
from tool_engine import render, state, util, wording  # noqa: E402
import t54_solver_a as sa  # noqa: E402
import t54_wording as tw  # noqa: E402

FAMILY = "T54"
SUB_BLOCKS = ("s1_need4", "s2_pick", "s3_limit", "s4_precond", "s5_argground", "s6_parseq")
SIZES = {"s1_need4": 1000, "s2_pick": 800, "s3_limit": 800, "s4_precond": 500, "s5_argground": 500, "s6_parseq": 400}
TOTAL = 4000
CARDS_BASE = ("card.t54.strict_ask", "card.t54.defaults_ok")
NBINS = ((2, 3), (4, 6), (7, 10), (11, 16), (17, 25))
T_VALUES = (4, 5, 6, 7, 8)
FAMILY_NBIN_SHARES = (0.20, 0.30, 0.25, 0.15, 0.10)
MIN_BIN = {"s1_need4": 0, "s2_pick": 1, "s3_limit": 0, "s4_precond": 0, "s5_argground": 0, "s6_parseq": 1}
ARCHETYPES = ("arch.records", "arch.schedule", "arch.messages", "arch.files", "arch.jobs", "arch.inventory",
              "arch.accounts", "arch.tickets", "arch.metrics", "arch.directory", "arch.queue", "arch.catalogue")
ARCH_VERBS = {  # structural kind -> the verbs its scenarios draw from (all on the closed 36-verb list)
    "arch.records": ["get", "list", "find", "create", "update", "delete", "count", "archive", "restore", "merge"],
    "arch.schedule": ["schedule", "cancel", "list", "get", "reserve", "release", "move", "check", "close", "open"],
    "arch.messages": ["send", "list", "get", "search", "archive", "delete", "tag", "read", "restore", "export"],
    "arch.files": ["read", "list", "copy", "move", "rename", "delete", "find", "export", "import", "lock"],
    "arch.jobs": ["create", "cancel", "check", "list", "get", "close", "approve", "reject", "sync", "assign"],
    "arch.inventory": ["count", "reserve", "release", "add", "remove", "update", "list", "find", "get", "set"],
    "arch.accounts": ["get", "create", "lock", "unlock", "update", "close", "assign", "lookup", "list", "set"],
    "arch.tickets": ["create", "assign", "close", "open", "tag", "list", "search", "update", "approve", "reject"],
    "arch.metrics": ["get", "list", "count", "export", "sync", "check", "find", "lookup", "set", "read"],
    "arch.directory": ["lookup", "find", "list", "add", "remove", "rename", "assign", "get", "update", "search"],
    "arch.queue": ["add", "remove", "list", "count", "get", "cancel", "merge", "move", "check", "release"],
    "arch.catalogue": ["list", "search", "get", "add", "update", "delete", "tag", "archive", "export", "import"],
}
# S4: write verbs that have a natural "already holds" state: verb -> (state after the write, state before)
STATE_WORDS = {"archive": ("archived", "active"), "close": ("closed", "open"), "cancel": ("cancelled", "active"),
               "restore": ("active", "archived"), "approve": ("approved", "pending"), "lock": ("locked", "unlocked"),
               "unlock": ("unlocked", "locked"), "release": ("released", "reserved"),
               "reserve": ("reserved", "free"), "open": ("open", "closed"), "assign": ("assigned", "unassigned"),
               "send": ("sent", "draft"), "create": ("present", "absent"), "add": ("present", "absent"),
               "delete": ("absent", "present"), "remove": ("absent", "present"),
               "schedule": ("scheduled", "unscheduled"), "reject": ("rejected", "pending"), "tag": ("tagged", "plain"),
               "set": ("updated", "stale")}
S4_VERBS = tuple(STATE_WORDS)
READ_FOR_STATE = ("check", "get", "read", "lookup")

# ---- plan entries: name, rows_per_group, rows at 4000, payload -------------------------------------------------
ENTRIES = {
    "s1_need4": [
        dict(name="pairA", size=2, rows=200, edit="A", labels=("CALL", "ASK")),
        dict(name="pairC", size=2, rows=140, edit="C", labels=("CALL", "ASK")),
        dict(name="pairB", size=2, rows=260, edit="B", labels=("CALL", "NO_TOOL")),
        dict(name="pairD", size=2, rows=360, edit="E", labels=("ANSWER", "CALL")),
        dict(name="single_nt", size=1, rows=40, labels=("NO_TOOL",)),
    ],
    "s2_pick": [
        dict(name="pair_hn", size=2, rows=360, edit="A", labels=("TARGET", "HN")),
        dict(name="single", size=1, rows=440, labels=("TARGET",)),
    ],
    "s3_limit": [
        dict(name="pair_tool", size=2, rows=214, edit="B", labels=("NO_TOOL", "CALL"), dele="TOOL"),
        dict(name="pair_param", size=2, rows=214, edit="A", labels=("ASK", "CALL"), dele="PARAM"),
        dict(name="pair_result", size=2, rows=212, edit="E", labels=("RESULT_MISSING", "CALL"), dele="RESULT"),
        dict(name="single_tool", size=1, rows=13, labels=("NO_TOOL",), dele="TOOL"),
        dict(name="single_param", size=1, rows=13, labels=("ASK",), dele="PARAM"),
        dict(name="single_result", size=1, rows=14, labels=("RESULT_MISSING",), dele="RESULT"),
        dict(name="null_control", size=1, rows=120, labels=("CALL",), dele="NULL"),
    ],
    "s4_precond": [
        dict(name="pair_done_read", size=2, rows=200, edit="D", labels=("DONE_NO_CALL", "READ_FIRST")),
        dict(name="pair_done_write", size=2, rows=80, edit="D", labels=("DONE_NO_CALL", "WRITE")),
        dict(name="pair_read_ask", size=2, rows=40, edit="B", labels=("READ_FIRST", "ASK")),
        dict(name="single_write_idem", size=1, rows=50, labels=("WRITE",), branch="idem"),
        dict(name="single_write_false", size=1, rows=50, labels=("WRITE",), branch="obs_false"),
        dict(name="single_ask_noread", size=1, rows=40, labels=("ASK",), branch="no_read"),
        dict(name="single_ask_missing", size=1, rows=40, labels=("ASK",), branch="missing_arg"),
    ],
    "s5_argground": [
        dict(name="pair_prov", size=2, rows=380, edit="E", labels=("GROUNDED", "UNGROUNDED")),
        dict(name="single_g", size=1, rows=60, labels=("GROUNDED",)),
        dict(name="single_u", size=1, rows=60, labels=("UNGROUNDED",)),
    ],
    "s6_parseq": [
        dict(name="pair_12", size=2, rows=50, edit="E", sizes=(1, 2)),
        dict(name="pair_23", size=2, rows=60, edit="E", sizes=(2, 3)),
        dict(name="pair_34", size=2, rows=30, edit="E", sizes=(3, 4)),
        dict(name="single_1", size=1, rows=95, sizes=(1,)),
        dict(name="single_2", size=1, rows=105, sizes=(2,)),
        dict(name="single_3p", size=1, rows=60, sizes=(3,)),
    ],
}
# label mix of each sub-block (shares), used by gate P-2 and checked against ENTRIES in the unit tests
LABEL_MIX = {
    "s1_need4": {"CALL": .48, "ASK": .17, "NO_TOOL": .17, "ANSWER": .18},
    "s3_limit": {"CALL": .55, "NO_TOOL": .15, "ASK": .15, "RESULT_MISSING": .15},
    "s4_precond": {"WRITE": .28, "READ_FIRST": .24, "DONE_NO_CALL": .28, "ASK": .20},
    "s5_argground": {"GROUNDED": .50, "UNGROUNDED": .50},
}


def nbin_weights():
    """Per-sub-block bin weights that hit the FAMILY N-bin shares (2-3 20 / 4-6 30 / 7-10 25 / 11-16 15 / 17-25 10).
    S2 and S6 need N >= 4 (four options / a multi-node plan) so they skip the first bin; the other sub-blocks carry it."""
    f = FAMILY_NBIN_SHARES
    share_r = sum(SIZES[s] for s in SUB_BLOCKS if MIN_BIN[s] == 1) / float(TOTAL)
    share_u = 1.0 - share_r
    tail = sum(f[1:])
    r = [0.0] + [x / tail for x in f[1:]]
    u = [f[0] / share_u] + [(f[j] - share_r * r[j]) / share_u for j in range(1, 5)]
    assert all(x >= 0 for x in u) and abs(sum(u) - 1) < 1e-9 and abs(sum(r) - 1) < 1e-9
    return {s: (r if MIN_BIN[s] == 1 else u) for s in SUB_BLOCKS}


NBIN_W = nbin_weights()


class Ctx:
    """Generation context: seed, names (namespace.py), wording pool. `standin=True` is for tests / the dry run only."""

    def __init__(self, seed="t54-v1", standin=False, pool=None, names_src=None):
        self.seed = seed
        self.names = names_src or names_mod.NameSource(FAMILY, seed=seed, standin=standin)
        self.pool = pool or tw.seed_pool()
        self.pool.balanced = True                       # every wording of a form is used equally often (see WordingPool)
        self.gold_pos = {}

    def rng(self, *parts):
        return util.rng_for(self.seed, *parts)

    def pick(self, form_id, gid, key, fallback=None):
        """Template choice keyed by (group, key): twins of a pair get the SAME wording, so only the edit differs."""
        fid, idx, tpl = self.pool.pick(form_id, self.rng("w", gid, key), fallback, key=(gid, key))
        return fid, idx, tpl


# =============================================================================================================
# plan
# =============================================================================================================
def alloc_entries(n_rows, entries):
    """Rows per entry (largest remainder), then groups per entry; rounding leftovers go to the first single entry."""
    raw = util.largest_remainder(n_rows, {e["name"]: e["rows"] for e in entries})
    groups, left = {}, 0
    for e in entries:
        g = raw[e["name"]] // e["size"]
        groups[e["name"]] = g
        left += raw[e["name"]] - g * e["size"]
    singles = [e for e in entries if e["size"] == 1]
    if singles and left:                                   # rounding leftovers go to the single-row entries, pro rata
        extra = util.largest_remainder(left, {e["name"]: e["rows"] for e in singles})
        for k, v in extra.items():
            groups[k] += v
    return groups


def build_plan(total=TOTAL, seed="t54-plan-v1"):
    """Group specs (a group is one row or one minimal pair). Exact sub-block sizes; label mixes follow the entries."""
    sizes = util.largest_remainder(total, SIZES)
    plan = []
    for sb in SUB_BLOCKS:
        alloc = alloc_entries(sizes[sb], ENTRIES[sb])
        for e in ENTRIES[sb]:
            for i in range(alloc[e["name"]]):
                plan.append(dict(gid="%s-%s-%05d" % (sb[:2], e["name"], i), sub_block=sb, entry=e["name"], spec=e))
    rng = util.rng_for(seed, "order")
    rng.shuffle(plan)
    # balanced gold positions: per (sub-block, label) for labelled sub-blocks, per sub-block for S2/S6
    row_slots = []                                   # (gid, row index, key)
    for g in plan:
        labs = g["spec"].get("labels", ())
        for i in range(g["spec"]["size"]):
            key = (g["sub_block"], labs[i]) if (g["sub_block"] not in ("s2_pick", "s6_parseq") and labs) else (g["sub_block"],)
            row_slots.append((g["gid"], i, key))
    by_key = collections.defaultdict(list)
    for gid_, i, key in row_slots:
        by_key[key].append((gid_, i))
    pos_of = {}
    for key, items in by_key.items():
        cyc_p = util.balanced_cycle(len(items), 4, util.rng_for(seed, "pos", *key))
        for (gid_, i), pv in zip(items, cyc_p):
            pos_of[(gid_, i)] = pv
    for g in plan:
        g["pos"] = [pos_of[(g["gid"], i)] for i in range(g["spec"]["size"])]
    bins_by_gid = {}
    for sb in SUB_BLOCKS:                     # stratified N-bin assignment: exact shares per sub-block AND per entry, shuffled.
        # Per ENTRY (not only per sub-block): an entry fixes the label (or the label pair) of its rows, so a bin sequence that
        # is balanced only over the sub-block lets the tool count drift between entries (measured: a 2-tool gap between the
        # S3 deletion entries) and the tool count would read as a label cue.
        for ent in ENTRIES[sb]:
            gs = [g for g in plan if g["sub_block"] == sb and g["entry"] == ent["name"]]
            cnt = util.largest_remainder(len(gs), {i: NBIN_W[sb][i] for i in range(5)})
            seq = [i for i in range(5) for _ in range(cnt[i])]
            util.rng_for(seed, "nbin", sb, ent["name"]).shuffle(seq)
            for g, b in zip(gs, seq):
                bins_by_gid[g["gid"]] = b
    for g in plan:
        r = util.rng_for(seed, "grp", g["gid"])
        w = NBIN_W[g["sub_block"]]
        g["nbin"] = bins_by_gid[g["gid"]]
        g["n"] = _sample_n(r, g["sub_block"], g["nbin"])
        g["card_pick"] = r.choice(CARDS_BASE)
        g["ref"] = r.random() < 0.2
        g["n_extra"] = r.choice([0, 0, 1, 1, 2])
    # the base card is drawn per ENTRY (an entry fixes the label or the label pair of its rows): a card that was drawn per group would
    # drift between entries by chance and read as a label cue; here every entry has 50 / 50 strict_ask / defaults_ok (+-1)
    for sb in SUB_BLOCKS:
        for ent in ENTRIES[sb]:
            gs_ = [g for g in plan if g["sub_block"] == sb and g["entry"] == ent["name"]]
            for g, c in zip(gs_, util.balanced_cycle(len(gs_), 2, util.rng_for(seed, "card", sb, ent["name"]))):
                g["card_pick"] = CARDS_BASE[c]
    # S1 cards: pairC ties card to label BY DESIGN (70 CALL rows under defaults_ok, 70 ASK rows under strict_ask). In every
    # other S1 row the declared-default rule never fires, so the card cannot change the gold and is assigned PER ROW to
    # make P(defaults_ok | call-bearing) equal P(defaults_ok | no-call) over the whole sub-block.
    by_label = collections.defaultdict(list)
    pc_rows = collections.Counter()                                   # pairC rows per label (card fixed by design)
    for g in plan:
        if g["sub_block"] != "s1_need4":
            continue
        for i, lab in enumerate(g["spec"]["labels"]):
            if g["entry"] == "pairC":
                pc_rows[lab] += 1
            else:
                by_label[lab].append((g["gid"], i))
    p_def = 0.35                                                      # same P(defaults_ok) for EVERY S1 label
    row_card = {}
    for lab, rows in by_label.items():
        total = len(rows) + pc_rows[lab]
        pc_def = pc_rows[lab] if lab == "CALL" else 0                 # pairC: CALL arm is defaults_ok, ASK arm strict
        k = max(0, min(len(rows), int(round(p_def * total)) - pc_def))
        flags = [True] * k + [False] * (len(rows) - k)
        util.rng_for(seed, "s1card", lab).shuffle(flags)
        for key, f in zip(rows, flags):
            row_card[key] = "card.t54.defaults_ok" if f else "card.t54.strict_ask"
    for g in plan:
        if g["sub_block"] == "s1_need4" and g["entry"] != "pairC":
            g["row_cards"] = [row_card[(g["gid"], i)] for i in range(g["spec"]["size"])]
    # value-bearing span total T (same draw for every label): a balanced cycle per (sub-block, class signature)
    sig_rows = collections.defaultdict(list)
    for g in plan:
        sig = tuple(sa.is_call_bearing(l) for l in g["spec"].get("labels", ())) if g["sub_block"] in (
            "s1_need4", "s3_limit", "s4_precond") else ()
        sig_rows[(g["sub_block"], sig)].append(g)
    for key, gs in sig_rows.items():
        cyc_t = util.balanced_cycle(len(gs), len(T_VALUES), util.rng_for(seed, "T", key[0], str(key[1])))
        for g, i in zip(gs, cyc_t):
            g["T"] = T_VALUES[i]
    # S2: the gold tool's position in the list is balanced WITHIN each N (a shuffled cycle per N value)
    cyc, cur = {}, {}
    big_n = [g for g in plan if g["sub_block"] == "s2_pick" and g["n"] > 8]
    big_rows = sum(g["spec"]["size"] for g in big_n)
    dec_cycle = util.balanced_cycle(big_rows, 10, util.rng_for(seed, "tdec"))
    dpos = 0
    for g in plan:
        if g["sub_block"] != "s2_pick":
            continue
        n = g["n"]
        g["tpos"] = []
        for _ in range(g["spec"]["size"]):
            if n > 8:                                      # decile-balanced over all N > 8 rows
                d = dec_cycle[dpos]
                dpos += 1
                cand = [q for q in range(n) if int(q * 10 / n) == d] or [min(n - 1, int((d + 0.5) * n / 10))]
                g["tpos"].append(util.rng_for(seed, "tp", g["gid"], len(g["tpos"])).choice(cand))
                continue
            if n not in cyc:
                cyc[n], cur[n] = [], 0
            if cur[n] >= len(cyc[n]):
                perm = list(range(n))
                util.rng_for(seed, "tpos", n, len(cyc[n])).shuffle(perm)
                cyc[n] = perm
                cur[n] = 0
            g["tpos"].append(cyc[n][cur[n]])
            cur[n] += 1
    return plan


# =============================================================================================================
# world building
# =============================================================================================================
def _sample_n(rng, sb, nbin):
    lo, hi = NBINS[max(nbin, MIN_BIN[sb])]
    n = rng.randint(lo, hi)
    # S2 gold position is balanced per DECILE for N > 8 (gate P-7); with N = 9 the tenth decile cannot be reached (positions 0..8 map
    # to deciles 0..8), which pulled that decile below its bar in about one seed in five. N = 9 is therefore drawn as 10 in S2.
    return 10 if (sb == "s2_pick" and n == 9) else n


def _extra_params(tool, rng, n_req, n_opt, used_roles):
    free = [r for r in state.ROLES_T54 if r not in used_roles]
    rng.shuffle(free)
    for i in range(n_req + n_opt):
        if not free:
            break
        role = free.pop()
        tool["params"].append({"name": role, "role": "param." + role, "required": i < n_req,
                               "type": state.ROLE_TYPE[role], "default": None})
        used_roles.add(role)


def build_world(ctx, rng, key, sb, n_tools, target_verbs=None, hn_ns=True, hn_sv=True, n_extra_req=0, n_extra_opt=0,
                idempotent=None, min_req=0, ent0_ban=()):
    """A tool list of exactly n_tools tools around one target tool 't0'. Returns a world dict (unshuffled tools).
    `ent0_ban`: verbs that no OTHER tool on the target's entity may carry (S1: a fetch-capable sibling such as list / find /
    check on the same entity would make the NO_TOOL arm arguable, so none is ever listed)."""
    arch = rng.choice(ARCHETYPES)
    pool_verbs = [v for v in ARCH_VERBS[arch] if v in state.VERBS_T54]
    ents = ctx.names.draw_nouns("noun_entity", max(3, min(n_tools, 6)), key, rng)
    fields = ctx.names.draw_nouns("noun_field", 3, key + "/f", rng)
    tv = rng.choice(target_verbs or pool_verbs)
    ent0 = ents[0]
    target = state.build_tool("t0", tv, ent0, fields, set(state.ROLES_T54), rng, idempotent=idempotent)
    # the target gets unusual extra roles with the SAME probability as every distractor (n_extra_* are accepted for
    # call-site compatibility and ignored), so a rare role is never a cue for the target
    _maybe_extra(target, rng)
    _ensure_min_req(target, rng, min_req)
    tools, taken = [target], {target["name"]}
    tgroup = target["group"]
    syn = set(state.synonym_class(tv))

    def add(verb, ent, tid):
        nm = "%s_%s" % (verb, ent)
        if nm in taken or state.group_id(verb, ent) == tgroup or (ent == ent0 and verb in ent0_ban):
            return False
        tl = state.build_tool(tid, verb, ent, fields, set(state.ROLES_T54), rng)
        _maybe_extra(tl, rng)
        _ensure_min_req(tl, rng, min_req)
        tools.append(tl)
        taken.add(nm)
        return True

    hn_flags = {"ns": False, "sv": False}
    if n_tools >= 4:
        if hn_ns:
            for _ in range(20):
                v = rng.choice([x for x in pool_verbs if x not in syn and x not in ent0_ban])
                if add(v, ent0, "t%d" % len(tools)):
                    hn_flags["ns"] = True
                    break
        if hn_sv:
            for _ in range(20):
                if add(tv, rng.choice(ents[1:]), "t%d" % len(tools)):
                    hn_flags["sv"] = True
                    break
    guard = 0
    while len(tools) < n_tools and guard < 500:
        guard += 1
        v = rng.choice(state.VERBS_T54 if rng.random() < 0.4 else pool_verbs)
        e = rng.choice(ents[1:] if rng.random() < 0.8 else ents)
        if e == ent0 and v in syn:
            continue
        add(v, e, "t%d" % len(tools))
    if len(tools) < n_tools:
        raise RuntimeError("could not fill the tool list")
    return dict(arch=arch, ents=ents, fields=fields, tools=tools, target=target, hn=hn_flags)


def _maybe_extra(tool, rng, p_req=0.3, p_opt=0.35):
    """Distractors get unusual extra roles with the SAME probability as the target, so rare roles are not a cue."""
    used = {p["role"][6:] for p in tool["params"] if p["role"]}
    _extra_params(tool, rng, 1 if rng.random() < p_req else 0, 1 if rng.random() < p_opt else 0, used)


def _ensure_min_req(tool, rng, min_req):
    need = min_req - len([p for p in tool["params"] if p["required"]])
    if need > 0:
        _extra_params(tool, rng, need, 0, {p["role"][6:] for p in tool["params"] if p["role"]})


def declare_default(tool, pname, rng):
    p = next(x for x in tool["params"] if x["name"] == pname)
    p["default"] = state.gen_value(rng, p["type"], tool["entity"])
    return p["default"]


def make_intent_args(tool, rng, stem, stated_optional=0, omit=None):
    """Intent args over a tool's params: every required, plus `stated_optional` optional ones. `omit` = param name
    whose value nobody supplies (source 'none')."""
    args = []
    opt = [p for p in tool["params"] if not p["required"]]
    rng.shuffle(opt)
    chosen = [p for p in tool["params"] if p["required"]] + opt[:stated_optional]
    for p in chosen:
        a = dict(param=p["name"], required=p["required"], role=p["role"], type=p["type"], default=p["default"],
                 value=None, source="none")
        if p["name"] != omit:
            a["value"] = state.gen_value(rng, p["type"], stem)
            a["source"] = "user_turn"
        args.append(a)
    return args


def shuffle_tools(rng, tools):
    t = list(tools)
    rng.shuffle(t)
    return t


# =============================================================================================================
# scenario builders (return a base record; twins are made by deepcopy + edit)
# =============================================================================================================
def _base(ctx, g, rowspec, role):
    return dict(family=FAMILY, sub_block=g["sub_block"], entry=g["entry"], group_id=g["gid"], pair_role=role,
                edit=rowspec.get("edit"), card=g["card_pick"], cards=[g["card_pick"]], view="view.primary",
                facts=[], declared_conversions=[], perturb="perturb.none", flags={})


def _spans_plan(g, needed):
    """Total value-bearing spans in the user turns: the planned T (balanced across labels in build_plan), raised only
    when more spans are strictly needed. Decoy notes fill the gap to T."""
    return max(g["T"], needed)


FETCH_VERBS = ["get", "read", "lookup", "check"]


def build_s1(ctx, g):
    """S1 NEED4. EVERY S1 request is an information request ("What is the <field> of the <entity> <ref>?") so that the
    ANSWER rows (18% of S1; the value is already stated in the conversation) cannot be told apart by request wording.
    Action requests with write verbs live in S3 / S4 / S6."""
    spec, rng = g["spec"], ctx.rng("b", g["gid"], g.get("attempt", 0))
    name = spec["name"]
    n = g["n"]
    w = build_world(ctx, rng, g["gid"], "s1_need4", max(n, 2), target_verbs=FETCH_VERBS, hn_ns=True,
                    ent0_ban=tuple(sorted(state.READ_VERBS)))
    tool = w["target"]
    for p in tool["params"]:
        p["default"] = None
    idp = "%s_id" % tool["entity"]
    field = w["fields"][0]
    ref = state.gen_value(rng, "str", tool["entity"])
    if name == "pairC":
        declare_default(tool, idp, rng)
    base = _base(ctx, g, spec, "a")
    base.update(tools=shuffle_tools(rng, w["tools"]), archetype=w["arch"], lists=dict(n=n))
    args_full = make_intent_args(tool, rng, tool["entity"], stated_optional=0, omit=None)
    for a in args_full:
        if a["param"] == idp:
            a["value"] = ref
    base["intent"] = dict(type="tool", target_group=tool["group"], target_tid="t0", verb=tool["verb"],
                          entity=tool["entity"], args=args_full)
    base["flags"] = {"info_form": True, "info_ref": ref, "info_field": field}
    base["n_stated_call"] = len(args_full)
    base["lists"] = dict(n=n)
    if name == "pairD":
        # ANSWER vs CALL: the request is IDENTICAL; only the context differs (value already stated -> ANSWER, located
        # by fact id; or not stated -> CALL, a read tool fetches it)
        value = state.gen_value(rng, "str", tool["entity"])
        # The CALL arm's other required parameters (the target may carry extra required roles) are STATED in the request,
        # or the text would hold less than the record says (a CALL whose required value is nowhere in the text reads as
        # ASK). The request is identical in both arms, so the ANSWER arm renders the same stated clauses (`text_args`).
        text_args = [dict(param=a["param"], type=a["type"], value=a["value"], source="user_turn")
                     for a in args_full if a["param"] != idp and a["source"] == "user_turn"]
        ans = copy.deepcopy(base)
        ans["pair_role"] = "a"
        ans["intent"] = dict(type="info", target_group=tool["group"], verb=tool["verb"], entity=tool["entity"],
                             args=[], answer=dict(fact_id="f1", where="context", value=value))
        ans["facts"] = [dict(fact_id="f1", where="context", entity=tool["entity"], field=field, value=value, ref=ref)]
        ans["span_total"] = _spans_plan(g, 3 + len(text_args))
        ans["flags"] = dict(ans["flags"], text_args=text_args)
        call = copy.deepcopy(base)
        call["pair_role"] = "b"
        call["span_total"] = ans["span_total"]
        call["flags"] = dict(call["flags"], text_args=text_args)
        return [ans, call], w
    base["span_total"] = _spans_plan(g, len([a for a in args_full if a["source"] == "user_turn"]) + 2)
    b = copy.deepcopy(base)
    b["pair_role"] = "b"
    if name == "pairA":
        for a in b["intent"]["args"]:
            if a["param"] == idp:
                a["value"], a["source"] = None, "none"
        b["flags"] = dict(b["flags"], info_ref=None)
        if g["ref"]:
            base["flags"]["ref_phrased"] = idp
            b["flags"]["ref_phrased"] = idp
    elif name == "pairC":
        # same scenario, the id param unstated but with a DECLARED default; only the card differs
        dflt = next(p for p in tool["params"] if p["name"] == idp)["default"]
        for r in (base, b):
            for a in r["intent"]["args"]:
                if a["param"] == idp:
                    a["value"], a["source"], a["default"] = None, "none", dflt
            r["flags"] = dict(r["flags"], info_ref=None)
        base["card"], base["cards"] = "card.t54.defaults_ok", ["card.t54.defaults_ok"]
        b["card"], b["cards"] = "card.t54.strict_ask", ["card.t54.strict_ask"]
    elif name in ("pairB", "single_nt"):
        # tool-list edit: the target is removed and replaced by a read tool for ANOTHER entity, so the tool count and the
        # number of fetch-type descriptions are unchanged (their absence would otherwise be readable from the list text)
        b["tools"] = [t for t in b["tools"] if t["tid"] != "t0"]
        b["perturb"] = "perturb.del_tool"
        taken_names = {t["name"] for t in b["tools"]}
        others = [e for e in w["ents"] if e != tool["entity"]]
        for _ in range(60):
            v, e = rng.choice(FETCH_VERBS), rng.choice(others)
            nm = "%s_%s" % (v, e)
            if nm in taken_names or state.group_id(v, e) == tool["group"]:
                continue
            rep = state.build_tool("tx", v, e, w["fields"], set(state.ROLES_T54), rng)
            for p in rep["params"]:
                p["default"] = None
            _maybe_extra(rep, rng)
            b["tools"].insert(rng.randrange(len(b["tools"]) + 1), rep)
            break
        else:
            raise RuntimeError("no replacement read tool")
        assert not any(t["group"] == tool["group"] for t in b["tools"])
    if name == "single_nt":
        b["pair_role"] = None
        return [b], w
    base["pair_role"] = "a"
    return [base, b], w


def build_s2(ctx, g):
    spec, rng = g["spec"], ctx.rng("b", g["gid"], g.get("attempt", 0))
    n = g["n"]
    w = build_world(ctx, rng, g["gid"], "s2_pick", n, hn_ns=True, hn_sv=(rng.random() < 0.35))
    if rng.random() < 0.5 and not w["hn"]["ns"] and n >= 4:
        raise RuntimeError("expected a same-namespace hard negative")
    tool = w["target"]
    for p in tool["params"]:
        p["default"] = None
    hn = None
    if spec["name"] == "pair_hn":
        hn = next((t for t in w["tools"] if t["entity"] == tool["entity"] and t["tid"] != "t0"
                   and t["group"] != tool["group"]), None)
        if hn is None:
            raise RuntimeError("pair_hn needs a same-namespace hard negative")
        for p in hn["params"]:
            p["default"] = None
    # S2: the gold tool's position in the list is balanced within each N (g["tpos"], see build_plan); in a pair the
    # hard negative (gold of the second row) gets the second balanced position
    special = [tool] + ([hn] if hn is not None else [])
    rest = shuffle_tools(rng, [t for t in w["tools"] if t not in special])
    slots_ = [None] * n
    p0 = g["tpos"][0]
    slots_[p0] = tool
    if hn is not None:
        p1 = g["tpos"][1]
        if p1 == p0:
            p1 = (p1 + 1) % n
        slots_[p1] = hn
    it = iter(rest)
    ordered = [t if t is not None else next(it) for t in slots_]
    recs = []
    roles = ("a", "b") if spec["size"] == 2 else (None,)
    for ri, role in enumerate(roles):
        rec = _base(ctx, g, spec, role)
        tgt = tool if ri == 0 else hn
        rec.update(tools=copy.deepcopy(ordered), archetype=w["arch"])
        args = make_intent_args(tgt, rng if ri == 0 else ctx.rng("b2", g["gid"], g.get("attempt", 0)), tgt["entity"])
        rec["intent"] = dict(type="tool", target_group=tgt["group"], target_tid=tgt["tid"], verb=tgt["verb"],
                             entity=tgt["entity"], args=args, target_params=[p["name"] for p in tgt["params"]])
        rec["n_stated_call"] = len(args)
        rec["span_total"] = _spans_plan(g, len(args))
        rec["lists"] = dict(n=n, gold_pos=[t["tid"] for t in ordered].index(tgt["tid"]))
        recs.append(rec)
    # option shortlist: gold + 3 distractors, >= 1 same-namespace hard negative in >= 50% of rows (always, when available)
    for rec in recs:
        gold_t = next(t for t in rec["tools"] if t["tid"] == rec["intent"]["target_tid"])
        others = [t for t in rec["tools"] if t["tid"] != gold_t["tid"] and t["group"] != gold_t["group"]]
        hns = [t for t in others if t["entity"] == gold_t["entity"]]
        svs = [t for t in others if t["verb"] == gold_t["verb"] and t["entity"] != gold_t["entity"]]
        rest = [t for t in others if t not in hns and t not in svs]
        short = []
        orng = ctx.rng("opt", g["gid"], rec["pair_role"] or "s")
        if hns:
            short.append(orng.choice(hns))
        if svs and len(short) < 3 and orng.random() < 0.5:
            short.append(orng.choice(svs))
        pool = [t for t in hns + svs + rest if t not in short]
        orng.shuffle(pool)
        while len(short) < 3 and pool:
            short.append(pool.pop())
        rec["shortlist_tids"] = [gold_t["tid"]] + [t["tid"] for t in short[:3]]
    if spec["name"] == "pair_hn":
        # both rows of the pair use the SAME four candidate tools (target and its hard negative among them)
        tids = list(dict.fromkeys([tool["tid"], hn["tid"]] + recs[0]["shortlist_tids"] + recs[1]["shortlist_tids"]))[:4]
        for rec in recs:
            rec["shortlist_tids"] = tids
    return recs, w


# ---- S3 LIMIT --------------------------------------------------------------------------------------------------
def _ensure_two_required(tool, rng):
    used = {p["role"][6:] for p in tool["params"] if p["role"]}
    need = 2 - len([p for p in tool["params"] if p["required"]])
    if need > 0:
        _extra_params(tool, rng, need, 0, used)


def _read_tool_for_output(w, rng, tid="tr"):
    """A read tool (not in the target's group) that supplies a value from an earlier call; it replaces a plain
    distractor so the tool count is unchanged."""
    ent = w["ents"][1]
    verb = rng.choice(["get", "lookup", "list", "find", "check"])
    tr = state.build_tool(tid, verb, ent, w["fields"], set(state.ROLES_T54), rng)
    tr["rw"], tr["idempotent"] = "read", True
    for p in tr["params"]:
        p["default"] = None
    names_taken = {t["name"] for t in w["tools"]}
    if tr["name"] in names_taken:
        tr["name"] = "%s_%s" % (verb, ent)
    # replace the last plain distractor (never t0, never a hard negative)
    for i in range(len(w["tools"]) - 1, 0, -1):
        t = w["tools"][i]
        if t["entity"] != w["target"]["entity"] and t["verb"] != w["target"]["verb"] and t["name"] != tr["name"]:
            w["tools"][i] = tr
            return tr
    w["tools"].append(tr)
    return tr


def build_s3(ctx, g):
    spec, rng = g["spec"], ctx.rng("b", g["gid"], g.get("attempt", 0))
    dele = spec["dele"]
    n = g["n"]
    w = build_world(ctx, rng, g["gid"], "s3_limit", max(n, 3), min_req=2)
    tool = w["target"]
    _ensure_two_required(tool, rng)
    for p in tool["params"]:
        p["default"] = None
    tr = _read_tool_for_output(w, rng)
    req = [p for p in tool["params"] if p["required"]]
    p_out = req[0]["name"]
    p_user = req[1]["name"]
    args = make_intent_args(tool, rng, tool["entity"], stated_optional=0)
    for a in args:
        if a["param"] == p_out:
            a["source"] = "prior_tool_output"
    out_val = next(a["value"] for a in args if a["param"] == p_out)
    # the earlier call C1 on tr: its argument is a fresh value, its output carries the target's p_out value
    tr_arg = state.gen_value(rng, tr["params"][0]["type"] if tr["params"] else "str", tr["entity"]) if tr["params"] else None
    calls = [dict(tool=tr["name"], tid="tr", args=[(tr["params"][0]["name"], tr_arg)] if tr["params"] else [],
                  out=[(p_out, out_val)], supplies=p_out)]
    decoy_ok = [t for t in w["tools"] if t["tid"] not in ("t0", "tr")]
    rec = _base(ctx, g, spec, "a" if spec["size"] == 2 else None)
    rec.update(tools=shuffle_tools(rng, w["tools"]), archetype=w["arch"], view="view.with_outputs",
               calls=calls, lists=dict(n=n))
    rec["intent"] = dict(type="tool", target_group=tool["group"], target_tid="t0", verb=tool["verb"],
                         entity=tool["entity"], args=args)
    rec["n_stated_call"] = len([a for a in args if a["source"] == "user_turn"])
    rec["span_total"] = _spans_plan(g, rec["n_stated_call"])
    rec["decoy_tool_tid"] = decoy_ok[0]["tid"] if decoy_ok else None
    rec["null_pick"] = None
    deleted = copy.deepcopy(rec)
    if dele == "TOOL":
        # the target goes and a tool for ANOTHER entity takes its place, so the tool count (and the read / write mix) equals the
        # intact twin's: the number of tools must not tell the deletion
        deleted["tools"] = [t for t in deleted["tools"] if t["tid"] != "t0"]
        taken_names = {t["name"] for t in deleted["tools"]}
        others = [e for e in w["ents"] if e != tool["entity"]]
        for _ in range(80):
            v_, e_ = rng.choice(state.VERBS_T54), rng.choice(others)
            if "%s_%s" % (v_, e_) in taken_names or state.group_id(v_, e_) == tool["group"]:
                continue
            rep_ = state.build_tool("tx", v_, e_, w["fields"], set(state.ROLES_T54), rng)
            for p_ in rep_["params"]:
                p_["default"] = None
            _maybe_extra(rep_, rng)
            deleted["tools"].insert(rng.randrange(len(deleted["tools"]) + 1), rep_)
            break
        else:
            raise RuntimeError("no replacement tool")
        assert not any(t["group"] == tool["group"] for t in deleted["tools"]) and len(deleted["tools"]) == len(rec["tools"])
        deleted["perturb"] = "perturb.del_tool"
    elif dele == "PARAM":
        for a in deleted["intent"]["args"]:
            if a["param"] == p_user:
                a["value"], a["source"] = None, "none"
        deleted["perturb"] = "perturb.del_param"
    elif dele == "RESULT":
        for a in deleted["intent"]["args"]:
            if a["param"] == p_out:
                a["source"] = "missing_result"
        deleted["calls"][0]["out"] = None
        deleted["perturb"] = "perturb.del_result"
    elif dele == "NULL":
        kind = rng.choice(["tool", "opt_param", "extra_output"])
        deleted["perturb"] = "perturb.null_del"
        if kind == "tool" and deleted["decoy_tool_tid"]:
            deleted["tools"] = [t for t in deleted["tools"] if t["tid"] != deleted["decoy_tool_tid"]]
            deleted["null_pick"] = "tool"
        elif kind == "opt_param" and any(not p["required"] for t in deleted["tools"] if t["tid"] == "t0" for p in t["params"]):
            for t in deleted["tools"]:
                if t["tid"] == "t0":
                    t["params"] = [p for p in t["params"] if p["required"]]
            deleted["null_pick"] = "opt_param"
        else:
            deleted["null_pick"] = "extra_output"                 # an extra, unneeded earlier output is simply absent
            deleted["calls"] = list(deleted["calls"])
        deleted["null_control"] = True
    if dele == "NULL":
        deleted["pair_role"] = None
        return [deleted], w
    if spec["size"] == 2:
        rec["pair_role"], deleted["pair_role"] = "b", "a"
        return [deleted, rec], w                                   # a = deleted, b = intact twin
    deleted["pair_role"] = None
    return [deleted], w


# ---- S4 PRECOND ------------------------------------------------------------------------------------------------
def build_s4(ctx, g):
    spec, rng = g["spec"], ctx.rng("b", g["gid"], g.get("attempt", 0))
    name = spec["name"]
    n = g["n"]
    verb = rng.choice(S4_VERBS)
    # the designated read tool is the ONLY read tool on the write tool's entity
    w = build_world(ctx, rng, g["gid"], "s4_precond", max(n, 3), target_verbs=[verb], hn_ns=False, n_extra_req=0)
    wt = w["target"]
    # The idempotent flag is a rule input for UNOBSERVED rows only, so it is placed to make P(idempotent | call-bearing)
    # equal P(idempotent | no-call) over the whole sub-block (about one third each): idempotent writes are the 50 unobserved
    # WRITE singles, both rows of the 40 DONE/WRITE pairs, and the 40 observed ASK singles; everything else is not.
    idem = name in ("single_write_idem", "pair_done_write", "single_ask_missing")
    wt["idempotent"] = idem
    for p in wt["params"]:
        p["default"] = None
    # drop any other read-verb tool on the write entity
    w["tools"] = [t for i, t in enumerate(w["tools"]) if i == 0 or not (t["entity"] == wt["entity"] and t["rw"] == "read")]
    rtool = state.build_tool("tr", rng.choice(READ_FOR_STATE), wt["entity"], w["fields"], set(state.ROLES_T54), rng)
    rtool["rw"], rtool["idempotent"] = "read", True
    for p in rtool["params"]:
        p["default"] = None
    need_listed = name not in ("single_ask_noread",)
    while len(w["tools"]) < max(n, 3):                              # keep N after the removals
        v = rng.choice(state.VERBS_T54)
        e = rng.choice(w["ents"][1:])
        nm = "%s_%s" % (v, e)
        if nm not in {t["name"] for t in w["tools"]} and e != wt["entity"]:
            w["tools"].append(state.build_tool("t%d" % (len(w["tools"]) + 5), v, e, w["fields"], set(state.ROLES_T54), rng))
    if need_listed:
        if len(w["tools"]) >= max(n, 3):
            w["tools"][-1] = rtool
        else:
            w["tools"].append(rtool)
    done_word, other_word = STATE_WORDS[verb]
    omit = None
    if name == "single_ask_missing":
        req = [p for p in wt["params"] if p["required"]]
        omit = req[-1]["name"] if len(req) > 1 or not req[0]["name"].endswith("_id") else None
        if omit is None:
            _extra_params(wt, rng, 1, 0, {p["role"][6:] for p in wt["params"] if p["role"]})
            omit = wt["params"][-1]["name"]
    args = make_intent_args(wt, rng, wt["entity"], omit=omit)
    ref = next((a["value"] for a in args if a["param"].endswith("_id")), None) or args[0]["value"]
    rec = _base(ctx, g, spec, "a" if spec["size"] == 2 else None)
    rec.update(tools=shuffle_tools(rng, w["tools"]), archetype=w["arch"], view="view.with_outputs", lists=dict(n=n))
    rec["intent"] = dict(type="tool", target_group=wt["group"], target_tid="t0", verb=verb, entity=wt["entity"], args=args)
    rec["cards"] = [rec["card"], "card.t54.read_before_write"]
    rec["n_stated_call"] = len([a for a in args if a["source"] == "user_turn"])
    rec["span_total"] = _spans_plan(g, rec["n_stated_call"])
    has_r = need_listed
    rec["fact"] = dict(id="f1", state="unobserved", write_tid="t0", read_tid="tr" if has_r else None,
                       done_word=done_word, other_word=other_word, entity=wt["entity"], ref=ref)
    rec["calls"] = []
    decoy = next((t for t in rec["tools"] if t["rw"] == "read" and t["tid"] not in ("t0", "tr")
                  and t["entity"] != wt["entity"]), None)
    if decoy is None:                                   # make one: convert a plain distractor into a read tool
        for t in rec["tools"]:
            if t["tid"] not in ("t0", "tr") and t["entity"] != wt["entity"] and t["verb"] not in READ_FOR_STATE:
                nt = state.build_tool(t["tid"], rng.choice(READ_FOR_STATE), t["entity"], w["fields"], set(state.ROLES_T54), rng)
                nt["rw"], nt["idempotent"] = "read", True
                if nt["name"] not in {x["name"] for x in rec["tools"]}:
                    rec["tools"][rec["tools"].index(t)] = nt
                    decoy = nt
                    break
    rec["decoy_read_tid"] = decoy["tid"] if decoy else None

    def observed(r, true_):
        r["fact"]["state"] = "observed_true" if true_ else "observed_false"
        r["calls"] = [dict(tool=rtool["name"], tid="tr", args=[(rtool["params"][0]["name"], ref)],
                           out=[("state", done_word if true_ else other_word)], fact_call=True)]

    labels = spec["labels"]
    if name in ("pair_done_read", "pair_done_write"):
        a = copy.deepcopy(rec)
        observed(a, True)                                           # DONE_NO_CALL arm
        b = copy.deepcopy(rec)
        if name == "pair_done_read":
            b["fact"]["state"] = "unobserved"                       # edit D: the read is not there -> READ_FIRST
        else:
            observed(b, False)                                      # edit D: observed false -> WRITE
        a["pair_role"], b["pair_role"] = "a", "b"
        return [a, b], w
    if name == "pair_read_ask":
        a = copy.deepcopy(rec)
        a["pair_role"] = "a"                                        # READ_FIRST: read tool listed
        b = copy.deepcopy(rec)
        b["pair_role"] = "b"
        b["tools"] = [t for t in b["tools"] if t["tid"] != "tr"]    # edit B: no read tool for THIS object -> ASK
        b["fact"]["read_tid"] = None
        _swap_in_other_read_tool(b, w, rng)                         # ...but the number of read tools is unchanged
        return [a, b], w
    if name == "single_write_idem":
        return [rec], w
    if name == "single_write_false":
        observed(rec, False)
        return [rec], w
    if name == "single_ask_noread":
        _swap_in_other_read_tool(rec, w, rng)
        return [rec], w
    if name == "single_ask_missing":
        observed(rec, False)
        return [rec], w
    raise RuntimeError(name)


def _swap_in_other_read_tool(rec, w, rng):
    """Add a read tool for ANOTHER entity so the count of read tools does not tell whether this object has one."""
    wt = w["target"]
    taken = {t["name"] for t in rec["tools"]}
    for _ in range(60):
        v, e = rng.choice(READ_FOR_STATE), rng.choice([x for x in w["ents"] if x != wt["entity"]])
        if "%s_%s" % (v, e) in taken:
            continue
        nt = state.build_tool("tx", v, e, w["fields"], set(state.ROLES_T54), rng)
        nt["rw"], nt["idempotent"] = "read", True
        for p in nt["params"]:
            p["default"] = None
        rec["tools"].insert(rng.randrange(len(rec["tools"]) + 1), nt)
        return
    raise RuntimeError("no replacement read tool")


# ---- S5 ARGGROUND ----------------------------------------------------------------------------------------------
DECLARED_UNITS = {"kg_to_g": ("kilograms", "grams", 1000), "km_to_m": ("kilometres", "metres", 1000),
                  "min_to_s": ("minutes", "seconds", 60)}


def _near_miss(value, rng):
    """A value of similar length that appears nowhere (digit changed)."""
    chars = list(value)
    idxs = [i for i, c in enumerate(chars) if c.isdigit()]
    if not idxs:
        return value + "x"
    i = rng.choice(idxs)
    chars[i] = str((int(chars[i]) + 1 + rng.randrange(8)) % 10)
    out = "".join(chars)
    return out if out != value else value[:-1] + ("7" if value[-1] != "7" else "3")


def build_s5(ctx, g):
    spec, rng = g["spec"], ctx.rng("b", g["gid"], g.get("attempt", 0))
    n = g["n"]
    w = build_world(ctx, rng, g["gid"], "s5_argground", max(n, 3), min_req=2)
    tool = w["target"]
    _ensure_two_required(tool, rng)
    base_card = g["card_pick"]
    for p in tool["params"]:
        p["default"] = None
    rec = _base(ctx, g, spec, "a" if spec["size"] == 2 else None)
    rec.update(tools=shuffle_tools(rng, w["tools"]), archetype=w["arch"], view="view.with_outputs", lists=dict(n=n))
    req = [p for p in tool["params"] if p["required"]]
    chosen = req[:3]
    opt = [p for p in tool["params"] if not p["required"]]
    if opt and rng.random() < 0.5:
        chosen.append(opt[0])
    numeric = [p for p in chosen if p["type"] in ("int", "num")]
    args, calls, user_vals = [], [], []
    kinds = ["user_turn", "prior_output_same_role", "transform", "card_default"]
    rng.shuffle(kinds)
    for i, p in enumerate(chosen):
        kind = kinds[i % len(kinds)]
        if kind == "card_default" and base_card != "card.t54.defaults_ok":
            kind = "user_turn"
        v = state.gen_value(rng, p["type"], tool["entity"])
        a = dict(param=p["name"], required=p["required"], type=p["type"], value=v, role=p["role"],
                 prov=dict(kind=kind), src_value=v)
        if kind == "card_default":
            p["default"] = v
            a["prov"] = dict(kind="card_default")
        elif kind == "transform":
            if p in numeric and rng.random() < 0.6:
                conv = rng.choice(sorted(DECLARED_UNITS))
                ufrom, uto, fac = DECLARED_UNITS[conv]
                base_n = rng.randrange(2, 20)
                a["src_value"] = "%d %s" % (base_n, ufrom)
                a["value"] = str(base_n * fac)
                a["prov"] = dict(kind="transform", base="user_turn", transform=conv)
                rec["declared_conversions"] = rec["declared_conversions"] + [conv]
            else:
                t = rng.choice(["case", "whitespace"]) if any(ch.isalpha() for ch in v) else "whitespace"   # a case change of a digits-only value changes nothing
                a["prov"] = dict(kind="transform", base=rng.choice(["user_turn", "prior_output_same_role"]), transform=t)
                if t == "case":
                    v = "".join(rng.choice([c.upper(), c]) if c.isalpha() else c for c in v)
                    a["src_value"], a["value"] = v.lower(), v.upper()
                else:
                    a["src_value"], a["value"] = "  " + v, v          # leading padding only: a trailing space would not survive any line-trimming step
        pk = a["prov"]["kind"]
        base_kind = a["prov"]["base"] if pk == "transform" else pk
        a["ctx"] = {"user_turn": "user", "prior_output_same_role": "output", "card_default": "default"}[base_kind]
        args.append(a)
    rec["call"] = dict(tool_tid="t0", name=tool["name"], args=args)
    rec["card"], rec["cards"] = base_card, [base_card]
    rec["intent"] = dict(type="tool", target_group=tool["group"], args=[])
    rec["n_stated_call"] = len([a for a in args if a["prov"]["kind"] == "user_turn" or a["prov"].get("base") == "user_turn"])
    rec["span_total"] = _spans_plan(g, rec["n_stated_call"])
    # the grounded base is complete; ungrounded rows are made by ONE provenance edit
    grounded = rec
    if spec["name"] == "pair_prov":
        u = copy.deepcopy(rec)
        _ungrounded_edit(u, rng, ctx)
        grounded["pair_role"], u["pair_role"] = "a", "b"
        return [grounded, u], w
    if spec["labels"] == ("UNGROUNDED",):
        _ungrounded_edit(grounded, rng, ctx)
    return [grounded], w


def _ungrounded_edit(rec, rng, ctx):
    """ONE length-preserving provenance edit that makes exactly one value ungrounded:
       swap   -- the call carries a near-miss of the value that is in context;
       remove -- the context mention is replaced by a near-miss, so the call's value appears nowhere;
       role   -- (prior-output values only) the value stays in context but under a different field key."""
    args = rec["call"]["args"]
    plain = [a for a in args if a["prov"]["kind"] in ("user_turn", "prior_output_same_role")]
    if plain:
        a = rng.choice(plain)
        modes = ["swap", "remove"] + (["role"] if a["prov"]["kind"] == "prior_output_same_role" else [])
        mode = rng.choice(modes)
    else:
        a = rng.choice([x for x in args if x["prov"]["kind"] == "transform"] or args)
        mode = "swap"
    if mode == "swap":
        a["value"] = _near_miss(a["value"], rng)
        a["prov"] = dict(kind="none")
    elif mode == "remove":
        a["src_value"] = _near_miss(a["src_value"], rng)
        a["prov"] = dict(kind="none")
    else:
        a["prov"] = dict(kind="wrong_role")
        a["ctx"] = "output_wrong"
    a["edit_mode"] = mode


# ---- S6 PARSEQ -------------------------------------------------------------------------------------------------
def build_s6(ctx, g):
    spec, rng = g["spec"], ctx.rng("b", g["gid"], g.get("attempt", 0))
    sizes = spec["sizes"]
    r_a = sizes[0]
    if sizes[-1] == 3 and len(sizes) == 1:                         # "3+" singles: 3 or 4
        r_a = rng.choice([3, 3, 4])
    paired = len(sizes) == 2
    n_blocked = 2 if paired else rng.choice([1, 1, 2])
    n_done = rng.choice([0, 1, 1, 2])
    need = r_a + n_blocked + n_done
    n = max(g["n"], need + 1)
    w = build_world(ctx, rng, g["gid"], "s6_parseq", n, hn_ns=False, hn_sv=False)
    # plan nodes get distinct entities/verbs -> distinct equivalence groups
    ents = w["ents"] + ctx.names.draw_nouns("noun_entity", 8, g["gid"] + "/more", rng)
    ents = list(dict.fromkeys(ents))
    node_ids = ["n%d" % i for i in range(need)]
    # DAG with the exact ready shape: r_a ready (+1 for the pair's freed node handled below)
    nodes, edges, done = dagmod.build_layered_dag(rng, n_done, r_a, n_blocked)
    x_of_b = None
    if paired:
        # blocked node b that depends ONLY on ready node x (edit E removes that single edge)
        orig_ready = dagmod.ready_set(nodes, edges, done)
        blocked = [nn for nn in nodes if nn not in done and nn not in orig_ready]
        b_node = blocked[0]
        edges = [e for e in edges if e[1] != b_node]
        x_of_b = rng.choice(orig_ready)
        edges.append((x_of_b, b_node))
    pool_verbs = [v for v in state.VERBS_T54 if v not in ("sync",)]
    tools_by_node, used = {}, set()
    for i, nid in enumerate(nodes):
        for _ in range(100):
            v = rng.choice(pool_verbs)
            e = ents[i % len(ents)]
            gname = state.group_id(v, e)
            if gname not in used and ("%s_%s" % (v, e)) not in {t["name"] for t in tools_by_node.values()}:
                used.add(gname)
                break
        t = state.build_tool("p%d" % i, v, e, w["fields"], set(state.ROLES_T54), rng)
        for p in t["params"]:
            p["default"] = None
        tools_by_node[nid] = t
    alias_nodes = {}
    if rng.random() < 0.6:
        nid = rng.choice(nodes)
        al = state.make_equivalent(tools_by_node[nid], "q%s" % nid, set(state.VERBS_T54), rng)
        if al is not None and al["name"] not in {t["name"] for t in tools_by_node.values()}:
            alias_nodes[nid] = al
    # step numbers: a shuffled labelling so the number carries no level information
    order = list(nodes)
    rng.shuffle(order)
    step_no = {nid: i + 1 for i, nid in enumerate(order)}
    preds = {nid: sorted(u for (u, v_) in edges if v_ == nid) for nid in nodes}
    # arguments: a consuming argument takes "<result of step k>"; the rest are stated values
    node_args = {}
    for nid in nodes:
        t = tools_by_node[nid]
        req = [p for p in t["params"] if p["required"]]
        al = []
        for j, p in enumerate(req):
            if j < len(preds[nid]):
                al.append(dict(param=p["name"], value=None, from_step=step_no[preds[nid][j]]))
            else:
                al.append(dict(param=p["name"], value=state.gen_value(rng, p["type"], t["entity"]), from_step=None))
        node_args[nid] = al
    # tools without enough params for all predecessors: add a required param
    for nid in nodes:
        t = tools_by_node[nid]
        short = len(preds[nid]) - len([p for p in t["params"] if p["required"]])
        if short > 0:
            used_roles = {p["role"][6:] for p in t["params"] if p["role"]}
            _extra_params(t, rng, short, 0, used_roles)
            req = [p for p in t["params"] if p["required"]]
            node_args[nid] = []
            for j, p in enumerate(req):
                if j < len(preds[nid]):
                    node_args[nid].append(dict(param=p["name"], value=None, from_step=step_no[preds[nid][j]]))
                else:
                    node_args[nid].append(dict(param=p["name"], value=state.gen_value(rng, p["type"], t["entity"]), from_step=None))
    # list of tools: every plan tool (+ alias), then plain distractors up to n
    listed = [copy.deepcopy(tools_by_node[nid]) for nid in nodes] + [copy.deepcopy(a) for a in alias_nodes.values()]
    taken = {t["name"] for t in listed}
    extra_ready = None
    guard = 0
    while len(listed) < n and guard < 400:
        guard += 1
        v, e = rng.choice(pool_verbs), rng.choice(ents)
        if ("%s_%s" % (v, e)) in taken or state.group_id(v, e) in used:
            continue
        t = state.build_tool("d%d" % len(listed), v, e, w["fields"], set(state.ROLES_T54), rng)
        for p in t["params"]:
            p["default"] = None
        listed.append(t)
        taken.add(t["name"])
        extra_ready = extra_ready or t
    if extra_ready is None:
        for _ in range(100):
            v, e = rng.choice(pool_verbs), rng.choice(ents)
            if ("%s_%s" % (v, e)) not in taken and state.group_id(v, e) not in used:
                extra_ready = state.build_tool("d%d" % len(listed), v, e, w["fields"], set(state.ROLES_T54), rng)
                for p in extra_ready["params"]:
                    p["default"] = None
                listed.append(extra_ready)
                break
    results = {nid: state.gen_value(rng, "str", tools_by_node[nid]["entity"]) for nid in done}

    def make(edge_removed):
        rec = _base(ctx, g, spec, None)
        e2 = [e for e in edges if not (edge_removed and e == (x_of_b, b_node))] if paired else list(edges)
        pr2 = {nid: sorted(u for (u, v_) in e2 if v_ == nid) for nid in nodes}
        na = copy.deepcopy(node_args)
        if paired and edge_removed:
            t = tools_by_node[b_node]
            for a in na[b_node]:
                if a["from_step"] is not None:
                    pnm = a["param"]
                    pty = next(p["type"] for p in t["params"] if p["name"] == pnm)
                    a["from_step"], a["value"] = None, state.gen_value(rng, pty, t["entity"])
        rec.update(tools=shuffle_tools(rng, copy.deepcopy(listed)), archetype=w["arch"], cards=[rec["card"], "card.t54.parallel_ok"],
                   lists=dict(n=len(listed)))
        rec["dag"] = dict(nodes=list(nodes), edges=[list(e) for e in e2], done=list(done),
                          node_tools=[dict(id=nid, tool=tools_by_node[nid]["name"], group=tools_by_node[nid]["group"],
                                           alias=(alias_nodes[nid]["name"] if nid in alias_nodes else None))
                                      for nid in nodes],
                          step_no=step_no, args=na, results=results)
        rec["intent"] = dict(type="tool", target_group="", args=[])
        rec["n_stated_call"] = sum(1 for nid in nodes for a in na[nid] if a["value"] is not None)
        rec["span_total"] = rec["n_stated_call"]
        rec["extra_ready_tool"] = extra_ready["name"] if extra_ready else None
        rec["extra_ready_args"] = [(p["name"], state.gen_value(rng, p["type"], extra_ready["entity"]))
                                   for p in extra_ready["params"] if p["required"]] if extra_ready else []
        _s6_options(rec, rng)
        return rec

    if paired:
        a_rec, b_rec = make(False), make(True)
        a_rec["pair_role"], b_rec["pair_role"] = "a", "b"
        return [a_rec, b_rec], w
    return [make(False)], w


S6_COUNT_P = ((1, 0.3), (2, 0.4), (3, 0.2), (4, 0.1))      # the ready-set size marginal of the sub-block (30 / 40 / 30 with 3+ = 3 or 4)


def _s6_options(rec, rng):
    """Four candidate call sets; exactly one equals the ready set after canonicalisation (asserted by solver A).
    The three distractors are wrong for a visible reason (a ready call is missing, a call that consumes a missing output is
    included, a call that is already done or not in the plan is included) and their SIZES are drawn from the same marginal as
    the gold's size, independently of it: the gold's rank by size is then uniform, so 'the middle-sized set' or 'the modal size'
    is no cue (measured before this change: the size heuristics picked the gold in 45% of rows against 25% by chance)."""
    d = rec["dag"]
    ready = list(sa.s6_ready_nodes(rec))
    tinfo = {t["id"]: t for t in d["node_tools"]}
    remaining = [n for n in d["nodes"] if n not in d["done"]]
    blocked = [n for n in remaining if n not in ready]
    wrong_universe = [("n", n) for n in blocked] + [("n", n) for n in d["done"]] + [("x", "x")]
    gold_canon = tuple(sorted(sa.s6_canonical(rec, ready)))
    opts, seen = [], set()

    def add(kind, nodes_, extra):
        canon = sorted(list(sa.s6_canonical(rec, nodes_)) + (["g:extra:%s" % rec["extra_ready_tool"]] if extra else []))
        key = tuple(canon)
        if key in seen:
            return False
        seen.add(key)
        parts = []
        for nid in sorted(nodes_, key=lambda x: d["step_no"][x]):
            nm = tinfo[nid]["alias"] if (tinfo[nid]["alias"] and rng.random() < 0.5) else tinfo[nid]["tool"]
            parts.append((nm, nid))
        if extra:
            parts.append((rec["extra_ready_tool"], "x"))
        opts.append(dict(label="set:" + "+".join(canon), canon=canon, kind=kind, parts=parts))
        return True

    add("gold", ready, False)
    assert tuple(opts[0]["canon"]) == gold_canon
    kinds = []
    for _ in range(3):
        for _try in range(200):
            c = rng.choices([c_ for c_, _w in S6_COUNT_P], [w_ for _c, w_ in S6_COUNT_P])[0]
            c = min(c, len(ready) + len(wrong_universe))
            lo = max(1 if ready else 0, c - len(wrong_universe))
            hi = min(len(ready), c)
            if lo > hi:
                continue
            k = rng.randint(lo, hi)                                    # how many ready calls the distractor keeps
            if k == len(ready) and c == len(ready):
                continue                                               # that would BE the ready set
            keep = rng.sample(ready, k)
            fill = rng.sample(wrong_universe, c - k)
            nodes_ = keep + [n for t, n in fill if t == "n"]
            extra = any(t == "x" for t, _n in fill)
            kind = "small" if (not fill and k < len(ready)) else ("large" if any(n in blocked for n in nodes_) else "wrong")
            if add(kind, nodes_, extra):
                kinds.append(kind)
                break
        else:
            raise RuntimeError("no distinct S6 distractor")
    rng.shuffle(opts)
    rec["s6_options"] = opts


# =============================================================================================================
# driver
# =============================================================================================================
BUILDERS = {"s1_need4": build_s1, "s2_pick": build_s2, "s3_limit": build_s3, "s4_precond": build_s4,
            "s5_argground": build_s5, "s6_parseq": build_s6}


MAX_ATTEMPTS = 12


def generate_group(ctx, g):
    """One group -> finished records. A group the spec cannot realise (S2 with two satisfying tools, a tool list that
    cannot be filled, ...) is REJECTED and regenerated with the next attempt number (deterministic). A disagreement
    between solver A and the entry's intended labels is a BUILD BUG and raises (never retried)."""
    last = None
    for attempt in range(MAX_ATTEMPTS):
        g["attempt"] = attempt
        try:
            return _generate_group_once(ctx, g)
        except (sa.SpecError, RuntimeError, dagmod.DagError) as e:
            last = e
            ctx.rejected = getattr(ctx, "rejected", 0) + 1
    raise RuntimeError("group %s rejected %d times: %s" % (g["gid"], MAX_ATTEMPTS, last))


def _generate_group_once(ctx, g):
    import t54_render as rd
    recs, _w = BUILDERS[g["sub_block"]](ctx, g)
    out = []
    spec = g["spec"]
    for r in recs:                                    # parameters of the intended target tool (before any deletion)
        r["intent"].setdefault("target_params", [p["name"] for p in _w["target"]["params"]])
    for i, r in enumerate(recs):
        if g.get("row_cards"):
            r["card"], r["cards"] = g["row_cards"][i], [g["row_cards"][i]]
        out.append(rd.finalize(ctx, g, r, int(g["pos"][i])))
    sb = g["sub_block"]
    if sb in ("s1_need4", "s3_limit", "s4_precond", "s5_argground"):
        want = spec["labels"]
        got = tuple(r["gold"] for r in out)
        if got != tuple(want):
            raise AssertionError("%s %s: solver A gave %s, entry intends %s" % (g["gid"], spec["name"], got, want))
    if sb == "s6_parseq":
        for r, s_ in zip(out, spec["sizes"]):
            if len(sa.s6_ready_nodes(r)) != s_ and not (s_ == 3 and len(spec["sizes"]) == 1 and len(sa.s6_ready_nodes(r)) in (3, 4)):
                raise AssertionError("%s: ready size %d, intended %s" % (g["gid"], len(sa.s6_ready_nodes(r)), s_))
    return out


def generate_in_memory(total=20, seed="t54-dry", standin=True, ctx=None):
    """Build `total` examples IN MEMORY (unit tests / dry run only; nothing is written). Production row jobs use
    standin=False and are refused until namespace.py has the noun kinds (names.NameSource)."""
    ctx = ctx or Ctx(seed=seed, standin=standin)
    plan = build_plan(total=total, seed=seed)
    recs = []
    for g in plan:
        recs.extend(generate_group(ctx, g))
    return recs
