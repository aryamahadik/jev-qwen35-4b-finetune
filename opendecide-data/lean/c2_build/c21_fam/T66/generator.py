"""T66 generator: plan (MERGE / SEMVER / MSG cells, oversampled by 15%) and group generation (spec -> records). No rows are written; every execution goes
through `ctx.executor` (SimExecutor = PyEval in the dry run; the od-sbx1 executor in production). The MSG-REAL slice (CommitPackFT) is not built here."""
import copy
import re

from LP_COMMON import plan as plan_mod
from LP_COMMON import sandbox_iface as S
from LP_COMMON import util, wording
from LP_COMMON.plan import Ctx as BaseCtx

from . import config as C
from . import merge as MG, merge_spec as MS, msg_pool as MP, msg_spec as MSG, rows as ROWS, semver as SV, semver_spec as SS


def form_slots():
    """Slots of every form of a STAND-IN (test) pool. The production MSG forms follow msg_form_rule (style I carries {fn}, style N carries no slot)."""
    slots = dict(C.FORM_SLOTS)
    for f in MSG.FORMS_MSG:
        slots[f] = list(MSG.MSG_SLOTS)
    return slots


TRIV_CHARS = 3          # CH-trivial NO message vs the true message: characters within +-3 (Opus ruling Q8 R3)
MSG_MIN_WORDINGS = 10   # per MSG form (one style of one kind); a dev / dev2 half of the production pool has 14


def msg_form_rule(form):
    """-> (allowed slots, must carry {fn}, must carry no slot) of a MSG change form (T66-M-<CH>-<I|N>, T66-M-TRIV-<t>). Style N is identifier-free: its only slots are numbers."""
    if form.startswith("T66-M-TRIV-"):
        return set(MSG.KIND_SLOTS[form.split("-")[-1]]), False, False
    ch, style = form[len("T66-M-"):].rsplit("-", 1)
    if style == "N":
        return set(MSG.KIND_SLOTS[ch]) & set(MSG.NUMERIC_SLOTS), False, False            # identifier-free: only numbers may be filled in
    return set(MSG.KIND_SLOTS[ch]), True, False


def pool_problems(pool):
    """Problems of a T66 wording pool ([] = usable). The question forms follow the shared slot / count / duplicate rules (`wording.validate`). The MSG change forms are COMMIT
    MESSAGES: each carries its own change class (verb class + object), so (a) no wording text may be shared by two change forms (a text shared by CH-1 and CH-5 describes
    neither), (b) a message is not a question (the pool must not reuse the question frames of MERGE / SEMVER / MSG as messages), (c) style I wordings carry {fn}, style N
    wordings carry no identifier slot (numbers only), and only the slots of their kind are used. Without this a pool of question frames passes every other check and the MSG label (own vs swapped vs
    trivial message) becomes unlearnable noise. (The kind-word and similarity lint of the production pool file is lint_msg_pool.py.)"""
    slots = {f: v for f, v in form_slots().items() if f not in MSG.FORMS_MSG}
    bad = list(wording.validate(pool, slots))
    # SEMVER options are BREAKING / SAFE: a frame that opens as a yes/no question does not ask for the class
    bad += wording.frame_problems(pool, "T66-Q-SEMVER", deny_start=r"(?:does|do|is|are|would|can|should|did)\b")
    owners = {}
    for f in MSG.FORMS_MSG:
        ws = pool.get("forms", {}).get(f)
        if not ws:
            bad.append("missing MSG form %s" % f)
            continue
        if len(ws) < MSG_MIN_WORDINGS:
            bad.append("MSG form %s has %d wordings (< %d)" % (f, len(ws), MSG_MIN_WORDINGS))
        if len({w["id"] for w in ws}) != len(ws) or len({w["text"] for w in ws}) != len(ws):
            bad.append("MSG form %s has duplicate ids or texts" % f)
        allowed, need_fn, no_slot = msg_form_rule(f)
        for w in ws:
            used = set(wording.SLOT.findall(w["text"]))
            if used - allowed:
                bad.append("MSG form %s wording %s uses slots %s that are not slots of its kind" % (f, w["id"], sorted(used - allowed)))
            if need_fn and "fn" not in used:
                bad.append("MSG form %s wording %s misses {fn}" % (f, w["id"]))
            if no_slot and used:
                bad.append("MSG form %s wording %s must be identifier-free but uses %s" % (f, w["id"], sorted(used)))
            owners.setdefault(w["text"], set()).add(f)
    shared = sum(1 for fs in owners.values() if len(fs) > 1)
    if shared:
        bad.append("%d message wordings are shared by more than one change form (a message must carry its own change class)" % shared)
    qs = sum(1 for t in owners if "?" in t)
    if qs:
        bad.append("%d message wordings are questions (a commit message is a statement)" % qs)
    return bad


