# Scout report: topic, emotion, sentiment and ordinal-score sources

Project: OpenDecide (GLiClass Edge v3 / modern-base v3 fine-tuned into a Jev-style System One).
Scout date: 2026-09-25. Environment: macOS, python 3.12, `datasets` 4.8.5, `transformers` 4.57.6, `huggingface_hub` 0.36.2.
Every dataset below was loaded with `datasets.load_dataset(..., streaming=True)` or, when that failed, through the parquet
conversion ref or a direct file download. Row counts come from the HF dataset-viewer `/size` endpoint and were
cross-checked by streaming. Scratch scripts and caches live in the session scratchpad. Nothing outside this folder was modified.

---

## 0. Summary

**Short version:** only five sources in this family are clean enough to train a commercial model on:
`fancyzhx/dbpedia_14` (CC BY-SA 3.0), `google-research-datasets/go_emotions` (Apache-2.0),
Women's E-Commerce Clothing Reviews (CC0, from Kaggle), the UCI Drug Review dataset (CC BY 4.0) and
`zeroshot/twitter-financial-news-sentiment` (MIT). Almost every well-known benchmark (AG News, Yelp, IMDB, Yahoo, Financial
PhraseBank, DAIR Emotion, SST) is non-commercial or has an unclear licence. Several of them are also already in the
DeBERTa zero-shot training mix or in GLiClass's benchmark tables. So they belong in eval only, shipped as a build script plus source IDs.

