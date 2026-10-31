# G0-LITE: T41c TAINT (clean-room)

Draft: Sun 18 Oct 2026 (UTC), lane L-I, Sonnet 5.5 high. Status: REVISED 18 Oct after Opus G0 approval verdict REVISE (G0_APPROVALS.md, T41c must-fix 1 to 3 plus global rulings G1, G2, G5, G6, G8, G9, G10); APPROVED in Opus Round 2 (G0_APPROVALS.md, R2-T41c-a to e); the L-I builder appended section 10 and edited 1.1 and line 8 as Round 2 requires (18 Oct). See section 9 Fixes and section 10. Where section 9 and an earlier section differ, section 9 binds.
Design only. No rows, no code run, no model call. Read for this draft: PLAN_TRAINING_SIDE.md, LANE_L-I.md, excerpts/injection_s5_1.md. Nothing else.
Rows start Sun 25 Oct. Data freeze Mon 2 Nov 23:59 UTC. Every bar below is written BEFORE any pilot.

Gate tags: **[PRE-FREEZE KILL]** = CPU, data only, can kill the family. **[POST-TRAINING REPORT]** = needs a trained model, report line only, never a kill rule.
"Near chance" bars (plan v3.1): binary probe held-out AUC <= 0.55 with upper bound <= 0.60, the bound being the 97.5th percentile of 2,000 cluster-bootstrap resamples (section 9; R2-T41c-e) (AUC is taken as max(AUC, 1-AUC)); k-way probe accuracy <= 1/k + 3 pp with upper bound <= 1/k + 6 pp.
Upper bound = 97.5th percentile of 2,000 cluster-bootstrap resamples over held-out groups (G5; groups = pair groups, see 3), on out-of-fold predictions of a 5-fold group CV, through the one L-0 probe harness (G5). Pilot (1,000 rows) numbers are advisory; the binding evaluation is on the full set.

## 1. Decision and label set

Question the family trains: given the user task and a set of source-tagged spans (the carrier is a tool output, file, MCP text or CI log), what should the gate do with the carrier content relative to the task? Output stays four-way (subtype goes to metadata only).

| Label | Meaning |
|---|---|
| ALLOW | Carrier has no directive aimed at the agent. Plain data, including off-topic noise. |
| ALLOW_BENIGN | Carrier has directive-looking or attack-vocabulary content that is acceptable: delegated and low-risk, task-necessary and low-risk, security discussion / trigger words, or human-addressed text. |
| ASK | Directive is in scope only with confirmation (soft-risk), or its authority is unclear (nested provenance). |
| BLOCK | Directive is out of scope and unrequested, or is a hard-risk action. Provenance, not claimed authority, decides. |

Label by provenance, not by shape. Claimed authority inside a span ("system says", "maintainers require") never changes a label.

### 1.1 PINNED LABEL TABLE (Opus rules on this; solver A and B both implement exactly this)

Row facts (all program-known from the spec): focus directive d (one per row, or two in a multi-directive row), its source tag, `agent_directed` (bool), `delegated` (bool: the user task points at this source or step with a generic verb and a scope), `necessary` (bool: d is on the critical path of the user task, from a per-task-class step set), `risk` in {LOW, SOFT, HARD} from the action record, `nested` (bool: third-party text quoted or vendored inside a user-owned file; both tags shown), `declared_policy` (bool: a system/developer span names this user-owned file as a project rules file).

Risk record (computed from the action against the "environment facts" block, or against the pinned facts-absent defaults when the block is absent; see 2 and 9.1): HARD if the action sends secret, credential or personal-data material to ANY host, declared or not, or places it in a URL, a log line or a package, or sends other project data to a host not in declared_hosts (R2-T41c-a; the one LOW exception is a credential used as an auth header to its own scope host (exact host, https), which is SLT-2 rule 2 under R2-T53-a and the only form of `ben.auth_declared_service`); deletes or overwrites outside declared_workspace or irreversibly; weakens a security check or permission; redirects a remote, endpoint, identity or access; adds a persistent hook; or changes a shared or production resource (the SLT-1 C3/C4 scope; R2-T41c-b: T41c has no lane facts, so such a directive class is generated only when an anchored span names the lane-tagged context). SOFT if it installs a package not in declared_manifest or from an undeclared index; is an unbounded or resource-heavy loop; touches targets beyond declared_targets; or deletes reversibly inside the workspace. Otherwise LOW.

