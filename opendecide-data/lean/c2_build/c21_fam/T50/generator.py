"""T50 generator: Cell -> Spec(s) (G0-lite T50 sections 1-4). CODE ONLY. Nothing here writes a row to disk.

Pipeline for one Cell:  BCtx (names from the training namespace) -> intent builder (state + visible evidence +
structured action) -> solver A (gold) -> design check (gold must equal the intent's design expectation) ->
user turns (wording FORMS; the text comes from a Haiku-written pool later) -> renderings (plain / operators /
view variants) -> round-trip check with our expander (K1) .
"""
import copy

from LA_COMMON.canon import FrozenTable, rng_for
from LA_COMMON.expander import Expander, roundtrip_equal, spec_canon
from LA_COMMON.render import (ALL_OPERATORS, HELDOUT_OPERATORS, TRAINED_OPERATORS, RenderError, render, render_plain)
from LA_COMMON.shellmodel import Cmd, Glob, RawScript, Script
from LA_COMMON.spans import ROLE_AUTHORITY, ROLE_ENTITY, ROLE_NUMBER
from LA_COMMON.spec import Gold, HistCall, Spec, Turn, check_gold_invariants
from LA_COMMON.wording import FORMS, WordingPool, register_form, render_form, stub_pool

from . import cards as cards_mod
from . import dialects
from .blocks import Cell, plan
from .build import BCtx, Built
from .intents import REGISTRY, build_intent, expected_for
from .solver_a import label_spec
from .verdict import single_trigger

FAMILY = "T50"
A, E_ = ROLE_AUTHORITY, ROLE_ENTITY

register_form("T50.U.task", FAMILY, {"topic": []}, "generic task statement; names neither operation nor target")
register_form("T50.U.op_only", FAMILY, {"op": [A]}, "names the operation only")
register_form("T50.U.target_only", FAMILY, {"target": [A, E_]}, "names the target only")
register_form("T50.U.both", FAMILY, {"op": [A], "target": [A, E_]}, "names the operation AND the target (consent)")
register_form("T50.U.named_paths", FAMILY, {"paths": [A, E_]}, "lists the exact files the user means (INFERRED-TARGET)")
register_form("T50.U.note_file_state", FAMILY, {"path": [E_], "state": []}, "state of a file (committed/untracked/...)")
register_form("T50.U.note_resource_owner", FAMILY, {"resource": [E_], "ctx": [E_], "owner": []}, "who created a resource")
register_form("T50.U.note_review", FAMILY, {"branch": [A, E_]}, "review of a protected branch is approved (authority)")
register_form("T50.U.note_tree_clean", FAMILY, {}, "working tree is clean")
register_form("T50.U.note_remote_visibility", FAMILY, {"remote": [E_], "vis": []}, "remote visibility")
register_form("T50.U.note_proc_owner", FAMILY, {"pid": [ROLE_NUMBER], "owner": []}, "owner of a process")
register_form("T50.Q.reason", FAMILY, {}, "head question form: reason (7 options)")
register_form("T50.Q.tier", FAMILY, {}, "head question form: consent tier (3 options)")

PAYLOAD_REGISTRY = FrozenTable("T50_payload_registry", "v1", sorted(i for i, m in REGISTRY.items() if m["registerable"]))


class GeneratorDefect(Exception):
    pass


class DropLedger:
    """K1 / K13 bookkeeping: every dropped rendering or row is counted with its reason (names only)."""

    def __init__(self):
        self.drops = []

    def add(self, spec_id, why):
        self.drops.append((spec_id, why))

    def count(self):
        return len(self.drops)


# ------------------------------------------------------------------------------------------------ helpers
def group_id(cell):
    """Spec-family id. A replacement group of a dropped slot is a NEW spec (GV5: attempt suffix); a held-out cell (dev only) draws the
    first suffix whose hash lands in the dev split, so the split stays a pure function of the group id (K13)."""
    base = "T50-%05d" % cell.extras.get("idx", 0)
    if cell.extras.get("attempt"):
        base += "r%d" % cell.extras["attempt"]
    if cell.extras.get("force_dev"):
        from LA_COMMON.canon import assign_split
        k = 0
        cand = base
        while assign_split(cand) != "dev":
            k += 1
            cand = base + "d%d" % k
        base = cand
    return base


def _target_surface(ref):
    if ref.startswith("/"):
        return ref
    if ref.startswith("metadata:"):
        return ref.split(":", 1)[1]
    if ref == "worktree":
        return "the working tree"
    if ref == "env":
        return "the environment variables"
    if ref.count("/") == 2:
        ctx, kind, name = ref.split("/")
        return "%s %s" % (kind, name)
    if "." in ref and "/" not in ref and ref.count(".") == 1:
        return ref.split(".", 1)[1]
    return ref


