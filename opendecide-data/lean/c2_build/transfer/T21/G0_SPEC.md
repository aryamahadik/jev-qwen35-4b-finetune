# G0-lite T21: contract cross-references and carve-outs (transfer dev only)

C2_DATA_SPEC 2.2 (T21, 300 items, held out, never trained) and 3.20 (a clause tree, two encodings); rules for every family in 3.0 and 4.1; gate names (G2, G3, G4, G-SL, G-LEX, G-TW, G3-H, G5-H) as in
spec 6.3 and c2_build/README.md. Fully synthetic contracts: no CUAD, MAUD or ContractNLI heading or text (LICENCE_REGISTER 5). **Status: FROZEN v1.3 (14 Oct 2026)** = v1.2 (sha256 bd464707...44cd1, kept
byte for byte as G0_SPEC_v1.2.md) + pilot fix iteration 1 (PILOT_VERDICT FIX-1 to FIX-8; sections 1.1, 1.2, 2, 3, 5, 6 and 10). Generator and template changes only: R1-R16 (the gold rules), every gate
bar and every section 6 target are unchanged and nothing is relabelled. v1.2 = v1.1 (sha256 1779244c...7b62) + section 9; v1.1 = v1 (185e94d1...a48b) + the one blind Haiku ambiguity pass (workflow
c2-data-stage-a, task `amb:T21`: 36 points, haiku/ambiguity/amb_T21_points.json) + one Claude resolution (section 8). sha256 in plugin.T21Plugin.G0_SHA256, pass id in G0_HAIKU_TASK. Code: plugin.py
(solver A), card.py (card styles), solver_b.py (solver B, a separate file written from this page), fixtures.py (test stand-ins), haiku_author.py (v1 authoring, frozen), authoring_i1.py (wording lint and
briefs for the next round). Every row is dev-only (meta.dev_only = true). This page and its card (1.2) are the whole T21 rule set: every row is answerable from its own text.

## 1. Semantics table (exact; rows R1-R16; S1-S5 are samplers only, section 2)

