# RUNBOOK: C1 read of the round-1 replay draw (free L4)

Spec: `C_DATA_SPEC.md` v4 section 5 ("C1 anchor targets", "Low-confidence replay rows"); recipe v4 section 3.
Sampler: `c_build/replay_sample.py`. Dry-run counts: `c_build/replay_counts_dryrun.json` (3 Oct).
Cost: $0 (Google credit L4, decision 3). This is not a GO point. It never runs on Modal or the H100.

## 1. What is read

| Item | Value (dry run, 3 Oct) |
|---|---|
| Round-1 draw (90,000 + 10% margin), nested in the round-2 draw | **99,069 rows** (85,352 relation units, 118 sources; A8' whole-source rule, 3 Oct 19:22 UTC) |
| Choice rows (read twice: given order + exact reversal) | 34,956 |
| Yes/no rows (read once) | 64,113 |
| **Forward reads** | **134,025** |
| Old slice (monitor; same session, optional but needed later anyway) | 2,000 rows, about 2,700 reads |
| Shards | 20 x about 5,000 rows (`data/c_replay_r1_shards/`); old slice: 1 shard (`data/c_old_slice_shards/`) |

Readout = the shipped A5 readout: choice rows given order + exact reversal, averaged; yes/no rows one read; T = 1
(raw softmax); merged adapter; bf16; no `--perm-seed`. In `od_gcp.py` this is `--tta-choice` without `--tta-noul`.

## 2. L4 time estimate

| Basis | Rate | Round-1 read |
|---|---|---|
| 4B-E label audit on this L4 (`logs/audit_label.log`, 30 Sep): 15,590 golden_train rows (<= 150 per source), 1 view, merged 4B, 4,491 s | 3.47 reads/s | 10.8 h (scaled by reads) |
| Same, scaled by prompt characters (draw: 1,989 chars per read vs 1,814) | | **11.8 h** |
| C1 dev reads on this L4 (`preds_dev/q35_4b_main500k.meta.json`): 10,795 rows in 2,249 s | 4.8 reads/s | 7.8 h (shorter rows; lower bound) |

**Plan: about 11-12 L4 hours** for round 1 (about 35 min per 5,000-row shard), plus about 15 min for the old slice
and 1-2 min of model load. The recipe budgets 20-28 L4 hours for the whole scoring crowd. Round 2 (if it runs)
reads about 134K more (its fresh half only). That run is not done now.

Ways to finish sooner without changing the read:
- **Start right after the G14 commit.** The draw depends only on the deny-list verdicts, not on any
  family, pack or public builder. So the 11-12 h overlap steps 2-8 of the build and stay off the critical path.
- **Two L4 VMs** (needs a second L4 with the same image, base cache and adapter): VM A reads the even shards and VM
  B the odd ones (section 5b). The settings are identical, so the label set merges (`shard_golden.one_view` checks).
  Wall time is about 6 h.
- Not recommended: installing `causal_conv1d` (the log shows the slow fallback). It changes the kernels against
  C1's stored reads and the gate environment.
- Needs an amendment: skipping the 8,410 rows that have their own targets (8,309 vote-share + 101 `gold_probs`).
  They get no anchor and the p_g rule does not apply to them, but spec 5 says "every sampled replay row". This
  saves 10,947 reads (-8%, about 1 h).

## 3. Preconditions (all must hold before `--write-shards`)

1. **G14.** The sealed suite's sha256 is committed in `PREREG_FINAL.md` (spec 11 order rule: the replay sample is a
   step-9 output). The sampler refuses without `--sealed-sha <64 hex>` and checks that the sha is the suite file's
   sha256 inside the amendment A15 block of `PREREG_FINAL.md`.
