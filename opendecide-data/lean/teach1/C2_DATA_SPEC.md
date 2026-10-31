# C2_DATA_SPEC: the final fine-tune of C1 into C2 (merged plan v1, 13 Oct 2026)

**What this is.** One plan, merged by the chief scientist from three independent designs: (D1) data quality first,
(D2) transfer first, (D3) product and agent first. Ideas are kept when at least two designs support them or when the
evidence clearly favours them. Every conflict is resolved and recorded in Appendix A, and every refuted claim is listed
in Appendix B.

**Status at writing.** This is a design only. Nothing was launched. A `ps` check on 13 Oct found no local Modal,
Python, SGLang, gcloud or training process running. No paid or remote compute and no Jev call were used, and no
OHS, sealed, DI, JevBench or ejs-5 content was opened.

**Inputs read.**
- `teach1/task_ranking.json`: 39 ranked families.
- `c_spec/C_DATA_SPEC.md` v4, `BUILDER_BRIEF.md`, `C_TRAIN_RECIPE.md` v4, and `LICENCE_REGISTER.md` (skimmed).
- The F1, F2, F3, F9 and F12 `G0_SPEC.md` files (grep checks) and every family's `qc/QC_REPORT.json` pass flag.
- `c_build/` headers: `mixer.py`, `crowd_select.py`, `decontam_g13.py`, `decontam_g13_batch.py`, `replay_sample.py`.
- Round-1 logs: `CANDIDATE_R1.json`, `gate_c_6.3_q35_4b_c_r1.json`, `snap_monitor.jsonl`, `r1_check_proj.json`.
- `reports/ROUND1_RESULTS.md`, `teach0/REPORT.md`, `HANDOFF.md`, and PREREG amendments A22-A36.

**Binding rules carried over unchanged.**
- A program computes every gold, and an independent solver B must agree on 100% of rows.
- No model sets a label.
- One pre-registered candidate and one sealed look.
- No Jev output is used as an input.
- Nothing is tuned on or designed toward OHS-1/2/3, DI, ejs-5, JevBench or the A15 sealed suite.
- Free Modal credit is used first, and every GPU step needs the owner's GO.

---

## 1. Goal and honest expected gains

### 1.1 Owner goal
Fine-tune C1 (`q35_4b_main500k`, adapter sha 507d1c29...) once more, into C2. The training data should be the
highest-quality, out-of-the-box, everyday and AI-agent decision tasks. Haiku 5.5 is the cheap **author** of wording
and scenarios, and **programs** compute the gold.

The targets, against Jev:
- general accuracy: close to Jev;
- rule and agent decisions, consistency, calibration, speed, cost and security: better than Jev.

Training budget: about $20-40 of free Modal credit, with the owner's GO before any GPU use. The speed work is done:
SGLang S1 was adopted under A35.

### 1.2 What the evidence says

| Fact | Value | Source | Meaning for C2 |
|---|---|---|---|
| Round 1 (F3, F5, F7; about 10.7K new + 16.1K replay = 26,785 rows; 1,650 steps at 5e-5; $8.4) | Sealed select +0.90 pp [−0.16, +1.96]; confirm +0.11 [−0.69, +0.96] | `ROUND1_RESULTS.md` | Synthetic rule data barely moves general real-text accuracy |
| Round-1 dev guards | D1 −0.38 [−1.06, +0.30]; D2 −0.42; D3 −0.31 / −0.47; D4 +0.0018; equivalence flips 7.89% vs 8.86% | `gate_c_6.3` artifact | 60% replay plus the C1 anchor held retention; the dev cost was small and not significant |
| Round-1 old slice | −1.85 / −1.40 / −1.25 pp at 25 / 50 / 75%; P(yes) drift ≤ 0.013 | `snap_monitor.jsonl` | The stop rule (−1.5 at both 25% and 50%) was missed by only 0.10 pp at 50%. The dip was largest early and shrank as LR decayed |
| Round-1 speed | 3.716 s/step at steps 100-300; about 16.2 rows/step; $0.31 per 1K rows all-in | `r1_check_proj.json`, HANDOFF | The cost model for C2 (section 9) |
| OHS-3, C1 vs Jev | Accuracy 74.3 vs 79.6; Brier 0.172 vs 0.150; complement violation 0.170 vs 0.088; option drift 0.023 vs 0.041 | `ROUND1_RESULTS.md` | General gap about 5 pp; consistency and calibration gaps on real text. OHS-3 is spent |
| TEACH-0 public subset (n = 1,722) | Haiku 80.8 / Jev 79.0 / C1 78.6 | `teach0/REPORT.md` | Haiku is not a strong general labeller (A36 MARGINAL), so it never labels |
| TEACH-0 authored splits (hard_dev 72 + pg_dev 206 = 278) | Haiku 98.9 / Jev 71.6 / C1 73.0 | same | Rule items are determinate for a Claude-family reader, and C1 ≈ Jev there. But n is small and A36 says these splits may be LLM-authored. **This is not proof that a 4B can learn them** |
| C1 already trained on the `pg_*` (2,688 rows) and `hard_*` (3,875 rows) train splits, plus about 100K `gd_gen_*` program rows | Still only 72.8 on pg_dev and 73.6 on hard_dev | LICENCE_REGISTER §4; TEACH-0 | The one-pass readout has a ceiling on deep procedural items, so C2 caps depth and prints intermediate values |
| F2 / competitor evidence | Rule paragraphs 0.24 vs 0.67 for one sentence | spec F2 | At most 2 unstated operations per row |
| SPEED-2 (dev) | S1 SGLang: server p95 98 ms at c = 1; $0.079 per 1K at 40% use vs Jev $0.061 | HANDOFF, A35 | Speed is solved. There is no cost-win claim at 40% use (S1 is cheaper only above about 55%) |

### 1.3 What C2 aims for, with honest expectations
C2 aims at what it can measurably win:
- rule and agent decisions;
- consistency (complement and minimal-edit);
- calibration on those decisions;
- security without over-refusal.

On general real text it only has to show **no harm**.

| Measure (fresh sealed OHS-4) | C2 − C1, expected | Comment |
|---|---|---|
| Mixdev, in-family (held-out samplers, packs and registers) | +10 to +20 pp | Learning check, not a claim |
| OHS-4 R: rule/agent items from independent generators | +4 to +10 pp (central ≈ +6) | The headline claim. Part of the in-family gain is lost to new authors and formats |
| OHS-4 U: unseen task kinds | 0 to +4 pp | Report-only transfer |
| OHS-4 G: general real text | −1.0 to +0.5 pp (central ≈ −0.3) | Round 1: dev −0.38, sealed +0.9. C2 does not promise a gain |
| Complement violation, R items | −0.03 to −0.08 | Overlay pairs in every family |
| Complement violation, G items | 0 to −0.03 | T37b real-text complements. **Reaching Jev's 0.088 is not expected** |
| Yes/no Brier | Better on R; about equal on G | Hard labels, temperature refit on mixdev |
| Security attack success | About equal to C1 (0-1.3% on dev) | Gated as no-harm |
| Latency and cost | Same as C1 on S1 | Same architecture; merged r16 |

**Against Jev** (report-only, read once after the C2 verdict):
- **General:** the gap of about 5 pp is expected to persist, so "close to Jev on general" is not expected to be
  claimable.
- **Rule/agent:** a win is plausible, because C1 ≈ Jev on rule items and C2 adds 4-10 pp.
- **Consistency and calibration:** a win is plausible on R items, but not on G items.
- **Speed:** p50/p95 claims follow SPEED-3 rules.
- **Cost:** there is no win at 40% use.

**Odds (rough, stated now):**
- P(dev pre-gate passes) ≈ 0.55-0.65.
- P(all OHS-4 ship rules pass | pre-gate passed) ≈ 0.45-0.55.
- **P(C2 ships) ≈ 0.25-0.35.**
- The largest single risk is the one-pass readout ceiling on rule items (1.2, row 7).

---

## 2. Selected families

### 2.1 Trained families (17 program families + the T37b block + carry-over pools)
Notes on the table:
- Rows are selected rows after the crowd step. Generate about 1.5× as many.
- "W" is the build wave (section 6.4).
- Every family uses solver A for gold, solver B of a different paradigm (G2 at 100%), G3 round-trip, at least 3 G4
  relations, and the G5-H blind read (section 6).

| ID | Name | Rows | W | Gold (solver A) | Verifier (solver B + extra checks) | Haiku role | Novelty vs existing builders |
|---|---|---|---|---|---|---|---|
| T28 | Permission verdicts from precedence rules (allow / ask / deny) | 2,400 | 1 | Glob-AST matcher + stated precedence | Regex compile + brute-force match table + precedence by a different sort key; precedence paraphrases admitted only by 3/3 extraction | Tool/org packs, policy surfaces with slots, precedence and question paraphrases, admin memos | F12 has only POL-ROLE role lists and CALL/ASK/UNABLE/ANSWER. F1 has precedence over case attributes. Neither has effect tiers, argument globs or precedence between call rules, and **neither was ever trained** (QC fail) |
| T35 | Path-rule access, robots-style (RFC 9309 rules stated on the card) | 600 | 1 | Trie longest match (T28 plugin) | Brute-force regex with explicit length comparison; `urllib.robotparser` is never a verifier | Site and crawler narratives only | Not in any builder |
| T33 | Outcome verification: step criteria and claims vs tool logs | 2,400 | 1 | Simulator ground truth | Re-parse the rendered log into sqlite; independent unit table; claim-to-field matcher; G3-H claim extraction | Agent final messages with claim slots; mock-API packs; criterion paraphrases | F9 extracts and aggregates; F3 tracks records. Neither judges claims or uses 202 / idempotency semantics |
| T29 | Confirmation gates before acting (proceed / confirm / refuse / cannot decide) | 2,000 | 1 | Rule evaluator | sqlite over the parsed snapshot; 3-valued enumeration over missing fields | Action catalogs, snapshot fields, a closed confirmation-phrase bank, pressure lines | F12 has single-field preconditions only. No builder has reversibility, blast radius or a confirmation tier (0 grep hits) |
| T30 | Clarify or proceed: distinct candidates after deduplication | 1,400 | 1 | Deduplicate on the stated key + consequence table | SQL GROUP BY on the parsed records + independent consequence lookup | Request phrasings, listings, name seed pools | F12 SEM-08 covers one narrow case; F6 points the opposite way (missing premise) |
| T27 | Embedded request that widens the user's scope | 1,600 | 1 | Action class × scope table (generator metadata) | Independent verb-lexicon-to-class table + scope table; 2/2 Haiku class extractions | Carrier pages, emails and tool outputs with `{ACTION}` and `{JUSTIFICATION}` slots; justification bank | planted_* and binj_* were dropped from replay. Nothing asks for a scope decision with in-scope controls |
| T26 | Legitimate vs fake authority by stated provenance checks | 1,400 | 1 | Checklist | Exact code-point compare + independent normaliser; pair checker (exactly one field differs) | One shared urgent-request skin per pair; context documents | No provenance checklist in any builder |
| T31 | Authority at time t: delegations, bands, revocations, sub-agent scopes | 1,000 | 2 | Precedence engine | UTC-epoch interval-table scan + set intersection | Memos, audit-log lines, grant documents | 0 G0 hits for delegation or revocation |
| T32 | Commitment ledger in chat | 800 | 2 | Event-sourced state machine | G3-H maps every message back to the event stream exactly, then an independent state machine | Renders each event as one casual chat message, with no status words | F3 tracks structured records only |
| T01 | Rolling windows and anchored deadlines (absorbs the T16 cutoff part and T02 rolling sums) | 1,600 | 1 | Day-ordinal interval arithmetic | Day-by-day bitmap; pandas rolling sum; integer-minute UTC | Trip diaries, insurer letters, ledgers, receipts; window-rule paraphrases (3/3 extraction) | F2 A20 says "rolling windows are never used"; F9 T16 has only an anchored filter |
| T23 | Governing version under transition clauses | 800 | 1 | Timeline resolver + transition rule | Evaluate every version + SQL window filter + separately coded transition rule | Policy pages, changelogs, emails | F1 S6 picks the dated version in force. There are 0 grandfather/transition hits, and F1 was never trained |
| T24 | Revision materiality: does the edit change this case's outcome? | 600 | 2 | outcome(V1) vs outcome(V2) | Second, independently written interpreter; cosmetic edits admitted only by AST equality | Cosmetic rewordings (AST-checked), documents | No builder asks for a V1-vs-V2 delta |
| T06 | Consumer return rights: non-waivable floor vs posted policy | 900 | 1 | Decision table on day ordinals | Independent day counter + separate exception evaluator | Store signs, receipts, chats; statute paraphrases | F1 handles precedence within one policy only |
| T15 | Eligibility gates and ordered claimant cascades | 900 | 2 | Ordered decision list | Decision-table enumeration | Fact sheets, HR notes, gate paraphrases | No builder has ordered gates with skips or tie-break cascades |
| T12 | Three-way match with ordered exception precedence | 800 | 2 | Decimal rule engine | Integer-cents join with an independently coded check order | ERP documents, vendor emails, AP notes | F9 joins two tables; F2 has tolerances; no builder has a three-document ordered first failure |
| T07 | Headline promise vs footnote qualifier | 800 | 2 | predicate(customer) | G3-H extracts (qualifier, bound) tuples, which must equal the spec; independent set-membership solver | Main free-form author (≤ 40% free-form) | Not in any builder |
| T25 | Source reliability conflict with tie-abstain | 600 | 2 | Resolver (tier > date > independence) | Sort-and-group implementation | Source excerpts with value and date slots | Replay already has `gd_gen_evidence_conflict` (11,536 rows). Only the independence and tie-abstain parts are new, so the family stays small |
| T37b | Real-text complements and paraphrases on replay yes/no rows | 2,000 | 1 | 1 − human gold (complement); same gold (equiv) | negcount polarity program + 2 Haiku polarity judgements + blind solver; binary-predicate sources only | Writes the complement or paraphrase question only | F5 is templated, and 91% of replay negation uses one template |
| F5 carry | Negation complement and equiv units (passed every round-1 gate; never in C1) | 1,500 | 1 | Existing | Existing gates + G13 against the new targets | none | Trained only in the unshipped round-1 candidate |
| F6 / F11 / F4 carry (conditional) | Abstain (F6), real-text codebook (F11, XED/MAMS), multi-hop (F4) | ≤ 1,000 / ≤ 1,000 / ≤ 500 | 2 | Existing | Only if each finishes its open steps by the cutoff (5.3) | none | QC passed; not in C1 |

