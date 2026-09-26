"""v0.11 TASK BANK: label-set breadth from hundreds of classification tasks (FREEZE.md block 1).

Two modes (deterministic, seed 20261001, CPU only, no LLM calls):

  inventory  Load the task sources, filter them, sample texts, split BY TASK GROUP (85% train / 15% dev), and write
               data/v11_parts/taskbank_inventory.json   list of tasks (labels, examples, split, def_slice, ...)
               data/v11_parts/taskbank_rows_raw.jsonl   the sampled items as plain choice rows, no cards yet
               data/v11_parts/taskbank_inventory_summary.json
  assemble   Read definition files data/v11_parts/defs/*.json and build the training/dev rows:
               data/v11_parts/taskbank_train.jsonl (~18,000), taskbank_dev.jsonl (~1,200), taskbank_relations.jsonl,
               data/v11_parts/taskbank_summary.json

  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python build_v11_taskbank.py inventory
  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python build_v11_taskbank.py assemble [--defs DIR] [--out DIR]

SOURCES
  1. MoritzLaurer/synthetic_zeroshot_mixtral_v0.1 (Apache-2.0), configs mixtral_written_texts_for_tasks (v1..v4):
     Mixtral-written texts for 543 invented tasks, each with a list of class statements (task_hypotheses). Every text
     appears as NLI pairs; labels == 0 is ENTAILMENT (the text's true class), labels == 1 is not-entailment. (Checked by
     hand: reading labels == 1 as the gold gives mostly wrong classes.) One task = one task_description. Labels are the
     class STATEMENTS ("The text describes ..."), so the definition files should give each one a short name.
     Not used: mixtral_refinedweb_categories / _characteristics (open-ended per-text multi-label topics, not tasks),
     mixtral_refinedweb_nli (NLI, not label sets).
  2. tasksource/zero-shot-label-nli (licence "other": the licence of each source dataset applies): 152 tasksource
     classification tasks recast as "This example is <label>." NLI pairs (labels 0 = entailment = gold). Regrouped here
     into per-task label sets; only the tasks in ZSL_SPECS are kept (every other 3-120-label task is in ZSL_DROP with the
     reason; 2-label tasks and discovery (174 labels) fall outside 3-120).

FILTERS
  * 3-120 labels per task (after dropping unusable labels such as IEMOCAP "xxx").
  * Drop a text whose label conflicts inside its task, a text shared by two split groups (it stays in the first), texts
    under the per-task minimum length or over 320 words.
  * Decontamination: drop any text sharing a 12-word run (or, under 12 words, equal to a whole line) with any state in
    lean/data/**/*.jsonl, EXCEPT OHS-1 files (data/ohs*.jsonl, data/ohs_parts/), which are never opened, and this
    script's own outputs. That covers every train, dev and eval file and data/v11_parts/dev_nc.jsonl (the v0.11 gate).
    JevBench (jev/bench) is never read here; run decontam.py on the assembled files if that check is wanted.
  * At most 150 texts per task, balanced (round-robin over labels, no label over 40%); tasks that cannot reach 30
    balanced texts are dropped.

SPLIT
  By task group, 85% train / 15% dev, stratified by source and label-set width (3 / 4 / 5-12 / 13+). Groups: Mixtral tasks linked by a shared class statement or
  TF-IDF cosine >= 0.5 between (description + statements) are one group (near-duplicate tasks never straddle the
  split); label-nli tasks that share texts or label inventories (MELD e/s, DailyDialog da/e, DynaSent r1/r2, the five
  lexical-relation sets, Switchboard/MRDA dialogue acts) are grouped.

DEFINITION FILES (assemble input): data/v11_parts/defs/*.json, each {task_id: {label: definition}} where label is the
  inventory label string. A value may also be {"name": "<short option name>", "definition": "<one line>"} to rename the
  option (needed for Mixtral statement labels, recommended for cryptic label-nli codes). An optional per-task key
  "_instruction" overrides the task question.

ASSEMBLE
  Choice rows over the task's FULL label set (gold position cycled over all positions within each task, other options
  shuffled), balanced yes/no bundles (aff + neg [+ para or dneg], 3-5 wordings per role; complement / equiv relations,
  track "train" / "dev"), the card on 100% of rows (choice: every option; yes/no: the asked label, the gold label and
  random others, up to 6 lines), and in ~30% of units (drawn per task, separately for choice and yes/no units) the
  labels renamed to opaque codes ("Class Q", "Code 17", "Option K", ...; consistent inside the row or bundle) with the
  definitions kept (meta.renamed = true, meta.label_map = shown -> canonical label). Items enter a task's rows
  round-robin over gold labels, so choice rows and yes/no units are label-balanced per task. Mixtral task questions are
  the description's first sentence with its class enumerations removed (task_question). Asserted before writing: card
  lines carry the definition of the code/name they show, label_map is a bijection onto the task labels, gold matches the
  raw item, one unit per text with one set of shown names, relation pairs share group/card/codes, no text in both
  splits. Reported (summary.definition_text_overlaps): any definition or name sharing an 8-word run with a text of its
  task.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import re
import sys
from array import array
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
from huggingface_hub import hf_hub_download

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
OUT_DIR = DATA / "v11_parts"
INV = OUT_DIR / "taskbank_inventory.json"
RAW = OUT_DIR / "taskbank_rows_raw.jsonl"
INV_SUMMARY = OUT_DIR / "taskbank_inventory_summary.json"
DEFS_DIR = OUT_DIR / "defs"
SEED = 20261001
MAX_PER_TASK = 150
CAP = 0.40
MIN_LABELS, MAX_LABELS = 3, 120
MIN_TASK_ROWS = 30
MAX_WORDS = 320
DEV_FRAC = 0.15
NGRAM = 12
SLICE = 60
TFIDF_LINK = 0.5
TRACK = "TB"

MIX_REPO = "MoritzLaurer/synthetic_zeroshot_mixtral_v0.1"
MIX_FILES = {
    "mixtral_written_texts_for_tasks": ["mixtral_written_texts_for_tasks/train-00000-of-00001.parquet"],
    "mixtral_written_texts_for_tasks_v2": ["mixtral_written_texts_for_tasks_v2/train-00000-of-00001.parquet"],
    "mixtral_written_texts_for_tasks_v3": [f"mixtral_written_texts_for_tasks_v3/train-0000{i}-of-00004.parquet" for i in range(4)],
    "mixtral_written_texts_for_tasks_v4": [f"mixtral_written_texts_for_tasks_v4/train-0000{i}-of-00002.parquet" for i in range(2)],
}
MIX_MIN_WORDS = 8
ZSL_REPO = "tasksource/zero-shot-label-nli"
ZSL_FILES = ["data/train-00000-of-00002-970172c89e89b5df.parquet", "data/train-00001-of-00002-509e762f01abeb95.parquet",
             "data/validation-00000-of-00001-79d9ba1d8f02bef0.parquet", "data/test-00000-of-00001-c260d1ee78ad6397.parquet"]

# forbidden datasets (hard rules) + our dev/eval sources + the dev_nc (BTZSC) source corpora
FORBIDDEN_PAT = re.compile(
    r"legalbench|cuad|maud|lex_?glue|ledgar|ecthr|scotus|eurlex|unfair|casehold|scone|not.a.dataset|hatecheck|pubmedqa|"
    r"vitaminc|goemotion|go_emotion|schema.guided|\bsgd\b|arxiv|tweet_eval|rotten|sms_spam|tfns|ag_?news|dair|emotion$|"
    r"enron|climatebert|\bcb\b|bbc|deysi|sst|imdb|btzsc|financial_phrasebank|empathetic|app_?reviews|social_bias|"
    r"trueteacher|manifesto|capsotu", re.I)

# every zero-shot-label-nli task with 3-120 labels that is NOT kept, and why
ZSL_DROP = {
    "ag_news": "our dev source (devzs)",
    "tweet_eval/emoji": "tweet_eval (dev/eval source)", "tweet_eval/emotion": "tweet_eval (dev/eval source)",
    "tweet_eval/sentiment": "tweet_eval (dev/eval source)", "tweet_eval/stance_abortion": "tweet_eval (dev/eval source)",
    "tweet_eval/stance_atheism": "tweet_eval (dev/eval source)", "tweet_eval/stance_climate": "tweet_eval (dev/eval source)",
    "tweet_eval/stance_feminist": "tweet_eval (dev/eval source)", "tweet_eval/stance_hillary": "tweet_eval (dev/eval source)",
    "vitaminc/tals--vitaminc": "forbidden (VitaminC, OHS-1 source)",
    "lex_glue/ledgar": "forbidden (LexGLUE/LEDGAR, OHS-1 source)", "lex_glue/scotus": "forbidden (LexGLUE)",
    "financial_phrasebank/sentences_allagree": "dev_nc gate source (BTZSC financialphrasebank)",
    "hate_speech18": "Stormfront posts (de Gibert 2018) are a Social Bias Frames source = dev_nc gate (biasframes)",
    "hate_speech_offensive": "Davidson tweets are a Social Bias Frames source = dev_nc gate (biasframes)",
    "banking77": "already trained (banking77)", "dbpedia_14/dbpedia_14": "already trained (dbpedia)",
    "yahoo_answers_topics": "already trained (yahoo)", "yelp_review_full/yelp_review_full": "already trained (yelp5)",
    "CONDAQA": "already trained (condaqa)",
    "blog_authorship_corpus/horoscope": "label not inferable from the text (author's star sign)",
    "blog_authorship_corpus/job": "label not inferable from the text (author's industry)",
    "TuringBench": "label not inferable from the text (which generator model)",
    "liar": "label depends on outside facts; near-chance even for trained models",
    "crowdflower/text_emotion": "very noisy crowd labels (13 overlapping tweet emotions)",
}


def _cc(s):  # CamelCase -> "camel case"
    return re.sub(r"(?<=[a-z])(?=[A-Z])", " ", s).lower()


LANGS = {"ar": "Arabic", "bg": "Bulgarian", "de": "German", "el": "Greek", "en": "English", "es": "Spanish", "fr": "French",
         "hi": "Hindi", "it": "Italian", "ja": "Japanese", "nl": "Dutch", "pl": "Polish", "pt": "Portuguese", "ru": "Russian",
         "sw": "Swahili", "th": "Thai", "tr": "Turkish", "ur": "Urdu", "vi": "Vietnamese", "zh": "Chinese"}
TREC = {"ABBR:abb": "abbreviation", "ABBR:exp": "expansion of an abbreviation", "DESC:def": "definition",
        "DESC:desc": "description", "DESC:manner": "manner", "DESC:reason": "reason", "ENTY:animal": "animal",
        "ENTY:body": "body part", "ENTY:color": "color", "ENTY:cremat": "creative work", "ENTY:currency": "currency",
        "ENTY:dismed": "disease or medicine", "ENTY:event": "event", "ENTY:food": "food", "ENTY:instru": "musical instrument",
        "ENTY:lang": "language", "ENTY:letter": "letter or character", "ENTY:other": "other entity", "ENTY:plant": "plant",
        "ENTY:product": "product", "ENTY:religion": "religion", "ENTY:sport": "sport", "ENTY:substance": "substance",
        "ENTY:symbol": "symbol or sign", "ENTY:techmeth": "technique or method", "ENTY:termeq": "equivalent term",
        "ENTY:veh": "vehicle", "ENTY:word": "word with a special property", "HUM:desc": "description of a person",
        "HUM:gr": "group or organization", "HUM:ind": "individual person", "HUM:title": "title of a person",
        "LOC:city": "city", "LOC:country": "country", "LOC:mount": "mountain", "LOC:other": "other location",
        "LOC:state": "state or province", "NUM:code": "code or number sequence", "NUM:count": "count",
        "NUM:date": "date", "NUM:dist": "distance", "NUM:money": "amount of money", "NUM:ord": "rank or position",
        "NUM:other": "other number", "NUM:perc": "percentage", "NUM:period": "time period", "NUM:speed": "speed",
        "NUM:temp": "temperature", "NUM:volsize": "size, area or volume", "NUM:weight": "weight"}

# kept label-nli tasks. wrap: ("one", header) | ("pair", h1, h2[, "last"]) | ("words",) | ("clutrr",) | ("humicro",)
ZSL_SPECS = {
    "EffectiveFeedbackStudentWriting": dict(
        name="Effectiveness of a student essay passage", wrap=("one", "Essay passage:"),
        instr="How effective is this passage from a student's argumentative essay?",
        domain="education; argumentative essays by US students in grades 6-12 (Feedback Prize)",
        labels={"Adequate": "adequate", "Effective": "effective", "Ineffective": "ineffective"}),
    "circa": dict(
        name="Interpreting indirect answers", wrap=("pair", "Situation and question:", "Reply:"),
        instr="How should the reply be interpreted as an answer to the question?",
        domain="dialogue; indirect answers to yes/no questions (Circa)", min_words=4),
    "citation_intent": dict(
        name="Citation function in NLP papers", wrap=("one", "Sentence from a paper:"),
        instr="Why does the author cite the work mentioned in this sentence?",
        domain="scientific writing; citation contexts from computational-linguistics papers (ACL-ARC)",
        labels={"Background": "background", "CompareOrContrast": "compare or contrast", "Extends": "extends",
                "Future": "future work", "Motivation": "motivation", "Uses": "uses"}),
    "crowdflower/airline-sentiment": dict(
        name="Airline tweet sentiment", wrap=("one", "Tweet to an airline:"),
        instr="What sentiment does this tweet express about the airline?",
        domain="customer-service tweets addressed to US airlines (CrowdFlower)"),
    "crowdflower/corporate-messaging": dict(
        name="Corporate message type", wrap=("one", "Company tweet:"),
        instr="What kind of corporate message is this tweet?",
        domain="tweets posted by large companies (CrowdFlower corporate messaging)",
        labels={"Action": "action", "Dialogue": "dialogue", "Exclude": "exclude", "Information": "information"}),
    "crowdflower/economic-news": dict(
        name="Relevance of news to the US economy", wrap=("one", "News article:"),
        instr="Is this news article relevant to the US economy?",
        domain="US news articles (CrowdFlower economic news relevance)",
        labels={"yes": "relevant", "no": "not relevant", "not sure": "not sure"}),
    "crowdflower/political-media-message": dict(
        name="Politician social media message type", wrap=("one", "Post by a US politician:"),
        instr="What is the main type of message in this post?",
        domain="social media posts by US politicians (CrowdFlower political media)"),
    "crowdflower/sentiment_nuclear_power": dict(
        name="Sentiment toward nuclear power", wrap=("one", "Tweet:"),
        instr="What is this tweet's attitude toward nuclear energy?",
        domain="tweets after the 2011 Fukushima accident (CrowdFlower)",
        labels={"Negative": "negative", "Neutral / author is just sharing information": "neutral",
                "Positive": "positive", "Tweet NOT related to nuclear energy": "not about nuclear energy"}),
    "dynasent/dynabench.dynasent.r1.all/r1": dict(
        name="Review sentence sentiment (DynaSent round 1)", wrap=("one", "Review sentence:"),
        instr="What sentiment does this sentence express?", group="dynasent",
        domain="sentences from business reviews, chosen to fool sentiment models (DynaSent)"),
    "dynasent/dynabench.dynasent.r2.all/r2": dict(
        name="Review sentence sentiment (DynaSent round 2)", wrap=("one", "Sentence:"),
        instr="What sentiment does this sentence express?", group="dynasent",
        domain="crowd-written adversarial review sentences (DynaSent round 2)"),
    "emo/emo2019": dict(
        name="Emotion in a short chat", wrap=("one", "Chat:"),
        instr="What emotion does the last speaker express in this short chat?",
        domain="3-turn text chats (SemEval-2019 EmoContext)", labels={"others": "other"}),
    "folio": dict(
        name="First-order logic entailment", wrap=("pair", "Premises:", "Conclusion:", "last"),
        instr="Given only the premises, is the conclusion true, false, or unknown?",
        domain="logic puzzles written by experts (FOLIO)",
        labels={"True": "true", "False": "false", "Unknown": "unknown"}),
    "health_fact": dict(
        name="Public-health claim rating", wrap=("one", "Claim:"),
        instr="How would a fact-checker rate this public-health claim?",
        domain="public-health claims rated by fact-checking sites (PUBHEALTH)"),
    "hope_edi/english": dict(
        name="Hope speech detection", wrap=("one", "Comment:"),
        instr="Is this comment hope speech?",
        domain="YouTube comments on equality, diversity and inclusion topics (HopeEDI)",
        labels={"Hope_speech": "hope speech", "Non_hope_speech": "not hope speech", "not-English": "not English"}),
    "humicroedit/subtask-2": dict(
        name="Funnier edited headline", wrap=("humicro",),
        instr="Each headline had one word replaced to make it funny. Which edited headline is funnier?",
        domain="news headlines with one-word humorous edits (Humicroedit / SemEval-2020 task 7)",
        labels={"sentence1": "headline A", "sentence2": "headline B", "equal": "equally funny"}),
    "implicit-hate-stg1": dict(
        name="Explicit vs implicit hate", wrap=("one", "Post:"),
        instr="Is this post hateful, and if so, is the hate explicit or implicit?",
        domain="tweets from extremist-adjacent accounts (Implicit Hate corpus)",
        labels={"explicit_hate": "explicit hate", "implicit_hate": "implicit hate", "not_hate": "not hate"}),
    "language-identification": dict(
        name="Language identification", wrap=("one", "Text:"), min_words=1,
        instr="What language is this text written in?", domain="short texts in 20 languages (papluca language identification)",
        labels=LANGS),
    "lexical_relation_classification/BLESS": dict(
        name="Word-pair relation (BLESS)", wrap=("words",), min_words=1, group="lexrel",
        instr="How is the second word related to the first word?", domain="lexical semantics; concrete nouns (BLESS)",
        labels={"attri": "attribute", "coord": "co-hyponym", "event": "event", "hyper": "hypernym", "mero": "meronym",
                "random": "unrelated"}),
    "lexical_relation_classification/CogALexV": dict(
        name="Word-pair relation (CogALex-V)", wrap=("words",), min_words=1, group="lexrel",
        instr="How is the second word related to the first word?", domain="lexical semantics (CogALex-V shared task)",
        labels={"ANT": "antonym", "HYPER": "hypernym", "PART_OF": "part of", "RANDOM": "unrelated", "SYN": "synonym"}),
    "lexical_relation_classification/EVALution": dict(
        name="Word-pair relation (EVALution)", wrap=("words",), min_words=1, group="lexrel",
        instr="How is the second word related to the first word?", domain="lexical semantics (EVALution)",
        labels={"Antonym": "antonym", "HasA": "has a", "HasProperty": "has property", "IsA": "is a", "MadeOf": "made of",
                "PartOf": "part of", "Synonym": "synonym"}),
    "lexical_relation_classification/K&H+N": dict(
        name="Word-pair relation (K&H+N)", wrap=("words",), min_words=1, group="lexrel",
        instr="How is the second word related to the first word?", domain="lexical semantics; taxonomy terms (K&H+N)",
        labels={"false": "unrelated", "hypo": "hyponym", "mero": "meronym", "sibl": "sibling"}),
    "lexical_relation_classification/ROOT09": dict(
        name="Word-pair relation (ROOT09)", wrap=("words",), min_words=1, group="lexrel",
        instr="How is the second word related to the first word?", domain="lexical semantics (ROOT09)",
        labels={"COORD": "co-hyponym", "HYPER": "hypernym", "RANDOM": "unrelated"}),
    "logical-fallacy": dict(
        name="Logical fallacy type", wrap=("one", "Argument:"), instr="Which logical fallacy does this argument commit?",
        domain="short arguments from educational sites (Logic / logical-fallacy dataset)"),
    "numer_sense": dict(
        name="Numerical commonsense", wrap=("one", "Sentence:"), instr="Which number word best fills the <mask> slot?",
        domain="commonsense statements with a masked number (NumerSense)"),
    "open_question_type": dict(
        name="Open question type", wrap=("one", "Question:"), instr="What type of question is this?",
        domain="open-ended questions from forums (open question type classification)"),
    "poem_sentiment": dict(
        name="Poem line sentiment", wrap=("one", "Line of poetry:"), instr="What sentiment does this line of poetry convey?",
        domain="single verses from Project Gutenberg poems (poem_sentiment)", labels={"no_impact": "no impact"}),
    "pragmeval/emergent": dict(
        name="Headline stance toward a claim", wrap=("pair", "Claim:", "Headline:"),
        instr="What stance does the headline take toward the claim?", domain="rumour claims and news headlines (Emergent)",
        labels={"for": "for", "against": "against", "observing": "observing"}),
    "pragmeval/gum": dict(
        name="Discourse relation (GUM)", wrap=("pair", "Segment 1:", "Segment 2:"),
        instr="What discourse relation holds between the two segments?", domain="RST relations in varied genres (GUM corpus)",
        labels={"no_relation": "no relation"}),
    "pragmeval/mrda": dict(
        name="Meeting dialogue act (MRDA)", wrap=("one", "Utterance from a meeting:"), group="swbd_mrda",
        instr="What dialogue act does this utterance perform?", domain="research-group meeting transcripts (ICSI MRDA)"),
    "pragmeval/pdtb": dict(
        name="Discourse relation (PDTB)", wrap=("pair", "Argument 1:", "Argument 2:"),
        instr="What discourse relation links the two text spans?", domain="Wall Street Journal text (Penn Discourse Treebank)"),
    "pragmeval/stac": dict(
        name="Discourse relation in game chat (STAC)", wrap=("pair", "Message 1:", "Message 2:"),
        instr="What discourse relation links the second chat message to the first?",
        domain="chat from online Settlers of Catan games (STAC)",
        labels={"Clarification_question": "clarification question", "Q_Elab": "question elaboration",
                "Question_answer_pair": "question-answer pair", "no_relation": "no relation"}),
    "pragmeval/switchboard": dict(
        name="Telephone dialogue act (Switchboard)", wrap=("one", "Utterance from a phone call:"), group="swbd_mrda",
        instr="What dialogue act does this utterance perform?", domain="telephone conversations (Switchboard SWDA)"),
    "pragmeval/verifiability": dict(
        name="Proposition verifiability", wrap=("one", "Comment on a proposed regulation:"),
        instr="What kind of proposition is this, in terms of how it could be verified?",
        domain="public comments on US government rulemaking (Park & Cardie verifiability)"),
    "rumoureval_2019/RumourEval2019": dict(
        name="Reply stance toward a rumour", wrap=("pair", "Source post:", "Reply:"),
        instr="What stance does the reply take toward the rumour in the source post?",
        domain="Twitter and Reddit rumour threads (RumourEval 2019)"),
    "scicite": dict(
        name="Citation intent (SciCite)", wrap=("one", "Citation sentence:"),
        instr="Why is the cited work mentioned in this sentence?", domain="scientific papers, mostly biomedical (SciCite)",
        labels={"background": "background", "method": "method", "result": "result"}),
    "scientific-exaggeration-detection": dict(
        name="Press release exaggeration", wrap=("pair", "Press release:", "Paper abstract:"),
        instr="Compared with the paper's finding, how does the press release state it?",
        domain="health-science press releases and paper abstracts",
        labels={"downplays": "downplays", "exaggerates": "exaggerates", "same": "same strength"}),
    "sciie": dict(
        name="Scientific relation between marked spans", wrap=("one", "Sentence:"),
        instr="What relation holds between the span in [[ ]] and the span in << >>?",
        domain="computer-science abstracts (SciERC)",
        labels={"COMPARE": "compare", "CONJUNCTION": "conjunction", "EVALUATE-FOR": "evaluate for", "FEATURE-OF": "feature of",
                "HYPONYM-OF": "hyponym of", "PART-OF": "part of", "USED-FOR": "used for"}),
    "sem_eval_2010_task_8": dict(
        name="Semantic relation between nominals", wrap=("one", "Sentence:"),
        instr="What semantic relation holds between the entities marked <e1> and <e2>?",
        domain="web sentences (SemEval-2010 task 8)"),
    "silicone/dyda_da": dict(
        name="Dialogue act (DailyDialog)", wrap=("one", "Utterance:"), group="dyda",
        instr="What dialogue act does this utterance perform?", domain="everyday English conversations (DailyDialog)"),
    "silicone/dyda_e": dict(
        name="Utterance emotion (DailyDialog)", wrap=("one", "Utterance:"), group="dyda",
        instr="What emotion does this utterance express?", domain="everyday English conversations (DailyDialog)"),
    "silicone/iemocap": dict(
        name="Utterance emotion (IEMOCAP)", wrap=("one", "Utterance:"), drop_labels=["xxx"],
        instr="What emotion does the speaker express?", domain="acted dyadic conversations (IEMOCAP transcripts)",
        labels={"ang": "anger", "dis": "disgust", "exc": "excitement", "fea": "fear", "fru": "frustration", "hap": "happiness",
                "neu": "neutral", "oth": "other", "sad": "sadness", "sur": "surprise"}),
    "silicone/maptask": dict(
        name="Map Task dialogue move", wrap=("one", "Utterance from a map-navigation dialogue:"),
        instr="What move does this utterance make in the dialogue?", domain="task-oriented route-giving dialogues (HCRC Map Task)",
        labels={"query_w": "wh-question", "query_yn": "yes-no question", "reply_n": "no reply", "reply_w": "wh-reply",
                "reply_y": "yes reply"}),
    "silicone/meld_e": dict(
        name="TV dialogue emotion (MELD)", wrap=("one", "Line from a TV-series dialogue:"), group="meld",
        instr="What emotion does the speaker express?", domain="dialogue from the TV series Friends (MELD)"),
    "silicone/meld_s": dict(
        name="TV dialogue sentiment (MELD)", wrap=("one", "Line from a TV-series dialogue:"), group="meld",
        instr="What sentiment does the speaker express?", domain="dialogue from the TV series Friends (MELD)"),
    "silicone/oasis": dict(
        name="Customer-service dialogue act (Oasis)", wrap=("one", "Utterance from a customer-service call:"),
        instr="What dialogue act does this utterance perform?",
        domain="British Telecom customer-service calls (Oasis BT); label names are terse codes, rename them"),
    "silicone/sem": dict(
        name="Conversation sentiment (SEMAINE)", wrap=("one", "Utterance:"),
        instr="What sentiment does the speaker express?", domain="conversations with emotionally coloured agents (SEMAINE)",
        labels={"Negative": "negative", "Neutral": "neutral", "Positive": "positive"}),
    "snips_built_in_intents": dict(
        name="Voice assistant intent (SNIPS)", wrap=("one", "Request to a voice assistant:"),
        instr="What does the user want the assistant to do?", domain="voice-assistant requests (SNIPS built-in intents)",
        labels="camel"),
    "spartqa-yn": dict(
        name="Spatial reasoning question", wrap=("pair", "Scene:", "Question:", "last"),
        instr="Based on the scene description, what is the answer to the question?",
        domain="synthetic block-world scene descriptions (SpartQA)",
        labels={"Yes": "yes", "No": "no", "DK": "cannot be determined"}),
    "trec": dict(
        name="Question answer type (TREC)", wrap=("one", "Question:"),
        instr="What type of answer is this question asking for?", domain="factoid questions (TREC question classification)",
        labels=TREC),
    "v1/gen_train234_test2to10": dict(
        name="Kinship reasoning (CLUTRR)", wrap=("clutrr",),
        instr="Which kinship term fills the blank in the query?", domain="short synthetic family stories (CLUTRR)"),
}

GENERIC_CHOICE = [
    "Which label best fits this text?",
    "Using the definitions provided, which category does this text belong to?",
    "Pick the one label that applies to this text.",
    "Which of the defined classes is the correct one for this text?",
    "According to the label definitions, how should this text be classified?",
]
AFF = ["Is '{L}' the correct label for this text?", "Should this text be labeled '{L}'?",
       "Does this text belong to the class '{L}'?", "Based on the definitions, does '{L}' apply to this text?",
       "Would you classify this text as '{L}'?"]
NEG = ["Is '{L}' the wrong label for this text?", "Should the label '{L}' be rejected for this text?",
       "Does this text fall outside the class '{L}'?", "Is it false that this text should be labeled '{L}'?"]
DNEG = ["Is it false that '{L}' is the wrong label for this text?",
        "Would it be a mistake to reject the label '{L}' for this text?",
        "Is it untrue that this text does not belong to the class '{L}'?"]
PARA = ["Going by the definitions, is this text an instance of '{L}'?", "Does the definition of '{L}' describe this text?",
        "Can this text be correctly assigned to '{L}'?", "Is this text a case of '{L}'?"]
YN_NOTE = "Each text has exactly one correct label."


# ------------------------------------------------------------------ helpers
def rng(*parts) -> random.Random:
    h = hashlib.sha256(":".join([str(SEED), *map(str, parts)]).encode()).hexdigest()
    return random.Random(int(h[:16], 16))


def sid(*parts) -> str:
    return hashlib.sha1("|".join(map(str, parts)).encode()).hexdigest()[:12]


def words(t: str) -> list[str]:
    return re.findall(r"\w+", str(t).lower())


def norm(t: str) -> str:
    return " ".join(words(t))


def short(t: str, n: int = 300) -> str:
    t = re.sub(r"\s+", " ", t).strip()
    return t if len(t) <= n else t[: n - 1].rstrip() + "\u2026"


# ------------------------------------------------------------------ n-gram hashing (stable, vectorised)
_P = np.uint64(0x9E3779B97F4A7C15)
_POW = np.array([pow(0x9E3779B97F4A7C15, NGRAM - 1 - k, 2 ** 64) for k in range(NGRAM)], dtype=np.uint64)
_WID: dict[str, int] = {}


def _wid(w: str) -> int:
    v = _WID.get(w)
    if v is None:
        v = int.from_bytes(hashlib.blake2b(w.encode(), digest_size=8).digest(), "little")
        _WID[w] = v
    return v


def gram_hashes(ws: list[str]) -> np.ndarray:
    if len(ws) < NGRAM:
        return np.zeros(0, dtype=np.uint64)
    ids = np.fromiter((_wid(w) for w in ws), dtype=np.uint64, count=len(ws))
    win = np.lib.stride_tricks.sliding_window_view(ids, NGRAM)
    with np.errstate(over="ignore"):
        return (win * _POW).sum(axis=1, dtype=np.uint64)


def existing_index():
    """12-gram hashes and short normalised lines of every state in lean/data, except OHS-1 files (never opened) and
    this script's outputs."""
    files = []
    for p in sorted(DATA.rglob("*.jsonl")):
        rel = p.relative_to(DATA)
        if rel.name.startswith("ohs") or (rel.parts and rel.parts[0].startswith("ohs")):
            continue
        if rel.parts[0] == "v11_parts" and rel.name.startswith("taskbank_"):
            continue
        files.append(p)
    buf, lines, seen, scanned = array("Q"), set(), set(), []
    for f in files:
        n = 0
        with open(f) as fh:
            for line in fh:
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                st = r.get("state") if isinstance(r, dict) else None
                if not isinstance(st, str):
                    continue
                n += 1
                h = hashlib.sha1(st.encode()).digest()
                if h in seen:
                    continue
                seen.add(h)
                ws = words(st)
                buf.extend(gram_hashes(ws).tolist())
                if len(ws) <= 40:
                    lines.add(" ".join(ws))
                for ln in st.split("\n"):
                    lw = words(ln)
                    if 0 < len(lw) <= 40:
                        lines.add(" ".join(lw))
        if n:
            scanned.append(str(f.relative_to(HERE)))
    grams = np.unique(np.frombuffer(buf, dtype=np.uint64)) if len(buf) else np.zeros(0, dtype=np.uint64)
    return grams, lines, scanned, len(seen)