| Role | Datasets (this family) |
|---|---|
| **TRAIN** (commercial-friendly, human labels, not in baselines' training) | `fancyzhx/dbpedia_14` (topic, 14-way plus a deterministic super-class hierarchy); `google-research-datasets/go_emotions` (emotion, raw rater votes, use the items where 2 or more raters agree); Women's Clothing Reviews (`saattrupdan/womens-clothing-ecommerce-reviews`, CC0: **Score 1-5 + Noul "recommend" + Choice department** on the same state); UCI Drug Reviews (`lewtun/drug-reviews`, CC BY 4.0: **Score 1-10**, the only 10-level human scale found) |
| **EVAL in-domain** | Held-out test splits of those four sources, deduplicated and grouped (the drug-review split **must be regrouped**: 67% of test texts also appear in train) |
| **EVAL zero-shot** (never trained on) | SST-5 (`stanfordnlp/sst` parquet, continuous 3-rater labels: Score 5); SuperTweetEval `tweet_sentiment` (5-point, target-based Score); Financial PhraseBank (agreement tiers, from the original zip); `zeroshot/twitter-financial-news-sentiment` (cleanest for every baseline); `cardiffnlp/tweet_topic_single` (topic, 6-way) |
| **EVAL comparability** (to match the community audit) | BTZSC `agnews` + `emotiondair` at revision `fef2a2ac…`, 100 items each, using AbdelStark's exact sampler (seed 20260917). I reproduced the sampler below. Flag both as contaminated or benchmark-exposed. DAIR Emotion labels are **machine-generated**. |
| **AVOID** | yahoo_answers_topics, SetFit/bbc-news, IMDB, Yelp (except as optional non-commercial eval), amazon_polarity, amazon_reviews_multi (all mirrors), sealuzh/app_reviews, argilla/tripadvisor, stepp1/tweet_emotion_intensity, SetFit/emotion (copy of DAIR), the mislabelled FPB mirrors |

Key hazards found by measurement (section 2):
1. **SST-5 test is 71.3% inside rotten_tomatoes TRAIN**, and SST-2 validation is 78.0% inside it (normalized exact match). Any model trained on rotten_tomatoes has seen the SST sentences. DeBERTa zeroshot v1.1 and v2.0 non-`-c` were trained on rotten_tomatoes. Never put RT in train while SST is in eval.
2. **UCI drug reviews: 32,115 of the 48,224 unique test reviews also appear in train.** The same review is posted under brand and generic drug names. Split by normalized review text instead.
3. **TweetEval vs SuperTweetEval:** sentiment test sets share 35.5% of texts exactly (62% by 60-character prefix), and emotion test sets share 82.8%. Treat each pair as one family when deduplicating.
4. **GLiClass pretraining corpus** (`knowledgator/gliclass-v2.0`, 1,196,218 rows, which matches the paper's "1.2M"): it contains **6.8% of TweetEval-sentiment TRAIN** texts and 3.5-5.6% of SuperTweetEval-sentiment train. Every candidate *test* split had about 0% overlap (table in 2.1). Amazon-polarity content is declared in the GLiClass training data.
5. **GoEmotions:** 1.66% of test texts also appear in train. Surge AI audited 1,000 items and judged 30.8% severely mislabelled. Mitigate with the raw per-rater votes (2.4).
6. **DAIR Emotion** (`dair-ai/emotion`): the card says `annotations_creators: machine-generated` (hashtag distant supervision), and the licence is "educational and research purposes only". This breaks the "human gold" rule. Keep it only for the 100-item comparability slice, and flag it.

---

## 1. Baseline training-data exposure (needed for the zero-shot track)

### 1.1 GLiClass v3 (edge-v3.0 `df03993a…`, modern-base-v3.0 `ac369222…`, both Apache-2.0)
- The v3 cards list only the post-training sets: `BioMike/formal-logic-reasoning-gliclass-2k`, `knowledgator/gliclass-v3-logic-dataset`
  (7,776 rows: FineWeb, CommonsenseQA and similar text, LLM-labelled) and `tau/commonsense_qa`. They are LoRA fine-tunes of earlier GLiClass checkpoints.
- The paper (arXiv 2508.07662) describes three stages. Pre-training uses a 1.2M-example general corpus whose sources it does not name. Mid-training uses a subset of it.
  Post-training uses logic/NLI data (CommonsenseQA, 2k synthetic items, MultiNLI) plus a "pattern" stream built from
  **`fancyzhx/amazon_polarity` content** and `m-a-p/FineFineWeb`, labelled with GPT-4o.
- The earlier `gliclass-modern-*-v2.0-init` cards declare this pre-training mix: `MoritzLaurer/synthetic_zeroshot_mixtral_v0.1`,
  `knowledgator/gliclass-v1.0`, **`fancyzhx/amazon_polarity`**, `cnmoro/QuestionClassification`, `Arsive/toxicity_classification_jigsaw`,
  `shishir-dwi/News-Article-Categorization_IAB`, `SetFit/qnli`, `nyu-mll/multi_nli`, `SetFit/student-question-categories`,
  **`SetFit/tweet_sentiment_extraction`**, `SetFit/hate_speech18`, `saattrupdan/doc-nli`.
- `knowledgator/gliclass-v2.0` (sha `93d3cdc8…`, 1,196,218 rows, Apache-2.0) is very likely the "1.2M" pre-training corpus.
  The row count matches, but no card says so. Its top gold labels show which sources went in: IAB news categories (shopping, travel, real estate…),
  toxic/obscene/insult/identity hate (Jigsaw), positive/negative/neutral, entailment/contradiction, subjective/objective, Chemistry/Physics/Maths/Biology,
  and noHate. I hashed every text in it and compared the hashes against our candidates (2.1).
- **Benchmark exposure:** the GLiClass v3 card reports "zero-shot" F1 on CR, sst2, **sst5**, **20_newsgroups**, spam,
  **financial_phrasebank**, **imdb**, **ag_news**, **emotion**, cap_sotu, **rotten_tomatoes**, massive, banking77 and snips.
  These were not trained on, but they were used to report and select models. Flag them as "benchmark-exposed" rather than "trained".

### 1.2 DeBERTa zero-shot (MoritzLaurer)
- `deberta-v3-{base,large}-zeroshot-v2.0-c` (the "-c" variants) were trained only on Mixtral synthetic data plus MNLI and FEVER-NLI. **Use these as the clean,
  commercial-friendly DeBERTa baseline.**
- `deberta-v3-*-zeroshot-v2.0` (no "-c") and `deberta-v3-base-zeroshot-v1.1-all-33` were also trained on up to 500 examples per class from 28
  classification sets: **amazonpolarity, imdb, appreviews, yelpreviews, rottentomatoes, emotiondair, emocontext, empathetic,
  financialphrasebank**, banking77, massive, wikitoxic_*, hateoffensive, hatexplain, biasframes_*, **agnews, yahootopics**,
  trueteacher, spam, wellformedquery, manifesto, capsotu (plus ANLI, WANLI and LingNLI). Moritz's `datasets_overview.csv`
  records sst2 and twitter_financial_news_sentiment as **excluded**.
- **BTZSC (`btzsc/btzsc`) is exactly the test half of those 22 Moritz datasets**, rewritten as NLI pairs. So on BTZSC, the non-`-c` DeBERTa is
  in-distribution, not zero-shot.

### 1.3 Small instruction-tuned LLMs
- P3/T0 and the FLAN collections include several of these sets as training tasks (e.g. ag_news, dbpedia_14, imdb, yelp, amazon_polarity,
  app_reviews, rotten_tomatoes, sst2). For any Flan-style or open small-LLM baseline, assume the classic benchmarks were seen. Report the small-LLM
  zero-shot track mainly on TFNS, FPB, tweet_topic_single, SuperTweetEval sentiment and the clothing/drug held-outs.
- Jev's training data is unknown. AbdelStark says outright that its BTZSC numbers are "benchmark performance, not clean evidence of
  uncontaminated generalization." Put the same caveat on our comparability slice.

---

## 2. Measurements (run in this scout)

### 2.1 Exact and prefix overlap with the GLiClass pre-training corpus
Normalization: lowercase, every non-alphanumeric run collapsed to one space. `exact` = whole normalized text matches.
`prefix60` = first 60 normalized characters match (only texts of 60 or more characters). `logic` = overlap with `gliclass-v3-logic-dataset`.
Large splits were capped at the first 20k rows.

| candidate split | n unique | exact | prefix60 | logic |
|---|---:|---:|---:|---:|
| ag_news/test | 7,599 | 0.00% | 0.03% | 0 |
| dbpedia_14/test (title+content) | 20,000 | 0.00% | 0.01% | 0 |
| yahoo/test (title) | 19,933 | 0.03% | 0.00% | 0 |
| 20ng/test | 7,288 | 0.03% | 0.00% | 0.01% |
| dair_emotion/test | 2,000 | 0.00% | 0.00% | 0 |
| go_emotions/test | 5,408 | 0.22% (short generic comments) | 0.00% | 0.04% |
| sst5/test | 2,210 | 0.05% | 0.00% | 0 |
| rotten_tomatoes/test | 1,066 | 0.00% | 0.00% | 0 |
| imdb/test | 19,835 | 0.00% | 0.00% | 0 |
| tweet_eval.sentiment/test | 12,271 | 0.00% | 0.01% | 0 |
| **tweet_eval.sentiment/train** | 19,981 | **6.78%** | **6.79%** | 0 |
| super_tweeteval.tweet_sentiment/test | 12,278 | 0.00% | 0.01% | 0 |
| **super_tweeteval.tweet_sentiment/train** | 19,908 | **3.54%** | **5.63%** | 0 |
| tweet_eval.emotion/test | 1,421 | 0.00% | 0.00% | 0 |
| super_tweeteval.tweet_emotion/test | 3,259 | 0.00% | 0.00% | 0 |
| tweet_topic_single/test_2021 | 1,692 | 0.00% | – | – |
| tfns/validation | 2,388 | 0.00% | 0.00% | 0 |
| fpb (all 4,846 sentences) | 4,835 | 0.00% | 0.00% | 0 |
| yelp_full/test | 20,000 | 0.00% | 0.00% | 0 |
| amazon_polarity/test | 19,997 | 0.00% | 0.01% | 0 |
| amazon_multi_en/test | 5,000 | 0.00% | 0.00% | 0 |
| app_reviews/train | 18,241 | 0.03% | 0.00% | 0.04% |
| drug_reviews/test | 19,216 | 0.00% | 0.00% | 0.01% |
| clothing/test, clothing/train | 1,000 / 19,995 | 0.00% | 0.00% | 0 |
| tripadvisor (jniimi) | 19,999 | 0.00% | 0.00% | 0 |
| fiqa_sa/test | 229 | 0.00% | 0.00% | 0 |

Caveats: the hashes only catch exact or prefix copies (a paraphrase or truncated snippet would slip through). The corpus may not be the complete mix.
The amazon_polarity and FineFineWeb pattern stream is declared but was not hashed.

### 2.2 Cross-dataset and within-dataset leakage (normalized exact)
| pair | overlap |
|---|---|
| SST-5 test vs rotten_tomatoes train | **1,576 / 2,210 (71.3%)** |
| SST-5 train vs rotten_tomatoes test | 821 / 8,533 (9.6%) |
| SST-2 validation vs rotten_tomatoes train | **680 / 872 (78.0%)** |
| TweetEval sentiment test vs SuperTweetEval sentiment test | **4,357 / 12,271 (35.5%)**; 7,630 by prefix60 |
| TweetEval emotion test vs SuperTweetEval emotion test | **1,177 / 1,421 (82.8%)** |
| Drug reviews: test texts also in train | **32,115 / 48,224 unique (66.6%)**. Train is 112,196 unique of 161,297 rows |
| GoEmotions test in train | 90 / 5,408 (1.66%) |
| DAIR emotion test in train | 11 / 2,000 (0.55%) |
| AG News test in train | 15 / 7,599 (0.20%) |
| TFNS validation in train | 15 / 2,388 (0.6%); 44 by prefix60 |
| Yelp-5 test (first 20k) in train | 12 (0.06%) |
| DBpedia test (first 20k) in train | 0 |
| Clothing test in train | 2 / 1,000 |
| TweetEval sentiment test in its own train | 0 |

**Rule for the build:** make one global hash index (normalized exact, prefix60 and MinHash for near-duplicates) over everything in train.
Drop any eval state that hits it. Also drop eval states that hit sibling datasets of the same family: RT/SST/SST-2, TweetEval/SuperTweetEval/SemEval-2018,
Yelp-full/Yelp-polarity, and drug brand/generic duplicates.

### 2.3 AbdelStark/jev-benchmarks comparability (read from the repo at commit `0d610cc…`, code Apache-2.0)
- Config `configs/pilot-v1.yaml`: `btzsc/btzsc` revision **`fef2a2ac62b69c58670047dddf045c53d7c3cb5e`**, 100 samples per dataset,
  datasets `[agnews, emotiondair, banking77]`, **seed 20260917 + dataset_offset** (0, 1, 2), 10 ECE bins, 5% error budget,
  2,000 stratified paired bootstrap resamples.
- The Jev call from `adapters/jev.py`:
  `client.system_one(state={"text": text}, questions={"label": Choice(instructions="Which single label best describes the input text?", criteria={"label_000": <BTZSC hypothesis 0>, ...}) })`.
  The criteria are the BTZSC **hypothesis strings** in BTZSC order (e.g. "This example news text is about business news"). Probabilities come from
  `response.choices["label"].probabilities[key]`. Two Jev vectors summed to 0.99 and were renormalized.
- Sampler (`src/jev_benchmarks/data.py`): infer the class count from repeated texts. For each example, the target is the index of the single `labels==1` row.
  Examples without exactly one positive are dropped (the 200 out-of-scope banking rows). Then per class, `random.Random(seed).shuffle` the indices and pop round-robin over sorted classes.
  **I re-implemented it and ran it.** agnews: 7,600 valid, 100 selected, 25 per class, first IDs `agnews:9, 267, 292, 427, 437`.
  emotiondair: 2,000 valid, 17/17/17/17/16/16, first IDs `emotiondair:23, 25, 50, 56, 63`. banking77: 2,880 valid of 3,080.
  The counts match the audit's text. Their manifest is gitignored, so ID-level identity is unverified but follows from the deterministic code.
- Their Jev numbers (jev-1.13.0, n=100): AG News acc 0.910, Brier 0.146, NLL 0.495, ECE 0.064, coverage at 5% error 0.83.
  DAIR Emotion acc 0.480, Brier 0.846, **NLL 5.588**, **ECE 0.351**, coverage 0.00. Jev gave exactly 0 probability to the true label on 16% of items.
  The emotion slice is where Jev's calibration fails most visibly, which makes it a strong demonstration slice even though its labels are noisy.
- The other audits checked (jev-calibration-audit: KoBBQ/MMLU-ProX; jevbench: authored items) use no topic or sentiment sets, so they do not constrain this family.

### 2.4 Label-quality measurements
- **GoEmotions raw** (`raw` config, 211,225 rater rows, 58,011 items). Raters per item: 3 raters for 37,335 items, 5 for 17,910, 4 for 2,104, 2 for 592, 1 for 70.
  93.5% of items have at least one fine label chosen by 2 or more raters, and 22.7% are unanimous. On the Ekman 7-way grouping, 98.4% have a 2-rater majority,
  36.1% are unanimous, and **47,548 items (82%) have exactly one Ekman category with 2 or more votes**. That is the clean single-label pool.
  `example_very_unclear` is never true in this HF copy.
- **Financial PhraseBank** agreement tiers from the original zip: 50Agree 4,846 (neu 2,879 / pos 1,363 / neg 604); 66Agree 4,217; 75Agree 3,453;
  AllAgree 2,264 (1,391 / 570 / 303). Each sentence's tier gives a per-item human-certainty level.
- **SST** (`stanfordnlp/sst`, parquet): each sentence has a continuous label in [0,1], the averaged phrase sentiment. Binning with edges 0.2/0.4/0.6/0.8
  reproduces SetFit/sst5 exactly (test 279/633/389/510/399). So we can drop near-boundary items from Score eval and use the continuous value as a soft target.
- **Clothing reviews**, rating vs recommended (train, n=20,641): rating ≥4 but not recommended = 169; rating ≤2 but recommended = 97.
  **So 1.3% of authors contradict themselves** across two related human labels. That is a useful human "consistency floor". Rating 3 splits 1,503 not-recommended vs 1,083 recommended, so it is genuinely ambiguous.
- **Drug reviews** rating distribution (test, first 20k): 10 = 6,238; 9 = 3,464; 1 = 2,777; 8 = 2,266; the other levels 670-1,164. Skewed to the extremes. Stratify for eval.
- **SuperTweetEval tweet_sentiment** test: 0 = 177, 1 = 3,545, 2 = 6,194, 3 = 2,332, 4 = 131 (very few extreme items). There are 125 targets with 100 tweets each.
  The card's label-name list ("negative or neutral" for 2) looks wrong. Use SemEval-2016 Task 4C semantics: 0..4 = strongly negative..strongly positive.

---

## 3. Dataset cards (one per scouted source)

Legend: **C/R** = commercial use OK / redistribution of text OK. "GLi" = GLiClass exposure, "DeB" = DeBERTa exposure.

### Topic

**fancyzhx/ag_news**. Loads on main; sha `eb185aade064a813bc0b7f42de02595523103ca4`.
- Splits: train 120,000 / test 7,600. Text `text`. Label `label` ClassLabel(4): World, Sports, Business, Sci/Tech (balanced, 1,900 per class in test). Median 37 words.
- Sample: "Wall St. Bears Claw Back Into the Black (Reuters) Reuters - Short-sellers, Wall Street's dwindling band of ultra-cynics, are seeing green again." → Business.
- Licence: card says `unknown`. The card text itself says the AG corpus is for "research purposes … and any other non-commercial activity". **C: no. R: no** (build script plus IDs).
- Noise: labels are source-feed categories (metadata), not annotation. Some World/Business and Sci/Tech/Business overlap. HTML artifacts (`#39;`). 0.2% of test texts are also in train.
- Exposure: GLi benchmark-exposed. DeB non-`-c` trained on it. Also in P3/FLAN. It is in BTZSC.
- **Role: eval-comparability only** (the 100-item BTZSC slice). Not for training, and not a clean zero-shot claim.

**fancyzhx/dbpedia_14**. Loads on main (config `dbpedia_14`); sha `9abd46cf7fc8b4c64290f26993c540b92aa145ac`.
- Splits: train 560,000 / test 70,000. Text `title` + `content`. Label `label` ClassLabel(14): Company, EducationalInstitution, Artist, Athlete, OfficeHolder,
  MeanOfTransportation, Building, NaturalPlace, Village, Animal, Plant, Album, Film, WrittenWork. Median 52 words.
- Sample: title "E. D. Abbott Ltd", content "Abbott of Farnham E D Abbott Limited was a British coachbuilding business…" → Company.
- Licence: **CC BY-SA 3.0 + GFDL** (Wikipedia). **C: yes** (attribution). **R: yes, under share-alike**.
- Noise: labels are DBpedia ontology classes (curated metadata, not annotation for this task). The task is easy (supervised models score about 99%) and some Village/NaturalPlace items are ambiguous.
  0 test-in-train overlap in the first 20k rows.
- Exposure: not in the GLi pretraining hashes (0%), not in the GLi benchmark list, not in DeB's 28 sets. It is in P3/T0.
- **Role: TRAIN (topic Choice) + eval-in-domain.** Useful extra: a deterministic super-class map (Person = Artist∪Athlete∪OfficeHolder; Organisation = Company∪EducationalInstitution;
  Place = Building∪NaturalPlace∪Village; Species = Animal∪Plant; Work = Album∪Film∪WrittenWork; Vehicle = MeanOfTransportation) gives exact
  multi-granularity consistency targets: P(Noul "about a person") = ΣChoice P(Artist, Athlete, OfficeHolder). Because it is easy, cap it at about 1k states and sample the ambiguous classes more often.

**community-datasets/yahoo_answers_topics**. Loads on main; sha `6652a1e7…`.
- Splits: train 1,400,000 / test 60,000. Text `question_title`, `question_content`, `best_answer`. Label `topic` ClassLabel(10) (Society & Culture … Politics & Government).
- Licence: card `unknown`. The source is Yahoo! Webscope (non-commercial research). **C: no. R: no.**
- Noise: labels are the categories users picked (silver). Many questions fit several categories.
- Exposure: DeB trained on it (yahootopics). In BTZSC.
- **Role: AVOID.**

**SetFit/20_newsgroups**. Loads on main; sha `f1b91292…`.
- Splits: train 11,314 / test 7,532. Text `text`. Labels `label` int plus `label_text` (20 newsgroup names).
- Licence: no card metadata. Upstream has no clear licence. The text contains names, emails and signatures (PII). **C: unclear. R: build script only.**
- Noise: newsgroup of posting, not annotation. Near-duplicate cross-posts (7,288 unique of 7,532 test). Long tail of lengths (p95 543 words).
- Exposure: GLi benchmark-exposed.
- **Role: AVOID** (optionally a flagged zero-shot extra; the long texts also hurt the CPU budget).

**cardiffnlp/tweet_topic_single**. Main uses a loading script and **fails**. Works via
`load_dataset("cardiffnlp/tweet_topic_single", revision="refs/convert/parquet", data_files={"test":"tweet_topic_single/test_2021/*.parquet", ...})`
(parquet commit `258efb7f0add57e5ed70f7d66dbdc7b90dcbf871`; main sha `87b7a0d1…`).
- Splits: train_2020 2,858, train_2021 1,516, validation_2020 352, validation_2021 189, test_2020 376, **test_2021 1,693**, plus random/coling variants.
  Fields `text`, `date`, `label` ClassLabel(6): arts_&_culture, business_&_entrepreneurs, pop_culture, daily_life, sports_&_gaming, science_&_technology; `label_name`, `id` (tweet ID).
- Test_2021 distribution: pop_culture 671, sports_&_gaming 630, daily_life 178, sci_tech 88, business 78, arts 48.
- Sample: "Philadelphia clearly didn't take a page out of the {{USERNAME}} Game 7 playbook…" → sports_&_gaming.
- Licence: card `other` (Twitter ToS). **C: unclear. R: tweet IDs plus build script.** The annotation is human (COLING 2022 paper).
- Exposure: 0/1,692 in GLi pretraining. Not in DeB or GLi benchmarks.
- **Role: eval-zero-shot (topic).** A temporal split (train 2020 → test 2021) is available.

**SetFit/bbc-news**. Loads; sha `9c31f708…`. train 1,225 / test 1,000, 5 labels. BBC copyright content. **Role: AVOID.**

### Emotion

**dair-ai/emotion** (config `split` for 16,000 / 2,000 / 2,000, or `unsplit` for 416,809). Loads; sha `cab853a1dbdf4c42c2b3ef2173804746df8825fe`.
- Text `text`. Label `label` ClassLabel(6): sadness, joy, love, anger, fear, surprise. Test: joy 695, sadness 581, anger 275, fear 224, love 159, surprise 66.
- Sample: "im updating my blog because i feel shitty" → sadness.
- Licence: `other`, "educational and research purposes only". **C: no. R: build script.**
- **Labels are machine-generated** (card `annotations_creators: machine-generated`; hashtag distant supervision per Saravia et al. 2018). Moritz's list calls it "noisy, requires cleaning".
- Exposure: DeB trained on it. GLi benchmark-exposed. In BTZSC (`emotiondair`). `SetFit/emotion` (`6c362e04…`) is the same data.
- **Role: eval-comparability only** (the BTZSC 100-item slice). It fails the human-gold rule, so flag it and never pool it into headline accuracy.

**google-research-datasets/go_emotions**. Configs `simplified` (train 43,410 / val 5,426 / test 5,427) and `raw` (211,225 rater rows). Loads; sha `add492243ff905527e67aeb8b80c082af02207c3`.
- Text `text`. Label `labels` (multi-label list over 28: admiration … neutral). The raw config has `rater_id` and one 0/1 column per emotion. Median 12 words.
- Sample: "My favourite food is anything I didn't have to cook myself." → [neutral].
- Licence: Apache-2.0 (card). The text is from Reddit. **C: yes. R: yes.**
- Noise: 3-5 crowdworkers per item. Surge AI judged 30.8% of 1,000 sampled items severely mislabelled (sarcasm, slang). 1.66% of test texts are also in train.
- Exposure: GLi about 0.2% exact (generic short comments). Not in DeB (it used emocontext/empathetic/emotiondair). Not in any benchmark list.
- **Role: TRAIN + eval-in-domain.** Use the raw config. Build states from items where one Ekman group (or one fine emotion) has 2 or more votes. Use rater vote fractions as
  **soft targets for Noul calibration** (compare model P to the human agreement rate). For eval, take unanimous or ≥2/3 items and dedupe against train.
  Ask about one emotion at a time with Noul. The labels are multi-label, so there is **no** complement rule *across* emotions. Only same-emotion negation is deterministic.

**cardiffnlp/tweet_eval `emotion`** (train 3,257 / val 374 / test 1,421; 4 labels anger, joy, optimism, sadness). Also **`cardiffnlp/super_tweeteval` `tweet_emotion`** (6,838 / 886 / 3,259; 11-way multi-label `gold_label_list`).
- Both come from SemEval-2018 Task 1 (82.8% test overlap). The tweet_eval card lists this licence as "Undefined" plus Twitter ToS. **C: unclear. R: build script.**
- Exposure: 0% in GLi. Not in DeB.
- **Role: optional eval-zero-shot for emotion** (use SuperTweetEval's 11-way multi-label as Noul questions). Dedupe the two against each other. Low priority.

**SemEvalWorkshop/sem_eval_2018_task_1**. Main is script-based, but the parquet ref loads (E-c subtask only: `ID`, `Tweet`, 11 bool emotions; the sample row was Arabic). Duplicates the above. **AVOID.**

**stepp1/tweet_emotion_intensity**. Loads (3,960 / 3,142). **Every test label is `*_NONE`**, meaning no intensity gold. No card. **AVOID.**

### Sentiment (nominal or binary)

**cardiffnlp/tweet_eval `sentiment`**. Loads; sha `b3a375baf0f409c77e6bc7aa35102b7b3534f8be`. train 45,615 / val 2,000 / test 12,284.
Text `text`, label ClassLabel(3): negative, neutral, positive (test 3,972 / 5,937 / 2,375).
- Licence: **CC BY 3.0** (SemEval-2017 Task 4) plus Twitter ToS. **C: yes-ish for the labels. R: tweet text is restricted by the ToS**, so ship IDs plus a build script.
- Exposure: **6.8% of its train is in GLi pretraining**. Test is clean. Not in DeB.
- **Role:** eval-zero-shot possible, but it overlaps SuperTweetEval sentiment. Prefer SuperTweetEval (5-point Score) and use this as its 3-class sibling only after deduplication.

**zeroshot/twitter-financial-news-sentiment** (TFNS). Loads; sha `ccbe24de388e287beb92dd393a335c376b350ac3`. train 9,543 / validation 2,388.
Text `text`, label int: 0 Bearish, 1 Bullish, 2 Neutral (val 347 / 475 / 1,566). Median 12 words.
- Sample: "$TAP - Barclays cools on Molson Coors https://t.co/…" → Bearish.
- Licence: **MIT**. **C: yes. R: yes** (tweets, but released under MIT; still prefer shipping a build script).
- Noise: annotation provenance is undocumented (card `annotations_creators: other`; only a blog post). Moritz's review: "not enough information on data quality".
  Hand-check about 100 eval items before use.
- Exposure: **clean for every baseline** (0% in GLi; DeB explicitly excluded it).
- **Role: eval-zero-shot (finance sentiment).** Bearish and bullish are not complements (neutral exists), which makes a good trap for naive P(not A) = 1 − P(A) rules.

**Financial PhraseBank** (`takala/financial_phrasebank`, sha `8d3fe0c36d5feec6b3cc5e455b0fcb4820fb9964`)
- `load_dataset` **fails** ("Dataset scripts are no longer supported"). There is **no** `refs/convert/parquet`.
- **Working recipe:** `hf_hub_download("takala/financial_phrasebank", "data/FinancialPhraseBank-v1.0.zip", repo_type="dataset", revision="8d3fe0c3…")`,
  then parse `Sentences_{50,66,75,All}Agree.txt` (latin-1, `sentence@label`). Counts are in 2.4.
- Mirrors: `mteb/financial_phrasebank` (`9349ecd3…`, AllAgree only, 1,129/1,129 train/test, label 0/1/2 with no names); `warwickai/financial_phrasebank_mirror` (`ff574606…`, 50Agree 4,846, no split);
  `atrost/financial_phrasebank` (`fc7fb491…`, 3,100/776/970); `gtfintechlab/financial_phrasebank_sentences_allagree` (`c9e6cd6b…`, needs config `5768`/`78516`/`944601`, and **wrongly claims cc-by-sa-3.0**).
  Use the original zip: it keeps the agreement tiers and the licence file.
- Label: negative / neutral / positive, "from an investor's perspective". Sample: "EBIT margin was up from 1.4 % to 5.1 % ." → positive.
- Licence (License.txt in the zip): **CC BY-NC-SA 3.0**; commercial use requires contacting the authors. **C: no. R: build script** (non-commercial research eval).
- Exposure: DeB non-`-c` trained on it. GLi benchmark-exposed. In BTZSC (690 items). 0% in GLi pretraining.
- **Role: eval-zero-shot (flagged for DeB non-`-c`).** Use AllAgree or 75Agree for the gold set, and the lower tiers for "human-uncertain" calibration analysis.
  Because the labels are ordinal, it also works as a 3-level Score, which enables a Score-vs-Choice agreement test on the same state.

**cornell-movie-review-data/rotten_tomatoes** (`aa13bc28…`; 8,530 / 1,066 / 1,066; neg/pos). Licence unknown.
DeB trained on it. GLi benchmark-exposed. It **contains most SST sentences**. **AVOID** (it would contaminate SST-5).

**stanfordnlp/sst2** (`8d51e7e4…`; 67,349 / 872 / 1,821 (test unlabeled)). Licence unknown. 78% of validation is in RT train. In FLAN. **AVOID.**

**stanfordnlp/imdb** (`e6281661…`; 25k / 25k / 50k unlabeled). IMDb non-commercial terms. Long (median 173 words). DeB trained on it; GLi benchmark-exposed. **AVOID.**

**fancyzhx/amazon_polarity** (`9d9c45c1…`; 3.6M / 400k). The card says Apache-2.0, but the upstream is SNAP Amazon reviews (unclear licence). **It is in GLiClass training** (declared) and in DeB.
**AVOID.**

**fancyzhx/yelp_polarity** (`bbf1c97a…`; 560k / 38k; card has no licence). Same Yelp terms as below. **AVOID.**

**mteb/tweet_sentiment_extraction** (`7261898e…`; 26,732 / 3,432). Kaggle competition data. It is the GLiClass pre-training source (`SetFit/tweet_sentiment_extraction`). **AVOID.**

### Ordinal / Score-track candidates (Jev Score supports 2-10 levels)

**stanfordnlp/sst (SST-5, sentence level)**. Main is script-based and **fails**. Works via
`load_dataset("stanfordnlp/sst", revision="refs/convert/parquet", data_dir="default")` (parquet commit `8a7d55ee01d70b8ae53e0b3c66a83b2a6198c2a7`).
Without `data_dir` it crashes on the `ptb` schema. `SetFit/sst5` (`e51bdcd8…`) is an identical 5-bin copy (train 8,544 / val 1,101 / test 2,210, `text`, `label` 0-4, `label_text` very negative … very positive).
- Fields: `sentence`, `label` float in [0,1] (averaged from 3 crowd raters per phrase), `tokens`, `tree`. Sample: "a stirring , funny and finally transporting re-imagining of beauty and the beast…" → very positive.
- Licence: unknown/none. **C: unclear. R: build script.**
- Noise: bin edges are arbitrary. Drop items within ±0.02 of an edge from gold eval and keep the continuous value for soft scoring. Neutral is hard.
- Exposure: GLi benchmark-exposed (sst5). **71% of test sentences are in RT train**, so DeB non-`-c` has seen them with binary labels. 0% in GLi pretraining.
- **Role: eval-zero-shot Score (5 levels)**, the de-facto standard. Mark results "exposed" for DeB non-`-c`. Never train on SST or RT.

**cardiffnlp/super_tweeteval `tweet_sentiment`**. Loads; sha `a10ac3d27a3499e870b6371df64c14e5a656131a`. train 26,632 / val 4,000 / test 12,379.
Fields `text`, `target`, `gold_label` 0-4 (SemEval-2016/2017 Task 4C, 5-point, topic-based).
- Sample: "dear @Microsoft the newOoffice for Mac is great and all, but no Lync update? C'mon." (target @microsoft) → 1.
- Licence: card `unknown`. The source licence is CC BY 3.0 plus Twitter ToS. **C: labels yes-ish. R: IDs plus build script.**
- Noise: crowd labels. Few items at the extremes (177 and 131 in test). 35.5% of test is shared with TweetEval sentiment test.
- Exposure: test clean. Train is 3.5-5.6% in GLi pretraining. Not in DeB.
- **Role: eval-zero-shot Score (5 levels, target-conditioned).** It tests literal reading (sentiment *toward the target*, not overall). Stratify so extremes are included.

**cardiffnlp/super_tweeteval `tweet_intimacy`** (1,191 / 396 / 396; `gold_score` float 1-5, averaged). Subjective construct, tiny. Optional Score extra. **Low priority.**

**Yelp/yelp_review_full**. Loads; sha `c1f9ee939b7d05667af864ee1cb066393154bf85`. train 650,000 / test 50,000. `label` ClassLabel(5) "1 star" … "5 stars" (balanced), `text`.
Median 100 words (p95 369).
- Licence: **Yelp Dataset Agreement**: non-commercial and academic, no redistribution. **C: no. R: no.**
- Noise: author star rating. Adjacent classes (2 vs 3, 4 vs 5) overlap a lot. 0.06% test-in-train.
- Exposure: DeB trained on yelp polarity. 0% in GLi pretraining. P3 includes yelp.
- **Role: optional eval-only Score** (the most-cited 5-star benchmark), as a build script and only if the team accepts non-commercial research evaluation.
  Pick short reviews (≤150 words) for CPU and token budget. Otherwise **AVOID**.

**SetFit/amazon_reviews_multi_en** (`ec73b665…`; 200,000 / 5,000 / 5,000; label 0-4, balanced). Card says apache-2.0, but **upstream MARC was withdrawn by Amazon**
(`defunct-datasets/amazon_reviews_multi` has its viewer disabled, and its script fails like `mteb/amazon_reviews_multi` main). **AVOID** (licence cannot be established).

**McAuley-Lab/Amazon-Reviews-2023**: script-based, fails, no parquet conversion, no licence. **AVOID.**

**sealuzh/app_reviews**. Loads on main (parquet ref `93e42cdc…` also works); sha `9eaa95f66364367e8752b0f34c00f67aafa95d15`. train only, 288,065 rows.
Fields `package_name`, `review`, `date`, `star` (1-5; skewed: 5 → 52%, 1 → 19%).
- Licence: card "More Information Needed". **C: unclear.** About 9% duplicate texts ("Good app"). DeB trained on it (appreviews). In BTZSC. **AVOID.**

**UCI Drug Review (Drugs.com)**, via mirror `lewtun/drug-reviews` (sha `07722f82287d0a94ddc80151390f34e65183b2c3`, loads, no card).
- Splits: train 161,297 / test 53,766. Fields `drugName`, `condition` (885 values; Birth Control 28,788, Depression 9,069, Pain, Anxiety, Acne…), `review`, `rating` (1-10 float), `date`, `usefulCount`. Median 84 words.
- Sample: drug Valsartan, condition "Left Ventricular Dysfunction", review "It has no side effect, I take it in combination of Bystolic 5 Mg and Fish Oil", rating 9.
- Licence: **CC BY 4.0** (UCI repository, DOI 10.24432/C5SK5S; Gräßer, Kallumadi et al. 2018). **C: yes** (attribution). **R: yes**. The mirror has no card, so cite UCI.
- Noise: patient self-rating (human, but no inter-rater agreement). HTML entities (`&#039;`). **66.6% of test texts duplicate train texts**, and the train set is only 70% unique.
  Condition strings include junk such as "3</span> users found this comment helpful.".
- Exposure: 0% in GLi pretraining. Not in DeB. Not in benchmark lists.
- **Role: TRAIN + eval-in-domain for Score with 10 levels.** It is the only 10-level human scale found, and it tests Jev's maximum level count.
  Apply deterministic re-binning to 5 levels ({1-2}, {3-4}, {5-6}, {7-8}, {9-10}) plus Noul("rating ≥ 7"). Group-split by normalized review text.
  It is medical content, so keep only the rating and condition questions (no advice).

**Women's E-Commerce Clothing Reviews** (Kaggle `nicapotato/womens-ecommerce-clothing-reviews`, **CC0**), via mirror `saattrupdan/womens-clothing-ecommerce-reviews`
(sha `4e788183125a6143d8bdba24e58f1efda2e4b48f`, loads, no licence field).
- Splits: train 20,641 / val 1,000 / test 1,000. Fields `review_text`, `age`, `rating` (1-5), `positive_feedback_count`, `division_name`, `department_name`
  (Tops 9,134, Dresses 5,630, Bottoms 3,355, Intimate 1,497, Jackets 913, Trend 112), `class_name` (20), `recommended_ind` ClassLabel(0/1). Median 59 words.
- Sample: "I loved this shirt until the first time i washed it. it shrunk so much it became unwearable…" → rating 1, not recommended, Tops/Knits.
- Licence: **CC0** at the Kaggle source (retailer name anonymized). **C: yes. R: yes.**
- Noise: author labels. 1.3% rating/recommend contradictions (2.4). The department is catalogue metadata, not always inferable from the text. Use department Choice only when the text mentions a garment.
- Exposure: 0% in GLi pretraining. Not in DeB. Not in benchmarks.
- **Role: TRAIN + eval-in-domain.** It has **three human labels per state** (Score 1-5, Noul recommend, Choice department), so it supports multi-question bundles
  and a cross-type consistency test (Score P(≥4) vs Noul recommend), with a measured human floor.

**jniimi/tripadvisor-review-rating**. Loads; sha `1a1b7077…`. 201,295 rows, train only. `title`, `text`, `overall` plus 5 aspect ratings
(cleanliness, value, location, rooms, sleep_quality), 1-5. Median 117 words.
- Licence: the uploader claims Apache-2.0, but the source is Li et al. / Wang et al. TripAdvisor research data ("follow the policy of the original data source").
  **C: unclear. R: build script.**
- 0% in GLi pretraining. Not in DeB.
- **Role: optional eval-zero-shot Score** with 6 Score questions per state (cheap per Jev call, and it tests aspect-literal reading). Needs short-review filtering.

**argilla/tripadvisor-hotel-reviews** (`f57199dd…`; 20,491). CC BY-NC 4.0 (the Kaggle Alam et al. set). The text is lowercased and stop-word-stripped.
The star rating is stored in Argilla's `prediction` field (`[{'label': '4', 'score': 1.0}]`, agent "Argilla"), and `annotation` is empty. **AVOID** (NC licence, altered text).

**TheFinAI/fiqa-sentiment-classification** (`b669064c…`; 822 / 117 / 234; `sentence`, `target`, `aspect`, continuous `score` −1..1). MIT per the mirror, but the upstream
FiQA-2018 licence is unclear. Tiny, with 5 duplicate texts in test. Optional Score extra. **Low priority.**

---

## 4. How each recommended source becomes questions (deterministic rules)

All variants of one base item share a `group_id`. The templates below are **examples of relation types**. Freely worded train templates and eval templates
must come from disjoint template pools, and the model is never told two questions are related.

| Source | Base questions | Consistency relations with deterministic gold |
|---|---|---|
| DBpedia | Choice(14 classes); Noul("Is this about a {class}?"); Noul(super-class) | Negation: Noul("…not a {class}…") = ¬gold. Choice↔Noul: P_choice(c) vs P_noul(c). Hierarchy: P(super) = Σ member probs. Double negation. |
| GoEmotions | Noul per emotion (gold = majority; soft target = vote fraction); Choice(Ekman 7) on single-majority items | Same-emotion negation; paraphrase; Choice(Ekman) vs Noul(Ekman). Do not add complements across emotions (multi-label). |
| Clothing | Score(1-5 satisfaction); Noul(recommend); Noul(≥4 stars); Choice(department) | Score reversal (dissatisfaction scale: level' = 6 − level); P_score(≥4) vs Noul(≥4); recommend vs rating (human floor 1.3%). |
| Drug | Score(1-10); Score(5 re-binned); Noul(rating ≥7) | 10↔5 re-binning (sum of adjacent levels); threshold Noul vs Score tail mass; scale reversal. |
| SST-5 | Score(1-5); Noul(positive = levels 4-5); Noul(negative = levels 1-2) | Positive and negative are **not** complements (neutral exists). Scale reversal; Score vs Noul tail mass. |
| SuperTweetEval sentiment | Score(1-5 toward {target}) | Scale reversal; target swap as a distractor (another entity named in the state). |
| FPB | Choice(3); Score(3, neg<neu<pos); Noul("good news for investors?") | Choice vs Score vs Noul agreement; negation. Agreement tier = per-item human certainty. |
| TFNS | Choice(bearish/bullish/neutral); Noul(bullish); Noul(bearish) | Non-complement trap; negation of each. |
| tweet_topic_single | Choice(6); Noul(topic) | Choice↔Noul; negation. |
| BTZSC agnews/emotiondair | **Exactly** the audit's Choice (same instruction and hypothesis strings) | Extra Noul and negation questions bundled in the same call. Also re-send the Choice alone on 30 states as a bundling-invariance control. |

---

## 5. Suggested sizing for this family (inside the global budgets)

Train (≤25k question rows overall; this family should take about 8-10k):
- DBpedia about 900 states (about 65 per class, ambiguous classes oversampled) × about 3 questions ≈ 2.7k rows
- GoEmotions about 900 states (single-majority Ekman items, balanced) × about 3 ≈ 2.7k
- Clothing about 700 states (stratified by rating, all rating-3 items kept) × about 4 ≈ 2.8k
- Drug about 500 states (stratified 1-10, group-deduplicated) × about 3 ≈ 1.5k

Eval (≤1,500 Jev calls and ≤5k question rows overall; this family should take about 550-650 calls, one call per state, several questions per call):
- Comparability: BTZSC agnews 100 + emotiondair 100 (200 calls; plus 30 invariance re-sends)
- In-domain: DBpedia 50, GoEmotions 60, clothing 60, drug 50 (220 calls)
- Zero-shot: SST-5 60, SuperTweetEval sentiment 50, FPB (AllAgree/75Agree) 50, TFNS 50, tweet_topic_single 50 (260 calls)
- Robustness variants (distractor/injection) reuse these base states and each costs one extra call per variant. Budget them in the global plan.

Power notes. At n=100 per slice, the 95% CI on accuracy is about ±10 pp near 50% and ±8 pp at 80%. At n=50 it is about ±14 pp. So claims at slice level
need n ≥ 100, and the rest should be pooled by track. Consistency gaps such as |P(A) + P(¬A) − 1| have per-item SD of about 0.1-0.2, so n=200 pairs gives CIs of about ±0.02.
Certifying coverage at ≤1% error needs about 300 or more accepted decisions with zero errors (rule of three). Pool Noul decisions across the family
(about 600 states × 3-4 Noul ≈ 2k decisions), choose thresholds on a validation half, and report on the other half, as AbdelStark's protocol recommends.
Use a paired, stratified bootstrap (2,000 resamples) with `group_id` as the resampling unit.

CPU and tokens: prefer states of ≤150 words. The recommended sources have medians of 12-84 words. Leave IMDB, Yelp, 20NG and TripAdvisor long tails
out of the default eval.

---

## 6. Loader recipes that worked (datasets 4.8.5)

```python
from datasets import load_dataset
from huggingface_hub import hf_hub_download
# plain parquet repos (pin the sha)
load_dataset("fancyzhx/dbpedia_14", revision="9abd46cf7fc8b4c64290f26993c540b92aa145ac")
load_dataset("google-research-datasets/go_emotions", "raw", revision="add492243ff905527e67aeb8b80c082af02207c3")
load_dataset("saattrupdan/womens-clothing-ecommerce-reviews", revision="4e788183125a6143d8bdba24e58f1efda2e4b48f")
load_dataset("lewtun/drug-reviews", revision="07722f82287d0a94ddc80151390f34e65183b2c3")
load_dataset("zeroshot/twitter-financial-news-sentiment", revision="ccbe24de388e287beb92dd393a335c376b350ac3")
load_dataset("cardiffnlp/super_tweeteval", "tweet_sentiment", revision="a10ac3d27a3499e870b6371df64c14e5a656131a")
load_dataset("btzsc/btzsc", name="agnews", split="test", revision="fef2a2ac62b69c58670047dddf045c53d7c3cb5e")
# script-based repos -> parquet conversion ref (pin the ref commit in the manifest)
load_dataset("stanfordnlp/sst", revision="refs/convert/parquet", data_dir="default")          # commit 8a7d55ee…
load_dataset("cardiffnlp/tweet_topic_single", revision="refs/convert/parquet",
             data_files={"train": "tweet_topic_single/train_2020/*.parquet",
                         "test": "tweet_topic_single/test_2021/*.parquet"})                    # commit 258efb7f…
# Financial PhraseBank: no parquet ref; use the original zip (keeps agreement tiers + License.txt)
hf_hub_download("takala/financial_phrasebank", "data/FinancialPhraseBank-v1.0.zip", repo_type="dataset",
                revision="8d3fe0c36d5feec6b3cc5e455b0fcb4820fb9964")
```
Failed under datasets 4.x: `takala/financial_phrasebank` (script, no parquet ref), `stanfordnlp/sst` main, `cardiffnlp/tweet_topic_single` main,
`mteb/amazon_reviews_multi` (script; its parquet ref only has `default`), `defunct-datasets/amazon_reviews_multi`, `McAuley-Lab/Amazon-Reviews-2023`.

---

## 7. Open items and risks
- Confirm by email or issue that `knowledgator/gliclass-v2.0` is the v3 pre-training corpus. Also hash the amazon_polarity and FineFineWeb pattern stream if it is released.
- TFNS label provenance is undocumented. Hand-audit about 100 items (two annotators) before counting it as gold, or tag it "silver".
- Decide as a team whether non-commercial or unclear sets (FPB, SST, Yelp, tweets, AG/DAIR comparability) are acceptable for *evaluation only*,
  distributed as a build script. The recommendation above assumes yes, with per-row `licence` and `commercial_ok=false` flags.
- Drug-review conditions include junk strings. Whitelist the top ~30 conditions for Choice questions.
- Clothing department is metadata. Filter to texts containing a garment keyword before asking department Choice, or drop that question from eval.
- DAIR Emotion: report it only in the comparability table with a "machine-generated labels" footnote.
