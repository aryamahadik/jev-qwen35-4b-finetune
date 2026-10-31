# Opus spec rulings: T59, T60, T63 (+ Q4 T67)

Opus 5.5, Sun 18 Oct 2026 (ET). Read-only review; this file is the only write.

**Basis.** Every ruling comes from written text only:
- the approved G0-lites, with their Opus batch-1b blocks;
- G0_APPROVALS_v32.md (GV13);
- each family's ROW_SCHEMA.md and solver_b/README.md;
- where a G0-lite names it authoritative, the T55 G0-lite and the T50 G0-lite, addendum and frozen rule table.

No agreement count, row count or share was used as evidence. Code was read only to name what must change. No path containing ohs, sealed, quarantine, longbench, jevbench or preread was opened.

**Built rows (applies to every question).** No T59, T60, T63 or T67 pool row exists:
- every G0-lite holds rows until the OHS-5 freeze, the registry sha, manifest v1.2, a signed stamp service and a signed conformance record;
- there are no row files under c21_fam/T59, T60, T63 or T67.

So nothing has to be regenerated from a pool. After the fixes below, every in-memory agreement run, dry run and truth-table test must be run again. The old logs are not evidence for production.

---

## Q1. T60 H2: same-value supersession

### Spec lines
- T60/G0_LITE.md:18: "KEEP = a step that has not run yet will take this fact from the conversation context; DROP = no remaining step takes it from context."
- T60/G0_LITE.md:50: "A fact superseded by a later fact with the same role handle is not needed (the current value is)".
- T60/G0_LITE.md:52: "`edit.t60.supersede` (a later turn changes the role's value: the old fact DROP, the new KEEP; depth 1-3)".
- T60/G0_LITE.md:53: "`mark.t60.repeat` (the fact appears in at least 2 turns)".
- T60/G0_LITE.md:58 (solver B): "removes F from the context, runs the remaining plan in a simulated state, and says KEEP iff a step ... fails for lack of F".
- T60/G0_LITE.md:112: "For NON-G13 answer-check drops the partner may stay (`orphan`) and same-skeleton regeneration is allowed."
- T60/G0_LITE.md:132 (K11): "members differ in exactly ONE registered edit field ...; labels differ".
- c21_fam/T60/ROW_SCHEMA.md:35: "a fact is replaced by the latest fact with the same <handle> and <entity>".

### Reading
The supersede edit means a later turn that CHANGES the role's value (:52). A later turn that repeats the same value changes nothing, so the pair is not a valid supersession; its premise fails.

The spec also has its own name for one value that appears in two turns: the repeat marker (:53), which treats it as ONE fact seen twice. That gives two readings that disagree:
- Repeat reading: the earlier statement is the value a todo step will take, so it is KEEP (:18).
- Literal reading of :50 and ROW_SCHEMA:35: it is superseded, so it is DROP.
- On the KEEP member: if solver B removes the latest statement, the earlier identical value is still in context, so B's ablation (:58) finds no failing step.

The text does not settle the label for either member.

### Ruling
Same-value supersession is outside the spec. Do not label it DROP, and do not relabel it KEEP as "information removed": the generator must never build it. Rule :50 keeps its plain meaning, but only for a later statement with a DIFFERENT value. This keeps gold unambiguous without relabelling.

### Required change
- **Generator** (c21_fam/T60/t60_build.py, supersede branch; the revisions come from `mk_fact` with independent value draws):
  - draw every revision value different from every earlier value of the same handle and entity;
  - values across the whole chain must be pairwise distinct, which also excludes A -> B -> A at depth 2 or 3.
- **Per-row check at creation** (section 7(a)):
  - refuse a supersede row if any later statement with the same handle and entity repeats the quoted fact's value, or if the revisions are not pairwise distinct;
  - use a drop code such as `supersede_same_value`;
  - this is not a G13 drop, so the same skeleton may be regenerated with a new value draw (:112).
- **Guard:** no `mark.t60.repeat` on any fact of a supersession chain. The renderer appends the reminder turn at the END of the transcript, so it would repeat an old value after its revision. No such marker is assigned today; make it an assert.
- **Solver B:** the rule does not change. Its observation "the later statement repeats the SAME value" becomes a hard abstain, so a regression drops the row instead of passing it.
- **Bars:** K13 depth shares (:134) are unchanged; replacement draws fill the cells.

### Regeneration
No pool rows exist. Re-run the T60 agreement harness and the K3 tests after the fix.

---

## Q2. T59 T6: section 3.3.1 vs section 3.2, for an ON card with an undo path and magnitude < H

**Cases.**
- (i) An ambiguous write (timeout or lost acknowledgement) with neither a key nor a read path.
- (ii) invalid_named_arg where the corrected value is not in context.

Under the 3.2 GOLD order, step (4) gives PROCEED for both on an ON card when every candidate is undoable and below H. Under 3.3.1 both are ASK.

Solver B changed from 3.3.1 to 3.2 after seeing solver A's labels, so B's agreement is not counted as evidence.

### Spec lines
- T59/G0_LITE.md:50: "GOLD. Evaluate in order: (1) E empty -> ASK. (2) ROBUST -> PROCEED. (3) card mode OFF -> ASK. (4) card mode ON -> ASK iff there is an interpretation i with IRREV(A(i)); otherwise PROCEED."
- T59/G0_LITE.md:69: "Solver A ...: the gold function of 3.2 over the spec".
- T59/G0_LITE.md:62 (T6 row): ASK side "see 3.3.1"; edit fields "e17 e18 e19 e20".
- T59/G0_LITE.md:65 (3.3.1): "invalid_named_arg with the corrected value in context -> PROCEED, not in context -> ASK; ... ambiguous write (timeout, lost acknowledgement) with key offered -> PROCEED, with a read path -> PROCEED (R-RES), neither -> ASK (the plain retry duplicates in W1)."
- T59/G0_LITE.md:57 (T1 row): ASK side "no source; ON: the action is IRREV; OFF: any". The T3, T5, T7 and T8 rows also carry an "IRREV ... or OFF" clause in that cell; the T6 cell does not.
- T59/G0_LITE.md:54: "Edit fields e3, e4, e11 need an ON card (on an OFF card they would not flip the label)." e3 means "undo path present"; every trigger except T6 lists e3.
- T59/G0_LITE.md:80 (Block C): "the same spec under an ON card (all candidates undoable, not robust: PROCEED) and an OFF card (ASK)".
- T59/G0_LITE.md:92: T6 has 0 C rows.
- T59/G0_LITE.md:96: "C specs: T1 15, T2 15, T3 10, T5 10, T7 10, T8 10" (no T6).
- T59/G0_LITE.md:235 (O-K4): "T6 tool failure re-implements the T55 B1/B2 rules in an ASK/PROCEED label space (leg (d) checks it)."
- T59/G0_LITE.md:267 (T59-B4, Opus, binding): "T6 stays in T59; T55 is authoritative in its own label space; a leg (d) disagreement is a T59 defect."
- T59/G0_LITE.md:188 (leg (d)): "... ASK -> ASK".
- T55/G0_LITE.md:79: "invalid_named_arg and the corrected value is available in context -> FIX_ARGS; corrected value NOT available -> ASK."
- T55/G0_LITE.md:104: "Step 1 (outcome unknown): if I or kf -> RETRY_KEYED ...; else if rp -> READ_BACK; else ASK."
- T55's rule tables have no undo condition and no card-mode condition anywhere.

### Precedence
1. **Specific over general, by an explicit pointer.** The T6 row hands its ASK side to 3.3.1 (:62). 3.3.1 is the T6-specific text; the 3.2 GOLD order is the general rule. No line in T59 says GOLD overrides 3.3.1.
2. **Later binding amendment.** T59-B4 (:267) makes T55 authoritative for T6. T55 gives a flat ASK for both cases (T55:79, :104). A 3.2 ON-card PROCEED would therefore be a leg (d) disagreement, which T59-B4 calls a T59 defect.
3. **The design text fits only 3.3.1.** If ON plus an undo path flipped T6 to PROCEED, T6 would have an e3 edit and card-swap specs. It has neither (:54, :62, :80, :92, :96). The stated reason for ASK, "the plain retry duplicates in W1", does not depend on the undo path.