def contaminated(texts: list[str], grams: np.ndarray, lines: set) -> np.ndarray:
    """Boolean mask over texts: shares a 12-gram with existing data, or (under 12 words) equals an existing line."""
    bad = np.zeros(len(texts), dtype=bool)
    hs, owner = [], []
    for i, t in enumerate(texts):
        ws = words(t)
        if len(ws) < NGRAM:
            bad[i] = " ".join(ws) in lines
            continue
        g = gram_hashes(ws)
        hs.append(g)
        owner.append(np.full(len(g), i, dtype=np.int64))
    if hs:
        H, O = np.concatenate(hs), np.concatenate(owner)
        hit = np.isin(H, grams)
        bad[np.unique(O[hit])] = True
    return bad


# ------------------------------------------------------------------ source loading
def load_mixtral():
    """-> dict task_description -> task dict with items [(text, gold_statement)]."""
    frames = []
    for cfg, files in MIX_FILES.items():
        for f in files:
            d = pd.read_parquet(hf_hub_download(MIX_REPO, f, repo_type="dataset"),
                                columns=["hypothesis", "text", "labels", "text_type", "profession", "task_description",
                                         "task_hypotheses"])
            d = d[d["labels"] == 0]  # 0 = entailment = the text's true class
            d = d.assign(cfg=cfg)
            frames.append(d)
    df = pd.concat(frames, ignore_index=True)
    tasks = {}
    for desc, g in df.groupby("task_description", sort=True):
        hyp_order = []
        for hl in g["task_hypotheses"]:
            for h in hl:
                if h not in hyp_order:
                    hyp_order.append(h)
        tasks[desc] = dict(
            desc=desc, labels=hyp_order,
            items=list(zip(g["text"].astype(str), g["hypothesis"].astype(str))),
            professions=Counter(g["profession"].astype(str)), text_types=Counter(g["text_type"].astype(str)),
            cfgs=sorted(set(g["cfg"])))
    return tasks, len(df)


