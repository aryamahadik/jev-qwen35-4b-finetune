# Shared pools rebuild after G13 wording fixes (task A of WORDING_FIXES.md) - 2026-10-08

Scope: packs-1, packs-2, packs-4 (sources edited) and formats-1 (build_pool.py + registers.jsonl edited). packs-3 untouched (no edits). formats-2 NOT touched.
Python: opendecide-data/.venv/bin/python, nice -n 5, 4 jobs max. Logs: c_build/endgame/logs/shared_rebuild/*.log.
Backups (previous pool): `<file>.pre_wording` next to each packs output (packs.jsonl, lint_report.json, packs.sealedqc.*, manifest*.json, packs-4 packs_index.jsonl + tmp/qc_report.json + tmp/sc_*), packs-2/qc.pre_wording/, formats-1/MANIFEST.json.pre_wording, formats-1/tmp/pool.pre_wording/{data,qc}/.

## Commands (each from its own folder)
- packs-1: `build_packs.py` -> `sealed_nd/qc/sealed_check.py packs.jsonl --id-field id --out packs.sealedqc.jsonl --summary packs.sealedqc.summary.json` -> `make_manifest.py`
- packs-2: `build_packs.py` -> `qc_packs.py packs.jsonl --others ../packs-1/packs.jsonl,../packs-4/packs.jsonl` -> `qc/verify_v11.py` -> copy tmp/qc outputs to qc/ (qc_report_packs2.json, sealedqc_packs_ids.jsonl, sealedqc_packs_summary.json, sealedqc_components_summary.json) -> `make_manifest.py`
- packs-4: `build_packs.py` -> `make_index.py` -> `qc_packs.py` -> sealed_check on packs.jsonl and packs_index.jsonl (tmp/sc_*) -> `make_manifest.py`
- formats-1: `build_pool.py` -> `qc/run_qc.py` (lints, loader, pytest, sealed id-only check on all data + previews, deny-list, MANIFEST)

## sha256 before -> after
| file | before | after |
|---|---|---|
| packs-1/packs.jsonl | 9a8a8944233001b4 | beba89b3e03e9804 |
| packs-2/packs.jsonl | 851baeabaaf9304e | 889186c11b47ba9b |
| packs-4/packs.jsonl | 5f8197be3737fe56 | de5703dea1aa67d1 |
| packs-4/packs_index.jsonl | 628c8f16344b5351 | same (byte-identical) |
| formats-1/data/registers.jsonl | a06fdb90f73d7983 (hand-edited, stale row sha) | ce2d53131c7623e6 |
| formats-1/data/*.jsonl (concat) | 9cf2ca4381bddd3f | 8906cc3bc7b3add0 |

## Diff vs previous pool (counts)
- packs-1: 88 -> 88 packs, same ids/order; 1 pack changed (the b02 pack): 5 attribute values + 5 scale levels (level N -> LN), 1 label predicate, pack_sha256. 87 packs byte-identical.
- packs-2: 80 -> 80, same ids/order; all 80 changed only in register.greetings (+ row sha256) from the shared greeting leaf. Other changes only in the 4 edited-sector packs (fo-03, hc-10, hr-08, hs-08): renamed values/roles/field key and derived lexicon/concept/inert-vocab fields (inert vocab total 7406 -> 7408; strings checked 81162 -> 81160; key word forms 32915 -> 32911). New dict keys 1, gone 1 (length_of_stay -> stay_days).
- packs-4: 84 -> 84; 3 packs changed: 2 quantities (name + derived sub-object id), 1 action synonym. Note: the 2 quantity sub-object ids changed with the rename (ids are slugs of names).
- formats-1: 14 data files; 13 byte-identical; registers.jsonl 1 row (RG-casual) changed vs the hand-edited file only in its `sha256` field (now correct); vs the original pre-wording file, the same 1 row changed.

## Old strings (old pool -> new pool)
- packs-1: "is level 4 or level 5" 1 -> 0; "level 1"/"level 4"/"level 5" list items 2 -> 0 each; new "L1".."L5" items 0 -> 2.
- packs-2: "Good morning," 80 -> 0; "length of stay" 10 -> 0; "length_of_stay" 7 -> 0; "chief financial officer" 6 -> 0; "green tea" 1 -> 0.
- packs-4: "response rate" 1 -> 0; "body weight" 1 -> 0; "welcome back" 1 -> 0.
- formats-1: "Good to know" 0 -> 0 in data (hand edit already in registers.jsonl; build_pool.py now writes the same text); no other file in formats-1 holds it.

## QC / lint / sealed check (all rc 0)
- packs-1 lint: 88 packs, errors 0, warnings 80 (same as before; affix-review only), ROUGE-L max 0.263. Sealed: 88 rows, hit 0, report-only 75 (before 0/75).
- packs-2 lint: 0 errors. qc_packs: sealed whole packs 80 hit 0 (keyword_soft 80, same); components 173870 hit 0 (keyword_soft 2467, same; before 173873); ROUGE-L worst 0.2967, cross 0.0735, none >= 0.7. verify_v11: BAD mk neg 0, mk none 0. Extra: the 1 new dict key through sealed_check: hit 0. qc/sealedqc_keys_and_filler_pool_summary.json is the old ad-hoc file (no script to rebuild it); only the renamed key differs and it passed.
- packs-4 lint: 84/84 ok, errors 0, affix flags 0. qc_report.json identical to before. Sealed packs 84 hit 0 (report-only 76, same); index 84 hit 0.
- formats-1 run_qc: lints negation_cue_hits 0, record_status_word_hits 0; pytest 1237 passed; sealed 15 inputs, hits 0, all exits 0; deny-list pass (check_exit 0, paths_exit 0).
- Manifests refreshed by each set's make_manifest.py / run_qc.py (new sha present in each). packs-2 manifest schema text also gained the v1.1 description lines emitted by make_manifest.py (code text, not data).

## Not checked here
New wordings vs sealed OHS-3 sources: G13 must re-check after this rebuild (per WORDING_FIXES.md).
