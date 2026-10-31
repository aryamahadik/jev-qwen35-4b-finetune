import json
import os

import pytest

import access_audit as aa

CFG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "audit_scopes.json")
ROOT = "/Users/aryamahadik/Documents/jev"
C2B = ROOT + "/opendecide-data/lean/c2_build"
C21 = C2B + "/zed_orch/c21"
TI = C21 + "/training_inputs"


@pytest.fixture(scope="module")
def cfg():
    with open(CFG_PATH) as f:
        return aa.Config(json.load(f))


def tu(name, inp, i):
    return {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "tu%d" % i, "name": name, "input": inp}]}}


def write_tr(path, label, uses, cwd=None):
    with open(path, "w") as f:
        for i, (name, inp) in enumerate(uses):
            e = tu(name, inp, i)
            e["agentLabel"] = label
            if cwd:
                e["cwd"] = cwd
            f.write(json.dumps(e) + "\n")


def run(cfg, tmp_path, label, uses, cwd=None):
    p = tmp_path / "t1.jsonl"
    write_tr(p, label, uses, cwd)
    stats, unm, unr, bad, n, ne = aa.audit([str(p)], cfg)
    return aa.summarise(stats, unm, unr, bad, n, ne, 1, cfg), unm


def test_in_scope_reads_are_clean(cfg, tmp_path):
    uses = [("Read", {"file_path": TI + "/PLAN_TRAINING_SIDE.md"}),
            ("Read", {"file_path": TI + "/LANE_L-0.md"}),
            ("Read", {"file_path": TI + "/excerpts/tools_s5.md"}),
            ("Write", {"file_path": C2B + "/c21_infra/row_start_guard.py"}),
            ("Edit", {"file_path": C2B + "/zed_orch/a64/A64_TOOLS.md"}),
            ("Read", {"file_path": C2B + "/c21_infra/tests/test_x.py"})]
    rep, _ = run(cfg, tmp_path, "L-0 guard", uses)
    p = rep["prefixes"]["L-0"]
    assert (p["ok"], p["deny"], p["out"]) == (6, 0, 0) and not rep["findings_present"]


def test_training_agent_forbidden_and_out_of_scope(cfg, tmp_path):
    uses = [("Read", {"file_path": C21 + "/C2_1_PLAN_v3.md"}),
            ("Read", {"file_path": C21 + "/C2_1_PLAN_v3_SKEPTIC.md"}),
            ("Read", {"file_path": C21 + "/research_v3/permission.md"}),
            ("Read", {"file_path": ROOT + "/opendecide-data/lean/ohs5_sealed/OHS5_FREEZE.json"}),
            ("Read", {"file_path": ROOT + "/opendecide-data/lean/data/ohs3_parts/part1.json"}),
            ("Read", {"file_path": TI + "/LANE_L-E.md"}),
            ("Read", {"file_path": TI + "/LANE_L-A.md"}),
            ("Read", {"file_path": ROOT + "/README.md"}),
            ("Write", {"file_path": C2B + "/mix_c2.py"}),
            ("Write", {"file_path": ROOT + "/HANDOFF.md"}),
            ("Write", {"file_path": ROOT + "/elsewhere/new.py"})]
    rep, _ = run(cfg, tmp_path, "L-0 guard", uses)
    p = rep["prefixes"]["L-0"]
    assert p["deny"] == 9 and p["out"] == 2 and rep["findings_present"]
    names = {(f["verdict"], f["kind"], f["basename"]) for f in p["findings"]}
    assert ("deny", "read", "C2_1_PLAN_v3.md") in names
    assert ("deny", "read", "OHS5_FREEZE.json") in names
    assert ("deny", "read", "LANE_L-E.md") in names
    assert ("deny", "read", "LANE_L-A.md") in names
    assert ("deny", "write", "mix_c2.py") in names
    assert ("out", "read", "README.md") in names
    assert ("out", "write", "new.py") in names


def test_other_training_lane_reads_own_lane_only(cfg, tmp_path):
    rep, _ = run(cfg, tmp_path, "L-A T50 solver",
                 [("Read", {"file_path": TI + "/LANE_L-A.md"}), ("Read", {"file_path": TI + "/LANE_L-0.md"})])
    p = rep["prefixes"]["L-A"]
    assert (p["ok"], p["deny"]) == (1, 1)


