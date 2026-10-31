"""families/T07/test_merged_pools.py: the v1 + redo2 + redo3 pool merge and the independent G0 verdict (merged_pools.py).

Reads the frozen pools; mutations run on copies under pytest's tmp_path. Nothing in the repository is written.
Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/families/T07/test_merged_pools.py
"""
from __future__ import annotations

import copy
import hashlib
import json
import shutil
import sys
from collections import Counter
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from families.T07 import freeze_pools as FZ  # noqa: E402
from families.T07 import merged_pools as M  # noqa: E402
from families.T07 import plugin as P  # noqa: E402


@pytest.fixture(scope="module")
def pools():
    """Every layer: v1 + redo2 + redo3 (what the generator loads)."""
    return M.load()


@pytest.fixture(scope="module")
def base():
    """v1 + redo2: the baseline the redo3 tasks were authored against (the 13 Oct / STAGE_A3 state)."""
    return M.load(through="redo2")


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def test_v1_pools_are_untouched_and_redo2_and_redo3_files_match_their_manifest():
    for root in (M.V1, M.R2, M.R3):
        man = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))
        assert man["pool_files"]
        for name, info in man["pool_files"].items():
            assert _sha(root / name) == info["sha256"], f"{root.name}/{name}"
            assert (root / name).stat().st_mode & 0o222 == 0, f"{name} is writable"


def _wording_counts(pools):
    w = Counter((x["qform"], "held_out" if x["held_out"] else "training") for x in pools["wordings"])
    return {q: {k: w[(q, k)] for k in ("training", "held_out")} for q in FZ.QFORMS}


def test_merged_counts_equal_the_admit_stage_counts(base):
    merged = base["manifests"]["redo2"]["counts"]["merged"]
    assert dict(sorted(Counter(s["register"] for s in base["skins"]).items())) == merged["skins_by_register"]
    assert dict(sorted(Counter(d["register"] for d in base["documents"]).items())) == merged["documents_by_register"]
    assert len(base["attacks"]) == merged["attacks"]
    assert _wording_counts(base) == merged["wordings"]
    assert len(base["packs"]) == 49 and base["manifests"].get("redo3") is None


def test_merged_counts_equal_the_redo3_admit_stage_counts(pools):
    merged = pools["manifests"]["redo3"]["counts"]["merged"]
    assert dict(sorted(Counter(s["register"] for s in pools["skins"]).items())) == merged["skins_by_register"]
    assert dict(sorted(Counter(d["register"] for d in pools["documents"]).items())) == merged["documents_by_register"]
    assert len(pools["attacks"]) == merged["attacks"]
    assert _wording_counts(pools) == merged["wordings"]
    assert merged["packs"] == {"total": len(pools["packs"]), "training": sum(not p["held_out"] for p in pools["packs"]),
                               "held_out": sum(p["held_out"] for p in pools["packs"])}
    assert merged["lexicon_admitted"] == sum(f["status"] == "admitted" for f in pools["lexicon"])


def test_redo3_only_adds_packs_wordings_and_forms(base, pools):
    for key in ("skins", "attacks", "documents", "g3h", "canonical_status_r2"):
        assert pools[key] == base[key], key
    for key in ("packs", "wordings", "lexicon"):
        assert pools[key][:len(base[key])] == base[key], key              # earlier rows first, byte for byte
        assert len(pools[key]) > len(base[key])
    assert (len(pools["packs"]) - 49, len(pools["wordings"]) - len(base["wordings"]),
            len(pools["lexicon"]) - len(base["lexicon"])) == (17, 3, 3)


def test_ids_texts_and_briefs_are_unique_across_both_layers(pools):
    for key, field in (("skins", "skin_id"), ("attacks", "attack_id"), ("wordings", "wording_id"),
                       ("documents", "doc_id"), ("lexicon", "form_id"), ("packs", "pack_id")):
        ids = [x[field] for x in pools[key]]
        assert len(ids) == len(set(ids)), key
    briefs = [d.get("v1_brief") or d["internal_id"] for d in pools["documents"]]
    assert len(briefs) == len(set(briefs)) == 182
    norm = lambda t: " ".join(t.casefold().split())      # noqa: E731
    for key in ("skins", "attacks", "wordings"):
        texts = [norm(x["text"]) for x in pools[key]]
        assert len(texts) == len(set(texts)), key