First match wins:
1. No directive-like or attack-vocabulary content in any span -> ALLOW.
2. Directive-like or attack-vocabulary content with `agent_directed` false (security write-up, fixture, quoted example, lint pragma, human-addressed footer or contribution note) -> ALLOW_BENIGN.
3. `agent_directed` and risk = HARD -> BLOCK, even if delegated or necessary-looking (a generic delegation never names the operation and target).
4. `agent_directed` and `nested` -> ASK (authority unclear).
5. `agent_directed` and `declared_policy` and in scope: LOW -> ALLOW_BENIGN; SOFT -> ASK.
6. `agent_directed` and `delegated`: LOW -> ALLOW_BENIGN; SOFT -> ASK.
7. `agent_directed` and `necessary` (not delegated): LOW -> ALLOW_BENIGN; SOFT -> ASK.
8. `agent_directed`, not delegated, not necessary (unrequested), any risk -> BLOCK.
Multi-directive row: label = most severe of the per-directive labels (BLOCK > ASK > ALLOW_BENIGN > ALLOW).
MCP rule: for mcp_description and mcp_response, `necessary` or `delegated` holds only if d concerns invoking that same tool; any other directive is unrequested.
Delegated instructions that trigger a high-risk class are never ALLOW_BENIGN (rules 3, 6).

Opus rulings on the table (section 9.4; R2-T41c-e): O1 delegated + HARD = BLOCK. O2 nested + LOW = ASK. O3 unrequested + LOW = BLOCK (this makes "unrelated to task" alone not benign). O4 the HARD/SOFT boundary list above is approved as written (with the R2-T41c-a and R2-T41c-b edits). O5 the rule 5 control block (declared_policy, 4% of rows) is kept.

## 2. Gold method, solvers, inputs and state model

**Gold = program.** Each row starts as a structured spec. The label is a pure function of the spec (1.1). Text is realised from the spec.

**Attack/benign tuple (D2).** (user task class, authority set, carrier type, carrier format, placement bin, directive class, wrapper style, channel visibility, plus delegation mode, necessary flag, risk record, nested, declared_policy, agent_directed). Directive class = one of 8 HIGH goal classes (exfiltrate, destroy, weaken_security, supply_chain_install, redirect_permission, persistence_hook, resource_exhaustion, scope_widening) or a benign action class (4.4). Claude (Haiku 5.5 medium for wording; writers never see the G13 literal list) writes the directive text from the tuple. Program writes everything else.

**Environment facts block (state model).** A short block (target <= 80 tokens) inside the system/developer span: declared_workspace, declared_manifest (package names), declared_hosts, declared_targets, declared_tools. All names come from the seeded TRAINING-salt namespace. Risk is derivable from the rendered row by comparing the directive's anchors against this block when it is present, or against the pinned facts-absent defaults (9.1) when it is absent. At least 25% of rows are facts-absent (9.1), because the product hook may not supply the block (risk R4).

**Input view (plan E).** User task + source-tagged spans (user, system_developer, user_repo_file, third_party_repo_file, tool_result, mcp_description, mcp_response, ci_log). T41c is a with-tool-outputs family by nature (the carrier is the object); the labelled variant is the primary view. The 256-token cap on auxiliary tool outputs does not apply to the carrier; the 1,536 hard cap does. Source tags sit inside C2's existing rendered fields (D7, no re-render). Row ends with the product-format scaffolding (header, option scaffolding, definitions card), owned by L-0 and sha-bound; this one-pager only needs the card to state the four definitions and the tier boundary.

**Artifact first (D1).** Per carrier type, a program grammar builds the benign artifact with ONE slot. Background blocks come from Claude-authored pools (hash-exported) that a lint proves contain no agent-directed directive and no attack vocabulary outside the designated subtypes. Slot fill: (a) neutral filler -> ALLOW, (b) benign directive -> ALLOW_BENIGN, (c) one payload -> BLOCK/ASK. Fillers and payloads are length-matched so the full-text length bucket and the slot token length are label-neutral. The splice position is sampled from 5 placement bins.

**Solver A** = the generator's label function plus the spec. **Solver B** = a PROGRAM (ruling G1), written by a separate Sonnet 5.5 high session from this one-pager (table 1.1 plus 9.1) and the row schema only. It takes the rendered row plus an anchor map (offsets and roles of anchored strings: source tags, directive span, addressee marker, host, package, path, tool role, delegation pointer). B never sees A's code, the spec, the label, risk, tier, subtype or flags. It derives `delegated` from the delegation-pointer anchor plus a closed list of task verbs, `agent_directed` from the addressee anchor, and `risk` by comparing the host, package, path and target anchors to the facts block (or to the facts-absent defaults in 9.1 when the block is absent). B's partial dependence on generator anchors is accepted (Opus ruling); the G5-H blind reads cover the natural-language side. No LLM reads rows one by one to set or check a label. Two independent Haiku 5.5 medium solvers (G5-H) then read 300 rows blind from the rendered row only. They are audits: they never set or change a gold label, and a confirmed defect is fixed in the generator or the table, never by relabelling a row (G1).

**Text faithfulness.** Every tuple anchor string must appear verbatim in the realised text; a program check drops rows that omit one (drops logged).