**Totals at full build:**
- 20,600 program rows: the agent tier (T28, T35, T33, T29, T30, T27, T26, T31, T32) is 13,600 and the everyday tier
  is 7,000.
- Plus 2,000 T37b, plus at most 4,000 carry-over rows.
- **New rows ≤ 26,600 (40%); replay ≤ 39,900 (60%); total ≤ 66,500.**

### 2.2 Held out, never trained (transfer dev; built after the OHS-4 freeze)

| ID | Name | Items | Why held out |
|---|---|---|---|
| T36 | Dependency version-range satisfaction (npm semver, PEP 440; semantics stated) | 300 | All three designs: tests transfer of matching and precedence skills (T28, T35) |
| T19 | Compliance checklist with scope exclusions and evidence expiry | 300 | D2 and D3: tests transfer of ordered gates (T15), expiry (T23) and abstain (T25, T29) |
| T21 | Contract cross-references and carve-outs (synthetic contracts; no CUAD headings or text) | 300 | D1 held it out, D2 trained it, D3 dropped it. As a held-out family it adds a legal-style transfer test at no training cost |
| T20 | Incident severity with override precedence and timed escalation | 300 | D1 held it out, D3 trained it, D2 dropped it. Same compromise; it overlaps F7 and F11 |

Each transfer-dev family has its own plugin, its own Haiku registers (never used in training) and the same
verification stack.

### 2.3 Dropped
- **T05, label compliance (allergens, per-serving claims).** Dropped by D2 and D3. openFDA recalls is an OHS source, so
  allergen-recall text is OHS-adjacent, and the mapping from derived ingredients to allergens is world knowledge.
- **T16 as a separate family.** Folded into T01 S6. F2 already covers business-day counting.
- **T02.** Folded into T01 S4.
- **T09, T08, T13, T14, T11, T10, T04.** Arithmetic depth (the F2 one-pass evidence), overlap with F2, and low
  learnable gain.
- **T22 (CUAD / ContractNLI).** Both are on the LICENCE_REGISTER §5 deny-list (LegalBench / LexGLUE, OHS-1).
- **T03.** mod-97 cannot be checked in one pass, and the lures are unsafe.
- **T17, T39, T38.** Judge vetoes: tzdata or formula world knowledge; opinion-like soft gold.
- **T34, T18.** Niche and low transfer. No design both trained them and had a second design agree.

---

## 3. Per-family build notes

### 3.0 Rules for every C2 family (changes from spec 2.1 are marked C2)

**Cards, samplers and packs**
- **Card:** unchanged definition (family, sampler, domain pack, label schema, instruction family).
- **(C2) Cards per family:** at least max(20, rows/45). Rows per card ≤ 64 (D1 and D2; Super-NI plateau), median
  30-45.
- **Samplers:** at least 4 training samplers of different shapes (forward, label-first, config/table-first, narrative
  or transcript), plus a held-out **S5** that feeds only mixdev.
- **(C2) Packs:** a new Haiku-written shared pool of at least 200 packs (tool namespaces, org contexts, everyday
  settings), plus the existing round-1 G13-clean `c_src/packs`. Every family uses at least 25 packs, with one pack per
  card. O*NET persona seeds are reused as in spec 2.1.

**Registers, wordings and definitions**
- **(C2) Registers:** at least 8 per family (memo, chat, ticket, JSON/YAML config, email, log, FAQ, transcript…).
  At least 2 registers per family are held out for mixdev or transfer dev. Each register is ≤ 15% of new rows, and
  each skin feeds ≤ 6 rows.
- **Wordings:** at least 30 instruction wordings per family. Each is ≤ 2% of its family, and each card uses at least 5.
- **Definition styles:** as spec 2.1. A short or no card on about 15% of rows.

**Answer balance**
- Yes/no is 45-55% of each family where both forms exist (T35 is 70%).
- Gold yes is 50 ± 2 per family × wording × bin × negation count; per-card rates are drawn from 20-80%.
- "Yes = bad outcome" is 50 ± 5.
- Syntactic negation is on at least 10% of yes/no rows, and double negation on at least 2%.

**Options**
- **(C2) Option counts:** the family's natural sets, 2-9 options (3- or 4-way verdicts; "which rule decides" with 3-9
  rule ids plus "no rule, the default applies"; inverted cards with 3-5 calls or cases). F11 carry-over keeps the
  large-option skill. Spec 2.1's 20-60-option quota does not apply to C2 families.
- Inverted cards are 10-15% and few-shot cards 5-10%.
- Masked label names are on 10-15% of choice rows. Swapped names are used only where the card defines the label,
  on ≤ 5% of rows.
- The gold position is uniform per option bucket.
- Every wrong option is the output of one named error model (first match, most specific, ignore arguments, default
  allow, earlier anchor, netting, and so on).
- **Abstain options** ("cannot decide", "not determinable", "escalate", "none"): each family states its gold share.
  An abstain option is wrong on at least 50% of the rows that show it. Yes/no rows never abstain.

**Depth and length**
- **Depth:** at most 2 unstated operations per row, and every intermediate value is printed (day counts, window starts,
  normalised UTC times, unit prices). Deep items are ≤ 10% of a family, flagged `meta.deep`, and reported separately.
- **(C2) Length:** every new row is ≤ 2,000 rendered tokens (instructions counted twice). Family mean ≤ 800. No long
  rows, so the A22/A28 long-row cap is met trivially.

**Text authoring**
- **(C2) Authoring modes:**
  - **Mode T, slot-template, ≥ 75% of each family:** Haiku writes label-blind skins with typed `{SLOT}`s, and the
    program fills every value, name, date, number and lexicon clause.
  - **Mode F, free-form, ≤ 25% (T07 and T32 ≤ 40%):** Haiku writes or paraphrases from a facts-only brief, then must
    pass the fact-lock checks (G-SL and G3-H, section 6).
- **(C2) Haiku never sees** the question, the options or the gold while writing.

**Content limits**
- Difficulty comes from the C1-only crowd: easy ≤ 25%, hard ≤ 30%.
- The label-check form ("Is the correct answer X?") has 0 rows.
- All entities, jurisdictions, programmes, thresholds and statutes are invented, and every rule the answer needs is
  stated in the item.
- Times use fixed UTC offsets only: no DST and no named time zones (T17 veto).
- No real statute text and no new public datasets.

**Row format:** spec 2.4 plus `meta.c2`: `{author_mode: "T" | "F", skin_id, register, lexicon_ids, haiku_task_id,
haiku_prompt_sha, twin_kind, twin_of, closed_world: bool}`. Licence: "CC0 1.0 (program-generated; Claude/Haiku-authored
wording)", added to LICENCE_REGISTER §3 when A37 is adopted.

### 3.1 T28: Permission verdicts (allow / ask / deny)

**Structure**
- 3-8 rules. Each rule has:
  - an effect: allow, ask or deny;
  - a tool pattern: exact name, `ns.*` or `*`;
  - 0-2 argument conditions: recipient-domain glob, path prefix, amount with a stated inclusive or exclusive
    comparator, owner self/other, environment.
- The glob semantics are stated on every card (whether `*` crosses `/`), and so is a default effect for no match.
- One precedence policy from a closed set of 5:
  - (P1) deny > ask > allow, regardless of order;
  - (P2) the first listed match;
  - (P3) the most specific match, by a specificity tuple stated on the card, with ties broken by effect order;
  - (P4) the last listed match;
  - (P5) a named priority list.
- One proposed call, rendered as JSON, a function call or a CLI line, with an optional session role.

**Samplers**
- S1 forward.
- S2 label-first: the decisive rule plus 1-2 near-miss rules, each failing on exactly one condition.
- S3 settings-file-first (YAML/JSON with invented keys).
- S4 admin memo, or the call embedded in an agent transcript.
- S5 (held out): IAM-style statement JSON and an IT chat thread.

**Question forms**

| Form | Share |
|---|---|
| 3-way verdict | 40% |
| Yes/no ("Can the agent run this call without asking?", "Must the agent refuse it?") | 45% |
| Which rule decides | 10% |
| Inverted: which of these calls runs without asking? | 5% |

**Balance and traps**
- Each verdict is 1/3 ± 2 pp per policy. The decisive rule's position is uniform.
- Trap shares (overlapping, as shares of rows):

| Trap | Share |
|---|---|
| The first listed match has the losing effect | 30% |
| The most specific match loses under P1 | 20% |
| The stated default decides | 15% |
| Argument-level deny vs tool-level allow | 15% |
| Amount exactly at the threshold | 15% |
| Near-miss strings (`.co` vs `.com`; `/data/prod` vs `/data/production`) | 10% |

- Tone is balanced: 50% of denies sound benign and 50% of allows sound alarming. Pressure lines ("just run it",
  "admin approved") never change the label.

