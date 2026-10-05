"""With the locally cached Qwen3.5-4B tokenizer (skipped when absent): the policy prompt is byte-identical to
think_rows.py's, and HFBackend works on a tiny random model and on a scripted stub model (CPU)."""
import json
from pathlib import Path

import pytest

torch = pytest.importorskip("torch")
LEAN = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def qtok():
    from transformers import AutoTokenizer
    import policies as P
    try:
        t = AutoTokenizer.from_pretrained(P.BASE, revision=P.REV, local_files_only=True)
    except Exception as e:  # noqa: BLE001
        pytest.skip(f"tokenizer not cached: {type(e).__name__}")
    t.padding_side = "left"
    return t


def test_prompt_identical_to_think_rows(qtok):
    import decoder_io as dio
    import think_engine as te
    rows = [json.loads(l) for l in open(LEAN / "data" / "dev_nc.jsonl")]
    wide = next(r for r in rows if r["qtype"] == "choice" and len(r["options"]) > 26)
    small = next(r for r in rows if r["qtype"] == "choice" and len(r["options"]) <= 9)
    tp = te.ThinkPath(te.FakeBackend(), qtok, dio)
    for row in (wide, small):
        row = {k: v for k, v in row.items() if k != "gold"}
        # think_rows.py, verbatim construction
        user = dio.user_msg(row)
        ref = qtok.apply_chat_template([{"role": "system", "content": dio.SYSTEM}, {"role": "user", "content": user}],
                                       tokenize=False, add_generation_prompt=True, enable_thinking=True)
        assert tp.prepare([{"id": row["id"], "row": row}])[0]["prompt"] == ref
    assert dio.LAYOUT == "schema_branch_mark" and dio.STYLE == "cygnet"


class StubModel(torch.nn.Module):
    """generate() appends a fixed continuation (then pads); forward() puts all mass on one token."""

    def __init__(self, cont_ids, pad, hot):
        super().__init__()
        self.w = torch.nn.Parameter(torch.zeros(1))
        self.cont, self.pad, self.hot = cont_ids, pad, hot

    def generate(self, input_ids, attention_mask=None, max_new_tokens=8, **kw):
        c = (self.cont + [self.pad] * max_new_tokens)[:max_new_tokens]
        return torch.cat([input_ids, torch.tensor([c] * input_ids.shape[0])], dim=1)

    def forward(self, input_ids, attention_mask=None):
        logits = torch.full((input_ids.shape[0], input_ids.shape[1], 300000), -50.0)
        logits[:, -1, self.hot] = 50.0
        return type("O", (), {"logits": logits})()


def test_hf_backend_stop_and_pad(qtok):
    from hf_backend import HFBackend
    cont = qtok.encode("step one</think>\n\nB more text", add_special_tokens=False)
    a_id = qtok.encode("A", add_special_tokens=False)[0]
    be = HFBackend(StubModel(cont, qtok.pad_token_id, a_id), qtok, seed=0)
    out = be.generate(["p1", "p two"], [{"temperature": 0.6, "top_p": 0.95, "top_k": 20, "max_new_tokens": 64,
                                         "stop": ["</think>"], "skip_special_tokens": False}] * 2)
    assert [o["text"] for o in out] == ["step one</think>"] * 2 and out[0]["finish"] == "stop"
    assert out[0]["tokens"] == len(qtok("step one</think>")["input_ids"])
    short = be.generate(["p"], [{"temperature": 0.0, "max_new_tokens": 2, "skip_special_tokens": True}])
    assert short[0]["finish"] == "length" and "<|endoftext|>" not in short[0]["text"]
    pr = be.letter_probs(["x"], [[a_id, a_id + 1]])
    assert pr[0][a_id] > 0.99


def test_hf_backend_tiny_random_model(qtok):
    from transformers import LlamaConfig, LlamaForCausalLM
    from hf_backend import HFBackend
    cfg = LlamaConfig(vocab_size=len(qtok), hidden_size=16, intermediate_size=32, num_hidden_layers=1,
                      num_attention_heads=2, num_key_value_heads=1, max_position_embeddings=256)
    torch.manual_seed(0)
    be = HFBackend(LlamaForCausalLM(cfg).eval(), qtok, seed=0, max_batch=2)
    outs = be.generate(["a b", "c", "d e f"], [{"temperature": 0.6, "top_k": 20, "top_p": 0.95, "max_new_tokens": 3,
                                               "stop": ["</think>"], "skip_special_tokens": False}] * 3)
    assert len(outs) == 3 and all(o["finish"] in ("stop", "length") for o in outs)
    pr = be.letter_probs(["a b", "c"], [[10, 11], [12]])
    assert set(pr[0]) == {10, 11} and 0 <= pr[1][12] <= 1