def test_v1_lexicon_statuses_are_unchanged_by_redo2_and_redo3(pools):
    v1 = {f["form_id"]: f for f in json.loads((M.V1 / "lexicon.json").read_text(encoding="utf-8"))["forms"]}
    merged = {f["form_id"]: f for f in pools["lexicon"]}
    assert set(v1) <= set(merged)
    assert all(merged[i]["status"] == f["status"] and merged[i]["extractions"] == f["extractions"] for i, f in v1.items())
    assert not set(v1) & {f["form_id"] for f in json.loads((M.R2 / "lexicon_add.json").read_text())["forms"]}
    r2 = {f["form_id"]: f for f in json.loads((M.R2 / "lexicon_add.json").read_text())["forms"]}
    assert all(merged[i] == f for i, f in r2.items())                    # redo3 changes no redo2 form either
    r3 = json.loads((M.R3 / "lexicon_add.json").read_text())["forms"]
    assert not set(r3_f["form_id"] for r3_f in r3) & (set(v1) | set(r2))
    # the v1 status.out rejections stand (H32: no re-read, no re-vote); the R1 pair is new
    old_status = [f for f in v1.values() if f["sem_id"] == "t07.status.out" and f["origin"] == "canonical"]
    assert old_status and all(f["status"] == "rejected" for f in old_status)
    new_canon = [f for f in pools["lexicon"] if f["origin"] == "canonical_r2"]
    assert sorted(f["text"] for f in new_canon) == sorted(pools["canonical_status_r2"]) and len(new_canon) == 2
    assert all(f["status"] == "admitted" for f in new_canon)


def test_every_new_form_was_read_by_two_independent_redo2_extractors(pools):
    new = json.loads((M.R2 / "lexicon_add.json").read_text())["forms"]          # 64 Haiku forms + the 2 R1 canonical
    assert len(new) == 66
    for f in new:
        assert sorted(e for e, _ in f["extractions"]) == ["redo2-r1", "redo2-r2"], f["form_id"]
        agree = all(s == f["sem_id"] for _, s in f["extractions"])
        assert (f["status"] == "admitted") == agree, f["form_id"]
    rec = json.loads((M.R2 / "extraction_record.json").read_text())["lexicon_extractions"]
    assert len(rec) == 2 * len(new) and {r["read"] for r in rec} == {"redo2-r1", "redo2-r2"}


def test_glex_gate_holds_on_the_merged_pools(pools):
    assert M.glex_problems(pools) == []
    assert all(len({e for e, _ in f["extractions"]}) >= 2 for f in pools["lexicon"] if f["status"] == "admitted")


def test_glex_rule_catches_a_dissent_a_missing_vote_and_an_unadmitted_use(pools):
    bad = copy.deepcopy(pools)
    adm = next(f for f in bad["lexicon"] if f["status"] == "admitted" and f["origin"] == "haiku_form_r2")
    adm["extractions"][1][1] = "t07.region.in"                       # one dissent on an admitted form
    assert any("marked admitted" in p for p in M.glex_problems(bad))
    bad = copy.deepcopy(pools)
    adm = next(f for f in bad["lexicon"] if f["status"] == "admitted" and f["origin"] == "haiku_form_r2")
    adm["extractions"] = adm["extractions"][:1]                      # 1/2 is not enough
    assert any("marked admitted" in p for p in M.glex_problems(bad))
    bad = copy.deepcopy(pools)
    rej = next(f for f in bad["lexicon"] if f["status"] == "rejected")
    fid = rej["form_id"]
    bad["wordings"][0] = dict(bad["wordings"][0], form_id=fid, text=rej["text"])
    assert any("not an admitted form" in p for p in M.glex_problems(bad))
    bad = copy.deepcopy(pools)
    bad["documents"][0] = dict(bad["documents"][0], lexicon_form_ids=[fid])
    assert any("canonical form" in p for p in M.glex_problems(bad))


def test_strict_kinds_need_three_votes_but_t07_has_none(pools):
    assert {"precedence", "window"} == set(M.LX.STRICT_KINDS)
    assert not {f["kind"] for f in pools["lexicon"]} & set(M.LX.STRICT_KINDS)
    bad = copy.deepcopy(pools)
    f = next(f for f in bad["lexicon"] if f["status"] == "admitted")
    f["kind"] = "precedence"                                         # 2/2 would not do for a strict kind
    assert any("3/3" in p for p in M.glex_problems(bad))


def test_g3h_bar_holds_in_each_read_pass(pools):
    for rnd, regs in pools["g3h"].items():
        for reg, d in regs.items():
            assert d["ok"] / d["n"] >= FZ.G3H_BAR, (rnd, reg)
    rec = json.loads((M.R2 / "g3h_record.json").read_text())
    assert rec["quarantined_registers"] == [] and all(t["ok"] for t in rec["texts"].values())


