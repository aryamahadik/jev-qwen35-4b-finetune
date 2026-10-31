CONFIRMED (Opus, 18 Oct) - with the corrections listed in "Opus review, 18 Oct" at the end. Still not frozen; the registry sha is computed only after L-E fills the K2 versions/URLs.

# G13 TARGET REGISTRY DRAFT (L-0 day-1 task 1)

Date: Sun 18 Oct 2026 (UTC). Status: DRAFT, for Opus confirmation (L-0 day-1 task 1). Not frozen. The registry sha is not computed yet.
Scope: names and sources only. No item text, no attack strings, no function bodies, no rows are written or read here.
Compiled by: Haiku 5.5 (medium), from the training-side plan only.

Read scope used:
- PLAN_TRAINING_SIDE.md section 2 (data_sources, incl. EVAL UPSTREAM EXCLUSION).
- Plan section 4 (benchmarks_to_report) via LANE_L-E.md lines 1-97 only, as the task names. The L-E block (lane lines 155 onward) was not opened.
- LANE_L-0.md (day-1 task 1 and output (d)).
Not opened: any ohs/sealed path, C2_1_PLAN_v3.md, the SKEPTIC file, OHS5 draft, research_v3, generators, templates, excerpts (none exist yet).

Role of each section (Opus, 18 Oct): G13 match targets are sections A, B, C, D, G, H and M (plan section 2: OHS-3, OHS-4, OHS-AC, OHS-5 once frozen, every public eval target, the eval-upstream exclusions and the attack-string literals). Section E is a SOURCE BAR (enforced by the names-only manifest and the row-start allow-list, and by 8.5/A61 for E65-E71), not a G13 content target, except where an E entry is also listed in A-D. Section F is the C_DATA_SPEC 4.3 guard set applied to every source. Section J is listed only for the exclusion check of candidate sources.
Literal-ban content is never written into this file: the literal-ban list is enforced inside G13 and never shown to writers; any G13 hit report shown to a builder carries row ids, target name and method only, never the matched text (plan section 2 / build order, v3.1 skeptic 8).

Conventions: "not stated" means the plan sections 2 and 4 give no version, licence or URL. L-E must fill those from the official release before any G13 pull. No URL in this file was invented.

---

## A. Public eval sets, Tier 1 (claim-gate, plan section 4 list 1-6)

| ID | Name | Version | Licence status | Data source (as the plan gives it) | Notes |
|---|---|---|---|---|---|
| A1 | When2Call MCQ (AA protocol) | not stated | not stated | not stated; AA protocol, 3,423 of 3,652 items (229 "ask for more info" removed) | Eval only. Jev 1.14 is read by us, not used as data. |
| A2 | AgentDojo as detector (AD-Clean, AD-Matched, AD-Shift; Liu MIT harness, arXiv 2610.03448) | AgentDojo v1.2 environments (per section 2); the version Liu's harness pins must be checked by L-E (flag K10) | harness MIT (per section 4); data licence not stated | Liu harness plus AgentDojo environments | Row counts must match: AD-Clean 339/97 tasks, AD-Matched 585/432, AD-Shift 975/720. |
| A3 | InjecAgent as detector (TB-Matched construction) | not stated | not stated | InjecAgent release; tau-bench product names | Labelled "our protocol", never "the InjecAgent benchmark". 584 injected / 1,533 benign. |
| A4 | NotInject | not stated | MIT (per section 4, eval only) | not stated | 339 benign. Eval only, never training (GPT-4o-mini written, per section 2 barred list). |
| A5 | ATBench-Codex | not stated | Apache-2.0 (per section 4) | not stated | 500 items. Eval only; as data it falls under the AgentDoG/ATBench data bar (E30). |
| A6 | ATBench | not stated | not stated | not stated | 1,000 items. Eval only; ATBench data is barred as training. |

## B. Public eval sets, Tier 2 and report-only (never in a "#1" claim)