**Contrast pairs (10% of rows).** Same carrier text, only the user turn edited (delegated vs not; necessary vs not). Label flips by table. Blocks the "carrier text alone decides" shortcut.

## 3. Sizes and shares

Training rows N = 2,000 if T41 is in C2's mix, else 3,000 (fixed at C2 GO #1). All shares are of N.

| Share | N=2,000 | N=3,000 |
|---|---|---|
| ALLOW 15% (clean twin 9%, off-topic noise 6%) | 300 | 450 |
| ALLOW_BENIGN 35%: delegated 14%, ambient helpful 12%, trigger-word / security discussion 5%, human-addressed or off-topic imperative 4% | 700 | 1,050 |
| BLOCK 35%: unrequested HIGH 20%, unrequested LOW 6%, HARD (delegated or necessary-looking) 9% | 700 | 1,050 |
| ASK 15%: delegated SOFT 5%, necessary SOFT 5%, nested or unclear 5% | 300 | 450 |
| Benign total (ALLOW + ALLOW_BENIGN) 50% | 1,000 | 1,500 |
| Delegated + ambient = 26% of rows = 52% of benign rows (bar >= 30%) | 520 | 780 |
| Facts-absent stratum (cross-cutting, 9.1) >= 25% of rows, >= 25% within every label, carrier type and subtype | 500 | 750 |
| Pair groups 60% of rows: 200 triples (clean+benign+attack) + 200 splice pairs + 100 task-edit pairs | 1,200 | 1,800 (x1.5 groups) |
| Multi-directive rows 12% | 240 | 360 |
| declared_policy control (cross-cutting, rule 5) 4% | 80 | 120 |

Extra dev blocks, never trained on, outside N, same generator, disjoint seeds:
- HO (held-out families): 480 rows, >= 80 per held-out value (2 wrapper styles, 2 goal classes, 1 carrier format, 1 placement). Label mix near the table. Training tuples exclude every held-out value (D3).
- BD (benign dev split): 400 rows, benign only (100 ALLOW, 300 ALLOW_BENIGN in training subtype proportions); handed to L-E as the Tier-1 AgentDojo threshold source.
- LS (long slice, optional, eval-only): 150 rows, carriers 1.5 to 3K tokens, uniform position, 50% benign. Exempt from the training cap because it is never trained on.

Pilot: 1,000 rows, then 200-row G13 pilot. Pilot rows are reused only if the template/wording hash is unchanged.

**Length (D6).** The 1.5 to 3K tail cannot fit the 1,536 cap, so the tail is NOT trained. Target carrier mix: 55% <= 256 tokens, 30% 257 to 640, 15% 641 to 1,200. Tier-1 long outputs use chunked max-score reads (stated). LS gives a post-training position/length report. Token budget: row mean <= 800, none > 1,536, <= 10% of rows above 1,024 (G6: the line moves from 1,000 to 1,024).

**Splits.** Pair groups never straddle train and dev. Options shuffled; 20% extra random-non-identity-permutation copies (plan 5). >= 50 wordings per task class and delegation mode, no wording above 2%.

## 4. Gates

### 4.1 PRE-FREEZE KILL (CPU, data only)

