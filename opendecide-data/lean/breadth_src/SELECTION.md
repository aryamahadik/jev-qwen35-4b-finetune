# Breadth corpus (v0.13): dataset selection

Written 27 Sep 2026 by the selector. Criteria were written first (section 1) and then applied to the candidate
metadata (section 2). No model was run, and no ohs*/preds_*/results_* file was opened.

## 1. Criteria (fixed before choosing)

Hard rules (any failure = reject; when unsure, reject):
1. **Exclusions.** Not in `ohs3/used_sources.json` for any use (held-out OHS-1/2/3, dev/selection, eval, JevBench,
   train). Not derived from, or sharing texts with, any of those. **All of `tasksource/zero-shot-label-nli` is
   forbidden**, including the datasets folded into it through aggregates (for example `mbib-base/*`, which contains
   HateXplain, the Contextual Abuse Dataset, Kaggle Jigsaw (Wikipedia talk comments), CMSB, RedditBias, LIAR, ...).
   The 152 task names were re-read from the HF datasets-server statistics endpoint on 27 Sep 2026.
   No text from a platform whose fresh posts are an OHS test source (Stack Exchange, OHS-3 `se_site`), to match the
   earlier AskUbuntu/WebApps rejection.
2. **Provenance.** Human-written texts and human labels only; no LLM-written or LLM-labelled parts.
3. **Licence.** CC0, public domain / US-government work, CC BY, CC BY-SA, MIT, Apache-2.0, ODC-BY/ODbL, stated in a
   file or official record we can cite. Licences outside this list (for example CDLA-Permissive-2.0), licences stated
   only by a third-party mirror, NC, ND, research-only and unknown licences are rejected.
4. **Train split only.** Never test; never a validation split that serves as the benchmark test. Datasets with no
   split count as train.
5. **No model calls.** Claude writes only definitions and questions.

Mix rules:
6. 22-28 datasets, at least 2 per family, no two from the same source dataset and no two with a near-identical label
   taxonomy and framing (for example two "polarity toward a target" sets, or two SUPPORTS/REFUTES Wikipedia sets).
7. Preference order when two candidates compete: real-world decision > many distinct label sets > annotator label
   distributions (calibration) > clean labels > new genre or text length.
8. `max_rows` 300-700 per dataset (upper end for several label sets or soft labels); total 11,000-15,000.
9. Builder duties for every set: 13-gram decontamination against all our train/dev/eval files, exact and 12-word-run
   dedup against BTZSC biasframes (all Gab/Reddit sets), dedup across the selected sets, class caps.

## 2. Decisions

Candidate list note: the candidate JSON handed to the selector was cut off inside the MN-DS entry; any candidates
after MN-DS were not seen and are not selected.

### Selected (23 datasets, 12,600 rows max)

| key | dataset | family | licence | qtype | max_rows |
|---|---|---|---|---|---|
| fm2 | Fool Me Twice | nli_facts | Apache-2.0 | yesno | 600 |
| infotabs | InfoTabs | nli_facts | Apache-2.0 | choice | 600 |
| claimbuster | ClaimBuster crowdsourced | nli_facts | CC BY 4.0 | choice | 450 |
| xed_en | XED English | opinion | CC BY 4.0 | choice | 500 |
| newsmtsc | NewsMTSC | opinion | MIT | choice | 550 |
| emobank | EmoBank | opinion | CC BY-SA 4.0 | choice | 600 |
| politeness_wiki | Stanford Politeness, Wikipedia half only | opinion | CC BY 4.0 | choice | 450 |
| sarcasm_headlines | News Headlines Sarcasm v2 | opinion | CC BY 4.0 | yesno | 300 |
| steam_aspect | Steam Review Aspect | opinion | CC BY 4.0 | yesno | 350 |
| mams_acsa | MAMS (aspect-category detection) | opinion | Apache-2.0 | yesno + choice | 450 |
| edos | EDOS | safety | CC0 1.0 | yesno + choice | 700 |
| ghc | Gab Hate Corpus | safety | CC BY 4.0 | yesno + choice | 650 |
| convabuse | ConvAbuse | safety | CC BY 4.0 | choice + yesno | 500 |
| hatemoji_build | HatemojiBuild | safety | CC BY 4.0 | yesno + choice | 400 |
| topv2 | TOPv2 | intent | CC BY-SA 4.0 | choice | 700 |
| abcd | ABCD | intent | MIT | choice | 650 |
| cfpb | CFPB complaints (pre Nov 2022) | intent | CC0 / US gov | choice | 650 |
| star | STAR (Rasa) | intent | MIT | choice | 550 |
| casino | CaSiNo strategies | intent | CC BY 4.0 | choice + yesno | 500 |
| newsgroups20 | 20 Newsgroups (by-date train) | topic | CC BY 4.0 | choice | 550 |
| congress_policy | US bills CRS policy area | topic | MIT / US gov | choice | 600 |
| wos46985 | Web of Science WOS-46985 | topic | CC BY 4.0 | choice | 650 |
| mnds | MN-DS (IPTC Media Topics) | topic | CC BY 4.0 | choice | 650 |

