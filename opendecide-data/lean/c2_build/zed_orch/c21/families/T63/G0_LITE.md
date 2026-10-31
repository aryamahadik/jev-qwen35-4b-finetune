# G0-LITE T63 DEP-RISK + EXISTS head + licence head + malicious-manifest slice (lane L-P; P1 wave A; clean-room; draft for Opus approval, target Mon 19 Oct 2026)

Author: Sonnet 5.5 high (L-P G0-lite writer), Sun 18 Oct 2026. Design only: no rows, no generator code, no download, no execution, no model call, no Modal.
Status: DRAFT 1. Every number below is a design value fixed BEFORE any pilot; changing one after a pilot is a gate edit and needs Opus.
Read for this file: PLAN_TRAINING_SIDE.md (sections 1 C, 2, 5, 8, 16 incl. 16.1, 16.3, 16.4, 16.9), LANE_L-P.md, excerpts/codeexec_s5.md, families/T50/G0_LITE.md (format, SLT tables), families/G0_APPROVALS_v32.md (GV1-GV9), families/G0_APPROVALS.md header, families/T42c G0-lite and addendum (execution-family format), families/LR/G0_LITE.md (rows LR-04, LR-B5 text), C2_1_PUBLIC_TRAIN_INVENTORY.md (A16, section 4 T63 row), l0/NAMES_MANIFEST_V1_1.json (structure only). NOT opened: any path containing "ohs" or "sealed", C2_1_PLAN_v3.md, any plan SKEPTIC file, OHS5_BRIEF_DRAFT.md, any generator, wording pool, benchmark item text, any dataset file (DataDog or other), mutate.py, ~/.claude. Dataset field names that appear below come from memory and are marked UNVERIFIED; the L-R licence / record step confirms them.
Shared rulings carried (index; full text in families/G0_APPROVALS.md and G0_APPROVALS_v32.md): G1 solver B is CODE; G2 data-audit gates are PRE-FREEZE; G3 no free pilot tuning, ONE combined fix; G4 no head or sub-block rolls alone; G5 one probe harness (grouped split, L2 logistic regression, AUC as max(AUC, 1 - AUC), 97.5th-percentile bound over 2,000 cluster-bootstrap resamples, balanced accuracy for k-way, permutation check 0.50 +- 0.03, injected-leak power check >= 0.80, GBT advisory); G6 tokens (mean <= 800, none > 1,536, > 1,024 on <= 10%); G7 secondary heads are head rows (T63 builds none, section 1); G8 shared host list (not used: T63 rows have no URLs); G9 cross-family label consistency (T63 labels FACTS, not permissions: section 1 and K19); G10 decision_spans (no natural-language user utterance in T63: nothing to export, recorded for the conformance map); GV1-GV4 (A10 / A14 not carried, section 3.6; GV4 binds: every trained row <= 1,536 tokens); GV5 (a G13 hit retires the spec and the whole group); GV6 (no text-perturbation rows in L-P); GV7 (dialect rows are L-A only); GV8 (pilot-pooled sub-block probes allowed on the pilot for equal k; the built-family read binds); GV9 (held-out dev rows: T63 has none outside the size).

## 0. One-paragraph summary

T63 teaches the 4B to answer supply-chain FACT questions about dependencies, with every label fixed by a program or a hashed table: (NEAR) is the proposed package a lookalike or cross-registry confusion of an established package shown in a registry snapshot; (EXISTS) does package P exist in registry snapshot R, and does symbol S exist in library version V or in a pinned toolchain's standard library; (LIC) is dependency licence A compatible with project licence B for a stated usage and distribution mode (Opus-written table over SPDX identifiers only); (MAL) a realism slice: is this package record malicious, with positives from the DataDog labels/metadata (via L-R, never payloads) and negatives built by T63. The family never labels a permission (ALLOW / ASK / BLOCK stays with T50 R14 and R12), so it cannot contradict T50. Third-party package names in generated rows are seeded-namespace names or standard-library names only; real third-party names appear only in the DataDog positives (P1-realism exemption, Sk 8) and are handled by the swap-or-exception rule of section 3.5.

## 1. Decision and label set

| Head | Question form id | Rows (generated) | Labels | Gold |
|---|---|---|---|---|
| NEAR typosquat / cross-registry near-miss | T63-Q-NEAR | 500 | YES (lookalike or confusion of an established package in the shown snapshot) / NO | program function of the snapshot record (section 2.1) |
| EXISTS | T63-Q-EXISTS | 500 (EX-A 250, EX-B 250) | YES (exists) / NO | membership in an offline snapshot of seeded names, a seeded library-version export list, or the stdlib symbol export of a pinned toolchain image (section 2.2) |
| LIC licence compatibility | T63-Q-LIC | 200 | COMPATIBLE / REVIEW / INCOMPATIBLE (letters shuffled per row) | lookup in the Opus-written licence table (section 2.3) |
| MAL malicious-manifest slice (P1-realism, via L-R LR-04) | T63-Q-MAL | 1,000 if built (500 DataDog positives + 500 T63 negatives) [Opus b1b T63-M5]; built only if the T63-M3 learnability precondition holds | YES (malicious) / NO | positives: the dataset's own human-triaged label; negatives: benign by construction (section 2.4) |

