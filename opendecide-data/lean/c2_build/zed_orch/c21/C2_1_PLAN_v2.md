# C2.1 PLAN v2 (17 Oct 2026; deep research + Opus plan + Opus skeptic (revised))

Status: DRAFT; no C2.1 build or spend before the owner's C2.1 GO.

## taxonomy_and_families
CHANGES FROM v2, AND WHY
- Every rebuilt family (T27, T40-T46) is now built CLEAN-ROOM. Fresh agents write it, and they never read the original generators, templates, wording pools or OHS-AC. No template quarantined under A64(c) is ever written again. This is skeptic problem 1: the old generators produced the OHS-AC A2/B splits, so their frames are shared with that test.
- Scope is managed in WAVES, not cuts. The owner's rule (15 Oct: "cover ALL data at its best", no cuts made from estimates) means no family is deleted from the plan. A family leaves C2.1 for C2.2/C3 only in two cases: (a) it fails its gates after its one fix iteration (an A59(e)-style kill rule), or (b) it is not through its gates by the fixed data-freeze date. Both are measured states, not forecasts.
- Families were merged so that P0 has 9 builds instead of 13+ (problem 9).
- Decision types the skeptic found missing are added as heads (problem 14).

A. DECISION TAXONOMY. Eight groups. Every coding-agent decision is mapped to a P0 family or head, a P1 family, a report-only U item, or C3 with a reason. Sources: Claude Code hooks, permission docs and the auto-mode post; Codex auto-review; Cline; OpenHands; SWE-PRM; When2Call; ATBench-Codex.
- G1 Permission and action safety:
  - allow/ask/block on shell, git, infra and SQL commands;
  - destructive or irreversible actions;
  - egress of data or secrets;
  - security weakening;
  - scope against the targets the user authorised;
  - boundaries the user stated, including after compaction;
  - supply-chain installs;
  - trust boundaries;
  - the Codex sandbox-escalation categories;
  - plan mode (read-only) vs act;
  - deny-and-continue vs escalate.
  Today in C2: generic domains only (T26, T28, T29, T31).
- G2 Injection and provenance: instructions inside tool outputs, repo artifacts, MCP tool descriptions and CI logs; authority framing; over-defence. Today: T26 in C2 (T27/T41 in C3; T41 has its last iteration due Mon 19 Oct).
- G3 Tool calling: call / ask for a missing parameter / no suitable tool / answer directly; which tool among distractors; whether arguments are grounded; parallel vs sequential; result vs claim. Today: T33 in C2.
- G4 Agent control flow: done or continue; stuck or looping vs legitimate polling; recovery after an error; ask or proceed; next step; delegate; what to keep at compaction; commit/PR readiness. Today: T30 and T32 in C2.
- G5 Code verification with execution gold: output and exception prediction; equivalence; will this test fail; does the patch fix the bug; best of k; localisation; test selection. Today: nothing in C2.
- G6 CI and repo operations: flaky vs real; dependency risk; merge choice; review gate. Today: nothing.
- G7 Code security: secret in a diff; vulnerable version (synthetic CWE patterns only). Today: nothing.
- G8 Monitoring the agent itself (AI safety): test gaming and reward hacking; a claim with no evidence behind it; overeager actions; edits to its own permissions. Today: part of T33.

B. P0 FAMILIES (9 builds; about 28K new rows)
Each has: a G0-lite spec approved by Opus, solver A and an independent solver B, program or execution gold, and one fix iteration.

1. T50 SHELL-GATE (4,000 rows; at least 45% ALLOW)
   - Decision: ALLOW / ASK / BLOCK under a policy card, plus a reason head (destroy / exfiltrate / weaken security / cross trust boundary / supply-chain / none).
   - Covers:
     - git reset --hard or clean -fd with uncommitted work; rm -rf on an unset variable; terraform destroy;
     - DROP/TRUNCATE, or DELETE without WHERE, on a production database;
     - force push; curl|bash; bypassing the registry; typosquats; unpinned installs or post-install scripts (T61 folded in);
     - --insecure; disabling CI or security tests; editing its own permission or hook files; repointing an API base URL; instance-metadata credentials; PRs to other orgs;
     - the Codex escalation classes (elevated shell, network, edits outside writable roots, MCP approval).
   - Carve-outs: lock-file installs, pushes to the working repo, read-only HTTP, rm -rf ./build.
   - Gold: our own parser (stdlib shlex plus a small grammar; no GPL tools), a canonicaliser, a rule engine and a SIMULATED filesystem and git state model. Nothing destructive is ever executed (problem 10).