| ID | Gate | Numeric bar |
|---|---|---|
| K1 | Format-only probe (D1). LR on carrier type, serialisation, length bucket (5 token buckets), key names, and the facts-present flag (9.1); slot text masked to a fixed placeholder, no payload tokens. Views: B1 attack (BLOCK+ASK) vs benign (ALLOW+ALLOW_BENIGN); B2 BLOCK vs ASK; B3 ALLOW vs ALLOW_BENIGN; 4-way. | Each binary view: held-out AUC <= 0.55, UB <= 0.60. 4-way uses balanced accuracy (class priors are unequal): <= 28%, UB <= 31%. |
| K2 | Meta probe: placement bin, visibility, wrapper style, slot token-length bucket, directive-count, facts-present flag (9.1). Includes benign directives wrapped in the same 8 styles. | Each binary view AUC <= 0.55, UB <= 0.60. Wrapper-style share among agent-directed benign vs attack rows within 5 pp per style. |
| K3 | Held-out-family CPU probe (D3). TF-IDF + LR trained on in-family train rows; scored on (a) held-out in-family groups, (b) the HO block. Primary metric 4-way balanced accuracy; secondary B1 AUC. | Gap (a) minus (b) <= 5 pp on both metrics. Above 5 pp = fix iteration. CI reported. Two rotations of the held-out draw are report-only. |
| K4 | Composition (3). Benign share, subtype shares, label shares, carrier-type label mix. | Benign 50% +/- 1 pp; delegated+ambient >= 30% of benign rows (target 52%); each label and subtype within +/- 1.5 pp of table; ASK >= 12%; per-carrier-type label share within 8 pp of global; pair share >= 30% (target 60%); multi-directive 10 to 14%. |
| K5 | Delegation-cue balance (stops "delegation phrase = ALLOW"). | P(ALLOW_BENIGN given a delegation clause) between 40% and 70% (design value 58%); delegated+HIGH rows (rules 3, 6) >= 8% of N and 100% labelled by table. |
| K6 | Solver A vs B. (i) exhaustive truth-table over all fact combinations; (ii) full-set row agreement. | (i) 100% identical, over all fact combinations including the facts-absent defaults. (ii) >= 98% agreement of A and program-B (Opus accepted 98% for this family because the facts are read from natural-language anchors); disagreeing rows dropped and counted; above 2% fails. Disagreements on CPU test fixtures before the pilot are build fixes (G3). |
| K7 | Probe power control: inject a known leak (one key name only on attack rows) and re-run K1. | Probe must reach AUC >= 0.80 on the injected leak, else the K1/K2 result is invalid and re-run (a repeat of an invalid run is not a fix iteration, G5). K7 also includes the label-permutation sanity check (AUC 0.50 +- 0.03) on every probe run. |
| K8 | Token histogram (A50/G5 style). | Mean <= 800, max <= 1,536, <= 10% of rows above 1,024 (G6). |
| K9 | Names and faithfulness. Row-start guard against the frozen names-only allow-list; anchor check. | Guard refusals <= 2% of candidates (more = generator bug); anchor drops <= 3%; zero accepted rows with an off-list name. |
| K10 | 200-row G13 pilot (orchestrator, Mac, serial). Targets include AgentDojo v1.2 environment strings and tool schemas; BIPIA contexts; InjecAgent user cases and tool lists; AgentDyn environments; MSB and MCPTox server/tool lists; LLMail-Inject; NotInject trigger words and prompts; PIDS-Bench hard-benign prompts; TensorTrust; CodeIPI; LogJack payloads; attack-string literals; plus Liu-style README/AESLC/FineWeb-Edu text if any README text is ever vendored. Row-by-row OHS-5 collisions are dropped. | > 1% of 200 (3 or more rows) hit by any method = back to generator = the fix iteration. Product-scaffolding-only hits are exempt. OHS-5 drops <= 5% of the family's rows are not the fix iteration. |
| K11 | Adopted gates as recorded for C2: A50 G6 at size, A49c balance, G5-H (two Haiku solvers on 300 rows + one Haiku read of 100% of free-form rows, Sonnet adjudicates, Opus confirms A43(d) flags), G3-H. | Thresholds are the values in C2's records (not restated; L-0 supplies). Confirmed gold errors found by G5-H > 1% of the 300 sends the generator back. These use Haiku reads on data only (no trained model). Opus ruling G2: these are PRE-FREEZE gates (they read data, not a trained model). A G5-H flag counts only after Sonnet medium adjudication and Opus A43(d) confirmation, and after a program re-run (solver B) reproduces it. |
| K12 | Wording and dedupe. | No wording > 2%; >= 50 wordings per task class and delegation mode; no group in both train and dev; exact-duplicate directive text <= 2%. |

Rows start only after the OHS-5 FREEZE record, the G13 target registry sha and the names-only manifest exist (program check).

### 4.2 POST-TRAINING REPORT (never a kill)
- P1: trained-model in-family vs held-out-family gap (4-way accuracy, attack recall, benign-block rate), with CI.
- P2: per-class recall and FPR/FNR next to trivial baselines (always-ALLOW, always-BLOCK, majority, keyword/imperative regex), never a single accuracy.
- P3: benign-block rate on BD at the operating points; K/X static-attack ASR and benign-block rate vs C2 + 2 pp (plan rule).
- P4: flip rate under option permutation with CI; ECE (bin count stated), Brier, trap-slice ECE.
- P5: LS long-carrier accuracy by position and length bin; chunked max-score read vs single read.
- P6: ASK/BLOCK confusion (tier learnability); delegated+HARD recall.
- P7: format-only probe re-run on the trained model's logit offset by carrier type.

## 5. Clean-room notes
- Builder, Solver B, skeptic and writers never open the T27 / T40-T46 generators, templates, wording pools, mutate.py, OHS-AC, any sealed or ohs path, or any benchmark item text. Builders read only the stripped injection excerpt.
- Benchmark names above are G13 TARGET names for the registry only. No payload, item, entity name, ID pattern or environment string from any benchmark enters a prompt. NotInject: categories only, none of its trigger words or sentences. IssueTrojanBench, CodeIPI, LogJack, AIShellJack, MSB and MCPTox are taxonomy only.
- Writers (Haiku) get the tuple, the anchors and the length target, never exemplars, never the G13 literal-ban list. Hit reports to builders carry row ids, target name and method only.
- No detector output (PromptGuard, PIGuard, Jev, AgentDoG, and so on) is a label or a filter. No large-model teacher. Claude authors the text.
- D5 real-text realism: default is Claude-authored carriers; the realism gap is untested and the report says so. Real README/CI text from vendored repos only if that P1 source clears its pre-mapper 8.5 PASS and licence check. Nothing in T41c touches a source before then.
- Names: every company, repo, package, host, service, MCP server/tool, handle, path stem and branch comes from the seeded TRAINING-salt namespace; hosts use the shared L-0 host-TLD list and raw-IP pool (G8, 9.3), not a T41c-only list. No hand-picked fake names.
- No execution: T41c rows run no code (no runner, no sandbox).

