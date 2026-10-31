import json
import os
import re

import pytest

import split_aware_check as s

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REAL_REG = os.path.join(HERE, "..", "zed_orch", "c21", "l0", "G13_TARGET_REGISTRY_DRAFT.md")

MINI_REG = """# mini registry
## A. eval sets
| ID | Name |
|---|---|
| A1 | When2Call MCQ |
| A6 | ATBench |
## C. not reported
| ID | Name |
|---|---|
| C8 | TRACE |
| C13 | LibriSpeech test-clean and test-other |
## E. bars
| ID | Name |
|---|---|
| E16 | ToolACE |
| E45 | Jev (all reads) |
| E65 | gsm8k |
"""


@pytest.fixture
def reg(tmp_path):
    """Registry with only the ids in MINI_REG, mapped through the real key table."""
    p = tmp_path / "reg.md"
    p.write_text(MINI_REG)
    return s.load_registry(str(p))


def good(**kw):
    c = {"name": "acme-intents", "splits_available": ["train", "validation", "test"], "licence": "cc-by-4.0",
         "label_provenance": "human_crowd"}
    c.update(kw)
    return c


def codes(rec):
    return set(rec["reason_codes"])


# ----------------------------------------------------------------------------------------------------- allow
def test_clean_human_permissive_train_is_allowed(reg):
    r = s.evaluate(good(), reg)
    assert r["decision"] == "ALLOW" and r["deny_class"] is None and r["reasons"] == []
    assert r["allowed_splits"] == ["train"]
    assert "8.5" in r["allow_means"]


def test_allowed_splits_only_train_like_even_with_many(reg):
    r = s.evaluate(good(splits_available=["train_clean_100", "train-other-500", "dev", "test"]), reg)
    assert r["decision"] == "ALLOW" and r["allowed_splits"] == ["train_clean_100", "train-other-500"]


@pytest.mark.parametrize("lic", ["MIT", "Apache-2.0", "apache 2.0", "BSD-3-Clause", "CC0-1.0", "cc-by-4.0", "CC BY 4.0",
                                 "ODC-BY", "ISC", "unlicense", ["mit", "cc-by-4.0"],
                                 "cc-by-sa-4.0", "CC BY-SA 4.0", "CC BY-SA 3.0", "cc-by-sa", "CC-BY-SA-2.5",
                                 "CDLA-Permissive-2.0", "cdla-permissive-2.0", "CDLA Permissive 2.0",
                                 "ODC-By-1.0", "Open Data Commons Attribution License 1.0",
                                 "US public domain", "public domain (US)", "US Government work", "PDDL"])
def test_permissive_licences_pass(reg, lic):
    assert s.evaluate(good(licence=lic), reg)["decision"] == "ALLOW"


@pytest.mark.parametrize("prov", ["human", "human_expert", "crowdsourced by annotators", "expert annotated",
                                  "manually labelled by humans"])
def test_human_provenance_passes(reg, prov):
    assert s.evaluate(good(label_provenance=prov), reg)["decision"] == "ALLOW"


# ------------------------------------------------------------------------------------------------ A61(a) HITs
@pytest.mark.parametrize("nm", [
    "gsm8k", "openai/gsm8k", "GSM-8K", "gsm8k_main", "mgsm", "grade school math 8k",
    "hover", "di_hover", "hover_claim", "iSarcasmEval", "isarcasmeval", "SemEval-2022 Task 6", "di_isarcasmeval",
    "google/tydiqa", "TyDi QA", "tydiqa_goldp", "md_fdc", "FoodData Central", "md_peps", "PEPs list",
    "DI-TS", "di_ts_inputs", "md_worldbank", "World Bank indicators", "md_usgs", "USGS earthquakes",
    "md_cma", "Cleveland Museum of Art", "SB6", "SB-6", "sb_6"])
def test_a61a_hits_barred_under_any_id_or_form(reg, nm):
    r = s.evaluate(good(name=nm), reg)
    assert r["decision"] == "DENY" and r["deny_class"] == "BAR" and "A61A_HIT" in codes(r)


def test_a61a_hit_via_alias_and_hf_id(reg):
    assert "A61A_HIT" in codes(s.evaluate(good(name="mystery", aliases=["gsm8k"]), reg))
    assert "A61A_HIT" in codes(s.evaluate(good(name="mystery", hf_id="google/tydiqa"), reg))


def test_a61a_hit_via_upstream(reg):
    r = s.evaluate(good(derived_from=["openai/gsm8k"]), reg)
    assert "UPSTREAM_A61A_HIT" in codes(r) and r["decision"] == "DENY"


def test_every_task_named_a61a_source_has_a_key():
    for n in s.A61A_TASK_NAMES:
        assert n in s.A61A_HITS and s.A61A_HITS[n]
    assert set(s.A61A_TASK_NAMES) == {"gsm8k", "hover", "isarcasmeval", "tydiqa", "md_fdc", "md_peps", "di_ts_inputs",
                                      "md_worldbank", "md_usgs", "md_cma"}


def test_innocent_lookalikes_not_hit(reg):
    for nm in ["hovercraft-manuals", "steps-dataset", "acme-intents", "cmake-logs"]:
        assert "A61A_HIT" not in codes(s.evaluate(good(name=nm), reg)), nm


# ------------------------------------------------------------------------------------------- registry bars
@pytest.mark.parametrize("nm", ["When2Call", "ATBench-Codex", "ToolACE", "Jev", "jevbench"])
def test_registry_eval_targets_and_source_bars_denied(reg, nm):
    r = s.evaluate(good(name=nm), reg)
    assert r["decision"] == "DENY" and r["deny_class"] == "BAR"
    assert codes(r) & {"REGISTRY_EVAL_TARGET", "REGISTRY_SOURCE_BAR"}


def test_exact_name_keys_do_not_overmatch(reg):
    assert s.evaluate(good(name="TRACE"), reg)["decision"] == "DENY"
    assert s.evaluate(good(name="stack-trace-logs"), reg)["decision"] == "ALLOW"


def test_competitor_source_bar_also_flags_competitor_output(reg):
    assert "COMPETITOR_OUTPUT" in codes(s.evaluate(good(name="Jev"), reg))


def test_derived_from_barred_upstream(reg):
    r = s.evaluate(good(derived_from=["ToolACE"]), reg)
    assert "UPSTREAM_BARRED" in codes(r) and r["deny_class"] == "BAR"


def test_registry_eval_target_denied_even_with_perfect_metadata(reg):
    r = s.evaluate(good(name="ATBench"), reg)
    assert r["decision"] == "DENY"


def test_eval_target_split_declared(reg):
    r = s.evaluate(good(eval_target_splits=["test"]), reg)
    assert "EVAL_TARGET_SPLIT_DECLARED" in codes(r) and r["decision"] == "DENY"


# ---------------------------------------------------------------------------------- split-scoped registry
def test_split_scoped_entry_denied_in_default_strict_mode(reg):
    r = s.evaluate(good(name="LibriSpeech", splits_available=["train-clean-100", "test-clean"]), reg)
    assert r["decision"] == "DENY" and "REGISTRY_EVAL_TARGET_SPLIT_SCOPED" in codes(r)


def test_split_scoped_release_flag_without_evidence_still_denies(reg):
    """A82 1 / v3.2-r Sk 2: the flag alone releases nothing (the v1 code released on split names alone)."""
    c = good(name="LibriSpeech", splits_available=["train-clean-100", "test-clean", "test-other"],
             train_split_rows=28539)
    r = s.evaluate(c, reg, split_scoped_release=True)
    assert r["decision"] == "DENY" and "REGISTRY_EVAL_TARGET_SPLIT_SCOPED" in codes(r)
    assert "G13_EVIDENCE_MISSING" in codes(r) and r["deny_class"] == "BAR"  # the registry split-scope bar stays
    assert "train_split_seen" not in r


