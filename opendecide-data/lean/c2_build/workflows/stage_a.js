export const meta = {
  name: 'c2-data-stage-a',
  description: 'C2 data stage A: sealed-side decontam tools; prep fixes + C2 G13 wrapper; per family: Haiku ambiguity pass -> lead resolves + freezes G0 + writes Haiku authoring tasks -> Haiku authors pools -> lint + lexicon extraction tasks -> Haiku extraction reads -> admission and frozen pools',
  phases: [
    { title: 'Sealed tools', detail: 'sealed agent: hash-only exports copy + sealed-side checkers (counts/ids only)' },
    { title: 'Prep', detail: 'fix post-A38 tests, T32/T23 rank cues, C2 G13 wrapper' },
    { title: 'Ambiguity', detail: 'Haiku reads each G0-lite spec' },
    { title: 'Resolve', detail: 'family lead (Opus): resolve, freeze G0, write Haiku authoring tasks' },
    { title: 'Author', detail: 'Haiku authoring agents (packs, skins, wordings, paraphrases, documents)' },
    { title: 'Lint', detail: 'Haiku: load answers, G-SL lint, lexicon extraction tasks' },
    { title: 'Extract', detail: 'Haiku extraction reads for G-LEX admission' },
    { title: 'Admit', detail: 'Haiku: G-LEX admission, pool freeze, shortfall report' },
  ],
}

const ROOT = '/Users/aryamahadik/Documents/jev'
const LEAN = ROOT + '/opendecide-data/lean'
const SEALED = LEAN + '/ohs4_sealed'
const PY = ROOT + '/opendecide-data/.venv/bin/python'
const C2 = LEAN + '/c2_build'
const FAMS = ['T28', 'T35', 'T33', 'T29', 'T30', 'T27', 'T26', 'T31', 'T32', 'T01', 'T23', 'T24', 'T06', 'T15', 'T12', 'T07', 'T25']
const EXTRA = ['t37b', 'T36', 'T19', 'T21', 'T20']   // t37b builder + transfer-dev families

const C2RULES = `You work on the C2 training data for OpenDecide. Binding: ${LEAN}/teach1/C2_DATA_SPEC.md, PREREG A37 + A38 (grep "Ruling A37"/"Ruling A38" in ${LEAN}/PREREG_FINAL.md), ${C2}/README.md (kit, plugin contract, Haiku task flow). Python ${PY}; work dir ${LEAN}.
RULES: never open any path containing "ohs" (incl. ${SEALED}), sealed_nd data, c_spec/sealed_brief, c_build/preread, bench/external_quarantine, bench/longbench_v2, any "jev" file, ~/.claude/projects/**, /private/tmp/claude-501/**; never edit pinned lean/*.py or existing c_build files (new C2 files only, under ${C2}); no paid/remote compute, no OpenRouter, no git commits; never set or edit a label by hand (gold comes only from solver A with solver B agreement; Haiku output never sets gold); never loosen a gate bar. Use the kit's guarded writers (paths.write_files / write_jsonl). Report honestly with counts.`

const OUT = { type: 'object', properties: { status: { type: 'string', enum: ['ok', 'partial', 'failed'] }, counts: { type: 'object', additionalProperties: { type: 'number' } }, tasks: { type: 'array', items: { type: 'object', properties: { task_file: { type: 'string' }, answer_file: { type: 'string' }, kind: { type: 'string' } }, required: ['task_file', 'answer_file', 'kind'] } }, issues: { type: 'array', items: { type: 'string' } } }, required: ['status', 'counts', 'issues'] }

phase('Sealed tools')
const sealedTools = await agent(`You are a SEALED agent for OpenDecide's frozen final test OHS-4 in ${SEALED} (read ${SEALED}/BRIEF.md and BUILD_LOG.md first). You may read the sealed folder; you must never open lean/teach1/, any C2 spec text or other "ohs" paths, sealed_nd data, quarantine, "jev" answer files, ~/.claude/projects, /private/tmp/claude-501. Python ${PY}. Do not modify any file listed in ${SEALED}/MANIFEST.json (the freeze).
TASKS (log in BUILD_LOG.md):
1) Copy ONLY the hash-only export files (no clear text; verify by program that every line is a hex digest or a {kind, hash} record) to ${C2}/sealed_hashes/ with a FORMAT.md describing exactly the normalisation and hashing so a C2 program can hash its own text the same way (tokenisation, lowercasing, n-gram sizes, sentence split), plus a manifest of sha256s. Nothing else leaves the sealed folder.
2) Write sealed-side child checkers in ${SEALED}/tools/ (new files; not in the freeze manifest): (a) g13_ohs4_check.py: input a JSONL path of C2 rows/units (fields id, state, instructions, card, options); it compares them against the FULL OHS-4 suite with decontam_g13-style methods (exact, substring, 10-gram, 12-gram, MinHash) and prints/writes ONLY counts and the C2 ids that hit (never OHS-4 text or ids); (b) gtpl_check.py: input a JSONL of C2 templates (id, text with {SLOT} placeholders); 8-gram compare (slots removed) vs OHS-4 R/U item wording; output only counts and hit C2 template ids. Add CPU tests with synthetic inputs. Write their usage to ${C2}/sealed_hashes/CHECKERS.md (commands, input format, output format; no OHS-4 details).
Return counts and paths only.`, { label: 'sealed:tools', phase: 'Sealed tools', schema: OUT })

