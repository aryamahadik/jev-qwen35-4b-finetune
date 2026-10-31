"""Tests for g13_c2.py refresh-dev (re-scan ONLY the C2 dev targets and merge into a block's candidates log).
Synthetic data only (the sealed checkers are fake, as in test_g13_c2.py; no ohs path is opened or listed). Method 5 runs for
real here: a deterministic bag-of-words encoder replaces the sentence-transformers model, so the embedding merge, the cache
fill and the top-5 per set are exercised. Everything is written under pytest's tmp_path. Run from lean/:
  ../.venv/bin/python -m pytest -q c2_build/tests/test_g13_c2_refresh.py

The parity claim under test: a refresh-dev log (old log + a dev change + refresh) equals, field for field, the log a FULL
candidates run on the current files writes, apart from bookkeeping (wall_s, unix, embed_stats, "refreshed").
"""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import inspect
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import pytest

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2B = HERE.parent
sys.path.insert(0, str(C2B))
sys.path.insert(0, str(HERE))
import c2io  # noqa: E402
import g13_c2 as G  # noqa: E402
from c2_kit import paths as kp  # noqa: E402
from test_g13_c2 import (A38, EVAL_SENT, SUITE_KEYWORD, TILED, FRAME, AUTHORED, exports, fake_tools, row)  # noqa: E402,F401

g = G.g
BOOKKEEPING = ("wall_s", "unix", "embed_stats", "refreshed")
BACKUP = C2B / "_backup_refresh" / "g13_c2.py"
INSTR_DEV = "Dev instruction wording for the held out rows only."
UNUSED_LIT = "Nobody may open the archive vault without two signed approvals from the board today."
EMBED_TEXT = "Quarterly inventory audit completed ahead of schedule across every regional warehouse today."
EMBED_SHUFFLED = "today warehouse regional every across schedule of ahead completed audit inventory Quarterly."


# ---------------------------------------------------------------------------------------------------- helpers
def strip_book(x):
    """A record without its bookkeeping keys (at any depth): what 'identical to a full run' compares."""
    if isinstance(x, dict):
        return {k: strip_book(v) for k, v in x.items() if k not in BOOKKEEPING}
    if isinstance(x, list):
        return [strip_book(v) for v in x]
    return x


def canon(rec) -> str:
    return json.dumps(strip_book(rec), sort_keys=True)


def first_diff(a, b, path="") -> str | None:
    if type(a) is not type(b):
        return f"{path}: type {type(a).__name__} vs {type(b).__name__}"
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                return f"{path}/{k}: only in {'refresh' if k in a else 'full run'}"
            d = first_diff(a[k], b[k], f"{path}/{k}")
            if d:
                return d
        return None
    if isinstance(a, list):
        if len(a) != len(b):
            return f"{path}: length {len(a)} vs {len(b)}"
        for i, (x, y) in enumerate(zip(a, b)):
            d = first_diff(x, y, f"{path}[{i}]")
            if d:
                return d
        return None
    return None if a == b else f"{path}: {str(a)[:80]!r} vs {str(b)[:80]!r}"


def same_log(refreshed: dict, full: dict) -> None:
    d = first_diff(strip_book(refreshed), strip_book(full))
    assert d is None, d
    assert canon(refreshed) == canon(full)


class FakeEnc:
    """Deterministic bag-of-words stand-in for the sentence-transformers Encoder (same interface)."""
    dim, dev = 24, "cpu"

    def __init__(self, cfg=None):
        pass

    def __call__(self, texts):
        out = np.zeros((len(texts), self.dim), np.float32)
        for i, t in enumerate(texts):
            for w in g.words(t):
                out[i, int(hashlib.md5(w.encode()).hexdigest(), 16) % self.dim] += 1.0
        n = np.linalg.norm(out, axis=1, keepdims=True)
        return (out / np.maximum(n, 1e-9)).astype(np.float16)


def a53_meta(fam, sk, w, c, p, reg, structure=None):
    return {"family": fam, "wording_id": w, "card_id": c, "domain_pack": p, "structure_hash": structure,
            "c2": {"skin_id": sk, "register": reg}}


def cand(i, state, assets=None, structure=None, group=None):
    sk, w, c, p = assets or (f"sk{i}", f"w{i}", f"c{i}", f"p{i}")
    r = row(i, state, meta=a53_meta("T97", sk, w, c, p, "cr", structure), instructions="Decide using the stated rule only.")
    if group:
        r["group_id"] = group
    return r


def dev_row(i, state, structure=None, group=None, instructions=INSTR_DEV, assets=("dk", "dw", "dc", "dp", "dr")):
    sk, w, c, p, reg = assets
    return {"id": f"d{i}", "state": state, "instructions": instructions, "options": None, "group_id": group,
            "meta": a53_meta("T97", sk, w, c, p, reg, structure)}


def write_rows(p: Path, rows) -> None:
    p.write_text("".join(json.dumps(r) + "\n" for r in rows))


CANDS = ([cand(i, f"{FRAME} Unique closing words number {i} here.") for i in range(8)] + [
    cand(20, f"{AUTHORED} Ending of the authored row.", ("ska", "wa", "ca", "pa")),
    cand(21, f"Opening of the tiled row. {TILED} Ending of it.", ("skt", "wt", "ct", "pt")),
    cand(22, "Clean text that shares no sentence with any dev row at all, honestly.", ("skc", "wc", "cc", "pc")),
    cand(30, "Ship today with " + SUITE_KEYWORD + " please, the client asked twice.", ("s30", "w30", "c30", "p30")),
    cand(31, "A row carrying SEALEDLEAK text in its state for the fake checker.", ("s31", "w31", "c31", "p31")),
    cand(32, "Rendered: " + EVAL_SENT, ("s32", "w32", "c32", "p32")),
    cand(33, EMBED_TEXT, ("s33", "w33", "c33", "p33")),
    cand(34, "Plain state thirty four about harbour pilots and tide tables.", ("s34", "w34", "c34", "p34"),
         structure="aa", group="g34"),
])

DEV_A = {
    "mixdev_a.jsonl": [dev_row(1, f"{FRAME} Different closing words for the dev row."),
                       dev_row(2, f"{AUTHORED} Dev ending."),
                       dev_row(3, f"Dev opening. {TILED} Dev ending.")],
    "c2_transfer_dev.jsonl": [dev_row(10, UNUSED_LIT, instructions="Transfer wording that only the held out family uses.")],
}
DEV_B = {
    "mixdev_a.jsonl": [dev_row(1, f"{FRAME} Different closing words for the dev row.")],        # two rows gone
    "mixdev_b.jsonl": [dev_row(4, EMBED_SHUFFLED),                                              # method 5 (same bag of words)
                       dev_row(5, "A fresh structure twin of another block.", structure="aa"),   # method 6 structure
                       dev_row(6, "Another fresh state with a group id of a training row.", group="g34")],   # group_id
    "c2_transfer_dev.jsonl": [dev_row(10, TILED, instructions="Transfer wording that only the held out family uses."),
                              dev_row(11, "Clean text that shares no sentence with any dev row at all, honestly.",
                                      instructions="Second transfer wording of the held out family.")],
}


def set_dev(dev: Path, files: dict) -> None:
    """Make the dev folder hold exactly `files` ({name: rows}); a name not in it is removed."""
    for p in dev.glob("*.jsonl"):
        if p.name not in files:
            p.unlink()
    for name, rows in files.items():
        write_rows(dev / name, rows)


