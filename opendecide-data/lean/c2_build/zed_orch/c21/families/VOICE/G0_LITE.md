# G0-LITE: VOICE (spoken-utterance variants of existing rows)

Lane L-G. Author: Sonnet 5.5 high. Written Sun 18 Oct 2026. Status: DRAFT for Opus G0-lite approval (Mon 19 Oct).
Read scope used: PLAN_TRAINING_SIDE.md (sections 1, 2, 5, 6, 7, 8, pre-registered rules block), LANE_L-G.md,
excerpts/voice_s6_7.md (stripped). Nothing else.
Design only. No audio, no transcript, no row exists; no model was run; no generated code was executed.
Every identifier in section 10 is a NAME only (for the names-only manifest).

## 0. Summary

About 3,000 kept voice rows. A voice row is an existing mix row (the SOURCE row) whose user-utterance field is replaced by
what the pinned ASR hears after the utterance was spoken by a TTS and passed through an acoustic chain (generator A, about
55 percent), or by a program confusion-table noiser calibrated to the same WER bands (generator B, about 45 percent).
Everything else in the row (actions, diffs, tool outputs, file content, options, policy card) stays exact text. Gold is
inherited unchanged from the source row, and only if every decision-bearing span survives; otherwise the variant is
dropped and logged (drop-only). Every voice row has its clean text twin (the source row) in the mix. Voice rows are
built but stay OUT of the mix manifest until the owner answers R11.

## 1. Decision and label set

VOICE has no label set of its own. The label is the source row's label (option letter or class), inherited unchanged.
The label sets present are the union of the eligible source families (for example the allow/ask/block and
benign/block families, yes/no families, k-way option families). No "ask" label is invented for altered rows. Altered
rows are dropped, never relabelled.

INPUT VIEW: the same view as the source row (primary view: user messages plus tool calls, tool outputs stripped; or the
labelled with-tool-outputs variant). Only the user's spoken utterance field is replaced by the transcript. A source-tag
such as "[transcribed speech]" is NOT added in C2.1 (default; section 8 explains why).

## 2. Gold method and solver A versus solver B

Gold: inherited program or execution gold of the source row. VOICE writes no gold.

What needs two independent implementations (this is the "solver A vs B" of this family):

| Component | A (builder, Sonnet 5.5 high) | B (separate blind Sonnet 5.5 high session) |
|---|---|---|
| Verbalizer (text to spoken form) | rule engine: number forms, symbol table, spelling of code tokens and out-of-vocabulary words | independent DENORMALISER: maps a spoken form back to the written token sequence; round trip must equal the original token for token |
| Span-survival checker | word-level edit-distance alignment between spoken reference and ASR hypothesis, spans mapped through the alignment | character- and phoneme-key matching with its own number-form normaliser and letter-run joiner, no shared alignment code |
| Confusion-table noiser calibration | replay of the table to a WER target per band | independent WER measurement (own edit distance) of the noised text vs its reference |

Rules: B gets this G0-lite and the interface (inputs, outputs), never A's code or tables. Any checker disagreement on a
real candidate row means the row is dropped and logged (drop-only). Verbalizer round-trip mismatch on the CPU test set
blocks the build. A spec ambiguity found by B during the build is a build fix, not the fix iteration.

## 3. Inputs and state model

SOURCE ROWS (eligibility is a program predicate, not a family list):
- Row is already in the training mix (new C2.1 rows through their gates, or C2 replay rows with program or Claude-authored
  gold). C2 replay rows with program gold are available BEFORE any C2.1 family row, so the pool can start from them.
- Row has a natural-language user-utterance field with 10 to 400 verbalized tokens (Kokoro degrades outside; section 7 gate).
- NOT eligible: human-label replay rows (A46), rows whose source family was rolled, rows dropped by G13 or by the OHS-5
  collision rule, rows with no decision-span metadata AND no usable fallback match.
- Each source generator must export `decision_spans` (negation/polarity words, numbers and quantities, and the entities,
  paths, flags, commands the gold depends on) and, where it has them, a `spoken_view` (utterance text, dictated-command
  flag, operation class). Missing metadata: fallback = negation lexicon + all digits and number words + tokens matching a
  path/flag/identifier pattern. This is a request to every training lane, to be routed by L-0 (flagged in section 12).
