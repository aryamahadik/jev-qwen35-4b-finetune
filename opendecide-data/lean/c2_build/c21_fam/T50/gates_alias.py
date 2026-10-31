"""K25 (ALIAS rows) and K26 (LATE-BINDING rows) -- addendum v3.2 section 12. CPU, data only; same style as
T50/gates.py (whose `_res` dict shape is reused so these slot into the same gate-report format).
"""
from collections import Counter

from LA_COMMON import probe
from LA_COMMON.expander import Expander
from LA_COMMON.render import render_plain
from LA_COMMON.spec import Gold, Spec

from .gates import _res
from .intents_alias import ALIAS_FORMS, build_all_alias_pairs
from .intents_late import LATE_CONSTRUCTS, LATE_D_OPAQUE_CONSTRUCT, LATE_FIXTURES, build_late_opaque
from .solver_a import label_spec


# ------------------------------------------------------------------------------------------------ spec building
def _to_spec(built, spec_id, group, block="A"):
    sp = Spec(spec_id=spec_id, family="T50", block=block, card_ref=built.c.card["card_id"], card=built.c.card,
              state=built.c.st, naming=built.c.naming, history=list(built.c.hist), action=built.script,
              payloads=dict(built.c.payloads), payload_kind=built.payload_kind, intent=built.intent,
              group=group, meta=dict(built.c.meta))
    res = label_spec(sp)
    sp.gold = Gold(res.label, res.reason, res.tier)
    sp.rule_ids = list(res.rules)
    sp.effects = list(res.effects)
    try:
        text = render_plain(sp.action).text
    except Exception:
        text = getattr(sp.action, "text", "")
    sp.renderings = [{"view": "primary", "role": "plain", "text": text, "ops": [], "programs": [],
                      "features": {}, "roundtrip": True}]
    return sp


def build_alias_specs():
    """150 pairs -> [(pair_info, spec_dangerous, spec_benign), ...]."""
    out = []
    for i, p in enumerate(build_all_alias_pairs()):
        gid = "ALIAS-%04d" % i
        gd = _to_spec(p["dangerous"], gid + ".d", gid)
        gb = _to_spec(p["benign"], gid + ".b", gid)
        out.append((p, gd, gb))
    return out


