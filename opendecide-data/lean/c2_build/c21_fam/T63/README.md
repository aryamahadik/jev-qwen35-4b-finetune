# T63 (NEAR, EXISTS, LIC): notes

Code only, no rows. Rows wait for the data freeze, the registry sha, manifest v1.2, a signed stamp service and a signed conformance record.
MAL (DataDog) is not built here. Solver B is a separate session (`solver_b/`, ROW_SCHEMA.md contract).

Assumption carried from `near.py`: "an established entry Q" in NM-T1..NM-T7 ranges over the entries of the QUERY's registry.

## Opus ruling Q3 (Sun 18 Oct 2026, recorded before any pool rows)

Source: `zed_orch/c21/families/RULINGS_T59_T60_T63.md`, section Q3.

### 3a. EXISTS-B and LIC sources (implemented, generator side)

* EX-B1 and EX-B2 rows are built only from the sha-bound L-0 image-record stdlib symbol export (3 identical runs, declared sha, image id).
  LIC rows are built only from the hashed Opus table T63-LIC-TABLE (separate fresh Opus session). EX-A rows and NEAR rows need no external source.
* `pool_writer.write_pool` is the only path from kept rows to a pool file. It refuses:
  * anything but the literal `standin=False`;
  * a fixture-flagged source, or any source or row whose sha is a fixture sha (also when the `fixture` flag was stripped);
  * EX-B rows without the real export AND the L-0 image record, LIC rows without the real table AND the Opus table record
    (`SourceMissing` names each missing file and who produces it);
  * an export sha / image id / table sha that is not the one RECORDED by the L-0 image record / the Opus table record;
  * a row whose spec, witness or manifest pins disagree with the bound source (EX-B1 carries `export_sha` in the witness too), whose gold is not the
    real membership / table label, whose B1 list is not the export slice, or a LIC cell used twice;
  * unstamped rows and the test double's stamp. It writes all-or-nothing and never overwrites a batch file.
* The generator raises when its source is absent (`gen_b`, `_generate_lic`, `solver_a.make_gold_a`) and a production `Ctx` refuses a fixture sha.
* Solver B's abstain-on-missing-sha behaviour is a B-side change (separate agent; not in this folder's generator files).
* The fixture K1 log counts only as build-stage evidence (G0-lite risk 6 / T63-B8). Production K1 is the per-row read at creation, on the real sources.

### Production sources (checked Sun 18 Oct; nothing is faked)

Default folder: `zed_orch/c21/l0/` (override with `base_dir`). The file NAMES below are what `pool_writer.SOURCES` reads.

| role | file | status | produced by | must contain |
|---|---|---|---|---|
| stdlib_export | `T63_STDLIB_EXPORT.json` | MISSING | L-0: image build, `runner.stdlib_export.python / .node / .go` on the pinned image (Wed 21 Oct sandbox sign-off) | `ExportSet` JSON: `fixture` false, `image_id`, `export_runs` >= 3, `exports{python,node,go}`, declared `sha256` |
| image_record | `L0_IMAGE_RECORD.json` | MISSING | L-0: the image record of that same image | `image_id` and `stdlib_export_sha256`, written before any EX-B row |
| lic_table | `T63_LIC_TABLE.json` | PRESENT (sha 81fe96f7...28eb) | a SEPARATE fresh Opus 5.5 high session (T63-B6) | `LicTable` JSON: `fixture` false, every dep x project x use x dist cell, declared `sha256` |
| lic_table_record | `T63_LIC_TABLE_RECORD.json` | PRESENT | the same Opus session | `table_id` = `T63-LIC-TABLE` and `sha256`, written before any LIC row |

Until the two L-0 files exist the writer raises `SourceMissing` for any batch that holds EX-B rows. Re-run the B harness and K1 on them once they exist.

### 3b. NEAR corner "age >= A2, low downloads" (no code change; out of scope by the G0-lite text)

The corner is a near entry Q with age >= A2 but downloads below D2 (so not "established"), everything else as for a squat. Such a NO row fits none of the closed
NO kinds NM-R1..NM-R4: no registered construction id (K17), no quota in the closed shares. The generator must NOT add it. The downloads conjunct of
"established" stays covered by the gold function, its unit test (conformance T63-CM-06) and the rendered definitions block.

Report disclosure line (verbatim, for the T63 section of the C2.1 report):

> downloads is never the deciding conjunct of 'established' in a C2.1 NEAR row

