"""T66 MSG production commit-message pool: the CH-6 fix, the pool file and its dev / dev2 split, the lint, and the generator wiring (Opus ruling Q8: verbatim swaps, matched CH-trivial
messages, the overlap hard stratum). CPU only (stand-in executor)."""
import collections
import copy
import json
import os
import re

import pytest

from LP_COMMON import sandbox_iface as S
from T66 import checked, generator as G, lint_msg_pool as LINT, msg_pool as MP, msg_spec as MSG

FAMDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = json.load(open(os.path.join(FAMDIR, "pools", "wording_pool.json")))
DOC = MP.load()


def _rows(split, seeds=(1,), total=1200):
    out = []
    for seed in seeds:
        ctx = G.Ctx(seed=seed, standin=True, pool=BASE, msg_split=split)
        for g in [g for g in G.build_plan(total=total, seed=seed) if g["head"] == "MSG"]:
            try:
                out += G.generate_group(ctx, g)
            except MSG.Reject:
                pass
    return out


@pytest.fixture(scope="module")
def rows_all():
    return _rows("all")


# ---- CH-6: the spec name, the verb class, the rendered diff and the messages describe the same change -------------------------------------------------------------------
def test_ch6_is_make_parameter_required_with_a_matching_diff():
    assert MSG.VERB_CLASS["CH-6"] == "required" and "required" in MSG.CH_NAMES["CH-6"] and "default" in MSG.CH_NAMES["CH-6"]
    assert MSG.VERB_CLASS["CH-5"] == "default"
    ctx = G.Ctx(seed=1, standin=True, pool=BASE, msg_split="all", executor=S.SimExecutor())
    specs = MSG.build_group(ctx, {"gid": "c6", "seed": "c6"}, {"chs": ["CH-6", "CH-3"], "trivial": [0]})
    s = next(x for x in specs if x["ch"] == "CH-6")
    minus = [ln[1:] for ln in s["diff"].split("\n") if ln.startswith("-") and not ln.startswith("---")]
    plus = [ln[1:] for ln in s["diff"].split("\n") if ln.startswith("+") and not ln.startswith("+++")]
    param, old = s["slots"]["param"], s["slots"]["num_old"]
    assert minus == ["def %s(%s, %s=%d):" % (s["fn"], s["slots"]["arg"], param, old)]
    assert plus == ["def %s(%s, %s):" % (s["fn"], s["slots"]["arg"], param)]            # the default is REMOVED: the parameter becomes required
    assert s["verb"] == "required"


def test_ch6_messages_never_say_default_and_ch5_messages_always_do():
    for t in DOC["kinds"]["CH-6"]["templates"]:
        assert "default" not in t["text"].lower(), t["text"]
    for t in DOC["kinds"]["CH-5"]["templates"]:
        assert "default" in t["text"].lower(), t["text"]


def test_ch4_and_ch7_stay_registered_but_unrealised():
    assert set(MSG.CH_NEVER) == {"CH-4", "CH-7"} and not set(MSG.CH_NEVER) & set(MSG.CH_REALISED)
    assert set(MP.KINDS) == set(MSG.CH_REALISED) | set(MSG.TRIV_IDS) and not set(MSG.CH_NEVER) & set(DOC["kinds"])


# ---- the pool file and its split ------------------------------------------------------------------------------------------------------------------------------------------
def test_pool_has_many_templates_per_kind_and_both_halves():                               # the old holdout half is dev material now (dev2); "holdout" is reserved
    for kind, body in DOC["kinds"].items():
        ts = body["templates"]
        assert len(ts) >= 40 and len({t["id"] for t in ts}) == len(ts)
        for half in ("dev", "dev2"):
            assert sum(1 for t in ts if t["split"] == half) >= 20
            for st in ("I", "N"):
                assert sum(1 for t in ts if t["split"] == half and t["style"] == st) >= 10


