import hashlib
import json
import os
import sys

import pytest

import row_start_guard as g

SHA_A = "a" * 64


def _w(path, obj):
    with open(path, "w") as f:
        json.dump(obj, f)
    return str(path)


def _sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def _fz(d, obj, sub="fz"):
    """A freeze record: the guard only accepts a file named OHS5_FREEZE.json."""
    (d / sub).mkdir(exist_ok=True)
    return _w(d / sub / "OHS5_FREEZE.json", obj)


ALLOW = {"frozen": True, "version": "v1", "row_job_families_allowed": ["FAM_A", "FAM_B"], "names": {
    "policy": ["pol_a", "pol_b"], "tool": ["tool_a"], "language": ["python", "go"],
    "runner": ["pytest"], "carrier": ["json", "yaml"]}}
JOB = {"job_id": "job1", "family": "FAM_A", "names": {"policy": ["pol_a"], "tool": ["tool_a"], "language": ["go"],
                                     "runner": ["pytest"], "carrier": ["json"]}}


@pytest.fixture
def env(tmp_path):
    d = tmp_path
    reg = d / "registry.json"
    reg.write_text('{"targets": ["t1"]}')
    return {
        "freeze": _fz(d, {"sha": SHA_A, "other": "ignored"}),
        "registry": str(reg),
        "registry_sha": _sha(reg),
        "allowlist": _w(d / "allow.json", ALLOW),
        "allowlist_sha": _sha(d / "allow.json"),
        "manifest": _w(d / "job.json", JOB),
        "dir": d,
    }


def run(env, **over):
    kw = dict(manifests=[env["manifest"]], allowlist=env["allowlist"], registry=env["registry"],
              registry_sha=env["registry_sha"], freeze=env["freeze"], freeze_sha=SHA_A,
              allowlist_sha=env["allowlist_sha"])
    if "allowlist" in over and "allowlist_sha" not in over and os.path.isfile(over["allowlist"]):
        kw["allowlist_sha"] = _sha(over["allowlist"])
    if "freeze" in over and "freeze_sha" not in over:
        kw["freeze_sha"] = None
        try:
            kw["freeze_sha"] = json.load(open(over["freeze"])).get("sha") or json.load(open(over["freeze"])).get("sha256")
        except (OSError, ValueError, AttributeError):
            pass
    kw.update(over)
    return g.evaluate(**kw)


def test_all_good(env):
    ok, reasons, facts = run(env)
    assert ok and reasons == []
    assert facts["freeze_sha"] == SHA_A and facts["registry_sha"] == env["registry_sha"]


def test_missing_freeze_refuses(env):
    ok, reasons, _ = run(env, freeze=str(env["dir"] / "fz" / "gone" / "OHS5_FREEZE.json"))
    assert not ok and reasons[0].startswith("FREEZE_MISSING")


def test_freeze_without_sha_or_bad_sha(env):
    ok, r, _ = run(env, freeze=_fz(env["dir"], {"x": 1}, "f2"), freeze_sha=SHA_A)
    assert not ok and r[0].startswith("FREEZE_NO_SHA")
    ok, r, _ = run(env, freeze=_fz(env["dir"], {"sha": "xyz"}, "f3"), freeze_sha=SHA_A)
    assert not ok and r[0].startswith("FREEZE_NO_SHA")
    (env["dir"] / "f4").mkdir()
    (env["dir"] / "f4" / "OHS5_FREEZE.json").write_text("not json")
    ok, r, _ = run(env, freeze=str(env["dir"] / "f4" / "OHS5_FREEZE.json"), freeze_sha=SHA_A)
    assert not ok and r[0].startswith("FREEZE_UNREADABLE")
    (env["dir"] / "f5").mkdir()
    (env["dir"] / "f5" / "OHS5_FREEZE.json").write_text('{"sha": "%s", "sha": "%s"}' % (SHA_A, "b" * 64))
    ok, r, _ = run(env, freeze=str(env["dir"] / "f5" / "OHS5_FREEZE.json"), freeze_sha=SHA_A)
    assert not ok and r[0].startswith("FREEZE_UNREADABLE")


