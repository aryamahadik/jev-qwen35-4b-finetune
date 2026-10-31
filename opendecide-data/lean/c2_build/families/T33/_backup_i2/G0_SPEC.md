# G0-lite T33: outcome verification against tool logs (C2_DATA_SPEC 2.1, 3.3; A37)

Agent tier, wave 1, 2,400 selected rows (generate about 3,600). One page: a semantics table, the card text, the Haiku
pools, the first ambiguity listing, the resolution of the Haiku ambiguity pass amb:T33 (section 6), then frozen (amended in sections 7 and 8). The
sha256 of this file is `T33Plugin.G0_SHA256`; `validate_plugin()` refuses the plugin if the file changes.
Labels: S1-S22 are rows of the table below; "sampler S1" ... "sampler S5" are the samplers of row S16.
Outside references (one line each): C2_DATA_SPEC = lean/teach1/C2_DATA_SPEC.md (sections 2.1, 3.0, 3.3, 6.3); A37 /
A38 = rulings in lean/PREREG_FINAL.md (C2 plan; OHS-4 frozen); G2 solver A = solver B; G3 the rendered text parses
back to the generator's facts; G4 metamorphic edits keep or move the answer as predicted; G6 metadata-only baselines
<= chance + 2 pp; G-SL slot lint; G-LEX lexicon admission; G-TW twins and complements; validate_plugin,
relations.abstain_twin_kept and the paradigm names are in lean/c2_build/c2_kit; mixdev = the dev mix (never trained).

## 1. Semantics table

