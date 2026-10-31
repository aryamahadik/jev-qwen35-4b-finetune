# OpenDecide CLM-4B implementation plan

**Status:** implementation specification; not evidence of an improvement yet.  
**Purpose:** test whether contrastive state–action scoring improves the shipped
OpenDecide decision model without sacrificing latency, robustness, or
evaluation integrity.

## 1. Decision and scope

The shipped decision baseline is **C1**:

```text
model ID: q35_4b_main500k
adapter: backups/modal_models/q35_4b_main500k/adapter_model.safetensors
working duplicate: c_build/endgame/tmp/m44/q35_4b_main500k/
SHA-256: 507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078
```

`q35_4b_c_r1` is preserved as a historical Round-1 candidate, but it was a
**no-ship** result. Do not use it as the CLM baseline, teacher, or starting
adapter unless a later protocol explicitly changes that decision.

The project is not trying to claim an immediate universal replacement for Jev.
The initial target is narrower and testable:

> Improve C1 on unseen closed-set decision tasks, especially difficult option
> discrimination, while retaining C1's trusted-context security design and
> improving latency on repeated-action workloads.

The design is inspired by Contrastive Language Models: separate state and
action representations, contrastive state–action training, and action-vector
caching. CLM's reported results use a Qwen3-8B encoder and a very large
multi-stage data recipe; those results must not be assumed to transfer to
Qwen3.5-4B or OpenDecide. See the primary reference:
<https://github.com/Contrastive-LM/CLM>.

## 2. Non-negotiable safety and evaluation boundaries

Never read, train on, derive labels from, or use as development feedback:

- OHS-3 or any OHS held-out/sealed content;
- Jev outputs, answers, or benchmark-specific artifacts;
- `bench/external_quarantine/`;
- `sealed_nd/`, `c_spec/sealed_brief/`, `preds_ohs*/`, or other protected
  evaluation data;
- hidden final tests or their prompt/answer distributions.

Do not replace C1, launch a paid cloud job, run a full LoRA fine-tune, or
change the current training/evaluation configuration in Stage A. Those need
an explicit user decision after the relevant gate passes.

All generated or downloaded training data must have:

1. a source and licence record;
2. a stable row ID and source/family group ID;
3. a construction recipe and hash manifest;
4. train/development split assignment before training;
5. overlap/decontamination checks against protected evaluation identifiers and
   available non-content fingerprints.

## 3. Assets to preserve and use

### Current OpenDecide data

Keep these inputs intact:

```text
data/v14_parts/golden_train.jsonl
data/v14_parts/golden_relations.jsonl
data/c_parts/c_train_r1.jsonl
data/c_parts/c_rel_r1.jsonl
data/c_replay_r1_shards/
data/c_crowd_r1_shards/          # current C1-labelled family data
think/data/clean_b1b/
```

These are the starting pool; do not rebuild the first CLM dataset from scratch
or ask an LLM to recreate every example.

### External data policy

External public data is permitted only as broad contrastive augmentation after
licence, source, and overlap review. Prefer datasets with explicit choices,
labels, or verifiable outcomes. The first run should not depend on a massive
new download.

Allowed role for external data:

- broad state–action alignment;
- additional lexical/task-family diversity;
- hard-negative source material where licence and task semantics allow it.

Not allowed role:

- replacing OpenDecide's trusted decision data;
- importing answer keys from protected evaluation sets;
- reporting performance on data that entered training.

### Claude/agent role

Claude should write the builders, validators, reports, and tests. It should
not manually author or inspect hundreds of thousands of rows.

Use an LLM only for a small, reviewed hard-case tranche (initially 1,000–3,000
examples): ambiguous decisions, negation, conflicting evidence, and authority
hijack attempts. Deterministic builders and validators handle the remaining
rows.

## 4. Dataset design

### Canonical contrastive row

Each row must follow this logical schema (JSONL is suitable):

```json
{
  "id": "stable-row-id",
  "source_id": "licensed-source-or-existing-c1-source",
  "family": "decision-family",
  "split": "train|dev",
  "state": "trusted state/situation text only",
  "actions": [
    {"action_id": "approve", "text": "Approve the eligible refund."},
    {"action_id": "deny", "text": "Deny the refund."}
  ],
  "gold_action_id": "approve",
  "hard_negative_action_ids": ["deny"],
  "construction": "original|option-swap|logical-negation|counterfactual|llm-reviewed",
  "licence": "recorded licence",
  "risk_flags": ["negation"]
}
```

Critical rules:

- `state` must never contain an answer letter, option position, or leaked gold
  label.
- `action_id` is a stable semantic identifier, not `A`/`B`/`C`.
- action text is encoded independently of the state and should not include an
  untrusted instruction.