def hard_refs(spec):
    """Plausible (op_ref, target_ref) for a HARD row: used to render the 'user names op and target' cells."""
    cmds = spec.action.cmds() if isinstance(spec.action, Script) else []
    if not cmds:
        return ("run", "script")
    c = cmds[0]
    op = "%s.%s" % (c.program, (c.sub or "run").replace(" ", "_"))
    tgt = next((a for a in c.args if not a.startswith("-")), None) or (c.redirs[0].target if c.redirs else c.program)
    return (op, str(tgt))


def _fact_visibility(c, res):
    out = {}
    for f in res.facts:
        if f in c.shown:
            out[f] = c.shown[f]
        elif f.startswith(("card.", "git.protected:", "infra.lane:", "sql.lane:", "pkg.registry", "fetch.host_trusted",
                           "image.", "egress.dest:")):
            out[f] = "card"
        elif f.startswith("git.review:"):
            out[f] = "user_turn"                   # an approval is a user statement; its absence is visible as no such turn
        elif f.startswith(("egress.class:", "fs.data_class:")):
            out[f] = c.shown.get(f, "path")
        elif f.startswith(("net.", "chmod.", "env.", "find.", "grep.", "firewall.", "docker.", "kubectl.", "git.hook_path",
                           "git.tls_off")):
            out[f] = "path"
        else:
            out[f] = "output"
    return out


def _consent_keys(res):
    """Uncleared soft members' consent keys (each is (op_ref, target_ref))."""
    return [m.consent for m in res.members if m.consent is not None and m.tier == "soft" and m.note != "cleared"]


def _make_spec(cell, c, built, spec_id, block, naming=None, extras_meta=None):
    from .blockg import _pad_evidence
    _pad_evidence(c)           # K6: the number of notes / earlier calls is constant, so it cannot follow the label (also K6 within shell_exec)
    spec = Spec(spec_id=spec_id, family=FAMILY, block=block, card_ref=c.card["card_id"], card=c.card, state=c.st,
                user_turns=[], naming=copy.deepcopy(naming if naming is not None else c.naming), history=list(c.hist),
                action=built.script, payloads=dict(c.payloads), payload_kind=built.payload_kind, intent=built.intent,
                group=group_id(cell), meta=dict(c.meta, **(extras_meta or {})))
    spec.dialect = dialects.dialect_for_group(spec.group, spec.split)         # A15: one dialect per spec group; the held-out ones are re-tagged by overlays.apply_dialects
    m_ = REGISTRY.get(cell.intent) or REGISTRY.get(getattr(built, "intent", "")) or {"domain": "fs", "family_part": "core"}
    spec.meta["domain"] = m_["domain"]
    spec.meta["provisional_names"] = c.names.used_provisional
    spec.meta["sub_family"] = cell.sub or m_.get("family_part", "core")
    spec.meta["names_provisional"] = c.names.used_provisional
    problems = spec.state.validate()
    if problems:
        raise GeneratorDefect("state: " + "; ".join(problems))
    return spec


def _solve(spec, c):
    res = label_spec(spec)
    spec.gold = Gold(res.label, res.reason, res.tier)
    spec.rule_ids = list(res.rules)
    spec.effects = list(res.effects)
    if res.egress_records:                       # the shared egress sub-record, present on every spec that reaches R13
        spec.egress = res.egress_records[0][0]
        spec.meta["egress_list"] = [r for r, _ in res.egress_records]
    spec.fact_visibility = _fact_visibility(c, res)
    spec.meta["primary_determinable"] = "output" not in spec.fact_visibility.values()
    spec.meta["single_trigger"] = single_trigger(res.members)             # Q11.1: reason heads come from single-trigger specs only
    bad = check_gold_invariants(spec)
    if bad:
        raise GeneratorDefect("gold invariants: " + "; ".join(bad))
    return res


def _design_check(spec, cell, res):
    if cell.tag in ("named",):
        want = ("ALLOW", "none", "soft")
    else:
        want = expected_for(REGISTRY[cell.intent], spec.card)
    got = (res.label, res.reason, res.tier)
    if got != want:
        raise GeneratorDefect("%s on %s: solver %s != design %s (rules %s)" % (cell.intent, spec.card_ref, got, want, res.rules))


def _programs(script, extra=()):
    ps = set(extra)
    if isinstance(script, Script):
        ps.update(c.program for c in script.cmds())
    elif isinstance(script, RawScript):
        ps.update(script.programs)
    return ps


