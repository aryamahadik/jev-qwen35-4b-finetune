"""Tests for c_src/common/denylist.py (C_DATA_SPEC.md v4 3.H). Run from lean/:
    ../.venv/bin/python -m pytest -q c_src/common/test_denylist.py
Never reads ohs3/used_sources.json: every OHS-3 test uses a synthetic fixture under c_build/tmp/test_denylist/.
"""
import json
import re
import shutil
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import denylist as D  # noqa: E402

TMP = D.LEAN / "c_build" / "tmp" / "test_denylist"


@pytest.fixture(scope="module")
def tmpdir():
    TMP.mkdir(parents=True, exist_ok=True)
    yield TMP
    shutil.rmtree(TMP, ignore_errors=True)


@pytest.fixture(scope="module")
def dl():
    return D.build(with_ohs3=False)


def _fixture_used_sources(tmpdir, doc, name="used_sources_fixture.json"):
    p = tmpdir / name
    p.write_text(json.dumps(doc))
    return p


FIX = {"generated": "x", "method": "x", "families_note": "x", "datasets": [
    {"name": "zqx-private-corpus", "roles": ["train"], "note": "avoid to be safe"},
    {"name": "plainly-used-set", "roles": ["train", "dev"]},
    {"hf_id": "someorg/kwv-ohs-thing", "status": "OHS-3 source"},
    {"name": "stanfordnlp/snli", "roles": ["locked"], "note": "avoid to be safe"},
    "loose-string-entry (avoid)",
]}


# ------------------------------------------------------------------ normaliser and aliases

def test_tokens_versions():
    assert D.tokens("SQuAD 2.0") == ["squad", "2.0"]
    assert D.strip_version(["squad", "2.0"]) == ["squad"]
    assert D.strip_version(["squad", "v2"]) == ["squad"]
    assert D.strip_version(["conll", "2003"]) == ["conll", "2003"]          # a year is not a version
    assert D.tokens("zenodo.8189044") == ["zenodo", "8189044"]
    assert D.tokens("NLU++") == ["nlupp"]
    assert D.tokens("HelpSteer2") == ["helpsteer2"]
    assert D.compact("Few-NERD") == D.compact("few_nerd") == "fewnerd"
    assert D.compact("O*NET") == "onet"


def test_alias_modes():
    assert D.compile_alias("name:abc")[0] == "name"
    assert D.compile_alias("snli")[0] == "name"                 # <= 4 characters
    assert D.compile_alias("emotion")[0] == "name"              # generic word
    assert D.compile_alias("measuring hate speech")[0] == "span"
    assert D.compile_alias("span:abc")[0] == "span"
    assert D.compile_alias("!!!") is None


def test_dev_rule_is_gate_dev_rule():
    assert D.dev_rule("gd_ghc_hate", "hate") and D.dev_rule("hate_x", "hate") and D.dev_rule("btzsc", "btzsc_x")
    assert not D.dev_rule("gab_hate_corpus", "hate")


def test_category_must_match_class():
    with pytest.raises(D.DenyError):
        D._entry("x", "x", "taint", "already_used", ["abcde"], "test")
    with pytest.raises(D.DenyError):
        D._entry("x", "x", "no_new_rows", "licence", ["abcde"], "test")
    with pytest.raises(D.DenyError):
        D._entry("x", "x", "taint", "label_quality", ["abcde"], "test")
    assert D._entry("x", "x", "no_new_rows", "label_quality", ["abcde"], "test")["class"] == "no_new_rows"


# ------------------------------------------------------------------ A16 ruling b: label quality -> no_new_rows

def test_label_quality_guard_reads_the_recorded_reason():
    """A label_quality entry whose recorded reason also names a taint reason fails the build (mixed -> taint)."""
    D._check_label_quality("e", "label_quality", "distant-supervision labels, about 30% wrong (silver)")
    D._check_label_quality("e", "gold_noise", "silver labels; non-commercial licence")        # not label_quality
    for reason, cls in (("silver labels; licence CC BY-NC", "licence"), ("noisy; listed avoid in used_sources", "ohs"),
                        ("silver; test split only", "test_eval_split"), ("labels by GPT-4", "llm_text_or_labels"),
                        ("machine-translated text, noisy", "synthetic_text"), ("noisy; in forbidden_label_nli", "forbidden_task"),
                        ("noisy; a DI benchmark", "test_eval_split")):
        with pytest.raises(D.DenyError, match=cls):
            D._check_label_quality("e", "label_quality", reason)
    assert D.lq_markers("Real-outcome labels with high Bayes error") == []


