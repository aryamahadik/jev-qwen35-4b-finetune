"""families/T07/haiku/redo3/test_admit_redo3.py: the T07 redo3 admit stage (admit_redo3.py) and the pools/redo3 supplement.

The stage is computed once in memory (about two minutes: it rebuilds the family's registry); mutation cases run on copies.
Nothing in the repository is written. Run (from lean/):
  PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python -m pytest -q -p no:cacheprovider \
      c2_build/families/T07/haiku/redo3/test_admit_redo3.py
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
import stat
import sys
from collections import Counter
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[4]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from families.T07 import authoring as A  # noqa: E402
from families.T07 import freeze_pools as FZ  # noqa: E402
from families.T07 import merged_pools as MP  # noqa: E402
from families.T07 import plugin as P  # noqa: E402
from families.T07.haiku.redo3 import admit_redo3 as AD  # noqa: E402
from families.T07.haiku.redo3 import build_redo3 as R3  # noqa: E402
from families.T07.haiku.redo3 import build_redo3_reads as RR  # noqa: E402

YN_MISSES = "q.t07.yn_misses"


@pytest.fixture(scope="module")
def c():
    return AD.compute()


@pytest.fixture(scope="module")
def pools():
    return MP.load()


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _fresh(c):
    """(registry copy with the new forms' votes cleared, raw read answers from disk)."""
    reg = copy.deepcopy(c["st"]["reg"])
    for fid in c["st"]["read_fids"]:
        reg.forms[fid].extractions = []
    raw, _ = AD.read_answers(c["st"])
    return reg, raw


# ------------------------------------------------------------------------------------------------ the files
def test_pool_files_on_disk_are_the_rebuild_byte_for_byte(c):
    assert sorted(c["texts"]) == sorted(AD.FILES + ("MANIFEST.json",))
    for name, text in c["texts"].items():
        assert (AD.SUPP / name).read_bytes() == text.encode("utf-8"), name


def test_manifest_hashes_match_files_and_files_are_read_only():
    man = json.loads((AD.SUPP / "MANIFEST.json").read_text(encoding="utf-8"))
    assert sorted(man["pool_files"]) == sorted(AD.FILES)
    for name, info in man["pool_files"].items():
        assert _sha(AD.SUPP / name) == info["sha256"] and (AD.SUPP / name).stat().st_size == info["bytes"]
    for p in AD.SUPP.iterdir():
        assert p.stat().st_mode & (stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH) == 0, p.name
    assert man["g0_sha256"] == P.T07Plugin.G0_SHA256_AUTHORED and man["version"] == "r3"
    assert "G13-seed" in man["not_run"][0]


def test_earlier_layers_are_untouched():
    for root in (MP.V1, MP.R2):
        man = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))
        for name, info in man["pool_files"].items():
            assert _sha(root / name) == info["sha256"], f"{root.name}/{name}"
    man = json.loads((AD.SUPP / "MANIFEST.json").read_text(encoding="utf-8"))
    assert man["inputs"]["baseline_manifest_sha256"] == {"v1": _sha(MP.V1 / "MANIFEST.json"),
                                                         "redo2": _sha(MP.R2 / "MANIFEST.json")}
    assert sorted(p.name for p in MP.V1.glob("redo*")) == ["redo2", "redo3"]


def test_every_input_answer_is_in_the_manifest_and_none_failed_audit():
    man = json.loads((AD.SUPP / "MANIFEST.json").read_text(encoding="utf-8"))
    want = {}
    for root, sub in ((R3.ROOT, "answers"), (RR.READS_ROOT, "answers")):
        for p in sorted((root / sub).glob("*.json")):
            want[p.stem] = _sha(p)
    assert man["inputs"]["answer_sha256"] == want and len(want) == 4
    assert man["inputs"]["failed_audit"] == []
    assert man["inputs"]["gaps_closed"] == {"wording": 1, "packs": 11}


