"""T56 DONE-CLAIM (done-claim half) generator (CODE ONLY: no rows are written; `generate_in_memory` returns records for unit
tests and the 20-example dry run). Clean-room: built from G0_LITE.md + G0_APPROVALS only. T56g (test gaming) is lane L-C's.

The scenario skeleton (items, values, call order, oddities, claim, task) is drawn from one RNG stream seeded by the group id;
the fault only changes the simulated environment's behaviour, so a matched pair has a byte-identical task, call skeleton and
closing claim, and differs ONLY in tool outputs (D5: by the existence of one verification call and its output).
Labels come from SOLVER A only (t56_solver_a.gold)."""
import collections
import copy
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_ROOT, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from tool_engine import names as names_mod, perturb, state, util  # noqa: E402
import t56_env as E  # noqa: E402
import t56_solver_a as sa  # noqa: E402
import t56_wording as tw  # noqa: E402

FAMILY = "T56"
SUB_BLOCKS = ("d1_evidence", "d2_ledger", "d3_demo_only", "d4_ready", "d5_unverified")
SIZES = {"d1_evidence": 900, "d2_ledger": 350, "d3_demo_only": 250, "d4_ready": 300, "d5_unverified": 200}
TOTAL = 2000
STAGES = ("early", "mid", "finish")
D1_FAULTS = {"f_unmet": 120, "f_count_short": 100, "f_skipped": 65, "f_stale_run": 90, "f_wrong_target": 75}
D4_FAULTS = {"f_stray": 75, "f_stale_final": 35, "f_failing_prior": 40}
D2_FAULTS = {"f_ledger_dup": 90, "f_ledger_missing": 85}
D3_FAULTS = {"import_not_wired": 31, "flag_default_off": 31, "unreachable_branch": 31, "helper_never_called": 32}
LANG_W = {"python": 40, "javascript": 20, "go": 20, "bash": 20}
STATUS_WORDS = ["closed", "archived", "approved", "shipped", "paused", "finalised"]


def _entries_from_faults(faults, pair_share):
    out = []
    singles_total = 0
    for f, cnt in faults.items():
        pairs = int(round(pair_share * cnt))
        sing = cnt - pairs
        singles_total += sing
        out.append(dict(name="p_" + f, size=2, rows=2 * pairs, fault=f, labels=("DONE", "CONTINUE")))
        if sing:
            out.append(dict(name="s_" + f, size=1, rows=sing, fault=f, labels=("CONTINUE",)))
    out.append(dict(name="s_done", size=1, rows=singles_total, fault="f_none", labels=("DONE",)))
    return out


def _entries_d4():
    out = []
    singles_total = 0
    for f, cnt in D4_FAULTS.items():
        pairs = int(round(0.8 * cnt))
        sing = cnt - pairs
        singles_total += sing
        out.append(dict(name="p_" + f, size=2, rows=2 * pairs, fault=f, labels=("READY", "NOT_READY")))
        if sing:
            out.append(dict(name="s_" + f, size=1, rows=sing, fault=f, labels=("NOT_READY",)))
    out.append(dict(name="s_ready", size=1, rows=singles_total, fault="f_none", labels=("READY",)))
    return out


ENTRIES = {
    "d1_evidence": _entries_from_faults(D1_FAULTS, 0.8),
    "d2_ledger": [dict(name="p_" + f, size=2, rows=2 * c, fault=f, labels=("DONE", "CONTINUE")) for f, c in D2_FAULTS.items()],
    "d3_demo_only": [dict(name="p_" + v, size=2, rows=2 * c, fault="f_demo_only", variant=v, labels=("DONE", "CONTINUE"))
                     for v, c in D3_FAULTS.items()],
    "d4_ready": _entries_d4(),
    "d5_unverified": [dict(name="p_no_check", size=2, rows=200, fault="f_no_check", labels=("DONE", "CONTINUE"))],
}
LABEL_MIX = {"d1_evidence": {"DONE": .5, "CONTINUE": .5}, "d2_ledger": {"DONE": .5, "CONTINUE": .5},
             "d3_demo_only": {"DONE": .5, "CONTINUE": .5}, "d4_ready": {"READY": .5, "NOT_READY": .5},
             "d5_unverified": {"DONE": .5, "CONTINUE": .5}}