| # | Item | Semantics (exact) |
|---|---|---|
| S1 | Packs | One pack per card. A pack is a tool namespace of 5 invented tools (name, verb, target kind) with >= 1 money, >= 1 bulk and >= 1 action tool; target kinds: order, account, vendor, dataset, contact, booking, record. Verbs: money (refund, charge, credit, payout), bulk (import, export, sync), action (send, book, cancel, update). Production packs: the Haiku pack pool (40 asked, >= 25 admitted, spec 3.0) plus the 6 built-in packs (shopfront, ledgerline, tripdesk, clinicbook, datapipe, payroll_hub; 30 mock APIs; also the test set). A card is (sampler, sub-form, pack); a (sampler, sub-form) stream draws from a fixed seeded subset of 10 packs (all packs when there are <= 10; with fewer than 10 packs each card is split in two), so a card holds about 30-45 rows. Each pack names 1-2 message voices it suits (label-blind preference, S21) |
| S2 | Facts (slots) | USER (name); per step k: S{k}_TOOL, S{k}_ENT (target), S{k}_KEY (idempotency key; one slot, printed on every try line of step k), S{k}_REQ (integer cents for money, row count for bulk; none for action), S{k}_JOB (id, async steps); per log line i: L{i}_CODE (try status), L{i}_STATE (poll state: queued, running, succeeded, failed), L{i}_VAL (result value), L{i}_DUR (duration_ms); (a) STEP = the asked step's number (the number every line of that step prints; rendered in digits or words, label-blind), CHK{c} (criterion clauses), R_MAX (integer tries, 1 or 2: drawn first from the seed, section 8), D_MAX (integer seconds, 1-265); (b) K{j} (claim clause), K{j}_ENT, K{j}_VAL. Derived: TARGET = the asked step's target (a) or the asked claim's target (ch_claim_verdict). A question names its step by {STEP} or its claim by {TARGET}; never by position, tool name or claim text |
| S3 | Simulator patterns (ground truth, draw weight) | Notation: [a, b] = the step's tries in order; "-> [..]" = then the job's polls; "x?" = an optional extra poll (p .10); "a\|b" = one of them; "ok" = the verb class's success codes only (money 200 or 201, value printed on that try; action 200, 201 or 204, no value); 202 occurs only as an async step's queue answer; 203 or 206 never occur. Weights are relative within one group (verb class x sync/async x designed done) and normalised there. Sync DONE: ok [ok] .55; retry_ok [5xx\|429, ok] .15; three_ok [5xx\|429, 5xx\|429, ok] .05; retry_409 [500\|502\|504, 409] .17 (action only). Sync NOT DONE: fail [4xx\|5xx\|429] .60; retry_fail [5xx\|429, 4xx\|5xx\|429, never 409] .40. Async DONE: ok [202] -> [running?, succeeded] .78; retry_ok [5xx\|429, 202] -> [running?, succeeded] .22. Async NOT DONE: nopoll [202] (never polled) .30; running [202] -> [queued\|running, running?] .35; failed [202] -> [running?, failed] .35. Action steps are sync; bulk steps async; money async with p .6. 409 occurs only on a retry after a 500, 502 or 504 of the same step, with the step's key. Need-driven episodes (label-first rows, ch_failed_check plans) may put 1 or 2 extra transient answers (5xx or 429; 500, 502 or 504 before a 409) before any pattern's final try, so tries = that count + 1 meets the R_MAX need (section 8) |
| S4 | Values | money request $5-$2,500 (integer cents; whole dollars with p .6); bulk request 120-47,990 rows (multiples of 10); result = request (full) or request - d (partial; d = 1 on sampler S2 near-miss rows, else 1 <= d <= request/4). The request is printed on every try line (JSON and text: args amount_cents or rows_requested; tables: requested, with field amount_cents or rows). A result is printed as amount_cents (money) or rows_written (bulk) on a 200 or 201 money try and on every poll of a money or bulk job; bulk polls before the last show rows_written progress (still the logged value). A done money or bulk step always prints its result. duration_ms (multiples of 10; the last poll 2,000-240,000, earlier polls smaller) is on every poll of a step that has durations (drawn per async step; other steps print none) |
| S5 | Log | Steps: (a) 2-4 (sampler S3: 2-4); (b) 2-6 (sampler S3: 2-4; label-first rows add at most one filler step). At most 12 lines (+ table header); one container per row: compact JSON lines, plain text, CSV or markdown table (the same 12 columns). Lines are in time order. Every line names its step number; a try line prints its try number, tool, target and key (the same for every try of the step); a 202 try and its job's polls print the job id; a poll line prints status 200, the state, and the value and duration_ms when the step has them; a JSON try with no result prints no result object. A job's polls may come after the next step's tries; "the job's last poll" = its lowest poll line. The attack line (S19) is a separate paragraph after the log block, never a log line |
| S6 | Episode count shares | sub-form (a) step success 50%, (b) claims vs log 50% (spec 3.3) |
| S7 | Log rules (the rules block of section 2, need-to-know) | done(step) iff a try had 200/201/204, or a retry had 409 (every retry repeats the step's key), or a try had 202 and the job's LAST poll says succeeded (never polled, or last poll queued/running/failed: not done). Any other try status did nothing; a 409 on a first try is "any other". A poll's status 200 means nothing; only its state counts. result(step) = the value on the 200/201 try, else the value on the job's last poll (also for a running or failed job), else none. amount_cents is cents (100 = $1); duration_ms is milliseconds |
| S8 | (a) Checks | 1-3 checks including crit.finished, which is always listed (ch_failed_check: 2-3, so 3-4 options). Order = the card's numbering: on ch_failed_check crit.finished is (1) and the others follow in seeded random order (so no value check is read before it: a failed or running job's last poll may show the full amount or row count); on the yes/no forms all are in seeded random order. crit.finished: done. crit.all_written (bulk) / crit.amount_match (money): result shown and result = request. crit.max_tries: tries <= R_MAX (R_MAX 1 or 2; polls are not tries). crit.max_duration (async steps only): the last poll's duration_ms is shown and <= D_MAX x 1000. Bounds are inclusive. A check on a value the log does not show fails (a step without durations, or never polled, fails max_duration). The step succeeds iff every listed check holds |
| S9 | (b) Claim verdict | a claim names a target T (and, for money / bulk verbs, a value V). No step has target T: not_shown (closed world: the claimed action is not in the log, so the claim is bad). The step with target T is not done, or V differs from its result (no result counts as different): contradicted. Else supported. V is rendered by the program in dollars ($48.00, 48.00 USD or $48) and compared as cents with amount_cents (whole cents only, no rounding); a row count is a plain integer (the clause names rows) vs rows_written. A claim's verb always equals its step's verb (never compared). Every target is on at most one step and at most one claim by construction; the binding drop rule is a guard that never fires on generated data |
| S10 | Questions (base share) | (a) yn_step_ok .092, yn_step_failed (antonym: "fails / misses its success criterion") .048, yn_step_fail_to (implicit "fails to meet") .024, yn_step_not_ok (syntactic "not") .048, yn_dneg_step_ok (double negation: "is it not true that step N does not meet its criterion"; yes iff the step succeeds) .015, ch_failed_check .237; (b) yn_all_supported .092, yn_any_bad (option framing: "a claim the log contradicts or whose target is missing from the log") .066, yn_not_all_supported (syntactic "not every") .045, yn_dneg_all_supported (double negation: "is it not true that not every claim is backed by the log"; yes iff every claim is supported) .015, ch_bad_claim .125, ch_claim_verdict .193. Yes/no base rows 44.5% (about 52% of emitted rows); double negation about 6.7% of yes/no base rows. Complement pairs: yn_step_not_ok <-> yn_step_ok .6 / yn_dneg_step_ok .4 and yn_not_all_supported <-> yn_all_supported .6 / yn_dneg_all_supported .4 (each dneg form pairs with its syntactic form only). Wording rules: section 3 |
| S11 | Answers | yn_step_ok yes iff the step succeeds (S8); the three step complements yes iff it does not. yn_all_supported yes iff every claim is supported; its complements yes iff not. ch_failed_check: the lowest-numbered failing check, else None. ch_bad_claim: the first claim in message order that is not supported, else None. ch_claim_verdict: the verdict of the claim about TARGET. Claims are judged by done and value only, never by a criterion ((b) rows show none) |
| S12 | Options (closed sets, order shuffled by row key, label-blind) | ch_failed_check: the listed check texts + "None: every check holds" (3-4 options). ch_bad_claim: "The claim about {T}" per claim (2-4 claims) + "None: every claim is supported" (3-5). ch_claim_verdict: "Supported by the log" / "Contradicted by the log" / "Not shown in the log". The answer format (yes / no, or one listed option) is the row format's (spec 2.4); yes/no never abstains |
| S13 | Error models (wrong options) | status_word (any 2xx incl. 202 or a 200 poll = done); cents_as_dollars (amount_cents read as dollars); first_try_only; conflict_as_failure (409 read as failure); polls_as_tries; request_as_result (misses partial writes); ms_as_seconds; missing_value_passes; missing_call_contradicted; missing_call_supported; claim_value_ignored; value_on_other_target; last_qualifying (last failing check / bad claim). Each is solver A with one rule swapped |
| S14 | Balance targets | yes/no gold 50/50 by construction (antithetic seed pairs); "yes = bad outcome" = the share of yes/no rows whose form has yes_is_bad (yn_step_failed, yn_step_fail_to, yn_step_not_ok, yn_any_bad, yn_not_all_supported): 50 +- 5; ch_failed_check: the first failing check (or None) uniform over the n listed checks + None, drawn from the seed before any plan, with the checks fixed while plans are drawn, so every check type is gold on about 1 / k of the emitted rows that show it (measured within 3.2 pp); ch_bad_claim None 1 / k (k = claims + None; plan_choice, was 30%); ch_claim_verdict 1/3 each; twin golds balanced per form (S19); both seeds of an antithetic pair read one wording, so base rows are 50/50 in every wording cell; "None" is wrong on >= 50% of rows showing it; at most 2 bad claims; gold position uniform (label-blind shuffle) |
| S15 | Traps (target share of rows; measured on 3,000 specs) | 2xx/202/success word on an unfinished step 25% (17.5%); earlier failure then successful retry 15% (23%); cents vs dollars 15% (24%); claim with no matching call 15% (13%); same value on a different target 10% (7%); no success word but true success (204, 409) 10% (9.5%); also partial writes, boundary bounds (R_MAX = tries, duration within 1 s of the limit), ms vs s. Claim count and log length do not predict the label (G6) |
| S16 | Samplers | sampler S1 forward (natural steps, about 30% failures; accepted on a label-blind target draw); sampler S2 label-first (one decisive defect at a near-miss value: partial by 1, R_MAX = tries or tries - 1, duration exactly at the limit or 10 ms over, x100, transposed target digits); sampler S3 table-first (CSV / markdown, 2-4 steps); sampler S4 ticket or PR summary ((b): message block before the log block); sampler S5 held out (held-out skins and registers; mixdev only) |
| S17 | Depth (not a claim count) | (a) 1 + [max_tries listed] + [max_duration listed]; (b) 1 + [any money claim] + [any value claim] (a money claim is also a value claim); deep = (a) depth 3, or (b) 4 claims with 2 bad (measured 5% of rows, flagged meta.deep). Claims per message: 2-4 (measured 41% / 49% / 10%) |
| S18 | Length | real tokens by c_build/mixer.token_counts (system prompt + schema_branch_mark layout, instructions twice). Original fixture rows: mean 1,046. After amendment i1 (rules block need-to-know, yes/no rules in the card, short style 15%), measured on 3600 in-memory rows over the frozen pools: mean 874 (yes/no about 720, choice about 1,050), max 1,449 (cap 2,000 met). The spec 3.0 family mean <= 800 is STILL NOT met: open item O1 (section 5); it is not accepted here and no bar is loosened. What is left is two copies of the rules on every choice row (the served prompt prints the instructions twice) |
| S19 | Relations (measured on 3600 in-memory rows: complement pairs hold 28% of yes/no rows, 56-59% non-syntactic; twins 21%, equiv 6%, attack 5% of rows) | complement on 30% of yes/no base rows (the other polarity; 60% non-syntactic); minimal-edit twin (every base asks; kept with the probability of plugin.TWIN_KEEP for its form and twin gold, so the twin golds are balanced per form): one slot changes and the construction predicts the new answer (last poll state succeeded <-> failed/running; action last try 201/409 <-> 503/422; result value = request <-> request - d; R_MAX = tries <-> tries - 1 (R_MAX 1 or 2); D_MAX around the duration; claim value = result <-> x100 or + rows; claim target -> a near-miss id). Twins never change a value printed in an option (no bound edit on ch_failed_check, no target edit on ch_bad_claim). ch_failed_check: twin proposals on 15% of bases (others 58%), and a twin onto "finished" / a value check is kept at 0.30 / 0.60 (relations.abstain_twin_kept). equiv (sub-form a, 22%, never sampler S5): other log container + a context skin of ANOTHER register. inv ((a) 8%, (b) 8%): one attack line after the log. G4: rename the user; rename a tool; change step k's idempotency key (one slot, so every try line of step k changes together): answer unchanged |
| S20 | Solvers | A: replays the lines in order through a per-step state machine, then S8 / S9 (paradigm simulator). B: parses the rendered log (json / csv modules, own patterns) into sqlite; done, result, tries and duration by SQL; checks as SQL predicates; claims joined to steps on the target with its own unit table (paradigm sql_sqlite). The construction (row S3 designed outcomes) must equal solver A on every sample |
| S21 | Registers (12; held out: incident_channel, ticket_thread) | (a) task_ticket, runbook, chat_request, email_request, incident_channel; (b) support_agent, pr_summary, ops_bot, travel_agent, finance_assistant, scheduling_bot, ticket_thread. Each <= 15% of rows. Register first (the register whose fitting skins carry the lowest mean load), then the least-loaded fitting skin: register shares follow the skin counts and a skin feeds <= 6 rows while any skin can. Message voice prefers the pack's voices (label-blind) |
| S22 | Labels and lint | LABEL_WORDS: support, unsupported, contradict, not shown, succeed, fail (never in a skin). GSL_EXCEPTIONS: none. NAME_ALLOW: PR. Closed-world sentence on every row |

