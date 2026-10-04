# C_DATA_SPEC: the golden dataset for model C (v4)

Date: 3 Oct 2026. Status: spec only, version 4. Version 2 answered most review items; version 3 closes the rest, applies
the owner's 3 Oct decisions and the section-12 defaults, and aligns with `C_TRAIN_RECIPE.md` v3. The 3 Oct licence
merge (CHANGES 13) is applied: every public and commit source in sections 3-4 now has a licence read upstream. Version 4
applies every data row of `ADDENDUM_research.md` (CHANGES v4 below; status of every addendum row in 0.2) and supplies
the `meta.option_level` field and A1 lint that `C_TRAIN_RECIPE.md` v4 (ordinal mean term, A4) reads. Nothing here has
been built or run.

**CHANGES (v4: research addendum, 3 Oct; all rows decided before any C row exists)**
1. **A1 ordinal target lint (2.4, 5, G18, step 9).** Builders emit `meta.option_level` on every ordinal row. The builder
   and the mixer compute E of the actual training target (after smoothing, KD and the C1 anchor) and require
   `round_half_even(E_target) == gold level`. On failure: drop the KD/anchor part and fall back to smoothed gold; drop
   the row if it still fails. 100% pass before any freeze.
2. **A2 level balance with real end levels (F7, 4.2).** Commit Score rubrics are stratified so every level, both ends
   included, is >= 1/K - 5 pp of that rubric's rows. F7 adds a cut-point sampler (a stated quantity binned by stated
   cut points, top level as common as the others), inside F7's 7%. Short end levels: raise the generation ratio, never
   relabel. No commit-size item, cut point or level wording is copied from ejs-5.
3. **B1 message-only commit rows (4.2).** 30% of Gate, Triage and Route commit rows (360 / 720 per type: 1,080 r1 /
   2,160 r2) show the commit message only (diff and numstat hidden); labels still come from the program over the real commit. A row is kept only if the decisive
   fact is stated in the message (matcher M, one symmetric program check, then the G5 re-read); failures are dropped,
   never relabelled. Keyword-shortcut negatives are required and come from the same matcher (gate: the trigger is
   hit and gold is "no"; route: a non-gold area is also hit). Score rows keep numstat shown.
4. **B2 per-rule yes rate (4.2, G10).** Commit Gate (per rule) and Match (per card) draw their yes rate uniformly from
   20-80%; aggregate 50 +/- 2, the same rule as own families. Replaces Gate's flat 50/50.
5. **B3 gold-free yes-share drift alarm (9, 10).** Report-only: mean P(yes) and predicted yes share per domain on the
   mix-tuning dev at each snapshot, and on each sealed set at its existing looks only. Alarm outside 30-70% on any
   domain that is 50/50 by construction. No new looks; it never chooses anything.
6. **B4 no test-time prior fix ships (4.4).** No Batch Calibration, EM, BBSE or median cut on any served or reported
   readout.
7. **B5 ejs-5 reporting, disclosed in advance (4.4).** ejs-5 is reported as full set + late rows + Gate. A tie on the
   full set is the realistic best case for C. The registered endpoint (full set) is unchanged; late rows and Gate were
   chosen after seeing ejs-5 results, so they stay report-only and can never become an endpoint.
8. **E2 replay yes rate per wording (5, G10).** CPU check of the replay yes rate per instruction wording; any wording
   cell outside 50 +/- 5% is re-stratified (whole units, same source).
9. **F3 F13 aggregate sub-type (F13).** About 20% of F13 rows (r1 about 410 / r2 about 820) need facts from 2-3
   sections (counts, latest valid version, totals split across sections), with program labels. Low confidence.
10. **F4 O*NET persona seeds (2.1, 3.G).** Claude-written scenarios and domain packs take their "who is deciding"
    persona from O*NET occupation titles (CC BY 4.0; `gd_onet_occupation`, KEEP in `LICENCE_REGISTER.md` section 4).
    PersonaHub (CC-BY-NC-SA-4.0) is never used.
11. **Addendum section I (orchestrator).** B6 (ejs-5 decomposition) is **not run**, so B7 **never fires**: commit Score
    keeps its 20% share. ejs-5 figures in the addendum are aggregate-score context (some gold-scored vs Jev). v3's
    commit shares had been set from the ejs-5 per-task C1-vs-Jev gaps in the ejs-5 run scores file (methods S3; a 7.4
    path, no longer an input), not from the addendum; v4 replaces them with equal shares (20% per type, 4.2).
    ejs-5 and OHS-3 never choose a data share, loss weight, temperature, readout or model.
12. **CONSIDER rows A6, C5, E4: not applied in round 1**; D2 is decided once, in the C PREREG amendment (adopted
    for round-1 public rows only if the G9 L4 pass can log C1's hidden states at no extra time, else it lapses for C);
    each one's condition is stated in 0.2. **REJECT rows A7,
    B8, C7, D3, F5 are excluded** (0.2). Recipe-only rows (A3-A5, C1-C4, C6, E1, E3, F1, F2) belong to
    `C_TRAIN_RECIPE.md`, which this version does not edit.
13. **Totals unchanged.** All v4 rows sit inside existing family, type and source quotas: new rows 60,000 / 120,000;
    own 45,250 / 90,500; public 8,750 / 17,500; commits 6,000 / 12,000 (0, 2.2, 3.2, 4.2). Commit types are now equal
    shares, 1,200 / 2,400 each (4.2); message-only rows 1,080 / 2,160, inside those counts.
14. **Verifier pass (3 Oct, owner rules).** Commit shares no longer come from ejs-5 vs Jev (equal shares, 4.2);
    ejs-5 late rows and Gate are report-only forever (4.4); B3 on sealed looks only if the frozen scorer prints it
    (9); B1 shortcut negatives use each rule's B2 rate (per-rule check pooled by rate decile under 20 rows), and B1
    keeps and shortcut negatives use one symmetric matcher M, the same for gold and non-gold (4.2, G6, G7, G10); O*NET seeds pass as `no_new_rows` (2.1, 3.H.2); no public ordinal rows in round 1 (2.4); D2
    decided once in the amendment (0.2, G9); sampler ids S6+ (2.1, 2.4, F7); E2 G10 cells >= 50 rows (G10).

**CHANGES (v3)**
1. ShARC, Measuring Hate Speech, CAD-SNLI, Social IQa, CosmosQA and NewsMTSC are out, **and so is anything built on
   them**: the deny-list program now checks each dataset's declared parents (3.H). They are no longer F5 bases.
2. Deny-list program (3.H). It checks every `golden_src/*/rejected.json` entry (both file formats), every "avoid" entry
   in `ohs3/used_sources.json` (read by the program only), the 152 forbidden tasks, the OHS source list and the 3.G
   table. It runs at builder start, in the mixer and in G1, and also over the 204 replay sources (3.H.3).
3. Jev outputs: every local Jev output file found on 3 Oct (`preds*/jev*`, `logs/jev_*`, `bench/runs/jev_*`, JevBench
   results, jagged trials, ejs-5 runs, report variants) is on every builder's forbidden list. The program refuses those
   paths and any `jev*` field (7.4).
4. Section 12 is rewritten as decisions **made by default** (the owner may override). Effects:
   - the orchestrator runs the counts-only checks;
   - the scoring crowd runs on the free L4;
   - forbidden-list and Claude-gold replay rows are dropped;
   - NewsMTSC is disclosed and excluded;
   - a creator's HF card does not count as a licence, so DocFinQA is out;
   - flagged document texts are out unless the licence check clears them. After the 3 Oct checks (item 13):
     MultiHiertt and ConvFinQA (FinTabNet text) are out, QuALITY Slate/OANC is cleared, and Qasper keeps only papers
     with an arXiv CC BY, CC BY-SA or CC0 licence;
   - Jev is read once on the sealed suite (report only);
   - the founder audit is optional.
5. Totals, default case: public block 14 datasets, 17,500 rows in round 2; own rows 90,500 (F13 +500). The 120,000 new
   rows are unchanged (0, 3.2).
6. The sealed suite is aligned with recipe v3:
   - part A has >= 5,000 real-text items (6-10 domains, none above 20%);
   - items are split 40/60 into select and confirm sets by sha256 mod 5;
   - adjacency labels are fixed at freeze;
   - looks follow recipe 6.2: **one candidate per round**, and round 2 runs only if round 1 clearly wins (recipe 6.3).
7. REF is C1 only; every "a*" path is removed. The anchor gets the protected-skill clause (`c1_anchor_protected`) from
   recipe 3.
8. The D2 unseen set is re-derived for each decision (round-2 rule and ship look) from that candidate's own training
   files, then frozen before the read (7.3).
9. Replay checks: no rows from the Stack Exchange half of politeness data; no bundled CoNLL-2003 rows in CrossNER;
   subset checks for RAGTruth, HelpSteer3, MultiWOZ and WebRED (3.H.3).
10. Stale references are fixed: the depth sweep reads CAND - C1, not K1; the hard-negation probe is report-only, not
    "D8"; the 0.1 table no longer says "2 candidates per round".
11. Commits (4): ejs-5 is labelled in-domain; the orchestrator runs the ejs-5 counts-only and wording checks; a PII
    scrub and a deny-list run are added as guards 10-11.
12. Order (11, G14): steps 2-9 start only after the sealed suite's sha256 is committed. Before that, no C data of any
    kind exists (packs, styles, codebooks, rows).
13. **Licence merge (3 Oct, `LICENCE_CHECK_1/2/3.md`).** All 19 new sources were read upstream. Final list: 14 public
    datasets IN, 3 OUT and moved to 3.G (DocFinQA: creator's card only; MultiHiertt and ConvFinQA: FinTabNet text
    licence unverified and not on the allowed list). Their round-2 rows went to F13 (+500), WikiSQL (+800) and
    HybridQA (+800), so the totals do not change. Nursery is verified; QuALITY's Slate/OANC articles are cleared;
    Qasper's per-paper filter reads the arXiv licence (NC and ND papers out); CommitChronicle cites its Zenodo
    record (CC BY 4.0) and CommitPackFT its GitHub repo (MIT). Replay `gd_finqa` (4,970 rows, same FinTabNet text)
    moves to "verify upstream or drop". New guards: MuSiQue's dev/test single-hop ids are a drop list on SQuAD rows.
14. **Verifier pass (3 Oct).** Decisions 6 and 12 now also cover replay: 15 replay sources (38,521 rows) whose only
    licence record is the creator's HF card move to "verify upstream or drop" (section 5; register section 4). The
    never-open list adds the review and licence-check files that name sealed candidates. Sealed part B1 commits come
    from repos in no split of either commit dataset. Section 12 rows are in order.

Inputs: the research reports in this folder, `golden_src/GOLDEN_SPEC.md`, `golden_src/forbidden_label_nli.json`,
`golden_src/*/rejected.json`, `breadth_src/SELECTION.md`, `FREEZE.md`, `PREREG_FINAL.md` (3.2, 3.3, A11, A12),
`runs/q35_4b_main.json`, `train_decoder.py`, `bench/ejs5/README.md`, and a per-source scan of
`data/v14_parts/golden_train.jsonl` (`replay_licence_scan.json`). (v4) No ejs-5 run or scores file is an input: those
paths are on the 7.4 list (v3 had used one to set commit shares; 4.2).
v4 adds `ADDENDUM_research.md` (verdicts and section I) with its evidence in `RESEARCH_EXTRA_1-6.md`. Builders work from
this file only: they do not open the addendum or `RESEARCH_EXTRA_*` (these quote ejs-5 aggregates and readout analysis).
Companion files: `C_TRAIN_RECIPE.md` (training, gate, expected value) and `LICENCE_REGISTER.md` (private).

All gains named here are estimates from other people's setups. Our own history says dev gains often do not transfer
(C1: +2.5 pp on dev unseen sources, but -0.4 pp vs 4B-E on ejs-5; A18 failed its gate).

**Who may read what.**
- C builders get an allow-list: this file, `C_TRAIN_RECIPE.md`, `LICENCE_REGISTER.md`, their own `c_src/<family>/`
  folder, and the input files named in their task.
- C builders never open: `c_spec/sealed_brief/`, `c_spec/RESEARCH_licensed-data.md`, `c_spec/REVIEW_methods.md`,
  `c_spec/REVIEW_rules.md` and `c_spec/LICENCE_CHECK_1/2/3.md` (they name sealed-suite candidates), `lean/sealed_nd/`, `lean/ohs3/` (including `used_sources.json`: the deny-list program reads it, agents
  do not), `data/ohs3*`, `data/*ohs3*`, `data/ohs3_parts/`, `prep89/`, `preds_ohs*/`, `bench/external_quarantine/`,
  `bench/longbench_v2/`, any eval test split, and **every Jev-output path in section 7.4**. (v4) Also
  `c_spec/ADDENDUM_research.md` and `c_spec/RESEARCH_EXTRA_*.md`: they quote ejs-5 aggregates and level names, and
  this file already carries every data rule from them.
  (v4, 3 Oct) Also every agent-session folder: `~/.claude/projects/**` (session transcripts, `subagents/`,
  `tool-results/`) and `/private/tmp/claude-501/**` (`tasks/` outputs, `scratchpad/`), because sealed-side agents ran in
  the same session. C builders write scratch files only inside their own `c_src/<family>/tmp/`.
- File lists are built by explicit allow-list, never by a broad `data/*` glob. The shared loader refuses any path on
  the 7.4 list and any path under the never-open list above, so a mistake fails loudly instead of reading.

---

## 0. Summary

| Item | Round 1 | Round 2 (superset of round 1; runs only if round 1's one candidate passes the owner's rule, recipe 6.3) |
|---|---|---|
| Total rows | 150,000 | 300,000 |
| Replay of C1's golden_train (60%) | 90,000 | 180,000 (round 1's 90,000 + 90,000 fresh, no repeats) |
| New rows (40%) | 60,000 | 120,000 |
| - own program-labelled questions (13 families, incl. real-text codebook variants) | 45,250 | 90,500 |
| - licensed public human-labelled train splits (14 datasets after the 3 Oct licence check; 3 moved to 3.G) | 8,750 | 17,500 |
| - commit decisions from other repos (never n8n; v4: 5 types at equal 20% shares; 30% of gate, triage and route rows message-only, 1,080 / 2,160) | 6,000 | 12,000 |
| Distinct task cards (own + public + commit) | >= 1,050 | >= 2,000 |
| Rows per card | median about 40, max 128 | median about 45, max 128 |
| Candidates | one, pre-registered (the final-step adapter, recipe 6.2) | one, pre-registered |

The owner's plan asked for about 90K own rows. Version 3 meets it. Dropping 7 public sets (section 3.G) freed about
10K rows, which moved to own families. The 3 Oct licence check (CHANGES 13) left three more sets out: DocFinQA's
500 rows went to F13, and MultiHiertt's and ConvFinQA's 1,600 rows went to WikiSQL and HybridQA (round 2 counts).
They come back only by PREREG amendment (3.G).

**Round 2 is conditional (owner, 3 Oct).** It runs only if round 1's single candidate shows a clear gain on the sealed
part-A select set: CAND - C1 >= +2.0 pp **and** paired 95% LB > 0, **and** guards D1-D6 pass (no harm to dev,
security, calibration or option order). Otherwise the owner reviews a diagnosis first (recipe 6.3). Under the recipe's
prior, P(round 2 runs) is about 13%, so **round 1 is the main shot**. Build round-1 data to full quality first. Round-2
rows (new cards, fresh replay) are generated only after the round-2 rule passes, except for the generator code itself.

The seven rules that matter most:
1. **Breadth beats volume.** Count distinct task cards, not rows. Held-out accuracy grows about log-linearly with the
   number of distinct tasks; extra rows stop helping at about 64 per task (Super-NI). Fewer than about 300 distinct
   instructions never generalized; 1,000 or more always did (Zhang 2024).
2. **Every label is exact.** Own rows: a program gives the label, and a second program of a different kind agrees on
   100% of rows. Public rows: human gold only. Real-text codebook rows: a program maps human annotations to codes.
   No model ever sets a label. Claude writes text, templates, definitions and code, and reads blind to flag problems.
3. **No shortcuts.** Partial-input and metadata baselines must sit at chance. Template, sampler, length, number of
   negations, option position and "attack present" must not predict the label.
4. **No leaks.** Decontaminate against every test we report, with counts-only checks for sets we may not open.
5. **The sealed new-domains suite is built and frozen first, by a separate agent. No C builder ever sees it.**
6. **Every `golden_src/*/rejected.json` entry and every `ohs3/used_sources.json` "avoid" entry is a deny-list**, and
   so is anything built on a denied dataset. The program in 3.H checks each dataset and its declared parents. A
   rejected dataset comes back only through a PREREG amendment that answers the recorded reason.
7. **No Jev output is ever an input.** Builders cannot open the 7.4 paths, and the loader refuses them.

### 0.1 Review items and where they are fixed (v2 and v3)

