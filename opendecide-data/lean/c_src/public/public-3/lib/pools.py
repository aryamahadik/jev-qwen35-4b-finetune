"""public-3 wording, card, label and state-style pools (Claude-written templates; no labels, no row text).

Every entry has a stable id. Yes/no wordings carry `pol`: "aff" asks the base predicate (gold 1 = predicate holds),
"neg" asks its negation (gold 1 = predicate fails; row role "neg"). Choice wordings may carry `inv` (the question asks
for the one option that does NOT have the property). Cards come in three definition styles: one_line, rubric, none
(about 15% of rows have no card). Definitions paraphrase each dataset's published annotation guideline in our own
words; they never quote a benchmark item.

Choice rows (v1.1, review-public3 fix 2). C trains and serves with decoder_io's cygnet style and schema_branch_mark
layout (decoder_io.py 908c08d7, A16). On a choice row decoder_io prints NO card text except lines
"- {exact option text}: {definition}", each appended to its option line; every other card line is hidden. So a choice
row's `card` holds only those option-definition lines (built from the *_DEFS dicts below; None when the options carry
no definition), and every other piece of choice guidance (headers, rubric steps, task notes) lives in the *_CH_GUIDES
pools and is written into `instructions`, before the question wording. Yes/no rows print the whole card under
"Definitions:", so yes/no cards are unchanged (their "- yes: / - no:" lines are lower case and never glue to the
"Yes" / "No" options).
"""
from __future__ import annotations

DEFS_STYLES = ["one_line", "rubric", "none"]
DEFS_WEIGHTS = [0.45, 0.40, 0.15]

# ---------------------------------------------------------------- XED English ------------------------------------
XED_EMOTIONS = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]
XED_WHEEL = ["joy", "trust", "fear", "surprise", "sadness", "disgust", "anger", "anticipation"]   # Plutchik order
XED_DEFS = {
    "anger": "irritation, annoyance, rage or hostility toward someone or something",
    "anticipation": "looking forward to, expecting, planning for or being eager about what comes next",
    "disgust": "revulsion, contempt or strong distaste",
    "fear": "fright, worry, anxiety or a sense of threat",
    "joy": "happiness, delight, amusement or pleasure",
    "sadness": "sorrow, grief, disappointment or regret",
    "surprise": "astonishment, or being caught off guard by something unexpected",
    "trust": "confidence in, reliance on, acceptance of or reassurance toward someone",
    "neutral": "no clear emotion: a plain remark, question or piece of information",
}
XED_YN_WORDINGS = [
    {"id": "xed_yn_w1", "pol": "aff", "text": "Does this line express {emotion}?"},
    {"id": "xed_yn_w2", "pol": "aff", "text": "Is {emotion} one of the emotions the speaker conveys in this line?"},
    {"id": "xed_yn_w3", "pol": "aff", "text": "Answer yes or no: does the subtitle line carry {emotion}?"},
    {"id": "xed_yn_w4", "pol": "aff", "text": "Would you tag this line of dialogue with the emotion {emotion}?"},
    {"id": "xed_yn_w5", "pol": "neg", "text": "Is {emotion} absent from this line?"},
    {"id": "xed_yn_w6", "pol": "neg", "text": "Would it be a mistake to tag this line with {emotion}?"},
]
XED_YN_CARDS = {
    ("aff", "one_line"): "- yes: the line expresses {emotion} ({definition}).\n- no: {emotion} is not among the "
                         "emotions the line expresses.",
    ("neg", "one_line"): "- yes: {emotion} ({definition}) is not among the emotions the line expresses.\n- no: the "
                         "line expresses {emotion}.",
    ("aff", "rubric"): "Emotion tags use Plutchik's eight basic emotions; a line can carry several at once.\n"
                       "{Emotion} means {definition}.\n1. Read the line as spoken dialogue.\n2. Judge what the speaker "
                       "conveys in this line itself, not what might happen elsewhere in the film.\n3. Answer yes if "
                       "{emotion} is conveyed, otherwise no.",
    ("neg", "rubric"): "Emotion tags use Plutchik's eight basic emotions; a line can carry several at once.\n"
                       "{Emotion} means {definition}.\n1. Read the line as spoken dialogue.\n2. Judge what the speaker "
                       "conveys in this line itself, not what might happen elsewhere in the film.\n3. Answer yes if "
                       "{emotion} is NOT conveyed; answer no if it is.",
}
XED_CH_WORDINGS = [
    {"id": "xed_ch_w1", "text": "Which emotion does this line express?"},
    {"id": "xed_ch_w2", "text": "Pick the emotion the speaker conveys in this line."},
    {"id": "xed_ch_w3", "text": "Classify the subtitle line by its emotion."},
    {"id": "xed_ch_w4", "text": "Which of the listed emotions best describes this line of dialogue?"},
]
# choice card = "- {emotion}: {XED_DEFS[emotion]}" lines for the shown options; guidance goes into instructions
XED_CH_GUIDES = {
    "one_line": None,
    "rubric": "Label the emotion the speaker conveys in this one line (Plutchik's basic emotions). Judge the line "
              "itself, not the wider scene. Exactly one listed label fits.",
}
XED_STYLES = [
    {"id": "xed_s1", "wrap": "Line: \"{text}\""},
    {"id": "xed_s2", "wrap": "Subtitle line:\n{text}"},
    {"id": "xed_s3", "wrap": "[dialogue]\n{text}\n[/dialogue]"},
    {"id": "xed_s4", "wrap": "{{\"subtitle\": {text_json}}}"},
]