@pytest.fixture()
def rw(tmp_path, monkeypatch, fake_tools, exports):
    """One block (T97) with A53-relevant candidates and program literals, a dev folder (mixdev_*.jsonl glob + the transfer
    dev), a synthetic old eval target, fake sealed checkers, and method 5 on with FakeEnc."""
    ev = tmp_path / "eval"
    ev.mkdir()
    write_rows(ev / "synthetic_1.jsonl", [{"id": "e1", "state": EVAL_SENT, "options": ["yes", "no"]}])
    blocks = tmp_path / "blocks"
    (blocks / "T97").mkdir(parents=True)
    plugin = blocks / "T97" / "plugin.py"
    plugin.write_text(f'TILED = "{TILED}"\nRENDERED = "{EVAL_SENT}"\nUNUSED = "{UNUSED_LIT}"\n'
                      'TPL = "SEALEDTPL program sentence with several more words in it."\n')
    parts = tmp_path / "c2_parts"
    candf = parts / "T97" / "out" / "candidates_c2.jsonl"
    candf.parent.mkdir(parents=True)
    write_rows(candf, CANDS)
    dev = tmp_path / "devsets"
    dev.mkdir()
    set_dev(dev, DEV_A)
    c2dev = {n: dict(d) for n, d in G.C2_DEV.items()}
    c2dev["c2_mixdev"]["paths"] = [f"abs:{dev}/mixdev_*.jsonl"]
    c2dev["c2_transfer_dev"]["paths"] = [f"abs:{dev}/c2_transfer_dev.jsonl"]
    monkeypatch.setattr(G, "C2_DEV", c2dev)
    monkeypatch.setattr(G, "block_dir", lambda b: blocks / b)
    monkeypatch.setattr(c2io, "C2_PARTS", parts)
    code = tmp_path / "code"
    code.mkdir()
    for n in ("g13_c2.py", "decontam_g13.py"):                 # stand-ins: the guard hashes these, not the real files
        (code / n).write_text(f"# stand-in {n}, version 1\n")
    monkeypatch.setattr(G, "CODE_GUARD", {n: code / n for n in ("g13_c2.py", "decontam_g13.py")})
    monkeypatch.setattr(G, "_CODE_AT_IMPORT", {n: g.sha256_file(code / n) for n in ("g13_c2.py", "decontam_g13.py")})
    monkeypatch.setattr(G, "a53_family_files", lambda: [])
    writes = {}

    def fake_write_json(p, obj, prereg_text=None):               # the guarded writer, without its lean/ rule: a real file
        writes[str(p)] = obj
        Path(p).parent.mkdir(parents=True, exist_ok=True)
        Path(p).write_text(json.dumps(obj, indent=1) + "\n")

    monkeypatch.setattr(kp, "write_json", fake_write_json)
    # method 5 on: a fixed threshold, the fake encoder, a private vector cache
    cos = tmp_path / "cosine.json"
    cos.write_text(json.dumps({"threshold": 0.9, "model": "fake-bow", "max_seq_length": 64, "dtype": "float32"}))
    monkeypatch.setattr(g, "COSINE", cos)
    monkeypatch.setattr(g, "EMB_DIR", tmp_path / "emb")
    monkeypatch.setattr(g, "Encoder", FakeEnc)
    monkeypatch.setattr(g, "_SIDE_DIGEST", {})
    monkeypatch.setattr(G, "OUT", tmp_path / "logs")
    tgs = [g.target("synthetic_eval", [f"abs:{ev}/synthetic_*.jsonl"])]
    w = {"tgs": tgs, "exports": exports, "writes": writes, "dev": dev, "cand": candf, "plugin": plugin, "eval": ev,
         "code": code, "cos": cos, "logs": tmp_path / "logs", "tmp": tmp_path}
    monkeypatch.setattr(G, "engine_targets", lambda run_name: tgs + G.c2_dev_targets() if run_name == "candidates"
                        else G.c2_dev_targets())
    return w


def full_run(w, **kw) -> dict:
    return G.run("candidates", ["T97"], embed=True, side=False, tgs=w["tgs"] + G.c2_dev_targets(), exports=w["exports"],
                 write=False, prereg_text=A38, **kw)["c2_cand_T97"]


def save_log(w, rec: dict, mutate=None) -> Path:
    """Write `rec` as the block's candidates log into the (private) log folder; returns the folder."""
    d = json.loads(json.dumps(rec))
    if mutate:
        mutate(d)
    w["logs"].mkdir(exist_ok=True)
    (w["logs"] / f"{d['set']}.json").write_text(json.dumps(d, indent=1))
    return w["logs"]


def refresh(w, **kw) -> dict:
    return G.refresh_dev(["T97"], tgs=w["tgs"] + G.c2_dev_targets(), exports=w["exports"], write=False, prereg_text=A38,
                         log_dir=w["logs"], **kw)["c2_cand_T97"]


def refusal(w, **kw) -> dict:
    with pytest.raises(G.RefreshRefused) as e:
        refresh(w, **kw)
    return e.value.problems


def no_scan(monkeypatch):
    """Fail the test when the engine scans anything (a refusal must come before the scan)."""
    def boom(*a, **k):
        raise AssertionError("the engine was started although refresh-dev should have refused")
    monkeypatch.setattr(g, "run_sets", boom)


# ---------------------------------------------------------------------------------------------------- the parity proof
def test_the_fixture_run_is_complete_and_the_dev_change_matters(rw):
    a = full_run(rw)
    assert a["complete"] and not a["incomplete_why"], a["incomplete_why"]
    set_dev(rw["dev"], DEV_B)
    b = full_run(rw)
    assert b["complete"], b["incomplete_why"]
    assert a["drop_ids"] != b["drop_ids"] and a["counts_by_target_and_method"] != b["counts_by_target_and_method"]
    assert a["inputs_at_start"] != b["inputs_at_start"]                 # a dev file appeared, one changed
    cb = b["counts_by_target_and_method"]
    assert "embed" in cb["c2_mixdev"] and "structure" in cb[G.C2_STRUCT] and "group_id" in cb[G.C2_STRUCT]
    assert cb["c2_transfer_dev"]                                         # the clean row and the TILED literal
    assert any(x.endswith("plugin.py#0") for x in b["code_seed_hits"])   # B: the TILED literal (rendered in r21) is hit by
    assert not any(x.endswith("plugin.py#0") for x in a["code_seed_hits"])          # the transfer dev and binds; not in A
    assert a["report_only"]["engine_seed_hits_report_only"].get("c2_transfer_dev")  # A: the unused literal, report only
    assert "c2_transfer_dev" not in b["report_only"]["engine_seed_hits_report_only"]
    assert a["a53"]["waived_units"]["c2_mixdev"] == 9 and b["a53"]["waived_units"]["c2_mixdev"] == 8   # A53 differs too


def test_refresh_after_a_dev_change_equals_a_full_run(rw):
    a = full_run(rw)
    save_log(rw, a)
    set_dev(rw["dev"], DEV_B)                                            # the mixdev change: a file gone rows, a new file
    full_b = full_run(rw)
    ref = refresh(rw)
    same_log(ref, full_b)
    assert full_b["engine"]["inputs_sha256"]["eval"] == ref["engine"]["inputs_sha256"]["eval"]
    assert ref["a53"] == full_b["a53"] and ref["inputs_at_start"] == full_b["inputs_at_start"]
    assert ref["complete"] and "refreshed" in ref and "refreshed" not in full_b


def test_refresh_with_no_change_returns_the_same_log(rw):
    a = full_run(rw)
    save_log(rw, a)
    same_log(refresh(rw), a)                                             # the merge loses and adds nothing


def test_refresh_of_a_refreshed_log_is_still_a_full_runs_log(rw):
    a = full_run(rw)
    save_log(rw, a)
    set_dev(rw["dev"], DEV_B)
    r1 = refresh(rw)
    save_log(rw, r1)
    set_dev(rw["dev"], DEV_A)                                            # and back
    r2 = refresh(rw)
    same_log(r2, a)
    assert [x["from_log_sha256"] for x in r2["refreshed"]] and len(r2["refreshed"]) == 2


def test_refresh_changes_only_dev_things_in_the_record(rw):
    a = full_run(rw)
    save_log(rw, a)
    set_dev(rw["dev"], DEV_B)
    ref = refresh(rw)
    old_hits, new_hits = a["engine"]["hits_by_eval"], ref["engine"]["hits_by_eval"]
    for lb in set(old_hits) | set(new_hits):
        if lb not in G.C2_DEV:
            assert old_hits.get(lb) == new_hits.get(lb), lb              # the other targets' hits are kept as they were
    assert old_hits.get("c2_mixdev") != new_hits.get("c2_mixdev")
    for key in ("methods", "rules", "train_units", "train_rows", "seed_literals", "tool_sha256", "spec"):
        assert a["engine"][key] == ref["engine"][key]
    assert a["engine"]["targets"]["synthetic_eval"] == ref["engine"]["targets"]["synthetic_eval"]


def test_the_refreshed_log_is_current_for_status_and_the_mixers_stale_check(rw, monkeypatch, tmp_path):
    import c2_select as sel
    a = full_run(rw)
    log = save_log(rw, a) / "c2_cand_T97.json"
    dev = rw["dev"]
    monkeypatch.setattr(sel, "current_dev_files", lambda: sorted(dev.glob("*.jsonl")))
    set_dev(dev, DEV_B)

    def stale():
        return [x for x in sel.g13_log_problems(c2io.C2InputLog(), [str(log)]) if "stale" in x]

    def status():
        return [x for x in G.log_problems([log]) if "changed after" in x]

    assert stale() and status()                                          # the dev change makes the old log stale
    ref = refresh(rw)
    log.write_text(json.dumps(ref))
    assert stale() == [] and status() == []                              # the refreshed one ties to the files now
    (dev / "mixdev_b.jsonl").write_text((dev / "mixdev_b.jsonl").read_text() + json.dumps(dev_row(9, "later")) + "\n")
    assert stale() and status()                                          # and goes stale again on the next change


def test_a_refresh_notes_where_it_came_from(rw):
    a = full_run(rw)
    log = save_log(rw, a) / "c2_cand_T97.json"
    set_dev(rw["dev"], DEV_B)
    ref = refresh(rw)
    (r,) = ref["refreshed"]
    assert r["from_log_sha256"] == hashlib.sha256(log.read_bytes()).hexdigest()
    assert r["targets"] == sorted(G.C2_DEV) and r["dev_files_before"] == 2 and r["dev_files_now"] == 3
    assert r["to_tool_sha256"] == ref["tool_sha256"] == g.sha256_file(Path(G.__file__))
    json.dumps(ref)                                                      # counts, hashes and C2 ids only


