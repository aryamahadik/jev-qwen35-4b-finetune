# OHS-3 final table: q35_4b_main500k_cal vs Jev

| Win condition | Metric | OpenDecide | Jev | Diff (+ = OD better) | 95% CI | Verdict | Won |
|---|---|---|---|---|---|---|---|
| accuracy >= Jev | accuracy micro, 1,852 base rows (pp) | 74.298 | 79.644 | -5.346 | [-7.085, -3.618] | jev_better | no |
| accuracy >= Jev | accuracy macro, 13 tasks (pp) | 74.314 | 79.676 | -5.362 | [-7.098, -3.645] | jev_better | no |
| calibration | Brier, 716 yes/no base rows | 0.172 | 0.150 | -0.022 | [-0.036, -0.008] | jev_better | no |
| consistency | complement violation, 300 _neg pairs | 0.170 | 0.088 | -0.082 | [-0.128, -0.034] | jev_better | no |
| consistency | option-order drift, 304 _perm pairs | 0.023 | 0.041 | 0.018 | [-0.008, 0.046] | no_clear_difference | no |
| speed (faster than Jev) | S1 end-to-end p50 per call (ms) | 100.110 | 219.010 | 118.902 | [117.266, 120.813] | not shown faster | no |
| speed (faster than Jev) | S2 end-to-end p95 per call (ms) | 603.070 | 301.370 | -301.706 | [-306.375, -294.943] | not lower | no |
| cost (cheaper than Jev) | C1 $/1K decisions at 0.4 utilisation | 0.433 | 0.061 | - | - | not cheaper | no |
| cost (cheaper than Jev) | input tokens per call on the OHS-3 calls (mean) | 2412.190 | 1459.760 | - | - | descriptive | - |
| cost (cheaper than Jev) | C3 JevBench v1.5.4 formula $/1K | 0.039 | 0.038 | - | - | not cheaper | no |
| hijack / injection resistance | not measured on OHS-3 (no attack rows) | - | - | - | - | n/a | - |
| JevBench | no submission (owner rule) | - | - | - | - | n/a | - |

**All measured win conditions won:** False.

**Dev-only evidence of the pre-registered T and cascade values:** PASS models.4b.T_fit_log.
Not won: accuracy >= Jev: accuracy micro, 1,852 base rows (pp); accuracy >= Jev: accuracy macro, 13 tasks (pp); calibration: Brier, 716 yes/no base rows; consistency: complement violation, 300 _neg pairs; consistency: option-order drift, 304 _perm pairs; speed (faster than Jev): S1 end-to-end p50 per call (ms); speed (faster than Jev): S2 end-to-end p95 per call (ms); cost (cheaper than Jev): C1 $/1K decisions at 0.4 utilisation; cost (cheaper than Jev): C3 JevBench v1.5.4 formula $/1K.

## Secondary endpoints (BH family)

| Endpoint | OD | Jev | Diff | 95% CI | q | Verdict |
|---|---|---|---|---|---|---|
| acc_track_F | 71.573 | 76.449 | -4.876 | [-7.301, -2.563] | 0.0000 | jev_better |
| acc_track_U | 78.170 | 84.183 | -6.013 | [-8.598, -3.576] | 0.0000 | jev_better |
| acc_over_26_options | 75.000 | 84.155 | -9.155 | [-13.415, -5.072] | 0.0000 | jev_better |
| complement_violation | 0.170 | 0.088 | -0.082 | [-0.128, -0.034] | 0.0014 | jev_better |
| option_order_drift | 0.023 | 0.041 | 0.018 | [-0.008, 0.046] | 0.2687 | no_clear_difference |
| bc_micro | 75.108 | 79.644 | -4.536 | [-6.305, -2.810] | 0.0000 | jev_better |
| bc_macro | 75.127 | 79.676 | -4.550 | [-6.318, -2.838] | 0.0000 | jev_better |
| bc_brier_yesno | 0.172 | 0.150 | -0.022 | [-0.036, -0.008] | 0.0027 | jev_better |
| acc_task_bias_in_bios_profession | 72.535 | 78.521 | -5.986 | [-10.993, -1.408] | 0.0180 | jev_better |
| acc_task_causal_news_corpus | 81.944 | 82.986 | -1.042 | [-6.944, 4.861] | 0.8096 | no_clear_difference |
| acc_task_ct_study_type | 84.286 | 90.000 | -5.714 | [-10.000, -1.429] | 0.0125 | jev_better |
| acc_task_few_nerd_fine | 78.169 | 76.408 | 1.761 | [-3.169, 6.690] | 0.5813 | no_clear_difference |
| acc_task_fewrel_relation | 84.507 | 90.845 | -6.338 | [-11.972, -0.704] | 0.0484 | jev_better |
| acc_task_fr_agency | 59.155 | 72.887 | -13.732 | [-20.946, -6.922] | 0.0000 | jev_better |
| acc_task_medrxiv_category | 61.972 | 67.606 | -5.634 | [-13.028, 1.761] | 0.1933 | no_clear_difference |
| acc_task_nvd_attack_vector | 63.194 | 65.972 | -2.778 | [-9.859, 4.317] | 0.5302 | no_clear_difference |
| acc_task_openfda_recall_class | 78.472 | 75.347 | 3.125 | [-3.901, 10.140] | 0.4895 | no_clear_difference |
| acc_task_rosetta_code_language | 73.944 | 96.479 | -22.535 | [-29.577, -15.493] | 0.0000 | jev_better |
| acc_task_se_site | 90.845 | 95.423 | -4.577 | [-9.507, 0.000] | 0.1009 | no_clear_difference |
| acc_task_uk_wq_answering_body | 68.310 | 69.014 | -0.704 | [-7.042, 5.405] | 0.8670 | no_clear_difference |
| acc_task_zenodo_resource_type | 68.750 | 74.306 | -5.556 | [-13.986, 2.797] | 0.2925 | no_clear_difference |
| acc_half_A | 72.936 | 77.220 | -4.284 | [-6.811, -1.859] | 0.0017 | jev_better |
| acc_half_S | 75.754 | 82.235 | -6.480 | [-8.952, -4.050] | 0.0000 | jev_better |
| McNemar vs_jev_guard | b=97 | c=196 | | | 0.0000 | jev_better |
| McNemar vs_jev_r2_guard | b=96 | c=195 | | | 0.0000 | jev_better |

## Jev runs

- jev_guard: micro 79.64, macro 79.68, Brier 0.1497, missing base 0 / twin 0, rows not from typesafe/jev-1.13-20260917: 0
- jev_r2_guard: micro 79.64, macro 79.67, Brier 0.1500, missing base 0 / twin 0, rows not from typesafe/jev-1.13-20260917: 0
- run-to-run agreement: decision 0.9773, correctness 0.9860

## Option-order drift by twin kind (descriptive, no CI)

With the 2-view readout a reversed twin is read in its base row's two orders, so its drift is ~0 by construction; the rotated twins are the informative comparison.

| Twin kind | Pairs | OD drift | Jev drift (mean of runs) |
|---|---|---|---|
| reversed | 149 | 0.000 | 0.010 |
| rotated | 155 | 0.045 | 0.071 |
- OpenDecide answers: missing base 0, twin 0, ties 0

## Every OpenDecide configuration run on OHS-3 (rule 4)

- q35_4b_main500k_1v_cal
- q35_4b_main500k_cal (headline)
  - q35_4b_main500k_1v_cal: micro 73.434 (diff -6.210, jev_better); macro 73.447 (diff -6.229, jev_better); brier_yesno 0.172 (diff -0.022, jev_better)
