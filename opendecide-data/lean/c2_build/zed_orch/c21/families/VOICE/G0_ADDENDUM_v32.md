# G0 ADDENDUM v3.2: VOICE (spoken-utterance variants of existing rows)

Lane L-G. Author: Sonnet 5.5 high. Written Sun 18 Oct 2026 (UTC). Status: DRAFT for Opus batch 1 (Mon 19 Oct), with the
other v3.2 G0-lites and addenda. Design only: no audio, no transcript, no row, no model run, no code executed.
Read scope used: C2_1_BUILD_ORDER.md (L-G lane block and v3.2 additions), C2_1_PLAN_v3.md sections 1, 2, 5, 6, 7, 8, 16 and
the PRE-REGISTERED RULES block of section 3 only, C2_1_EXTRA_LEVERS.md section 1 (A18 and the other ADOPT NOW rows),
VOICE/G0_LITE.md, families/G0_APPROVALS.md, PREREG_FINAL.md blocks A77, A79, A82 (read only). Not opened: any "ohs" or
"sealed" path, OHS5_BRIEF_DRAFT.md, any C2 file, data/, logs/, ~/.claude, any T27 / T40-T46 / T42 / T43 generator, any
benchmark item text, any speech benchmark clip.
RELATION TO THE G0-LITE: VOICE/G0_LITE.md (with its appended "Opus rulings 18 Oct") stays in force. Where this addendum
differs, this addendum binds, and it needs Opus approval (batch 1). Every identifier in section 11 is a NAME only.

## 0. What this addendum changes (one paragraph)

(1) R11 is DECIDED (A79): ASR transcripts as training inputs, Kokoro-82M, the NVIDIA Open Model License for Nemotron and the
espeak-ng fallback OFF are all allowed, so voice rows may enter the mix after their gates and Opus confirmation (the G0-lite
line "stay OUT of the mix manifest until the owner answers R11" is superseded). (2) A18: a THIRD program generator C
(rule-based phoneme-neighbour word swaps from a pronunciation dictionary) joins INSIDE the 3,000-row pool (0 extra rows), after
a dictionary-licence check. (3) OWNER RULE (18 Oct): every voice variant is answer-checked and G13-stamped when it is made,
through the stamp wrapper; the 200-row G13 pilot (V-G1) is gone; sources must carry a current clean stamp; set-level checks
run once on the pilot pool and once on the built pool. (4) The difficulty ladder is the WER band table (report-only bar).
(5) The conformance items of section 10, the v3.2 shed positions and the money-shed step (section 12).

## 1. Generator C (A18) [LEV A18; plan 7]

Purpose: an ASR-INDEPENDENT hedge beside generators A (round trip through the pinned Nemotron) and B (confusion table
harvested from Nemotron). Real speech will come from other ASR behaviour than the pinned model's training-favourable errors.
Expected effect: +0 to +2 pp on real-speech decision-unchanged rate (DERIVED; C1 measured 89%, goal >= 97%); not a claim.

DESIGN (code written by the lane builder; checker B written by the separate Sonnet high session of the G0-lite section 2)
- Dictionary: a pronunciation dictionary that passes the LICENCE CHECK (MIT / Apache / BSD / CC0 / CC BY / CC BY-SA only; any NC or ND
  term, GPL / LGPL or unknown licence = not used) [Opus b1 VOICE-M1]. Candidates: the misaki
  lexicon data and CMUdict; L-0 already re-checks both before the first TTS job (G0_APPROVALS VOICE note). Generator C uses
  whichever passes; if NEITHER passes, generator C is OFF, the pool stays A 55% / B 45% as in the G0-lite, and this is logged.
- Phoneme key per word; NEIGHBOUR = a word whose phoneme sequence differs by exactly one phoneme (substitute, insert or
  delete), same or +/-1 syllable count; HOMOPHONE = identical key. Operators: PN-SWAP (word to a phoneme neighbour),
  HOMOPH-SWAP (word to a homophone), BOUNDARY-SHIFT (a two-word span replaced by a two-word span with the same phoneme
  string, from the dictionary only). No operator uses a model.
- Corruption rate: P(corrupt) per eligible token is CALIBRATED by a program loop on text so the measured WER of the noised
  text falls in the band table (30 / 35 / 25 / 10 / 0 for < 3 / 3-8 / 8-15 / 15-25 / > 25 percent), NOT set at a fixed
  0.10-0.20. WER is measured by checker B's own edit distance (not generator code).