def test_refresh_writes_the_log_through_the_guarded_writer(rw):
    """The guarded writer writes a temp file beside the log and the log is replaced in one step; the old log is kept."""
    old = save_log(rw, full_run(rw)) / "c2_cand_T97.json"
    old_bytes = old.read_bytes()
    set_dev(rw["dev"], DEV_B)
    G.refresh_dev(["T97"], tgs=rw["tgs"] + G.c2_dev_targets(), exports=rw["exports"], prereg_text=A38, log_dir=rw["logs"])
    tmp, final = G.OUT / ".c2_cand_T97.json.tmp", G.OUT / "c2_cand_T97.json"
    assert list(rw["writes"]) == [str(tmp)] and rw["writes"][str(tmp)]["complete"] is True
    assert not tmp.exists() and json.loads(final.read_text())["complete"] is True and final.read_bytes() != old_bytes
    kept = G.OUT.parent / "logs_refresh_backup" / f"c2_cand_T97.{hashlib.sha256(old_bytes).hexdigest()[:12]}.json"
    assert kept.read_bytes() == old_bytes                                 # the basis of the refresh is still there


# ---------------------------------------------------------------------------------------------------- incomplete old logs
def test_refresh_repairs_a_log_written_before_a_dev_set_existed(rw):
    (rw["dev"] / "c2_transfer_dev.jsonl").unlink()
    a = full_run(rw)
    assert not a["complete"] and any("not built yet" in w for w in a["incomplete_why"])
    save_log(rw, a)
    set_dev(rw["dev"], DEV_B)
    ref = refresh(rw)
    assert ref["complete"] and not ref["incomplete_why"]
    same_log(ref, full_run(rw))


def test_refresh_repairs_a_log_whose_run_saw_a_dev_file_change(rw, monkeypatch):
    orig = G.A53State

    def late(*a, **k):                                                   # the dev file is rewritten after the engine read it
        write_rows(rw["dev"] / "mixdev_a.jsonl", DEV_B["mixdev_a.jsonl"])
        return orig(*a, **k)

    monkeypatch.setattr(G, "A53State", late)
    a = full_run(rw)
    monkeypatch.setattr(G, "A53State", orig)
    assert not a["complete"] and any(G.CHANGED in w and "mixdev_a.jsonl" in w for w in a["incomplete_why"])
    save_log(rw, a)
    ref = refresh(rw)
    assert ref["complete"], ref["incomplete_why"]
    same_log(ref, full_run(rw))


def test_refresh_does_not_repair_an_incomplete_log_whose_reason_is_not_a_dev_one(rw):
    a = full_run(rw)
    for why, pairs in (("synthetic_eval: no input file found (abs:x)", [[["synthetic_eval"], "synthetic_eval: no input file found (abs:x)"]]),
                       ("some run-level reason", [[["_run"], "some run-level reason"]]),
                       ("method 5 (embed) off in this run (--no-embed)", None),
                       ("ohs4_hash: refused", None),
                       (f"plugin.py {G.CHANGED} (gone)", None)):
        def mutate(d, why=why, pairs=pairs):
            d["complete"], d["incomplete_why"] = False, [why]
            if pairs is not None:
                d["engine"]["why_by_target"], d["engine"]["incomplete_why"] = pairs, [why]
        save_log(rw, a, mutate)
        probs = refusal(rw)
        assert any("incomplete" in x for x in probs["c2_cand_T97"]), (why, probs)
    save_log(rw, a, lambda d: d.update(complete=False))                  # flag and reasons disagree
    assert any("disagree" in x for x in refusal(rw)["c2_cand_T97"])


# ---------------------------------------------------------------------------------------------------- refusals
def _old(rw):
    a = full_run(rw)
    save_log(rw, a)
    return a


def test_refuses_when_the_candidates_changed(rw, monkeypatch):
    _old(rw)
    write_rows(rw["cand"], CANDS + [cand(40, "A late extra row with enough words to be a row of the block.")])
    no_scan(monkeypatch)
    probs = refusal(rw)
    assert any("candidates_c2.jsonl" in x and "changed" in x for x in probs["c2_cand_T97"]), probs
    assert rw["writes"] == {}


def test_refuses_when_a_program_literal_file_changed_or_appeared(rw, monkeypatch):
    _old(rw)
    no_scan(monkeypatch)
    rw["plugin"].write_text(rw["plugin"].read_text() + 'MORE = "a new program literal with several words"\n')
    assert any("plugin.py" in x and "changed" in x for x in refusal(rw)["c2_cand_T97"])
    rw["plugin"].write_text(rw["plugin"].read_text().rsplit("MORE", 1)[0])           # back as it was
    assert not G.refresh_check(["T97"], tgs=rw["tgs"] + G.c2_dev_targets(), log_dir=rw["logs"])
    (rw["plugin"].parent / "vocab.py").write_text('V = "a vocabulary literal with several words in it"\n')
    assert any("vocab.py" in x and "appeared" in x for x in refusal(rw)["c2_cand_T97"])


def test_refuses_when_another_targets_eval_file_changed_gone_or_new(rw, monkeypatch):
    _old(rw)
    no_scan(monkeypatch)
    f = rw["eval"] / "synthetic_1.jsonl"
    text = f.read_text()
    write_rows(f, [{"id": "e1", "state": EVAL_SENT + " plus", "options": ["yes", "no"]}])
    assert any("changed or gone" in x for x in refusal(rw)["c2_cand_T97"])
    f.write_text(text)
    assert not G.refresh_check(["T97"], tgs=rw["tgs"] + G.c2_dev_targets(), log_dir=rw["logs"])
    write_rows(rw["eval"] / "synthetic_2.jsonl", [{"id": "e2", "state": "A new eval file in the old target."}])
    assert any("not in the log" in x for x in refusal(rw)["c2_cand_T97"])


def test_a_change_of_the_dev_files_alone_is_not_a_refusal(rw, monkeypatch):
    _old(rw)
    set_dev(rw["dev"], DEV_B)
    assert G.refresh_check(["T97"], tgs=rw["tgs"] + G.c2_dev_targets(), log_dir=rw["logs"]) == {}
    (rw["dev"] / "mixdev_a.jsonl").unlink()                              # a dev file gone, another added: still dev only
    write_rows(rw["dev"] / "mixdev_c.jsonl", [dev_row(7, "A third mixdev file with its own state words.")])
    assert G.refresh_check(["T97"], tgs=rw["tgs"] + G.c2_dev_targets(), log_dir=rw["logs"]) == {}


@pytest.mark.parametrize("what", ["engine_sha", "tool_sha", "g13_ias", "decontam_ias", "no_inputs_at_start", "other_run",
                                  "other_set", "methods", "train_sha", "seed_sha", "cosine_sha", "no_eval_hashes",
                                  "extra_file", "no_why_by_target"])
def test_refuses_a_log_that_is_not_a_valid_basis(rw, monkeypatch, what):
    a = full_run(rw)

    def mutate(d):
        e = d["engine"]
        if what == "engine_sha":
            d["engine_sha256"] = "1" * 64
        elif what == "tool_sha":
            d["tool_sha256"] = "2" * 64
        elif what == "g13_ias":
            d["inputs_at_start"]["g13_c2.py"] = "3" * 64
        elif what == "decontam_ias":
            d["inputs_at_start"]["decontam_g13.py"] = "4" * 64
        elif what == "no_inputs_at_start":
            d.pop("inputs_at_start")
            d.pop("inputs_at_start_paths")
        elif what == "other_run":
            d["run"] = "carry"
        elif what == "other_set":
            d["set"] = "c2_cand_T01"
        elif what == "methods":
            e["methods"] = {**e["methods"], "embed": "not_run"}
        elif what == "train_sha":
            e["inputs_sha256"]["train"] = {k: "5" * 64 for k in e["inputs_sha256"]["train"]}
        elif what == "seed_sha":
            e["inputs_sha256"]["seeds"] = {k: "6" * 64 for k in e["inputs_sha256"]["seeds"]}
        elif what == "cosine_sha":
            e["inputs_sha256"]["cosine"] = "7" * 64
        elif what == "no_eval_hashes":
            e["inputs_sha256"]["eval"] = {}
        elif what == "extra_file":                                       # an input of the log that is gone now
            d["inputs_at_start"]["gone.py"] = "8" * 64
            d["inputs_at_start_paths"]["gone.py"] = "c2_build/families/T97/gone.py"
        elif what == "no_why_by_target":
            e.pop("why_by_target")
            d["complete"], d["incomplete_why"] = False, ["x"]
    save_log(rw, a, mutate)
    no_scan(monkeypatch)
    probs = refusal(rw)
    assert probs.get("c2_cand_T97") or probs.get("*"), probs
    assert rw["writes"] == {}


def test_refuses_when_there_is_no_log_or_no_candidates(rw, monkeypatch):
    with pytest.raises(G.RefreshRefused) as e:
        refresh(rw)
    assert "no readable candidates log" in e.value.problems["c2_cand_T97"][0]
    _old(rw)
    no_scan(monkeypatch)
    rw["cand"].unlink()
    with pytest.raises(G.RefreshRefused) as e:
        refresh(rw)
    assert "nothing to refresh" in e.value.problems["c2_cand_T97"][0]


