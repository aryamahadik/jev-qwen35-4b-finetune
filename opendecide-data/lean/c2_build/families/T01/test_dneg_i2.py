"""families/T01/test_dneg_i2.py: dneg_i2 / dneg_stage2 / dneg_stage3 on FABRICATED answers in a temp dir (no Haiku, no model).

The fabricated wordings are built from the plan of each item (frame, lead-in, inner phrasing, slot set); the fabricated G-LEX
reads pick the form's own meaning (or, in the rejection cases, another one). Nothing is written under families/T01/haiku or pools_v2.
  ../../.venv/bin/python -B -m pytest -q families/T01/test_dneg_i2.py      (from lean/c2_build)
"""
from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pytest  # noqa: E402

from c2_kit.lexicon import question_sem  # noqa: E402
from families.T01 import dneg_i2 as D  # noqa: E402
from families.T01 import dneg_stage2 as S2  # noqa: E402
from families.T01 import dneg_stage3 as S3  # noqa: E402
from families.T01 import freeze_v2 as FV  # noqa: E402
from families.T01 import plugin as P  # noqa: E402

@pytest.fixture()
def tmp_path():
    """The kit's writers only write under lean/ (c2_kit.paths), so the temp dir is a scratch folder next to the family,
    removed afterwards."""
    d = Path(__file__).resolve().parent / f"_scratch_dneg_i2_{os.getpid()}"
    d.mkdir(parents=True, exist_ok=True)
    yield d
    shutil.rmtree(d, ignore_errors=True)


PREDS = {
    "yn_dneg_over": ("is not over the stay limit", "is not above the stay limit", "is not beyond the stay limit",
                     "does not exceed the stay limit"),
    "yn_dneg_timely": ("was not filed in time", "was not filed on or before the final day", "was not submitted in time",
                       "was not filed by the final day of the filing period"),
    "yn_dneg_covered": ("is not covered", "is not covered under the cover rule", "is not a covered loss",
                        "is not one that the policy covers"),
    "yn_dneg_quotes": ("does not need written quotes", "does not call for written quotes",
                       "does not require written quotes", "does not have to get written quotes"),
    "yn_dneg_on_time": ("was not on time", "was not counted as received on time", "was not on time under the receipt rule",
                        "was not received on time under the receipt rule"),
}
CASH = ("required", "needed", "called for", "due")


def fabricate(meta: dict) -> str:
    q, s, k = meta["qform"], set(meta["slots"]), meta["inner"]
    if q == "yn_dneg_over":
        subj = "{PERSON}" if "PERSON" in s else "the person in file {REF}"
        tail = (" in file {REF}" if "PERSON" in s and "REF" in s else "") + (" on {REF_DATE}" if "REF_DATE" in s else "")
        body = f"{subj} {PREDS[q][k]}{tail}"
    elif q == "yn_dneg_timely":
        body = "the {ACTION}" + (" from {PERSON}" if "PERSON" in s else "") + (" in case {REF}" if "REF" in s else "") \
            + f" {PREDS[q][k]}"
    elif q == "yn_dneg_covered":
        subj = "the {PERIL} loss" if "PERIL" in s else "the loss"
        body = subj + (" of {PERSON}" if "PERSON" in s else "") + (" under policy {REF}" if "REF" in s else "") \
            + f" {PREDS[q][k]}"
    elif q == "yn_dneg_quotes":
        subj = "the request from {PERSON}" if "PERSON" in s else "request {REF}"
        body = subj + (" in log {REF}" if "PERSON" in s and "REF" in s else "") + f" {PREDS[q][k]}"
    elif q == "yn_dneg_cash_report":
        day = "for {DAY}" if "DAY" in s else "for the day"
        body = f"no cash report is {CASH[k]} {day}" + (" for {PERSON}" if "PERSON" in s else "") \
            + (" in ledger {REF}" if "REF" in s else "")
    else:
        subj = "the response from {PERSON}" if "PERSON" in s else "the response"
        body = subj + (" to notice {REF}" if "REF" in s else "") + f" {PREDS[q][k]}"
    text = f"{meta['frame']} {body}?"
    if meta["lead"]:
        text = f"{meta['lead']} {text}"
    return text[0].upper() + text[1:]


def write_authoring_answers(root: Path, bad_iid: str | None = None) -> dict:
    b, plan = D.build_batch()
    texts = {}
    for c in b.chunks:
        out = []
        for it in c["items"]:
            iid = b.key[it["qid"]]
            t = fabricate(plan[iid])
            if iid == bad_iid:
                t = "Isn't it true that {PERSON} is not over the stay limit?"        # contracted frame, wrong slots
            texts[iid] = t
            out.append({"qid": it["qid"], "text": t})
        p = Path(root) / b.answer_path(c["task_id"])
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(out), encoding="utf-8")
    return texts


def write_glex_answers(root: Path, *, wrong=(), skip_reads=()) -> None:
    """Fabricated reads: every item answered with its own meaning; `wrong` = {(read, form id)} answered with another meaning;
    `skip_reads` = reads whose answer files are not written."""
    state = json.loads((Path(root) / "stage2_state.json").read_text(encoding="utf-8"))
    reg, _fids, _d = D.glex_registry(state["candidates"])
    for label, b in D.glex_batches(reg, [c["form_id"] for c in state["candidates"]]):
        if label in skip_reads:
            continue
        for c in b.chunks:
            out = []
            for it in c["items"]:
                fid = b.key[it["qid"]]
                right = reg.sems[reg.forms[fid].sem_id].meaning
                pick = right if (label, fid) not in wrong else next(m for m in it["choices"] if m != right)
                assert right in it["choices"]
                out.append({"qid": it["qid"], "meaning": pick})
            p = Path(root) / "glex_tasks" / b.answer_path(c["task_id"])
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(out), encoding="utf-8")