Per-family: nli_facts 3 (1,650), opinion 7 (3,200), safety 4 (2,250), intent 5 (3,050), topic 4 (2,450).

### Rejected

| dataset | reason |
|---|---|
| FEVER 1.0 | `fever-evidence-related/mwong--fever-related` (FEVER-derived) is a task in the forbidden label-NLI set; VitaminC (OHS-1) is also built from FEVER claims; and its SUPPORTS/REFUTES/NEI taxonomy duplicates FM2/InfoTabs. |
| FEVEROUS | Near-identical taxonomy and framing to FM2 (Wikipedia SUPPORTS/REFUTES; NEI only 3%), and InfoTabs already covers table evidence. FM2 wins on vote distributions and independence from FEVER. |
| CREAK | `CREAK` is a task in the forbidden `tasksource/zero-shot-label-nli` (the candidate check was wrong). |
| Senti4SD | Stack Overflow text (Stack Exchange is an OHS-3 source platform; same rule as the AskUbuntu reject) and its pos/neg/neutral taxonomy duplicates NewsMTSC. |
| Stanford Politeness, Stack Exchange half | Stack Exchange text (OHS-3 platform). Only the Wikipedia half is selected. |
| MAMS ATSA (polarity part) | Target-polarity taxonomy duplicates NewsMTSC; only ACSA aspect-category detection is used. |
| DynaHate | `dynahate` is a task in the forbidden label-NLI set (the candidate check was wrong). |
| Wikipedia Talk Detox (attack/aggression/toxicity) | Its comments are reused by Kaggle Jigsaw, which is inside `mbib-base/hate-speech`, a forbidden label-NLI task; text overlap cannot be ruled out. |
| CAD (Contextual Abuse Dataset) | Inside `mbib-base/text-level-bias`, a forbidden label-NLI task. |
| HateXplain | Inside `mbib-base/hate-speech`, a forbidden label-NLI task. |
| MTOP (English) | Same TOP family and IN:* taxonomy as TOPv2, 38% of utterances shared. |
| doc2dial | Licence stated only on the HF card (no licence file in the release); dialogue acts already covered (silicone/pragmeval). |
| DSTC11 Track 2 insurance | CDLA-Permissive-2.0 is not on the allowed licence list; synthetic-call check unconfirmed. |
| News Category (HuffPost) | News-topic taxonomy overlaps MN-DS; noisy editorial section tags that need merging; headlines overlap the HuffPost half of the Sarcasm set. MN-DS wins (manual labels, official IPTC definitions, full articles). |
| Candidate-side rejects (kept rejected) | HoVer (partly BERT-generated claims), Climate-FEVER (test-only, licence unknown), AmbiFC and NLI4CT (no licence), WiCE (GPT-3.5 sub-claims), SciTail (no licence, NC source), HealthVer/ANLI/SICK (NC), StrategyQA (in label-NLI), PerSenT (licence unknown), SemEval ABSA (NC original), OpeNER (no licence), M-ABSA (translated), Cleanlab politeness (noised labels), figlang sarcasm (no licence), GoodNewsEveryone (text rights), steam constructiveness (label provenance unknown), CheckThat subjectivity (NC), tasksource subjectivity (in label-NLI), crowd-enVent (unverifiable), Davidson and Stormfront (in label-NLI and SBF), UCC (NC), ETHOS (in label-NLI, GPL), ToxiGen/BeaverTails/Aegis/DICES/ProsocialDialog (LLM text), ToxicChat (NC), OpenAI moderation (test-only), HatemojiCheck (HateCheck derivative), MultiWOZ 2.2, Coarse Discourse, Harper Valley, MIDAS, Bitext, Twitter Customer Support, Frames/MetaLWOz, ATIS, Braun NLU, Reuters/RCV1, Blog Authorship, Blurb Genre, register_oscar/mc4, Open Food Facts, EURLEX/MultiEURLEX, Amazon categories, hyperpartisan and crowdflower sets. |

