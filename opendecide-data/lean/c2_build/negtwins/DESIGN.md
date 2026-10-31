# A42-D item 7: negation-twin framework (design, 15 Oct 2026)

Binding: PREREG A42-D 7.1-7.5, 10 (symmetrisation uses this catalogue), 12.1 (150 held-out complement pairs), A43 (f),
A45 (a) (mandatory for C2), spec 3.18 / 4.2. Code: this folder. Tests: `negtwins/test_negtwins.py` (26 pass,
`../../.venv/bin/python -B -m unittest negtwins.test_negtwins`). No Haiku was run, no row was written.

## 1. A pattern is a program rewrite

`core.py`. A base row's `instructions` = preamble + core (the core is the last sentence, one polar question). The core is
parsed by two independent parsers (A regex, B token scan; closed verb table and closed predicate-start list); if they
disagree the base is dropped for that pattern, never guessed. A pattern is

    (operator, predicate class, frame or cue, contraction, verb, lexical pair + direction)       pid = hash of these

| Operator | Relation | What it does | Example |
|---|---|---|---|
| FRAME_NOT | complement | positive frame + one `not` / `n't` after the auxiliary (T37b syntactic; do / is / has / `can`) | Is it true that this text does not contain a passport number? |
| NEG_FRAME | complement | negative frame over the POSITIVE proposition, declarative order (any class incl. modals, quantified cores) | Is it false that this text contains a passport number? |
| FAIL_TO | complement | `fail to` before the main verb, frame optional | Does this text fail to contain ...? |
| LACK | complement | have / contain / include -> lack, frame optional | Does this text lack a passport number? |
| LEX_PAIR | complement | the predicate word -> its exact lexical complement (pair admitted by G-LEX 2/2) | Is the pet allowed -> Is the pet prohibited |
| POS_FRAME | equiv | positive frame over the unchanged proposition | |
| DNEG_PAIR | equiv | positive frame + not + the pair's complement word | Is it true that the pet is not prohibited ...? |
| DNEG_FAIL | equiv | positive frame + does not fail to | |

Classes: DO, COP, HAVE, MOD (`can` only for FRAME_NOT), THERE. Scope guards are the T37b ones (no quantifier / modal /
clause word / `and` / existing negation for operators that insert a negation; `rewrite` returns None, never a guess).
**A43 (f):** no operator puts a negated interrogative frame over a negated proposition. NEG_FRAME needs a negation-free
core, double negations (DNEG_*) keep the frame positive, contracted frames are refused, and a test runs
`c2_kit.polarity.read` over every twin the catalogue can make. Complement twins carry the card with its definitions
exchanged (T37b swap rule); a yes-only card (G-block wave 1) gets the exact-by-construction wrap
`- yes: It is not the case that <condition>.` / `- no: <condition>.` (`checks.twin_card`; see section 8 item 1).
Gold is never set by a person: gold = 1 - base gold (complement) or the base gold (equiv) (7.5).

## 2. Catalogue size (>= 300)

116 patterns are purely programmatic (6 seed frames x {FRAME_NOT: DO, COP, HAVE, MOD, THERE x not/n't = 60; POS_FRAME 12;
DNEG_FAIL 6; wrapped FAIL_TO 6 + unwrapped 1; LACK 21} + the 2 seed negative frames x 5 classes = 10). Everything else
needs an admitted lexicon entry and is lexicon-based: each extra positive frame adds 17 patterns, each negative frame 5,
each admitted pair up to 3 (a>b, b>a, double negation). The seed-only catalogue is below 300 on purpose (test).

| Admitted by G-LEX 2/2 (frames pos / neg / pairs) | programmatic | lexicon-based | total | complement / equiv |
|---|---|---|---|---|
| low 6 / 4 / 30 | 116 | 212 | 328 | 262 / 66 |
| mid 10 / 6 / 55 | 116 | 365 | 481 | 378 / 103 |
| high 14 / 10 / 70 | 116 | 498 | 614 | 484 / 130 |