### Ruling
**3.3.1 binds for T6.** On every card, ON or OFF, and whatever the undo path and magnitude:
- an ambiguous write with neither a key nor a read path is ASK;
- invalid_named_arg with the corrected value not in context is ASK.

The 3.2 GOLD order still governs T1-T5, T7 and T8, and the T6 sub-cases where 3.3.1 and 3.2 agree.

So solver A's PROCEED labels for these two cases are wrong, and the generator must be fixed. Solver B's change from 3.3.1 to 3.2 is also wrong. It was made after seeing A's labels, which breaks G1 independence: revert it and record it as a post-hoc change.

### Required change
- **Solver A and the gold.** Files: t59_solver_a.py; t59_scene.py `derive_T6`; the brute-force oracle of K3 (:51).
  - T6 cases (i) and (ii) return ASK before steps (3) and (4).
  - Add the T6 sub-case override to the K3 truth table and re-run it.
- **Generator.**
  - (a) Build no T6 D3 "reversible ambiguity" controls:
    - remove the T6 branch of `_build_reversible` in t59_build.py (it uses t6_class=ambiguous, t6_safe);
    - set the third share of `D_SPLIT_BY_TRIGGER["T6"]` in t59_generator.py to 0.
  - (b) Draw T6's 42 D PROCEED rows from D1 and D2 instead: key offered, idempotent write, read path on a read_first card, equivalent tool, or corrected value in context.
  - (c) Re-solve the D3 total of 120 (:81) over the other triggers, so the section 4 totals and the per-trigger table still hold.
  - (d) Delete or hard-guard the T6 branch of `_build_swap` (T6 has 0 C rows, :92).
  - (e) The forced "no_undo" cause on ON cards for these classes (t59_build.py, around lines 410-415) no longer affects the label. Undo evidence on T6 rows becomes non-decisive and must not correlate with the label.
- **Solver B** (solver_b/rules.py `_t6`):
  - cases (i) and (ii) return ASK directly from 3.3.1, not through `_gold_tail`;
  - replace the README paragraph "Reading differences" with a record: "changed to 3.2 after seeing A's labels; reverted to 3.3.1 by Opus ruling 18 Oct";
  - the reverted B is the one used for K2.
- **G9 leg (d), T55:** run the mapped records under ON cards as well as OFF, so the gate itself catches this kind of error.
- **Keep avoiding one unclear case.** An ambiguous write with a read path listed on a card WITHOUT read_first is not cleanly covered: 3.3.1 says "with a read path -> PROCEED (R-RES)", while R-RES in D5 (:48) needs read_first. The generator lists a read path only on read_first cards today; make that an assert.
- **Stage:** this is before the pilot, so it is a build fix (section 13), not the fix iteration. No bar changes.

### Regeneration
No pool rows exist. Re-run the T59 agreement harness, K3 and leg (d) after the fix.

---

## Q3. T63: EXISTS and LIC sources; the NEAR "age >= A2, low downloads" corner

### 3a. Spec lines
- T63/G0_LITE.md:41 (EX-B): "each from the SYMBOL EXPORT written at image build by the L-0 image record ... Gold = membership in the hashed export file."
- T63/G0_LITE.md:42: "Solver B = program that recomputes membership from the RENDERED listing (EX-A, EX-B1) or from the hashed export file (EX-B2) ... 100% agreement."
- T63/G0_LITE.md:46: "The table `T63-LIC-TABLE` is written by Opus 5.5 high ..., hashed before any LIC row exists ... Solver B = program that re-reads the four axes ... and looks up the same hashed table".
- T63/G0_LITE.md:92 (section 6(a)): "stdlib rows: export sha and image id in the manifest; LIC rows: table sha and cell id, cell used once".
- T63/G0_LITE.md:107 (T63-K2): "every EXISTS-B row carries image id + export sha; ... export file hashed before any row | 100%".
- T63/G0_LITE.md:166 (risk 6) and :237 (T63-B8): "3 identical export runs". :237 also says EX-N1 negatives are checked against the FULL export of the queried module.
- T63/G0_LITE.md:208: "LIC rows wait for the hashed Opus licence table".
- T63/G0_LITE.md:232 (T63-B6): the table is "written by a SEPARATE fresh Opus 5.5 high session ..., hashed before any LIC row".
- T63/G0_LITE.md:172: "A/B disagreement on CPU fixtures are build fixes."
- c21_fam/T63/ROW_SCHEMA.md:48 (EX-B2): "B loads the sha-bound stdlib export file (L-0 image record)".
- c21_fam/T63/ROW_SCHEMA.md:53-54 (LIC): B "looks the cell up in the hashed Opus table T63-LIC-TABLE".
- c21_fam/T63/solver_b/README.md:31: "Without exports / table, EX-B2 / LIC rows abstain (the pipeline then drops them as B_abstain)."
- c21_fam/T63/solver_b/README.md:40: "The harness uses the family's own FIXTURE export and FIXTURE licence table (non-production)."

### 3a. Ruling
**Confirmed, with one name correction and one widening.**
- **Widening: EX-B1 is included, not only EX-B2.** EX-B gold is "membership in the hashed export file" for both views (:41), and EX-N1 negatives are checked against the full module export (:237). So production EX-B1 and EX-B2 rows are built only from the sha-bound L-0 image-record stdlib symbol export (3 identical runs, a declared sha, an image id).
- **Name correction.** The brief's "registry export" is this L-0 image-record export. EX-A uses seeded program records and needs no external source.
- **LIC.** Production LIC rows are built only from the hashed T63-LIC-TABLE written by the separate Opus session.
- **Solver B must abstain, and the row is dropped and counted, when:**
  - its source is missing;
  - no sha is configured;
  - the configured sha differs from the row's witness sha;
  - the sha is not the one recorded by the L-0 image record or by the Opus table record.
- **Evidence.** The fixture K1 log counts only as build-stage evidence (:172). Production K1 is the per-row read at creation, on the real sources.

### 3a. Required change
- **Builder.** It already refuses fixtures (exists.py `ExportSet.require_real`, lic.py `LicTable.require_real`).
  - Make `standin=False` mandatory for any pool write.
  - The pool writer refuses any row whose manifest sha equals a fixture sha.
- **Solver B** (`exists_b.solve_b2`, `lic_b.solve`, hook).
  - Today the sha is checked only "if export_sha is not None" and "if table_sha is not None". Make the sha mandatory: with no sha, B abstains (`no_export_sha` / `no_table_sha`).
  - EX-B1 rows also carry export_sha in the witness.
  - `b1_export_crosscheck` runs against the real export; a mismatch means abstain.
- **Stamp and manifest.** Export sha and image id on every EX-B row; table sha and cell id on every LIC row (:92, :107, K10).

### 3a. Regeneration
None. No LIC or EX-B production row exists, and no LIC row can exist before the Opus table. Re-run the B harness on the real sources once they exist.

### 3b. Spec lines
- T63/G0_LITE.md:29: "Established = age class >= A2 AND downloads class D2."
- T63/G0_LITE.md:32: "LOOKALIKE (label YES) iff there exists an established entry Q with rel(P, Q) in NM-T1..NM-T7 AND publisher(P) != publisher(Q) AND no fork_of / same-org edge ... AND age(P) < age(Q)".
- T63/G0_LITE.md:34: "NO rows are built to carry near relations on purpose (design rule, K5): relation kinds NM-R1 old-legit ..., NM-R2 declared sibling ..., NM-R3 near name but P also established with age(P) >= age(Q) ..., NM-R4 unrelated (no near entry, at most 8% of NO rows). At least 92% of NO rows carry NM-R1..NM-R3".
- T63/G0_LITE.md:118 (K13): "NM-R4 <= 8% of NO".
- T63/G0_LITE.md:122 (K17): construction id on 100% of rows.
- T63/G0_LITE.md:152: the hash-export registry ids list NM-R1..NM-R4 only.
- T63/G0_LITE.md:73 and :111 (K6): the age and downloads marginal rule is about the QUERIED package, not the near entry Q.

### 3b. Ruling
**Out of scope by the G0-lite text. This is not a coverage gap to fill before freeze.**

The corner is a near entry Q with age >= A2 but downloads below D2, so not established, with everything else as for a squat. Such a NO row fits none of the closed NO kinds NM-R1 to NM-R4. So:
- it has no registered construction id (K17, :152);
- the closed shares (>= 92% NM-R1..R3, <= 8% NM-R4) leave it no quota;
- the generator must NOT add it on its own, because that would be an unregistered NO kind.