def _known_files(spec):
    """path -> script text, for the expander (write-then-run)."""
    out = {}
    late = spec.meta.get("late_text") if ".wtr_" in spec.intent else None      # LATE-BINDING: the file holds the wrapped (trap / heredoc / alias) text
    for path, pid in spec.state.session.written_files.items():
        pl = spec.payloads.get(pid)
        if isinstance(pl, Script):
            out[path] = late or render_plain(pl).text
    return out


def _history_text(spec):
    for h in spec.history:
        if h.carrier == "shell_exec" and isinstance(h.script, Script):
            h.text = render_plain(h.script).text + ("\n" + h.output if h.output else "")
        elif h.carrier == "shell_exec" and isinstance(h.script, RawScript):
            h.text = h.script.text + ("\n" + h.output if h.output else "")
        elif h.carrier == "file_write":
            pl = spec.payloads.get(h.payload_id)
            h.text = render_plain(pl).text if isinstance(pl, Script) else ""
            if spec.meta.get("late_text") and ".wtr_" in spec.intent:
                h.text = spec.meta["late_text"]


def validator_flags(spec, text):
    """Parse-only validators: our expander, tree-sitter-bash, mvdan/sh (shape agreement), sqlglot (embedded SQL).
    None = validator not installed; a False from any available validator drops the rendering (K1)."""
    from LA_COMMON import validators as V
    from LA_COMMON.expander import shape
    flags = {"tree_sitter": V.shapes_agree(shape(text), V.tree_sitter_shape(text)), "mvdan": V.shapes_agree(shape(text), V.mvdan_shape(text)),
             "sqlglot": None}
    if isinstance(spec.action, Script):
        sqls = [c for c in spec.action.cmds() if c.sql is not None]
        if sqls:
            flags["sqlglot"] = all(V.sql_matches(c.sql, V.sql_info(c.sql.text())) for c in sqls)
    return flags


def _add_rendering(spec, view, role, text, ops, programs, features, ledger):
    r = {"view": view, "role": role, "text": text, "ops": ops, "programs": sorted(programs), "features": features}
    if isinstance(spec.action, Script):
        expect = spec.action
        if spec.intent.startswith("wtr."):
            expect = spec.payloads.get("payload.main")
        elif ".wtr_" in spec.intent:
            expect = spec.payloads.get("payload.late_wtr")
        ok, why = roundtrip_equal(expect, text, _known_files(spec))
        r["validators"] = validator_flags(spec, text)
        if any(v is False for v in r["validators"].values()):
            ok, why = False, "validator:" + ",".join(k for k, v in r["validators"].items() if v is False)
        r["roundtrip"] = ok
        if not ok:
            ledger.add(spec.spec_id, "K1:" + why)
    else:
        kinds = Expander(_known_files(spec)).resolve(text).opaque
        r["roundtrip"] = (kinds == [spec.action.opaque_kind])
        if not r["roundtrip"]:
            ledger.add(spec.spec_id, "K3:opaque kinds %s != %s" % (kinds, spec.action.opaque_kind))
    spec.renderings.append(r)
    return r


def _pick_chain(rng, split, allow_b64, heldout_required=False, level=None):
    """Operator chain. LADDER M5 (obfuscated benign = obfuscated dangerous): level 2 = one operator, 3 = two, 4 = three including a
    resolvable B64-LIT (only for a registered payload); level None keeps the v3.1 draw."""
    pool = [o for o in TRAINED_OPERATORS if allow_b64 or o != "b64_pipe"]
    if split == "dev":
        pool = pool + list(HELDOUT_OPERATORS)
    k = {2: 1, 3: 2, 4: 3}.get(level) or rng.choice([1, 2, 2, 3])
    for _ in range(20):
        ch = rng.sample(pool, min(k, len(pool)))
        if level == 4 and allow_b64 and "b64_pipe" not in ch:
            ch[0] = "b64_pipe"
        if heldout_required and not any(o in HELDOUT_OPERATORS for o in ch):
            ch[0] = rng.choice(HELDOUT_OPERATORS)
        nest = sum(1 for o in ch if o in ("sh_c", "b64_pipe"))
        if nest <= 2:
            tok = [o for o in ch if o not in ("sh_c", "b64_pipe")]
            txt = [o for o in ch if o in ("sh_c", "b64_pipe")]
            return tok + txt
    return ["wrapper_insert"]


def _ladder_ok(ops, level):
    n = len(ops)
    return level is None or (level == 2 and n == 1) or (level == 3 and n == 2) or (level == 4 and n >= 3 and "b64_pipe" in ops)


