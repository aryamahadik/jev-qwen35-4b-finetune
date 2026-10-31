"""families/T27: embedded request that widens the user's scope (C2_DATA_SPEC 2.1 / 3.6; A37). Code only before A38.

  G0_SPEC.md      the one-page G0-lite spec (v1.2, 14 Oct 2026: v1.0 frozen after the Haiku ambiguity pass amb:T27, v1.1 =
                  P49 / P50, v1.2 = the Stage B pilot fixes: card styles + placement, gold uniform over the three labels,
                  wording polarity; sha in plugin.py; G0_SPEC.v1_1.md is the v1.1 text)
  plugin.py       T27Plugin: sampling, solver A (rule engine), rendering, relations, error models
  solver_b.py     parse(row, ctx) + solve_b(view): independent parser and set-algebra solver
  vocab.py        closed value sets both solvers read (pure data)
  fixtures.py     in-memory stand-ins for the Haiku skins / wordings / lexicon forms (tests only, never written)
  test_plugin.py  in-memory tests
  authoring.py    the 33 Haiku authoring tasks (G0 section 6), their loader and the family lint (lint_piece)
  test_authoring.py  in-memory tests of the tasks, the lint and the loader
  run_pilot.py    the pilot driver (loader of pools_v2/ registered in-process; --out pilot | pilot_i1)
  measure.py      in-memory balance / length measurement used to tune the sampler (writes nothing)
  haiku/author/   the written task chunks (after A38), TASKS.json, key/ and manifest/ (orchestrator side), answers/
"""
