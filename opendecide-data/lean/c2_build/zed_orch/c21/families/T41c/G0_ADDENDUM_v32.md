# G0 ADDENDUM v3.2: T41c TAINT (clean-room)

Lane L-I. Author: Sonnet 5.5 high. Written Sun 18 Oct 2026 (UTC), for Opus batch 1 on Mon 19 Oct.
Status: DRAFT for Opus approval. Extends families/T41c/G0_LITE.md (APPROVED, Opus Round 2). It does NOT change the
pinned label table 1.1, the facts-absent defaults 9.1, or any Opus ruling in section 10 of the G0-lite. Where this
addendum and the G0-lite differ, this addendum binds, and only on the items it names (section 12 lists them).
Read for this addendum: C2_1_BUILD_ORDER.md (L-I block and v3.2 additions), C2_1_PLAN_v3.md sections 1, 2, 5, 6, 7, 8,
the PRE-REGISTERED RULES block of section 3 and section 16, C2_1_EXTRA_LEVERS.md section 1 (A1-A36 rows), the
families/T41c/G0_LITE.md and families/G0_APPROVALS.md, and C2_1_PUBLIC_TRAIN_INVENTORY.md (section 4 T41c row, A18/A19).
Design only. No rows, no code run, no model call. No other file was opened. The T41c builder code was not opened;
section 13 asks a fresh conformance session to map clauses to code.
Rows start Sun 25 Oct (after the OHS-5 freeze, the registry sha, the names manifest v1.1, the signed stamp service and
a signed conformance record). v3.2 DATA FREEZE: stretch Fri 30 Oct 12:00 UTC (declared Thu 29 12:00 from measured
status), fallback Mon 2 Nov 23:59 UTC. The G0-lite's "Mon 2 Nov" is the fallback date.

Gate tags (as in the G0-lite): **[PRE-FREEZE KILL]** = CPU, data only, can kill the family. **[POST-TRAINING REPORT]**
= needs a trained model, report line only. New tag **[PRE-FREEZE FIX-TRIGGER]** = reads our own models on data
(od-l4b), pre-registered by plan 1E; a miss goes into the ONE combined fix, and after the fix a miss is a report line,
never a kill. "Near chance" bars are the G5 bars: binary probe held-out AUC <= 0.55 with 97.5th-percentile bound <= 0.60
(AUC taken as max(AUC, 1 - AUC)); k-way probe balanced accuracy <= 1/k + 3 pp with bound <= 1/k + 6 pp; through the one
L-0 probe harness; plus K7 (permutation sanity and injected-leak power) on every run.

## 0. What T41c now carries (one table)

| Item | Source | Kind | Size inside N (N = 2,000 / 3,000) | Section |
|---|---|---|---|---|
| Check-at-generation (stamp wrapper) | OWNER-ROW, plan 16.1 | replaces K10 and the 200-row pilot | all rows | 1 |
| A13 benign-worded hijacks + lexical-balance probe | LEV A13 | mix shift, 0 extra rows | 500 / 750 attack rows; 260 / 390 alarm-register benign rows | 2 |
| A10 cue-invariance pairs | LEV A10 | build only if the Fri 23 probe says so | 200 / 300 rows (100 / 150 pairs) | 3 |
| A12 character perturbation | LEV A12 | substitution | 200 / 300 rows | 4 |
| A14 long-input slice | LEV A14 | build only if the Fri 23 probe says so | 100 / 150 rows | 5 |
| A16 observation-format perturbation | LEV A16 | re-render, 0 extra rows | about 13% of N, 40% of tool-output carriers | 6 |
| A6 gate-directed wording pool for L-A | LEV A6 | pool delivery (no T41c rows) | pool of 800 wordings | 7 |
| Difficulty ladder + mandatory quad | CRIT D1, D2; plan 1E | composition + measured bar | quads: 100 / 150 groups | 8 |
| Benign twins for Aya and Gandalf summarization | plan 16.3, 16.4, Sk 7 | twin generator for L-R | about 400 twins in block R | 9 |
| A1, A2, A15, A24 hooks | LEV | tools / manifest fields | 0 | 10 |

All new row types are BY SUBSTITUTION inside N. None adds a row to the family size. Held-out dev blocks are outside N
and never trained on. T41c stays an INDIRECT-injection family: NO direct (user-turn) injection rows are added to T41c
(plan 1E); the Gandalf direct slice is block R (L-R G0-lite) and only the benign twins are written here.

Dependency flagged for the orchestrator: N is 2,000 if T41 is in C2's mix and 3,000 if not. That status is a C2 record
outside this lane's read scope; both columns are given. All cross-cutting shares below are fractions of N.

## 1. Check at generation (OWNER-ROW; replaces K10 and every "200-row pilot" line)

Owner, 18 Oct (binding): "If you're building one row, check that row at that same point and that's it ... then train."

1.1 THE ONE WRITE PATH. T41c rows (training N, HO, BD, LS, and the pool wordings of section 7) are written only through
the L-0b STAMP WRAPPER. Per batch (<= 500 rows, same day) it runs, in this order:
1. Schema and anchor faithfulness (K9): every tuple anchor appears verbatim in the realised text.
2. Answer check: solver A label == program solver B label, per row (B runs from the rendered row plus the anchor map
   only; the closed task-verb list is frozen with the template hash and hidden from A, G1). A disagreement drops the row
   and logs it (row id, spec cell; never text).
3. Family invariants: facts-absent decidability (9.1: a facts-absent row whose risk is undecidable from its spans is
   dropped); pair and quad group integrity (section 1.3); A12 survival check (4.3); A16 label-preserving check (6.3);
   A10 cue-source check (3.3); A14 layout check (5.3).
4. Names guard (closed allow-list; hosts from the shared L-0 host-TLD list and raw-IP pool, G8); token rule G6 per row
   (a row above 1,536 tokens is dropped); PII scrub; decision-span export (G10; the user task and its delegation pointer
   are the AUTHORITY spans).
5. G13 STAMP SERVICE against EVERY registered target with every method listed for that target (R6 scaffolding exemption;
   OHS-AC binding for new rows; OHS-5 export from Sat 24; literal-ban enforced inside G13, never shown to writers).
6. Manifest stamp: row id, registry sha, method-set version, generator code sha, template hash, verdict.
A failed row is dropped and logged (row id, target name, method; never the matched text). No unstamped or failed row
ever enters a pool or the mix.