| ID | Name | Version | Licence status | Data source | Notes |
|---|---|---|---|---|---|
| B1 | BFCL v4 decision categories (relevance, irrelevance, live_irrelevance, miss_func, miss_param) | v4 | not stated | BFCL v4 release | Item subset we read and found clean. Epoch rated BFCL v4 Flawed. Eval only. |
| B2 | MCP-Atlas public 500 | public 500 | not stated | not stated | Scored only on steps whose next tool is uniquely forced. |
| B3 | CRUXEval-O and CRUXEval-I | not stated | not stated | not stated | Multiple choice; gated against base 4B. Also an upstream exclusion (section D). |
| B4 | EquiBench, Python pairs | not stated | not stated | not stated | Gated against base 4B. Also an upstream exclusion (section D). |
| B5 | AgentProcessBench | not stated | not stated | not stated | Reference is the author table, not the "79.1 vs 66.8" figure. Trajectories are also an upstream exclusion (section D). |
| B6 | SteerBench-Work | 106 scenarios | runner MIT; scenarios CC BY 4.0 (per section 4) | not stated | Scenario strings are also a permission target (section G). |
| B7 | MSB (MCP signature and response carriers) | not stated | MIT (per section 4) | not stated | Server and tool lists are also an upstream exclusion (section D). |
| B8 | Impossible-LiveCodeBench and Impossible-SWEbench (item level) | not stated | none stated in plan | not stated | Used only if a data licence is stated by the report date; otherwise skipped and said so. Registered as a G13 target either way (D29). See flag K3. |
| B9 | WildGuardTest (AA subset, 835) | not stated | ODC-BY (per section 4) | not stated | One-line report only (25% of the AA index). |
| B10 | Saber harm rate | not stated | not stated | not stated | Name only; no source in plan sections 2 or 4. |
| B11 | SWE-bench-Live and SWE-rebench fresh patch verdicts | not stated | not stated | not stated | Eval use only. SWE-rebench is also a P1-conditional training source. See flag K1. |
| B12 | JevBench coding topic (sanity only, no submission) | not stated | not stated | JevBench board (Jev-owned) | Competitor-owned benchmark. Sanity read only. Jev outputs are never data. |
| B13 | Jev Decision Index Tools area | not stated | not stated | Jev-owned | Competitor read. Never data. |

## C. Named in section 4 as NOT REPORTED, but still G13 targets (plan: "all eval sets are registered")

| ID | Name | Licence status (as plan states it) | Why still registered |
|---|---|---|---|
| C1 | AmPermBench | NC or unclear (section 4) | Exact item strings, entity names and ID patterns are permission targets (section G). |
| C2 | R-Judge | NC or unclear (section 4) | Named in section 4; registered for the exclusion check. |
| C3 | TraceSafe | NC or unclear (section 4) | Named in section 4; registered for the exclusion check. |
| C4 | end-to-end tau2 / tau-bench | not stated | tau-bench data is also an upstream exclusion (section D). |
| C5 | Terminal-Bench | not stated | Named in section 4. |
| C6 | SWE-bench (full) | not stated | Named in section 4; the SWE-bench family is also a P1 source question (section J). |
| C7 | AuthGateBench | no data licence (section 4) | Also barred as training (section E). |
| C8 | TRACE | CC-BY-SA per HF card; sources disagree (section 2) | Not needed; also an upstream exclusion (section E). |
| C9 | UnderSpecBench | unreleased (section 4) | Exact item strings, entity names and ID patterns are permission targets (section G). |
| C10 | OverEager | unreleased (section 4) | Named in section 4; register whatever is public (paper examples) so the name is on the list when data appears. |
| C11 | CARE split (CARE-style protocol) | split unreleased (section 4) | Our own held-out commands are used; "not comparable" label. CARE code and rules are barred (section E). |
| C12 | CoRE | no licence file (section 2) | Also an upstream exclusion (section D) and barred (section E). |
| C13 | LibriSpeech test-clean and test-other | standard eval sets | Never used in training (section 2 voice). Register as G13 targets. |

## D. Upstream eval-environment exclusions (section 2, EVAL UPSTREAM EXCLUSION; these are G13 targets)

Injection and agent environments (plan injection 2.3):

| ID | Target | Source named in plan |
|---|---|---|
| D1 | AgentDojo v1.2 environment strings and tool schemas | AgentDojo v1.2 |
| D2 | tau-bench data | tau-bench |
| D3 | BIPIA contexts | BIPIA |
| D4 | InjecAgent user cases and tool lists | InjecAgent |
| D5 | AgentDyn environments | AgentDyn |
| D6 | MSB server and tool lists | MSB |
| D7 | MCPTox server and tool lists | MCPTox |
| D8 | LLMail-Inject | LLMail-Inject |
| D9 | NotInject trigger words and prompts | NotInject |
| D10 | PIDS-Bench hard-benign prompts | PIDS-Bench |
| D11 | TensorTrust | TensorTrust |
| D12 | CodeIPI | CodeIPI |
| D13 | LogJack payloads | LogJack |

