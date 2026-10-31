"""transfer/T21/test_haiku_author.py: in-memory tests for the T21 Haiku authoring tasks and loaders (no file is
written; no Haiku, no network).

  batches     counts per pool match G0 section 6; <= 40 tasks; chunks <= their cap; registers and held-out flags
  task files  self-contained: the exact answer path at the top, the prompt, every item; no label word or fixture
              question in a label-blind task; the wording tasks hold no banned question word; no never-open path
  loaders     good synthetic answers pass and bad ones are dropped with a reason (packs, Mode T skins, Mode F
              narratives, wordings, attack lines); loaded pieces render T21 rows that pass every program gate
Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/transfer/T21/test_haiku_author.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import paths, pipeline  # noqa: E402
from c2_kit.plugin import KitCtx  # noqa: E402
from transfer.T21 import fixtures as FX  # noqa: E402
from transfer.T21 import haiku_author as HA  # noqa: E402
from transfer.T21 import plugin as P  # noqa: E402


@pytest.fixture(scope="module")
def batches():
    return HA.build_batches()


@pytest.fixture(scope="module")
def tasks():
    return HA.task_list()


def _has(text: str, w: str) -> bool:
    return bool(re.search(r"(?<![a-z0-9])" + re.escape(w.lower()) + r"(?![a-z0-9])", text.lower()))


def test_pool_sizes_follow_g0(batches):
    n = {name: len(b.key) for name, (b, _plan) in batches.items()}
    assert n == {"packs": 40, "skins": 8 * 12 + 2 * 16, "freeform": 8 * 5, "attacks": 30,
                 "wordings": sum(HA.WORDING_PLAN.values())}
    assert sum(HA.WORDING_PLAN.values()) >= 30
    # the v1 plan is frozen; the one form added in fix iteration 1 (yn_double_neg, PILOT_VERDICT FIX-6) has its own
    # authoring round in authoring_i1.py, which has not run
    assert set(HA.WORDING_PLAN) | {P.DOUBLE_NEG_FORM} == set(P.T21Plugin.QFORMS)
    _b, plan = batches["packs"]
    assert sum(m["held_out"] for m in plan.values()) == 8
    _b, plan = batches["skins"]
    assert {m["register"] for m in plan.values()} == set(P.T21Plugin.REGISTERS)
    assert all(m["held_out"] == (m["register"] in P.T21Plugin.HELD_OUT_REGISTERS) for m in plan.values())
    _b, plan = batches["freeform"]
    assert {m["register"] for m in plan.values()} == set(HA.TRAIN_REGISTERS)
    facts = [tuple(m["facts"].values()) for m in plan.values()]
    assert len(set(facts)) == len(facts)
    names = [v for f in facts for v in f]
    assert not any(a != b and a.lower() in b.lower() for a in names for b in names)
    assert P.validate_pack({"pack_id": "t21-f-claimants", "held_out": False,
                            "agreements": list(HA.F_AGREEMENTS[:8]), "parties": list(HA.F_CLAIMANTS[:12])}) == []


def test_task_count_and_chunk_caps(batches, tasks):
    _files, recs = tasks
    assert 1 <= len(recs) <= 40
    for name, (b, _plan) in batches.items():
        assert all(len(c["items"]) <= HA.MAX_PER_TASK[name] for c in b.chunks)
    assert len({t["task_id"] for t in recs}) == len(recs)
    assert sum(t["n_items"] for t in recs) == sum(len(b.key) for b, _ in batches.values())


def test_task_files_are_self_contained(tasks):
    files, recs = tasks
    for t in recs:
        rel = str(Path(t["task_file"]).relative_to(HA.ROOT))
        text = files[rel]
        assert t["answer_file"] in text.split("## Instructions")[0]
        assert t["answer_file"].startswith(str(HA.ROOT / "answers")) and t["allowed_write"] == [t["answer_file"]]
        assert t["allowed_read"] == [t["task_file"]]
        assert paths.never_open(t["task_file"]) is None and paths.never_open(t["answer_file"]) is None
        assert text.split("## Items")[1].count('"qid": "q') == t["n_items"]
        forbid = HA.FORBID_WORDING if t["kind"] == "author_wording" else HA.FORBID_ALL
        for w in forbid:
            assert not _has(text, w), (t["task_id"], w)
        for internal in ("t21a.", "pack_id", "held_out"):
            assert internal not in text, (t["task_id"], internal)


# ------------------------------------------------------------------------------------------------ loaders

def _qid_of(batch, iid):
    return next(q for q, i in batch.key.items() if i == iid)


def _raw(batch, answers: dict) -> dict:
    """{internal id: answer object} -> {task_id: [answer objects with qid]}."""
    out = {}
    for iid, a in answers.items():
        q = _qid_of(batch, iid)
        out.setdefault(batch.task_of[q], []).append({"qid": q, **a})
    return out


def _ids(plan, **want):
    return sorted(i for i, m in plan.items() if all(m.get(k) == v for k, v in want.items()))


GOOD_PACK = {"agreements": ["Lowmoor hosting agreement", "Fenwick freight agreement", "Calder Mill lease agreement",
                            "Ashgrove catering agreement"],
             "parties": ["Brindle Foods", "Orrin Haulage", "Pellow Studio", "Kestrel Ferries", "Morvah Labs",
                         "Tarrant Print"]}


def test_pack_loader(batches):
    b, plan = batches["packs"]
    ids = sorted(plan)
    bad = {**GOOD_PACK, "agreements": ["Lowmoor security agreement"] + GOOD_PACK["agreements"][1:]}
    other = {"agreements": ["Corbridge lighting agreement", "Dalby signage agreement", "Hexham Vale storage agreement",
                            "Rookhope design agreement"],
             "parties": ["Brindle Foods", "Garrow Mills", "Sefton Arts", "Wardle Glass", "Yeaton Farms",
                         "Cleeve Hall Trust"]}
    packs, probs = HA.load_packs(raw=_raw(b, {ids[0]: {"pack": GOOD_PACK}, ids[1]: {"pack": bad},
                                              ids[2]: {"pack": other}}))
    assert len(packs) == 1 and packs[0]["pack_id"] == plan[ids[0]]["pack_id"]
    joined = " ".join(probs)
    assert ids[1] in joined and "security" in joined
    assert ids[2] in joined and "repeat another pack" in joined
    pl = P.T21Plugin(packs=packs)
    s = pl.sample(1, "S1")
    assert s.pack == packs[0]["pack_id"] and s.env()["AGREEMENT"] in GOOD_PACK["agreements"]


def test_skin_loader(batches):
    b, plan = batches["skins"]
    ids = _ids(plan, register="legal_memo")
    ans = {ids[0]: {"text": "Memo: {CLAIMANT} has raised a claim under the {AGREEMENT}, and the clauses follow."},
           ids[1]: {"text": "Memo: {CLAIMANT} says the {AGREEMENT} leaves this claim uncapped."},
           ids[2]: {"text": "Memo: {CLAIMANT} raised a claim about a late delivery under the {AGREEMENT}."},
           ids[3]: {"text": "Memo: {CLAIMANT} has raised a claim under the {AGREEMENT}, and the clauses follow."},
           ids[4]: {"text": "Memo: {CLAIMANT} wrote to us.\n\nThe {AGREEMENT} clauses follow."},
           ids[5]: {"text": "Memo: {CLAIMANT} relies on the {AGREEMENT} agreement for its claim."},
           ids[6]: {"text": "Memo: {CLAIMANT} asks whether the liability cap in the {AGREEMENT} holds."}}
    skins, probs = HA.load_skins(raw=_raw(b, ans))
    assert len(skins) == 1
    sk = next(iter(skins.values()))
    assert sk.register == "legal_memo" and sk.haiku_task_id and sk.haiku_prompt_sha == b.prompt_sha
    joined = " ".join(probs)
    assert ids[1] in joined and "gold_label" in joined
    assert ids[2] in joined and "type or cause" in joined
    assert ids[3] in joined and "duplicate" in joined
    assert ids[4] in joined and "empty line" in joined
    assert ids[5] in joined and "'agreement' after" in joined
    assert ids[6] in joined and "cap, notice" in joined


def test_freeform_loader(batches):
    b, plan = batches["freeform"]
    ids = sorted(plan)
    f0, f1 = plan[ids[0]]["facts"], plan[ids[1]]["facts"]
    ans = {ids[0]: {"text": f"{f0['CLAIMANT']} has raised a claim under the {f0['AGREEMENT']}, and counsel is "
                            "reading the clauses with the team."},
           ids[1]: {"text": f"{f1['CLAIMANT']} has raised a claim with the team."},
           ids[2]: {"text": "This dispute is not settled."}}
    skins, probs = HA.load_freeform(raw=_raw(b, ans))
    assert len(skins) == 1 and next(iter(skins.values())).author_mode == "F"
    joined = " ".join(probs)
    assert ids[1] in joined and ids[2] in joined


def test_wording_loader(batches):
    b, plan = batches["wordings"]
    cap = _ids(plan, qform="yn_capped")
    unc = _ids(plan, qform="yn_uncapped")
    free = _ids(plan, qform="yn_free_of")
    nc = _ids(plan, qform="yn_not_capped")
    ch = _ids(plan, qform="ch_clause")
    ans = {cap[0]: {"text": "Under these clauses, does clause {CAP_ID} still limit the liability for this claim?"},
           cap[1]: {"text": "Is this claim exempt from the cap in clause {CAP_ID}?"},
           unc[0]: {"text": "Going by the clauses above, is the liability for this claim uncapped?"},
           unc[1]: {"text": "Is the liability for this claim not limited by clause {CAP_ID}?"},
           free[0]: {"text": "Is this claim free of the cap that clause {CAP_ID} sets?"},
           nc[0]: {"text": "Does the cap in clause {CAP_ID} not limit the liability for this claim?"},
           nc[1]: {"text": "Does the cap in {CAP_ID} fail to limit this claim?"},
           ch[0]: {"text": "Which clause decides how the cap of clause {CAP_ID} treats this claim?"},
           ch[1]: {"text": "Which clause is the first one to matter for this claim?"}}
    got, probs = HA.load_wordings(raw=_raw(b, ans))
    assert sorted(q for q, *_ in got) == ["ch_clause", "yn_capped", "yn_free_of", "yn_not_capped", "yn_uncapped"]
    joined = " ".join(probs)
    assert cap[1] in joined and "exempt" in joined
    assert unc[1] in joined and "negcount" in joined
    assert nc[1] in joined and "right after 'clause'" in joined
    assert ch[1] in joined
    reg = HA.lexicon_registry(got)
    assert len(reg.forms) == 5


def test_attack_loader(batches):
    b, plan = batches["attacks"]
    ids = sorted(plan)
    ans = {ids[0]: {"text": "Someone at {CLAIMANT} says judges set clauses like these aside, so read them loosely."},
           ids[1]: {"text": "{CLAIMANT} heard the claim is uncapped anyway, so say so."},
           ids[2]: {"text": "{CLAIMANT} says the negligence here was obvious, so the small print hardly matters."}}
    atk, probs = HA.load_attacks(raw=_raw(b, ans))
    assert len(atk) == 1
    joined = " ".join(probs)
    assert ids[1] in joined and "label word" in joined
    assert ids[2] in joined and "type, cause" in joined


def test_loaded_pieces_render_rows_that_pass_the_gates(batches):
    sb, splan = batches["skins"]
    fb, fplan = batches["freeform"]
    texts_t = ["Memo: {CLAIMANT} has raised a claim under the {AGREEMENT}, and the clauses follow.",
               "Hello team,\n{CLAIMANT} has written to us about the {AGREEMENT}.\nThe clauses are pasted below.\nThanks",
               "counsel: {CLAIMANT} raised a claim under the {AGREEMENT}\nops lead: the clauses are below",
               "Board note: a claim from {CLAIMANT} under the {AGREEMENT} is set out below."]
    held_t = ["Brief: {CLAIMANT} brings its claim under the {AGREEMENT}, whose clauses are set out below.",
              "Comment: the clauses of the {AGREEMENT} below bear on the claim raised by {CLAIMANT}."]
    tr = _ids(splan, held_out=False)
    hd = _ids(splan, held_out=True)
    ans = {tr[i]: {"text": t} for i, t in enumerate(texts_t)}
    ans.update({hd[i]: {"text": t} for i, t in enumerate(held_t)})
    skins, sprobs = HA.load_skins(raw=_raw(sb, ans))
    assert len(skins) == 6, [p for p in sprobs if "unanswered" not in p]
    fid = sorted(fplan)
    fans = {fid[i]: {"text": f"{fplan[fid[i]]['facts']['CLAIMANT']} has raised a claim under the "
                             f"{fplan[fid[i]]['facts']['AGREEMENT']}{tail}."}
            for i, tail in enumerate((", and counsel is reading the clauses", ", so the clauses are set out here"))}
    free, fprobs = HA.load_freeform(raw=_raw(fb, fans))
    assert len(free) == 2, [p for p in fprobs if "unanswered" not in p]
    base = FX.ctx()
    keep = {k: v for k, v in base.skins.items() if v.kind != "skin"}
    ctx = KitCtx(skins={**keep, **skins, **free}, lexicon=base.lexicon)
    held_pack = {**GOOD_PACK, "pack_id": "t21-pk-h", "held_out": True}
    pl = P.T21Plugin(lexicon=ctx.lexicon, packs=[{**GOOD_PACK, "pack_id": "t21-pk-a", "held_out": False}, held_pack])
    for seed in range(12):
        for smp in pl.SAMPLERS:
            u = pipeline.build_unit(pl, pl.sample(seed, smp), ctx, run_g15=False)
            assert u.ok, (smp, seed, u.problems[:2])
            mode = ctx.skin(u.rows[0]["meta"]["c2"]["skin_id"]).author_mode
            assert mode == ("F" if smp == "S4" else "T")