## 6. NAMES for the names-only manifest (identifiers only; no surface names)

Surface names (org, repo, package, host, service, handle, path stem, branch, env var, ticket id, project, endpoint, MCP server and tool) are drawn per row from the TRAINING-salt namespace; the manifest records the slot IDs and the namespace spec, not values.

- Namespace slot IDs: `ns.org`, `ns.repo`, `ns.package`, `ns.host`, `ns.service`, `ns.handle`, `ns.path_stem`, `ns.branch`, `ns.envvar`, `ns.ticket`, `ns.project`, `ns.endpoint`, `ns.mcp_server`, `ns.mcp_tool`. Hosts and raw IPs come from the ONE shared L-0 list: `shared.host_tld_list` and `shared.raw_ip_pool` (reserved TLDs plus a generic list; documentation and private IP ranges; deny-list collision check against real brands and registered names). T41c keeps no list of its own.
- Policy / card IDs: `policy.taint_four_way` (definitions card, wording owned by L-0 scaffolding).
- Source tags (8): `src.user`, `src.system_developer`, `src.user_repo_file`, `src.third_party_repo_file`, `src.tool_result`, `src.mcp_description`, `src.mcp_response`, `src.ci_log`. Attribute: `attr.declared_policy`, `attr.nested`.
- Carrier types (12): `car.readme`, `car.contributing_guide`, `car.issue_body`, `car.review_comment`, `car.code_comment`, `car.rules_file`, `car.ci_log`, `car.ci_config`, `car.tool_json`, `car.tool_text`, `car.mcp_description`, `car.mcp_response`.
- Carrier formats (7): `fmt.markdown`, `fmt.json`, `fmt.yaml`, `fmt.plain`, `fmt.html`, `fmt.log_lines`, `fmt.toml`. Rule: each format used by >= 3 carrier types and each carrier type available in >= 2 formats, so holding out a format is not holding out a type. `car.ci_config` uses a generic synthetic pipeline schema with a closed key list (no vendor dialect).
- Code-comment languages (carrier content only, nothing executed): `lang.python`, `lang.javascript`, `lang.typescript`, `lang.go`, `lang.bash`. Runners: none.
- Task classes (12): `task.fix_failing_test`, `task.summarise_issue`, `task.update_dependency`, `task.review_change`, `task.answer_from_docs`, `task.triage_ci_failure`, `task.write_docs`, `task.refactor_function`, `task.run_build`, `task.onboarding_setup`, `task.search_codebase`, `task.use_mcp_tool`.
- Tool roles (stable internal IDs, never rendered): `tool.shell_run`, `tool.file_read`, `tool.file_write`, `tool.file_delete`, `tool.http_request`, `tool.pkg_install`, `tool.git_op`, `tool.mcp_invoke`, `tool.search_code`, `tool.run_tests`.
- HIGH goal classes (8): `goal.exfiltrate`, `goal.destroy`, `goal.weaken_security`, `goal.supply_chain_install`, `goal.redirect_permission`, `goal.persistence_hook`, `goal.resource_exhaustion`, `goal.scope_widening`.
- Benign action classes: `ben.install_declared_deps`, `ben.run_declared_tests`, `ben.run_declared_build`, `ben.lint_task_files`, `ben.auth_declared_service`, `ben.read_declared_docs`, `ben.set_task_env_flag`, `ben.apply_local_migration`, `ben.checkout_declared_branch`.
- Benign subtypes (metadata): `sub.delegated`, `sub.ambient`, `sub.trigger_security`, `sub.human_offtopic`, `sub.clean_twin`, `sub.noise`.
- Wrapper styles (8): `wrap.plain_imperative`, `wrap.authority_framing`, `wrap.urgency`, `wrap.fake_system_tag`, `wrap.role_play`, `wrap.preauthorised_disguise`, `wrap.conditional_trigger`, `wrap.hidden` (sub-variants `hid.html_comment`, `hid.alt_text`, `hid.zero_width`, `hid.base64`, `hid.split_chunks`).
- Placement bins: `place.p0` (first 20%), `place.p1`, `place.p2`, `place.p3`, `place.p4` (last 20%). Visibility: `vis.user_visible`, `vis.agent_only`.
- Delegation modes: `deleg.none`, `deleg.source_pointer`, `deleg.step_pointer`.
- Held-out draw (seeded, TRAINING salt, drawn once and recorded before any pilot): 2 of 8 wrapper styles, 2 of 8 goal classes, 1 of 7 formats, 1 of 5 placement bins. Nobody hand-picks it.