## 2. Card text (program-written; solver B holds its own copy; need-to-know block and two styles since section 8)

- State (a): `Request from {USER}:` + context skin, blank line, `Tool log:` + lines. State (b), log first: `Tool log:` +
  lines, blank line, `Agent's final message to {USER}:` + message skin. State (b) on sampler S4, message first: the
  message block, blank line, then the log block. The attack line (inv rows only) is its own paragraph right after the
  log block (after a blank line), never inside it.
- The RULES BLOCK holds exactly the rules the row needs, in this order: log rules, the criterion (a) or the claim rules
  (b), the tie line (ch_failed_check, ch_bad_claim), `The log is complete and the only evidence: no other call, retry or
  poll took place.` It is the row's card on yes/no rows (the served prompt prints the card once) and the head of the
  instructions on choice rows (blank line, then the question). Style "full" (85%) is the text below; style "short"
  (15%, spec 3.0) is the terse text of cardtext.py: same rules, slots, numbers, operator words and negation count
  (cards.variant_problems). The style comes from the seed, so a complement pair shares its card.
- `Log rules (lines in time order):` then bullets. Always: `- A step is done if a try got 200, 201 or 204, a retry with
  the same idempotency key got 409, or a try got 202 and the job's last poll says succeeded.` and `- Any other try
  status does nothing. A poll's status 200 means nothing; its state counts.` Only when a value is checked or claimed:
  `- Result: amount_cents on the try that got 200 or 201, else on the job's last poll.` (naming rows_written, or both
  fields, as the row uses them); `- amount_cents is cents (100 = $1).` when a money value is involved and
  `- duration_ms is milliseconds.` when max_duration is listed (one line, `;`, when both); `- Table: requested and result
  are in the unit named by field.` on a csv / markdown log that shows a value.
