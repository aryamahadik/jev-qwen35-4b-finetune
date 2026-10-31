export const meta = {
  name: 'c-lanes-v3',
  description: 'PREREG A21.1: one token-lean lane per family (max 6 at once) for F1-F13 + COMMIT: status -> gen -> G2 (solver B 100%) -> independent check -> repair + fresh recheck until pass or proven infeasible. Same roles/gates/G0 specs; verbatim BUILDER_BRIEF; blocking waits; handoff notes keep contexts small; heavy jobs via rrun.',
  phases: [{ title: 'Status' }, { title: 'Generate' }, { title: 'G2' }, { title: 'Check' }, { title: 'Repair' }],
}
const L = '/Users/aryamahadik/Documents/jev/opendecide-data/lean'
const PY = '/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python'
const RULES = `
You are a C builder for OpenDecide round 1 in workflow c-lanes-v3; you own family <FAM> (its LANE_LOCK.md names c-lanes-v3, i.e. you).
BINDING TEXT: ${L}/c_spec/BUILDER_BRIEF.md (verbatim extracts of PREREG A15, A16, A16.1, A16.2, A19, A20, A21 and C_DATA_SPEC v4 sections 2.1, 2.2, 2.4, 6, 8, 10; read it instead of the full PREREG/spec/recipe, and open a source section only if the brief lacks something you need), your family's frozen ${L}/c_src/<FAM>/G0_SPEC.md (check its sha256 against G0_FROZEN.json; read the sections you need with grep/sed rather than all of it, unless you are writing the generator from scratch), ${L}/c_src/<FAM>/qc/QC_REPORT.json, and the notes in ${L}/c_src/<FAM>/tmp/repair/ (LANE_LOCK, MIXER_NOTE, RRUN_NOTE, TRAINER_INCIDENT, INFEASIBLE_*, earlier repair notes) and ${L}/c_src/<FAM>/tmp/HANDOFF_*.md.
ALLOW-LIST: those; ${L}/c_src/** (common tools incl. negcount.py, markers.json, denylist.py, g8_aflite.py; packs; formats-1/formats-2); ${L}/decoder_io.py and ${L}/train_decoder.py (import only; NEVER edit them or anything outside c_src/<FAM>/: they are pinned by sha); ${L}/c_build/rrun.py + RRUN.md; public web downloads (COMMIT only, permissive per spec 4).
NEVER open: c_spec/sealed_brief/, lean/sealed_nd/ (only RUN ${L}/sealed_nd/qc/sealed_check.py), c_spec/RESEARCH_*, REVIEW_*, LICENCE_CHECK_*, ADDENDUM_research.md, lean/ohs3/, data/ohs3*, data/*ohs3*, data/ohs3_parts/, prep89/, preds_ohs*/, bench/**, eval test splits, any Jev output (*jev*), ~/.claude/projects/**, /private/tmp/claude-501/**. Scratch only in c_src/<FAM>/tmp/.
FIX RULES: fix the GENERATOR (matched twins first, then template/sampler changes); never bulk-delete rows to hide a cue, never hand-edit or relabel rows; regenerate; after every regeneration re-run G2 (0 mismatches), G3, G4, G15, G18, sealed_check and refresh out/MANIFEST.json (counts, sha256, relation counts/sha, parents list) and record pool sha256s in qc/QC_REPORT.json. G6 metadata = only what the model sees. Infeasible gate (provably cannot pass for any generator meeting the G0 spec): write the proof with numbers to tmp/repair/INFEASIBLE_<gate>.md; never weaken a gate. G8: if ${L}/c_build/g8v2/A19_ADOPTED exists, judge G8 with ${L}/c_src/common/g8_aflite.py (A19) and also report the old raw share; otherwise run the spec G8 and also the shared tool if present, reporting both.
COMPUTE: run every job expected > 2 min through ${PY} ${L}/c_build/rrun.py --fam <FAM> -- <command> (Modal CPU, the only permitted cloud call; see RRUN.md), started in the background (nohup ... > tmp/<name>.log 2>&1 &). Local jobs: nice -n 10, <= 2 workers. No other Modal/gcloud/ssh/paid calls; no git commits. Disk is tight: COMMIT keeps raw <= 2 GB and deletes raw after extraction.
TOKEN-LEAN RULES (critical; usage is the binding limit): (1) wait for a background job with ONE blocking command per check, e.g. for i in $(seq 1 28); do [ -f DONE_MARKER ] && break; kill -0 PID 2>/dev/null || break; sleep 5; done; tail -n 5 LOG  (about 140 s; never check more often, never use sleep < 60 s between checks); (2) never print more than 40 lines from a command (use tail/head/grep -c/python summaries; never cat data files, long logs or whole JSON reports); (3) do not re-read files you already read; (4) after about 100 tool calls in this agent, write ${L}/c_src/<FAM>/tmp/HANDOFF_<step>.md (<= 60 lines: state, files, done, exact next actions, running jobs with PIDs/logs) and return status CONTINUE; a fresh agent will continue from it.
STALL RULE: the harness restarts an agent with no activity for ~3 minutes, so no single tool call may exceed ~150 s; on start, check HANDOFF notes, running processes (pgrep -fl) and logs, and continue partial work rather than redoing it.
Progress lines to ${L}/c_build/progress_phase2.log prefixed [<FAM>]. Return short structured results; never row texts.`
const ST = { type: 'object', properties: { status: { type: 'string', enum: ['DONE', 'CONTINUE'] }, summary: { type: 'string' } }, required: ['status', 'summary'] }
const STATE = { type: 'object', properties: { outputs_complete: { type: 'boolean' }, g2_current_ok: { type: 'boolean' }, qc_current: { type: 'boolean' }, qc_pass: { type: 'boolean' }, failed_gates: { type: 'array', items: { type: 'string' } }, infeasible: { type: 'array', items: { type: 'string' } }, notes: { type: 'string' } }, required: ['outputs_complete', 'g2_current_ok', 'qc_current', 'qc_pass', 'failed_gates', 'infeasible', 'notes'] }
const G2S = { type: 'object', properties: { status: { type: 'string', enum: ['DONE', 'CONTINUE'] }, rows_checked: { type: 'number' }, mismatches: { type: 'number' }, notes: { type: 'string' } }, required: ['status', 'rows_checked', 'mismatches', 'notes'] }
const QCS = { type: 'object', properties: { status: { type: 'string', enum: ['DONE', 'CONTINUE'] }, pass: { type: 'boolean' }, failed_gates: { type: 'array', items: { type: 'string' } }, infeasible: { type: 'array', items: { type: 'string' } }, details: { type: 'string' } }, required: ['status', 'pass', 'failed_gates', 'infeasible', 'details'] }
const R = f => RULES.split('<FAM>').join(f)
async function step(f, label, phase, task, schema) {
  let r = null
  for (let k = 0; k < 6; k++) {
    const cont = k === 0 ? '' : `\n\nCONTINUATION ${k}: a previous agent for this step handed off; read ${L}/c_src/${f}/tmp/HANDOFF_${label.split(':')[0]}.md first and continue from it.`
    r = await agent(`${R(f)}\n\nTASK (${label}): ${task}${cont}\nReturn status DONE when the step is complete, or CONTINUE after writing the handoff note.`, { label: k ? `${label}+${k}` : label, phase, schema })
    if (!r || r.status !== 'CONTINUE') break
  }
  return r
}
const RESOLVED = x => /G8|length|token|median/i.test(String(x))
const blocking = q => (q && q.infeasible ? q.infeasible.filter(x => !RESOLVED(x)) : [])
async function runFamily(f) {
  const n = ['F1', 'F5', 'F6', 'F13', 'COMMIT'].includes(f) ? 600 : 300
  const s = await agent(`${R(f)}\n\nTASK (status, read-only, <= 15 tool calls): report ${f}'s state from files only: do out/candidates_r1.jsonl, out/qc_sample.jsonl, out/mixdev_S5.jsonl and out/MANIFEST.json exist and match (outputs_complete)? Was solver B run on the CURRENT outputs with 0 mismatches (g2_current_ok: compare solverB/mismatch.json and its logs' sha/mtime with the pools)? Does qc/QC_REPORT.json describe the current pools (qc_current) and pass (qc_pass)? List failed gates and any INFEASIBLE_*.md. Note running background jobs (pgrep -fl) and HANDOFF notes. Builds that ran 00:06-00:58 UTC on 6 Oct are invalid (TRAINER_INCIDENT.md).`, { label: `status:${f}`, phase: 'Status', schema: STATE, model: 'haiku' })
  if (!s) return { f, stage: 'status-failed' }
  if (s.qc_pass && s.qc_current && s.g2_current_ok && s.outputs_complete) return { f, pass: true, failed: [], infeasible: [] }
  if (!s.outputs_complete) {
    await step(f, `gen:${f}`, 'Generate', `generator author for ${f}: inspect partial work (gen/, out/, tmp/, HANDOFF, running jobs) and finish; regenerate cleanly where unsure. Implement gen/ per the frozen G0 spec and the brief: samplers (training + S5 held-out), solver A, renderer with packs (>= 30 packs; record domain_pack, persona_seed) and formats (fmt1 render_and_check, formats-2 wordings), >= 3 metamorphic relations, round-trip parser. Produce out/candidates_r1.jsonl (1.5x the family's round-1 rows from spec 2.2, training samplers only), out/qc_sample.jsonl (>= 5,000 rows unless the spec allows fewer), out/mixdev_S5.jsonl (400 S5 items), our row format with full meta incl. meta.format_style. Pass at 100%: G3, G4 (>= 1,000 rows), G15 (check_rows + fmt1 loader_check under random permutation), G18 where ordinal, negcount quotas, real-tokenizer length <= 7,900 with instructions counted twice; sealed_check on all outputs (replace hits). Write out/MANIFEST.json incl. parents.`, ST)
  }
  if (!s.g2_current_ok || !s.outputs_complete) {
    let g2 = await step(f, `g2:${f}`, 'G2', `independent solver B for ${f}: you must NOT read c_src/${f}/gen/ or any solver A code. From the frozen G0 spec and the row format only, write (or reuse if it exists and was written from the spec only) c_src/${f}/solverB/solver_b.py in a DIFFERENT paradigm, re-derive gold for EVERY row of the three outputs, write mismatches (ids, both answers, spec item; no row text) to solverB/mismatch.json.`, G2S)
    for (let k = 1; g2 && g2.mismatches > 0 && k <= 3; k++) {
      await step(f, `fixA:${f}`, 'G2', `G2 repair for ${f} (pass ${k}); last G2: ${JSON.stringify(g2).slice(0, 400)}. Read solverB/mismatch.json, decide from the frozen G0 spec which side is wrong, fix the generator (regenerate the affected outputs, never patch rows) or ONLY the cited spec item in solver B (log the spec line); drop ambiguous templates and log them; re-run G3/G4/G15/G18/sealed_check and refresh the MANIFEST.`, ST)
      g2 = await step(f, `g2:${f}`, 'G2', `independent solver B re-run for ${f} after a generator fix: do not read gen/ or solver A code; run solverB/solver_b.py on EVERY row of the current three outputs and update solverB/mismatch.json.`, G2S)
    }
    if (!g2 || g2.mismatches > 0) return { f, stage: 'G2', g2 }
  }
  let qc = null
  if (!s.qc_current || !s.g2_current_ok) {
    qc = await step(f, `check:${f}`, 'Check', `independent checker for ${f} (you never wrote its generator or solvers): (1) A24: FIRST run the script gates in (2); ONLY if every script gate passes, do the G5 blind read of ${n} rows (seed 5001) from out/candidates_r1.jsonl reading ONLY what the model sees (decoder_io.user_msg, cygnet, schema_branch_mark); flag clearly wrong or genuinely ambiguous golds (flag only; qc/g5.json). (2) QC gates as scripts on the current pools: G6 (5-fold CV grouped by card; each <= chance + 2 pp), G7, G8 (see G8 rule), G10 (all v4 rules), G11, G12, G15, G18. Write qc/QC_REPORT.json with pool sha256s. pass=true only if every gate passes AND the G5 read was done with 0 clearly wrong and ambiguous <= ${Math.floor(n / 100)}; if script gates fail, skip G5 and say 'G5 deferred (A24)'.`, QCS)
  } else {
    qc = { pass: s.qc_pass, failed_gates: s.failed_gates, infeasible: s.infeasible }
  }
  for (let r = 1; qc && !qc.pass && !blocking(qc).length && r <= 4; r++) {
    await step(f, `repair:${f}`, 'Repair', `repair round ${r} for ${f}: read qc/QC_REPORT.json (failing: ${JSON.stringify(qc.failed_gates)}), the repair notes and any HANDOFF; fix every failing gate at the generator level, verify G5 flags against the frozen spec and solver B, regenerate, re-run all label gates (G2 0 mismatches, G3, G4, G15, G18, sealed_check), refresh the MANIFEST, re-run the failing QC gates yourself and update qc/QC_REPORT.json (keep the previous as qc/QC_REPORT_prev.json).`, ST)
    qc = await step(f, `recheck:${f}`, 'Repair', `fresh independent re-check of ${f} after repair round ${r} (you did not write this generator): re-run ALL QC gates G6-G12, G15, G18 on the current out/ (reuse the family's gate scripts only after checking them against spec 8 in the brief; fix and report any script bug) and, ONLY if every script gate passes (A24), a fresh G5 blind read of ${n} rows (seed 710${r}; flag only); otherwise skip G5 and say 'G5 deferred (A24)'. Reuse the family's gate scripts; read a script line by line only the first time this family is rechecked or when it changed (note its sha in qc/GATE_SCRIPTS_CHECKED.json). Write qc/QC_REPORT.json with pool sha256s. pass=true only if every gate passes and G5 has 0 clearly wrong.`, QCS)
  }
  return { f, pass: qc ? qc.pass : null, failed: qc ? qc.failed_gates : null, infeasible: qc ? qc.infeasible : null }
}
const QUEUE = ['F9', 'F10', 'F11', 'F6', 'F1', 'F3', 'F7', 'F8', 'F12', 'F13', 'COMMIT', 'F2', 'F4', 'F5']
const MAXP = 6
let active = 0
const waiters = []
async function slot(fn) {
  while (active >= MAXP) await new Promise(r => waiters.push(r))
  active++
  try { return await fn() } finally { active--; const w = waiters.shift(); if (w) w() }
}
const res = await parallel(QUEUE.map(f => () => slot(() => runFamily(f).then(x => { log(`${f}: ${JSON.stringify(x).slice(0, 240)}`); return x }))))
return res