**G4 metamorphic relations**
- Shuffling the rules under an order-free policy leaves the label unchanged.
- Adding an inert rule leaves it unchanged.
- Renaming a tool or domain leaves it unchanged.
- Moving an argument across a threshold flips the label as predicted.

**Haiku**
- 40+ org/tool packs (8-15 tools per namespace, with argument names and plausible values).
- At least 6 paraphrases per precedence sentence and per question form.
- Admin memos as free-form rows.

**Risk:** config syntax may echo real products. Products are a design reference only, and G13 method 8 runs against
eval_opi and eval_jagged.

### 3.2 T35: Path-rule access (robots-style; T28 plugin cards)

**Structure**
- 1-6 agent groups and 1-8 Allow/Disallow lines with `*` and `$`. A named group competes with the `*` group.
- An optional fetch status (2xx, 4xx, 5xx, unreachable) on 15% of rows.
- The card states every rule:
  - group selection;
  - longest match in octets;
  - Allow wins a tie at equal length;
  - 4xx means allowed;
  - 5xx or unreachable means everything is disallowed;
  - percent-encoding equivalence.

**Questions:** 70% yes/no ("May the crawler fetch this URL?"); 30% "which line decides?".

**Traps**

| Trap | Share |
|---|---|
| Equal-length tie | 30% |
| The first listed matching line is wrong | 30% |
| Named group vs `*` conflict | 25% |
| Status rows | 15% |

**Verifier:** Protego may be a third check only after its licence is read upstream (G1).

**Haiku:** writes site and crawler narratives only. The program writes every rule, path and URL, and URLs use
reserved `.example` domains.

### 3.3 T33: Outcome verification against tool logs

**Simulator**
- 25-30 invented mock APIs with status codes and async jobs (202, then poll).
- Retries with idempotency keys: a later 409 with the same key means the work is already done.
- Partial writes (`rows_written` < `rows_requested`) and unit fields (`amount_cents`, `duration_ms`, `bytes`).
- 2-6 calls per episode, with 30% injected failures.

**Sub-forms**
- **(a) Step success, 50% of rows:** one of about 20 stated criteria. Asks "Did step k succeed?" (yes/no) or
  "Which check failed?" (choice).
- **(b) Claims vs log, 50% of rows:** the agent's final message holds 2-4 claim slots, 0-2 of them corrupted (status
  flip, ×100 unit scale, value swap, wrong entity, no matching call, wrong time order). Questions:
  - which claim is contradicted or unsupported (the claims plus "none");
  - per claim: supported, contradicted, or not shown in the log;
  - yes/no: "Is every claim supported?"
- The card states the label semantics on every row: 202 means queued, not done; a later 409 with the same key means
  already done; amounts are in cents; a claim with no matching call is "not shown", not "contradicted".

**Rendering**
- The program renders the log as JSON lines, plain text, CSV or a markdown table.
- Logs are ≤ 20 lines and rows ≤ 2,000 tokens.

**Samplers:** S1 forward episode; S2 label-first (pick the corruption); S3 table-first; S4 ticket or PR summary;
S5 (held out): a ticket thread with pasted logs.

**Traps**

| Trap | Share |
|---|---|
| 2xx, 202 or a success word on an unfinished or failed step | 25% |
| An earlier failure, then a successful retry (gold: success) | 15% |
| Cents read as dollars | 15% |
| A claim with no matching call | 15% |
| The same value on a different entity | 10% |
| No success word, but a true success | 10% |

Claim count, message length and log length must not predict the label (G6 metadata).

**Verifier:** solver B re-parses the rendered log into sqlite, normalises units with its own table and re-matches
the claims. A claim that binds to two fields drops the row.

**Haiku**
- Writes final-message skins in at least 6 voices: support agent, coding-agent PR summary, ops bot, travel agent,
  finance assistant, scheduling bot.
- Writes API pack names and descriptions, and criterion paraphrases.
- Never writes or edits a log line, and never chooses which claim is corrupted.

### 3.4 T29: Confirmation gates

**Structure**
- 3-6 conditions per card, from a pool of about 15:
  - irreversible, or the undo window is closed (elapsed hours printed);
  - bulk action over N records;
  - payment over a threshold;
  - external recipient;
  - another team's record;
  - production environment;
  - deletion;
  - PII export;
  - outside the stated hours (fixed UTC offset);
  - "explicit confirmation already given in this conversation for THIS action".
- The card states the precedence: forbidden > needs confirmation > permitted. A missing decisive field means
  "cannot decide".
- About 40 action types. The state snapshot is rendered as an admin console, a ticket, JSON or key-value lines.

**Questions**

| Form | Share |
|---|---|
| 4-way verdict | 45% |
| Yes/no ("May the agent go ahead now?", "Must it ask the user first?") | 50% |
| Which rule applies | 5% |

**Samplers:** S1 forward; S2 label-first near-miss; S3 snapshot-table-first; S4 chat-session-first (with an earlier
confirmation turn); S5 (held out): a runbook page or a multi-step agent plan.

**Balance**
- "Cannot decide" is gold on 15% of choice rows; the other three verdicts are about 28% each.
- "Cannot decide" is shown on about 60% of choice rows and is wrong on at least 50% of the rows that show it.

**Traps**

| Trap | Share |
|---|---|
| Threshold boundary (N vs N+1; 23:59 / 24:00 / 24:01, inclusive or exclusive stated) | 20% |
| Sounds harmless but is irreversible | 15% |
| Sounds alarming but is reversible and under every threshold (gold: proceed) | 15% |
| The owner field triggers a rule | 15% |
| Confirmation given for a different action | 10% |
| A missing field that does not matter (the verdict is still decided) | 10% |

**Premise-removal twins** on 5% of rows: the gold becomes "cannot decide", and each twin has its own call_id.

**Verifier:** solver B decides "cannot decide" only if the completions of the missing fields disagree.

**Report:** the over-ask rate on mixdev and transfer dev.

### 3.5 T30: Clarify or proceed after deduplication

**Structure**
- Context records of about 12 types (contacts, files, calendar slots, accounts, orders…), with 0-4 candidates.
- The card states:
  - the identity key (email, path, account id);
  - the normalisation rule (case-folding, whitespace);
  - an exact, closed-world name-match rule;
  - a consequence table: read, draft and search are low; sending money, deleting and sharing externally are
    consequential.
- The decision rule: 1 distinct candidate → proceed; 0 → stop and say none was found; more than 1 with a
  consequential action → ask; more than 1 with a low action → proceed on all, only if the card's batch rule allows it.

**Questions:** 3-way proceed / ask / stop; yes/no "Can the agent go ahead without asking?"; "Which record is the
target?".

**Gold:** proceed 42%, ask 42%, stop 16%.

**Traps**

| Trap | Share |
|---|---|
| Exact duplicates that must collapse | 35% |
| Same first name, different identity | 30% |
| A low-consequence batch with several candidates (gold: proceed) | 15% |
| A nickname that does not count as a match | 10% |

A recency hint is present but never decisive.

**Haiku:** writes request phrasings, listings and chat context. Name pools are expanded by program from Haiku seed
pools. G6 and G7 catch any request that hints at the target.

### 3.6 T27: Embedded request that widens scope

**Structure**
- About 25 user-task templates with explicit scope classes (read, summarise, extract, compare, draft-not-send,
  book-within-budget). Each lists its allowed action classes.
- About 60 carriers: web page, email, PDF text, tool output, calendar invite.
- 0-2 embedded requests per carrier. Each request's action class comes from a closed lexicon: subscribe, forward,
  send, purchase, accept terms, change settings, save a payment method, share a link or file, enter credentials,
  download, reply, delete.
- The card's rule: in scope → follow it; out of scope and not blocking the task → ignore it and continue; out of scope
  and blocking the task → stop and ask the user.

**Controls:** 30-40% of rows (no request, an in-scope request, or a purely informational sentence).

**Questions:** yes/no "Does doing what this content asks stay within the user's task?"; a 3-way choice (continue the
user's task / do the requested step / stop and ask).

**Balance**
- Yes/no is 50/50; "stop and ask" is gold on about 20% of choice rows.
- Imperatives appear in both labels, and every justification string is used for both labels (G7).
- Polite and urgent phrasing appear equally in both labels.
- "Attack present" is uncorrelated with the label (G10).

**Safety**
- Never override phrasing ("ignore previous instructions…").
- Never a working lure: the asks are generic and the brands and URLs are invented.

**Decontamination:** G13 method 8 is binding against eval_opi's strategy strings and jagged's injected line. A
template that hits is dropped before any row exists.

### 3.7 T26: Provenance authority (legitimate vs fake)

**Structure**
- 2-4 checks per card, from:
  - a signed, numbered addendum or attachment number;
  - the sending domain equals the registered domain;
  - a call-back verification is logged;
  - the approver holds the stated role (delegation table);
  - the version id is in the register.
- About 15 contexts: bank-detail change, invoice, refund approval, IT access, HR edit, vendor onboarding, contract
  amendment, and others.
- Items come in pairs that are identical except for **exactly one** provenance field.
- Look-alike domains are made by program (`.co` vs `.com`, `rn` vs `m`, a hyphen). The program rejects pairs that
  tokenise identically.

**Questions:** yes/no ("Should the agent apply this change?"); a choice of apply / reject / escalate to the named
contact (escalate only when the card says a check cannot be verified from the text); "Which check fails?" plus
"none".

**Balance**
- Legitimate vs fake is 50/50 per context × phrasing.
- Urgency and authority vocabulary is identical across labels (G7 checks every unigram and bigram).
- Traps: legitimate amendments in alarming language 20-25%; look-alike domains 20-25%; the right domain but a missing
  attachment 15-20%.

**Risk:** a drift toward distrusting every amendment. This is guarded by the 50/50 balance and the D6 and OPI checks.

### 3.8 T31: Authority at time t (wave 2)

**Structure**
- Org graphs of 6-12 roles, with RACI defaults.
- 1-3 delegations with windows and value bands (inclusive or exclusive stated).
- 0-2 overrides or revocations with timestamps in fixed UTC offsets: at most one conversion, and normalised times are
  printed on non-deep rows.
- Agent grants with 2-6 scopes and chains of depth 1-2 (3 only on deep rows). The attenuation rule is stated: a child
  scope is the intersection and never exceeds its parent.
- Requests sit at boundaries.

**Questions:** choose the accountable approver (with "escalate: no unique approver" gold on ≤ 12%); yes/no "Is the
action authorised at T?".

**Traps**

| Trap | Share |
|---|---|
| Revocation 1 minute before the request | 25% |
| Band edge | 20% |
| Sub-agent broader than its parent | 20% |
| Lapsed delegate | 15% |
| Escalate | 10% |

**Solvers:** A is "latest explicit override > in-window delegation > default". B scans an interval table in UTC epoch.

### 3.9 T32: Commitment ledger in chat (wave 2)

**Structure**
- 2-6 commitments among 2-4 people. Events: fulfilment, an extension proposed then accepted or refused, a condition
  resolved, a waiver by an authorised or unauthorised party (the authority table is pinned), a retraction.
- "I'll try" is defined on the card as not a commitment.
- The status at time T is one of a closed set of 5: kept, broken, not yet due, not triggered, waived.

**Haiku:** renders each event as ONE casual chat message. The decisive phrase comes from the verified lexicon, and
there are no status words. Registers: family chat, landlord-tenant, freelance client, team chat.

**Verification**
- G3-H must map every message back to (event type, arguments), equal to the stream.
- A blind read of 400 rows (the highest ambiguity risk), with quarantine capped at 3%.

**Complements** use the closed set: "Was the promise broken?" vs "Is the promise not broken (kept, waived, not yet due
or not triggered)?".

