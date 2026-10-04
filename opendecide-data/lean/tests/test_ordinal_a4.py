"""Recipe v4 A4 (ordinal mean term) and F2 (rendered-prompt identity): CPU tests, synthetic rows, no model download.

Run:  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python -m pytest -q tests/test_ordinal_a4.py
The F2 test on the real Qwen3.5-4B tokenizer runs only when it is in the local Hugging Face cache (offline).
"""
from __future__ import annotations

import json
import math
import os
import random
import sys
from pathlib import Path

import pytest
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import decoder_io  # noqa: E402
import train_decoder as td  # noqa: E402
from test_train_loss import _write_data, choice, fake_env, noul, opts  # noqa: E402,F401

pytestmark = pytest.mark.filterwarnings("ignore::UserWarning")  # torch.autocast("cuda") on a CPU-only box


def ordinal(rid, call, k, gold_level, scramble=None, meta=None):
    names = [f"lv{j}" for j in range(k)]
    order = scramble or list(range(k))
    r = choice(rid, call, [names[j] for j in order], names[gold_level])
    r["meta"] = {"option_level": {n: j for j, n in enumerate(names)}, **(meta or {})}
    return r


# ---------------------------------------------------------------- 1. the term (pre-flight 10)

def test_recipe_example_k4_uniform_y0_is_4():
    r = ordinal("o", "c", 4, 0, [3, 1, 0, 2])
    for perm in (None, [0, 1, 2, 3], [2, 0, 3, 1]):
        assert float(td.ord_term(r, torch.zeros(4), perm)) == pytest.approx(4.0, abs=1e-6)  # E = 1.5, (1.5 * 4/3)^2


def test_selftest_passes():
    assert td.a4_selftest()["ok"]


@pytest.mark.parametrize("k", [3, 4, 5])
def test_term_and_grad_match_hand_computation_shuffled(k):
    rng, g = random.Random(k), torch.Generator().manual_seed(k)
    for _ in range(20):
        r = ordinal("o", "c", k, rng.randrange(k), rng.sample(range(k), k))
        perm = rng.sample(range(k), k)
        z = (torch.randn(k, generator=g, dtype=torch.float64) * 2).requires_grad_(True)
        t = td.ord_term(r, z, perm)
        t.backward()
        ol = r["meta"]["option_level"]
        lev = [ol[r["options"][i]] for i in perm]
        th, gh, _ = td._ord_hand(lev, z.detach().tolist(), ol[r["gold"]])
        assert float(t.detach()) == pytest.approx(th, rel=1e-5, abs=1e-6)
        assert z.grad.tolist() == pytest.approx(gh, rel=1e-4, abs=1e-6)


def test_term_is_permutation_invariant_for_the_same_canonical_logits():
    """A view shows canonical option perm[j] at position j; with displayed logits z[perm] the term is the canonical one."""
    rng, g = random.Random(1), torch.Generator().manual_seed(1)
    for k in (2, 3, 5, 7):
        r = ordinal("o", "c", k, rng.randrange(k), rng.sample(range(k), k))
        z = torch.randn(k, generator=g) * 3
        ref = float(td.ord_term(r, z, None))
        for _ in range(5):
            p = rng.sample(range(k), k)
            assert float(td.ord_term(r, z[torch.tensor(p)], p)) == pytest.approx(ref, abs=1e-5)


def test_term_bounds_and_extremes():
    r = ordinal("o", "c", 5, 0)
    assert float(td.ord_term(r, torch.tensor([1e4, 0, 0, 0, 0.0]), None)) == pytest.approx(0.0, abs=1e-6)
    assert float(td.ord_term(r, torch.tensor([0, 0, 0, 0, 1e4]), None)) == pytest.approx(16.0, abs=1e-4)
    assert td.ord_finite_check([r, noul("n", "c")], [[4, 3, 2, 1, 0], [0, 1]], twins=[(0, [0, 1, 2, 3, 4])]) == \
        {"ordinal_views": 2, "evaluations": 12}
    with pytest.raises(FloatingPointError):
        td.ord_finite_check([r], probes=lambda k: [torch.full((k,), float("nan"))])


# ---------------------------------------------------------------- 2. compute_loss wiring

