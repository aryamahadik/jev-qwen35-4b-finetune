# G0 ADDENDUM v3.2: T42c CODE-EXEC (lane L-C; clean-room; 3,000 rows kept; compile / type-check head by substitution)

Status: DRAFT for Opus batch 1 (Mon 19 Oct 2026). Written Sun 18 Oct 2026 by the L-C Sonnet author (v3.2 addendum pass).
Design only: no rows, no generated code, no execution, no download, no model call, no Modal. Every identifier below is a
NAME for the names-only manifest or a registry id, never a row value.
Binds over: families/T42c/G0_LITE.md. Where this addendum and the G0-lite body disagree, this addendum binds. The "Opus
rulings 18 Oct" block at the end of the G0-lite (G1-G10 and the T42c decision) stays in force and is carried below.
Sources, each tagged where used: [OWNER-ROW] (owner 18 Oct: check each row when it is made), [LEV A10], [LEV A16],
[LEV A1, A2] (inherited L-0 tools), [CRIT C2] (compile / type-check head), [CRIT D1, D2] (difficulty ladder), [INV C14]
(MBPP), [A79 R6], [A82 7] (CDLA, not used here), plan 16.1 (stamp pipeline), plan 16.3 rule 4 (names exemption), Sk 8, Sk 23a.
Read for this addendum: build order (L-C block and v3.2 L-C lines); plan sections 1 (B.8, E), 2, 5, 6, 7, 8, the
PRE-REGISTERED RULES block of section 3 only, and 16; EXTRA_LEVERS 1; PUBLIC_TRAIN_INVENTORY (C14 row and section 4 T42c
row); families/G0_APPROVALS.md; the T42c G0-lite. NOT opened: any T27/T40-T46/T42/T43 generator, template or wording
pool, mutate.py, OHS-AC, any "ohs" or "sealed" path, OHS5_BRIEF_DRAFT.md, the rest of plan section 3, C2 build files,
data/, logs/, ~/.claude, or any benchmark item text. Public benchmark names appear as G13 TARGET NAMES only.

## 1. Rulings carried word for word (families/G0_APPROVALS.md, Round 1; Round 2 added nothing for this family)

Global rulings G1-G10 apply to this family. Their full text sits unchanged in the "Global rulings" block at the end of
families/T42c/G0_LITE.md (byte-identical to G0_APPROVALS.md). One-line index of the ones this addendum leans on:
G1 solver B is CODE (a separate Sonnet high session; stdlib + row schema only); LLM reads are audits and never set a
label. G2 A50 G6, A49c, G5-H, G3-H, A43(d) are PRE-FREEZE data-audit gates. G3 no free pilot tuning: the 1,000-row pilot
is the first measured look, then ONE combined fix. G4 no head or sub-block rolls alone in C2.1. G5 one probe harness
(grouped split, L2 logistic regression, AUC as max(AUC, 1 - AUC), 97.5th-percentile cluster-bootstrap bound over 2,000
resamples, balanced accuracy for k-way, permutation sanity 0.50 +- 0.03, injected-leak power check >= 0.80); GBT advisory.
G6 token rule: mean <= 800, none > 1,536, > 1,024 on <= 10% of the family. G7 secondary heads are head rows (T42c has
none). G9 cross-family label consistency (T42c is not an action gate; not in the test). G10 decision_spans export (T42c
has no natural-language user utterance; nothing to export; recorded so the conformance map can say "not applicable").

T42c decision (Opus, copied word for word):

