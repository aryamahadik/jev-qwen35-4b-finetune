# T31 fix iteration 3 (A44 a)

## Change
- New `families/T31/run_pilot_i3.py`: a copy of `run_pilot_i2.py` (still reads `pools_v2_dneg/`), output `pilot_i3/`.
- Its loader removes, in memory, every T31 form id in `zed_orch/a43f_quarantine.json` (44 ids): from the registry (44 removed)
  and their wording skins from the pool (44 removed). They cover the frozen and the supplement `yn_holder_dneg` / `yn_agent_dneg` forms.
  The plugin then falls back to the plain forms. No frozen pool file, `plugin.py` or G0 text is edited. No relabel, no bar change.
- The runner audits the rendered yes/no rows with `zed_orch/dneg_frame_audit.flag_text` (negated frame over negated proposition).

## Frame audit (A43 f)
- pilot_i3: 521 yes/no rows, 0 banned-shape rows.
- G6 build (6,001 rows): 3,042 yes/no rows, 0 banned-shape rows.

## gates_after
- Program gates (pilot_size 1002 rows, G2, G3, G4, G-SL, G-LEX, G-TW, G15, schema, options, G7, overlay, spec_3_0): pass.
- G3-H / G5-H: task files written in `pilot_i3/g3h`, `pilot_i3/g5h` (not answered).
- G6 at 6,000 rows (`G6_AT_6000.json`, 6,001 rows): pass. Max yes/no 0.5105 (c_card_without_question/lr) vs bar 0.52;
  max choice 0.2994 (d_meta/gbt) vs bar 0.3144.
- G6 at the 1,000-row pilot size: choice b_options/gbt 0.3243 and c_card_without_question/gbt 0.3243 vs bar 0.3163 are above the bar
  (not significant at pilot size). They are within the pilot-size null only if `pilot.g6`'s null check says so; I did not verify it.
  The 6,000-row run is the A43 test.
- G10 double_negation_share: 0.0% vs bar >= 2%: fails, WAIVED by A44 (b) (A43 f bans the shape). Negation robustness is carried by A42 item 7.
- G10 yes_rate_cells (report-only): a small cell `T31-W-yn_holder-q880686a401|None|0` n=39 yes=0.718 has binomial p < 0.01.
  Not a selection-quota failure here (report-only per the brief).
- Determinism: rows sha256 `a98c2a6c1542474076e74c7696b7c04d83cc18a3c505110930062f1aa552a837`, relations sha256
  `c90ef16a6d6f3840e1ffe3fd0bf45c3bae5884b2e47f8353c32ee2e94d4e3969`, identical under PYTHONHASHSEED=1 and 2 (dry run, --no-g15).
  The written pilot_i3 build includes G15 and has 1002 rows (the dry run used --no-g15); its sha is in `PILOT_REPORT.json`.
- Tests: `pytest families/T31` started in the background; see the final status in the final reply.

## Commands
    cd lean/c2_build
    ../.venv/bin/python -B families/T31/run_pilot_i3.py                    # pilot_i3 + task files
    PYTHONHASHSEED=1 ../.venv/bin/python -B families/T31/run_pilot_i3.py --dry-run --no-g15
    ../.venv/bin/python -B families/T31/run_pilot_i3.py --g6 --n 6000      # pilot_i3/G6_AT_6000.json
    ../.venv/bin/python -B families/T31/run_pilot_i3.py --score            # after Haiku G5-H / G3-H answers

## Open
- Haiku: G5-H (100 rows) and G3-H reads, orchestrator.
