# T42 CODE-EXEC: G0-lite spec (A42; FINAL_PLAN section 3, row 2)

Code execution reasoning over Python 3.12. Choice rows only. Gold is program execution; no model sets a label.

## 1. Decision, heads and options
- **Head 1, output.** "What does this Python snippet print / what does `result` hold, or which exception does it raise?"
  Question forms `ch_output` (the program ends in one `print(...)`; the answer is the printed line) and `ch_return` (the
  program ends in `result = ...`; the answer is `repr(result)`). 4 or 5 options (k drawn from the row key). An uncaught
  exception is the option `raises <Class>`. Open answer set: the k options are the real outputs of the programs of one STAR (section 4): the hub program and k-1 of its mutants; the shown program is the member at the planned length rank.
- **Head 2, equivalence.** `ch_equiv`: two functions `f` and `g` (same signature, annotated `int`, `list[int]` or `str`).
  Closed set of 3 options: `SAME`, `DIFFERS_TYPICAL`, `DIFFERS_EDGE`. Outcome of a call = the returned value plus the
  arguments afterwards, or the exception class. Ordinary input: ints in {2..12}, non-empty lists of 3-5 distinct values,
  words of 3+ lowercase letters. Edge input: everything else (empty / 1-2 item lists, repeated items, 0, 1, negatives,
  capitals, digits, spaces). Exact grids: section 3.

## 2. Gold (solver A: hermetic execution) and solver B
- **A.** `executor.py` + `exec_child.py`: venv CPython 3.12, `PYTHONHASHSEED=0`, a fresh subprocess (`-S -s -B -P`), 5 s
  cap, empty temp dir as cwd, minimal environment, no network and no writes (audit hook, RLIMIT_FSIZE 0), step cap by
  `sys.settrace` line events. Every shown program, shown distractor and equivalence pair is executed twice in two fresh
  processes; a disagreement drops the draw. Output gold = `out:<line>` or `exc:<Class>`; programs that print nothing, print
  several lines, > 70 characters, an address, or hit the step cap are never used.
- **B.** `solver_b.py` (paradigm `independent_interpreter`, imports no solver-A code): parses the rendered row (layout
  inverses, rules text, wording skin, options back to keys), then a tree-walking interpreter of the shown AST (scope chains
  with late-binding closures, defaults at def time, classes with C3 + `super()`, try/except/else/finally, comprehension
  scope, f-strings) and, for equivalence, exhaustive enumeration of the grids (no fuzz, no coverage).