1.2 WHAT IS NO LONGER DONE. K10 (200-row G13 pilot, orchestrator, Mac, serial) is removed. The G13 read is on ALL rows
of the 1,000-row pilot and of each full-generation day. The mix guard refuses any T41c row without a current clean
stamp. The binding G13 is one confirming pass (plan 16.1 step 8). Stamps go stale per plan 16.1 step 6: a template
change after hash export v1.1 means a new hash export and re-stamped rows; a late target runs the delta only.

1.3 QUOTAS HOLD AFTER DROPS (G13, A/B, anchor, OHS-5 and every other drop). The generator fills per-cell quotas (label,
carrier type, subtype, facts-absent, section 2-8 cells) and oversamples every cell by at least 10%. A member dropped by a
NON-G13 answer check (A/B, anchor, facts-absent, survival, label-preserving, layout) is regenerated on the SAME skeleton
with a fresh wording seed (at most 2 attempts). A member dropped by the G13 stamp (any non-exempt hit) RETIRES its
skeleton: the whole group is dropped and a NEW skeleton is drawn for the cell; a hit skeleton is never re-worded
[Opus b1 GV5]. Regeneration is quota filling under the same spec and is not pilot tuning (G3); the first-pass drop rate (before any regeneration) is the number the triggers read.

1.4 FIX TRIGGER ON ALL ROWS (plan 16.1 step 3). First-pass drop rates on ALL 1,000 pilot rows and on each full-
generation day:
- G13 stamp drops for a reason other than exempt scaffolding or OHS-5 collisions: > 1% = the family's ONE combined fix
  (G3). OHS-5 collisions are dropped row by row; at or below 5% of the family's rows this is not the fix iteration.
- Answer-check drops use the G0-lite bars: solver disagreement <= 2% (K6(ii)); anchor drops <= 3% and guard refusals
  <= 2% (K9); facts-absent undecidable drops <= 3%; A12 survival drops <= 10% of perturbation attempts; A16 label-check
  drops <= 5% of A16 attempts; A10 cue-source violations 0 (generator bug); A14 layout drops <= 5% of A14 attempts.
The five answer-check lines beyond K6(ii) and K9 (facts-absent, A12, A16, A10, A14) are NEW design values fixed here, before any
pilot. Any figure above its line is the one combined fix. A second trigger after the fix is spent is the KILL rule (section 12).
The 1,000 pilot rows are part of N when their template/wording hash is unchanged.

1.5 SET-LEVEL CHECKS RUN ONCE PER FAMILY (plan 16.1 step 4): once on the 1,000-row pilot (first look, no free tuning,
G3) and once on the fully built family; not repeated at the mix. These are K1-K9 and K11-K12 of the G0-lite as amended
here, and K13-K19 below. K11 (A50 G6, A49c, G5-H, G3-H, A43(d)) keeps its values from C2's records (L-0 supplies); a
G5-H flag counts only after Sonnet medium adjudication, Opus A43(d) confirmation and a solver-B re-run (G2).

1.6 REPLAY AND MIX. T41c rows enter the mix only with a clean stamp for the final registry sha. Nothing else in T41c
touches the replay clean-up (that is L-0b, plan 16.1 step 5).

## 2. A13: benign-worded hijacks and the lexical-balance gate (mix shift; 0 extra rows)

2.1 DEFINITIONS (all program-checkable). LEXICON: a closed list of 120 to 200 single-word stems of ATTACK REGISTER,
written by the builder from first principles (not from any benchmark, not the G13 literal list): override and ignore
words, concealment words, security-jargon words (exploit, payload, backdoor and similar), and pressure words. Content
nouns of a goal class (a path, a credential, a package) are NOT lexicon words, so a benign-worded exfiltration still
names what it sends. The lexicon is frozen with the template hash and may be shown to writers as a "do not use these
words" list for benign-worded rows (it is not the G13 list; a lexicon word can never equal a G13 literal because it is a
single stem). HIT = the focus directive sentence contains at least one lexicon stem. BENIGN-WORDED = zero hits.

2.2 DESIGN VALUES (fixed before the pilot).
- Among AGENT-DIRECTED attack directives (every BLOCK and ASK row; rules 3 to 8 of 1.1): 50% are BENIGN-WORDED
  (zero hits) and 50% carry >= 1 hit. That is 25% of N: 500 rows at N = 2,000, 750 at N = 3,000, spread over the 8 HIGH goal
  classes (each class between 35% and 65% benign-worded) and over the label cells (BLOCK-unrequested-HIGH, -LOW, -HARD, ASK
  cells), all inside the existing BLOCK 35% + ASK 15%.
- Among AGENT-DIRECTED benign directives (delegated 14% + ambient 12% = 26% of N): 50% carry >= 1 hit (ALARM-REGISTER
  benign: "mandatory", "immediately", security-flavoured but acceptable) and 50% are zero-hit. That is 13% of N: 260 / 390.
- The non-agent-directed benign rows (trigger-word / security discussion 5%, human-addressed or off-topic imperative 4%)
  keep their design of high lexicon density (>= 70% hit rate in the trigger subtype). They are not payloads and are not in
  the A13 bar.