def test_longest_prefix_and_case_insensitive(cfg):
    assert cfg.agent_for("L-0:something")["prefix"] == "L-0"
    assert cfg.agent_for("l-s sealed brief")["prefix"] == "L-S"
    assert cfg.agent_for("mystery") is None


def test_unmapped_label_reported_and_nonzero(cfg, tmp_path):
    rep, unm = run(cfg, tmp_path, "mystery-agent", [("Read", {"file_path": "/x/y.md"})])
    assert unm["mystery-agent"] == 1 and rep["findings_present"] and rep["prefixes"] == {}


def test_unrestricted_not_audited(cfg, tmp_path):
    rep, _ = run(cfg, tmp_path, "orchestrator", [("Read", {"file_path": C21 + "/C2_1_PLAN_v3.md"})])
    assert rep["unrestricted_tool_uses"] == {"orchestrator": 1} and not rep["findings_present"]


def test_sealed_agent_cannot_read_training_side(cfg, tmp_path):
    uses = [("Read", {"file_path": ROOT + "/opendecide-data/lean/ohs5_sealed/notes.md"}),
            ("Read", {"file_path": TI + "/PLAN_TRAINING_SIDE.md"}),
            ("Read", {"file_path": C21 + "/research_v3/sealed.md"})]
    rep, _ = run(cfg, tmp_path, "L-S brief", uses)
    p = rep["prefixes"]["L-S"]
    assert p["ok"] == 1 and p["deny"] == 2 and p["scope_unconfirmed"]


def test_bash_reads_writes_and_redirects(cfg, tmp_path):
    cmd = ("cd %s && cat %s/PLAN_TRAINING_SIDE.md | head -5 && sed -n 1,5p %s/C2_1_PLAN_v3.md "
           "&& echo hi > %s/c21_infra/out.txt && python3 ./row_start_guard.py 2>/dev/null") % (TI, TI, C21, C2B)
    rep, _ = run(cfg, tmp_path, "L-0 x", [("Bash", {"command": cmd})], cwd=ROOT)
    p = rep["prefixes"]["L-0"]
    bn = {(f["verdict"], f["kind"], f["basename"]) for f in p["findings"]}
    assert ("deny", "read", "C2_1_PLAN_v3.md") in bn
    assert p["ok"] >= 3                       # plan, out.txt write, /dev/null
    assert ("out", "read", "row_start_guard.py") in bn   # relative to cd'ed training_inputs: not in scope


def test_bash_sed_inplace_cp_and_tee_are_writes(cfg):
    got = aa.bash_paths("sed -i s/a/b/ /x/f.py; cp /a/src.py /b/dst.py; mv /a/m.py /b/m2.py; echo x | tee /c/t.log; rm -f /d/gone.txt", "/")
    kinds = {(k, os.path.basename(t)) for k, t, _ in got}
    assert ("write", "f.py") in kinds
    assert ("read", "src.py") in kinds and ("write", "dst.py") in kinds
    assert ("write", "m.py") in kinds and ("write", "m2.py") in kinds
    assert ("write", "t.log") in kinds and ("write", "gone.txt") in kinds


def test_heredoc_body_not_scanned(cfg):
    cmd = "cat > /a/file.py <<'EOF'\nopen('/secret/ohs5/x.json')\nEOF\nls /b/dir"
    got = [t for _, t, _ in aa.bash_paths(cmd, "/")]
    assert "/a/file.py" in got and "/b/dir" in got and not any("ohs5" in t for t in got)


def test_relative_paths_never_out_but_deny_still_hits(cfg, tmp_path):
    uses = [("Bash", {"command": "cat data/foo/bar.json application/json"}),
            ("Bash", {"command": "cat data/ohs3_parts/p.json"})]
    rep, _ = run(cfg, tmp_path, "L-A x", uses, cwd=None)
    p = rep["prefixes"]["L-A"]
    assert p["out"] == 0 and p["deny"] == 1 and p["unresolved"] >= 2


def test_search_tools_broad_vs_deny(cfg, tmp_path):
    uses = [("Grep", {"pattern": "x", "path": C21}),                    # ancestor of the allowed region
            ("Glob", {"pattern": "*.md", "path": TI + "/excerpts"}),
            ("Grep", {"pattern": "x", "path": ROOT + "/opendecide-data/lean/ohs5_sealed"}),
            ("Grep", {"pattern": "x", "path": "/somewhere/else"})]
    rep, _ = run(cfg, tmp_path, "L-C x", uses)
    p = rep["prefixes"]["L-C"]
    assert (p["broad"], p["ok"], p["deny"], p["out"]) == (1, 1, 1, 1)