- option position is assigned only at presentation/evaluation time.
- group related transformations by the same `source_id`/family in one split to
  prevent leakage.

### Initial size

Start with a cheap, diagnostic dataset rather than a huge new corpus:

| Component | Initial target | Construction |
|---|---:|---|
| Existing clean C1 rows | 100k–200k | deterministic conversion |
| Existing wrong options / controlled variants | 200k–500k comparisons | deterministic |
| Fresh hard negatives | 25k–75k | template + validator |
| LLM-reviewed hard cases | 1k–3k | small audited tranche |

Scale toward 500k–1M positive state/action examples only if Stage A shows an
independent improvement. Two to four hard negatives per positive are enough
for the first serious test.

### Hard-negative builder priority

Build deterministic transformations first:

1. existing incorrect options from the same item;
2. option-order reversals and semantic-ID preservation;
3. controlled negation pairs;
4. evidence removal or conflicting-evidence counterfactuals;
5. near-neighbour actions from the same decision family;
6. prompt-injection/adversarial text held in the untrusted field, with the
   same correct trusted decision.

The builder must reject a row if it changes the gold decision without a new
verified label.

## 5. Stage A: frozen-C1 contrastive probe

### Objective

Answer one question before any backbone/LoRA training:

> Does a lightweight contrastive head on frozen C1 representations provide
> independent predictive signal on unseen task families?

### Representation extraction

Load frozen Qwen3.5-4B + the shipped C1 adapter. Extract a deterministic
pooled hidden representation for each separately rendered state and action.

Use an explicit, versioned pooling choice, initially:

```text
last non-padding hidden state from the final layer
```

Record model revision, adapter SHA-256, tokenizer revision, prompt template,
sequence truncation policy, dtype, and pooling location in every artifact.

Do not encode an entire multiple-choice prompt as the action. Encode each
semantic action separately. This is what permits action embedding reuse.

### Head architecture

Start small and fixed:

```text
state head:  hidden_size -> 1024 -> projection_dim
action head: hidden_size -> 1024 -> projection_dim
projection_dim: test 256 and 512 only
normalization: L2 normalize final vectors
score: dot product / learned temperature
```

Train only the heads and temperature in Stage A. No C1 adapter, backbone, or
tokenizer update is allowed in this stage.

### Loss

Use bidirectional in-batch InfoNCE. Add explicit hard-negative scoring only
after the basic path and validators work:

```text
L_stage_a = L_bidirectional_infonce + lambda_hard * L_hard_negative
```

Tune at most a small declared grid for learning rate, temperature, projection
dimension, and hard-negative weight. Do not search indefinitely.

## 6. Baselines and fusion

Every development evaluation must score the identical rows in these modes:

1. **C1 direct:** current original/reversed option-order readout.
2. **Contrastive only:** state/action dot-product softmax.
3. **Fixed fusion:** a predeclared weighted combination of normalized C1 and
   contrastive scores.
4. **Learned fusion:** logistic/linear calibrator trained only on a separate
   development-calibration split, then evaluated on an unseen family split.

Do not use the test-family labels to choose fusion weights.

The contrastive pathway is valuable only if it fixes a material set of C1
errors rather than reproducing them.

## 7. Required validation suite

Run all checks before interpreting a gain:

| Category | Required evidence |
|---|---|
| Provenance | manifest, licence, row/source hashes |
| Split integrity | source/family-level train/dev separation |
| Decontamination | protected-set identifier/fingerprint checks |
| Label validity | deterministic validator or audited receipt |
| Option invariance | original/reversed order agreement |
| Logical consistency | complement/equivalence/negation suite |
| Calibration | Brier/ECE and confidence distribution |
| Security | fresh authority-hijack/prompt-injection tests |
| Latency | warm and cold p50/p95, identical hardware/settings |

Report paired deltas, bootstrap confidence intervals, macro and micro
accuracy, and per-family deltas. Never report only the best aggregate number.

## 8. Stage-A promotion gate

Do not start hard-negative expansion or joint training unless all are true on
the preregistered unseen-family development set:

1. fused or contrastive-only macro accuracy improves over C1 by at least
   **+1.0 percentage point**;
2. the paired 95% confidence interval lower bound is above zero;
3. option-order and complement/negation checks do not regress materially;
4. fresh injection/hijack checks do not regress;
5. fast-path latency is within **10%** of C1 for the same fixed short-input
   evaluation, or the cached repeated-action measurement shows a compensating
   improvement;
6. an equal-compute ordinary fine-tune control does not explain the gain.

If the gate fails, retain C1 and stop CLM work. Do not rescue a failed result
with an unrestricted new fine-tune.