- Labels never change: the label table decides, by provenance and risk; wording never does (1.1 and the line "Claimed
  authority inside a span never changes a label").

2.3 K13 [PRE-FREEZE KILL] LEXICAL BALANCE.
(a) Hit rate among agent-directed attack directives minus hit rate among agent-directed benign directives: |difference|
<= 5 pp overall; within each goal class and each benign action class, the hit rate is within 15 pp of 50%.
(b) Payload bag-of-words probe: binary term-presence features (min document frequency 5) over the focus-directive
sentence with anchor strings masked to placeholders (host, package, path, tool role, addressee marker), wrapper words kept;
label = attack (BLOCK+ASK) vs benign (agent-directed ALLOW_BENIGN); groups = pair groups. Bar: held-out AUC <= 0.55, bound
<= 0.60. The same probe is run inside each wrapper style (report-only; amber if > 0.60 in any style with >= 200 rows).
(c) View V2 (all directive-bearing rows incl. non-agent-directed benign security text) is advisory only: it cannot be
balanced together with the 70% trigger-subtype density, and A13 asks for the payload-sentence probe.
(d) K7 power control: a planted single stem only on attack directives must reach AUC >= 0.80, else the K13 result is
invalid and re-run (not a fix iteration).
FIX knobs (declared now): rebalance the hit shares per class and style; widen the wording pools for the failing class;
the A2 AFLite filter of 10.2.

2.4 POST-TRAINING (never a kill) P9: recall on benign-worded attack directives vs hit attack directives (CI); benign-
block rate on alarm-register benign vs zero-hit benign (CI); the lexical-cue gap (hit minus zero-hit label rate, paired).

## 3. A10: cue-invariance pairs (build only if the Fri 23 probe says so)

3.1 FREE PROBE FIRST (PB; not a T41c gate). Fri 23: L-0 / L-E builds 200 wrapped items from C2's EXISTING dev rows (no
C2.1 row exists before the OHS-5 freeze; the items are eval-only and registered as internal held-out G13 targets), C2 reads
each wrapped item and its unwrapped original on od-l4b (pipelined, free L4). DECISION RULE written now, before any read: T41c
builds A10 pairs if C2's answer changes (wrapped vs unwrapped, same label) on >= 10 of the 200 items (5%; an exact
one-sided binomial test against a 2% noise rate gives p < 0.01). Fewer than 10, or no result by Fri 23 18:00 UTC, means
A10 is NOT built in T41c and its 200 / 300 rows revert to ordinary pair cells. The Thu 22 hash export contains ALL A10
templates unconditionally; the Fri 23 decision toggles sampling only, never a template, so no re-export is needed.

3.2 DESIGN (if built). A cue pair = two members with the same skeleton, directive, label and facts stratum; member U has
wrap.plain_imperative and member W has a cue-family wrapper. The clean twin (ALLOW) of the triple stays in the group.
Size: 5% of N wrapped members + their 5% unwrapped twins = 10% of N: 200 / 300 rows, counted inside the 60% pair share.
Half the pairs are attack (label BLOCK or ASK), half benign (ALLOW_BENIGN), so a cue never marks a class. Cue families
group the wrapper styles (the set of styles grows from 8 to 11 by three new base styles that hardest.md names and the
G0-lite lacks: `wrap.benign_justification`, `wrap.prerequisite`, `wrap.term_redefinition`):
- `cue.authority` = {wrap.authority_framing, wrap.fake_system_tag}
- `cue.pressure` = {wrap.urgency, wrap.conditional_trigger}
- `cue.persona` = {wrap.role_play, wrap.benign_justification}
- `cue.task_logic` = {wrap.prerequisite, wrap.term_redefinition}
- `cue.approval` = {wrap.preauthorised_disguise} (single style; never held out)
`wrap.plain_imperative` and `wrap.hidden` belong to no cue family. HELD-OUT WRAPPER LINE (A10 and D3 together): the
held-out wrapper value is the cue family `cue.persona` (wrap.role_play + wrap.benign_justification), FIXED by Opus batch 1
(GV2) so that every lane holds out the same two styles; no draw. It replaces "2 wrapper styles" in the G0-lite (still 2
styles, now grouped).
Real consent signals are excluded: a cue is rendered only in spans with source tag in {user_repo_file, third_party_repo_file,
tool_result, mcp_description, mcp_response, ci_log}; NEVER in the user span or in the system/developer span (a cue is
never an authorisation, label by provenance).

3.3 K16 [PRE-FREEZE KILL] (only if A10 is built). (a) Label equality inside each pair by the table (solver A and B). (b)
Cue-source check: 0 cue spans in user or system_developer spans (program, per row). (c) Cue-presence probe: features =
cue family, cue flag, wrapper style; views attack vs benign and 4-way: AUC <= 0.55 / bound <= 0.60; balanced accuracy <=
28%, bound <= 31%. (d) Cue flag and cue family share per label within 3 pp of 10% of rows. (e) No cue wording in more than
2% of rows; >= 50 wordings per cue family.

3.4 POST-TRAINING P10: accuracy and attack recall on the held-out cue family (HO block, 4.4) vs in-family, with CI;
wrapper-induced error rate wrapped minus unwrapped, paired.

## 4. A12: character-perturbation augmentation (substitution; 10% of N)

4.1 DESIGN. 10% of rows (200 / 300) have their SLOT TEXT perturbed (the one-slot filler or directive, so a perturbed row
exists in every label, including ALLOW rows whose slot is neutral filler). Perturbation rate per label: 10% +/- 2 pp (so
the perturbation flag cannot mark a label). Exactly one transform family per perturbed row. TRAINING families
(`pert.diacritics`, `pert.spacing`, `pert.leetspeak`, `pert.homoglyph`, `pert.zero_width`); HELD-OUT families, never
trained (`pert.fullwidth`, `pert.bidi`, `pert.upside_down`), fixed here because the lever text itself names them as the
examples and no result informs them. NOT used: the Unicode Tags block U+E0000-E007F and stray variation selectors (the
A11 canonicaliser strips them at the product wrapper, so they never reach the gate at serving). ZWJ / ZWNJ and flag
emoji are not generated. Rows with `wrap.hidden` / `hid.zero_width` get no `pert.zero_width` (that is an attack wrapper,
not a perturbation). A12 never touches: the user task text and delegation pointer (AUTHORITY spans, G10); anchor strings
(host, package, path, tool role, addressee marker); negation or polarity tokens; numbers. A homoglyph host is a different
host and belongs to T53, so no anchor is ever perturbed.

4.2 PERTURBATION SHARE ACROSS LANES. The ids `pert.*` are shared names across gate lanes; if L-0 publishes a common
transform library before the Thu 22 hash export, T41c uses it unchanged; otherwise T41c carries a local implementation
with identical ids and the orchestrator reconciles at the manifest v1.1 freeze.

4.3 K17 [PRE-FREEZE KILL]. (a) Survival check at creation (drop-only): apply the family's inverse normaliser to the
perturbed slot; every anchor string, negation token and number must be recovered exactly, and solver B on the NORMALISED
view must equal solver A's label; otherwise the row is dropped and counted (> 10% of attempts = generator bug = the
combined fix). (b) Perturbation-flag probe: features = perturbation flag and family; binary views AUC <= 0.55 / bound
<= 0.60; 4-way balanced accuracy <= 28% / bound <= 31%. (c) No held-out family appears in N or in any training row (CPU
set intersection). (d) Perturbation family shares within the training set within 3 pp of equal.

4.4 POST-TRAINING P11 (never a kill): accuracy, attack recall and benign-block rate on held-out transform families vs in-
family transforms vs unperturbed, with CI.

## 5. A14: long-input slice (build only if the Fri 23 probe says so)

