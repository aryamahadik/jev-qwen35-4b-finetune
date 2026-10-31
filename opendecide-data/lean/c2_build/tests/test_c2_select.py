"""Tests for c2_select.py and c2io.py (C2 crowd selection, A37 e). In memory only: no row, pool or file is written
(A37 f); the only disk reads are the guard's string checks. Run from lean/:
  ../.venv/bin/python -m pytest -q c2_build/tests/test_c2_select.py
"""
from __future__ import annotations

import random
import sys
from collections import Counter
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2B))
import c2io  # noqa: E402
import c2_select as sel  # noqa: E402
import crowd_select as cs  # noqa: E402
from c2_kit import paths as kp  # noqa: E402


def fam_rows(fam="T28", n_units=600, seed=1, prefix=""):
    """A synthetic C2 family in memory: yes/no rows over 4 wordings (complement partners in some units, same
    call_id) + choice rows with 2-4 and 6 options; per-card yes rates 20-80%."""
    rnd = random.Random(seed)
    rows, rels = [], []
    for u in range(n_units):
        card = u % 10
        rate = 0.2 + 0.6 * card / 9
        base = {"call_id": f"{prefix}c{u}", "group_id": f"{prefix}g{u}", "source": "c2_" + fam.lower(),
                "role": "base", "state": f"s{u}", "card": "card"}
        meta = {"family": fam, "wording_id": f"w{u % 4}", "card_id": f"k{card}", "sampler": f"S{u % 4 + 1}"}
        if u % 3:
            g = int(rnd.random() < rate)
            r = base | {"id": f"{prefix}u{u}a", "qtype": "noul", "gold": g, "options": None,
                        "instructions": "Is it so?", "meta": dict(meta)}
            rows.append(r)
            if u % 5 == 0:
                rows.append(r | {"id": f"{prefix}u{u}b", "gold": 1 - g, "role": "complement"})
                rels.append({"a": f"{prefix}u{u}a", "b": f"{prefix}u{u}b", "type": "complement"})
        else:
            k = [2, 3, 4, 6][u % 4]
            opts = [f"opt{j}" for j in range(k)]
            rows.append(base | {"id": f"{prefix}u{u}a", "qtype": "choice", "gold": opts[rnd.randrange(k)],
                                "options": opts, "instructions": "Which?", "meta": dict(meta)})
    return rows, rels


def crowd(rows, seed=7, vals=(0.99, 0.995, 0.6, 0.8, 0.5, 0.1, 0.2)):
    rnd = random.Random(seed)
    return {r["id"]: rnd.choice(vals) for r in rows}


# ---- the guard and layout (c2io) ------------------------------------------------------------------------------------
@pytest.mark.parametrize("p", ["lean/ohs4_sealed/suite.jsonl", "lean/data/ohs3_parts/x.jsonl",
                               "lean/sealed_nd/score_nd.py", "lean/c_build/preread/x", "lean/logs/jev_raw.jsonl",
                               "bench/external_quarantine/a", "~/.claude/projects/x/memory.md"])
def test_guard_refuses_never_open(p):
    if p.startswith("~"):
        full = p
    elif p.startswith("lean/"):
        full = kp.REPO_ROOT / "opendecide-data" / p
    else:
        full = kp.REPO_ROOT / p
    assert c2io.refusal(full)


def test_guard_allows_c2_inputs_and_checks_names():
    assert c2io.refusal(c2io.C2_PARTS / "T28/out/candidates_c2.jsonl") is None
    assert c2io.refusal(c2io.LEAN / "logs/decontam_counts/pool_drops_r1.json") is None
    with pytest.raises(SystemExit):
        c2io.check_name("ohs4_r")
    with pytest.raises(SystemExit):
        c2io.check_name("preds_jev")
    assert c2io.check_name("c2_mixdev") == "c2_mixdev"
    with pytest.raises(c2io.C2Refused):
        c2io.C2InputLog().check(kp.LEAN / "ohs4_sealed" / "brief.md")


def test_targets_are_spec_2_1_and_5_1():
    assert sum(c2io.AGENT.values()) == 13600 and sum(c2io.EVERYDAY.values()) == 7000
    assert sum(c2io.PROGRAM.values()) == 20600 and len(c2io.PROGRAM) == 17
    assert c2io.T37B == {"T37b": 2000} and c2io.CARRY == {"F5": 1500, "F6": 1000, "F11": 1000, "F4": 500}
    assert sum(c2io.TARGETS.values()) == c2io.NEW_MAX == 26600 and max(c2io.PROGRAM.values()) == 2400
    assert set(c2io.WAVE1) | set(c2io.WAVE2) == set(c2io.TARGETS) | set(c2io.NEW_FAMILIES) | set(c2io.POST_FREEZE) and not set(c2io.WAVE1) & set(c2io.WAVE2)   # A59: T46
    assert not set(c2io.TRANSFER_DEV) & set(c2io.TARGETS)
    assert c2io.NEW_FAMILIES == {"T40": 1333, "T41": 1166, "T42": 1333, "T43": 1166, "T44": 833, "T45": 833}
    assert c2io.ALL_TARGETS["GB"] == 15000 and c2io.ALL_TARGETS["MD"] == 12000 and c2io.ALL_TARGETS["RTW"] == 8000
    assert set(c2io.NEW_FAMILIES) | set(c2io.BLOCK_TARGETS) <= set(sel.TARGETS) and not set(c2io.BLOCK_TARGETS) & set(c2io.TARGETS)


def test_manifest_contract():
    got = {c2io.CAND: ("a" * 64, 10), c2io.REL: ("b" * 64, 3)}
    man = {"family": "T28", "files": {c2io.CAND: {"sha256": "a" * 64, "rows": 10},
                                      c2io.REL: {"sha256": "b" * 64, "rows": 3}}}
    assert c2io.manifest_problems("T28", man, got) == []
    bad = {"family": "T28", "files": {c2io.CAND: {"sha256": "c" * 64, "rows": 9}}}
    p = c2io.manifest_problems("T28", bad, got)
    assert any("sha256" in x for x in p) and any("10 rows" in x for x in p) and any("does not declare" in x for x in p)
    assert c2io.manifest_problems("T28", {}, got) == ["T28: MANIFEST has no 'files' record"]


def test_candidate_problems():
    rows, _ = fam_rows(n_units=30)
    assert c2io.candidate_problems("T28", rows) == []
    rows[0]["meta"]["sampler"] = "S5"
    rows[1]["meta"]["dev_only"] = True
    rows.append(dict(rows[2]))
    rows[3]["meta"] = dict(rows[3]["meta"], family="T29")
    p = c2io.candidate_problems("T28", rows)
    assert any("S5 / dev_only" in x and "2 " in x for x in p) and any("duplicate" in x for x in p)
    assert any("other families" in x for x in p)
    assert c2io.candidate_problems("T36", rows) == ["T36: transfer-dev family, never trained (spec 2.2)"]


def _snapshot(*paths):
    """(path, size, mtime) of every file under the given paths (absent paths give nothing)."""
    out = []
    for p in paths:
        if p.is_file():
            out.append((str(p), p.stat().st_size, p.stat().st_mtime_ns))
        elif p.is_dir():
            out += [(str(f), f.stat().st_size, f.stat().st_mtime_ns) for f in sorted(p.rglob("*")) if f.is_file()]
    return out


