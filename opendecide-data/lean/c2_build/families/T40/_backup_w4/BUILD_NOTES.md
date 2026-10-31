# T40 CALL-GATE: build notes (14 Oct 2026)

Status: built and tested in memory; no row, pool or sealed file exists on disk; no Haiku or model run. Template (program) text only.

## What exists (`c2_build/families/T40/`)
| File | Role |
|---|---|
| `G0_SPEC.md` | G0-lite (heads, all 15 options with one-line definitions, gold, verifier, held-out configuration, relations, balance). sha256 frozen in `T40Plugin.G0_SHA256` |
| `plugin.py` | `T40Plugin`: `design()` (stateless balance), `sample`, `solve_a`, `canonical`, `render`, `relations` (complement, twin, equiv, 3 metamorphic per head), error models |
| `resolver.py`, `schema.py`, `edit.py`, `edit_exec.py` | gold: closed-world resolver, own JSON-schema validator, slot ledger, head-C generator, hermetic str_replace + `ast.parse` executor (subprocess, `-I -B`, `PYTHONHASHSEED=0`, temp cwd, 5 s cap) |
| `world.py`, `pools.py` | registry generator: 16 domains x 5 tool templates, typed parameter templates, 8 naming styles, value pools |
| `solver_b.py` | verifier, paradigm sql_sqlite (own parser; relational anti-joins, `json_type`, BETWEEN, regexp UDF; head C by `re` + `compile(PyCF_ONLY_AST)`) |
| `fixtures.py`, `loader.py` | program-authored wordings / headers (stand-in G-LEX admissions) and runtime registration (`FAMILIES["T40"]`, `pilot_loaders.LOADERS["T40"]`) |
| `run_pilot_i1.py` | pilot runner (`--dry-run`, `--n`, `--no-g15`), T28 pattern |
| `test_t40.py` | 16 pytest tests |
| `haiku/author.py`, `haiku/tasks/*.md` (8 files, `manifest.json`) | Haiku task files (header skins per register; question wordings per qform) + admission checker `admit_skin`, `admit_wording`, `check_answers`. NOT RUN |

## Design in one paragraph
Three heads (A: 8-way call verdict, B: 3-way agent action, C: 4-way str_replace outcome), each as yes/no forms (positive, double negation, antonym, syntactic complement) and one closed choice form. Gold is label-first: `design(seed, sampler)` fixes the label, form, wording, overlay and gold position of a seed from the seed alone (128-seed blocks of groups: yes/no groups are two seeds with opposite gold and identical overlay, choice groups hold every label once), the world is drawn until solver A returns that label (drops are redraws, never relabels). Surface features that a label forces (duplicated tool, off-menu tool, Provider clause, earlier results, clause count) are drawn at equal overall rates on the other labels (`world.neutral_p`, `P_COLL_B`).

## Test results (`../.venv/bin/python -m pytest -q -p no:cacheprovider c2_build/families/T40`, from `lean/`, about 8 min)
16 passed: schema validator; pool consistency (no purpose inside another; no negation cue in pools; held-out styles / domains / packs disjoint); wording lint and negation profiles (G-SL, k_all / k_syn per kind); executor (MULTIPLE, APPLIES_ONCE, BREAKS_SYNTAX, NO_MATCH, non-overlapping count); `validate_plugin(strict)` == [], independence, distinct paradigms; resolver precedence; **solver A == solver B on 2,000 specs** (400 per sampler, render + parse + G3 facts + options); every label of every head reached; **determinism under PYTHONHASHSEED 1 and 777** (identical rows); in-memory build of **3,000 rows through `pilot.build_pilot`** with the loader registered at runtime (0 drops by any gate; G15 not run in the build, run separately on 400 and 300 rows: 0 failures); **G6, G7, G10 pass**; held-out samplers carry only held-out styles / domains / packs and `dev_only`; **3% reseed audit** (another random stream, same cells): 0 label flips of at most 1%.

