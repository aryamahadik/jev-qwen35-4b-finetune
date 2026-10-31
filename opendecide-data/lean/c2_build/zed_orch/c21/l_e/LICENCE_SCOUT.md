# L-E licence scout (18 Oct 2026)

Scout: Haiku 5.5, day-1 task 1 of LANE_L-E.md. Opus confirmation still required.
All pages were fetched on 18 Oct 2026 with WebFetch (no downloads). Where a page only
showed a sidebar label, the text is quoted as the label and the item is marked accordingly.
Status key: VERIFIED = licence text or licence field quoted from the card/repo with URL and date;
PARTIAL = licence named but the data-file or weight-file terms are not shown; UNVERIFIED = no usable licence text.

## Opus confirmation (18 Oct 2026)

Every cited URL was re-opened with WebFetch on 18 Oct 2026, plus the raw README/LICENSE files and the HF API listings named below. Nothing was downloaded, no model or API was called, and no path containing "ohs" or "sealed" was opened.
Verdict key: CONFIRMED = the scout's status holds; CORRECTED = the scout's status was wrong and is fixed here; UNVERIFIED = still no usable licence text after the re-check.
"Eval read" means internal reading/scoring only: no training, no redistribution, attribution kept.

| # | Item | Opus verdict | Licence (evidence) | Eval read? |
|---|---|---|---|---|
| 1 | BFCL data files | CORRECTED (UNVERIFIED to Apache-2.0) | HF raw README YAML `license: apache-2.0` (the sidebar reads "apache-2.0", not "cc"); BFCL README: "All the leaderboard statistics, and data used to train the models are released under Apache 2.0."; gorilla LICENSE = Apache License 2.0 | YES |
| 2 | CRUXEval | CONFIRMED (MIT) | LICENSE file now read: "MIT License / Copyright (c) 2023 Meta"; HF `License: mit` | YES |
| 3 | LiveCodeBench data | CONFIRMED UNVERIFIED (data) | Code LICENSE = MIT ("Copyright (c) 2024 LiveCodeBench"). HF raw YAML for code_generation_lite is only `license: cc`, with no variant; code_generation is the same. MIT covers the code only. | NO until the owner rules (see note A) |
| 4 | ImpossibleBench data | CONFIRMED UNVERIFIED (data) | Repo LICENSE = MIT ("Copyright (c) 2025 ImpossibleBench Team"), but it covers the code. HF API: impossible_livecodebench and impossible_swebench have no licence tag and empty READMEs. Upstream: SWE-bench LICENSE MIT; LiveCodeBench data unknown (item 3). | NO until the owner rules (see note A) |
| 5 | AgentDoG 1.5-4B weights | CORRECTED (UNVERIFIED to Apache-2.0) | The scout's repo id was wrong. HF search API lists `AI45Research/AgentDoG1.5-Qwen3.5-4B` (also `-Unified-` and `-FG-` 4B variants). That card shows `License: apache-2.0` and says "This project is released under the Apache 2.0 License."; base Qwen3.5-4B. | YES (weights, as an eval comparator) |
| 6 | Strands Decider 2B | CORRECTED (PARTIAL to Apache-2.0 for v19 and v21) | v19 LICENSE.md read: "This model is released under the Apache License 2.0 ..."; base Qwen/Qwen3.5-2B-Base (Apache-2.0). The v21 card exists (created 2026-10-05) with `License: apache-2.0` and the same LICENSE.md pointer, base Qwen3.5-2B-Base. The card does not say v21 supersedes v19; it calls v21 "the released seed of six". The org also has `strands-decider-2B-qwen3.5-v1-2610` (apache-2.0 tag, API only). | YES (v19 or v21; the plan must name one) |
| 7 | Liu harness (arXiv 2610.03448) | Licence CONFIRMED (MIT); mapping CORRECTED (UNVERIFIED to resolved); row counts UNVERIFIED | LICENSE: "MIT License / Copyright (c) 2026 lzwhehe". Upstream AgentDojo LICENSE MIT (Debenedetti et al. 2024); README: tau-bench, InjecAgent, BIPIA MIT. Paper CC BY 4.0. Mapping from analysis/compute_all.py + make_macros.py: AD-Matched = agentdojo_pairs.jsonl; AD-Shift = agentdojo_pairs_shift.jsonl; AD-Clean = agentdojo_benign_outputs.jsonl (keys `adclean_*`; the literal label "AD-Clean" is not printed). The counts 339/585/975 appear in no fetched file. | YES (rebuild from upstream; counts must be checked after the CPU rebuild) |

