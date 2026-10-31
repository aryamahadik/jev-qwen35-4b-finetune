# yn2b SPEC (draft): hard yes/no data for the final 2B

**Status:** DRAFT for owner review, 30 Sep 2026. Nothing is built, trained or edited yet.
**Inputs:** the gap analysis (`gap_targets.json`), the JevBench v1.5 family specs, three designs (exam-gap
`suite_examgap.json`, agentic `agentic_suite.json`, robust `robust/suite_spec.json`) and the owner + Codex
must-haves (`REQUIREMENTS_review.md`).

**Rules for every step (breaking one rejects the data):**
- Follow GOLDEN_SPEC. Labels come only from a deterministic CPU program that Claude writes. No model labels anything.
- No model bigger than our 4B. No Jev outputs.
- No JevBench item text. OHS-1 and OHS-2 are analysed only, never copied or fitted.
- OHS-3 is read only by programs, which print counts and never text.
- A PREREG_FINAL + FINETUNE_PLAN amendment is committed before 2B step 0.
- GPU work starts only after the owner says GO.

---

## 0. Summary

- **What:** 8 generator families, 20,000 rows: 12,700 yes/no, 5,000 choice and 2,300 score. About 1,000 attack twins
  come on top, for about 4.0% of the 2B training file.
  - **Wave 1** (6 families, 17,500 rows) is the core.
  - **Wave 2** (2 families, 2,500 rows) goes in only if it passes every gate before the A/B starts.
- **Targets:** the 2B's largest measured gaps, and the three new JevBench v1.5 families. Those are the tool-call
  guardrail, state tracking and lead-qualification Score. Today we have 0 guardrail yes/no rows, 0 state-tracking
  rows and 0 score rows.
- **Labels:** exact program gold only. There is no 4B teacher on these rows, so the trainer target is 0.95 / 0.05.
- **Gate into the 2B:** a pre-registered 2-arm A/B of short 2B runs. The data must show:
  - a gain on held-out generator families and templates;
  - a gain on external dev splits;
  - no regression on the full dev set, multiple choice, the unseen-source test, calibration, flip rates and security
    (jagged, OPI, redef).
- **If the A/B passes,** the 2B main run trains on `train_2b_golden_kd_yn2b.jsonl`. **If it fails,** the 2B trains
  on the plan-of-record file, unchanged.
- **Time and cost:**
  - Build: about 2 days of CPU work by 5 Claude agents, starting now while the 4B trains.
  - A/B: about $20–25 (about $30 with the optional arm C), 0.5–1.2 days.
  - 2B main run: about +4% steps, about +$3.
- **Owner decisions:**
  - **D1:** the teacher gate on generator rows (optional arm C).
  - **D2:** the PRISM-X I override amendment. It is needed whatever happens to yn2b.
  - **GO** for the GPU steps.

---

## 1. Scores of the three designs (1–10, 10 = best / safest)

| Axis | exam-gap | agentic | robust |
|---|---|---|---|
| Expected gain (measured gaps + v1.5 families) | 8 | 6 | 8 |
| Label-correctness guarantee | 8 | 8 | 9 |
| Contamination / leakage (10 = safest) | **3** | 7 | 9 |
| Multiple choice / no-regress (10 = safest) | 7 | 7 | 9 |
| Build effort and time (10 = fastest) | 6 | 5 | 8 |
| Pipeline fit | 8 | 7 | 7 |
| **Mean** | **6.7** | **6.7** | **8.3** |

**exam-gap.** It has the best gap evidence and a clean pipeline: new files, correct `kd_skip_src` semantics, and the
PREREG §10.10 row-count note.
- **Fatal flaw in its top family, F1 `gen3_meta_frame`.** Its frames are the held-out dev_negwords family
  `dialogue_rebuttal` (`build_v11_fixes.py:218-224`):
  - "X says P. Is X mistaken?";
  - "two conflicting notes";
  - "does the text undercut the reply?";
  - "in a debate".

  dev_negwords supplies 422 of the 3,847 rows of the primary ship test (rotten_tomatoes 70, irony 82, climate 90,
  spam 90, cb 54, bbc 36). Training on these frames would turn a held-out transfer test into an in-family test. A
  6-gram check does not prevent this.
- The rest is sound. It is also the slowest design (42 h for the full set).

**agentic.** It is the best on the JevBench v1.5 families: guardrail, output check, state, dialogue/trajectories and
lead score. It uses two checkers and a 100-row blind solve.
- It covers only one measured local gap (policy chains). It has no negation, literal-definition, table or moral work,
  and it expects about 0 gain on OHS and broad dev.
- It is the largest code base (about 9,600 lines, 4–5 days serial).
- It proposes dropping the teacher on about 88K rows wherever the teacher is ≥15% wrong. That is broad.

**robust (base).**
- It found the dialogue_rebuttal leak and replaced it with a leak-safe polarity ladder. A prototype
  (`robust/ladder_proto.py`) checks for 6-word runs, dialogue cues and cue shares.
- It keeps the 64/36 yes/no–choice mix and adds choice rows where the 2B trails.
- Its label guarantee is the strongest: decide + decide2, parse-back, verbatim grounding, and rejection of items with
  two independent reasons.
- It protects the attack-success gates with an authority rule.
- It noticed that the PRISM-X I override is missing.
- **Weaknesses:**
  - It writes the merged file under the existing name `train_2b_golden_kd.jsonl`, which hides which file trained.
  - Its JSON note says to write rows to `v14_parts/raw/`, which a golden rebuild would pick up.
  - It gives no A/B design.

---

## 2. Synthesis: robust as the base, plus grafts

| Taken from | What |
|---|---|
| robust | Shared multi-view engine; F1 long rule chains; F2 guardrail; F3 state tracking; F4 polarity ladder (no dialogue frames); authority rule; QA gates; teacher Option B; PRISM-X override note |
| exam-gap | F6 literal definitions **promoted to wave 1** (the most significant OHS gap: 28 vs 4 discordant pairs, p<0.0001; cheap to build); F1b short numeric claim checks (vitaminc-style boundaries); new output file names (never overwrite); amendment items (§10.10, the design shaped by OHS/dev misses, yn2b_dev report-only); "no single shortcut above 60%" rule |
| agentic | Dialogue-slot and agent-trajectory machines inside F3; output-check and judge views inside F2; F5 lead score **promoted to wave 1** (Score is 1/3 of Intelligence; Jev leads Qwen-4B fine-tunes on sealed Score 81.1 vs about 62; we have 0 score rows); the commitment metric (share of answers outside 0.2–0.8) in every report; blind solve of 100 rows per family |
| gap analysis | New rows train on gold only; teacher-error evidence (re-run today: 29,515 generator yes/no rows, teacher wrong on 22.1%, 35.8% of kd-0.5 targets inside 0.2–0.8, down to 13.7% under Option B) |

**New in this spec:**
- The pre-registered A/B (section 12). The owner's must-haves require it. FINETUNE_PLAN §7 had rejected a "20K-row A/B
  pilot" as unresolvable; this version is built to be resolvable.
- An unseen-set check that includes the new file (section 8.4). The registered ship run only reads golden_train plus
  the lineage files.
- F4 also builds ladders on **human-gold golden_train label propositions**. This follows the v11 precedent, which took
  dev_negwords from 73.2 to 82.5 through held-out frames. It targets transfer to dev_negwords, not only program
  decisions.
- F6 definitions sit in the **card**, the trusted field, and 10% of F6 twins plant a counter-definition in the text
  with the gold unchanged. This protects `eval_redef`, one of the 2B's `ablate_splits`.