def test_split_is_the_seeded_hash_rule_and_halves_are_disjoint_and_complete():
    for kind, body in DOC["kinds"].items():
        for st in MP.STYLES:
            texts = [t["text"] for t in body["templates"] if t["style"] == st]
            want = MP.split_ranks(kind, texts)
            assert all(want[t["text"]] == t["split"] for t in body["templates"] if t["style"] == st)
    dev, hold = MP.templates(DOC, "dev"), MP.templates(DOC, "dev2")
    ids = lambda tt: {t["id"] for by in tt.values() for ts in by.values() for t in ts}                     # noqa: E731
    assert not ids(dev) & ids(hold) and ids(dev) | ids(hold) == ids(MP.templates(DOC, "all")) and not MP.templates(DOC, "holdout")
    assert MP.split_ranks("CH-1", ["a b", "c d", "e f", "g h"]) == MP.split_ranks("CH-1", ["g h", "e f", "c d", "a b"])           # order independent
    with pytest.raises(ValueError):
        MP.templates(DOC, "train")


def test_wording_pool_replaces_the_message_forms_only():
    with pytest.raises(ValueError):                                                                          # the reserved holdout half has no templates yet
        MP.wording_pool(BASE, DOC, "holdout")
    for split in ("dev", "dev2"):
        pool = MP.wording_pool(BASE, DOC, split)
        assert G.pool_problems(pool) == []
        for f in BASE["forms"]:
            if f not in MSG.FORMS_MSG:
                assert pool["forms"][f] == BASE["forms"][f]
        assert set(MSG.FORMS_MSG) <= set(pool["forms"]) and pool["msg_split"] == split
        assert {w["id"] for f in MSG.FORMS_MSG for w in pool["forms"][f]} == {t["id"] for by in MP.templates(DOC, split).values() for ts in by.values() for t in ts}
    assert BASE["forms"]["T66-M-CH-1-I"][0]["text"].startswith("Does the commit message") and "msg_split" not in BASE      # the base pool is untouched (deep copy)


def test_cli_writes_the_pool_file_the_agreement_harness_takes(tmp_path):
    out = tmp_path / "pool.json"
    assert MP.main(["--split", "dev2", "--out", str(out)]) == 0
    pool = json.load(open(out))
    assert pool["msg_split"] == "dev2" and G.pool_problems(pool) == []
    assert {t["id"] for by in MP.templates(DOC, "dev2").values() for ts in by.values() for t in ts} == {w["id"] for f in MSG.FORMS_MSG for w in pool["forms"][f]}


def test_message_pool_file_is_part_of_the_generator_sha():
    names = [os.path.basename(p) for p in checked.CODE_FILES]
    assert "msg_messages.json" in names and "msg_pool.py" in names and all(os.path.exists(p) for p in checked.CODE_FILES)


# ---- the lint -------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_lint_passes_on_the_shipped_pool():
    bad, rep = LINT.lint(DOC)
    assert bad == [] and rep["max_cross_kind_jaccard"]["value"] < 0.5 and rep["templates"] >= 11 * 40


def _first(doc, kind, style):
    return next(t for t in doc["kinds"][kind]["templates"] if t["style"] == style)


def test_lint_catches_a_text_shared_between_kinds():
    d = copy.deepcopy(DOC)
    _first(d, "CH-9", "N")["text"] = _first(d, "CH-1", "N")["text"]
    assert any("shared" in b for b in LINT.lint(d)[0])
    d = copy.deepcopy(DOC)                                                                                    # the same text behind a conventional-commit prefix is still shared
    _first(d, "CH-9", "N")["text"] = "fix: " + _first(d, "CH-1", "N")["text"]
    assert any("shared" in b for b in LINT.lint(d)[0])


def test_lint_catches_a_template_too_similar_to_another_kind():
    d = copy.deepcopy(DOC)
    t = _first(d, "CH-3", "I")
    d["kinds"]["CH-6"]["templates"].append(dict(t, id="CH-6-I-99", text=t["text"] + " now"))                 # CH-3 wording inside CH-6 (also names the wrong kind)
    bad = LINT.lint(d)[0]
    assert any("Jaccard" in b for b in bad) and any("names other kind" in b for b in bad)


