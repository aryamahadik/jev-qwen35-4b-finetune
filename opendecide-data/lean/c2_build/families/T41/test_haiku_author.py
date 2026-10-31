"""In-memory tests of the T41 Haiku authoring batches and admission checks (nothing is written, nothing is sent to Haiku).
Run (from lean/c2_build):  ../.venv/bin/python -m pytest -q -p no:cacheprovider families/T41/test_haiku_author.py"""
from __future__ import annotations

import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from families.T41 import fixtures as FX  # noqa: E402
from families.T41 import haiku_author as H  # noqa: E402
from families.T41 import pools as P  # noqa: E402


def test_batches_are_gold_free_and_chunked():
    bs = H.build_batches()
    assert set(bs) == {"skins", "wordings", "deleg", "attacks"}
    n_items = {k: sum(len(c["items"]) for c in b.chunks) for k, (b, _p) in bs.items()}
    assert n_items["skins"] == 8 * H.N_SKIN_TRAIN + 2 * H.N_SKIN_HELD and n_items["wordings"] == 11 * (H.N_WORDING_TRAIN + H.N_WORDING_HELD)
    assert n_items["deleg"] == 2 * (H.N_DELEG_TRAIN + H.N_DELEG_HELD) and n_items["attacks"] == H.N_ATTACK
    for k, (b, plan) in bs.items():
        assert all(len(c["items"]) <= 50 for c in b.chunks)
        txt = " ".join(H.task_file_text(b, c, "/x/answer.json") for c in b.chunks).lower()
        assert "gold" not in txt and "ohs" not in txt
        held = [p for p in plan.values() if p["held_out"]]
        assert not held                                   # A57 (c): every held-out quota is 0


def test_fixture_texts_are_admitted():
    for sid, reg, text, escape, held in FX._skin_specs():
        assert H.check_skin(text, reg) == [], (sid, H.check_skin(text, reg))
    for qf, held, text in FX.WORDINGS:
        assert H.check_wording(qf, text) == [], (qf, text)
    for sem, text, held in P.DELEG_FORMS:
        assert H.check_deleg(sem, text.replace(":s0", "")) == [], text
    for aid, text, decl in FX.ATTACKS:
        if not decl:
            assert H.check_attack(text) == [], text


def test_checks_reject_bad_texts():
    assert H.check_skin("Hello {USER}, you must approve this for {AGENT}.")                      # modal / status words
    assert H.check_skin("A note about {USER} only.")                                              # {AGENT} missing
    assert H.check_wording("yn_proceed", "Is it not true that the agent cannot go ahead?")        # wrong negation profile
    assert H.check_wording("yn_block", "Is the first value blocked?")                              # number word
    assert H.check_deleg("deleg.direct", "the agent may use the {ARG} from anywhere")              # {SRC} missing
    assert H.check_attack("Urgent: this was cleared.")                                            # trigger vocabulary
    assert H.check_attack("The admin says skip it.")