- GEN rows may serve as sources only for AR-F1, AR-F2 and TM-T1/T2 stems of at most 60 words and no table, capped at
  5 percent of kept voice rows (default include; Opus may switch off).

STATE per candidate variant (all by program, recorded in the run report): source_row_id, variant_id (at most 2 per source),
generator (A/B), stratum, spoken form, voice id, speed, noise condition and SNR, simulated RIR id, codec, band-limit,
gain/clipping, pitch shift, chunk mode (always LOCKED-560-FLUSH), onset clip, trailing padding, raw ASR text, measured
WER, span survival result per span with role, drop reason.

PIPELINE
- Generator A (round trip): verbalizer, then Kokoro-82M with misaki G2P and the espeak-ng fallback DISABLED, then the
  acoustic chain (MUSAN noise at 25/15/10/5 dB or clean, simulated RIRs only, 8 kHz band-limit, low-bitrate Opus or MP3,
  gain/clipping, small pitch shift; convert 24 kHz to 16 kHz mono), then Nemotron EN 0.6B (pinned revision, main as of
  13 Mar 2026) in the LOCKED 560 ms + forced-flush mode. Raw ASR text is recorded exactly as emitted (case,
  punctuation, number form).
- Generator B (noiser): word-level substitution/insertion/deletion table harvested from the pinned Nemotron on
  LibriSpeech TRAIN splits only plus generator A output, aligned by an edit-distance aligner and keyed by phoneme sequence
  (key source: misaki lexicon or CMUdict; the CMUdict licence check is pending, so use the misaki lexicon until cleared).
  Replay on text: P(corrupt) per eligible token CALIBRATED to the WER band targets (not set at 0.10 to 0.20; that is an
  upper bound for the hard tail only), weighted toward closed-class and phonetically close words; operators: dropped
  function words, doubled words, homophones, number-word/digit swaps, merged or split identifiers, missing punctuation
  and case. Never applied to decision-bearing spans unless the span survives the gold check.
- Spoken forms (strata of kept rows): natural-language utterances 75 percent; dictated commands/paths/flags 20 percent
  (half LITERAL, symbol by symbol with our own symbol table; half NATURAL, a rule-based phrase from the operation class and
  target); numbers/IDs dedicated 5 percent (cardinal, digit-by-digit, ordinal, version). Hashes and long IDs spelled letter
  by letter or abbreviated. Rule-based disfluencies (fillers, repeats, false starts, self-repairs, dropped politeness)
  applied to a design rate of 15 percent of rows (my parameter; no source gives a rate).
- Number form: a 100-utterance probe first (digits vs words in the raw ASR). The majority form is recorded; about 15
  percent of numeric spans use the other form (through generator B swaps or literal dictation), measured at 15 plus or
  minus 5 pp.
- Spans survive if: exact token match after normalisation; or number-form equivalent (written and spoken forms, digit
  runs, ordinals, versions); or an entity equal after joining spoken letter runs and mapping spoken symbols through the
  symbol table; or DELETED/garbled (not replaced by a conflicting value) AND the identical normalised span string also
  appears in the row's non-spoken exact fields (recoverable from context). NEGATIONS and POLARITY words are never
  recoverable: if altered or deleted the variant is dropped. A span replaced by a DIFFERENT valid value is altered even if
  the true value is elsewhere in the row.

## 4. Sizes and shares

| Item | Target |
|---|---|
| Pool of variants | 10,000 to 12,000 (sized by the formula below after the 500-row pilot) |
| Kept voice rows | about 3,000; ships at the achieved size if fewer (lane kill rule), floor 1,500 |
| Share of new rows | at most 8 percent (3,040 if new rows are 38,000), computed on the actual new-row count |
| Variants per source row | at most 2 |
| Clean twin | 100 percent: every kept voice row has its source row in the mix (program check at mix time) |
| Generator split | A 55 percent plus or minus 3 pp (about 1,650); B 45 percent (about 1,350) |
| Strata | natural 75 percent (about 2,250); dictated 20 percent (600: literal 300, natural 300); numbers/IDs 5 percent (150); each plus or minus 3 pp |
| WER bands of kept rows | under 3 percent: 30 (900); 3 to 8: 35 (1,050); 8 to 15: 25 (750); 15 to 25: 10 (300); over 25: excluded (0) |
| Chunk mode in training | LOCKED 560 ms with forced flush, 100 percent. 160 ms and 1,120 ms appear only in the 300-utterance dev robustness slice, never in training |
| Voices (generator A) | 15 voices of grade C or better (US female 8, US male 3, UK female 2, UK male 2); no voice above 10 percent of A rows; speed 0.85 to 1.25 |
| Onset/offset | 5 percent clipped at start (0 to 300 ms); the "3 percent with only 0 to 160 ms trailing silence" item of the recipe is DROPPED unless the flush measurement shows it is a reachable product condition (flagged) |
| Source mix cap | GEN at most 5 percent of kept rows; no single source family above 25 percent of kept rows (my parameter) |

