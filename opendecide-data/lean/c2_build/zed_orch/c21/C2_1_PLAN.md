# C2.1 plan (draft v1, 17 Oct 2026 ~15:45 UTC; orchestrator, Opus)

Status: DRAFT. Nothing in this file is built or spent before the owner's C2.1 GO (owner, 17 Oct: "I'll tell you when to
go for C2.1 after I check the report for C2"). Preparation listed in section 8 is planning, tooling and CPU-only checks.

## 1. Goal (owner, 17 Oct)
- **Best at agentic coding decisions** ("the Anthropic playbook": win a niche, not general chat): the fast yes/no/which
  calls a coding agent makes many times per task.
- **Better general accuracy:** owner target at least +2 to +3 points over C2 on the sealed general test.
- **Lower latency and lower cost** than C2: all optimisations that need training.
- Voice (English) + image attached unchanged; other-language audio later. No per-customer fine-tunes.

## 2. Honest targets (projections, not measurements)
| Metric | C1 (measured) | C2 (proj.) | C2.1 target | C2.1 likely | Jev 1.14 |
|---|---|---|---|---|---|
| General (sealed) | 74.3 (OHS-3) | ~74-75 | C2 + 2-3 | C2 + 1-2 | 79.6 |
| Agentic coding decisions (new sealed block) | n/a | n/a | best measured | clearly > C1 | unknown |
| Server ms / decision (H100, batch 1) | 32 | ~30 | ~20 | ~20-25 | ? |
| e2e p50, hosted near users | ~85 | ~85 | ~75 | ~75-80 | 156 |
| $ / 1K (busy GPU) | 0.014 | ~0.012 | ~0.006 | ~0.006-0.008 | 0.023 |
| ECE | 3.3% | ~3-4% | <= 3% | ~3% | 6.0% |
- +2-3 general over C2 is ambitious at 4B; +1-2 is the realistic expectation unless the owner opens the extra levers in
  section 7.

## 3. Order of work (the new sealed test comes FIRST)
1. **OHS-5 (new clean sealed test), frozen before any C2.1 data.**
   - Blocks: G (general: >= 20 fresh public human/official/program-gold sources, <= 500 items each), C (agentic coding
     decisions, built by NEW sealed-side generators that share no code, templates or wording with any training
     generator), R (rule/agent), K/X (option-order and attack robustness).
   - Design rules fixed in its brief before building: training-side frames disjoint from sealed frames by construction;
     keyword export = dataset-specific identifiers only (multi-word names, rare single tokens, URL paths; never common
     words, generic hosts or licence URLs); hash exports for every G13 method; a sealed-side access audit.
2. **Data** (written blind to OHS-5; G13 against OHS-4 + OHS-5 + every public/dev target):
   - **Agentic coding decisions (main focus), execution gold where possible:** patch verdict (does the patch fix the
     failing test: run it), bug localisation (which file/function), tool/command safety (destructive or secret-leaking
     commands), next agent step (run tests / edit / ask), CI triage (flaky vs real: re-run gold), code review verdict,
     dependency-upgrade risk (resolver + test run), merge-conflict choice, test selection (coverage gold), output
     prediction (execution gold). Sources: synthetic repos written by Sonnet + permissively licensed open-source code
     passing the deny-list and the 8.5 check. Haiku writes wording; a separate session writes solver B.
   - **General accuracy:** harder reasoning with program gold (math word problems, causal, logic), new fresh public
     sources (each 8.5-checked once by the orchestrator), C1/C2-error-focused selection (units the model already knows
     are dropped; wrong ones get weight).
   - **Rebuilt agent families T40-T46** with training-side text disjoint from every sealed frame.
   - **Voice robustness:** transcripts with real ASR errors (TTS -> ASR, 3-15% WER) so speech decisions match text
     decisions (today 89% on real spoken commands; target >= 97%).
   - Replay from C2's mix to keep skills.
3. **Training (one run, continuing from C2 if C2 ships; else from C1 or C2's weights, owner's choice at the C2.1 GO):**
   - compact, static-first prompt (instructions + definitions first and cacheable; compact JSON);
   - option-order-invariant training so serving can use ONE read per choice question (~30% less compute);
   - optional second stage: FP8-aware distillation (KL to the BF16 parent) so the 8-bit model gives the same answers;
   - calibration kept (ECE <= 3%).
   - Budget ~$10-20 Modal.
4. **Serving (from the C1 trials):** exact server bundle, safe-FP8 margin gate re-fitted on C2.1, hosting near users,
   keep-alive connections, warm pool, cheapest acceptable GPU host; voice (Nemotron EN 560 ms streaming, offline mode
   for files, push-to-talk default) and native images.
5. **Evaluation:** OHS-5 one-shot (G, C, R, K/X) vs C2 and Jev; OHS-4 report; latency/cost suite; voice (real audio)
   and image packs.

## 4. Timeline (if the owner gives the C2.1 GO ~Tue 20 Oct)
| When | Step |
|---|---|
| Tue 20 - Fri 23 Oct | OHS-5 sealed build + freeze (sealed-side agents) |
| Wed 21 - Mon 26 | C2.1 data build + gates (parallel family drivers; heavy CPU on od-cpu1) |
| Tue 27 | G13 (serial on the Mac), selection, mix, preflight |
| Wed 28 | GO #1 for C2.1 -> train (~4 h) |
| Thu 29 - Fri 30 | checks + GO #2 -> OHS-5 final test |
| ~Fri 30 Oct - Sun 1 Nov | C2.1 report |
- If training must wait for the 1 Nov credit renewal: results ~4-5 Nov.

## 5. Budget
- Modal: after C2 (~$23) about $10 remains on the 2 training accounts; C2.1 needs ~$10-20 -> spare accounts or the card
  only by an owner ruling at its GO #1, or wait for 1 Nov.
- OpenRouter (Jev reads on OHS-5): ~$7 left; may need a small owner-named top-up.
- Claude usage: heavy; use the Monday reset and the manual reset; ping the owner at 96%.

## 6. Risks
- The general +2-3 target may not be reached at 4B (realistic +1-2).
- Execution-gold sandboxes must be hermetic (no network, pinned deps); 8.5/deny-list may remove open-source code sources.
- OHS-5 must be frozen before data, or its claims are weaker.

## 7. Owner decisions (at the C2.1 GO, none now)
1. The C2.1 GO itself (after the C2 report).
2. Optional extra lever for general accuracy: a split-aware deny-list (train splits of datasets whose test splits are
   benchmarks; standard practice elsewhere; changes adopted rule A61 b).
3. Funding route (spare accounts / card / wait for 1 Nov).
4. Later, not C2.1: a bigger base model; image training data; other-language ASR.

## 8. What can be prepared now (no C2.1 builds, no spend)
- Family design notes for the 10 coding-decision families (inputs, gold method, solver B, gates).
- OHS-5 brief draft (blocks, disjointness rules, keyword-export rule) for the sealed side.
- CPU-only checks: token counts of the compact static-first prompt on the 8,143 parity prompts; order-invariance
  measurement of C1 (and later C2) on dev to size the single-read gain.
- Sandbox design for execution gold (container, no network, pinned toolchains).
- Licence scouting list for permissive code sources (to be 8.5-checked by the orchestrator only at build time).