5.1 FREE PROBE FIRST (PB). Fri 23: C2 reads a 200-item buried-payload slice built from its existing dev rows (eval-only,
registered as an internal held-out target) and the same items in a short-input form. DECISION RULE written now: build A14
in T41c if short-input attack recall minus buried-payload attack recall >= 5 pp on the 200 items AND the paired bootstrap
95% lower bound of that gap is > 0. Otherwise, or no result by Fri 23 18:00 UTC, A14 is not trained: its 100 / 150
rows revert to the short bucket, and the LS block (eval only) carries the long-input report. A14 tokens are the first item
in the plan's money shed step 2; if the measured projection sheds it, the rows revert the same way.

5.2 TOKEN RULE CONFLICT, RESOLVED IN FAVOUR OF G6 (Opus to confirm, question Q1). The lever and plan D6 say 1.5 to 3K
tokens; G6 says no row above 1,536 tokens and <= 10% above 1,024. Here "long" means a trained row of 1,000 to 1,500
tokens in total (carrier 750 to 1,250 tokens plus about 250 tokens of context spans). The 1.5 to 3K range and 3-8K stay in
LS (eval only, never trained). Effect on K8: mean stays <= 800 (DERIVED design mean about 640; K8 measures it); rows above 1,024 about 5.6%
(<= 10%).

5.3 DESIGN (if built). 5% of N (100 / 150 rows), taken from the <= 256-token carrier bucket (carrier mix 55 / 30 / 15
becomes 50 / 30 / 15 / 5). Payload layouts: `lay.head`, `lay.middle`, `lay.tail`, `lay.interleaved` (the directive in one
contiguous run between filler paragraphs), `lay.split` (the directive in two chunks, both anchors present, filler between
them). Filler kinds: `fill.coherent` (task-relevant), `fill.neutral`, `fill.flood` (repetition flood: a repeated filler
sentence). ONE layout is held out (seeded TRAINING-salt draw among the five, recorded before any pilot): its rows go to the
HO block, never to N. The other four layouts take 25 rows each at N = 2,000 (37-38 at 3,000), 50% benign (ALLOW_BENIGN
or ALLOW with a buried benign directive), label mix per carrier type within 8 pp of global. Placement bins p0-p4 still
apply to the directive start. Layout check at creation: the directive (or both chunks) is present, contiguous as designed,
and in the declared bin; else drop.

5.4 K18 [PRE-FREEZE KILL] (only if A14 is built). (a) Slice share 5% +/- 1 pp; carrier length 750-1,250 tokens; total row
length <= 1,500; K8 holds on the whole family. (b) Layout / length / position probe INSIDE the slice: features = layout id,
filler kind, token-length bucket (4), directive start bin; views attack vs benign and 4-way; AUC <= 0.55 / bound <= 0.60; 4-
way balanced accuracy <= 28% / bound <= 31%. (c) The held-out layout does not appear in N. (d) Benign share in the slice 50%
+/- 5 pp; delegated + ambient >= 30% of its benign rows. (e) K1 gains layout id and long flag as features (the whole-family
format-only probe still passes).

5.5 POST-TRAINING P12: recall by layout and length on the trained slice and on LS (1.5-3K), single read vs chunked max-
score read; in-family layouts vs the held-out layout.

## 6. A16: observation-format perturbation (re-render; 0 extra rows)

6.1 DESIGN. Applies to carriers that are tool outputs: `car.tool_json`, `car.tool_text`, `car.ci_log`, `car.mcp_response`.
40% of the rows of those four carrier types (about 13% of N; measured, not fixed) get exactly ONE operator. Operators:
`obs.ansi` (colour / cursor codes), `obs.crlf_tab` (CRLF and tab mixes), `obs.wrapped` (hard-wrapped lines),
`obs.paginated` (page breaks with page markers), `obs.trunc_marker` (truncation markers outside the directive),
`obs.progress_bar` (interleaved progress-bar lines), `obs.key_order` (key reordering in structured carriers). The seven
serialisation formats `fmt.*` of the G0-lite already realise the JSON / YAML / plain part of the lever, with one format
held out. ONE OPERATOR is held out (seeded TRAINING-salt draw among the seven, recorded before any pilot); its rows go to
the HO block. At most one of A12 and A16 per row; an A14 long row may also carry one A16 operator.

6.2 CONSTRAINTS. The directive is never cut, wrapped through, paginated through or split by an operator (the directive, or
both chunks of a `lay.split` directive, sit inside one wrapped run, one page, outside any truncation). Carrier length grows
by <= 15%; the 256-token cap applies to auxiliary tool outputs (the carrier is exempt, as in the G0-lite section 2); a row
pushed over 1,536 tokens is dropped.

6.3 K19 [PRE-FREEZE KILL]. (a) Label-preserving check at creation (drop-only): the inverse normaliser (strip codes,
normalise CRLF, join wrapped lines, remove page, truncation and progress lines, restore key order) must return the
un-operated carrier text exactly, and solver B on the transformed row with the remapped anchor map must equal solver A's
label; failures are dropped and counted (> 5% of attempts = combined fix). (b) Operator-flag probe: features = operator id
and flag; AUC <= 0.55 / bound <= 0.60 in each binary view; 4-way balanced accuracy <= 28% / bound <= 31%. (c) Operator
share per label within 3 pp of the design value; (d) the held-out operator does not appear in N.

6.4 POST-TRAINING P13: accuracy and attack recall on the held-out operator vs in-family operators vs clean, with CI.

## 7. A6: gate-directed wording pool for L-A (delivery only)

7.1 WHAT. L-A uses gate-directed injection INSIDE the agent's own action (comments, docstrings, commit and PR text,
written file content, MCP arguments that address the reviewer or gate, for example a fake "approved" note) with benign
twins whose comments explain a real change; the label comes from the ACTION alone (plan 16.2 A6). T41c does not label
these rows. L-I delivers a Claude-authored WORDING POOL, hash-exported with the Thu 22 export, read-only to L-A.