- Never applied to decision-bearing spans unless the span survives the gold check (same rule as B). Strata: natural
  utterances and dictated-NATURAL phrases only; dictated-LITERAL (spelled symbol by symbol) and numbers / IDs strata are not
  touched by C (spelled forms have no word neighbours).
- Eligible sources, span rules, label inheritance and the clean twin are exactly those of the G0-lite. Gold is inherited and
  drop-only.

SIZES BY SUBSTITUTION (kept pool stays about 3,000; floor 1,500; at most 8% of new rows; at most 2 variants per source):
| Item | G0-lite | Now |
|---|---|---|
| Generator A (round trip) | 55% +/- 3 pp (about 1,650) | 50% +/- 3 pp (about 1,500) |
| Generator B (confusion-table noiser) | 45% (about 1,350) | 30% +/- 3 pp (about 900) |
| Generator C (phoneme-neighbour swaps) | none | 20% +/- 3 pp (about 600) |
| Strata, WER bands, voices, chunk mode, source mix cap | as G0-lite section 4 | unchanged (strata 75 / 20 / 5; bands 30 / 35 / 25 / 10 / 0; LOCKED 560 ms + forced flush; GEN <= 5%; no family > 25%) |

Gates for generator C:
| Gate | Class | Numeric bar | When |
|---|---|---|---|
| V-C11 Dictionary licence | PK | licence record (quote, URL, fetch date) shows MIT / Apache / BSD / CC0 / CC BY / CC BY-SA (no NC, no ND) for the dictionary actually used; else C is OFF [Opus b1 VOICE-M1] | before any C code touches the data |
| V-C12 Phoneme-key coverage | PK | >= 98% of eligible tokens have a dictionary key or are routed to letter-spelling; the rest are never swapped | pool build |
| V-C13 Neighbour validity | PK | 100% of swaps recomputed by checker B's own phoneme edit distance are within 1 phoneme (PN-SWAP), identical key (HOMOPH-SWAP) | every variant (at creation) |
| V-C14 Band calibration of C on text | PK | B-measured WER band shares within +/- 3 pp of 30 / 35 / 25 / 10 / 0 on at least 1,000 noised variants of C alone | before the pool |
| V-C15 Swap-class mix | PK | share of swaps on closed-class words within +/- 10 pp of generator B's share, so C is not a new artefact | pool build |

## 2. R11 decided: mix entry rule [A79 R11]

Voice rows enter the mix manifest when ALL hold: (i) every PK and PK-D gate of the G0-lite and of this addendum passes at the
set level; (ii) an Opus 5.5 high confirmation record exists (plan 7); (iii) each kept voice row has its clean text twin in the
mix and a current clean stamp for both rows (program check at mix time); (iv) voice <= 8% of new rows; (v) no human-label
source (A46) and no L-R row as a source (they carry human labels and their utterances would have fallback spans only).
The four sub-decisions are recorded as decided: (a) ASR transcripts as training inputs, (b) Kokoro-82M as the only TTS, (c) the
NVIDIA Open Model License exception for Nemotron, (d) espeak-ng fallback DISABLED (V-C2, V-C3 still prove it on CPU on
Day 2; if misaki cannot run with the fallback off, voice waits and the question goes to the orchestrator; the owner has
already ruled the fallback stays off). Claims remain "English only".

## 3. Check at generation (OWNER RULE) [OWNER-ROW; plan 16.1 steps 0, 2, 3, 4, 5, 6, 7]

Owner, 18 Oct: "If you're building one row, check that row at that same point and that's it ... then train."
Every voice variant is written ONLY through the stamp wrapper, in batches of at most 500 rows, the same day.

