"""CPU tests for the labelling / eval side of FINETUNE_PLAN.md: C6 (layout from train_meta, jevbench cygnet prompt,
modal_od soup_eval / multi_eval), C7 (per-row permutations in predict), C8 (tta_choice / tta_noul), C9 (od_gcp relay),
C10 (save, sharded labels, pinned base commit), plus shard_golden.py, build_2b_kd.py and flag_labels.py on synthetic
fixtures. No model download, no GPU, no Modal call.

Run:  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python -m pytest -q tests/test_labelling.py
"""
from __future__ import annotations

import ast
import hashlib
import json
import random
import sys
import types
import zlib
from pathlib import Path
from types import SimpleNamespace

import pytest
import torch

LEAN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LEAN))
import build_2b_kd  # noqa: E402
import decoder_io  # noqa: E402
import flag_labels  # noqa: E402
import jevbench_od  # noqa: E402
import od_gcp  # noqa: E402
import shard_golden as sg  # noqa: E402


@pytest.fixture(autouse=True)
def _restore_globals(monkeypatch):
    """Every test starts from the module defaults and leaves them as they were."""
    monkeypatch.setattr(decoder_io, "LAYOUT", "text_first")
    monkeypatch.setattr(decoder_io, "STYLE", "cygnet")
    monkeypatch.setattr(decoder_io, "LOAD_INFO", {})
    monkeypatch.setattr(decoder_io, "_SET_BY", {})


# ---------------------------------------------------------------- synthetic rows

def noul(rid, gold=1, source="gd_x", meta=None, role="aff", state="The office opens at nine."):
    return {"id": rid, "call_id": "c_" + rid, "source": source, "state": state, "qtype": "noul", "options": None,
            "instructions": "Is it open at nine?", "gold": gold, "role": role, "meta": dict(meta or {})}


def choice(rid, options, gold, source="gd_y", meta=None, role="choice", state="Pick one."):
    return {"id": rid, "call_id": "c_" + rid, "source": source, "state": state, "qtype": "choice", "options": list(options),
            "instructions": "Which one?", "gold": gold, "role": role, "meta": dict(meta or {})}


def write_jsonl(path, rows):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("".join(json.dumps(r) + "\n" for r in rows))


def adapter_dir(tmp_path, name="ad", **cfg):
    d = tmp_path / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "train_meta.json").write_text(json.dumps({"cfg": cfg, "steps": 1}))
    return d


# ================================================================ C6: layout / style / base / revision from train_meta

def test_resolve_prompt_reads_train_meta(tmp_path):
    d = adapter_dir(tmp_path, base="Qwen/Qwen3.5-4B", layout="schema_branch_mark", style="cygnet", base_revision="abc")
    info = decoder_io.resolve_prompt([d], "Qwen/Qwen3.5-4B")
    assert (info["layout"], info["style"], info["revision"], info["forced"]) == ("schema_branch_mark", "cygnet", "abc", [])
    same = decoder_io.resolve_prompt([d], "Qwen/Qwen3.5-4B", layout="schema_branch_mark", style="cygnet", revision="abc")
    assert same["forced"] == [] and same["layout"] == "schema_branch_mark"


def test_resolve_prompt_default_layout_is_text_first(tmp_path):
    d = adapter_dir(tmp_path, base="B", style="cygnet")  # trained before the layout key existed
    assert decoder_io.resolve_prompt([d], "B")["layout"] == "text_first"
    d2 = adapter_dir(tmp_path, "nostyle", base="B")  # no style saved: the caller's STYLE stays
    assert decoder_io.resolve_prompt([d2], "B")["style"] is None


@pytest.mark.parametrize("key,kw", [("layout", {"layout": "text_first"}), ("style", {"style": "od"}),
                                    ("revision", {"revision": "zzz"})])
def test_resolve_prompt_conflict_raises_unless_forced(tmp_path, key, kw):
    d = adapter_dir(tmp_path, base="B", layout="schema_branch_mark", style="cygnet", base_revision="abc")
    with pytest.raises(ValueError, match=key):
        decoder_io.resolve_prompt([d], "B", **kw)
    info = decoder_io.resolve_prompt([d], "B", force=True, **kw)
    assert info[key] == kw[key]
    assert info["forced"] == [{"key": key, "saved": {"layout": "schema_branch_mark", "style": "cygnet",
                                                     "revision": "abc"}[key], "used": kw[key]}]


def test_resolve_prompt_base_mismatch(tmp_path):
    d = adapter_dir(tmp_path, base="Qwen/Qwen3.5-2B", layout="schema_branch_mark")
    with pytest.raises(ValueError, match="base"):
        decoder_io.resolve_prompt([d], "Qwen/Qwen3.5-4B")
    info = decoder_io.resolve_prompt([d], "Qwen/Qwen3.5-4B", force=True)
    assert info["base"] == "Qwen/Qwen3.5-4B" and info["forced"][0]["key"] == "base"


def test_resolve_prompt_missing_meta(tmp_path):
    d = tmp_path / "bare"
    d.mkdir()
    with pytest.raises(FileNotFoundError):
        decoder_io.resolve_prompt([d], "B")
    info = decoder_io.resolve_prompt([d], "B", layout="schema_branch_mark")
    assert info["layout"] == "schema_branch_mark" and info["saved_in"] == {str(d): None}
    assert decoder_io.resolve_prompt([], "B") == {"adapters": [], "layout": None, "style": None, "base": "B",
                                                  "revision": None, "saved": {}, "saved_in": {}, "forced": []}


def test_resolve_prompt_snapshot_and_blend(tmp_path):
    s = tmp_path / "snap"
    s.mkdir()
    (s / "snap.json").write_text(json.dumps({"step": 2500, "cfg": {"base": "B", "layout": "schema_branch_mark"}}))
    assert decoder_io.resolve_prompt([s], "B")["layout"] == "schema_branch_mark"
    a = adapter_dir(tmp_path, "a", base="B", layout="schema_branch_mark", style="cygnet")
    b = adapter_dir(tmp_path, "b", base="B", layout="text_first", style="cygnet")
    c = adapter_dir(tmp_path, "c", base="B", layout="schema_branch_mark", style="cygnet")
    assert decoder_io.resolve_prompt([a, c], "B")["layout"] == "schema_branch_mark"
    with pytest.raises(ValueError, match="disagree"):
        decoder_io.resolve_prompt([a, b], "B")
    forced = decoder_io.resolve_prompt([a, b], "B", layout="text_first", force=True)
    assert forced["layout"] == "text_first" and forced["forced"][0]["key"] == "layout"


class _FakeHFTok:
    chat_template = "a template"
    eos_token = "<eos>"

    def __init__(self):
        self.pad_token = None


class _FakeLM(torch.nn.Module):
    def to(self, dev):
        return self


@pytest.fixture
def fake_hf(monkeypatch):
    calls = {"tok": [], "model": []}

    class AutoTokenizer:
        @staticmethod
        def from_pretrained(src, **kw):
            calls["tok"].append((str(src), kw))
            return _FakeHFTok()

    class AutoModelForCausalLM:
        @staticmethod
        def from_pretrained(src, **kw):
            calls["model"].append((src, kw))
            return _FakeLM()

    tf = types.ModuleType("transformers")
    tf.AutoTokenizer, tf.AutoModelForCausalLM = AutoTokenizer, AutoModelForCausalLM
    peft = types.ModuleType("peft")
    peft.PeftModel = SimpleNamespace(from_pretrained=lambda model, adapter: model)
    monkeypatch.setitem(sys.modules, "transformers", tf)
    monkeypatch.setitem(sys.modules, "peft", peft)
    return calls


def test_load_sets_layout_style_revision_from_train_meta(tmp_path, fake_hf, capsys):
    d = adapter_dir(tmp_path, base="Qwen/Qwen3.5-4B", layout="schema_branch_mark", style="cygnet", base_revision="r1")
    decoder_io.STYLE = "od"
    model, tok, info = decoder_io.load("Qwen/Qwen3.5-4B", "cpu", adapter=str(d), return_info=True)
    assert (decoder_io.LAYOUT, decoder_io.STYLE) == ("schema_branch_mark", "cygnet")
    assert fake_hf["model"][-1][1]["revision"] == "r1"
    # no tokenizer files in the adapter: the base's tokenizer at the pinned commit (a checkpoint adapter copy)
    assert fake_hf["tok"][-1] == ("Qwen/Qwen3.5-4B", {"revision": "r1"})
    assert info is decoder_io.LOAD_INFO and info["layout"] == "schema_branch_mark" and info["prism_x"] is False
    assert info["chat_template_sha"] == hashlib.sha256(b"a template").hexdigest()
    assert '"layout": ["text_first", "schema_branch_mark"]' in capsys.readouterr().out
    assert len(decoder_io.load("Qwen/Qwen3.5-4B", "cpu", adapter=str(d))) == 2  # default return is unchanged
    (d / "tokenizer_config.json").write_text("{}")  # a saved adapter with its own tokenizer uses it, as before
    decoder_io.load("Qwen/Qwen3.5-4B", "cpu", adapter=str(d))
    assert fake_hf["tok"][-1] == (str(d), {})


