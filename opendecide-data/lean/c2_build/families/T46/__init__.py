"""c2_build/families/T46: DISPOSITION-GATE, the post-freeze disposition family (Ruling A59; C2_DATA_SPEC 2.1, 3.0).

  G0_SPEC.md        the G0-lite spec (targets of A59 (c) and (d), the label / value lexicon, seed ranges)
  tables.py         the program tables: classes, vocabularies, workflows, flags, numeric pairs, name pools, layouts
  policy.py         policy cards (plain and stated) and the decision engine (solver A, paradigm rule_engine)
  vocab.py          state layouts, rules block, codes (renderer side)
  plugin.py         T46Plugin: samplers, solver A, rendering, relations, error models, make_ctx
  solver_b.py       independent parser of the rendered row + decision-table solver (paradigm decision_table)
  fixtures.py       in-memory stand-ins for the Haiku pools (tests only; never trained)
  haiku_author.py   Haiku task files (wordings, glosses, Arabic slots, G-LEX reads), admission, pool freeze / load
Imports only c2_kit (never job3_disposition, never another family).
"""