def test_writers_after_a38(tmp_path, monkeypatch):
    """A38 (13 Oct) froze OHS-4, so the writers pass the freeze guard. They still refuse never-open paths, paths
    outside lean/ and a PREREG text without A38, and the commands write only through c2io's guarded writers. Nothing
    reaches disk here: refused writes raise before any open, and the command runs use an empty C2 tree in tmp_path,
    with the writers and the progress log captured in memory."""
    before = _snapshot(sel.OUT, sel.LOG, sel.SHARDS, c2io.C2_PARTS)
    assert kp.a38_frozen()                                   # PREREG_FINAL.md holds the "Ruling A38" block
    kp.require_a38()
    c2io.require_a38()
    with pytest.raises(kp.DataBeforeFreeze):                 # the guard itself is unchanged
        c2io.write_json(sel.OUT / "never.json", {"x": 1}, prereg_text="no freeze in this text")
    with pytest.raises(kp.DataBeforeFreeze):
        c2io.write_jsonl(sel.OUT / "never.jsonl", [{"x": 1}], prereg_text="no freeze in this text")
    with pytest.raises(c2io.C2Refused):                      # never-open paths stay refused after A38
        c2io.write_json(kp.LEAN / "ohs4_sealed" / "never.json", {"x": 1})
    with pytest.raises(c2io.C2Refused):
        c2io.write_jsonl(kp.LEAN / "logs" / "jev_never.jsonl", [{"x": 1}])
    with pytest.raises(PermissionError):                     # outside lean/
        c2io.write_json(tmp_path / "never.json", {"x": 1})
    assert not (tmp_path / "never.json").exists()

    writes, logged = {}, []
    monkeypatch.setattr(c2io, "C2_PARTS", tmp_path / "c2_parts")           # no candidates on disk
    monkeypatch.setattr(c2io, "write_json", lambda p, obj, prereg_text=None: writes.__setitem__(str(p), obj) or "0")
    monkeypatch.setattr(c2io, "write_jsonl", lambda p, rows, prereg_text=None: writes.__setitem__(str(p), rows) or "0")
    monkeypatch.setattr(sel, "log_line", lambda path, msg: logged.append((str(path), msg)))
    sel.main(["select", "--fam", "T28"])                     # passes the guard; no candidates -> inputs record only
    assert writes == {str(sel.OUT / "select_inputs.json"): {"inputs": {}}}
    writes.clear()
    sel.main(["tasks", "--write-shards"])
    assert list(writes) == [str(sel.OUT / "crowd_tasks_c2.json")]
    t = writes[str(sel.OUT / "crowd_tasks_c2.json")]
    assert t["model"] == c2io.C1 and t["families"] == {} and t["estimate"]["reads"] == 0
    assert logged and all(p == str(sel.LOG) and m.startswith("c2_select: ") for p, m in logged)
    monkeypatch.setattr(kp, "PREREG", tmp_path / "prereg_without_a38.md")
    (tmp_path / "prereg_without_a38.md").write_text("> **Ruling A37 (13 Oct 2026)**\n", encoding="utf-8")
    with pytest.raises(kp.DataBeforeFreeze):                 # a PREREG without A38 still locks every command
        sel.main(["select", "--fam", "T28"])
    with pytest.raises(kp.DataBeforeFreeze):
        sel.main(["tasks", "--write-shards"])
    assert _snapshot(sel.OUT, sel.LOG, sel.SHARDS, kp.C2_PARTS) == before


# ---- the C1-only crowd ----------------------------------------------------------------------------------------------
def test_view_must_be_one_c1_view():
    v = {"settings": {"name": "q35_4b_main500k", "tta": False, "tta_choice": False, "tta_noul": False,
                      "perm_seed": None}}
    assert sel.view_problem(v) is None
    assert sel.view_problem({"settings": {**v["settings"], "name": "q35_4b_main500k_merged"}}) is None
    assert "C1-only" in sel.view_problem({"settings": {**v["settings"], "name": "q35_4b_pxE"}})
    assert "TTA" in sel.view_problem({"settings": {**v["settings"], "tta_choice": True}})
    assert sel.view_problem(None)


def test_c1_pg_is_c1_probability_on_gold_and_complete():
    rows = [{"id": "a", "qtype": "noul", "gold": 1}, {"id": "b", "qtype": "noul", "gold": 0},
            {"id": "c", "qtype": "choice", "gold": "X", "options": ["X", "Y"]}]
    probs = {"a": {"yes": 0.9, "no": 0.1}, "b": {"yes": 0.9, "no": 0.1}, "c": {"X": 0.3, "Y": 0.7}}
    assert sel.c1_pg(rows, probs) == {"a": 0.9, "b": 0.1, "c": 0.3}
    with pytest.raises(SystemExit, match="incomplete"):
        sel.c1_pg(rows, {"a": probs["a"]})


# ---- selection (crowd_select, unchanged) ----------------------------------------------------------------------------
def test_select_family_caps_balance_units_and_record():
    rows, rels = fam_rows()
    pg = crowd(rows)
    rec = sel.select_family("T28", rows, rels, pg, 300)
    rep = rec["report"]
    assert 270 <= rep["rows"] <= 300 and rec["seed"] == 20261013 and rec["key"] == "T28"
    assert rep["shares"].get("easy", 0) <= 0.25 + 1e-9 and rep["shares"].get("hard", 0) <= 0.30 + 1e-9
    assert rep["crowd_rule"].startswith("A37 (e)") and rec["crowd"] == {"c1": "q35_4b_main500k"}
    ids = set(rec["selected_ids"])
    yn = [r["gold"] for r in rows if r["id"] in ids and r["qtype"] == "noul"]
    assert abs(sum(yn) / len(yn) - 0.5) <= 0.03
    for x in rels:                                  # whole relation units only
        assert (x["a"] in ids) == (x["b"] in ids)
    assert rec["parts"] == [{"key": "T28", "ids": rec["selected_ids"]}]
    p = rep["chi2_label_x_bin"]["yes_no"]
    assert p is None or p > 0.01
    g5 = rec["g5"]
    assert g5["n_low"] == 0 and g5["n_sample"] <= 300      # no p_g < 0.05 in this crowd
    again = sel.select_family("T28", rows, rels, pg, 300)
    assert again["selected_ids"] == rec["selected_ids"]    # seeded, deterministic


def test_select_family_g5_lists_low_pg_and_refuses_s5():
    rows, rels = fam_rows(n_units=200)
    pg = {r["id"]: (0.01 if i % 4 == 0 else 0.7) for i, r in enumerate(rows)}
    rec = sel.select_family("T28", rows, rels, pg, 100)
    assert rec["g5"]["n_low"] == sum(1 for v in pg.values() if v < 0.05)
    rows[0]["meta"]["sampler"] = "S5"
    with pytest.raises(SystemExit, match="S5"):
        sel.select_family("T28", rows, rels, pg, 100)


def test_g13_exclusion_removes_whole_units():
    rows, rels = fam_rows(n_units=60)
    pair = rels[0]
    keep, info = sel.drop_excluded(rows, rels, {pair["b"]})
    ids = {r["id"] for r in keep}
    assert pair["a"] not in ids and pair["b"] not in ids and info["units_removed"] == 1 and info["rows_removed"] == 2
    rec = sel.select_family("T28", rows, rels, crowd(rows), 40, drop_ids={pair["a"]})
    assert pair["a"] not in rec["selected_ids"] and rec["exclude_ids"]["units_removed"] == 1


# ---- --exclude-ids: the G13 log check, one function shared with the mixer (16 Oct 2026, guard review 3) -------------
# An isolated C2 layout under tmp_path: C2_PARTS and the carry-over candidates live in the test folder, the dev files are
# tmp_path/dev/**.jsonl (c2_select.current_dev_files follows). g13_log() writes a guarded G13 log the way g13_c2._record
# does (inputs_at_start + inputs_at_start_paths + engine.inputs_sha256.train), consistent with the files it just made.
import json  # noqa: E402
import types  # noqa: E402

NAME_RUN = (("c2_seed_", "seed"), ("c2_cand_", "candidates"), ("c2_carry_", "carry"), ("c2_final", "final"))


@pytest.fixture()
def g13w(tmp_path, monkeypatch):
    parts, dev = tmp_path / "c2_parts", tmp_path / "dev"
    dev.mkdir()
    monkeypatch.setattr(c2io, "C2_PARTS", parts)
    real = c2io.fam_files

    def fam_files(fam, root=None):
        f = real(fam, root)
        if fam in c2io.CARRY:                                       # keep the round-1 layout inside the test folder
            f = {**f, "cand": tmp_path / "r1" / fam / "out" / "candidates_r1.jsonl"}
        return f

    monkeypatch.setattr(c2io, "fam_files", fam_files)
    for n in ("c2_mixdev.jsonl", "c2_transfer_dev.jsonl"):
        (dev / n).write_text(json.dumps({"id": n}) + "\n")
    monkeypatch.setattr(sel, "current_dev_files", lambda: sorted(dev.rglob("*.jsonl")))
    return types.SimpleNamespace(tmp=tmp_path, dev=dev, parts=parts)


def g13_file_sha(p) -> str:
    return sel.sha256_file(Path(p))


def g13_log(w, name: str, run: str | None = None, block: str | None = None, **kw) -> Path:
    """A guarded G13 log for `name` (c2_cand_<B>.json ...), made consistent with the files under the isolated layout.
    Keyword values override the record's keys; None removes a key."""
    stem = name.removesuffix(".json")
    run = run or next((r for pre, r in NAME_RUN if stem.startswith(pre)), "candidates")
    block = block or ("final" if run == "final" else stem.split("_", 2)[-1])
    train = c2io.C2_PARTS / "c2_train.jsonl" if run == "final" else c2io.fam_files(block)["cand"]
    if not train.exists():
        train.parent.mkdir(parents=True, exist_ok=True)
        train.write_text(json.dumps({"id": f"{block}-r1"}) + "\n")
    rel = sel.lean_rel(train)
    ias, paths = {train.name: g13_file_sha(train)}, {train.name: rel}
    for q in sel.current_dev_files():
        key = q.name if sum(x.name == q.name for x in sel.current_dev_files()) == 1 else sel.lean_rel(q)
        ias[key], paths[key] = g13_file_sha(q), sel.lean_rel(q)
    d = {"set": stem, "run": run, "block": block, "tool": sel.G13_TOOL, "drop_ids": ["r1", "r2"], "complete": True,
         "incomplete_why": [], "inputs_at_start": ias, "inputs_at_start_paths": paths,
         "engine": {"inputs_sha256": {"train": {rel: g13_file_sha(train)}, "seeds": {}}}} | kw
    f = w.tmp / name
    f.write_text(json.dumps({k: v for k, v in d.items() if v is not None}))
    return f