def test_label_quality_entries_on_real_inputs(dl):
    lq = [e for e in dl.entries if e["cat"] == "label_quality"]
    assert len(lq) == 17 and all(e["class"] == "no_new_rows" for e in lq)
    names = {e["name"] for e in lq}
    assert {"T-REx", "REBEL", "NYT10 / NYT-H", "SciNLI", "UCI German Credit"} <= names
    # entries whose recorded reason mixes in a taint reason stay taint
    for nm in ("ConjNLI", "FactCC", "HEAD-QA (English)", "TreeDST", "Anthropic/hh-rlhf", "AQuA-RAT", "StepGame",
               "GAD / EU-ADR", "eLife Assessments", "HELP (verypluming)", "Math-Shepherd, PRMBench, auto-labelled PRM sets"):
        assert {e["class"] for e in dl.entries if e["name"] == nm} == {"taint"}, nm
    assert not any(e["cat"] == "llm_written" and e["class"] != "taint" for e in dl.entries)
    v = lambda s, par=(): D.verdict_new(dl, {"names": [s], "parents": list(par)})
    assert v("T-REx")["verdict"] == "no_new_rows" and v("Child", ["T-REx"])["verdict"] == "pass"
    assert v("MuSiQue", ["SQuAD", "T-REx", "Natural Questions", "MLQA", "Zero Shot RE"])["verdict"] == "pass"
    assert v("ShARC")["verdict"] == "deny"                     # rejected.json reason also names a taint reason
    assert v("Social IQa")["verdict"] == "deny"                # 3.G: no licence (the noise entry alone is label_quality)
    assert v("Child", ["Social IQa"])["verdict"] == "deny"
    assert v("UCI German Credit")["verdict"] == "no_new_rows"


# ------------------------------------------------------------------ inputs

def test_rejected_both_formats_and_bad_format(tmpdir, monkeypatch):
    g = tmpdir / "golden_src"
    (g / "fam_a").mkdir(parents=True, exist_ok=True)
    (g / "fam_b").mkdir(parents=True, exist_ok=True)
    (g / "fam_a" / "rejected.json").write_text(json.dumps([{"dataset": "A1", "reason": "r"}]))
    (g / "fam_b" / "rejected.json").write_text(json.dumps({"family": "b", "rejected": [{"dataset": "B1", "reason": "r"},
                                                                                     {"dataset": "B2", "reason": "r"}]}))
    monkeypatch.setattr(D, "GOLDEN_SRC", g)
    rows, files = D.load_rejected()
    assert [(f, i, d) for f, i, d, _ in rows] == [("fam_a", 0, "A1"), ("fam_b", 0, "B1"), ("fam_b", 1, "B2")]
    (g / "fam_b" / "rejected.json").write_text(json.dumps({"family": "b", "items": []}))
    with pytest.raises(D.DenyError):
        D.load_rejected()


def test_real_inputs_fully_curated(dl):
    rows, _ = D.load_rejected()
    assert len(rows) == 243                                    # 10 files, 243 entries on 3 Oct
    assert dl.meta["warnings"] == []                           # every entry, 3.G row, task and OHS item curated
    ids = {e["origin"] for e in dl.entries}
    for fam, i, _, _ in rows:
        assert f"rejected:{fam}#{i}" in ids
    assert len(D.load_3g()) == 30 and all(f"3.G#{r}" in ids for r in range(30))
    tasks = json.load(open(D.FORBIDDEN))
    assert len(tasks) == 152 and all(any(e["id"] == f"forbidden:{t}" for e in dl.entries) for t in tasks)
    assert len(D.load_ohs_list()) == 32


def test_dev_eval_reader_drops_jev_keys():
    r = json.loads('{"source": "a", "meta": {"jev_recorded_p_yes": 0.3, "x": 1}, "jevx": 1}',
                   object_pairs_hook=D.strip_jev_keys)
    assert r == {"source": "a", "meta": {"x": 1}}