2. **3.H deny-list verdicts** at `c_build/replay_denylist_verdicts.json` (the sampler's default
   `--denylist-verdicts`; `c_src/common/denylist.py replay` writes there by default). Run the program in its own
   process. It is the only reader of `ohs3/used_sources.json`, and its CLI has no override flag (3.H.2):
   ```
   ../.venv/bin/python c_src/common/denylist.py replay --denylist c_build/denylist.json
   ```
   It reads `c_build/replay_denylist_query.json`, which the sampler rewrites whenever the pool changes. For each of
   the 204 sources, the query lists its names, `meta.dataset` strings and domains. The sampler reads only this
   output (denylist.py v1.2 schema; A16 rulings applied):
   ```
   {"program": "c_src/common/denylist.py", "version": "1.2", "program_sha256": "...", "aliases_sha256": "...",
    "denylist": "lean/c_build/denylist.json", "denylist_sha256": "...", "run": "replay", "query_sha256": "...",
    "canonical": true, "provisional": [], "platform_rule": "RULED (PREREG_FINAL.md A16 a): ...",
    "ohs3_platform_alias_suppressed_entries": <count>, "counts": {...},
    "verdicts": {"<source>": {"hit": bool, "verdict": "drop" | "drop_part" | "keep_dev_seen" |
                                                       "keep_no_new_rows" | "keep",
                              "class": "taint" | "no_new_rows" | null,
                              "entry": "<entry name only, no content>",
                              "parts": [{"field": "dataset" | "domain" | "group", "values": [...]}
                                        | {"field": "split", "values": [...], "rule": "train_provenance"}],
                              "part": <parts[0] or null>, "dev_seen_exception": bool, "matches": [...]}}}
   ```
   - `drop` drops the source.
   - `drop_part` drops the rows matched by **every** element of `parts`, each with its whole relation unit.
     - A `dataset`, `domain` or `group` part drops the rows whose field equals one of `values`.
     - A `split` part (scope split: only the test, dev or eval items are tainted) is **fail closed**. The sampler
       keeps a row only if it can prove the row came from a train split, and drops every other row. Proofs, in
       order:
       1. Refuted first: a test, validation, valid, dev or eval token in any `group_id` segment, or a non-train
          split marker in `meta.dataset`.
       2. A `group_id` segment that names the train split, such as `train` or `xl_train_<n>`.
       3. A train-split marker in `meta.dataset`, such as "train split" or `.../train.txt`.
       4. A split declared per source in `replay_sample.TRAIN_SPLIT_DECLARED`, for rows with the declared group
          prefix. The sampler re-checks this declaration in the builder source on every run. Today the only one is
          `arc`: `build_train_v06.py` loads ARC-Challenge with `split="train"`.
     - The dry-run report gives the proof counts per source under `drops.split_scope_train_provenance`.
     - An unknown part field fails the run.
   - Every `keep_*` verdict keeps the rows. `dev_seen_exception` is true only when the only taint reason is "dev
     source" (3.H.3); test-split, OHS, licence and Jev reasons always drop.
   - `--write-shards` refuses in any of these cases:
     - the verdicts are missing;
     - the verdicts are non-canonical (`canonical` false);
     - the verdicts are provisional (non-empty `provisional`);
     - the verdicts are stale: their `query_sha256`, `program_sha256` or `aliases_sha256` is not the sha of the
       current query file, `c_src/common/denylist.py` or `c_src/common/deny_aliases.json`, or the deny-list file they
       name no longer has their `denylist_sha256`;
     - the header predates the A16 rulings (`platform_rule` not "RULED (PREREG_FINAL.md A16 a)");
     - a pool source has no verdict;
     - `--allow-pending` is given (a dry-run flag; the write path never runs without usable verdicts).
     A bare platform word never matches on its own (A16 a), so there is no report-only platform label any more.

     A dry run applies the verdicts anyway and lists the reasons under `drops.denylist_3H`.
3. **OHS-3 hit sources: no input needed.** The A8' whole-source rule (PREREG_FINAL.md amendment A8-prime; the same
   `OHS3_HIT_SOURCES` as `extra/build_fix2.py`) drops gd_redocred (7,979 rows) and gd_helpsteer3_pref (3,369 rows)
   whole. It replaces the A10 7-unit id file (`a10_overlap_ids.json` is no longer read).
4. Optional: `--verified <json list>` for VERIFY sources with an upstream record read (default: none, so all 53,270
   VERIFY / HF-card-only / gd_finqa rows are out).

## 4. Write the shards (Mac, CPU, about 1 min)

```
cd ~/Documents/jev/opendecide-data/lean
../.venv/bin/python c_build/replay_sample.py --write-shards --sealed-sha <sealed sha256>
```
Writes `data/c_replay_r1_shards/shard_000..019.jsonl` + `shards.json` (manifest last, with an ids and rows sha256),
`data/c_old_slice_shards/` and `c_build/replay_draw.json` (round-1 and round-2 unit ids and the old-slice ids). If the
deny-list verdicts moved rows, the counts differ from section 1. The new counts are in
`c_build/replay_counts_dryrun.json`.

**Done 3 Oct 2026, 20:50 UTC** (`c_build/replay_r1_write.json`): 99,069 round-1 rows in 20 shards (manifest sha256
`3f96d3ed...`), old slice 2,000 rows in 1 shard (`9118d6b5...`); counts as in section 1 (the A16 rulings moved no
replay verdict).

## 5. Read on the L4

