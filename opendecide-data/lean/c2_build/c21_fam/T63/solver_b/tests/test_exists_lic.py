"""EXISTS (EX-A1, EX-A2, EX-B1, EX-B2) and LIC: fact classes, absence only inside the stated range, sources injected as plain data."""
import pytest

from T63.solver_b import exists_b, hook
from helpers import EXISTS_DEFS, LIC_DEFS, bview


def run(v, **kw):
    return hook.evaluate(v, **kw)


# ---- EX-A1 --------------------------------------------------------------------------------------------------------------------------
def a1_context(blocks):
    parts = [EXISTS_DEFS]
    for rid, host, lo, hi, names in blocks:
        parts.append('Registry index for %s (%s), complete for package names from "%s" to "%s":\n%s' % (rid, host, lo, hi, "\n".join("- " + n for n in names)))
    return "\n\n".join(parts)


R1 = ("R1", "one.example", "alpha-aaa-lib", "zulu-zzz-lib", ["alpha-aaa-lib", "kilo-kkk-core", "mike-mmm-kit", "zulu-zzz-lib"])
R2 = ("R2", "two.example", "bravo-bbb-lib", "yank-yyy-lib", ["bravo-bbb-lib", "delta-ddd-core", "yank-yyy-lib"])


def a1(name, asked="R1", blocks=(R1, R2), frame="Does the listing for {s} include an entry named {n}?"):
    host = {b[0]: b[1] for b in blocks}[asked] if asked in {b[0] for b in blocks} else "x.example"
    q = frame.format(s="%s (%s)" % (asked, host), n=name)
    return bview("EXISTS", "EX-A1", a1_context(blocks), q, ["YES", "NO"], {"head": "EXISTS", "sub": "EX-A1"})


def test_a1_listed_is_yes_and_absent_inside_range_is_no():
    assert run(a1("kilo-kkk-core"))["label"] == "YES"
    r = run(a1("lima-lll-core"))
    assert r["label"] == "NO" and r["reason"] == "a1_absent_in_range"


def test_a1_only_the_asked_registry_block_counts():
    assert run(a1("delta-ddd-core", asked="R1"))["label"] == "NO"          # listed in R2 only
    assert run(a1("delta-ddd-core", asked="R2"))["label"] == "YES"
    assert run(a1("kilo-kkk-core", asked="R2"))["label"] == "NO"           # listed in R1 only; inside R2's range, so absence is provable


def test_a1_name_outside_the_range_abstains_when_not_listed():
    r = run(a1("zzzz-zzz-core", blocks=(R2,), asked="R2"))
    assert r["status"] == "abstain" and r["reason"] == "a1_outside_range"


def test_a1_single_block_and_unlisted_registry():
    assert run(a1("mike-mmm-kit", blocks=(R1,)))["label"] == "YES"
    assert run(a1("mike-mmm-kit", blocks=(R1,), asked="R2"))["status"] == "abstain"        # the asked registry has no block


@pytest.mark.parametrize("frame", ["Is the name {n} listed under {s}?", "Is {n} listed for {s} in this record?", 'For {s}, is "{n}" among the rows?',
                                   "Does {s} hold {n} according to the table above?", "Is there a {n} entry in the listing of {s}?"])
def test_a1_question_wordings(frame):
    assert run(a1("kilo-kkk-core", frame=frame))["label"] == "YES"
    assert run(a1("lima-lll-core", frame=frame))["label"] == "NO"


def test_a1_list_marked_complete_only_for_its_range():
    v = a1("kilo-kkk-core")
    assert run(v)["status"] == "ok"
    v["rendered"]["context"] = v["rendered"]["context"].replace("a name inside the range that is not listed does not exist", "an unlisted name may exist")
    assert run(v)["reason"] == "defs_mismatch"


# ---- EX-A2 --------------------------------------------------------------------------------------------------------------------------
def a2_context(lib="torget-sdk", ver="4.2.0", mods=None):
    mods = mods or {"lonrolu": ["bolnudi", "fudoru", "mospame"], "nonzuvu": ["bengoko", "fudoru", "vizafe"]}
    return EXISTS_DEFS + "\n\nLibrary %s version %s, complete export list:\n" % (lib, ver) + "\n".join("module %s: %s" % (m, ", ".join(s)) for m, s in sorted(mods.items()))


def a2(name, lib="torget-sdk", ver="4.2.0", mods=None, frame="Is {n} one of the names given for {s}?"):
    q = frame.format(n=name, s="%s version %s" % (lib, ver))
    return bview("EXISTS", "EX-A2", a2_context(lib, ver, mods), q, ["NO", "YES"], {"head": "EXISTS", "sub": "EX-A2"})