def test_freeze_sha_field_alias_and_pin(env):
    f = _fz(env["dir"], {"sha256": SHA_A}, "f6")
    assert run(env, freeze=f)[0]
    ok, r, _ = run(env, freeze=f, freeze_sha="b" * 64)
    assert not ok and r[0].startswith("FREEZE_SHA_MISMATCH")


def test_freeze_must_be_pinned_and_named_right(env):
    # a hand-made record with a well-formed sha does not pass unless the orchestrator pinned that exact sha
    ok, r, _ = run(env, freeze_sha=None)
    assert not ok and r[0].startswith("FREEZE_SHA_NOT_PINNED")
    ok, r, _ = run(env, freeze_sha="nothex")
    assert not ok and r[0].startswith("FREEZE_SHA_MALFORMED")
    ok, r, _ = run(env, freeze_sha="b" * 64)
    assert not ok and r[0].startswith("FREEZE_SHA_MISMATCH")
    # the guard can never be pointed at any other file (e.g. another sealed record)
    other = _w(env["dir"] / "OTHER_RECORD.json", {"sha": SHA_A})
    ok, r, _ = run(env, freeze=other, freeze_sha=SHA_A)
    assert not ok and r[0].startswith("FREEZE_PATH_WRONG")
    # an oversized record is refused unread
    big = env["dir"] / "big"
    big.mkdir()
    (big / "OHS5_FREEZE.json").write_text('{"sha": "%s", "pad": "%s"}' % (SHA_A, "x" * (g.MAX_FREEZE_BYTES + 10)))
    ok, r, _ = run(env, freeze=str(big / "OHS5_FREEZE.json"), freeze_sha=SHA_A)
    assert not ok and r[0].startswith("FREEZE_UNREADABLE")


def test_registry_sha_must_be_pinned_and_match(env):
    ok, r, _ = run(env, registry_sha=None)
    assert not ok and r[0].startswith("REGISTRY_SHA_NOT_PINNED")
    ok, r, _ = run(env, registry_sha="b" * 64)
    assert not ok and r[0].startswith("REGISTRY_SHA_MISMATCH")
    ok, r, _ = run(env, registry_sha="nothex")
    assert not ok and r[0].startswith("REGISTRY_SHA_MALFORMED")
    ok, r, _ = run(env, registry=str(env["dir"] / "gone.json"))
    assert not ok and r[0].startswith("REGISTRY_MISSING")
    # registry edited after pinning
    with open(env["registry"], "a") as f:
        f.write(" ")
    ok, r, _ = run(env)
    assert not ok and r[0].startswith("REGISTRY_SHA_MISMATCH")


@pytest.mark.parametrize("cat,bad", [("policy", "pol_zzz"), ("tool", "tool_x"), ("language", "rust"),
                                     ("runner", "unittest"), ("carrier", "xml")])
def test_each_category_name_off_allowlist_refuses(env, cat, bad):
    job = json.loads(json.dumps(JOB))
    job["names"][cat].append(bad)
    m = _w(env["dir"] / "job_bad.json", job)
    ok, r, _ = run(env, manifests=[m])
    assert not ok
    assert any(x.startswith("NAME_OFF_ALLOWLIST") and bad in x for x in r)


def test_case_and_near_miss_names_refused(env):
    job = {"names": {"policy": ["Pol_A"], "tool": ["tool_a "]}}
    ok, r, _ = run(env, manifests=[_w(env["dir"] / "j.json", job)])
    assert not ok and len([x for x in r if x.startswith("NAME_OFF")]) == 2


def test_unknown_category_refused(env):
    job = {"names": {"policy": ["pol_a"], "company": ["Foo"]}}
    ok, r, _ = run(env, manifests=[_w(env["dir"] / "j.json", job)])
    assert not ok and any(x.startswith("UNKNOWN_CATEGORY") for x in r)