## 3. Builder notes (per selected set)

- fm2: train.jsonl only; premise = gold_evidence; soft label = correct_votes/total_votes where total_votes >= 3.
- infotabs: train parquet only; linearise the infobox as "Key: value" lines; 3-way.
- claimbuster: crowdsourced.csv only, never groundtruth.csv; 3-way NFS/UFS/CFS; balance classes.
- xed_en: en-annotated.tsv single-label lines + neu_en.txt; drop lines under 4 words; never the fi/projected files.
- newsmtsc: train.jsonl at commit 6b838e00 only; question names the target mention; use the two-target sentences as contrast pairs.
- emobank: split=='train' rows of corpus/emobank.csv; drop 'SemEval' ids; keep only clear extremes; three label sets (valence, arousal, dominance); soft labels from rater spread.
- politeness_wiki: ConvoKit wikipedia-politeness-corpus only; 3-way from Binary; soft from 5 ratings; drop texts in Cleanlab test.csv.
- sarcasm_headlines: raquiba train.json only; drop article_link; redact 'onion'/'huffpost'; dedup against MN-DS and NewsMTSC.
- steam_aspect: train split only; yes/no per aspect using the card's definitions; use cleaned_review.
- mams_acsa: MAMS-ACSA/raw/train.xml only; questions: "Does the sentence give an opinion on <category>?" and "Which aspect category is discussed?"; no polarity rows.
- edos: split=='train'; binary + 11-way vector (category optional); soft labels from the individual-annotations file; dedup vs biasframes.
- ghc: ghc_train.tsv only; HD / CV / VO yes/no and target choice; soft labels by joining annotations on text; dedup vs biasframes.
- convabuse: ConvAbuseEMNLPtrain.csv only; state = user utterance (+ prev_user); severity scale, type, target; soft labels.
- hatemoji_build: train.csv only; label_gold + type; keep original/perturbation pairs together.
- topv2: official zip, <domain>_train.tsv only; top-level IN:* label; cap per label; sibling intents as distractors.
- abcd: train key only; state = first 1-3 customer turns; merge FAQ subflows to the 55 official intents.
- cfpb: Date received < 2022-11-01; dedup template letters; merge renamed legacy products; cap credit reporting.
- star: user text only; skip MultiTask dialogues; first non-greeting user turn.
- casino: single-label utterances as choice, multi-label as yes/no per label; cap non-strategic/small-talk.
- newsgroups20: SetFit train.jsonl only (never the by-date test); drop very short posts.
- congress_policy: CRS summary (or title) as state; drop 'Social Sciences and History' and 'Private Legislation'; congress.gov policy-area descriptions as definitions.
- wos46985: abstract only, never keywords; Domain 7-way and area-within-domain; cap Medical/biochemistry. Verifier: only records whose author keywords name their WOS area (retrieval-keyword labels are otherwise noisy, e.g. "Attention" sensor papers); area-name-in-text rows ~1/3 of area task; stricter copyright-notice stripping; cut-off abstracts dropped.
- mnds: level-1 (17) and level-2-within-parent choices; IPTC official definitions; dedup vs NewsMTSC/sarcasm.
