# G0-lite T36: dependency version-range satisfaction (transfer dev only)

One page (C2_DATA_SPEC 6.2 item 3): a semantics table, one ambiguity listing, one resolution. **v2, FROZEN** on 13 Oct
2026 after the one Haiku ambiguity pass (`c2-data-stage-a/amb:T36`; 33 points H1-H33, verbatim in
haiku/ambiguity/amb_T36.json; it read v1, sha e7800917). **v2.1** (13 Oct 2026, ruling v2.1, section 7): sections 6
and 7 wording only. **v2.2** (14 Oct 2026, ruling v2.2: Stage B pilot fix iteration 1): R12, R13, R16, R21, sections
1.1-1.2 (row-specific cards), 3-6; no row R1-R11 or R15-R20 and no gate bar changed. This file's sha is
`plugin.T36Plugin.G0_SHA256`; `validate_plugin` refuses the plugin if the file changes, so a later change is a new
version with a new sha. The Haiku pools stay as frozen (built under the v2.1 sha 775e2c7d: plugin.POOL_G0_SHA256; v2.1
kept as G0_SPEC_v2.1.md).
Spec 2.2 (T36: 300 items, held out, never trained) and 3.20 (npm semver and PEP 440 semantics reimplemented twice); it
tests transfer of matching and precedence skills (T28, T35). Every row is dev-only (meta.dev_only = true). Code:
plugin.py, solver_b.py, fixtures.py, authoring.py. Ids (H30): R1-R21 are rows of the semantics table, S1-S5 name
samplers only, H1-H33 Haiku points. Terms from outside this page (H10): spec 3.0 (packs, registers, wordings, Mode T /
F, balance, depth), spec 4.1 (overlay: complement, minimal-edit twin, equiv, inv; a unit = a base row and its
partners), spec 6.3 (G2 solver B = A on 100%, G3 parse round trip, G4 metamorphic, G-SL, G-LEX, G-TW, G3-H, G5-H),
PREREG A38 (OHS-4 frozen before any data), kit README (QuestionForm, build_options, KitCtx.pick, lexicon kind
"question"). None of them decides an answer: every rule an answer needs is on the row's card (section 1.2, R13).

## 1. Semantics table (exact)