Total trained rows: 1,200 generated (NEAR, EXISTS, LIC) + MAL 1,000 if built (T63-M3, T63-M5) = 2,200, else 1,200 [Opus b1b]. Binary heads shuffle the option order per row; 20% extra order-invariance copies are mix-level and not counted below.
T63 builds NO secondary head (G7): a transformation-class head would draw from at most 25% of 250 YES specs (about 62 rows), too few to bar; not built (recorded so Opus sees the choice).
Label semantics are facts about the shown evidence. The product maps them to actions elsewhere. K19 asserts that no T63 question form offers ALLOW / ASK / BLOCK options. Where a T50 install spec and a T63 NEAR row describe the same package, T50's label stands for the permission and T63's label answers the fact question; they are different question forms, so G9 does not apply (flagged O-T63-5 for confirmation).

## 2. Gold method; solver A and independent solver B

### 2.1 NEAR gold (program over the snapshot record)

Snapshot record (all names seeded, TRAINING salt): registries R1..R3 (each with a seeded host and an ecosystem word: pip, npm, cargo or go; no real registry brand), entries {name, registry, publisher handle (seeded), age class A0 < 30 days / A1 < 1 year / A2 1-4 years / A3 > 4 years, downloads class D0 low / D1 mid / D2 high, fork_of (optional edge)}. Established = age class >= A2 AND downloads class D2.
A card slot `reserved_internal_namespaces` (policy card card.t63.registry_resolve) lists names the project reserves on its internal registry; `resolve_order` states which registry a bare install resolves from first.
Query: package P at registry R is proposed. Relations (registry ids NM-T1..NM-T8): T1 single-character omission; T2 insertion; T3 substitution by a keyboard neighbour; T4 adjacent transposition; T5 separator change among hyphen, underscore, dot, none; T6 ASCII look-alike swap (rn/m, l/1, O/0; NO Unicode confusables in T63, so no overlap with the trained text perturbations); T7 scope or namespace change (org-scoped vs bare name); T8 cross-registry confusion (same name on a different registry where the card reserves it for another registry or resolve order puts the public registry first).
LOOKALIKE (label YES) iff there exists an established entry Q with rel(P, Q) in NM-T1..NM-T7 AND publisher(P) != publisher(Q) AND no fork_of / same-org edge links P and Q AND age(P) < age(Q) (P is newer than Q, compared on the shown age classes; the same class is NOT newer).
[Opus b1b T63-M1] T8 CROSS-REGISTRY CONFUSION is its own first-match clause (the "established Q" and age conditions do NOT apply: an internal reserved package need not be public or old): a T8-shaped query is YES iff (i) P's name is listed in the card's `reserved_internal_namespaces`, (ii) the query's registry R is not the internal registry the card reserves the name for, (iii) a bare install of the name resolves to R under the card's `resolve_order` (public first) or the install names R explicitly, and (iv) publisher(P) is not the project's own org handle shown on the card; otherwise NO. Solvers A and B implement this clause separately from NM-T1..NM-T7; K13 counts T8 YES rows inside the NM-T quota as before.
Else NO. NO rows are built to carry near relations on purpose (design rule, K5): relation kinds NM-R1 old-legit (P is the older established side of a near pair; the squat is the OTHER row of the pair), NM-R2 declared sibling (same publisher or fork_of edge), NM-R3 near name but P also established with age(P) >= age(Q) (two long-lived packages), NM-R4 unrelated (no near entry, at most 8% of NO rows). At least 92% of NO rows carry NM-R1..NM-R3 (so "a near name exists" is not a cue).
The snapshot record states the decisive fields in the shown table (publisher, age class, downloads class, fork_of when present). Nothing outside the shown record is needed.
Solver A = forward function over the spec. Solver B = a program written by a separate Sonnet high session from THIS file and the row schema only: it parses the RENDERED snapshot table and query, recomputes the relation test with its own implementation of NM-T1..NM-T8, then applies the age / publisher / edge rules. Agreement required on 100% of kept rows; disagreement drops the row (counted); a block with > 2% dropped goes back to the generator.

### 2.2 EXISTS gold

EX-A (seeded, snapshot visible, 250 rows: YES 125 / NO 125): (EX-A1, 140 rows) "does package P exist in registry R" with the registry INDEX shown as a listing that is COMPLETE for the alphabetical range [lo, hi] and P inside that range, so absence is provable from the row; (EX-A2, 110 rows) "does symbol S exist in library L version V" with the complete export list of L at V shown. Library histories (versions, added / removed exports) are seeded program records. NO kinds (registry ids EX-N1..EX-N5): EX-N1 cross-module conflation (the name exists in another module of the same library or another library); EX-N2 cross-registry (the name exists in registry R2, not R); EX-N3 version mismatch (EX-A2 only: the symbol exists in V2, not in the shown V1, or was removed); EX-N4 one-edit near-miss of an existing name (capped at 30% of NO rows, only if K4 passes with it); EX-N5 plausible composition of two seeded name tokens (hallucination-style).
EX-B (stdlib, 250 rows: YES 125 / NO 125): Python 3.12, Node 24 built-in modules, Go 1.26 standard library, each from the SYMBOL EXPORT written at image build by the L-0 image record (public names only: Python names without a leading underscore from each module's namespace after `python -I` import on the pinned Linux image; Node built-in module exports; Go exported identifiers). The question says "in the pinned toolchain image", so platform-conditional names cannot be mislabelled. Language split 150 / 50 / 50. Two views, half each: EX-B1 visible-list view (the module's export list, up to 40 names, complete for the module or for an alphabetical range, is shown) and EX-B2 knowledge view (no list; the model must know). NO kinds: EX-N1 (a real name that exists in a sibling module; natural-looking by construction), EX-N5, EX-N4 (capped). Gold = membership in the hashed export file. No claim about other versions or platforms.
Solver A = membership in the spec's source (snapshot, library history, export file). Solver B = program that recomputes membership from the RENDERED listing (EX-A, EX-B1) or from the hashed export file (EX-B2) with its own parser. 100% agreement.