def test_report_has_basenames_and_counts_only(cfg, tmp_path):
    secret = "SUPERSECRETCONTENTSTRING"
    uses = [("Bash", {"command": "echo %s > %s/c21_infra/a.txt; cat %s/C2_1_PLAN_v3.md" % (secret, C2B, C21)}),
            ("Read", {"file_path": C21 + "/C2_1_PLAN_v3.md"})]
    p = tmp_path / "t.jsonl"
    write_tr(p, "L-0 z", uses)
    # add result text containing content; it must never be printed
    with open(p, "a") as f:
        f.write(json.dumps({"type": "user", "message": {"content": [{"type": "tool_result", "content": secret + " /full/path/leak.md"}]}}) + "\n")
    stats, unm, unr, bad, n, ne = aa.audit([str(p)], cfg)
    rep = aa.summarise(stats, unm, unr, bad, n, ne, 1, cfg)
    text = aa.render(rep) + json.dumps(rep)
    assert secret not in text and C21 not in text and "/full/path" not in text
    assert "C2_1_PLAN_v3.md" in text


def test_duplicate_tool_use_ids_counted_once(cfg, tmp_path):
    p = tmp_path / "d.jsonl"
    e = tu("Read", {"file_path": C21 + "/C2_1_PLAN_v3.md"}, 1)
    e["agentLabel"] = "L-0 a"
    p.write_text(json.dumps(e) + "\n" + json.dumps(e) + "\n")
    stats, unm, unr, bad, n, _ = aa.audit([str(p)], cfg)
    assert n == 1 and stats["L-0"]["verdict"]["deny"] == 1


def test_label_from_label_map_and_stem(cfg, tmp_path):
    p = tmp_path / "agent-abc.jsonl"
    p.write_text(json.dumps(tu("Read", {"file_path": TI + "/LANE_L-I.md"}, 1)) + "\n")
    cfg2 = aa.Config(dict(json.load(open(CFG_PATH)), label_map={"agent-abc": "L-I t41c"}))
    stats, unm, _, _, _, _ = aa.audit([str(p)], cfg2)
    assert stats["L-I"]["verdict"]["ok"] == 1 and not unm
    stats, unm, _, _, _, _ = aa.audit([str(p)], cfg)
    assert unm["agent-abc"] == 1


def test_bad_lines_counted_json_array_supported(cfg, tmp_path):
    p = tmp_path / "bad.jsonl"
    p.write_text("not json\n" + json.dumps(tu("Read", {"file_path": TI + "/LANE_L-I.md"}, 1)) + "\n")
    _, _, _, bad, n, _ = aa.audit([str(p)], cfg, label_override="L-I x")
    assert bad == 1 and n == 1
    q = tmp_path / "arr.json"
    q.write_text(json.dumps([tu("Read", {"file_path": TI + "/LANE_L-I.md"}, 1)]))
    _, _, _, bad, n, _ = aa.audit([str(q)], cfg, label_override="L-I x")
    assert bad == 0 and n == 1


def test_directory_discovery_skips_data_ohs3_and_ohs3_parts(tmp_path):
    root = tmp_path / "wf"
    for rel in ["a.jsonl", "sub/b.jsonl", "data/ohs3_parts/c.jsonl", "data/sealed/d.jsonl", "ohs3_parts/e.jsonl",
                "agent-sealed-lane.jsonl", "x.meta.json"]:
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("")
    got = sorted(os.path.relpath(p, str(root)) for p in aa.find_transcripts(str(root)))
    assert got == ["a.jsonl", "agent-sealed-lane.jsonl", "sub/b.jsonl"]


def test_cli_exit_codes_and_json(cfg, tmp_path, capsys):
    p = tmp_path / "t.jsonl"
    write_tr(p, "L-0 ok", [("Read", {"file_path": TI + "/LANE_L-0.md"})])
    assert aa.main([str(p), "--config", CFG_PATH]) == 0
    assert "RESULT: CLEAN" in capsys.readouterr().out
    write_tr(p, "L-0 bad", [("Read", {"file_path": C21 + "/C2_1_PLAN_v3.md"})])
    assert aa.main([str(p), "--config", CFG_PATH, "--json"]) == 1
    rep = json.loads(capsys.readouterr().out)
    assert rep["prefixes"]["L-0"]["deny"] == 1
    assert aa.main([str(tmp_path / "missing.jsonl"), "--config", CFG_PATH]) == 2