class Ctx(BaseCtx):
    """Generation context. MSG messages come from the production commit-message pool (pools/msg_messages.json, msg_pool.py): `msg_split` picks the half of its templates
    ("dev", "dev2", "holdout" or "all"); `msg_pool` is a pool path or dict (default: the shipped file). The message forms of the wording pool are REPLACED by that half when
    `msg_split` or `msg_pool` is given, and in a production context that loads its wording pool from `pool_path` (split "all" then); a wording pool passed as `pool=` without
    either argument is used as given (and refused in production if its message forms are not commit messages)."""

    def __init__(self, seed, standin=False, pool_path=None, pool=None, executor=None, deny_check=None, msg_split=None, msg_pool=None):
        if pool is None and pool_path is None and standin:
            pool = wording.make_test_pool(form_slots())
        from_path = pool is None and pool_path is not None
        super().__init__(seed, standin=standin, pool_path=pool_path, pool=pool, deny_check=deny_check)
        if self.pool is None:
            raise wording.PoolError("no wording pool")
        if msg_split is not None and msg_split not in MP.SPLITS:
            raise wording.PoolError("msg_split must be one of %s" % (MP.SPLITS,))
        self.msg_split = msg_split
        if msg_pool is not None or msg_split is not None or (from_path and not standin):
            doc = msg_pool if isinstance(msg_pool, dict) else MP.load(msg_pool)
            self.msg_split = msg_split or "all"
            self.pool = MP.wording_pool(self.pool, doc, self.msg_split)
        if executor is None and standin:
            executor = S.SimExecutor()
        if executor is None:
            raise ValueError("an executor is required (the od-sbx1 two-phase driver, or SimExecutor for tests)")
        if not standin:
            wording.require_real(self.pool)
            problems = pool_problems(self.pool)
            if problems:
                raise wording.PoolError("the T66 wording pool is not usable: " + "; ".join(problems[:4]))
            if isinstance(executor, S.SimExecutor):
                raise ValueError("SimExecutor cannot build rows (it predicts; it does not witness)")
        self.executor = executor
        self.picker = wording.Picker(self.pool, util.rng_for("T66-picker", seed))


# ---- plan ---------------------------------------------------------------------------------------------------------------------------------
def _cycle(items, n, rng):
    out = [items[i % len(items)] for i in range(n)]
    rng.shuffle(out)
    return out


TRIV_GROUP_SHARE = 0.27     # share of MSG groups whose NO rows are CH-trivial (>= 25% of NO rows, T66-B3); the type is fixed by quota, not drawn
SAME_FN_SHARE = 0.85        # share of the swap groups built on two kinds that change the same function (the M-OVL hard stratum needs >= 30% of the MSG rows)


def _kind_pair(rng, other_function=False):
    kinds = list(MSG.CH_REALISED)
    while True:
        chs = []
        while len(chs) < 2:
            c = rng.choice(kinds)
            if c not in chs and rng.random() < MSG.KIND_WEIGHT.get(c, 1.0):
                chs.append(c)
        if frozenset(chs) in MSG.CONFUSABLE_PAIRS or (other_function and MSG.BLOCK_OF[chs[0]] == MSG.BLOCK_OF[chs[1]]):
            continue
        return chs


def _same_fn_pair(rng):
    """(kinds, styles) of a same-function swap group: a weighted pair, one spec style N and the other style I (CH-8 is always the N one)."""
    pairs = sorted(MSG.SAME_FN_WEIGHT)
    r, acc = rng.random() * sum(MSG.SAME_FN_WEIGHT.values()), 0.0
    for pr in pairs:
        acc += MSG.SAME_FN_WEIGHT[pr]
        if r <= acc:
            break
    chs = list(pr)
    rng.shuffle(chs)
    styles = ["N", "I"] if (chs[0] in MSG.ALWAYS_N or (chs[1] not in MSG.ALWAYS_N and rng.random() < 0.5)) else ["I", "N"]
    return chs, styles


