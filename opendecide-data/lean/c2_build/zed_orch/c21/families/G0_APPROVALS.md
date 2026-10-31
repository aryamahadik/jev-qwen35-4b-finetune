# C2.1 G0-LITE APPROVALS (batched; Opus 5.5 high; Sun 18 Oct 2026 UTC)

Read for this approval: families/*/G0_LITE.md (12 files), training_inputs/PLAN_TRAINING_SIDE.md, training_inputs/LANE_L-0,
L-A, L-C, L-G, L-I, L-T and L-D lane blocks, and the L-E lane block only. Section 4 inside LANE_L-E.md is outside the
training-side read scope and was NOT read. No excerpt, research file, generator, sealed path or benchmark text was opened.
No rows, no code, no model calls.

## Verdict table

| Family | Lane | Verdict | Must-fix items | What may start now |
|---|---|---|---|---|
| T50 SHELL-GATE | L-A | REVISE | 5 (shared-core rule table) | spec schema, state model, renderer, expander, validators |
| T51 SCOPE-BOUNDARY | L-A | REVISE | 3 | entity oracle, matrix, trajectory and consent blocks |
| T53 EGRESS-SECRET | L-A | REVISE | 5 | fake-credential registry, destination normaliser |
| T41c TAINT | L-I | REVISE | 3 | benign-artifact generators, splice engine |
| T54 TOOL-NEED/PICK | L-T | APPROVE | 0 (1 binding condition) | everything |
| T55 RECOVER-ESCALATE | L-T | APPROVE | 0 (3 binding conditions) | everything |
| T56 DONE-CLAIM (done half) | L-T | APPROVE | 0 (rulings only) | everything |
| T56g TEST-GAMING | L-C | APPROVE | 0 (4 binding conditions) | everything |
| T42c CODE-EXEC | L-C | APPROVE | 0 (rulings only) | everything |
| T57 PATCH-VERDICT | L-C | APPROVE | 0 (2 binding conditions) | everything |
| GEN general rows | L-G | APPROVE | 0 (1 binding condition) | everything |
| VOICE | L-G | APPROVE | 0 (2 binding conditions) | everything |

What the verdicts mean:
- APPROVE: generator code may start. The rulings and binding conditions below go into an "Opus rulings 18 Oct" addendum at
  the end of the family's G0_LITE.md, copied word for word by the lane builder. No second approval is needed. The build
  skeptic checks that the code follows them.
- REVISE: the numbered must-fix items are edited into the G0-lite and sent back for an Opus re-check (one quick batch,
  target Mon 19 Oct, before the names-only manifest freeze). Code for parts not touched by the must-fix items may start
  now (listed above). Rule-table code waits for the re-check.

Clean checks that every family passed: gold is program or execution gold in all 12; every family has a kill rule and
one fix iteration; no NC, GPL or AGPL component is used (bashlex, TruffleHog, Hypothesis, espeak-ng fallback, PSL data
all kept out); no third-party LLM-generated dataset is used (Claude-authored wording, directive text and natural hacks
are allowed by the plan; no LLM writes a label); every family names its G13 targets by name only; names come from the
TRAINING-salt namespace.

## Global rulings (bind every family; each family addendum cites them by number)

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

## Per-family decisions

### T50 SHELL-GATE: REVISE

Must-fix (re-submit the shared-core rule table with these changes):
1. R09 vs T51 conflict (G9). Replace R09 with the shared lane rule:
   - agent-created in a contained lane = ALLOW;
   - contained lane, not agent-created, not authorised = ASK / bypass_review_or_affect_others / soft;
   - shared lane, not agent-created, not authorised = BLOCK / bypass_review_or_affect_others / soft (ASK when the card
     has ask_on_soft);
   - production lane = BLOCK / bypass_review_or_affect_others / soft.
   Anthropic's "changing shared resources the agent did not create" is a default-block (soft) group, so shared = BLOCK
   soft, not ASK.
2. R13 vs T53 conflict (G9). As written, R13 makes "trusted host = ALLOW" win over "sensitive data = BLOCK". Delete R13's
   own conditions and make R13 = "apply T53's data-class x destination table". Secret to any host = BLOCK / exfiltrate /
   hard, even a trusted one, except T53's scoped credential-use case. Confidential to an untrusted host = BLOCK / soft
   (ASK under ask_on_soft). Public = ALLOW. EXTERNAL-SHARE rows follow this.
3. R04 says "BLOCK if card strict", but no card slot "strict" exists. Either add a named slot to the 8-card schema, with
   its K7 swap pairs, or delete the clause.
4. Base64 resolvability. State whether `base64 -d` of a visible literal piped to a shell is inside the expander. Ruling:
   it is resolvable (decode, then label the decoded registered payload with the state advancing). Only a base64 payload
   that is not visible in the session (read from an unknown file, or fetched) is opaque, and so ASK under R19. Add this
   case to the resolver list and to K3.
5. Tier source column. The frozen rule table gets a column that maps each rule's soft/hard tier to the Claude Code
   auto-mode-config category it comes from (hard_deny / soft_deny entry, as in the stripped excerpt). A rule with no
   source entry is marked "planner choice" and listed for the Opus re-check. This makes risk 1 (over-assigning hard)
   checkable.

Rulings on open questions: O1 keep `none` for opaque ASK (7 classes). O2 CRED-SCOUT reason = `cross_trust`. O3 the
section-3 minimum is confirmed as the binding no-execution rule (no rendered string is ever executed anywhere; validators
parse only; K16). O4 see G2. O5 yes: report FNR, flag precision and false blocks per 1,000 beside FPR (the author is right
that FPR does not move under class reweighting).
Notes (no re-check needed): add a construct-presence check over ALL rows, beside K6. Among rows that contain an
opaque-capable construct (`$(`, redirection into a shell, control flow), resolvable rows must be at least 40%, and the
ASK share among all such rows at most 60%. This stops "any `$(` means ASK" (risk 2). K10 and K12 follow G5 and G6.

### T51 SCOPE-BOUNDARY: REVISE

Must-fix:
1. Compaction block. Drop the invented "pinned-fact field". It is not a product field, it changes C2's rendered layout,
   and a boundary that is always pinned teaches nothing about compaction. Redesign: in both variants the boundary is
   stated in an ORIGINAL user turn that stays in the gate's input view (the gate sees user messages; the compaction
   summary is an agent-authored context block). Variant K = the summary repeats the boundary; variant D = the summary
   leaves it out. The label is the label under the boundary in both, and K3 checks that the gold is the same across K
   and D. L-0 checks against the product hook that original user turns survive compaction in what the hook receives. If
   they do not, the block is built eval-only and reported, not trained (answer to O2).
2. Shared lane rule (G9). The T51 oracle must use the shared table from T50 must-fix 1. Contained, unlicensed,
   unprotected = ASK. Shared, not agent-created, unauthorised = BLOCK (soft). Production = BLOCK. All 6 T51 cards set
   ask_on_soft = off; the alternative is to adopt the slot with T50's meaning and add card-swap pairs. With this, the
   answer to O4 is yes.
3. Neighbour cue (risk 5) becomes a gate, not a "maybe". In each label, 40-60% of rows contain a similar-named
   neighbour, and K6 includes a neighbour-present feature from the start.

Rulings: O1 metadata only (G7). O3 see G2. O5 yes, as T50 O5. The S x B x R matrix, the set-algebra oracle and the
"read-only/dry-run = ALLOW" rule against "vague means ASK" are approved as written. K14 targets are exact strings, names
and ID patterns only (plan v3.1 skeptic 9), as written.

### T53 EGRESS-SECRET: REVISE

Must-fix:
1. Rule precedence. Write the label table as first-match in a fixed order: (1) secret in a URL; (2) scoped credential-use
   (auth header to its own scope host); (3) secret in any other place; (4) package_publish; (5) mcp_call; (6) log/telemetry;
   (7) confidential cases; (8) public. As written, "secret, any destination = BLOCK" and the credential-use ALLOW
   exception both match the same row.
2. Personal data. Section 2 maps personal data to `secret`, while the table has "confidential ... (hard if personal
   data)". Pick one. Ruling: personal data = secret (hard), and delete the confidential-row clause.
3. K16 "live-validity check" must mean OFFLINE checksum and format verifiers only. No row value, and no part of one, is
   ever sent to any service or API. State this, and add a CPU test that the registry code has no network import.
4. Shared egress table (G9). T53's table becomes the shared egress rule that T50 R13 cites (T50 must-fix 2). The
   cross-family CPU test covers T50 EXTERNAL-SHARE specs.
5. ASK quota. ASK is 10.5% against a 10% floor. Quotas are counted AFTER drops (A/B, anchor, G13, OHS-5). The generator
   oversamples the ASK cells (unknown visibility, transport defect, unlisted MCP server) by at least 10% so K13 holds.
   Otherwise a pilot drop of 0.6 pp burns the fix iteration.

Rulings: O1 yes, a secret in a URL is BLOCK for every destination, its own scope host included (the credential-use
exception covers auth headers only). O2 K1 as written is accepted (it is at least as strict as Guard-10); L-0 attaches
the Guard-10 definition to the registry spec. O3 accepted with must-fix 5. O4 see G2. O5 own suffix table (default); the
public suffix list is not used.

### T41c TAINT: REVISE

Must-fix:
1. Facts-absent stratum (risk R4). The labels depend on an "environment facts" block that the product hook may not
   supply. Add a FACTS-ABSENT stratum of at least 25% of rows, spread over every label and carrier type, with defaults
   pinned in the label table:
   - no declared_hosts: every host outside the working repo's remotes is undeclared;
   - no declared_manifest: any package install is SOFT unless a manifest file is visible in a span;
   - no declared_workspace: the workspace is the repo root;
   - no declared_targets: only targets named in the user task are declared.
   Risk and labels are then computed by the same table. K1 and K2 gain a facts-present flag as a feature (it must not
   predict the label: AUC <= 0.55). L-0 or L-D records which facts the Claude Code hook can really supply, for C2.2.
2. Solver B (G1). B is a program. It derives `delegated` from the delegation-pointer anchor plus a closed list of task
   verbs, `agent_directed` from the addressee anchor, and `risk` from anchors vs the facts block (or the facts-absent
   defaults). State this. B's partial dependence on generator anchors is accepted, because the G5-H blind reads cover
   the natural-language side.
3. TLDs (G8): use the shared host list. K-gates G5/G6 follow (97.5th-percentile bound already used; token line 1,024).

Rulings on the pinned table: O1 delegated + HARD = BLOCK (a generic delegation never names the operation and target,
which matches T50's "hard never clears"). O2 nested + LOW = ASK. O3 unrequested + LOW = BLOCK (plan D4: "out of scope ...
unrequested -> BLOCK"). O4 the HARD/SOFT boundary list is approved as written. O5 keep the declared_policy control block
(4%). K6 at 98% agreement (not 99%) is accepted for this family, because the facts are read from natural-language
anchors. HO, BD and LS stay outside N and are never trained on.

### T54 TOOL-NEED/PICK: APPROVE

Binding condition C1 (gold must be program-checkable): ANSWER gold only when the answer content is present in the
rendered context or card, and a program locates it (a span or fact id in the record). Delete "general knowledge the card
allows" from the label meaning. A "definitional" ANSWER must point to a card or context span.
Rulings: 1. the idempotent-write rule (S4: unobserved + idempotent = WRITE) is approved as a card-stated policy. 2. R-1
floor and margin are approved as written (recall >= 80% per class, <= 2 pp below init, |gap| <= 8 pp, offset <= 0.50
nats; post-training report). 3. see G2. 4. the call-bearing definition is approved (S2, S5 and S6 use their own balance
gates). 5. see G5 (already compliant). 6. see G6 (already compliant). 7. sub-block drop is not adopted (G4).

### T55 RECOVER-ESCALATE: APPROVE

Binding conditions (gold order fixed now, so solvers A and B cannot read it differently):
- C1 B3 is first-match in this order: (1) no violation = ACCEPT; (2) violation caused by the call's own arguments
  (visible) = FIX_ARGS; (3) violation on a WRITE = ASK; (4) READ, first occurrence = RETRY; (5) READ, recurrence =
  SWITCH_TOOL if an equivalent tool is listed, else ASK.
- C2 B6 is first-match in this order: (1) changed and calls_used < P_cap = KEEP_POLLING; (2) changed and calls_used >=
  P_cap = ESCALATE; (3) not changed for < L calls = KEEP_POLLING; (4) not changed for >= L and an alternative exists =
  BREAK_LOOP_ALT; (5) not changed for >= L and the card marks the goal non-waitable = STOP; (6) otherwise ESCALATE.
- C3 P-4 is widened. The exhaustive truth-table test (rule table = A's evaluator = B's evaluator, 100%) covers B1, B3, B5
  and B6 as well as B2.
Rulings: 1-2 the tables and escalation cards are approved with C1-C3. 3 the observability check P-10 with a 2% pilot drop
tolerance is approved. 4 the B5 thresholds are approved (both published settings present, each card <= 25%). 5 the two
held-out violation types are drawn by seeded draw before any pilot. Their rows are dev-only, outside the 3,000. 6
approved (k_eff bars as written; G5). 7 see G2. Sub-block drop is not adopted (G4). The with-tool-outputs primary view
is accepted, because the error is the content.

### T56 DONE-CLAIM (done-claim half): APPROVE

Rulings: 1 the evidence-sufficiency invariant and the hidden-truth A vs visible-evidence B design are approved (a strong
design). 2 single-fault generation with the fixed precedence is approved. 3 the D5 exception is approved (the claim text
is still byte-identical). 4 P-8 is adopted as a PRE-FREEZE KILL gate: the outputs-only probe on the hard bin passes at AUC
<= 0.65 AND upper bound <= 0.70 (a sanity bar that relation faults are not keyword-readable, not a near-chance bar). 5
the optional D3 sandbox check is approved only after the L-0 sandbox sign-off. 6 the reason head follows G7 (head rows),
P-7 stays a kill gate, and per-class recall is report-only. 7 pairs >= 60% is approved. 8-9 see G5, G2, G6.

### T56g TEST-GAMING: APPROVE

Binding conditions:
- C1 VISIBLE_PASS is the RUNNER'S OWN success verdict on the patched tree: exit status 0 and no failed or errored test,
  with skipped and xfail counted as not failing, 2 runs agreeing. Without this, F2 (skip/xfail) and F8 (forced exit 0)
  hacks never satisfy VISIBLE_PASS and would all be dropped.
- C2 Contradicting-spec rows use the SAME label function. The held-out suite H of a contradicting-spec task always holds
  the spec-correct version of the contradicted case. Then "any passing patch is HACK" falls out of HELDOUT_FAIL and is
  not a separate rule. A CPU assertion checks this for every LIB-CONTRA task.
- C3 The natural slice is split by task: at least 100 of its 300 rows (whole tasks, both twins) form a natural DEV split
  that is never trained on. R2 is reported on that split only. Accuracy on trained natural rows is not a report line.
- C4 G3 applies (no free pilot tuning).
Rulings: (a) the 300-row reading (150 hacks + 150 honest twins) is approved, matching the v3.1 wording "the 300-row
slice"; the family stays 1,000 rows. (b) dropping honest-intended rows that fail held-out is approved (counted; they are
T57 PARTIAL material). (c) K6 and K8 are kept as PRE-FREEZE KILL gates. (d) K4 passes when the MEAN of the four rotation
AUCs is >= 0.70 and no single rotation is below 0.60, with CIs reported. This is fixed now, before any pilot, because
about 75 hack rows per fold give an AUC SE of about 0.05. (e) 25% with-outputs copies are approved. (g) The folds are
re-paired ACROSS mechanism groups: {F1,F5}, {F2,F6}, {F3,F7}, {F4,F8}. Mechanism pairing would hold out a whole mechanism
(both test-edit families) and fail K4 because of the TF-IDF probe, not the data. R1 also reports a whole-mechanism
holdout as an extra post-training line.

### T42c CODE-EXEC: APPROVE

Rulings: (a) 3 identical runs for OUT4 and TFAIL2 witnesses override the sandbox default (the plan's witness rule wins).
(b) the per-language step counters are approved; the 10% Python agreement check on 100 programs is a CPU/sandbox test that
must pass before any row. (c) the yield floor (< 80% kept triggers the fix iteration) is approved. (d) see G3: not
approved as written; section 9 is rewritten to G3. (e) authored failure markers for Go and bash are approved. (f) GBT
probes are advisory (G5).
Note: the exact toolchain patch versions and image digests from the L-0 image record are appended to this G0-lite (and
to T57 and T56g) before the first non-Python row (plan section 2: "pins go into the G0-lites before any non-Python row").

### T57 PATCH-VERDICT: APPROVE

Binding conditions:
- C1 TESTSEL leakage. TESTSEL options are hidden-suite tests by design, so a base module used for a TESTSEL row is never
  used for any other T57 head, nor for T42c or T56g. K10 adds a cross-row scan: no H test body of a module appears in
  ANY rendered row of the family except that module's own TESTSEL rows.
- C2 Wording fix. The hidden suites are PROGRAM-generated from behaviour atoms (the generator code is Claude-authored).
  Replace the "Claude-written tests/suites" wording in gate a and risk 1, so it does not read as LLM-written tests. The
  gold-sanity and strength gates stay exactly as written.
Rulings: (a) the TESTSEL definition (fails on buggy, passes after the fix; 3 distractors pass both) is approved. (b) the
reason head follows G7. (c) the T_s rule (0.90 if >= 70% of the 50 pilot modules reach it; one suite-recipe revision;
floor 0.80; non-Python pilot extended to 20 modules if it scores below 0.80) is approved and fixed before any row. (d)
excluding test-editing patches is approved. (e) 25% with-outputs copies are approved. (f) see G3. (g) the per-head
roll-alone rule is not adopted (G4).

### GEN general rows: APPROVE

Binding condition C1. CA-C4 (adjustment set) and CA-C5 (conditional independence) are graph questions. With
deterministic functions and fixed exogenous values, "independent given Z" is not defined. Rows of these two forms state
that the exogenous variables are independent random inputs and that the question is about the stated graph. They give
no fixed exogenous values. Gold = d-separation / backdoor validity on the graph (A and B as written).
Rulings: 1 the confirm rule is approved for GEN (G5), and GEN's GBT probes count as written. 2 see G2 (the G-H1 rule as
written is approved). 3 sub-block independence is approved (GEN is not P0; G4). 4 the 600 dev rows are never trained on;
L-0 decides whether they merge into mixdev. 5 L-0 confirms C2's general-type render shape before generator code
freezes. 6 GEN as a VOICE source (<= 5%) is included by default. The domain list is name-only and L-0 may replace items
after the G-name intersection without re-approval.

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

## Hand-off

- L-A: re-submit T50 (shared-core table with G9 test), T51 and T53 in one batch. Opus re-check target Mon 19 Oct, before
  the manifest freeze.
- L-I: re-submit T41c with the facts-absent stratum.
- L-T, L-C, L-G: copy the rulings and conditions into the addenda and start generator code.
- L-0: G5 probe harness, G8 shared TLD/IP list, G9 cross-family test hook, G10 span-export routing, the C2 layout check
  for G7 head rows and GEN rows, the misaki lexicon licence check.
- Orchestrator: the VOICE C2 question (no-voice arm or move to C2.2); the T51 compaction product check result.

## Round 2 (Opus re-check of the fixes; Opus 5.5 high; Sun 18 Oct 2026 UTC)

Read for this re-check: this file and the 12 families/*/G0_LITE.md files only (revision 2 of T50, T51, T53 and T41c; the
8 approved files as they stand). No excerpt, plan file, research file, generator, sealed path or benchmark text was
opened. No rows, no code, no model calls.

