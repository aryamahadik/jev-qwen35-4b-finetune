# F7 devx v2 (blind, round-2 rebuild): notes

**What it is.** The blind-written F7 dev set from checklist section 2 rule 10 and SPEC section 6, rebuilt on 2 Oct 2026
to close every devx ruling in `yn2b/F7_OBJECTIONS.md`. It has 220 rows in 44 ladders: 176 yes/no rows and 44 choice
rows. Every instruction, card line and option is hand-written in `yn2b/f7_devx_build.py`. A program computes every
gold from the row's logical form (`lf`), and the build asserts it equals the gold written by hand for each twin.

**Files** (round 1 is kept byte for byte in `data/v14_parts/f7_devx_r1_backup/`)

| File | Rows | sha256 (round 3) |
|---|---|---|
| `data/v14_parts/f7_devx.jsonl` | 220 | `b5579786954652c201d9871a2d4e8a16c23340d4cad0254c1e5e84f8a4d34168` |
| `data/v14_parts/f7_devx_meta.jsonl` | 220 (sidecar, keyed by `id`) | `bc22f752d2e917f333401bfad926dfddfcf41a9d48ace2de156f6b10a11e5ac2` |
| `data/v14_parts/f7_devx_relations.jsonl` | 150 | `74cb00c9918959480caed38a1eb409974e7284578bde125f484994dc4c7da9d2` |
| `yn2b/f7_devx_blind_packet.jsonl` | 220, no gold, no lf, no sidecar | `eb5f482aae5774d76a15ba69d48cbc4b03308a1733dd610ef86ec14ec55fed9f` |

Round 2 is kept byte for byte in `data/v14_parts/f7_devx_r2_backup/` (round-2 hashes `d17f3221…`, `bea7571c…`,
`bcf3b339…`, `fe9117bb…`). Round 3 is in section 5.

Tools:
- `yn2b/f7_devx_build.py` builds everything (deterministic; a fresh build equals the written files).
- `yn2b/f7_devx_audit.py [--decontam]` writes `yn2b/f7_devx_audit.json`: 60 checks, all PASS.
- `yn2b/f7_devx_pool_scan.py` writes `yn2b/f7_devx_pool_flags.json`: overlap counts for the 54 real base texts.
- `yn2b/tests/test_f7_devx_build.py`: 30 tests.

Rebuild and check (CPU, about 1 minute, from `opendecide-data/lean`):
`../.venv/bin/python yn2b/f7_devx_build.py && ../.venv/bin/python yn2b/f7_devx_audit.py --decontam`

Row ids are `r_f7x2_<pair><twin>_<k>` (ladders `f7x2_L<pair><a|b>`). The round-1 ids `r_f7x_*` no longer exist, so the
round-1 decide2 parse table cannot silently match a rewritten row.

## 1. Design

**Twin ladders.** The 44 ladders are 22 twin pairs. Both ladders of a pair ask the same yes/no questions (same
instruction, same card) over two states whose core claim P has opposite truth values. So every yes/no question
appears once with gold yes and once with gold no. Twins share source, ladder kind, state format and state negation.
As a result every yes/no stratum the audit measures is exactly 50% yes, and every text-only shortcut scores exactly
50% on the yes/no rows. Each ladder has one choice row of its own.

**Ladder shape.** R0 plus three yes/no rungs plus one choice row (5 rows). R0 is in 44 of 44 ladders.

| Kind | Pairs | Source |
|---|---|---|
| Card format over one real text | 13 | civil_comments 4, toxic_conv 3, gd_saferproducts_severity 3, gd_wiki_help_routing 3 |
| Multi-text (2-5 real texts) | 4 | comment batches 2 (4 and 5 comments), two SaferProducts reports 1, three wiki posts 1 |
| Invented records | 5 | email thread, key: value ticket with rules, JSON expense claim, parcel log, chat |

**Base texts (ruling 10.8).** 54 real texts. Each is a plain base row (`r_` + 12 hex; every copy of a comment carries
the same human label, symbol-label copies read through their card). Each has 0 word 8-grams in common with any
golden_train state and with any F7 train or probe state, and 0 12-grams in the ship audit's reference sets
(golden_dev, breadth_dev, every dev / eval / held-out split, yn2b devs). Five texts picked first were replaced because
they overlapped golden_dev. Invented records use names from the devx pool of `mv_core.py`.

**LF contract (rulings 1.2, 1.4, 9.6).**
- Choice rows: CHOICE at the root; a negated selection carries its cue on the CHOICE node; every option has exactly
  one CORE; sidecar `gold` is the option index; `depth` = NOT nodes on the gold option's path + 1 for a negated
  selection. An instruction-level distractor is a DIST node on the gold option.
- Look-alikes (under, notable, uniform) are cues of class `lookalike` on no node; they are not distractors.
- Rule words (`must not`, `unless`, `need not`) are NOT nodes on the claim path.
- A negation inside reported content of a non-factive verb ("claims that the request is unapproved") is not a cue;
  it is listed in `content_negations`.