# ---------------------------------------------------------------- MAMS (ACSA + ATSA) -----------------------------
MAMS_CATS = {"food": "the food", "service": "the service", "staff": "the staff", "price": "the prices",
             "ambience": "the ambience", "menu": "the menu", "place": "the location"}
MAMS_CAT_DEFS = {
    "food": "the dishes, drinks, taste, portions and quality of what is served",
    "service": "how the customer is served: speed, attention, reservations, waiting",
    "staff": "the people who work there: waiters, hosts, managers, bartenders, chefs",
    "price": "cost and value for money",
    "ambience": "atmosphere, decor, noise, music, crowd and seating comfort",
    "menu": "the choice and range of dishes offered",
    "place": "the location, neighbourhood or building of the restaurant",
}
POL_ADV = {"positive": "favorably", "negative": "unfavorably"}
MAMS_LABELS = {
    "L1": {"positive": "positive", "negative": "negative", "neutral": "neutral"},
    "L2": {"positive": "favorable", "negative": "unfavorable", "neutral": "no opinion expressed"},
}
MAMS_LABEL_DEFS = {
    "positive": "the sentence praises it or reports a good experience with it",
    "negative": "the sentence criticizes it or reports a bad experience with it",
    "neutral": "the sentence mentions it without judging it either way",
}
ACSA_YN_WORDINGS = [
    {"id": "acsa_yn_w1", "pol": "aff", "text": "Is the reviewer {pol} about {cat}?"},
    {"id": "acsa_yn_w2", "pol": "aff", "text": "Does this sentence express a {pol} opinion of {cat}?"},
    {"id": "acsa_yn_w3", "pol": "aff", "text": "Going by this sentence, does the reviewer view {cat} {adv}?"},
    {"id": "acsa_yn_w4", "pol": "neg", "text": "Is the sentence's opinion of {cat} something other than {pol}?"},
]
ACSA_YN_CARDS = {
    ("aff", "one_line"): "- yes: the sentence expresses a {pol} opinion about {cat} ({catdef}).\n- no: its opinion "
                         "about {cat} is not {pol}: the other sentiment, or a mention with no judgement.",
    ("neg", "one_line"): "- yes: the sentence's opinion about {cat} ({catdef}) is not {pol}: the other sentiment, or "
                         "a mention with no judgement.\n- no: the sentence expresses a {pol} opinion about {cat}.",
    ("aff", "rubric"): "Aspect: {cat} = {catdef}. The aspect may be referred to without being named.\n"
                       "1. Find what the sentence says about this aspect.\n2. Praise or a good experience is positive; "
                       "criticism or a bad experience is negative; a mention without judgement is neutral.\n"
                       "3. Opinions about other aspects in the same sentence do not count.\n4. Answer yes if the "
                       "opinion about this aspect is {pol}.",
    ("neg", "rubric"): "Aspect: {cat} = {catdef}. The aspect may be referred to without being named.\n"
                       "1. Find what the sentence says about this aspect.\n2. Praise or a good experience is positive; "
                       "criticism or a bad experience is negative; a mention without judgement is neutral.\n"
                       "3. Opinions about other aspects in the same sentence do not count.\n4. Answer yes if the "
                       "opinion about this aspect is anything other than {pol}; answer no if it is {pol}.",
}
ACSA_CH_WORDINGS = [
    {"id": "acsa_ch_w1", "text": "What is the sentiment toward {cat} in this review sentence?"},
    {"id": "acsa_ch_w2", "text": "How does the reviewer feel about {cat}?"},
    {"id": "acsa_ch_w3", "text": "Classify the opinion this sentence gives about {cat}."},
]
# choice card = "- {label}: {MAMS_LABEL_DEFS[polarity]}" lines; guidance goes into instructions. ACSA guides name the
# category and its definition ({target} = "the food (the dishes, ...)"); ATSA guides name the quoted term.
MAMS_POL_GUIDES = {
    ("acsa", "one_line"): "Here {cat} means {catdef}.",
    ("acsa", "rubric"): "Judge only what the sentence says about {cat} ({catdef}); opinions about anything else in the "
                        "sentence do not count. Exactly one label fits.",
    ("atsa", "one_line"): None,
    ("atsa", "rubric"): "Judge only what the sentence says about \"{term}\"; opinions about anything else in the "
                        "sentence do not count. Exactly one label fits.",
}
ATSA_YN_WORDINGS = [
    {"id": "atsa_yn_w1", "pol": "aff", "text": "Is the sentiment toward \"{term}\" {pol}?"},
    {"id": "atsa_yn_w2", "pol": "aff", "text": "Does the reviewer speak {adv} of \"{term}\"?"},
    {"id": "atsa_yn_w3", "pol": "aff", "text": "Yes or no: the opinion this sentence gives about \"{term}\" is {pol}."},
    {"id": "atsa_yn_w4", "pol": "neg", "text": "Is the opinion about \"{term}\" something other than {pol}?"},
]
ATSA_YN_CARDS = {
    ("aff", "one_line"): "- yes: the sentence expresses a {pol} opinion about \"{term}\".\n- no: its opinion about "
                         "\"{term}\" is not {pol}: the other sentiment, or a mention with no judgement.",
    ("neg", "one_line"): "- yes: the sentence's opinion about \"{term}\" is not {pol}: the other sentiment, or a "
                         "mention with no judgement.\n- no: the sentence expresses a {pol} opinion about \"{term}\".",
    ("aff", "rubric"): "Target: \"{term}\", as it appears in the sentence.\n1. Find what the sentence says about this "
                       "target.\n2. Praise or a good experience is positive; criticism or a bad experience is "
                       "negative; a mention without judgement is neutral.\n3. Opinions about other targets in the "
                       "same sentence do not count.\n4. Answer yes if the opinion about the target is {pol}.",
    ("neg", "rubric"): "Target: \"{term}\", as it appears in the sentence.\n1. Find what the sentence says about this "
                       "target.\n2. Praise or a good experience is positive; criticism or a bad experience is "
                       "negative; a mention without judgement is neutral.\n3. Opinions about other targets in the "
                       "same sentence do not count.\n4. Answer yes if the opinion about the target is anything "
                       "other than {pol}; answer no if it is {pol}.",
}
ATSA_CH_WORDINGS = [
    {"id": "atsa_ch_w1", "text": "What sentiment does the sentence express toward \"{term}\"?"},
    {"id": "atsa_ch_w2", "text": "How is \"{term}\" judged in this review sentence?"},
    {"id": "atsa_ch_w3", "text": "Pick the label for the reviewer's opinion of \"{term}\"."},
]
ATSA_WHICH_WORDINGS = [
    {"id": "atsa_wh_w1", "text": "Which of these is the reviewer {pol} about?"},
    {"id": "atsa_wh_w2", "text": "The sentence judges exactly one of the listed things {adv}. Which one?"},
    {"id": "atsa_wh_w3", "text": "Pick the item that gets a {pol} opinion in this sentence."},
]
# which-term choice: the options (terms) carry no definitions, so the card is None and all guidance is instructions
ATSA_WHICH_GUIDES = {
    "one_line": "Each option is a thing the sentence talks about. Exactly one of them gets a {pol} opinion "
                "({poldef}).",
    "rubric": "1. For each listed item, find what the sentence says about it.\n2. Praise or a good experience is "
              "positive; criticism or a bad experience is negative; a mention without judgement is neutral.\n"
              "3. Choose the single item whose opinion is {pol}.",
}
MAMS_STYLES = [
    {"id": "mams_s1", "wrap": "Review sentence: {text}"},
    {"id": "mams_s2", "wrap": "Restaurant review excerpt:\n\"{text}\""},
    {"id": "mams_s3", "wrap": "> {text}\n(from a customer review)"},
    {"id": "mams_s4", "wrap": "{{\"review_sentence\": {text_json}}}"},
]