### 2.3 LIC gold (Opus-written table)

The table `T63-LIC-TABLE` is written by Opus 5.5 high (LANE_L-P: licence-ID table owner), hashed before any LIC row exists, and keyed on four axes: dependency licence id (about 16 SPDX identifiers: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, CC0-1.0, Unlicense, MPL-2.0, LGPL-2.1-only, LGPL-3.0-only, GPL-2.0-only, GPL-3.0-only, AGPL-3.0-only, CC-BY-4.0, CC-BY-NC-4.0, a proprietary / no-assertion marker), project licence id (about 8 of the same set), usage mode LC-USE-1..5 (vendored source copy, static link, dynamic link, separate process, dev-time tool only), distribution LC-DIST-1..3 (distributed to others, internal only, offered as a network service). Cell value COMPATIBLE / REVIEW / INCOMPATIBLE plus a one-line rationale column that never quotes licence text (identifiers only, no SPDX text copied). REVIEW is the safe label for contested or condition-dependent cells. The table is policy gold for a coding agent, not legal advice; the report says so. Each cell is used by at most one row. Solver A = table lookup from the spec. Solver B = program that re-reads the four axes from the RENDERED licence card and looks up the same hashed table; agreement 100%.

### 2.4 MAL gold (L-R slice; contract for LR-04)

Positives: DataDog malicious-software-packages-dataset, labels / manifests / metadata ONLY (Apache-2.0 quote in the inventory), human-triaged per the publisher (UNVERIFIED claim). Payload ZIPs are never opened or executed; the mapper's file-access log must show reads only under the label / manifest / metadata paths (K11a). Negatives: T63 generator rows, benign by construction, in the SAME field schema as the positives (the record lists every field read). Negative generation is conditional: field marginals (ecosystem word, name length bucket, version pattern, field count, description present, script-hook present, dependency count bucket) are matched to the positives' empirical marginals by stratified sampling BEFORE the probe is run (a stated design step, not tuning on probe numbers). Where a positive's label depends on its real name (a typosquat of a real package), the mapper swaps BOTH names through the training namespace keeping the program-recognised relation (NM-T1..NM-T8), so the label survives; where no relation is recognised and the label rests on the real name, the row carries the recorded T63-gate exception "real package name, label depends on it" (counted, reported). Solver A = the mapper's provenance record (positive) or generator spec (negative). Solver B = a program that re-derives class membership from the source record id (positives) or the generator seed (negatives) and checks the swap kept the relation; 100% agreement, no LLM reads.
[Opus b1b T63-M3] MAL LEARNABILITY PRECONDITION (decided on the MEASURED LR-04 field record, before any mapper code reads data; CPU, no rows): the builder lists every field the label / manifest / metadata files carry and declares which rendered fields bear on maliciousness by their meaning (the SIGNAL list) and shows, from the schema and the generator spec, that a benign negative can carry each signal field at the positives' marginal rate WITHOUT copying a positive. Opus confirms the list in the LR-04 recast-table batch; it is hashed before mapping. (a) If the record carries only ecosystem, package name, version, category and date fields (no signal field outside the payload ZIPs), the MAL slice is NOT built in C2.1 (left out as a dataset, logged with the field list; C2.2 item: benign negatives drawn from a licensed public registry index, not seeded), because after the name swap (Sk 8) and under K3, K4 and K11(e) no visible field could carry the label and 1,000 rows of an unlearnable label teach noise. (b) If built: K11(e) binds on every field NOT on the signal list; a "relation-present" parity (a shown near-name of an established package) holds across labels as in K5; exception rows (real names) stay subject to K4 and are dropped first if K4 fails, as written.
[Opus b1b T63-M5, O-T63-1] Size if built: 500 DataDog positives (the LR-04 cap counts dataset rows, LR-01 "300 + 300 twins" precedent) + 500 T63 negatives = 1,000 rows, balanced 50% (K11(b)), counted in T63 outside the 1,200, shed with the P1 realism slices (money shed step 6).

## 3. Inputs, carriers, generator design

3.1 Input view: there are no user messages or tool calls in T63 (single-view family; recorded so the per-family view requirement is met). Carriers (names in section 9): SNAPSHOT table (rendered through the existing TBL-* formats so the table format is not a cue), QUERY line, REGISTRY_INDEX listing, LIB_EXPORTS listing, MODULE_EXPORTS listing, CODE_LINE (one or two lines of application-style code that use the name; carried by SRC_FILE), MANIFEST_RECORD, LICENCE_CARD, QUESTION_FORM.
3.2 Application-style framing: each row is a short dependency-review situation in an application-style project (domains as the T42c list). The code line and manifest line use only seeded names and stdlib names.
3.3 Generator: spec -> render -> validate by parse (the snapshot table re-parses to the spec; the listing re-parses to the export set). Rows are written only through the stamp wrapper (section 6).
3.4 Splits: dev = 10% of GROUPS (a group = one snapshot, or one library history, or one licence-axis block); a group is wholly dev or wholly train (K15). All rows of one snapshot share a split.
3.5 MAL slice rules (LR-B5 carried): the combined slice (positives + negatives) is the unit for R7 balance and for the name-shape probe; exception rows <= 20% of positives; if the K11 probe fails WITH the exception rows, they are dropped first (the slice then shrinks; logged); if it still fails, the slice is left out as a DATASET (an L-R decision under rules 3 and 6, not a T63 family roll; flagged O-T63-3 because G4 says heads do not roll alone). The mapper never reads a name list from the payloads.
3.6 Levers: A10, A12, A14, A15, A16 are NOT carried by L-P (the build order assigns them to L-A, L-I, L-T, L-C, L-K; GV7 for A15). An extension is an orchestrator ruling before the Thu 22 hash export. A1 / A2 hooks are carried: every row records template id, wording id and construction id (NM-T*, EX-N*, LC cell id) for the L-0 gold-bug audit and the AFLite-style repair.

