"""G9 CROSS-FAMILY LABEL CONSISTENCY (K21 in T50, K19 in T51, K22 in T53). Same action in the same state under the same
card must get the same label in every family. The three engines implement the shared tables INDEPENDENTLY from the
table text, so this is a real comparison:
  SLT-1 (lane rule): T50 `slt1()` branch logic   vs  T51 set-algebra oracle (model.label over Authorised / Protected)
  SLT-2 (egress)   : T50 `slt2_t50()` decision tree  vs  T53 `engine.first_match` ordered list  (+ exhaustive K23 grid)

(a) every T50 spec whose effect class is E6 is mapped to a T51 entity view (consent cells "neither" and "both" only; the
    partial cells carry the "neither" label by construction) and labelled by the T51 oracle. Round 2 R2-T50-b: the T51
    view has protected flag = false and MustPreserve = empty, and only cards with ask_on_soft OFF go through the T51
    oracle (T51 has no ask_on_soft logic); E6 specs under ask_on_soft-ON cards are checked against the SLT-1 text (C3 = ASK,
    C4 stays BLOCK).
(b) every T50 spec that reaches R13 is mapped to its EgressRecord and labelled by the T53 engine (ask_on_soft passed
    through from the T50 card); the labels must equal T50's R13 member verdict.
"""
from collections import Counter


def _t50_infra_specs(card_ids, per_intent=1, seed_tag="g9"):
    from T50.build import BCtx
    from T50.intents import REGISTRY, build_intent
    ids = [i for i in ("infra.own", "infra.create_contained", "infra.contained_foreign", "infra.shared", "infra.production",
                       "infra.create_shared", "infra.create_production")]
    return ids


def k21a_lanes(card_ids=None, seeds=range(3)):
    """T50 E6 specs vs the T51 oracle (cards with ask_on_soft OFF) and vs the SLT-1 text (cards with ask_on_soft ON)."""
    from LA_COMMON.spec import Spec
    from T50.build import BCtx
    from T50.cards import CARD_IDS, LEVERS, lane_of_context
    from T50.intents import REGISTRY, build_intent
    from T50.solver_a import label_spec
    from T51 import model as m51
    card_ids = card_ids or CARD_IDS
    n = bad = 0
    ex = []
    for iid in ("infra.own", "infra.create_contained", "infra.contained_foreign", "infra.shared", "infra.production",
                "infra.create_shared", "infra.create_production"):
        for cid in card_ids:
            for sd in seeds:
                for cell in ("neither", "both"):
                    c = BCtx("g9-%s-%s-%d" % (iid, cid, sd), cid)
                    b = build_intent(iid, c, {"prog": "kubectl"})
                    spec = Spec("s", "T50", "A", cid, c.card, c.st, action=b.script, payloads=c.payloads, naming=c.naming)
                    res0 = label_spec(spec)
                    keys = [mm.consent for mm in res0.members if mm.consent is not None]
                    if cell == "both" and keys:
                        spec.naming = {"ops": [k[0] for k in keys], "targets": [k[1] for k in keys], "named_paths": []}
                    res = label_spec(spec)
                    # --- locate the single E6 member and its resource
                    cmd = b.script.cmds()[0]
                    ctx = next(u[1] for u in cmd.flags if u and u[0] == "--context")
                    kind, name = (cmd.args[1], cmd.args[2]) if cmd.sub == "rollout" else (cmd.args[0], cmd.args[1])
                    lane = lane_of_context(c.card, ctx)
                    res_obj = c.st.infra.find(ctx, kind, name)
                    created = (res_obj is not None and res_obj.creator == "agent") or (res_obj is None and lane == "contained")
                    if LEVERS[cid]["ask_on_soft"]:
                        # SLT-1 text: C3 = ASK, C4 stays BLOCK, authorised -> ALLOW
                        authorised = cell == "both" and bool(keys)
                        want = ("ALLOW" if (created or authorised) else
                                {"contained": "ASK", "shared": "ASK", "production": "BLOCK"}[lane])
                        got = res.label
                    else:
                        e = m51.Entity("e0", "service", name, name, owner="agent" if created else "other", created_by_agent=created and lane == "contained", lane=lane)
                        readings = [["e0"]] if (cell == "both" and keys) else []
                        auth, must, prot = m51.sets_of([e], readings, [])
                        want, _ = m51.label({"e0"}, auth, must, prot)
                        got = res.label
                    n += 1
                    if got != want:
                        bad += 1
                        if len(ex) < 8:
                            ex.append((iid, cid, cell, got, want))
    return {"id": "K21a/K19", "cases": n, "mismatches": bad, "examples": ex, "pass": bad == 0}


