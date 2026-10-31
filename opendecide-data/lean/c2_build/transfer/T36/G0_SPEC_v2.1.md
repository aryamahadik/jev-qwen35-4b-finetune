# G0-lite T36: dependency version-range satisfaction (transfer dev only)

One page (C2_DATA_SPEC 6.2 item 3): a semantics table, one ambiguity listing, one resolution. **v2, FROZEN** on 13 Oct
2026 after the one Haiku ambiguity pass (`c2-data-stage-a/amb:T36`; 33 points H1-H33, verbatim in
haiku/ambiguity/amb_T36.json; it read v1, sha e7800917). This file's sha is `plugin.T36Plugin.G0_SHA256`;
`validate_plugin` refuses the plugin if the file changes, so a later change is a new version with a new sha.
**v2.1** (13 Oct 2026, ruling v2.1 in section 7): sections 6 and 7 wording only; no R row, card, gate or bar changed.
Spec 2.2 (T36: 300 items, held out, never trained) and 3.20 (npm semver and PEP 440 semantics reimplemented twice);
it tests transfer of matching and precedence skills (T28, T35). Every row is dev-only (meta.dev_only = true).
Code: plugin.py (solver A, construction, rendering), solver_b.py (solver B), fixtures.py (test stand-ins),
authoring.py (the Haiku authoring tasks). Ids (H30): R1-R20 are rows of the semantics table, S1-S5 name samplers
only, H1-H33 Haiku points. Terms from outside this page (H10): spec 3.0 (packs, registers, wordings, Mode T / F,
balance, depth), spec 4.1 (overlay: complement, minimal-edit twin, equiv, inv; a unit = a base row and its partners),
spec 6.3 (G2 solver B = A on 100%, G3 parse round trip, G4 metamorphic, G-SL, G-LEX, G-TW, G3-H, G5-H), PREREG A38
(OHS-4 frozen before any data), kit README (QuestionForm, build_options, KitCtx.pick, lexicon kind "question").
None of them decides an answer: every rule an answer needs is on the row's card, quoted in full below (R13).

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
| R12 | Options (H6, H7) | ch_pick rows only (yes/no rows have none). k = 3 or 4 options, the None option included and shown on every ch_pick row; k is drawn 50/50 from the row key (family, seed, sampler, form) before the gold and never lowered. Wrong options = R14 error-model outputs, minus the gold, minus `none`; equal outputs merge into one option (all its models recorded). Gold `none`: k - 1 versions; else gold + None + k - 2 versions. A spec whose models give too few distinct versions for its k is redrawn (a twin is skipped). Order: kit build_options (hash order, gold position uniform per k) |
| R13 | Closed world | The card is the box for the row's style (section 1.2), verbatim; its last line: "The range, the listed versions and these rules are complete: nothing else changes the answer." "Published versions" on the row = the listed versions, all of them (H28). Narrative, attack lines (section 6) and names never change an answer (H13, H33) |
| R14 | Error models | Section 4; each is solver A with one switch and answers ch_pick only |
| R15 | Solver A | ast_interpreter: the range parsed into alternatives of (operator, sort-key) tests and prefix tests, one interpreter over tuple sort keys, the gate per alternative; pick = max by key. Gold = solver A |
| R16 | Solver B | interval_scan (solver_b.py, from this page and the card): its own parser of the RENDERED row (card compared verbatim); each alternative becomes ONE interval (bounds with inclusive flags) + != exclusions + ==P.* prefixes + the gate; versions ordered by a pairwise compare function (loops, zero padding), never sort keys; pick = the first meeting version of the list sorted highest first. G2: B = A on 100%, else the unit is dropped and counted (H27) |
| R17 | Construction | _tag(): interval arithmetic on version triples / padded releases; builds boundary candidates and predicts twins. A guard refuses a spec where _tag and solver A differ on a listed version. Twins (section 5): G-TW checks _tag's prediction against solver A on the twin, and G2 runs solver B on the twin row (H26) |
| R18 | Depth (H1, H29) | Operations the reader performs whose result is not printed (every RULE is printed on the card; no intermediate value is): compare (always), desugar (^, ~, x-range, ~= or ==P.* in the range), gate (yes/no: the version under review is tagged; ch_pick: a listed tagged version lies within an alternative's numeric bounds but fails its gate). depth = their count, 1-3; deep = 3, kept only on seeds whose hash is < 0.10 (other seeds redraw), so deep <= 10% of specs: a hard limit (test), flagged meta.deep, reported apart |
| R19 | Packs (spec 3.0) | A pack = one invented software project: name (2-3 capitalised ASCII words), 3 package ids (lower-case ASCII words joined by single hyphens, 4-24 characters, no digits), 2 maintainer names (two capitalised ASCII words); `check_pack`: no label word (R20), no negation cue, no reserved G4 value (yarrow-sync, Lowmoor Desk). One pack per card: card ordinal = sampler index x 24 + style x 12 + card (0-11), modulo the pool; S5 draws from held-out packs. Frozen pool: >= 25 training + >= 5 held-out packs; the 8 + 2 code stand-ins serve tests only |
| R20 | One spelling, words | No two listed versions are equal under R5 (never 1.4 and 1.4.0 both), so the pick is unique. LABEL_WORDS (G-SL, every inflection; H12): meets meet met satisfies satisfy outside inside within compatible incompatible matches match fit fitting installs install resolves resolve allowed exclude included supported unsupported newest latest oldest highest lowest newer older higher lower upgrade downgrade stable unstable prerelease beta alpha breaking |

### 1.1 Program text (H9, H28)

- State: narrative skin, blank line, the range block, blank line, the version list, then on yes/no rows "Version
  under review: V". Range blocks: inline "Declared range for PKG in project ID (npm style): R" / "Declared specifiers
  for PKG in project ID (Python packaging style): R"; package.json (one JSON line, name and dependencies);
  pyproject.toml ([project] name + one dependencies entry "PKG R"); lockfile request (sampler S5: "lockfile request
  for ID:", "package: PKG", "wanted: R", where R is the declared range in the card's style, never one version).
  Version list: "Published versions of PKG: a, b, ..." or the one-column table (sampler S3). Attack line (inv rows):
  after the version block, blank line first.
- Instructions: the style's card (box below, verbatim), blank line, the question wording.

### 1.2 The cards (program text; plugin.CARD, solver_b.NPM_CARD / PEP_CARD are copies; a test checks they are equal)

npm: "How to read this version range (npm style):" then bullets: (1) "A version is MAJOR.MINOR.PATCH, optionally
followed by "-" and a pre-release tag such as "beta.2". Compare versions by MAJOR, then MINOR, then PATCH, each as a
number. A version with a pre-release tag comes before the same version without one. Two tags compare part by part:
numbers as numbers, words alphabetically, a number before a word, and a shorter tag first when all its parts match (tag
parts are separated by ".")." (2) "">=V", ">V", "<=V", "<V" and "=V" compare with V; a bare "V" means "=V"." (3) ""^V"
means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2
means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5." (4) ""~V" means >=V and below the next minor version: ~1.4.2 means
>=1.4.2 <1.5.0." (5) ""A - B" means >=A <=B. "1.4.x" means >=1.4.0 <1.5.0, and "1.x" means >=1.0.0 <2.0.0." (6) "Parts
separated by spaces must all hold. "||" separates alternatives: the range is met when one alternative is met." (7) "A
version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same
MAJOR.MINOR.PATCH and a pre-release tag (bounds that "^", "~" or "x" imply do not count)." (8) "A version is inside
the range when it meets the range, and outside the range when it does not, even when its numbers lie between the
bounds." (9) "The resolver installs the highest listed version that meets the range; when no listed version meets it,
the resolver installs none of them." Last line: the R13 sentence.

Python: "How to read these version specifiers (Python packaging style):" then bullets: (1) "A version is a release of
numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then
by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals
1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release."
(2) "">=V", ">V", "<=V", "<V", "==V" and "!=V" compare with V." (3) ""==1.4.*" holds for every version whose release
starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule
below." (4) ""~=V" means >=V together with ==P.*, where P is V without its last release number: ~=1.4.2 means >=1.4.2
and ==1.4.*, and ~=1.4 means >=1.4 and ==1.*." (5) "Specifiers separated by commas must all hold." (6) "A version with
a pre-release meets the specifiers only if one of them, other than a "!=" one, names a pre-release version; this holds
for every set of specifiers." (7) "The specifiers together form the range. A version is inside the range when it meets
the specifiers, and outside the range when it does not, even when its numbers lie between the bounds." (8) "The
resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the
resolver installs none of them." Last line: the R13 sentence.

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
<= 10, > with < 10 (%). Candidates: the bounds and their neighbours, next minor and major, tagged versions of the base
and within the numeric bounds, padding twins (1.4 / 1.4.0), post-releases, text-order traps (1.12 vs 1.9).

## 3. Traps and balance (H22-H24)

- Tags in meta.edge: caret_zero, prerelease_listed, alternatives, padding, text_order_trap (comparing as text changes
  the answer for a listed version), at_bound.
- Balance is on meets-status (H22): a block = seeds 2b and 2b + 1 of one sampler; a hash of the block picks which seed
  targets "meets"; when both are yes/no specs, one meets and one does not. Gold yes = meets (yn_meets) or not meets
  (complements); the form is drawn apart from the target, so gold yes is 50% in expectation (measured 50.5%).
- Shares are per-seed hash draws: targets, not quotas, so no rounding (H24). Base forms: ch_pick 40%; of yes/no bases
  45% take a complement form, one of the three uniformly (one third each). Separately, 50% of yes/no bases get a
  complement PARTNER row (section 5) (H23). ch_pick `none` gold on about 15% (the list then holds only versions outside
  the range). Tested bands: meets 45-55% of yes/no specs, ch_pick 30-50% of specs, `none` 8-25% of ch_pick specs,
  deep <= 10% (hard). Measured rows per base 2.04; row shares ch_pick 34%, yn_meets 34%, each complement form 10-11%.

## 4. Error models (every wrong option; prefix t36_; H8, H31)

lexical_compare (versions compared as text), caret_as_major (^0.m.p's upper bound read as the next major: ^0.4.2 ->
>=0.4.2 <1.0.0; only on ^0 ranges), tilde_as_caret, prerelease_ignored (the gate switched off: a tagged version meets
whenever it lies within an alternative's numeric bounds; never "tag dropped"), upper_inclusive (< read as <=, also the
computed bounds), highest_listed (range ignored), lowest_meeting, first_alternative_only (npm, two alternatives),
no_padding (Python: 1.4 differs from 1.4.0), wildcard_text (==P.* as a text prefix), post_before_release. A model that
does not apply or gives the gold adds no option (R12).

## 5. Relations (G-TW 100%; H25, H26)

- Complement on 50% of yes/no bases: positive -> outside / not / fails (one third each); a complement base -> positive.
- Minimal-edit twin tried on 60%: yes/no = the version under review replaced by another listed version on the other
  side in the R9 sense (inside <-> outside, gate included); ch_pick = the picked version's slot overwritten in place
  by an unlisted version outside the range (the list keeps its size; prediction: the next highest meeting version, or
  none), or on a none row one listed version overwritten by one inside. Predictions come from _tag (R17).
- equiv 12% (another container and skin), inv 8% (one attack line; gold unchanged by R13).
- G4 (answer unchanged): rename the package; rename the project (and its id); list the versions in reverse order.

## 6. Haiku pools (after A38; T36's own registers, never used in training; tasks in haiku/author/TASKS.json)

- Packs: 48 authored (R19 format; >= 25 training + >= 5 held-out after check_pack, dedup and G13-seed; seeded split).
- Mode T skins (>= 75% of rows): registers dep_pr_review, ci_log, dev_chat, maintainer_email, issue, release_notes,
  dep_ticket, dep_wiki (20 each); held out (S5 only) lockfile_comment, changelog (20 each). Slots {PROJECT} (name),
  {PERSON} (name), {PKG} (id), each EXACTLY once (H32). Outside the slots the whole G-SL skin lint applies: CORE and
  EXTENDED lists (digits and number words, dates, relative time, quantity, quantifiers, modals, hedges, status and
  operator words), negation cues, names, plus LABEL_WORDS in every inflection (H12; "number" covers number words).
  Never a version, operator, comparison or verdict; no blank line; no "a" / "an" before a slot. Capitals
  mid-sentence only for CI, PR, QA and API (plugin.NAME_ALLOW; every other one is a name). The 20 per register is a
  floor of admitted skins (freeze.py reports a shortfall, never absorbs it). A lint loss is refilled by a redo round
  on the same items (same qids; haiku/redo/, haiku/redo2/); a redo item may ask for up to 3 candidate texts, and the
  first candidate in written order that passes every check is kept, the rest discarded (one skin per item at most).
- Mode F documents (<= 25% of rows; the frozen pool keeps at most 1 per 3 Mode T skins of the same held-out status):
  32 training (8 registers x 4) + 10 held-out (2 x 5) from facts-only briefs {PERSON, PROJECT}. The document states
  in plain words that PERSON maintains PROJECT (R1: the person is the project's maintainer), e.g. "<PERSON>, who
  maintains <PROJECT>" or a field "maintainer=<PERSON>"; every other person is unnamed and nobody else is called a
  maintainer. G-SL lint_freeform and the name check; G3-H recovers project and person, the person being the maintainer
  (plugin.extract_fields and extract.G3H_PROMPT as frozen), bar 98% per document. Same redo rule as Mode T with 2
  candidates per item; G3-H reads every lint-clean candidate and the first that passes both is kept.
- Question wordings (lexicon kind question, sem q.t36.<form>, slots {CAND} {PKG} on yes/no, {PKG} on ch_pick; H5):
  each <= 2% of rows, so >= 18 admitted for ch_pick and yn_meets and >= 6 per complement form; authored 40 / 40 /
  14 / 14 / 14. Meanings = plugin.QUESTION_MEANINGS; G-LEX 2/2 with decoys plugin.QUESTION_DECOYS (newest listed,
  lowest meeting, "is listed"). Negations: yn_meets, yn_outside, ch_pick 0; yn_not_meets exactly one "not" / "n't";
  yn_fails "fail(s) to" only. ch_pick wordings ask for the highest listed version that meets the range or for the
  resolver's pick under these rules, never "latest", "newest", "most recent" or "upgrade"; no wording names a rule,
  an operator, a tag or an option.
- Attack lines: 40, {PERSON} exactly once (half also {PKG} once), after the version block. A person's claim or push
  (e.g. that the newest version is always fine or that tags do not matter); data, never a rule: R13 keeps gold (H13).
- No precedence or window paraphrases: the card is fixed program text that solver B reads verbatim. G-SL exceptions:
  none.

## 7. Ambiguity points and resolution (Claude, 13 Oct 2026; v2)

Own points (v1): (1) ^0.0.4: below 0.0.5 (R3). (2) beta.10 after beta.2 (R2). (3) 1.3.0-rc.1 under ^1.2.3: outside
(R4, R9). (4) 1.4 = 1.4.0 under ==1.4 / !=1.4 (R5, R6). (5) ==1.4.* and 1.40: no (numbers). (6) ~=1.4 = ==1.* vs
~=1.4.0 = ==1.4.* (card). (7) PEP 440's extra rules: never generated (R8). (8) equal versions: never (R20). (9) pick:
highest meeting, never the highest listed or the first listed (R11). Tests also check R5-R7 against `packaging`
(SpecifierSet.contains with pre-releases on, plus the R7 gate) on every generated Python-style spec.
Haiku pass `amb:T36`: H1 gate printed or depth item; H2 Python gate in plain windows, R8 exhaustive; H3 ==P.* vs gate;
H4 inside / outside; H5 wordings off-page; H6 k and None; H7 duplicate options; H8 prerelease_ignored; H9 lockfile
style; H10 outside terms; H11 which named versions count; H12 skin word list; H13 attack lines; H14 partial operands;
H15 tokens and precedence; H16 tag parts; H17 Python spellings; H18 ~= with one number or a tag; H19 !=P.*; H20 bare
Python version; H21 key format; H22 balance unit; H23 two complement shares; H24 rounding; H25 twin replace or add;
H26 twin guard; H27 newest, A / B disagreement; H28 published vs listed; H29 depth count; H30 S-id clash; H31
caret_as_major; H32 each once; H33 inert fields.
- Code changes (v2; both solvers and the generator): card bullets (H3, H4, H5, H11, H16; R4, R7, R9, R11) in plugin.CARD
  and solver_b's copies; ^0.0.0 never generated (H14); the option count k never lowered (H6, R12); LABEL_WORDS
  widened (H12, R20); packs: one pack per card from check_pack-clean packs (R19; spec 3.0); QUESTION_MEANINGS and
  QUESTION_DECOYS for G-LEX (H5, H27). Every other point is stated, not coded: H1 (R4, R7, R18), H2 (R7, R8), H7
  (R12), H8, H31 (section 4), H9, H28 (1.1, R13), H10, H30 (header), H13 (R13, section 6), H14, H15 (R3), H17
  (R5), H18-H20 (R6), H21 (R11), H22-H24 (section 3), H25, H26 (section 5, R17), H27 (R11, R16), H29 (R18), H32,
  H33 (R1, section 6). Readings chosen: H1 a, H2 a, H3 b, H4 b, H6 a (k includes None), H7 a, H8 a, H9 a (the card
  names the style), H11 a, H13 a, H21 b (key; letters at serving), H22 a, H25 a, H26 a, H27 a (B must agree or the
  unit drops), H28 a, H31: the next major, H32 a, H33 a.
- Recorded choices: every row prints the full card (no short-card rows: R7 and R4 are not world knowledge); no held-out
  wordings (S5 holds out packs, registers and the container); no masked-label, inverted or few-shot cards in v2.
- Ruling v2.1 (Claude, 13 Oct 2026; pool blockers after the extraction round). (1) Mode F person: the round 1 briefs
  (authoring.freeform_prompt) never asked a document to state the maintainer role, so G3-H read person NONE on 33 of
  34 documents. Kept: the G3-H field "the person who maintains the project" (R1, H33). Not chosen: widening it to "the
  one person named in the text" (a document naming PERSON in another role would pass, which weakens the fact-lock),
  or leaving Mode F empty (lowers the section 6 targets). Fix: haiku/redo2/ re-authors the 41 unfrozen Mode F items
  with the maintainer statement (section 6), then one G3-H read of the candidates with the unchanged prompt.
  (2) Mode T: "third-party" in authoring.HEAD and the dep_wiki style ("third" is a number word for the lint) and
  label-word slips (chunker refuses label words in an authoring prompt, so redo prompts describe them by function)
  are prompt defects. authoring.py stays as frozen (its prompt shas name the round 1 task ids); the redo task files
  carry the fixed text, and the 20 per register stays a floor.