def test_load_base_only_keeps_globals(fake_hf):
    decoder_io.LAYOUT, decoder_io.STYLE = "schema_first", "od"
    decoder_io.load("Qwen/Qwen3.5-2B", "cpu")
    assert (decoder_io.LAYOUT, decoder_io.STYLE) == ("schema_first", "od")
    assert fake_hf["model"][-1][1] == {"dtype": torch.bfloat16, "attn_implementation": "sdpa"}  # no revision key
    decoder_io.load("Qwen/Qwen3.5-2B", "cpu", revision="r9", layout="schema_branch_mark")
    assert decoder_io.LAYOUT == "schema_branch_mark" and fake_hf["model"][-1][1]["revision"] == "r9"
    assert fake_hf["tok"][-1] == ("Qwen/Qwen3.5-2B", {"revision": "r9"})


def test_base_load_after_adapter_warns_but_keeps_layout(tmp_path, fake_hf, capsys):
    d = adapter_dir(tmp_path, base="B", layout="schema_branch_mark", style="cygnet")
    decoder_io.load("B", "cpu", adapter=str(d))
    capsys.readouterr()
    decoder_io.load("B", "cpu")
    assert decoder_io.LAYOUT == "schema_branch_mark" and "earlier adapter" in capsys.readouterr().out
    decoder_io.load("B", "cpu", layout="text_first")
    assert decoder_io.LAYOUT == "text_first" and "earlier adapter" not in capsys.readouterr().out


def test_load_conflicts(tmp_path, fake_hf):
    d = adapter_dir(tmp_path, base="Qwen/Qwen3.5-2B", layout="schema_branch_mark", style="cygnet")
    with pytest.raises(ValueError):
        decoder_io.load("Qwen/Qwen3.5-4B", "cpu", adapter=str(d))  # the base it was not trained on
    with pytest.raises(ValueError):
        decoder_io.load("Qwen/Qwen3.5-2B", "cpu", adapter=str(d), layout="text_first")
    _, _, info = decoder_io.load("Qwen/Qwen3.5-2B", "cpu", adapter=str(d), layout="text_first", force=True,
                                 return_info=True)
    assert decoder_io.LAYOUT == "text_first" and info["forced"] == [{"key": "layout", "saved": "schema_branch_mark",
                                                                     "used": "text_first"}]
    bare = tmp_path / "bare"
    bare.mkdir()
    with pytest.raises(FileNotFoundError):
        decoder_io.load("Qwen/Qwen3.5-2B", "cpu", adapter=str(bare))


def test_load_prism_x_json_must_agree(tmp_path, fake_hf, monkeypatch):
    import prism_x

    def fake_maybe_load(model, adapter, dev):
        decoder_io.LAYOUT, decoder_io.STYLE = "schema_branch_mark", "cygnet"
        return {"params": 1, "cfg": {}}
    monkeypatch.setattr(prism_x, "maybe_load", fake_maybe_load)
    ok = adapter_dir(tmp_path, "ok", base="B", layout="schema_branch_mark", style="cygnet")
    decoder_io.load("B", "cpu", adapter=str(ok))
    assert decoder_io.LOAD_INFO["prism_x"] is True
    bad = adapter_dir(tmp_path, "bad", base="B", layout="text_first", style="cygnet")
    with pytest.raises(RuntimeError, match="prism_x.json"):
        decoder_io.load("B", "cpu", adapter=str(bad))


# ---------------------------------------------------------------- jevbench_od fmt="cygnet" follows LAYOUT

def old_letter_row(task, tok, fmt):
    """Frozen copy of jevbench_od.letter_row before C6 (hard-coded text-first cygnet prompt)."""
    LET, CYGNET_SYSTEM, state_text = jevbench_od.LET, jevbench_od.CYGNET_SYSTEM, jevbench_od.state_text
    q = task.question
    qt, crit, instr = q["type"], q.get("criteria"), q["instructions"]
    if qt == "score":
        items = [(str(i), v) for i, v in enumerate(crit)]
    else:
        items = list((crit or {}).items()) if isinstance(crit, dict) else []
        if qt == "noul" and not items:
            items = [("true", "yes, this holds"), ("false", "no, this does not hold")]
    keys = [k for k, _ in items]
    yes_index = next((i for i, k in enumerate(keys) if str(k).lower() == "true"), None) if qt == "noul" else None
    st = state_text(task.state)
    if fmt == "cygnet":
        lines = [st.rstrip(), "", instr.rstrip(), "", "Options:"] + [f"{LET[i]}. {d or k}" for i, (k, d) in enumerate(items)]
        lines += ["", "Answer with the letter of exactly one option, and nothing else:"]
        msgs = [{"role": "system", "content": CYGNET_SYSTEM}, {"role": "user", "content": "\n".join(lines)}]
        kw = {"enable_thinking": False} if "enable_thinking" in (tok.chat_template or "") else {}
        try:
            text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True, **kw)
        except Exception:
            msgs = [{"role": "user", "content": CYGNET_SYSTEM + "\n\n" + "\n".join(lines)}]
            text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True, **kw)
        row = {"state": st, "instructions": instr, "qtype": "choice", "options": [str(d or k) for k, d in items], "_prompt": text}
    else:
        opts = [f"{k}: {d}" if d and str(d).strip() and str(d).strip() != str(k) else str(k) for k, d in items]
        row = {"state": st, "instructions": instr, "qtype": "choice", "options": opts}
    return row, keys, yes_index


class ChatTok:
    chat_template = "... enable_thinking ..."

    def apply_chat_template(self, msgs, tokenize=False, add_generation_prompt=True, **kw):
        return "".join(f"<|{m['role']}|>{m['content']}<|end|>" for m in msgs) + f"<|gen={add_generation_prompt}|{sorted(kw.items())}>"


class NoSystemTok(ChatTok):
    chat_template = "plain"

    def apply_chat_template(self, msgs, **kw):
        if any(m["role"] == "system" for m in msgs):
            raise ValueError("no system role")
        return super().apply_chat_template(msgs, **kw)


JB_TASKS = [
    SimpleNamespace(state="The shop opens at 9.  \n", question={"type": "noul", "instructions": "Is it open at 10? ",
                                                                 "criteria": {"true": "it is open", "false": ""}}),
    SimpleNamespace(state={"a": 1, "b": [2, 3]}, question={"type": "noul", "instructions": "Holds?", "criteria": None}),
    SimpleNamespace(state="Refund request.", question={"type": "choice", "instructions": "Route it.",
                                                       "criteria": {"billing": "money issues", "tech": "", "other": None}}),
    SimpleNamespace(state="Rate this.", question={"type": "score", "instructions": "How good?",
                                                  "criteria": ["bad", "ok", "good"]}),
]


@pytest.mark.parametrize("tok", [ChatTok(), NoSystemTok()])
@pytest.mark.parametrize("fmt", ["cygnet", "inline"])
def test_jevbench_letter_row_text_first_parity(tok, fmt):
    for t in JB_TASKS:
        assert jevbench_od.letter_row(t, tok, fmt) == old_letter_row(t, tok, fmt)


def test_jevbench_cygnet_follows_layout():
    decoder_io.LAYOUT = "schema_branch_mark"
    row, keys, yes = jevbench_od.letter_row(JB_TASKS[2], ChatTok(), "cygnet")
    msg = decoder_io.cygnet_msg({k: v for k, v in row.items() if k != "_prompt"})
    assert decoder_io.UNTRUSTED[0] in row["_prompt"] and msg in row["_prompt"]
    assert row["_prompt"] != old_letter_row(JB_TASKS[2], ChatTok(), "cygnet")[0]["_prompt"]
    assert keys == ["billing", "tech", "other"] and yes is None


# ================================================================ C7 / C8: predict with perms and per-type TTA

class _M:
    def eval(self):
        return self


def _score(rid, opt):
    return (zlib.crc32(f"{rid}|{opt}".encode()) % 1000) / 250.0


def fake_cand_factory(bias=0.0, calls=None):
    """Logits from the DISPLAYED option texts, plus an optional position bias (bias * position, a letter bias)."""
    def fake(model, ro, rows, dev, perms=None):
        if calls is not None:
            calls.append(([r["id"] for r in rows], None if perms is None else [None if p is None else list(p) for p in perms]))
        out = []
        for r, p in zip(rows, perms or [None] * len(rows)):
            lr = decoder_io.as_letter_row(r)
            if lr["qtype"] == "noul":  # od style: fixed Yes/No readout, no letters
                shown = ["Yes", "No"]
            else:
                shown = lr["options"] if p is None else [lr["options"][i] for i in p]
            out.append(torch.tensor([_score(r["id"], o) + bias * k for k, o in enumerate(shown)], dtype=torch.float32))
        return out
    return fake


def pred_rows():
    rs = [noul(f"n{i}", gold=i % 2, state="x" * (i * 7)) for i in range(7)]
    rs += [choice(f"c{i}", [f"opt{j}" for j in range(2 + i % 5)], "opt1", state="y" * (i * 5)) for i in range(9)]
    rs += [choice("wide", [f"w{j}" for j in range(30)], "w3")]
    return rs