# ------------------------------------------------------------------------------------------------ G-LEX
def test_each_new_wording_has_two_independent_agreeing_reads(c):
    forms = json.loads((AD.SUPP / "lexicon_add.json").read_text(encoding="utf-8"))["forms"]
    words = json.loads((AD.SUPP / "wordings_add.json").read_text(encoding="utf-8"))["items"]
    assert len(forms) == len(words) == 3
    for f in forms:
        assert f["sem_id"] == YN_MISSES and f["origin"] == AD.WORD_ORIGIN and not f["held_out"]
        assert f["extractions"] == [["redo3-r1", YN_MISSES], ["redo3-r2", YN_MISSES]], f["form_id"]
        assert f["status"] == "admitted"
    rec = json.loads((AD.SUPP / "extraction_record.json").read_text(encoding="utf-8"))["lexicon_extractions"]
    assert len(rec) == 6 and {r["read"] for r in rec} == {"redo3-r1", "redo3-r2"}
    assert all(r["meaning"] == A.Q_SEM_MEANING["yn_misses"] and r["sem_id"] == YN_MISSES for r in rec)
    assert {w["form_id"] for w in words} == {f["form_id"] for f in forms}
    assert all(w["qform"] == "yn_misses" and not w["held_out"] for w in words)
    # the wording texts are the three Haiku outputs, in the pool as written
    ans = json.loads((R3.ROOT / "answers" / "T07-author_wording-30ca5994-000.json").read_text(encoding="utf-8"))
    assert sorted(w["text"] for w in words) == sorted(ans[0]["wordings"])


def test_the_two_reads_were_separate_tasks_with_separate_answer_files():
    idx = json.loads((RR.READS_ROOT / "TASKS.json").read_text(encoding="utf-8"))
    assert [t["read"] for t in idx["tasks"]] == ["redo3-r1", "redo3-r2"]
    assert len({t["task_id"] for t in idx["tasks"]}) == len({t["answer_file"] for t in idx["tasks"]}) == 2
    assert len({t["batch_id"] for t in idx["tasks"]}) == 2


def test_no_earlier_form_changed_status_or_votes(pools):
    base = MP.load(through="redo2")
    new = {f["form_id"]: f for f in pools["lexicon"]}
    assert all(new[f["form_id"]] == f for f in base["lexicon"])
    assert pools["lexicon"][:len(base["lexicon"])] == base["lexicon"]


def test_glex_gate_passes_on_the_merged_pools(pools):
    assert MP.glex_problems(pools) == []
    adm = {f["form_id"] for f in pools["lexicon"] if f["status"] == "admitted"}
    assert all(w["form_id"] in adm for w in pools["wordings"])


def test_a_dissent_a_missing_vote_and_an_off_list_pick_keep_a_wording_out(c):
    st = c["st"]
    fid = st["read_fids"][0]
    other = A.Q_SEM_MEANING["yn_fails_to"]                           # what the redo2 'forfeit' wordings were read as
    # a dissent in the second read
    reg, raw = _fresh(c)
    b2 = st["batches"]["redo3-r2"]
    qid = next(q for q, i in b2.key.items() if i == fid)
    tid = b2.task_of[qid]
    raw["redo3-r2"][tid] = [dict(a, meaning=other) if a["qid"] == qid else a for a in raw["redo3-r2"][tid]]
    rec = AD.record_votes(st, raw, reg)
    assert reg.status(fid) == "rejected"
    layer = AD.build_layer(st, rec, reg)
    assert fid not in {w["form_id"] for w in layer["wordings_add.json"]["items"]} and layer["wordings_add.json"]["n"] == 2
    assert any(d["stage"] == "G-LEX" and d["form_id"] == fid for d in layer["quarantine.json"]["items"])
    assert [f["status"] for f in layer["lexicon_add.json"]["forms"]].count("rejected") == 1      # still recorded
    # one read only: pending, not admitted
    reg, raw = _fresh(c)
    for fid2 in st["read_fids"]:
        reg.record_extraction(fid2, "redo3-r1", YN_MISSES)
    assert {reg.status(f) for f in st["read_fids"]} == {"pending"}
    layer = AD.build_layer(st, [], reg)
    assert layer["wordings_add.json"]["n"] == 0 and layer["lexicon_add.json"]["forms"][0]["status"] == "pending"
    # an off-list pick maps to no sem: rejected for good
    reg, raw = _fresh(c)
    b1 = st["batches"]["redo3-r1"]
    q1 = next(q for q, i in b1.key.items() if i == fid)
    raw["redo3-r1"][b1.task_of[q1]] = [dict(a, meaning="something else") if a["qid"] == q1 else a
                                       for a in raw["redo3-r1"][b1.task_of[q1]]]
    AD.record_votes(st, raw, reg)
    assert reg.status(fid) == "rejected" and reg.forms[fid].extractions[0] == ("redo3-r1", None)