def test_refuses_without_method_5_and_for_other_runs(rw, monkeypatch):
    _old(rw)
    no_scan(monkeypatch)
    with pytest.raises(G.RefreshRefused) as e:
        refresh(rw, embed=False)
    assert any("method 5" in x for x in e.value.problems["*"])
    with pytest.raises(G.RefreshRefused) as e:                           # carry / final runs scan the dev targets only already
        G.refresh_engine("final", {}, {}, None, G.c2_dev_targets(), {})
    assert "scan only the C2 dev targets already" in e.value.problems["*"][0]


def test_refuses_when_the_cosine_settings_changed(rw, monkeypatch):
    _old(rw)
    no_scan(monkeypatch)
    rw["cos"].write_text(json.dumps({"threshold": 0.95, "model": "fake-bow", "max_seq_length": 64, "dtype": "float32"}))
    assert any("a full run" in x for x in refusal(rw)["c2_cand_T97"])


def test_a_sealed_side_digest_is_checked_like_the_engines_stale_check(rw, monkeypatch):
    a = full_run(rw)
    save_log(rw, a, lambda d: d["engine"]["inputs_sha256"].update(sealed_side={"sidea": "d1", "sideb": "d2", "gone": None}))
    calls = []

    def fake_side(units, owner, names, cosine, mode="scan", py=None):
        calls.append((list(names), mode))
        return {n: {"digest": {"sidea": "d1", "sideb": "d2"}[n]} for n in names}

    monkeypatch.setattr(g, "sealed_side_run", fake_side)
    assert G.refresh_check(["T97"], tgs=rw["tgs"] + G.c2_dev_targets(), log_dir=rw["logs"]) == {}
    assert calls == [(["sidea", "sideb"], "digest")]                     # a digest only, never a scan; a failed child skipped
    monkeypatch.setattr(g, "_SIDE_DIGEST", {})
    monkeypatch.setattr(g, "sealed_side_run", lambda *a, **k: {"sidea": {"digest": "d1"}, "sideb": {"digest": "CHANGED"}})
    assert any("sealed-side input digest changed" in x for x in refusal(rw)["c2_cand_T97"])


def test_a_refused_refresh_writes_nothing_and_names_no_sealed_path(rw, monkeypatch):
    a = full_run(rw)
    key = "opendecide-data/lean/ohs/cache/x.abst"                       # a key naming a never-open folder: never echoed
    save_log(rw, a, lambda d: d["engine"]["inputs_sha256"]["eval"].update({key: "9" * 64}))
    real = g.eval_path
    monkeypatch.setattr(g, "eval_path", lambda k: None if "ohs" in k else real(k))   # (no stat of any such path here)
    no_scan(monkeypatch)
    msg = "\n".join(refusal(rw)["c2_cand_T97"])
    assert "ohs" not in msg and "<withheld " in msg
    assert rw["writes"] == {}


# ---------------------------------------------------------------------------------------------------- the guard, during a refresh
def test_a_dev_change_during_a_refresh_is_caught_like_in_a_full_run(rw, monkeypatch):
    a = full_run(rw)
    save_log(rw, a)
    set_dev(rw["dev"], DEV_B)
    orig = G.A53State

    def hook(w):
        def late(*aa, **kk):                                             # a lane rewrites a dev file after the engine read it
            write_rows(w["dev"] / "mixdev_b.jsonl", DEV_B["mixdev_b.jsonl"][:2])
            return orig(*aa, **kk)
        return late

    monkeypatch.setattr(G, "A53State", hook(rw))
    ref = refresh(rw)
    set_dev(rw["dev"], DEV_B)
    monkeypatch.setattr(G, "A53State", hook(rw))
    full = full_run(rw)
    assert ref["complete"] is False and any(G.CHANGED in w and "mixdev_b.jsonl" in w for w in ref["incomplete_why"])
    assert "waived_units" not in ref["a53"] and ref["a53"]["note"].startswith("not applied")     # no waiver from changed files
    same_log(ref, full)


def test_a_change_after_the_a53_step_withdraws_the_waivers_in_a_refresh_too(rw, monkeypatch):
    a = full_run(rw)
    save_log(rw, a)
    monkeypatch.setattr(G, "a53_apply", (lambda orig: lambda *aa, **kk: (
        write_rows(rw["dev"] / "mixdev_a.jsonl", DEV_B["mixdev_a.jsonl"]), orig(*aa, **kk))[1])(G.a53_apply))
    ref = refresh(rw)
    assert not ref["complete"] and ref["a53"]["note"].startswith("withdrawn")
    assert any(G.CHANGED in w for w in ref["incomplete_why"])


def test_the_code_guard_watches_a_refresh_as_well(rw, monkeypatch):
    a = full_run(rw)
    save_log(rw, a)
    orig = G.A53State

    def late(*aa, **kk):
        (rw["code"] / "g13_c2.py").write_text("# stand-in g13_c2.py, version 2\n")
        return orig(*aa, **kk)

    monkeypatch.setattr(G, "A53State", late)
    ref = refresh(rw)
    assert not ref["complete"] and any("g13_c2.py" in w and G.CHANGED in w for w in ref["incomplete_why"])


# ---------------------------------------------------------------------------------------------------- the CLI
def test_cli_check_refresh_and_refusal(rw, monkeypatch, capsys):
    a = full_run(rw)
    save_log(rw, a)
    set_dev(rw["dev"], DEV_B)
    monkeypatch.setattr(G, "refresh_dev", lambda blocks, **kw: G.run(
        "candidates", blocks, tgs=rw["tgs"] + G.c2_dev_targets(), exports=rw["exports"], write=False, prereg_text=A38,
        refresh_from=G.read_refresh_logs(blocks), side=False, side_parallel=False))
    with_scan = g.run_sets
    no_scan(monkeypatch)                                                 # --check scans nothing
    assert G.main(["refresh-dev", "--check", "--block", "T97"]) == 0
    assert "may be refreshed" in capsys.readouterr().out
    monkeypatch.setattr(g, "run_sets", with_scan)
    assert G.main(["refresh-dev", "--block", "T97"]) == 0
    out = capsys.readouterr().out
    assert "G13-C2 c2_cand_T97 (refresh-dev)" in out and "complete True" in out
    rw["plugin"].write_text(rw["plugin"].read_text() + 'MORE = "a new program literal with several words"\n')
    assert G.main(["refresh-dev", "--check", "--block", "T97"]) == 1
    out = capsys.readouterr().out
    assert "refresh-dev refused [c2_cand_T97]" in out and "nothing was scanned or written" in out
    assert G.main(["refresh-dev", "--no-embed"]) == 2


def test_default_blocks_are_the_candidates_blocks_that_have_a_file(rw, monkeypatch):
    monkeypatch.setattr(G, "default_blocks", lambda run_name: ["T97", "T96"])
    assert G.default_refresh_blocks() == ["T97"]                         # T96 has no candidates file


def test_logs_on_a_never_open_path_are_not_read(rw, monkeypatch):
    save_log(rw, full_run(rw))
    monkeypatch.setattr(G, "resolved_refusal", lambda p: "refused" if str(p).endswith("c2_cand_T97.json") else None)
    assert G.read_refresh_logs(["T97"], rw["logs"]) == {}
    with pytest.raises(G.RefreshRefused):
        refresh(rw)


# ---------------------------------------------------------------------------------------------------- dev path rules
def test_dev_path_rules_on_the_real_layout():
    lean = c2io.LEAN
    assert G.is_dev_path(lean / "data/c2_parts/T31/out/mixdev_S5.jsonl") and G.is_dev_path(lean / "data/c2_mixdev.jsonl")
    assert G.is_dev_path(lean / "data/c2_transfer_dev.jsonl")
    assert not G.is_dev_path(lean / "data/c2_parts/T31/out/candidates_c2.jsonl")
    assert not G.is_dev_path(lean / "c_src/F5/out/mixdev_S5.jsonl") and not G.is_dev_path(lean / "data/c2_parts/mixdev_S5.jsonl")
    assert not G.is_dev_path(lean / "data/c2_parts/T31/out/x/mixdev_S5.jsonl")
    assert G.is_dev_key("opendecide-data/lean/data/c2_parts/GB/out/mixdev_S5.jsonl")
    assert G.is_dev_key("opendecide-data/lean/data/c2_transfer_dev.jsonl")
    assert not G.is_dev_key("opendecide-data/lean/data/dev_nc.jsonl") and not G.is_dev_key("hfstream:x/y|z")
    assert not G.is_dev_key("datasets--a--b/snapshots/x/data/train-00000.parquet")
    assert G._safe("opendecide-data/lean/ohs/cache/a.xml").startswith("<withheld ") and G._safe("data/dev_nc.jsonl") == "data/dev_nc.jsonl"