# ------------------------------------------------------------------------------------------------- splits
def test_requested_test_or_dev_split_denied(reg):
    for sp in ("test", "validation", "dev", "train_val", "heldout"):
        r = s.evaluate(good(splits_available=["train", sp], splits_requested=[sp]), reg)
        assert "REQUESTED_SPLIT_NOT_TRAIN" in codes(r) and r["decision"] == "DENY", sp


def test_no_train_split_denied(reg):
    r = s.evaluate(good(splits_available=["test", "validation"]), reg)
    assert "NO_TRAIN_SPLIT" in codes(r) and r["deny_class"] == "BAR"


def test_missing_split_info_is_insufficient_not_bar(reg):
    r = s.evaluate(good(splits_available=None), reg)
    assert r["decision"] == "DENY" and r["deny_class"] == "INSUFFICIENT_EVIDENCE" and "NO_SPLIT_INFO" in codes(r)


def test_requested_split_not_available(reg):
    r = s.evaluate(good(splits_requested=["train2"]), reg)
    assert "REQUESTED_SPLIT_NOT_AVAILABLE" in codes(r)


def test_split_class_table():
    assert s.split_class("train") == "train" and s.split_class("train[:80%]") == "train"
    assert s.split_class("train_clean_100") == "train"
    for n in ("test", "dev", "validation", "val", "eval", "test-clean", "train_val", "heldout", "devtest"):
        assert s.split_class(n) == "eval", n
    assert s.split_class("default") == "unknown" and s.split_class("all") == "unknown"


# ----------------------------------------------------------------------------------------------- licence
@pytest.mark.parametrize("lic,code", [
    ("cc-by-nc-4.0", "LICENCE_NOT_PERMISSIVE"), ("CC BY-NC-ND 4.0", "LICENCE_NOT_PERMISSIVE"),
    ("cc-by-nc-sa-4.0", "LICENCE_NOT_PERMISSIVE"), ("CC BY-ND 4.0", "LICENCE_NOT_PERMISSIVE"),
    ("cc-by-nc-nd-4.0", "LICENCE_NOT_PERMISSIVE"), ("CDLA-Sharing-1.0", "LICENCE_NOT_PERMISSIVE"),
    ("ODbL-1.0", "LICENCE_NOT_PERMISSIVE"), ("LGPL-2.1", "LICENCE_NOT_PERMISSIVE"), ("GPL-3.0", "LICENCE_NOT_PERMISSIVE"),
    ("AGPL-3.0", "LICENCE_NOT_PERMISSIVE"), ("MPL-2.0", "LICENCE_NOT_PERMISSIVE"),
    ("research purposes only", "LICENCE_NOT_PERMISSIVE"), ("non-commercial", "LICENCE_NOT_PERMISSIVE"),
    ("cc-by-4.0 / research purposes only", "LICENCE_NOT_PERMISSIVE"),
    ("none", "LICENCE_ABSENT"), ("not stated", "LICENCE_ABSENT"),
    ("unknown", "LICENCE_UNKNOWN"), ("mixed", "LICENCE_UNKNOWN"), ("other", "LICENCE_UNKNOWN"),
    ("weird-custom-thing-1.0", "LICENCE_NOT_PERMISSIVE"), ("foobar licence", "LICENCE_UNRECOGNISED"),
    (None, "LICENCE_UNKNOWN"), ([], "LICENCE_UNKNOWN"),
])
def test_licence_denials(reg, lic, code):
    r = s.evaluate(good(licence=lic), reg)
    assert r["decision"] == "DENY" and code in codes(r)


def test_licence_list_needs_all_to_pass(reg):
    assert s.evaluate(good(licence=["mit", "cc-by-nc-4.0"]), reg)["decision"] == "DENY"


def test_licence_unknown_is_insufficient_but_nc_is_bar(reg):
    assert s.evaluate(good(licence=None), reg)["deny_class"] == "INSUFFICIENT_EVIDENCE"
    assert s.evaluate(good(licence="cc-by-nc-4.0"), reg)["deny_class"] == "BAR"


# -------------------------------------------------------------------------------------------- provenance
@pytest.mark.parametrize("prov", ["llm_generated", "mixed_human_llm", "GPT-4 generated", "labelled by Claude",
                                  "synthetic", "human-verified LLM output", "distilled from Mixtral 8x22B",
                                  "generated by a language model", "ChatGPT annotations"])
def test_llm_label_provenance_denied(reg, prov):
    r = s.evaluate(good(label_provenance=prov), reg)
    assert "LABELS_LLM_GENERATED" in codes(r) and r["deny_class"] == "BAR"


@pytest.mark.parametrize("prov", ["program", "heuristic", "weak supervision", "distant supervision",
                                  "silver labels", "human annotated then rule-based relabelled",
                                  "model_labelled"])
def test_non_human_labels_denied(reg, prov):
    r = s.evaluate(good(label_provenance=prov), reg)
    assert "LABELS_NOT_HUMAN" in codes(r) and r["deny_class"] == "BAR"


@pytest.mark.parametrize("prov", [None, "unknown", "see paper", ""])
def test_unknown_label_provenance_is_insufficient(reg, prov):
    r = s.evaluate(good(label_provenance=prov), reg)
    assert "LABELS_UNKNOWN" in codes(r) and r["deny_class"] == "INSUFFICIENT_EVIDENCE"


def test_llm_generated_text_denied_even_with_human_labels(reg):
    r = s.evaluate(good(text_provenance="GPT-4o-mini written"), reg)
    assert "TEXT_LLM_GENERATED" in codes(r) and r["decision"] == "DENY"


def test_human_written_text_ok(reg):
    assert s.evaluate(good(text_provenance="human written"), reg)["decision"] == "ALLOW"


def test_jev_provenance_denied(reg):
    r = s.evaluate(good(label_provenance="human relabelled using Jev outputs"), reg)
    assert "COMPETITOR_OUTPUT" in codes(r) and r["decision"] == "DENY"


# ------------------------------------------------------------------------------------- split-aware denylist
def dl(*entries):
    return {"sha256": "0" * 64, "entries": list(entries)}


def test_split_blind_denylist_entry_denies(reg):
    d = dl({"name": "x", "keys": ["acme intents"], "tainted_splits": None, "ref": "DL-1"})
    r = s.evaluate(good(), reg, d)
    assert "DENYLIST_SPLIT_BLIND" in codes(r) and r["decision"] == "DENY"
    d2 = dl({"name": "x", "keys": ["acme intents"], "tainted_splits": ["*"]})
    assert "DENYLIST_SPLIT_BLIND" in codes(s.evaluate(good(), reg, d2))


def test_test_only_taint_alone_no_longer_releases_train_split(reg):
    """Skeptic S7: A82 1 needs the flag AND a G13 result record; a deny-list entry is a registered test/dev target."""
    d = dl({"name": "x", "keys": ["acme intents"], "tainted_splits": ["test", "validation"], "ref": "DL-2"})
    r = s.evaluate(good(), reg, d)
    assert r["decision"] == "DENY" and "DENYLIST_TEST_ONLY_SPLIT_SCOPED" in codes(r) and "train_split_seen" not in r
    r2 = s.evaluate(good(), reg, d, split_scoped_release=True)
    assert r2["decision"] == "DENY" and "G13_EVIDENCE_MISSING" in codes(r2)


def test_taint_on_train_split_denies(reg):
    d = dl({"name": "x", "keys": ["acme intents"], "tainted_splits": ["test", "train"]})
    assert "DENYLIST_TAINTED_TRAIN_SPLIT" in codes(s.evaluate(good(), reg, d))


def test_split_awareness_never_releases_an_a61a_hit(reg):
    d = dl({"name": "gsm8k", "keys": ["gsm8k"], "tainted_splits": ["test"]})
    r = s.evaluate(good(name="gsm8k", splits_available=["train", "test"]), reg, d)
    assert r["decision"] == "DENY" and "A61A_HIT" in codes(r)


def test_split_awareness_never_releases_a_registry_eval_target(reg):
    d = dl({"name": "a1", "keys": ["when2call"], "tainted_splits": ["test"]})
    assert s.evaluate(good(name="When2Call"), reg, d)["decision"] == "DENY"