def g13_probs(*files, **kw):
    return sel.g13_log_problems(c2io.C2InputLog(), [str(f) for f in files], **kw)


PLAIN_LISTS = {                                                  # the three drop lists with no completeness key
    "REPLAY_DENY_A46.json": {"set": "replay_deny_a46", "drop_ids": ["a", "b"], "note": "no complete key"},
    "REPLAY_UNSCREENED_A46.json": {"set": "x", "drop_ids": [], "note": "empty list"},
    "pool_drops_r1.json": {"set": "pool_drops_r1", "drop_ids": ["c"], "note": "x"}}


def test_exclude_ids_refuses_the_plain_drop_lists_as_it_always_did(g13w):
    """Guard review 4 (16 Oct 2026): the backup c2_select refused EVERY --exclude-ids file whose "complete" was not true, the
    replay deny lists and the round-1 pool drops included (they hold no such key). An exemption for those three paths
    opened the gate (a loosening) and is gone: no file is exempt, by path or by name, and no exemption list exists."""
    for name in ("plain_drop_lists", "REPLAY_DENY", "REPLAY_UNSCREENED", "POOL_DROPS_R1"):
        assert not hasattr(sel, name), name                                       # nothing left to match a path against
    ilog = c2io.C2InputLog()
    (g13w.tmp / "elsewhere").mkdir()
    for name, body in PLAIN_LISTS.items():
        for f in (g13w.tmp / name, g13w.tmp / "elsewhere" / name, g13w.tmp / ("copy_of_" + name)):
            f.write_text(json.dumps(body))
            with pytest.raises(SystemExit, match="G13 log is not complete"):
                sel.drop_ids_of(ilog, [f])
            assert len(sel.plain_list_problems(ilog, [f])) == 1 and sel.g13_log_problems(ilog, [f]) == []
        link = g13w.tmp / f"link_to_{name}"
        link.symlink_to(g13w.tmp / name)                                          # a link to one of them is no way round it
        with pytest.raises(SystemExit, match="G13 log is not complete"):
            sel.drop_ids_of(ilog, [link])
    with pytest.raises(SystemExit, match="G13 log is not complete"):              # one of them among complete ones: refused whole
        ok = g13w.tmp / "g13_ok.json"
        ok.write_text(json.dumps({"complete": True, "drop_ids": ["z"]}))
        sel.drop_ids_of(ilog, [ok, g13w.tmp / "pool_drops_r1.json"])
    assert sel.drop_ids_of(ilog, None) == set() and sel.drop_ids_of(ilog, []) == set()
    # a G13-shaped record sitting at one of those names is judged as a G13 log (no path exempts it from that check either)
    bad = g13_log(g13w, "pool_drops_r1.json", run="candidates", block="T28", complete=False, incomplete_why=["x"])
    with pytest.raises(SystemExit, match="incomplete G13 log"):
        sel.drop_ids_of(ilog, [bad])


@pytest.mark.skipif(not (c2io.LEAN / "c2_build/replay_screen/REPLAY_DENY_A46.json").exists(), reason="real lists absent")
def test_the_real_replay_and_round1_drop_lists_are_refused_by_exclude_ids():
    """The backup c2_select refused logs/decontam_counts/pool_drops_r1.json and both replay_screen lists (no complete key); so
    does this one. (mix_c2 --decontam-drops reads them; --exclude-ids never did.)"""
    files = [c2io.LEAN / "c2_build/replay_screen" / n for n in ("REPLAY_DENY_A46.json", "REPLAY_UNSCREENED_A46.json")]
    files.append(c2io.LEAN / "logs/decontam_counts/pool_drops_r1.json")
    seen = 0
    for f in files:
        if not f.exists():
            continue
        d = json.loads(f.read_text())
        if isinstance(d, dict) and d.get("complete") is True and not d.get("incomplete_why"):
            continue                                                              # completed since: it would pass, as before
        seen += 1
        with pytest.raises(SystemExit, match=f"{f.name}: G13 log is not complete"):
            sel.drop_ids_of(c2io.C2InputLog(), [f])
        assert len(sel.plain_list_problems(c2io.C2InputLog(), [f])) == 1
    assert seen >= 1


def test_drop_ids_of_keeps_the_complete_gate_for_every_other_list(g13w, monkeypatch):
    """Before the guard EVERY --exclude-ids file needed complete = True. A file that is not one of the three plain lists
    keeps that gate, G13 log or not: a partial round-1 log (F6.json: tool decontam_g13.py, complete false) and a plain
    drop list with no complete key are refused whole, naming the file; complete ones are merged."""
    tmp = g13w.tmp
    ok = tmp / "g13_ok.json"
    ok.write_text(json.dumps({"complete": True, "drop_ids": ["a", "b"]}))
    ok2 = tmp / "g13_ok2.json"
    ok2.write_text(json.dumps({"complete": True, "training_ids_to_drop": ["b", "c"]}))
    r1_ok = tmp / "round1_complete.json"                                         # a complete round-1 log: used, as before
    r1_ok.write_text(json.dumps({"set": "F5", "tool": "c_build/decontam_g13.py", "complete": True, "ids": ["d"]}))
    assert sel.drop_ids_of(c2io.C2InputLog(), [ok, ok2, r1_ok]) == {"a", "b", "c", "d"}
    bad = {"g13_false.json": {"complete": False, "drop_ids": ["a"], "incomplete_why": ["x"]},
           "g13_missing.json": {"drop_ids": ["a"]},
           "g13_string.json": {"complete": "true", "drop_ids": ["a"]},
           "g13_one.json": {"complete": 1, "drop_ids": ["a"]},
           "g13_null.json": {"complete": None, "drop_ids": ["a"]},
           "g13_list.json": ["a"],
           "ids_only.json": {"ids": [1, 2]},                                     # a plain list is not one of the three
           "F6.json": {"set": "F6", "tool": "c_build/decontam_g13.py", "drop_ids": ["a"], "complete": False,
                       "incomplete_why": ["x", "y"], "seeds_clean": False},      # the real partial round-1 log, in shape
           "sealed_drop_r1.json": {"set": "sealed", "drop_ids": ["a"], "complete": False},
           "why_listed.json": {"complete": True, "drop_ids": ["a"], "incomplete_why": ["x"]},
           "why_text.json": {"complete": True, "drop_ids": ["a"], "incomplete_why": "x changed"},
           "tool_removed.json": {"set": "something", "drop_ids": ["a"], "complete": False, "incomplete_why": []}}
    for name, body in bad.items():
        f = tmp / name
        f.write_text(json.dumps(body))
        with pytest.raises(SystemExit, match=name):                              # the message names the file
            sel.drop_ids_of(c2io.C2InputLog(), [f])
        with pytest.raises(SystemExit, match="not complete"):
            sel.drop_ids_of(c2io.C2InputLog(), [ok, f])                          # one bad log among good ones still refuses
        assert len(sel.plain_list_problems(c2io.C2InputLog(), [f])) == 1, name
    no_list = tmp / "g13_nolist.json"
    no_list.write_text(json.dumps({"complete": True}))
    with pytest.raises(SystemExit, match="no drop id list"):                     # a complete log without an id list still refuses
        sel.drop_ids_of(c2io.C2InputLog(), [no_list])


def test_a_g13_c2_record_is_checked_as_one_even_with_its_tool_key_removed_or_its_file_renamed(g13w, monkeypatch):
    """A g13_c2 record carries inputs_at_start / engine / a c2_* set name. Taking its tool key away or renaming the file
    must not move it out of the G13 check (it is refused as "not a g13_c2.py record", the stale check runs on it)."""
    plain = {"set": "A46 replay-wide label-noise screen", "drop_ids": ["a"], "note": "x", "inputs_sha256": {"a": "b"},
             "counts": {}, "by_source": {}}
    assert not sel.is_g13_log(plain, "REPLAY_DENY_A46.json")
    assert not sel.is_g13_log({"set": "F6", "tool": "c_build/decontam_g13.py", "complete": True, "drop_ids": []}, "F6.json")
    assert not sel.is_g13_log(["a"], "c2_x.json") and not sel.is_g13_log(None, "x.json")
    for body in ({"inputs_at_start": {}}, {"inputs_at_start_paths": {}}, {"engine": {}}, {"set": "c2_cand_T28"},
                 {"tool": "./c2_build/g13_c2.py"}, {"tool": "other/g13_c2.py"}):
        assert sel.is_g13_log({"drop_ids": [], **body}, "x.json"), body
    assert sel.is_g13_log({"drop_ids": []}, "c2_hand_made.json")
    # a partial one, tool key removed, odd name: refused as a G13 log (not just by the complete gate)
    for kw in ({"complete": False, "incomplete_why": ["x"]}, {}):
        f = g13_log(g13w, "my_copy.json", block="T28", tool=None, **kw)
        p = g13_probs(f)
        assert any("not a g13_c2.py record" in x for x in p), (kw, p)
        with pytest.raises(SystemExit, match="not a g13_c2.py record"):
            sel.drop_ids_of(c2io.C2InputLog(), [f])
    # ... and with the right tool but complete = True it is judged by the stale check like any other
    f = g13_log(g13w, "my_copy.json", block="T28")
    assert g13_probs(f) == []
    c2io.fam_files("T28")["cand"].write_text("changed\n")
    assert g13_probs(f) == [stale_msg("my_copy", "candidates_c2.jsonl", "T28")]
    named = g13w.tmp / "renamed.json"
    named.write_text(json.dumps({"set": "c2_cand_T28", "complete": True, "drop_ids": ["a"], "incomplete_why": []}))
    assert any("not a g13_c2.py record" in x for x in g13_probs(named))