def _batch():
    rows = [ordinal("s1", "c1", 4, 1, [2, 0, 3, 1]), ordinal("s2", "c2", 3, 2, [1, 2, 0]),
            choice("k1", "c3", opts(4), "o2"), noul("n1", "c4", 1)]
    perms = [[3, 1, 0, 2], [2, 0, 1], [1, 0, 3, 2], [1, 0]]
    g = torch.Generator().manual_seed(3)
    lg = [torch.randn(len(p), generator=g).requires_grad_(True) for p in perms]
    return rows, perms, lg


@pytest.mark.parametrize("norm", [False, True])
def test_compute_loss_adds_ramped_ord_term(norm):
    rows, perms, lg = _batch()
    base = {"recipe": "A3", "lam": 1.0, "beta": 0.0}
    nm = {"rows": 8, "cons": 0, "comp": 0, "equiv": 0, "inv": 0, "twin": 1} if norm else None
    g2 = torch.Generator().manual_seed(9)
    l2 = torch.randn(4, generator=g2)
    twins = [(0, [0, 1, 2, 3], l2)]  # second view of s1
    for step, n_steps in [(0, 100), (10, 100), (50, 100)]:
        l0, t0, c0 = td.compute_loss(base, rows, perms, lg, {}, step, n_steps, "cpu", twins=twins, cyg=True, norm=nm)
        l1, t1, c1 = td.compute_loss({**base, "lam_ord": 1.0}, rows, perms, lg, {}, step, n_steps, "cpu", twins=twins,
                                     cyg=True, norm=nm)
        o1 = (td.ord_term(rows[0], lg[0], perms[0]) + td.ord_term(rows[0], l2, [0, 1, 2, 3])) / 2  # mean over views
        o2 = td.ord_term(rows[1], lg[1], perms[1])
        want = (o1 + o2) / (8 if norm else len(rows))  # normalised like the task CE (per batch row)
        ramp = min(1.0, step / (0.2 * n_steps))
        assert td.ORD_TERM not in t0 and "ord" not in c0
        assert float(t1["ord"]) == pytest.approx(float(want), rel=1e-6)
        assert float(l1) == pytest.approx(float(l0) + ramp * float(want), rel=1e-6, abs=1e-7)
        assert c1["ord"] == 2


def test_compute_loss_default_and_zero_are_identical():
    rows, perms, lg = _batch()
    base = {"recipe": "A3", "lam": 1.0, "beta": 0.0}
    a = td.compute_loss(base, rows, perms, lg, {}, 30, 100, "cpu", cyg=True)
    b = td.compute_loss({**base, "lam_ord": 0.0}, rows, perms, lg, {}, 30, 100, "cpu", cyg=True)
    assert torch.equal(a[0], b[0]) and list(a[1]) == list(b[1]) == list(td.TERMS) and a[2] == b[2]
    ga = torch.autograd.grad(a[0], lg, retain_graph=True)
    gb = torch.autograd.grad(b[0], lg)
    assert all(torch.equal(x, y) for x, y in zip(ga, gb))


def test_nan_in_ord_term_aborts():
    rows, perms, lg = _batch()
    lg[0] = torch.full((4,), float("nan"))
    with pytest.raises(FloatingPointError, match="'ord'"):
        td.compute_loss({"recipe": "A0", "lam": 1.0, "beta": 0.0, "lam_ord": 1.0, "label_smooth": 0.0},
                        rows[:2], perms[:2], lg[:2], {}, 50, 100, "cpu", cyg=True)


# ---------------------------------------------------------------- 3. row checks

@pytest.mark.parametrize("bad,match", [
    ({"option_level": {"lv0": 0, "lv1": 1, "lv2": 1}}, "not the levels"),
    ({"option_level": {"lv0": 0, "lv1": 1}}, "differ from the options"),
    ({"option_level": {"lv0": 0, "lv1": 1, "lv2": 2, "x": 3}}, "differ from the options"),
    ({"option_level": {"lv0": 0, "lv1": 1.0, "lv2": 2}}, "not the levels"),
    ({"option_level": {}}, "non-empty"),
])
def test_check_rows_refuses_bad_option_level(bad, match):
    r = ordinal("o", "c", 3, 1)
    r["meta"] = bad
    with pytest.raises(ValueError, match=match):
        td.check_rows([r])


def test_check_rows_refuses_option_level_on_yes_no():
    with pytest.raises(ValueError, match="ordinal rows are choice rows"):
        td.check_rows([noul("n", "c", meta={"option_level": {"Yes": 1, "No": 0}})])


