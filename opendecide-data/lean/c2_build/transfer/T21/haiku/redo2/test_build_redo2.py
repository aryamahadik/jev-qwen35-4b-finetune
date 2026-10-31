"""transfer/T21/haiku/redo2/test_build_redo2.py: in-memory tests of build_redo2.py (nothing is written).

  need        the plan equals the frozen pools/manifest.json shortfalls (B1: 20 pieces); pools/ is unchanged
  candidates  3 per missing piece, 4 per missing wording; ranks 0..k-1 per cell; ids never collide with v1 ids
  task files  self-contained: answer path inline under haiku/redo2/answers/, no internal id, new qids, prompt = the v1
              prompt + an addendum whose words the gates already refuse
  facts       the 15 Mode F name pairs are valid, new and lint clean
  plumbing    stage B / C on SYNTHETIC in-memory answers (monkeypatched loader; a code test, never data, never
              written): the selection fills exactly the need with the lowest-ranked passing candidates; a lint hit,
              a G-LEX disagreement and a G3-H mismatch each drop a candidate; the tally after the top-up is full
Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/transfer/T21/haiku/redo2
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import build_redo2 as B  # noqa: E402
from transfer.T21 import fixtures as FX  # noqa: E402  (on sys.path through build_redo2)
from transfer.T21 import haiku_author as HA  # noqa: E402


@pytest.fixture(scope="module")
def built():
    return B.stage_a()


def test_need_is_the_frozen_shortfall():
    need = B.need_from_manifest()
    assert need == B.EXPECTED_NEED and sum(need.values()) == 20
    assert not B.v1_pool_problems()
    q = json.loads((B.POOLS / "quarantine.json").read_text(encoding="utf-8"))
    per = {}
    for d in q:
        per[d["pool"]] = per.get(d["pool"], 0) + 1
    assert per == {"packs": 2, "skins": 8, "freeform": 5, "wordings": 5}


def test_candidates_ranks_and_ids(built):
    batches = B.build_batches()
    need = B.need_from_manifest()
    v1_ids = set()
    for name, (b, _plan) in HA.build_batches().items():
        v1_ids |= set(b.key.values())
    v1_qids = {q for b, _p in HA.build_batches().values() for q in b.key}
    for name, (b, plan) in batches.items():
        assert not set(plan) & v1_ids and not set(b.key) & v1_qids
        assert all(i.startswith(B.PREFIX) for i in plan)
        for (pool, lab), n in need.items():
            if pool != name:
                continue
            ranks = sorted(p["rank"] for p in plan.values() if p["cell"] == f"{pool}|{lab}")
            assert ranks == list(range(n * B.FACTOR[pool]))
    assert sum(len(p) for _b, p in batches.values()) == 65
    pk = batches["packs"][1]
    assert all(not p["held_out"] for p in pk.values())
    assert not {p["pack_id"] for p in pk.values()} & {p["pack_id"] for p in json.loads(
        (B.POOLS / "packs.json").read_text(encoding="utf-8"))}


def test_task_files_are_self_contained(built):
    files, rows = built
    assert len(rows) == 6 and sum(r["n_items"] for r in rows) == 65
    v1_prompts = {"author_pack": HA.PACK_PROMPT, "author_skin": HA.SKIN_PROMPT, "author_freeform": HA.FREEFORM_PROMPT,
                  "author_wording": HA.WORDING_PROMPT}
    batches = B.build_batches()
    internal = {i for b, _p in batches.values() for i in b.key.values()}
    for r in rows:
        text = files[f"tasks/{r['task_id']}.md"]
        assert r["answer_file"] in text and r["answer_file"].startswith(str(B.HERE / "answers") + "/")
        assert r["allowed_read"] == [r["task_file"]] and r["allowed_write"] == [r["answer_file"]]
        assert not any(i in text for i in internal)
        assert v1_prompts[r["kind"]] in text
        assert "pools/" not in text and "ohs" not in text.lower()
    tj = json.loads(files["TASKS.json"])
    assert tj["g0_sha256"] == B.PL.G0_SHA256 and tj["n_tasks"] == 6


def test_addenda_and_facts():
    assert B.addendum_problems() == []
    assert B.fact_problems() == []
    assert len(B.F_FACTS_R2) == 15 and len(B.SETTINGS_R2) >= 12 and len(B.PACK_THEMES_R2) == 6


# ------------------------------------------------------------------------------------------------ plumbing
_PRE = ("Bral", "Cosk", "Dremm", "Fask", "Grold", "Halm", "Kesp", "Lurn", "Marv", "Nolt", "Prask", "Quorl", "Rusk",
        "Sarn", "Tolv", "Varn", "Wesk", "Yarl", "Zorn")
_SUF = ("ock", "eth", "ira", "uno", "aby")


def _word(i: int) -> str:
    return _PRE[i % len(_PRE)] + _SUF[(i // len(_PRE)) % len(_SUF)]


def _synthetic(b, plan_all: dict) -> dict:
    """SYNTHETIC answers for the plumbing test only (never written): one per item, shaped like a valid answer, with
    one planted failure per stage (rank 0 of the first cell of each gate)."""
    raw = {}
    for c in b.chunks:
        out = []
        for it in c["items"]:
            iid = b.key[it["qid"]]
            if b.kind == "author_pack":
                r = plan_all[iid]["rank"]
                base = 10 * (r + 1)
                ag = [f"{_word(base + k)} {d} agreement" for k, d in enumerate(("hosting", "catering", "printing",
                                                                                   "glazing"))]
                if r == 0:
                    ag[0] = f"{_word(base)} bulk agreement"                  # planted lint failure
                pa = [f"{_word(base + 4 + k)} {_word(base + 40 + k)}" for k in range(6)]
                out.append({"qid": it["qid"], "pack": {"agreements": ag, "parties": pa}})
            elif b.kind == "author_skin":
                p = plan_all[iid]
                w = _word(200 + 10 * B.TRAIN_REG.index(p["register"]) + p["rank"]).lower()
                extra = " Everyone has the file." if (p["register"] == "dispute_email" and p["rank"] == 0) else ""
                out.append({"qid": it["qid"], "text": f"Note: {{CLAIMANT}} has raised a claim under the {{AGREEMENT}}. "
                                                      f"The {w} desk holds the file, and the clauses follow.{extra}"})
            elif b.kind == "author_freeform":
                f = it["facts"]
                w = _word(300 + len(out) + 20 * b.chunks.index(c)).lower()
                out.append({"qid": it["qid"], "text": f"{f['CLAIMANT']} has raised a claim under the "
                                                      f"{f['AGREEMENT']}. The {w} desk holds the file."})
            elif b.kind == "author_wording":
                p = plan_all[iid]
                opener = re.search(r"'([^']+)'", B.STYLES_R2[p["rank"] % len(B.STYLES_R2)]).group(1)
                body = {"yn_capped": "does the cap of clause {CAP_ID} hold the liability for this claim to the cap?",
                        "ch_clause": "which clause is the deciding clause on the cap for this claim?",
                        "yn_free_of": "does this claim sit free of the cap of clause {CAP_ID}?"}[p["qform"]]
                out.append({"qid": it["qid"], "text": f"{opener} {body}"})
            elif b.kind == "extract_lex":
                q = iid.split("#")[0].rsplit(".", 1)[1]
                meaning = FX.QUESTION_MEANINGS[q]
                if b.seed.endswith("r2") and q == "yn_capped" and it["text"].startswith("According to"):
                    meaning = FX.QUESTION_MEANINGS["yn_uncapped"]              # planted G-LEX disagreement
                assert meaning in it["choices"]
                out.append({"qid": it["qid"], "meaning": meaning})
            elif b.kind == "extract_g3h":
                claimant, agreement = next((cl, ag) for cl, ag in B.F_FACTS_R2 if cl in it["text"])
                if claimant == B.F_FACTS_R2[0][0]:
                    claimant = "Ashwell Rope"                                  # planted G3-H mismatch
                out.append({"qid": it["qid"], "claimant": claimant, "agreement": agreement})
        raw[c["task_id"]] = out
    return raw, []


def test_plumbing_on_synthetic_answers(monkeypatch):
    plan_all = {}
    for _b, plan in B.build_batches().values():
        plan_all.update(plan)
    monkeypatch.setattr(B, "_load_raw", lambda b: _synthetic(b, plan_all))
    res = B.stage_b()
    drops = res["lint"]["drops"]
    assert list(drops["packs"]) == ["t21r2.pack.100"]
    assert list(drops["skins"]) == ["t21r2.skin.dispute_email.100"]
    assert not drops["freeform"] and not drops["wordings"], (drops, res["admit_drops"])
    assert len(res["fid_of"]) + len(res["admit_drops"]) == 20
    assert len(res["g3_expected"]) == 15 and len(res["glex"]) == 2
    out = B.stage_c(verify_disk=False)
    assert out["problems"] == [], out["problems"]
    m = out["manifest"]
    assert m["shortfalls_after_topup"] == [] and m["v1_pools_unchanged"] and m["merged"] is False
    assert m["counts"]["chosen"] == {"packs": 2, "skins": 8, "freeform": 5, "wordings": 5}
    sel = json.loads(out["files"]["results/selection.json"])["cells"]
    assert sel["packs|train"]["chosen"] == ["t21r2.pack.101", "t21r2.pack.102"]
    assert sel["skins|dispute_email"]["chosen"] == ["t21r2.skin.dispute_email.101", "t21r2.skin.dispute_email.102"]
    assert sel["freeform|dispute_email"]["chosen"] == ["t21r2.free.dispute_email.101", "t21r2.free.dispute_email.102"]
    yc = sel["wordings|yn_capped"]
    assert yc["candidates"][0]["status"] == "G-LEX rejected" and yc["chosen"][0].endswith(".101")
    lex = json.loads(out["files"]["results/topup/lexicon_v1_plus_topup.json"])
    assert len(lex["forms"]) == 98 and all(f["status"] == "admitted" for f in lex["forms"])
    assert all(s["haiku_task_id"].startswith("T21-author_skin-") and s["skin_id"].startswith("T21-SK-")
               for s in json.loads(out["files"]["results/topup/skins.json"]))
    assert not any((B.HERE / rel).exists() for rel in out["files"])          # nothing was written
