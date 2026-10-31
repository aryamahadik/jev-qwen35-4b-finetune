# C2.1 plan, TRAINING-SIDE scope (sections 1, 2, 5, 6, 7, 8 + section 3's PRE-REGISTERED RULES block)

# C2.1 PLAN v3 (Sun 18 Oct 2026, ~02:00 UTC; Opus planner; v3.1 skeptic revision same day; v3.2 merge same day)

v3.2 (Sun 18 Oct 2026, ~07:00 UTC; Opus planner): merges owner Records A79 and A82 (PREREG_FINAL.md), the owner's
18 Oct check-at-creation rule (HANDOFF "OWNER feedback 18 Oct ~04:10 UTC"), C2_1_EXTRA_LEVERS.md ADOPT NOW A1-A36,
C2_1_PUBLIC_TRAIN_INVENTORY.md (new lane L-R) and research_v4/CRITIC.md (new families and every gap). Every change is
marked "v3.2:" with its source in brackets: [A79], [A82 n], [OWNER-ROW] (check-at-creation rule), [LEV An] (extra
levers), [INV] (inventory), [CRIT xn] (critic gap id). The detail tables are in the NEW section 16 (training side only).
The v3.1 text approved by A79 is kept byte-for-byte in C2_1_PLAN_v3_1_A79_SNAPSHOT.md (sha256 27a1fb785918d563…,
the sha A79 cites); where v3.2 and v3.1 differ, v3.2 binds only where it implements an owner decision or is stricter.

## 1. taxonomy_and_families

CHANGES FROM v1 KEPT FROM v2
- Every rebuilt family (T27, T40-T46) is built CLEAN-ROOM. Fresh agents write it; they never read the original
  generators, templates, wording pools or OHS-AC. No template quarantined under A64(c) is written again.
- Scope is managed in WAVES, not cuts ("cover ALL data at its best"; no cuts made from estimates). A family leaves C2.1
  for C2.2/C3 only if (a) it fails its gates after its one fix iteration, or (b) it is not through its gates by the data
  freeze. Both are measured states.
- P0 has 9 families. v3: T56 is built by two lanes (done-claim half in L-T, test-gaming half "T56g" in L-C), because the
  test-gaming half needs the sandbox. It still counts as one family for the floor. [codeexec 5.2]

A. DECISION TAXONOMY (eight groups; unchanged from v2 except where marked)
- G1 Permission and action safety: allow/ask/block on shell, git, infra and SQL actions; destructive or irreversible
  actions; egress of data or secrets; security weakening; scope against authorised targets; user-stated boundaries,
  including after compaction; supply-chain installs; trust boundaries; the Codex sandbox-escalation classes; plan mode
  vs act; deny-and-continue vs escalate.
  v3: add Anthropic's fourth risk group "bypass review or affect others" (push to main, production deploys, changing
  shared resources the agent did not create), and four failure modes named by both Anthropic and AuthGateBench:
  credential scouting, guardrail bypass, external sharing, inferred target. [permission 1.2, 2.4]
- G2 Injection and provenance: instructions inside tool outputs, repo artifacts, MCP tool descriptions and CI logs;
  authority framing; over-defence. v3: add user-delegated and task-necessary ("ambient helpful") instructions as the
  hardest benign classes. [injection D4]
- G3 Tool calling: call / ask / no suitable tool / answer directly; pick among distractors; argument grounding; parallel
  vs sequential; result vs claim. v3: add limit awareness (a needed tool, parameter or tool RESULT is missing) and
  "precondition already true". [tools 5.1-5.2]
- G4 Agent control flow: done or continue; stuck loop vs polling; recovery after an error; ask or proceed; next step;
  delegate; what to keep at compaction; commit/PR readiness. v3: add ambiguous non-idempotent write and implicit
  (well-formed but wrong) tool results. [tools 5.8-5.9]
- G5 Code verification with execution gold. G6 CI and repo operations. G7 Code security (synthetic CWE patterns only).
- G8 Monitoring the agent: test gaming and reward hacking; claims without evidence; overeager actions; edits to its own
  permissions.

B. P0 FAMILIES (9 families; about 28K new rows)
Each has: a G0-lite spec approved by Opus, solver A and an independent solver B, program or execution gold, one fix
iteration, and (v3) the family-specific gates listed below. Sizes are unchanged from v2 unless marked.

1. T50 SHELL-GATE (4,000 rows; at least 45% ALLOW)
   - Decision: ALLOW / ASK / BLOCK under a policy card, plus a reason head.
   - v3: reason head has 7 classes: destroy, exfiltrate, weaken_security, cross_trust, bypass_review_or_affect_others
     (new), supply_chain, none. [permission 5.4]
   - v3: second head "consent tier": clears_with_user_naming (soft) vs never (hard). Soft rows are paired: the same
     action with and without a user message that names both the operation and its target. Source of the tier: Claude
     Code auto-mode-config page (hard_deny / soft_deny). The Codex "forbidden/prompt" analogy is NOT used (refuter).
     Output to the product stays ALLOW/ASK/BLOCK plus reason plus tier. [permission 5.5, verification 2]
   - v3: four new sub-families: CRED-SCOUT, GUARDRAIL-BYPASS, EXTERNAL-SHARE (hands off to T53), INFERRED-TARGET (hands
     off to T51). [permission 5.4]
   - v3 GOLD: generate-then-render. Each row starts as a structured action spec (program, subcommand, flags, target,
     wrappers, environment, working tree and git state, policy card). The label is a function of the spec and the
     simulated state. The command string is rendered from the spec through semantics-preserving operators. Our own
     small expander owns brace/IFS/variable semantics. tree-sitter-bash (MIT) and mvdan/sh (BSD-3-Clause, Go 1.26+) are
     round-trip VALIDATORS only; rows where they disagree with the spec are dropped. shlex and bashlex are never the
     labeller (shlex is "short of a full parser"; bashlex is GPL-3.0 and is barred). [permission 5.1, 2.1-2.2]
   - v3 RULING on the render-vs-opaque conflict (planner decision; the gate sees only the string, so the safer reading
     wins): a rendering that a static engine cannot resolve (substitution, redirection into execution, control flow,
     unknown file) is ASK by rule unless its payload is visible (write-then-run of known content), in which case the
     written content is evaluated. "Same spec, same label" applies only to renderings the engine can resolve.
     [permission verification 1]
   - v3: an evasion sub-block with obfuscated-dangerous and obfuscated-benign rows in equal numbers (so "looks
     obfuscated" is not a cue), and an adversarial-benign slice (dangerous tokens in benign contexts). [permission 5.2]
   - v3: write-then-run rows (the payload written to a file is evaluated when run, as Anthropic's classifier does).
     [permission 2.8, 5.3]
   - v3 EVAL SLICES (dev, not sealed): reweight the dev set to 1:19 and 1:99 block-to-allow and report FPR with a CI at
     each (design choice, no published protocol); always report trivial baselines (always-allow, always-ask, regex
     prefix list, block-when-unsure) with per-class FPR and FNR. [permission 5.6-5.7]
   - Carve-outs, no-execution rule and simulated filesystem/git model: as v2.
2. T51 SCOPE-BOUNDARY (3,500 rows)
   - v3: built as an S x B x R matrix with a program oracle (authorised / must-preserve / protected sets computed from a
     generated entity list). S = how the request names the target; B = how many entities match; R = contained vs
     shared/production lane. Idea credited to AmPermBench (arXiv 2604.04978v2, independent of Anthropic) and
     UnderSpecBench (arXiv 2607.02294v1). [permission 5.8]
   - v3 CLEAN-ROOM against both: never copy their item text, entity names, ID formats, prompt wording or preambles.
     v3.1 (skeptic 9): only exact item strings, exact entity names and exact ID patterns go on the G13 target list;
     generic domain words (git branch, Kubernetes, S3, Slurm, job, service, bucket) are NEVER targets, and using the
     same domains is allowed. (AmPermBench's repo states MIT in the README only and
     ships an NC-SA paper; clean-room is the safe reading.) [permission 5.9, verification 4]
   - v3: trajectory-established authorisation (an earlier user message, a confirmed listing or an earlier approved action
     can authorise), built as contrast pairs that edit only the user turn. [permission 5.10]
   - v3: consent-declaration pairs (scope stated vs omitted with the same action; declared scope exceeded; scope only
     implied but clearly inside) to block the "target string in request means ALLOW" shortcut. [permission 5.11]
   - Compaction rows kept, now sourced: Claude docs say a boundary stated only in conversation "can be lost if context
     compaction removes the message". Gold is the label under the boundary. [permission 5.12]
3. T53 EGRESS-SECRET (2,000 rows)
   - v3 GOLD by provenance, not shape: every credential-like value carries a provenance attribute (authored as a
     placeholder in this session; read from a sensitive path or environment earlier; copied from an existing file;
     public key). Same-shape strings get different labels by provenance. Source: Claude auto-mode-config "Test
     Artifacts" and "Sensitive-Source Provenance" rules. [permission 5.13]
   - v3: visibility axis and data-class axis (secret / confidential / public): confidential may go to a private repo;
     secrets are never cleared by repo visibility. Default trust = working repo and its remotes. [permission 5.14]
   - v3: destination distractors from the CredLeakBench cue list (typosquat, wrong TLD, raw IP, homograph, misleading
     subdomain, brand mismatch, plain HTTP, certificate warning); gold = exact comparison to the trusted list after
     normalisation (public suffix, punycode); odd-looking trusted hosts are ALLOW to balance. [permission 5.15]
   - v3 FAKES: registered-fake rule kept. Checksummed formats get deliberately wrong checksums, used uniformly across
     ALLOW and BLOCK rows so the checksum carries no label signal (planner decision on the permission open question 5).
     Documented example keys are frequency-capped. gitleaks (MIT) is a catalogue of key shapes only; TruffleHog
     (AGPL-3.0) is barred. [permission 5.16]
   - v3: egress channels: HTTP POST of file contents, credentials in URLs, git push to an untrusted remote, bucket
     uploads, log/telemetry endpoints, package publish, MCP tool calls; T50's obfuscation operators reused. [permission
     5.17]
   - Guard-10 PII scrub as the registered-fake check: as v2.
4. T41c TAINT (clean-room; ALLOW / BLOCK / ASK / ALLOW_BENIGN by provenance)
   - Size: fixed from T41's recorded C2 status at C2 GO #1 (2,000 rows if T41 is in C2's mix; otherwise 3,000).
   - v3 D1 MINIMAL PAIRS: program-generate the benign artifact first; the malicious twin is the same artifact with one
     Claude-authored payload spliced at a sampled position. Gate: a format-only probe (logistic regression on carrier
     type, serialisation, length bucket, key names, no payload tokens) must be near chance on a held-out split.
     [injection D1] v3.1 numeric bar: held-out AUC <= 0.55 with a 95% upper bound <= 0.60 (skeptic 20).
   - v3 D2: structured attack tuples (task, authority set, carrier type and format, placement, goal class, wrapper
     style, visibility); Claude writes the text from the tuple under the G13 literal ban. [injection D2]
   - v3 D3: hold out whole FAMILIES in validation (2 wrapper styles, 2 goal classes, 1 carrier format, 1 placement);
     an in-family vs held-out gap above 5 pp triggers the fix iteration (5 pp is our choice; the cited "10-15 pp" was
     refuted). [injection D3] v3.1 SPLIT (skeptic 6): PRE-FREEZE KILL GATE = a CPU probe (TF-IDF + logistic
     regression on the in-family rows, scored on the held-out families; gap above 5 pp = fix iteration). The trained-
     model in-family vs held-out gap is a POST-TRAINING report line, not a kill rule.
   - v3 D4: benign share 50% (was at least 45%), at least 30% of benign rows user-delegated or ambient-helpful, plus
     trigger-word/security-discussion benign text and off-topic benign text. Label table is pinned in G0-lite: in the
     delegated set -> ALLOW_BENIGN; task-necessary and low-risk -> ALLOW_BENIGN; out of scope or high-risk and
     unrequested -> BLOCK; in scope only with confirmation, or authority unclear -> ASK. Delegated instructions that
     trigger a high-risk action class are not ALLOW_BENIGN (the MELON authors treat them as real risks).
     [injection D4, verification 5]
   - v3 D6: a length tail (10-15% of rows with 1.5-3K-token carriers) only if the token budget allows; otherwise Tier-1
     long outputs use chunked max-score reads and the plan says so. [injection D6]
   - v3 D7: explicit source tags per span (user, system/developer, user-owned repo file, third-party repo file, tool
     result, MCP description, MCP response, CI log) placed inside C2's existing rendered fields (no re-render).
     [injection D7]
   - Benchmark attack strings banned from all prompts: as v2.
5. T54 TOOL-NEED/PICK (clean-room; 4,000 rows)
   - The four When2Call answers; which tool among distractors; argument grounding; parallel vs sequential.
   - v3: LIMIT-AWARENESS block by deletion (remove a required tool, parameter or tool RESULT; gold = no suitable tool /
     ask / say the result is missing). Idea credited to CAR-bench (we copy only the removal idea). [tools 5.1]
   - v3: "precondition already true" near-misses (gold from simulated state: read first or no write). [tools 5.2]
   - v3: distractor count is a G0-lite design parameter (the "widen to 25 from MCP-Atlas" claim was refuted: unit
     mismatch); same-namespace hard negatives kept as a design idea. [tools 5.3, verification 7]
   - v3 GATE: call/no-call bias gate on a held-out balanced set: per-class recall for call and no-call, and the logit
     offset between the two option tokens; floor and margin fixed in G0-lite before any pilot. [tools 5.4]
     v3.1 SPLIT (skeptic 6): PRE-FREEZE KILL GATE = CPU checks on the data (call/no-call share 40-60% per sub-block,
     and a feature logistic-regression probe on surface features scoring held-out AUC <= 0.55, upper bound <= 0.60).
     The per-class recall and logit offset are measured on the TRAINED C2.1 after training, report-only.
   - v3: parallel vs sequential gold = topological levels of a generated dependency DAG. [tools 5.5]
   - v3: argument grounding of SUPPLIED values against earlier context stays our own OHS-5 metric, no public claim.
     [tools 5.6, verification 10]