def test_check_rows_accepts_ordinal_with_teacher():
    r = ordinal("o", "c", 3, 1, meta={"teacher": {"lv0": 0.1, "lv1": 0.8, "lv2": 0.1}, "teacher_src": "c1_anchor"})
    td.check_rows([r], kd=0.5)


# ---------------------------------------------------------------- 4. train(): config keys, count check, default off

def _write_ordinal_data(d: Path, n_ord: int = 30):
    _write_data(d)
    rows = [json.loads(x) for x in (d / "train.jsonl").read_text().splitlines()]
    rng = random.Random(5)
    for i in range(n_ord):
        k = 3 + i % 5
        rows.append(ordinal(f"s{i}", f"sc{i}", k, rng.randrange(k), rng.sample(range(k), k)))
    (d / "train.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    return rows


CFG = {"base": "fake", "grad_ckpt": False, "batch": 8, "epochs": 1.0, "beta": 0.1, "log_every": 1,
       "train_file": "train.jsonl", "rel_file": "rels.jsonl", "lam_inv": 1.0, "sym_cons": True, "perm_twin": 0.5,
       "ckpt_every_min": 0, "aux_norm": "batch"}


def _params(res):
    return {n: p.detach().clone() for n, p in res["model"].named_parameters()}


def _calls(res):
    return [(ids, pp) for ids, pp, g in res["model"].calls if g]


def test_off_is_bit_identical_with_ordinal_rows_and_count_check(fake_env, tmp_path, capsys):
    """lam_ord unset, lam_ord 0 with the count check on: same batches, permutations, twins, losses and weights."""
    rows = _write_ordinal_data(tmp_path)
    cfg = {**CFG, "epochs": _one_pass_epochs(tmp_path)}
    a = td.train(dict(cfg), tmp_path, tmp_path / "a", dev="cpu")
    out_a = capsys.readouterr().out
    n_file = sum(td.is_ordinal(r) for r in rows)
    n_drawn = td.ord_rows_drawn(*_units_steps(tmp_path, cfg["epochs"]), cyg=True)
    b = td.train({**cfg, "lam_ord": 0.0, "expect_ord_rows": n_file}, tmp_path, tmp_path / "b", dev="cpu")
    assert '"ordinal"' not in out_a and "ordinal" not in a["meta"] and "n_ord" not in a["meta"]["log"][0]
    assert [{k: v for k, v in r.items() if k not in ("min", "n_ord")} for r in a["meta"]["log"]] == \
           [{k: v for k, v in r.items() if k not in ("min", "n_ord")} for r in b["meta"]["log"]]
    assert _calls(a) == _calls(b)
    pa, pb = _params(a), _params(b)
    assert all(torch.equal(pa[k], pb[k]) for k in pa)
    assert b["meta"]["ordinal"]["rows_drawn"] == b["meta"]["ordinal"]["rows_drawn_planned"] == n_drawn > 0
    assert b["meta"]["ordinal"]["rows_in_file"] == b["meta"]["ordinal"]["expect_ord_rows"] == n_file
    assert sum(r["n_ord"] for r in b["meta"]["log"]) == n_drawn


def _one_pass_epochs(d: Path) -> float:
    """The epochs value of exactly one pass of train()'s data order (replay_steps.py, as the C config's epochs)."""
    import replay_steps as rs
    c = rs.stream_cfg({**CFG, "style": "cygnet"})
    rows_all, _, _, units, _ = rs.load_data({**c, "train_file": "train.jsonl", "rel_file": "rels.jsonl"}, d)
    return rs.epochs_for(rs.first_pass(units, c)["batches"], len(rows_all), CFG["batch"])


def _units_steps(d: Path, epochs: float = CFG["epochs"]):
    rows = td.read_jsonl(d / "train.jsonl")
    rels = td.read_jsonl(d / "rels.jsonl")
    units, _ = td.make_units(rows, rels)
    n_steps = math.ceil(len(rows) / CFG["batch"] * epochs)
    random.seed(20260925)  # train()'s default seed: the dry run starts from the same state as train()'s
    return units, CFG["batch"], n_steps


def test_lam_ord_trains_and_logs(fake_env, tmp_path):
    _write_ordinal_data(tmp_path)
    off = td.train(dict(CFG), tmp_path, tmp_path / "off", dev="cpu")
    on = td.train({**CFG, "lam_ord": 1.0}, tmp_path, tmp_path / "on", dev="cpu")
    assert _calls(off) == _calls(on)  # the term never changes the data order
    log = on["meta"]["log"]
    assert any(r["ord"] is not None for r in log) and all(r["ord"] is None or math.isfinite(r["ord"]) for r in log)
    assert all((r["ord"] is None) == (r["n_ord"] == 0) for r in log)
    assert not all(torch.equal(a, b) for a, b in zip(_params(off).values(), _params(on).values()))
    assert on["meta"]["ordinal"]["rows_drawn"] == sum(r["n_ord"] for r in log)


@pytest.mark.parametrize("delta,ok", [(0, True), (-1, False), (1, False), (-3, False)])
def test_expect_ord_rows_must_equal_the_file_count(fake_env, tmp_path, delta, ok):
    """Exact, like expect_kd_targets: one ordinal row more or less than the mixer counted fails before the model loads."""
    rows = _write_ordinal_data(tmp_path, n_ord=250)
    n_file = sum(td.is_ordinal(r) for r in rows)
    assert n_file == 250
    cfg = {**CFG, "epochs": _one_pass_epochs(tmp_path), "lam_ord": 1.0, "expect_ord_rows": n_file + delta,
           "stop_at_step": 1}
    if ok:
        assert td.train(cfg, tmp_path, tmp_path / "x", dev="cpu")["stopped"]
    else:
        with pytest.raises(ValueError, match="training file has 250 ordinal rows"):
            td.train(cfg, tmp_path, tmp_path / "x", dev="cpu")


def test_row_that_lost_option_level_fails_the_count(fake_env, tmp_path):
    """The case the exact count exists for: a mixer or augmentation bug strips meta.option_level from one row."""
    rows = _write_ordinal_data(tmp_path, n_ord=250)
    lost = next(r for r in rows if td.is_ordinal(r))
    lost["meta"] = {k: v for k, v in lost["meta"].items() if k != "option_level"}
    (tmp_path / "train.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    cfg = {**CFG, "epochs": _one_pass_epochs(tmp_path), "lam_ord": 1.0, "expect_ord_rows": 250, "stop_at_step": 1}
    with pytest.raises(ValueError, match="expected 250, the training file has 249"):
        td.train(cfg, tmp_path, tmp_path / "x", dev="cpu")


def test_draw_must_cover_the_file(fake_env, tmp_path):
    """The file count matches, but the planned steps draw 5% more ordinal rows than the file holds (epochs 1.0 here
    runs past one pass): the coverage check (+-1%, at least batch - 1 rows) fails before the model loads."""
    rows = _write_ordinal_data(tmp_path, n_ord=250)
    n_drawn = td.ord_rows_drawn(*_units_steps(tmp_path), cyg=True)
    assert n_drawn > 1.01 * 250
    with pytest.raises(ValueError, match=f"the run draws {n_drawn} ordinal rows, the file has 250"):
        td.train({**CFG, "lam_ord": 1.0, "expect_ord_rows": 250, "stop_at_step": 1}, tmp_path, tmp_path / "x", dev="cpu")


def test_check_ord_count_rule():
    td.check_ord_count(1000, 1000, 1000)
    td.check_ord_count(1000, 990, 1000)
    td.check_ord_count(1000, 1010, 1000)
    td.check_ord_count(1000, None, 1000)  # no dry run: only the exact file count is checked
    td.check_ord_count(0, 0, 0)
    td.check_ord_count(7, 0, None)  # expect_ord_rows unset: nothing is checked
    td.check_ord_count(250, 243, 250, tail=7)  # a one-pass run's trailing partial batch (batch 8) is allowed for
    td.check_ord_count(4350, 4307, 4350, tail=15)  # ... and at C's size the 1% bound (43.5 rows) is the larger
    for in_file, drawn, expect, tail, match in ((999, 999, 1000, 0, "file has 999"), (1001, 1001, 1000, 0, "file has 1001"),
                                                (1000, 989, 1000, 0, "draws 989"), (1000, 1011, 1000, 0, "draws 1011"),
                                                (1, 1, 0, 0, "file has 1"), (0, 1, 0, 0, "draws 1"),
                                                (250, 242, 250, 7, "draws 242"), (4350, 4306, 4350, 15, "draws 4306")):
        with pytest.raises(ValueError, match=match):
            td.check_ord_count(in_file, drawn, expect, tail=tail)


def test_dry_run_restores_random_state():
    units = [[ordinal(f"s{i}", f"c{i}", 3, 0)] for i in range(40)]
    random.seed(11)
    st = random.getstate()
    td.ord_rows_drawn(units, 8, 12, cyg=True)
    assert random.getstate() == st


@pytest.mark.parametrize("extra,match", [({"lam_ord": -0.1}, "lam_ord"), ({"lam_ord": float("nan")}, "lam_ord"),
                                         ({"lam_ord": "1"}, "lam_ord"), ({"expect_ord_rows": 2.5}, "expect_ord_rows"),
                                         ({"expect_ord_rows": -1}, "expect_ord_rows")])
def test_bad_ord_config_raises(fake_env, tmp_path, extra, match):
    _write_data(tmp_path)
    with pytest.raises(ValueError, match=match):
        td.train({**CFG, **extra}, tmp_path, tmp_path / "x", dev="cpu")


def test_keys_are_known_and_identity():
    assert "lam_ord" in td.KNOWN_KEYS and "expect_ord_rows" in td.KNOWN_KEYS
    assert "expect_ord_rows" in td.RUN_KEYS and "lam_ord" not in td.RUN_KEYS  # lam_ord is part of the run's identity
    assert "lam_ord" not in td.LOSS_DEFAULTS  # a C1 config's fingerprint and saved cfg stay as they were


def test_relay_with_lam_ord_is_bit_identical(fake_env, tmp_path):
    _write_ordinal_data(tmp_path)
    cfg = {**CFG, "epochs": 2.0, "lam_ord": 1.0}
    ref = td.train(cfg, tmp_path, tmp_path / "straight", dev="cpu")
    r1 = td.train({**cfg, "stop_at_step": 5}, tmp_path, tmp_path / "relay", dev="cpu")
    assert r1["stopped"]
    r2 = td.train(cfg, tmp_path, tmp_path / "relay", dev="cpu")
    pa, pb = _params(ref), _params(r2)
    assert all(torch.equal(pa[k], pb[k]) for k in pa)
    assert r2["meta"]["ordinal"]["rows_drawn"] == ref["meta"]["ordinal"]["rows_drawn"]


# ---------------------------------------------------------------- 5. F2: rendered prompt, fallback, thinking off

class TemplTok:
    """Minimal chat tokenizer: renders ChatML; refuses a system turn when system_ok is False."""

    def __init__(self, name, template, system_ok=True):
        self.name_or_path, self.chat_template, self.system_ok = name, template, system_ok
        self.seen = []

    def apply_chat_template(self, msgs, tokenize=False, add_generation_prompt=True, **kw):
        self.seen.append(kw)
        if not self.system_ok and msgs[0]["role"] == "system":
            raise ValueError("System role not supported")
        think = "<think>\n\n</think>\n\n" if kw.get("enable_thinking") is False else ""
        return "".join(f"<|im_start|>{m['role']}\n{m['content']}<|im_end|>\n" for m in msgs) + "<|im_start|>assistant\n" + think


Q35_TMPL = "{{ '<|im_start|>' }} {% if enable_thinking is defined %}{% endif %} <|vision_start|>"


def test_fallback_raises_for_qwen35_by_name_and_by_template():
    for tok in (TemplTok("Qwen/Qwen3.5-4B", "x", system_ok=False), TemplTok("/vol/models/q35_c", Q35_TMPL, system_ok=False)):
        assert decoder_io.is_qwen35(tok)
        with pytest.raises(RuntimeError, match="Qwen3.5"):
            decoder_io.render_chat(tok, "SYS", "USER")


def test_fallback_still_folds_for_templates_without_a_system_role():
    tok = TemplTok("google/gemma-2-2b-it", "{{ raise_exception('System role not supported') }}", system_ok=False)
    assert not decoder_io.is_qwen35(tok)
    assert decoder_io.render_chat(tok, "SYS", "USER") == "<|im_start|>user\nSYS\n\nUSER<|im_end|>\n<|im_start|>assistant\n"


def test_qwen35_always_renders_with_thinking_off():
    tok = TemplTok("Qwen/Qwen3.5-4B", "no switch named here")
    out = decoder_io.render_chat(tok, "SYS", "USER")
    assert tok.seen[-1] == {"enable_thinking": False} and out.endswith("<think>\n\n</think>\n\n")
    assert decoder_io.chat_kwargs(TemplTok("Qwen/Qwen3-4B-Instruct-2507", "<|im_start|>")) == {}
    assert decoder_io.SERVER_CHAT_TEMPLATE_KWARGS == {"enable_thinking": False}


def _old_prompt(tok, row, perm=None):
    """Readout.prompt before recipe v4 (train_decoder ebdf046d / decoder_io 8ba8ff4f), verbatim."""
    system = decoder_io.CYGNET_SYSTEM if decoder_io.STYLE == "cygnet" else decoder_io.SYSTEM
    msgs = [{"role": "system", "content": system}, {"role": "user", "content": decoder_io.user_msg(row, perm)}]
    kw = {"enable_thinking": False} if "enable_thinking" in (tok.chat_template or "") else {}
    try:
        return tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True, **kw)
    except Exception:
        msgs = [{"role": "user", "content": system + "\n\n" + decoder_io.user_msg(row, perm)}]
        return tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True, **kw)


