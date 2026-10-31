"""families/T23: governing version under transition clauses (C2_DATA_SPEC 2.1, 3.11). Code only before A38.

  G0_SPEC.md     the frozen one-page G0-lite spec, v4 (sha256 in plugin.T23.G0_SHA256); G0_SPEC_v3.md is the v3 text the
                 pools_v2 freeze and the Stage B pilot (pilot/) were made under (plugin.T23.G0_SHA256_V3)
  plugin.py      sampling, solver A (rule engine over version windows and clauses), rendering, relations, error models,
                 the wording screen (ctx_for) and the card (CardSpec; rules in row.card on yes/no rows)
  solver_b.py    the independent parser + solver B (in-memory sqlite window filter + separately coded clause rule)
  fixtures.py    in-memory stand-ins for Haiku skins / wordings / attack lines and the lexicon (tests only)
  test_plugin.py in-memory tests (no file is written); test_pilot_fixes.py: the fix iteration 1 tests on the real pools
  run_pilot_i1.py  pilot.py `run T23` with the output in pilot_i1/ (fix iteration 1 of 2)
"""
