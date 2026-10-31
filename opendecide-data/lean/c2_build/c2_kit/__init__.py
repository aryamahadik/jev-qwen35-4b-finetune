"""c2_kit: the shared C2 build kit (C2_DATA_SPEC 6.2 items 1, 2 and 5; PREREG_FINAL A37). Code only: before the
OHS-4 freeze (A38) nothing here writes data; every writer goes through paths.require_a38().

Modules
  paths        never-open guard (spec 6.5), A38 data guard, guarded writers
  slots        typed slots: date, UTC-offset datetime, integer cents, count, category, id, glob, URL, name, clause
  skin         slot-locked skins, the renderer with grammar agreement and spans, the template-guided parser (G3)
  rules        rule AST, interpreter, precedence policies P1-P5 (solver-A side)
  globsem      glob semantics; glob_a (token AST matcher, solver A) and glob_b (regex compile, solver B)
  brute        brute-force helpers for solver B (completions, day lists, epoch minutes, integer cents)
  lexicon      operator lexicon registry: surface form -> semantic id, unit tests, 2/2 or 3/3 admission (G-LEX)
  distractors  options from named error models; label-blind gold position; abstain checks
  choiceplan   choice-row display plan drawn at sampling time (k, abstain display, abstain gold 1/k, position,
               length rank); plan_report() pre-pilot balance check
  polarity     a yes/no wording must read with its form's polarity (G-LEX meaning check; opt in)
  cards        compact rule cards: placement (yes/no rules in row.card), compact / short variants, style
               draw, token_report() with the pinned tokenizer
  plugin       THE PLUGIN CONTRACT (C2Plugin, Spec, QuestionForm, RenderedRow, RelationProposal, KitCtx),
               validate_plugin(), check_independence()
  rows         row assembly (spec 2.4 + meta.c2), validate_row(), G15 bridge (formats-1 loader_check)
  relations    relation emitter (complement, minimal-edit twin, equiv, inv, premise removal) and G-TW
  gsl          G-SL slot lint / fact-lock
  g3h          G3-H LLM round-trip comparison
  g5h          G5-H two blind reads + Claude adjudication queue
  chunker      Haiku task chunks (TEACH-0 pattern: gold-free, opaque ids, <= 50 items)
  audit        file-access auditor for Haiku task agents
  pipeline     one relation unit through G2, G3, G4, G-SL, G-TW, G15 in memory; overlay share report
  reference/   R00, the complete reference plugin (kit example only: never written, never trained)
See c2_build/README.md.
"""
__version__ = "1.0"