def test_lint_catches_missing_slots_unknown_slots_and_foreign_verbs():
    d = copy.deepcopy(DOC)
    _first(d, "CH-2", "I")["text"] = "fix the off-by-one in the loop range"                                 # style I without {fn}
    assert any("misses {fn}" in b for b in LINT.lint(d)[0])
    d = copy.deepcopy(DOC)
    _first(d, "CH-2", "N")["text"] = "fix the off-by-one in the {fn} loop range"                            # style N with a slot
    assert any("identifier slots" in b for b in LINT.lint(d)[0])
    d = copy.deepcopy(DOC)
    _first(d, "CH-2", "I")["text"] = "fix the off-by-one in {fn} for {param}"                               # {param} is not a CH-2 slot
    assert any("not slots of CH-2" in b for b in LINT.lint(d)[0])
    d = copy.deepcopy(DOC)
    _first(d, "CH-8", "N")["text"] = "rename the error message into something clearer"                      # names CH-3's verb
    assert any("names other kind" in b for b in LINT.lint(d)[0])
    d = copy.deepcopy(DOC)
    _first(d, "CH-8", "N")["text"] = "make the report friendlier for operators"                              # names no kind word at all
    assert any("does not name its own kind" in b for b in LINT.lint(d)[0])
    d = copy.deepcopy(DOC)
    _first(d, "CH-8", "N")["text"] = "is the error message clear?"
    assert any("question" in b for b in LINT.lint(d)[0])


def test_lint_catches_a_wrong_stored_split_and_small_pools():
    d = copy.deepcopy(DOC)
    t = _first(d, "CH-10", "N")
    t["split"] = "dev2" if t["split"] == "dev" else "dev"
    assert any("seeded-hash rule" in b for b in LINT.lint(d)[0])
    d = copy.deepcopy(DOC)
    d["kinds"]["CH-10"]["templates"] = d["kinds"]["CH-10"]["templates"][:30]
    assert any("CH-10 has 30 templates" in b for b in LINT.lint(d)[0])


# ---- generator wiring -----------------------------------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("split", ["dev", "dev2"])
def test_a_half_draws_only_its_own_templates(split):
    rows = _rows(split)
    assert rows
    allowed = {t["id"] for by in MP.templates(DOC, split).values() for ts in by.values() for t in ts}
    other = {t["id"] for by in MP.templates(DOC, "dev2" if split == "dev" else "dev").values() for ts in by.values() for t in ts}
    used = {r["spec"]["message_wid"] for r in rows}
    assert used and used <= allowed and not used & other


def test_all_uses_both_halves(rows_all):
    halves = {next(t["split"] for body in DOC["kinds"].values() for t in body["templates"] if t["id"] == r["spec"]["message_wid"]) for r in rows_all}
    assert halves == {"dev", "dev2"}


def test_rows_carry_pool_messages_not_question_frames(rows_all):
    for r in rows_all:
        assert not r["spec"]["message"].endswith("?") and "{" not in r["spec"]["message"] and len(r["spec"]["message"].split()) >= 4
        assert re.match(r"^(CH-\d+|fmt|comment|doc)-[IN]-\d+$", r["spec"]["message_wid"])
    own = [r for r in rows_all if r["gold"] == "YES"]
    assert all(r["spec"]["message_wid"].startswith(r["meta"]["ch"] + "-") for r in own)                    # a true message is a template of the diff's own kind


def test_true_messages_name_only_what_the_diff_shows(rows_all):
    """Every function / variable name in a YES message (style I) occurs in the diff; style N carries no name and no slot value."""
    seen_i = 0
    for r in rows_all:
        if r["gold"] != "YES":
            continue
        names = re.findall(r"[a-z]+_[a-z_]+", r["spec"]["message"])
        if r["spec"]["style"] == "I":
            seen_i += 1
            assert names and all(n in r["spec"]["diff"] for n in names), (r["spec"]["message"], r["spec"]["diff"])
        else:
            assert not names
    assert seen_i > 20


def _by_group(rows):
    by = collections.defaultdict(list)
    for r in rows:
        by[r["group_id"]].append(r)
    return by


def test_swap_no_message_is_the_partner_true_message_verbatim(rows_all):
    """Opus ruling Q8 R1 / R2: inside a swap group each true message is used exactly once as a NO message on the other diff, as rendered in its own YES row."""
    n = 0
    for gid, rs in _by_group(rows_all).items():
        no = [r for r in rs if r["gold"] == "NO"]
        if no[0]["spec"]["origin"] != "swap":
            continue
        n += 1
        yes = {r["meta"]["pair_id"]: r for r in rs if r["gold"] == "YES"}
        assert sorted(r["spec"]["message"] for r in no) == sorted(r["spec"]["message"] for r in yes.values())          # multiset identity
        for r in no:
            own = yes[r["meta"]["pair_id"]]
            partner = next(y for pid, y in yes.items() if pid != r["meta"]["pair_id"])
            assert r["spec"]["message"] == partner["spec"]["message"] and r["spec"]["message_wid"] == partner["spec"]["message_wid"]       # verbatim: same wording id and fillers
            assert MSG.jaccard(r["spec"]["message"], own["spec"]["message"]) < 0.5 and partner["meta"]["ch"] != own["meta"]["ch"]
            assert partner["spec"]["verb"] != own["spec"]["verb"] and r["manifest"]["own_message"] == own["spec"]["message"]
    assert n > 20