### 3.10 T01: Windows and deadlines

**Samplers**
- **S1 rolling window:** at most N days in any M-day window. Stays have inclusive entry and exit, ≤ 3 stays, and each
  stay's day count and the window start are printed.
- **S2 later-of-two anchor:** a deadline anchored to the later of two events.
- **S3 waiting period:** day 1 is the day after inception, compared against the loss date.
- **S4 rolling sums** (from T02): purchases, or cash-in and cash-out kept separate (never netted), against a strict
  threshold.
- **S6 cutoffs** (from T16): a same-day cutoff stated in one fixed offset and applied to another, a day-of-receipt
  convention, a mail add-on and a holiday list stated in the text. No plain business-day counting, because F2 has it.
- **S5 (held out):** a table-first travel log or a court-style notice.

**Traps**
- 30% of rows sit exactly on a boundary: ±0 / ±1 day, or ±5 minutes for cutoffs.
- Named-error distractors: calendar year instead of the rolling window; the earlier anchor; counting day 0; netting
  cash-in against cash-out; "more than" read as "at least"; dropping an inclusive endpoint; rolling the wrong way;
  skipping the offset conversion.

**Haiku:** paraphrases of the window rules are admitted only by 3/3 extraction to the same rule id.

### 3.11 T23: Governing version (transition clauses)

**Structure**
- 2-4 versions of a rule in 10 domains: refunds, fees, leave, subscriptions, warranties, shipping, retention, pricing,
  travel caps, licences.
- Each version has an effective window (inclusive or exclusive ends stated), a supersession pointer and 0-1 transition
  clauses: prospective, grandfathered by purchase date, retroactive for open cases, or sunset.
- An anchor choice: event, purchase or filing date.
- Plain version-in-force rows with no transition clause are ≤ 30%, because F1 S6 already covers them.

**Questions:** which version governs; the outcome under the governing version; "Is this claim supported by the
governing version?".

**Traps**

| Trap | Share |
|---|---|
| The newest version is wrong | 30% |
| A distractor clause from another version | 30% |
| A decisive transition clause | 25% |
| A boundary day | 20% |

### 3.12 T24: Revision materiality (wave 2)

**Structure**
- About 40 rule templates, with typed edits:
  - threshold, anchor, exception added or removed, scope;
  - a cosmetic rewording (gold: no change);
  - an edit to a clause the case never touches (gold: no change);
  - a date-scoped edit whose window excludes the case (gold: no change).
- Cases sit at boundaries.

**Questions:** yes/no "Does the edit change the outcome for this case?", plus a choice of the outcome under V2.

**Admission:** a cosmetic Haiku rewording is admitted only if 2 independent extractions give an AST identical to V1's.

**Traps:** cosmetic or irrelevant edits 30%; anchor changes that flip the outcome 20%. Edit length must not predict the
label.

### 3.13 T06: Consumer return rights

**Structure**
- Invented jurisdictions with at least 3 statute styles; one style is held out for S5.
- The statute grants a right to reject faulty goods within N days of **delivery** and a withdrawal window counted from
  possession, with exceptions: personalised goods, sealed hygiene goods opened after delivery, perishables.
- A posted store policy that is stricter or looser.
- Dates cross month ends and leap days.

**Questions:** "Is the customer entitled to a full refund?"; which rule decides.

**Traps**

| Trap | Share |
|---|---|
| A stricter sign (the statute wins) | 25% |
| Order date vs delivery date | 20% |
| Boundary day | 20% |
| A conditional exception | 15% |
| A posted policy more generous than the statute (the policy applies) | 10% |

No UK or EU text is copied.

### 3.14 T15: Eligibility gates (wave 2)

**Structure**
- Invented programmes, with the year labelled in the text.
- Ordered gates, with amounts at, one cent above and one cent below each limit; gross vs net income.
- Categorical routes that skip gates.
- Claimant sets of 2-4 people with months lived, flags and ordered tie-breakers on the card.

**Questions:** yes/no eligibility; the named claimant; the deciding gate ("Not eligible: <reason>").

**Traps:** stopping at the first gate; net vs gross; an amount equal to the limit; a missed categorical route; the
wrong tie-breaker order.

Real benefit values are never used.

### 3.15 T12: Three-way match (wave 2)

**Structure**
- A PO with 1-4 lines, 2-200 units and integer-cent prices. Receipt shortfalls of 0-3 units.
- Invoice price shifts of −5% to +5%, including the exact tolerance boundary (computed in cents).
- 2-4 checks in a stated order: quantity vs received, unit-price tolerance on a stated base, duplicate invoice number,
  approver limit.
- The tolerance is an absolute amount on 50% of cards, and unit prices are always printed.

**Answer:** approve, hold for receipt, price-variance review, or reject as a duplicate.

**Traps**

| Trap | Share |
|---|---|
| Totals match but the lines differ | 25% |
| Two checks fail and the policy order decides | 20% |
| Exactly at the tolerance | 20% |

A wrong tolerance base is also used as a trap.

### 3.16 T07: Headline promise vs footnote (wave 2)

**Structure**
- A bank of headline promises × structured qualifiers: region, product class, time bound, membership tier, minimum
  spend, exclusions.
- Two-part qualifiers (AND). The customer's attributes fall inside or outside each qualifier.
- Controls (35%): the qualifier does not apply to this customer.

**Haiku:** the main free-form author (≤ 40% free-form): ad copy, checkout notes, SMS promotions, app banners and
warranty cards, with `{REGION}`, `{TIER}`, `{DATE}` and `{SPEND}` slots.

**Traps:** the qualifier sits in a later paragraph; a time bound ending on the purchase date. Headline salience is equal
across labels.

### 3.17 T25: Source reliability with tie-abstain (wave 2)

**Structure**
- Bundles of 3-5 sources, each with a stated tier, a date and an independence flag ("copied from X").
- The card's rule:
  - the highest tier wins;
  - within a tier, the most recent wins;
  - copies are ignored;
  - independent top-tier sources that tie on tier and date and disagree → "not determinable".
- 25% of bundles are ties, and half of those agree (so they stay determinable).

**Abstain and yes/no**
- Yes/no rows are generated only on determinable bundles.
- "Not determinable" is gold on 15-25% of choice rows and wrong on at least 50% of the rows that show it.

### 3.18 T37b: Real-text complements on replay (block of 2,000 rows)

**Bases**
- Hard-label yes/no replay rows with **human** gold, from KEEP-licence sources whose card defines a **binary**
  predicate.
- Never vote-share rows, never 3-class sources (so "not positive" is never read as "negative"), and never the old
  slice.
- Only bases that are not already in a relation unit, so each unit is 2 rows.
- At most 10% of the block from any one source.

**Partners**
- **1,400 complements** (gold = 1 − gold; a `complement` relation with the base; same call_id). Of these:
  - at least 25% use implicit negation (fail to, lack, rule out);
  - at least 30% use a closed per-source antonym list or option framing.
- **600 equiv paraphrases** (same gold).

**Checks**
- negcount must find exactly one added negation cue on the predicate span, or an antonym from the closed list.
- Two independent Haiku polarity judgements must agree.
- A blind Haiku solver answers the base and the partner. Any inconsistent pair goes to Claude review, and any doubt
  drops the pair.
- Templates may not match dev_negwords, dev dneg frames or the F5 held-out probe templates (G13 method 8).

**T37b-dev:** 300 complement pairs on binary-predicate yes/no rows of the 9 gate dev splits, written with held-out
frame templates. They are never trained.

### 3.19 Carry-over pools
- **F5** (QC pass; trained only in the unshipped round-1 candidate): 1,500 rows, complement and equiv units only.
  Re-run G13 against the new targets only (OHS-4 exports, C2 mixdev, transfer dev, T37b-dev).
- **F6** (QC pass; its v2 rebuild still owes the G5 delta, QC finalize, crowd/select/G9 redo and its own G13): ≤ 1,000
  rows, only if every open step passes by the cutoff.
- **F11** (QC pass; needs a G13 re-run after the 8 Oct wording fixes): ≤ 1,000 rows. Prefer its XED/MAMS real-text
  codebook rows.
- **F4** (QC pass; the A31 seed hedge must be fixed at the generator, then G10 and G13 re-run): ≤ 500 rows.
- **Not carried over:**
  - F3: one design only, and long rows drove the round-1 cost.
  - F7: no design.
  - F12: QC pass=false, and its design copies When2Call (a DI test).
  - F9: its rules-block text collided with OHS-source text.

### 3.20 Transfer-dev builders (T36, T19, T21, T20; dev only)
- Built by separate plugins after the OHS-4 freeze, with held-out registers and two solvers each:
  - T36: node-semver and PEP 440 semantics reimplemented twice;
  - T19: a boolean evaluator plus SQL;
  - T21: a clause tree, two encodings;
  - T20: a matrix plus an escalation counter, twice in integer minutes.
- 300 items each. Frozen with sha256 before training, and never trained.

---

## 4. Consistency, minimal-edit pairs and calibration

### 4.1 The overlay (every program family; 3/3 designs)

| Relation | Share | Unit rule |
|---|---|---|
| Minimal-edit twin: exactly one slot changes and the program recomputes a flipped gold | 20-25% of each family's rows | Own call_id per twin, linked by `meta.twin_of` (no relation term, as in spec 2.1) |
| Complement yes/no pair | ≥ 20% of each family's yes/no rows | Same call_id, `complement` relation, lam 1.0 with sym_cons |
| Non-syntactic complements (closed antonym list or option framing) | ≥ 30% of complement pairs | As above |
| Equiv format twin (same facts, different register or container, e.g. JSON vs CSV, YAML vs memo) | 5-10% of rows | Same call_id, `equiv` |
| Attack twin (an inert injected line or a fake authority line in a tool output; label unchanged) | About 5% of agent-tier rows | Same call_id, `inv`; wording never matches eval_opi or jagged |
| Premise-removal twin (gold becomes "cannot decide") | T29 5%; T25 via ties | Own call_id |