# ---------------------------------------------------------------- Sarcasm v2 -------------------------------------
SAR_YN_WORDINGS = [
    {"id": "sar_yn_w1", "pol": "aff", "text": "Is this headline sarcastic?"},
    {"id": "sar_yn_w2", "pol": "aff", "text": "Is the headline written as satire rather than as straight news?"},
    {"id": "sar_yn_w3", "pol": "aff", "text": "Does this headline use sarcasm or irony to mock its subject?"},
    {"id": "sar_yn_w4", "pol": "neg", "text": "Is this a straightforward, non-sarcastic news headline?"},
    {"id": "sar_yn_w5", "pol": "neg", "text": "Is this headline meant to be read literally?"},
]
SAR_YN_CARDS = {
    ("aff", "one_line"): "- yes: the headline is sarcastic: it states something absurd, exaggerated or ironic for "
                         "comic or critical effect, as satire sites do.\n- no: the headline reports or comments in "
                         "earnest, as ordinary news headlines do.",
    ("neg", "one_line"): "- yes: the headline reports or comments in earnest, as ordinary news headlines do.\n- no: "
                         "the headline is sarcastic: it states something absurd, exaggerated or ironic for comic or "
                         "critical effect, as satire sites do.",
    ("aff", "rubric"): "1. Ask whether the headline could plausibly be a sincere report or opinion.\n2. Signs of "
                       "sarcasm: a mundane event told as major news, a deadpan absurdity, an ironic reversal, or a "
                       "quote no real person would say.\n3. Topic alone is not a sign: serious and silly subjects "
                       "appear in both kinds.\n4. Answer yes if the headline is sarcastic.",
    ("neg", "rubric"): "1. Ask whether the headline could plausibly be a sincere report or opinion.\n2. Signs of "
                       "sarcasm: a mundane event told as major news, a deadpan absurdity, an ironic reversal, or a "
                       "quote no real person would say.\n3. Topic alone is not a sign: serious and silly subjects "
                       "appear in both kinds.\n4. Answer yes if the headline is sincere (not sarcastic); answer no "
                       "if it is sarcastic.",
}
SAR_CH_WORDINGS = [
    {"id": "sar_ch_w1", "inv": False, "text": "Which of these headlines is sarcastic?"},
    {"id": "sar_ch_w2", "inv": False, "text": "Exactly one headline below is satire. Which one?"},
    {"id": "sar_ch_w3", "inv": True, "text": "Which of these headlines is a straight news headline?"},
    {"id": "sar_ch_w4", "inv": True, "text": "Only one of these headlines is meant literally. Which one?"},
]
# headline choice: the options (headlines) carry no definitions, so the card is None and all guidance is instructions
SAR_CH_GUIDES = {
    (False, "one_line"): "Exactly one listed headline is sarcastic (absurd, exaggerated or ironic, for comic or "
                         "critical effect); the others are sincere news headlines.",
    (True, "one_line"): "Exactly one listed headline is a sincere news headline; the others are sarcastic (absurd, "
                        "exaggerated or ironic, for comic or critical effect).",
    (False, "rubric"): "For each headline, ask whether it could plausibly be a sincere report or opinion. Deadpan "
                       "absurdity, a mundane event told as major news, or an ironic reversal marks sarcasm. Topic "
                       "alone is not a sign. Choose the single sarcastic headline.",
    (True, "rubric"): "For each headline, ask whether it could plausibly be a sincere report or opinion. Deadpan "
                      "absurdity, a mundane event told as major news, or an ironic reversal marks sarcasm. Topic "
                      "alone is not a sign. Choose the single sincere headline.",
}
# "wrap" is a str.format template (doubled braces); "ch" is the literal state of a headline-choice row (never
# formatted, so single braces: v1.1 fix 1)
SAR_STYLES = [
    {"id": "sar_s1", "wrap": "Headline: {text}", "ch": "Headlines from news and satire websites (outlet names "
                                                       "replaced by [outlet]) are listed as the options."},
    {"id": "sar_s2", "wrap": "News headline:\n\"{text}\"", "ch": "The options are news headlines. Some sites publish "
                                                                "satire; outlet names are hidden as [outlet]."},
    {"id": "sar_s3", "wrap": "{{\"headline\": {text_json}}}", "ch": "{\"task\": \"headline review\", "
                                                                    "\"outlet_names\": \"redacted\"}"},
    {"id": "sar_s4", "wrap": "Today's headline -- {text}", "ch": "A feed of headlines; [outlet] marks a hidden "
                                                                 "publication name."},
]