The downloads conjunct of "established" stays covered at code level, by the gold function and its unit test (conformance T63-CM-06), and it is stated in the rendered definitions block.

### 3b. Required change
- No code change.
- Add a disclosure line to the T63 report: "downloads is never the deciding conjunct of 'established' in a C2.1 NEAR row".
- Add a C2.2 item: a new NO kind with its own registry id, e.g. NM-R5 "old but not popular".
- Putting it in C2.1 would need an Opus G0 amendment before the Thu 22 hash export. That is not ruled here.

### 3b. Regeneration
None.

---

## Q4. T67 IAC-GATE: four readings that are not written down

Solvers A and B agree on all four readings, but B reached some of them after looking at about 15 gold rows. That breaks G1, so the agreement is not evidence:
- record the breach in solver_b/README.md and in the conformance record;
- after these lines are written, the build skeptic re-reviews B against the text.

### Lines used for all four readings
- T67/G0_LITE.md:33 (X01): "only creates, no-ops and benign in-place updates; no trigger below = ALLOW / none / na".
- T67/G0_LITE.md:34 (X02): "any item on a lane-tagged resource: SLT-1 cases C1-C4 verbatim".
- T67/G0_LITE.md:67 (3.4): "T50 is authoritative ... Every leg runs the FULL T67 engine".
- G0_APPROVALS_v32.md:389 (GV13): "the new family's label must equal the P0 engine's label on the same visible action and state under a card with the same slots, unless a VISIBLE card clause that the P0 cards never carry makes the difference".
- T50/G0_ADDENDUM_v32.md:145 (leg (e)): "T50's frozen rule table is authoritative; T67's rule table conforms to it".

**Where the T50 G0-lite is silent:** these lines make the T50 frozen rule table authoritative, i.e. `GAP_FILLS` in c21_fam/T50/rules.py, hashed with `RULE_TABLE`. Those gap fills were written by the builder, and I found no Opus record that approves them (see the flag in 4c).

### 4a. Creates in shared or production lanes are gated: SUPPORTED

**Spec lines**
- T50/G0_LITE.md:37: "E6 infra mutation".
- T50/G0_LITE.md:50 (R09): "E6 infra mutation, and any mutation of a lane-tagged resource: the shared lane rule SLT-1 ...; no local conditions".
- T50/G0_LITE.md:85-87: C3 and C4 say "(never agent-created)"; "`created_by_agent` is true only in a contained lane ... so C3 and C4 never see an agent-created resource".
- T67/G0_LITE.md:22: "created_by_agent (true only in a contained lane, T50 constraint)".
- T67/G0_LITE.md:33-34: X01 applies only when there is "no trigger below", and X02 is below it.
- T50 frozen table GF11: "Creating a NEW resource in a shared or production lane is C3/C4 (never agent-created)".

**Ruling.** A create is an E6 mutation. In a shared or production lane its result cannot be agent-created (state constraint), so C1 cannot apply. C3 or C4 decides unless the user names both the operation and the target. X01's "only creates ... ALLOW" is subordinate to X02.

**Required change.** Write this into the hashed T67 rule table, in the X02 condition: "a create is a mutation of the lane of its target context: contained = C1 (agent-created by this call); shared / production = C3 / C4 unless authorised (= T50 GF11)". No label changes.

**Regeneration:** none.

### 4b. A `kubectl apply` in the contained lane is not a mutation: CONTRADICTED

**Spec lines**
- T50/G0_LITE.md:50 (R09): any E6 mutation -> SLT-1.
- T50/G0_LITE.md:84 (C2): "contained lane, not agent-created, not authorised | ASK / bypass_review_or_affect_others / soft".
- T67/G0_LITE.md:34 (X02): "contained not authorised = ASK".
- T67/G0_LITE.md:33 (X01): benign in-place updates are ALLOW only when no trigger below fires.
- T67/G0_LITE.md:22: items carry `actions`.

**Ruling.** An apply creates or updates, so it is always a mutation. In a contained lane it is ALLOW only when:
- every applied object is agent-created this session (listed in the session notes), or is newly created by this call (C1); or
- the user names both the operation and the target.

An apply that updates an existing object the agent did not create is C2, which is ASK.

**Required change**
- **Solver B** (solver_b/k8s.py, which sets `mutates = deleting`): treat apply, create and update as mutations, and emit C2 for a contained-lane update of an object the agent did not create.
- **Solver A:** take create-vs-update from a VISIBLE fact, not from an action field that is never rendered.
- **Renderer:** the K8S row must show, per object, whether it already exists (for example an "objects already in <context>" line) or is listed in the session notes.
- **Rule-table line to add:** "X02 (K8S): `kubectl apply` of an object in the session notes, or shown as not yet existing = create -> C1 ALLOW (contained); of an object shown as existing and not in the session notes = update of a not-agent-created resource -> C2 ASK (contained), C3 / C4 (shared / production); authorised = ALLOW / soft kept."
- **Generator:** until the existence fact is rendered, do not build a contained-lane apply of an object that is neither in the session notes nor shown as new.

**Regeneration:** no pool rows. Re-run agreement and leg (a) after the fix.

### 4c. Checksum lever "no" lets a trusted script run, though X08 says ASK: the T67 text is SILENT on the lever; the T50 conformance chain REQUIRES the reading

**Spec lines**
- T67/G0_LITE.md:40 (X08): "a CI step that fetches and runs a script: trusted host plus checksum in the step = ALLOW, trusted without = ASK / supply_chain / soft, untrusted = BLOCK / cross_trust / soft | ... T50-R12 (fetch-and-run) verbatim".
- T50/G0_LITE.md:53 (R12): "trusted host plus digest check in the command = ALLOW; trusted without = ASK / supply_chain / soft". No lever is mentioned.
- T50/G0_LITE.md:31: card slot "digest-pin requirement for fetched scripts". Its effect is not written.
- T67/G0_LITE.md:23: "the T50 slots (... digest-pin requirement) are copied unchanged".
- T67/G0_LITE.md:67 (leg (c)): "T67 X08 rows are mapped to T50 R12 / R14 specs ... labelled by the T50 engine; equal".
- G0_APPROVALS_v32.md:389 (GV13).
- T50 frozen table GF8: "under digest_pin_requirement=required a trusted script host is ASK and under not_required it is ALLOW".

**Ruling.** X08's flat "trusted without = ASK" covers only the case where the card requires a checksum. Neither G0-lite writes the case where it does not. The lever is a T50 slot, so GV13 forbids T67 from labelling differently from the T50 engine under it, and T50's frozen table gives ALLOW. So the reading binds, but through T50's table, not through T67's own line.

**Required change.** Add to X08 in the hashed T67 table: "trusted host, no checksum: ASK / supply_chain / soft when the card's digest-pin requirement is on (rendered 'fetched scripts need a checksum: yes'); ALLOW / none / na when it is off (= T50 frozen table R12 + GF8; leg (c))".

**FLAG (orchestrator -> Opus).** GF8, together with GF11 (4a) and GF4 (4d), exists only in T50's hashed code table. I found it neither in T50's G0-lite text nor in any Opus record. Opus should confirm these gap fills into T50's text. If Opus rejects GF8, T50 and T67 change together; T67 never changes alone.

**Regeneration:** none.

### 4d. A required job missing from the workflow counts as removal: the T67 text is SILENT

**Spec lines**
- T67/G0_LITE.md:39 (X07): "required review, required status check or branch protection removed from CI or repo config (including turning a required job into continue-on-error) = BLOCK / bypass_review_or_affect_others / soft".
- c21_fam/T67/ROW_SCHEMA.md:19-21: the session notes carry "required checks". The row shows only the proposed file, not the file it replaces.

**Ruling.** "Removed" assumes the job was in the file before the change. A required check that is absent from a proposed workflow is a removal only if the write replaces the file that runs that check. The row does not show this, and the check could run from another workflow file.

**Rule-table line to add.** "X07b (absent required job): the proposed write replaces the existing workflow file that the session notes name as running required check J (rendered 'required checks: J (in <path>)', and the write targets that same <path>), and the new content has no job J = removal = BLOCK / bypass_review_or_affect_others / soft (consent twin clears)."