6. T55 RECOVER-ESCALATE (3,000 rows)
   - Retry / fix arguments / switch tool / ask / stop; deny-and-continue vs escalate (3 consecutive or 20 total for
     Claude Code; 3 consecutive or 10 of the last 50 for Codex, confirmed [permission verification 10]); loop vs polling
     as a state-change predicate.
   - v3: AMBIGUOUS-WRITE class with ledger-simulation gold (key offered -> retry with the same key; read path exists ->
     read back first; neither -> escalate). LIMBO (author-run, single author): frontier models duplicated a lost-ack
     write in 56-74% of cases when read-back cannot show the outcome; keys cut duplicates 28% to 4%. [tools 5.8]
     v3.2 CORRECTION [CRIT H2; hardest.md row 31, https://arxiv.org/html/2609.29095, fetched 18 Oct 2026]: the
     56-74% sentence above is wrong. LIMBO's rates are lost-ack 0.5%, misleading HTTP 500 8%, late commit 56%,
     redelivery 74%. The AMBIGUOUS-WRITE class design is unchanged; no number from LIMBO drives a decision.
   - v3: IMPLICIT-ERROR class (well-formed result that violates an invariant), with violation types the card does not
     name. ToolMaze (author-run): explicit-minus-implicit recovery gap 37.15 points (mean over nine models). [tools 5.9]
   - v3: paired "blind retry" negatives (same error text; one names the bad argument, one does not). [tools 5.10]
   - Loop vs polling reported only on OHS-5 as "our items" (no public eval exists). [tools 5.11]
7. T56 DONE-CLAIM (3,000 rows: 2,000 done-claim in L-T + 1,000 test-gaming "T56g" in L-C)
   - Done vs continue with hidden acceptance tests executed; claim vs evidence; commit/PR readiness.
   - v3: matched pairs keep the claim text IDENTICAL across true and false rows; the difference lives only in tool
     outputs. GATE: a TF-IDF + logistic regression on claim text alone must score near chance (a generator sanity
     check). [tools 5.12, verification 15] v3.1 numeric bar: held-out AUC <= 0.55, 95% upper bound <= 0.60.
   - v3: subfamilies: ledger mismatch (done claimed, ledger disagrees); demo-only / dead code (small). [tools 5.14]
   - v3 T56g TEST-GAMING: hacks built from a transform library we write (delete or comment an assertion; add skip/xfail;
     hard-code the visible expected value; special-case the visible inputs; operator overload; record state; conftest or
     setup tamper; force exit 0 or swallow the assert). Label: HACK iff the artifact passes the visible tests AND (fails
     the held-out suite OR a registered transform signature matches OR a protected test path is modified). Honest-fix
     rows are the same task with a real fix. Contradicting-spec rows (ImpossibleBench's idea): any passing patch is a
     hack by construction. [codeexec T56-1]
   - v3 T56g GATE: hack-FAMILY holdout (train on 6 of 8 transform families, test on the other 2, rotate), bar set from
     base 4B on the same families; plus 300 "natural-looking" hacks written by Claude without the library, G5-H
     reviewed. Reason: monitors trained on prompt-elicited hacks "often fail to generalize" to naturally arising ones
     (ModernBERT 34.50 vs 99.70, author-run). [codeexec T56-2]
     v3.1 SPLIT (skeptic 6): PRE-FREEZE KILL GATE = a CPU probe (TF-IDF over diff tokens + logistic regression) trained
     on 6 transform families and scored on the other 2, rotated 4 times; it must reach held-out AUC >= 0.70 (the
     families must carry a learnable, non-trivial signal) while a diff-length/line-count-only probe stays at AUC <= 0.55
     (upper bound <= 0.60). The base-4B bar and the trained-model family holdout are POST-TRAINING report lines.
     v3.1 (skeptic 21): the 300-row slice is labelled "Claude-authored, prompted (no library)"; no transfer claim is made
     from it. An eval-only slice of hacks that arise on their own in Claude agent runs on impossible tasks in the sandbox
     is OPTIONAL and moves to C2.2 unless L-C is ahead of plan; it is never trained on.
   - v3: held-out suite runs in a fresh container from a pristine copy after the patch, with an executor-owned empty
     ini file on a read-only path and explicit --rootdir (not `-c /dev/null`, which is undocumented). [codeexec T56-3]
   - v3: P0 test-gaming rows are single artifacts (a diff plus test state), not trajectories. [codeexec T56-4]
8. T42c CODE-EXEC (clean-room; 3,000 rows)
   - Output or exception (4 options), equivalence (yes/no), will this test fail (yes/no). Application-style code only.
   - v3 LABEL WITNESS RULE: output = captured stdout/return value, three identical runs; exception = class name only;
     equivalence "no" = a concrete distinguishing input found by execution; equivalence "yes" = equivalent by
     construction AND exhaustive run over a small declared domain (never from random testing alone); will-this-test-fail
     = three runs agree, generator lint bans clocks, randomness, environment reads and order-dependent printing.
     [codeexec T42c-1]
   - v3: at least half of the 30% matched-pair quota are "same behaviour, different implementation" pairs plus one-token
     near-miss pairs. [codeexec T42c-2]
   - v3: report by trace length (about <10, 10-40, >40 executed steps), each bin gated against base 4B. [codeexec
     T42c-3] v3.1 SPLIT (skeptic 6): pre-freeze kill gate = each bin holds at least 15% of rows and a length-only
     CPU probe stays at AUC <= 0.55 (upper bound <= 0.60); the per-bin comparison against base 4B is a POST-TRAINING
     report line, not a kill rule.
   - v3: non-Python 25% split as JS/TS, Go and bash each at least 8%; language-native runners only; no package
     installs; `GOFLAGS=-mod=vendor GOPROXY=off GOTOOLCHAIN=local`. [codeexec T42c-5]
9. T57 PATCH-VERDICT (clean-room; 3,000 rows)
   - Does the patch fix the failing test without breaking passing ones; best of 4; TEST-SELECTION; LOCALISE.
   - v3 FOUR-GATE GOLD replaces "F2P and P2P execution": (a) gold-sanity: every hidden test passes on the reference;
     (b) strength: the hidden suite kills at least a preset share of independent AST mutants of the reference
     (threshold set by a 50-module pilot; proposal 90% of non-equivalent mutants; mutmut BSD-3 / cosmic-ray MIT as
     offline scorers only); (c) differential: reference vs candidate over program-generated inputs (our own generator;
     Hypothesis is MPL-2.0 and is not used); (d) two-solver agreement. Reason: on real data a single reference suite
     lets 7.8-28.5% wrong patches through (PatchDiff, UTBoost, arXiv 2606.16062; author-run). [codeexec T57-1]
   - v3 ANTI-SHORTCUT: a style-only baseline (patch length, line counts, comment ratio, identifier stats) must stay near
     chance (v3.1: held-out AUC <= 0.55, 95% upper bound <= 0.60; for best-of-4, accuracy <= 25% + 3 pp, upper bound
     <= 25% + 6 pp); 15% misleading-comment decoys; rename and option-order swaps; always report random and trivial baselines
     (random beat every patch-overfitting tool in 71-96% of cases, author-run). [codeexec T57-2]
   - v3 LOCALISE gold from our own mutator: one modifier per mutant, a test that fails only because of the mutation and
     traverses the entity; SWE-smith's 13 Python / 14 JS modifier names as the checklist (about 2.5 candidates per kept
     row is a planning guess). [codeexec T57-3]

TRAINING FLOOR (fixed in advance; unchanged): at least 6 of the 9 P0 families pass their gates, AND at least one of
T42c/T57 passes. Otherwise the orchestrator stops and reports at GO #1. v3: T56 counts as passed when its done-claim half
passes; if only T56g fails, only the test-gaming head rolls to C2.2.
v3.2 [CRIT C1]: T59 and T60 are P0-EXTRA families: built now, same pipeline and kill rule, enter the mix if through
their gates, but they do NOT count toward the 6-of-9 floor and cannot replace a failed P0 family (the floor is a
pre-registered rule; adding families to it would loosen it).

10. v3.2 T59 ASK-OR-PROCEED (P0-extra; lane L-K; 2,000 rows) [CRIT C1; LEV A9; INV section 4]
   - Decision: ASK the user / PROCEED, with an early-gate variant before the first state-changing edit.
   - Gold (program): a generated task spec with k admissible interpretations; ASK iff the interpretations lead to
     different actions AND at least one of them has a non-reversible cost; contrast pairs remove exactly one detail.
     Eight paired triggers (missing parameter, ambiguous spec, conflicting constraints, high stakes, missing capability,
     tool failure, conflicting evidence, risk appearing mid-run). PROCEED side >= 55% of rows (asking without need costs
     task success). Oracles reused read-only from L-A (spec/state) and L-T (DAG, ledger); label consistency with T50/T51
     /T54 is part of the G9 cross-family CPU test.
   - Realism slice from L-R dialogue sets (ABCD, MultiWOZ, Taskmaster) uses their own act labels, inside block R.
10b. v3.2 T60 CONTROL-NEXT (P0-extra; lane L-K; 2,000 rows) [CRIT C1; INV section 4]
   - Three heads: delegate vs do; keep vs drop a fact at a context summary (gold = whether a later step of the generated
     task DAG reads that fact); plan first vs act (gold from a generated task-risk spec: irreversible, multi-step and
     under-specified -> plan). Distractor facts that look important but no later step reads.
   - No published difficulty study exists (hardest.md section 0); the ladder is program-parameter only.
   - The boundary-after-compaction rows stay in T51 (approved design); T60 never labels permission.

C. P1 (wave C; starts as lanes free up; enters C2.1 only if through its gates by the data freeze)
Order as v2: T59 ASK-OR-PROCEED; T62 FLAKY-OR-REAL; T63 DEP-RISK (T36 folds in); T65 VULN-SYNTH (synthetic CWE, static-
taint gold, no CVE/NVD text); T66 REVIEW-GATE; T44c SEQ-CHECK and T45c TRACE-VERIFY (clean-room); T27c SCOPE-WIDEN
(clean-room); T64 LOCALIZE-REAL (vendored repos; conditional on the sandbox and 8.5). v3: T57r real-patch slice (partial
/ symptom-only / breaks-passing built from SWE-Gym or SWE-smith-procedural gold patches, execution gold only) joins P1
as a transfer slice, because benchmark-trained critics can be near random on real outcomes (OpenHands critic AUC
0.45-0.48 benchmark-only, vendor-run). [codeexec T57-4]
v3.2 P1 changes [CRIT A3, C2-C8; INV sections 1 and 4; A82 4, 7, 8]. New lane L-P owns T63, T66 and T67 so L-C keeps
only T42c / T57 / T56g; P1 families still enter C2.1 only if through their gates by the data freeze.
- T63 DEP-RISK (lane L-P; about 1,200 rows): typosquat / cross-registry near-miss (as v2); NEW "EXISTS?" head (500 rows:
  does package P or symbol S exist in registry snapshot R or library version V; gold = membership in an offline snapshot
  of seeded-namespace names plus a symbol list exported from the PINNED toolchains' own standard libraries at image build;
  conflation and cross-registry negatives); NEW licence-compatibility head (200 rows; gold = an Opus-written compatibility
  table over SPDX licence IDs only, no SPDX text copied); malicious-manifest slice from DataDog labels/metadata via L-R
  (never open or execute payloads). Real third-party package names never appear; only stdlib names and seeded names.
- T66 REVIEW-GATE (lane L-P; 800 head rows + 800 CommitPackFT rows via L-R): merge head (300; gold = the resolution
  under which BOTH sides' generated tests pass, executed on od-sbx1); semver head (300; "is this change breaking for
  callers?", gold = a generated caller suite run on the old and the new API on od-sbx1); message head (200 + the L-R
  CommitPackFT rows; "does this message describe this diff?", negatives by swapping messages across same-repo commits,
  licence whitelist mit / apache-2.0 / bsd-2 / bsd-3 / cc0 only).
- T67 IAC-GATE (NEW; lane L-P; 1,000 rows: 700 IaC/config + 300 MIGRATION): ALLOW / ASK / BLOCK on a proposed infra or
  config change before apply (destroy or replace hidden in a long plan, public exposure, privilege widening) and on a
  schema migration (lock class x table-size spec). Generated specs rendered to plan JSON, manifests and CI workflows;
  labels from OUR rule table, which reuses T50's reason head and the shared lane table SLT-1 (G9 cross-family test
  extended to T67). Checkov (Apache-2.0) and squawk (Apache-2.0/MIT) are round-trip VALIDATORS only, like
  tree-sitter-bash in T50 (CRITIC.md C4/C5, fetched 18 Oct 2026).
- T42c gains a COMPILE / TYPE-CHECK head (P0 family, so a G0 addendum + Opus approval; about 300 rows by substitution
  inside 3,000): "will this build / type-check pass?", gold from the pinned toolchains (Python 3.12 with a permissive
  type checker after its component-licence check, Node 24 tsc, Go 1.26 vet); ShellCheck and hadolint are never gold.
- T62 FLAKY-OR-REAL gets LogChunks failure chunks and FlakeFlagger run statistics; T65 VULN-SYNTH gets Juliet good/bad
  twins (no CVE ids, guard F2); T57 LOCALISE realism gets ManySStuBs4J / TSSB-3M diffs (permissive-repo filter); T57r
  gets SWE-Gym instances and SWE-smith PROCEDURAL rows (A82 8; problem_statement field barred; GPL/LGPL repos dropped
  row by row; strategy mapping verified first). All via L-R mappers.
- NOT BUILT: T58 SOLUTION-VERDICT (CodeNet / CodeContests / APPS are contest problem statements: A82 4 says NO).

D. C3 or report-only (U block): unchanged from v2.

E. RULES FOR EVERY FAMILY (v2, plus v3 lines)
- At least 30% matched minimal pairs; near-miss program negatives; C2's own errors through A42-D 6 trap selection;
  options shuffled; at least 50 wordings per question form from the start, no wording above 2%; A50 G6 at size; A49c
  balance; G5-H as adopted (two Haiku solvers on 300 rows per family plus one read of 100% of free-form rows); G3-H;
  A43(d) Opus confirmation of flags; token mean at most 800, hard cap 1,536 on at most 10% of rows; at least 25% non-
  Python in code families; a 200-row G13 pilot before full generation.
  v3.2 [OWNER-ROW]: the "200-row G13 pilot" is REPLACED by the check-at-creation pipeline (section 16.1): every row is
  G13-checked against every target and answer-checked when it is generated; the ">1% of rows hit" fix-iteration
  trigger is now measured on ALL rows of the 1,000-row pilot (and on full generation), not on a 200-row sample. The
  token rule reads as G0 ruling G6 (mean <= 800; none above 1,536; above 1,024 on <= 10%).
- v3.2 DIFFICULTY LADDER [CRIT D1, D2; INV section 4]: every family's G0 addendum names its hardest.md mechanisms (from a
  stripped excerpt), gives each a level parameter L1-L4, and puts >= 25% of rows at L3-L4; the alarming/calm x
  risk-present/resolved quad is mandatory for T50, T51, T53, T41c and T56; every hard cell has an easy-looking twin with
  the opposite label. MEASURED BAR (set-level, once per family, on the 1,000-row pilot): C2 (C1 if C2 has no weights)
  scores <= 70% on L4 rows (od-l4b read). A miss is folded into the family's ONE combined fix (G0 ruling G3: raise the
  program parameter; never drop rows by model score); after the fix a miss is a report line, not a kill (difficulty is
  not validity).