Note A (items 3 and 4): HF `license: cc` with no variant could be BY, BY-SA or BY-NC(-SA). Under the strictest of these (NC-SA), even internal eval by a commercial project is a grey area. ImpossibleBench's HF datasets carry no licence at all, which defaults to all rights reserved. Both stay NOT CLEARED. They need an owner ruling, or a written licence statement from the dataset authors, before any eval read.

Other source in the list: `OpenHands/openhands-critic-4b-v1.0` is CONFIRMED `License: mit` (not one of the 7 items).

## Scout summary (original, superseded by the table above)

| # | Item | Status | Licence named | Note |
|---|---|---|---|---|
| 1 | BFCL data files | UNVERIFIED | HF sidebar "cc" (variant not shown); code Apache-2.0 | Data terms not stated. |
| 2 | CRUXEval HF card | VERIFIED (card + GitHub) | MIT | Card prose quoted. |
| 3 | LiveCodeBench data | UNVERIFIED | HF sidebar "cc"; GitHub "MIT license" label only | Data licence not stated. |
| 4 | ImpossibleBench data | UNVERIFIED | none shown; GitHub code "MIT license" label only | HF dataset README is empty. |
| 5 | AgentDoG 1.5-4B weights | UNVERIFIED | HF page returned HTTP 401 | 1.5 model not found on any fetched card. |
| 6 | Strands Decider 2B | PARTIAL | HF card (hobson-v19) sidebar "apache-2.0" | Checkpoint is v19; current version not confirmed. |
| 7 | Liu harness (arXiv 2610.03448) | VERIFIED licence; script-to-set mapping UNVERIFIED | MIT | Repo lzwhehe/benign-instruction-bench. |

## 1. BFCL data files

- Source checked: https://huggingface.co/datasets/gorilla-llm/Berkeley-Function-Calling-Leaderboard (fetched 18 Oct 2026). Sidebar field reads: "cc". No licence text on the card. The card does not say which CC variant applies.
- Code repo https://github.com/ShishirPatil/gorilla (fetched 18 Oct 2026): sidebar "Apache-2.0 license"; card text quoted: "Gorilla is Apache 2.0 licensed, making it suitable for both academic and commercial use." The card says nothing about the BFCL data terms.
- Raw LICENSE for berkeley-function-call-leaderboard: HTTP 404 (not retrieved).
- Status: UNVERIFIED for the data files. The Apache-2.0 code licence does not cover the data. Opus must decide whether a "cc" sidebar value is enough, or whether a data-licence statement is needed.
- **Opus: CORRECTED to Apache-2.0.** The HF raw README YAML reads `license: apache-2.0` (the sidebar shows apache-2.0, not cc). The BFCL README (raw, gorilla/berkeley-function-call-leaderboard/README.md) says: "All the leaderboard statistics, and data used to train the models are released under Apache 2.0." The repo LICENSE is Apache License 2.0. Eval read: YES.

## 2. CRUXEval HF card

- Source: https://huggingface.co/datasets/cruxeval-org/cruxeval (fetched 18 Oct 2026). Licence section quoted: "CRUXEval is MIT licensed, as found in the LICENSE file." Sidebar: "mit". No date shown on the card.
- Source: https://github.com/facebookresearch/cruxeval (fetched 18 Oct 2026). Licence section names "MIT license". The LICENSE file text was not quoted.
- Status: VERIFIED (card prose plus GitHub sidebar). Opus may want the LICENSE file text quoted in full.
- **Opus: CONFIRMED MIT.** Raw LICENSE opens "MIT License / Copyright (c) 2023 Meta". Eval read: YES.

## 3. LiveCodeBench data

- Source: https://github.com/LiveCodeBench/LiveCodeBench (fetched 18 Oct 2026). Only the label "MIT license" appears (sidebar and file list). No licence text and no dataset-licence statement.
- Source: https://huggingface.co/datasets/livecodebench/code_generation_lite (fetched 18 Oct 2026). Sidebar: "cc". No licence text.
- Source: https://huggingface.co/datasets/livecodebench/code_generation (fetched 18 Oct 2026). Sidebar: "cc". No licence text.
- Status: UNVERIFIED for the data. The code label MIT is not quoted from the LICENSE file. The "cc" value is not tied to a named variant.
- **Opus: CONFIRMED UNVERIFIED for data.** Code LICENSE is MIT ("Copyright (c) 2024 LiveCodeBench"). The HF raw YAML is only `license: cc`, with no variant. Eval read: NO until the owner rules (note A).

