# R5 CANDIDATES CHECK (A61(b) split-aware check applied; L-0 item k)

Date: Sun 18 Oct 2026 (UTC). Names and metadata only: no download, no dataset read, no model call, no Modal, no rows, no G13.
Tool: `c2_build/c21_infra/split_aware_check.py` (split_aware_check v1 (18 Oct 2026)), sha256 `698692c6631456e9577d18085da8e39502bc9fbc5713fecf3f89d0063689aa74`. CPU tests: `python3 -m pytest c21_infra/tests/test_split_aware_check.py` (142 pass; whole c21_infra suite 287 pass).
Command: `python3 split_aware_check.py --registry l0/G13_TARGET_REGISTRY_DRAFT.md --r5-manifest l0/NAMES_MANIFEST_V1.json --a61a-sentinels --out <records.json>`

Inputs (shas):
- Names-only manifest `NAMES_MANIFEST_V1.json` (frozen, version v1): `04732bdbf968218d9ea902f9509bce08932740b5a3bf8362c214befd93a1c0b1` (matches `NAMES_MANIFEST_V1.sha256`).
- G13 target registry DRAFT `G13_TARGET_REGISTRY_DRAFT.md`: `33b355cd9444fa9eb580d69cab80c695ea19556a012c790adf558c367ef6ffc5`; 143 registry ids parsed (A 6, B 13, C 13, D 33, E 74, M 4), 0 unmapped. The registry is still a draft (K2 versions/URLs not filled), so this sha will change and the check must be re-run on the frozen registry.
- Deny-list file: none supplied (the existing project deny-list is outside this lane's read scope).

## Result

13 records: **ALLOW 0**, **DENY 13** (BAR 11, INSUFFICIENT_EVIDENCE 2).

| Group | Records | Decision | Why |
|---|---|---|---|
| R5 candidates in the manifest (`candidates`) | 2 (tasksource; Decision Index public index sources, TRAIN splits only) | DENY, INSUFFICIENT_EVIDENCE | Both are catalogues or groups with no member names, no splits, no per-task licence and no label provenance in the manifest. A catalogue is never a source as a whole. Not barred; each member needs its own record after the licence scout (and a name on manifest v2). |
| Manifest `excluded_even_if_R5_adopted` names | 8 (gsm8k, hover, isarcasmeval, tydiqa, md_fdc, md_peps, DI-TS inputs, SB6) | DENY, BAR (A61A_HIT) | Recorded A61(a) 8.5 HITs, barred under any id or form. R5 does not lift them. |
| A61(a) sentinels not on the manifest list | 3 (md_worldbank, md_usgs, md_cma) | DENY, BAR (A61A_HIT) | Name-only rows to show the tool bars them. |

Reason-code counts: A61A_HIT 11; CATALOGUE_PER_MEMBER_REQUIRED 2; LABELS_UNKNOWN 13, LICENCE_UNKNOWN 13, NO_SPLIT_INFO 13 (no metadata exists for any record, so these appear on every row, also on the barred ones).

Bottom line: **R5 releases nothing on today's list.** No candidate is a dataset with known splits, licence and label provenance, and no deny-list entry with split scope exists yet, so the split-aware step (a deny-list entry that taints only test/dev splits releases the train split) has not been exercised on a real entry. It is covered by CPU tests only.

## Findings for the orchestrator

1. Manifest gap: `excluded_even_if_R5_adopted.names` lists SB6 but NOT md_worldbank, md_usgs, md_cma, which the A61(a) record includes. They do not enter the allow-list (R5 candidates are not in `names`), so nothing is unsafe, but manifest v2 should add them (the manifest is frozen; I did not edit it).
2. Aliases: the tool's keys for the md_* sources (for example fdc, peps, usgs, cma, world bank and their long names) are my derivations from the abbreviations, because the A61(a) record itself is outside the read scope. They over-block by design; please confirm them against the A61(a) record.
3. Ruling needed (strict default): a registry entry that targets only named splits of a larger dataset (C13 LibriSpeech test-clean/test-other) denies the whole dataset by default, which is the literal reading of "test/dev splits are not our eval targets". The opposite reading is the `--split-scoped-release` flag (releases a train split whose requested splits do not intersect the scope); it is tested but off. The voice harvest corpus (J10, train splits only) is governed by its own manifest ruling, not by this check.
4. Name-level conflicts with plan P1 sources: SWE-rebench V2 and SWE-bench-family names match registry B11/C6 (eval), SWE-smith matches E19/E19b (LM-written bugs and issue text). The tool denies these by name. The plan's P1 route (instance-level G13 matching, K9; gold patches, tests and repos only for SWE-smith) is a different mechanism and is not an R5 question; they are not R5 candidates.
5. Fail-closed rules worth knowing: a free-text label provenance with any LLM marker denies even when negated ("no LLM involvement"); use the enumerated values. CC-BY-SA, MPL, GPL-family, NC, ND, "research only" and "no licence" are all non-permissive (SA follows the plan's TRACE ruling). Mixed human plus rule-based labels deny.
6. What ALLOW will mean when it appears: "not barred by A61(b)" only. Pre-mapper 8.5 PASS, guards, G13 pilot and a re-frozen manifest name are still required before any mapper.

## Records

| # | Name | Source | Decision | Class | Reason codes |
|---|---|---|---|---|---|
| 1 | tasksource | R5 candidate | DENY | INSUFFICIENT_EVIDENCE | CATALOGUE_PER_MEMBER_REQUIRED, LABELS_UNKNOWN, LICENCE_UNKNOWN, NO_SPLIT_INFO |
| 2 | Decision Index public index sources, TRAIN splits only | R5 candidate | DENY | INSUFFICIENT_EVIDENCE | CATALOGUE_PER_MEMBER_REQUIRED, LABELS_UNKNOWN, LICENCE_UNKNOWN, NO_SPLIT_INFO |
| 3 | gsm8k (DI-KR train split; also deny-list split-blind taint) | manifest excluded name | DENY | BAR | A61A_HIT, LABELS_UNKNOWN, LICENCE_UNKNOWN, NO_SPLIT_INFO |
| 4 | hover (di_hover) | manifest excluded name | DENY | BAR | A61A_HIT, LABELS_UNKNOWN, LICENCE_UNKNOWN, NO_SPLIT_INFO |
| 5 | isarcasmeval (di_isarcasmeval) | manifest excluded name | DENY | BAR | A61A_HIT, LABELS_UNKNOWN, LICENCE_UNKNOWN, NO_SPLIT_INFO |
| 6 | tydiqa | manifest excluded name | DENY | BAR | A61A_HIT, LABELS_UNKNOWN, LICENCE_UNKNOWN, NO_SPLIT_INFO |
| 7 | md_fdc | manifest excluded name | DENY | BAR | A61A_HIT, LABELS_UNKNOWN, LICENCE_UNKNOWN, NO_SPLIT_INFO |
| 8 | md_peps | manifest excluded name | DENY | BAR | A61A_HIT, LABELS_UNKNOWN, LICENCE_UNKNOWN, NO_SPLIT_INFO |
| 9 | DI-TS GitHub-licensed tasks (9 tasks; inputs) | manifest excluded name | DENY | BAR | A61A_HIT, LABELS_UNKNOWN, LICENCE_UNKNOWN, NO_SPLIT_INFO |
| 10 | SB6 | manifest excluded name | DENY | BAR | A61A_HIT, LABELS_UNKNOWN, LICENCE_UNKNOWN, NO_SPLIT_INFO |
| 11 | md_worldbank | A61(a) sentinel | DENY | BAR | A61A_HIT, LABELS_UNKNOWN, LICENCE_UNKNOWN, NO_SPLIT_INFO |
| 12 | md_usgs | A61(a) sentinel | DENY | BAR | A61A_HIT, LABELS_UNKNOWN, LICENCE_UNKNOWN, NO_SPLIT_INFO |
| 13 | md_cma | A61(a) sentinel | DENY | BAR | A61A_HIT, LABELS_UNKNOWN, LICENCE_UNKNOWN, NO_SPLIT_INFO |

### 1. tasksource: DENY
- NO_SPLIT_INFO: splits_available not provided
- LICENCE_UNKNOWN: licence not provided
- LABELS_UNKNOWN: label provenance None not shown to be human
- CATALOGUE_PER_MEMBER_REQUIRED: a catalogue is never a source as a whole; each member needs its own record and name

### 2. Decision Index public index sources, TRAIN splits only: DENY
- NO_SPLIT_INFO: splits_available not provided
- LICENCE_UNKNOWN: licence not provided
- LABELS_UNKNOWN: label provenance None not shown to be human
- CATALOGUE_PER_MEMBER_REQUIRED: a catalogue is never a source as a whole; each member needs its own record and name

### 3. gsm8k (DI-KR train split; also deny-list split-blind taint): DENY
- A61A_HIT: matches the recorded A61(a) 8.5 HIT source gsm8k (barred under any id or form)
- NO_SPLIT_INFO: splits_available not provided
- LICENCE_UNKNOWN: licence not provided
- LABELS_UNKNOWN: label provenance None not shown to be human

### 4. hover (di_hover): DENY
- A61A_HIT: matches the recorded A61(a) 8.5 HIT source hover (barred under any id or form)
- NO_SPLIT_INFO: splits_available not provided
- LICENCE_UNKNOWN: licence not provided
- LABELS_UNKNOWN: label provenance None not shown to be human

### 5. isarcasmeval (di_isarcasmeval): DENY
- A61A_HIT: matches the recorded A61(a) 8.5 HIT source isarcasmeval (barred under any id or form)
- NO_SPLIT_INFO: splits_available not provided
- LICENCE_UNKNOWN: licence not provided
- LABELS_UNKNOWN: label provenance None not shown to be human

### 6. tydiqa: DENY
- A61A_HIT: matches the recorded A61(a) 8.5 HIT source tydiqa (barred under any id or form)
- NO_SPLIT_INFO: splits_available not provided
- LICENCE_UNKNOWN: licence not provided
- LABELS_UNKNOWN: label provenance None not shown to be human

### 7. md_fdc: DENY
- A61A_HIT: matches the recorded A61(a) 8.5 HIT source md_fdc (barred under any id or form)
- NO_SPLIT_INFO: splits_available not provided
- LICENCE_UNKNOWN: licence not provided
- LABELS_UNKNOWN: label provenance None not shown to be human

### 8. md_peps: DENY
- A61A_HIT: matches the recorded A61(a) 8.5 HIT source md_peps (barred under any id or form)
- NO_SPLIT_INFO: splits_available not provided
- LICENCE_UNKNOWN: licence not provided
- LABELS_UNKNOWN: label provenance None not shown to be human

### 9. DI-TS GitHub-licensed tasks (9 tasks; inputs): DENY
- A61A_HIT: matches the recorded A61(a) 8.5 HIT source di_ts_inputs (barred under any id or form)
- NO_SPLIT_INFO: splits_available not provided
- LICENCE_UNKNOWN: licence not provided
- LABELS_UNKNOWN: label provenance None not shown to be human

### 10. SB6: DENY
- A61A_HIT: matches the recorded A61(a) 8.5 HIT source sb6 (barred under any id or form)
- NO_SPLIT_INFO: splits_available not provided
- LICENCE_UNKNOWN: licence not provided
- LABELS_UNKNOWN: label provenance None not shown to be human

### 11. md_worldbank: DENY
- A61A_HIT: matches the recorded A61(a) 8.5 HIT source md_worldbank (barred under any id or form)
- NO_SPLIT_INFO: splits_available not provided
- LICENCE_UNKNOWN: licence not provided
- LABELS_UNKNOWN: label provenance None not shown to be human

### 12. md_usgs: DENY
- A61A_HIT: matches the recorded A61(a) 8.5 HIT source md_usgs (barred under any id or form)
- NO_SPLIT_INFO: splits_available not provided
- LICENCE_UNKNOWN: licence not provided
- LABELS_UNKNOWN: label provenance None not shown to be human

### 13. md_cma: DENY
- A61A_HIT: matches the recorded A61(a) 8.5 HIT source md_cma (barred under any id or form)
- NO_SPLIT_INFO: splits_available not provided
- LICENCE_UNKNOWN: licence not provided
- LABELS_UNKNOWN: label provenance None not shown to be human