def wrap_zsl(spec, premise: str):
    """premise -> (state, text used for decontam) or None when the premise cannot be parsed."""
    w = spec["wrap"]
    p = premise.replace("</br>", "\n").replace("\r", "")
    p = re.sub(r"\n{3,}", "\n\n", p).strip()
    if w[0] == "one":
        if spec.get("_flatten", True) and w[1] in ("Citation sentence:", "Sentence from a paper:"):
            p = re.sub(r"\s*\n\s*", " ", p)
        return f"{w[1]}\n{p}", p
    if w[0] == "pair":
        if "\n" not in p:
            return None
        a, b = (p.rsplit("\n", 1) if len(w) > 3 and w[3] == "last" else p.split("\n", 1))
        a, b = a.strip(), b.strip()
        if not a or not b:
            return None
        return f"{w[1]}\n{a}\n\n{w[2]}\n{b}", p
    if w[0] == "words":
        parts = [x.strip() for x in p.split("\n") if x.strip()]
        if len(parts) != 2:
            return None
        return f"First word: {parts[0]}\nSecond word: {parts[1]}", p
    if w[0] == "clutrr":
        m = re.match(r"(?s)(.*)\n\('([^']+)', '([^']+)'\)\s*$", p)
        if not m:
            return None
        story = re.sub(r"\[([^\]]+)\]", r"\1", m.group(1)).strip()
        a, b = m.group(2), m.group(3)
        return f"Story:\n{story}\n\nQuery: {b} is {a}'s ___.", p
    if w[0] == "humicro":
        heads = []
        for ln in p.split("\n"):
            ln = ln.strip()
            if ln.endswith(":"):
                ln = ln[:-1].rstrip()
            if " : " not in ln:
                return None
            head, repl = ln.rsplit(" : ", 1)
            if len(re.findall(r"<[^<>]+/>", head)) != 1 or not repl.strip():
                return None
            edited = re.sub(r"<[^<>]+/>", repl.strip(), head)
            edited = re.sub(r"\s+([,.;:!?'\u2019])", r"\1", edited)
            heads.append(re.sub(r"\s+(n't|n\u2019t)\b", r"\1", edited).strip())
        if len(heads) != 2:
            return None
        return f"Edited headline A:\n{heads[0]}\n\nEdited headline B:\n{heads[1]}", p
    raise ValueError(w)