def test_config_rejects_unknown_scope():
    with pytest.raises(aa.ConfigError):
        aa.Config({"scopes": {}, "agents": [{"prefix": "X", "scope": "nope"}]})


def test_shipped_config_scopes_load(cfg):
    for a in cfg.agents:
        if a["scope"] != "unrestricted":
            assert cfg.scope_for(a).allow_read


# ------------------------------------------------------------------ skeptic round: reads the first version missed
def verdicts(cfg, label, tool, inp, cwd=ROOT):
    sc = cfg.scope_for(cfg.agent_for(label))
    return [(k, aa.safe_base(raw), aa.judge(sc, k, raw, c, s, m)) for k, raw, s, c, m in aa.accesses_of(tool, inp, cwd)]


def worst(cfg, label, cmd, tool="Bash", cwd=ROOT, key="command"):
    vs = [v for _, _, v in verdicts(cfg, label, tool, {key: cmd}, cwd)]
    return max(vs, key=lambda v: aa._SEV[v]) if vs else None


PLAN = C21 + "/C2_1_PLAN_v3.md"


@pytest.mark.parametrize("cmd", [
    "cat " + PLAN,
    "cat " + PLAN.replace("C2_1_PLAN_v3", "c2_1_plan_V3"),                     # APFS is case-insensitive
    "cat " + C21 + "/C2_1_PLAN*",
    "cat " + C21 + "/*PLAN*.md",
    "grep -n x " + C21 + "/C2_1_PLAN_v?.md",
    "cat " + C21 + "/C2_1_PLAN_v[0-9].md",
    "cat " + C21 + "/{C2_1_PLAN_v3.md,README.md}",
    "ls " + C21 + "/research_v3/*",
    "cat " + TI + "/../C2_1_PLAN_v3.md",
    "cat " + TI + "/excerpts/../../C2_1_PLAN_v3.md",
    "cat $C21/C2_1_PLAN_v3.md",
    'cat "${C21}/research_v3/permission.md"',
    "cat opendecide-data/lean/c2_build/zed_orch/c21/C2_1_PLAN_v3.md",
    "cat zed_orch/c21/research_v3/x.md",
    "git show HEAD:opendecide-data/lean/c2_build/zed_orch/c21/C2_1_PLAN_v3.md",
    "cat \\\n  /Users/x/ohs5_sealed/f.json",
    'bash -c "cat /Users/x/ohs5_sealed/f.json"',
    "sh -lc 'cat /Users/x/ohs5_sealed/f.json'",
    'echo "$(cat /Users/x/ohs5_sealed/f.json)"',
    "echo `cat /Users/x/ohs5_sealed/f.json`",
    "eval 'cat /Users/x/ohs5_sealed/f.json'",
    "python3 -c \"print(open('/Users/x/ohs5_sealed/f.json').read())\"",
    "node -e \"require('fs').readFileSync('/Users/x/ohs5_sealed/f.json')\"",
    "python3 - <<'EOF'\nimport json\nopen('/Users/x/ohs5_sealed/f.json')\nEOF",
    "bash <<'EOF'\ncat /Users/x/ohs5_sealed/f.json\nEOF",
    'cat "/Users/x/my ohs dir/f.json"',
    "head -n 5 < " + PLAN,
    "dd if=" + PLAN + " of=/dev/null",
    "cp " + PLAN + " /private/tmp/claude-501/x",
    "ln -s " + PLAN + " /private/tmp/claude-501/l",
    "for f in " + C21 + "/research_v3/*; do cat $f; done",
    "cd " + C21 + " && cat C2_1_PLAN_v3.md",
    "cd " + C21 + "/research_v3 && ls",
    "cat /Users/x/ohs5_sealed/f.json | head",
    "/Users/x/ohs5_sealed/run.sh",
    "CONFIG=/Users/x/ohs5_sealed/c.json python3 run.py",
    "export CONFIG=/Users/x/ohs5_sealed/c.json",
    "xargs -a /Users/x/ohs5_sealed/list.txt cat",
])
def test_bash_read_forms_that_reach_a_denied_path(cfg, cmd):
    assert worst(cfg, "L-A x", cmd) == "deny", cmd