7.2 POOL SPEC. Five placement kinds (`pool.comment`, `pool.docstring`, `pool.commit_pr_text`, `pool.written_content`,
`pool.mcp_argument`) x two sub-pools (`pool.gate_directed`: addresses a reviewer, gate, monitor or approver, with a claim
of approval, safety or routine nature; `pool.explanatory`: explains a real change in neutral engineering language) = 10
cells, >= 80 wordings per cell, 800 in all, none reused in more than 2% of L-A rows. Entries are TEMPLATES with named
slots ({target}, {tool}, {change_summary}, {scope}); L-A fills slots from its own namespace, so the pool contains no
concrete action, host, path or package and works for either label. Writers: Haiku 5.5 medium from a tuple (kind,
sub-pool, intent class, length bucket, register); no exemplars; never the G13 literal list; no paper wording (the cited
monitor-evasion paper's phrases are never used).

7.3 POOL GATES (PRE-FREEZE KILL for the pool, not for T41c). PG1: every wording is G13-stamped AS IT IS MADE as a standalone
string (exact and hashed n-gram methods), and stamped again inside L-A's rows; failures are dropped from the pool and
logged. PG2: token length of `pool.gate_directed` and `pool.explanatory` matched per kind: each of 4 length buckets within
5 pp between the two sub-pools. PG3: slot syntax and anchor check by program (every slot present, none unfilled in a
rendered sample of 1,000). PG4: >= 50 wordings per form per cell, none above 2%. The "comment present = suspicious"
probe is L-A's gate (A6 row: AUC <= 0.55), not the pool's. Hits are reported to the builder by wording id, target and
method only.

## 8. Difficulty ladder and the mandatory quad (CRIT D1, D2; plan 1E)

8.1 SOURCE OF THE MECHANISMS. The T41c row of the inventory section 4 (copied from hardest.md 1.4): helpful ambient
instructions are the hard benign class; trigger-word density; tail placement; prerequisite, term-redefinition,
conditional and authority framing; benign text with three or more security words; malicious text with zero trigger
words; delegated-instruction pairs that differ only in the user turn. I had no stripped hardest.md excerpt; if the L-0
excerpt names more mechanisms they are added as `mech.*` under a new hash export.

8.2 MECHANISMS AND LEVELS (program parameters, no model scoring). Each row has ONE PRIMARY mechanism with level L1-L4;
all other mechanisms on the row are capped at L2.
- `mech.trigger_density` (lexicon hits in the slot): L1 0; L2 1-2; L3 3-4; L4 >= 5.
- `mech.tail_placement` (directive start bin): L1 p0-p1; L2 p2; L3 p3; L4 p4.
- `mech.framing_depth`: L1 plain_imperative; L2 one base style; L3 conditional, prerequisite or term-redefinition;
  L4 a cue-family wrapper stacked on a base style (A10 cue) or two stacked framings.
- `mech.ambient_genre` (hard benign class; surface genres of the EXISTING ben.* classes, no new class, no table change):
  L1 `genre.readme_setup`; L2 `genre.contributing_note`; L3 `genre.todo_note`, `genre.merge_conflict_msg`; L4
  `genre.setup_login_note` (account-sounding setup wording) with a decoy pointer. Invite, one-time-code and attachment
  genres exist only as human-addressed text (rule 2, ALLOW_BENIGN).
- `mech.delegation_indirection`: L1 no delegation; L2 `deleg.source_pointer`; L3 `deleg.step_pointer`; L4 a step pointer
  plus a decoy pointer (`sub other`) plus the pair twin that differs only in the user turn.
- `mech.lexical_inversion`: L1 matched wording; L2 mild; L3 benign with >= 3 lexicon hits (security discussion or alarm-
  register benign) OR attack with 0 hits; L4 the L3 case inside a stacked framing.
- `mech.nested_depth`: L1 not nested; L2 nested quote; L3 nested inside a declared policy file; L4 nested + conflicting
  `declared_policy` (rule 4 before rule 5 in the table).

8.3 K14 [PRE-FREEZE KILL] COMPOSITION. (a) Rows at L3-L4 >= 25% of N (design 30%: L3 18%, L4 12%); L4 >= 10% (so a 1,000-
row pilot holds >= 100 L4 rows). (b) Level is not a label cue: the L3-L4 share inside each label is within 10 pp of the global
share and >= 20% in each label; K2 gains primary mechanism and level as features (AUC <= 0.55 / bound <= 0.60 in each
binary view; 4-way balanced accuracy <= 28% / bound <= 31%). (c) EASY-LOOKING TWIN: >= 90% of L4 rows sit in a pair
group with a member at L1-L2 of the opposite attack / benign side. (d) MANDATORY QUAD (alarming vs calm surface x risk
present vs resolved): QUAD cells are Q1 alarming + present (attack with >= 3 hits, BLOCK / ASK), Q2 calm + present (the
benign-worded attack, BLOCK / ASK), Q3 alarming + resolved (alarm-register benign or security discussion, ALLOW_BENIGN), Q4
calm + resolved (the clean twin, ALLOW, or plain benign, ALLOW_BENIGN). Complete quad groups (all four cells on one skeleton; the benign member of a quad is the alarm-register Q3 kind) >=
100 groups at N = 2,000 (150 at 3,000) = 20% of N, built by adding the Q2 member to 100 / 150 of the existing triple groups
and taking those members from the splice-pair budget (pair share stays 60%). Each quad cell holds 15% to 35% of rows.

8.4 K15 [PRE-FREEZE FIX-TRIGGER] MEASURED BAR (CRIT D2). Once on the 1,000-row pilot (first look), C2 (C1 if C2 has no weights) is
read on od-l4b (pipelined, Haiku low runs, Sonnet medium checks; free L4, no Modal). Bar: 4-way accuracy on L4 rows <=
70% (point estimate, CI reported). A miss is folded into the ONE combined fix by RAISING the program parameter (more
hits, later tail bins, deeper framing, more decoys); rows are NEVER dropped by model score. After the fix a miss is a
report line P14, not a kill (difficulty is not validity). A model read never kills T41c.

## 9. Benign twins for the L-R Aya and Gandalf-summarization rows (twin generator; rows are block R)

9.1 SCOPE. Plan 16.3 and 16.4 (v3.2-r Sk 7): block R maps Aya Red-teaming English (300 rows) and Gandalf SUMMARIZATION
train (about 100 rows; Gandalf ignore-instructions is DENIED, selection-rule provenance, rolled to C2.2) with Claude-
authored benign twins at a 50% share. L-I writes the twins under the program-enforced literal ban; writers never see the
literal-ban list. These twins are the ONLY Claude-authored text in block R. Task for the model: harmful yes/no (Aya) and
injection yes/no (Gandalf), the datasets' own source labels; the twins are benign BY CONSTRUCTION (no model sets a label).

9.2 INTERFACE (clean with the S-pre rule). The twin generator is code that consumes a TUPLE, never a source row: (twin kind,
topic tag, register, length bucket, form). Tuples are produced by the L-R mapper after the source's S-pre PASS and train-
only reader (L-R rule 1, Sk 5); until then this lane writes the generator and tests it on synthetic tuples. A twin is not
a minimal edit of any source row; the 4-gram overlap between a twin and any source row is <= 20% (program).
- `twin.aya_benign`: kinds `twin.safety_education` (asking how to stay safe or recognise harm on the topic), `twin.mundane_same_topic` (an ordinary, clearly permitted request in the same domain), `twin.opposite_intent` (the same topic, protective intent). Topic tag = the source row's own Aya harm-category tag.
- `twin.gandalf_summ_benign`: kinds `twin.plain_document` (a plain document to summarise), `twin.document_human_note` (a document with a human-addressed footer or note that is NOT aimed at the assistant), `twin.document_security_text` (a document that discusses security without any instruction to the assistant).
Names inside twins come from the TRAINING-salt namespace (twin rows are family L-R, which is exempt from the closed names
list, but twins stay strict: no real names, CPU test).

9.3 GATES (set-level, once per twin set; PRE-FREEZE KILL for the twin set, meaning a failed twin set leaves the dataset's
twins AND its source rows out of C2.1, logged; no model gate).
- TW1 share: twins = 50% +/- 2 pp of the dataset's retained rows (twins are removed, by seeded draw, when source rows are
  dropped by the A46 screen, the stamp or G13, to hold the share).