def test_load_denylist_shape(tmp_path):
    p = tmp_path / "d.json"
    p.write_text(json.dumps({"a": 1}))
    with pytest.raises(ValueError):
        s.load_denylist(str(p))
    p.write_text(json.dumps([{"name": "x"}]))
    with pytest.raises(ValueError):
        s.load_denylist(str(p))
    p.write_text(json.dumps([{"name": "x", "keys": ["foo"], "tainted_splits": ["test"]}]))
    assert len(s.load_denylist(str(p))["entries"]) == 1


# ------------------------------------------------------------------------------------------------ catalogue
def test_catalogue_never_allowed_as_a_whole_and_members_get_records(reg):
    cat = {"name": "taskhub", "kind": "catalogue", "splits_available": ["train"], "licence": "mit",
           "label_provenance": "human",
           "members": [good(name="m1"), good(name="m2", licence="cc-by-nc-4.0"), {"name": "gsm8k"}]}
    r = s.evaluate(cat, reg)
    assert r["decision"] == "DENY" and r["deny_class"] == "INSUFFICIENT_EVIDENCE"
    assert [m["decision"] for m in r["members"]] == ["ALLOW", "DENY", "DENY"]
    assert "A61A_HIT" in codes(r["members"][2])


def test_catalogue_with_no_members_denied(reg):
    r = s.evaluate({"name": "taskhub", "kind": "catalogue"}, reg)
    assert r["decision"] == "DENY" and "CATALOGUE_PER_MEMBER_REQUIRED" in codes(r)


# ------------------------------------------------------------------------------------------ name matching
@pytest.mark.parametrize("key,name,want", [
    ("hover", "hovercraft", False), ("hover", "di_hover", True), ("gsm8k", "GSM-8K", True),
    ("gsm8k", "openai/gsm8k", True), ("peps", "steps", False), ("=trace", "TRACE", True),
    ("=trace", "stack trace", False), ("atbench", "ATBench-Codex", True), ("swe bench", "SWE-bench_Verified", True),
    ("swe bench", "swe-gym", False), ("tydiqa", "tydi_qa", True), ("jev", "jevons", False),
])
def test_match_key(key, name, want):
    assert s.match_key(key, s._name_forms([name])) is want


# ------------------------------------------------------------------------------------------------- registry
@pytest.mark.skipif(not os.path.isfile(REAL_REG), reason="registry draft not present")
def test_real_registry_fully_mapped_and_counts():
    R = s.load_registry(REAL_REG)
    assert R["unmapped"] == []
    by = {}
    for e in R["entries"].values():
        by[e["section"]] = by.get(e["section"], 0) + 1
    assert by == {"A": 6, "B": 13, "C": 13, "D": 33, "E": 74, "M": 4}
    assert set(s.REGISTRY_KEYS) == set(R["entries"])
    # E65-E71 names in the registry are all on the A61(a) key table
    for rid in ["E%d" % i for i in range(65, 72)]:
        nm = R["entries"][rid]["name"]
        hit = s._a61a_matches(s._name_forms([nm]))
        assert hit, (rid, nm)


@pytest.mark.skipif(not os.path.isfile(REAL_REG), reason="registry draft not present")
def test_real_registry_known_cases():
    R = s.load_registry(REAL_REG)
    assert s.evaluate(good(name="allenai/wildguardmix"), R)["decision"] == "DENY"
    assert s.evaluate(good(name="openai_humaneval"), R)["decision"] == "DENY"
    assert s.evaluate(good(name="SWE-bench_Verified"), R)["decision"] == "DENY"
    assert s.evaluate(good(name="acme-intents"), R)["decision"] == "ALLOW"


def test_unmapped_registry_id_refuses_run(tmp_path):
    p = tmp_path / "reg.md"
    p.write_text(MINI_REG + "\n| E99 | Brand New Bar |\n")
    R = s.load_registry(str(p))
    assert R["unmapped"] == ["E99"]
    with pytest.raises(ValueError, match="REGISTRY_UNMAPPED_ID"):
        s.evaluate_all([good()], R)


def test_registry_duplicate_id_refused(tmp_path):
    p = tmp_path / "reg.md"
    p.write_text(MINI_REG + "\n| E16 | ToolACE again |\n")
    with pytest.raises(ValueError, match="REGISTRY_DUPLICATE_ID"):
        s.load_registry(str(p))


def test_registry_path_with_sealed_component_refused(tmp_path):
    d = tmp_path / "sealed_x"
    d.mkdir()
    (d / "reg.md").write_text(MINI_REG)
    with pytest.raises(ValueError, match="REGISTRY_PATH_BARRED"):
        s.load_registry(str(d / "reg.md"))


# --------------------------------------------------------------------------------------------- manifest
def _manifest(tmp_path):
    m = {"frozen": True, "version": 2, "r5_candidate_datasets": {
        "candidates": [
            {"name": "tasksource", "kind": "task catalogue (1,100+ tasks)", "use": "TRAIN-split subset only", "status": "candidate_pending"},
            {"name": "Decision Index public index sources, TRAIN splits only", "kind": "group (37 public benchmarks)", "status": "group_names_pending"}],
        "excluded_even_if_R5_adopted": {"names": ["gsm8k (DI-KR train split)", "hover (di_hover)", "SB6"]}}}
    p = tmp_path / "m.json"
    p.write_text(json.dumps(m))
    return str(p)


def test_r5_adapter_and_cli_end_to_end(tmp_path, capsys):
    mp = _manifest(tmp_path)
    rp = tmp_path / "reg.md"
    rp.write_text(MINI_REG)
    out = tmp_path / "out.json"
    rc = s.main(["--registry", str(rp), "--r5-manifest", mp, "--a61a-sentinels", "--out", str(out)])
    assert rc == 0
    res = json.load(open(out))
    names = [r["name"] for r in res["records"]]
    assert names[:2] == ["tasksource", "Decision Index public index sources, TRAIN splits only"]
    assert res["counts"]["ALLOW"] == 0 and res["counts"]["DENY"] == res["counts"]["total"]
    by = {r["name"]: r for r in res["records"]}
    assert by["tasksource"]["deny_class"] == "INSUFFICIENT_EVIDENCE"
    assert "CATALOGUE_PER_MEMBER_REQUIRED" in by["tasksource"]["reason_codes"]
    assert by["gsm8k (DI-KR train split)"]["deny_class"] == "BAR"
    # sentinels exist only for A61(a) names the manifest list does not already cover
    assert {"md_fdc", "md_peps", "md_worldbank", "md_usgs", "md_cma", "isarcasmeval", "tydiqa", "di_ts_inputs"} <= set(names)
    assert "gsm8k" not in names and "hover" not in names
    assert res["registry_sha256"] == s.sha256_file(str(rp))
    assert "tool_sha256" in res and res["inputs"]["manifest_frozen"] is True
    md = s.render_markdown(res)
    assert "tasksource" in md and "ALLOW" not in md.split("###")[0].split("\n", 2)[2]


def test_cli_refuses_barred_paths(tmp_path, capsys):
    d = tmp_path / "ohs_stuff"
    d.mkdir()
    rp = tmp_path / "reg.md"
    rp.write_text(MINI_REG)
    cp = d / "c.json"
    cp.write_text("[]")
    assert s.main(["--registry", str(rp), "--candidates", str(cp), "--out", str(tmp_path / "o.json")]) == 2
    assert s.main(["--registry", str(rp), "--candidates", str(tmp_path / "c.json"), "--out", str(d / "o.json")]) == 2
    assert not (d / "o.json").exists()


