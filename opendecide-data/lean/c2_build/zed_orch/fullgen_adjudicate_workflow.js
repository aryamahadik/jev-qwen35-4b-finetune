export const meta = {
  name: 'fullgen-adjudicate',
  description: 'Sonnet first-pass G5-H adjudication (A43 d) of full-generation families; one adjudication file per family',
  phases: [{ title: 'Adjudicate', detail: 'Sonnet, flag only', model: 'sonnet' }],
}
const B = '/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts'
const SCHEMA = { type: 'object', properties: { wrote_answer_file: { type: 'boolean' }, n_answers: { type: 'integer' } }, required: ['wrote_answer_file', 'n_answers'] }
phase('Adjudicate')
return await parallel(args.fams.map(F => () => agent(
`You are the first-pass G5-H adjudicator (Sonnet; PREREG A43 d). Your ONLY task file is:
${B}/${F}/qc/adjudication/tasks/${F}-ADJ-000.md
Read it fully with the Read tool and follow its instructions exactly. For each item judge from the material, the card rules and the program gold whether the gold is right; flag only, never propose a new label: wrong_gold only when the gold clearly contradicts the rules; ambiguous only when the rules do not settle it. Write the answer file named at the top of the task file with the Write tool. Use only the Read and Write tools; open no other file. Check your answer count equals the item count. Then return the structured result.`,
  { label: `${F}-ADJ`, phase: 'Adjudicate', schema: SCHEMA, model: 'sonnet', effort: 'high' }).then(r => ({ F, ...(r || { wrote_answer_file: false, n_answers: 0 }) }))))