| Step | What runs on THIS variant | Pass rule |
|---|---|---|
| (a0) Source eligibility | the source row carries a CURRENT clean stamp (registry sha and method-set version); it is a program- or execution-gold row (not human-label, A46); its family is not rolled; if it is a C2 replay row it comes from the replay pool AFTER the one-time clean-up (plan 16.1 step 5; done by Mon 26); not an L-R row; verbalized length 10-400 tokens | 100% (program); a source that fails never produces a variant |
| (a1) Verbalizer round trip | the independent denormaliser (B) maps the spoken form back to the written token sequence for THIS utterance (not only for test strings) | token-for-token equal, else drop |
| (a2) Span survival A = B | both span-survival checkers (word-level alignment in A; character / phoneme-key matching in B) say every decision-bearing span survived; NEGATIONS and POLARITY words are never recoverable | both agree, else drop and log (role, source family) |
| (a3) Context-recoverable exception (C1) | OFF by default: a DELETED or garbled span counts as surviving only if (i) its role is not AUTHORITY (G10) and (ii) re-running the SOURCE family's gold function on the structured spec with that span removed from the user turn gives the same label; rows on the fallback regex never use it. Config flag `ctx_recoverable_enabled` is False in C2.1 until Opus rules (open point 1); with the flag False every deleted or garbled decision span drops the variant | program check; label change drops the row |
| (a4) Generator-specific | V-C13 (C) ; for A the raw ASR text recorded exactly as emitted; for B the aligner's own check of the substitution list | as listed |
| (a5) Token rule G6 and WER band | row <= 1,536 tokens; the measured per-row WER (checker B's edit distance, whisper-normaliser style) is in a kept band (< 25%) | else drop |
| (a6) PII scrub and guards | transcript field and whole row: PII scrub drop-only, plan section 2 guards, deny-list | a hit drops the row |
| (b) G13 stamp | the transcript field AND the whole row are sent to the stamp service and checked against EVERY registered target with every method listed for that target (R6 scaffolding exemption; OHS-AC binding for new rows; OHS-5 hash export from Sat 24 with the separate hash-export salt) | clean, else drop; log row id, target name, method only |
| (c) manifest stamp | variant id, source row id, source stamp ref, generator (A/B/C), registry sha, method-set version, code sha, table hashes, verdict | written; the mix guard refuses a voice row whose twin is missing or whose stamp is stale |

RULES AROUND THE WRAPPER
- No unstamped or failed variant enters the pool. A late target runs only the delta targets (step 6); a table or phrase-pool
  change after hash export v1.1 means a new hash export and re-made variants for the changed table.
- STAMP WRAPPER on voice rows is the same service as for text rows; GPU steps (TTS, ASR) run on od-l4b as data-production
  components and write rows only after the wrapper has accepted them. Queue priority 4; no voice job until C2's grid reads end.
- The 500-row WER pilot (V-D3) is generated through the wrapper; its kept rows are pool rows ONLY if their condition
  (voice, SNR, RIR, codec, speed) is in the FINAL condition map; otherwise they are dropped with reason "condition removed".
- FIX TRIGGER (plan 16.1 step 3), read on ALL pilot rows and on each pool day: more than 1% of variants dropped by the G13
  stamp for a reason other than exempt scaffolding or OHS-5 collisions (<= 5% of voice rows are collisions dropped row by
  row and are NOT the fix iteration) = the ONE combined fix (G3). Span-survival and verbalizer drops are NOT fix triggers
  (they are the design filter, drop-only); they are reported by role and set the pool-sizing formula.
- SET-LEVEL checks run ONCE on the pilot pool (first look) and ONCE on the built pool, never again at the mix: V-C6 label
  drift, V-C7 surface probes, V-C8 size / share, V-C9 and V-C14 noiser calibration, V-D5 band shares, V-D6 span report, V-D7
  A-B consistency, V-H1 (G5-H) with Sonnet adjudication and Opus A43(d). The confirm rule stays.
- The binding G13 at the freeze is the one confirming pass (stamp audit + exact / hash re-run on every mix row + fuzzy on
  delta targets); VOICE adds nothing.

## 4. Gate changes against the G0-lite

| G0-lite gate | Change |
|---|---|
| V-G1 (200-row G13 pilot) | REMOVED; replaced by step (b) on every variant and the fix trigger above |
| V-C1, V-C4 | unchanged bars (CPU tests before any GPU job); in addition (a1) and (a2) run on every variant at creation |
| V-C2, V-C3 (misaki / Kokoro with the fallback off) | unchanged bars; R11(d) is decided, so a failure blocks voice and is reported to the orchestrator, not to the owner |
| V-C5 metadata coverage | fallback rows <= 30% of kept rows (fixed design value, ruling 5) and each is checked by both checkers; fallback rows never use (a3) |
| V-C6, V-C7, V-C8, V-C9, V-D5, V-D6, V-D7, V-H1 | bars unchanged; ONCE on the pilot pool and ONCE on the built pool; V-C7 now includes generator id (A / B / C) among the surface features; V-C9 is read per generator (A, B, C) |
| V-D1 to V-D4 | unchanged (PK-D data-production gates, approved by ruling 1: drop-only and achieved-size consequences only) |
| V-C8 | adds: generator split A 50 / B 30 / C 20 percent each +/- 3 pp (C absent if V-C11 fails) |
| P-V0 thresholds | pre-registered amber REPORT thresholds, not gates, not claims (ruling 6) |
| P-V1 | POST-TRAINING REPORT with NO removal power in C2.1 (C2). The orchestrator decides whether a no-voice grid arm is added or the rule moves to C2.2. If voice enters the mix and no no-voice arm exists, the P-V1 line compares to init with the plan's 1.5 pp margin |
| P-V3 | adds a per-generator line (A, B, C) so the ASR-independent hedge is visible: decision-unchanged rate by generator (TTS-based, an upper bound) |

NEW
| Gate | Class | Numeric bar | When |
|---|---|---|---|
| VW-1 Stamp coverage | PK | 0 pool rows without a current clean stamp for the variant AND its twin (CPU test) | every batch |
| VW-2 Source stamp currency | PK | 100% of sources carry a current clean stamp; replay sources only after clean-up | every variant |
| VW-3 Conformance record signed | PK (process) | signed record for the current code sha and ruling sha before the wrapper accepts voice rows | before any row |
| VW-4 Ladder report | PR | C2 decision-unchanged rate and accuracy on L4 (WER 15-25%) voice rows next to the clean twins | after pilot; report only |

## 5. Difficulty ladder [CRIT D1, D2; plan section 1 E]

For VOICE the program parameter IS the WER band: L1 < 3%, L2 3-8%, L3 8-15%, L4 15-25%; bands > 25% excluded. L3 + L4 = 35% of
kept rows (>= 25% required: met by design). Secondary ladder parameters: stratum (natural, dictated-NATURAL, dictated-LITERAL,
numbers / IDs) and decision-span count per utterance. The mandatory quad is not used (not a gate family). The measured bar
"C2 <= 70% on L4" is a REPORT line for VOICE (VW-4), not a parameter-raising trigger: band shares are fixed by the plan and
voice accuracy is bounded by the source row's difficulty (open point 2).

## 6. ADOPT NOW levers and this lane (A1-A36; plan 16.2)

| Lever | VOICE |
|---|---|
| A18 voice generator C | CARRIES (section 1); stays inside the 3,000 pool; dictionary-licence check first; WER-band match; drop-only gold |
| A1 template-level gold-bug audit | applies to the SOURCE families; VOICE passes through `source_row_id`, `source_family` so a dropped source template drops its variants |
| A2 AFLite-style filter | AVAILABLE as a repair inside the ONE combined fix for a failed V-C7 surface probe (CPU features; filtered <= 30% of the pool; band and strata shares kept) |
| A10, A12, A13-A16, A3-A9 | not VOICE (gate-lane row types); voice transcripts are NOT character-perturbed (A12 is for text-bearing gate lanes; ASR noise is the perturbation here) |
| A11 canonicaliser | product wrapper; no voice effect |
| A17 multilingual | NOT ADOPTED (A82 9): English only |
| A19-A29, A30-A36 | recipe, reporting, serving; VOICE supplies metadata (`generator`, `band`, `stratum`, `chunk_mode`) |
| A21 length coverage | not a VOICE item (utterances 10-400 tokens); transcripts enter the L-0 histogram as part of the mix |

## 7. Sources and the clean twin (clarifications)

- The pool starts from C2 replay rows only after the replay clean-up (Mon 26); before that, the first sources are new C2.1
  rows that passed their stamps (families through pilots from Sun 25-Mon 26). GEN stems (AR-F1, AR-F2, TM-T1 / T2, <= 60
  words, no table) stay <= 5% of kept voice rows; TP and HX forms are NOT voice sources.
- If a source family rolls, or a source row is dropped from the mix by selection or the confirming pass, its variants are
  dropped with reason "twin missing"; the count is logged. A variant never outlives its twin.
- The decision_spans export (G10) is required of every lane; roles: negation / polarity, number, entity / path / flag,
  AUTHORITY. The AUTHORITY role is never covered by a recoverable-span rule.

## 8. Timeline [plan 16.7]

- Sun 18: this addendum; NEW NAMES (section 11) to L-0b.
- Mon 19: Opus batch 1; names freeze v1.1. Day 2 CPU tests V-C2 / V-C3. Verbalizer, denormaliser and span checkers A / B
  (CPU code, tests V-C1 / V-C4). Generator C code only after the dictionary-licence record exists.
- Tue 20 - Sat 24: dictionary-licence record (L-0), table hash export, conformance map in a separate fresh session.
- Sat 24 18:00: conformance and stamp-service sign-off, or voice rows wait.
- Sun 25 - Mon 26: replay clean-up ends; od-l4b voice jobs only when higher-priority jobs are done (expected from about Mon 26):
  V-D1, V-D2, then the 500-row WER pilot through the wrapper; set-level gates on the pilot pool; ONE combined fix.
- Tue 27 - Thu 29 12:00: pool and built-pool gates; Opus confirmation; Thu 29 12:00 declaration; freeze per the orchestrator.

## 9. Fix iteration, kill rule and shed positions (v3.2)

- ONE combined fix (G3). Triggers: the section 3 fix trigger; a PK / PK-D gate failing at the pilot pool after normal
  parameter setting (verbalizer rules, calibration, condition map, padding value, dictionary choice); V-H1 confirmed meaning
  changes above the bar (4 rows or more of 300); OHS-5 collisions above 5%. A fix may change tables, conditions,
  calibration, padding or switch generator C off; then hash export and the set-level gates run again.
- Lane rule (unchanged): if span-survival leaves fewer than 1,500 kept rows by the declared data freeze, voice ships at the
  achieved size; a clean-text loss on dev removes voice rows from the mix as an arm decision only through the orchestrator's
  ruling (P-V1 has no removal power in C2.1). A PK gate failing after the fix rolls VOICE to C2.2 with the gate and numbers
  logged. VOICE never counts toward the 6-of-9 floor.
- USAGE SHED (plan section 8, v3.2): research pass and tasksource scouting first, wave-C P1 second, VOICE POOL THIRD (the
  G0-lite said second), then open tier-C L-R datasets, general rows, remaining L-R, remaining lanes.
- MONEY SHED (plan 16.7): step 5 is "voice pool to its 1,500 floor", applied only to a MEASURED projection. Pre-registered way:
  drop whole sources (both of a source's variants and nothing else) uniformly across generators and strata until the floor,
  keeping the A / B / C and strata shares; nothing is shed on an estimate. Voice tokens are short; the projection counts them.

## 10. Ruling-to-code conformance items for VOICE (plan 16.1 step 0; a fresh Sonnet 5.5 high session writes the map and CPU
tests, never the VOICE builder; Opus 5.5 high signs; the wrapper REFUSES voice rows without the record)

| Clause (ruling id) | CPU test id |
|---|---|
| G1 checkers A / B are programs; no LLM writes a transcript or a label | CT-V-G1-no-llm |
| G10 decision_spans with roles incl. AUTHORITY; fallback regex only when absent | CT-V-G10-roles; CT-V-fallback-cap-30 |
| VOICE C1: recoverable-span exception OFF; (a) not AUTHORITY (b) gold re-run on the structured spec with the span removed; fallback rows never | CT-V-C1-flag-off-drops; CT-V-C1-authority-never; CT-V-C1-label-recheck; CT-V-C1-fallback-never |
| VOICE C2: P-V1 has no removal power | CT-V-C2-no-removal-code-path |
| Ruling 4: the 0-160 ms trailing-silence item is not used | CT-V-padding-from-VD2 |
| Ruling 5: 15% disfluency, 30% fallback cap, 25% per-family cap, 5% GEN cap, 50% V-D3 reach | CT-V-params-fixed |
| Ruling 6: P-V0 thresholds are amber report lines | CT-V-P0-report-only |
| R11 (a)-(d) decided: espeak-ng absent from PATH and no subprocess spawn during G2P | CT-V-espeak-off |
| This addendum: generator C dictionary check; V-C13 neighbour validity; A / B / C split; source stamp currency; twin present at mix; replay sources only after clean-up | CT-V-C-licence, CT-V-C-neighbour, CT-V-split, CT-V-source-stamp, CT-V-twin-at-mix, CT-V-replay-after-clean |
| data/ohs3* and ohs3_parts/ skipped in every data/** glob | CT-OHS3-skip |
No VOICE program reads a path containing "ohs" or "sealed"; the wrapper and registry are reached only through the stamp service.

## 11. NEW NAMES for the names-only manifest v1.1 (names only)

```
FAMILY: VOICE (addendum v3.2)
GENERATORS: VGEN-A (round trip), VGEN-B (confusion-table noiser), VGEN-C (phoneme-neighbour swaps)   # VGEN-C is new
PRONUNCIATION_DICTIONARIES (licence check pending; the one that passes is used): misaki lexicon data, CMUdict
OPERATORS (VGEN-C): PN-SWAP, HOMOPH-SWAP, BOUNDARY-SHIFT
CONFIG_FLAGS: ctx_recoverable_enabled (False in C2.1)
LADDER_LEVELS: L1 (WER < 3 percent), L2 (3-8), L3 (8-15), L4 (15-25)
STRATA / CARRIERS / CHUNK_MODE / TTS / ASR / VOICES / HARVEST_CORPUS / TABLES: unchanged from the G0-lite section 10
SOURCE_FAMILIES: unchanged (no L-R dataset; no TP or HX form)
```

## 12. Open points for Opus (batch 1)

1. Condition C1 says the context-recoverable exception is "OFF by default" and then states the conditions under which a deleted
   span would count as surviving. This addendum reads it conservatively: the flag is False in C2.1, so a deleted or garbled
   decision span drops the variant; (a) and (b) are coded and tested but unused. Confirm, or turn it on with (a) and (b).
2. The ladder bar "C2 <= 70% on L4" is a report line for VOICE (VW-4). Confirm.
3. Generator split A 50 / B 30 / C 20: confirm, or give a different C share. C is CPU-only and ASR-independent; A uses the GPU.
4. L-R rows are excluded as voice sources (human labels; fallback spans only). Confirm.
5. If neither dictionary passes the licence check, generator C is OFF and the split returns to A 55 / B 45. Confirm.

---

## Binding conditions carried from families/G0_APPROVALS.md (copied word for word by the lane builder, Sun 18 Oct 2026; the
build skeptic checks the code against these lines; G1-G10 are already appended in VOICE/G0_LITE.md and are not repeated)

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

NOTE by the lane builder (not part of the copied ruling): the sentence "Voice rows stay OUT of the mix manifest until the owner answers R11" is
superseded by section 2 of this addendum, because the owner answered R11 in Record A79 (a)-(d allowed). All other copied lines bind unchanged.

---

## Opus batch-1 rulings v3.2 (Opus 5.5 high, Sun 18 Oct 2026 UTC; source: families/G0_APPROVALS_v32.md; binds over this file)

Global rulings GV1-GV9 of families/G0_APPROVALS_v32.md bind this file (GV1 one A10 build rule: flip = predicted label differs
wrapped vs unwrapped, build iff >= 10 of 200, no result by Fri 23 18:00 UTC = not built; GV2 role-play and benign justification
held out in every lane; GV3 one A14 build rule: >= 5 pp gap and bootstrap lower bound > 0; GV4 G6 binds A14, no exemption; GV5 a
G13-hit row retires its spec and its whole group, never re-worded, triggers read first-pass drops incl. collateral; GV6 one
perturbation library pert.*, zero_width = U+200B only, fullwidth / bidi / upside_down held out everywhere; GV7 A15 dialect rows in
L-A only; GV8 pilot-pooled sub-block probes, built-family read binds; GV9 held-out dev rows never trained, mix guard excludes them).
VERDICT: REVISE -> APPROVED after fix (applied in place): VOICE-M1 dictionary licence list = MIT / Apache / BSD / CC0 /
CC BY / CC BY-SA only (no NC, no ND, no GPL / LGPL, no unknown), in section 1 and V-C11.
Binding conditions: VOICE-B1 point 1: ctx_recoverable_enabled = False in C2.1. VOICE-B2 point 2: the L4 bar is a report line.
VOICE-B3 points 3-5 confirmed (A 50 / B 30 / C 20; no L-R source; C off -> A 55 / B 45). VOICE-B4 the section 2 mix-entry rule
supersedes the round-1 "stay OUT until R11" sentence (A79 R11). VOICE-B5 voice <= 8% of new rows.