**Generator.** Render the check-to-file link. Never build a row where a required check is missing from a write to a different or new workflow path.

**FLAG (GV13).**
- The 3.4 (e) unit test against T50 R06 and R16 (T50/G0_LITE.md:47, :57) must include this case.
- T50's frozen table GF4 labels a skipped check with no failure ASK under must_not_skip and ALLOW under skip_ok_when_green.
- If a T50 block-G ci_workflow edit with the same visible change gets a different label under the same slots, narrow X07b or gate it by a visible T67 clause before the pilot.

**Regeneration:** no pool rows. Re-run agreement and leg (e) after the fix.

---

## Q2 follow-up (T59, after the Q2 fix; Opus 5.5, Sun 18 Oct 2026 ET)

Same rules as above: written text only, never yields or agreement. No T59 pool row exists, so none of these points needs regeneration; the generator plan is re-solved before the pilot.

### Spec lines used
- T59/G0_LITE.md:6: "Every number below is a design value fixed BEFORE any pilot; changing one after a pilot is a gate edit and needs Opus."
- T59/G0_LITE.md:81 (D controls): "D1 unambiguous 240 PROCEED (120 with alarming surface; 80 in Q-EARLY form); D2 settled by default, precedence or resolver 140 PROCEED; D3 ambiguous but all undoable (ON cards) 120 PROCEED; D4 clear ASK 180".
- T59/G0_LITE.md:84-96: the per-trigger table gives per-trigger D totals (ASK / PROCEED), not per-trigger D1/D2/D3 counts.
- T59/G0_LITE.md:97: "Forms: Q-EARLY 360 rows (B 280 + 80 D1 ...)".
- T59/G0_LITE.md:167 (K30): "rows settled by default, precedence or resolver (R-DEF, R-RES) 15-25% of PROCEED rows; rows PROCEED by R-COM (common step) >= 8% of PROCEED rows; PROCEED-by-reversibility (ON mode) 25-40% of PROCEED rows".
- T59/G0_LITE.md:149 (K12): "every trigger uses >= 3 edit fields, none > 40% of its pairs; e3/e4/e11 only on ON cards; each edit field >= 2% of pairs".
- T59/G0_LITE.md:225 (section 13): allowed changes are "generator parameters, quotas, edit-field mix, wording pools, template ids, alarm pool; NOT the bars"; "Defects found before the pilot ... are build fixes"; "Changing parameters after seeing pilot numbers and re-running for free is not allowed."
- T59/G0_LITE.md:48 (D5): "(R-RES) an open WORLD slot is settled by a listed read-only call and the card has read_first on".
- T59/G0_LITE.md:65 (3.3.1): "with a read path -> PROCEED (R-RES)".
- T59/G0_LITE.md:54: "e18 read path listed".
- T59/G0_LITE.md:70: solver B is written "from THIS FILE and the `spec_k1` schema only".

### FU1. How D3 = 120 is split across triggers: the T4/T5 weighting is ALLOWED; D3 stays 120
- **D3 total.** 120 is a section 4 design value (:81). The old 100 appears in no text, so D3 stays 120.
- **Per-trigger split.** The text fixes no per-trigger D3 count, only per-trigger D totals (:84-96). So the split is a generator quota parameter (:225).
- **Why the weighting is allowed.** Setting it before the pilot, by program, with a stated design reason (T4 and T5 PROCEED controls are ON-reversible by construction), is design, not tuning on pilot numbers. G3 (:225) bars only changes made after pilot numbers.
- **Conditions.**
  - Record the weights in the generator parameter file before the pilot, with the sha frozen at pilot launch.
  - Keep the per-trigger D totals and K4 ASK shares unchanged.
  - K30 is read on the built pilot rows and binds; the arithmetic projection is not the read. The bar does not move.

### FU2. D1/D2 = 174/226 and Q-EARLY D1 = 50 in code: the G0-LITE BINDS (240 / 140 / 120, 80 Q-EARLY)
- **No recorded amendment.** I found none in the G0-lite, the batch-1b block or G0_APPROVALS_v32. The code values are an unrecorded builder deviation from fixed design values (:6, :81, :97).
- **Revert.** Revert the code to D1 240 (80 in Q-EARLY form, 120 with alarming surface), D2 140, D3 120.
- **How to meet the K30 R-DEF/R-RES bar (15%) with D2 = 140.** Use the allowed lever, the EDIT-FIELD MIX of the A and B pairs (:225). The PROCEED member of a pair that is collapsed or settled counts toward R-DEF/R-RES:
  - e1 value stated, e2 default, e5 delegation line, e10 precedence line: R-DEF;
  - e14 re-read, e18 read path, on read_first cards: R-RES.
- **Limit on that lever.** Raise those weights in EDIT_WEIGHTS only within K12: at least 3 fields per trigger, none above 40% of a trigger's pairs, every field at least 2% of pairs.
- **If that cannot reach 15% within K12:** stop and ask Opus for a recorded section 4 amendment (for example a D1/D2 re-split), made before the pilot. Do NOT keep 174/226 silently, and do not loosen K30.

### FU3. ROW_SCHEMA pointer for T6 3.3.1: YES, add it
- **Why.** ROW_SCHEMA restates the gold "in order" (the 3.2 order) and is B's contract. As written it misstates T6, even though B's other input (the G0-lite, :70) carries 3.3.1.
- **Line to add** under "What the label is": "T6 error classes follow G0-lite 3.3.1, which overrides steps (3)/(4) for T6 (Opus ruling Q2, 18 Oct): an ambiguous write with neither key nor read path = ASK, and invalid_named_arg with the corrected value not in context = ASK, on every card."
- **Scope.** This is a documentation correction, not a new rule. Re-hash ROW_SCHEMA in the hash export, and record in solver_b/README that the line was added after B was written.

### FU4. Thin invalid_named ASK rows; no idempotent-write PROCEED control: NOT a required gap
- **No quota in the text.** The G0-lite sets no per-sub-case quota inside T6. 3.3.1 (:65) defines labels, not counts. The binding T6 quantities are:
  - the trigger totals and ASK share (:92, K4, K5);
  - K12 edit coverage (e17-e20);
  - K30 at family level.
- **Ruling.** Neither the thin invalid_named-not-in-context ASK rows nor the missing idempotent-write PROCEED control fails a bar, and neither must be filled.
- **Optional.** Raising either, inside T6's fixed totals, is an allowed quota choice made before the pilot. It needs no Opus ruling.

### FU5. Only `get_<noun>` counts as a read path, though `list_<noun>` is in every row: NOT supported by the text as a verb rule
- **What the text says.** It defines a read path by what the call can do, not by its verb: "settled by a listed read-only call" (:48); "read path listed" (:54, :65).
- **Why list_ qualifies on the plain text.** `list_<noun>` is a listed read-only call that "Lists <noun> records". On that plain text it can settle whether the failed write committed: the target is present or absent after a delete, or shows the written field.
- **What follows.** A T6 "neither" row that lists `list_<noun>` for the target noun is ambiguous:
  - on a read_first card it reads as R-RES, so PROCEED;
  - on a card without read_first it falls into the unclear case noted in Q2.
- **Ruling.** Keep the gold unambiguous; do not relabel. In every T6 ambiguous-write row meant to have no read path (the ASK base of e17 and e18 pairs, the D4 ASK rows), the generator must not render a read-only call on the target's noun (no `list_<noun>`, no `get_<noun>`).
- **Where a read path is intended,** render it as now (`get_<noun>` on a read_first card).
- **Asserts:** add a per-row assert at creation, and make solver B abstain when a "neither" row shows any read-only call on the target's noun.
- **Wider scope.** The same applies wherever R-RES decides a label (T7 e14, T8): a read-only call that could settle the open WORLD slot must be either the intended resolver or absent.

### FU5 note (T8)
- **Text.** T59/G0_LITE.md:64 (T8 row) allows an "INTENT/WORLD fork". D5 (:48) lets R-RES settle only "an open WORLD slot" and says "A resolver NEVER settles an INTENT slot".
- **So R-RES can decide a T8 label only when T8's fork is a WORLD slot.**
- **As built, it never does.** The builder makes every T8 fork an INTENT slot (t59_scene.py `derive_T8`), and the T8 edits (e3, e8, e16) include no resolver edit. Strike T8 from FU5 for C2.1.
- **Condition.** If a WORLD-slot T8 fork is ever built, the FU5 rule applies to it: a read-only call that could settle the fork is either the intended resolver (on a read_first card) or absent.