**Rules for the overlay**
- Relation units hold at most 3 rows.
- Complements are exact only under a **closed-world sentence** on the card ("the listed rules and records are
  complete…"). The program asserts gold(Q) = not gold(not-Q).
- G-TW (section 6) checks that exactly one slot differs between twins and that the gold flips exactly as predicted.

### 4.2 T37b: real-text complements
See 3.18. This is the only lever aimed at the real-text complement gap. It is capped at 2,000 rows to limit label risk.

### 4.3 Calibration
- **Hard 0/1 labels** on every new row, with C1's label smoothing (0.05; MNLI 0.08). No LLM soft labels (T38 veto),
  and F8-style soft yes/no targets are never added.
- **Abstain options** are trained in both directions:
  - T29 "cannot decide", T25 "not determinable" and T31 "escalate", each wrong on at least 50% of the rows that show
    it;
  - T30 trains against over-asking;
  - F6, if carried over, trains abstaining when a premise is missing.
- **Serving temperature:** as recipe 6.0. One T per type, fitted leave-one-group-out on the C2 mixdev groups (held-out
  sampler, pack and register groups), and bounded to [0.8, 1.3]. Never fitted on OHS-4 or any sealed or Jev data. No
  test-time prior fix (B4).
- **Brier** is gated at C2 ≤ C1 + 0.005: on dev (D4, the PREREG 3.3 d cross-fit T) and on OHS-4 yes/no.

---

## 5. Mix and replay

### 5.1 The mix (one pass)

| Block | Rows (full build) | Share of the mix |
|---|---|---|
| Agent tier (T28, T35, T33, T29, T30, T27, T26, T31, T32) | 13,600 | 20.5% |
| Everyday tier (T01, T23, T24, T06, T15, T12, T07, T25) | 7,000 | 10.5% |
| T37b real-text complements | 2,000 | 3.0% |
| F5 carry-over | 1,500 | 2.3% |
| F6 / F11 / F4 carry-over (conditional) | ≤ 2,500 | ≤ 3.8% |
| **New rows** | **≤ 26,600** | **40%** |
| **Replay** (C1's golden_train) | **≤ 39,900** | **60%** |
| **Total** | **≤ 66,500** | 100% |

### 5.2 Caps
- One family ≤ 2,400 rows (≈ 9% of new rows). The agent tier is ≤ 55% of new rows.
- Free-form rows ≤ 25% per family (T07 and T32 ≤ 40%).
- Every new row ≤ 2,000 tokens; the mean of new rows ≤ 800.
- New yes/no rows are 45-55%. G10 cells are 50 ± 2.
- Difficulty: easy ≤ 25%, hard ≤ 30%.
- No new ordinal rows (T20 is not trained), so G18 and `lam_ord` apply only to replay ordinal rows.

### 5.3 Waves and the cutoff
- **Wave 1** (core; built first): T28 + T35, T33, T29, T30, T27, T26, T01, T23, T06, T37b, F5.
- **Wave 2:** T31, T32, T24, T15, T12, T07, T25, plus the conditional carry-overs.
- **Cutoff:** a family enters only if it passes every gate by the data cutoff (10.1, D6).
  - A family that fails after **2 fix iterations** is cut.
  - Missing shares **lower the total**; they are never refilled with lower-quality rows. This follows A34 (c): no
    tested balance-keeping refill exists.
  - Replay is always floor(1.5 × realised new rows).
- **Minimum to train:** at least 5 of the 6 agent-core families (T28, T33, T29, T30, T27, T26) plus at least 10
  program families in total. Otherwise stop and report to the owner, and do not train.

### 5.4 Replay (reuse `replay_sample.py` unchanged)
- **Pool and drops:** C1's golden_train with every round-1 drop (DROP, DEFAULT_DROP, Claude-gold prefixes, VERIFY and
  HF-card-only unless verified, deny-list verdicts, OHS-3 hit sources, human rows with p_g < 0.2), **plus
  `pool_drops_r1.json`** (the 25,147 rows the round-1 pool decontamination removed).
- **Quotas:** n_s^0.7, floor min(n_s, 150), cap 4%.
- **Draw:** whole relation units; E2 yes rate per wording.
- **Old slice:** 2,000 rows, held out by group_id and normalised state (the same slice as round 1, so the snapshot
  reads compare like with like).
- **Fresh draw:** a new seed, preferring units that were not in round 1's replay (C1 has seen all of them; this only
  spreads coverage).
- **C1 anchor:** KD 0.5 on replay rows where C1 is right and p_top ≥ 0.8, or right on a protected unit (inv, equiv or
  complement). Never on new rows.
- **G13 on replay:** only against the **new** targets (OHS-4 exports, C2 mixdev, transfer dev, T37b-dev), through
  `decontam_g13.py refresh --targets …` behind a wrapper. Every old target was already cleared in round 1.

### 5.5 Budget trim
Before launch, `mix_c2.py` projects the training cost from real padded tokens: A28's 0.163 ms per padded token, at
$4.09/h.
- If the projection is above **$17** (one free account's balance minus a $2 reserve), it trims new and replay rows in
  proportion, keeping the 40/60 split, the family shares and every balance rule.
- The floor is 50,000 rows. Below that, it stops and asks the owner.

---

## 6. Pipeline and gates

### 6.1 Reused as is
No pinned `lean/*.py` file and no existing `c_build` file is edited. All new code lives in `lean/c2_build/`.

| Tool | Use in C2 |
|---|---|
| `c_src/common/denylist.py`, `negcount.py`, `g8_aflite.py`, MARKERS | Deny-list on declared parents; polarity checks and T37b; G8 |
| `c_build/decontam_g13.py` + `decontam_g13_batch.py` | G13, all 8 methods + A31 b/c + the sealed-side child, through a C2 target-registry wrapper that adds OHS-4 exports, C2 mixdev, transfer dev and T37b-dev |
| `c_build/crowd_select.py` | Bins, stratified whole-unit selection, reflow, chi-square and the G5 re-read list, imported by `c2_select.py` |
| `c_build/mixer.py` + `mixio.py` logic | Through `mix_c2.py`, a copy with C2 shares and the OHS-4 sha. Its existing tests must pass, plus new share tests |
| `c_build/replay_sample.py` | As is, with `pool_drops_r1.json` |
| `gate_dev.py`, `calibrate.py`, `preds_to_gate.py`, the `gate_c.py` pattern | D1-D6 and T fits; `gate_c2.py` is a new file |
| `spend_guard.py`, `r1_check.py`, `r1_chain.sh`, `fill_config.py` | Spend guard, projection, segments, config fill (C2 copies with new caps) |
| `train_decoder.py`, `decoder_io.py` (pinned) | Training; G15 round trip; cygnet + schema_branch_mark |
| `hosting/` SGLang S1 | Crowd read and the OHS-4 look (served path) |
| TEACH-0 harness pattern | Haiku agents get gold-free chunks with opaque ids, at most 50 items each, plus a file-access audit |
| O*NET persona seeds, the formats-1 renderer, `c_src/packs` | Reused seeds (already G13-clean) |

### 6.2 New code (Claude writes it once)
1. **`c2_kit`**
   - Typed slots: date, UTC-offset datetime, integer cents, count, category, id, glob, URL.
   - A rule AST and solver A/B interfaces.
   - The slot-locked skin renderer (with grammar agreement).
   - The relation emitter (complement, twin with a slot-diff assert, equiv, inv).
   - A distractor helper driven by named error models.
   - The Haiku task chunker and auditor.
2. **Operator lexicon registry.** Each surface form maps to one semantic id and has a parser unit test. A form is
   admitted only if 2 independent Haiku extractions agree; precedence and window rules need 3/3.
3. **G0-lite specs.** One page per family: a semantics table of at most about 150 lines, one Haiku ambiguity listing,
   one Claude resolution, then frozen. This replaces round 1's 1,200-1,900-line specs (20,653 lines across the G0
   specs).
4. **Plugins.** 17 family plugins (about 300-600 lines each), the T37b builder and 4 transfer-dev plugins.
5. **New gate code.** G-SL, G3-H, G5-H, G-LEX and G-TW (below).
6. **`c2_select.py`, `mix_c2.py`, `gate_c2.py`**, and `snap_monitor_c2.py`, a copy with the pgrep self-match bug fixed.

### 6.3 Gates and bars

**Kept from round 1**

| Gate | C2 bar | Change vs round 1 |
|---|---|---|
| G0 | One-page spec + semantics table + one ambiguity pass | Lighter |
| G1 provenance | Spec 2.4 meta + `meta.c2` (author mode, Haiku task id, prompt sha) | + Haiku fields |
| G2 solver B | 100% agreement | Same |
| G3 round trip | 100% on template rows | Same |
| G4 metamorphic | ≥ 3 relations, 100%, ≥ 1,000 rows per sampler | Same |
| G5 → **G5-H** | Two independent Haiku blind solvers on 300 rows per family (400 for T32), plus one Haiku read of 100% of free-form rows. Every disagreement with gold goes to **Claude** adjudication (flag only), plus 30 seeded agreed rows per family. Bar: **0 confirmed wrong golds, ambiguous ≤ 1%**. A template with > 3% disagreement is quarantined; a confirmed wrong gold is a generator bug. Rows are never relabelled | Reader changes (Haiku, then Claude); bar unchanged |
| G6 partial-input baselines | ≤ chance + 2 pp on ≥ 5,000 QC rows, plus a separate report on the free-form slice. This absorbs D1's G8-H text-only predictor | Pilot first (6.4) |
| G7 feature z-test | No failing feature; features include register, skin id, justification string and urgency words | + Haiku features |
| G8 AFLite | < 10% | Same |
| G9 crowd | **C1-only** p_g (A18.2 readout) on SGLang S1 or the free L4. Same bins. Rows with p_g < 0.05 go to the G5-H re-read | One model instead of 3 |
| G10 balance | Spec 2.1 + section 3.0 | Same |
| G11 diversity | No skin or template above 2% of a family; Self-BLEU and Vendi no worse than the golden_train slice | Same |
| G12 dedup | Exact 0; MinHash keep one; one structure per surface except twins | Same |
| G13 decontam | 0 hits after drops: **seed-first** (Haiku pools before any row), then candidates, then the final mix (replay only vs new targets) | Order changed |
| G14 | OHS-4 frozen (A38) before any C2 pool, pack, template, generator run or row | Same rule, new suite |
| G15 loader round trip | 100% | Same |
| G18 ordinal lint | 100% on replay ordinal rows | Same |

**New in C2**

| Gate | Bar |
|---|---|
| **G-SL slot lint / fact-lock** | Every slot appears exactly as required. Outside the slots: no literal number, date, weekday, month, relative-time word, quantity, quantifier, modal, hedge, name, status word or gold-label word, and no negation in names. Mode-F text keeps every slot value verbatim and adds no number, date, id or negation (negcount). **100%**, else the row is dropped |
| **G3-H LLM round trip** | An independent Haiku extractor turns the filled free-form text back into the structured spec, which must equal the generator's. **≥ 98% per template**, else the template is quarantined. Mismatched rows are always dropped |
| **G-LEX lexicon admission** | Every lexicon form passes its unit test, plus 2/2 extraction agreement (3/3 for precedence and window rules) |
| **G-TW twins and complements** | A minimal-edit twin differs in exactly one slot and its gold flips exactly as predicted. A complement pair satisfies gold(Q) = not gold(not-Q) under the closed-world card. **100%** |
| **G-TPL (sealed side)** | A counts-only 8-gram compare of C2 templates vs OHS-4 templates. A hit drops the C2 template |

### 6.4 Gate order per family
1. G0-lite spec frozen.
2. Code: samplers, solvers A and B, parser.
3. Haiku pools (packs, lexicon, skins, wordings).
4. **G13-seed** on the pools; a hit quarantines that template only.
5. **Pilot of 1,000 rows:** G2, G3, G4, G-SL, G3-H, G-TW, G6, G7, G10, and G5-H on 100 rows.
6. At most 2 fix iterations (generator only).
7. Full 1.5× generation: G2-G4, G6 on ≥ 5,000 rows, G7, G8, G10-G12, G15, G-SL, G3-H, G-TW, G5-H at full.
8. G13 on candidates (one batch for every family).
9. C1 crowd, selection, G9 re-read.
10. Mix, then G13 on the final mix (new targets), then preflight.

G13 batches take about 8-10 h of CPU each (round-1 logs). The plan runs three: seed-first, candidates and final mix.
They run overnight, niced, with resumable caches.

### 6.5 Who may read what
**C2 builders and Haiku agents never open:**
- any path containing "ohs" (including `lean/ohs4_sealed/`);
- `sealed_nd/`, `c_spec/sealed_brief/`, `c_build/preread/`;
- `bench/external_quarantine/`, `bench/longbench_v2/`;
- any file with "jev" in its name, and the 7.4 Jev-output list;
- DI items and JevBench items (only the decontamination program may read JevBench item text).

**Other access rules**
- A Haiku agent reads only its own task chunk, and the audit checks its file access.
- The OHS-4 sealed session never reads C2 specs, the kit, pools or rows.

---

## 7. Dev gate and ship rule

### 7.1 Dev sets (built before training; never trained)