def test_trivial_no_message_is_matched_to_its_true_message(rows_all):
    """Opus ruling Q8 R3: same rendered token count, same style, characters within +-3, and it describes a trivial hunk of its own diff."""
    n = 0
    for gid, rs in _by_group(rows_all).items():
        yes = {r["meta"]["pair_id"]: r for r in rs if r["gold"] == "YES"}
        for r in rs:
            if r["gold"] != "NO" or r["spec"]["origin"] != "trivial":
                continue
            n += 1
            own = yes[r["meta"]["pair_id"]]
            a, b = r["spec"]["message"], own["spec"]["message"]
            assert len(a.split()) == len(b.split()) and abs(len(a) - len(b)) <= 3 and MSG.jaccard(a, b) < 0.5
            assert r["spec"]["message_wid"].split("-")[-2] == own["spec"]["message_wid"].split("-")[-2]            # the same style
            assert r["spec"]["message_wid"].rsplit("-", 2)[0] in own["spec"]["trivials"]
    assert n > 20


def test_every_message_has_at_least_four_tokens_and_solver_a_checks_it(rows_all):
    assert all(len(r["spec"]["message"].split()) >= 4 for r in rows_all)
    from T66 import solver_a
    rec = next(r for r in rows_all if r["gold"] == "YES")
    assert solver_a.gold_a(rec) == "YES"
    short = copy.deepcopy(rec)
    short["spec"]["message"] = "add a guard"
    assert solver_a.gold_a(short) is None


def test_slots_are_the_kinds_own_and_bound_to_the_change():
    ctx = G.Ctx(seed=3, standin=True, pool=BASE, msg_split="all", executor=S.SimExecutor())
    specs = MSG.build_group(ctx, {"gid": "s1", "seed": "s1"}, {"chs": ["CH-5", "CH-9"], "trivial": [2, 2]})
    for s in specs:
        assert sorted(s["slots"]) == sorted(MSG.KIND_SLOTS[s["ch"]]) and "obj" not in s["slots"]
        assert len(s["triv_fns"]) == len(s["trivials"]) and all(f for f in s["triv_fns"])
        for t, f in zip(s["trivials"], s["triv_fns"]):                                                       # a trivial message names the function its hunk sits in
            if t in ("comment", "doc"):
                assert "def %s(" % f in s["diff"]
    ch5 = next(s for s in specs if s["ch"] == "CH-5")
    assert ch5["slots"]["num_new"] > ch5["slots"]["num_old"] and "%s=%d" % (ch5["slots"]["param"], ch5["slots"]["num_new"]) in ch5["diff"]
    ch9 = next(s for s in specs if s["ch"] == "CH-9")
    assert '.append("%s")' % ch9["slots"]["tok"] in ch9["diff"]
    assert not hasattr(MSG, "complete_slots") and not hasattr(G, "SWAP_STYLE_RULE") and not hasattr(G, "LENGTH_MATCH")        # no re-binding, no levers (Q8 R1)



def test_enclosing_function_of_trivial_hunks():
    lines = ["def alpha(x):", "    v = x * 2", "    return v", "", "", "def beta(y):", "    w = y + 1", "    return w"]
    assert MSG.enclosing_fn(lines, (5, 5, ["# c"])) == "beta"            # comment hunk sits on the def line
    assert MSG.enclosing_fn(lines, (6, 6, ['    """d"""'])) == "beta"     # docstring hunk right after the def
    assert MSG.enclosing_fn(lines, (1, 2, ["    v = x*2"])) == "alpha"    # formatting hunk inside the body


