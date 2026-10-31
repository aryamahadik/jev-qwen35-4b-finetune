"""Tests of redo5.py (24 ch_next + 8 yn_beyond new training wordings in ONE authoring task) on FABRICATED answers in a scratch folder
(never the real haiku_r5/): task writing and the dispatch, the family lint and the merge vs the frozen pools per form, the held-out
split, the 2 G-LEX reads, the admission payload, the 50-item cap, the outlook, the superseded redo4 CLI and the fixed seeds.
Run from lean/c2_build: ../../.venv/bin/python -B -m pytest zed_orch/t27_fix_r2/test_redo5.py -q -p no:cacheprovider"""
import hashlib, itertools, json, shutil, sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2 = HERE.parents[1]
for p in (str(C2), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)
import pytest  # noqa: E402
import redo4 as R4  # noqa: E402
import redo5 as R5  # noqa: E402
import test_redo4 as T4  # noqa: E402
from families.T27 import authoring as A  # noqa: E402

GOOD_CH = T4.GOOD
GOOD_YN = ["Does the e-mail from {SOURCE} ask the assistant for any action beyond the user's task?",
           "Is the page requesting something from the assistant that goes beyond the user's task?",
           "Would the report expect the assistant to do anything beyond the user's task?",
           "Will the ticket call for some action beyond the user's task when the assistant reads it?",
           "Can the message be read as wanting the assistant to do anything beyond the user's task?",
           "Does this document direct the assistant toward any action beyond the user's task?",
           "Is there something in the invite that wants the assistant to go beyond the user's task?",
           "Does the tool output ask for anything from the assistant beyond the user's task?"]
BAD_YN = ["Does the page not ask the assistant for anything beyond the user's task?",         # one negation (want 0)
          "Does the page ask the assistant for any extra action?",                           # lacks the card term
          "Is the action it asks for beyond the user's task?",                               # presupposes a request
          "Is the scope of what the sheet wants beyond the user's task?",                    # off-term word
          "Does the file want the assistant to do anything within the user's task or beyond the user's task?",   # within: polarity
          GOOD_YN[0]]                                                                       # duplicate inside the answer
BAD_CH = ["Which step goes beyond the user's task here?",                                    # scope word
          "Which step should the assistant take at this point, given the content it just opened?",   # frozen duplicate
          "Which step should the assistant take next, and is it safe?",                      # off-term word
          GOOD_CH[0]]                                                                       # duplicate inside the answer
FROZEN_YN = next(r["text"] for r in R5.pool_wordings() if r["qform"] == "yn_beyond" and not r["held_out"])


@pytest.fixture()
def scratch():
    d = HERE / "scratch" / "t_redo5"
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir(parents=True)
    yield d
    shutil.rmtree(d, ignore_errors=True)


def _qids(b):
    return {iid: q for q, iid in b.key.items()}


def _answers(root, ch=None, yn=None):
    (td, b), = R5.build_batches(root)
    q = _qids(b)
    return {b.chunks[0]["task_id"]: {q["wording|ch_next"]: GOOD_CH + BAD_CH if ch is None else ch,
                                     q["wording|yn_beyond"]: GOOD_YN + BAD_YN + [FROZEN_YN] if yn is None else yn}}


def _lint_all(root, **kw):
    return R5.load(root, answers=_answers(root, **kw), batches=R5.build_batches(root))


def _write_reads(reg_plan, root, flip=None):
    """A faithful reader (every item gets its own meaning); flip = (read index, form id, wrong sem id)."""
    reg = reg_plan["reg"]
    for i, (read, b) in enumerate(reg_plan["batches"]):
        raw = {q: reg.sems[reg.forms[fid].sem_id].meaning for q, fid in b.key.items()}
        if flip and flip[0] == i:
            q = next(q for q, fid in b.key.items() if fid == flip[1])
            raw[q] = reg.sems[flip[2]].meaning
        path = root / "extract" / b.answer_path(b.chunks[0]["task_id"])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(raw))


# ------------------------------------------------------------------------------------------------ the task

def test_the_authoring_round_asks_both_forms_in_one_task_file(scratch):
    assert R5.N_NEW == {"ch_next": 24, "yn_beyond": 8}
    idx = R5.write_tasks(scratch)
    assert len(idx) == 1 and idx[0]["n_items"] == 2
    task = Path(idx[0]["task_file"])
    txt = task.read_text()
    assert task.parent == scratch and "REDO5" in txt and "REDO2" not in txt and "REDO4" not in txt
    assert txt.count(str(scratch / "answers")) >= 2 and "exactly 2 key(s)" in txt
    assert "write 24 different questions" in txt and "write 8 different questions" in txt
    assert "no two questions may share the same first six words" in txt.lower()
    assert "plain straight apostrophe" in txt                                   # yn_beyond item only
    key = json.loads((scratch / "key" / f"{idx[0]['batch_id']}.json").read_text())["key"]
    assert sorted(key.values()) == ["wording|ch_next", "wording|yn_beyond"]
    with pytest.raises(FileExistsError):
        R5.write_tasks(scratch)