def test_the_dev_patterns_follow_c2_dev(monkeypatch):
    pats = G.dev_patterns()
    assert all(isinstance(p, tuple) and p[0] == "/" for p in pats)
    spec = {n: dict(d) for n, d in G.C2_DEV.items()}
    spec["c2_mixdev"]["paths"] = ["lean:data/x/*/y.jsonl"]
    monkeypatch.setattr(G, "C2_DEV", spec)
    assert G.is_dev_path(c2io.LEAN / "data/x/B/y.jsonl") and not G.is_dev_path(c2io.LEAN / "data/c2_mixdev.jsonl")
    spec["c2_mixdev"]["paths"] = ["lean:data/x/**/y.jsonl", "http:nope"]
    monkeypatch.setattr(G, "C2_DEV", spec)
    with pytest.raises(ValueError):
        G.dev_patterns()


# ---------------------------------------------------------------------------------------------------- the predecessor
def _load_backup():
    spec = importlib.util.spec_from_file_location("g13_c2_predecessor", BACKUP)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_the_listed_predecessor_is_the_file_kept_in_the_backup_folder():
    sha = hashlib.sha256(BACKUP.read_bytes()).hexdigest()
    assert sha in G.REFRESH_COMPATIBLE_TOOL_SHAS
    assert sha != g.sha256_file(Path(G.__file__))                        # this file is the new one
    assert set(G.REFRESH_COMPATIBLE_TOOL_SHAS) == {sha}


def _top_level(path: Path) -> dict:
    out = {}
    for node in ast.parse(path.read_text()).body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            out[node.name] = ast.dump(node)
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    out[t.id] = ast.dump(node)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            out[node.target.id] = ast.dump(node)
    return out


def test_this_code_changed_the_predecessor_only_where_refresh_dev_needs_it():
    """The claim behind REFRESH_COMPATIBLE_TOOL_SHAS: the full-run code path of the predecessor is this file's. Every top-level
    function, class and constant of the predecessor is unchanged here except `run` (one new keyword and its refresh branches) and
    `main` (the new command); everything else in this file is new."""
    old, new = _top_level(BACKUP), _top_level(Path(G.__file__))
    changed = sorted(k for k in old if old[k] != new.get(k))
    assert changed == ["main", "run"], changed
    added = sorted(set(new) - set(old))
    assert set(added) == {"REFRESH_COMPATIBLE_TOOL_SHAS", "REFRESH_TOOL", "_NO_ECHO", "RefreshRefused", "_safe",
                          "dev_patterns", "is_dev_path", "is_dev_key", "RefreshBasis", "refresh_engine",
                          "read_refresh_logs", "default_refresh_blocks", "refresh_check", "refresh_dev", "main_refresh_dev",
                          "write_refreshed_log"}, added
    src_new, src_old = inspect.getsource(G.run), BACKUP.read_text()
    assert "refresh_from is None" in src_new and "refresh_engine(" in src_new
    # run() minus the refresh branches IS the predecessor's run(): undo the three hunks and compare the source text
    undo = src_new
    undo = undo.replace(', refresh_from: dict | None = None) -> dict:', ') -> dict:')
    undo = undo.replace('''writes each record (guarded).
    refresh_from = {set name: {"log": the block's candidates log (dict), "sha256": its file's}} (refresh-dev): the engine
    scans only the C2 dev targets and merges them into those logs (refresh_engine); every other step is this same code."""''',
                        'writes each record (guarded)."""')
    undo = undo.replace('''    refresh_meta: dict = {}
    basis = None
    if refresh_from is None:
        with fresh_tempdir("c2g13e_") as td:
            eng = g.run_sets(eng_sets, tgs, Path(td), cosine=g.COSINE if embed else None,
                             side=side and run_name in ("seed", "candidates"), side_parallel=side_parallel)
    else:                                          # refresh-dev: the basis checks, then the dev targets only, merged
        basis = RefreshBasis(tgs, embed)
        eng = refresh_engine(run_name, sets, eng_sets, guard, tgs, refresh_from, embed=embed, meta=refresh_meta,
                             basis=basis)
''', '''    with fresh_tempdir("c2g13e_") as td:
        eng = g.run_sets(eng_sets, tgs, Path(td), cosine=g.COSINE if embed else None,
                         side=side and run_name in ("seed", "candidates"), side_parallel=side_parallel)
''')
    undo = undo.replace('''        if refresh_from is not None:            # the old targets' side, again: a 20-40 min scan has passed since the start check
            late = late + basis.finalize(out[name], name, refresh_from[name]["log"])
''', '')
    undo = undo.replace('''        if refresh_from is not None:                            # bookkeeping only (a full run has no such key)
            out[name]["refreshed"] = list(refresh_from[name]["log"].get("refreshed") or []) + [
                {"unix": round(time.time()), "targets": sorted(C2_DEV), **refresh_meta[name]}]
''', '')
    undo = undo.replace('''            (kp.write_json if refresh_from is None else write_refreshed_log)(
                OUT / f"{name}.json", out[name], prereg_text=prereg_text)
''', '''            kp.write_json(OUT / f"{name}.json", out[name], prereg_text=prereg_text)
''')
    assert undo in src_old, "run() differs from the predecessor's outside the refresh-dev hunks"


def test_a_log_of_the_predecessor_is_a_valid_basis_and_equals_this_codes_log(rw, monkeypatch):
    pred = _load_backup()
    for attr in ("C2_DEV", "block_dir", "CODE_GUARD", "_CODE_AT_IMPORT", "a53_family_files", "G13_OHS4_TOOL", "GTPL_TOOL"):
        monkeypatch.setattr(pred, attr, getattr(G, attr))
    old_p = pred.run("candidates", ["T97"], embed=True, side=False, tgs=rw["tgs"] + pred.c2_dev_targets(),
                     exports=rw["exports"], write=False, prereg_text=A38)["c2_cand_T97"]
    assert old_p["tool_sha256"] in G.REFRESH_COMPATIBLE_TOOL_SHAS and old_p["tool_sha256"] != g.sha256_file(Path(G.__file__))
    new_a = full_run(rw)
    assert canon({**old_p, "tool_sha256": ""}) == canon({**new_a, "tool_sha256": ""})   # same record from either code
    save_log(rw, old_p)
    set_dev(rw["dev"], DEV_B)
    ref = refresh(rw)                                                   # the predecessor's log is accepted as a basis
    same_log(ref, full_run(rw))
    assert ref["tool_sha256"] == g.sha256_file(Path(G.__file__)) and ref["refreshed"][0]["from_tool_sha256"] == old_p["tool_sha256"]


# ---------------------------------------------------------------------------------------------------- reviewer issues (16 Oct)
def _check(w, **kw) -> dict:
    return G.refresh_check(["T97"], tgs=w["tgs"] + G.c2_dev_targets(), log_dir=w["logs"], **kw)


def test_refuses_when_a_target_has_a_coverage_gap_now(rw, monkeypatch):
    """The log was written with no gap (the real ones: G13_BIGPAT_STREAM=1); refreshing under an environment that gives a target
    a gap used to return complete=True where a full run on the same files is incomplete."""
    _old(rw)
    rw["tgs"][0]["gap"] = "synthetic_eval: train / validation descriptions not scanned (a coverage gap)"
    full = full_run(rw)
    assert full["complete"] is False and any("coverage gap" in w for w in full["incomplete_why"])
    no_scan(monkeypatch)
    probs = refusal(rw)
    assert any("coverage gap now" in x for x in probs["*"]), probs
    assert rw["writes"] == {}
    rw["tgs"][0]["gap"] = None                                           # the environment of the full run again: allowed
    assert _check(rw) == {}


def test_the_real_big_patent_gap_follows_the_environment_and_is_never_echoed(monkeypatch):
    """The real target list (specs only: no file is resolved, opened or listed): without G13_BIGPAT_STREAM=1 (or a written
    ruling) big_patent has a gap, refresh-dev refuses and the message withholds the sealed-source target's name."""
    monkeypatch.setattr(g, "target_files_now", lambda t: set())
    monkeypatch.delenv("G13_BIGPAT_STREAM", raising=False)
    monkeypatch.delenv("G13_BIGPAT_RULING", raising=False)
    full = g.targets() + G.c2_dev_targets()
    gaps = [x for x in RefreshBasisFor(full).general() if "coverage gap now" in x]
    assert len(gaps) == 1 and "<withheld " in gaps[0] and "ohs" not in gaps[0].lower(), gaps
    monkeypatch.setenv("G13_BIGPAT_STREAM", "1")
    assert not [x for x in RefreshBasisFor(g.targets() + G.c2_dev_targets()).general() if "coverage gap" in x]


def RefreshBasisFor(full):
    return G.RefreshBasis(full, embed=False)


@pytest.mark.parametrize("what", ["note", "blind", "status", "extra_target", "target_gone"])
def test_refuses_when_the_target_list_gives_another_record_than_the_log(rw, monkeypatch, what):
    _old(rw)
    t = rw["tgs"][0]
    if what == "note":
        t["note"] = "a note of another environment"
    elif what == "blind":
        t["blind"] = True
    elif what == "status":
        t["status"] = "pending_owner"
    elif what == "extra_target":
        rw["tgs"].append(g.target("synthetic_two", [f"abs:{rw['eval']}/none_*.jsonl"]))
    else:
        rw["tgs"].pop()
    no_scan(monkeypatch)
    probs = refusal(rw)["c2_cand_T97"]
    assert any(("target list" in x or "the log recorded another" in x) for x in probs), probs
    assert rw["writes"] == {}