| Review item | Fix | Where |
|---|---|---|
| Methods B1: 5 public sets already rejected | ShARC, Measuring Hate Speech, CAD-SNLI, Social IQa and CosmosQA dropped, plus anything built on them (parent check). e-CARE, EmoBank and ConvAbuse are also dropped (they are in rejected.json). rejected.json entries and used_sources "avoid" entries form a program deny-list. MultiDoc2Dial and NLU++ are never sealed candidates | 3.1, 3.G, 3.H, 9 |
| Rules B1: NewsMTSC uses non-commercial POLUSA text | NewsMTSC dropped; `br_newsmtsc` (607 rows) dropped from replay; C1's use is disclosed (decision 5) | 3.G, 5, 12 |
| Rules B2: CosmosQA source text | Dropped | 3.G |
| Methods B2: round-1 rule vs owner's decision | Round 2 runs only under the owner's rule, on one pre-registered candidate | 0; recipe 6.3 |
| Methods B3: gate rarely ships a better model | Sealed part A >= 5,000 items with a 40/60 select/confirm split; **one candidate per round**; P(ship) stated in recipe 10 | 9; recipe 6, 10 |
| Methods B4: sealed suite not independent | Headline on real text only (>= 4 non-adjacent domains); program-built part report-only; own format styles; no domain names in this file; rule-based label filters; frozen before any C data exists | 9, 11 |
| Rules B3: blind decontam misses short items | Counts-only script adds exact text and sentence hashes, 5-word substring check, 10-grams, 8-gram rule, MinHash | 7 |
| Rules B4: missing decontam targets | Adds the 152 forbidden tasks' texts, all splits of OHS source datasets, eval_opi, eval_jagged, TabFact tables, HateXplain and SBF posts | 7 |
| Replay licence and rule gaps (rules S1-S3) | Jigsaw-derived sources dropped; forbidden-list and Claude-gold sources dropped (decided by default, decision 4); licence join; deny-list run over replay sources | 3.H.3, 5 |
| Methods S1-S2: noisy replay rows, anchor softens clean labels | Drop human-labelled replay rows with p_g < 0.2. Anchor only where C1 is right and confident (p_top >= 0.8), or right on a pre-registered protected skill | 5; recipe 3 |
| Methods S3: commit weights | (v4) equal shares, 20% per type (route, triage, score, gate, match). v3's 10/20/25/35/10 had been set from ejs-5 per-task C1-vs-Jev gaps, which the owner rule forbids, so v4 replaced them. Numstat shown on score rows; file headers hidden on route rows | 4 |
| Methods S5-S7: negation evidence weak, deep arithmetic, few samplers | Lighter negation quotas, F5 sized by the round-1 probe; F2 at most 2 operations by default; >= 4 training samplers per family | 2 |
| Methods S8: difficulty selection breaks yes/no balance | 3-model scoring crowd; selection inside label x wording strata | 2.1, 8 |
| Methods S10, N6: memory and batching | Relation units of at most 3 rows; long units at most 2 rows; real-tokenizer unit check | 2.1, 6; recipe 3 |
| Methods S14: no real-text seeding | Real-text codebook variants in F10 and F11 (30% of their rows) | 2.3 |
| Rules S4-S8, S10, S11 | Sealed fixes, commit guards, Jev-output deny paths (full local list, loader-enforced), group-level holdouts, split rules, attack-wording check, re-derived D2 per decision | 4, 5, 7, 9; recipe 6 |
| Rules S9: creator's-card licences | A creator's HF card is not an official record (decision 6). DocFinQA is out; MHS was already out. The 3 Oct licence merge read every new source upstream; 3 sets are out (3.G) | 3.1, 3.2, 3.G, 12; `LICENCE_REGISTER.md` |
| Methods S9, S12 | 400 mix-tuning-dev items per family; the cosine threshold is set on open sets, then applied blind | 7.2, 10 |

### 0.2 Research addendum rows and where they land (v4)

Source: `ADDENDUM_research.md` (verdicts) and its section I (orchestrator decisions, 3 Oct, before any C row exists).
**Every applied row stands on dev or external evidence alone.** ejs-5 figures in the addendum (A2, A3, A5, B1, B2) are
aggregate-score context (some gold-scored vs Jev). v3's commit shares had been set from the ejs-5 per-task
C1-vs-Jev gaps in the ejs-5 run scores file (methods S3; a 7.4 path), not from the addendum; v4 replaces them with
equal shares (4.2). B1 follows ejs-5's public input format (prose only, PREREG_ejs5 section 7) and uses no ejs-5 item or wording.

