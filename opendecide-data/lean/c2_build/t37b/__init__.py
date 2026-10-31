"""c2_build/t37b: the T37b real-text complement / equiv builder (C2_DATA_SPEC 2.1 T37b, 3.18, 4.2; PREREG A37).

T37b is not a C2Plugin family: it adds ONE partner question to a hard-label, human-gold yes/no replay row whose card
defines a binary predicate, and links the two rows as a 2-row relation unit (same call_id). Partner gold is
1 - human gold (complement) or the human gold (equiv). No model sets a label.

  G0_LITE_T37B.md  the frozen one-page spec v2 (sha256 in builder.G0_SHA256; Haiku pass builder.G0_HAIKU_TASK, points
                   in haiku/ambiguity/amb_t37b_points.json); the frozen pool and every Haiku task record are bound to it
  G0_LITE_T37B_A1.md  Amendment 1 (14 Oct 2026; G0 v3 = v2 + A1; sha256 in builder.G0_AMENDMENT_SHA256): the fix
                   iteration 1 items A1-1 .. A1-6 (blind base against the human gold drops the unit; hotpotqa anchor
                   rule; equiv capped by its paraphrase; fixed-point plan; partner-gold balance; 2,000-token cap) and
                   A1-7, the open double-negation question. g0_problems() checks both files
  sources.py       the closed source registry: which replay questions define a binary predicate, their allowed
                   partner kinds, closed antonym lists, option-framing rules and card handling (written from the
                   golden_src builder code and MANIFEST notes only; no row was opened)
  polarity.py      polarity program A: negcount (XF02) cue counts, cue class and position, scope rules
  polarity_b.py    polarity program B: an independent word-level edit-script classifier (no negcount, no polarity.py)
  select.py        base selection (every spec 3.18 base rule, counted) and the block plan (never reads the gold to
                   choose a kind or wording; reads it only to balance the partner gold, A1-5)
  builder.py       program-written partners (all kinds), polarity / blind-read items, partner rows, the keep-or-drop
                   decision, the block report, the A38- and G0-guarded writers (train block, T37b-dev)
  author_pool.py   Haiku's only authoring job: the equiv paraphrase pool (slot templates per entry): tasks, lint, the
                   two polarity reads, admission and the frozen pool (pools/)
  fixtures.py      Claude-written stand-in rows and stand-in Haiku answers for the tests (in memory only)
  test_t37b.py, test_author_pool.py, test_fix_i1.py   in-memory tests (no file is written)
  pools/FIX_I1_MANIFEST.json  the generator code files fix iteration 1 changed after the pool freeze (frozen sha ->
                   current sha); answers_gate.v1_untouched excuses exactly those, never a data file
Every writer refuses before A38 and while builder.g0_problems() is non-empty.
"""