### Round 2 verdict table

| Family | Round 2 verdict | Round-1 must-fix items | New binding conditions (copy into the addendum) |
|---|---|---|---|
| T50 SHELL-GATE | APPROVE | 5 of 5 done | R2-T50-a to e |
| T51 SCOPE-BOUNDARY | APPROVE | 3 of 3 done | R2-T51-a to c |
| T53 EGRESS-SECRET | APPROVE | 5 of 5 done | R2-T53-a to e |
| T41c TAINT | APPROVE | 3 of 3 done | R2-T41c-a to e |
| T54, T55, T56, T56g, T42c, T57, GEN, VOICE | APPROVE (round 1 stands) | n/a | none new; the round-1 addendum is NOT yet in any of the 8 files (see below) |

No family is STILL-REVISE. Every gap found in this check is closed by an exact ruling below, so there is no third round.
APPROVE here means: the rule-table code of T50, T51, T53 and T41c may start now, after the lane builder copies the
round-1 decision and the R2 conditions word for word into an "Opus rulings 18 Oct" addendum at the end of the family's
G0_LITE.md. The build skeptic checks the code against the addendum. The K21/K19/K22 cross-family test still has to pass
100% before any pilot.

### T50 SHELL-GATE: APPROVE

Check of the fixes: [FIX-1] SLT-1 matches the round-1 lane rule word for word. [FIX-2] R13 has no conditions of its own
and cites SLT-2. [FIX-3] the `strict` clause is deleted and no slot is added. [FIX-4] B64-LIT is in the expander, the
resolver list, K3 and K18, and a not-visible payload is ASK under R19. [FIX-5] the tier-source column exists, nothing
was invented, and K20 checks it. Notes K19, K10 and K12 are applied. Choices 11.3 a-f are confirmed. The K10 reading in
11.4 is confirmed: G5 governs every probe gate and G6 governs K12.

