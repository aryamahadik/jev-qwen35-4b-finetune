"""G-block wave 2 builders (PREREG_FINAL Ruling A40 b): one module per task type W1-W7.

  W1 w1_injection   prompt-injection detection (system prompt + user message)        gold: construction (Haiku pieces)
  W2 w2_pii         PII presence by type in real G-block texts                       gold: program (synthetic insert)
  W3 w3_rag         RAG faithfulness (real passage + question + answer)              gold: construction (Haiku pieces)
  W4 w4_offtopic    off-topic vs a stated assistant scope                            gold: construction (Haiku pieces)
  W5 w5_relevance   search relevance (real document + graded query)                  gold: construction (Haiku pieces)
  W6 w6_commit      Conventional Commits type (real permissive-repo commits)         gold: program (stripped prefix)
  W7 w7_tools       tool routing over a catalog, with abstain (no_tool)              gold: construction (Haiku pieces)

Shared code (paths, the never-open and A38 write guards, the decoder_io render check, the row schema, G-block text
pools) is in common.py; the Haiku authoring tasks are written by make_tasks.py. Every builder writes
candidates/<T>.jsonl and candidates/<T>_stats.json; no builder sets, edits or chooses a label beyond recording the
program result or the label slot the authoring brief asked for.
"""