@pytest.fixture()
def staged(tmp_path):
    root = tmp_path / "dneg_i2"
    D.write_tasks(root)
    texts = write_authoring_answers(root, bad_iid="t01d2.wording.yn_dneg_over.000")
    rep = S2.run(root)
    return root, texts, rep


def test_tasks_are_self_contained(tmp_path):
    root = tmp_path / "dneg_i2"
    tasks = D.write_tasks(root)
    assert len(tasks) == 8 and sum(t["n_items"] for t in tasks) == 6 * D.N_PER_FORM == 192
    for t in tasks:
        text = Path(t["task_file"]).read_text(encoding="utf-8")
        assert t["answer_file"] in text and "## Answer format" in text and '"qid"' in text
        assert "TWO negations" in text and "is it not the case that" in text
        assert "answer" not in json.dumps(json.loads(text.split("```json")[1].split("```")[0])).lower().replace("answer file", "")


def test_stage2_admits_and_writes_two_reads(staged):
    root, texts, rep = staged
    assert not rep["short_forms"], rep["short_forms"]
    assert all(n >= D.MIN_ADMITTED for n in rep["candidates_per_form"].values()), rep["first_failing_rule_counts"]
    assert any("P3" in x or "negcount" in x or "contracted" in x.lower() for _i, v in S2.read_authoring(root)[1] for x in v)
    gl = json.loads((root / "glex_tasks" / "TASKS.json").read_text(encoding="utf-8"))
    assert gl["reads"] == list(D.GLEX_READS) and set(gl["batches"]) == set(D.GLEX_READS)
    by_read = {r: [t for t in gl["tasks"] if t["read"] == r] for r in D.GLEX_READS}
    assert all(by_read.values()) and not ({t["task_id"] for t in by_read[D.GLEX_READS[0]]}
                                         & {t["task_id"] for t in by_read[D.GLEX_READS[1]]})
    for t in gl["tasks"]:
        assert t["answer_file"] in Path(t["task_file"]).read_text(encoding="utf-8")


def test_stage2_short_form_is_reported(tmp_path):
    root = tmp_path / "dneg_i2"
    D.write_tasks(root)
    texts = write_authoring_answers(root)
    b, plan = D.build_batch()
    for c in b.chunks:                    # the over form answers 5 of 32 with the contracted frame: < 8 left
        p = Path(root) / b.answer_path(c["task_id"])
        ans = json.loads(p.read_text())
        for a in ans:
            if plan[b.key[a["qid"]]]["qform"] == "yn_dneg_over":
                a["text"] = "Isn't it true that {PERSON} is over the limit?"
        p.write_text(json.dumps(ans))
    rep = S2.run(root)
    assert "yn_dneg_over" in rep["short_forms"] and S2.main(["--root", str(root)]) == 1


def test_stage3_admits_freezes_and_merges(staged, tmp_path):
    root, _texts, _rep = staged
    write_glex_answers(root)
    pools, out = tmp_path / "pools", tmp_path / "out"
    pools.mkdir()
    rep = S3.run(root, pools_dir=pools, out=out, no_run=True)
    assert rep["freeze"] == "written" and not rep["short_forms"], rep
    assert all(n >= D.MIN_ADMITTED for n in rep["admitted_per_form"].values())
    assert (out / "G13_PENDING.txt").read_text().count("\n") > 6
    assert D.freeze_supplement(S3.supplement_of(S3.admit(root)), pools_dir=pools) == "unchanged"
    sup = D.read_supplement(pools)
    ctx = D.merge(_base_ctx(), sup)
    plug = P.T01(lexicon=ctx.lexicon)
    assert all(plug.dneg_ok[q] for q in P.DNEG_FORMS.values())
    assert ctx.lexicon.gate([w["form_id"] for w in sup["wordings"]])["pass"]
    assert D.read_supplement(tmp_path / "nowhere") is None
    (pools / D.SUPPLEMENT).write_text((pools / D.SUPPLEMENT).read_text() + " ")        # drift is refused
    with pytest.raises(RuntimeError):
        D.read_supplement(pools)


def test_stage3_rejects_one_read_miss_and_stops_on_missing_reads(staged, tmp_path):
    root, _texts, _rep = staged
    state = json.loads((root / "stage2_state.json").read_text(encoding="utf-8"))
    victim = next(c for c in state["candidates"] if c["qform"] == "yn_dneg_covered")
    write_glex_answers(root, wrong={(D.GLEX_READS[1], victim["form_id"])})
    got = S3.admit(root)
    kept = {c["form_id"] for c in got["keep"]}
    assert victim["form_id"] not in kept and got["rejected"].get("yn_dneg_covered:rejected") == 1
    assert all(n >= D.MIN_ADMITTED for n in got["per_form"].values())
    # read 2 never answered: no vote, nothing admitted, nothing frozen
    for f in (root / "glex_tasks" / "answers").glob("*.json"):
        if f.stem in {t["task_id"] for t in json.loads((root / "glex_tasks" / "TASKS.json").read_text())["tasks"]
                      if t["read"] == D.GLEX_READS[1]}:
            f.unlink()
    pools = tmp_path / "pools"
    pools.mkdir()
    rep = S3.run(root, pools_dir=pools, out=tmp_path / "out", no_run=True)
    assert rep["verdict"].startswith("STOP") and not list(pools.iterdir()) and sum(rep["admitted_per_form"].values()) == 0


def _base_ctx():
    return D._BASE_MAKE_CTX(FV.load_pools())


def test_sem_declared_for_every_form():
    reg, _f, _d = D.glex_registry([])
    for q in D.FORMS:
        assert question_sem("T01", q) in reg.sems
