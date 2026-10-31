# T60 ROW SCHEMA (input for the solver-B session; spec_k1 for T60). Solver B is a PROGRAM written from G0_LITE.md and THIS file only.

Solver B reads the RENDERED ROW (`rec["rendered"]["text"]`, `rec["options"]`) and returns {label, letter} (or abstains). It never reads `rec["scene"]`
or t60_rule.py. Heads and labels: H1 DELEGATE / DO_HERE, H2 KEEP / DROP, H3 PLAN / ACT; two lettered options, order shuffled. The head is told by
the question line ("... hand this subtask to a separate worker ..." / "... context summary ... kept ... dropped" / "... write out a plan ...").

## Record fields
As T59 (sub_block = "h1" | "h2" | "h3"; the pipeline reserves the key `head`, so the head is `hd`). Tags never rendered: hd, edit, ctl, cell
(quad cell), h2kind, levels, scenario_id (the group id; K21 twins and K19 splits use it), decisive (the registered decisive mechanism of the row, t60_levels.DECISIVE,
"-" for the control singles), lever_tag, split, twin_of, a12, wrapper.

## Rendered text grammar
CARD lines first (a title line, then 4 lines for H1 (size, brief, bound, free), 2 for H2 (keep rule, recovery), 3 for H3 (high stakes, steps, order)),
each with its visible numbers.
H1  numbers on the card: S (steps), V (tokens), B (facts), R (result tokens). Then
    "The agent is working on ..." / "The main thread is busy with ...", `Main thread facts:` (`- the <handle> is <value>`), `Main thread pending steps:`
    (`- mK: reads <paths>; writes <paths>`), `Candidate subtask (hand-off brief):` with `- steps:` (numbered lines), `- reads <path> (N tokens)`,
    `- returns a summary of the findings (N tokens)`, `- needs from the main thread: the <handle>, ... | nothing`, `- writes: <paths>`,
    `- input from pending main steps: mK | none`.
    DELEGATE iff steps >= S OR sum(read tokens) >= V; AND needs <= B; AND result tokens <= R; AND the written paths do not occur in any pending main
    step's reads / writes AND the incoming list is `none`. Else DO_HERE.
H3  card: H (units) and n (steps). Then `The request: carry out the steps listed below.`, `Order given in the request:` (`- Do step sA before step sB.` /
    `- Step sA has to come before step sB.` / `- no order is given`), `Steps:` (`- sK: <phrase> (changes N <unit>s; <effect>)`, <phrase> = `<verb> the <entity> <id>` in the tool world or a shell step `rm P` / `mkdir P` / `touch P` / `mv SRC DEST` / `cp SRC DEST` in the repo world (both operands are always shown), with effect one of
    "can be undone for D more days" | "cannot be undone" | "reaches people outside the team" | "creates a new object that can be removed again" |
    repo: "the working tree is clean, so git can restore it" | "creates a new file in this session" | "the file was made in this session and is not
    tracked"), `Data flow ...:` (`- sB uses the output of sA`). A step is HIGH STAKES iff it is not undoable (no undo / not clean / external) or
    N >= H (a create of an agent-made, non-external object is undoable). PLAN iff some step is high stakes AND #steps >= n AND some data-flow edge is
    not implied by the transitive closure of the order statements. Else ACT.
H2  card: keep rule + one recovery line ("... count as steps still to run" = counts / "... do not count ..."). Then `Task: ...`, `Remaining plan:`
    (`[done|todo] step K: <verb> the <entity> using <reference>[ and <reference>]`; a contingency step reads `[todo] step K (only if step J fails): ...`),
    `Context transcript:` numbered events `(n) User: ...` / `(n) Agent called <call>` + `-> output:` + `key: value` lines, and the QUOTED FACT line
    `Fact in question (turn n, <type>): <handle>: <value>`. References: L1 `the <handle>`; L2 `the value given|returned|we agreed for the <entity>` /
    `the key recorded for the <entity>` / `the saved location for the <entity>`; L3 `the <ordinal> record fetched by a get call` (ordinal among the outputs of `get_<entity>` calls ONLY, in transcript order; the outputs of
    check_, create_, export_ and read_ calls are never counted); L4 `the value derived in step K` (what step K takes, if K is todo) or `the saved location of the <entity> snapshot` (the
    pointer fact of the artifact, never its content). KEEP iff some todo step on the unconditional plan (plus contingency steps of todo hosts when the
    card counts them) takes the quoted fact; a fact is replaced by the latest fact with the same <handle> and <entity>; a done step takes nothing.
    Solver B decides by ABLATION: redact the quoted fact, run the todo steps in a simulated state, KEEP iff a step fails for lack of it.
No instruction to the agent about remembering or keeping ever appears in a row; outputs are `key: value` data lines only.

## Additions of 18 Oct 2026 (Opus ruling Q6, ladder design). The label rules above are unchanged; these lines are new in the RENDERED text
- BACKGROUND NOTES (all heads, any row): after the card lines an optional block `Background notes:` followed by indented lines of neutral prose
  (`  The review group refreshed ...`). They carry no fact, number or instruction: ignore them. Both members of a group carry the same notes.
- H1 paths. Paths are compared after collapsing `./` and `../` segments (`/a/b/./x` and `/a/b/c/../x` are `/a/b/x`; `/a/b/../c/x` is `/a/c/x`).
  SHARED: a path in `- writes:` equals (after that collapse) a path read or written by a pending main step. FED (new): a file of `- reads <path> (N tokens)`
  equals a path that a pending main step WRITES (the subtask would read what a pending step still has to produce). DELEGATE needs `input from pending main
  steps: none`, no SHARED and no FED; otherwise FREE fails. The `reads` volume counts every `- reads` line, a fed file included.
- H1 main-thread facts. A fact line may read `- the <h1> is the <h2> plus <k>` (a value stated through another fact). It is still a main-thread fact; only the
  handles named in `needs from the main thread` count towards the brief predicate.
- H3 effects (tool world). `reaches people outside the team (can be undone for D more days)`: the effect is external (high stakes) although an undo path
  exists. `can be undone for D more days (the step runs in E days)`: the undo window runs from now and the step runs E days later; the effect can be
  undone only if D - E >= 1, otherwise it counts as `cannot be undone` (high stakes). Without the parenthesis E = 0.
- H3 order. `- the steps are numbered in the order in which they are to be carried out` states the order of the steps as listed: every consecutive pair
  s(i) before s(i+1) is stated (and their transitive closure). Data-flow lines may read `- sB uses a value derived from the output of sA`: the same
  dependency as `sB uses the output of sA`.
- H2 markers. Pair kinds (pointer, supersession, step-done, recovery) now also carry quad markers on the quoted fact(s): a striking / remarkable / notable
  suffix on the fact line (a `path:` line included), an identifier-shaped or large value. `repeat` (a second user turn) never occurs on a supersession chain.
- H2 ordinals (Opus ruling Q6 batch 2, B2-1). The reading rule is unchanged (a reference of any level takes the CURRENT value of the fact it resolves to). The generator
  never builds an L3 ordinal reference, in any step, that lands on a superseded record: the ordinal names the latest record of a chain, and the superseded records of the
  chain are still counted as positions among the fetched records. If solver B ever meets the case it abstains.