## 4. ImpossibleBench data

- Source: https://github.com/safety-research/impossiblebench (fetched 18 Oct 2026). Only the label "MIT license" appears. The page says the benchmark datasets are on HuggingFace, with no licence statement.
- Source: https://huggingface.co/datasets/fjzzq2002/impossible_livecodebench (fetched 18 Oct 2026). Card: "README.md exists but content is empty." No licence field. Collection "ImpossibleBench Datasets" shows "Updated Oct 24, 2025."
- Web search (18 Oct 2026): no licence found in the results.
- Note: the datasets derive from LiveCodeBench and SWE-bench (search summary), so upstream terms may also apply. Upstream terms were not checked here.
- Status: UNVERIFIED. The Impossible-SWEbench dataset page was not fetched.
- **Opus: CONFIRMED UNVERIFIED for data.** Repo LICENSE is MIT ("Copyright (c) 2025 ImpossibleBench Team") and covers the code. The impossible_swebench page was fetched: empty README, and the HF API shows no licence tag on either dataset. Upstream SWE-bench is MIT; upstream LiveCodeBench data is unknown. Eval read: NO until the owner rules (note A).

## 5. AgentDoG 1.5-4B weights

- Source tried: https://huggingface.co/AgentDoG/AgentDoG-1.5-4B (fetched 18 Oct 2026): HTTP 401 (matches the plan's note).
- Web search (18 Oct 2026): AgentDoG 1.5 comes in 0.8B, 2B, 4B and 8B sizes, per the search summary of the paper. The search did not return a model card with a licence. A third-party page (everydev.ai) says Apache 2.0 for the earlier AgentDoG family. That is not the 1.5 model card, so it is not counted.
- Different model, not the same: https://huggingface.co/ninty-seven/AgentDoG-Step (fetched 18 Oct 2026). Sidebar "License: apache-2.0". Card quoted: "The StepGuard model weights and accompanying StepGuard materials are released under the Apache License 2.0." Base model Qwen3-4B-Instruct-2507. This card is for StepGuard, not AgentDoG 1.5-4B, and must not be used as the AgentDoG 1.5 licence.
- Status: UNVERIFIED for AgentDoG 1.5-4B. Needs the correct repo ID and an accessible card, or an authenticated route.
- **Opus: CORRECTED to Apache-2.0.** The correct repo is https://huggingface.co/AI45Research/AgentDoG1.5-Qwen3.5-4B (found via the HF search API). Its card shows `License: apache-2.0` and says "This project is released under the Apache 2.0 License."; base Qwen3.5-4B. Sibling AI45Research/AgentDoG1.5-Unified-Qwen3.5-4B is also apache-2.0. Eval read: YES. The plan must name the variant (plain, Unified or FG).

## 6. Strands Decider 2B

- Source: https://huggingface.co/StrandsAgents/strands-decider-2B-hobson-v19 (fetched 18 Oct 2026). Sidebar: "License: apache-2.0". Card text quoted: "the code is under the same Apache-2.0 license as this model (see LICENSE.md)." The card gives no release date. The LICENSE.md file was not fetched.
- Version caveat: this card is for v19. Secondary news coverage (search, 18 Oct 2026) says v21 is now the reference checkpoint with v19 still published. That coverage is not licence text. The current repo was not checked.
- Secondary coverage (not counted as licence evidence): several news pages say Apache 2.0.
- Status: PARTIAL. Apache-2.0 is quoted from the v19 card. Opus must confirm the checkpoint the plan will use, and read its LICENSE.md.
- **Opus: CORRECTED to Apache-2.0 (v19 and v21).** v19 LICENSE.md read: "This model is released under the Apache License 2.0, the same license as the strands-decider code ..."; base Qwen3.5-2B-Base. The v21 card (created 2026-10-05) shows `License: apache-2.0` and the same LICENSE.md pointer. It calls itself "the released seed of six" and does not claim to supersede v19. Eval read: YES. The plan must name v19 or v21.

## 7. Liu harness (arXiv 2610.03448)