def test_cli_candidates_file_and_exit_code_for_unmapped(tmp_path):
    rp = tmp_path / "reg.md"
    rp.write_text(MINI_REG + "\n| E99 | New |\n")
    cp = tmp_path / "c.json"
    cp.write_text(json.dumps([good()]))
    assert s.main(["--registry", str(rp), "--candidates", str(cp), "--out", str(tmp_path / "o.json")]) == 2
    rp.write_text(MINI_REG)
    assert s.main(["--registry", str(rp), "--candidates", str(cp), "--out", str(tmp_path / "o.json")]) == 0
    res = json.load(open(tmp_path / "o.json"))
    assert res["counts"]["ALLOW"] == 1


def test_manifest_without_r5_block_refused(tmp_path):
    p = tmp_path / "m.json"
    p.write_text(json.dumps({"frozen": True}))
    with pytest.raises(ValueError, match="MANIFEST_NO_R5"):
        s.r5_candidates_from_manifest(str(p))


# --------------------------------------------------------------------------------------------- static rules
FORBIDDEN = re.compile(r"\b(glob\.glob|glob\.iglob|\.rglob\(|\.glob\(|\.iterdir\(|os\.listdir|os\.scandir|os\.walk|os\.fwalk|fnmatch|"
                       r"subprocess|os\.system|os\.popen|shutil\.copytree|requests|urllib|socket|http\.client)")


def test_tool_walks_nothing_and_calls_no_network_or_subprocess():
    src = open(os.path.join(HERE, "split_aware_check.py")).read()
    assert not FORBIDDEN.search(src)
    assert "is_skipped_path" in src


def test_tool_never_mentions_data_ohs3_globs():
    src = open(os.path.join(HERE, "split_aware_check.py")).read()
    assert "data/**" not in src


# ====================================================================================================================
# v2 (18 Oct): ruling-to-code conformance tests (plan 16.1 step 0; v3.2-r Sk 1, 2, 24; A82 1, 2, 7)
# ====================================================================================================================
import hashlib  # noqa: E402

DI_TS_MEMBER_NAMES = ["CogComp/perspectrum", "google-deepmind/logical-entailment-dataset",
                      "kunalkukreja21/temporal-expressions-evaluation-lm"]
DI_TS_ALIASES = ["perspectrum", "PERSPECTRUM", "cogcomp_perspectrum", "CogComp perspectrum",
                 "logical-entailment-dataset", "logical_entailment_dataset", "Logical Entailment Dataset",
                 "deepmind/logical-entailment-dataset", "google-deepmind/logical-entailment",
                 "temporal-expressions-evaluation-lm", "temporal_expressions_evaluation_lm",
                 "Temporal Expressions Evaluation", "kunalkukreja21", "kunalkukreja21/temporal-expressions-evaluation"]


# ----------------------------------------------------------------------- Sk 1: DI-TS members and A61(a) HITs
@pytest.mark.parametrize("nm", DI_TS_MEMBER_NAMES + DI_TS_ALIASES)
def test_di_ts_members_barred_by_name_and_alias(reg, nm):
    r = s.evaluate(good(name=nm), reg)
    assert r["decision"] == "DENY" and r["deny_class"] == "BAR" and "A61A_HIT" in codes(r)


@pytest.mark.parametrize("nm", DI_TS_MEMBER_NAMES)
def test_di_ts_members_barred_via_hf_id_alias_upstream(reg, nm):
    assert "A61A_HIT" in codes(s.evaluate(good(name="mystery-set", hf_id=nm), reg))
    assert "A61A_HIT" in codes(s.evaluate(good(name="mystery-set", aliases=[nm]), reg))
    r = s.evaluate(good(name="mystery-set", derived_from=[nm]), reg)
    assert "UPSTREAM_A61A_HIT" in codes(r) and r["deny_class"] == "BAR"


def test_skeptic_scenario_perspectrum_cc_by_sa_is_denied_not_allowed(reg):
    """The skeptic's case: once CC BY-SA is allowed (A82 2) a CC BY-SA perspectrum must still be DENY (A61(a) HIT)."""
    r = s.evaluate(good(name="CogComp/perspectrum", licence="cc-by-sa-4.0", label_provenance="human_crowd",
                        splits_available=["train", "dev", "test"]), reg)
    assert r["decision"] == "DENY" and r["deny_class"] == "BAR" and "A61A_HIT" in codes(r)
    assert "LICENCE_NOT_PERMISSIVE" not in codes(r)


@pytest.mark.parametrize("nm", ["perspectrum", "logical-entailment-dataset", "temporal-expressions-evaluation-lm", "sb6", "gsm8k"])
def test_a61a_hit_never_released_even_with_flag_and_full_evidence(reg, tmp_path, nm):
    c = good(name=nm, splits_available=["train", "test"], train_split_rows=100)
    c["g13_record"] = write_g13(tmp_path, reg, dataset=nm, rows=100)
    r = s.evaluate(c, reg, split_scoped_release=True)
    assert r["decision"] == "DENY" and "A61A_HIT" in codes(r) and "train_split_seen" not in r


def test_di_ts_members_are_in_a61a_table_and_e71_keys():
    for m in s.DI_TS_MEMBERS:
        assert s.A61A_HITS[m]
    for nm in DI_TS_MEMBER_NAMES:
        assert s._a61a_matches(s._name_forms([nm]))
        assert any(s.match_any(s.REGISTRY_KEYS["E71"], s._name_forms([nm])) for _ in [0])
    # the ten task names and SB6 are still all present
    assert set(s.A61A_TASK_NAMES) <= set(s.A61A_HITS) and "sb6" in s.A61A_HITS


def test_every_a61a_key_denies_through_name_hf_id_and_upstream(reg):
    for hit, keys in s.A61A_HITS.items():
        for k in keys:
            assert hit in s._a61a_matches(s._name_forms([k])), (hit, k)
            assert "A61A_HIT" in codes(s.evaluate(good(name="x-set", hf_id="org/" + k.replace(" ", "-")), reg)), (hit, k)
            assert "UPSTREAM_A61A_HIT" in codes(s.evaluate(good(name="x-set", derived_from=[k]), reg)), (hit, k)


def test_sentinels_cover_di_ts_members_and_sb6_when_manifest_lacks_them():
    sent = s.a61a_sentinels([{"name": "gsm8k"}])
    names = {x["name"] for x in sent}
    assert set(DI_TS_MEMBER_NAMES) <= names and "sb6" in names and "gsm8k" not in names
    sent2 = s.a61a_sentinels([{"name": "SB6"}, {"name": "CogComp/perspectrum"}])
    assert "sb6" not in {x["name"] for x in sent2} and "CogComp/perspectrum" not in {x["name"] for x in sent2}


def test_denylist_taint_on_di_ts_member_test_split_does_not_release(reg):
    dl = {"entries": [{"keys": ["perspectrum"], "tainted_splits": ["test"], "ref": "dl1"}]}
    r = s.evaluate(good(name="perspectrum"), reg, dl)
    assert r["decision"] == "DENY" and "A61A_HIT" in codes(r)


# ------------------------------------------------------------------------------------ A82 2, A82 7: licences
@pytest.mark.parametrize("lic", ["cc-by-sa-4.0", "CC BY-SA 4.0", "CC BY-SA 3.0", "cc-by-sa-2.0", "CC-BY-SA"])
def test_cc_by_sa_allowed_with_share_alike_disclosure(reg, lic):
    r = s.evaluate(good(licence=lic), reg)
    assert r["decision"] == "ALLOW" and r["share_alike_disclosure"] is True
    assert any("SHARE_ALIKE" in n for n in r["notes"])


def test_permissive_licence_has_no_share_alike_flag(reg):
    r = s.evaluate(good(licence="cc-by-4.0"), reg)
    assert r["decision"] == "ALLOW" and "share_alike_disclosure" not in r
    assert "share_alike_disclosure" not in s.evaluate(good(licence="MIT"), reg)


def test_list_with_cc_by_sa_and_mit_allowed_and_flagged(reg):
    r = s.evaluate(good(licence=["mit", "CC BY-SA 4.0"]), reg)
    assert r["decision"] == "ALLOW" and r["share_alike_disclosure"] is True


