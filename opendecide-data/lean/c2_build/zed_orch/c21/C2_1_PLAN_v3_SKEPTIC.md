# C2.1 PLAN v3 SKEPTIC (Opus; Sun 18 Oct 2026)

Targets: C2_1_PLAN_v3.md, C2_1_BUILD_ORDER.md, OHS5_BRIEF_DRAFT.md.
Read: plan v3 (all), build order (all), plan v2 (sections on A62(c), OHS-AC, owner decisions), research_v3
ORCHESTRATION_RULES.md, OWNER_GOALS_18OCT.md, THINK_MODE_MEASURED.md, ALREADY_TESTED_C1_OPT.md, and greps of voice.md,
injection.md and permission.md.
NOT read: OHS5_BRIEF_DRAFT.md and research_v3/sealed.md. Their paths contain "OHS" / "sealed", and the task rules say
never to open such paths. The brief is attacked only through what plan v3 section 3 and the build order say about it.
It needs its own fresh sealed-side skeptic (build order L-S day-1 task 1). See problem 7.
Web: the shared WebSearch budget was used up before this pass (same as the v3 planner pass). Only direct fetches were
made: Qwen3.5-4B config.json and Modal terms (both fetched 18 Oct 2026). Every other external fact below comes from
research_v3 files and is marked as such.

Severity: HIGH = breaks a rule, or can kill C2.1 / void the headline. MEDIUM = wrong number, gate that cannot be
measured, or owner-reserved decision taken. LOW = hygiene.

---------------------------------------------------------------------------------------------------------------------
## HIGH

1. Selective-think tier is still in the plan after it was removed.
   Where: plan section 6 ("v3 selective-thinking tier"), section 9 (R8a row and the "With R5 and R8a" projection),
   section 10 R8(a).
   Problem: THINK_MODE_MEASURED.md (orchestrator decision, 18 Oct) says the tier is REMOVED from C2.1 and "the planner
   must not list it as a lever". Measured basis: about 0 gain on OHS-1/2; every think policy failed the A17 B1 "e2e
   median <= 1 s" rule; about 5-7x average cost. The owner's own concern was latency and cost.
   Fix: delete R8a everywhere. Recompute section 9 without it, so only the "without levers" and "with R5" rows remain.
   Keep the general levers data-side only, as that file says.