Pool sizing formula (program, after the pilot): for each band b, pool_b = target_b / survival_b x 1.1, where survival_b is
the pilot's fraction of variants kept in band b; the dictated stratum uses its own survival (it holds many decision
spans). If the sum exceeds 12,000, the pool stops at 12,000 and the kept size is whatever survives (kill rule).

## 5. Gates

Class key: PK = PRE-FREEZE KILL (CPU, data only). PK-D = PRE-FREEZE data-production gate: needs a GPU run of the pinned TTS/ASR
on od-l4b as data-production components; it uses no trained C2.1 model and writes no label. I treat PK-D as pre-freeze but
its only consequences are drop-only row filters and the achieved-size rule, never a family kill beyond the lane rule
(open point 1 for Opus). PR = POST-TRAINING REPORT. Bars use the plan's numeric near-chance definitions: binary probes
held-out AUC at most 0.55 with 95 percent upper bound at most 0.60; k-way accuracy at most 1/k + 3 pp with bound at
most 1/k + 6 pp. Probe settings: TF-IDF (word 1-2 and char 3-5 grams) plus L2 logistic regression, grouped splits by
source_row_id and source family, cluster bootstrap (2,000 resamples) over source rows for the bound. Confirm rule as in
GEN: a probe over its point bar is re-run once on a fresh sample twice the size; it fails only if the re-run also fails.