C2.2 item: a new NO kind with its own registry id, NM-R5 "old but not popular" (near entry Q with age >= A2 and downloads below D2, publisher differs, no
fork / same-org edge, age(P) < age(Q): label NO because Q is not established). Putting it in C2.1 would need an Opus G0 amendment before the Thu 22 hash
export; that is not ruled.

## Opus ruling Q5, before any pool rows (Sun 18 Oct 2026): LIC quota against the hashed table

Source: `zed_orch/c21/families/RULINGS_T59_T60_T63.md`, section Q5. Option (a), resize and substitute; the family stays 1,200 rows; no bar changes.
Block sizes: NEAR 550, EX-A 290 (EX-A1 160, EX-A2 130), EX-B 250, LIC 110 = 1,200.

* The hashed table (sha 81fe96f7c803da485fa26d1f1664dac626d0b53ed09755249daa5603113228eb; 1,920 cells: COMPATIBLE 1,550 / REVIEW 330 / INCOMPATIBLE 40) has only 40
  INCOMPATIBLE cells and a cell is used once, so INCOMPATIBLE <= 34 kept (34 x 1.15 = 39.1) and K10 (each label 30-40%) caps LIC at 113 rows.
* LIC = 110 kept rows: COMPATIBLE 38 / REVIEW 38 / INCOMPATIBLE 34 (34.5 / 34.5 / 30.9%). Generation draws at most 44 / 44 / 40 cells (`config.LIC_DRAW`), so all 40 real
  INCOMPATIBLE cells are used, each once. Cells are drawn stratified by LABEL only. At least 33 of the 110 rows are in one-axis-flip pairs (17 pairs kept, 20 drawn), and
  >= 50% of the pairs flip on usage mode or distribution (K10 axis reading). The LIC pairs are generated before the LIC singles so the last INCOMPATIBLE cells go to singles.
* The freed 90 rows move by substitution: NEAR 500 -> 550 (YES 275 / NO 275; `near_plan.GROUPS_550`, K13 shares unchanged), EX-A 250 -> 290 (EX-A1 160, EX-A2 130; YES = NO).
  EX-B stays 250 (bound to the pinned export; risk 2 allows EX-B2 to shrink, not grow).
* Pilot = 600: NEAR 275 / EX-A 145 / EX-B 125 / LIC 55 (replaces 250 / 125 / 125 / 100), `config.PILOT_ROWS`; `build_plan(total=600, oversample=False)` lands on exactly these.
* Every LIC row is bound to the table sha and its cell id (`construction_id` = `LC:dep|project|use|dist`); `pool_writer.write_pool` checks both against the Opus table record.
* Cell use: a cell is "used" by a row that enters the pool. Oversample rows truncated after drops, and pilot rows discarded by the one fix iteration, are never trained, so their
  cells are released (a post-fix re-read with new seeds may draw them again).
  * Inside a run: `checked.run` wraps the stamp hook in a `KeptTracker`; at every refill round `CellPicker.release_unkept` hands back the cell of each row of an EARLIER round
    that did not enter the pool (answer-check drop, G13 hit, retired group) so the refill can draw it again. Rows of the current round are pending and never released; a row
    the tracker cannot prove dropped counts as kept, so a cell is never handed out twice. A builder error after a draw releases its cells too.
  * The cut: `lic.cut_to_quota` / `checked.cut_lic(rows, seed, total)` takes the surviving LIC rows (up to 44 / 44 / 40) to the kept quota (38 / 38 / 34; 19 / 19 / 17 at the
    pilot). Over-quota labels lose SINGLES first (an orphan counts as a single), in the order of sha256(seed | row_id); a pair member goes only when no single of an over-quota
    label is left. Deterministic per seed. Inputs are row_id, gold, pair_id and the seed ONLY: no model score, no row text, no spec field. `report["pair_ok"]` flags fewer than
    33 rows in complete pairs. Apply `cut_lic` before `write_pool`.
* Names manifest v1.2: no impact (all 16 ids are in `fixed_real_licence_ids`). Table author: nothing to do.
* C2.2 item (from the ruling): a project axis chosen for coverage of real project licences, written by a separate Opus session. Not adopted for C2.1.

## Opus ruling Q7, before any pool rows (Sun 18 Oct 2026): LIC gates after Q5. No bar changed.

Source: `zed_orch/c21/families/RULINGS_T59_T60_T63.md`, section Q7.