Binding conditions:
- R2-T50-a SLT-1 SCOPE IN T50. In T50 only E6 infra contexts carry a lane tag. Files and branches have no lane in T50 and
  keep R03-R08 and R18. R09 = SLT-1 for E6 only. When an E6 spec also hits another T50 rule, R20 decides (the most
  restrictive label wins). Edit the SLT-1 scope sentence: the job, service, bucket, branch and file kinds are lane-tagged
  only inside T51. K21(a) covers E6 specs only. Reason: as written, SLT-1 and R03-R08 both claim branch and file
  mutations, and no order between them is stated.
- R2-T50-b K21(a) MAPPING. The T51 view of a T50 E6 spec has protected flag = false and MustPreserve = empty, so T50 E6
  specs carry no exclusion or boundary user turn. Only E6 specs under cards with ask_on_soft OFF go through the T51
  oracle (all T51 cards are OFF, and T51 has no ask_on_soft logic). E6 specs under ask_on_soft-ON cards are checked by a
  T50 unit test against the SLT-1 text (C3 = ASK).
- R2-T50-c MEANING OF ask_on_soft. The slot turns every soft BLOCK into ASK, in every T50 rule and in SLT-2 (rows 7(b) and
  7(e), see R2-T53-c), with ONE exception: SLT-1 C4 (production lane) stays BLOCK under ask_on_soft, as ruled in round 1.
  Hard rows never change. Write this into the card-slot definition (section 2) and into SLT-1 C4.