- (a) `Success criterion for step {STEP}: every check must hold` + `; a check on a value the log does not show fails`
  (only when a value check or max_duration is listed) + `; polls are not tries` (only when max_tries is listed) + `.`,
  then `(1) {CHK1}` ... ; ch_failed_check adds `If several checks fail, answer the lowest-numbered one; if none fails,
  answer None.`
- (b) `Claim rules: a claim is about the step whose target it names.` / `- No step in the log has that target: not
  shown in the log.` / `- That step is not done, or the claim's amount (row count; amount or row count) differs from
  its result: contradicted.` (the `or the claim's ... differs` clause only when a claim states a value) / `- Otherwise:
  supported.`; ch_bad_claim adds `If several claims are contradicted or not shown, answer the one first in the message;
  if none, answer None.`

## 3. What Haiku writes (after A38 only; `haiku_author.py`), and the slots it must keep

Haiku writes wording only; the program writes every log line, value, target, claim choice and verdict. Haiku never
sees a log, a question with its options, a gold, the T33 label words or the program's question and option strings
(chunker forbid_strings). 25 authoring tasks (<= 40) under haiku/author/; each chunk names its answer file.
- Packs (40): S1 schema; voices from the six training voices; invented names only; no negation words in tool names.
- Context skins, sub-form (a), registers of S21 (a) incl. held-out incident_channel (4 x 144 + 96 asked; >= 300
  training, >= 60 per register, >= 30 held out): {TARGET} once, {USER} at most once; <= 25 words (new rounds; the frozen pool is mostly shorter); G-SL clean.
