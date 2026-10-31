export const meta = {
  name: 'task-file-runner',
  description: 'Run one agent per task file (adjudication / confirmation / reads) for a prefix and index range; model set per call',
  phases: [{ title: 'Run', detail: 'one agent per task file' }],
}
const ids = []
for (let i = args.start; i <= args.end; i++) ids.push(`${args.prefix}-${String(i).padStart(3, '0')}`)
const SCHEMA = { type: 'object', properties: { wrote_answer_file: { type: 'boolean' }, n_answers: { type: 'integer' }, note: { type: 'string', description: 'at most 20 words; problems only' } }, required: ['wrote_answer_file', 'n_answers'] }
log(`${args.tag}: ${ids.length} task files, model ${args.model}`)
phase('Run')
const out = await parallel(ids.map(id => () => {
  const tf = `${args.tasks_dir}/${id}.md`, af = `${args.answers_dir}/${id}.json`
  return agent(
`${args.role}
Your ONLY task file is:
${tf}
Open it with the Read tool and follow its instructions exactly. If it is too large to read in one call, read it in parts with offset/limit until you have seen every line, to the end. Then write your answers with the Write tool to exactly this answer file (the one named at the top of the task file):
${af}
Rules: use ONLY the Read and Write tools (never ToolSearch, Bash, Grep, Glob or any other tool). Open no other file, list no folder, run no command, use no web. Answer every item exactly once, keyed as the task file's answer contract says; before writing, check that your answer count equals the item count. Then return the structured result.`,
    { label: id.slice(-34), phase: 'Run', schema: SCHEMA, model: args.model, effort: args.effort }
  ).then(r => ({ id, ...(r || { wrote_answer_file: false, n_answers: 0, note: 'null' }) }))
}))
return { tag: args.tag, files: ids.length, done: out.filter(r => r.wrote_answer_file).length, failed: out.filter(r => !r.wrote_answer_file).map(r => r.id), notes: out.filter(r => r.note).map(r => `${r.id}: ${r.note}`).slice(0, 30) }
