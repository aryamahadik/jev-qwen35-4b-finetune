"""c2_build/families/T06: consumer return rights, non-waivable floor vs posted policy (C2_DATA_SPEC 2.1, 3.13).
Code only before A38.

  plugin.py      sampling, solver A (decision tables on day ordinals), rendering, relations, error models
  solver_b.py    independent parser of the rendered row + solver B (day-by-day window bitmaps, a separate
                 exclusion evaluator, its own notice and question tables)
  fixtures.py    in-memory stand-ins for Haiku skins / wordings / attack lines / store-notice forms (tests only)
  G0_SPEC.md     the one-page G0-lite spec (sha frozen in plugin.T06Plugin.G0_SHA256)
  test_plugin.py in-memory tests (A == B, relations, balance, G-SL, determinism, error models, gate teeth)
"""
