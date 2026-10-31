# mix_c2.py for A42-D and A45: what changed, the interface, the open items (15 Oct 2026)

Files: `c2_build/mix_c2.py` (edited), `c2_build/tests/test_mix_c2.py` (updated where the design changed),
`c2_build/tests/test_mix_c2_a42d.py` (new, 31 tests). Backup of the originals: `c2_build/_backup_a42d_mix/`.
Tests: `test_mix_c2.py` + `test_mix_c2_a42d.py` = 59 passed; `test_c2_select.py` + `test_gate_c2.py` = 44 passed.
No shared file was edited (c2io.py, c2_select.py, c2_kit/**, pilot*.py, g13_c2.py untouched). No row, pool or file was written
to the C2 tree; no commit.

## 1. What is implemented (task item -> code)
1. **T_max** (A42-D 2.3): `t_max_usd(spend)` = min(34, 32 - spend); `--spend-to-date` is a required argument. Negative, NaN or
   non-numeric spend refuses; T_max <= the $2 smoke refuses ("no training budget": stop and ask). `BUDGET_USD` (17.0) is gone;
   `budget_factor(proj, rnd, t_max, rows)`. The projection (`project_cost`) is unchanged and still compares `total_usd` (train +
   $2 smoke) with the limit, as the $17 did.
2. **125,000-row cap** on the whole mix incl. every twin: `ROWS_MAX`; it triggers the same trim as money (factor = min of both),
   and `share_checks` refuses a final mix above it.
3. **Trim order** (`budget_trim`, `TRIM_ORDER`): item10 -> wave2 -> meta_tail -> proportional. Seeded (20261013) whole-unit removal
   (`remove_groups`, `trim_blocks`, `trim_meta_tail`); each step is used up (`exhausted_steps`) before the next starts; after each
   step the replay is cut to floor(1.5 x new) (`replay_to_rule`; removing a new row takes about 2.5 rows in all, which sets how
   many new rows a round asks for). Item 10: hook `ITEM10_BLOCKS = ("I10",)` (not built for C2, A45 f; nothing there is removed).
   Wave 2: `WAVE2_NEW = (T44, T45)` in proportion (only T44 exists; T45 is C3). Metadata tail: whole tasks above 8,000, a task is
   skipped if removing it would put a source above 15% or a domain above 20%, leave < 8 domains, drop a source under 30%
   card-free, empty a source or take the block below 8,000 (a rule the block already breaks is only required not to get worse).
   Proportional: `scale_plan` + `apply_targets` (metadata by whole tasks per source via `reduce_meta`; G-block by `c2_select.reselect`
   then `fit_block`). Floor: 50,000 rows -> `SystemExit` in --final, a problem line in --dry-run. `BUDGET_ROUNDS` 4 -> 10 because
   steps 1-3 are sized from the 2.5 factor and the cost is not exactly linear.
4. **New blocks** through the same `out/ + MANIFEST + qc/QC_REPORT.json + crowd_c2/select_<B>.json` interface:
   - `GB` G-block (target and cap 15,000 incl. twins; twins <= 5,000; no domain > 20%; yes share 40-60% per yes/no card with >= 10 rows).
   - `MD` metadata (cap 12,000; floor 8,000 unless step 4 trimmed it; twins <= 5,000; source <= 15%; domain <= 20%; >= 8 domains;
     >= 30% card-free per source; <= 200 rows per task; 40-80 tasks per source checked on the loaded block, <= 80 always).
   - `RTW` replay yes/no twins: replay side (`REPLAY_SIDE = (replay, RTW)`), counted inside floor(1.5 x new); T37b + RTW <= 10,000
     (so RTW <= 8,000 with the original 2,000); the sampler draws `replay_sampler = floor(1.5 x new) - RTW`.
   - `T40..T44` (budgets 1,333 / 1,166 / 1,333 / 1,166 / 833; together <= 6,666, scaled in proportion if above). All count in the agent tier
     (`AGENT = c2io.AGENT + T40-T44`). Agent-cap overflow scales T40-T44 down first (in proportion), then the older agent families.
   - `fit_block` brings GB / MD / RTW inside their caps at load (twins, size, domain, source) by whole-unit (metadata: whole-task)
     removal only. Nothing is relabelled or edited.
   - Entry of T40-T44 needs a pilot verdict: `data/c2_parts/<T>/qc/PILOT_GATE.json` (see 3) and QC by Mon 19 Oct 23:59 UTC.
     They never count toward the 10 program families.
5. **Caps asserted on realised rows** (`cap_checks`, `share_checks`, `block_rules`): family <= 2,400 (blocks use their caps); agent tier
   (incl. T40-T44) <= 55% of new; free-form <= 25% per family (T07, T32 40%); every new row <= 2,000 tokens and block mean <= 800;
   yes/no 45-55% of new rows (unchanged reading); easy <= 25%, hard <= 30%; no ordinal, soft-label or S5 / dev_only row; **<= 64 rows per
   card** for the 17 families and T40-T44 (new); new <= 40% (3 new <= 2 replay + 1: the one-row slack is floor rounding) and replay
   side == floor(1.5 x new); total <= 125,000; T40-T44 <= 6,666; twin caps; T37b + RTW <= 10,000.
6. **OHS4_MANIFEST_SHA256** = `c0217e7739c570b9d22176b68e1c489623dcd5f7c551011606b6ff17e59c09c3`. Confirmed: it is on PREREG line 2025,
   inside the Ruling A38 block (lines 2021-2073); a test re-checks it with `ohs4_problem`.
7. **Deadlines.** The old constant was Tue 20 Oct 23:59 (A37 d). Binding: **A39 (g) and A42-D 1.6: Wed 21 Oct 23:59 UTC**
   (`CUTOFF_UTC = 2026-10-21T23:59:00+00:00`, A40 d and the A42-D text agree). For T40-T44 the QC `passed_utc` and the pilot verdict must be by
   **Mon 19 Oct 23:59 UTC** (A42-D 1.6 / 3.6: iteration-2 results due then; later = C3) -> `NEW_FAMILY_DEADLINE_UTC`.
8. **Never-train guard** (A42-D 13.1): `MixInputLog` refuses (a) any path with "ohs" in a part (covers `data/ohs3*`, `ohs3_parts/`,
   `ohs4_sealed/`, `ohs_ac_sealed/`), (b) the G-proxy file by path and by sha256, (c) every path / sha256 in the never-train manifest;
   `filter_train_globs` expands and filters the `--decontam-drops` lists (excluded names are reported in the run record);
   `anchor_row_problems` refuses training rows whose source / text-source dataset is a manifest anchor name. `--final` requires
   `--never-train-manifest` and `--gproxy-file` (existing files). Dry run works without them.

## 2. Reading choices to confirm (each is one constant or one function)
- **RTW is replay-side.** A42-D 7.2 says replay twins count inside the replay budget, so RTW rows are not "new" and get no 1.5x replay.
  T37b stays a new block (spec 5.1) and counts in the 10,000.
- **Per-card yes/no band for GB** (A42-D 5.5) is asserted only for cards of >= 10 rows that are all yes/no (a smaller card cannot hold 40-60%).
- **Yes/no 45-55%** keeps the old reading (share of yes/no rows among all new rows, GB and MD included). The G-block is about half yes/no,
  but if MD is mostly yes/no this check can fail and --final will refuse; that is a mix-composition question for the orchestrator.
- **Metadata step 3 does not protect "40-80 tasks per source"**; A42-D 2.3 names only the source and domain rules. It is reported.
  After step 4 the 8,000 floor is waived (step 4 is a proportional trim of every block).
- **Pilot verdict by numbers**, not by a flag: gain >= +2.0 pt, existing-dev drop <= 0.5 pt, G-proxy CI upper bound >= -0.5 pt (A42-D 4.2, 4.3).
- **A37 (k)** (training steps 100-300 projection above T_max) belongs to the launcher / preflight, not to the mix. The mix only trims.
- Mixer helpers copied from round 1 that treat "not replay" as new (`g10_checks`, `unit_check` ...) also see RTW rows; they are hard-label
  twin rows, so G10 counts them with the new rows.

## 3. Interface other agents must produce (nothing of this is on disk yet)
- Block dirs `data/c2_parts/{GB,MD,RTW,T40..T44}/out/{candidates_c2.jsonl, candidates_c2.relations.jsonl, MANIFEST.json (parents)}` and
  `qc/QC_REPORT.json` (pass, passed_utc, fix_iterations, files{sha256}), plus `crowd_c2/select_<B>.json` (candidates_sha256, target =
  `mix_c2.TARGETS[B]`: GB 15000, MD 12000, RTW 8000, T40-T44 as above; GB / MD / RTW may fall short).
- Row meta keys the mixer reads: `meta.domain` (or top-level `domain`, or `domain_pack`), `meta.card_id`, `meta.task_id` (metadata: all rows of a
  task incl. twins), `meta.twin_of` (a negation-twin row names its base row; GB / MD twin caps use it), row `source` (metadata source),
  `card` text (empty = card-free), `meta.difficulty_bin` / `crowd_pg` from the crowd step.
- `qc/PILOT_GATE.json` for T40-T44: `{"verdict": "PASS", "logged_utc": ISO+offset, "own_dev_gain_pt": x, "existing_dev_drop_pt": y,
  "gproxy_change_ci_upper_pt": z}`.
- Never-train manifest: any JSON; the mixer collects strings under path/paths/file/files keys, 64-hex strings, and name/names/source(s)/dataset(s)/anchor(s).

## 4. Open items (shared files I did not touch)
1. `c2io.TARGETS` / `c2_select.available()` do not know T40-T44, GB, MD, RTW, so the crowd step (`c2_select.py select`) refuses them until
   `c2_select`/`c2io` register those blocks with the targets above (`mix_c2.TARGETS` is the list). The mixer itself accepts them.
2. `gate_c2.py` / the training launcher need `spend_to_date` and T_max from the same rule (use `mix_c2.t_max_usd`).
3. A real-data dry run was not made (no C2 rows exist); the fabricated-fixture flows (T28, T01, T44, GB, trim by wave 2 first) pass.
4. The test fixture's fabricated replay pool grew from 900 to 1,800 rows (quota 600 per source) so the new-block flow can reach floor(1.5 x new).