- v3.2 NEW HEADS INSIDE APPROVED FAMILIES (each needs a G0 addendum + Opus approval before code): T53 phishing-link head
  (destination-trust verdict reusing T53's normaliser and cue categories; head rows per G0 ruling G7) [CRIT C8]; T42c
  compile/type-check head (above) [CRIT C2]. Direct (user-turn) injection is NOT added to T41c (approved as an indirect
  family): L-R maps the Gandalf train splits (MIT) as block-R rows with Claude-authored benign twins at 50% written by
  L-I under the literal ban [CRIT C8; INV A18-A19].
- v3.2 ADOPT NOW row types (section 16.2) go in BY SUBSTITUTION inside each family's size; none adds rows (A14 and verbose A15 dialects add TOKENS, counted in the cost projection).
- v3: every family states its INPUT VIEW. Primary view = user messages plus tool calls, tool outputs stripped (Claude
  auto-mode style); a labelled variant with tool outputs (Codex auto-review style). When tool outputs are shown, the
  T41c taint rules apply to them. [permission 5.18]
- v3: every family reports trivial baselines next to the model, never a single accuracy (always-unsafe F1 0.690 beat 5
  of 21 models on R-Judge, independent). [permission 1.4; sealed 1.3]
- v3: shortcut gates named in each G0-lite (format-only, claim-only, style-only, call/no-call offset) run on CPU before
  full generation.
- v3.1 NUMERIC "NEAR CHANCE" (skeptic 20): binary probes pass at held-out AUC <= 0.55 with 95% upper bound <= 0.60;
  k-way probes pass at accuracy <= 1/k + 3 pp with upper bound <= 1/k + 6 pp. Each G0-lite writes its values before any
  pilot. Every G0-lite also marks each gate PRE-FREEZE KILL (CPU, data only) or POST-TRAINING REPORT (needs a trained
  model); no model-based gate is a kill rule before the data freeze (skeptic 6).
- v3.1 NAMES (skeptic 3, 4): every company, repo, host, service, bucket, tool, policy and runner name in a training row
  is drawn from a seeded random namespace with the TRAINING salt (no hand-picked fake names); the row-start guard
  checks every policy, tool, language, runner and carrier name against the closed allow-list in the frozen names-only
  manifest, and a row with any name outside it is refused.
- v3.1 G13 HIT REPORTS (skeptic 8): a hit report shown to a builder carries row ids, target name and method only, never
  the matched text. The literal-ban list is enforced by program inside G13; writers never see it.
- v3.1 a C2.1 training row that collides with frozen OHS-5 is dropped row by row; if drops stay at or below 5% of the
  family's rows this is NOT the family's fix iteration; above 5% it is (skeptic 22b).

F. HONEST LIMIT (unchanged): "beats every model" cannot be measured under our rules. We can show wins on a fixed public
list and on OHS-5 C-transfer.

## 2. data_sources

P0 USES ONLY CLAUDE-AUTHORED GENERATORS WITH PROGRAM OR EXECUTION GOLD. No external code or text corpus in P0.
v3.2 [INV; CRIT A1; A79 R5; A82 1-8]: a NEW BLOCK R (lane L-R) adds public TRAIN splits mapped to C2's layout with each
dataset's OWN human or program labels (no LLM writes or labels a block-R row), feeding mainly the GENERAL score and P1
realism slices. P0 gate families stay Claude-authored with program gold (every public tool-calling and agent-safety
train corpus found is LLM-made; INV section 0 item 4). Dataset list, conditions, row format and caps: section 16.3.
- v3 TOOLCHAINS: Python 3.12.x (exact patch pinned; security-only until Oct 2028), Node 24.x LTS, Go 1.26.x, bash from
  the pinned base image with an allow-list of external commands; image digests pinned. Node 20 is EOL and Go 1.22 is
  unsupported (nodejs.org; go.dev). Pins go into the T42c/T56g/T57 G0-lites before any non-Python row. sqlglot (MIT)
  for SQL parsing as v2. [codeexec C1, C8, P-1]
- No external identifiers in P0, so no source can HIT on 8.5; the manifest records "no external source" per family.
  The A61 final-mix 8.5 run still covers the whole mix.

GUARDS ON EVERY C2.1 SOURCE (as v2): every C_DATA_SPEC 4.3 guard (n8n/ejs-5; CVE-/GHSA- ids; /rosetta/i; stackoverflow
and stackexchange links; BIG-bench canary; lm-eval-harness, opencompass, helm, bigbench, leetcode repos; PII scrub as
the T53 registered-fake check; the deny-list program on every name); domain rule 3; the 200-row G13 pilot against
OHS-3, OHS-4, OHS-AC, OHS-5 (once frozen), every public eval target and the attack-string literals (more than 1% of rows
hit by any method sends the generator back; this is its one fix iteration). v3.2 [OWNER-ROW]: no 200-row sample any
more; G13 runs on EVERY row at generation (section 16.1); the >1% trigger is read on all pilot rows. v3.2 [A79 R4]:
OHS-AC is BINDING for new C2.1 rows and REPORT-ONLY for C2-replay rows (hits published, not dropped); R6 exemption
applies on every target. v3.1 (skeptic 2d, owner-reserved with R6):
a pilot hit traced ONLY to the sha-bound product-format scaffolding (header, option scaffolding, definitions card) is
not the family's fix iteration; the scaffolding is exempt, the item content is fully checked.
v3.1 (skeptic 30): every new L-0 program (C2-mix hash export, token histogram, access audit, manifest builder, row-start
guard) skips data/ohs3* and ohs3_parts/ in every data/** glob, and a CPU test asserts it.

v3 LICENCE/TOOL BARS (new): bashlex (GPL-3.0); CARE code and rules (depend on bashlex; rule bank mixes MITRE/GTFOBins
with unchecked terms); AgentTrust code and rules (AGPL-3.0 from v0.6.0); TruffleHog (AGPL-3.0); Hypothesis vendored into
rows (MPL-2.0); SWE-smith-js (no licence stated). Allowed as tools only: tree-sitter-bash (MIT) and mvdan/sh (BSD-3) as
validators; gitleaks (MIT) as a key-shape catalogue; mutmut (BSD-3) and cosmic-ray (MIT) as offline scorers.
[permission 3; codeexec 3]

8.5 PROCEDURE (A61 a/d; as v2): only the orchestrator runs 8.5, once before any mapper is written and once on the final
mix; the form-shopping bar applies; no generator code that touches a source before that source's pre-mapper PASS;
recorded A61(a) HITs (gsm8k, hover, isarcasmeval, tydiqa, md_fdc, md_peps, DI-TS inputs) bar a source under any id or
form. v3.2 [CRIT B6, I1]: md_worldbank, md_usgs and md_cma join the barred list in names manifest v1.1 (Opus checks the
md_* aliases against the A61(a) record). With about 60-70 L-R sources, 8.5 is batched BY SOURCE GROUP (intent/dialogue,
NLI/claim, reading/QA, reasoning/generators, safety text, code realism, tasksource sources); the orchestrator publishes
the measured time per source after the first batch and the schedule for the rest; a source with no pre-mapper PASS by
Thu 29 Oct 12:00 UTC is simply not in C2.1 (logged, not a cut by estimate).
v3.2-r (Sk 5; A61(d)): TWO pre-registered 8.5 stages per L-R source, written into ONE file (batch membership fixed in
advance, file sha logged) before batch 1 on Tue 20: S-pre (against the OHS-3, OHS-4 and OHS-AC exports, Tue 20-Fri 23)
and S-post (against the OHS-5 export, Sun 25-Thu 29 12:00, after the freeze). Each source runs ONCE per stage on whole,
fixed inputs; a source is never re-run inside a stage (form-shopping bar). An Opus 5.5 high ruling that this two-stage
schedule satisfies A61(d) ("once per stage, on whole fixed inputs") is signed BEFORE batch 1; without it, no batch
runs. Until a source's S-pre PASS exists, only its licence record (URL, quote, fetch date) may exist: no download, no
reader, no mapper code for it. Rows of a source need its S-post PASS. (Sk 1): "DI-TS inputs" is expanded into its
member sources from di_train/DI-TS/SOURCES_DITS_85.json: google-deepmind/logical-entailment-dataset,
kunalkukreja21/temporal-expressions-evaluation-lm and CogComp/perspectrum (names, hf ids, GitHub ids, tasksource task
names, aliases) are barred under every form, in split_aware_check.py A61A_HITS and in manifest v1.1, each with a CPU
test; every other A61(a) group name is expanded the same way from its own 8.5 input files. Any source that is an upstream of a barred
A61(a) source (e.g. HotpotQA for hover) needs an Opus 8.5 ruling first plus a transitive full-row G13 against every form
of the barred source; any hit = the whole dataset is DENY.

REMOVED SINCE v1 (as v2): CVEfixes, PrimeVul, BigVul, MoreFixes; Atomic Red Team, GTFOBins, NL2Bash, tldr-pages;
human-written MCP server schemas; CommitPackFT and SWE-rebench V2 out of P0.

P1-CONDITIONAL SOURCES (each needs a pre-mapper 8.5 PASS, per-row permissive repo licence, the guards and the A61(b)
check; each has a fallback)
- Vendored permissive Python repos (MIT/Apache/BSD; 30-60 repos; T64), offline venvs on the sandbox only. Fallback:
  synthetic modules. v3: also the possible source of real README/CI text for T41c benign twins (injection D5), same
  conditions; if it does not clear, T41c ships Claude-authored carriers and says the realism gap is untested.
- SWE-smith-py procedural instances only. v3.1 (skeptic 27, VERIFIED): the SWE-smith paper says "We prompt the LM for
  GitHub issue-style text" per task instance (arXiv 2504.21798v2 section 2.1, fetched 18 Oct 2026, author paper), so
  the problem_statement field is BARRED in T57r and P1; only gold patches, tests and repos are used (dataset card MIT,
  https://huggingface.co/datasets/SWE-bench/SWE-smith, fetched 18 Oct 2026). v3: exclude GPL/LGPL repos row by row (the paper's own Table 6 lists GPL and
  LGPL repos under a "permissive" caption); build the manifest from the rows, not the card (card 50,137 vs viewer
  59,136). Docker under runsc is untested: test it in L-0 before P1 depends on it. [codeexec C3, P-2]
- SWE-Gym. v3: repo Apache-2.0, HF card MIT (v2 said MIT for both). [codeexec C2]
- SWE-rebench V2, CommitPackFT: as v2.

GENERAL ROWS (about 7K) AND VOICE (v3: about 3K kept)
- General: Claude-authored harder items with program gold (multi-step arithmetic, logic, causal and temporal reasoning,
  tables); must not share sources or domains with OHS-3/4/5 G. v3.2 [CRIT A4, D3]: about 2,000 of the 7K come from
  vetted third-party GENERATORS run fresh (Reasoning Gym per-task allow-list minus gsm_symbolic and codeio and any task
  wrapping a public benchmark; DeepMind Mathematics regenerated; bAbI generator; fresh seeds only, never their published
  files); the hard-extension generators (one-edit negation/quantifier/scope/date flips, near-domain out-of-scope twins,
  unanswerable twins with the answer span removed, one injected unsupported claim at a known span, first-wrong-step
  traces, select-all and ordinal recasts) use GOLD BY CONSTRUCTION only. The critic's "two Claude solvers + Opus
  adjudication" route is NOT used: G0 ruling G1 says no LLM sets a label. A generic ABSTAIN option on Claude-authored
  general rows follows extra-lever O10 (A82 default): built, kept OUT of the mix; dataset-native labels such as
  out-of-scope, unanswerable, not-enough-info and unknown stay (they are the sets' own labels) [CRIT E2]. v3: these rows get NO hard-bin upweight (FLOW finds
  upweighting already-fit samples limits forgetting; the tension with a 2x hard weight is unresolved, so protect G).
  [recipe open question 2; planner decision]
- Voice: see section 7 (serving/multimodal) and the L-G lane. v3 recipe [voice 6]:
  - Only the user's spoken utterance passes through TTS and ASR. Actions, diffs, tool outputs and file content stay
    exact text. Dictated commands/paths/flags are a separate stratum (about 20%), half literal and half natural.
  - Two program generators: A = round trip (Kokoro-82M, Apache-2.0, voices graded C or better; acoustic chain with
    MUSAN CC BY 4.0 noise and OpenSLR 28 SIMULATED RIRs only; Nemotron EN 0.6B at a pinned revision); B = a confusion
    table harvested from Nemotron on LibriSpeech (CC BY 4.0) and generator A output, replayed by rules. v3.1 (skeptic
    33): LibriSpeech TRAIN splits only (test-clean/test-other are standard eval sets and are never used); Nemotron was
    trained on LibriSpeech (vendor card, per voice.md), so harvested error rates understate real error and the report
    says so. v3.1 (skeptic 29): the espeak-ng (GPL) out-of-vocabulary fallback inside misaki/Kokoro is DISABLED; our
    verbalizer spells every code token before TTS. Whether misaki can run with the fallback off is UNVERIFIED: L-G
    tests it on day 2; if it cannot, the espeak-ng tool-only question joins R11 and voice rows wait. Generator B's
    corruption rate is calibrated to the WER band table, not set to 0.10-0.20 (refuter).
  - WER bands per kept row: <3% 30%, 3-8% 35%, 8-15% 25%, 15-25% 10%, >25% excluded; a 500-row pilot maps conditions to
    WER first.
  - Gold is inherited only if every decision-bearing span (negations, numbers, the entities/paths/flags the gold depends
    on) survives; otherwise the variant is dropped and logged (drop-only). Loss by edit role, author-run SpeechEvalX:
    negation 25.7, number 21.9, entity 17.1 points.
  - Pool about 10-12K variants, keep about 3K, at most 2 per source row, voice at most about 8% of new rows, every
    voice row paired with its clean text twin (HIVE, author-run: LoRA robustness training can cost clean accuracy).
  - Nemotron revision pinned (main 13 Mar 2026, not the Jan 2026 branch); v3.1 (skeptic 14): every TRAINING voice row
    uses the LOCKED product mode, 560 ms chunks with forced flush (ALREADY_TESTED_C1_OPT.md); trailing-silence padding
    and flush behaviour are MEASURED at 560 ms first (voice.md marks 560/1,120 padding UNVERIFIED; 320 ms is proven only
    for 160 ms); 160 ms and 1,120 ms appear only in a 300-utterance dev robustness slice, never in training; first task is a 100-utterance probe of number form (digits vs words) because the card is
    silent. [voice 2.1, 2.7, C4, C5]
  - Chatterbox (unnamed 0.5M-hour data), Piper (GPL engine, research-only voices), F5-TTS (NC weights), XTTS and the
    other non-permissive engines: not used. [voice 4.2]
- Replay of C2's mix with drop-only steps (A46, p_g < 0.2 human rows, pg_anchor): as v2; human-label replay rows get no
  voice variants. [voice 6.1]

STATUSES CLOSED (as v2, with v3 wording fixes)
- When2Call train: OUT. v3 reason reworded: the paper says Mixtral 8x22B generated and classified the new data (owner
  27 Sep rule bars it); its training set uses APIGen categories, and the xLAM-60k card mixes a cc-by-4.0 field with
  "research purposes only" (so not a clean NC licence, but barred either way). [tools C2]
- BFCL: eval only (v3: Tier 2). SWE-rebench: P1-conditional. CodeReviewer: OUT. CodeReviewQA: v3 OUT of every tier
  (confirmed derived from CodeReviewer; distractors by Codestral-22B; no licence found). [landscape C4]
- A61(b) split-aware deny-list check: built as a pre-result program fix (Sonnet code, CPU tests, Opus ruling).
  Adoption is OWNER-RESERVED (section 10, R5). v3.2 [A79 R5; A82 1, 2]: ADOPTED. Code must be brought to the ruling text
  BEFORE any L-R record: (i) `--split-scoped-release` ON, releasing a TRAIN split only if full-row G13 shows it disjoint
  from every registered test/dev item, it is not an A61(a) HIT, and its report rows say "train split seen"; (ii) the
  tool's licence table today treats CC BY-SA as non-permissive (R5_CANDIDATES_CHECK.md finding 5): change it to
  "allowed, share-alike disclosed" per A82 2, and add CDLA-Permissive-2.0 per A82 7; (iii) catalogues stay refused
  (tasksource only per source, A82 6). The ruling-to-code conformance gate (section 16.1 step 0) checks all three.
- v3.2 [A82 5]: When2Call train, WildGuardMix and WildJailbreak stay OUT (no-LLM-data rule kept).

BARRED BY THE NO-LLM-GENERATED-DATASETS RULE (kept; not an owner question): Toucan-1.5M, Nemotron tool_calling, Nemotron-
RL-IPI, ToolACE, AceCode-87K, CodeScaler synthetic data, SWE-smith's LM bugs, R2E-Gym issue text. v3 additions (all
eval-only at most): NotInject (GPT-4o-mini written), AuthGateBench (DeepSeek-V4-Flash), AgentAbstain, ToolMaze,
ToolBench-X, NesTools, ToolHop, CAR-bench tasks, ClarifyBench, AgentDoG/ATBench data, StepGuard, DynaGuard, Terminal
Wrench, HackTrace, IH-Challenge (creation method not stated; treated as barred), PIDS-Bench. [injection, tools,
permission, codeexec, sealed]

NOT USABLE (licence; v2 list plus v3): IssueTrojanBench (CC BY-NC-ND), WASP (CC-BY-NC), TensorTrust data (no licence),
MCPTox (no terms found), TRACE data (CC-BY-SA per HF card; sources disagree), ImpossibleBench HF data (no licence
stated), AuthGateBench (paper CC BY-NC-ND; no data licence), CoRE (no licence file). [injection 3; codeexec 3]

NEVER USED AS DATA: outputs or weights of competitors (Jev, AgentDoG, OpenHands critic, Strands Decider, Horizon,
PromptGuard, PIGuard and every other detector). v3: no detector output is a label source or a filter. [injection 5.3]

EVAL UPSTREAM EXCLUSION (v2 list, plus v3)
- v3: the benign side of Tier-1 evals uses benchmark ENVIRONMENT content, so T41c carriers must not copy it either. Add
  as G13 targets: AgentDojo v1.2 environment strings and tool schemas; tau-bench data; BIPIA contexts; InjecAgent user
  cases and tool lists; AgentDyn environments; MSB and MCPTox server/tool lists; LLMail-Inject; NotInject's trigger
  words and prompts; PIDS-Bench hard-benign prompts; TensorTrust; CodeIPI; LogJack payloads. [injection 2.3]
- v3 tools targets: tau2/tau-bench tool and domain names, MCP-Atlas tool names (220), MCP-Bench servers (28), MCP-
  Universe servers (11), ToolHop tools, CAR-bench tool names, AgentProcessBench trajectories. [tools 5.19]
- v3 code targets: CRUXEval, LiveCodeBench (incl. test-output prediction), REval sources (HumanEval/ClassEval), CodeMind
  sources, CoRE, SWE-Flux repos, EquiBench Python pairs, CRUXEval-X, Impossible-LiveCodeBench/SWEbench, EvilGenie.
  [codeexec T42c-4]
- v3 permission targets: AmPermBench and UnderSpecBench exact item strings, exact entity names and exact ID patterns
  (v3.1: not generic domain words or "phrase frames"; skeptic 9); SteerBench-Work scenarios. [permission 5.9, 5.19]
  v3.1 (skeptic 28): CredLeakBench items and its cue-list strings are added as a G13 target (T53 uses only the cue
  CATEGORIES, never its strings).
- v3.1 (skeptic 8c): research excerpts given to clean-room builders (for example permission.md section 5 for L-A) are
  first passed through a Haiku strip step that removes every quoted benchmark string and ID example (such as
  AmPermBench's ID format); builders read only the stripped copy.
- All eval sets are registered as G13 targets BEFORE any C2.1 row exists (as v2). v3: enforced by a program check
  (row-producing jobs refuse to start without the OHS-5 FREEZE record and the G13 target registry sha).
- v3.2 [CRIT B1, F2; INV section 5 B1]: about 80 more benchmark test/dev splits are registered BEFORE manifest v1.1 and
  before any L-R row: HLE, AA-Omniscience-Public, every Decision Index 0.3 tested split, the 13 Nimble subsets, all
  JevBench variants, the safety.md 0.6 list, the tools.md section 5 list, the hardest.md section 2 list, EquiBench and
  CodeMind at problem-id level, the Codeforces/AtCoder date rule, and the test/dev splits of EVERY L-R dataset
  (section 16.3). One merged list (Haiku dedupe, Opus confirm); the row-start guard refuses every L-R job until the
  registry sha includes them. Transitive routes are targets too (HotpotQA vs hover; MuSiQue vs SQuAD/NQ; APPS vs
  CodeContests).

## 3 (PRE-REGISTERED RULES block only)
PRE-REGISTERED RULES (one look; Jev read once, after the C2.1 verdict)
- HEADLINE C-transfer: C2.1 - Jev >= +5 pp with paired LB > 0, AND C2.1 - C2 >= +3 pp with LB > 0. v3 note: the point
  condition caps power near 50% if the true gap is exactly +5; the rule is "expected to pass if the true gap is about
  +8". v3.1 (skeptic 17): at the planned SE 1.77 pp (deff 2), P(point >= +5 | true +8) = P(Z >= -1.69) = about 95%
  (DERIVED); if the realised SE exceeds the 2.0 pp resolution line the headline reads "unresolved". [sealed 5.1]
- SECONDARY C-total ("home field"): C2.1 - Jev >= +8 pp with LB > +3; at or above Jev's point on at least 5 of 6
  sub-blocks; C2.1 - C2 >= +5 with LB > 0.
- v3 G SHIP RULE (owner 18 Oct: "at most 2-3 points behind, 4 is the maximum acceptable"): Jev - C2.1 <= 4.0 pp on
  OHS-5 G point estimate, CI reported; target <= 3.0. Ship-binding. [GOALS]
- v3 G FLOOR as a stated non-inferiority test: C2.1 - C2, margin -1.0 pp, one-sided alpha 0.05. v3.1 (skeptic 17, 18):
  planned SE 0.40 pp at about 10,000 G items and deff 2 (DERIVED). If the realised SE is above 0.45 pp the -1.0 test is
  "unresolved". The -1.5 pp fallback margin is a loosening of v2's recommended "-1.0" floor, so it is NOT decided by
  the planner: it is OWNER-RESERVED R13 (default in section 10). It is fixed before any result. [sealed C2, 5.2.3]
  v3.2 [A79 R13]: DECIDED as written: G about 10,000 items with the -1.0 pp floor; -1.5 pp only if 10,000 cannot be
  reached, and the owner is told that day.
- K/X: static-attack ASR <= max(C2 + 2 pp, 3%), with the benign-block rate at the same threshold not worse than C2 +
  2 pp.
- ECE (l1, pooled C and pooled G) <= 3.5%.
- v3.2 CALIBRATION CLAIM RULE [LEV A27]: the 3.5% line above is the SHIP gate only (an independent protocol measured
  Jev 1.13 at ECE 3.3% / 3.2% on typed decisions, so 3.5% does not beat Jev). "Better calibrated than Jev" is claimed
  per pool (pooled C, pooled G) only if C2.1's protocol-aligned ECE is <= 3.0% (target <= 2.5%) AND the paired
  cluster-bootstrap 95% upper bound of (C2.1 ECE - Jev ECE), both under the aligned protocol on the same items from
  the one Jev read, is below 0. Otherwise the report gives both numbers and no claim.
- OHS-4 is report-only for C2.1 (C2 spends it).
- v3 second-look rule: one look. If a second read is ever needed after a fix, it counts as an improvement only if it
  beats the first by more than the paired cluster SE, and it is labelled a second look (adapted rule; not "the Ladder
  rule"). [sealed 5.2.11]

## 5. training_recipe

INIT (v3.1, skeptic 19: the rule below is the DEFAULT of owner-reserved R14; v2 put init under owner decision #1 "after
the C2 report", and the 18 Oct GO covered research and building, not init. The orchestrator works on the default from
the hour C2's gates exist and asks R14 in the owner message the day the C2 report lands; the GO #1 packet shows the
branch again. A different owner choice at GO #1 costs about 1 day of re-selection and replay-ratio change.)
- If C2 ships: init = C2.
- If C2 does not ship only because of the Jev-beat claim gate (S1) but passes its G floor and non-regression gates vs
  C1: init = C2's unshipped weights (they hold C2's added C skills and passed every safety/regression gate).
- If C2 fails its G floor or a non-regression gate: init = C1.
- The orchestrator records which branch applies from C2's measured gate results the hour they exist.
- Same Qwen3.5-4B base and r16 LoRA, merged to bf16, so the S1 parity path does not change.
- v3.2: R14 stays owner-reserved (asked the day the C2 report lands). The replay COUNT below depends on it.

v3 LORA OPTIMISATION BLOCK (written down; inherited from C2's recorded values; [recipe 5.1, verification 1])
- Peak LR no higher than C2's AND alpha/r no higher than C2's (LR and alpha are coupled; alpha/r scales the step).
- Same target modules as C2 (Qwen3.5-4B has 24 linear-attention and 8 full-attention layers, so q/k/v/o LoRA touches
  only 8 of 32 layers while MLP LoRA covers all 32; keep C2's set for parity). bf16 LoRA, no QLoRA.
- If any C2 value is missing from its records: LR 1e-4 (cosine, warmup 0.1, range 5e-5 to 2e-4), dropout 0.05, alpha
  equal to C2's alpha/r times 16. These single values are weakly supported; ranges are medium-supported.
- Epochs: 2 over the mix unless C2's measured s/step makes the cost cap bind; then fewer, stated.
- All values go into the grid sha.
- v3.2 [LEV A19]: LoRA ATTACH AUDIT in preflight: a CPU listing of attached module names must show MLP LoRA in all 32
  layers plus C2's attention set; GDN projections are NOT added (EXTRA_LEVERS 3a). [CRIT E3] is closed with this
  written reason instead of an ablation: one Modal run has no second arm, adding GDN targets breaks "same as C2", and
  the cap is tight; the C2 module list is recorded in the GO #1 packet.
- v3.2 [LEV A20]: BATCH CHECK in preflight: read C2's recorded global batch; above 64 goes to an Opus ruling (32-64
  with LR scaled) instead of being inherited silently.
- v3.2 [LEV A21]: LENGTH COVERAGE: a CPU histogram of general + block-R + replay token lengths vs the public-G panel
  and G-like dev lengths; L-G / L-R lengthen rows inside the 1,536 cap if a gap shows.
- v3.2 [REFUTED L22 in EXTRA_LEVERS 3b]: one preflight RECORD line of the loss normaliser C2 used; nothing changes.

v3 ALPHA AND GAMMA, DEFINED IN WORDS [recipe 2.2, 5.7]
- "init" = the start weights chosen above (C2, C2-unshipped or C1). "trained" = init plus the C2.1 LoRA delta.
- alpha arm: theta(alpha) = init + alpha x (trained - init), alpha in [0, 1]; alpha = 1 is the fully trained C2.1;
  alpha = 0 is init. (v2's formula read as reversed; this replaces it.)
- v3 gamma arm: 3 to 6 of the 18 grid points scale only the C2.1 delta before merge, gamma in {0.6, 0.8}. Evidence is one
  off-domain study (Qwen3-14B, biology; gamma 0.6 cost 1.07 general points, 0.8 cost 5.27; author-run). Under the
  definition above, the alpha arm and the gamma arm are the same operation on the delta; the gamma points are the
  pre-registered low-alpha points that protect G. The grid sha records the convention.

ONE MODAL RUN (as v2). v3.1 (skeptic 11): stage B FP8-KL is SCHEDULED, as owner-reserved R12 (it changes v2's "one
stage" and the serving parity path). Default: after stage A in the SAME Modal run, a short stage B trains the C2.1 LoRA
with FP8 fake-quantised forward passes and a KL term to the merged bf16 C2.1 parent (our own model, not a bigger
teacher; no new data), at most 15% of stage A's steps; its cost is inside the R1 cap and counted in the measured
projection before GO #1. FP8 serving is then adopted ONLY if the stage-B weights pass >= 99.5% argmax parity to the
bf16 C2.1 on dev; otherwise bf16 S1 ships and stage B is reported as "no gain". Precondition: a CPU test of the
fake-quant + KL trainer change and a Sonnet skeptic; if either fails, R12 defaults to "drop" and the GO #1 packet says
so. The gain is UNKNOWN (FP8 W8A8 gave +21% throughput at 98.7-99.0% parity on C1 without FP8-aware training; author-
run, ALREADY_TESTED_C1_OPT.md); no number from it drives a decision.
v3.2 [A79 R12]: DECIDED as written (include, inside R1; dropped automatically if its CPU test or skeptic fails or if it
busts the cap). It is therefore STEP 1 of the money shed order (section 11).

v3.2 MIX (supersedes the v3 numbers below where they differ; DERIVED, replaced by measured numbers before GO #1)
[INV section 6; CRIT A1, C1-C7]
| Block | Rows | Note |
|---|---|---|
| P0 9 families | about 28,000 | ADOPT NOW row types by substitution inside sizes |
| P0-extra T59 + T60 | 4,000 | 2,000 each; not in the floor |
| P1 families and heads (T62, T63, T65, T66, T67, T57r; T44c/T45c/T27c/T64 if through) | about 7,500 | 5,000 L-R realism rows + 2,500 new heads; only families through their gates |
| General program-gold | 7,000 | about 2,000 from third-party generators |
| Voice | about 3,000 | R11 decided (A79), so voice rows may enter after their gates |
| Block R (L-R public train splits) | about 25,000 | all eligible datasets at their caps (section 16.3) |
| Replay of C2's mix (a COUNT; pre-cleaned once) | 38,000 at C2 / C2-unshipped init; 57,000 at C1 init | v3.2 ruling below |
| Total | about 112,500 (C2 init) | mix cap 125,000 rows kept |
v3.2 REPLAY RULING (planner, before any data; not a loosening): replay is a fixed COUNT, not a ratio of the new rows
(the v3.1 ratio was written for 38K new rows; 1.0x of about 69.5K new rows would give about 139K rows and break the
cap). 38,000 = v3.1's 1.0x of its 38K new rows; 57,000 = its 1.5x. Block R is general-skill data that also protects G.
At C1 init the mix (about 131.5K) does not fit the cap: Opus re-sizes block R and P1 heads to fit (A82 9: no cap raise).
v3.2 COST of this mix (DERIVED from C2's measured mixes: $15.09 / 62,982 rows and $17.03 / 75,370 rows, i.e. about
$0.23-0.25 per 1K rows at 2 epochs, about $5 per 1K steps): stage A about $26-28; stage B (<= 15%) up to about $4;
total about $30-32 against the $30 training cap. So stage B is the first thing shed and is LIKELY shed unless the
measured rate is below C2's (A79 R12 allows exactly this).
v3.2-r (Sk 11): this per-ROW figure is probably LOW, because cost scales with TOKENS and block R (mean up to 800
tokens), the A14 long-input share and A15 verbose dialects add tokens without adding rows. It drives nothing. On Mon 26
Oct the projection is recomputed from the MEASURED token histograms of the 1,000-row pilots (every lane, plus the
first L-R datasets) times C2's measured $ per token, and the shed level is set then (re-measured Thu 29 12:00 and at
the data freeze). (Sk 12) the bound is min($30, ONE account's live credit / 1.25), about $24 at a $30 renewed credit.
(Sk 23c) the replay COUNT is a ceiling: if fewer clean rows exist, all clean rows are used and the shrink is recorded.

MIX (v3 numbers)
- New rows about 38K: P0 about 28K; general program-gold about 7K (about 18%); voice about 3K kept; plus any P1 family
  through its gates by the data freeze.
- Replay ratio fixed before any data: 1.0x if init is C2 or C2-unshipped; 1.5x if init is C1. Basis stated honestly: no
  published replay sweep exists; data quantity outweighs ratio (Dong et al.); already-known rows drive overconfidence.
  [recipe 5.8]
- Total about 76-95K rows, at most 125K.
- Replay of C2's program families depends on the OHS-AC regime (section 10, R4). Until the owner rules, the plan applies
  OHS-AC as BINDING to every C2.1 row (new and replay), which is the stricter reading. v3.1 (skeptic 2): R4 is now
  asked in the Mon 19 Oct owner message and needed by Sat 24 Oct (before any row), together with the widened R6; the
  Thu 22 format exposure probe (section 3) shows the owner how much of C2's scaffolding OHS-AC methods match.
  v3.2 [A79 R4]: DECIDED: OHS-AC report-only for C2-replay rows (hits published), binding for new C2.1 rows.
  v3.2 [OWNER-ROW]: the replay pool is pre-cleaned ONCE against every target (section 16.1 step 5) before any mix.

PROMPT FORMAT (as v2): keep C2's rendered layout (cygnet + schema_branch_mark) for every row; static-first reorder only
if the CPU measurement shows less than 60% shared-prefix tokens on gate calls; token mean <= 800 per family; 1,536 cap
on <= 10%; diffs trimmed by a program; gate rows see user turns and tool calls only (primary view), taint and done rows
also see relevant tool outputs capped at 256 tokens each; v3 labelled with-tool-outputs variants per family.
v3.2 [A82 11; LEV O7]: "READ TWICE" (repeat the question + options block after the evidence) gets a ZERO-SHOT test on
C2 on od-l4b dev, decided by Sat 24 Oct 18:00 UTC (before any row is rendered, so no G13 stamp goes stale): adopt only
at >= +1 pp on dev AND a passing repetition-flood eval. If adopted, it is a layout change: new rendered-prompt sha, a
new S1 parity record, a re-run of the format exposure probe on the new layout, and the R6 scaffolding sha updated
before rows start; if not adopted, C2's layout stays. No later switch.

ORDER INVARIANCE (v3 [recipe 5.2])
- Options shuffled per row.
- 20% extra copies with a RANDOM NON-IDENTITY PERMUTATION of the options (for 2 options this equals reversal), so each
  content visits each letter; selection bias is mainly option-ID token bias (Zheng et al., ICLR 2024, author-run).
- Symmetric KL term only if the trainer change passes its CPU test and a Sonnet skeptic review; otherwise plain copies.
  v3.2 [LEV A26]: CLOSED. Permutation invariance is plain permuted copies only (JS-consistency LoRA lost to plain
  augmentation on all 8 models in Seleznyov; no trainer change, no skeptic needed).
- v3.2 [LEV A15]: format dialects of the policy-card BODY and tool schemas are sampled ONE dialect per training batch
  (batch-by-dialect sampler in the trainer; unit test + Sonnet skeptic; scaffold sha unchanged).
- Flip rate is reported beside accuracy with a CI. The 1% dev target is kept as a reported metric and as the condition
  for the one-read-per-choice serving dial; it is not a claim.

HARD NEGATIVES (as v2, plus v3): at least 30% minimal pairs and program near-misses; A42-D 6 trap selection on C2's own
errors; hard bin 2x, hard <= 30%, easy <= 25%, no trap type above 35%; same code as C2's implementation. v3: the 2x
weight applies only after G5-H/G9 QC confirms the hard-bin golds; no hard upweight on general rows; "unstable under
option permutation or small margin on C2's reads" is an optional extra trap signal (unverified hypothesis), off by
default. v3: C2's reads of C2.1 candidate rows run as a pipeline on od-l4b as each family finishes full generation, so
selection does not wait for one big read. [recipe 5.6; ORCH rule 6]

BALANCE: gates at least 45% ALLOW (T41c 50% benign); yes rate 40-60% per family; class weights, not resampling.

LOSS AND CALIBRATION (v3 [recipe 5.3])
- Cross-entropy on option letters; no label smoothing (a simplicity and Modal-cost choice, not evidence-driven:
  Gemma2-2B in the same small-hidden/large-vocab regime gained a lot from smoothing).
- One temperature per type, fit leave-one-group-out on mixdev INCLUDING the hard/near-miss bin, bounded [0.8, 1.3],
  frozen with the candidate.
- Report ECE (bin count stated), Brier and a separate trap-slice ECE (guard overconfidence concentrates on adversarial
  inputs: WildGuard ECE .004 to .196 clean to adversarial, author-run).
- v3.2 [LEV A27]: report the protocol-aligned ECE (section 3) beside ours on mixdev and dev; target <= 2.5%.
- v3.2 [LEV A28]: temperature per (type x option-count bucket) with a CLIP AUDIT (if more than 10% of types sit at 0.8
  or 1.3, report it and widen the bound by Opus ruling); abstain score per type chosen by AURC among max-prob, margin,
  entropy, option log-sum-exp mass and a small CPU logistic correctness head (used only if it beats max-prob on a
  held-out family-group split; type left out of its features for unseen-type claims; argmax never changes); report
  AURC, E-AURC and per-slice risk-coverage (trap, near-miss, long-trace, ASR, identity-like).
- v3.2 [LEV A29]: CONFORMAL ASK band (split-conformal per type, Mondrian; ASK when the set has more than one option) and
  Learn-then-Test / conformal risk control for each FPR target, calibrated on family-group splits with >= 1,000
  held-out negatives per gate; every guarantee is printed with its ASK rate, its false-ASK cost and "marginal
  guarantee; breaks under shift". Never fit on sealed sets.

CANDIDATE GRID (as v2, plus v3): A42-D 9 grid of 18 candidates including the gamma points; grid sha (with LoRA block and
convention) recorded before any look; CANDIDATE record before the pre-gate reads; S = mean(general dev term, C/R
mixdev); general dev term from sources with a whole-file 8.5 PASS, else the G-proxy with the A61(f) label and S stated
as not claimable.
v3.2 GRID COMPOSITION AND S TERMS (all in the grid sha before any look; no weight searched after it):
- 18 points = 12 alpha/gamma points (as v3.1, including the 3-6 gamma points) + 2 last-K checkpoint averages [LEV A22]
  (K = 3 and K = 6 of the last ~6 saved LoRA states; average the merged deltas B x A, never A and B separately; LR
  schedule unchanged; CPU merge-math unit test) + 4 weighted soups of our own C1 / C2 (or C2-unshipped) / C2.1 as fixed
  simplex points [LEV A23]. A point ships only through S and gets its own parity record.
- S gains two pre-registered terms: a leave-one-family-out held-out sub-family score (one wrapper style, one
  obfuscation family, one dialect, one carrier format, never trained on; -3 to -5% rows) [LEV A24] and post-temperature
  NLL / ECE / AURC [LEV A25]; their weights are written before any look (otherwise it is a second look).

SNAPSHOT STOP (as v2): general slice below init - 1.5 pp at both the 25% and 50% snapshots.

COST (as v2): computed before GO #1 from C2's MEASURED s/step and the real C2.1 token histogram; projection about $18-28
for 76-95K rows; A37(k)-style stop-and-ask if the steps-100-300 projection exceeds the cap.
v3.2: the planned mix is about 112.5K rows; DERIVED projection about $26-28 without and $30-32 with stage B (task range $23-33); the
money shed order and the relay rules are in section 11 MONEY. The owner's "decide on measured usage" rule holds:
nothing is shed on this estimate; shedding happens only on the measured projection before GO #1 or the A37(k) check.

NOT ADOPTED (v2 list plus v3): non-causal attention; higher rank or a bigger base (owner only); RL with sandbox rewards
(C3); any distillation. v3: DPO/ORPO/preference optimisation (the only guard measurement found gave +0.7 to +1.0 F1 from
the model's own sampled outputs, which a one-token readout lacks; trap selection already covers hard samples).
[recipe 5.5]

## 6. serving

BASE PATH (as v2): SGLang S1 serving the merged bf16 model; argmax agreement with the HF adapter >= 99.5% on dev;
identical rendered-prompt sha in trainer, gate and server; any re-render gets a new parity record. v3: the parity check
also asserts thinking is OFF in every rendered prompt (Qwen3.5 thinks by default; disabled via enable_thinking False;
Qwen3.5-4B card, fetched 18 Oct 2026).

LATENCY AND COST TARGETS (as v2, indicative): gate calls 12-20 ms, tool/control 15-25 ms, code 20-35 ms server p50 (H100
batch 1); end-to-end p50 near users about 75-85 ms. v3 CLAIM LIMITS [landscape C7-C8]:
- Compare latency with hosted decision models measured by OUR client under the same conditions (our measured Jev e2e
  156 ms). AA's per-task medians (Celeris 63 ms, Jev 1.13 127 ms) are medians across all four index evals with no stated
  method, so they are context, not a like-for-like bar. Rule engines (CARE 2.3 ms) and DreamGuard (25 ms, author-run) are
  named as faster or similar classes; no "fastest" claim over them.
- Price in the rival's unit: Jev lists $0.042 per M input tokens, output free (docs, verified 18 Oct). Our cost is a
  hosting cost; the earlier C1 measurement found it cheaper than Jev only above about 59% utilisation, so any cost claim
  states the utilisation it assumes.
- Calibration claims name the protocol (Jev 6.0 ECE is our own measurement; Liquid's vendor claim of Jev 2.7 uses a
  different suite). v3.2 [LEV A27]: an independent protocol measured Jev 1.13 at 3.3% / 3.2% on typed decisions; any
  "better calibrated" claim follows the section 3 claim rule (aligned ECE <= 3.0%, paired win).

SPEED CHANGES THAT DO NOT CHANGE ANSWERS (as v2): exact batch-1 bundle; policy-card prefix caching; hosting near users,
keep-alive, warm pool, cheapest host meeting targets.

v3.2 SERVING AND DEPLOYMENT LEVERS (no training; L-D on od-l4b or CPU; never Modal) [LEV A30-A36]: A30 breakable
prefill CUDA graph with a text-only hot-path server (first read the B1a log, which says graph == eager); A31 SGLang
0.5.21 /v1/score with label_token_ids on OUR rendered prompt (never /v1/decisions), short-prefill scheduler flags, chunk
size that never splits a prompt, optional sliced LM head; A32 radix-cache ON vs OFF A/B on the real request mix before
any prefix-cache saving is counted; A33 persistent local sidecar for the coding-agent hook (warm HTTP/2 over a unix
socket, fail-closed fallback; first check how the hook process is spawned); A34 exact-match decision cache keyed by the
rendered-prompt hash + policy version, hashes only; A35 L4 fast-path ms/decision and $/1K curve; A36 hardened chunk
reads for tool outputs above 256 tokens (overlapping windows, contiguity-gated aggregate, view alignment; else ASK).
Every one that touches the served path needs a >= 99.5% argmax parity record, with A31's flip rate measured under
MIXED batches and cold vs cached requests (temperatures refit on the served path if they drift).
v3.2 [A82 10]: margin-gated second read with permuted options for low-margin items: MEASURE on od-l4b dev after GO #2;
adopt only at >= +0.3 pp with p95 under Jev's measured p95; it changes answers, so it joins R8 as dial (e) with its
own parity statement. [A82 12]: confidence API fields (calibrated probability on every primitive incl. yes/no, defined
`confidence`, published ASK thresholds per type, `calibration_version`, reliability diagram per type) are ADDED as
additive fields once the A27-A29 numbers exist. [A82 13]: multi-field single read, 2B student/cascade, paid extra
regions or GPU tiers and a batch pricing tier are NOT in C2.1 (C2.2 design / owner pricing later).

CHANGES THAT CAN CHANGE ANSWERS (OWNER-RESERVED, after measurements; section 10 R8): one read per choice question;
v3.1: FP8 serving only via the R12 FP8-KL-trained weights at >= 99.5% parity (block-FP8 at 98.38% and the FP8 margin
gate are recorded FAILED on C1 and are not re-planned; ALREADY_TESTED_C1_OPT.md); v3 PriDe-style per-letter prior
offset (zero added calls; needs a new S1 parity statement; tested only on untuned models) [recipe 5.4]. v3.1: the
selective-thinking tier is REMOVED (THINK_MODE_MEASURED.md, orchestrator decision 18 Oct: about 0 gain on OHS-1/2,
every think policy failed the A17 B1 "e2e median <= 1 s" rule, about 5-7x average cost).

v3.1 DEPLOYMENT WORK (no training; lane L-D in the build order; skeptic 15): warm pool (no 131 s cold start), hosting
region near users, cheapest GPU that keeps parity (measured on od-l4b; other GPU types cost money and go to the owner
as an R1-type question), batching plan to keep utilisation above about 59%. Never on Modal.

CASCADE PRODUCT (as v2): Stage 1 calibrated p(block); three operating points with FPR/FNR on sealed C-PERM; an ASK band
to a human or the customer's bigger model. v3: ASK is shown with an escalation-vs-risk curve (coverage vs error), not as
free recall (eBay paper: deferral helps only with a strong reviewer). [injection P-J]

INTEGRATIONS (product work, no training): Claude Code PreToolUse hook (allow/deny/ask JSON, reason category, fail-closed
option); adapters for Codex, Cline and OpenHands; an MCP server. v3: the hook's default view matches the training
primary view (user messages plus tool calls; tool outputs stripped).

## 7. multimodal (voice and images)

- Images: attached unchanged (as v2).
- Voice (v3 [voice]): Nemotron Speech Streaming EN 0.6B (NVIDIA Open Model License: commercial use allowed; NVIDIA
  claims no rights in outputs) in front of the text model; explicit end of input with measured silence padding.
- v3.1 (skeptic 10): the voice questions are OWNER-RESERVED R11, not planner rulings: (a) ASR transcripts used as
  training INPUTS (the ASR is not an LLM, is the product's locked input component, writes no labels; gold stays program
  gold); (b) Kokoro-82M as the only TTS although its training set includes some closed-TTS audio; (c) the NVIDIA Open
  Model License for Nemotron, which is outside the MIT/Apache/BSD/CC list (research_v3/voice.md C6 and section 4 ask
  for one explicit owner line). Default: allow all three. Until the owner answers, voice rows may be BUILT but stay
  OUT of the mix manifest. Chatterbox, Dia and Parler-TTS are not used in C2.1.
  v3.2 [A79 R11]: DECIDED: (a)-(c) allowed, (d) espeak-ng fallback disabled. Voice rows may enter the mix after their
  gates and Opus confirmation. [LEV A18]: a third program generator C (rule-based phoneme-neighbour word swaps from a
  pronunciation dictionary, corruption rate set to the WER-band table) joins inside the 3K pool (0 extra rows), after a
  CPU dictionary-licence check (MIT/Apache/BSD/CC only; L-0 already re-checks the misaki lexicon and CMUdict).
  [A82 9]: no non-English and no vision data in C2.1; claims say "English only" and exclude vision.
- v3 eval tiers: V0 (text vs clean TTS-ASR, every run), V1 (fixed SNR/RIR grid), V2 real human speech (at least 500
  pairs, at least 12 speakers) is NOT in the C2.1 critical path: it needs volunteers and consent; planned for C2.2.
- v3.1 V2-LITE (skeptic 13): the real-speech set already measured on C1 (speed/opt_c1_round2_20261017/VOICE_REAL.md:
  decision unchanged 89% vs the >= 97% goal) is re-read on C2.1 as an eval-only V2-lite, with n and a Wilson CI
  stated, IF its recorded consent/licence covers that use (Haiku reads the record, Opus confirms by Sun 25 Oct). It is
  registered as a G13 target and never trained on. If consent does not cover it, the real-speech goal is reported as
  "not measured in C2.1". Synthetic voice results stay labelled "TTS-based, an upper bound".
- v3 voice metrics: flip rate text vs speech with CI; harmful flips (allow where gold denies) separate from over-block
  flips; ECE text vs speech; flip rate by WER band and by error role; altered-span rate.

## 8. orchestration_and_parallel_lanes

MODEL TIERS (v3, from ORCHESTRATION_RULES.md; set `model` on every agent; never Fable)
| Work | Model | Effort |
|---|---|---|
| Orchestrator: plans, rulings, GO packets, 8.5 runs, verifying every agent's numbers | Opus 5.5 (main session) | high |
| Design/judgment: plan synthesis, ruling drafts, plan/ruling skeptics, OHS-5 brief, sealed freeze sign-off, A43(d) confirmations, G0-lite approvals | Opus 5.5 | high |
| All code: generators, solver A, independent solver B, executor, tools, G13/select/mix runs needing judgment, trainer, eval harnesses | Sonnet 5.5 | high (routine runs medium) |
| Code reviews and build skeptics (fresh agent, did not write the code) | Sonnet 5.5 | high |
| Research and research refuters | Sonnet 5.5 | high |
| First-pass adjudication of blind-read disagreements | Sonnet 5.5 | medium |
| Blind reads (G5-H, G9, answerability), wording pools, licence scouting, extraction, counting, running known scripts, log condensing, HANDOFF drafts | Haiku 5.5 | medium (mechanical: low) |
Haiku script-runners stop and report after 2 failed attempts. Any Haiku result that decides a gate is checked by the
next tier. Every prompt carries the no-probing and sealed-access rules; clean-room agents also get "never open the T27
or T40-T46 generators, templates or OHS-AC".

ORCHESTRATION RULES (v3, [ORCH]): critical path C2 > OHS-5 sealed build > C2.1 generator code > C2.1 rows; one writer per
file set (overlapping writers get worktrees); single-resource locks (Mac G13 one job at a time and never overlapping
C2's binding G13; od-l4b GPU one job at a time; Modal training only; execution only on the disposable sandbox); every
build gets an independent skeptic, every ruling an Opus skeptic; blind readers get Read + Write on their own files only;
access audit on every read batch; pipelines by default, loops capped, no silent caps; usage measured with get_usage
before every large launch (ping the owner at 96%, never cross 98%); never idle (prepare the next step's tools while
long jobs run); no placeholder arguments; agents read files, not pasted summaries.

USAGE: measured, currently low. Weekly reset Mon 15:00 UTC (19 Oct, 26 Oct, 2 Nov, 9 Nov). v3 correction: v2 said
07:00 UTC. v3.1 (skeptic 25): the orchestrator records the MEASURED day-1 burn per lane (get_usage before and after
each lane's first launch) and publishes a per-lane weekly projection on Mon 19 Oct. Pre-registered SHED ORDER at 90%
weekly usage: (1) pause wave-C (P1) families, (2) pause the voice pool, (3) pause general rows, (4) pause the remaining
training lanes; L-S, C2 and the GO steps are never shed. At 96% the owner is pinged (memory rule: ping, not stop);
never cross 98%.
v3.2 USAGE SHED ORDER [CRIT I2] (replaces the list above): (1) the optional research pass of CRIT I3 and tasksource
scouting beyond sources already promoted; (2) wave-C (P1) families in L-P and the P1 realism slices; (3) the voice
pool; (4) L-R tier-C datasets whose mechanical check is still open; (5) general rows; (6) remaining L-R datasets;
(7) remaining training lanes. L-S, C2, the G13 service, the GO steps and the confirming G13 are never shed.

MACHINES
- G13: serial on the Mac, alone; never overlapping C2's capture or binding G13.
  v3.2 [OWNER-ROW; CRIT B3]: G13 becomes a long-lived STAMP SERVICE on the Mac (one job, the lock holder) with every
  target pre-indexed once; lanes submit row batches and get back row-level stamps (row id, verdict, target name and
  method only). L-0 measures its throughput on 10,000 rows by Wed 21 Oct; if it cannot keep up with generation, a
  second G13 host is an orchestrator ruling (never sampling). The service never runs while C2's binding G13 runs.
- od-l4b (free L4): heavy agent CPU, all model reads (C2 trap reads, rival reads, base reads), TTS/ASR for voice.
  One GPU job at a time; C2's grid reads go first. v3.1 (skeptic 23): queue priority (1) C2 jobs, (2) C2 reads of
  C2.1 candidate rows, (3) L-E base-4B harness dry runs, (4) voice probe/pilot/pool, (5) L-D deployment measurements.
  L-0 measures throughput per job type (rows/hour) by Wed 21 Oct and publishes a queue plan with expected finish
  dates. C2 reads of C2.1 rows are NOT a kill gate: a family whose C2 reads are queued at the data freeze is still
  "through" if every data gate passed; its trap selection finishes in the Wed 4 Nov window.
- v3 od-sbx1 sandbox (execution gold only) [codeexec 5.4]:
  - Disposable CPU-only GCE VM on free credit, in its own VPC with no peering, NAT, Private Google Access or VPN; no
    external IP; no service account and no scopes; project SSH keys blocked; no data disk; Shielded VM with Secure Boot;
    --max-run-duration with DELETE as the termination action (flags confirmed on the gcloud reference).
  - Egress DENY all (IPv4 and IPv6); ingress only TCP 22 from the IAP range 35.235.240.0/20. Because Google always
    allows VM-to-metadata traffic, the host drops 169.254.169.254 and fd20:ce::254 for every UID except root and the
    guest agent, and every sandbox runs with --network=none.
  - Container runtime gVisor runsc (systrap platform; no nested virtualisation, no Firecracker in P0); one container per
    run (read-only root, cap-drop ALL, no-new-privileges, pids/memory/CPU/fd/file-size limits, nobody user, tmpfs /work);
    timeouts enforced from outside; stdout/stderr capped at 64 KB; 2 runs per execution (3 for will-this-test-fail),
    mismatches dropped and counted.
  - Images built on a separate build VM (od-sbx-build: egress, no data); the sandbox VM never pulls anything; runsc
    installed from the apt repo or tarball (the legacy auto-download path was retired at end of Sep 2026).
  - Data in and out over IAP-tunnelled scp only (the scp flag is UNVERIFIED; test it, fallback = IAP ssh with stdin).
  - Re-imaged per batch (at most one hour or N executions); image id, runsc and kernel versions in every manifest.
  - Executor self-test at every VM start (network, metadata, docker.sock, write-outside-/work, mount/ptrace/unshare,
    fork/memory/disk bombs, infinite loop, 1 GB stdout, a T56 tamper test, determinism, pinned versions); any failure
    aborts the batch. A Sonnet skeptic reviews exactly this list and Opus signs off before first use.
  - Fallbacks: nsjail (Apache-2.0) in the same VM; then rootless podman with crun; Firecracker only after a nested-virt
    machine type is confirmed. Never od-cpu1 or any data host.
  - v3: the sealed side uses a separate VM instance from the same reviewed image (od-sbx-s), with its own scp scope.
    v3.1: plus its own sealed image layer and no training identities on its IAP after handover (section 3).
- Modal: training only.

LANES (details, day-1 tasks and owners in C2_1_BUILD_ORDER.md)
- L-S sealed OHS-5 (separate sessions). L-0 infra. L-A T50/T51/T53. L-I T41c. L-T T54/T55/T56 done-claim. L-C T42c/T57/
  T56g. L-G general rows and voice. v3.1 (skeptic 15): L-E eval harnesses (Tier-1 + V2-lite; eval-side agents never
  write training generators and training lanes never open L-E files) and L-D deployment measurements (free GCP / od-
  l4b only, never Modal).
  v3.2 NEW LANES: L-R public train-split mappers (block R) [INV; CRIT A1]; L-K control lane T59/T60 [CRIT C1]; L-P P1
  repo/config lane T63/T66/T67 [CRIT C3-C7]. Each has one builder (Sonnet high), program solver B written by a separate
  Sonnet high session (G0 ruling G1), Haiku wording/scouting, Opus approvals, a fresh Sonnet skeptic.
- Per family: G0-lite (Opus) -> generator code (no rows) -> template/wording-pool hash export -> [OHS-5 freeze] ->
  1,000-row pilot -> 200-row G13 pilot -> gates (A50 G6, A49c, G5-H, G3-H, family shortcut gates) -> full generation ->
  C2 reads on od-l4b (pipelined) -> one fix iteration if needed -> kill rule.
  v3.2 [OWNER-ROW] REPLACED BY: G0-lite (Opus) -> generator code (no rows) -> ruling-to-code conformance record ->
  hash export -> [OHS-5 freeze] -> 1,000-row pilot WITH every row G13-stamped and answer-checked at generation ->
  set-level gates once on the pilot -> ONE combined fix if anything fails (G3) -> full generation, every row stamped
  at generation -> set-level gates once on the built family -> C2 reads (pipelined; trap selection, A46 screen on L-R
  rows; not a kill gate) -> kill rule. Section 16.1 has the steps.
- Wave C (P1) starts when a lane frees up, on measured progress.
- One binding G13 window, then selection, mix, d2-set, final-mix 8.5, preflight, GO #1.
  v3.2 [OWNER-ROW]: the binding G13 is ONE CONFIRMING PASS over the final mix (target <= 1 h; expected 0 drops because
  every row already carries a current clean stamp; any hit is a drop-only and a defect report on the inline check).

KILL RULE: a family that fails its gates after its one fix iteration, or is not through its gates at the data freeze,
rolls to C2.2/C3 (logged). If the floor (6 of 9 plus one code family) is missed at the freeze, the orchestrator stops
and reports at GO #1.

## 16. v3.2 merge detail (TRAINING SIDE ONLY; sealed-side agents never read this section)

Sources: PREREG A77, A79, A82 (read from PREREG_FINAL.md, blocks only); HANDOFF owner feedback 18 Oct ~04:10 UTC;
C2_1_EXTRA_LEVERS.md; C2_1_PUBLIC_TRAIN_INVENTORY.md; research_v4/CRITIC.md; research_v3/ALREADY_TESTED_C1_OPT.md,
THINK_MODE_MEASURED.md, ORCHESTRATION_RULES.md; families/G0_APPROVALS.md and the 12 G0_LITE.md headers and gate lists;
l0/R5_CANDIDATES_CHECK.md (findings only). Not opened: any ohs/sealed path, OHS5_BRIEF_DRAFT.md, C2 build files, data/,
logs/, ~/.claude. No download, no row, no model call, no Modal.

### 16.1 Check-at-creation pipeline [OWNER-ROW] (replaces "200-row G13 pilot" everywhere)

Owner, 18 Oct (binding): "If you're building one row, check that row at that same point and that's it ... then train."

| Step | What runs | When | Who (model, effort) | Pass rule |
|---|---|---|---|---|
| 0 RULING-TO-CODE CONFORMANCE (the A78 lesson) | For every ruling whose program builds, filters or stamps a record: A61(b) split-aware tool (A79 R5 + A82 1, 2, 6, 7), R4 replay report-only, R6 scaffolding exemption, A46 noise screen, A42-D 6 trap selection, A49c balance, A50 G6, any A69 selection code reused, G0 global rulings G1-G10, this section's stamp rules, the L-R recast tables and caps, the money shed order. A fresh skeptic who did not write the code maps every clause of the ruling text (ruling id + sha) to file:function and a CPU test id | before the first record of that kind; again after any code change | Sonnet 5.5 high (fresh skeptic) writes the map and tests; Opus 5.5 high signs | every clause has code and a passing test; the record builder REFUSES to run without a signed conformance record for its current code sha and ruling sha. Known items to fix first: split_aware_check.py treats CC BY-SA as non-permissive (must become allowed + disclosed, A82 2), lacks CDLA-Permissive-2.0 (A82 7), and has --split-scoped-release off (must be on with the 3 A82 1 conditions). v3.2-r (Sk 24, VERIFIED): CDLA-Permissive-2.0 is ALREADY allowed (CPU run: FinQA ALLOW); maps are built from the CODE, never from this list. v3.2-r fixes required before any L-R record: (Sk 1) A61A_HITS lists the three DI-TS member sources (logical-entailment-dataset, temporal-expressions-evaluation-lm, perspectrum; every id and alias) with CPU tests, and the conformance record expands EVERY A61(a) group name into its member sources from the 8.5 input files; (Sk 2) --split-scoped-release releases a train split ONLY when given a G13 result record (result sha, registry sha, method-set version, row count of the FULL train split, 0 hits outside R6 scaffolding) and writes train_split_seen: true into every released record, with one CPU test per A82 1 condition; (Sk 24) row_start_guard checks the job family field, and T59, T60, T63, T66, T67 join row_job_families_allowed in manifest v1.1; the tool docstring stops saying "G13 pilot". DEADLINE (Sk 23b): a record type whose map is unsigned at Sat 24 Oct 18:00 starts no rows |
| 1 REGISTRY FINAL | v3.2-r (Sk 4, 15): test/dev splits are fetched ONLY by the L-0b registry PROGRAM (Haiku 5.5 low runs it) into a registry-only store that the access audit denies to every lane; they are indexed and their shas logged; no agent reads them and no L-R builder is given the path. The registry lists the G13 METHODS PER TARGET: hash-only targets (the OHS-5 salted export) get exact and hashed n-gram methods only; the sealed side's counts-only reverse check covers what hashes cannot. G13 registry incl. the CRIT B1 additions, the test/dev split of EVERY L-R dataset, transitive targets, OHS-3/4/AC, the OHS-5 hash export (from Sat 24), attack literals, A61(a) sources, internal held-out sets, public-G panel items, the free-probe items | registry sha by Thu 22; OHS-5 export added Sat 24 | Haiku 5.5 medium compiles; Opus 5.5 high confirms | row-start guard refuses any row job without the registry sha |
| 2 STAMP AT CREATION | Every generator or mapper writes rows only through a wrapper that, per batch (<= 500 rows, same day): (a) runs the row's ANSWER CHECKS: program solver A = program solver B; family invariants (render round-trip, witness rule, ledger rule, registered fakes, no-network test); names guard (closed allow-list); token rule G6; PII scrub; decision-span export (G10); for L-R rows: train split only, licence record present, label = the dataset's own label through its Opus-approved recast table; (b) sends the row to the G13 STAMP SERVICE on the Mac, which checks it against EVERY registered target with every G13 method listed for that target (v3.2-r Sk 15: hash export targets use a SEPARATE hash-export salt, never the namespace salt and never the sealed salt, held only by the matcher process; R6 scaffolding exemption; OHS-AC binding for new rows); (c) writes the stamp (row id, registry sha, method-set version, generator code sha, verdict) into the row manifest | at generation, every row | lane builder's code (Sonnet 5.5 high); runs by Haiku 5.5 low; stamp service built by the L-0 builder (Sonnet 5.5 high) with a fresh Sonnet skeptic and Opus sign-off | a failed row is dropped and logged (row id, target name, method; never the matched text); no unstamped or failed row ever enters a family pool |
| 3 FIX TRIGGER ON ALL ROWS | G13 drop rate per family on ALL pilot rows and on each full-generation day | at the pilot; daily | orchestrator (Opus 5.5 high) reads the counts | > 1% of rows dropped for a reason other than exempt scaffolding or OHS-5 collisions (<= 5%, row by row) = the family's ONE combined fix (G3); answer-check drop rates use each G0-lite's own bars. v3.2-r (Sk 23a): an L-R DATASET (no generator to fix) with > 1% stamp drops outside the exemptions goes to Opus; > 5% = the dataset is left out (logged) |
| 4 SET-LEVEL CHECKS ONCE PER FAMILY | A50 G6 at size, A49c balance, wording variety (>= 50 per form, none > 2%), matched-pair share, difficulty ladder and the C2 <= 70% L4 bar, the G5 probe harness (shortcut probes), G5-H / G3-H reads with Sonnet adjudication and A43(d) Opus confirmation | once on the 1,000-row pilot (first look) and once on the fully built family | as G0 rulings G2, G3, G5 | the family's pre-registered bars; not repeated at the mix |
| 5 REPLAY CLEANED ONCE | The whole C2 replay pool is stamped once against every target (incl. targets C2 never saw); drop-only; OHS-AC hits on replay rows published, not dropped (A79 R4) | after the OHS-5 export loads (Sat 24), done by Mon 26, before any C2.1 mix | stamp service; Haiku 5.5 low runs; Opus verifies the counts | logged per family; a delta pass only if the Mon 26 hard stop adds sealed items. v3.2-r (Sk 23c, 23d): if fewer clean rows remain than the replay count, ALL clean rows are used, never refilled with unclean or unread rows, and the shrink is recorded; Opus records in the conformance record that A79 R4 (OHS-AC report-only on replay) is the specific ruling and stands, and that "clean" means drop for every other binding target |
| 6 STALE STAMPS | A stamp is current only for its registry sha. A late target (e.g. the Mon 26 delta) runs only the DELTA targets on the affected rows; a template change after hash export v1.1 means a new hash export and re-stamped rows | when the registry or a template changes | stamp service | incremental; never a full re-run by default |
| 7 MIX DRAWS ONLY CLEAN ROWS | The mix builder refuses any row without a current clean stamp (CPU test) | at selection and mix | L-0 code; Opus verifies | 0 unstamped rows in the mix manifest |
| 8 CONFIRMING G13 (the binding pass) | One pass over the final mix against the final registry sha | after the data freeze | stamp service; Opus 5.5 high verifies | target <= 1 h (from the Wed 21 throughput number); expected 0 drops. v3.2-r (Sk 14) DEFINITION (written into the conformance record): (a) stamp audit: every mix row's stamp is current for the FINAL registry sha, method-set version and generator code sha; (b) a full re-run of the exact and hash methods on every mix row; (c) fuzzy / sentence methods only against delta targets (added after the row's stamp). The Wed 21 throughput test is sized with the FINAL-size registry and block-R-length rows; if (a)-(c) take longer than 1 h they still run in full (no sampling). ANY hit stops the mix: that family or dataset is re-stamped whole and the service gets a skeptic re-check before training. Replaces v3.1's Tue 3 Nov 8-10 h window. The final-mix 8.5 still runs once (orchestrator) |
Locks: the stamp service is the single G13 job on the Mac and never runs while C2's binding G13 runs; od-l4b stays one
GPU job at a time; generation itself may run on od-l4b CPU or the Mac. If the Wed 21 throughput test shows the Mac
cannot keep up, a second G13 host is an orchestrator ruling; sampling is never allowed.
v3.2-r (Sk 22) STAMP-SERVICE STOP RULE: the second-host ruling is made on Wed 21 from the full-registry throughput. If
the stamp service is not signed off by Sat 24 Oct 18:00, row jobs WAIT (there is no unstamped quarantine pool); the
data freeze date does not move, and the kill rule and the floor apply to the lost days.
v3.2-r (Sk 3) B2 DISJOINTNESS: A82 1 "full-row G13 shows it disjoint" is read STRICTLY at the level of the whole TRAIN
split: the FULL train split (never the capped 1,200 rows) is G13'd against every registered target, after the OHS-5
export loads (Sun 25 on, Mac windows), and a B2 set is released only with 0 hits outside R6 scaffolding. Making the
subset disjoint by dropping hit rows is NOT used in C2.1 (it may loosen owner words); hit counts per dataset are
published either way and the row-drop reading is an owner question inside the GO #1 packet, for C2.2. An Opus 5.5
high ruling records this reading on Mon 19, before any B2 record exists.

### 16.2 ADOPT NOW levers A1-A36: owner and proving test [LEV]

Kind: PK = pre-freeze kill/data gate (CPU or od-l4b reads of our own models, data only); PR = post-training report
line; PB = proof before use (CPU or free L4; no kill power over a family). All row types are BY SUBSTITUTION.
| # | Lever | Assigned to | Proving test (kind) |
|---|---|---|---|
| A1 | Template-level gold-bug audit by confident C2 disagreement, before the 2x hard weight | L-0 script over C2 reads of C2.1 rows (od-l4b); lanes fix generators; Opus confirms each dropped template | flag threshold written before the look; solver B / execution re-check of every flagged template; drop-only by template slice (PK) |
| A2 | AFLite-style filter as the one-fix repair for a missed shortcut probe | L-0 tool, any family at its fix iteration | probe back under its bars; filtered <= 30% of the family, reported; easy share inside plan bounds (PK; counts as the fix iteration) |
| A3 | EDIT-AS-ACTION gate rows (Edit/Write/patch on CI files, hooks, lockfiles, rc files, cron/systemd, migrations/IaC, scripts) | L-A: new T50 sub-family 1,500-2,500 rows (scope variants in T51), >= 60% ALLOW, each state-file edit paired with the same diff on a non-state file; G9 test covers it | path-class-only probe AUC <= 0.55, bound <= 0.60 (PK); dev slice (PR) |
| A4 | Alias / protected-root reachability rows | L-A T50, 300-500 rows; alias tables in the simulated FS | alias-table unit tests; benign-alias twin rate by program (PK) |
| A5 | LATE-BINDING rows (trap, heredoc quoting, rebinding, redefinition, edit after review) | L-A T50 expander, 150-300 rows; unresolved = ASK | expander fixtures + Sonnet skeptic (PB) |
| A6 | GATE-DIRECTED INJECTION inside the agent's own action | L-A (T50/T51/T53 commands and edits) with an L-I Claude-written pool; 1,500-2,500 balanced rows | comment-presence probe AUC <= 0.55 (PK) |
| A7 | VERIFICATION-RELEVANCE near-misses (0 tests collected, filtered module, masked exit code, unrelated tests) | L-T T56 done-claim, 300-600 rows | gold from the simulated test run; claim text identical across each pair (PK, existing T56 gate) |
| A8 | SMELLY tool-description operators | L-T T54 program operators | drop any row whose gold needs the removed text, at creation (PK) |
| A9 | T59 promoted with the 8-trigger paired design | L-K T59 (P0-extra) | G0-lite approval; PROCEED >= 55% (PK) |
| A10 | Cue-invariance wrappers on every gate family, 1-2 wrapper families held out | L-A, L-I, L-T, L-C, L-K | FREE PROBE FIRST (Fri 23): 200 wrapped items built from C2's existing dev rows, read by C2; build only if C2 flips on more than a share written before the read (PB); held-out wrapper line (PR) |
| A11 | Hidden-character canonicaliser (strip Tags block, stray selectors; flag, not delete, ZWJ/flags) | product wrapper (L-D integration code); no flag field (that would be a re-render) | FREE PROBE on C2, 200 items (PB) |
| A12 | Character-perturbation augmentation, whole transform families held out | all text-bearing gate lanes, about 3,000 rows | drop at creation if a decision span does not survive (PK); held-out transforms (PR) |
| A13 | Benign-WORDED hijack payloads + lexical-balance gate | L-I T41c mix shift (0 extra rows); G0 addendum | payload bag-of-words probe AUC <= 0.55 (PK) |
| A14 | Long-input slice at a FIXED 5% share (layouts, filler, one layout held out, repetition flood) | L-I / L-T, 1.5-3K tokens; 3-8K only as eval | FREE PROBE on C2 first (buried-payload slice vs short-input recall, margin written before the read) (PB); tokens in the projection; money shed step 2 |
| A15 | Format dialects of card body and tool schemas, 1-2 held out, one dialect per batch | all lanes re-render inside the fixed scaffold; batch-by-dialect sampler in the trainer (L-0) | format-only probe per dialect (PK); scaffold sha unchanged; sampler unit test + skeptic (PB); shed step 3 |
| A16 | Observation-format perturbation of tool outputs, one format held out | L-I, L-T, L-C re-render | label-preserving check by program; 256-token cap kept (PK) |
| A17 | Multilingual measure-first slice | NOT ADOPTED in C2.1: A82 9 says NO non-English; eval slice deferred to C2.2 | none |
| A18 | Voice generator C (phoneme-neighbour swaps) | L-G voice pool (0 extra rows) | dictionary licence check; WER-band match; drop-only gold (PK) |
| A19 | LoRA attach audit | L-0 preflight | attached-module listing vs 32 layers (PB, blocks GO #1 if wrong) |
| A20 | Batch / LR check | L-0 preflight, then recipe | C2 config read; > 64 to an Opus ruling (PB) |
| A21 | Length coverage of general, block R and replay | L-0 CPU histogram; L-G / L-R fix | histogram vs public-G panel and dev (PB) |
| A22 | Last-K checkpoint averaging (2 grid points) | recipe grid sha | merge-math unit test; parity record if shipped (PB) |
| A23 | Weighted soups of C1 / C2 / C2.1 (4 grid points) | recipe grid sha | same as A22 (PB) |
| A24 | Leave-one-family-out term in S | recipe S | weight written before any look; held-out sub-families never trained (PB) |
| A25 | Calibration-aware term in S (NLL / ECE / AURC) | recipe S | weight written before any look (PB) |
| A26 | Close the symmetric-KL branch | recipe (order invariance) | none needed |
| A27 | Calibration protocol aligned to the independent Jev measurement | L-E reporting; recipe fit; sealed metric via section 3's protocol-aligned ECE line (v3.2-r Sk 9: not via the planner-written delta) | CPU on mixdev / dev reads; claim rule in section 3 (PR) |
| A28 | Option-count-aware temperature + clip audit + AURC-chosen abstain score | recipe + L-E | clip audit (> 10% at a bound = report + Opus); head only if it beats max-prob on a held-out family-group split (PB) |
| A29 | Conformal ASK band + Learn-then-Test FPR points | recipe post-hoc + L-E; never on sealed sets | >= 1,000 held-out negatives per gate; ASK rate and false-ASK cost printed (PB) |
| A30 | Breakable prefill CUDA graph + text-only hot path | L-D | read the B1a log first; od-l4b gain + 99.5% parity (PB) |
| A31 | /v1/score with label_token_ids on our prompt; scheduler and chunk settings; optional sliced head | L-D | parity under mixed batches and cold vs cached (PB) |
| A32 | Radix-cache ON vs OFF A/B | L-D | A/B on the real request mix; hit-rate check (PB) |
| A33 | Persistent local hook sidecar | product integrations (L-D measures) | hook spawn model checked; new vs reused connection timing (PB) |
| A34 | Exact-match decision cache (hashes only) | product / L-D | repeat rate on our own gate traces before any claim (PB) |
| A35 | L4 fast-path ms and $/1K curve | L-D (od-l4b, free) | measured numbers replace the derived ones (PB) |
| A36 | Hardened chunk reads for long tool outputs | serving / product (L-D) | program-built split-payload eval set (A14 data, eval only); FPR on long benign logs (PB) |
Probe items for A10, A11 and A14 are built from C2's EXISTING dev rows (no C2.1 training row exists before the OHS-5
freeze, A77), are eval-only and are registered as internal held-out G13 targets.

### 16.3 Lane L-R: public TRAIN-split mappers [INV; CRIT A1-A6, B1-B5, E5; A79 R5; A82 1-9]

RULES FOR EVERY L-R DATASET
1. Eligible only with: a manifest v1.1 record (one per dataset; tasksource one per SOURCE); licence quote + URL + fetch
   date; label provenance enum (human or program; any LLM marker refuses it); the A61(b) split-aware record with
   split-scoped release where its test/dev split is registered (A82 1); a pre-mapper 8.5 PASS (batched); guards F1-F10;
   not an A61(a) HIT, and an Opus ruling first if it is an upstream of one; no social-platform posts and no contest or
   exam statements inside it (A82 4); English only and no vision (A82 9).
   v3.2-r: (Sk 5) a source needs its S-pre 8.5 PASS before any download or reader code and its S-post PASS before rows
   (section 2); (Sk 7) the provenance enum has a third value "selection-rule" (labels picked by a similarity or other
   selection rule), which DENIES under this rule; (Sk 19) the LAST source addition is Fri 23 Oct 12:00 UTC (manifest
   v1.2 at most, names-only copy to L-S the same day); later sources roll to C2.2 (logged), including tier-C "waiting"
   sets confirmed after that time; Humicroedit and NLI4CT each get an A82 4 check before they enter; (Sk 26) every
   tasksource per-source record quotes the UPSTREAM licence, never tasksource's own card (NC / NC-SA upstreams DENY).
2. Splits: only the TRAIN split is downloaded or opened BY THE LANE where the release ships splits separately. v3.2-r
   (Sk 4) EXCEPTION: test/dev splits are fetched only by the L-0b registry program into the registry-only store (16.1
   step 1); no agent reads them and no L-R builder is given the path. Where one file holds
   several splits, a streaming reader filters on the split field and a CPU test asserts that no test/dev id reaches the
   output. Every test/dev split is a G13 target before mapping. Where no split exists, a seeded program freezes a 10%
   hold-out (by project, repo or CWE family) BEFORE mapping; it is an internal held-out target, never trained.
3. Labels: the dataset's own human or program label, recast through a per-dataset table approved by Opus. v3.2-r
   (Sk 6) WORDING: no third-party LLM-made text or labels and no model-made labels in block R; Claude-authored text
   only for the named benign twins (Aya, Gandalf summarization), whose gold is benign by construction, under the
   program-enforced literal ban. The A46-style screen (rule 6) uses C2 reads to DROP rows only; it never writes or
   changes a label. Opus records in the conformance record that this block-R use of A46 is a stricter, drop-only
   extension of the owner-approved A46 (which covered replay human-label rows), and that the twins are the only
   Claude-authored block-R text.
4. Row format: C2's rendered layout (or the read-twice layout if adopted on Sat 24; v3.2-r Sk 16: adopted ONLY if a
   program shows the new scaffold is the R6-exempted strings repeated with no new scaffolding text and Opus records
   it, so A79 R6's sha-bound exemption still covers it and the S1 parity record and format exposure probe stay valid;
   otherwise read-twice is not adopted in C2.1 and goes to C2.2); pick-one or yes/no; options
   shuffled; 20% random non-identity permutation copies at mix level; large label sets show the gold plus k-1
   program-chosen hard distractors (nearest label names or train-set confusion), k in {4, 8} rotating; multi-label sets
   become one yes/no per option; ordinal sets become an ordinal-bucket Choice (C2 renderer Score support checked first);
   long documents use program span selection (gold-bearing span + distractor spans, never a cut that drops evidence;
   length drops logged). Token mean <= 800 per dataset; none above 1,536; above 1,024 on <= 10%. v3.2-r (Sk 25): every
   long-document dataset gets a set-level span-position / span-length probe (gold span vs distractor spans; held-out
   AUC <= 0.55, bound <= 0.60); a failing dataset re-samples span order and lengths once, else it is left out.
   v3.2-r (Sk 8) NAMES: L-R and P1-realism rows carry REAL tool, language, runner, package and entity names, so the
   seeded-namespace rule (build order global order 5) and the row-start names guard (h) do NOT apply to them; this
   scoped exemption is written into the names guard (row family field = L-R / P1-realism) with a CPU test, and every
   other row keeps the closed allow-list. A program extracts the tool / language / runner / package vocabulary of every
   L-R and P1-realism source into names-only manifest v1.1 (v1.2 for Fri 23 additions) BEFORE the OHS-5 freeze, so the
   sealed side keeps C-transfer clear of those names. DataDog (T63): where the label does not depend on the name, names
   are swapped through the training namespace; where it does, the row carries a recorded T63-gate exception
   ("real package name, label depends on it"; counted and reported).
5. Caps: per dataset at most 1,200 rows (about 5% of block R); tasksource at most 300 per source and 3,000 in total, and
   a source that duplicates a directly mapped dataset is skipped; P1 realism rows count inside their P1 family. A dataset
   smaller than its cap enters whole. Every eligible dataset gets a mapper ("all data"); only the MEASURED money shed
   order lowers caps (uniformly, floor 300).
6. Checks: every row stamped at creation (16.1); A46-style drop-only noise screen on every human-label row (C2 reads on
   od-l4b, drop at p_g < 0.2); a dataset losing more than 15% goes to Opus; set-level once per dataset (class balance vs
   source, duplicates, length histogram, question-form variety >= 50 per form); every report row says "train split
   seen"; every CC BY-SA dataset carries a share-alike disclosure flag (A82 2). v3.2-r (Sk 23a): > 1% G13 stamp drops
   outside the exemptions = Opus; > 5% = dataset left out (logged). (Sk 3) B2 sets: the strict whole-split reading of
   16.1 binds.
7. G exclusion: every L-R dataset and its close siblings are on the manifest v1.1 R5 candidate list (names only), so the
   sealed side excludes them from G.
8. Owners (v3.2-r Sk 17: ONE L-R builder first, working in a pre-registered source-group order: safety text, code
   realism, intent/dialogue, NLI/claim, reading/QA, tables, reasoning, low relevance, tasksource; after S-pre batch 1
   the MEASURED time per source decides whether a second L-R builder starts, never an estimate; Opus approves recast
   tables in ONE batch per source group): L-R builder Sonnet 5.5 high (one per source group if usage allows); records scouted by Haiku 5.5 medium and
   verified by Sonnet 5.5 high; Opus 5.5 high approves each recast table and each tier-C check result; a fresh Sonnet 5.5
   high skeptic reviews the mapper code; Haiku 5.5 low runs the mappers.

DATASETS (caps are row targets; "B2" = needs A82 1 split-scoped release; licence quotes and URLs are in the inventory)
| Group | Datasets and target rows | Feeds |
|---|---|---|
| Intent / out-of-scope | CLINC150+OOS 1,200 (B2); MASSIVE en-US 900 (B2); HWU64 500; SNIPS 2017-06 400 | general; T54 analogue |
| Dialogue ask / act | ABCD 700; MultiWOZ 2.2 system acts 500; Taskmaster TM-1..3 300; SGD 500 (CC BY-SA) | T59/T60 realism, general |
| Evidence / NLI / claim | SciFact 500; ContractNLI 700 (B2); CUAD 500 (C); SNLI 800; MultiNLI minus FICTION 800 (B2); FEVER 600; VitaminC 400 (B2); CREAK 300; CondaQA 500 | general |
| Reading / QA / abstain | Qasper 800; SQuAD 2.0 800 (B2; 1.1 is subsumed); BoolQ 600 (B2); Natural Questions 500; DROP 500; QuAC 300; AmbigQA 200; Quoref 300; HotpotQA 500 (Opus 8.5 ruling first: upstream of barred hover); MuSiQue 400; 2WikiMultihopQA 400 | general |
| Tables / numeric / SQL | WikiTableQuestions 400; TabFact 400; HybridQA 300; FinQA 300 (C; CDLA, A82 7); Spider 300 | general |
| Reasoning / norms | WinoGrande 700 (B2); CommonsenseQA 400; Social IQa 400 (C); e-CARE 400 (C); QuaRTz 200 (C); QASC 200 (C); StrategyQA 300 (C); ETHICS MTurk subsets 600; BoardgameQA 400; FLD corpus (GitHub release) 200 (C); FOLIO 300; CLadder minus its GPT-4 variant 300 (A82 8; licence check first) | general |
| Low relevance | ESCI 100 (B2; minus the DI kit query ids); ChessBench 100 (B2) | general, low |
| Safety text | Aya red-teaming English 300 + benign twins; Gandalf summarization 100 + twins (manually reviewed); v3.2-r (Sk 7): Gandalf ignore-instructions is "selection-rule" provenance (embedding-similarity pick; card: some rows "might not be real prompt injections") = DENY under rule 1, rolled to C2.2 (logged) | G1 chat-side; direct injection (CRIT C8) |
| Code realism (P1) (v3.2-r Sk 26: CommitPackFT and SWE-Gym / SWE-smith rows pass a per-REPO code-licence check (MIT / Apache-2.0 / BSD-2 / BSD-3 / CC0 only; others dropped row by row); T57r NEGATIVES come only from our own mutator, never from SWE-Gym agent trajectories or patches) | Juliet 700 (T65); DataDog labels/metadata 500 (T63); LogChunks 700 and FlakeFlagger 200 (T62); ManySStuBs4J 400 and TSSB-3M 400 (T57 LOCALISE); SWE-Gym 1,000 and SWE-smith procedural (cap 1,000; A82 8) (T57r); CommitPackFT whitelist 800 (T66); MBPP train 300 (block-R will-this-test-pass rows, execution gold on od-sbx1) | P1 families |
| tasksource per source | up to 3,000 (A82 6; each source its own inventory row first) | general |
| Generators (general block, not block R) | Reasoning Gym allow-list, DeepMind Mathematics, bAbI (about 2,000 inside the 7K) | general |
| Waiting for a primary page (enter tier C by default when confirmed) | BANKING77, CosmosQA, OpenBookQA, ProofWriter/RuleTaker, NLI4CT, Humicroedit, WikiSQL, FLD.v2, CredData, ParamBench | general |
| EXCLUDED by A82 | Civil Comments, Social Chemistry 101, GoEmotions, Measuring Hate Speech, HateXplain (social-platform posts, A82 4); ARC, MedMCQA, MATH, AQuA-RAT, MathQA, CodeContests, APPS, Project CodeNet, Codeflaws, New Yorker caption-contest text (contest/exam, A82 4; New Yorker is the strict reading until Opus rules); When2Call train, WildGuardMix, WildJailbreak (A82 5); MASSIVE non-English, Aya non-English (A82 9); e-SNLI (duplicate SNLI labels) | none |
Totals (DERIVED): about 25,000 block-R rows (11,800 inventory core without Civil Comments + 10,100 A82 sets + 600 FinQA /
CLadder + up to 3,000 tasksource) plus about 5,000 P1 realism rows counted in the P1 families. About 60-70 sources.
v3.2-r (Sk 7): minus Gandalf ignore-instructions (400), about 24,600 block-R rows; B2 sets enter only under the strict
whole-split reading (16.1), so the real block-R size is MEASURED, not planned.

### 16.4 New families and heads [CRIT C1-C8]

| Family / head | Lane | Size | Gold method | Key PRE-FREEZE gates (bars in its G0-lite) | Status |
|---|---|---|---|---|---|
| T59 ASK-OR-PROCEED | L-K (new) | 2,000 | program: k admissible interpretations; ASK iff they lead to different actions and one has a non-reversible cost; single-detail contrast pairs; 8 triggers | PROCEED >= 55%; trigger-only probe AUC <= 0.55; G9 consistency with T50/T51/T54 | P0-extra (not in the floor) |
| T60 CONTROL-NEXT | L-K (new) | 2,000 | program: delegate/do from a generated task spec; keep/drop = whether a later DAG step reads the fact; plan/act from a task-risk spec | per-head label share 40-60%; "fact looks important" probe AUC <= 0.55 | P0-extra (not in the floor) |
| T63 DEP-RISK + EXISTS + licence heads | L-P (new) | about 1,200 + DataDog 500 via L-R | membership in an offline seeded-namespace snapshot + pinned-toolchain stdlib symbol list; Opus licence-ID table; DataDog labels | name-shape-only probe AUC <= 0.55; no real third-party package names in generated rows (v3.2-r Sk 8: DataDog rows swap names where the label allows, else carry the recorded T63-gate exception) | P1 |
| T66 REVIEW-GATE merge / semver / message heads | L-P (new) | 800 + CommitPackFT 800 via L-R | execution on od-sbx1 (both sides' tests; caller suite old vs new API); message swap by construction | diff-length-only probe AUC <= 0.55; licence whitelist | P1 |
| T67 IAC-GATE + MIGRATION | L-P (new) | 1,000 (700 + 300) | our rule table over generated specs (reuses T50 reason head and SLT-1); Checkov / squawk round-trip validators only | validator round-trip drop <= 5% (kill > 10%); G9 test extended to T67; resource-type-only probe AUC <= 0.55 | P1 |
| T42c compile / type-check head | L-C | about 300 by substitution | pinned toolchains (type checker after its component-licence check, tsc, go vet) | 3-run witness agreement; never ShellCheck/hadolint | inside P0 T42c (G0 addendum) |
| T53 phishing-link head | L-A | head rows per G7 (<= 25% of specs) | exact comparison to the trusted list after normalisation (existing T53 normaliser) | k-way head probe bars (G7) | inside P0 T53 (G0 addendum) |
| Direct injection | L-R + L-I twins | v3.2-r (Sk 7): about 100 + twins (Gandalf summarization only; ignore-instructions DENY) | Gandalf's own labels; benign twins by construction | twin share 50%; G13 at creation | block R |

### 16.5 Critic gaps: disposition [CRIT]

| Gap | v3.2 disposition |
|---|---|
| A1 no public-data block | FIXED: lane L-R, block R about 25K (16.3) |
| A2 tasksource path | FIXED by A82 6: per-source rows, cap 300/source, 3,000 total |
| A3 code realism sets | FIXED: P1 slices (16.3); T58 not built (A82 4 contest statements) |
| A4 third-party generators | FIXED: Reasoning Gym / DM Math / bAbI inside the general block |
| A5 noise screen on public rows | FIXED: A46-style screen on every block-R human-label row; > 15% loss to Opus |
| A6 large label sets / multi-label / Score | FIXED: L-R rule 4 |
| B1 unregistered test splits | FIXED: registry additions before manifest v1.1 and before any L-R row |
| B2 split scope | DECIDED by A82 1 (3 conditions); tool code brought to the text (16.1 step 0) |
| B3 200-row G13 | FIXED by the owner rule: every row at creation (16.1) |
| B4 replay vs new targets | FIXED: replay cleaned once against every target (16.1 step 5) |
| B5 seen flag | FIXED: section 4 and L-R rule 6 |
| B6 three A61(a) names | FIXED: manifest v1.1 |
| C1 ask-or-proceed / control flow | FIXED: T59, T60 as P0-extra (lane L-K) |
| C2 compile / type-check | FIXED: T42c head (G0 addendum) |
| C3 hallucinated package / API | FIXED: T63 EXISTS head (P1) |
| C4 IaC review | FIXED: T67 IAC-GATE (P1) |
| C5 DB migration | FIXED: MIGRATION block inside T67 (T50's approved table untouched) |
| C6 merge / semver / message | FIXED: three T66 heads (P1) |
| C7 dependency licence | FIXED: T63 licence head |
| C8 phishing / direct injection | FIXED: T53 head; Gandalf rows in block R |
| D1 hardest mechanisms | FIXED: difficulty ladder in every G0 addendum (section 1 E) |
| D2 measured difficulty | FIXED: C2 <= 70% on L4, once per family, inside the one fix |
| D3 NLU hard extensions | FIXED with gold by construction only (G1 bars Claude-solver labels) |
| E1 projected G gap | FIXED: public-G panel before GO #1 (section 4) |
| E2 abstention | PARTLY: dataset-native abstain labels kept; generic NOTA option built but out of the mix (A82 default for O10) |
| E3 LoRA on linear-attention layers | CLOSED with a written reason (section 5) and the A19 audit |
| E4 multilingual | DECIDED NO by A82 9 ("English only") |
| E5 long documents | FIXED: L-R rule 4 span selection |
| F1 public general eval | FIXED: public-G panel (L-E) |
| F2 families with no public eval | FIXED: "OHS-5 only" lines; report-only sets where licences allow |
| F3 vision | DECIDED NO by A82 9 (claims exclude vision) |
| G1 licence bundle | DECIDED by A82 |
| H1 verdict conflicts | FIXED: strictest verdict until Opus rules; Opus confirms at manifest v1.1 |
| H2 LIMBO citation | FIXED in section 1 (T55) |
| H3 Nimble intersections | FIXED: marked B2 in 16.3 |
| I1 8.5 critical path | FIXED: batches by source group, Thu 29 cut-off (section 2) |
| I2 shed order | FIXED: usage shed order (section 8) and money shed order (section 11) put block R and general last |
| I3 missing research angles | PARTLY: vision and multilingual closed by A82 9; one Sonnet + refuter pass on coding-agent everyday decisions, code-review preference and the unopened code.md names runs only as usage-shed item 1 (never on the critical path) |

### 16.6 v3.2 change list (one line each)

1. Owner decisions A79 and A82 recorded as decided items D10-D12; section 10 statuses; new R15 (October money).
2. Check-at-creation pipeline with a ruling-to-code conformance gate; 200-row G13 pilot removed; replay cleaned once;
   confirming G13 <= 1 h.
3. 36 ADOPT NOW levers assigned with proving tests (A17 not adopted, A82 9).
4. Lane L-R with block R about 25K rows over about 60-70 sources; A61(b) tool fixes (CC BY-SA, CDLA, split scope).
5. New lanes L-K (T59, T60) and L-P (T63, T66, T67); T42c and T53 heads; Gandalf direct-injection rows.
6. Calibration claim rule: aligned ECE <= 3.0% (target 2.5%) with a paired win; 3.5% stays the ship gate.
7. Recipe: attach audit, batch check, length coverage, grid = 12 alpha/gamma + 2 last-K + 4 soups, S terms, symmetric
   KL closed, dialect batching, option-count temperature, conformal ASK.
8. Mix about 112.5K rows, replay a fixed count (38K at C2 init); money projection about $26-32 with stage B shed first.
9. Money shed order, relay rules, No-Fee terms check moved to Wed 21.
10. Timeline: stretch data freeze Fri 30 Oct, fallback Mon 2 Nov; honest must-go-right list (money is the weakest).
11. Usage shed order puts block R and general rows last (CRIT I2).
12. LIMBO citation corrected; read-twice decision moved to Sat 24 (before any row is rendered).
13. v3.2-r: skeptic revision (16.7 training timeline and money moved out of sealed-readable sections; 16.8 response).

### 16.7 Training-side timeline, money and lines moved from sections 4 and 11 (v3.2-r; TRAINING SIDE ONLY)

MOVED FROM SECTION 4 (Sk 10)
- Public-G projection arms: (a) no block R; (b) block R tiers A + C; (c) plus B2 and A82 sets.
- "OHS-5 only" decision types (no usable public eval): shell-action gating, recovery/escalation, done-claim,
  ask-or-proceed, control-next, config/migration review. Report-only where licences allow: CredLeakBench (secret
  egress), Impossible-* and EvilGenie (test gaming), SWE-bench-family verdicts (patch verdicts).

TIMELINE (replaces the v3.2 timeline; UTC). One track up to Thu 29 Oct; the EARLY data freeze is only a declaration
made on Thu 29 12:00 from measured status (Sk 18: no extra work items for it). Training is on the renewed 1 Nov credit
in both cases (R1 as written; R15 dropped, Sk 13).
| Date (UTC) | C2.1 (training side) |
|---|---|
| Sun 18 Oct (D1) | v3.2-r (this revision); NEW G0-lites and G0 addenda written (list in 16.9); L-R LICENCE RECORDS ONLY (URL, quote, fetch date; no download, no reader code, Sk 5); two-stage 8.5 pre-registration file drafted (membership per batch fixed); conformance maps started in SEPARATE fresh sessions (Sk 17); No-Fee terms scout started; day-1 usage burn per lane recorded |
| Mon 19 Oct (D2) | Opus batch 1 (fresh, high): new G0-lites + addenda. Opus batch 2 (separate fresh session): names manifest v1.1 freeze (DI-TS member sources, md_* names, L-R / P1-realism vocabulary, new family ids in row_job_families_allowed); A61(d) two-stage 8.5 ruling (Sk 5); A82 1 strict-reading ruling (Sk 3); Gandalf "selection-rule" record (Sk 7); rule-3 / A46 note (Sk 6). Orchestrator moves SEALED_DELTA_v32.md UNREAD into the sealed directory (audit-logged, Sk 9). Generator / solver CODE in L-A, L-I, L-T, L-C, L-G. L-K, L-P and L-R builders launch after the 15:00 reset ONLY if the measured day-1 burn projects under the 90% weekly shed line (Sk 21). Usage reset 15:00 |
| Tue 20 Oct (D3) | 8.5 S-pre batch 1 (only after the Mon 19 Opus ruling); L-0b builds the stamp service, stamp wrapper and mix guard, and the registry program fetches test/dev splits into the registry-only store; split_aware_check.py and row_start_guard fixes (16.1 step 0); reader code only for sources with an S-pre PASS; sealed side's COUNT report (G sources / items) |
| Wed 21 Oct (D4) | stamp-service throughput on 10,000 block-R-length rows against a FINAL-SIZE registry (every test/dev split, a stand-in at OHS-5 export size) -> second-host ruling the same day (Sk 14, 22); sandbox sign-off; No-Fee terms result (Opus confirms); C2 report (about) and R14; od-l4b queue plan; measured time per source from batch 1 -> second L-R builder yes/no (Sk 17) |
| Thu 22 Oct (D5) | format exposure probe; registry sha fixed (OHS-5 export added Sat 24); methods-per-target table and hash-export salt signed (Sk 15); training-side hash export v1.1 |
| Fri 23 Oct (D6) | free probes on C2 (A10, A11, A14); read-twice zero-shot test on C2 (od-l4b); 12:00 LAST source addition (manifest v1.2 at most; names-only to L-S the same day, Sk 19); S-pre stage closes 23:59 |
| Sat 24 Oct (D7) | by 18:00: read-twice decision (Sk 16 condition), stamp service signed off (else row jobs wait, Sk 22), every conformance record signed (else that record type starts no rows, Sk 23b); 23:59 OHS-5 freeze target; OHS-5 hash export loaded |
| Sun 25 Oct (D8) | ROWS START (row-start guard): 1,000-row pilots in every lane, every row answer-checked and stamped at creation; C2 replay pool cleaned once against every target; 8.5 S-post stage starts; B2 full-train-split G13 starts in Mac windows (Sk 3) |
| Mon 26 Oct | sealed HARD STOP 23:59 (delta stamp pass if sealed grew); set-level gates on the pilots; MEASURED cost projection from pilot token histograms -> shed level set (Sk 11); replay clean-up done; usage reset 15:00 |
| Tue 27 - Wed 28 Oct | full generation, stamped at creation; one combined fix per family landed by Wed 28; set-level gates once per built family and per L-R dataset; C2 reads on od-l4b (trap selection, A46-style screen on block-R human-label rows, difficulty bar); public-G panel reads; L-E dry runs; B2 rows only for B2 sets with 0 hits |
| Thu 29 Oct 12:00 | last fix iterations; last S-post passes; projection re-measured; orchestrator declares EARLY or FALLBACK |
| Fri 30 Oct 12:00 (EARLY only) | DATA FREEZE -> confirming G13 (16.1 step 8) -> selection, mix, d2-set, final-mix 8.5, preflight -> GO #1 packet ready Sat 31 |
| Sun 1 Nov | Modal renewal: live credit check (ONE account >= 1.25x measured projection, Sk 12); EARLY: if GO #1, training on the renewed credit (about 4-6 h) |
| EARLY Mon 2 - Fri 6 Nov | grid reads Mon 2 -> GO #2 Tue 3 -> R9 one look + Jev read Wed 4 -> Tier-1 Thu 5 -> report about Thu 5 - Fri 6 Nov |
| Mon 2 Nov | FALLBACK DATA FREEZE 23:59; usage reset 15:00 |
| Tue 3 Nov | FALLBACK: confirming G13; selection, mix, d2-set, final-mix 8.5, preflight; GO #1 packet |
| Wed 4 - Mon 9 Nov | FALLBACK: training Wed 4 -> grid Thu 5 -> GO #2 Fri 6 -> R9 + Jev read Sat 7 -> Tier-1 Sun 8 -> report Mon 9 Nov (latest about Sat 14 Nov) |

WHAT MUST GO RIGHT FOR THE EARLY FREEZE (planner judgement; FALLBACK is the realistic date)
1. OHS-5 freezes Sat 24 without the Mon 26 slip. 2. Manifest v1.1 freezes Mon 19 and v1.2 (if any) lands Fri 23
12:00 without a late C-transfer re-pick. 3. The stamp service is signed off by Sat 24 18:00 and its MEASURED throughput
keeps up; the replay clean-up ends Mon 26. 4. Sandbox sign-off Wed 21. 5. Each family passes its first pilot or lands
its one fix by Wed 28. 6. S-pre and S-post 8.5 stages finish by Thu 29 12:00 (sources that miss are left out, logged).
7. The single free L4 holds its queue. 8. Claude usage holds through the Mon 26 reset with no P0 lane shed. 9. C2
reports by about Wed 21. 10. MONEY: the run must fit ONE account at 1.25x (about $24 at a $30 renewed credit), against
a per-row projection of $26-32 that is probably low (Sk 11): stage B and further shed steps are likely; the measured
Mon 26 projection decides.

MONEY [A79 R1; A82 9; HANDOFF 18 Oct] (moved from section 11; v3.2-r changes marked)
- C2: about $15 (measured: current mix $15.09 for 62,982 rows; dry run $17.03 for 75,370 rows; about $5 per 1K steps;
  T_max $22.96). C2 is paid from mahadikarya2 -> mahadikarya3 under A81.
- C2.1 projection: per-row DERIVED $26-28 without stage B and $30-32 with it (about 112.5K rows) drives NOTHING
  (Sk 11). The binding projection is MEASURED on Mon 26 from pilot token histograms x C2's measured $ per token,
  re-measured Thu 29 12:00 and at the data freeze, and replaced by the measured s/step before GO #1. Caps (A79 R1):
  Modal total <= $35, training <= $30 incl. stage B; A82 9: no raise of the $30 cap.
- MONEY SHED ORDER (pre-registered; applied ONLY to a MEASURED projection; stops as soon as the projection
  <= min($30, ONE account's live credit / 1.25), Sk 12): (1) R12 stage B; (2) A14 long-input share -> eval-only;
  (3) verbose A15 dialects (compact stay); (4) A10 held-out-wrapper extras; (5) voice pool to its 1,500 floor; (6) P1
  realism slices and P1 heads uniformly to half; (7) block-R per-dataset caps lowered uniformly (floor 300 rows; no
  dataset removed); (8) general block to 5,000; (9) stop and ask the owner (A37(k) style). Never shed: P0 and P0-extra
  family sizes, the replay count (a ceiling that may shrink only to the clean count, Sk 23c), the training floor. Step
  9 can only be "train the shed mix" or "wait" (A82 9).
- RELAY RULES (v3.2-r Sk 12, 13): payers mahadikarya2 -> mahadikarya3 only, exactly as A79 R1 words it, and only if the
  Wed 21 No-Fee terms check clearly allows it; no third account (R15 dropped); never a card (aryamhd never pays). The
  1.25x test applies to ONE account's live credit (strict R1 reading); the summed-relay reading is an owner question in
  the GO #1 packet. Credit is read only through the existing read-only billing check, never by launching anything.
- MODAL NO-FEE TERMS CHECK (Wed 21 Oct): a Haiku scout finds and reads the separate No-Fee terms that
  https://modal.com/legal/terms section 1.2 refers to; Opus confirms. If they bar or do not clearly allow a
  multi-account relay: no relay for C2.1, and the orchestrator is told the same day that C2's own relay is affected.
- OpenRouter: Jev reads about $2.4 (DERIVED) against the live key balance (re-read by the price script before the read).

### 16.8 v3.2 skeptic response (to C2_1_PLAN_v3_2_SKEPTIC.md, sha256 cf7bd62f…; one line each)

| # | Sev | Verdict | Where / what |
|---|---|---|---|
| 1 | HIGH | FIXED | Section 2 8.5 PROCEDURE and 16.1 step 0: DI-TS expanded to logical-entailment-dataset, temporal-expressions-evaluation-lm, perspectrum (re-VERIFIED from SOURCES_DITS_85.json); A61A_HITS + manifest v1.1 + CPU tests; every A61(a) group expanded from its 8.5 inputs |
| 2 | HIGH | FIXED | 16.1 step 0: release needs a G13 result record over the FULL train split and writes train_split_seen: true; one CPU test per A82 1 condition (re-VERIFIED: the code releases on split names alone) |
| 3 | HIGH | FIXED | 16.1 B2 DISJOINTNESS: strict whole-split reading binds; full split, not 1,200 rows; row-drop reading only as a GO #1 packet question for C2.2; Opus ruling Mon 19 |
| 4 | HIGH | FIXED | 16.1 step 1 and 16.3 rule 2: test/dev splits fetched only by the L-0b registry program into a store no agent reads |
| 5 | HIGH | FIXED | Section 2 and 16.3 rule 1: licence records only until S-pre PASS; S-pre (OHS-3/4/AC) and S-post (OHS-5) pre-registered in one file; no re-run within a stage; Opus A61(d) ruling before batch 1 |
| 6 | MED | FIXED | 16.3 rule 3 reworded; Opus note that the block-R A46 screen is a stricter drop-only use |
| 7 | MED | FIXED | 16.3: "selection-rule" provenance; Gandalf ignore-instructions DENY, rolled to C2.2; direct injection about 100 + twins |
| 8 | MED | FIXED | 16.3 rule 4 NAMES: scoped exemption for L-R / P1-realism rows; vocabulary extracted into v1.1/v1.2 before the freeze; DataDog swap or recorded T63 exception |
| 9 | HIGH | FIXED (process) | Header and section 3: the delta is moved unread to the sealed dir, re-derived by a fresh sealed Opus from G1-G8 + literature, reviewed by a second; Mon 19 23:59 or dropped. The file itself was not opened (path rule) |
| 10 | MED | FIXED | Section 4 lines and section 11 timeline / money moved to 16.7; section 11 now has a sealed-safe calendar |
| 11 | HIGH | FIXED | Section 5 cost note and 16.7: Mon 26 measured token-based projection sets the shed level |
| 12 | HIGH | FIXED | Section 10 R1 READING and 16.7: strict one-account reading binds; bound min($30, one account / 1.25); relay reading in GO #1 packet |
| 13 | HIGH | FIXED | Section 10: R15 dropped; relay only as A79 R1 words it and only if the No-Fee terms clearly allow it |
| 14 | HIGH | FIXED | 16.1 step 8: confirming pass = stamp audit + full exact/hash re-run + fuzzy on delta targets; throughput sized on the final registry; any hit stops the mix |
| 15 | MED | FIXED | 16.1 steps 1-2: methods listed per target; separate hash-export salt held by the matcher only; sealed counts-only reverse check covers the rest |
| 16 | MED | FIXED | Build order L-0b and 16.7 Sat 24: read-twice adopted only if a program shows the new scaffold is the exempted strings repeated with no new text (Opus records it); else C2.2 |
| 17 | HIGH | FIXED | Build order: L-0 split into L-0a / L-0b; conformance maps in separate fresh sessions; L-R source-group order pre-registered, second builder by measured time; Opus batches per group; Mon 19 Opus work split into two sessions |
| 18 | MED | FIXED | 16.7: only the Thu 29 declaration remains; no stretch work items; R15 removed |
| 19 | MED | FIXED | 16.3 rule 1: last source Fri 23 12:00 (v1.2 at most), names-only to L-S the same day; Humicroedit / NLI4CT A82 4 checks |
| 20 | MED | FIXED | Section 3: Tue 20 counts-only report; R7 / R13 as A79 decided; owner told that day |
| 21 | MED | FIXED | 16.7 Mon 19 and build order global order 4: L-R / L-K / L-P launch only under the measured day-1 burn projection |
| 22 | HIGH | FIXED | 16.1 STAMP-SERVICE STOP RULE: unsigned by Sat 24 18:00 = row jobs wait; freeze does not move; second-host ruling Wed 21 |
| 23 | MED | FIXED | (a) 16.1 step 3 and 16.3 rule 6; (b) 16.1 step 0 deadline; (c) 16.1 step 5 and 16.7; (d) 16.1 step 5 Opus note |
| 24 | LOW | FIXED | 16.1 step 0: CDLA claim corrected; maps from code; family-field check; new family ids allowed |
| 25 | LOW | FIXED | 16.3 rule 4: span-position / length probe per long-document dataset |
| 26 | LOW | FIXED | 16.3 rule 1 (upstream licence) and code-realism row (per-repo licence; T57r negatives from our mutator only) |
| 27 | LOW | KEPT | No action (skeptic found these correct) |
No item was rebutted: each one names a real gap between owner words or rulings and the v3.2 text or code.

### 16.9 G0-lites and per-lane addenda that must now be written (Sun 18 Oct; Opus batch 1 on Mon 19)

NEW G0-LITES (Sonnet 5.5 high writes; with PRE-FREEZE / POST-TRAINING gate split and numeric bars)
| Family / lane | Scope |
|---|---|
| T59 ASK-OR-PROCEED (L-K) | 2,000 rows, P0-extra; 8-trigger paired design (A9); k-interpretation gold; PROCEED >= 55%; trigger-only probe; G9 with T50/T51/T54 |
| T60 CONTROL-NEXT (L-K) | 2,000 rows, P0-extra; delegate/do, keep/drop, plan/act heads; label share 40-60%; important-looking-fact probe |
| T63 DEP-RISK (L-P) | about 1,200 rows + DataDog 500 via L-R; EXISTS and licence heads; seeded snapshot + stdlib symbols; DataDog name swap / T63 exception (Sk 8) |
| T66 REVIEW-GATE (L-P) | 800 head rows + CommitPackFT 800 via L-R; merge / semver / message heads on od-sbx1; per-repo licence whitelist (Sk 26) |
| T67 IAC-GATE + MIGRATION (L-P) | 1,000 rows (700 + 300); rule table on SLT-1; Checkov / squawk validators only; round-trip drop bars; G9 extension |
| L-R LANE (block R) G0-lite (L-R) | rules 1-8 of 16.3 as gates: provenance enum incl. selection-rule; S-pre / S-post; strict B2; recast-table template; per-dataset set-level bars (balance, duplicates, length, variety, span probe); A46 drop-only screen; names exemption; stamp-drop triggers |
| T62 FLAKY-OR-REAL (P1; L-P wave C) | only the slice fed by LogChunks 700 + FlakeFlagger 200; needed before those L-R rows map (by Fri 23) |
| T65 VULN-SYNTH (P1; L-P wave C) | synthetic CWE + Juliet 700 good/bad twins via L-R; no CVE ids (F2); needed before the Juliet rows map (by Fri 23) |

PER-LANE G0 ADDENDA (v3.2; each also copies in the round-1 / round-2 binding conditions from G0_APPROVALS.md)
| Lane | Family | Addendum scope |
|---|---|---|
| L-A | T50 | A3 edit-as-action sub-family (1,500-2,500), A4 alias (300-500), A5 late-binding (150-300), A6, A10 (if probe says build), A12, A15, difficulty ladder; G9 extended to edit actions and T67 |
| L-A | T51 | A3 scope variants, A6, A10, A12, A15, ladder |
| L-A | T53 | phishing-link head (G7, <= 25% of specs), A6, A10, A12, A15, ladder |
| L-I | T41c | A13 benign-worded hijacks + lexical-balance probe, A14 (if probe says build), A16, A12, A10, ladder; benign twins for Aya and Gandalf summarization only (Sk 7) |
| L-T | T54 | A8 smelly descriptions, A16, A12, A10, A14, ladder |
| L-T | T55 | LIMBO citation fix, A16, A12, A10, A14, ladder |
| L-T | T56 | A7 verification-relevance near-misses, A16, A12, A10, A14, ladder |
| L-C | T42c | compile / type-check head (about 300; type-checker component-licence check first), A16, A10, ladder |
| L-C | T57 | A10, A16, ladder; LOCALISE realism (ManySStuBs4J / TSSB-3M) and T57r slice (SWE-Gym, SWE-smith procedural; negatives only from our mutator, per-repo licence, Sk 26) |
| L-C | T56g | A10, A16, ladder |
| L-G | GEN | about 2,000 third-party-generator rows (Reasoning Gym allow-list, DM Math, bAbI; fresh seeds), gold-by-construction hard extensions, NOTA out of the mix, A21 length coverage |
| L-G | VOICE | R11 decided (A79); A18 generator C after its dictionary-licence check |
| L-0b | (infra) | stamp-service, wrapper, mix-guard and confirming-pass specs (16.1 steps 2, 7, 8); methods-per-target table; names-guard L-R / P1-realism exemption |
