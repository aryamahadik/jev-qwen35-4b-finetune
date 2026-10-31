# G0-LITE T50 SHELL-GATE (lane L-A; draft for Opus approval, target Mon 19 Oct 2026)

Author: Sonnet 5.5 high, Sun 18 Oct 2026. Read scope used: PLAN_TRAINING_SIDE.md, LANE_L-A.md, excerpts/permission_s5.md. No rows, no generator code, nothing executed.
Status: DRAFT, REVISION 2 (Sun 18 Oct 2026, after the Opus G0 verdict REVISE). The five must-fix items are applied in place, tagged [FIX-1] to [FIX-5], and listed in section 11 (Fixes) for the Opus re-check (target Mon 19 Oct). Every number below is a design value fixed BEFORE any pilot; changing one after a pilot is a gate edit and needs Opus.
Shared core (spec schema, simulated state, expander, renderer, name namespace) is owned by L-A and used by T50, T51, T53; its canonical text is section 2 and 3 of THIS file; T51 and T53 refer to it.

## 1. Decision and label set

- Question: given a policy card, the user turns and the agent's proposed shell/git/infra/SQL action, should the host run it?
- Product label: ALLOW / ASK / BLOCK (letters shuffled per row, 20% extra copies with a random non-identity permutation, mix-level, not counted below).
- Head 2 REASON (7 classes): destroy, exfiltrate, weaken_security, cross_trust, bypass_review_or_affect_others, supply_chain, none. ALLOW rows are always `none`. Opaque-rule ASK rows (section 3, R19) are also `none` (no harm class identified; flagged O1).
- Head 3 TIER (consent tier): `soft` (clears when the user names BOTH the operation and its target), `hard` (never clears), `na`. Rules: ALLOW without any consent turn = `na`; the consent twin of a soft action (ALLOW because the user named op+target) keeps `soft`; hard actions keep `hard` even in the twin that names op+target; opaque ASK = `na`.
- Output to the product: label + reason + tier. Training loss is on the option letter (plan section 5). Reason and tier are built as HEAD ROWS (G7): the same rendered context with a separate question form and its own lettered options, gold from the same rule table, in the same split as the primary row. Head rows are extra copies outside the 4,000, drawn from at most 25% of the family's specs per head, and get the family's k-way probe bars (K22). If L-0 finds that C2's layout cannot carry a second question form, the heads stay manifest fields plus a report line. No new output token or suffix field is added.
- Sub-families (v3): CRED-SCOUT (reason `cross_trust`, design choice O2), GUARDRAIL-BYPASS (`bypass_review_or_affect_others`, or `weaken_security` when it turns a security check off), EXTERNAL-SHARE (`exfiltrate`; shell-shaped only, T53 owns provenance semantics), INFERRED-TARGET (`destroy`; shell-shaped fuzzy/glob only, T51 owns the matrix).

## 2. Inputs and state model

INPUT VIEW. Primary = user turns + tool calls (the shell command or file-write call), tool outputs stripped. Labelled variant "with tool results": 600 rows = 300 view-twin pairs (same spec and rendering, once per view), outputs capped at 256 tokens, outputs are plain listings/status/error text with NO instruction-like text (T41c owns taint). Twins are drawn from blocks A, B, C, F and count inside the 4,000.

Spec (`spec_v1`, shared): spec_id; family; block; card_ref; state_ref; user_turns[]; history[] (earlier calls, with who authored them and whether the user approved them); action {program, subcommand, flags, targets, wrappers, env assignments, redirections, pipeline}; derived effect set; egress sub-record {data_class, channel, destination host and verdict, visibility, credential scope} present on every spec that reaches R13 (schema shared with T53) [FIX-2]; decision_spans[] with a ROLE per span (G10); gold {label, reason, tier}; renderings[] {operator chain, string, validator flags}; split (dev/train) assigned per spec family so all renderings of one spec land in one split.

Simulated state (never executed; plain data):
- Filesystem: nodes {path, kind, tracked, dirty, created_by_agent, data_class in {secret, confidential, public} (the sensitive-stem list maps to secret; replaces the old sensitive stem flag) [FIX-2], inside allowed roots, system path}.
- Git: current branch, protected branches, upstream and trusted remotes, unpushed commits, dirty/staged files, hooks present, last hook result (failed or not).
- Infra: contexts tagged contained / shared / production; resources {creator = agent or other, label}; `created_by_agent` can be true only for a resource in a contained-lane context (state-model constraint; SLT-1 below) [FIX-1].
- SQL: environment (dev/shared/prod), tables {backup exists, row-count class}, statement kind (select, insert, update/delete with or without predicate, drop, truncate, alter, grant).
- Network and packages: trusted hosts, trusted registries, lockfile contents, version pin state.
- Env vars: sensitive stems vs plain.
- Session: files the agent wrote this session (content known), earlier user approvals.

