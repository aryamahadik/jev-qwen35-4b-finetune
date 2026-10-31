# OHS-3 final table: dry_4b_cal vs Jev (DRY RUN, synthetic data)

**Deviations recorded by score_ohs3.py:** ['data/ohs3.jsonl sha256 c5b651216c14 != frozen 68cb27da1390', 'data/ohs3_relations.jsonl sha256 5e4a26077523 != frozen c2e1dcee9ba4']

| Win condition | Metric | OpenDecide | Jev | Diff (+ = OD better) | 95% CI | Verdict | Won |
|---|---|---|---|---|---|---|---|
| accuracy >= Jev | accuracy micro, 1,852 base rows (pp) | 21.976 | 84.044 | -62.068 | [-64.001, -60.141] | jev_better | no |
| accuracy >= Jev | accuracy macro, 13 tasks (pp) | 21.885 | 84.017 | -62.132 | [-64.071, -60.223] | jev_better | no |
| calibration | Brier, 716 yes/no base rows | 0.250 | 0.103 | -0.147 | [-0.156, -0.138] | jev_better | no |
| consistency | complement violation, 300 _neg pairs | 1.000 | 0.125 | -0.875 | [-0.901, -0.848] | jev_better | no |
| consistency | option-order drift, 304 _perm pairs | 0.490 | 0.378 | -0.112 | [-0.185, -0.039] | jev_better | no |
| speed (faster than Jev) | S1 end-to-end p50 per call (ms) | 18.310 | 34.220 | 15.915 | [15.313, 16.513] | not shown faster | no |
| speed (faster than Jev) | S2 end-to-end p95 per call (ms) | 51.140 | 48.380 | -2.758 | [-5.552, -1.364] | not lower | no |
| cost (cheaper than Jev) | C1 $/1K decisions at 0.4 utilisation | 0.067 | 0.031 | - | - | not cheaper | no |
| cost (cheaper than Jev) | input tokens per call on the OHS-3 calls (mean) | 1504.390 | 729.780 | - | - | descriptive | - |
| cost (cheaper than Jev) | C3 JevBench v1.5.4 formula $/1K | 0.039 | 0.038 | - | - | not cheaper | no |
| hijack / injection resistance | not measured on OHS-3 (no attack rows) | - | - | - | - | n/a | - |
| JevBench | no submission (owner rule) | - | - | - | - | n/a | - |
| speed (faster than Jev), 2b (dry_2b; not the headline) | S1 end-to-end p50 per call (ms) | 21.170 | 34.290 | 13.116 | [11.620, 14.923] | not shown faster | n/a (not the headline) |
| speed (faster than Jev), 2b (dry_2b; not the headline) | S2 end-to-end p95 per call (ms) | 66.420 | 48.130 | -18.287 | [-27.797, -13.195] | not lower | n/a (not the headline) |
| speed (faster than Jev), cascade (dry_cascade; not the headline) | S1 end-to-end p50 per call (ms) | 27.620 | 33.840 | 6.219 | [5.537, 7.066] | not shown faster | n/a (not the headline) |
| speed (faster than Jev), cascade (dry_cascade; not the headline) | S2 end-to-end p95 per call (ms) | 78.590 | 47.800 | -30.790 | [-34.171, -28.318] | not lower | n/a (not the headline) |
| cascade routing, cascade | routed share of rows (served pass) | 0.473 | - | - | - | 1163/2456 rows | n/a (not the headline) |

**All measured win conditions won:** False.
Not won: accuracy >= Jev: accuracy micro, 1,852 base rows (pp); accuracy >= Jev: accuracy macro, 13 tasks (pp); calibration: Brier, 716 yes/no base rows; consistency: complement violation, 300 _neg pairs; consistency: option-order drift, 304 _perm pairs; speed (faster than Jev): S1 end-to-end p50 per call (ms); speed (faster than Jev): S2 end-to-end p95 per call (ms); cost (cheaper than Jev): C1 $/1K decisions at 0.4 utilisation; cost (cheaper than Jev): C3 JevBench v1.5.4 formula $/1K.

## Secondary endpoints (BH family)