# ------------------------------------------------------------------ the OHS-3 part (fixture only)

def test_ohs3_part_is_hashed_and_redacted(tmpdir):
    p = _fixture_used_sources(tmpdir, FIX)
    dlx = D.build(used_sources=p)
    o = dlx.meta["ohs3"]
    assert o["entries"] == 5 and o["selected"] == 4 and o["selected_without_name"] == 0
    assert o["canaries"]["SNLI"] == "hit" and o["canaries"]["HANS"] == "no-hit"
    hit = lambda s: any(i == D.OHS3_LABEL for i, *_ in dlx.match(names=[s]))
    assert hit("zqx private corpus") and hit("kwv-ohs-thing") and hit("someorg/kwv-ohs-thing")
    assert hit("loose string entry")
    assert not hit("plainly used set")                         # a train/dev-only entry is not an input (3.H.1)
    doc = json.dumps(D.denylist_doc(dlx))
    for secret in ("zqx", "plainly", "kwv", "loose"):
        assert secret not in doc                               # names never stored in clear
    v = D.verdict_new(dlx, {"names": ["Zqx Private Corpus"], "parents": []})
    assert v["verdict"] == "deny" and v["entry"] == D.OHS3_LABEL
    assert v["matches"] == [{"entry": D.OHS3_LABEL, "class": "taint"}]      # no alias, field or via
    v = D.verdict_new(dlx, {"names": ["Child set"], "parents": ["zqx-private-corpus"]})
    assert v["verdict"] == "deny" and v["matches"] == [{"entry": D.OHS3_LABEL, "class": "taint"}]
    r = D.verdict_replay(dlx, "s", {"names": ["gd_q"], "datasets": ["Zqx Private Corpus rows", "other clean rows"]})
    assert r["verdict"] == "drop" and r["part"] is None       # never a part (values would say which string hit)


def test_ohs3_alias_expansion_two_spellings(tmpdir):
    """Review case: used_sources names CLINC150 by its HF name clinc_oos; the replay query says clinc150. The checked
    name hits the clear CLINC150 entries, whose curated aliases include clinc_oos, so the hashed part hits too."""
    fx = {"datasets": [{"name": "clinc_oos", "note": "avoid to be safe"},
                       {"hf_id": "AmazonScience/massive", "note": "avoid"},
                       {"name": "stanfordnlp/snli", "note": "avoid"}]}
    dlx = D.build(used_sources=_fixture_used_sources(tmpdir, fx, "us_alias.json"))
    for nm in ("clinc150", "massive"):
        v = D.verdict_replay(dlx, nm, {"names": [nm]})
        assert v["verdict"] == "drop" and v["entry"] == D.OHS3_LABEL and v["part"] is None and v["parts"] == [], nm
        assert {"entry": D.OHS3_LABEL, "class": "taint"} in v["matches"]
    v = D.verdict_new(dlx, {"names": ["CLINC 150"], "parents": []})
    assert v["verdict"] == "deny" and {"entry": D.OHS3_LABEL, "class": "taint"} in v["matches"]
    assert D.verdict_replay(dlx, "banking77", {"names": ["banking77"]})["entry"] != D.OHS3_LABEL
    # a spelling that matches no span of the checked name directly ('amazon massive' vs 'massive') is found only
    # through the clear MASSIVE entry's curated aliases
    fx2 = {"datasets": [{"name": "amazon massive", "note": "avoid"}, {"name": "stanfordnlp/snli", "note": "avoid"}]}
    dl2 = D.build(used_sources=_fixture_used_sources(tmpdir, fx2, "us_alias2.json"))
    assert not any(isinstance(i, str) for i, *_ in dl2._match(names=["massive"]))       # no direct hit
    v = D.verdict_replay(dl2, "massive", {"names": ["massive"]})
    assert v["verdict"] == "drop" and v["entry"] == D.OHS3_LABEL
    # without the used_sources entry the same sources keep their old verdicts (no false expansion)
    dl0 = D.build(used_sources=_fixture_used_sources(tmpdir, {"datasets": [{"name": "stanfordnlp/snli",
                                                                             "note": "avoid"}]}, "us_alias0.json"))
    assert D.verdict_replay(dl0, "massive", {"names": ["massive"]})["verdict"] == "keep_no_new_rows"
    assert D.verdict_replay(dl0, "clinc150", {"names": ["clinc150"]})["verdict"] == "drop_part"
    assert len(dlx.entries) == len(dl0.entries)                 # hashed names never become clear entries