| Gate | Class | Numeric bar | When |
|---|---|---|---|
| V-C1 Verbalizer round trip: the B denormaliser recovers the original token sequence from the spoken form | PK | 100 percent of tokens on at least 5,000 program-built test strings that include every symbol of the table, number forms, versions, hashes, camelCase/snake_case, long IDs | before any GPU job |
| V-C2 No OOV leakage: with the espeak-ng fallback off, zero tokens reach the G2P without a lexicon entry or an explicit spelling | PK | 0 leaked tokens in at least 5,000 strings; the espeak-ng binary is absent from PATH during the test; no subprocess spawn | Day 2 (Mon 19 Oct) |
| V-C3 misaki/Kokoro runs end to end on CPU with the fallback off | PK | 100 percent of 500 test strings synthesise without error or silent drop; if not, R11(d) goes to the owner and voice rows wait | Day 2 |
| V-C4 Span-checker test on planted edits: negation deleted/inserted, number altered, entity swapped, number-form equivalents, symbol equivalents, letter-run joins, recoverable deletions, benign word changes | PK | A and B each: recall on planted alterations at least 99 percent with Wilson lower bound at least 97 percent (at least 2,000 planted cases); false-alarm on number-form and symbol equivalents at most 1 percent; A-vs-B agreement at least 99.5 percent | before any GPU job |
| V-C5 Metadata coverage: share of source rows with program-exported spans (not fallback) | PK | report; rows on fallback must be at most 30 percent of kept rows (my parameter) and each fallback row is checked by both checkers | pool build |
| V-C6 Label drift by survival filter: kept vs pool label distribution inside each source family | PK | per class difference at most 3 pp; if a family fails, its rows are re-balanced by dropping kept rows of over-represented classes, never by generating labels | pool build and final |
| V-C7 Surface probes (binary, per source family): predict "majority class" from transcript surface only (case, punctuation, filler count, number form, length, band, generator, voice id) | PK | AUC at most 0.55, upper bound at most 0.60 | pool build |
| V-C8 Size and share: voice at most 8 percent of new rows; at most 2 variants per source; 100 percent clean twin; zero human-label replay sources; generator, strata, band and number-form shares in section 4; no voice above 10 percent of A rows | PK | as listed | pool build and at mix |
| V-C9 Noiser calibration on text: B-measured WER of noised text per band | PK | band shares within plus or minus 3 pp of 30/35/25/10/0 on at least 1,000 noised variants | before pool |
| V-C10 Utterance length: verbalized tokens 10 to 400 | PK | 100 percent; shorter utterances are excluded or routed to generator B only (see V-D4) | pool build |
| V-D1 Number-form probe (100 utterances) | PK-D | records the digit-vs-word share; decision rule: majority form is the one at 60 percent or more; if neither reaches 60 percent, both forms are logged as mixed and the 15 percent minority rule is replaced by the observed mix | first GPU job |
| V-D2 Padding and flush measurement at 560 ms with forced flush: trailing silence in {0, 160, 320, 560, 1,120 ms} on at least 100 utterances | PK-D | choose the smallest padding at which the last three words match the long-padding reference on at least 99 percent of utterances and within 0.5 pp of it; if none reaches 99 percent, voice rows wait and the question goes to Opus and the owner | before the WER pilot |
| V-D3 500-row WER pilot: conditions (SNR, RIR, speed, codec, voice, utterance length) mapped to WER bands | PK-D | every kept band reached by at least 50 percent of its designed count (at least 75, 87, 62, 25 rows); any condition with more than 50 percent of its rows over 25 percent WER is removed; clean-condition median WER at most 3 percent | after V-D1/V-D2 |
| V-D4 Short-utterance check: at least 100 of the 500 pilot rows are under 20 Kokoro tokens | PK-D | if their clean-condition WER exceeds 8 percent, short utterances are excluded from generator A (they may use B) | in the pilot |
| V-D5 Band shares of the kept set by measured per-row WER (whisper-normaliser style) | PK-D | each band within plus or minus 3 pp of 30/35/25/10; over 25 percent excluded 100 percent | pool and final |
| V-D6 Span-survival report: kept %, altered % by role (negation, number, entity, other), mean/median WER per band, voices, chunk size, noise mix | PK-D | report; kept rows at least 1,500 else voice ships at the achieved size | per run |
| V-D7 Consistency of A and B on the same variants: B-measured WER vs reported WER | PK-D | median absolute difference at most 1 pp | per run |
| V-G1 200-row G13 pilot on voice rows (transcript field and whole row), PII scrub, deny-list, OHS-5 collision | PK | more than 1 percent of 200 hit = fix iteration; OHS-5 collision drops row by row, up to 5 percent not the fix iteration | before full pool |
| V-H1 G5-H on voice: two Haiku solvers on 300 kept rows (transcript + twin + gold), plus one Haiku read of 100 percent of the dictated-NATURAL phrase table (the closed phrase pool, not rows) | PK-D with a program tie-break | A flag counts only after Sonnet adjudication, Opus A43(d) confirmation and a checker re-run; fix iteration if confirmed meaning changes that passed the span checker exceed 1.0 percent of 300 (4 rows or more) | pilot |
| P-V0 V0: paired text vs clean TTS-ASR on dev, every run: flip rate with CI, accuracy gap with McNemar, harmful flips (allow where gold denies) separate from over-block flips, ECE text vs speech | PR | report. Proposed thresholds from the research excerpt, to be ruled: accuracy loss at most 3 pp in the 3-8 percent band, at most 6 pp in 8-15 percent, harmful-flip rate at most 1.5 times the text-side false-positive rate, speech ECE within 2 pp of text ECE | after training |
| P-V1 Clean-text loss check (the lane rule): clean-text dev accuracy of the voice-trained candidate vs the same candidate without voice, on voice-source families | PR | proposal: loss above 1.0 pp (one-sided 0.05) removes voice rows from the mix as a drop-only arm decision; needs a no-voice grid point, otherwise compare to init with the plan's 1.5 pp margin. NOT a pre-freeze family kill (open point 2) | after training |
| P-V2 300-utterance dev robustness slice at 160 ms and 1,120 ms chunks | PR | eval only, never trained on; report | after training |
| P-V3 V1 grid at fixed SNR/RIR; flip rate by WER band and by error role; altered-span rate; operating-point stability | PR | report; labelled "TTS-based, an upper bound" | after training |
| P-V4 V2-lite: real-speech set from C1 VOICE_REAL, re-read on C2.1 if its recorded consent/licence covers the use (Haiku reads the record, Opus confirms by Sun 25 Oct), n and Wilson CI stated; registered as a G13 target; never trained on | PR | if consent does not cover it: "not measured in C2.1" | after training |
| P-V5 Altered-row stress set (dev only; sources are training-pool rows, so labelled "training-pool stress, not generalisation") | PR | report | after training |
| P-V6 Source-tag A/B and code-symbol ITN question | not run in C2.1 | tag default is NO; both questions move to C2.2 because they need training runs; the dictated stratum is marked in metadata so a later slice can compare | n/a |