def test_a2_symbol_in_its_module():
    r = run(a2("lonrolu.fudoru"))
    assert r["label"] == "YES" and r["letter"] == "B"


def test_a2_symbol_exists_only_in_a_sibling_module_is_no():
    assert run(a2("lonrolu.bengoko"))["label"] == "NO"
    assert run(a2("nonzuvu.bengoko"))["label"] == "YES"


def test_a2_version_dots_in_the_scope_are_not_the_name():
    assert run(a2("nonzuvu.vizafe", ver="12.0.3"))["label"] == "YES"


def test_a2_scope_mismatch_abstains():
    v = a2("lonrolu.fudoru")
    v["rendered"]["question"] = v["rendered"]["question"].replace("4.2.0", "4.3.0")
    assert run(v)["reason"] == "a2_scope_mismatch"


# ---- EX-B1 / EX-B2 ------------------------------------------------------------------------------------------------------------------
def b1_context(lang_word="Python 3.12", module="pathx", names=("aa", "bb", "Cc", "dd"), rng=None):
    scope = "complete" if rng is None else 'complete for names from "%s" to "%s"' % rng
    return EXISTS_DEFS + "\n\nExports of %s module %s in the pinned toolchain image, %s:\n" % (lang_word, module, scope) + "\n".join("- " + n for n in names)


ESHA = "e" * 64
B1_NAMES = ["aa", "bb", "Cc", "dd"]
B1_EXPORTS = {"python": {"pathx": list(B1_NAMES)}, "node": {"pathx": list(B1_NAMES)}, "go": {"pathx": list(B1_NAMES)}}
S1 = {"exports": B1_EXPORTS, "export_sha": ESHA}                 # the sha-bound export source EX-B1 / EX-B2 REQUIRE (Opus ruling Q3a)


def b1(name, lang="python", module="pathx", rng=None, names=("aa", "bb", "Cc", "dd"), sha=ESHA):
    lw = {"python": "Python 3.12", "node": "Node 24", "go": "Go 1.26"}[lang]
    q = "%s %s module %s in the pinned toolchain image" % (name, lw, module)
    wit = {"head": "EXISTS", "sub": "EX-B1", "lang": lang, "module": module, "name": name}
    if sha is not None:
        wit["export_sha"] = sha
    return bview("EXISTS", "EX-B1", b1_context(lw, module, names, rng), q, ["YES", "NO"], wit)


def test_b1_listed_and_absent():
    assert run(b1("Cc"), **S1)["label"] == "YES"
    assert run(b1("cc"), **S1)["label"] == "NO"                       # case matters
    assert run(b1("zz"), **S1)["label"] == "NO"


def test_b1_range_listing_decides_absence_inside_the_range_only():
    assert run(b1("bc", rng=("aa", "dd")), **S1)["label"] == "NO"
    r = run(b1("zz", rng=("aa", "dd")), **S1)
    assert r["status"] == "abstain" and r["reason"] == "b1_outside_range"


def test_b1_witness_must_match_the_shown_scope():
    v = b1("aa")
    v["witness_inputs"]["module"] = "other"
    assert run(v, **S1)["reason"] == "b1_scope_mismatch"
    v = b1("aa", lang="go")
    v["witness_inputs"]["lang"] = "node"
    assert run(v, **S1)["reason"] == "b1_scope_mismatch"


def b2(name, lang="python", module="pathx", sha=ESHA):
    lw = {"python": "Python 3.12", "node": "Node 24", "go": "Go 1.26"}[lang]
    q = "Is %s exported by %s module %s in the pinned toolchain image?" % (name, lw, module)
    wit = {"head": "EXISTS", "sub": "EX-B2", "lang": lang, "module": module, "name": name}
    if sha is not None:
        wit["export_sha"] = sha
    return bview("EXISTS", "EX-B2", EXISTS_DEFS, q, ["NO", "YES"], wit)


EXPORTS = {"python": {"pathx": ["aa", "bb", "Cc"]}, "node": {"fsx": ["readX"]}, "go": {"httpx": ["Get", "Post"]}}
S2 = {"exports": EXPORTS, "export_sha": ESHA}


def test_b2_membership_in_the_export_data():
    assert run(b2("aa"), **S2)["label"] == "YES"
    assert run(b2("zz"), **S2)["label"] == "NO"
    assert run(b2("Get", lang="go", module="httpx"), **S2)["label"] == "YES"
    assert run(b2("get", lang="go", module="httpx"), **S2)["label"] == "NO"