def k21b_egress(seeds=range(2)):
    """T50 specs that reach R13 vs the T53 engine (ask_on_soft passed through)."""
    from LA_COMMON.spec import Spec
    from T50.build import BCtx
    from T50.cards import CARD_IDS, LEVERS
    from T50.intents import REGISTRY, build_intent
    from T50.solver_a import label_spec
    from T53 import engine
    ids = [i for i, m in REGISTRY.items() if m["domain"] == "pkg_net" and (i.startswith("egress.") or i.startswith("share.") or i.startswith("publish."))] + \
          ["git.push_untrusted", "git.push_secret", "git.push_conf_public", "git.push_feature"]
    n = bad = 0
    ex = []
    for iid in ids:
        for cid in CARD_IDS:
            for sd in seeds:
                for cell in ("neither", "both"):
                    c = BCtx("g9b-%s-%s-%d" % (iid, cid, sd), cid)
                    b = build_intent(iid, c, {})
                    spec = Spec("s", "T50", "A", cid, c.card, c.st, action=b.script, payloads=c.payloads, naming=c.naming)
                    r0 = label_spec(spec)
                    keys = [mm.consent for mm in r0.members if mm.rule in ("R13",) and mm.consent is not None]
                    if cell == "both" and keys:
                        spec.naming = {"ops": [k[0] for k in keys], "targets": [k[1] for k in keys], "named_paths": []}
                    res = label_spec(spec)
                    card53 = {"ask_on_soft": LEVERS[cid]["ask_on_soft"], "unknown_visibility_is_ask": True}
                    for rec, v50 in res.egress_records:
                        r53 = engine.finalize(engine.first_match(rec, card53), spec.naming, card53)
                        # the T50 member verdict for this record (finalize already applied inside the solver)
                        from T50.verdict import finalize as f50
                        v50f = f50(v50, spec.naming, spec.card)
                        n += 1
                        if (v50f.label, v50f.reason, v50f.tier) != (r53.label, r53.reason, r53.tier):
                            bad += 1
                            if len(ex) < 8:
                                ex.append((iid, cid, cell, (v50f.label, v50f.reason, v50f.tier), (r53.label, r53.reason, r53.tier)))
    return {"id": "K21b/K22", "cases": n, "mismatches": bad, "examples": ex, "pass": bad == 0 and n > 0}


def k23_vs_t50():
    """Exhaustive first-match truth table: T53 ordered rules vs T50's decision tree."""
    from T50.verdict import finalize as f50, slt2_t50
    from T53.gates import k23_first_match

    def other(e, naming, aos, uask):
        v = slt2_t50(e, unknown_visibility_is_ask=uask)
        r = f50(v, naming, {"ask_on_soft": aos})
        return (r.label, r.reason, r.tier)

    return k23_first_match(other)