@pytest.mark.parametrize("lic", ["CDLA-Permissive-2.0", "cdla-permissive-2.0", "CDLA Permissive 2.0"])
def test_cdla_permissive_2_allowed(reg, lic):
    assert s.evaluate(good(licence=lic), reg)["decision"] == "ALLOW"


@pytest.mark.parametrize("lic", ["ODC-By", "ODC-By-1.0", "US public domain", "public domain (US)", "US Government work"])
def test_odc_by_and_us_public_domain_allowed(reg, lic):
    assert s.evaluate(good(licence=lic), reg)["decision"] == "ALLOW"


@pytest.mark.parametrize("lic", [
    "cc-by-nc-4.0", "CC BY-NC 4.0", "cc-by-nc-sa-4.0", "CC BY-NC-SA 3.0", "cc-by-nc-nd-4.0", "cc-by-nd-4.0",
    "CC BY-ND", "non-commercial use only", "no derivatives", "GPL-2.0", "GPL-3.0", "LGPL-3.0", "AGPL-3.0",
    "GPL-3.0-or-later", "mit / gpl-3.0 dual", ["cc-by-sa-4.0", "cc-by-nc-4.0"], ["mit", "GPL-3.0"],
    "CDLA-Sharing-1.0", "ODbL-1.0"])
def test_nc_nd_gpl_never_allowed(reg, lic):
    r = s.evaluate(good(licence=lic), reg)
    assert r["decision"] == "DENY" and r["deny_class"] == "BAR" and "LICENCE_NOT_PERMISSIVE" in codes(r)
    assert "share_alike_disclosure" not in r or r["decision"] == "DENY"


def test_nc_never_released_by_split_scoped_release_either(reg, tmp_path):
    c = good(name="LibriSpeech", licence="cc-by-nc-sa-4.0", splits_available=["train-clean-100", "test-clean"],
             train_split_rows=100)
    c["g13_record"] = write_g13(tmp_path, reg, dataset="LibriSpeech", rows=100, split="train-clean-100")
    r = s.evaluate(c, reg, split_scoped_release=True)
    assert r["decision"] == "DENY" and "LICENCE_NOT_PERMISSIVE" in codes(r) and "train_split_seen" not in r


# ------------------------------------------------------------------- Sk 2: split-scoped release needs evidence
def write_g13(tmp_path, registry, dataset="LibriSpeech", split="train-clean-100", rows=28539, **over):
    """Write a G13 result record; returns the {path, sha256} reference. `over` overrides top-level fields; a key
    'split_<field>' overrides a field of the split entry."""
    ent = {"rows_in_split": rows, "rows_checked": rows, "sampled": False, "row_cap": None, "hits": 0,
           "hits_outside_r6_scaffolding": 0}
    rec = {"kind": "g13_result_record", "dataset": dataset, "registry_sha256": registry["sha256"],
           "method_set_version": "ms-1", "registry_entries": len(registry["entries"]), "targets_all_registered": True,
           "complete": True, "rows_dropped_for_disjointness": 0, "splits": {split: ent}}
    for k, v in over.items():
        if k.startswith("split_"):
            ent[k[len("split_"):]] = v
        elif k == "rows":
            continue
        else:
            rec[k] = v
    n = len(list(tmp_path.glob("g13_*.json")))
    p = tmp_path / ("g13_%d.json" % n)
    p.write_text(json.dumps({k: v for k, v in rec.items() if v != "__DEL__"}))
    return {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}


def libri(tmp_path, reg, **over):
    c = good(name="LibriSpeech", splits_available=["train-clean-100", "test-clean", "test-other"], train_split_rows=28539)
    c["g13_record"] = write_g13(tmp_path, reg, **over)
    return c


def test_release_with_complete_full_split_evidence(reg, tmp_path):
    r = s.evaluate(libri(tmp_path, reg), reg, split_scoped_release=True)
    assert r["decision"] == "ALLOW" and r["allowed_splits"] == ["train-clean-100"]
    assert r["train_split_seen"] is True
    ev = r["g13_evidence"]
    assert ev["registry_sha256"] == reg["sha256"] and ev["method_set_version"] == "ms-1"
    assert ev["splits"]["train-clean-100"]["rows_checked"] == 28539 == ev["splits"]["train-clean-100"]["rows_in_split"]
    assert len(ev["sha256"]) == 64 and any("FULL train split" in n for n in r["notes"])


def test_no_flag_means_no_release_even_with_perfect_evidence(reg, tmp_path):
    r = s.evaluate(libri(tmp_path, reg), reg)
    assert r["decision"] == "DENY" and "REGISTRY_EVAL_TARGET_SPLIT_SCOPED" in codes(r) and "train_split_seen" not in r


def test_released_record_with_share_alike_carries_both_flags(reg, tmp_path):
    c = libri(tmp_path, reg)
    c["licence"] = "cc-by-sa-4.0"
    r = s.evaluate(c, reg, split_scoped_release=True)
    assert r["decision"] == "ALLOW" and r["train_split_seen"] is True and r["share_alike_disclosure"] is True


def test_condition_evidence_absent(reg):
    c = good(name="LibriSpeech", splits_available=["train-clean-100", "test-clean"], train_split_rows=10)
    r = s.evaluate(c, reg, split_scoped_release=True)
    assert r["decision"] == "DENY" and "G13_EVIDENCE_MISSING" in codes(r)


def test_condition_evidence_sha_mismatch(reg, tmp_path):
    c = libri(tmp_path, reg)
    c["g13_record"]["sha256"] = "0" * 64
    r = s.evaluate(c, reg, split_scoped_release=True)
    assert r["decision"] == "DENY" and "G13_EVIDENCE_INVALID" in codes(r)
    assert any("sha256 mismatch" in x["detail"] for x in r["reasons"])


def test_condition_evidence_file_edited_after_sha_taken(reg, tmp_path):
    c = libri(tmp_path, reg)
    pth = c["g13_record"]["path"]
    d = json.load(open(pth))
    d["method_set_version"] = "ms-2"
    open(pth, "w").write(json.dumps(d))
    r = s.evaluate(c, reg, split_scoped_release=True)
    assert r["decision"] == "DENY" and any("sha256 mismatch" in x["detail"] for x in r["reasons"])


@pytest.mark.parametrize("ref", [{"path": "x"}, {"sha256": "a" * 64}, {"path": "", "sha256": "a" * 64},
                                 {"path": "x", "sha256": "xyz"}, "just-a-string", 5])
def test_condition_evidence_reference_shape(reg, ref):
    c = good(name="LibriSpeech", splits_available=["train-clean-100", "test-clean"], train_split_rows=10, g13_record=ref)
    r = s.evaluate(c, reg, split_scoped_release=True)
    assert r["decision"] == "DENY" and "G13_EVIDENCE_INVALID" in codes(r)


def test_condition_evidence_file_missing(reg, tmp_path):
    c = good(name="LibriSpeech", splits_available=["train-clean-100", "test-clean"], train_split_rows=10,
             g13_record={"path": str(tmp_path / "nope.json"), "sha256": "a" * 64})
    r = s.evaluate(c, reg, split_scoped_release=True)
    assert r["decision"] == "DENY" and "G13_EVIDENCE_INVALID" in codes(r)


def test_condition_evidence_not_json_or_not_object(reg, tmp_path):
    for body in (b"not json", b"[1,2]"):
        p = tmp_path / "bad.json"
        p.write_bytes(body)
        c = good(name="LibriSpeech", splits_available=["train-clean-100", "test-clean"], train_split_rows=10,
                 g13_record={"path": str(p), "sha256": hashlib.sha256(body).hexdigest()})
        assert "G13_EVIDENCE_INVALID" in codes(s.evaluate(c, reg, split_scoped_release=True))


def test_condition_evidence_path_with_sealed_component_never_opened(reg, tmp_path):
    d = tmp_path / "sealed_records"
    d.mkdir()
    ref = write_g13(d, reg)
    c = good(name="LibriSpeech", splits_available=["train-clean-100", "test-clean"], train_split_rows=28539, g13_record=ref)
    r = s.evaluate(c, reg, split_scoped_release=True)
    assert r["decision"] == "DENY" and any("never opened" in x["detail"] for x in r["reasons"])


