# C2.1 PLAN v3.2 SKEPTIC (Sun 18 Oct 2026; fresh Opus 5.5; attacks the v3.2 changes only)

Scope read: C2_1_PLAN_v3.md (header, section 0 item 12, sections 3/4/10/11 v3.2 lines, section 16), C2_1_BUILD_ORDER.md
(whole), PREREG_FINAL.md blocks A61, A77-A82 (read only), C2_1_PUBLIC_TRAIN_INVENTORY.md (grep for licence/provenance
rows), c2_build/c21_infra/split_aware_check.py (code), di_train/DI-TS/SOURCES_DITS_85.json and build_dits.py (to find
the DI-TS inputs). One CPU-only run of split_aware_check.py on four names-only candidate records (scratchpad; no data,
no download, no model).
NOT opened: SEALED_DELTA_v32.md. Its path contains "sealed", and the task's own path rule bars any such path. Its
content is therefore NOT reviewed here; items 9 and 10 attack how it was made and where it sits, not its text. No
ohs/sealed path, OHS5_BRIEF_DRAFT.md, C2 build file, data/, logs/ or ~/.claude was opened.

Severity: HIGH = breaks an owner rule or ruling, or blocks the plan; MEDIUM = likely defect or overrun; LOW = fix in
passing. "VERIFIED" = checked against code or files, not just plan text.

---------------------------------------------------------------------------------------------------------------------
## A. Rule violations and ruling-to-code gaps

1. HIGH, VERIFIED. The A61(a) DI-TS bar is not enforced by name anywhere. A61(a) bars "every source in every DI-TS
   8.5 input" under any id or form. DI-TS is a tasksource subset, and its 8.5 input (SOURCES_DITS_85.json) holds
   three sources: google-deepmind/logical-entailment-dataset, kunalkukreja21/temporal-expressions-evaluation-lm and
   CogComp/perspectrum. split_aware_check.py's A61A_HITS entry "di_ts_inputs" only matches the strings "di ts" /
   "dits", and none of the plan, the inventory or NAMES_MANIFEST_V1.json names the three sources. A CPU run gave
   `perspectrum ALLOW []`. Once A82 2 lets CC BY-SA through (perspectrum is CC BY-SA 4.0), the tool will ALLOW a
   barred source. A82 6 (tasksource per source) sends the scout through about 751 tasksource tasks, which include
   these three.
   FIX: add the three sources (names, hf ids, GitHub ids, tasksource task names, aliases) to A61A_HITS and to the
   manifest v1.1 barred list, each with a CPU test. The conformance record (16.1 step 0) must expand every A61(a)
   group name into its member sources from the 8.5 input files, not only from the plan text.

2. HIGH, VERIFIED. The `--split-scoped-release` code does not carry out A82 1's conditions. It releases a train split
   on split NAMES alone: the requested splits are train-like and do not overlap the registry scope. It takes no G13
   evidence, even though condition (i) says "full-row G13 shows it disjoint", and it writes no "train split seen"
   flag, which condition (iii) requires. This is the A78 pattern: the code is looser than the ruling text.
   FIX: release only when the run is given a G13 result record (result sha, registry sha, method-set version, the
   row count of the full candidate pool, 0 hits or the ruled hit handling of item 3). Write `train_split_seen: true`
   into every released record. Add CPU tests for each of the 3 conditions. Opus signs the conformance map before
   any L-R record exists.

3. HIGH. "Disjoint" in A82 1 is not decided at dataset vs row level, and it decides what block R can contain. Short
   intent utterances (CLINC150, MASSIVE, HWU64, SNIPS) and NLI premises will almost certainly hit their own test
   splits under n-gram methods. Under the literal dataset-level reading, most B2 sets are DENY. Under a row-drop
   reading, we make the subset disjoint ourselves, which may loosen owner words.
   FIX: Opus rules on the literal reading before any B2 record exists, with G13 run over the FULL candidate pool,
   not the capped 1,200 rows. If Opus finds row-drop to be a loosening, B2 sets wait and the question goes into the
   GO #1 packet (a GO point). Until then the strict reading binds, and hit counts per dataset are published either
   way.