def test_platform_words_never_match_on_their_own(tmpdir):
    """A16 ruling a: a bare platform word never matches (no report-only set either); the left-out count is disclosed."""
    fx = {"datasets": [{"names": ["zqx-relcorpus", "wikipedia"], "note": "avoid"},
                       {"name": "stanfordnlp/snli", "note": "avoid"}]}
    dlx = D.build(used_sources=_fixture_used_sources(tmpdir, fx, "us_plat.json"))
    o = dlx.meta["ohs3"]
    assert o["selected"] == 2 and o["selected_platform_alias_suppressed"] == 1 and o["selected_platform_alias_only"] == 0
    assert set(dlx.hashed) == {D.OHS3_LABEL}
    v = D.verdict_new(dlx, {"names": ["Some child set"], "parents": ["Wikipedia"]})
    assert v["verdict"] == "pass" and not v["hit"] and v["matches"] == [] and "report_only" not in v
    v = D.verdict_new(dlx, {"names": ["zqx relcorpus"], "parents": []})
    assert v["verdict"] == "deny"
    r = D.verdict_replay(dlx, "s", {"names": ["gd_q"], "domains": ["wikipedia"]})
    assert r["verdict"] == "keep" and not r["hit"] and "report_only" not in r
    doc = D.denylist_doc(dlx)
    assert doc["ohs3"]["selected_platform_alias_suppressed"] == 1 and "zqx" not in json.dumps(doc)
    assert "platform_keys" not in doc["ohs3"] and doc["rulings"]["platform_words"].startswith("RULED (PREREG_FINAL.md A16 a)")
    assert not any("platform" in p for p in doc["provisional"])
    q = tmpdir / "q_plat.json"
    q.write_text(json.dumps({"datasets": {"a": {"names": ["Child"], "parents": ["Wikipedia"]},
                                          "b": {"names": ["Clean"], "parents": []}}}))
    counts, _ = D.run_check(dlx, tmpdir / "dl.json", "0" * 64, q, tmpdir / "out_plat.json")
    assert "ohs3_platform_hit" not in counts and counts["deny_taint"] == 0 and counts["pass"] == 2
    hdr = json.load(open(tmpdir / "out_plat.json"))
    assert hdr["ohs3_platform_alias_suppressed_entries"] == 1 and hdr["canonical"] is False
    assert hdr["platform_rule"] == D.PLATFORM_RULE
    out = tmpdir / "classes_plat.md"
    D.classes_md(dlx, out)
    assert "1 of the 2 selected entries had such a word left out" in out.read_text()
    # the curated Stack Exchange alias still denies (its text is the denied OHS source, not a host)
    assert D.verdict_new(dlx, {"names": ["Child"], "parents": ["Stack Exchange"]})["verdict"] == "deny"
    only = {"datasets": [{"name": "wikipedia", "note": "avoid"}, {"name": "stanfordnlp/snli", "note": "avoid"}]}
    with pytest.raises(D.DenyError, match="1 of them only a bare platform word"):
        D.build(used_sources=_fixture_used_sources(tmpdir, only, "us_plat_only.json"))


def test_no_override_flags_and_fixed_selection(tmpdir):
    for flag in (["--no-ohs3"], ["--avoid-pattern", "^a"], ["--used-sources", "x.json"]):
        with pytest.raises(SystemExit) as e:
            D.main(["check", "--query", "q.json", "--out", "o.json"] + flag)
        assert e.value.code == 2, flag                         # argparse: unknown argument, nothing built
    p = _fixture_used_sources(tmpdir, FIX, "us_sel.json")
    with pytest.raises(D.DenyError):
        D.read_used_sources(p, selection="^a")                # never a free pattern
    lk = _fixture_used_sources(tmpdir, {"datasets": [{"name": "lk-set", "roles": ["locked"]},
                                                     {"name": "stanfordnlp/snli", "note": "avoid"}]}, "us_lk.json")
    assert D.read_used_sources(lk)[3]["selected"] == 2                           # default: avoid_or_locked (A16 c)
    assert D.read_used_sources(lk, selection="avoid_only")[3]["selected"] == 1   # the one other fixed choice
    assert D.build(with_ohs3=False).meta["canonical"] is False
    assert D.build(used_sources=p).meta["canonical"] is False  # a fixture is never canonical


