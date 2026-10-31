export const meta = {
  name: 'endgame-build-4',
  description: 'Implement PREREG A25: (A) G13 decontam completeness (mixdev instance-only compare, methods 6-8, TabFact resolver, missing datasets, cosine threshold calib, eval-side stale check, sealed counts-only targets) ; (B) preds_to_gate converter + sealed-side B5 re-confirm + bootstrap text fixes; independent review + fix. Token-lean; no paid calls.',
  phases: [{ title: 'Build' }, { title: 'Review' }, { title: 'Fix' }],
}
const L = '/Users/aryamahadik/Documents/jev/opendecide-data/lean'
const E = `${L}/c_build/endgame`
const PY = '/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python'
const COMMON = `
Binding: ${L}/PREREG_FINAL.md Amendment A25 (last block; read it first) and A15, A23; ${L}/c_spec/C_DATA_SPEC.md section 7 (7.1 targets, 7.2 methods 1-8) and section 10 only; ${E}/RUNBOOK.md section B; the endgame-build-3 review issues are summarised in A25.
NO paid Modal calls, no VM start, no git commits, never edit lean/*.py (pinned), never write an OWNER-WAIVER line. Free downloads of public datasets are allowed (HF hub / GitHub), within ~2 GB, into ~/.cache.
NEVER open (as a reader): data/ohs3*, data/*ohs3*, data/ohs3_parts/, lean/ohs3/, bench/longbench_v2/, c_spec/sealed_brief/, lean/sealed_nd/ data, preds_ohs*/, any *jev* content, ~/.claude/projects/**, /private/tmp/claude-501/**. Programs may READ sealed/held-out files only where A25 (d) says, emitting counts and unit ids only; never print or log their text.
TOKEN-LEAN: one blocking wait <= 140 s per check; <= 40 output lines; no re-reading; no tool call > 150 s; background long jobs (nice -n 10, <= 2 workers; the Mac must stay light); continue partial work on restart. Python ${PY}.`
const A = `${COMMON}
TASK A (decontam, files: ${L}/c_build/decontam_g13.py, decontam_g13_batch.py + tests): implement A25 (c), (d), (e) exactly: mixdev compared on instance content only (state, options, group_id, structure hash of state+options); methods 6 (structure hash vs mixdev and sealed part P via the sealed-side program interface), 7 (sealed-domain keyword block-list), 8 (literal/template check: OPI strategy strings from build_opi.py, jagged's injected line, dev/eval instruction templates as substrings); TabFact '#'-CSV resolver giving the same header+cell-set hash; download the missing HF datasets (big_patent, schema_guided_dstc8) to the cache; run the pre-registered cosine calibration + a 100-pair hand check and write g13_cosine_threshold.json; eval-side stale check (re-hash eval inputs too); OHS-3/LongBench counts-only via a sealed-side program (counts + unit ids only). Then re-run G13 for F3, F6, F9 (counts only) and report per-family hits/drops by target and method.`
const B = `${COMMON}
TASK B (scorer side): (1) write ${E}/preds_to_gate.py + tests per A25 (a): {id, model, probs} -> {id, choice} (argmax under the 6.0 readout rule, fixed tie order) or {id, p_yes}; prove it reproduces C1's dev-side readout accuracy exactly on C1's dev reads (c_build/preread/preread_c1, never sealed preds); (2) as the sealed agent (read the scorer CODE ${L}/sealed_nd/score_nd.py only; synthetic inputs only, never the real suite), re-run the synthetic confirm with converted files under ${E}/sealed_confirm/, check whether a refused look writes a looks line, and record via score_nd_cli.py confirm; (3) update score_nd_cli.py, SCORE_ND_CLI.json and gate_c.py text/checks to A25 (b) (sealed CIs = frozen scorer 2,000/seed 7, reported; dev CIs 10,000/seed 0), and put the converter into the E3/S1 look commands in RUNBOOK. Run all endgame tests.`
phase('Build')
const res = await parallel([() => agent(A, { label: 'build:decontam', phase: 'Build' }), () => agent(B, { label: 'build:scorer', phase: 'Build' })])
phase('Review')
const R = { type: 'object', properties: { verdict: { type: 'string', enum: ['READY', 'ISSUES'] }, issues: { type: 'array', items: { type: 'object', properties: { problem: { type: 'string' }, fix: { type: 'string' }, severity: { type: 'string', enum: ['blocker', 'should', 'nit'] } }, required: ['problem', 'fix', 'severity'] } } }, required: ['verdict', 'issues'] }
const rev = await agent(`${COMMON}\n\nRESULTS:\n${String(res[0]).slice(0, 2200)}\n\n${String(res[1]).slice(0, 1800)}\n\nTASK (independent reviewer; default ISSUES if unsure): check A25 implementation line by line (mixdev instance-only scope is not wider than A25 says; methods 6-8 really run and are logged; no sealed text printed; converter exactness; B5 confirm genuine; bootstrap text), run all tests and r1_check.py preflight (Modal stubbed), and list remaining refusals.`, { label: 'review', phase: 'Review', schema: R })
phase('Fix')
let fix = null
const open = rev ? rev.issues.filter(i => i.severity !== 'nit') : []
if (open.length) fix = await agent(`${COMMON}\n\nISSUES:\n${JSON.stringify(open, null, 1).slice(0, 4500)}\n\nTASK: fix each (within A25), re-run tests and preflight (Modal stubbed); report remaining refusals.`, { label: 'fix', phase: 'Fix' })
return { decontam: String(res[0]).slice(0, 1500), scorer: String(res[1]).slice(0, 1200), review: rev, fix: fix ? String(fix).slice(0, 1500) : null }
