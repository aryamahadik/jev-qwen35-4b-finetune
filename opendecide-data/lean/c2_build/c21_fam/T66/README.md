# T66 generator notes (generator side; Solver B does not read this file)

Sun 18 Oct 2026 (updated after the Opus K7 ruling and dev rounds X1-X3). No bar, gold label or model changed; no row has been built. Solver B's own files are untouched.

## 1. CH-6 and the kinds

* CH-6 = "make a parameter required (its default is removed)", verb class `required` (was `param`, G0-lite "add parameter"): `def f(x, b=2)` -> `def f(x, b)`. Rendering unchanged. CH-6 messages never say
  "default" (CH-5 does, always). CH-4 (extract helper) and CH-7 (remove dead branch) are behaviour-preserving: registered, never realised.
* `msg_spec.CH_NAMES` names every realised kind; `KIND_SLOTS` fixes the slots each kind's templates may use (`fn`, `arg`, `param`, `num_old`, `num_new`, `new_fn`, `tok`, `word`, `word_old`, `word_new`, `lv`).

## 2. The message pool (`pools/msg_messages.json`, source `msg_pool_src.py`, rebuild `python3 -m T66.msg_pool_src` from c21_fam/)

* 8 realised kinds x 56 templates (28 style I = names the function / values of the change, 28 style N = identifier-free, numbers allowed) = 448, plus the three trivial kinds `fmt`, `comment`,
  `doc` with 216 / 212 / 216 templates (they must cover the lengths of the true messages, section 4). 1,092 templates; halves by a seeded hash (`msg_pool.split_ranks`, rank parity inside every
  (kind, style)): **`dev`** and **`dev2`**, 546 each. `dev2` is the half the first holdout run was spent on (Sun 18 Oct, 4.8% abstain); both halves are dev material now. The label **`holdout`** is
  reserved for a freshly written half: a separate file in the same format (templates labelled `holdout`, 20+ per kind), used with `--msg-pool`.
* `Ctx(..., msg_split="dev"|"dev2"|"holdout"|"all", msg_pool=<path|dict>)` replaces the 19 MSG forms of the wording pool by that half. Pool file for `solver_b/agree.py --msg-pool`:
  `python3 -m T66.msg_pool --split dev|dev2|holdout|all [--msg-pool FILE] --out PATH`. A fresh half is checked with `python3 -m T66.lint_msg_pool --pool FILE` and run with
  `--split holdout --msg-pool FILE`.
* `checked.CODE_FILES` includes `msg_pool.py` and `pools/msg_messages.json`; `msg_pool.MSG_POOL_SHA256` puts the file's sha into the HASH_EXPORT tables.

## 3. Lint (`lint_msg_pool.py`, output `pools/msg_messages.lint.txt`) - the rules a new half must satisfy

Fails on: a shared normalised text (prefixes `fix:` ... stripped, also across kinds); token Jaccard >= 0.5 between templates of two kinds that can meet in a row (a trivial kind never meets another
trivial kind); missing / unknown slots (style I carries `{fn}`, style N no identifier slot); a template that names another kind's words; a question; < 4 or > 16 rendered tokens; an internal id;
a wrong stored dev / dev2 split; < 40 templates per kind (20 in a holdout-only file), < 20 per half, < 10 per (kind, style, half); and, new:
* **REQUIRED kind phrase** (G0-lite kind phrase + its object word): CH-1 guard / validate / reject + negative; CH-2 `off-by-one`; CH-3 `rename`; CH-5 `default`; CH-6 `required parameter` or
  `mandatory parameter`; CH-8 `error|failure|exception message|text|wording`; CH-9 `log*`; CH-10 constant / multiplier / factor / coefficient / scale; fmt `reformat` or `formatting`;
  comment `comment`; doc `docstring`.
* **FORBIDDEN words** (read as another kind or as noise by Solver B; evidence: abstain lifts in rounds 4-6 and the first holdout run): `refactor`, `descriptive` outside CH-3; `tweak` outside CH-10;
  for CH-8 `clarify`, `unclear`, `pick`, `report`, `on`, `shown`, `carries`, `some`, `hint`; for CH-6 `optional`, `implicit`, `drop`, `enforce`, `turn*`, `takes`, `anymore`, `force`, `pass`;
  for comment `hint`, `purpose`, `commentary`, `ownership`, `annotate`, `leave`, `explain*`, `some`; for doc `some`, `give`, `put`, `been`, `top`, `text`, `short`, `code`. The `config:` prefix
  abstained 11% of 38 uses; keep it out.
* **Trivial coverage**: every half has >= 2 (aim for 6+, spread over the character range) templates per (trivial kind, style, token count 5..10).

## 4. NO-message construction (Opus ruling Q8, `RULINGS_T66.md`) - `generator._msg_group`

* R1 a non-trivial NO message is the partner's TRUE message verbatim (same wording id, fillers and identifiers); `SWAP_STYLE_RULE`, `LENGTH_MATCH` and the slot re-binding (`complete_slots`) are gone;
  each spec's slots are its kind's own (`msg_spec.own_slots`).
* R2 a group (two specs on one base module, <= 4 rows per module) is a SWAP group or a CH-TRIVIAL group; in a swap group the derangement over the two diffs makes the NO messages equal the YES
  messages as a multiset (Jaccard < 0.5, different verb class, >= 4 tokens).
* R3 a CH-trivial NO message describes one of the diff's own trivial hunks and matches its true message in rendered token count and style, characters within +-3 (`trivial_pick`); with no fit
  the group is regenerated (up to 8 new seeds, picker counters restored); the pipeline refills what still fails (1-2% of trivial groups).
