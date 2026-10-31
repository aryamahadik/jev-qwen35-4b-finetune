# Owner options for the OHS-AC stop (A62 c / A64) — built, NOT applied

Written 17 Oct 2026 by the orchestrator's builder. Both options are **default OFF**. Nothing here changes data, a QC record, a bar, PREREG_FINAL.md
or HANDOFF.md, and nothing was run on real data except two read-only counts commands (below). No Modal, no paid compute, no sealed folder opened.

**Pinned tools are untouched** (A64_TOOLS.md): `g13_c2.py 49f4c795…`, `mix_c2.py 3faaf07a…`, `c2_select.py 70cde02d…` have the same sha256 as before
(the tests assert the option names appear in none of them). The options patch the running process through thin wrappers; with no flag a wrapper
hands its arguments to the original `main()` unchanged.

## 0. How an option is armed (all options)

An option runs only if its flag carries an **owner-ruling id that exists in `PREREG_FINAL.md`**. The check (`ruling_gate.py`) refuses unless the
ruling block (a `> **Ruling <id> (...)` block) (1) exists once, (2) says "owner" in its header, (3) carries the option's marker word in its text.
Since 17 Oct 2026 the owner ruling **A68** carries `OHSAC_REPORT_ONLY` (option 3); no other id and no other option is armed (tested against the real
file). The marker must stand as a whole token on a line that starts `> Machine marker` (A68: `> Machine marker for the A68 switch (...): OHSAC_REPORT_ONLY.`);
a prose mention or a longer word never arms. A repeated flag is refused. The orchestrator writes a ruling, with its marker line, only after the owner
decides in words. A refusal changes nothing.

**A68 review fixes (17 Oct 2026; default OFF unchanged).** (1) marker = whole token on a `> Machine marker` line, (2) repeated flag refused,
(3) each captured split is sealed (`capture.set/run/log_tool_sha256/ruling/split_sha256`; a split moved, edited, copied from another log or captured
under another ruling is refused), (4) the ruling of the run must equal the ruling the logs were captured under (id and block sha256), (5)
`select_<FAM>.json` carries the `ohsac_report_only` block and the mix manifest lists which selections were made under the option, (6) `--remove-sources`
on a mix written under the option goes only through `mix_c2_opt3.py ... --ohsac-report-only <id>` (block carried over unchanged; the plain tool is
refused by the wrapper), (7) the G13-seed report of `gen_full_c2_opt3.py` names the templates not applied. Dry run of what the capture batch must
produce: `ac_report_only.py report --capture-plan`.

| option | marker word the ruling must contain | flag |
|---|---|---|
| 3  OHS-AC report-only | `OHSAC_REPORT_ONLY` | `--ohsac-report-only <id>` |
| 2 (a) own frame text excused | `OHSAC_FRAME_EXCUSE` (scope `code+pools` also `OHSAC_FRAME_POOLS`) | `--frame-excuse <id> [--frame-scope code\|code+pools]` |
| 2 (b) narrowed keyword export | `OHSAC_KW_NARROW` | `--kw-narrow <id> [--kw-dir DIR]` |

