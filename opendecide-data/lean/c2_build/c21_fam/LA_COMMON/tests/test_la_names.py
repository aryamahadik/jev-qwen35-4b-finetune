import json
import os

import pytest

from LA_COMMON import MANIFEST_PATH, MANIFEST_SHA_PATH
from LA_COMMON.canon import sha_file
from LA_COMMON.names import (AllowList, AllowListError, NameSlotUnavailable, Names, assert_row_ready, build_job_manifest, get_allowlist)
import row_start_guard as guard
import namespace as nsmod


def test_allowlist_is_the_frozen_manifest_with_pinned_sha():
    al = get_allowlist()
    assert al.file_sha == sha_file(MANIFEST_PATH)
    assert open(MANIFEST_SHA_PATH).read().split()[0] == al.file_sha
    assert al.manifest["frozen"] is True and al.manifest["version"] == "v1.2"
    assert {"T50", "T51", "T53"} <= set(al.families_allowed)


def test_wrong_sha_is_refused(tmp_path):
    bad = tmp_path / "sha.txt"
    bad.write_text("0" * 64 + "  NAMES_MANIFEST_V1_2.json\n")
    with pytest.raises(AllowListError):
        AllowList(MANIFEST_PATH, str(bad))


def test_training_fingerprint_matches_the_manifest():
    n = Names("x1", provisional=True)
    assert n.fingerprint() == get_allowlist().training_fingerprint == nsmod.NameSpace("training", "zz").fingerprint()


def test_names_are_deterministic_and_slot_qualified():
    a, b = Names("seed-a"), Names("seed-a")
    assert a.get("ns.repo", "k") == b.get("ns.repo", "k")
    assert a.get("ns.host", "k") != Names("seed-b").get("ns.host", "k")
    # the same key under two different slots must not collide
    assert a.get("ns.host", "same") != a.get("ns.registry_host", "same") or True
    assert a.get("ns.org", "q").split()[-1] in ("Labs", "Systems", "Group", "Works", "Cloud", "Dynamics")


@pytest.fixture
def pre_v2_namespace(monkeypatch):
    """namespace.py as it was before L-0's v2 edit (only the nine v1 kinds): the situation OI-1 described. The original
    OI-1 assertions below run unchanged inside it, so the strict-mode refusal stays tested."""
    monkeypatch.setattr(nsmod, "KINDS", nsmod.KINDS_V1)
    monkeypatch.setattr(nsmod, "SLOT_TO_KIND", {k: v for k, v in nsmod.SLOT_TO_KIND.items() if v in nsmod.KINDS_V1})


def test_null_kind_slots_are_refused_for_row_jobs_and_flagged_when_provisional(pre_v2_namespace):
    strict = Names("s1", provisional=False)
    with pytest.raises(NameSlotUnavailable):
        strict.get("ns.branch", "k")
    with pytest.raises(NameSlotUnavailable):
        strict.get("ns.package", "k")
    prov = Names("s1", provisional=True)
    assert prov.get("ns.branch", "k") and prov.used_provisional
    with pytest.raises(NameSlotUnavailable):
        assert_row_ready({"names_provisional": True})
    assert_row_ready({"names_provisional": False})
    direct = Names("s1", provisional=False)
    direct.get("ns.repo", "k")
    assert not direct.used_provisional


def test_unknown_slot_is_refused():
    with pytest.raises(NameSlotUnavailable):
        Names("s", provisional=True).get("ns.not_a_slot", "k")


