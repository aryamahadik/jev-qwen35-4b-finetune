# G0-LITE T65 VULN-SYNTH (synthetic CWE twins by static-taint gold + Juliet good/bad twins via L-R) (lane L-P wave C; P1; clean-room; draft for Opus approval, due Fri 23 Oct 2026, written early)

Author: Sonnet 5.5 high (L-P G0-lite writer), Sun 18 Oct 2026. Design only: no rows, no generator code, no download, no execution, no model call, no Modal.
Status: DRAFT 1. Every number below is a design value fixed BEFORE any pilot; changing one after a pilot is a gate edit and needs Opus.
Scope (plan 16.9): "synthetic CWE + Juliet 700 good/bad twins via L-R; no CVE ids (F2); needed before the Juliet rows map (by Fri 23)". Plan section 1 C: "synthetic CWE, static-taint gold, no CVE/NVD text".
Read for this file: PLAN_TRAINING_SIDE.md (sections 1 C and E, 2, 5, 8, 16), LANE_L-P.md, excerpts/codeexec_s5.md, families/T42c G0-lite and addendum (execution witnesses, ladder, check-at-generation), families/LR/G0_LITE.md (row LR-03, rules R5-R16), families/T50/G0_LITE.md (format), families/G0_APPROVALS_v32.md (GV1-GV9), C2_1_PUBLIC_TRAIN_INVENTORY.md (A14, section 4 T65 row), l0/NAMES_MANIFEST_V1_1.json (structure only). NOT opened: any path containing "ohs" or "sealed", C2_1_PLAN_v3.md, any plan SKEPTIC file, OHS5_BRIEF_DRAFT.md, any generator, wording pool, Juliet file, vulnerability database entry, benchmark item text, mutate.py, ~/.claude. Dataset details and tool behaviours that appear below come from memory and are marked UNVERIFIED.
Shared rulings carried (index): G1 solver B is CODE; G2 data-audit gates are PRE-FREEZE; G3 no free pilot tuning, ONE combined fix; G4 no head or sub-block rolls alone (the Juliet slice is an L-R dataset decision: section 11); G5 one probe harness; G6 tokens; G7 secondary heads are head rows (CWE class head); G9 not applicable (T65 labels facts, not permissions); G10 not applicable; GV1-GV4 (A10 / A14 not carried; GV4 binds); GV5 (a G13 hit retires the spec and the whole twin pair); GV6, GV7 (not applicable); GV8; GV9.

## 0. One-paragraph summary

T65 teaches the 4B to tell a vulnerable function from its fixed twin, where the two differ by ONE neutralising call or edit. Generated rows (600) come from a taint-flow spec (attacker-controlled source, optional benign transforms, an optional registered neutralising step, a class-specific sink) rendered into application-style Python, JavaScript / TypeScript and Go. Gold is a static taint engine over the spec (solver A) cross-checked by an independent solver B: a sandbox execution witness with a registered benign canary payload for the six classes where one exists, and an independent AST pattern engine for the three static-only classes. A realism slice of Juliet Test Suite good / bad twins (700 rows via L-R LR-03; public domain) adds real C / C++ / Java / C# shapes after a program scrub removes every label-bearing token. No CVE id, advisory text or NVD text appears anywhere (guard F2).

## 1. Decision and label set

| Head | Question form id | Rows | Labels | Gold |
|---|---|---|---|---|
| VULN (generated) | T65-Q-VULN | 600 (300 twin pairs) | YES (attacker-controlled input reaches the sensitive operation without being neutralised for that operation) / NO | static taint over the spec; execution witness or independent AST engine as solver B |
| VULN (Juliet, L-R LR-03, P1-realism) | T65-Q-VULN | 500 (250 twins) | YES (the flawed variant) / NO (its good counterpart) | the dataset's own bad / good pairing (program label), after the scrub |
| CWE class head rows (G7), GENERATED only | T65-Q-CWE | generated <= 75 (<= 25% of YES specs), outside the 600 | pick-one of 4 class names (the gold class plus 3 program-chosen nearest classes) | the spec's class |
| JUL-CWE (L-R question form, NOT a G7 head) [Opus b1b T65-M1] | T65-Q-CWE | 200, inside the LR-03 700 cap | pick-one of 4 class names | the dataset's own CWE label through the recast table; drawn from Juliet test cases NOT used by JUL-VULN (no same-context second question) |
Binary heads shuffle option order per row; 20% order-invariance copies are mix-level, not counted. Class names appear as WORDS in the CWE head options; no CWE number appears in any prompt or code (K9). The family labels facts, not permissions; no ALLOW / ASK / BLOCK option (K21).

