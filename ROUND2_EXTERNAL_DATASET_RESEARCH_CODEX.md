# Round-2 external dataset research for the previously missing families

Date: 7 October 2026 (EDT)

Scope: F1, F2, F6, F8, F10, F12, F13 and COMMIT — the eight families that were missing in the earlier round-1 snapshot. This is an independent research note. It does not amend `PREREG_FINAL.md`, change a mix, download data, or touch any file being edited by another session.

## Bottom line

Do **not** replace the program-built family data wholesale. The repo has progressed beyond the pasted snapshot and already has family work for F1-F13 plus COMMIT. It also already contains strong public or replay sources for most of the former gaps. External data should be a small supplement after the same licence, quality, split, and decontamination gates.

The best new candidates are:

1. **QUITE -> F8 risk and probability** — best new fit; CC BY 4.0 dataset; numeric Bayesian answers are executable/verifiable.
2. **Schema-Guided Dialogue (SGD/SGD-X) -> F12 tool and action selection** — best new tool-use fit; CC BY-SA 4.0; provides API schemas, required/optional parameters, service calls and results.
3. **TabMWP -> F2 arithmetic** — useful non-commercial supplement; CC BY-NC-SA 4.0; 38,431 table-based math problems with gold solutions.
4. **RuleTaker -> F1/F10 auxiliary rule following** — useful but only partial fit; official Apache-2.0 repo and theorem-prover labels. It teaches rule chaining, not the project's exception/precedence semantics.
5. **CLUTRR -> F10 auxiliary definition/relationship following** — non-commercial and useful only after codebook remapping; CC BY-NC 4.0. It is not a drop-in F10 replacement.

No genuinely better new drop-in source was found for F6, F13 or COMMIT. The sources already selected in this repo are stronger and safer for those families.

## Recommended additions

