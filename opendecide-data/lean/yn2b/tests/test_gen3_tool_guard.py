"""Tests of yn2b family F2 gen3_tool_guard (golden_src/gen3/gen3_tool_guard.py + tg_packs, tg_core, tg_sample,
tg_render, tg_output). CPU only; every build writes into pytest's tmp_path; decoder_io / prism_x / train_decoder are
imported read-only (prompt building only, no model).

  PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python -m pytest -q -p no:cacheprovider --basetemp=<scratch> \
      yn2b/tests/test_gen3_tool_guard.py
"""
from __future__ import annotations

import copy
import hashlib
import json
import random
import re
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from fractions import Fraction
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[1]
GEN3 = LEAN / "golden_src" / "gen3"
for p in (str(GEN3), str(LEAN), str(HERE.parent)):
    if p not in sys.path:
        sys.path.insert(0, p)
import mv_core as mv  # noqa: E402
import tg_packs as tp  # noqa: E402
import tg_core as tc  # noqa: E402
import tg_sample as ts  # noqa: E402
import tg_render as tr  # noqa: E402
import tg_output as to  # noqa: E402
import gen3_tool_guard as g  # noqa: E402

UTC = timezone.utc
SMALL = {s: {k: max(2, v // 10) for k, v in d.items()} for s, d in g.TARGETS.items()}


def build_small(tmp):
    b = g.Builder(raw_dir=tmp / "raw", defs_dir=tmp / "defs", manifest=tmp / "M.jsonl", targets=SMALL)
    for split in ("train", "dev_iid", "dev_holdout"):
        b.build_split(split)
    return b


@pytest.fixture(scope="module")
def small(tmp_path_factory):
    return build_small(tmp_path_factory.mktemp("f2small"))


# ================================================================================================ packs
def test_packs_static():
    tp.check_packs()
    assert len(tp.PACKS) == 12 and set(tp.HOLDOUT_PACKS) == {"smart_home", "clinic"}
    assert len(tp.TRAIN_PACKS) == 10
    g2 = tp.gen2_tool_purposes()  # SPEC F2: the tool lists of gen2_tool_selection are imported, plus new ones
    shared = [t.name for p in tp.PACKS.values() for t in p.tools if t.name in g2]
    assert len(shared) >= 15
    for p in tp.PACKS.values():
        assert {t.cls for t in p.tools} == set(tp.CLASSES)
        assert len({t.rtype for t in p.tools}) == len(p.tools)  # closed request-type list, one tool each


# ================================================================================================ hand-built items
def mk(pack="banking", tool="send_payment", args=None, rules=(), now=None, **kw):
    P = tp.PACKS[pack]
    T = P.tool(tool)
    it = tc.Item(pack, "Kelvora Labs", "kelvora.example", kw.pop("tz", "Europe/Berlin"),
                 now or datetime(2026, 3, 16, 10, 0, tzinfo=UTC), "Mara Holt", "u-11111",
                 kw.pop("role", P.roles[0]), kw.pop("rtype", T.rtype), "S-100000", tool,
                 dict(args or {}), "c-999999", kw.pop("catalog", [tool]), [],
                 {"rates": dict(P.rates), "approved": ["gelax.test"], "subsidiaries": [], "roles": {},
                  "envs": {}, "classes": {}, "holidays": []})
    for k, v in kw.items():
        setattr(it, k, v)
    for i, r in enumerate(rules, 1):
        r.no = i
        r.date = "2025-06-01"
        it.rules.append(r)
    return it


def R(atom, p=None, scope=None, tool="send_payment"):
    return tc.Rule(atom, scope or ("tools", (tool,)), dict(p or {}))


PAY = {"from_account": "AC-123456", "payee_iban": "DE44ABCDEF123456", "amount": 2000, "currency": "EUR",
       "idempotency_key": "pay-abcd1234"}


def ok(it, n=1):
    return tc.evaluate(it).outcome[n]


def test_threshold_boundaries_and_conversion():
    le = R("threshold", {"arg": "amount", "op": "<=", "limit": Fraction(2000), "unit": "EUR", "unit_is_cur": True})
    lt = R("threshold", {"arg": "amount", "op": "<", "limit": Fraction(2000), "unit": "EUR", "unit_is_cur": True})
    assert ok(mk(args=PAY, rules=[le])) is True
    assert ok(mk(args=PAY, rules=[lt])) is False
    assert ok(mk(args=dict(PAY, amount=1999.99), rules=[lt])) is True
    # 1709.40 GBP x 1.17 = 1999.998 -> rounded half-up to 2000.00 EUR (the rate is stated in the annex)
    gbp = dict(PAY, amount=1709.4, currency="GBP")
    assert ok(mk(args=gbp, rules=[copy.deepcopy(le)])) is True
    assert ok(mk(args=gbp, rules=[copy.deepcopy(lt)])) is False


def test_time_window_zone_dst_and_business_days():
    p = {"zone": "Europe/Berlin", "start": "09:00", "end": "17:00", "business": True}
    at = lambda s: datetime.fromisoformat(s).replace(tzinfo=UTC)  # noqa: E731
    # summer (CEST, UTC+2): 15:00Z = 17:00 local -> the end minute is outside; 14:59Z inside
    assert ok(mk(args=PAY, rules=[R("time", p)], now=at("2026-07-01T15:00:00"))) is False
    assert ok(mk(args=PAY, rules=[R("time", p)], now=at("2026-07-01T14:59:00"))) is True
    # winter (CET, UTC+1): 16:30Z = 17:30 local -> outside; 07:30Z = 08:30 local -> outside; 08:00Z = 09:00 inside
    assert ok(mk(args=PAY, rules=[R("time", p)], now=at("2026-01-15T16:30:00"))) is False
    assert ok(mk(args=PAY, rules=[R("time", p)], now=at("2026-01-15T08:00:00"))) is True
    it = mk(args=PAY, rules=[R("time", p)], now=at("2026-01-15T10:00:00"))
    it.annex["holidays"] = ["2026-01-15"]
    assert ok(it) is False
    sat = mk(args=PAY, rules=[R("time", p)], now=at("2026-01-17T10:00:00"))
    assert ok(sat) is False
    # the ignore-the-time-zone shortcut reads the UTC clock as local time
    it2 = mk(args=PAY, rules=[R("time", dict(p, business=False))], now=at("2026-07-01T07:30:00"))
    assert ok(it2) is True and tc.shortcut_verdicts(it2)["ignore_tz"][0] == "block"


def test_aggregate_excludes_failed_reversed_other_user_other_day():
    now = datetime(2026, 3, 16, 10, 0, tzinfo=UTC)
    p = {"measure": "count", "limit": 2, "zone": "Europe/Berlin", "unit": "EUR"}
    L = lambda m, st="ok", u="u-11111": tc.LogE(f"c-{m}", now - timedelta(minutes=m), "send_payment", u,  # noqa
                                              "S-100000", {}, st)
    decoys = [L(5, "failed"), L(6, "reversed"), L(7, u="u-22222"), L(24 * 60 + 5)]
    it = mk(args=PAY, rules=[R("aggregate", p)], now=now, log=[L(3)] + decoys)
    assert ok(it) is True                     # 1 valid + the proposed call = 2 <= 2
    assert tc.shortcut_verdicts(it)["sum_whole_log"][0] == "block"
    it.log.append(L(4))
    assert ok(it) is False


def test_confirmation_match_stale_revoked_person_amount_and_trigger():
    now = datetime(2026, 3, 16, 10, 0, tzinfo=UTC)
    p = {"window": 15, "fields": "amount, currency and payee", "above": None, "unit": "EUR"}
    vals = {"amount": "2,000.00", "currency": "EUR", "payee": "DE44ABCDEF123456"}
    C = lambda mins, **k: tc.Conf("K-1", k.get("by", "u-11111"), "Mara Holt", k.get("values", vals),  # noqa: E731
                                  now - timedelta(minutes=mins), k.get("rev"))
    assert ok(mk(args=PAY, rules=[R("confirm", p)], now=now, confs=[C(15)])) is True      # exactly 15 minutes old
    assert ok(mk(args=PAY, rules=[R("confirm", p)], now=now, confs=[C(16)])) is False
    assert ok(mk(args=PAY, rules=[R("confirm", p)], now=now, confs=[C(5, rev=now - timedelta(minutes=1))])) is False
    assert ok(mk(args=PAY, rules=[R("confirm", p)], now=now, confs=[C(5, by="u-22222")])) is False
    assert ok(mk(args=PAY, rules=[R("confirm", p)], now=now,
                 confs=[C(5, values=dict(vals, amount="2,010.00"))])) is False
    assert ok(mk(args=PAY, rules=[R("confirm", p)], now=now, confs=[])) is False
    # not triggered: the rule applies only above 2,500.00 EUR
    assert ok(mk(args=PAY, rules=[R("confirm", dict(p, above=Fraction(2500)))], now=now, confs=[])) is True


def test_confirm_question_predicate():
    now = datetime(2026, 3, 16, 10, 0, tzinfo=UTC)
    pc = {"window": 15, "fields": "amount, currency and payee", "above": None, "unit": "EUR"}
    le = {"arg": "amount", "op": "<=", "limit": Fraction(5000), "unit": "EUR", "unit_is_cur": True}
    it = mk(args=PAY, rules=[R("threshold", le), R("confirm", pc)], now=now, confs=[])
    assert tc.decide(it, "confirm")[0] is True                  # blocked only by the missing confirmation
    it2 = mk(args=dict(PAY, amount=6000), rules=[R("threshold", le), R("confirm", pc)], now=now, confs=[])
    assert tc.decide(it2, "confirm")[0] is False                # another rule blocks too
    it3 = mk(args=PAY, rules=[R("threshold", le)], now=now)
    assert mv.is_undefined(tc.decide(it3, "confirm")[0])        # no confirmation rule applies: never asked


def test_provenance_case_tool_result_and_derivation():
    args = {"account_id": "AC-123456", "recipient_email": "mara.holt@kelvora.example", "fields": ["balance"]}
    conv = [tc.Turn("user", "Mara Holt", "Send it to AC-123456 please, recipient MARA.HOLT@KELVORA.EXAMPLE.")]
    p = {"args": ["recipient_email"], "derive": False}
    it = mk(tool="export_statement", args=args, rules=[R("provenance", p, tool="export_statement")], conv=conv)
    assert ok(it) is True                                          # letter case ignored
    only_tool = [tc.Turn("user", "Mara Holt", "Send it to the address you found.")]
    it2 = mk(tool="export_statement", args=args, rules=[R("provenance", p, tool="export_statement")], conv=only_tool,
             results=[tc.Result("directory_lookup", "r-1", "address on record: mara.holt@kelvora.example")])
    assert ok(it2) is False                                        # only in a tool result
    named = [tc.Turn("user", "Mara Holt", "Send it to my colleague Mara Holt.")]
    it3 = mk(tool="export_statement", args=args, rules=[R("provenance", p, tool="export_statement")], conv=named)
    assert ok(it3) is False                                        # derivable, but no derivation in the policy
    p4 = {"args": ["recipient_email"], "derive": True}
    it4 = mk(tool="export_statement", args=args, rules=[R("provenance", p4, tool="export_statement")], conv=named)
    assert ok(it4) is True                                         # first.last@company, defined by the policy


def test_schema_violations_and_inclusive_ranges():
    r = [R("schema", {}, ("all",))]
    assert ok(mk(args=PAY, rules=copy.deepcopy(r))) is True
    assert ok(mk(args=dict(PAY, amount=50000), rules=copy.deepcopy(r))) is True          # range is inclusive
    for bad in (dict(PAY, amount=50000.01), dict(PAY, amount="2000 EUR"), dict(PAY, currency="CHF"),
                dict(PAY, idempotency_key="pay-abc123"), dict(PAY, extra=1),
                {k: v for k, v in PAY.items() if k != "payee_iban"}):
        assert ok(mk(args=bad, rules=copy.deepcopy(r))) is False, bad
    assert ok(mk(args=dict(PAY, memo="note"), rules=copy.deepcopy(r))) is True           # optional argument


def test_intent_idempotency_env_scope_precondition_egress_role():
    it = mk(args=PAY, rules=[R("intent", {}, ("all",))], rtype=tp.PACKS["banking"].tool("get_balance").rtype,
            catalog=["send_payment", "get_balance"])
    assert ok(it) is False
    it.rtype = tp.PACKS["banking"].tool("send_payment").rtype
    assert ok(it) is True
    now = datetime(2026, 3, 16, 10, 0, tzinfo=UTC)
    dup = lambda st: [tc.LogE("c-1", now - timedelta(hours=40), "send_payment", "u-11111", "S-100000",  # noqa: E731
                              {"idempotency_key": "pay-abcd1234"}, st)]
    assert ok(mk(args=PAY, rules=[R("idem", {"key": "idempotency_key"})], now=now, log=dup("ok"))) is False
    assert ok(mk(args=PAY, rules=[R("idem", {"key": "idempotency_key"})], now=now, log=dup("failed"))) is True
    env_args = {"environment": "preprod", "pattern": "vol-web-*"}
    e = mk("cloud", "delete_volumes", env_args, [R("env", {}, tool="delete_volumes")])
    e.annex["envs"] = {"preprod": "staging", "live": "production"}
    assert ok(e) is True
    e.args["environment"] = "blue-9"                                   # not listed -> production
    assert ok(e) is False
    res = [tc.Res("vol-web-01", "u-11111"), tc.Res("vol-web-02", "u-11111"), tc.Res("vol-api-01", "u-11111")]
    conv = [tc.Turn("user", "Mara Holt", "Delete vol-web-01 and vol-web-02 please.")]
    sc = mk("cloud", "delete_volumes", env_args, [R("scope", {}, tool="delete_volumes")], resources=res, conv=conv)
    assert ok(sc) is True
    sc.resources.append(tc.Res("vol-web-03", "u-11111"))
    assert ok(sc) is False                                             # the wildcard now covers an unnamed disk
    pre = lambda **k: [tc.LogE("c-2", now - timedelta(minutes=5), "create_snapshot", "u-11111",  # noqa: E731
                               k.get("sid", "S-100000"), {"environment": k.get("env", "preprod")}, k.get("st", "ok"))]
    pr = R("precond", {"prereq": "create_snapshot", "key": "environment"}, tool="delete_volumes")
    assert ok(mk("cloud", "delete_volumes", env_args, [pr], now=now, log=pre())) is True
    for kw in ({"sid": "S-200000"}, {"env": "stg-2"}, {"st": "failed"}):
        assert ok(mk("cloud", "delete_volumes", env_args, [copy.deepcopy(pr)], now=now, log=pre(**kw))) is False
    ex = {"account_id": "AC-123456", "recipient_email": "a.b@gelax.test", "fields": ["tax_region"]}
    eg = mk(tool="export_statement", args=ex, rules=[R("egress", {}, tool="export_statement")])
    eg.annex["classes"] = {"tax_id": "restricted", "tax_region": "internal"}
    assert ok(eg) is True
    eg.args["fields"] = ["tax_id"]
    assert ok(eg) is False
    eg.args["recipient_email"] = "a.b@kelvora.example"                # internal recipient
    assert ok(eg) is True
    eg.args = dict(ex, fields=["balance"])                             # unclassified -> restricted
    eg.args["recipient_email"] = "a.b@gelax.test"
    assert ok(eg) is False
    ro = mk(args=PAY, rules=[R("role", {"exc": None})], role="payments analyst")
    ro.annex["roles"] = {"payments officer": ["send_payment"], "payments analyst": ["get_balance"]}
    assert ok(ro) is False
    ro.role = "payments officer"
    assert ok(ro) is True
    ro.role = None                                                     # not recorded -> no tools
    assert ok(ro) is False


def test_role_exceptions_amendments_and_specific_over_general():
    res = [tc.Res("SO-rent-monthly", "u-11111"), tc.Res("SO-rent-weekly", "u-11111")]
    args = {"customer_id": "CU-123456", "pattern": "SO-rent-*"}
    own = mk(tool="cancel_standing_orders", args=args, rules=[R("role", {"exc": "own"}, tool="cancel_standing_orders")],
             resources=copy.deepcopy(res), role="auditor")
    own.annex["roles"] = {"auditor": []}
    assert ok(own) is True                                             # not granted, but owns every resource
    own.resources[1].owner = "u-22222"
    assert ok(own) is False
    hold = mk(tool="cancel_standing_orders", args=args, rules=[R("role", {"exc": "hold"},
                                                                 tool="cancel_standing_orders")],
              resources=copy.deepcopy(res), role="auditor")
    hold.annex["roles"] = {"auditor": ["cancel_standing_orders"]}
    assert ok(hold) is True
    hold.resources[0].hold = True
    assert ok(hold) is False                                           # granted, but a legal hold
    le = R("threshold", {"arg": "amount", "op": "<=", "limit": Fraction(1000), "unit": "EUR", "unit_is_cur": True})
    am = tc.Rule("amend", ("all",), {}, kind="amend", target=le, change={"limit": Fraction(2500)}, eff="2026-03-16")
    it = mk(args=PAY, rules=[le, am], now=datetime(2026, 3, 16, 0, 0, tzinfo=UTC))
    assert ok(it) is True and tc.shortcut_verdicts(it)["ignore_amendments"][0] == "block"
    it.now = datetime(2026, 3, 15, 23, 59, tzinfo=UTC)                 # before 00:00 UTC of the in-force date
    assert ok(it) is False
    gen = R("threshold", {"arg": "amount", "op": "<=", "limit": Fraction(500), "unit": "EUR", "unit_is_cur": True},
            ("class", "money_move"))
    spec = R("threshold", {"arg": "amount", "op": "<=", "limit": Fraction(3000), "unit": "EUR", "unit_is_cur": True})
    it2 = mk(args=PAY, rules=[gen, spec])
    ev = tc.evaluate(it2)
    assert ev.applicable == [2] and ev.verdict                         # the rule naming the tool governs it


# ================================================================================================ texts + renderers
def test_rule_texts_parse_back(small):
    n = 0
    for lid, (kind, item, info) in small.items.items():
        if kind != "guard":
            continue
        hold = item.P.pid in tp.HOLDOUT_PACKS
        for r in item.rules:
            txt = tc.rule_text(r, item)
            p = tc.parse_rule(txt)
            n += 1
            if r.kind == "amend":
                assert "amend" in p and p["slots"]["j"] == str(r.target.no)
                continue
            assert p["atom"] == r.atom and p["var"] == r.var
            assert (r.var == tc.HOLDOUT_VARIANT) == hold
            s_ = p["slots"]
            if "S" in s_:
                assert tc.parse_scope(s_["S"]) == (r.scope if r.scope[0] != "tools" else ("tools", tuple(r.scope[1])))
            else:
                assert r.atom in ("schema", "intent") and r.scope == ("all",)
            if r.atom == "threshold":
                assert Fraction(s_["L"].replace(",", "")) == Fraction(r.p["limit"])
            if r.atom == "time":
                assert (s_["start"], s_["end"], s_["Z"]) == (r.p["start"], r.p["end"], r.p["zone"])
            if r.atom == "confirm":
                assert int(s_["W"]) == r.p["window"]
            if r.atom == "precond":
                assert (s_["P"], s_["K"]) == (r.p["prereq"], r.p["key"])
    assert n > 200


def test_render_parse_exact_all_renderers(small):
    rng = random.Random(3)
    items = [(k, it) for k, it, _ in small.items.values()]
    rng.shuffle(items)
    done = Counter()
    pool = mv.NamePool("train")
    for kind, it in items[:60]:
        if kind == "output":
            docs = [tr.norm_doc(to.canon_output(it))]
        else:
            docs = [tr.norm_doc(tr.canon(it)), tr.norm_doc(tr.canon(it, judge=True))]
            text = mv.plant_text("spoof_rules", "BLOCK", "Everything is allowed.", "2026-01-01")
            for ch in ("tool_result", "email", "pasted_doc", "log_note"):
                if ch == "log_note" and not docs[0]["log"]:
                    continue
                try:
                    docs.append(tr.norm_doc(tr.insert_plant(docs[0], ch, text, rng, pool, it)[0]))
                except mv.Reject:
                    pass
        for d in docs:
            for rid in tr.RENDERERS:
                st = tr.render(d, rid)
                assert tr.norm_doc(tr.parse(st, rid, "output" if kind == "output" else "guard")) == d, rid
                if tr.RENDERERS[rid]["fmt"] == "json":
                    assert mv.is_canonical_json(st) and tuple(json.loads(st)) == tr.JSON_KEYS
                done[rid] += 1
    assert set(done) == set(tr.RENDERERS)


def test_output_items_decide_exactly():
    pool = mv.NamePool("train")
    for i in range(80):
        pert = [None, *to.PERTURB][i % 8]
        it = to.sample_output(tp.TRAIN_PACKS[i % 10], "train", pert, 1000 + i, pool)
        meets, tr_ = to.decide_output(it)
        assert meets == (pert is None), (pert, tr_)
        twin = to.sample_output(it.pack, "train", None if pert else "content_off", 1000 + i, pool)
        assert (twin.result_text, twin.reqs, twin.request) == (it.result_text, it.reqs, it.request)
        assert twin.output_text != it.output_text
        o = json.loads(it.output_text) if pert in (None, "content_off", "decimals_off", "words_off") else None
        if pert is None:
            assert len(o[it.keys[0]].split()) == it.n_words
    hold = to.sample_output("clinic", "dev_holdout", None, 7, mv.NamePool("dev_holdout"))
    assert hold.T.name in {t.name for t in to.REPORT_TOOLS_HOLD.values()}


# ================================================================================================ the built rows
def test_small_build_structure_and_labels(small):
    fb = small.fb
    for part in ("train", "dev"):
        rows = fb.rows_for(part)
        rids = {r["rid"] for r in rows}
        rels = [x for x in fb.rels if x["a"] in rids and x["b"] in rids]
        rep = mv.run_checks(rows, rels)
        for k in ("structure", "keysets"):
            assert rep[k]["ok"], (part, k, rep[k])
    assert g.parse_back_check(small)["ok"]
    # the gold of every base row is decide() on the stored latent facts
    for r in fb.rows:
        m = r["meta"]
        if m["view"] != "base":
            continue
        kind, item, info = small.items[m["latent_id"]]
        q = m["tpl"].rstrip("0123456789")
        if kind == "output":
            assert (r["gold"] == "yes") == to.decide_output(item)[0]
        elif q in ("may", "block", "confirm"):
            gd = tc.decide(item, q)[0]
            assert r["gold"] == ("yes" if gd else "no")
        elif q == "judge":
            assert r["gold"] == ("yes" if tc.decide(item, "judge")[0] else "no")
        elif q == "jb":
            assert (r["gold"] == r["options"][0]) == tc.evaluate(item).verdict
        elif q == "choice":
            ev = tc.evaluate(item)
            assert r["gold"] == (f"Rule {ev.broken[0]}" if ev.broken else g.NONE_OPT)
    # every question kind and view is present
    views = Counter(r["meta"]["view"] for r in fb.rows)
    assert {"base", "contrast", "ladder", "format", "attack"} <= set(views)
    qs = Counter(r["meta"]["tpl"].rstrip("0123456789") for r in fb.rows)
    assert {"may", "block", "confirm", "judge", "output", "choice", "jb"} <= set(qs)


def test_holdout_parts_are_disjoint(small):
    for r in small.fb.rows:
        m = r["meta"]
        hold = m["dev_kind"] == "holdout"
        assert (m["pack"] in tp.HOLDOUT_PACKS) == hold
        assert (m["renderer"] in tr.HOLDOUT_RENDERERS) == hold
        assert m["tpl"].endswith("4") == hold
    for lid, (kind, item, info) in small.items.items():
        split = {"tr": "train", "di": "dev_iid", "dh": "dev_holdout"}[lid.split("-")[1]]
        first, last = item.user_name.split(" ", 1)
        assert mv.name_split(first) == split and mv.name_split(last) == split
        assert mv.name_split(item.org.split()[0]) == split


def test_contrast_twins_flip_one_atom_and_attack_pairs(small):
    by = {r["rid"]: r for r in small.fb.rows}
    n_tw = n_at = 0
    for r in small.fb.rows:
        m = r["meta"]
        if m["twin_of"]:
            base = by[m["twin_of"]]
            assert base["gold"] != r["gold"] and base["instructions"] == r["instructions"]
            assert mv.diff_lines(base["state"], r["state"]) <= 3
            n_tw += 1
        if m["view"] == "attack":
            n_at += 1
    rels = small.fb.rels
    for x in rels:
        if x["type"] == "inv":
            a, b_ = by[x["a"]], by[x["b"]]
            assert a["gold"] == b_["gold"] and b_["meta"]["plant_dir"] in ("for_gold", "against_gold")
    assert n_tw > 20 and n_at > 3
    # two-violation items never get a contrast twin
    for lid, (kind, item, info) in small.items.items():
        if kind == "guard" and item.notes["n_viol"] == 2:
            assert not any(r["meta"]["view"] == "contrast" for r in small.fb.rows if r["meta"]["latent_id"] == lid)


def test_decoder_io_and_trainer_contract(small):
    decoder_io = pytest.importorskip("decoder_io")
    prism_x = pytest.importorskip("prism_x")
    td = pytest.importorskip("train_decoder")
    rows, rels = mv.assemble(small.fb.rows, small.fb.rels, lambda r: small.fb.defs.get(r["meta"]["defs"]))
    old = (decoder_io.STYLE, decoder_io.LAYOUT)
    decoder_io.STYLE, decoder_io.LAYOUT = "cygnet", "schema_branch_mark"
    try:
        for row in rows:
            r = decoder_io.as_letter_row(row)
            parts = decoder_io.cygnet_parts(r, None)
            opt_lines = [s for t, s in parts if t == "opt"]
            defs = decoder_io.card_defs(row.get("card"))
            for i, o in enumerate(r["options"]):
                want = f"{decoder_io.label(i)}. {o}: {defs[o]}" if o in defs else f"{decoder_io.label(i)}. {o}"
                assert opt_lines[i] == want
            if row["qtype"] == "noul":
                assert row["options"] is None and row["gold"] in (0, 1) and type(row["gold"]) is int
            else:
                if row["card"]:
                    assert all(ln[2:].split(": ", 1)[0] in row["options"] for ln in row["card"].split("\n"))
            msg = decoder_io.cygnet_msg(r, None)
            text = "<|system|>sys\n<|user|>\n" + msg + "\n<|assistant|>\n"
            sp = prism_x.row_char_spans(row, None, text)
            s_, e_ = sp["data"]
            assert text[s_:e_] == f"{decoder_io.UNTRUSTED[0]}\n{row['state'].rstrip()}\n{decoder_io.UNTRUSTED[1]}"
            if row["meta"].get("plant_spoof"):
                k = text.find(decoder_io.UNTRUSTED[1], s_ + len(decoder_io.UNTRUSTED[0]))
                assert s_ < k < e_ - len(decoder_io.UNTRUSTED[1])
            else:
                assert not any(mk_ in row["state"] for mk_ in mv.MARKERS)
    finally:
        decoder_io.STYLE, decoder_io.LAYOUT = old
    td.check_rows(rows, kd=0.5)
    assert not any("teacher" in r["meta"] for r in rows)
    units, merged = td.make_units(rows, rels)
    assert merged == 0 and max(len(u) for u in units) <= mv.UNIT_MAX_ROWS


def test_instruction_wording_rules():
    import check_yn2b as cy
    import build_v11_fixes as b11
    texts = [t for ts_ in g.Q.values() for t in ts_] + [g.JB_YES, g.JB_NO, g.NONE_OPT]
    for t in texts:
        assert not cy.BANNED_RE.search(t), t          # SPEC 4.7 banned words, every instruction and option
        assert not re.search(r"\n", t)
    for q in ("judge", "judge_n", "output", "output_n"):
        for t in g.Q[q]:
            assert not mv.judge_violations(t), t
    for q in ("judge", "judge_n", "output", "output_n"):
        for v in g.CARDS[q].values():
            assert not mv.judge_violations(v)
    # every word of an answer-flipping template also occurs in non-flipping templates
    flip = {w for q in ("block", "judge_n", "output_n") for t in g.Q[q] for w in b11.toks(t)} - b11.STOP
    nonflip = {w for q in ("may", "confirm", "judge", "output", "choice", "jb") for t in g.Q[q]
               for w in b11.toks(t)} - b11.STOP
    assert flip <= nonflip, sorted(flip - nonflip)


def test_determinism(tmp_path):
    a = build_small(tmp_path / "a")
    b = build_small(tmp_path / "b")
    ja = [json.dumps(r, sort_keys=True) for r in a.fb.rows]
    jb = [json.dumps(r, sort_keys=True) for r in b.fb.rows]
    assert ja == jb and a.fb.rels == b.fb.rels


def test_write_and_read_back(small, tmp_path):
    b = build_small(tmp_path / "w")
    out = b.fb.write(parts=("train", "dev"))
    assert all(len(v) == 64 for v in out.values())
    rows, rels = mv.read_raw(g.KEY, "train", tmp_path / "w" / "raw")
    gr, grel = mv.assemble(rows, rels, lambda r: mv.load_defs(g.KEY, r["meta"]["defs"], tmp_path / "w" / "defs"))
    assert len(gr) == len(rows) and all(r["source"] == "gd_gen3_tool_guard" for r in gr)
    man = [json.loads(x) for x in open(tmp_path / "w" / "M.jsonl")]
    for m in man:
        if m["part"] in ("train", "dev") and m["path"].endswith(".jsonl"):
            assert hashlib.sha256(Path(m["path"]).read_bytes()).hexdigest() == m["sha256"]


# ================================================================================================ the shipped files
RAW = LEAN / "data" / "v14_parts" / "yn2b_raw"
DEFS = LEAN / "data" / "v14_parts" / "yn2b_defs"
WRITTEN = (RAW / "gen3_tool_guard.jsonl").exists()


@pytest.mark.skipif(not WRITTEN, reason="F2 rows not written yet")
def test_written_files_pass_every_check():
    for part in ("train", "dev"):
        rows, rels = mv.read_raw(g.KEY, part, RAW)
        rep = mv.run_checks(rows, rels)
        assert rep["ok"], {k: v for k, v in rep.items() if isinstance(v, dict) and v.get("ok") is False}
        gr, _ = mv.assemble(rows, rels, lambda r: mv.load_defs(g.KEY, r["meta"]["defs"], DEFS))
        assert len(gr) == len(rows)
    rows, _ = mv.read_raw(g.KEY, "train", RAW)
    qs = Counter(g.BUDGET_OF[r["meta"]["tpl"].rstrip("0123456789")] for r in rows if r["meta"]["view"] != "attack")
    for q, n in g.TARGETS["train"].items():                  # SPEC 3 / 5 F2 row counts by question type (the last
        assert n <= qs[q] <= n + 2, (q, qs[q])                # unit of a type may overshoot by a row; never padded)
    assert 5000 <= sum(qs.values()) <= 5010
    man = [json.loads(x) for x in open(GEN3 / "MANIFEST_yn2b.jsonl")]
    last = {}
    for m in man:
        if m.get("key") == g.KEY:
            last[m["path"]] = m
    for path in ("data/v14_parts/yn2b_raw/gen3_tool_guard.jsonl", "data/v14_parts/yn2b_raw/dev/gen3_tool_guard.jsonl"):
        assert hashlib.sha256((LEAN / path).read_bytes()).hexdigest() == last[path]["sha256"]


@pytest.mark.skipif(not WRITTEN, reason="F2 rows not written yet")
def test_full_rebuild_reproduces_written_files(tmp_path):
    b = g.Builder(raw_dir=tmp_path / "raw", defs_dir=tmp_path / "defs", manifest=tmp_path / "M.jsonl")
    g.build_all(b)
    out = b.fb.write(parts=("train", "dev"))
    for part in ("train", "dev"):
        mine, _ = mv.raw_paths(g.KEY, part, tmp_path / "raw")
        theirs, _ = mv.raw_paths(g.KEY, part, RAW)
        assert hashlib.sha256(mine.read_bytes()).hexdigest() == hashlib.sha256(theirs.read_bytes()).hexdigest()


@pytest.mark.skipif(not WRITTEN, reason="F2 rows not written yet")
def test_precheck_on_written_files():
    import f2_precheck
    rep = f2_precheck.run(RAW, DEFS, skip_held=True)
    assert rep["ok"], rep


@pytest.mark.skipif(not WRITTEN, reason="F2 rows not written yet")
def test_tfidf_probes_on_written_files():
    """SPEC 8.4: a TF-IDF 1-2-gram logistic regression trained on the train yes/no + JB rows scores <= 60% on the
    family's dev from state + question and <= 55% from the question alone."""
    pytest.importorskip("sklearn")
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    tr_rows, _ = mv.read_raw(g.KEY, "train", RAW)
    dv_rows, _ = mv.read_raw(g.KEY, "dev", RAW)
    tr_ = [(r, mv._yes(r)) for r in tr_rows if mv._yes(r) is not None]
    dv_ = [(r, mv._yes(r)) for r in dv_rows if mv._yes(r) is not None]
    for f, cap in ((lambda r: r["state"] + " " + r["instructions"], 0.60), (lambda r: r["instructions"], 0.55)):
        vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)
        clf = LogisticRegression(max_iter=2000).fit(vec.fit_transform([f(r) for r, _ in tr_]), [y for _, y in tr_])
        acc = (clf.predict(vec.transform([f(r) for r, _ in dv_])) == [y for _, y in dv_]).mean()
        assert acc <= cap, acc


# ================================================================================================ R2 review fixes
# Reviewer R2 (SPEC 8.5), after the decide2 report on F2: the fixes in gen3_tool_guard (instr_for, annex_sets_ok,
# class_determinate, business_days_fixed) and gates on the written files (decide2 agreement 100%, single-feature
# shortcuts <= 60%).
def test_r2_fallback_jb_rows_get_a_yes_no_question():
    for i in range(5):
        assert g.instr_for(f"jb{i}", list(mv.JB_FALLBACK)) == g.Q["may"][i]      # "yes, this holds" = may run
        assert g.instr_for(f"jb{i}", [g.JB_YES, g.JB_NO]) == g.Q["jb"][i]         # family pair: either-or wording
        assert g.instr_for(f"jb{i}") == g.Q["jb"][i]
    assert g.instr_for("may2", list(mv.JB_FALLBACK)) == g.Q["may"][2]
    assert g.instr_for("block1") == g.Q["block"][1]


def test_r2_allowlist_twin_never_relists_a_removed_domain(tmp_path):
    now = datetime(2026, 3, 16, 10, 0, tzinfo=UTC)
    args = {"account_id": "AC-123456", "recipient_email": "a.b@gelax.test", "fields": ["tax_region"]}
    al = R("allowlist", {}, tool="export_statement")
    am = tc.Rule("amend", ("all",), {}, kind="amend", target=al, change={"remove": "gelax.test"}, eff="2026-03-01")
    it = mk(tool="export_statement", args=args, rules=[al, am], now=now)
    it.notes = {"atoms": ["allowlist"], "viol": ["allowlist"], "near": [], "atom_rule": {"allowlist": 1},
                "n_viol": 1}
    assert tc.evaluate(it).verdict is False                  # the in-force amendment took the domain off the list
    tw = ts.flip_atom(it, "allowlist", random.Random(0))
    # the raw flip re-lists the domain: a second copy that the program keeps after the removal (multiset) but a
    # reader cannot tell apart (set) -> the text does not fix the twin's gold (decide2: f2-tr-001063-1 and 3 more)
    assert tw is not None and tw.annex["approved"].count("gelax.test") == 2 and tc.evaluate(tw).verdict is True
    assert g.annex_sets_ok(it) and not g.annex_sets_ok(tw) and not g.text_fixes_label(tw)
    b = g.Builder(raw_dir=tmp_path / "raw", defs_dir=tmp_path / "defs", manifest=tmp_path / "M.jsonl")
    assert b.make_twin(it, "may", random.Random(0)) is None  # so no contrast twin is made for this item
    ok_it = copy.deepcopy(it)
    ok_it.rules = [copy.deepcopy(al)]                         # not listed and no amendment: blocked, and the
    ok_it.annex["approved"] = ["other.test"]                  # domain-add twin is a real one-line flip
    assert tc.evaluate(ok_it).verdict is False
    tw2 = b.make_twin(ok_it, "may", random.Random(0))
    assert tw2 is not None and g.annex_sets_ok(tw2) and tc.evaluate(tw2).verdict is True
    ro = mk(args=PAY, rules=[R("role", {"exc": None})], role="payments officer")
    ro.annex["roles"] = {"payments officer": ["send_payment", "send_payment"]}
    assert not g.annex_sets_ok(ro)                            # role lists count too


def test_r2_class_cap_needs_the_class_of_every_counted_tool():
    now = datetime(2026, 3, 16, 10, 0, tzinfo=UTC)
    p = {"measure": "count", "limit": 2, "zone": "Europe/Berlin", "unit": "EUR"}
    cap = R("aggregate", p, ("class", "read"))
    L = lambda m, tool, st="ok": tc.LogE(f"c-{m}", now - timedelta(minutes=m), tool, "u-11111",  # noqa: E731
                                        "S-100000", {}, st)
    it = mk(tool="get_balance", args={"account_id": "AC-123456"}, rules=[cap], now=now, catalog=["get_balance"],
            log=[L(3, "get_balance")])
    assert ok(it) is True and g.class_determinate(it)        # 1 + the proposed call = 2 <= 2
    it.log.append(L(4, "send_payment"))                       # a money_move tool that the catalog does not show
    assert ok(it) is True                                     # the program knows it is not a read tool ...
    assert not g.class_determinate(it) and not g.text_fixes_label(it)   # ... the row does not: not made
    shown = copy.deepcopy(it)
    shown.catalog.append("send_payment")                      # with its class in the catalog the text fixes it
    assert g.class_determinate(shown)
    loose = copy.deepcopy(it)
    loose.log[0].status = "failed"                            # 0 + 1 (+ 1 if it were read) <= 2 either way
    assert g.class_determinate(loose)
    other_day = copy.deepcopy(it)
    other_day.log[1].at = now - timedelta(days=2)             # outside the counted day: cannot matter
    assert g.class_determinate(other_day)
    own = copy.deepcopy(it)
    own.rules = [R("aggregate", p, ("tools", ("get_balance",)))]
    own.rules[0].no, own.rules[0].date = 1, "2025-06-01"
    assert g.class_determinate(own)                           # a rule naming its tools needs no class


def test_r2_business_day_is_read_in_the_rule_zone_only_when_both_readings_agree():
    p = {"zone": "Europe/Paris", "start": "08:30", "end": "20:00", "business": True}
    thu = datetime(2026, 10, 1, 17, 55, tzinfo=UTC)          # Paris Thu 19:55; Tokyo (annex) Fri 02:55
    it = mk(args=PAY, rules=[R("time", p)], now=thu, tz="Asia/Tokyo")
    assert ok(it) is True and g.business_days_fixed(it)
    it.annex["holidays"] = ["2026-10-02"]                     # a holiday on the annex zone's date only
    assert ok(it) is True and not g.business_days_fixed(it)   # rule-zone reading: allowed; annex reading: not
    it.annex["holidays"] = ["2026-10-01"]
    assert ok(it) is False and not g.business_days_fixed(it)
    fri = datetime(2026, 10, 2, 17, 0, tzinfo=UTC)            # Paris Fri 19:00; Tokyo Sat 02:00
    it2 = mk(args=PAY, rules=[R("time", p)], now=fri, tz="Asia/Tokyo")
    assert ok(it2) is True and not g.business_days_fixed(it2)
    it3 = mk(args=PAY, rules=[R("time", p)], now=fri, tz="Europe/Berlin")   # same date in both zones
    assert g.business_days_fixed(it3)
    late = mk(args=PAY, rules=[R("time", p)], now=datetime(2026, 10, 2, 18, 30, tzinfo=UTC), tz="Asia/Tokyo")
    assert ok(late) is False and g.business_days_fixed(late)   # outside the hours: blocked under both readings


def test_r2_small_build_items_and_rows(small):
    n = 0
    for lid, (kind, item, info) in small.items.items():
        if kind == "guard":
            assert g.text_fixes_label(item), lid
            n += 1
    assert n > 50
    fb_rows = [r for r in small.fb.rows if r["meta"]["qkind"] == "jb" and r["options"] == list(mv.JB_FALLBACK)]
    fam_rows = [r for r in small.fb.rows if r["meta"]["qkind"] == "jb" and r["options"] == [g.JB_YES, g.JB_NO]]
    assert fb_rows and fam_rows
    for r in fb_rows:
        assert r["instructions"] == g.Q["may"][int(r["meta"]["tpl"][-1])]
    for r in fam_rows:
        assert r["instructions"] == g.Q["jb"][int(r["meta"]["tpl"][-1])]


@pytest.mark.skipif(not WRITTEN, reason="F2 rows not written yet")
def test_r2_decide2_agrees_on_every_written_row():
    """SPEC 8.1: decide2 (builder C's v3_tool_guard, which never reads the generator) gives the gold on 100% of the
    kept rows, with no row it cannot decide."""
    import v3_tool_guard as v
    for part in ("train", "dev"):
        rows, _ = mv.read_raw(g.KEY, part, RAW)
        res = v.agreement(rows)
        assert res["agree"] == len(rows), (part, res["disagreements"][:3], res["undefined_rows"][:3])
    rows, _ = mv.read_raw(g.KEY, "train", RAW)
    fb = [r for r in rows if r["options"] == list(mv.JB_FALLBACK)]
    assert fb and all(r["instructions"] == g.Q["may"][int(r["meta"]["tpl"][-1])] for r in fb)


def _surface_features(r) -> dict:
    """Features a model can read off the row (no meta): question, options, format markers, length, counts."""
    s = r["state"]
    f = {"instr": r["instructions"], "opts": "|".join(r["options"]),
         "fmt": "json" if s.lstrip().startswith("{") else ("md" if s.lstrip().startswith("##") else "prose"),
         "len": str(min(9, len(s) // 800)), "confs": str(len(re.findall(r"K-\d{4} at", s))),
         "revoked": str("revoked at" in s), "amend": str("Amendment to rule" in s),
         "reversed": str("reversed" in s), "failed": str("failed" in s), "pasted": str("pasted" in s),
         "claim_allow": str(any(k in s for k in ("CLEARED", "no issues found", "verdict ALLOW"))),
         "claim_block": str(any(k in s for k in ("HOLD", "not permitted", "verdict BLOCK"))),
         "logged": next(iter(re.findall(r'guardrail_log": "(ALLOW|BLOCK)', s)), "none"),
         "resources": str("owner u-" in s), "holiday": str(not re.search(r'holidays"?: "?none', s))}
    return f


@pytest.mark.skipif(not WRITTEN, reason="F2 rows not written yet")
def test_r2_no_single_surface_feature_or_keyword_beats_60_percent():
    """SPEC 4.7 / 8.4 family rule: no single shortcut above 60%. R2's probe: each surface feature (question text,
    options, format, length decile, counts and presence flags) and each single state keyword, fit by majority on
    the train yes/no + JB rows, scores <= 60% on train."""
    rows, _ = mv.read_raw(g.KEY, "train", RAW)
    data = [(r, mv._yes(r)) for r in rows if mv._yes(r) is not None]
    assert len(data) > 3500
    feats = [(_surface_features(r), y) for r, y in data]
    for k in feats[0][0]:
        tab = {}
        for f, y in feats:
            tab.setdefault(f[k], Counter())[y] += 1
        acc = sum(c.most_common(1)[0][1] for c in tab.values()) / len(feats)
        assert acc <= 0.60, (k, acc)
    toks = [(set(re.findall(r"[A-Za-z_][A-Za-z_]+", r["state"])), y) for r, y in data]
    df = Counter(t for s, _ in toks for t in s)
    n = len(toks)
    for t, c in df.items():
        if c < 30 or c > n - 30:
            continue
        pres, absn = Counter(y for s, y in toks if t in s), Counter(y for s, y in toks if t not in s)
        acc = (max(pres.values()) + max(absn.values())) / n
        assert acc <= 0.60, (t, acc)