def zsl_label_map(task, spec, raw_labels):
    lm = spec.get("labels") or {}
    out = {}
    for r in raw_labels:
        if lm == "camel":
            out[r] = _cc(r)
        elif r in lm:
            out[r] = lm[r]
        else:
            out[r] = r.replace("_", " ")
    assert len(set(out.values())) == len(out), (task, out)
    return out


def load_zsl():
    frames = []
    for f in ZSL_FILES:
        frames.append(pd.read_parquet(hf_hub_download(ZSL_REPO, f, repo_type="dataset")))
    df = pd.concat(frames, ignore_index=True)
    all_tasks = df.groupby("task")["hypothesis"].nunique()
    in_range = sorted(t for t, n in all_tasks.items() if MIN_LABELS <= n <= MAX_LABELS)
    missing = [t for t in in_range if t not in ZSL_SPECS and t not in ZSL_DROP]
    assert not missing, f"unreviewed label-nli tasks: {missing}"
    for t in ZSL_SPECS:
        assert t in all_tasks.index, t
        assert not FORBIDDEN_PAT.search(t), f"forbidden-looking task kept: {t}"
    df = df[df["task"].isin(set(ZSL_SPECS))]
    pre = "This example is "
    tasks = {}
    for task, g in df.groupby("task", sort=True):
        spec = ZSL_SPECS[task]
        raw_labels = sorted({h[len(pre):].rstrip(".") if h.startswith(pre) else h for h in g["hypothesis"]})
        raw_labels = [l for l in raw_labels if l not in set(spec.get("drop_labels", []))]
        lmap = zsl_label_map(task, spec, raw_labels)
        pos = g[g["labels"] == 0]
        items = []
        for prem, hyp in zip(pos["premise"].astype(str), pos["hypothesis"].astype(str)):
            lab = hyp[len(pre):].rstrip(".") if hyp.startswith(pre) else hyp
            if lab not in lmap:
                continue
            items.append((prem, lab))
        tasks[task] = dict(spec=spec, raw_labels=raw_labels, lmap=lmap, items=items, n_labels_all=int(all_tasks[task]))
    return tasks, {t: int(n) for t, n in all_tasks.items()}


