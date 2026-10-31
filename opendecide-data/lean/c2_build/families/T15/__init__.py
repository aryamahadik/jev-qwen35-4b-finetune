"""c2_build/families/T15: eligibility gates and ordered claimant cascades (C2_DATA_SPEC 2.1, 3.14). Code only before
A38.

  plugin.py      sampling, solver A (ordered decision lists: rules.RuleSet first_match + a rule-step cascade),
                 rendering, relations, error models
  solver_b.py    independent parser of the rendered row + solver B (decision-table enumeration: a gate truth table
                 and a pairwise claimant duel table)
  fixtures.py    in-memory stand-ins for Haiku skins / wordings / attack lines and the lexicon (tests only)
  G0_SPEC.md     the one-page G0-lite spec (sha frozen in plugin.T15Plugin.G0_SHA256)
  test_plugin.py in-memory tests (A == B, relations, balance, G-SL, determinism, error models, gate teeth)
  haiku_author.py  the Haiku authoring tasks (G0 section 3; written under haiku/author/) and their answer loaders
  test_haiku_author.py  in-memory tests of the task batches, the loaders and Haiku-shaped packs driving the plugin
  haiku/ambiguity/amb_T15_points.json  the one Haiku ambiguity pass (resolved in G0 section 6)
"""