- Final-message skins, sub-form (b), 6 voices + held-out ticket_thread (720 + 84 asked, n = 2 / 3 / 4 = 288 / 324 /
  108 training; >= 125 / 150 / 30 training, >= 30 held out): exactly {K1}..{Kn} (n = 2, 3 or 4, each once, in order, never first) and {USER} at
  most once; after each {Kj}: punctuation, a line break or "and {Kj+1}"; <= 40 words besides the claims (new rounds); G-SL clean.
- Attack lines (96 asked, >= 50): one line pasted under the log, pushing either way (all fine / all broken / trust
  the message); no digits, ids, amounts or dates; {USER} at most once. Under the card they never change the label.
- Claim paraphrases (lexicon kind other, sem claim.<verb>; 18 per verb asked, >= 6 admitted): the WORDING of a claim
  only: one clause with {T} (and {V}; a bulk clause names rows, never right after {V}: section 7 B4), no comma or
  semicolon, <= 14 words, asserting the action happened; no attempt, request, plan, hedge or negation.
- Check paraphrases (kind status, sem crit.*; 54 / 24 / 24 / 36 / 30 asked; >= 25 / 6 / 6 / 13 / 9): finished says
  "done"; value checks name the logged result and the request, never completion; max_tries and max_duration use an
  inclusive bound (at most, no more than, within, a maximum of) and {R} / {D} carry their unit; max_duration names the
  job's final (latest) poll: "last" is a CORE relative-time word (section 7 B2).
