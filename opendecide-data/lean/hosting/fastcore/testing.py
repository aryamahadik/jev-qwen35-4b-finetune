"""fastcore.testing: shared CPU fixtures for hosting/tests/test_fastcore_*.py (no GPU, no network, no protected files).

  c1_tokenizer()  the C1 tokenizer from the local adapter backup, with decoder_io's LAYOUT/STYLE set from its
                  train_meta.json (schema_branch_mark / cygnet), as decoder_io.load would set them
  readout()       ONE full decoder_io.Readout for the process (vocabulary scan: two-letter labels after Z)
  tiny_model()    a random Qwen3.5 hybrid text model (linear_attention + full_attention layers), vocab = len(tok)
  dev_rows()      rows of the 9 gate dev splits (gate_dev.SPLITS; a split named ohs* is refused before any open)
"""
from __future__ import annotations

import functools
import json
from pathlib import Path

from .readout import dio

LEAN = Path(__file__).resolve().parents[2]
ADAPTER = LEAN.parent.parent / "backups" / "modal_models" / "q35_4b_main500k"  # tokenizer + train_meta only
BASE = "Qwen/Qwen3.5-4B"
SPLITS = "dev_nc,taskbank_dev,hard_dev,dev_negwords,dev_claims,pg_dev,devzs,devp_card,dev".split(",")  # gate_dev.SPLITS


@functools.lru_cache(maxsize=1)
def c1_tokenizer():
    info = dio.resolve_prompt([str(ADAPTER)], BASE, None, None, None)
    dio.LAYOUT, dio.STYLE = info["layout"], info["style"]
    return dio.load_tokenizer(BASE, adapter=str(ADAPTER), revision=info["revision"])


@functools.lru_cache(maxsize=1)
def readout():
    return dio.Readout(c1_tokenizer())


def tiny_config(vocab: int, pad_id: int, layers=("linear_attention", "full_attention", "linear_attention", "full_attention"),
                hidden: int = 64):
    from transformers import Qwen3_5TextConfig
    return Qwen3_5TextConfig(vocab_size=vocab, hidden_size=hidden, intermediate_size=2 * hidden, num_hidden_layers=len(layers),
                             layer_types=list(layers), num_attention_heads=4, num_key_value_heads=2, head_dim=16,
                             linear_num_key_heads=2, linear_num_value_heads=4, linear_key_head_dim=16,
                             linear_value_head_dim=16, linear_conv_kernel_dim=4, max_position_embeddings=32768,
                             tie_word_embeddings=False, pad_token_id=pad_id)


def tiny_model(seed: int = 0, dtype=None, **kw):
    import torch
    from transformers import Qwen3_5ForCausalLM
    tok = c1_tokenizer()
    torch.manual_seed(seed)
    m = Qwen3_5ForCausalLM(tiny_config(len(tok), tok.pad_token_id, **kw)).eval()
    with torch.no_grad():  # spread the random head so readouts are not all near-uniform
        m.lm_head.weight.mul_(20.0)
    return m.to(dtype) if dtype is not None else m


def dev_rows(splits=SPLITS) -> list:
    out = []
    for sp in splits:
        if sp.startswith("ohs"):
            raise SystemExit(f"dev splits only ({sp} refused)")
        with open(LEAN / "data" / f"{sp}.jsonl") as f:
            out += [{**json.loads(x), "_split": sp} for x in f if x.strip()]
    return out
