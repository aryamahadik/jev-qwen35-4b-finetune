"""Shared CPU fixtures for the think/ tests: tiny fake tokenizer, fake decoder_io, scripted fake engine."""
import re
import sys
import types
from pathlib import Path

import pytest

THINK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(THINK))
sys.path.insert(0, str(THINK.parent))


class FakeTok:
    """Word-level stand-in: every whitespace-split piece is one 'token'; A..Z encode to one id each."""
    pad_token_id, eos_token_id, pad_token = 0, 1, "<pad>"

    def apply_chat_template(self, msgs, tokenize=False, add_generation_prompt=True, enable_thinking=True):
        body = "".join(f"<|im_start|>{m['role']}\n{m['content']}<|im_end|>\n" for m in msgs)
        return body + "<|im_start|>assistant\n" + ("<think>\n" if enable_thinking else "<think>\n\n</think>\n\n")

    def encode(self, s, add_special_tokens=False):
        return [100 + ord(s)] if len(s) == 1 else [100 + ord(c) for c in s]

    def __len__(self):
        return 300


def fake_dio():
    """The decoder_io surface ThinkPath uses (SYSTEM, user_msg, Readout, LAYOUT, STYLE); options lettered A., B., ..."""
    d = types.SimpleNamespace(SYSTEM="SYS", LAYOUT=None, STYLE=None)

    def user_msg(row):
        head = f"TEXT:\n<<<\n{row['state']}\n>>>\n\nQUESTION: {row['instructions']}\n"
        if row["qtype"] == "noul":
            return head + "A. Yes\nB. No\n"
        return head + "".join(f"{chr(65 + i)}. {o}\n" for i, o in enumerate(row["options"]))

    d.user_msg = user_msg
    d.Readout = lambda tok: object()
    return d


class ScriptEngine:
    """Think: 'step ' words up to max_new_tokens (or `think_len`, then '</think>'). Answer (temperature 0): the
    scripted answer text for the item whose state appears in the prompt; cycles through a list per call."""

    def __init__(self, answers, think_len=50):
        self.answers, self.think_len, self.calls, self.seen = answers, think_len, [], {}

    def generate(self, prompts, params):
        self.calls.append((len(prompts), params[0].get("max_new_tokens")))
        out = []
        for p, sp in zip(prompts, params):
            if sp.get("temperature") == 0.0:
                key = next(k for k in self.answers if f"<<<\n{k}\n>>>" in p)
                seq = self.answers[key] if isinstance(self.answers[key], list) else [self.answers[key]]
                i = self.seen.get(key, 0)
                self.seen[key] = i + 1
                out.append({"text": seq[i % len(seq)], "tokens": 2, "finish": "length", "accept_len": None})
                continue
            n = min(sp["max_new_tokens"], self.think_len)
            text = "step " * n + ("</think>" if n == self.think_len else "")
            out.append({"text": text, "tokens": n, "finish": "stop", "accept_len": None})
        return out

    def letter_probs(self, prompts, ids_list):
        return [{ids[0]: 0.99} if ids else {} for ids in ids_list]


@pytest.fixture
def tok():
    return FakeTok()


@pytest.fixture
def dio():
    return fake_dio()


def mc_row(rid, state, options, gold, **kw):
    return {"id": rid, "qtype": "choice", "state": state, "instructions": "Pick one.", "options": options,
            "gold": gold, **kw}


def yn_row(rid, state, gold, **kw):
    return {"id": rid, "qtype": "noul", "state": state, "instructions": "Is it so?", "options": None, "gold": gold, **kw}