def test_baseline_verdict_matches_the_redo2_manifest_and_names_the_exact_shortfalls(base):
    v = M.verdict(base)
    man = base["manifests"]["redo2"]
    got = {(s["item"].split(" (")[0], s["target"], s["admitted"], s["short_by"]) for s in v["shortfalls"]}
    want = {(s["item"].split(" (")[0], s["target"], s["admitted"], s["short_by"]) for s in man["shortfalls"]}
    assert got == want == {("wordings training yn_misses", 20, 19, 1), ("packs asked", 60, 49, 11)}
    assert v["ready"] is False and v["gates"]["G-LEX"]["pass"] and v["gates"]["G3-H"]["pass"]


def test_full_verdict_is_ready_and_matches_the_redo3_manifest(pools):
    v = M.verdict(pools)
    man = pools["manifests"]["redo3"]
    assert v["shortfalls"] == man["shortfalls"] == [] and man["n_shortfalls"] == 0
    assert v["ready"] is True and man["ready"] is True
    assert all(g["pass"] for g in v["gates"].values()) and set(v["gates"]) >= {"G-LEX", "G3-H"}
    assert v["counts"]["packs"] == 66 and v["counts"]["packs_training"] == 60 and v["counts"]["packs_held_out"] == 6
    w = _wording_counts(pools)
    assert all(w[q]["training"] >= FZ.WORDING_TARGET["training"][q] and w[q]["held_out"] >= 6 for q in FZ.QFORMS)
    assert w["yn_misses"] == {"training": 22, "held_out": 7}


def test_verdict_never_lowers_a_target(pools, base):
    assert FZ.PACK_ASKED == 60 and FZ.ATTACK_TARGET == 60 and FZ.WORDING_TARGET["training"]["yn_misses"] == 20
    assert set(FZ.MODE_T_TARGET.values()) == {40, 24}
    v = M.verdict(pools)
    assert v["counts"]["attacks"] >= 60
    # removing one admitted yn_misses training wording makes the shortfall one bigger: the verdict reads the pools
    bad = copy.deepcopy(base)
    i = next(i for i, w in enumerate(bad["wordings"]) if w["qform"] == "yn_misses" and not w["held_out"])
    del bad["wordings"][i]
    short = {s["item"]: s["short_by"] for s in M.verdict(bad)["shortfalls"]}
    assert short["wordings training yn_misses"] == 2
    # the full pools: 22 of 20, so three removals are needed to fall one short; 66 of 60 packs, so seven removals
    bad = copy.deepcopy(pools)
    for _ in range(3):
        bad["wordings"].pop(next(i for i, w in enumerate(bad["wordings"]) if w["qform"] == "yn_misses"
                                 and not w["held_out"]))
    assert {s["item"]: s["short_by"] for s in M.verdict(bad)["shortfalls"]} == {"wordings training yn_misses": 1}
    bad = copy.deepcopy(pools)
    del bad["packs"][-7:]
    assert {s["item"]: s["short_by"] for s in M.verdict(bad)["shortfalls"]} == {"packs asked (G0 section 4)": 1}
    bad = copy.deepcopy(pools)
    bad["documents"].pop()
    assert any(s["item"].startswith("Mode F texts") for s in M.verdict(bad)["shortfalls"])


def test_a_changed_pool_file_is_refused(tmp_path):
    v1, r2 = tmp_path / "pools", tmp_path / "pools" / "redo2"
    shutil.copytree(M.V1, v1)
    p = r2 / "skins_add.json"
    p.chmod(0o644)
    p.write_text(p.read_text(encoding="utf-8").replace("T07-", "T08-", 1), encoding="utf-8")
    with pytest.raises(M.PoolError, match="sha256 differs"):
        M.load(v1, r2)


def test_a_changed_redo3_file_is_refused_and_through_redo2_does_not_read_it(tmp_path):
    v1, r2 = tmp_path / "pools", tmp_path / "pools" / "redo2"
    shutil.copytree(M.V1, v1)
    p = v1 / "redo3" / "packs_add.json"
    p.chmod(0o644)
    p.write_text(p.read_text(encoding="utf-8").replace("Ferrin Brook", "Ferrin Brooke", 1), encoding="utf-8")
    with pytest.raises(M.PoolError, match="sha256 differs"):
        M.load(v1, r2)
    assert len(M.load(v1, r2, through="redo2")["packs"]) == 49          # the baseline never touches redo3
    shutil.rmtree(v1 / "redo3")
    assert len(M.load(v1, r2, through="redo2")["wordings"]) == 208
    with pytest.raises(FileNotFoundError):
        M.load(v1, r2)
    with pytest.raises(M.PoolError, match="through must be"):
        M.load(through="redo4")