## Measured numbers (3,000-row build, pilot.g6 / g7 / g10 / overlay)
- Rows: 3,001; yes/no 51.3%; 0 unit drops. Mean prompt about 680 tokens (3-chars-per-token estimate, instructions twice), max 1,167. Head A: 1,610 rows, **VALID 43.2%** (696); faults 38-183 each (BORROWED_SIGNATURE 38, lowest). Head B 705 rows (CALL 248, ASK 231, CANNOT 226); head C 686 rows (APPLIES_ONCE 207, NO_MATCH 207, MULTIPLE 137, BREAKS_SYNTAX 135).
- G6 (bar chance + 2 pp): yes/no a 0.473, c 0.492, d 0.498 (chance 0.500); choice b_options lr 0.2245 / gbt 0.2266 (chance 0.2611), a 0.1875 / 0.2266, c 0.2546 / 0.2266, d 0.1869 / 0.2635. **Options-only is below chance (-3.7 / -3.5 pp), not above:** exact label balance makes every cross-validation fold test on a deficit of the label it trained on. Formatting-only probe (lengths, line and bracket counts, register) on yes/no rows within 50 +- 3 pp, diff-size probe (head C yes/no, lengths of old_str / new_str) within the test's band (-8 / +6 pp, about 190 rows): both asserted in `test_formatting_only_and_diff_size_probes`.
- G7: 0 failing features of the tested features. G10: all checks pass (yes rate 0.500, yes = bad 50 +- 5, syntactic negation, double negation, gold position, longest option, per cell yes rate 50 +- 2).
- Overlay: complement 22.3% of yes/no, non-syntactic 33.7% of pairs, twin 20.5%, equiv 6.3%, unit size <= 3; attack 0 (no attack lines).