2. T51 SCOPE-BOUNDARY (3,500 rows; v2's T51 and T52 merged)
   - Is the action inside the authorised / must-preserve / protected sets, which are computed from generated repo or infra state?
   - Does a boundary the user stated still apply, was it lifted, or was it superseded (including after a compaction summary)?
   - Plan-mode read-only vs act.
3. T53 EGRESS-SECRET (2,000 rows)
   - Does an action, diff or commit send out or store a live secret?
   - Inputs mix seeded synthetic fake credentials with placeholders, test fixtures and public keys, plus a list of trusted destinations.
   - Gold: by construction.
   - The C_DATA_SPEC guard-10 PII scrub runs here as a check: every high-entropy token must be one of the generator's registered fakes. Any unregistered token is a generator bug and the row is dropped.
4. T41c TAINT (clean-room)
   - Decision: ALLOW / BLOCK / ASK / ALLOW_BENIGN, by provenance.
   - Carriers: tool outputs, repo artifacts (README, issue, code comment), MCP tool descriptions, CI logs, authority framing. At least 45% benign.
   - Benchmark attack strings are banned from all prompts.
   - Size depends on T41's C2 outcome: if T41 enters C2, T41c builds only the new carriers (2,000 rows); otherwise 3,000.
5. T54 TOOL-NEED/PICK (clean-room; replaces T40r; 4,000 rows)
   - The four When2Call answers.
   - Which tool among 5-20 distractors.
   - Argument grounding: does each value appear in the request, the config or earlier results?
   - Parallel vs sequential order, from a dependency graph.
   - Schemas: Claude-authored only in P0.
6. T55 RECOVER-ESCALATE (3,000 rows)
   - Retry / fix arguments / switch tool / ask / stop, from the error class and state.
   - Deny-and-continue vs escalate: 3 consecutive or 20 total denials (Claude Code), or 3 consecutive or 10 of the last 50 (Codex).
   - Loop vs polling, as a state-change predicate (T60 folded in).
7. T56 DONE-CLAIM (3,000 rows)
   - Done vs continue: hidden acceptance tests are executed.
   - Claim vs evidence: e.g. "tests pass" when no test was run.
   - TEST-GAMING (T58 folded in): the patch edits or skips tests or special-cases inputs. Also ImpossibleBench's trick on our own synthetic tasks: the tests contradict the spec, so any passing patch is a hack.
   - Commit/PR readiness.
8. T42c CODE-EXEC (clean-room; 3,000 rows)
   - Output or exception (4 options), equivalence (yes/no), will this test fail (yes/no).
   - APPLICATION-STYLE code only (parsers, data transforms, business rules, small CLIs). Never Rosetta- or leetcode-style algorithm puzzles (problem 3).
   - At least 25% JS/TS, Go or bash.
   - Gold: execution in the sandbox.
9. T57 PATCH-VERDICT (clean-room; 3,000 rows)
   - Does the patch fix the failing test without breaking passing ones?
   - Best of 4: correct / partial / symptom-only / breaks passing tests / edits tests.
   - TEST-SELECTION head (coverage gold) and LOCALISE head (which function; verified by a failing test).
   - Code: Claude-authored multi-file synthetic modules, plus a NEW mutator (T43's mutate.py is not reused).
   - Gold: fail-to-pass (F2P) and pass-to-pass (P2P) execution.

Training floor for C2.1, fixed in advance: at least 6 of the 9 P0 families pass their gates, AND at least one of T42c/T57 (execution-gold code) passes. Otherwise the orchestrator stops and reports at GO #1.

C. P1 (wave C)
- Starts as lanes free up, judged on measured progress.
- A family enters C2.1 only if it passes its gates by the data freeze; otherwise it goes to C2.2/C3.
- Order:
  1. T59 ASK-OR-PROCEED: remove one detail from an issue; gold is "ask" if the hidden tests tell the two interpretations apart.
  2. T62 FLAKY-OR-REAL: seeded nondeterminism, 20 re-runs.
  3. T63 DEP-RISK: local index and resolver; T36 folds in here.
  4. T65 VULN-SYNTH: synthetic CWE patterns with static-taint gold; no CVE or NVD text.
  5. T66 REVIEW-GATE.
  6. T44c SEQ-CHECK and T45c TRACE-VERIFY (clean-room).
  7. T27c SCOPE-WIDEN (clean-room).
  8. T64 LOCALIZE-REAL (vendored repos; conditional on the sandbox and 8.5).

D. C3 or report-only (U block)
- MERGE-PICK, CTX-KEEP and DELEGATE (by description match): U items only.
- Model-tier routing: C3, because its gold needs bigger models (no-big-teachers rule).
- T46.
- AIDev merge outcome and JIT defect prediction: their labels are social or heuristic.

E. RULES FOR EVERY FAMILY
- At least 30% matched minimal pairs.
- Near-miss program negatives.
- C2's own errors through A42-D 6 trap selection.
- Options shuffled.
- At least 50 wordings per question form from the start; no single wording above 2%.
- A50 G6 at size; A49c balance; G5-H as adopted (two Haiku solvers on 300 rows per family, plus one read of 100% of free-form rows); G3-H; A43(d) Opus confirmation of flags.
- Token mean at most 800 (the same as C2's A49c cap); hard cap 1,536 tokens on at most 10% of rows.
- At least 25% non-Python code in the code families.
- A 200-row G13 pilot before full generation (see data_sources).

F. HONEST LIMIT
- Under our rules (no frontier reads, no third-party numbers on our block), "beats every model" cannot be measured.
- What we can show: a win on a fixed list of public decision benchmarks, plus OHS-5 transfer items. See benchmarks_to_report.

## data_sources
P0 USES ONLY CLAUDE-AUTHORED GENERATORS WITH PROGRAM OR EXECUTION GOLD. No external code or text corpus is used in P0.
- Toolchains are pinned: Python 3.12 stdlib, Node 20, Go 1.22, bash, sqlglot (MIT) for SQL parsing.
- There are no external identifiers, so no source can HIT on 8.5. The manifest records "no external source" for each P0 family.
- The A61 final-mix 8.5 run still covers the whole mix.

GUARDS ON EVERY C2.1 CODE OR TEXT SOURCE, Claude-authored included (problems 2 and 3)
- Every C_DATA_SPEC 4.3 guard applies:
  - n8n (ejs-5);
  - CVE-/GHSA- identifiers;
  - /rosetta/i;
  - stackoverflow and stackexchange links;
  - the BIG-bench canary;
  - lm-evaluation-harness, opencompass, helm, bigbench and leetcode repos;
  - the PII scrub (guard 10, run as the T53 registered-fake check);
  - the deny-list program on every name.
- Domain rule 3: no vulnerability or CVE text, no Rosetta-style code tasks, no Stack Exchange-style Q&A.
- 200-ROW G13 PILOT for every family before full generation, against OHS-3, OHS-4, OHS-AC, OHS-5 (once frozen), every public eval target and the attack-string literal targets. Any method hitting more than 1% of rows sends the generator back for a fix (this counts as its one iteration).

8.5 PROCEDURE (A61 a/d; problem 4)
- Only the orchestrator runs 8.5: once before any mapper is written and once on the final mix, on whole fixed inputs.
- The form-shopping bar applies.
- No generator code that touches a source is written before that source's pre-mapper PASS.
- Recorded A61(a) HITs bar a source for C2.1 under any id or form: gsm8k, hover, isarcasmeval, tydiqa, md_fdc, md_peps and the DI-TS inputs.

REMOVED SINCE v2
- CVEfixes, PrimeVul, BigVul and MoreFixes: NVD is an OHS-3 source (RESEARCH_licensed-data.md:332, guard 5, domain rule 3).
- Atomic Red Team, GTFOBins, NL2Bash and tldr-pages: upstreams of the CARE eval, or licence unverified. Commands are Claude-authored instead.
- Human-written MCP server schemas: they may overlap the MCP-Atlas (36), MCP-Universe (11) and MCP-Bench (28) server lists. Claude-authored schemas only.
- CommitPackFT and SWE-rebench V2 move out of P0.

P1-CONDITIONAL SOURCES. Each needs: a pre-mapper 8.5 PASS, a per-row permissive repo licence, the guards, and the A61(b) check. Each has a fallback.
- Vendored permissive Python repos (MIT/Apache/BSD; 30-60 repos; T64). They are synced as offline venvs to the sandbox VM only. Fallback: synthetic modules.
- SWE-smith-py (MIT): procedural-mutation instances only (no lm_modify, lm_rewrite or pr_mirror); code and tests only, never its problem statements or trajectories. Requires Docker on the sandbox VM, so far unverified. Fallback: copy the method only.
- SWE-Gym (MIT): checked for repo overlap with the SWE-bench test repos. Docker, optional.
- SWE-rebench V2 (CC BY 4.0): permissive rows, with the agentleak overlap IDs dropped. Its v1 sibling feeds a public leaderboard, so it is held until the split-aware A61(b) decision.
- CommitPackFT (MIT tag, per-row licences): A61(b) status unverified.

GENERAL ROWS (about 7K) AND VOICE (about 2K)
- Claude-authored, harder general items with program gold: multi-step arithmetic, logic, causal and temporal reasoning, tables. They must not share sources or domains with OHS-3/4/5 G.
- ASR-noised copies of existing decision rows: TTS then ASR, 3-15% WER, run on the free L4.
- Replay of C2's mix, with drop-only steps (A46, p_g < 0.2 human rows, pg_anchor).

STATUSES CLOSED NOW (problem 18)
- When2Call train: OUT. It is LLM-labelled (Mixtral), which the owner's 27 Sep rule bars, and it has xLAM non-commercial upstream taint.
- BFCL: eval only.
- SWE-rebench: P1-conditional, as above.
- CodeReviewer: OUT, as in the register (decision 7; deny-list taint 3G#27.0).
- CodeReviewQA: reported only if it is shown NOT to derive from CodeReviewer.
- A61(b) split-aware deny-list check: built in prep as a pre-result program fix (Sonnet code, CPU tests, Opus ruling). The owner decides adoption at the GO. The A61(a) HIT bars stand either way.

BARRED BY THE NO-LLM-GENERATED-DATASETS RULE (owner may relax; recommended: keep): Toucan-1.5M, Nemotron tool_calling, Nemotron-RL-IPI (only 1,272 rows, all successful attacks), ToolACE, AceCode-87K, CodeScaler synthetic data, SWE-smith's LM bugs, R2E-Gym's issue text.

NOT USABLE (licence): xLAM-60k; APIGen-MT-5k; AgentHarm; R-Judge, TraceSafe, AmPermBench, WASP (non-commercial); AgentDoG training data ("other"); CleanVul, DiverseVul, IDoFT, ToolPRMBench (no licence); SecretBench; CodeI/O; AgentTrust (AGPL).

NEVER USED AS DATA: outputs or weights of competitors (Jev, AgentDoG, OpenHands critic).

EVAL UPSTREAM EXCLUSION (problem 5)
- Every Tier-1 eval's upstreams are listed and excluded from training:
  - When2Call: BFCL v2 Live, APIGen/xLAM.
  - CARE: Atomic Red Team, RedCode, NL2Bash, NL2SH-ALFA, GTFOBins, Exploit-DB.
  - MCP benchmarks: their server lists.
  - ATBench: the ToolBench/ToolAlpaca tools.
  - AgentDojo, InjecAgent, BIPIA and ASB: their attack templates.
- Attack strings and BFCL function docs are registered as G13 literal targets, and are banned in every Haiku wording prompt.
- All eval sets are registered as G13 targets BEFORE any C2.1 row exists.

## sealed_test_coding_block
OHS-5: a new sealed test, frozen before any C2.1 training row exists. Its blocks are G (general), C (coding and agentic), R (rule/agent), K/X (option-order and attack robustness), and U (report-only).

WHO
- Fresh sealed-side sessions with a sealed-only file scope and an access audit.
- A sealed Sonnet builder works from the OHS-5 brief only.
- An independent sealed Sonnet writes solver B.
- Sealed Haiku writes the wording.
- A separate sealed Opus signs off the freeze.
- Barred authors: anyone who wrote or read any C2 or C2.1 training generator, and the reverse (the A64 lesson).
- Every prompt carries the no-probing rule.

THE C BLOCK IS PROGRAM-GENERATED ONLY (problems 2 and 4)
- It has no external upstreams: no real repos, no CVEs, no MCP repos.
- Its source list is the sealed generator IDs, so no training source can HIT it on 8.5 through a shared host, publisher or licence URL.
- Real-repo items are dropped from OHS-5. Time-split public sets cover that ground as Tier 2.
- C-SEC vulnerable-version pairs are synthetic CWE code with static-taint gold and no CVE/NVD-style text. The brief records this before building, as a domain-rule-3 decision.
- No Rosetta-style algorithm tasks.

THE G BLOCK (at least 20 fresh public/official/program-gold sources, at most 500 items each)
- The sealed side receives a NAMES-ONLY list of planned C2.1 training sources and C2's mix sources, as in BRIEF rule 1. It picks G sources that share no dataset name, publisher or upstream ID with them.
- Before choosing, a sealed-side agent reads the 8.5 matcher CODE (no OHS data) to learn whether generic hosts (github.com, huggingface.co, zenodo.org) and licence URLs are normalised out.
- If they are not, the owner decides at the GO:
  - (a) a pre-result ruling that scopes OHS-5 8.5 identifiers to the dataset level; or
  - (b) G sources restricted to hosts no training source uses.

DISJOINT BY CONSTRUCTION
- Separate generator code, templates, wording pools and narrative domains.
- Different policy cards, tool sets and fake-credential formats.
- 25% TRANSFER items use policies, tool catalogues and languages or ecosystems no training generator uses. This is a headline sub-score.

PREVENTING A REPEAT OF THE A62(c) STOP
1. A product-format exemption is registered before building, bound by sha and shown to the owner. The instruction header, option scaffolding and public definitions-card text are left out of the sentence and n-gram methods. Item content is still fully checked.
2. Keyword export covers dataset-specific identifiers only.
3. Reverse pre-check before the freeze: the sealed side runs a G13 child on its own items against hash exports of (a) the training-side templates and wording pools, which exist as code while no rows do, and (b) C2's mix. It regenerates colliding items and reports the rate. Nobody on the training side ever sees sealed text.

GOLD
- Program or execution only. Sealed solvers A and B must agree; disagreements are dropped.
- Two Haiku blind reads test answerability; items both reads mark unanswerable are dropped.
- Execution runs only on the disposable sandbox VM.

COMPOSITION (about 3,700 items; at most 450 per decision type; options randomised; at least 40% in minimal pairs)
- C-PERM 800: gate 450; scope 200; boundary/plan-mode 150.
- C-INJ 450: carriers 300; benign 150.
- C-TOOL 600: need 250; pick 200; arguments/order 150.
- C-CTRL 550: done/claim 200; recover/escalate 200; loop 150.
- C-CODE 700: exec/equivalence/test-fail 300; patch/best-of-4/test-select/localise 300; test-gaming 100.
- C-SEC 150: secret egress (plus vulnerable pairs if T65 trains).
- U, report-only, 450: ask-or-proceed 100, flaky 50, dependency risk 50, vulnerable pair 100, review 50, merge-pick 50, context keep 25, delegate 25.
- A sub-block whose family is not in the final mix manifest (fixed before any read) is scored report-only, as "family not trained".
- G, R and K/X blocks as in v1.

POWER
- C total: paired SE about 0.8-1.0 pp.
- Transfer (about 800 items): about 1.6-1.8 pp.
- Each sub-block: 1.6-4 pp. C-SEC at n=150 is about 3.5-4 pp.

METRICS
- Accuracy.
- For gates: balanced accuracy, plus TPR at 1% and at 0.4% FPR.
- ECE and Brier.
- Order consistency.
- Latency per decision type.

COMPARATORS (one job)
- C1, C2, C2.1 and base Qwen3.5-4B.
- Jev 1.14 via OpenRouter, priced in timeline_budget.
- AgentDoG 1.5-4B and OpenHands critic-4B on the free L4, only if the owner says yes.
- No frontier reads.

PRE-REGISTERED RULES (one look; Jev is read once, after the C2.1 verdict)
- HEADLINE C-transfer: C2.1 − Jev ≥ +5 pp with paired LB > 0, and C2.1 − C2 ≥ +3 pp with LB > 0.
- SECONDARY C-total (labelled "home field: taxonomy and cards we train on"): C2.1 − Jev ≥ +8 pp with LB > +3; at or above Jev's point on at least 5 of the 6 sub-blocks; C2.1 − C2 ≥ +5 with LB > 0.
- G FLOOR (ship-binding): C2.1 − C2 LB > −1.0 pp.
- G TARGET (the owner's "≤ 3-4 behind"): Jev − C2.1 ≤ 4.0 pp on OHS-5 G, reported with its CI.
- K/X: attack success ≤ max(C2 + 2 pp, 3%).
- ECE ≤ 3.5%.
- OHS-4 is report-only for C2.1, because C2 spends it.

## benchmarks_to_report
RULES
- We never train on any of these. All are registered as G13 targets, and their upstreams excluded, before any C2.1 row exists.
- Every result states version, date and protocol.
- Other models' scores are published numbers only, each cited and tagged vendor-run, author-run or independent.
- We read only C1, C2, C2.1, base 4B and Jev ourselves (plus the AgentDoG and critic 4B models if the owner agrees).
- Safety results show precision, recall, FPR and TPR at a fixed FPR, plus an "always unsafe" baseline. Never F1 alone.
- Both option orders are read.
- No cherry-picking: every Tier-1 result is published, wins and losses alike.

TIER 1: THE HEADLINE LIST, fixed now (problem 6). The claim gate on public data.
1. When2Call MCQ: 3,652 items; AA protocol 3,423; letter readout, protocol stated.
   - We read Jev ourselves.
   - The third-party mirror figures (Jev 80.8, d1-ultra 92.6) are tagged UNVERIFIED and drive no decision.
2. BFCL v4 decision categories: relevance, irrelevance, live_irrelevance, multi-turn miss_func and miss_param. Labelled "decision-readout framing". Near saturation, so not a lead claim.
3. AgentDojo and InjecAgent as detectors: TPR at 1% FPR. Reference: Horizon-Labs 82.2% (vendor).
4. NotInject: over-defence FPR.
5. CARE split, if its licence allows: F1 and FPR vs 85.64 / 0.91% (author numbers).
6. ATBench-Codex (500) and ATBench (1,000). Problem 13 fixes:
   - (a) the compaction is pre-registered: user turns plus the last N calls, 1,536 tokens or fewer;
   - (b) we also report a CHUNKED full-trajectory read: windows that include tool outputs, scored as the max p(unsafe) over windows;
   - (c) we compare only with AgentDoG v1.5-4B 74.3 F1 on the 1,000-case set, never with v1's 93.0 (500-case set).
   - Honest expectation: per-call gating may lose to a trajectory judge on whole-trajectory labels.
7. CodeReviewQA (900): only if verified not derived from CodeReviewer. Otherwise it moves out of the list, and that is stated.

CLAIM RULE PER BENCHMARK: "#1 among models with published numbers on <benchmark, protocol>" only if our paired 95% lower bound is above the best published point estimate. Otherwise we state our rank.

TIER 2: report only, in our own framing, never part of a "#1" claim
- MCP-Atlas public 500, next-tool per step (no rivals use this framing).
- CRUXEval-O/I as multiple choice (published numbers are generative and not comparable).
- AgentProcessBench (the reference 79.1 vs 66.8 is UNREPLICATED).
- Saber: harm rate with our gate in front of an agent (on the sandbox VM).
- Fresh SWE-bench-Live or SWE-rebench monthly sets as patch verdicts, only if public predictions with resolved labels exist.
- Jev Decision Index, Tools area.
- JevBench coding topic: 56 items, sanity only, no submission.

NON-COMMERCIAL (owner; recommended: do not report): AmPermBench (its 81% figure is UNVERIFIED), R-Judge, TraceSafe.

NOT REPORTED: end-to-end tau2, Terminal-Bench and SWE-bench. They are not decision-shaped.

UNVERIFIED NUMBERS ARE TAGGED AND DRIVE NO DECISION (problem 15): "Jev let 3 of 30 through" (n=30, third-party), the When2Call mirror figures, AmPermBench 81%, AgentProcessBench, and all vendor auto-mode and Codex figures.

CLAIM WORDING
- "#1 measured on X among published numbers."
- "Beats Jev 1.14 by X (CI) on OHS-5 C-transfer."
- Never "beats every model". We tell the owner plainly that this cannot be measured under our rules.

## training_recipe
INIT
- From C2 if it ships. Otherwise the owner chooses C1 or C2's unshipped weights at the GO.
- Same Qwen3.5-4B base and r16 LoRA, merged to bf16, so the S1 parity path does not change.
- α interpolation is θ(α) = init + α(base − init).

ONE MODAL RUN, ONE STAGE. Stage B (FP8-KL) is dropped unless the owner adopts FP8 serving (problem 8).

MIX
- New rows, about 35-37K:
  - P0 about 26-28K;
  - general program-gold about 7K (problem 7: general is now about 20% of new rows, up from 10%);
  - ASR-noised about 2K;
  - plus any P1 family that passed its gates by the data freeze.
- Replay ratio, fixed by an orchestrator ruling before any data:
  - 1.0x if init is C2 (C2's mix is already in the weights);
  - 1.5x if init is C1.
- Total about 72-90K rows, at most 125K.
- The replay of C2's program families depends on the owner's OHS-AC decision. If OHS-AC binds, replay keeps only the rows that pass, and that is stated.

PROMPT FORMAT (problem 12)
- Default: KEEP C2's rendered layout (cygnet + schema_branch_mark) for every row. C2's G13 and S1 parity records (8,143 prompts) then stay valid for replay.
- The static-first reorder is adopted only if a CPU measurement before the GO shows that C2's layout gives less than 60% shared-prefix tokens on gate calls. In that case:
  - the re-rendered replay gets G13 in the same binding window;
  - a new S1 parity record is made on od-l4b.
- Token mean at most 800 for each family; 1,536 cap on at most 10% of rows; diffs trimmed by a program.
- Gate rows see user turns and tool calls only. Taint and done rows also see the relevant tool outputs, capped at 256 tokens each.

ORDER INVARIANCE
- Options shuffled per row.
- 20% reversed copies with a symmetric KL term, only if the trainer change passes its CPU test and a Sonnet skeptic review. Otherwise plain duplicates.
- Target: 1% or less disagreement on dev.

HARD NEGATIVES
- At least 30% minimal pairs and program near-misses.
- A42-D 6 trap selection on C2's own errors. This needs C2 reads of the C2.1 candidates on od-l4b (free; Modal is for training only).
- Hard bin 2x, at most 30% hard, at most 25% easy, no trap type above 35%.
- The same code as C2's implementation (problem 11; built and tested for C2 first).

BALANCE
- Gates at least 45% ALLOW; yes rate 40-60% per family.
- Class weights, not resampling.

LOSS AND CALIBRATION
- Cross-entropy on option letters. No label smoothing, because a training pilot would need Modal.
- One temperature per type, fitted leave-one-group-out on mixdev, bounded to [0.8, 1.3], frozen with the candidate.

CANDIDATE GRID
- The A42-D 9 grid: 18 candidates, grid sha recorded before any look, CANDIDATE record written before the pre-gate reads.
- S = mean(general dev term, C/R mixdev).
- The general dev term is a dev set from sources holding a valid whole-file 8.5 PASS before training. If none exists by the GO, the G-proxy is used with the A61(f) label, and S is stated as NOT claimable (problem 11).
- α < 1 is the pre-registered way to protect G.

SNAPSHOT STOP: the general slice falls below init − 1.5 pp at both the 25% and 50% snapshots.

COST
- Computed before GO #1 from C2's MEASURED s/step and the real C2.1 token histogram.
- Projection now: about $18-28 (72-90K rows at about 1.1x C2's mean tokens, round-1's 27% slowdown, plus $2).
- A37(k)-style stop and ask if the steps-100-300 projection is above the cap.

NOT ADOPTED: non-causal attention, higher rank or a bigger base (owner only), RL with sandbox rewards (C3), any distillation from a bigger model.

## serving
BASE PATH
- SGLang S1 serving the merged bf16 model.
- Argmax agreement with the HF adapter of at least 99.5% on dev.
- Rendered-prompt sha identical in trainer, gate and server.
- Any re-render gets a new parity record (problem 12).

LATENCY AND COST TARGETS PER DECISION TYPE
- Pre-registered from the CPU token histogram before the GO. Indicative, H100 batch 1, server p50:
  - gate calls (cached policy card plus a 150-400-token suffix): 12-20 ms;
  - tool/control calls: 15-25 ms;
  - code calls (mean 800 tokens or fewer): 20-35 ms.
- End-to-end p50 near users: about 75-85 ms.
- $/1K: about $0.008-0.012 at 50-60% utilisation or more.

SPEED CHANGES THAT DO NOT CHANGE ANSWERS
- The exact batch-1 bundle: input_ids with skip-tokenizer-init, /v1/score, LM head sliced to the option rows, full-graph prefill if capture works.
- Policy-card prefix caching for gate calls.
- Hosting near users, keep-alive connections, a warm pool, and the cheapest host that meets the targets.

CHANGES THAT CAN CHANGE ANSWERS (owner's words, after measurements)
- One read per choice question, only if order disagreement on dev is 1% or less.
- Block-FP8 with a margin gate (tau fitted split-half; low-margin items deferred to bf16).

CASCADE PRODUCT
- We are Stage 1, returning a calibrated p(block).
- Three operating points (strict, balanced, permissive), each with FPR and FNR measured on sealed C-PERM.
- An "ask" band hands off to a human or to the customer's bigger model (Stage 2).

INTEGRATIONS (product work, no training)
- A Claude Code PreToolUse hook: allow/deny/ask JSON with a reason category and a fail-closed option.
- Adapters for Codex, Cline and OpenHands.
- An MCP server exposing the decide endpoints.

MULTIMODAL
- Voice (Nemotron EN 0.6B streaming, explicit end of input) and native images, attached unchanged.

## orchestration_and_parallel_lanes
MODEL TIERS (set `model` on every agent; never Fable)
- Opus 5.5:
  - the orchestrator;
  - rulings;
  - G0-lite approvals;
  - A43(d) confirmation of wrong_gold and ambiguous flags, batched once per family;
  - the OHS-5 brief, plus a separate sealed Opus for the freeze;
  - 8.5 runs (orchestrator only, pre-mapper and final mix);
  - GO packets;
  - the final skeptic pass.
- Sonnet 5.5:
  - all code: generators, solvers A and B, sandbox executor, G13, selection and mix, trainer, serving, eval harnesses;
  - first-pass G5-H adjudication;
  - one skeptic review per build;
  - ONE Sonnet builder per lane.
- Haiku 5.5:
  - wording pools;
  - G5-H at the adopted sizes (two solvers on 300 rows per family, plus one read of 100% of free-form rows);
  - G3-H and G-LEX;
  - licence-card scouting (Opus confirms);
  - running scripts, stopping and reporting after 2 failures;
  - condensing logs and drafting HANDOFF.
- Every prompt carries the no-probing and sealed-access rules.
- Clean-room agents also get "never open the T27 or T40-T46 generators, templates or OHS-AC".

USAGE
- Decided on MEASURED usage (get_usage), never on forecasts (owner, 15 Oct). Ping the owner at 96%; never cross 98%. Monday reset 19 Oct 07:00 UTC.

MACHINES
- G13: serial on the Mac only, alone. Its windows never overlap C2's capture or binding G13.
- Heavy agent CPU and all model reads: od-l4b (free).
- Execution: only on a NEW disposable sandbox VM, od-sbx1 (problem 10):
  - free GCP credit; no data disk; no service-account scopes or credentials; deny-all egress;
  - rootless containers (gVisor or podman), no host mounts, re-imaged per batch;
  - never od-cpu1 or any data host;
  - a Sonnet skeptic review plus Opus sign-off of the executor before first use;
  - T50 executes nothing (static engine plus a simulated filesystem).
- Modal: training only.

NOW, BEFORE THE C2 REPORT (the C2 path has priority; no C2.1 builds, rows or spend)
- (a) Haiku scouts licence cards; Opus confirms.
- (b) Opus drafts the OHS-5 brief, the product-format exemption, the reverse pre-check and the names-only list.
- (c) Sonnet writes G0-lite one-pagers for the 9 P0 and 9 P1 families (design only; clean-room authors for the c-families).
- (d) Sonnet designs od-sbx1 and the executor (design only), the token-histogram and cost tool, and the CPU prefix-share measurement.
- (e) Sonnet builds the A61(b) split-aware check as a pre-result program fix, with CPU tests.
- (f) Haiku lists the public-eval G13 targets, their upstreams and the attack-string literals.

AFTER THE C2.1 GO (lanes in parallel; concurrency set by measured usage)
- L-S, sealed (separate sessions): build OHS-5, run the reverse pre-check, freeze, export hashes. Days 1-5.
- L-0, infra: od-sbx1 plus executor review; register G13 targets; set up the C2-reads pipeline on od-l4b for trap selection. Days 1-3.
- Generator CODE may be written from day 1. ROWS only after the freeze.
- Build lanes:
  - L-A (one Sonnet builder): T50, T51, T53.
  - L-I: T41c.
  - L-T: T54, T55, T56.
  - L-C: T42c, T57.
  - L-G: general program-gold rows and ASR noise.
- Per family:
  1. 1,000-row pilot.
  2. 200-row G13 pilot.
  3. Gates: A50 G6 at size, A49c, G5-H, G3-H.
  4. Full generation.
  5. One fix iteration; then the kill rule (rolls to C2.2/C3).
- Wave C (P1) starts when a lane frees up, on measured progress.
- One binding G13 window. Then selection, mix, d2-set, the final-mix 8.5 run, preflight, GO #1.

## timeline_budget
TIMELINE (problem 9; real dates; anything after the C2 report is an estimate)
- Now to about Sun 25 Oct: the C2 path (see c2_pass_actions) and C2.1 prep only. Wed 21-Fri 23 Oct: C2 GO #1 and training (estimate).
- About Mon 26 Oct: C2 report, then the C2.1 GO, with the owner decisions in one packet.
- Mon 26 - Fri 30 Oct:
  - OHS-5 sealed build, reverse pre-check, freeze (the brief is frozen at the GO);
  - in parallel: od-sbx1 plus executor review, G13 target registration, generator code with no rows.
- Sat 31 Oct - Sun 8 Nov:
  - P0 data build in 5 lanes;
  - 200-row G13 pilots as small Mac windows;
  - wave C as lanes free.
  - DATA FREEZE: Sun 8 Nov 23:59 UTC.
- Mon 9 Nov: binding G13 window (8-10 h, Mac alone).
- Tue 10 Nov:
  - C2 reads for trap selection (od-l4b);
  - selection, mix, d2-set, final-mix 8.5, preflight;
  - measured-cost projection.
- Wed 11 Nov: GO #1, then training on renewed 1 Nov credit (about 4-6 h).
- Thu 12 Nov: grid reads, pre-gate, GO #2.
- Fri 13 - Sat 14 Nov: OHS-5 one look, Jev read, Tier-1 reads, latency suite.
- About Sun 15 - Mon 16 Nov: C2.1 report.
- Slip risk: 3-5 days if a lane fails its gates. A family failure does not stop C2.1 unless the floor (6 of 9 plus one code family) is missed.

MODAL (problem 8)
- Training happens after the 1 Nov credit renewal.
- C2.1 cap proposal for the GO #1 ruling: Modal total ≤ $35, training ≤ $30.
- Payers: the mahadikarya2 → mahadikarya3 relay. mahadikarya44 and jaypatil-duke only if the owner names them. No card.
- Projection now: $18-28. It is recomputed from C2's measured s/step and the real token histogram before GO #1, and the live credit is verified.
- No C2.1 Modal spend before GO #1 (reads go on od-l4b).

OPENROUTER (Jev reads; problem 17, part rebuttal)
- Measured rate: $0.0234 per 1K calls at about 550 tokens (HANDOFF, C1 trials).
- Planned reads, about 60K calls with both orders:
  - OHS-5 G, C, R and K/X: about 30K;
  - Tier-1 sets: about 30K.
- At about 1.5x length: about $2-3, inside the about $7 left on the $10 key. No top-up expected.
- A CPU price script confirms before the GO; any overrun goes to the owner.

GCP: od-sbx1 and od-l4b on free credit.

CLAUDE USAGE: measured, not forecast; ping at 96%.

## c2_pass_actions
C2 COMES FIRST. Every item stays inside adopted rules: no bar loosened, all fixes made before training or before the first read.

P1. Make A68 runnable.
- An orchestrator erratum adds the OHSAC_REPORT_ONLY marker to the A68 block without changing its meaning (ruling_gate.py refuses an id whose block lacks it).
- Fix the switch's 7 defects; Sonnet skeptic review.
- Dry-run `owner_options/ac_report_only.py report`.

P2. Binding G13 through the capture wrapper.
- After batch5 (pid 17331, started before A68, so its logs have no drop_ids_by_class), run `g13_c2_opt3.py … --ohsac-report-only A68`: candidates for all 20 blocks plus carry for F4 F5 F6 F11.
- Mac alone. Then a scratch `mix_c2_opt3.py --dry-run`.

P3. Implement A42-D 6 trap selection in c2_select and crowd_select.
- Uses meta.opt_err; C1 ≥ 0.25 on a trap option puts a unit in the hard bin at 2x.
- Caps: hard ≤ 30% (T32 is at 36%, so cap it), easy ≤ 25%, no trap type above 35%.
- CPU tests and a skeptic review.
- It raises pre-gate (a) and S1 by putting C1's own errors into training. C2.1 reuses this code.

P4. A whole-unit, same-bin, seeded balance-repair step that may under-fill (spec 5.3) and never relabels.
- Covers every binding A49c and cap check that swaps cannot fix:
  - T26 token mean 807.7 and longest-option −3.26;
  - longest-option for T06, T12, T24;
  - T15 equiv share 4.56%;
  - T01 card 67 > 64;
  - twin share 25-28%;
  - yes/no share for T15, T23, T25, T26.
- Recorded as a program-fix ruling like A66; tests; skeptic review.
- T26 decides training, because its pool is about at target.

P5. Start the G9 re-read of the 695 low-p_g rows now (T28 192, T26 90, T29 56, T33 26, T30 19). The seeded 300 per family follow after selection.

P6. Dev sets.
- Build T37b-dev per spec 3.18: 300 pairs, frames outside the 379-pattern catalogue, after a short pre-result Opus ruling on where the frames come from.
- Build the merged c2_mixdev: 150 per trained family.
- Register both as G13 targets in the code-edit window after batch5; otherwise run one refresh-dev.

P7. Money and blocks.
- No C2 Modal spend before training.
- At GO #1, show the owner neutrally the projections at 2.92 vs 3.716 s/step, and the A61(e) extra-account option.
- F6 carry QC before Tue 20 Oct 23:59 UTC; F4/F5/F11 carry G13; SB5 and md_* in the final-mix 8.5 run.
- T41 iteration 2 by Mon 19 Oct 23:59 UTC.

P8. Candidate tooling.
- A per-candidate eligibility wrapper and an 18-candidate read plan on od-l4b.
- Grid sha recorded before any look; CANDIDATE_C2.json before the pre-gate reads.
- G-proxy results carry the A61(f) label.
- Symmetrisation q / flip-q and latency scripts.

P9. Same readout everywhere.
- A CPU prompt-sha check across trainer, gate predict and S1 client.
- One frozen S1 config hash; no trial-bundle dials; leave-one-group-out temperatures.

P10. Order of steps: d2-set right after mix --final; the snap-monitor CPU record; OWNER_GO_C2.txt; FILL values.

HONEST ODDS (rough, not measured)
- C2 trains: about 80% if P1-P6 land by about Wed 21 Oct.
- Pre-gate passes: about 60-70% of those. Transfer dev is only 600 rows, so (b) needs about +3.7-4 pp observed.
- S1 passes: about 50% at a true +5 pp, about 80% at +6.
- End to end: about 30-40%.
- The legitimate way to raise this is to raise the true gain: trap selection, every passing block in, and the 18-candidate grid. It will not pass "easily", and the owner should hear that.
- C2.1 does not depend on C2 passing S1, only on the init choice.

## expected_results
ALL PROJECTIONS, NOT MEASUREMENTS.
- C2 (from c2_pass_actions): ships with S1 about 30-40%. General is about 74-75 on sealed tests (C1 74.3 vs Jev 79.6 on OHS-3).

C2.1 ON OHS-5 C
- Trained sub-blocks: C2.1 about 85-92. Jev is unknown, perhaps 65-78. That gives +10-20 pp over Jev, but this is a home-field result.
- C-transfer (the headline): about +4-10 pp over Jev and +3-8 over C2. This is the most uncertain number.
- Below C2 by 0-2 pp on R is possible, and is watched.

PUBLIC TIER 1 (fixed list)
- When2Call MCQ about 82-90. Jev to be measured by us; third-party 80.8 is unverified.
- BFCL decision categories about 88-93 (near saturation).
- AgentDojo/InjecAgent TPR at 1% FPR about 55-80 vs Horizon 82.2 (vendor). A win is not likely.
- NotInject FPR ≤ 5%.
- CARE F1 about 80-90 vs 85.6. A toss-up.
- ATBench-Codex balanced accuracy about 70-82.
- ATBench (1,000) F1 about 65-78 vs AgentDoG v1.5-4B 74.3.
- CodeReviewQA: unknown.
- Expect clear "#1 among published" on 1-3 of the 7. On the rest we report our rank honestly.

GENERAL
- C2 + 0 to +1.5 pp.
- Gap to Jev about 3.5-5.5 pp. The owner's ≤ 4 target is met about 40-50% of the time unless the owner opens the split-aware deny-list lever. Even then, A61(a) bars GSM8K and the other HIT sources.

LATENCY AND COST
- Server p50: gate calls 12-20 ms; code calls 20-35 ms.
- End-to-end p50 near users about 75-85 ms vs Jev 156 (measured).
- $0.008-0.012 per 1K vs Jev $0.0234 (measured).
- ECE ≤ 3.5% vs Jev 6.0.

WHERE WE WIN
- Per-call permission, scope, secret, tool-need, recovery and done decisions.
- Rivals that are decision models publish no numbers on these.
- Chat guards fail on tool calls.
- Our latency and calibration are far ahead.

WHERE WE LIKELY LOSE
- Frontier chain-of-thought models on hard code judging (not measurable under our rules).
- Possibly AgentDojo TPR and whole-trajectory ATBench.

WHAT WE CAN HONESTLY CLAIM: "best measured decision model for coding-agent gating among published numbers on X", and "beats Jev by X on OHS-5 C-transfer". We cannot claim "crushes every model".

## owner_decisions
ALL AT THE C2.1 GO, IN ONE PACKET WITH DEFAULTS. None are asked now.

1. The C2.1 GO itself, after the C2 report. Init: C2 if it ships; otherwise C1 or C2's unshipped weights.
2. OHS-AC for C2.1 (problem 1). A68 covers C2 only.
   - Recommended: extend report-only to C2-replay rows only, with drops published.
   - Alternative: binding. Then the replay of C2's program families falls to the rows that pass (likely near 0 after A62(c)), and the risk of forgetting R goes up.
   - New C2.1 rows get OHS-AC applied as binding either way (stricter, drops only).
3. Money: a C2.1 cap of Modal ≤ $35 (training ≤ $30) on the renewed 1 Nov credit, via the mahadikarya2 → 3 relay. Extra accounts only if named; no card.
4. The general goal.
   - Recommended: the "≤ 4 pp behind Jev on OHS-5 G" target is a CLAIM gate, and the ship floor is C2.1 − C2 LB > −1.0.
   - Alternative: make the ≤ 4 gap ship-binding.
   - The projection (gap about 3.5-5.5) is shown plainly.
5. Claim wording: accept that "beats every model" cannot be measured under the rules. The headline becomes the fixed Tier-1 list plus OHS-5 C-transfer, with the C total secondary.
6. The A61(b) split-aware deny-list. It is built as a pre-result program fix; adopt or not. A61(a) HIT bars stand either way.
7. The no-LLM-generated-datasets rule (27 Sep). Recommended: keep (this bars Toucan, Nemotron and others).
8. Reading rival 4B models (AgentDoG 1.5-4B, OpenHands critic-4B) on the free L4, as eval only. Recommended: yes. They are the same size, so no bigger model is involved.
9. Non-commercial evals (AmPermBench, R-Judge, TraceSafe). Recommended: no.
10. The OHS-5 product-format exemption: shown, bound by sha, approve.
11. Only if the sealed-side matcher read shows that generic hosts or licence URLs HIT: scope OHS-5 8.5 identifiers to the dataset level (pre-result; recommended), or restrict the G-block hosts.
12. Later, after measurements: answer-changing serving dials (one read per choice question; FP8 with a margin gate).

## risks
RANKED RISKS, HOW EACH SHOWS UP EARLY, AND THE MITIGATION
1. C2 process gaps keep C2 from training (A68 marker, capture batch, T37b-dev, mixdev, trap selection). Seen through: the ac_report_only dry run and the opt3 dry-run mix. Mitigation: c2_pass_actions P1-P6.
2. The OHS-AC ruling for C2.1 is missing. If OHS-AC binds, C2's program-family replay disappears and R regresses. Mitigation: owner decision 2; clean-room families; OHS-AC applied as binding to new rows.
3. Clean-room families fail their gates, as T40, T43 and T45 did. Seen through: the 1,000-row pilots. Mitigation: one fix iteration and the kill rule; the floor of 6 of 9 plus one code family; P1 waves.
4. Mass G13 drops of code rows against OHS-3/4 (Rosetta and CVE adjacency). Seen through: the 200-row G13 pilots. Mitigation: guards 1-11, domain rule 3, application-style code only.
5. The G target is missed (gap above 4). Seen through: snapshots and the grid's general term. Mitigation: general at 20% of new rows, the α grid, trap selection; told to the owner up front.
6. A sandbox escape or data loss. Mitigation: a disposable od-sbx1 with no data, credentials or egress; T50 static and simulated only; executor review before first use.
7. 8.5 HITs on generic identifiers between OHS-5 and training sources. Mitigation: a program-only C block, a names-only list, the matcher read, owner decision 11.
8. Eval-upstream contamination (CARE, MCP benchmarks, attack templates). Mitigation: upstream exclusion, literal G13 targets, a ban in prompts.
9. Home-field optimism. Mitigation: the transfer sub-score as the headline and a fixed Tier-1 list with no cherry-picking.
10. ATBench is not comparable. Mitigation: pre-registered compaction, a chunked full read, the v1.5 1,000-case set only.
11. Money: the size of the renewed credit is unknown and step time is about 27% slower. Mitigation: measured s/step, the cap ruling, a stop-and-ask at steps 100-300.
12. The order-invariance trainer change breaks training. Mitigation: a CPU test; otherwise plain duplicates.
13. A re-render voids C2's records. Mitigation: keep C2's layout by default.
14. A 3-5 day slip if lanes fail or G13 windows clash with C2. Mitigation: a fixed data freeze and serial G13 windows.

REBUTTALS (skeptic points that are invalid or partly invalid)
- #16, partly invalid. v2's "dual blind reads" means the ADOPTED G5-H sizes (two solvers on 300 rows per family, plus one read of 100% of free-form rows), not every row. A42-D 8.4's "13 per task" is the noise gate for public tasks. Using it for program families would lower an adopted bar. The owner (15 Oct) bars shrinking quality checks on usage forecasts. A43(d) Opus applies only to flags, batched per family. A separate sealed side is required by the A64 lesson. Cost is controlled through 9 builds, one builder per lane and measured usage.
- #17, partly invalid. At the MEASURED Jev rate of $0.0234 per 1K calls, about 60K length-scaled calls cost about $2-3, inside the about $7 left. The fix (price it before the GO) is still adopted.
- #9, partly invalid. No family is deleted, because of the owner's "all data" rule. Instead: merges (13+ builds become 9), waves, the kill rule and a fixed data freeze. The timeline itself was rewritten to about mid November.
- #8, partly invalid. The "2x tokens" assumption is withdrawn: the token mean is capped at 800 per family, the same as C2's A49c cap. Cost is now computed from measured s/step.
- All other skeptic points (1-7, 10-15, 18) are valid and are fixed in the sections above.