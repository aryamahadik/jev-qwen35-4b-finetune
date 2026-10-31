"""c2_build/families/T30: clarify or proceed after deduplication (C2_DATA_SPEC 2.1, 3.5). Code only before A38.

  plugin.py      sampling, solver A (set algebra + decision table), rendering, relations, error models
  solver_b.py    independent parser of the rendered row + solver B (sqlite GROUP BY + SQL CASE)
  fixtures.py    in-memory stand-ins for Haiku skins / wordings / attack lines and the lexicon (tests only)
  G0_SPEC.md     the one-page G0-lite spec (sha frozen in plugin.T30Plugin.G0_SHA256)
  test_plugin.py in-memory tests (A == B, relations, balance, G-SL, determinism)
"""