# ------------------------------------------------------------------ sampling
def balanced_alloc(avail: dict, target: int = MAX_PER_TASK, cap: float = CAP):
    labs = sorted(avail)
    for n in range(min(target, sum(avail.values())), MIN_TASK_ROWS - 1, -1):
        cnt, tot = dict.fromkeys(labs, 0), 0
        while tot < n:
            moved = False
            for l in labs:
                if tot < n and cnt[l] < avail[l]:
                    cnt[l] += 1
                    tot += 1
                    moved = True
            if not moved:
                break
        if tot == n and max(cnt.values()) <= cap * n:
            return cnt
    return None


class UF:
    def __init__(self, n):
        self.p = list(range(n))

    def f(self, i):
        while self.p[i] != i:
            self.p[i] = self.p[self.p[i]]
            i = self.p[i]
        return i

    def u(self, a, b):
        a, b = self.f(a), self.f(b)
        if a != b:
            self.p[max(a, b)] = min(a, b)


def mixtral_groups(tasks: list[dict]) -> list[str]:
    from sklearn.feature_extraction.text import TfidfVectorizer
    n = len(tasks)
    uf = UF(n)
    by_h = defaultdict(list)
    for i, t in enumerate(tasks):
        for h in t["labels"]:
            by_h[h].append(i)
    for ids in by_h.values():
        for j in ids[1:]:
            uf.u(ids[0], j)
    docs = [t["desc"] + " " + " ".join(t["labels"]) for t in tasks]
    X = TfidfVectorizer(stop_words="english", sublinear_tf=True).fit_transform(docs)
    S = (X @ X.T).toarray()
    np.fill_diagonal(S, 0)
    for i, j in zip(*np.where(S >= TFIDF_LINK)):
        uf.u(int(i), int(j))
    return [f"mix_g{uf.f(i):04d}" for i in range(n)]


