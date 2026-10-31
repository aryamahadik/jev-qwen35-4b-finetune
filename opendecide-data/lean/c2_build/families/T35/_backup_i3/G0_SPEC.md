# G0-lite T35: path-rule access, robots-style (may the crawler fetch this URL? which line decides?)

C2_DATA_SPEC 2.1 (row T35, 600 rows, wave 1, agent tier) and 3.2; PREREG_FINAL A37 (A38: OHS-4 frozen). The card is the
only law (closed world, M10). Its rules follow RFC 9309 where both speak; where the card is silent the generator never
builds the case (redirects, other directives, comments, non-ASCII codes; H2, H23). urllib.robotparser is never a verifier.
v4 = v3 (v2 frozen after the one Haiku ambiguity pass, section 7; + packs, section 6) + pilot fix iteration 1 (section 9); sha256: plugin.py.
Labels: M1-M25 = semantics items, S1-S5 = samplers, H1-H33 = ambiguity points (section 7); glossary in H26.

## 1. Semantics table

| # | Item | Semantics (exact) |
|---|---|---|
| M1 | File | 1-6 groups and 1-8 rule lines in all (User-agent lines not counted; H1). A group = 1+ `User-agent:` lines (a product token, id slot `A<i>`, letters and `-`; or the literal `*`), then 1+ rule lines `Allow:` / `Disallow:` (effect = category slot `E<n>`, pattern = glob slot `P<n>`). At most one `*` group, and `*` never shares a group with a token (H3). Well formed only (H2): no comment, no other directive, no blank line inside a group, no rule before the first User-agent, no empty value, names exactly `User-agent` / `Allow` / `Disallow` + `: `. Every (effect, pattern) pair is distinct in a file, twins included (H33); choice rows: distinct beyond letter case too |
| M2 | Patterns | start with `/`; literal characters are letters, digits and `/ - _ . ? = & %` (`%` only inside `%2F`); `*` anywhere but never doubled; `$` only as the last character and never right after `*`. No pattern holds an unreserved `%XX` |
| M3 | Request | crawler token (id slot `UA`); URL (url slot `URL`: `https://<site-slug>.example` + a path that starts with `/`; no port, user info or fragment); printed path (derived slot `PATH` = the URL from the first `/` after the host, query included, as written: a literal string, never a pattern; it holds only letters, digits, `/ - _ . ? = &` and uppercase `%XX`, never `*`, `$`, `~` or a stray `%`; H4); optional robots.txt fetch status (category slot `STATUS`, M9). On a label-blind 60% of URLs one path segment or the file name starts with a capital, so lines with capitals match as often as others (review fix: with all-lowercase paths a capital marked a non-matching line) |
| M4 | Group choice | a group applies when one of its User-agent values equals the token ignoring ASCII case (equality, never prefix: `FernhillBot-News` is not `FernhillBot`). All applying groups are combined (file order). If none applies, the `*` group applies; if there is no `*` group, no group applies. The applying groups' lines are the applying lines; no other line counts (H10) |
| M5 | Decoding | in the path, each `%XX` whose byte is an ASCII unreserved character (A-Z a-z 0-9 `- . _ ~`) is decoded; every other `%XX` stays as written (only `%2F` occurs). The generator writes uppercase hex and codes only for those characters and `/`, so hex-case and non-ASCII readings never differ; both solvers accept either case (H12). Patterns are not decoded (M2) |
| M6 | Match | a line matches when its pattern matches the START of the decoded path: `*` = any run (empty and `/` included); final `$` = the path ends there; every other character exact and case-sensitive. The query string is part of the path |
| M7 | Length | characters of the pattern as written, `*` and `$` one each, `%2F` three; not the matched span, not literals only, not decoded (H8). `Allow: /*` vs `Disallow: /a` on `/a/b`: 2 vs 2, a tie, Allow |
| M8 | Decider | among matching applying lines the longest decides; an Allow and a Disallow line of equal (longest) length: Allow (equal length only; H9). No applying line matches (or no group applies): the crawler may fetch (card item 6, its own item; H11). A matching line of a group that does not apply decides nothing |
| M9 | Status | closed set (H5): `200 OK`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `410 Gone`, `500 Internal Server Error`, `502 Bad Gateway`, `503 Service Unavailable`, `no response (server unreachable)`; never 1xx, 3xx, 429, 504 or another 2xx. Always the robots.txt fetch, never the URL's. 200 or no status line: M4-M8. 4xx: may fetch; 5xx or no response: may not fetch; both override the lines (card item 7; H7) |
| M10 | Closed world | "The file is the robots.txt of the URL's site, and the file, the request and these rules are complete: nothing else changes the answer." (every card). The file shown is what the site's robots.txt holds; the status says how its fetch went, and on 4xx / 5xx rows item 7 alone decides (H7). Nothing else counts: cached copies, file age, meta robots, X-Robots-Tag, crawler habits, PURPOSE, other hosts, notes or attack lines (H16, H17) |
| M11 | yn_fetch; yn_double_neg | positive polarity: yes iff may fetch (H20). yn_double_neg asks it with two syntactic negations (k_syn 2) on the positive bases of 12% of 4-base blocks (both outcomes; spec 3.0: >= 2% of yes/no rows). Wording rule (c2_kit.polarity P1-P4; first pilot G5-H: 3 wrong golds): an explicit outer frame "is it not the case / true / so that" over "not" + a word of PERMISSION (allowed, permitted, entitled, cleared, authorized); never a negative predicate (bar, block, close, exclude, forbid, stop, skip, off-limits, breach ...), never a contracted frame ("isn't it ..."). No frozen wording passes it, so the form is not drawn (0%) until Haiku re-authors and 2/2 admits one (F1) |
| M12 | yn_skip (antonym) | negative polarity: yes iff may not fetch ("must skip", "fetching ... disallowed"); no negation cue |
| M13 | yn_not_allowed (syntactic) | yes iff may not fetch ("not allowed to fetch"; exactly one negation cue more than yn_fetch) |
| M14 | yn_prevented (implicit) | yes iff may not fetch ("prevent ... from fetching", "lack permission"; one implicit cue). Rule-based: the item-6 default counts as permission, so "lack permission" = may not fetch under the card (H18) |
| M15 | ch_line | gold = key of the M8 decider (`allow:<pattern>` / `disallow:<pattern>`), or `none` when no applying line matches. Only rows with status 200 or none and a unique decider: no two equal-longest lines of the winning effect (a gold-none row has no decider and stays; the losing Disallow of an Allow tie is no decider, so tie rows stay; H13). No query string in the URL (the query rule is tested on yes/no rows). Display plan (c2_kit ChoicePlan, fixed by the seed's place in its sampler's stratified stream BEFORE any structure; F3; H14): k = 3 or 4 shown options counting the always-shown "No applying line matches (so the crawler may fetch the URL)"; the gold IS that option on exactly 1/k of the rows of each k (one per block of k), its position is uniform per k, its 0-based rank by visible text length (`Allow: <p>` / `Disallow: <p>`, then code point) among the k - 1 line options is uniform. The sampler draws structure until solver A's gold agrees with the plan (label-first, never relabelled). Wrong lines = error-model outputs (section 4), gold and `none` dropped, pattern >= 4 characters, the nearest look-alikes of the reference line (gold; on a gold-none row a hash-drawn candidate) by profile ("*", final "$", "?", capital, file ending, final "/", digit, effect), then word count and length (`matched_models`), on each side of the gold as its rank asks; texts differ beyond letter case, else the structure is redrawn |
| M16 | Precedence clauses | lexicon kind `precedence` (3/3): `{LONGEST}` sem `prec.robots_longest` (M7 + M8 first half), `{TIE}` sem `prec.robots_tie_allow` (Allow wins at equal longest length only). G-LEX meaning list also offers `prec.robots_literal_longest`, `prec.robots_first`, `prec.robots_tie_disallow`, `prec.robots_allow_always` (never on cards). Program check before admission (authoring.precedence_problems; H8, H9): a {LONGEST} form names its measure (character(s), `"*"` and `"$"`); a {TIE} form names `Allow`, `Disallow` and equal length (equal / same / tie); neither says first, last, order, priority, specific, literal, always or a number word but "one" |
| M17 | Card styles | one per row from the row key (label-blind): full 20%, compact 65%, short 15% (the spec 3.0 share); same rules, `{LONGEST}` / `{TIE}` filled with admitted forms, closed-world sentence last. Item 7 (the status rule, last bullet in the short card) stands only when the request block shows a fetch status: a rule the answer cannot need is not stated, and the card is the largest part of a row's tokens (F4: the 70/30 split of rows made the mean 811 against 800) |
| M18 | Card placement | c2_kit.cards.place_rules: yes/no rows row.card (the served prompt prints it once, as the definitions block); choice rows the head of the instructions (the only place a choice row prints it; counted twice) |
| M19 | Rules containers | robots (S1, S2, S4): `robots.txt of the site:` + `=== begin robots.txt ===` ... `=== end robots.txt ===`, groups separated by one blank line, each group's User-agent lines then its rule lines, file order. table (S3): `robots.txt of the site, one table row per line (rows with the same group number form one group):` + `\| group \| line \| value \|`; one row per User-agent value or rule line in file order; `line` = the directive name exactly, `value` as written, case kept (H21). json (S5, held out): `robots.txt of the site, as parsed into JSON by the site's tools:` + `{"groups": [{"user_agents": [...], "lines": [{"type": "Allow", "pattern": "..."}]}]}` (key `pattern`; `type` exactly `Allow` / `Disallow`; H22) |
| M20 | Request block | `Fetch request:` / `- crawler product token: {UA}` / `- URL: {URL}` / `- path to check (query included): {PATH}` / [`- robots.txt fetch status: {STATUS}`] |
| M21 | Row layout | state = narrative skin, blank line, rules block, blank line, request block [, blank line, attack line]. Yes/no rows: row.card = the card (the served prompt prints it once, as the definitions block), instructions = the question wording. Choice rows: instructions = card, blank line, question (the served layout prints row.card on yes/no rows only). H21, H28 |
| M22 | Narrative facts | `SITE` (name), `OPERATOR` (name), `PURPOSE` (category: search indexing, web archiving, price comparison, accessibility checks, link checking, academic research, link previews); inert (G4); Mode F rows check them by G3-H |
| M23 | Depth | status rows 1; else 1 (longest match) + 1 if the file has > 1 group (all groups, not only applying ones; H31) + 1 if the URL holds `%XX`; the tie step adds nothing. deep = depth 3, kept <= 10%; the printed path is the intermediate |
| M24 | Solver A | `trie_longest_match`: token index for M4; one char trie of the applying patterns (`*` = star edge, final `$` = anchored end) walked once over the decoded path (DFS); max length, Allow on tie; status class: absent = 2xx, `no response` = 5xx, else the code's hundreds digit (H6) |
| M25 | Solver B | `regex_compile` (solver_b.py, written from this page): own readers for the three containers (anything outside M1 / M19 is refused) and the request (a URL with no path is refused); each applying pattern compiled to a regex (`.*`, `\Z`) and tried one by one with `re.match`; explicit pairwise length comparison; status and question by lookup tables. Imports no solver-A code |

Card texts (M17; the status item 7 / last bullet only when the request shows a fetch status):
```
[full]
Robots rules (they decide this request):
1. Group: a group applies if one of its User-agent values equals the crawler's product token, ignoring case (equal, not just a prefix). All applying groups are combined. If none applies, the "*" group applies; if there is none, no group applies. The lines of the applying groups are the applying lines; no other line counts.
2. Path: the URL from the first "/" after the host, query included (the path to check). Decode each "%XX" that encodes an ASCII letter, digit, "-", ".", "_" or "~"; keep every other "%XX" as written.
3. Match: a line matches if its pattern matches the start of the path. "*" matches any run of characters (even empty, even "/"); a final "$" means the path must end there; every other character must match exactly, case-sensitive.
4. {LONGEST}
5. {TIE}
6. If no applying line matches, the crawler may fetch the URL.
7. robots.txt fetch status, which overrides items 1-6: 2xx or none shown: use the lines. 4xx: the crawler may fetch any URL on the site. 5xx or no response: it may fetch none.
<closed-world sentence M10>
[compact: items 4-6 as in the full card; items 1-3 and 7 differ]
Robots rules:
1. Group: a group applies if a User-agent value equals the crawler's token, ignoring case (equal, not a prefix); all applying groups are combined. If none applies, the "*" group applies; if there is none, no group applies. Their lines are the applying lines; no other line counts.
2. Path: the URL from the first "/" after the host, query included. Decode each "%XX" for an ASCII letter, digit, "-", ".", "_" or "~"; keep every other "%XX" as written.
3. Match: a line matches if its pattern matches the start of the path: "*" matches any run (even empty, even "/"); a final "$" means the path must end there; every other character must match exactly, case-sensitive.
7. robots.txt fetch status overrides items 1-6: 2xx or none shown: use the lines; 4xx: it may fetch any URL; 5xx or no response: it may fetch none.
[short]
Robots rules, short form:
- Group: the groups whose User-agent value equals the crawler's token (case ignored; all combined), else the "*" group, else none; only their lines apply.
- Path: the URL from the first "/" after the host, query included; decode "%XX" only for ASCII letters, digits, "-", ".", "_" and "~".
- Match: a pattern matches the start of the path; "*" is any run ("/" and empty included); a final "$" means the path ends there; case matters.
- {LONGEST}
- {TIE}
- No applying line matches: may fetch.
- robots.txt status (overrides the lines): 4xx: may fetch any URL; 5xx or no response: may fetch none; 2xx or none shown: use the lines.
<closed-world sentence M10>
```

## 2. Samplers (>= 4 training shapes + held-out S5)

| Sampler | Shape | Rules container | Notes |
|---|---|---|---|
| S1 | forward: random file around the path, outcome planned first, file kept only if it reaches the plan | robots | groups: named 42%, `*` 43%, combined 7%, no group 8% (only when no line should match) |
| S2 | label-first near miss: the decider is built first, then losers one condition away (equal-length tie, shorter opposite line listed first, longer non-matching near miss) | robots | ties 90% of Allow-decided files (ch_line 60%) |
| S3 | table-first: S1 shapes rendered as a table | table | |
| S4 | group conflicts and fetch status: more combined groups, case-variant tokens, look-alike groups, 30% of the yes/no bases show a status line (mostly 200 OK) | robots | |
| S5 | held out (mixdev only): S1 shapes, held-out skins, registers, wordings and packs | json | dev_only; the 8 held-out packs only (section 6) |

Display choices are label-blind (container by sampler; card style, status shown, skin, wording, forms from seeded hashes; the
choice plan from the stream, M15). The outcome is planned first. Each block of 88 seeds of a sampler holds exactly 41
choice bases (46.6%) at seeded places; each block of 4 yes/no bases holds each (outcome, polarity) cell once, one negative form
and one partner form (so every form is 50% yes).

## 3. Traps, balance targets and question shares (H29: a target holds when the measure is inside its band)

| Item | Target [unit-test band] | Measured, v4 (16,000 S1-S4 specs; "rows" = a 1,000-row dev pilot, seeds from 1,100,000) |
|---|---|---|
| Yes/no share of ROWS (partners and twins counted: yes/no bases carry ~2.4 rows, choice ~1.1); choice ("which line decides") | 70% / 30% [67-73] (G10) | specs 53.4% yes/no; rows 69.3% |
| Gold yes = share of gold 1 over yes/no rows; may-fetch outcome = share of yes/no rows whose outcome is may fetch (H20) | 50 ± 2 each [48-52] | 50.0%; 50.0% |
| Yes = bad outcome (bad = may not fetch, so yes is bad on the negative forms) among gold-yes rows | 50 ± 5 [45-55] | 50.0% |
| ch_line gold `none` = 1/k of each k (F3; kit plan); the abstain option wrong on rows that show it | 33.3% at k = 3, 25% at k = 4, mean ~29% [27-32]; >= 50% (hard) | 33.4% / 25.0% / 29.2%; 72.6% |
| Trap `tie`: equal-length Allow/Disallow tie decides | 30% [22-38] | 24.3% |
| Trap `first_match_loses`: the first listed matching applying line has the losing effect | 30% [22-38] | 27.9% |
| Trap `group_conflict`: named group vs `*` / look-alike / first-group-only reading flips the outcome | 25% [18-35] | 32.6% |
| Status line shown (spec 3.2: about 15% of rows); trap `status` = 4xx / 5xx / no response, which decides alone and so is read by G6's metadata view (a perfect rule scores 0.5 + s / 2 <= 0.52): re-frozen (F2) | line on 15% of rows [10-20]; 4xx / 5xx <= 4% of yes/no rows, aim 2-3% (spec 3.2's 15% cannot hold under G6) | line 16.2% of yes/no specs; 4xx / 5xx 1.6% |
| Also tagged: `percent`, `token_case`, `combined`, `no_group`; deep (depth 3) | deep <= 10% (hard cap) | 9.1% / 16.0% / 7.6% / 0.7%; 7.7% |
| G6 pre-check: URL-free single features (majority effect, longest line's effect, first line's effect, identical-pattern pair, line count, group count) | each <= 55% on 16,000 specs [unit test: <= 58% on 2,000, noise allowance]; the binding G6 gate is spec 6.3 | max 53.5% (majority) |
| Length (H28): real tokens = mixer.token_counts (pinned Qwen3.5-4B tokenizer on the served cygnet / schema_branch_mark prompt, instructions twice) | every row <= 2,000 and family mean <= 800 real tokens; the kit estimate (3 chars / token) is a pre-check only | frozen pools, 70/30 rows: mean 727 (yes/no 619, choice 970), max 1,194 (v3 at 82/18 rows: 767; at 70/30 with the v3 card it projects to 811) |

Non-deciding lines of a yes/no file are effect-balanced so the file's effect mix does not give the label away: losing lines
are matched by same-effect supporters, longer near misses take the losing effect 80% of the time, identical-pattern pairs
occur on both outcomes; on a ch_line file their effects are coin flips. Pressure (attack) lines never change the label.

## 4. Error models (every wrong ch_line option is the output of one)

`first_match`, `last_match`, `effect_order` (longest Disallow if any matches), `robots_allow_wins` (longest Allow if any matches), `robots_disallow_wins_tie`,
`robots_length_literals_only` (length without `*`/`$`), `robots_star_group_over_named`, `robots_lookalike_group`,
`robots_first_group_only`, `robots_merge_star_group`, `robots_ignore_end_anchor` (final `$` read as a prefix pattern),
`robots_star_stops_at_slash`, `robots_whole_path` (pattern must match the whole path), `robots_no_percent_decode`,
`robots_path_case_ignored`, `robots_query_ignored`. Each returns a line key, `none`, or nothing (does not apply).
Choice rows carry 1-3 "bait" lines that one of these models reads as a match, each made from a MATCHING pattern drawn
like the deciders (stars, `$`, capitals at the deciders' own rates; bare prefixes of the path read as wrong in the pilot's
options-only views): a case flip (a capital to lower case when the pattern has one); an early anchor, i.e. a matching
pattern + final `$` that stops before the path ends (legal under M2; `robots_ignore_end_anchor` reads it as a match; H15;
one `$` bait on 20% of rows, `$` deciders on 40%). The non-option near lines of a ch_line file (typo, extra letter,
sibling) have no case, anchor or `/*.ext$` form, and a no-line file holds as many lines as a line file.

## 5. Relations

- Complement (45% of yes/no bases, drawn per block of 4 so a partner form gets as many yes as no golds; same call_id):
  positive base -> yn_skip 40% / yn_not_allowed 30% / yn_prevented 30%; yn_double_neg base -> yn_not_allowed; negative base -> yn_fetch.
- Minimal-edit twin (90% of yes/no bases when one exists; own call_id): (a) status twin (from a base that shows 4xx / 5xx, or 20% of 2xx ones; F2): STATUS moves to a 5xx key
  (outcome was may fetch) or a 4xx key (was may not) and the outcome flips by M9; (b) effect twin: the one deciding
  line's effect flips; it keeps its length, so its new effect wins; (c) pattern twin (a no-line row has no line to flip): the
  pattern of an applying Disallow line becomes one that matches. Never built over an existing pair (M1; H33). The prediction is the flipped outcome.
- Equiv (13% of bases): another rules container (robots <-> table; json -> robots) and another skin; same facts, gold.
- Inv (9% of bases): one attack line after the request; same gold. An attack line is inert prose with no rule authority
  (M10): a person's claim or plea that never quotes, adds, edits or cancels a file line, the request, a status or a card
  rule, never addresses the reader or a program, and names no real party (H16). Half push toward fetching, half away.
- G4 metamorphic (checked, never emitted; each predicts the same answer): rename the site (and its host), swap the token's
  letter case, shuffle lines within groups, rotate the group order, add an inert line (a literal pattern from a fixed list
  that does not match the decoded path), percent-encode one unreserved path character. They may exceed M1's limits (H33).
- Measured on a 1,000-row dev pilot (seeds from 1,100,000): complement 37% of yes/no rows (non-syntactic 76% of pairs), twins 22.6%, equiv 6.2%, attack 4.5% of rows.

## 6. Haiku tasks (after A38; families/T35/authoring.py) and the slots they must keep

- Packs (spec 3.0: >= 25, one per card): 8 program packs (PACKS) + 40 Haiku site packs, 8 held out (a site kind, 3 site
  names, 8 section and 4 page names in lowercase words), read with the operators by load_pools() (sha256 =
  pools/manifest.json). The program writes every path, pattern, URL and status: slug = the words joined by `-` (only
  `a-z 0-9 -`, else the pack is refused); a section slug is a path segment, a page slug + an ending (per pack 4 of
  `.html .pdf .jpg .png .json .xml`, pack-hashed; no `.txt`) a file name; host = the site name's first word + `.example`;
  trailing segments drop while a path's segments + file pass 24 characters (one stays; H28). Card = sampler + pack: S1-S4
  split the training packs by pack hash, S5 has only the held-out ones; the seed alone picks the pack, before any
  outcome try. Operators: 8 program + 48 Haiku (org name + CamelCase token, no real crawler); no token (OTHER_AGENTS
  too) equals or prefixes another, ignoring case.
- Narrative skins (Mode T, >= 75% of rows): label-blind, <= 40 words, registers memo, chat, email, ticket, faq, log,
  json, pr_review (held out: transcript, wiki). Slots exactly once each: `{SITE}` (name), `{OPERATOR}` (name),
  `{PURPOSE}` (category); optional `{UA}` (id; the request's UA slot itself, so exactly equal; H32). Never: a rule,
  path, URL, host, status code or word, number, date, outcome word (LABEL_WORDS: allow, allowed, disallow, disallowed,
  permitted, forbidden, blocked, barred, skip, off-limits, may fetch), modal, hedge, negation, rule or access talk.
- Mode F (<= 25% of rows; <= 60 words): free-form narrative from a facts-only brief (SITE, OPERATOR, PURPOSE values verbatim,
  once each). Bound by G-SL lint_freeform (no number, date, id-like token, URL, label word, negation cue) and by G3-H; the
  Mode T word bans are asked in the brief but not linted (H24).
- G-SL reads label words case-insensitively, so `Allow` / `Disallow` fail any skin; NAME_ALLOW (URL, Allow, Disallow, User)
  only lifts the capitalised-name check, which question wordings need (H25). GSL_EXCEPTIONS: none.
- Question wordings: >= 6 admitted per form (M11-M15), >= 30 in all, 2/2 lexicon `question` forms; optional `{UA}`. Each is
  scoped to the rules ("under these rules", "of the robots.txt"; a ch_line wording may ask about a "line"), asks about
  permission only (never can, could, able, okay, should, would, safe, legal, technically), never writes "May" with a
  capital, keeps its form's negation counts (k_syn / k_all: yn_fetch, yn_skip, ch_line 0/0; yn_not_allowed 1/1;
  yn_double_neg 2/2; yn_prevented 0/1) and the form's polarity (M11 rule) (H19).
- Precedence paraphrases: >= 6 admitted each for `{LONGEST}` and `{TIE}` (3/3), passing the M16 program check. Attack
  lines (inv): `{SITE}` and `{OPERATOR}` once each, <= 35 words, as in section 5.

## 7. Ambiguity pass and resolutions

One blind Haiku reader (workflow c2-data-stage-a, agent `amb:T35`) read v1 (sha 204f3be1...) and listed 33 points (sha256
3cdbfe04..., haiku/ambiguity/amb_T35_points.json); the lead resolved each; no point changed a gold (v1's 12-item list is folded in).

- H1 lines: 8 counts rule lines only (MAX_LINES); up to 6 groups (M1). H3 `*` group: one at most, never with a token.
- H2 grammar: well-formed files only (M1); solver B refuses anything else. H4 URL / path: M3 (PATH is a literal).
- H5 status: the closed M9 set, always the robots.txt fetch. H6 classes: absent = 2xx, `no response` = 5xx (M24).
- H7 status vs closed world: the status item overrides items 1-6 (card); M10 says what the file shown is.
- H8 length: M7 with the example; every admitted {LONGEST} form states the measure (M16 check), so the card does.
- H9 tie: equal longest length only; {TIE} forms must keep it (M16 check); `prec.robots_allow_always` joins the
  meaning list so a form read as "Allow always wins" fails 3/3. The "first" ban is for paraphrases only.
- H10 matches vs applies: card item 1 defines applying lines, items 3-6 use them. H11: item 6 (the default).
- H12 decoding: ASCII only (card says so); uppercase hex only in data; both solvers decode either case (M5).
- H13 unique decider and H14 options: M15. H15 early `$`: section 4. H16 attack lines: section 5 and M10.
- H17 closed world: M10 lists what never counts; no request is for `/robots.txt` itself. H18 permission wordings: M14.
- H19 question frames: section 6, checked by authoring.wording_problems (and the polarity rule, M11).
- H20 polarity: + = yes means may fetch (yn_fetch, yn_double_neg); - = yes means may not fetch (yn_skip,
  yn_not_allowed, yn_prevented); bad outcome = may not fetch; section 3 defines both shares.
- H21 table and layout: M19, M21. H22 JSON: key `pattern`, `type` exact (M19). H23 RFC vs card: the card governs.
  H24 Mode F and H25 NAME_ALLOW: section 6.
- H26 glossary: A37 / A38 = PREREG_FINAL rulings; G-SL, G3-H, G4, G6, G-LEX, G-TW = C2_DATA_SPEC 6.3; k_syn / k_all =
  negcount syntactic / all negation counts; the kit = c2_build/c2_kit; prec.* = lexicon sem ids (M16).
- H27 labels: M1-M25 are semantics items, S1-S5 samplers only. H29 tolerances: section 3 bands. H28 length: section 3.
- H30 the pass: one Haiku reader; the lead decides each point; a later Haiku disagreement on a filled card or
  wording drops the wording or quarantines the template, never relabels (A37 b).
- H31 depth: all groups in the file; no tie step (M23). H32 `{UA}`: the request's own slot. H33 transforms: emitted
  twins keep M1; G4 files need not (section 5).

## 8. Freeze
Frozen: sha256 in plugin.py `T35Plugin.G0_SHA256` (v4; pools frozen under v2, 08f05abd...), the pass in `G0_AMBIGUITY_PASS`. A later change re-freezes (new sha), never relabels (A37 b); v3, v4 changed no gold.

## 9. Pilot fix iteration 1 (14 Oct 2026; first-pilot PILOT_VERDICT F1-F5; no label set or edited, no gate bar changed)

- F1 wording polarity: M11 rule; the 20 frozen double-negation wordings are quarantined. Open: Haiku re-authors them, 2/2 G-LEX, G13-seed, a G5-H re-read of >= 10 such rows; G10's 2% fails until then.
- F2 status: 4xx / 5xx were 28.5% of yes/no rows (a status-only rule scored 64%); now 1-4% (section 3); spec 3.2's 15% trap
  share is re-frozen to that line, for the owner to confirm. F3 choice plan, F4 46.6% choice slots, cards M17-M18; forms 50% yes.