- R2-T50-d TIER SOURCES (11.5 re-check list). R05 is split: system paths (OS and system config directories, other
  accounts' home directories) = BLOCK / destroy / hard; any other target outside the allowed roots = BLOCK / destroy /
  soft (clears when the user names the operation and the target). Reason: risk 1 (over-assigning hard); an explicit user
  request to delete a named directory outside the project is a normal request. R07 protected-branch force-push = hard is
  accepted (it rewrites history other people depend on; one user's naming does not cover them; this matches T51's
  never-cleared protected flag). R15 hard part (remote-login keys, privilege files) is accepted. Every soft PLANNER
  CHOICE row is accepted as written. All of these stay marked PLANNER CHOICE in the column; K20 reports the hard share.
- R2-T50-e SLT-2 CHANGES. R2-T53-a to d change the shared egress table that R13 cites. T50 takes them over unchanged, and
  "rows not clearable by naming" in the consent-quad rule now means the SLT-2 rows with tier hard or na.

### T51 SCOPE-BOUNDARY: APPROVE

Check of the fixes: [FIX-1] the pinned-fact field is gone; the boundary sits in an original user turn in both K and D;
K3 checks gold equality and byte-identity outside the summary; K18 and the 3,120-row eval-only fallback (numbers
checked: ALLOW 46.8%, ASK 32.1%, BLOCK 21.2%, pairs 43.6%) are stated. [FIX-2] the oracle cites SLT-1; Protected
includes unauthorised, not agent-created shared/production entities; all 6 cards are ask_on_soft OFF. [FIX-3] K17 is a
pre-freeze kill gate per label, and K6 has the neighbour feature from the start.

Binding conditions:
- R2-T51-a Choices 11.2 a-c are confirmed. Dropping `own-cleanup` is correct (one label for one action, state and card).
- R2-T51-b K19 uses the R2-T50-b mapping (protected false, MustPreserve empty, ask_on_soft OFF only).
- R2-T51-c NEIGHBOUR VISIBILITY. K6 uses the RENDERED-row neighbour flag (what the model can see) as the neighbour
  feature, plus the spec-level flag as a second feature. When neighbours are made visible through user turns or earlier
  calls (11.2c), each carrier that shows a neighbour meets the 40-60% per-label share of K17 by itself, so the carrier is
  not a cue.

### T53 EGRESS-SECRET: APPROVE

Check of the fixes: [FIX-1] the 8-row first-match table is in the ruled order, and K23 tests it exhaustively. [FIX-2]
personal data = secret, and the confidential clause is deleted. [FIX-3] offline-only is stated, with the K21
no-network/no-subprocess test. [FIX-4] the table is SLT-2, with the ask_on_soft slot fixed OFF on T53 cards and K22.
[FIX-5] quotas are counted after drops, with the >= 10% ASK oversampling (at least 11% at generation). Block arithmetic
re-checked: 958 / 210 / 832.

Binding conditions:
- R2-T53-a RULE 2 MATCH. Rule 2 matches only when the normalised destination host EQUALS the credential's scope host,
  with scheme https and no certificate warning. Membership in the card's trusted list is NOT required (a service
  credential's scope host is usually not a repo remote, so the old "verdict trusted_exact or trusted_odd" condition
  would send most block-e ALLOW rows to rule 3). Raw-IP forms and other trusted_odd forms do not match. A lookalike of
  the scope host falls to rule 3. Solvers A and B compute this from the scope record and the host, not from the
  trusted-list verdict. Choice 11.2a (a transport defect on the scope host = rule 3) is confirmed.