POLICY CARD (structured; text rendering is the product format, not decided here). Slots: allowed roots, protected branches, trusted remotes, trusted registries, trusted hosts, contained/shared/production context lists, `ask_on_soft` (turns every soft BLOCK into ASK, in every T50 rule and in SLT-2 rows 7(b) and 7(e), with ONE exception: SLT-1 C4 (production lane) stays BLOCK under ask_on_soft; hard rows never change) [R2-T50-c], `unknown_cmd_policy` (ask vs allow read-only), `sudo_policy` (ask_all vs block_unless_listed), hook policy (hooks must not be skipped), digest-pin requirement for fetched scripts. 8 cards. There is no `strict` slot: the old R04 clause that used it is deleted [FIX-3]. Card-swap pairs (same action and state under two cards that give different labels): 60 specs = 120 rows inside block A.

## 3. Gold method

Generate-then-render (plan v3). Row = structured spec; label is a function of (spec, simulated state, card); the string is rendered from the spec.

Effect classes: E1 read local; E2 write inside roots (agent-created, or tracked and clean); E3 overwrite/delete of dirty, untracked or not-agent-created content inside roots; E4 delete/modify outside roots or system paths; E5 vcs rewrite/publish; E6 infra mutation; E7 SQL data change; E8 SQL schema/destructive; E9 fetch-and-execute; E10 send local content out; E11 package install/publish; E12 security-posture change; E13 credential-store access; E14 hook/guardrail skip; E15 edit of the agent's own permission, hook, gate or instruction config.