@pytest.mark.skipif(not (c2io.LEAN / "logs/decontam_counts/F6.json").exists(), reason="real round-1 log absent")
def test_a_real_partial_round1_log_is_still_refused_by_exclude_ids():
    """logs/decontam_counts/F6.json is a partial round-1 log (complete false): the backup c2_select refused it, so does this."""
    f = c2io.LEAN / "logs/decontam_counts/F6.json"
    d = json.loads(f.read_text())
    if d.get("complete") is True and not d.get("incomplete_why"):
        pytest.skip("F6.json was completed since")
    with pytest.raises(SystemExit, match="F6.json: G13 log is not complete"):
        sel.drop_ids_of(c2io.C2InputLog(), [f])


def test_drop_ids_of_refuses_a_g13_log_that_is_not_complete(g13w):
    """A C2 G13 log (tool g13_c2.py or named c2_*.json) must pass the mixer's check: complete true, no reasons, guarded.
    Any problem refuses the whole run and names the file. Real files through the guarded C2InputLog."""
    ok = g13_log(g13w, "c2_cand_T28.json")
    ok2 = g13_log(g13w, "c2_cand_T01.json", drop_ids=None, training_ids_to_drop=["r2", "r3"])
    assert sel.drop_ids_of(c2io.C2InputLog(), [ok, ok2]) == {"r1", "r2", "r3"}
    bad = {"c2_cand_T06.json": {"complete": False, "incomplete_why": ["x"]},
           "c2_cand_T07.json": {"complete": None},
           "c2_cand_T12.json": {"complete": "true"},
           "c2_cand_T23.json": {"complete": 1},
           "c2_cand_T24.json": {"incomplete_why": ["x changed during the run: re-run"]},       # complete true, reasons listed
           "c2_cand_T25.json": {"incomplete_why": None},                                         # no reasons record
           "c2_cand_T26.json": {"inputs_at_start": None},                                        # pre-guard
           "c2_cand_T29.json": {"inputs_at_start": {}},
           "c2_carry_F5.json": {"run": "carry", "inputs_at_start": None},
           "c2_final.json": {"run": "final", "inputs_at_start": None},
           "my_g13_copy.json": {"complete": False, "incomplete_why": ["x"]}}                      # tool, not the name
    for name, kw in bad.items():
        f = g13_log(g13w, name, **kw)
        with pytest.raises(SystemExit, match=name.removesuffix(".json")):               # the message names the log
            sel.drop_ids_of(c2io.C2InputLog(), [f])
        with pytest.raises(SystemExit, match="refused"):
            sel.drop_ids_of(c2io.C2InputLog(), [ok, f])                                 # one bad log among good ones
    named = g13w.tmp / "c2_hand_made.json"                                              # named like a C2 log, no tool
    named.write_text(json.dumps({"complete": True, "drop_ids": ["a"]}))
    with pytest.raises(SystemExit, match="not a g13_c2.py record"):
        sel.drop_ids_of(c2io.C2InputLog(), [named])
    variant = g13_log(g13w, "my_variant_copy.json", tool="./c2_build/g13_c2.py")           # another spelling of the tool path
    with pytest.raises(SystemExit, match="not a g13_c2.py record"):
        sel.drop_ids_of(c2io.C2InputLog(), [variant])
    seed = g13_log(g13w, "c2_seed_T28.json", inputs_at_start=None, inputs_at_start_paths=None, engine=None, drop_ids=[])
    assert sel.drop_ids_of(c2io.C2InputLog(), [seed]) == set()               # a seed log needs no inputs_at_start


def test_the_g13_check_is_one_function_for_select_and_the_mixer(g13w, monkeypatch):
    """Both call c2_select.g13_log_problems: a stub there is seen by --exclude-ids (and, in test_mix_c2_g13_logs, by the mixer)."""
    f = g13_log(g13w, "c2_cand_T28.json")
    seen = []

    def stub(ilog, files, **kw):
        seen.append((list(files), sorted(kw)))
        return ["c2_cand_T28: stub problem"]

    monkeypatch.setattr(sel, "g13_log_problems", stub)
    with pytest.raises(SystemExit, match="stub problem"):
        sel.drop_ids_of(c2io.C2InputLog(), [f])
    assert seen and str(f) in map(str, seen[0][0])


def stale_msg(name, fname, block):
    return f"{name}: stale G13 log ({fname} changed after the run): re-run G13 for {block}"


def test_a_fresh_guarded_log_is_not_stale_and_a_changed_candidates_file_is(g13w):
    f = g13_log(g13w, "c2_cand_T28.json")
    assert g13_probs(f) == []
    cand = c2io.fam_files("T28")["cand"]
    cand.write_text(cand.read_text() + json.dumps({"id": "late"}) + "\n")             # the candidates changed after the run
    assert g13_probs(f) == [stale_msg("c2_cand_T28", "candidates_c2.jsonl", "T28")]
    with pytest.raises(SystemExit, match=r"stale G13 log \(candidates_c2.jsonl changed after the run\): re-run G13 for T28"):
        sel.drop_ids_of(c2io.C2InputLog(), [f])
    cand.unlink()                                                                       # gone is a change too
    assert g13_probs(f) == [stale_msg("c2_cand_T28", "candidates_c2.jsonl", "T28")]
    other = g13_log(g13w, "c2_cand_T01.json")                                          # another block's log is unaffected
    assert g13_probs(other) == []


def test_the_training_sha_is_read_from_the_inputs_at_start_and_from_the_engine_record(g13w):
    """Either record alone ties the log to the file; both are compared when both are there."""
    f = g13_log(g13w, "c2_cand_T28.json")
    d = json.loads(f.read_text())
    rel = sel.lean_rel(c2io.fam_files("T28")["cand"])
    wrong = "0" * 64
    only_ias = {**d, "engine": None}
    only_eng = {**d, "inputs_at_start": {k: v for k, v in d["inputs_at_start"].items() if k != "candidates_c2.jsonl"}}
    for body, expect in ((only_ias, []), (only_eng, [])):
        f.write_text(json.dumps({k: v for k, v in body.items() if v is not None}))
        assert g13_probs(f) == expect
    for body in ({**d, "engine": {"inputs_sha256": {"train": {rel: wrong}}}},                 # the engine's sha differs
                 {**d, "inputs_at_start": {**d["inputs_at_start"], "candidates_c2.jsonl": wrong}},
                 {**only_eng, "engine": {"inputs_sha256": {"train": {rel: wrong}}}}):
        f.write_text(json.dumps(body))
        assert g13_probs(f) == [stale_msg("c2_cand_T28", "candidates_c2.jsonl", "T28")]
    # a guarded log that records no training sha at all cannot be tied to the file: refused
    none = {**only_eng, "engine": None}
    f.write_text(json.dumps({k: v for k, v in none.items() if v is not None}))
    p = g13_probs(f)
    assert len(p) == 1 and "stale G13 log (candidates_c2.jsonl not recorded in the log)" in p[0]
    # an older record (names only: no inputs_at_start_paths, no engine) is still tied through the file name
    names_only = {**d, "engine": None, "inputs_at_start_paths": None}
    f.write_text(json.dumps({k: v for k, v in names_only.items() if v is not None}))
    assert g13_probs(f) == []
    c = c2io.fam_files("T28")["cand"]
    c.write_text(c.read_text() + "{}\n")
    assert g13_probs(f) == [stale_msg("c2_cand_T28", "candidates_c2.jsonl", "T28")]