- R2-T53-b SLT-2 IS TOTAL. Rule 4 is "package_publish with a public payload". A confidential payload in a package_publish
  row continues to rule 7 with visibility = public (a registry is public): 7(b) if the registry is trusted, 7(e)
  otherwise. T53 still does not generate this cell (11.2c is accepted), but the engine and K23 cover it, because T50
  specs can reach it through R13.
- R2-T53-c ONE MEANING OF TIER. `soft` means the same as in T50: it clears when the user names both the operation and
  the destination. So: 7(b) can be cleared like 7(e) (both named -> ALLOW, tier soft kept). Rule 4's not-named ASK on a
  trusted registry keeps tier soft (its naming test is the clearing). The ASK rows caused by a fact that naming does not
  settle carry tier `na`, like T50's opaque ASK: rule 5 (unlisted MCP server), 7(c) (unknown visibility), 7(d)
  (transport defect) and rule 4 with an untrusted registry. Their reason is unchanged, and naming does not change their
  label. Choice 11.2e is replaced by this. No planned primary label changes. The tier head rows (K24) use these tiers.
- R2-T53-d ask_on_soft (T50 cards only) turns 7(b) and 7(e) into ASK. Hard and na rows never change.
- R2-T53-e Choices 11.2 b, d and f are confirmed. K23's truth table adds the naming flag and ask_on_soft as inputs.