# ------------------------------------------------------------------ inventory mode
def inventory():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    skipped = Counter()
    mix, n_mix_rows = load_mixtral()
    zsl, zsl_all = load_zsl()

    # ---- unified task list
    T = []
    for desc, t in mix.items():
        k = len(t["labels"])
        if not (MIN_LABELS <= k <= MAX_LABELS):
            skipped[f"mixtral task with {k} labels (outside {MIN_LABELS}-{MAX_LABELS})"] += 1
            continue
        tid = "tbm_" + sid("mix", desc)[:8]
        prof = t["professions"].most_common(1)[0][0].replace("_", " ")
        tt = [x for x, _ in t["text_types"].most_common(3)]
        T.append(dict(task_id=tid, task_name=re.split(r"(?<=[.!?])\s", desc)[0][:160], source="mixtral",
                      desc=desc, labels=t["labels"], display=None, items=t["items"], min_words=MIX_MIN_WORDS,
                      domain_hint=f"{prof}; text types: {', '.join(tt)}", label_kind="statement",
                      hf=dict(hf_id=MIX_REPO, hf_configs=t["cfgs"]), wrap=None))
    for task, t in zsl.items():
        spec = t["spec"]
        k = len(t["raw_labels"])
        if not (MIN_LABELS <= k <= MAX_LABELS):
            skipped[f"label-nli {task}: {k} labels"] += 1
            continue
        tid = "tbz_" + re.sub(r"[^a-z0-9]+", "_", task.lower()).strip("_")[:40]
        T.append(dict(task_id=tid, task_name=spec["name"], source="label_nli", desc=spec["instr"],
                      labels=t["raw_labels"], display=t["lmap"], items=t["items"], min_words=spec.get("min_words", 3),
                      domain_hint=spec["domain"], label_kind="name", tasksource_task=task, spec=spec,
                      hf=dict(hf_id=ZSL_REPO, tasksource_task=task), wrap=spec["wrap"]))
    assert len({t["task_id"] for t in T}) == len(T)

    # ---- per-item state + filters
    for t in T:
        labset = set(t["labels"])
        by_text = defaultdict(set)
        states = {}
        for text, lab in t["items"]:
            if lab not in labset:
                skipped[f"{t['source']}: gold not in label set"] += 1
                continue
            if t["source"] == "mixtral":
                txt = re.sub(r"\n{3,}", "\n\n", text.replace("\r", "")).strip()
                st, key = f"Text:\n{txt}", txt
            else:
                w = wrap_zsl(t["spec"], text)
                if w is None:
                    skipped[f"label_nli: premise not parseable ({t['tasksource_task']})"] += 1
                    continue
                st, key = w
            nk = norm(key)
            by_text[nk].add(lab)
            states.setdefault(nk, (st, key, lab))
        pool = []
        for nk, labs in by_text.items():
            st, key, lab = states[nk]
            if len(labs) > 1:
                skipped[f"{t['source']}: same text with two labels in one task"] += 1
                continue
            nw = len(words(key))
            if nw < t["min_words"]:
                skipped[f"{t['source']}: under min words"] += 1
                continue
            if nw > MAX_WORDS:
                skipped[f"{t['source']}: over {MAX_WORDS} words"] += 1
                continue
            pool.append(dict(nk=nk, state=st, text=key, gold=lab))
        pool.sort(key=lambda x: hashlib.sha1(x["nk"].encode()).hexdigest())
        t["pool"] = pool
        del t["items"]

    # ---- split groups
    mix_T = [t for t in T if t["source"] == "mixtral"]
    for t, g in zip(mix_T, mixtral_groups(mix_T)):
        t["group"] = g
    for t in T:
        if t["source"] == "label_nli":
            t["group"] = "zsl_" + (t["spec"].get("group") or t["task_id"][4:])

    # ---- a text may live in one split group only (first group in sorted order keeps it)
    owner = {}
    for t in sorted(T, key=lambda x: (x["group"], x["task_id"])):
        for it in t["pool"]:
            owner.setdefault(it["nk"], t["group"])
    for t in T:
        keep = []
        for it in t["pool"]:
            if owner[it["nk"]] != t["group"]:
                skipped[f"{t['source']}: text also in another task group"] += 1
                continue
            keep.append(it)
        t["pool"] = keep

    # ---- decontamination against every non-OHS state in lean/data
    grams, lines, scanned, n_states = existing_index()
    flat = [(ti, j) for ti, t in enumerate(T) for j in range(len(t["pool"]))]
    mask = contaminated([T[ti]["pool"][j]["text"] for ti, j in flat], grams, lines)
    bad = defaultdict(set)
    for (ti, j), b in zip(flat, mask):
        if b:
            bad[ti].add(j)
    decon = Counter()
    for ti, t in enumerate(T):
        if bad[ti]:
            decon[t["source"]] += len(bad[ti])
            t["pool"] = [it for j, it in enumerate(t["pool"]) if j not in bad[ti]]

    # ---- balanced sampling
    kept = []
    for t in T:
        r = rng("taskbank", t["task_id"])
        by = defaultdict(list)
        for it in t["pool"]:
            by[it["gold"]].append(it)
        for l in sorted(by):
            r.shuffle(by[l])
        alloc = balanced_alloc({l: len(v) for l, v in by.items()})
        if alloc is None or len(by) < 2:
            skipped[f"task dropped: cannot sample {MIN_TASK_ROWS}+ texts with no label over {int(CAP * 100)}%"] += 1
            t["dropped"] = f"unbalanced/too small (pool {len(t['pool'])}, labels with texts {len(by)})"
            continue
        t["sample"] = [it for l in sorted(by) for it in by[l][: alloc[l]]]
        t["leftover"] = {l: by[l][alloc[l]:] for l in by}
        t["label_counts"] = {l: alloc.get(l, 0) for l in t["labels"]}
        kept.append(t)

    # ---- split by group, stratified by source and label-set width (the widest task in the group)
    gwidth = defaultdict(int)
    for t in kept:
        gwidth[t["group"]] = max(gwidth[t["group"]], len(t["labels"]))

    def width(g):
        k = gwidth[g]
        return "3" if k == 3 else "4" if k == 4 else "5-12" if k <= 12 else "13+"

    strata = sorted({(t["source"], width(t["group"])) for t in kept})
    for src, wb in strata:
        ts = [t for t in kept if t["source"] == src and width(t["group"]) == wb]
        groups = defaultdict(list)
        for t in ts:
            groups[t["group"]].append(t)
        order = sorted(groups, key=lambda g: sid("split", g))
        target = round(DEV_FRAC * len(ts))
        n_dev = 0
        dev_groups = set()
        for g in order:
            sz = len(groups[g])
            if n_dev < target and n_dev + sz <= max(target + 1, 2):
                dev_groups.add(g)
                n_dev += sz
        for t in ts:
            t["split"] = "dev" if t["group"] in dev_groups else "train"

    # ---- definition slices (60 tasks each, train then dev, by task_id)
    kept.sort(key=lambda t: (t["split"] != "train", t["task_id"]))
    for i, t in enumerate(kept):
        t["def_slice"] = i // SLICE

    # ---- write inventory + raw rows
    inv, rows = [], []
    for t in kept:
        disp = t["display"] or {l: l for l in t["labels"]}
        r = rng("examples", t["task_id"])
        ex = {}
        for l in t["labels"]:
            left = list(t["leftover"].get(l, []))
            cand = [x for x in left if len(words(x["text"])) <= 60] or left
            if not cand:
                cand = [x for x in t["sample"] if x["gold"] == l]
            r.shuffle(cand)
            ex[disp[l]] = [short(x["state"] if t["source"] == "label_nli" else x["text"]) for x in cand[:2]]
        entry = dict(
            task_id=t["task_id"], task_name=t["task_name"], domain_hint=t["domain_hint"],
            labels=[disp[l] for l in t["labels"]], examples=ex, split=t["split"], def_slice=t["def_slice"],
            source=t["source"], label_kind=t["label_kind"],
            needs_names=t["label_kind"] == "statement" or t["task_id"] == "tbz_silicone_oasis",
            task_description=t["desc"], instruction=(t["spec"]["instr"] if t["source"] == "label_nli" else None),
            n_rows=len(t["sample"]), label_counts={disp[l]: c for l, c in t["label_counts"].items()},
            split_group=t["group"], **({"raw_labels": {disp[l]: l for l in t["labels"]}} if t["display"] else {}),
            origin=t["hf"])
        inv.append(entry)
        rr = rng("raw_rows", t["task_id"])
        for it in t["sample"]:
            th = sid("text", it["nk"])
            opts = [disp[l] for l in t["labels"]]
            rr.shuffle(opts)
            instr = entry["instruction"] or "Which label best fits this text?"
            state = it["state"]
            rows.append({
                "id": "r_" + sid(SEED, "tbraw", t["task_id"], th), "group_id": f"g:tb:{t['task_id']}:{th}",
                "call_id": "c_" + sid(SEED, t["split"], state), "split": t["split"], "track": TRACK,
                "source": "tb_" + t["source"], "state": state, "qtype": "choice", "instructions": instr, "options": opts,
                "gold": disp[it["gold"]], "role": "choice",
                "meta": {"task_id": t["task_id"], "n_labels": len(opts), "text_sha": th, "label_kind": t["label_kind"],
                         **({"tasksource_task": t["tasksource_task"]} if t["source"] == "label_nli" else {})}})
    rows.sort(key=lambda x: x["id"])
    assert len({x["id"] for x in rows}) == len(rows)
    for x in rows:
        assert x["gold"] in x["options"] and len(set(x["options"])) == len(x["options"])
    INV.write_text(json.dumps(inv, indent=1, ensure_ascii=False))
    with open(RAW, "w") as f:
        for x in rows:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")

    def hist(ts):
        return dict(sorted(Counter(len(t["labels"]) for t in ts).items()))

    def bucket(k):
        return "3" if k == 3 else "4" if k == 4 else "5-6" if k <= 6 else "7-12" if k <= 12 else "13-26" if k <= 26 else "27-120"

    tr = [t for t in kept if t["split"] == "train"]
    dv = [t for t in kept if t["split"] == "dev"]
    summ = {
        "files": {"inventory": str(INV), "rows_raw": str(RAW), "script": str(Path(__file__).resolve())},
        "n_tasks": len(kept), "n_tasks_train": len(tr), "n_tasks_dev": len(dv),
        "n_tasks_by_source": {s: {"train": sum(t["source"] == s for t in tr), "dev": sum(t["source"] == s for t in dv)}
                              for s in ("mixtral", "label_nli")},
        "n_split_groups": len({t["group"] for t in kept}),
        "label_count_histogram": hist(kept),
        "label_count_buckets": dict(Counter(bucket(len(t["labels"])) for t in kept)),
        "label_count_histogram_train": hist(tr), "label_count_histogram_dev": hist(dv),
        "n_rows": len(rows), "rows_by_split": dict(Counter(x["split"] for x in rows)),
        "rows_by_source": dict(Counter(x["source"] for x in rows)),
        "n_labels_total": sum(len(t["labels"]) for t in kept),
        "n_labels_needing_names": sum(len(t["labels"]) for t in kept if t["label_kind"] == "statement"),
        "definition_slices_of_60": math.ceil(len(kept) / SLICE),
        "max_label_share": max(max(t["label_counts"].values()) / len(t["sample"]) for t in kept),
        "rows_per_task": {"min": min(len(t["sample"]) for t in kept), "max": max(len(t["sample"]) for t in kept)},
        "dropped_tasks": {t["task_id"]: t["dropped"] for t in T if t.get("dropped")},
        "label_nli_tasks_kept": sorted(t["tasksource_task"] for t in kept if t["source"] == "label_nli"),
        "label_nli_tasks_dropped": ZSL_DROP,
        "label_nli_all_task_label_counts": zsl_all,
        "mixtral_positive_pairs_loaded": n_mix_rows,
        "decontam": {"method": f"{NGRAM}-word run (stable hash), or whole line if under {NGRAM} words; OHS-1 files never opened",
                     "unique_states_scanned": n_states, "files_scanned": scanned, "dropped_by_source": dict(decon)},
        "skipped": dict(sorted((k, v) for k, v in skipped.items() if v)),
        "costs": {"openrouter_usd": 0.0, "modal_usd": 0.0, "note": "CPU only; no LLM calls"},
        "seed": SEED,
    }
    INV_SUMMARY.write_text(json.dumps(summ, indent=1))
    print(json.dumps({k: v for k, v in summ.items() if k not in ("label_nli_all_task_label_counts", "decontam")}, indent=1))
    print(json.dumps({"decontam": {k: v for k, v in summ["decontam"].items() if k != "files_scanned"}}, indent=1))


# ------------------------------------------------------------------ assemble mode
CODE_STYLES = ["Class {L}", "Code {N}", "Option {L}", "Category {N}", "Type {L}", "Group {L}{D}", "Label {N}"]


def opaque_codes(n: int, r: random.Random) -> list[str]:
    style = r.choice(CODE_STYLES)
    if "{L}" in style and "{D}" not in style and n > 26:
        style = r.choice(["Code {N}", "Category {N}", "Label {N}"])
    letters = [chr(65 + i) for i in range(26)]
    if "{D}" in style:
        pool = [style.format(L=l, D=d) for l in letters for d in range(1, 10)]
    elif "{L}" in style:
        pool = [style.format(L=l) for l in letters]
    else:
        lo = r.choice([1, 10, 100])
        pool = [style.format(N=k) for k in range(lo, lo + max(3 * n, 30))]
    return r.sample(pool, n)


def load_defs(ddir: Path) -> dict:
    out, src = {}, {}
    for p in sorted(ddir.glob("*.json")):
        d = json.loads(p.read_text())
        for tid, m in d.items():
            if tid in out and out[tid] != m:
                raise SystemExit(f"conflicting definitions for {tid} in {src[tid]} and {p.name}")
            out[tid], src[tid] = m, p.name
    return out


