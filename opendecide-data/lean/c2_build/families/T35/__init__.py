"""c2_build/families/T35: path-rule access, robots-style (C2_DATA_SPEC 2.1, 3.2). Code only before A38.

  plugin.py      sampling, solver A (trie longest match), rendering, relations, error models
  solver_b.py    independent parser of the rendered row + solver B (regex compile, brute force)
  fixtures.py    in-memory stand-ins for Haiku skins / wordings / attack lines and the lexicon (tests only)
  G0_SPEC.md     the one-page G0-lite spec (sha frozen in plugin.T35Plugin.G0_SHA256)
  pools/         the frozen Haiku pools; plugin.load_pools() reads packs.json and operators.json by sha256
  test_plugin.py in-memory tests (A == B, relations, balance, G-SL, determinism)
"""
