# Wording fixes for G13 seed hits (A31 (b)/(c)); backups: <file>.pre_wording

## Task A, shared vocabulary: packs + formats (2026-10-08 04:40 UTC)

Check: new wordings vs open dev/eval instruction texts (decontam_g13.instr_wordings + template_rev_hits): 5979 wordings, binding hits 0, report-only {'exact_2w_report_only': 0, 'contained_3_4w_report_only': 0}, >=5-word containment 0; full edited lines binding 0. OHS-3 sources are sealed: not checkable here.

| file:line | old | new | why |
|---|---|---|---|
| c_src/packs/packs-2/src/common_pools.py:89 | `"Good morning,"` x1 | `"Good morning to the team,"` | greeting leaf 'Good morning,' = short OHS-source item (exact_short; 80 rendered pack leaves) |
| c_src/packs/packs-2/src/lex_hs.py:150 | `length of stay` x1 | `nights of stay` | synonym = short OHS-source item (exact_short) |
| c_src/packs/packs-2/src/sec_hs.py:565 | `aka=length of stay` x1 | `aka=nights of stay` | aka = short OHS-source item (exact_short) |
| c_src/packs/packs-2/src/lex_hc.py:196 | `length_of_stay` x1 | `stay_days` | field name reads 'length of stay' (exact_short); renamed in all hc refs |
| c_src/packs/packs-2/src/sec_hc.py:726,761 | `length_of_stay` x2 | `stay_days` | same field, consistent rename |
| c_src/packs/packs-2/src/sec_fo.py:168,182,204,207 | `chief financial officer` x4 | `finance chief` | role/level = short OHS-source item (exact_short); all refs |
| c_src/packs/packs-2/src/sec_hr.py:617 | `green tea` x1 | `green leaf tea` | category value = short OHS-source item (exact_short) |
| c_src/packs/packs-4/src/batch_05.py:180 | `response rate|percent` x1 | `rate of replies|percent` | quantity name = short OHS-source item (exact_short) |
| c_src/packs/packs-4/src/batch_02.py:20 | `body weight|percent` x1 | `bodyweight|percent` | quantity name = short OHS-source item (exact_short) |
| c_src/packs/packs-4/src/batch_01.py:92 | `restore,welcome back|` x1 | `restore,readmit|` | synonym = short OHS-source item (exact_short) |
| c_src/packs/packs-1/src/b02.pack.txt:218,242 | `level 1, level 2, level 3, level 4, level 5` x2 | `L1, L2, L3, L4, L5` | ordinal scale = 10-gram in OHS source (ngram10, big_patent) |
| c_src/packs/packs-1/src/b02.pack.txt:235 | `is level 4 or level 5` x1 | `is L4 or L5` | rule text kept consistent with the renamed scale |
| c_src/formats/formats-1/build_pool.py:54 | `"notes": "Good to know"` x1 | `"notes": "Worth knowing"` | register header = short OHS-source item (exact_short) |
| c_src/formats/formats-1/data/registers.jsonl:2 | `"notes": "Good to know"` x1 | `"notes": "Worth knowing"` | same register header (data copy) |
| c_src/formats/formats-2/records/edos.jsonl | 455 records (lines 20..13998) | removed | public-data records flagged binding by G13 (methods 1-7 vs open evals / OHS sources); protective drop, text untouched; ids in formats-2/tmp/g13_wording/dropped_records.json |
| c_src/formats/formats-2/records/ghc.jsonl | 43 records (lines 346..4389) | removed | public-data records flagged binding by G13 (methods 1-7 vs open evals / OHS sources); protective drop, text untouched; ids in formats-2/tmp/g13_wording/dropped_records.json |

