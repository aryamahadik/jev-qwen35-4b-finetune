"""families/T31: authority at time t (delegations, bands, revocations, sub-agent scopes). Code only before A38.

  G0_SPEC.md       the frozen one-page G0-lite spec, v1.2 (sha256 in plugin.T31.G0_SHA256); G0_SPEC_v1_1.md is v1.1
                   verbatim, the spec the Haiku pools were authored under (plugin.POOL_G0_SHA256)
  plugin.py        sampling, solver A (rule engine), rendering, relations, error models, packs / names wiring, the
                   choice plan, the card styles, the pool screen (ctx_for)
  solver_b.py      the independent parser + solver B (epoch-minute interval scan + set intersection)
  fixtures.py      in-memory stand-ins for Haiku skins / wordings / attack lines and the lexicon (tests only)
  dneg_authoring.py the F07 authoring brief and admission check of the double-negation wordings (no Haiku run yet)
  run_pilot_i1.py  the fix-iteration-1 pilot into pilot_i1/ (pilot.py's own gates; pilot/ stays as produced)
  test_plugin.py, test_i1_fixes.py   in-memory tests (no file is written)
  haiku_author.py, topup.py, glex_admit.py, freeze_v2.py, extract_build.py   the pool tools (pools_v2 is frozen)
"""