def old_predict(model, tok, rows, batch_size=16, dev="cuda", tta=False, token_budget=12000, tta_noul=False):
    """Frozen copy of decoder_io.predict before C7/C8 (it calls the module's Readout / cand_logits / to_probs)."""
    Readout, cand_logits, to_probs, STYLE = decoder_io.Readout, decoder_io.cand_logits, decoder_io.to_probs, decoder_io.STYLE
    model.eval()
    ro = Readout(tok)
    order = sorted(range(len(rows)), key=lambda i: len(rows[i]["state"]) + 20 * len(rows[i]["options"] or []))
    preds = [None] * len(rows)
    est = lambda i: (len(rows[i]["state"]) + len(rows[i].get("card") or "") + 400) / 3.2  # noqa: E731
    batches, cur = [], []
    for i in order:
        if cur and (len(cur) >= batch_size or (len(cur) + 1) * est(i) > token_budget):
            batches.append(cur)
            cur = []
        cur.append(i)
    if cur:
        batches.append(cur)
    for idx in batches:
        batch = [rows[i] for i in idx]
        lg = cand_logits(model, ro, batch, dev)
        for j, i in enumerate(idx):
            preds[i] = to_probs(rows[i], lg[j])
        if tta:
            ch = [(j, i) for j, i in enumerate(idx) if rows[i]["qtype"] == "choice"]
            if ch:
                perms = [list(range(len(rows[i]["options"])))[::-1] for _, i in ch]
                lg2 = cand_logits(model, ro, [rows[i] for _, i in ch], dev, perms=perms)
                for (j, i), p, l2 in zip(ch, perms, lg2):
                    p2 = to_probs(rows[i], l2, p)
                    preds[i] = {o: (preds[i][o] + p2[o]) / 2 for o in rows[i]["options"]}
            yn = [(j, i) for j, i in enumerate(idx) if rows[i]["qtype"] == "noul" and STYLE == "cygnet" and tta_noul]
            if yn:
                lg2 = cand_logits(model, ro, [rows[i] for _, i in yn], dev, perms=[[1, 0]] * len(yn))
                for (j, i), l2 in zip(yn, lg2):
                    p2 = to_probs(rows[i], l2, [1, 0])
                    preds[i] = {k: (preds[i][k] + p2[k]) / 2 for k in ("yes", "no")}
    return preds


@pytest.fixture
def fake_predict_env(monkeypatch):
    monkeypatch.setattr(decoder_io, "Readout", lambda tok: None)
    calls = []
    monkeypatch.setattr(decoder_io, "cand_logits", fake_cand_factory(bias=0.4, calls=calls))
    return calls


def _dump(p):
    return json.dumps(p)  # exact floats and key order


@pytest.mark.parametrize("style", ["cygnet", "od"])
@pytest.mark.parametrize("tta,tta_noul", [(False, False), (True, False), (True, True), (False, True)])
def test_predict_default_matches_old(fake_predict_env, style, tta, tta_noul):
    decoder_io.STYLE = style
    rs = pred_rows()
    new = decoder_io.predict(_M(), None, rs, batch_size=4, tta=tta, tta_noul=tta_noul)
    old = old_predict(_M(), None, rs, batch_size=4, tta=tta, tta_noul=tta_noul)
    assert _dump(new) == _dump(old)


@pytest.mark.parametrize("style", ["cygnet", "od"])
@pytest.mark.parametrize("tta", [False, True])
def test_identity_perms_equal_none(fake_predict_env, style, tta):
    decoder_io.STYLE = style
    rs = pred_rows()
    ident = [list(range(len(r["options"]))) if r["qtype"] == "choice" else ([0, 1] if style == "cygnet" else None)
             for r in rs]
    a = decoder_io.predict(_M(), None, rs, batch_size=4, tta=tta, tta_noul=tta)
    b = decoder_io.predict(_M(), None, rs, batch_size=4, tta=tta, tta_noul=tta, perms=ident)
    assert _dump(a) == _dump(b)


