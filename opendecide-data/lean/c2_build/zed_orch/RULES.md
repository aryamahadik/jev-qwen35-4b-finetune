# Rules for every Zed subagent on the C2 build (binding; read before anything else)

Project root in tool paths: `jev/`. The C2 build is `jev/opendecide-data/lean/c2_build` (absolute:
`/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build`). Run Python from that folder as
`/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python -B ...` (set the terminal `cd` to
`jev/opendecide-data/lean/c2_build`).

## Binding documents
- `jev/opendecide-data/lean/teach1/C2_DATA_SPEC.md`: sections 3.0, 4, 6.3, 6.4 (gates and the fix loop).
- `jev/opendecide-data/lean/PREREG_FINAL.md`: amendments A37, A38, A40, A42 (with the A42 erratum) and A43.
- `c2_build/README.md`, `c2_build/STAGE_B_PILOT_REPORT.json`, `c2_build/FIX_ITER1_REPORT.json`, and each family's
  `pilot/PILOT_REPORT.json` + `pilot/PILOT_VERDICT.json` (when present).
- Kit changes from fix iteration 1 (what families must call): `c2_build/zed_orch/kit_instructions.txt`.
- The A42 plan: `jev/reports/research_oct14/FINAL_PLAN.md`.

## Never
- Never open, read, list or search any path containing "ohs" (any case), `sealed_nd`, `c_spec/sealed_brief`,
  `c_build/preread`, `bench/external_quarantine` or `bench/longbench_v2`. Never open any file or folder *inside the
  repo* whose own name contains "jev" (Jev model outputs). Also never open `~/.claude/**` or `/private/tmp/claude-501/**`.
- No paid compute and no network: no Modal, GCP, OpenRouter, Hugging Face or web fetches. No git commits.
- Never edit pinned `lean/*.py` or `lean/c_build/**` files. Never edit `c2_build/pilot.py`, `c2_build/pilot_loaders.py`
  or `c2_build/c2_kit/**` unless your task says so explicitly (other agents run in parallel; shared files would conflict).
- Generator/template fixes only (spec 6.4 step 6). Never relabel. Never loosen a gate bar or lower a G0 target.
- You cannot run Haiku or any model. If a step needs Haiku (authoring, blind reads, G-LEX reads), write the task files
  and their admission checks, list the exact paths in your notes and stop at that step. The orchestrator runs Haiku.

## How to work
- Large files: `read_file` returns an outline. Read the needed line ranges with start_line/end_line.
- Long runs: start them in the background (`nohup ... > out 2>&1 &`), then poll with short commands. Bound every
  command with `timeout_ms`. Keep terminal output small with `head_lines` or `tail_lines`.
- Before editing a family's `plugin.py` or `G0_SPEC.md`, copy them to `<family>/_backup_<step>/`. These folders have
  no git history.
- If a script error persists after 2 attempts, stop and report it.
- Write details to files in your family or task folder, not into the chat.
- Final reply: at most 120 words: one status line, failing gates (number vs bar), the files written and open items.