---

## Q5. T63 LIC quota against the hashed licence table (Opus 5.5, Sun 18 Oct 2026 ET)

### Spec lines and fixed inputs
- T63/G0_LITE.md:46: "project licence id (about 8 of the same set)"; "REVIEW is the safe label for contested or condition-dependent cells"; "Each cell is used by at most one row."
- T63/G0_LITE.md:63: "rows before drops; quotas counted AFTER drops, every quota cell oversampled by 15% at generation, fixed now".
- T63/G0_LITE.md:70: "| LIC | 200 | COMPATIBLE 70 / REVIEW 60 / INCOMPATIBLE 70 | >= 30% of rows in a one-axis-flip pair |".
- T63/G0_LITE.md:73: "<= 1 per licence cell".
- T63/G0_LITE.md:21: "Total trained rows: 1,200 generated (NEAR, EXISTS, LIC)".
- T63/G0_LITE.md:4: every number is a design value fixed before any pilot.
- T63/G0_LITE.md:112 (K7): "LIC >= 30%" in one-axis-flip pairs.
- T63/G0_LITE.md:115 (K10): "label shares 30-40% each; cells drawn stratified by LABEL only (no per-licence cap that distorts the table)", plus the axis-reading check.
- T63/G0_LITE.md:162 (risk 2): "EX-B2 shrinks to the visible share if R3 shows no signal".
- T63/G0_LITE.md:230 (T63-B5): pilot = 50% of 1,200, proportional by block.
- T63/G0_LITE.md:232 (T63-B6): "the identifier set 16 x 8 x 5 x 3 is confirmed; `fixed_real_licence_ids` is a NON-GUARD fixed-name list in manifest v1.2".
- zed_orch/c21/l0/T63_LIC_TABLE_RECORD.json: 1,920 cells; COMPATIBLE 1,550 / REVIEW 330 / INCOMPATIBLE 40; canonical sha 81fe96f7...28eb.
- l0/NAMES_MANIFEST_V1_2.json, `v1_2_additions.fixed_real_licence_ids.T63_spdx`: all 16 ids, including GPL-2.0-only and NOASSERTION.

### Arithmetic (from fixed inputs and bars only)
- Only 40 INCOMPATIBLE cells exist, and each can be used once.
- Every generated row needs its own cell, including the 15% oversample. So the kept INCOMPATIBLE quota is at most 34 (34 x 1.15 = 39.1, which fits in 40).
- K10 needs INCOMPATIBLE >= 30% of LIC, so LIC can hold at most 113 rows.
- The planned 200 rows (70 INCOMPATIBLE) cannot be built without reusing cells, relabelling or loosening K10. All three are barred.

### Ruling: option (a), resize and substitute; the family stays 1,200
- **LIC = 110 kept rows: COMPATIBLE 38 / REVIEW 38 / INCOMPATIBLE 34 (34.5 / 34.5 / 30.9%).**
  - Generation draws at most 44 / 44 / 40 cells; all 40 real INCOMPATIBLE cells are used.
  - 110, not 113: with 110, one INCOMPATIBLE shortfall beyond the spare cells still passes K10 (33/109 = 30.3%); with 113 it fails (33/112).
- **The 90 freed rows move by substitution to the two seeded blocks**, which have no source limit:
  - NEAR 500 -> 550 (YES 275 / NO 275);
  - EX-A 250 -> 290 (YES 145 / NO 145; EX-A1 140 -> 160, EX-A2 110 -> 130).
- **EX-B stays 250.** It is bound to the pinned export, and risk 2 says EX-B2 may shrink, not grow.
- **New pilot split (GV10 / T63-B5):** 600 = NEAR 275 / EX-A 145 / EX-B 125 / LIC 55. This replaces 250 / 125 / 125 / 100.
- **Status of this change.** It amends the section 4 design values before the pilot. No bar changes. It respects the owner rule: the reduction is forced by the measured, hashed table plus the one-use rule and K10, not by an estimate, and the family size is kept.
- **Cell use.** A cell is "used" by a row that enters the pool. Oversample rows truncated after drops, and pilot rows discarded by the one fix iteration, are never trained, so their cells are released. A post-fix re-read (new seeds) may draw them again.

### Options not adopted
- **(b) Widening an axis** breaks T63-B6's confirmed 16 x 8 x 5 x 3 and would need a new Opus amendment.
- **Swapping project ids inside the 16 ids** (for example adding GPL-2.0-only) keeps 16 x 8 and the v1.2 list. But the text gives no reason to prefer another project set, and choosing axis ids for their INCOMPATIBLE yield would be a label-driven redesign of a signed, hashed table. Not adopted for C2.1. C2.2 item: a project axis chosen for coverage of real project licences, written by a separate Opus session.
- **Also barred:** reusing cells (:46, :73), relabelling (owner rule), per-licence caps (K10), and loosening the K10 shares.

### Who does what
- **Generator:**
  - set the LIC quota to 38 / 38 / 34 and cap each label's oversample at its available cells;
  - draw cells stratified by LABEL only;
  - keep at least 30% of LIC rows (at least 33) in one-axis-flip pairs, and keep the K10 axis-reading shares;
  - bind every LIC row to table sha 81fe96f7...28eb and its cell id;
  - scale the NEAR plan to 550 rows (`GROUPS_500` x 1.1; re-derive the K13 quotas);
  - set EX-A1 / EX-A2 to 160 / 130 and the pilot split to 275 / 145 / 125 / 55.
- **Table author:** nothing to do. No new cells and no relabelling; the table stays as hashed.
- **Names manifest v1.2:** no impact. Every id in use is already in `fixed_real_licence_ids`.

---

## Q6. T60 ladder design for K4 and K21 (Opus 5.5, Sun 18 Oct 2026 ET; pre-pilot design; no bar or gate is changed)

### Spec lines
- T60/G0_LITE.md:83: "Row level = the highest mechanism level on the row, except L4 only when at least two mechanisms are at L3 or above"; T60 uses "the TWIN RULE for every head".
- T60/G0_LITE.md:86-96: mechanism ladder. Interference :88, coupling :87, salience :89 ("needed: 1 + (3 - markers); unneeded: 1 + markers"), recovery :92, irrev :94, depvis :95, length :96 (L4 "> 1,024 (cap 1,536)").
- T60/G0_LITE.md:97 (K21 text):
  - "every mechanism populates all four levels (each >= 10% of its rows)";
  - "L4 >= 8% of the family ... and >= 5% of each head; no more than 55% of L4 rows share a label";
  - "every L3-L4 row has an easy-looking twin with the OPPOSITE label (same scenario-id prefix, level <= L2, token count +-15%, same salience-marker count) for >= 80% of L3-L4 rows".
- T60/G0_LITE.md:125 (K4): "per ladder level 35-65%".
- T60/G0_LITE.md:126 (K5): marker-count distribution identical across labels (TV <= 0.05).
- T60/G0_LITE.md:129 (K8): structure-only probe, includes token length.
- T60/G0_LITE.md:136 (K15): "> 1,024 on <= 10%".
- T60/G0_LITE.md:142 (K21 gate): "as section 5".
- T60/G0_LITE.md:43 (FREE): "... before the subtask can end, AND no pending main-thread step feeds it".
- T60/G0_LITE.md:47: "The near-miss ACT rows are the 'two of three' cells".
- T60/G0_LITE.md:245-248 (T60-B10): quad marker edits are emphasis, magnitude, ident and repeat only.
- T60/G0_LITE.md:243 (T60-B9): design value "L3-L4 30%".
- T60/G0_LITE.md:201: before the pilot, defects are build fixes.

### Ruling (1): the design the generator must use
- **a. Honour every planned level.** Every section 5 mechanism gets a planned level on every row, and the builder realises it.
  - Add a per-row assert at creation: realised level (`t60_render.realised_levels`) == planned level. A mismatch is dropped and regenerated on the same skeleton (a non-G13 drop).
  - Mechanisms the pair's edit field does not touch are held at the SAME level on both members (K11).