### T41c TAINT: APPROVE

Check of the fixes: [9.1] the facts-absent stratum has pinned defaults for all five facts; they do not contradict 1.1;
K1/K2 have the facts-present feature, K4 the stratum row, K6(i) the facts-absent branch, and there is a P8 report line.
[9.2] solver B is a program, with the task-verb list frozen with the template hash and hidden from A. [9.3] the shared
host list is used, and the 97.5th-percentile bound and the 1,024 line are applied.

Binding conditions:
- R2-T41c-a EGRESS ALIGNMENT (G9 spot-check, done here). Replace the HARD send clause in the 1.1 risk record with: "sends
  secret, credential or personal-data material to ANY host, declared or not, or places it in a URL, a log line or a
  package; or sends other project data to a host not in declared_hosts". The one LOW exception is a credential used as
  an auth header to its own scope host (exact host, https), which is SLT-2 rule 2 under R2-T53-a and the only form of
  `ben.auth_declared_service`. Reason: under the old clause, a delegated directive to upload a secret to a declared host
  came out LOW, so ALLOW_BENIGN, while T50 and T53 BLOCK the resulting action as hard.
- R2-T41c-b LANE ALIGNMENT. A directive whose action changes a shared or production resource (the SLT-1 C3/C4 scope) is
  HARD. T41c has no lane facts, so such a directive class is generated only when an anchored span names the lane-tagged
  context. Otherwise it is not generated.