| Row | Verdict | Status in this file | Where |
|---|---|---|---|
| A1 ordinal target lint | ADOPT | Applied: `meta.option_level`, lint in builder and mixer, 100% pass before freeze | 2.4, F7, 4.2, 5, G18, step 9 |
| A2 level balance incl. end levels | ADOPT | Applied: commit Score per-rubric level floor; F7 cut-point sampler; F7 uniform gold kept | F7, 4.2, G10 |
| B1 message-only commit rows | ADOPT | Applied: 30% of gate, triage and route rows; symmetric matcher M (keep check and shortcut negatives) | 4.2, G5, G6, G7 |
| B2 per-rule commit yes rate | ADOPT | Applied: gate per rule, match per card, 20-80%, aggregate 50 +/- 2 | 4.2, G10 |
| B3 yes-share drift alarm | ADOPT | Applied, report-only; no new looks | 9, 10 |
| B4 no test-time prior fix | ADOPT (rule) | Applied | 4.4 |
| B5 ejs-5 report form + expectation | ADOPT (expectation) | Applied and disclosed in advance; endpoint unchanged | 4, 4.4 |
| B6 ejs-5 decomposition | CONSIDER | **Not run** (section I). Nothing reads ejs-5 gold for diagnosis | 4.4 |
| B7 cut commit Score to <= 10% | CONSIDER | **Never fires** (it needed B6). Commit Score keeps its 20% share (equal shares, 4.2) | 4.2 |
| D1 keep stratified selection | ADOPT (no change) | Applied as written: no LESS, influence, IFD or targeted selection; replay p_g < 0.2 rule kept | 2.1, 5 |
| E2 replay yes rate per wording | ADOPT | Applied: CPU check; re-stratify cells outside 50 +/- 5 | 5, G10 |
| F3 F13 aggregate sub-type | ADOPT (low confidence) | Applied: about 20% of F13, inside its 4.5% | F13 |
| F4 O*NET persona seeds | ADOPT | Applied; PersonaHub excluded | 2.1, 3.G |
| A6 ordinal order in permutations | CONSIDER | **Not applied in round 1.** Condition: round-1 view agreement on dev ordinal rows < 89%, then a trainer change by amendment | recipe |
| C5 per-card gold-NEI rate 0-20% | CONSIDER | **Not applied in round 1.** Condition: owner OK or amendment; the ~10% aggregate (F6) stays either way | F6 |
| D2 facility-location pick of public rows | CONSIDER | **Decided once, in the C PREREG amendment (before any C row exists).** It is adopted for round-1 public rows (3A-3E) only if the G9 L4 pass can log C1's pooled hidden states at no extra time. Otherwise it lapses for C (it cannot be added later). If adopted: P5-style checks after selection | 3, G9 |
| E4 FAM-1 share cuts | CONSIDER | **Not applied in round 1.** Condition: round 2 runs; jackknife CI < 0 at >= 2 reads, lookahead agrees in sign, old slice agrees; inside existing bounds; by amendment | recipe 7.2 |
| A7 variance term, level-k yes/no rows, SORD labels | REJECT | Excluded: no CORAL/CORN-style "at least level k?" rows and no SORD soft labels are generated | - |
| B8 slice discovery, MIA probes, Jev contamination tests | REJECT | Excluded | - |
| C7 per-set prior readouts, T predictor, OTTER, conformal | REJECT | Excluded | - |
| D3 LESS / RDS+ targeting, new selection split, LIMO / s1 copies | REJECT | Excluded | - |
| F5 blends, snapshot averages, seed soups | REJECT | Excluded (no blended candidate) | - |
| A3, A4, A5, C1-C4, C6, E1, E3, F1, F2 | ADOPT (recipe) | Owned by `C_TRAIN_RECIPE.md`; not edited here. This file only supplies `meta.option_level` (A4's mean term reads it) and the family and replay groups E1 uses | recipe |

---

## 1. What C must fix (from LOCAL_GAPS.md and local results)

| Gap | Evidence | Fix in this spec |
|---|---|---|
| Far domain: software commits | ejs-5: C1 54.1 vs Jev 58.5 (-4.4, paired 95% CI -7.8 to -0.9). Late rows (268, from 1 Jun 2026): 46.3 vs 45.9, a tie. 0 code or diff rows in golden_train | Commit block (section 4), equal shares per type (20% each; v4); (v4) message-only rows for gate, triage and route (B1) and per-rule gate yes rates (B2) |
| Hard / negated yes/no | Weak evidence. JevBench hard yes/no is 9/19 vs 11/19 for 4B-E (a 2-item gap). Dev shows no C1 weakness (neg 87.6 vs 85.4, dneg 85.1 vs 84.5). C1's double-negation flips are 8.9%, and 29 of 30 of one probe's flips sit in one frame. dneg is 0.22% of rows; 91% of "neg" rows use one template | F5 at 8%, sized for round 2 by the probe (recipe 7.2) |
| Policy precedence, amendments | pg_policy 73.3 vs 84.0 (-10.7) | F1 |
| Multi-hop record chains | pg_multihop 55.3 vs 66.7 (-11.3) | F3 |
| Rule arithmetic | pg_numeric 51.3 | F2 (shallow by default) |
| Fine-grained taxonomies (20-60 labels) | 21+ options 53.4; empathetic 45.5 vs 55.4 | F11 |
| Ordinal levels | 51.6; 58% of errors are one level off. (v4) Dev: rounded E gives 34 end-level answers where gold has 52 (ratio 0.65) | F7; (v4) ordinal target lint (A1, G18), end-level balance and cut-point rubrics (A2) |
| Abstain as gold | gold NEI 59.4, "none of these" 52.6 (small n); yes/no can never abstain | F6 |
| Long documents | 0.39% of rows over 2K tokens, max 5,445 | F13 + public long block (3B) |
| Near-zero Jev-index types | tools 0.06%, risk 0.17%, stance 0.18%, emotion 0.31%, sarcasm 0.38%, ABSA 0.12% | F8, F12, public 3E |
| Invented jargon in the card | 0 rows | F10 |
| Codebook classification of real text | The sealed real-text domains have this shape; F1-F9 do not train it | Real-text codebook variants (2.3) |
| Narrow formats | 51% of rows from sources with <= 5 instruction templates; JSON 0.46%; diffs 0 | Section 6 |
| "Yes" drift on familiar families | Seen sources, gold "no": 80.4 vs 85.4 | Yes/no balance per family and wording; replay strata; (v4) replay yes rate per wording (E2), per-rule commit rates (B2), report-only drift alarm (B3) |

---

## 2. Own program-labelled families (90,000 rows in round 2)

### 2.1 Rules that apply to every family

**Definitions.**
- A **task card** is one unique (family, sampler, domain pack, label schema, instruction family). Two cards must
  differ in the domain pack and in the label schema or rule set.
- A **domain pack** is a Claude-written bundle: setting, roles, entity name pools, invented jargon, document types,
  units, number ranges. Target: a shared pool of >= 300 packs (round 1 >= 200). Every family uses >= 40 packs (round 1
  >= 30). The QC program drops any pack that hits the sealed keyword block-list (section 9). Builders never read that
  list; the program applies it.
- **(v4, F4) Persona seeds.** When Claude writes a pack or a scenario, the "who is deciding" role is seeded from an
  O*NET occupation title (CC BY 4.0; `gd_onet_occupation`, KEEP in `LICENCE_REGISTER.md` section 4). Titles only, drawn
  by program (fixed seed, spread over O*NET major groups); the pack records `persona_seed` (O*NET code) and declares
  O*NET as a parent (3.H). Credit O*NET in the notices file. **PersonaHub (CC-BY-NC-SA-4.0) is never used** (3.G).
  O*NET's rejected.json entry (large_labelsets: alternate titles / SOC direct-match file, overlap) is class
  `no_new_rows`. Persona seeds are titles inside Claude-written packs, not rows from O*NET, so a `no_new_rows` hit on
  this persona-seed parent passes. Seeds come from the main occupation titles, never the alternate-titles or SOC
  direct-match file.
  Packs still pass the sealed keyword block-list and decontamination (7.2).
- A **sampler** is the code that draws the hidden structure (rules, facts, events, tables). Each family has
  **>= 4 training samplers (S1-S4, plus S6 and up when a family needs more) and 1 held-out sampler (S5)**. Each training sampler gives at most 2,500 rows over
  both rounds, so F1 (10,800 rows) needs 5. The samplers must differ in shape (for example forward vs label-first vs
  table-first vs narrative). S5 feeds only the mix-tuning dev. Reason: a model trained on one logic sampler scored 99.9%
  in distribution and 57.3% on a second sampler of the same problems (Zhang et al. 2022, arXiv 2205.11502); a
  competitor's generator gave +26 pp from its first 6K rows, then +5.

**Pipeline for every own row.**
1. Sample a structure with a training sampler (fixed seed).
2. Solver A (the generator's own logic) computes the label.
3. Render to text: template + domain pack + format style + instruction wording + definition style.
4. Parse the rendered text back with an independent parser written from the family spec, not from the renderer.
5. Solver B, of a different paradigm, re-solves the parsed structure. It must agree with solver A on 100% of rows.
6. Emit twins (fact-flip, negation, premise removal, attack) and their relations.
7. Record provenance (section 2.4).

**Expert level means:** professional documents (policies, SOPs, case files, audit logs, schedules, multi-table
reports, change logs), 2-6 interacting conditions, exceptions and precedence, values at the exact boundary, implicit
cues ("fail to", "lack", "no fewer than"), and functional distractors (each wrong option comes from one specific,
plausible error). It does not mean outside knowledge. Every question must be decidable from the card and the text
alone. Facts are about invented entities, so memory cannot answer (FLD design rule 1, arXiv 2411.12498).

**Per-family quotas (all own families).**

| Quota | Value |
|---|---|
| Max share of own rows per family | 12% |
| Cards per family | round 1 >= 80, round 2 >= 150 (F12: 40 / 80; F13: 40 / 70) |
| Rows per card | max 128; median about 40-50 |
| Instruction wordings | pool >= 30 per family; each card uses >= 5 |
| Definition styles | >= 3 per family: one-line, one-line + 1-2 examples (about 50% of cards), rubric or decision list; plus a short or no card on about 15% of rows |
| Yes/no vs choice | 45-55% yes/no where the family allows both |
| Yes rate | Per card: drawn uniformly from 20-80% (cards differ). Aggregate: 50% +/- 2 within each family x wording x difficulty bin x negation count |
| "Yes = bad outcome" polarity | 50% +/- 5 of yes/no rows |
| Syntactic negation in yes/no questions | >= 10% of each family's yes/no rows (today 6.6% overall) |
| Double negation with affirmative twin | >= 2% of each family's yes/no rows (overall new-row target 2-5%) |
| Minimal-pair (label-flip) twins | 20-25% of own rows sit in a twin set |
| Attack twins (instruction injection, label unchanged) | about 5% of own rows, `inv` relation; wording never matches eval_opi or eval_jagged (section 7) |
| Few-shot cards (1-3 worked examples in the card) | 5-10% of cards |
| Inverted cards ("which of these cases meets rule X?") | 10-15% of cards |
| Masked label names (neutral IDs) | 10-15% of choice rows (F10: 40%) |
| Swapped label names (familiar word, different definition) | about 5% of choice rows (F10: 30%) |
| Option counts (choice rows) | 2-4: 35%; 5-9: 35%; 10-19: 15%; 20-60: 15% |
| Gold letter position | uniform per option-count bucket (the trainer shuffles again at train time) |
| Abstain options | when "not enough information" or "none of these" is shown, it is the wrong answer on >= 50% of those rows |
| Deep items (beyond the family's default depth cap) | <= 10% of the family's rows; they form the depth sweep (section 10) |
| Difficulty (set by the scoring crowd, below) | easy <= 25%, medium >= 45%, hard <= 30% |
| Label-check form (`Is the correct answer "X"?`) | 0 new rows |

**Relation units and batching (code fact: `train_decoder.make_units` groups rows by `call_id`).**
- All rows joined by a `complement`, `equiv` or `inv` relation share one `call_id`.
- A relation unit holds **at most 3 rows**. The trainer may add permutation twins on top.
- Contrast twins with no relation term (label-flip pairs, deleted-premise twins) get their own `call_id`.
- Units with any row of 2,000 tokens or more hold at most 2 rows.

**Difficulty and selection.**
- p_g = probability on the gold answer. The scoring crowd is REF = C1 (step B adopted nothing), 4B-E and the base
  Qwen3.5-4B, each read with the shipped A5 readout on the free L4 (decision 3). Crowd p_g = the mean of the three.
  No model above 4B is used.
- Bins: easy if crowd p_g > 0.97; medium if 0.30 < p_g <= 0.97; hard if p_g <= 0.30.
- Generate about 1.5x the target rows. Keep all medium and hard rows and 30% of easy rows. Then downsample **inside
  each family x gold label x wording x difficulty-bin cell**, so yes = no and gold letters stay uniform in every bin.
  C1 leans "yes", so gold-"no" rows are harder; selecting without strata would break the balance.
- A family with more than 30% hard rows after the G5 re-read has its depth cap lowered.

### 2.2 The 13 families

Rows: round 1 / round 2. Cards: round 1 / round 2 minimum.

| Family | Share | Rows (r1 / r2) | Cards (r1 / r2) |
|---|---|---|---|
| F1 Policy composition and precedence | 12% | 5,400 / 10,800 | 80 / 150 |
| F2 Rule arithmetic, money, quantities, dates | 7% | 3,150 / 6,300 | 80 / 150 |
| F3 State tracking and record chains | 10% | 4,500 / 9,000 | 80 / 150 |
| F4 Indirect evidence and multi-hop yes/no | 8% | 3,600 / 7,200 | 80 / 150 |
| F5 Hard and negated yes/no | 8% | 3,600 / 7,200 (r2 size set by the probe) | 80 / 150 |
| F6 Not enough information, abstain as gold | 8% | 3,600 / 7,200 | 80 / 150 |
| F7 Ordinal rubrics | 7% | 3,150 / 6,300 | 80 / 150 |
| F8 Risk and probability | 5% | 2,250 / 4,500 | 80 / 150 |
| F9 Tables, JSON and logs | 9% | 4,050 / 8,100 | 80 / 150 |
| F10 Invented jargon and definition following (30% real-text codebook) | 8% | 3,600 / 7,200 | 80 / 150 |
| F11 Fine-grained taxonomies, close distractors (30% real-text codebook) | 8% | 3,600 / 7,200 | 80 / 150 |
| F12 Tool and action selection | 6% | 2,700 / 5,400 | 40 / 80 |
| F13 Long documents, program-built | 4.5% | 2,050 / 4,100 (incl. DocFinQA's fallback, +250 / +500) | 40 / 70 |
| **Total** | about 100% (F13 4.5% includes the +250 / +500 DocFinQA fallback) | **45,250 / 90,500** | **>= 960 / >= 1,800** |

Shares F1-F12 are of the original 45,000 / 90,000. F13 carries the DocFinQA fallback rows (DocFinQA is out after the
3 Oct licence check; it returns only by amendment, and then F13 goes back to 1,800 / 3,600).

**F1. Policy composition and precedence**
- Skill: apply 3-12 rules to a case when rules have exceptions, amendments with effective dates, supersession, and a
  precedence policy stated in the card (specific beats general, later beats earlier, or a named priority order).
- Structure: rule base over 4-10 case attributes (Boolean, threshold, date, category); 0-3 amendments (modify, repeal,
  insert, with dates); a case with 0-2 attributes missing.
- Samplers: forward (rules, then case); label-first (pick the outcome, build a decisive chain of depth 1-4 and >= 1
  near-miss rule that fails on exactly one condition); decision-table-first; narrative policy memo. S5 (held out):
  flowchart text. Default depth cap 4; depth 5-6 only as deep items.
- Labels: solver A forward chaining with precedence; solver B z3 (MIT) or brute force over the parsed rules.
- Questions: choice among 3-8 outcomes (including "escalate" and, in open-world cards, "cannot be determined");
  yes/no ("Is the claim approved?" and negated forms); inverted ("Which case would be approved?").
- Twins: flip one attribute at a boundary; repeal the decisive rule; move an effective date; add an inert rule.
- Shortcuts to block: number of rules, exception words, and the decisive rule's position must not predict the label.
  Decisive rule position is uniform.

**F2. Rule arithmetic, money, quantities and dates**
- Skill: compute an amount, count or date under caps, floors, proration, tiers, stated rounding and exceptions, then
  decide a threshold or pick the value.
- **Depth (changed).** A one-pass readout cannot do long arithmetic (competitor "decider": rule paragraphs scored 0.24
  vs 0.67 for one sentence). Default: at most 2 operations, or more operations only when the text states each
  intermediate value. Items with 3-4 unstated operations are deep items (<= 10% of F2) and feed the depth sweep.
- Samplers: forward formula graphs; target-first (result placed below, at, or above a threshold by +/- 1 unit, 30%
  exactly at the boundary); tiered rate tables; calendar and business-day rules. S5 (held out): payroll-style
  statements.
- Labels: solver A Python `Decimal` + `datetime`; solver B an independent integer-cents and day-ordinal implementation
  on the parsed text.
- Distractors: each from one named error (missed cap, wrong rounding, off-by-one day, ignored exception, wrong tier,
  wrong unit).
- State day counts when the card's rule needs them (a competitor's date items went from 0.65 to 1.00 with stated day
  counts).
- Shortcuts to block: number magnitude; answer = largest or smallest option.

**F3. State tracking and record chains**
- Skill: track entity state over 5-40 events with VOID, CORRECTION, supersede, rename, merge and transfer; follow ID
  chains across notices.
- Samplers: forward event sequences; target-first (decisive event at a uniform random position, distractor events on
  look-alike IDs); ledger tables; multi-notice correspondence. S5 (held out): git-like log syntax.
- Labels: solver A event replay; solver B an independent version-graph resolver that follows pointers backwards from
  the query on the parsed text.
- Questions: final or at-time value; which record is current; "Does X still hold Y?" (with negated forms); "not
  enough information" when the card says the log may be incomplete.
- Metamorphic checks: no-op events, commuting reorders and ID renames leave the label unchanged.
- Shortcuts to block: last-event recency, ID string similarity. (A competitor's event-log family with VOID and
  CORRECTION entries took fresh yes/no from 58.8 to 71.6.)

**F4. Indirect evidence and multi-hop yes/no**
- Skill: decide whether a claim follows, is contradicted, or is undetermined from facts plus general statements, over
  2-4 hops, with defeasible exceptions.
- Samplers: forward chaining over a fact graph; FLD-style deduction with distractor facts and rules (Apache-2.0 code
  idea, our own implementation); evidence tables; witness statements. S5 (held out): facts embedded in narrative prose.
- Labels: solver A forward chainer; solver B model enumeration (truth tables) on parsed facts.
- Lexical overlap between claim and text is decorrelated from the label (HANS control).
- 30% of rows carry one inert but relevant-looking sentence; the label must not change (GSM-NoOp showed drops up to 65%
  from one such clause).

**F5. Hard and negated yes/no**
- Skill: answer yes/no correctly under negation, double negation, scope shifts, implicit negation (fail to, lack,
  deny, refuse, rule out, hardly, no fewer than, unless, other than), quantifiers and modal negation.
- Base items: (fact, question) pairs from the F1-F4 and F9 structures, and from human-gold public items in section 3
  (SQuAD 2.0 answerability, MuSiQue, 2WikiMultihopQA yes/no, QuALITY and Qasper yes/no, GHC, EDOS). For soft-labelled
  bases, the negated row gets 1 - p. ShARC, CAD-SNLI, Measuring Hate Speech, Social IQa, CosmosQA and NewsMTSC are
  not bases, and neither is any set built on them (3.G, 3.H). The F5 builder runs the deny-list check on every base
  source and its parents.
- Each base gives 4 rows in 2 units:
  - unit 1 (3 rows, one `call_id`): affirmative; negated (`complement`); double-negated (`equiv` to the affirmative);
  - unit 2 (1 row, own `call_id`): a scope-shift or implicit-cue variant, labelled by polarity logic.
- Cue bank: >= 250 templates in >= 12 cue families. 25 templates are held out for the hard-negation probe and never
  trained. No template may match a dev or eval negation wording (dev_negwords is a held-out template family; dev's
  dneg is 92% "Should the statement that ... be rejected?"; the C1 failure frame "only non-hateful" + outer "be
  rejected" is also a dev wording and is blocked).
- Labels: a polarity-logic program over the base label; solver B re-derives polarity from the parsed question.
- Balance: P(yes | number of negation cues) = 0.50 +/- 0.02 for 0, 1, 2 and 3 cues, so counting negations cannot help.
  "Yes = bad" at 50%. At least 25% of F5 rows are double negation.
- Size: 8% in round 1. Round 2's F5 share comes from the hard-negation probe under the bounded weight rule (recipe 7.2).

**F6. Not enough information and abstain as gold**
- Construction: start from an answerable twin and remove exactly one necessary premise (open-world card). Build "none
  of these" by deleting the gold option and checking that no remaining option qualifies. Add yes/no "Can it be
  determined that ...?" rows with the semantics stated in the card.
- Labels: solver A an open-world solver that proves neither answer follows; solver B z3 shows both answers are
  satisfiable.
- Target: gold is NEI or "none of these" on about 10% of all new choice rows (F6 plus other families).
  (v4, addendum C5, CONSIDER: **not applied in round 1**. Varying the gold-NEI rate per card over 0-20% while keeping
  the ~10% aggregate needs an owner OK or an amendment first.)
- The NEI option must also appear on rows where it is wrong (>= 50% of rows that show it).

**F7. Ordinal rubrics**
- Skill: pick a level on a 3-7 level rubric where adjacent levels differ in exactly one stated criterion.
- Samplers: random points; level boundaries (the decisive criterion just met or just missed); multi-criterion
  scoring sheets; narrative incident write-ups; **(v4, A2) cut-point rubrics (sampler id S6)**: a stated quantity binned by stated cut
  points (the card states the quantity, its unit and 3-7 ranges; the pack sets the numbers), with the top level as
  common as the others and values placed at, just below and just above each cut. No software-change size rubric here
  (that skill is the commit block's, under guard 4). The cut-point sampler is about 1/5 of F7 rows (r1 about 630 / r2 about 1,260),
  inside F7's 7%. S5 (held out): rubric as a table.
- Labels: solver A rubric evaluator; solver B independent re-implementation from the parsed rubric.
- Metamorphic: raising a severity factor never lowers the level.
- Labels carry their number ("Level 3 - Elevated") because the trainer shuffles options. Gold is uniform across levels,
  **end levels included (v4, A2)**: per sampler x K, each level is 1/K +/- 2 pp of rows, and every card shows gold at
  every level at least once (G10). Short end levels are fixed by generating more, never by relabelling. Distractors include both adjacent levels.
- **(v4, A1) Ordinal meta.** Every F7 row carries `meta.option_level` (option text to level index 0..K-1) and passes the
  ordinal target lint (G18).
- **(v4, A2) Report-only check (dev, never ejs-5).** On dev ordinal rows, the ratio of end-level predictions to
  end-level gold (C1: 0.65) is logged for C at each snapshot. Target >= 0.9. It chooses nothing.

**F8. Risk and probability**
- Skill: apply a card-defined scoring rule (points table), base rates with stated likelihoods (Bayes), expected cost
  or value, and risk-tier thresholds.
- Questions: probability-bin choice; "Is the expected loss above X?"; rank options by risk.
- Labels: solver A exact fractions (`fractions.Fraction`); solver B an independent exact implementation.
- **Soft targets (changed).** `meta.gold_probs` (exact posteriors) only on choice rows that ask which outcome will
  happen. Every yes/no row ("Is the expected loss above X?") has a hard 0/1 label, and the F8 source is **not** in
  `kd_full_src`. Reason: more soft yes/no targets push answers into the 0.4-0.6 band that JevBench v1.5.4 scores as an
  abstention.
- No real-outcome labels (noisy, high Bayes error). UCI credit outcome data is excluded for this reason.

**F9. Tables, JSON and logs**
- Skill: filter, count, aggregate, compare, join two tables, argmax with a stated tie rule, date windows; pick records
  out of JSON arrays of 10-200 records; read log lines.
- Containers: markdown table, CSV, HTML table, JSON, YAML, fixed-width text, log lines.
- Multi-select as single-letter choice: options list record sets ("A: R2 and R5 only").
- Labels: solver A pandas; solver B sqlite on the parsed text.
- Metamorphic: row shuffle, column rename and unit restatement leave the label unchanged.
- Shortcuts to block: answer in the first row; number magnitude.

**F10. Invented jargon and definition following**
- Skill: decide using terms that exist only in the card, and definitions that override a word's usual meaning (for
  example "minor" defined as "over $5,000").
- Invented words are checked against a large word list (>= 300K entries, 3 languages) and carry no morphology hint (no
  "-phobia", "mal-", "-itis").
- 40% of F10 choice rows use neutral IDs ("Category K7"); 30% use swapped label words; 10% of F10 rows are
  label-description rows (the text paraphrases one definition).
- Twins: swap two definitions; the label must follow the definition.
- Labels: solver A definition substitution; solver B attribute matcher on the parsed definitions.
- 30% of F10 rows are real-text codebook variants (section 2.3).
- Evidence: GoLLIE went from 42.3 to 55.3 F1 on unseen schemas; removing examples inside definitions cost the most
  (-5.4). 7-12B models lean on label names more than on definitions (Codebook LLMs).

**F11. Fine-grained taxonomies and close distractors**
- Skill: choose among 20-60 near-synonym labels with sharp definitions and boundary notes.
- Construction: items are attribute vectors (for example mechanism, object, severity, actor) rendered through
  templates; a mapping table gives the label.
- Option display: all labels on 50% of rows; a subset of 8-15 that includes the 2-3 nearest labels on 50%. Codes on
  50%, names on 50%.
- Close distractors: every row has >= 1 option that differs from gold in one attribute.
- Labels: solver A the mapping table; solver B a decision tree compiled independently from the card text.
- 30% of F11 rows are real-text codebook variants (section 2.3).

**F12. Tool and action selection**
- Catalog: >= 200 invented APIs in >= 40 domains, written by Claude, with JSON-schema parameters. No public tool
  dataset text is used (they contain LLM-written text; see 3.G).
- Requests come from structured intents. Outcomes: call tool X; ask for a missing parameter; unable; answer directly
  without a tool. Also "which parameter is missing?" and "is this call valid?" (yes/no).
- Distractor tools differ in one capability or one parameter.
- Labels: solver A schema matcher; solver B independent validator.
- Disclosure: the four outcomes copy When2Call's design (a Jev Decision Index test). Report DI When2Call as "trained on
  a similar task design", never as unseen.

**F13. Long documents, program-built**
- Coherent documents of 2,000-7,900 tokens: manuals, case files, audit logs, multi-table reports. Every section is
  domain content from the same pack. No filler text.
- Decisive content sits in 1-3 sections at depths uniform across the 10 deciles. Near-miss sections: a superseded
  version, another region's rule, a look-alike ID.
- Questions reuse the F1, F3, F6 and F9 skills. Length bins: 2-4K tokens 50%, 4-6K 30%, 6-7.9K 20% (token cap,
  section 6).
- **(v4, F3) "Aggregate" sub-type, about 20% of F13 rows (r1 about 410 / r2 about 820), inside F13's 4.5%.** The answer
  needs facts from **2-3 sections**: a count (for example of active exceptions), the latest valid version among
  several, or a total over a table split across sections. Labels come from the generator's ground truth (solver A) and
  an independent re-solve on the parsed document (solver B), like every family; no LLM labels, no filler. The decisive
  sections keep the uniform-depth rule; `meta.subtype` = "aggregate". Low confidence: expected LongBench v2 effect +0
  to +2 pp.
- Twins: move the decisive section (gold unchanged; `equiv`, a 2-row unit); delete it (gold becomes NEI; its own
  unit, no relation term).
- Evidence for this design: burying a short state in filler cost a competitor 22-43 pp, and training on filler moved
  real long documents by only +/- 1 pp; ProLong found synthetic long SFT data hurt. So F13 uses coherent documents and
  stays small, and real long documents come from the public block (3B).

### 2.3 Real-text codebook variants (new in v2)

Why: about 67% of new rows would otherwise be invented-domain text. Real data beat zero-shot synthetic data by 16.9 pp,
and real seeds added 10.3 pp (Li et al. 2023). The sealed real-text domains are codebook classification of real text.

- Size: 30% of F10 and of F11 rows (round 2: 2,160 + 2,160; round 1: 1,080 + 1,080).
- Text: unused train-split records of the human-annotated sets in section 3E (MAMS ACSA and ATSA, XED English, GHC,
  EDOS). "Unused" means the normalized text is not in golden_train and not in any other C row.
- Codebooks: Claude writes >= 40 codebooks in round 2 (>= 20 in round 1). Each has 5-30 codes. Every code is defined
  as an explicit function of the dataset's **human annotation vector** (for example MAMS: "K4 = the sentence is
  negative about staff or service"; EDOS: the 11 fine-grained vectors regrouped into new code sets).
- Labels: a program maps each record's human annotations to its code (solver A); an independent implementation of the
  mapping agrees on 100% (solver B). A code may never depend on Claude reading the text.
- Questions: choice over codes, per-code yes/no, masked and swapped code names, definitions with 1-2 examples drawn
  from other train records.
- QC: G5 reads 300 rows per source dataset and checks that the text supports the human annotation. More than 8%
  clearly wrong drops that dataset's codebook rows (a dataset-level decision, never row by row).
- These rows count toward the source dataset's 3,000-row cap (section 3.1). `meta.licence` is the dataset's licence.

### 2.4 Row format (own rows)

Same raw format as `GOLDEN_SPEC.md`, with extra meta:

```
{"id", "group_id", "call_id", "source", "state", "qtype", "instructions", "options", "gold", "role", "card",
 "meta": {"family": "F1".."F13", "spec_id", "card_id", "domain_pack", "sampler": "S1".."S4" | "S6".."S9" | "S5" (S5 is always the held-out sampler: mix-tuning dev items only, never a training row),
          "gen_version", "git_sha", "seed", "structure_hash", "difficulty_bin", "crowd_pg", "depth", "deep": bool,
          "format_style", "wording_id", "defs_style", "twin_of", "twin_kind",
          "text_source": null | {"dataset", "record_id", "split": "train"},
          "licence": "CC0 1.0 (program-generated)" | <dataset licence for real-text rows>,
          "edge": [...], "gold_probs"?: {...},
          "option_level"?: {<option text>: <level index 0..K-1>},   (v4, A1: required on every ordinal row)
          "subtype"?: "aggregate" | "cutpoint" | ...,               (v4: F13 aggregate, F7 cut-point)
          "persona_seed"?: <O*NET code>}}                           (v4, F4: when the pack or scenario has one)
```

**(v4, A1) Ordinal rows.** An ordinal row is any row whose options are the levels of one ordered scale: every F7 row,
every commit score row, no public row in round 1 (UCI Car and Nursery classes are not marked ordinal, like F8 bins,
so A4 keeps its sized row set), and replay rows whose options carry level numbers (the mixer detects these by
program, adds `option_level`, and counts them in its report). F8 probability-bin rows are not marked ordinal in round
1 (this keeps the row set that the recipe's A4 mean term was sized on: F7 own rows + commit Score rows + replay). `option_level` keys the canonical option text, so the trainer's option shuffle does not change it.
Commit rows carry the same meta keys that apply to them, plus `input_view` ("message_only" | "message_diff") and, on
message-only rows, `trigger_entities` (4.2).

Definitions go to `data/c_parts/defs/<key>.json`. Relations (`complement`, `equiv`, `inv`) go to the relation file in
the format `train_decoder.py` reads. Builders live in `c_src/<family>/`; outputs in `data/c_parts/`.

---

## 3. Licensed public training splits (17,500 rows in round 2; 8,750 in round 1)

### 3.1 Rules (GOLDEN_SPEC.md and SELECTION.md, plus v2 and v3 additions)
- Licence must be one of the commercial-use licences the owner allowed:
  - permissive: CC0, public domain or US government, CC BY, ODC-BY, MIT, Apache-2.0 or BSD;
  - share-alike: CC BY-SA or ODbL, allowed only if the data is kept private and the source is listed in the notices
    file (decision 8).
- The licence must be stated in a file or official record that we cite. Record the upstream URL and commit in
  `meta.licence`.
- A Hugging Face tag alone is never enough: 5 of the tags checked this session were wrong (ContractNLI, LogiQA 2.0,
  FOLIO, QuAC, FeTaQA).
- **Non-commercial (NC) or research-only terms mean study only.** Such data is never a training row, a seed text, a
  codebook example or a mix-tuning-dev item.
- **(v2) The document text needs its own licence check**, separate from the annotations (QuALITY articles, Qasper
  papers, DocFinQA filings, MultiHiertt and ConvFinQA reports). See `LICENCE_REGISTER.md`.
  - **(v3, decision 9, by default)** Flagged document texts are out unless the licence check clears them.
  - **(3 Oct licence merge) Result:** QuALITY Slate/OANC articles are cleared (OANC: any use, including commercial).
    Qasper papers are kept only with an arXiv CC BY, CC BY-SA or CC0 licence (Qasper chose "CC-BY-*" papers, which
    include NC and ND). FinTabNet report text (MultiHiertt, ConvFinQA, and replay `gd_finqa`) is **not** cleared: its
    CDLA-Permissive-1.0 licence is stated only in two papers, IBM's record was not reached, and the licence is not on
    the list above. DocFinQA is out (decision 6).
  - Text that reaches us **through another licensed dataset** (FinTabNet, S2ORC, OANC) needs that dataset's licence
    read upstream. Third-party user or press text under a clean dataset licence (subtitles, reviews, posts, headlines,
    Wikipedia, commit messages) is recorded in the register and is not a blocker (decided by default).
- **Unverified means out.** A dataset whose licence record no checker could read is not a training row, a seed text, a
  codebook example or a mix-tuning-dev item, the same as NC. It moves to 3.G and its rows go to the named fallback.
- **(v3, decision 6, by default) A creator's own Hugging Face card is not an official licence record.** "(H)" sets are
  out unless the builder finds an upstream licence file or an official page. Their rows go to the named fallback.
  A creator's Kaggle page that is the only official release, with a structured licence field (Sarcasm v2), counts as
  an official record (decided by default; the owner may override, fallback in 3.2 #15).
- Human-written text and human labels only. No LLM-written text or LLM labels.
- **Train split only.** Never a test split, and never a validation split that serves as a benchmark's test. Sets with
  official splits use only `train` (EDOS, MAMS, GHC). Sets with no split (XED, Sarcasm v2, UCI) get our own 90/10 split
  by record; the 10% feeds only the mix-tuning dev.
- **(v2, v3) The deny-list program (3.H) passes the dataset and every declared parent.** A dataset is denied if it or
  a parent is:
  - in any `golden_src/*/rejected.json`;
  - in `golden_src/forbidden_label_nli.json` (152 tasks);
  - an "avoid" (or OHS-3 source) entry of `ohs3/used_sources.json`, which the program checks and agents do not open;
  - an OHS-1/2/3 source;
  - Stack Exchange text;
  - a dev or eval source;
  - in the 3.G table.
- **Never test items.** No test split, no hidden-label dev split, and no item of any benchmark we report.
- **(v2) Unused records only.** A record whose normalized text is already in golden_train is never a new row, and never
  a mix-tuning-dev item.
- **(v2) Wikipedia-based sets split by page.** SQuAD 2.0, MuSiQue, 2WikiMultihopQA, HybridQA, WikiSQL and DROP are
  split into train and mix-tuning dev by Wikipedia page title (MuSiQue reuses SQuAD and NQ paragraphs). Passages are
  deduped against C1's `qnli`, `gd_answer_equiv`, `gd_hotpotqa_yesno`, `gd_feverous`, `gd_totto_claims`, `gd_wtq`
  and `boolq` texts.
- Cap: <= 3,000 rows per dataset in round 2 (direct + codebook rows), <= 500 rows per class. At least 3 instruction
  wordings and at least 2 framings (for example per-label yes/no and full choice) per dataset.
- Keep human vote shares as soft targets (`meta.teacher`, `meta.teacher_src: "human_votes"`).

### 3.2 The list (14 datasets, every licence read upstream on 3 Oct)
"(V)" = licence read upstream by a 3 Oct checker (`LICENCE_CHECK_1/2/3.md`); every row below is V and allows
commercial use. SA = share-alike: fine for private training; never publish derived rows. The three sets that failed
the check (DocFinQA, MultiHiertt, ConvFinQA) are in 3.G; their rows already sit in the fallbacks named here. Full
evidence, URLs, commits and text-licence notes are in `LICENCE_REGISTER.md` section 1.

**3A. Hard yes/no, NEI, indirect evidence (5,000)**

| # | Dataset | Licence | Train size | Use (r1 / r2) | Exclude | Notes |
|---|---|---|---|---|---|---|
| 1 | SQuAD 2.0 (answerability) | CC BY-SA 4.0 (V, SQuAD-explorer page); SA | 130,319 | 900 / 1,800 | dev, test | "Does the passage answer the question?" 50/50. Strict G5 read (300 rows; drop the set if > 5% wrong or ambiguous): unanswerable items are often ambiguous (Platinum). Drop every question whose id is in MuSiQue's `dev_test_singlehop_questions_v1.0.json` (MuSiQue README asks for this; keeps MuSiQue dev/test seeds out). |
| 2 | MuSiQue (Ans + Full) | CC BY 4.0 (V, repo LICENSE); text SA (Wikipedia, CC BY-SA seed questions) | 19,938 | 1,000 / 2,000 | dev, test | Answerable vs unanswerable twins; supporting-paragraph choice. Parents: SQuAD, T-REx, Natural Questions, MLQA, Zero Shot RE (declared for 3.H). |
| 3 | 2WikiMultihopQA | Apache-2.0 (V, repo LICENSE); Wikipedia text SA | 167,454 | 600 / 1,200 | dev, test | Comparison and yes/no types only. |

**3B. Long documents, real text (1,900)**

| # | Dataset | Licence | Train size | Use | Exclude | Notes |
|---|---|---|---|---|---|---|
| 4 | QuALITY | CC BY 4.0 annotations (V, project page); article text V (Gutenberg public domain, Slate via OANC, CC BY) | 2,523 questions, 150 articles | 600 / 1,200 | dev, test | All 150 articles are usable: the program keeps an article only if its `license`/`source` field is Gutenberg, OANC/Slate or CC BY, and logs it. Strip the Gutenberg header and trademark text. Articles <= 7,500 tokens. Counts-only check vs LongBench v2. |
| 5 | Qasper | CC BY 4.0 annotations (V, official AI2 page, archived 14 Apr 2023; the live URL redirects to the HF card, which is not the record) | 888 papers | 350 / 700 | dev, test | Only papers whose **arXiv licence** (read per paper by program from arXiv metadata; keys are arXiv ids) is CC BY, CC BY-SA (SA, notices file) or CC0. Every NC or ND paper is out. No ACL Anthology route: the text in the file is the arXiv/S2ORC version. Log each paper's licence. If fewer than 150 papers qualify, drop Qasper; its rows go to QuALITY and F13. Truncate to <= 7,500 tokens keeping the evidence; log truncation. |

DocFinQA (was #6) is out (3.G); its 250 / 500 rows are in F13.

**3C. Tables and numbers (4,800)**

| # | Dataset | Licence | Train size | Use | Exclude | Notes |
|---|---|---|---|---|---|---|
| 7 | HybridQA | MIT annotations (V, repo LICENSE); tables and passages from WikiTables-WithLinks (no LICENSE; Wikipedia, CC BY-SA): SA | 62,682 | 1,000 / 2,000 (base 600 / 1,200, plus 400 / 800 from MultiHiertt and ConvFinQA) | dev, test | Table hash check vs TabFact (OHS-2), section 7. |
| 8 | WikiSQL (execute the SQL) | BSD-3-Clause (V, repo LICENSE; data in the repo); Wikipedia tables CC BY-SA: SA | 56,355 | 1,150 / 2,300 (base 750 / 1,500, plus 400 / 800 from MultiHiertt and ConvFinQA) | dev, test | Program labels from SQL execution ("is the count above 3?"). Table hash check vs TabFact. |
| 11 | DROP | CC BY-SA 4.0 (V, `license.txt` in the official AI2 zip): SA | 77,400 | 250 / 500 | dev | Numeric comparisons as yes/no thresholds. |

MultiHiertt (was #9) and ConvFinQA (was #10) are out (3.G). Their 800 / 1,600 rows are in HybridQA and WikiSQL above
(MultiHiertt: WikiSQL +250 / +500, HybridQA +200 / +400; ConvFinQA: WikiSQL +150 / +300, HybridQA +200 / +400). Both
stay under the 3,000-row cap. Real finance tables still reach C through replay (`gd_tatqa`, `gd_tathqa`, both KEEP in
the register), and program-built tables through F9.

**3D. Official decision rules (1,000)**

| # | Dataset | Licence | Size | Use | Notes |
|---|---|---|---|---|---|
| 12 | UCI Car Evaluation + Nursery | CC BY 4.0 (both V, UCI pages, DOIs 10.24432/C5JP48 and 10.24432/C5P88W) | 1,728 + 12,960 | 500 / 1,000 | Labels come from published DEX hierarchical rules; the rules go in the card. Split rows across both sets (Car has only 1,728 records: at most 1 row per record per framing). Credit the DEX model creators in the notices file. |

**3E. Subjective decisions with human labels (4,800)**
All five were licence-checked for v0.13/golden and read again upstream on 3 Oct. They add new framings and unused
records only. They also supply the real-text codebook rows (2.3), which count toward the same 3,000-row cap. Their
texts are third-party (subtitles, reviews, headlines, posts) under clean dataset licences: recorded in the register,
not a blocker (decided by default; the owner may override).

| # | Dataset | Licence | Use (r1 / r2) | Task type | Notes |
|---|---|---|---|---|---|
| 13 | XED English | CC BY 4.0 (V, README) | 600 / 1,200 | emotion | Per-emotion yes/no + choice. No official split: own 90/10 by line. Text is OpenSubtitles lines; no licence for the subtitle text was found (OPUS page 404), recorded in the register. The README's "24164 + 9384" are annotation counts: count lines. |
| 14 | MAMS (ACSA + ATSA) | Apache-2.0 (V, repo LICENSE covers `data/`) | 750 / 1,500 | ABSA, target sentiment | ATSA is new: two aspect terms with different polarities in one sentence make natural contrast pairs (replaces NewsMTSC's role). Train split only. |
| 15 | News Headlines Sarcasm v2 | CC BY 4.0 (V, creator's Kaggle page: the only official v2 release, structured licence field) | 350 / 700 | sarcasm | Load the creator's Kaggle v2 copy only; never the GitHub v1 file (no LICENSE) or a third-party mirror. Redact outlet names. Dedupe vs C1's `br_sarcasm_headlines`. **If the owner reads decision 6 as covering Kaggle pages too**, Sarcasm v2 goes out and its rows go to XED +175 / +350 and GHC +175 / +350 (both stay under the cap). |
| 16 | Gab Hate Corpus | CC BY 4.0 (V, OSF node licence via the OSF API) | 350 / 700 | hate, soft | `ghc_train.tsv` only. Exact-text dedupe vs HateXplain (mbib-base) and Social Bias Frames (section 7). |
| 17 | EDOS | CC0 1.0 (V, repo LICENSE) | 350 / 700 | sexism, soft | `split == train` only (14,000 of 20,000; the labelled CSV also holds dev and test labels). Same dedupe as GHC. C1 already used 4,057 EDOS rows; new rows use unused posts only. |

Total 3A-3E (round 2): 5,000 + 1,900 + 4,800 + 1,000 + 4,800 = **17,500** (round 1: 8,750), from 14 datasets.
Long rows from 3B: 1,900 (round 2). Any set that fails G1 or the deny-list at build time sends its rows to the
fallback named in its row; a set with no named fallback sends its rows to the own family closest in skill (F4 for 3A,
F13 for 3B, F9 for 3C, F1 for 3D, F11 for 3E), and the change is logged in the mixer report.

### 3.G Excluded (do not use), with the reason

Every row below is also excluded as a **parent**. No C row may use a dataset built on, derived from, or sharing source
text with an excluded dataset; the 3.H program enforces this through declared parents. Examples: CAD-SNLI and every
other SNLI derivative; NewsMTSC and anything using POLUSA; ATOMIC-context sets via Social IQa; Spinn3r-blog sets via
CosmosQA. The first six rows are the methods-B1 and rules-B1/B2 drops.

| Dataset(s) | Reason |
|---|---|
| **ShARC** | `nli_logic_reasoning/rejected.json`: about 15-20% wrong golds in about 34 hand-checked yes/no rows, clustered on negatively phrased rules |
| **Measuring Hate Speech** | 3 rejected.json files: listed "avoid to be safe" in ohs3/used_sources.json |
| **CAD-SNLI** | SNLI is "avoid" in used_sources; its sibling `counterfactually-augmented-imdb` and the SNLI reusers `defeasible-nli/snli` and `probability_words_nli/usnli` are forbidden |
| **Social IQa** | `moral_social_norms/rejected.json`: no licence in card or loader; ATOMIC contexts (delta-ATOMIC is forbidden); about 3/30 wrong and 8/30 with a second right answer |
| **CosmosQA** | `mcq_exams/rejected.json`: licence only "as reported via email"; Spinn3r blog text needs a signed research agreement |
| **NewsMTSC** | Source text is POLUSA (Zenodo 3946057: "non-commercial research and educational use … must not be shared") and Bias Flipper; the MIT licence covers annotations only |
| **e-CARE, PIQA, COPA-style sets** | `mcq_exams/rejected.json`: only 2 options; PIQA is AFL-3.0 |
| **EmoBank, ConvAbuse severity** | `calibration_distributions` and `ordinal_scales` rejected.json: per-rater labels almost all neutral; texts already used |
| **Steam Review Aspect** | Creator's card only, and the train pool is 900 reviews (C1 already used 200 rows); low value |
| **PersonaHub** (v4, addendum F4) | CC-BY-NC-SA-4.0 (non-commercial); also LLM-written personas. Never a persona seed, pack seed or row; O*NET titles are the persona source (2.1) |
| **SNLI and every SNLI derivative** (CAD-SNLI, UNLI, delta-NLI snli, e-SNLI, ...) | SNLI is "avoid" in used_sources (`nli_logic_reasoning/rejected.json`) |
| **DocFinQA** (was 3.2 #6) | **Unverified licence** (3 Oct check 3): MIT appears only in the creator's HF card YAML (decision 6); no official repo; the paper states no data licence. Also: train and dev "not fully validated", code "generated by WizardCoder LLMs". Rows (250 / 500) moved to F13 |
| **MultiHiertt** (was 3.2 #9) and **ConvFinQA** (was 3.2 #10) | **Document text unverified** (3 Oct checks 1 and 3): annotations are MIT (V), but the report text is FinTabNet, whose CDLA-Permissive-1.0 licence is stated only in the FinQA and MultiHiertt papers; IBM's own record was not reached, and CDLA-Permissive-1.0 is not on the 3.1 list. Rows (800 / 1,600) moved to WikiSQL and HybridQA. The same text puts replay `gd_finqa` in "verify upstream or drop" (section 5). All three return only by PREREG amendment after IBM's record is read **and** the owner accepts the licence |
| **Qasper papers whose arXiv licence is NC or ND** | Qasper chose "CC-BY-*" papers (includes NC and ND). Per-paper program filter; the rest of Qasper stays in (3.2 #5) |
| **MultiDoc2Dial / doc2dial, NLU++** | rejected.json (licence only on the HF card; NLU++ group listed in used_sources) |
| CommonsenseQA 2.0, CREAK, StrategyQA, PAWS, FOLIO, delta-NLI (atomic, snli), Scruples, ETHICS, args.me, DynaSent (R1 and R2), FLUTE, DynaHate, RumourEval, PUBHEALTH (`health_fact`), CondaQA, BoolQ, IMDb, Yelp, Yahoo Answers, DBpedia-14, Banking77 | In `forbidden_label_nli.json` |
| FEVER | `fever-related` is forbidden, and VitaminC (OHS-1) is built from FEVER |
| HateXplain, Wikipedia Talk Labels / Jigsaw (incl. Civil Comments, toxic_conversations), CAD (Contextual Abuse) | Inside `mbib-base` (MBIB `040_Jigsaw` is Jigsaw Unintended Bias = Civil Comments), a forbidden label-NLI task |
| WANLI, ProsocialDialog, HH-RLHF red-team, Aegis 2.0 responses, When2Call, xLAM, ToolACE, Glaive, Hermes FC, SPML, Bitext, lmarena-55k, ToxiGen, BeaverTails | LLM-written text or labels |
| MTOP | 38% of utterances shared with TOPv2 (in C1) |
| more BANKING77 / CLINC150, SLURP, HWU64 | Dev sources, DI tests, or near-duplicates of MASSIVE (in C1) |
| SciTail | No licence file; rejected in SELECTION.md |
| SWAG, alpha-NLI | Source text terms unclear (LSMDC, ROCStories) |
| UCI German Credit, Default of Credit Card Clients | Real-outcome labels with high Bayes error |
| CUAD, MAUD, ContractNLI, PrivacyQA, OPP-115, Unfair-ToS, LexGLUE tasks | LegalBench / LexGLUE family (OHS-1) or DI test |
| ESCI, GSM8K, HoVer, HellaSwag | Jev Decision Index adjacent (HellaSwag repo also DMCA-blocked 14 Sep 2026) |
| openFDA recalls, big_patent, Federal Register, NVD, Rosetta Code, Stack Exchange, Zenodo record text (the OHS-3 source) | OHS sources (GOLDEN_SPEC.md) |
| CodeReviewer | Default OUT (owner decision, section 12; per-repo licences unknown) |
| Natural Questions long pages | Wikipedia; overlaps the Wikipedia sets above |
| Sealed-suite candidates | Reserved for evaluation; the program block-list enforces this |

### 3.H The deny-list program (v3; methods B1, rules B4 and S1)

**3.H.1 Inputs.** One program, `c_src/common/denylist.py`, builds `data/c_parts/denylist.json` and checks names against
it. Its inputs:
- Every entry of every `golden_src/*/rejected.json`. There are two file formats: a top-level list of
  `{dataset, reason}`, or a dict whose `rejected` key holds that list. That is 10 files and 243 entries on 3 Oct.
  The program fails if a file has neither format, so a new format cannot be skipped silently.
- Every entry of `ohs3/used_sources.json` marked "avoid", plus every entry it marks as an OHS-3 source. The program reads this
  file in its own process. It prints only hit or no-hit per checked name, never the file's content. Agents never open
  it.
- `golden_src/forbidden_label_nli.json` (152 tasks), the OHS-1/2/3 source list in `GOLDEN_SPEC.md`, the dev and eval
  sources, the Decision Index test list, and the 3.G table.
- The Jev-output path globs of 7.4. These are checked against input paths, not dataset names.

**Matching.** An agent writes `c_src/common/deny_aliases.json` from the rejected.json and 3.G texts only. For each
denied dataset it records names, Hugging Face ids, GitHub repos, upstream URLs, Zenodo or OSF record ids and known
mirrors. The program normalizes case, punctuation and version suffixes. A match on any alias is a hit. The used_sources
part is matched inside the program with the same normalizer.

**Reason class (one per entry, set from its recorded reason).**
- **`taint`**: the text or labels are unusable for us. This covers licence or terms (incl. non-commercial and
  research-only), OHS-1/2/3 source or used_sources "avoid", overlap with a forbidden task, DI test item, test or
  hidden-label split, dev or eval source, LLM-written text or labels, gold noise above the bar (ShARC, Social IQa), a
  sealed-suite source, or Jev output. A taint entry denies the dataset as new data, denies every dataset built on it
  (parents, below), and drops its replay rows (3.H.3).
- **`no_new_rows`**: we may not add rows from it, but its text is not tainted. This covers "already used", "extra rows",
  "duplicate taxonomy", "a different subset or pool is used", low value, too few options, or overlap with C's own sets
  (for example Natural Questions, which overlaps C's Wikipedia sets). It denies the dataset as new data only. Children
  are not denied, and replay rows are kept.
- When the recorded reason is unclear, the class is `taint`. The class table is part of the PREREG amendment.

**Parents ("anything built on them").** Every public dataset, real-text codebook source, F5 base source, commit
source and domain-pack seed source declares `parents` in its builder manifest. Parents are the datasets its text or
labels come from (for example CAD-SNLI -> SNLI; NewsMTSC -> POLUSA, Bias Flipper; MuSiQue -> SQuAD, Natural
Questions; ConvFinQA -> FinQA -> FinTabNet). The program checks the dataset and every parent, recursively. Any hit
with class `taint` denies the dataset. A missing `parents` field fails G1.

**3.H.2 Where it runs.**
- At builder start: the builder refuses to run on a `taint` hit. A `no_new_rows` hit refuses only a builder that emits
  rows from that dataset.
- In the mixer: it refuses to write a file that holds a denied `source` or `text_source.dataset`.
- In G1: every row's provenance is checked.

There is no override flag. A denied dataset comes back only through a PREREG amendment that answers the recorded
reason.

**3.H.3 Replay.** The program also runs over the 204 replay sources (C1's golden_train). Many entries in rejected.json
only record that C1 already holds those rows, so the action depends on the entry's **reason class** (3.H.1):
- **`taint`**: drop the replay rows. Where only part of a source is tainted (one subset, half or split), drop only that
  part, by a program check.
- **`no_new_rows`**: keep the rows. The section-5 licence rules still apply to kept rows.
- One exception to `taint` in replay: a replay source that dev uses as a **seen** source by design is kept, because dev's
  seen-source split was built around C1's training sources. The test-split, OHS, licence and Jev parts of `taint`
  still drop such a source.

Known name-level matches (CPU check on 3 Oct, rejected.json only; the used_sources part is unknown until the program
runs):

| Replay source(s) | Matching rejected.json entry (reason class) | Action |
|---|---|---|
| clinc150 (2,651), massive (1,703), banking77 (2,300) | `large_labelsets`: "in used_sources (train/dev/eval or 'avoid') or OHS-1"; `intent_business_support`: extra rows | Drop if used_sources marks "avoid" (program decides). banking77 is dropped anyway (section 5); clinc150 and massive are in "verify or drop" |
| gd_politeness_votes (1,444), br_politeness_wiki (488) | `calibration_distributions`: "Stanford Politeness, **Stack Exchange half**" (OHS source text) | Drop every row from the Stack Exchange half (program check on the source file or domain field); keep the Wikipedia half |
| gd_crossner (950) | `relations_entities`: "CoNLL-2003, incl. the copy bundled in the CrossNER repo" (Reuters RCV1 licence) | Drop any row from the bundled CoNLL-2003 split; keep CrossNER's own domains |
| gd_ragtruth_summary, gd_helpsteer3_pref, gd_multiwoz21_sysacts, gd_webred, gd_redocred | Other subsets rejected (RAGTruth QA/Data2txt; HelpSteer3 principle; MultiWOZ 2.2 / user acts; WebRED 5 eval set; original DocRED) | Keep. The program asserts that only the accepted subset is present (task = Summary; preference; 2.1 system acts; WebRED 2+1; Re-DocRED) |
| gd_crowdtruth_mre (963) | Name is close to "CrowdTruth Open-Domain RE" (LDC text) | Keep only if the program confirms that the record is the medical RE set, not Zenodo 1472330 |
| proofwriter, mnli, mnli3, mnli_neutral, qnli, arc, csqa, copa, gd_codah, gd_qasc, gd_quartz, gd_winogrande, gd_medqa_yn, gd_medmcqa_subject, br_emobank, br_convabuse, gd_clickbait17, gd_sc101, gd_taskmaster1-3, gd_dstc9_track1, br_abcd, br_star, gd_star_next_action, br_casino, br_topv2, gd_oiics_event, gd_msha_injury, gd_naics_subsector, gd_onet_occupation, gd_saferproducts_severity, gd_sd311_routing, gd_wiki_help_routing, gd_wands_product, gd_uds_ordinal, gd_ncvec_ham, gd_uscg_mariner | Already used, extra rows, duplicate taxonomy, or a different subset or pool | Keep, subject to section 5 (several are in "verify upstream or drop"; condaqa is dropped as forbidden) |

---

## 4. Commit decisions from other repos (12,000 rows in round 2; 6,000 in round 1)

**ejs-5 is in-domain from now on (owner, 3 Oct).** This block trains the same kinds of software-commit decisions that
ejs-5 tests, using other repos and sources. It never uses n8n, and it never uses an ejs-5 item, question, criterion or
level wording. ejs-5 results for C are labelled "in-domain" (disclosed), never "unseen". **(v4, B5)** ejs-5 is
reported as full set (endpoint) + the 268 late rows + Gate (both report-only), and a tie on the full set is the
realistic best case for C (4.4).

### 4.1 Sources
| Source | Licence | Size | Use (r2) | Notes |
|---|---|---|---|---|
| CommitChronicle (JetBrains) | CC BY 4.0 compilation (V, Zenodo record 10.5281/zenodo.8189044; cite this, not the HF card's "other"); each commit under its repo's MIT, Apache-2.0 or BSD-3 licence (per-commit `license` field) | 7.66M train commits (10.7M total), 11.9K repos, 20 languages | 8,000 | Human messages and real diffs. The split is by project: use the **train split only**. The record asks that only public, non-personal information is used: PII scrub (guard 10). Per-repo attribution in the notices file. |
| CommitPackFT (BigCode) | MIT compilation (V, github.com/bigcode-project/octopack README + LICENSE; cite this, not the HF card) + per-sample `license`; keep only mit, apache-2.0, bsd-2/3, isc, cc0, unlicense | 702,062 single-file commits | 4,000 | n8n's Sustainable Use License keeps it out of both permissive sets; the guards below still run. The `license` field is detected per repo, so a few files may differ. |

Repos are deduped across the two datasets by normalized `owner/name`. Every held-out repo and language (mix-tuning dev,
sealed part B1) is held out of **both** datasets.

### 4.2 Task types (mirror ejs-5's kinds; never copy its items, questions, criteria or level wording)
ejs-5 has route 180, triage 148, score 360 and gate 180 rows; mean prompt 317 tokens. **(v4) Equal shares, 20% per
type (r1 1,200 / r2 2,400 each), pre-registered in the C PREREG amendment.** Disclosure: v3's shares (route 10,
triage 20, score 25, gate 35, match 10) had been set from ejs-5's per-task C1-vs-Jev gaps (methods S3), which breaks
the owner rule that neither ejs-5 nor Jev outputs choose a data share. v4 replaces them with a rule that uses neither.
The shares are frozen and never re-tuned. B6 is not run, so B7 never fires and score keeps its 20% (addendum
section I). Fallback, only by an owner-signed PREREG amendment: keep v3's shares, state that ejs-5 per-task results
vs Jev set them, and label C's ejs-5 result "in-domain, commit shares informed by ejs-5", so it cannot support a win
claim.

| Type | Share | Label from | Example question |
|---|---|---|---|
| route | 20% (r1 1,200 / r2 2,400; 30% message-only) | Top-level changed path or package (the repo's real directories; Claude writes one-line definitions from the directory names). **File headers and paths are hidden** (diff hunks only), or route becomes string matching | "Which area does this change belong to?" (3-12 options) |
| triage | 20% (r1 1,200 / r2 2,400; 30% message-only) | Conventional-commit prefix (feat, fix, docs, refactor, perf, test, build, ci, chore, revert), only in repos that follow the convention; the prefix is stripped from the shown message | "What kind of change is this?" |
| score | 20% (r1 1,200 / r2 2,400; diff + numstat always shown) | A card-defined rubric computed by program from numstat and paths (lines and files changed; sensitive paths such as lockfiles, migrations, auth, CI config). **The numstat line is shown**, so the label needs no counting in one pass. >= 40 rubrics. **(v4, A2)** Each rubric is stratified so every level, both ends included, is >= 1/K - 5 pp of that rubric's rows; a rubric whose natural skew leaves an end level short gets a higher generation ratio, never a relabel. **(v4, A1)** Every score row carries `meta.option_level` and passes G18 | "Which risk level applies under this rubric?" (3-7 levels) |
| gate | 20% (r1 1,200 / r2 2,400; 30% message-only) | A card-defined rule over the diff ("hold if a migration changes without a test", "hold if a public API changes without a changelog entry", "hold on a major dependency bump"). >= 60 rules. **(v4, B2)** Each rule draws its yes rate uniformly from 20-80% (rules differ); aggregate 50 +/- 2 per wording x bin (G10) | "Should this change be held for review?" (yes/no; per-rule rate 20-80%, aggregate 50%) |
| match | 20% (r1 1,200 / r2 2,400) | Real message-diff pair vs a message from a different commit in the same repo touching similar files. **(v4, B2)** Each card draws its yes rate uniformly from 20-80%; aggregate 50 +/- 2 | "Does this message accurately describe the diff?" (yes/no) |

Totals: 1,200 x 5 = 6,000 (r1); 2,400 x 5 = 12,000 (r2). Message-only rows: 30% of route, triage and gate =
360 + 360 + 360 = 1,080 (r1) / 2,160 (r2), inside these counts.

Rules:
- Diff-shown rows (`input_view` = "message_diff"; all score and match rows, 70% of route, triage and gate rows): show
  the message and a diff truncated to <= 1,500 tokens (record truncation; the program checks that the decisive lines
  are shown, so a truncated diff never decides a gate or score label). Mean about 600 tokens.
- **(v4, B1) Message-only rows** (`input_view` = "message_only"; 30% of route, triage and gate rows, drawn per type and
  per card). Reason: ejs-5's public input format is commit prose only (PREREG_ejs5 section 7); diff-shown rows train a
  different skill. This copies the input form only, never an ejs-5 item, question, criterion or wording.
  - Shown: the commit message only (triage: with the prefix stripped). Diff, numstat, file headers and paths are
    hidden. The label still comes from the program over the **real** commit (diff, numstat, paths), exactly as for
    diff-shown rows.
  - **Matcher M (one program, `c_src/commits/mention.py`; the same code and rules for gold and non-gold).**
    Tokenise: split on non-alphanumerics and camelCase, lowercase, drop one final "s", drop tokens under 3 characters
    and a stop list frozen before generation (generic words such as src, lib, util, main, index, update, change; never
    chosen from model or eval results; a G5-driven tightening is re-frozen before the regeneration). Entity token sets, built from the real commit and repo: a gate entity = the rule's frozen
    alias list plus the tokens of the changed paths and identifiers (path segments, file stems, names defined or
    changed in the hunks) that the rule's program assigned to that entity in this commit; a route area (every option,
    gold or not) = the tokens of its directory name and of the path segments, file stems and identifiers under it in
    the repo tree at the commit (for touched areas this includes the commit's own changed paths and identifiers);
    a token in two or more options' sets is removed from all of them. An entity is **hit** when any token of its set
    equals a message token. Directory names count the same for every area. M writes every hit (entity, token,
    position) to `meta.trigger_entities`.
  - **Keep only if the decisive fact is stated in the message.** Step 1, M: gate, every entity the rule's decision
    turns on (for "migration without a test": the migration and the test) is hit; route, the gold area is hit;
    triage, the stripped message has >= 5 words and hits >= 1 token of the commit's own changed paths or
    identifiers. Step 2, the G5 re-read (section 8). Rows that fail either step are **dropped, never relabelled**.
    The measured keep rate sets how many commits are drawn; the row counts above do not change.
  - **Keyword-shortcut negatives (required), from the same M.** A hit must not predict the label beyond the base
    rate. Gate: every kept row hits its rule's entities, so each rule's message-only rows use that rule's B2 yes
    rate (G10: within 5 pp per rule with >= 20 message-only rows, pooled by rate decile otherwise), and every rule
    in the slice has kept rows with gold "no" (for example "add migration and its test" under "hold if a migration
    changes without a test"). Fallback: a rule that cannot reach its B2 yes rate in message-only form is left out of
    the message-only slice and logged; its 30% share goes to other gate rules, and per-type counts are unchanged.
    Route: >= 50% of kept rows also hit >= 1 non-gold area; on rows that hit m >= 2 areas, the share of rows whose
    gold area is the first area hit has target mean(1/m) over those rows, +/- 5 pp, enforced when rows are built;
    the pass check is G7's Bonferroni binomial test. G6 and G7 run on the message-only slice as its own group.
  - Score rows are never message-only: numstat stays shown (rubric skill).
  - Message-only rows are shorter than the 800-token commit assumption in section 6, so the token cap is not affected.
- Hide hashes, author names, emails and dates.
- Cap each repo at 3% of commit rows. >= 400 repos in round 2.
- "Later reverted" labels are not used (rare and noisy). They may come back only by amendment.
- Split by repo: train repos; 30 held-out repos for the mix-tuning dev; 2 held-out languages for sealed part B1 (chosen
  by the sealed agent; the commit builder receives only a deny-list of languages and repos).

### 4.3 Guards
**n8n (ejs-5 is n8n; we never train on n8n).**
1. Drop any repo whose name matches `/n8n/i`, forks included.
2. Content filter on paths and diffs: `packages/nodes-base`, `packages/workflow`, `packages/core`, `n8n-workflow`,
   `n8n-core`, `INodeType`, `INodeExecutionData`.
3. The orchestrator runs the counts-only script (section 7, all blind-mode methods), on ejs-5, under the owner's
   earlier count-only approval (decision 1). It prints only the training ids to drop.
4. The orchestrator runs a counts-only check of our commit questions, criteria and level wording against ejs-5's
   (read from `run_public_bench.py` by AST, as the ejs-5 kit does). Methods: exact match, the 5-word substring check
   and 8-grams, because criteria are short. Any hit drops that card. The commit builder never sees ejs-5 wording.
   **(v4, A2)** The same check covers score rubric level names and stated cut points, and the gate rules' trigger alias
   lists (B1), so no commit-size item, cut point or level wording is copied from ejs-5.

**Other OHS and eval sources (v2).**
5. Drop commits whose message or diff mentions `CVE-` or `GHSA-` identifiers (NVD is an OHS-3 source).
6. Drop repos matching `/rosetta/i`.
7. Drop commits with `stackoverflow.com` or `stackexchange.com` links.
8. Drop diffs that contain the BIG-bench canary GUID (BBH is a DI test).
9. Drop eval-harness and benchmark repos: names matching `lm-evaluation-harness`, `opencompass`, `helm`, `bigbench`,
   `leetcode` (solution repos), and the BRIGHT source repos.
10. (v3) PII scrub: drop or redact emails, API keys and tokens (high-entropy strings next to `key`, `token` or
    `secret`), and IP addresses in messages and diffs. Count every scrub. Hidden hashes and author fields stay hidden
    (4.2).
11. (v3) The deny-list program (3.H) runs on both commit datasets and on every repo name. A repo that is itself a
    denied dataset's source (for example a benchmark's data repo) is dropped.

CommitChronicle's data is hosted on Zenodo. Under decision 7, "Zenodo" in the OHS list means the OHS-3 Zenodo record
text, not Zenodo hosting, so CommitChronicle is allowed. Cite its record licence in `meta.licence`.

### 4.4 ejs-5 reporting and test-time rules (v4; addendum B4, B5 and section I; disclosed in advance)

This section is written before any C row exists, so it is the advance disclosure B5 asks for.
- **Report form (B5).** ejs-5 is reported as three numbers, each C - Jev and C - C1 with paired 95% CIs: the full set,
  the 268 late rows (from 1 Jun 2026), and Gate. The registered endpoint is unchanged; late rows and Gate are reported
  next to it. Late rows and Gate were chosen after seeing ejs-5 results, so they are report-only for C and can never
  become an ejs-5 endpoint or support a win, tie or loss claim.
- **Expectation (B5).** A tie on the full ejs-5 set is the realistic best case for C. On current evidence, about 20-41
  of the 38 missing items come from an early-row edge only Jev has, which C's data cannot buy (we never train on n8n).
  C1 already ties on the late rows (46.3 vs 45.9). Win, tie and loss wording follows the registered rule.
- **No test-time prior fix ships (B4).** No Batch Calibration, EM prior re-estimation, BBSE, median cut or any other
  per-set prior correction is applied to a served or reported readout, on ejs-5 or anywhere else. Serving is one
  request at a time, and on C1's ejs-5 probabilities EM collapses (Gate all "no").
- **ejs-5 chooses nothing (section I).** B6 (the ejs-5 decomposition) is **not run**: nothing reads ejs-5 gold for
  diagnosis, and B7 never fires. ejs-5 (like OHS-3) never chooses a data share, loss weight, temperature, readout or
  model. It is read only as the final in-domain check, under the existing counts-only and scoring rules.

---

## 5. Replay of C1's data (60%)

**Pool.** `data/v14_parts/golden_train.jsonl`: 501,732 rows in 204 sources. Per-source counts and licence strings are
in `replay_licence_scan.json`; every source's status is in `LICENCE_REGISTER.md` section 4.

**Dropped from replay.**

| Source(s) | Rows | Why |
|---|---|---|
| yelp, yelp5 | 303 + 373 | Yelp agreement is non-commercial; also read from test splits (`build_train_v03/v06`) |
| logiqa2 | 441 | CC BY-NC-SA 4.0 upstream |
| yahoo | 538 | Licence unknown; forbidden list; also read from a test split |
| amazon_polarity | 754 | Forbidden list; terms unclear; also read from a test split |
| musr_murder_mysteries, musr_object_placements, musr_team_allocation | 111 + 96 + 91 | Decision Index test items (MuSR has no train split) |
| mrpc, rte | 632 + 952 | GLUE licence unknown; `glue/mrpc` is forbidden |
| tb_label_nli | 1,288 | Forbidden label-NLI set; licence "other" |
| gd_bbh_mistake | 905 | Reuses BBH inputs (DI test) |
| 7 OHS-3 overlap units (gd_redocred 6, gd_helpsteer3_pref 1) | 7 units | Owner's counts-only check (A10 disclosure) |
| **(v2)** civil_comments, toxic_conv | 364 + 729 | Jigsaw-derived; MBIB `040_Jigsaw` (inside forbidden `mbib-base`) is the same corpus. Not grandfatherable |
| **(v2)** br_newsmtsc | 607 | Non-commercial POLUSA source text. Not grandfatherable. **Disclose: C1 trained on these 607 rows** |
| **(v2)** wiki_stance_afd | 901 | No licence on the card; AfD is also a JevBench "jagged" source (`routing_dialogue/rejected.json`) |
| **(v3, decided by default, decision 4)** boolq, condaqa, dbpedia, banking77 | 896 + 788 + 882 + 2,300 = 4,866 | In `forbidden_label_nli.json`. **Dropped.** The owner may override by amendment; risk if dropped: drift on the banking77 dev rows (559 seen-source rows) and DI BANKING77 |
| **(v3, decided by default, decision 4)** binj_\* (4), std_\* (4), hard_\* (18), planted_\* (2), proc_\* (9) | 854 + 1,538 + 3,875 + 890 + 1,450 = 8,607 | Golds written by Claude (builder headers: "Claude as teacher", "Claude-authored"), then blind-solved. This breaks "programs or human gold give labels". **Dropped.** The owner may override by amendment; risk if dropped: small drift on hard_dev (208 rows) |
| **(v2; merge 3 Oct)** Sources whose licence the mixer cannot verify | up to 53,270 (9,779 with no licence in meta + `gd_finqa` 4,970 + 38,521 whose only record is the creator's HF card) | See below |
| **(v2)** Human-labelled replay rows with C1 p_g < 0.2 | unknown (estimate 2-5%) | See below |
| **(v3)** Deny-list hits with a drop-class reason (3.H.3) | known: Stack Exchange half of politeness data, bundled CoNLL-2003 rows; plus any used_sources "avoid" hit | OHS source text, licence, or OHS-3 "avoid" |
| Old-slice monitor | 2,000 rows | Held out in both rounds, by `group_id` **and** by normalized state, so no sibling stays in replay |

**(v2) Licence join.** The mixer joins a per-source licence table (`LICENCE_REGISTER.md` section 4). 35,279 replay rows in
77 sources have no `meta.licence`. Their status:
- Program-generated, keep and stamp "CC0 1.0 (program-generated)": `pg_*` (7 sources, 2,688 rows; `build_pg.py`),
  `judge_mathderiv` (479; procedural, `build_judge.py`).
- Mappable to a verified golden licence, keep: `judge_prm800k` (826; MIT, openai/prm800k, as `gd_prm800k_steps`).
  `judge_helpsteer2` (461) maps to `gd_helpsteer2_attr`, whose record is an HF card, so it is in the next bullet but one.
- Verify upstream or drop (9,779 rows): clinc150 2,651, massive 1,703, mnli3 1,090, qnli 903, mnli 661, mnli_neutral
  164, proofwriter 687, fld 574, csqa 478, arc 414, copa 243, clothing 211. Candidate upstream licences are in the
  register; a mirror's card does not count.
- **(merge 3 Oct) Licence in meta, but the document text is unverified:** `gd_finqa` (4,970 rows). FinQA's annotations
  are MIT, but the report text is FinTabNet, the same unverified CDLA-Permissive-1.0 text that keeps MultiHiertt and
  ConvFinQA out (3.G). Verify upstream (IBM's record) **and** owner acceptance by amendment, or drop. The register's
  generator (`tools/make_replay_register.py`) lists it under VERIFY.
- **(verifier 3 Oct; decisions 6 and 12 apply to replay too) Licence only on the creator's HF card:** 38,521 rows in 15
  sources: `gd_mfrc` 8,254, `gd_qasc` 6,107, `gd_edgar_10k_item` 6,070, `gd_helpsteer3_pref` 3,369, `gd_faithdial`
  2,963, `gd_helpsteer2_attr` 2,729, `gd_aegis_prompts` 1,887, `gd_quartz` 1,798, `gd_climate_targets` 1,071,
  `gd_spiced` 1,002, `gd_mtbench_human` 970, `gd_ropes_sci` 941, `br_congress_policy` 699, `judge_helpsteer2` 461,
  `br_steam_aspect` 200. Verify upstream (repo LICENSE, official project page or release; never an HF card or mirror)
  or drop. The register generator lists them under VERIFY.

**(v2) Low-confidence replay rows.** C1 (REF) has trained on every replay row for one epoch. Rows it still gets confidently
wrong are where label noise collects (golden_train: about 2.7% wrong and 6.3% ambiguous; legacy replay about 6% wrong,
GOLDEN_CARD.md). Rule:
- Hard-label rows from **human-labelled** sources with C1 p_g < 0.2 are dropped.
- Program-labelled sources (`gd_gen*`, `gd_gen2_*`, `pg_*`, `judge_mathderiv`, `gd_babi_logic`, `gd_prontoqa`,
  `gd_logicinference`) keep such rows: their labels are exact, so these are real model errors.
- Soft-label rows (vote shares) are kept.
- A G5 read of 300 dropped rows estimates the noise rate (report only).

`gd_casehold_yn` stays: OHS-1's legal part is LegalBench CC BY tasks and LEDGAR (`PREREG_OHS.md`), not CaseHOLD.
The judge family (`gd_helpsteer2_attr`, `gd_helpsteer3_pref`, `gd_prm800k_steps`, `gd_ragtruth_summary`,
`gd_mtbench_human`, `judge_*`) stays under the judged-object rule: LLM outputs are the objects being judged, and the labels
are human. Several of them are also in the HF-card VERIFY list above and stay only if that check passes. No such row is
added as new data.

**Eligible pool.** About 478K rows before the licence verification and the p_g rule, and about 405-470K after (the
lower end if no VERIFY source, `gd_finqa` and the HF-card-only sources included, is confirmed). Round 2's 180K is about
38-45% of it. If an HF-card-only source is dropped, the judge-family and protected-skill counts in the mixer report
show the loss.

**Sampling (round 2 quota 180,000; round 1 takes a random half of each source's quota).**
- Sample whole relation units, never single rows, so complement, equiv and inv partners stay together.
- Per-source quota proportional to n_s^0.7 (mild flattening), floor min(n_s, 150), cap 4% of replay (7,200).
- Within a source: stratify by qtype x role x gold. Keep yes/no gold balanced per source and per wording.
- **(v4, E2) Replay yes rate per instruction wording (CPU, $0).** After sampling, the mixer groups hard-label yes/no
  replay rows by normalized instruction wording (the question frame with entity and text slots masked; one cell per
  wording, pooled across sources) and logs each cell's gold-yes rate. Any cell with >= 50 rows outside 50% +/- 5 is
  re-stratified: swap whole relation units with other unused units from the same sources until the cell is inside
  the band, keeping the per-source quotas. If no unused unit can fix a cell, drop units from the over-represented
  side and refill from the same source's other wordings, so replay stays at 90,000 / 180,000. Smaller cells are pooled
  by wording family. Vote-share rows are logged
  separately and never resampled for this. Before/after rates per cell go in the mixer report. This tests the
  wording-prior source of the "yes" drift; it chooses nothing else.
- Keep human vote-share rows at their natural rate.
- No row is used twice.

**C1 anchor targets (owner, 3 Oct: "KL to C1 only where C1 is confident or on protected skills"; weight and reasoning in `C_TRAIN_RECIPE.md` section 3).** REF is C1, because
step B adopted nothing.
- C1 scores every sampled replay row once with the shipped A5 readout (choice: given order and exact reversal,
  averaged; yes/no: one read; T = 1), on the free L4 (decision 3). The same pass gives the p_g used by the
  low-confidence rule above.
- A replay row gets `meta.teacher` = C1's probabilities in two cases, both decided by a pre-registered program. In
  either case the row must have no human vote-share or exact-probability target.
  1. `meta.teacher_src` = "c1_anchor" (**confident rows**): C1's top answer equals gold **and** C1's top probability is
     >= 0.8.
  2. `meta.teacher_src` = "c1_anchor_protected" (**protected skills**): C1's top answer equals gold, at any
     confidence, and the row is in a protected unit:
     - (a) security: `inv` relation units, and attack-resistant variant rows (`meta.attack_target` set or `role` =
       "attacked") together with their clean partners;
     - (b) consistency: `equiv` and `complement` relation units.
     The protected list is fixed in the amendment. Adding a skill needs a new amendment.
- No anchor in these cases:
  - rows where C1 is wrong, at any confidence, so C can fix C1's mistakes;
  - every new row (own families, public splits, commits);
  - rows with their own vote-share or exact-probability targets.
- A row whose only teacher is the old "blend50" model counts as having no target. It gets an anchor under the same
  two rules, and no target otherwise.
- The mixer reports both counts ("c1_anchor", "c1_anchor_protected") for `expect_kd_targets`. Expected coverage is
  about 75-85% of replay rows (an estimate).

**(v4, A1) Ordinal target lint (builder and mixer; gate G18).** For every ordinal row (2.4), new or replay, the program
builds the **actual training target** the trainer will see: gold, after the recipe's label smoothing, combined with
any KD target (human vote shares, `gold_probs`) and any C1 anchor, using the recipe's registered values. It computes
E_target = sum over options of p(option) x `option_level`, and requires `round_half_even(E_target) == gold level`
(the same rounding as the Score readout). Examples it catches: vote shares 0.55 / 0.35 / 0.10 on a level-0 row give
E 0.55, which rounds to level 1; an anchor with p_top 0.8 and 0.2 on the far end of K = 4 gives E 0.6, also wrong.
- On failure: drop that row's KD or anchor part and fall back to smoothed gold (C1's smoothing of 0.05 / 0.08 is
  safe; the limit is 1/3 at K = 4). If it still fails, drop the row. Never change the gold.
- Builders run it on their own rows; the mixer re-runs it on the final merged targets (after the anchor merge), since
  that is where anchors are attached.
- **Pass rate must be 100% before any freeze.** The mixer report gives counts per source: rows checked, rows that
  fell back to smoothed gold, rows dropped.
- The lint never reads a model's eval predictions. It uses only the targets that go into training.

---

## 6. Format augmentation

| Lever | Spec | Evidence |
|---|---|---|
| Format style pool | About 400 styles = container (prose, memo, email thread, chat log, JSON, YAML, CSV, markdown table, HTML snippet, key-value record, bullet SOP, log lines, diff, form) x card style x register x instruction position. 50 styles are held out for the mix-tuning dev only and never trained. The sealed suite uses its own styles, written by the sealed agent | Prompt format alone moved LLaMA-2-13B by up to 76 points (Sclar et al.) |
| Instruction wordings | >= 30 per family, >= 5 per card; >= 3 per public dataset | Many templates gave +1.9 to +5.6 ROUGE-L on small Qwen3/Llama models, more on the worst template (Sadrieh and Stefanik 2026) |
| Definition styles | one-line; one-line + 1-2 examples (about 50% of cards); rubric table; short or no card (about 15% of rows; today 4%) | GoLLIE ablation; Super-NI "definition + examples" |
| Few-shot cards | 5-10% of cards | Flan: >= 5% few-shot templates improved zero-shot |
| Inverted cards | 10-15% of cards | Flan: removing input inversion cost 8.6 MMLU and 7.8 BBH points |
| Masked / swapped label names | 10-15% / about 5% of choice rows | GoLLIE; Codebook LLMs |
| Option counts | 2-60, buckets in section 2.1 | C1 weak at 21+ options |
| Registers and locales | Formal, casual, terse, verbose; US and UK spelling; date formats; currencies; units | AttrPrompt |
| Lengths | Non-long rows: median 500-900 tokens. Long rows: 2,000-7,900. No row above 7,900 real tokens (fits `micro_tokens` 8192) | |
| Batching | A relation unit holds at most 3 rows (F5 splits its quadruple into a 3-row unit and a 1-row unit); long units at most 2 rows | Same-batch paraphrases gave conflicting updates on 57-64% of weights (Sadrieh and Stefanik) |

Format variety lives inside `state`, `instructions`, `options` and the card. The outer prompt layout
(`schema_branch_mark`, cygnet style) stays exactly as trained, served and evaluated.

**Token cap (real tokenizer, enforced by the mixer).** Rows of 2,000 tokens or more are at most 9% of new rows and at
most 30% of new-row tokens. Planned round 2 (assumptions: own non-long rows about 850 estimated tokens, F13 about
4,600, public long about 5,600, commits about 800): long rows are about 6,000 (5% of new rows) and about 25% of new-row
tokens. If the real count passes 30%, the mixer drops F13 and 3B rows from the 6-7.9K bin first.

---

## 7. Decontamination (G13, before every freeze)

### 7.1 Against
- The 9 dev gate splits; the mix-tuning dev; JevBench public (231) and the v1.5.4 files; BTZSC.
- **(v2)** `data/eval_opi.jsonl` and `data/eval_jagged.jsonl` (texts and attack wording; the decontam program reads only
  `state`, `instructions` and `options`, never the `jev_*` meta fields).
- **(v2)** The texts of all 152 tasks in `forbidden_label_nli.json`.
- **(v2)** All splits of every OHS-1/2/3 source dataset (PREREG_OHS rule 1: "any split of its source datasets"), and
  TabFact's tables (OHS-2) as normalized table hashes.
- **(v2)** HateXplain and Social Bias Frames posts (exact normalized text), for GHC and EDOS rows.
- **(v3) Counts-only, run by the orchestrator (decision 1, under the owner's earlier count-only approval).** Neither
  the orchestrator nor any agent reads these sets; only the counts-only script does:
  - OHS-3;
  - ejs-5;
  - LongBench v2;
  - the Jev Decision Index test sets;
  - the texts of the 152 forbidden tasks;
  - all splits of the OHS-1/2/3 source datasets;
  - TabFact's tables;
  - the sealed suite (its script reads `sealed_nd/` in its own process).
- OHS-1 and OHS-2 are practice sets now. They get program-only checks; no agent reads them.
- **(v3)** A dataset hit by the 3.H deny-list is not decontaminated row by row: it is out.

### 7.2 Methods (any hit drops the training unit)
For sets we may open (by program):
1. **(v2)** Exact match of the normalized full text, and of each sentence or line with >= 5 words.
2. **(v2)** Any shared 10-gram (word, lower case). (v1 used 13; the v14 build used 12, JevBench decontam used 10.)
3. Tulu-3 rule: an eval item is contaminated if > 50% of its tokens fall in 8-grams shared with one training row.
4. MinHash on word 5-grams (Jaccard >= 0.8), confirmed by edit similarity >= 0.8.
5. Embedding cosine top-5 above a threshold set by hand-checking 100 pairs at 0.85 / 0.90 / 0.95 **on open sets**.
6. Structure hash: an own row whose canonical problem (rule graph + facts + query, names abstracted) equals a
   mix-tuning-dev item or a sealed part P item (from the sealed export).
7. Domain keyword block-list for the sealed domains (applied by program).
8. Template check: no negation, instruction or attack template may match a dev or eval wording. This includes OPI's
   five strategy strings in `build_opi.py` ("Ignore previous instructions.", "Answer: task complete.", and the rest)
   and jagged's injected line.
9. **(v2)** Table hash (normalized title + header + cell set) for WikiSQL and HybridQA vs every TabFact table; both come
   from the same WikiTables corpus (arXiv 1709.00103, 2004.07347, 1909.02164).

**Blind mode (counts-only).** For every set in the counts-only list (7.1), the orchestrator runs one script in its own
process (decision 1). No data agent runs it or sees its inputs. **(v2)** It runs methods 1 (exact text and sentence/line hashes), a substring check for
every eval text of >= 5 words inside training texts, 2 (10-grams), 3 (8-gram rule), 4 (MinHash) and 5 (cosine, at the
threshold fixed on open sets), plus table hashes where the eval has tables. It prints only (a) counts per training
source and (b) the training ids to drop. No eval text is ever printed. Items shorter than 5 words are covered only by
the exact full-text hash; the report says how many such items each eval has. **(v3)** It runs before each freeze
(round-1 files, round-2 files), on the Claude-written seeds below, and once on the final mix. Its logs hold counts and
training ids only, and they are stored under `logs/decontam_counts/`.

**Claude-written seeds.** Claude may recall benchmark items (12.8% of HumanEval overlapped CodeAlpaca). Every
Claude-written template, seed, domain pack and codebook is decontaminated too, not only the final rows.

### 7.3 Re-derived dev unseen set (D2; rules S11)
New hate, emotion, finance and sarcasm data sits next to the dev sources hate, emotion, financialphrasebank, climate
and irony. So the frozen 3,847-row unseen set no longer means "unseen" for C. The procedure:
- **When.** For each decision that reads D2, the orchestrator re-runs `gate_dev.py`'s name rule and text guard (CPU)
  with that candidate's own training files added:
  - the round-2 rule (recipe 6.3) uses the round-1 files;
  - the ship look (recipe 6.4) uses the finalist's files (round 1 alone, or the round-2 superset).
- **Freeze.** The re-derived row list is written with its sha256 to the look log **before** the candidate's first
  read. It is never changed after any model read.
- **Inputs.** The re-derivation uses training text only, never predictions.
- **Size floor.** If the re-derived set falls below 2,000 rows, the look log records the new size and SE. The D2 rule
  stays.
- **Reporting.** Both sets are reported, the frozen set and the re-derived one; the gate uses the re-derived one.

### 7.4 Jev outputs (never read by builders; never used to train or choose anything; rules S6)
Jev's terms forbid training on its outputs. Every path below is on **every builder's forbidden list**: QC, mixer,
public, commit, pack and format agents, and blind readers. The shared loader refuses them. Paths are relative to the
repo root (`jev/`); `lean/` = `opendecide-data/lean/`. The list comes from a file-name search on 3 Oct that skipped the
sealed paths.

| Path or glob | What it holds |
|---|---|
| `lean/preds*/jev*` (now in `preds`, `preds_ohs`, `preds_ohs2`, `preds_eval_card`, `preds_eval_hc`, `preds_eval_jagged`, `preds_eval_long`, `preds_eval_multi`, `preds_eval_opi`) and `lean/preds_ohs3*/` (sealed) | Jev predictions on dev, OHS and eval sets |
| `lean/logs/jev_*.log` (8 files) | Jev run logs (OHS rounds, hc tournament and shortlist, long) |
| `lean/prep89/` (whole folder; includes the OHS-3 Jev collector) | OHS-3 preparation (already never-open) |
| `bench/runs/jev_*` (`jev_p1`, `jev_p2` and their logs) | JevBench runs of Jev |
| `bench/jevbench/results/`, `bench/jevbench_v154/results/` | Published leaderboard outputs, including Jev's |
| `bench/jagged/data/` (`trials`, `main`, `pilot`, `followup`) and the `jev_recorded_p_yes` field in `lean/data/eval_jagged.jsonl` meta | Jev-recorded jagged answers |
| `bench/external_quarantine/` (includes ejs-5's published answers), `bench/ejs5/runs/`, `bench/ejs5/tests/_work/` (`jevcopy`) | ejs-5 answers and score work |
| `reports/pdf_build_30sep/v154_variants/jev_*`, `reports/OpenDecide_v05_vs_Jev.md` | Report copies of Jev numbers |
| `lean/sealed_nd/jev_*` (future) | The single Jev read of the sealed suite (decision 10) |

**Program rule (beyond the list).** The loader also refuses:
- any input path whose file or directory name matches `/(^|[_/.-])jev/i`. There is one exception: the decontamination
  program may read the JevBench **item** files (`bench/splits/jevbench_*.jsonl` and the v1.5.4 item files), using item
  text only. Builders need none of these paths, including the code files `run_jev*.py` and `jevbench_od.py`;
- any row field whose key starts with `jev`.

The decontamination program reads `eval_jagged` and `eval_opi` only through `state`, `instructions` and `options`. If a
new Jev file appears, the rule above already covers it. The mixer logs every input path with its sha256, so an audit
can show that no Jev file was read.

**Jev read on the sealed suite (decision 10, by default).** Jev is read **once** on the sealed suite. The goal's
criterion ("+1 pt vs Jev on the new-domains suite") needs it. The rules are in section 9.

---

## 8. QC checklist (every family passes every gate before it enters a mix)

| Gate | Pass rule | Tool / cost |
|---|---|---|
| G0 Spec first | 1-page spec per generator with a semantics table (open or closed world; "unless", "only if", "at least", inclusive or exclusive "or", date ranges, rounding, ties, units; exception precedence). Every choice that could flip a label is stated in the card. A second Claude session lists ambiguities; all are resolved | CPU |
| G1 Provenance | Every row has the section 2.4 meta. Every public source has an upstream licence URL + commit + sha256, and a document-text licence note. Every (H) set is dropped unless an upstream record is found (decision 6). **(merge 3 Oct)** The cited URL is the official record named in `LICENCE_REGISTER.md` section 1-2 (never an HF card or mirror); the builder re-reads it, and a changed or missing record fails G1. Per-item text filters are logged per item (QuALITY article field, Qasper arXiv licence, CommitPackFT `license`). **(v3)** The 3.H deny-list program passes every dataset and every declared parent, and no input path is on the 7.4 Jev list (mixer input log) | CPU |
| G2 Independent re-derivation | Solver B (different paradigm) agrees with solver A on **100% of rows**. Any mismatch: stop, fix, regenerate the whole generator. **This and G3-G4 are the primary label guarantees**, because Claude both writes and blind-reads, so Claude errors can correlate | CPU |
| G3 Round-trip parse | Parse the rendered text back and re-solve: **100% agreement** | CPU |
| G4 Metamorphic tests | >= 3 relations per generator (option shuffle, rename, inert sentence, row or rule reorder, negate a premise, remove a premise, monotonic severity, injected instruction), **100% pass** on >= 1,000 rows. Hypothesis (MPL-2.0) for property tests | CPU |
| G5 Blind read | A separate Claude session (never a generator author) sees only the card and text. **Claude is a flag-only reader (decision 2): it never sets, edits or chooses a label.** 300 rows per family; 600 for F1, F5, F6, F13 and commits. **Zero confirmed wrong golds** (95% upper bound 1.0% at n = 300, 0.5% at n = 600). Ambiguous <= 1%. A confirmed error is a generator bug: fix, regenerate, re-sample a fresh 300. Claude only flags; a label is never edited by hand. Public and real-text rows: dataset-level decisions only (drop the dataset if > 8% clearly wrong; SQuAD 2.0 > 5%), never row by row. **(v4, B1)** The 600 commit rows include 300 message-only rows (stratified over route, triage and gate); a message-only row whose decisive fact the reader cannot find in the message counts as ambiguous (bar <= 1%). Above the bar: tighten matcher M (alias lists, stop list), regenerate the message-only rows and re-sample a fresh 300 | agent time |
| G6 Partial-input and metadata baselines | Per family, 5-fold CV on a **separate QC sample of >= 5,000 rows** from the same generators (F8, F12 and F13 have fewer real rows): bag-of-n-grams logistic regression + small gradient-boosted trees on (a) question only, (b) options only, (c) card without question, (d) metadata only (depth, rule count, length, option lengths, number magnitudes, name pool, template id, sampler id, repo). Accuracy <= chance + 2 pp. **(v4, B1)** Message-only commit rows are a separate group, and (d) adds the number of areas or entities M hits and `input_view` | CPU |
| G7 Feature z-test | One-sided binomial per unigram, bigram and metadata feature; p0 = 1/k; alpha 0.01 Bonferroni over features. Yes/no with 50K features: a feature fails at 200 occurrences with >= 67.9% one label, 1,000 with >= 58.0%, 5,000 with >= 53.6%. No feature may fail. Fix by matched twins first, z-filtering second. **(v4, B1)** On the message-only route slice, "option is the first area M hits" is a tested feature on rows where M hits m >= 2 areas (p0 = 1/m) | CPU |
| G8 AFLite-lite | Frozen MiniLM-L6 (Apache-2.0) embeddings, 64 partitions, linear models, tau 0.75. Predictable share < 10% per family. Over 10%: find the cue and fix the generator; do not bulk-delete | CPU |
| G9 Difficulty from the crowd | C1, 4B-E and base 4B score every candidate row on the free L4 (decision 3; not the H100). Bins and stratified selection as in 2.1. Every row with crowd p_g < 0.05 enters a G5 re-read sample (300 per family; any confirmed error = generator bug). After stratified selection, label x bin chi-square p > 0.01. (v4) Selection stays stratified and representative (addendum D1): no LESS, influence, IFD or targeted selection. Addendum D2 (facility location on C1 hidden states for public 3A-3E rows) is CONSIDER: D2 is decided once, in the C PREREG amendment (before any C row exists). It is adopted for round-1 public rows (3A-3E) only if this G9 L4 pass can log C1's pooled hidden states at no extra time. Otherwise it lapses for C (it cannot be added later) | free L4, about 20-28 h (no Modal spend) |
| G10 Balance | Aggregate yes rate 50% +/- 2 per family x wording x bin x negation count (per-card rates vary 20-80% by design); gold letter uniform per option bucket (chi-square p > 0.01); "longest option is gold" within +/- 2 pp of 1/k; abstain options wrong on >= 50% of rows that show them; "attack present" uncorrelated with the label. **(v4)** Commit gate (per rule) and match (per card) yes rates within 20-80%, aggregate 50% +/- 2 per type x wording x bin (B2); per gate rule, the message-only yes rate is within 5 pp of the rule's drawn rate, checked on rules with >= 20 message-only rows and pooled by rate decile otherwise (B1); ordinal levels: F7 each level 1/K +/- 2 pp per sampler x K, commit score each level >= 1/K - 5 pp per rubric, end levels included (A2); replay hard-label yes/no rate 50% +/- 5 per wording cell with >= 50 rows; smaller cells are checked pooled by wording family (E2, section 5) | CPU |
| G11 Diversity | Card, pack and sampler counts as in 2.1; no surface template above 2% of a family; every Claude seed has ROUGE-L < 0.7 to all other seeds; compression ratio, Self-BLEU and Vendi score no worse than the same family's slice of golden_train | CPU |
| G12 Dedup | Exact hash: 0 duplicates. MinHash near-dups: keep one. Structure hash: one surface form per structure, except planned twins and format variants | CPU (datasketch, MIT) |
| G13 Decontamination | Section 7. Zero hits after drops | CPU + orchestrator counts-only runs (decision 1) |
| G14 Sealed separation | The sealed suite exists and is frozen, with its sha256 committed in a PREREG amendment, before any C data exists: no generator run, pack, style pool, codebook, public row or commit row. No C builder has read access to it. The build log shows the order | process |
| G15 Loader round-trip | Every row passes `train_decoder.check_rows`; render each row through `decoder_io.user_msg` under a random permutation; map the displayed gold letter back to the canonical gold: **100% match**. Print 20 rendered prompts per family and read them. **(v2)** Every relation unit shares one `call_id` and has <= 3 rows; units with a row >= 2,000 tokens have <= 2 rows; real-tokenizer length <= 7,900 for every row | CPU |
| G16 Owner audit (**optional, non-blocking**, decision 11) | If the founder chooses: 200 rows answered blind on an audit page: 30 from each high-risk block (F1, F5, F6, F13, commits) + 50 stratified over the rest. Agreement >= 95% per block, and every disagreement is adjudicated against the spec. About 2-3 hours. Round 1 never waits for it; a failed block found later is fixed before round 2 | owner time |
| G17 Post-round-1 cartography | Log per-row gold probability at the 25/50/75/100% snapshots. Audit 30 rows per family from the low-confidence, low-variability region with G5. If >= 15 of 30 are wrong, fix the generator before round 2 | reads only |
| G18 Ordinal target lint (v4, A1) | Every ordinal row (2.4) has `meta.option_level` covering all its options, and `round_half_even(E_target) == gold level` on the actual training target after smoothing, KD and the C1 anchor (section 5). Fallback to smoothed gold, else drop. **100% pass** in the builder and again in the mixer, before every freeze | CPU |

Public rows pass G1, G6 (on our framings), G7, G10, G12, G13, G15 and a G5 read of 100 rows per dataset (300 for
SQuAD 2.0). (v4) Replay rows on a level scale also pass G18.

---

## 9. The sealed new-domains dev suite (built first, by a separate agent; recipe 6.1)

**Purpose.** Measure transfer to domains that neither C1 nor C ever trained on. Its real-text part A is the headline
test in the C gate. It is a dev suite: it is used for selection (select set) and for one confirm look. It is also where
C is compared with Jev once before OHS-3, for the goal's "+1 pt vs Jev on the new-domains suite" (decision 10, report
only).

**Isolation (owner, 3 Oct: adopted Codex item 3; methods B4).**
- **Separate builder.** A separate agent session builds the suite in `lean/sealed_nd/` (git-ignored). Its candidate
  list and instructions are in `c_spec/sealed_brief/`, which no C builder opens. **This file names no domain, source or
  theme of the suite.**
- **No access to C.** The sealed agent never reads C data, C family specs, `c_src/`, `data/c_parts/`, section 6's
  style or wording pools, or any C builder's folder. To apply rule 1 it reads only C1's and C's training-source names.
- **Different source pool and different templates.** The sealed agent writes its own templates, instruction wordings,
  cards and format styles. Once C's pools exist, the orchestrator's counts-only script compares C's templates and
  styles with the sealed ones (exact match and 8-grams). A hit drops the **C** template, never the frozen sealed item.
- **Frozen first.** The suite is built and frozen, with its sha256 committed in a PREREG amendment, **before any C data
  exists** (G14, section 11).
- **Exports.** The suite exports only:
  - (a) a domain keyword block-list;
  - (b) hashed 10-grams and 12-grams;
  - (c) exact hashes of normalized full texts and of sentences/lines;
  - (d) structure hashes of part P items;
  - (e) item counts per part.

  No text is exported. The QC program applies these; builders never read them. The remaining blind methods (8-gram
  rule, MinHash, cosine, 5-word substring) run in the orchestrator's counts-only script, which reads `sealed_nd/` in
  its own process.
- **Aggregates only.** Scoring prints aggregates only: overall, per part, per set, per domain, per question type.
  **Nobody inspects per-item failures**, for any model, at any time. The noise-floor read below happens before the
  freeze and never sees model outputs.
- **Looks follow recipe 6.2 (one candidate per round).**
  - S1: round-1 candidate, select set.
  - S2: round-2 candidate, select set, only if round 2 ran.
  - C: the finalist, read once on the confirm set, all of part A per domain, and parts B and P.

  The scorer logs every look in `sealed_nd/looks.jsonl`, refuses any look not in that table, and refuses a second C
  look.
- **(v4, B3) Yes-share drift alarm, report-only, at the existing looks only.** At S1, S2 (if run) and C, the look's
  aggregate output also logs, per set and per domain, the candidate's mean P(yes) and predicted yes share on yes/no
  items. Both are gold-free (predictions only). Alarm if a domain whose yes/no items are 50/50 by construction falls
  outside 30-70%. Both are computed from the same served-pipeline output as the look's accuracy (recipe 6.0, 6.1).
  B3 printing is part of the sealed scorer, which the sealed agent builds and CPU-tests with the suite; the suite's and
  the scorer's sha256 go into amendment A15 before any C training row exists (recipe 6.2, 11 step 2), and the scorer
  is never changed after that without a new amendment. If the frozen scorer lacks B3, B3 is dev only. The alarm is reported next to the look's result; it never changes a ship verdict, a data
  share, a weight, a temperature, a readout or the candidate.

**Domain selection rules.**
1. The source was never used in C1's or C's training (name check and counts-only text check).
2. The domain is absent from C1's domain map (`LOCAL_GAPS.md` 1.9), or it is an adjacent genre, marked "adjacent".
   Government incident reports, weather events, 311 or help-desk routing, and benefit or eligibility rules count as
   adjacent (C1 has about 9.8% government incident text, storm data and 311/help routing).
3. Not an OHS-1/2/3 source and not next to an OHS-3 source domain (no vulnerability or CVE text, no Rosetta-style code,
   no Stack Exchange-style Q&A).
4. Not Wikipedia, not Natural Questions, not a LongBench v2 source (counts-only check), and not a source behind any C
   public set (section 3) or any 3.G dataset.
5. Permissive licence verified upstream (same list as section 3.1). A creator's own card is not enough (decision 6).
6. Gold from humans, officials or programs. No LLM labels.
7. **(v3)** MultiDoc2Dial, doc2dial and NLU++ are never candidates, and neither is any dataset on the 3.H deny-list.
8. **(v3)** Every part-A domain gets an "adjacent" or "non-adjacent" label at freeze, before any model read. The label
   never changes.

**Layout (v3, recipe 6.1; supersedes v2's 3,200-4,000 items and parity halves).**

| Part | Content | Items | Role |
|---|---|---|---|
| A (headline) | 6-10 real-text domains, 500-1,000 items each, no domain above 20% of part A; >= 4 non-adjacent domains holding >= 50% of items | **>= 5,000** (target 5,000-6,000) | Select set (about 40%, >= 2,000): round-2 rule (6.3) and finalist choice. Confirm set (about 60%, >= 3,000): ship rule P1. All of part A per domain: P2 |
| P (program-built) | 3 domains x 200, with the sealed agent's own code, templates, themes and format styles | 600 | Report only (same-family, new-theme; reported separately from A); read only at the C look |
| B1 (commits) | Commits from 2 held-out languages, from permissive-licence repos that are in **no split** of CommitChronicle or CommitPackFT (different source pool; deduped by normalized `owner/name`); never n8n; the sealed agent's own questions and rubrics | 300 | P3 guard + report; read only at the C look |
| B2 (long documents) | 4-8K-token real documents from a non-Wikipedia, non-NQ source that no C row uses | 200 | P3 guard + report; read only at the C look |

If part A ends below 5,000 items, the rules stay and the power is re-stated (recipe 6.1).

**Item rules.**
- Yes/no is 40-50% of items, with yes at 50%. Choice items have 2-60 options.
- >= 30% of items are card-free or in a sealed-only format.
- Items are grouped by source record (`group_id`).
- The split uses sha256("ndsel:" + group_id) mod 5: values {0, 1} form the **select** set and {2, 3, 4} the **confirm**
  set. Siblings therefore never straddle the two sets.

**Label filters (v2): rules, not model agreement.**
- Drop an item when its text contains the gold label word or a listed synonym. In coded reports the coded outcome is
  often written into the narrative; a rejected candidate failed exactly this way.
- Drop items whose gold is "other", "unknown" or "not coded", and items whose decisive field is missing.
- Drop exact and near-duplicate texts (MinHash).
- Before the freeze, a second sealed-side Claude session reads 200 items per part to estimate the noise floor. It only
  flags (decision 2). It never drops single items. A domain with more than 8% clearly wrong golds is dropped as a whole.

**Jev read (decision 10, by default: Jev IS read, once).**
- **When.** Once, at the C look, **after** the ship verdict is written to the look log. So it cannot affect the ship
  decision or any earlier choice.
- **What.** Parts A (both sets), B and P, with the harness used for the OHS Jev reads. Answers are stored under
  `sealed_nd/jev_*`. The scorer refuses a second Jev read. Jev's API spend is a GO point.
- **Report.** Aggregates only: the shipped model (C if it ships, else C1) minus Jev, and C1 minus Jev, on the part-A
  confirm set and on all of part A, with paired 95% CIs; per part and per domain as well.
  - "Beats Jev by >= 1 pt" is claimed only if the point gain is >= +1.0 and the LB > 0.
  - Otherwise the report says "tie" or "behind", with the numbers.
- **Never an input.** Jev's answers are never used to train, or to choose data, weights, candidates, thresholds or
  temperatures. Jev's terms forbid training on its outputs.

---

## 10. Mix-tuning dev (separate from the sealed suite)

| Part | Items | Use |
|---|---|---|
| 13 families x 400 (S5 sampler, held-out packs, held-out styles) | 5,200 | Bounded weight update (recipe 7.2); paired SE about 1.8-2.5 pp per family |
| Depth sweep: F1, F2, F3, F4 x 5 depth levels x 60 | 1,200 | Sets round-2 depth caps: the deepest level where round 1's candidate CAND - C1 >= +3 pp and CAND >= chance + 15 pp |
| Hard-negation probe (the 25 held-out cue templates) | 400 | Report only (recipe 6.4); F5 size for round 2 (recipe 7.2) |
| Commits from 30 held-out repos | 400 | Commit transfer before any ejs-5 read |
| Public: our own 10% splits (by page or record; never official dev or test) | 600 | Public-block check |
| F14 hold-out family: one skill family that is never trained (the QC agent picks it, for example constraint scheduling) | 400 | Report only: transfer to an untrained family |
| Codebook behavioural tests (generic labels, swapped labels, exclusion pairs) | 300 | Report only |
| **Total** | **about 8,500** | Never used for the final ship decision |

Rules for this set (rules S7):
- No item shares a `group_id` or normalized text with golden_train or with any C training row.
- Wikipedia-based public items are split by page title.
- Commit items come from the 30 held-out repos of both commit datasets. **(v4, B1)** They mirror the training form:
  30% of their route, triage and gate items are message-only (same keep rule), inside the 400.
- The 50 held-out format styles are C-side only. The sealed suite has its own styles.
- Temperature refits use dev or this set only (recipe 6.4).
- **(v4, B3) Yes-share drift alarm, report-only.** At each training snapshot the dev read logs, per part and per
  domain (each family, commit type, public dataset and F14), mean P(yes) and the predicted yes share on yes/no items,
  without using gold. Snapshot reads use a fixed T stated in advance: T = 1 (C1's recipe 6.0 serving T is not yet
  fitted for snapshots). Alarm if a domain that is 50/50 by construction falls outside 30-70%. An alarm is logged and
  reported; it never moves a share, weight, temperature, readout or candidate by itself (any change needs an
  amendment before round 2).
- **(v4, A2)** Ordinal items here also log the end-level ratio (end-level predictions / end-level gold), report-only.

---

## 11. Build plan and agents (at most 30 running at once)

**Order rule (G14).** Step 1 ends with the sealed suite frozen and its sha256 committed in a PREREG amendment. Steps
2-9 start only after that commit. Exception: spec agents may draft G0 specs earlier, but no generator, pack, style,
codebook, public row or commit row may exist before the commit, and the build log shows the order. The C plan also
needs its own PREREG_FINAL amendment before any C training row or candidate exists (recipe header).

| Step | Who | Output |
|---|---|---|
| 1 | Sealed agent (1-2, isolated; reads `sealed_brief/`) | Sealed suite frozen + exports (section 9); sha256 in a PREREG amendment |
| 2 | Spec agents (13, one per family) | G0 specs; ambiguity review by a second session |
| 3 | Domain-pack agents (4) | >= 300 packs, decontaminated; (v4) persona seeds from O*NET titles, never PersonaHub |
| 4 | Format agents (2) | 400-style pool (50 held out), wording pools, codebooks for 2.3 |
| 5 | Generator agents (13) | >= 4 training samplers + S5, solver B, parser, metamorphic tests; G2-G4 at 100% |
| 6 | Public-data agents (3) + commit agent (1) | Section 3 and 4 builders, pinned, licence-checked, deny-list-checked (3.H) and decontaminated; (v4) commit: message-only rows with trigger check and shortcut negatives (B1), per-rule yes rates (B2), score level floors (A2), `option_level` + G18 (A1) |
| 7 | Blind readers (4-6, never authors of what they read; flag-only) | G5 reports |
| 8 | QC agent (1) | G6-G8, G10-G12, G15 reports; F14 and behavioural tests |
| 9 | Mixer (1) | Deny-list and licence join, replay sample, relations, C1-target merge, token cap, final files, input-path log, manifest, sha256; (v4) replay `option_level` detection and the ordinal target lint on final targets (A1, G18, 100% pass), replay yes rate per wording (E2) |
| 10 | Orchestrator | Deny-list program over `used_sources.json` (hits only); counts-only decontam runs (G13, decision 1); scoring crowd on the free L4 (G9); re-derived D2 (7.3) |
| 11 | Owner | Round GO (paid steps), the Jev-read spend GO, optional audit (G16), any override of section 12 |

Peak concurrency: steps 3-7 overlap, about 25-30 agents.

---

## 12. Owner decisions: decided by default (the owner may override)

These were open questions in v2. On 3 Oct the orchestrator applied these defaults, as recorded in memory
`final-goal-30sep.md`. Each one is **decided by default; the owner may override** by a PREREG amendment before the
first C training row is generated. An override after that point needs its own amendment, which states what it
changes.

| # | Decision (default) | Effect in this spec |
|---|---|---|
| 1 | **Counts-only decontamination scripts are run by the orchestrator**, under the owner's earlier count-only approval. Targets: OHS-3, ejs-5, LongBench v2, the DI test sets, the 152 forbidden tasks, all splits of the OHS source datasets, TabFact tables, and the sealed suite. The scripts print counts and training ids only | 4.3, 7.1, 7.2, G13, step 10 |
| 2 | **Claude may be a flag-only blind reader.** It never sets, edits or chooses a label; labels come from programs or human gold | 2.1, G5, step 7, 9 |
| 3 | **The scoring crowd pass (C1 + 4B-E + base 4B) runs on the free L4**, not the H100: about 20-28 h, no Modal spend | 2.1, 5, G9 |
| 4 | **Replay grandfathering: drop both groups.** (a) Forbidden-list rows boolq, condaqa, dbpedia, banking77 (4,866). (b) Claude-gold rows binj/std/hard/planted/proc (8,607). Never grandfatherable: civil_comments, toxic_conv, br_newsmtsc | 5 |
| 5 | **Disclose and exclude NewsMTSC.** C1 trained on 607 `br_newsmtsc` rows whose text is non-commercial POLUSA. The C1 model card and any C claim disclose this. NewsMTSC and anything using POLUSA are out of C (new and replay) | 3.G, 5 |
| 6 | **A creator's own HF card is NOT an official licence record.** DocFinQA is out (fallback F13, +250 / +500); any other (H) set is out unless an upstream record is found. This covers replay too: 15 replay sources (38,521 rows) whose only record is the creator's HF card are "verify upstream or drop" (section 5). The 3 Oct licence merge reads this as HF cards only: a creator's Kaggle page that is the dataset's only official release, with a structured licence field, counts (Sarcasm v2). If the owner reads it more widely, Sarcasm v2 goes out (fallback XED +175 / +350, GHC +175 / +350) | 3.1, 3.2, 3.G, 5, G1 |
| 7 | **The Zenodo rule as written.** "Zenodo" in the OHS list means the OHS-3 Zenodo record text, not Zenodo hosting. C1's 7 Zenodo-hosted sources stay (the counts-only OHS-3 check found no overlap), and CommitChronicle (Zenodo-hosted) is allowed. **CodeReviewer is out** | 3.G, 4.3 |
| 8 | **Share-alike is allowed** (CC BY-SA, ODbL), with a third-party notices file. Data and derived rows are never published. The notices file lists every CC BY, MIT, BSD, Apache and SA source (new and replay) and every commit repo | 3.1 |
| 9 | **Flagged document-text licences are dropped unless the licence check clears them.** Covers QuALITY Slate/OANC articles, Qasper papers without a CC BY / CC0 licence, DocFinQA, and MultiHiertt plus ConvFinQA (FinTabNet text). **Applied (3 Oct licence merge):** QuALITY Slate/OANC is cleared (OANC terms verified); Qasper keeps papers with an arXiv CC BY, CC BY-SA or CC0 licence; DocFinQA, MultiHiertt and ConvFinQA are out (3.G), and replay `gd_finqa` is "verify upstream or drop". FinTabNet's CDLA-Permissive-1.0 is stated only in two papers (IBM's record not reached) and is not on the 3.1 list. They return only by PREREG amendment after IBM's record is read **and** the owner accepts the licence | 3.1, 3.2, 3.G, 5 |
| 10 | **Jev IS read once on the sealed suite.** The goal's "+1 pt vs Jev on the new-domains suite" criterion needs it. It runs at the C look, after the ship verdict. It is report and evaluation only, never training or selection. The API spend is a GO point | 7.4, 9 |
| 11 | **The founder's 200-row audit is optional and non-blocking** | G16 |
| 12 | **(merge 3 Oct) Unverified means out; third-party text is recorded, not a blocker.** A dataset or document text with no readable official licence record is out of training (new and replay), like NC. Third-party user or press text inside a dataset with a verified licence (XED subtitles, MAMS reviews, Sarcasm headlines, GHC and EDOS posts, Wikipedia, commit messages) is recorded in the register and stays in | 3.1, 3.2, 3E; register 6 |

Still owner-only (not defaulted): every paid GPU step (round GO), the Jev API spend, OHS-3 and LongBench reads, any
public upload or leaderboard submission.
