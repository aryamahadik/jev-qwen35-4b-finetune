"""GEN lane unit tests (CPU only). No file is written outside pytest tmp dirs; no model, no network, no subprocess."""
import copy
import json
import os
import re

import pytest

import blocks as B
import builder as BU
import canon
import gen_common as g
import gates as GT
from gen_common import FORMS

POOL = g.make_testonly_pool(60)


@pytest.fixture(scope="module")
def allow():
    return g.GenAllow()


@pytest.fixture(scope="module")
def rows(allow):
    b = BU.Builder("unit-1", POOL, allow=allow, provisional=True)
    out = []
    for f in FORMS:
        for i in range(10):
            out.extend(b.unit(f, "train", i))
    return out


# ------------------------------------------------------------------ allow-list / names
def test_allow_list_loads_and_is_frozen(allow):
    assert allow.sha == open(g.DEFAULT_MANIFEST_SHA).read().split()[0]
    assert allow.carriers == frozenset(["TBL-PIPE", "TBL-CSV", "TBL-TSV", "TBL-KV", "TBL-JSON", "TXT-PROSE", "TXT-BULLET", "TXT-NUMBERED", "TXT-TIMELINE", "TXT-LEDGER"])
    assert len(allow.train_domains) == 22 and len(allow.dev_domains) == 2


def test_allow_list_refuses_off_list_names(allow):
    for bad in ("TXT-MARKDOWN", "carrier.user_turn", ""):
        with pytest.raises(g.AllowListError):
            allow.check_carrier(bad)
    with pytest.raises(g.AllowListError):
        allow.check_domain("D99")
    with pytest.raises(g.AllowListError):
        allow.check_unit("furlong")
    with pytest.raises(g.AllowListError):
        allow.check_form("AR-F9")


def test_allow_list_sha_mismatch_refused(tmp_path):
    m = tmp_path / "m.json"
    m.write_bytes(open(g.DEFAULT_MANIFEST, "rb").read())
    s = tmp_path / "m.sha256"
    s.write_text("0" * 64 + "  m.json\n")
    with pytest.raises(g.AllowListError):
        g.GenAllow(str(m), str(s))


def test_allow_list_path_with_ohs_or_sealed_refused(tmp_path):
    for comp in ("ohs5x", "my_SEALED_dir"):
        d = tmp_path / comp
        d.mkdir()
        (d / "m.json").write_bytes(open(g.DEFAULT_MANIFEST, "rb").read())
        (d / "m.sha256").write_text(open(g.DEFAULT_MANIFEST_SHA).read())
        with pytest.raises(g.AllowListError):
            g.GenAllow(str(d / "m.json"), str(d / "m.sha256"))


def test_job_names_block_has_all_five_categories(allow):
    nb = allow.job_names(["TBL-CSV", "TXT-PROSE", "TBL-CSV"])
    assert set(nb) == {"policy", "tool", "language", "runner", "carrier"} and nb["carrier"] == ["TBL-CSV", "TXT-PROSE"]
    with pytest.raises(g.AllowListError):
        allow.job_names(["TXT-MARKDOWN"])


def test_row_job_guard_accepts_gen_names_and_rejects_others(rows, allow):
    import row_start_guard as rsg
    al, sha, why = rsg.load_allowlist(g.DEFAULT_MANIFEST, open(g.DEFAULT_MANIFEST_SHA).read().split()[0])
    assert not why
    for r in rows[:40]:
        assert rsg.check_names(r["names"], al, r["row_id"]) == []
    bad = dict(rows[0]["names"], tool=["prog.notatool"])
    assert rsg.check_names(bad, al, "x")
    # the global list contains other families' names; the GEN gate is stricter (GEN rows name only carriers)
    wrong_family = dict(rows[0]["names"], tool=["prog.bash"])
    assert rsg.check_names(wrong_family, al, "x") == []
    r2 = copy.deepcopy(rows[0])
    r2["names"] = wrong_family
    assert not GT.gate_d2_guard([r2], g.DEFAULT_MANIFEST, open(g.DEFAULT_MANIFEST_SHA).read().split()[0])["passed"]
    assert GT.gate_d2_guard(rows[:30], g.DEFAULT_MANIFEST, open(g.DEFAULT_MANIFEST_SHA).read().split()[0])["passed"]