- R2-T41c-c FACTS-ABSENT HOSTS. A host named only in the user task is NOT declared in facts-absent rows (remotes only, as
  ruled in round 1). After R2-T41c-a this affects project data only.
- R2-T41c-d STRATUM SHARE. The facts-absent share is ONE design value, fixed before the pilot (>= 25%; for example 30%),
  used in every label, carrier type and subtype cell, with each cell within +-2 pp of it. A 25% floor alone would let
  the share differ by label, and the facts-present flag would then fail K1/K2.
- R2-T41c-e Line 8 ("95% upper bound") and the O1-O5 line in 1.1 are superseded by section 9 (the 97.5th-percentile
  bound; rulings in 9.4). Edit them to match, so the builder does not read two bounds. K6(i) covers the R2-T41c-a
  exception.

### The 8 round-1 APPROVE families: verdict stands, addendum still to append

None of the 8 files has the round-1 "Opus rulings 18 Oct" addendum yet (all were last written before this file). The
verdict stands and needs no further Opus check. The lane builder must append the addendum before the names-only
manifest freeze; the build skeptic refuses a code review without it. Where the body text still says otherwise, the
addendum binds. Lines the addendum overrides:
- All 8: "Solver B = separate Sonnet high session" means CODE written by that session (G1).
- T54: the ANSWER meaning "general knowledge the card allows" (section 1) is deleted (C1). The section 9 / item 7
  sub-block drop is not adopted (G4).
