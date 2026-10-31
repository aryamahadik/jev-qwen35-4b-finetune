"""F2 generator (rule arithmetic, money, quantities, dates) for OpenDecide C round 1.

Binding: c_src/F2/G0_SPEC.md v7 (frozen, sha256 2c03f4cf...), c_spec/C_DATA_SPEC.md v4, c_spec/C_TRAIN_RECIPE.md v4,
PREREG_FINAL A15, A16, A16.1. Modules:
  common   paths, IO, Decimal context, display formats, guard
  packs    pack adapters (packs-1..4) and the train / held-out pack split
  lex      the phrase lexicon (card clauses, question frames, cues): the parser owns it, the renderer must parse through it
  money    S1 / S2 money pipeline (solver A, readings, hooks)
  bands    S3 tiered tables
  dates    S4 calendar rules
  stmt     S5 line-item statements (held out)
  canon    canonical problem (structure hash input) shared by A and the parser
  solve_b  integer re-solver on the canonical problem (G3 re-solve; no decimal / fractions / datetime)
  parse    the round-trip parser (rendered row text -> canonical problem)
  build    cards, rows, twins, rendering, gates, outputs
"""