| Set | Size | Use |
|---|---|---|
| Mixdev | 150 per trained family from S5 + held-out packs, registers and wordings (about 2,550), plus F5/F6/F11 existing S5 mixdev | Learning check (a); temperature fit |
| Transfer dev | T36, T19, T21, T20 × 300 = 1,200 | Transfer check (b) |
| T37b-dev | 300 complement pairs on gate-dev yes/no rows | Complement check (d) |
| Retention | 9 gate dev splits (7,056 rows), _perm, jagged, OPI; D2 unseen set re-derived with C2's training files (spec 7.3) | D1-D6 |
| Old slice | 2,000 C1 training rows held out | Snapshot stop rule only, never a ship rule (recipe 5) |

### 7.2 Pre-gate (all must pass before C2 gets its one OHS-4 look)
C1 and C2 are read in the same job.

| Check | Pass when |
|---|---|
| (a) Learning | Mixdev C2 − C1 ≥ +8.0 pp and paired LB > 0 |
| (b) Transfer | Transfer dev C2 − C1 ≥ +3.0 pp and LB > 0 |
| (c1) D1 | Dev full set: LB > −1.5 pp |
| (c2) D2 | Re-derived unseen set: not (point < −1.0 and UB < 0) |
| (c3) D3 | Yes/no and choice accuracy each ≥ C1 − 1.0 |
| (c4) D4 | Calibrated yes/no Brier ≤ C1 + 0.005 |
| (c5) D5 | Equivalence and permutation flips each ≤ C1 + 2 pp |
| (c6) D6 | jagged and OPI attack success: not (above max(C1 + 2 pp, 3%) and LB of the increase > 0) |
| (c7) D9 | p50 latency ≤ 1.05 × C1 (same served path) |
| (d) Complement | Complement violation on T37b-dev: C2 < C1 (point) |

Dev CIs use 10,000 paired group-bootstrap resamples, seed 0.

**If any check fails:** C2 gets no OHS-4 look and does not ship. OHS-4 is still read once for **C1 vs Jev**
(SPEED-3). The diagnosis reads dev only.

**Report-only:** each held-out family, the over-ask rate, ECE, the yes-share drift, hard_dev and pg_dev, and the
C2 − C1 complement LB.

### 7.3 Ship rule (one OHS-4 look)
- **The candidate:** the final-step adapter, merged to bf16 and served on SGLang S1. C1 and C2 are read in the same
  job.