## 9. Stage B: targeted hard-negative expansion

Only after Stage A passes:

- grow the data mixture using the hard-negative builder;
- concentrate on C1 error clusters, not random volume;
- create a separate fresh development family after every major builder change;
- keep broad clean replay in the mixture to preserve ordinary decisions;
- rerun all Stage-A baselines and guards.

Suggested mixture for the first expansion:

```text
60% clean existing C1 examples
25% deterministic hard negatives / counterfactuals
10% fresh public licensed augmentation
 5% LLM-reviewed difficult cases
```

This is a starting hypothesis, not a fact. Change it only through a recorded
ablation.

## 10. Stage C: selective refinement

Do not equate a second forward pass with reasoning. It must demonstrate error
correction.

Train a small router only after the contrastive head passes:

```text
router inputs:
  - C1 top-two margin
  - contrastive top-two margin
  - C1/contrastive agreement or disagreement
  - input length and action-set size
  - validated structural risk features (negation, conflict, untrusted text)

router outputs:
  FAST or REFINE
```

The refinement budget must be capped. Evaluate quality, p50, p95, cost, and
route rate together. A router that refines most traffic has failed the latency
objective.

## 11. Stage D: joint fine-tuning (optional)

Only after Stages A–C demonstrate a stable benefit may a new adapter be
considered. It requires a new protocol, budget, checkpoint safety rules, and
independent evaluation plan.

Candidate joint objective:

```text
L = L_decision
  + lambda_contrastive * L_contrastive
  + lambda_consistency * L_consistency
  + lambda_distill * L_c1_preservation
```

Requirements:

- initialize from the shipped C1 adapter;
- conservative learning rate and full C1 replay;
- checkpoint safety reads at declared fractions;
- an ordinary same-compute C1 fine-tune control;
- no OHS-3 use until model selection is frozen.

## 12. Latency plan

The relevant product claim is not a generic “9x faster” statement. Measure
three separate cases:

1. **Short, one-off decision:** full state and actions, no cache.
2. **Repeated action set:** cache actions, embed new state only.
3. **Selective refinement mixture:** fast and refined requests in their real
   measured proportions.

For each, record warm and cold p50/p95, tokens, batch size, hardware, model
revision, action count, state length, and cache hit rate. A meaningful win
must improve C1's tail latency as well as its median. Do not compare unlike
hardware, context sizes, or batch settings to Jev.

The 50–70 ms target is an engineering hypothesis for short, eligible H100
requests. It is not a promise for long or one-off prompts.

## 13. Expected outcomes and stop rules

Expected first experiment outcome:

```text
overall unseen accuracy: C1 +0 to +2 percentage points
targeted negation/conflict slice: C1 +2 to +4 points if hard negatives work
security: no regression permitted
```

A +5-point general OHS-3 improvement or immediate universal Jev parity is not
a justified expectation from a small head experiment. The plausible initial
competitive position is lower p50 latency on repeated closed-set actions,
stronger trusted-context resistance, and a measurable accuracy gain in target
decision workflows.

Stop the project iteration if:

- the Stage-A gate fails;
- data provenance or contamination cannot be established;
- security regresses;
- latency gains depend only on incomparable serving conditions;
- the same-compute ordinary control matches the claimed CLM improvement.

## 14. Deliverables, in order

1. `clm4b/DATA_CARD.md` — sources, licences, exclusions, row counts, hashes.
2. `clm4b/build_pairs.py` — deterministic state/action and hard-negative
   builder with tests.
3. `clm4b/validate_pairs.py` — schema, duplicate, split, and leakage checks.
4. `clm4b/extract_embeddings.py` — frozen-C1 extraction, provenance sidecar.
5. `clm4b/train_heads.py` — Stage-A only.
6. `clm4b/evaluate.py` — all baselines, paired statistics, security/consistency
   calls, and latency receipts.
7. `clm4b/STAGE_A_REPORT.md` — pass/fail decision against the promotion gate.

Do not create later-stage code, paid jobs, or a new LoRA until Deliverables
1–7 have been completed and Stage A has formally passed.

## 15. Claude execution instructions

Work in small, reviewable changes. For each deliverable:

1. inspect current repository instructions and relevant existing builders;
2. write or modify only the required files;
3. add tests before running data transforms;
4. run the validation suite on a tiny synthetic fixture first;
5. report exact files changed, data read, row counts, hashes, and failures;
6. stop at the gate instead of silently broadening scope.

Never access protected evaluations, personal chats, credentials, or unrelated
projects. Never claim a latency, accuracy, safety, or Jev-comparison result
without a saved, reproducible measurement receipt.