def test_the_streamed_inputs_of_the_log_and_of_the_target_list_must_agree(rw, monkeypatch):
    a = full_run(rw)
    key = "hfstream:fake/bigpat/all/train-00000.parquet"
    spec = "hfstream:fake/bigpat|^all/(train|validation)-"
    save_log(rw, a)
    no_scan(monkeypatch)
    assert _check(rw) == {}
    rw["tgs"][0]["paths"].append(spec)                                   # streams now, the log read no streamed file
    assert any("hfstream" in x for x in refusal(rw)["c2_cand_T97"])
    save_log(rw, a, lambda d: d["engine"]["inputs_sha256"]["eval"].update({key: "9" * 64}))
    assert _check(rw) == {}                                              # both sides stream the same repo: allowed
    rw["tgs"][0]["paths"].remove(spec)                                   # the log streamed, the target list does not
    assert any("hfstream" in x for x in refusal(rw)["c2_cand_T97"])
    rw["tgs"][0]["paths"].append("hfstream:fake/other|^x")               # another repo than the one the log read
    assert any("hfstream" in x for x in refusal(rw)["c2_cand_T97"])


def test_check_with_no_block_to_check_is_an_error_not_an_ok(rw, monkeypatch, capsys):
    _old(rw)
    with pytest.raises(SystemExit) as e:
        G.refresh_check([], tgs=rw["tgs"] + G.c2_dev_targets(), log_dir=rw["logs"])
    assert "nothing to check" in str(e.value)
    for argv in (["refresh-dev", "--check", "--block"], ["refresh-dev", "--block"]):      # nargs='*' gives []
        with pytest.raises(SystemExit) as e:
            G.main(argv)
        assert "nothing to check" in str(e.value), argv
    monkeypatch.setattr(G, "default_refresh_blocks", lambda: [])        # no block has a candidates file
    for argv in (["refresh-dev", "--check"], ["refresh-dev"]):
        with pytest.raises(SystemExit) as e:
            G.main(argv)
        assert "nothing to check" in str(e.value), argv
    assert G.main(["refresh-dev", "--check", "--block", "T96"]) == 1   # a named block without a candidates file: a refusal
    assert "refresh-dev refused [c2_cand_T96]" in capsys.readouterr().out


def test_a_bare_file_name_is_a_dev_file_only_when_no_other_guarded_file_has_it(rw):
    basis = G.RefreshBasis(rw["tgs"] + G.c2_dev_targets())
    dev = {"data/c2_parts/T31/out/mixdev_S5.jsonl": "s"}
    other = {"c2_build/families/T97/mixdev_S5.jsonl": "x"}
    assert "mixdev_S5.jsonl" in basis.dev_names(dev, {}) and "mixdev_S5.jsonl" in basis.dev_names({}, dev, {"a/b.py": "y"}, {})
    assert "mixdev_S5.jsonl" not in basis.dev_names(dev, {}, old_rest=other)
    assert "mixdev_S5.jsonl" not in basis.dev_names({}, dev, cur_rest=other)
    assert "data/c2_parts/T31/out/mixdev_S5.jsonl" in basis.dev_names(dev, {}, other, other)    # the full path is exact


def test_a_changed_during_the_run_reason_of_a_non_dev_file_is_not_repaired_by_a_dev_scan(rw):
    """A reason that names `mixdev_a.jsonl` is a dev file's only if no non-dev guarded file has that file name."""
    a = full_run(rw)
    reason = f"mixdev_a.jsonl {G.CHANGED} (gone)"

    def only_reason(d):
        d["complete"], d["incomplete_why"] = False, [reason]

    def with_twin(d):
        only_reason(d)
        d["inputs_at_start"]["twin"] = "8" * 64                          # a non-dev guarded file called mixdev_a.jsonl
        d["inputs_at_start_paths"]["twin"] = "c2_build/families/T97/mixdev_a.jsonl"

    save_log(rw, a, only_reason)
    assert not any("cannot repair" in x for x in refusal_or_empty(rw)), "the dev file's own name is repaired"
    save_log(rw, a, with_twin)
    assert any("cannot repair" in x for x in refusal(rw)["c2_cand_T97"])


def refusal_or_empty(w) -> list:
    return [x for v in _check(w).values() for x in v]


# ---------------------------------------------------------------------------------------------------- reviewer issues (16 Oct, round 2)
# (1) the sealed-suite target was carried over unchecked, (2) the old targets' side was checked only at the start, (3) the
# sublabel task-name list is an unhashed input, plus the two operational notes (a half-written log; the helper modules).
FAKE_SEALED_CHECK = '''
import json, sys
a = sys.argv
src, out, summ = a[1], a[a.index("--out") + 1], a[a.index("--summary") + 1]
cfg = json.load(open(CFG_PATH))
rows = [json.loads(l) for l in open(src) if l.strip()]
with open(CFG_PATH + ".calls", "a") as f:
    f.write(str(len(rows)) + "\\n")
hit = [r for r in rows if any(n in r.get("state", "") for n in cfg["needles"])]
with open(out, "w") as f:
    for r in rows:
        f.write(json.dumps({"id": r["id"], "hit": r in hit, "hit_kinds": [{"kind": "p_struct"}] if r in hit else []}) + "\\n")
json.dump({"rows": len(rows), "rows_hit": len(hit), "suite_sha256": cfg["suite"], "checker_sha256": cfg["checker"]}, open(summ, "w"))
sys.exit(cfg.get("exit", 0))
'''


class SealedScript:
    """A fake sealed checker script behind the REAL decontam_g13.sealed_hits (which only ever RUNS it): the suite and checker
    hashes, the exit code and the needles it hits are in a json file the test rewrites between runs."""

    def __init__(self, tmp: Path, monkeypatch, tgs):
        self.cfg, self.script, self.mp = tmp / "sealed_cfg.json", tmp / "sealed_script.py", monkeypatch
        self.script.write_text(FAKE_SEALED_CHECK.replace("CFG_PATH", json.dumps(str(self.cfg))))
        self.set(suite="S1", checker="c" * 64, needles=["SEALEDLEAK"], exit=0)
        monkeypatch.setattr(g.sealed_hits, "__defaults__", (sys.executable, self.script))
        tgs.append(g.target("sealed_suite", [], kind="sealed_check", blind=True, note="fake sealed checker"))

    def set(self, **kw):
        cur = json.loads(self.cfg.read_text()) if self.cfg.exists() else {}
        cur.update(kw)
        self.cfg.write_text(json.dumps(cur))

    def calls(self) -> list:
        f = Path(str(self.cfg) + ".calls")
        return [int(x) for x in f.read_text().split()] if f.exists() else []

    def reset(self):
        Path(str(self.cfg) + ".calls").unlink(missing_ok=True)

    def gone(self):
        self.mp.setattr(g.sealed_hits, "__defaults__", (sys.executable, self.script.with_name("absent_checker.py")))


def sealed_world(rw, monkeypatch):
    """The sealed_check target (as the real `sealed_suite`) with a fake checker function that records the units it is given."""
    sw = {"suite": "S1", "checker": "c" * 64, "status": "scanned", "needle": "SEALEDLEAK", "calls": []}
    rw["tgs"].append(g.target("sealed_suite", [], kind="sealed_check", blind=True, note="fake sealed checker"))

    def fake_hits(units, train_path, py=None, checker=None):
        sw["calls"].append(len(units))
        if isinstance(sw["status"], Exception):
            raise sw["status"]
        rec = {"checker": "fake (run only)", "status": sw["status"], "exit": 0, "rows": 99, "rows_hit": 0,
               "suite_sha256": sw["suite"], "checker_sha256": sw["checker"]}
        ui = {i for i, u in enumerate(units) if any(sw["needle"] in t for _f, t in u["texts"])}
        return ({"sealed_p_structure": ui} if ui else {}), rec

    monkeypatch.setattr(g, "sealed_hits", fake_hits)
    return sw


class Late:
    """Call `fn()` right after the engine's dev-only scan returns: what happens in the 20 to 40 minutes of a real one. Set
    `.fn = None` to switch it off."""

    def __init__(self, monkeypatch):
        self.fn = None
        real = g.run_sets

        def scan_then(*a, **k):
            out = real(*a, **k)
            if self.fn is not None:
                self.fn()
            return out

        monkeypatch.setattr(g, "run_sets", scan_then)


def sublabel_world(rw):
    """A target with a sublabel (like tasksource's forbidden152): rows whose values hold a listed task name. The list is
    written long before any run of the test."""
    names = rw["tmp"] / "names.json"
    names.write_text(json.dumps(["alpha"]))
    back(names)
    rw["tgs"].append(g.target("synthetic_sub", [f"abs:{rw['eval']}/sub_*.jsonl"],
                              sublabel={"names": f"abs:{names}", "label": "sub_label"}))
    write_rows(rw["eval"] / "sub_1.jsonl", [{"id": "s1", "state": EVAL_SENT, "tag": "alpha"},
                                            {"id": "s2", "state": "Another eval row with the beta tag here today.", "tag": "beta"}])
    return names


