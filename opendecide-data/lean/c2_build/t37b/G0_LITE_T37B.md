# G0-lite T37b: real-text complements and paraphrases on replay yes/no rows

C2_DATA_SPEC 2.1 (T37b: a nominal 2,000 partner rows, build wave 1 of spec 5.3), 3.18, 4.2, 7.1 (T37b-dev); PREREG
A37 (b) T37b golds, (f) nothing T37b is written before Ruling A38. One page: semantics, bases, partner kinds, the two
polarity programs, Haiku's role, the decision rule, outputs, ambiguity points and their resolution. **v2, frozen**: v1
(sha256 3a16d271) plus the resolution (section 5) of the one blind Haiku pass `c2-data-stage-a/amb:t37b` (61 points
H1-H61, verbatim in haiku/ambiguity/amb_t37b_points.json). This file's sha256 is builder.G0_SHA256 and the pass id
builder.G0_HAIKU_TASK (a file cannot hold its own hash). builder.g0_problems() must be empty, or every writer refuses.
Code: sources.py, polarity.py, polarity_b.py, select.py, builder.py, author_pool.py.

## 1. Semantics table

| # | Item | Semantics (exact) |
|---|---|---|
| S1 | Base | One replay row of C1's golden_train (after replay_sample's round-1 drops and pool_drops_r1): qtype noul (yes/no, no options), gold 0 / 1, role `aff`, no meta.teacher, no meta.gold_probs, no meta.attack_target; source in the registry, KEEP by the replay register (verified set passed in), not an OHS-3 hit source, not program-labelled, not Claude-gold (H4, H5) |
| S2 | Binary predicate | The base instructions re.fullmatch one entry of the closed registry (sources.ENTRIES): one golden_src builder question whose label space, as built, has exactly two values and whose card is exactly the two lines `- yes: <Y>` / `- no: <N>`, N the source's other label. Questions with 3+ values, ordinal-cut, vote-share, answer-verification (label-check) and DI-adjacent sources are out (sources.EXCLUDED) (H33-H36) |
| S3 | Unit | The base is in no golden_relations edge and no other pool row shares its call_id. Partner = same state (raw), same group_id, same call_id; edge {a: base id, b: partner id, type: complement or equiv}; unit = 2 rows (H7-H10) |
| S4 | Old slice | Never a base: a round-1 old-slice id, group_id or normalised state (passed in; required) (H4, H6) |
| S5 | Gold | gold 1 = the answer is yes. complement: partner gold = 1 - base gold; equiv: partner gold = base gold. Human gold only; no model sets a label (H12) |
| S6 | Partner kinds | The base splits into (optional fronted prefix ending ", ", first auxiliary, subject, rest) by the entry's subject rule. syntactic: `<frame>[, <prefix>,] <subject> <aux> not\|n't <rest>?` (can: can not / cannot / can't); implicit (do / does / did questions only): `<prefix><Aux> <subject> fail to <rest>?`, or `<prefix><Aux> <subject> lack <rest after the verb>?` when the main verb is have / contain / include; antonym: one closed (phrase, antonym) pair, the phrase present once; option_framing: comve's digit swap after "Statement "; equiv: a pool paraphrase template filled with the base's slot values (H13-H21, H40) |
| S7 | Frames | Training: Is it true that / Is it correct that / Is it accurate to say that / Would it be correct to say that / Is it right to say that / Is it the case that (never "right" on gd_sc101 acceptable / wrong). T37b-dev only (FRAMES_DEV): Is it so that / Would it be true to say that / Is it accurate that. No frame holds a negcount entry (H23-H25) |
| S8 | Scope | syntactic: the base holds no negation; no quantifier, modal, negation or subordinator in the prefix or subject; the rest holds no modal and, as quantifiers, only any / anything / anyone / anybody / both / either / always (after "not"); first auxiliary do / does / did / is / are / was / were / has / have / had / can. implicit: no negation, quantifier, modal, collective or comparative word; "fail to" right before the main verb (H26-H29) |
| S9 | Program A | polarity.py: builds every exact partner string S6 allows and reads both questions with negcount (XF02): syntactic = one of those strings, base (k_all, k_syn) = (0, 0), partner (1, 1); implicit = one of those strings, partner (1, 0) with a fail to / lack entry; antonym / option framing = k_all, k_syn and negcount entries equal and the closed rewrite; equiv = equal negcount entries, quantifier and modal multisets and anchors (H30, H31) |
| S10 | Program B | polarity_b.py, written from v1 of this page without A's code: own tokenizer (n't, can't, cannot split), own word lists and subject reader (CAPS by token case), token sequences instead of counts; the same five constructions and the S8 scope (H32) |
| S11 | Card | complement (syntactic, implicit, antonym): the base card with the two definitions exchanged; hotpotqa: its own complement card (sources.COMPLEMENT_CARDS); option framing and equiv keep the base card. A swap entry whose definitions use an answer word is not a base (H37-H39) |
| S12 | Haiku | Writes only the equiv paraphrase pool: slot templates per registry entry (author_pool.py; kind author_wording; it sees the entry's question or template and closed rules, never a state, card, gold or option). Every other partner is program-written. Flags only: two polarity reads (kind polarity) per distinct question pair, the blind solver on the base and on the partner in separate batches (kind blind_read) (H40-H42) |
| S13 | Decision | keep iff program A = program B = the planned relation, both polarity reads = that relation, and the blind solver's two answers are consistent (opposite for complement, equal for equiv). Only a solver inconsistency goes to Claude review (keep \| drop; keep only when certain); every other failure drops. Haiku never relabels (H43, H44) |
| S14 | Block (train) | 1,400 complements (implicit / C >= 0.25 and (antonym + option framing) / C >= 0.30, exact) + 600 equiv; base source <= floor(10%) of the realised block; each wording key (entry x kind x frame / cue / pair x base question, and each pool paraphrase) <= floor(2%). The complement count is cut to the largest that keeps both floors; shortfalls lower the block, never refill it (H45-H48) |
| S15 | T37b-dev | 300 complement units (antonyms included) on binary-predicate yes/no rows of the 9 gate dev splits (caller passes them; S1-S3 apply, S4 does not), syntactic with FRAMES_DEV only; meta.dev_only true; never trained (H49, H50) |
| S16 | Row | C2 row format (rows.validate_row) with source c2_t37b, role complement / equiv, meta.twin_of = base id, meta.t37b = {base_id, base_source, entry, kind, frame, cue, template, author, polarity_a, polarity_b, base_gold}; licence = the base licence for text and definitions AND CC0 for the question wording; closed_world false (no sentence printed; exactness from S2); G15 loader_check on every partner (H51) |
| S17 | Decontamination | template_strings() (frames, cues, complement cards, antonyms, pool templates, prompts) and the admitted pool go through G13 method 8 seed-first; LOCAL_BANS ("Should the statement that", "be rejected", "Is it wrong to answer", "only non-", "Is the correct answer") drop a partner or pool paraphrase at once; candidates and the final mix pass G13 (H52, H53) |
| S18 | Mix | The base is a replay row: whenever a partner enters the mix its base enters with it (one unit). The 2,000 counts partner rows; bases count once, as replay (H54) |

## 2. Registry (sources.py; the code is the authority, kinds complete)

check_covid support (syntactic, implicit on "support", antonym: support -> contradict / refute, equiv) and refute
(syntactic, implicit on "contradict", antonym: contradict -> support / back up, equiv), subject "the evidence";
comve against (syntactic, antonym: "go against" -> "agree with", "go against common sense" -> "make sense",
option framing, equiv), subject `Statement [12]`; hotpotqa_yesno q (native questions, CAPS subject, syntactic only:
no pool, H40; own complement card); multiwoz21 booking (syntactic, implicit on "confirm", equiv) and match (equiv);
taskmaster1 status (syntactic, equiv; quoted-span subject); taskmaster3 purchase (syntactic, equiv); nhtsa crash /
fire (syntactic, implicit on "report", equiv) and injury (equiv); answer_equiv equiv / notequiv and usb_factuality sup
(equiv); onet_occupation yn (syntactic, equiv); cards claim (syntactic, implicit on "make", equiv; a claim holding
"not" / "won't" leaves equiv only); sc101 acceptable (syntactic, antonym -> wrong / bad, equiv), wrong (syntactic,
antonym -> acceptable / okay, equiv) and legal (equiv); semtabfacts_sci supported (syntactic, antonym -> refuted by /
contradicted by, equiv); hatemoji_build_v14 hateful (syntactic, equiv). Pool slots: comve {N}, taskmaster1 {SPAN}
{ORDER}, cards {CLAIM}; other pool entries are fixed questions.

## 3. Ambiguity listing (v1 items, kept; fixes from section 5 marked)

1. "X and Y are not both ..." vs "both X and Y are not ...": the second reads as "neither". Every quantifier sits
   after the "not"; both programs refuse the second.
2. "fail to" on a stative predicate may carry an attempt reading: implicit only on do-questions whose entry names the
   main verb and whose subject is inanimate (H59), with no comparison or collective word.
3. "lack the same X": refused (collective word).
4. Modal scope: "must not" is not "need not": no modal anywhere in a syntactic base; "can" only as the first
   auxiliary, where "cannot" = not possible is the exact complement (H26).
5. Negative matrix questions ("Doesn't the evidence ...?") are ambiguous: the "not" sits only in the embedded
   statement after a truth frame.
6. 3-class questions: "not supported" is not "refuted" when NEI exists: label space per question as built (H35);
   antonyms only on entries whose builder kept two labels (check_covid without NEI, semtabfacts manual set, sc101,
   comve).
7. A swapped card whose definitions use an answer word would contradict itself: such a base is refused (H37);
   hotpotqa has its own complement card.
8. Option framing on comve keeps the card: its definitions speak of "the asked-about statement", and exactly one
   statement goes against common sense (H58).
9. Where does the auxiliary go? Both programs read the subject by the entry's rule, so misplaced auxiliaries or cues
   are refused, not only judged.
10. Equiv may shift a quantifier ("at least one" -> "any"): "least" is on both quantifier lists, so the multisets
    differ (H29); the reads and the blind solver catch meaning shifts the lists miss.
11. The base gold may be wrong (human noise): T37b inherits it; the blind solver's disagreement with gold alone never
    drops a pair, only its inconsistency between base and partner does.

## 4. Outputs

Training: data/c2_parts/t37b_r1.jsonl (partner rows) and t37b_r1_relations.jsonl (edges), builder.write_block. Dev:
data/c2_t37b_dev.jsonl (300 dev bases + their partners) and data/c2_t37b_dev_relations.jsonl, builder.write_dev. The
block report (select.plan_report + finalize: counts, shares, by source, drops and trims by reason). Pool:
haiku/author/ (tasks, TASKS.json), haiku/author/lint/, haiku/extract/ (two polarity reads), pools/t37b_equiv_pool.json
+ pools/MANIFEST.json (sha256, counts, targets, shortfalls). Every writer: paths guard (A38, never-open) + G0 check.

## 5. Resolution of the Haiku pass (H<n> = points[n-1]; one line each)

- H1: outputs are section 4. A non-empty g0_problems() halts: write_block, write_dev and every author_pool writer raise first. The sha lives in builder.G0_SHA256 and in each TASKS.json.
- H2: 2,000 is a nominal cap: shortfalls lower it (S14), never an error, never refilled. Wave 1 = spec 5.3's first build wave (core families; cutoff Tue 20 Oct 23:59 UTC).
- H3: A38 = PREREG_FINAL "Ruling A38" (13 Oct 2026, the OHS-4 freeze), an amendment id. Before it no T37b pool, task, plan or row could be written (paths.require_a38); it is now in force.
- H4: the caller passes the pool (golden_train after spec 5.4's drops and pool_drops_r1), golden_relations, the round-1 old slice (ids, groups, normalised states), the verified set and, for dev, the 9 gate dev splits. Empty relations or old-slice sets stop the build (select.eligible strict_inputs; only tests and dev pass False); an empty verified set is allowed (stricter). Terms are defined in the named code, which is the authority.
- H5: provenance from the source id (reading 2): only registry sources (human gold per their builders' MANIFEST); Claude-gold and program-labelled sources are excluded by name or prefix.
- H6: the partner shares the base's state, group_id and call_id, so S4 on the base covers it (reading 1); its id (c2_t37b:<hash>) is new; mix_c2.old_slice_clash re-checks every unit.
- H7: "no twin" = no other pool row shares the base's call_id (reading 1); the partner then becomes the unit's second row. Bundle = C1 rows sharing a call_id; attack copy = meta.attack_target; relation edge = a golden_relations line.
- H8: raw string equality (validate_partner); normalisation only for S4.
- H9: 2,000 = partner rows; a full block adds 2,000 base rows counted as replay. Dev: 300 pairs = 300 units = 300 partner rows, written with their 300 dev bases.
- H10: a = base id, b = partner id (fixed). train_decoder's complement and equiv terms are symmetric, so the orientation only fixes the file.
- H11: the plan (select.plan_block) is fixed: bases in uhash(seed, row id) order; implicit up to 30% of the target, then antonym / option framing up to 35% (a base allowing both: uhash pick), then the cut (H48), syntactic fill, then equiv; one kind per base; frame, cue, antonym pair and pool paraphrase by uhash order, first under its cap. Never reads gold (tested).
- H12: gold 1 = yes holds (reading 1); noul rows have no options; the exchanged definitions make 1 - gold exact.
- H13: the prefix is optional; implicit keeps it unchanged before the auxiliary (reading 3); syntactic moves it after the frame with a lowered first letter.
- H14: frame is null except for syntactic; cue is set only for implicit (reading 1).
- H15: the subject starts after the first auxiliary (the question's first word), so a sentence-initial capital is never in it; CAPS = maximal run of capitalised tokens joined by and / or / of / the / de / van / von / &; a lowercase start fails the split, so the base gets no syntactic kind. Subject regexes: sources.ENTRIES.
- H16: program A builds every accepted surface (reading 1); the program writes the partner and picks one surface by uhash(plan id); B splits all of them.
- H17: do-question = first auxiliary do, does or did only (reading 1).
- H18: lack replaces the main verb and the rest follows (reading 1); one partner per base: lack or fail to by uhash when the verb is have / contain / include, else fail to (reading 4). No current registry verb takes lack.
- H19: pairs whose phrase occurs exactly once (word-bounded, case-sensitive) in the base; uhash(seed, "pair", row id, i) order, first under its cap; that one occurrence changes; a repeated phrase refuses the pair.
- H20: the pairs are ("go against" -> "agree with") and ("go against common sense" -> "make sense"); section 2 now says so.
- H21: swap the digit after "Statement " both ways (1 <-> 2); refused unless the question full-matches with exactly one such digit; B: exactly one difflib replace "1" <-> "2" right after "statement".
- H22: anchors = quoted spans, digit runs and capitalised words after the first word, compared as multisets; negation, quantifier and modal words as multisets; the rest rests on the reads and the blind solver.
- H23: FRAMES_DEV = the 3 dev-only frames; dev uses only them, training only FRAMES_TRAIN (tested). "Should the statement that ... be rejected" is a banned C1 dev pattern (LOCAL_BANS), never a T37b frame.
- H24: L_neg = negcount's negation lexicon; "no entry" = negcount k_all 0 and no NEG_B word on every frame (tested).
- H25: a frame asks whether the embedded statement holds under the card's definitions (reading 3); "Is it right to say that" is never used on gd_sc101 acceptable / wrong (sources.FRAMES_EXCLUDED).
- H26: "can" is accepted only as the first auxiliary (reading 1); neither program lists it as a modal; the modal ban covers must, may, might, should, shall, could, would, will, ought, need(s).
- H27: closed lists are in code: A = polarity.QUANT / AFTER_OK / MODAL / SUBORD / COLLECTIVE + negcount; B = polarity_b.NEG_B / QUANT_B / SAFE_AFTER_B / MODAL_B / SUB_B / SHAPE_B. A difference only drops (A = B). Any negation word in the base (never, no, neither ...) refuses syntactic and implicit. "always" counts as a quantifier on purpose; "that" is checked only in the prefix and subject.
- H28: changed: after "not" only any / anything / anyone / anybody / both / either / always (one natural not(...) reading); all / every / each / everything / everyone / everybody are refused in both programs (all-not reading). "not ... either" = neither = not(either), the exact complement.
- H29: "at least one" holds "least" (both quantifier lists), so a swap to "any" fails both programs (reading 1).
- H30: exactly +1 (reading 1); syntactic base (0, 0) -> (1, 1); implicit base k_all 0 -> (1, 0); antonym and option framing: counts and entries equal.
- H31: the relation comes from the kind (four complement kinds, equiv = same); a program returns it only when the kind's construction holds; equal counts alone never mean equiv (reading 1).
- H32: the code is the authority for word lists and tokenisers (reading 1); this page fixes the procedures; B shares no code with A (tested).
- H33: Python re.fullmatch of the entry pattern on the instructions; the card is checked separately; the first entry of the row's source that matches wins, and no fixed question matches two entries (tested).
- H34: N is the source's other label as its builder defines it (reading 2); "exactly" applies to the whole card.
- H35: label space per question as built (reading 2): check_covid's builder drops NEI, so its two questions are in; gd_feverous (NEI folded into no) is excluded.
- H36: answer_equiv is in, equiv only: a human equivalence rating of two given answers, not "is X the correct answer". Label-check = yes means a shown candidate is a task's answer (answer-key gold); vote-share = meta.teacher gold; ordinal-cut = a scale cut at a threshold; DI-adjacent = flagged in LICENCE_REGISTER; list: sources.EXCLUDED.
- H37: answer word = yes or no used as an answer (select.ANSWER_WORD); true / false / supported / refuted are not. A swap entry whose card has one is not a base at all (fail closed).
- H38: the base card is right (reading 1): the definitions speak of the asked-about statement and the answer tracks it (H58).
- H39: wording, not a label (reading 1): the card defines yes / no for the negated question; gold stays 1 - human gold. "Claude" = the C2 build author (Claude Opus 5.5, A37 b); the card is closed, frozen and G13-checked.
- H40: changed: syntactic and implicit partners are exactly program A's strings, so the program writes them (surface by uhash), like antonym and option framing; Haiku writes only the equiv pool (author_pool.rules_for, closed); a paraphrase is used only after lint (both programs 'same' on probe fills), two 'same' reads and admission. hotpotqa (native per-row questions) has no pool, so no equiv.
- H41: two independent reads (two batches: own seed, order, chunks, agent) of each distinct (question_a, question_b) pair; output same | opposite | unclear (else no reading); both must equal the planned relation. A pool paraphrase is read once, as a template (placeholders stand for one shared value).
- H42: the blind solver answers yes | no only; anything else counts as inconsistent (review). It sees text, question and definitions (g5h.read_item), never gold or meta.
- H43: only a blind-solver inconsistency goes to review; program or read failures drop (reading 1).
- H44: review = the orchestrating Claude session on builder.review_items, verdict keep | drop; it sees only pairs that passed programs and reads, never overrides them, never relabels; an unreviewed pair drops.
- H45: shares of the realised complement count C, each floor on its own; antonym + option framing combined; exact integers (4 implicit >= C, 10 non-syntactic >= 3 C).
- H46: source = meta.t37b.base_source; cap = floor(0.10 x realised partner rows), min 1 (200 at 2,000).
- H47: one combined key, exact base question; cap floor(0.02 x realised block) (40 at 2,000). For a fixed question it means "no partner question above 2%"; per-row questions count per question. Added (stricter): each pool paraphrase is a second key under the same cap.
- H48: n_comp = min(1,400, 4 implicit, floor(10 non-syntactic / 3)): the largest count keeping both floors (1,001 needs 251 implicit). After the checks, select.trim_block cuts syntactic (latest first), then over-cap rows; it only removes; equiv is cut only by a cap.
- H49: 300 = units including antonyms; S1-S3 apply to dev bases, S4 does not (dev rows are not replay rows).
- H50: dev bases come from gate dev splits, disjoint from golden_train; T37b-dev is a G13 target (g13_c2), so a training row hitting a dev base drops at G13.
- H51: both licences apply in full (reading 1); C2 wording licence = rows.LICENCE (CC0). A G15 failure drops the whole unit; the base stays an ordinary replay row.
- H52: LOCAL_BANS are case-insensitive regex searches as written ("..." = any text; "only non-" also hits "only non-binary", fail-safe), on partner questions and pool templates; a dropped partner consumes its base.
- H53: G13 = c_build/decontam_g13.py through g13_c2; method 8 = its template check; seed-first = on template_strings() and the frozen pool before any row; a hit removes that piece; a candidate hit drops its unit; G13 runs per family and on the final mix.
- H54: a base also drawn as replay counts once (one row by id), against the replay share, never the 2,000.
- H55: section 2 lists every entry's kinds; sources.ENTRIES (kinds, subject regex) is the authority.
- H56: the subsets are made by their golden_src builders, so every replay row of the source is in; the registry line is the full definition.
- H57: closed world per source: an entry is admitted only when every row carries exactly one of the two labels (exhaustive and exclusive as built), so "no" means the other label holds; exact for the source's labels (reading 3).
- H58: ComVE subtask A pairs one nonsensical statement with one sensible statement by construction (reading 1).
- H59: implicit verbs (support, contradict, confirm, report, make) all have inanimate subjects (evidence, reply, complaint, paragraph): no attempt reading, "fail to V" = "does not V"; "X lacks Y" = "X does not have Y" (reading 1).
- H60: closed vocabularies: reads same | opposite | unclear; solver yes | no; review keep | drop; answer words yes | no; word lists in code (H27).
- H61: section 3 is restated with items 4, 6, 7, 8 and 10 fixed by H26, H35, H37, H58 and H29; every point is resolved here.