def test_a_read_answered_twice_by_one_extractor_is_refused(c):
    reg, raw = _fresh(c)
    AD.record_votes(c["st"], raw, reg)
    with pytest.raises(Exception, match="already extracted"):          # extractors must be independent
        AD.record_votes(c["st"], raw, reg)


def test_three_rejected_wordings_leave_the_line_one_short(c):
    st = c["st"]
    reg, raw = _fresh(c)
    for read in AD.RR.READS:
        for tid, arr in raw[read].items():
            raw[read][tid] = [dict(a, meaning=A.Q_SEM_MEANING["yn_not_gets"]) for a in arr]
    rec = AD.record_votes(st, raw, reg)
    layer = AD.build_layer(st, rec, reg)
    assert layer["wordings_add.json"]["n"] == 0
    _pools, v = AD.merged_verdict(layer)
    assert v["ready"] is False
    assert {s["item"]: (s["admitted"], s["short_by"]) for s in v["shortfalls"]} == {"wordings training yn_misses": (19, 1)}


# ------------------------------------------------------------------------------------------------ packs
def test_seventeen_clean_training_packs_close_the_asked_line(pools):
    add = json.loads((AD.SUPP / "packs_add.json").read_text(encoding="utf-8"))
    assert add["n"] == len(add["items"]) == 17
    assert all(not p["held_out"] and p["piece_id"].startswith("t07r3.pack.") for p in add["items"])
    assert len(pools["packs"]) == 66 >= FZ.PACK_ASKED == 60
    assert sum(not p["held_out"] for p in pools["packs"]) == 60 and sum(p["held_out"] for p in pools["packs"]) == 6
    assert MP.pack_problems(pools) == []
    assert Counter(len(p["ladder"]) for p in add["items"]) == Counter({4: 11, 3: 6})


def test_new_packs_are_exactly_the_answered_packs():
    add = json.loads((AD.SUPP / "packs_add.json").read_text(encoding="utf-8"))["items"]
    ans = json.loads((R3.ROOT / "answers" / "T07-author_pack-56620cf3-000.json").read_text(encoding="utf-8"))
    given = {json.dumps(a["pack"], sort_keys=True) for a in ans}
    kept = {json.dumps({k: p[k] for k in ("store", "ladder", "regions", "categories", "customers")}, sort_keys=True)
            for p in add}
    assert kept == given and len(kept) == 17


def test_new_pack_words_clash_with_no_seed_pack_or_pool_text(pools):
    """Re-checked here with plain word sets, not with the stage's own functions."""
    base = MP.load(through="redo2")
    new = [p for p in pools["packs"] if p["piece_id"].startswith("t07r3.")]
    old = base["packs"]
    word = lambda t: set(re.findall(r"[a-z]+", t.casefold()))                                    # noqa: E731
    texts = [x["text"] for k in ("skins", "attacks", "wordings") for x in base[k]]
    texts += [w["text"] for w in pools["wordings"]]
    texts += [d["text"].replace(d["run"], " ").replace(d["store"], " ") for d in base["documents"]]
    texts += [f["text"] for f in pools["lexicon"] if f["status"] == "admitted"]
    pool_words = set().union(*(word(re.sub(r"\{[A-Za-z0-9_|]+\}", " ", t)) for t in texts))
    taken = set()
    for p in old:
        for f in ("ladder", "regions", "categories"):
            for v in p[f]:
                taken |= word(v)
    for p in new:
        surf = [v for f in ("ladder", "regions", "categories") for v in p[f]]
        sw = set().union(*(word(v) for v in surf))
        assert not sw & pool_words, (p["store"], sorted(sw & pool_words))
        assert not sw & taken, (p["store"], sorted(sw & taken))
        names = [p["store"], *p["customers"]]
        assert not any(word(n) & sw for n in names)                                              # no own-name surface
        assert len({v.casefold() for v in [*surf, *names]}) == len(surf) + len(names)
    stores = [p["store"].casefold() for p in pools["packs"]] + [s.casefold() for s in P.STORES + P.STORES_HELD]
    assert len(stores) == len(set(stores))


