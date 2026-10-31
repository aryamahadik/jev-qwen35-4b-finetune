"""Build-skeptic tests (Sun 18 Oct): an unsound MERGE witness is no label, the B-view id is opaque."""
import copy

import pytest

from LP_COMMON import sandbox_iface as S
from T66 import dryrun, generator as G, merge as MG, merge_spec as MS, msg_spec as MSG, schema


def _w(passed_a, passed_b, ok=True, runs=3):
    return {"A": {"passed": passed_a, "ok": ok, "runs": runs}, "B": {"passed": passed_b, "ok": ok, "runs": runs}}


def test_merge_witness_labels():
    assert MS.label_from_witness(_w(True, True)) == "YES"
    assert MS.label_from_witness(_w(True, False)) == "NO"
    assert MS.label_from_witness(_w(False, False)) == "NO"


@pytest.mark.parametrize("w", [_w(True, True, ok=False), _w(False, False, ok=False), _w(True, True, runs=2), _w(False, True, runs=None),
                               dict(_w(True, True), B={"passed": True, "ok": False, "runs": 3})])
def test_unsound_merge_witness_is_no_label_not_a_no(w):
    assert MS.label_from_witness(w) is None


def test_a_nondeterministic_executor_cannot_make_a_no_row():
    class Flaky(S.SimExecutor):
        def run(self, requests):
            out = super().run(requests)
            for o in out:
                if o["row_id"].endswith(":B") or ":RK" in o["row_id"]:
                    o["deterministic"] = False
            return out

    ctx = G.Ctx(seed=1, standin=True, executor=Flaky())
    g = {"gid": "g1", "seed": "s1"}
    with pytest.raises(MG.Reject):
        MS.build_group(ctx, g, {"cf": "CF-1", "rks": ["RK1"]})


def test_b_view_id_is_opaque():
    rows, *_ = dryrun.dry_rows(120, seed=3)
    for r in rows:
        bv = schema.b_view(r)
        assert bv["row_id"] != r["row_id"] and not bv["row_id"].endswith(("-a", "-b"))
    pairs = [r for r in rows if r["head"] == "SEMVER" and r["meta"].get("pair_id")]
    assert pairs and all((r["gold"] == "BREAKING") == r["row_id"].endswith("-a") for r in pairs)      # why the real id must not reach B


def _msg_text(f, k):
    """A statement message for MSG form f: style I and TRIV carry {fn}, style N carries no slot (the production rule, generator.msg_form_rule)."""
    return "%s message %d" % (f, k) + ("" if f.endswith("-N") else " about {fn}")


def _pool(msg_texts):
    pool = {"version": 1, "test_only": False, "forms": {}}
    for f, slots in G.form_slots().items():
        if f in MSG.FORMS_MSG:
            pool["forms"][f] = [{"id": "w%03d" % k, "text": _msg_text(f, k)} for k in range(60)]
        else:
            pool["forms"][f] = [{"id": "w%03d" % k, "text": "%s %d %s" % (f, k, " ".join("{%s}" % s for s in slots))} for k in range(60)]
    for f, texts in msg_texts.items():
        pool["forms"][f] = [{"id": "w%03d" % k, "text": t} for k, t in enumerate(texts)]
    return pool


def test_pool_problems_accepts_distinct_statement_messages():
    assert G.pool_problems(_pool({})) == []


def test_pool_problems_rejects_question_frames_shared_across_change_forms():
    """The shipped-style defect: the same 60 question frames serve as the 'commit message' of every change class."""
    frames = ["Does the commit message describe this diff, where the change is in {fn} on the module? #%d" % k for k in range(60)]
    shared = {f: list(frames) for f in MSG.FORMS_MSG}
    bad = G.pool_problems(_pool(shared))
    assert any("shared by more than one change form" in b for b in bad) and any("are questions" in b for b in bad)
    with pytest.raises(Exception):
        G.Ctx(seed=1, standin=False, pool=_pool(shared), executor=S.SimExecutor())          # refused (and SimExecutor refused anyway)
    ctx_err = None
    try:
        G.Ctx(seed=1, standin=False, pool=_pool(shared), executor=object())
    except Exception as e:                                                                      # noqa: BLE001
        ctx_err = e
    assert ctx_err is not None and "wording pool is not usable" in str(ctx_err)


def test_pool_problems_flags_a_single_shared_text_and_a_question_mark():
    base = {f: [_msg_text(f, k) for k in range(60)] for f in MSG.FORMS_MSG}
    assert G.pool_problems(_pool(base)) == []
    first, third = MSG.FORMS_MSG[0], MSG.FORMS_MSG[2]                 # two style-I forms: a text shared by both is refused
    one = dict(base, **{third: [base[first][0]] + base[third][1:]})
    assert any("shared" in b for b in G.pool_problems(_pool(one)))
    q = dict(base, **{first: ["why does %s {fn}?" % first] + base[first][1:]})
    assert any("questions" in b for b in G.pool_problems(_pool(q)))


def test_semver_frames_that_open_as_yes_no_questions_are_refused():
    base = {f: [_msg_text(f, k) for k in range(60)] for f in MSG.FORMS_MSG}
    pool = _pool(base)
    assert G.pool_problems(pool) == []
    pool["forms"]["T66-Q-SEMVER"] = pool["forms"]["T66-Q-SEMVER"] + [{"id": "wx", "text": "Does the rule settle the change to {api}?"}]
    assert any("opens as a yes/no question" in p for p in G.pool_problems(pool))


def test_the_question_frame_pool_alone_is_refused_for_the_message_forms():
    """pools/wording_pool.json still holds the 19 shared QUESTION frames under the MSG change forms (kept as shipped, hashed in HASH_EXPORT); the guard refuses it. The production
    pool is that file with the message forms REPLACED by pools/msg_messages.json (Ctx / msg_pool.wording_pool), tested below."""
    import json
    pool = json.load(open(os.path.join(FAMDIR, "pools", "wording_pool.json")))
    bad = G.pool_problems(pool)
    assert bad and not any("SEMVER" in b for b in bad)


@pytest.mark.parametrize("split", ["all", "dev", "dev2"])
def test_the_production_pool_passes_the_guard_in_every_split(split):
    import json
    from T66 import msg_pool as MP
    base = json.load(open(os.path.join(FAMDIR, "pools", "wording_pool.json")))
    pool = MP.wording_pool(base, MP.load(), split)
    assert G.pool_problems(pool) == []
    ctx = G.Ctx(seed=1, standin=False, pool=base, executor=object(), msg_split=split)             # msg_split replaces the message forms by that half of the shipped pool
    assert ctx.msg_split == split and G.pool_problems(ctx.pool) == []
    want = {t["id"] for body in MP.load()["kinds"].values() for t in body["templates"] if split == "all" or t["split"] == split}
    got = {w["id"] for f in MSG.FORMS_MSG for w in ctx.pool["forms"][f]}
    assert got == want


def test_a_production_context_loading_its_pool_from_a_path_uses_the_message_pool_by_default():
    path = os.path.join(FAMDIR, "pools", "wording_pool.json")
    ctx = G.Ctx(seed=1, standin=False, pool_path=path, executor=object())
    assert ctx.msg_split == "all" and G.pool_problems(ctx.pool) == []
    import json
    base = json.load(open(path))
    with pytest.raises(Exception):                                                                  # a pool passed as given keeps its question-frame message forms: refused
        G.Ctx(seed=1, standin=False, pool=base, executor=object())
    with pytest.raises(Exception):
        G.Ctx(seed=1, standin=False, pool=base, executor=object(), msg_split="train")


import os      # noqa: E402

FAMDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