- **b. Choose the hard member per group, and alternate its label.**
  - In each pair, quad or swap, one member is the hard one (L3-L4). The other is its twin: level <= L2, tokens +-15%, same marker count.
  - Across groups the hard member's label alternates, so that per head and per level the label share is 35-65% (K4) and at most 55% of L4 rows share a label.
- **c. Mechanisms that are one-sided by definition** need balancing across mechanisms:
  - H1 interference rises only on DO_HERE;
  - H1 coupling "exactly B_max" is DELEGATE;
  - H2 recovery L2 = k01 KEEP and L3 = k02 DROP;
  - H3 depvis L3-L4 = unstated order.
- **d. Balance them with near-misses the rule text itself defines, plus quota mixing:**
  - H1 DELEGATE near-misses of FREE (:43): a main-thread write after the subtask can end; a pending step whose output the subtask does not take; an alias that resolves to a different resource. These are scored at the visibility level of their form (explicit / alias / declared output). Record this scoring convention in the conformance map.
  - H3 "two of three" ACT rows (:47): unstated order (depvis L3-L4) with R1 or R2 failing; a short-window step on a row failing R2 or R3.
- **e. Markers in every H2 pair kind, not only quads.**
  - The quoted fact or facts of pointer, supersede, step_done and recovery pairs carry quad markers (emphasis, magnitude, ident; repeat only on V or D facts, and never on a supersession chain, per Q1).
  - Both members carry the same marker count.
  - The count m in {0, 1, 2, 3} is drawn so that m and 3 - m are equally frequent within each pair kind. Then the hard member is KEEP when m <= 1 and DROP when m >= 2, equally often, and the marker-count distribution is identical across labels (K5).
- **f. Fill every level of every mechanism** (>= 10% of its rows each, K21 text): H1 interference L2 and L4; H2 salience L2 and L3 (from e) and recovery L2 and L3; H3 irrev L4 (the window expires between plan time and step time) and depvis L2 and L4 (numbered list; data flow through a derived value).
- **g. Reach L4 >= 5% in H1 and H3** by planning L4 groups (two mechanisms at L3 or above) in those heads' pairs.
- **h. Length: the bars force an amendment of one design value.**
  - K21 (:97) wants length L4 (> 1,024 tokens) >= 10% of its rows (all rows); K15 (:136) wants > 1,024 on <= 10%. So length L4 must be exactly 10% of the family, by count after drops (100 in the 1,000-row pilot).
  - Build length-L4 rows at >= 1,100 tokens and length-L3 rows at <= 960, so rewording cannot cross 1,024 or 800 (cap 1,536).
  - A length-L4 row can never have a valid twin: +-15% tokens puts the twin at >= 871 tokens, which is length L3, so the twin's level is >= L3. All such rows fall in the twin rule's 20% allowance.
  - At the confirmed design value L3-L4 = 30% (T60-B9), that allowance is 6% of the family, less than 10%, so the text cannot be met.
  - **Ruling:** raise the L3-L4 DESIGN share for the family to 55% (about 1,100 rows; 550 in the pilot). This is a design value, not a bar, and the change is stricter, not looser.
  - Why 55%: twinless allowance 220 >= 200 length-L4 rows; twinned hard rows >= 880 <= 900 easy rows; both have 20 rows of margin.
  - Per-head bars stay as written (>= 25% L3-L4, >= 5% L4). Record this as an amendment of T60-B9's "L3-L4 30%", made before the pilot from the bars' own arithmetic.

### Ruling (2): gate code
Yes. Add to the K21 gate code, so the code matches the text (:97, :142); this is not a loosening:
- every mechanism populates all four levels, each >= 10% of its rows;
- the twin rule: >= 80% of L3-L4 rows have a twin with the same scenario-id prefix, the opposite label, level <= L2, tokens +-15% and the same marker count;
- the existing per-head and family L3-L4 / L4 checks and the 55% L4 label cap.
Also add the planned == realised level assert, and re-run the dry-run read after these changes.

### Ruling (3): what to avoid
- **Label-correlated surface cues.** No marker, decoy phrase, order word, list format or length pattern may appear on one label only (K5, K6, K7, K8). Decoy wordings come from the same pools for both labels.
- **Markers.** Markers come only from the four quad markers (T60-B10); user_source and recency stay derived and balanced. No repeat marker on a supersession chain.
- **Padding.** Do not reach a level by padding one label (token length is a K8 feature).
- **Post-hoc filtering.** Do not drop or filter rows by realised level or label after generation to hit shares; steer only through the planned quotas. AFLite is only the post-pilot fix (:202).
- **Rendering.** Levels and mechanism tags stay manifest metadata, never rendered. Hard cells never sit on a subjective boundary (:97).

---

## Q7. T63 LIC gates after Q5 (Opus 5.5, Sun 18 Oct 2026 ET; text only; no bar changed)

### Spec lines
- T63/G0_LITE.md:6 (G5): "one probe harness (grouped split, L2 logistic regression, ... 97.5th-percentile bound over 2,000 cluster-bootstrap resamples, balanced accuracy for k-way, permutation check ..., injected-leak power check >= 0.80 ...)".
- T63/G0_LITE.md:101: "Probe protocol = G5 throughout (groups: snapshot / library history / licence block / source record)".
- T63/G0_LITE.md:97: "SET-LEVEL checks run ONCE per family, on the pilot (first look) and on the built family, never at the mix: ... the section 7 probes".
- G0_APPROVALS_v32.md:98-99 (GV8): "On the 1,000-row pilot a per-sub-block probe may be pooled across sub-blocks of equal k; the per-sub-block read on the fully built family is the binding one. Bars unchanged."
- T63/G0_LITE.md:115 (K10): "format-only probe (card layout, field order, wording id; no licence ids) balanced accuracy | format-only <= 1/3 + 3 pp = 36.3%, ub <= 39.3%".
- T63/G0_LITE.md:86 (M-CELL): LOW "far from any REVIEW boundary"; HIGH "one axis from a flip".
- T63/G0_LITE.md:87:
  - "Row level: L1 no mechanism; L2 one LOW; L3 one HIGH or two LOW; L4 two or more HIGH. Composition (set-level, PRE-FREEZE): L1 20% / L2 30% / L3 30% / L4 20% (each +- 5 pp); L3-L4 = 50% (floor 25%), per block L3-L4 >= 25%";
  - "TWIN rule: every L3 / L4 row has an easy-looking twin with the opposite label (differing in <= 1 field or <= 1 edit); twins cover >= 50% of L3-L4 rows";
  - "MAL rows have no ladder".
- T63/G0_LITE.md:117 (K12): "L1 20 / L2 30 / L3 30 / L4 20 +- 5 pp; L3-L4 >= 25% overall and per block; twins >= 50% of L3-L4".

### Q7a. The K10 format-only probe: no larger sample exists by the text; fix the features and the format assignment

**Where the probe is read.** The text fixes it: on the pilot (first look) and on the built family, which is binding (:97, GV8). So the read is on the LIC rows in the pool: 55 in the pilot, 110 when built.
- Pooling LIC rows across the 5 build seeds is not allowed. Those rows are not the family; a dry-run read is a build-stage diagnostic only.
- GV8 pooling is only "across sub-blocks of equal k", and LIC is T63's only 3-way block, so it has nothing to pool with.
- "The full pool" is the built family, i.e. the same 110 rows.

**What the generator and the probe must change** (the 36.3% / 39.3% bar is unchanged):
1. **Use exactly K10's features:** card layout, field order and wording id.
   - Token count is not a K10 format feature. It carries the length of the licence ids, which K10 excludes ("no licence ids"), so it is a licence proxy. Remove it.
   - Option order is not in K10's list either. Letter integrity is checked by the pipeline's option check and by the R7 flip rate.
2. **Assign the format label-blind and balanced by construction.** Draw card layout, field order and wording id from the same distribution inside each label (for example cycle the format cells within each label stratum). Then the built rows carry zero format signal.
3. **Use the one shared L-0 G5 harness as configured.** No T63-specific regularisation and no tuning on held-out rows. Run its permutation and injected-leak power checks. A run that fails either check is invalid and is repeated (G5); it is not a fix iteration.
4. **If K10 still fails** on the pilot after 1-3, it goes into the ONE combined fix through the allowed levers (wording pools, template ids; :172). If it still fails on the built family, that is a K10 failure as written. No bar is loosened.

