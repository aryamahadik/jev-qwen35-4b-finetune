"""c2_build/families/T42: CODE-EXEC, code execution reasoning (A42; FINAL_PLAN section 3, row 2).

  plugin.py      sampling, solver A (hermetic execution), rendering, G4 relations, error models (mutants)
  executor.py    the hermetic runner: venv CPython 3.12, PYTHONHASHSEED=0, subprocess, 5 s cap, temp dir, no network
  exec_child.py  the child program (snippets, equivalence grids / fuzz / branch coverage with sys.settrace)
  gen_out.py     typed templates of the output head;  mutate.py: the mutation operators (distractors)
  gen_eq.py      function-pair skeletons of the equivalence head
  solver_b.py    independent parser + tree-walking interpreter + grid enumeration (solver B)
  texts.py       rules and wordings;  probes.py: options-only / formatting-only / diff-size probes
  G0_SPEC.md     the G0-lite spec;  BUILD_NOTES.md: results, probes, commands, open items
  run_pilot_i1.py  the pilot driver (--dry-run, --n, --no-g15);  test_*.py: pytest
"""
