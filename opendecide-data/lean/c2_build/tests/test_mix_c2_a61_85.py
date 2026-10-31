"""Tests for mix_c2.py under Ruling A61 (f), program fixes 4 and 5: the 8.5 membership list, the 0-DI refusal, the credit fit, P (the MD rows the
proportional step removed), and --remove-sources, the drops-only path after an 8.5 HIT or an incomplete check (load the written final mix, remove the
sources with their relation units and twins, refit MD, finish()'s steps after the refill loop with no refill, gates with the 8,000 floor lowered only by
P). In memory / tmp_path only: nothing is written to the C2 tree, no sealed or ohs path is named, source_name_check.py is never run. Run from c2_build/:
  ../../.venv/bin/python -B -m pytest -q tests/test_mix_c2_a61_85.py
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2B))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import c2io  # noqa: E402
import mix_c2 as m  # noqa: E402
import mixer as mx  # noqa: E402
from test_mix_c2 import flow  # noqa: E402,F401  (the in-memory build fixture)
from test_mix_c2_a42d import args_for, mk  # noqa: E402


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# ------------------------------------------------------------------------------------------------ ids and membership
def test_gate_ids_map_both_ways():
    assert m.gate_id("MD", "c2_md_cma") == "md_cma" and m.gate_id("MD", "c2_md_gene_ontology") == "md_gene_ontology"
    assert m.gate_id("SB5", "c2_sb5") == "SB5_uci293"
    for bad in (("MD", "c2_md_"), ("MD", "md_cma"), ("MD", "c2_sb5"), ("SB5", "c2_sb5x"), ("SB5", "c2_md_x"), ("T28", "c2_md_cma"), ("GB", "c2_sb5")):
        assert m.gate_id(*bad) is None, bad
    assert m.row_source_of("md_cma") == ("MD", "c2_md_cma") and m.row_source_of("SB5_uci293") == ("SB5", "c2_sb5")
    assert m.row_source_of("md_") is None and m.row_source_of("gp_x") is None and m.row_source_of("DI-KR_gsm8k") is None
    for sid in ("md_a", "md_b_c", "SB5_uci293"):
        b, src = m.row_source_of(sid)
        assert m.gate_id(b, src) == sid


@pytest.fixture
def binding(tmp_path, monkeypatch):
    """Fixture binding inputs (the ruling's closed list) under tmp, with their real-shaped entries and shas."""
    md = tmp_path / "SOURCES_CANDIDATES.json"
    sb56, sb5 = tmp_path / "SOURCES_SB56_85.json", tmp_path / "SOURCES_SB5_85.json"
    md.write_text(json.dumps({"sources": [{"id": f"md_{x}", "name": x} for x in "abcdefgh"] + [{"id": "md_a#2", "name": "a2"}]}))
    sb56.write_text(json.dumps({"sources": [{"id": "SB5_uci293", "name": "x"}, {"id": "SB6_tydiqa", "name": "y"}]}))
    sb5.write_text(json.dumps({"sources": [{"id": "SB5_uci293#doi", "name": "x"}]}))
    sh = lambda p: sha_bytes(p.read_bytes())    # noqa: E731
    monkeypatch.setattr(m, "BINDING_INPUTS", {"md": ((md, sh(md)),), "SB5_uci293": ((sb56, sh(sb56)), (sb5, sh(sb5)))})
    return md, sb56, sb5


def test_membership_lists_the_gated_sources_with_a_row_and_checks_the_binding_inputs(binding):
    rows = [mk(f"m{i}", "MD", source=f"c2_md_{'abc'[i % 3]}") for i in range(9)] + [mk("s1", "SB5", source="c2_sb5"), mk("t1", "T28"), mk("g1", "GB")]
    rep, probs = m.gated_membership(rows)
    assert probs == [] and rep["sources"] == ["SB5_uci293", "md_a", "md_b", "md_c"]
    assert rep["rows_by_source"] == {"SB5_uci293": 1, "md_a": 3, "md_b": 3, "md_c": 3}
    assert rep["row_sources"]["md_a"] == "c2_md_a" and set(rep["binding_inputs"]) == {"md", "SB5_uci293"}
    assert all(len(f["sha256"]) == 64 for v in rep["binding_inputs"].values() for f in v)
    assert m.gated_membership([mk("t1", "T28")]) == ({"sources": [], "rows_by_source": {}, "row_sources": {}}, [])      # nothing gated: no binding read


def test_a_gated_row_whose_source_maps_to_no_id_refuses(binding):
    probs = m.gated_membership([mk("m1", "MD", source="c2_md_a"), mk("m2", "MD", source="weird")])[1]
    assert len(probs) == 1 and "maps to no 8.5 id" in probs[0]
    assert "maps to no 8.5 id" in m.gated_membership([mk("s1", "SB5", source="c2_sb5_other")])[1][0]
    probs = m.gated_membership([mk("m1", "MD", source="c2_md_zzz")])[1]                       # maps, but the id is in no binding input
    assert len(probs) == 1 and "no id in the binding inputs" in probs[0] and "md_zzz" in probs[0]
    assert m.gated_membership([mk("m1", "MD", source="c2_md_a")])[1] == []                    # md_a#2 folds into md_a: found


def test_a_binding_input_with_another_sha_or_missing_refuses(binding, monkeypatch):
    md, sb56, sb5 = binding
    md.write_text(md.read_text() + " ")                                                        # edited after the logged sha
    assert any("SOURCES_CANDIDATES.json sha256 differs" in x for x in m.gated_membership([mk("m1", "MD", source="c2_md_a")])[1])
    sb5.unlink()
    assert any("SOURCES_SB5_85.json unreadable" in x for x in m.gated_membership([mk("s1", "SB5", source="c2_sb5")])[1])


def test_the_pins_are_the_rulings():
    """The module's own BINDING_INPUTS (A61 f: SOURCES_CANDIDATES.json, SOURCES_SB56_85.json, SOURCES_SB5_85.json), read from its source text."""
    src = Path(m.__file__).read_text(encoding="utf-8")
    for name, sha in (("SOURCES_CANDIDATES.json", "644cb9f5b6ca34dc5e5ac21b021bc559c2bb465d66bf7baf720b254cdd86f5f7"),
                      ("SOURCES_SB56_85.json", "c4a9f5f555838a548a844f165b2571c9f39a79dce89babcc5dc1e358f0fc1c4b"),
                      ("SOURCES_SB5_85.json", "bdb1e171ec59601ab3cc0cd215e2e215bb788ee0ef10a506f3831b8aa2a09f4e")):
        assert f'"{name}", "{sha}"' in src, name
    assert set(m.BINDING_INPUTS) == {"md", "SB5_uci293"} and len(m.BINDING_INPUTS["SB5_uci293"]) == 2


# ------------------------------------------------------------------------------------------------ the 0-DI refusal, the credit fit
def final_args(args, tmp_path, monkeypatch, **kw):
    monkeypatch.setattr(m, "ohs4_problem", lambda sha, text, pinned=None: None)
    man, gp = tmp_path / "never_train.json", tmp_path / "gproxy.jsonl"
    man.write_text('{"anchors": [{"name": "bfcl", "sha256": "' + "a" * 64 + '"}]}')
    gp.write_text('{"id": "g1"}\n')
    return args(final=True, ohs4_sha="e" * 64, decontam_drops=[], never_train_manifest=man, gproxy_file=gp, **kw)


def test_final_refuses_when_a_di_block_enters(flow, monkeypatch, tmp_path):
    args, writes, inp = flow

    def admit(ilog, leave_out, rep):
        rep["entry"] = {"entered": ["DI-KR"], "left_out": {}}
        return ["DI-KR"]
    monkeypatch.setattr(m, "admit_blocks", admit)
    with pytest.raises(SystemExit, match=r"DI block\(s\) \['DI-KR'\] entered but the DI part is 0"):
        m.assemble(final_args(args, tmp_path, monkeypatch, credit_usd=100.0))
    assert writes == {}


def test_gates_refuse_a_di_row_in_a_final_mix_and_a_dry_run_only_reports(monkeypatch):
    monkeypatch.setattr(m, "gated_membership", lambda rows: ({"sources": []}, []))
    stubs_for_gates(monkeypatch)
    rows = [mk("k1", "DI-KR", source="gsm8k"), mk("a1", "T28")]
    seen = {}
    monkeypatch.setattr(m, "write_outputs", lambda a, rep, rows, rels: seen.setdefault("p", list(rep["problems"])) or rep)
    a = type("A", (), {"final": True, "spend_to_date": 0.0})()
    m.gates(a, FakeIlog({}), {"budget": {}, "plan_final": None}, [], rows, [], {r["id"]: 10 for r in rows}, FakeHO(), {"targets": {}}, 0.0)
    assert any("DI row(s) in the final mix" in x and "the DI part is 0" in x for x in seen["p"])
    seen.clear()
    a = type("A", (), {"final": False, "spend_to_date": 0.0})()
    monkeypatch.setattr(m, "dry_report", lambda rep: rep)
    rep = m.gates(a, FakeIlog({}), {"budget": {}, "plan_final": None}, [], rows, [], {r["id"]: 10 for r in rows}, FakeHO(), {"targets": {}}, 0.0)
    assert not any("DI row(s) in the final mix" in x for x in rep["problems"])


def test_main_needs_credit_usd_with_final_and_remove_sources_rules(monkeypatch, tmp_path):
    with pytest.raises(SystemExit, match="decontam"):                                           # checked first, as before
        m.main(["--final", "--spend-to-date", "1.5", "--ohs4-sha", "e" * 64])
    f = tmp_path / "d.json"
    f.write_text("{}")
    with pytest.raises(SystemExit, match="needs --credit-usd"):
        m.main(["--final", "--spend-to-date", "1.5", "--ohs4-sha", "e" * 64, "--decontam-drops", str(f)])
    rm_file = tmp_path / "rm.json"
    rm_file.write_text('["md_a"]')
    with pytest.raises(SystemExit, match="needs --final"):
        m.main(["--dry-run", "--spend-to-date", "1.5", "--remove-sources", str(rm_file)])
    with pytest.raises(SystemExit, match="takes no --decontam-drops"):
        m.main(["--final", "--spend-to-date", "1.5", "--credit-usd", "40", "--remove-sources", str(rm_file), "--decontam-drops", str(f)])
    called = {}
    monkeypatch.setattr(m, "remove_sources", lambda a: called.setdefault("a", a) and {"shares": {}, "problems": [], "entry": {}})
    m.main(["--final", "--spend-to-date", "1.5", "--credit-usd", "40", "--remove-sources", str(rm_file)])
    assert called["a"].remove_sources == str(rm_file) and called["a"].credit_usd == 40.0 and called["a"].final


def test_the_credit_fit_is_in_the_report_and_lowers_the_ceiling(flow):
    args, writes, inp = flow
    rep = m.build(args(spend_to_date=0.0))
    assert rep["credit_usd"] is None and rep["t_core_usd"] == rep["t_max_usd"] == 32.0
    rep = m.build(args(spend_to_date=0.0, credit_usd=39.0))                                    # C - 8 = 31 < 32
    assert rep["credit_usd"] == 39.0 and rep["t_core_usd"] == rep["t_max_usd"] == 31.0 and rep["budget"]["credit_usd"] == 39.0
    assert rep["budget"]["t_max_usd"] == 31.0
    rep = m.build(args(spend_to_date=0.0, credit_usd=500.0))
    assert rep["t_core_usd"] == rep["t_max_usd"] == 32.0                                        # never raised
    assert rep["relay_accounts"] == ["mahadikarya2", "mahadikarya3"] and rep["c2_modal_cap_usd"] == 40.0 and rep["rows_max"] == 125000


# ------------------------------------------------------------------------------------------------ P: the proportional step's MD rows
def md_rows(sizes: dict, tag="M", per_task=10, free=True):
    rows = []
    for s, n in sizes.items():
        for t in range(n // per_task):
            for i in range(per_task):
                rows.append(mk(f"{tag}_{s}_t{t}_{i}", "MD", source=f"c2_md_{s}", gold=i % 2, card="" if free else "c",
                               meta={"task_id": f"{s}t{t}", "domain": f"dom_{s}"}))
    return rows


def test_budget_trim_records_p_the_md_rows_the_proportional_step_removed(monkeypatch):
    monkeypatch.setattr(m, "project_cost", lambda rows, rels, ntok, seed=m.SEED: {
        "total_usd": round(len(rows) * 0.01, 4), "train_usd": round(len(rows) * 0.01, 4), "rows": len(rows)})
    monkeypatch.setattr(m, "OVERHEAD_USD", 0.0)
    monkeypatch.setattr(m, "FLOOR_ROWS", 100)
    monkeypatch.setattr(m, "META_MIN_ROWS", 10 ** 6)                   # trim_meta_tail (step 3) has nothing above the floor: the proportional step runs

    def stub(rows, rels, targets, parts, seed=m.SEED, **kw):                 # keep the first t rows of each block
        seen, out = Counter(), []
        for r in rows:
            b = r["_block"]
            if b in targets and seen[b] >= targets[b]:
                continue
            seen[b] += 1
            out.append(r)
        return out, rels, {}
    monkeypatch.setattr(m, "apply_targets", stub)
    rows = md_rows({s: 100 for s in "abcdefgh"}) + [mk(f"a{i}", "T28", source="t28") for i in range(400)]        # 800 MD + 400 T28 = $12
    rep, probs = {}, []
    out, _ = m.budget_trim(args_for(24.0), rows, [], {}, {}, {}, {}, rep, probs)           # T_core $8: trimmed in proportion
    b = rep["budget"]
    assert b["proportional_used"] and b["p_md_proportional"] == 800 - sum(1 for r in out if r["_block"] == "MD") > 0
    rep2 = {}
    m.budget_trim(args_for(0.0), rows, [], {}, {}, {}, {}, rep2, [])                       # no trim: P = 0
    assert rep2["budget"]["p_md_proportional"] == 0 and not rep2["budget"]["proportional_used"]


# ------------------------------------------------------------------------------------------------ gates: the MD floor on the removal path
class FakeIlog:
    def __init__(self, files):
        self.files, self.entries, self.never = files, [], {"names": set()}

    def jsonl(self, p):
        return self.files[str(p)] if str(p) in self.files else [json.loads(x) for x in Path(p).read_text().splitlines() if x.strip()]


class FakeHO:
    def check(self, rows, rep):
        return []


def stubs_for_gates(monkeypatch):
    monkeypatch.setattr(mx, "licence_ok", lambda r: True)
    monkeypatch.setattr(m, "refuse_held_out", lambda ilog, blocks, rep: [])
    monkeypatch.setattr(mx, "split_replay_call_ids", lambda rows, rels, ntok, rep: rels)
    monkeypatch.setattr(mx, "unit_check", lambda rows, rels, ntok, rep: [])
    monkeypatch.setattr(mx, "check_rows", lambda rows, rep: [])
    monkeypatch.setattr(mx, "g10_checks", lambda rows, rep, final, side=None: [])
    monkeypatch.setattr(m, "cap_checks", lambda rows, ntok, final=True: ({}, []))
    monkeypatch.setattr(m, "a49c_assert", lambda rows, rels, ntok: ({}, []))
    monkeypatch.setattr(m, "a60_shares", lambda rows: ({"problems": []}, []))
    monkeypatch.setattr(m, "block_mixdev_ids", lambda ilog, blocks: {})
    monkeypatch.setattr(m, "mixdev_id_problems", lambda rows, mixdev, rep: [])
    monkeypatch.setattr(m, "anchor_row_problems", lambda rows, names: [])
    monkeypatch.setattr(m, "share_checks", lambda by, plan: ({"total": sum(by.values()), "new": 0, "replay": [0, 0]}, []))
    monkeypatch.setattr(m, "config_fill", lambda rows, rels, seed=m.SEED: {"epochs": 1, "seed": m.SEED})


def test_gates_pass_block_rules_the_floor_and_never_proportional_trim_on_the_removal_path(monkeypatch):
    stubs_for_gates(monkeypatch)
    monkeypatch.setattr(m, "gated_membership", lambda rows: ({"sources": []}, []))
    calls = []
    real = m.block_rules
    monkeypatch.setattr(m, "block_rules", lambda b, rows, **kw: calls.append((b, kw)) or real(b, rows, **kw))
    monkeypatch.setattr(m, "write_outputs", lambda a, rep, rows, rels: rep)
    rows = md_rows({s: 30 for s in "abcdefgh"})
    base = {"budget": {"proportional_used": True}, "plan_final": None}
    for remove, want_trim in ((None, True), ("/x/rm.json", False)):
        calls.clear()
        a = type("A", (), {"final": True, "spend_to_date": 0.0, "remove_sources": remove, "md_min_rows": 123 if remove else None})()
        m.gates(a, FakeIlog({}), copy.deepcopy(base), [], list(rows), [], {r["id"]: 10 for r in rows}, FakeHO(), {"targets": {}}, 0.0)
        md = [kw for b, kw in calls if b == "MD"]
        assert len(md) == 1 and md[0]["proportional_trim"] is want_trim, md                      # True is never passed on the removal path
        assert md[0]["min_rows"] == (123 if remove else None)


def test_block_rules_floor_argument():
    rows = md_rows({s: 30 for s in "abcdefgh"})                                                  # 240 rows, 8 sources, 8 domains
    assert m.block_rules("MD", rows, min_rows=240)[1] == [] and m.block_rules("MD", rows)[1] != []        # default floor 8,000
    low = m.block_rules("MD", rows, min_rows=241)[1]
    assert len(low) == 1 and "240 rows < 241" in low[0] and "8,000 floor less P = 7759" in low[0]
    assert m.block_rules("MD", rows, min_rows=241, proportional_trim=True)[1] == []              # the waiver of the normal path, unchanged
    assert m.block_rules("MD", rows, min_rows=0)[1] == [] and m.block_rules("MD", rows)[0]["min_rows"] == m.META_MIN_ROWS


# ------------------------------------------------------------------------------------------------ --remove-sources
def j(o):
    return json.dumps(o, sort_keys=True)


class Harness:
    """A written final mix on disk (tmp), the membership list, and a fake assemble() with the replay pool; everything heavy is stubbed."""

    def __init__(self, tmp, mp, md_sizes, p=0, floor=250, sb5=100, t28=50, member=None):
        self.tmp, self.mp = tmp, mp
        mp.setattr(m, "META_MIN_ROWS", floor)
        mp.setattr(m, "FLOOR_ROWS", 100)
        mp.setattr(m, "OVERHEAD_USD", 0.0)
        mp.setattr(m, "project_cost", lambda rows, rels, ntok, seed=m.SEED: {
            "total_usd": round(len(rows) * 0.001, 4), "train_usd": round(len(rows) * 0.001, 4), "rows": len(rows)})
        mp.setattr(mx, "e2_final", lambda ctx, rows, rep: [])
        mp.setattr(m, "A72_FIXES", False)                                                  # these tests pin the A61 f removal logic; the A72 fixes have their own tests
        mp.setattr(mx, "token_counts", lambda ilog, rows, chunk=2000: [100] * len(rows))
        mp.setattr(mx, "HeldOut", lambda dev, rs: FakeHO())
        mp.setattr(m, "dev_items", lambda ilog, blocks, dev_sets=None: ({}, []))
        mp.setattr(mx, "shrink_replay", self.shrink)
        mp.setattr(m, "apply_targets", self.no_apply)
        mp.setattr(c2io, "require_a38", lambda prereg_text=None: None)
        mp.setattr(m, "log_line", lambda *a, **k: None)
        stubs_for_gates(mp)
        self.writes = {}
        mp.setattr(c2io, "write_json", lambda path, obj, prereg_text=None: self.writes.__setitem__(str(path), obj) or sha_bytes(j(obj).encode()))
        mp.setattr(c2io, "write_jsonl", lambda path, rows, prereg_text=None: self.writes.__setitem__(str(path), rows) or sha_bytes(j(rows).encode()))
        self.md = md_rows(md_sizes)
        self.sb5 = [mk(f"S_{i}", "SB5", source="c2_sb5", gold=i % 2, meta={"domain": "x"}) for i in range(sb5)]
        self.t28 = [mk(f"A_{i}", "T28", source="t28", gold=i % 2) for i in range(t28)]
        new = len(self.md) + len(self.sb5) + len(self.t28)
        self.replay = [mk(f"R_{i}", "replay", source=f"gd_{i % 3}", call_id=f"rc{i}", gold=i % 2) for i in range(math.floor(1.5 * new))]
        self.rels = [{"a": f"M_{s}_t0_0", "b": f"M_{s}_t0_1", "type": "twin"} for s in md_sizes]
        rows = self.replay + self.t28 + self.md + self.sb5
        self.clean = [{k: v for k, v in r.items() if k != "_block"} for r in rows]
        self.block = {r["id"]: r["_block"] for r in rows}
        self.train, self.rel, self.man, self.mem = tmp / "c2_train.jsonl", tmp / "c2_rel.jsonl", tmp / "c2_mix_manifest.json", tmp / "membership.json"
        mp.setattr(m, "OUT_TRAIN", self.train)
        mp.setattr(m, "OUT_REL", self.rel)
        mp.setattr(m, "OUT_MAN", self.man)
        mp.setattr(m, "MEMBERSHIP", self.mem)
        mp.setattr(m, "WORK", tmp / "work")
        mp.setattr(m, "write_outputs", m.write_outputs)
        srcs = member if member is not None else sorted({f"md_{s}" for s in md_sizes} | ({"SB5_uci293"} if sb5 else set()))
        self.mem.write_text(j({"sources": srcs}))
        bi = {k: tmp / f"bind_{k}.json" for k in ("md", "sb56", "sb5")}                               # fixture binding inputs with every id of the mix
        bi["md"].write_text(j({"sources": [{"id": f"md_{s}"} for s in md_sizes] + [{"id": "md_s1#2"}]}))
        bi["sb56"].write_text(j({"sources": [{"id": "SB5_uci293"}, {"id": "SB6_tydiqa"}]}))
        bi["sb5"].write_text(j({"sources": [{"id": "SB5_uci293#doi"}]}))
        mp.setattr(m, "BINDING_INPUTS", {"md": ((bi["md"], sha_bytes(bi["md"].read_bytes())),),
                                         "SB5_uci293": tuple((bi[k], sha_bytes(bi[k].read_bytes())) for k in ("sb56", "sb5"))})
        self.train.write_text("\n".join(j(r) for r in self.clean) + "\n")
        self.rel.write_text("\n".join(j(x) for x in self.rels) + "\n")
        self.mem_sha = sha_bytes(self.mem.read_bytes())
        self.man.write_text(j({"files": {"c2_train.jsonl": {"sha256": sha_bytes(self.train.read_bytes()), "rows": len(self.clean)},
                                         "c2_rel.jsonl": {"sha256": sha_bytes(self.rel.read_bytes()), "rows": len(self.rels)}},
                               "counts": {"by_block": dict(Counter(r["_block"] for r in rows))}, "ohs4_manifest_sha256": "e" * 64,
                               "p_md_proportional": p, "a61_85_membership": {"sha256": self.mem_sha, "sources": srcs}}))
        self.refilled = []
        self.mp.setattr(m, "assemble", self.assemble)

    def shrink(self, rows, rels, pools, ctx, cut, info):
        rep_ids = sorted(r["id"] for r in rows if r["_block"] == "replay")
        gone = set(rep_ids[len(rep_ids) - cut:]) if cut > 0 else set()
        info["replay_shrink"] = {"cut_asked": cut}
        return mx.drop_rows(rows, rels, gone)

    def no_apply(self, rows, rels, targets, parts, seed=m.SEED, **kw):
        raise AssertionError("apply_targets must not run here (no agent cap, no proportional step)")

    def assemble(self, a, removal=False):
        assert removal and a.final and a.decontam_drops == []
        pool_md = type("P", (), {"block": "MD", "cands": {"x": ["u"]}, "raw_of": lambda self_, u: [mk("POOL_MD_1", "MD", source="c2_md_a")],
                                 "rows_of": lambda *aa, **kk: self.refilled.append(1)})()
        rp = type("P", (), {"block": "replay", "unit_of": {r["id"]: i for i, r in enumerate(self.replay)}})()
        st_rows = self.t28 + self.md + self.sb5
        plan = m.plan_shares(dict(Counter(r["_block"] for r in st_rows)))
        rep = {"mode": "final", "never_train": {}, "spend_to_date_usd": a.spend_to_date, "credit_usd": a.credit_usd, "t_max_usd": 32.0,
               "t_core_usd": 32.0, "entry": {}}
        return None, {"ilog": FakeIlog({}), "rep": rep, "probs": [], "rows": st_rows, "rels": [], "parents": {}, "pools": {"replay": rp, "MD": pool_md},
                      "parts": {}, "ctx": {}, "plan": plan, "t0": 0.0, "rs": None}

    def args(self, ids, **kw):
        f = self.tmp / "rm.json"
        f.write_text(j(ids))
        return type("A", (), {"final": True, "remove_sources": str(f), "spend_to_date": 0.0, "credit_usd": 100.0, "ohs4_sha": None,
                              "decontam_drops": [], "leave_out": []} | kw)()

    def out(self):
        rows = self.writes[str(self.train)]
        return rows, self.writes[str(self.rel)], self.writes[str(self.man)]


SIZES12 = {**{f"s{i}": 30 for i in range(12)}, "s0": 50}      # 380 MD rows: 12 sources, 12 domains, s0 = 13.2%


@pytest.fixture
def hz(tmp_path, monkeypatch):
    return lambda **kw: Harness(tmp_path, monkeypatch, **({"md_sizes": SIZES12} | kw))


def counts(rows):
    return Counter(r.get("source") if r.get("source") in ("c2_sb5",) else ("replay" if r["id"].startswith("R_") else
                   ("T28" if r["id"].startswith("A_") else "MD" if r["id"].startswith("M_") else "?")) for r in rows)


def test_an_md_source_removal_refits_the_caps_adds_nothing_keeps_the_membership_and_the_replay_rule(hz):
    h = hz(floor=200)
    ids = {r["id"] for r in h.clean}
    rep = m.remove_sources(h.args(["md_s1", "md_s2", "md_s3", "md_s4"]))
    rows, rels, man = h.out()
    out_ids = {r["id"] for r in rows}
    assert out_ids <= ids and "POOL_MD_1" not in out_ids and h.refilled == []                     # no id is ever added; no pool row; no refill
    assert not any(r["source"] in {f"c2_md_s{k}" for k in (1, 2, 3, 4)} for r in rows if r["id"].startswith("M_"))
    md = [r for r in rows if r["id"].startswith("M_")]
    sc = Counter(r["source"] for r in md)
    assert len(md) == 240 and sc["c2_md_s0"] == 30 and max(sc.values()) <= 0.15 * len(md) + 1e-9      # s0 was 50/260 = 19%: refitted by whole tasks to 30
    assert rep["a61_remove"]["md_fit"]["steps"] and not rep["a61_remove"]["md_removed_whole"] and rep["a61_remove"]["P"] == 0
    assert len({r["meta"]["domain"] for r in md}) == 8 and not m.block_rules("MD", [r | {"_block": "MD"} for r in md], min_rows=200)[1]
    new = sum(1 for r in rows if not r["id"].startswith("R_"))
    assert sum(1 for r in rows if r["id"].startswith("R_")) == math.floor(1.5 * new)               # replay follows floor(1.5 x new)
    assert sum(1 for r in rows if r["id"].startswith("A_")) == 50 and sum(1 for r in rows if r["source"] == "c2_sb5") == 100   # the other blocks stay
    assert sha_bytes(h.mem.read_bytes()) == h.mem_sha and str(h.mem) not in h.writes             # the membership list is not rewritten
    assert man["a61_85_membership"]["sha256"] == h.mem_sha and man["a61_remove"]["sources"] == ["md_s1", "md_s2", "md_s3", "md_s4"]
    assert man["p_md_proportional"] == 0 and man["credit_usd"] == 100.0 and rep["mode"] == "final (--remove-sources)"
    assert (h.tmp / "work").is_dir() and list((h.tmp / "work").glob("pre_remove_*/c2_train.jsonl"))   # the replaced mix is kept first
    assert all("_block" not in r for r in rows)


def test_an_8_2_failure_removes_the_metadata_block_whole_and_the_tail_runs_again(hz):
    h = hz(md_sizes={f"s{i}": 30 for i in range(8)}, floor=100)                                  # 8 domains: one source removed leaves 7 < 8
    rep = m.remove_sources(h.args(["md_s7"]))
    rows, rels, man = h.out()
    assert not any(r["id"].startswith("M_") for r in rows) and rep["a61_remove"]["md_removed_whole"]
    assert any("7 domains < 8" in x for x in rep["a61_remove"]["md_8_2_problems"])
    assert sum(1 for r in rows if r["id"].startswith("A_")) == 50 and sum(1 for r in rows if r["source"] == "c2_sb5") == 100
    new = len(rows) - sum(1 for r in rows if r["id"].startswith("R_"))
    assert sum(1 for r in rows if r["id"].startswith("R_")) == math.floor(1.5 * new) and new == 150        # replay again follows the rule
    assert man["a61_remove"]["md_removed_whole"] is True and not h.refilled


@pytest.mark.parametrize("p,kept", [(20, True), (10, True), (9, False), (5, False), (0, False)])
def test_the_8000_floor_is_lowered_only_by_p(hz, p, kept):
    """MD 240 rows after the removal and the refit (s0 50 -> 30); the floor stands at 250: P = 10 is the largest shortfall P can cover."""
    h = hz(floor=250, p=p)
    rep = m.remove_sources(h.args(["md_s1", "md_s2", "md_s3", "md_s4"]))
    rows, _, man = h.out()
    has_md = any(r["id"].startswith("M_") for r in rows)
    assert has_md is kept and rep["a61_remove"]["md_removed_whole"] is (not kept)
    assert rep["a61_remove"]["md_floor"] == 250 - p and man["p_md_proportional"] == p
    if has_md:
        assert sum(1 for r in rows if r["id"].startswith("M_")) == 240
    else:
        assert any("rows <" in x for x in rep["a61_remove"]["md_8_2_problems"])


def test_p_is_zero_when_the_record_lacks_it_and_a_shortfall_is_never_waived(hz):
    h = hz(floor=250)
    man = json.loads(h.man.read_text())
    man.pop("p_md_proportional")
    h.man.write_text(j(man))
    rep = m.remove_sources(h.args(["md_s1", "md_s2", "md_s3", "md_s4"]))
    assert rep["a61_remove"]["P"] == 0 and rep["a61_remove"]["md_removed_whole"]                # no waiver: proportional_trim=True is never passed


def test_an_sb5_removal_works_and_leaves_md(hz):
    h = hz(floor=200)
    rep = m.remove_sources(h.args(["SB5_uci293"]))
    rows, _, man = h.out()
    assert not any(r["source"] == "c2_sb5" for r in rows) and sum(1 for r in rows if r["id"].startswith("M_")) == 380
    assert not rep["a61_remove"]["md_removed_whole"] and "md_fit" in rep["a61_remove"]
    new = len(rows) - sum(1 for r in rows if r["id"].startswith("R_"))
    assert new == 430 and sum(1 for r in rows if r["id"].startswith("R_")) == math.floor(1.5 * new)


def test_relation_units_and_twins_leave_with_the_source(hz):
    h = hz(floor=100)
    twin = mk("M_s0_twin", "MD", source="c2_md_s5", gold=0, meta={"task_id": "s5t0", "domain": "dom_s5", "twin_of": "M_s1_t0_0"}, call_id="M_s1_t0_0")
    h.clean.append({k: v for k, v in twin.items() if k != "_block"})                              # a twin row of another source in the same call unit
    h.rels.append({"a": "M_s1_t0_0", "b": "M_s0_twin", "type": "twin"})
    h.train.write_text("\n".join(j(r) for r in h.clean) + "\n")
    h.rel.write_text("\n".join(j(x) for x in h.rels) + "\n")
    man = json.loads(h.man.read_text())
    man["files"]["c2_train.jsonl"]["sha256"] = sha_bytes(h.train.read_bytes())
    man["files"]["c2_rel.jsonl"]["sha256"] = sha_bytes(h.rel.read_bytes())
    man["counts"]["by_block"]["MD"] += 1
    h.man.write_text(j(man))
    h.md.append(twin)
    rep = m.remove_sources(h.args(["md_s1"]))
    rows, rels, _ = h.out()
    assert "M_s0_twin" not in {r["id"] for r in rows}                                              # the related twin of another source left with it
    assert not [x for x in rels if "M_s0_twin" in (x["a"], x["b"])] and rep["a61_remove"]["rows_removed_with_units_and_twins"] == 31


def test_only_listed_gated_sources_of_the_membership_can_be_removed(hz):
    h = hz(floor=100)
    for bad in (["md_nope"], ["gp_x"], ["DI-KR_gsm8k"], ["SB6_tydiqa"], ["md_s1", "md_nope"]):
        with pytest.raises(SystemExit, match="not 8.5-gated sources of the membership list"):
            m.remove_sources(h.args(bad))
    assert h.writes == {} and sha_bytes(h.mem.read_bytes()) == h.mem_sha
    h2 = hz(floor=100, member=["md_s1"])
    with pytest.raises(SystemExit, match="not 8.5-gated sources of the membership list"):
        m.remove_sources(h2.args(["md_s2"]))                                                      # a real source, but not in the membership


def test_the_removal_refuses_when_the_tail_would_run_the_proportional_step_again(hz, monkeypatch):
    h = hz(floor=100)

    def prop(a, rows, rels, ntok, pools, parts, ctx, rep, probs):
        rep["budget"] = {"proportional_used": True, "final_total_usd": 1.0}
        return rows, rels
    monkeypatch.setattr(m, "budget_trim_a61", prop)
    with pytest.raises(SystemExit, match="proportional step again"):
        m.remove_sources(h.args(["SB5_uci293"]))
    assert h.writes == {}                                                                         # nothing written: no training


def test_any_other_gate_failure_stops_with_nothing_written(hz, monkeypatch):
    h = hz(floor=100)
    monkeypatch.setattr(m, "cap_checks", lambda rows, ntok, final=True: ({}, ["a cap is broken"]))
    with pytest.raises(SystemExit, match="a cap is broken"):
        m.remove_sources(h.args(["SB5_uci293"]))
    assert str(h.train) not in h.writes and str(h.man) not in h.writes


def test_a_mix_that_is_not_the_written_one_or_not_reproducible_is_refused(hz):
    h = hz(floor=100)
    h.train.write_text(h.train.read_text() + "\n")                                                # the file changed after the manifest
    with pytest.raises(SystemExit, match="differs from c2_mix_manifest.json"):
        m.remove_sources(h.args(["SB5_uci293"]))
    h = hz(floor=100)
    man = json.loads(h.man.read_text())
    man["a61_85_membership"]["sha256"] = "0" * 64
    h.man.write_text(j(man))
    with pytest.raises(SystemExit, match="membership list"):
        m.remove_sources(h.args(["SB5_uci293"]))
    h = hz(floor=100)
    man = json.loads(h.man.read_text())
    man["counts"]["by_block"]["MD"] += 1
    h.man.write_text(j(man))
    with pytest.raises(SystemExit, match="cannot be reproduced"):
        m.remove_sources(h.args(["SB5_uci293"]))
    h = hz(floor=100)
    h.train.write_text(h.train.read_text() + j({"id": "ghost", "source": "q"}) + "\n")
    man = json.loads(h.man.read_text())
    man["files"]["c2_train.jsonl"]["sha256"] = sha_bytes(h.train.read_bytes())
    h.man.write_text(j(man))
    with pytest.raises(SystemExit, match="cannot be reproduced"):
        m.remove_sources(h.args(["SB5_uci293"]))
    h = hz(floor=100)
    with pytest.raises(SystemExit, match="--ohs4-sha differs"):
        m.remove_sources(h.args(["SB5_uci293"], ohs4_sha="f" * 64))


def test_a_remove_file_must_be_a_list_of_ids(tmp_path):
    f = tmp_path / "r.json"
    for good, want in (('["b", "a", "a"]', ["a", "b"]), ('{"sources": ["x"]}', ["x"]), ('{"ids": ["x"]}', ["x"]), ('{"remove": ["y"]}', ["y"]), ('[]', [])):
        f.write_text(good)
        assert m.load_remove_ids(f) == want
    for bad in ("{not json", '{"other": ["a"]}', '[1, 2]', '["a", ""]', '"a"'):
        f.write_text(bad)
        with pytest.raises(SystemExit):
            m.load_remove_ids(f)
    with pytest.raises(SystemExit):
        m.load_remove_ids(tmp_path / "absent.json")


def test_final_writes_the_membership_list_and_records_p_in_the_manifest(monkeypatch, tmp_path, binding):
    writes = {}
    monkeypatch.setattr(c2io, "write_json", lambda p, obj, prereg_text=None: writes.__setitem__(str(p), obj) or "shamem")
    monkeypatch.setattr(c2io, "write_jsonl", lambda p, rows, prereg_text=None: writes.__setitem__(str(p), rows) or "shatrain")
    monkeypatch.setattr(c2io, "require_a38", lambda prereg_text=None: None)
    monkeypatch.setattr(m, "log_line", lambda *a, **k: None)
    monkeypatch.setattr(m, "MEMBERSHIP", tmp_path / "mem.json")
    rows = md_rows({"a": 20, "b": 20}) + [mk("s1", "SB5", source="c2_sb5"), mk("t1", "T28")]
    rep = {"problems": [], "a61_85": m.gated_membership(rows)[0], "budget": {"final_total_usd": 1.0, "p_md_proportional": 7},
           "config_fill": {}, "t_max_usd": 32.0, "t_core_usd": 32.0, "spend_to_date_usd": 0.0, "never_train": {}, "credit_usd": 40.0}
    a = type("A", (), {"final": True, "ohs4_sha": "e" * 64})()
    m.write_outputs(a, rep, rows, [])
    mem = writes[str(m.MEMBERSHIP)]
    assert mem["sources"] == ["SB5_uci293", "md_a", "md_b"] and mem["mix_train_sha256"] == "shatrain" and mem["rows_by_source"]["md_a"] == 20
    man = writes[str(m.OUT_MAN)]
    assert man["p_md_proportional"] == 7 and man["credit_usd"] == 40.0 and man["a61_85_membership"]["sha256"] == "shamem"
    assert man["a61_85_membership"]["sources"] == ["SB5_uci293", "md_a", "md_b"] and man["a61_remove"] is None
    assert man["c2_modal_cap_usd"] == 40.0 and man["relay_accounts"] == ["mahadikarya2", "mahadikarya3"] and man["rows_max"] == 125000
    writes.clear()
    rep["problems"] = ["x"]
    with pytest.raises(SystemExit):
        m.write_outputs(a, rep, rows, [])
    assert str(m.MEMBERSHIP) not in writes and str(m.OUT_MAN) not in writes                       # a refused mix writes no membership list


# ------------------------------------------------------------------------------------------------ the real assemble() state (flow fixture)
def test_assemble_is_what_build_ran_and_the_removal_flag_skips_only_the_fresh_final_checks(flow, monkeypatch, tmp_path):
    args, writes, inp = flow
    early, st = m.assemble(args())
    assert early is None and {"ilog", "rep", "probs", "rows", "rels", "parents", "pools", "parts", "ctx", "plan", "t0", "rs"} <= set(st)
    assert "replay" in st["pools"] and {"T28", "T01"} <= set(st["pools"])
    a = final_args(args, tmp_path, monkeypatch, credit_usd=100.0)
    monkeypatch.setattr(m, "minimum_to_train", lambda entered: (True, {"ok": True}))
    seen = []
    monkeypatch.setattr(m, "g13_log_problems", lambda ilog, files: seen.append(1) or [])
    early, st2 = m.assemble(a)
    assert early is None and seen == [1]                                                           # a fresh --final checks the G13 drop lists
    seen.clear()
    early, st3 = m.assemble(a, removal=True)
    assert early is None and seen == []                                                            # the removal path does not (the written mix has them)
    assert len(st3["rows"]) == len(st2["rows"])
    a.credit_usd = None
    with pytest.raises(SystemExit, match="needs --credit-usd"):
        m.assemble(a, removal=True)


def test_place_written_rows_on_the_real_pools(flow):
    args, writes, inp = flow
    early, st = m.assemble(args())
    rows = st["rows"]
    pool_t01 = [r for c in st["pools"]["T01"].cands.values() for u in c for r in st["pools"]["T01"].raw_of(u)]
    assert pool_t01 and st["pools"]["replay"].unit_of
    written = [{k: v for k, v in r.items() if k != "_block"} for r in rows] + [dict(pool_t01[0], meta=dict(pool_t01[0].get("meta") or {}, replay_unit="T46"))]
    placed, unplaced = m.place_written_rows(written, rows, st["pools"])
    assert unplaced == 0 and len(placed) == len(rows) + 1
    assert Counter(r["_block"] for r in placed[:len(rows)]) == Counter(r["_block"] for r in rows)    # every row gets the block it came from
    assert placed[-1]["_block"] == "T01" and "replay_unit" not in placed[-1]["meta"]                  # a refill row of a pool is placed too; the T46 tag is cleared
    placed, unplaced = m.place_written_rows(written + [{"id": "ghost", "source": "q"}], rows, st["pools"])
    assert unplaced == 1 and len(placed) == len(rows) + 1


def test_t46_fix_max_is_one_a67():
    """A67 / A59 (e): T46 allows one fix iteration; a record claiming more is cut."""
    import mix_c2
    assert mix_c2.FIX_MAX_BY_FAMILY["T46"] == 1