## 2. Gold method; solver A and independent solver B

### 2.1 Generated rows (spec -> render)

Spec: base application scenario (request handler, report export, file serving, search, redirect after login, audit log, upload store, client call, token hashing, temp file use; domains as the T42c list); a SOURCE (a request parameter, argument or message field the spec marks attacker-controlled), 0-2 benign TRANSFORMS (trim, lower-case, format into a larger string, put in and read from a container), at most one NEUTRALISING step drawn from the sanitiser registry SAN-* for the sink's class, and a SINK of that class.
Classes (registry ids CWEC-22 path traversal, CWEC-78 OS command injection, CWEC-79 cross-site scripting through unescaped output, CWEC-89 SQL injection, CWEC-117 log injection, CWEC-601 open redirect, CWEC-295 certificate / TLS verification disabled, CWEC-327 weak hash for a password, CWEC-377 insecure temporary file). Dynamic-witness classes: 22, 78, 79, 89, 117, 601. Static-only classes: 295, 327, 377.
LABEL FUNCTION (solver A, over the spec): YES iff a SOURCE-to-SINK flow exists and no neutralising step valid for that class and that flow lies on every path before the sink. Neutralising steps are valid only if: of the sink's own class; applied to the tainted variable (or a value derived from it) that reaches the sink; executed before the sink on all paths; its result used. Static-only classes: YES iff the flagged API use is present with the flagged argument (certificate checks off; a fast unsalted hash for a password; a predictable temporary name) and absent in the fixed twin.
TWIN construction: each pair has the same scenario, names and layout. Plain pair: the neutralising call is present (NO) or removed (YES). Decoy pair: the YES member carries a DECOY step (registry ids DS-1 sanitiser on a different variable; DS-2 sanitiser of the wrong class; DS-3 sanitiser after the sink; DS-4 sanitiser on one branch only; DS-5 sanitiser result discarded; DS-6 sanitised value later replaced by the raw one) and the NO member differs by the one token, argument or position that repairs it. NO-HARD kinds: NS-1 neutralising step inside a helper two calls away; NS-2 strict allow-list lookup instead of a sanitiser; NS-3 the sink is unprotected but the value is not attacker-controlled (constant or configuration), looking like a flaw; NS-4 library-level parameterisation.
EXECUTION WITNESS (solver B for dynamic classes; the label is NOT taken from it alone): the function is run in the od-sbx1 sandbox (no network, tmpfs /work) with a REGISTERED benign canary payload (PAY-22 a parent-directory path to a canary file outside the served root; PAY-78 a shell separator plus an echo of a canary string; PAY-79 a canary markup tag; PAY-89 a boolean-tautology string against an in-memory database with two rows; PAY-117 a newline plus a canary field; PAY-601 an off-site canary host). YES iff the canary effect is observed in 3 of 3 identical runs, NO iff in 0 of 3; any other pattern is dropped. No other payload exists; K14.
SOLVER B (G1): a PROGRAM from a separate Sonnet high session that sees only this file and the row schema (never A's code): for dynamic classes it parses the RENDERED function, builds its own harness, executes through the sandbox interface and applies the canary rule; for static-only classes it is an independent AST pattern engine (Python `ast`; Go's standard `go/parser` via a small program; JavaScript / TypeScript through tree-sitter, MIT, parse only) that recomputes the flagged-use test from the rendered code. Agreement among A, B and the spec expectation on 100% of kept rows; disagreements dropped and counted (unexpected results also catch generator bugs).

### 2.2 Juliet slice (L-R LR-03; contract for the mapper)