@pytest.mark.parametrize("cmd", [
    "cat " + TI + "/LANE_L-A.md",
    "cat " + TI + "/excerpts/*.md",
    "ls " + TI + "/excerpts/*",
    "cat $HOME/notes.txt",
    "python3 -c \"print(1+1)\"",
    "python3 -c \"import re; re.compile('ohs')\"",             # a bare string without a path is not a read
    "cat > /private/tmp/claude-501/f.py <<'EOF'\nopen('/Users/x/ohs5_sealed/f.json')\nEOF",   # writing code is not reading
    "git status --short | head -5",
    "echo hi > /private/tmp/claude-501/x.txt",
])
def test_bash_forms_that_are_not_findings(cfg, cmd):
    assert worst(cfg, "L-A x", cmd) in (None, "ok", "dynamic", "unresolved"), cmd


def test_wildcards_inside_scope_stay_ok_for_l0(cfg):
    assert worst(cfg, "L-0 x", "wc -l %s/c21_infra/*.py" % C2B) == "ok"
    assert worst(cfg, "L-0 x", "cd %s && python3 -m pytest c21_infra/tests -q 2>&1 | tail -5" % C2B) == "ok"


@pytest.mark.parametrize("cmd", [
    "grep -rn needle .", "grep -r needle", "rg needle", "find . -name x", "ls", "tree", "git grep needle",
])
def test_search_without_operand_is_a_broad_root(cfg, cmd):
    assert worst(cfg, "L-A x", cmd) == "broad", cmd


def test_unknown_cwd_search_root_is_broad_not_silent(cfg):
    assert worst(cfg, "L-A x", "ls", cwd=None) == "broad"
    assert verdicts(cfg, "L-A x", "Grep", {"pattern": "x"}, cwd=None)[0][2] == "broad"


@pytest.mark.parametrize("tool,inp", [
    ("Monitor", {"command": "tail -f " + PLAN}),
    ("mcp__terminal__run_in_terminal", {"command": "cat " + PLAN}),
    ("Artifact", {"file_path": PLAN}),
    ("Artifact", {"file_path": "/x/page.html", "files": {"a.js": PLAN}}),
    ("Artifact", {"file_path": "/x/page.html", "files": [{"path": PLAN}]}),
    ("SomeNewTool", {"paths": [PLAN]}),
    ("WebFetch", {"url": "file://" + PLAN}),
])
def test_unknown_tools_with_commands_or_paths_are_audited(cfg, tool, inp):
    assert max((v for _, _, v in verdicts(cfg, "L-A x", tool, inp)), key=lambda v: aa._SEV[v]) == "deny"


def test_glob_and_grep_patterns_are_joined_to_the_root(cfg):
    assert verdicts(cfg, "L-A x", "Glob", {"pattern": "**/*sealed*", "path": ROOT})[0][2] == "deny"
    assert verdicts(cfg, "L-A x", "Glob", {"pattern": C21 + "/research_v3/*.md"})[0][2] == "deny"
    assert verdicts(cfg, "L-A x", "Grep", {"pattern": "x", "path": ROOT, "glob": "*sealed*"})[0][2] == "deny"
    assert verdicts(cfg, "L-A x", "Grep", {"pattern": "x", "path": TI + "/excerpts", "glob": "*.md"})[0][2] == "ok"
    assert verdicts(cfg, "L-A x", "Grep", {"pattern": "x", "path": C21 + "/research_v3"})[0][2] == "deny"


def test_broad_search_roots_make_the_run_a_finding(cfg, tmp_path):
    rep, _ = run(cfg, tmp_path, "L-C x", [("Grep", {"pattern": "x", "path": C21})])
    assert rep["prefixes"]["L-C"]["broad"] == 1 and rep["findings_present"]
    assert aa.main([str(tmp_path / "t1.jsonl"), "--config", CFG_PATH]) == 1


def test_heredoc_to_a_non_interpreter_is_not_scanned_but_unterminated_is_rescanned(cfg):
    ok_cmd = "cat > /private/tmp/claude-501/f.py <<'EOF'\nopen('/Users/x/ohs5_sealed/f.json')\nEOF\nls /private/tmp/claude-501"
    assert not any(m == "inline" for *_, m in aa.bash_accesses(ok_cmd, "/"))
    swallowed = 'echo "a <<foo"\ncat /Users/x/ohs5_sealed/f.json'
    assert worst(cfg, "L-A x", swallowed) == "deny"
    herestring = "cat <<< hello\ncat /Users/x/ohs5_sealed/f.json"
    assert worst(cfg, "L-A x", herestring) == "deny"


