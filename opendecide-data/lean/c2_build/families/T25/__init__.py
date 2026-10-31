"""families/T25: source reliability conflict with tie-abstain (C2_DATA_SPEC 2.1, 3.17). Code only before A38.

  G0_SPEC.md     the frozen one-page G0-lite spec, v4 (sha256 in plugin.T25.G0_SHA256); G0_SPEC_v3.md is the v3 text the pool
                 freeze (freeze_v2.py, pools_v2/) was made under, kept byte for byte
  plugin.py      sampling, solver A (rule engine: a pairwise "outranks" rule AST), rendering, relations, error models
  solver_b.py    the independent parser + solver B (sort by tier rank and date, itertools.groupby head group);
                 written from G0_SPEC.md, imports nothing from plugin.py
  fixtures.py    in-memory stand-ins for Haiku skins / wordings / attack lines and the lexicon (tests only)
  test_plugin.py in-memory tests (no file is written: A37 f)
  haiku_author.py the Haiku authoring tasks (G0 section 7; written under haiku/author/ after A38) + answer loaders
  test_haiku_author.py in-memory tests of the authoring tasks and loaders
  test_polarity_regression.py the wording polarity rule (c2_kit.polarity) on the pool, the authoring check and the pipeline
  run_pilot_i1.py the pilot of fix iteration 1 (pilot.run_family with its output folder redirected to pilot_i1/)
  haiku/ambiguity/amb_T25_points.json the Haiku ambiguity listing resolved in G0 section 9
"""