def test_condition_evidence_stale_registry_sha(reg, tmp_path):
    r = s.evaluate(libri(tmp_path, reg, registry_sha256="f" * 64), reg, split_scoped_release=True)
    assert r["decision"] == "DENY" and any("stale" in x["detail"] for x in r["reasons"])


def test_condition_evidence_registry_entry_count_must_match(reg, tmp_path):
    r = s.evaluate(libri(tmp_path, reg, registry_entries=len(reg["entries"]) - 1), reg, split_scoped_release=True)
    assert r["decision"] == "DENY" and "G13_EVIDENCE_INVALID" in codes(r)


@pytest.mark.parametrize("field,val", [("targets_all_registered", False), ("complete", False),
                                       ("method_set_version", ""), ("method_set_version", 3),
                                       ("rows_dropped_for_disjointness", 5), ("kind", "g13_stamp"),
                                       ("dataset", "SomeOtherDataset")])
def test_condition_evidence_top_level_fields_strict(reg, tmp_path, field, val):
    r = s.evaluate(libri(tmp_path, reg, **{field: val}), reg, split_scoped_release=True)
    assert r["decision"] == "DENY" and "G13_EVIDENCE_INVALID" in codes(r) and "train_split_seen" not in r


def test_condition_whole_split_not_a_subset(reg, tmp_path):
    """v3.2-r Sk 3: the FULL train split, never the capped 1,200 rows."""
    c = libri(tmp_path, reg, split_rows_checked=1200)
    r = s.evaluate(c, reg, split_scoped_release=True)
    assert r["decision"] == "DENY" and any("whole split" in x["detail"] for x in r["reasons"])


def test_condition_self_consistent_capped_record_fails_against_declared_size(reg, tmp_path):
    c = libri(tmp_path, reg, rows=1200, split_rows_in_split=1200, split_rows_checked=1200)
    assert c["train_split_rows"] == 28539
    r = s.evaluate(c, reg, split_scoped_release=True)
    assert r["decision"] == "DENY" and any("declared full train split" in x["detail"] for x in r["reasons"])


def test_condition_declared_full_size_required(reg, tmp_path):
    c = libri(tmp_path, reg)
    del c["train_split_rows"]
    r = s.evaluate(c, reg, split_scoped_release=True)
    assert r["decision"] == "DENY" and any("train_split_rows" in x["detail"] for x in r["reasons"])


@pytest.mark.parametrize("field,val", [("sampled", True), ("row_cap", 1200), ("rows_in_split", 0), ("rows_checked", "28539"),
                                       ("hits", None), ("hits_outside_r6_scaffolding", None)])
def test_condition_split_entry_fields_strict(reg, tmp_path, field, val):
    r = s.evaluate(libri(tmp_path, reg, **{"split_" + field: val}), reg, split_scoped_release=True)
    assert r["decision"] == "DENY" and "train_split_seen" not in r


def test_condition_hits_outside_scaffolding_is_a_bar(reg, tmp_path):
    r = s.evaluate(libri(tmp_path, reg, split_hits=3, split_hits_outside_r6_scaffolding=2), reg, split_scoped_release=True)
    assert r["decision"] == "DENY" and r["deny_class"] == "BAR" and "G13_HITS_OUTSIDE_SCAFFOLDING" in codes(r)
    assert "train_split_seen" not in r


def test_condition_r6_scaffolding_hits_alone_do_not_block(reg, tmp_path):
    r = s.evaluate(libri(tmp_path, reg, split_hits=40, split_hits_outside_r6_scaffolding=0), reg, split_scoped_release=True)
    assert r["decision"] == "ALLOW" and r["train_split_seen"] is True
    assert r["g13_evidence"]["splits"]["train-clean-100"]["hits"] == 40


def test_condition_outside_hits_cannot_exceed_hits(reg, tmp_path):
    r = s.evaluate(libri(tmp_path, reg, split_hits=0, split_hits_outside_r6_scaffolding=1), reg, split_scoped_release=True)
    assert r["decision"] == "DENY"


def test_condition_every_requested_split_needs_evidence(reg, tmp_path):
    c = good(name="LibriSpeech", splits_available=["train-clean-100", "train-other-500", "test-clean"],
             train_split_rows={"train-clean-100": 28539, "train-other-500": 148688})
    c["g13_record"] = write_g13(tmp_path, reg)  # covers only train-clean-100
    r = s.evaluate(c, reg, split_scoped_release=True)
    assert r["decision"] == "DENY" and any("not covered" in x["detail"] for x in r["reasons"])


def test_two_train_splits_released_with_per_split_sizes(reg, tmp_path):
    c = good(name="LibriSpeech", splits_available=["train-clean-100", "train-other-500", "test-clean"],
             train_split_rows={"train-clean-100": 28539, "train-other-500": 148688})
    ref = write_g13(tmp_path, reg)
    d = json.load(open(ref["path"]))
    d["splits"]["train-other-500"] = dict(d["splits"]["train-clean-100"], rows_in_split=148688, rows_checked=148688)
    open(ref["path"], "w").write(json.dumps(d))
    c["g13_record"] = {"path": ref["path"], "sha256": hashlib.sha256(open(ref["path"], "rb").read()).hexdigest()}
    r = s.evaluate(c, reg, split_scoped_release=True)
    assert r["decision"] == "ALLOW" and set(r["allowed_splits"]) == {"train-clean-100", "train-other-500"}
    assert r["train_split_seen"] is True


def test_scalar_train_split_rows_not_accepted_for_two_splits(reg, tmp_path):
    c = good(name="LibriSpeech", splits_available=["train-clean-100", "train-other-500", "test-clean"], train_split_rows=28539)
    c["g13_record"] = write_g13(tmp_path, reg)
    assert s.evaluate(c, reg, split_scoped_release=True)["decision"] == "DENY"


def test_condition_requested_split_intersecting_scope_not_released_even_with_evidence(reg, tmp_path):
    c = libri(tmp_path, reg)
    c["splits_requested"] = ["train-clean-100", "test-clean"]
    r = s.evaluate(c, reg, split_scoped_release=True)
    assert r["decision"] == "DENY" and "REQUESTED_SPLIT_NOT_TRAIN" in codes(r) and "train_split_seen" not in r


def test_evidence_not_read_when_release_flag_off_or_dataset_not_scoped(reg, tmp_path):
    """A candidate with no split-scoped registry entry never reads its g13_record and gets no train_split_seen."""
    c = good(g13_record={"path": str(tmp_path / "never.json"), "sha256": "a" * 64})
    r = s.evaluate(c, reg, split_scoped_release=True)
    assert r["decision"] == "ALLOW" and "train_split_seen" not in r and "g13_evidence" not in r


def test_released_catalogue_member_gets_its_own_evidence(reg, tmp_path):
    cat = {"name": "multi-asr", "kind": "catalogue", "members": [libri(tmp_path, reg)]}
    r = s.evaluate(cat, reg, split_scoped_release=True)
    assert r["decision"] == "DENY" and "CATALOGUE_PER_MEMBER_REQUIRED" in codes(r)
    assert r["members"][0]["decision"] == "ALLOW" and r["members"][0]["train_split_seen"] is True


