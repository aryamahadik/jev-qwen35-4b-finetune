"""c2_build/families/T24: revision materiality, does the edit change this case's outcome? (C2_DATA_SPEC 2.1, 3.12).

  G0_SPEC.md        the one-page G0-lite spec, v2 FROZEN after the Haiku ambiguity pass c2-data-stage-a/amb:T24
                    (sha pinned in plugin.T24Plugin.G0_SHA256; the pass in plugin.T24Plugin.G0_AMBIGUITY_PASS)
  plugin.py         T24Plugin: samplers, solver A (rule AST per version), rendering, relations, error models
  solver_b.py       independent parser of the rendered row + solver B (one SQL query per version over sqlite);
                    written from G0_SPEC.md, imports nothing from plugin.py
  fixtures.py       in-memory stand-ins for the Haiku skins, wordings and clause lexicon (tests only; never written to
                    disk, never training text)
  authoring.py      the Haiku authoring tasks (G0 section 3; written after A38 to haiku/author/ by paths.write_files)
                    and the lint-stage loader / program checks
  haiku/            ambiguity/amb_T24.json (the pass's 45 points); author/ (tasks, chunks, prompts, key, TASKS.json)
  test_plugin.py, test_authoring.py   in-memory tests (the loader test writes only to pytest's tmp_path)
"""