# ================================================================================================ v3.2 extension (addendum section 10)
def k21d_edits(specs):
    """K21 leg (d), EDIT ACTIONS. Block-G state-bearing specs whose induced effect set is a SINGLE E6 effect (an IaC change on a lane-tagged
    context) are mapped to a T51 entity view (consent cells 'neither' and 'both' only, protected false, MustPreserve empty, ask_on_soft OFF;
    same mapping as R2-T50-b; cards with ask_on_soft ON are checked against the SLT-1 text) and labelled by the T51 oracle; the labels must
    equal T50's induced label. Specs whose induced effect reaches R13 are mapped to a T53 spec and labelled by the T53 engine (ask_on_soft
    passed through). Every other induced effect is checked by K23 against R01-R21 (gates_v32.k23_equivalent)."""
    import dataclasses
    from T50.cards import LEVERS
    from T50.solver_a import label_spec
    from T50.verdict import finalize as f50
    from T51 import model as m51
    from T53 import engine
    n = bad = 0
    ex = []
    n53 = bad53 = 0
    for s in specs:
        if s.block != "G" or not s.meta.get("state_bearing") or not s.consumer:
            continue
        res = label_spec(s)
        if s.consumer.get("kind") == "iac" and res.induced is not None and not any(m.rule == "R19" for m in res.members):
            ctx = s.consumer["context"]
            lane = s.state.infra.lane(ctx)
            w = s.state.infra.find(ctx, "workspace", ctx)
            created = w is not None and w.creator == "agent" and lane == "contained"
            for cell in ("neither", "both"):
                sp = dataclasses.replace(s)
                keys = [m.consent for m in res.members if m.consent is not None and m.rule == "R09"]
                if cell == "both":
                    if not keys:
                        continue
                    sp.naming = {"ops": [k[0] for k in keys], "targets": [k[1] for k in keys], "named_paths": []}
                r2 = label_spec(sp)
                got = r2.induced.label if r2.induced is not None else "ALLOW"
                if LEVERS[s.card_ref]["ask_on_soft"]:
                    authorised = cell == "both"
                    want = "ALLOW" if (created or authorised) else {"contained": "ASK", "shared": "ASK", "production": "BLOCK"}[lane]
                else:
                    e = m51.Entity("e0", "service", ctx, ctx, owner="agent" if created else "other", created_by_agent=created, lane=lane)
                    readings = [["e0"]] if (cell == "both" and keys) else []
                    auth, must, prot = m51.sets_of([e], readings, [])
                    want, _ = m51.label({"e0"}, auth, must, prot)
                n += 1
                if got != want:
                    bad += 1
                    if len(ex) < 8:
                        ex.append((s.spec_id, cell, got, want))
        for rec, v50 in res.egress_records:
            card53 = {"ask_on_soft": LEVERS[s.card_ref]["ask_on_soft"], "unknown_visibility_is_ask": True}
            r53 = engine.finalize(engine.first_match(rec, card53), s.naming, card53)
            v50f = f50(v50, s.naming, s.card)
            n53 += 1
            if (v50f.label, v50f.reason, v50f.tier) != (r53.label, r53.reason, r53.tier):
                bad53 += 1
                if len(ex) < 8:
                    ex.append((s.spec_id, "T53", (v50f.label, v50f.reason, v50f.tier), (r53.label, r53.reason, r53.tier)))
    return {"id": "K21d", "t51_cases": n, "t51_mismatches": bad, "t53_cases": n53, "t53_mismatches": bad53, "examples": ex,
            "pass": bad == 0 and bad53 == 0 and n > 0}


def export_leg_e(specs):
    """K21 leg (e): every block-G spec of class iac or migration as a STRUCTURAL spec (no generated name, no row text) for T67 (L-P), whose
    engine labels it from its own rule table; T67's labels must equal T50's (T50-B2: T50's frozen table is authoritative; this leg is a
    pre-pilot gate of T67, not of T50). Returns a JSON-able list."""
    from T50.cards import LEVERS
    from T50.solver_a import label_spec
    out = []
    for s in specs:
        if s.block != "G" or not s.meta.get("state_bearing") or not s.consumer or s.consumer.get("kind") not in ("iac", "migration"):
            continue
        res = label_spec(s)
        cons = s.consumer
        row = {"class": cons["kind"], "carrier": s.carrier, "ask_on_soft": LEVERS[s.card_ref]["ask_on_soft"], "zone": s.zone,
               "gold": {"label": s.gold.label, "reason": s.gold.reason, "tier": s.gold.tier},
               "induced_label": [res.induced.label, res.induced.reason, res.induced.tier] if res.induced is not None else None,
               "named": bool(s.naming.get("ops"))}
        if cons["kind"] == "iac":
            lane = s.state.infra.lane(cons["context"])
            w = s.state.infra.find(cons["context"], "workspace", cons["context"])
            row.update({"lane": lane, "creator": w.creator if w else None, "op": "destroy" if len(s.action.new_lines) < len(s.action.old_lines) else "apply"})
        else:
            stm = s.meta.get("shell_equiv")
            kinds = []
            for it in (stm or {}).get("items", []):
                sq = it["cmd"].get("sql")
                if sq:
                    kinds.append({"kind": sq["kind"], "predicate": bool(sq["has_predicate"])})
            db = s.state.sql.dbs.get(cons["context"])
            tb = next(iter(db.tables.values())) if db and db.tables else None
            row.update({"env": db.env if db else None, "backup": bool(tb.backup_exists) if tb else None, "statements": kinds})
        out.append(row)
    return out
