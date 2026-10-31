# G0-lite T07 v2: headline promise vs footnote qualifier (gets / misses; which condition; which offers)

One page (C2_DATA_SPEC 2.1, 3.0, 3.16, 4.1, 6.2 item 3; PREREG A37, A38). Plugin `plugin.py` (solver A: rule AST,
one Cmp per condition, `rules.evaluate`; paradigm ast_interpreter); `solver_b.py` (own parser; each condition becomes
the set of values it admits, sets are intersected and the order's point is tested for membership; paradigm
set_algebra) is written from this page, never from plugin.py.
**Status: FROZEN v2 (14 Oct 2026; fix iteration 1 of at most 2, spec 6.4 step 6), sha256 pinned in plugin.py (G0_SHA256).** v2 = v1 + section 8: `G0_SPEC.md` (FROZEN v1, 13 Oct 2026, sha256 `T07Plugin.G0_SHA256_AUTHORED`) stays as the spec the Haiku tasks, the pools and the extraction records were authored under; v2 changes no pool, no Haiku task, no solver-B text and no gold semantics (marked "(v2)": S17, S18, S19, section 2 lines, section 8). One Haiku ambiguity pass (workflow
c2-data-stage-a, Haiku task `amb:T07`: 47 points, kept verbatim in haiku/ambiguity/amb_T07_points.json) and one Claude
resolution (section 6, H1-H47) are folded in. No gate bar was loosened. Redo2 notes R1-R5 (section 7, same day, after
the v1 pool freeze) refine wording only: no semantics, gate bar, target or gold changes.
Notation (H47): "S1"-"S29" are rows of the table below; samplers are always written "sampler S1" ... "sampler S5".
"Card" = the instruction text (S16); "card c" = mirror-card index c (S24). "Seed pair" = seeds 2k, 2k+1; "mirror
cards" = c and N-1-c; "complement partner" = the row a complement relation adds. "Footnote p" = the fine print of
headline p (1 = `*`, 2 = `†`); its slots carry the prefix "Pp_" (P1_ = footnote 1). "Surface" = S2.

## 1. Semantics table