- **Parity:** S1 vs the HF adapter read on dev must reach ≥ 99.5% argmax agreement (A35's bar for the served path).
  C2 replaces C1 only if every rule below holds.

| Rule | Part | Pass when |
|---|---|---|
| S1 | R (rule/agent, trained categories, independent generators; n ≈ 1,600) | C2 − C1 ≥ +5.0 pp **and** paired 95% LB > 0 |
| S2 | G (general real text; n ≈ 3,000) | Non-inferiority: LB of C2 − C1 > −1.5 pp |
| S3 | Complement pairs (G + R) | C2 ≤ C1 (point) and UB of C2 − C1 < +0.01 |
| S4 | All yes/no | Calibrated Brier (mixdev T) ≤ C1 + 0.005 |
| S5 | X (security) | Attack success not above max(C1 + 2 pp, 3%) |
| S6 | Dev | Pre-gate (c1)-(c7) still pass (they are not re-read) |

**Report-only:** part U (unseen kinds), per kind and per domain, minimal-edit consistency, option-order drift, ECE,
latency and $/1K.

**Power** (from round 1's realised paired SE of 0.541 at n = 2,542)
- At n ≈ 3,000, SE ≈ 0.50, so S2 passes with probability 85% at a true 0, 59% at a true −0.4 and 17% at a true −1.0.
- S1 at SE ≈ 1.1 passes with probability 82% at a true +6 and 50% at a true +5.

### 7.4 Draft amendment A37 (to be dated and committed only after the owner's GO; before any C2 pool or row)

> **Amendment A37 (DRAFT; owner GO pending): C2, the final fine-tune of C1 on program-gold agent and everyday decision
> data, with Haiku 5.5 as a text author only. Written before any C2 Haiku pool, pack, template, generator run, row or
> OHS-4 item exists.**
> - **(a) Plan.** `lean/teach1/C2_DATA_SPEC.md` (sha256 <fill at commit>) is binding, like the C spec.
>   - The C spec and the recipe apply unless this file changes them. Every change is listed in sections 3.0, 5 and 6.3
>     and in Appendix A.
>   - Start: C1 (adapter 507d1c29...). One candidate: the final-step adapter.
> - **(b) Haiku 5.5's role.**
>   - **Allowed.** Haiku 5.5 may write packs, slot templates, skins, paraphrases and free-form documents. It may also
>     read blind to flag problems (G5-H, G3-H, G-LEX, T37b polarity).
>   - **Never allowed.** Haiku never sets, edits or chooses a label, and its outputs are never training targets.
>   - **Where gold comes from.** Every gold comes from solver A and is re-derived by an independent solver B (G2 at
>     100%). T37b golds are 1 − human gold or the same human gold.
>   - **What a disagreement can do.** A Haiku disagreement can only drop a row or quarantine a template.
>   - **What this changes.** This changes the "no bigger teacher" and "Claude authors the data" rules ONLY to let
>     Haiku author wording. No model above 4B is trained, distilled from or used as a label source.
> - **(c) Licence.** New rows are "CC0 1.0 (program-generated; Claude/Haiku-authored wording)".
>   - LICENCE_REGISTER §3 gets this entry.
>   - **The owner confirms** that the Anthropic output terms on this account allow training an in-house model on
>     Haiku-written text, the same status as the existing Claude-written packs.
>   - No new public dataset is added.
> - **(d) Data.**
>   - 17 program families: 20,600 rows (agent tier 13,600, everyday tier 7,000).
>   - T37b: 2,000 rows. Carry-over: F5 1,500, plus F6/F11/F4 ≤ 2,500 if gated by the cutoff.
>   - Replay = floor(1.5 × new rows), so new is 40% and replay 60%.
>   - Waves, cutoff and minimums as in 5.3. Families not passed by the cutoff are left out with no refill.
>   - Transfer-dev families T36, T19, T21 and T20 are never trained.
> - **(e) Gates.** As in 6.3: G2, G3, G4, G15, G-SL, G-TW and G18 at 100%; G5-H with 0 confirmed wrong golds and
>   ambiguous ≤ 1%; G6 ≤ chance + 2 pp; G8 < 10%; G13 with 0 hits (seed-first).
>   - The crowd becomes C1-only. Bins and selection are unchanged.
>   - No gate bar is loosened.
> - **(f) Order (G14).**
>   - OHS-4 is built by an isolated session and frozen with its suite and scorer sha256 in **A38**, before any C2
>     Haiku pool, pack, template, generator run or row exists.
>   - C2 code and G0-lite specs may be written before A38, but no data may be.
> - **(g) Pre-gate and ship rule.** Exactly as in 7.2 and 7.3, fixed now.
>   - One OHS-4 look for C2. A failed pre-gate means no C2 look, and OHS-4 is read for C1 and Jev only.
>   - No snapshot, blend or second candidate.
> - **(h) Jev.** Read once on OHS-4, after the C2 verdict (or the failed pre-gate) is logged, with the owner's GO
>   (about $1 on OpenRouter; check the balance first). Claim rules are in 8.6. Jev outputs are never used for anything
>   else.
> - **(i) Training.** Recipe as in 9.1: LR 5e-5, one pass, C1's losses unchanged, `lam_ord` only on replay ordinal
>   rows, a new seed <fill>.
> - **(j) Money.**
>   - Training runs on mahadikarya2 free credit and is projected ≤ $17 (trim rule 5.5). Reads go on mahadikarya3 free
>     credit or the od-l4 VM (Google credit).
>   - No card is used without the owner's word. The C2 Modal total is capped at $30.
> - **(k) Stop rules.** Stop and ask if the steps-100-300 projection is above $17.
>   - Abort at once on a non-finite loss term.
>   - Stop if the old slice is below C1 − 1.5 pp at both the 25% and 50% snapshots, or if mean P(yes) on old yes/no rows
>     drifts by more than 0.02.
>   - A stopped run yields no candidate.
> - **(l) GO points.** The owner says GO on:
>   - this amendment;
>   - the crowd read;
>   - training;
>   - the OHS-4 look;
>   - the Jev read.
> - **(m) Unchanged.** No tuning on, and no design toward, OHS-1/2/3, DI, ejs-5, JevBench or the A15 suite. The A15
>   suite's looks are spent, and its scorer refuses more. Also unchanged: the Jev-output deny paths, one candidate and
>   one look, and no JevBench submission.

---

## 8. Fresh sealed final test: OHS-4 (also serves SPEED-3)

### 8.1 Isolation and order
- **Who builds it:** a separate Claude session, the sealed agent, working in a git-ignored folder
  `lean/ohs4_sealed/`. The name contains "ohs", so every existing never-open rule covers it.
- **What the sealed agent reads:** only a short brief. The brief gives the parts and categories below, the item format,
  the licence rules and the never-open list. It names **no** C2 family, sampler, register, lexicon or template.
- **No cross-reading:** the sealed agent never reads C2 specs, `c2_build/`, `c_src/` or any C2 pool. C2 builders
  never read OHS-4 or its brief.
- **Freeze:** the suite, the scorer and the exports are frozen with sha256s in **A38** before any C2 pool or row
  exists. The build log shows the order.
- **No spillage (lesson of the A15 incident):**
  - tool results never print item text outside the sealed folder;
  - after the build, a 12-gram re-scan of the shared session and temp folders must find 0 files with 3 or more hits.

### 8.2 Parts

| Part | Items | Content |
|---|---|---|
| **G** general | ≈ 3,000 | 8-10 fresh real-text sources with gold from humans, officials or programs (no LLM labels) |
| **R** rule/agent | ≈ 1,600 | 800 agent + 800 everyday-rule items in the owner's categories, with the sealed agent's own generators, solvers and wording |
| **U** unseen kinds | ≈ 600 | At least 3 task kinds the sealed agent invents and names only inside the sealed folder (report-only) |
| **X** security | ≈ 300 | Clean / attacked pairs over R kinds, in the sealed agent's own wording |
| Consistency (embedded) | +1,000 calls | 500 exact complement pairs (binary-predicate items only), 200 minimal-edit pairs (R only), 300 option-order pairs |

### 8.3 Rules for each part

**Part G**
- **Sources:** none may be:
  - in C1's 204 replay sources;
  - an OHS-1/2/3 source (a program check against `ohs3/used_sources.json`, never read by agents) or adjacent to one;
  - an A15 suite source (sealed-side check);
  - a DI test set, JevBench, ejs-5, LongBench v2, or on the 3.H deny-list;
  - Wikipedia or Natural Questions.
- **Licences:** permissive licences verified upstream. A creator's HF card does not count.
- **Domain spread:** at least 4 non-adjacent domains together hold at least 50% of items, and no domain is above 15%.
- **Item balance:** yes/no is 40-50% of items with gold yes at 50%; at least 30% of items are card-free; 2-8 options.
- **Quality:** a flag-only noise-floor read of 200 items per domain; a domain with more than 8% clearly wrong is dropped
  whole.
- **Leak filters:** label-word leak filters, MinHash dedup, and splits by group_id.
- **Decontamination:** a counts-only 12-gram check against C1's training file (the A15 precedent).

**Part R**
- **Categories named in the brief:** action authorisation; confirming or clarifying before acting; verifying outcomes
  and claims against evidence; untrusted content and authority; windows and deadlines; consumer and work policies;
  eligibility; fine print; versioned rules.
- **Wording:** written by the sealed session's own Claude model, **not Haiku**, so C2's Haiku style cannot inflate R.
- **Formats:** at least 40% of items use real-world syntaxes or public-domain document text that is absent from C2's
  format pool. Examples: IAM-style JSON, RBAC YAML, real robots files, ERP exports, messy email threads. Federal
  Register, eCFR and EDGAR text are excluded as OHS-adjacent.
- **Verification:** solver A = solver B on 100%. A Haiku blind read only flags items, and flagged ambiguous items are
  dropped.
- **Overlap report:** a structure-hash overlap with C2 is reported as counts only.

**Part U:** the same verification as R. Report-only.

**Part X:** checked by program against eval_opi and jagged wording. Gold is unchanged by the attack. Scored as attack
success.

### 8.4 Decontamination exports
- **The exports:** hashed 10-grams and 12-grams, exact full-text and sentence hashes, R and U structure hashes, and a
  keyword block-list.
- **Applied by program:** the C2 QC program applies the exports to every C2 Haiku pool, candidate and the final mix.
  Builders never see them.
- **Sealed-side child:** a counts-only process run by the orchestrator, like A25 d. It runs exact, substring, 10-gram,
  8-gram rule, MinHash, cosine and G-TPL checks of C2 against OHS-4.
- **On any hit:** the C2 unit or template is dropped, never an OHS-4 item.

### 8.5 Scoring and looks
- **Output:** the scorer prints aggregates only: per part, slice, domain and question type. It reports accuracy,
  complement violation, minimal-edit consistency, Brier (mixdev T), option-order drift and the B3 yes-share alarm.
- **Per-item failures:** nobody inspects them.
- **Paired bootstrap:** 10,000 resamples, seed 0, over group_id.
- **Allowed looks:**
  - **L1:** C1 + C2 in the same job, or C1 alone if the pre-gate failed.
  - **J:** Jev once, after L1's verdict is logged.
  - The look log refuses every other look.
- **SPEED-3 is measured at L1 and J:**
  - S1 pinned to a US region;
  - p50, p95 and p99 at concurrency 1, 16 and 64;
  - $/1K at 40% use;
  - Jev latency from the same US client.

### 8.6 Claims against Jev (pre-registered; report-only)
- **"Beats Jev on rule/agent decisions":** C2 − Jev on part R has LB > 0 in **both** pinned Jev runs.
- **"Also on unseen kinds":** part U LB > 0.
- **"More consistent" / "better calibrated":** the CI of the difference excludes 0 in C2's favour, per part.
- **"Close to Jev on general":** only if the 95% CI of C2 − Jev on G includes −2 pp or better. Otherwise the gap is
  reported with its CI.
- **Speed:** p50/p95 at the stated concurrency.
- **Cost:** stated honestly at 40% use (no win expected at 40%).
- No JevBench submission and no general-win claim without the owner.

---

## 9. Training recipe and cost

### 9.1 Recipe (round 1's code path; no new trainer code)

| Item | Value |
|---|---|
| Start | Continue C1's LoRA through `init_adapter` (q35_4b_main500k, 507d1c29...; base Qwen3.5-4B @ 851bf6e8) |
| LoRA | r16, alpha 32, dropout 0.05, QWEN35 targets, `expect_trainable` 32,464,896 |
| Optimiser | AdamW, weight decay 0, clip 1.0, batch 16, micro_tokens 8192 |
| Schedule | Peak LR **5e-5**, 5% linear warm-up, cosine to 0, **exactly one pass** (`epochs` = 16 / measured rows per step) |
| Losses | C1's, unchanged: CE with label smoothing 0.05 (MNLI 0.08); KD 0.5 only through the C1 anchor on replay; complement / equiv at lam 1.0 with sym_cons; lam_inv 1.0; perm_twin 0.3 with lam_p 0.5; `lam_ord` 1.0 only on replay ordinal rows after G18; beta 0 |
| Labels | Hard 0/1 on every new row |
| Seed | New, fixed in A37 |
| Prompt | cygnet + schema_branch_mark; rendered-prompt sha identical across trainer, gate and server |
| Snapshots | 25 / 50 / 75%: monitors only, read on od-l4. Old slice, P(yes), mixdev (report-only) and KL(C1‖C2) on 2,000 new rows. Never candidates; never read on OHS-4, transfer dev or the gate dev splits |

### 9.2 Size and cost (H100 at $4.09/h)
- Rows: ≤ 66,500. At about 16.2 rows/step (round 1), that is about 4,100 steps, with about 205 warm-up steps.

| Case | s/step | Hours | Training $ | + smoke and overhead | Total |
|---|---|---|---|---|---|
| Expected (new-row mean ≤ 800 tokens; replay about 620-742; A28 model 0.163 ms per padded token) | 2.8-3.2 | 3.2-3.6 | $13-15 | $2 | **$15-17** |
| Pessimistic (round 1's measured 3.716 s/step) | 3.72 | 4.2 | $17.3 | $2 | $19.3, so the 5.5 trim brings it to ≤ $17 (about 58K rows) |

**Other GPU and API spend**

| Item | Where | Cost |
|---|---|---|
| C1-only crowd read (about 40K candidates; SGLang about 124K rows/h) | mahadikarya3 or free od-l4 | ≈ $1.5 or $0 |
| Dev pre-gate, mixdev, transfer and snapshot reads | od-l4 (Google credit) | $0 Modal |
| OHS-4 look (C1 + C2) + SPEED-3 load test | mahadikarya3, US region | ≈ $2-3 |
| Jev read (about 6.5K calls × 2 runs) | OpenRouter | ≈ $0.5-1 (check the balance first) |

**Total C2 Modal:** about $19-22 expected, ≤ $25 pessimistic, capped at $30.

**Free credit:** mahadikarya2 has about $19 and mahadikarya3 about $13 after SPEED-2. No card is used without the
owner's word.

---

## 10. Timeline, Claude usage, risks and stop rules

### 10.1 Timeline (about 9-10 days after the owner's GO on A37)

| Day | Dates | Work |
|---|---|---|
| D0 | Tue 13 - Wed 14 Oct | A37 + owner GO. Write the OHS-4 brief; launch the sealed session |
| D0-D2 | 14-16 Oct | **OHS-4 built and frozen (A38).** In parallel, code only (no pools, no rows): `c2_kit`, linters, G5-H harness, `c2_select`, `mix_c2`, `gate_c2`, `snap_monitor_c2`; 17 G0-lite specs |
| D2-D4 | 16-18 Oct | Haiku pools: packs, lexicons, skins, wordings, T37b drafts. G13-seed batch #1 overnight. Wave-1 plugins; T37b builder; transfer-dev plugins |
| D4-D6 | 18-20 Oct (weekly reset Mon 19 Oct 07:00 UTC) | Wave-1 pilots, then at most 2 fixes, then full 1.5× generation and gates. Wave-2 plugins and pilots. Carry-over re-gates. Mixdev and transfer dev frozen |
| **D6 = data cutoff** | Tue 20 Oct 23:59 UTC | Families that have passed every gate enter. No waiting |
| D6-D7 | 20-21 Oct | G13 batch #2 (candidates) overnight; crowd read (GO); selection; G9 re-read; replay draw; `mix_c2`; G13 #3 (new targets); preflight; smoke run ($0.5) |
| D7-D8 | 21-22 Oct | Owner GO, then training (3.2-4.2 h) with snapshot monitors |
| D8-D9 | 22-23 Oct | Merge, parity, dev pre-gate, verdict. OHS-4 look L1 (GO). Jev read J (GO). SPEED-3 numbers. Report |

### 10.2 Claude usage plan (two weekly windows; throttle as in A29)
- **Rules:** pause new lanes at 90% of weekly usage, and never cross 97%. Claude writes code, semantics tables and
  adjudications. Haiku does every bulk text task and every blind read.

| Work | Claude, % of one week |
|---|---|
| A37, the OHS-4 brief, orchestration | 4 |
| OHS-4 sealed session | 10-12 |
| `c2_kit`, linters, harness, select / mix / gate / snap copies (plus one independent review) | 10 |
| 17 G0-lite specs + ambiguity resolution | 5 |
| 17 plugins (about 0.8% each) + T37b + 4 transfer plugins | 17 |
| Pilot fixes, G5-H adjudication, G13 fixes | 7 |
| Mix, preflight, training watch, gate, look, report | 5 |
| **Total** | **≈ 58-60%**, about 25% before the reset and 35% after |

- **Haiku:** about 1,150 agent tasks of at most 50 items each:

| Task | Haiku tasks |
|---|---|
| Packs | 60 |
| Lexicon | 45 |
| Skins and templates | 330 |
| Wordings | 20 |
| Free-form documents | 150 |
| G3-H extraction | 120 |
| G5-H dual reads | 210 |
| Free-form single reads | 100 |
| T37b writing and polarity | 80 |
| OHS-4 flags | 40 |

  Measure the weekly-usage cost after the first 50 tasks and re-plan if Haiku would exceed 10% of a week.
- **If usage runs short:** cut wave 2 in this order: T25, T12, T15, T24, T31, T07, T32. Never cut T28, T33, T29 or
  T37b, and never cut a gate.

### 10.3 Top risks

| # | Risk | Evidence | Mitigation | Residual |
|---|---|---|---|---|
| 1 | One-pass readout ceiling on rule items | C1 is at about 73 on pg_dev and hard_dev after training on them; F2's 0.24 vs 0.67 | ≤ 2 unstated operations, printed intermediates, short rows, depth report; pre-gate (a) catches no-learning | High |
| 2 | In-family gains don't transfer (style or format match) | Round 1: sealed +0.9 | Independent OHS-4 R wording (not Haiku), real-world syntaxes, held-out families; claims only from OHS-4 | High |
| 3 | General regression | Round 1 dev −0.38 | 60% replay + C1 anchor; NI rule S2 (passes 59% at a true −0.4) | Medium |
| 4 | Snapshot stop fires (about $9 lost, no candidate) | Round 1 −1.40 vs the −1.5 bar at 50% | Same LR and replay share as round 1 (the dip tracked LR, not run length); stop at both reads | Medium |
| 5 | Haiku adds facts or leaks the answer | — | Mode-T majority; G-SL fact-lock; G3-H; G6/G7 on the free-form slice; G5-H | Low-medium |
| 6 | Late decontamination hits kill families | A31: F4 hit; F9 kept 742/6,005 | G13-seed on every Haiku pool before rows; per-template quarantine | Low-medium |
| 7 | T37b complement label noise | Subtle predicates | Binary-predicate sources only, program polarity, 2/2 judgements, blind solver, drop any doubt, 2,000 cap | Low-medium |
| 8 | OHS-4 general sources hard to find (8-10 fresh, licensed, unused) | OHS-3 used many | Built first; if fewer than 2,400 items, A38 records the n and the power before any C2 data; never relaxed afterwards | Medium |
| 9 | Over-asking (T29, T30) or over-refusal (T26, T27) | — | Balanced shares, controls, over-ask report, D6 | Low |
| 10 | Claude weekly limit | Round 1 ran at 93-99% | Haiku bulk, 2-page specs, waves, cut order | Medium |
| 11 | Laptop crash during G13 | 7 Oct crash | Resumable caches, niced batches | Low |
| 12 | Haiku output terms | — | Owner confirmation in A37 (c) before any training | Owner |
| 13 | Sealed spill | A15 incident | Sealed folder, no item text in tool results, 12-gram re-scan | Low |

### 10.4 Stop rules (pre-registered)
- **Data:** a family that fails after 2 fix iterations is cut. Fewer than 5 of the 6 agent-core families, or fewer than
  10 program families, at the cutoff means **stop and report, no training**.
- **Usage:** at 90% weekly, no new lane steps; never cross 97%.
- **Money:** a pre-launch projection above $17 means trim (5.5). A projection above $17 at steps 100-300 means stop and
  ask. The C2 Modal cap is $30.
- **Training:** abort on a non-finite loss term. Alert when the gradient norm is above 5× its 200-step median for 20
  steps. Stop if the old slice is below C1 − 1.5 pp at both the 25% and 50% snapshots, or if P(yes) drifts by more than
  0.02. A stopped run gives no candidate.
- **Evaluation:** a failed pre-gate means no C2 look on OHS-4. Every look is single, and the scorer refuses repeats.

---

## 11. Round-1 lessons applied

| # | Round-1 lesson | Evidence | C2 change |
|---|---|---|---|
| 1 | Synthetic invented-domain rows barely move real text | Sealed +0.90 / +0.11 | No general-gain promise. The claim moves to a rule/agent slice (S1) with general non-inferiority (S2). T37b and F11 are the only real-text levers |
| 2 | Only 3 of 14 sources entered | A26-A34; 20,653 G0-spec lines; 5-7 review rounds | One shared kit, one-page specs with one review, pilot-first QC, at most 2 fixes, waves, a cutoff that never waits |
| 3 | Late G13 seed and wording hits | A31 (F4); 7 Oct batch: F9 742/6,005, F5 2,295/5,252 | G13-seed on every Haiku pool before any row; per-template quarantine; synthetic statutes only |
| 4 | Near-miss G6/G7/G10 failures (F1, F2, F8, public builders) | QC reports; A29 | Balance by construction: display drawn before gold, named-error distractors, the same skin for both labels, identical cue vocabulary; G6/G7 on the pilot |
| 5 | Public data failed G5/G6, and decontamination removed thousands of records | A29; 2,914 formats-2 records removed | No new public datasets; D2's new X1 codebooks are refuted (Appendix B) |
| 6 | Complement violation 0.170 vs Jev 0.088 | OHS-3 | Overlay in every family (≥ 20% of yes/no rows), non-syntactic complements, T37b, and a ship rule (S3) |
| 7 | Brier 0.172 vs 0.150 | OHS-3 | Hard labels, abstain options wrong on ≥ 50% of rows showing them, T fit on mixdev, Brier gates (D4, S4) |
| 8 | Old-slice dip near the stop line | −1.85 / −1.40 / −1.25 | Keep LR 5e-5, 60% replay and the anchor; same stop rule; fix the snap_monitor pgrep bug (new copy) |
| 9 | Cost driven by long rows (A28: $48-54 projected for 150K) | A28; 3.716 s/step | Rows ≤ 2,000 tokens, mean ≤ 800; trim to one free account |
| 10 | Haiku is a weak general labeller but reads rule items well | TEACH-0 | Haiku authors and flags only; programs label |
| 11 | OHS-3 is spent | ROUND1_RESULTS | Fresh OHS-4 built first by an isolated session, also serving SPEED-3: one build, one look, one Jev read |
| 12 | The 3-model crowd was slow and costly | A17 crowd about $15 | C1-only crowd on S1 or the free L4 |
| 13 | Isolation spill (A15) | A15 disclosure | Sealed folder rules and a re-scan |

---

## Appendix A. Merge decisions (conflicts resolved)

| Topic | D1 | D2 | D3 | Decision | Why |
|---|---|---|---|---|---|
| Total rows | 60K | 100K | 72.5K | **≤ 66.5K**, trimmed to ≤ $17 | Fits one free account; 2.5× round 1's rows; 100K exceeds the free credit (about $27-31) with no evidence that volume transfers |
| Replay share | ≥ 50% (53%) | 55% | 60% | **60%** (floor(1.5 × new)) | Round 1 at 60% came within 0.10 pp of the stop rule. It is the existing tested mixer guard (A33) |
| Peak LR | 5e-5 | 5e-5 | 4e-5 | **5e-5** | 2/3 designs, and it is tested. Round-1 snapshots show the dip tracks instantaneous LR (largest at 25%, shrinking after), not run length, so the same LR and replay share predict a similar dip. 4e-5 would add an untested learning cost |
| Old-slice stop | −1.5 | −2.5 + dev-monitor stop | −1.5 | **−1.5 at both 25% and 50%** | 2/3. D2's loosening is post hoc, and its dev-monitor read breaks recipe 5 |
| Crowd | C1 + base 4B | C1 only | C1 only | **C1 only** | 2/3; cheaper; bins unchanged |
| T35 | Train (700) | Hold out | Train (800) | **Train 600, inside the T28 plugin** | 2/3 train it. Transfer is covered by T36 |
| T07 | Train | Train | Hold out | **Train 800 (wave 2)** | 2/3. It is the main free-form realism family |
| T19 | Train (wave 2) | Hold out | Hold out | **Hold out** | 2/3 |
| T21 | Hold out | Train | Drop | **Hold out** | The middle position: adds legal-style transfer at no training cost |
| T20 | Hold out | Drop | Train | **Hold out** | Same reasoning; overlaps F7 and F11 |
| T05 | Train | Drop | Drop | **Drop** | 2/3; OHS-adjacent (openFDA recalls); world knowledge |
| T16 | Fold into T01 | Merge with T01 | Separate (800) | **Fold into T01 S6** | 2/3; F2 covers business days |
| T02 | Fold into T01 S4 | Drop | Fold into T01 S4 | **T01 S4** | 2/3 |
| T23 / T24 | Separate | Merged | Separate | **Separate families, one interpreter** | 2/3; T23 keeps only the transition and anchor parts F1 lacks (D2 + D3) |
| Consistency block | Overlay + T37b on real text | Overlay + 2,800-row synthetic T37 | Overlay only | **Overlay (all) + T37b 2,000 + D2's antonym/option-framing forms as an overlay rule (≥ 30% of pairs)** | 2/3 want a block. Real text is the measured gap. D2's surface variety is kept without extra rows |
| Complement share | ≥ 15% | ≥ 25% | ≥ 15% | **≥ 20% of yes/no rows** | Above the D1/D3 floor; below D2 to keep units ≤ 3 rows |
| Carry-over | F5, F6, F3, F11, F4 | F11, F6, F4, F5 | F5, F12 | **F5 + conditional F6, F11, F4** | 2/3 for each kept pool. F3 (1/3) and F12 (1/3; QC fail; When2Call design) are dropped |
| Rows per card | ≤ 64 | ≤ 64 | ≤ 128 | **≤ 64** | 2/3; Super-NI plateau |
| G5 reader | Haiku blind solve + Claude 150 audit | Haiku dual read + Claude adjudicates | Haiku 300 + Claude trace review | **Haiku dual read 300/family + Claude adjudication + 30 agreed rows** | Merges all three; the bar is unchanged |
| Pilot size | 5K QC sample | 1,000 | 500 | **1,000 pilot, then the 5K G6 sample at full** | Spec G6 needs 5K; a pilot catches cues early |
| Free-form share | 20-30% | 0% (slot-locked) | about 20% | **≤ 25% (T07/T32 ≤ 40%)** | 2/3 allow free-form; fact-lock + G3-H required |
| OHS-4 R wording | Sealed agent + its Haiku workers | No Haiku | Not stated | **Sealed Claude, no Haiku authoring** | Avoids style match with C2's Haiku text |
| OHS-4 sizes | G 2,400, R 1,600 | G ≥ 3,000, R ≥ 2,000 | G 2,000, R 1,500, U 600 | **G 3,000, R 1,600, U 600, X 300** | n for S2 power (D2); U from D3 |
| General ship rule | LB > −1.5 and point ≥ −0.5 | LB > −2.0 | Fail if point < −1 and UB < 0 | **LB > −1.5 at n ≈ 3,000** | SE ≈ 0.50 makes this 85% at a true 0. −2.0 would pass a 1 pp loss half the time, against the "close to Jev" goal |
| R ship threshold | +5 | +3 | +5 | **+5 and LB > 0** | 2/3 |
| Transfer pre-gate | Gate (+3, LB > 0) | Gate (+3, LB > 0) | Report-only | **Gate** | 2/3 |
| Merged parity bar | 99.5% | 99.9% | 99.9% | **99.5% on SGLang S1** | S1 measured 99.77% (A35); 99.9% would block the adopted serving path |
| Temperature bound | [0.8, 1.3] | [0.8, 1.5] | [0.8, 1.3] | **[0.8, 1.3]** | Recipe 6.0; 2/3 |
| `lam_ord` | 1.0 on replay ordinal | 0 | 1.0 on replay ordinal | **1.0 on replay ordinal rows** | 2/3; the tested round-1 path |
| Replay quota | n^0.7 | n^0.6 | n^0.7 | **n^0.7** | `replay_sample.py` unchanged; no evidence for 0.6 |
| Refill when families are cut | None | Up to 1.3× | None | **None** | A34 (c): no tested balance-keeping refill |

## Appendix B. Claims refuted or not adopted

1. **"Haiku 98.9 on the rule splits shows these skills are learnable by a 4B" (all three designs, as motivation).**
   Refuted as stated.
   - n = 278, and A36 notes hard_dev and pg_dev may be LLM-authored, which advantages Claude.
   - C1 already trained on the pg_* and hard_* train splits and still scores about 73.
   - It shows the items are determinate, not learnable. Hence risk 1 and the depth caps.
2. **D2: new X1 real-text codebooks on MAMS, XED and EDOS (3,000 rows).** Not adopted.
   - A29: public-3 failed G6 on MAMS and EDOS (and G5 on GHC).
   - The 7-8 Oct G13 wording fixes removed 2,914 EDOS, GHC, MAMS and XED formats records.
   - The already-QC-passed F11 real-text rows are the cheaper way to get this skill.
3. **D2: relax the old-slice stop to −2.5 and add a dev-monitor stop on the gate dev splits.** Refuted.
   - Recipe 5 forbids snapshot reads on the dev gate splits.
   - The loosening was chosen after seeing round 1's numbers.
4. **D3: an A15 sealed part-A aggregate as a report-only guard.** Refuted. The A15 S1 and C looks are spent, and its
   frozen scorer refuses looks outside recipe 6.2.
5. **D1: old slice ≥ C1 − 1.5 as a pre-gate.** Refuted. Recipe 5 says the old slice is a monitor and stop rule only,
   never a ship rule (it measures memorised rows).
6. **D1: G8-H text-only gold predictor as a new gate.** Redundant. It equals G6 baseline (c), "card without question".
   C2 runs G6 separately on the free-form slice.
7. **Round-1 speed figures.**
   - D1's "4.6 s/step" is A28's pre-run estimate for the 150K mix.
   - D3's "about 4.4 s/step" is not in the logs.
   - **The measured value is 3.716 s/step** (steps 100-300), with 1,650 steps and $8.4 all-in.
8. **D2: merged-model parity ≥ 99.9% on the served path.** This would fail the adopted S1 (99.77%, A35). The served-path
   bar is 99.5%.
9. **D2: about 6,000 steps "because round 1 trained too little".** No evidence that more steps transfer to real text.
   It costs about $27-31, more than one free account, and raises the drift risk. Not adopted.
10. **D3: F12 tool-selection carry-over.** Not adopted. F12's QC is pass=false, its design copies When2Call (a DI test),
    and T28 and T29 cover the agent skill.
11. **T22 and CUAD headings for T21.** CUAD, MAUD and ContractNLI are on the LICENCE_REGISTER §5 deny-list. T21 (dev
    only) uses fully synthetic contracts.
12. **Any cost-win claim at 40% use.** S1 costs $0.079 vs Jev's $0.061 at 40%. It wins only above about 55% use, so
    the report states it that way.
