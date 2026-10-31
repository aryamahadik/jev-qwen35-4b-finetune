"""Fix iteration 2 double-negation round: write_author, stage 2 and stage 3 on fabricated answers in a temp dir."""
import json
import shutil
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from families.T29 import authoring as A  # noqa: E402
from families.T29 import dneg_i2 as D  # noqa: E402
from families.T29 import dneg_stage2 as S2  # noqa: E402
from families.T29 import dneg_stage3 as S3  # noqa: E402

import pytest  # noqa: E402


@pytest.fixture
def tmp_path():
    """A scratch folder under lean/ (the kit writers refuse any other place), removed afterwards."""
    p = D.HERE / "_tmp_dneg_i2_test"
    shutil.rmtree(p, ignore_errors=True)
    p.mkdir()
    yield p
    shutil.rmtree(p, ignore_errors=True)


FRAMES = ("Is it not the case that", "Is it not true that", "Is it not so that")
CLAUSES = ("the agent may not run {ACTION} on {TARGET} straight away", "the agent is not cleared to run {ACTION} on {TARGET} right away",
           "the agent is not free to run {ACTION} on {TARGET} at this point", "the agent is not able to run {ACTION} on {TARGET} straight away")
LEADS = ("", "Under this policy, ", "According to the policy, ", "Reading the policy closely, ", "Given the policy above, ",
         "Taking the policy as written, ", "Under the rules shown, ", "With the policy in view, ")


def fabricated_wordings(n, offset=0):
    out = []
    for i in range(offset, offset + n):
        frame = FRAMES[i % 3]
        lead = LEADS[(i // 12) % len(LEADS)]
        txt = f"{frame} {CLAUSES[i % 4]}?" if not lead else f"{lead}{frame[0].lower()}{frame[1:]} {CLAUSES[i % 4]}?"
        out.append(txt[0].upper() + txt[1:])
    return out


def write_authoring_answers(root: Path, bad: bool = True):
    k = 0
    for t in D.author_tasks():
        ans = []
        for it in t.chunk["items"]:
            n = 8 if not t.held_out else 6
            ws = fabricated_wordings(n, offset=k)
            k += n
            if bad and not ans:       # a wording with one negation, one with a blocking word: both must be dropped
                ws[0] = "Is the agent allowed to run {ACTION} on {TARGET} straight away at this point?"
                ws[1] = "Is it not the case that the agent does not bar {ACTION} on {TARGET} straight away?"
            ans.append({"qid": it["qid"], "wordings": ws})
        p = t.answer_file(root)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(ans))


def write_glex_answers(root: Path, wrong_once: bool = True):
    state = json.loads((root / "stage2_state.json").read_text())
    reg = D.restore_registry(state)
    batches = D.glex_batches(reg, sorted(f["form_id"] for f in state["forms"]))
    first_wrong = wrong_once
    for read, _k, b in batches:
        for c in b.chunks:
            ans = []
            for it in c["items"]:
                good = A.DNEG_SEM_MEANING
                choice = good if good in it["choices"] else it["choices"][0]
                if read == "glex-r2" and first_wrong:
                    choice = next(x for x in it["choices"] if x != good)
                    first_wrong = False
                ans.append({"qid": it["qid"], "meaning": choice})
            p = root / D.GLEX_SUB / b.answer_path(c["task_id"])
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(ans))


def test_authoring_task_files(tmp_path):
    m = D.write_author(tmp_path)
    assert m["n_tasks"] == 2 and m["outputs_expected"] == 54
    files = sorted((tmp_path / "tasks").glob("*.md"))
    assert len(files) == 2
    text = files[0].read_text()
    assert str(tmp_path / "answers") in text and "ANSWER FILE" in text
    assert "Is it not the case that" in text and "blocking" in text      # the polarity-aware brief


def test_stage2_then_stage3(tmp_path):
    root, pool, out = tmp_path / "dneg_i2", tmp_path / "pool", tmp_path / "pilot_i2"
    D.write_author(root)
    write_authoring_answers(root)
    rep = S2.stage2(root)
    assert rep["authored"] == 54 and rep["survivors"] < 54
    reasons = " ".join(r for d in rep["drops"] for r in d["reasons"])
    assert "negation k_syn/k_all" in reasons or "polarity" in reasons
    assert rep["new_forms"] >= 20 and rep["new_forms_held_out"] >= 1
    assert rep["glex_tasks"] >= 2
    for p in rep["glex_task_files"]:
        assert Path(p).is_file() and str(root / D.GLEX_SUB / "answers") in Path(p).read_text()
    # stage 3 stops while a read is missing
    try:
        S3.admit(root, pool)
        raise AssertionError("expected STOP")
    except SystemExit as e:
        assert "STOP" in str(e)
    write_glex_answers(root)
    adm = S3.admit(root, pool)
    s = adm["summary"]
    assert s["new_forms"] == rep["new_forms"] and s["admitted"] == s["new_forms"] - 1 and s["quarantined"] == 1
    assert s["status"].get("admitted") == s["admitted"]
    man = json.loads((pool / "MANIFEST.json").read_text())
    assert set(man["pool_files"]) == {"wordings.jsonl", "lexicon_merged.json", "quarantine.jsonl"}
    rows = [json.loads(x) for x in (pool / "wordings.jsonl").read_text().splitlines()]
    assert len(rows) == s["admitted"] and all(r["qform"] == A.DNEG and r["status"] == "admitted" for r in rows)
    assert all(not A.wording_problems(A.DNEG, r["text"]) for r in rows)
    # the supplement registry has them admitted
    from c2_kit import lexicon as LX
    reg = LX.LexiconRegistry.from_json(json.loads((pool / "lexicon_merged.json").read_text()))
    assert all(reg.status(r["form_id"]) == "admitted" for r in rows)
    # CLI path with --no-pilot writes the G13 list
    assert S3.main(["--root", str(root), "--pool", str(pool), "--out", str(out), "--no-pilot"]) == 0
    pend = (out / "G13_PENDING.txt").read_text().splitlines()
    assert len(pend) == 1 + s["admitted"]