def test_empty_or_missing_names_refused(env):
    for obj in ({"job_id": "x"}, {"names": {}}):
        ok, r, _ = run(env, manifests=[_w(env["dir"] / "j.json", obj)])
        assert not ok and any(x.startswith("NAMES_MISSING") for x in r)
    ok, r, _ = run(env, manifests=[])
    assert not ok and any(x.startswith("MANIFEST_MISSING") for x in r)


def test_per_row_names_checked(env):
    job = dict(JOB, rows=[{"row_id": "r1", "names": {"tool": ["tool_a"]}},
                          {"row_id": "r2", "names": {"tool": ["sneaky_tool"]}}])
    ok, r, _ = run(env, manifests=[_w(env["dir"] / "j.json", job)])
    assert not ok and any("row r2" in x and "sneaky_tool" in x for x in r)
    assert not any("row r1" in x for x in r)


def test_allowlist_must_be_frozen_complete_and_pinnable(env):
    ok, r, _ = run(env, allowlist=_w(env["dir"] / "a2.json", dict(ALLOW, frozen=False)))
    assert not ok and any(x.startswith("ALLOWLIST_NOT_FROZEN") for x in r)
    partial = {"frozen": True, "names": {"policy": ["pol_a"]}}
    ok, r, _ = run(env, allowlist=_w(env["dir"] / "a3.json", partial))
    assert not ok and any(x.startswith("ALLOWLIST_INCOMPLETE") for x in r)
    ok, r, _ = run(env, allowlist_sha="c" * 64)
    assert not ok and any(x.startswith("ALLOWLIST_SHA_MISMATCH") for x in r)
    ok, r, _ = run(env, allowlist_sha=None)
    assert not ok and any(x.startswith("ALLOWLIST_SHA_NOT_PINNED") for x in r)
    ok, r, _ = run(env, allowlist_sha="zz")
    assert not ok and any(x.startswith("ALLOWLIST_SHA_MALFORMED") for x in r)
    assert run(env, allowlist_sha=_sha(env["allowlist"]))[0]
    # editing the list after it was pinned (to add the off-list name) is caught
    edited = json.loads(json.dumps(ALLOW))
    edited["names"]["tool"].append("sneaky_tool")
    _w(env["dir"] / "allow.json", edited)
    job = json.loads(json.dumps(JOB))
    job["names"]["tool"].append("sneaky_tool")
    ok, r, _ = run(env, manifests=[_w(env["dir"] / "j.json", job)], allowlist_sha=env["allowlist_sha"])
    assert not ok and any(x.startswith("ALLOWLIST_SHA_MISMATCH") for x in r)
    ok, r, _ = run(env, allowlist=str(env["dir"] / "none.json"))
    assert not ok and any(x.startswith("ALLOWLIST_MISSING") for x in r)


def test_barred_manifest_path_refused(env):
    d = env["dir"] / "ohs5_stuff"
    d.mkdir()
    m = _w(d / "job.json", JOB)
    ok, r, _ = run(env, manifests=[m])
    assert not ok and any(x.startswith("MANIFEST_PATH_BARRED") for x in r)


def test_barred_path_is_checked_on_every_component_not_just_the_last_four(env):
    deep = env["dir"] / "Sealed_dir" / "a" / "b" / "c" / "d" / "e"
    deep.mkdir(parents=True)
    ok, r, _ = run(env, manifests=[_w(deep / "job.json", JOB)])
    assert not ok and any(x.startswith("MANIFEST_PATH_BARRED") for x in r)
    # the allow-list and the registry are held to the same rule
    d2 = env["dir"] / "x" / "ohs_stuff" / "y"
    d2.mkdir(parents=True)
    a = _w(d2 / "allow.json", ALLOW)
    ok, r, _ = run(env, allowlist=a, allowlist_sha=_sha(a))
    assert not ok and any(x.startswith("ALLOWLIST_PATH_BARRED") for x in r)
    reg = d2 / "registry.json"
    reg.write_text('{"targets": []}')
    ok, r, _ = run(env, registry=str(reg), registry_sha=_sha(reg))
    assert not ok and any(x.startswith("REGISTRY_PATH_BARRED") for x in r)


