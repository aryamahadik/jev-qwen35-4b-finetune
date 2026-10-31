# G0-lite T44: SEQ-CHECK (workflow routing over a tool algebra)

A42 wave 2 (FINAL_PLAN section 3 row 5; A42-D 1.1: 833 rows, plans of at most 6 steps, at least 20 cards; A45 d). Agent tier, 1.5 x 833 candidates, 400 sealed items later (S5 only). Code: `plugin.py` (sampler, solver A glue, rendering, relations), `world.py` (algebras, forward executor, BFS: solver A), `solver_b.py` (parser + backward regression: solver B), `texts.py` (rules, wordings, layouts shared by the renderer and the parser).

## 1. Semantics (exact)

| # | Item | Semantics |
|---|---|---|
| S1 | Algebra | 5-7 tools. A tool has typed parameters, a `needs` list of literals (`p(x)` must be true, `not p(x)` must be false), an `adds` list and a `removes` list of facts over its parameters. Its adds and removes are disjoint. Predicates have 1-2 typed arguments. |
| S2 | State | a set of ground facts; only the `Start` facts are true at first (closed world). |
| S3 | Call | `tool(o1, ..)`. Applicable iff every needed fact is in the state and no `not` fact is. Result state = (state - removes) + adds. |
| S4 | Plan verdict (head 1) | in this order: INVALID if any step names an unlisted tool, has the wrong number of arguments, or has an argument that is not an object of its parameter's type (checked on the whole plan first); else STEP_k_NOT_APPLICABLE for the smallest k whose call is not applicable in the state reached by steps 1..k-1 (the plan stops); else GOAL_NOT_REACHED if the Goal literals do not all hold after the last step; else VALID. |
| S5 | Next call (head 2) | the options are 4 ground calls. Let d be the fewest calls that make the whole Goal true from the state reached by the calls so far (BFS over the whole reachable space). The gold is the one option that is applicable now and after which d-1 calls suffice. The other 3 options are not on any shortest route: class `inapp` (needs fail now) or `stuck` (applicable, but the goal is then no nearer or out of reach). Exactly one option is optimal (built so; checked by both solvers). |
| S6 | Closed world | "Only the listed tools, objects and facts exist; nothing else is true or can be called." |
| S7 | Solvers | A (paradigm simulator): `world.verdict` forward state simulation; `world.explore` layered BFS with first-move sets. B (paradigm rule_engine): `solver_b.py` parses the rendered text with its own inverse of every layout, then answers by BACKWARD REGRESSION (weakest preconditions of needs and goal through the plan; regression levels from the goal for d and shortest-route options). The two share no code beyond `texts.py` constants. |

## 2. Heads, options, wordings

| Head | Question form | Options (closed set shown whole / open set of 4) |
|---|---|---|
| 1 | ch_verdict (4 wordings) | INVALID, STEP_k_NOT_APPLICABLE, GOAL_NOT_REACHED, VALID. The k printed in the STEP option is drawn from the row key before the structure (uniform on 1..plan length), so the printed k is a decoy on every row whose gold is not the STEP label. |
| 2 | ch_next (4 wordings) | 4 calls `tool(obj, ..)`; open set (error models below); gold position and visible-length rank planned from the row key (`choiceplan`, k = 4, no abstain). |

Rules (instructions, counted twice) restate S3-S5 in about 100 tokens. Wordings contain no label word (G-SL list: invalid, valid, applicable, reached). Rules are program text and carry the label words.

## 3. Samplers, held out, balance

| Sampler | Content |
|---|---|
| S1 | head 1, plans of 2-4 steps, training domains |
| S2 | head 2, 2-4 calls in total (calls so far m + remaining d), training domains |
| S3 | head 1, 4-6 steps |
| S4 | head 2, 4-6 calls in total |
| S5 (held out, `dev_only`, sealed split only) | both heads (50/50), 7-8 steps / calls in total, held-out domains, held-out layouts |

Training domains (7): git, build, deploy, db (hand-written tool libraries, a dependency-closed random subset of 5-7 tools plus per-algebra perturbations) and alchemy, harbor, theatre (layered random generator over a vocabulary of typed predicates and verbs). 40 algebras per domain (280 in all, index = card). Objects: 2 or 3 per type and 2-5 start facts, both drawn from the row key (so no label can move them). Goal: 1-3 literals (negative literals allowed).
Held out (S5 only; nothing below is reachable from S1-S4, tested): domains registry (dev, release workflow), observatory, bakery (fictional): their tool, predicate, type and object names (disjoint from every training domain), plan lengths 7 and 8, and the layouts `hoare` and `colon`. Training layouts: semi, dash, lines, when, bracket, numbered, pipes (7 registers); head 2 in S5 uses d <= 5.

Label-first generation (head 1): the label is dealt in blocks of 4 consecutive seeds per sampler (a seed-hash permutation), the length n, goal size, printed k, domain and algebra come from the row key, and the structure is searched (random applicable walk, then a label-specific edit: replace a step by an inapplicable call / swap two steps / replace an earlier step; a goal literal replaced by a false one / a step replaced by another applicable call; a step replaced by an unknown tool, a wrong-arity call or a wrong-type argument) until solver A returns the target; drops are redraws, never relabels. Head 2: the total length T, d, option classes and gold rank come from the row key; goal = literals first satisfied exactly at BFS depth d.
Balance: head 1 labels 25% each (exact per block), gold position uniform, STEP printed k independent of the label; replaced plan steps keep the arity of the step they replace and are picked tool-first (no arity or sign shift by label). Head 2: the tool names of the algebra are shuffled among its tools per row (a name carries no role), the 4 options share one parameter-type signature, no option repeats a printed call, no distractor ties the gold in length, and the gold's strict length rank and position are planned from the row key (uniform). Heads 50/50 in the pilot. No row is yes/no.
Budget: mean prompt <= 800 tokens (instructions twice), max 2,000; <= 64 rows per card (card = domain x algebra index); 833 final rows, >= 20 cards.

## 4. Error models (every wrong option is the output of a named model)
Head 1 (closed set; unlisted labels stay `closed`): t44_skips_needs, t44_ignores_deletes, t44_skips_malformed, t44_goal_unchecked. Head 2: t44_inapp (up to 3 variants), t44_stuck (up to 3 variants).

## 5. Relations (G4, metamorphic only; no yes/no, so no complement / twin / equiv / inv partners)
Rename the objects (fresh names of the same type from the domain pool); rename every tool and predicate; reverse the tool block; add a tool that can never run (needs a fact nothing adds). Each keeps the answer (head 2: the renamed call). The partner is solved by solver A, rendered, and passes G2 / G3 again.

## 6. Surface text
Program / template text only (rules, 8 wordings, 9 layouts). No Haiku text and no Mode F field: G3-H does not apply (Mode T). A Haiku task file for tool descriptions would be an optional realism step (BUILD_NOTES).
