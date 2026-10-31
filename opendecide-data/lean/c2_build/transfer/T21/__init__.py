"""transfer/T21: contract cross-references and carve-outs on synthetic contracts (C2_DATA_SPEC 2.2, 3.20; transfer dev
only, never trained; no CUAD heading or text).

  G0_SPEC.md     the frozen one-page G0-lite spec, v1.3 (sha256 in plugin.T21Plugin.G0_SHA256); G0_SPEC_v1.2.md is the
                 v1.2 the pools were frozen under, kept byte for byte
  plugin.py      skeleton-first sampling, solver A (recursive clause tree), rendering, relations, error models
  card.py        the rules card in two styles (full = the frozen card, short) and their placement (fix iteration 1)
  solver_b.py    the independent parser + solver B (effective claim-cell sets by set algebra); written from
                 G0_SPEC.md, imports nothing from plugin.py
  fixtures.py    in-memory stand-ins for skins / wordings / attack lines and the lexicon (tests only)
  haiku_author.py, freeze_pools.py, freeze_v2.py, extract_build.py   the v1 pool authoring and freezes (frozen)
  authoring_i1.py   wording lint (polarity, no contractions) and briefs for the next wording round (fix iteration 1)
  quarantine_i1.json   the post-freeze quarantine record read by freeze_v2.make_ctx (PILOT_VERDICT FIX-1)
  run_pilot_i1.py   the pilot after fix iteration 1 -> pilot_i1/ (sampler seed weights, FIX-5)
  test_plugin.py, test_fix_i1.py, test_*.py   in-memory tests (no file is written: A37 f)
"""
