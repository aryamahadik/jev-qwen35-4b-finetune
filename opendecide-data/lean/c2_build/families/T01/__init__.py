"""families/T01: rolling windows and anchored deadlines (C2_DATA_SPEC 2.1 T01, 3.10). Code only before A38.

  G0_SPEC.md     the G0-lite spec v3 (sha256 in plugin.T01.G0_SHA256_AUTHORED): the version every pools_v2 task, answer and
                 manifest was authored against (freeze.py, freeze_v2.py, haiku_author.py, haiku/redo2 and redo3)
  G0_SPEC_v4.md  the frozen one-page G0-lite spec (sha256 in plugin.T01.G0_SHA256): v3 plus section 12, the Stage B pilot
                 fix iteration 1 (double negation, option cues, polarity rule, wording rulings)
  plugin.py      sampling, solver A (day-ordinal integer arithmetic), rendering, relations, error models
  solver_b.py    the independent parser + solver B (day-by-day bitmap, per-day ledgers, epoch minutes)
  fixtures.py    in-memory stand-ins for Haiku skins / wordings and the lexicon (tests only)
  haiku_dneg.py  the double-negation wording round (redo4): brief, checker, task files (nothing run)
  run_pilot_i1.py the iteration-1 pilot into pilot_i1/ (pilot.py, output folder redirected)
  test_plugin.py, test_i1_fixes.py  in-memory tests (no file is written)
"""
