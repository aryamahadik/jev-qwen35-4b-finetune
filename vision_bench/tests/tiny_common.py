"""Tiny random Qwen3.5 composite model (same architecture family/versions as the real one) for CPU checks of the harness."""
import copy, json, os, torch
import transformers
from transformers import AutoConfig

CONF = "/Users/aryamahadik/Documents/jev/vision_bench/src/qwen35-4b-config/config.json"

def tiny_config():
    d = json.load(open(CONF))
    t = d["text_config"]
    t.update(hidden_size=64, intermediate_size=128, num_hidden_layers=4, num_attention_heads=4, num_key_value_heads=2,
             linear_key_head_dim=32, linear_num_key_heads=2, linear_num_value_heads=4, linear_value_head_dim=32,
             vocab_size=400, layer_types=["linear_attention"] * 3 + ["full_attention"], mtp_num_hidden_layers=0,
             eos_token_id=1, max_position_embeddings=4096)
    v = d["vision_config"]
    v.update(depth=2, hidden_size=64, num_heads=4, intermediate_size=128, out_hidden_size=64)
    d.update(image_token_id=5, video_token_id=6, vision_start_token_id=3, vision_end_token_id=4)
    d.pop("transformers_version", None)
    cfg = transformers.Qwen3_5Config(**d)
    return cfg