* R4 hard stratum: a swap group on two kinds that change the SAME function (`msg_spec.SAME_FN_PAIRS`: CH-1 + CH-10, CH-2 + CH-9, CH-5 + CH-8, CH-6 + CH-8; weights `SAME_FN_WEIGHT`), styles (N, I):
  the partner's verbatim style-I message names the function, which is in this diff (checked per row, `mech.ovl = "high"`). Every other group is style N on both specs (a one-sided identifier
  overlap is what the overlap probe read: AUC 0.59). 85% of the swap groups are same-function; CH-8 is always the N one.
* R5 every message has >= 4 tokens (pool lint + `Reject` + `solver_a.gold_a` returns None).
* Plan: 27% of the groups are CH-trivial groups (quota, not drawn; realised 26-27% of NO rows, >= 25%), the rest swap; hard-stratum rows 31%; `CONFUSABLE_PAIRS` (CH-5 + CH-6, CH-5 + CH-10) never
  share a module; kind mix `KIND_WEIGHT` (CH-5 / CH-6 / CH-8 drawn at 0.7, the kinds Solver B abstains on most).

## 5. Solver B dev rounds (default strict thresholds, `agree.py --rows 2400`; counts in `pools/msg_dev_rounds.json`)

MERGE / SEMVER: 100% agreement, 0 abstain in every round. MSG:

| round | what | agree / labelled | disagree | abstain |
|---|---|---|---|---|
| 1-6 | old construction, dev half (round 6 = 1.24%) | 100% | 0 | 34 / 2752 |
| first holdout run (coordinator) | old construction, then-final pool | 2620 / 2620 | 0 | 132 / 2752 = 4.8% (CH-8 14%, CH-6 9%) |
| X1 (seeds 1-4) | Q8 construction + CH-8 / CH-6 / CH-10 rework | dev 2701 / 2701; dev2 2681 / 2681 | 0 | dev 43 = 1.57%; dev2 71 = 2.58% |
| X2 (seeds 1-4) | CH-5 + CH-10 not grouped, kind mix, CH-8 style N, weakest CH-5 N / CH-10 I re-cut | dev 2720 / 2720; dev2 2731 / 2731 | 0 | dev 24 = 0.87%; dev2 21 = 0.76% |
| X3 (seeds 5-8, unseen diffs) | = X2 pool | dev 2734 / 2734; dev2 2732 / 2732 | 0 | dev 18 = 0.65%; dev2 20 = 0.73% |

What the data said: abstains were kind- and template-bound (CH-8 style N templates without "error message" and with `refactor`, `descriptive`, `tweak`, `clarify`, `shown` were the 14%); with every template carrying its
kind phrase the half-to-half gap closed. About 16 abstains recur on the same rows (diff-bound): CH-5 diffs with a CH-10 message (now never grouped) and CH-6 / CH-8 diffs in the p3 pairs.
The extension's 3-round cap is spent (X1-X3); the pool files measured in X2 / X3 are byte-identical to what the generator writes now.

## 6. K7 (dry run, SimExecutor, 4 seeds, ~2750 MSG rows, 300 bootstrap draws; the pilot and the built family are the binding reads)

| pool / construction | message_only | diff_only | joint_length | overlap |
|---|---|---|---|---|
| before Q8 (levers off) | 0.580 (0.598) | 0.50 | 0.526 (0.540) | 0.528 (0.549) |
| after Q8, all templates | 0.520 (0.526) | 0.50 | 0.512 (0.517) | 0.527 (0.533) |
| after Q8, `dev` half | 0.531 (0.539) | 0.50 | 0.514 (0.520) | 0.530 (0.535) |
| after Q8, `dev2` half | 0.515 (0.522) | 0.50 | 0.508 (0.513) | 0.525 (0.532) |

All three probes (and diff_only) pass the bar 0.55 (0.60) on all templates and on each half. Checks that make it hold by construction (`tests/test_msg_pool_t66.py`): swap groups equal as a
multiset (0 mismatches in 504 groups), every CH-trivial NO message matched on tokens, style and +-3 characters (368 / 368), no message under 4 tokens.

## 7. Other notes

* Pipeline behaviour (LP_COMMON, unchanged): the reuse ledger keys on the base group id, so the rows of a G13-retired MSG group still count against its refill and the refill is dropped as incomplete.
* SHAS.json = sha256 of every T66 `.py` / `.md` file (tests included, `solver_b/` and `__pycache__` excluded) plus `pools/msg_messages.json`; `_combined_code_sha256` = sha256 of the concatenated hex shas of
  the `.py` keys in key order. Rewrite from c21_fam/:
  `python3 -c "import hashlib,json,os;h=lambda p:hashlib.sha256(open(p,'rb').read()).hexdigest();ks=sorted(['T66/'+os.path.relpath(os.path.join(r,f),'T66') for r,d,fs in os.walk('T66') if 'solver_b' not in r and '__pycache__' not in r for f in fs if f.endswith(('.py','.md'))]+['T66/pools/msg_messages.json']);d={k:h(k) for k in ks};d['_combined_code_sha256']=hashlib.sha256(''.join(d[k] for k in ks if k.endswith('.py')).encode()).hexdigest();json.dump(d,open('T66/SHAS.json','w'),indent=1,sort_keys=True)"`
* HASH_EXPORT: `python3 -I c21_fam/LP_COMMON/hash_export.py T66` from c2_build/ (after the last edit of any T66 `.py` or test file); `LP_COMMON/tests/test_lp_hash_export.py::test_checked_in_export_is_current[T66]` checks it.