def test_duplicate_json_keys_refused(env):
    m = env["dir"] / "dup.json"
    m.write_text('{"names": {"tool": ["tool_a"], "tool": ["not_on_list"]}}')
    ok, r, _ = run(env, manifests=[str(m)])
    assert not ok and any(x.startswith("MANIFEST_UNREADABLE") for x in r)
    al = env["dir"] / "dup_allow.json"
    al.write_text('{"frozen": true, "frozen": false, "names": {}}')
    ok, r, _ = run(env, allowlist=str(al))
    assert not ok and any(x.startswith("ALLOWLIST_UNREADABLE") for x in r)


def test_job_must_declare_all_five_categories_and_some_name(env):
    partial = {"job_id": "p", "names": {"policy": ["pol_a"]}}
    ok, r, _ = run(env, manifests=[_w(env["dir"] / "p.json", partial)])
    assert not ok and sum(x.startswith("NAMES_INCOMPLETE") for x in r) == 4
    unused = {"job_id": "u", "family": "FAM_A", "names": {"policy": ["pol_a"], "tool": [], "language": [], "runner": [], "carrier": []}}
    assert run(env, manifests=[_w(env["dir"] / "u.json", unused)])[0]
    empty = {"job_id": "e", "family": "FAM_A", "names": {c: [] for c in g.CATEGORIES}}
    ok, r, _ = run(env, manifests=[_w(env["dir"] / "e.json", empty)])
    assert not ok and any(x.startswith("NAMES_EMPTY") for x in r)


def test_freeze_record_other_fields_not_returned(env):
    _, _, facts = run(env)
    assert set(facts) == {"freeze_sha", "registry_sha", "allowlist_sha", "manifest_0_sha"}
    assert "ignored" not in json.dumps(facts)


def test_require_start_raises(env):
    with pytest.raises(g.GuardRefused):
        g.require_start([env["manifest"]], env["allowlist"], env["registry"], None, env["freeze"], env["allowlist_sha"], SHA_A)
    facts = g.require_start([env["manifest"]], env["allowlist"], env["registry"], env["registry_sha"], env["freeze"],
                            env["allowlist_sha"], SHA_A)
    assert facts["freeze_sha"] == SHA_A


def _cli(env, extra=()):
    return ["--manifest", env["manifest"], "--allowlist", env["allowlist"], "--registry", env["registry"],
            "--registry-sha", env["registry_sha"], "--freeze", env["freeze"], "--freeze-sha", SHA_A,
            "--allowlist-sha", env["allowlist_sha"], *extra]


def test_cli_codes_and_output(env, capsys):
    assert g.main(_cli(env)) == 0
    assert "ROW START ALLOWED" in capsys.readouterr().out
    os.remove(env["freeze"])
    assert g.main(_cli(env)) == 1
    assert "ROW START REFUSED" in capsys.readouterr().out


def test_cli_manifest_glob_skips_ohs_and_sealed_dirs(env, capsys):
    root = env["dir"] / "gl"
    (root / "data" / "ok").mkdir(parents=True)
    (root / "data" / "ohs3_parts").mkdir(parents=True)
    (root / "data" / "sealed_x").mkdir(parents=True)
    _w(root / "data" / "ok" / "job_a.json", JOB)
    _w(root / "data" / "ohs3_parts" / "job_b.json", {"names": {"tool": ["not_on_list"]}})
    _w(root / "data" / "sealed_x" / "job_c.json", {"names": {"tool": ["not_on_list"]}})
    argv = ["--manifest-glob", "data/**/job_*.json", "--root", str(root), "--allowlist", env["allowlist"],
            "--registry", env["registry"], "--registry-sha", env["registry_sha"], "--freeze", env["freeze"],
            "--freeze-sha", SHA_A, "--allowlist-sha", env["allowlist_sha"]]
    assert g.main(argv) == 0
    assert "manifests=1" in capsys.readouterr().out