def test_a_changed_or_new_or_gone_dev_file_makes_a_g13_log_stale(g13w):
    f = g13_log(g13w, "c2_cand_T28.json")
    assert g13_probs(f) == []
    mixdev = g13w.dev / "c2_mixdev.jsonl"
    mixdev.write_text(mixdev.read_text() + json.dumps({"id": "rebuilt"}) + "\n")           # a dev file changed
    assert g13_probs(f) == [stale_msg("c2_cand_T28", "c2_mixdev.jsonl", "T28")]
    f = g13_log(g13w, "c2_cand_T28.json")                                                 # a log of the new bytes is fine
    assert g13_probs(f) == []
    new = g13w.dev / "T28" / "mixdev_S5.jsonl"                                             # a dev file that exists now but is
    new.parent.mkdir()                                                                     # not in the log (a glob target)
    new.write_text(json.dumps({"id": "m1"}) + "\n")
    assert g13_probs(f) == [stale_msg("c2_cand_T28", "mixdev_S5.jsonl", "T28")]
    with pytest.raises(SystemExit, match="stale G13 log"):
        sel.drop_ids_of(c2io.C2InputLog(), [f])
    f = g13_log(g13w, "c2_cand_T28.json")                                                 # recorded with the new file: fine
    assert g13_probs(f) == []
    (g13w.dev / "c2_transfer_dev.jsonl").unlink()                                          # a recorded dev file is gone
    assert g13_probs(f) == [stale_msg("c2_cand_T28", "c2_transfer_dev.jsonl", "T28").replace(
        "changed after the run)", "changed after the run (gone))")]
    # two dev files share a basename: the lean-relative path names the file
    f = g13_log(g13w, "c2_cand_T28.json")
    other = g13w.dev / "T01" / "mixdev_S5.jsonl"
    other.parent.mkdir()
    other.write_text(json.dumps({"id": "m2"}) + "\n")
    p = g13_probs(f)
    assert len(p) == 1 and sel.lean_rel(other) in p[0] and "stale G13 log" in p[0]


def test_a_final_or_carry_log_is_tied_to_its_own_training_file(g13w):
    final = g13_log(g13w, "c2_final.json")
    carry = g13_log(g13w, "c2_carry_F5.json")
    assert g13_probs(final, carry) == []
    train = c2io.C2_PARTS / "c2_train.jsonl"
    train.write_text(train.read_text() + "{}\n")
    assert g13_probs(final, carry) == [stale_msg("c2_final", "c2_train.jsonl", "final")]
    r1 = c2io.fam_files("F5")["cand"]
    r1.write_text(r1.read_text() + "{}\n")
    assert g13_probs(carry) == [stale_msg("c2_carry_F5", "candidates_r1.jsonl", "F5")]


def test_a_seed_log_is_not_tied_to_the_candidates_or_dev_files(g13w):
    seed = g13_log(g13w, "c2_seed_T28.json", drop_ids=[])
    c2io.fam_files("T28")["cand"].write_text("changed\n")
    (g13w.dev / "c2_mixdev.jsonl").write_text("changed\n")
    assert g13_probs(seed) == []


def test_the_stale_check_does_not_repeat_a_pre_guard_message_and_names_the_block(g13w):
    pre = g13_log(g13w, "c2_cand_T28.json", inputs_at_start=None)
    p = g13_probs(pre)
    assert len(p) == 1 and "pre-guard G13 log" in p[0]                                    # one message, no stale noise
    no_block = g13_log(g13w, "weird.json", run="candidates", block="T28", block_=None, set="odd")   # tool names it
    d = json.loads(no_block.read_text())
    d.pop("block")
    no_block.write_text(json.dumps(d))
    p = g13_probs(no_block)
    assert len(p) == 1 and "cannot tell which block" in p[0]


def test_the_stale_check_applies_the_never_open_rule_before_any_stat(g13w, monkeypatch):
    import os
    f = g13_log(g13w, "c2_cand_T28.json")
    d = json.loads(f.read_text())
    d["block"] = "T28ohs"                                                                  # a block name the guard refuses
    f.write_text(json.dumps(d))
    seen = []
    real = {n: getattr(os, n) for n in ("stat", "lstat")}

    def spy(name):
        def w(p, *a, **k):
            if "ohs" in str(p).lower():
                seen.append(str(p))
            return real[name](p, *a, **k)
        return w

    for n in real:
        monkeypatch.setattr(os, n, spy(n))
    p = g13_probs(f)
    assert len(p) == 1 and "training file refused" in p[0] and seen == [], (p, seen)
    # the same for a dev file on the never-open list
    f = g13_log(g13w, "c2_cand_T01.json")
    bad = g13w.dev / "x_ohs_dev.jsonl"
    bad.write_text("{}\n")
    seen.clear()
    p = g13_probs(f)
    assert len(p) == 1 and "refused" in p[0] and seen == [], (p, seen)


# ---- guard review 3 (16 Oct 2026): the never-open rule before any stat / listing, the names-only record, the logged inputs
REAL_CURRENT_DEV_FILES = sel.current_dev_files            # the g13w fixture replaces sel.current_dev_files; this is the real one


@pytest.fixture()
def nopen(monkeypatch):
    """Every path holding NOPEN is on the never-open list; any stat / open / listing of one is recorded in the returned list
    (clear it after setting a test up: writing the fixture files is not the program's doing)."""
    import builtins
    import io
    import os
    seen = []
    monkeypatch.setattr(c2io, "refusal", lambda p: "NOPEN" if "NOPEN" in str(p) else None)

    def spy(fn):
        def watched(p, *a, **k):
            if "NOPEN" in str(p):
                seen.append(str(p))
            return fn(p, *a, **k)
        return watched

    for mod, attr in ((os, "stat"), (os, "lstat"), (os, "open"), (os, "scandir"), (os, "listdir"), (os, "readlink"),
                      (builtins, "open"), (io, "open")):
        monkeypatch.setattr(mod, attr, spy(getattr(mod, attr)))
    return seen


def test_sha_if_file_refuses_a_never_open_path_before_any_stat_and_logs_the_input(tmp_path, nopen):
    ok, bad = tmp_path / "ok.jsonl", tmp_path / "NOPEN.jsonl"
    ok.write_text("1")
    bad.write_text("1")
    ilog = c2io.C2InputLog()
    nopen.clear()
    assert sel._sha_if_file(ilog, ok, {}) == g13_file_sha(ok)
    assert [e["sha256"] for e in ilog.entries.values()] == [g13_file_sha(ok)]       # logged like every input of the run
    assert sel._sha_if_file(ilog, tmp_path / "gone.jsonl", {}) is None
    assert len(ilog.entries) == 1                                                     # a missing file is not an input
    with pytest.raises(c2io.C2Refused):
        sel._sha_if_file(ilog, bad, {})
    assert nopen == [], nopen
    cache = {}
    assert sel._sha_if_file(ilog, ok, cache) == sel._sha_if_file(ilog, ok, cache) == g13_file_sha(ok)   # cached per run


def test_the_stale_check_logs_the_candidates_and_dev_files_it_hashes(g13w):
    f = g13_log(g13w, "c2_cand_T28.json")
    ilog = c2io.C2InputLog()
    assert sel.g13_log_problems(ilog, [str(f)]) == []
    logged = {Path(k).name for k in ilog.entries}                                     # keys: repo-relative or absolute paths
    assert {"candidates_c2.jsonl", "c2_mixdev.jsonl", "c2_transfer_dev.jsonl", "c2_cand_T28.json"} <= logged, logged


def test_g13_log_problems_and_drop_ids_of_refuse_a_never_open_file_before_any_stat(g13w, nopen):
    bad = g13w.tmp / "NOPEN_c2_cand_T28.json"
    bad.write_text(json.dumps({"set": "c2_cand_T28", "drop_ids": ["a"], "complete": True}))
    nopen.clear()
    for call in (lambda: sel.g13_log_problems(c2io.C2InputLog(), [str(bad)]),
                 lambda: sel.g13_log_problems(c2io.C2InputLog(), [], exempt=(str(bad),)),
                 lambda: sel.plain_list_problems(c2io.C2InputLog(), [str(bad)]),
                 lambda: sel.drop_ids_of(c2io.C2InputLog(), [str(bad)])):
        with pytest.raises(c2io.C2Refused):
            call()
    assert nopen == [], nopen
    ok = g13_log(g13w, "c2_cand_T28.json")                                            # control: the same call on a clean file
    assert sel.g13_log_problems(c2io.C2InputLog(), [str(ok)], exempt=(str(g13w.tmp / "other.json"),)) == []


def test_a_g13_log_is_judged_by_the_g13_check_only(g13w):
    bad = g13_log(g13w, "c2_cand_T28.json", complete=False, incomplete_why=["x"])
    ilog = c2io.C2InputLog()
    assert sel.plain_list_problems(ilog, [bad]) == []                      # a G13 log is the other check's business
    with pytest.raises(SystemExit) as e:
        sel.drop_ids_of(ilog, [bad])
    assert "G13 log is not complete" not in str(e.value) and "incomplete G13 log" in str(e.value)    # one message, not two