The draft asks for 24 + 16 frame candidates and 95 pair candidates; the 300 floor holds if about a quarter of the
frames and a third of the pairs survive G-LEX and the exactness/audit drops. Below that the orchestrator drafts a
second round (more Haiku reads) before training; nothing is lowered.

## 3. Held-out set (7.4), frozen first

`heldout.py`, `HELDOUT_SPECS.json`, `HELDOUT_FREEZE.json`: **43 patterns (40 complement, 3 equiv), sha256
`302e6d4c00be20b614360ebf654adb86d306822ee4ca4ba1bf17970fc3697681`, frozen 2026-10-15T18:05:51Z before any training
pattern, lexicon draft or Haiku task existed** (`verify_frozen()` re-checks it). They are: the 3 T37b-dev frames x
{FRAME_NOT DO / COP / HAVE, POS_FRAME DO} (fixed surface, never trained), 4 Haiku-realised positive frames x n't x
{DO, COP}, 4 Haiku-realised negative frames x {DO, COP, MOD}, 11 Haiku-realised pairs (6 verb, 5 adjective).
`H.disjoint` removes any TRAINING frame / pair that shares a content word with an admitted held-out surface (the
held-out set wins); `H.freeze_realised` logs a second hash of the admitted surfaces. Use: only the G-proxy's 150
complement pairs (`plan.heldout_pairs`, <= 5 per pattern, round-robin, 40 x 5 = 200 slots for 150, so 30 patterns must
survive their exactness check) and the item 10 probe pairs (10.3). The item 10 served flip is a trained-catalogue program
(FRAME_NOT seed frame first, else NEG_FRAME), never a held-out pattern.

## 4. Which base rows qualify (`plan.base_record`)

Common: qtype noul, gold 0/1, hard label (no vote shares, no attack target), a card that is two lines swap-safe or a
yes-only card, core parses with both parsers, no negation cue in the core (negcount k_all = 0) for any complement twin.
A base gets at most one complement twin and one equiv twin (unit <= 3 rows). Complement twins on two-line cards also need
the base type (core x card) to pass the card certificate (2/2 Haiku reads that the two definitions are exact opposites).

* **G-block** (cap 5,000): kept yes/no rows after routing and 5.5 rebalance. Measured today on the Haiku-accepted wave-1
  pool (4,938 yes/no rows, all yes-only cards, **16 distinct questions**, classes DO 3,246 / MOD 984 / COP 708): the plan
  realises about 3,200 twins (1,712 complement, 1,500 equiv) with the programmatic catalogue plus 10 + 6 frames
  (twin yes share 0.524, type share <= 10%, 136 patterns used). Wave-2 two-line cards and the lexical pairs lift it toward
  the 5,000 cap; the final kept set decides the real number.