def test_b2_never_guesses_without_its_source_or_with_the_wrong_one():
    assert run(b2("aa"))["reason"] == "no_export_source"
    assert run(b2("aa"), exports=EXPORTS, export_sha="f" * 64)["reason"] == "export_sha_mismatch"
    assert run(b2("aa", module="unknown"), **S2)["reason"] == "b2_module_unknown"


def test_b1_export_crosscheck_flag():
    r = run(b1("aa"), **S2)
    assert r["status"] == "ok" and r["xcheck"] is True
    assert exists_b.b1_export_crosscheck(b1("dd"), "YES", EXPORTS) is False      # shown list says dd is there, the export file does not


# ---- Opus ruling Q3a (18 Oct): the sha of the export / table is MANDATORY; a missing, mismatched or fixture source or sha is an abstain ---------
REAL_HEX = "9f2b6c1d0a4e8b7351c6d2f09e8a7b34c5d1e0f2a9b8c7d6e5f40312a1b0c9d8"


@pytest.mark.parametrize("make,sources", [(b1, S1), (b2, S2)])
def test_q3a_export_sha_is_mandatory_for_b1_and_b2(make, sources):
    ex = sources["exports"]
    assert run(make("aa"), **sources)["status"] == "ok"
    # (1) source missing
    assert run(make("aa"))["reason"] == "no_export_source"
    assert run(make("aa"), export_sha=ESHA)["reason"] == "no_export_source"
    # (2) the sha is not configured: the old "if sha is not None" shortcut is gone
    for blank in (None, "", "   "):
        r = run(make("aa"), exports=ex, export_sha=blank)
        assert r["status"] == "abstain" and r["label"] is None and r["reason"] == "no_export_sha", (blank, r)
    # (3) the row's witness has no sha
    r = run(make("aa", sha=None), **sources)
    assert r["status"] == "abstain" and r["reason"] == "witness_export_sha_missing", r
    r = run(make("aa", sha=""), **sources)
    assert r["reason"] == "witness_export_sha_missing", r
    # (4) the witness sha differs from the configured (recorded) one
    r = run(make("aa", sha="f" * 64), **sources)
    assert r["status"] == "abstain" and r["reason"] == "export_sha_mismatch", r
    r = run(make("aa"), exports=ex, export_sha="f" * 64)
    assert r["reason"] == "export_sha_mismatch", r
    # a real-looking sha256 passes
    assert run(make("aa", sha=REAL_HEX), exports=ex, export_sha=REAL_HEX)["status"] == "ok"


@pytest.mark.parametrize("make,sources", [(b1, S1), (b2, S2)])
def test_q3a_fixture_export_source_or_sha_is_an_abstain_unless_explicitly_allowed(make, sources):
    ex = sources["exports"]
    # declared fixture: refused
    r = run(make("aa"), fixture=True, **sources)
    assert r["status"] == "abstain" and r["reason"] == "fixture_export_source", r
    # a sha that names itself a fixture / stand-in: refused even when the caller did not declare it, even when the witness agrees
    for marker in ("fixture-export-sha", "STANDIN-EXPORT", "stand-in_sha", "dummy", "test-sha"):
        r = run(make("aa", sha=marker), exports=ex, export_sha=marker)
        assert r["status"] == "abstain" and r["reason"] == "fixture_export_source", (marker, r)
    # the build-stage harness may opt in explicitly; the result then says so
    r = run(make("aa"), fixture=True, allow_fixture=True, **sources)
    assert r["status"] == "ok" and r["fixture"] is True and r["label"] == "YES"
    r = run(make("aa", sha="fixture-export-sha"), exports=ex, export_sha="fixture-export-sha", allow_fixture=True)
    assert r["status"] == "ok"
    # allowing fixtures never relaxes the sha rules
    assert run(make("aa", sha=None), fixture=True, allow_fixture=True, **sources)["reason"] == "witness_export_sha_missing"
    assert run(make("aa", sha="f" * 64), fixture=True, allow_fixture=True, **sources)["reason"] == "export_sha_mismatch"
    assert run(make("aa"), exports=ex, export_sha=None, fixture=True, allow_fixture=True)["reason"] == "no_export_sha"