phase('Prep')
const prep = await agent(`${C2RULES}
TASKS: (1) update the two c2_build tests that assumed A38 did not exist (test_c2_select.py::test_writers_refuse_before_a38, test_mix_c2.py::test_main_refuses_before_a38_and_without_drops) to test the post-A38 behaviour, without writing data; (2) fix the remaining rank cues in T32 (ch_due top rank 42% at k=3) and T23 (ch_version higher-sorting 62% at k=2) with the kit's order_key / ordered_k, rerun those families' tests; (3) build ${C2}/g13_c2.py: the C2 G13 wrapper per spec 6.1/6.3 (seed-first on Haiku pools, candidates, final mix) that runs c_build/decontam_g13.py's methods (import read-only, its existing targets incl. the sealed-side child for OHS-3 etc.) PLUS the OHS-4 checks: hash-compare against ${C2}/sealed_hashes/ (read ${C2}/sealed_hashes/FORMAT.md) and call the sealed-side checkers as subprocesses per ${C2}/sealed_hashes/CHECKERS.md (you may RUN ${SEALED}/tools/*.py as programs with input files you create outside the sealed folder; never open the sealed folder's files), plus C2 mixdev, transfer dev and T37b-dev targets once they exist. Output: counts by target and method and the C2 ids to drop; per-template quarantine for pools. Tests with synthetic data. (4) Run all c2_build tests and report.
Sealed tools report: ${JSON.stringify(sealedTools ? { status: sealedTools.status, counts: sealedTools.counts, issues: sealedTools.issues } : 'FAILED')}`, { label: 'prep', phase: 'Prep', schema: OUT })

const AMB = { type: 'object', properties: { points: { type: 'array', items: { type: 'object', properties: { where: { type: 'string' }, issue: { type: 'string' }, readings: { type: 'array', items: { type: 'string' } } }, required: ['where', 'issue'] } }, files_opened: { type: 'array', items: { type: 'string' } } }, required: ['points', 'files_opened'] }
const FLAGS = { type: 'object', properties: { n_items: { type: 'number' }, written_to: { type: 'string' }, files_opened: { type: 'array', items: { type: 'string' } } }, required: ['n_items', 'written_to', 'files_opened'] }

const famDir = id => (id === 't37b' ? `${C2}/t37b` : (['T36', 'T19', 'T21', 'T20'].includes(id) ? `${C2}/transfer/${id}` : `${C2}/families/${id}`))