2. OHS-AC stays binding on new rows that use C2's rendered layout, so the A62(c) mass drop can happen again.
   Where: plan section 5 MIX ("plan applies OHS-AC as BINDING to every C2.1 row"); R4 default ("new rows binding either
   way"); R4 needed only "~Wed 4 Nov"; build-order kill rule ("more than 1% of a 200-row G13 pilot hit ... IS the fix
   iteration"); R6 exemption scoped to OHS-5 only.
   Problem: plan v2 says that under a binding OHS-AC, replay "likely [falls to] near 0 after A62(c)". v3's own
   "preventing a repeat" list blames product-format text (header, option scaffolding, definitions card) and keywords.
   C2.1 keeps C2's layout (cygnet + schema_branch_mark). Clean-room families change the content, not the scaffolding.
   If any OHS-3/4/AC method matches the scaffolding, every family's first pilot (25 Oct) uses up its one fix
   iteration. A second hit kills the family, and the floor (6 of 9) fails. This all happens about 10 days before R4 is
   even asked. (UNVERIFIED whether the A62(c) drop was format-driven; the plan's own fix list implies it was.)
   Fix:
   (a) Before 25 Oct, run every G13 target (OHS-3, OHS-4, OHS-AC) on about 200 format-only dummy rows in C2's layout.
       The dummy rows carry neutral content. Publish the hit rate per method.
   (b) Widen R6 to "the product-format exemption applies to every G13 target", in the same owner message.
   (c) Move R4 to before the rows start (Sat 24 Oct).
   (d) Pre-register that a pilot hit traced only to exempted scaffolding is not the family's fix iteration. This loosens
       a rule, so it goes to the owner with R6.

3. Keyword export: Claude-picked fake names on both sides will collide, the same way OHS-AC killed rows.
   Where: plan section 3 "Keyword export covers dataset-specific identifiers only"; nothing says how this is tested.
   Problem: C-block items and training rows are both written by Claude agents from scenario templates. Claude tends to
   reuse the same "natural" fake names on both sides (company, repo, host, service, bucket and tool names).
   "Dataset-specific" is not defined by any test. A sealed fake host that also shows up in a training wording pool
   becomes a keyword HIT on training rows.
   Fix:
   (a) Both sides draw every identifier from a seeded random namespace with a side-specific salt. No hand-picked fake
       names.
   (b) Program filter on the export: drop any keyword that appears in C2's mix, in the training names-only manifest or
       in a public common-token list.
   (c) Before the freeze, dry-run the keyword export against C2's mix. If more than 0.5% of C2 rows hit, the export is
       too generic and the sealed side prunes it.

4. The names-only manifest is frozen before the names it must hold exist, and it is not a closed list.
   Where: build order L-0 day-1 task 2 and orchestrator step 3 freeze manifest v1 on Sun 18. The G0-lites define the
   policy cards, tool catalogues, carrier formats and runners, and they are only approved Mon 19. C-transfer is defined
   as names "absent from the frozen training names-only manifest".
   Problem: v1 will miss names that the G0-lites add later. Nothing stops a training generator, or its fix iteration,
   from later adopting a name that C-transfer uses. That makes "transfer" items quietly in-distribution, and the
   headline is void.
   Fix:
   (a) Freeze v1 after the Mon 19 G0-lite approvals, before L-S picks names.
   (b) The row-start guard checks every policy, tool, language, runner and carrier name in each row against a closed
       allow-list taken from the manifest.
   (c) No additions after the OHS-5 freeze. If one is unavoidable, the affected C-transfer sub-block becomes
       report-only.

5. R5 (A61(b) public TRAIN splits) is decided after the sealed side has already picked G sources.
   Where: R5 is "by ~Sun 25 Oct". The sealed side picks the G-source shortlist on Mon 19 and does G extraction on
   Tue 20.
   Problem: if the owner adopts R5, the train split of a dataset whose other split (or close sibling) is a G source can
   enter training. That inflates OHS-5 G, which is the owner's ship metric (gap <= 4).
   Fix: list the R5 candidate datasets now (names only) in manifest v1. L-S excludes every one of them from G at
   dataset level, whatever the owner answers.

6. Four gates need a trained model before the data freeze, so they cannot be measured.
   Where:
   - T56g "train on 6 of 8 transform families, test on the other 2, rotate; bar from base 4B".
   - T41c D3 "in-family vs held-out gap above 5 pp triggers the fix iteration".
   - T54 call/no-call bias gate (per-class recall and logit offset: of which model?).
   - T42c "each [trace-length] bin gated against base 4B".
   Problem: the plan has one Modal run, one stage, and Modal is training only. od-l4b is not for training. These gates
   cannot run before the 2 Nov data freeze, yet the kill rule needs them by then.
   Fix: split each gate in two.
   - Pre-freeze kill gate: a CPU probe, e.g. TF-IDF or feature logistic regression trained on the in-family rows and
     scored on the held-out families. CPU probes are already allowed as "shortcut gates".
   - Post-training eval: the model-based version, report-only, not a kill rule.
   Write which is which into each G0-lite.

7. The barred-author rule is broken by how the brief is written, and the plan leaks sealed design into
   training-readable files.
   Where: plan section 3 bars from the sealed side "anyone who wrote or read ... the family-design sections of this plan
   or research_v3, and the reverse". The Opus planner wrote both the family designs and OHS5_BRIEF_DRAFT.md. Build
   order L-S day 1 says "planner fixes" the brief after the skeptic.
   Plan section 3, which training lanes can open, mirrors training mechanics into the sealed composition:
   - "obfuscation and consent-tier pairs";
   - "ambiguous write and implicit error";
   - "hack families no training transform uses";
   - "held-out attack families".
   This workflow step itself asked one agent to read both the training plan and the sealed brief.
   Fix:
   (a) A fresh sealed Opus re-derives the brief from a decision-level spec only: taxonomy, counts, statistics, metrics.
       No family mechanics. After day 1 the planner never edits the brief.
   (b) Move the section 3 composition into the brief. The plan keeps only the pre-registered headline rules.
   (c) Lane prompts name only the plan sections they may read. The access audit flags any training-side read of
       section 3.
   (d) Never again give one agent both sides.

8. G13 hit details and eval strings reach training authors.
   Where: kill rule (a G13 hit sends the generator back for a fix); L-I inputs include "the G13 literal-ban list from
   L-0"; L-A inputs include research_v3/permission.md section 5.
   Problem:
   - Nothing says what a hit report shows the fixing builder. If it shows the matched string, sealed or eval text
     reaches a training author.
   - The literal-ban list puts public attack strings in front of the T41c writer, inviting paraphrases that slip past
     literal matching.
   - permission.md section 5 quotes AmPermBench's ID format (`job-dev-4812-a`) and its four task families, but L-A is
     meant to be clean-room against them.
   Fix:
   (a) Hit reports carry row ids, target name and method only, never the matched text.
   (b) The ban is enforced by program inside G13; writers never see the list.
   (c) Strip quoted benchmark strings from research excerpts before they go to clean-room builders.

9. G13 targets for AmPermBench/UnderSpecBench "phrase frames" and "four task families" use generic coding-agent words,
   which makes them a keyword-kill risk.
   Where: plan section 2 (v3 permission targets); permission.md 5.9 lists the families as git branches, Slurm jobs,
   Kubernetes services and S3 artifacts.
   Problem: T50/T51/T53 cannot avoid git branches, Kubernetes or S3. As keyword or frame targets, these words would hit
   most permission rows, which is the same failure as OHS-AC.
   Fix: register only exact item strings, exact entity names and exact ID patterns from those benchmarks. Generic domain
   words are never targets. Write the "as written" ban as "never copy their item text or IDs", not "never use the
   domain".

10. Voice rulings that belong to the owner were taken by the planner.
    Where: plan section 7 rulings (a) "ASR transcripts as training INPUTS are allowed" and (b) Kokoro despite its
    closed-TTS training audio, with "the owner may veto".
    Problem:
    - research_v3/voice.md C6 says "Rule 27 and the NVIDIA licence deserve one explicit owner line". Q4 asks for an
      owner ruling on TTS provenance.
    - The NVIDIA Open Model License is outside the owner's MIT/Apache/BSD/CC list (voice.md section 4).
    - The plan's own section 10 reserves "loosening an adopted rule" for the owner. Model-made text as training input
      and an off-list licence are both loosenings.
    Fix: add R11 (ASR transcripts as inputs; Kokoro provenance; NVIDIA OML exception) to the next owner message with
    the default "allow". Until the owner answers, voice rows may be built, but they stay out of the mix manifest.

11. FP8-aware training was dropped, and an FP8 lever that already failed is re-listed.
    Where: plan section 5 "stage B FP8-KL dropped unless FP8 serving is adopted"; R8d "block-FP8 with margin gate".
    Problem:
    - ALREADY_TESTED_C1_OPT.md lists "FP8-aware training (KL to the bf16 parent)" as the first item of the only new
      work left. The owner says C2.1 "must carry EVERY optimisation".
    - The plan's condition is circular: FP8 serving cannot pass 99.5% parity without FP8-aware training.
    - Block-FP8 (98.38%) and the FP8 margin gate ("not confirmed out of sample") are recorded as FAILED, with "do NOT
      re-plan".
    Fix: either schedule the FP8-KL stage, with its cost inside R1, or make dropping it an owner-reserved line with a
    default. Remove R8d as an independent lever, or reword it as "only via FP8-KL training".

---------------------------------------------------------------------------------------------------------------------
## MEDIUM

12. An UNVERIFIED number drives the owner recommendation.
    Section 9 says R5 gives "+0.5 to +2.0 (UNVERIFIED planner estimate)", and the "honest message" then says the
    target "is reachable but not likely without R5". The header says UNVERIFIED numbers never drive a decision. The
    P(gap <= 4) values are pure guesses presented with precision.
    Fix: state "R5 gain: no evidence for a 4B; unknown". Drop the probabilities, or label them "no basis".

13. The owner's real-speech goal is not measured.
    ALREADY_TESTED records a real-speech measurement already: decision unchanged 89%, against a goal of 97% or more.
    Plan section 7 moves real speech to C2.2 and labels C2.1 voice results "TTS-based, an upper bound". So the stated
    voice goal has no measurement in C2.1.
    Fix: reuse the existing real-speech set, if its consent covers it, as an eval-only V2-lite with n and CI stated.
    Never train on it.

14. Voice chunk mix contradicts the locked product.
    The plan uses 160 / 560 / 1,120 ms "until the product chunk size is fixed". ALREADY_TESTED says 560 ms plus forced
    flush is LOCKED.
    Fix: make 560 ms with forced flush the main condition. Measure padding and flush behaviour at 560 ms (voice.md marks
    560/1,120 flush padding UNVERIFIED). Use other chunk sizes as a small robustness slice, or drop them.

15. No lane builds the Tier-1 harnesses or the deployment work.
    ALREADY_TESTED says the planner "must give each a lane, model tier, gate and day". The build order has no lane for:
    - the Tier-1 harnesses (Liu's AgentDojo harness, NotInject, ATBench and ATBench-Codex, When2Call AA, BFCL subset);
    - the deployment items (warm pool, hosting near users, cheapest parity GPU on the L4, batching to stay above about
      59% utilisation).
    Tier-1 reads "begin Sat 7 Nov" with no harness built.
    Fix: add L-E (Sonnet high) for eval harnesses: CPU build days 2-10, then a base-4B dry run on od-l4b, with row counts
    checked against Liu's (339/585/975). Add L-D for the deployment measurements on free GCP, never Modal.

16. The AgentDojo threshold is tuned on the benchmark itself.
    The 1%-FPR threshold is fit on "a task-disjoint benign dev split drawn from the larger benign pools", meaning
    AgentDojo's own pools. That tunes on an eval set, and it is inconsistent with OHS-5's "threshold frozen from
    non-sealed dev data".
    Fix: the primary threshold comes from our own non-benchmark dev data. The benchmark-split threshold is a labelled
    secondary.

17. The design-effect arithmetic is inconsistent.
    - C uses deff 2, but G's "sampling SE about 0.34 pp" equals sqrt(0.08/7,000), which is deff 1. At deff 2 it is
      sqrt(0.08 x 2 / 7,000) = 0.48 pp. That is above the 0.45 "unresolved" line, so the -1.0 test is unresolved by
      design and the -1.5 fallback becomes the real floor.
    - The C-transfer power note uses SE 2.2, but its own resolution line is 2.0, so that case would read "unresolved".
    - K/X power uses deff 1.5.
    Fix: one deff everywhere. Either enlarge G (about 10K items for 0.40 pp at deff 2, DERIVED) or state -1.5 as the
    planned floor and send it to the owner (problem 18). Restate the K/X power at deff 2.

18. The -1.5 pp G fallback margin is a loosening the planner decided alone.
    v2 recommended a ship floor of "C2.1 - C2 LB > -1.0". v3 adds a -1.5 fallback. OWNER_GOALS says the owner will
    review the plan.
    Fix: put it in the owner message as an owner-reserved line with a default.

19. The init branch "C2's unshipped weights" is decided without the owner.
    v2 listed init under owner decision #1, "after the C2 report". The memory rule says C2.1 needs the owner's GO after
    the C2 report. The 18 Oct GO covered research and building, not the choice of init.
    Fix: show the init branch in the GO #1 packet as an owner choice with a default.

20. "Near chance" is not a number.
    The T41c format-only probe, the T56 claim-only probe and the T57 style-only baseline are "near chance". As a kill
    rule, that cannot be applied.
    Fix: fix numbers in each G0-lite before any pilot, e.g. held-out AUC <= 0.55 with a 95% upper bound <= 0.60.

21. The T56g "natural-looking" slice cannot test the failure it cites.
    300 hacks "written by Claude without the library" are still prompt-elicited. The cited failure is that monitors
    trained on prompt-elicited hacks miss naturally arising ones (34.5 vs 99.7, author-run, from codeexec.md).
    Fix: label the slice "Claude-authored, prompted" and make no transfer claim. Optionally add an eval-only slice of
    hacks that arise on their own in Claude agent runs on impossible tasks in the sandbox (Claude output, never
    trained on).

22. The sealed timeline is not realistic, and late collisions land on training.
    - The sealed sessions start Mon 19 and have 6 days for about 14K+ items (C 4,400, U 450, K/X 1,900, G about 7,000,
      plus R).
    - C-CODE's 1,050 execution items can only run from Thu 22, after the Wed 21 sandbox sign-off.
    - The reverse pre-check (Fri 23) runs against training hash export v1 (Thu 22). Templates changed later, in fix
      iterations, are never checked by the sealed side, so every later collision kills training rows instead.
    - "80% by Sat 24" conflicts with "slip to Mon 26". A slip past Mon 26 has no hard stop.
    Fix:
    (a) Hard stop: if there is no freeze by Mon 26 23:59, each sub-block freezes at its achieved size, or the owner
        hears of it that day.
    (b) Pre-register that a training row colliding with frozen OHS-5 is dropped row by row, up to a stated share, and
        that this is not the generator's fix iteration.
    (c) Collect training hash exports at every template change, so the next C2.2 sealed build can use them.

23. The single L4 is oversubscribed, and the kill rule could fire on queue delay.
    od-l4b carries: C2 grid reads; C2 reads of about 38K C2.1 candidate rows; the voice probe, pilot and a 10-12K TTS+ASR
    pool; rival, base and Tier-1 reads; and the 18-candidate grid on Fri 6 Nov. There is no throughput budget.
    Fix:
    (a) C2 reads are not a kill gate. Selection can finish in the Wed 4 Nov window.
    (b) Measure L4 throughput per job type by Wed 21 and publish a queue plan.

24. The shared sandbox image and shared access weaken the sealed side.
    - C-transfer code needs languages or runners absent from training. od-sbx-s is cut from the training-side image
      (Python 3.12 / Node 24 / Go 1.26 / bash only). Adding a runner means telling the L-0 builder which one, which
      leaks it.
    - The L-0 builder and the orchestrator keep IAP access to od-sbx-s, where sealed items sit.
    Fix:
    (a) The sealed side builds its own image layer on its own build step. Otherwise, C-transfer code uses different
        test frameworks or runners inside the shared languages, and the brief says so.
    (b) Remove training identities from od-sbx-s IAP after handover and check Cloud Audit Logs at the freeze.

25. Usage has no shed order.
    Seven lanes run Sonnet high in parallel for about 2.5 weeks. "Currently low" is not quantified.
    Fix: record the measured day-1 burn per lane. Pre-register a shed order at 90%: P1 wave, then voice pool, then
    general rows, then the rest. Ping the owner at 96%.

26. Money and the credit relay are not checked early enough.
    - The renewed credit size is unknown (risk 14). The R1 cap ($35) may exceed one account's free credit, and a single
      training run cannot span two accounts.
    - Modal's terms (fetched https://modal.com/legal/terms, "Effective May 2026") put free use under separate "No-Fee
      Use Limitations" that I could not read. Multi-account free-credit use is UNVERIFIED against them.
    Fix:
    (a) Verify the live credit on Sun 1 Nov and raise any money question that day, not at GO #1 on Thu 5 Nov.
    (b) Require the credit on the single training account to be at least 1.25x the measured projection.
    (c) Read the No-Fee terms before relying on the relay.

---------------------------------------------------------------------------------------------------------------------
## LOW

27. SWE-smith problem statements: the plan bars "SWE-smith's LM bugs" but not its issue text, which (from my
    knowledge of the SWE-smith paper; UNVERIFIED this pass) is LM-generated. Fix: bar the problem-statement fields
    explicitly in T57r and P1. Use only gold patches, tests and repos.
28. The CredLeakBench cue list feeds T53, but CredLeakBench is not on the G13 target list. Fix: add it.
29. espeak-ng (GPL) is misaki's OOV fallback inside Kokoro (voice.md section 4), and code identifiers are OOV. Fix:
    treat it consistently with the bashlex rule. Disable the fallback, so our verbalizer handles code tokens, or record
    a tool-only ruling.
30. The new L-0 programs (C2-mix hash export, token histogram, access audit, manifest builder) must skip data/ohs3* and
    ohs3_parts/ in every data/** glob. The plan does not restate this. Fix: add it to every L-0 prompt and to CPU
    tests.
31. Rival weight licences (AgentDoG 1.5-4B, OpenHands critic-4B) are not stated in the plan. Fix: check them (Haiku
    scouting, Opus confirm) before any read.
32. Jev version pinning: fix the OpenRouter model id and the read date, and word claims as "Jev 1.14 as served on
    <date>". If the served model changes before 7 Nov, record it and do not read twice.
33. LibriSpeech confusion harvest: use train splits only (test-clean and test-other are standard eval sets). State that
    Nemotron was trained on LibriSpeech, so the error rates are understated (voice.md, vendor card).
34. Checked, not a problem: Qwen3.5-4B config has num_hidden_layers 32 and full_attention_interval 4, so there are 8
    full-attention layers and 24 linear-attention layers. The plan's "q/k/v/o LoRA touches only 8 of 32 layers" holds.
    Source: https://huggingface.co/Qwen/Qwen3.5-4B/raw/main/config.json, fetched 18 Oct 2026, vendor config.