Skeleton of such a ruling (the orchestrator fills the words; the owner's own words are quoted):
`> **Ruling A68 (<date, time> UTC; owner decision in chat; orchestrator, Opus).** <the owner's words, quoted>. OHSAC_REPORT_ONLY: <what changes and
what does not>. <the counts reported to the owner before the decision>.`

## 1. OPTION 3 — "OHS-4 is the binding test; OHS-AC is report-only for C2"

**Effect (only under the ruling).** The three OHS-AC targets (`ohsac_hash`, `ohsac_rows`, `ohsac_gtpl`) and the OHS-AC-only seed quarantines leave
the *binding* drop set. Every other target stays binding exactly as now: the OHS-4 child (`ohs4_hash`, `ohs4_rows`, `ohs4_gtpl`), the sob / DI /
public targets, the C2 dev targets, A53 and A31 (b). The OHS-AC hits are still computed and logged, and are written as `ohsac_report_only` into
`mix_report_c2.json` **and** the mix manifest `c2_mix_manifest.json` (per log: counts and sha256 of the id lists; no ids, no text). The drop set is
the union over logs of the ids hit by at least one non-OHS-AC target (an id hit by both stays dropped). The A61 final-mix 8.5 source gate is not
touched (`--exports all`, stricter, as adopted; the tests check `gated_membership`, `binding_ids`, `remove_sources` are the same objects).
`drop_ids` in every log stays the full (stricter) set; the split is an extra key, so any consumer that does not know the option keeps the strict set.

**Files.** `ac_report_only.py` (library + CLI), wrappers `g13_c2_opt3.py`, `c2_select_opt3.py`, `mix_c2_opt3.py`, `gen_full_c2_opt3.py`, `ruling_gate.py`.

**Why a G13 re-run is needed.** A log's `drop_ids` is one flat list; the per-target ids are not kept, and counts cannot be turned back into ids.
The capture wrapper adds `drop_ids_by_class = {"binding", "ohsac_report_only", "units", "capture"}` to each record (same run, same cost, same
tool sha; `binding ∪ ohsac_report_only = drop_ids`, disjoint). Under the option a log that has an OHS-AC record but no valid split is **refused**
(never guessed); a log with no OHS-AC record (pre-A64) has no OHS-AC drops, so all its drops stay binding. Every completeness / staleness /
inputs-at-start check of the original tools runs first, unchanged.

**Exact commands** (run from `lean/`; `PY=../.venv/bin/python -B`; `OPT=c2_build/zed_orch/owner_options`; "…" = the arguments you would use anyway).

```
# dry, counts only, nothing written, no ruling needed: what the split gives for the logs on disk
$PY $OPT/ac_report_only.py report [--glob 'c2_*.json' 'acquick_c2_*.json']

# after the ruling (id A68 as an example):
$PY $OPT/g13_c2_opt3.py   candidates --block T28 … --ohsac-report-only A68        # adds drop_ids_by_class to logs/decontam_counts/c2_cand_T28.json
$PY $OPT/g13_c2_opt3.py   carry|final … --ohsac-report-only A68                    # same for the carry blocks and the final-mix G13
$PY $OPT/c2_select_opt3.py select --fam T28 --exclude-ids logs/decontam_counts/c2_cand_T28.json … --ohsac-report-only A68
$PY $OPT/mix_c2_opt3.py   --dry-run|--final --decontam-drops logs/decontam_counts/c2_*.json … --ohsac-report-only A68
$PY $OPT/gen_full_c2_opt3.py … --g13-seed T27 --ohsac-report-only A68             # only T27 honours the seed quarantine list today
$PY $OPT/ac_report_only.py seed-split --log logs/decontam_counts/c2_seed_T27.json --out <new file>   # optional: a mirror without the OHS-AC-only entries (never overwrites)
```
Without `--ohsac-report-only` each wrapper is the original tool. With an unknown / unmarked / non-owner id: `owner option refused: … the option stays OFF`, exit 1, nothing patched.

**Indicative effect (counts only; NOT a measurement of option 3).** Rows now dropped by OHS-AC (acquick logs, 17 Oct) against the drop counts of the
older complete full G13 candidates logs (`c2_cand_*`, which have no OHS-AC step and predate the A64 / sob / DI targets and some dev-file rebuilds, so
they can be stale). "Left under option 3" = rows − older drops; the binding run has to be re-done with the capture wrapper before any number counts.

| block | rows | left now (OHS-AC binding) | older non-AC drops | left under option 3 (indicative) |
|---|---|---|---|---|
| GB | 5,537 | 947 | 1,826 | ~3,711 |
| GW | 5,443 | 1,016 | 923 | ~4,520 |
| MD | 10,491 | 6,359 | 139 | ~10,352 |
| T01 | 2,391 | 0 | 97 | ~2,294 |
| T06 / T07 / T12 | 1,251 / 1,179 / 1,154 | 0 | 513 / 491 / 331 | ~738 / ~688 / ~823 |
| T15 / T23 / T24 / T25 | 1,328 / 1,057 / 847 / 894 | 0 | 129 / 323 / 573 / 556 | ~1,199 / ~734 / ~274 / ~338 |
| T26 / T28 / T29 / T30 / T31 | 1,857 / 3,151 / 2,667 / 1,977 / 1,475 | 0 | 455 / 721 / 63 / 136 / 60 | ~1,402 / ~2,430 / ~2,604 / ~1,841 / ~1,415 |
| T27, T32, T33, F4/F5/F6/F11, I10, DI-* | — | — | no comparable older full log on disk | not estimable |

So option 3 would take the C2 families from "0 left" to "most rows left" in the families that have an older log; the agent-core / 10-family floors of
A62 (c) would be tested again on measured numbers, not these.

**Tests.** `tests/test_opt3_ac_report_only.py` (25): ruling gate (unknown id, no marker, no owner, duplicate, other option's marker, real PREREG),
drop set = union of non-OHS-AC targets with the flag / unchanged without (select and mixer), an id hit by both stays, unknown ruling id refused and
nothing patched, incomplete logs still refused, log without a split refused, end-to-end capture through `g13_c2.run` (fake OHS-AC side, fake checkers),
withdrawn-waiver handling, seed quarantine split, manifest + report block, the wrappers delegate untouched without the flag, the 8.5 gate objects unchanged.

## 2. OPTION 2 — "allow shared templates" (design + code + sealed brief; not run)

### What the counts say (why this is two parts, and what it will not do)

From `logs/decontam_counts/acquick_c2_*.json` (units hit per method, not exclusive):

- **GB, F4, F5, F6, F11, MD, I10, DI-KR, DI-TS: `keyword` is the only OHS-AC method that hits.** Part (b) alone can free these (as far as the narrowed
  names do not occur). Part (a) does nothing for them.
- **Program families (T01 … T33): `keyword` hits ~every unit AND sentence / n-gram methods hit ~every unit** (e.g. T28: keyword 2,462 / 2,462; exact_sentence
  2,462; ngram10/12 2,462; exact_seg 2,462; tulu8 2,462). Both (a) and (b) are needed.
- **Methods option 2 does NOT touch still bind** (whole-text, containment, near-duplicate, shape). A unit that hits one of them still drops, so
  (a)+(b) frees the program families only partly. Lower bound of units that still drop after (a)+(b) = the largest such count:

| family | units | still drop at least | by |
|---|---|---|---|
| T01 / T24 / T29 | 1,870 / 686 / 2,066 | 506 / 247 / 617 | skeleton_line |
| T06 / T26 | 1,039 / 1,469 | 642 / 1,099 | skeleton_line |
| T28 | 2,462 | 1,383 | minhash (also exact_full 309, substring 344, skeleton_line 21) |
| T30 | 1,544 | 1,544 (all) | substring |
| T25 | 714 | 714 (all) | substring |
| T27 | 984 | 984 (all) | minhash |
| T31 / T32 / T33 | 1,127 / 730 / 2,616 | 1,081 / 640 / 1,893 | minhash / minhash / substring |
| T07 / T12 / T15 / T23 | 898 / 903 / 1,104 / 846 | 442 / 557 / 542 / 540 | skeleton_line / skeleton_line / minhash / skeleton_line |

So option 2 as specified is not enough for T25, T27, T30 and (almost) T28/T31/T32 on current counts. The next lever, **not built** and needing its own
owner word, would add `skeleton_line`, `substring` and `minhash` to the excusable set for text that lies inside own-family frame (the constants
`EXCUSE_*` in `frame_excuse.py`). Option 3 does not have this limit.

### (a) Own frame text excused — `frame_excuse.py`

*What is frame text (fixed now, from code, never from hits).* String literals of the family's program files (`g13_c2.CODE_FILES` + `AC_PROGRAM_FILES`;
the same units g13_c2 already builds as `code` / `ac_code`), docstrings out, cut at every placeholder and line break (`template_pieces`), pieces of
at least 6 words, **minus every literal inside a `HELD_OUT*` assignment or `held_out*` function** (the held-out values are instance content and keep
binding). Scope `code` (default); `code+pools` adds the family's pool templates and needs the extra marker `OHSAC_FRAME_POOLS`. A text is excused only
against pieces of **its own family** (row `meta.family`, else the set's block).

*How.* `ohsac_stage` runs twice: unmasked (all methods) and on a copy where every frame piece is replaced by one sentinel word. From the masked pass
it takes `exact_sentence, ngram10, ngram12` (hash), `exact_seg, ngram10, ngram12, tulu8` (rows checker), `gtpl8` (G-TPL). From the unmasked pass it
keeps everything else (`exact_full/raw`, `substring`, `minhash`, `keyword`, `skeleton_*`, `structure_g13`). Whole-text methods are excused only for a
**pure-frame unit** (every text of the unit is nothing but own frame once masked). So an instance-level sentence or n-gram (text around the frame, or
frame spliced with a held-out value) still drops the unit. The record gets `ohsac.frame_excuse` (ruling, scope, units hit before / after, units
excused, pairs per method; counts only). Cost: the OHS-AC step runs twice (about +20 min per full candidates batch; the OHS-AC-only candidates batch of 17 Oct took about 21 min, the slowest
record in the acquick logs).

### (b) Narrowed keyword export — `keyword_rule.py`, `keyword_narrow.py`, `OPT2_SEALED_BRIEF_KW.md`

*Rule, fixed before running* (`keyword_rule.py`; its sha256 is stamped into the export and checked): keep a held-out name or source identifier if it is
multi-token, or identifier-like (digit or `/ . _ @ : #`), or a single token of >= 5 characters with `wordfreq` (3.1.1, large list) Zipf < 3.0; drop
the rest. A **fresh sealed agent** (brief: `OPT2_SEALED_BRIEF_KW.md`, no C2 hit data in its prompt) writes `c2_build/sealed_hashes_ac_kw2/` (hash-only).
*C2-side switch* (`--kw-narrow <id>`): `g13_c2.AcSide.load` verifies the export (sha, rule sha == `keyword_rule.py` now, parent MANIFEST sha == the
OHS-AC export now, **narrowed ⊆ full by hash**, 0 < narrowed < full, counts add up) and swaps only the `keyword` set; any problem stops the run (no
silent fallback). The two narrowed files join the run-input guard. The C2 side never tests which common words are in the export (that would be a
probe); it relies on the rule sha, the subset check and the agent's counts. `ohsac.keyword_narrow` records ruling, counts and shas.

**Exact commands.**
```
# sealed side (after the ruling; one fresh sealed agent, brief OPT2_SEALED_BRIEF_KW.md); then, C2 side, counts only:
$PY $OPT/keyword_narrow.py verify                                   # prints ok + counts, or the refusal
# early OHS-AC check with the options (drops only, as A64 f allows):
$PY $OPT/g13_c2_opt2.py candidates --ohsac-only --frame-excuse A70 --kw-narrow A71          # any subset of the flags
$PY $OPT/g13_c2_opt2.py carry      --ohsac-only --frame-excuse A70 --kw-narrow A71
# binding runs: the same flags on candidates / carry / final (without --ohsac-only), then select and mix as usual (they see smaller drop_ids)
```
`g13_c2_opt2.py` takes `--frame-excuse`, `--frame-scope`, `--kw-narrow`, `--kw-dir` and `--ohsac-report-only`; with none of them it is `g13_c2.py`.
A log made with option 2 carries its stamp (`ohsac.frame_excuse`, `ohsac.keyword_narrow`) and the ruling id; `drop_ids` of such a log is the *reduced*
set, so a log made under option 2 must not be mixed with logs made without it.

**Time estimate (option 2), wall-clock after the owner decides.**

| step | who | time |
|---|---|---|
| ruling text for (a) and (b) | orchestrator | 15–30 min |
| narrowed export: fresh sealed agent (read builder, pin wordfreq, run, 5 self-checks, `verify`) | 1 sealed agent (Sonnet code, Opus review), CPU only | 1.5–2.5 h |
| orchestrator review of the counts + `verify` | orchestrator | 20–30 min |
| early OHS-AC check with (a)+(b) over candidates + carry | CPU, no Modal | 45–60 min (two passes) |
| **first measured numbers** | | **about 3–4 h; budget 5 h** |
| then the binding G13 reruns the plan needs anyway | | as planned (hours, parallel by block) |

Expectation, honestly: (b) should free the keyword-only blocks (GB, F-blocks, MD, I10, DI-*); (a)+(b) frees the program families only up to the lower
bounds in the table above, so the outcome for the 10-family and agent-core floors is **unknown until measured** and, on current counts, at risk for
T25 / T27 / T30. No family is re-opened and no bar moves because of this document.

**Tests.** `tests/test_opt2_frame_and_keywords.py` (40): the keyword rule (every branch, zipf asked only when needed), the narrowed export (good +
15 bad variants refused), the keyword compare with the full vs narrowed set (only `keyword` changes), install/guard/no-fallback, frame pieces from
code only and never held-out values, token-exact own-family masking, the two-pass stage on a synthetic family (own frame + clean instance excused;
keyword, instance n-gram, other family's row, whole-text match, frame+instance whole-text match all still hit; pure-frame unit excused whole), the
launcher (no flag = original, 8 refusals patch nothing, each option arms alone), the real PREREG arms nothing, pinned tools unedited, the real
`sealed_hashes_ac_kw2/` does not exist.

## 3. Files

`ruling_gate.py`, `ac_report_only.py` (opt 3), `g13_c2_opt3.py`, `c2_select_opt3.py`, `mix_c2_opt3.py`, `gen_full_c2_opt3.py`, `frame_excuse.py`,
`keyword_rule.py`, `keyword_narrow.py`, `opt2_launch.py`, `g13_c2_opt2.py`, `OPT2_SEALED_BRIEF_KW.md`, `tests/`.
Run all tests from `lean/`: `../.venv/bin/python -B -m pytest -q c2_build/zed_orch/owner_options/tests/` (about 1 min; the gen_full_c2 import is the slow part).
Existing suites re-run green with the pinned tools unchanged: `test_g13_c2.py` 94, `test_mix_c2_g13_logs.py` 28, `test_c2_select.py` 53.

## 4. What was read and run while building this (disclosure)

- Read-only counts commands on real logs: `ac_report_only.py report` (acquick and older c2_* logs) and the counts tables above (JSON counts only).
- Two files with restricted-looking names were opened before the constraint was applied: `c2_build/tests/test_g13_c2_ohsac.py` (C2-side synthetic-data test; read
  in part, and its suite run once) and `c2_build/zed_orch/AC_SEALED_BRIEF.md` (the C2-side brief for sealed agents, read in part). Neither holds sealed content; nothing
  from either was copied except the general layout of the brief. No `ohs*` data path, no `ohs4_sealed`, `ohs_ac_sealed`, `sealed_hashes*` file, preread, quarantine,
  LongBench, Jev output, `~/.claude` or scratchpad script was opened. All new files avoid "ohs" in their names for that reason.