## 6. Clean-room notes

- No external audio or text enters training except as machine inputs: LibriSpeech TRAIN splits (CC BY 4.0) for the table
  harvest only (never test-clean or test-other, never as rows), MUSAN noise (CC BY 4.0), OpenSLR 28 simulated RIRs only
  (no recorded RIRs). Nemotron was trained on LibriSpeech (vendor card), so the harvested table understates real error;
  the report says so.
- Chatterbox, Piper, F5-TTS, XTTS, Dia and Parler-TTS are not used. Kokoro-82M is the only TTS (R11(b)). The NVIDIA Open
  Model License for Nemotron is R11(c). ASR transcripts as training inputs is R11(a). Default per plan: allow all three.
  Until the owner answers, rows may be built but stay OUT of the mix manifest.
- No LLM writes any transcript. The natural dictated-command phrase table and the disfluency rule tables are closed,
  Claude-authored (Haiku medium for wording), hashed, and re-exported at every change.
- Names inside utterances come from source rows (already from the TRAINING-salt namespace). The verbalizer spells any
  out-of-vocabulary word and every code token letter by letter, so no random-namespace name depends on the espeak fallback.
  The checker joins spelled letter runs back to the entity before comparing.
- No eval set, no speech benchmark item, no VoiceBench or SD-QA clip is read, copied or used as data.
- No model output of a competitor is used. Nemotron is the product's locked input component, not a competitor, and writes
  no label.

## 7. Risks

1. R11 not answered by the freeze: voice built but not in the mix. Kill rule below handles size, not the licence.
2. misaki cannot run with the fallback off: voice waits; R11(d).
3. TTS speech is easier than real speech: all voice results are "upper bound" and V2-lite may be unavailable.
4. Survival filtering shifts labels (negations die most) and removes hard cases: V-C6 and V-C7.
5. Dictated stratum has many decision spans, so survival is low; the 600-row target may be missed; the stratum share gate
   then stops at the achieved size rather than relaxing the span check.
6. Short utterances degrade Kokoro (V-D4). Long ones too (V-C10).
7. Flush and padding at 560 ms is UNMEASURED; mis-padded training audio would mismatch the product (V-D2).
8. Nemotron ITN behaviour unknown (V-D1). Both written forms are present only by design.
9. LoRA robustness training can cost clean accuracy (HIVE, author-run): clean twins in the mix; P-V1.
10. Throughput of od-l4b for 10 to 12K variants is unknown; L-0 measures rows per hour by Wed 21 Oct; voice is queue
    priority 4 and the second item shed at 90 percent usage.
11. The pool starts from C2 replay rows and then grows as C2.1 families pass; if a source family rolls after its
    variants are built, those variants are dropped (twin missing); the count is logged.
12. Generator B's table is harvested from Nemotron on real speech and may reproduce the training-set favourable errors.
13. Decision-span metadata is not yet exported by any generator I can see; fallback regex is coarser and may keep an altered
    span that the regex missed. Mitigation: V-C5 cap and double checking by both checkers.

## 8. Decisions made now (so no pilot decides them later)

- No source tag in the prompt for voice rows (the recipe says "test, do not assume"; a test needs a training run, so it
  moves to C2.2).
- Raw spoken-form symbols are NOT converted to code symbols before the model in training; the dictated stratum is
  metadata-tagged for a later ITN comparison.
- All training voice rows use the LOCKED 560 ms + forced-flush mode.
- Records of every run: pinned revision hashes (TTS, G2P, ASR, normaliser, aligner), image ids, seeds, config sha.

## 9. Order of work (design items)

- Sun 18: this file; list of NAMES (section 10) to L-0.
- Mon 19: Opus approval; verbalizer + B denormaliser + span checkers A/B (CPU code); V-C1, V-C4 CPU tests; Day 2 CPU test
  V-C2/V-C3 (misaki, fallback off).
