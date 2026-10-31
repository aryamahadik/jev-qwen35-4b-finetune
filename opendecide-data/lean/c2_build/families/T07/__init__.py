"""c2_build/families/T07: headline promise vs footnote qualifier (C2_DATA_SPEC 2.1, 3.16; PREREG_FINAL A37).
Code only before A38.

  G0_SPEC.md     the one-page G0-lite spec v1 (+ redo2 notes R1-R5): the spec the Haiku tasks, the pools and the
                 extraction records were authored under (sha256 T07Plugin.G0_SHA256_AUTHORED); frozen, never edited
  G0_SPEC_v2.md  v2 = v1 + section 8 (fix iteration 1, 14 Oct 2026): ch_failing None gold 1/k, stratified ch_offers
                 outcome, polarity screen; pinned by sha in plugin.py (T07Plugin.G0_SHA256, G0_LITE)
  plugin.py      T07Plugin: samplers, solver A (rule AST over the fine-print conditions), rendering, relations,
                 error models, row_plan (the choice-row plan), ctx_for (the polarity screen)
  solver_b.py    independent parser of the rendered row + solver B (set algebra: each condition becomes the set of
                 attribute values it admits; sets are intersected and the order is tested for membership); written
                 from G0_SPEC.md, imports nothing from plugin.py
  fixtures.py    in-memory stand-ins for the Haiku skins, wordings, attack lines and condition paraphrases (tests
                 only; never written to disk, never training text)
  merged_pools.py  how the generator loads the v1 + redo2 + redo3 pools (sha-checked) and the pool verdict
  load_v2.py     registry + KitCtx over the merged pools (the pilot loader of c2_build/pilot_loaders.py)
  run_pilot_i1.py  the pilot after fix iteration 1, written to pilot_i1/ (pilot/ keeps the first pilot)
  test_plugin.py in-memory tests (no file is written: A37 f)
  test_i1_fixes.py  the fix iteration 1 tests (polarity quarantine, 1/k plan, twins, G0 v2 pin, hash-seed determinism)
"""