def back(p: Path, seconds: float = 86400) -> None:
    t = time.time() - seconds
    os.utime(p, (t, t))




# ---- (1) the sealed suite
def test_a_changed_sealed_suite_is_a_refusal(rw, monkeypatch):
    """The reviewer's synthetic case: the suite hash changes S1 -> S2 and the new suite hits row r34. refresh-dev used to accept
    and return a log with r34 missing from drop_ids where a full run has it."""
    sw = sealed_world(rw, monkeypatch)
    a = _old(rw)
    assert a["complete"] and a["engine"]["targets"]["sealed_suite"]["suite_sha256"] == "S1"
    assert "r31" in a["drop_ids"] and "r34" not in a["drop_ids"]
    sw["suite"], sw["needle"] = "S2", "harbour pilots"            # the sealed suite was rebuilt
    full = full_run(rw)
    assert "r34" in full["drop_ids"] and full["engine"]["targets"]["sealed_suite"]["suite_sha256"] == "S2"
    no_scan(monkeypatch)
    probs = refusal(rw)["c2_cand_T97"]
    assert any("suite or the checker differs" in x for x in probs), probs
    assert "sealed_suite" not in "\n".join(probs) and rw["writes"] == {}          # the target is named by a hash only
    sw["suite"], sw["checker"] = "S1", "d" * 64                    # the checker alone differs, the suite as logged
    assert any("suite or the checker differs" in x for x in refusal(rw)["c2_cand_T97"])
    sw["checker"] = "c" * 64                                       # everything as logged: allowed
    assert _check(rw) == {}


def test_an_unchanged_sealed_suite_refresh_equals_a_full_run(rw, monkeypatch):
    sealed_world(rw, monkeypatch)
    save_log(rw, full_run(rw))
    set_dev(rw["dev"], DEV_B)
    ref = refresh(rw)
    same_log(ref, full_run(rw))
    assert ref["complete"] and ref["engine"]["targets"]["sealed_suite"]["status"] == "scanned"


@pytest.mark.parametrize("what", ["failed", "missing", "raises", "log_without_hashes", "log_not_scanned"])
def test_a_sealed_checker_that_cannot_run_now_or_has_no_logged_hashes_is_a_refusal(rw, monkeypatch, what):
    """A full run with a failing checker is incomplete (a reason in incomplete_why) where the old refresh returned complete."""
    sw = sealed_world(rw, monkeypatch)
    a = _old(rw)
    if what in ("failed", "missing"):
        sw["status"] = what
        full = full_run(rw)
        assert full["complete"] is False and any("sealed_check" in w for w in full["incomplete_why"])
    elif what == "raises":
        sw["status"] = subprocess.TimeoutExpired("checker", 1)
    elif what == "log_without_hashes":
        save_log(rw, a, lambda d: d["engine"]["targets"]["sealed_suite"].pop("suite_sha256"))
    else:
        save_log(rw, a, lambda d: d["engine"]["targets"]["sealed_suite"].update(status="failed"))
    no_scan(monkeypatch)
    probs = refusal(rw)["c2_cand_T97"]
    assert any(("cannot be run now" in x) or ("no 'scanned' record" in x) for x in probs), probs
    assert rw["writes"] == {}


def test_the_real_sealed_hits_is_run_once_on_one_probe_unit_and_its_summary_is_read(rw, monkeypatch, tmp_path):
    """The real decontam_g13.sealed_hits with a fake checker SCRIPT: the probe is one run, on one row, of the same checker, and
    the suite / checker hashes come from the checker's own summary."""
    sc = SealedScript(tmp_path, monkeypatch, rw["tgs"])
    a = _old(rw)
    assert a["complete"], a["incomplete_why"]
    srec = a["engine"]["targets"]["sealed_suite"]
    assert (srec["status"], srec["suite_sha256"], srec["checker_sha256"]) == ("scanned", "S1", "c" * 64)
    assert "r31" in a["drop_ids"] and sc.calls() and sc.calls()[0] > 1
    sc.reset()
    set_dev(rw["dev"], DEV_B)
    assert _check(rw) == {}
    assert sc.calls() == [1]                                         # ONE run of the checker, on ONE row: not on the candidates
    sc.reset()
    ref = refresh(rw)
    assert sc.calls() == [1, 1]                                      # at the start and again just before the write
    same_log(ref, full_run(rw))
    for change, why in ((dict(suite="S2"), "suite or the checker differs"), (dict(checker="e" * 64), "suite or the checker differs"),
                        (dict(exit=1), "cannot be run now")):
        sc.set(**change)
        assert any(why in x for x in refusal(rw)["c2_cand_T97"]), change
        sc.set(suite="S1", checker="c" * 64, exit=0)
    assert _check(rw) == {}
    sc.gone()                                                        # the checker file is missing
    assert any("cannot be run now" in x for x in refusal(rw)["c2_cand_T97"])


def test_the_real_sealed_check_target_is_covered_and_never_named(monkeypatch):
    monkeypatch.setattr(g, "target_files_now", lambda t: set())
    monkeypatch.setenv("G13_BIGPAT_STREAM", "1")
    basis = G.RefreshBasis(g.targets() + G.c2_dev_targets(), embed=False)
    (name,) = [t["name"] for t in basis.other_tgs if t["kind"] == "sealed_check"]
    monkeypatch.setattr(G.RefreshBasis, "sealed_now", lambda self: {"status": "scanned", "suite_sha256": "S2", "checker_sha256": "c"})
    msg = basis.sealed_check({"targets": {name: {"status": "scanned", "suite_sha256": "S1", "checker_sha256": "c"}}})
    assert len(msg) == 1 and "<withheld " in msg[0] and "sealed" not in msg[0].lower() and "ohs" not in msg[0].lower()
    assert basis.sealed_check({"targets": {name: {"status": "scanned", "suite_sha256": "S2", "checker_sha256": "c"}}}) == []
    assert basis.sealed_check({"targets": {}})                     # a log with no record of the target: refused


# ---- (2) the old targets' side, again just before the write
def test_an_old_target_eval_file_changing_during_the_scan_is_flagged_at_the_end(rw, monkeypatch):
    """The reviewer's p3: an old-target eval file rewritten after the dev scan returned a refreshed log with complete=True that
    claims the old sha of a file that no longer has it."""
    _old(rw)
    set_dev(rw["dev"], DEV_B)
    late = Late(monkeypatch)
    control = refresh(rw)
    assert control["complete"] and not [w for w in control["incomplete_why"] if w.startswith(G.RefreshBasis.LATE)]
    f = rw["eval"] / "synthetic_1.jsonl"
    text = f.read_text()
    late.fn = lambda: write_rows(f, [{"id": "e1", "state": EVAL_SENT + " plus", "options": ["yes", "no"]}])
    ref = refresh(rw)
    why = [w for w in ref["incomplete_why"] if w.startswith(G.RefreshBasis.LATE)]
    assert ref["complete"] is False and len(why) == 1 and "changed or gone" in why[0], ref["incomplete_why"]
    assert ref["a53"]["note"].startswith("withdrawn") and set(control["drop_ids"]) <= set(ref["drop_ids"])   # no waiver from it
    late.fn = None
    f.write_text(text)                                               # the file is back as it was: the log is still not a basis
    save_log(rw, ref)
    assert any("cannot repair" in x and G.RefreshBasis.LATE in x for x in refusal(rw)["c2_cand_T97"])


def test_a_new_eval_file_or_a_new_cosine_file_during_the_scan_is_flagged_at_the_end(rw, monkeypatch):
    _old(rw)
    late = Late(monkeypatch)
    late.fn = lambda: write_rows(rw["eval"] / "synthetic_2.jsonl", [{"id": "e2", "state": "A new eval file."}])
    ref = refresh(rw)
    assert ref["complete"] is False and any("not in the log" in w for w in ref["incomplete_why"])
    (rw["eval"] / "synthetic_2.jsonl").unlink()
    late.fn = lambda: rw["cos"].write_text(json.dumps({"threshold": 0.8, "model": "fake-bow", "max_seq_length": 64,
                                                       "dtype": "float32"}))
    ref = refresh(rw)
    assert ref["complete"] is False and any("cosine_threshold.json changed" in w for w in ref["incomplete_why"])