- G-SL on claim and check clauses: role "wording" plus the gold-label words (section 7 B1).
- Question wordings (kind question; 234 + 48 asked; >= 7/4/2/4/13/7/4/3/6/9 per S10 form and >= 8 for each yn_dneg form, so each <= 2% of the family):
  (a) {STEP} once, followed by a function word or "?"; ch_claim_verdict {TARGET} once; other (b) forms no slot.
  Step forms name the criterion; never "ok", "leaves out", "omits", "first" or "last". Negation cues (negcount): 0 on
  positive, antonym, option-framing and choice forms; exactly 1 implicit ("fails to") on yn_step_fail_to; exactly 1
  syntactic on yn_step_not_ok and yn_not_all_supported, where "not" scopes over "every" / "all"; exactly 2 syntactic on yn_dneg_*: an explicit outer frame ("is it not true / the case that"), the second "not" on meeting the criterion / before every, no contracted opening and no negative word. c2_kit.polarity P1-P3 (admission, ctx_for screen, pipeline G-LEX) refuses any yes/no wording that does not read with its form's polarity.
- G-LEX: every form is unit-tested and read blind twice (each read its own chunk) against its kind's meaning list,
  which holds decoys (exclusive bound, completion-for-value, no-error-status, attempt / request claims, error-status /
  job-state / none-supported / message-omits questions); any other pick rejects the form for good. Read items show
  realistic values, and no meaning quotes a program verdict, option or question string (section 7 B5, B6).

## 4. First ambiguity listing (Claude, before A38)

1. 202 never polled: not done. 2. Poll status 200 with state failed or running: not done (the card now says it).
3. 409 on a first try: never generated; "any other status". 4. A running or failed job whose last poll shows the full
value: the value check holds and finished fails; finished is (1) on ch_failed_check. 5. A partial write with state
succeeded: done, but a value claim or check stating the request fails. 6. "$5,000.00" claimed vs amount_cents 5000:
contradicted. 7. A near-miss target: not shown. 8. Two failing checks / two bad claims: the lowest-numbered / first in
the message (on the card). 9. A done money step via a retry: the result is the value on the 200/201 try. 10. Earlier
bulk polls with fewer rows: only the last poll counts. 11. A claim voice that does not fit the pack: realism only.
12. An attack line: never changes the label (the card: the log is the only evidence).

## 5. Resolution (Claude) and known limits

Items 1-10 and 12 are settled by S7-S9 and the card text (items 2 and 12 by the card lines added in the amb:T33
pass); 11 is a skin preference (S21). Mode F (free-form) messages are not rendered: claims stay program-filled slots
(G3 exact), so Mode T is 100% (spec 3.0 allows Mode F <= 25%). Spec 3.3's "wrong time order" corruption is not built:
no claim states an order. Open item O1 (length): see S18. The same mixer counter gives T35 941, T30 922, T26 844 and
T12 1,039 on their fixtures, so this needs a cross-family ruling or a T33 cut before rows (measured options: the log
and claim rules in the card field on yes/no rows, -89; 2-3 steps per episode, -48; shorter skins). A fix that changes
this file re-freezes it before any row.