def test_cli_exec_runs_only_after_pass(env, tmp_path):
    import subprocess
    marker = tmp_path / "ran.txt"
    script = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "row_start_guard.py")
    cmd = [sys.executable, "-I", script, *_cli(env), "--exec", "--", sys.executable, "-c",
           "open(%r,'w').write('x')" % str(marker)]
    assert subprocess.run(cmd, capture_output=True).returncode == 0 and marker.exists()
    # the child receives the shas that were checked, so it can detect a file changed after the check
    envfile = tmp_path / "env.txt"
    cmd2 = [sys.executable, "-I", script, *_cli(env), "--exec", "--", sys.executable, "-c",
            "import os;open(%r,'w').write(os.environ['OD_ROWGUARD_FREEZE_SHA']+os.environ['OD_ROWGUARD_MANIFEST_0_SHA'])" % str(envfile)]
    assert subprocess.run(cmd2, capture_output=True).returncode == 0
    assert envfile.read_text() == SHA_A + _sha(env["manifest"])
    marker.unlink()
    os.remove(env["freeze"])
    r = subprocess.run(cmd, capture_output=True)
    assert r.returncode == 1 and not marker.exists()


def test_default_freeze_path_constant_points_at_the_record():
    assert g.DEFAULT_FREEZE.endswith("/lean/ohs5_sealed/OHS5_FREEZE.json")


def test_manifest_symlink_into_a_barred_dir_is_refused(env):
    real = env["dir"] / "ohs5_real"
    real.mkdir()
    _w(real / "job.json", JOB)
    os.symlink(str(real / "job.json"), str(env["dir"] / "innocent_job.json"))
    ok, r, _ = run(env, manifests=[str(env["dir"] / "innocent_job.json")])
    assert not ok and any(x.startswith("MANIFEST_PATH_BARRED") for x in r)


# ---------------------------------------------------------------- family check (L-0, PREREG A77/A79)
def _job(**over):
    j = json.loads(json.dumps(JOB))
    j.update(over)
    return j


def _fam_reasons(env, job, name="jf.json", **kw):
    ok, r, _ = run(env, manifests=[_w(env["dir"] / name, job)], **kw)
    return ok, [x for x in r if x.startswith("FAMILY")]


def test_family_on_list_passes_and_each_listed_family_is_usable(env):
    for fam in ("FAM_A", "FAM_B"):
        ok, r = _fam_reasons(env, _job(family=fam))
        assert ok and r == []


def test_family_missing_refused(env):
    j = _job()
    del j["family"]
    ok, r = _fam_reasons(env, j)
    assert not ok and r and r[0].startswith("FAMILY_MISSING")


@pytest.mark.parametrize("bad", ["FAM_C", "fam_a", "Fam_A", "FAM_A ", " FAM_A", "FAM_A\n", "FAM", "FAM_AA", "",
                                 "FAM_A/FAM_B", "T50"])
def test_family_off_list_or_near_miss_refused(env, bad):
    ok, r = _fam_reasons(env, _job(family=bad))
    assert not ok and len(r) == 1
    assert r[0].startswith("FAMILY_OFF_ALLOWLIST") or r[0].startswith("FAMILY_BAD_SHAPE")


@pytest.mark.parametrize("bad", [None, 7, True, ["FAM_A"], {"x": "FAM_A"}, 1.5])
def test_family_wrong_type_refused(env, bad):
    ok, r = _fam_reasons(env, _job(family=bad))
    assert not ok and len(r) == 1 and (r[0].startswith("FAMILY_BAD_SHAPE") or r[0].startswith("FAMILY_MISSING"))


def test_row_family_must_equal_job_family(env):
    rows = [{"row_id": "r1", "family": "FAM_A", "names": {"tool": ["tool_a"]}},
            {"row_id": "r2", "names": {"tool": ["tool_a"]}}]
    ok, r = _fam_reasons(env, _job(rows=rows))
    assert ok and r == []
    rows[1]["family"] = "FAM_B"          # on the list, but not this job's family
    ok, r = _fam_reasons(env, _job(rows=rows))
    assert not ok and len(r) == 1 and r[0].startswith("FAMILY_ROW_MISMATCH") and "r2" in r[0]
    rows[1]["family"] = "NOPE"
    ok, r = _fam_reasons(env, _job(rows=rows))
    assert not ok and r[0].startswith("FAMILY_ROW_MISMATCH")
    rows[1]["family"] = None
    ok, r = _fam_reasons(env, _job(rows=rows))
    assert not ok and r[0].startswith("FAMILY_ROW_MISMATCH")