Source: Juliet Test Suite 1.3 (C / C++; Java / C# same terms), "not subject to copyright protection and is in the public domain", foreign rights CC0 1.0 (quote in the record). No split exists: a seeded program freezes an internal 10% hold-out by CWE FAMILY BEFORE mapping (internal target, never trained). Label provenance: program (the suite's own bad / good function pairing); the A46 noise screen is exempt (LR R14 exact-program-label set).
Construction: per test case, the flawed function and ONE good counterpart (the good variant whose statement count is closest to the flawed one; length parity within +- 15% for >= 90% of twins, K10). SCRUB by program, 100% of rows: remove every comment (including the flaw and fix markers); rename functions and variables that contain bad, good, G2B, B2G, the CWE number or the flow-variant number to neutral names from a fixed program list; neutralise file names; drop the harness `main` and output helpers; keep real library API names. [Opus b1b T65-M2] The scrub and its K10 scan cover EVERY token class: identifiers, preprocessor macros and guards (the OMITBAD / OMITGOOD style guards are removed with their branches resolved for the kept function), string literals, comments, include names of the suite's support headers, and file names; for JUL-CWE rows the words of every CWE class name that the options can print are also absent from the code (an identifier that spells the class is renamed), so the label is never in the code text. Rows: JUL-VULN 500 (250 twins), JUL-CWE 200 (the dataset's CWE class as a 4-way pick-one with program-chosen nearest classes, class names as words). Real names are exempt (P1-realism, Sk 8); vocabulary extraction BY PROGRAM for manifest v1.2.
SOLVER A = the mapper's pairing record. SOLVER B = a program that re-derives pairing and class from the source file names and function names with its own parser, and re-checks the scrub; 100% agreement; no LLM reads rows to label or check.

## 3. Inputs, carriers, design values

3.1 Input view: no user messages or tool calls (single view; recorded for the per-family view requirement). Carriers (section 9): SRC_FILE (the function, <= 40 lines), FUNC_CONTEXT (caller lines, <= 12), OPTIONS, QUESTION_FORM.
3.2 Languages (generated): Python 65% (390), JS/TS 18% (108), Go 17% (102); each class appears in at least 2 languages except CWEC-89 (Python only unless the Node SQLite module passes a self-test; UNVERIFIED). Pins (Python 3.12.x, Node 24.x, Go 1.26.x with GOFLAGS=-mod=vendor GOPROXY=off GOTOOLCHAIN=local) come from the L-0 image record and are appended before the first non-Python row. Sink and sanitiser API names are standard-library names from the L-0 stdlib symbol export; entity strings are seeded (TRAINING salt).
3.3 Application-style rule: no textbook vulnerable snippet shapes copied from public sets; domain list as T42c; code is produced by program templates written by the builder (no model authors or labels a row).
3.4 Comments: either all rows have no comments, or comments are neutral and present at the same rate across labels (+- 3 pp, K5).
3.5 Splits: dev = 10% of GROUPS (a group = one base scenario with all its twins and renderings); never split across dev / train (K13).
3.6 Levers: A10, A12, A14, A15, A16 are NOT carried by L-P; GV7. A1 / A2 hooks: template id, wording id, construction id (class, SAN, DS, NS) on every row.

## 4. Sizes and shares (rows before drops; quotas counted AFTER drops, every quota cell oversampled by 15% at generation)

