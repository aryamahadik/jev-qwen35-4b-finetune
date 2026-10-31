# G0-lite T21: contract cross-references and carve-outs (transfer dev only)

C2_DATA_SPEC 2.2 (T21, 300 items, held out, never trained) and 3.20 (a clause tree, two encodings); rules for every
family in 3.0 and 4.1; gate names (G2, G3, G4, G-SL, G-LEX, G-TW, G3-H, G5-H) as in spec 6.3 and c2_build/README.md.
Fully synthetic contracts: no CUAD, MAUD or ContractNLI heading or text (LICENCE_REGISTER 5).
**Status: FROZEN v1.2 (13 Oct 2026)** = v1.1 (sha256 1779244c...7b62) + section 9 (the redo2 top-up; process only).
v1.1 = v1 (sha256 185e94d1...a48b) + the one blind Haiku ambiguity pass (workflow c2-data-stage-a, task `amb:T21`:
36 points, verbatim in haiku/ambiguity/amb_T21_points.json) + one Claude resolution (section 8). sha256 in
plugin.T21Plugin.G0_SHA256, pass id in G0_HAIKU_TASK. Code: plugin.py (solver A), solver_b.py
(solver B, a separate file written from this page), fixtures.py (test stand-ins), haiku_author.py (Haiku authoring
tasks and loaders). Every row is dev-only (meta.dev_only = true). This page and its card (1.2) are the whole T21 rule
set: every row is answerable from its own text.

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
| R11 | ch_clause | Closed set, one answer: CAP, the decoy rule X, and every clause that names a clause (the definition excluded); each option shown as "Clause N" in both layouts; key = the id N; gold = R9 |
| R12 | Closed world | The card's last line (1.2). No narrative, note, attack line, outside law or default rule changes an answer; yes/no rows never abstain |
| R13 | Decoy rule | "(Notice of claims) A party must give written notice of a claim before bringing it." with its own switch-off clause ("Clause X does not apply to claims for LIST", no cause qualifier): it names X, never CAP, so it never changes the answer. Nothing in T21 depends on time |
| R14 | Solver A | ast_interpreter (plugin.py): R8 recursively from CAP; R9 by the contiguous walk |
| R15 | Solver B | set_algebra (solver_b.py, from this page): grid of cells T x C; cover set per clause (term expanded); effective set = cover minus the effective sets of the clauses naming it, bottom-up; capped iff the claim cell is in CAP's effective set; deciding = the clause with the longest path to CAP whose every link covers the cell (= R9). Refuses the row (ParseError, unit dropped): a cycle, a self-switch, a target that is the definition or not listed, two clauses naming one clause, a duplicate id, two definitions or notice clauses, a term without a definition |
| R16 | Construction, depth | _plan_c(): the planned chain and which links cover; it predicts twins; a guard refuses a spec where it and solver A disagree. G2: an A/B disagreement drops the unit (gold never follows A alone). depth = covering links the walk follows (= the deciding depth 0-3; the stopping link is not counted) + 1 for a definition hop (L1 uses the term and the walk passes L1); the term is drawn only when the planned depth <= 1, so depth <= 3; deep = depth 3 (meta.deep) |

### 1.1 Lists and program text