def test_family_check_does_not_replace_the_name_check(env):
    job = _job()
    job["names"]["tool"].append("sneaky_tool")
    ok, r = _fam_reasons(env, job)
    assert not ok and r == []       # family fine, name still refuses
    ok, rr, _ = run(env, manifests=[_w(env["dir"] / "jn.json", job)])
    assert any(x.startswith("NAME_OFF_ALLOWLIST") for x in rr)


@pytest.mark.parametrize("mut,code", [
    (lambda a: a.pop("row_job_families_allowed"), "ALLOWLIST_FAMILIES_MISSING"),
    (lambda a: a.update(row_job_families_allowed=[]), "ALLOWLIST_FAMILIES_BAD_SHAPE"),
    (lambda a: a.update(row_job_families_allowed="FAM_A"), "ALLOWLIST_FAMILIES_BAD_SHAPE"),
    (lambda a: a.update(row_job_families_allowed={"FAM_A": 1}), "ALLOWLIST_FAMILIES_BAD_SHAPE"),
    (lambda a: a.update(row_job_families_allowed=["FAM_A", 3]), "ALLOWLIST_FAMILIES_BAD_SHAPE"),
    (lambda a: a.update(row_job_families_allowed=["FAM_A", ""]), "ALLOWLIST_FAMILIES_BAD_SHAPE"),
    (lambda a: a.update(row_job_families_allowed=["FAM_A", "FAM_A"]), "ALLOWLIST_FAMILIES_BAD_SHAPE"),
    (lambda a: a.update(row_job_families_allowed=None), "ALLOWLIST_FAMILIES_MISSING"),
])
def test_allowlist_without_a_usable_family_list_refuses_every_job(env, mut, code):
    a = json.loads(json.dumps(ALLOW))
    mut(a)
    ok, r, _ = run(env, allowlist=_w(env["dir"] / "af.json", a))
    assert not ok
    assert any(x.startswith(code) for x in r)
    assert any(x.startswith("FAMILY_LIST_UNAVAILABLE") for x in r)


def test_family_list_is_covered_by_the_allowlist_pin(env):
    # adding a family after the pin (to let an off-list family through) changes the file sha -> refused
    edited = json.loads(json.dumps(ALLOW))
    edited["row_job_families_allowed"].append("FAM_C")
    _w(env["dir"] / "allow.json", edited)
    ok, r, _ = run(env, manifests=[_w(env["dir"] / "jc.json", _job(family="FAM_C"))], allowlist_sha=env["allowlist_sha"])
    assert not ok and any(x.startswith("ALLOWLIST_SHA_MISMATCH") for x in r)


def test_duplicate_key_in_families_field_refused(env):
    al = env["dir"] / "dupf.json"
    al.write_text('{"frozen": true, "row_job_families_allowed": ["FAM_A"], "row_job_families_allowed": ["FAM_A", "X"], '
                  '"names": {}}')
    ok, r, _ = run(env, allowlist=str(al))
    assert not ok and any(x.startswith("ALLOWLIST_UNREADABLE") for x in r)


def test_load_allowlist_keeps_its_three_value_shape_and_new_loader_returns_families(env):
    allow, sha, why = g.load_allowlist(env["allowlist"], env["allowlist_sha"])
    assert why == [] and sha == env["allowlist_sha"] and set(allow) == set(g.CATEGORIES)
    allow2, sha2, why2, fams = g.load_allowlist_and_families(env["allowlist"], env["allowlist_sha"])
    assert (allow2, sha2, why2) == (allow, sha, why) and fams == frozenset({"FAM_A", "FAM_B"})
    # no family list: names still load (old callers), the family reason is reported
    a = json.loads(json.dumps(ALLOW))
    del a["row_job_families_allowed"]
    p = _w(env["dir"] / "nofam.json", a)
    _, _, why3, fams3 = g.load_allowlist_and_families(p, _sha(p))
    assert fams3 is None and any(x.startswith("ALLOWLIST_FAMILIES_MISSING") for x in why3)