| Block | Rows | Notes |
|---|---|---|
| VULN generated | 600 | YES 300 / NO 300; 300 twin pairs; Python 390, JS/TS 108, Go 102 |
| class shares (of 600) | 22: 12%, 78: 14%, 79: 12%, 89: 12%, 117: 8%, 601: 10%, 295: 10%, 327: 12%, 377: 10% | each class 5-15%; dynamic-witness classes 68% (>= 60%) |
| YES composition | DS-1..DS-6 decoy rows >= 40% of YES (each kind 5-25% of the decoy rows); plain removal rows the rest | |
| NO composition | NS-1..NS-4 >= 40% of NO, NS-3 >= 10% of NO; plain correct-sanitiser rows the rest | |
| CWE head rows (generated) | <= 75 | outside the 600; <= 25% of YES specs |
| JUL-VULN | 500 | 250 twins, YES 250 / NO 250 |
| JUL-CWE | 200 | 4-way pick-one |
| Total trained (default) | 1,300 + <= 75 head rows | the money projection counts these |
Matched pairs: 100% of generated and Juliet VULN rows are in a pair (bar >= 30%). Reuse: <= 2 pairs per base scenario, <= 4 rows per base scenario overall. Pilot (G3 first look) = a seeded proportional 50% sample of the generated block (floor 300, cap 1,000; O-T65-5). O-T65-1: the plan gives no size for the generated block; 600 is a design value (the plan's P1 new-heads line is about 2,500 and T63 + T66 + T67 already use about 3,000).

## 5. Difficulty ladder L1-L4 [CRIT D1, D2]

Mechanism (inventory): "good/bad twins that differ by one sanitising call". Program parameters only.
| Id | Mechanism | LOW | HIGH |
|---|---|---|---|
| M-FLOW | taint path length | source passed directly | passed through 2 intermediate variables, a container field, a format step |
| M-HELP | neutralising step location | in the function | inside a helper two calls away (NS-1) or a decoy inside a helper (DS-1) |
| M-DECOY | decoy subtlety | wrong-class sanitiser (DS-2) | wrong variable differing by one character (DS-1), or the step on one branch only (DS-4) |
| M-LOOK | looks flawed / looks safe | the code looks like what it is | NS-3 (looks flawed, not attacker-controlled) or a correct step written unusually |
Row level: L1 none; L2 one LOW; L3 one HIGH or two LOW; L4 two or more HIGH. Composition (PRE-FREEZE): L1 20% / L2 30% / L3 30% / L4 20% (each +- 5 pp); L3-L4 >= 25% overall and per class group (dynamic / static). TWIN rule: every pair is a twin by design; L3 / L4 pairs differ by <= 1 token, argument or position (>= 50% of L3-L4 rows). MEASURED BAR (K20, once, on the pilot): C2 (C1 if none), read on od-l4b, scores <= 70% on L4 rows. Model-based, so NOT a kill: a miss is folded into the ONE combined fix by raising HIGH settings (never by dropping rows by model score); afterwards a report line. Juliet rows have no ladder.

## 6. CHECK AT GENERATION [OWNER-ROW] (plan 16.1)

Owner, 18 Oct (binding): "If you're building one row, check that row at that same point and that's it ... then train." Every row is written ONLY through the L-0b stamp wrapper, per batch (<= 500 rows, same day):
(a) ANSWER CHECKS per row: manifest complete (K1: image id, runsc and kernel versions, 3 run hashes, payload id); solver A = solver B = spec expectation; twin integrity (K2); witness rule of its class (3 identical runs; payload registered); generator lint (K15); identifier and comment scrub (K5); guard F2 scan (K9); names guard (K16); token rule G6 (> 1,536 refused); PII scrub; exact-duplicate refusal (AST-normalised hash) and the reuse ledger; ladder level and A1 fields; Juliet rows: scrub rules, pairing, length parity, hold-out exclusion, licence record.
(b) G13: the stamp service checks the row against every registered target with every listed method (registry sha bound; R6 scaffolding exemption; OHS-5 hash-export targets: exact and hashed n-gram methods only).
(c) The stamp is written to the row manifest. A failed row is dropped and logged (row id, target name, method). No unstamped or failed row enters the pool.
GV5: a G13-dropped row retires its spec; the whole twin pair (and the pair's CWE head row) is dropped with it; the replacement is a NEW spec with a new seed; same-skeleton regeneration only for NON-G13 answer-check drops. A Juliet hit row is dropped and its source test case is never re-sampled.
FIX TRIGGER (all rows): > 1% of the pilot rows (or of any generation day) dropped for a reason other than exempt scaffolding or OHS-5 collisions (<= 5%) = the ONE combined fix. Code-idiom note: short idiomatic functions can match public sets by accident; per-method drop counts are reported; if idiom-driven drops exceed 1% the ONE fix may raise scenario distinctiveness, never relax a bar. SET-LEVEL checks once per family (pilot first look, then built family): A50 G6, A49c, wording variety, matched-pair share, ladder and measured bar, section 7 probes, G5-H (two Haiku solvers on 300 rows plus one Haiku read of 100% of free-form wording), G3-H, Opus A43(d). Then C2 reads on od-l4b: not a kill gate.

## 7. Gates

Probe protocol = G5 (groups: base scenario for generated rows; test case for Juliet). PRE-FREEZE KILL = CPU or sandbox, data only; a miss after the one fix rolls the family (the Juliet slice: dataset-level leave-out, section 11). POST-TRAINING REPORT = needs the trained model, never a kill.

PRE-FREEZE KILL
| ID | Gate | Bar |
|---|---|---|
| T65-K1 | Witness compliance: complete manifest; 3 identical runs; registered payload | 100% |
| T65-K2 | Twin integrity: each pair differs by exactly the registered edit (token diff equals the edit spec); labels opposite; no unpaired row | 100% |
| T65-K3 | Solver A = solver B = spec expectation; per construction id (SAN, DS, NS, class) expectation mismatch rate | 100% of kept rows; block drop > 2% returns the block; any id > 10% returns to the builder |
| T65-K4 | Sanitiser-presence probe: count of registered sanitiser-API calls, any-sanitiser flag, calls from OTHER classes' sanitiser lists; and the presence-rate parity | AUC <= 0.55, ub <= 0.60; any-sanitiser rate within 5 pp across labels |
| T65-K5 | Identifier / comment scrub: banned-word list (vuln, bad, good, safe, unsafe, secure, insecure, tainted, clean, evil, attack, exploit, inject, malicious, sanitised, trusted, untrusted, fix, flaw, cwe and their forms) absent from OUR identifiers and comments (standard-library API names are exempt); comment-presence parity; identifier bag-of-words probe | 0 hits; <= 3 pp; AUC <= 0.55, ub <= 0.60 |
| T65-K6 | Length / structure probe (tokens, lines, call count, nesting depth, variable count; no content tokens) | AUC <= 0.55, ub <= 0.60 |
| T65-K7 | Balance: classes 5-15% each; YES 45-55% overall and per class, per language; language shares Python <= 70%, JS/TS >= 10%, Go >= 10%; dynamic classes >= 60% | as stated |
| T65-K8 | Composition: DS-1..DS-6 >= 40% of YES (each 5-25% of decoy rows); NS-1..NS-4 >= 40% of NO, NS-3 >= 10% of NO | as stated |
| T65-K9 | Guard F2: 0 CVE-, GHSA- or NVD strings, advisory text, or product-and-version vulnerability claims; 0 CWE numbers in prompts or code (class names as words only in the CWE head options) | 0 (program scan, 100% of rows) |
| T65-K10 | Juliet contract (LR-03) [GV11: an L-R DATASET gate of LR-03; failing after its ONE correction leaves the Juliet slice out, never rolls T65; T65's own gates are read on the generated rows]: scrub 100% (banned tokens and, for JUL-CWE, class-name words absent from identifiers, macros, string literals, comments, include and file names; Opus b1b T65-M2); pairing preserved 100%; length parity +- 15% for >= 90% of twins; hold-out by CWE family frozen before mapping and absent from output; licence record with the public-domain and CC0 quotes; surface probe grouped by test case (tokens, lines, statements, identifier count, nesting depth) | 100% / 100% / >= 90% / 100% / present / AUC <= 0.55, ub <= 0.60. A failing probe gets ONE fix (re-select good variants for length parity) else the slice is left out |
| T65-K11 | Head-row probes (G7): CWE head (generated and Juliet), format-only and option-surface features | balanced accuracy <= 1/4 + 3 pp = 28%, ub <= 31% |
| T65-K12 | Token rule G6; >= 50 wordings per question form, none > 2%; A50 G6, A49c, G5-H, G3-H, A43(d) per pipeline (G2) | per pipeline |
| T65-K13 | Split hygiene: no base scenario in both dev and train; OHS-5 collision drops | 100% / <= 5% of rows (above 5% IS the fix iteration) |
| T65-K14 | Payload registry: every executed payload is a registered canary; no other payload exists; execution only in the sandbox | 100% / 0 violations |
| T65-K15 | Generator lint (clock, randomness, environment reads, network, filesystem outside /work, order-dependent output); hash seed and locale fixed | 0 violations in kept rows |
| T65-K16 | Names guard: language, runner, carrier, card ids on the frozen allow-list (v1.2); entity strings seeded; API names from the stdlib export; Juliet rows exempt by family field with the CPU test | 0 refusals |
| T65-K17 | Check at creation (section 6): 100% of pooled rows carry a current clean stamp and an answer-check record | 100% / 0 unstamped; drops <= 1% outside exempt scaffolding and OHS-5 collisions, else the fix iteration |
| T65-K18 | A1 / A2 hooks: template id, wording id, construction id on 100% of rows | 100% |
| T65-K19 | Ladder composition and twin share (section 5) | L1 20 / L2 30 / L3 30 / L4 20 +- 5 pp; L3-L4 >= 25% overall and per group; twins >= 50% of L3-L4 |
| T65-K20 | Ladder measured bar: C2 (C1 if none) on L4 rows of the pilot | accuracy <= 70% (FIX TRIGGER, never a kill; after the fix a report line) |
| T65-K21 | Scope asserts: no ALLOW / ASK / BLOCK option; generators never run generated code locally (sandbox only); no exploit tooling beyond PAY-* | 0 violations (CPU) |

POST-TRAINING REPORT (never a kill)
| ID | Report line |
|---|---|
| T65-R1 | Accuracy per class, language, decoy kind and NO-HARD kind with CI against base 4B and baselines: always-YES, majority, sanitiser-presence rule, token-"escape/quote" keyword rule |
| T65-R2 | Twin consistency: both members of a pair correct; flip under the one-token edit |
| T65-R3 | Juliet slice accuracy (no official split; internal CWE-family hold-out used) separately from the generated block; generated-to-Juliet transfer gap |
| T65-R4 | Accuracy by ladder level L1-L4 vs base 4B and trivial baselines |
| T65-R5 | CWE head accuracy and confusion |
| T65-R6 | Order-invariance flip rate with CI; ECE and Brier |

## 8. Clean-room notes

- Built only from the plan, LANE_L-P, the stripped codeexec excerpt and the approved G0 files. No vulnerability database, advisory, benchmark item, Juliet file or textbook vulnerable-snippet collection was opened. CVEfixes, BigVul, PrimeVul and MoreFixes are removed sources and appear only as G13 TARGET names.
- No CVE or advisory text, no product-and-version claim, no real exploit tooling: PAY-* canaries only, executed only in the egress-deny sandbox. Code is produced by program templates; no model writes, labels or checks a row. Entity names are seeded (TRAINING salt); standard-library API names are real names from the L-0 export.
- Juliet code is used only after the scrub; the public-domain / CC0 statement is quoted in the record; no CVE id is derived from it (guard F2). Writers (Haiku wording pools) get the question forms and slots, never the literal-ban list. G13 hit reports carry row ids, target name and method only.

## 9. NAMES this family needs (names only; for manifest v1.2, due Fri 23 12:00; family id T65 must be ADDED to row_job_families_allowed in v1.2)

- Languages: python, javascript, typescript (conditional on the Node type-stripping self-test; otherwise folded into JS), go (existing). Juliet rows: C, C++, Java, C# as real-name language labels under the P1-realism exemption (the guard's language list may need these four added under the exemption; O-T65-4).
- Runners (harness names; new ids): runner.canary_harness.python, runner.canary_harness.javascript, runner.canary_harness.go; runner.python_isolated (existing). Parse-only tools (never in rows): tree-sitter (MIT), Python ast, Go go/parser.
- Definition cards: defs_card.t65.vuln, defs_card.t65.cwe.
- Carriers: FUNC_CONTEXT; reused: SRC_FILE, OPTIONS, QUESTION_FORM.
- Registry ids (hash export): T65-Q-VULN, T65-Q-CWE (>= 50 wording ids each); CWEC-22, CWEC-78, CWEC-79, CWEC-89, CWEC-117, CWEC-295, CWEC-327, CWEC-377, CWEC-601; SAN-* (one or more per class and language, builder fixes the list from the pinned toolchains' documentation); DS-1..DS-6; NS-1..NS-4; PAY-22, PAY-78, PAY-79, PAY-89, PAY-117, PAY-601; M-FLOW, M-HELP, M-DECOY, M-LOOK; levels L1-L4.
- Standard-library API names for sinks and neutralising steps: taken from the L-0 stdlib symbol export (names only, v1.2); not hand-listed here.
- Namespace slot kinds used (all existing): ns.noun.entity, ns.noun.field, ns.noun.module, ns.noun.symbol, ns.path_stem, ns.table, ns.column, ns.endpoint, ns.handle, ns.variable. No new kind.
- G13 targets to register before any row (names only): the Juliet CWE-family hold-out (internal); removed-source names CVEfixes, BigVul, PrimeVul, MoreFixes; public secure-code and vulnerability-detection sets found by the L-0b registry scout (candidate names from memory, existence and licence UNVERIFIED: DiverseVul, Devign, SecurityEval, CyberSecEval insecure-code subset); the standing list.
- R5 candidate list (names only): Juliet Test Suite 1.3 (already LR-03).

## 10. Risks

1. Sanitiser-presence is the obvious shortcut. Mitigation: decoys (>= 40% of YES), sanitiser-free NO rows (NS-2, NS-3), K4 probe and parity.
2. Static-only classes (295, 327, 377) have a pattern engine on both sides (A and B are independent code but the label notion is shared); the K3 agreement is weaker evidence than an execution witness. Mitigation: their share is 32%; the report separates them.
3. Canary execution inside a sandbox: command-injection rows run a shell echo. The sandbox is disposable, egress-deny, no data; payloads are registered canaries (K14).
4. Juliet scrub residue: flow-variant structure (numbered variants) can still separate good from bad. Mitigation: length parity, surface probe grouped by test case, one fix, else left out.
5. Synthetic rows are cleaner than real code; transfer to real code is untested (the Juliet slice and R3 measure a first step, not real-world detection). The report says so.
6. Language coverage gaps (CWEC-89 in Node, SQL driver absence in Go): the class-by-language matrix is fixed by the builder before the pilot.
7. Sandbox throughput: 3 runs per dynamic row (about 410 rows) plus solver B's own runs; L-0 owes the number by Wed 21.

## 11. One fix iteration and kill rule

- G3 governs. Allowed fix levers: generator parameters, quotas, decoy and NO-HARD kind mix, scenario distinctiveness, wording pools, AFLite-style repair (filtered <= 30% of the family, reported), raising ladder HIGH settings; for Juliet the one re-selection of good variants; NOT the bars.
- Kill (standard P1 rule): any PRE-FREEZE gate still failing after the fix, or not through all of them by the data freeze (Mon 2 Nov 23:59 UTC; stretch Fri 30 Oct) -> T65 rolls to C2.2 / C3 with the failing gate and numbers logged. G4: no head rolls alone inside the generated block (a CWE-head failure rolls T65). The Juliet slice is an L-R dataset: if it fails K10 after its one fix it is LEFT OUT (logged) and does not roll the generated block (O-T65-2). POST-TRAINING lines are never kill rules. First in the usage shed order after the research pass.
- Timeline: approval by Fri 23 (needed before the LR-03 mapper runs); generated dynamic-class rows after the sandbox sign-off (Wed 21) and the Sat 24 18:00 rules; rows from Sun 25.

## 12. Open questions for Opus

- O-T65-1 Size of the generated block: 600 is a design value (300 pairs). Keep, shrink to 400, or 0 (Juliet only)?
- O-T65-2 Confirm that a failed Juliet slice is left out as a dataset and does not roll the generated block (G4 reading).
- O-T65-3 Static-only classes (295, 327, 377): accept that solver B is an independent pattern engine, or drop them (the generated block would be 6 classes, 100% execution witness)?
- O-T65-4 Juliet rows are C / C++ / Java / C# code; the names guard's language list has none of them. Confirm they enter under the P1-realism family-field exemption (no execution; labels from the dataset).
- O-T65-5 Pilot size for families under 1,000 rows: 50% of the generated block, floor 300.
- O-T65-6 Registered canary payloads PAY-*: confirm that running them in the egress-deny sandbox is inside the plan's "execution only on the disposable sandbox" rule.

## 13. Conformance seed (plan 16.1 step 0)

| Clause | Obligation | CPU test id |
|---|---|---|
| G1 | solver B imports stdlib + row schema (+ parse libraries); no model client | T65-CM-01 |
| G3 | parameter file sha frozen at pilot launch; later change needs the fix-iteration flag | T65-CM-02 |
| G5 | probe calls: grouped split, 97.5th-percentile bound, permutation and leak checks | T65-CM-03 |
| G6 / GV4 | row > 1,536 tokens refused at creation | T65-CM-04 |
| GV5 | G13 drop retires the spec and the whole twin pair and its head row | T65-CM-05 |
| 2.1 | label function; neutralising-step validity rules; twin edit equals spec | T65-CM-06 |
| 2.1 | witness: 3 identical runs, registered payload only; sandbox only | T65-CM-07 |
| 2.2 | Juliet scrub, pairing, length parity, hold-out before mapping | T65-CM-08 |
| K5 | banned-word scan of our identifiers and comments | T65-CM-09 |
| K9 | guard F2 scan: no CVE / GHSA / NVD text; no CWE number in prompts or code | T65-CM-10 |
| K21 | no permission option; no local execution of generated code | T65-CM-11 |
| 6 | pool writer refuses any row without a current clean stamp and an answer-check record | T65-CM-12 |
| 3.6 | A10 / A12 / A14 / A15 / A16 not carried; A1 hook fields present | T65-CM-13 |

## Opus batch-1b rulings v3.2 (Opus 5.5 high, Sun 18 Oct 2026 UTC; families/G0_APPROVALS_v32.md "Batch 1b")

VERDICT: REVISE -> APPROVED after the 2 fixes below (applied in this file, marked "[Opus b1b ...]"). Generator, taint
engine, solver B, canary harness and probe CODE may start now; Juliet mapper code only after the LR-03 S-pre PASS; dynamic
rows only after the od-sbx1 sign-off; every row only after the OHS-5 freeze, the registry sha, manifest v1.2, a signed
stamp service and a signed conformance record (Sat 24 18:00 rules unchanged). T65 is added to row_job_families_allowed
in manifest v1.2.

Must-fix (applied):
- T65-M1 JUL-CWE is an L-R question form on the dataset's own CWE label (LR-03 names both forms), not a G7 head row, drawn
  from test cases not used by JUL-VULN. Reason: G7 head rows are extra copies of the same context from <= 25% of specs and
  sit outside the size; 200 head rows on 250 Juliet pairs would break both rules.
- T65-M2 the Juliet scrub and K10 scan cover macros, string literals and include names, and (for JUL-CWE) class-name words.
  Reason: Juliet source carries good / bad markers and the CWE class name outside identifiers and comments.

Binding conditions:
- T65-B1 O-T65-1: keep 600 generated rows (owner "all data"; the measured Mon 26 projection and the money shed order decide
  any cut, never an estimate).
- T65-B2 O-T65-2 -> GV11 (Juliet left out alone; if T65 is killed, the Juliet slice goes with it).
- T65-B3 O-T65-3 accepted: the static-only classes keep an independent AST pattern engine as solver B (the plan's gold for
  T65 is static taint); the report separates them (R1).
- T65-B4 O-T65-4 accepted: Juliet rows (C, C++, Java, C#) enter under the P1-realism family-field exemption; the four
  language labels are recorded in manifest v1.2 as a scoped NON-GUARD list (p1_realism_language_labels), never added to
  the closed `language` category, so no non-realism row may use them.
- T65-B5 O-T65-5 -> GV10: pilot = 50% of the 600 generated rows = 300, proportional by class and language; Juliet has no
  pilot (set-level checks once per built dataset slice).
- T65-B6 O-T65-6 confirmed with conditions: every PAY-* literal is registered and hashed before the first dynamic row; the
  harness asserts the sandbox egress-deny state before each batch; PAY-601 is witnessed in process by reading the
  redirect target value (no request is made and no name is resolved); PAY-89 runs only against the in-memory two-row
  database; no payload exists outside the registry (K14).
- T65-B7 The canary harness ids runner.canary_harness.python / .javascript / .go are guard names in manifest v1.2.