def test_names_come_from_training_namespace_and_are_reproducible(rows):
    for r in rows[:60]:
        assert g.verify_provenance(r["name_seed"], r["name_provenance"], provisional=r["provisional_names"])
        pset = {p[3].lower() for p in r["name_provenance"]}
        assert all(n.lower() in pset for n in BU.spec_names(r["spec"]))
    assert GT.gate_d1_names(rows)["passed"]


def test_tampered_name_is_caught(rows):
    r = copy.deepcopy(rows[0])
    r["name_provenance"][0][3] = "zzzhand"
    assert not g.verify_provenance(r["name_seed"], r["name_provenance"], provisional=True)


def test_rows_mode_refuses_provisional_flag_and_test_only_pool():
    with pytest.raises(g.ProvisionalNamesError):
        BU.Builder("x", POOL, provisional=True, mode="rows")
    with pytest.raises(g.ProvisionalNamesError):
        BU.Builder("x", POOL, provisional=False, mode="rows")        # test-only pool


def test_namespace_has_every_kind_gen_needs_so_names_are_never_provisional():
    """L-0 added the GEN kinds to namespace.py on 18 Oct (this test used to assert they were missing). Every slot now resolves to its own kind,
    and a row built with provisional=False carries provisional_names False and names re-derivable from (TRAINING salt, row seed, slot, key)."""
    import namespace as ns
    for slot, kind in g.SLOT_SUFFIX.items():
        assert kind in ns.KINDS, (slot, kind)
    n = g.RowNamer("s", provisional=False)
    nm = n.entity("a")
    assert nm and not n.used_provisional
    assert g.verify_provenance("s", [list(p) for p in n.provenance], provisional=False)


def test_namer_distinct_names_within_row():
    n = g.RowNamer("rowx")
    names = [n.lower("variable", "v%d" % i) for i in range(40)]
    assert len(set(names)) == 40


# ------------------------------------------------------------------ determinism / uniqueness / shape
def test_determinism_per_seed(allow):
    def run(seed):
        b = BU.Builder(seed, POOL, allow=allow, provisional=True)
        return [json.dumps(r, sort_keys=True, default=str) for f in ("AR-F1", "LG-L1", "CA-C3", "TM-T2", "TB-B2") for r in b.unit(f, "train", 0)]
    assert run("seedA") == run("seedA")
    assert run("seedA") != run("seedB")


def test_all_forms_build_and_validate(rows, allow):
    assert {r["form"] for r in rows} == set(FORMS)
    for r in rows:
        assert BU.validate_row(r, allow) == [], (r["row_id"], BU.validate_row(r, allow))


def test_uniqueness_and_label_gate(rows):
    r = GT.gate_a3_uniqueness(rows)
    assert r["passed"], r


def test_no_hard_bin_upweight_and_weight_one(rows):
    assert all(r["weight"] == 1.0 for r in rows)


def test_tokens_under_cap(rows):
    assert max(r["tokens_est"] for r in rows) <= 1536


def test_json_round_trip_resolves_to_same_label(rows):
    for r in rows:
        r2 = json.loads(json.dumps(r))
        assert norm(B.solve_row_spec(r2["spec"])) == norm(r2["options"][r2["label"]])


def norm(x):
    return BU.norm_option(x)


def test_render_map_offsets_match_text(rows):
    for r in rows:
        assert g.slot_check(r["stem"], r["render_map"])
        for d in r["decision_spans"]:
            assert r["stem"][d["start"]:d["end"]] == d["text"]


def test_canonical_spec_is_json_and_stable_under_round_trip(rows):
    for r in rows:
        c1 = canon.canonical_spec(r["spec"])
        c2 = canon.canonical_spec(json.loads(json.dumps(r["spec"])))
        assert json.loads(json.dumps(c1)) == c1
        assert c1 == c2