### Q7b. K12 ladder for LIC: LIC is not exempt, but the text needs no other LIC levels

- **All L3 is correct by the text.** Only MAL has no ladder (:87); LIC is on it, through M-CELL. On the hashed table every cell is one axis from a flip, so every LIC row is M-CELL HIGH, which is L3.
  - L4 cannot occur in LIC: it needs two HIGH mechanisms, and LIC has one.
  - A LOW cell does not exist in this table. The generator must NOT invent a narrower distance measure, or pick cells by level, to manufacture L2 rows.
- **The only per-block bar is "L3-L4 >= 25%" (:87, :117), and LIC meets it at 100%.** The L1/L2/L3/L4 composition (each +-5 pp) and the twin share (>= 50%) are family-level ("overall").
- **For LIC, the twin is the one-axis-flip partner:** it differs in one field and has the opposite label (:87). These twins count toward the family twin share.
- **Required:** the generator sets the NEAR and EXISTS level quotas so the FAMILY composition holds with LIC's rows (about 9% of the family) all at L3.
- **Report line:** "LIC rows are single-level (L3, M-CELL HIGH) on the hashed table".

### Q7a follow-up: the valid K10 read for the 110-row LIC block (Opus 5.5, Sun 18 Oct 2026 ET; text only; bar 36.3% / 39.3% unchanged)

#### Spec lines
- G0_APPROVALS.md:64 (G5): "L-0 builds one CPU probe harness for all families, and every family uses it with its own features".
- G0_APPROVALS.md:71: "k-way probes use balanced accuracy (mean per-class recall) against 1/k + 3 pp and 1/k + 6 pp".
- G0_APPROVALS.md:72-73: "every probe run includes a label-permutation sanity check ... and an injected-leak power check (... a planted one-feature leak must reach AUC >= 0.80), else the run is invalid and is repeated (not a fix iteration)".
- G0_APPROVALS.md:74-76: the confirm rule "is approved for GEN and VOICE only".
- T63/G0_LITE.md:115 (K10): the features are "card layout, field order, wording id; no licence ids".
- T63/G0_LITE.md:119 (K14): ">= 50 wordings per question form, none > 2%". So each LIC wording id sits on at most 2 of the 110 rows.
- T63/G0_LITE.md:173: T63 rolls if it is "not through all of them by the data freeze".
- c21_fam/LC_COMMON/probe.py:
  - `binary_probe` carries both G5 checks; its planted leak is one column, y + N(0, 0.15);
  - `kway_probe` carries neither check;
  - every feature is standardised (`StandardScaler`), with C fixed at 1.0.

#### Ruling
1. **The checks belong to the shared harness, not the family.**
   - G5 makes both checks part of every probe run of the ONE shared harness. `kway_probe` lacking them is a harness defect, and L-0 fixes it once for every family. The checks the family added are not the G5 checks.
   - The k-way analog, read from G5's own k-way line: the mean permutation balanced accuracy must lie within 1/k +- 3 pp, and a planted one-feature label leak (the `binary_probe` form, one column) must reach balanced accuracy >= 0.80.
2. **Features and encoding.**
   - Use K10's features as written. Layout and field order are constant by B's contract, so they carry no information.
   - Encode wording id as raw 0/1 indicators. Do NOT standardise indicators: scaling a 1-in-77 indicator to about 8.7 is what swamps the planted leak. This is a harness rule for categorical inputs in every family.
   - Do NOT coarsen wording id to a template family. That is a different, weaker feature than the one K10 names, so it would be a loosening.
3. **Label-blind assignment means independent of the label.**
   - Use a seeded random draw of wording ids over rows that ignores the label, within the K14 cap.
   - Do NOT use a cycle that pairs each wording with different labels. That builds a deterministic anti-correlation, which is why the raw reads are 0.03-0.05 and the permutation mean sits below 1/3.
   - This corrects the "cycle ... within each label stratum" example I gave in Q7a.
4. **If the read is still invalid after steps 1-3,** at n = 110 (or 55 in the pilot), the text gives no valid K10 read:
   - T63 has no "not measurable" exit: the confirm rule is GEN and VOICE only;
   - pooling is ruled out (Q7a);
   - an invalid run is repeated, never passed.
   An unread K10 is not "through" (:173). The result then goes to Opus as a G0 amendment of K10 BEFORE the pilot. One example would be a CPU construction assert on 100% of rows: card constant, wording ids drawn independently of the label, K14 cap. That amendment is not ruled here; any probe that is read keeps the 36.3% / 39.3% bar.

### Q7b. T63 K10 amendment (Opus 5.5, Sun 18 Oct 2026 ET; before the pilot; data-only gate; no model result used)

#### Facts and spec lines
- **Harness finding.** On PURE NOISE at k = 3 and n = 110, the 97.5% upper bound is about 0.40-0.44. That is above the K10 bar of ub <= 39.3%. The 6-shuffle permutation check holds in only about 55% of runs (cross-validation anti-learning at small n). So a block with no leak at all fails or is invalid most of the time: the bar cannot be met at this n by correct data.
- T63/G0_LITE.md:115 (K10): "format-only probe (card layout, field order, wording id; no licence ids) ... <= 36.3%, ub <= 39.3%".
- The same K10 cell records the precedent: "The old per-licence purity <= 70% bar is DELETED (for permissive dependencies one label is correct in nearly every cell, so it would fail on correct data ...)".
- T63/G0_LITE.md:221 (T63-M4): "K10 purity bar replaced by label-stratified cell sampling plus an axis-reading check". Opus replaced a K10 part before the pilot because it would fail on correct data.
- T63/G0_LITE.md:4: design values are fixed before any pilot; after a pilot, a change is a gate edit and needs Opus.
- T63/G0_LITE.md:172: "Defects found before the pilot ... are build fixes".

#### Ruling (1): who may amend, and who records it
- Before the pilot, Opus may amend a gate whose bar cannot be met by correct data. T63-M4 is the exact precedent: same gate, same reason, same stage.
- Unlike the licence table (T63-B6), a gate ruling does not need a separate session.
- **Recording.** The orchestrator records the amendment in three places:
  - T63/G0_LITE.md, as an "[Opus Q7b]" note in K10 and in the batch-1b block;
  - the G0 approvals log;
  - the Thu 22 hash export and conformance map.
- **The owner is informed, not asked.** The C2.1 owner report must state this gate-form change, its reason and the noise-simulation record (seeded and reproducible). Owner decisions are reserved for the GO points, and I found no owner reservation over data-gate form.
- **Honest caveat.** If the owner wants to approve every change of a kill gate's form, this becomes an owner decision. The orchestrator should say so in the report rather than assume.

#### Ruling (2): the replacement, stricter in intent
K10's format-only part becomes a K10-F CONSTRUCTION ASSERT. It is a PRE-FREEZE KILL with a 100% bar.
- **(a) Code-level independence** (a CPU test, re-run at every code sha):
  - every format choice of a LIC row is a function of (seed, row index) only: card layout, field order, wording id, template id and option order;
  - regenerating the block with the labels permuted, or with the licence cells swapped, gives byte-identical format choices on every row;
  - the format draw function takes no label or cell input (a static check).
- **(b) Exact replay on 100% of built rows** (pilot and family):
  - from the recorded seed, each row's realised format choices replay exactly;
  - card layout and field order are single-valued;
  - wording use stays within the K14 cap.

This proves format and label independent exactly. That is stronger than bounding a noisy estimate, and it covers two features K10 did not list (template id, option order).

- **The probe stays REPORT-ONLY beside the assert.** Report its read, n, validity flags and the noise upper bound at that n. It is never a kill.
- **No realised-table p-value threshold.** A test like that fails correct data at its alpha rate; the replay is exact instead.
- **All other K10 parts stay binding:** table sha, each cell once, label shares 30-40%, label-stratified draw, axis-reading shares.

#### Ruling (3): other small k-way blocks
- Yes, the finding must be handled, but family by family, never as a blanket change.
- For every k-way probe at its planned pilot and family n (including T57 K7 and T67 K17), the harness owner (L-0) runs the seeded noise simulation and reports the noise 97.5% ub and the permutation-check pass rate.
- If the noise ub is at or below the bar and the checks are stable, the probe stays as written.
- Where GV8 equal-k pooling applies on the pilot, it may be used; the built-family read still binds per sub-block.
- Only a probe that correct data cannot pass goes to its own Opus amendment, following this pattern: a construction assert for what the probe protects, plus the probe as report-only.
- Never apply the T63 amendment to another family by default.