- A cap on unit size, for `micro_tokens` 16384.

---

## 3. Facts checked today that constrain the build

1. **`kd_skip_src` matches `meta.teacher_src`, not the row's source** (`train_decoder.py:686-691`). A source name in
   that list does nothing.
   - A new row with no `meta.teacher` trains on `gold*(1-2*0.05)+0.05` (`train_decoder.py:302-303`, EPS default
     0.05).
2. **`kd_full_src` uses a yes/no teacher alone as the target** (`train_decoder.py:304-305`).
   - `build_2b_kd.py` gives no fresh teacher to yes/no rows of those sources.
   - Attacked twins copy the partner's teacher only if it gives the gold answer.
3. **The golden assembler reads `data/v14_parts/raw/*.jsonl`** (`build_v14_golden.py:78`). New raw rows must never go
   there.
4. **Upload rules** (`modal_od.py:55-73`):
   - Only the `V14_KEEP` files inside `v14_parts/` are uploaded.
   - Top-level `data/*.jsonl` files are uploaded.
   - Other `*_parts/` folders are ignored.
5. **The ship rule re-derives the unseen set** from `golden_train` plus the REF lineage files only (`gate_dev.py:110`,
   `derive_unseen` at 186-226). A new training file is not checked by a registered run.
6. **The dialogue_rebuttal frame family is held out** of all training (`build_v11_fixes.py:224`).
7. **PRISM-X I is not adopted for the 2B unless an override amendment exists** (PREREG_FINAL §1). `runs/q35_2b_main.json`
   already has `"prism_x": "I"`.
8. **JevBench formats** (`jevbench_od.py:20-44`):
   - dict states are rendered `json.dumps(indent=1, ensure_ascii=False)`;
   - the yes/no card is `- Yes: …\n- No: …`;
   - Score options are `"i: level text"` with no card.

   **v1.5 scoring** (METHOD-v1.5 §3.1):
   - Noul with 0.2 < P(yes) < 0.8 counts as wrong;
   - Score uses the expected position, scored by nMAE.
9. **golden_train today:** 501,732 rows, 64.55% yes/no, 0 score rows, 0 proposed tool calls in any state, 290
   tool-selection choice rows.

---

## 4. The families

| # | Source key | Wave | Rows | yes/no | choice | score | Dev (iid + holdout) | Main target |
|---|---|---|---|---|---|---|---|---|
| F1 | `gd_gen3_rule_chain` | 1 | 4,000 | 2,500 | 1,500 | 0 | 400 | pg_dev yes/no 76.2 (4B-E) vs 65.0 (v11r) / 62.7 (pilot); long yes/no 78.3 vs 61.4; pg_numeric 71.1 vs 55.6; JevBench long_policy (2B commits 0/5) |
| F2 | `gd_gen3_tool_guard` | 1 | 5,000 | 3,500 | 1,500 | 0 | 500 | JevBench v1.5 guardrail (48 open + part of 180 sealed Noul); adequacy 2B 8/12; 0 rows today |
| F3 | `gd_gen3_state_track` | 1 | 3,500 | 1,700 | 1,100 | 700 | 350 | v1.5 state tracking (at least 12% of every type); about 0 rows today |
| F4 | `gd_gen3_polarity_ladder` | 1 | 1,500 | 1,500 | 0 | 0 | 300 | dev_negwords 86.1 vs 73.0; the 2B contradicts itself on 23.5% of complement pairs vs 4.8% for the 4B; only 1,107 double-negation rows |
| F5 | `gd_gen3_lead_score` | 1 | 2,000 | 400 | 0 | 1,600 | 200 | v1.5 Score (80% of open Score items are new); 0 score rows today |
| F6 | `gd_gen3_def_literal` | 1 | 1,500 | 1,100 | 400 | 0 | 150 | OHS-1 hearsay-style 56.1 vs Jev 85.4 (4B false-No 34 vs 2); inherited by the 2B through the teacher |
| F7 | `gd_gen3_norm_action` | 2 | 1,500 | 1,200 | 300 | 0 | 150 | OHS-2 moral_stories 85.0 vs 97.5 |
| F8 | `gd_gen3_table_layouts` | 2 | 1,000 | 800 | 200 | 0 | 100 | OHS-2 tabfact on short tables 84.4 vs 96.1 |
| | **Total** | | **20,000** | **12,700** | **5,000** | **2,300** | **2,150** | |

**Mix.** yes/no is 63.5% of the new rows. With golden, the combined yes/no share is 64.5%, the same as today, so the
multiple-choice share does not move.

**Attack twins** (`inv`) add about 1,000 rows (8% of base rows of F1, F2, F3, F5 and F6). The final total is about
21,000 rows, 4.0% of 522.7K.

**No cheap filler.** F3 already contains ticket SLA and dialogue slots. F2 already contains the output checks.
Nothing is padded to reach a count.

**If time runs short:** each family goes to the A/B only after it passes every gate, in the priority order F4 → F2 →
F1 → F3 → F5 → F6. A family that has not passed every gate is never added.

---

## 5. Shared engine: `golden_src/gen3/mv_core.py`

### 5.1 Latent item
```
Latent(family, pack, facts: dict, query, latent_id, split in {train, dev_iid, dev_holdout}, seed, tier)
decide(latent)   -> (gold, trace)     # primary evaluator on the typed facts; trace = decisive facts + rule ids
render(latent, fmt, rng) -> state     # one of the formats in 5.3
parse(fmt, state) -> facts            # parse-back of the RENDERED text
decide2(facts)   -> gold              # independent evaluator, written by a different agent (section 9)
shortcuts        -> [callable(latent) -> answer]   # heuristics used for tiering only, never for labels
```

### 5.2 Views (one `call_id` unit per latent item; at most 5 rows per unit)

| View | Rule | Relation | Share of latents |
|---|---|---|---|
| base | the yes/no, choice or score question | — | all |
| contrast twin | flip exactly one decisive atom (at most 3 lines differ); gold flips under both evaluators; `meta.twin_of` | none (same call_id) | about 50% |
| ladder | the same state, the question at another polarity level from the F4 quads | para↔neg `complement`; para↔dneg `equiv` | 30% of yes/no latents |
| format-equivalent | the same latent in another format; choice rows keep the identical option set | `equiv` | about 30% |
| choice mirror | options = gold + the answers of named shortcut solvers (+ "none of these" 20%) | none (same call_id) | about 30% |
| attack twin | an imperative planted **only in an untrusted sub-field** (tool result, email, rep note, document footer, log note); gold unchanged | `inv` (a = clean) | 8% of base rows |

- Each row is in at most one `complement` relation.
- All views and twins of a latent item sit on the same side of the train/dev split.

### 5.3 Formats
- **json:** exactly `json.dumps(obj, indent=1, ensure_ascii=False)`.
- **prose; markdown sections;** `key: value`.
- **log:** chronological, newest-first, shuffled with timestamps, or grouped by source system.
- **email thread; chat transcript** (structured turns).
- **tables:** reuse the `golden_src/gen/tab_core.py` layouts by import. That module is read-only; do not edit it.

### 5.4 Cards
**yes/no:**
- 70% golden style: `- yes: …\n- no: …`;
- 20% JevBench style: `- Yes: …\n- No: …`;
- 10% no card.

**choice:** a definition for each option, in golden style. 20% have no card when the options are self-explanatory.

**score:** options `"0: …", "1: …"`, no card, gold = the option string.