Tool-use targets (plan tools 5.19):

| ID | Target | Source named in plan |
|---|---|---|
| D14 | tau2 / tau-bench tool and domain names | tau2, tau-bench |
| D15 | MCP-Atlas tool names (220) | MCP-Atlas |
| D16 | MCP-Bench servers (28) | MCP-Bench |
| D17 | MCP-Universe servers (11) | MCP-Universe |
| D18 | ToolHop tools | ToolHop |
| D19 | CAR-bench tool names | CAR-bench |
| D20 | AgentProcessBench trajectories | AgentProcessBench |

Code targets (plan codeexec T42c-4):

| ID | Target | Source named in plan |
|---|---|---|
| D21 | CRUXEval | CRUXEval |
| D22 | LiveCodeBench, incl. test-output prediction | LiveCodeBench |
| D23 | REval sources | HumanEval, ClassEval |
| D24 | CodeMind sources | CodeMind |
| D25 | CoRE | CoRE |
| D26 | SWE-Flux repos | SWE-Flux |
| D27 | EquiBench Python pairs | EquiBench |
| D28 | CRUXEval-X | CRUXEval-X |
| D29 | Impossible-LiveCodeBench and Impossible-SWEbench | Impossible-* |
| D30 | EvilGenie | EvilGenie |

Permission targets (plan permission 5.9, 5.19; section 2 v3.1):

| ID | Target | Source named in plan |
|---|---|---|
| D31 | AmPermBench and UnderSpecBench exact item strings, exact entity names, exact ID patterns (not generic domain words or phrase frames) | AmPermBench, UnderSpecBench |
| D32 | SteerBench-Work scenarios | SteerBench-Work |
| D33 | CredLeakBench items and cue-list strings (T53 uses cue categories only) | CredLeakBench |

## E. Training upstreams to exclude (never as data)

