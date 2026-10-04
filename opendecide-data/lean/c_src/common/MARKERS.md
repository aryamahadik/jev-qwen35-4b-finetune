# MARKERS: the cross-family missing-value marker table (XF06), v1.1

Date: 3 Oct 2026. Owner: the orchestrator (`c_src/common/`). No family builder edits this table. Every family's parser
enforces it (XF06). The machine copy is `c_src/common/markers.json`, and `c_src/common/test_markers.py` checks that the
copy is consistent. F8 and any other family that reads this table as a named input reads one fixed version: the
orchestrator names the path and sha256 in the generator task (F8-R2-19).

**Status.** This is a G0 closed lexicon (XF17). It passes the 7.2 Claude-seed decontamination and the counts-only sealed
template compare before any row uses it. It was written before the sealed sha256 commit, by orchestrator task. See
open item M3.

**Sources.** Every reference to the marker table, to XF06, to missing-value markers, to blanks and to missing keys in
`c_src/*/G0_SPEC.md` (COMMIT, F1-F13), re-read on 3 Oct at about 20:20 UTC. Each spec's sha256 at that read is in
`markers.json` under `built_from.specs`. `test_markers.py` fails when a spec has changed since. When that happens,
re-read that spec's references, update this file and `markers.json`, and only then record the new sha256. Never
refresh the sha256 alone. References are cited by rule ID, not by line number, because line numbers move.

**v1.1 (this version) against v1.0 (3 Oct, about 19:15 UTC).**
- The family rows follow the specs as they now stand. Changed rows: COMMIT, F1, F2, F3, F4, F5, F9, F10, F11 and F12.
  F6, F7, F8 and F13 have only their references or stricter bans updated (F8: the F8-R4-06 record-status-word lint).
- M1 (F12) and M2 (F11) are closed: both families now render no blank, and F12 renders no "not available".
- N2 is closed by F6. M4 is narrowed.
- The table's own classes, banned list and matching rules are unchanged. F6 still cites "v1.0" (row 4, 3.1 markers, S5).
  Its row is unchanged in v1.1.

## 1. The table

| Class | Meaning | Word markers (any letter case) | Typed (JSON/YAML) |
|---|---|---|---|
| **Unknown** | The value exists, but the record does not give it. | "not recorded", "unknown" | `null` |
| **Zero or absent** | Zero, no item, or a Boolean fact recorded as not holding. | "0", "none", "no" | `false` |
| **Banned in every family** | Never a value, in any container. G3 or a lint rejects it. | "-", "n/a", "N/A", "TBD", "?" (and their case and dash variants: en dash, em dash, minus sign, "--", "??") | |

- **Blank** (an empty cell, an empty string, or "key:" with nothing after it). A blank's meaning is set by the card. It
  appears only on rows whose card states what it means; this is a definition-following contrast.
  - On closed or local cards, a blank is never an unknown: unknowns there use a word marker or `null`. So a blank on a
    complete record means none or no, or another card-stated value that is not an unknown (F3's "no change" and
    "<default>", F2's "no edge", F4's closed-column No).
  - On open-world cards, a blank may mean unknown if the card says so (F5 open cards, F6 open-world tables).
  - Families that never render a blank: F1, F8, F9, F10, F11, F12, F13 (and COMMIT, which has no records).
- **Missing key / left-out field.** XF06 does not cover this. Each family's card defines it (section 3; open item M4).
- **Rendering.**
  - JSON and YAML write null as `null`. YAML never uses `~` or an empty scalar for null (F9 1.6, F7 3.1, F3 rule 20).
  - A YAML word marker that YAML 1.1 would coerce ("no", "yes", "on", "off") is either quoted or written as the typed
    value it means (F9 1.6).

## 2. Matching

- A marker is matched against the whole cell, field or value after the outer whitespace is trimmed. It is never matched
  as a substring of a longer value.
- Word markers ignore case: F8 says "not recorded" in any letter case, and "N/A" and "n/a" are the same marker.
- `null` and `false` are typed values. The quoted strings "null" and "false" in a JSON or YAML container are not those
  values. Where a family writes the word "false" outside JSON and YAML (F9 T34, F11 SEM-50), the word means the typed
  value: zero or absent.
