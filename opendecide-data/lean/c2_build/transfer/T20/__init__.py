"""transfer/T20: incident severity with override precedence and timed escalation (C2_DATA_SPEC 2.2, 3.20; transfer dev
only, never trained).

  G0_SPEC.md          the frozen one-page G0-lite spec, v3 = v2 (after the Haiku pass amb:T20) + fix iteration 1 of the
                      pilot verdict (sha256 in plugin.T20Plugin.G0_SHA256; pass id in plugin.T20Plugin.G0_HAIKU_TASK)
  plugin.py           sampling, packs (one per card), solver A (matrix lookup + integer-minute arithmetic), rendering,
                      relations, error models
  solver_b.py         the independent parser + solver B (matrix read from the card, minute-by-minute escalation
                      simulator); written from G0_SPEC.md, imports nothing from plugin.py
  fixtures.py         in-memory stand-ins for skins / wordings / attack lines and the lexicon (tests only)
  haiku_author.py     the Haiku pools (G0 section 6): write-tasks -> haiku/author/; lint (program checks, G-SL, unit
                      tests, render probes; writes the G-LEX reads to haiku/extract/); admit (2/2 G-LEX, pools/)
                      run from lean/c2_build:  ../../.venv/bin/python -m transfer.T20.haiku_author lint | admit
  haiku/ambiguity/    the amb:T20 points, verbatim, with their sha256 and the resolution map
  roles.py            the Mode F REPORTER role rule (F6; used by haiku_author.check_freeform and plugin.ctx_for)
  quarantine.py       pool templates the plugin never renders (G3-H, G5-H evidence; nothing relabelled, pools/ untouched)
  run_pilot_i1.py     the pilot after fix iteration 1, written to pilot_i1/ (same pilot.py, seeds and bars; pilot/ is the
                      first pilot and is kept as evidence)
  test_plugin.py, test_haiku_author.py, test_fix_i1.py   in-memory tests (no file is written)
  _pre_i1/            the code and G0 as they were before fix iteration 1 (*.orig; evidence for diffs, not imported)
"""