- **Equivalence label rule** (A's counts; B uses the grids alone): `DIFFERS_TYPICAL` when >= 10% of the typical grid
  differs (witness = first differing input); `DIFFERS_EDGE` when the typical grid and 5,000 typical fuzz inputs agree and
  an edge or cross input differs (witness); `SAME` when no difference on the full grid and in 10,000 fuzz inputs
  (5,000 typical-range, 5,000 wide) and branch coverage >= 95% for both functions. Anything else (a few typical
  differences, fuzz-only difference, low coverage, timeout) is rejected: the structure is redrawn, never relabelled.
- **Coverage:** `sys.settrace` with opcode events (CPython 3.12 delivers them from the second traced run: one warm-up pass),
  conditional jumps (`POP_JUMP_IF_*`, `FOR_ITER`) of f, g and nested code objects; both successors must be seen; the
  suite is the grid plus 1,000 of the fuzz inputs.
- **Grids** (typical / edge): int {2,3,4,5,6,7,8,9,10,12} / {-9,-5,-3,-2,-1,0,1,100}; list: for each combination of 3-5 of
  {2,3,5,7,8} the ascending list and the left-rotated descending list (32) / 15 fixed lists ([], singles, pairs, repeats,
  negatives, zero); str: 24 fixed words / 14 fixed strings ("", "a", "ab", "A", "Ab", "ABC", "a b", " x", "x ", "a1", "7",
  "aa", "aaa", "ab ba"). Full grid = product of (typical + edge) per argument.

## 3. Samplers (training S1-S4; held out S5)
| Sampler | Content |
|---|---|
| S1 | `ch_output`, difficulty bins 1-2 |
| S2 | `ch_return`, bins 2-3 |
| S3 | `ch_equiv`, label thirds, diff bin 0-3 |
| S4 | `ch_output` / `ch_return` mix, bins 1-3 |
| S5 (HELD_OUT_SAMPLERS) | **idiom buckets closure/late-binding and MRO**; **mutation operators `swap_args` and `wrong_slice_bound`** (+ `late_binding`, `mro_order` that only those buckets use); **layouts `numbered` and `tabs`**; 25% equivalence rows with the held-out operators; all rows dev only |
Round robin S1-S4 gives 25% equivalence and 75% output rows. **Idioms (training):** arith_loop, slice_str, comprehension,
dict_ops, sort_key, set_ops, default_arg, aliasing, exceptions, formatting, iteration (11 buckets, 20 templates). **Equivalence
skeletons:** 13 typed functions with choice points (reference forms A, typical near-misses, edge near-misses); 4 of the 17 written skeletons cannot yield every label at a similar rate (measured: SAME, TYPICAL and EDGE in 24 tries each) and are excluded.
**Difficulty bin** (steps, nesting): 1 = one construct, trace <= 40 line events; 2 = two constructs, <= 120; 3 = three
constructs / nesting 2, <= 300. Trace cap enforced by execution.

## 4. Options and distractors
- **Mutants** (error models, one named near-miss edit by `mutate.py`, printed by the same `ast.unparse` as the shown program):
  off_by_one, wrong_operator, swap_args*, mutate_default, wrong_slice_bound*, late_binding, int_float_div, flip_sort,
  wrong_method, reorder_stmts, wrong_except, wrong_format, mro_order, wrong_key, repair_failure (exception rows: the failing
  step repaired), and `compound` (two different edits); * held out. Names `op`, `op@2`, `op@3`, `op@4` when one operator
  yields several distractors. Every wrong option is the real output of such a mutant (executed twice); nothing is predicted.
- **Star design** (found by the probes: a gold that is always the generated program, with every distractor one edit away, is the
  centre of the option set and sits inside the generator's number prior, so token, number and "most similar to the others" cues
  find it). The sampler generates a HUB program, executes its mutants (one named edit, or two) and builds the set
  {hub output} + k-1 mutant outputs. The SHOWN program is the member whose (visible length, text) rank equals the planned
  rank (`choiceplan.plan_choice`, abstain False, ks (4,5): k, gold position and gold length rank from the row key; the kit's
  `length_balance` agrees by construction), so the shown program is the hub itself exactly 1 time in k, and its distractors
  are the hub (named `revert_edit`) and sibling mutants (1-2 edits away). Every wrong option is the real output of such a
  program, executed twice.
- **Label-blind option sets** (each makes one visible property of an option say nothing about the gold): (1) all value options of
  a row have one SHAPE (container, sign, decimal point, letters; None / True / False alone); (2) one overlap class, read against the
  SHOWN program, the rules and the wordings (no token / some / every token of the option occurs there); (3) the shown program's rank by
  total similarity (difflib) to the other value options is drawn from the row key (uniform): the "most central option" cue
  is at chance; (4) constants of the templates range widely (2-9) so a +-1 mutation stays inside the prior.
- **Exceptions.** Exception options appear only in exception rows (20% of output rows, template `exc_fail`; card = template x class x bin x style). One class per
  row (KeyError, IndexError or ZeroDivisionError from the row key); the program is 2-3 steps of that class, and the only
  exception option is `raises <class>` (mutants raising another class are not used). m = 1 option is the exception with
  probability 0.5, else none; value options are <= 12 characters, so shorter than any `raises X` text: with m = 1 the shown
  program raises exactly when its rank is the longest (probability 1/k, exchangeable). A failing hub takes its value options from its repaired versions
  (`repair_failure`, alone and with one more edit). Everywhere else no option is an exception.
- Equivalence options: the closed set in a row-key permutation (`build_closed`, plan closed=3). Error models: `typical_only_check`,
  `edge_as_typical`, `typical_as_edge`, `same_as_differs`.
- **Pairs.** f and g come from one skeleton through one printer. The token-diff bin (<=7, 8-14, 15-24, >=25) is drawn from
  the row key before the label is built, so each label has the same bin marginals; extra equivalent rewrites and renames
  of locals pad small diffs. Probes: options-only, formatting-only (+/- 3 pp) and diff size (CV accuracy <= majority + 3 pp,
  AUC 0.5 +/- 0.05).

## 5. Balance and budget
Answer labels: SAME / DIFFERS_TYPICAL / DIFFERS_EDGE = 1/3 each. Gold position uniform per k; gold-length rank uniform; gold
is longest within +/- 2 pp of 1/k. Registers (layouts of the code block; both functions of a pair share it): fenced, plain,
headed, task_intro, md_quote, narrow (train); numbered, tabs (held out). Cards = template (or skeleton) x bin x naming
style: >= 70 per 3,000 rows, <= 64 rows each. Prompts: mean <= 800 tokens, max 2,000; rules (printed in `instructions`, counted
twice) are 40-110 tokens. Rows: about 2,000 C2 rows (1,500 output + 500 equivalence); 900 sealed items by the held-out S5 later.
Question wordings: 3 per form (9), admitted in the lexicon (G-LEX); stand-in admission until the Haiku 2/2 runs.

## 6. G4 metamorphic relations (checked, never emitted)
(1) rename parameters and locals (output answer / label unchanged); (2) add a dead statement (output unchanged); (3) swap in
the first distractor's mutant (the answer becomes that distractor's output, the old gold joins the distractors); (4)
swap which function is `f` (label unchanged). Equivalence rows use (1) and (4); output rows (1)-(3). Twins, equiv format
partners, complements and attack lines are not defined for T42 (no input slots; choice rows only): open item.