def test_assert_prompt_identity_catches_a_layout_difference(monkeypatch):
    tok = TemplTok("Qwen/Qwen3.5-4B", Q35_TMPL)
    same = {"tok": tok, "layout": "schema_branch_mark", "style": "cygnet"}
    rep = decoder_io.assert_prompt_identity({"train": same, "gate": dict(same), "serve": dict(same)})
    assert len(rep["train"]["sha"]) == 6 and rep["train"]["sha"] == rep["serve"]["sha"]
    with pytest.raises(RuntimeError, match="F2"):
        decoder_io.assert_prompt_identity({"train": same, "gate": {**same, "layout": "text_first"}})
    other = TemplTok("Qwen/Qwen3.5-4B", Q35_TMPL + " changed")
    other.apply_chat_template = lambda msgs, **kw: TemplTok.apply_chat_template(other, msgs, **kw) + " "
    with pytest.raises(RuntimeError, match="F2"):
        decoder_io.assert_prompt_identity({"train": same, "serve": {**same, "tok": other}})


def test_prompt_texts_is_the_cand_logits_text():
    tok = TemplTok("Qwen/Qwen3.5-4B", Q35_TMPL)
    ro = decoder_io.Readout.__new__(decoder_io.Readout)
    ro.tok = tok
    rows = [dict(decoder_io.F2_ROWS[0]), {**decoder_io.F2_ROWS[1], "_prompt": "PREBUILT"}]
    assert decoder_io.prompt_texts(ro, rows, [[3, 2, 1, 0], None]) == [ro.prompt(rows[0], [3, 2, 1, 0]), "PREBUILT"]