def test_cli_split_scoped_release_end_to_end_writes_train_split_seen(tmp_path, capsys):
    rp = tmp_path / "reg.md"
    rp.write_text(MINI_REG)
    regd = s.load_registry(str(rp))
    cp = tmp_path / "cands.json"
    ok = libri(tmp_path, regd)
    no_ev = good(name="LibriSpeech-2", aliases=["librispeech"], splits_available=["train-clean-100", "test-clean"], train_split_rows=5)
    cp.write_text(json.dumps([ok, no_ev]))
    out = tmp_path / "out.json"
    assert s.main(["--registry", str(rp), "--candidates", str(cp), "--split-scoped-release", "--out", str(out)]) == 0
    res = json.load(open(out))
    assert res["split_scoped_release"] is True
    assert res["records"][0]["decision"] == "ALLOW" and res["records"][0]["train_split_seen"] is True
    assert res["records"][1]["decision"] == "DENY" and "G13_EVIDENCE_MISSING" in res["records"][1]["reason_codes"]
    out2 = tmp_path / "out2.json"
    assert s.main(["--registry", str(rp), "--candidates", str(cp), "--out", str(out2)]) == 0
    assert all(r["decision"] == "DENY" for r in json.load(open(out2))["records"])


def test_tool_docstring_no_longer_says_g13_pilot_and_version_bumped():
    src = open(os.path.join(HERE, "split_aware_check.py")).read()
    assert "G13 pilot" not in src and "200-row" not in src
    assert s.TOOL_VERSION.startswith("split_aware_check v2")


# =============================================================== skeptic round (fresh Sonnet) S1-S14
def _ev_good(tmp_path, reg, name="acme-intents", rows=1000):
    return good(name=name, train_split_rows=rows,
                g13_record=write_g13(tmp_path, reg, dataset=name, split="train", rows=rows))


def test_s7_test_only_taint_releases_with_flag_and_full_evidence(reg, tmp_path):
    d = dl({"name": "x", "keys": ["acme intents"], "tainted_splits": ["test", "validation"], "ref": "DL-2"})
    r = s.evaluate(_ev_good(tmp_path, reg), reg, d, split_scoped_release=True)
    assert r["decision"] == "ALLOW" and r["train_split_seen"] is True and any("SPLIT_AWARE_RELEASE" in n for n in r["notes"])
    assert r["g13_evidence"]["splits"]["train"]["rows_checked"] == 1000


def test_s7_test_only_taint_with_capped_record_still_denied(reg, tmp_path):
    d = dl({"name": "x", "keys": ["acme intents"], "tainted_splits": ["test"]})
    c = good(train_split_rows=5000, g13_record=write_g13(tmp_path, reg, dataset="acme-intents", split="train", rows=1200))
    r = s.evaluate(c, reg, d, split_scoped_release=True)
    assert r["decision"] == "DENY" and "train_split_seen" not in r


def test_s7_test_only_taint_cannot_release_requested_taint_split(reg, tmp_path):
    d = dl({"name": "x", "keys": ["acme intents"], "tainted_splits": ["test", "train"]})
    assert "DENYLIST_TAINTED_TRAIN_SPLIT" in codes(s.evaluate(_ev_good(tmp_path, reg), reg, d, split_scoped_release=True))


# ---- S1: wrong-typed identity fields must not drop out of the bar checks
@pytest.mark.parametrize("field,val,want", [
    ("aliases", "CogComp/perspectrum", "A61A_HIT"),
    ("aliases", ["ok", {"name": "gsm8k"}], "CANDIDATE_MALFORMED"),
    ("hf_id", ["CogComp/perspectrum"], "CANDIDATE_MALFORMED"),
    ("hf_id", {"id": "CogComp/perspectrum"}, "CANDIDATE_MALFORMED"),
    ("derived_from", "gsm8k", "UPSTREAM_A61A_HIT"),
    ("derived_from", [{"name": "CogComp/perspectrum"}], "UPSTREAM_A61A_HIT"),
    ("derived_from", [{"hf_id": "gsm8k"}], "UPSTREAM_A61A_HIT"),
    ("derived_from", [["gsm8k"]], "CANDIDATE_MALFORMED"),
    ("derived_from", [5], "CANDIDATE_MALFORMED"),
    ("derived_from", 7, "CANDIDATE_MALFORMED"),
])
def test_s1_type_confusion_is_denied(reg, field, val, want):
    r = s.evaluate(good(**{field: val}), reg)
    assert r["decision"] == "DENY" and want in codes(r)


def test_s1_name_must_be_a_string(reg):
    r = s.evaluate(good(name=["CogComp/perspectrum"], hf_id="ok-ds"), reg)
    assert r["decision"] == "DENY" and "CANDIDATE_MALFORMED" in codes(r)
    assert s.evaluate({"hf_id": "ok-ds", "splits_available": ["train"], "licence": "mit", "label_provenance": "human"},
                      reg)["decision"] == "DENY"


@pytest.mark.parametrize("bad", [None, "perspectrum", 5, ["x"]])
def test_s1_non_object_candidate_is_denied_not_a_crash(reg, bad):
    r = s.evaluate(bad, reg)
    assert r["decision"] == "DENY" and "CANDIDATE_MALFORMED" in codes(r)


def test_s14_cli_non_object_candidate_denied_end_to_end(tmp_path):
    rp = tmp_path / "reg.md"
    rp.write_text(MINI_REG)
    cp = tmp_path / "c.json"
    cp.write_text(json.dumps([5, good()]))
    out = tmp_path / "o.json"
    assert s.main(["--registry", str(rp), "--candidates", str(cp), "--out", str(out)]) == 0
    recs = json.load(open(out))["records"]
    assert recs[0]["decision"] == "DENY" and recs[1]["decision"] == "ALLOW"


# ---- S2: spelling variants of a barred name
@pytest.mark.parametrize("name", ["\uff50\uff45\uff52\uff53\uff50\uff45\uff43\uff54\uff52\uff55\uff4d",  # full-width
                                  "Perspectrum", "Pers\u00e9pectrum".replace("\u00e9p", "p"), "CogComp/PERSPECTRUM",
                                  "cog_comp-perspectrum", "PerSpectrum_v2", "https://huggingface.co/datasets/CogComp/perspectrum",
                                  "github.com/google-deepmind/logical-entailment-dataset", "LogicalEntailment",
                                  "logical_entailment", "kunalkukreja21", "KunalKukreja21/temporal-expressions-evaluation-lm",
                                  "temporal-expressions-eval-lm", "temporal_expressions", "TemporalExpressions-LM",
                                  "GSM-8K", "gsm_8_k", "GradeSchoolMath", "TyDi-QA", "iSarcasmEval", "HoVer",
                                  "md-fdc", "MD_PEPs", "SB-6", "sb_6", "ｇｓｍ８ｋ"])
def test_s2_barred_name_under_other_spellings(reg, name):
    r = s.evaluate(good(name=name), reg)
    assert r["decision"] == "DENY" and r["deny_class"] == "BAR" and "A61A_HIT" in codes(r), (name, r["reason_codes"])


@pytest.mark.parametrize("name", ["p\u0435rspectrum", "gsm\u0038k\u200b".replace("\u200b", "\u200b"), "\u0261sm8k", "tydi\u0510qa"])
def test_s2_homoglyph_or_zero_width_name_is_denied(reg, name):
    r = s.evaluate(good(name=name), reg)
    assert r["decision"] == "DENY" and ("NON_ASCII_NAME" in codes(r) or "A61A_HIT" in codes(r))


def test_s2_non_ascii_in_alias_hf_id_and_upstream_is_denied(reg):
    cyr = "p\u0435rspectrum"
    for kw in ({"aliases": [cyr]}, {"hf_id": "CogComp/" + cyr}, {"derived_from": [cyr]}):
        r = s.evaluate(good(**kw), reg)
        assert r["decision"] == "DENY" and "NON_ASCII_NAME" in codes(r), kw


# ---- S3: catalogue spellings and members on a dataset
@pytest.mark.parametrize("kind", ["catalog", "Catalogue", "CATALOGUE ", "collection", "bundle", "multi-task", 5])
def test_s3_catalogue_spellings_never_allowed_and_members_evaluated(reg, kind):
    r = s.evaluate(good(kind=kind, members=[good(name="CogComp/perspectrum"), good(name="m2")]), reg)
    assert r["decision"] == "DENY" and "CATALOGUE_PER_MEMBER_REQUIRED" in codes(r)
    assert [m["decision"] for m in r["members"]] == ["DENY", "ALLOW"] and "A61A_HIT" in codes(r["members"][0])


