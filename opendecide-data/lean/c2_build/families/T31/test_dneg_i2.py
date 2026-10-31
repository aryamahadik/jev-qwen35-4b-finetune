"""families/T31/test_dneg_i2.py: the double-negation round (dneg_i2.py, dneg_stage2.py, dneg_stage3.py) on FABRICATED Haiku
answers in a temp dir. No model is run; nothing under families/T31/haiku or pools_v2_dneg is written."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from c2_kit.lexicon import question_sem  # noqa: E402
from families.T31 import dneg_i2 as D  # noqa: E402
from families.T31 import dneg_stage2 as S2  # noqa: E402
from families.T31 import dneg_stage3 as S3  # noqa: E402
from families.T31 import freeze_v2 as FV  # noqa: E402
from families.T31 import plugin as P  # noqa: E402

@pytest.fixture
def tmp_path():
    """A temp dir INSIDE lean/ (the kit's guarded writers only write under lean/); removed afterwards."""
    import shutil
    import uuid
    p = D.C2_BUILD / "_tmp_test_dneg_i2" / uuid.uuid4().hex[:8]
    p.mkdir(parents=True)
    try:
        yield p
    finally:
        shutil.rmtree(p.parent, ignore_errors=True)


TAILS = ("at the time of the request", "when the request was made", "per the records", "according to the records",
         "for this request", "going by the records above")
PIECE = {"holder": {"was": "was not the accountable approver", "holding": "did not hold the accountable role",
                    "is": "is not the accountable approver"},
         "agent": {"permitted": "is not permitted to use", "allowed": "is not allowed to use",
                   "entitled": "is not entitled to use", "authorised": "is not authorised to use"}}


def _wording(item: dict, q: str, n: int) -> str:
    rules = " | ".join(item["rules"])
    outer = next(o for o in D.OUTER if f"open with exactly '{o}'" in rules)
    tail = TAILS[(n // 3) % len(TAILS)]
    if q == "yn_holder_dneg":
        key = next(k for k in PIECE["holder"] if f"on the verb '{k}'" in rules or (k == "holding" and "holding verb" in rules))
        return f"{outer} {{CANDIDATE}} {PIECE['holder'][key]} {tail}?"
    key = next(k for k in PIECE["agent"] if f"on '{k}'" in rules)
    return f"{outer} {{REQ_AGENT}} {PIECE['agent'][key]} {{REQ_SCOPE}} {tail}?"


def fabricate_authoring(root: Path) -> dict:
    """Write an answer file per authoring task: mostly good wordings, a few the checks must reject."""
    man = json.loads((root / "TASKS.json").read_text(encoding="utf-8"))
    bad_seen = {}
    n = 0
    for t in man["tasks"]:
        chunk = json.loads((root / "chunks" / f"{t['task_id']}.json").read_text(encoding="utf-8"))
        out = []
        for k, it in enumerate(chunk["items"]):
            n += 1
            text = _wording(it, t["qform"], n)
            if t["task_id"].endswith("000") and t["qform"] == "yn_holder_dneg":
                if k == 0:
                    text = "Isn't it the case that {CANDIDATE} was not the accountable approver?"          # contracted
                    bad_seen["contracted"] = it["qid"]
                elif k == 1:
                    text = "Is it not the case that {CANDIDATE} was the accountable approver?"             # one negation
                    bad_seen["one_not"] = it["qid"]
                elif k == 2:
                    text = "Is it not the case that {CANDIDATE} did not block the accountable approver role?"   # P1
                    bad_seen["polarity"] = it["qid"]
                elif k == 3:
                    out.append({"qid": it["qid"], "text": out[0]["text"]})                                   # duplicate
                    bad_seen["dup"] = it["qid"]
                    continue
                elif k >= 4 and "req_id" not in bad_seen and it["slots"]["REQ_ID"] == "leave it out":
                    text = "Is it not the case that {CANDIDATE} was not the accountable approver for {REQ_ID}?"
                    bad_seen["req_id"] = it["qid"]
            out.append({"qid": it["qid"], "text": text})
        (root / "answers").mkdir(exist_ok=True)
        Path(t["answer_file"]).write_text(json.dumps(out), encoding="utf-8")
    return bad_seen


def fabricate_glex(root: Path, cands: list, *, disagree: tuple = ()) -> None:
    """Answer both reads with the declared meaning; read d2read1 answers null / another meaning for `disagree` form ids."""
    reg = D.restore_registry(cands)
    gd = root / D.GLEX_SUB
    man = json.loads((gd / "TASKS.json").read_text(encoding="utf-8"))
    other = reg.sems[question_sem(D.F, "yn_holder_not")].meaning
    for t in man["tasks"]:
        key = json.loads((gd / "key" / f"{t['batch_id']}.json").read_text(encoding="utf-8"))["key"]
        chunk = json.loads((gd / "chunks" / f"{t['task_id']}.json").read_text(encoding="utf-8"))
        out = []
        for it in chunk["items"]:
            fid = key[it["qid"]]
            choice = reg.sems[reg.forms[fid].sem_id].meaning
            if t["read"] == "d2read1" and fid in disagree:
                choice = None if fid == disagree[0] else other
            out.append({"qid": it["qid"], "choice": choice})
        (gd / "answers").mkdir(exist_ok=True)
        Path(t["answer_file"]).write_text(json.dumps(out), encoding="utf-8")


def test_authoring_task_files_are_self_contained(tmp_path):
    root = tmp_path / "dneg_i2"
    man = D.write_author(root)
    assert man["n_tasks"] == 4 and man["items_expected"] == 2 * D.PER_FORM == 64 and D.PER_FORM == 4 * D.NEEDED
    forms = {}
    for t in man["tasks"]:
        text = Path(t["task_file"]).read_text(encoding="utf-8")
        assert Path(t["task_file"]).parent == root / "tasks" and t["answer_file"] == str(root / "answers" / f"{t['task_id']}.json")
        assert "ANSWER FILE" in text and t["answer_file"] in text and "EXACT ANSWER CONTRACT" in text
        assert '"qid"' in text and "Exactly two 'not'" in text
        assert t["n_items"] <= D.AUTHOR_CHUNK and t["allowed_write"] == [t["answer_file"]]
        assert "wording|" not in text                                          # no internal id in the task file
        forms[t["qform"]] = forms.get(t["qform"], 0) + t["n_items"]
    assert forms == {"yn_holder_dneg": D.PER_FORM, "yn_agent_dneg": D.PER_FORM}
    with pytest.raises(SystemExit):
        D.write_author(root)                                                   # never rewrites (keys would drift)
    again, _ = D.author_files(root)
    assert all((root / rel).read_text(encoding="utf-8") == text for rel, text in again.items())    # deterministic


def test_stage2_stage3_on_fabricated_answers(tmp_path):
    root, supp, out = tmp_path / "dneg_i2", tmp_path / "pools_v2_dneg", tmp_path / "pilot_i2"
    D.write_author(root)
    bad = fabricate_authoring(root)
    st = D.run_stage2(root, write=False)
    assert not st["written"] and st["status"] == "OK", st
    rep = D.run_stage2(root)
    assert rep["written"] and all(rep["to_glex_per_form"][q] >= 12 for q in D.FORMS), rep
    quar = json.loads((root / "QUARANTINE_AUTHORING.json").read_text(encoding="utf-8"))["rows"]
    reasons = {r["piece"]: r["reason"] for r in quar}
    assert len(quar) >= 5 and any("polarity" in r or "P1" in r for r in reasons.values())
    assert any("duplicate" in r for r in reasons.values()) and any("REQ_ID" in r for r in reasons.values())
    assert any("outer frame" in r or "k_syn" in r for r in reasons.values())
    gtasks = json.loads((root / D.GLEX_SUB / "TASKS.json").read_text(encoding="utf-8"))
    assert gtasks["reads"] == ["d2read0", "d2read1"] and {t["read"] for t in gtasks["tasks"]} == set(D.READS)
    assert all(Path(t["task_file"]).is_file() and Path(t["answer_file"]).parent == root / D.GLEX_SUB / "answers"
               for t in gtasks["tasks"])
    with pytest.raises(SystemExit):
        D.run_stage2(root)                                                     # glex_tasks exist: no rewrite
    with pytest.raises(SystemExit):
        S3.admit(root, supp)                                                   # reads not answered yet: stop

    cands = json.loads((root / "admitted_candidates.json").read_text(encoding="utf-8"))["candidates"]
    holder = sorted(c["form_id"] for c in cands if c["qform"] == "yn_holder_dneg")
    fabricate_glex(root, cands, disagree=(holder[0], holder[1]))
    rc = S3.main(["--root", str(root), "--supp", str(supp), "--out", str(out), "--no-pilot"])
    assert rc == 0
    man = json.loads((supp / "MANIFEST.json").read_text(encoding="utf-8"))
    n_h = len(holder) - 2
    assert man["counts"]["admitted_per_form"]["yn_holder_dneg"] == n_h and man["short"] == []
    assert man["counts"]["admitted_per_form"]["yn_agent_dneg"] == len([c for c in cands if c["qform"] == "yn_agent_dneg"])
    rej = json.loads((supp / "QUARANTINE.json").read_text(encoding="utf-8"))["rows"]
    assert {r["stage"] for r in rej} == {"G-LEX"} and len(rej) == 2
    pend = (out / "G13_PENDING.txt").read_text(encoding="utf-8").splitlines()
    assert len([ln for ln in pend if not ln.startswith("#")]) == man["counts"]["admitted"]
    with pytest.raises(SystemExit):
        S3.admit(root, supp)                                                   # supplement exists: no overwrite

    pools = FV.load_pools()
    before = len(pools["wordings"])
    notes = D.apply_supplement(pools, supp)
    assert len(pools["wordings"]) == before + man["counts"]["admitted"] and "wordings" in notes[0]
    plugin = P.T31(lexicon=pools["lexicon"])
    assert plugin.dneg_ok == {"yn_holder_dneg": True, "yn_agent_dneg": True}
    assert P.T31(lexicon=FV.load_pools()["lexicon"]).dneg_ok == {"yn_holder_dneg": False, "yn_agent_dneg": False}
    assert D.apply_supplement(FV.load_pools(), tmp_path / "none")[0].startswith("no double-negation supplement")
    (supp / "wordings_dneg.json").write_text("{}", encoding="utf-8")
    with pytest.raises(D.SupplementError):
        D.apply_supplement(FV.load_pools(), supp)                              # a changed supplement file is refused


def test_loader_draws_double_negation_rows(tmp_path):
    """The runner's loader (no edit of pilot_loaders.py) with a supplement of fabricated, G-LEX-admitted wordings."""
    root, supp, out = tmp_path / "dneg_i2", tmp_path / "pools_v2_dneg", tmp_path / "pilot_i2"
    D.write_author(root)
    fabricate_authoring(root)
    D.run_stage2(root)
    cands = json.loads((root / "admitted_candidates.json").read_text(encoding="utf-8"))["candidates"]
    fabricate_glex(root, cands)
    assert S3.main(["--root", str(root), "--supp", str(supp), "--out", str(out), "--no-pilot"]) == 0
    import pilot as PI
    import pilot_loaders as PL
    from families.T31 import run_pilot_i2 as RP
    orig = PL.LOADERS["T31"]
    try:
        RP.install_loader(supp)
        with PL.open_family("T31") as kit:
            assert kit.plugin.dneg_ok == {"yn_holder_dneg": True, "yn_agent_dneg": True} and kit.notes
            b = PI.build_pilot(kit, 160, run_g15=False)
        forms = [r.row["meta"]["qform"] for r in b.infos]
        assert b.stats["rows_written"] >= 160
        assert sum(q in RP.DNEG_FORMS for q in forms) >= 1
        assert b.stats["units_attempted"] - b.stats["units_written"] <= 0.2 * b.stats["units_attempted"]
    finally:
        PL.LOADERS["T31"] = orig


def test_stage_scripts_expose_their_cli():
    assert S2.D is D and callable(S2.main) and callable(S3.main)