| Priority | Dataset | Family | Ready-made usable part | Licence / restriction | Suggested cap | Fit and caveats |
|---|---|---|---|---|---:|---|
| 1 | [QUITE](https://github.com/boschresearch/quite-emnlp24) | F8 | `train` examples from `evidence-query-pairs` and, if separately audited, the authors' additional silver pairs | Dataset is **CC BY 4.0**; repository code is AGPL-3.0 | 2,000-4,000 | Excellent for conditional/Bayesian probability and probability bins. Numeric answers are included. It does not cover all expected-loss and risk-tier constructs, so retain the program-built F8 rows. Audit silver data separately. |
| 2 | [Schema-Guided Dialogue / SGD-X](https://github.com/google-research-datasets/dstc8-schema-guided-dialogue) | F12 | `train` dialogues and schemas; derive rows from `service_call.method`, parameters, required slots, optional slots and `NONE` intent | **CC BY-SA 4.0**; keep private unless share-alike obligations are handled | 3,000-5,000 | Very strong match to choosing a tool/action and deciding whether required parameters are present. More than 20K annotated conversations across 20 domains. Dialogues used a simulator plus paid crowd-workers; schemas were manually written and SGD-X paraphrases were crowdsourced. Use only train; reserve dev/test. |
| 3 | [TabMWP](https://github.com/lupantech/PromptPG) | F2 | Official training split only; prefer examples whose solutions are deterministically recomputable | **CC BY-NC-SA 4.0** | 1,500-3,000 | 38,431 table-based math word problems with free-text or multiple-choice answers and gold solutions. Good for quantities, percentages and multi-step arithmetic, but weak for dates, amendments, caps/floors and policy exceptions. Non-commercial use is required; share-alike applies. |
| 4 | [RuleTaker](https://github.com/allenai/ruletaker) | F1, auxiliary F10 | Official downloadable theories/assertions or regenerated rows from the official grammar, with labels re-derived using ProbLog | Official repo is **Apache-2.0** | 2,000-4,000 | Program labels and controllable proof depth are valuable. It lacks the project's dated amendments, exception precedence and explicit escalation outcomes. Verify that the downloaded archive itself carries the repo licence before ingesting it; do not infer a data licence from a mirror. |
| 5 | [CLUTRR](https://github.com/facebookresearch/clutrr) | auxiliary F10 | Official generated training tasks, optionally with relation names remapped to per-card arbitrary tokens | **CC BY-NC 4.0** | 1,000-2,000 | Teaches compositional relation following and includes irrelevant/disconnected-fact variants. It becomes F10-like only after a deterministic codebook transform, so it is supplemental rather than ready-to-mix. Keep all original attribution and non-commercial restrictions. |

### Exact transforms to the Jev decision format

- **QUITE:** show the probability premises and evidence in the state; ask for a probability bin, a threshold yes/no decision, or a ranking. Recompute the numeric answer independently before binning. Do not turn the repository's paper test examples into training rows.
- **SGD/SGD-X:** make the available service schema the card, the latest user turn/dialogue state the state, and the gold `service_call.method` the action. Add a `request more information` option when required slots are absent. Split by service/schema as well as dialogue so paraphrases of one schema do not cross train/dev.
- **TabMWP:** keep the table and question; convert only answers whose derivation can be recomputed. Do not train on natural-language solution text if it leaks the answer format or contains unverified reasoning. Filter out problems derived from any local evaluation source.
- **RuleTaker:** use theorem-prover labels, not model-generated rationales. It can supply entailment/contradiction rule chains, but it must not be relabelled as F1 exception precedence unless the theory actually encodes that semantics.
- **CLUTRR:** replace relation names with per-card arbitrary tokens and include the mapping in the card. Keep each story/template family in one split. This is a deterministic derived task, not direct use of the original labels alone.

## What the repo already has for these families

This is why the recommended new-data list is short.

| Family | Existing or already selected sources in this repo | Decision |
|---|---|---|
| F1 policy composition | Program-built F1; replay includes `gd_gen_policy_exceptions` (11,463 rows), `gd_boardgameqa` (9,550) and `gd_conditionalqa` (1,713); public UCI Car/Nursery rule rows are already selected | Add RuleTaker only for diversity; it is not a replacement for F1 |
| F2 rule arithmetic | Program-built F2; replay includes `gd_gen_numeric_dates` (11,531), TAT-QA (6,740), TAT-HQA (4,154); DROP and WikiSQL are already selected | TabMWP is optional breadth, not a missing core source |
| F6 abstention | Program-built F6; SQuAD 2.0, MuSiQue Full and 2WikiMultihopQA are already selected; replay contains 687 ProofWriter rows | No new source needed; spend effort on auditing and balance |
| F8 risk/probability | Program-built F8 and 478 replay `gd_gen2_probability` rows | **QUITE is the clearest useful new addition** |
| F10 invented definitions | Program-built F10 plus real-text codebook rows and logic/rule replay | CLUTRR or RuleTaker can add breadth only after a codebook transform |
| F12 tools/actions | Program-built F12; replay already includes STAR (3,339), SMCalFlow (6,220), MultiWOZ 2.1 system actions (2,703), Taskmaster 1/2/3 and `gd_gen2_tool_selection` | SGD adds schema and missing-parameter diversity, but cap it because this lane is already well covered |
| F13 long documents | Program-built F13; QuALITY and licence-filtered Qasper are already selected | No new drop-in source is better under the current contamination and document-licence rules |
| COMMIT | CommitChronicle (planned 8,000 round-2 rows) and CommitPackFT (4,000) are already selected and licence-checked | No new source needed |

Local evidence: `opendecide-data/lean/c_spec/C_DATA_SPEC.md`, `opendecide-data/lean/c_spec/LICENCE_REGISTER.md`, and `opendecide-data/lean/c_spec/replay_licence_scan.json`.

## Datasets not to add

| Dataset or group | Reason |
|---|---|
| ShARC | Already explicitly rejected in the project after a hand audit found a concentrated wrong-label problem. |
| ProofWriter expansion | The existing licence scan has 687 replay rows but no recorded licence. The official data licence could not be verified from a first-party page during this research. Keep the existing rows quarantined for licence review and do not add more merely because the RuleTaker code repo is Apache-2.0. |
| PubMedQA | It is already used by the local think-check path and is named in the repo's OHS overlap checks. Training on it would contaminate a reported check. |
| Natural Questions / AmbigQA | NQ is a parent of current sources and NQ long pages are explicitly excluded locally; adding it increases duplicate and benchmark-overlap risk. |
| LegalBench, LexGLUE, ContractNLI, CUAD, MAUD, PrivacyQA, OPP-115 | Explicitly reserved or denied by the project's OHS/Decision Index rules. |
| ToolBench, ToolACE, xLAM, Glaive, Hermes function calling, API-Bank-style synthetic tool corpora | Many use LLM-generated text or labels; several are already explicitly denied. They conflict with the project's human-text / program-label rule and are especially vulnerable to benchmark leakage. |
| Metaculus live API data | Current official API terms prohibit using retrieved data to train or develop AI/ML without prior written permission. Non-commercial status alone is not permission. |
| AutoCast snapshot | The authors say they obtained permission to host it for research purposes only, but it is forecasting rather than rule-defined risk reasoning. Use only if the exact research permission covers this training, and only after decontamination; QUITE is cleaner. |
| NarrativeQA full stories | The official repo is Apache-2.0, but it links out to full books and movie scripts; the repository licence does not automatically clear every underlying document. Also, the task is narrative QA rather than decision-focused document reasoning. |
| SCROLLS / LongBench evaluation items | They are benchmark suites. Do not ingest validation/test material from anything that will be reported. Qasper and QuALITY train data are already handled directly with stronger per-document licence controls. |

## Proposed external supplement

If an amendment allows non-commercial sources, a conservative round-2 supplement is:

| Source | Rows | Family |
|---|---:|---|
| QUITE train, gold subset | 3,000 | F8 |
| SGD/SGD-X train, split by schema | 4,000 | F12 |
| TabMWP train, executable/recomputed subset | 2,000 | F2 |
| RuleTaker, archive-licence verified | 2,000 | F1/F10 auxiliary |
| CLUTRR, codebook-transformed | 1,000 | F10 auxiliary |
| **Total maximum** | **12,000** | supplement only |

This cap avoids drowning the project's program-verified distributions with benchmark-specific surface patterns. If time is tight, use only **QUITE (3,000)** and **SGD (4,000)**.

## Required checks before any row enters training

1. Create a preregistration amendment naming the dataset, exact revision, split, row cap, transform and licence obligations. Non-commercial permission is not retroactive permission for unverified data.
2. Use train data only. Keep dataset groups together: QUITE story/network, SGD schema/service/dialogue, TabMWP problem family, RuleTaker theory, CLUTRR story/template.
3. Re-read the first-party licence at the pinned revision and store the licence file plus SHA-256. Check source-document licences separately from annotation licences.
4. Run the full local deny-list on the dataset and every declared parent before rendering rows.
5. Decontaminate against OHS-1/2/3, Decision Index, Nimble, JevBench, LongBench v2, sealed hashes, dev sets and replay.
6. Re-derive every program-checkable label. For human labels, blind-audit a stratified sample and drop the whole source if error exceeds the preregistered threshold.
7. Check a source-only baseline and metadata-only baseline for shortcuts. Cap every external dataset so it cannot dominate a family.
8. Keep NC/SA-derived rows and notices private. A later commercial release would require retraining without NC rows, not merely changing a model card.

## First-party web sources consulted

- RuleTaker official repository and Apache-2.0 licence: https://github.com/allenai/ruletaker
- QUITE official repository and dataset licence statement: https://github.com/boschresearch/quite-emnlp24
- Google SGD/SGD-X official repository and CC BY-SA 4.0 licence: https://github.com/google-research-datasets/dstc8-schema-guided-dialogue
- TabMWP official repository, size, format and CC BY-NC-SA 4.0 dataset licence: https://github.com/lupantech/PromptPG
- CLUTRR official repository and CC BY-NC 4.0 licence: https://github.com/facebookresearch/clutrr
- ConditionalQA official project page: https://haitian-sun.github.io/conditionalqa/
- SMCalFlow official project page: https://microsoft.github.io/task_oriented_dialogue_as_dataflow_synthesis/
- STAR official repository: https://github.com/RasaHQ/STAR
- Natural Questions official repository: https://github.com/google-research-datasets/natural-questions
- AutoCast official repository permission note: https://github.com/andyzoujm/autocast
- Metaculus official API terms summary: https://www.metaculus.com/api/
- CommitPack official dataset card: https://huggingface.co/datasets/bigcode/commitpack
- CommitChronicle official Zenodo record: https://zenodo.org/records/8189044

This is research guidance, not legal advice.