@pytest.mark.parametrize("style", ["cygnet", "od"])
def test_random_perms_map_back_to_options(monkeypatch, style):
    """Without a position bias the per-option probabilities cannot depend on the view: a mapping bug would move
    probability to the wrong option (about 1/n agreement)."""
    decoder_io.STYLE = style
    monkeypatch.setattr(decoder_io, "Readout", lambda tok: None)
    calls = []
    monkeypatch.setattr(decoder_io, "cand_logits", fake_cand_factory(bias=0.0, calls=calls))
    rs = pred_rows()
    perms = decoder_io.view_perms(rs, 7)
    assert any(p is not None and p != sorted(p) for p in perms)
    ref = decoder_io.predict(_M(), None, rs)
    got = decoder_io.predict(_M(), None, rs, perms=perms)
    for r, x, y in zip(rs, ref, got):
        assert list(y) == list(x)  # keyed by the original options, in the original order
        assert all(abs(x[k] - y[k]) < 1e-6 for k in x)
    seen = {rid: p for ids, ps in calls[len(calls) // 2:] for rid, p in zip(ids, ps)}  # the perms that reached cand_logits
    assert all(seen[r["id"]] == perms[i] for i, r in enumerate(rs))
    calls.clear()
    tta = decoder_io.predict(_M(), None, rs, perms=perms, tta_choice=True, tta_noul=True)
    assert all(abs(x[k] - y[k]) < 1e-6 for x, y in zip(ref, tta) for k in x)
    want = {r["id"]: perms[i] for i, r in enumerate(rs)}
    reads = {}
    for ids, ps in calls:
        for rid, p in zip(ids, ps):
            reads.setdefault(rid, []).append(p)
    for r in rs:  # the second read is the reversed (choice) / swapped (yes/no) version of the row's own view
        if r["qtype"] == "choice" or style == "cygnet":
            assert reads[r["id"]] == [want[r["id"]], want[r["id"]][::-1]]
        else:
            assert reads[r["id"]] == [None]


def test_perms_change_reads_under_letter_bias(fake_predict_env):
    """With a letter bias the view matters: a random view must NOT reproduce the given-order read."""
    rs = pred_rows()
    a = decoder_io.predict(_M(), None, rs)
    b = decoder_io.predict(_M(), None, rs, perms=decoder_io.view_perms(rs, 3))
    assert _dump(a) != _dump(b)


def test_view_perms_seeded():
    rs = pred_rows()
    p1 = decoder_io.view_perms(rs, 11)
    assert p1 == decoder_io.view_perms(list(reversed(rs)), 11)[::-1]  # independent of row order
    assert p1 != decoder_io.view_perms(rs, 12)
    r = rs[-1]
    rng = random.Random(int.from_bytes(hashlib.sha256(f"11:{r['id']}".encode()).digest()[:8], "big"))
    want = list(range(len(r["options"])))
    rng.shuffle(want)
    assert p1[-1] == want
    for r, p in zip(rs, p1):
        assert sorted(p) == list(range(len(r["options"]) if r["qtype"] == "choice" else 2))
    decoder_io.STYLE = "od"
    assert all(p is None for r, p in zip(rs, decoder_io.view_perms(rs, 11)) if r["qtype"] == "noul")


def test_view_perms_stable_across_processes():
    import subprocess
    code = ("import sys; sys.path.insert(0, %r); import decoder_io; decoder_io.STYLE = 'cygnet'; "
            "print(decoder_io.view_perms([{'id': 'r1', 'qtype': 'choice', 'options': list('abcdefg')}, "
            "{'id': 'r2', 'qtype': 'noul', 'options': None}], 5))") % str(LEAN)
    outs = {subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True).stdout
            for _ in range(2)}
    assert len(outs) == 1
    here = decoder_io.view_perms([{"id": "r1", "qtype": "choice", "options": list("abcdefg")},
                                  {"id": "r2", "qtype": "noul", "options": None}], 5)
    assert outs.pop().strip() == str(here)


def test_tta_flags_are_separate(fake_predict_env):
    calls = fake_predict_env
    rs = pred_rows()
    decoder_io.predict(_M(), None, rs, tta_choice=True, tta_noul=False)
    second = [ids for ids, ps in calls if ps is not None]
    assert second and all(i.startswith(("c", "w")) for ids in second for i in ids)
    calls.clear()
    decoder_io.predict(_M(), None, rs, tta_choice=False, tta_noul=True)
    second = [ids for ids, ps in calls if ps is not None]
    assert second and all(i.startswith("n") for ids in second for i in ids)
    legacy = decoder_io.predict(_M(), None, rs, tta=True, tta_noul=False)
    assert _dump(legacy) == _dump(decoder_io.predict(_M(), None, rs, tta_choice=True, tta_noul=False))
    both = decoder_io.predict(_M(), None, rs, tta=True, tta_noul=True)
    assert _dump(both) == _dump(decoder_io.predict(_M(), None, rs, tta_choice=True, tta_noul=True))
    with pytest.raises(ValueError):
        decoder_io.predict(_M(), None, rs, tta=True, tta_choice=True)
    with pytest.raises(ValueError):
        decoder_io.predict(_M(), None, rs, perms=[None])


def test_od_gcp_tta_kwargs():
    ns = lambda **k: SimpleNamespace(**{"tta": False, "tta_choice": False, "tta_noul": False, **k})  # noqa: E731
    assert od_gcp.tta_kwargs(ns()) == {"tta": False, "tta_noul": False}  # the old call, unchanged
    assert od_gcp.tta_kwargs(ns(tta=True)) == {"tta": True, "tta_noul": True}
    assert od_gcp.tta_kwargs(ns(tta_noul=True)) == {"tta_choice": False, "tta_noul": True}
    with pytest.raises(SystemExit):
        od_gcp.tta_kwargs(ns(tta=True, tta_choice=True))
    assert od_gcp.tta_meta({"tta": True, "tta_noul": True}) == {"tta": True, "tta_choice": True, "tta_noul": True}


# ================================================================ C9: od_gcp relay

def _modal_consts():
    tree = ast.parse((LEAN / "modal_od.py").read_text())
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id in ("RELAY_REQUIRED", "QWEN35_TARGETS"):
                out[node.targets[0].id] = ast.literal_eval(node.value)
    return out


def test_relay_constants_match_modal():
    m = _modal_consts()
    assert od_gcp.RELAY_REQUIRED == m["RELAY_REQUIRED"] and od_gcp.QWEN35_TARGETS == m["QWEN35_TARGETS"]


def relay_config(tmp_path, **over):
    cfg = {k: 1 for k in od_gcp.RELAY_REQUIRED}
    cfg.update(name="run1", base="Qwen/Qwen3.5-4B", style="cygnet", layout="schema_branch_mark", targets="QWEN35",
               base_revision="abc", **over)
    p = tmp_path / "runs" / "run1.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(cfg))
    return p


def test_relay_cfg(tmp_path):
    name, cfg = od_gcp.relay_cfg(relay_config(tmp_path), stop_at_step=7)
    assert name == "run1" and "name" not in cfg and cfg["targets"] == od_gcp.QWEN35_TARGETS
    assert (cfg["no_overwrite"], cfg["expect_resume"], cfg["allow_env_change"], cfg["stop_at_step"],
            cfg["stop_at_unix"]) == (True, True, True, 7, 0)
    _, cfg2 = od_gcp.relay_cfg(relay_config(tmp_path), stop_after_min=5)
    assert cfg2["stop_at_unix"] > 0
    p = relay_config(tmp_path)
    c = json.loads(p.read_text())
    del c["micro_tokens"]
    p.write_text(json.dumps(c))
    with pytest.raises(SystemExit, match="micro_tokens"):
        od_gcp.relay_cfg(p)


ENV = {"python": "3.12.1", "torch_cuda": "12.8", "cudnn": 91000, "torch": "2.14.0", "transformers": "5.0.0",
       "peft": "0.17.0", "gpu": "NVIDIA H100 80GB HBM3", "sm_count": 132}


def test_relay_env_diff():
    l4 = {**ENV, "gpu": "NVIDIA L4", "sm_count": 58, "python": "3.12.3", "cudnn": 90100, "torch_cuda": "13.0"}
    assert od_gcp.relay_env_diff(ENV, l4) == {}
    assert od_gcp.relay_env_diff(ENV, {**l4, "peft": "0.18.0"}) == {"peft": ["0.17.0", "0.18.0"]}
    assert od_gcp.relay_env_diff(ENV, {k: v for k, v in l4.items() if k != "transformers"}) == {
        "transformers": ["5.0.0", None]}


def _ckpt(tmp_path, name="run1", env=ENV, where="_ckpt"):
    d = tmp_path / "models" / name / where
    d.mkdir(parents=True, exist_ok=True)
    torch.save({"step": 3, "env": env}, d / "state.pt")
    return d


def test_check_relay_env(tmp_path):
    d = tmp_path / "models" / "run1" / "_ckpt"
    with pytest.raises(SystemExit, match="no checkpoint"):
        od_gcp.check_relay_env(d, ENV)
    _ckpt(tmp_path, where="_ckpt.old")  # stopped between the two renames: still found
    assert od_gcp.check_relay_env(d, {**ENV, "gpu": "NVIDIA L4"}) == {"gpu": ["NVIDIA H100 80GB HBM3", "NVIDIA L4"]}
    _ckpt(tmp_path)
    with pytest.raises(SystemExit, match="torch"):
        od_gcp.check_relay_env(d, {**ENV, "torch": "2.15.0"})


def test_cmd_relay(tmp_path, monkeypatch):
    import train_decoder
    monkeypatch.setattr(od_gcp, "HERE", tmp_path)
    monkeypatch.setattr(od_gcp, "MODELS", tmp_path / "models")
    monkeypatch.setattr(od_gcp, "DATA", tmp_path / "data")
    monkeypatch.setattr(train_decoder, "_env", lambda: {**ENV, "gpu": "NVIDIA L4", "sm_count": 58})
    seen = {}

    def fake_train(cfg, data_dir, out_dir, **kw):
        seen.update(cfg=cfg, data=data_dir, out=out_dir, style=decoder_io.STYLE)
        return {"stopped": True, "next_step": 9, "n_steps": 20, "meta": {"cfg": cfg}}
    monkeypatch.setattr(train_decoder, "train", fake_train)
    decoder_io.STYLE = "od"
    cfgp = relay_config(tmp_path)
    a = od_gcp.parser().parse_args(["relay", "--config", str(cfgp), "--stop-at-step", "9"])
    with pytest.raises(SystemExit, match="no checkpoint"):  # a missing checkpoint never starts at step 0
        od_gcp.cmd_relay(a)
    assert not seen
    _ckpt(tmp_path)
    res = od_gcp.cmd_relay(a)
    assert res["next_step"] == 9 and seen["style"] == "cygnet" and seen["out"] == tmp_path / "models" / "run1"
    assert seen["cfg"]["expect_resume"] and seen["cfg"]["no_overwrite"] and seen["cfg"]["allow_env_change"]
    assert (tmp_path / "logs" / "relay_run1_stopped_at_9.json").exists()
    monkeypatch.setattr(train_decoder, "_env", lambda: {**ENV, "numpy": "3.0"})
    seen.clear()
    with pytest.raises(SystemExit, match="numpy"):
        od_gcp.cmd_relay(a)
    assert not seen  # refused before training


# ================================================================ C10: save() and sharded labels

def test_save_mkdir_parents_and_meta_layout(tmp_path, monkeypatch):
    here = tmp_path / "deep" / "er"
    monkeypatch.setattr(od_gcp, "HERE", here)
    monkeypatch.setattr(od_gcp, "DATA", tmp_path / "data")
    write_jsonl(tmp_path / "data" / "dev_x.jsonl", [noul("a"), noul("b")])
    decoder_io.LAYOUT = "schema_branch_mark"
    od_gcp.save("m1", {"dev_x": [{"yes": 0.25, "no": 0.75}, {"yes": 1.0, "no": 0.0}]}, {"base": "B"})
    lines = (here / "preds_dev_x" / "m1.jsonl").read_text().splitlines()
    assert lines[0] == json.dumps({"id": "a", "model": "m1", "probs": {"yes": 0.25, "no": 0.75}})
    meta = json.loads((here / "preds_dev_x" / "m1.meta.json").read_text())
    assert meta == {"name": "m1", "rows": 2, "layout": "schema_branch_mark", "style": "cygnet", "base": "B"}


def golden_fixture():
    rows = [noul("y1", 1), noul("y2", 0), noul("att", 1, role="attacked"), choice("c1", ["a", "b", "c"], "b"),
            noul("b50", 1, meta={"teacher": {"yes": 0.9}, "teacher_src": "blend50"}),
            choice("gp", ["a", "b"], "a", meta={"gold_probs": {"a": 0.7, "b": 0.3}}),
            choice("r_84331130428f", ["x", "y", "x"], "y"), noul("lin", 1, state="seen in training"),
            noul("h1", 1, meta={"teacher": {"yes": 0.8}})]
    rels = [{"type": "inv", "a": "y1", "b": "att"}, {"type": "complement", "a": "y1", "b": "y2"}]
    lineage = {sg.row_key(noul("lin", 1, state="seen in training"))}
    return rows, rels, lineage


def test_select_rows_exclusions():
    rows, rels, lineage = golden_fixture()
    keep, first, total = sg.select_rows(rows, rels, lineage)
    assert [r["id"] for r in keep] == ["y1", "y2", "c1", "h1"]
    assert first == {"attacked_twin": 1, "blend50": 1, "gold_probs": 1, "csqa_dup_options": 1, "in_lineage": 1}
    assert sum(first.values()) + len(keep) == len(rows)


def test_lineage_keys_skip_missing(tmp_path):
    write_jsonl(tmp_path / "train_v11.jsonl", [noul("q", state="s1")])
    warned = []
    keys, seen = sg.lineage_keys(tmp_path, names=("train_v11", "train_v99"), warn=warned.append)
    assert keys == {sg.row_key(noul("q", state="s1"))} and seen == {"train_v11": 1, "train_v99": None}
    assert len(warned) == 1 and "train_v99" in warned[0]


def test_split_even():
    assert sg.split_even(422044, 22000) == [21103] * 4 + [21102] * 16
    assert sg.split_even(5, 2) == [2, 2, 1] and sg.split_even(0, 10) == [0]


def make_shards(tmp_path, n=23, shard_rows=10):
    rows = [noul(f"y{i}", i % 2) if i % 3 else choice(f"c{i}", ["p", "q", "r"], "q") for i in range(n)]
    sd = tmp_path / "shards"
    man = sg.write_shards(rows, sd, shard_rows, {"note": "test"})
    return rows, sd, man


def test_write_shards_and_manifest(tmp_path):
    rows, sd, man = make_shards(tmp_path)
    assert [s["rows"] for s in man["shards"]] == [8, 8, 7] and man["rows"] == 23
    files = sg.shard_files(sd)
    assert [p.name for p in files] == ["shard_000.jsonl", "shard_001.jsonl", "shard_002.jsonl"]
    assert [r["id"] for p in files for r in sg.read_jsonl(p)] == [r["id"] for r in rows]
    assert not list(sd.glob("*.tmp"))
    assert sg.write_shards(rows, sd, 10, {"note": "test"}) == man  # same set: nothing rewritten
    with pytest.raises(SystemExit):
        sg.write_shards(rows[:-1], sd, 10, {})  # a different set never replaces shards silently


@pytest.fixture
def fake_label_env(monkeypatch):
    calls = []

    def fake_predict(model, tok, rows, dev="cuda", perms=None, **kw):
        calls.append({"ids": [r["id"] for r in rows], "perms": perms, "kw": kw})
        return [{"yes": 0.25, "no": 0.75} if r["qtype"] == "noul" else {o: 1 / len(r["options"]) for o in r["options"]}
                for r in rows]
    monkeypatch.setattr(decoder_io, "predict", fake_predict)
    decoder_io.LAYOUT = "schema_branch_mark"
    return calls


SETTINGS = {"name": "t4b", "base": "B", "revision": None, "layout": "schema_branch_mark", "perm_seed": None,
            "tta": False, "tta_choice": False, "tta_noul": False, "merged": True}


def test_label_shards_resumable(tmp_path, fake_label_env):
    calls = fake_label_env
    rows, sd, _ = make_shards(tmp_path)
    out = sd / "labels_t4b"
    shards = sg.shard_files(sd)
    done = od_gcp.label_shards(None, None, shards, out, SETTINGS, {"tta": False, "tta_noul": False}, "cygnet")
    assert len(done) == 3 and len(calls) == 3 and calls[0]["kw"] == {"tta": False, "tta_noul": False}
    for s in shards:
        lp, mp = sg.label_paths(out, s)
        assert sg.shard_done(s, lp, mp)
        meta = json.loads(mp.read_text())
        assert meta["rows"] == len(sg.read_ids(s)) and meta["settings"] == SETTINGS and meta["style"] == "cygnet"
    assert not list(out.glob("*.tmp"))
    labels = sg.load_labels(out, sd)
    assert set(labels) == {r["id"] for r in rows}
    calls.clear()
    od_gcp.label_shards(None, None, shards, out, SETTINGS, {}, "cygnet")
    assert calls == []  # every shard done: nothing relabelled
    lp1, mp1 = sg.label_paths(out, shards[1])
    lp1.write_text("\n".join(lp1.read_text().splitlines()[:-1]) + "\n")  # truncated label file
    mp2 = sg.label_paths(out, shards[2])[1]
    mp2.unlink()  # crashed after the label file, before the meta
    assert not sg.shard_done(shards[1], lp1, mp1) and not sg.shard_done(shards[2], *sg.label_paths(out, shards[2]))
    with pytest.raises(RuntimeError, match="not labelled"):
        sg.load_labels(out, sd)
    od_gcp.label_shards(None, None, shards, out, SETTINGS, {}, "cygnet")
    assert [c["ids"][0] for c in calls] == [sg.read_ids(shards[1])[0], sg.read_ids(shards[2])[0]]
    assert all(sg.shard_done(s, *sg.label_paths(out, s)) for s in shards)


def test_label_shards_ids_must_match(tmp_path, fake_label_env):
    rows, sd, _ = make_shards(tmp_path)
    shards = sg.shard_files(sd)
    out = sd / "labels_t4b"
    od_gcp.label_shards(None, None, shards, out, SETTINGS, {}, "cygnet")
    lp, mp = sg.label_paths(out, shards[0])
    recs = sg.read_jsonl(lp)
    recs[0], recs[1] = recs[1], recs[0]  # same count, wrong order
    write_jsonl(lp, recs)
    assert not sg.shard_done(shards[0], lp, mp)


def test_label_shards_refuses_other_settings_and_layout(tmp_path, fake_label_env):
    rows, sd, _ = make_shards(tmp_path)
    shards = sg.shard_files(sd)
    out = sd / "labels_t4b"
    od_gcp.label_shards(None, None, shards[:1], out, SETTINGS, {}, "cygnet")
    with pytest.raises(SystemExit, match="other settings"):
        od_gcp.label_shards(None, None, shards, out, {**SETTINGS, "perm_seed": 3}, {}, "cygnet")
    decoder_io.LAYOUT = "text_first"
    with pytest.raises(RuntimeError, match="layout"):
        od_gcp.label_shards(None, None, shards, out, SETTINGS, {}, "cygnet")


def test_label_shards_crash_leaves_no_done_shard(tmp_path, fake_label_env, monkeypatch):
    rows, sd, _ = make_shards(tmp_path)
    shards = sg.shard_files(sd)
    out = sd / "labels_t4b"
    real = decoder_io.predict
    n = {"k": 0}

    def flaky(*args, **kw):
        n["k"] += 1
        if n["k"] == 2:
            raise KeyboardInterrupt("VM stopped")
        return real(*args, **kw)
    monkeypatch.setattr(decoder_io, "predict", flaky)
    with pytest.raises(KeyboardInterrupt):
        od_gcp.label_shards(None, None, shards, out, SETTINGS, {}, "cygnet")
    assert sg.shard_done(shards[0], *sg.label_paths(out, shards[0]))
    assert not any(p.exists() for p in sg.label_paths(out, shards[1]))
    od_gcp.label_shards(None, None, shards, out, SETTINGS, {}, "cygnet")
    assert all(sg.shard_done(s, *sg.label_paths(out, s)) for s in shards)


def test_label_shards_stale_meta_never_vouches(tmp_path, fake_label_env, monkeypatch):
    """Relabelling a broken shard deletes its old meta first: a crash between the new label file and the new meta must
    leave the shard 'not done', never 'done' under the old meta."""
    rows, sd, _ = make_shards(tmp_path)
    shards = sg.shard_files(sd)
    out = sd / "labels_t4b"
    od_gcp.label_shards(None, None, shards[:1], out, SETTINGS, {}, "cygnet")
    lp, mp = sg.label_paths(out, shards[0])
    lp.write_text(lp.read_text().splitlines()[0] + "\n")

    def boom(path, obj):
        raise OSError("disk full")
    monkeypatch.setattr(sg, "write_json_atomic", boom)
    with pytest.raises(OSError):
        od_gcp.label_shards(None, None, shards[:1], out, SETTINGS, {}, "cygnet")
    assert lp.exists() and not mp.exists() and not sg.shard_done(shards[0], lp, mp)


def test_label_shards_perm_seed_views(tmp_path, fake_label_env):
    calls = fake_label_env
    rows, sd, _ = make_shards(tmp_path)
    shards = sg.shard_files(sd)
    out = sd / "labels_view"
    od_gcp.label_shards(None, None, shards[:1], out, {**SETTINGS, "perm_seed": 5}, {}, "cygnet")
    rs = sg.read_jsonl(shards[0])
    assert calls[0]["perms"] == decoder_io.view_perms(rs, 5)
    assert [x["view"] for x in sg.read_jsonl(sg.label_paths(out, shards[0])[0])] == decoder_io.view_perms(rs, 5)


REV = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"


@pytest.fixture
def label_cli(tmp_path, fake_label_env, monkeypatch):
    """od_gcp label on 3 synthetic shards with a fake load; env["commit"] is the base commit the fake model reports."""
    rows, sd, _ = make_shards(tmp_path)
    env = {"loads": [], "commit": REV, "sd": sd, "out": sd / "labels_t4b", "models": tmp_path / "models",
           "argv": ["label", "--name", "t4b", "--base", "B", "--layout", "schema_branch_mark", "--shards-dir", str(sd)]}

    class FM:
        def __init__(self):
            self.config = SimpleNamespace(_commit_hash=env["commit"])

        def merge_and_unload(self):
            return self

        def eval(self):
            return self

    def fake_load(base, dev, adapter=None, revision=None, layout=None, style=None, force=False):
        env["loads"].append((base, adapter, revision, layout, style, force))
        decoder_io.LAYOUT = layout
        decoder_io.LOAD_INFO = {"layout": layout, "revision": revision}
        return FM(), None
    monkeypatch.setattr(decoder_io, "load", fake_load)
    monkeypatch.setattr(od_gcp, "gpu_info", lambda: {})
    monkeypatch.setattr(od_gcp, "MODELS", env["models"])
    monkeypatch.setenv("HF_HUB_OFFLINE", "")  # label sets it (offline is the default); restored after the test
    env["run"] = lambda *extra: od_gcp.cmd_label(od_gcp.parser().parse_args(env["argv"] + list(extra)))
    return env


def test_cmd_label(label_cli):
    run, loads, out = label_cli["run"], label_cli["loads"], label_cli["out"]
    run("--shard", "1", "--revision", REV)
    assert [p.name for p in sorted(out.glob("*.meta.json"))] == ["shard_001.meta.json"]
    assert loads == [("B", str(label_cli["models"] / "t4b"), REV, "schema_branch_mark", None, False)]
    run("--revision", REV)
    assert len(list(out.glob("*.meta.json"))) == 3 and len(loads) == 2
    run("--revision", REV)  # all done: the model is not even loaded
    assert len(loads) == 2
    with pytest.raises(SystemExit, match="other settings"):
        run("--revision", REV, "--perm-seed", "1")
    assert len(loads) == 2


def test_cmd_label_checks_every_shard_before_narrowing(label_cli):
    """A per-shard job (--shard i) with other settings is refused even though its own shard is not done: before, only
    shard i's meta was checked, so one label set could mix views (review item 7)."""
    run, loads, out = label_cli["run"], label_cli["loads"], label_cli["out"]
    run("--shard", "0", "--revision", REV, "--perm-seed", "5")
    with pytest.raises(SystemExit, match="other settings"):
        run("--shard", "1", "--revision", REV)  # the seed forgotten
    with pytest.raises(SystemExit, match="other settings"):
        run("--shard", "2", "--revision", REV, "--perm-seed", "5", "--no-merge")
    assert len(loads) == 1 and [p.name for p in out.glob("*.meta.json")] == ["shard_000.meta.json"]
    run("--shard", "1", "--revision", REV, "--perm-seed", "5")
    assert len(loads) == 2


def test_load_labels_refuses_mixed_settings(tmp_path, fake_label_env):
    rows, sd, _ = make_shards(tmp_path)
    shards = sg.shard_files(sd)
    out = sd / "labels_t4b"
    od_gcp.label_shards(None, None, shards[:1], out, SETTINGS, {}, "cygnet")
    labels, view = sg.load_labels(out, return_view=True)
    assert view == {"settings": SETTINGS, "style": "cygnet"} and len(labels) == len(sg.read_ids(shards[0]))
    od_gcp.label_shards(None, None, shards[1:], out, {**SETTINGS, "perm_seed": 5}, {}, "cygnet")  # each call alone passes
    with pytest.raises(RuntimeError, match="different settings"):
        sg.load_labels(out, sd)
    with pytest.raises(RuntimeError, match="different settings"):
        sg.load_labels(out)  # the glob branch too
    out2 = sd / "labels_style"
    od_gcp.label_shards(None, None, shards, out2, SETTINGS, {}, "cygnet")
    mp = sg.label_paths(out2, shards[2])[1]
    mp.write_text(json.dumps({**json.loads(mp.read_text()), "style": "od"}))
    with pytest.raises(RuntimeError, match="different settings"):
        sg.load_labels(out2, sd)
    mp.write_text(json.dumps({**json.loads(mp.read_text()), "style": "cygnet"}))
    labels, view = sg.load_labels(out2, sd, return_view=True)
    assert set(labels) == {r["id"] for r in rows} and view["settings"] == SETTINGS


def test_cmd_label_pins_the_base_commit(label_cli, monkeypatch):
    """label refuses to run without a 40-character base commit (4B-E's train_meta has none), binds it into the settings
    every done shard is checked against, is offline by default and records the commit the model reports (item 8)."""
    import os
    run, loads, out = label_cli["run"], label_cli["loads"], label_cli["out"]
    with pytest.raises(SystemExit, match="40-character"):
        run("--shard", "0")  # no --revision, no adapter train_meta
    with pytest.raises(SystemExit, match="40-character"):
        run("--shard", "0", "--revision", "851bf6e")  # a short hash is not an exact commit
    assert loads == []
    adapter_dir(label_cli["models"], "t4b", base="B", layout="schema_branch_mark", base_revision=REV)
    run("--shard", "0")  # the adapter's base_revision
    assert loads[-1][2] == REV and os.environ["HF_HUB_OFFLINE"] == "1"
    meta = json.loads(sg.label_paths(out, sg.shard_files(label_cli["sd"])[0])[1].read_text())
    assert meta["settings"]["revision"] == REV and meta["load"]["base_commit"] == REV
    other = "0" * 40
    with pytest.raises(SystemExit, match="other settings"):  # a restart on another base never continues the set
        run("--shard", "1", "--revision", other, "--force")
    label_cli["commit"] = other  # the cache or Hub gave another snapshot than asked for
    with pytest.raises(RuntimeError, match="base commit"):
        run("--shard", "1")
    assert not sg.label_paths(out, sg.shard_files(label_cli["sd"])[1])[1].exists()
    label_cli["commit"] = REV
    monkeypatch.setenv("HF_HUB_OFFLINE", "")
    run("--shard", "1", "--online")
    assert os.environ["HF_HUB_OFFLINE"] == ""


def test_regenerated_rows_are_relabelled(tmp_path, fake_label_env, capsys):
    """Rows regenerated under the same ids (new state/gold) change the shard set and make only their shard not done,
    so they get new labels instead of the old text's (review item 9)."""
    calls = fake_label_env
    rows, sd, _ = make_shards(tmp_path)
    shards = sg.shard_files(sd)
    out = sd / "labels_t4b"
    od_gcp.label_shards(None, None, shards, out, SETTINGS, {}, "cygnet")
    assert all(json.loads(sg.label_paths(out, s)[1].read_text())["shard_sha256"] == sg._sha_file(s) for s in shards)
    new = [dict(r) for r in rows]
    new[9] = {**new[9], "state": "The office opens at ten.", "gold": 0}  # same id, second shard
    with pytest.raises(SystemExit, match="different shard set"):
        sg.write_shards(new, sd, 10, {"note": "test"})
    capsys.readouterr()
    sg.write_shards(new, sd, 10, {"note": "test"}, overwrite=True)
    assert "wrote 3 shards" in capsys.readouterr().out
    assert [sg.shard_done(s, *sg.label_paths(out, s)) for s in shards] == [True, False, True]
    calls.clear()
    od_gcp.label_shards(None, None, shards, out, SETTINGS, {}, "cygnet")
    assert [c["ids"] for c in calls] == [sg.read_ids(shards[1])]
    mp = sg.label_paths(out, shards[0])[1]  # a meta without the hash (older label code) is not done either
    mp.write_text(json.dumps({k: v for k, v in json.loads(mp.read_text()).items() if k != "shard_sha256"}))
    assert not sg.shard_done(shards[0], *sg.label_paths(out, shards[0]))


def test_shard_golden_main_reports_unchanged_set(tmp_path, capsys):
    rows, rels, _ = golden_fixture()
    data = tmp_path / "data"
    write_jsonl(data / "v14_parts" / "golden_train.jsonl", rows)
    write_jsonl(data / "v14_parts" / "golden_relations.jsonl", rels)
    argv = ["--data-dir", str(data), "--out", str(tmp_path / "shards"), "--shard-rows", "3"]
    sg.main(argv)
    assert "wrote 2 shards" in capsys.readouterr().out
    sg.main(argv)
    out = capsys.readouterr().out
    assert "nothing written" in out and "wrote" not in out
    man = json.loads((tmp_path / "shards" / sg.MANIFEST).read_text())
    assert man["rows_sha256"] == hashlib.sha256(b"".join(p.read_bytes() for p in sg.shard_files(tmp_path / "shards"))).hexdigest()


# ================================================================ od_gcp predict / blend: snapshot names

class _FakePeft:
    """PEFT stand-in: from_pretrained / load_adapter / add_weighted_adapter / merge, recording the adapters."""

    def __init__(self, base=None):
        self.base, self.adapters, self.config = base, [], SimpleNamespace(_commit_hash=None)

    @classmethod
    def from_pretrained(cls, model, path, adapter_name="default"):
        m = cls(model)
        m.adapters.append((adapter_name, str(path)))
        return m

    def load_adapter(self, path, adapter_name="default"):
        self.adapters.append((adapter_name, str(path)))

    def add_weighted_adapter(self, names, weights, adapter_name, combination_type="svd"):
        self.adapters.append((adapter_name, list(weights)))

    def to(self, dev):
        return self

    def merge_and_unload(self, adapter_names=None):
        return self

    def set_adapter(self, name):
        pass

    def delete_adapter(self, name):
        pass

    def save_pretrained(self, path, selected_adapters=None):
        pass

    def eval(self):
        return self


@pytest.fixture
def gcp_env(tmp_path, monkeypatch):
    """od_gcp paths in tmp_path, one split dev_x, fake load / predict / GPU info / PEFT."""
    monkeypatch.setattr(od_gcp, "HERE", tmp_path)
    monkeypatch.setattr(od_gcp, "DATA", tmp_path / "data")
    monkeypatch.setattr(od_gcp, "MODELS", tmp_path / "models")
    monkeypatch.setattr(od_gcp, "gpu_info", lambda: {})
    write_jsonl(tmp_path / "data" / "dev_x.jsonl", [noul("a"), noul("b")])
    loads = []

    def fake_load(base, dev, adapter=None, revision=None, layout=None, style=None, force=False):
        loads.append(adapter)
        decoder_io.LAYOUT = layout or decoder_io.LAYOUT
        decoder_io.LOAD_INFO = {"layout": decoder_io.LAYOUT}
        return _FakePeft(), None
    monkeypatch.setattr(decoder_io, "load", fake_load)
    monkeypatch.setattr(decoder_io, "predict", lambda model, tok, rows, dev="cuda", **kw: [{"yes": 0.5, "no": 0.5}] * len(rows))
    peft = types.ModuleType("peft")
    peft.PeftModel = _FakePeft
    monkeypatch.setitem(sys.modules, "peft", peft)
    return loads


def test_predict_and_blend_flatten_snapshot_names(tmp_path, gcp_env):
    """--name run/snaps/s002500 (a snapshot) is scored and saved as one flat file (review item 11): before, save()
    opened preds_dev_x/run/snaps/s002500.jsonl and the scores were lost."""
    snap = "q35_4b_main500k/snaps/s002500"
    adapter_dir(tmp_path / "models" / "q35_4b_main500k" / "snaps", "s002500", base="B", layout="schema_branch_mark")
    od_gcp.cmd_predict(od_gcp.parser().parse_args(["predict", "--name", snap, "--base", "B", "--splits", "dev_x"]))
    assert gcp_env == [str(tmp_path / "models" / snap)]
    flat = "q35_4b_main500k__snaps__s002500"
    recs = sg.read_jsonl(tmp_path / "preds_dev_x" / f"{flat}.jsonl")
    assert [r["model"] for r in recs] == [flat, flat]
    assert json.loads((tmp_path / "preds_dev_x" / f"{flat}.meta.json").read_text())["name"] == flat
    adapter_dir(tmp_path / "models", "e", base="B", layout="schema_branch_mark")
    od_gcp.cmd_blend(od_gcp.parser().parse_args(["blend", "--name", "mix/s1", "--base", "B", "--adapters",
                                                 f"{snap},e", "--weights", "0.75,0.25", "--splits", "dev_x"]))
    meta = json.loads((tmp_path / "preds_dev_x" / "mix__s1.meta.json").read_text())
    assert meta["blend"] == {snap: 0.75, "e": 0.25} and meta["load"]["layout"] == "schema_branch_mark"
    assert od_gcp.out_name("plain", "_t") == "plain_t"


# ================================================================ modal_od.py soup_eval / multi_eval (C6)

@pytest.fixture
def modal_eval(tmp_path, fake_hf, monkeypatch):
    """modal_od with the real decoder_io.load on fake HF / PEFT; predict records the layout and style it read in."""
    pytest.importorskip("modal")
    import modal_od
    peft = types.ModuleType("peft")
    peft.PeftModel = _FakePeft
    monkeypatch.setitem(sys.modules, "peft", peft)
    seen = []

    def fake_predict(model, tok, rows, dev="cuda", **kw):
        seen.append((decoder_io.LAYOUT, decoder_io.STYLE))
        return [{"yes": 0.5, "no": 0.5}] * len(rows)
    monkeypatch.setattr(decoder_io, "predict", fake_predict)
    monkeypatch.setattr(modal_od, "_rows", lambda s: [noul("a"), noul("b")])
    monkeypatch.setattr(modal_od, "vol", SimpleNamespace(commit=lambda: None))
    monkeypatch.setattr(modal_od, "HERE", tmp_path)
    write_jsonl(tmp_path / "data" / "dev_x.jsonl", [noul("a"), noul("b")])
    return modal_od, seen


class _FakeModalFn:
    def __init__(self, res):
        self.res, self.calls = res, []

    def with_options(self, **kw):
        return self

    def remote(self, *a, **kw):
        self.calls.append((a, kw))
        return self.res


@pytest.mark.filterwarnings("ignore:.*executing locally:UserWarning")
def test_soup_eval_reads_the_adapters_layout(tmp_path, modal_eval, fake_hf, monkeypatch):
    """soup_eval attaches the adapters with PEFT (no resolve_prompt): it must still read them in their train_meta
    layout, on their pinned base, and record it (review item 6); before, a fresh container scored in text_first."""
    modal_od, seen = modal_eval
    cfgs = {"/vol/models/new": {"base": "B", "layout": "schema_branch_mark", "style": "cygnet", "base_revision": REV},
            "/vol/models/e": {"base": "B", "layout": "schema_branch_mark", "style": "cygnet"},
            "/vol/models/old": {"base": "B", "style": "cygnet"}}  # no layout key: trained in text_first
    monkeypatch.setattr(decoder_io, "adapter_cfg", lambda a: (cfgs[str(a)], "train_meta.json") if str(a) in cfgs else None)
    raw = modal_od.soup_eval_remote.local
    res = raw("B", "new", "e", [0.75, 0.5], ["dev_x"])
    assert seen == [("schema_branch_mark", "cygnet")] * 2 and fake_hf["model"][-1][1]["revision"] == REV
    assert list(res["preds"]) == ["soup75", "soup50"] and res["load"]["layout"] == "schema_branch_mark"
    assert res["load"]["revision"] == REV and res["load"]["adapters"] == ["/vol/models/new", "/vol/models/e"]
    with pytest.raises(ValueError, match="disagree"):
        raw("B", "new", "old", [0.5], ["dev_x"])
    fn = _FakeModalFn(res)
    monkeypatch.setattr(modal_od, "soup_eval_remote", fn)
    modal_od.soup_eval.info.raw_f(a="new", b="e", weights="0.75,0.5", base="B", splits="dev_x")
    meta = json.loads((tmp_path / "preds_dev_x" / "new_e_soup75.meta.json").read_text())
    assert (meta["layout"], meta["style"], meta["revision"]) == ("schema_branch_mark", "cygnet", REV)
    assert meta["load"]["adapters"] == ["/vol/models/new", "/vol/models/e"] and meta["blend"] == "soup75"


@pytest.mark.filterwarnings("ignore:.*executing locally:UserWarning")
def test_multi_eval_layout_per_spec(tmp_path, modal_eval, monkeypatch):
    """Each spec is read in its own layout whatever the spec order: an adapter in its train_meta's, a base-only spec in
    the requested one (default text_first); an explicit layout that conflicts with an adapter raises (item 10)."""
    modal_od, seen = modal_eval
    ad = adapter_dir(tmp_path, "new", base="B", layout="schema_branch_mark", style="cygnet", base_revision=REV)
    new, base = {"label": "new", "base": "B", "adapter": str(ad)}, {"label": "base", "base": "B", "adapter": ""}
    raw = modal_od.multi_eval_remote.local
    for specs in ([new, base], [base, new]):
        seen.clear()
        res = raw(specs, ["dev_x"])
        got = {sp["label"]: lay for sp, lay in zip(specs, seen)}
        assert got == {"new": ("schema_branch_mark", "cygnet"), "base": ("text_first", "cygnet")}
        assert res["new"]["_load"]["layout"] == "schema_branch_mark" and res["new"]["_load"]["revision"] == REV
        assert res["base"]["_load"]["layout"] == "text_first" and res["base"]["_load"]["revision"] is None
    seen.clear()
    raw([new, base], ["dev_x"], layout="schema_branch_mark")
    assert seen == [("schema_branch_mark", "cygnet")] * 2
    with pytest.raises(ValueError, match="layout"):
        raw([new], ["dev_x"], layout="text_first")
    res = raw([new, base], ["dev_x"])
    pd = tmp_path / "preds_dev_x"
    pd.mkdir()
    (pd / "base.meta.json").write_text(json.dumps({"name": "base", "tta": True, "layout": "schema_branch_mark",
                                                   "latency_l4": {"p50": 1}}))  # an earlier od_gcp predict
    fn = _FakeModalFn(res)
    monkeypatch.setattr(modal_od, "multi_eval_remote", fn)
    modal_od.multi_eval.info.raw_f(specs=f"new=B:{ad},base=B", splits="dev_x")
    assert fn.calls[0][1] == {"layout": ""}
    m_new = json.loads((pd / "new.meta.json").read_text())
    assert (m_new["layout"], m_new["style"], m_new["revision"]) == ("schema_branch_mark", "cygnet", REV)
    m_base = json.loads((pd / "base.meta.json").read_text())
    assert m_base["layout"] == "text_first" and "tta" not in m_base and m_base["latency_l4"] == {"p50": 1}
    assert "_load" not in json.dumps(sg.read_jsonl(pd / "new.jsonl"))


# ================================================================ build_2b_kd.py

def kd_fixture():
    rows = [
        noul("ya", 1), noul("yn", 0),  # a complement pair, both fresh
        noul("z1", 1), noul("z1_atk", 1, role="attacked"),  # teacher right -> copied
        noul("z2", 0), noul("z2_atk", 0, role="attacked"),  # teacher wrong -> deleted
        choice("c1", ["a", "b", "c"], "b"), choice("c1_atk", ["a", "b", "c"], "b", role="attacked",
                                                   meta={"teacher": {"a": 0.2, "b": 0.5, "c": 0.3}, "teacher_src": "blend50"}),
        choice("c2", ["a", "b"], "a"), choice("c2_atk", ["a", "b"], "a", role="attacked"),  # a tie -> wrong -> deleted
        noul("h1", 1, meta={"teacher": {"yes": 0.8}}), noul("h1_atk", 1, role="attacked"),  # human partner -> copied
        noul("b50", 1, meta={"teacher": {"yes": 0.9}, "teacher_src": "blend50"}),
        noul("b50_atk", 1, role="attacked"),  # partner had only a blend50 teacher -> none
        choice("gp", ["a", "b"], "a", meta={"gold_probs": {"a": 0.7, "b": 0.3}}),
        choice("r_84331130428f", ["x", "y", "x"], "y", meta={"teacher": {"x": 0.5, "y": 0.5}, "teacher_src": "blend50"}),
        noul("prob", 1, source="gd_gen2_probability", meta={"teacher": {"yes": 0.37}}),
    ]
    rels = [{"type": "complement", "a": "ya", "b": "yn"}] + [
        {"type": "inv", "a": a, "b": a + "_atk"} for a in ("z1", "z2", "c1", "c2", "h1", "b50")]
    labels = {"ya": {"yes": 0.7, "no": 0.3}, "yn": {"yes": 0.5, "no": 0.5}, "z1": {"yes": 0.6, "no": 0.4},
              "z2": {"yes": 0.55, "no": 0.45}, "c1": {"a": 0.1, "b": 0.7, "c": 0.2}, "c2": {"a": 0.5, "b": 0.5},
              "h1": {"yes": 0.2, "no": 0.8}, "prob": {"yes": 0.9, "no": 0.1}}
    return rows, rels, labels


def test_build_2b_kd_rules():
    rows, rels, labels = kd_fixture()
    before = json.dumps(rows)
    keep, _, _ = sg.select_rows(rows, rels, set())
    eligible = {r["id"] for r in keep}
    assert eligible == set(labels)
    new, n = build_2b_kd.build(rows, rels, labels, eligible)
    assert json.dumps(rows) == before  # the input rows are never modified
    by = {r["id"]: r["meta"] for r in new}
    assert [r["id"] for r in new] == [r["id"] for r in rows]
    # complement pair: t_a <- (0.7 + 1 - 0.5) / 2 = 0.6, t_b <- 0.4; the raw reads stay in teacher4b
    assert by["ya"]["teacher"]["yes"] == pytest.approx(0.6) and by["yn"]["teacher"]["yes"] == pytest.approx(0.4)
    assert by["ya"]["teacher4b"] == {"yes": 0.7} and by["ya"]["teacher_src"] == "q35_4b_E"
    assert by["z1_atk"]["teacher"] == {"yes": 0.6} and by["z1_atk"]["teacher_src"] == "q35_4b_E_clean_copy"
    assert "teacher" not in by["z2_atk"] and "teacher_src" not in by["z2_atk"]  # 0.55 >= 0.5 but gold is 0
    assert by["c1_atk"]["teacher"] == {"a": 0.1, "b": 0.7, "c": 0.2}  # the blend50 read on attacked text is gone
    assert by["c1_atk"]["teacher_src"] == "q35_4b_E_clean_copy" and "teacher4b" not in by["c1_atk"]
    assert "teacher" not in by["c2_atk"]  # tie counts as wrong
    assert by["h1"] == {"teacher": {"yes": 0.8}}  # human teacher unchanged; its 4B-E label is audit-only
    assert by["h1_atk"]["teacher"] == {"yes": 0.8} and by["h1_atk"]["teacher_src"] == "human_clean_copy"
    assert "teacher" not in by["b50"] and "teacher" not in by["b50_atk"]
    assert by["gp"] == {"gold_probs": {"a": 0.7, "b": 0.3}} and "teacher" not in by["r_84331130428f"]
    assert by["prob"] == {"teacher": {"yes": 0.37}}  # exact probability row unchanged
    assert n["kd_targets"] == sum(1 for m in by.values() if isinstance(m.get("teacher"), dict))
    assert n["kd_targets"] == 11 and n["complement_pairs_symmetrised"] == 1  # 6 fresh + 2 human + 3 twin copies
    assert n["twin_copied_fresh"] == 2 and n["twin_copied_human_or_exact"] == 1
    assert n["twin_partner_wrong_deleted"] == 2 and n["twin_no_partner_teacher"] == 1
    assert not any(m.get("teacher_src") == "blend50" for m in by.values())


def test_build_2b_kd_refuses_bad_labels():
    rows, rels, labels = kd_fixture()
    elig = set(labels)
    with pytest.raises(ValueError, match="must not be labelled"):
        build_2b_kd.build(rows, rels, {**labels, "z1_atk": {"yes": 0.1, "no": 0.9}}, elig)
    with pytest.raises(ValueError, match="no label"):
        build_2b_kd.build(rows, rels, {k: v for k, v in labels.items() if k != "c1"}, elig)
    with pytest.raises(ValueError, match="label keys"):
        build_2b_kd.build(rows, rels, {**labels, "c1": {"a": 0.5, "b": 0.5}}, elig)
    bad_rels = rels + [{"type": "complement", "a": "ya", "b": "z1"}]  # golds 1 + 1: not complementary
    with pytest.raises(ValueError):
        build_2b_kd.build(rows, bad_rels, labels, elig)


def test_build_2b_kd_validate():
    ok = [choice("c", ["a", "b"], "a", meta={"teacher": {"a": 0.4, "b": 0.6}})]
    build_2b_kd.validate(ok)
    for bad in ([choice("c", ["a", "b"], "a", meta={"teacher": {"a": 0.4, "b": 0.5}})],
                [choice("c", ["a", "b"], "a", meta={"teacher": {"a": 0.4, "z": 0.6}})],
                [choice("c", ["a", "a"], "a", meta={"teacher": {"a": 1.0}})],
                [noul("y", 1, meta={"teacher": {"yes": 1.2}})],
                [noul("y", 1, meta={"teacher": {"yes": 0.2}, "teacher_src": "blend50"})]):
        with pytest.raises(ValueError):
            build_2b_kd.validate(bad, ("blend50",))


def test_build_2b_kd_main(tmp_path, capsys):
    rows, rels, labels = kd_fixture()
    data = tmp_path / "data"
    write_jsonl(data / "v14_parts" / "golden_train.jsonl", rows)
    write_jsonl(data / "v14_parts" / "golden_relations.jsonl", rels)
    write_jsonl(tmp_path / "labels.jsonl", [{"id": k, "model": "t", "probs": v} for k, v in labels.items()])
    golden_bytes = (data / "v14_parts" / "golden_train.jsonl").read_bytes()
    argv = ["--labels", str(tmp_path / "labels.jsonl"), "--data-dir", str(data)]
    n = build_2b_kd.main(argv)
    out = data / "v14_parts" / "train_2b_golden_kd.jsonl"
    assert n["kd_targets"] == 11 and "kd targets: 11" in capsys.readouterr().out
    assert [r["id"] for r in sg.read_jsonl(out)] == [r["id"] for r in rows]
    assert (data / "v14_parts" / "golden_train.jsonl").read_bytes() == golden_bytes
    with pytest.raises(SystemExit, match="exists"):
        build_2b_kd.main(argv)
    with pytest.raises(SystemExit, match="new file"):
        build_2b_kd.main(argv + ["--out", "v14_parts/golden_train.jsonl", "--overwrite"])
    with pytest.raises(SystemExit, match="kd_skip_src"):
        build_2b_kd.main(argv + ["--overwrite", "--teacher-src", "blend50_x"])


# ================================================================ flag_labels.py

def flag_fixture(n=160):
    rng = random.Random(0)
    rows, labels = [], {}
    for i in range(n):  # group bad: the 4B reads the opposite of gold on 40% of rows; group ok: almost never
        for grp, wrong in (("gd_gen_bad", 0.4), ("gd_ok", 0.02)):
            r = noul(f"{grp}_{i}", i % 2, source=grp)
            rows.append(r)
            p_gold = 0.03 if rng.random() < wrong else 0.95
            labels[r["id"]] = {"yes": p_gold if r["gold"] == 1 else 1 - p_gold}
    for i in range(120):
        r = choice(f"ch_{i}", [f"o{j}" for j in range(6)], "o2", source="gd_choice")
        rows.append(r)
        p = [0.1] * 6
        p[2] = 0.5 if i % 10 else 0.0
        s = sum(p)
        labels[r["id"]] = {f"o{j}": p[j] / s for j in range(6)}
    hv = noul("human_v", 1, source="gd_votes", meta={"teacher": {"yes": 0.9}})
    rows.append(hv)
    labels[hv["id"]] = {"yes": 0.1}
    tw = noul("twin", 1, source="gd_ok", meta={"twin_of": "gd_ok_1"})
    rows.append(tw)
    labels["twin"] = {"yes": 0.0}
    return rows, labels


def test_flag_screen_and_groups():
    rows, labels = flag_fixture()
    recs, n_hard = flag_labels.screen(rows, labels, T=0.9)
    assert n_hard == 1 and "twin" not in {x["id"] for x in recs}  # designed-hard rows stay out of the bug hunt
    by = {x["id"]: x for x in recs}
    assert "vote_gap" in by["human_v"]["flags"] and "p_below" in by["human_v"]["flags"]
    lowest_ch = [x for x in recs if x["bucket"] == "5-9" and "lowest" in x["flags"]]
    assert len(lowest_ch) == 4 and all(x["p_gold"] == 0.0 for x in lowest_ch)  # ceil(3% of 120)
    cells, base = flag_labels.group_table(recs, min_n=100, excess=0.02)
    out = [c for c in cells if c["outlier"]]
    assert [c["group"] for c in out] == ["gd_gen_bad"] and out[0]["n"] == 160
    assert base["yn"] == pytest.approx(sum(bool(x["flags"]) for x in recs if x["bucket"] == "yn")
                                       / sum(x["bucket"] == "yn" for x in recs), abs=1e-4)
    sample = flag_labels.audit_sample(recs, cells, top=10, per_group=30, n_spread=20, n_human=5, seed=1)
    sets = [s for s, _ in sample]
    assert sets.count("top_group") == 30 and sets.count("flagged_spread") == 20
    assert all(x["group"] == "gd_gen_bad" for s, x in sample if s == "top_group")
    assert all(not flag_labels.is_generator(x["source"]) and not x["agree"] for s, x in sample if s == "human_disagree")
    ids = [x["id"] for _, x in sample]
    assert len(ids) == len(set(ids))
    assert [x["id"] for _, x in flag_labels.audit_sample(recs, cells, seed=1, n_spread=20, n_human=5)] == ids


def test_flag_temperature():
    assert flag_labels.temper(0.5, 0.65) == pytest.approx(0.5)
    assert flag_labels.temper(0.8, 1.0) == pytest.approx(0.8)
    assert flag_labels.temper(0.8, 0.5) > 0.8 and flag_labels.temper(0.2, 2.0) > 0.2


def test_flag_main(tmp_path):
    rows, labels = flag_fixture()
    rp, lp = tmp_path / "rows.jsonl", tmp_path / "labels.jsonl"
    write_jsonl(rp, rows)
    write_jsonl(lp, [{"id": k, "probs": v} for k, v in labels.items()])
    summary, sample = flag_labels.main(["--rows", str(rp), "--labels", str(lp), "--relations", "",
                                        "--out-dir", str(tmp_path / "audit"), "--n-spread", "10", "--n-human", "3"])
    assert summary["outliers"][0]["group"] == "gd_gen_bad"
    got = sg.read_jsonl(tmp_path / "audit" / "audit_rows.jsonl")
    assert len(got) == len(sample) and all("state" in x and "probs" in x for x in got)
    assert json.loads((tmp_path / "audit" / "flag_groups.json").read_text())["screened"] == summary["screened"]