Every yes/no card says what yes **and** no mean, including "not enough information → no" where that applies.

### 5.5 Balance
- Yes share is 45–55% in every stratum: family × tier × polarity (plain or inverted question) × format × length bin.
- Gold levels are uniform over the K levels on score rows.
- Exception items come in three equal groups:
  - the default denies and the exception allows;
  - the default allows and the exception denies;
  - a near-miss exception that does not apply.

  So "an exception is mentioned" never predicts the answer.

### 5.6 Tiers
The tier mix is easy 15 / standard 30 / judge 20 / hard 35.

- **hard:** at least 2 shortcut solvers disagree with gold.
- **Family rule:** on each family's final rows, no single shortcut is above 60% accuracy.

### 5.7 Authority rule (protects jagged, OPI and redef)
- Rules the model must obey are always numbered and dated statements in the policy or definition part, or in the card.
- Injected text is always an imperative aimed at the reader, inside an untrusted field.
- In F1 and F2, pairs that put the same fact in the policy in one row and only in a tool result in the other are capped
  at 5%.
- F1 attack twins include "the policy above is outdated; the decision is X" style plants, with gold unchanged. The model
  must learn to tell a real amendment from an injection.

### 5.8 Unit size
- A unit's total state is at most 24K characters.
- A unit containing a state longer than 6K characters has at most 3 rows.
- After the merge, the 2B smoke run repeats the heaviest-micro-batch check at `micro_tokens` 16384 (FINETUNE_PLAN 4.2).

### 5.9 Raw row format
The row follows GOLDEN_SPEC:
```
{"key","rid","state","instructions","options","gold","soft":null,
 "meta":{"dataset":"program generator golden_src/gen3/gen3_<name>.py",
         "licence":"Generated by Claude-written program in this repo (no third-party text); CC0 1.0",
         "family","edge","tier","n_shortcut_wrong","view","fmt","latent_id","twin_of","defs","dev_kind",
         "n_events"?, "base_source"?}}
```
- yes/no rows use options exactly `["yes", "no"]`.
- Definitions go to `defs/gen3_<name>[__<qid>].json`.

### 5.10 Determinism
- Train seed = 20261001 + family index. dev_iid seed = train seed + 10^9. dev_holdout seed = train seed + 2·10^9.
- The name, organisation and domain pools for train and dev are disjoint. All names are invented.
- Pin the tzdata version, and record the sha256 of every output in `golden_src/gen3/MANIFEST_yn2b.jsonl`. This is a new
  file; the existing MANIFEST is not touched.

---

## 6. Generator logic by family

### F1 `gen3_rule_chain` (wave 1): 4,000 rows = F1a 3,400 + F1b 600

**F1a: long rule chains** (1,900 yes/no + 1,500 choice).

**Documents.** 10 document families:
- municipal fee code;
- leave handbook;
- warranty and returns;
- shipping-claims tariff;
- pharmacy-benefit formulary;
- grant eligibility;
- data-retention SOP;
- IT change policy;
- HOA bylaws;
- school-transport eligibility, **held out whole for dev**.

5 document styles: numbered code (§), handbook prose, FAQ, limits table plus clauses, contract. Contract is **held out
for dev**.

About 1,000 of the rows come from `gen2_long_policy`'s families, imported read-only, with `fit_state` bounds of
1,500–6,000 characters, new seeds and a new output key.

Never import `lean/pg/*`: pg_dev must stay an external probe.

**Rule program.** `Clause(id, kind, atoms, effect)`, where kind is one of:
- definition;
- entitlement / permission;
- exception;
- exception-to-exception;
- amendment (effective date; replaces a clause text or a threshold);
- precedence;
- cross-reference;
- limit table;
- time rule (business days, a named time zone).

The atoms reuse `pe_atoms`, `nd_money`, `nd_time` and `nd_units` by import.

**Evaluation.** An interpreter applies the clause graph to a typed case (dates, amounts, roles, statuses, counts,
units) and returns the outcome plus a trace.

**Independent check.** Every clause renderer registers a parse regex. `decide2` rebuilds the clause graph from the
rendered text and re-evaluates it.

**Hardness knobs:**
- reasoning steps: 1–5;
- distractor clauses: 2–15 (superseded revisions, a rule for a neighbouring case, parties with the same name);
- the decisive clause in the first, middle or last third, balanced;
- exception depth: 0–2;
- an amendment in force before or after the event;
- numeric boundary triples: 25% exactly at the limit, 25% within 1 unit or 1%, with inclusive and exclusive wording
  varied;
- length: 85% at 1,500–6,000 characters, 15% at 6,000–12,000.

**Queries:**
- yes/no: "Is <outcome> the result?", "Is the fee waived?", with 30% asked inverted;
- choice: an outcome code (4–6 options), "which clause decides" (with "none of these"), or an amount bin.

**Shortcuts:** ignore exceptions; any mentioned exception applies; ignore amendments; the latest-dated clause wins;
keyword overlap; every boundary is inclusive; the first matching clause wins.

**Twins:** flip one of these:
- a date across an effective date;
- an amount across a threshold by 1 unit;
- a role or status;
- the event day across a business-day window.

**F1b: numeric claim checks** (600 yes/no).
- **Input:** a 1–4-sentence evidence text with figures, "as of" dates, revisions, units and rounding, plus a crisp
  claim.
- **Claim wording:** "at least", "more than", "fewer than", "exactly", "up by more than X%". "About" appears only with a
  tolerance stated in the card.
- **Boundaries:** 30% of claims sit exactly at the boundary, 30% within 1 unit or 1%.
- **Label:** exact rational arithmetic.
- **Twins:** move the figure by one unit, or switch to the revised figure.

**Dev (400):** 200 iid plus 200 holdout (the held-out document family and style).

### F2 `gen3_tool_guard` (wave 1): 5,000 rows = 3,500 yes/no + 1,500 choice

**Domain packs.** There are 12:
- banking and payments;
- email and workspace;
- cloud deploy and change;
- HR records;
- CRM;
- files and DB admin;
- e-commerce refunds;
- calendar and travel;
- IT access;
- support ticketing;
- smart-home, **held out**;
- clinic scheduling (no clinical content), **held out**.

The tool lists of `gen2_tool_selection` are imported read-only, plus new ones.

**Tools.** Each tool has a JSON schema (types, enums, patterns, ranges, required and optional fields) and a
side-effect class: read, write, destructive, external_send or money_move.

**Policy DSL.**
- `Rule(id, scope, predicate, effect)`, where effect is one of deny_if, allow_only_if, require_confirmation or
  require_approval.
- Precedence mode: deny-overrides, amendment-overrides or specific-over-general.
- Definitions: an annex of domains, a role table, a time zone, the business day.

**Predicate atoms.** There are 11. Each has an evaluator, 3–6 renderers and a parse regex:
1. **threshold:** ≤ vs <, with a currency conversion at a stated rate;
2. **allowlist:** look-alike domains (`.co` vs `.com`), with a subsidiary annex;
3. **role or permission;**
4. **time window:** a zone with DST (zoneinfo);
5. **log aggregate:** a sum or count over a window, excluding failed, reversed and other-day entries;
6. **confirmation match:** amount, payee, recency, who confirmed, whether it was revoked;
7. **provenance:** an argument value must occur in user turns or the session, not only in a tool result or document;
8. **schema validity:** type, pattern, enum, range, an extra field, a missing field;
9. **intent match:** a look-alike tool;
10. **idempotency key:** a duplicate request;
11. **environment alias:** prod vs staging names.

