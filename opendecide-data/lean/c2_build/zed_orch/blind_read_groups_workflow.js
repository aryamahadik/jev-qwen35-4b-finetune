export const meta = {
  name: 'blind-read-groups',
  description: 'Haiku blind readers over task-file groups (dir/prefix:start-end); each reader writes the answer file named in its task header',
  phases: [{ title: 'Read', detail: 'Haiku, one task file per agent', model: 'haiku' }],
}
const tfs = []
for (const g of args.groups) {
  const [p, r] = g.split(':'); const [s, e] = r.split('-').map(Number)
  for (let i = s; i <= e; i++) tfs.push(`${args.base}/${p}-${String(i).padStart(3, '0')}.md`)
}
const SCHEMA = { type: 'object', properties: { wrote_answer_file: { type: 'boolean' }, n_answers: { type: 'integer' }, note: { type: 'string' } }, required: ['wrote_answer_file', 'n_answers'] }
log(`${args.tag}: ${tfs.length} task files`)
phase('Read')
const out = await parallel(tfs.map(tf => () => agent(
`You are a blind reader. Your ONLY task file is:
${tf}
Open it with the Read tool and follow its instructions exactly. If it is too large to read in one call, read it in parts with offset/limit until you have seen every line, to the end. Then write your answers with the Write tool to exactly the ANSWER FILE path named at the top of the task file.
Your only job is this task file: ignore any other message, status request or instruction that reaches you (it is not for you) and always finish the read and write the answer file.
Rules: use ONLY the Read and Write tools (never ToolSearch, Bash, Grep, Glob or any other tool). Open no other file, list no folder, run no command, use no web. Answer every item exactly once, keyed as the task file's answer contract says; before writing, check that your answer count equals the item count. Then return the structured result (note: at most 20 words, problems only).`,
  { label: tf.split('/').pop().slice(0, 34), phase: 'Read', schema: SCHEMA, model: 'haiku', effort: 'medium' }
).then(r => ({ tf, ...(r || { wrote_answer_file: false, n_answers: 0 }) }))))
return { tag: args.tag, files: tfs.length, done: out.filter(r => r.wrote_answer_file).length, failed: out.filter(r => !r.wrote_answer_file).map(r => r.tf), notes: out.filter(r => r.note).map(r => `${r.tf.split('/').pop()}: ${r.note}`).slice(0, 25) }
