# T37b Haiku pool (G0_LITE_T37B.md v2, S12 / H40-H41)

T37b's only Haiku authoring: paraphrase templates for the equiv pool (author_wording; answers in answers/<task id>.json).
Every complement partner is program-written, so there are no skins, packs, registers or documents for T37b.

Next stages (run from lean/; never edit labels; Haiku answers only admit or drop a paraphrase):
  lint:  ../.venv/bin/python c2_build/t37b/author_pool.py lint
         (loads these answers, checks them with both polarity programs, dedups, writes ../extract/: two independent
         polarity reads per paraphrase in separate chunks; tasks listed in ../extract/TASKS.json)
  admit: ../.venv/bin/python c2_build/t37b/author_pool.py admit
         (admits a paraphrase only when both reads say 'same'; freezes ../../pools/)