REASON_MIX = {  # CONTINUE / NOT_READY reasons per sub-block (rows at the nominal size)
    "d1_evidence": {"unmet_criterion": 120, "short_coverage": 165, "stale_evidence": 90, "wrong_target": 75},
    "d2_ledger": {"ledger_mismatch": 175}, "d3_demo_only": {"dead_or_demo_only": 125},
    "d4_ready": {"stray_change": 75, "stale_evidence": 35, "unmet_criterion": 40}, "d5_unverified": {"unverified": 100},
}
N_REQ = {"early": (1, 2), "mid": (3, 4), "finish": (5, 6)}       # finish = 5+ store criteria; 5-6 keeps the token mean under the G6 bar


class Ctx:
    def __init__(self, seed="t56-v1", standin=False, pool=None, names_src=None):
        self.seed = seed
        self.names = names_src or names_mod.NameSource(FAMILY, seed=seed, standin=standin)
        self.pool = pool or tw.seed_pool()
        self.pool.balanced = True                       # every wording of a form is used equally often (see WordingPool)

    def rng(self, *parts):
        return util.rng_for(self.seed, *parts)

    def pick(self, form_id, gid, key):
        return self.pool.pick(form_id, self.rng("w", gid, key), key=(gid, key))


# =============================================================================================================
# plan
# =============================================================================================================
def alloc_entries(n_rows, entries):
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


def build_plan(total=TOTAL, seed="t56-plan-v1", n_claims=None):
    sizes = util.largest_remainder(total, SIZES)
    plan = []
    for sb in SUB_BLOCKS:
        alloc = alloc_entries(sizes[sb], ENTRIES[sb])
        for e in ENTRIES[sb]:
            for i in range(alloc[e["name"]]):
                plan.append(dict(gid="%s-%s-%05d" % (sb[:2], e["name"], i), sub_block=sb, entry=e["name"], spec=e))
    util.rng_for(seed, "order").shuffle(plan)
    # stage, claim wording, output style and language: balanced INSIDE every entry. An entry fixes the fault (so the reason) of its rows;
    # a balance over the sub-block only would let stage (the number of criteria in the task text), the claim wording or the style
    # drift between faults by chance, and the reason head's text-only probe (task + claim, no outputs) would read that drift.
    # Stage keeps its per-sub-block 30-37% share (every entry splits evenly); the claim index is balanced separately for the
    # positive-first and the negative-first entries so every claim wording is used with both labels (DONE share 50% per claim).
    for sb in SUB_BLOCKS:
        for ent in ENTRIES[sb]:
            gs = [g for g in plan if g["sub_block"] == sb and g["entry"] == ent["name"]]
            n = len(gs)
            st = util.balanced_cycle(n, 3, util.rng_for(seed, "stage", sb, ent["name"]))
            nc = n_claims or len(tw.CLAIMS[_claim_key(sb)])        # the size of the claim pool in use (the expanded pool in production)
            cl = util.balanced_cycle(n, nc, util.rng_for(seed, "claim", sb, ent["name"]))
            sty = util.balanced_cycle(n, 2, util.rng_for(seed, "style", sb, ent["name"]))
            lg = util.balanced_cycle(n, 5, util.rng_for(seed, "lang", sb, ent["name"]))      # python 2 of 5, the other three 1 each
            for g, s_, c_, y_, l_ in zip(gs, st, cl, sty, lg):
                g["stage"], g["claim_idx"], g["style"] = STAGES[s_], c_, ("counts", "lines")[y_]
                g["lang"] = ("python", "python", "javascript", "go", "bash")[l_]
    # head rows: <= 25% of the specs, chosen by a seeded hash of the group id (same split as the primary row)
    ranked = sorted(plan, key=lambda g_: util.sha256_text("%s|head|%s" % (seed, g_["gid"])))
    cut = int(0.25 * len(plan))
    for i, g in enumerate(ranked):
        g["head"] = i < cut                                  # exactly the lowest-hash 25% of the specs (a pair is one spec)
    # balanced gold position (option order of the two options) per (sub-block, label)
    by = collections.defaultdict(list)
    for g in plan:
        for i, lab in enumerate(g["spec"]["labels"]):
            by[(g["sub_block"], lab)].append((g["gid"], i))
    pos_of = {}
    for key, items in by.items():
        for (gid_, i), pv in zip(items, util.balanced_cycle(len(items), 2, util.rng_for(seed, "pos", *key))):
            pos_of[(gid_, i)] = pv
    for g in plan:
        g["pos"] = [pos_of[(g["gid"], i)] for i in range(g["spec"]["size"])]
    return plan


