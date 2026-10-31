"""families/T33/test_dneg_i2.py: the double-negation stage scripts of fix iteration 2 on FABRICATED Haiku answers.

Everything runs in a temp folder under lean/ (the kit's writers only write under lean/; the folder is removed at the
end): authoring tasks -> fabricated authoring answers (good and bad wordings) -> dneg_stage2 -> fabricated G-LEX reads
(one form disagrees in read 2) -> dneg_stage3 (--no-run) -> the supplement is frozen, merged by load_ctx_i2 and
refuses to be rewritten. No Haiku, no model, no network. The frozen pools are only read.
"""
from __future__ import annotations

import itertools
import json
import shutil
import tempfile
from pathlib import Path

import pytest

from c2_kit import polarity as POL
from families.T33 import dneg_i2 as D
from families.T33 import dneg_stage2 as S2
from families.T33 import dneg_stage3 as S3
from families.T33 import haiku_author as H
from families.T33 import plugin as T

SCRATCH = Path(__file__).resolve().parent / "_scratch_i2"

STEP_GOOD = [f"{lead}{frame} step {{STEP}} {mid}{verb} {tail}?"
             for lead, frame, mid, verb, tail in itertools.product(
                 ("", "In the log, "), ("is it not true that", "is it not the case that"),
                 ("of the log does not ", "in the log does not "),
                 ("meet", "satisfy", "reach"), ("its success criterion", "the success criterion"))]
ALL_GOOD = [f"{lead}{frame} not {q} claim in the agent's message {verb} by the log?"
            for lead, frame, q, verb in itertools.product(
                ("", "Going by the log, "), ("is it not true that", "is it not the case that"), ("every", "all"),
                ("is supported", "is backed up", "is borne out"))]
ALL_GOOD = [t.replace("not all claim ", "not all claims ").replace("all claims in", "all claims in")
            .replace("not all claims in the agent's message is", "not all of the claims in the agent's message are")
            for t in ALL_GOOD]
STEP_BAD = ["Isn't it true that step {STEP} doesn't meet its success criterion?",                  # contracted frame
            "Is it not true that step {STEP} does not fail its success criterion?",                # not over a negative
            "Does step {STEP} meet its success criterion?",                                         # no double negation
            "Is it not true that step {STEP} does not meet its success criterion",                  # no question mark
            "Is it not true that the step does not meet its success criterion?"]                    # no {STEP}
ALL_BAD = ["Isn't it true that not every claim in the agent's message is supported by the log?",
           "Is it not true that not every claim in the message is missing from the log?",
           "Is it true that every claim in the message is supported?"]


@pytest.fixture(scope="module")
def work():
    SCRATCH.mkdir(exist_ok=True)
    root = Path(tempfile.mkdtemp(dir=SCRATCH, prefix="dneg_"))
    yield root
    shutil.rmtree(root, ignore_errors=True)


def _write_answers(root: Path, texts_for) -> None:
    tasks_root = root / "tasks"
    tasks = json.loads((tasks_root / "TASKS.json").read_text(encoding="utf-8"))
    b = H.batch_from_disk(tasks_root, tasks["batches"]["wordings"])
    for c in b.chunks:
        ans = [{"qid": it["qid"], "texts": texts_for(b.key[it["qid"]])} for it in c["items"]]
        Path(c["answer_file"]).parent.mkdir(parents=True, exist_ok=True)
        Path(c["answer_file"]).write_text(json.dumps(ans), encoding="utf-8")


def _texts_for(iid: str) -> list:
    _t, _w, qf, j = iid.split("|")
    good, bad = (STEP_GOOD, STEP_BAD) if qf == "yn_dneg_step_ok" else (ALL_GOOD, ALL_BAD)
    j = int(j)
    return good[j * 4:j * 4 + 4] + bad[j % len(bad):j % len(bad) + 2]      # 4 good + 2 bad per item (6 per item)


def test_fabricated_good_wordings_pass_the_polarity_rules():
    for t in STEP_GOOD:
        assert POL.form_problems(T.T33Plugin, "yn_dneg_step_ok", t) == [], t
    for t in ALL_GOOD:
        assert POL.form_problems(T.T33Plugin, "yn_dneg_all_supported", t) == [], t
    assert POL.form_problems(T.T33Plugin, "yn_dneg_step_ok", STEP_BAD[0])             # contracted frame (P3)
    assert POL.form_problems(T.T33Plugin, "yn_dneg_step_ok", STEP_BAD[1])             # not over a negative predicate (P1)