def resolve_task(entry: dict, defs: dict | None, problems: Counter):
    """-> (names {label: option name}, definitions {label: one-line def}, instruction) or None."""
    if defs is None:
        problems["task has no definitions"] += 1
        return None
    names, dfn = {}, {}
    for lab in entry["labels"]:
        v = defs.get(lab)
        if v is None:
            problems["label missing from definitions"] += 1
            return None
        if isinstance(v, dict):
            nm, d = (v.get("name") or lab).strip(), (v.get("definition") or "").strip()
        else:
            nm, d = lab, str(v).strip()
        d = re.sub(r"\s+", " ", d)
        if not d:
            problems["empty definition"] += 1
            return None
        if entry.get("needs_names") and nm == lab and entry["label_kind"] == "statement":
            problems["statement label without a short name (statement used as option)"] += 1
        nm = re.sub(r"\s+", " ", nm).replace(": ", " - ")
        names[lab], dfn[lab] = nm, d
    if len(set(names.values())) != len(names):
        problems["duplicate option names in a task"] += 1
        return None
    instr = defs.get("_instruction") or entry.get("instruction")
    if not instr:
        first = TASK_Q_FIX.get(entry["task_id"]) or task_question(entry["task_description"], len(entry["labels"]))
        instr = f"Task: {first[:1].lower() + first[1:]}. Which label applies to this text?" if first else None
    return names, dfn, instr


_NUM = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}
# Mixtral task descriptions whose first sentence, even cleaned, names only part of the label set or reads badly
TASK_Q_FIX = {
    "tbm_eec25af0": "Classify physics texts by the kind of research work they describe",
    "tbm_cc14f7d7": "Classify texts by their research approach",
    "tbm_48dbd4c8": "Classify texts by how they draw on and combine fields of knowledge",
    "tbm_11df610a": "Classify chemistry texts by the time period they focus on",
    "tbm_3a8dd213": "Classify physics texts by the time period they focus on",
}


def task_question(desc: str, n_labels: int) -> str:
    """First sentence of a Mixtral task description with the class enumerations removed ("...: A, B, or C",
    "such as ...", "choosing from the following options ...", "as A, B, or C", "into N categories" when N is wrong):
    the options and the card carry the label set, and the description's lists often name only some labels or use
    other wordings."""
    desc = re.sub(r"(?i)\s*the (classes|categories|labels) are\b.*$", "", desc).strip()
    s = re.split(r"(?<=[.!?])\s", desc)[0].strip().rstrip(".")
    s = re.sub(r"\s*\([^)]*\)", "", s)
    s = re.sub(r"(?i),?\s*(by )?(choosing|selecting|picking) (from )?(one of |among )?(the following|these|the)\b.*$", "", s)
    s = re.sub(r"(?i),?\s*\b(such as|e\.g\.|including|like|for example|for instance)\b.*$", "", s)
    s = re.sub(r"(?i),\s*whether\b.*$", "", s)
    s = re.sub(r"(?i)\s+(as|into) [\w-]+(?: [\w-]+)?(?:, [\w-]+(?: [\w-]+)?)+,? (?:or|and) [\w-]+"
               r"(?: (?:priority|sentiments?|tone))?", "", s)
    s = re.sub(r"\s*:.*$", "", s)

    def num(m):
        k = _NUM.get(m.group(1).lower()) or (int(m.group(1)) if m.group(1).isdigit() else None)
        return m.group(0) if k == n_labels else ""

    s = re.sub(r"(?i)\s+into (\w+) (?:main |distinct |different )?(categories|classes|types|groups|levels)\b", num, s)
    return re.sub(r"\s+", " ", s).strip().rstrip(",;- ")