def test_parse_back_gate_harness(rows):
    good = {r["row_id"]: canon.canonical_spec(r["spec"]) for r in rows}
    assert GT.gate_a2_parseback(rows, good)["passed"]
    bad = dict(good)
    bad[rows[0]["row_id"]] = {"form": "x"}
    assert GT.gate_a2_parseback(rows, bad, max_drop=0.0)["passed"] is False


def test_agreement_gate_harness(rows):
    ok = {r["row_id"]: r["options"][r["label"]] for r in rows}
    assert GT.gate_a1_agreement(rows, ok)["passed"]
    bad = dict(ok)
    bad[rows[3]["row_id"]] = "definitely not the answer"
    assert not GT.gate_a1_agreement(rows, bad, per_block_pilot_cap=0.0)["passed"]


# ------------------------------------------------------------------ pairs and splits
def test_pair_integrity(allow):
    b = BU.Builder("pairs", POOL, allow=allow, provisional=True)
    seen = {}
    for f in FORMS:
        for i in range(12):
            for r in b.unit(f, "train", i, pair_prob=1.0):
                seen.setdefault(r["pair_id"], []).append(r)
    n_pairs = 0
    for pid, rs in seen.items():
        if pid is None:
            continue
        assert len(rs) == 2 and {x["pair_role"] for x in rs} == {"a", "b"}
        a, bb = rs
        assert a["split"] == bb["split"] and a["domain_id"] == bb["domain_id"] and a["form"] == bb["form"]
        assert a["wording"] == bb["wording"]
        assert a["answer_text"] != bb["answer_text"]       # the edit changes the answer
        n_pairs += 1
    assert n_pairs >= len(FORMS) * 6


def test_split_integrity_train_vs_dev(allow):
    b = BU.Builder("splits", POOL, allow=allow, provisional=True)
    tr, dv = [], []
    for f in ("AR-F1", "LG-L2", "CA-C4", "TM-T1", "TB-B1"):
        for i in range(12):
            tr += b.unit(f, "train", i)
            dv += b.unit(f, "dev", i)
    assert all(r["domain_id"] in g.TRAIN_DOMAINS and r["wording"]["group"] != g.DEV_WORDING_GROUP for r in tr)
    assert all(r["domain_id"] in g.DEV_DOMAINS and r["wording"]["group"] == g.DEV_WORDING_GROUP for r in dv)
    assert not ({r["row_id"] for r in tr} & {r["row_id"] for r in dv})


def test_wording_pool_check_and_hash():
    assert g.check_pool(POOL) == []
    bad = g.WordingPool({k: list(v) for k, v in POOL.entries.items()}, testonly=True)
    bad.entries["q.AR-F2"][0] = "the question has no slots"
    assert any("lacks slots" in p for p in g.check_pool(bad))
    short = g.WordingPool({k: list(v) for k, v in POOL.entries.items()}, testonly=True)
    short.entries["q.AR-F1"] = short.entries["q.AR-F1"][:30]
    assert any("TRAIN wordings" in p or "needs >=" in p for p in g.check_pool(short))
    assert POOL.sha() != bad.sha()


def test_label_letter_balance_greedy(allow):
    b = BU.Builder("letters", POOL, allow=allow, provisional=True)
    rs = []
    for i in range(80):
        rs += b.unit("AR-F1", "train", i, pair_prob=0.0)
    c = [sum(1 for r in rs if r["label"] == k) for k in range(4)]
    assert max(c) - min(c) <= 2


def test_wording_cap_is_respected_when_target_given(allow):
    pool = g.make_testonly_pool(120)
    b = BU.Builder("cap", pool, allow=allow, provisional=True, form_targets={"AR-F1": 100})
    rs = []
    for i in range(70):
        rs += b.unit("AR-F1", "train", i, pair_prob=0.4)
    import collections
    mx = max(collections.Counter(r["wording"]["idx"] for r in rs).values())
    assert mx / len(rs) <= 0.02 + 1e-9 or mx <= 2