def test_ohs3_key_needs_the_file(tmpdir):
    p = _fixture_used_sources(tmpdir, FIX)
    dlx = D.build(used_sources=p)
    keys = D.denylist_doc(dlx)["ohs3"]["keys"]["span"]
    naive = D.hashlib.sha256(b"span:zqxprivatecorpus").hexdigest()[:32]
    assert naive not in keys                                   # keyed by the file bytes, not brute-forceable


def test_ohs3_format_failures(tmpdir):
    with pytest.raises(D.DenyError):
        D.read_used_sources(_fixture_used_sources(tmpdir, {"items": []}, "bad1.json"))
    nameless = {"datasets": [{"weird_key": "zz-set", "note": "avoid"}, {"name": "stanfordnlp/snli", "note": "avoid"}]}
    with pytest.raises(D.DenyError):
        D.build(used_sources=_fixture_used_sources(tmpdir, nameless, "bad2.json"))
    no_canary = {"datasets": [{"name": "zz-set-only", "note": "avoid"}]}
    with pytest.raises(D.DenyError):
        D.build(used_sources=_fixture_used_sources(tmpdir, no_canary, "bad3.json"))
    with pytest.raises(D.DenyError):
        D.read_used_sources(tmpdir / "missing.json")


# ------------------------------------------------------------------ new-data verdicts

def test_parents_recursive_and_cycles(dl):
    reg = {"Mid set": {"parents": ["SNLI"]}, "Loop A": {"parents": ["Loop B"]}, "Loop B": {"parents": ["Loop A"]}}
    v = D.verdict_new(dl, {"names": ["Child corpus"], "parents": ["Mid set"]}, reg)
    assert v["verdict"] == "deny" and any(m.get("via") == "Mid set > SNLI" for m in v["matches"])
    v = D.verdict_new(dl, {"names": ["Clean thing"], "parents": ["Loop A"]}, reg)
    assert v["verdict"] == "pass" and not v["hit"]


def test_no_new_rows_rules(dl):
    v = D.verdict_new(dl, {"names": ["Pack"], "parents": [{"name": "O*NET occupation titles"}]})
    assert v["verdict"] == "pass" and v["parent_no_new_rows_pass"] == ["O*NET occupation titles"]
    assert D.verdict_new(dl, {"names": ["MedMCQA"], "parents": []})["verdict"] == "no_new_rows"
    assert D.verdict_new(dl, {"names": ["MedMCQA"], "parents": [], "emits_rows": False})["verdict"] == "pass"
    v = D.verdict_new(dl, {"names": ["Fresh set"], "parents": ["ChaosNLI"]})      # taint parent -> deny
    assert v["verdict"] == "deny"


def test_versions_and_subsets_distinguish(dl):
    cls = lambda s, desc=(): {m["class"] for m in D.verdict_new(dl, {"names": [s], "datasets": list(desc),
                                                                      "parents": []})["matches"]}
    assert "taint" not in cls("nvidia/HelpSteer2") and "taint" in cls("HelpSteer v1")
    assert "taint" in cls("Taskmaster-4") and cls("gd_taskmaster3") == {"no_new_rows"}
    assert "taint" in cls("MultiWOZ 2.2") and cls("MultiWOZ 2.1") == {"no_new_rows"}
    assert "taint" in cls("WebRED 5") and cls("x", ["WebRED (webred_21.tfrecord, WebRED 2+1)"]) == set()
    assert "taint" in cls("CommonsenseQA 2.0") and cls("csqa") == {"no_new_rows"}
    assert cls("x", ["ParticleMedia/RAGTruth (Summary task, train split)"]) == {"taint"}   # DI RAGTruth, split scope
    assert "taint" in cls("x", ["RAGTruth QA (MS MARCO)"])
    assert cls("x", ["FEVEROUS (fever.ai), feverous_train_challenges.jsonl"]) == set()  # 'fever' is name-only
    assert "taint" in cls("FEVER")
    assert cls("x", ["openFDA drug labeling (SPL)"]) == set() and "taint" in cls("openFDA recalls")
    assert cls("x", ["Stanford Politeness Corpus, Wikipedia half"]) == {"no_new_rows"}
    assert "taint" in cls("x", ["Stanford Politeness Corpus, Stack Exchange half"])
    assert cls("x", ["JetBrains CommitChronicle, Zenodo record 8189044"]) == set()        # Zenodo hosting is fine


