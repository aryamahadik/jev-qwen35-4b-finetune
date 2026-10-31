"""families/T31/test_haiku_author.py: the T31 authoring tasks and their loader, in memory only (nothing is written).

Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/families/T31/test_haiku_author.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker as CH  # noqa: E402
from c2_kit.lexicon import LexiconRegistry  # noqa: E402
from families.T31 import haiku_author as H  # noqa: E402
from families.T31 import plugin as P  # noqa: E402


@pytest.fixture(scope="module")
def built():
    return H.files_for(H.build_batches())


def test_at_most_40_self_contained_tasks(built):
    files, manifest = built
    tasks = manifest["tasks"]
    assert 1 <= len(tasks) <= 40 and manifest["g0_sha256"] == P.POOL_G0_SHA256
    kinds = {t["kind"] for t in tasks}
    assert kinds == {"author_skin", "author_freeform", "author_wording", "author_lexicon", "author_pack"}
    for t in tasks:
        text = files[t["task_file"].split("/haiku/author/")[1]]
        assert t["answer_file"] in text.split("\n")[3] and t["answer_file"].startswith(str(H.ROOT))
        assert 1 <= t["n_items"] <= CH.MAX_ITEMS and t["task_file"] in t["allowed_read"]
        items = json.loads(text[text.index("ITEMS (JSON"):].split("\n", 1)[1].rsplit("\n\nReminder", 1)[0])
        assert len(items) == t["n_items"] and all(re.fullmatch(r"q[0-9a-f]{10}", it["qid"]) for it in items)
    held = {t["register"] for t in tasks if t["pool"] == "skin" and t["held_out"]}
    assert held == set(P.T31.HELD_OUT_REGISTERS)
    regs = {t["register"] for t in tasks if t["pool"] == "skin" and not t["held_out"]}
    assert len(regs) >= 8 and regs <= set(P.T31.REGISTERS)


def test_no_label_word_or_question_text_reaches_an_authoring_task(built):
    files, manifest = built
    for t in manifest["tasks"]:
        low = files[t["task_file"].split("/haiku/author/")[1]].lower()
        forbid = H.FORBID_WORDING if t["kind"] == "author_wording" else H.FORBID_SKIN
        for f in forbid:
            assert not re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", low), (t["task"], f)
        for key in ("gold", "answer_key", "solver"):
            assert f'"{key}"' not in low


def test_pool_plan_covers_the_g0_targets(built):
    _files, manifest = built
    n = {}
    for t in manifest["tasks"]:
        n[t["pool"]] = n.get(t["pool"], 0) + t["n_items"]
    assert n["wording"] == sum(H.WORDINGS.values()) >= 150
    assert n["skin"] >= 2 * sum(H.SKINS_T.values()) and n["freeform"] / (n["skin"] + n["freeform"]) <= 0.25
    assert n["comparator"] == 4 * H.BANDS_PER_SEM and n["attack"] == 2 * H.ATTACKS
    for q, k in H.WORDINGS.items():                     # each wording <= 2% of the family's rows (G0 7)
        assert k >= 6, q


def test_loader_keeps_clean_pieces_and_drops_leaky_ones():
    pools = {"skins": {}, "attacks": {}, "wordings": {}, "packs_appr": [], "packs_agent": [], "names": [],
             "lexicon": H.declare_lexicon(LexiconRegistry("T31"))}
    task = {"task_id": "T31-author_test-000", "prompt_sha": "0" * 64}
    keep = [(["skin", "appr", "memo", "T", "0"], {"slots": {"REQ_ID": "required, exactly once"}},
             "Internal memo for the sign-off desk.\n{REQUESTER} sent in {a|ITEM} under reference {REQ_ID}."),
            (["skin", "agent", "json", "T", "1"], {"slots": {"REQ_ID": "leave it out"}},
             '{"raised_by": {REQUESTER}, "task": {ITEM}}'),
            (["wording", "yn_holder_not", "2"], {"slots": {"REQ_ID": "optional, at most once"}},
             "Is it true that {CANDIDATE} does not hold the accountable (A) role for request {REQ_ID}?"),
            (["band", "cmp.le", "3"], {}, "of {X} or less")]
    drop = [(["skin", "appr", "memo", "T", "4"], {"slots": {"REQ_ID": "leave it out"}},
             "Memo. {REQUESTER} has already signed {a|ITEM}, approved."),
            (["wording", "yn_agent_ok", "5"], {"slots": {"REQ_ID": "optional, at most once"}},
             "Is {REQ_AGENT} currently allowed to use {REQ_SCOPE}?"),
            (["band", "cmp.gt", "6"], {}, "not exceeding {X}"),
            (["free", "appr", "chat", "T", "7"],
             {"facts": {"REQUESTER": "Ana Ruiz", "ITEM": "server rack order", "REQ_ID": "REQ-1234"}},
             "Ana Ruiz: hi, sending a server rack order, ref REQ-1234.")]
    for parts, item, text in keep:
        assert H._load_one(task, parts, item, {"text": text}, f"q{parts[-1]}", pools) is None, text
    for parts, item, text in drop:
        assert H._load_one(task, parts, item, {"text": text}, f"q{parts[-1]}", pools), text
    assert all(P.skin_track(s) in ("appr", "agent") for s in pools["skins"].values())
    reg = pools["lexicon"]
    assert all(reg.unit_test_all().values()) and all(reg.status(f) != "admitted" for f in reg.forms)