# ------------------------------------------------------------------ code hygiene
def _code_facts(path):
    import ast
    tree = ast.parse(open(path).read())
    imports, calls = set(), []
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            imports |= {a.name.split(".")[0] for a in n.names}
        elif isinstance(n, ast.ImportFrom) and n.module:
            imports.add(n.module.split(".")[0])
        elif isinstance(n, ast.Call):
            f = n.func
            name = f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else "")
            mode = None
            if name == "open":
                if len(n.args) > 1 and isinstance(n.args[1], ast.Constant):
                    mode = n.args[1].value
                for kw in n.keywords:
                    if kw.arg == "mode" and isinstance(kw.value, ast.Constant):
                        mode = kw.value.value
            calls.append((name, mode))
    return imports, calls


def test_no_file_writes_network_or_subprocess_in_generator_code():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bad_imports = {"subprocess", "socket", "urllib", "requests", "http", "shutil", "ftplib", "smtplib", "ssl", "multiprocessing"}
    for f in GT.CODE_FILES:
        imports, calls = _code_facts(os.path.join(here, f))
        assert not (imports & bad_imports), (f, imports & bad_imports)
        for name, mode in calls:
            assert name not in ("system", "popen", "unlink", "rmtree", "mkdir", "makedirs", "write_text", "write_bytes", "exec", "eval"), (f, name)
            if name == "open":
                assert mode in (None, "r", "rb"), (f, mode)


def test_no_directory_walks_so_ohs3_paths_are_never_touched():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for f in GT.CODE_FILES:
        src = open(os.path.join(here, f)).read()
        assert not re.search(r"os\.walk|glob\.|\.rglob\(|os\.listdir|scandir", src), f


def test_hash_export_changes_with_pool():
    h1 = GT.hash_export(POOL)
    h2 = GT.hash_export(g.make_testonly_pool(60))
    assert h1["code_sha"] == h2["code_sha"] and h1["pool_testonly"] is True
    other = g.WordingPool(dict(POOL.entries, **{"q.AR-F1": POOL.entries["q.AR-F1"][:-1] + ["{final} changed"]}), testonly=True)
    assert GT.hash_export(other)["pool_sha"] != h1["pool_sha"]


def test_dryrun_builds_twenty_examples_in_memory_only(tmp_path, monkeypatch):
    import dryrun
    monkeypatch.chdir(tmp_path)
    ex = dryrun.build_examples()
    assert len(ex) == 20 and {r["form"] for r in ex} == set(FORMS)
    assert list(tmp_path.iterdir()) == []


# ------------------------------------------------------------------ Opus ruling C1 and the closed-world check
def test_ca_c4_and_c5_state_independent_inputs_and_carry_no_fixed_values(allow):
    b = BU.Builder("c1rule", POOL, allow=allow, provisional=True)
    rs = []
    for f in ("CA-C4", "CA-C5"):
        for i in range(12):
            rs += b.unit(f, "train", i)
    assert rs
    for r in rs:
        assert any(t in r["stem"] for t in (POOL.entries["ca.indep"]))                       # the stated sentence is in the stem
        assert "roots" not in r["spec"] and "fn" not in r["spec"] and "obs" not in r["spec"]  # no fixed exogenous values, no functions
        assert not re.search(r"\bset to \d|\bwas \d|=\s*\d", r["stem"])


def test_closed_world_every_spec_fact_is_in_the_stem(rows):
    for r in rows:
        spec, stem, form = r["spec"], r["stem"], r["form"]
        names = BU.spec_names(spec)
        for n in names:
            assert n in stem, (r["row_id"], n)
        if form.startswith("AR"):
            for bq in spec["base"]:
                assert bq["value"] in stem, (r["row_id"], bq)
        if form == "TM-T1":
            assert spec["start"] in stem
            for o in spec["ops"]:
                assert str(o["n"]) in stem
        if form.startswith("TB"):
            for t in spec["tables"]:
                for row in t["rows"]:
                    assert str(row[0]) in stem


def test_option_texts_never_contain_the_stem_only_unit_conversions_unlisted(rows):
    allowed = set(g.GenAllow().units) | {"count"}
    for r in rows:
        if r["form"] == "AR-F1":
            for o in r["options"]:
                unit = o.split(" ", 1)[1].rstrip("s")
                assert unit in allowed or unit == r["spec"].get("count_noun"), o