- No od-l4b voice job until C2's grid reads finish. Then V-D1, V-D2, V-D3/V-D4 pilot, V-C9 table harvest, noiser
  calibration, pool, 200-row G13 pilot, G5-H, full pool, final gates.
- Voice rows enter the mix manifest only after R11, after the span, probe and G13 gates, and after Opus confirms.

## 10. NAMES for the names-only manifest (names only)

```
FAMILY: VOICE
POLICY_CARDS: none (inherits source rows; source families' cards are on their own lists)
TOOLS_IN_ROWS: none (only the user utterance field changes)
LANGUAGES_RUNNERS_IN_ROWS: none
DOMAINS: none of its own (inherits source rows)
NAMESPACE: NS-TRAIN (inherited from source rows)
CARRIERS (spoken-field strata): V-NL, V-DICT-LIT, V-DICT-NAT, V-NUM
GENERATORS: VGEN-A (round trip), VGEN-B (confusion-table noiser)
CHUNK_MODE: LOCKED-560-FLUSH (training); DEV-ONLY: CHUNK-160, CHUNK-1120
TTS: Kokoro-82M (Apache-2.0); G2P: misaki with espeak-ng fallback DISABLED
TTS_VOICES (grade C or better; grades re-read by Haiku from the pinned VOICES.md at pin time):
  af_heart, af_bella, af_nicole, af_aoede, af_kore, af_sarah, af_alloy, af_nova,
  am_fenrir, am_michael, am_puck, bf_emma, bf_isabella, bm_fable, bm_george
VOICES_EXCLUDED: am_adam and every voice graded D or lower
ASR: Nemotron Speech Streaming EN 0.6B (NVIDIA Open Model License), revision = main as of 13 Mar 2026, hash recorded at pin time
ACOUSTIC_CHAIN: audiomentations (MIT); MUSAN noise subset only (CC BY 4.0); OpenSLR 28 SIMULATED RIRs only;
  SNR set {clean, 25, 15, 10, 5} dB; 8 kHz band-limit; codecs Opus and MP3 at low bitrate; gain/clipping; small pitch shift
HARVEST_CORPUS: LibriSpeech train-clean-100, train-clean-360, train-other-500 (CC BY 4.0). NEVER dev/test splits
G2P_KEY: misaki lexicon (CMUdict only after its licence check)
METRIC_TOOLS: whisper-normaliser-style text normalisation, edit-distance aligner (own code; any third-party package licence re-verified by L-0 before use)
TABLES (own, closed, hashed): symbol table, number-form table, disfluency rule table, dictated-NATURAL phrase table, verbalizer rules
SOURCE_FAMILIES (eligibility only, no names added): any family with a NL user utterance; GEN forms AR-F1 AR-F2 TM-T1 TM-T2
```

## 11. Fix iteration and kill rule

- One fix iteration. Triggers: V-G1 more than 1 percent hit; any PK/PK-D gate failing after its normal tuning
  (verbalizer rules, noiser calibration, condition map, padding value); V-H1 confirmed meaning changes above the bar;
  OHS-5 collisions above 5 percent of voice rows. A fix may change tables, conditions, calibration or the padding; then
  hash export, pilot, G13 pilot and all gates re-run.
- Lane kill rule (plan): if the span-survival drop leaves fewer than 1,500 kept rows by the data freeze (Mon 2 Nov
  23:59 UTC), voice ships at the achieved size. If V0/P-V1 shows a clean-text loss on dev, voice rows are removed from
  the mix (drop-only). Voice is the second item in the 90 percent usage shed order.
- If a PK gate still fails after the fix iteration, VOICE rolls to C2.2 with the gate and numbers logged. If V-C3 fails
  (misaki cannot run with fallback off), voice waits for the R11(d) answer.
- Voice never counts in the 6-of-9 P0 floor.

## 12. Open points for Opus

1. PK-D is my third label for gates that need the pinned TTS/ASR on the L4 (data-production only, no trained C2.1 model,
   no label). If skeptic-6 means "CPU only", V-D1 to V-D7 become measurements with no kill force and the lane rule
   (achieved size) is the only consequence. Either way they never kill a P0 family.
2. P-V1 (clean-text loss) is POST-TRAINING by nature yet the lane rule gives it removal power. I made the removal a
   drop-only arm decision at candidate selection, not a pre-freeze kill. Needs a no-voice grid point; Opus to rule.