def build_plan(total=C.GENERATED_ROWS, seed=0, oversample=True):
    scale = total / float(C.GENERATED_ROWS) * (plan_mod.OVERSAMPLE if oversample else 1.0)
    rng = util.rng_for("T66-plan", seed)
    groups = []
    k = 0

    def add(head, size, cell):
        nonlocal k
        k += 1
        groups.append({"gid": "T66-%s-%04d" % (head, k), "seed": "%s-%d" % (head, k), "size": size, "head": head, "cell": cell})

    # ---- MERGE (300 rows: 90 pairs + 60 YES singles + 60 NO singles)
    n_pairs, n_ys, n_ns = [int(round(x * scale)) for x in (92, 58, 58)]
    no_pool = ["RK1"] * 15 + ["RK2"] * 15 + ["RK3"] * 22 + ["RK4"] * 23 + ["RK7"] * 60 + ["RK8"] * 15
    no_all = _cycle(no_pool, n_pairs + n_ns, rng)
    yes_all = _cycle(["RK5"] * 55 + ["RK6"] * 45, n_pairs + n_ys, rng)
    cfs = _cycle(list(MG.CF_IDS), n_pairs + n_ys + n_ns, rng)
    ci = 0
    for i in range(n_pairs):
        no_rk = no_all[i]
        if no_rk in ("RK1", "RK2", "RK8"):
            no_rk = ("RK3", "RK4", "RK7")[i % 3]                 # a pair's NO partner differs from the YES one in the resolution kind only
        add("MERGE", 2, {"cf": cfs[ci], "rks": [yes_all[i], no_rk]})
        ci += 1
    for i in range(n_ys):
        add("MERGE", 1, {"cf": cfs[ci], "rks": [yes_all[n_pairs + i]]})
        ci += 1
    for i in range(n_ns):
        add("MERGE", 1, {"cf": cfs[ci], "rks": [no_all[n_pairs + i]]})
        ci += 1
    # ---- SEMVER (300 rows: 60 pairs, 90 BREAKING singles, 90 SAFE singles)
    pair_kinds = _cycle(["SV-C1", "SV-C2", "SV-C3", "SV-C6", "SV-C7", "SV-C8", "SV-C9", "SV-C10"], int(round(62 * scale)), rng)
    for kind in pair_kinds:
        add("SEMVER", 2, {"sv": kind, "variants": ["break", "safe"], "bump": rng.random() < 0.5})
    for kind in _cycle(["SV-C1", "SV-C2", "SV-C3", "SV-C5", "SV-C6", "SV-C7", "SV-C8", "SV-C9", "SV-C10"], int(round(88 * scale)), rng):
        add("SEMVER", 1, {"sv": kind, "variants": ["break"], "bump": rng.random() < 0.5})
    for kind in _cycle(["SV-C4", "SV-C11", "SV-C12"], int(round(88 * scale)), rng):
        add("SEMVER", 1, {"sv": kind, "variants": ["safe"], "bump": rng.random() < 0.5})
    # ---- MSG (100 change specs in groups of 2 = 200 rows): <= 4 rows per base module per head (T66-K13), so a group is two change specs on one base module. A group is either a
    # SWAP group (each spec's NO message is the partner's true message verbatim, Opus ruling Q8 R1 / R2) or a CH-TRIVIAL group (each NO message describes one of the spec's own trivial
    # hunks and is matched to its true message, R3): with two specs a derangement over the swap diffs needs both of them, so the type is per group. The hard stratum (R4) is a swap group on
    # two kinds that change the SAME function, styles (N, I): the partner's verbatim message names that function, which is in this diff. Every other group is style N on both specs: a
    # style-I message whose identifiers are NOT in the other diff (or a CH-trivial message with fewer identifiers than the true one) would put "YES shares more identifiers" on one side only,
    # and the K7 overlap probe would read it (dry run: AUC 0.59); with the hard stratum balanced by its mirror pair (I, N) and the rest identifier-free the probe stays at chance.
    n_groups = int(round(50 * scale))
    n_triv = int(round(n_groups * TRIV_GROUP_SHARE))
    types = ["trivial"] * n_triv + ["swap"] * (n_groups - n_triv)
    rng.shuffle(types)
    same_left = int(round((n_groups - n_triv) * SAME_FN_SHARE))
    for typ in types:
        if typ == "trivial":
            chs = _kind_pair(rng)
            add("MSG", 4, {"type": "trivial", "chs": chs, "styles": ["N", "N"], "trivial": [rng.choice((1, 1, 2)) for _ in chs]})
            continue
        if same_left > 0:
            same_left -= 1
            chs, styles = _same_fn_pair(rng)
        else:
            chs = _kind_pair(rng, other_function=True)
            styles = ["N", "N"]
        add("MSG", 4, {"type": "swap", "chs": chs, "styles": styles, "trivial": [rng.choice((0, 1, 1, 2, 2)) for _ in chs]})
    rng.shuffle(groups)
    return groups