def test_task_files_are_self_contained_and_polarity_aware(work):
    tasks = D.write_tasks(work)
    assert len(tasks) == 4
    assert all(str(work / "tasks") in t["task_file"] and str(work / "tasks") in t["answer_file"] for t in tasks)
    items = 0
    for t in tasks:
        c = json.loads(Path(t["task_file"]).read_text(encoding="utf-8"))
        assert c["instructions"] and c["answer_format"] and c["answer_file"] == t["answer_file"]
        assert '"qid"' in c["answer_format"] and '"texts"' in c["answer_format"]
        for it in c["items"]:
            items += 1
            assert "exactly two nots" in it["brief"] and "contracted" in it["brief"]
    assert items == 2 * D.ITEMS_PER_FORM
    assert 2 * D.ITEMS_PER_FORM * H.FORMS_PER_ITEM >= 4 * D.MIN_ADMITTED * 2        # 4x the admitted target, per form


def test_stage2_admits_good_wordings_drops_bad_and_writes_two_reads(work):
    _write_answers(work, _texts_for)
    rep = S2.run(work)
    assert rep["candidates_per_form"] == {"yn_dneg_step_ok": 24, "yn_dneg_all_supported": 24}, rep["drops"]
    assert not rep["short_forms"]
    # 6 wordings per item, 4 good + 2 bad; the bad ones repeat across items (counted as duplicates after the first)
    assert set(rep["drops"]) <= {"wording_polarity", "wording_shape", "wording_words", "wording_negation",
                                 "duplicate"}, rep["drops"]
    assert rep["drops"]["wording_polarity"] and rep["drops"]["wording_shape"] and rep["drops"]["wording_words"]
    total = sum(len(_texts_for(f"t33|wording|{q}|{j}")) for q in D.FORMS for j in range(D.ITEMS_PER_FORM))
    assert sum(rep["drops"].values()) == total - 48                      # every text is admitted or dropped with a reason
    glex = json.loads((work / "glex_tasks" / "TASKS.json").read_text(encoding="utf-8"))
    assert glex["reads_per_form"] == 2 and set(glex["batches"]) == {"read0", "read1"}
    kinds = {t["kind"] for t in rep["glex_tasks"]}
    assert kinds == {"extract_lex:read0", "extract_lex:read1"}
    for t in rep["glex_tasks"]:
        assert Path(t["task_file"]).is_file() and str(work / "glex_tasks") in t["answer_file"]


def _glex_answers(work: Path, disagree_form_text: str | None) -> str | None:
    gl = json.loads((work / "glex_tasks" / "TASKS.json").read_text(encoding="utf-8"))
    pieces = H.load_pieces(work / "tasks")
    reg = pieces["registry"]
    decoy = reg.sems["q.t33.x_done_only"].meaning
    victim = None
    for name, bid in gl["batches"].items():
        b = H.batch_from_disk(work / "glex_tasks", bid)
        for c in b.chunks:
            ans = []
            for it in c["items"]:
                f = reg.forms[b.key[it["qid"]]]
                choice = reg.sems[f.sem_id].meaning
                if name == "read1" and victim is None and f.sem_id.endswith("yn_dneg_all_supported"):
                    victim, choice = f.form_id, decoy              # one form fails G-LEX in its second read
                ans.append({"qid": it["qid"], "choice": choice})
            Path(c["answer_file"]).write_text(json.dumps(ans), encoding="utf-8")
    return victim