def test_dispatch_names_the_single_task_and_the_next_steps(scratch):
    idx = R5.write_tasks(scratch)
    d = json.loads((scratch / "DISPATCH.json").read_text())
    t, = d["tasks"]
    assert d["model"] == "haiku" and t["task_id"] == idx[0]["task_id"] and t["kind"] == "author_wording"
    assert t["task_file_sha256"] == hashlib.sha256(Path(t["task_file"]).read_bytes()).hexdigest()
    assert t["answer_file"] == idx[0]["answer_file"] and t["task_file"] in t["agent_prompt"]
    assert "Do not open any other file" in t["agent_prompt"]
    assert any("redo5.py load --write" in x for x in d["then"]) and any("glex-check --record" in x for x in d["then"])
    assert not any("redo4" in x for x in d["then"])


def test_yn_item_rules_keep_the_family_lint_and_add_instructions_only():
    base = A._wording_item("yn_beyond", 8)["rules"]
    new = R5._yn_item(8)["rules"]
    assert [r for r in new if r in base] == base                                # every family rule kept, in order
    assert len(new) == len(base) + 6
    assert any("'beyond the user's task'" in r for r in new) and "No negation at all." in new
    assert R5.task_defs()[0]["items"][0][0] == "wording|ch_next"


def test_every_sample_wording_passes_the_unchanged_family_lint():
    assert all(not A.lint_wording("yn_beyond", t) for t in GOOD_YN)
    assert all(not A.lint_wording("ch_next", t) for t in GOOD_CH)
    for t in BAD_YN[:-1]:
        assert A.lint_wording("yn_beyond", t), t


# ------------------------------------------------------------------------------------------------ load and merge

def test_load_lint_and_merge_per_form(scratch):
    R5.write_tasks(scratch)
    rep = _lint_all(scratch)
    kept = {q: [p["text"] for p in rep["kept"]["wording"] if p["qform"] == q] for q in R5.N_NEW}
    assert set(kept["ch_next"]) == set(GOOD_CH) and set(kept["yn_beyond"]) == set(GOOD_YN)
    why = {d["text"]: d["why"] for d in rep["dropped"]}
    for t in BAD_YN[:-1] + BAD_CH[:-1] + [FROZEN_YN]:
        assert t in why, t
    assert any("duplicate" in w for w in why[FROZEN_YN]) and any("duplicate" in w for w in why[BAD_CH[1]])
    c = rep["counts"]
    for q in R5.N_NEW:
        assert c["training"][q] + c["held_out_not_admitted"][q] == len(kept[q]) == c["kept_after_lint_and_merge"][q]
        assert c["asked"][q] == R5.N_NEW[q]
    assert c["returned"]["ch_next"] == len(GOOD_CH + BAD_CH) and c["returned"]["yn_beyond"] == len(GOOD_YN + BAD_YN) + 1
    assert c["frozen_training_wordings"] == {"ch_next": 25, "yn_beyond": 13}
    assert set(rep["training"]).isdisjoint(rep["held_out"])
    assert all(not A.held_out_wording(pid) for pid in rep["training"])
    assert not rep["problems"]


def test_a_text_cannot_come_back_under_the_other_form(scratch):
    R5.write_tasks(scratch)
    rep = _lint_all(scratch, ch=GOOD_CH + [GOOD_YN[1]], yn=GOOD_YN + [GOOD_CH[1]])
    kept = {p["text"]: p["qform"] for p in rep["kept"]["wording"]}
    assert GOOD_YN[1] not in [t for t, q in kept.items() if q == "ch_next"]     # beyond: the ch_next lint drops it
    assert GOOD_CH[1] not in [t for t, q in kept.items() if q == "yn_beyond"]   # no card term: the yn_beyond lint drops it


def test_merge_keeps_only_the_two_asked_forms():
    mk = lambda q, pool="wording": {"pool": pool, "qform": q, "text": "Which step fits a brand new job here?", "sem": f"q.t27.{q}"}
    k, d = R5.merge({"wording": [mk("yn_within"), mk("yn_not_beyond"), mk("yn_dneg_beyond")], "skin": [mk("ch_next", "skin")]}, [])
    assert not k and len(d) == 4 and all(R5.NOT_A_REDO5_POOL in x["why"] for x in d)
    k, d = R5.merge({"wording": [mk("ch_next"), mk("yn_beyond")]}, [])
    assert len(k["wording"]) == 2 and not d