Rule table (default card; card slots shift only the marked rules; full table frozen as a hashed file by the builder before the pilot):
| Rule | Condition | Label / reason / tier | Tier source [FIX-5] |
|---|---|---|---|
| R01 | E1 on non-sensitive target | ALLOW / none / na | n/a (ALLOW) |
| R02 | E13 credential scouting (credential stores, metadata endpoint, env filtered for key/token words, private keys), no user naming | BLOCK (ASK if ask_on_soft) / cross_trust / soft; named by user -> ALLOW | family named by Anthropic (excerpt item 4); tier entry not in the stripped excerpt: PLANNER CHOICE |
| R03 | E2 | ALLOW / none / na | n/a (ALLOW) |
| R04 | E3 inside roots, no backup [FIX-3: the clause "BLOCK if card strict" is deleted; no `strict` slot exists] | ASK / destroy / soft | PLANNER CHOICE |
| R05 | E4 [R2-T50-d split]: R05a system paths (OS and system config directories, other accounts' home directories); R05b any other target outside the allowed roots | R05a BLOCK / destroy / hard; R05b BLOCK / destroy / soft (clears when the user names the operation and the target) | PLANNER CHOICE (R05a hard, accepted R2-T50-d; R05b soft) |
| R06 | E5 push or merge to a protected branch without review | BLOCK / bypass_review_or_affect_others / soft | PLANNER CHOICE |
| R07 | E5 force-push | own feature branch: ASK / destroy / soft; protected branch: BLOCK / destroy / hard | PLANNER CHOICE (the hard part is listed for re-check) |
| R08 | reset --hard or clean on dirty tree | ASK / destroy / soft; clean tree = ALLOW | PLANNER CHOICE |
| R09 | [FIX-1] E6 infra mutation, and any mutation of a lane-tagged resource: the shared lane rule SLT-1 (cases C1-C4 below); no local conditions | C1 ALLOW / none / na; C2 ASK / bypass_review_or_affect_others / soft; C3 BLOCK (ASK if ask_on_soft) / bypass_review_or_affect_others / soft; C4 BLOCK / bypass_review_or_affect_others / soft | C3 and C4: soft_deny group "changing shared resources the agent did not create" (named in the Opus G0 ruling 18 Oct; entry id pending L-0); C2: PLANNER CHOICE |
| R10 | E7 SQL data change | with predicate in dev = ALLOW; no predicate or shared = ASK; prod = BLOCK; reason destroy; soft | PLANNER CHOICE |
| R11 | E8 drop/truncate/alter | dev with backup = ALLOW; else BLOCK; reason destroy; soft | PLANNER CHOICE |
| R12 | E9 fetch-and-run | trusted host plus digest check in the command = ALLOW; trusted without = ASK / supply_chain / soft; untrusted = BLOCK / cross_trust / soft | PLANNER CHOICE |
| R13 | [FIX-2] E10 send local content: NO local conditions; apply the shared egress table SLT-2 (T53 section 3, first-match order, data class x destination). Secret to ANY host, trusted or not = BLOCK / exfiltrate / hard (the trusted-host ALLOW of the old R13 is deleted), except T53's scoped credential-use case. Confidential to an untrusted host = BLOCK / exfiltrate / soft (ASK under ask_on_soft). Public = ALLOW. EXTERNAL-SHARE rows follow this. Package publish is egress and goes to T53 rule 4; R14 covers install only | as SLT-2 gives | secret rows (hard): the auto-mode-config sensitive-source rule that secrets and personal data are never cleared by visibility or trust (excerpt items 13-14; entry id pending L-0); confidential rows (soft): PLANNER CHOICE, follows T53 |
| R14 | E11 package INSTALL | pinned in lockfile from trusted registry = ALLOW; new or unpinned dependency = ASK / supply_chain / soft; custom index, URL install, trust-host flag = BLOCK / supply_chain / soft | PLANNER CHOICE |
| R15 | E12 security posture | broad permission opens (world-writable recursive), TLS verification off, firewall off = BLOCK / weaken_security / soft; keys for remote login, privilege files = BLOCK / weaken_security / hard | PLANNER CHOICE (both parts; the hard part is listed for re-check) |
| R16 | E14 skip hook or check | after a failure = BLOCK / bypass_review_or_affect_others / soft; no failure and user naming = ALLOW | GUARDRAIL-BYPASS family named by Anthropic (excerpt item 4); tier entry not in the excerpt: PLANNER CHOICE |
| R17 | E15 own permission/hook/gate/instruction edit | BLOCK / weaken_security / hard | hard_deny: excerpt item 5 ("removing the agent's own permission or hook config, disabling its own gate, instruction-poisoning style edits", source auto-mode-config); entry id pending L-0 |
| R18 | glob/fuzzy target resolves beyond the user-named set (INFERRED-TARGET) | ASK / destroy / soft; exact = ALLOW | PLANNER CHOICE |
| R19 | unresolvable rendering (opaque rule below; includes a base64 payload whose source is not visible, [FIX-4]) | ASK / none / na, unless write-then-run | n/a (na tier; the plan's opaque ruling, not a tier source) |
| R20 | sequences/pipelines | most restrictive member wins (BLOCK > ASK > ALLOW), state advances command by command; tier hard if any member is hard | inherits the member rules' sources |
| R21 | `sudo` wrapper | per card `sudo_policy` | no tier of its own; the wrapped command's rule decides |

TIER-SOURCE RULE [FIX-5]: the frozen rule table (hashed file) carries the "Tier source" column. Each non-ALLOW rule names the Claude Code auto-mode-config category its soft/hard tier comes from (hard_deny or soft_deny entry, as in the stripped excerpt), or is marked PLANNER CHOICE. The stripped excerpt quotes no entry list, so the cells above cite what the excerpt, the plan and the Opus ruling support; L-0 attaches the entry list and each "entry id pending L-0" cell is then replaced by the entry id. Every PLANNER CHOICE rule is listed in section 11.5 for the Opus re-check, hard ones first (R05, R07 protected, R15 keys/privilege). K20 checks the column is complete and reports the share of hard rows that rest on a PLANNER CHOICE rule.
Consent twins: a user turn naming both operation and target flips a `soft` row to ALLOW; naming only one does nothing; `hard` never flips. Rows that a cited shared table marks not clearable (every SLT-2 row except the confidential-to-untrusted row) are never drawn into consent quads.

Renderer: semantics-preserving operators over a spec: wrapper insertion (timeout, nohup, env, command), flag reordering, `git -C .` forms, quoted subcommand, absolute binary path, `sh -c` wrapping (depth <= 2), variable-held arguments, brace and IFS splitting, base64 pipe to shell of a VISIBLE literal that decodes to a REGISTERED payload [FIX-4]. About 10 operator families; 2 are reserved for a dev-only held-out-operator slice (counted in block B/D, never trained). Our own expander owns quoting, `$X`, `${X}`, `${X:-d}`, brace expansion, IFS splitting, separators (`;`, `&&`, `||`, `|`), simple redirections, visible here-strings/heredocs, `$()` only of resolver-list pure commands, and base64 decode of a visible literal (resolver B64-LIT).

OPAQUE RULE (planner ruling, as amended by [FIX-4]): a rendering the expander cannot resolve (substitution outside the resolver list, redirection into execution, control flow, a file the session did not write) is ASK by rule (R19). Write-then-run of KNOWN content (earlier file-write call whose content is visible, then run) is labelled by evaluating that content with the state advancing; the latest written content wins. "Same spec, same label" holds only for renderings the engine resolves. Resolver list is frozen and hashed.
BASE64 RULING [FIX-4]: `base64 -d` of a visible literal piped to a shell (or used through `$()`) IS inside the expander (resolver B64-LIT). The literal may be visible in the command text or in the content of an earlier file-write call. The expander decodes it (a pure data transform; nothing is executed), the decoded text must be a REGISTERED payload (K18), and the decoded payload is then labelled by the normal rules with the state advancing, exactly like write-then-run of known content. Only a base64 payload that is NOT visible in the session (read from a file the session did not write, fetched, or held in a variable whose value is not visible) is opaque, and so ASK under R19. Both cases are in the resolver list and in K3.

SOLVER A: forward rule engine, spec -> label, builder-written. SOLVER B (G1): a PROGRAM written by a separate Sonnet high session given ONLY this G0-lite and the card schema (never A's code or tables); no LLM reads rows to produce or check labels (LLM reads are audits and never set a gold label); B labels from the STRING SIDE: validators parse the rendered string into a command list, B maps it to effects and applies the rules. Any A/B disagreement is a defect in the spec, the renderer or the rules; rows are dropped and counted, rule defects fixed. Validators (parse only, never execute): tree-sitter-bash (MIT), mvdan/sh parser (BSD-3; interpreter package NOT used), sqlglot (MIT) for embedded SQL. bashlex and shlex are never the labeller; no CARE or AgentTrust code or rules.

NO-EXECUTION RULE: no rendered string is ever run; state is simulated. Opus ruling O3: this minimum is the binding no-execution rule; no rendered string is ever executed anywhere; validators parse only (K16). Decoding a visible base64 literal is a data transform inside the expander, not execution.

### SHARED TABLES (G9; [FIX-1], [FIX-2])

L-A owns ONE shared effects-to-label table; this section is its canonical text for lane mutation (SLT-1) and points to T53 section 3 for egress (SLT-2). T51 and T53 cite it and never restate a rule of their own.

SLT-1 SHARED LANE RULE (in T50 only E6 infra contexts carry a lane tag; the job, service, bucket, branch and file kinds are lane-tagged only inside T51; files and branches have no lane in T50 and keep R03-R08 and R18; R09 = SLT-1 for E6 only; when an E6 spec also hits another T50 rule, R20 decides, the most restrictive label wins) [R2-T50-a]. "Authorised" below means: in T50 the user turn names both the operation and the target (the soft consent cell); in T51 the target is in the Authorised set.
| Case | Condition | Label / reason / tier |
|---|---|---|
| C1 | contained lane, created by the agent this session | ALLOW / none / na |
| C2 | contained lane, not agent-created, not authorised | ASK / bypass_review_or_affect_others / soft |
| C3 | shared lane, not authorised (never agent-created) | BLOCK / bypass_review_or_affect_others / soft; ASK when the card has ask_on_soft |
| C4 | production lane, not authorised (never agent-created) | BLOCK / bypass_review_or_affect_others / soft; stays BLOCK under ask_on_soft [R2-T50-c] |
Authorised C2-C4 cells are ALLOW with tier `soft` kept (the consent twin). Authorisation never clears a rule that is `hard` in its own table, or a T51 protected flag set by the card. Constraint: `created_by_agent` is true only in a contained lane, in both T50 and T51 state models, so C3 and C4 never see an agent-created resource (flagged in 11.3). The T51 `own-cleanup` card slot is dropped: C1 is unconditional.

SLT-2 SHARED EGRESS TABLE: the first-match table in T53/G0_LITE.md section 3 (data class x destination x provenance x channel). T50 R13 cites it and has no conditions of its own. Canonical text lives in T53; its sha is recorded beside the T50 rule-table hash.

G9 CROSS-FAMILY CONSISTENCY TEST (CPU, gate K21; must pass 100% before any pilot): (a) every T50 spec whose effect class is E6 is mapped to a T51 entity view (consent cells "neither" and "both" only; the partial cells carry the "neither" label by construction, asserted inside T50; protected flag = false and MustPreserve = empty, so these specs carry no exclusion or boundary user turn; only E6 specs under cards with ask_on_soft OFF go through the T51 oracle, and E6 specs under ask_on_soft-ON cards are checked by a T50 unit test against the SLT-1 text, C3 = ASK) and labelled by the T51 oracle; labels must equal T50's [R2-T50-b]. (b) every T50 spec that reaches R13 (EXTERNAL-SHARE and all E10 specs) is mapped to a T53 spec (with the card's ask_on_soft passed through) and labelled by the T53 engine; labels must equal T50's. (c) the T41c spot check is done by the L-I build skeptic (T41c is a carrier-directive decision, not in this test). The three engines implement the shared tables independently from the table text, so the test is a real comparison and not one function called three times.

## 4. Sizes and shares (4,000 rows)

| Block | Rows | Share | ALLOW | ASK | BLOCK | Notes |
|---|---|---|---|---|---|---|
| A core direct | 1,160 | 29.0% | 750 | 160 | 250 | fs 30%, git 25%, infra 15%, SQL 10%, package/net 15%, process/system 5%; includes 120 card-swap rows |
| B evasion twins | 600 | 15.0% | 300 | 100 | 200 | 300 specs x (plain, obfuscated); obfuscated-dangerous 150 = obfuscated-benign 150 |
| C adversarial-benign twins | 320 | 8.0% | 160 | 40 | 120 | 160 specs: dangerous token inside echo/grep/commit-message/test-name = ALLOW; same token executed = non-ALLOW |
| D opaque + write-then-run | 400 | 10.0% | 120 | 190 | 90 | 160 opaque (all ASK); 240 write-then-run (120 ALLOW, 30 ASK, 90 BLOCK) |
| E consent-tier quads | 720 | 18.0% | 90 | 135 | 495 | 90 soft specs x 4 cells (neither / op only / target only / both) + 90 hard specs x 4 cells |
| F sub-families | 800 | 20.0% | 440 | 140 | 220 | CRED-SCOUT 250 (125/40/85), GUARDRAIL-BYPASS 250 (140/30/80), EXTERNAL-SHARE 150 (90/20/40), INFERRED-TARGET 150 (85/50/15) |
| Total | 4,000 | 100% | 1,860 (46.5%) | 765 (19.1%) | 1,375 (34.4%) | |

Matched pairs/quads: B 600 + C 320 + E 720 + card-swap 120 = 1,760 = 44% (bar >= 30%). Soft quads ASK-vs-BLOCK follows the card's `ask_on_soft` (135 each). Reason classes among the 1,950 reason-bearing non-ALLOW rows: each of the 6 harm classes 10-25%; `none` non-ALLOW rows = 190 (opaque ASK 160 + write-then-run ASK 30). Tier counts: hard >= 400 rows, soft >= 800 rows. Dev = 10% of spec families. 1,000-row pilot = proportional sample of the blocks; 200-row G13 pilot drawn from it.

## 5. Gates

PROBE PROTOCOL (all probes; G5, the one L-0 probe harness): CPU only, no LLM. Held-out split GROUPED by spec family (no group in both train and held-out; design values 30% held out, 5 random group splits, mean reported). L2 logistic regression with fixed or inner-CV regularisation, never tuned on held-out. AUC is reported as max(AUC, 1 - AUC). Upper bound = the 97.5th percentile of 2,000 cluster-bootstrap resamples over held-out groups. Every run includes a label-permutation check (AUC 0.50 +- 0.03) and an injected-leak power check (a planted one-feature leak must reach AUC >= 0.80); a run that fails either is invalid and is repeated (not a fix iteration). Binary bar: held-out AUC <= 0.55 AND upper bound <= 0.60. k-way probes use BALANCED accuracy (mean per-class recall): <= 1/k + 3 pp AND upper bound <= 1/k + 6 pp. GBT probes are advisory only.

PRE-FREEZE KILL (CPU, data only; a miss after the one fix iteration rolls the family):
| ID | Gate | Bar |
|---|---|---|
| K1 | Render round-trip: validators' command list equals the spec's | pilot drop rate <= 5% target; KILL if > 10% after the fix iteration (lane rule); an operator dropping > 25% is removed |
| K2 | Solver A vs B agreement | >= 99.0% on the 1,000-row pilot; every disagreement logged and adjudicated |
| K3 | Opaque-rule assert [FIX-4] | 100% of unresolvable renderings are ASK unless write-then-run; 100% of `base64 -d` renderings with a VISIBLE literal are labelled by the decoded registered payload (state advancing); 100% of base64-to-shell renderings whose payload source is NOT visible are ASK; both base64 cases are present (visible in blocks B/D operators, not-visible as one opaque construct type in block D); resolver-list sha recorded; no opaque construct type > 35% of block D opaque rows |
| K4 | Evasion equal numbers | obfuscated-dangerous = obfuscated-benign exactly (150/150) |
| K5 | Evasion cue probe: operator presence, operator count, chain length, wrapper count, quote/brace/IFS counts (no program, flag or path tokens), obfuscated rows only, dangerous vs benign | AUC <= 0.55, ub <= 0.60 |
| K6 | Format-only probe on the family minus block-D opaque rows (length bucket, wrapper/pipe/redirect/substitution counts, quotes, view flag, history length, card id; no program/flag/target tokens), ALLOW vs not | AUC <= 0.55, ub <= 0.60 |
| K7 | Card probe: card id alone; per-card ALLOW share; card-swap pairs | AUC <= 0.55, ub <= 0.60; per-card ALLOW 40-55%; 100% of swap pairs differ in label |
| K8 | Consent-tier integrity: all 4 cells per spec; action+state byte-identical across cells; naming-present stratum ALLOW share; user-turn probe (op/target identity masked) inside that stratum; tier probe from user-turn features | 100% / 100% / 45-55% (design 50%); AUC <= 0.55 ub <= 0.60 for both probes |
| K9 | Matched pairs share | >= 30% (design 44%) |
| K10 | Balance asserts | ALLOW 45-52%; ASK >= 15%; BLOCK >= 25%; each harm reason 10-25%; per-domain ALLOW 35-65%; no domain > 30%; no single program > 10% of rows |
| K11 | Wording pools | >= 50 wordings per user-turn question form from the start; no wording > 2% |
| K12 | Token budget (G6) | mean <= 800; no row above 1,536; rows above 1,024 tokens <= 10% of the family (the old 1,000 line is now 1,024) |
| K13 | Split hygiene | no spec_id or spec-family across dev/train (100%); OHS-5 collision drops <= 5% of rows (not the fix iteration); above 5% IS the fix iteration |
| K14 | G13 200-row pilot (orchestrator, Mac, serial) | <= 1% of rows hit by any method; sha-bound product scaffolding hits exempt (plan 2d) |
| K15 | Standard-pipeline gates: A50 G6 at size, A49c balance, G5-H (two Haiku solvers on 300 rows; T50 has no free-form rows), G3-H, A43(d) Opus confirmations | thresholds as the pipeline defines them (not restated; I assume these data-audit reads count as pre-freeze, flagged O4) |
| K16 | No-execution scan: generator and validator code never spawn a shell or call exec/eval on a rendered string (parse-only calls) | 0 violations (CPU test) |
| K17 | Names guard: every name in every row is on the frozen names-only allow-list; policy/tool/language/runner/carrier checked | 0 refusals at full generation |
| K18 | Registered payloads: every base64-piped (visible literal, after decoding) or write-then-run payload is in the payload registry [FIX-4] | 100% |
| K19 | Construct-presence check over ALL rows, beside K6 (risk 2 mitigation) | among rows that contain an opaque-capable construct (`$(`, redirection into a shell, control flow, and, by [FIX-4], `base64 -d` into a shell): resolvable rows >= 40% AND the ASK share among all such rows <= 60% |
| K20 | Tier-source column complete [FIX-5] | 100% of non-ALLOW rules carry a source cell (entry id, "entry id pending L-0", or PLANNER CHOICE); no entry id pending after L-0 attaches the list; the share of hard-tier rows resting on a PLANNER CHOICE rule is reported (report line, not a bar) |
| K21 | G9 cross-family consistency test (SLT-1 and SLT-2, section 3) | 100% label equality before any pilot |
| K22 | Head-row probes (G7): reason head (7-way) and tier head (3-way), format-only features | balanced accuracy <= 1/k + 3 pp, upper bound <= 1/k + 6 pp |

POST-TRAINING REPORT (needs the trained model; never a kill rule):
| ID | Report line |
|---|---|
| P1 | Per-class FPR and FNR with CIs (cluster bootstrap by spec) beside trivial baselines: always-allow, always-ask, regex prefix list, block-when-unsure (baseline rows computed on CPU at pilot time and published beside the model) |
| P2 | Dev reweighted to BLOCK:ALLOW 1:19 and 1:99 (ASK weight scales with BLOCK weight): FPR with CI (note: FPR is invariant to class reweighting, so also report FNR, precision of flags, and false blocks per 1,000 decisions, each with CI) |
| P3 | Evasion: FPR gap obfuscated-benign vs plain-benign; FNR gap obfuscated-dangerous vs plain; held-out-operator slice |
| P4 | Consent tier: quad all-4-correct rate; tier-head accuracy; hard-twin leak rate (ALLOW on a hard cell that names op+target) |
| P5 | Reason-head accuracy and confusion; opaque-rule adherence on block D |
| P6 | Stripped vs with-tool-results view delta on the 300 twins |
| P7 | Flip rate under option permutation with CI |

## 6. Clean-room notes

- Built only from the plan and the stripped permission excerpt. No original generator, template, wording pool, OHS-AC or benchmark item text was opened. Domains (git, Kubernetes-style services, buckets, job schedulers, SQL) are allowed; no benchmark entity name, ID pattern or prompt wording is used (none was visible to me).
- No hand-picked fake names: all repo, host, user, service, branch, path-component, table and policy-card display names come from the seeded TRAINING-salt namespace. Real program names are listed in section 7 because they are tool names, not fake entities.
- bashlex, CARE and AgentTrust code or rules are barred; shlex is never the labeller; mvdan/sh used as parser only.
- Claude Code auto-mode-config is the tier source; the Codex forbidden/prompt analogy is NOT used.
- G13 hit reports for this family carry row ids, target name and method only.
- Writers (Haiku wording pools) get the question forms and slots, never the literal-ban list.

## 7. NAMES this family needs (names only; no strings generated here)

Fixed real names (tool names and generic words; allow-list entries):
- Shell/programs: bash, sh, env, timeout, nohup, command, sudo, xargs, base64, tee, sed, awk, echo, printf, cat, head, tail, sort, wc, ls, find, grep, du, df, ps, kill, pkill, rm, rmdir, cp, mv, ln, mkdir, touch, chmod, chown, tar, gzip, unzip, curl, wget, ssh, scp, rsync, nc.
- VCS/infra/data CLIs: git, gh (gist subcommand only), kubectl, docker, terraform, aws, gcloud, psql, sqlite3, mysql, scancel, squeue.
- Package managers: pip, npm, yarn, cargo, go, apt-get, brew.
- Generic words: main, master, develop, release, hotfix, feature; origin, upstream; hook names pre-commit, pre-push, commit-msg; sensitive stems (`.env`, `.netrc`, `id_` key files, `credentials`, key/token/secret/password words) and the link-local metadata address literal 169.254.169.254.
- Languages: bash and sh as the rendered languages; SQL (statement text only). Runners: NONE (no execution). Validators (tools, not runners): tree-sitter-bash, mvdan/sh parser, sqlglot.
- Carriers (logical ids; rendered tool names follow the C2 product layout, supplied by L-0): `shell_exec` tool call, `file_write` tool call (write-then-run), user turn, tool-output listing (variant view only).
Namespace kinds (counts and rules only, strings produced by the L-0 namespace program into the manifest): policy_card (8), org, repo, branch suffix, path component, user, host (trusted/untrusted), registry host, package, service, context, table, database, env-var stem, bucket. Host TLDs and raw IPs come from the ONE shared host-TLD list and ONE raw-IP pool kept by L-0 in the names-only manifest (G8), used by T50, T51, T53 and T41c alike (reserved TLDs plus a generic list; documentation and private IP ranges; deny-list collision check against real brands and registered names).

## 8. Risks

1. Label ambiguity in soft vs hard assignments (tier source is one docs page): builder may over-assign `hard`. Mitigation: Opus approves the rule table; hard share capped by K10; [FIX-5] the tier-source column and K20 make over-assignment checkable.
2. "Opaque => ASK" can teach "any `$(` or redirect means ASK". Mitigation: resolver list is generous; K3/K6 exclude opaque rows from the format probe, and opaque share is 4%; resolvable substitution rows exist in A/B.
3. Operators leak their own signal (e.g. base64 only on dangerous). Mitigation: K4/K5.
4. Renderer/validator drift (>10% drops) = generator defect, T50 kill (lane rule).
5. Simulated state may not match real git/shell edge cases; gold is policy-correct under the model, not a claim about every shell.
6. Hand-off overlap with T51/T53 (INFERRED-TARGET, EXTERNAL-SHARE) could duplicate; T50 keeps only shell-shaped, unambiguous-data-class versions.
7. Card text rendering is unspecified here; 8 cards must be read, not memorised (K7 swap pairs).

## 9. One fix iteration and kill rule

- One fix iteration after the first failing pre-freeze gate: allowed changes = generator parameters, quotas, operator library, rule-table defects found by Solver B, wording pools; NOT the bars. Re-run all pre-freeze gates. G3: the 1,000-row pilot is the first measured look at every pre-freeze gate; the ONE combined fix after it IS the fix iteration; changing generator parameters after seeing pilot gate numbers and re-running is not allowed. Defects found before the pilot by unit tests, the build skeptic or A/B disagreement on CPU test fixtures are build fixes.
- Kill: any pre-freeze gate still failing after the fix, K1 drop rate > 10% after the fix, or not through all pre-freeze gates by the data freeze (Mon 2 Nov 23:59 UTC) -> family rolls to C2.2/C3 with the failing gate and numbers logged. POST-TRAINING lines are never kill rules. A G13 pilot hit rate > 1% IS the fix iteration (exceptions per plan 2d and 22b).

## 10. Open questions for Opus (ALL RULED 18 Oct 2026; rulings in section 11.4)

- O1 add an 8th reason `unresolved` for opaque ASK, or keep `none` (default: keep, to hold the plan's 7 classes)?
- O2 CRED-SCOUT reason: `cross_trust` (default) or `exfiltrate`?
- O3 v2 carve-outs and no-execution text were outside my scope: please attach them or confirm section 3's minimum.
- O4 confirm G5-H/G3-H/A43(d) count as pre-freeze data-audit gates (not model gates under skeptic 6).
- O5 P2: confirm reporting FNR/precision/false-blocks-per-1,000 beside FPR, since FPR alone does not change under reweighting.

## 11. Fixes (Revision 2, Sun 18 Oct 2026; for the Opus re-check, target Mon 19 Oct)

Source: families/G0_APPROVALS.md, T50 REVISE, must-fix items 1-5, plus its notes and rulings. Edited in place above; each edit carries its [FIX-n] tag. No rows, no code, nothing executed.

### 11.1 Must-fix items

1. [FIX-1] R09 replaced by the shared lane rule SLT-1 (section 3, Shared Tables): agent-created in contained = ALLOW; contained, not agent-created, not authorised = ASK / bypass_review_or_affect_others / soft; shared, not agent-created, not authorised = BLOCK / bypass_review_or_affect_others / soft (ASK when the card has ask_on_soft); production = BLOCK / bypass_review_or_affect_others / soft. Shared = BLOCK soft, not ASK, following the Anthropic default-block group "changing shared resources the agent did not create".
2. [FIX-2] R13's own conditions deleted; R13 = "apply T53's data-class x destination table" (SLT-2). Secret to any host, trusted or not = BLOCK / exfiltrate / hard, except T53's scoped credential-use case; confidential to an untrusted host = BLOCK / soft (ASK under ask_on_soft); public = ALLOW; EXTERNAL-SHARE rows follow this. The state model gained `data_class` on filesystem nodes and an `egress` sub-record on the spec so the shared table has its inputs.
3. [FIX-3] R04's "BLOCK if card strict" clause deleted (option 2 of the two allowed). No `strict` slot is added, so the 8-card schema and the K7 swap pairs are unchanged.
4. [FIX-4] `base64 -d` of a visible literal piped to a shell is RESOLVABLE: decode, then label the decoded registered payload with the state advancing. Only a base64 payload not visible in the session (unknown file, fetched, invisible variable) is opaque and ASK under R19. Added to the renderer line, the opaque rule, the resolver list (B64-LIT) and K3; K18 now counts the decoded payload.
5. [FIX-5] The frozen rule table has a "Tier source" column mapping each rule's soft/hard tier to its auto-mode-config category (hard_deny / soft_deny) or PLANNER CHOICE. The stripped excerpt quotes no entry list, so only R09 (C3, C4), R13 (secret rows) and R17 are tied to a source named in the excerpt, the plan or the Opus ruling; every other tier is marked PLANNER CHOICE and listed in 11.5. K20 checks the column.

### 11.2 Note applied (no re-check needed)

K19: construct-presence check over ALL rows, beside K6. Among rows with an opaque-capable construct, resolvable rows >= 40% and the ASK share <= 60%, so "any `$(` means ASK" cannot be learned (risk 2). I added `base64 -d` into a shell to the construct list, which follows from must-fix 4.

### 11.3 Choices I had to make while applying the items (please confirm in the re-check)

a. `created_by_agent` is true only in a contained lane (both T50 and T51 state models). The ruling gives no label for an agent-created resource in a shared or production lane, and the T51 oracle would give ASK there while "production = BLOCK" gives BLOCK. Removing the cell removes the conflict. If Opus wants those cells, a label must be ruled.
b. The T51 `own-cleanup` card slot is dropped, because the ruling's "agent-created in a contained lane = ALLOW" has no card slot in T50 and G9 requires the same label under the same card. This is also recorded in T51 section 11.
c. SLT-2 clearability: only the confidential-to-untrusted row is clearable by naming (as written in the draft). The soft ASK rows (unknown visibility, transport defect, unlisted MCP server, unnamed publish) are not drawn into consent quads. The draft's tier text said "soft", but gave naming-clears only for that row.
d. The cross-family test uses the consent cells "neither" and "both" only. The partial cells carry the "neither" label by construction inside T50.
e. R14 is narrowed to package INSTALL; package publish is egress and goes to T53 rule 4. The draft's E11 said "install/publish" but R14 had no publish condition.
f. Tier sources: only R09 (C3, C4), R13 (secret) and R17 are source-backed from what I may read; everything else is PLANNER CHOICE (11.5). I did not invent entry ids.

### 11.4 Rulings recorded and global rulings conformed

O1 keep reason `none` for opaque ASK (7 classes). O2 CRED-SCOUT reason = `cross_trust`. O3 the section-3 minimum is the binding no-execution rule (K16). O4 and O5: see G2 (data-audit gates are PRE-FREEZE) and report FNR, flag precision and false blocks per 1,000 beside FPR (P2 already does). Global rulings applied to this file (conformance, not must-fix): G1 Solver B is a program (section 3); G3 no free pilot tuning (section 9); G5 probe protocol, 97.5th-percentile bound, permutation and leak-power checks, GBT advisory (section 5); G6 tokens, 1,024 line (K12); G7 reason and tier as head rows (section 1, K22); G8 shared host-TLD list and raw-IP pool (section 7); G9 shared tables and cross-family test (section 3, K21); G10 `decision_spans` with ROLE per span, and `spoken_view` where it exists, exported by the spec (section 2; a code requirement, not a gate). K10 (balance asserts) has no probe and follows G5/G6 only through K12; I read the ruling's "K10 and K12 follow G5 and G6" that way. If Opus meant a different K10, please say.

### 11.5 Re-check list: rules with no source entry (PLANNER CHOICE tier)

Hard-tier first: R05 (outside roots / system paths), R07 protected-branch force-push, R15 keys for remote login and privilege files. Soft-tier: R02, R04, R06, R07 own-branch part, R08, R09 C2, R10, R11, R12, R13 confidential rows, R14, R15 soft part, R16, R18.

### 11.6 What may start now (unchanged from the verdict)

Spec schema, state model, renderer, expander, validators. Rule-table code waits for the re-check.


## 12. Opus rulings 18 Oct (addendum; copied word for word from families/G0_APPROVALS.md by the L-A builder, Sun 18 Oct 2026)

Where the body text above still says otherwise, this addendum binds (G0_APPROVALS.md "Round 2 hand-off"). The build skeptic checks the code against it.

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

### Round 1 decision (REVISE; the five/three must-fix items are applied above as [FIX-n])

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

### Round 2 decision (APPROVE; binding conditions)

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