def _claim_key(sb):
    return "all"


def n_required(stage, rs):
    lo, hi = N_REQ[stage]
    return rs.randint(lo, hi)


# =============================================================================================================
# scenario construction (shared helpers)
# =============================================================================================================
def _ident(rs, noun):
    return "%s-%d" % (state.id_stem(noun), rs.randrange(100, 9999))


def _warn_sets(rs, n_calls):
    """Oddities decided in the skeleton (identical across a pair): per-call warnings and a trace length."""
    warn = [rs.choice(tw.WARNINGS) if rs.random() < 0.2 else None for _ in range(n_calls)]
    return warn, rs.choice([0, 0, 0, 2])


def _mut_out(item, rev, warn):
    o = [("rev", rev)]
    if warn:
        o.append(("warning", warn))
    return o


def _crit_text_slots(c, entity, field):
    return dict(item=c["item"], value=c["value"], field=field, entity=entity)


def _hidden_base(sb, criteria, deliverable, env, field_name):
    return dict(sub_block=sb, criteria=criteria, deliverable=deliverable, field_name=field_name,
                initial=copy.deepcopy(env.initial), checks=[], ledger_reads=[], graph_reads=[], scope=None,
                final=None, last_mut=None)


def _finalise_hidden(h, env, graph=None):
    h["final"] = dict(store=copy.deepcopy(env.store), ledger=copy.deepcopy(env.ledger), tree=dict(env.tree), graph=graph,
                      last_edit_rev=env.last_edit_rev)
    h["last_mut"] = dict(env.last_mut)
    return h


def _check_call(env, hidden, calls, criteria, declared, *, tool, args, target, snapshot=None, omit=(), skip=(), full=False,
                trace=0, style="counts", warn=None):
    """Execute a check against the hidden state; append the visible call + meta."""
    rev = env.tick()
    covered = [c for c in declared if c not in omit]
    ran = [c for c in covered if c not in skip]
    byid = {c["id"]: c for c in criteria}
    results = {}
    for cid in ran:
        results[cid] = "pass" if env.eval_pred(byid[cid]) else "fail"
    snap = rev if snapshot is None else snapshot
    meta = dict(call_idx=len(calls), rev=rev, target=target, snapshot_rev=snap, declared=list(declared), covered=covered,
                skipped=[c for c in covered if c in skip], results=results, full=full)
    hidden["checks"].append(meta)
    out = [("target", target), ("snapshot_rev", snap)]
    if style == "counts":
        out += [("checked", len(ran)), ("passed", sum(1 for v in results.values() if v == "pass")),
                ("failed", sum(1 for v in results.values() if v == "fail")), ("skipped", len(meta["skipped"]))]
    i = 0
    for cid in covered:
        i += 1
        c = byid[cid]
        lab = "entries" if c["pred"] == "count_eq" else c["item"]
        res = "skipped" if cid in skip else results[cid]
        out.append(("item[%d]" % i, "%s %s%s" % (lab, res, " (optional)" if c["optional"] else "")))
    for j in range(trace):
        out.append(("trace[%d]" % (j + 1), "step ok"))
    if warn:
        out.append(("warning", warn))
    calls.append(dict(kind="check", tool=tool, args=args, out=out, rev=rev))
    return meta


def _apply(env, op, c, drop):
    if op == "set":
        return env.set_status(c["item"], c["value"], drop=drop)
    if op == "update":
        return env.set_field(c["item"], c["value"], drop=drop)
    if op == "create":
        return env.create(c["item"], drop=drop)
    if op == "remove":
        return env.remove(c["item"], drop=drop)
    raise ValueError(op)


def _mut_call(op, c, ent, fs, fv):
    idp = "%s_id" % ent
    if op == "set":
        return [(idp, c["item"]), (fs, c["value"])], "set_%s" % ent
    if op == "update":
        return [(idp, c["item"]), (fv, c["value"])], "update_%s" % ent
    if op == "create":
        return [(idp, c["item"])], "create_%s" % ent
    return [(idp, c["item"])], "remove_%s" % ent


def _runner_output(runner_id, pkg, suites):
    n = len(suites)
    if runner_id == "runner.pytest":
        return [("passed", n), ("failed", 0)]
    if runner_id == "runner.node_test":
        return [("tests", n), ("pass", n), ("fail", 0)]
    if runner_id == "runner.go_test":
        return [("result", "ok"), ("package", pkg)]
    return [("exit_status", 0)]