def test_current_dev_files_never_stats_or_scans_a_never_open_folder(tmp_path, monkeypatch, nopen):
    data, parts = tmp_path / "data", tmp_path / "data" / "c2_parts"
    ok = parts / "fam_ok" / "out" / "mixdev_S5.jsonl"
    bad = parts / "NOPEN_fam" / "out" / "mixdev_S5.jsonl"
    for f in (ok, bad, data / "c2_mixdev.jsonl", data / "c2_transfer_dev.jsonl", parts / "plain_file"):
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("{}\n")
    monkeypatch.setattr(c2io, "DATA", data)
    monkeypatch.setattr(c2io, "C2_PARTS", parts)
    nopen.clear()
    assert REAL_CURRENT_DEV_FILES() == sorted([data / "c2_mixdev.jsonl", data / "c2_transfer_dev.jsonl", ok])
    assert nopen == [], nopen                                       # NOPEN_fam, NOPEN_fam/out ... were never touched
    monkeypatch.setattr(c2io, "C2_PARTS", tmp_path / "NOPEN_parts")      # the c2_parts folder itself refused
    (tmp_path / "NOPEN_parts" / "x" / "out").mkdir(parents=True)
    (tmp_path / "NOPEN_parts" / "x" / "out" / "mixdev_S5.jsonl").write_text("{}\n")
    nopen.clear()
    assert REAL_CURRENT_DEV_FILES() == sorted([data / "c2_mixdev.jsonl", data / "c2_transfer_dev.jsonl"])
    assert nopen == [], nopen


def test_current_dev_files_does_not_stat_a_dev_file_the_rule_refuses(tmp_path, monkeypatch):
    """A refused dev file (by its own path, not through a folder name) is neither stat-ed nor returned."""
    import os
    data, parts = tmp_path / "data", tmp_path / "data" / "c2_parts"
    files = {"mixdev": data / "c2_mixdev.jsonl", "transfer": data / "c2_transfer_dev.jsonl",
             "a": parts / "a" / "out" / "mixdev_S5.jsonl", "b": parts / "b" / "out" / "mixdev_S5.jsonl",
             "c": parts / "c" / "out" / "mixdev_S5.jsonl"}
    for f in files.values():
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("{}\n")
    refused = {str(files["mixdev"]), str(files["b"]), str(parts / "c")}      # c: the FOLDER is refused, its file's path is not
    monkeypatch.setattr(c2io, "refusal", lambda p: "refused" if str(p) in refused else None)
    monkeypatch.setattr(c2io, "DATA", data)
    monkeypatch.setattr(c2io, "C2_PARTS", parts)
    seen = []
    for name in ("stat", "lstat"):
        real = getattr(os, name)
        monkeypatch.setattr(os, name, lambda p, *a, real=real, **k: (seen.append(str(p)) if str(p) in refused else None,
                                                                    real(p, *a, **k))[1])
    assert REAL_CURRENT_DEV_FILES() == sorted([files["transfer"], files["a"]])
    assert seen == [], seen


def gone_msg(name, fname, block):
    return f"{name}: stale G13 log ({fname} changed after the run (gone)): re-run G13 for {block}"


def test_a_gone_dev_file_is_stale_also_when_the_record_names_it_by_file_name_only(g13w):
    """An older record (inputs_at_start by file name, no inputs_at_start_paths): a changed or new dev file was caught, a
    GONE one was not (g13_c2 status says 'gone: no such file now')."""
    mixdev_s5 = g13w.dev / "T28" / "mixdev_S5.jsonl"
    mixdev_s5.parent.mkdir()
    mixdev_s5.write_text(json.dumps({"id": "m1"}) + "\n")
    f = g13_log(g13w, "c2_cand_T28.json", inputs_at_start_paths=None)
    assert set(json.loads(f.read_text())["inputs_at_start"]) >= {"candidates_c2.jsonl", "mixdev_S5.jsonl", "c2_mixdev.jsonl"}
    assert "inputs_at_start_paths" not in json.loads(f.read_text())
    assert g13_probs(f) == []
    (g13w.dev / "c2_transfer_dev.jsonl").unlink()
    assert g13_probs(f) == [gone_msg("c2_cand_T28", "c2_transfer_dev.jsonl", "T28")]
    with pytest.raises(SystemExit, match=r"c2_transfer_dev.jsonl changed after the run \(gone\)"):
        sel.drop_ids_of(c2io.C2InputLog(), [f])
    mixdev_s5.unlink()
    assert g13_probs(f) == [gone_msg("c2_cand_T28", "c2_transfer_dev.jsonl", "T28"),
                            gone_msg("c2_cand_T28", "mixdev_S5.jsonl", "T28")]
    # the same record with the paths: the same messages (the path-recorded case was always caught)
    mixdev_s5.write_text(json.dumps({"id": "m1"}) + "\n")
    (g13w.dev / "c2_transfer_dev.jsonl").write_text(json.dumps({"id": "c2_transfer_dev.jsonl"}) + "\n")
    f = g13_log(g13w, "c2_cand_T28.json")
    mixdev_s5.unlink()
    assert g13_probs(f) == [gone_msg("c2_cand_T28", "mixdev_S5.jsonl", "T28")]
    # a recorded name that is not a dev file (an unknown key) is not read as a gone dev file
    d = json.loads(f.read_text())
    d["inputs_at_start"]["some_other_input.jsonl"] = "0" * 64
    f.write_text(json.dumps(d))
    assert g13_probs(f) == [gone_msg("c2_cand_T28", "mixdev_S5.jsonl", "T28")]


def test_a_file_name_alone_does_not_vouch_for_two_dev_files_that_share_it(g13w):
    a = g13w.dev / "T28" / "mixdev_S5.jsonl"
    a.parent.mkdir()
    a.write_text(json.dumps({"id": "m1"}) + "\n")
    f = g13_log(g13w, "c2_cand_T28.json", inputs_at_start_paths=None)         # names only: "mixdev_S5.jsonl" -> one sha
    assert g13_probs(f) == []
    b = g13w.dev / "T01" / "mixdev_S5.jsonl"                                  # a second file with that name, same bytes
    b.parent.mkdir()
    b.write_text(a.read_text())
    p = g13_probs(f)
    assert len(p) == 2 and all("stale G13 log" in x and "re-run G13 for T28" in x for x in p), p
    assert any(sel.lean_rel(a) in x for x in p) and any(sel.lean_rel(b) in x for x in p)    # each named by its path


def test_select_and_carry_run_the_g13_check_before_they_read_a_family(g13w, monkeypatch):
    """cmd_select / cmd_carry call drop_ids_of first: a stale G13 log stops them before any family file is read."""
    monkeypatch.setattr(c2io, "require_a38", lambda prereg_text=None: None)
    monkeypatch.setattr(sel, "available", lambda fams=None: pytest.fail("a family was read"))
    stale = g13_log(g13w, "c2_cand_T28.json")
    c2io.fam_files("T28")["cand"].write_text("changed\n")
    ns = types.SimpleNamespace(fam=None, exclude_ids=[str(stale)])
    for cmd in (sel.cmd_select, sel.cmd_carry):
        with pytest.raises(SystemExit, match="stale G13 log"):
            cmd(ns)


def test_reselect_keeps_the_easy_keep_and_balance():
    rows, rels = fam_rows(n_units=900, seed=4)
    pg = crowd(rows, seed=3, vals=(0.99, 0.999, 0.6, 0.8, 0.5, 0.1))
    rec = sel.select_family("T28", rows, rels, pg, 500)
    chosen = set(rec["selected_ids"])
    sub = [r for r in rows if r["id"] in chosen]
    srel = [x for x in rels if x["a"] in chosen and x["b"] in chosen]
    units = cs.units_of(sub, srel)
    bins = {r["id"]: cs.bin_of(pg[r["id"]]) for r in sub}
    assert any(all(bins[sub[i]["id"]] == "easy" for i in u) for u in units)      # some all-easy units were kept
    assert cs.easy_thinned(sub, units, bins, "T28", 20261013) == set()           # same key + seed: none thinned again
    small = sel.reselect(sub, srel, pg, rec["parts"], 250)
    got = set(small["selected_ids"])
    assert got <= chosen and 230 <= len(got) <= 250 and small["parts"][0]["key"] == "T28"
    b = Counter(bins[i] for i in got)
    assert b["easy"] <= 0.25 * len(got) + 1e-9 and b["hard"] <= 0.30 * len(got) + 1e-9
    yn = [r["gold"] for r in sub if r["id"] in got and r["qtype"] == "noul"]
    assert abs(sum(yn) / len(yn) - 0.5) <= 0.03
    for x in srel:
        assert (x["a"] in got) == (x["b"] in got)