Q35_SNAP = Path.home() / ".cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
C1_ADAPTER = Path(os.environ.get("OD_C1_ADAPTER", "/Users/aryamahadik/Documents/jev/backups/modal_models/q35_4b_main500k"))


@pytest.fixture
def q35_tok(monkeypatch):
    if not (Q35_SNAP / "tokenizer_config.json").exists():
        pytest.skip("Qwen3.5-4B tokenizer not in the local Hugging Face cache")
    monkeypatch.setenv("HF_HUB_OFFLINE", "1")
    from transformers import AutoTokenizer
    return AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", revision=Q35_SNAP.name)


@pytest.mark.parametrize("style", ["cygnet", "od"])
@pytest.mark.parametrize("layout", ["text_first", "schema_first", "schema_first_mark", "schema_branch_mark"])
def test_real_qwen35_prompt_unchanged_and_thinking_off(q35_tok, monkeypatch, style, layout):
    monkeypatch.setattr(decoder_io, "STYLE", style)
    monkeypatch.setattr(decoder_io, "LAYOUT", layout)
    assert decoder_io.is_qwen35(q35_tok)
    ro = decoder_io.Readout.__new__(decoder_io.Readout)
    ro.tok = q35_tok
    vr, vp = decoder_io.f2_views()
    for r, p in zip(vr, vp):
        new = ro.prompt(r, p)
        assert new == _old_prompt(q35_tok, r, p)  # byte-identical to the C1 renderer
        assert new.startswith("<|im_start|>system\n") and new.endswith("<|im_start|>assistant\n<think>\n\n</think>\n\n")