def assemble(defs_dir: Path, out_dir: Path, n_train: int, n_dev: int, p_rename: float, p_choice: float):
    inv = json.loads(INV.read_text())
    raw = [json.loads(l) for l in open(RAW)]
    defs = load_defs(defs_dir)
    by_task = defaultdict(list)
    for x in raw:
        by_task[x["meta"]["task_id"]].append(x)
    problems = Counter()
    ready = {}
    for e in inv:
        res = resolve_task(e, defs.get(e["task_id"]), problems)
        if res is not None:
            ready[e["task_id"]] = (e, *res)
    unknown = sorted(set(defs) - {e["task_id"] for e in inv})
    rows, rels = {"train": [], "dev": []}, []
    seen_ids = set()

    def add(split, r):
        if r["id"] in seen_ids:
            problems["duplicate row id skipped"] += 1
            return None
        seen_ids.add(r["id"])
        rows[split].append(r)
        return r["id"]

    # definitions / names must not share an 8-word run with any text of their task (sampled rows + the examples the
    # definition writer saw), and short texts must not appear whole inside a definition
    leak_n = 8
    leaks = []
    for tid, (e, names, dfn, _) in ready.items():
        grams, shorts = set(), set()
        for t in [x["state"] for x in by_task[tid]] + [s for v in e["examples"].values() for s in v]:
            for part in re.split(r"\n\n(?=[^\n]*:\n)", t):
                body = part.split("\n", 1)[1] if "\n" in part and part.split("\n", 1)[0].endswith(":") else part
                ws = words(body)
                grams.update(tuple(ws[i:i + leak_n]) for i in range(len(ws) - leak_n + 1))
                if 3 <= len(ws) < leak_n:
                    shorts.add(" ".join(ws))
        for lab in e["labels"]:
            for field, val in (("definition", dfn[lab]), ("name", names[lab])):
                ws = words(val)
                hit = next((" ".join(ws[i:i + leak_n]) for i in range(len(ws) - leak_n + 1)
                            if tuple(ws[i:i + leak_n]) in grams), None)
                if hit is None:
                    padded = f" {' '.join(ws)} "
                    hit = next((s for s in sorted(shorts) if f" {s} " in padded), None)
                if hit is not None:
                    leaks.append({"task_id": tid, "label": lab, "field": field, "shared": hit})
    if leaks:
        problems["definition shares an 8-word run with a task text"] += len(leaks)

    for split, target in (("train", n_train), ("dev", n_dev)):
        tids = sorted(t for t, v in ready.items() if v[0]["split"] == split)
        if not tids:
            continue
        base, extra = divmod(target, len(tids))
        order = sorted(tids, key=lambda t: sid("quota", t))
        quota = {t: base + (1 if i < extra else 0) for i, t in enumerate(order)}
        for tid in tids:
            e, names, dfn, t_instr = ready[tid]
            labels = e["labels"]
            r = rng("assemble", tid)
            # items interleaved round-robin over gold labels (label order reshuffled every round), so the choice rows
            # and the yes/no units of a task are each close to label-balanced
            by_gold = defaultdict(list)
            for x in sorted(by_task[tid], key=lambda x: x["id"]):
                by_gold[x["gold"]].append(x)
            for g_ in sorted(by_gold):
                r.shuffle(by_gold[g_])
            items = []
            for rnd in range(max(len(v) for v in by_gold.values())):
                labs_ = sorted(by_gold)
                r.shuffle(labs_)
                items += [by_gold[g_][rnd] for g_ in labs_ if rnd < len(by_gold[g_])]
            q = quota[tid]
            n_choice = round(q * p_choice)
            yes_first = r.random() < 0.5
            k = 0
            used = 0
            made = 0
            trk = "train" if split == "train" else "dev"
            # renaming schedule: p_rename * units (stochastically rounded) renamed units, drawn separately among the
            # choice units and among the yes/no units of each task (a yes/no bundle holds 3 rows, 2 at the quota end)
            rem = max(0, q - n_choice)
            n_yn_units = rem // 3 + (1 if rem % 3 == 2 else 0)
            def n_ren(n):  # stochastic rounding keeps the overall share at p_rename for small tasks too
                x = p_rename * n
                return min(n, int(x) + (r.random() < x - int(x)))

            ren_c = set(r.sample(range(n_choice), n_ren(n_choice)))
            ren_y = set(r.sample(range(n_yn_units), n_ren(n_yn_units)))
            n_c_units = n_y_units = 0
            pos_cycle = []

            def unit_names(is_choice):
                nonlocal n_c_units, n_y_units
                if is_choice:
                    ren = n_c_units in ren_c
                    n_c_units += 1
                else:
                    ren = n_y_units in ren_y
                    n_y_units += 1
                if ren:
                    codes = opaque_codes(len(labels), r)
                    return True, dict(zip(labels, codes))
                return False, dict(names)

            while made < q and used < len(items):
                it = items[used]
                used += 1
                gold = it["gold"]
                state = it["state"]
                # a single missing row is filled with a choice row (a yes/no bundle needs at least 2)
                is_choice = made < n_choice or q - made == 1
                ren, shown = unit_names(is_choice)
                label_map = {shown[l]: l for l in labels}
                meta0 = {"task_id": tid, "task_source": e["source"], "n_labels": len(labels), "renamed": ren,
                         "label_map": label_map, "text_sha": it["meta"]["text_sha"]}
                group = it["group_id"]
                if is_choice:
                    # gold position follows a shuffled cycle over all positions, so every position gets the gold
                    # equally often inside each task (no position prior to learn)
                    if not pos_cycle:
                        pos_cycle = list(range(len(labels)))
                        r.shuffle(pos_cycle)
                    opts = [shown[l] for l in labels if l != gold]
                    r.shuffle(opts)
                    opts.insert(pos_cycle.pop(), shown[gold])
                    card = "\n".join(f"- {o}: {dfn[label_map[o]]}" for o in opts)
                    ins = r.choice(GENERIC_CHOICE) if (ren or not t_instr or r.random() < 0.5) else t_instr
                    key = f"tb|{split}|{group}|choice|{ins}|{json.dumps(opts)}"
                    rid = add(split, {"id": "r_" + sid(SEED, key), "group_id": group, "call_id": "c_" + sid(SEED, split, state),
                                      "split": split, "track": TRACK, "source": it["source"], "state": state,
                                      "qtype": "choice", "instructions": ins, "options": opts, "gold": shown[gold],
                                      "role": "choice", "card": card, "meta": {**meta0, "n_options": len(opts)}})
                    made += rid is not None
                    continue
                # yes/no bundle
                g = 1 if ((k % 2 == 0) == yes_first) else 0
                k += 1
                asked = gold if g == 1 else r.choice([l for l in labels if l != gold])
                others = [l for l in labels if l not in (asked, gold)]
                r.shuffle(others)
                shown_labels = list(dict.fromkeys([asked, gold] + others))[: max(6, 2)]
                if len(labels) <= 6:
                    shown_labels = list(labels)
                r.shuffle(shown_labels)
                card = "\n".join(f"- {shown[l]}: {dfn[l]}" for l in shown_labels)
                L = shown[asked]
                ymeta = {**meta0, "asked_label": asked, "card_labels": len(shown_labels)}

                def yn(role, tpl_list, gold_v):
                    ins = r.choice(tpl_list).format(L=L)
                    if r.random() < 0.5:
                        ins = f"{YN_NOTE} {ins}"
                    key = f"tb|{split}|{group}|{role}|{ins}|{asked}"
                    return add(split, {"id": "r_" + sid(SEED, key), "group_id": group,
                                       "call_id": "c_" + sid(SEED, split, state), "split": split, "track": TRACK,
                                       "source": it["source"], "state": state, "qtype": "noul", "instructions": ins,
                                       "options": None, "gold": gold_v, "role": role, "card": card, "meta": ymeta})

                a = yn("aff", AFF, g)
                n_ = yn("neg", NEG, 1 - g)
                made += (a is not None) + (n_ is not None)
                if a and n_:
                    rels.append({"type": "complement", "a": a, "b": n_, "track": trk})
                if made < q and a:
                    role, tpl = ("para", PARA) if r.random() < 0.6 else ("dneg", DNEG)
                    b = yn(role, tpl, g)
                    if b:
                        made += 1
                        rels.append({"type": "equiv", "a": a, "b": b, "track": trk})
            if made < q:
                problems[f"{split}: task ran out of items before its quota"] += 1

    # checks
    allr = rows["train"] + rows["dev"]
    ids = {x["id"]: x for x in allr}
    assert len(ids) == len(allr)
    raw_gold = {(x["meta"]["task_id"], x["meta"]["text_sha"]): x["gold"] for x in raw}
    code_re = re.compile(r"^(Class [A-Z]|Code \d+|Option [A-Z]|Category \d+|Type [A-Z]|Group [A-Z]\d|Label \d+)$")
    unit_sig = {}
    for x in allr:
        m = x["meta"]
        e, names, dfn, _ = ready[m["task_id"]]
        lm = m["label_map"]
        assert sorted(lm.values()) == sorted(e["labels"]), x["id"]  # shown -> canonical is a bijection
        if m["renamed"]:
            assert all(code_re.match(s) for s in lm) and not set(lm) & set(names.values()), x["id"]
        else:
            assert all(names[c] == s for s, c in lm.items()), x["id"]
        assert x["card"] and "\n\n" not in x["card"]
        card = []
        for ln in x["card"].split("\n"):
            assert ln.startswith("- ") and ": " in ln, ln
            s, d = ln[2:].split(": ", 1)
            assert s in lm and dfn[lm[s]] == d, (x["id"], s)  # each shown code/name carries its own definition
            card.append(s)
        assert len(set(card)) == len(card)
        g_can = raw_gold[(m["task_id"], m["text_sha"])]
        if x["qtype"] == "choice":
            assert x["gold"] in x["options"] and len(set(x["options"])) == len(x["options"])
            assert all(": " not in o and "\n" not in o for o in x["options"])
            assert card == x["options"] and set(x["options"]) == set(lm) and lm[x["gold"]] == g_can, x["id"]
        else:
            assert x["gold"] in (0, 1) and x["options"] is None
            inv_lm = {c: s for s, c in lm.items()}
            assert inv_lm[m["asked_label"]] in card and inv_lm[g_can] in card and f"'{inv_lm[m['asked_label']]}'" in x["instructions"]
            truth = int(m["asked_label"] == g_can)
            assert x["gold"] == (1 - truth if x["role"] == "neg" else truth), x["id"]
        # one unit per text: every row of a group shares the state and the shown names (codes)
        sig = (x["split"], x["state"], json.dumps(lm, sort_keys=True))
        assert unit_sig.setdefault(x["group_id"], sig) == sig, x["group_id"]
    for rel in rels:
        a, b = ids[rel["a"]], ids[rel["b"]]
        assert (a["gold"] + b["gold"] == 1) if rel["type"] == "complement" else (a["gold"] == b["gold"]), rel
        assert a["group_id"] == b["group_id"] and a["card"] == b["card"] and a["meta"]["label_map"] == b["meta"]["label_map"]
        assert a["meta"]["asked_label"] == b["meta"]["asked_label"] and rel["track"] == a["split"] == b["split"]
    split_of = defaultdict(set)
    for x in allr:
        split_of[norm(x["state"])].add(x["split"])
    assert all(len(v) == 1 for v in split_of.values()), "a text is in both train and dev"
    out_dir.mkdir(parents=True, exist_ok=True)
    for split in ("train", "dev"):
        rows[split].sort(key=lambda x: x["id"])
        with open(out_dir / f"taskbank_{split}.jsonl", "w") as f:
            for x in rows[split]:
                f.write(json.dumps(x, ensure_ascii=False) + "\n")
    with open(out_dir / "taskbank_relations.jsonl", "w") as f:
        for rel in rels:
            f.write(json.dumps(rel) + "\n")

    def stats(rs):
        yn_ = [x for x in rs if x["qtype"] == "noul"]
        return {"rows": len(rs), "by_role": dict(Counter(x["role"] for x in rs)),
                "by_source": dict(Counter(x["source"] for x in rs)),
                "yes_share_noul": round(sum(x["gold"] for x in yn_) / max(1, len(yn_)), 3),
                "renamed_share": round(sum(x["meta"]["renamed"] for x in rs) / max(1, len(rs)), 3),
                "card_share": round(sum(bool(x.get("card")) for x in rs) / max(1, len(rs)), 3),
                "tasks": len({x["meta"]["task_id"] for x in rs}),
                "option_count_histogram": dict(sorted(Counter(len(x["options"]) for x in rs if x["options"]).items())),
                "choice_gold_max_label_share_per_task": round(max(
                    max(c.values()) / sum(c.values()) for c in per_task_gold(rs).values()), 3) if rs else None}

    def per_task_gold(rs):
        out = defaultdict(Counter)
        for x in rs:
            if x["qtype"] == "choice":
                out[x["meta"]["task_id"]][x["meta"]["label_map"][x["gold"]]] += 1
        return out

    summ = {"files": {s: str(out_dir / f"taskbank_{s}.jsonl") for s in ("train", "dev")} | {
                "relations": str(out_dir / "taskbank_relations.jsonl")},
            "defs_dir": str(defs_dir), "tasks_in_inventory": len(inv), "tasks_with_definitions": len(ready),
            "tasks_missing_definitions": sorted(e["task_id"] for e in inv if e["task_id"] not in ready),
            "unknown_task_ids_in_defs": unknown, "train": stats(rows["train"]), "dev": stats(rows["dev"]),
            "relations": dict(Counter(f"{x['type']}/{x['track']}" for x in rels)),
            "definition_text_overlaps": leaks, "problems": dict(problems), "seed": SEED}
    (out_dir / "taskbank_summary.json").write_text(json.dumps(summ, indent=1))
    print(json.dumps(summ, indent=1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["inventory", "assemble"])
    ap.add_argument("--defs", default=str(DEFS_DIR))
    ap.add_argument("--out", default=str(OUT_DIR))
    ap.add_argument("--n-train", type=int, default=18000)
    ap.add_argument("--n-dev", type=int, default=1200)
    ap.add_argument("--p-rename", type=float, default=0.30)
    ap.add_argument("--p-choice", type=float, default=0.55)
    a = ap.parse_args()
    if a.mode == "inventory":
        inventory()
    else:
        assemble(Path(a.defs), Path(a.out), a.n_train, a.n_dev, a.p_rename, a.p_choice)


if __name__ == "__main__":
    main()