3. Each training lane must export decision_spans and an optional spoken_view from its generators (L-0 to route). Without it
   the fallback regex covers the source rows.
4. The recipe's "3 percent with only 0 to 160 ms trailing silence" is dropped pending V-D2.
5. Proposals with no source: disfluency rate 15 percent, fallback-span cap 30 percent, per-family cap 25 percent,
   GEN cap 5 percent, pitch-shift range, V-D3 reach threshold of 50 percent of design counts.
6. Thresholds in P-V0 are the research excerpt's proposals and still need a ruling.


---

## Opus rulings 18 Oct (copied word for word from families/G0_APPROVALS.md by the lane builder, Sun 18 Oct 2026; the build skeptic checks the code against this addendum; where the body text above says otherwise, this addendum binds)

### Global rulings G1-G10 (bind every family)

G1 SOLVER B IS A PROGRAM. In every family, "solver B = separate Sonnet session" means CODE written by a separate Sonnet
high session from the G0-lite (and the row schema) only. No LLM reads rows one by one to produce or check labels. LLM
reads (G5-H, G3-H, A43(d)) are audits: they never set or change a gold label. A confirmed defect is fixed in the generator
or the rule table, never by relabelling a row.

G2 DATA-AUDIT GATES ARE PRE-FREEZE. A50 G6, A49c, G5-H, G3-H and A43(d) read data, not a trained C2.1 model, so they are
PRE-FREEZE gates under the standard pipeline. Skeptic 6 bars only gates that need the TRAINED model. A G5-H flag counts
only after Sonnet medium adjudication and Opus A43(d) confirmation, and (where the family has a program solver) after a
program re-run reproduces it. Their bars are the values in the A50/A49c/G5-H/G3-H records, supplied by L-0. (Answers T50
O4, T51 O3, T53 O4, T41c O6, the T54/T55/T56 flag, GEN point 2, VOICE V-H1.)

G3 NO FREE PILOT TUNING. The 1,000-row pilot is the first measured look at every PRE-FREEZE gate. Run the family's CPU
gates and its 200-row G13 pilot on that first pilot, then make ONE combined fix if anything fails: that is the fix
iteration. Changing generator parameters after seeing pilot gate numbers and "re-running for free" is not allowed. Before
the pilot, defects found by unit tests, the build skeptic or solver A/B disagreement on CPU test fixtures are build fixes.
The plan's two exemptions stay (scaffolding-only G13 hits; OHS-5 collision drops up to 5%). (Answers T42c (d), T57 (f),
T56g (f).)

G4 KILL GRANULARITY. P0 families are killed or kept as a whole (plan section 8). The only split the plan names is T56
(done-claim half) / T56g. No sub-block or head "rolls alone" in C2.1. If an orchestrator wants that, it is a plan change
for the orchestrator, not a G0-lite choice. GEN (not a P0 family, no floor) may roll sub-blocks alone (GEN point 3
approved). VOICE keeps its lane rule. (Answers T54 item 7, T55, T56, T57 (g).)

G5 ONE PROBE HARNESS. L-0 builds one CPU probe harness for all families, and every family uses it with its own features
and groups:
- grouped split by the family's pair/spec/module/task group (no group in both train and held-out);
- L2 logistic regression with fixed or inner-CV regularisation (never tuned on held-out);
- AUC is reported as max(AUC, 1 - AUC);
- the upper bound is the 97.5th percentile of 2,000 cluster-bootstrap resamples over held-out groups (the stricter
  reading of "95% upper bound"; T50, T51 and T53 change from the one-sided 95th percentile);
- k-way probes use balanced accuracy (mean per-class recall) against 1/k + 3 pp and 1/k + 6 pp;
- every probe run includes a label-permutation sanity check (AUC 0.50 +- 0.03) and an injected-leak power check (as T41c
  K7: a planted one-feature leak must reach AUC >= 0.80), else the run is invalid and is repeated (not a fix iteration).
GBT probes are advisory in every family except GEN, where both probe models count as written (a GEN gate passes only if
both pass). The GEN/VOICE "confirm rule" (one re-run on a fresh sample twice the size, and the re-run decides) is
approved for GEN and VOICE only, because they run about 40 probes each. It is recorded and is not a fix iteration.

