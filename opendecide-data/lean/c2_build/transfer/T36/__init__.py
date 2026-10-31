"""transfer/T36: dependency version-range satisfaction (C2_DATA_SPEC 2.2, 3.20; transfer dev only, never trained).

  G0_SPEC.md       the frozen one-page G0-lite spec v2.2 (sha256 in plugin.T36Plugin.G0_SHA256); G0_SPEC_v2.1.md is the
                   v2.1 the Haiku pools were frozen under (plugin.POOL_G0_SHA256)
  plugin.py        sampling (stratified slots, the ch_pick plan), solver A (comparator AST interpreter over sort keys),
                   rendering (row-specific cards), relations, error models
  solver_b.py      the independent parser + solver B (one interval per alternative, pairwise compare function); written
                   from G0_SPEC.md, imports nothing from plugin.py; builds the expected card from the parsed range
  fixtures.py      in-memory stand-ins for skins / wordings / attack lines and the lexicon (tests only)
  double_neg.py    the Haiku brief and the admission check of the yn_double wordings (pilot fix F5; run after A38)
  pilot_i1.py      the pilot re-run after fix iteration 1, into pilot_i1/ (pilot/ keeps the first pilot and its verdict)
  test_*.py        in-memory tests (no file is written: A37 f); test_pilot_i1.py covers the pilot fixes F1-F8
"""