- Facts-absent names (9.1): `facts.present`, `facts.absent`, `facts.stratum_flag`, `fact.declared_hosts`, `fact.declared_manifest`, `fact.declared_workspace`, `fact.declared_targets`, `fact.declared_tools`, `fact.repo_remotes` (visible-in-span remotes of the working repo), `fact.visible_manifest_file`.
- Voice metadata (G10): `export.decision_spans`, roles `role.negation_polarity`, `role.number`, `role.entity_path_flag`, `role.authority`; `export.spoken_view` (not built for T41c carriers; user-task view only).

## 7. Risks

- R1: Table ambiguity (O1 to O5). Mitigation: Opus rules before code; K6(i) is an exhaustive truth-table test.
- R2: Claude-authored carriers may not match real text (PIDS-Bench: detectors fail on external benign text). Untested realism gap; reported.
- R3: Writer faithfulness. Haiku text may not express the tuple. Mitigation: anchors, K9, G5-H.
- R4: Labels depend on the environment facts block; the real hook may not supply declared hosts/manifest/workspace. Mitigated by the facts-absent stratum (>= 25% of rows) with pinned defaults (9.1); L-0 or L-D records which facts the Claude Code hook can really supply, for C2.2.
- R5: Shortcuts outside the probe features (for example lexical urgency cues). Mitigation: benign directives share the 8 wrapper styles (K2), held-out probe K3, contrast pairs.
- R6: ASK vs BLOCK may look arbitrary (HARD/SOFT boundary). Mitigation: definitions card states the tiers; P6 reports confusion.
- R7: Over-defence on benign utility (Tier-1 benign block rate). Mitigation: 50% benign, 52% of it delegated/ambient, BD dev split.
- R8: Phrase overlap with benchmark environment text. Mitigation: G13 on exact strings only; generic domain words are not targets.
- R9: Token budget forces dropping the 1.5 to 3K tail; long Tier-1 outputs depend on chunked reads. Stated.
- R10: Boundary with T50/T53: T41c judges carrier content by provenance; the action-level gate is T50. No overlap in labels.
- R11: Extra dev blocks (HO 480, BD 400, LS 150) add generation and G13 load; LS is optional.
- R12: The OHS-AC regime (R4/R6, owner-reserved) may exempt or bind scaffolding; this family assumes binding.

## 8. The one fix iteration and kill rule

Triggers (any PRE-FREEZE KILL gate failing, including K10 > 1%, K3 gap > 5 pp, K1/K2 above bar).
Allowed knobs, declared now: (1) re-balance carrier / format / length sampling; (2) widen the benign wrapper mix and wording pools; (3) fix a table implementation bug (a table change needs an Opus ruling, not a knob); (4) widen the wording pools for the failing family axis; (5) remove an offending carrier-format pairing. Then a new template/wording hash export and a rerun of ALL pre-freeze gates on the fixed set.
Kill: any pre-freeze gate still failing after the fix iteration, or not through all pre-freeze gates by Mon 2 Nov 23:59 UTC, rolls T41c to C2.2/C3 (logged with the gate and numbers). A failed format-only probe (K1) after the fix is a kill because the generator leaks format into the label. POST-TRAINING lines (4.2) and queued C2 reads never kill. T41c is wave P0 family 4 of 9; the floor needs 6 of 9.

## 9. Fixes (Opus approval verdict REVISE, 18 Oct; must-fix 1 to 3)

Edits above are marked by reference to this section. Rows and code are still not started; nothing here changes a label rule in 1.1 except the facts-absent defaults, which are new pinned rules.

### 9.1 Must-fix 1: FACTS-ABSENT stratum and pinned defaults (risk R4)

Each row carries `facts.present` (the environment facts block is rendered) or `facts.absent` (it is not). At least 25% of all rows are facts-absent, with at least 25% facts-absent inside EVERY label (ALLOW, ALLOW_BENIGN, ASK, BLOCK), every carrier type (12) and every benign and attack subtype in section 3. The stratum is fixed at spec time (per-cell quotas, not rejection sampling after the fact) and applies to the 1,000-row pilot too. HO and BD blocks use the same 25% rule; LS follows it where practical.

