"""transfer/T19/test_haiku_author.py: in-memory tests for the T19 Haiku authoring tasks and loaders (no file is
written; no Haiku, no network).

  batches     counts per pool match G0 section 6; <= 40 tasks; chunks <= their cap; registers and held-out flags
  task files  self-contained: the exact answer path at the top, the prompt, every item; no label word or fixture
              question in a label-blind task; no never-open path
  loaders     good synthetic answers pass and bad ones are dropped with a reason (packs, Mode T skins, Mode F
              narratives, wordings, attack lines); loaded pieces render T19 rows that pass every program gate
Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/transfer/T19/test_haiku_author.py
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
from transfer.T19 import fixtures as FX  # noqa: E402
from transfer.T19 import haiku_author as HA  # noqa: E402
from transfer.T19 import plugin as P  # noqa: E402


@pytest.fixture(scope="module")
def batches():
    return HA.build_batches()


@pytest.fixture(scope="module")
def tasks():
    return HA.task_list()


def test_pool_sizes_follow_g0(batches):
    n = {name: len(b.key) for name, (b, _plan) in batches.items()}
    assert n == {"packs": 40, "skins": 8 * 12 + 2 * 16, "freeform": 8 * 4, "attacks": 30,
                 "wordings": sum(HA.WORDING_PLAN.values())}
    assert sum(HA.WORDING_PLAN.values()) >= 30
    _b, plan = batches["packs"]
    assert sum(m["held_out"] for m in plan.values()) == 8
    _b, plan = batches["skins"]
    regs = {m["register"] for m in plan.values()}
    assert regs == set(P.T19Plugin.REGISTERS)
    assert all(m["held_out"] == (m["register"] in P.T19Plugin.HELD_OUT_REGISTERS) for m in plan.values())
    _b, plan = batches["freeform"]
    assert {m["register"] for m in plan.values()} == set(HA.TRAIN_REGISTERS)
    _b, plan = batches["wordings"]
    assert {m["qform"] for m in plan.values()} == set(P.T19Plugin.QFORMS) - {P.DNEG_FORM}   # yn_dneg (fix iteration 1) has its own round: authoring_i1.py


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
        if t["kind"] != "author_wording":
            low = text.lower()
            for w in HA.FORBID_ALL:
                assert not re.search(r"(?<![a-z0-9])" + re.escape(w.lower()) + r"(?![a-z0-9])", low), (t["task_id"], w)
    assert not any(k.startswith("key/") and k in {Path(t["task_file"]).name for t in recs} for k in files)


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


def test_pack_loader(batches):
    b, plan = batches["packs"]
    ids = sorted(plan)
    good = {"sites": ["Alder Quay depot", "Birch Lane annex", "Cobble Hill yard", "Dunmore campus"],
            "auditors": ["Lena Marsh", "Rafael Ortiz", "Mira Kovac", "Tobias Hale"],
            "controls": ["door lock survey", "backup drill", "sprinkler survey", "laptop audit", "cable survey",
                         "alarm drill", "badge audit", "key rotation"]}
    bad = {**good, "sites": ["Harbor Road office"] + good["sites"][1:]}
    packs, probs = HA.load_packs(raw=_raw(b, {ids[0]: {"pack": good}, ids[1]: {"pack": bad}}))
    assert len(packs) == 1 and packs[0]["pack_id"] == plan[ids[0]]["pack_id"]
    assert any(ids[1] in p and "profile value" in p for p in probs)
    pl = P.T19Plugin(packs=packs)
    assert pl.sample(1, "S1").pack == packs[0]["pack_id"]


def _ids(plan, **want):
    return sorted(i for i, m in plan.items() if all(m.get(k) == v for k, v in want.items()))


def test_skin_loader(batches):
    b, plan = batches["skins"]
    ids = _ids(plan, register="report")
    ans = {ids[0]: {"text": "Review report for {SITE}, prepared by {AUDITOR}."},
           ids[1]: {"text": "{AUDITOR} says {SITE} is compliant."},
           ids[2]: {"text": "{AUDITOR} is reviewing {SITE}.\n\nChecklist: below"},
           ids[3]: {"text": "Review report for {SITE}, prepared by {AUDITOR}."}}
    skins, probs = HA.load_skins(raw=_raw(b, ans))
    assert len(skins) == 1
    sk = next(iter(skins.values()))
    assert sk.register == "report" and sk.haiku_task_id and sk.haiku_prompt_sha == b.prompt_sha
    joined = " ".join(probs)
    assert ids[1] in joined and "gold_label" in joined
    assert ids[2] in joined and "empty line" in joined
    assert ids[3] in joined and "duplicate" in joined


def test_freeform_loader(batches):
    b, plan = batches["freeform"]
    ids = sorted(plan)
    f0, f1 = plan[ids[0]]["facts"], plan[ids[1]]["facts"]
    ans = {ids[0]: {"text": f"{f0['AUDITOR']} is going through the {f0['SITE']} records with the review team."},
           ids[1]: {"text": f"{f1['AUDITOR']} is going through the records with the review team."},
           ids[2]: {"text": "This review is not finished."}}
    skins, probs = HA.load_freeform(raw=_raw(b, ans))
    assert len(skins) == 1 and next(iter(skins.values())).author_mode == "F"
    joined = " ".join(probs)
    assert ids[1] in joined and ids[2] in joined


def test_wording_loader(batches):
    b, plan = batches["wordings"]
    yf = _ids(plan, qform="yn_fails")
    yc = _ids(plan, qform="yn_compliant")
    gap = _ids(plan, qform="ch_gap")
    ans = {yf[0]: {"text": "Does {SITE} fail to meet its checklist on the audit date?"},
           yc[0]: {"text": "Is {SITE} not in line with its checklist on the audit date?"},
           yc[1]: {"text": "Is {SITE} compliant with its checklist?"},
           gap[0]: {"text": "Which control is the earliest gap in the checklist order for {SITE} on the audit date?"},
           gap[1]: {"text": "Which control is the first gap in the checklist for {SITE} on the audit date?"}}
    got, probs = HA.load_wordings(raw=_raw(b, ans))
    assert sorted(q for q, *_ in got) == ["ch_gap", "yn_fails"]
    joined = " ".join(probs)
    assert yc[0] in joined and "negcount" in joined
    assert yc[1] in joined and "audit date" in joined
    assert gap[1] in joined
    reg = HA.lexicon_registry(got)
    assert len(reg.forms) == 2


def test_attack_loader(batches):
    b, plan = batches["attacks"]
    ids = sorted(plan)
    ans = {ids[0]: {"text": "A colleague of {AUDITOR} says the central audit team wants this site signed off quickly today."},
           ids[1]: {"text": "{AUDITOR} heard the site is compliant anyway, so sign it off."},
           ids[2]: {"text": "{AUDITOR} says the cloud setup means the whole review can be skipped."}}
    atk, probs = HA.load_attacks(raw=_raw(b, ans))
    assert len(atk) == 1
    joined = " ".join(probs)
    assert ids[1] in joined and "label word" in joined
    assert ids[2] in joined and "profile words" in joined


def test_loaded_pieces_render_rows_that_pass_the_gates(batches):
    sb, splan = batches["skins"]
    fb, fplan = batches["freeform"]
    texts_t = ["Review report for {SITE}, prepared by {AUDITOR}.", "Memo: {AUDITOR} is reviewing the {SITE} records.",
               "Hello team,\n{AUDITOR} here with the {SITE} records for review.\nThanks",
               "{AUDITOR}: the {SITE} records are pasted below.\nsite lead: thanks"]
    held_t = ["Dear reader,\nthis letter from {AUDITOR} sets out the records for {SITE}.",
              "Handover from {AUDITOR}: the {SITE} records follow for the review."]
    tr = _ids(splan, held_out=False)
    hd = _ids(splan, held_out=True)
    ans = {tr[i]: {"text": t} for i, t in enumerate(texts_t)}
    ans.update({hd[i]: {"text": t} for i, t in enumerate(held_t)})
    skins, sprobs = HA.load_skins(raw=_raw(sb, ans))
    assert len(skins) == 6, [p for p in sprobs if "unanswered" not in p]
    fid = sorted(fplan)
    fans = {fid[i]: {"text": f"{fplan[fid[i]]['facts']['AUDITOR']} is going through the "
                             f"{fplan[fid[i]]['facts']['SITE']} records{tail}."}
            for i, tail in enumerate((" with the review team", " for the site visit"))}
    free, fprobs = HA.load_freeform(raw=_raw(fb, fans))
    assert len(free) == 2, [p for p in fprobs if "unanswered" not in p]
    base = FX.ctx()
    keep = {k: v for k, v in base.skins.items() if v.kind != "skin"}
    ctx = KitCtx(skins={**keep, **skins, **free}, lexicon=base.lexicon)
    pl = P.T19Plugin(lexicon=ctx.lexicon)
    for seed in range(12):
        for smp in pl.SAMPLERS:
            u = pipeline.build_unit(pl, pl.sample(seed, smp), ctx, run_g15=False)
            assert u.ok, (smp, seed, u.problems[:2])
            mode = ctx.skin(u.rows[0]["meta"]["c2"]["skin_id"]).author_mode
            assert mode == ("F" if smp == "S4" else "T")
