export const meta = {
  name: 'endgame-build-3',
  description: 'Close the remaining round-1 preflight blockers: G13 counts-only decontam tool, A23 preflight alignment (FAM-1 report-only), sealed-side score_nd CLI confirm (no real sealed score), r1_chain/snap_monitor hardening; independent review + fix. Token-lean; no paid Modal.',
  phases: [{ title: 'Build' }, { title: 'Review' }, { title: 'Fix' }],
}
const L = '/Users/aryamahadik/Documents/jev/opendecide-data/lean'
const E = `${L}/c_build/endgame`
const PY = '/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python'
const COMMON = `
Binding: ${E}/RUNBOOK.md (blocker list), ${E}/r1_check.py, ${L}/PREREG_FINAL.md Amendment A23 (last block) + A15 + spec 7 decontamination in ${L}/c_spec/C_DATA_SPEC.md section 7 (read only that section). NO paid Modal calls, no VM start, no git commits, never edit lean/*.py (pinned), never write an OWNER-WAIVER line.
NEVER open: data/ohs3*, data/*ohs3*, data/ohs3_parts/, lean/ohs3/, bench/longbench_v2/, c_spec/sealed_brief/, preds_ohs*/ contents, any *jev* content, ~/.claude/projects/**, /private/tmp/claude-501/**. lean/sealed_nd/ DATA files are never opened by the builder; see the sealed task for the one exception.
TOKEN-LEAN: one blocking wait <= 140 s per check; <= 40 output lines; no re-reading; no tool call > 150 s; background long jobs; continue partial work on restart. Python ${PY}.`
const B1 = `${COMMON}
TASK (builder): (1) write ${L}/c_build/decontam_g13.py (+ tests) implementing spec 7 counts-only decontamination exactly (7.1 targets, 7.2 methods; any hit drops the whole training unit; output only counts and unit ids, never text), with CLI modes per family and final_mix_r1 as RUNBOOK expects, and wire it into r1_check.py preflight / autopilot_check.py; run it on F3 and F6 now (counts only) and record logs. (2) Implement A23 in r1_check.py: FAM-1 record must exist and be reported (controls status, flags, wall time); it no longer requires controls_pass or a waiver. (3) Harden r1_chain.sh: after starting snap_monitor, verify it is alive and re-check every segment; if it is dead, stop the chain (no new segment) and log; give snap_monitor a retry cap with escalation (after 3 failed reads of a snapshot: stop the round-1 app and log), and fix the refparity substring nit and add set -o pipefail to SCORE_ND_CLI commands. Run all endgame tests and r1_check.py preflight with Modal calls stubbed; list what still refuses.`
const B2 = `${COMMON}
TASK (sealed-side confirm, the ONE exception): you act as the sealed agent. You may READ the scorer CODE under ${L}/sealed_nd/qc/ (python files only) but never any sealed data file, prediction file or manifest content beyond what the code needs to run on SYNTHETIC inputs. Build a tiny synthetic suite + synthetic predictions in a temp dir under ${E}/sealed_confirm/ that mimic the format, run the scorer on them (never on the real suite), and confirm: the accepted prediction format ({id, model, probs} or as the code says), the printed fields (n, cand, ref, diff, paired bootstrap LB/UB, resamples, seed). Record via ${PY} ${E}/score_nd_cli.py confirm --from <json> (read its usage first). Return the confirmed fields.`
phase('Build')
const res = await parallel([() => agent(B1, { label: 'build', phase: 'Build' }), () => agent(B2, { label: 'sealed-confirm', phase: 'Build' })])
phase('Review')
const R = { type: 'object', properties: { verdict: { type: 'string', enum: ['READY', 'ISSUES'] }, issues: { type: 'array', items: { type: 'object', properties: { problem: { type: 'string' }, fix: { type: 'string' }, severity: { type: 'string', enum: ['blocker', 'should', 'nit'] } }, required: ['problem', 'fix', 'severity'] } } }, required: ['verdict', 'issues'] }
const rev = await agent(`${COMMON}\n\nRESULTS:\n${String(res[0]).slice(0, 2200)}\n\n${String(res[1]).slice(0, 1500)}\n\nTASK (independent reviewer; default ISSUES if unsure): check decontam_g13.py against spec 7 line by line (targets, methods, unit drops, counts-only), the A23 change in r1_check.py (no other preflight item loosened), the r1_chain/snap_monitor hardening, and that the sealed confirm never touched real sealed data. Run tests and r1_check.py preflight (Modal stubbed) and list remaining refusals.`, { label: 'review', phase: 'Review', schema: R })
phase('Fix')
let fix = null
const open = rev ? rev.issues.filter(i => i.severity !== 'nit') : []
if (open.length) fix = await agent(`${COMMON}\n\nISSUES:\n${JSON.stringify(open, null, 1).slice(0, 4500)}\n\nTASK: fix each; re-run tests and preflight (Modal stubbed); report remaining refusals.`, { label: 'fix', phase: 'Fix' })
return { build: String(res[0]).slice(0, 1500), confirm: String(res[1]).slice(0, 1000), review: rev, fix: fix ? String(fix).slice(0, 1500) : null }
