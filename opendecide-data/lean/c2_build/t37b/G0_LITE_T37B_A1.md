# G0-lite T37b, Amendment 1 (G0 v3 = G0_LITE_T37B.md v2 + this page)

Frozen 14 Oct 2026 for fix iteration 1 of at most 2 (C2_DATA_SPEC 6.4 step 6: generator and template fixes only). Source:
the stage-B pilot verdict `t37b/pilot/PILOT_VERDICT.json` (FIX: F1, F2, F3, F5 are amended here; F4 is not, see A1-7).
G0 v2 is untouched: its sha256 (builder.G0_SHA256, 9733b721...) binds the frozen Haiku pool, every Haiku task record and
answers_gate, and the pool is unaffected by this page. Where v2 and this page differ, this page wins for the items it
names. builder.G0_AMENDMENT_SHA256 is the sha256 of this file; builder.g0_problems() must be empty. Nothing here sets,
edits or chooses a label, loosens a bar or lowers a target; the amendment only drops units, refuses base shapes,
changes which wording keys are capped and chooses which bases enter.

- A1-1 (S13, H43, section 3 point 11; fix F1). The blind solver's disagreement with the human gold now matters in one
  place: a unit whose blind solver answers the BASE against the base's human gold is dropped (no Claude review can keep
  it), however consistent its base and partner answers are. Order in builder.decide: programs, then both polarity
  reads, then this test, then the consistency test (an inconsistent pair whose base answer equals the gold still goes to
  Claude review). Pilot evidence: of 42 units, exactly the 2 units whose blind base answer differed from the base gold
  (a wrong human gold, a0036; an unsupported base, a0019) were the 2 G5-H rows traced to the base.
- A1-2 (H15, section 2 hotpotqa; fix F2). The hotpotqa subject rule is the anchor rule, in both programs: the question
  is `<aux> <SUBJECT> both <REST>?` with exactly ONE " both " (whole word, lower case), the subject is everything between
  the auxiliary and that " both ", the rest starts with "both"; every other shape (no " both ", two, "the same",
  "Do X <verb>", "Is X a ...", a leading "both") is refused, so such a base has no kind at all (hotpotqa has only
  syntactic, H40). The capital-run
  rule is gone (it cut "Are BLT cocktail and Tamango both ..." at "BLT"). A reads " both " in the text, B counts the
  word "both" among case-kept words and then compares token sequences; a difference between them only drops. Measured
  read-only on the 3,027 hotpotqa aff yes/no rows of golden_train: both programs accept 1,269 for a syntactic partner
  (the old rule accepted 1,694; the pilot verdict counted 95 of its 1,101 one-" both " questions and many of its 593
  others cut mid-name); every accepted base's partners read "opposite" in both programs.
- A1-3 (S14, H47; fix F3). A partner wording key is entry x kind x frame / cue / pair x base question for the four
  complement kinds, as before. For equiv the key is the pool paraphrase only (para_key): the base question of an equiv
  row is not a partner wording, and counting it capped all of a fixed-question entry's equiv rows at 2% together (the
  pilot plan collapsed to 42 rows). The cap is still floor(2%) of the realised block (min 1) for every counted key.
  meta.t37b.template keeps its v2 value on every row (the G5-H template key); only the cap count changes.
- A1-4 (S14, H2, H48; fix F3). The caps are shares of the REALISED block, so plan_block re-plans on a smaller basis
  until they hold on the size it realises (the first fixed point). With A1-3 that point exists: measured on the pilot
  inputs it is 564 rows at the 1,000 target (700 : 300; 66 implicit, 93 non-syntactic, 105 syntactic, 300 equiv) and
  1,152 at the 2,000 target (138 implicit, 194 non-syntactic, 220 syntactic, 600 equiv). The binding limit is implicit
  wording capacity: 6 implicit wordings (check_covid support / refute, multiwoz booking, nhtsa crash / fire, cards
  claim; "fail to" is the only exact cue, H59) times floor(2%) is at most 12% of the block, and implicit must be >= 25%
  of the complements, so complements are <= 0.48 of the realised block. A shortfall lowers the block (H2); it is never
  refilled and no cap or floor is relaxed.
- A1-5 (H11; fix F5). The plan still never reads the gold to choose a kind, frame, cue, pair or paraphrase, and the
  partner's label is always 1 - base gold (complement) or the base gold (equiv), set in builder.partner_row. It reads
  the gold for one thing: which bases enter. A base is skipped when its partner's gold side (1 = yes) is already ahead
  at any of three levels: the whole block, its wording cell (frame / cue / antonym pair / option frame / paraphrase),
  its (entry, kind) cell. So the partner yes rate is 50% within one row at each level, whatever the base sources'
  own rates. The test is symmetric, so flipping every gold leaves the plan unchanged. When surplus implicit or
  non-syntactic items are released (H48) the latest are removed, alternating the partner gold. trim_block (H48) is
  unchanged: it only removes, after the Haiku checks, and does not rebalance. T37b-dev (S15) is not balanced.
- A1-6 (S14, spec 3.0 length; new). Every partner row must be <= 2,000 rendered tokens (spec 3.0: the pinned Qwen3.5
  tokenizer through c_build/mixer.token_counts, instructions counted twice). builder.finalize drops the whole unit of a
  partner row over that, like a G15 failure (counted by reason, never a fix-up; trim_block then restores the floors and
  caps, and a shortfall is not refilled). The family mean (<= 800) is measured by the pilot (spec_3_0), not enforced
  per row. T37b-dev is exempt (never trained). Pilot i1 evidence: 1 of 564 rows had 2,020 tokens (v2 had no length rule).
- A1-7 (open, not amended). Spec 3.0's double-negation floor (>= 2% of yes/no rows with k_syn >= 2) cannot be met by
  any T37b row: the base holds no negation (S8) and each partner adds exactly one. It needs a ruling (the floor is a
  program-family overlay rule and 3.18 does not name it) or a new closed double-negation kind with its own exactness
  argument, polarity programs, Haiku reads and G13 method-8 check. Neither is made here; G10 reports the share.