4. HIGH. Test splits are needed in the registry, but L-R rule 2 says "only the TRAIN split is downloaded or opened".
   16.1 step 1 registers "the test/dev split of EVERY L-R dataset" (about 80 or more splits). G13 cannot match
   against text it does not hold, so the test splits have to be downloaded by someone.
   FIX: write the exception into rule 2. Test/dev splits are fetched only by the L-0 registry job (a program, run by
   Haiku low) into a registry-only store that the access audit denies to every lane. They are indexed, and their
   shas are logged. No agent reads them, and no L-R builder is given the path.

5. HIGH. The 8.5 schedule conflicts with A61(d) and with the OHS-5 timing.
   (a) Build order L-R "Sun 18-Mon 19: records and readers" comes before the first 8.5 batch on Tue 20. Plan line 462
       says "no generator code that touches a source before that source's pre-mapper PASS", and this is the A61(d)
       breach pattern ("builder code before a valid PASS").
   (b) Pre-mapper passes on Tue 20-Fri 23 run before the OHS-5 export exists (Sat 24). A second run per source after
       the freeze is then a re-run that the form-shopping bar can catch.
   (c) Batching 60-70 sources into group runs needs an explicit reading of "once per stage, on whole fixed inputs".
   FIX: Sun 18-Mon 19 may produce licence records only (URL, quote, date, no downloads, no reader code). Pre-register
   two 8.5 stages per source in one file before batch 1: S-pre (against OHS-3/4/AC exports) and S-post (against the
   OHS-5 export, after the freeze). Fix each batch's membership in advance and never re-run a source within a stage.
   An Opus ruling that this satisfies A61(d) comes before batch 1. Reader code for a source is written only after
   its S-pre PASS.

6. MEDIUM. The no-LLM wording in L-R rule 3 contradicts itself, and the A46 extension has no ruling. Rule 3 says "No
   LLM writes, labels, filters or re-labels a block-R row", but then Claude writes the benign twins in block R, and
   the A46-style screen uses C2 (an LLM) to drop rows. The owner approved A46 for replay human-label rows. Its use
   on block R is a planner extension. It is drop-only, so it is stricter, but it is not covered by the approved text.
   FIX: reword rule 3 to say no third-party LLM-made text or labels, no model labels, and Claude-authored twins only,
   with gold by construction. Record an Opus note that the block-R A46 screen is a stricter, drop-only use. Both
   items go into the conformance record.

7. MEDIUM. Gandalf ignore_instructions fails L-R rule 1 as written. Its rows were picked by an embedding-similarity
   rule, and the card says "a few ... might not be real prompt injections". The label therefore comes from a
   selection rule: it is neither human nor program, which is what rule 1 requires.
   FIX: either record a provenance enum value of "selection-rule", which DENYs it under rule 1, or get an Opus ruling
   that keeps it only behind the A46-style screen with a stated noise disclosure. Gandalf summarization (manually
   reviewed) and Aya are unaffected.

8. MEDIUM. The names guard and the seeded-namespace rule (global order 5, row-start guard (h)) cannot hold for real
   data, and real names threaten C-transfer.
   - Block R and P1 realism rows (CommitPackFT, SWE-Gym, LogChunks, Juliet, CUAD, NQ) contain real tool, language,
     runner, package and entity names. The guard will either drop them in bulk or be bypassed silently.
   - DataDog rows ARE real package names, while T63's gate says "no real third-party package names".
   - C-transfer is defined as names absent from the training manifest. Real names in block R are not in the
     manifest, so they can collide with C-transfer names and contaminate the transfer claim.
   FIX: write a scoped exemption from the namespace rule for L-R and P1-realism rows. Have a program extract the
   tool, language, runner and package vocabulary of every L-R/P1 row into a names-only manifest v1.x before the
   OHS-5 freeze, so the sealed side avoids those names in C-transfer. For DataDog, either swap names through the
   namespace where the label does not depend on the name, or record a T63-gate exception with its reason.

