# RESUME NOTE (1 Oct 2026, about 6 pm EDT / 22:00 UTC): where to continue when the laptop reopens

## State
- **4B:** q35_4b_main500k is FINISHED, 30,457 steps. Backup: backups/modal_models/q35_4b_main500k.
- **Gate (1 Oct 21:11 UTC):** DO NOT SHIP. It is +2.47 pp on unseen sources and better on almost everything, but
  constraint (e), equivalence flips, failed: 8.86% vs 5.68%, all from devp_card double-negation pairs.
- **Owner decision:** the new 4B is OUR model. Keep the 4B-E files; do not delete them.
- **Owner instruction:** FIX the double-negation weakness, but do NOT launch any fix until the research is done.
- **L4 VMs:** od-l4 (original, us-central1-a) STOPPED; od-l4b (clone, us-east4-c) STOPPED.
- **Modal:** nothing running. October credit $141 left.

## Running when the lid closed (local workflows; they may need resuming)
1. **w74nvebvo** (research-dneg-fix): web research on negation / repair without regression / consistency + local
   diagnosis, then synthesis and skeptic.
   - If interrupted: re-run with Workflow scriptPath
     .../workflows/scripts/research-dneg-fix-wf_234b6397-3bc.js, resumeFromRunId wf_234b6397-3bc.
2. **ww3izlexw** (fix-4b-dneg-topup-prep): CPU prep of the top-up: data mix, config, A8 draft, launcher.
   - Resume id wf_b7d5cc2e-03e (script .../fix-4b-dneg-topup-prep-wf_b7d5cc2e-03e.js).
3. **wuaz2itsk** (prep-steps-8-9): readout settings from dev + the OHS-3 harness.
   - Resume id wf_13878454-68a (script .../prep-steps-8-9-wf_13878454-68a.js).

## Next steps, in order (the GO rules apply)
1. When the research finishes: show the owner ONE recommended fix plan + a backup (effect, regression risk, cost).
   Wait for the owner's choice.
2. Launch the chosen fix: a top-up (about $8, extra/relay_spawn.py style so it survives the laptop going offline) or a
   merge (no training).
   - Pre-register the re-check (A8) BEFORE any candidate prediction.
   - Re-check on the ORIGINAL L4 od-l4 with gate/gate_4b_l4.sh; the owner wants the original machine for the 4B
     gate.
3. Final 4B is decided (fixed 4B, or the new 4B by override).
   - Run the JevBench public run on the final 4B (free L4, about 30 min); the owner wants this.
4. 2B teacher: waiting for the owner's "OK plan" (wait for the final 4B and relabel, about $23).
   - The 2B pilot needs GO, plus the rule choices in reports/MORNING_REPORT_1oct.md.
   - Pilot on 2 L4s (original + clone), or on Modal if the owner adds an account.
5. 2B main (about $74), then readouts + direct-hosting test, then OHS-3 once at the end, then the report.

## Key files
- Gate: lean/logs/gate4b/look_ship1.txt, summary.json; ledger lean/logs/budget_ledger.md.
- Relays: lean/logs/main4b_relays.md. Memory: final-goal-30sep.md.