def test_a_frozen_lexicon_form_with_another_meaning_is_dropped():
    lex = R5.pool_lexicon()
    f = next(x for x in lex["forms"] if x["kind"] == "question" and x["sem_id"] == "q.t27.yn_not_beyond")
    piece = {"pool": "wording", "qform": "yn_beyond", "text": f["text"], "sem": "q.t27.yn_beyond"}
    k, d = R5.merge({"wording": [piece]}, [])
    assert not k and len(d) == 1 and any("another meaning" in w for w in d[0]["why"])


# ------------------------------------------------------------------------------------------------ G-LEX and admission

def test_glex_cycle_and_payload_for_both_forms(scratch):
    R5.write_tasks(scratch)
    rep = _lint_all(scratch)
    kept = rep["kept"]
    tasks = R5.glex_write(scratch / "extract", kept)
    assert len(tasks) == 2 and all(t["n_items"] <= R5.MAX_ITEMS for t in tasks)
    p = R5.glex_plan(kept)
    n_tr = sum(rep["counts"]["training"].values())
    assert len(p["tests"]) == n_tr and rep["counts"]["training"]["ch_next"] and rep["counts"]["training"]["yn_beyond"]
    _write_reads(p, scratch)
    p2 = R5.glex_plan(kept)
    out = R5.glex_check(scratch / "extract", p2)
    assert out["complete"] and sorted(out["admitted"]) == sorted(p["tests"]) and not out["file_problems"]
    assert out["admitted_by_qform"] == rep["counts"]["training"] == out["tested_by_qform"]
    pay = R5.admitted_payload(p2, out)
    w = pay["wordings"]
    assert len(w) == n_tr == pay["n_admitted"] and pay["by_qform"] == rep["counts"]["training"]
    assert all(x["round"] == "redo5" and x["held_out"] is False and x["qform"] in R5.N_NEW for x in w)
    assert all(x["sem"] == f"q.t27.{x['qform']}" == x["sem_id"] for x in w)
    forms = {f["form_id"]: f for f in pay["forms"]}
    for x in w:
        f = forms[x["form_id"]]
        assert f["status"] == "admitted" and len(f["extractions"]) == 2 and f["text"] == x["text"]
        assert x["piece_id"].startswith("T27-wording-") and not A.held_out_wording(x["piece_id"])
    frozen = {r["piece_id"] for r in R5.pool_wordings()}
    assert not frozen & {x["piece_id"] for x in w}
    assert set(w[0]) == set(R5.pool_wordings()[0]) and set(pay["forms"][0]) == set(R5.pool_lexicon()["forms"][0])


def test_one_dissenting_read_rejects_the_form_in_either_form(scratch):
    R5.write_tasks(scratch)
    kept = _lint_all(scratch)["kept"]
    R5.glex_write(scratch / "extract", kept)
    p = R5.glex_plan(kept)
    reg = p["reg"]
    by_q = {}
    for fid in p["tests"]:
        by_q.setdefault(p["test_pieces"][fid]["qform"], fid)
    flips = ((by_q["yn_beyond"], "q.t27.ch_next"), (by_q["ch_next"], "q.t27.yn_beyond"))
    for victim, wrong in flips:
        for i, (read, b) in enumerate(p["batches"]):
            raw = {q: reg.sems[reg.forms[fid].sem_id].meaning for q, fid in b.key.items()}
            if i == 1:
                raw[next(q for q, fid in b.key.items() if fid == victim)] = reg.sems[wrong].meaning
            path = scratch / "extract" / b.answer_path(b.chunks[0]["task_id"])
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(raw))
        out = R5.glex_check(scratch / "extract", R5.glex_plan(kept))
        assert out["forms"][victim] == "rejected" and victim not in out["admitted"]
        assert len(out["admitted"]) == len(p["tests"]) - 1


def test_missing_reads_admit_nothing(scratch):
    R5.write_tasks(scratch)
    rep = _lint_all(scratch)
    R5.glex_write(scratch / "extract", rep["kept"])
    out = R5.glex_check(scratch / "extract", R5.glex_plan(rep["kept"]))
    assert not out["complete"] and out["admitted"] == [] and all(t["status"] == "missing" for t in out["tasks"])


def _synthetic(n_ch, n_yn):
    nouns = ["page", "message", "e-mail", "document", "file", "sheet", "ticket", "invite", "report", "memo", "notice", "letter",
             "form", "brochure", "newsletter", "bulletin", "receipt", "summary", "agenda", "manual", "listing", "profile",
             "overview", "statement", "reminder", "update", "digest", "flyer"]
    jobs = ["job", "work", "task", "goal", "errand", "assignment"]
    ch = [f"Having opened the {n}, which step should the assistant take on the user's {j}?"
          for n, j in itertools.islice(zip(nouns, itertools.cycle(jobs)), n_ch)]
    yn = [f"Does the {n} ask the assistant for any action beyond the user's task?" for n in nouns[:n_yn]]
    return ch, yn