Notes:
- The two record backups live in `c_src/formats/formats-2/tmp/g13_wording/*.pre_wording` (not in `records/`, so finalize.py's `records/` iterdir does not list them). Other backups sit next to their files.
- `formats-2/manifest.json` still has the old sha256/rows for edos.jsonl (now 13545 rows) and ghc.jsonl (now 21987). finalize.py refreshes it at rebuild.
- packs-*/packs.jsonl and formats-1 pool outputs still hold the old text until the packs/formats rebuild (the fixes are in the generator sources; no rows were regenerated here).
- New wordings vs the OPEN dev/eval instruction texts: 0 binding, 0 report-only, 0 pieces of >= 5 words contained. They cannot be checked against the sealed OHS-3 sources (exact_short / ngram10 targets), so G13 must re-check them after the rebuild.

Groups (binding, from logs/decontam_counts/{packs,formats}.json):
- packs: 101 binding, all rendered, all fixed at source: packs-2 96 ('Good morning,' 80, 'length of stay' 10, 'length_of_stay' 4, CFO 1, 'green tea' 1), packs-4 3, packs-1 2. The other 57 'binding_lines' in G13_FIX_LIST are report-only (A31 (b), not rendered), so no change is needed.
- formats: 2919 binding = 2914 public_record + 5 rendered. Fixed: the 2 known rendered ('Good to know') and 498 public records (edos 455, which is all of edos; ghc 43).

Left (cannot fix from the current report):
- About 2416 binding public records past the report's 500-locator cap (`seed_hit_locs` is capped at sorted[:500]): the rest of ghc.jsonl, then mams_acsa / mams_atsa / xed. To list them, G13 needs an uncapped locator dump for formats.
- 3 binding rendered formats seeds, also past the cap. They sort after records/, so they are most likely in formats-2/wordings/. Same need.

## Task B: family templates F3 F4 F5 F9 F11 (2026-10-08 04:43 UTC)
Backups: `<file>.pre_wording` next to each changed file. Every new wording checked with decontam_g13 instr_wordings() + template_strings() via template_rev_hits (binding 0, report-only 0) and an extra 5-gram scan (0 shared 5-grams with open dev/eval instruction texts). Generator-level templates_rev after the edit: 0 binding in F3 F4 F5 F9 F11. Parsers re-tested: F3 parse_f3 finds T42/T42k; F9 f9parse + solver B sb_parse read all three number formats. OHS-3 sources are sealed and were not checked.
Note: G13_FIX_LIST locators `file#N (L)` are seed-literal index N (literals of >= 2 words) at file line L, so f4lex.py#151 = line 241, packs_f4.py#29 = line 96, F11 lex.py#227 = line 68, lex.py#29 = line 29.
- `c_src/F3/gen/registry.py:101` - T42 ledger-table rule: G13 drop 5-grams (share one entry number sequence / take effect in entry number / entry a void or correction / change but in a creation)
  - old: `Change rows share one entry-number sequence. 'From' and 'to' are a transfer's sender and receiver ('to' is the new ID on a rename row and the surviving {holder} on a merge row); 'refers to' is the entry a void or correction names. A blank cell means no change, but in a creation row the starting value '{default}'{qtyclause}. Rows are listed by {key} and take effect in entry-number order.`
  - new: `All change tables count entries in one numbered run. In a transfer, 'from' names the sending side and 'to' the receiving side; on a rename row 'to' holds the new ID, and on a merge row it holds the {holder} that remains. For a void or correction, 'refers to' gives the number of the entry it targets. An empty cell leaves the value unchanged; on a creation row it stands for the starting value '{default}'{qtyclause}. Rows are listed by {key}; their effects apply by ascending entry number.`
- `c_src/F3/gen/registry.py:102` - T42k (records variant of T42): same 5-grams
  - old: `Change records share one entry-number sequence. 'From' and 'to' are a transfer's sender and receiver ('to' is the new ID on a rename and the surviving {holder} on a merge); 'refers to' is the entry a void or correction names. A field left out is blank: no change, but in a creation the starting value '{default}'{qtyclause}. Records are listed by {key} and take effect in entry-number order.`
  - new: `All change records count entries in one numbered run. In a transfer, 'from' names the sending side and 'to' the receiving side; on a rename 'to' holds the new ID, and on a merge it holds the {holder} that remains. For a void or correction, 'refers to' gives the number of the entry it targets. A field that is left out counts as empty and leaves the value unchanged; on a creation it stands for the starting value '{default}'{qtyclause}. Records are listed by {key}; their effects apply by ascending entry number.`
- `c_src/F5/gen/sem.py:126` - SEM-28: G13 drop 5-grams (but also b means both / means both a and b / a and b are true)
  - old: `'"Not only A but also B" means both A and B are true.'`
  - new: `'"Not only A but also B" is true exactly when A is true and B is true as well.'`
- `c_src/F5/gen/sem.py:47` - SEM-08 (first variant): G13 drop 5-grams (include n at most n / more reaches n and meets); every quoted lexicon phrase kept
  - old: `"SEM-08": '"At least N", "no fewer than N", "not less than N", "N or more", "reaches N" and "meets N" include N. '
              '"At most N", "no more than N", "not more than N" and "up to N" include N. "More than N", "over N", '
              '"above N" and "exceeds N" exclude N. "Fewer than N", "less than N", "under N" and "below N" exclude N. '`
  - new: `"SEM-08": 'N itself counts for "at least N", "no fewer than N", "not less than N", "N or more", "reaches N" or '
              '"meets N", and likewise for "at most N", "no more than N", "not more than N" or "up to N". N itself '
              'does not count for "more than N", "over N", "above N" or "exceeds N", nor for "fewer than N", '
              '"less than N", "under N" or "below N". '`
- `c_src/F11/gen/lex.py:120` - SEM-15: G13 drop 5-grams (names a condition that must / must also hold it is / it is not enough on)
  - old: `"'Only if' names a condition that must also hold; it is not enough on its own."`
  - new: `"'Only if' adds a condition that is required too; that condition alone does not suffice."`
- `c_src/F9/gen/f9cards.py:500` - Text rule (T26): G13 drop 5-grams (match when they are the / upper lower case and spaces / s means s appears)
  - old: `["Text values match when they are the same apart from upper / lower case and spaces at "
                             "either end. '<col> contains <s>' means <s> appears anywhere in <col>, ignoring upper / "
                             "lower case."]`
  - new: `["Two text values count as equal if they differ only in capital letters or in spaces "
                             "before or after the text. '<col> contains <s>' is true when <s> occurs somewhere inside "
                             "<col>, with capitals ignored."]`
- `c_src/F9/gen/f9cards.py:563` - unit rule: G13 drop 5-gram (means that many of that)
  - old: `"An amount that a question asks for is given in the unit the question names. Every amount in a "
               "question or a definition is written with its unit and means that many of that unit."`
  - new: `"When a question asks for an amount, use the unit named in that question. Every amount written in "
               "a question or a definition carries its unit, and its number counts units of that kind."`
- `c_src/F9/gen/f9fmt.py:18` - number-format line (T21): G13 drop 5-grams (thousands and ' ' for / for decimals negative numbers / decimals negative numbers have a)
  - old: `Numbers use no separator for thousands and '.' for decimals. Negative numbers have a leading minus.`
  - new: `No mark splits thousands, and '.' marks decimals. A value below zero starts with a minus sign.`
- `c_src/F9/gen/f9fmt.py:19` - number-format line (T21): G13 drop 5-grams (thousands and ' ' for / for decimals negative numbers / decimals negative numbers have a)
  - old: `Numbers use ',' for thousands and '.' for decimals. Negative numbers have a leading minus.`
  - new: `',' splits thousands, and '.' marks decimals. A value below zero starts with a minus sign.`
- `c_src/F9/gen/f9fmt.py:20` - number-format line (T21): G13 drop 5-grams (thousands and ' ' for / for decimals negative numbers / decimals negative numbers have a)
  - old: `Numbers use '.' for thousands and ',' for decimals. Negative numbers have a leading minus.`
  - new: `'.' splits thousands, and ',' marks decimals. A value below zero starts with a minus sign.`
- `c_src/F9/gen/f9parse.py:151` - parser follows the new number-format line (same groups)
  - old: `r"Numbers use (no separator|'[.,]') for thousands and '([.,])' for decimals\."`
  - new: `r"(No mark|'[.,]') splits thousands, and '([.,])' marks decimals\."`
- `c_src/F9/gen/f9parse.py:153` - parser follows the new number-format line
  - old: `th = "" if m.group(1) == "no separator" else`
  - new: `th = "" if m.group(1) == "No mark" else`
- `c_src/F9/solverB/sb_parse.py:74` - solver B hard-codes the number-format line
  - old: `r"Numbers use '(.)' for thousands and '(.)' for decimals"`
  - new: `r"'(.)' splits thousands, and '(.)' marks decimals"`
- `c_src/F9/solverB/sb_parse.py:77` - solver B hard-codes the number-format line
  - old: `r"Numbers use no separator for thousands and '(.)' for decimals"`
  - new: `r"No mark splits thousands, and '(.)' marks decimals"`
- `c_src/F9/solverB/sb_parse.py:80` - solver B hard-codes the number-format line (unused space variant kept parallel)
  - old: `r"Numbers use a space for thousands and '(.)' for decimals"`
  - new: `r"A space splits thousands, and '(.)' marks decimals"`
- `c_src/F4/gen/f4lex.py:177` - rule text names the hedge lexicon
  - old: `'X might be H' and 'X appears to be "`
  - new: `'X might be H' and 'X could be "`
- `c_src/F4/gen/f4lex.py:241` - binding seed literal f4lex.py#151 (line 241)
  - old: `ENTITY_HEDGES = ("may be", "might be", "appears to be")`
  - new: `ENTITY_HEDGES = ("may be", "might be", "could be")`
- `c_src/F4/gen/f4lex.py:329` - hedge strip follows the lexicon
  - old: `r"\b(may be|might be|appears to be)\b"`
  - new: `r"\b(may be|might be|could be)\b"`
- `c_src/F4/gen/parse_f4.py:380` - parser follows the lexicon
  - old: `r" (may be|might be|appears to be) "`
  - new: `r" (may be|might be|could be) "`
- `c_src/F4/qc/g6.py:38` - QC hedge list follows the lexicon
  - old: `"may be", "might be", "appears to be")`
  - new: `"may be", "might be", "could be")`
- `c_src/F4/solverB/solver_b.py:547` - solver B follows the lexicon
  - old: `r' (?:may be|might be|appears to be) '`
  - new: `r' (?:may be|might be|could be) '`
- `c_src/F4/gen/packs_f4.py:96` - binding seed packs_f4.py#29 (line 96) is a code regex; replaced by the same test with no text literal
  - old: `if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9 '\-]*[A-Za-z0-9]", s):`
  - new: `if not (len(s) >= 2 and s[0].isalnum() and s[-1].isalnum()
            and all(ch.isascii() and (ch.isalnum() or ch in " '-") for ch in s)):`
- `c_src/F11/gen/lex.py:68` - binding seed lex.py#227 (line 68) is a code stopword list; one line so the A31 (b) render check sees one piece (word set unchanged)
  - old: `STOPWORDS literal over 9 lines`
  - new: `same words on one line`
- NOT FIXED: `c_src/F11/gen/lex.py:29` 'according to' (lex.py#29) is an entry of the QC ban list BANNED_PREP_ATTRIB. Rewording it would change what the QC bans, and splitting it only to hide it from the scan would loosen the gate. It binds only because the A31 (b) render check found the phrase in training rows; needs an orchestrator call (check those rows with methods 1-7, or a ruling).
- Spec note: F4 G0_SPEC.md:321 still lists the hedge lexicon as {may be, might be, appears to be}; the generator, rule text, parser, QC g6 and solver B now use 'could be' for the third item (same meaning: a possibility that settles nothing). G0_SPEC.md was not edited (frozen); needs a one-line spec/ruling note.
- Backups moved to `<dir>/tmp/<file>.pre_wording` (G13 seed_units skips tmp/; a backup beside the generator would be rescanned as a seed file with the old wording).
- 8 Oct ~02:50 EDT orchestrator: decontam_g13.py output-only change: seed_hit_locs / _report_only no longer capped at 500 (detection unchanged; backup c_build/tmp/decontam_g13.pre_uncap.py) so the formats run lists every binding location

## Task C: formats-2 remaining binding seeds from the uncapped formats run (2026-10-08 10:20 UTC)
Source: logs/decontam_counts/formats.json `seed_hit_locs` (2419 = 2416 public records + 3 Claude-written), mapped to records / literals with decontam_g13.seed_units (the '#N' index is the seed-literal index, not the file line).
| file:line | old | new | why |
|---|---|---|---|
| c_src/formats/formats-2/records/xed.jsonl | 1644 records | removed | public-data records flagged binding by G13 (A31 c); protective drop, text untouched |
| c_src/formats/formats-2/records/ghc.jsonl | 657 records | removed | same (ghc total dropped now 700) |
| c_src/formats/formats-2/records/mams_atsa.jsonl | 64 records | removed | same |
| c_src/formats/formats-2/records/mams_acsa.jsonl | 51 records | removed | same |
| c_src/formats/formats-2/wordings_src_a.py:241 (#206) | `"Use what's on the page plus the card. What do you make of it?"` | `"Use what's on the page plus the card and tell me what you conclude from it."` | F6.E casual wording; segment 'What do you make of it?' = exact_seg hit vs OHS source (gliclass-v2.0). Same meaning, one sentence |
| c_src/formats/formats-2/wordings/family_pools.jsonl:207 (#1032 text, #1033 text_gb) | same old | same new | wd.F6.E.03, regenerated by build_wordings.py (only this line changed) |
- Render check before rewording: the old wording renders in 254 rows of c_src/F6/out/candidates_r1.jsonl only; 0 rows in any round-1 family (F3 F4 F5 F7 F9) and 0 in the other families / public rows. F6 regenerates later, so its 254 rows keep the old text until then.
- New wording check: decontam_g13.instr_wordings + template_rev_hits: binding 0, report-only 0; lint_f2.lint_text F6: no problems; ROUGE-L max 0.452 vs 923 codebook / wording texts. It cannot be checked against OHS sources here; the r1 batch (formats set) rechecks it.
- Ids appended to formats-2/tmp/g13_wording/dropped_records.json (now edos 455, ghc 700, mams_acsa 51, mams_atsa 64, xed 1644). Backups in formats-2/tmp/g13_wording/: xed / mams_atsa / mams_acsa .jsonl.pre_wording, ghc.jsonl.pre_wording2, wordings_src_a.py.pre_wording, pre_rebuild/{wordings,locales}, manifest.json.pre_wording(2).
- Refresh: build_wordings.py (lints pass, 672 family wordings), finalize.py --manifest (records rows: edos 13545, ghc 21330, mams_acsa 3098, mams_atsa 4233, xed 25558). finalize --stamp not rerun (per-record rule, unchanged by removals). Dropped ids are referenced by no codebook / wording file.
- 8 Oct ~11:30 EDT orchestrator (owner OK): decontam_g13.py stream branch reads G13_BIGPAT_LOCAL/<file> when present (same parquet, pre-downloaded with retries; sha still recorded); backup c_build/tmp/decontam_g13.pre_localbigpat.py
