# c_build/preread: C1 pre-reads (PREREG A21 d)

- Kept sealed until the 6.3 gate / final report: **sha256 only** (`PREREAD_MANIFEST.json`). No score is computed or
  looked at here.
- `sealed_preread_c1/` holds C1's predictions on the A15 sealed suite. They are keyed by option text, so they are
  **sealed text**. Never open, cat, head or grep them; programs only (gate_c.py / the sealed scorer).
- `preread_c1/`: dev / attack reads (`q35_4b_main500k_pre`, `_perm`, `_revchoice` or `_served`).
- How to produce them: `c_build/endgame/RUNBOOK.md` section P2. **Status 6 Oct 05:35 UTC: not run yet** (payer
  decision pending).