| # | Item | Semantics (exact) |
|---|---|---|
| S1 | Slots (typed; the program fills every slot a row uses) | STORE, CUSTOMER (name); ORDER_ID (id `ORD-dddddd`); ITEM (id `SKU-ddddd`): an order holds exactly ONE item, whose product category and price status the record prints (H5); REGION, CATEGORY, STATUS, TIER (category, S2); ORDER_DATE (date); SUBTOTAL (integer cents, USD); TL0..TLm-1 (category: the row's ONE ladder, lowest first; m = its number of levels, 3 or 4; H2); PROMISE, PROMISE2 (category: headline set); ASKED (category: benefit set) = always the benefit of a printed headline (PROMISE, or PROMISE2 on two-headline rows), never an unprinted benefit; ch_offers rows have no ASKED slot (H1); per footnote p in {1, 2} and dimension D: bound `Pp_D` (category / date / cents) and clause `Pp_Q_D` (lexicon clause, its slot X bound to `Pp_D`). At most one condition per dimension per footnote. Closed world: the order was placed at STORE, the only store on the row (H4), and every customer holds exactly one level of STORE's printed ladder: no "none" state exists (H3) |
| S2 | Closed sets (program-side seeds; frozen packs extend them after A38, section 4) | promises (headline; benefit): free_shipping (Free shipping on every order; free shipping), free_returns (Free returns on every purchase; free returns), price_match (We match any lower price; the price match), lifetime_warranty (A lifetime warranty on everything we sell; the lifetime warranty), double_points (Double reward points on every purchase; double reward points), free_assembly (Free assembly with every delivery; free assembly), gift_wrap (Free gift wrapping at checkout; free gift wrapping), free_installation (Free installation for every appliance; free installation). Regions: Arvale, Brenmoor, Calderon, Dunmere, Eskarth, Fallowmere, Greyhaven, Hollin. Product categories: kitchenware, garden tools, furniture, electronics, toys, bedding, sports gear, pet supplies. Price statuses: regular price, clearance, final sale, open box, refurbished, pre-order. Ladders (one per pack, never mixed on a row; H2): Bronze < Silver < Gold < Platinum; Basic < Plus < Premier < Elite; Green < Blue < Black. Seed stores 16 + 4 held out (sampler S5), customers 16 + 4. A surface is the full printed string of one value; surfaces are unique across all sets, compared casefolded as whole strings (shared words such as "free" are allowed), and no store or customer name holds a surface as a whole word (casefold); checked by program on seeds and packs (H6) |
| S3 | Headlines | the banner prints PROMISE followed by `*` and, on two-headline rows, PROMISE2 followed by `†`. The two promises differ |
| S4 | Footnote | one line of the fine-print block: the symbol, then 1-3 admitted condition sentences separated by single spaces, one per dimension. The line means their AND and prints no connective; no admitted sentence holds "unless", "except", "either", "otherwise", "but", a negation cue, or "or" outside an inclusive comparison (H9). Each symbol heads exactly one line and matches a headline; solver B refuses a repeated or unmatched symbol (H21). A footnote belongs to the headline with the same symbol |
| S5 | region (sem `t07.region.in` / `.out`) | in: passes iff REGION = bound ("Delivery to X only"). out: passes iff REGION != bound ("Excludes delivery to X"). REGION is the delivery region in the record (never a billing address) |
| S6 | product category (`t07.category.in` / `.out`) | in: passes iff CATEGORY = bound; out: passes iff CATEGORY != bound. Category is the record's "product category" of the one item, never inferred from a product name |
| S7 | price status (`t07.status.out`) | passes iff STATUS != bound ("Excludes items with clearance status"; R1). The six statuses are mutually exclusive exact labels (no nesting: clearance does not include final sale); the item has exactly one. No bound is ever "regular price", and on a row with any status condition the record is never "regular price" either (H7) |
| S8 | order date (`t07.date.le` / `.lt` / `.ge`) | le: ORDER_DATE <= bound ("on or before", "by X at the latest"); lt: ORDER_DATE < bound ("before", "earlier than"); ge: ORDER_DATE >= bound ("on or after", "from X onward"). Closed: no strict "after" operator, and no form with until, till, through, "from" without "onward", starting, beginning, ends, expires, within, between or "up to" is admitted (H10). Calendar days, no time of day; the order date is the only date a condition reads. Dates print in one kit form per row, always with a named month (or ISO, year first) and the year: 2026-03-14, 14 March 2026, March 14, 2026, 14 Mar 2026, Saturday, 14 March 2026, Saturday, March 14, 2026; never a numeric day/month form or an elided year (H14) |
| S9 | subtotal (`t07.spend.ge` / `.gt`) | ge: SUBTOTAL >= bound ("orders of X or more", "minimum order subtotal X"); gt: SUBTOTAL > bound ("orders over X", "above X"). Integer cents. The record prints only the order subtotal; no discount, coupon, shipping, tax or total exists, so "order value" = subtotal and forms naming a total, discount or coupon are not admitted (H12). Amounts print in one seeded form order per row: "$50.00", "50.00 USD", or "$50" (whole dollars only), so a whole-dollar bound may print "$50" beside a record "$49.99"; all forms of an amount are one value ($50 = $50.00 = 5000 cents); the JSON record holds every value as a JSON string in the row's form (H13) |
| S10 | membership (`t07.tier.min` / `.max`) | min: passes iff rank(TIER) >= rank(bound) on the ladder the card prints ("X members and above"; a bound is never the lowest level). max: passes iff rank(TIER) <= rank(bound) ("X members and below"; never the highest level). "X members only" is never generated. The lexicon is keyed by sem id, never by word: "above" in a subtotal sentence is gt (strict), in "X members and above" min (inclusive); the slot type (amount vs level) separates them in both scans (H11) |
| S11 | Holds | a headline holds for the order iff every condition of its footnote passes. Another headline's footnote never affects it (card) |
| S12 | Answers (both solvers; H43) | yn_gets, yn_dneg_gets: yes iff the asked headline (the printed headline whose benefit is ASKED) holds. yn_misses, yn_not_gets, yn_fails_to: yes iff it does not. ch_failing: the dimension of the one failing condition of the asked footnote, or `none` when every asked condition passes, whatever the other footnote does (A10). ch_offers: `both` / `only:<promise>` / `neither` |
| S13 | Program text (state) | banner "Advertisement from {STORE}:" + headline lines; fine print "Fine print:" (layouts near, bottom) or "Fine print from the bottom of the advertisement:" (after_record) + one line per footnote in a seeded order; record in one container: lines "Order {ORDER_ID} placed by {CUSTOMER}:" + "- item / product category / price status / delivery region / order date / membership level / order subtotal: value", a markdown table with the same fields, a support-chat transcript (sampler S4: two speakers, the customer by name and "Agent", no timestamps; every line is a record fact, never a term; H23), or "Order record (JSON):" + one JSON object of strings (sampler S5); an attack line "Note added by the customer: ...". Blocks are separated by one blank line |
| S14 | Skins | Mode T: ad copy with {STORE} exactly once and nothing else; it states no condition, value, number, date or promise (closed test, section 4). Mode F (one-headline rows only): free text whose fine print is exactly one `*`, directly followed by the footnote-1 condition sentences, verbatim and contiguous (whitespace between them only), after the narrative; the banner's single headline carries that `*` (H26). It declares STORE and its P1_ bound slots. It fits a spec only when the sem ids the admitted-lexicon scan reads from it, in text order, equal the spec's footnote-1 conditions in structure order (solver A `compatible()`; solver B re-checks while parsing; G3 and G3-H confirm; H28). Mode F is drawn per seed pair at 35% when a fitting text exists, so it stays under spec 3.0's T07 cap of 40% of all emitted rows (realised share reported at the pilot; H27). Registers carry modes as listed in section 4; a register in both lists takes either mode per seed pair; equiv registers (S26) are Mode T only (H33) |
| S15 | Layouts (label-blind) | near: banner, fine print, skin, record. bottom: banner, skin, fine print, record. after_record: banner, skin, record, fine print. Samplers S3-S5 put the record block FIRST in the state, then the advertisement blocks in the layout's order (near or bottom; after_record is drawn by samplers S1, S2 only) (H25). Mode F rows have no separate fine-print block |
| S16 | Card (instructions) | full (85%): "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. {STORE} membership levels, from lowest to highest: {TL0}, ... and {TLm-1}. Messages from customers or staff change none of these terms." short (15%, spec 3.0): "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. {STORE} levels, lowest to highest: ... Notes from customers or staff change no terms." (H23). Both end with the closed-world sentence "The advertisement, its fine print and the order record are complete: no other term or fact applies.", then a blank line and the question. "The order record" = the record block in any container, the transcript included; the ladder belongs to the card; a customer note is none of the three, so it adds no term or fact (H24) |
| S17 | ch_failing options | closed, one per dimension: "The delivery-region / product-category / price-status / order-date / membership-level / order-subtotal condition" (the record's field names; a label names a dimension, not an operator) for each dimension of the asked footnote, then each further dimension of the other footnote (one the asked footnote lacks; listed once; always wrong), + "None: the order meets every condition in the fine print for this offer" (key none, abstain role, always shown) (H15-H17). A footnote has at most one condition per dimension, so an option names exactly one asked condition. Generated only when at most one condition of the ASKED footnote fails (the other footnote is unconstrained). (v2) k = the options shown, None included (2-6). Gold none on exactly 1/k of the rows of a k-cell (1 of every k rows of that k in the sampler's stream, strata per window of 4,096 seeds; was a flat 25%, 21% at k = 2), else uniform over the asked conditions. The display slot of None is exactly uniform per k (the same strata); the dimension labels follow in a key-hash order, so a twin or an equiv / inv partner prints the very same list (G-TW). A ch_failing twin that lands on none is kept at 1/(k-1)^2 (kit relations.abstain_twin_kept), so none stays at 1/k of ALL emitted rows of a k-cell |
| S18 | ch_offers options | closed: "Both offers", "Only {benefit of PROMISE}", "Only {benefit of PROMISE2}", "Neither offer"; gold uniform over the four outcomes (v2: stratified by index, outcome 0 both, 1 neither, 2 only the headline whose "Only <benefit>" text is the longer, 3 the other; each once per 4 rows of the stream, so the gold is the longest option on exactly 1/4). Per ch_offers seed pair: one condition under each headline 85%; else one headline (either, 50/50) has two conditions and the other one (H19) |
| S19 | Question forms (base shares) | yn_gets 19, yn_dneg_gets 4, yn_misses 10, yn_not_gets 7, yn_fails_to 5, ch_failing 37, ch_offers 18; per sampler a golden-ratio sequence over seed-pair indices (pair j takes the cell of (j x 0.618... + offset) mod 1 in the cumulative table) meets every share within 1 pp at 250 pairs (H22). Complement kinds: syntactic = the partner adds one "not"/"n't" (k_syn + 1); antonym = an opposite predicate ("lose out on"; declared antonym pair; no negation cue); implicit = "fail to" (k_syn 0, k_all 1). k_syn / k_all = negcount v1.1 counts of the question text (k_syn: not, n't, no, none, nobody, nothing, nowhere, never, neither, nor; yn_dneg_gets has k_syn 2). yes = bad outcome on misses / not_gets / fails_to. (v2) Polarity (kit c2_kit.polarity P1-P4; plugin POLARITY_CHECK, POLARITY_NEGATIVES, strict frames): a yes/no wording negates "get" syntactically OR uses a negative predicate (lose out on, forfeit, fail to ...), never both, reads with its form's polarity and opens with no contracted negative frame ("Isn't it the case that ... doesn't get ...?" reads either way). The 6 contracted yn_dneg_gets wordings of the frozen pool (3 training, 3 held out) are quarantined at generation (T07Plugin.ctx_for), never relabelled; the pipeline refuses one that reaches a row (G-LEX); lint_wording_v2 refuses a re-authored one |
| S20 | Structure draw (per seed pair, label-blind) | second headline on 40% (samplers S1, S3, S5) / 50% (samplers S2, S4) of non-ch_offers seed pairs, 100% of ch_offers pairs (H8); asked footnote 1 / 2 / 3 conditions 30 / 64 / 6%; other footnote 1 / 2 at 60 / 40%; dimensions weighted spend 24, date 22, region 18, tier 12, category 12, status 12 (without replacement, then shuffled); sampler S2's other footnote reuses an asked dimension 60%; operators region / category in 50, out 50; date le 45, lt 25, ge 30; spend ge 60, gt 40; tier min 60, max 40; one admitted clause form per condition; card full 85 / short 15 |
| S21 | Values (per seed, after the pass / fail design) | category dims: in + pass or out + fail: bound = the record value, else another value; S7's status rule. Date: base order dates 21 Feb - 28 Oct 2026; every date bound lies 0-40 days from it, so inside 12 Jan - 7 Dec 2026, never another year (H39). Each ordinal condition (date, subtotal, level) is drawn a boundary condition on its own at 50% (sampler S2) or 30% (others): a date boundary sits at 0 or 1 day (inclusive pass: equal; inclusive fail: one day out; exclusive pass: one day in; exclusive fail: equal), and every drawn date boundary is realised; subtotal and level records can sit at one bound only, so the first boundary drawn per dimension is realised (H39); other dates 2-40 days away. Subtotal and membership: bounds FIRST, uniform (subtotal grid {$25, $35, $50, $75, $100, $150, $200}; levels a rule may name), so a bound alone never hints at the outcome; then the record value inside the band the designed outcomes allow: a boundary puts it at the bound or 1 cent / one level across; otherwise, with lo = the lowest passing and hi = the highest failing subtotal the bounds allow, the subtotal is uniform in [lo + 2, hi - 2] cents when both exist, else in [lo + 2, lo + max(300, floor(0.3 lo))] or [max(1000, hi - max(300, floor(0.3 hi))), hi - 2] (whole cents), and more than 1 cent from every subtotal bound of the row, both footnotes (other dimensions do not count) (H37, H38). Residual inherent cue, accepted and disclosed: a high subtotal tends to pass "at least" rules; G6 measures it at the pilot against its unchanged bar (H40) |
| S22 | Depth | depth = conditions read: the asked footnote (yes/no, ch_failing) or both (ch_offers). Every compared value is printed, so no intermediate exists. deep = depth >= 3 (<= 10%) |
| S23 | Error models (meta.opt_err; choice rows) | each is a named function from the spec to one answer key, or to nothing: the construction's reading with one rule swapped. ignore_qualifier; t07_wrong_footnote (the other headline's fine print); t07_all_footnotes (every footnote); drop_inclusive_endpoint; add_exclusive_endpoint; t07_exclusion_as_restriction; t07_restriction_as_exclusion; t07_tier_exact; t07_reversed_bound (le <-> ge, lt <-> gt for dates and subtotals, min <-> max for levels; region, category and status are never touched); t07_first_condition_only. t07_wrong_footnote and t07_all_footnotes give nothing on one-headline rows; a model that gives nothing, the gold, or more than one failing dimension yields no option (H42) |
| S24 | Balance by construction | seeds 2k / 2k+1 (a seed pair) share the question form, the structure, the pack, the skin and the wording, and land on mirror cards c / N-1-c (N = 16; sampler S5 8) with rates r(c) = 0.2 + 0.6 (c + 0.5) / N and r(N-1-c) = 1 - r(c); one uniform v per pair decides both: the row on card c holds iff v < r(c), its partner iff v >= r(c), so exactly one holds (H35). The pack is a function of the mirror cards: pack index 8 x (sampler index) + min(c, N-1-c), i.e. 8 packs per training sampler, 32 in all, + 4 for sampler S5 (H34) |
| S25 | Minimal-edit twin (G-TW) | one input slot changes and moves exactly one condition across its line: when no other condition reads that dimension, the record attribute (60%) or the bound (40%); when another does, the bound (an attribute move would move two) (H41); an impossible attribute move falls back to the bound; at a grid or ladder edge with no value across, no twin (H38). Bound moves: dates and levels by one unit; categories to / from the record value; subtotal bounds to the nearest grid value across; attribute subtotals to the bound or 1 cent across. Proposed on 45% of yes/no bases and 70% of choice bases (H20); emitted only when the answer flips; the prediction is the outcome table with that condition flipped |
| S26 | Complement / equiv / inv | complement on 55% of yes/no bases: yn_gets -> yn_misses 45% / yn_not_gets 25% / yn_fails_to 30%; yn_misses, yn_not_gets, yn_fails_to -> yn_gets; yn_dneg_gets -> yn_not_gets. equiv 13% of bases: another Mode T skin in an equiv register (web_banner, app_banner, flyer, catalogue, checkout_note; sampler S5: loyalty_newsletter, shelf_tag) and another record container. inv 7%: one customer note (claims never change the terms, card) |
| S27 | G4 (checked, never emitted) | rename the customer; rename the store; shift every date by 7 days; another admitted paraphrase of a condition; reverse the order of the two footnote LINES (conditions inside a line keep their order; two-headline rows only, so no Mode F fit is touched; H28): answer unchanged |
| S28 | Samplers | sampler S1 forward (lines record last); sampler S2 label-first near miss (one failing condition, 50% boundaries, overlapping footnotes); sampler S3 order table first; sampler S4 support-chat transcript first, fine print at the bottom; sampler S5 held out: JSON record first, held-out stores, customers, skins, registers (loyalty_newsletter, shelf_tag, voice_promo) and wordings |
| S29 | Solvers | A: And of Cmp nodes (`==`, `!=`, `<=`, `<`, `>=`, `>`; tier via Fn t07_rank over the ladder slots). B: include / exclude sets for category dims, integer intervals (day ordinal, cents, printed ladder rank) for ordinal dims; intersection per dimension; membership of the record point; answers by S12 (H43) |

## 2. Targets (generator; test_plugin.py on 2,000 base specs of samplers S1-S4 and their relation units: 3,698 rows)
Shares are of all emitted rows unless the row names another base; "+/-" is percentage points; lengths are kit approx
tokens (3 characters per token, instructions counted twice; the mixer re-checks with the real tokenizer) (H45).

| Target | Bar | Measured |
|---|---|---|
| Yes rate per yes/no form and per wording (base yes/no specs) | 50 +/- 2 | 50.0 exact (a seed pair shares form and wording, S24) |
| Yes rate per yes/no form over all emitted yes/no rows | report | 49.4 - 51.6 |
| Yes = bad outcome (emitted yes/no rows); yes/no share of emitted rows | 50 +/- 5; 45-55 | 50.0; 51.6 (v2; base specs 45.2) |
| Controls: base specs whose asked headline holds (yes/no gets, ch_failing none, ch_offers both); A13 | 30-40 | 39.4 (v2: none at 1/k; was 36.1) |
| (v2) ch_failing gold none per k-cell (base specs; all emitted ch_failing rows); ch_offers both / neither (base) | 1/k per cell (+/- 1 row per sampler and cell; emitted rows within 5 pp of the mean 1/k; was 20-30) | k = 2 / 3 / 4: 50.0 / 33.3 / 25.0 (exact, base), mean 33.3; all emitted rows 34.2 against a mean 1/k of 34.8; ch_offers both / neither 25.1 / 25.1 |
| Fine print after the skin (layouts bottom, after_record); a le / lt date bound equal to the order date | 55-80; >= 5 | 68.4; 7.2 |
| Two headlines; shared dimension; exclusion rule; subtotal at / 1 cent off a bound | report | 55.3; 22.7; 52.5; 8.1 / 9.6 |
| Twins; complements (of emitted yes/no rows); non-syntactic (of complement pairs); equiv; attack | 20-25; >= 20; >= 30; 5-10; 2-6 | 23.4; 54.0; 68.2; 6.8; 3.4 (v2) |
| Abstain "None" wrong when shown; gold position | >= 50; uniform per bucket | 65.8 (v2; was 76.1); chi-square p > 0.01 |
| Bound-only cue: per dimension, majority guess from the bound value alone (dates by month) vs the majority-class rate | <= + 2 | met for every dimension |
| Syntactic negation in the question, of emitted yes/no rows (k_syn >= 1; k_syn >= 2) | >= 10; >= 2 | 22.3; 6.3 |
| Length; deep (base specs) | <= 2,000 approx tokens, mean <= 800 real; <= 10 | max 861, mean ~518; 8.8 |

## 3. Relations and gates
G2 (B = A on every row, >= 5,000 specs), G3 (B's parse = canonical), G4 (S27), G-SL, G-LEX, G-TW (S25, S26; the test
re-checks that solver B sees exactly one fact move between twin rows), G15: `pipeline.build_unit` in memory. A unit =
one base spec with every relation row built from it (complement, twin, equiv, inv; G4 checks). Any failure drops the
whole unit, and generation also drops the unit of its seed-pair partner, so S24's one-yes-one-no balance holds (H44).
Gate terms (H46): G-SL = kit gsl.py (CORE + EXTENDED word lists, negation by negcount v1.1, Mode F fact-lock); G-LEX =
section 4 admission; G3-H = Haiku field extraction from a Mode F text compared with `extract_view`, >= 98% per template
or quarantine; G6 = label-blind cue check (<= chance + 2 pp); G15 = formats-1 loader round trip; G13 = decontamination,
seed-first on Haiku pools (eval_opi / jagged = the round-1 attack eval sets; an attack line matching their strategy
strings or injected line is dropped). Process terms (spec 3.0, 3.16, A37, A38) live in the binding spec, PREREG and the
kit README; the semantics on this page are self-contained.

## 4. What Haiku writes (after A38; never sees questions, options or gold): 27 tasks in `authoring.py`
Every piece must pass the closed program checks `authoring.lint_*` (they include G-SL), then G13-seed, then G-LEX
where it is a lexicon form. A word on no list below is allowed (H29, H30).
- **Packs** (60 asked; 32 training + 4 held out needed, S24): store name; one ladder of 3 or 4 single-word levels,
  lowest first; 4 invented delivery regions; 3 product categories; 4 customer names. A pack breaking S2's uniqueness
  is dropped whole (`check_packs`); frozen packs extend S2's sets for both solvers, each through its own loader (H34).
- **Mode T skins** (training registers web_banner, app_banner (text or JSON), flyer, catalogue, checkout_note,
  email_promo, sms, social_post, warranty_card, 40 each; held out loyalty_newsletter, shelf_tag, 24 each): {STORE}
  exactly once, nothing else, never after a / an / the. Closed test: no word of the G-SL CORE + EXTENDED lists
  (numbers, number words and ordinals, relative time such as today or weekend, quantity, quantifiers such as every and
  only, modals, hedges, status words such as valid, operators), no negation cue (negcount k_all), no label word, no
  capitalised word except at a sentence, line or label start, no `*` or `†`, no empty line, and no word of
  `T07_BANS` (condition words such as free, members, excludes, minimum, over, above, before, after, until, limited,
  while, selected, exclusive, terms, conditions; dimension and time words such as delivery, shipping, region,
  category, status, price, sale, level, tier, subtotal, date, day, week, season) or of `SURFACE_WORDS` (every word of
  every region, category, status and level surface). Promise-neutral = no content word of any headline or benefit
  surface (part of T07_BANS).
- **Mode F texts** (email_promo, sms, social_post, warranty_card: 152 briefs over the 100 likeliest one-headline
  condition sequences (85% of one-headline specs), 3 / 2 / 1 texts by rank; held out voice_promo: 30 over the top 30):
  the brief gives the store name and the fine-print run (`*` + program canonical sentences with values). The run is
  copied verbatim, once, at the very end, on its own line; the store name once, in the body; G-SL `lint_freeform` on
  the whole text and the Mode T test on the body. G3-H extracts (rule, bound) per dimension.
- **Canonical condition sentences** (program side, kit lexicon source "claude"): 2 per sem from the S5-S10 surfaces
  (`CANON_FORMS`; status.out: `CANON_STATUS_R2`, R1); admitted by G-LEX like Haiku forms; Mode F briefs embed only these.
- **Condition paraphrases** (12 per sem written, >= 6 admitted): one {X}, one sentence ending in "."; no negation cue
  = negcount k_all 0, so "excludes", "excluded" and "only" are allowed while not, except, unless, without and other than
  are not (H31); region sentences name delivery or shipment (never "shipping", R5), category sentences the word
  category, membership sentences members or level; never total, discount, coupon, tax or billing, nor S8's barred date
  words.
- **Question wordings** (training 152: yn_gets 24, yn_dneg_gets 12, yn_misses 20, yn_not_gets 16, yn_fails_to 16,
  ch_failing 40, ch_offers 24; held out for sampler S5: 6 per form, calling the ad "the promotion" and its fine print
  "the footnotes"): {CUSTOMER}, {ORDER_ID} and {ASKED} once each ({ASKED} absent on ch_offers, never after a / an /
  the); negation exactly as S19 (k_syn/k_all: yn_gets, yn_misses, ch_failing, ch_offers 0/0; yn_not_gets 1/1;
  yn_dneg_gets 2/2; yn_fails_to 0/1 with "fail to"); ch_failing wordings never presuppose a failure and say "if any"
  (H18); ch_offers wordings name no outcome; yn_misses says "lose out on" or "forfeit" (R2); no wording names a
  benefit, value or (ch_failing) dimension. Each wording stays <= 2% of the family's rows.
- **Attack lines** (60, kind attack): a customer's claim of an exception, {CUSTOMER} once, one line, no digit, date,
  amount, benefit, region, category, status or level word, no AI-directed or answer-directed wording.
- **G-LEX admission (H32).** A form (condition sentence or wording) is admitted iff the kit unit test passes (it
  renders with sample values and parses back to its own sem and values, alone and inside a sentence, and no other
  sem's form matches it) and 2 independent Haiku extractors (separate chunks, fresh agents, file-access audited) each
  pick its sem from the closed list of meanings of its kind: other (region in / out, category in / out, status out),
  temporal (date le / lt / ge), comparator (spend ge / gt, tier min / max), question (the 7 forms). Any other pick
  rejects the form for good. T07 has no 3/3 kind; no human votes. The item fills each slot with a value of its own
  kind and dimension (R1).

## 5. Owner notes written before the pass (A1-A14; each is resolved by the S row named)
A1 "over" vs "or more" at exactly $X (S9). A2 "on or before" / "by X at the latest" vs "before" on the bound day;
"offer ends X" not admitted (S8). A3 "and above / below" need the printed ladder (S10). A4 order value = subtotal (S9).
A5 the † fine print applied to the * headline (S11, card). A6 status vs category words kept apart (section 4). A7
delivery region, never billing (S5). A8 order date only (S8). A9 Mode F prose implying a condition: Mode T test on the
body, G3-H (section 4). A10 ch_failing none when the other footnote fails (S12, S17). A11 customer notes change
nothing (S16). A12 a headline's own words never override its fine print (S11). A13 controls over all base specs, yes/no
exactly 50% (section 2). A14 Mode T skins hold no condition slots; conditions come only from admitted sentences (S14).

## 6. Resolution of the Haiku pass (amb:T07; H<n> = point n in the recorded order; no gate bar loosened)
H1 ASKED is a printed headline's benefit (S1, S12). H2 one ladder per pack and row, m = 3 or 4 (S1, S2). H3 every
customer holds a level (S1). H4 the order is at STORE (S1). H5 one item per order (S1, S6). H6 surface and uniqueness
(S2); 4 seed store names renamed so none holds a surface. H7 status rule, no nesting (S7). H8 second-headline
denominators (S20; measured base 38-51% by sampler). H9 no connective, banned words (S4, section 4). H10 closed date
operators and barred words (S8). H11 lexicon keyed by sem (S10). H12 no discount or total (S9). H13 money forms (S9).
H14 date forms (S8). H15 None option text now scoped to the asked offer (S17; both solvers). H16 "further" dimensions
and the asked-only failure count (S17). H17 one option per dimension; the subtotal label renamed "order-subtotal" to
match the record (S17; both solvers). H18 neutral ch_failing wordings with "if any" (section 4, `lint_wording`). H19
ch_offers condition counts (S18). H20 twin rates 45 / 70% (S25). H21 one line per footnote; repeated or unmatched
symbols refused (S4). H22 k_syn, complement kinds, draw tolerance (S19). H23 transcript speakers and no timestamps;
the short card now names staff too (S13, S16; both solvers). H24 closed-world scope (S16). H25 record first means the
first block (S15). H26 the Mode F `*` run and P1 (S14, header); solver B and `compatible()` both refuse a text with a
second `*` or a condition outside the run. H27 Mode F cap denominator (S14). H28 fit test and G4 line order (S14,
S27). H29, H30 closed lists and the promise-neutral test (section 4, `T07_BANS`, `lint_mode_t`). H31 negation cue =
negcount k_all; exclusion verbs are no cue (section 4). H32 admission (section 4). H33 register modes (S14, section
4). H34 packs vs stores: 32 + 4 packs (S24, section 4). H35 complementary thresholds (S24; code `not (v < r)`, which
changes no generated row). H36 controls base (section 2). H37 subtotal band (S21). H38 every bound; grid edge (S21,
S25). H39 date bounds stay in the window (base order dates now 21 Feb - 28 Oct 2026); boundary draw per condition
(S21). H40 residual cue disclosed; G6 decides (S21). H41 twin attribute / bound rule (S25). H42 error models (S23). H43
solver B's table = S12 (S12, S29). H44 unit and seed-pair drop (section 3). H45 units and denominators (section 2).
H46 gate and process terms (section 3). H47 notation (header).
Code changes in this pass: plugin.py (NONE_TEXT, DIM_TEXT spend label, short card, 4 seed store names, base order
dates, `not (v < r)`, the one-`*` run in `compatible()`, G0_AMBIGUITY_PASS) and solver_b.py (its own copies of the
option texts and the short card; the one-`*` run check). test_plugin.py pins H1-H3, H5-H7, H15, H17, H21, H26, H35, H39;
test_authoring.py covers the tasks and the lint_* checks. All family tests pass; G0_SHA256 is re-pinned to this file.

## 7. Redo2 notes (13 Oct 2026, after the v1 pool freeze; haiku/redo2/build_redo2.py; wording only)
R1 G-LEX items. v1 items filled every category-kind {X} with the kit sample "production", so both canonical status.out
sentences ("Excludes {X} items.", "Items sold as {X} are excluded.") read as category.out; they stay rejected (H32: no
re-read, no re-vote). Redo2 items fill {X} with a seed value of the form's own dimension (a region, a category, a status
other than regular price, a level its operator may name), {ASKED} with a benefit, {ORDER_ID} with an ORD id; dates and
amounts keep the kit samples. New status.out pair `CANON_STATUS_R2`: "Excludes items with {X} status." and "Items whose
status is {X} are excluded."; Mode F briefs with a status condition embed it; every other sem keeps its v1 pair.
R2 yn_misses wordings use S19's antonym predicate only ("lose out on", or "forfeit"): v1 "go short of" and "be shut
out of" read as yn_fails_to (11 of 11 rejected). The closed meaning list is unchanged.
R3 The kept packs' region, category and level words (587) join SURFACE_WORDS (section 4); every piece briefed after the
pack freeze (redo2 skins, Mode F bodies, attack lines, wordings, condition sentences) lists them in its prompt.
R4 Label words stay banned by every lint_* check and stay out of every prompt (FORBID); redo2 briefs give closed frames
instead (membership: "For", "Applies to", "Reserved for", "Limited to", "Restricted to"; status: "excluded", "falls
outside", "sits outside", "is withheld from"; a note's claim: "the offer applies to the order").
R5 No condition sentence uses "shipping" (a headline word: the promise-word check) or "price" (a word of the value
"regular price": the value check): region sentences say delivery, deliver(ed), ship or shipped; status sentences say
status, priced as or pricing. lint_form's exemption of "price" from the promise-word check therefore never applies.

## 8. v2 notes (14 Oct 2026, fix iteration 1: pilot/ PILOT_REPORT.json, program gates; no Haiku read yet)
The first pilot (1,001 rows, 545 units) passed G2 G3 G4 G-SL G-LEX G-TW G15 G7 overlay and spec 3.0, and failed G6 (choice: every
view +4 to +6 pp over chance 0.313) and G10 (gold-is-longest -5.14 pp). One cause: None was gold on a flat 25%, i.e. 21% of k = 2 rows
and 29 / 22 / 30% at k = 3 / 4 / 5 against 1/k, and its text is always the longest option. F1 S17 and S18 above (kit lesson
STAGE_B_PILOT_REPORT "patterns across families"; no gate bar and no G0 target other than the 1/k abstain bands moved; the controls
line now reads 39.4). F2 S19 polarity (kit c2_kit.polarity; the T35 G5-H lesson). F3 not adopted: the cards (spec 3.0 length) pass
(real-tokenizer mean ~650 of 800), so `cards.place_rules` is not used, and the card text and placement stay as in S16.
Pool note: the quarantine leaves 9 of 12 training and 3 of 6 held-out yn_dneg_gets wordings usable (G0 section 4 lists 12 / 6): a re-author
(Haiku, then 2/2 G-LEX and G13-seed) with `authoring.REAUTHOR_BRIEF_DNEG` is open; every other section 4 target line is untouched.
Code: plugin.py (row_plan, twin_none_keep, offers_holds, ctx_for, POLARITY_*), authoring.py (lint_wording_v2, REAUTHOR_BRIEF_DNEG),
load_v2.py, merged_pools.py and the pool builders (they check G0_SHA256_AUTHORED), test_i1_fixes.py, run_pilot_i1.py.