## B. Sealed-side separation

9. HIGH (process; the file itself not opened). SEALED_DELTA_v32.md was written by the same Opus planner who wrote
   the training-side section 16. The new C-block decision types it carries (by plan line 623 and build order L-S)
   track the new training families one-to-one: T59/T60, T63/T66/T67, A3 edit-as-action and the T53 phishing head.
   That brings back the contamination that skeptic 7 removed by retiring the planner-written OHS5_BRIEF_DRAFT. The
   test taxonomy would be shaped by the training design, even at "decision level". The file also sits in the
   training-side c21/ folder, where any c21/* glob will find it.
   FIX: move it into the sealed directory and log the move in the access audit. A fresh sealed Opus re-derives any
   C-block additions from the product taxonomy G1-G8 and public literature, using the delta at most as a list of
   type names. A second fresh sealed Opus reviews it for training detail (row types, sizes, generators, levers,
   families) before the brief is amended. If the review cannot finish by Mon 19 23:59, the delta is dropped and the
   v3.1 brief stands (protects the Sat 24 freeze).

10. MEDIUM. Sealed-readable sections now carry training detail. L-S reads sections 3, 4, the section 10 OWNER-RESERVED
    table and section 11. The v3.2 lines added there expose training design:
    - section 4 PUBLIC-G PANEL: "no block R / block R tiers A+C / plus B2 and A82 sets";
    - section 4 PER-DECISION-TYPE: "ask-or-proceed, control-next, config/migration review";
    - section 11 timeline: "L-R mapping", "8.5 pre-mapper passes for about 60-70 L-R sources", "A46-style screen on
      block-R human-label rows";
    - section 11 MONEY: mix of 112.5K rows, replay 38K.
    FIX: move these lines into section 16, and give L-S a sealed-safe calendar (its own dates, freeze, hard stop, R9)
    in place of section 11.

## C. Money ($30 training cap)

11. HIGH. The cost projection is based on rows while cost scales with tokens, so it is probably low. $0.23-0.25 per
    1K rows comes from C2 mixes. Block R rows run up to an 800-token mean (long-document spans), and A14 (5% at
    1.5-3K tokens) and A15 verbose dialects add tokens without adding rows. Stage A alone can reach or pass $30
    before stage B is even counted.
    FIX: at the Mon 26 pilots (a MEASURED input), compute the projection from the real pilot token histograms times
    C2's measured $/token, and set the shed level then. Do not wait until Thu 29, after 25K block-R rows are built.
    The shed order stays as pre-registered.

12. HIGH. The plan loosens R1's "single training account". A79 R1 (owner words) says "single training account >=
    1.25x projection ... extra accounts only if named". Section 11 re-reads this as the summed credit of the relay,
    citing A81. A81's words covered C2 only.
    FIX: the strict reading binds. One account's live credit must be at least 1.25x the measured projection, so about
    $24 or less if the renewed credit is $30 (verify the renewal amount and time on 1 Nov). The summed-relay reading
    goes into the GO #1 packet as an owner question. The shed order targets min($30, single-account credit / 1.25).

13. HIGH. Drop R15. It asks the owner to name about four more free Modal accounts so October leftovers can be
    pooled. That is multi-accounting on a free tier, and Modal's No-Fee terms are still UNVERIFIED. By the plan's own
    arithmetic, the full mix does not fit even with every account.
    FIX: remove R15 from C2.1. The relay rule stays exactly as A79 R1 says, and only if the Wed 21 No-Fee terms check
    clearly allows it. The stretch gains only an earlier data freeze (training stays Sun 1 Nov or later on renewed
    credit).

## D. Gates that cannot run at generation time, and the confirming pass

14. HIGH. A confirming G13 in 1 hour or less is not credible as a full pass. C2's binding G13 took 8-10 h on a
    55-75K-row mix. The v3.2 mix is about 112.5K rows, and the registry grows by about 80+ test/dev splits, every
    L-R split, the OHS-5 export, the public-G panel and the probe items. A full every-method pass will take many
    hours.
    FIX: define the confirming pass in the conformance record as:
    (a) a stamp audit: every row's stamp is current for the final registry sha, method-set version and generator
        code sha;
    (b) a full re-run of the exact and hash methods on every row;
    (c) the fuzzy methods only on delta targets.
    Size the Wed 21 throughput test with the FINAL-size registry and block-R-length rows. Any hit in the confirming
    pass stops the mix: that family or dataset is re-stamped whole, and the service gets a skeptic re-check.

15. MEDIUM. Not every G13 method can run against OHS-5. A salted hash export supports exact and hashed n-gram
    matching only; sentence and fuzzy methods cannot run against hashes, so "EVERY method against EVERY target"
    (16.1 step 2b) is false for OHS-5. The plan also does not say which salt the stamp service uses. If it is the
    sealed salt, it contradicts "the sealed salt never leaves L-S".
    FIX: list the methods per target in the registry. Use a separate hash-export salt (not the namespace salt),
    given only to the matcher process. Have the sealed side's reverse check (counts only) cover what hashes cannot.

16. MEDIUM. The read-twice switch breaks R6's sha binding. Adopting it on Sat 24 at 18:00 gives a new scaffold sha.
    A79 R6's exemption is "sha-bound" to the approved scaffold, so the new scaffold is not covered by owner words.
    The S1 parity record and the format exposure probe would also need re-running within 6 hours.
    FIX: adopt only if a program shows the new scaffold is the same exempted strings repeated, with no new
    scaffolding text, and Opus records that. Otherwise read-twice is not adopted in C2.1 and goes to C2.2.

## E. Lanes and timeline

17. HIGH. The lanes are overloaded on the critical path to Sun 25.
    - L-0, one Sonnet builder, carries the v3.1 items (a)-(n) plus: the stamp service, the wrapper, the replay
      clean-up, the mix guard, about 80+ registry splits, manifest v1.1, tools A1/A2/A15/A19-A21, and 12 or more
      conformance maps.
    - L-R must deliver 60-70 datasets in about 5 days, each needing a record, an Opus recast table, a mapper, a
      skeptic, two 8.5 stages, the A46 screen and set-level checks.
    - L-A carries 3 families, 7 levers and a new head, and also exports its state model to L-K.
    - The orchestrator alone runs every 8.5, reads the daily fix triggers and verifies every number.
    - The Mon 19 Opus batch holds about 14 G0-lites, 6 addenda and the v1.1 freeze.
    FIX: split L-0 into L-0a (sandbox and images) and L-0b (stamp service, wrapper, mix guard, registry), each with
    its own builder. Conformance maps go to separate fresh sessions. Pre-register the L-R order by source group;
    after batch 1, the MEASURED time per source decides whether a second L-R builder starts (no cut by estimate).
    Batch the Opus recast-table approvals per source group.

18. MEDIUM. The stretch timeline is unrealistic and costs orchestration effort. There are 5 days from the first row
    (Sun 25) to the Fri 30 freeze with one combined fix, while 8.5 batches run until Thu 29 and the L4 queue is full.
    The plan itself says training on 30-31 Oct is unlikely.
    FIX: keep only the Thu 29 declaration ("early freeze if measured status allows"). Add no work items for the
    stretch and remove R15 (item 13).

19. MEDIUM. Late sources conflict with the closed allow-list. Manifest v1.1 freezes Mon 19, but tasksource sources
    are promoted from Tue 20 and tier-C "waiting" sets "enter by default when confirmed". Each late source needs a
    new manifest version, AND it must reach the sealed side's R5 list before the OHS-5 freeze, or sealed G may
    contain a source we train on.
    FIX: last addition by Fri 23 12:00 (v1.2 at most), passed names-only to L-S the same day for the G re-check.
    Later sources roll to C2.2 (logged). Humicroedit (Reddit-sourced headlines) and NLI4CT each get an A82 4 check
    before they enter.

20. MEDIUM. Block R can starve sealed G. Every one of the 60-70 L-R sources and their siblings leaves the sealed G
    pool (25 or more sources, about 10K items), and the public-G panel takes further unseen sets.
    FIX: by Tue 20 the sealed side reports only the surviving source COUNT and reachable item count (no names). If
    it is under 25 sources or 10K items, R7/R13 apply as A79 decided, and the owner is told that day, before L-R
    rows start.

21. MEDIUM. Usage burn is not measured. v3.2 adds 3 lanes and many sessions (Sonnet high and Opus sign-offs), but no
    day-1 burn is measured yet.
    FIX: launch L-R/L-K/L-P only after the measured per-lane day-1 burn gives a weekly projection under the 90% shed
    line. Shed order as written; ping the owner at 96%.

## F. Missing kill and stop rules

22. HIGH. No rule covers the stamp service missing its date. By the owner rule, rows cannot exist unstamped, yet
    nothing says what happens if the service is not signed off or too slow.
    FIX: if the service is not signed off by Sat 24 18:00, row jobs wait (no unstamped quarantine pool). The
    freeze date does not move, and the kill rule and the floor apply to the lost days. A second-host ruling is made
    by Wed 21, from the full-registry throughput.

23. MEDIUM. Further kill and stop rules are missing:
    (a) L-R datasets have no G13 drop trigger. The 1% rule assumes a generator to fix. Rule: over 1% stamp drops
        (outside exemptions) goes to Opus; over 5% means the dataset is left out (logged).
    (b) Conformance records have no deadline. Rule: a record type whose conformance map is unsigned at Sat 24 18:00
        starts no rows.
    (c) Replay below its count. Cleaning against about 80 new targets and OHS-5 may leave fewer than 38K clean replay
        rows. Rule: use all clean rows; never refill with unclean or unread rows; record that the count shrank.
    (d) R4 vs the 18 Oct owner rule. Record that A79 R4 (OHS-AC report-only on replay) is the specific ruling and
        stands, and that "clean" means drop for every binding target. Opus notes this in the conformance record.

## G. Smaller items

24. LOW, VERIFIED. The plan's "known items to fix" are partly wrong. split_aware_check.py already allows
    CDLA-Permissive-2.0 (CPU run: `FinQA ALLOW []`). The CC BY-SA refusal claim is right (`SNLI DENY
    LICENCE_NOT_PERMISSIVE`). The tool's docstring still says "G13 pilot". row_start_guard v1 does not check the job
    family field (NAMES_MANIFEST_V1 note).
    FIX: build conformance maps from the code, not from plan text. Add the family check, and add T59, T60, T63, T66
    and T67 to row_job_families_allowed in v1.1.

25. LOW. Span selection can create a shortcut. In L-R rule 4, the gold-bearing span is always included alongside
    distractor spans, so position or length can give the answer away.
    FIX: add a set-level span-position/length probe per long-document dataset (AUC <= 0.55).

26. LOW. Licence and provenance details:
    - tasksource per-source records must quote the UPSTREAM licence, not tasksource's card (its rows include
      cc-by-nc-4.0 and BY-NC-SA).
    - CommitPackFT and SWE-Gym need per-repo code licence checks.
    - Plan 16.3 should state that T57r negatives come only from our own mutator and never from SWE-Gym agent
      trajectories or patches (the inventory says so; the plan does not).
    No NC or GPL dataset was found among the named block-R licence quotes I checked.

27. LOW. Kept as fine: the A82 4/5/9 exclusions are carried correctly; the voice R11 handling is right; P0 sizes are
    never shed; there are no Modal or model calls before GO #1.
