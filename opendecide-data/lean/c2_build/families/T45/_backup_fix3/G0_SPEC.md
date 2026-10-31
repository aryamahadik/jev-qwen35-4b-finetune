# G0-lite T45: TRACE-VERIFY (real-tool step verification)

G0-lite, about 2 pages (C2_DATA_SPEC 6.2 item 3; FINAL_PLAN section 3 row 6, A42-D 1.1, 3.1, 13.1, A45 d, A47). Agent tier, wave 2.
Target: 833 C2 rows (A42-D 1.1), at least 20 cards (this build: kind x legend x pack = 5 x 16 x 8 = 640 cards, at most 64 rows each),
SUCCESS >= 35%, 400 sealed items later (S5 only). Choice rows only; no yes/no head (A42-D 1.5). Gold is by EXECUTION only.

## 1. Decision, heads and options
One step of an agent run was executed for real. The row shows: the intended effect (a list of `key=value` items), the state before, the step AS PLANNED (one fault-independent command line per kind; the executed variant, e.g. another branch, a typo or other flags, is the hidden cause and is not printed), the result (the runner's exit code and tag), the state after, and the card's runner legend. Closed-world: the
legend, the two states and the intended effect are the only evidence (`CLOSED_WORLD_SENTENCE`, not printed: choice rows only).

| Head | Question | Option | Definition (printed in the row's rules) |
|---|---|---|---|
| 1 `ch_outcome` | Which outcome describes this step? | SUCCESS | the step reported success, every intended item holds after the step, at least one did not hold before |
| | | NEUTRAL | the step reported success, every intended item already held before the step |
| | | SILENT_PARTIAL | the step reported success, some intended items newly hold, the others are missing, no intended key has another value |
| | | SILENT_WRONG | the step reported success, no intended item newly holds, or an intended key has another value |
| | | LOUD_RETRYABLE | the step reported failure, the tag marks a temporary condition |
| | | LOUD_PERMANENT | the step reported failure, any other tag |
| 2 `ch_move` | What should the agent do after this step? | ADVANCE | the step reported success and every intended item holds after the step |
| | | RETRY | otherwise, the tag marks a temporary condition |
| | | REPAIR_ARGS | otherwise, the tag marks wrong arguments or input, or there is no remark |
| | | ESCALATE | otherwise, the tag marks a block (rights, policy): a person has to act |

Option texts print the label with a gloss where needed so that no two options of a head have the same length (kit length-rank balance): `NEUTRAL (no-op)`, `LOUD_RETRYABLE (temp)`, `LOUD_PERMANENT (final)`; the others are the bare label. The definitions are the row's `card` lines `- <option text>: <definition>` (printed once, for the shown options only).
An item holds in a state when its key has exactly its value (other keys do not matter). Tags and the two exit codes (success, failure; both stated in the rules) are opaque 4-LETTER codes without digits (found by ablation: the mean magnitude of the numbers of a row, a G6 meta feature, decoded which 4-digit code was shown, hence the exit class and the label); every row lists the
four codes of its card's legend (temporary / wrong arguments or input / blocked / no remark), in a card-seeded order and
phrasing (3 phrasings each), so the tag in the result line is joined to the legend and never carries a label by itself.
Every git intent holds the branch and 1-2 tags for every fault, so the intent size is label-blind.
Values are renamed injectively to digit-free words (git shas to 7 letters; quantities and artifact versions to words); ids and version tags in keys keep their digits. Every rules block states a 5-digit runner build number (constant per legend, larger than any number in a state): found by ablation, the maximum magnitude of the numbers of a row (a G6 meta feature) depended on how many FRESH random numbers a row showed (real items repeat the intent's numbers, disguises do not), hence on the label; the constant caps it. Each state line shows the keys that were there before (real), then ONE DISGUISED item per intent key that is not set in that state (same kind, character length and digit count as the missing item; pseudo-word names and values), then 1-3 padding items; new non-intent keys written by the step are not shown (other keys never matter). So the item count, the character length, the digits and the token set of a line do not depend on what the step did. Found by ablation: padding sized by characters from small-vocabulary words made the token set depend on the pad count, hence the label (G6 c LR +4.8 pp); dashes as placeholders for unset keys were rejected (a formatting-only model reads the dash count, +31 to +41 pp).
Each row SHOWS k = 2 (p .30) or 3 labels. The anchor (SUCCESS / ADVANCE) is always shown; the shown set is drawn from the row
key (head 1, k = 3: a confusable pair LOUD_RETRYABLE+LOUD_PERMANENT or SILENT_PARTIAL+SILENT_WRONG w.p. .6, else two other
labels uniformly); the gold is UNIFORM inside the shown set. So the options alone say nothing (P(gold | shown label) = 1/k),
SUCCESS is 38.3% of head-1 rows (E[1/k]) and the majority share equals the mean 1/k.

## 2. Gold (solver A) and verifier (solver B)
- **A, paradigm simulator** (`executor.py`, `exec_child.py`): a fresh sandbox per execution; the REAL step runs: `git push` to a
  local bare remote (pre-receive hooks for "busy" and "protected"), `python dbload.py` (sqlite3: NOT NULL / CHECK / UNIQUE, a
  second connection holds an exclusive lock, a read-only file), `curl` against a ThreadingHTTPServer started inside the child on
  127.0.0.1 (200 with an error body, 503, 403, 404, partial store, staging collection), `make` (GNU make 3.81: a `-`
  recipe prefix, `make -k`, stale mtimes, a lock file, a read-only directory), `python -m unittest discover` (exit 5 = no tests ran,
  skipped tests, a flaky test, a failing test). States are read back by inspectors (`git ls-remote`, SELECT, GET, directory
  read, parsed `-v` output). The runner tag class (T temporary / A arguments / H blocked / 0 none) is the wrapper's reading of the
  real error text (regex table per kind in `exec_child.py`).
  `classify(res)`: LOUD_* = exit != 0, RETRYABLE iff the same step run again (EXECUTED) makes every intended item hold;
  otherwise the diff rules of section 1 on the executed before / after states. Next move: ADVANCE for SUCCESS / NEUTRAL; else
  RETRY iff the executed retry fixes it; else REPAIR_ARGS iff the executed repaired step (corrected arguments or input) fixes it;
  else ESCALATE. It raises `Inconsistent` (the spec is redrawn, never relabelled) when the tag class contradicts the executed retry
  and repair, or when the label differs from the fault's target.
- **Hermetic runs (A47):** `python -S -s -B -P exec_child.py`, venv CPython 3.12.10, `PYTHONHASHSEED=0`, empty temp cwd, minimal env,
  5 s cap per run (a wall-clock timeout, an inner timeout of any step or readback, or an exit status no catalogue tool produces makes the child exit 97 and the whole spec is repeated, at most 4 more times; after the last repeat the spec is dropped and counted; a timeout is never a state, an exit code or a label), localhost only. Every spec is executed in
  TWO independent fresh processes whose structured results (intent, before, main step, retry, repair) must be identical, else the spec is
  dropped. Execution uses canonical names; results are cached in memory by sha256 of (kind, params).
- **B, paradigm set_algebra** (`solver_b.py`, written from this page; imports no solver-A, executor or texts code): parses the
  rendered row (10 layouts by their five line prefixes, the legend by keywords, the item lists, the options back to keys), then
  sets of (key, value) pairs: `want <= now`, `(want & now) - was`, keys of `want` with another value in `now`, and the legend group of
  the tag. No execution, no tool model. Disagreement with A drops the unit (G2 100%).

## 3. Fault catalogue (label-first: the fault is drawn to reach the gold; a draw whose executed answer differs is redrawn)
| Fault | Label (move) | Tag | git | db | http | build | tests |
|---|---|---|---|---|---|---|---|
| ok | SUCCESS (ADVANCE) | none | push branch + tags | load | POST batch | make | unittest |
| already_done | NEUTRAL (ADVANCE) | none | up to date | rows exist | ids exist | up to date | re-run all green |
| swallowed | SILENT_PARTIAL (REPAIR) | none / A | branch pushed, tags left behind | rows skipped (lenient) | items rejected | `-` recipe ignores failure | tests skipped |
| deferred | SILENT_PARTIAL (RETRY) | T | | | rate limit: rest deferred | | |
| wrong_target | SILENT_WRONG (REPAIR) | none | other branch / backup remote | decoy db file | staging collection | `OUT=` redirect | other directory |
| **stale_noop (HELD OUT)** | SILENT_WRONG (REPAIR) | none / A | push of a stale branch: up to date | conflict keeps old rows | create-only skips | stale mtime: "nothing to do" | |
| error_body | SILENT_WRONG (REPAIR or ESCALATE) | A / H | | | 200 with `{"error": ...}` | | |
| busy | LOUD_RETRYABLE (RETRY) | T | hook "ref lock busy" once | database is locked | 503 once | lock file | flaky test |
| bad_arg | LOUD_PERMANENT (REPAIR) | A | remote / branch typo | strict mode, bad row | path typo, 404 | unknown target | pattern: exit 5 |
| blocked | LOUD_PERMANENT (ESCALATE) | H | protected-branch hook | read-only db | 403 | read-only dir | failing test |
| fail_midway | LOUD_PERMANENT (REPAIR) | A | | script stops, earlier rows kept | | `make -k`, one source corrupt | |

## 4. Samplers, held out
Training S1-S4 (S1 head 1 only; S2 head 2 at .70; S3 head 1 at .70; S4 .60; mean .65). **S5 (HELD_OUT_SAMPLERS, dev / sealed only):
the held-out fault type `stale_noop` (leave-one-fault-type-out: it is the SILENT_WRONG fault of every S5 head-1 row where the kind has
it, and one of the repair faults in S5 head 2), registers `memo` and `journal`.** Training samplers never reach it (test:
`heldout_check`: 0 rows in 1,200 training draws). Kinds, packs (8 domain vocabularies) and legends (16) are uniform in all samplers.
Registers (layouts, each about 12.5%): plain, terminal, ci, ticket, yaml, bullets, chat, report (training); memo, journal (held out).
Head 2 gold ADVANCE: `ok` 85% / `already_done` 15% (keeps SUCCESS >= 35% over all rows).

## 5. Relations (G4 metamorphic only; choice rows have no input slots, no twins / complements / attacks)
(1) rename every name, id, value and sha (another pack and surface draw); (2) another runner legend (codes, phrasing, order); (3) other
padding items; (4) another option order and layout draw. Each leaves solver A's answer unchanged (the executed structure is the
same) and the transformed row passes G2 / G3. Open item: no minimal-edit twins (a twin would need a second execution per row).

## 6. Balance, tokens, rows
Gold position uniform per k (`plan_choice(closed=k)`), gold length rank uniform and gold-is-longest = 1/k by the uniform-in-set
design; abstain none. Surface quantities are drawn before the label: item counts m = 3-4 (git: 1 branch + 1-2 tags); disguised and padding items are never intent keys and are never executed (program-rendered noise, re-derived from the row key). Depth = 2 and deep = False on every row (no
label-associated depth). Prompts: mean <= 800 real tokens (instructions counted twice; the head decides which rules block a row
carries), max 2,000. Rows: 833 C2 rows (1.5 x = 1,250 generated), 400 sealed (S5).

## 7. Code-body exemptions (A42-D 3.1) -- E1, E2, E3 confirmed by the orchestrator, 15 Oct ~19:40 UTC
All text is program text (Mode T); no Haiku text exists; G3-H and G5-H-from-Haiku-text are not applicable. The kit's G-SL lints skin
templates (here a one-line layout label and the question wordings), which contain none of the banned words; it does not read the
state or the rules. Requested exemptions:
- **E1. The transcript span (`state` field): intended effect, state before, command, result line, state after.** Exempt from the G-SL
  checks that are undefined on it: literal numbers, ids, shas, ports, quantities, capitalised names, paths and URL-like tokens (they
  are values of the executed step). Both execution runs re-derive every fact (states, exit status, tag class; the command is the
  executed step; the printed command is its fault-independent plan). NOT exempt: the gold-label words (success, neutral, silent, loud, retryable, permanent, advance, retry,
  repair, escalate, partial, wrong) and the negation check: `test_t45` asserts that none occurs in any `state` field.
- **E2. Padding items inside E1** (keys never in the intent, seeded from the row key): same exemption, same re-derivation.
- **E3. The rules and legend block (`instructions`, before the question).** Fixed program template text; it defines the labels, so it
  contains the label words and the quantifier / modal / negation words the lint bans in skins. **Confirmed by the orchestrator, 15 Oct
  ~19:40 UTC, on three conditions, all met and tested:** (1) it is registered as a role `program` template (`T45-RULES-<head>` in the
  kit context; placeholder lint only, the kit's existing G-SL scope, so no exemption beyond it); (2) it is byte-identical for every row of
  a (head, legend); (3) it carries no row fact (the legend codes and exit codes are a function of the legend id only). The legend lines are
  also checked for tag-group keyword disjointness (solver B reads groups from them).
- **E1 and E2 confirmed as written by the orchestrator, 15 Oct ~19:40 UTC** (program-rendered transcript spans, re-derived by both runs;
  exempt only from the G-SL checks undefined on them; the label-word and negation test on `state` stays).
- No other exemption. None is added after a gate result has been seen. No bar is lowered.
