"""fastcore: the SPEED-1 HF fast-path core for C1 (hosting/SPEED1_DESIGN.md). Library only: no Modal, no network.

  readout  API v1 parsing, decoder_io-identical prompts / candidate groups / token caps, 2view combine -> answers
  graphs   FastGraphs: pre-tokenized batches -> fp32 candidate logits; SPEED-1 graph plan (one shared pool, largest
           first, self-check + private-pool fallback), A0's legacy shapes and rules, eager path = decoder_io's
  batcher  BatchingEngine: one GPU worker, opportunistic length-bucketed batching, runtime flags, per-request timing
  fp8      RowwiseFP8Linear + quantize_model (arm A3)
  engine   FastEngine: the API v1 decider the HTTP host calls (decide / set_flags / health / boot / close)

Tests (CPU, tiny random Qwen3.5 with the C1 tokenizer): ../.venv/bin/python -m pytest hosting/tests -k fastcore
"""
from .readout import (API_VERSION, MAX_QUESTIONS, TEMPS, RequestError, WorkItem, build_items, combine, parse_v1,  # noqa: F401
                      prepare_items, request_from_row, tokenize_items)
from .batcher import (ARM_FLAGS, FLAG_DEFAULTS, BatchingEngine, BatchResult, EngineClosed, is_cuda_fatal,  # noqa: F401
                      plan_batches)
from .graphs import (FastGraphs, LADDER, NEW_COVERAGE, boot_shapes, legacy_shapes, memory_estimate,  # noqa: F401
                     select_legacy, select_new)
from .engine import FastEngine, load_merged  # noqa: F401,E402