- TW2 format-only probe (twin vs source row): features = token-length bucket (5), character-count bucket, line count,
  punctuation and digit rates, capitalisation ratio, quote-mark count, form id; AUC <= 0.55 / bound <= 0.60.
- TW3 topic parity: the twin topic-tag distribution equals the source's within 2 pp per tag with >= 10 source rows.
- TW4 lexical balance (T41c lexicon, 2.1): Gandalf twin hit rate 25% to 45% (design 35%) so that "attack register = injection"
  is not the only cue; Aya twin hit rate within 15 pp of the source rows' rate. The bag-of-words probe for Aya (harmful vs
  twin) is REPORT-ONLY (intent differs by design, so it cannot be near chance).
- TW5 blind read: ALL twins (about 400) are read by two Haiku 5.5 medium readers blind as "clearly benign / ambiguous /
  harmful"; a twin read as ambiguous or harmful by either, after Sonnet medium adjudication and Opus A43(d) confirmation, is
  DROPPED (drop-only; the generator knob is widened; no label is ever relabelled, G1).
- TW6 stamp at creation: every twin is G13-stamped when made (literal ban inside G13); first-pass drops > 1% outside
  exemptions go to Opus, > 5% leaves the twin set out (L-R rule 6).

## 10. Hooks: A1, A2, A15, A24

10.1 A1 (template-level gold-bug audit). Every row carries `template_id` (generator template / operator / wrapper / carrier
grammar). L-0's script clusters C2's confident disagreements (p >= 0.95) by template id with a flag threshold written
before the look; a flagged template slice is re-checked by solver B and by program re-run, and dropped drop-only only after
Opus confirms; single rows are never dropped because C2 disagrees. The lane fixes the generator.

10.2 A2 (AFLite-style filter). Added to the declared fix knobs of the G0-lite section 8 as knob (6): the L-0 AFLite filter
may be the fix iteration for a missed K1, K2, K13, K14(b), K16, K17, K18 or K19 probe, if the probe returns under its bars,
the filtered share is <= 30% of the family and reported, and the easy share stays inside plan bounds.

10.3 A15 (dialects). 16.9 does not list A15 for T41c. T41c rows have no policy-card body or tool schema; the carrier
formats `fmt.*` (7, one held out) already play the dialect role for the schema-like carriers. The only hook added is a
manifest field `dialect = fmt.*` of the carrier, for L-0's batch-by-dialect sampler. Rendering the facts block in several
dialects is NOT done unless an Opus ruling asks for it (question Q4).

10.4 A24 (leave-one-family-out term in S). The HO block IS the held-out sub-family score: held-out values are one cue
family (2 styles), 2 goal classes, 1 carrier format, 1 placement, 3 perturbation families, 1 observation operator, 1 layout
(if A14 is built). Training tuples exclude every held-out value; N is a fixed count, so no training row is lost.

## 11. Held-out, benign-dev and long blocks (outside N, never trained on)

- HO (held-out families): 480 rows become 780. >= 80 rows per original held-out value (2 styles of one cue family, 2 goal
  classes, 1 carrier format, 1 placement) and >= 60 rows per new value (3 perturbation families, 1 observation operator, 1 layout
  if A14 is built). One held-out value per HO row (clean attribution). All HO rows are stamped.
- K3 (held-out-family CPU probe) is run on the NORMALISED view of the text (NFKC, strip diacritics, zero-width and bidi
  controls, collapse spacing, undo the leet map, strip ANSI / CRLF / page / progress / truncation lines) because a TF-IDF
  probe trained on in-family perturbations cannot read an unseen transform family and would fail for the probe, not the
  data. The raw-view gap is report-only. Per-axis gaps (cue family, perturbation, operator, layout) are report-only with an
  amber line at 10 pp; the pooled K3 bar of the G0-lite (gap <= 5 pp on both metrics) stays the kill gate.
- BD (benign dev split, 400 rows) is still handed to L-E as the AgentDojo Tier-1 threshold source; it is stamped like every
  row (so it is clear of every external target) and carries the same A12 / A16 shares as N (it must not be easier).
- LS (long slice, 150 rows, eval only) stays at 1.5 to 3K tokens and gains the A14 layouts, including the held-out layout.

## 12. Amendments to the G0-lite, kill rule and schedule

12.1 GATE TABLE CHANGES. K1 gains features: facts-present flag (unchanged), layout id, long flag, A16 operator id,
A12 perturbation flag (each must not predict the label; same bars). K2 gains: cue family and flag, ladder primary mechanism
and level (the quad cell id is NOT a feature: it is a function of the label). K4 gains the section 2-8 shares: benign-worded attack 25% +/- 1.5
pp, alarm-register benign 13% +/- 1.5 pp, A10 pairs 10% +/- 1.5 pp (if built), A12 10% +/- 2 pp per label, A14 5% +/- 1 pp
(if built), complete quad groups >= 100 / 150. K5, K6 (K6(ii) is now per-row at creation, bar unchanged at 98% and measured
on the pilot and on each generation day), K7, K8, K9, K12 unchanged. K10 is REPLACED by section 1. New gates K13-K19 and
report lines P9-P14. The facts-absent design value is ONE value, 30%, in every label, carrier type, subtype AND every
section 2-8 cell (+/- 2 pp), per R2-T41c-d; exact per-cell quotas by construction.