T (8 claim types, key: text): conf "breach of confidentiality", dp "breach of data protection duties", ip
"infringement of intellectual property", late "late delivery", defect "defective goods", fees "unpaid fees", injury
"personal injury", property "damage to property". C (6 causes): security "a security incident", negligence "gross
negligence", misconduct "wilful misconduct", subcontractor "a subcontractor's error", mistake "an ordinary mistake",
supplier "a supplier delay". Both lists are closed.
State: narrative skin; blank line; "Clauses of the AGREEMENT:" (or, schedule layout, "Schedule of clauses,
AGREEMENT:") and one line per clause in R1 order ("Clause N BODY" or "[N] BODY"); blank line; "Claim: A brings a claim
against B for TYPE, arising from CAUSE."; on an inv row, a blank line and one attack line. Instructions: the card
(1.2, CAP's id filled in), blank line, the question wording. Options (ch_clause): "Clause N".

### 1.2 The card (verbatim; test_plugin checks plugin.CARD and solver_b.CARD against this block)

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

## 2. Samplers (all dev-only)

S1 forward. S2 label-first near misses: always one extra link at depth k + 1 of the deciding depth k (none at k = 3)
that misses the claim: at L1 by type or by cause (about half each), at L2 and L3 always by cause. S1, S3, S4 and S5
add that link with p 0.6; 20% of depth-0 agreements have no switch-off clause. S3 definitions first (L1 uses the
term; only when the planned depth <= 1). S4 dispute narrative (Mode F narratives, plugin.ctx_for). S5 held out
(schedule layout, held-out registers arbitration_brief and clause_comment, held-out packs; these feed S5 rows only).
A decoy rule appears with p 0.7; its switch-off clause lists the claim's type with p 0.6 of those (0.42 of all) and has
no cause qualifier, so listing the type = covering the claim. One pack per card, 12 cards per sampler.

## 3. Traps and balance

Tags: near_miss_link (the k + 1 link exists), cause_decides (a cause-blind reading changes capped),
decoy_covers_claim, definition_hop. Every share is a per-draw probability over sampled specs (no quota, no rounding);
the 300 items are later picked as whole relation units. Base form: ch_clause p 0.35; yes/no p 0.65, of which yn_capped
p 0.55 and each complement form p 0.15 (base draws, before relation partners). Yes/no seed pairs: seeds 2b and 2b + 1
of one sampler form block b, and a seeded hash makes exactly one of the two planned capped. Capped: depth 0 or 2
(p 0.5 each); not capped: depth 1 (p 0.85) or 3 (p 0.15). ch_clause: depth uniform 0-3. A planned depth 3 is kept
with p 0.30, else it becomes 1 (depth 3: 7.5% of ch_clause, 4.5% of not-capped yes/no).

## 4. Error models (prefix t21_; each is solver A with one switch; ch_clause is a closed set)

ignore_switch_back (L2 ignored), ignore_counter (L3 ignored), wrong_target (the decoy's switch-off read as switching off
the cap), cause_ignored (every clause covers its types whatever the cause), definition_first_only (the term read as
only the first type of its list), first_mention (the first clause in listing order whose list names the claim's type
decides; listing order carries no meaning, R1).

## 5. Relations (G-TW 100%)

- Complement: p 0.50 per yes/no base (positive -> one complement form; complement form -> yn_capped).
- Minimal-edit twin: p 0.55 per base of any form, kept only where a cause change grows or shrinks the covered chain by
  one link and flips the answer (prediction from _plan_c), so the realised share is lower.
- equiv p 0.12 (the other layout and another skin of the same mode), else inv p 0.08 (one attack line).
- G4: rename the claimant; rename the agreement; reverse the defined list.

## 6. What Haiku writes (after A38; T21's own registers, never trained); tasks and loaders in haiku_author.py

- Packs: 40 (8 held out, S5 cards only): 4 agreement names ("Oatfield licence agreement": 1-2 capitalised invented
  words, 1-2 lower-case words, "agreement") + 6 party names (2-3 capitalised words). plugin.validate_pack.
- Mode T narrative skins: 12 per training register (dispute_email, legal_memo, counsel_chat, contract_ticket,
  board_note, negotiation_notes, contract_faq, claims_log; S1-S3) and 16 per held-out register (arbitration_brief,
  clause_comment; S5). {CLAIMANT} and {AGREEMENT} each exactly once per skin; one block; <= 6 rows per skin.
- Mode F narratives (S4): 5 per training register, from facts-only briefs (an invented claimant and agreement name,
  each kept verbatim); G-SL lint_freeform and G3-H (claimant, agreement).
- A narrative names the dispute only generically. It never states a clause number or id, a claim type or cause (or a
  synonym: the loaders' word list), the cap, liability, notice, timing, an amount, another party or an outcome. The
  bare word "clause(s)" is allowed.
- Question wordings (lexicon kind question, sem q.t21.<form>, admitted 2/2 by G-LEX): yn_capped 30, ch_clause 26,
  yn_uncapped 14, yn_not_capped 14, yn_free_of 14. {CAP_ID} exactly once in yn_capped, yn_not_capped and yn_free_of, at
  most once in yn_uncapped and ch_clause; "this claim"; negcount (k_all, k_syn) exactly (0, 0), (0, 0), (1, 1), (1, 0)
  and (0, 0) for yn_capped, yn_uncapped, yn_not_capped, yn_free_of and ch_clause; yn_uncapped says "uncapped",
  yn_free_of says "free of", ch_clause asks which clause decides (or is the deciding clause).
- Attack lines: 30, one line with {CLAIMANT} once; pressure only (H19).
- No operator lexicon besides the wordings: the clause bodies (R2-R4, R7, R13) are fixed program text the card
  defines (no precedence or window paraphrases).
- LABEL_WORDS (forbidden in skins, Mode F, packs and attack lines): capped, uncapped, unlimited, limited, excluded,
  exempt, carve-out, carve-back, applies, switched, deciding. A wording may use its own predicate words (capped,
  uncapped, limit, limited, decides, deciding), never unlimited, excluded, exempt, carve-out, carve-back, applies or
  switched. G-SL exceptions: none. NAME_ALLOW: none.

## 7. First ambiguity listing (v1, Claude)

1. "Does not apply" covers only the claims it describes (R3). 2. A switch-back switches Y off (R4). 3. The decoy's
switch-off never touches the cap (R13). 4. A switch-back with the type but another cause does not cover (R6). 5. A
term is exactly its list (R7). 6. Two clauses naming one clause: never generated (R5). 7. L2 covers, L3 does not: L2
(R9). This list was incomplete; the Haiku pass (section 8) completes it.

## 8. Resolution of the Haiku pass (amb:T21; H<n> = point n of the record; no gold rule changed, no bar loosened)

Code changes (*): card lines and closed-world line (H1, H3, H6, H7, H10, H20, H32); solver B refusals (H23, H24); a
generator guard, one naming clause per clause (H4, H24); tests pin both skip examples (H2) and the card (H21); packs,
S4 Mode F narratives and haiku_author.py (section 6, spec 3.0).
- H1* NAMES = the switch target only (R5): X of R3, Y of R4. A switch-back's mention of CAP names nothing, so CAP is
  named by L1 alone; the card says a clause affects only the clause it switches off.
- H2 Contiguous walk (R9); the skip and id-order readings are never gold. Both solvers walk contiguously (B: every
  link on the path covers); test_plugin pins example (a) -> L1, not capped, and (b) -> CAP, capped. No generated chain
  has a link after the k + 1 near miss (section 2), so the readings never split on a generated row.
- H3* covers is R6: D only, never activity; the card's "describes" line states it for the reader.
- H4 Only Y's switch-off is neutralised (R4, R8); every row has one clause naming CAP (guard), so both readings agree.
- H5 "It" is the claim (R5; card: "no effect on that claim").
- H6* Flat labels, numeric component order, no inheritance (R1, card). Generated ids: CAP s.1, links s.2-s.8, the
  definition 1.k, the decoy (s+1..s+3).1 and .2, s in 6-14, so no 2.9 / 2.10 pair occurs.
- H7* Listing order carries no meaning (R1, card); precedence is structural. first_mention and definition_first_only
  are error models (section 4), never gold.
- H8 The qualifier binds every type of the HEAD and may follow the term (R6); types in one LIST are distinct.
- H9 Parties never affect coverage and claimant != respondent (R1); D has no party grammar.
- H10* Every claim is made under this agreement (closed-world line).
- H11 Capped = CAP in force (R2); no amount exists or is asked; "total" is per claim (one claim per row).
- H12 "Excluded" and "exempt" never appear in a question, skin or attack line (section 6); the term is a type list (R7).
- H13 carve-out, carve-back, applies and switched never appear in a question, skin or attack line; questions ask only
  R10 and R11. On the card, "describes" = covers and "switched off" = not active.
- H14 "unlimited" is never a question word; "limit" or "limited (by the cap)" in a yn_capped wording means capped.
- H15 yn_free_of says "free of" with its object stated (R10); exact negcount per form (section 6).
- H16 G-SL and the label-word ban scan only Haiku-written text (skins, Mode F, packs, attack lines; wordings by their
  own role); program text (clauses, card, claim line) is never linted. "Verdict word" = a LABEL_WORDS word.
- H17 Bare "clause(s)" is allowed; numbers and ids are G-SL violations; types and causes are refused by name and by
  synonym (haiku_author.py word lists).
- H18 Each placeholder exactly once per skin; reuse is capped separately (<= 6 rows per skin).
- H19 Attack lines are pressure only (urgency, an outside opinion, a claimed sign-off); no clause, id, type, cause,
  amount, date or label word. R12 makes them inert, so inv keeps the gold. Skins add no amount, date or party.
- H20* R12's scope: no other clause, narrative fact or note, outside law or default rule; yes/no never abstains.
- H21* The card is quoted in 1.2 and test-checked against plugin.CARD and solver_b.CARD.
- H22 T and C are closed lists (1.1).
- H23* Cycles, self-switches, unknown or definition targets, duplicate ids, a term without a definition: invalid,
  never generated, refused by solver B (R15).
- H24 No tie: one naming clause per clause (generator guard; solver B refuses otherwise).
- H25 Gold is solver A's only when solver B agrees (G2 100%); a disagreement drops the unit.
- H26 R16: the stopping link is not counted; the hop is counted when the walk passes L1; "unstated operations" is spec
  3.0's term; deep = exactly 3, the maximum.
- H27 The near miss sits exactly at k + 1 (none at k = 3): at L1 by type or cause, at L2 and L3 by cause (section 2).
- H28 Semantics rows are R1-R16; S1-S5 name samplers only.
- H29 Seed pairs, the depth splits and the depth-3 rate: section 3.
- H30 Every share is a per-draw probability per base (sections 3, 5); the 45% is a base draw, the 50% a partner rate.
- H31 Decoy switch-offs have no cause qualifier, so covering the type = covering the claim; 0.6 of decoy agreements.
- H32* Options read "Clause N" in both layouts (key N); the card says "[N]" is clause N; CAP's label is its id; one
  answer; ch_clause wordings ask which clause decides (section 6).
- H33 Held-out registers, skins and packs feed S5 rows only (section 2).
- H34 Section 7 was incomplete; this section completes the pass.
- H35 No time element: the notice rule is a decoy (R13); narratives never mention notice or timing (section 6).
- H36 Gate names are defined in C2_DATA_SPEC 6.3 and c2_build/README.md; each row is answerable from its own text.

## 9. Top-up round redo2 (v1.2; process only: R1-R16, the card, every gate and bar and the section 6 targets unchanged)

- Why (blocker B1): v1 authored exactly the section 6 targets, so 20 lint drops (pools/quarantine.json) left the frozen
  pools 2 training packs, 8 Mode T skins, 5 Mode F narratives and 5 wordings short. No target is lowered, no v1 task is
  re-read (that re-authors its whole chunk) and pools/ is never rewritten by this round.
- Round: haiku/redo2/build_redo2.py authors new candidates for the short cells only (new seed, opaque qids and answer
  paths): 3 per missing piece and 4 per missing wording, each with a rank fixed before any answer. Prompts are the v1
  prompts plus words the gates already refuse and v1 openings to avoid; Mode F briefs carry new invented names.
- Gates, unchanged: the v1 loaders and lints by role, dedup against every v1 text and name, G-LEX 2/2 inside the v1
  registry (a form that fails, or breaks any form's unit test, is dropped), one exact G3-H read per narrative.
- Selection: per cell, the lowest-ranked candidates that pass every gate fill exactly the shortfall; the rest stay
  unused. A cell still short stays short and is reported. Results go to haiku/redo2/results/ with sha256s; joining
  them to pools/ (an additive load or a re-freeze) is the orchestrator's call.
