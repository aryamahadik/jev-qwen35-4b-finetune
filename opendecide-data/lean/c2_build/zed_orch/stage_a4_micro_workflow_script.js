export const meta = {
  name: 'c2-stage-a4-micro',
  description: 'Stage A4 micro-round for the 7 SHORT families: Sonnet prep (self-contained pending reads + small new authoring tasks) -> Haiku -> Sonnet builds G-LEX reads for new pieces -> Haiku -> Sonnet freeze_v2 re-run; READY/SHORT',
  phases: [
    { title: 'Prep', detail: 'Sonnet: self-contained task files for pending reads and new authoring to close shortfalls' },
    { title: 'Haiku1', detail: 'Haiku answers / authors' },
    { title: 'Reads', detail: 'Sonnet: lint new pieces, write G-LEX/G3-H read tasks' },
    { title: 'Haiku2', detail: 'Haiku reads' },
    { title: 'Freeze', detail: 'Sonnet: fold + freeze_v2 + READY/SHORT' },
  ],
}
const C2 = '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build'
const LEAN = '/Users/aryamahadik/Documents/jev/opendecide-data/lean'
const FAMS = ['T28', 'T27', 'T26', 'T01', 'T06', 'T07', 'T19']
const famDir = id => (['T36', 'T19', 'T21', 'T20'].includes(id) ? `${C2}/transfer/${id}` : `${C2}/families/${id}`)
const RULES = `Binding: ${LEAN}/teach1/C2_DATA_SPEC.md, PREREG A37/A38, ${C2}/README.md, the family's G0 spec, ${C2}/STAGE_A3_REPORT.json (this family's exact shortfalls). Python /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python. NEVER open any path containing "ohs", sealed_nd data, c_spec/sealed_brief, c_build/preread, bench/external_quarantine, bench/longbench_v2, any "jev" file, ~/.claude/projects/**, /private/tmp/claude-501/**. No paid compute, no git commits; never edit pinned lean/*.py or existing c_build files outside this family's folder; never set or edit a label or a read's answer; never loosen a gate or lower a G0 target. If a script error persists after 2 attempts, stop and report it.`
const TASKS = { type: 'object', properties: { tasks: { type: 'array', items: { type: 'object', properties: { file: { type: 'string' }, answer_file: { type: 'string' } }, required: ['file', 'answer_file'] } }, note: { type: 'string' } }, required: ['tasks'] }
const READ = { type: 'object', properties: { answers: { type: 'array', items: { type: 'object', properties: { qid: { type: 'string' } }, required: ['qid'] } }, files_opened: { type: 'array', items: { type: 'string' } } }, required: ['answers', 'files_opened'] }
const OUT = { type: 'object', properties: { status: { type: 'string' }, ready: { type: 'boolean' }, shortfalls: { type: 'array', items: { type: 'string' } }, issues: { type: 'array', items: { type: 'string' } } }, required: ['status', 'ready', 'shortfalls', 'issues'] }
const haiku = (t, lbl, ph) => agent(`Use the Read tool on exactly ${t.file} (if truncated, read the rest of the SAME file with offset/limit). It contains complete instructions and an exact answer contract. Follow them exactly for every item. Do not open any other file, run commands or use the web. Write your answer with the Write tool to exactly ${t.answer_file} in EXACTLY the contract's JSON shape, and also return the entries in the structured output (answers: one entry per item with its qid plus the contract's fields; for authoring tasks use the item ids given in the task as qid). files_opened: plain paths only.`, { label: lbl, phase: ph, schema: READ, model: 'haiku' }).then(x => ({ ...t, ok: !!(x && x.files_opened.every(f => f.startsWith(t.file) || f.startsWith(t.answer_file))) }))
const ok = (id, ts) => (ts || []).filter(t => t.file.startsWith(famDir(id) + '/haiku/') && t.answer_file.startsWith(famDir(id) + '/haiku/'))

const res = await pipeline(FAMS,
  id => agent(`${RULES}
FAMILY ${id} (folder ${famDir(id)}). Using STAGE_A3_REPORT.json's shortfalls for ${id}: write SELF-CONTAINED task files under ${famDir(id)}/haiku/redo3/ (each with the full prompt text, the exact answer contract with a literal JSON example, the items, and the exact answer path under ${famDir(id)}/haiku/redo3/answers/): (a) every pending G-LEX/G3-H read that already exists without answers (re-wrap its chunk with the family's unchanged prompt inline; keep qids); (b) small NEW authoring tasks for every remaining piece shortfall (ask for ~50% more than the gap, same briefs as before, so lint/G-LEX losses still close it). At most 12 tasks. Return tasks.`, { label: `prep:${id}`, phase: 'Prep', schema: TASKS, model: 'sonnet' }),
  async (p, id) => { const r = await parallel(ok(id, p && p.tasks).slice(0, 12).map((t, k) => () => haiku(t, `h1:${id}:${k}`, 'Haiku1'))); return { bad: r.filter(x => x && !x.ok).map(x => x.answer_file) } },
  (st, id) => agent(`${RULES}
FAMILY ${id}: load the redo3 answers in ${famDir(id)}/haiku/redo3/answers/ (ignore audit-failed: ${JSON.stringify(st.bad)}; validate each against its contract). For newly AUTHORED pieces: run the family's lint/dedup, then write self-contained G-LEX (2 independent reads; 3 for precedence/window) or G3-H read tasks for them under ${famDir(id)}/haiku/redo3/reads/ with answer paths under ${famDir(id)}/haiku/redo3/reads/answers/ (each read its own file). If no new reads are needed, return an empty list. At most 8 tasks. Return tasks.`, { label: `reads:${id}`, phase: 'Reads', schema: TASKS, model: 'sonnet' }),
  async (r, id) => { const x = await parallel(ok(id, r && r.tasks).slice(0, 8).map((t, k) => () => haiku(t, `h2:${id}:${k}`, 'Haiku2'))); return { bad: x.filter(y => y && !y.ok).map(y => y.answer_file) } },
  (st, id) => agent(`${RULES}
FAMILY ${id}: fold every validated redo3 answer (authoring + reads; ignore audit-failed: ${JSON.stringify(st.bad)}) into the family's freeze_v2 path (extend freeze_v2.py to read haiku/redo3 if needed, with tests), move the previous pools_v2/ aside as pools_v2_prev/ if the script refuses to overwrite, re-freeze with a MANIFEST, and report READY (every G0 minimum met, G-LEX gate passes) or SHORT with exact remaining shortfalls.`, { label: `freeze:${id}`, phase: 'Freeze', schema: OUT, model: 'sonnet' }),
)
return FAMS.map((id, i) => ({ id, ready: res[i] && res[i].ready, shortfalls: res[i] && res[i].shortfalls }))

