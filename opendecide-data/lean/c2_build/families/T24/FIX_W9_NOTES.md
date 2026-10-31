# T24 w9 fix round (A49 d, A52 d): generator fix, one iteration

## Cause (evidence: zed_orch/w9/diag_old_3000000.jsonl, the old generator at the old QC base, 6,000 rows)
A50 worst cell yes_no / a_question / LR +2.09 pp (mean of 4 builds). The question carried the yes rate because the
yes rate differed by question form: yn_changes 0.463, yn_dneg 0.485, yn_same 0.532, yn_not_change 0.537,
yn_fail_change 0.525. The base rows were balanced (dealt hit 0.49-0.52 per form) and so were the complement partners;
the minimal-edit TWINS were not: a twin always has the opposite gold, a changing base has a twin on 100% of seeds and an
unchanged base on ~45% (qform x gold table in the notes of `_twin_plan`), so twin rows were ~2:1 "unchanged" (yn_changes
twins: 156 no vs 85 yes). A second, smaller source: the wording was a hash pick, so each (form, wording) cell carried
binomial noise in its yes rate (112 yes/no wordings, ~27 rows each).

## Changes (generator only; no relabel, no feature dropped, no bar touched; G0_SPEC.md and its sha unchanged)
- `plugin.py` `_deal_of` / `_wording_ranks` / `_dealt_wording` (WORD_BLOCK 1024 seeds): label-first wording deal. The
  gold label of the row (the hit draw, or the dealt (k, role) cell for ch_v2) is fixed by the seed first; the wording is
  then a round robin over the form's wordings (permutation seeded per sampler, block, form) by the rank of the row inside
  its (form, gold) group, so every (form, wording) cell holds yes and no equally often up to the rows by which the
  form's yes and no counts in a block differ. Base rows, complement partners (the pipeline's hash-picked partner
  wording is replaced in render by the dealt one) and ch_v2 rows all use it. Also caps wording use (G11).
- `plugin.py` `_twin_plan` (TWIN_BLOCK 256 seeds, TWIN_BALANCED 0.175): per yes/no form and block, twins with gold yes
  and gold no are equal in number (Q = min(available per direction, cap), the Q lowest label-blind hashes in each
  direction). Twin share per yes/no seed stays ~0.35 (old 0.24 + 0.11). ch_v2 twins keep the old rule.
- `plugin.py` `EQUIV_RATE` 0.10 -> 0.13: the first regeneration (bases 124M/125M/126M) passed every program gate except
  overlay (equiv share 4.77% < 5%). Label-blind; equiv rows copy their base's gold and wording.
- Tests: `test_balance.py` +3 (wording deal, dealt label == solved gold, twin plan), `test_plugin.py` whitelist
  `_backup_w9` and the two G2-teeth tests use 160 seeds (twins thinned). Backups in `_backup_w9/`.

## Process notes
- Attempt 1 of the regeneration (bases 124M/125M/126M, EQUIV_RATE 0.10) is kept in `zed_orch/w9/_attempt1_gen3` and
  `zed_orch/a50/_attempt1_w9` (its G6 cells already passed; only overlay equiv_share failed). The shipped generation
  uses new bases 127M/128M/129M (a failed generation is never re-drawn on its seeds).
- The VM CPU venv has no torch: G15 failed every unit there (0 candidate rows). The generation ran with
  `PYTHONPATH=~/lean ~/od/bin/python` (torch 2.14; pinned prism_x/decoder_io/train_decoder sha-equal to the Mac).
  The three extra G6 builds ran with the CPU venv. Other families' VM generation jobs through gen_full_c2.run() need the
  same interpreter (a run with `~/cpu/bin/python` reports "0 candidate rows" with `render` drops).