def test_s3_members_on_a_plain_dataset_make_it_a_catalogue(reg):
    r = s.evaluate(good(members=[good(name="m1")]), reg)
    assert r["decision"] == "DENY" and "CATALOGUE_PER_MEMBER_REQUIRED" in codes(r) and r["members"][0]["decision"] == "ALLOW"


def test_s3_unknown_kind_word_denied_even_without_members(reg):
    r = s.evaluate(good(kind="whatever"), reg)
    assert r["decision"] == "DENY" and "CANDIDATE_MALFORMED" in codes(r)


def test_s3_members_as_single_object_still_evaluated(reg):
    r = s.evaluate({"name": "hub", "kind": "catalogue", "members": good(name="CogComp/perspectrum")}, reg)
    assert r["members"][0]["decision"] == "DENY"


# ---- S4: joined split names
@pytest.mark.parametrize("sp", ["trainval", "traintest", "traindev", "trainvalid", "traineval", "trainholdout",
                                "train_val", "train+validation", "trainheldout", "holdout", "heldout", "hold-out",
                                "blind", "secret", "devtest", "validation", "test", "dev"])
def test_s4_joined_or_hold_out_split_names_are_not_train(sp):
    assert s.split_class(sp) == "eval", sp


@pytest.mark.parametrize("sp", ["train", "train_clean_100", "train-other-500", "training", "train[:80%]", "TRAIN"])
def test_s4_real_train_names_stay_train(sp):
    assert s.split_class(sp) == "train", sp


def test_s4_trainval_only_dataset_has_no_train_split(reg):
    r = s.evaluate(good(splits_available=["trainval"]), reg)
    assert r["decision"] == "DENY" and "NO_TRAIN_SPLIT" in codes(r)


# ---- S5: slices are subsets
def test_s5_slice_request_cannot_ride_a_split_scoped_release(reg, tmp_path):
    c = libri(tmp_path, reg)
    sl = "train-clean-100[:1200]"
    c["splits_available"] = ["train-clean-100", sl, "test-clean"]
    c["splits_requested"] = [sl]
    c["train_split_rows"] = 1200
    c["g13_record"] = write_g13(tmp_path, reg, split=sl, rows=1200)
    r = s.evaluate(c, reg, split_scoped_release=True)
    assert r["decision"] == "DENY" and any("slice" in x["detail"] for x in r["reasons"]) and "train_split_seen" not in r


# ---- S8: LLM markers in free-text provenance
@pytest.mark.parametrize("prov", ["human annotated, some labels by Grok", "human verified, relabelled by Claude Sonnet",
                                  "human annotators; opus rewrites", "crowd workers plus Kimi", "human with GPT4 help",
                                  "crowd + GPT-4o filtering", "human annotators, AI-assisted", "expert with Haiku check",
                                  "annotators, paraphrased by a model", "crowdsourced then translated by MT"])
def test_s8_free_text_llm_markers_deny(reg, prov):
    r = s.evaluate(good(label_provenance=prov), reg)
    assert r["decision"] == "DENY" and "LABELS_LLM_GENERATED" in codes(r), prov


@pytest.mark.parametrize("prov", ["selection-rule", "selection_rule", "labels picked by a similarity rule"])
def test_s8_selection_rule_provenance_denies(reg, prov):
    assert s.evaluate(good(label_provenance=prov), reg)["decision"] == "DENY"


# ---- S9, S10: evidence file and dataset match
def test_s9_evidence_path_must_be_a_regular_file(reg):
    c = good(name="LibriSpeech", splits_available=["train-clean-100", "test-clean"], train_split_rows=10,
             g13_record={"path": "/dev/zero", "sha256": "a" * 64})
    r = s.evaluate(c, reg, split_scoped_release=True)
    assert r["decision"] == "DENY" and any("regular file" in x["detail"] for x in r["reasons"])


def test_s10_punctuation_only_name_cannot_match_a_record_for_another_dataset(reg, tmp_path):
    c = libri(tmp_path, reg, dataset="---")
    c["aliases"] = ["!!!"]
    r = s.evaluate(c, reg, split_scoped_release=True)
    assert r["decision"] == "DENY" and "train_split_seen" not in r


# ---- S11: the one upstream the plan names
@pytest.mark.parametrize("name", ["hotpot_qa", "HotpotQA", "hotpotqa/hotpot_qa", "Hotpot QA"])
def test_s11_hotpotqa_needs_an_opus_ruling(reg, name):
    r = s.evaluate(good(name=name), reg)
    assert r["decision"] == "DENY" and "UPSTREAM_OF_A61A_NEEDS_RULING" in codes(r)
    assert r["deny_class"] == "INSUFFICIENT_EVIDENCE"


def test_s11_declared_hotpotqa_upstream_also_denied(reg):
    assert "UPSTREAM_OF_A61A_NEEDS_RULING" in codes(s.evaluate(good(derived_from=["hotpot_qa"]), reg))


# ---- S12: A82 4, 5, 9 defence in depth
@pytest.mark.parametrize("name", ["civil_comments", "Social Chemistry 101", "go_emotions", "GoEmotions", "ucberkeley-dlab/measuring-hate-speech",
                                  "hatexplain", "allenai/ai2_arc", "ARC", "ARC-Challenge", "openlifescienceai/medmcqa",
                                  "hendrycks/competition_math", "MATH", "deepmind/aqua_rat", "math_qa", "MathQA",
                                  "deepmind/code_contests", "codeparrot/apps", "APPS", "Project_CodeNet", "codeflaws",
                                  "New Yorker Caption Contest", "allenai/wildjailbreak", "allenai/wildguardmix", "When2Call",
                                  "esnli", "e-SNLI"])
def test_s12_a82_excluded_names_denied(reg, name):
    r = s.evaluate(good(name=name), reg)
    assert r["decision"] == "DENY" and "A82_EXCLUDED" in codes(r) and r["deny_class"] == "BAR", name


@pytest.mark.parametrize("name", ["snli", "mathematics-dataset", "arcade-intents", "applications-intents", "maths-word-problems",
                                  "acme-intents"])
def test_s12_name_bars_do_not_overblock_unrelated_names(reg, name):
    assert "A82_EXCLUDED" not in codes(s.evaluate(good(name=name), reg)), name


def test_s12_a82_excluded_upstream_denied(reg):
    assert "A82_EXCLUDED" in codes(s.evaluate(good(derived_from=["civil_comments"]), reg))


@pytest.mark.parametrize("langs,ok", [(["en"], True), (["English"], True), (["en-US"], True), ("en", True), ([], True),
                                      (["en", "de"], False), (["de"], False), ("fr", False)])
def test_s12_a82_9_english_only_when_declared(reg, langs, ok):
    r = s.evaluate(good(languages=langs), reg)
    assert (r["decision"] == "ALLOW") is ok and (("NON_ENGLISH_DECLARED" in codes(r)) is (not ok))


@pytest.mark.parametrize("mod,ok", [("text", True), (["text"], True), (["text", "image"], False), ("image", False),
                                    (["audio"], False), ("vision", False)])
def test_s12_a82_9_text_only_when_declared(reg, mod, ok):
    r = s.evaluate(good(modality=mod), reg)
    assert (r["decision"] == "ALLOW") is ok and (("NON_TEXT_DECLARED" in codes(r)) is (not ok))


# ---- never released by split-scoped release or denylist
def test_barred_facts_survive_a_perfect_evidence_record(reg, tmp_path):
    for name in ("CogComp/perspectrum", "hotpot_qa", "civil_comments"):
        c = _ev_good(tmp_path, reg, name=name)
        d = dl({"name": "x", "keys": [name], "tainted_splits": ["test"]})
        assert s.evaluate(c, reg, d, split_scoped_release=True)["decision"] == "DENY", name


def test_version_is_v2_1():
    assert s.TOOL_VERSION.startswith("split_aware_check v2.1")
