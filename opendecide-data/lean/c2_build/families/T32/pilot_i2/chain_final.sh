cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build
/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python -B families/T32/run_pilot_i2.py determinism --n 300 > families/T32/pilot_i2/determinism_final.log 2>&1
/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python -B families/T32/run_pilot_i2.py run --n 1000 > families/T32/pilot_i2/run_final.log 2>&1
/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python -B zed_orch/g6_at_size.py T32 --dir pilot_i2 > families/T32/pilot_i2/g6_final.log 2>&1
/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python -B -m pytest -q -p no:cacheprovider --ignore=families/T32/_backup_i2 --ignore=families/T32/_backup_i2b_final families/T32 > families/T32/pilot_i2/tests_i2_final.log 2>&1
echo done > families/T32/pilot_i2/chain_final.done