* K10 format part, amended before the pilot by **Opus Q7b: K10-F, a construction assert** (PRE-FREEZE KILL, 100%, no p-value threshold). Reason: on pure noise at k=3, n=110 the
  probe's 97.5% bound is about 0.40-0.44, above the 39.3% bar (and the permutation check holds in about half the runs), so correct data cannot pass (precedent T63-M4).
  * (a) Code level, re-run at every code sha (CPU tests + `lic_format.static_problems`, also inside the gate): every format choice of a LIC row (card layout, field order, wording
    id, template id, option order) is `lic_format.draw(seed, row index)`; the function takes no label and no licence cell (static check on its parameters and names); regenerating
    with the labels permuted, or with the licence cells swapped (another table), gives byte-identical formats on every row (`tests/test_q5_t63.py`).
  * (b) Exact replay on 100% of built rows (`gates.k10_f_construction`, in `run_all`): from the (seed, index) recorded in `meta.lic_format`, each row's wording index, option
    order, template id, card layout and field order replay exactly; layout and order are single-valued; row indexes are unique; the K14 wording cap holds. The wording draw
    is least-used-first by construction (round r = index div W is a seeded permutation of the pool). Row index = place in the LIC block in gid order (pair / single structure only);
    a refill takes a fresh index range, so a retired group is never re-worded.
  * The probe stays REPORT-ONLY beside the assert (`gates.k10_format_probe`, `ok` always True): shared L-0 harness (`LC_COMMON.probe.kway_probe`, harness 4896b2d5, its own
    permutation and leak checks), RAW 0/1 indicators (`indicator_matrix`, `raw_cols`) of exactly K10's features (card layout, field order, wording id); status PASS / FAIL / INVALID,
    n, validity flags and the noise bound for that n.
  * Noise-simulation record (seeded, reproducible, `gates.k10_noise_simulation`, stored in `K10_NOISE_SIM.json`; 200 simulated blocks per n, formats from the real draw, labels an
    independent balanced assignment; the owner report states the gate-form change, its reason and this record): n=55 ub median 0.320 (p97.5 0.389), permutation pass rate 0.00
    (all INVALID); n=110 ub median 0.399 (p97.5 0.508; 46% of blocks within the 39.3% bar), permutation pass rate 0.67, statuses PASS 62 / FAIL 72 / INVALID 66.
  * All other K10 parts stay binding: table sha, each cell once, label shares 30-40%, label-stratified draw, axis-reading shares (`gates.k10_lic`).
  * Binding K10-F reads: the pilot (55 LIC rows) and the built family (110); the earlier probe-based "one combined fix" path for K10 no longer applies.
* K12 ladder (Q7b). LIC is on the ladder through M-CELL; on the hashed table every cell is one axis from a flip, so every LIC row is M-CELL HIGH = L3 and L4 cannot occur. The
  generator does NOT invent a narrower distance measure or pick cells by level. NEAR and EXISTS plan their levels (`config.NON_LIC_LEVEL_WEIGHTS`: 22.0 / 33.0 / 22.9 / 22.0%) so the
  FAMILY composition L1 20 / L2 30 / L3 30 / L4 20 holds with LIC's 110 rows (9.2% of the family) at L3. The LIC twin is the one-axis-flip partner.

Dry-run read (build-stage DIAGNOSTIC; real hashed table, stand-in plumbing; seeds 1-5 each at the pilot (600 rows, LIC cut to 55) and the family (1,200 rows, LIC cut to 110)):
* K10-F holds on 100% of the rows on all 10 runs (drawn 64 / 128 rows and kept 55 / 110: 0 replay failures, layout and field order single-valued, K14 cap holds).
* The other K10 parts hold on all 10 runs: kept 19 / 19 / 17 and 38 / 38 / 34, label shares 34.5 / 34.5 / 30.9%, 22 / 40 rows in complete pairs, mode-flip share 0.73 / 0.70,
  mixed-pair share 0.63-0.78, each cell once, one table sha.
* Report-only probe (never a kill): pilot INVALID on 5 / 5 (n=55, noise permutation pass rate 0.00); family FAIL, PASS, FAIL, FAIL, INVALID (bal_acc 0.24-0.38, ub 0.32-0.47 against
  the noise median 0.399).

Report line (verbatim, for the T63 section of the C2.1 report):

> LIC rows are single-level (L3, M-CELL HIGH) on the hashed table