def test_symlink_inside_allowed_area_pointing_at_denied_path(cfg, tmp_path):
    real = tmp_path / "ohs_real"
    real.mkdir()
    (real / "f.json").write_text("{}")
    os.symlink(str(real), str(tmp_path / "innocent"))
    cfg2 = aa.Config(json.load(open(CFG_PATH)), {"SCRATCH": str(tmp_path)})
    sc = cfg2.scope_for(cfg2.agent_for("L-A x"))
    assert aa.judge(sc, "read", str(tmp_path / "innocent" / "f.json"), ROOT, False, "path") == "deny"
    assert aa.judge(sc, "read", str(tmp_path / "plain.txt"), ROOT, False, "path") == "ok"


def test_var_override_narrows_the_scratch_area(cfg, tmp_path):
    cfg2 = aa.Config(json.load(open(CFG_PATH)), {"SCRATCH": "/private/tmp/claude-501/-proj/sessionA"})
    sc = cfg2.scope_for(cfg2.agent_for("L-A x"))
    assert aa.judge(sc, "read", "/private/tmp/claude-501/-proj/sessionA/x.txt", ROOT, False, "path") == "ok"
    assert aa.judge(sc, "read", "/private/tmp/claude-501/-proj/sessionB/x.txt", ROOT, False, "path") == "out"
    p = tmp_path / "t.jsonl"
    write_tr(p, "L-A z", [("Read", {"file_path": "/private/tmp/claude-501/-proj/sessionB/x.txt"})])
    assert aa.main([str(p), "--config", CFG_PATH, "--var", "SCRATCH=/private/tmp/claude-501/-proj/sessionA"]) == 1
    assert aa.main([str(p), "--config", CFG_PATH]) == 0


def test_pretty_printed_json_transcript_and_unparsed_lines_are_not_silent(cfg, tmp_path, capsys):
    q = tmp_path / "pretty.json"
    q.write_text(json.dumps(tu("Read", {"file_path": PLAN}, 1), indent=2))
    _, _, _, bad, n, _ = aa.audit([str(q)], cfg, label_override="L-A x")
    assert bad == 0 and n == 1
    p = tmp_path / "torn.jsonl"
    p.write_text(json.dumps(tu("Read", {"file_path": TI + "/LANE_L-A.md"}, 1)) + "\n" + '{"type": "assistant", "mess')
    assert aa.main([str(p), "--config", CFG_PATH, "--label", "L-A x"]) == 1
    out = capsys.readouterr().out
    assert "INCOMPLETE" in out and "RESULT: INCOMPLETE" in out


def test_transcript_without_any_tool_use_is_reported(cfg, tmp_path, capsys):
    p = tmp_path / "other_format.jsonl"
    p.write_text(json.dumps({"role": "assistant", "text": "hi"}) + "\n")
    stats, unm, unr, bad, n, ne = aa.audit([str(p)], cfg, label_override="L-A x")
    assert n == 0 and ne == 1
    assert "transcripts_without_tool_use=1" in aa.render(aa.summarise(stats, unm, unr, bad, n, ne, 1, cfg))


def test_dynamic_and_inline_findings_print_only_basenames(cfg, tmp_path):
    uses = [("Bash", {"command": "cat $SECRETROOT/ohs5_sealed/hidden_name.json"}),
            ("Bash", {"command": "python3 -c \"open('/Users/x/ohs5_sealed/other_name.json')\""})]
    rep, _ = run(cfg, tmp_path, "L-A y", uses)
    text = aa.render(rep) + json.dumps(rep)
    assert "hidden_name.json" in text and "other_name.json" in text
    assert "SECRETROOT" not in text and "/Users/x" not in text
    assert rep["prefixes"]["L-A"]["deny"] == 2


def test_cd_in_one_bash_call_carries_to_the_next_call(cfg, tmp_path):
    # no cwd field in the transcript: only the cd of the first call can tell where x.md is
    uses = [("Bash", {"command": "cd " + C21 + "/research_v3"}), ("Bash", {"command": "cat x.md"})]
    rep, _ = run(cfg, tmp_path, "L-A x", uses, cwd=None)
    assert rep["prefixes"]["L-A"]["deny"] == 1
    uses = [("Bash", {"command": "cat x.md"})]
    rep, _ = run(cfg, tmp_path, "L-A x", uses, cwd=None)
    assert rep["prefixes"]["L-A"]["deny"] == 0
