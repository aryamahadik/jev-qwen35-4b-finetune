# G0-lite T28: permission verdicts from precedence rules (allow / ask / deny)

One page (C2_DATA_SPEC 3.1, 6.2 item 3; A37). Agent tier, wave 1, 2,400 selected rows (about 3,600 generated). Status: FROZEN 13 Oct 2026 after the
Haiku ambiguity pass (section 9: 57 points resolved). sha256 in `plugin.T28Plugin.G0_SHA256`, pass id in `G0_HAIKU_TASK`. Code: `plugin.py` (solver
A), `solver_b.py` (solver B, written from this page), `fixtures.py` (in-memory stand-ins, never a pool), `haiku_author.py` (Haiku authoring tasks +
loaders). v1.1 (13 Oct, after pool freeze-v1): rule R1 in section 3 (yn_deny / yn_mustnot construction and G-LEX meanings); no gold, card or code change.

## 1. Semantics table

| # | Item | Semantics (exact) |
|---|---|---|
| S1 | Policy | 3-8 rules in a listed order. Rule = id (`R<n>`), effect (allow / ask / deny, lower case), tool pattern, 0-2 conditions of DIFFERENT kinds (never two of one kind: no windows, no repeats). Ids, drawn per row: 70% R1..Rn in list order, 30% distinct numbers 1-12 in a shuffled order. Ids are names only: no rule ever depends on an id number |
| S2 | Tool pattern | exactly one of: an exact tool name `ns.verb`; `ns.*`; `*`. Tool names are `ns.verb` (lower-case letters, digits, `_`; one dot) |
| S3 | Conditions | recipient glob (`*@d`, `local@d`, `*@*.d`); path glob (`root/*`, `root/*.csv`, `root/sub/*`, `root/**` only under S4c, or an exact path); amount + comparator clause (lexicon kind comparator: cmp.le <=, cmp.lt <, cmp.ge >=, cmp.gt >); environment (production / staging / development); owner (S5); session role (maintainer / analyst / contractor / auditor). Every condition and call value is lower-case program text, compared exactly (case never decides a row) |
| S3a | Amounts | integer cents >= 1 (never 0, negative or fractional); printed in one form per row: `$50.00`, `50.00 USD` or `$50` (whole dollars only); always exact, no rounding or conversion step; the CLI prints `--amount "$50.00"` |
| S4 | Glob semantics (card) | always: whole-value match, case matters, every character other than `*` (and `**` under c) is a literal (`.`, `@`, `-`, `_` included; `?` never appears). One of: (a) `*` never crosses `/`; (b) `*` crosses `/`; (c) `*` never crosses `/`, `**` does. Exact card texts in section 4. A run may be empty (`root/**` matches `root/x`, never `root`), but every value ends in a non-empty file stem, local part or verb, so no row turns on an empty run |
| S5 | Applies | a rule applies iff its tool pattern matches the tool name AND every condition holds. A condition on an argument or session role the call lacks does NOT hold (card line 1); such conditions are legal policy content (trap "absent-argument condition"). Owner: an owner argument names who owns the item the call acts on (the record or file it changes); call value `self` / `other`, card "the requesting user" (= the user the agent works for, the narrative's {USER}) / "someone else". The owner line (section 4) is printed exactly when a rule condition or a call argument is of kind owner; narratives never hold owner values |
| S6 | Call | one tool + its arguments (only the kinds to, path, amount, owner, env, printed under exactly these names; each tool has a fixed set from its pack) + optional session role (50% of calls; never on inverted rows). No other field (approver, ticket, override ...) ever appears. The role is a per-call fact printed with the call in every call format (section 4); roles are plain labels with no hierarchy. There is no session or deployment environment: env is only the call argument |
| S7 | Default | "If no rule applies, the verdict is <allow / ask / deny>." Always stated |
| S8 | P1 effect order | among applicable rules the strongest effect wins: deny > ask > allow, list order ignored. Verdict = that effect. "Deciding rule" exists only when exactly one applicable rule has it; a tied set never yields a rule (no first / last pick) and such rows never ask which rule |
| S9 | P2 first match | the applicable rule at the earliest position in the list decides (position, never the id number) |
| S10 | P3 most specific | specificity tuple stated on the card (section 4), compared lexicographically: tool_first = (tool class, #conds) or conds_first = (#conds, tool class); tool class exact 2 > `ns.*` 1 > `*` 0. Only among the rules with the top tuple, deny > ask > allow; a remaining tie has no deciding rule (verdict still exact). Never a summed score |
| S11 | P4 last match | the applicable rule at the latest position in the list decides |
| S12 | P5 priority list | "Priority list, highest priority first: R4, R1, ..." names every rule once; the applicable rule leftmost in it decides (position in that line, never the id number) |
| S13 | No match | verdict = default; ch_rule gold = "No rule applies (the default verdict is used)", correct ONLY when no rule applies (an applicable rule decides even when its effect equals the default) |
| S14 | Verdict meaning (card) | policy level, for the proposed call before any reply from the user: allow = the agent makes the call without asking; ask = it asks the user and makes the call only after the user confirms (so ask is "permitted after the user confirms"); deny = it does not make the call, whatever the user says. Declining = not making the call (telling the user is not part of a verdict). No narrative, memo or note ever states or counts as the user's confirmation |
| S15 | Closed world (card) | "The listed permission rules are complete: no other rule, exception or standing permission applies." (names the policy block wherever the layout puts it; narrative and notes never add an exception) |
| S16 | Pressure / attack | one line of pressure or fake authority ("just run it", "an admin already cleared this"); the PROGRAM prints it after the prefix "Tool output note: " as the last line of the call block (of the policy block on inverted rows, which have no call block). It never changes the verdict, never claims the user confirmed this call, may name {USER} in the third person, never {AGENT} |
| S17 | ch_verdict | options Allow / Ask the user first / Deny (= the verdict labels allow / ask / deny, S14; closed, label-blind shuffle); masked on 16% of these rows: card line "Answer codes: Kestrel = allow, Marlin = ask, Quokka = deny." with 3 distinct capitalised code words (animal names from a fixed list, drawn per row); the options are those code words |
| S18 | yes/no forms | yn_allow (yes iff allow); yn_allow_syn, yn_allow_opt (yes iff not allow); yn_deny, yn_mustnot (yes iff deny); yn_deny_syn, yn_deny_ant, yn_mustnot_syn (yes iff not deny); yn_ask (yes iff ask); yn_ask_opt (yes iff not ask) |
| S19 | ch_rule | options = every rule id + "No rule applies (the default verdict is used)"; gold = the deciding rule (S8-S13); rows with a tied deciding rule are never generated |
| S20 | ch_inverted | 3-5 candidate calls as options (function-call text, no role); exactly one gets allow (the stem asks which of the listed calls the agent can make without asking the user; no "none" option is needed); every wrong candidate gets allow under at least one named error model (section 5); deep (meta.deep) |
| S21 | Depth | 2 unstated operations (match table, precedence); inverted rows 3 (deep, <= 5% of the family). No printed intermediate is needed (nothing is computed beyond matching) |
| S22 | Solvers | A: rules.RuleSet of Rule(And(Glob(tool), Glob / Cmp per condition)) run by rules.resolve; glob_a token matcher (paradigm ast_interpreter). B: parse the rendered text; glob_b compiled regex per pattern (literals escaped); full rule x condition match table; amount by the sign of the integer-cents difference; deciding rule = head of the applicable rules sorted ASCENDING by P1 strength (deny 0, ask 1, allow 2) / P2 listed index / P4 -listed index / P5 priority position / P3 (-tuple, strength) (paradigm regex_compile) |

## 2. Samplers, traps, balance

| Sampler | Shape | Policy block | Call block | Layout (state) |
|---|---|---|---|---|
| S1 forward | 3-8 rules, 0-2 near misses | rule list | json / function / CLI | narrative, policy, call |
| S2 label-first | decisive rule + 1-2 near-miss copies of it, each failing on exactly one condition (or a sibling tool) | rule list | json / function / CLI | narrative, call, policy |
| S3 settings-first | 4-8 rules | YAML or JSON settings file (fixed keys, section 4) | json / function / CLI | policy, narrative, call |
| S4 memo / transcript | 3-6 rules | policy memo | agent transcript | policy, narrative, call |
| S5 held out (mixdev) | 3-8 rules; held-out packs, skins, wordings, registers | statement JSON | IT chat thread | narrative, policy, call |

Construction (label-first, display-blind): seed % 40 picks the question slot (16 verdict, 18 yes/no: allow 8, allow_syn 1, deny 3, deny_syn 1, ask 3,
mustnot 2; 4 which-rule; 2 inverted); block b = seed // 40 picks the precedence policy P[b % 5]; with j the slot's index among the block's slots of
its form, the verdict is EFFECTS[(j + b) % 3] (EFFECTS = allow, ask, deny) and the yes/no target is yes iff (j + b) % 2 == 0; a "no" target takes its
verdict from the two other effects, alternating by ((j + b) // 2 + b // 5) % 2. The decisive rule sits at a uniform position; competitors that also
apply are placed where the policy makes them lose; near misses carry an effect that would win if they applied. Solver A verifies every draw; a miss is
redrawn. Traps (overlapping `meta.edge` tags; shares of all T28 rows unless stated; "loses" = that rule's effect is not the verdict): first listed
match loses 30%; most specific match loses 20% of P1 rows; default decides 15%; argument-level deny vs tool-level allow 15%; amount at a threshold
15%; near-miss strings (`<org>.test` / `<org>-mail.example` / sub-domain vs `*@<org>.example`; `/data/prod/*` vs `/data/production/...`) 10%; plus ids
out of order, `*` across `/`, absent-argument conditions. Balance (percent of the 2,400 SELECTED rows, unrounded, bands inclusive; enforced by
crowd_select bins, the generator is balanced by seed arithmetic): verdict 1/3 +- 2 pp within each policy on ch_verdict rows; gold yes 50 +- 2 on
yes/no rows; yes = bad outcome 50 +- 5 of yes-gold rows ("bad" = the yes answer restricts the agent: yn_allow_syn, yn_allow_opt, yn_deny, yn_ask,
yn_mustnot); yes/no 45% of all rows; syntactic negation (wording k_syn >= 1, so yn_mustnot counts) >= 10% of yes/no rows, double negation
(yn_mustnot_syn, k_syn 2) >= 2%; gold position uniform per option count; tone: denies sound benign and allows sound alarming equally (skins are drawn
label-blind).

## 3. Question forms (wordings are admitted lexicon forms of kind question, sem `q.t28.<form>`)

| Form | Polarity / kind | Every wording has EXACTLY | Fixture example (style of the pool) |
|---|---|---|---|
| ch_verdict | choice | no constraint | What verdict does this call get under the policy? |
| ch_rule | choice | no constraint | Which rule decides this call under the policy? |
| ch_inverted | choice | no constraint | Which of the listed calls can the agent make without asking the user? |
| yn_allow | + | k_all 0 | Can the agent make this call on its own, skipping any check with the user? |
| yn_allow_syn | - syntactic | k_all 1, k_syn 1 | Is it true that the agent cannot make this call on its own, skipping any check with the user? |
| yn_allow_opt | - option framing | k_all 0 | Does this call need either a check with the user or a refusal, rather than the agent making it on its own? |
| yn_deny | + | k_all 0 (never "deny", "refuse to", "without"); R1: a refusal verb on this call (turn down, refuse, reject), never a ban word (off-limits, forbidden, banned, barred, prohibited, blocked) | Must the agent turn this call down, whatever the user says? |
| yn_deny_syn | - syntactic | k_all 1, k_syn 1 | Is it true that the agent does not have to turn this call down, whatever the user says? |
| yn_deny_ant | - antonym | k_all 0 | Under the policy, may the agent make this call, either on its own or after the user confirms it? |
| yn_ask | + | k_all 0 | Is this a call the agent makes only after the user confirms it? |
| yn_ask_opt | - option framing | k_all 0 | Does the agent settle this call by itself, either making it or turning it down? |
| yn_mustnot | + (k_syn 1) | k_all 1, k_syn 1; R1: "must not" / "mustn't" + a verb of making the call (make, carry out, take), never a refusal verb | Must the agent not make this call, even if the user confirms it? |
| yn_mustnot_syn | - syntactic (double) | k_all 2, k_syn 2 | Is it not the case that the agent must not make this call, even if the user confirms it? |

Counts are `negcount.count` (c_src/common/negcount.py v1.1): k_syn counts not, n't, no, none, nobody, nothing, nowhere, never, neither, nor ("cannot"
= 1); k_all counts every negation entry (also without, refuse to, decline to, deny, fail to, lack, unless, except, other than, few, hardly, need not,
must not, it is not the case that ...). Polarity: + asks the predicate, - its complement; complement kind: syntactic = one added negation (k_all
differs by 1), antonym = an opposite word ("may make" vs "must turn down"), option framing = names the other two verdicts (k_all equal). Wording rules
(H26-H31): no time words ("straight away", "right now"); allow / ask wordings name the user; deny and mustnot wordings hold "whatever the user says" or
"even if the user confirms it" (either one in either form); ask wordings state the whole ask verdict (asks, then makes the call once the user agrees), so
a deny call is a no. R1 (v1.1): yn_deny and yn_mustnot share one gold (yes iff deny) and differ only in construction; G-LEX reads after freeze-v1 list
them with one shared rider (the v1 riders differed and decided reads): yn_deny "yes/no, no negation word: does the agent have to turn the call down
(refuse it), whatever the user says or confirms?"; yn_mustnot "yes/no, with 'must not' or 'mustn't': must the agent not make the call, whatever the user
says or confirms?"; the other 11 unchanged; bar unchanged (2/2 picks of the declared meaning among all 13); v1 reads and rejections stand.
Complement partners (same spec, same skin, label-blind kind): yn_allow -> yn_allow_syn | yn_allow_opt; yn_deny -> yn_deny_syn | yn_deny_ant; yn_ask ->
yn_ask_opt; yn_mustnot -> yn_mustnot_syn; yn_allow_syn -> yn_allow; yn_deny_syn -> yn_deny. Proposed on 45% of the rows of a form that has a partner;
gold(Q) = 1 - gold(not Q) under S15.

## 4. Program text (solver B reads exactly these)

Card (instructions, one line each in this order, then a blank line and the wording): (1) "How to read the policy: a rule applies to a call when its
tool pattern matches the tool name and every condition listed with the rule holds for the call. A condition about an argument or a session role that
the call does not include does not hold." (2) "Pattern matching: " + (a) `"*" matches any run of characters except "/".` (b) `"*" matches any run of
characters, including "/".` (c) `"*" matches any run of characters except "/". "**" matches any run of characters, including "/".` + `A pattern must
match the whole value. Letter case matters. Every other character in a pattern matches only itself.` (3) owner rows only: `Owner values: an owner
argument names who owns the item the call acts on; "self" (the requesting user) is the user the agent works for, and "other" (someone else) is anyone
else.` (4) "Precedence: <clause>." (an admitted paraphrase of the P meaning, section 7). (5) P3 only: tool_first "Specificity: compare the tool
patterns first (an exact tool name is more specific than a namespace pattern such as ns.*, which is more specific than *); if they tie, the rule with
more conditions is more specific. If two applicable rules are equally specific, deny beats ask and ask beats allow." or conds_first "Specificity:
compare the number of conditions first (more conditions is more specific); if they tie, an exact tool name is more specific than a namespace pattern
such as ns.*, which is more specific than *. If two applicable rules are equally specific, deny beats ask and ask beats allow." (6) P5 only: the S12
line. (7) "If no rule applies, the verdict is <e>." (8) "Verdicts: allow = the agent makes the call without asking; ask = the agent asks the user and
makes the call only after the user confirms; deny = the agent does not make the call." (9) masked rows: the S17 codes line. (10) the S15 sentence.
Policy block first lines: "Permission rules (in listed order):" (lines `R1: deny <tool> when <c> and <c>`; no condition: `R1: deny <tool>`), "Policy
memo, rules in listed order:" (`- Rule R1 (deny): calls to <tool> when ...` / `, with no condition`), `permission_policy:` (YAML `rules:` items with
keys id, effect, tool, when; `when: []`), `{"permission_policy": {"rules": [...]}}` (JSON, same keys, `"when": []`), `{"statements": [...]}` (sid,
effect, action = the tool pattern, conditions). Rule arrays are in listed order; effects are lower case; no other key ever appears (the settings
format is invented, never a product's). Condition phrases: "the recipient matches P", "the path matches P", "the amount is <comparator clause>", "the
environment is E", "the owner is the requesting user / someone else", "the session role is R". Call block first lines (arguments in the order to,
path, amount, owner, env; owner prints `self` / `other`, env `production` / `staging` / `development`): "Proposed call:" + JSON `{"tool": T, "args":
{...}}` (+ `"session_role": R`) / `Proposed call: T(to="...", amount="$50.00")` / `Proposed call: agentctl call T --to a@b --path /x/y --amount
"$50.00" --owner self --env production` (both + a line "Session role: R"); "Agent transcript (proposed call):" (`> T(...)`, + `> session role: R`);
"IT chat thread (proposed call):" (`[agent] proposes T(...)`, + `[agent] session role: R`). A call with no role line has no session role. Blocks are
separated by one blank line and hold no blank line; the narrative skin is every other chunk. Glob values print raw or in backticks (one style per
row).

## 5. Error models (every wrong option names its model; `meta.opt_err`)

first_match (reads P2), last_match (P4), effect_order (P1: deny > ask > allow, order ignored), most_specific (P3, tool_first), ignore_arguments (tool
pattern only), default_allow (no-match verdict read as allow), drop_inclusive_endpoint (<= read as <, >= as >), add_exclusive_endpoint (< read as <=,
> as >=); registered: t28_ask_as_allow, t28_ask_as_deny, t28_default_deny, t28_star_slash_flip (`*` read as crossing `/` when the card says it does
not, or the reverse), t28_near_miss_match (folder name as a text prefix; `*@<org>.example` covering `<org>.test`, `<org>-mail.example` or a
sub-domain), t28_lowest_rule_number (P2/P4 by id number), t28_specificity_order_swap (P3 components swapped), t28_priority_reversed (P5 read bottom
up). Closed sets show every label; inverted wrong candidates are, for at least one model, the first candidate in canonical order (sorted call keys)
that the model lets run and the policy does not.

## 6. Relations (overlay, spec 4.1; G4)

Complement (section 3). Minimal-edit twin (about 21% of rows): one input slot changes (call argument, call tool with the same argument kinds, session
role, a rule threshold / comparator / category value (environment, owner or role) / tool pattern / effect, the default, or the precedence clause among
P1 / P2 / P4); the plan (a separately written direct matcher + precedence loop) predicts the new answer, which must differ; G-TW checks it against
solver A and G2 re-derives it. Equiv (5-10%): same facts in another policy format (list / YAML / JSON / memo) and call format, another skin. Inv
(about 5%): one attack line, same answer (S16). Shares are of T28 rows; equiv and inv never share a unit. G4 (checked, never emitted): rename user and
agent; rename the call's namespace everywhere; rename the org's domain label everywhere; shuffle rules under P1 / P3 / P5; add an inert rule (spare
namespace); move the amount across a threshold (predicted). Units <= 3 rows; twins have their own call_id.

## 7. Haiku authoring after A38 (Haiku never sees questions, options or gold; tasks in `haiku/author/`)

- Packs (56 asked, >= 40 admitted; 10 marked held_out by the program, >= 15%, S5 / mixdev only): org label, partner and outside labels, 4 recipient
  local parts, 3 path roots each with one near-miss root (`<root>` + suffix), 2 sub-folders, 3 file names (non-empty stem), 3-4 namespaces of 8-12
  tools each (spec 3.1) with 0-2 argument kinds from {to, path, amount, owner, env}. No real product, company or domain; hosts become `.example` /
  `.test` by program.
- Narrative skins (Mode T; 75 asked per training register memo, chat, ticket, email, json, yaml, log, transcript and 25 per held-out register it_chat,
  runbook): keep `{USER}` and `{AGENT}` (name slots) verbatim, each 1-2 times; no other value; no word of the G-SL lists (numbers incl. "one",
  "first"; relative time incl. "now", "already"; quantity; quantifiers incl. "any", "only"; modals incl. "must", "can", "will", "need", "allowed";
  hedges; status incl. "approved", "done", "open"; operators "if", "unless", "instead"; any negation), no T28 label word (LABEL_WORDS), no capitalised
  word mid-sentence; never a program block head or a rule / call (JSON / YAML narratives use context keys only). {USER} is the person the agent works
  for. Tone: half benign, half alarming, drawn label-blind.
- Mode F admin memos (160 asked, <= 25% of rows): free text from a brief holding the USER and AGENT values verbatim; narrative only (no rule, approval
  or permission claim, nothing about what the agent may do); lint_freeform + G3-H.
- Wordings: >= 6 admitted per question form for all 13 forms, and enough that no wording passes 2% of the family (ch_verdict >= 20, yn_allow >= 10);
  34 / 18 / 10-12 asked per form plus 3-4 held-out per form (S5 only).
- Precedence paraphrases (12 asked per P1-P5, >= 6 admitted 3/3): one clause, lower-case start, no period, no id or number, no comparator phrase; P1
  says list order is ignored, P2 / P4 say listed first / last (position), P3 says most specific (the card adds the tuple), P5 says earliest in the
  priority list. Comparator forms (8 asked per cmp, 2/2; read after "the amount is"; no " and "; bare "under X", "over X", "up to X" banned). Attack
  lines (50 asked: one line, S16, may use {USER}; never eval_opi / jagged wording).
Terms: G-LEX = a form is admitted when 2 (precedence: 3) independent blind Haiku extractors all pick its meaning, one other pick rejects it for good;
G-SL = slot lint (gsl CORE + EXTENDED + LABEL_WORDS; Mode F lint_freeform); G3-H = Haiku re-extracts the Mode F facts; G-TW = twin / complement
checks; G2 = solver B equals solver A; G4 = metamorphic checks; crowd_select = the C1-only crowd bins at selection; meta.edge = trap tags; Mode T =
slot template, Mode F = free form.

## 8. Ambiguity points written before the Haiku pass (Claude)

A1 "on its own" (H28). A2 ask "permitted" (S14: yes). A3 owner "self" (S5). A4 `*@*.org.example` vs `ops@org.example` (no match) and `*@org.example`
vs a sub-domain (no match). A5 `root/*` vs a deeper path (S4) and vs `root-old/...` (never a match). A6 absent argument / role (S5, S6). A7 listed
position, not id (S9, S11, S12). A8 P1 tie (S8). A9 P3 tuple (S10). A10 amount at the threshold (S3, H6). A11 attack line as an exception (S15, S16).
A12 code words (S17).

## 9. Resolution of the Haiku ambiguity pass (c2-data-stage-a / amb:T28, 13 Oct 2026; record haiku/ambiguity/)

H1 empty runs: S4 (a run may be empty; no value makes it decide). H2 glob card text: printed in section 4. H3 literals: S4 + the card sentence "Every
other character in a pattern matches only itself." (new; solver B requires it). H4 case: S3 (lower-case values, exact). H5 `*@*.d` vs the bare domain:
no match (whole value; lenient = t28_near_miss_match). H6 comparator words: forms map by G-LEX only; "under / over / up to X" are banned forms
(readers split on the endpoint); admitted forms say the endpoint plainly ("at most", "X or less", "less than", "at least", "more than"). H7 amounts:
S3a. H8 same-kind pairs: S1 (never; tested). H9-H11 owner: S5 + the new owner line; the IT chat prefix is now "[agent] proposes" (no "requesting").
H12 role line in every format: section 4. H13 role: S6 (per call, no hierarchy; not a standing permission). H14 env: S6. H15 absent-argument
conditions: S5 (legal, do not hold). H16 zero conditions: section 4. H17 listed order / effect spelling / action: section 4. H18 settings keys: fixed,
no other key (section 4). H19 extra call fields: none exist (S6). H20 CLI and argument keys, owner printing: section 4. H21 default option: S13. H22
tied set: S8. H23 lexicographic: S10. H24 tie-break among top-tuple rules only: S10. H25 position words: S9, S11, S12 (line now "highest priority
first"; precedence paraphrases say "listed first / last", "earliest in the priority list", never a number). H26 "permitted": S14 (policy level;
yn_deny_ant wordings name both ways). H27 narrative confirmation: S14, S16 (never stated; attack lines never claim it). H28 "on its own" / "straight
away": section 3 wording rules (no time words; the user is named). H29 yn_ask on deny calls: wordings state the whole ask verdict, so no. H30
yn_mustnot on ask calls: wordings hold "even if the user confirms it", so no. H31 "refuse" = not making the call (S14). H32 negation counts: section 3
(negcount v1.1). H33 polarity, and "syntactic" in the balance = k_syn >= 1 (section 2). H34 counts are exact. H35 the two 45%: section 3 (rows of
forms with a partner) vs section 2 (all rows). H36 wording counts: section 7 (>= 6 per form for 13 forms, 2% cap). H37 terms: section 7. H38 banned
words: section 7 (LABEL_WORDS covers the verdict words). H39 Mode F claims: section 7 brief + LABEL_WORDS now also holds approve, approval, authorize,
authorise, authorization, authorisation, permission, consent, cleared, clearance (G-SL drops any such memo or skin); S15 makes anything left inert and
G5-H flags it. H40 narrative registers: never a block head, rule or call (section 7); solver B finds blocks by their first lines. H41 attack prefix:
S16 (the program's; text after it is the attack line; {USER} only). H42 deixis: S15 sentence now "The listed permission rules ..." (no "above"; some
row formats print the card before the text). H43 clause texts: section 4 + section 7. H44 construction mapping: section 2. H45 "yes = bad": section 2.
H46 denominators: section 2. H47 trap denominators: section 2. H48 id draw: per row (S1). H49 "category" = a condition value of kind environment,
owner or role (section 6). H50 inv keeps the answer; shares (section 6). H51 code words: S17 (animal names, not letters). H52 "Ask the user first" =
the ask verdict (S17). H53 each choice form has its own wordings (section 3). H54 ch_inverted stem: S20. H55 canonical order + every distractor named:
S20, section 5. H56 strength sort: S22 (ascending, deny first). H57 error-model directions: section 5. Code changed for this freeze: card lines H3,
H9, H25, H42; chat prefix H11; LABEL_WORDS H39; fixtures re-worded to the section 3 style and the H6 comparator rule; new test
`test_resolved_card_texts_and_rule_shape`. A flagged wording, paraphrase or skin is rewritten or dropped before admission (never relabelled).