def test_plan_group_types_hard_stratum_and_trivial_share():
    plan = [g for g in G.build_plan(total=2400, seed=1) if g["head"] == "MSG"]
    typ = collections.Counter(g["cell"]["type"] for g in plan)
    assert abs(typ["trivial"] / float(len(plan)) - G.TRIV_GROUP_SHARE) < 0.02
    swap = [g for g in plan if g["cell"]["type"] == "swap"]
    same = [g for g in swap if MSG.BLOCK_OF[g["cell"]["chs"][0]] == MSG.BLOCK_OF[g["cell"]["chs"][1]]]
    assert abs(len(same) / float(len(swap)) - G.SAME_FN_SHARE) < 0.02
    assert all(sorted(g["cell"]["styles"]) == ["I", "N"] for g in same)
    assert all(g["cell"]["styles"] == ["N", "N"] for g in plan if g not in same)                              # no one-sided identifier overlap outside the hard stratum
    assert all(frozenset(g["cell"]["chs"]) not in MSG.CONFUSABLE_PAIRS for g in plan) and len(MSG.CONFUSABLE_PAIRS) == 2
    assert all(g["cell"]["styles"][g["cell"]["chs"].index("CH-8")] == "N" for g in plan if "CH-8" in g["cell"]["chs"] and g in same)         # CH-8 style I is the weakest cell for Solver B
    w = collections.Counter(tuple(sorted(g["cell"]["chs"])) for g in same)
    assert w[("CH-1", "CH-10")] > w[("CH-5", "CH-8")] > w[("CH-6", "CH-8")]                                    # kind mix: the p3 kinds are drawn less often
    assert set(tuple(sorted(g["cell"]["chs"])) for g in same) <= set(MSG.SAME_FN_PAIRS) and all(len(g["cell"]["trivial"]) == 2 and min(g["cell"]["trivial"]) >= 1 for g in plan if g["cell"]["type"] == "trivial")


def test_hard_stratum_is_at_least_30_percent_and_trivial_share_at_least_25(rows_all):
    msg = rows_all
    no = [r for r in msg if r["gold"] == "NO"]
    assert sum(1 for r in no if r["spec"]["origin"] == "trivial") / float(len(no)) >= 0.25
    hard = [r for r in msg if (r["meta"]["mech"] or {}).get("ovl") == "high"]
    assert len(hard) / float(len(msg)) >= 0.30
    for r in hard:                                                                                            # true message style N, partner style I naming identifiers of THIS diff
        assert r["spec"]["style"] == "N" and r["spec"]["origin"] in ("own", "swap")
    pairs = collections.defaultdict(dict)
    for r in msg:
        pairs[r["meta"]["pair_id"]][r["gold"]] = r
    for pid, p in pairs.items():
        if (p["NO"]["meta"]["mech"] or {}).get("ovl") == "high":
            assert p["YES"]["spec"]["style"] == "N" and p["NO"]["spec"]["message_wid"].split("-")[-2] == "I"
            assert MSG.BLOCK_OF[p["YES"]["meta"]["ch"]] == MSG.BLOCK_OF[next(r["meta"]["ch"] for r in msg if r["spec"]["message_wid"] == p["NO"]["spec"]["message_wid"] and r["gold"] == "YES")]


def test_k7_dry_run_passes_all_probes():
    """Diagnostic (the binding reads are the pilot and the built family): the message-only, diff-only, joint-length and overlap probes on 2 seeds of dry-run rows."""
    from T66 import gates
    rows = _rows("all", seeds=(1, 2), total=2400)
    r = gates.k7_msg(rows, B=100)
    for name, (auc, upper, _passed) in r["probes"].items():                                                  # the AUC bars (0.55 / 0.60); the probe's own validity checks need the full 4-seed run
        assert auc <= 0.55 and upper <= 0.60, (name, r["probes"])
    assert r["trivial_share_of_no"] >= 0.25



def test_generation_is_deterministic():
    a = [(r["row_id"], r["spec"]["message"]) for r in _rows("dev")]
    b = [(r["row_id"], r["spec"]["message"]) for r in _rows("dev")]
    assert a == b and a


def test_checked_run_passes_the_message_split_through():
    from LP_COMMON import pipeline as pl
    rows, summary, _log, _rep = checked.run(160, 5, pl.TestDoubleHook(), standin=True, msg_split="dev2")
    msg = [r for r in rows if r["head"] == "MSG"]
    allowed = {t["id"] for by in MP.templates(DOC, "dev2").values() for ts in by.values() for t in ts}
    assert msg and {r["spec"]["message_wid"] for r in msg} <= allowed and summary["kept"] == len(rows)
