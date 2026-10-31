import os

import pathskip as ps


def _touch(root, rel):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        f.write("{}")
    return p


def _tree(tmp_path):
    root = str(tmp_path)
    for rel in [
        "data/keep/a.json", "data/keep/sub/b.json", "data/c2_parts/c.json",
        "data/ohs3/x.json", "data/ohs3_x/x.json", "data/OHS3-final/x.json", "data/ohs3_parts/p.json",
        "data/ohs5/x.json", "data/ohs_ac/x.json", "data/sealed/x.json", "data/pre_Sealed_stuff/x.json",
        "data/keep/ohs3_notes.json", "data/keep/SEALED.json",
        "other/ohs3_parts/y.json",
    ]:
        _touch(root, rel)
    return root


def test_data_glob_skips_ohs3_ohs_and_sealed(tmp_path):
    root = _tree(tmp_path)
    hits = sorted(os.path.relpath(p, root) for p in ps.safe_glob(root, "data/**/*.json"))
    assert hits == ["data/c2_parts/c.json", "data/keep/a.json", "data/keep/sub/b.json"]


def test_ohs3_parts_skipped_outside_data_too(tmp_path):
    root = _tree(tmp_path)
    assert ps.safe_glob(root, "**/y.json") == []
    assert ps.safe_glob(root, "other/**") == []


def test_top_level_double_star(tmp_path):
    root = _tree(tmp_path)
    got = [os.path.relpath(p, root) for p in ps.safe_glob(root, "**/*.json")]
    assert "data/keep/a.json" in got
    assert not any("ohs" in g.lower() or "sealed" in g.lower() for g in got)


def test_only_below_data_mode_keeps_lane_named_transcripts(tmp_path):
    root = str(tmp_path)
    _touch(root, "wf/agent-L-S-sealed-brief.jsonl")      # legit transcript name outside data/
    _touch(root, "wf/data/ohs3_parts/t.jsonl")           # data glob: skipped
    _touch(root, "wf/data/sealed/t.jsonl")               # below data: skipped
    _touch(root, "wf/ohs3_parts/t.jsonl")                # ohs3_parts anywhere: skipped
    got = sorted(os.path.relpath(p, root) for p in ps.safe_walk(root, only_below_data=True))
    assert got == ["wf/agent-L-S-sealed-brief.jsonl"]


def test_is_skipped_rel_cases():
    assert ps.is_skipped_rel(["data", "ohs3_v1", "f"])
    assert ps.is_skipped_rel(["data", "ohs3_parts"])
    assert ps.is_skipped_rel(["x", "OHS5_Sealed", "f"])
    assert not ps.is_skipped_rel(["data", "c2_parts", "f"])
    assert not ps.is_skipped_rel(["wf", "sealed.jsonl"], only_below_data=True)
    assert ps.is_skipped_rel(["wf", "data", "sealed.jsonl"], only_below_data=True)


def test_symlinked_dirs_not_followed(tmp_path):
    root = str(tmp_path)
    _touch(root, "real/a.json")
    os.symlink(os.path.join(root, "real"), os.path.join(root, "link"))
    got = [os.path.relpath(p, root) for p in ps.safe_walk(root)]
    assert got == ["real/a.json"]


def test_glob_regex_semantics():
    rx = ps.glob_to_regex("a/**")
    assert rx.match("a") and rx.match("a/b/c") and not rx.match("ab")
    rx = ps.glob_to_regex("a/**/c.txt")
    assert rx.match("a/c.txt") and rx.match("a/x/y/c.txt") and not rx.match("a/x/c.txt2")
    rx = ps.glob_to_regex("*.json")
    assert rx.match("a.json") and not rx.match("d/a.json")


def test_is_skipped_path_checks_every_component(tmp_path):
    assert ps.is_skipped_path("/a/b/c/d/e/f/ohs5/x.json")
    assert ps.is_skipped_path("/a/Sealed_x/b.json")
    assert not ps.is_skipped_path("/a/b/c/d/e/f/g/x.json")
    # the system temp prefix (random folder names) never bars a path by accident
    import tempfile
    t = os.path.join(os.path.realpath(tempfile.gettempdir()), "ok_dir", "job.json")
    assert not ps.is_skipped_path(t)
    assert ps.is_skipped_path(os.path.join(os.path.realpath(tempfile.gettempdir()), "ohs_dir", "job.json"))


def test_temp_prefix_with_ohs_in_its_random_name_does_not_bar(monkeypatch, tmp_path):
    import tempfile
    fake = os.path.join(str(tmp_path), "xohsx", "T")
    os.makedirs(fake)
    monkeypatch.setattr(tempfile, "gettempdir", lambda: fake)
    assert not ps.is_skipped_path(os.path.join(fake, "run1", "job.json"))
    assert ps.is_skipped_path(os.path.join(fake, "run1", "sealed", "job.json"))


def test_symlink_named_innocently_into_a_barred_dir_is_barred(tmp_path):
    bad = tmp_path / "ohs5_real"
    bad.mkdir()
    (bad / "job.json").write_text("{}")
    os.symlink(str(bad), str(tmp_path / "plain_link"))
    assert ps.is_skipped_path(str(tmp_path / "plain_link" / "job.json"))
    os.symlink(str(bad / "job.json"), str(tmp_path / "job_link.json"))
    assert ps.is_skipped_path(str(tmp_path / "job_link.json"))
    (tmp_path / "fine.json").write_text("{}")
    assert not ps.is_skipped_path(str(tmp_path / "fine.json"))