# ---- generation --------------------------------------------------------------------------------------------------------------------------
def _retry(fn, n, ctx, g, exc):
    last = None
    for t in range(n):
        try:
            return fn(dict(g, seed="%s#t%d" % (g["seed"], t)))
        except exc as e:
            last = e
    raise last


def _gen_merge(ctx, g):
    cell = g["cell"]
    specs = _retry(lambda gg: MS.build_group(ctx, gg, cell), 6, ctx, g, MG.Reject)
    out = []
    pair = len(specs) == 2
    for i, s in enumerate(specs):
        s["module_group"] = g["gid"]
        out.append(ROWS.build_record(ctx, g, s, i, "%s:%s" % (s["cf"], s["rk"]), pair_id=g["gid"] if pair else None,
                                     twin_of=("%s-%s" % (g["gid"], "ab"[1 - i])) if pair else None, extra_meta={"cf": s["cf"], "rk": s["rk"]}))
    return out


def _gen_semver(ctx, g):
    cell = g["cell"]
    specs = _retry(lambda gg: SS.build_group(ctx, gg, cell), 8, ctx, g, SV.Reject)
    pair = len(specs) == 2
    out = []
    for i, s in enumerate(specs):
        s["module_group"] = g["gid"]
        out.append(ROWS.build_record(ctx, g, s, i, "%s:%s" % (s["sv"], s["variant"]), pair_id=g["gid"] if pair else None,
                                     twin_of=("%s-%s" % (g["gid"], "ab"[1 - i])) if pair else None, extra_meta={"sv": s["sv"], "variant": s["variant"], "diff_lines": s["diff_lines"]}))
    return out


def draw(ctx, form, slots, accept=None, tries=60):
    """Least-used-first wording draw (the shared Picker rule) that skips wordings whose RENDERED text `accept` refuses. -> (wording id, text) or None."""
    pk = ctx.picker
    ws = pk.pool["forms"][form]
    use = pk.use.setdefault(form, {w["id"]: 0 for w in ws})
    for w in sorted(ws, key=lambda w: (use[w["id"]], pk.rng.random()))[:tries]:
        text = w["text"].format(**slots)
        if accept is None or accept(text):
            use[w["id"]] += 1
            return w["id"], text
    return None


def msg_text(ctx, spec, accept=None):
    """(wording id, message text): the change spec's own (true) message."""
    return draw(ctx, MSG.form_of(spec["ch"], spec["style"]), spec["slots"], accept)


def _wid_style(wid):
    """'I' / 'N' for a pool wording id like CH-2-N-07 or fmt-I-03; None for ids without a style (stand-in test pools)."""
    parts = wid.split("-")
    return parts[-2] if len(parts) >= 3 and parts[-2] in ("I", "N") and parts[-1].isdigit() else None


def trivial_pick(ctx, spec, true_msg):
    """The CH-trivial NO message of `spec` (Opus ruling Q8 R3): it describes one of the spec's OWN trivial hunks and matches the spec's true message in rendered token count and style,
    with a character length within +-3. -> (wording id, text) or None (no wording fits: the group is regenerated, never an unmatched draw)."""
    wid, text = true_msg
    nt, nc = len(text.split()), len(text)
    pk = ctx.picker
    cands = []
    for t, tfn in zip(spec["trivials"], spec["triv_fns"]):
        form = "T66-M-TRIV-%s" % t
        ws = pk.pool["forms"][form]
        use = pk.use.setdefault(form, {w["id"]: 0 for w in ws})
        slots = {"fn": tfn or spec["slots"]["fn"]}
        for w in ws:
            if _wid_style(w["id"]) not in (None, spec["style"]):
                continue
            r = w["text"].format(**slots)
            if len(r.split()) == nt and abs(len(r) - nc) <= TRIV_CHARS and MSG.jaccard(r, text) < 0.5:
                cands.append((use[w["id"]], pk.rng.random(), form, w["id"], r))
    if not cands:
        return None
    _u, _r, form, wid2, text2 = min(cands)
    pk.use[form][wid2] += 1
    return wid2, text2


