"""F8 stage scripts (dneg_stage2 / dneg_stage3) on FABRICATED answers in a temp dir: no Haiku, nothing written to haiku/."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parents[1]), str(HERE)]
import dneg_stage2 as S2  # noqa: E402
import dneg_stage3 as S3  # noqa: E402

GOOD = ["Is the following statement true: it is not the case that {WHO} has not broken the promise to {QTASK} at the end of {ASOF}?",
        "Is this claim accurate: it is not the case that {WHO} has not broken the promise to {QTASK} by the end of {ASOF}?"]
BAD_FRAME = "Is it not the case that {WHO} has not broken the promise to {QTASK} at the end of {ASOF}?"
BAD_CONTRACTED = "Isn't it so that {WHO} hasn't broken the promise to {QTASK} at the end of {ASOF}?"


def _fab_author(root: Path):
    for c in S2._A().reauthor_dneg_batch(root).chunks:
        ans = []
        for k, it in enumerate(c["items"]):
            ws = [GOOD[k % 2] + (" " * 0), BAD_FRAME, BAD_CONTRACTED, GOOD[0], GOOD[1]] if k == 0 else [
                GOOD[0].replace("the following statement", f"the following statement #{k}").replace("#", "") for _ in range(1)] * 0
            if k:
                ws = [f"Is the following statement true: it is not the case that {{WHO}} has not broken the promise to {{QTASK}} "
                      f"at the end of {{ASOF}} ({w})?" for w in ("a", "b", "c", "d", "e")]
            ans.append({"qid": it["qid"], "wordings": ws})
        p = Path(c["answer_file"])
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(ans))


def test_tasks_files_are_self_contained(tmp_path):
    out = S2.tasks(tmp_path)
    md = Path(out[0]).read_text()
    assert "ANSWER FILE" in md and "answers/" in md and "Answer contract" in md and "it is not the case that" in md
    assert (tmp_path / "tasks").is_dir()


def test_admit_then_glex_then_supplement(tmp_path):
    S2.tasks(tmp_path)
    _fab_author(tmp_path)
    r = S2.admit(tmp_path)
    cj = json.loads((tmp_path / "candidates.json").read_text())
    reasons = " ".join(" ".join(x["problems"]) for x in cj["rejected"])
    assert BAD_FRAME in [x["text"] for x in cj["rejected"]] and BAD_CONTRACTED in [x["text"] for x in cj["rejected"]], reasons
    assert r["candidates"] >= 5 and len(r["glex_tasks"]) == 2
    # fabricated G-LEX answers: read 1 picks the right meaning on every item, read 2 says "none of these" on the first
    reg = S2._registry()
    fids = S2._add_candidates(reg, [{**c, "slots": dict(c["slots"])} for c in cj["candidates"]])
    first = None
    for read, gb in S2.glex_batches(reg, fids, tmp_path):
        right = reg.sems[next(iter(s for s in reg.sems if s.endswith(S2.QFORM)))].meaning
        for c in gb.chunks:
            ans = []
            for it in c["items"]:
                pick = right if right in it["choices"] else it["choices"][-1]
                if read == "glex-r2" and first is None:
                    first, pick = it["qid"], it["choices"][-1]
                ans.append({"qid": it["qid"], "meaning": pick})
            p = Path(c["answer_file"])
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(ans))
    s = S3.admit_glex(tmp_path)
    assert s["admitted"] == len(fids) - 1 and s["dropped"] == 1, s
    supp = json.loads((tmp_path / "pool_supplement.json").read_text())
    assert len(supp["forms"]) == s["admitted"] and (tmp_path / "G13_PENDING.txt").exists()
    import pilot_loaders as PL
    with PL.open_family("T32") as kit:
        assert kit.plugin.dneg_ok is False
        assert S2.apply_supplement(kit, tmp_path / "pool_supplement.json") == s["admitted"]
        assert kit.plugin.dneg_ok is True
        assert any(sk.qform == S2.QFORM and sk.text in {f["text"] for f in supp["forms"]} for sk in kit.ctx.skins.values())
