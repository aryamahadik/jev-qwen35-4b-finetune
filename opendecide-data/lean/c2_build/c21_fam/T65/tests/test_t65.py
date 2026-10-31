"""T65 CPU tests: templates (render vs label engine), twin pairs per kind, canary witnesses through PyEval (the executor interface), record assembly, the check-at-generation
pipeline (solver B absent in tests = noted; production raises), CWE head rows, GV5 retirement, gates. Nothing generated is executed by this process: PyEval interprets the text."""
import ast
import collections
import os

import pytest

from LP_COMMON import pipeline as pl
from LP_COMMON import sandbox_iface as S
from T65 import checked, config as C, dryrun, gates, generator as G, roundtrip, schema, solver_a, specs as SP, templates as T

FAMDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _ctx(seed=1):
    return G.Ctx(seed=seed, standin=True)


def _cell(cls, kind, tr=(), noise=False):
    return {"cls": cls, "pair_kind": kind, "transforms": list(tr), "noise": noise}


def _pair(cls, kind, seed=1, **kw):
    return SP.make_pair_specs(_ctx(seed), {"gid": "g%d" % seed, "seed": "s%d" % seed}, _cell(cls, kind, **kw))


@pytest.fixture(scope="module")
def dry():
    return dryrun.dry_rows(600, seed=7)


def test_config_shape():
    assert sum(C.CLASS_PAIRS.values()) == C.PAIRS == 300
    assert set(C.CLASS_PAIRS) == set(C.CLASSES)
    assert all(p in C.PAYLOADS for p in C.PAY_OF.values())


@pytest.mark.parametrize("cls", C.CLASSES)
def test_plain_pair_labels_and_parse(cls):
    y, n = _pair(cls, "plain", seed=3)
    assert (y["label"], n["label"]) == ("YES", "NO")
    for s in (y, n):
        ast.parse(s["source_text"])
    assert y["edit_lines"] == n["edit_lines"] and y["edit_lines"] <= 6


@pytest.mark.parametrize("ds", C.DS_IDS)
@pytest.mark.parametrize("cls", ["CWEC-22", "CWEC-79", "CWEC-327"])
def test_decoy_pairs(cls, ds):
    y, n = _pair(cls, "decoy:" + ds, seed=5)
    assert (y["label"], n["label"]) == ("YES", "NO")
    assert y["pair_kind"] == "decoy:" + ds


@pytest.mark.parametrize("cls", C.DYNAMIC)
def test_ns_pairs_dynamic(cls):
    for ns in ("NS-1", "NS-2", "NS-3"):
        y, n = _pair(cls, "ns:" + ns, seed=2)
        assert (y["label"], n["label"]) == ("YES", "NO")


@pytest.mark.parametrize("cls", ["CWEC-78", "CWEC-89"])
def test_ns4_only_for_78_89(cls):
    y, n = _pair(cls, "ns:NS-4", seed=2)
    assert n["label"] == "NO"
    with pytest.raises(SP.Reject):
        _pair("CWEC-22", "ns:NS-4", seed=2)


@pytest.mark.parametrize("cls", C.STATIC)
def test_static_classes_reject_ns2(cls):
    with pytest.raises(SP.Reject):
        _pair(cls, "ns:NS-2")


@pytest.mark.parametrize("cls", C.DYNAMIC)
def test_witness_agrees_with_spec_engine(cls):
    y, n = _pair(cls, "plain", seed=4)
    assert SP.label_from_witness(y["witness"]) == "YES" and SP.label_from_witness(n["witness"]) == "NO"
    assert y["witness"]["runs"] >= 3 and y["witness"]["payload_id"] == C.PAY_OF[cls]


def test_witness_mismatch_is_rejected():
    class Lying(S.SimExecutor):
        def run(self, reqs):
            out = super().run(reqs)
            for r in out:
                r["stdout"] = r["stdout"].replace("canarytoken", "zzz")
            return out
    ctx = G.Ctx(seed=1, standin=True, executor=Lying())
    with pytest.raises(SP.Reject):
        SP.make_pair_specs(ctx, {"gid": "g", "seed": "s"}, _cell("CWEC-78", "plain"))


def test_effect_requires_exact_canary():
    assert SP.effect("CWEC-22", ["ok", "CANARY-FILE-CONTENT"]) and not SP.effect("CWEC-22", ["ok", "other"])
    assert SP.effect("CWEC-601", ["ok", "https://canary.example/x"]) and not SP.effect("CWEC-601", ["ok", "https://canary.example.evil.org/x"][:1] + ["/home"])
    assert not SP.effect("CWEC-79", ["err", "x"])


def test_label_from_witness_none_when_not_ok():
    assert SP.label_from_witness({"ok": False, "benign_ok": True, "effect": True}) is None


def test_plan_counts_and_kinds():
    plan = G.build_plan(600, seed=1, oversample=False)
    assert len(plan) == 300
    kinds = collections.Counter(g["cell"]["pair_kind"].split(":")[0] for g in plan)
    assert kinds["decoy"] / 300 >= 0.38 and kinds["ns"] / 300 >= 0.38
    assert {g["cell"]["cls"] for g in plan} == set(C.CLASSES)
    assert all(g["cell"]["pair_kind"] != "ns:NS-2" for g in plan if g["cell"]["cls"] in C.STATIC)


def test_plan_oversampled():
    assert len(G.build_plan(600, seed=1)) > 300


def test_records_hide_labels_from_text(dry):
    rows = dry[0]
    for r in rows[:300]:
        t = r["rendered"]["text"]
        assert "CWE-" not in t and "CVE" not in t
        assert not any(i in t for i in C.FORBIDDEN_IDS)


