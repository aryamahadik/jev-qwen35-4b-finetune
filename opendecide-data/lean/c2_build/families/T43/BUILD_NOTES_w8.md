# T43 w8 (16 Oct, Sonnet 5.5): state after four more diff-size iterations
Pre-existing (w4b-w4d, other agent): cell-first draw; ll/lf/pv per-head G6, options-only, formatting-only all PASS at 10,206 rows (w4d: max cell +1.87 pp ll gbt; probes within +-2.1).
Open: A42-D 3.2 diff-size probe (bar majority + 3 pp). w4d (10,206): lr +3.25, gbt +4.06 (7,000-row prefix passes). w8 variants (quick builds, 10,206 rows):
 w8q (B/C hunk count = A-reference hunk count; CURRENT plugin.py): lr +3.1, gbt +2.0 (5,999-row prefix passes both); w8b (+exact added/removed): +4.2/+4.0;
 w8c (+token signature, A core fixed): +4.0/+3.5; w8d (+pad count enforced): +3.2/+3.5; w8e (+gold line closed to rewrites): +3.9/+5.1. Only w8q is kept.
Null (labels shuffled) probe is within +-1 pp, so the +3 pp is a real, small size signal. Residual: label shares rise for B at the largest patches (added 7, removed 3, hunks 4).
Hypothesis for next iteration: pads land differently around the gold hunk for A vs B/C (merge/split of hunks); choose pad lines from the key before the core edit.
Backups: _backup_w8/ (plugin.py as found, plugin_before_tuple.py, plugin_w8e_tuple_pads.py). Tests not re-run after w8q (A==B test needs a rerun; it failed once at S2 seed 379 before patch9, which now samples).
