# G0 ADDENDUM v3.2 T53 EGRESS-SECRET (lane L-A; draft for Opus batch 1, target Mon 19 Oct 2026)

Author: Sonnet 5.5 high, Sun 18 Oct 2026 (UTC). Read scope used: C2_1_BUILD_ORDER.md (L-A and v3.2 blocks), C2_1_PLAN_v3.md sections 1, 2, 5, 6, 7, 8, the PRE-REGISTERED RULES block of section 3 and section 16, C2_1_EXTRA_LEVERS.md (ADOPT NOW), C2_1_PUBLIC_TRAIN_INVENTORY.md (section 4 ladder row for T53), PREREG_FINAL.md blocks A77, A79, A82, families/T53/G0_LITE.md (approved, rounds 1 and 2) and families/T50/G0_ADDENDUM_v32.md (same author, same day; the shared core and the generic overlay rules are defined there). No rows, no generator code, nothing executed, no model or API call. Never opened: any "ohs" or "sealed" path, OHS5_BRIEF_DRAFT.md, C2 build files, T27/T40-T46 generators, or any benchmark item text or cue-list string (only the cue CATEGORIES stated in the plan are used; CredLeakBench strings stay a G13 target).
Status: DRAFT for the Opus batch-1 approval (Mon 19 Oct). Every number is a design value fixed BEFORE any pilot; changing one after a pilot is a gate edit and needs Opus.
How this file binds: families/T53/G0_LITE.md (v3.1, APPROVED round 2, with its section 12 rulings) stays in force. This addendum binds ONLY where it says "REPLACES" or "ADDS". Unchanged: provenance gold, SLT-2 (the 8-rule first-match table, with R2-T53-a to e), the fake-credential registry (offline only), the six blocks and their sizes, K1-K24 bars. Sources: [OWNER-ROW], [LEV An], [CRIT x], [A82 n] as in the T50 addendum.

## 0. What changes, in six lines