# ---- carry-over pools (spec 3.19) -----------------------------------------------------------------------------------
def f5_rows(n=300):
    rows, rels = [], []
    for u in range(n):
        g = u % 2
        meta = {"family": "F5", "wording_id": f"w{u % 3}", "sampler": "S1"}
        base = {"call_id": f"c{u}", "group_id": f"g{u}", "source": "c_f5", "qtype": "noul", "options": None,
                "instructions": "Is it so?", "role": "base", "meta": meta}
        if u % 3 == 0:          # complement + equiv unit (3 rows)
            rows += [base | {"id": f"{u}a", "gold": g}, base | {"id": f"{u}b", "gold": 1 - g, "role": "complement"},
                     base | {"id": f"{u}c", "gold": g, "role": "equiv"}]
            rels += [{"a": f"{u}a", "b": f"{u}b", "type": "complement"}, {"a": f"{u}a", "b": f"{u}c", "type": "equiv"}]
        elif u % 3 == 1:        # inv unit
            rows += [base | {"id": f"{u}a", "gold": g}, base | {"id": f"{u}b", "gold": g, "role": "attack"}]
            rels += [{"a": f"{u}a", "b": f"{u}b", "type": "inv"}]
        else:
            rows.append(base | {"id": f"{u}a", "gold": g})
    return rows, rels


def test_f5_carry_pool_is_complement_and_equiv_units_of_the_round1_selection():
    rows, rels = f5_rows()
    r1 = {r["id"] for r in rows if int(r["id"].rstrip("abc")) < 240}
    pool, prel, info = sel.carry_pool("F5", rows, rels, r1)
    us = cs.units_of(pool, prel)
    assert pool and all(len(u) == 3 for u in us)                   # only the 3-row complement + equiv units
    assert {r["id"].rstrip("abc") for r in pool} <= {str(u) for u in range(0, 240, 3)}
    assert info["units_left_out"]["not_round1_selected"] > 0 and all(x["type"] in ("complement", "equiv") for x in prel)
    assert sel.sel_key("F5") == "F5|c2carry" and sel.sel_key("T28") == "T28"


def test_f11_carry_prefers_xed_mams_units():
    rows, rels = fam_rows("F11", n_units=900, seed=9)
    for i, r in enumerate(rows):
        r["source"] = "c_f11"
        if int(r["id"][1:].rstrip("ab")) % 2 == 0:
            r["meta"]["text_source"] = {"dataset": "xed_en" if i % 3 else "mams"}
    pg = crowd(rows, seed=2)
    allids = {r["id"] for r in rows}
    small = sel.select_carry("F11", rows, rels, pg, 200, allids)        # the preferred units alone fill it
    assert all(sel.preferred("F11", r) for r in rows if r["id"] in set(small["selected_ids"]))
    assert len(small["parts"]) == 1 and small["parts"][0]["key"] == "F11|c2carry|pref"
    big = sel.select_carry("F11", rows, rels, pg, 600, allids)          # more than they can give: the rest fills
    ids = set(big["selected_ids"])
    pref = [r for r in rows if r["id"] in ids and sel.preferred("F11", r)]
    rest = [r for r in rows if r["id"] in ids and not sel.preferred("F11", r)]
    assert pref and rest and [p["key"] for p in big["parts"]] == ["F11|c2carry|pref", "F11|c2carry|rest"]
    assert big["report"]["rows"] == len(ids) <= 600 and big["report"]["checks"]["easy_le_25"]
    assert set(big["g5"]["sample_ids"]) <= ids


def test_manifest_declared_relation_file_must_exist():
    man = {"files": {c2io.CAND: {"sha256": "a" * 64, "rows": 10}, c2io.REL: {"sha256": "b" * 64, "rows": 3}}}
    p = c2io.manifest_problems("T28", man, {c2io.CAND: ("a" * 64, 10)})
    assert p == [f"T28: MANIFEST declares {c2io.REL}, which is not on disk"]


# ---- guard review 4 (16 Oct 2026): a link with a harmless name into a refused folder is not followed ----------------------
# c2io.refusal is string logic (and round-1's list, which has no generic "ohs" rule): c2_parts/benign -> .../bench/decision_index
# passed it, so the dev-file listing, the sha and the logged inputs reached the refused folder. These tests use the REAL rule.
HIDDEN = "decision_index"             # <tmp>/bench/decision_index/: the REAL rule refuses bench/decision_index (and no name here holds ohs / jev)


def _refused_folder(tmp_path) -> Path:
    hid = tmp_path / "bench" / HIDDEN
    (hid / "out").mkdir(parents=True)
    (hid / "out" / "mixdev_S5.jsonl").write_text("{}\n")
    (hid / "out" / "candidates_c2.jsonl").write_text("{}\n")
    (hid / "drop.json").write_text(json.dumps({"drop_ids": ["x"], "complete": True, "incomplete_why": []}))
    (hid / "dev.jsonl").write_text("{}\n")
    return hid


@pytest.fixture()
def leak(monkeypatch):
    """Every open / listing of a path that really is inside the refused folder (links followed) is recorded. lstat and readlink
    are not watched (resolving a link needs them), nor is stat: pathlib's resolve() ends with one stat of the real path (its
    link-loop check), and mixio.refusal, inside c2io.refusal, has always resolved every path it is given."""
    import builtins
    import io
    import os
    seen = []

    def spy(fn):
        def watched(p, *a, **k):
            if isinstance(p, (str, bytes, os.PathLike)) and HIDDEN in os.path.realpath(os.fsdecode(p)):
                seen.append(os.fsdecode(p))
            return fn(p, *a, **k)
        return watched

    for mod, attr in ((builtins, "open"), (io, "open"), (os, "open"), (os, "scandir"), (os, "listdir")):
        monkeypatch.setattr(mod, attr, spy(getattr(mod, attr)))
    return seen


def test_a_harmless_link_name_passes_the_string_rule_and_not_the_resolved_one(tmp_path):
    import os
    hid = _refused_folder(tmp_path)
    os.symlink(hid, tmp_path / "benign")
    os.symlink(hid / "drop.json", tmp_path / "benign.json")
    os.symlink(tmp_path / "loop_b", tmp_path / "loop_a")
    os.symlink(tmp_path / "loop_a", tmp_path / "loop_b")
    (tmp_path / "plain.json").write_text("{}")
    for p in (tmp_path / "benign" / "dev.jsonl", tmp_path / "benign.json", tmp_path / "benign"):
        assert c2io.refusal(p) is None, p                       # the premise: the string rule lets a link through
        assert sel.resolved_refusal(p), p                       # ... and the resolved one does not
    assert sel.resolved_refusal(hid / "dev.jsonl") and sel.resolved_refusal(tmp_path / "loop_a")      # direct; a link loop
    assert "cannot be resolved" in sel.resolved_refusal(tmp_path / "loop_a")
    assert sel.resolved_refusal(tmp_path / "plain.json") is None and sel.resolved_refusal(tmp_path / "absent.json") is None
    assert sel.resolved_refusal(tmp_path / "absent" / "deeper" / "x.json") is None             # a missing path is not refused
    link_ok = tmp_path / "link_to_plain.json"
    link_ok.symlink_to(tmp_path / "plain.json")
    assert sel.resolved_refusal(link_ok) is None                # a link to an allowed file stays allowed
    with pytest.raises(c2io.C2Refused):
        sel.guard(c2io.C2InputLog(), tmp_path / "benign.json")
    assert sel.guard(c2io.C2InputLog(), link_ok) == link_ok
    for log in (sel.LinkGuardedInputLog(), ):
        for call in (log.check, log.record, log.json, log.jsonl):
            with pytest.raises(c2io.C2Refused):
                call(tmp_path / "benign.json")
        assert log.entries == {} and log.check(link_ok) == link_ok


def test_current_dev_files_does_not_follow_a_link_into_a_refused_folder(tmp_path, monkeypatch, leak):
    import os
    hid = _refused_folder(tmp_path)
    data, parts = tmp_path / "data", tmp_path / "data" / "c2_parts"
    ok = parts / "fam_ok" / "out" / "mixdev_S5.jsonl"
    for f in (ok, data / "c2_transfer_dev.jsonl"):
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("{}\n")
    os.symlink(hid, parts / "benign")                                       # the family folder is a link
    (parts / "fam_file" / "out").mkdir(parents=True)
    os.symlink(hid / "out" / "mixdev_S5.jsonl", parts / "fam_file" / "out" / "mixdev_S5.jsonl")     # the dev file is a link
    os.symlink(hid / "dev.jsonl", data / "c2_mixdev.jsonl")                 # so is the top-level one
    monkeypatch.setattr(c2io, "DATA", data)
    monkeypatch.setattr(c2io, "C2_PARTS", parts)
    leak.clear()
    assert REAL_CURRENT_DEV_FILES() == sorted([data / "c2_transfer_dev.jsonl", ok])
    assert leak == [], leak
    os.rename(parts, tmp_path / "real_parts")                               # the c2_parts folder itself a link
    os.symlink(hid, parts)
    leak.clear()
    assert REAL_CURRENT_DEV_FILES() == [data / "c2_transfer_dev.jsonl"] and leak == [], leak