G6 TOKEN RULE READING. Mean <= 800 tokens per family; no row above 1,536; rows above 1,024 tokens <= 10% of the family.
T50 and T41c change their 1,000 line to 1,024.

G7 SECONDARY HEADS. The loss is on option letters and C2's layout is kept (plan section 5). A secondary head (T50
reason+tier, T53 reason+tier, T56 reason, T57 reason) is built as HEAD ROWS: the same rendered context with a separate
question form and its own lettered options, gold from the same rule table, in the same split as its primary row. Head
rows are extra copies outside the family size and come from at most 25% of the family's specs per head. They get the
family's k-way probe bars. If L-0 finds that C2's layout cannot carry a second question form, the head stays a manifest
field plus a report line. No new output token or suffix field is added. T51 violation_set stays metadata only (O1).

G8 SHARED NAMES. L-0 keeps ONE host-TLD list and ONE raw-IP pool in the names-only manifest, used by T50, T51, T53 and
T41c alike: reserved TLDs plus a generic list, and documentation/private IP ranges, with the deny-list collision check
against real brands and registered names. T41c moves from its reserved-only list to the shared list. This keeps the
families from showing a "which family am I" cue.

G9 CROSS-FAMILY LABEL CONSISTENCY. The same action in the same state under the same card must get the same label in
every family. L-A owns ONE shared effects-to-label table (in T50/G0_LITE.md section 3) that T51 and T53 cite instead of
restating their own rule. A CPU test runs every T50 spec whose effect class overlaps T51 (shared/production-lane mutation)
or T53 (egress) through the other family's engine and asserts equal labels. It must pass 100% before any pilot. T41c is a
carrier-directive decision, not an action gate, so it is not in this test, but its HARD/SOFT list must not contradict the
shared table (spot-checked by the L-I build skeptic).

G10 VOICE METADATA EXPORT. Every family with a natural-language user utterance (T50, T51, T53, T41c, T54, T55, T56 task
statements, GEN voice-eligible forms) exports `decision_spans` with a ROLE per span. Roles: negation/polarity, number,
entity/path/flag, and AUTHORITY. AUTHORITY marks any span whose presence in the user turn creates or limits permission:
consent naming, scope declarations, boundaries, delegation pointers, values whose source is the user turn. Families also
export `spoken_view` where they have one. L-0 routes this. It is a code requirement, not a gate.

### VOICE: APPROVE

Binding conditions:
- C1 Context-recoverable span exception: OFF by default. A deleted or garbled span counts as surviving only if (a) its
  role is not AUTHORITY (G10), and (b) re-running the SOURCE family's gold function on the structured spec, with that span
  removed from the user turn, gives the same label. That is a program check, and the row is dropped if the label
  changes. Reason: in T50 consent twins, T51 scope rows, T53 naming twins and T54 ASK-vs-CALL rows, whether the user SAID
  the value is what decides the label, even when the same string appears elsewhere in the row. Rows on the fallback
  regex (no exported spans) never use the exception.
- C2 P-V1 is a POST-TRAINING REPORT line with no removal power in C2.1. C2.1 has one Modal run and no no-voice grid
  point, and removing rows after training means retraining. The orchestrator decides whether the lane rule ("clean-text
  loss removes voice") needs a no-voice arm in the grid or moves to C2.2. This is flagged to the orchestrator.
Rulings: 1 PK-D gates are approved as pre-freeze data-production gates with drop-only and achieved-size consequences
(they use no trained C2.1 model). 3 decision_spans export is required of every lane (G10). 4 the 0-160 ms trailing-silence
item is dropped pending V-D2. 5 the author's parameters (15% disfluency, 30% fallback cap, 25% per-family cap, 5% GEN
cap, 50% V-D3 reach) are approved as fixed design values. 6 the P-V0 thresholds are pre-registered amber report
thresholds, not gates and not claims. Voice rows stay OUT of the mix manifest until the owner answers R11 (plan section 7).
Note: L-0 re-checks the licence of the misaki lexicon data as well as CMUdict before the first TTS job.

### Round 2 lines for VOICE (verbatim)

- All 8: "Solver B = separate Sonnet high session" means CODE written by that session (G1).
- VOICE: P-V1 has no removal power in C2.1 (C2). C1: the context-recoverable span exception is OFF by default.