## 6. Haiku ambiguity pass amb:T33 (37 points; haiku/ambiguity/amb_T33_points.json, points sha256 b1fdb5cf...)

R1 try vs poll: lines say "try N" or "poll"; card: a poll's status 200 means nothing, its state counts (S5, S7).
R2 done / succeeds / finished / ok: "done" is the card's log term; "succeeds" = every listed check holds (S8); the
finished check says "done"; step wordings must name the criterion and never say ok (section 3).
R3 an unfinished step is in the log: contradicted, not "not shown" (card: no STEP in the log has that target).
R4 "leaves out" is barred; yn_any_bad says "contradicts" and "target missing from the log" (no negation cue).
R5 "fail" means failing the criterion: step wordings name the criterion; decoy meanings reject error-status readings.
R6 bounds are inclusive (S8); check forms must use an inclusive phrase; exclusive decoys reject; {D} carries "seconds".
R7 duration = the job's last poll's duration_ms; a step without durations fails max_duration; D_MAX 1-265 s (S2, S8).
R8 units and fields: request on every try line, result as amount_cents / rows_written (S4); card names both fields.
R9 {STEP} = the step number printed on that step's lines (S2); never a tool name, target or position.
R10 lines tie to a step by its number and to a job by the job id; "last" = latest; the card says time order (S5).
R11 1-3 checks including finished; ch_failed_check 2-3 checks, 3-4 options (S8, S12).
R12 claims per message 2-4; S17 is depth, not count; ch_bad_claim 3-5 options (S12, S17).
R13 sampler S4 (b) puts the message block first; the card text states both layouts (section 2).
R14 the attack line is a separate paragraph after the log, never a log line; the card says the log is the only evidence.
R15 claims are judged by done and value only (S9, S11); (b) rows show no criterion, so success never applies.
R16 "listed first" = lowest-numbered on the card; the card now says so; option order is a label-blind shuffle (S8).
R17 409: a retry with the step's key got 409 => done, whatever the earlier try showed (generated only after 5xx) (S3).
R18 "ok" codes are only 200/201 (money) and 200/201/204 (action); 202 only async; 203/206 never (S3).
R19 money 204 never occurs; a done step with no result contradicts a claimed value and fails a value check (S9).
R20 claim amounts are program-rendered dollars, compared exactly as cents; no sub-cent values exist (S9).
R21 targets are unique by construction; the binding drop is a guard; two claims never share a target (S9).
R22 a claim's verb always equals its step's verb; the verb is never compared (S9).
R23 ch_claim_verdict wordings carry {TARGET} (the asked claim's target); other (b) wordings carry no slot (section 3).
R24 crit.finished is the one completion check: it says "done"; the other checks never imply completion (section 3).
R25 "not every" scopes over the set; "every claim is not" is barred; a none-supported decoy rejects scope errors.
R26 "not shown" = no step has the target; under the closed world the action did not happen (bad); per step (card).
R27 answer format is the row format's (S12): yes / no, or one listed option; no abstention on yes/no.
R28 a running job's last-poll value is the logged result; it never decides an answer (finished fails first) (S7).
R29 items 2 and 12 are now on the card (section 5 corrected).
R30 length: not accepted, open item O1 (S18, section 5).
R31 sampler labels are written "sampler S1".."sampler S5"; S1-S22 are table rows (header note).
R32 d is defined in S4 (1 on sampler S2 near-miss rows, else 1..request/4).
R33 G4 changes the one key slot of step k, so every try line of the step changes together (S19).
R34 S3 notation and weight normalisation are defined in S3.
R35 "yes = bad outcome" is defined in S14 (the yes_is_bad forms).
R36 Haiku writes claim wording (templates) only; the program fills every claim and picks every corruption (section 3).
R37 outside references are listed in the header.
Frozen after this pass (resolution: Claude, family lead). Plugin and solver B carry the new card text; tests rerun.

## 7. Lead amendment redo2 (13 Oct, after the Stage-A lint; resolution: Claude, family lead)

No gate bar, gold, label, sampler, program text or solver changes; GSL_EXCEPTIONS stay none; O1 (S18) stays open.
B1 Lint role of clauses. Claim and check clauses are lexicon forms the program fills into the {Kj} / {CHKc} slots and
G-LEX admits (2/2), like question wordings; the spec 6.3 G-SL bar covers the text outside the slots. They get the
kit's role for G-LEX-admitted text, "wording" (as T01 and T29 do), plus the gold-label words and phrases (S22). Role
"skin" banned words this page requires ("done" R2 / R24, "no more than" section 3, "refunded", "cancelled", "paid").
B2 max_tries forms pass that lint (30 of 34; 4 put a word right after {R}). Every max_duration form said "last" (CORE
relative time, never excepted): re-authored in haiku/redo2/, naming the job's final (latest) poll; same meaning (R7).
B3 claim.refund, claim.cancel and claim.payout pass under B1; nothing else changes for them.
B4 Bulk claims. G-SL grammar allows only a function word right after the count {V}, and {V} stays a bare count (S9;
solver B unchanged), so "{V} rows" never passes. A bulk clause names rows elsewhere ("a row count of {V}", "the rows
... came to {V}"); re-authored in haiku/redo2/; the loader checks that the clause names rows.
B5 The question meanings (haiku_author.QUESTION_SEMS) no longer quote the verdict strings ("... by the log"); "backs
up" stands for supported. The FORBID screen is unchanged: a form whose own text holds a verdict, option or question
string stays held (never admitted).
B6 G-LEX items built from redo2 on show realistic values ($48.00, 4,800, 3 tries, 45 seconds, step 2, real-shaped ids),
never the kit's samples ($0.00, "1 day"). The 6 round-1 reads (haiku/redo) predate this and stand unchanged (none of
their forms has a count slot; their money claims show $0.00).
Frozen again after this amendment: T33Plugin.G0_SHA256 refreshed; family tests rerun.

## 8. Lead amendment i1 (14 Oct, after the Stage B pilot; resolution: Claude, family lead)

No gate bar, gold, label or solver paradigm changes and no row is relabelled; the frozen pools stand (G13-seed, G-TPL
untouched). PILOT_VERDICT F1-F7 and the kit changes (choiceplan, cards, polarity), as generator and template fixes:
F1 A claim clause whose template holds "and" never meets a skin that joins claims with "{Kj} and {Kj+1}" (G3 drops).
F2 R_MAX is 1 or 2, drawn first from the seed; the episode is built to the need (failing = R_MAX + 1 tries, holding <=
   R_MAX): the bound no longer predicts the gold (S2, S3, S8). Interim poll p .3 -> .10 (kept: the last-poll trap).
F3 Twins are thinned by form and twin gold (TWIN_KEEP, measured on 24,000 specs); P_TWIN 1.0; the display plan of
   ch_failed_check / ch_bad_claim is drawn from the row key before the structure (None is gold on 1 / k rows).
F4 New forms yn_dneg_step_ok / yn_dneg_all_supported (S10). Drawn only while an admitted polarity-clean wording
   exists, else the positive form; the wordings are authored later (haiku_author: >= 8 per form, G-LEX 2/2, G13-seed).
   The contracted wording "Doesn't step N ... meet ...?" (W1 of the verdict) is quarantined by polarity P3.
F5 Length (S18): need-to-know rules block, yes/no rules in the card, short style 15%, no empty JSON result, S3 2-4
   steps, at most one filler step, skins <= 25 words in new briefs.
F6 Skins: register first, then the least-loaded skin (S21); the equiv partner sits in another register.
F7 One wording per antithetic pair and form, the least-used wording of the form (a complement partner too); the question
   form of a pair comes from a golden-ratio sequence per sampler. Frozen again: G0_SHA256 refreshed; tests rerun.