**od-l4b (us-east4-c): use `c_build/L4_REPLAY_READ.sh`** (steps local, start, preflight, push, f2, launch, status,
fetch, stop; every pushed file pinned in `c_build/L4_REPLAY_READ.sha256`). The commands below are the original od-l4
form.

```
P=system-one-509903; Z=us-central1-a; VM=od-l4
gcloud compute instances start $VM --zone $Z --project $P
gcloud compute scp --recurse --zone $Z --project $P data/c_replay_r1_shards data/c_old_slice_shards $VM:~/lean/data/
gcloud compute ssh $VM --zone $Z --project $P --command 'cd ~/lean && pgrep -f od_gcp.py && echo BUSY || echo idle; \
  sha256sum models/q35_4b_main500k/adapter_model.safetensors od_gcp.py decoder_io.py shard_golden.py'
```
The adapter sha must be `507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078` (A10). Run one job at
a time on the VM. Log the three code shas.

**5a. One VM (default):**
```
gcloud compute ssh $VM --zone $Z --project $P --command 'cd ~/lean && mkdir -p logs && nohup bash -c "\
for D in data/c_replay_r1_shards data/c_old_slice_shards; do \
  ~/od/bin/python od_gcp.py label --name q35_4b_main500k --base Qwen/Qwen3.5-4B \
    --revision 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a --layout schema_branch_mark \
    --shards-dir \$D --tta-choice; done" > logs/c_replay_r1_label.log 2>&1 < /dev/null & echo launched'
```
`label` runs offline by default (`HF_HUB_OFFLINE=1`, pinned base from the cache) and merges the adapter. It asserts
the layout and base commit, skips finished shards, and refuses a shard labelled with other settings.

**5b. Two VMs (optional):** the same command with `for I in 0 2 4 ... 18` (VM A) or `1 3 ... 19` (VM B) and
`--shard $I`. The old slice goes on either VM. Pull both label folders into the same directory.

**Status:** `--command 'tail -n 4 ~/lean/logs/c_replay_r1_label.log; ls ~/lean/data/c_replay_r1_shards/labels_q35_4b_main500k/*.meta.json | wc -l'`
(20 when done). **Resume** after a stop or preemption: run the same launch command again.

**Pull and stop:**
```
gcloud compute scp --recurse --zone $Z --project $P $VM:~/lean/data/c_replay_r1_shards/labels_q35_4b_main500k data/c_replay_r1_shards/
gcloud compute scp --recurse --zone $Z --project $P $VM:~/lean/data/c_old_slice_shards/labels_q35_4b_main500k data/c_old_slice_shards/
gcloud compute scp --zone $Z --project $P $VM:~/lean/logs/c_replay_r1_label.log logs/
gcloud compute instances stop $VM --zone $Z --project $P
```

## 6. What it outputs

`data/c_replay_r1_shards/labels_q35_4b_main500k/shard_NNN.jsonl` has one line per row, in shard order:
`{"id": ..., "model": "q35_4b_main500k", "probs": {...}}`. **`probs` is C1's full option probability vector:**
- choice rows: every option, keyed in the row's original order; each value is the mean of the given-order read and
  the exact-reversal read;
- yes/no rows: `{"yes": p, "no": 1 - p}` from one read.