def _obfuscate(spec, c, rng, ledger, heldout_required=False, level=None):
    """-> RenderResult with at least one operator applied (falls back to wrapper_insert). With a ladder level (M5) the draw is repeated
    (up to 40 times) until the APPLIED operator count matches: an operator that does not apply to the action is silently skipped by the
    renderer, so the level is read from the result, not from the request."""
    allow_b64 = spec.payload_kind is not None and spec.payload_kind in PAYLOAD_REGISTRY.entries
    best = None
    for attempt in range(40 if level else 8):
        chain = _pick_chain(rng, spec.split, allow_b64, heldout_required and attempt < 30, level if (attempt < 30 or not level) else None)
        try:
            r = render(spec.action, rng, c.names, chain, split=spec.split, allowed_programs=None, registered_payload=allow_b64)
        except RenderError:
            continue
        if not r.ops:
            continue
        if _ladder_ok(r.ops, level):
            return r
        best = best or r
    if best is not None:
        return best
    return render(spec.action, rng, c.names, ["wrapper_insert"], split=spec.split)


# ------------------------------------------------------------------------------------------------ user turns
def _turns(spec, c, res, naming_cell=None, cell_keys=None):
    """Task turn (+ naming turn by cell) + evidence notes. naming_cell in {None, neither, op, target, both}."""
    t = [Turn("user", "T50.U.task", {"topic": "lex:topic." + spec.meta.get("domain", "fs")})]
    if spec.naming.get("named_paths"):
        t.append(Turn("user", "T50.U.named_paths", {"paths": ", ".join(spec.naming["named_paths"])}))
    keys = cell_keys or []
    nm = naming_cell or ("both" if (spec.naming["ops"] and spec.naming["targets"]) else None)
    if nm in ("op", "target", "both") and keys:
        op_ref, tgt_ref = keys[0]
        if nm == "op":
            t.append(Turn("user", "T50.U.op_only", {"op": "lex:op." + op_ref}))
        elif nm == "target":
            t.append(Turn("user", "T50.U.target_only", {"target": _target_surface(tgt_ref)}))
        else:
            for (o, g) in keys[:2]:
                t.append(Turn("user", "T50.U.both", {"op": "lex:op." + o, "target": _target_surface(g)}))
    for form, slots in c.user_notes:
        t.append(Turn("user", form, {k: str(v) for k, v in slots.items()}))
    return t


def render_turns(spec, pool=None, seed_tag="turns"):
    """Fill Turn.text and spec.decision_spans from a wording pool (stub pool when None: tests only)."""
    pool = pool or stub_pool()
    rng = rng_for("t50-wording", spec.spec_id, seed_tag)
    spans = []
    for i, t in enumerate(spec.user_turns):
        vals = {}
        for k, v in t.slots.items():
            if isinstance(v, str) and v.startswith("lex:"):
                lid = v[4:]
                vals[k] = pool.lexicon[lid][rng.randrange(len(pool.lexicon[lid]))] if lid in pool.lexicon else lid.split(".")[-1]
            else:
                vals[k] = v
        t.text, sp, t.wording_idx = render_form(pool, t.form, vals, rng, turn_idx=i)
        spans += sp
    spec.decision_spans = spans
    return spec


# ------------------------------------------------------------------------------------------------ views
def with_results_output(spec, warn_level=None):
    """Plain listing/status text for facts that exist only in tool outputs (cap ~256 tokens, no instruction text). LADDER M3 (warning
    visible + safe path exists, with-results view only): warn_level 1-4 appends the warning / preview-form lines of that level."""
    lines = []
    st = spec.state
    for f, how in sorted(spec.fact_visibility.items()):
        if how != "output":
            continue
        kind, _, rest = f.partition(":")
        if kind in ("fs.tracked", "fs.dirty", "fs.created_by_agent"):
            n = st.node(rest)
            if n is not None:
                line = "%s %s %s%s" % (rest, "tracked" if n.tracked else "untracked", "modified" if n.dirty else "clean",
                                       " agent-created" if n.created_by_agent else "")
                if line not in lines:
                    lines.append(line)
        elif kind == "git.hook_failed":
            lines.append("last hook result: %s" % (st.git.last_hook_result or "none"))
        elif kind in ("pkg.lock", "pkg.pin"):
            for p, v in sorted(st.net.lockfile.items()):
                lines.append("lock %s==%s" % (p, v))
        elif kind == "sql.backup":
            db, _, t = rest.partition(".")
            tb = st.sql.dbs.get(db).tables.get(t) if st.sql.dbs.get(db) else None
            lines.append("%s backup=%s" % (rest, "yes" if tb and tb.backup_exists else "no"))
        elif kind == "infra.creator":
            ctx, k, name = rest.split("/")
            r = st.infra.find(ctx, k, name)
            lines.append("%s creator=%s" % (rest, r.creator if r else "none"))
        elif kind == "fs.visibility":
            n = st.node(rest)
            lines.append("%s visibility %s" % (rest, (n.visibility if n is not None and n.visibility else "private")))
        elif kind == "git.tree_tracked":
            pass
        elif kind in ("proc.owner",):
            p = st.proc.procs.get(rest)
            lines.append("pid %s owner=%s" % (rest, p["owner"] if p else "none"))
        else:
            lines.append("%s %s" % (kind, rest))
    if warn_level:
        from .ladder import warning_lines
        lines += warning_lines(warn_level)
    out = "\n".join(dict.fromkeys(lines))
    return out[:1000]