def _names_in(slots, diff):
    """Do identifiers of a message (the function, parameter, token ... names it fills in) occur in `diff`?"""
    names = [v for k, v in slots.items() if isinstance(v, str) and k not in ("num_old", "num_new")]
    return any(re.search(r"\b%s\b" % re.escape(n), diff) for n in names)


def _msg_group(ctx, g):
    cell = g["cell"]
    specs = MSG.build_group(ctx, g, cell)
    own = []
    for s in specs:
        first = own[0][1] if own else None
        m = msg_text(ctx, s, lambda t, o=first: len(t.split()) >= 4 and (o is None or MSG.jaccard(t, o) < 0.5))        # R5: >= 4 tokens; the two true messages differ enough to swap
        if m is None:
            raise MSG.Reject("true message constraints")
        own.append(m)
    k = len(specs)
    no = []
    for i, s in enumerate(specs):
        if cell["type"] == "swap":
            j = (i + 1) % k                                               # derangement over the swap diffs: each true message is used exactly once as a NO message
            if specs[j]["verb"] == s["verb"] or MSG.jaccard(own[j][1], own[i][1]) >= 0.5:
                raise MSG.Reject("swap constraints")
            no.append((own[j][0], own[j][1], "swap", specs[j]))
        else:
            if not s["trivials"]:
                raise MSG.Reject("trivial group without a trivial hunk")
            tp = trivial_pick(ctx, s, own[i])
            if tp is None:
                raise MSG.Reject("no CH-trivial wording matches the true message")
            no.append((tp[0], tp[1], "trivial", None))
    order = sorted(range(k), key=lambda i: specs[i]["diff_size"])
    out, member = [], 0
    for i in order:
        s = specs[i]
        nwid, ntext, origin, partner = no[i]
        pid = "%s-p%d" % (g["gid"], i)
        base = dict(head="MSG", stem=s["stem"], diff=s["diff"], lang="python", module_group=g["gid"], ch=s["ch"], verb=s["verb"], trivials=s["trivials"],
                    diff_size=s["diff_size"], style=s["style"], witness=None, strength=None)
        yes = dict(base, message=own[i][1], label="YES", origin="own", message_wid=own[i][0])
        no_spec = dict(base, message=ntext, label="NO", origin=origin, message_wid=nwid)
        ovl = None
        if origin == "swap":
            if s["style"] == "N" and partner["style"] == "I" and _names_in(partner["slots"], s["diff"]):
                ovl = "high"                                              # M-OVL: the true message shares none, the swapped one names identifiers of this diff
            elif s["style"] == "I" and partner["style"] == "N":
                ovl = "low"
        mech = {"multi": "high" if (len(s["trivials"]) >= 2 and origin == "trivial") else ("low" if not s["trivials"] else None), "ovl": ovl}
        yes["mech"], no_spec["mech"] = dict(mech), dict(mech)
        a = ROWS.build_record(ctx, g, yes, member, "%s:own" % s["ch"], pair_id=pid, twin_of="%s-%s" % (g["gid"], "abcdefgh"[member + 1]), extra_meta={"ch": s["ch"]})
        b = ROWS.build_record(ctx, g, no_spec, member + 1, "%s:%s" % (s["ch"], origin), pair_id=pid, twin_of="%s-%s" % (g["gid"], "abcdefgh"[member]),
                              extra_meta={"ch": s["ch"], "no_kind": "CH-trivial" if origin == "trivial" else "swap"})
        b["manifest"]["own_message"] = own[i][1]
        out += [a, b]
        member += 2
    return out


def _gen_msg(ctx, g):
    saved = copy.deepcopy(ctx.picker.use)

    def attempt(gg):
        try:
            return _msg_group(ctx, gg)
        except MSG.Reject:
            ctx.picker.use.clear()                                       # a failed attempt leaves no trace in the least-used counters
            ctx.picker.use.update(copy.deepcopy(saved))
            raise
    out = _retry(attempt, 8, ctx, g, MSG.Reject)
    return out


def generate_group(ctx, g):
    return {"MERGE": _gen_merge, "SEMVER": _gen_semver, "MSG": _gen_msg}[g["head"]](ctx, g)