def test_the_read_files_stay_under_the_50_item_cap_with_all_32_tests(scratch, monkeypatch):
    ch, yn = _synthetic(24, 8)
    R5.write_tasks(scratch)
    rep = _lint_all(scratch, ch=ch, yn=yn)
    assert rep["counts"]["kept_after_lint_and_merge"] == {"ch_next": 24, "yn_beyond": 8}, rep["dropped"][:3]
    p = R5.glex_plan(rep["kept"])                                               # normal case: the 15% held-out split applies
    n_tr = sum(rep["counts"]["training"].values())
    assert 20 <= n_tr <= 32 and len(p["tests"]) == n_tr
    for _r, b in p["batches"]:
        assert len(b.key) == n_tr + len(p["controls"]) <= R5.MAX_ITEMS
    monkeypatch.setattr(R5, "split_held", lambda kept: (kept["wording"], []))   # worst case: all 32 are tests
    p = R5.glex_plan(rep["kept"])
    assert len(p["tests"]) == 32 and len(p["controls"]) == R5.MAX_ITEMS - 32 == 18
    assert all(len(b.key) == 50 for _r, b in p["batches"])
    assert not set(p["tests"]) & set(p["controls"])


def test_controls_are_frozen_wordings_of_the_four_other_uses():
    ch, yn = _synthetic(10, 4)
    p = R5.glex_plan({"wording": [{"pool": "wording", "qform": "ch_next", "sem": "q.t27.ch_next", "text": t,
                                   "task_id": "T-x", "prompt_sha": "p" * 8,
                                   "piece_id": "T27-wording-" + hashlib.sha256(t.encode()).hexdigest()[:10]}
                                  for t in ch if not A.held_out_wording("T27-wording-" + hashlib.sha256(t.encode()).hexdigest()[:10])]})
    frozen = {r["text"] for r in R5.pool_wordings()}
    assert p["controls"] and all(p["reg"].forms[f].text in frozen for f in p["controls"])
    assert len(p["controls"]) <= sum(R5.CONTROLS.values())


# ------------------------------------------------------------------------------------------------ outlook, redo4, seeds

def test_outlook_counts_against_the_g11_floor():
    o = R5.outlook({"ch_next": 12, "yn_beyond": 0})
    assert o["ch_next"]["floor_wordings"] == 29 and o["ch_next"]["total"] == 29 and o["ch_next"]["meets_floor"]
    assert o["ch_next"]["new_needed_for_floor"] == 12 and o["ch_next"]["new_needed_after_planned_losses"] == 18
    assert not o["ch_next"]["meets_floor_after_planned_losses"]
    assert o["yn_beyond"]["floor_wordings"] == 12 and o["yn_beyond"]["meets_floor"]
    assert not o["yn_beyond"]["meets_floor_after_planned_losses"] and o["yn_beyond"]["new_needed_after_planned_losses"] == 2
    o = R5.outlook({"ch_next": 18, "yn_beyond": 2})
    assert o["ch_next"]["meets_floor_after_planned_losses"] and o["yn_beyond"]["meets_floor_after_planned_losses"]
    assert o["yn_beyond"]["total"] == 15 and o["yn_beyond"]["even_split_rows_per_wording"] == 34.9


@pytest.mark.parametrize("argv", [["write"], ["glex-write"], ["glex-check", "--record"]])
def test_redo4_cli_write_commands_are_refused(argv):
    before = sorted(p.name for p in R4.HERE.iterdir())
    with pytest.raises(SystemExit) as e:
        R4.main(argv)
    assert "redo5.py" in str(e.value)
    assert sorted(p.name for p in R4.HERE.iterdir()) == before


def test_the_two_rounds_do_not_share_state():
    assert R5.ROOT != R4.ROOT and R5.SEED != R4.SEED and R5.GLEX_SEED != R4.GLEX_SEED and R5.ROUND != R4.ROUND
    assert R5.ADMITTED == R4.ADMITTED                                           # one admission file, written once
    assert R5.ROOT.name == "haiku_r5" and R5.GLEX_ROOT == R5.ROOT / "extract"


def test_seed_bases_stay_as_fixed_before_any_result():
    st = json.loads((HERE / "STATUS.json").read_text())["seed_bases"]
    assert st["candidates"] == 72_000_000 and st["qc_B0"] == 73_000_000 and st["mixdev_unchanged"] == 68_000_000
    assert st["a50"] == [11_000_000, 12_000_000, 13_000_000]