def test_q3a_b1_must_agree_with_the_real_export():
    # the shown list has dd, the real export does not: a defect row, B abstains instead of labelling it
    r = run(b1("dd"), **S2)
    assert r["status"] == "abstain" and r["label"] is None and r["reason"] == "b1_export_mismatch", r
    # the shown list omits an export name inside a complete-listing range (NO on the list, YES in the export)
    ex = {"python": {"pathx": ["aa", "bb", "Cc", "dd", "ee"]}}
    r = run(b1("ee", rng=("aa", "ff")), exports=ex, export_sha=ESHA)
    assert r["reason"] == "b1_export_mismatch", r
    # the module is not in the export at all: not checkable, so no label
    r = run(b1("aa"), exports={"python": {"other": ["aa"]}}, export_sha=ESHA)
    assert r["reason"] == "b1_export_module_unknown", r
    r = run(b1("aa", lang="go"), exports={"python": {"pathx": ["aa"]}}, export_sha=ESHA)
    assert r["reason"] == "b1_export_module_unknown", r
    # agreement: YES and NO both pass the cross-check
    assert run(b1("bb"), **S1)["xcheck"] is True
    assert run(b1("zz"), **S1)["xcheck"] is True


# ---- LIC ----------------------------------------------------------------------------------------------------------------------------
USE = ["vendored source copy", "static link", "dynamic link", "separate process", "dev-time tool only"]
DIST = ["distributed to others", "internal only", "offered as a network service"]


def lic(dep, proj, use, dist, order=None):
    ctx = LIC_DEFS + "\n\nLicence card\nDependency licence: %s\nProject licence: %s\nUsage: %s\nDistribution: %s" % (dep, proj, use, dist)
    return bview("LIC", "LIC", ctx, "What is the licence status of %s for the project %s, under the rules above?" % (dep, proj),
                 ["COMPATIBLE", "REVIEW", "INCOMPATIBLE"], {"head": "LIC", "table_sha": "t" * 64}, order)


def make_table():
    t = {}
    for d in ("MIT", "GPL-3.0-only"):
        for p in ("Apache-2.0", "MIT"):
            for ui in range(5):
                for si in range(3):
                    t[(d, p, "LC-USE-%d" % (ui + 1), "LC-DIST-%d" % (si + 1))] = ("COMPATIBLE", "REVIEW", "INCOMPATIBLE")[(ui + si + len(d)) % 3]
    return t


TABLE = make_table()
TSHA = "t" * 64
SL = {"table": TABLE, "table_sha": TSHA}                         # the hashed table source LIC REQUIRES (Opus ruling Q3a)


@pytest.mark.parametrize("ui", range(5))
@pytest.mark.parametrize("si", range(3))
def test_lic_every_axis_value_reaches_its_own_cell(ui, si):
    want = TABLE[("GPL-3.0-only", "MIT", "LC-USE-%d" % (ui + 1), "LC-DIST-%d" % (si + 1))]
    r = run(lic("GPL-3.0-only", "MIT", USE[ui], DIST[si]), **SL)
    assert r["status"] == "ok" and r["label"] == want


def test_lic_letter_follows_the_shuffled_option_order():
    for order in ((0, 1, 2), (2, 0, 1), (1, 2, 0)):
        v = lic("MIT", "MIT", USE[0], DIST[0], order)
        r = run(v, **SL)
        want_letter = "ABC"[[("COMPATIBLE", "REVIEW", "INCOMPATIBLE")[i] for i in order].index(r["label"])]
        assert r["letter"] == want_letter


def test_lic_no_table_or_missing_cell_or_wrong_sha_abstains():
    assert run(lic("MIT", "MIT", USE[0], DIST[0]))["reason"] == "no_table_source"
    assert run(lic("MIT", "MIT", USE[0], DIST[0]), table_sha=TSHA)["reason"] == "no_table_source"
    assert run(lic("BSD-2-Clause", "MIT", USE[0], DIST[0]), **SL)["reason"] == "cell_missing"
    assert run(lic("MIT", "MIT", USE[0], DIST[0]), table=TABLE, table_sha="x" * 64)["reason"] == "table_sha_mismatch"
    assert run(lic("MIT", "MIT", "static linking", DIST[0]), **SL)["reason"] == "axis_phrase"


def lic_w(sha):
    v = lic("MIT", "MIT", USE[0], DIST[0])
    if sha is None:
        v["witness_inputs"].pop("table_sha", None)
    else:
        v["witness_inputs"]["table_sha"] = sha
    return v