## 4. Sizes and shares (rows before drops; quotas counted AFTER drops, every quota cell oversampled by 15% at generation, fixed now)

| Block | Rows | Labels | Notes |
|---|---|---|---|
| NEAR | 500 | YES 250 / NO 250 | YES transformations NM-T1..NM-T8 each 5-25% of YES; NO kinds NM-R1..NM-R4 as section 2.1; >= 50% of rows in a pair (squat and original asked in the same snapshot, or the squat and its one-edit non-near twin); query registry spread over R1..R3 |
| EXISTS EX-A | 250 | YES 125 / NO 125 | EX-A1 140, EX-A2 110 |
| EXISTS EX-B | 250 | YES 125 / NO 125 | Python 150, Node 50, Go 50; EX-B1 visible 125, EX-B2 knowledge 125 |
| LIC | 200 | COMPATIBLE 70 / REVIEW 60 / INCOMPATIBLE 70 | >= 30% of rows in a one-axis-flip pair |
| MAL | 1,000 if built [Opus b1b T63-M5] | YES 500 / NO 500 | 500 DataDog + 500 T63 negatives; built only under T63-M3 |
| Total | 2,200 if MAL is built, else 1,200 | | trained rows; money projection counts these |
Reuse limits: <= 3 rows per snapshot / library history, <= 1 per licence cell. Age and downloads marginals of the queried package equal across NEAR labels within 5 pp per class (K13). Pilot (G3 first look) = a seeded proportional sample of 50% of each block, floor 300 rows total per block set, cap 1,000 (O-T63-6).
Token budget (G6): snapshot tables <= 14 entries per NEAR row, listings <= 40 names.

## 5. Difficulty ladder L1-L4 [CRIT D1, D2]

Mechanisms (program parameters, never from a model score). Source mechanisms from the inventory: hallucinated names that look plausible and repeat (the 43% repeat figure is secondary and UNVERIFIED; used only as the reason for M-PLAUS), cross-registry near-miss, typosquat.
| Id | Mechanism | LOW | HIGH |
|---|---|---|---|
| M-PLAUS | non-existent name that looks plausible (EXISTS NO rows) | random seeded token pair | composed from two high-frequency seeded tokens that appear in neighbouring real entries |
| M-XREG | cross-registry confusion | name differs by registry word only | reservation and resolve order interact (reserved internal name, public registry first, query on a third registry) |
| M-EDIT | edit distance of a squat | distance 1 omission | distance 2 or an NM-T6 / NM-T7 relation |
| M-SIB | legit near-pair | same publisher | fork_of edge plus a different publisher for P |
| M-VER | symbol present in another version (EX-A2) | removed 2 versions ago | present in V, removed in V+1, shown V is one before |
| M-CELL | licence cell near a boundary (LIC) | far from any REVIEW boundary | one axis from a flip |
Row level: L1 no mechanism; L2 one LOW; L3 one HIGH or two LOW; L4 two or more HIGH. Composition (set-level, PRE-FREEZE): L1 20% / L2 30% / L3 30% / L4 20% (each +- 5 pp); L3-L4 = 50% (floor 25%), per block L3-L4 >= 25%. TWIN rule: every L3 / L4 row has an easy-looking twin with the opposite label (differing in <= 1 field or <= 1 edit); twins cover >= 50% of L3-L4 rows and count inside the matched-pair share. MEASURED BAR (K21, once, on the pilot): C2 (C1 if C2 has no weights), read on od-l4b, scores <= 70% on the L4 rows. A model-based gate, so it is NOT a kill: a miss is folded into the ONE combined fix by raising HIGH settings (never by dropping rows by model score); after the fix a miss is a report line. MAL rows have no ladder (dataset gold).

## 6. CHECK AT GENERATION [OWNER-ROW] (plan 16.1; replaces the 200-row G13 pilot)

Owner, 18 Oct (binding): "If you're building one row, check that row at that same point and that's it ... then train." Every row is written to the family pool ONLY through the L-0b stamp wrapper, per batch (<= 500 rows, same day):
(a) ANSWER CHECKS per row: solver A = solver B (NEAR, EXISTS, LIC, MAL); render round-trip (the shown table / listing / card re-parses to the spec); stdlib rows: export sha and image id in the manifest; LIC rows: table sha and cell id, cell used once; names guard (K3, K18: only seeded, stdlib and fixed words; PII scrub); token rule G6 (> 1,536 refused); exact-duplicate refusal and the reuse ledger; ladder level and A1 fields recorded; MAL rows: field record present, access-log check, swap relation kept or exception recorded.
(b) G13: the batch goes to the Mac stamp service, which checks every row against every registered target with every method listed for that target (registry sha bound; R6 scaffolding exemption; OHS-5 hash-export targets use exact and hashed n-gram methods only).
(c) The stamp (row id, registry sha, method-set version, generator code sha, verdict) is written into the row manifest. A failed row is dropped and logged (row id, target name, method; never the matched text). No unstamped or failed row enters the pool.
GV5: a G13-dropped row retires its spec; the replacement is a NEW spec for the same cell with a new seed; a pair or group member's drop drops the whole pair / snapshot group. Same-skeleton regeneration stays allowed only for NON-G13 answer-check drops. Quota steering during generation uses running COUNTS only (label shares, kinds, levels), never pilot probe numbers (G3).
FIX TRIGGER (all rows): > 1% of the pilot rows (and of any full-generation day) dropped for a reason other than exempt scaffolding or OHS-5 collisions (<= 5%, row by row) = the family's ONE combined fix. A real-name collision is not expected (T63 rows are seeded or stdlib names); a stdlib name that collides with a G13 target string is a G13 drop like any other.
SET-LEVEL checks run ONCE per family, on the pilot (first look) and on the built family, never at the mix: A50 G6 at size, A49c balance, wording variety, matched-pair share, ladder and measured bar, the section 7 probes, G5-H (two Haiku solvers on 300 rows plus one Haiku read of 100% of free-form wording), G3-H, Opus A43(d). Then C2 reads on od-l4b (trap selection, A1 template audit): not a kill gate.