---

## Q6 follow-up. T60 K21 twin rule and level fill after the Q6 design (Opus 5.5, Sun 18 Oct 2026 ET; text only; no bar changed)

### Spec lines
- T60/G0_LITE.md:47: "Pairs flip exactly one of R1, R2, R3 ...; the near-miss ACT rows are the 'two of three' cells".
- T60/G0_LITE.md:83: "Row level = the highest mechanism level on the row".
- T60/G0_LITE.md:95 (m.t60.depvis, "is the order stated"): L1 explicit order words, L2 numbered list, L3 implied by data flow, L4 through a derived value.
- T60/G0_LITE.md:97 (K21): "every mechanism populates all four levels (each >= 10% of its rows)"; "every L3-L4 row has an easy-looking twin with the OPPOSITE label (same scenario-id prefix, level <= L2, token count +-15%, same salience-marker count) for >= 80% of L3-L4 rows".
- T60/G0_LITE.md:134 (K13): "contingency-reader rows >= 40 ... plus every m.t60.recovery L2-L4 row".
- T60/G0_LITE.md:136 (K15): "> 1,024 on <= 10%".
- T60/G0_LITE.md:201: allowed changes are "generator parameters, quotas, edit-field mix, card numbers, marker assignment, wording pools, template ids; NOT the bars".
- T60/G0_LITE.md:237-238 (T60-B2): "H3 is the conjunction R1 and R2 and R3 ...; the near-miss ACT cells are the contrast the head teaches".
- T60/G0_LITE.md:243 (T60-B9): design value "L3-L4 30%".

### FU-a. How depvis is scored
**On EVERY row, by what the row shows** (:83, :95). The text has no "focal" scoring. `DEPVIS_SCOPE="focal"` changes realised row levels and is not allowed.
- Allowed generator change: let the H3 pair kinds share scenario-id prefixes. Then a PLAN row of an R1, R2 or card pair can take the order-stated ACT member of an R3-flip pair as its twin, since twins need only the same prefix, not the same pair.

### FU-b. Length and the twin rule
**There is no length exemption in the text.** The 20% allowance is the only cover for length rows (Q6 h).
- Length-L3 rows (800-1,024 tokens) are twinnable in principle by a same-prefix row below 800 tokens within 15%. K11 constrains pair members, not twins.

### FU-c. The fill shortfalls
These are generator changes, as build fixes, INSIDE the section 4 block sizes and the family size:
- the mechanism and decoration mix, the planned level quotas, and the card and marker assignment (:201);
- more contingency-reader specs inside the H2 cells (K13 already expects "every m.t60.recovery L2-L4 row");
- more KEEP-hard distance and indirection groups inside QUAD and pair cells (keeping K10 and K11);
- H3 irrev L4;
- length-L3 rows (planned jointly with K15: mean <= 800, > 1,024 on <= 10%).

The text has no mechanism exemption. Section 4 block sizes stay as they are.

### FU-d. K21 as written cannot be met
Two confirmed rules together make it unsatisfiable:
- By T60-B2, PLAN needs R3 (an unstated order).
- By :95 on every row, an unstated order is depvis L3 or above.

Consequences:
- No PLAN row can ever be at level <= L2, so no PLAN row can be an easy twin.
- So every ACT row with an unstated order is twinless by definition. These are the R1, R2 and card near-miss cells that T60-B2 keeps, about 180 rows at section 4 sizes.
- Length L4 must be exactly 10% of the family (K21 fill plus K15, Q6 h), about 200 more twinless rows.
- So at least about 19% of the family is twinless. Meeting ">= 80% of L3-L4 rows twinned" would then need L3-L4 >= ~95% of the family. That is impossible for any design consistent with section 4 and T60-B9.
- Q6 h's 55% does not cover it (allowance about 220 against about 380).

**The amendment that is needed:** scope the K21 twin clause to the DECISIVE mechanism:
> "A row whose decisive mechanism (the mechanism tied to the predicate its edit field or control flips; a registered map in the hash export) is at L3-L4 needs a twin with the opposite label, the same scenario-id prefix, tokens +-15% and the same marker count, with that mechanism at <= L2; this holds for >= 80% of such rows."

- All other mechanism levels, length included, still count for the composition, K4 per level and the 55% L4 cap.
- If adopted, Q6 h's 55% raise is withdrawn and T60-B9's 30% stands.

**Who decides: the OWNER.**
- This relaxes the letter of a kill-gate clause, and my rules forbid loosening a bar. Unlike Q7b, it is not provably stricter.
- No compensating probe is possible: a level-only probe would read the predicate inputs themselves (depvis is R3's visible fact) and fail on correct data.
- If the owner declines, K21 stays as written, T60 cannot pass it and rolls at the freeze. T60 is P0-extra and does not count toward the 6-of-9 floor.
- Opus recommends adopting the scoped clause, recorded in T60/G0_LITE.md and the approvals log, and disclosed in the C2.1 report.

---

## Q6 batch 2. T60, after A102 and the build fixes (Opus 5.5, Sun 18 Oct 2026 ET; text only; no bar changed)

### B2-1. An ordinal reference that lands on a superseded fact

#### Spec lines
- T60/G0_LITE.md:50: "A fact superseded by a later fact with the same role handle is not needed (the current value is)".
- T60/G0_LITE.md:51: "L3 an ordinal ('the second record fetched')".
- c21_fam/T60/ROW_SCHEMA.md:32-35: "L3 `the <ordinal> record fetched by a get call` (ordinal among the outputs of `get_<entity>` calls ONLY, in transcript order ...)"; "a fact is replaced by the latest fact with the same <handle> and <entity>".
- T60/G0_LITE.md:122 (K1): "every determining fact is visible".
- T60/G0_LITE.md:97: "Hard cells never sit on a subjective boundary".
- c21_fam/T60/t60_wording.py `CLAUSE["k_rule"]`: the rendered card states the keep rule only. NO rendered line states the replacement rule.

#### Ruling
**The gold rule is CURRENT VALUE.** A reference of any level resolves to a fact, and a superseded fact maps to the latest same-handle, same-entity fact (:50, ROW_SCHEMA:35). B's change agrees with the text and stands. Record it as made after seeing 40 disagreement rows (disclosed).

**The generator must AVOID the case.** No L3 ordinal reference, in any step, may land on a superseded record.
- Ordinals may still COUNT superseded records as positions; they must not land on one.
- Why: the rendered row never states the replacement rule, while the ordinal literally names the old record. The label would rest on a rule the row does not show (:122, :97). An L1 handle ("the <handle>") naturally means the current value, so the supersede pairs themselves are fine.
- A row that breaks this is dropped and regenerated on the same skeleton (a non-G13 drop, :112).
- B abstains if it ever meets the case.
- The 55 abstains do not arise, because no such row is built.

### B2-2. The L3-L4 design share of 30%

#### Spec lines
- T60/G0_LITE.md:97: "Required (K21): >= 25% of rows at L3-L4 in the family and in each head (design 30%: H1 180, H2 240, H3 180)".
- T60/G0_LITE.md:6: every number is a design value fixed before any pilot.
- T60/G0_LITE.md:243 (T60-B9, restored by A102): L3-L4 30%.
- No gate reads the design share, and the text gives it no tolerance.

#### Ruling
**30% is a design value, not a target with a tolerance.** The binding requirement is the bar: >= 25% in the family and in each head. A realised 84% fails no bar.

**The overshoot is forced by the text.** PLAN rows and the near-miss ACT rows have depvis at L3 or above by definition, so H3 sits at about 80% or more whatever the generator does. The fill rule (>= 10% at each level of each mechanism) pushes H1 and H2 up.

**What the generator may do (optional, not required).** Before the pilot, it may concentrate the mechanisms' high levels on the same rows in H1 and H2, which reduces stacking, as long as every one of these still holds:
- the K21 fill and the L3-L4 / L4 floors;
- K4 per level;
- the 55% L4 cap;
- A102 twins.

**No owner decision is needed:** no bar or gate is touched. Record the realised shares (H1 64%, H2 93%, H3 92%) and their cause in the conformance record and the C2.1 report.