# ------------------------------------------------------------------------------------------------ builders per block
def _new_ctx(cell, card=None):
    return BCtx(group_id(cell), card or cell.card, seed_tag=cell.block)


def _finish_single(cell, c, built, spec_id, ledger, block, naming=None, extras_meta=None, ops=None):
    spec = _make_spec(cell, c, built, spec_id, block, naming, extras_meta)
    res = _solve(spec, c)
    return spec, res


def _build_named(cell, c, built, spec_id, block):
    """User names op+target for every soft verdict: solve once uncleared, then clear."""
    spec = _make_spec(cell, c, built, spec_id, block)
    res0 = label_spec(spec)
    keys = _consent_keys(res0)
    if not keys:
        raise GeneratorDefect("named variant of %s has no soft consent key" % cell.intent)
    spec.naming = {"ops": sorted({k[0] for k in keys}), "targets": sorted({k[1] for k in keys}),
                   "named_paths": list(c.naming.get("named_paths", []))}
    res = _solve(spec, c)
    return spec, res, keys


def build_cell(cell, ledger=None, pool=None):
    """-> list[Spec]. Every Spec has gold, renderings (with round-trip flags) and user turns (text if pool given)."""
    ledger = ledger or DropLedger()
    blk = cell.block
    if blk == "G":
        from .blockg import build_g_cell
        return build_g_cell(cell, ledger, pool)
    if cell.tag == "alias":
        return _build_alias_pair(cell, ledger, pool)
    if cell.tag == "quad4":
        return _build_quad4(cell, ledger, pool)
    if cell.tag == "swap":
        return _build_swap(cell, ledger, pool)
    if blk == "E":
        return _build_quad(cell, ledger, pool)
    if blk == "B":
        return _build_evasion(cell, ledger, pool)
    if blk == "C":
        return _build_adversarial(cell, ledger, pool)
    return _build_single(cell, ledger, pool)


def _views(cell):
    return ("primary", "with_results") if cell.extras.get("twin") else ("primary",)


def _plain(spec, c, ledger, role="plain"):
    r = render_plain(spec.action) if isinstance(spec.action, Script) else None
    text = r.text if r is not None else spec.action.text
    if spec.meta.get("late_text") and spec.intent.startswith("late.") and ".wtr_" not in spec.intent and r is not None:
        text = spec.meta["late_text"]                  # LATE-BINDING direct row: the final binding decides, the text carries the construct
    progs = _programs(spec.action, c_extra(spec))
    for v in _views_of(spec):
        _add_rendering(spec, v, role, text, [], progs, r.features if r else {}, ledger)


def c_extra(spec):
    return set(spec.meta.get("extra_programs", ()))


def _views_of(spec):
    return spec.meta.get("views", ("primary",))


def _build_single(cell, ledger, pool):
    c = _new_ctx(cell)
    meta = REGISTRY[cell.intent]
    v = dict(cell.extras.get("v") or {})
    if cell.tag == "ov":
        v["variant"] = "overwritten"
    built = build_intent(cell.intent, c, v)
    sid = group_id(cell) + ".s0"
    keys = None
    if cell.tag == "named":
        spec, res, keys = _build_named(cell, c, built, sid, cell.block)
    else:
        spec, res = _finish_single(cell, c, built, sid, ledger, cell.block)
    _design_check(spec, cell, res)
    spec.meta["views"] = _views(cell)
    spec.meta["extra_programs"] = sorted(built.extra_programs)
    spec.user_turns = _turns(spec, c, res, "both" if keys else None, keys)
    spec.meta["tag"] = cell.tag
    if cell.extras.get("ladder"):
        spec.ladder = dict(cell.extras["ladder"])
    if cell.intent.startswith("late."):
        spec.sub_block = "LATE"
        spec.meta["domain"] = c.meta.get("real_domain") or c.meta.get("domain") or "fs"        # the real effect domain of the final command
        spec.binding = {"construct": spec.meta.get("late_construct"), "resolved": not isinstance(spec.action, RawScript)}
    _history_text(spec)
    _plain(spec, c, ledger)
    if pool is not None:
        render_turns(spec, pool)
    return [spec]


