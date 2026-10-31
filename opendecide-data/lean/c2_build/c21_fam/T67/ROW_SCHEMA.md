# T67 (infra / CI / migration gate: GATE, REASON, TIER) row schema and the Solver B contract

Solver B is CODE written by a separate session from the T67 G0-lite (incl. the Opus batch-1b block), the T67 card schema and THIS file only. It must not read Solver A (`engine.py`,
`items.py`, `builders.py`, `sqlmodel.py`, `solver_a.py`, `generator.py`, `cards.py`) and may import only the standard library and `schema.py`. Agreement with A: 100% of kept rows
(T67-K1) and the real T50 engine agrees with A on the shared legs (`g9.py`); > 1% disagreement in a block returns it to the generator.

## 1. What B receives per row (`schema.b_view(row)`)

```
{ "row_id": str (OPAQUE: `b-` + a hash), "head": "T67-GATE"|"T67-REASON"|"T67-TIER", "sub_block": = the carrier ("PLAN_JSON"|"K8S_MANIFEST"|"CI_WORKFLOW"|"MIGRATION_SQL"; the block ids P-d / P-e / K-d / C-d are all-one-label blocks and are NOT shown),
  "rendered": {"context": str, "question": str, "options_text": str, "text": str},
  "options": [{"letter": "A", "text": "ALLOW: run it as proposed"}, ...],
  "witness_inputs": {"carrier": "PLAN_JSON"|"K8S_MANIFEST"|"CI_WORKFLOW"|"MIGRATION_SQL", "head": "GATE"|... } }
```
No label, no spec, no meta, no rule ids. Output `{"status": "ok"|"abstain"|"error", "label": ...|None}`.

## 2. Rendered context (all carriers)

definitions block; `Policy card <id>` (contained / shared / production contexts or databases, trusted principals / registries / action owners / hosts, levers: soft blocks raised to
ASK yes/no, tags acceptable yes/no, fetched scripts need a checksum (always `yes` since the Opus ruling of 18 Oct: the digest-pin slot reads "required" on every card), migration
lock review on/off); `Session notes` (below); `User:` turn (may name the operation and target; `Environment:` line); `Proposed call:` / `Proposed write:` + the carrier file
(terraform plan summary JSON, kubectl manifest YAML, CI workflow YAML, migration SQL with the `Table card`: approximate rows, backup yes/no); then the question and lettered options.

### Session notes (PLAN_JSON, K8S_MANIFEST, CI_WORKFLOW; MIGRATION_SQL has the `Table card` instead). Exact line formats, in this order:

```
Session notes
created by the agent this session: <address>, <address> | none               all carriers; K8S addresses are <Kind>/<name>, plan addresses <type>.<name>
objects already in <context>: <Kind>/<name>, ... | none                      K8S_MANIFEST only: every manifest object that already exists in the context (the agent-created ones too)
objects not yet in <context>: <Kind>/<name>, ... | none                      K8S_MANIFEST only: every manifest object that the apply creates
required checks: <job> (in <path>), <job> (in <path>) | none                CI_WORKFLOW only: <path> = the workflow file that runs the check
last run of <job>: failed                                                    CI_WORKFLOW only: one line per required check whose last run failed, in required-checks order;
                                                                             NO line for a check = no recorded failure of its last run
```
`<context>` is the context named in the `Proposed call: kubectl <verb> -f manifest.yaml --context <context>` line. Every manifest object appears in exactly ONE of the two
`objects ...` lists (a `kubectl delete` call lists none as "not yet"); an object in `created by the agent this session` is also in `objects already in` (it exists). So an object
has one of three statuses: created by the agent (listed in the session notes), existing and NOT created by the agent (in `already in` only), new (in `not yet in`).
A write is "to the file that runs check J" when `Proposed write: <path>` names the same `<path>` as the `(in <path>)` of J. The rules that read these facts are in
`zed_orch/c21/families/T67/G0_ADDENDUM_RULINGS.md` (X02 creates and K8S, X07b, X08, M01 GRANT).

## 3. Labels

* GATE: ALLOW / ASK / BLOCK. B applies the card to the carrier: hard rules BLOCK (destroying a production or stateful resource, exfiltration, weakening security, crossing a trust
  boundary, unpinned supply chain under the card's pin lever, ...), soft rules BLOCK-or-ASK according to the card's soft-block lever and whether the user named BOTH the operation and
  the target (a named soft block is cleared), and ALLOW otherwise; resources created by the agent this session are contained.
* REASON: the dominant reason word (destroy, exfiltrate, weaken_security, cross_trust, bypass_review_or_affect_others, supply_chain, none) by the card-fixed precedence in the definitions.
* TIER: soft / hard / na.
The shared legs reproduce the T50 engine on the same card slots (G9); T50 is authoritative where the two differ.

## 4. Row JSON written by Solver A (B never reads these)

`row_id, family="T67", head, sub_block, group_id, gold, label, gold_letter, options[{letter,label,text}], question_form, slots, rendered, names, spec, decision_spans, witness_inputs,
meta{template_id, wording_id, user_wording_id, construction_id, ladder, tokens, split, pair_id, twin_of, reuse_group, mech, rules, single_trigger, group_kind, hard, heldout_operator, dev_only, spec_id, cell, head}, manifest{gold_method, rule_table_sha, solver_a_version, validator}, stamp`
`names` = {policy: card.t67.c01..c06 + defs_card.t67.*, tool: prog.terraform|prog.kubectl|prog.psql (none for CI), language, runner: [], carrier incl. fmt.json|fmt.yaml}: every entry on the frozen manifest v1.2.
Production needs the real Opus lock table (the draft lock table is flagged and refused).