| # | Item | Semantics |
|---|---|---|
| R1 | Facts | From the card's pack (R19): the project (name; its id = the name in lower case, spaces as hyphens), the package PKG (id) and the maintainer (name). The row adds the declared range in ONE style (npm or Python packaging; the card printed on the row names the style, H9), 4-7 listed versions and, on yes/no rows, one version under review (always a listed one). Project, id and maintainer are inert: no rule reads them, G4 renames them (H33) |
| R2 | npm versions | MAJOR.MINOR.PATCH[-tag], numbers without leading zeros. Generated tags: alpha, alpha.3, beta, beta.2, rc.1, rc.2: parts split on "." only, each part lower-case letters or a number, never mixed (no rc1) or upper case (H16). Order: numbers as numbers; a tagged version before the same untagged one; tags part by part: numbers as numbers, words alphabetically, a number before a word, a shorter tag first when all its parts match |
| R3 | npm ranges | Operators sit on their version (never ">= 1.2.3"). Parse: alternatives split at " \|\| " (loosest), then "A - B" is a whole alternative, else comparators split at single spaces, all must hold (H15). Operands: always full M.m.p[-tag], except the x-ranges M.m.x and M.x; never partial (^1.2, ~1, "1.2.3 - 2"), *, x, X, empty, 1.x.x or >=1.2.x (H14). ^V: below the next version that raises V's first non-zero part; ^0.0.0 (no non-zero part) is never generated (H14). ~V: below the next minor. Card examples fix ^0.x |
| R4 | npm pre-release gate | A tagged version meets an alternative only if that alternative WRITES a version (any comparator, either end of a hyphen range, the operand of ^ or ~) with the same MAJOR.MINOR.PATCH and a tag; bounds that ^, ~ or x imply never count (node-semver default; H11). Printed on the card (H1) |
| R5 | Python versions | Canonical forms only: release N.N or N.N.N (no leading zeros), then optionally aN / bN / rcN directly after it (1.4rc1) or .postN (1.4.post1), always with N. Never separators (1.4-rc1, 1.4.rc.1), implicit numbers, c / alpha / preview spellings, dev, local or epoch versions (H17). Order: releases number by number with zero padding (1.4 = 1.4.0); a < b < rc, then N; pre-release < its release < its post-release < the next release |
| R6 | Python specifiers | Every specifier has an operator; commas = and; a bare version ("1.4") is never generated, exact is ==1.4 (H20). >=, >, <=, <, ==, != compare with zero padding; != takes one exact version, never !=P.* (H19). ==P.*: the release starts with P (padded); post-releases included; pre-releases match the prefix but still need R7 (H3, reading b). ~=V = >=V and ==P.*, P = V's RELEASE without its last number; V has 2 or 3 release numbers, maybe a pre-release, never a post-release: ~=1.4.2rc1 = >=1.4.2rc1 and ==1.4.* (H18) |
| R7 | Python pre-release gate | A pre-release meets the set only if some specifier other than != names a pre-release (packaging's SpecifierSet default). It applies to every set, whatever the numeric window: ">=1.0,<2" with listed 1.5rc1, "<=2.0" with 2.0rc1 and "==1.4.*" with 1.4.1rc1 do NOT meet (H2, H3). Printed on the card (H1) |
| R8 | Never generated (the complete list; H2) | Where real PEP 440 has rules the card does not print: a post-release of V under ">V", a pre-release of V under "<V", "!=" with a pre-release; plus the forms R3, R5 and R6 exclude. Every other pair the samplers draw is generated and decided by the card alone |
| R9 | Inside / outside | Inside the range = meets it (R3-R8); outside = does not meet it, even when its numbers lie between the bounds: 1.3.0-rc.1 under ^1.2.3 is outside. The card prints this (H4). This page says "numeric bounds" when only the numbers are meant |
| R10 | yes/no forms | yn_meets: yes iff the version under review meets the range. Complements, yes iff it does not: yn_outside (antonym, "outside the range", R9), yn_not_meets (syntactic, one "not" or "n't"), yn_fails (implicit, "fail to") |
| R11 | ch_pick | The resolver installs the highest listed version that meets the range ("highest" = R2 / R5 version order, never list order or a date: the list has no dates; H27), none when no listed version meets. The card prints this rule (H5). Key = the version's text or `none`; the row's gold is the gold option's text, "None of the listed versions meets the range" for `none`; the served prompt letters the options (formats-1; H21) |
| R12 | Options (H6, H7; v2.2) | ch_pick rows only. A PLAN is fixed from the seed's place in its sampler's stream before any structure is drawn (plugin.choice_plan; c2_kit.choiceplan): k = 3 or 4 (None included and shown on every row), the outcome (A: gold None, 1/k; N1: exactly one listed version meets the range, 1/k; N2: two or more, the rest; per block of k rows of that k), the gold's position (uniform per k) and its rank among the version options in version order (uniform). The sampler redraws structure until solver A's gold agrees and the plan can be filled; it never relabels (the seed's own choices of range shape, listing size and style, pre-release count and kind of version under review are redrawn every 100 failed draws, so no seed fails; one that fails 2,500 draws would be dropped and counted). Wrong options = R14 outputs, minus the gold, minus `none`, of the gold's shape (R21); equal outputs merge into one option (all models recorded). Gold `none`: k - 1 version options; else gold + None + k - 2 versions, the gold at its planned position and rank. A twin is rendered under its base's plan and skipped when it cannot fill it |
| R13 | Closed world | The card (section 1.2) prints the rules the row needs; its last line: "The range, the listed versions and these rules are complete: nothing else changes the answer." "Published versions" on the row = the listed versions, all of them (H28). Narrative, attack lines (section 6) and names never change an answer (H13, H33) |
| R14 | Error models | Section 4; each is solver A with one switch and answers ch_pick only |
| R15 | Solver A | ast_interpreter: the range parsed into alternatives of (operator, sort-key) tests and prefix tests, one interpreter over tuple sort keys, the gate per alternative; pick = max by key. Gold = solver A |
| R16 | Solver B | interval_scan (solver_b.py, from this page and the card): its own parser of the RENDERED row (the card, read through cards.split_rules, is compared verbatim with the card B builds from its own copy of the items for the parsed range); each alternative becomes ONE interval (bounds with inclusive flags) + != exclusions + ==P.* prefixes + the gate; versions ordered by a pairwise compare function (loops, zero padding), never sort keys; pick = the first meeting version of the list sorted highest first. G2: B = A on 100%, else the unit is dropped and counted (H27) |
| R17 | Construction | _tag(): interval arithmetic on version triples / padded releases; builds boundary candidates and predicts twins. A guard refuses a spec where _tag and solver A differ on a listed version. Twins (section 5): G-TW checks _tag's prediction against solver A on the twin, and G2 runs solver B on the twin row (H26) |
| R18 | Depth (H1, H29) | Operations the reader performs whose result is not printed (every RULE is printed on the card; no intermediate value is): compare (always), desugar (^, ~, x-range, ~= or ==P.* in the range), gate (yes/no: the version under review is tagged; ch_pick: a listed tagged version lies within an alternative's numeric bounds but fails its gate). depth = their count, 1-3; deep = 3, kept only on seeds whose hash is < 0.10 (other seeds redraw), so deep <= 10% of specs: a hard limit (test), flagged meta.deep, reported apart |
| R19 | Packs (spec 3.0) | A pack = one invented software project: name (2-3 capitalised ASCII words), 3 package ids (lower-case ASCII words joined by single hyphens, 4-24 characters, no digits), 2 maintainer names (two capitalised ASCII words); `check_pack`: no label word (R20), no negation cue, no reserved G4 value (yarrow-sync, Lowmoor Desk). One pack per card: card ordinal = sampler index x 24 + style x 12 + card (0-11), modulo the pool; S5 draws from held-out packs. Frozen pool: >= 25 training + >= 5 held-out packs; the 8 + 2 code stand-ins serve tests only |
| R20 | One spelling, words | No two listed versions are equal under R5 (never 1.4 and 1.4.0 both), so the pick is unique. LABEL_WORDS (G-SL, every inflection; H12): meets meet met satisfies satisfy outside inside within compatible incompatible matches match fit fitting installs install resolves resolve allowed exclude included supported unsupported newest latest oldest highest lowest newer older higher lower upgrade downgrade stable unstable prerelease beta alpha breaking |
| R21 | Shape (F3; v2.2) | Shape never tells a wrong option from the gold. (a) Options: every wrong option has the gold's kind (plain / pre-release / Python post-release), its number of characters and the bucket of its last number (0, 1-3, 4-6, 7-9, 10 and up); a `none` row has no gold, so its reference is plain, with the length and bucket of its highest plain listed version. (b) Numbers: every final number (a patch; the last Python release number) is 0 with chance 0.2 wherever the version sits; every number is as wide as the range's own (1 or 2 digits, drawn per row); a Python row lists 2 or 3 release numbers throughout; the neighbours of a bound are never always +1. (c) The version under review is a pre-release (10%), a post-release (Python, 8%) or plain, and zero-final (12%) or not, from the seed alone, on either side of the range (a post-release of an inside version is inside, a pre-release is outside unless the range writes one: R4, R7); Python bounds name a pre-release on 14% of ranges (28% in S2). (d) A ch_pick listing holds 0, 1, 2 or 3 pre- / post-releases with chance 42, 38, 17, 3 (%), from the seed alone; (e) the listing is in a random order (a sorted list put the highest version last, and a twin left its one new version out of order). A text-order trap (R18) stays in yes/no rows and in listings; as an OPTION it is dropped by (a), because the trap is a length difference (the gold the longer string) |

### 1.1 Program text (H9, H28)

- State: narrative skin, blank line, the range block, blank line, the version list, then on yes/no rows "Version
  under review: V". Range blocks: inline "Declared range for PKG in project ID (npm style): R" / "Declared specifiers
  for PKG in project ID (Python packaging style): R"; package.json (one JSON line, name and dependencies);
  pyproject.toml ([project] name + one dependencies entry "PKG R"); lockfile request (sampler S5: "lockfile request
  for ID:", "package: PKG", "wanted: R", where R is the declared range in the card's style, never one version).
  Version list: "Published versions of PKG: a, b, ..." or the one-column table (sampler S3). Attack line (inv rows):
  after the version block, blank line first.
- Instructions: the question wording. The card (section 1.2): row.card on yes/no rows (the served prompt prints it
  once), the head of the instructions on ch_pick rows (cards.place_rules; printed twice, its only place); B:
  cards.split_rules.

### 1.2 The cards (v2.2; program text: plugin.CARD_ITEMS; solver_b.ITEM is a copy; a test checks they are equal)

A card = its heading ("How to read this version range (npm style):" / "How to read these version specifiers (Python
packaging style):"), one "- " line per item the row needs (in this order), then the R13 sentence. The texts are the
v2.1 words split per rule (v2.1 printed every rule on every row). A condition reads the declared range and the
question form only (never a version, the gold or a twin's slot), so a row and its partners print one card; every
needed rule stays.
npm items (id, condition: text):
  - ver (always): A version is MAJOR.MINOR.PATCH, optionally followed by "-" and a pre-release tag such as "beta.2". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.
  - tags (the range writes a tag): A version with a pre-release tag comes before the same version without one. Two tags compare part by part: numbers as numbers, words alphabetically, a number before a word, and a shorter tag first when all its parts match (tag parts are separated by ".").
  - cmp (a comparator or bare version): ">=V", ">V", "<=V", "<V" and "=V" compare with V; a bare "V" means "=V".
  - caret (^ in the range): "^V" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.
  - tilde (~ in the range): "~V" means >=V and below the next minor version: ~1.4.2 means >=1.4.2 <1.5.0.
  - hyphen (a hyphen range): "A - B" means >=A <=B.
  - xr (an x-range): "1.4.x" means >=1.4.0 <1.5.0, and "1.x" means >=1.0.0 <2.0.0.
  - parts (an alternative with 2+ comparators): Parts separated by spaces must all hold.
  - alts (2 alternatives): "||" separates alternatives: the range is met when one alternative is met.
  - gate (always): A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that "^", "~" or "x" imply do not count).
  - inout (yes/no rows): A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.
  - pick (ch_pick rows): The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.
Python items (id, condition: text):
  - ver (always): A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.
  - cmp (an operator besides ~= and ==P.*): ">=V", ">V", "<=V", "<V", "==V" and "!=V" compare with V.
  - wild (==P.* or ~=): "==1.4.*" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.
  - compat (~=): "~=V" means >=V together with ==P.*, where P is V without its last release number: ~=1.4.2 means >=1.4.2 and ==1.4.*, and ~=1.4 means >=1.4 and ==1.*.
  - comma (2+ specifiers): Specifiers separated by commas must all hold.
  - gate (always): A version with a pre-release meets the specifiers only if one of them, other than a "!=" one, names a pre-release version; this holds for every set of specifiers.
  - inout (yes/no rows): The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.
  - pick (ch_pick rows): The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.

## 2. Samplers (all dev-only)

| Sampler | Shape |
|---|---|
| S1 | forward: random shapes, inline range, list |
| S2 | label-first boundaries: more tagged bases (pre-release traps), candidates at bounds |
| S3 | manifest file first (package.json / pyproject.toml) + version table |
| S4 | dependency-bot narrative, inline range |
| S5 | held out: lockfile container, held-out packs, skins and registers (lockfile_comment, changelog) |

npm shapes (per alternative; 25% of ranges have two): caret 30, tilde 20, x-range 12, hyphen 12, comparator pair
20, exact 6 (%). Python shapes: compatible ~= 22, range 22, wildcard 14, range with != 12, exact with padding 10,
<= 10, > with < 10 (%). Numbers (v2.2): 1 or 2 digits per part, drawn per row (R21). Candidates: the bounds and their
neighbours, next minor and major, tagged versions of the base and within the numeric bounds, padding spellings (1.4 /
1.4.0: one kept), post-releases of versions on both sides, text-order traps (1.12 vs 1.9).

## 3. Traps and balance (H22-H24; v2.2)

- Tags in meta.edge: caret_zero, prerelease_listed, alternatives, padding, text_order_trap (text compare changes the
  answer for a listed version), at_bound.
- Slots are STRATIFIED per sampler, not drawn per seed (the pilot's share noise was one SD against the bars): a block
  of 20 seeds holds exactly 12 ch_pick bases (60%; about 50% of ROWS) and 8 yes/no bases, at seeded places. Yes/no
  bases (blocks of 4): each (meets, negative form) cell once, so gold yes is 50% and the negative forms (yn_outside /
  yn_not_meets / yn_fails, uniformly) are half of the bases. Positive bases take yn_meets, or yn_double on 12% of the
  blocks while an admitted wording passes the polarity rule (none yet: 0%). ch_pick bases: k alternates 3 / 4; per
  block of k rows of one k the outcomes A, N1 and N2 (twice at k = 4) once each.
- Bands: meets 45-55% of yes/no specs; ch_pick 45-55% of ROWS; `none` gold = 1/k +/- 3 pp per k (gold-is-longest 1/k
  +/- 2 pp: the None text is the longest option); yes_is_bad 50 +/- 5; deep <= 10% (hard); double negation >= 2% (0
  until the yn_double wordings exist: G10 fails until then).

## 4. Error models (every wrong option; prefix t36_; H8, H31; v2.2: 19 models)

lexical_compare (versions compared as text), caret_as_major (^0.m.p's upper bound read as the next major: ^0.4.2 ->
>=0.4.2 <1.0.0; only on ^0 ranges), tilde_as_caret, prerelease_ignored (the gate switched off: a tagged version meets
whenever it lies within an alternative's numeric bounds; never "tag dropped"), upper_inclusive (< read as <=, also the
computed bounds), highest_listed (range ignored), lowest_meeting, first_alternative_only (npm, two alternatives),
no_padding (Python: 1.4 differs from 1.4.0), wildcard_text (==P.* as a text prefix), post_before_release; v2.2 (F2,
supply on each side of the gold): major_only / minor_only (compare MAJOR / MAJOR.MINOR only; the lowest of the
versions they cannot tell apart wins), upper_ignored (every upper bound dropped), lowest_listed, second_listed (range
ignored), second_meeting (off by one), below_range / above_range (the listed version nearest the range below its
lowest lower bound / above its highest upper bound). A model that does not apply or gives the gold adds no option
(R12).

## 5. Relations (G-TW 100%; H25, H26; v2.2)

- Complement on 50% of yes/no bases: positive -> outside / not / fails (one third each), yn_double -> not (one
  negation fewer: the syntactic complement); a complement base -> yn_meets.
- Minimal-edit twin on 65% of bases: yes/no = the version under review replaced by another listed version on the other
  side in the R9 sense (inside <-> outside, gate included); ch_pick = the picked version's slot overwritten in place
  by an unlisted version outside the range (the list keeps its size; prediction: the next highest meeting version, or
  none), or on a none row one listed version overwritten by one inside. A base with exactly one version inside (N1,
  1/k) lands on none; such twins are kept with chance 0.7 so that the twins' None share is 1/k too; a choice twin
  whose plan cannot be filled is skipped (_tag: R17).
- equiv 15% (another container and skin), inv 10% (one attack line; gold unchanged by R13); decisions stratified (grid
  of 20). A yes/no base shares its decisions with the other base of its block of 4 with the same form polarity and the
  opposite gold, so partners add as many yes rows as no rows (yes rate 50 +/- 2).
- G4 (answer unchanged): rename the package; rename the project (and its id); list the versions in reverse order.

## 6. Haiku pools (after A38; T36's own registers, never used in training; tasks in haiku/author/TASKS.json)

- Packs: 48 authored (R19 format; >= 25 training + >= 5 held-out after check_pack, dedup and G13-seed; seeded split).
- Mode T skins (>= 75% of rows): registers dep_pr_review, ci_log, dev_chat, maintainer_email, issue, release_notes,
  dep_ticket, dep_wiki (20 each); held out (S5 only) lockfile_comment, changelog (20 each). Slots {PROJECT} (name),
  {PERSON} (name), {PKG} (id), each EXACTLY once (H32). Outside the slots the whole G-SL skin lint applies (CORE and
  EXTENDED lists, negation cues, names, LABEL_WORDS in every inflection: H12); never a version, operator, comparison
  or verdict; no blank line; no "a" / "an" before a slot; capitals mid-sentence only for CI, PR, QA and API
  (plugin.NAME_ALLOW). The 20 per register is a floor of admitted skins; a lint loss is refilled by a redo round on
  the same items (haiku/redo/, haiku/redo2/: up to 3 candidate texts per item, the first candidate in written order
  that passes every check is kept).
- Mode F documents (<= 25% of rows; the frozen pool keeps at most 1 per 3 Mode T skins of the same held-out status):
  32 training (8 registers x 4) + 10 held-out (2 x 5) from facts-only briefs {PERSON, PROJECT}; each states in plain
  words that PERSON maintains PROJECT (R1), e.g. "<PERSON>, who maintains <PROJECT>"; every other person is unnamed.
  G-SL lint_freeform; G3-H recovers project and person (plugin.extract_fields, extract.G3H_PROMPT as frozen), bar 98%
  per document; same redo rule with 2 candidates per item.
- Question wordings (lexicon kind question, sem q.t36.<form>, slots {CAND} {PKG} on yes/no, {PKG} on ch_pick; H5):
  each <= 2% of rows, so >= 18 admitted for ch_pick and yn_meets and >= 6 per complement form; authored 40 / 40 /
  14 / 14 / 14. Meanings = plugin.QUESTION_MEANINGS; G-LEX 2/2 with decoys plugin.QUESTION_DECOYS (newest listed,
  lowest meeting, "is listed"). Negations: yn_meets, yn_outside, ch_pick 0; yn_not_meets exactly one "not" / "n't";
  yn_fails "fail(s) to" only. ch_pick wordings ask for the highest listed version that meets the range or for the
  resolver's pick under these rules, never "latest", "newest", "most recent" or "upgrade"; no wording names a rule,
  an operator, a tag or an option.
  yn_double (v2.2, F5; yes iff it meets; two syntactic negations, no negative predicate; sem q.t36.yn_double,
    plugin.QUESTION_MEANINGS_V22): >= 6 wordings from the double_neg.py brief (G-LEX 2/2); none yet, so the form is
    drawn only while an admitted wording passes c2_kit.polarity (P1-P3, plugin.NEGATIVE_PREDICATES), which screens
    EVERY yes/no wording at generation (plugin.ctx_for, quarantined_wordings()).
- Attack lines: 40, {PERSON} exactly once (half also {PKG}), after the version block: a person's claim, data, never a rule (R13, H13).
- No precedence or window paraphrases: the card items are fixed program text (R16). G-SL exceptions: none.

## 7. Ambiguity points and resolution (Claude, 13-14 Oct 2026; v2.2)

Own points (v1): ^0.0.4 below 0.0.5 (R3); beta.10 after beta.2 (R2); 1.3.0-rc.1 under ^1.2.3 outside (R4, R9); 1.4 =
1.4.0 under ==1.4 (R5, R6); ==1.4.* and 1.40: no; PEP 440's extra rules never generated (R8); equal versions never
(R20); pick = highest meeting (R11); R5-R7 are tested against `packaging`.
- Haiku pass `amb:T36`: H1-H33 (haiku/ambiguity/amb_T36.json), each resolved in the R rows, section 1.2 and sections
  3-6; readings: H1 a, H2 a, H3 b, H4 b, H6 a (k includes None), H7 a, H8 a, H9 a, H11 a, H13 a, H21 b (key; letters
  at serving), H22 a, H25 a, H26 a, H27 a (B must agree or the unit drops), H28 a, H31: next major, H32 a, H33 a. Code
  (v2): card rules, ^0.0.0 never generated (H14), LABEL_WORDS widened (H12), one pack per card (R19).
- Recorded choices: no short-card rows (R4 and R7 are not world knowledge, and a short card would drop the rest of the
  rules a row needs); no held-out wordings; no masked-label, inverted or few-shot cards.
- Ruling v2.1 (13 Oct 2026; pool blockers). (1) Mode F person: the round 1 briefs never asked a document to state the
  maintainer role (G3-H read person NONE on 33 of 34): kept the field "the person who maintains the project" (R1,
  H33); haiku/redo2/ re-authors the 41 unfrozen Mode F items with the maintainer statement. (2) Mode T: "third-party"
  ("third" is a number word for the lint) and label-word slips are prompt defects; authoring.py stays as frozen, the
  redo files carry the fix.
- Ruling v2.2 (14 Oct 2026; Stage B pilot, fix iteration 1 of 2; PILOT_VERDICT F1-F7, kit choiceplan / cards /
  polarity). The failing gates came from the generator, none from a template. (1) None gold 14.5% against 1/k = 29%,
  and a wrong option told itself from the gold by version order (the gold the middle one), shape, length and digits:
  R12 plan, R21, section 4. (2) Length: the card printed every rule on every row, twice on yes/no rows: row.card plus
  row-specific items (mean 1,207 -> about 715 tokens, real tokenizer). Not chosen: a short card on 15% of rows (it
  drops rules the row needs). (3) Shares: stratified slots, twin 65%, equiv 15%, inv 10% of bases. (4) yn_double (F5),
  polarity rule. (5) Same rows under every PYTHONHASHSEED (_pool_guess sorts by key and text). Open: the yn_double
  wordings (Haiku); the G5-H re-read.