- A word marker may also appear in a sentence that states it of one value, such as "<fact> was not recorded" (F8
  missing-value lexicon, F11 SEM-04).

## 3. How each family uses it

Each family uses only markers from section 1, plus the family-local markers it registers here. A family-local marker is
never one of the banned markers, and a word has the same class in every family that uses it. `test_markers.py` checks
both rules.

| Family | Shared markers used | Family-local markers (class) | Blank | Missing key | Stricter than the table | References |
|---|---|---|---|---|---|---|
| COMMIT | "0" (a binary or mode-only file: 0 added, 0 removed, never git's "-") | none | none | not used (no records) | none | 1.3 numstat, XF06 effect |
| F1 | "not recorded" (listed non-Boolean fields of missing-field cards, <= 2 per case, Unknown class); "no" / false (known-false Booleans in tables, forms and key-value records on closed-world and missing-field cards) | none | never: open-world case files are prose only, so an unknown is simply not mentioned | never an unknown: closed-world and missing-field records leave out a key only for a false Boolean (= false, row 1); non-Boolean keys are never left out | no "unknown", no null, no blank | row 1, row 2, row 3 / A10, F1R2-A01, F1R2-K3, F1R3-K3, F1R3-K4, X6, 4 parser |
| F2 | "not recorded" (exactly one rule-read field per open-world row, the literal text in every container, JSON/YAML included); "0", "no", false (closed world: absent values printed) | M4 "<computed-cell marker>" (a computed amount, not a missing value) | card-defined only: M3 (closed-world cards, the named amount column, a line with no quantity and no rate) = nothing charged; B1 edge blank = no edge on that side; open-world cards have no blank amount cell | closed world: absent line item, condition or W3 field left out = absent (W1) or the W3 default; open world: never for a field a rule reads | null and "unknown" never rendered; "not recorded" never on a closed-world card | 2.1 (R3-11), W1, W2, W3, M3, M4, B1, R1-01, R1-05, R3-07, R3-11, 9 item 9 |
| F3 | "0" (a zero `<quantity>` only) | T3 "<gap marker>" (one or more missing log entries) | card-defined only: T8 = no change; T9, T42, B17 = "<default>" in a creation row; shown only where the card states it (no-card rows: none); tables: empty cell | JSON, YAML, key-value: a left-out key is a blank, as T8's card sentence states | no null, `~`, empty string or empty "key:"; no "unknown", "not recorded", "none", "no" or false as a field value; unknowns come only from open-world gaps | rule 5, rule 20, T2, T3, T8, T9, T42, B17, F3-R3-06, F3-R3-07, F3-R3-C1 |
| F4 | "not recorded" (OW tables and CSV), null (OW JSON/YAML), "no" / false | "Yes" / true (present) | only in a column that a record line declares complete (18c), where it means No; an unknown cell is never blank; CW: no blanks | OW JSON/YAML: missing key or null = not recorded (unknown); CW: none that a rule reads | empty strings and empty "key:" lines rejected; "not recorded" never in a closed column | clause 18 legends (1)-(4), 18c, section 4 G3 rejects incl. X11, F4-A09, F4-R1-09, F4-R3-06, R4-C3, X18, 12.11 |
| F5 | "not recorded", null, "no" | none | open card: a blank = unknown; complete record: a yes/no blank = no only (a number, date or category is never blank on a closed card) | closed cards: never (every key, field and number / date / category attribute is rendered; G3 rejects an omission); open cards: an unmentioned attribute is unknown (SEM-03) | none | SEM-02, SEM-03, SEM-04, F5-A11, F5-R2-01, F5-R3-07, 10 item 12 |
| F6 | "not recorded", "unknown", null | S5 dialogue only: "don't know", "declined to answer", "can't recall" (unknown; listed in the card, matched whole) | unknown on open-world tables only; closed and local cards print no blank | JSON/YAML: no entry (closes where the card closes that fact type, unknown otherwise); banned in row-42 tables and member lists | "none" as a marker, "pending", 0 as a marker, plan-word markers | rows 2, 4, 6, 42; 3.1 markers; S5; F6-A16, F6-A17, F6-A18, F6-R1-04, F6-R2-05, F6-R2-21, F6-R3-SC1 |
| F7 | "no" / false | "yes", "Y", "present", "x" on checklists, true (present); "N", "absent" (absent) | card-defined C15: blank, empty string or left-out key = not present (0 points), Boolean fields only | not present (C15) | "unknown", "pending", "none", "maybe", "partial", null, "~" | 3.1 sheet markers, C15, A15, GRID note ("not required" instead of "-") |
| F8 | "not recorded" (as a value, or "<fact> was not recorded"), "0", "None" | none | never | absent, only for a Boolean factor in a closed-world row; never for numbers | "unknown", null, "not stated", "pending", empty cells; a record-status word ("record" or "log" in any form, "on file", "documented", "registered", "reported") outside the two "not recorded" marker forms and the SEM-01 to SEM-03 card lines that define them | 5 missing-value lexicon (F8-AMB-07), 5 record-status words (F8-R4-06), SEM-01, SEM-02, SEM-03, F8-R2-19 |
| F9 | "not recorded", "unknown" (tables, CSV, fixed-width, key-value), null (JSON/YAML), "0" (a real zero; also T34's false token), false | none. T34 Boolean tokens: true / false (typed in JSON/YAML, words elsewhere) or "1" / "0"; the false tokens are the zero-or-absent class, "true" and "1" are in no class | never (no blank cells, empty fields, empty strings or empty "key:") | never an unknown: non-T6 cards never leave a key out (G3 rejects); T6 cards (S4): the field's stated default | "none", blank cells, empty strings; "Y" / "N", "T" / "F", "yes" / "no" as Boolean tokens | T3, T6, T34, 1.6 containers, F9-A07, F9-A09, F9-A26, F9-A51, R3-SC1, R3-SC3, X6 |
| F10 | "not recorded", "unknown", null (one omission marker per format style, named in ST5); "0", "no", "none", false (stated values, ST6) | "not listed" (absent; ST4, only inside a stated tag list) | never (table containers use a word marker) | open world, key-value / JSON / YAML / prose containers only: a left-out key can be the style's one omission marker (unknown), named in ST5 | blank cells | 2 Case record, ST4, ST5, ST6, A12 |
| F11 | "not recorded", "unknown", null (= not stated, only on cards with a missing rule for that attribute); "no", "none", false (absent; "none" in a set field = the empty set) | "not checked" (unknown: report text on SEM-03/04 cards only, never a field value); "yes", "true", true and the attribute's listed terms (present); "false" (absent) | never (no empty value, empty string or empty "key:") | not stated (SEM-50), only on cards with a missing rule for that attribute | no empty value; a set field never holds `[]`, null, "unknown" or "not recorded"; "present", "absent", "not stated" and absence cues never written as field values | SEM-03, SEM-04, SEM-05, SEM-43, SEM-47, SEM-50, A15, A19, R35, F11-R2-04, F11-R3-07, F11-R3-13, X17 / K29 |
| F12 | "not recorded", "unknown" (SEM-31; never on a decisive precondition field) | none ("0", "no" and false are ordinary values; "not given" is a parameter status, not a rendered marker) | never (records and tool outputs are closed: no empty cell, empty string or key with nothing after it) | a field that is not shown gives no value (SEM-02 field-name rule; not a marker) | null, "not available", "none" as a field value, empty strings, empty lists | SEM-02, SEM-25, SEM-31, NG-03, NG-04, F12-A11, F12-R2-14, F12-R3-SC1 |
| F13 | "0", "none" (SEM-40) | one value marker per card: "[not provided]", "[not provided in this copy]" or "[illegible in this copy]" (unknown); part trace "<part label> (<scope label>): not included in this copy." | never (no empty fields) | not used (every attribute a rule reads is stated or traced, F13R1-07) | "unknown", "not recorded", null, empty fields; "pending" and "not yet received" are statuses (SEM-48), never traces | 2.4 TR list, SEM-01, SEM-02, SEM-40, A02, A03, F13R1-07, F13R1-28, 7 lint |

## 4. Readings used where the references leave a choice

- **Dashes and case.** XF06 bans "-", and F6 bans any dash. This table bans every standalone dash form: hyphen-minus,
  en dash, em dash, minus sign, "--" and "---". These are forms of the XF06 marker, not a new class.
- **YAML `~` and empty scalars** are banned as null renderings. F9 writes `null`; F3 and F7 ban `~`. This adds no
  meaning.
- **An empty string counts as a blank.** XF06 does not mention it. F3, F4, F9, F11, F12 and F13 never write one. F7
  (not present) defines it on the card. Every one of those uses is card-defined and fits section 1.
- **"A blank on a complete record means none/no"** is read as "a blank there is never an unknown". So these are allowed
  card-defined meanings, and each family's XF06 effect line says "No conflict":
  - F3's "no change" and "<default>" blanks;
  - F2's "no edge" blank;
  - F4's closed-column No.
- **The word "false"** outside JSON and YAML (F9 T34, F11 SEM-50 records) is the typed `false` written as a word: zero
  or absent. "true" and "1" (F9) and "yes" / "true" (F4, F7, F11) are never missing-value markers. F4, F7 and F11
  register them as family-local "present" words. F9 assigns them no class.
- **Family-local markers** are registered only where a spec defines them (F6 S5, F7, F10, F11, F13). A family that
  needs a new local marker asks the orchestrator for a new version of this table. It never adds one itself.

## 5. Open items for the orchestrator

| ID | Item | Why it cannot be met as written | Suggested fix |
|---|---|---|---|
| M3 | **The XF preamble in every G0 spec** (all 14, re-checked in v1.1): "Code named here (`c_src/common/...`) is orchestrator-owned and is written only after the sealed sha256 commit." | `negcount.py` and this table were written before that commit, by orchestrator task. Both hold closed lexicons only (no templates, domain words or rows), which XF17 allows before the freeze. | Record that XF17 covers both files, or move them behind the sealed commit. Both still pass 7.2 and the counts-only sealed compare before any use. |
| M4 | **Missing keys (narrowed in v1.1).** XF06 does not cover them. Several families now never let a left-out key be an unknown: F1 (false Booleans only), F2 (closed: absent or default), F3 (a blank), F5 (closed: never), F7 (not present), F8 (closed-world Boolean = absent), F9 (T6 default only) and F13 (not used). | A left-out key can still be an unknown in five families. Three of them are open-world cases, which fit XF06: F4 OW JSON/YAML, F5 open cards and F10 open world. Two are not: F6 closed and local cards (a missing key for a number, date or category is unknown, because those fact types never close) and F11 (not stated, which F11 renders on every card with a missing rule). F12's "a field not shown gives no value" is a field-name rule, not a marker. | Rule once whether a left-out key on a closed or local card may be an unknown. The cases to check are F6 (closed and local cards) and F11. If the ruling is no, F6 writes null for an unknown number, date or category on those cards, and F11 writes null, "unknown" or "not recorded" instead of leaving the key out. |
| N3 | **negcount R3 comparator aliases.** | Beyond F5's six negated comparison words, negcount exempts these phrases from k_syn: "no less than", "no later than", "no earlier than", "not exceeding", "does not exceed" and "not equal to". The specs name them as comparators (F2, F4, F6, F7, F8, F9, F12, F13). They are k_all-neutral, which is tested. Other "not" + predicate phrases still count k_syn 1: "not above", "not below", "no longer than". | Confirm the list. A family that needs another comparator phrase exempted asks for a new negcount version. |

**Closed in v1.1.**

| ID | Item (v1.0) | Closed by |
|---|---|---|
| M1 | F12 SEM-31, SEM-25 and F12-A11: "a record field that is blank, marked not available, or marked unknown gives no value". This conflicted with XF06 on F12's closed cards. | F12-R3-SC1, SEM-31 and NG-04. An unknown is "not recorded" or "unknown". F12 renders no blank field and no "not available", and does not use null. No pending marker is left in the table. |
| M2 | F11 SEM-50: "an empty field means not stated". | F11 X17 and K29 (SEM-50, A15, S4 renders): F11 never writes an empty value. Not stated is a missing key or column, null, "unknown" or "not recorded". The blank question is moot. F11's left-out key is now part of M4. |
| N1 | negcount R4: "neither ... nor" gave k_syn 2 and k_all 1, so one negated connective could fill the k_syn >= 2 double-negation quota. | PREREG_FINAL.md amendment A16 (counters ruling): a matched "neither ... nor" pair is one syntactic negation, k_syn 1 (k_all unchanged, 1). `negcount.py` v1.1 (`_SYN_ONCE`, in the lexicon sha), test rows updated. |
| N2 | F6 3.1 negation cues and its G3 rule "agree with negcount on every row". | F6 3.1 negation-cues row. Every gate count (the 2.1 quotas and the G10 strata) is negcount's k_syn and k_all. Quotas are planned with L_core cues only: "not" in S, the "Is it not the case that ..." frame, and "no `<member>`". The clausal cues are never used to plan a quota. |

**Requests from the specs that this version carries out:**
- F2 section 9 item 9;
- F4 12.11;
- F5 section 10 item 12;
- F9 X6;
- F11 X17;
- F1 X6 (an optional sentence);
- F3 F3-R3-06 (missing key = a blank, as T8 states).

## 6. Other orchestrator-owned shared items named in the G0 specs

| Item | Named in | State on 3 Oct |
|---|---|---|
| `c_src/common/negcount.py`: one negation counter (k_syn, k_all) | XF02 (all specs); F2, F3, F4, F6, F7, F8, F9 bodies; F8-R2-19 named input | Written (v1.1: A16 "neither ... nor" = k_syn 1) with `test_negcount.py` |
| The marker table | XF06 (all specs); F1 parser, F3 rule 20, F4 section 4, F5 SEM-04, F6 row 4, F7 3.1, F8 lexicon, F9 T3, F10 Case record, F11 SEM-50, F12 SEM-31, F13 2.4 | This file + `markers.json` (v1.1; built-from spec sha256s checked by `test_markers.py`) |
| Shared negation-frame lint: no outer judgement or acceptance frame around a negated or negatable proposition | XF10; F4 section 4 (X11), F5 3.4, F6, F11 SEM-40, F12 | Rule text only; no shared code file is named |
| Cross-family G12 pass: exact hash + MinHash, F5 against F1-F4 and F9, F13 against F1, F3, F6 and F9 | XF11; F5 section 9 | Not written (runs on built rows, after G14) |
| F14 exclusion lint ("No row poses <F14 task>"); the provisional instance is constraint scheduling | XF16; F1 parser, F4 X11, F5, F7, F8 | The orchestrator names F14's skill and structure type before step 5 |
| One literal Score `qtype` string, shared by F7 and commit score rows and accepted by `train_decoder.check_rows` | F7 T24 (placeholder `<SCORE_QTYPE>`), F7 11.3 item 6 | Open; due before step 5 |
| One XED split file (sha256) for the public block, F10, F11 and the S5 arm | F11 A35, S7 | Not written |
| Named inputs (path + sha256) for F8: F5's trainable cue list, the shared attack pool, the 50 held-out format styles, negcount and the marker table | F8-R2-19 | negcount and the marker table exist now; the others do not |
| Shared code in `c_src/common/`: loader, deny-list, provenance, record ledger | F5 section 1 | The deny-list program `c_src/common/denylist.py` (v1.1, with `test_denylist.py` and `DENY_CLASSES.md`) is written. Its replay run writes `c_build/replay_denylist_verdicts.json`, which `c_build/replay_sample.py` reads by default (RUNBOOK_replay_reads.md 3.2). Loader, provenance and record ledger are not written |
