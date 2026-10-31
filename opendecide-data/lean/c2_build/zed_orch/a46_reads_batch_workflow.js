export const meta = {
  name: 'a46-replay-reads-batch',
  description: 'A46 replay noise screen: Haiku blind readers over a batch of task-file ranges (one task file per agent)',
  phases: [{ title: 'Read', detail: 'Haiku blind readers, one task file each', model: 'haiku' }],
}
const BASE = '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/replay_screen/reads'
const ids = []
for (const g of args.groups) {
  const [b, r] = g.split(':'); const [s, e] = r.split('-').map(Number)
  for (let i = s; i <= e; i++) ids.push(`${b}-${String(i).padStart(3, '0')}`)
}
const SCHEMA = { type: 'object', properties: { wrote_answer_file: { type: 'boolean' }, n_answers: { type: 'integer' }, note: { type: 'string', description: 'at most 20 words; problems only' } }, required: ['wrote_answer_file', 'n_answers'] }
log(`${args.tag}: ${ids.length} task files`)
phase('Read')
const out = await parallel(ids.map(id => () => {
  const tf = `${BASE}/tasks/${id}.md`, af = `${BASE}/answers/${id}.json`
  return agent(
`You are a blind reader. Your ONLY task file is:
${tf}
Open it with the Read tool and follow its instructions exactly. If it is too large to read in one call, read it in parts with offset/limit until you have seen every line, to the end of the file. When an item has definitions, follow them exactly, even if they differ from everyday meanings. Then write your answers with the Write tool to exactly this answer file (the one named at the top of the task file):
${af}
Rules: use ONLY the Read and Write tools (they are already loaded; never call ToolSearch, Bash, Grep, Glob, Edit or any other tool, not even to count items). Open no other file, list no folder, run no command, use no web. Answer every item exactly once, keyed by its qid, as the task file's answer contract says; before writing, check that your answer count equals the item count. Then return the structured result.`,
    { label: id.slice(0, 30), phase: 'Read', schema: SCHEMA, model: 'haiku', effort: 'medium' }
  ).then(r => ({ id, ...(r || { wrote_answer_file: false, n_answers: 0, note: 'null' }) }))
}))
return { tag: args.tag, files: ids.length, done: out.filter(r => r.wrote_answer_file).length, failed: out.filter(r => !r.wrote_answer_file).map(r => r.id), notes: out.filter(r => r.note).map(r => `${r.id}: ${r.note}`).slice(0, 40) }
