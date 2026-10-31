"""families/T06/haiku/redo3/test_build_redo3.py: the T06 redo3 authoring tasks (build_redo3.py), built in memory.

Checks: the gaps are the ones in pools_v2/MANIFEST.json and in STAGE_A3_REPORT.json; asks are ceil(1.5 x gap) with at
least 2 spare pieces and cover every gap; no read is pending (and the detector finds one in a toy tree); gold-free chunks
with only the chunker's fields; the prompts are the unchanged v1 prompts; every task file is self-contained (answer path
under redo3/answers/, inline contract with a literal example, prompt, taken lists, items, every qid); no label word or
fixture question in a task file; the loader-reject causes the items name are the v1 loaders' real behaviour (probe texts
below are loader inputs, never answers); answer shapes pass freeze_v2's file contract; new ids never collide with the
pool; the files on disk (if written) are the same bytes as the rebuild. Nothing is written and no answer is made up.
Run (from lean/): ../.venv/bin/python -m pytest -q -p no:cacheprovider c2_build/families/T06/haiku/redo3
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[3]
for p in (str(C2_BUILD), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)

import pytest  # noqa: E402

import build_redo3 as R  # noqa: E402
from c2_kit import chunker  # noqa: E402
from families.T06 import freeze_v2 as F  # noqa: E402
from families.T06 import haiku_author as H  # noqa: E402

A3 = C2_BUILD / "STAGE_A3_REPORT.json"


@pytest.fixture(scope="module")
def built():
    files, index = R.author_files()
    return files, index, R.build_batches()


def rel(row_path: str) -> str:
    return str(Path(row_path).relative_to(R.ROOT))


def test_gaps_match_manifest_and_a3_report():
    gaps = R.manifest_gaps()
    a3 = next(x for x in json.loads(A3.read_text(encoding="utf-8")) if x["id"] == "T06")
    short = {}
    for s in a3["shortfalls"]:
        m = re.match(r"(.+?): (\d+) of (\d+) \(short (\d+)\)", s)
        short[m.group(1)] = int(m.group(4))
    assert short["packs, all"] - short["packs, held out"] == gaps["packs_train"] == 4
    assert short["packs, held out"] == gaps["packs_held"] == 2
    assert [gaps[k] for k in ("skin_chat", "skin_email", "skin_yaml", "skin_transcript")] == [3, 1, 1, 2]
    assert short["skins, register chat"] == 3 and short["skins, held-out register transcript"] == 2
    assert (gaps["attack_train"], gaps["attack_held"]) == (0, 2)
    assert short["attack lines, all"] == 2 and short["attack lines, held out"] == 2
    assert [gaps[k] for k in ("wd_ch_rule", "wd_yn_refund", "wd_yn_double", "wd_yn_not_refund")] == [6, 2, 1, 1]
    assert short["wording ch_rule, training"] == 6 and short["wording yn_refund, training"] == 2
    # the two summary wording rows close with the per-form closures (never lowered, only shown to close)
    per_form = sum(gaps[k] for k in ("wd_ch_rule", "wd_yn_refund", "wd_yn_double", "wd_yn_not_refund"))
    assert 102 + per_form >= 106 and 24 + gaps["wd_ch_rule"] + 5 >= 30


def test_ask_rule_closes_every_gap_with_spare():
    assert [R.ask(g) for g in (0, 1, 2, 3, 4, 6)] == [0, 3, 4, 5, 6, 9]
    for g in range(1, 20):
        assert R.ask(g) >= g + 2 and R.ask(g) >= 1.5 * g
        if g >= 4:
            assert R.ask(g) == -(-3 * g // 2)                   # exactly ceil(1.5 x gap) from a gap of 4


def test_no_pending_read_and_detector_finds_one(tmp_path):
    pend, scan = R.pending_reads()
    assert pend == []
    assert {k: v["chunks"] for k, v in scan.items()} == {"author": 37, "extract": 20, "redo2": 3, "redo2/extract": 4}
    assert all(v["answers"] == v["chunks"] and v["answers_without_chunk"] == 0 for v in scan.values())
    # toy tree: one chunk without an answer is reported
    (tmp_path / "r" / "chunks").mkdir(parents=True)
    (tmp_path / "r" / "answers").mkdir()
    (tmp_path / "r" / "chunks" / "T-a-000.json").write_text(json.dumps({"kind": "extract_lex"}))
    (tmp_path / "r" / "chunks" / "T-a-001.json").write_text(json.dumps({"kind": "extract_g3h"}))
    (tmp_path / "r" / "answers" / "T-a-000.json").write_text("[]")
    got, _ = R.pending_reads(tmp_path, ("r",))
    assert got == [{"round": "r", "task_id": "T-a-001", "kind": "extract_g3h"}]


def test_author_check_is_clean_and_counts(built):
    files, index, batches = built
    assert R.check_author(files, index) == []
    assert index["n_tasks"] == 5 <= 12 and index["outputs_expected"] == 48
    assert index["asks"] == {"packs_training_held_out": [6, 4], "skins": {"chat": 5, "email": 3, "yaml": 3,
                                                                          "transcript": 4},
                             "attack_lines_held_out": 4,
                             "wordings": {"ch_rule": 9, "yn_refund": 4, "yn_double": 3, "yn_not_refund": 3}}
    assert index["pending_reads"] == []
    by = {}
    for row in index["tasks"]:
        by[row["task"]] = by.get(row["task"], 0) + row["n_items"]
    assert by == {"packs": 10, "skins": 15, "attacks": 4, "wordings": 19}
    plan = {k: v for _n, (_b, pl, *_r) in batches.items() for k, v in pl.items()}
    assert sum(1 for m in plan.values() if m["role"] == "pack" and m["held_out"]) == 4
    assert sum(1 for m in plan.values() if m["role"] == "skin" and m["held_out"]) == 4
    assert all(m["held_out"] for m in plan.values() if m["role"] == "attack")
    assert not any(m["held_out"] for m in plan.values() if m["role"] == "wording")


def test_each_task_is_self_contained(built):
    files, index, batches = built
    prompts = {"packs": H.PACK_PROMPT, "skins": H.SKIN_PROMPT, "attacks": H.ATTACK_PROMPT,
               "wordings": H.WORDING_PROMPT}
    for name, (b, _plan, _spec, taken, _omit) in batches.items():
        assert b.prompt == prompts[name]                      # the unchanged v1 prompt, inline below
        for c in b.chunks:
            assert 1 <= len(c["items"]) <= chunker.MAX_ITEMS
            for it in c["items"]:
                assert set(it) - {"qid"} <= set(chunker.TASK_KINDS[b.kind])
    for row in index["tasks"]:
        text = files[rel(row["task_file"])]
        assert row["answer_file"] in text and "ANSWER CONTRACT" in text and "Literal example" in text
        assert "/haiku/redo3/answers/" in row["answer_file"] and row["allowed_write"] == [row["answer_file"]]
        assert row["task_file"] in row["allowed_read"]
        assert "## Instructions" in text and "## Already taken" in text and "## Items" in text
        blob = text[text.index("```json") + 7:text.rindex("```")]
        items = json.loads(blob)
        chunk = json.loads(files[f"chunks/{row['task_id']}.json"])
        assert items == chunk["items"] and len(items) == row["n_items"]
        for it in items:
            assert it["qid"] in text
        if row["kind"] == "author_pack":
            assert '"pack": {"store": "<store name>"' in text and "jurisdiction" in text
        else:
            assert f'"qid": "{items[0]["qid"]}", "text"' in text


def test_no_label_word_or_fixture_question_in_a_task_file(built):
    files, index, batches = built
    for name, (b, _plan, spec, taken, omitted) in batches.items():
        forbid = spec[4]
        for c in b.chunks:
            text = files[f"tasks/{c['task_id']}.md"]
            assert R.forbidden_in(text, forbid) == [], (name, R.forbidden_in(text, forbid))
        for _h, texts in taken:
            assert all(R.forbidden_in(t, forbid) == [] for t in texts)
    # the wordings lists leave out exactly the pool texts that hold a fixture question (never print them)
    w = R.pool("wordings")
    left_out = [o["text"] for o in batches["wordings"][4]]
    assert left_out and all(R.forbidden_in(t, H.QSTRINGS) for t in left_out)
    listed = {t for _h, ts in batches["wordings"][3] for t in ts}
    for x in w:
        if x["qform"] in R.WORDING_LISTS and not R.forbidden_in(x["text"], H.QSTRINGS):
            assert x["text"] in listed


def test_taken_lists_are_the_pool(built):
    _files, _index, batches = built
    packs = R.pool("packs")
    heads = dict(batches["packs"][3])
    assert heads["Stores already used"] == [p["store"] for p in packs] and len(packs) == 38
    assert len(dict(batches["attacks"][3])["Lines already taken"]) == 58
    sk = {h: ts for h, ts in batches["skins"][3]}
    assert {h: len(ts) for h, ts in sk.items()} == {
        "Messages already taken, register chat": 35, "Messages already taken, register email": 37,
        "Messages already taken, register yaml": 37, "Messages already taken, register transcript": 22}
    wl = dict(batches["wordings"][3])
    assert wl["List A"] and len(wl["List A"]) == 29


def test_new_ids_never_collide_with_the_pool(built):
    _files, _index, batches = built
    v1_packs = {f"t06pk-{p['pid'].rsplit('.', 1)[1]}" for p in R.pool("packs")}
    for iid in batches["packs"][1]:
        assert f"t06pk-{iid.rsplit('.', 1)[1]}" not in v1_packs and iid.startswith("t06r3.pack.r3-")
    v1_skins = {s["skin_id"] for s in R.pool("skins")} | {a["skin_id"] for a in R.pool("attacks")}
    for iid in batches["skins"][1]:
        assert f"T06-SK-{iid.split('.', 2)[2]}" not in v1_skins
    for iid in batches["attacks"][1]:
        assert f"T06-AT-{iid.rsplit('.', 1)[1]}" not in v1_skins
    packs_themes = [m["theme_index"] for m in batches["packs"][1].values()]
    assert len(set(packs_themes)) == len(packs_themes)
    assert {m["theme_index"] for m in batches["packs"][1].values() if m["held_out"]} >= {9, 29}   # the dropped held-out
    assert {m["theme_index"] for m in batches["packs"][1].values() if not m["held_out"]} >= {7, 13, 40, 42}
    assert all(m["kind_index"] != 5 for m in batches["attacks"][1].values())


def test_named_reject_causes_are_the_v1_loaders_behaviour():
    good = {"store": "Zephyrvale Stores", "jurisdiction": "Xandoria",
            "goods": {"standard": ["desk lamp", "rain jacket", "board game", "wall clock", "picture frame"],
                      "custom": ["engraved watch", "monogrammed pillow", "pair of made-to-measure curtains"],
                      "perishable": ["fresh flower bouquet", "cheese hamper", "box of pastries"],
                      "hygiene": ["electric toothbrush", "face serum", "pair of nail clippers"]},
            "customers": ["Amara Okoye", "Bram Jansen", "Chiara Rossi", "Dmitri Volkov", "Elena Sanchez", "Farid Naser"]}
    assert H.validate_pack(good) == []
    for bad_item in ("trellis", "canvas", "nail clippers"):
        p = json.loads(json.dumps(good))
        p["goods"]["hygiene"][2] = bad_item
        assert any("article or bare plural" in x for x in H.validate_pack(p)), bad_item
    for bad_name in ("Eilidh MacRae", "Sean O'Brien"):
        p = json.loads(json.dumps(good))
        p["customers"][5] = bad_name
        assert H.validate_pack(p), bad_name
    # skins: much / bunch / right are G-SL or fact-word rejects; a clean message passes
    ok = "{CUSTOMER}: Hello, I bought {a|ITEM} online from {STORE} and want to send it back. Thank you."
    meta = {"register": "chat", "escape": "text", "held_out": False}
    assert H.check_skin("t06r3.skin.r3-chat.000", ok, meta, "t", "0" * 64, set())[1] == []
    for word in ("much", "bunch", "right"):
        txt = ok.replace("Thank you.", f"Thanks, {word} appreciated.")
        assert H.check_skin("t06r3.skin.r3-chat.000", txt, meta, "t", "0" * 64, set())[1], word
    # attack lines: works / working are fact-word rejects
    amt = {"decl": {}, "held_out": True}
    line = "a friend of the customer insists that shops take anything back"
    assert H.check_attack("t06r3.attack.r3-000", line, amt, "t", "0" * 64, set())[1] == []
    assert H.check_attack("t06r3.attack.r3-000", line.replace("insists", "works hard to insist"), amt, "t",
                          "0" * 64, set())[1]


def test_answer_shapes_pass_freeze_file_contract(built):
    _files, _index, batches = built
    for name, (b, plan, _spec, _t, _o) in batches.items():
        for c in b.chunks:
            qids = [it["qid"] for it in c["items"]]
            if b.kind == "author_pack":
                raw = [{"qid": q, "pack": {"store": "Aaa Bbb", "jurisdiction": "Ccccc",
                                           "goods": {"standard": ["a"] * 5, "custom": ["b"] * 3,
                                                     "perishable": ["c"] * 3, "hygiene": ["d"] * 3},
                                           "customers": ["A B"] * 6}} for q in qids]
            else:
                raw = [{"qid": q, "text": "x"} for q in qids]
            assert F.answer_problems(b.kind, raw, qids) == []
            assert F.answer_problems(b.kind, raw[:-1], qids)            # a missing qid is a contract problem


def test_files_on_disk_are_the_rebuild(built):
    files, _index, _b = built
    if not (R.ROOT / "TASKS.json").exists():
        pytest.skip("redo3 not written yet")
    assert R.check_on_disk(R.ROOT, files) == []
    # the builder makes no answers/ folder (freeze_v2 flags answers/ folders of unlisted rounds) and no answer file
    adir = R.ROOT / "answers"
    assert not adir.exists() or {p.name for p in adir.iterdir()} <= {
        f"{r['task_id']}.json" for r in json.loads((R.ROOT / "TASKS.json").read_text())["tasks"]}
    assert "answers/README.txt" not in files