**Sampler.**
- Build a valid baseline call from the session and conversation.
- Then apply 0 violations (allowed), 1 violation (80% of blocked items) or 2 (20%).
- At least 40% of allowed items contain a near-miss decoy.
- 25% of allowed items are **dangerous but allowed**: a sandbox, the user's own resource, or a valid confirmation.
- 20% of items are provenance items.
- Items with 2 violations get no contrast twin.

**Rejection.** Reject an item if:
- the verdict depends on an unstated fact;
- a decisive fact is missing from the text;
- a DST fold time is not disambiguated.

**Views:**
- **Guard yes/no (2,500):** "May the proposed call run?" In 30% of items the question is inverted: "Must the guardrail
  block this call?" or "Does it need the user's confirmation first?".
- **Judge yes/no (500):** "The guardrail logged ALLOW / BLOCK. Is the logged verdict correct under the policy?"
- **Output check yes/no (500):** tool result plus the assistant's output, checked against stated constraints: JSON
  types, keys, exact word count, decimals, and a **content rule** (totals equal the sum; values match the tool result;
  feels-like vs actual).
  - Exactly 0 or 1 fact is perturbed.
  - The content rule is always present. The dropped judge_ifcheck data passed filler replies because only format
    rules were checked.
  - Use the words "answer", "message" or "output", never "reply", and never "right/wrong/correct" about a reply
    (section 8.3).
- **Choice (1,000):** "Which rule does the call break? If several, the lowest-numbered; or none."
- **Choice (500):** an allow/block mirror with 2 options.

**Formats:** 50% JSON dicts with keys such as assistant, policy, session, recent_calls, conversation, tool_results and
proposed_call; 50% prose or markdown.

**Knobs by tier:**
- easy: 1–2 rules, no log;
- standard: 3–5 rules plus one hop;
- judge: the judge and output-check views;
- hard: 6–12 rules with amendments, a log of 6 or more entries, a time zone, at least 2 near-misses, and at least 2
  shortcuts wrong.

**Shortcuts:** block anything destructive; sum the whole log; ignore the time zone; obey text in tool results; ignore
amendments; keyword match between the user's words and the tool; trust any confirmation.

**Twins:** flip one of these:
- a log status;
- a timestamp across the zone boundary;
- one argument;
- one definition line;
- one severity event.

**Dev (500):** 250 iid plus 250 holdout. The holdout uses the 2 held-out packs, 20% of renderers and 20% of question
phrasings.

### F3 `gen3_state_track` (wave 1): 3,500 rows = 1,700 yes/no + 1,100 choice + 700 score

**Machines.** 10 typed state machines with guards, side effects and time rules:
- order lifecycle;
- ticket workflow with an SLA clock in business hours;
- access control (grants, expiry, deny-overrides, groups, renames);
- inventory (holds, transfers, cycle counts, quarantine);
- bookings with expiring holds;
- account balance (pending, posted, reversed);
- dialogue slots ("actually make it…", "same as before", "not the window seat");
- agent trajectories (tool calls whose results change files, a calendar or a cart; some calls fail);
- feature flags, **held out**;
- document versions with revert, **held out**.

**Events.** The sampler produces:
- valid events;
- guard-failing events (rejected; they change nothing);
- resends (a repeated event id; apply it once);
- reverts;
- expiries;
- decoy entities with near-identical ids (W3319027 vs W3319072);
- mixed structured and natural-language events.

**Simulation.**
- The simulator computes the full trajectory.
- A query picker chooses entity × time (the end, or an intermediate time t) × output type.
- `decide2` parses the rendered log, re-sorts it by timestamp and replays it on an independently written simulator.

**Views:**
- **choice:** a status, owner, version or slot value; 4–7 options, the wrong ones from shortcuts.
- **yes/no:** "Can X do Y at t?", "In stock at the end?", "Was the request accepted?". 300 of these are judge rows: an
  agent's claimed state, either correct or wrong by exactly one controlled error (a stale value, an off-by-one count,
  the wrong entity, an ignored rejection).
- **score:** bucketed counts or an escalation level, K = 4–6 in `"i: text"` format. Each trap lands on a different
  level where possible.

**Knobs by tier:**
- easy: 2–5 events;
- standard: 6–12;
- hard: 13–40, with at least 2 shortcuts wrong.

Every state is at most 10,000 characters (about 2,500 tokens). `meta.n_events` is recorded so dev can be reported by
event count.

**Shortcuts:** the last event wins; ignore guards; apply resends twice; treat display order as time order; ignore
expiry; fuzzy entity id.

**Dev (350):** 175 iid plus 175 holdout (the 2 held-out machines).

### F4 `gen3_polarity_ladder` (wave 1): 1,500 standalone yes/no, plus ladder views inside F1, F2, F3 and F6

**Quads.** Each quad is frame × switch A × switch B. This gives:
- para (0 flips);
- neg (1 flip, via A or via B);
- dneg (2 flips).

Gold = truth(P) XOR flipA XOR flipB.

**Frame families.** There are 10: the 7 in `robust/ladder_proto.py` (verdict_record, decision_direct, exception_scope,
gatekeeping, burden, checklist, counter_hypothesis) plus sign_off, compliance_flag and audit_finding, which are still
to write. 8 are used for training and 2 are **held out** for dev.

**Base propositions P:**
- **(a) 750 rows on human hard-gold golden_train rows.**
  - Exclude rows with a vote-share teacher, `gold_probs`, the roles attacked, defswap or neg, and `gd_gen*` sources.
  - For choice rows, P = 'the right label for the text is "L"'. L is the gold label (50%) or the nearest wrong label
    (50%), by definition word overlap, as in `build_v14_golden`'s near-miss rule.
  - For yes/no rows, use question-form quads.
  - The card is the definitions of L, the gold label and up to 4 other labels, the same convention as the golden
    near-miss bundles.
  - `group_id` and `call_id` are the base row's, and `meta.base_source` is recorded.
  - The label is the human gold transformed by a program. That is a construction, not a model label.