def test_q3a_lic_table_sha_is_mandatory():
    assert run(lic("MIT", "MIT", USE[0], DIST[0]), **SL)["status"] == "ok"
    # the table sha is not configured: the old "if sha is not None" shortcut is gone
    for blank in (None, "", "  "):
        r = run(lic("MIT", "MIT", USE[0], DIST[0]), table=TABLE, table_sha=blank)
        assert r["status"] == "abstain" and r["label"] is None and r["reason"] == "no_table_sha", (blank, r)
    # the row's witness has no table sha
    for blank in (None, ""):
        r = run(lic_w(blank), **SL)
        assert r["status"] == "abstain" and r["reason"] == "witness_table_sha_missing", (blank, r)
    # mismatch
    assert run(lic_w("u" * 64), **SL)["reason"] == "table_sha_mismatch"
    assert run(lic_w(REAL_HEX), table=TABLE, table_sha=REAL_HEX)["status"] == "ok"


def test_q3a_lic_fixture_table_or_sha_is_an_abstain_unless_explicitly_allowed():
    v = lic("MIT", "MIT", USE[0], DIST[0])
    r = run(v, fixture=True, **SL)
    assert r["status"] == "abstain" and r["reason"] == "fixture_table_source", r
    for marker in ("fixture-table-sha", "STANDIN_TABLE", "stand-in-table"):
        r = run(lic_w(marker), table=TABLE, table_sha=marker)
        assert r["status"] == "abstain" and r["reason"] == "fixture_table_source", (marker, r)
    r = run(v, fixture=True, allow_fixture=True, **SL)
    assert r["status"] == "ok" and r["fixture"] is True
    assert run(lic_w(None), fixture=True, allow_fixture=True, **SL)["reason"] == "witness_table_sha_missing"
    assert run(lic_w("u" * 64), fixture=True, allow_fixture=True, **SL)["reason"] == "table_sha_mismatch"
    assert run(v, table=TABLE, table_sha=None, fixture=True, allow_fixture=True)["reason"] == "no_table_sha"


def test_q3a_module_level_plug_point_applies_the_same_rules():
    try:
        hook.configure(exports=B1_EXPORTS, export_sha=ESHA, table=TABLE, table_sha=TSHA)
        assert hook.solver_b(b1("Cc"))["label"] == "YES" and hook.solver_b(lic("MIT", "MIT", USE[0], DIST[0]))["status"] == "ok"
        hook.configure(exports=B1_EXPORTS, table=TABLE)                                   # sources without their shas
        assert hook.solver_b(b1("Cc"))["reason"] == "no_export_sha" and hook.solver_b(b2("aa"))["reason"] == "no_export_sha"
        assert hook.solver_b(lic("MIT", "MIT", USE[0], DIST[0]))["reason"] == "no_table_sha"
        hook.configure(exports=B1_EXPORTS, export_sha=ESHA, table=TABLE, table_sha=TSHA, fixture=True)
        assert hook.solver_b(b1("Cc"))["reason"] == "fixture_export_source"
        assert hook.solver_b(lic("MIT", "MIT", USE[0], DIST[0]))["reason"] == "fixture_table_source"
        assert hook.make_solver_b(exports=B1_EXPORTS, export_sha=ESHA, fixture=True)(b2("aa"))["reason"] == "fixture_export_source"
    finally:
        hook.configure()


def test_lic_table_keyed_by_phrases_is_accepted():
    phr = {("MIT", "MIT", USE[1], DIST[2]): "REVIEW"}
    assert run(lic("MIT", "MIT", USE[1], DIST[2]), table=phr, table_sha=TSHA)["label"] == "REVIEW"


def test_lic_axes_are_not_confused_dep_vs_project():
    t = {("MIT", "GPL-3.0-only", "LC-USE-2", "LC-DIST-1"): "INCOMPATIBLE", ("GPL-3.0-only", "MIT", "LC-USE-2", "LC-DIST-1"): "COMPATIBLE"}
    assert run(lic("MIT", "GPL-3.0-only", USE[1], DIST[0]), table=t, table_sha=TSHA)["label"] == "INCOMPATIBLE"
    assert run(lic("GPL-3.0-only", "MIT", USE[1], DIST[0]), table=t, table_sha=TSHA)["label"] == "COMPATIBLE"


def test_table_from_label_fn_builds_the_plain_table():
    def fn(d, p, u, s):
        if d == "bad":
            raise KeyError(d)
        return "REVIEW"
    t = hook.table_from_label_fn(fn, ["MIT", "bad"], ["MIT"])
    assert len(t) == 15 and ("MIT", "MIT", "LC-USE-5", "LC-DIST-3") in t
    assert run(lic("MIT", "MIT", USE[4], DIST[2]), table=t, table_sha=TSHA)["label"] == "REVIEW"
    assert run(lic("bad", "MIT", USE[4], DIST[2]), table=t, table_sha=TSHA)["reason"] == "cell_missing"