| Endpoint | OD | Jev | Diff | 95% CI | q | Verdict |
|---|---|---|---|---|---|---|
| acc_track_F | 25.851 | 85.005 | -59.154 | [-61.721, -56.535] | 0.0000 | jev_better |
| acc_track_U | 16.471 | 82.680 | -66.209 | [-69.093, -63.264] | 0.0000 | jev_better |
| acc_over_26_options | 2.465 | 79.401 | -76.937 | [-80.488, -73.239] | 0.0000 | jev_better |
| complement_violation | 1.000 | 0.125 | -0.875 | [-0.901, -0.848] | 0.0000 | jev_better |
| option_order_drift | 0.490 | 0.378 | -0.112 | [-0.185, -0.039] | 0.0028 | jev_better |
| bc_micro | 22.246 | 84.044 | -61.798 | [-63.749, -59.844] | 0.0000 | jev_better |
| bc_macro | 22.156 | 84.017 | -61.861 | [-63.805, -59.915] | 0.0000 | jev_better |
| bc_brier_yesno | 0.250 | 0.103 | -0.147 | [-0.156, -0.138] | 0.0000 | jev_better |
| acc_task_syn_bios | 3.521 | 78.169 | -74.648 | [-79.930, -69.014] | 0.0000 | jev_better |
| acc_task_syn_cnc | 50.000 | 93.403 | -43.403 | [-51.389, -35.417] | 0.0000 | jev_better |
| acc_task_syn_ct_study | 50.000 | 92.143 | -42.143 | [-51.071, -33.214] | 0.0000 | jev_better |
| acc_task_syn_fewnerd | 7.042 | 80.986 | -73.944 | [-80.282, -66.901] | 0.0000 | jev_better |
| acc_task_syn_fewrel | 5.634 | 76.761 | -71.127 | [-77.113, -64.437] | 0.0000 | jev_better |
| acc_task_syn_fr_agency | 2.113 | 77.817 | -75.704 | [-80.690, -70.503] | 0.0000 | jev_better |
| acc_task_syn_medrxiv | 4.930 | 76.408 | -71.479 | [-77.113, -65.845] | 0.0000 | jev_better |
| acc_task_syn_nvd | 50.000 | 90.625 | -40.625 | [-49.296, -31.849] | 0.0000 | jev_better |
| acc_task_syn_openfda | 50.000 | 93.403 | -43.403 | [-51.645, -35.273] | 0.0000 | jev_better |
| acc_task_syn_rosetta | 4.225 | 79.577 | -75.352 | [-80.986, -69.366] | 0.0000 | jev_better |
| acc_task_syn_se_site | 2.817 | 80.986 | -78.169 | [-83.451, -72.887] | 0.0000 | jev_better |
| acc_task_syn_uk_wq | 4.225 | 79.930 | -75.704 | [-81.338, -69.792] | 0.0000 | jev_better |
| acc_task_syn_zenodo | 50.000 | 92.014 | -42.014 | [-50.350, -33.784] | 0.0000 | jev_better |
| acc_half_A | 21.288 | 83.853 | -62.565 | [-65.240, -59.792] | 0.0000 | jev_better |
| acc_half_S | 22.722 | 84.252 | -61.530 | [-64.496, -58.582] | 0.0000 | jev_better |
| McNemar vs_jev_guard | b=38 | c=1189 | | | 0.0000 | jev_better |
| McNemar vs_jev_r2_guard | b=31 | c=1179 | | | 0.0000 | jev_better |

## Jev runs

- jev_guard: micro 84.13, macro 84.10, Brier 0.0978, missing base 0 / twin 0, rows not from typesafe/jev-1.13-20260917: 0
- jev_r2_guard: micro 83.96, macro 83.94, Brier 0.1078, missing base 0 / twin 0, rows not from typesafe/jev-1.13-20260917: 0
- run-to-run agreement: decision 0.7144, correctness 0.7414

## Option-order drift by twin kind (descriptive, no CI)

With the 2-view readout a reversed twin is read in its base row's two orders, so its drift is ~0 by construction; the rotated twins are the informative comparison.

| Twin kind | Pairs | OD drift | Jev drift (mean of runs) |
|---|---|---|---|
| reversed | 152 | 0.000 | 0.411 |
| rotated | 152 | 0.980 | 0.345 |
- OpenDecide answers: missing base 0, twin 0, ties 0

## Every OpenDecide configuration run on OHS-3 (rule 4)

- dry_2b_1v_cal
- dry_2b_cal
- dry_4b_1v_cal
- dry_4b_cal (headline)
- dry_4b_served_cal
- dry_cascade_cal
- dry_cascade_served_cal
- dry_oracle_cal
  - dry_4b_1v_cal: micro 22.030 (diff -62.014, jev_better); macro 21.939 (diff -62.078, jev_better); brier_yesno 0.250 (diff -0.147, jev_better)
  - dry_2b_cal: micro 22.300 (diff -61.744, jev_better); macro 22.210 (diff -61.807, jev_better); brier_yesno 0.483 (diff -0.381, jev_better)
  - dry_2b_1v_cal: micro 21.976 (diff -62.068, jev_better); macro 21.885 (diff -62.132, jev_better); brier_yesno 0.482 (diff -0.380, jev_better)
  - dry_oracle_cal: micro 86.069 (diff 2.025, matches); macro 86.043 (diff 2.026, matches); brier_yesno 0.083 (diff 0.019, beats)
  - dry_cascade_cal: micro 22.192 (diff -61.852, jev_better); macro 22.103 (diff -61.914, jev_better); brier_yesno 0.483 (diff -0.381, jev_better)
  - dry_4b_served_cal: micro 21.976 (diff -62.068, jev_better); macro 21.885 (diff -62.132, jev_better); brier_yesno 0.250 (diff -0.147, jev_better)
  - dry_cascade_served_cal: micro 22.192 (diff -61.852, jev_better); macro 22.103 (diff -61.914, jev_better); brier_yesno 0.483 (diff -0.381, jev_better)