def test_sha_if_file_and_the_stale_check_refuse_a_link_into_a_refused_folder(g13w, leak):
    import os
    hid = _refused_folder(tmp_path := g13w.tmp)
    ilog = c2io.C2InputLog()
    link = tmp_path / "benign.jsonl"
    os.symlink(hid / "dev.jsonl", link)
    leak.clear()
    with pytest.raises(c2io.C2Refused):
        sel._sha_if_file(ilog, link, {})
    assert ilog.entries == {} and leak == [], (ilog.entries, leak)           # not hashed, not logged, not opened
    # the stale check: a dev file that is such a link is "refused", and the hashes of the others are still judged
    f = g13_log(g13w, "c2_cand_T28.json")
    p = sel.g13_log_problems(ilog, [str(f)], dev_now=lambda: [link])
    assert len(p) == 1 and "dev file refused" in p[0] and leak == [], (p, leak)
    # the training file: c2_parts/T28 became a link into the refused folder after the run
    cand = c2io.fam_files("T28")["cand"]
    shutil_target = hid / "out" / "candidates_c2.jsonl"
    shutil_target.write_text(cand.read_text())
    import shutil
    shutil.rmtree(cand.parent.parent)
    os.symlink(hid, cand.parent.parent)
    leak.clear()
    p = sel.g13_log_problems(c2io.C2InputLog(), [str(f)])
    assert len(p) == 1 and "training file refused" in p[0] and leak == [], (p, leak)
    with pytest.raises(SystemExit, match="training file refused"):
        sel.drop_ids_of(c2io.C2InputLog(), [f])


def test_a_drop_list_that_is_a_link_into_a_refused_folder_is_refused_before_it_is_opened(g13w, leak):
    import os
    hid = _refused_folder(g13w.tmp)
    link = g13w.tmp / "benign_drop.json"
    os.symlink(hid / "drop.json", link)                                       # complete true, a drop id list: it WOULD load
    ok = g13w.tmp / "ok_drop.json"
    ok.write_text(json.dumps({"complete": True, "drop_ids": ["z"], "incomplete_why": []}))
    assert sel.drop_ids_of(c2io.C2InputLog(), [ok]) == {"z"}                  # control
    leak.clear()
    for call in (lambda: sel.g13_log_problems(c2io.C2InputLog(), [str(link)]),
                 lambda: sel.g13_log_problems(c2io.C2InputLog(), [], exempt=(str(link),)),
                 lambda: sel.plain_list_problems(c2io.C2InputLog(), [str(link)]),
                 lambda: sel.drop_ids_of(c2io.C2InputLog(), [ok, link]),
                 lambda: sel.drop_ids_of(sel.LinkGuardedInputLog(), [link])):
        with pytest.raises(c2io.C2Refused):
            call()
    assert leak == [], leak


def test_select_and_carry_read_their_inputs_through_the_link_guarded_log(g13w, monkeypatch):
    """cmd_select / cmd_carry / cmd_tasks build their input log with LinkGuardedInputLog, so a candidates file, a label file
    or a drop list reached through a link into a refused folder is refused, whatever function reads it."""
    import os
    hid = _refused_folder(g13w.tmp)
    link = g13w.tmp / "benign_drop.json"
    os.symlink(hid / "drop.json", link)
    monkeypatch.setattr(c2io, "require_a38", lambda prereg_text=None: None)
    monkeypatch.setattr(sel, "available", lambda fams=None: pytest.fail("a family was read"))
    made = []
    real = sel.LinkGuardedInputLog

    def spy_cls():
        made.append(real())
        return made[-1]

    monkeypatch.setattr(sel, "LinkGuardedInputLog", spy_cls)
    ns = types.SimpleNamespace(fam=None, exclude_ids=[str(link)], write_shards=False)
    for cmd in (sel.cmd_select, sel.cmd_carry):
        with pytest.raises(c2io.C2Refused):
            cmd(ns)
    assert len(made) == 2 and all(isinstance(x, c2io.C2InputLog) for x in made)
    monkeypatch.setattr(sel, "available", lambda fams=None: [])
    monkeypatch.setattr(c2io, "write_json", lambda *a, **k: "0" * 64)
    sel.cmd_tasks(ns)
    assert len(made) == 3                                                      # tasks reads through it too


# ---- guard review 4: the exemption of the mixer's round-1 list is its RESOLVED PATH, never a name ------------------------
def test_an_exempt_path_is_matched_by_its_resolved_path_not_by_a_name(g13w):
    """mix_c2 passes exempt=(pool_drops_r1.json,). A stale / incomplete G13 record under that FILE NAME elsewhere (or a name
    that merely holds it) is still checked and refused; the path itself is skipped, a link to it too."""
    rec = json.loads(g13_log(g13w, "c2_cand_T28.json", complete=False, incomplete_why=["x"]).read_text())
    real = g13w.tmp / "real" / "pool_drops_r1.json"
    real.parent.mkdir()
    (g13w.tmp / "other").mkdir()
    same_name = g13w.tmp / "other" / "pool_drops_r1.json"
    holds = [g13w.tmp / "my_pool_drops_r1.json", g13w.tmp / "pool_drops_r1_copy.json", g13w.tmp / "pool_drops_r2.json",
             g13w.tmp / "other" / "pool_drops_r1.json.bak"]
    link = g13w.tmp / "link_to_real.json"
    for f in (real, same_name, *holds):
        f.write_text(json.dumps(rec))
    link.symlink_to(real)
    ilog = c2io.C2InputLog()
    assert sel.g13_log_problems(ilog, [real], exempt=(real,)) == []                  # the exempt path: skipped
    assert sel.g13_log_problems(ilog, [link], exempt=(real,)) == []                  # a link to it: the same file
    assert sel.g13_log_problems(ilog, [real]) != []                                  # ... only because it is exempt
    for f in (same_name, *holds):
        p = sel.g13_log_problems(ilog, [f], exempt=(real,))
        assert any("incomplete G13 log" in x for x in p), (f.name, p)               # name or substring is no exemption
    both = sel.g13_log_problems(ilog, [real, same_name], exempt=(real,))
    assert len(both) == len(sel.g13_log_problems(ilog, [same_name]))                 # only the real path dropped out


def test_a_g13_shaped_record_at_the_round1_list_path_is_checked_by_exclude_ids(g13w):
    """--exclude-ids exempts no path, the mixer's round-1 list included: a stale / incomplete G13 record AT that real path is
    checked and refused (the file is faked through the log's reader; nothing is written under logs/)."""
    real = c2io.LEAN / "logs" / "decontam_counts" / "pool_drops_r1.json"
    rec = json.loads(g13_log(g13w, "c2_cand_T28.json", complete=False, incomplete_why=["x"]).read_text())

    class Faked(c2io.C2InputLog):
        def json(self, p):
            return rec if Path(p).resolve() == real.resolve() else super().json(p)

    with pytest.raises(SystemExit, match="incomplete G13 log"):
        sel.drop_ids_of(Faked(), [real])
    assert any("incomplete G13 log" in x for x in sel.g13_log_problems(Faked(), [real]))
    assert sel.g13_log_problems(Faked(), [real], exempt=(real,)) == []              # the mixer's call exempts it, by path
    link = g13w.tmp / "spelled_via_a_link.json"                                      # ... however the path is spelled
    link.symlink_to(real)
    assert sel.g13_log_problems(Faked(), [real], exempt=(link,)) == []
    assert sel.g13_log_problems(Faked(), [link], exempt=(real,)) == []


def test_tasks_refuses_a_shard_folder_behind_a_link_into_a_refused_folder(g13w, monkeypatch):
    import os
    hid = _refused_folder(g13w.tmp)
    shards = g13w.tmp / "shards"
    shards.mkdir()
    os.symlink(hid, shards / "T28")
    monkeypatch.setattr(sel, "SHARDS", shards)
    monkeypatch.setattr(c2io, "require_a38", lambda prereg_text=None: None)
    monkeypatch.setattr(sel, "available", lambda fams=None: ["T28"])
    monkeypatch.setattr(sel, "family_inputs", lambda ilog, fam: ([], [], {"candidates_sha256": "0" * 64, "relations_sha256": None}))
    monkeypatch.setattr(c2io, "candidate_problems", lambda fam, rows: [])
    monkeypatch.setitem(sys.modules, "shard_golden", types.SimpleNamespace(write_shards=lambda *a, **k: pytest.fail("written")))
    with pytest.raises(SystemExit, match="shard dir refused"):
        sel.cmd_tasks(types.SimpleNamespace(fam=None, write_shards=True))


def test_train_file_of_refuses_a_block_name_the_rule_refuses_before_a_path_is_built(g13w):
    for bad in ("T28ohs", "ohs4", "jevX", "T01_Jev"):
        with pytest.raises(c2io.C2Refused):
            sel.train_file_of("candidates", bad)
        with pytest.raises(c2io.C2Refused):
            sel.train_file_of("carry", bad)
    assert sel.train_file_of("final", "ohs_ignored") == c2io.C2_PARTS / "c2_train.jsonl"     # a final run has no block path
    assert sel.train_file_of("candidates", "T28") == c2io.fam_files("T28")["cand"]