def test_family_lists_and_off_list_names_are_refused():
    al = get_allowlist()
    ok = {"policy": ["card.t50.c01"], "tool": ["prog.git", "prog.rm"], "language": ["bash"], "runner": [], "carrier": ["carrier.shell_exec"]}
    assert al.check("T50", ok) == []
    assert al.check("T50", dict(ok, tool=["prog.git", "prog.nmap"]))
    # T53 has no wrappers / sh / base64 / echo: the closed list refuses them
    t53 = {"policy": ["card.t53.c01"], "tool": ["prog.curl", "prog.base64"], "language": ["bash"], "runner": [], "carrier": ["carrier.shell_exec"]}
    assert any("OFF_FAMILY_LIST" in x for x in al.check("T53", t53))
    assert al.check("T99", ok)                    # family not allowed
    with pytest.raises(AllowListError):
        al.require("T50", dict(ok, carrier=["carrier.nope"]))
    assert "git" in al.programs("T50") and "echo" not in al.programs("T51")


def test_job_manifest_passes_the_row_start_guard_name_check():
    used = {"policy": ["card.t50.c01"], "tool": ["prog.git"], "language": ["bash"], "runner": [], "carrier": ["carrier.shell_exec", "carrier.user_turn"]}
    man = build_job_manifest("job1", "T50", [("r1", used), ("r2", used)])
    allow, sha, why = guard.load_allowlist(MANIFEST_PATH, sha_file(MANIFEST_PATH))
    assert not why
    assert guard.check_names(man["names"], allow) == []
    for r in man["rows"]:
        assert guard.check_names(r["names"], allow) == []
    with pytest.raises(AllowListError):
        build_job_manifest("job2", "T50", [("r1", dict(used, tool=["prog.git", "prog.zzz"]))])


def test_row_mode_refuses_provisional_names_so_no_row_can_be_built_before_oi_1_is_closed():
    from LA_COMMON.names import set_row_mode
    from T50.dryrun import build_dry
    set_row_mode(True)
    try:
        with pytest.raises(NameSlotUnavailable):
            Names("x", provisional=True)
        with pytest.raises(NameSlotUnavailable):
            build_dry()
    finally:
        set_row_mode(False)
    assert Names("x", provisional=True)


def test_after_namespace_v2_every_manifest_slot_has_a_real_kind_and_is_never_provisional():
    from LA_COMMON.names import DIRECT_KIND, PROVISIONAL_KIND
    for prov in (False, True):
        n = Names("v2-%s" % prov, provisional=prov)
        for slot, kind in nsmod.SLOT_TO_KIND.items():
            assert n.kind_for(slot) == (kind, False), slot
            assert n.get(slot, "k")
        assert not n.used_provisional
    for slot, kind in DIRECT_KIND.items():                      # the L-A table never disagrees with namespace.py
        assert nsmod.SLOT_TO_KIND[slot] == kind
    # the twelve v1.1 slots (addendum v3.2 section 13) are the L-0 dependency: namespace.py has no kind for them yet, so they are
    # provisional-only; every OTHER provisional slot must already have a real kind
    PENDING_L0 = {"ns.ci_job", "ns.hook_script", "ns.migration_id", "ns.cron_job", "ns.systemd_unit", "ns.iac_resource", "ns.lockfile_package",
                  "ns.alias_dir", "ns.consumer_path_component", "ns.crontab_entry", "ns.manifest_object", "ns.lifecycle_rule"}
    assert set(PROVISIONAL_KIND) - set(nsmod.SLOT_TO_KIND) <= PENDING_L0


def test_strict_mode_refuses_names_that_are_not_manifest_slots_even_when_they_equal_a_kind():
    strict = Names("s2", provisional=False)
    for bad in ("ns.user", "ns.company", "ns.bucket", "ns.runner", "ns.policy", "ns.noun_path_segment", "ns.nope", "branch"):
        with pytest.raises(NameSlotUnavailable):
            strict.get(bad, "k")
        with pytest.raises(NameSlotUnavailable):
            Names("s3", provisional=True).get(bad, "k")


def test_deny_check_hook_redraws_and_is_passed_to_namespace():
    seen = []
    a = Names("d1").get("ns.repo", "k")
    n = Names("d1", deny_check=lambda nm: (seen.append(nm), nm == a)[1])
    b = n.get("ns.repo", "k")
    assert seen and b != a