| ID | Name | Reason (as plan states) |
|---|---|---|
| E1 | CVEfixes | Removed since v1 |
| E2 | PrimeVul | Removed since v1 |
| E3 | BigVul | Removed since v1 |
| E4 | MoreFixes | Removed since v1 |
| E5 | Atomic Red Team | Removed since v1 |
| E6 | GTFOBins | Removed since v1 |
| E7 | NL2Bash | Removed since v1 |
| E8 | tldr-pages | Removed since v1 |
| E9 | Human-written MCP server schemas | Removed since v1 |
| E10 | When2Call train | OUT (paper: Mixtral 8x22B generated and classified the data; barred by owner 27 Sep rule) |
| E10b | xLAM-60k / APIGen data (When2Call's training categories; card mixes cc-by-4.0 with "research purposes only") | Barred either way (section 2, STATUSES CLOSED) |
| E11 | CodeReviewer | OUT |
| E12 | CodeReviewQA | OUT of every tier (derived from CodeReviewer) |

Barred by the no-LLM-generated-datasets rule:

| ID | Name |
|---|---|
| E13 | Toucan-1.5M |
| E14 | Nemotron tool_calling |
| E15 | Nemotron-RL-IPI |
| E16 | ToolACE |
| E17 | AceCode-87K |
| E18 | CodeScaler synthetic data |
| E19 | SWE-smith LM-written bugs |
| E19b | SWE-smith problem_statement field (LM-prompted issue text; barred in T57r and P1; skeptic 27, verified 18 Oct) |
| E20 | R2E-Gym issue text |
| E21 | NotInject (GPT-4o-mini written; eval only) |
| E22 | AuthGateBench (DeepSeek-V4-Flash written; eval barred as data) |
| E23 | AgentAbstain |
| E24 | ToolMaze |
| E25 | ToolBench-X |
| E26 | NesTools |
| E27 | ToolHop (as data) |
| E28 | CAR-bench tasks (as data) |
| E29 | ClarifyBench |
| E30 | AgentDoG and ATBench data |
| E31 | StepGuard |
| E32 | DynaGuard |
| E33 | Terminal Wrench |
| E34 | HackTrace |
| E35 | IH-Challenge (creation method not stated; treated as barred) |
| E36 | PIDS-Bench (as data) |

Not usable (licence):

| ID | Name | Reason |
|---|---|---|
| E37 | IssueTrojanBench | CC BY-NC-ND |
| E38 | WASP | CC-BY-NC |
| E39 | TensorTrust data | no licence |
| E40 | MCPTox | no terms found |
| E41 | TRACE data | CC-BY-SA per HF card; sources disagree |
| E42 | ImpossibleBench HF data | no licence stated |
| E43 | AuthGateBench | CC BY-NC-ND paper; no data licence |
| E44 | CoRE | no licence file |

Competitor outputs and weights (never data, never label, never filter):

| ID | Name |
|---|---|
| E45 | Jev (all reads) |
| E46 | AgentDoG |
| E47 | OpenHands critic |
| E48 | Strands Decider |
| E49 | Horizon |
| E50 | PromptGuard |
| E51 | PIGuard |
| E52 | every other detector |
| E52b | every rival or reference model named in plan section 4 (Celeris-1, GLiDE, d1-ultra, Prompt Guard 2 86M, Horizon guard-base, AgentDoG v1 / 1.5, GPT-5.4, the 7-8B task-aware judges, CLM-8B, Microsoft-Decision-1, Gemini-3-Flash-Preview-Thinking); outputs never data, label or filter (section 2 NEVER USED AS DATA; owner no-big-teachers rule) |

Licence bars on code and tools (not data, but barred):

| ID | Name | Licence (as plan states) |
|---|---|---|
| E53 | bashlex | GPL-3.0 |
| E54 | CARE code and rules | depends on bashlex; rule bank mixes MITRE/GTFOBins with unchecked terms |
| E55 | AgentTrust code and rules | AGPL-3.0 from v0.6.0 |
| E56 | TruffleHog | AGPL-3.0 |
| E57 | Hypothesis (vendored into rows) | MPL-2.0 |
| E58 | SWE-smith-js | no licence stated |

Voice barred (plan section 2 voice):

| ID | Name | Reason |
|---|---|---|
| E59 | Chatterbox | unnamed 0.5M-hour data |
| E60 | Piper | GPL engine; research-only voices |
| E61 | F5-TTS | NC weights |
| E62 | XTTS and other non-permissive engines | licence |
| E63 | espeak-ng (out-of-vocabulary fallback inside misaki/Kokoro) | GPL; disabled; L-G tests day 2 |
| E64 | SWE-smith-py GPL and LGPL repos | row-level exclusion (paper Table 6) |

8.5 HIT list (recorded A61(a) HITs; bar the source under any id or form):

| ID | Source |
|---|---|
| E65 | gsm8k |
| E66 | hover |
| E67 | isarcasmeval |
| E68 | tydiqa |
| E69 | md_fdc |
| E70 | md_peps |
| E71 | DI-TS inputs |

Allowed as tools only (not exclusions): tree-sitter-bash (MIT), mvdan/sh (BSD-3), gitleaks (MIT; key-shape catalogue), mutmut (BSD-3), cosmic-ray (MIT), sqlglot (MIT; SQL parsing).

## F. Guard literal classes (C_DATA_SPEC 4.3, applied to every C2.1 source)

| ID | Class | Note |
|---|---|---|
| F1 | n8n and ejs-5 | named guard |
| F2 | CVE- and GHSA- identifiers | pattern guard |
| F3 | /rosetta/i pattern | pattern guard |
| F4 | stackoverflow and stackexchange links | link guard |
| F5 | BIG-bench canary string | canary guard |
| F6 | Repos: lm-eval-harness, opencompass, helm, bigbench, leetcode | repo guard |
| F7 | PII scrub: T53 registered-fake check | check, not a literal list |
| F8 | Deny-list program on every name | program check |
| F9 | Domain rule 3 | named in section 2 GUARDS; applies to every C2.1 source |
| F10 | General rows: no shared sources or domains with OHS-3/4/5 G | section 2 GENERAL ROWS; a domain-level check, not a literal match |

## G. Literal-target classes (the 200-row pilot checks these; more than 1% hit sends the generator back)

| ID | Class | Targets (names only) |
|---|---|---|
| G1 | Injection-eval literals (attack strings AND benign-side strings; NotInject trigger words and PIDS-Bench hard-benign prompts are benign-side) | InjecAgent attacker instructions (62); AgentDojo injection strings; BIPIA contexts; LLMail-Inject; TensorTrust; CodeIPI; LogJack payloads; NotInject trigger words and prompts; PIDS-Bench hard-benign prompts (MSB and MCPTox server/tool lists sit in G3) |
| G2 | Function docs and code-eval sources | CRUXEval; LiveCodeBench; REval (HumanEval, ClassEval); CodeMind; EquiBench pairs; CRUXEval-X; EvilGenie; SWE-Flux repos; Impossible-* items |
| G3 | Tool and server names | tau2 and tau-bench tools and domains; MCP-Atlas (220); MCP-Bench (28 servers); MCP-Universe (11 servers); ToolHop tools; CAR-bench tool names; MSB and MCPTox server and tool lists; AgentDojo v1.2 tool schemas |
| G4 | Exact item strings, entity names, ID patterns | AmPermBench; UnderSpecBench; CredLeakBench items and cue-list strings (T53: categories only) |
| G5 | Scenario strings | SteerBench-Work |
| G6 | Product-format scaffolding (an EXEMPTION class, not a target: hits traced only to it are logged but do not count as the fix iteration; owner-reserved with R6) | sha-bound header, option scaffolding, definitions card (exempt from the fix iteration only when the hit traces to this scaffolding alone; v3.1 exception (a)) |

## H. Sealed-side G13 targets (names only; never opened by a training lane)

| ID | Target |
|---|---|
| H1 | OHS-3 (matched by G13 under the orchestrator only; separately, every NEW L-0 program - C2-mix hash export, token histogram, access audit, manifest builder, row-start guard - skips data/ohs3* and ohs3_parts/ in every data/** glob, with a CPU test; skeptic 30) |
| H2 | OHS-4 |
| H3 | OHS-AC |
| H4 | OHS-5 (once frozen; row jobs refuse to start without the OHS-5 FREEZE record and this registry's sha; rows colliding with frozen OHS-5 are dropped row by row, up to 5% of a family not counting as the fix iteration, skeptic 22b) |

## I. Items named in lane files, source not given in sections 2 or 4 (not registered yet)

| ID | Name | Where named | Status |
|---|---|---|---|
| I1 | V2-lite real-speech set | LANE_L-0 output (d); LANE_L-E inputs ("the V2-lite real-speech record (if consent covers it)") | Opus: REGISTER NOW as a conditional held-out eval target (moved to M4). L-E reports by Sun 25 whether consent covers eval-only reuse; if not, the entry is retired, never moved to training. |
| I2 | R5 candidate dataset list | LANE_L-0 day-1 task 2 (names from the 17 Oct Decision Index note) | Owned by the names-only manifest v1 (Sonnet draft, Opus freeze Mon 19). Not read here. |

## J. Candidate training sources (P0 and P1-conditional; each needs a pre-mapper 8.5 PASS, listed for the exclusion check)

| ID | Name | Status (as plan states) | Licence (as plan states) |
|---|---|---|---|
| J1 | Vendored permissive Python repos (30-60; T64) | P1-conditional; fallback synthetic modules | MIT, Apache or BSD per repo |
| J2 | SWE-smith-py procedural instances (gold patches, tests, repos only; problem_statement barred) | P1-conditional; Docker under runsc untested | Dataset card MIT; GPL/LGPL repos excluded row by row |
| J3 | SWE-Gym | P1-conditional | Repo Apache-2.0; HF card MIT |
| J4 | SWE-rebench V2 | P1-conditional; out of P0 | not stated in plan here |
| J5 | CommitPackFT | P1-conditional; out of P0 | not stated in plan here |
| J6 | Kokoro-82M (voice generator A) | voice rows (section 2 / 7; L-G), not P1-conditional | Apache-2.0 (voices graded C or better); espeak-ng fallback disabled (E63) |
| J7 | MUSAN (acoustic noise) | voice rows (L-G) | CC BY 4.0 |
| J8 | OpenSLR 28 (SIMULATED RIRs only) | voice rows (L-G) | not stated in plan; use restricted to the simulated RIRs |
| J9 | Nemotron EN 0.6B (ASR, pinned main revision 13 Mar 2026, not the Jan 2026 branch) | voice rows (L-G) | not stated in plan (vendor card: trained on LibriSpeech, so harvested error rates understate real error) |
| J10 | LibriSpeech TRAIN splits only (generator B) | voice rows (L-G) | CC BY 4.0; test-clean / test-other are G13 targets (C13) |

## K. Flags for Opus confirmation

- K1. SWE-rebench appears twice: as a fresh-verdict eval (B11) and as a P1-conditional training source (J4). Two entries are kept, and the eval use must stay out of training.
- K2. Most eval sets have no version, licence or URL in sections 2 and 4. L-E must fill these from the official release before any pull, and the registry sha depends on it.
- K3. Impossible-* (D29, B8): section 2 says the HF data has no licence. Item-level use stays skipped unless a licence is stated by the report date.
- K4. AgentDoG 1.5-4B licence is UNVERIFIED (HTTP 401, 18 Oct). It is a rival read, never data, so this does not block the registry.
- K5. LibriSpeech test-clean and test-other are eval standards (C13). Training uses TRAIN splits only.
- K6. Section 2 also bars AgentDoG and ATBench data (E30) while section 4 reads ATBench as eval (A6). Both entries are kept as eval-only.
- K7. The V2-lite real-speech set (I1) has no source in sections 2 or 4. It is not registered here.
- K8 (kept, see K11). Training lanes do not read section 4 by plan rule. This draft used it only because the task names it (LANE_L-E.md lines 1-97). The L-E block was not opened.

- K9 (Opus). P1 sources J2-J5 (SWE-smith-py, SWE-Gym, SWE-rebench V2, CommitPackFT) can share repos and instances with the B11 / C6 SWE-bench-family evals. G13 for these families must match at instance level (instance ids, gold-patch hashes, test ids) against SWE-bench, SWE-bench-Live and the SWE-rebench eval instances, and the B11 eval instances are named in the manifest before any P1 pre-mapper 8.5 run.
- K10 (Opus). AgentDojo version: section 2 names v1.2 environments; Liu's harness may pin a different AgentDojo release. L-E records the harness's pinned version; if it differs from v1.2, both versions are registered (D1 and A2).
- K11 (Opus). Section 4 was read by a training-lane (L-0) agent because the orchestrator task named it, for names only. Section 4 holds no sealed content, but the access audit must log this read as an orchestrator-authorised exception rather than a violation.

## M. Internal held-out sets (Opus, 18 Oct; ours, never trained on; G13 targets so no training row can copy them)

| ID | Set | Source in plan | Why registered |
|---|---|---|---|
| M1 | L-I benign injection dev split (AgentDojo PRIMARY 1%-FPR threshold source) | section 4 Tier 1 item 2 (v3.1 skeptic 16); LANE_L-E inputs | Must be "never trained on"; T41c and every injection family are matched against it. |
| M2 | Our own held-out commands for the CARE-style protocol (Tier 2) | section 4 Tier 2 | Held out by definition; labelled "not comparable". |
| M3 | Voice 300-utterance dev robustness slice (160 ms and 1,120 ms chunk modes) | section 2 voice (skeptic 14) | Dev only, never training. |
| M4 | V2-lite real-speech set (conditional on consent; see I1) | LANE_L-E inputs | Eval only if consent covers it. |

## L. Counts

- Tier 1 eval sets: 6 (A1-A6)
- Tier 2 and report-only: 13 (B1-B13)
- Not-reported eval sets registered: 13 (C1-C13)
- Upstream eval-environment exclusions: 33 (D1-D33)
- Training upstream exclusions (source bars): 74 entries (E1-E71 plus E10b, E19b, E52b), of which E65-E71 are the 7 recorded 8.5 HITs
- Guard classes: 10 (F1-F10)
- Literal-target classes: 6 (G1-G6)
- Sealed targets (names only): 4 (H1-H4)
- Lane-named items: 2 (I1 now registered as M4; I2 owned by the manifest)
- Internal held-out sets: 4 (M1-M4)
- Candidate training sources: 10 (J1-J10)
- Flags: 11 (K1-K11)

## Opus review, 18 Oct (changes made in place)

Checked against PLAN_TRAINING_SIDE.md section 2 and LANE_L-E.md section 4. Every Tier-1, Tier-2 and NOT REPORTED name in section 4 and every EVAL UPSTREAM EXCLUSION, barred, not-usable, never-used and 8.5-HIT name in section 2 is present. Changes:
1. Added "Role of each section": G13 targets are A-D, G, H, M; E is a source bar (manifest / allow-list / 8.5), not a G13 content target.
2. Added the skeptic-8 rule (literal-ban list inside G13 only; hit reports carry row id, target name, method).
3. MISSING, added: F9 domain rule 3 and F10 general-row domain disjointness from OHS-3/4/5 G (both section 2).
4. MISSING, added: E10b xLAM-60k / APIGen data; E19b SWE-smith problem_statement field; E52b section-4 rival models; sqlglot to the allowed tools.
5. MISSING, added: section M internal held-out sets (L-I benign dev split = AgentDojo primary threshold source; CARE-style held-out commands; voice 300-utterance dev slice; V2-lite real speech, conditional). I1 is now registered as M4.
6. WRONG, fixed: B8 pointed at K4 (now K3); C9/C10 licence "not stated" is "unreleased" per section 4; G1 mixed benign-side strings and server lists into "attack-string literals" (renamed; MSB/MCPTox lists and AgentDojo tool schemas moved to G3); G6 is an exemption, not a target; H1 implied G13 skips OHS-3 (the skip is for new L-0 programs only); J6-J10 voice sources were labelled "P1" (voice is a planned L-G row group); J8/J9 licence column held non-licence facts.
7. Added flags K9 (SWE-family instance-level matching against B11/C6), K10 (AgentDojo version pinned by Liu's harness), K11 (section-4 read logged as an authorised exception).
Unchanged and still open: K2 (versions, licences, URLs are L-E's to fill before the sha), K4 (AgentDoG 1.5-4B licence UNVERIFIED; rival read only).

## N. L-E Tier-1 eval targets filled (L-E day-1, Sun 18 Oct 2026; Sonnet 5.5 builder)

Status: FILLED, for Opus confirmation. These are the G13 TARGETS for A1-A6 and fill K2 for them (version, licence, URL, sha). Eval only, never a training input. Paths are relative to lean/. Harness code: c2_build/c21_eval/. `format_status` of every rows file is PROVISIONAL until the owner-reserved product format is supplied (see c2_build/c21_eval/formats.py); rows shas change when it is frozen and are then re-registered. K10 (AgentDojo version): Liu's harness uses agentdojo==0.1.34 with suites v1.2 = the same v1.2 as D1; no second version to register.

| G13 ID | Target | Path | Data sha256 | Licence | Version / URL | Row count |
|---|---|---|---|---|---|---|
| A1 | When2Call MCQ (AA protocol) | bench/c21_eval_quarantine/when2call/test/when2call_test_mcq.jsonl | 8c3694e583eeeb8dbc297e6cd90da70efc68efa4b6adb7227523e828c6b7b14c | CC-BY-4.0 | HF nvidia/When2Call @ 0582f7749df63a96fdc3070932e83e72396ace53 | 3,652 (AA used 3,423; the 229 dropped are unpublished -> NOT SAME-PROTOCOL) |
| A4 | NotInject | bench/c21_eval_quarantine/notinject/data/*.parquet (one, two, three) | one:5b1d3a8ec3412053 two:a5a8c1b3b851b0b5 three:d5c685b123570c09 (first 16 hex; full in SOURCES.json) | MIT | HF leolee99/NotInject @ 847ae76cf8fea5ed325429e569ae8cfef022d2e0 | 339 (3 x 113) |
| A5 | ATBench-Codex | bench/c21_eval_quarantine/atbench_codex/test.json | b402a8b6b7fdeea20f0acb1e5b88308307c74e003c1724fde7290496ff12970f | Apache-2.0 | HF AI45Research/ATBench-Codex @ 0991350e2f7ad174fae5fb8f7b6f5ec5a171a609 | 500 (250 safe / 250 unsafe) |
| A6 | ATBench | bench/c21_eval_quarantine/atbench/ATBench/test.json | 80c534b5f3517c872b528a2e6b64e34495206968edd184f4aed563d39f0cca09 | Apache-2.0 | HF AI45Research/ATBench config ATBench @ 4476ef92ed8f85c8d58d8a5b9dfdf55aa7893138 | 1,000 (503 safe / 497 unsafe) |
| A2 | AD-Clean (Liu harness, rebuilt) | bench/c21_eval_quarantine/agentdojo_liu/built/agentdojo_benign_outputs.jsonl | 55122ae3ff83836d94c479a796dc88e891378a863adf2f3281b0937fe9f0b02b | MIT (harness) + MIT (AgentDojo) | github.com/lzwhehe/benign-instruction-bench @ 10430ce05038faf6241338af91d620a50dae4356; agentdojo==0.1.34 suites v1.2 | 339 outputs / 97 tasks: MATCHES |
| A2 | AD-Matched | bench/c21_eval_quarantine/agentdojo_liu/built/agentdojo_pairs.jsonl | 1965375338a6cbb006edf431faea9ab19351754ac552223f572b952fbd94ac96 | same | same | 585 benign / 432 injected: MATCHES |
| A2 | AD-Shift | bench/c21_eval_quarantine/agentdojo_liu/built/agentdojo_pairs_shift.jsonl | a198c0fd5eec786c1b73d725e9bd588331326423d77bbba32caf173ee4abf454 | same | same | 975 benign / 720 injected: MATCHES |

Built rows files (the files a model reads; derived from the data above; also G13 targets):

| Rows file | sha256 | n |
|---|---|---|
| bench/c21_eval_quarantine/when2call/rows/rows.jsonl | 07bd45e7b8c725122aa7884d78ebefc952434edeaf530b41885f8fbd1606280c | 3652 |
| bench/c21_eval_quarantine/notinject/rows/rows_tool_result.jsonl | 07f73c9b67244f6aad61a0ab5b1047dc5c02bb85a35046705e0fc7498aef0c1f | 339 |
| bench/c21_eval_quarantine/notinject/rows/rows_user.jsonl | 586abca66a9c04bf4f9411852a2d42a25e079dc5cf883c87523f777ac7dd34f5 | 339 |
| bench/c21_eval_quarantine/atbench/rows/rows_chunked.jsonl | fd8e1d3eb13292841ef4ba9d6a1c577086e27763e425b4bd50f005c36af09227 | 1582 |
| bench/c21_eval_quarantine/atbench/rows/rows_compact.jsonl | 4a055fdc8e9e1b276404b0c2dbab3d1ea48bdfd26c62e3962f48855d317a86d6 | 1000 |
| bench/c21_eval_quarantine/atbench_codex/rows/rows_chunked.jsonl | a9c3ec4b287bae4ed5256e155b91cdb0b92e68c621165bed55119fac228ffe95 | 544 |
| bench/c21_eval_quarantine/atbench_codex/rows/rows_compact.jsonl | 500cce29eddbf7c84c1bdaf8044b8c239d42ee4be49e45eebbc494b73007c08c | 500 |
| bench/c21_eval_quarantine/agentdojo_liu/rows/rows_clean.jsonl | 46c5a9aabf86fdeb818a54ba22a068d429585a27d8a32b2ae6c6c2813748f769 | 339 |
| bench/c21_eval_quarantine/agentdojo_liu/rows/rows_matched.jsonl | c1920cd9da50610950799373a6cc93bf6ea7d77a98cb7d5af9268f675f7b7f33 | 1017 |
| bench/c21_eval_quarantine/agentdojo_liu/rows/rows_shift.jsonl | 81089ce1f37626f96da9a250885d3b8992e318dc0a5dd0f10e49b1b3624e1882 | 1695 |

Not registered here (not a Tier-1 set in this task): A3 InjecAgent-as-detector (TB-Matched needs tau-bench plus InjecAgent clones; not downloaded in this pass) and the Tier-2 sets (B1-B13). Their K2 fields stay open.

Flags from this fill (for Opus):
- K12. When2Call: the AA 3,423-item subset cannot be reproduced; AA names no ids for the 229 dropped request_for_info items. The harness reports the full 3,652 and a lower / expected / upper bound for any 229-item drop, labelled NOT SAME-PROTOCOL. An 'ahead of Jev 1.14 under the AA protocol' claim needs the lower bound to clear Jev read by us on the same rows.
- K13. AgentDojo labels: 51 of 432 AD-Matched and 85 of 720 AD-Shift positives (11.8% of each) are write-tool outputs that differ from the clean replay only by a wall-clock timestamp, with no injected goal text in the output. Liu's counts (432 / 720) include them, so protocol-exact numbers keep them and cap any detector's TPR near 88%; an audited subset is a labelled secondary. Horizon's 82.2 / 87.9 are exposed to the same cap.
- K14. Liu's rebuild must run with PYTHONHASHSEED=0 and NOT under `python -I` (which ignores it). With the seed fixed, structure, labels and injection assignment repeat; texts differ only by timestamps, so the built/ files are the frozen copy and their sha is the registered one.
- K15. ATBench F1 bars (77.7 / 83.8): which F1 (UNSAFE-class or macro) the authors use is not in the text we hold; the harness prints both and makes no F1 claim until checked.
