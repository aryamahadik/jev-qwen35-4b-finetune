#!/bin/bash
# Runs the fast CPU tests (everything except the slow real-model one) and writes tests/logs/<test>.txt. Read-only use of the opendecide venv.
cd "$(dirname "$0")"
PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python
for t in test_adapter_gate_identical test_lockcheck test_rows_vs_c1_and_bench test_scoring_synthetic test_run_text_tiny; do
  $PY -B -I $t.py > logs/$t.txt 2>&1; echo "$t exit $?" | tee -a logs/summary.txt
done
