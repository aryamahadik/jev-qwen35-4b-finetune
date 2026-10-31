"""c2_build/families/T12: three-way match with ordered exception precedence (C2_DATA_SPEC 3.15).
Haiku authoring tasks written after A38.

  plugin.py      T12Plugin: sampling, solver A (Decimal rule engine), rendering, relations, error models
  solver_b.py    solver B (sqlite join of the three documents in integer cents), written from G0_SPEC_v2_2.md
  fixtures.py    in-memory stand-ins for the Haiku pools (tests only; never written)
  G0_SPEC_v2_2.md  the frozen one-page G0-lite spec in force (v2.2, fix iteration 1, 14 Oct 2026; T12Plugin.G0_SHA256)
  G0_SPEC.md     G0-lite v2.1 (13 Oct 2026, after the Haiku ambiguity pass amb:T12): the spec the Haiku tasks and the
                 pools were authored under, unchanged (plugin.G0_SHA256_AUTHORED)
  authoring.py   the Haiku authoring tasks (haiku/author/) and the checks the lint stage runs on the answers
  wording_screen.py  the generation-time wording screen (premise rule of F1 + the kit polarity rule)
  run_pilot_i1.py    the pilot of fix iteration 1 into pilot_i1/ (pilot/ is the Stage B record)
  run_pilot_i2.py    the pilot of fix iteration 2 into pilot_i2/ (R20 yes draw stratified by question form x card)
"""