def test_stage3_freezes_the_2_of_2_wordings_and_the_loader_merges_them(work):
    victim = _glex_answers(work, None)
    pools, out = work / "pools", work / "pilot_i2"
    pools.mkdir()
    rep = S3.run(work, pools_dir=pools, out=out, no_run=True)
    assert rep["freeze"] == "written" and not rep["short_forms"], rep["verdict"]
    assert rep["admitted_per_form"] == {"yn_dneg_step_ok": 24, "yn_dneg_all_supported": 23}
    sup = json.loads((pools / D.SUPPLEMENT).read_text(encoding="utf-8"))
    assert victim not in {f["form_id"] for f in sup["lexicon_forms"]}
    assert all(f["status"] == "admitted" and len(f["extractions"]) == 2 for f in sup["lexicon_forms"])
    fz = json.loads((pools / D.FREEZE).read_text(encoding="utf-8"))
    assert set(fz["frozen_pools_sha256"]) == set(D.FROZEN_FILES) and fz["n_skins"] == 47
    pending = (out / "G13_PENDING.txt").read_text(encoding="utf-8").splitlines()
    assert len([x for x in pending if not x.startswith("#")]) == 47
    # the loader: frozen pools + supplement, the frozen files untouched
    ctx, packs, voices = D.load_ctx_i2(H.POOLS, pools_dir=pools)
    base_ctx, _p, _v = D._BASE_LOAD(H.POOLS)
    assert len(ctx.skins) == len(base_ctx.skins) + 47 and len(ctx.lexicon.forms) == len(base_ctx.lexicon.forms) + 47
    new = [s for s in ctx.skins.values() if s.kind == "wording" and s.qform in D.FORMS]
    assert len(new) == 47 and all(ctx.lexicon.status(f) == "admitted" for s in new for f in s.lexicon_ids)
    for q in D.FORMS:
        assert sum(1 for s in new if s.qform == q) >= D.MIN_ADMITTED
    assert D.load_ctx_i2(H.POOLS, pools_dir=work / "no_such_pools")[0].skins.keys() == base_ctx.skins.keys()
    # append-and-freeze: the same content is a no-op, other content is refused, a tampered file is detected
    assert S3.run(work, pools_dir=pools, out=out, no_run=True)["freeze"] == "unchanged"
    with pytest.raises(RuntimeError):
        D.freeze_supplement([], [], {}, pools_dir=pools)
    original = (pools / D.SUPPLEMENT).read_text(encoding="utf-8")
    (pools / D.SUPPLEMENT).write_text(original + " ", encoding="utf-8")
    with pytest.raises(RuntimeError):
        D.read_supplement(pools)
    (pools / D.SUPPLEMENT).write_text(original, encoding="utf-8")            # the next test reads the frozen file


def test_the_generator_draws_the_supplement_wordings_and_every_gate_holds(work):
    """End to end on the fabricated supplement: with the merged ctx the sampler asks the double-negation forms (not the
    positive fallback) and solver A == solver B, G3 and the relations hold on those rows."""
    from c2_kit import pipeline
    ctx, packs, voices = D.load_ctx_i2(H.POOLS, pools_dir=work / "pools")
    pl = T.T33Plugin(lexicon=ctx.lexicon, packs=packs, voices=voices)
    seen = {q: 0 for q in D.FORMS}
    for seed in range(260):
        for smp in ("S1", "S3"):
            res = pipeline.build_unit(pl, pl.sample(seed, smp), ctx, run_g15=False)
            assert res.ok, res.problems[:2]
            for r in res.rows:
                qf = ctx.skin(r["meta"]["wording_id"]).qform
                seen[qf] = seen.get(qf, 0) + 1
    assert all(seen[q] >= 3 for q in D.FORMS), seen


def test_stage3_stops_when_a_form_has_fewer_than_8_admitted(work):
    # a read pair that rejects every all_supported form: the form falls under 8, nothing is frozen
    gl = json.loads((work / "glex_tasks" / "TASKS.json").read_text(encoding="utf-8"))
    reg = H.load_pieces(work / "tasks")["registry"]
    decoy = reg.sems["q.t33.x_done_only"].meaning
    for _n, bid in gl["batches"].items():
        b = H.batch_from_disk(work / "glex_tasks", bid)
        for c in b.chunks:
            ans = [{"qid": it["qid"], "choice": decoy if reg.forms[b.key[it["qid"]]].sem_id.endswith("all_supported")
                    else reg.sems[reg.forms[b.key[it["qid"]]].sem_id].meaning} for it in c["items"]]
            Path(c["answer_file"]).write_text(json.dumps(ans), encoding="utf-8")
    pools = work / "pools_short"
    pools.mkdir()
    rep = S3.run(work, pools_dir=pools, out=work / "pilot_i2_short", no_run=True)
    assert rep["short_forms"] == {"yn_dneg_all_supported": 0} and rep["freeze"] is None
    assert rep["verdict"].startswith("STOP") and not (pools / D.SUPPLEMENT).exists()
