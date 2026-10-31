# T59 solver B (independent, string side)

**Method.** `parse.py` is a deterministic parser of the RENDERED row (`rendered.context`; the option text for the letter). It recovers the card
slots (mode, H and unit, defaults, read-first, retry cap, precedence), the tool list (verb, noun, parameters with optionality and declared
defaults, read/write, idempotent, exposure, undo window, key, authority), the repo environment line, the user turns (request, stated values,
option lists, delegation, qualifier, cap statement, notes, prerequisite, tree state, candidate lists), the call history with outputs and the
planned step. `rules.py` then builds, from those facts only, the open slots, the interpretations (candidate actions with effect records) and
evaluates the G0-lite GOLD order: E empty -> ASK; ROBUST (R-SAME, R-DEF, R-COM, R-RES) -> PROCEED; card OFF -> ASK; card ON -> ASK iff some
interpretation is IRREV (not undoable, or magnitude >= H; a non-external create is undoable; a read is never IRREV), plus the T6 sub-cases of
G0-lite 3.3.1. `hook.py` maps the label to a letter through the TEXT of the options (the given `label` field is never read).
No file is read at run time, nothing in the text is executed, no model is called; stdlib only.

**How it differs from A.** A works on the structured scene/case (`derive_case`, gold function, brute-force oracle). B never sees them: it
re-derives every fact from the sentences, tool lines and call text, so a renderer that fails to show a decisive fact makes B abstain or
disagree (K1/K2). Unknown phrasing is an ABSTAIN (parse gap), never a guess; a structure that contradicts the `sub_block` input also abstains.

**Plug-points.** `hook.solver_b(view)` -> object with `.label .letter .abstain .reason`; `hook.render_b(view)` -> `("letter", X)` or
`("abstain", why)`. `t59_checked.adapter(solver_b=hook.solver_b, render_b=hook.render_b)`.

**Run.**
- tests: `cd c21_fam/T59 && PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -p no:cacheprovider solver_b/tests -q`
- agreement (in memory; imports the generator side, only this file does): `PYTHONDONTWRITEBYTECODE=1 python3 solver_b/agree.py --rows 2000 --seeds a,b,c --levers --pipeline --out <scratch>/report.json [--real-names] [--log]`
  (`--log` rewrites the counts-only `agreement_log.json`; K2 bar 99.0%).
- hashes: `python3 -I solver_b/shas.py` -> `SHAS.json`.

**Post-hoc change record (G1 breach, reverted by Opus ruling Q2, 18 Oct).** Solver B first followed G0-lite 3.3.1 for the two T6 sub-cases
"ambiguous write, neither key nor read path" and "invalid_named, corrected value not in context" (flat ASK). It was then CHANGED to the 3.2
GOLD order (OFF -> ASK; ON -> ASK iff IRREV) AFTER seeing solver A's labels. That change is a post-hoc edit made with A's labels in view, so the
agreement obtained with it is not evidence. It is REVERTED by the Opus ruling Q2 (RULINGS_T59_T60_T63.md): 3.3.1 binds for T6 on every card,
ON or OFF, whatever the undo path and the magnitude. B now returns ASK for both cases directly (rules `E_empty_ambiguous_no_key_no_read`,
`E_empty_invalid_named_value_missing`), never through `_gold_tail`. The reverted B is the one used for K2; every earlier agreement log is void.
One further case the ruling calls "not cleanly covered" (ambiguous write, a read path listed, card WITHOUT read-first, planned step the plain
write) is an ABSTAIN (`t6_read_path_without_read_first`) in B; the generator must never build it.

**Read path (Opus ruling "Q2 follow-up" FU5, 18 Oct).** A READ PATH is ANY listed read-only call on the target's noun (`list_`, `get_`, `find_` ...), not only `get_`
(`rules.read_path_tools`). It is used wherever a read path decides a label: T6 ambiguous write (key -> PROCEED; the planned step is the read -> PROCEED; a read path
on a read-first card -> PROCEED R-RES; neither key nor read path -> ASK) and T7 (read-first card + any read-only call on the noun, the e14 authoritative re-read
included -> PROCEED R-RES; so the get_ call that produced a tool result counts too). A read-only call on another noun is no read path. A row that lists a read path on
a card WITHOUT read-first (the card's other facts say "no read path") is an inconsistent row: B abstains (`t6_read_path_without_read_first`). T8 has no read-path
rule in B (its fork is an INTENT/observation fork and a resolver never settles INTENT, D5).

**ROW_SCHEMA pointer (ruling FU3).** After B was written, the generator side adds one line to ROW_SCHEMA.md under "What the label is": "T6 error classes follow G0-lite
3.3.1, which overrides steps (3)/(4) for T6 (Opus ruling Q2, 18 Oct): an ambiguous write with neither key nor read path = ASK, and invalid_named_arg with the corrected
value not in context = ASK, on every card." B already followed 3.3.1 (see the post-hoc change record above); the line is a documentation correction, not a new rule.
