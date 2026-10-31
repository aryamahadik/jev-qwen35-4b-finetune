export const meta = {
  name: 'c2-fix-iter1',
  description: 'C2 fix iteration 1 (spec 6.4 step 6): kit-level fixes (abstain gold balance, card length) + gold-bug fixes (Opus), then per-family generator fixes + program-gate re-pilot (Sonnet) for all 22 families; G5-H re-reads deferred to after the weekly reset',
  phases: [
    { title: 'Kit', detail: 'Opus: shared fixes for abstain/none gold share and the 800-token mean; T35 double-negation gold bug' },
    { title: 'Family', detail: 'Sonnet per family: apply its verdict fixes, re-run pilot.py program gates; pilot the 7 not yet piloted' },
  ],
}
const LEAN = '/Users/aryamahadik/Documents/jev/opendecide-data/lean'
const C2 = LEAN + '/c2_build'
const ALL = ['T35', 'T30', 'T24', 'T33', 'T29', 'T31', 'T32', 'T23', 'T15', 'T12', 'T25', 't37b', 'T36', 'T21', 'T20', 'T28', 'T27', 'T26', 'T01', 'T06', 'T07', 'T19']
const famDir = id => (id === 't37b' ? `${C2}/t37b` : (['T36', 'T19', 'T21', 'T20'].includes(id) ? `${C2}/transfer/${id}` : `${C2}/families/${id}`))
const RULES = `Binding: ${LEAN}/teach1/C2_DATA_SPEC.md (3.0, 4, 6.3, 6.4), PREREG A37/A38/A40, ${C2}/README.md, ${C2}/STAGE_B_PILOT_REPORT.json and each family's pilot/PILOT_REPORT.json + PILOT_VERDICT.json. Python /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python. NEVER open any path containing "ohs", sealed_nd data, c_spec/sealed_brief, c_build/preread, bench/external_quarantine, bench/longbench_v2, any "jev" file, ~/.claude/projects/**, /private/tmp/claude-501/** (not even as scratch). No paid compute, no git commits, never edit pinned lean/*.py or c_build files; generator/template fixes only (spec 6.4 step 6), never relabel, never loosen a gate bar or lower a G0 target. Do NOT run Haiku or any model; G5-H re-reads come later. If a script error persists after 2 attempts, stop and report it.`
const OUT = { type: 'object', properties: { status: { type: 'string' }, gates_after: { type: 'string' }, changes: { type: 'array', items: { type: 'string' } }, open: { type: 'array', items: { type: 'string' } } }, required: ['status', 'gates_after', 'changes', 'open'] }

phase('Kit')
const kit = await agent(`${RULES}
TASK (kit level, once, with tests): (1) abstain / "none" / "no line matches" options: across families they are gold far below 1/k, which fails G6 options-only, G7 and G10 longest-option. Add a kit-level, label-blind mechanism (e.g. in c2_kit/distractors.py or a new helper) that lets a family set the abstain-gold share and the option-length balance at sampling time so the gold position, length rank and abstain-gold rate are balanced by construction (never by relabeling). (2) The spec 3.0 family mean of <= 800 tokens fails in 13/15 families (810-1,207, real tokenizer via mixer.token_counts): add kit support for compact cards (shorter rule phrasing, card variants, optional short-card rows within the G0's allowed share) that families can adopt without changing semantics. (3) Fix the T35 yn_double_neg wrong-gold bug (3 confirmed wrong golds) at its root, with a regression test, and check whether the same double-negation wording logic exists in other families' plugins (list them). Run all kit tests. Return what families must call, as precise instructions.`, { label: 'kit', phase: 'Kit', schema: OUT })

phase('Family')
const fams = await parallel(ALL.map(id => () => agent(`${RULES}
KIT CHANGES (adopt them where your verdict needs them):\n${kit ? kit.changes.join('\n') + '\nOPEN: ' + kit.open.join('\n') : 'kit agent failed: fix within the family only'}
FAMILY ${id} (folder ${famDir(id)}). ${['T28', 'T27', 'T26', 'T01', 'T06', 'T07', 'T19'].includes(id) ? 'This family has NOT been piloted yet: first run pilot.py for it as-is (see the README and pilot_loaders.py; add a loader if needed) to get its PILOT_REPORT, then fix what fails.' : 'Apply every generator/template fix in its PILOT_VERDICT.json and PILOT_REPORT.json failures.'} Then re-run pilot.py (program gates only: G2, G3, G4, G-SL, G-LEX, G-TW, G15, G6, G7, G10, overlay, spec 3.0 token mean, determinism under two PYTHONHASHSEEDs) into ${famDir(id)}/pilot_i1/ and regenerate the G5-H/G3-H task files there (do NOT answer them). Report gates_after (one line per gate, pass/fail with the number vs bar) and anything still open.`, { label: `fix:${id}`, phase: 'Family', schema: OUT, model: 'sonnet' })))
return { kit: kit && { status: kit.status, changes: kit.changes, open: kit.open }, families: ALL.map((id, i) => ({ id, status: fams[i] && fams[i].status, gates_after: fams[i] && fams[i].gates_after, open: fams[i] && fams[i].open })) }