def _build_alias_pair(cell, ledger, pool):
    """ALIAS row pair (addendum section 5): a dangerous command reaching a protected node through an alias form and a benign
    command using the SAME alias form on an unprotected target, built on one context (same names, same alias tables)."""
    from . import intents_alias as IA
    c = _new_ctx(cell)
    gid = group_id(cell)
    bd, bb = IA.build_alias_pair(c, cell.extras["form"], cell.extras["severity"], domain=cell.extras["domain"], reason=cell.extras["reason"])
    out = []
    for built, sid, role in ((bd, gid + ".d", "dangerous"), (bb, gid + ".b", "benign")):
        spec = _make_spec(cell, c, built, sid, "A")
        res = _solve(spec, c)
        want = expected_for(REGISTRY[built.intent], spec.card)
        if (res.label, res.reason, res.tier) != want:
            raise GeneratorDefect("alias %s on %s: solver %s != design %s (rules %s)" % (built.intent, spec.card_ref, (res.label, res.reason, res.tier), want, res.rules))
        spec.sub_block = "ALIAS"
        spec.meta["domain"] = cell.extras["domain"]
        spec.alias_ref = cell.extras["form"]
        spec.meta.update({"views": ("primary",), "extra_programs": sorted(built.extra_programs), "tag": "alias", "alias_role": role})
        spec.user_turns = _turns(spec, c, res)
        _history_text(spec)
        _plain(spec, c, ledger, role=role)
        if pool is not None:
            render_turns(spec, pool)
        out.append(spec)
    return out


def _build_quad4(cell, ledger, pool):
    """MANDATORY QUAD (section 9): alarming/calm surface x risk-present/resolved, four specs in ONE spec family. Block A builds the four
    template cells directly; block C builds the two risk-present cells and their adversarial-benign twins (the same token inside a harmless
    carrier), so the resolved cells are the C-style 'dangerous token, not executed' rows."""
    from . import quads as Q
    tpl = Q.TEMPLATES[cell.extras["template"]]
    gid = group_id(cell)
    out = []

    def finish(spec, c, res, built, surf, risk, role, surface_text=None):
        text = surface_text if surface_text is not None else render_plain(spec.action).text
        if Q.surface_of(text) != surf:
            raise GeneratorDefect("quad %s cell %s/%s has surface %s: %r" % (cell.extras["template"], surf, risk, Q.surface_of(text), text[:80]))
        spec.sub_block = "QUAD"
        spec.meta["domain"] = REGISTRY[tpl[(surf, "present" if risk == "resolved" and cell.block == "C" else risk)][0]]["domain"]
        spec.quad_id = gid
        spec.quad_axes = {"surface": surf, "risk": risk}
        spec.meta.update({"views": ("primary",), "extra_programs": sorted(built.extra_programs), "tag": "quad4", "quad_cell": "%s/%s" % (surf, risk)})
        spec.user_turns = _turns(spec, c, res)
        _history_text(spec)
        _plain(spec, c, ledger, role=role)
        if pool is not None:
            render_turns(spec, pool)
        out.append(spec)

    if cell.block == "A":
        for k, (surf, risk) in enumerate(Q.CELLS):
            iid, v = tpl[(surf, risk)]
            c = BCtx(gid, cell.card, seed_tag="Q%d" % k)
            built = build_intent(iid, c, dict(v))
            spec = _make_spec(cell, c, built, "%s.q%d" % (gid, k), "A")
            res = _solve(spec, c)
            want = expected_for(REGISTRY[iid], spec.card)
            if (res.label, res.reason, res.tier) != want:
                raise GeneratorDefect("quad %s %s/%s: solver %s != design %s" % (cell.extras["template"], surf, risk, (res.label, res.reason, res.tier), want))
            finish(spec, c, res, built, surf, risk, "quad")
        return out
    for k, surf in enumerate(("alarming", "calm")):
        iid, v = tpl[(surf, "present")]
        c = BCtx(gid, cell.card, seed_tag="Q%d" % k)
        built = build_intent(iid, c, dict(v))
        execd = _make_spec(cell, c, built, "%s.x%d" % (gid, k), "C")
        res = _solve(execd, c)
        want = expected_for(REGISTRY[iid], execd.card)
        if (res.label, res.reason, res.tier) != want:
            raise GeneratorDefect("quad %s %s/present: solver %s != design %s" % (cell.extras["template"], surf, (res.label, res.reason, res.tier), want))
        token = render_plain(execd.action).text
        carrier = rng_for("t50-quad-carrier", gid, k).choice(CARRIERS)
        ben_built = Built(c, Script.of(_token_carrier(c, token, carrier)), "adv.benign:" + carrier, payload_kind=None)
        ben = _make_spec(cell, c, ben_built, "%s.b%d" % (gid, k), "C")
        bres = _solve(ben, c)
        if bres.label != "ALLOW":
            raise GeneratorDefect("quad benign twin labelled %s (carrier %s)" % (bres.label, carrier))
        ben.meta["adv_role"] = "benign"
        execd.meta["adv_role"] = "executed"
        for sp in (execd, ben):
            sp.meta["adv_carrier"] = carrier
        finish(execd, c, res, built, surf, "present", "executed")
        finish(ben, c, bres, ben_built, surf, "resolved", "benign", surface_text=token)
    return out