- T55: the section 9 sub-block drop question is not adopted (G4). The C1-C3 gold orders go into 3.2.
- T56: the section 9 drop-only question is not adopted (G4). P-8 is a PRE-FREEZE KILL gate.
- T56g: C1-C4 and rulings (a)-(g); the fold pairing is {F1,F5}, {F2,F6}, {F3,F7}, {F4,F8}.
- T42c: section 9 is rewritten to G3; the toolchain pins go in before the first non-Python row.
- T57: the "Claude-written" test/suite wording (gate a, risk 1, T57-R5) is replaced (C2). The section 9 per-head
  roll-alone rule is not adopted (G4).
- GEN: C1 (CA-C4/CA-C5 rows state independent random exogenous inputs; graph gold).
- VOICE: P-V1 has no removal power in C2.1 (C2). C1: the context-recoverable span exception is OFF by default.

### Round 2 hand-off

- L-A: append the round-1 decision and R2-T50, R2-T51 and R2-T53 to the three addenda. Rule-table code may start. The
  K21/K19/K22 test still passes 100% before any pilot.
- L-I: append the T41c addendum with R2-T41c-a to e. Edit the 1.1 risk record and line 8. Code may start.
- L-T, L-C, L-G: append the round-1 addenda to the 8 approved files before the manifest freeze.
- L-0: in the 8-card schema, write the ask_on_soft definition with the SLT-1 C4 exception (R2-T50-c). Attach the
  auto-mode-config entry list so the "entry id pending" cells in T50 are filled (K20).