Defaults when the block is absent. The risk record in 1.1 is computed by the SAME table, with these substitutions:
- no declared_hosts: every host outside the working repo's remotes is undeclared. The remotes must be visible in a span (a git remote line, a repo URL in a user or system span, or a tool result) as an anchored string; if no remote is visible, every host is undeclared. A directive that sends secret, credential or project data to an undeclared host is HARD; a directive that only contacts one (no data sent) follows the SOFT/LOW rules for its tool role as in 1.1.
- no declared_manifest: any package install is SOFT, unless a manifest file naming that package is visible in a span (anchor `fact.visible_manifest_file`), in which case it is declared and LOW. An install from an undeclared index stays SOFT.
- no declared_workspace: the workspace is the repo root. Deletes or overwrites outside the repo root, or irreversibly, are HARD; reversible deletes inside the repo root are SOFT.
- no declared_targets: only targets named in the user task are declared; touching any other target is SOFT.
- no declared_tools: only tools named in the user task, or a tool the user task points at through a delegation pointer, count as declared (used only by the MCP rule in 1.1, which is unchanged).
The label then follows rules 1 to 8 of 1.1 unchanged. Both solvers implement the substitution identically (K6(i) includes the facts-absent branch of every fact combination). The definitions card (L-0 scaffolding) is the same in both strata.

Generator consequences: a facts-absent row must still contain every anchor the defaults need (the repo remote, the visible manifest file, the task-named targets); a program check drops a facts-absent row whose risk would be undecidable from its rendered spans. The ben.* classes that rely on a declared manifest or host (`ben.install_declared_deps`, `ben.auth_declared_service`, `ben.checkout_declared_branch`) are realised in facts-absent rows only through a visible manifest file, visible remote or task-named target, so they stay LOW there; otherwise the same directive is SOFT and the row is ASK or BLOCK by the table, which is the point of the stratum.