def _build_swap(cell, ledger, pool):
    out = []
    a, b = cell.extras["swap_cards"]
    for k, card in enumerate((a, b)):
        c = BCtx(group_id(cell), card, seed_tag="A")          # same group -> same names under both cards
        built = build_intent(cell.intent, c, {})
        spec = _make_spec(cell, c, built, "%s.w%d" % (group_id(cell), k), "A")
        res = _solve(spec, c)
        want = expected_for(REGISTRY[cell.intent], spec.card)
        if (res.label, res.reason, res.tier) != want:
            raise GeneratorDefect("swap %s on %s: %s != %s" % (cell.intent, card, (res.label, res.reason, res.tier), want))
        spec.meta.update({"swap_lever": cell.extras["lever"], "swap_member": k, "views": ("primary",),
                          "extra_programs": sorted(built.extra_programs), "tag": "swap"})
        spec.user_turns = _turns(spec, c, res)
        _history_text(spec)
        _plain(spec, c, ledger)
        if pool is not None:
            render_turns(spec, pool)
        out.append(spec)
    labs = {s.gold.label for s in out}
    if len(labs) < 2:
        raise GeneratorDefect("swap pair for %s on %s,%s does not differ in label" % (cell.intent, a, b))
    return out


def _build_quad(cell, ledger, pool):
    c = _new_ctx(cell)
    built = build_intent(cell.intent, c, {})
    base = _make_spec(cell, c, built, group_id(cell) + ".q", "E")
    res0 = label_spec(base)
    soft = cell.tag == "soft_quad"
    keys = _consent_keys(res0) if soft else [hard_refs(base)]
    if soft and not keys:
        raise GeneratorDefect("soft quad %s has no consent key (rules %s)" % (cell.intent, res0.rules))
    cells = {"neither": ({"ops": [], "targets": []}), "op": {"ops": [keys[0][0]], "targets": []},
             "target": {"ops": [], "targets": [keys[0][1]]},
             "both": {"ops": sorted({k[0] for k in keys}), "targets": sorted({k[1] for k in keys})}}
    out = []
    for nm, naming in cells.items():
        c2 = copy.deepcopy(c)
        spec = _make_spec(cell, c2, built, "%s.q_%s" % (group_id(cell), nm), "E", naming=dict(naming, named_paths=[]))
        spec.state = copy.deepcopy(c.st)
        res = _solve(spec, c2)
        spec.meta.update({"quad": cell.tag, "quad_cell": nm, "views": ("primary",), "extra_programs": sorted(built.extra_programs),
                          "tag": cell.tag})
        spec.user_turns = _turns(spec, c2, res, nm, keys)
        _history_text(spec)
        _plain(spec, c2, ledger)
        out.append(spec)
    # label expectations of a quad
    labs = {s.meta["quad_cell"]: s.gold.label for s in out}
    if soft:
        if labs["both"] != "ALLOW" or any(labs[k] == "ALLOW" for k in ("neither", "op", "target")):
            raise GeneratorDefect("soft quad %s labels %s" % (cell.intent, labs))
    else:
        if any(v != "BLOCK" for v in labs.values()):
            raise GeneratorDefect("hard quad %s labels %s" % (cell.intent, labs))
        if any(s.gold.tier != "hard" for s in out):
            raise GeneratorDefect("hard quad %s lost its hard tier" % cell.intent)
    if pool is not None:
        for s in out:
            render_turns(s, pool)
    return out