def test_pack_decisions_account_for_all_seventeen(c):
    dec = c["layer"]["quarantine.json"]["pack_decisions"]
    assert len(dec) == 17 and all(d["status"] == "kept" and not d["reasons"] for d in dec)
    assert c["manifest"]["gates"]["packs"] == {"kept": 17, "asked": 17, "problems": [], "pass": True}


# ------------------------------------------------------------------------------------------------ verdict
def test_verdict_is_ready_every_target_met_and_no_target_lowered(c, pools):
    v = MP.verdict(pools)
    assert v["ready"] is True and v["shortfalls"] == [] and c["verdict"]["ready"] is True
    assert all(g["pass"] for g in v["gates"].values())
    assert (FZ.PACK_ASKED, FZ.PACK_NEEDED, FZ.ATTACK_TARGET) == (60, {"training": 32, "held_out": 4}, 60)
    assert FZ.WORDING_TARGET["training"]["yn_misses"] == 20 and set(FZ.MODE_T_TARGET.values()) == {40, 24}
    assert FZ.CANON_PER_SEM == 2 and FZ.PARAPHRASE_ADMIT == 6 and FZ.G3H_BAR == 0.98
    assert (v["counts"]["attacks"], v["counts"]["packs"]) == (65, 66)
    w = Counter((x["qform"], x["held_out"]) for x in pools["wordings"])
    assert w[("yn_misses", False)] == 22 and w[("yn_misses", True)] == 7


def test_the_verdict_on_disk_equals_the_one_computed_in_memory(c, pools):
    mem, disk = c["verdict"], MP.verdict(pools)
    assert (mem["ready"], mem["shortfalls"], mem["counts"]) == (disk["ready"], disk["shortfalls"], disk["counts"])
    assert c["pools"]["packs"] == pools["packs"] and c["pools"]["wordings"] == pools["wordings"]
    assert c["pools"]["lexicon"] == pools["lexicon"]


def test_g3h_bar_still_holds_and_redo3_added_no_mode_f_text(pools):
    for rnd, regs in pools["g3h"].items():
        assert all(d["ok"] / d["n"] >= FZ.G3H_BAR for d in regs.values()), rnd
    assert set(pools["g3h"]) == {"v1", "redo2"}
    assert len(pools["documents"]) == 182


def test_the_redo3_task_files_still_equal_their_rebuild_after_the_freeze():
    """build_redo3*.py read the baseline (v1 + redo2), not the merged pools, so the frozen tasks stay reproducible."""
    files, _ = R3.author_files(g=RR.gap_dict())
    assert R3.check_on_disk(R3.ROOT, files) == []
    assert R3.BASELINE == "redo2"


# ------------------------------------------------------------------------------------------------ guards
def test_an_audit_failed_task_stops_the_stage_and_an_invalid_answer_is_a_problem():
    assert AD.check_answers()[0] == []
    probs, _ = AD.check_answers(["T07-extract_lex-0830ebcd-000"])
    assert probs and any("ignored" in p for p in probs)
    probs, _ = AD.check_answers(["T07-author_pack-56620cf3-000"])
    assert probs and any("ignored" in p for p in probs)


def test_an_existing_different_layer_is_not_overwritten(c, tmp_path, monkeypatch):
    monkeypatch.setattr(AD, "SUPP", tmp_path / "redo3")
    (tmp_path / "redo3").mkdir()
    for n, t in c["texts"].items():
        (tmp_path / "redo3" / n).write_text(t, encoding="utf-8")
    assert AD.write_layer(c["texts"]) == "unchanged"                          # same bytes: nothing to do
    (tmp_path / "redo3" / "packs_add.json").write_text("{}", encoding="utf-8")
    with pytest.raises(SystemExit, match="redo3_prev"):
        AD.write_layer(c["texts"])
    assert (tmp_path / "redo3" / "packs_add.json").read_text(encoding="utf-8") == "{}"      # untouched
    (tmp_path / "redo3" / "packs_add.json").write_text(c["texts"]["packs_add.json"], encoding="utf-8")
    (tmp_path / "redo3" / "stray.json").write_text("{}", encoding="utf-8")
    with pytest.raises(SystemExit, match="exists and differs"):
        AD.write_layer(c["texts"])


def test_writers_refuse_before_a38():
    from c2_kit import paths
    with pytest.raises(paths.DataBeforeFreeze):
        paths.write_text(AD.SUPP / "x.json", "{}", prereg_text="no ruling here")
