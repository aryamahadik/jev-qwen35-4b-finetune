"""c2_build/families/T28: permission verdicts from precedence rules (allow / ask / deny) (C2_DATA_SPEC 2.1, 3.1).
G0 frozen after the Haiku pass (13 Oct 2026).

  plugin.py      sampling, solver A (rule AST + glob_a under the stated precedence), rendering, relations, error models
  solver_b.py    independent parser of the rendered row + solver B (regex compile, match table, sort-key precedence)
  fixtures.py    in-memory stand-ins for Haiku skins / wordings / attack lines and the lexicon (tests only)
  G0_SPEC.md     the one-page G0-lite spec, v1.2 (14 Oct 2026; sha in plugin.T28Plugin.G0_SHA256)
  G0_SPEC.v1_1.md  the byte-exact v1.1 the Haiku tasks and pools_v2 were authored under (G0_SHA256_AUTHORED)
  test_fix_i1.py in-memory tests of the Stage B fix iteration 1 (cards, balance, plans, deals, polarity, pins)
  run_pilot_i1.py  the pilot of fix iteration 1, written to pilot_i1/
  test_plugin.py in-memory tests (A == B, relations, balance, G-SL, determinism, G0 section 9 resolutions)
  haiku_author.py   Haiku authoring tasks (haiku/author/, written after A38) + answer loaders / checks
  test_haiku_author.py   in-memory tests of the authoring batches, task files, pack validator and checks
  haiku/ambiguity/  the Haiku G0-lite ambiguity listing this freeze resolves (G0 section 9)
"""