def test_the_sealed_checker_or_a_sealed_side_digest_changing_during_the_scan_is_flagged(rw, monkeypatch):
    sw = sealed_world(rw, monkeypatch)
    digests = {"sidea": "d1"}
    save_log(rw, full_run(rw), lambda d: d["engine"]["inputs_sha256"].update(sealed_side={"sidea": "d1"}))
    monkeypatch.setattr(g, "sealed_side_run", lambda units, owner, names, cosine, mode="scan", py=None:
                        {n: {"digest": digests[n]} for n in names})
    late = Late(monkeypatch)
    assert _check(rw) == {}
    assert refresh(rw)["complete"] is True                           # nothing changes: the late check passes
    late.fn = lambda: sw.__setitem__("suite", "S2")
    ref = refresh(rw)
    assert ref["complete"] is False and any("suite or the checker differs" in w for w in ref["incomplete_why"])
    sw["suite"] = "S1"
    late.fn = lambda: digests.__setitem__("sidea", "d2")
    ref = refresh(rw)
    assert ref["complete"] is False and any("sealed-side input digest changed" in w for w in ref["incomplete_why"])


def test_the_late_check_adds_each_reason_once(rw):
    _old(rw)
    basis = G.RefreshBasis(rw["tgs"] + G.c2_dev_targets())
    log = json.loads((rw["logs"] / "c2_cand_T97.json").read_text())
    rec = {"incomplete_why": [], "complete": True}
    assert basis.finalize(rec, "c2_cand_T97", log) == [] and rec == {"incomplete_why": [], "complete": True}
    write_rows(rw["eval"] / "synthetic_1.jsonl", [{"id": "e1", "state": EVAL_SENT + " plus", "options": ["yes", "no"]}])
    first = basis.finalize(rec, "c2_cand_T97", log)
    assert len(first) == 1 and rec["complete"] is False and rec["incomplete_why"] == first
    assert basis.finalize(rec, "c2_cand_T97", log) == [] and rec["incomplete_why"] == first        # not repeated


# ---- (3) the sublabel task-name list
def test_a_sublabel_names_list_written_after_the_log_is_a_refusal(rw, monkeypatch):
    """The reviewer's m13: the list changed after the log (same number of names, other names): refresh-dev accepted and the
    log lacked the counts a full run has. The engine notes no sha256 of the list, so the rule is the log's name count plus
    'not written since the run that wrote the log began'."""
    names = sublabel_world(rw)
    a = _old(rw)
    assert a["complete"] and a["engine"]["targets"]["synthetic_sub"]["sublabel_names"] == 1
    assert a["engine"]["sublabel_rows"]["sub_label"] == 1
    set_dev(rw["dev"], DEV_B)
    assert _check(rw) == {}                                          # the list is as it was (and old): allowed
    same_log(refresh(rw), full_run(rw))
    names.write_text(json.dumps(["beta"]))                           # other names, same count, written now
    assert canon(full_run(rw)) != canon(a)                           # a full run on the new list differs: the fixture matters
    no_scan(monkeypatch)
    assert any("written after the run" in x for x in refusal(rw)["c2_cand_T97"])
    names.write_text(json.dumps(["alpha", "beta"]))                  # another number of names (and an old file)
    back(names)
    assert any("has 2 now" in x for x in refusal(rw)["c2_cand_T97"])
    names.write_text(json.dumps(["alpha"]))                          # the original content, rewritten now: still refused
    assert any("written after the run" in x for x in refusal(rw)["c2_cand_T97"])
    back(names)                                                      # and with its old time back: allowed again
    assert _check(rw) == {}


def test_the_sublabel_rule_is_anchored_at_the_full_run_of_a_refreshed_log(rw, monkeypatch):
    names = sublabel_world(rw)
    a = _old(rw)
    set_dev(rw["dev"], DEV_B)
    r1 = refresh(rw)
    assert r1["refreshed"][0]["from_engine_wall_s"] == a["engine"]["wall_s"]
    save_log(rw, r1)
    assert G.RefreshBasis.run_start(r1) == a["engine"]["unix"] - a["engine"]["wall_s"]     # the FULL run's start, not the refresh's
    set_dev(rw["dev"], DEV_A)
    same_log(refresh(rw), a)                                         # a second refresh: allowed while the list is untouched
    # the full run began 2 h ago, the first refresh just now; the list was written 1 h ago: after the full run began
    save_log(rw, r1, lambda d: d["refreshed"][0].update(from_engine_unix=d["refreshed"][0]["from_engine_unix"] - 7200))
    back(names, 3600)
    no_scan(monkeypatch)
    assert any("written after the run" in x for x in refusal(rw)["c2_cand_T97"])


def test_run_start_of_a_log_and_of_a_refreshed_log():
    f = G.RefreshBasis.run_start
    assert f({"engine": {"unix": 1000, "wall_s": 100.5}}) == 899.5
    chain = {"engine": {"unix": 5000, "wall_s": 1}, "refreshed": [{"from_engine_unix": 1000, "from_engine_wall_s": 100},
                                                                   {"from_engine_unix": 5000, "from_engine_wall_s": 1}]}
    assert f(chain) == 900
    for bad in ({"engine": {"unix": 1000}}, {"engine": {"unix": 1000, "wall_s": True}}, {"engine": {}},
                {"engine": {}, "refreshed": [{"from_engine_unix": 1000}]}, {}):
        assert f(bad) is None


def test_a_log_that_does_not_say_when_its_run_began_is_no_basis_for_a_sublabel_target(rw):
    sublabel_world(rw)
    a = _old(rw)
    save_log(rw, a, lambda d: d["engine"].pop("wall_s"))
    assert any("does not say when its run began" in x for x in refusal(rw)["c2_cand_T97"])


def test_the_sublabel_list_changing_during_the_scan_is_flagged_at_the_end(rw, monkeypatch):
    names = sublabel_world(rw)
    _old(rw)
    late = Late(monkeypatch)
    late.fn = lambda: names.write_text(json.dumps(["beta"]))
    ref = refresh(rw)
    assert ref["complete"] is False and any("written after the run" in w for w in ref["incomplete_why"])


# ---- the two operational notes
def test_a_failed_write_leaves_the_old_log_whole_and_the_old_log_is_kept(rw, monkeypatch):
    old = save_log(rw, full_run(rw)) / "c2_cand_T97.json"
    before = old.read_bytes()
    set_dev(rw["dev"], DEV_B)

    def broken(p, obj, prereg_text=None):
        Path(p).write_text('{"half": ')                              # the process dies in the middle of the write
        raise OSError("disk full")

    monkeypatch.setattr(kp, "write_json", broken)
    with pytest.raises(OSError):
        G.refresh_dev(["T97"], tgs=rw["tgs"] + G.c2_dev_targets(), exports=rw["exports"], prereg_text=A38, log_dir=rw["logs"])
    assert old.read_bytes() == before and not (G.OUT / ".c2_cand_T97.json.tmp").exists()
    (kept,) = (G.OUT.parent / "logs_refresh_backup").glob("c2_cand_T97.*.json")
    assert kept.read_bytes() == before


def test_every_refresh_keeps_the_log_it_replaces_under_the_sha_the_provenance_names(rw):
    save_log(rw, full_run(rw))
    shas = []
    for dev in (DEV_B, DEV_A):
        shas.append(hashlib.sha256((G.OUT / "c2_cand_T97.json").read_bytes()).hexdigest())
        set_dev(rw["dev"], dev)
        G.refresh_dev(["T97"], tgs=rw["tgs"] + G.c2_dev_targets(), exports=rw["exports"], prereg_text=A38, log_dir=rw["logs"])
    final = json.loads((G.OUT / "c2_cand_T97.json").read_text())
    assert [x["from_log_sha256"] for x in final["refreshed"]] == shas
    back_dir = G.OUT.parent / "logs_refresh_backup"
    assert sorted(p.name for p in back_dir.iterdir()) == sorted(f"c2_cand_T97.{s[:12]}.json" for s in shas)
    for s in shas:                                                   # each backup IS the log the entry names
        assert hashlib.sha256((back_dir / f"c2_cand_T97.{s[:12]}.json").read_bytes()).hexdigest() == s


def test_a_full_run_still_writes_through_the_plain_guarded_writer(rw):
    G.run("candidates", ["T97"], embed=True, side=False, tgs=rw["tgs"] + G.c2_dev_targets(), exports=rw["exports"],
          write=True, prereg_text=A38)
    assert list(rw["writes"]) == [str(G.OUT / "c2_cand_T97.json")]          # no temp file, no backup: the predecessor's path
    assert not (G.OUT.parent / "logs_refresh_backup").exists()


def test_a_refresh_records_the_helper_shas_but_does_not_gate_on_them(rw, monkeypatch):
    a = full_run(rw)
    save_log(rw, a)
    set_dev(rw["dev"], DEV_B)
    r1 = refresh(rw)
    h = r1["refreshed"][0]["helpers_sha256"]
    assert {Path(k).name for k in h} == {"c2io.py", "mixio.py", "paths.py"} and all(len(v) == 64 for v in h.values())
    assert h == G.RefreshBasis.helpers_now() and r1["refreshed"][0]["from_engine_wall_s"] == a["engine"]["wall_s"]
    save_log(rw, r1)
    monkeypatch.setattr(G.RefreshBasis, "helpers_now", staticmethod(lambda: {"c2_build/c2io.py": "f" * 64}))
    r2 = refresh(rw)                                                 # a helper changed between the refreshes: still allowed
    assert r2["complete"] and r2["refreshed"][1]["helpers_sha256"] == {"c2_build/c2io.py": "f" * 64}
