"""transfer/T19: compliance checklist with scope exclusions and evidence expiry (C2_DATA_SPEC 2.2, 3.20; transfer dev
only, never trained).

  G0_SPEC.md        the frozen one-page G0-lite spec, v1.2 (sha256 in plugin.T19Plugin.G0_SHA256)
  G0_SPEC.v1_1.md   the v1.1 text the Haiku task files and pools_v2 were authored under, byte for byte
                    (plugin.T19Plugin.G0_SHA256_AUTHORED; freeze_v2 / redo2 / redo3 rebuild from it)
  plugin.py         sampling, solver A (kit rule AST + Kleene evaluate3), rendering, relations, error models
  solver_b.py       the independent parser + solver B (sqlite tables and SQL); written from G0_SPEC.md, imports nothing
                    from plugin.py
  fixtures.py       in-memory stand-ins for skins / wordings / attack lines and the lexicon (tests only)
  test_plugin.py    in-memory tests (no file is written: A37 f)
  test_fix_i1.py    tests of Stage B pilot fix iteration 1 (card placement and styles, balance cycles, kinds-first evidence,
                    twins, yn_dneg, wording polarity, the G0 v1.2 page)
  authoring_i1.py   the yn_dneg wording brief and admission check for a later Haiku round (nothing has run)
  measure_i1.py     in-memory balance / length / G6 / G7 measurement used to tune the fixes (writes nothing)
  run_pilot_i1.py   pilot.py's pilot with the output folder renamed to pilot_i1/ (the first pilot, pilot/, stays as evidence)
  pre_i1_backup/    plugin.py, solver_b.py, fixtures.py, G0_SPEC.md and test_plugin.py as they were before fix iteration 1
"""