# ------------------------------------------------------------------------------------------------ K25
def k25_alias(pair_specs=None):
    pair_specs = pair_specs if pair_specs is not None else build_alias_specs()
    n = len(pair_specs)
    dang_block = sum(1 for p, gd, gb in pair_specs if gd.gold.label == "BLOCK")
    dang_ask = sum(1 for p, gd, gb in pair_specs if gd.gold.label == "ASK")
    dang_other = n - dang_block - dang_ask
    benign_allow = sum(1 for p, gd, gb in pair_specs if gb.gold.label == "ALLOW")
    per_form = Counter(p["form"] for p, gd, gb in pair_specs)
    forms_ok = set(per_form) == set(ALIAS_FORMS) and all(abs(c - 25) <= 5 for c in per_form.values())
    counts_ok = (n == 150 and dang_block == 110 and dang_ask == 40 and dang_other == 0 and benign_allow == 150)

    unit_bad = []
    for p, gd, gb in pair_specs:
        if gb.gold.label != "ALLOW" or gb.gold.reason != "none" or gb.gold.tier != "na":
            unit_bad.append(gb.spec_id)
        want_hard = p["severity"] == "hard"
        if want_hard and gd.gold.tier != "hard":
            unit_bad.append(gd.spec_id + ":tier")
        if not want_hard and gd.gold.label not in ("BLOCK", "ASK"):
            unit_bad.append(gd.spec_id + ":label")
    unit_tests_ok = not unit_bad

    rows = []
    for p, gd, gb in pair_specs:
        base = {"form_" + p["form"]: 1.0, "alias_count": 1.0}
        rows.append((dict(base, path_len=float(len(gd.renderings[0]["text"]))), 1))
        rows.append((dict(base, path_len=float(len(gb.renderings[0]["text"]))), 0))
    prob = probe.run_valid(probe.binary_probe, [r[0] for r in rows], [r[1] for r in rows],
                            [i // 2 for i in range(len(rows))]) if len(rows) >= 20 else None
    probe_ok = prob is None or prob["pass"]

    ok = counts_ok and unit_tests_ok and forms_ok and probe_ok
    return _res("K25", "alias rows", "alias-table unit tests 100%; benign twins = dangerous count (150/150); "
               "6 forms x 50 rows (+-5); alias-form-only probe AUC <= 0.55, ub <= 0.60", ok,
               n_pairs=n, dangerous_block=dang_block, dangerous_ask=dang_ask, dangerous_other=dang_other,
               benign_allow=benign_allow, per_form=dict(per_form), forms_ok=forms_ok, unit_tests_ok=unit_tests_ok,
               unit_test_violations=unit_bad[:20], probe=prob)


# ------------------------------------------------------------------------------------------------ K26
def _fixtures_by_construct():
    by = {}
    for construct, text, env, expected in LATE_FIXTURES:
        by.setdefault(construct, []).append((text, env, expected))
    return by


def k26_late_fixtures():
    """100% of LATE_FIXTURES pass, reported per construct."""
    by = _fixtures_by_construct()
    per_construct = {}
    all_ok = True
    for construct, cases in by.items():
        bad = []
        for text, env, expected in cases:
            res = Expander(env=env).resolve(text)
            if expected == "opaque":
                ok = bool(res.opaque)
            else:
                ok = (not res.opaque) and [c.words for c in res.cmds] == expected
            if not ok:
                bad.append(text)
        per_construct[construct] = {"n": len(cases), "pass": not bad, "failures": bad}
        all_ok = all_ok and not bad
    return all_ok, per_construct


def k26_late(built_rows=None):
    """built_rows: optional list of (spec, is_opaque) from the caller's own build of the 150 late-binding rows
    (60 block A + 90 block D). When omitted, builds a representative sample via the registry (every construct x
    every label, plus the 35-row opaque construct) to compute the resolvable/ASK shares."""
    fixtures_ok, per_construct = k26_late_fixtures()

    if built_rows is None:
        from .build import BCtx
        from .intents_late import build_late_direct, build_late_wtr
        built_rows = []
        for construct in LATE_CONSTRUCTS:
            for label in ("ALLOW", "ASK", "BLOCK"):
                c = BCtx("k26-direct-%s-%s" % (construct, label), "card.t50.c01")
                b = build_late_direct(c, construct, label)
                sp = _to_spec(b, "k26.%s.%s" % (construct, label), "k26-%s-%s" % (construct, label))
                built_rows.append((sp, False))
                c2 = BCtx("k26-wtr-%s-%s" % (construct, label), "card.t50.c01")
                b2 = build_late_wtr(c2, construct, label)
                sp2 = _to_spec(b2, "k26.wtr.%s.%s" % (construct, label), "k26-wtr-%s-%s" % (construct, label),
                               block="D")
                built_rows.append((sp2, False))
        c3 = BCtx("k26-opaque", "card.t50.c01")
        b3 = build_late_opaque(c3)
        sp3 = _to_spec(b3, "k26.opaque", "k26-opaque", block="D")
        built_rows.append((sp3, True))

    n = len(built_rows)
    resolved = [sp for sp, opq in built_rows if not opq]
    opaque_rows = [sp for sp, opq in built_rows if opq]
    opaque_all_ask = all(sp.gold.label == "ASK" and sp.gold.reason == "none" and sp.gold.tier == "na"
                        for sp in opaque_rows)
    resolvable_share = len(resolved) / n if n else 0.0
    ask_share = sum(1 for sp, _ in built_rows if sp.gold.label == "ASK") / n if n else 0.0

    ok = (fixtures_ok and opaque_all_ask and resolvable_share >= 0.40 and ask_share <= 0.60)
    return _res("K26", "late-binding rows", "fixtures pass 100% per construct; 100% unresolved -> ASK; "
               "resolvable >= 40%, ASK share <= 60%", ok,
               fixtures_per_construct=per_construct, fixtures_ok=fixtures_ok, n_rows=n,
               resolvable_share=resolvable_share, ask_share=ask_share, opaque_all_ask=opaque_all_ask,
               opaque_construct=LATE_D_OPAQUE_CONSTRUCT,
               skeptic_review_recorded=False)   # ASSUMPTION: the Sonnet skeptic review itself is a process step
                                                 # outside this CPU gate; recorded here only as a flag to fill in.
