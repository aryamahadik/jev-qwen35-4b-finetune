"""pytest for the T46 Haiku pipeline (from lean/c2_build):  ../../.venv/bin/python -m pytest -q -p no:cacheprovider families/T46/test_haiku_author.py
Writes only under families/T46/_scratch_test/ (removed at the end): the authoring chunks, the G-LEX read chunks, the frozen pools."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest

C2 = Path(__file__).resolve().parents[2]
if str(C2) not in sys.path:
    sys.path.insert(0, str(C2))

from c2_kit import chunker  # noqa: E402
from families.T46 import fixtures as FX  # noqa: E402
from families.T46 import haiku_author as HA  # noqa: E402
from families.T46 import plugin as P  # noqa: E402
from families.T46 import tables as T  # noqa: E402

SCRATCH = Path(__file__).resolve().parent / "_scratch_test"


@pytest.fixture(scope="module")
def scratch():
    shutil.rmtree(SCRATCH, ignore_errors=True)
    SCRATCH.mkdir()
    yield SCRATCH
    shutil.rmtree(SCRATCH, ignore_errors=True)


def synth_answers(batches):
    """{name: {task_id: [{"qid", "texts"}]}}: every item answered from the stand-in pools (one text per slot of the brief)."""
    raw = {}
    for name, b in batches:
        inv = {q: iid for q, iid in b.key.items()}
        per_task = {}
        for c in b.chunks:
            ans = []
            for it in c["items"]:
                iid = inv[it["qid"]]
                parts = iid.split("|")
                if name == "wordings":
                    texts = FX.WORDINGS[parts[1]]["dev" if parts[2] == "dev" else "train"]
                elif name == "glosses":
                    texts = FX.GLOSSES[parts[1]]["dev" if parts[2] == "dev" else "train"]
                elif name == "names":
                    texts = FX.NAMES_AR["dev" if parts[1] == "dev" else "train"]
                else:
                    texts = FX.NOTES_AR[parts[1]][parts[2]]["dev" if parts[3] == "dev" else "train"]
                ans.append({"qid": it["qid"], "texts": list(texts)})
            per_task[c["task_id"]] = ans
        raw[name] = per_task
    return raw


def test_authoring_tasks_are_written_and_label_blind(scratch):
    root = scratch / "author"
    tasks = HA.write_tasks(root)
    assert 8 <= len(tasks) <= HA.MAX_TASKS
    for t in tasks:
        assert Path(t["task_file"]).is_file() and t["answer_file"].startswith(str(root))
        body = json.loads(Path(t["task_file"]).read_text())
        assert body["answer_file"] == t["answer_file"] and body["instructions"]
        assert not any(k in json.dumps(body["items"]).lower() for k in ("\"gold\"", "\"label\""))
    man = json.loads((root / "TASKS.json").read_text())
    assert set(man["batches"]) == {"wordings", "glosses", "names", "notes"}


def test_answers_are_loaded_linted_and_counted(scratch):
    batches = HA.build_batches(scratch / "author")
    pieces = HA.load_pieces(batches=dict(batches), raw=synth_answers(batches))
    c = pieces["counts"]
    assert c["wordings"]["yn_is"]["train"] >= 5 and c["wordings"]["ch_disp"]["dev"] >= 1
    assert c["glosses"]["E"]["train"] >= 5 and c["names_ar"]["train"] >= 5
    assert sum(c["notes_ar"][wf]["H"]["dev"] for wf in c["notes_ar"]) >= 1 and sum(c["notes_ar"][wf]["D"]["train"] for wf in c["notes_ar"]) >= 1   # the stand-in notes are shared by every workflow: a duplicate is kept once
    assert pieces["drops"].get("duplicate", 0) > 0                     # the same stand-in text answered twice is kept once
    assert not [p for p in pieces["problems"] if "drop " in p and "duplicate" not in p], pieces["problems"][:5]


def test_a_bad_answer_is_dropped_never_fixed(scratch):
    batches = HA.build_batches(scratch / "author")
    raw = synth_answers(batches)
    first = next(iter(raw["wordings"].values()))
    first[0]["texts"] = ["Should we pay it?", "Is the proposed action 7 times right?"] + first[0]["texts"]
    pieces = HA.load_pieces(batches=dict(batches), raw=raw)
    assert pieces["drops"]
    flat = json.dumps(pieces["pools"], ensure_ascii=False)
    assert "Should we pay it?" not in flat and "7 times" not in flat


def test_glex_reads_admit_correct_forms_and_reject_wrong_ones(scratch):
    pools = {"wordings": FX.WORDINGS, "glosses": FX.GLOSSES, "names_ar": FX.NAMES_AR, "notes_ar": FX.NOTES_AR}
    reg = HA.registry_for(pools)
    reg.unit_test_all()
    assert all(f.unit_ok for f in reg.forms.values()), [f.unit_problems for f in reg.forms.values() if not f.unit_ok][:3]
    bs = HA.extraction_batches(reg, scratch / "extract", tag="main")
    assert len(bs) == 2 and sum(len(b.chunks) for _, b in bs) >= 6
    raw = {}
    wrong = None
    for n, b in bs:
        per = {}
        for c in b.chunks:
            ans = []
            for it in c["items"]:
                fid = b.key[it["qid"]]
                f = reg.forms[fid]
                meaning = reg.sems[f.sem_id].meaning
                if n.endswith("read1") and wrong is None and f.sem_id == "disp.hold":
                    wrong = fid
                    meaning = reg.sems["disp.deny"].meaning                  # one reader disagrees
                ans.append({"qid": it["qid"], "choice": meaning})
            per[c["task_id"]] = ans
        raw[n] = per
    rec = HA.record_extractions(reg, bs, raw=raw)
    assert rec["reads"]["disagree"] == 1 and not rec["problems"]
    assert reg.status(wrong) == "rejected"
    assert sum(1 for i in reg.forms if reg.status(i) == "admitted") == len(reg.forms) - 1


def test_freeze_and_load_roundtrip_gives_a_working_plugin(scratch):
    pools = {"wordings": FX.WORDINGS, "glosses": FX.GLOSSES, "names_ar": FX.NAMES_AR, "notes_ar": FX.NOTES_AR}
    reg, nreg = HA.registry_for(pools), HA.names_registry(pools)
    reg.unit_test_all()
    nreg.unit_test_all()
    for r in (reg, nreg):
        for fid, f in r.forms.items():
            for e in range(f.required):
                r.record_extraction(fid, f"haiku:test-{e}", f.sem_id)
    pieces = {"pools": pools, "drops": {}}
    root = scratch / "pools"
    man = HA.freeze(pieces, reg, nreg, root=root)
    assert man["lexicon_status"] == {"admitted": len(reg.forms)} and man["names_status"] == {"admitted": len(nreg.forms)}
    assert HA.frozen_pools_exist(root) and man["counts"]["wordings.jsonl"] == 40
    plugin, ctx = HA.load_plugin(root)
    from c2_kit import pipeline
    ok = 0
    for seed in range(20):
        sp = plugin.sample(seed, "S1")
        ok += pipeline.build_unit(plugin, sp, ctx, run_g15=False).ok
    assert ok == 20
    # a changed frozen file is refused
    f = root / "glosses.jsonl"
    f.write_text(f.read_text() + "\n")
    with pytest.raises(RuntimeError):
        HA.load_pools(root)


def test_quarantine_leaves_a_piece_out_but_keeps_its_form(scratch):
    pools = {"wordings": FX.WORDINGS, "glosses": FX.GLOSSES, "names_ar": FX.NAMES_AR, "notes_ar": FX.NOTES_AR}
    recs = HA.pools_to_records(pools)
    rid = recs["glosses.jsonl"][0]["id"]
    cut = HA.records_to_pools(recs, {rid})
    assert sum(len(v["train"]) + len(v["dev"]) for v in cut["glosses"].values()) == 31


def test_arabic_probe_check_reads_only_arabic_literals(tmp_path):
    f = tmp_path / "pg.py"
    f.write_text('A = {"x": "ليلى حداد"}\nB = "latin only"\n', encoding="utf-8")
    assert HA.arabic_literals(f) == {"ليلى حداد"}


def test_topup_items_are_dneg_only_and_load_from_disk():
    from families.T46 import haiku_author as H
    items = H.topup_items()
    assert len(items) == H.TOPUP_ITEMS and all(i.startswith("wording|yn_dneg|train|T") for i, _ in items)
    bs = H.topup_batches()
    assert set(bs) <= {"wordings_topup", "wordings_topup2", "notes_topup2"}
