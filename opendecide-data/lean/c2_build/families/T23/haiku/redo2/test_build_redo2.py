"""families/T23/haiku/redo2/test_build_redo2.py: in-memory tests of build_redo2.py (nothing is written).

  frame rule      flags exactly the ten v1 forms with a negated question frame (G0 v3 section 10 B3/B4), none else
  fill            every G-LEX redo2 text is filled as a row fills it: pack DOC / TERM_LABEL, CASE-dddd, a version id;
                  no placeholder value, no value in two slots (B1)
  task files      self-contained: answer path inline, no internal id, the v1 G-LEX prompt, two separate reads
  G3-H schema     same field names and kinds as plugin.extract_fields; only the item describe changes (B2)
  plumbing        stage B / C on SYNTHETIC in-memory answers (monkeypatched loader; a code test, never data): the
                  admission rule keeps v1 rejections, needs both redo2 reads, rejects on a decoy or invalid pick
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

EXCLUDED = ["q.t23.yn_claim#485c0a50", "q.t23.yn_claim#8c77afd3", "q.t23.yn_claim#b0ba2bfe",
            "q.t23.yn_outcome#961b0c9e", "q.t23.yn_outcome#cfa3f0d3", "q.t23.yn_outcome#e4058170",
            "q.t23.yn_outcome_not#e68728cb", "q.t23.yn_version#c00d7af6", "q.t23.yn_version#c7854e2e",
            "q.t23.yn_version#d349e7f6"]


@pytest.fixture(scope="module")
def built():
    return B.stage_a()


def test_frame_rule_on_v1_forms():
    reg = B.v1_registry()
    part = B.b1_partition(reg)
    assert sorted(part["excluded_frame"]) == EXCLUDED
    assert part["v1_rejected"] == ["q.t23.yn_version_other#3e049a82"]
    assert len(part["reread"]) == 195 and not set(part["reread"]) & set(EXCLUDED)
    assert all(reg.status(f) == "admitted" for f in part["reread"])


@pytest.mark.parametrize("text,bad", [
    ("Isn't it so that case {CASE_ID} is within the {TERM_LABEL}?", True),
    ("Under these rules, doesn't the quantity fit within the {TERM_LABEL}?", True),
    ("Is it not the case that {CANDIDATE} governs case {CASE_ID}?", True),
    ("Does it not hold that the governing version supports the claim to check?", True),
    ("Does {CANDIDATE} govern case {CASE_ID}, doesn't it?", True),
    ("Is not {CANDIDATE} the governing version?", True),
    ("Is it so that it is not the case that {CANDIDATE} does not govern case {CASE_ID}?", False),
    ("According to the card, is it the case that {CANDIDATE} does not govern case {CASE_ID}?", False),
    ("Does {CANDIDATE} not govern case {CASE_ID} under {DOC}?", False),
    ("Would this case not sit within the {TERM_LABEL} set by the governing version?", False),
])
def test_frame_rule_cases(text, bad):
    assert bool(B.frame_problems(text)) is bad


def test_no_word_rule_only_on_double_negation():
    assert B.v3_problems("Is case {CASE_ID} not a case that is not beyond the {TERM_LABEL}?")
    assert not B.v3_problems("Does case {CASE_ID} go beyond the {TERM_LABEL} set by the governing version?")
    assert not B.v3_problems("Is case {CASE_ID} not a case that does not fall within the {TERM_LABEL}?")


def test_fill_is_row_like(built):
    files, _rows = built
    fills = json.loads(files["plan/b1_fills.json"])
    assert len(fills) == 195
    for fid, f in fills.items():
        v, txt = f["values"], f["text"]
        assert len(set(v.values())) == len(v), fid
        assert "{" not in txt and "Dana Okafor" not in txt and "INV-20419" not in txt
        pack = B.P.DOMAINS[f["domain"]]
        assert v.get("DOC", pack.doc) == pack.doc and v.get("TERM_LABEL", pack.term) == pack.term
        assert re.fullmatch(r"CASE-\d{4}", v.get("CASE_ID", "CASE-1000"))
        assert re.fullmatch(r"v[1-4]|rev-[A-D]|[A-Z]{2}-\d{3}", v.get("CANDIDATE", "v1"))


def test_task_files_self_contained(built):
    files, rows = built
    kinds = {}
    for r in rows:
        txt = files[r["task_file"].split("/haiku/redo2/")[1]]
        assert r["answer_file"] in txt and r["answer_file"].startswith(str(B.HERE / "answers"))
        assert "q.t23." not in txt and "t23r2." not in txt and "T23-MF-" not in txt
        kinds.setdefault((r["kind"], r["read"]), 0)
        kinds[(r["kind"], r["read"])] += r["n_items"]
    assert kinds == {("extract_lex", "glex-r2read0"): 195, ("extract_lex", "glex-r2read1"): 195,
                     ("extract_g3h", "g3h-r2"): 172, ("author_wording", None): 27}
    assert len({r["batch_id"] for r in rows if r["kind"] == "extract_lex"}) == 2
    assert B.lex_prompt() == B.HX.LEX_PROMPT + B.HX.LEX_TAIL


def test_g3h_schema_names_kinds_unchanged():
    new, old = B.g3h_fields(), B.P.T23.extract_fields(None, None)
    assert [(f.name, f.kind) for f in new] == [(f.name, f.kind) for f in old]
    assert [f.describe for f in new if f.name != "item"] == [f.describe for f in old if f.name != "item"]


# ------------------------------------------------------------------------------------------------ plumbing (synthetic)
_FAKE = {   # in-memory only: shapes that pass the v1 loader and the v3 rules, plus deliberate failures
    "yn_version": ["Is it so that it is not the case that {CANDIDATE} does not govern case {CASE_ID}?",
                   "Under these rules, is {CANDIDATE} not a version that does not govern case {CASE_ID}?",
                   "Isn't it so that {CANDIDATE} does not govern case {CASE_ID}?"],                    # frame: drop
    "yn_claim": ["Going by the version history, is the claim to check not a claim that the governing version does "
                 "not support?",
                 "Is the claim to check not a claim that the governing version does not differ from?"],  # no-word: drop
    "yn_outcome": ["Does it hold that it is not the case that case {CASE_ID} does not fall within the {TERM_LABEL} "
                   "set by the governing version?",
                   "Is case {CASE_ID} not within the {TERM_LABEL} set by the governing version?"],       # k_syn 1: drop
}


def test_stage_b_c_plumbing(monkeypatch):
    db, dplan = B.dneg_batch()
    reg0 = B.v1_registry()
    part = B.b1_partition(reg0)
    lex1 = B.glex_batches(reg0, part["reread"], "b1")
    g3, expected = B.g3h_batch()
    used = {q: 0 for q in _FAKE}
    dneg_ans = []
    for qid, iid in sorted(db.key.items()):
        q = dplan[iid]["qform"]
        if used[q] < len(_FAKE[q]):
            dneg_ans.append({"qid": qid, "text": _FAKE[q][used[q]]})
            used[q] += 1
    meaning = {s.sem_id: s.meaning for s in reg0.sems.values()}
    decoy_fid, invalid_fid = part["reread"][0], part["reread"][1]

    def lex_answers(b, reg):
        out = {}
        for c in b.chunks:
            ans = []
            for it in c["items"]:
                fid = b.key[it["qid"]]
                ch = meaning[reg.forms[fid].sem_id]
                if fid == decoy_fid and b.batch_id == lex1[1][1].batch_id:
                    ch = meaning["q.t23.decoy_today"]
                if fid == invalid_fid and b.batch_id == lex1[0][1].batch_id:
                    ch = "something else"
                ans.append({"qid": it["qid"], "choice": ch})
            out[c["task_id"]] = ans
        return out

    g3_bad = sorted(expected)[0]
    cache = {}

    def fake_load(b):
        if b.batch_id == db.batch_id:
            return {db.chunks[0]["task_id"]: dneg_ans}, []
        if b.kind == "extract_g3h":
            out = {}
            for c in b.chunks:
                out[c["task_id"]] = [{"qid": it["qid"], **{k: (("the " + v) if (k == "item" and b.key[it["qid"]] ==
                                                                               g3_bad) else v)
                                                           for k, v in expected[b.key[it["qid"]]]["expected"].items()}}
                                     for it in c["items"]]
            return out, []
        if any(b.key[q] in reg0.forms for q in b.key):
            return lex_answers(b, reg0), []
        if "reg_b" not in cache:
            cache["reg_b"] = B.dneg_forms()[0]
        return lex_answers(b, cache["reg_b"]), []

    monkeypatch.setattr(B, "_load_raw", fake_load)
    reg_b, new, drops, _p = B.dneg_forms()
    assert len(new) == 4, (new, drops)
    assert any("frame" in r for v in drops.values() for r in v)
    assert any("'no' word" in r for v in drops.values() for r in v)
    assert any("negcount" in r for v in drops.values() for r in v)
    out = B.stage_c()
    lex = out["results/glex_redo2.json"]
    st = lex["status"]
    assert st[decoy_fid] == "rejected" and st[invalid_fid] == "rejected"
    assert all(st[f] == "excluded_frame" for f in EXCLUDED)
    assert st["q.t23.yn_version_other#3e049a82"] == "rejected_v1"
    assert all(st[f] == "admitted" for f in new)
    assert sum(1 for s in st.values() if s == "admitted") == 195 - 2 + 4
    assert lex["double_negation_admitted"] == {"yn_claim": 1, "yn_outcome": 1, "yn_version": 2}
    g = out["results/g3h_redo2.json"]
    assert g["n"] == 172 and g["pass"] == 171
    assert [r["sid"] for r in g["rows"] if not r["ok"]] == [g3_bad]
