"""A49 additions to gen_full_c2.py (16 Oct 2026): the type-keeping redraw, the per-hash-cell G10 position / rank check, the
prefix of a larger QC build, the G6 excess summary, and the A49 binding rule."""
import sys
import types
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

import gen_full_c2 as G  # noqa: E402
from c2_kit.distractors import Option, OptionSet  # noqa: E402


# ---------------------------------------------------------------- redraw keeps the question type
class _QF:
    def __init__(self, qtype):
        self.qtype = qtype


class _Plugin:
    QFORMS = {"yn_dead": _QF("noul"), "yn_live": _QF("noul"), "ch_live": _QF("choice"), "ch_dead": _QF("choice")}

    def sample(self, seed, sampler):
        # seed % 4 chooses the form; seed 0 -> dead yes/no; redraws (seed + j * stride) land on other forms by j
        order = ["yn_dead", "ch_live", "ch_dead", "yn_live"]
        j = seed // G.REDRAW_STRIDE
        base = seed % G.REDRAW_STRIDE
        return types.SimpleNamespace(qform=order[(base + j) % 4], seed=seed)


def test_redraw_keeps_question_type_and_block_position():
    pl = _Plugin()
    rd = G.Redraw(pl, {"yn_dead", "ch_dead"})
    spec = pl.sample(0, "s")                       # j=1 -> ch_live (wrong type: skipped), j=2 -> ch_dead (dead), j=3 -> yn_live
    assert spec.qform == "yn_live"
    assert spec.seed == 3 * G.REDRAW_STRIDE and spec.seed % 32 == 0
    assert pl.sample(1, "s").qform == "ch_live"    # a live draw is untouched
    assert pl.sample(2, "s").qform == "yn_live" or pl.sample(2, "s").qform in ("ch_live", "yn_live")
    assert rd.redrawn["yn_dead"] == 3
    rd.restore()
    assert "sample" not in pl.__dict__


def test_redraw_dead_choice_gives_choice():
    pl = _Plugin()
    rd = G.Redraw(pl, {"ch_dead"})
    spec = pl.sample(2, "s")                       # ch_dead -> j=1 yn_live (wrong type), j=2 yn_dead (wrong type), j=3 ch_live
    assert pl.QFORMS[spec.qform].qtype == "choice" and spec.qform == "ch_live"
    rd.restore()


# ---------------------------------------------------------------- per-cell G10
def _set(k, gold, rank=None):
    opts = [Option(i, f"o{i}", "gold" if i == gold else "error") for i in range(k)]
    return OptionSet(opts, gold, {"gold_rank": rank})


def _units(sets):
    return [types.SimpleNamespace(rendered=[types.SimpleNamespace(option_set=s)]) for s in sets]


def test_partner_rows_count_once_per_cell():
    # 90 cells, each used by 3 partner rows; the 90 cells are position-uniform over k=3, so the cell test passes
    sets, reg = [], {}
    for c in range(90):
        for _ in range(3):
            s = _set(3, c % 3, c % 3)
            sets.append(s)
            reg[id(s)] = (s, f"key{c}", f"key{c}")
    out = G.g10_cell_checks(_units(sets), reg)
    assert out["gold_position"]["value"]["counts"]["3"] == [30, 30, 30]
    assert out["gold_position"]["value"]["position_cells"] == 90 and out["gold_position"]["verdict"] == "pass"
    assert out["gold_rank"]["value"]["counts"]["3"] == [30, 30, 30]


def test_cell_check_fails_a_real_skew_and_counts_untraced_sets():
    sets, reg = [], {}
    for c in range(60):
        s = _set(3, 0 if c < 40 else c % 3, 0)
        sets.append(s)
        reg[id(s)] = (s, f"key{c}", f"key{c}")
    sets.append(_set(3, 1, 1))                      # never traced: its own cell
    out = G.g10_cell_checks(_units(sets), reg)
    assert out["gold_position"]["verdict"] == "fail" and out["gold_position"]["value"]["sets_not_traced"] == 1


def test_annotate_g10_replaces_row_level_checks():
    g10 = {"checks": {"gold_position": {"value": 1, "verdict": "fail", "bar": "b"},
                      "gold_rank": {"value": 2, "verdict": "pass", "bar": "b"},
                      "yes_rate_cells": {"verdict": "pass"}}, "failing": ["gold_position"], "verdict": "fail"}
    cell = {"gold_position": {"value": 3, "verdict": "pass", "bar": "c", "unit": "cell"},
            "gold_rank": {"value": 4, "verdict": "pass", "bar": "c", "unit": "cell"}}
    g = G.annotate_g10(g10, "T30", 0, 0, cell)
    assert g["verdict"] == "pass" and g["checks"]["gold_position"]["unit"] == "cell"
    assert g["checks"]["gold_position_rowlevel"]["verdict"] == "report"
    assert G.annotate_g10(g10, "T30", 0, 0)["verdict"] == "fail"          # old callers: unchanged behaviour


# ---------------------------------------------------------------- prefix and G6 summary
def test_prefix_build_is_the_smaller_build():
    infos = [types.SimpleNamespace(unit=u, row={"id": f"{u}.{j}"}) for u in range(10) for j in range(3)]
    b = types.SimpleNamespace(infos=infos, units=list(range(10)), stats={"rows_written": 30})
    p = G.prefix_build(b, 10, 3_000_000)           # units hold 3 rows: 4 units = 12 >= 10, as build_pilot would stop
    assert p.stats["units_written"] == 4 and p.stats["rows_written"] == 12 and len(p.units) == 4
    assert G.prefix_build(b, 12, 1).stats["rows_written"] == 12             # stops at the first unit that reaches n


def _g6(acc_yes, acc_ch):
    v = lambda a: {"lr": a, "gbt": a}  # noqa: E731
    return {"yes_no": {"n": 100, "chance": 0.5, "a_question": v(acc_yes), "c_card_without_question": v(0.5), "d_meta": v(0.5)},
            "choice": {"n": 100, "chance": 0.34, "a_question": v(0.34), "b_options": v(acc_ch),
                       "c_card_without_question": v(0.34), "d_meta": v(0.34)}}


def test_g6_summary_bar_and_max_cell():
    ok = G.g6_summary(_g6(0.51, 0.35))
    assert ok["verdict"] == "pass" and ok["max_excess_pp"] == 1.0
    bad = G.g6_summary(_g6(0.51, 0.3601))
    assert bad["verdict"] == "fail" and bad["max_cell"].startswith("choice/b_options")


def test_a49_binding_rule():
    gates = {"G2": {"verdict": "pass"}, "G10": {"verdict": "fail"}, "overlay": {"verdict": "fail"},
             "spec_3_0": {"verdict": "fail"}, "G6": {"verdict": "fail"}, "G7": {"verdict": "pass"},
             "G11": {"verdict": "pass"}, "G12": {"verdict": "pass"}, "full_size": {"verdict": "pass"}}
    assert G.program_pass_a49(gates) == (False, ["G6_24K_missing"])
    gates["G6_24K"] = {"verdict": "pass"}
    assert G.program_pass_a49(gates) == (True, [])
    gates["G6_24K"] = {"verdict": "fail"}
    assert G.program_pass_a49(gates)[1] == ["G6_24K"]
    gates["G6_24K"] = {"verdict": "pass"}
    gates["G11"] = {"verdict": "fail"}
    assert G.program_pass_a49(gates)[1] == ["G11"]