def test_real_f2_preflight_train_gate_serve(q35_tok, monkeypatch):
    if not (C1_ADAPTER / "train_meta.json").exists():
        pytest.skip("no local copy of the C1 adapter (set OD_C1_ADAPTER)")
    monkeypatch.setenv("HF_HUB_OFFLINE", "1")
    cfg = json.loads((Path(__file__).resolve().parents[1] / "runs/q35_4b_main.json").read_text())
    before = (decoder_io.LAYOUT, decoder_io.STYLE)
    rep = td.f2_preflight(cfg, C1_ADAPTER)
    assert (decoder_io.LAYOUT, decoder_io.STYLE) == before  # the module's prompt settings are restored
    assert set(rep) == {"train", "gate_serve"}  # od_gcp.py predict and di_engine / serve_tunnel: one load call
    assert rep["train"]["sha"] == rep["gate_serve"]["sha"]
    assert all(v["qwen35"] and v["chat_kwargs"] == {"enable_thinking": False} for v in rep.values())
    assert rep["train"]["layout"] == "schema_branch_mark" and rep["train"]["style"] == "cygnet"
    rec = td.f2_record(rep, "test")
    assert len(rec["sha"]) == 6 and set(rec["paths"]) == {"train", "gate_serve"}
    c_cfg = json.loads((Path(__file__).resolve().parents[1] / "runs/q35_4b_c_r1.json").read_text())
    rec_c = td.f2_record(td.f2_preflight(c_cfg), "train path only, C draft config")  # what the Modal smoke records
    assert td.f2_compare({"c1": rec, "c": rec_c})["f2_cross"] == "pass"