- **(b) 750 rows on program decisions** from F1, F2, F3 and F6 latents (slot `{d}`, for example "the proposed
  transfer_funds call may run under the policy").

**Constraints:**
- 50% of rows have depth 0, and depth is balanced against truth(P), so counting negations is exactly 50% accurate.
- Every cue word is at most 60% tied to answer-flipping questions (`build_v11_fixes.cue_shares`).
- No 6-word run is shared with the dialogue_rebuttal templates, any v11 train template, or any dev_negwords or
  dev_claims instruction.
- **Banned cues:** reply, replies, commenter, debate, "two notes", a speaker label "Name:", agreed, disagree, back,
  undercut.

**Relations:** para↔neg `complement`; para↔dneg `equiv`.

**Dev (300):** 150 iid plus 150 holdout (the 2 held-out frame families).

### F5 `gen3_lead_score` (wave 1): 2,000 rows = 1,600 score + 400 yes/no

**Rubric archetypes.**
- Train uses 3:
  - a points table with bands, caps, negatives, recency windows, disqualifiers, thresholds and post-threshold
    overrides;
  - a criteria-count ladder (BANT) that counts only the prospect's own words;
  - a gated ladder.
- Dev holds out 1: a weighted scorecard with a tie-break rule.
- 10 industry packs, 2 of them held out.

**Latent lead:**
- company size, from both the enrichment figure and a self-reported range;
- title → seniority table ("Assistant to the VP" scores 0);
- budget: amount, period (monthly / annual / per seat) and status (approved / requested / hoped / hypothetical);
- target date relative to "today";
- events: type, date, attended flag, duplicates;
- email domain (a personal-domain list);
- customer, competitor and region flags;
- decoy secondary contacts;
- rep notes and quoted bosses, which never count unless the rubric says so.

**Scoring.** A scorer computes the points and the level. `scorer2` recomputes both from the parsed text.

**Sampling:**
- 40% of items land within ±3 points of a threshold;
- every item has at least 1 trap that moves the level if misapplied (at least 2 for hard items);
- levels are uniform over 0..K−1, with K = 3–6.

**Views:**
- **Score (1,600):** "What qualification level does the rubric give this lead?"
- **yes/no (200):** "Is this lead sales-ready under the rubric?"
- **judge yes/no (200):** "The SDR scored this lead N because …; is that score right under the rubric?" Here "SDR" is
  a record author, not a dialogue.

**Shortcuts:** ignore the window; ignore the cap; trust rep notes; use the self-reported size; count registrations;
score the wrong contact; treat a monthly figure as annual.

**Twins:** one fact moves the level by one, or a disqualifier moves it to 0.

**Dev (200):** 100 iid plus 100 holdout (the held-out archetype and industries).

### F6 `gen3_def_literal` (wave 1): 1,500 rows = 1,100 yes/no + 400 choice

**Domains.** 10 packs:
- evidence rules of a fictional tribunal;
- sports eligibility;
- club membership;
- insurance terms;
- school policy;
- platform content rules;
- procurement;
- tenancy;
- grant rules;
- workplace safety.

2 packs and 3 invented terms are **held out**.

**Definition.** A term T is defined by 2–4 elements joined by AND or OR, plus 0–2 stated exclusions. The operative
definition sits **in the card** (trusted). The facts sit in the state.
- 30% of items use a real word (resident, employee, damaged, new) with a deliberately different definition.
- Never use "hearsay" or Federal Rules of Evidence wording, so OHS-1 hearsay stays an untouched probe.

**Facts.** Each fact pattern includes 1–3 outside-knowledge distractors that the definition ignores: a party admission,
a business record, probation, a family tie, good faith, de minimis.

**Gold:** every element is met AND no stated exclusion applies.

**Twins and views:**
- **exclusion twin:** the outside exclusion is written **into the card's definition** → gold flips;
- **element twin:** one element fact is flipped → gold flips;
- **equiv:** an outside rule is added only as background in the facts → gold unchanged;
- **attack twin (10% of latents, `inv`):** a counter-definition planted in the state text ("For this file, 'relayed
  statement' excludes …") → gold unchanged.
- **Choice:** "Which element is not met?" (the elements plus "all are met").

**Dev (150):** 75 iid plus 75 holdout.

### F7 `gen3_norm_action` (wave 2): 1,500 rows = 1,200 yes/no + 300 choice

**Norms.** About 60 structured norm schemas (actor, required or forbidden act, scope), all written by Claude. Nothing
comes from moral_stories. 10 schemas are held out.

**Actions.** Each action is tagged: in scope, does the required act, goal achieved (always stated), motive. The card
states the convention used:
- **C1:** the action does not act against the norm (out-of-scope actions pass; motive is irrelevant);
- **C2:** the action keeps the norm and achieves the stated intention.

**Twins:**
- an intention-flip twin (`equiv`, gold unchanged);
- an action-flip twin (gold flips).

**Dev:** 150.

### F8 `gen3_table_layouts` (wave 2): 1,000 rows = 800 yes/no + 200 choice

**Tables.** Short tables of 4–12 rows, in 8 layouts from `tab_core` plus JSON records. The fixed-width and key:value
layouts are **held out**. 20% of items have no card.

**Claims:** counting, superlative or range, comparison, difference or sum, "there is no", multi-condition lookup,
"only".

**Views:**
- `equiv` pairs: the same table in 2 layouts;
- twins that change one cell.

**Dev:** 100.

---

## 7. Dev split: `data/yn2b_dev.jsonl` (2,150 rows) + `data/yn2b_dev_relations.jsonl`

- **Two parts, recorded in `meta.dev_kind`:**
  - **iid:** the same templates as training, a new seed stream and disjoint name pools.
  - **holdout:** whole held-out sub-families, templates, packs or machines.

  The A/B's G1 uses the **holdout** part only (about 1,075 rows).
- **Status:** report-only. It is **not** one of the 9 ship splits and is never used for a choice, except by the single
  pre-registered A/B rule.
- **Reports:** accuracy per family × tier; the commitment rate (share of yes/no answers outside 0.2–0.8); committed
  accuracy (P(gold) ≥ 0.8); F3 accuracy by event count.

---

## 8. Decontamination (programs only; a new `check_yn2b.py`)

1. **12-word runs** (`build_v13_breadth.grams`) of every new state, instruction and option are checked against:
   - `held_out_grams()`: OHS-1/2/3 states, eval, eval_card, eval_jagged, eval_opi, eval_long, eval_multi, and
     `bench/jevbench/datasets/public`;
   - extended to OHS-1/2/3 instructions and options;
   - `bench/jevbench_v154/datasets/public/*.jsonl`, every string.

   A hit drops the whole latent unit. **OHS-3 is held in memory only.** The program prints hit counts and our own row
   ids, never OHS-3 text.
2. **12-word runs against every dev and eval split:** dev, devzs, devzs2, devp_card, pg_dev, debate_dev, dev_nc,
   taskbank_dev, hard_dev, dev_negwords, dev_claims, hard12_dev, proc12_dev, planted12_dev, golden_dev, breadth_dev.
   This is stricter than today's exact-state `dev_exact`.
3. **Instruction templates (all families):**
   - no 6-word run shared with the dialogue_rebuttal templates, any dev_negwords or dev_claims instruction, or the v11
     train templates;
   - the banned-cue list of F4 applies to F4, and to F2's output and judge views;
   - the cue-share rule (at most 60%) applies to every family.
4. **Unseen set with the new file.** A new `yn2b/check_unseen.py` calls
   `gate_dev.derive_unseen(SPLITS, list(gate_dev.TRAIN_FILES) + ["v14_parts/yn2b_train"])`. It asserts:
   - the unseen rows per source equal `UNSEEN_FROZEN_ROWS` (17 sources, 3,847 rows);
   - `overlap.flagged == {}`.

   The new source keys (`gd_gen3_*`) must match no dev source under the name rule. It never writes
   `ship_unseen_sources.json`.
5. **Exact dedupe** (normalised state + instruction) against golden_train and within yn2b. F4 (a) rows share a state
   with their base row by design; their deduplication runs on state + instruction.
6. **Dev vs train inside yn2b.** Holdout dev states may share at most 20% of their 12-grams with any train state
   (clause boilerplate included). No iid dev state may equal a train state.
7. **Names.** No organisation or person name in our pools appears as a substring of any JevBench public string, or of
   OHS-1/2 text. OHS-3 is checked by hash comparison only.
8. **Disclosure.** The families were designed from OHS-1/OHS-2 error patterns, dev diagnostics (both halves) and the
   JevBench v1.5 method text. No item text was copied. OHS-1/2 gains are therefore not claimed as held-out evidence.

---

## 9. Label verification

1. **Two independent programs.** `decide` works on the latent facts. `decide2` works on the parse-back of the rendered
   text, and **a different agent writes it**, without reading `decide`:
   - Agent B writes F3's decide2;
   - Agent C writes F2's decide2;
   - Agent D writes F5's decide2;
   - Agent E writes F1's decide2;
   - Agent A writes F6's decide2;
   - Agent C writes F4's decide2;
   - for wave 2, the agent that did not write F7 or F8 writes its decide2.

   They must agree on 100% of kept rows. If more than 1% of generated items disagree, stop and fix the generator.
   Never just filter.
2. **Grounding.** Every decisive fact in the trace appears verbatim in the rendered text.
3. **Structure checks:**
   - every contrast twin flips gold under both programs;
   - equiv views keep gold;
   - complement views invert it;
   - attack twins keep it;
   - items with two independent sufficient reasons are rejected, except the declared 2-violation F2 items, which get no
     twins.
4. **Artefact probes:**
   - a TF-IDF 1–2-gram logistic regression trained on train rows scores at most 60% on the family's dev from state +
     question, and at most 55% from the question alone;
   - |corr(gold, length / format / position / tier / polarity)| < 0.05;
   - no shortcut is above 60% on the family.
5. **Adversarial review.**
   - **(a)** The builder reads 30 random rows and 5 full twin sets per family.
   - **(b)** A fresh reviewer agent (no generator code, no gold) **blind-solves 100 rows per family**. Every
     disagreement is traced: a generator bug means fix, regenerate and re-run every gate; a reviewer error is logged.
     **Pass:** 0 open generator bugs, and at least 97% agreement after tracing.
   - **(c)** The reviewer runs an ambiguity hunt on 30 hard items per family: is there a reasonable reading under
     which the gold is wrong? Any ambiguity found means a template fix.
   - **(d)** Optional: the owner spot-checks 40 rows (5 per family) on an audit page.

   The review is verification only. Labels stay program-made.
6. **Existing generators.** Before D1, run the FINETUNE_PLAN §3.4 audit on 30 teacher-vs-gold disagreements each for
   gd_gen_numeric_dates, gd_gen_evidence_conflict and gd_gen_tables. A 28–41% disagreement rate may hide generator
   bugs. If 15 or more of 30 are wrong, apply the §3.4 action rule.

All results go to `logs/yn2b_checks.json`, plus a `yn2b_summary.json` with the counts, shares and sha256 of every
output.

---

## 10. How the rows enter the 2B

**Code, all new files.**
- Generators: `golden_src/gen3/` (mv_core.py, gen3_*.py, v3_*.py for decide2).
- Raw rows: `data/yn2b_parts/raw/gen3_<name>.jsonl`, `data/yn2b_parts/defs/`, `data/yn2b_parts/dev_raw/`. These are
  never read by `build_v14_golden.py` and never uploaded.

**Assembly** (`assemble_yn2b.py`, new):
- It reuses `build_v13_breadth.card` and the id and cid helpers.
- Ids are `r_yn2b_<key>_<k>`; `group_id` is `g:yn2b:<key>:<latent_id>`; `call_id` is `cid(group_id)`. F4 (a) rows take
  their base row's `group_id` and `call_id`.
- `source` is `gd_<key>`; `track` "GD"; `split` "train".
- Roles are aff / neg / dneg / para / choice / attacked (the trainer ignores `role`).
- Outputs: `data/v14_parts/yn2b_train.jsonl`, `data/v14_parts/yn2b_relations.jsonl`, `data/yn2b_dev.jsonl`,
  `data/yn2b_dev_relations.jsonl`.

**Merge** (`merge_yn2b.py`, new; it runs after `build_2b_kd.py`, which is unchanged).
- It writes **new** files:
  - `data/v14_parts/train_2b_golden_kd_yn2b.jsonl` (the build_2b_kd output + yn2b_train);
  - `data/v14_parts/golden_relations_yn2b.jsonl` (golden_relations + yn2b_relations).
- It asserts: no id collisions; `train_decoder.check_rows(rows, kd=0.5)` passes; no yn2b row has `meta.teacher`; the kd
  count equals build_2b_kd's print. The inputs are never overwritten.

**Targets.** New rows carry **no `meta.teacher`** → gold smoothed to 0.95 / 0.05.
- `kd_skip_src` stays `["blend50"]`. Adding names there does nothing (fact 1).
- `kd_full_src` stays `["gd_gen2_probability"]`, and `expect_kd_full` stays 238.
- `expect_kd_targets` equals build_2b_kd's print, or teacher_gate's print if D1 is adopted.

**Weights:** uniform; one pass, every row once. There is no up-weighting or curriculum (rejected in FINETUNE_PLAN §7).

**Config changes** (later, in the 2B worktree, after the amendment is committed; never in the frozen 4B worktree):
```
runs/q35_2b_main.json:
  "train_file": "v14_parts/train_2b_golden_kd_yn2b.jsonl",
  "rel_file":   "v14_parts/golden_relations_yn2b.jsonl",
  "epochs":     FILL from `replay_steps.py --config runs/q35_2b_main.json` (about 31.7K steps expected),
  "expect_kd_targets": FILL (unchanged by yn2b)
modal_od.V14_KEEP += {"train_2b_golden_kd_yn2b.jsonl", "golden_relations_yn2b.jsonl"}
```
- `yn2b_dev.jsonl` is top-level and uploads automatically.
- On the L4, copy the two files to `~/lean/data/v14_parts/`.
- Re-run the 2B smoke (the trainable count and the heaviest micro-batches).
- Record C2's snapshot steps (0.85 / 0.90 / 0.95 × the replayed steps) in the amendment.

**Compute:** +4.2% steps and about +5–7% tokens: about +$3 on the H100, or about +5 L4-hours.

---

## 11. Owner decisions

**D1: teacher gate on exact-label generator rows (Option B). Default: OFF, the tested setting.**
- A new `teacher_gate_2b.py` runs on build_2b_kd's output. It covers rows with `teacher_src == "q35_4b_E"` (fresh reads
  only) and source in the gd_gen_* sources, gd_gen2_json_fields, gd_gen2_long_policy and gd_gen2_tool_selection, plus
  gd_gen2_probability for choice rows only.
- **Rule:** if `build_2b_kd.gives_gold(row, teacher)` is false, delete `meta.teacher` and `teacher_src`, and keep
  `teacher4b` for audit.
- **Consistency:**
  - complement pairs stay consistent, because a symmetrised wrong teacher is wrong on both sides;
  - attacked twins already copy the teacher only when it gives the gold answer.
- **Effect** on the out-of-sample generator yes/no rows measured today: targets inside 0.2–0.8 fall from 35.8% to
  13.7%.
- **Against:** it is untested, and X16 (sharpening everywhere) lost −1.29 pp. It is decided by arm C (section 12)
  plus the owner's approval.

**D2: PRISM-X I override for the 2B.** It is required because the config has `prism_x "I"` and PREREG_FINAL §1 says it
is not adopted without an override. Draft text is in section 13, A2.

**GO:** the A/B and the 2B main run use Modal or L4 money, so they need the owner's GO.

---

## 12. The A/B test (pre-registered; the cheapest valid design)

**Question.** Do the new rows teach generalisable skills, and cause no regression, when added to the 2B recipe?

**Design:** 2 arms from base Qwen3.5-2B. The recipe is identical to `q35_2b_main.json`: PRISM-X I, layout E, kd 0.5,
aux_norm micro, seed 20260925. The arms differ **only** in the training file.

**The control subsample S:**
- `build_ab_yn2b.py` (new) takes the call_id units of `train_2b_golden_kd.jsonl` with
  `int(sha256("yn2b-ab:" + call_id), 16) % 4 == 0`.
- That is about 25%, about 125.4K rows, stratified by construction.
- Relations are filtered to rows present.

**Arms:**

| Arm | Train file | Rows | epochs | Steps |
|---|---|---|---|---|
| A (control) | `ab_A_train.jsonl` = S | about 125.4K | 0.4 | about 3,136 |
| B (yn2b) | `ab_B_train.jsonl` = S + all yn2b rows that passed their gates (wave 1 + any wave 2 ready) | about 146.4K | 0.4 | about 3,661 |
| C (optional, D1) | `ab_C_train.jsonl` = B with teacher_gate applied to S | about 146.4K | 0.4 | about 3,661 |

- The **same epochs fraction** means B and C see the same expected number of golden rows as A, plus the new rows. This
  mirrors the production change, where the rows are added on top.
- The new-row dose is about 3.6× production (14% vs 4%). It is a **stress test**: passing the no-regression rules at
  3.6× implies safety at 1×, and in-family learning is visible.

**Runs:**
- Configs: `runs/q35_2b_ab_{A,B,C}.json`.
- All arms run on **one GPU type** (H100, one arm per Modal account in parallel), or all on the L4 in sequence. Never
  mix: the E-on-H100 vs E_L4 comparison was confounded.
- One code commit. `expect_kd_targets` comes from the builder's print.
- The arm files are added to V14_KEEP only on the A/B branch.

**Reads.**
- One job on the L4: `od_gcp.py predict`, the pinned 2B base revision, layout taken from `train_meta`.
- Splits: the 9 gate splits, eval_jagged, eval_opi, eval_redef, yn2b_dev.
- Plus a `_perm` read (`--perm-seed 1`) on the 9 splits.

**Readout.**
- A new `yn2b/ab_readout.py` imports gate_dev's functions: `load_rows`, `group_boot` (group_id units, 10,000
  resamples, seed 0), the tb_mixtral-free full set, `crossfit` (the Brier score), `relation_flips`, `perm_flips` and
  `asr_compare`.