- AR rows are `NOT` with `"cue": null` and no cue word, each with an odd-depth sibling of the same gold.
- Item-21 rows carry `antonym_gold`; the antonym reading is wrong on 2 of 4 such rows (C7 >= 30%).

## 2. Audit results (`yn2b/f7_devx_audit.json`, all PASS)

**Ship-audit row checks on devx** (the precheck's own functions): 1.1-1.7, 2.1, 2.2 (84/84 distractor deletions),
2.4 (34/34 bivalence lines), 2.5, 2.6, 3.3 (0 tag mismatches), 4.1c (12 cells, 0 bad), 4.2c (278 strata, 0 bad),
5.l (138/138), 7.1 (0 for X1-X12), 8.9, 9.1-9.3, 9.5-9.7. With `--decontam`: 8.1-8.8, 8.11, 8.12, 8.14, 8.15 all 0.

**Section-3 targets, computed on devx**

| Target | Wanted | devx |
|---|---|---|
| Depth mix d0 / d1 / d2 / d3 / d4 | 18 / 25 / 30 / 24 / <=3 (+-2) | 20.0 / 25.0 / 30.0 / 24.1 / 0.9 |
| Yes share per cell, rung, stratum | 48-52 / 45-55 | 50.0 everywhere (twins) |
| truth(P) per rung (all rows) and per depth (yes/no) | 48-52 | all in band; R0 ladders 22 / 44 |
| Choice rows; negated selection; gold position | 20 +- 3; 50%; uniform | 20.0; 50.0; 7-7-7 (k=3), 6-6-6-5 (k=4) |
| Rows with a distractor, overall / per depth 0-3 | >=35 / >=25 | 37.3 / 31.8, 30.9, 43.9, 37.7 |
| Parity(all cues) != parity(scoping) | >=30 | 45.9 |
| AR + lexical-only flips, share of odd rows | >=15 | 15.7 |
| Cue mix syn / aff / lex / truth frame / cross+answer | 25-35 / 20-30 / 20-30 / 10-15 / 5-10 | 30.3 / 21.4 / 26.1 / 13.7 / 8.5 |
| not + n't; top lexeme | <=20; <=10 | 10.1; un- 8.5 |
| Scoping positions inner / outer / card / separate / key+map / options | 25-35 / 20-30 / 15-25 / 5-10 / 5-10 / 5-10 | 25.5 / 28.3 / 24.9 / 6.1 / 5.5 / 9.7 |
| Card styles (yes/no) per depth and gold | equal +-2 pts | golden 69.3, defs 12.5, Yes 9.1, none 9.1; 0 cells off |
| Yes share with / without state negation | equal | 50.0 / 50.0 |
| C1 / C2 / C3 / C4 / C5 / C6 (aff, lex, cross) | 45-55 / <=70 / <=65 / <=60 / <=60 / <=60 | 51.1 / 53.4 / 47.7 / 56.8 / 58.0 / 58.0, 51.1, 50.0 |
| C2 per depth | <=75 | 63.6 / 47.8 / 59.1 / 45.0 (d4: 2 rows) |
| Odd-parity share per lexeme with >= 10 rows | 40-60 | all in band |
| Choice probes: longest / most cues / fewest / overlap | <=55 | 54.5 / 50.0 / 18.2 / 45.5 |
| |r| gold position vs negated selection / depth / options / cues | <0.05 | 0.010 / 0.004 / 0.028 / 0.017 |

**Checklist items (rows tagged; one row can carry several).** Every item 1-38 is present. MUST: 1 (44), 2 (6), 3 (4),
4 (7), 5 (6), 6 (34), 8 (52), 10 (34), 11 (22), 12 (72), 13 (16), 15 (18), 16 (68), 21 (4), 22 (12), 24 (5),
27 (3), 36 (22). SHOULD: 7 (6), 14 (4), 17 (2), 18 (26), 19 (40), 20 (12), 23 (2), 26 (10), 28 (7), 30 (8), 31 (4),
32 (2), 33 (5), 34 (4), 35 (4), 37 (3), 38 (2). NICE: 9 (2), 25 (2), 29 (1). The checklist sets no per-item floor
for devx (the >=40 / 20 / 10 floors apply to iid + holdout); caps hold (item 9 0.9%, 14 1.8%, 38 0.9%).

## 3. Full ship precheck (every input, `--decide2-independent yes`)

110 PASS, 1 FAIL, 2 PENDING. Every devx failure of round 1 (1.2, 1.4, 3.3, 4.1c, 4.2c, 5.l, 7.1, 8.3, 8.4, 8.6, 8.14,
9.3, 9.5, 9.6, 10.8) now passes; so do 3.9 (220 devx rows), 10.6 (max 12-gram share with train 0.0) and 10.7.
- **2.3 FAIL:** decide2 agrees 15,086 / 15,086 on train and probe; the 220 devx rows are unparsed ("devx row not in the
  parse table"). This is the 2.3b exception: devx's decide2 LFs must be written again by an agent who has not seen
  devx golds. That agent reads `yn2b/f7_devx_blind_packet.jsonl` only (never `data/v14_parts/f7_devx*.jsonl`, the
  sidecar or this builder) and rewrites `yn2b/f7_devx_decide2_lf.json` for the `r_f7x2_*` ids; then decide2 is run
  with no `--files` and the precheck again.
- **8.13 PENDING:** owner step (`--ohs3-blind`).
- **11.1 PENDING:** a separate blind reader.

## 4. Blindness and disclosures

- Never opened: `gen3_nested_negation.py`, `nn_lexicon.py`, `f7_lexicon.json`, any F7 train / probe row text, any
  `ohs3` file.
- Read: the checklist, SPEC, the arbiter rulings, `yn2b/f7_precheck.py` (the audit, to meet its contract; round 1 had
  not read it), the devx section of `v3_nested_negation.py` (for the parse-table interface only), `train_decoder.
  check_rows` (read-only import), `mv_core._pools` (devx name pool).
- Count-only scans: word 8-gram membership of the 54 base texts in golden_train and in F7 train / probe states
  (no text printed or stored); the SPEC 7.3 cue-share rule over F7 + devx instructions, which printed six aggregate
  instruction words with their odd-parity shares (the worst was 0.58).
- 8.6 reads the OHS-3 negation frames from `build_ohs3.py` text inside the precheck, as designed; nothing was printed.
- The second pass in `yn2b/f7_devx_coldpass.json` and the parse table `yn2b/f7_devx_decide2_lf.json` belong to round 1
  (ids `r_f7x_*`); both are superseded.

## 5. Round 3 (2 Oct 2026): the two ambiguous rows from arbiter round 3 (A3, A4)

Written by the round-3 repair agent **before it opened any F7 renderer**: at the time of these edits it had not read
`gen3_nested_negation.py`, `nn_lexicon.py`, `f7_lexicon.json` or any F7 train / probe row text (the devx hashes above
were recorded first, then the generator was opened). It read the arbiter rulings, the checklist, this builder, the
devx audit and the devx part of `v3_nested_negation.py` (interface only). Only 4 rows change; the other 216 rows and
their sidecar lines are byte for byte round 2 (`test_round3_rewrites_exactly_the_four_ambiguous_rows`).

| Ruling | Row (old id -> new id) | Old wording | New wording |
|---|---|---|---|
| A3 | `r_f7x2_17a_1` -> `r_f7x3_17a_1`, `r_f7x2_17b_1` -> `r_f7x3_17b_1` | "Is it true that no post apart from Post 3 belongs at the Language desk?" (twin b has no Language post and Post 3 is a Mathematics post, so the exceptive's inclusion reading and the literal reading differ) | "Is it true that no post apart from Post 3 belongs at either of the Language and Mathematics desks?" Post 3 is a Mathematics post in both twins (human label; the build asserts it), so the inclusion holds and both readings agree on both states. Same depth (1), cue ("no", inner claim), items [2, 31], frame and golds (a no, b yes). |
| A4 | `r_f7x2_14a_3` -> `r_f7x3_14a_3`, `r_f7x2_14b_3` -> `r_f7x3_14b_3` | card had no definition of 'the opposite' of "not a single comment is toxic" (on twin a's mixed batch, plain denial gives no and the contrary reading gives yes) | the question is unchanged; the card gains "- note: here 'the opposite' of a claim means its plain negation." |

- **New ids.** The 4 rows carry `r_f7x3_` ids (ladder ids stay `f7x2_L..`). decide2's parse table still holds the
  round-2 LFs of the old wording under the old ids, so it cannot silently match a rewritten row: until their LFs are
  written again the 4 rows are unparsed, and 2.3 fails safe.
- **Still to do (2.3b exception, not this agent):** an agent who has not seen devx golds writes the decide2 LFs of
  `r_f7x3_14a_3`, `r_f7x3_14b_3`, `r_f7x3_17a_1` and `r_f7x3_17b_1` from `yn2b/f7_devx_blind_packet.jsonl` only, adds
  them to `yn2b/f7_devx_decide2_lf_author.py`, and rebuilds `yn2b/f7_devx_decide2_lf.json`. This agent has seen the
  golds of pairs 14-17, so it did not write them.
- **Checks.** `f7_devx_audit.py --decontam`: 60 / 60 PASS (positions unchanged: inner claim 25.48%, outer 28.25%; the
  worst instruction word is still 'not' at 0.5758; "or" was avoided because it would reach 30 rows at 0.60).
  `test_f7_devx_build.py`: 33 passed, including 3 new tests that fail on the round-2 rows (the 4-row diff, the pair-17
  inclusion, the 'opposite' definition).