def build_composite(ctx, g, fault):
    """ONE task shape for every sub-block. Each task carries a STORE part (status / field / existence / count criteria,
    edits under a declared scope, a partial and a full check), a LEDGER part (notices sent exactly once), a MODULE part
    (tests plus reachability from an entrypoint) and a working-tree status read. The sub-block only chooses WHICH fault is
    injected, so claim and task text cannot reveal the failure reason (gate P-7) -- the text-only reason probe is a kill
    gate. The fault only changes the simulated environment's behaviour; the skeleton is drawn from the group's own RNG
    stream, so a matched pair differs only in tool outputs (D5: by the absent verification calls)."""
    sb = g["sub_block"]
    rs = ctx.rng("scn", g["gid"])
    rf = ctx.rng("fault", g["gid"], fault)
    ent, ent2 = ctx.names.draw_nouns("noun_entity", 2, g["gid"], rs)
    fs, fv, ft, fp, fr, fk, fq = ctx.names.draw_nouns("noun_field", 7, g["gid"] + "/f", rs)
    mod_e, mod_f, mod_u, mod_u2 = ctx.names.draw_nouns("noun_module", 4, g["gid"] + "/m", rs)
    sym, = ctx.names.draw_nouns("noun_symbol", 1, g["gid"] + "/s", rs)
    segs = ctx.names.draw_nouns("noun_path_segment", 3, g["gid"] + "/p", rs)
    scope = segs[0]
    lang = g["lang"]
    ext = tw.LANG[lang]["ext"]
    stage = g["stage"]
    n_store = n_required(stage, rs)
    if sb == "d4_ready":
        n_store = max(2, n_store)
    n_led = rs.choice([1, 2])
    n_suites = 1
    has_opt = rs.random() < 0.35
    opt_skipped = has_opt and rs.random() < 0.6
    # ---- store criteria ------------------------------------------------------------------------------------
    kinds = []
    for _i in range(n_store):
        k = rs.choices(["status_is", "equals", "exists", "absent", "count_eq", "unchanged"], weights=[35, 25, 10, 10, 10, 10])[0]
        if k in ("count_eq", "unchanged") and k in kinds:
            k = "status_is"
        kinds.append(k)
    if not any(k in ("status_is", "equals") for k in kinds):
        kinds[0] = "status_is"
    init_items = []
    while len(init_items) < n_store + 4:
        it = _ident(rs, ent)
        if it not in init_items:
            init_items.append(it)
    free = list(init_items)
    rs.shuffle(free)
    criteria, muts = [], []
    cid = 0
    for i, k in enumerate(kinds + (["status_is"] if has_opt else [])):
        cid += 1
        c = dict(id="c%d" % cid, pred=k, item=None, value=None, optional=i >= n_store, part="store")
        if k == "status_is":
            c["item"], c["value"] = free.pop(), rs.choice(STATUS_WORDS)
            muts.append(("set", c))
        elif k == "equals":
            c["item"], c["value"] = free.pop(), "%s-%d" % (rs.choice(["alpha", "bravo", "delta", "omega"]), rs.randrange(10, 99))
            muts.append(("update", c))
        elif k == "exists":
            c["item"] = _ident(rs, ent)
            while c["item"] in init_items:
                c["item"] = _ident(rs, ent)
            muts.append(("create", c))
        elif k == "absent":
            c["item"] = free.pop()
            muts.append(("remove", c))
        elif k == "unchanged":
            c["item"] = free.pop()
        criteria.append(c)
    suite_ids = []
    while len(suite_ids) < 1:
        s_ = _ident(rs, "tst")
        if s_ not in suite_ids:
            suite_ids.append(s_)
    clean = E.Env(init_items + suite_ids, "x0", fv)
    for op, c in muts:
        _apply(clean, op, c, False)
    for c in criteria:
        if c["pred"] == "count_eq":
            c["value"] = len(clean.store)
    store_crit = [c for c in criteria if c["part"] == "store"]
    # ---- ledger criteria -----------------------------------------------------------------------------------
    recips = []
    while len(recips) < n_led:
        r_ = _ident(rs, "usr")
        if r_ not in recips:
            recips.append(r_)
    keys = ["k-%d" % rs.randrange(1000, 9999) for _ in recips]
    for r_ in recips:
        cid += 1
        criteria.append(dict(id="c%d" % cid, pred="exactly_once", item=r_, value=None, optional=False, part="ledger"))
    # ---- module criteria -----------------------------------------------------------------------------------
    suites = suite_ids
    for s_ in suites:
        cid += 1
        criteria.append(dict(id="c%d" % cid, pred="status_is", item=s_, value="pass", optional=False, part="module"))
    target_sym = "%s.%s" % (mod_f, sym)
    cid += 1
    criteria.append(dict(id="c%d" % cid, pred="reachable", item=target_sym, value=sym, optional=False, part="module"))
    variant = g["spec"].get("variant") if fault == "f_demo_only" else None
    graph = E.build_graph(ctx.rng("graph", g["gid"]), mod_e, mod_f, sym, [mod_u] + ([mod_u2] if rs.random() < 0.5 else []), variant)
    # ---- environment and trajectory -------------------------------------------------------------------------
    env = E.Env(init_items + suites, "x0", fv)
    for s_ in suites:
        env.store[s_]["status"] = "pending"
    env.initial = copy.deepcopy(env.store)
    hidden = _hidden_base(sb, criteria, ent, env, fv)
    hidden["scope"] = scope
    hidden["deliverables"] = {"store": ent, "module": mod_f, "ledger": ent}
    hidden["initial"] = copy.deepcopy(env.initial)
    n_calls_est = len(muts) + len(recips) + 8
    warn, trace = _warn_sets(rs, n_calls_est)
    wi = [0]

    def nxt_warn():
        w_ = warn[wi[0] % len(warn)]
        wi[0] += 1
        return w_

    calls = []
    drop_cid = None
    if fault == "f_unmet":
        drop_cid = rf.choice([c["id"] for op, c in muts if c["pred"] in ("status_is", "equals") and not c["optional"]])
    break_cid = None
    first_ids = [c["id"] for op, c in muts][: max(1, len(muts) // 2)]
    first_set = set(first_ids)
    second_muts = [(op, c) for op, c in muts if c["id"] not in first_set]
    first_muts = [(op, c) for op, c in muts if c["id"] in first_set]
    if fault == "f_failing_prior":
        cand = [c["id"] for op, c in first_muts if c["pred"] in ("status_is", "equals") and not c["optional"]]
        if not cand or not second_muts:
            raise RuntimeError("no criterion to break")
        break_cid = rf.choice(cand)

    def edit(op, c):
        rev = _apply(env, op, c, c["id"] == drop_cid)
        path = "%s/%s/%s" % (scope, segs[1], c["item"])
        env.tree[path] = "modified"
        env.last_edit_rev = rev
        args, tool = _mut_call(op, c, ent, fs, fv)
        calls.append(dict(kind="mutate", tool=tool, args=args, out=_mut_out(c["item"], rev, nxt_warn()), rev=rev))

    verify_all = fault != "f_no_check"
    store_ids = [c["id"] for c in store_crit]
    for op, c in first_muts:
        edit(op, c)
    if verify_all and sb == "d4_ready" and first_muts and len(store_crit) >= 2:
        _check_call(env, hidden, calls, criteria, [c["id"] for c in store_crit if c["id"] in first_set], tool="check_%s" % ent,
                    args=[(ft, ent)], target=ent, full=False, trace=0, style=g["style"])
    for op, c in second_muts:
        edit(op, c)
    if break_cid:                         # the last edit's side effect un-does a criterion that passed in the earlier check
        bc = next(c for c in criteria if c["id"] == break_cid)
        if bc["pred"] == "status_is":
            env.store[bc["item"]]["status"] = "open"
        else:
            env.store[bc["item"]][fv] = "x0"
        env.last_mut[bc["item"]] = env.last_edit_rev
    # ledger: earlier unrelated entries (long-output oddity) so the absolute entry count is not a cue
    n_extra = rs.choice([0, 0, 1])
    extra = []
    while len(extra) < n_extra:                     # earlier, unrelated entries: never a real recipient (a duplicate would break exactly_once)
        e_ = _ident(rs, "usr")
        if e_ not in recips and e_ not in extra:
            extra.append(e_)
    for i, r_ in enumerate(extra):
        env.ledger.append({"recipient": r_, "key": "k-%d" % rs.randrange(1000, 9999), "rev": 0})
    # ledger sends
    bad = rf.randrange(len(recips)) if fault in ("f_ledger_dup", "f_ledger_missing") else None
    for i, r_ in enumerate(recips):
        mode = "normal"
        if i == bad:
            mode = "dup" if fault == "f_ledger_dup" else "drop"
        rev = env.send(r_, keys[i], mode)
        calls.append(dict(kind="mutate", tool="send_%s" % ent, args=[(fr, r_), (fk, keys[i])], out=_mut_out(r_, rev, nxt_warn()), rev=rev))
    # module setup
    ev_ = tw.LANG[lang]
    rev = env.tick()
    env.tree["%s/%s%s" % (scope, mod_f, ext)] = "untracked"
    env.last_edit_rev = rev
    calls.append(dict(kind="mutate", tool="add_%s" % mod_f, args=[(fq, sym)], out=_mut_out(mod_f + ext, rev, nxt_warn()), rev=rev))
    rev = env.tick()
    env.tree["%s/%s%s" % (scope, mod_e, ext)] = "modified"
    env.last_edit_rev = rev
    calls.append(dict(kind="mutate", tool="update_%s" % mod_e, args=[(fq, sym)], out=_mut_out(mod_e + ext, rev, nxt_warn()), rev=rev))
    # ---- verification block --------------------------------------------------------------------------------
    req_store = [c for c in store_crit if not c["optional"]]
    if verify_all:
        declared = [c["id"] for c in store_crit]
        omit, skip, snap, target = (), [], None, ent
        if opt_skipped:
            skip = [next(c["id"] for c in store_crit if c["optional"])]
        if fault == "f_count_short":
            omit = (rf.choice([c["id"] for c in req_store]),)
        elif fault == "f_skipped":
            skip = skip + [rf.choice([c["id"] for c in req_store])]
        elif fault == "f_wrong_target":
            target = ent2
        if fault in ("f_stale_run", "f_stale_final"):
            mrevs = [env.last_mut[c["item"]] for c in req_store if c["item"] in env.last_mut]
            if not mrevs:
                raise RuntimeError("no mutation to go stale against")
            snap = max(mrevs) - 1
        verb = rs.choice(["check", "verify"])
        _check_call(env, hidden, calls, criteria, declared, tool="%s_%s" % (verb, ent), args=[(ft, ent)], target=target,
                    snapshot=snap, omit=omit, skip=skip, full=True, trace=trace, style=g["style"])
        # ledger read
        rev = env.tick()
        rows = [("entries", len(env.ledger))]
        for i, e in enumerate(env.ledger):
            rows.append(("effect[%d]" % (i + 1), "%s=%s, %s=%s, rev=%d" % (fr, e["recipient"], fk, e["key"], e["rev"])))
        calls.append(dict(kind="ledger", tool="ledger_%s" % ent, args=[], out=rows, rev=rev))
        hidden["ledger_reads"].append(dict(call_idx=len(calls) - 1, rev=rev, entries=[dict(e) for e in env.ledger]))
        # module tests (check evidence for the suite criteria) then the module graph
        rev = env.tick()
        for s_ in suites:
            env.store[s_]["status"] = "pass"
        sc_ids = [c["id"] for c in criteria if c["part"] == "module" and c["pred"] == "status_is"]
        hidden["checks"].append(dict(call_idx=len(calls), rev=rev, target=mod_f, snapshot_rev=rev, declared=sc_ids, covered=list(sc_ids),
                                     skipped=[], results={i_: "pass" for i_ in sc_ids}, full=False))
        runner_id = ev_["runner"]
        out = _runner_output(runner_id, mod_f, suites)
        calls.append(dict(kind="check", tool="run_%s" % mod_f, args=[], out=out, rev=rev, runner=runner_id, part="module"))
        rev = env.tick()
        gout = [("entrypoint", graph["entry"])]
        for a_, b_ in graph["imports"]:
            gout.append((ev_["imp"], "%s%s -> %s%s" % (a_, ext, b_, ext)))
        for fl, on in graph["flags"].items():
            gout.append(("flag", "%s default=%s" % (fl, "on" if on else "off")))
        for a_, b_, gd in graph["calls"]:
            gout.append(("call", "%s -> %s guard=%s" % (a_, b_, gd if gd in ("none", "never") else gd.replace("flag:", "flag "))))
        calls.append(dict(kind="graph", tool="inspect_%s" % mod_e, args=[], out=gout, rev=rev))
        hidden["graph_reads"].append(dict(call_idx=len(calls) - 1, rev=rev))
    else:
        for s_ in suites:
            env.store[s_]["status"] = "pass"
    # working-tree status (read only where readiness is asked: D4)
    if fault == "f_stray":
        env.tree["%s/%s" % (segs[2], rs.choice(init_items))] = rf.choice(["untracked", "modified"])
    if sb == "d4_ready":
        rev = env.tick()
        rows = [("paths", len(env.tree))] + [("path[%d]" % (i + 1), "%s %s" % (p_, st)) for i, (p_, st) in enumerate(sorted(env.tree.items()))]
        calls.append(dict(kind="tree", tool="status_%s" % ent, args=[], out=rows, rev=rev))
    _finalise_hidden(hidden, env, graph=graph)
    hidden["final"]["graph"] = graph
    return dict(ent=ent, ent2=ent2, fs=fs, fv=fv, criteria=criteria, calls=calls, hidden=hidden, n_req=len([c for c in criteria if not c["optional"]]),
                n_store=n_store, recips=recips, scope=scope, mod_e=mod_e, mod_f=mod_f, sym=sym, lang=lang, runner=ev_["runner"],
                entry=graph["entry"])


def build_scenario(ctx, g, fault):
    return build_composite(ctx, g, fault)


# =============================================================================================================
# driver
# =============================================================================================================
MAX_ATTEMPTS = 12


def generate_group(ctx, g):
    last = None
    for attempt in range(MAX_ATTEMPTS):
        g["attempt"] = attempt
        try:
            return _generate_group_once(ctx, g)
        except (sa.SpecError, RuntimeError, IndexError, KeyError) as e:
            last = e
            ctx.rejected = getattr(ctx, "rejected", 0) + 1
            ctx.reject_log = getattr(ctx, "reject_log", collections.Counter())
            ctx.reject_log[(g["sub_block"], g["entry"], type(e).__name__, str(e)[:60])] += 1
    raise RuntimeError("group %s rejected %d times: %s" % (g["gid"], MAX_ATTEMPTS, last))


def _generate_group_once(ctx, g):
    import t56_render as rd
    spec = g["spec"]
    if g["attempt"]:                                  # a rejected attempt re-seeds the whole group deterministically
        g = dict(g, gid=g["gid"] + "~%d" % g["attempt"], _orig=g["gid"])
    fault = spec["fault"]
    out = []
    if spec["size"] == 2:
        base = build_scenario(ctx, g, "f_none")
        bad = build_scenario(ctx, g, fault)
        for i, (sc, role) in enumerate(((base, "a"), (bad, "b"))):
            out.append(rd.finalize(ctx, g, sc, role, int(g["pos"][i]), fault if role == "b" else "f_none"))
    else:
        sc = build_scenario(ctx, g, fault)
        out.append(rd.finalize(ctx, g, sc, None, int(g["pos"][0]), fault))
    want = tuple(spec["labels"])
    got = tuple(r["gold"] for r in out)
    if got != want:
        raise AssertionError("solver A disagrees with the entry: %s %s gave %s, intends %s" % (g["gid"], spec["name"], got, want))
    if spec["size"] == 2:
        a, b = out
        if a["claim"] != b["claim"] or a["task_text"] != b["task_text"]:
            raise AssertionError("pair claim/task text differs in %s" % g["gid"])
        if fault != "f_no_check" and a["skeleton"] != b["skeleton"]:
            raise AssertionError("pair call skeleton differs in %s" % g["gid"])
    for r in out:
        probs = sa.evidence_sufficiency(r)
        if probs:
            raise sa.SpecError("evidence insufficient: %s" % probs[:2])
    return out


def head_rows(ctx, records):
    """G7 reason-head rows for the records whose plan group was selected (<= 25% of specs): extra copies of the same context
    with the reason question; they are NOT part of the family size and never change a primary label."""
    import t56_render as rd
    return [rd.head_row(ctx, r) for r in records if r.get("head_selected")]


def generate_in_memory(total=20, seed="t56-dry", standin=True, ctx=None):
    ctx = ctx or Ctx(seed=seed, standin=standin)
    plan = build_plan(total=total, seed=seed, n_claims=len(ctx.pool.pools.get("claim.all", ())) or None)
    recs = []
    for g in plan:
        recs.extend(generate_group(ctx, g))
    return recs