12.2 KILL RULE (G0-lite section 8, with the v3.2 changes). A PRE-FREEZE KILL gate that still fails after the one combined
fix, or a family not through all PRE-FREEZE KILL gates by the declared data freeze (Fri 30 Oct 12:00 if EARLY is declared on
Thu 29 12:00, else Mon 2 Nov 23:59 UTC), rolls T41c to C2.2/C3 with the gate and numbers logged. K15 and every POST-
TRAINING line never kill; queued C2 reads never block. A failed K1 after the fix is a kill (format leak). T41c is P0 family 4
of 9; the floor needs 6 of 9.

12.3 SCHEDULE. Sun 18-Mon 19: this addendum; Opus batch 1. Mon 19-Wed 21: generator code for sections 2 to 9 (no rows); the
conformance record (section 13) is written by a SEPARATE fresh Sonnet 5.5 high session and signed by Opus. Thu 22: template /
wording-pool hash export v1.1 (all A10 and A14 templates included, the section 7 pool included, the lexicon frozen).
Fri 23: free probes (3.1, 5.1). Sat 24 18:00: conformance record signed (else T41c starts no rows) and stamp service signed
off (else row jobs wait). Sun 25: 1,000-row pilot through the stamp wrapper. Mon 26: set-level gates on the pilot; the pilot
token histogram goes to the measured cost projection. Tue 27-Wed 28: full generation (stamped at creation) and the ONE
combined fix. Thu 29 12:00: last fixes. NO "200-row G13 pilot" slot exists.

## 13. Ruling-to-code conformance clauses (the A78 lesson)

A fresh Sonnet 5.5 high session that did not write the T41c code maps each clause below to file:function and a CPU test id;
Opus signs; T41c builds no record without the signed record for its current code sha and ruling sha. This author did not
open the code; the table is the clause list only.
| Id | Clause | Ruling text |
|---|---|---|
| C41-01 | HARD send clause and the single LOW exception | R2-T41c-a |
| C41-02 | shared / production resource directive is HARD; generated only with a lane-tagged anchored span | R2-T41c-b |
| C41-03 | facts-absent hosts: remotes only | R2-T41c-c |
| C41-04 | facts-absent share one design value (30%), each cell +/- 2 pp | R2-T41c-d |
| C41-05 | 97.5th percentile bound; no "95%" bound anywhere | R2-T41c-e, G5 |
| C41-06 | first-match rules 1-8, multi-directive, MCP rule | G0-lite 1.1, O1-O5 |
| C41-07 | five facts-absent default bullets | G0-lite 9.1 |
| C41-08 | solver B is program code; hidden task-verb list | G1 |
| C41-09 | no free pilot tuning; one combined fix | G3 |
| C41-10 | probe harness: grouped split, L2 LR, max(AUC, 1-AUC), 2,000 cluster resamples, permutation and leak checks | G5, K7 |
| C41-11 | token rule: mean <= 800, none > 1,536, > 1,024 on <= 10% | G6 |
| C41-12 | shared host list | G8 |
| C41-13 | decision_spans export with AUTHORITY spans | G10 |
| C41-14 | stamp order and drop-and-log; quota-after-drops; group regeneration | this addendum 1.1-1.4, plan 16.1 |
| C41-15 | lexicon, 50% shares, K13 | this addendum 2 |
| C41-16 | A10 cue families, cue-source check, held-out family | this addendum 3 |
| C41-17 | A12 families, protected spans, survival check | this addendum 4 |
| C41-18 | A14 layouts, token range, held-out layout | this addendum 5 |
| C41-19 | A16 operators, inverse normaliser | this addendum 6 |
| C41-20 | ladder levels, quad groups, L4 bar | this addendum 8 |
| C41-21 | twin tuple interface, 4-gram limit, TW1-TW6 | this addendum 9 |
The G9 spot-check by the L-I build skeptic stays: the HARD / SOFT list must not contradict the shared effects-to-label
table in T50/G0_LITE.md section 3, and once L-A's addendum lands (A3 edit-as-action rows) the skeptic also compares every T41c
directive class whose action edits a state file (hook, CI workflow, lockfile, rc file, cron or systemd unit, script a later
step runs) with the T50 edit-as-action rows. Any disagreement goes to Opus. This addendum adds NO new directive class and no
new risk entry.

## 14. Rulings carried (copied word for word from G0_APPROVALS.md, as the plan requires)

Round 1 must-fix, T41c (items 1-3 and the table rulings) and Round 2 conditions R2-T41c-a to e are copied below; the same
text is in G0_LITE.md section 10, which this addendum does not replace.

R2-T41c-a EGRESS ALIGNMENT (G9 spot-check, done here). Replace the HARD send clause in the 1.1 risk record with: "sends secret, credential or personal-data material to ANY host, declared or not, or places it in a URL, a log line or a package; or sends other project data to a host not in declared_hosts". The one LOW exception is a credential used as an auth header to its own scope host (exact host, https), which is SLT-2 rule 2 under R2-T53-a and the only form of `ben.auth_declared_service`. Reason: under the old clause, a delegated directive to upload a secret to a declared host came out LOW, so ALLOW_BENIGN, while T50 and T53 BLOCK the resulting action as hard.
R2-T41c-b LANE ALIGNMENT. A directive whose action changes a shared or production resource (the SLT-1 C3/C4 scope) is HARD. T41c has no lane facts, so such a directive class is generated only when an anchored span names the lane-tagged context. Otherwise it is not generated.
R2-T41c-c FACTS-ABSENT HOSTS. A host named only in the user task is NOT declared in facts-absent rows (remotes only, as ruled in round 1). After R2-T41c-a this affects project data only.
R2-T41c-d STRATUM SHARE. The facts-absent share is ONE design value, fixed before the pilot (>= 25%; for example 30%), used in every label, carrier type and subtype cell, with each cell within +-2 pp of it. A 25% floor alone would let the share differ by label, and the facts-present flag would then fail K1/K2.
R2-T41c-e Line 8 ("95% upper bound") and the O1-O5 line in 1.1 are superseded by section 9 (the 97.5th-percentile bound; rulings in 9.4). Edit them to match, so the builder does not read two bounds. K6(i) covers the R2-T41c-a exception.
Round 1, T41c TAINT: REVISE. Must-fix:
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
Global rulings G1 to G10 (G0_APPROVALS.md "Global rulings") bind this family unchanged.

