# T60 solver B (independent, string side)

A deterministic PROGRAM (stdlib only, no files read at run time, no LLM, nothing executed) that reads the RENDERED row, recovers the facts and
recomputes the label by the G0-lite rule. It was written from `G0_LITE.md` (incl. the Opus batch-1b block), `G0_APPROVALS_v32.md` and
`ROW_SCHEMA.md` only; it never imports or reads the in-generator gold function (solver A), the oracle, the rule or the model files.

## Method (and how it differs from A)
* A computes the label over the SPEC (rule tables; H2 needs-set). B works on the TEXT.
* H1: parse the card numbers (S, V, B, R), the brief (steps, read sizes, needs, result size, writes, incoming) and the pending main steps; apply
  SIZE and BRIEF and BOUND and FREE (written paths compared with the pending steps' reads and writes after path normalisation).
* H3: parse the card numbers (H, n_min), the steps with their visible effect phrase, the order statements and the data-flow lines. R1 (a step is
  not undoable / reaches outside / changes N >= H), R2 (steps >= n_min), R3 (a data-flow edge not implied by the TRANSITIVE CLOSURE of the order
  statements, closure built by graph search).
* H2 by ABLATION (G0-lite 3.5): parse the card (does it count recovery steps), the plan (todo/done, contingency host, references), the transcript
  (turn -> fact) and the quoted fact; resolve the reference grammar L1 handle / L2 role description / L3 ordinal (get outputs only) / L4 chain or
  pointer; run the plan twice in a simulated state, with the full context and with the quoted fact REDACTED (a hole, so ordinals do not shift; a
  "reminder" turn that restates it is redacted with it, a second separate statement is not). A step runs if it is todo and unconditional, or a
  contingency step of a todo host while the card counts recovery steps; it fails if a reference resolves to the hole. KEEP iff a step runs in the
  baseline and fails in the ablated run. The latest fact with the same handle and entity replaces the earlier ones; done steps take nothing; a
  chain reference takes what step K takes when K is todo.
* Same-value supersession ABSTAINS (Opus ruling Q1, 18 Oct). It is outside the spec, so B does not label it. Facts with the same handle and
  entity (any type) must have pairwise distinct values over the whole transcript (this excludes A -> A, A -> B -> A and A -> B -> C -> A, wherever
  the quoted fact sits, also when the repeat is in another chain than the quoted fact's): otherwise `parse_gap:h2_same_value_supersession`. A
  repeat-marker ("As a reminder") turn on a fact that has a revision in the transcript abstains too:
  `parse_gap:h2_repeat_marker_in_supersession_chain`. The labelling rule itself is unchanged.
* Rendered-grammar additions of 18 Oct 2026 (ROW_SCHEMA "Additions", Opus ruling Q6 + owner A102), read from that text only:
  - `Background notes:` (all heads): the header and its indented prose lines are dropped before any parser runs (`t60b_text.strip_notes`).
  - H1: paths are compared after collapsing `./` and `../`; SHARED (a `- writes:` path is read or written by a pending main step) and FED (a `- reads` file is a path a pending
    main step WRITES) both fail FREE; every `- reads` line counts for the volume, a fed file included; `- the <h1> is the <h2> plus <k>` is an ordinary main-thread fact (only the
    handles named in `needs from the main thread` count for the brief predicate).
  - H3: `reaches people outside the team (can be undone for D more days)` is external (high stakes); `can be undone for D more days (the step runs in E days)` is undoable only if
    D - E >= 1; `- the steps are numbered in the order in which they are to be carried out` states every consecutive pair s(i) before s(i+1) (closure taken as for explicit order
    lines; if the listing order and the numbering disagree B abstains, `h3_numbered_listing_order_ambiguous`); `- sB uses a value derived from the output of sA` is the same data-flow edge as
    `sB uses the output of sA`.
  - H2: an emphasis suffix on the fact line (a `path:` line included), identifier-shaped and large values are plain values; a repeat marker never sits on a supersession chain (abstain if it does).
  - READING TO CONFIRM (Opus): a plan reference of ANY level (L2 role description, L3 ordinal, L4 pointer) that lands on a SUPERSEDED fact takes the CURRENT value of that role, because
    G0-lite 3.4 says "a fact superseded by a later fact with the same role handle is not needed (the current value is)" and ROW_SCHEMA says "a fact is replaced by the latest fact with the
    same <handle> and <entity>". Before 18 Oct B resolved "the first record fetched by a get call" to that exact record even when a later get replaced it; the new supersession rows with an
    ordinal onto a superseded record exposed this (55 of 247 supersede rows in the official run; 40 disagreements with the old reading, all of this one form). The text states the clause without
    a level qualifier, but it never spells out the L3 case, so Opus should confirm it.
* Option letters: `solver_b` takes the letter from the TEXT of `view["options"]`; `render_b` takes it from the lettered lines of
  `rendered.options_text`. The `label` field of an option is never read. Any unknown construct => abstain (never a guess).

## Files
`t60b_text.py` (head, options, shared parsers) `t60b_h1.py` `t60b_h2.py` `t60b_h3.py` `hook.py` (plug points) `agree.py` (in-memory agreement
harness; the ONLY file that imports the generator side) `make_shas.py` -> `SHAS.json` `agreement_log.json` (counts only) `tests/`.

## Run
    from solver_b import hook        # or put this folder on sys.path and `import hook`
    <T60 checked module>.adapter(solver_b=hook.solver_b, render_b=hook.render_b)
    hook.solver_b(view) -> Result(label, letter, abstain, reason, parsed);  hook.render_b(view) -> ("letter", X) | ("abstain", why)
    hook.parse_view(view) -> the recovered facts (for the K1 / K14 round-trip checks)
    PYTHONDONTWRITEBYTECODE=1 python3 agree.py --rows 1000 --seeds a,b,c --out SCRATCH/agree.json [--log] [--a10] [--standin]
    PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q          # from this folder (pytest.ini sets rootdir and no cache)
    python3 make_shas.py                                    # rewrites SHAS.json