def test_check_manifest_without_families_argument_refuses(env):
    allow, _, _ = g.load_allowlist(env["allowlist"], env["allowlist_sha"])
    out = g.check_manifest(env["manifest"], allow)       # an old-style caller that passes no families
    assert any(x.startswith("FAMILY_LIST_UNAVAILABLE") for x in out)
    allow, _, _, fams = g.load_allowlist_and_families(env["allowlist"], env["allowlist_sha"])
    assert g.check_manifest(env["manifest"], allow, fams) == []


def test_cli_refuses_a_job_with_no_or_unlisted_family(env, capsys):
    j = _job()
    del j["family"]
    m = _w(env["dir"] / "nofam_job.json", j)
    argv = _cli(env)
    argv[1] = m
    assert g.main(argv) == 1
    assert "FAMILY_MISSING" in capsys.readouterr().out
    argv[1] = _w(env["dir"] / "badfam_job.json", _job(family="T99"))
    assert g.main(argv) == 1
    assert "FAMILY_OFF_ALLOWLIST" in capsys.readouterr().out
    assert g.main(_cli(env)) == 0


def test_cli_exec_does_not_run_for_an_unlisted_family(env, tmp_path):
    import subprocess
    marker = tmp_path / "ran_fam.txt"
    script = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "row_start_guard.py")
    argv = _cli(env)
    argv[1] = _w(env["dir"] / "badfam2.json", _job(family="NOPE"))
    cmd = [sys.executable, "-I", script, *argv, "--exec", "--", sys.executable, "-c", "open(%r,'w').write('x')" % str(marker)]
    assert subprocess.run(cmd, capture_output=True).returncode == 1 and not marker.exists()


# ---- the real frozen manifest (read-only; skipped if the file is not where the build tree keeps it)
_L0 = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "zed_orch", "c21", "l0")
_REAL = os.path.join(_L0, "NAMES_MANIFEST_V1.json")
_REAL_SHA = os.path.join(_L0, "NAMES_MANIFEST_V1.sha256")
_FAMS = ["T50", "T51", "T53", "T41c", "T54", "T55", "T56", "T56g", "T42c", "T57", "GEN", "VOICE"]


@pytest.mark.skipif(not (os.path.isfile(_REAL) and os.path.isfile(_REAL_SHA)), reason="frozen manifest not present")
def test_real_frozen_manifest_family_list_loads_and_is_exact():
    pin = open(_REAL_SHA).read().split()[0]
    allow, sha, why, fams = g.load_allowlist_and_families(_REAL, pin)
    assert why == [] and sha == pin
    assert fams == frozenset(_FAMS)
    for fam in _FAMS:
        assert g.check_family(fam, fams) == []
    for bad in ("t50", "T50 ", "T58", "T40", "T42", "T56G", "gen", "voice", "L-A", ""):
        assert g.check_family(bad, fams), bad
    # the list in the file is the one the guard uses (no copy of the family names kept in the guard source)
    src = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "row_start_guard.py")).read()
    assert not any('"%s"' % f in src for f in _FAMS[1:])


@pytest.mark.skipif(not (os.path.isfile(_REAL) and os.path.isfile(_REAL_SHA)), reason="frozen manifest not present")
def test_real_manifest_end_to_end_family_gate(env):
    pin = open(_REAL_SHA).read().split()[0]
    names = {"policy": [], "tool": [], "language": ["python"], "runner": [], "carrier": []}
    ok, r, _ = run(env, allowlist=_REAL, allowlist_sha=pin,
                   manifests=[_w(env["dir"] / "real_ok.json", {"job_id": "r", "family": "T50", "names": names})])
    assert ok, r
    ok, r, _ = run(env, allowlist=_REAL, allowlist_sha=pin,
                   manifests=[_w(env["dir"] / "real_bad.json", {"job_id": "r", "family": "T58", "names": names})])
    assert not ok and any(x.startswith("FAMILY_OFF_ALLOWLIST") for x in r)
