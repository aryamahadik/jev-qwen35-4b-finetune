"""Reviewer R's devx (yn2b/SPEC.md 6, 8.1, 8.5; yn2b/build_devx.py + golden_src/gen3/dx_*.py).

500 rows, 100 per family (F1 rule_chain, F2 tool_guard, F3 state_track, F5 lead_score, F6 def_literal) from each
family's devx export (held-out distribution); gold from the shared decide(); 100% parse-back; card and option rules;
determinism; renderer isolation (no training-template module is imported); the write path (tmp only); the blind scorer
and the SPEC 7 decontamination gate. CPU only; nothing is written outside pytest's tmp_path.
"""
from __future__ import annotations

import ast
import copy
import json
import re
from pathlib import Path

import pytest

from devx_helpers import FAMILY_CODE, GEN3, KEYS, LEAN, bd, built, dx, mv, rows_sha


def _answer(g):
    return ("yes" if g["gold"] == 1 else "no") if g["qtype"] == "noul" else g["gold"]


# ------------------------------------------------------------------------------------------------ counts + labels
@pytest.mark.parametrize("key", KEYS)
def test_counts_ids_and_split(key):
    b = built()[key]
    assert len(b.rows) == 100 and len(b.golden) == 100
    assert len({g["id"] for g in b.golden}) == 100
    assert len({g["meta"]["latent_id"] for g in b.golden}) == len({r["meta"]["latent_id"] for r in b.rows})
    for g in b.golden:
        assert g["split"] == "yn2b_devx"
        assert g["source"] == f"gd_{key}"
        assert g["meta"]["dev_kind"] == "devx"
        assert g["meta"]["latent_id"].startswith(FAMILY_CODE[key] + "-dx-")


def test_total_is_500_rows():
    assert sum(len(b.golden) for b in built().values()) == 500


@pytest.mark.parametrize("key", KEYS)
def test_parse_back_is_100_percent(key):
    a = built()[key].agree
    assert (a["rows"], a["agree"], a["disagree"], a["proj_mismatch"]) == (100, 100, 0, 0), a["examples"][:3]


@pytest.mark.parametrize("key", KEYS)
def test_parse_back_catches_a_wrong_gold(key):
    """The parse-back is not vacuous: a row whose stored gold is changed is reported as a disagreement."""
    b = built()[key]
    mod = bd.module(key)
    bad = []
    for g in b.golden[:12]:
        h = copy.deepcopy(g)
        if h["qtype"] == "noul":
            h["gold"] = 1 - h["gold"]
        else:
            h["gold"] = next(o for o in h["options"] if o != h["gold"])
        bad.append(h)
    rep = dx.parse_back(mod, bad, {})
    assert rep["disagree"] == len(bad) and rep["agree"] == 0


@pytest.mark.parametrize("key", KEYS)
def test_yes_share_of_yes_no_rows_is_balanced(key):
    s = dx.summary(built()[key].rows)
    assert s["n_yn_jb"] >= 25
    assert 0.45 <= s["yes_share_yn_jb"] <= 0.55, s["yes_share_yn_jb"]


# ------------------------------------------------------------------------------------------------ cards + options
CARD_LINE = re.compile(r"- ([^:]+): .+")


@pytest.mark.parametrize("key", KEYS)
def test_card_and_option_rules(key):
    for g in built()[key].golden:
        q = g["meta"]["qkind"]
        if g["qtype"] == "noul":
            assert g["gold"] in (0, 1) and not g["options"]
            assert isinstance(g["card"], str), g["id"]
            heads = [CARD_LINE.fullmatch(x).group(1) for x in g["card"].split("\n")]
            yn = sorted(h.lower() for h in heads if h.lower() in ("yes", "no"))
            assert yn == ["no", "yes"], g["id"]
            extra = [h for h in heads if h.lower() not in ("yes", "no")]
            if extra:   # F6 is/not and judge rows key the definition itself by its clause name
                assert key == "gen3_def_literal" and len(extra) == 1 and extra[0] in g["instructions"], g["id"]
            continue
        opts = g["options"]
        assert g["qtype"] == "choice" and len(opts) >= 2 and len(set(opts)) == len(opts), g["id"]
        assert g["gold"] in opts, g["id"]
        if q == "jb":
            assert len(opts) == 2
            if tuple(opts) == tuple(mv.JB_FALLBACK):
                assert "Statement:" in g["instructions"], g["id"]     # a fallback JB question states the claim
        if q == "score":
            assert g["card"] is None, g["id"]
        if g["card"] is not None:
            for line in g["card"].split("\n"):
                m = CARD_LINE.fullmatch(line)
                assert m and m.group(1) in opts, (g["id"], line)