| # | Item | Semantics |
|---|---|---|
| R1 | Facts | An agreement (a name). Clauses with flat dotted ids ("9.3"): labels only, no parent-child reach (a switch on 9 is not a switch on 9.3); listed in numeric order by component (6.2 before 10.1); the listing order carries no meaning. One claim: claimant and respondent (two different names; parties never affect coverage), a claim type from the closed list T and a cause from the closed list C (1.1) |
| R2 | Cap clause | Clause CAP "(Limitation of liability) Each party's total liability for a claim under this agreement is limited to the cap." Every claim is made under this agreement (R12). Capped = CAP is in force for the claim (R8); "the cap" names no amount and no question asks about one |
| R3 | Switch-off | "Clause X does not apply to D." switches X off for the claims D describes (covers, R6), and only for them |
| R4 | Switch-back | "Despite clause Y, clause CAP does apply to D." switches Y off for the claims D describes (same D grammar). Its mention of CAP switches nothing |
| R5 | Names, chains | A clause NAMES only its switch target: X in R3, Y in R4. A clause switched off for a claim has no effect on that claim. Chain CAP <- L1 (switch-off) <- L2 (switch-back on L1) <- L3 (switch-off on L2); every clause is named by at most one clause |
| R6 | D, covers | D = HEAD, optionally + " that arise from C". HEAD = "claims" (every type), "claims for LIST" (LIST = 1-3 distinct types: "T1", "T1 or T2", "T1, T2 or T3") or the defined term. covers(X) = the claim's type is in X's HEAD (the term expanded by R7) and, if the cause qualifier is present, the claim's cause is C. The qualifier binds every type of the HEAD and may follow the term. covers never depends on whether X is active |
| R7 | Definition | "(Definitions) \"Excluded Claims\" means claims for LIST." gives exactly that LIST (2-3 distinct types). Never a switch target, never an option |
| R8 | Capped | covers(CAP) always. active(X) = covers(X) and no clause naming X is active. Well-founded: chains are finite and acyclic. Capped iff active(CAP) |
| R9 | Deciding clause | A walk starts at CAP; it steps to the clause naming the current one only if that clause covers the claim, and stops at the first that does not (or when none names the current one). The deciding clause is where the walk stops: contiguous, never a skip to a deeper covering clause, never "last in id order". Capped iff its depth is even (CAP 0, L1 1, L2 2, L3 3) |
| R10 | yes/no forms | yn_capped: yes iff capped. Complements, yes iff not capped: yn_uncapped (antonym: the word "uncapped"), yn_not_capped (syntactic: exactly one "not" or n't), yn_free_of (implicit: the phrase "free of" with its object, the cap of clause CAP, stated) |
| R11 | ch_clause | Closed set, one answer: CAP, the decoy rule X, and every clause that names a clause (the definition excluded); each option shown as "Clause N"; key = the id N; gold = R9 |
| R12 | Closed world | The card's last line (1.2). No narrative, note, attack line, outside law or default rule changes an answer; yes/no rows never abstain |
| R13 | Decoy rule | "(Notice of claims) A party must give written notice of a claim before bringing it." with its own switch-off clause ("Clause X does not apply to claims for LIST", no cause qualifier): it names X, never CAP, so it never changes the answer. Nothing in T21 depends on time |
| R14 | Solver A | ast_interpreter (plugin.py): R8 recursively from CAP; R9 by the contiguous walk |
| R15 | Solver B | set_algebra (solver_b.py, from this page): grid of cells T x C; cover set per clause (term expanded); effective set = cover minus the effective sets of the clauses naming it, bottom-up; capped iff the claim cell is in CAP's effective set; deciding = the clause with the longest path to CAP whose every link covers the cell (= R9). Refuses the row (ParseError, unit dropped): a cycle, a self-switch, a target that is the definition or not listed, two clauses naming one clause, a duplicate id, two definitions or notice clauses, a term without a definition |
| R16 | Construction, depth | _plan_c(): the planned chain and which links cover; it predicts twins; a guard refuses a spec where it and solver A disagree. G2: an A/B disagreement drops the unit (gold never follows A alone). depth = covering links the walk follows (= the deciding depth 0-3; the stopping link is not counted) + 1 for a definition hop (L1 uses the term and the walk passes L1); with the term the deciding depth is at most 1, so depth <= 3; deep = 3 operations (meta.deep), on choice rows only. meta.depth = the number of switch clauses in the chain (a property of the text); the deciding depth is the label's parity (R9) and is never written |

### 1.1 Lists and program text

T (8 claim types, key: text): conf "breach of confidentiality", dp "breach of data protection duties", ip "infringement of intellectual property", late "late delivery", defect "defective goods", fees
"unpaid fees", injury "personal injury", property "damage to property". C (6 causes): security "a security incident", negligence "gross negligence", misconduct "wilful misconduct", subcontractor "a
subcontractor's error", mistake "an ordinary mistake", supplier "a supplier delay". Both lists are closed. State: narrative skin; blank line; "Clauses of the AGREEMENT:" (or, yes/no rows in the schedule
layout, "Schedule of clauses, AGREEMENT:") and one line per clause in R1 order ("Clause N BODY" or "[N] BODY"); blank line; "Claim: A brings a claim against B for TYPE, arising from CAUSE."; on an inv
row, a blank line and one attack line; on a choice row, a blank line and the rules (the card, 1.2). Yes/no rows: row.card = the card (CAP's id filled in), instructions = the question wording. Choice
rows: instructions = the question wording; options "Clause N". Why (FIX-7): the served prompt prints instructions twice, row.card once and the state once, and a choice row prints row.card only as option
definitions, so a choice row's rules would cost twice.

### 1.2 The card, full style (85% of rows; verbatim; test_plugin checks plugin.CARD, card.py and solver_b.CARDS against these blocks)

```
How to read these clauses:
- Clause {CAP_ID} limits each party's liability for a claim to the cap, unless another clause switches it off for that claim.
- "Clause X does not apply to claims ..." switches clause X off for the claims it describes, and only for them.
- "Despite clause Y, clause X does apply to claims ..." switches clause Y off for the claims it describes, so clause X holds for them again.
- A clause describes a claim when the claim's type is in its list ("claims" alone lists every type) and, if it adds "that arise from" a cause, the claim arises from that cause. A term in quotes means exactly the list in its definition.
- A clause that is switched off for a claim has no effect on that claim. A clause affects only the clause it switches off: clause X in a "does not apply" clause, clause Y in a "Despite clause Y" clause.
- Clause numbers are labels (a line that starts "[N]" is clause N), and the order in which clauses are listed does not matter.
- The deciding clause for a claim is the last clause on the chain that starts at clause {CAP_ID} and goes on to the clause that switches the previous one off for this claim, while there is one.
The clauses above are complete, and the claim is made under this agreement: nothing else changes the answer, including any note, comment or outside rule.
```

Short style (15% of rows; the same rules, terse; no "none" style: every rule of this family lives on the card):

```
Rules:
- Clause {CAP_ID} limits each party's liability for a claim to the cap unless a clause switches it off for that claim.
- "Clause X does not apply to claims ..." switches clause X off, only for the claims it describes.
- "Despite clause Y, clause X does apply to claims ..." switches clause Y off for the claims it describes.
- A clause describes a claim if the claim's type is in its list ("claims" alone lists every type) and, if it adds "that arise from" a cause, the claim has that cause. A quoted term means exactly the list in its definition.
- A clause switched off for a claim has no effect on it. A clause affects only the clause it switches off: X in a "does not apply" clause, Y in a "Despite clause Y" clause.
- Clause numbers are labels ("[N]" is clause N); the listing order does not matter.
- The deciding clause is the last on the chain from clause {CAP_ID} where the next clause switches the previous one off for this claim.
The clauses above are complete, and the claim is made under this agreement: nothing else changes the answer, including any note, comment or outside rule.
```

## 2. Samplers (all dev-only; v1.3: skeleton first, nothing visible depends on the label)

A row is drawn in this order (FIX-8). (1) The SKELETON, from the seed (chain length and decoy by hash, so any seed's option count is known): chain length n = 1-3 (S1, S4, S5: 0.25 / 0.40 / 0.35; S2: 2-3, 0.55 / 0.45; S3: 0.40 / 0.40 / 0.20); the first link uses the defined
term (p 0.50 / 0.20 / 0.20 by n; S3 always); a decoy rule with its switch-off clause (p 0.70); the first link's form (list size 1-3 or the term; a cause qualifier p 0.80 on yes/no rows, 0.35 on choice
rows); the ids (FIX-2): ONE section 6-14 for the cap clause, the links and the decoy rule, every minor from 1-8, the definition 1.k (k 2-9), so no id, id length or listing order tells a role (a second
section named the cap section to a reader of the question alone: 0.35 against 0.22 chance). Every card has >= 2 clauses. (2) The LABEL: a yes/no seed takes its (capped, polarity) cell from a stratified
stream (blocks of 32 seeds; each group of four yes/no seeds holds the four cells once); capped takes depth 0, or 2 (p 0.70) where allowed, not capped depth 1; a choice row has the cap clause as gold in exactly 1/k of
its k cell (k = its option count, stratified per block like the yes/no cells: the question names the cap clause) and else depth 1-3 (0.34 / 0.26 / 0.18 over the allowed depths). Allowed: at most n (S2: n - 1, so a link always follows the
deciding one and misses), at most 1 with the term, at most 2 on yes/no rows. (3) The VALUES: links 1..depth cover the claim and every later link misses (L1 by type or, with a qualifier, by cause (the
type is listed with p 0.85); L2 and L3 by cause), so no generated chain has a covering link after a miss (H2, H27). S1 forward; S2 label-first near misses; S3 definitions first; S4 dispute narrative
(Mode F narratives, plugin.ctx_for) with 0.85 of the seeds of each of S1-S3 (SAMPLER_SEED_WEIGHTS, FIX-5: the pilot and the 1.5x generation); S5 held out (schedule layout on yes/no rows, held-out
registers arbitration_brief and clause_comment, held-out packs; S5 rows only). A decoy's switch-off clause lists the claim's type with p 0.6 and has no cause qualifier, so listing the type = covering the
claim. One pack per card, 12 cards per sampler.

## 3. Traps and balance

Tags: near_miss_link (a link follows the deciding one), cause_decides (a cause-blind reading changes capped), decoy_covers_claim, definition_hop. Every share is a per-draw probability over sampled specs
(no quota, no rounding); the 300 items are later picked as whole relation units. Base form (FIX-3): a seed asks ch_clause with p 0.62 when its skeleton shows >= 3 options (else yes/no), so yes/no bases are 46% and yes/no
rows 50% of the pilot (yes/no bases give 2.0 rows, choice bases 1.6); half the yes/no cells are positive (yn_capped, or yn_double_neg p 0.12 once a clean wording exists, FIX-6) and half negative (each complement form 1/3), by the stratified stream of section 2.
Not capped yes/no rows are depth 1, capped rows depth 0 or 2. Deep (3 operations) occurs on choice rows only (about 3% of rows): a yes/no row is never deep, so meta.deep carries no label.

## 4. Error models (prefix t21_; each is solver A with one switch; ch_clause is a closed set)

ignore_switch_back (L2 ignored), ignore_counter (L3 ignored), wrong_target (the decoy's switch-off read as switching off the cap), cause_ignored (every clause covers its types whatever the cause),
definition_first_only (the term read as only the first type of its list), first_mention (the first clause in listing order whose list names the claim's type decides; listing order carries no meaning,
R1).

## 5. Relations (G-TW 100%)

- Complement: p 0.50 per yes/no base (positive -> one complement form; yn_double_neg -> yn_not_capped; complement form -> yn_capped).
- Minimal-edit twin: p 0.95 per base of any form (FIX-4), kept only where a cause change flips the answer (prediction from _plan_c), leaves a run of covering links then misses and, on yes/no rows, stays
  under 3 operations. A twin exists for 46% of capped and 88% of not capped yes/no bases, so a not capped base attempts at 0.53 of the capped rate (twin rows are 50% capped: the question form must not
  predict capped). Choice rows: a twin of a base whose gold is not the cap clause is a cap-clause twin with probability TWIN_CAP_Q[k] (0.62, 0.26, 0.37, 0.30 for k = 3-6, measured), so the cap clause is
  gold 1/k of all rows.
- equiv p 0.12 (yes/no: the other layout and another skin of the same mode; choice: another skin, plain layout: in the schedule layout an option is verbatim in the text only when a clause names it, which
  marked the chain's inner clauses in G7), else inv p 0.08.
- G4: rename the claimant; rename the agreement; reverse the defined list.

## 6. What Haiku writes (after A38; T21's own registers, never trained); tasks and loaders in haiku_author.py

- Packs: 40 (8 held out, S5 cards only): 4 agreement names ("Oatfield licence agreement": 1-2 capitalised invented words, 1-2 lower-case words, "agreement") + 6 party names (2-3 capitalised words).
  plugin.validate_pack.
- Mode T narrative skins: 12 per training register (dispute_email, legal_memo, counsel_chat, contract_ticket, board_note, negotiation_notes, contract_faq, claims_log; S1-S3) and 16 per held-out register
  (arbitration_brief, clause_comment; S5). {CLAIMANT} and {AGREEMENT} each exactly once per skin; one block; <= 6 rows per skin.
- Mode F narratives (S4): 5 per training register, from facts-only briefs (an invented claimant and agreement name, each kept verbatim); G-SL lint_freeform and G3-H (claimant, agreement).
- A narrative names the dispute only generically. It never states a clause number or id, a claim type or cause (or a synonym: the loaders' word list), the cap, liability, notice, timing, an amount,
  another party or an outcome. The bare word "clause(s)" is allowed.
- Question wordings (lexicon kind question, sem q.t21.<form>, admitted 2/2 by G-LEX): yn_capped 30, ch_clause 26, yn_uncapped 14, yn_not_capped 14 (13 after the FIX-1 quarantine), yn_free_of 14, and from
  v1.3 yn_double_neg >= 8 (none authored: authoring_i1.py). {CAP_ID} exactly once in the yes/no forms but yn_uncapped, at most once in yn_uncapped and ch_clause; "this claim"; negcount (k_all, k_syn)
  exactly (0, 0), (0, 0), (1, 1), (1, 0), (2, 2) and (0, 0) for yn_capped, yn_uncapped, yn_not_capped, yn_free_of, yn_double_neg and ch_clause; yn_uncapped says "uncapped", yn_free_of "free of",
  ch_clause asks which clause decides. Polarity (c2_kit.polarity, FIX-1): a yes/no wording reads with its form's polarity (P1 no negation over a negative predicate: uncapped, unlimited, free of / from,
  set aside, removed, lifted, falling away, waived, disapplied, no longer; P2 parity) and has no contracted negative frame (P3: "isn't this claim capped ...?" reads either way); P4 is off: "Is/Does ...
  not ...?" is the allowed shape of yn_not_capped. yn_double_neg opens "is it not the case that" / "is it not true that" with one "not" on the cap, no n't. A failing wording is never drawn
  (plugin.ctx_for) and never admitted (authoring_i1.check_wording_i1).
- Attack lines: 30, one line with {CLAIMANT} once; pressure only (H19).
- No operator lexicon besides the wordings: the clause bodies (R2-R4, R7, R13) are fixed program text the card defines (no precedence or window paraphrases).
- LABEL_WORDS (forbidden in skins, Mode F, packs and attack lines): capped, uncapped, unlimited, limited, excluded, exempt, carve-out, carve-back, applies, switched, deciding. A wording may use its own
  predicate words (capped, uncapped, limit, limited, decides, deciding), never unlimited, excluded, exempt, carve-out, carve-back, applies or switched. G-SL exceptions: none. NAME_ALLOW: none.

## 7. First ambiguity listing (v1): superseded by section 8, which completes it.

## 8. Resolution of the Haiku pass (amb:T21; H<n> = point n of the record; no gold rule changed, no bar loosened)

Code changes (*): card lines and closed-world line (H1, H3, H6, H7, H10, H20, H32); solver B refusals (H23, H24); a generator guard, one naming clause per clause (H4, H24); tests pin both skip examples
(H2) and the card (H21); packs, S4 Mode F narratives and haiku_author.py (section 6, spec 3.0).
- H1* NAMES = the switch target only (R5): X of R3, Y of R4. A switch-back's mention of CAP names nothing, so CAP is named by L1 alone; the card says a clause affects only the clause it switches off.
- H2 Contiguous walk (R9); the skip and id-order readings are never gold. Both solvers walk contiguously (B: every link on the path covers); test_plugin pins example (a) -> L1, not capped, and (b) ->
  CAP, capped. No generated chain has a link after the k + 1 near miss (section 2), so the readings never split on a generated row.
- H3* covers is R6: D only, never activity; the card's "describes" line states it for the reader.
- H4 Only Y's switch-off is neutralised (R4, R8); every row has one clause naming CAP (guard), so both readings agree.
- H5 "It" is the claim (R5; card: "no effect on that claim").
- H6* Flat labels, numeric component order, no inheritance (R1, card). Generated ids (v1.3): one section s in 6-14 holds the cap clause, the links and the decoy rule, every minor from 1-8, the definition
  1.k: no 2.9 / 2.10 pair occurs.
- H7* Listing order carries no meaning (R1, card); precedence is structural. first_mention and definition_first_only are error models (section 4), never gold.
- H8 The qualifier binds every type of the HEAD and may follow the term (R6); types in one LIST are distinct.
- H9 Parties never affect coverage and claimant != respondent (R1); D has no party grammar.
- H10* Every claim is made under this agreement (closed-world line).
- H11 Capped = CAP in force (R2); no amount exists or is asked; "total" is per claim (one claim per row).
- H12 "Excluded" and "exempt" never appear in a question, skin or attack line (section 6); the term is a type list (R7).
- H13 carve-out, carve-back, applies and switched never appear in a question, skin or attack line; questions ask only R10 and R11. On the card, "describes" = covers and "switched off" = not active.
- H14 "unlimited" is never a question word; "limit" or "limited (by the cap)" in a yn_capped wording means capped.
- H15 yn_free_of says "free of" with its object stated (R10); exact negcount per form (section 6).
- H16 G-SL and the label-word ban scan only Haiku-written text (skins, Mode F, packs, attack lines; wordings by their own role); program text (clauses, card, claim line) is never linted. "Verdict word" =
  a LABEL_WORDS word.
- H17 Bare "clause(s)" is allowed; numbers and ids are G-SL violations; types and causes are refused by name and by synonym (haiku_author.py word lists).
- H18 Each placeholder exactly once per skin; reuse is capped separately (<= 6 rows per skin).
- H19 Attack lines are pressure only (urgency, an outside opinion, a claimed sign-off); no clause, id, type, cause, amount, date or label word. R12 makes them inert, so inv keeps the gold. Skins add no
  amount, date or party.
- H20* R12's scope: no other clause, narrative fact or note, outside law or default rule; yes/no never abstains.
- H21* The card is quoted in 1.2 and test-checked against plugin.CARD and solver_b.CARD.
- H22 T and C are closed lists (1.1).
- H23* Cycles, self-switches, unknown or definition targets, duplicate ids, a term without a definition: invalid, never generated, refused by solver B (R15).
- H24 No tie: one naming clause per clause (generator guard; solver B refuses otherwise).
- H25 Gold is solver A's only when solver B agrees (G2 100%); a disagreement drops the unit.
- H26 R16: the stopping link is not counted; the hop is counted when the walk passes L1; "unstated operations" is spec 3.0's term; deep = exactly 3, the maximum.
- H27 Every link after the deciding one misses (v1.3; S2 always has one): at L1 by type or cause, at L2 and L3 by cause (section 2).
- H28 Semantics rows are R1-R16; S1-S5 name samplers only.
- H29 The label cells, the depth splits and the depth-3 rate: sections 2 and 3.
- H30 Every share is a per-draw probability per base (sections 3, 5); the 45% is a base draw, the 50% a partner rate.
- H31 Decoy switch-offs have no cause qualifier, so covering the type = covering the claim; 0.6 of decoy agreements.
- H32* Options read "Clause N" (key N; choice rows use the plain layout); the card says "[N]" is clause N; CAP's label is its id; one answer; ch_clause wordings ask which clause decides (section 6).
- H33 Held-out registers, skins and packs feed S5 rows only (section 2).
- H34 The first listing was incomplete; this section completes the pass.
- H35 No time element: the notice rule is a decoy (R13); narratives never mention notice or timing (section 6).
- H36 Gate names are defined in C2_DATA_SPEC 6.3 and c2_build/README.md; each row is answerable from its own text.

## 9. Top-up round redo2 (v1.2; process only: R1-R16, the card, every gate and bar and the section 6 targets unchanged)

Blocker B1: 20 lint drops left the v1 pools 2 packs, 8 Mode T skins, 5 Mode F narratives and 5 wordings short, so haiku/redo2/ authored 3 candidates per missing piece (4 per missing wording; ranks fixed
before any answer) under the v1 loaders, lints and G-LEX 2/2, and per cell the lowest-ranked passing candidates fill exactly the shortfall (freeze_v2.py
-> pools_v2/, sha-pinned, frozen under v1.2). No target is lowered and pools/ is never rewritten.

## 10. Fix iteration 1 (14 Oct 2026; PILOT_VERDICT FIX-1 to FIX-8; rulings and what stays open)

- FIX-1: wording 10e86065 (contracted "isn't ...?": 12 pilot rows, both G5-H readings split) and the two templates the > 3% rule flags (T21-SK-contract_ticket.006, T21-MF-claims_log.003) are quarantined
  (quarantine_i1.json, read by freeze_v2.make_ctx; pools_v2/ stays as frozen). Cells short of their section 6 minimum: yn_not_capped 13/14, contract_ticket skins 11/12, claims_log narratives 4/5. No
  target is lowered: one Haiku top-up round under the unchanged gates (authoring_i1.py) or a lead ruling that a G5-H quarantine overrides the minimum. The four "does the cap ... not limit" wordings stay
  (the full read measures them).
- FIX-2 and FIX-8: role-blind ids and skeleton-first sampling (section 2). Ruling (FIX-8 b): meta.depth is the chain length, the deciding depth is not written (it is the label's parity); meta.deep is
  kept and is never true on a yes/no row.
- FIX-3, FIX-4, FIX-5: sections 3, 5 and 2. FIX-6: yn_double_neg is in the plugin and solver B; it is not drawn until a clean wording is admitted, so G10 double_negation_share stays 0 against its >= 2%
  bar until the Haiku round (authoring_i1.py) has run.
- FIX-7: placement and styles (1.1, 1.2): full 85% / short 15% (spec 3.0 "about 15%"), no "none" style. Card tokens 304 (full), 258 (short); the pilot mean is 745 rendered tokens (bar 800). A compact
  middle style saved 28 tokens and was dropped.
- Changes a lead should confirm (all generator or template side; no gold rule or bar moved): (a) choice rules close the state instead of the instructions (the kit's cards.place_rules home: mean 881 tokens,
  over the 800 bar at any yes/no share in 45-55%); (b) one section number per row instead of two (FIX-2 text said above or below; two sections let a question-only reader find the chain: 0.35 vs 0.22); (c) the v1.2
  "20% of depth-0 agreements have no switch-off clause" is dropped (a chain-less card is capped by shape, a label leak; no card has a single clause); (d) the schedule layout is for yes/no rows only (G7).
- Open: the Haiku wording round and G13-seed (yn_double_neg, the yn_not_capped top-up); the G5-H re-read (new placement, short card, skeleton-first rows; >= 10 double-negation rows once they exist); the
  G3-H re-read.