def test_missing_parents_fails_g1(tmpdir, dl):
    q = tmpdir / "q_noparents.json"
    q.write_text(json.dumps({"datasets": {"a": {"names": ["Something"]}}}))
    with pytest.raises(D.DenyError):
        D.run_check(dl, tmpdir / "dl.json", "0" * 64, q, tmpdir / "out.json")


# ------------------------------------------------------------------ replay verdicts (3.H.3)

def test_replay_rules(dl):
    r = lambda it: D.verdict_replay(dl, "s", it)
    v = r({"names": ["yelp"]})
    assert v["verdict"] == "drop" and v["class"] == "taint" and v["part"] is None
    v = r({"names": ["clinc150"]})                              # dev + eval/DI test split: train rows kept
    assert v["verdict"] == "drop_part" and v["part"]["field"] == "split" and not v["dev_seen_exception"]
    v = r({"names": ["pg_numeric"]})                            # dev seen source by design
    assert v["verdict"] == "keep_dev_seen" and v["dev_seen_exception"] and v["class"] == "taint"
    v = r({"names": ["mnli"]})
    assert v["verdict"] == "keep_no_new_rows" and v["class"] == "no_new_rows"
    v = r({"names": ["gd_x"], "datasets": ["Foo (prompts from Anthropic/hh-rlhf)", "Bar clean text"]})
    assert v["verdict"] == "drop_part" and v["part"] == {"field": "dataset",
                                                         "values": ["Foo (prompts from Anthropic/hh-rlhf)"]}
    v = r({"names": ["gd_x"], "datasets": ["Foo (Anthropic/hh-rlhf)", "Bar (Anthropic/hh-rlhf)"]})
    assert v["verdict"] == "drop" and v["part"] is None
    v = r({"names": ["clinc150"], "datasets": ["Foo (prompts from Anthropic/hh-rlhf)", "Bar clean text"]})
    assert v["verdict"] == "drop_part" and [p["field"] for p in v["parts"]] == ["dataset", "split"]
    assert v["part"] == v["parts"][0] and v["parts"][1]["rule"] == "train_provenance"
    v = r({"names": ["musr_team_allocation"]})                  # MuSR has no train split: whole source
    assert v["verdict"] == "drop"
    v = r({"names": ["gd_politeness_votes"], "datasets": ["Stanford Politeness Corpus, Wikipedia half"]})
    assert v["verdict"] == "keep_no_new_rows"
    assert r({"names": ["gd_casehold_yn"], "datasets": ["casehold/casehold (CaseHOLD)"]})["verdict"] == "keep"


def test_replay_query_file_runs(tmpdir, dl):
    q = D.LEAN / "c_build" / "replay_denylist_query.json"
    counts, ver = D.run_replay(dl, tmpdir / "dl.json", "0" * 64, q, tmpdir / "replay_out.json")
    assert counts["sources"] == 204
    out = json.load(open(tmpdir / "replay_out.json"))
    for v in out["verdicts"].values():                          # the sampler's schema (RUNBOOK_replay_reads 3.2)
        assert set(v) >= {"hit", "class", "entry", "part", "parts", "dev_seen_exception"}
        assert v["part"] == (v["parts"][0] if v["parts"] else None)
        assert bool(v["parts"]) == (v["verdict"] == "drop_part")
    for s in ("banking77", "boolq", "condaqa", "dbpedia", "br_newsmtsc", "civil_comments", "toxic_conv", "yelp",
              "yelp5", "yahoo", "amazon_polarity", "mrpc", "tb_label_nli", "gd_bbh_mistake", "musr_team_allocation",
              "wiki_stance_afd", "gd_finqa"):
        assert ver[s]["verdict"] == "drop", s
    for s in ("proofwriter", "mnli", "qnli", "csqa", "copa", "gd_sc101", "gd_onet_occupation", "br_emobank",
              "gd_taskmaster1", "massive"):
        assert ver[s]["verdict"] == "keep_no_new_rows", s
    for s in ("pg_numeric", "gd_ghc_hate"):
        assert ver[s]["verdict"] == "keep_dev_seen", s
    for s in ("gd_crossner", "gd_webred", "gd_helpsteer3_pref", "gd_feverous", "gd_druglabel_section",
              "gd_crowdtruth_mre", "gd_edgar_10k_item"):
        assert ver[s]["verdict"] in ("keep", "keep_no_new_rows"), s