# ---------------------------------------------------------------- GHC --------------------------------------------
GHC_LABELS = ["hd", "cv", "vo"]
GHC_DEFS = {
    "hd": "an attack on human dignity: it demeans, dehumanizes, insults or degrades people because of their group "
          "identity (race, ethnicity, nationality, religion, gender, sexual orientation, disability, and so on)",
    "cv": "a call for violence: it urges, threatens, endorses or glorifies violent or harmful action against people "
          "because of their group identity",
    "vo": "vulgar or offensive language: profanity, slurs or obscene wording, whether or not it targets a group",
}
GHC_YN_WORDINGS = [
    {"id": "ghc_yn_hd1", "label": "hd", "pol": "aff", "text": "Does this post attack people's dignity because of a "
                                                              "group they belong to?"},
    {"id": "ghc_yn_hd2", "label": "hd", "pol": "aff", "text": "Does the post demean or dehumanize a group of people "
                                                              "for who they are?"},
    {"id": "ghc_yn_hd3", "label": "hd", "pol": "neg", "text": "Is the post free of attacks on people's dignity "
                                                              "based on their group identity?"},
    {"id": "ghc_yn_cv1", "label": "cv", "pol": "aff", "text": "Does this post call for violence against people "
                                                              "because of their group identity?"},
    {"id": "ghc_yn_cv2", "label": "cv", "pol": "aff", "text": "Does the post urge, threaten or endorse violent action "
                                                              "against a group?"},
    {"id": "ghc_yn_cv3", "label": "cv", "pol": "neg", "text": "Is the post free of any call for violence?"},
    {"id": "ghc_yn_vo1", "label": "vo", "pol": "aff", "text": "Does this post use vulgar or offensive language?"},
    {"id": "ghc_yn_vo2", "label": "vo", "pol": "aff", "text": "Does the post contain profanity, slurs or obscene "
                                                              "wording?"},
    {"id": "ghc_yn_vo3", "label": "vo", "pol": "neg", "text": "Is the post's language free of vulgarity and "
                                                              "offensive words?"},
]
GHC_YN_CARDS = {
    ("aff", "one_line"): "- yes: the post contains {def}.\n- no: it does not.",
    ("neg", "one_line"): "- yes: the post does not contain {def}.\n- no: it does.",
    ("aff", "rubric"): "Content policy check.\nTarget: {def}.\n1. Read the whole post, including quoted parts the "
                       "author endorses.\n2. Reporting or condemning such content is not the same as producing it.\n"
                       "3. Answer yes if the post itself contains the target content.",
    ("neg", "rubric"): "Content policy check.\nTarget: {def}.\n1. Read the whole post, including quoted parts the "
                       "author endorses.\n2. Reporting or condemning such content is not the same as producing it.\n"
                       "3. Answer yes if the post does NOT contain the target content; answer no if it does.",
}
# choice framing (k = 3): hate (hd or cv) / vulgar only / none. Key order is the distractor order fed to the shuffle.
GHC_CH_OPTIONS = {
    "hate": "attack on dignity or call for violence",
    "vo": "vulgar or offensive language only",
    "none": "none of these",
}
GHC_CH_WORDINGS = [
    {"id": "ghc_ch_w1", "text": "Which label fits this post?"},
    {"id": "ghc_ch_w2", "text": "Classify the post under the content policy below."},
    {"id": "ghc_ch_w3", "text": "What is the most serious problem in this post, if any?"},
]
# choice card: one "- {option}: {definition}" line per option ({hd}, {cv}, {vo} = GHC_DEFS); guidance -> instructions
GHC_CH_CARDS = {
    "one_line": "- attack on dignity or call for violence: the post contains {hd}, or {cv}.\n- vulgar or offensive "
                "language only: {vo}, with neither of the above.\n- none of these: the post has none of the above.",
    "rubric": "- attack on dignity or call for violence: (rule 1, checked first) the post contains {hd}; or {cv}.\n"
              "- vulgar or offensive language only: (rule 2) {vo}.\n- none of these: (rule 3) none of the above "
              "applies.",
}
GHC_CH_GUIDES = {
    "one_line": None,
    "rubric": "Content policy, checked in order; the first rule that applies gives the label. Reporting or condemning "
              "such content is not the same as producing it.",
}
POST_STYLES = [
    {"id": "post_s1", "wrap": "Post: {text}"},
    {"id": "post_s2", "wrap": "Social media post:\n\"\"\"\n{text}\n\"\"\""},
    {"id": "post_s3", "wrap": "{{\"post\": {text_json}}}"},
    {"id": "post_s4", "wrap": "Message from a public forum:\n{quoted}"},
]