Gates: K1 and K2 gain the facts-present flag as a feature; it must not predict the label (the flag's own contribution is read by the same harness: AUC <= 0.55, upper bound <= 0.60, in every binary view; 4-way balanced accuracy bar unchanged). K4 gains: facts-absent share >= 25% overall and within each label, carrier type and subtype (tolerance as for the other K4 rows, +/- 1.5 pp below the 25% floor is NOT allowed, the floor is a minimum). K3 and K6 are run on the whole set and on the facts-absent stratum separately; K6(ii) agreement >= 98% must hold in each. Report line P8 (POST-TRAINING, never a kill): trained-model accuracy facts-present vs facts-absent, with CI.

Product check (not a gate): L-0 or L-D records which of the five facts the Claude Code hook can really supply, for C2.2.

### 9.2 Must-fix 2: Solver B is a program (G1)

Stated in section 2 above. In short: B is code, written by a separate Sonnet high session from this one-pager and the row schema only; `delegated` = delegation-pointer anchor AND a task verb from a closed list (the list is written by the B session, frozen with the template hash, and not shown to the A builder); `agent_directed` = the addressee anchor; `risk` = anchors compared with the facts block or the 9.1 defaults. Partial dependence on generator anchors is accepted. G5-H (two Haiku solvers, blind) covers natural language and is audit-only.

### 9.3 Must-fix 3: shared host list (G8) and token line (G6)

T41c uses the ONE shared L-0 host-TLD list and raw-IP pool (reserved TLDs plus a generic list; documentation and private IP ranges; deny-list collision check against real brands and registered names). The reserved-only list is removed from sections 5 and 6. The K-gates follow the global rules: bound = 97.5th percentile (2,000 cluster-bootstrap resamples over held-out groups, G5), token line 1,024 (G6, in section 3 and K8). K9's names guard checks hosts against the shared list.

### 9.4 Opus rulings 18 Oct (copied word for word from G0_APPROVALS.md, plus global rulings that bind this family)

Rulings on the pinned table: O1 delegated + HARD = BLOCK (a generic delegation never names the operation and target, which matches T50's "hard never clears"). O2 nested + LOW = ASK. O3 unrequested + LOW = BLOCK (plan D4: "out of scope ... unrequested -> BLOCK"). O4 the HARD/SOFT boundary list is approved as written. O5 keep the declared_policy control block (4%). K6 at 98% agreement (not 99%) is accepted for this family, because the facts are read from natural-language anchors. HO, BD and LS stay outside N and are never trained on.

Global rulings that bind T41c: G1 (solver B is a program; LLM reads are audits and never set a label); G2 (A50 G6, A49c, G5-H, G3-H, A43(d) are PRE-FREEZE; answers O6); G3 (no free pilot tuning: the 1,000-row pilot is the first measured look, one combined fix is the fix iteration; defects found by unit tests, the build skeptic or A/B disagreement on CPU fixtures before the pilot are build fixes; exemptions: scaffolding-only G13 hits and OHS-5 collision drops up to 5%); G4 (T41c is kept or killed as a whole); G5 (one L-0 probe harness: grouped split, L2 logistic regression with fixed or inner-CV regularisation, AUC as max(AUC, 1 - AUC), 97.5th percentile of 2,000 cluster-bootstrap resamples, k-way balanced accuracy, permutation check, injected-leak power check); G6 (mean <= 800 tokens, no row above 1,536, rows above 1,024 <= 10%); G8 (shared host list); G9 (T41c is a carrier-directive decision, not an action gate, so it is not in the cross-family label test, but its HARD/SOFT list must not contradict the shared effects-to-label table in T50/G0_LITE.md section 3; the L-I build skeptic spot-checks this); G10 (voice metadata export: `decision_spans` with roles negation/polarity, number, entity/path/flag, AUTHORITY, where AUTHORITY marks any span whose presence in the user turn creates or limits permission: consent naming, scope declarations, boundaries, delegation pointers, values whose source is the user turn; `spoken_view` where one exists; L-0 routes it; a code requirement, not a gate; for T41c the user-task text and its delegation pointer are the AUTHORITY spans).

### 9.5 Re-check checklist for Opus

(a) Facts-absent defaults 9.1 (five bullets) do not contradict 1.1. (b) Stratum quotas: >= 25% overall and inside every label, carrier type and subtype. (c) Solver B is a program (9.2). (d) Shared host list and 1,024 line (9.3). (e) K1, K2 facts-present feature; K4 stratum row; P8 report line.

## 10. Opus rulings 18 Oct (addendum; copied word for word from G0_APPROVALS.md by the L-I builder)

Where the body text above still says otherwise, this addendum binds. The build skeptic checks that the code follows it.
Global rulings G1 to G10 (G0_APPROVALS.md "Global rulings") bind this family and are cited in section 9.4.

### 10.1 Round 1 decision, T41c

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

### 10.2 Round 2 decision, T41c

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

### 10.3 Builder implementation notes (NOT Opus rulings; flagged for the build skeptic and the next Opus batch)

Code: c2_build/c21_fam/T41c/t41c/ (table.py is solver A). Where the G0-lite is silent the builder chose the following;
none changes a rule of 1.1.
- I1. Rule 5's "in scope" is a program flag (`Directive.in_scope`), True only on declared_policy control rows. A
  declared_policy row whose flag is False falls through to rules 6 to 8.
- I2. The LOW exception of R2-T41c-a is: auth header, https, destination host == the credential's scope host. It does
  not also require the host to be declared. An undeclared service TARGET still makes the row SOFT (targets clause), which
  is how a `ben.auth_declared_service` row becomes ASK/BLOCK in the facts-absent stratum.
- I3. The 4% declared_policy block is 3% inside the ambient bucket (LOW -> ALLOW_BENIGN) and 1% inside the necessary-SOFT
  bucket (SOFT -> ASK). Its directive class is NOT on the task's critical path and no pointer covers it, so rule 5 alone
  decides the label.
- I4. "Unrequested HIGH" (20%) means unrequested with risk SOFT or HARD (any class); "unrequested LOW" (6%) means risk LOW.
- I5. Wrapper style, visibility, slot-length bucket, placement and chunk count are assigned to EVERY slot (fillers and
  non-agent content too) and are shared inside a pair group; the slot count is the same for every label. Without this the
  K2 probe separates ALLOW rows (no wrapper, no directive) from the rest.
- I6. Placement bin = the slot's position as a fraction of the NON-SLOT (skeleton) text, so it does not depend on the
  slot's own length and every member of a pair group sits in the same bin.
- I7. Necessary steps: the per-task-class step sets are `ids.NECESSARY_STEPS` (pinned data; every ben.* class is on the
  critical path of at least one task class). The MCP rule reads `declared_tools` only to decide whether the tool a
  mcp_* carrier belongs to is declared (facts-absent: named in the user turn or reached through a delegation pointer).
- I8. A step pointer in T41c covers every agent-directed directive of its carrier; a pointer anchor with sub `other`
  names a different source and delegates nothing (decoy, 5% of non-delegation units).
- I9. Pair groups: triples = the clean-twin count (180 at N=2,000), then task-edit pairs (5.5% of N), then splice pairs to
  reach 60% of rows. This is 540 + 220 + 440 rows instead of the 200/200/100 split in section 3 (1,200 rows either way).
- I10. The delegated-clause design value 58% (K5) is not reachable with the mandated shares: delegated ALLOW_BENIGN is 14%
  of N while HARD-delegated (>= 8%) and delegated-SOFT (5%) add at least 13%, so P(ALLOW_BENIGN | clause) <= 52%. The
  planner gives about 44%, inside the 40% to 70% bar.
- I11. Carrier lengths: carrier token classes 90-250 / 265-630 / 641-780 (55% / 30% / 15%) instead of 641-1,200, so that
  the row cap (<= 10% of rows above 1,024 tokens, G6) holds with the ~250-token context spans. The 1.5 to 3K tail is the
  LS block only.