## 7. Gates

Probe protocol = G5 throughout (groups: snapshot / library history / licence block / source record). Class legend: PRE-FREEZE KILL = CPU or data-only, a miss after the one fix iteration rolls the family; POST-TRAINING REPORT = needs the trained model, never a kill rule.

PRE-FREEZE KILL
| ID | Gate | Bar |
|---|---|---|
| T63-K1 | Solver A = solver B on kept rows (per row at creation) | 100% of kept rows; block drop > 2% returns the block; > 5% of the pilot dropped for disagreement = the fix iteration |
| T63-K2 | Provenance: every EXISTS-B row carries image id + export sha; every snapshot / history entry is from the seeded namespace; export file hashed before any row | 100% |
| T63-K3 | No real third-party package name in generated rows: every package-like token is in {seeded names} + {stdlib exports} + {fixed words}; the shared deny-list collision check on seeded names | 0 violations; 0 deny-list hits |
| T63-K4 | Name-shape-only probe, per block: NEAR, EX-A1, EX-A2, EX-B1, EX-B2 (queried name only: length, character-class counts, hyphen / underscore / digit counts, token count, vowel ratio, character 2-3-gram TF-IDF); MAL on the COMBINED slice (name features plus field-shape features) | AUC <= 0.55, upper bound <= 0.60 each |
| T63-K5 | NEAR relation-presence probe (min edit distance to any snapshot name, near-relation flag, count of names within distance 2, snapshot size, query registry) | AUC <= 0.55, ub <= 0.60; >= 92% of NO rows carry NM-R1..NM-R3 |
| T63-K6 | NEAR metadata-only probe (queried package's age class, downloads class, publisher type, registry; no name features) | AUC <= 0.55, ub <= 0.60; age and downloads marginals equal across labels within 5 pp per class |
| T63-K7 | NEAR / EXISTS / LIC matched-pair shares | NEAR >= 50%, EXISTS >= 30%, LIC >= 30%, family >= 30% |
| T63-K8 | EXISTS surface probe with the membership feature EXCLUDED (EX-A: rank in range, list length, range width, distance to the nearest listed name; EX-B1: list length, position, module id; EX-B2: module id, name length) | AUC <= 0.55, ub <= 0.60 per sub-block (GV8: pooled across equal-k sub-blocks on the pilot, per sub-block on the built family binds). The intended-path audit (membership lookup reproduces gold) is 100% by construction, reported, not a bar |
| T63-K9 | EXISTS balance: YES 45-55% per sub-block; EX-N1, EX-N2, EX-N3, EX-N5 each >= 15% of the NO rows of sub-blocks where defined; EX-N4 <= 30%; none > 40%; EX-B language split 60 / 20 / 20 +- 5 pp | as stated |
| T63-K10 | LIC integrity [Opus b1b T63-M4]: table sha recorded; 100% of rows = lookup; each cell used once; label shares 30-40% each; cells drawn stratified by LABEL only (no per-licence cap that distorts the table); format-only probe (card layout, field order, wording id; no licence ids) balanced accuracy; AXIS-READING check: >= 50% of the one-axis-flip pairs flip on usage mode or distribution (not on a licence id) and >= 40% of LIC rows come from (dependency, project) pairs whose 15 mode x distribution cells hold at least two different labels. The old per-licence purity <= 70% bar is DELETED (for permissive dependencies one label is correct in nearly every cell, so it would fail on correct data or force under-sampling the most common real case). Single-licence-feature probes and per-licence label shares are REPORTED | format-only <= 1/3 + 3 pp = 36.3%, ub <= 39.3%; axis-reading shares as stated |
| T63-K11 | MAL slice (LR-B5) [Opus b1b T63-M2, GV11: an L-R DATASET gate of LR-04, not a T63 family kill: failing after the slice's ONE set-level correction (LR-B8) leaves the DataDog slice and its negatives out, logged; T63's own gates are read WITHOUT the MAL rows]: (a) field record complete and the access log shows 0 reads inside payload ZIPs; (b) combined-slice class balance; (c) exception rows; (d) probe of K4; (e) all-field parity probe (every non-label field of the combined slice) | (a) 100% / 0; (b) 50% +- 3 pp; (c) <= 20% of positives; (d) K4 bars; (e) AUC <= 0.55, ub <= 0.60 |
| T63-K12 | Ladder composition and twin share (section 5) | L1 20 / L2 30 / L3 30 / L4 20 +- 5 pp; L3-L4 >= 25% overall and per block; twins >= 50% of L3-L4 |
| T63-K13 | NEAR quotas: YES 45-55%; NM-T1..NM-T8 each 5-25% of YES; NM-R4 <= 8% of NO | as stated |
| T63-K14 | Token rule G6; >= 50 wordings per question form, none > 2%; A50 G6, A49c, G5-H, G3-H, A43(d) per the pipeline (G2) | per pipeline |
| T63-K15 | Split hygiene: no group in both dev and train; OHS-5 collision drops | 100% / <= 5% of rows (above 5% IS the fix iteration) |
| T63-K16 | Check at creation (section 6): 100% of pooled rows carry a current clean stamp and an answer-check record; 0 unstamped rows | 100% / 0; drops <= 1% outside exempt scaffolding and OHS-5 collisions, else the fix iteration |
| T63-K17 | A1 / A2 hooks: template id, wording id, construction id on 100% of rows | 100% |
| T63-K18 | Names guard: language, runner, carrier, card ids on the frozen allow-list (manifest v1.2 once it lands); family id T63 on row_job_families_allowed (already listed in v1.1) | 0 refusals |
| T63-K19 | Fact-label assert: no T63 question form lists ALLOW / ASK / BLOCK; no T63 row offers an install permission | 0 violations (CPU) |
| T63-K20 | No-execution scan: no generator or validator imports or runs third-party code named in a row; the stdlib export is produced at image build only | 0 violations (CPU) |
| T63-K21 | Ladder measured bar: C2 (C1 if none) on L4 rows of the pilot | accuracy <= 70% (FIX TRIGGER, never a kill; after the fix a report line) |

POST-TRAINING REPORT (never a kill)
| ID | Report line |
|---|---|
| T63-R1 | Per-head accuracy with CI against base 4B and baselines: always-YES, majority, edit-distance rule (NEAR), list-lookup rule (EX-A), "name looks real" prior (EX-B2), table majority per licence (LIC) |
| T63-R2 | NEAR by transformation id, by relation kind (squat / old-legit / sibling / two long-lived), by query registry |
| T63-R3 | EXISTS by sub-block, view (visible vs knowledge) and language; EX-N kind breakdown |
| T63-R4 | LIC accuracy by class, usage mode and distribution mode |
| T63-R5 | MAL slice result with "train split seen"; the real-name exception subset reported separately |
| T63-R6 | Accuracy by ladder level L1-L4 vs base 4B and trivial baselines |
| T63-R7 | Flip rate under option permutation with CI; ECE and Brier per head |

## 8. Clean-room notes

- Built only from the plan, LANE_L-P, the stripped codeexec excerpt and the approved G0 files. No original T36 or T63 generator, template, wording pool, hardest.md text, public package-hallucination or typosquat benchmark item, or OHS file was opened (none visible to me). The old family T36 "folds in": nothing of it was read.
- No real third-party package name in any generated row (K3). The only real names in T63 rows are standard-library module and symbol names, the fixed SPDX identifiers, ecosystem words and the DataDog positives under the P1-realism exemption (Sk 8) with the swap-or-exception rule.
- No SPDX text is copied: the LIC table cites identifiers only. No licence text, no package README, no vulnerability advisory text.
- DataDog payload ZIPs are never opened or executed; no field from inside them is read (K11a). The dataset's Apache-2.0 terms cover labels / manifests / metadata; payload code keeps its original licences and is never used.
- Writers (Haiku wording pools) get the question forms and slots, never the literal-ban list. G13 hit reports carry row ids, target name and method only.

## 9. NAMES this family needs (names only; for manifest v1.2, due Fri 23 12:00; family id T63 is already on row_job_families_allowed)

- Programs / ecosystem words (existing ids): prog.pip, prog.npm, prog.yarn, prog.cargo, prog.go. Languages: python, javascript, typescript, go, json, yaml (existing). Runners: none for row labels (no execution). Image-build export programs (never in rows): runner.stdlib_export.python, runner.stdlib_export.node, runner.stdlib_export.go (names-only dump; sha in the manifest).
- Policy / definition cards: card.t63.registry_resolve (slots reserved_internal_namespaces, resolve_order), defs_card.t63.near, defs_card.t63.exists, defs_card.t63.licence, defs_card.t63.mal.
- Carriers: SNAPSHOT_TABLE (rendered via TBL-CSV / TBL-JSON / TBL-KV / TBL-PIPE / TBL-TSV), QUERY_LINE, REGISTRY_INDEX, LIB_EXPORTS, MODULE_EXPORTS, MANIFEST_RECORD, LICENCE_CARD; SRC_FILE and QUESTION_FORM reused.
- Registry ids (hash export, not guard-checked): T63-Q-NEAR, T63-Q-EXISTS, T63-Q-LIC, T63-Q-MAL (>= 50 wording ids each); NM-T1..NM-T8; NM-R1..NM-R4; EX-A1, EX-A2, EX-B1, EX-B2; EX-N1..EX-N5; LC-USE-1..5; LC-DIST-1..3; LC-ID-1..16 (the identifier set); T63-LIC-TABLE; M-PLAUS, M-XREG, M-EDIT, M-SIB, M-VER, M-CELL; levels L1-L4.
- Fixed real names (a NEW names category "fixed_real_licence_ids", proposed for v1.2): the SPDX identifiers listed in section 2.3 and the proprietary / no-assertion marker.
- Stdlib vocabulary: the Python / Node / Go public-symbol export (program output, names only, hashed) enters v1.2 so the sealed side keeps C-transfer clear of those names. Real MAL vocabulary is extracted BY PROGRAM after the L-R S-pre PASS (plan 16.3 rule 4), not listed by hand.
- Namespace slot kinds used (all existing): ns.package, ns.registry_host, ns.handle, ns.org, ns.noun.module, ns.noun.symbol, ns.project, ns.policy_card. No new kind.
- G13 targets to register before any row (names only): the DataDog set's own non-trained parts are not targets; ANY public package-hallucination, typosquat or API-hallucination evaluation set that the L-0b registry scout finds (names UNKNOWN to me, none invented here); the standing list (OHS-3, OHS-4, OHS-AC, OHS-5 once frozen, public eval targets).
- R5 candidate list (names only): DataDog malicious-software-packages-dataset (already LR-04).

## 10. Risks

1. NEAR gold is a policy function of the shown record, not a claim about real registries; a reader could say a same-publisher near name is still risky. Mitigation: the decisive fields are shown, the rule is stated in defs_card.t63.near, and the report names it "policy label on the shown snapshot".
2. The knowledge view (EX-B2) can teach recall the 4B lacks, i.e. noise-like rows. Mitigation: half of EX-B is the visible-list view; the report line R3 separates the views; EX-B2 shrinks to the visible share if R3 shows no signal (a C2.2 note, not a kill).
3. Name-shape leaks in the knowledge view (mutated negatives look odd). Mitigation: negatives are real names from sibling modules; EX-N4 capped and only kept if K4 passes.
4. MAL slice: positives carry real-name residue, negatives are seeded; the combined-slice probe may fail even after the swap. Mitigation: exceptions dropped first; slice left out as a dataset (O-T63-3) rather than weakening a bar.
5. LIC table errors: legal nuance can be wrong. Mitigation: REVIEW for contested cells, rationale column, Opus writes and signs, the table is policy not advice.
6. Platform-conditional stdlib names: handled by the pinned-image wording; a name that differs between two runs of the export tool is dropped from the export (3 identical export runs).
7. Sandbox dependence: the stdlib export needs the L-0 image; T63 rows other than EX-B do not need the sandbox.
8. Snapshot token cost: 14-entry tables plus the card may exceed budget; entry count is a program parameter chosen BEFORE the pilot to keep the mean <= 800.

## 11. One fix iteration and kill rule

- G3 governs: the pilot through the stamp wrapper is the first measured look at every PRE-FREEZE gate; ONE combined fix follows. Allowed fix levers: generator parameters, quotas, relation and negative-kind mix, snapshot size, wording pools, AFLite-style repair (filtered <= 30% of the family, reported), raising ladder HIGH settings; NOT the bars. Defects found before the pilot by unit tests, the build skeptic or A/B disagreement on CPU fixtures are build fixes.
- Kill (standard P1 rule): any PRE-FREEZE gate still failing after the fix, or not through all of them by the data freeze (Mon 2 Nov 23:59 UTC; stretch Fri 30 Oct) -> T63 rolls to C2.2 / C3 with the failing gate and numbers logged. G4: no head rolls alone inside T63 (NEAR, EXISTS, LIC are kept or killed with the family). The MAL slice is an L-R DATASET (GV11, plan 16.3 rules 3 and 6): it is left out by its own dataset gates and never rolls T63; if T63 is killed, the MAL slice goes with it (its negatives are T63 rows) [Opus b1b T63-M2]. POST-TRAINING lines are never kill rules. T63 is first in the usage shed order after the research pass (plan 16.9 / build order).
- Timeline: G0-lite and Opus approval Mon 19; builder launched only under the measured burn projection (Sk 21); rows after the OHS-5 freeze, the registry sha, manifest v1.2, a signed stamp service and a signed conformance record (Sat 24 18:00 rules unchanged); EXISTS-B needs the L-0 image record (Wed 21 sandbox sign-off).

## 12. Open questions for Opus

- O-T63-1 MAL size: default 250 + 250 (total 500 = the plan's P1 realism line). If the 500 cap in LR-04 counts positives only, the slice becomes 500 + 500 and the money projection grows by 500 rows. Which?
- O-T63-2 Confirm that DataDog negatives (program-made benign records) are T63 generator rows under T63's gold (LR OQ-R3) and that the slice is counted in T63, outside the 1,200.
- O-T63-3 G4 reading: confirm that failure of the MAL slice leaves out the DATASET slice (L-R rules 3 and 6) and does not roll T63.
- O-T63-4 LIC probe deviation: single-licence-feature probes are report-only, replaced by the purity <= 70% bar and the format-only 36.3% / 39.3% bar. Accept?
- O-T63-5 Confirm that fact-labelled T63 forms need no G9 test against T50 R14 / R12 (K19 asserts no permission option).
- O-T63-6 Pilot size for families under 1,000 rows: 50% of the family, floor 300, cap 1,000 (design value).
- O-T63-7 Licence table: Opus writes it on Mon 19 and hashes it before any LIC row; confirm the identifier set size (16 dependency x 8 project) and that "fixed_real_licence_ids" may be a new names category.
- O-T63-8 Is the age < age(Q) condition in the NEAR gold acceptable as "P is newer", or should a registered-date field be shown instead of classes?

## 13. Conformance seed (plan 16.1 step 0)

| Clause | Obligation | CPU test id |
|---|---|---|
| G1 | solver B package imports stdlib + row schema only; no model client; a labeller never reads a model output | T63-CM-01 |
| G3 | generator parameter file sha frozen at pilot launch; a changed sha after pilot-gate numbers exist needs the fix-iteration flag | T63-CM-02 |
| G5 | probe calls use grouped split, 97.5th-percentile bound, permutation and leak checks | T63-CM-03 |
| G6 / GV4 | row > 1,536 tokens refused at creation; mean and > 1,024 share at set level | T63-CM-04 |
| GV5 | a G13-dropped row retires its spec and the whole pair / snapshot group; no same-skeleton regeneration after a G13 drop | T63-CM-05 |
| 2.1 | NEAR gold function, relation test and the >= 92% NO-near rule | T63-CM-06 |
| 2.2 | EXISTS membership sources; export sha and image id in manifest | T63-CM-07 |
| 2.3 | licence table hashed before the first LIC row; each cell once | T63-CM-08 |
| 2.4 / 3.5 | MAL: field record, access-log audit, swap-or-exception, exception cap | T63-CM-09 |
| K3 | no real third-party package name outside the MAL exemption | T63-CM-10 |
| K19 | no ALLOW / ASK / BLOCK option in any T63 form | T63-CM-11 |
| 6 | pool writer refuses any row without a current clean stamp and an answer-check record | T63-CM-12 |
| 3.6 | A10 / A12 / A14 / A15 / A16 not carried; A1 / A2 hook fields present | T63-CM-13 |

## Opus batch-1b rulings v3.2 (Opus 5.5 high, Sun 18 Oct 2026 UTC; families/G0_APPROVALS_v32.md "Batch 1b")

VERDICT: REVISE -> APPROVED after the 5 fixes below (applied in this file, marked "[Opus b1b ...]"). Generator, solver
and probe CODE for NEAR, EXISTS and LIC may start now; LIC rows wait for the hashed Opus licence table; MAL mapper code
waits for the LR-04 S-pre PASS and the T63-M3 decision. Rows only after the OHS-5 freeze, the registry sha, manifest v1.2,
a signed stamp service and a signed conformance record (Sat 24 18:00 rules unchanged).

Must-fix (applied):
- T63-M1 NEAR T8 written as its own first-match clause with all four conditions; NM-T1..NM-T7 keep the established /
  publisher / edge / age rule. Reason: "for T8 the card makes the public entry the risk" left solvers A and B to guess
  which conditions apply; a reserved internal name has no established public twin.
- T63-M2 (GV11) K11 is an LR-04 dataset gate (leave-out), not a family kill; T63 gates are read without the MAL rows;
  section 11 kill text aligned (G4 is not loosened for NEAR / EXISTS / LIC).
- T63-M3 MAL learnability precondition on the measured field record (section 2.4). Reason: with names swapped through the
  namespace, no real names in negatives (K3), and every non-label field required uninformative (K4, K11(e)), a slice
  whose files carry only name / version / ecosystem has no visible label signal; the probes would PASS on noise.
- T63-M4 K10 purity bar replaced by label-stratified cell sampling plus an axis-reading check (section 7).
- T63-M5 O-T63-1: if built, MAL = 500 + 500 (the LR-04 cap counts dataset rows; LR-01 precedent).

Binding conditions:
- T63-B1 O-T63-2 confirmed: DataDog negatives are T63 generator rows under T63's gold, counted in T63 with the slice,
  outside the 1,200 (LR-B5, OQ-R3).
- T63-B2 O-T63-3 -> GV11. T63-B3 O-T63-4 -> T63-M4.
- T63-B4 O-T63-5 confirmed: T63 forms are fact questions (K19); no G9 leg against T50 R12 / R14 is needed while no T63
  row shows an install or fetch ACTION (a T63 row that renders one would fall under GV13 and needs a leg).
- T63-B5 O-T63-6 -> GV10: pilot = 50% of the 1,200 generated rows = 600, proportional by block (NEAR 250, EX-A 125,
  EX-B 125, LIC 100); MAL has no pilot (L-R rule 6: set-level checks once per built dataset slice).
- T63-B6 O-T63-7: the licence table is written by a SEPARATE fresh Opus 5.5 high session (not this one), hashed before any
  LIC row; the identifier set 16 x 8 x 5 x 3 is confirmed; `fixed_real_licence_ids` is a NON-GUARD fixed-name list in
  manifest v1.2 (the five guard categories are unchanged). NC, AGPL and proprietary ids are identifiers only; no licence
  text enters any row.
- T63-B7 O-T63-8: the shown age CLASSES decide (strict class order; same class = not newer = NO). No date field.
- T63-B8 EX-B export: public module-namespace names (no leading underscore) of the pinned image, 3 identical export runs;
  a name re-exported into a module counts as present (attribute access works) and defs_card.t63.exists says so; EX-N1
  negatives are checked against the FULL export of the queried module, so a sibling-module name that is also re-exported
  is never a NO.
- T63-B9 The stdlib symbol export, the DataDog real vocabulary and the licence spellings are PROGRAM outputs; they are
  hashed with the Thu 22 export. They are not guard categories; their entry into a names manifest after the v1.2 freeze
  is an orchestrator item (flag 3 of Batch 1b).

[Opus Q7b, 2026-10-18 19:59 UTC; recorded by the orchestrator; source RULINGS_T59_T60_T63.md "Q7b T63 K10 amendment"] K10's format-only
probe part is replaced, before the pilot, by K10-F, a construction assert (PRE-FREEZE KILL, 100%): (a) code-level: each LIC
row's card layout, field order, wording id, template id and option order depend only on (seed, row index); regenerating
with labels permuted or cells swapped gives byte-identical formats; a static check shows the format draw takes no label or
cell input; (b) exact replay on 100% of built rows (layout and field order single-valued; K14 wording cap holds). The
probe stays REPORT-ONLY beside the assert (n, validity flags, noise ub). Reason: on pure noise at k=3, n=110 the probe's
97.5% ub is 0.40-0.44, above the 39.3% bar, so correct data cannot pass (precedent T63-M4). All other K10 parts bind.
