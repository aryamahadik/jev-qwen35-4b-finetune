"""families/T32: commitment ledger in chat (kept / broken / not yet due / not triggered / waived). Code only before
A38.

  G0_SPEC.md      the frozen one-page G0-lite spec (sha256 in plugin.T32.G0_SHA256)
  plugin.py       sampling, solver A (event-sourced state machine), rendering, relations, error models
  solver_b.py     the independent parser + solver B (sqlite queries + one SQL CASE; refuses invariant breaks)
  vocab.py        stand-in value sets (task phrases, events, topics; pure data): unit tests and the authoring rounds
  packs_v2.py     the 30 frozen Haiku packs both solvers read (sha checked), skin settings, register weights (F7)
  fixtures.py     in-memory stand-ins for Haiku message forms / skins / wordings / attack notes (tests only)
  test_plugin.py  in-memory tests (no file is written)
  test_pilot_fixes.py  tests of the Stage B pilot fixes F1-F8 (iteration 1, G0 v3)
  run_pilot_i1.py rerun of the pilot into pilot_i1/ (and the two-hash-seed determinism check); pilot/ stays as the record
"""