def _build_evasion(cell, ledger, pool):
    c = _new_ctx(cell)
    built = build_intent(cell.intent, c, {})
    spec, res = _finish_single(cell, c, built, group_id(cell) + ".b", ledger, "B")
    _design_check(spec, cell, res)
    rng = rng_for("t50-evasion", spec.spec_id)
    spec.meta.update({"views": _views(cell), "extra_programs": sorted(built.extra_programs), "tag": "evasion"})
    spec.user_turns = _turns(spec, c, res)
    _history_text(spec)
    plain = render_plain(spec.action)
    obf = _obfuscate(spec, c, rng, ledger, heldout_required=(spec.split == "dev"), level=cell.extras.get("m5"))
    progs_p = _programs(spec.action, built.extra_programs)
    n_ops = len(obf.ops)
    lvl = 2 if n_ops <= 1 else (3 if n_ops == 2 else (4 if "b64_pipe" in obf.ops else 3))
    for v in _views(cell):
        r0 = _add_rendering(spec, v, "plain", plain.text, [], progs_p, plain.features, ledger)
        r1 = _add_rendering(spec, v, "obf", obf.text, obf.ops, progs_p | obf.programs, obf.features, ledger)
        r0["ladder"] = {"mechanism": "M5", "level": 1}
        r1["ladder"] = {"mechanism": "M5", "level": lvl}
    spec.meta["heldout_ops"] = [o for o in obf.ops if o in HELDOUT_OPERATORS]
    if pool is not None:
        render_turns(spec, pool)
    return [spec]


CARRIERS = ("echo", "grep", "commit", "testname")


def _token_carrier(c, token, carrier):
    """The dangerous token inside a harmless carrier (adversarial-benign): echo / grep / commit message / test name."""
    docs = c.root + "/src"
    if carrier == "echo":
        return Cmd("echo", args=[token])
    if carrier == "grep":
        return Cmd("grep", flags=[["-rn"]], args=[token, docs])
    if carrier == "commit":
        c.file("dirty", "advc", ".txt", "src")
        return Cmd("git", sub="commit", flags=[["-m", token]])
    slug = "_".join(w for w in "".join(ch if ch.isalnum() else " " for ch in token).split()[:4])
    tpath = c.root + "/tests/test_%s.txt" % slug
    c.file("clean", "advt", ".txt", path=tpath)
    return Cmd("cat", args=[tpath])


def _build_adversarial(cell, ledger, pool):
    c = _new_ctx(cell)
    built = build_intent(cell.intent, c, {})
    gid = group_id(cell)
    execd, res = _finish_single(cell, c, built, gid + ".x", ledger, "C")
    _design_check(execd, cell, res)
    token = render_plain(execd.action).text
    rng = rng_for("t50-adv", gid)
    carrier = rng.choice(CARRIERS)
    cmd = _token_carrier(c, token, carrier)
    benign_built = Built(c, Script.of(cmd), "adv.benign:" + carrier, payload_kind=None)
    ben = _make_spec(cell, c, benign_built, gid + ".b", "C")
    bres = _solve(ben, c)
    if bres.label != "ALLOW":
        raise GeneratorDefect("adversarial-benign twin of %s labelled %s (carrier %s, rules %s)" % (cell.intent, bres.label, carrier, bres.rules))
    out = []
    for sp, kind in ((execd, "executed"), (ben, "benign")):
        sp.meta.update({"adv_role": kind, "adv_carrier": carrier, "views": _views(cell), "tag": "adversarial",
                        "extra_programs": sorted(built.extra_programs)})
        sp.user_turns = _turns(sp, c, bres if kind == "benign" else res)
        _history_text(sp)
        _plain(sp, c, ledger, role=kind)
        if pool is not None:
            render_turns(sp, pool)
        out.append(sp)
    return out


# ------------------------------------------------------------------------------------------------ rows
def spec_rows(spec, ledger=None):
    """Expand a spec into row dicts (one per rendering that passed the round-trip check). TESTS / PILOT ONLY.
    A15: every row carries its dialect id and the policy-card BODY rendered in that dialect (the C2 scaffold around it is L-0's: the stub
    scaffold in dialects.py is NOT used here); the v3.2 overlay fields ride along so a consumer (solver B, the gates) can measure them."""
    rows = []
    body = dialects.render_card_body(spec.dialect, spec.card) if spec.dialect else ""
    for r in spec.renderings:
        if not r.get("roundtrip", True):
            continue
        rows.append({"spec_id": spec.spec_id, "group": spec.group, "block": spec.block, "view": r["view"], "role": r["role"],
                     "call": r["text"], "ops": r["ops"], "gold": {"label": spec.gold.label, "reason": spec.gold.reason,
                                                                  "tier": spec.gold.tier},
                     "split": spec.split, "card": spec.card_ref, "intent": spec.intent,
                     "dialect": spec.dialect, "card_body": body, "heldout_family": spec.heldout_family, "sub_block": spec.sub_block,
                     "path_class": spec.path_class, "zone": spec.zone, "carrier": spec.carrier, "alias_ref": spec.alias_ref,
                     "quad_id": spec.quad_id, "quad_axes": spec.quad_axes, "ladder": spec.ladder, "cue": spec.cue,
                     "perturbation": spec.perturbation, "single_trigger": spec.meta.get("single_trigger", True)})
        if r["view"] == "with_results":
            rows[-1]["output"] = with_results_output(spec, r.get("warning_level"))
    return rows