## Open items
1. **Per-head G6.** The pooled G6 passes; split by head, head B choice c_card lr 0.368 (chance 0.333, +3.5 pp, n=627) and head A / C choice d_meta gbt (0.198 vs 0.125 on n=288; 0.299 vs 0.25 on n=546) are above their own chance. Counts are small and the earlier source of a larger gap was fixed (unsupported purposes and generic clause labels only occurred on CANNOT rows; now drawn from other domains' real tools); re-check per head on the 5,000-row G6 sample.
2. **Spec 3.0 shares not met by program text:** 38 wordings (each about 2.6% of rows, bar 2%), 27 header skins (each feeds far more than 6 rows), 20 packs (domains + code vocabularies, bar 25). Run the Haiku tasks in `haiku/tasks/` (not run); then add pool loaders and freeze. Wordings are admitted by stand-in extractors `program:template-1/2`; real G-LEX needs 2 blind Haiku reads (`lexicon_items`).
3. **Mode T only.** No Mode F text: the user request is a program template (`Request: "<purpose>. <Label>: <value>."`). A Haiku paraphrase of the request would need a G3-H fact lock (values verbatim, labels recoverable).
4. BORROWED_SIGNATURE is 2.4% of head A rows (never in twin-carrying yes/no groups; it has no one-slot twin); head B has no twins.
5. Tokens are the 3-chars-per-token estimate; run `pilot.real_tokens` on the pilot rows (mean about 680 against the 800 bar).
6. Rows per skin / register: 7 training registers (each about 14%, bar 15%).

## Kit candidates (not applied; shared files untouched)
- `plugin.FAMILIES` has no T40 entry: `loader.register()` adds it at runtime (and `pilot_loaders.LOADERS`).
- `design()`-style stateless group balance (paired yes/no seeds, label-complete choice groups) is reusable by any family that needs exact per-wording yes rates.
- The hermetic executor pattern in `edit.apply_edit` (subprocess, `-I -B`, temp cwd, cache).
- G6 one-sided reading: a below-chance probe on an exactly balanced design should be reported as such.

## Commands (from `jev/opendecide-data/lean/c2_build`, `.venv` python)
- Tests: from `lean/`: `../.venv/bin/python -m pytest -q -p no:cacheprovider c2_build/families/T40`.
- Pilot, in memory: `../../.venv/bin/python -B families/T40/run_pilot_i1.py --dry-run --n 1000` (add `--no-g15` for speed). Determinism: run under two `PYTHONHASHSEED`s and compare `rows_sha256`. Without `--dry-run` it WRITES `pilot_i1/`: only on the orchestrator's go. (`--n 300` is below one design block per sampler: G6 / G10 cell checks fail there by sample size, as the first dry run showed; use 1,000 or more.)
- Sealed run (separate sealed agent, never here): `loader.register(); p = T40Plugin(lexicon=fixtures.make_ctx().lexicon); spec = p.sample(seed, "S5")` for a sealed seed range, `pipeline.build_unit(p, spec, ctx)`; S5 draws only the held-out domains (shipping, astronomy, veterinary, library), naming styles (camelCase noun-verb, dotted noun.verb, kebab), code packs (orbits, kennel, harbor), break operators (unterminated_string, stray_keyword) and header registers (transcript, form). All S5 rows are `dev_only`. `lean/ohs_ac_sealed/` was not created.
- Haiku tasks: `../../.venv/bin/python -B families/T40/haiku/author.py write` (rewrites `haiku/tasks/`), then one fresh Haiku agent per task file, then `haiku.author.check_answers(task_id, answers)`.

## A45 pre-freeze check (15 Oct 2026; in memory, no row on disk; backups in `_backup_a45/`)
Script: `_prefreeze/prefreeze_check.py` (`show.py` prints a result). Command (from `c2_build`): `../../.venv/bin/python -B families/T40/_prefreeze/prefreeze_check.py --n 7000 --out families/T40/_prefreeze/result_fix3.json` (about 20 min). Results kept: `result_base.json` (before), `result_fix1.json` (after fix 1), `result_fix3.json` (current).
Build 7,001 rows, 0 drops: head A 3,745 (yes/no 3,120, choice 625), head B 1,628 (yes/no 197, choice 1,431), head C 1,628 (yes/no 346, choice 1,282). Each head >= 1,000 rows; the (head, qtype) cells with n < 1,000 (A choice, B yes/no, C yes/no) are reported, not binding.

### Generator fixes (balance by construction; no G6 feature dropped, no relabel)
1. `design()` now fixes pack (domain / code vocabulary) and naming style per label group by cycling, and `world.draw` / `edit.draw` take them from the cell. Every card (sampler, head, pack) then holds whole label groups, so each card is exactly label-balanced. Effect: the inverse artifacts are gone (head A d_meta lr 0.045 vs 0.125, B yes/no a_question 0.28, pooled a_question 0.474 are now all within +-1 pp of chance) and options-only LR went from 0.2245 (-3.7 pp) to 0.2567 vs 0.2623 (-0.6 pp).
2. Head B CANNOT_ANSWER: the unserved request names a real tool of the SAME domain left out of the registry (was another domain's tool, whose foreign words were a bag-of-words tell). B c_card lr 0.368 -> 0.374 after the change (0.388 in the intermediate run): not enough.
3. Head C: every file holds a repeated fragment for every label (no measured effect: C d_meta gbt unchanged at 0.2808).

### Gates vs bars (7,001 rows; chance = mean 1/k as the kit's G6; bar chance + 2 pp)
| Gate | Value | Bar | Pass |
|---|---|---|---|
| program gates G2 G3 G4 G-SL G-LEX G-TW G15 schema options | all pass | pass | yes |
| G7 | pass | pass | yes |
| G10 | pass, 0 failing | pass | yes |
| G6 pooled yes/no (a, c, d; lr, gbt) | 0.496-0.500 | <= 0.520 | yes |
| G6 pooled choice | c_card lr 0.2852; d_meta gbt 0.2776 (chance 0.2623) | <= 0.2823 | NO (c_card lr +2.3 pp) |
| G6 head A (yes/no 3,120; choice 625) | all <= 0.1296 vs 0.125 (choice), 0.4926-0.5 (yes/no) | pass | yes |
| G6 head B choice (n=1,431) | c_card lr 0.3739 vs 0.3333 (+4.1 pp) | <= +2 pp | NO |
| G6 head B yes/no (n=197, small) | d_meta gbt 0.5482 (+4.8 pp) | <= +2 pp | NO (n < 1,000; noise band about 3.5 pp) |
| G6 head C choice (n=1,282) | d_meta gbt 0.2808 vs 0.25 (+3.1 pp) | <= +2 pp | NO |
| G6 head C yes/no (n=346) | <= 0.5145 | pass | yes |
| Options-only probe (pooled choice) | lr 0.2567, gbt 0.2597 vs 0.2623 (-0.6 / -0.3 pp) | +-3 pp | yes |
| Options-only per head | A 0.1168/0.0992 vs 0.125; B 0.3333; C 0.2371/0.2457 vs 0.25 | +-3 pp | yes (A gbt -2.6 pp, n=625) |
| Formatting-only, yes/no (acc vs majority) | all 0.4971 vs 0.5001; A 0.4946; C 0.4913; B 0.5431 vs 0.5025 (n=197) | +-3 pp | yes except B small cell (+4.1 pp, n=197) |
| Formatting-only on choice labels (extra probe: label from lengths, line, bracket counts) | pooled 0.338 vs 0.143; B 0.375 vs 0.333; C 0.387 vs 0.251 | +-3 pp | NO for C (+13.6 pp) and B (+4.1): see open item 1 |
| Reseed audit (3%, independent random stream) | 216 audited, 0 flips | <= 1% | yes |
| Prompt tokens | mean 675, max 1,186 | <= 800 / 2,000 | yes |
| Rows per card | max 88 | <= 64 | NO (card = sampler x head x pack; the kit caps per-card rows at selection time via mix; to check in `c2_select`) |
| A == B on 2,000 specs, determinism (2 hash seeds), pools, contract, resolver, label cover | 6 tests re-run after the edits | pass | yes |
| Diff-size probe | not required (T40 is not a coding-diff family) | n/a | n/a |
The formatting-only choice probe pooled over 8/3/4-way heads is not a clean statistic (its majority share is dominated by the head mix); per head it is the C line that matters: file length and shape predict BREAKS_SYNTAX / MULTIPLE / NO_MATCH because the edit itself changes them (a broken edit adds tokens, a duplicated fragment adds lines).

### Open items (family does NOT yet meet the A45 (d) freeze bar)
1. **Head C choice leaks through code-shape numbers** (d_meta gbt +3.1 pp; the formatting-only choice probe +13.6 pp). No single feature carries it (each alone is at chance; len_state, n_lines, n_numbers, mag_mean jointly give 0.278). Next fix: make the label-conditional shape equal by construction: the same file and the same old_str fragment for all four labels of a choice group (change only the edit: NO_MATCH corrupts old_str, MULTIPLE uses a count >= 2 fragment present in the same file, BREAKS_SYNTAX / APPLIES_ONCE change new_str to equal length). Needs a group-level shared file seed in `design()`.
2. **Head B choice c_card lr +4.1 pp**: surface rates per label are close (results 0.30 CANNOT vs 0.36; provider clause 0.33 CALL vs 0.37-0.39; tools 5.12 vs 5.25-5.30); top LR words are tool, provider and result-tool names (memorised vocabulary, ASK: redwood, northwind, find_item, resolve_ref; CANNOT: request verbs create, drop, read, write, play, commit). Next fix: share the registry (tools, providers, results) across a choice group and vary only the request / values; make P(results block | label) equal.
3. **Rows per card 88 > 64**: the card is (sampler, head, pack); more cards would need a finer pack key (for example pack x register) or the mixer's per-card cap at selection.
4. B yes/no (197 rows) and C yes/no (346) are small cells: raise the B yes/no share in `LAYOUT` (now 2/18 groups) if a binding per-cell G6 is wanted; at 7,000 rows only A yes/no, B choice and C choice have >= 1,000 rows.
5. Haiku tasks not run (as ordered). Earlier open items 2-6 above are unchanged.

### Sealed-run entry point (unchanged by the fixes; S5 only, never run here)
`from families.T40 import loader, fixtures; from families.T40.plugin import T40Plugin; from c2_kit import pipeline; loader.register(); ctx = fixtures.make_ctx(); p = T40Plugin(lexicon=ctx.lexicon); spec = p.sample(seed, "S5"); res = pipeline.build_unit(p, spec, ctx)` for each seed in the sealed range (N held-out items = N units' rows; S5 draws only the held-out domains shipping / astronomy / veterinary / library, styles camelCase / dotted / kebab, code packs orbits / kennel / harbor, break operators unterminated_string / stray_keyword, header registers transcript / form; all rows `dev_only`). The new design cell also cycles S5 packs / styles from the held-out lists only (`design()` uses `E.HELD_OUT_PACKS`, `P.HELD_OUT_DOMAINS`, `P.HELD_OUT_STYLES` when sampler == "S5"). Unreachable from S1-S4 by the sampler test `test_held_out_only_in_s5` (not re-run after the edits; the 7,001-row build used S1-S4 only).