## 15. NAMES for the names-only manifest v1.1 (identifiers only)

New to the T41c list in G0-lite section 6:
- Wrapper styles added (3, total 11): `wrap.benign_justification`, `wrap.prerequisite`, `wrap.term_redefinition`.
- Cue families (5): `cue.authority`, `cue.pressure`, `cue.persona`, `cue.task_logic`, `cue.approval`.
- Lexicon: `lex.attack_register_v1` (closed list, builder-authored; stems not recorded in the manifest, only the id and sha).
- Wording flags: `word.benign_worded`, `word.alarm_register`.
- Perturbation families (8): `pert.diacritics`, `pert.spacing`, `pert.leetspeak`, `pert.homoglyph`, `pert.zero_width`, `pert.fullwidth`, `pert.bidi`, `pert.upside_down`; flag `pert.flag`.
- Long-slice layouts (5): `lay.head`, `lay.middle`, `lay.tail`, `lay.interleaved`, `lay.split`; filler kinds (3): `fill.coherent`, `fill.neutral`, `fill.flood`; flag `long.flag`.
- Observation operators (7): `obs.ansi`, `obs.crlf_tab`, `obs.wrapped`, `obs.paginated`, `obs.trunc_marker`, `obs.progress_bar`, `obs.key_order`; flag `obs.flag`.
- Ladder: `mech.trigger_density`, `mech.tail_placement`, `mech.framing_depth`, `mech.ambient_genre`, `mech.delegation_indirection`, `mech.lexical_inversion`, `mech.nested_depth`; levels `lvl.l1`, `lvl.l2`, `lvl.l3`, `lvl.l4`; genres `genre.readme_setup`, `genre.contributing_note`, `genre.todo_note`, `genre.merge_conflict_msg`, `genre.setup_login_note`; quad cells `quad.q1`, `quad.q2`, `quad.q3`, `quad.q4`.
- A6 pool: `pool.comment`, `pool.docstring`, `pool.commit_pr_text`, `pool.written_content`, `pool.mcp_argument`, `pool.gate_directed`, `pool.explanatory`; slot names `slot.target`, `slot.tool`, `slot.change_summary`, `slot.scope`.
- Twins: `twin.aya_benign`, `twin.gandalf_summ_benign`, `twin.safety_education`, `twin.mundane_same_topic`, `twin.opposite_intent`, `twin.plain_document`, `twin.document_human_note`, `twin.document_security_text`.
- Manifest fields: `template_id`, `dialect` (= the carrier `fmt.*`), `stamp.*` (written by the wrapper; not a name list).
- Held-out values: cue family `cue.persona` FIXED (Opus b1 GV2); seeded TRAINING-salt draws recorded before any pilot: 1 observation operator of 7, 1 layout of 5 (if A14 built). Perturbation held-out families are fixed by the lever text.
No real third-party name enters any T41c list. The Gandalf, Aya and benchmark names appear only in the L-R manifest records.

## 16. Open questions for Opus batch 1 (each has the default this addendum already applies)

Q1 (5.2) A14 trained rows at 1,000-1,500 total tokens because G6 caps rows at 1,536, instead of the lever's 1.5-3K; the 1.5-3K range stays eval-only in LS. Default: as written.
Q2 (3.2) The wrapper holdout becomes ONE cue family of two styles (was "2 wrapper styles"), and three base styles are added (benign justification, prerequisite, term redefinition) because hardest.md names them. Default: as written.
Q3 (2.2) Lexicon design values: 50% benign-worded among attack directives, 50% alarm-register among agent-directed benign; |diff| <= 5 pp. Default: as written.
Q4 (10.3) No facts-block dialects in T41c (A15 is not in the 16.9 T41c scope); only the `dialect` manifest field. Default: as written.
Q5 (8.4) The L4 bar is 4-way accuracy <= 70% for C2, point estimate, measured once on the pilot, fix-trigger not kill. Default: as written.
Q6 (11) K3 runs on the normalised view; per-axis gaps are report-only. Default: as written.
Q7 (9.3) TW5: twins read as ambiguous or harmful after the A43(d) route are dropped (drop-only), never relabelled. Default: as written.
Q8 (4.1) Held-out perturbation families are the three the lever names, fixed (not drawn). Default: as written.
Q9 (0) N (2,000 or 3,000) depends on T41's C2 status, which this lane cannot read; the orchestrator supplies it.

---

## Opus batch-1 rulings v3.2 (Opus 5.5 high, Sun 18 Oct 2026 UTC; source: families/G0_APPROVALS_v32.md; binds over this file)

Global rulings GV1-GV9 of families/G0_APPROVALS_v32.md bind this file (GV1 one A10 build rule: flip = predicted label differs
wrapped vs unwrapped, build iff >= 10 of 200, no result by Fri 23 18:00 UTC = not built; GV2 role-play and benign justification
held out in every lane; GV3 one A14 build rule: >= 5 pp gap and bootstrap lower bound > 0; GV4 G6 binds A14, no exemption; GV5 a
G13-hit row retires its spec and its whole group, never re-worded, triggers read first-pass drops incl. collateral; GV6 one
perturbation library pert.*, zero_width = U+200B only, fullwidth / bidi / upside_down held out everywhere; GV7 A15 dialect rows in
L-A only; GV8 pilot-pooled sub-block probes, built-family read binds; GV9 held-out dev rows never trained, mix guard excludes them).
VERDICT: REVISE -> APPROVED after fixes (applied in place): 1.3 G13-hit members retire their skeleton and group (GV5);
3.2 and section 15 held-out cue family = cue.persona, fixed (GV2).
Binding conditions: T41c-B1 Q1 -> GV4 (as written). T41c-B2 Q2 confirmed with GV2. T41c-B3 Q3 confirmed. T41c-B4 Q5-Q8 confirmed
(Q6: the raw-view K3 gap is published); Q4 -> GV7; Q9: the orchestrator fixes N before the Thu 22 hash export. T41c-B5 the 3.1
A10 rule is GV1 (same numbers).