def test_b_view_has_no_label(dry):
    r = dry[0][0]
    v = schema.b_view(r)
    assert "gold" not in v and "spec" not in v and "witness" not in str(v.get("witness_inputs"))
    assert all("label" not in o for o in v["options"])


def test_pair_members_share_names_and_layout(dry):
    rows = {r["row_id"]: r for r in dry[0] if r["head"] == "VULN"}
    seen = 0
    for r in rows.values():
        t = rows.get(r["meta"]["twin_of"])
        if t and r["row_id"] < t["row_id"]:
            assert r["spec"]["fn"] == t["spec"]["fn"] and r["spec"]["stem"] == t["spec"]["stem"]
            assert r["gold"] != t["gold"]
            seen += 1
    assert seen > 50


def test_dry_run_summary(dry):
    rows, summ, log, rep = dry
    assert summ["dropped"].get("answer:roundtrip", 0) == 0
    assert summ["fix_trigger_g13"] is False
    assert all(r["manifest"]["gold_method"] == "static_taint" for r in rows)


def test_head_rows_cap_and_derivation(dry):
    rows = dry[0]
    heads = [r for r in rows if r["head"] == "CWE"]
    yes = [r for r in rows if r["head"] == "VULN" and r["gold"] == "YES"]
    assert 0 < len(heads) <= C.HEAD_ROWS_MAX and len(heads) <= 0.25 * len(yes)
    ids = {r["row_id"] for r in yes}
    assert all(h["meta"]["head_of"] in ids for h in heads)
    assert all(len({o["label"] for o in h["options"]}) == 4 and h["gold"] in [o["label"] for o in h["options"]] for h in heads)


def test_head_rows_never_from_no_specs(dry):
    rows = {r["row_id"]: r for r in dry[0]}
    for h in [r for r in dry[0] if r["head"] == "CWE"]:
        assert rows[h["meta"]["head_of"]]["gold"] == "YES"


def test_solver_a_matches_gold(dry):
    assert all(solver_a.gold_a(r) == r["gold"] for r in dry[0])


def test_solver_a_detects_corruption(dry):
    r = next(x for x in dry[0] if x["head"] == "VULN" and x["spec"]["cls"] in C.DYNAMIC)
    bad = dict(r, spec=dict(r["spec"], witness=dict(r["spec"]["witness"], effect=not r["spec"]["witness"]["effect"])))
    assert solver_a.gold_a(bad) is None


def test_roundtrip_catches_banned_word_and_cwe_number(dry):
    r = next(x for x in dry[0] if x["head"] == "VULN")
    spec = dict(r["spec"], source_text=r["spec"]["source_text"].replace("def ", "def evil_", 1))
    assert any(b.startswith("banned_word") for b in roundtrip.check(dict(r, spec=spec)))
    r2 = dict(r, rendered=dict(r["rendered"], text=r["rendered"]["text"] + " CWE-79"))
    assert "F2" in roundtrip.check(r2)


def test_roundtrip_comment_detected_but_hash_in_string_ok():
    assert roundtrip.F2.search("see CVE-2020-1")
    import io, tokenize
    assert not any(t.type == tokenize.COMMENT for t in tokenize.generate_tokens(io.StringIO('x = "a#top"\n').readline))


def test_g13_hit_retires_pair_and_head_row():
    hook = pl.TestDoubleHook(hit_if=lambda it: it["row_id"].startswith("T65-") and it["row_id"].split("-")[2] in ("0001", "0002"))
    rows, summ, log, rep = dryrun.dry_rows(120, seed=2, hook=hook)
    assert summ["retired_groups"] >= 1
    gids = {r["group_id"] for r in rows}
    assert not any(g.endswith("-0001") for g in gids)
    for r in rows:
        if r["head"] == "CWE":
            assert r["meta"]["head_of"] in {x["row_id"] for x in rows}


def test_production_requires_solver_b_and_real_pool():
    with pytest.raises(Exception):
        checked.run(10, 1, pl.RefusingHook(), standin=False)


def test_sim_executor_refused_for_production_ctx():
    with pytest.raises(Exception):
        G.Ctx(seed=1, standin=False, pool_path=None, executor=S.SimExecutor())


def test_names_avoid_banned_words(dry):
    for r in dry[0][:200]:
        assert roundtrip.check(r) == []


def test_gate_composition(dry):
    res = {g["id"]: g for g in gates.run_all(dry[0])}
    for gid in ("T65-witness", "T65-K14", "T65-balance", "T65-kinds", "T65-pairs", "T65-head-cap", "T65-tokens", "T65-split", "T65-stamps", "T65-hooks", "T65-no-permission", "T65-twin-edit"):
        assert res[gid]["ok"], res[gid]


def test_gate_catches_head_cap_violation(dry):
    heads = [r for r in dry[0] if r["head"] == "CWE"]
    rows = dry[0] + [dict(heads[0], row_id=heads[0]["row_id"] + "x")] * 5
    assert not gates.g_head_cap(rows)["ok"]


def test_tokens_under_cap(dry):
    assert max(r["meta"]["tokens"] for r in dry[0]) <= 1536


def test_no_label_words_in_picked_names():
    for seed in range(1, 6):
        for cls in C.CLASSES:
            y, n = _pair(cls, "plain", seed=seed)
            assert roundtrip.check({"spec": y, "rendered": {"text": y["source_text"]}, "head": "CWE"}) == [], (cls, seed)


def test_no_rows_written():
    assert not [f for f in os.listdir(FAMDIR) if f.endswith((".jsonl", ".parquet"))]