# ---------------------------------------------------------------- EDOS -------------------------------------------
EDOS_SEXIST_DEF = ("abuse, prejudice or negative sentiment aimed at women because they are women (or because of "
                   "their gender combined with another identity, such as race or religion)")
EDOS_CATS = {
    "1. threats, plans to harm and incitement": "threats",
    "2. derogation": "derogation",
    "3. animosity": "animosity",
    "4. prejudiced discussions": "prejudiced discussion",
}
EDOS_CAT_DEFS = {
    "threats": "states an intent or wish to harm women, or urges others to harm them (physical, sexual or privacy "
               "harm)",
    "derogation": "openly insults, demeans or dehumanizes women: slurs, degrading descriptions, objectifying their "
                  "bodies, hostile generalizations",
    "animosity": "subtler or implicit sexism: stereotypes, condescension, sexist jokes, or a 'compliment' that puts "
                 "women down",
    "prejudiced discussion": "argues that mistreating women is justified, or denies that sexism and gender "
                             "inequality exist",
    "not sexist": "the post contains no sexism as defined here (it may still be rude or about women)",
}
EDOS_YN_WORDINGS = [
    {"id": "edos_yn_w1", "pol": "aff", "text": "Is this post sexist?"},
    {"id": "edos_yn_w2", "pol": "aff", "text": "Does the post contain abuse or prejudice aimed at women because they "
                                               "are women?"},
    {"id": "edos_yn_w3", "pol": "aff", "text": "Should this post be flagged under a policy against sexism?"},
    {"id": "edos_yn_w4", "pol": "neg", "text": "Is this post free of sexism?"},
    {"id": "edos_yn_w5", "pol": "neg", "text": "Can this post pass a sexism policy check without being flagged?"},
]
EDOS_YN_CARDS = {
    ("aff", "one_line"): "- yes: the post is sexist: it contains {def}.\n- no: it contains no such content.",
    ("neg", "one_line"): "- yes: the post contains no {def}.\n- no: the post is sexist: it contains such content.",
    ("aff", "rubric"): "Sexism policy.\nSexist = {def}.\nIncludes: threats, insults and slurs, objectification, "
                       "stereotypes, condescension, and denying or justifying discrimination against women.\n"
                       "Not sexist: criticism of a specific person for reasons other than gender, or neutral talk "
                       "about women.\nAnswer yes if the post is sexist.",
    ("neg", "rubric"): "Sexism policy.\nSexist = {def}.\nIncludes: threats, insults and slurs, objectification, "
                       "stereotypes, condescension, and denying or justifying discrimination against women.\n"
                       "Not sexist: criticism of a specific person for reasons other than gender, or neutral talk "
                       "about women.\nAnswer yes if the post is NOT sexist; answer no if it is.",
}
EDOS_CH_WORDINGS = [
    {"id": "edos_ch_w1", "k": 5, "text": "Which category fits this post?"},
    {"id": "edos_ch_w2", "k": 5, "text": "Classify the post using the sexism categories below."},
    {"id": "edos_ch_w3", "k": 5, "text": "What kind of sexism, if any, does this post show?"},
    {"id": "edos_ch_w4", "k": 4, "text": "This post was judged sexist. Which category of sexism does it show?"},
    {"id": "edos_ch_w5", "k": 4, "text": "The post below is sexist. Pick the category that describes how."},
    {"id": "edos_ch_w6", "k": 4, "text": "Assign the sexist post to one category."},
]
# choice card = "- {category}: {EDOS_CAT_DEFS[category]}" lines; guidance goes into instructions
EDOS_CH_GUIDES = {
    "one_line": None,
    "rubric": "Sexism taxonomy. Read the whole post and choose the one category that best describes it; the post's "
              "target must be women as a group or a woman because of her gender.",
}


def all_pool_objects():
    """Every Claude-written template object, flattened with stable ids (for the sealed check and the manifest)."""
    out = []
    g = globals()
    for name, val in g.items():
        if not name.isupper() or name in ("DEFS_STYLES", "DEFS_WEIGHTS"):
            continue
        if isinstance(val, list):
            for i, x in enumerate(val):
                if isinstance(x, dict):
                    out.append({"id": f"pub3:{name}:{x.get('id', i)}", "kind": name,
                                **{k: v for k, v in x.items() if k != 'id'}})
                else:
                    out.append({"id": f"pub3:{name}:{i}", "kind": name, "text": x})
        elif isinstance(val, dict):
            for k, v in val.items():
                if v is None:
                    continue                                     # a style with no guidance text
                key = k if isinstance(k, str) else "|".join(map(str, k))
                out.append({"id": f"pub3:{name}:{key}", "kind": name, "text": v if isinstance(v, str) else
                            json_text(v)})
        elif isinstance(val, str):
            out.append({"id": f"pub3:{name}", "kind": name, "text": val})
    return out


def json_text(v):
    import json
    return json.dumps(v, ensure_ascii=False)