- Paper: https://arxiv.org/abs/2610.03448 (fetched 18 Oct 2026). Title "Passing the Test You Trained On: Re-evaluating Prompt-Injection Detectors for LLM Agents". Sole author Zhuowen Liu. Submitted 2 Oct 2026 (v1). Comments field: "Code: this https URL" pointing to github.com/lzwhehe/benign-instruction-bench. The arXiv page shows a CC BY 4.0 licence for the paper, which is not the harness licence.
- Repo: https://github.com/lzwhehe/benign-instruction-bench (fetched 18 Oct 2026). Licence section quoted: "Code, analysis scripts, and score files: MIT (see `LICENSE`)." Also: "Third-party files keep their own terms: the USENIX LaTeX style ... the benchmarks and detectors the scripts download (AgentDojo, tau-bench, InjecAgent, BIPIA, and each detector's model license)." Sidebar: "MIT license".
- Data note quoted from README: "Evaluation data is rebuilt from the public sources, not redistributed: AgentDojo v1.2, tau-bench (MIT), InjecAgent attacks (MIT), BIPIA (MIT)."
- Script-to-set mapping (fetched via WebFetch; the summary was not verbatim, so Opus should check the raw file):
  - reproduce.sh contents were summarised. Steps 1-3 build the .jsonl sets on CPU with PYTHONHASHSEED=0 (README quote).
  - scripts/collect_agentdojo_pairs.py is run with two attack-type lists. One list (important_instructions, ignore_previous, direct) writes agentdojo_pairs.jsonl. A second list (tool_knowledge, injecagent, system_message, important_instructions_no_names, important_instructions_wrong_model_name) writes agentdojo_pairs_shift.jsonl. scripts/attach_requests.py combines them.
  - scripts/collect_agentdojo_outputs.py writes agentdojo_benign_outputs.jsonl (clean replay).
  - scripts/build_bipia.py writes the BIPIA matched set. scripts/collect_taubench.py and scripts/build_taubench_eval.py build the tau-bench set.
  - scripts/score_normalized.py runs on the main, shift and BIPIA pair files. scripts/hf_judge.py runs the 4-bit Qwen2.5-7B and Llama-3.1-8B judges.
  - Robustness and agent run: scripts/e5_run.py, e5_compare.py and e5_score.py (needs vLLM serving Qwen2.5-7B-Instruct).
- Not found: the names AD-Clean, AD-Matched, AD-Shift do not appear in the README or the fetched reproduce.sh summary. The 339 / 585 / 975 row counts cannot be checked here. The mapping from the pair files to Liu's named sets is UNVERIFIED and must be checked against the raw reproduce.sh and the analysis scripts.
- Status: licence VERIFIED (MIT, quoted from repo). Script-to-set mapping UNVERIFIED (partial; AD-named sets not found).
- **Opus: licence CONFIRMED MIT** (LICENSE "Copyright (c) 2026 lzwhehe"; upstream AgentDojo LICENSE MIT). **Mapping CORRECTED to resolved** via analysis/compute_all.py and make_macros.py: AD-Matched = agentdojo_pairs.jsonl, AD-Shift = agentdojo_pairs_shift.jsonl, AD-Clean = agentdojo_benign_outputs.jsonl (`adclean_*` keys). **Row counts 339/585/975 remain UNVERIFIED**; they appear in no fetched file and must be checked after the CPU rebuild. Small fix: the arXiv comments field reads "12 pages, 5 figures, 4 tables" plus the code link. Eval read: YES.

## Items not covered

- Not fetched: the raw LICENSE files for BFCL, LiveCodeBench, ImpossibleBench and CRUXEval. Each item above says which file was read.
- Not touched: nothing downloaded, no model or API called, no path containing "ohs" or "sealed" opened, no changes to HANDOFF.md or PREREG_FINAL.md.

## Sources (all fetched 18 Oct 2026)

- https://huggingface.co/OpenHands/openhands-critic-4b-v1.0 (MIT; header "License: mit")
- https://huggingface.co/datasets/cruxeval-org/cruxeval
- https://github.com/facebookresearch/cruxeval
- https://huggingface.co/datasets/gorilla-llm/Berkeley-Function-Calling-Leaderboard
- https://github.com/ShishirPatil/gorilla
- https://github.com/LiveCodeBench/LiveCodeBench
- https://huggingface.co/datasets/livecodebench/code_generation_lite
- https://huggingface.co/datasets/livecodebench/code_generation
- https://github.com/safety-research/impossiblebench
- https://huggingface.co/datasets/fjzzq2002/impossible_livecodebench
- https://huggingface.co/AgentDoG/AgentDoG-1.5-4B (HTTP 401)
- https://huggingface.co/ninty-seven/AgentDoG-Step (apache-2.0, StepGuard, not AgentDoG 1.5)
- https://huggingface.co/StrandsAgents/strands-decider-2B-hobson-v19 (apache-2.0, v19)
- https://arxiv.org/abs/2610.03448
- https://github.com/lzwhehe/benign-instruction-bench (MIT)
