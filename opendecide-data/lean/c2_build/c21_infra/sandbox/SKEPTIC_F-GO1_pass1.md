# F-GO1 skeptic, pass 1: NOT SOUND (one blocking defect) - Sun 18 Oct 2026

FILING NOTE (builder): this file is a SUMMARY written by the builder from the coordinator's relayed message. The skeptic's own text was not available to the
builder. If the verbatim report is wanted here, paste it over this file. Nothing below goes beyond what the coordinator relayed.

Subject: the first F-GO1 proposal (`TMPDIR=/work/.tmp`, IMAGE_RECIPE.md 10.5, executor tree `c96d247b...`, 34 executor tests). Verdict: NOT SOUND, one blocking defect, fix it plus the cheap notes.

## D1 (blocking): the `.tmp` drop was not enforced
`runner.py:233` stripped the reserved `.tmp` entries and recorded them in `stripped`, but for `kind="run"` nothing reads `stripped`: `cli.py:93-94` only bumps a counter and the row still runs
on the altered tree. Rule (a) of 10.4 covers verdict (suite) runs only.
Required fix: in `run_once`, after `norm_key`, raise `StageError` if any patch or overlay key's first component is in `RESERVED_TOP`; `cli.py:87-90` already turns that into `rejected` /
`rejected_unstageable_tree`, so the row is DROPPED for both kinds. Remove `_drop_reserved` and its tests. Also fold the executor-owned Go names `.gocache` and `.gopath` into the same reject for
run rows (they were stripped only for suite runs, `runner._strip_reason` / `STRIP_GO_TOP_DIRS`); keep the suite behaviour if the recipe requires it, and explain.

## D1b (test gap)
`test_run_once_records_reserved_entries...` raised inside `fake_stage` and never checked the result; a mutation that discarded the drop still passed all 34 tests. Required: a real test that a
reserved key raises `StageError`; a test that the cli writes `rejected` plus the counter for such a row for both run kinds; and a mutation check (the tests must fail if the check is removed).

## Minor (all four requested)
1. sh fixture: `touch "$TMPDIR/x"` and print `$TMPDIR`; `selftest.py` must compare the LAST stdout line to `WORK_TMP` exactly, not as a substring (all four toolchains).
2. Document in IMAGE_RECIPE.md that every run now has an empty `/work/.tmp`, so `ls -A`, `find .`, `os.listdir` and `du` rows list it; add a note for the L-C lane and the T56 lint.
3. Fix the rebuild note: steps 50 and 60 source `${SBX_SRC}/pins.env` (`common.sh:9-10`), so delete the old `~/sandbox` first, then use `SBX_SRC=/tmp/sandbox`, which step 60 scrubs itself.
4. Rebuild note: on the build VM's next boot, stop the enabled `od-sbx-selftest` unit before step 50's `systemctl restart docker`.

## Resolution (builder, same day)
All of the above were done: `_reject_reserved` (StageError for `.tmp`; Go `.gocache`/`.gopath` rejected for run patches and all overlays, K6 strip kept for Go suite patches), `_drop_reserved` and its tests
removed, 37 executor tests, mutation runs (check removed, suite-only, `continue` instead of `raise`, overlay skipped, Go run rows not rejected) caught by 2 or 3 tests each, exact last-line check
(`selftest.last_line`), sh `touch`, recipe 10.5 text on directory listings, rebuild notes 1 to 4. Re-check: SKEPTIC_F-GO1_pass2.md.