* **Metadata block** (cap 5,000, inside item 8's 12,000): the item 8 mapper supplies `neg_spec {pre, core}` per task
  (structured, no free-text parse needed beyond `core.parse`) and its two-line card. No row exists yet: the realised
  count cannot be measured. Mappers should phrase predicates in the DO / COP shapes above.
* **Replay yes/no** (cap 10,000 including the original 2,000 T37b): the T37b registry bases (`t37b/select.eligible`)
  keep their entry-specific rules; further KEEP-licence human-gold sources enter through the generic engine only after
  their base type passes the card certificate. Not measurable here (replay shards not read); the 8,000-10,000 target
  needs 6,000-8,000 new replay twins beyond T37b.

## 5. Quotas

Complement : equiv = 70 : 30 (T37b 1,400 : 600). Shares of the POOLED complement twins (spec 3.18): implicit (FAIL_TO,
LACK, NEG_FRAME: fail to, lack, false) >= 25%, antonym (LEX_PAIR) >= 30%, syntactic <= 45% (`plan.pooled_report`,
`plan.trim_pooled` removes syntactic twins only, as T37b `trim_block`). One (pattern, question) cell <= 2%, one pattern
<= 1.2%, one base type <= 10% of the REALISED block (re-planned to a fixed point), twin yes share 45-55%. The plan reads
gold for one thing, which bases enter (the T37b A1-5 precedent); patterns are chosen by hash order.
The G-block alone cannot carry the antonym share (no pair covers most of its 16 questions): the share is pooled and the
pair drafting targets the live predicate words (contain, ask, say, give, require, given, limited, free, ...).

## 6. Checks

1. **Single predicate changed (program):** `checks.check_pair`, an independent reader (lemmas + difflib edit script, no
   call to the rewrite): the added and removed tokens equal the operator's exactly, the edit is one cluster, tense and
   number are unchanged, the token evidence of negation layers (odd = complement) equals the pattern's declared relation.
2. **Exactness (Haiku, flag only):** 10 base/twin pairs per pattern (probe bank + live cores, hash order), one blind
   polarity read each; a pattern needs >= 9/10 (>= 0.9, `unclear` is wrong). A failing pattern leaves the catalogue; no
   twin or label is edited.
3. **G-LEX 2/2** for every drafted frame (3 probes) and pair (2 per direction + 1 double negation), two independent rounds;
   any other pick rejects the entry. Static lint first (`lexicon.lint_frame`, `lint_pair`).
4. **Card certificate** (2/2 reads) per two-line base type.
5. **Sonnet audit** of 3% of twin rows (`tasks.audit_sample`: seeded, >= 1 row per pattern, the rest proportional);
   `audit_decide`: a pattern above 3% error is dropped, a pattern with <= 33 audited rows is dropped on one confirmed
   error. At about 18,000 twins that is 540 rows over about 500 patterns (about 1 per pattern), so nearly every pattern
   is on the single-error rule; the 10-pair Haiku exactness read carries the pattern-level evidence.
6. **G-TW 100%** (`checks.g_tw`): gold(twin) = 1 - gold(base) (complement) or equal (equiv), card = `twin_card(base)`,
   same state and preamble, twins of one role agree. **G13** on `plan.template_strings` (frames, cues, pair words) seed-first,
   then on the twin rows, 0 hits after drops.

## 7. Haiku / Sonnet work and reads (nothing run)

Written now (37 task files, `haiku/`): **draft** (10 tasks, 75 items: 6 pos-frame, 4 neg-frame, 30 pair items x 2 pairs,
35 targeted pair items), **heldout** (3 tasks, 19 slots), **exact_prog** (24 tasks, 1,160 reads for the 116 programmatic
patterns). Writers for the rest: `tasks.write_glex_tasks`, `write_exact_tasks`, `write_card_tasks`, `write_audit_tasks`.

| Stage | Item reads | Tasks |
|---|---|---|
| draft + held-out (author) | 94 | 13 |
| G-LEX, 2 rounds | about 1,190 | 24 |
| exactness, about 520 trained patterns | about 5,200 | 104 |
| exactness, 43 held-out patterns | 430 | 9 |
| card certificates, 2 reads x about 120 types | about 240 | 5 |
| **Haiku total** | **about 7,150** | **about 155** |
| Sonnet audit, 3% of about 18,000 twins | about 540 | 11 |

Order: freeze (done) -> draft + heldout -> `parse_draft` / `heldout_candidates` -> G-LEX -> `lexicon.admit`,
`choose_heldout`, `H.disjoint`, `H.freeze_realised` -> `build_catalogue(admitted)` -> exact -> `exactness_decide` -> plans
-> `build_rows` -> `g_tw` -> audit -> `audit_decide` -> drop patterns and their twins -> `trim_pooled` -> G13.

## 8. Open items for the orchestrator

1. The wrap card for yes-only cards (G-block wave 1) is a new card rule; it is exact by construction and covered by the
   audit, but an Opus nod is needed (`plan.WRAP_ONE_SIDED = False` makes those bases equiv-only).
2. The G-block has 16-23 distinct questions, so its twins rest on pattern variety, not question variety; the cell and
   type caps bind early (about 3,200 of 5,000 today).
3. Parsers A and B share the closed word lists; their independence is mild. The real guards are the checker, the Haiku
   exactness read and the audit.
4. Metadata mappers must expose `neg_spec`; replay sources beyond the T37b registry need card certificates.
5. `Is it not the case that` is a seed negative frame over a positive proposition (allowed by A43 f); G5-H should include
   a sample of its twins.

## 9. Ruling A48 (h) (15 Oct 2026, ~22:35 UTC): stricter admission, applied before any G-LEX or lexicon exactness read

Dropped by program whatever the exactness score: (i) every pattern whose frame negates the interrogative (`core.a48h_class`: the
seed "Is it not the case that" x 5 classes); (ii) a split or ambiguous modal negation: `core.MODAL_SPLIT` refuses any twin with "can
not", "could not", "couldn't" and the like, while "cannot" and "can't" (the modal negated as a unit; orchestrator decision, 15 Oct)
stay, so the 6 "can't" seed patterns are kept (exact_prog 0.9 / 0.9 / 1.0 / 0.9 / 1.0 / 0.9); (iii) frames that change the subject
or add an epistemic or source layer; (iv) ungrammatical frames. (iii)/(iv) are `lexicon.a48h_frame_problems`, called by
`lint_frame`: a frame is "(Is it | Would it be) <truth word> [to say] that" and nothing else. Seeds, dev frames and "Is it false
that" pass it. `build_catalogue(a48h=False)` rebuilds the old 116 (the exact_prog batch id only). Result: seed catalogue 111.

## 10. The frame bank (orchestrator approval, 15 Oct 2026, after A48 (h))

The Haiku drafts left 1 positive and 8 negative training frames and 23 held-out patterns, so neither floor was reachable. Under
A48 (h) the frame space is closed, so `stage2_bank.py` generated the compliant frames not yet drafted BY PROGRAM (10 positive,
14 negative; `stage2/BANK_CANDIDATES.json`, frozen once approved). They are surface wordings only: gold stays program gold, and
admission is decided by the same program checks, G-LEX 2/2 and the pattern exactness read as any drafted frame. Every bank frame
is a training candidate; the held-out slots HF1-4 take the positive ones (3+3+2+2 candidates) and HN3, HN4 the negative ones
(4+4), disjoint slices (`stage2_admit.allocate_bank`); `choose_heldout` + `H.disjoint` then keep the final surfaces disjoint.
Task folders: `haiku/_superseded_a48h/` (first pass) and `haiku/_superseded_a48h2/` (second pass) are never answered;
`tasks.GEN = "a48h2"` seeds the current glex / exact batches (`GEN_CARD = "a48h"`: the card certificates did not change).

## 11. Freeze, guard, RTW and the block builders (stage 3, 15 Oct 2026)

**Freeze** (`stage3_freeze.py`, run once): `TRAINED_CATALOGUE.json` (379 patterns = 111 programmatic + 268 lexicon-based, with the 20
admitted pairs), `lexicon/admitted.json`, `HELDOUT_REALISED.json` (11 chosen surfaces; 33 held-out patterns, 30 complement) and
`FREEZE_A42D7.json` (sha256 of each, counts by class, the chosen map, UTC time). `frozen.load_trained()` re-checks the hash and the
guard; `frozen.guard_patterns` (called by `plan.plan_block`) and `checks.twin_row` refuse any held-out pattern, any pattern that
trains on a held-out frame (the dev frames included) and any pair sharing a word with a held-out pair. Tests: `FrozenGuard`.

**RTW** (`rtw.py`): bases are replay yes/no rows (qtype noul) in `REPLAY` A46 `agreed`, not in the deny / unscreened lists, read from
`data/v14_parts/golden_train.jsonl` (the pool the A46 draw used), hard labels only. 29,899 agreed yes/no rows -> 7,525 bases (core
parses with both parsers, swap-safe two-line card) in 15 sources / 24 base types. Caps are shares of the realised block: one source
<= 10% (spec 3.18; the base-type cap 10% of DESIGN section 5 cannot hold with fewer than 10 types and is implied by the source cap),
one pattern <= 1.2%, one (pattern, core) cell <= 2%, enforced by removal only (`plan.enforce_caps`). A complement twin on a two-line
card needs the base type's card certificate (`cardcert_replay_r1|r2`, 24 types, 2 Haiku reads 'opposite'); without the answers
`rtw build` refuses (nothing half-built is written) and `--preview` prints the all-certified upper bound. T37b overlap: bases already
used by T37b are excluded when `c2_parts/T37b/out/candidates_c2.relations.jsonl` exists (or `--exclude-ids`); rerun the build after
T37b freezes. Open: the antonym share (>= 30% of complements, pooled) cannot come from RTW (replay cores rarely carry an admitted
pair word; 0.5%), and the syntactic share is 58% before `plan.trim_pooled` (needs GB + MD + RTW together).

**GB / MD builders** (`block_twins.py gb|md [--apply]`): the same engine, twins <= 5,000 and base rows + twins <= the block cap (15,000 /
12,000), card-free bases allowed for MD (no card to swap), yes-only cards through the A48 (c) wrap, two-line card types need their own
certificate (`block_twins <b> cardtasks`). `--apply` appends the twins to `out/candidates_c2.jsonl` (idempotent) and updates the MANIFEST /
QC file records; the base QC verdict is untouched.

## 12. RTW build and the pooled audit (16 Oct 2026, first run)

**RTW with 12 of 24 base types certified.** The replay card certificates (`cardcert_replay_r1|r2`) passed 12 of 24 types, so a complement
twin can only come from 6 sources (2,614 bases) while equiv twins come from all 15. With the caps as written (source <= 10%, (pattern, core)
cell <= 2%, pattern <= 1.2% of the block) `plan_block(trim=True)` collapses to 33 rows and a max-flow bound shows no block above about 64
rows exists: the 1.2% pattern cap needs >= 84 live patterns in the block and only 122 are live. The pattern cap is a DESIGN parameter (not in
PREREG A42-D 7 or spec 3.18); the spec's "shares of the POOLED twin set" is the rule the build uses for it: **a pattern holds <= 1.2% of the
pooled twin set (GB + MD + RTW)**. Source <= 10% and cell <= 2% stay on the RTW block itself.

* `plan.plan_flow`: the largest block whose caps hold on its own size, by max-flow (`scipy.sparse.csgraph.maximum_flow`): complement twins
  first (they are the scarce ones), then equiv twins on what the caps leave; the yes share is brought into 45-55% by removal (`balance_yes`).
  Result on this data: 1,916 planned, 1,902 after the schema (token length) check; the 70:30 complement:equiv ratio is not reachable (743 : 1,159).
  `plan_fit` (greedy scan) is kept as `--greedy` (about 40% below the flow bound); the old rule is `--strict-pattern-cap`.
* `twin_table(..., twin_ok)`: the program checks (polarity A/B, A43 f, A48 h, edit site) are applied while planning, so no planned twin is
  dropped afterwards (a drop after the caps were set would break them).
* Successive removal from a block planned exactly at its caps collapses (every removal tightens every share). After the pooled audit drops
  patterns, RTW is therefore **planned again from the surviving catalogue** (`rtw.build(exclude_patterns=...)`); GB and MD (already built)
  only lose rows.

**Pooled audit** (`pooled_audit.py`): ONE Sonnet 3% audit over the twins of GB, MD and RTW (3,671 twins; 171 patterns, one row at least per
pattern = 171 items = 4.7%). Sonnet flags (anything but the expected relation), Opus confirms EVERY flag blind, `tasks.audit_decide` drops
the patterns (> 3% error, or <= 33 audited rows and one confirmed error), `apply` removes them from the three blocks.

**Edit-site check (A48 h (iv), found by the audit).** The audit found twins whose inserted word cuts a noun phrase ("the stated distance to
the is named place", "the action being is judged": the subject boundary of the core was mis-parsed at "named", "being", "used", "listed",
"name", "do"). `checks.bad_edit_site` refuses a twin whose inserted or replaced word lands right after a function word or after "being":
9 of 9 flagged on the audit sample that have the signature, 0 of 151 clean twins, but 11 of the 20 flagged twins are other mis-parses
(verb-noun homographs such as "does not name contain") that the signature does not catch. It is a program refusal (drop only) in
`rtw.twin_checks` (RTW planner) and in `pooled_audit apply` (GB / MD twins).
