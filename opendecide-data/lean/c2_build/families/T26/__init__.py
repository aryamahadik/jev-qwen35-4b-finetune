"""c2_build/families/T26: legitimate vs fake authority by stated provenance checks (C2_DATA_SPEC 2.1, 3.7).

  G0_SPEC.md     the one-page G0-lite spec (frozen v1 after the Haiku ambiguity pass; sha pinned in plugin.py)
  plugin.py      T26Plugin: samplers, solver A (checklist rule engine), rendering, relations, error models
  solver_b.py    independent parser of the rendered row + solver B (exact code-point compare, normaliser guard,
                 2x2 decision table); written from G0_SPEC.md, imports nothing from plugin.py
  fixtures.py    in-memory stand-ins for the Haiku skins, wordings, attack lines and lexicon (tests only; never
                 written to disk, never training text)
  test_plugin.py in-memory tests (no file is written)
  author_tasks.py builds the Haiku authoring task chunks (packs, skins, Mode F, attack lines, wordings,
                 precedence paraphrases) under haiku/author/ through the kit's guarded writers (after A38)
"""