ARTICLE_SLIP = re.compile(r"(?<![A-Za-z])a '?[aeioAEIO]\w*")


@pytest.mark.parametrize("key", KEYS)
def test_no_a_before_a_vowel(key):
    for g in built()[key].golden:
        txt = " ".join([g["state"], g["instructions"] or "", g["card"] or "", json.dumps(g["options"])])
        m = ARTICLE_SLIP.search(txt)
        assert m is None, (g["id"], txt[max(0, m.start() - 40):m.end() + 20])


# ------------------------------------------------------------------------------------------------ determinism + latents
@pytest.mark.parametrize("key", KEYS)
def test_build_is_deterministic(key):
    again = bd.build([key])[key]
    assert rows_sha(again.golden) == rows_sha(built()[key].golden)
    assert rows_sha(again.rows) == rows_sha(built()[key].rows)


@pytest.mark.parametrize("key,fname,n", [("gen3_def_literal", "f6_devx_latents.json", 100),
                                         ("gen3_rule_chain", "f1_devx_latents.json", 100)])
def test_latent_export_prefix_equals_the_frozen_file(key, fname, n):
    """The renderers use a longer export (to pick balanced latents); it is prefix-stable: its first 100 latents are the
    frozen devx latent file."""
    mod = bd.module(key)
    frozen = json.loads((LEAN / "yn2b" / fname).read_text())
    if isinstance(frozen, dict):
        assert (frozen["key"], frozen["split"], frozen["n"]) == (key, "devx", n)
        frozen = frozen["latents"]
    got = json.loads(json.dumps(mod.export()[:n], default=list))
    assert len(frozen) == n
    assert got == frozen


@pytest.mark.parametrize("key", KEYS)
def test_devx_latents_never_appear_in_train_or_dev(key):
    lids = {g["meta"]["latent_id"] for g in built()[key].golden}
    for part in ("train", "dev"):
        try:
            rows, _ = mv.read_raw(key, part)
        except FileNotFoundError:
            continue
        assert not lids & {r["meta"]["latent_id"] for r in rows}
        assert not {g["state"] for g in built()[key].golden} & {r["state"] for r in rows}


# ------------------------------------------------------------------------------------------------ renderer isolation
CORES = {
    "gen3_def_literal": {"export_latents"},
    "dl_core": {"decide", "definition_parts", "edge_tags"},
    "gen3_lead_score": {"ATTACK_ROWS", "PLAN_ROWS", "LeadScoreBuilder", "QUERY_OF_KIND", "__file__", "decide"},
    "gen3_rule_chain": {"devx_latents"},
    "rc_core": {"SK", "decide", "evaluate", "groups", "pivotal", "primary_group", "shortcut_traces"},
    "gen3_tool_guard": {"devx_latents"},
    "tg_core": {"Conf", "Item", "LogE", "Res", "Result", "Rule", "Turn", "appears", "decide", "evaluate",
                "named_resources", "tool_of"},
    "tg_output": {"OItem", "REPORT_TOOLS_HOLD", "TRICKY_RX", "decide_output"},
    "tg_packs": {"Arg", "PACKS", "Tool"},
    "gen3_state_track": {"MACHINES", "TIER_EVENTS"},
    "gen3_state_track_sim": {"Ev", "Query", "SHORTCUT_NAMES", "World", "decide", "in_play", "replay",
                             "shortcut_answer"},
}
STDLIB = {"__future__", "copy", "json", "re", "sys", "zoneinfo", "collections", "datetime", "fractions", "pathlib",
          "random", "hashlib", "dataclasses", "typing"}