> Rulings: (a) 3 identical runs for OUT4 and TFAIL2 witnesses override the sandbox default (the plan's witness rule wins).
> (b) the per-language step counters are approved; the 10% Python agreement check on 100 programs is a CPU/sandbox test that
> must pass before any row. (c) the yield floor (< 80% kept triggers the fix iteration) is approved. (d) see G3: not
> approved as written; section 9 is rewritten to G3. (e) authored failure markers for Go and bash are approved. (f) GBT
> probes are advisory (G5).
> Note: the exact toolchain patch versions and image digests from the L-0 image record are appended to this G0-lite (and
> to T57 and T56g) before the first non-Python row (plan section 2: "pins go into the G0-lites before any non-Python row").

Probe protocol reading (binds over G0-lite section 5 header): G5 replaces "5-fold group CV ... 95% bound". Every
PRE-FREEZE probe below uses the G5 harness with groups = base module id (COMPILE2: pair group id, then module id).

## 2. What changes in v3.2 (one line each)

| # | Change | Source | Effect on size |
|---|---|---|---|
| 1 | NEW head COMPILE2 "will this build / type-check pass" (Python, TypeScript, Go; no bash) | [CRIT C2] | 300 rows, by substitution |
| 2 | Cue-invariance wrapper rows (A10), conditional on the Fri 23 Oct free probe | [LEV A10] | about 150 rows by substitution (5% of each head); about 60 held-out-wrapper dev rows outside the size |
| 3 | Source-as-observation views (A16) | [LEV A16] | 5% of each head re-rendered, 0 extra rows; about 30 held-out-format dev rows outside |
| 4 | Difficulty ladder L1-L4 with a measured bar (C2 <= 70% on L4) | [CRIT D1, D2] | 0 rows (shifts the mix inside heads) |
| 5 | CHECK AT GENERATION: every row answer-checked and G13-stamped when it is made; the 200-row G13 pilot is gone | [OWNER-ROW] plan 16.1 | 0 rows; replaces K16 / K17 / section 9 wording |
| 6 | Templates addressable for the L-0 gold-bug audit and the AFLite-style repair | [LEV A1, A2] | 0 rows |
| 7 | Contract for the MBPP realism slice L-R will map into T42c's TFAIL2 form | [INV C14] | 0 rows in T42c (counted in L-R) |
| 8 | Ruling-to-code conformance seed (clause list) | plan 16.1 step 0 | 0 rows |
| 9 | Not carried: A12 (build order gives it to L-A, L-I, L-T), A14, A15 (see Opus item 6) | build order | none |

## 3. Sizes by substitution (family total stays 3,000 kept rows)

COMPILE2 takes its 300 rows from the three execution heads pro rata to their 40/30/30 shares.

| Head | G0-lite rows | v3.2 rows | YES / NO (or letters) | Notes |
|---|---|---|---|---|
| OUT4 | 1,200 | 1,080 | exception-gold 25% = 270; value-gold 810 | letters 25% +- 3 pp |
| EQV2 | 900 | 810 | YES 405 / NO 405 | hard-NO >= 20% of NO |
| TFAIL2 | 900 | 810 | YES 405 / NO 405 | |
| COMPILE2 | 0 | 300 | YES 150 / NO 150 | question form T42c-Q-COMPILE2 |
| Total | 3,000 | 3,000 | | |

Language split (replaces G0-lite section 4 per-head split; Python <= 75%, JS/TS >= 8%, Go >= 8%, bash >= 8% all hold):
| Head | Python | JS/TS | Go | bash | Total |
|---|---|---|---|---|---|
| OUT4 | 852 | 72 | 60 | 96 | 1,080 |
| EQV2 | 639 | 54 | 45 | 72 | 810 |
| TFAIL2 | 639 | 54 | 45 | 72 | 810 |
| COMPILE2 | 120 | 90 | 90 | 0 | 300 |
| Total | 2,250 (75.0%) | 270 (9.0%) | 240 (8.0%) | 240 (8.0%) | 3,000 |
Bash is not in COMPILE2: bash has no compile step, `bash -n` is syntax-only and would teach "syntax only", and ShellCheck
is never gold. Denominators: K4 (trace bins), K5, K6, K10 (letter and exception shares) and the per-language trace-bin
warning use the 2,700 execution-head rows; COMPILE2 has no trace length (its bin field is "n/a"). K11 uses all 3,000.

Extra copies outside the 3,000, unchanged from the G0-lite: +20% order-invariance copies (OUT4 random non-identity
permutation; binary heads reversal, COMPILE2 included). Reuse limits unchanged (<= 4 rows per base module per head, <= 6
overall), counting wrapper and view copies (A10, A16) as rows of their base module.

Quotas are counted AFTER drops. Every cell with a quota (COMPILE2 YES/NO per language, hard-NO, L4, wrapper cells) is
oversampled by 15% at generation (fixed now, not tuned on the pilot), so a stamp or answer-check drop cannot break a
quota by itself (the T53 Round-2 lesson).

## 4. The COMPILE2 head (new)

### 4.1 Decision and label set
Question form T42c-Q-COMPILE2 (>= 50 wording ids, none above 2%). The row shows 1-3 small application-style source files
and a TOOLCHAIN card naming the check configuration (fixed ids, below). Question: "with this configuration, does the
check pass with no errors?" Label YES (exit status 0 and no error diagnostics) / NO (any error diagnostic). Warnings are
off or non-failing by configuration. No secondary head (the error class stays a manifest field and a report line, G7).
Labels are the checker's verdict, never an author intent.

### 4.2 Toolchains and gold (execution gold; no model writes or checks a label)
| Language | Check | Config id (policy card id) | Notes |
|---|---|---|---|
| Python 3.12.x | a permissive static type checker, chosen ONLY after the component-licence check (4.3) | card.t42c.chk_py | strictness flags fixed in an executor-owned config file (checks untyped bodies, no implicit-Any leniency beyond the listed escapes); error-code set limited to the closed class list |
| TypeScript on Node 24.x | `tsc --noEmit` with an executor-owned tsconfig (strict) | card.t42c.chk_ts | TypeScript is Apache-2.0 (UNVERIFIED here; the licence record re-quotes it). Independent of the Node type-stripping self-test: tsc is a separate tool, so COMPILE2 TS rows exist even if TS rows are folded into JS in the other heads |
| Go 1.26.x | `go vet ./...` (type-checks the package and runs the vet analyzers) with `GOFLAGS=-mod=vendor GOPROXY=off GOTOOLCHAIN=local` | card.t42c.chk_go | analyzer set pinned by the toolchain patch; a NO caused only by an analyzer outside the registered list GO-AN-1..n (builder fixes the list from the pinned toolchain docs) is dropped, counted |
ShellCheck, hadolint and any other linter are never gold (plan). The tool's diagnostic text, error codes and tool name are
never rendered in a row (K23 scans for them).
Execution rule: THREE runs with identical exit status AND identical set of error classes (closed list CT-E1..CT-E10
below); timeouts and any disagreement are dropped and counted. Image id, runsc and kernel versions, checker name and
version, config sha and the L-0 image record are in every manifest. Exact patch versions and digests come from the L-0
image record and are appended before the first non-Python row (ruling note).

### 4.3 Type-checker component-licence check (first task, before any COMPILE2 code runs on a row)
A record per component of the chosen Python checker: the package, every runtime dependency, any bundled stubs or standard-
library type data, and any compiled part. Each gets licence quote + URL + fetch date. Rule: every component MIT, BSD-2,
BSD-3, Apache-2.0, PSF, ISC or CC0 passes. Any GPL, LGPL, AGPL, NC, unknown or missing licence = that checker is out. Any
MPL-2.0 component goes to an Opus ruling (the checker is an offline tool and its output is a yes/no label plus a closed
error class, with no tool text in any row, but the plan treated Hypothesis as barred, so the planner decides). UNVERIFIED
from memory, to be confirmed by the record: some current checkers pull in an MPL-2.0 file-matching dependency. Candidate
checker names for the record are NAMES only (see section 11); the lane builder picks the first that passes. Gate K21.
Fallback if no Python checker passes by Fri 23 Oct: the 120 Python COMPILE2 rows move to TS and Go (TS 150, Go 150; the
head stays 300; family language shares still hold: Python 2,130 = 71.0%, JS/TS 330, Go 300) and Opus confirms this
substitution; if TS or Go fail their own record, the head's rows revert to the three execution heads pro rata. Reason: the
checker is a missing INPUT, not a failed gate, so G4 is not triggered (Opus item 2).

### 4.4 Row construction (generate-then-check; a registry id per construction)
NO constructions (error classes, closed lists per language; the generator inserts exactly ONE error into an otherwise
passing application-style module; matched YES twin = the same module with the error token fixed):
CT-E1 argument type mismatch; CT-E2 return type mismatch; CT-E3 arity (missing or extra argument); CT-E4 undefined name or
unknown attribute; CT-E5 nullable used without narrowing (Python, TS; not Go); CT-E6 incompatible assignment to a declared
type; CT-E7 missing return path; CT-E8 unused import or variable (Go only: a compile error there; off by config in
Python and TS); CT-E9 wrong element or generic type; CT-E10 interface / protocol not satisfied. Each language uses >= 5
classes; no class above 25% of the NO rows; errors appear at three distances from their cause (same line / one call away /
two definitions away, the ladder parameter M-CT).
YES constructions: CT-OK-1 plain correct typed code; CT-OK-2 narrowing guard or early return that satisfies the checker;
CT-OK-3 suppression comment on a real error (<= 10% of YES rows, the same comment rate on NO rows within 3 pp); CT-OK-4
explicit escape (cast, Any, unknown, interface{} assertion) that is legal; CT-OK-5 structural or duck-typed compatibility
that looks wrong; CT-OK-6 type-correct but logically wrong code (types cannot see it, so the answer stays YES).
All Python rows are fully annotated (K23 annotation-parity), so "no annotations, so nothing is checked" is not a cue.
Minimal pairs: >= 50% of COMPILE2 rows are in a pair whose two modules differ by one token or one short expression and have
opposite verdicts (plan floor 30%). Reuse: one error per module, <= 4 rows per base module per head.

### 4.5 Solvers
Solver A: generator spec expectation + executor (mode 1: checker run from the module root with the config at the executor-
owned path). Solver B (G1: CODE, separate Sonnet high session; sees only this addendum, the G0-lite and the row schema;
imports stdlib + schema only): its own driver invoking the same pinned checker in a different invocation form (different
working directory layout, config passed another way, environment scrubbed independently), its own exit / error-class
parser. Agreement required on 100% of kept rows among A, B and the spec expectation; disagreements dropped and counted;
a block with > 2% dropped for disagreement returns to the generator (as K3). A construction id whose realised verdict
differs from its spec expectation on > 10% of its candidates returns to the builder.

## 5. A10 cue-invariance wrapper rows [LEV A10] (conditional)

Precondition: the Fri 23 Oct FREE PROBE (orchestrator, 200 wrapped items built from C2's existing dev rows, read by C2 on
od-l4b; share written before the read) says "build". Decision recorded by Sat 24 Oct 18:00 UTC, before any row is rendered
(a later change would be a template change and a stale hash export). If it says "do not build", T42c has 0 wrapper rows
and the substitution budget returns to the base rows.
Design (all wrappers are text in a source comment or docstring beside SRC_FILE / PROGRAM_PAIR / TEST_FILE; never in the
QUESTION_FORM, DOMAIN_DECL, OPTIONS or TOOLCHAIN card; T42c has no consent signal, so none is excluded):
- Wrapper families W1 authority claim, W2 urgency, W3 role-play, W4 fake "already checked", W5 benign justification.
  Trained: W1, W2, W4. HELD OUT (never trained, dev only): W3, W5. (Drawn by seeded draw before any pilot; the seed and the
  result are recorded in the pre-pilot parameter file.)
- Each wrapper asserts an answer ("returns ...", "equivalent: yes", "type-checks"). The asserted answer is correct on 50%
  +- 5 pp of wrapped rows and wrong on the rest, so a cue carries no label information.
- Size: 5% of each head, rounded (OUT4 54, EQV2 41, TFAIL2 41, COMPILE2 15; about 151 rows), 3 trained families about equal,
  by substitution. Every wrapped row has its clean twin among the family's base rows (same module, same gold). Held-out
  wrapper dev rows: 30 base rows per held-out family = 60 rows, eval only, outside the 3,000.
- A row gets at most one of A10 and A16.
Gate K24 (PRE-FREEZE KILL): wrapper presence vs label parity <= 3 pp (binary heads; letter distribution for OUT4);
asserted-answer-correct share 50% +- 5 pp; asserted-answer-only probe AUC <= 0.55 / upper <= 0.60 (binary) or acc <= 28% /
upper <= 31% (OUT4); wrapper share 5% +- 1 pp per head; 0 held-out-family rows in the training pool.

## 6. A16 source-as-observation views [LEV A16]

T42c has no tool-output carrier by design (captured outputs would be the answer). A16 is therefore applied to how the
source is OBSERVED: SRC_FILE rendered as a file-read result. View registry OBS-GUTTER (line-number gutter), OBS-CRLF (CRLF
endings), OBS-ANSI (ANSI colour around tokens), OBS-WRAP (long lines wrapped with a continuation marker), OBS-TAB (leading
indentation as tabs; Go, JS/TS and bash only, never Python), OBS-BANNER (path and line-range banner). One format is held out
by seeded draw before the pilot (dev only). 5% of each head (about 151 rows) is re-rendered by substitution, evenly over the
trained formats; held-out format dev rows 30, outside the size; 0 extra trained rows.
Label preservation, by program on every row: the de-rendered view is byte-identical to the original source (all formats);
for OBS-TAB the witness is re-run on the rendered source (3 runs) and must agree. The perturbation never touches the
checker input of COMPILE2 differently from the displayed text (the checked text IS the de-rendered text).
Gate K25 (PRE-FREEZE KILL): round trip 100%; OBS-TAB witness agreement 100%; label rate parity across formats <= 3 pp;
format-only probe AUC <= 0.55 / upper <= 0.60; 0 held-out-format rows in training. Opus item 5 (default ON at 5%).

## 7. Difficulty ladder L1-L4 [CRIT D1, D2]

Mechanisms (hardest-questions targets for T42c, program parameters only; copied as mechanisms, never as items). Each has a
LOW and a HIGH setting:
| Id | Mechanism | LOW | HIGH |
|---|---|---|---|
| M-TRACE | executed steps | 10-14 | 15-40 and above (the 15-40 band is the hard one) |
| M-STR | exact string assembly | 1-2 format steps | >= 4 steps incl. padding, truncation, separator edge |
| M-NAME | misleading names | one name mismatches behaviour | >= 3, or two names swapped between functions |
| M-OBO | off-by-one compare | one boundary | two interacting boundaries (<= vs < with index offset) |
| M-ALIAS | aliasing through two names | one alias | mutation through the other name plus a copy-vs-reference mix |
| M-POST | post-loop value | value after normal exit | value after break / continue / else path with loop-variable reuse |
| M-DCE | dead-code removal that depends on state (EQV2) | branch dead in all states | branch dead only under the declared domain, or live after one earlier call |
| M-XSIM | similarity crossing (EQV2) | on-diagonal cells (large change and equal; small change and unequal are the HARD cells) | the two off-diagonal hard cells |
| M-HELP | helper two calls away (TFAIL2) | one call away | two or three calls away |
| M-CT | error far from its cause (COMPILE2) | same line | two definitions away |
Row level (assigned by program, recorded in the manifest, never from a model score): L1 no mechanism active; L2 one mechanism
at LOW; L3 one at HIGH or two at LOW; L4 two or more at HIGH, or one HIGH plus M-TRACE HIGH. Composition (set-level,
PRE-FREEZE): L1 20% / L2 30% / L3 30% / L4 20% (each +- 5 pp), so L3-L4 = 50% (floor 25%), per head L3-L4 >= 25%.
TWIN rule: every L3 / L4 row is paired with an easy-looking twin of the opposite label (binary heads) or of a different
gold option (OUT4) that differs by <= 1 token; twins cover >= 50% of L3-L4 rows (they count inside the 30% matched-pair
quota). The quad (alarming / calm x risk present / resolved) is not mandatory for T42c.
MEASURED BAR (gate K27, once, on the 1,000-row pilot): C2 (C1 if C2 has no weights), read on od-l4b, scores <= 70% on the L4
rows (base 4B read beside it). It is a model-based gate, so by skeptic 6 it is NOT a kill: a miss is folded into the ONE
combined fix (G3) by raising the HIGH settings of the program parameters (never by dropping rows by model score); after the
fix a miss is a report line.

## 8. CHECK AT GENERATION [OWNER-ROW] (plan 16.1)

Owner, 18 Oct (binding): "If you're building one row, check that row at that same point and that's it ... then train."
Replaces: T42c-K16's "200-row G13 pilot (<= 1% hit)"; T42c-K17's reading; and the first bullet of G0-lite section 9
("after the 200-row G13 pilot every change consumes the fix iteration"; "CPU gates K1-K15 are run FIRST, before the G13
pilot is queued").
New rule: every row is written to the family pool ONLY through the stamp wrapper. Per batch (<= 500 rows, same day):
(a) ANSWER CHECKS, per row, before stamping: manifest complete (K1); witness rule of its head satisfied (OUT4 3 runs
identical; EQV2-NO distinguishing input; EQV2-YES transform id + exhaustive run; TFAIL2 3 runs agree; COMPILE2 3 runs
identical status + class set); solver A = solver B = spec expectation (100%); OUT4 options distinct and gold unique;
generator lint (K12); names guard (K15, closed allow-list incl. the new ids in section 11); token rule G6 per row (> 1,536 =
refuse); PII scrub; exact-duplicate refusal on the AST-normalised hash and the reuse ledger (<= 4 per base module per head,
<= 6 overall) enforced AT CREATION; executed-step count from the twin run and bin recorded; ladder level, wrapper / view
ids and A1 fields (template id, wording id, construction / operator / transform id) recorded; round trip for A16 rows.
(b) G13: the batch goes to the stamp service, which checks every row against every registered target with every method
listed for that target (the registry sha is bound; the R6 sha-bound scaffolding exemption applies; OHS-AC binding for new
rows; OHS-5 hash-export targets use exact and hashed n-gram methods only).
(c) The stamp (row id, registry sha, method-set version, generator code sha, verdict) is written into the row manifest.
A failed row is dropped and logged (row id, target name, method; never the matched text). No unstamped or failed row enters
the pool. A template, renderer, wording-pool or cue-pool change after hash export v1.1 means a new hash export and
re-stamped rows (plan 16.1 step 6): the cue pool, view renderers and COMPILE2 wordings are in the export.
FIX TRIGGER (all rows, not a sample): more than 1% of the rows of the 1,000-row pilot, or of any full-generation day,
dropped for a reason other than exempt scaffolding or OHS-5 collisions = the family's ONE combined fix (G3). OHS-5
collisions are dropped row by row and are not the fix iteration while <= 5% of the family. Answer-check drop rates use the
G0-lite bars (block drop > 2% for disagreement returns the block; kept yield < 80% of 3,000 = fix iteration).
Code-idiom note: short idiomatic programs can match public execution-prediction sets by accident. L-C does not whitelist
anything; per-method drop counts are reported, and if idiom-driven drops exceed 1% the ONE fix may raise module
distinctiveness (application-style vocabulary, more state), never relax a bar.
Set-level checks (ONCE per family, on the 1,000-row pilot and once on the built family; not repeated at the mix): A50 G6 at
size, A49c balance, wording variety (>= 50 per form, none > 2%), matched-pair share, K4-K11, K13, K22-K27 probes, the
ladder composition and measured bar, G5-H (two Haiku solvers on 300 rows + one Haiku read of 100% free-form wording), G3-H,
Opus A43(d).
Then C2 reads on od-l4b (pipelined: trap selection, A1 template audit); not a kill gate. AFLite-style repair [LEV A2] may be
used as the ONE fix tool when a shortcut probe misses (filtered <= 30% of the family and reported; it counts as the fix
iteration).

## 9. Gates added or changed (G0-lite ids kept; new ids continue the sequence)

Probe protocol is G5 throughout. "PK" = PRE-FREEZE KILL (CPU or sandbox, data only). "PR" = POST-TRAINING REPORT.
| Id | Gate | Bar | Class |
|---|---|---|---|
| T42c-K4, K5, K6, K10 | as G0-lite, denominators = the 2,700 execution-head rows | as G0-lite | PK |
| T42c-K11 | quotas on all 3,000: pairs >= 30%, invariant >= 15%, near-miss >= 10%; language shares as section 3 | as stated | PK |
| T42c-K16 (replaced) | A50 G6, A49c, G5-H, G3-H, A43(d) per plan; the G13 line is replaced by K28 | per plan | PK |
| T42c-K18 | COMPILE2 witness: complete manifest; 3 runs identical in status and class set | 100% | PK |
| T42c-K19 | COMPILE2 spec expectation: realised verdict = construction expectation; per-id mismatch <= 10% (else the id returns) | kept rows 100% | PK |
| T42c-K20 | COMPILE2 solver A = solver B (different invocation form) | 100% of kept; block drop > 2% returns block | PK |
| T42c-K21 | Python type-checker component-licence record clean before any COMPILE2 row (4.3) | 100% components clean or Opus-ruled | PK |
| T42c-K22 | COMPILE2 balance and quotas: YES 40-60% overall, per language, per error group; NO class <= 25% of NO rows; >= 5 classes per language; suppression <= 10% of YES rows with comment-rate parity <= 3 pp; pairs >= 50%; language shares 40 / 30 / 30 +- 5 pp | as stated | PK |
| T42c-K23 | COMPILE2 shortcut probes: surface features (length, tokens, annotation density, Optional / None / Any counts, imports, identifier stats, suppression comments) | AUC <= 0.55, upper <= 0.60; annotated-module share equal across labels <= 3 pp; 0 diagnostic text, error codes or tool names in rendered rows | PK |
| T42c-K24 | A10 wrapper gates (section 5) | as stated | PK |
| T42c-K25 | A16 view gates (section 6) | as stated | PK |
| T42c-K26 | Ladder composition and twin share (section 7) | L1 20 / L2 30 / L3 30 / L4 20 +- 5 pp; L3-L4 >= 25% overall and per head; twins >= 50% of L3-L4 | PK |
| T42c-K27 | Ladder measured bar: C2 (C1 if none) on L4 rows of the 1,000-row pilot | accuracy <= 70% | PRE-FREEZE FIX TRIGGER (model read on our own data, never a kill; after the fix a miss is a report line) |
| T42c-K28 | Check at creation (section 8): 100% of pooled rows carry a current clean stamp and an answer-check record; 0 unstamped rows | 100% / 0; drops <= 1% (other than exempt scaffolding and OHS-5 collisions <= 5%) or the fix iteration | PK |
| T42c-K29 | Reuse ledger and exact-duplicate refusal enforced at creation; near-duplicate rate stays K13 | 0 violations | PK |
| T42c-K30 | A1 / A2 hooks: template id, wording id, construction / operator / transform id on 100% of rows | 100% | PK |
| T42c-R6 | COMPILE2 accuracy per language and per error class vs base 4B, always-YES, majority, annotation-density logistic baseline, random | report (CI) | PR |
| T42c-R7 | Wrapper flip rate (wrapped vs clean twin); held-out wrapper accuracy gap | report (CI) | PR |
| T42c-R8 | Held-out view-format accuracy vs trained formats | report (CI) | PR |
| T42c-R9 | Accuracy by ladder level L1-L4 vs base 4B and trivial baselines | report (CI) | PR |
| T42c-R10 | MBPP realism slice accuracy (separate line, "train split seen") | report | PR |

## 10. MBPP realism slice: contract for L-R [INV C14]
L-R maps MBPP (full config, TRAIN split only, 374 problems, "CC-BY-4.0"; test, validation and prompt splits are registry-only
and never opened) into at most 300 rows of T42c-Q-TFAIL2 form: "will this stated test fail" on the dataset's human solutions
plus program mutants of them (our own mutator, operator ids MUT-01..MUT-14). T42c's requirements for those rows: execution
gold on od-sbx1 with THREE identical runs (same witness rule as TFAIL2); A = B; label = execution only; problem-level G13
against CodeMind sources and REval (and the MBPP test / validation / prompt splits, as registry-only targets); real names are
exempt (Sk 8: family field P1-realism); human solutions only from the TRAIN split. These rows are counted in L-R / P1 realism,
NOT inside T42c's 3,000 and NOT in its bars; they never roll T42c and T42c's roll does not drop them (Opus item 4).

## 11. NAMES (new, relative to NAMES_MANIFEST_V1; for manifest v1.1; ids as the v1 id scheme)
- runner ids: runner.python_typecheck (Python static type check, concrete tool recorded from 4.3), runner.tsc_noemit,
  runner.go_vet, runner.go_build (conditional: only if build-only rows are added; default unused).
- policy / card ids: card.t42c.chk_py, card.t42c.chk_ts, card.t42c.chk_go (toolchain cards), defs_card.t42c.compile2.
- carrier ids: CHECK_CARD (the rendered toolchain card), CUE_COMMENT (A10 wrapper comment; shared with T57, T56g).
- tool-only dependency names (never in rows): tsc (TypeScript compiler), go vet, and the Python checker chosen by 4.3;
  candidate names for the record, builder picks the first that passes: mypy, pyright, pytype, pyre.
- registry ids (not guard-checked; listed for the hash export): question form T42c-Q-COMPILE2; CT-E1..CT-E10, CT-OK-1..CT-OK-6;
  GO-AN-1..n; wrapper families W1..W5; view formats OBS-GUTTER, OBS-CRLF, OBS-ANSI, OBS-WRAP, OBS-TAB, OBS-BANNER; ladder
  mechanisms M-TRACE, M-STR, M-NAME, M-OBO, M-ALIAS, M-POST, M-DCE, M-XSIM, M-HELP, M-CT; levels L1-L4.
- languages: none new for P0 rows. The MBPP slice uses python only.
- row_job_families_allowed: T42c unchanged (COMPILE2 is a head, not a family).

## 12. G13 targets added (names only, to the registry before any row)
No new benchmark for COMPILE2 rows. For the MBPP slice (registry-only, via the L-0b registry program): MBPP test, validation
and prompt splits; EvalPlus MBPP+ (if the registry lists it); the existing CodeMind sources and REval. The standing list
(OHS-3, OHS-4, OHS-AC, OHS-5 once frozen, public eval targets, the T42c targets in G0-lite section 7) stays.

## 13. Fix iteration and kill rule
G3 governs (no free pilot tuning; the 1,000-row pilot through the stamp wrapper is the first measured look; ONE combined
fix). G4 governs (no head rolls alone). The kill rule is unchanged: a failed PRE-FREEZE KILL gate after the fix, or not
through by the data freeze, rolls T42c to C2.2/C3. COMPILE2 is 10% of the family, so a COMPILE2-only failure (for example
K22 or K23) would roll all of T42c under G4 and could cost the "one of T42c/T57" floor: this is recorded as Opus item 2.
Order inside L-C stays T42c, T57, T56g.

## 14. Conformance seed
Plan 16.1 step 0: the fresh skeptic maps each row to file:function and a CPU test; the record builder refuses to run without
the signed record for its code sha and this ruling sha.

| Clause | Obligation | CPU test id |
|---|---|---|
| G1 | solver B package imports stdlib + row schema only; no model client; a labeller never reads a model output | T42c-CM-01 |
| G3 | the generator parameter file sha is frozen at pilot launch; a changed sha after pilot-gate numbers exist needs the fix-iteration flag in the run record | T42c-CM-02 |
| G5 | probe calls use grouped split by module / pair group, 97.5th-percentile bound, permutation and leak checks | T42c-CM-03 |
| G6 | row > 1,536 tokens refused at creation; mean and > 1,024 share computed at set level | T42c-CM-04 |
| ruling (a) | OUT4, TFAIL2, EQV2 and COMPILE2 witnesses use 3 runs; a 2-run witness is refused | T42c-CM-05 |
| ruling (b) | step counters per language; 10% Python agreement on 100 programs passes before any row | T42c-CM-06 |
| ruling (c) | kept yield < 80% of 3,000 raises the fix-iteration flag | T42c-CM-07 |
| ruling (e) | Go and bash exception options are authored markers only; no raw runtime error text in any option | T42c-CM-08 |
| 4.2 | COMPILE2 rows carry checker, version, config sha, image id; no diagnostic text in rendered rows | T42c-CM-09 |
| 4.3 | no COMPILE2 row exists without a clean licence record for the chosen Python checker | T42c-CM-10 |
| 3 | quotas counted after drops; 15% oversample of quota cells | T42c-CM-11 |
| 5 | wrapper answer-correct share 50% +- 5; held-out families absent from training pool | T42c-CM-12 |
| 6 | A16 round trip 100%; OBS-TAB witness re-run | T42c-CM-13 |
| 7 | level assigned from mechanism parameters only (no model-score input); twins present | T42c-CM-14 |
| 8 | pool writer refuses any row without a current clean stamp and an answer-check record | T42c-CM-15 |
| Sk 8 | names guard: P0 rows keep the closed allow-list; no P1-realism exemption inside the 3,000 | T42c-CM-16 |

## 15. Risks (new)
1. A Python checker may not pass the component-licence check; the fallback shifts Python rows to TS and Go and needs Opus.
2. Checker verdicts depend on pinned versions and stubs; a patch bump changes labels. The image record pins them and the
   manifest carries them; a bump after rows exist re-checks every COMPILE2 row.
3. "Annotated vs unannotated" and "suppression comment" cues: gated by K23 and K22.
4. Go vet analyzers drift between patch releases: closed analyzer list; unlisted-analyzer NO rows dropped.
5. A10 wrapper claims in a code comment are close to the M-NAME mechanism; the probe K24 and the 50/50 correctness keep them
   from carrying a label.
6. A16 views add whitespace and gutter tokens (about +5% tokens on those rows); counted in the measured token projection.
7. COMPILE2 adds a third kind of execution (tool runs, not program runs) to the sandbox throughput number L-0 owes (Wed 21).

## 16. Items for Opus to confirm
1. Sizes by substitution (COMPILE2 300 = 120 / 90 / 90 out of OUT4 / EQV2 / TFAIL2) and the language table (bash 0 in COMPILE2).
2. A COMPILE2-only failure under G4 (whole-family roll) and the licence-check fallback (rows move to TS and Go, or revert).
3. Ladder rule (level from mechanism counts), 20 / 30 / 30 / 20 composition, and K27 as a fix trigger rather than a kill.
4. MBPP slice accounting (outside T42c's 3,000, P1-realism family field).
5. A16 applied to the source view at 5% (default ON), since T42c has no tool-output carrier.
6. A15 (format dialects of card bodies) is not assigned to L-C in the build order; T42c's toolchain cards are the only card
   bodies. Default: NOT carried. Say so if the cards should join the dialect sampler.

---

## Opus batch-1 rulings v3.2 (Opus 5.5 high, Sun 18 Oct 2026 UTC; source: families/G0_APPROVALS_v32.md; binds over this file)

Global rulings GV1-GV9 of families/G0_APPROVALS_v32.md bind this file (GV1 one A10 build rule: flip = predicted label differs
wrapped vs unwrapped, build iff >= 10 of 200, no result by Fri 23 18:00 UTC = not built; GV2 role-play and benign justification
held out in every lane; GV3 one A14 build rule: >= 5 pp gap and bootstrap lower bound > 0; GV4 G6 binds A14, no exemption; GV5 a
G13-hit row retires its spec and its whole group, never re-worded, triggers read first-pass drops incl. collateral; GV6 one
perturbation library pert.*, zero_width = U+200B only, fullwidth / bidi / upside_down held out everywhere; GV7 A15 dialect rows in
L-A only; GV8 pilot-pooled sub-block probes, built-family read binds; GV9 held-out dev rows never trained, mix guard excludes them).
VERDICT: APPROVE (no must-fix).
Binding conditions: T42c-B1 items 1, 3, 5 confirmed. T42c-B2 item 2: G4 binds; the licence fallback is approved (a missing input,
not a failed gate). T42c-B3 4.3: an MPL-2.0 component of a checker RUN unmodified as an offline tool is allowed (nothing modified,
vendored or rendered; K23), recorded in the licence record; GPL / LGPL / AGPL / NC / unknown stay out. T42c-B4 item 4: MBPP rows
are family LR-code, P1-realism, block R, outside the 3,000, T42c-Q-TFAIL2 form (LR-M7). T42c-B5 A10 held-out W3 / W5 are fixed by
GV2 (the "seeded draw" words are superseded); item 6 -> GV7.