def _add_of(pools_dir: Path) -> dict:
    return {n: json.loads((pools_dir / "redo3" / n).read_text(encoding="utf-8")) for n in M.REDO3_FILES}


def test_the_supplement_must_only_add(base):
    add = _add_of(M.V1)
    man = {"version": "r3"}
    ok = M.merge_redo3(base, add, man)
    assert len(ok["packs"]) == 66 and ok["manifests"]["redo3"] is man and len(base["packs"]) == 49    # base untouched
    bad = copy.deepcopy(add)
    bad["wordings_add.json"]["items"][0]["wording_id"] = base["wordings"][0]["wording_id"]
    with pytest.raises(M.PoolError, match="id repeats"):
        M.merge_redo3(base, bad, man)
    bad = copy.deepcopy(add)
    bad["wordings_add.json"]["items"][0]["text"] = base["wordings"][0]["text"].upper()
    with pytest.raises(M.PoolError, match="text repeats"):
        M.merge_redo3(base, bad, man)
    bad = copy.deepcopy(add)
    bad["packs_add.json"]["items"][1]["store"] = base["packs"][0]["store"].lower()
    with pytest.raises(M.PoolError, match="store name repeats"):
        M.merge_redo3(base, bad, man)
    bad = copy.deepcopy(add)
    bad["lexicon_add.json"]["forms"][0]["form_id"] = base["lexicon"][0]["form_id"]
    with pytest.raises(M.PoolError, match="id repeats"):
        M.merge_redo3(base, bad, man)


def test_pack_checks_read_the_pack_contents(pools):
    assert M.pack_problems(pools) == []
    new = [p for p in pools["packs"] if p["piece_id"].startswith("t07r3.")]
    assert len(new) == 17 and not any(p["held_out"] for p in new)
    bad = copy.deepcopy(pools)
    bad["packs"][-1]["regions"][0] = bad["packs"][0]["ladder"][0]                                  # an earlier pack's level as a region
    assert any("clash" in x for x in M.pack_problems(bad))
    bad = copy.deepcopy(pools)
    bad["packs"][-1]["customers"][0] = "Sung-min Park"                                                 # lint_pack accepts a hyphen, the brief did not
    bad["packs"][-1]["customers"][1] = "Catriona MacLeod"
    assert any("customers" in x for x in M.pack_problems(bad))
    bad = copy.deepcopy(pools)
    bad["packs"][-1]["store"] = bad["packs"][0]["store"]
    assert any("store_taken" in x or "repeats" in x for x in M.pack_problems(bad))
    # the direction check_packs does not look at: an EARLIER store name holds a surface of a redo3 pack
    bad = copy.deepcopy(pools)
    bad["packs"][-1]["ladder"][0] = bad["packs"][0]["store"].split()[0]
    assert any("whole word of the name" in x or "S2 uniqueness" in x for x in M.pack_problems(bad))
    bad = copy.deepcopy(pools)
    bad["packs"][-1]["customers"][0] = "Anna " + bad["packs"][-1]["ladder"][0]                        # its own name holds its own level
    assert M.pack_problems(bad)
    assert M.verdict(bad)["ready"] is False


def test_two_texts_for_one_brief_are_refused(tmp_path):
    v1, r2 = tmp_path / "pools", tmp_path / "pools" / "redo2"
    shutil.copytree(M.V1, v1)
    man_p = r2 / "MANIFEST.json"
    docs_p = r2 / "documents_add.json"
    docs = json.loads(docs_p.read_text(encoding="utf-8"))
    v1_docs = json.loads((v1 / "documents.json").read_text(encoding="utf-8"))["items"]
    docs["items"].append(dict(docs["items"][0], v1_brief=v1_docs[0]["internal_id"], doc_id="T07-dup"))
    docs_p.chmod(0o644)
    docs_p.write_text(json.dumps(docs, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    man = json.loads(man_p.read_text(encoding="utf-8"))
    man["pool_files"]["documents_add.json"]["sha256"] = _sha(docs_p)
    man_p.chmod(0o644)
    man_p.write_text(json.dumps(man), encoding="utf-8")
    with pytest.raises(M.PoolError, match="more than one Mode F text"):
        M.load(v1, r2)


def test_g0_pin_is_the_one_in_every_manifest(pools):
    sha = P.T07Plugin.G0_SHA256_AUTHORED
    assert pools["manifests"]["v1"]["g0_sha256"] == pools["manifests"]["redo2"]["g0_sha256"] == sha
    assert pools["manifests"]["redo3"]["g0_sha256"] == sha
