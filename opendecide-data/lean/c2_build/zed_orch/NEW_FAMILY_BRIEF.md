# Brief: building an A42 agentic/coding family (wave 1: T40 CALL-GATE, T41 TAINT-GATE, T42 CODE-EXEC)

Read `c2_build/zed_orch/RULES.md` first; it binds you. Then read:
- `jev/reports/research_oct14/FINAL_PLAN.md`:
  - section 3: your family's row of the table, the probes and the "held out for the sealed split" list;
  - section 4: OHS-AC;
  - section 2: your item.
- `jev/opendecide-data/lean/teach1/C2_DATA_SPEC.md` sections 3.0, 4, 6.3 and 6.4.
- The kit in `c2_build/c2_kit/`:
  - `plugin.py`: the interface every family implements;
  - `pipeline.py`: build_unit and the gates;
  - `choiceplan.py`, `cards.py`, `polarity.py`, `distractors.py`, `relations.py`;
  - `c2_build/zed_orch/kit_instructions.txt`.
- One exemplar family end to end: `c2_build/families/T28/` (`plugin.py`, `solver_b.py`, `G0_SPEC.md`, `run_pilot_i1.py`,
  tests). Use `c2_build/pilot.py` (build_pilot, the gates) to run your in-memory checks.

## What to deliver, in `c2_build/families/<ID>/`
1. **`G0_SPEC.md`**, G0-lite (at most about 2 pages). It covers:
   - the decision and the exact heads and options from FINAL_PLAN section 3;
   - gold (solver A) and the independent verifier (solver B, a different paradigm);
   - the training samplers and the HELD_OUT_SAMPLERS, which implement the sealed configuration in FINAL_PLAN
     section 3 "Held out for the sealed split" (held-out registries and naming styles, idioms, operators, fault
     type, plan lengths, as they apply);
   - at least 3 G4 metamorphic relations, the question forms and cards;
   - answer and option balance, the token budget and the row budget.
2. **`plugin.py`**: the kit Plugin. Gold is computed only by program or execution, never by a model.
3. **`solver_b.py`** plus any oracle or executor modules.
4. **Tests (pytest):**
   - solver A equals solver B on at least 2,000 sampled specs;
   - determinism under two PYTHONHASHSEEDs;
   - an in-memory build of at least 3,000 rows through `pilot.build_pilot` with a loader that your own runner
     registers at runtime (`pilot_loaders.LOADERS["<ID>"] = ...` inside your runner; do not edit
     `pilot_loaders.py`);
   - on that build, the options-only probe and the formatting-only probe are at chance ± 3 pp (coding families also
     get a diff-size probe);
   - pilot.g6, g7 and g10 pass at the C2 bars;
   - a 3% reseed audit with at most 1% label flips.
5. **`run_pilot_i1.py`**: same pattern as T28's; it must support `--dry-run`, `--n` and `--no-g15`.
6. **Surface text:**
   - First make it work with program/template text only, so the pilot can run before any Haiku text exists.
   - If natural-language surface text would add realism (user requests, documents, docstrings), write Haiku
     authoring task files plus an admission checker under `haiku/`, in the format other families use, and do NOT run
     them. Claude text is never gold.
7. **`BUILD_NOTES.md`**: what exists, the test results, the measured probe numbers, the open items, and the exact
   commands for the sealed run and for the pilot.

## Hard constraints
- **Gold:** program or execution gold only. Execution is hermetic: venv CPython 3.12, `PYTHONHASHSEED=0`, a
  subprocess with a 5 s cap, no network and a temp dir.
- **Libraries:** standard library plus what is already in `/Users/aryamahadik/Documents/jev/opendecide-data/.venv`.
  jsonschema, libcst and hypothesis are NOT installed and there is no network: write minimal validators yourself.
- **Prompts:** mean ≤ 800 tokens, max 2,000 (instructions count twice). At most 64 rows per card; 20-30 or more
  cards or specs.
- **Balance:** as in spec 3.0. Use the kit choiceplan (abstain share 1/k, gold position, length balance). Respect
  the class floors in FINAL_PLAN section 3 (for example CALL-GATE ≥ 40% VALID, TAINT-GATE ≥ 45% benign).
- **No rows on disk and nothing sealed:**
  - Write NO row files to disk. Only in-memory builds and test fixtures of at most 50 rows.
  - Never create or write `lean/ohs_ac_sealed/`. The sealed split is emitted later by a separate sealed agent through
    your HELD_OUT_SAMPLERS.
- **Shared code:** do not modify shared kit files. If the kit lacks something, put a helper in your family folder
  and list it in BUILD_NOTES as a kit candidate.
- **Budget:** aim for at most about 150 tool calls. Spend them on correctness of gold and balance, not on prose.