- It writes `logs/yn2b_ab.json` and appends one line to `logs/yn2b_ab_looks.jsonl`.
- It is **not** a ship look and does not touch `logs/ship_looks.jsonl`.
- **One A/B, one verdict. No re-runs with other seeds.**

**Cost:**

| Item | Cost |
|---|---|
| H100, 1.6–1.9 s/step | A about $6–7, B about $7–8, C about $7–8 |
| Reads, about 2.5–3 L4-hours per arm | about $7–9 |
| **Total** | **about $20–25** for A+B, about $30 with C |
| L4-only fallback | about 10–12 h per arm |

### Pass rule for B (all must hold; B minus A)

**G1: held-out generalisation**
- On the yn2b_dev **holdout** rows: accuracy ≥ +5.0 pp, and the 95% lower bound (LB) > 0.
- On the holdout yes/no rows, committed accuracy (P(gold) ≥ 0.8) ≥ +5.0 pp.
- **Family drop rule:** any wave-1 family whose holdout difference is below 0 is **dropped** from the final add. This
  moves the file towards A, so no re-run is needed.

**G2: external transfer**
- On the pooled dev_negwords + pg_dev + hard_dev rows (2,057), the point difference is ≥ +0.5 pp.
- None of these sets is built by our generators: the dialogue frames are held out, `pg/` is never imported, and
  hard_dev is Claude-written.