`shard_NNN.meta.json` records rows, shard_sha256, settings (`name q35_4b_main500k`, revision 851bf6e8..., layout
`schema_branch_mark`, `perm_seed null`, `tta false`, `tta_choice true`, `tta_noul false`, `merged true`), style
`cygnet`, sec, rows_per_sec and load. Check: every meta's `load.chat_template_sha` =
`a4aee8afcf2e0711942cf848899be66016f8d14a889ff9ede07bca099c28f715` (the same as C1's stored reads).

From it, per row: `p_g` = probs[gold] (yes/no: probs["yes"] if gold = 1 else probs["no"]), C1's top answer and
`p_top`. The **selective anchor** is the whole `probs` vector, attached as `meta.teacher` only when the row has no
own target and C1's top answer = gold, with either p_top >= 0.8 ("c1_anchor") or a protected unit
("c1_anchor_protected": an inv / equiv / complement unit, an attacked row or its clean partner).

## 7. Second pass (Mac, CPU)

```
../.venv/bin/python c_build/replay_sample.py --second-pass data/c_replay_r1_shards/labels_q35_4b_main500k \
    --pg-rule-amendment A<n>    # the C PREREG amendment that discloses the attacked-row rule
```
It refuses labels that are not the C1 A5 read. Rules:
- A human-labelled hard-label row with p_g < 0.2 drops its whole relation unit (63,172 rows in the draw fall under
  this rule; the spec estimates 2-5% drop). Program-labelled sources, vote-share rows and `gold_probs` rows are never
  dropped.
- **Attacked rows: counted, not dropped (orchestrator decision, disclosed in the C PREREG amendment).** An attacked
  row with p_g < 0.2 is a successful attack, not label noise: it is counted (`attacked_rows_pg_lt_0.2_kept`) and its
  unit is judged by its clean partner. This is the sampler's default (`--attacked-pg-rule clean_partner`). Because it
  changes spec v4 5's rule, the second pass refuses until `--pg-rule-amendment A<n>` names that amendment and
  "amendment A<n>" is in `PREREG_FINAL.md`. The spec rule stays available as `--attacked-pg-rule spec`.
- The rule used (`pg_rule`: `attacked_rows` "spec" or "clean_partner", plus the amendment id) is written into
  `replay_r1_pg_anchor.json`, with `attacked_rows_pg_lt_0.2` (and `_kept` under clean_partner).

Output: `c_build/replay_r1_pg_anchor.json` with, per row, p_g, top, p_top, anchor and drop_pg, plus counts. The mixer
(step 9) then:
- trims the margin to exactly 90,000 inside each source's quota;
- re-runs the E2 wording check on the trimmed set;
- attaches the anchors and runs the G18 lint.

It also needs a G5 read of 300 rows dropped by the p_g rule (report only).

## 8. Notes

- The round-2 superset draw (197,896 rows with margin) contains round 1. Its fresh half is read only if round 2 runs.
- E2 (re-run 3 Oct, after review). Cells are re-derived after every swap: a wording that falls under 50 rows is scored
  in its family. Each of the 157 wording cells with >= 50 rows at the start also stays scored on its own rate, so
  shrinking a cell is never counted as fixing it. The after-report re-derives the cells on the final set.
  - Round-1 draw: 32 cells out of 50 +/- 5 (3,137 rows). 100 same-source, same-size swaps brought this to 0 on the
    final set's cells. All 157 start cells are in band on their own rate (2 are now under 50 rows), and none is stuck.
    Rows and reads are unchanged (99,073 / 134,582).
  - The earlier run (75 swaps) had 4 cells (196 rows) that were only shrunk under 50, plus 1 family cell out of band
    once re-derived ('f:attacked|in the customer's', 74 rows, 0.446). Both are fixed.
  - Round-2 draw: 53 -> 4 cells out (219 rows) after 249 swaps. They are 2 family cells and 2 wording cells (the 2
    wording cells are start cells, 108 rows). No swap improves them, so they are marked stuck and reported. Round 2's
    E2 runs again when round 2 is built.
- No `equiv` units remain in the eligible pool: all 1,922 equiv rows are in dropped Claude-gold sources. Protected
  units are complement (15,254 rows) and inv (13,520 rows), plus 6,498 attacked rows.

## 9. F2 rendered-prompt record (recipe v4 pre-flight 9; CPU, $0, same session)

F2 can only find a machine difference (for example, transformers 5.17.0 in the training image against the VM's
version) if each machine writes its own record and the records are compared. On the L4, while it is up for section 5,
after copying `runs/q35_4b_c_r1.json` and the current `train_decoder.py` / `decoder_io.py`:
```
gcloud compute ssh $VM --zone $Z --project $P --command 'cd ~/lean && HF_HUB_OFFLINE=1 ~/od/bin/python train_decoder.py f2 \
  --config runs/q35_4b_c_r1.json --adapter models/q35_4b_main500k --where l4-gate --out logs/f2_l4.json'
gcloud compute scp --zone $Z --project $P $VM:~/lean/logs/f2_l4.json c_build/f2_l4.json
```
`--adapter` adds the gate/serve load path (`od_gcp.py predict` and di_engine / serve_tunnel make the same
`decoder_io.load(adapter)` call). Modal side: the C smoke run records the same 6 sha256 in the training image
(`modal_od.py::smoke_heavy ... --config runs/q35_4b_c_r1.json --f2-ref c_build/f2_l4.json`; it writes
`logs/pilot/f2_<tag>.json` and prints pass / FAIL).

**Before the GO:**
```
../.venv/bin/python train_decoder.py f2cmp c_build/f2_l4.json logs/pilot/f2_<smoke tag>.json c_build/f2_local_mac.json
```
It must print `"f2_cross": "pass"`. Write its output (the 6 sha256 and each machine's transformers / jinja2 versions)
to the look log. `c_build/f2_local_mac.json` is the Mac's record (3 Oct, transformers 4.57.6): it covers the train and
gate_serve paths on the C draft config with the C1 adapter, template sha a4aee8af.... If only the Mac record
differs, the three real paths can still agree. In that case, re-run f2cmp without it and record why.