def test_public_and_commit_queries(tmpdir, dl):
    _, ver = D.run_check(dl, tmpdir / "dl.json", "0" * 64, D.LEAN / "c_build" / "denylist_query_public.json",
                         tmpdir / "pub.json")
    assert len(ver) == 14
    assert all(v["verdict"] == "pass" for v in ver.values())                  # A16 b: T-REx is label_quality
    assert "T-REx" in ver["2_musique"]["parent_no_new_rows_pass"]
    _, ver = D.run_check(dl, tmpdir / "dl.json", "0" * 64, D.LEAN / "c_build" / "denylist_query_commit.json",
                         tmpdir / "com.json")
    assert all(v["verdict"] == "pass" for v in ver.values())


# ------------------------------------------------------------------ paths (7.4) and output

def test_paths():
    L = D.LEAN
    refused = [L / "preds_ohs" / "jev_x.jsonl", L / "ohs3" / "used_sources.json", L / "data" / "ohs3.jsonl",
               L / "data" / "ohs3_parts" / "a.jsonl", D.ROOT / "bench" / "runs" / "jev_p1" / "x.json",
               L / "c_spec" / "REVIEW_rules.md", L / "c_spec" / "sealed_brief" / "a.md", L / "logs" / "jev_ohs.log",
               D.ROOT / "reports" / "OpenDecide_v05_vs_Jev.md", L / "c_build" / "foo_jev.json",
               D.ROOT / "bench" / "ejs5" / "runs" / "x.jsonl", L / "prep89" / "a.py",
               Path("/private/tmp/claude-501/x/scratchpad/a.json"), Path.home() / ".claude" / "projects" / "a.jsonl"]
    for p in refused:
        assert D.check_path(p), p
    for p in (L / "data" / "eval_jagged.jsonl", L / "c_spec" / "C_DATA_SPEC.md", L / "golden_src" / "GOLDEN_SPEC.md",
              D.ROOT / "bench" / "decision_index" / "sample_manifest_sample10k.json"):
        assert D.check_path(p) is None, p
    item = D.ROOT / "bench" / "splits" / "jevbench_public.jsonl"
    assert D.check_path(item) and D.check_path(item, allow_jevbench_items=True) is None
    with pytest.raises(D.DenyError):
        D.safe_open(L / "ohs3" / "used_sources.json")


def test_classes_md_lists_every_entry(tmpdir):
    dlx = D.build(used_sources=_fixture_used_sources(tmpdir, FIX))
    out = tmpdir / "classes.md"
    D.classes_md(dlx, out)
    t = out.read_text()
    for e in dlx.entries:
        assert f"`{e['id']}`" in t
    assert "zqx" not in t and "kwv" not in t and "ohs3-avoid" in t
    assert re.search(r"4 selected", t)


def test_derived_aliases_skip_platform_words_and_fragments():
    a = D.derive_aliases("FooRel (Wikipedia + Wikidata, built 2019)")
    assert "FooRel" in a and not any(D.compact(x) in ("wikipedia", "wikidata") for x in a)
    a = D.derive_aliases("wikimedia/wikipedia")
    assert "wikimedia/wikipedia" in a and "wikipedia" not in a
    a = D.derive_aliases("stanfordnlp/snli (SNLI, avoid to be safe)")
    assert {"stanfordnlp/snli", "snli", "SNLI"} <= set(a)
    a = D.derive_aliases("Yahoo Questions and Answers")
    assert a == ["Yahoo Questions and Answers"]