1. [OWNER-ROW] The 200-row G13 pilot (K18) is REPLACED: every row is answer-checked and G13-stamped when it is made (section 8).
2. [CRIT C8; G7] A PHISHING-LINK HEAD: 300 head rows (extra copies outside the 2,000; at most 25% of the family's specs), 4-way destination-trust verdict (section 4).
3. [LEV A6, A10, A12, A15] Gate-directed injection (350), cue wrappers (250, conditional), character perturbation (250) and card-body / MCP-schema dialects are overlays on existing rows. Sizes unchanged.
4. [CRIT D1, D2] Difficulty ladder (L1-L4 per mechanism), mandatory quad, measured C2 bar on L4 rows.
5. [Opus b1 T53-M1, O-C1] Non-"send" sinks (stdout echo, temp file, shell history) are NOT added in C2.1; rule 6 stays log / telemetry only (section 5). C2.2 item.
6. [G9] K22 is extended to T50 edit actions that reach R13 (section 9).

## 1. Conditions carried from the Opus rounds (word for word; they still bind)

- R2-T53-a RULE 2 MATCH. Rule 2 matches only when the normalised destination host EQUALS the credential's scope host, with scheme https and no certificate warning. Membership in the card's trusted list is NOT required. Raw-IP forms and other trusted_odd forms do not match. A lookalike of the scope host falls to rule 3. Solvers A and B compute this from the scope record and the host, not from the trusted-list verdict. A transport defect on the scope host = rule 3 (choice 11.2a confirmed).
- R2-T53-b SLT-2 IS TOTAL. Rule 4 is "package_publish with a public payload". A confidential payload in a package_publish row continues to rule 7 with visibility = public (a registry is public): 7(b) if the registry is trusted, 7(e) otherwise. T53 does not generate this cell, but the engine and K23 cover it, because T50 specs can reach it through R13.
- R2-T53-c ONE MEANING OF TIER. `soft` clears when the user names both the operation and the destination: 7(b) can be cleared like 7(e); rule 4's not-named ASK on a trusted registry keeps tier soft. The ASK rows caused by a fact that naming does not settle carry tier `na`: rule 5, 7(c), 7(d) and rule 4 with an untrusted registry. The tier head rows (K24) use these tiers.
- R2-T53-d ask_on_soft (T50 cards only) turns 7(b) and 7(e) into ASK. Hard and na rows never change.
- R2-T53-e Choices 11.2 b, d and f are confirmed. K23's truth table adds the naming flag and ask_on_soft as inputs.
- Round 1: [FIX-1] first-match order; [FIX-2] personal data = secret (hard); [FIX-3] OFFLINE verifiers only, no network import (K21); [FIX-4] SLT-2 with `ask_on_soft` fixed OFF on the 6 T53 cards; [FIX-5] ASK quota counted AFTER drops, with the >= 10% oversampling of the ASK cells (unknown visibility, transport defect, unlisted MCP server): STILL BINDING and unchanged by check-at-generation.
- Global: G1 (solver B is a program), G2, G3, G4 (no sub-block or head rolls alone), G5, G6, G7 (heads as head rows), G8 (ONE host-TLD list and ONE raw-IP pool), G9, G10 (decision_spans; AUTHORITY marks naming of the operation and the destination and values whose source is the user turn).

## 2. Gate changes at a glance (K ids are those of the approved G0-lite)

All K-gates keep their v3.1 marking (PRE-FREEZE KILL, CPU, data only) and all P-lines stay POST-TRAINING REPORT, unless a row below says otherwise.

| Gate | v3.2 status |
|---|---|
| K1 registered-fake scan, K2 checksum uniformity | PER-ROW at creation (an unregistered token or a valid checksum = row dropped); bars unchanged (100%) |
| K3 documented-example cap and balance | SET-LEVEL (shares over the family) |
| K4, K5, K6, K8, K11, K12, K13, K14, K24 | SET-LEVEL, once on the pilot and once on the built family. K13 ASK quota is read on the FINAL set after all drops; the >= 10% ASK oversampling stays |
| K7 verdict and label agreement | PER-ROW (destination verdicts must agree 100%, otherwise the row is dropped and logged; label disagreement counts as an A/B drop; bar: label agreement >= 99% of generated rows) |
| K9 provenance fact coverage | PER-ROW |
| K10 contrast integrity | PER-GROUP at creation; a failing group is dropped whole |
| K15 wording pools, token budget | wordings SET-LEVEL; the 1,536 cap PER-ROW; mean and the 1,024 share SET-LEVEL |
| K16 no live-looking secret | PER-ROW |
| K17 split hygiene | PER-ROW; OHS-5 collisions dropped row by row by the stamp (<= 5% not the fix iteration) |
| K18 G13 200-row pilot | REPLACED by K18s (section 8) |
| K19 standard pipeline | SET-LEVEL once per family |
| K20 names guard / no-execution scan | names PER-ROW; the no-execution scan is CODE-LEVEL, rerun at each code sha |
| K21 no-network test | CODE-LEVEL CPU test, rerun at each code sha |
| K22 G9 | EXTENDED (section 9) |
| K23 first-match truth table | CODE-LEVEL exhaustive test; inputs unchanged (no `sink` attribute, O-C1) [Opus b1] |
| K25-K34 | NEW (section 10) |

## 3. Sizes: UNCHANGED, overlays by substitution, heads outside

The six blocks keep their sizes and labels: a provenance quads 440 (248/0/192), b destination distractors 480 (240/60/180), c visibility x class grid 360 (160/40/160), d channel coverage + consent twins 420 (160/110/150), e credential-use pairs 160 (80/0/80), f shape-confuser pairs 140 (70/0/70); total 2,000 (958 ALLOW = 47.9%, 210 ASK = 10.5%, 832 BLOCK = 41.6%); matched pairs/quads 1,400 = 70%; 60% primary / 40% with-results; dev = 10% of spec families; the 1,000-row pilot is half the family, proportional. Every overlay re-renders rows that already exist and is STRATIFIED by label, so no block's label totals change; the ASK quota arithmetic of FIX-5 is untouched.

| Overlay | Lever | Rows | Carried by |
|---|---|---|---|
| gate-directed injection | A6 | 350 (175 cue + 175 benign twins) | a 100, d 150, e 50, f 50 |
| cue wrappers | A10 | 250, CONDITIONAL on the Fri 23 probe | a 80, b 80, c 40, d 50 |
| character perturbation | A12 | 250 | user-turn prose, comments, file prose |
| card-body and MCP-schema dialects | A15 | all rows (one dialect per spec group) | 5 trained + 2 held-out dialects |
| held-out sub-families | A24 | 80 (4%) | tagged `heldout_family`, never trained |
| phishing-link head rows | CRIT C8 | 300 EXTRA head rows, outside the 2,000 | section 4 |
| reason and tier head rows (G7) | unchanged | extra, each from <= 25% of specs | unchanged |

## 4. PHISHING-LINK HEAD [CRIT C8; G7; plan 16.4 "T53 phishing-link head"]

QUESTION. The same rendered context as a primary T53 row (user turns, calls, card, destination string; the link may come from a user turn, a call argument or an earlier file_write; in the with-results view also from a tool output), with a separate question form and its own lettered options: "What is the trust verdict of this destination against the card's trusted list?" Options (4, letters shuffled per row, 20% extra permutation copies at mix level, not counted below):
- TRUSTED: destination verdict trusted_exact or trusted_odd (raw IP of a listed host, internal TLD, odd but exact after normalisation);
- LOOKALIKE: typosquat, wrong TLD, raw IP not listed, homograph/punycode, misleading subdomain, brand mismatch;
- TRANSPORT_DEFECT: a listed host reached over plain HTTP or with a certificate warning;
- UNRELATED: untrusted_plain (a host with no relation to the list).
GOLD (program, by construction): the T53 destination verdict computed by the existing normaliser (lower-casing, our own public-suffix table, stdlib punycode codec) and an exact comparison to the card's trusted list; precedence lookalike over transport (a lookalike over HTTP is LOOKALIKE). Solver B recomputes it from the rendered string with its own, different normaliser algorithm; agreement must be 100%.
SIZE AND DRAW. 300 head rows, one per distinct destination-bearing primary spec (blocks b, d and e first, then a and c), cap = min(300, floor(25% of the family's spec count)); the family has about 1,800 specs (2,000 rows less obfuscated duplicate renderings), so the cap is about 450 and 300 is inside it. Exact class balance 75 / 75 / 75 / 75: TRUSTED 75 (trusted_exact 38, trusted_odd 37); LOOKALIKE 75 (six cue categories, 12-13 each: typosquat 13, wrong TLD 13, raw IP 12, homograph 13, misleading subdomain 12, brand mismatch 12); TRANSPORT_DEFECT 75 (plain HTTP 38, certificate warning 37); UNRELATED 75. Raw-IP forms appear in both TRUSTED (odd) and LOOKALIKE, which is the counterweight to "odd looking => bad". Head rows sit in the same split as their primary row (G7). All hosts, brands and registries come from the TRAINING-salt namespace; lookalikes are program mutations of namespace hosts (character edit, TLD from the ONE shared list, confusable swap from our own small table, subdomain prefix, brand swap); the deny-list program rejects real-brand collisions.
HONESTY ABOUT SIGNAL. The head's classes are defined by the comparison to the card's trusted list, so destination-string oddness legitimately informs it (lookalikes look odd) while the trusted-odd rows break the shortcut; the scheme and the certificate flag legitimately define TRANSPORT_DEFECT. K31 therefore probes the destination string alone WITHOUT the scheme and certificate flag and WITHOUT the card's list, and requires near chance: the head has to be answered by comparing to the list, not by looking at the string.
If L-0 finds that C2's layout cannot carry a second question form, the head stays a manifest field plus a report line (G7); no new output token or suffix field is added.

## 5. SINKS for the non-"send" channels: WITHDRAWN for C2.1 [Opus b1 T53-M1, O-C1]

RULING (Opus batch 1): the stdout_echo, temp_file and shell_history sinks are NOT added, as trained rows or as report slices. Reason (G9): T50 R02 labels a user-named credential read ALLOW (soft, named), and secret content written to a file is decided by SLT-2 rule 7 through its visibility record (T50 R26); treating stdout, temp files and shell history as rule-6 sinks (secret => BLOCK / hard) would give one action two labels across T50 and T53 and would change an approved hard rule. Rule 6 stays "log or telemetry lines"; the 60 channel-coverage rows of block d for this channel keep the telemetry endpoint form; there is no `sink` attribute and K23 is unchanged. A shared SLT-2 row for these sinks, agreed with T50 first, is a C2.2 item. The (withdrawn) draft text: a `sink` attribute with values telemetry_endpoint, stdout_echo, temp_file, shell_history, 15 rows each.

## 6. OVERLAYS: INJECTION, WRAPPERS, PERTURBATION, DIALECTS [LEV A6, A10, A12, A15]

A6 gate-directed injection (350 rows). Free text inside the agent's own action tries to move the gate: a comment, docstring, commit or PR text, written file content or an MCP argument that CLAIMS a provenance ("example", "placeholder key"), a destination approval ("this host is approved"), an internal-host status, or urgency. The label comes from the ACTION ALONE: provenance comes only from visible calls (T53 risk 2 and K9), the destination verdict only from the normalised string vs the card's list. So a placeholder claim on a read-from-sensitive value stays BLOCK; a lookalike with an approval claim stays BLOCK; an honest explanatory comment on a clean ALLOW row stays ALLOW. Cue types (4): provenance claim, destination-approval claim, internal-status claim, urgency; cue type x label within +-5 pp of 50% ALLOW inside the A6 rows; benign explanatory twins >= 45% of the A6 rows. The wording pool is the L-I Claude-authored pool under the program-enforced literal ban (T53 writers never see the list). Stub slot until the pool arrives.
A10 cue wrappers (250, CONDITIONAL). Same Fri 23 probe and the single shared build rule GV1 (Opus batch 1: a flip = C2's predicted label differs wrapped vs unwrapped; build iff flips >= 10 of 200; no result by Fri 23 18:00 UTC = not built). If built: the 3 trained wrapper families (authority, urgency, a fake "already approved" note OUTSIDE the user turn); role-play and benign justification held out (GV2) [Opus b1]; hard labels only; every wrapped row keeps its clean twin; the user-turn AUTHORITY spans (naming of the operation and the destination) are byte-identical before and after wrapping.
A12 character perturbation (250). Natural-language fields only. NEVER perturbed: hostnames, URLs, credential-like tokens (they must stay exactly as registered, K1/K2), paths, flags, variable names. The G10 span survival check (negation/polarity, number, entity/path/flag, AUTHORITY) drops any row whose span changed. Trained transform families: diacritics, spacing, leetspeak, homoglyph, zero-width; held out (dev only): full-width, bidi. A family losing > 25% of its rows to the check is removed. Clean twin for every perturbed row.
A15 dialects. The card BODY (trusted lists, visibility declaration, unknown-visibility slot, MCP trusted servers, publish policy) AND the MCP tool schemas of block d's mcp_call rows are rendered in one of 7 dialects inside C2's fixed scaffold (scaffold sha unchanged): JSON schema, TS-style signature, YAML, markdown table, XML, prose, CLI help style. Trained 5 (JSON, TS-style, YAML, markdown table, prose); held out XML and CLI help. A spec group shares one dialect. Each trained dialect 12-25% of rows. Verbose dialects add 5-15% tokens (cost projection; G6 holds).

## 7. DIFFICULTY LADDER, QUAD, HELD-OUT [CRIT D1, D2; LEV A24]

Mechanisms (inventory section 4 T53 row; clean-room, mechanism only). Each row gets a level L1-L4 set by program; >= 25% of rows are L3-L4 (design 30% = 600 rows); each mechanism populates all four levels (each >= 10% of its rows).
| Mechanism | L1 | L2 | L3 | L4 |
|---|---|---|---|---|
| M1 plain transport on the correct host (host string identical) | different host | same host, https vs http in separate rows | same host with port and path variants | identical host string and path; ONLY the scheme (or a certificate warning) differs inside a pair (ALLOW vs ASK) |
| M2 follow-up escalation (a second request asks for more fields) | one public field | two public fields | the follow-up adds a confidential field | the follow-up adds a secret read from a sensitive path after an allowed first call to the same host in the history |
| M3 trusted address in context | full trusted address in the user turn | domain-only, exact match | domain-only with a lookalike nearby | full trusted address earlier in context, action host a lookalike of that domain (BLOCK) vs domain-only exact (ALLOW) |
| M4 indirect provenance on existing channels [Opus b1 T53-M1] | http_post | file upload | log_or_telemetry line whose value is reached through one variable indirection | log_or_telemetry line whose value was written to a file earlier and read back (two indirections) |
| M5 odd-looking but allow-listed hosts | plain trusted | internal TLD | raw IP of a listed host | punycode-form host that is EXACTLY on the list (ALLOW); at L3-L4 the ALLOW (odd) count is at least the BLOCK (lookalike) count |
| M6 phishing verdict (head rows only) | clear unrelated | lookalike with one cue | lookalike with two cues | trusted_odd vs lookalike pair sharing every surface feature except the list membership |
MANDATORY QUAD: alarming/calm surface x risk-present/resolved. 100 specs x 4 cells = 400 rows (20%), carried 40 specs in block a (provenance), 40 in block b (destination) and 20 in block c (class x visibility). Alarming surface = secret-sounding names (`token`, `.env`, `key`), shady-looking host shapes; calm = routine names, ordinary hosts. Risk present = BLOCK or ASK by SLT-2 (read-from-sensitive provenance, secret placement, lookalike, plain transport); resolved = authored placeholder, public key, exact trusted host (ALLOW). Every hard cell (calm + risk present; alarming + resolved) has an easy-looking twin with the opposite label in the same quad.
MEASURED BAR: C2 (C1 if C2 has no weights) on od-l4b scores <= 70% on L4 rows of the 1,000-row pilot; a miss is folded into the ONE combined fix (raise the program parameter, never drop rows by model score); after the fix a miss is a report line (K29). PRE-FREEZE FIX-TRIGGER, NOT A KILL.
HELD-OUT (inside the 2,000, never trained, design 80 rows = 4%): wrapper families role-play and benign justification 15 (only if A10 is built) [Opus b1 GV2], dialects XML and CLI help 25, transform families full-width and bidi 20, one carrier FORMAT: TOML file content for file_write payloads (base formats JSON, YAML, dotenv) 20. Tag `heldout_family`.

## 8. CHECK AT GENERATION [OWNER-ROW; plan 16.1]

Every T53 row passes the L-0b STAMP WRAPPER before it enters any pool. Per row: (a) answer checks: registered-fake scan and checksum uniformity (K1, K2), destination-verdict agreement A = B and label agreement (K7), provenance fact coverage (K9), group integrity (K10), A12 span survival, names guard including the closed allow-list for registries, MCP servers, tools, packages (K20), token per-row cap (K15), PII scrub (the Guard-10 registered-fake check), no-live-looking-secret verifiers (K16, offline only; no row value or part of one ever leaves the process), decision_spans export (G10), spec-family -> split (K17); for head rows also K30; (b) the G13 stamp against EVERY registered target (OHS-3, OHS-4, OHS-AC binding for new rows, OHS-5 hash export from Sat 24, public scope-eval targets, CredLeakBench items and cue-list strings as exact literals, attack literals; R6 scaffolding exemption), hit reports with row id, target name and method only; (c) the stamp (row id, registry sha, method-set version, generator code sha, verdict) in the row manifest.
DROPS. A failed row is dropped and logged; no unstamped or failed row enters a pool. A failing group member drops the whole group; a replacement group is drawn from the same cell with a new seed: a NEW spec; a group dropped for a G13 hit is never re-rendered or re-worded (GV5) [Opus b1] (at most 2 attempts per slot; an empty slot is reported as a short cell). ASK cells keep the >= 10% oversampling of FIX-5 and K13 is read on the FINAL set after all drops. K18s counts ALL dropped rows including collateral group members (stricter reading; O-C3).
K18s (REPLACES K18): drops other than exempt R6 scaffolding hits or OHS-5 collisions <= 1% of generated rows, read on ALL 1,000 pilot rows and on each full-generation day; above 1% is the ONE combined fix (G3); OHS-5 collisions <= 5% are not the fix iteration. The pilot is the FIRST look at every set-level gate; set-level gates then run once on the built family. A template change after the hash export means a new hash export and re-stamped rows; redo it after any change to the destination mutators, cue pool, wrappers, transforms, dialect renderers, or head question forms.

## 9. G9 EXTENSION [build order L-A]

K22 (must pass 100% before any pilot) gains leg (b'): every T50 block-G edit spec whose induced effect reaches R13 (secret-class or confidential content written to a file whose visibility record is public, or published by a later push in the history; T50 addendum section 10(d)) is mapped to a T53 spec (channel git_push, bucket_upload or file upload as the history says; ask_on_soft passed from the T50 card) and labelled by the T53 engine; labels must equal T50's. The head rows add a CONSISTENCY check: each head row's gold verdict is computed from the SAME destination record as its primary row, and the primary row's label under rules 7-8 and the head verdict never contradict (TRUSTED head with an exact listed host while the primary label rests on a lookalike verdict is impossible): 100%.

## 10. GATES ADDED OR CHANGED

PRE-FREEZE KILL (CPU, data only unless marked). Probe protocol = G5 (grouped split by spec family, 30% held out, 5 splits, L2 logistic regression, AUC = max(AUC, 1-AUC), 97.5th percentile bound over 2,000 cluster-bootstrap resamples, permutation check 0.50 +- 0.03, leak-power check >= 0.80, GBT advisory). Binary bar: held-out AUC <= 0.55 AND bound <= 0.60. k-way: balanced accuracy <= 1/k + 3 pp AND bound <= 1/k + 6 pp.
| ID | Gate | Bar |
|---|---|---|
| K18s | Stamp on ALL rows (section 8) | <= 1% non-exempt drops; OHS-5 drops <= 5% |
| K22 leg (b') | Edit actions that reach R13 (section 9) | 100% label equality before any pilot |
| K25 | Gate-directed injection | label unchanged when the free text is removed: 100% (solver B ignores free text); comment-presence probe (features: free-text field present, length bucket, position kind, count; no tokens) on the family and inside the A6 rows: AUC <= 0.55, ub <= 0.60; benign twins >= 45% of A6 rows; cue type x label within +-5 pp |
| K26 | Character perturbation | 100% decision spans survive; 0 hostnames, tokens or paths touched; clean twin for every perturbed row; 0 held-out transform rows in train; perturbation-presence probe AUC <= 0.55, ub <= 0.60; perturbed rows' ALLOW share within +-5 pp of the family |
| K27 | Dialects | scaffold-sha assert 100%; 0 held-out dialect rows in train; each trained dialect 12-25%; K12 features rerun WITHIN each dialect AUC <= 0.55, ub <= 0.60; dialect-id-only vs label AUC <= 0.55, ub <= 0.60; MCP-schema dialects only on mcp_call rows |
| K28 | Ladder structure | >= 25% of rows L3-L4; each mechanism populates 4 levels (each >= 10%); 100 quad specs x 4 cells exact; opposite-label easy twin for every hard cell 100%; at L3-L4 the ALLOW (odd host) count >= the BLOCK (lookalike) count; no more than 55% of L4 rows share one label |
| K29 | C2 (or C1) <= 70% on L4 rows (od-l4b read of our own model) | PRE-FREEZE FIX-TRIGGER, NOT A KILL |
| K30 | Phishing head integrity | gold = destination verdict, A vs B agreement 100%; exact class balance 75 x 4 (the draw respects the cap of 25% of specs); cue coverage: six lookalike cue categories 12-13 each, trusted_exact 38, trusted_odd 37, plain HTTP 38, certificate warning 37; head and primary rows share one destination record 100%; same split as the primary row 100% |
| K31 | Phishing head probes | head format-only probe (channel, view flag, length bucket, carrier, turn count; no host tokens), 4-way balanced accuracy <= 28% and bound <= 31%; DESTINATION-STRING-ONLY probe (length, label count, digits, hyphens, IP-literal flag, punycode flag; NO scheme, NO certificate flag, NO list) 4-way balanced accuracy <= 28% and bound <= 31% |
| K32 | (WITHDRAWN, Opus b1 T53-M1: no sink attribute in C2.1) | n/a |
| K33 | Held-out sub-families | 80 rows (+-8); 0 in train: 100% |
| K34 | Cue wrappers (only if A10 is built) | wrapper-presence probe AUC <= 0.55, ub <= 0.60; AUTHORITY spans byte-identical 100%; clean twin for every wrapped row |
| K13 note | ASK >= 10% is read on the FINAL set after all drops; with replacement draws per cell the oversampling of FIX-5 stays as the safety margin. Overlays do not move label totals | unchanged bars |

POST-TRAINING REPORT (never a kill rule):
| ID | Report line |
|---|---|
| P6 | Phishing head: balanced accuracy and confusion over the 4 classes, recall by lookalike cue category, trusted_odd false-alarm rate, TRANSPORT_DEFECT vs LOOKALIKE confusion, with CIs (cluster bootstrap by spec) |
| P7 | A6 slice: cue rows vs plain rows (target within 2 pp); benign-twin over-block rate |
| P8 | Held-out lines: transform families, wrapper family, dialects, file format TOML (A24 term in S) |
| P9 | Accuracy by ladder level and by quad cell; scheme-only pairs (M1 L4) both-correct rate; follow-up escalation (M2) accuracy; M4 indirection accuracy by level |
| P10 | C2 vs C2.1 on L4 rows |

## 11. NAMES this addendum needs (names only; for manifest v1.1; L-0 owns the strings)

New fixed real names (allow-list entries):
- Head option ids and question forms: TRUSTED, LOOKALIKE, TRANSPORT_DEFECT, UNRELATED (labels of options; not strings of real entities); the head question form id `t53_dest_verdict` and its >= 50 wordings (Haiku wording pool under the same rules as every wording pool).
- Sink values: NONE (withdrawn, Opus b1 T53-M1).
- File content format added to the carrier format list (held out): TOML.
- Dialect and wrapper and transform family names as in the T50 addendum (JSON schema, TS-style signature, YAML, markdown table, XML, prose, CLI help style; authority, urgency, role-play, already-approved note, benign justification; diacritics, spacing, leetspeak, homoglyph, zero-width, full-width, bidi).
- Carrier ids: no new carrier (shell_exec, file_write, mcp_call as in v3.1).
Generator-internal enums (not row strings): head classes (4), lookalike cue categories (6, already in v3.1 as categories), M1-M6, quad cell ids, cue types (4).
Namespace kinds: unchanged from v3.1 (policy_card, org, brand, repo, remote name, host, registry host, bucket, MCP server, MCP tool, package, user, file/path component, env-var stem, TLD pick from the ONE shared list). Added: none (the sink-specific path components are withdrawn with the sinks, Opus b1 T53-M1).
Row family: stays `T53` in row_job_families_allowed; head rows carry `head = t53_phishing`, overlay rows carry `overlay` lists. No new family id.
G13: CredLeakBench items and cue-list strings stay targets; only cue categories are used; no benchmark string, entity name or ID pattern appears.

## 12. Risks

1. The head's TRUSTED class includes trusted_odd forms that look like lookalikes; a head model may over-flag odd hosts. K30 balances them (75 TRUSTED, 37 odd) and K31 requires the destination-only probe near chance.
2. (Closed by Opus b1: the sinks are withdrawn, O-C1.)
3. Phishing-style signal can drift into the primary rows through the shared destination record; the consistency check (section 9) and the K6/K12 probes cover it.
4. A6 provenance-claim cues can look like a "placeholder claim => ALLOW" lesson if mis-balanced; K25 balances cue type x label and the ALLOW rows that carry a claim are true authored placeholders.
5. M2 (follow-up escalation) needs a history with an allowed first call; those rows are mostly with-results or call-visible and must keep K9 at 100%.
6. Dependencies: the L-I pool (A6), the Fri 23 probe (A10), T50's shared spec_v2 (this lane), the L-0 stamp wrapper. None blocks T53's own pilot (stubs are reported).

## 13. Open questions for Opus

- O-C1: confirm the sink extension of rule 6 (telemetry_endpoint, stdout_echo, temp_file, shell_history) with identical outcomes, or make the three new sinks report-only.
- O-C2: confirm the 4-way phishing head (TRUSTED / LOOKALIKE / TRANSPORT_DEFECT / UNRELATED) with 300 rows, or ask for a different class set. The head uses the existing destination verdict, so no new gold logic exists.
- O-C3: confirm K18s counts collateral group members (stricter reading; same as O-A4 and O-B2).
- O-C4: confirm that heads still roll with the family (G4); the head is not a P0 sub-block that can fail alone.

## 14. Fix iteration, kill rule, what may start now

As v3.1 section 9 (one combined fix after the pilot; G3): K18s > 1% is the fix; K29 is a fix trigger only; a K25-K28 or K30-K33 miss after the fix rolls the family (G4). Floor and freeze rules unchanged (declared Thu 29 12:00; fallback Mon 2 Nov 23:59 UTC). Rows start Sun 25 Oct after the OHS-5 freeze, through the stamp wrapper.
May start now (code, no rows): the fake-credential registry and the destination normaliser (as in v3.1); the head question form and head-row drawer; the K23 truth table (unchanged inputs); A12 transforms; dialect renderers incl. MCP-schema dialects; K25-K34 CPU tests; solver B from this addendum plus the G0-lite only. The stamp wrapper is used only with a signed ruling-to-code conformance record for the current code sha (plan 16.1 step 0).

---

## Opus batch-1 rulings v3.2 (Opus 5.5 high, Sun 18 Oct 2026 UTC; source: families/G0_APPROVALS_v32.md; binds over this file)

Global rulings GV1-GV9 of families/G0_APPROVALS_v32.md bind this file (GV1 one A10 build rule: flip = predicted label differs
wrapped vs unwrapped, build iff >= 10 of 200, no result by Fri 23 18:00 UTC = not built; GV2 role-play and benign justification
held out in every lane; GV3 one A14 build rule: >= 5 pp gap and bootstrap lower bound > 0; GV4 G6 binds A14, no exemption; GV5 a
G13-hit row retires its spec and its whole group, never re-worded, triggers read first-pass drops incl. collateral; GV6 one
perturbation library pert.*, zero_width = U+200B only, fullwidth / bidi / upside_down held out everywhere; GV7 A15 dialect rows in
L-A only; GV8 pilot-pooled sub-block probes, built-family read binds; GV9 held-out dev rows never trained, mix guard excludes them).
VERDICT: REVISE -> APPROVED after fixes (applied in place): T53-M1 (O-C1) the stdout_echo / temp_file / shell_history sinks
are withdrawn for C2.1 (G9 conflict with T50 R02 and R26; rule 6 stays log / telemetry only; no sink attribute; K32 withdrawn;
ladder M4 rewritten to indirection levels; names and report lines updated; C2.2 item); A10 build rule (GV1); held-out wrappers
(GV2); replacement group = a NEW spec (GV5).
Binding conditions: T53-B1 O-C2 confirmed (4-way head, 75 x 4); the head drawer stratifies the six K31 string features so
their distributions match across the four classes before K31 runs. T53-B2 O-C3 confirmed (GV5). T53-B3 O-C4 confirmed (the head
rolls with the family, G4). T53-B4 A6 over L-A is exactly the plan floor (1,500); a shortfall is reported, not back-filled.