def _f2_rec(where, tok=None, layout="schema_branch_mark", style="cygnet"):
    tok = tok or TemplTok("Qwen/Qwen3.5-4B", Q35_TMPL)
    rep = decoder_io.assert_prompt_identity({"train": {"tok": tok, "layout": layout, "style": style, "src": "t"}})
    return td.f2_record(rep, where)


def test_f2_record_and_cross_machine_compare():
    a, b = _f2_rec("modal"), _f2_rec("l4")
    assert a["where"] == "modal" and len(a["sha"]) == 6 and a["views"] == list(a["sha"])
    assert {"python", "host", "transformers", "tokenizers", "jinja2"} <= set(a["env"])
    out = td.f2_compare({"ref": a, "l4": b})
    assert out["f2_cross"] == "pass" and out["sha"] == a["sha"] and out["reference"] == "ref"
    # another machine's renderer differs by one character: caught, with both software versions in the message
    other = TemplTok("Qwen/Qwen3.5-4B", Q35_TMPL)
    other.apply_chat_template = lambda msgs, **kw: TemplTok.apply_chat_template(other, msgs, **kw).replace("\n", " \n", 1)
    c = _f2_rec("l4", tok=other)
    c["env"]["transformers"] = "9.9.9"
    with pytest.raises(RuntimeError, match="F2 cross-machine.*9.9.9"):
        td.f2_compare({"ref": a, "l4": c})
    with pytest.raises(RuntimeError, match="F2 cross-machine"):  # a layout difference on one machine
        td.f2_compare({"ref": a, "l4": _f2_rec("l4", layout="text_first")})
    bad = json.loads(json.dumps(b))
    bad["paths"]["train"]["chat_kwargs"] = {}
    with pytest.raises(RuntimeError, match="enable_thinking"):
        td.f2_compare({"ref": a, "l4": bad})
    with pytest.raises(RuntimeError, match="6 views"):
        td.f2_compare({"ref": a, "l4": {**b, "sha": {}}})
    with pytest.raises(ValueError):
        td.f2_compare({"ref": a})


def test_f2_cli_writes_and_compares_records(tmp_path):
    """`train_decoder.py f2cmp` on saved records (what the GO step runs on the Modal and L4 records)."""
    import subprocess
    lean = Path(__file__).resolve().parents[1]
    a = _f2_rec("modal")
    (tmp_path / "a.json").write_text(json.dumps(a))
    (tmp_path / "b.json").write_text(json.dumps({**a, "where": "l4"}))
    (tmp_path / "c.json").write_text(json.dumps({**a, "where": "l4", "sha": {**a["sha"], a["views"][0]: "0" * 64}}))
    run = lambda *f: subprocess.run([sys.executable, str(lean / "train_decoder.py"), "f2cmp", *map(str, f)],
                                    capture_output=True, text=True, cwd=lean)
    ok = run(tmp_path / "a.json", tmp_path / "b.json")
    assert ok.returncode == 0 and json.loads(ok.stdout)["f2_cross"] == "pass"
    bad = run(tmp_path / "a.json", tmp_path / "c.json")
    assert bad.returncode != 0 and "F2 cross-machine" in bad.stderr
