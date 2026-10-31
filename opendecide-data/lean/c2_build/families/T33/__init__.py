"""c2_build/families/T33: outcome verification against tool logs (C2_DATA_SPEC 2.1, 3.3). Code only before A38.

  plugin.py      simulator (pattern table), sampling, solver A (log replay state machine), rendering, relations,
                 error models
  solver_b.py    independent parser of the rendered row + solver B (sqlite over the parsed log)
  fixtures.py    in-memory stand-ins for Haiku skins / wordings / attack lines and the lexicon (tests only)
  G0_SPEC.md     the one-page G0-lite spec (sha frozen in plugin.T33Plugin.G0_SHA256, after the Haiku ambiguity
                 pass amb:T33: haiku/ambiguity/amb_T33_points.json)
  haiku_author.py  the Haiku pools: authoring tasks (haiku/author/), loader + G-SL lint, G-LEX extraction tasks
                 (haiku/extract/), admission and the frozen pools (pools/)
  test_plugin.py in-memory tests (A == B, relations, balance, G-SL, determinism)
  test_haiku_author.py  in-memory tests of the pool module (tasks, loader, G-LEX, stand-in pools end to end)
"""