const results = await pipeline([...FAMS, ...EXTRA],
  // Stage 1: Haiku ambiguity pass on the G0-lite spec (no data)
  id => agent(`Read ONLY the G0-lite spec file(s) in ${famDir(id)} (G0_SPEC.md or G0_LITE*.md; use Glob then Read). Do not open any other file. As a careful, independent reader, list every point where the rules, semantics, precedence, windows, rounding, question wordings or answer options could be read in two different ways, or where a closed-world assumption is missing. For each: where, the issue, and the competing readings. Report files_opened.`, { label: `amb:${id}`, phase: 'Ambiguity', schema: AMB, model: 'haiku' }),
  // Stage 2: lead resolves, freezes G0, writes Haiku authoring tasks
  (amb, id) => agent(`${C2RULES}
YOU ARE THE LEAD for family ${id} (folder ${famDir(id)}). A blind Haiku reader listed these ambiguity points in its G0-lite spec:\n${JSON.stringify(amb ? amb.points : [])}
1) Resolve each point (state the resolution in the G0-lite spec; change the plugin/solvers only if needed; keep solver A/B independent); rerun the family tests; freeze the G0 sha in the plugin (G0_SHA256) and record the Haiku task id of this pass.
2) Create the Haiku AUTHORING tasks for this family's pools exactly as its G0-lite and spec 3.0/3.x require (packs, slot-locked skins per register incl. held-out registers, question wordings / lexicon forms, precedence or window paraphrases, attack lines, free-form documents for Mode F), using c2_kit.chunker.make_batch with authoring briefs (forbid label words and question strings; slot placeholders must be kept verbatim) and paths.write_files under ${famDir(id)}/haiku/author/. At most 40 authoring tasks for this family; each task file must state the exact answer file path the agent must write. Do NOT run Haiku yourself.
Return tasks (task_file, answer_file, kind) and counts.`, { label: `lead:${id}`, phase: 'Resolve', schema: OUT }),
  // Stage 3: Haiku authors
  async (lead, id) => {
    const tasks = (lead && lead.tasks || []).filter(t => t.task_file.startsWith(C2 + '/')).slice(0, 40)
    const outs = await parallel(tasks.map((t, i) => () => agent(`You are writing training-text pieces for a decision dataset. Use the Read tool on exactly ${t.task_file} and follow its brief EXACTLY (keep every {SLOT} placeholder verbatim; never write numbers, dates, names, statuses, label words or negations outside slots unless the brief allows it; vary wording and register as asked). Do not open any other file. Write your output ONLY to ${t.answer_file} with the Write tool, in the format the brief specifies. Report files_opened and the number of items written.`, { label: `author:${id}:${i}`, phase: 'Author', schema: FLAGS, model: 'haiku' })))
    return { lead, authored: outs.filter(Boolean).length, n_tasks: tasks.length }
  },
  // Stage 4: Sonnet lint + extraction tasks
  (st, id) => agent(`${C2RULES}
Family ${id} (folder ${famDir(id)}): load the Haiku authoring answers (${st.authored}/${st.n_tasks} tasks returned; use c2_kit.chunker.load_answers or the family's loader), run G-SL lint (gsl.lint_template / lint_freeform / lint_values) and drop failing pieces (log reasons), dedup, then build the G-LEX extraction tasks for every lexicon form, precedence/window paraphrase and question wording that needs admission (2 independent reads; 3 for precedence and window rules) and the G3-H round-trip items for Mode-F documents if the G0 asks for them at pool stage. Write each independent read as its OWN chunk file (so 3/3 forms appear in 3 separate chunks) with make_batch + paths.write_files under ${famDir(id)}/haiku/extract/. Return tasks (task_file, answer_file, kind) and counts (pieces authored, lint dropped, forms needing admission). If a script error persists after 2 attempts, stop and report it exactly instead of improvising.`, { label: `lint:${id}`, phase: 'Lint', schema: OUT, model: 'haiku' }),
  // Stage 5: Haiku extraction reads
  async (lint, id) => {
    const tasks = (lint && lint.tasks || []).filter(t => t.task_file.startsWith(C2 + '/')).slice(0, 30)
    const outs = await parallel(tasks.map((t, i) => () => agent(`Use the Read tool on exactly ${t.task_file} and do what it asks for every item (extract the structured meaning / fields exactly as instructed; do not guess beyond the text). Do not open any other file. Write the answers ONLY to ${t.answer_file} with the Write tool in the requested format. Report files_opened.`, { label: `extract:${id}:${i}`, phase: 'Extract', schema: FLAGS, model: 'haiku' })))
    return { lint, extracted: outs.filter(Boolean).length, n_tasks: tasks.length }
  },
  // Stage 6: Sonnet admission + pool freeze
  (st, id) => agent(`${C2RULES}
Family ${id} (folder ${famDir(id)}): load the extraction answers (${st.extracted}/${st.n_tasks} returned), record them (reg.record_extraction; g3h.compare where applicable), admit forms by the G-LEX rule (2/2; 3/3 for precedence and window), quarantine pieces that fail, then FREEZE the family's pools (skins, wordings, lexicon, packs, documents) into ${famDir(id)}/pools/ with a manifest (sha256s, counts per kind/register, admitted vs target from the G0-lite). Report counts and every shortfall vs the G0 targets (do not lower targets). Do not generate rows yet. If a script error persists after 2 attempts, stop and report it exactly (file, command, error) instead of improvising.`, { label: `admit:${id}`, phase: 'Admit', schema: OUT, model: 'haiku' }),
)

return {
  sealedTools: sealedTools && { status: sealedTools.status, counts: sealedTools.counts, issues: sealedTools.issues },
  prep: prep && { status: prep.status, counts: prep.counts, issues: prep.issues },
  families: [...FAMS, ...EXTRA].map((id, i) => ({ id, admit: results[i] && { status: results[i].status, counts: results[i].counts, issues: results[i].issues } })),
}