@pytest.mark.parametrize("modname", ["dx_common"] + [bd.MODULES[k] for k in KEYS])
def test_renderers_use_only_latents_and_shared_decide(modname):
    """dx_* import no family renderer or template module, and use only the latent exports, schemas and decide() of
    the shared cores (the allow-list above); rc_core skins are read for the time direction only."""
    src = (GEN3 / f"{modname}.py").read_text()
    tree = ast.parse(src)
    alias = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                assert a.name in STDLIB | {"mv_core", "dx_common"} | set(CORES), (modname, a.name)
                alias[a.asname or a.name] = a.name
        elif isinstance(node, ast.ImportFrom):
            assert node.module in STDLIB, (modname, node.module)
    used = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and alias.get(node.value.id) in CORES:
            used.setdefault(alias[node.value.id], set()).add(node.attr)
    for m, attrs in used.items():
        assert attrs <= CORES[m], (modname, m, attrs - CORES[m])
    for m in re.finditer(r"SK\.SKINS\[[^\]]+\](.{0,20})", src):
        assert m.group(1).startswith('["time"]["dir"]'), m.group(0)


# ------------------------------------------------------------------------------------------------ write path + scorer
def test_write_path_goes_only_where_redirected(tmp_path, monkeypatch):
    key = "gen3_def_literal"
    monkeypatch.setattr(mv, "RAW_DIR", tmp_path / "raw")
    monkeypatch.setattr(mv, "DEFS_DIR", tmp_path / "defs")
    monkeypatch.setattr(mv, "MANIFEST", tmp_path / "MANIFEST_yn2b.jsonl")
    monkeypatch.setattr(bd, "REPORT", tmp_path / "devx_report.json")
    monkeypatch.setattr(bd, "BLIND", tmp_path / "devx_blind.json")
    ans = {key: {g["id"]: _answer(g) for g in built()[key].golden[:20]}}
    ap = tmp_path / "answers.json"
    ap.write_text(json.dumps(ans))
    bd.main(["--families", key, "--write", "--score-blind", str(ap)])
    rows, _ = mv.read_raw(key, "devx", tmp_path / "raw")
    assert json.loads(json.dumps(built()[key].rows)) == rows
    rep = json.loads((tmp_path / "devx_report.json").read_text())
    assert rep["families"][key]["parse_back"]["agree"] == 100
    assert rep["written"] and all(Path(p).is_absolute() and Path(p).is_relative_to(tmp_path.resolve())
                                  for p in rep["written"])   # a relative path would mean a write inside lean/
    blind = json.loads((tmp_path / "devx_blind.json").read_text())
    assert blind["results"][key] == {"rows": 20, "agree": 20, "share": 1.0, "misses": []}
    man = [json.loads(x) for x in (tmp_path / "MANIFEST_yn2b.jsonl").read_text().splitlines()]
    assert {m["part"] for m in man} >= {"devx", "defs", "devx_report", "devx_blind"}
    with pytest.raises((SystemExit, RuntimeError)):     # a second write without --overwrite is refused
        bd.main(["--families", key, "--write"])


def test_default_outputs_stay_under_the_allowed_roots():
    import devx_decontam as dd
    roots = [LEAN / "golden_src" / "gen3", LEAN / "yn2b", LEAN / "data" / "v14_parts" / "yn2b_raw",
             LEAN / "data" / "v14_parts" / "yn2b_defs"]
    paths = [bd.REPORT, bd.BLIND, dd.OUT, mv.MANIFEST, mv.DEFS_DIR / "x.json"]
    for k in KEYS:
        paths += list(mv.raw_paths(k, "devx"))
    for p in paths:
        assert any(Path(p).resolve().is_relative_to(r.resolve()) for r in roots), p


def test_score_blind_counts_hits_and_misses():
    b = built()
    key = "gen3_state_track"
    ans = {g["id"]: _answer(g) for g in b[key].golden}
    first = sorted(ans)[0]
    ans[first] = "not an option"
    res = bd.score_blind(b, {key: ans})[key]
    assert (res["rows"], res["agree"]) == (100, 99)
    assert [m["id"] for m in res["misses"]] == [first]


def test_blind_sheets_are_gold_free_50_per_family():
    sheets = bd.blind_sheets(built())
    assert set(sheets) == set(KEYS)
    for k, sheet in sheets.items():
        ids = {g["id"] for g in built()[k].golden}
        assert len(sheet) == 50 and {x["id"] for x in sheet} <= ids
        for x in sheet:
            assert "gold" not in x and "meta" not in x


# ------------------------------------------------------------------------------------------------ decontamination
def test_decontamination_gate_passes():
    import devx_decontam as dd
    rep = dd.run(built())
    assert rep["rows"] == 500
    assert rep["missing_reference_files"] == []
    assert rep["7.1_ohs3_loaded"] is True
    assert rep["ok"] is True, {k: v for k, v in rep.items() if k != "7.3_cue_shares"}