**No regression** (all computed on the full set without tb_mixtral, as in the ship rule):

| | Constraint | Must hold |
|---|---|---|
| NR1 | Full set (7,056 rows) | point ≥ −0.3 pp, and LB > −1.0 pp |
| NR2 | **Multiple choice** (3,189) | point ≥ −1.0 pp |
| | Yes/no (3,867) | point ≥ −0.5 pp |
| NR3 | Primary unseen-source set (3,847) | point ≥ −0.5 pp |
| NR4 | Calibrated yes/no Brier (d) | ≤ +0.005 |
| | Equivalence flips (e) | ≤ +2 pp |
| | Permutation flips (f) | ≤ +2 pp |
| NR5 | Jagged ASR and OPI ASR | each ≤ A + 1.0 pp (point) |
| | eval_redef accuracy | ≥ A − 2.0 pp |
| NR6 | Human-labelled splits (dev, devzs, dev_nc, devp_card, dev_claims) | no point drop > 2.0 pp on any of them |

**Verdict:**
- **PASS** (G1, G2 and NR1–NR6 all hold) → the 2B main run uses `train_2b_golden_kd_yn2b.jsonl`, without any family
  dropped by G1.
- **FAIL** → the 2B main run uses `train_2b_golden_kd.jsonl`, the plan of record. The numbers go into the ledger and the
  amendment. A redesigned set needs a new pre-registered A/B.

### Arm C rule (D1)
Adopt Option B only if **all** of these hold, and the owner approves:
- C passes NR1–NR6 against A;
- (C − B) full-set point ≥ 0.0;
- (C − B) committed yes/no accuracy on the 9 splits ≥ +1.0 pp;
- (C − B) Brier (d) ≤ +0.002.

Otherwise the tested kd setting stays.

### What the A/B cannot show
- Two 2B arms give bootstrap half-widths of about ±1.0–1.3 pp on the full set (PREREG §3.5).
- So the A/B rejects clear harm (1 pp or more) and confirms held-out in-family learning. It cannot certify effects
  below 1 pp.
- The final ship rule against v11r stays the decisive test.
- The gains on the new JevBench families are inferred from G1 only; no local v1.5 items exist.

---

## 13. Amendment texts (commit before 2B step 0; fill the `<…>` values from the build and A/B logs)

### A1: appended to PREREG_FINAL.md

> **Amendment A1 (<date>): new program-labelled rows in the 2B training file (yn2b).**
>
> 1. **Change.**
>    - The final 2B trains on `v14_parts/train_2b_golden_kd_yn2b.jsonl`: build_2b_kd's output plus `<N>` rows from 8
>      (or `<k>`) new generators, `gd_gen3_*`, listed in `yn2b/SPEC_draft.md` §4.
>    - Counts per family: `<table>`. Generator sha256 values: `golden_src/gen3/MANIFEST_yn2b.jsonl` (`<sha>`).
>    - Relations: `v14_parts/golden_relations_yn2b.jsonl`.
>    - §10.10's "frozen at 501,732 rows" no longer holds for the 2B: its file has `<N_total>` rows. golden_train itself
>      is unchanged, and so is the 4B.
> 2. **Labels.**
>    - Every new label is computed by a deterministic program and checked by an independent second program on the
>      rendered text (100% agreement), with a blind review of 100 rows per family.
>    - No model labelled any row.
>    - New rows carry no teacher and train on gold smoothed to 0.95/0.05. kd, kd_skip_src, kd_full_src and
>      expect_kd_full are unchanged; expect_kd_targets = `<n>`.
> 3. **Design provenance (disclosure).**
>    - The families were chosen from OHS-1 and OHS-2 error analyses (already-used sets; no text copied), from dev
>      diagnostics on both halves (dev_negwords, pg_dev, hard_dev, long yes/no), and from the JevBench v1.5 method text
>      (no item text; the new v1.5 items are not in our copy).
>    - No OHS-3 or JevBench half-B information was used.
>    - dev_negwords' held-out frame family (dialogue_rebuttal) remains out of training (6-gram and cue checks:
>      `<result>`).
> 4. **Decontamination:**
>    - 12-word-run check against OHS-1/2/3 (OHS-3 read by program only; counts printed), eval*, both JevBench public
>      copies and all dev splits: `<hits dropped>`;
>    - `yn2b/check_unseen.py`: unseen-source set unchanged (17 sources, 3,847 rows), text guard 0 flags with the new
>      file included.
>
>    The registered ship run still re-derives the set from the 12 registered files.
> 5. **A/B evidence.**
>    - Arms A and B (and C, if run) per SPEC §12, pre-registered in this amendment's first commit `<sha>` before any
>      A/B training.
>    - Result: `<G1, G2, NR1–NR6 numbers>` → `<PASS/FAIL>`. Families dropped by the G1 rule: `<none/list>`.
>    - The A/B used dev splits for one data choice; this adds a small selection bias to the later ship look, which we
>      accept and disclose.
> 6. **Schedule.** Replayed 2B steps: `<S>`. C2 snapshots: `<s085>`, `<s090>`, `<s095>`.
> 7. **yn2b_dev.** It is report-only: never a ship split, never used for selection beyond rule 5.
> 8. **Teacher gate (D1):** `<not adopted | adopted under the arm-C rule, owner approval <date>>`.
> 9. **Unchanged:** REF (v11r), the ship rule, the ASR caps, the held-out discipline (§8), no JevBench submission,
>    and OHS-3 once, blind.

### A2: appended to PREREG_FINAL.md (owner override, D2)

> **Amendment A2 (<date>): PRISM-X arm I adopted for the final 2B (owner override for security).**
> - The pre-registered accuracy margin for I vs E_L4 failed (−0.27 pp [−1.34, +0.79]).
> - The owner adopts arm I because layout E at 1,600 steps would be vetoed on jagged ASR: 10.0% vs a cap of 6.9%, an
>   increase of +6.1 pp [+2.8, +9.6], against 1.1% for I_1600.
> - The 2B ship rule, REF (v11r) and caps are unchanged. The 2B must still pass them.
> - Latency is reported with PRISM-X on.
> - 2B base revision for scoring: `<hash>`.

### Addendum to FINETUNE_PLAN.md
> **Addendum (<date>), 2B data:**
> - §3.3 now ends with `merge_yn2b.py`, which writes `train_2b_golden_kd_yn2b.jsonl` and
>   `golden_relations_yn2b.jsonl`.
> - §3.5: train_file, rel_file and epochs as in SPEC §10.
> - §6: +$20–30 for the A/B and about +$3 for the 2B pass.
> - §7's "20K-row A/B pilot: not resolvable" is superseded for this decision only, by the owner's must-haves: the A/B
>   here is a stress-dose, 2-arm test with non-inferiority margins and a held-out generalisation bar. It resolves
>   ≥ 1 pp harm and in-family generalisation, not sub-1-pp effects.
> - Up-weighting, curricula and teacher sharpening remain rejected.

---

## 14. Build plan (who, what, order, time)

**Agents.** 5 Claude builder agents plus 1 fresh reviewer. CPU only. Everything is written to new files.

| Day | Agent A (core) | Agent B | Agent C | Agent D | Agent E |
|---|---|---|---|---|---|
| D0 (30 Sep), first half | mv_core API + formats + views; F4 frames + quads; `check_yn2b.py` skeleton | F2 atoms + evaluator | F3 machines + simulator | F1 clause engine (+ gen2_long_policy import) | F5 scorer; `assemble_yn2b.py`, `merge_yn2b.py`, `build_ab_yn2b.py`, `check_unseen.py`, `ab_readout.py` |
| D0, second half – D1 | F4 rows (a) + (b); F6 decide2 | F2 renderers, views, shortcuts; F3's decide2 | F3 renderers and views; F2's decide2 | F1a + F1b rows; F5's decide2; then F6 | F5 rows; F1's decide2; teacher_gate_2b.py |
| D1.5 | Run all gates (section 8, 9.1–9.4); assemble; dev | fixes | fixes | fixes | merge dry run on a dummy KD file; `check_rows`; replay_steps on the arm configs |
| D1.5–D2 | **Reviewer R:** blind solve of 100 rows per family plus the ambiguity hunt; builders fix and re-gate | | | | Wave 2 (F7, F8), only if wave 1 is green |
| D2 | Owner: D1, D2, GO; commit A1 (design and A/B rule sections) **before** the A/B trains | | | | |
| D2–D3 | A/B: arms train (H100 about 2 h in parallel, or L4 about 1 day) → reads (6–9 L4-hours) → `ab_readout.py` verdict | | | | |
| D3 | Fill A1 with results → commit → build the final 2B file (or keep plan of record) → 2B smoke → **2B main** | | | | |

**Critical path to 2B step 0.** It is the latest of:
1. the 4B-E labels are complete (shards 10–19 are on disk; 211,020 rows);
2. `build_2b_kd.py` and the §3.4 audit;
3. the yn2b A/B verdict (about D3).

The 4B main run does not block the 2B, because the teacher is 4B-E (PREREG §6).

### Where each piece is used

| Piece | Built | Used in |
|---|---|---|
| Generators + gates + yn2b_dev | Now (CPU, during the 4B run) | 2B data build |
| check_unseen, decontamination | Now | the A1 amendment; the ship-rule integrity of the 2B |
| §3.4 audit + teacher_gate (D1) | Now / after the labels | build_2b_kd output → arm C → 2B file (if adopted) |
| A/B arms + ab_readout | After labels + gates, before 2B | decides whether yn2b enters the 2B main run |
| Merged 2B file + config fills + amendments | After the A/B | 2B main training |
| yn2b_dev report, commitment rates | After the 2B | serving calibration (per-type T, FINETUNE_PLAN §5.1), JevBench half-A report |
| Ship look vs v11r | After the 2B | ship decision (PREREG §3–5) |
| OHS-3 once, blind | Last | final claim vs Jev |

---

## 15. Optional later: the 4B variant (owner must-have #4)

This is not on the 2B's path.
- **What:** "4B_main + yn2b", a short continued fine-tune from the new 4B adapter.
  - About 2,000 steps.
  - yn2b_train plus at least 75% replay from golden_train. A18 showed forgetting at about 48% replay.
  - Gold targets only.
- **When it can be used:** only if it passes the same ship rule against 4B_main. The clean 500K 4B stays the headline.
- **Cost:** about $8–10 on the H100, plus reads.
- It never changes the 2B's teacher (4B-E, PREREG §6).

---

## 16. Risks and limits

- **Gains may stay in-family** (A18, G2). This is controlled by G1 (holdout families only) and G2 (external probes).
  The realistic dev-gate effect for the full 2B is +0.3 to +1.0 pp. The main payoff is confident yes/no answers on
  JevBench v1.5 guardrail, state and score items, and fewer self-contradictions.
- **Security.** The tool, injection and definition rows could shift the attack success rates. This is controlled by
  the authority rule, F6's definitions-in-card rule, the attack twins, and NR5 (tighter than the ship veto).
- **Label bugs.** Controlled by two programs written by different agents, parse-back, grounding, a blind solve and an
  ambiguity hunt.
- **Leakage into held-out splits.** Controlled by the 12-gram checks, the template, cue and dialogue bans, and
  check_unseen.
- **Time.** If wave 1 is not green by D2, the A/B runs with the families that passed, in priority order. The 2B never
  trains on a family that skipped a gate or the A/B.
- **Unmeasurable.** Gains on the new JevBench families cannot be measured locally. The 2B pilot's commitment numbers
  (for example 30 of 38 hard yes/no items abstained) come from a 1,600-step model.
