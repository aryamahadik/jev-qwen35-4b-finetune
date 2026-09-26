#!/usr/bin/env python3
"""Author the TRAIN and DEV wording banks of OpenDecide v1.0-rc (DESIGN 6.1).

Writes, next to this file, one JSONL per bank (sorted by id, deterministic, no randomness):
  aff, neg, qn, qf, scope, choice_instr, none_option, choice2_keys, choice3, score_scales, conj_disj

Only train and dev pools live here. Eval wordings are authored separately, by another agent,
in assets/templates/eval/ (never read by this script or its author).

Entry schema (every entry carries every base field; null when not applicable):
  id               "<BANK>-<style>-t<n>" (train) or "-d<n>" (dev); rule entries end in "-rule-<pool>"
  bank             aff | neg | qn | qf | scope | choice_instr | none_option | choice2_keys | choice3 | score_scales | conj_disj
  pool             train | dev
  style_or_class   AFF style F1-F6/F9; NEG class C1/C2/C4/C7; QN class QA/QJ/QD; QF; SCOPE;
                   choice family; NONE; CH2; CH3; score construct id; CONJ_DISJ
  kind             template | rule
  wording          w<n>: position in the 6.1 wording sequence of that style (train w1.., dev after train)
  text             UNSCOPED template (used on non-grounded task families)
  decl / decl_neg  Noul criteria for criteria_mode=restating: the instruction as a declarative / its denial
                   (always aligned with the instruction, never the resolved clause alone; field rule 3)
  nli              declarative NLI hypothesis rendering (ser-v1 input); for choice_instr it is the
                   per-option template with "{}" for the option key
  sources_allowed  task families the entry may be used on (intent, topic, emotion, review, nli, qa, fact,
                   sentiment, spam, toxicity, phishing, policy). Grounded families (R14): nli, qa, fact, policy.
  scoped           true iff the entry has a scoped rendering; REQUIRED (and then mandatory) whenever
                   sources_allowed contains a grounded family
  scoped_text      "{Scope}, ..." rendering used on grounded families (R14); scoped_decl / scoped_decl_neg /
                   scoped_nli are its criteria and NLI forms
  neg_words        count of lexical negation tokens in `text` outside slots (lexicon NEG_LEXICON below);
                   slot fillers (e.g. {negP}) are counted by the build, not here
  authored_by      "llm:claude:train-dev-wording-author" (deviation D1)
Slots: {p} proposition clause (lower-case start unless proper noun/acronym/"I", no final period);
       {negP} its clause-internal negation; {p2} second proposition (conj/disj only); {np} noun phrase;
       {q} polar question, capitalised, ending in "?"; {doc} / {agent} from the label asset;
       {Scope} a scope phrase from scope.jsonl of the SAME pool (itself containing {doc});
       {target} the emotion noun of an emotion-strength Score.
"""
import json
import re
from pathlib import Path

OUT = Path(__file__).resolve().parent
AUTH = "llm:claude:train-dev-wording-author"
GROUNDED = {"nli", "qa", "fact", "policy"}
PROP_FAMILIES = ["intent", "topic", "emotion", "review", "nli", "fact"]   # {p}-frames (label assets + NLI/claims)
NEGP_FAMILIES = ["intent", "topic", "emotion", "review"]                  # only sources with negP_* fields

NEG_LEXICON = {
    "not", "no", "never", "none", "nothing", "neither", "nor", "cannot", "false", "falsehood", "untrue",
    "incorrect", "inaccurate", "wrong", "erroneous", "error", "mistake", "mistaken", "misrepresent",
    "misrepresentation", "misstatement", "reject", "rejected", "contrary", "negative", "disprove",
    "disproves", "refute", "refutes", "fail", "fails", "unfavourable", "unfavourably", "dissatisfied",
    "undercut",
}
SLOT_RE = re.compile(r"\{[A-Za-z0-9_]*\}")


def neg_words(text):
    if not text:
        return 0
    toks = re.findall(r"[a-z']+", SLOT_RE.sub(" ", text).lower())
    return sum(1 for t in toks if t in NEG_LEXICON or t.endswith("n't"))


def lc1(s):
    return s[0].lower() + s[1:]


def base(id_, bank, pool, style, wording, text, **kw):
    e = {
        "id": id_, "bank": bank, "pool": pool, "style_or_class": style, "kind": "template",
        "wording": wording, "text": text, "decl": None, "decl_neg": None, "nli": None,
        "sources_allowed": None, "scoped": False, "scoped_text": None, "scoped_decl": None,
        "scoped_decl_neg": None, "scoped_nli": None, "neg_words": neg_words(text), "authored_by": AUTH,
    }
    e.update(kw)
    return e


def noul(id_, bank, pool, style, wording, text, decl, decl_neg, sources, scoped_text=None,
         scoped_decl=None, scoped_decl_neg=None, auto_scope=True, **extra):
    """A Noul frame. On grounded families it renders as scoped_text; by default scoped_* are
    '{Scope}, ' + the unscoped form with a lower-cased first letter."""
    grounded = bool(GROUNDED & set(sources))
    if grounded and scoped_text is None and auto_scope:
        scoped_text = "{Scope}, " + lc1(text)
    if grounded and scoped_decl is None and auto_scope:
        scoped_decl = "{Scope}, " + lc1(decl)
        scoped_decl_neg = "{Scope}, " + lc1(decl_neg)
    return base(id_, bank, pool, style, wording, text, decl=decl, decl_neg=decl_neg, nli=decl,
                sources_allowed=sources, scoped=scoped_text is not None, scoped_text=scoped_text,
                scoped_decl=scoped_decl, scoped_decl_neg=scoped_decl_neg, scoped_nli=scoped_decl, **extra)


# ----------------------------------------------------------------------------------------------
# AFF: F1-F6 x (w1-w3 train, w4 dev); F9 dev-only x 3. 18 train + 9 dev.
# Each row: (style, wording, pool, text, decl, decl_neg, scoped_text|None, scoped_decl|None, scoped_decl_neg|None)
AFF = [
    # F1 direct
    ("F1", "w1", "train", "Is it a fact that {p}?", "It is a fact that {p}.", "It is not a fact that {p}.", None, None, None),
    ("F1", "w2", "train", "Does it hold true that {p}?", "It holds true that {p}.", "It does not hold true that {p}.", None, None, None),
    ("F1", "w3", "train", "Is the following true: {p}?", "The following is true: {p}.", "The following is not true: {p}.", None, None, None),
    ("F1", "w4", "dev", "Can it truthfully be said that {p}?", "It can truthfully be said that {p}.", "It cannot truthfully be said that {p}.", None, None, None),
    # F2 text-grounded (the scoped form drops the second mention of the document)
    ("F2", "w1", "train", "Can one tell from the {doc} that {p}?", "One can tell from the {doc} that {p}.", "One cannot tell from the {doc} that {p}.",
     "{Scope}, can one tell that {p}?", "{Scope}, one can tell that {p}.", "{Scope}, one cannot tell that {p}."),
    ("F2", "w2", "train", "Does the {doc} make it clear that {p}?", "The {doc} makes it clear that {p}.", "The {doc} does not make it clear that {p}.",
     "{Scope}, has it been made clear that {p}?", "{Scope}, it has been made clear that {p}.", "{Scope}, it has not been made clear that {p}."),
    ("F2", "w3", "train", "Does the content of the {doc} establish that {p}?", "The content of the {doc} establishes that {p}.", "The content of the {doc} does not establish that {p}.",
     "{Scope}, does what is written establish that {p}?", "{Scope}, what is written establishes that {p}.", "{Scope}, what is written does not establish that {p}."),
    ("F2", "w4", "dev", "Does the {doc} tell us that {p}?", "The {doc} tells us that {p}.", "The {doc} does not tell us that {p}.",
     "{Scope}, are we told that {p}?", "{Scope}, we are told that {p}.", "{Scope}, we are not told that {p}."),
    # F3 statement check
    ("F3", "w1", "train", "Take the statement that {p}. Is it correct for this {doc}?", "The statement that {p} is correct for this {doc}.", "The statement that {p} is not correct for this {doc}.",
     "{Scope}, is the statement that {p} correct?", "{Scope}, the statement that {p} is correct.", "{Scope}, the statement that {p} is not correct."),
    ("F3", "w2", "train", "Someone claims that {p}. Is that claim right about the {doc}?", "The claim that {p} is right about the {doc}.", "The claim that {p} is not right about the {doc}.",
     "Someone claims that {p}. {Scope}, is that claim right?", "{Scope}, the claim that {p} is right.", "{Scope}, the claim that {p} is not right."),
    ("F3", "w3", "train", "Check this statement against the {doc}: {p}. Is it borne out?", "The {doc} bears out the statement that {p}.", "The {doc} does not bear out the statement that {p}.",
     "Check this statement: {p}. {Scope}, is it borne out?", "{Scope}, the statement that {p} is borne out.", "{Scope}, the statement that {p} is not borne out."),
    ("F3", "w4", "dev", "Statement to verify: {p}. Does the {doc} confirm it?", "The {doc} confirms the statement that {p}.", "The {doc} does not confirm the statement that {p}.",
     "Statement to verify: {p}. {Scope}, is it confirmed?", "{Scope}, the statement that {p} is confirmed.", "{Scope}, the statement that {p} is not confirmed."),
    # F4 reader
    ("F4", "w1", "train", "If someone read the {doc} closely, would they take away that {p}?", "Someone who read the {doc} closely would take away that {p}.", "Someone who read the {doc} closely would not take away that {p}.",
     "{Scope}, would a close reader take away that {p}?", "{Scope}, a close reader would take away that {p}.", "{Scope}, a close reader would not take away that {p}."),
    ("F4", "w2", "train", "Reading the {doc}, would most people understand that {p}?", "Most people reading the {doc} would understand that {p}.", "Most people reading the {doc} would not understand that {p}.",
     "{Scope}, would most readers understand that {p}?", "{Scope}, most readers would understand that {p}.", "{Scope}, most readers would not understand that {p}."),
    ("F4", "w3", "train", "After going through the {doc}, would a reader be led to the view that {p}?", "After going through the {doc}, a reader would be led to the view that {p}.", "After going through the {doc}, a reader would not be led to the view that {p}.",
     "{Scope}, would a reader be led to the view that {p}?", "{Scope}, a reader would be led to the view that {p}.", "{Scope}, a reader would not be led to the view that {p}."),
    ("F4", "w4", "dev", "Would a person who has read the {doc} know that {p}?", "A person who has read the {doc} would know that {p}.", "A person who has read the {doc} would not know that {p}.",
     "{Scope}, would a person know that {p}?", "{Scope}, a person would know that {p}.", "{Scope}, a person would not know that {p}."),
    # F5 decision (imperative; criteria restate it as a plain declarative about {p})
    ("F5", "w1", "train", "Determine whether {p}.", "It holds that {p}.", "It does not hold that {p}.", None, None, None),
    ("F5", "w2", "train", "Your task is to judge whether {p}.", "It is true that {p}.", "It is not true that {p}.",
     "{Scope}, your task is to settle whether {p}.", None, None),
    ("F5", "w3", "train", "Please assess whether {p}.", "It is correct that {p}.", "It is not correct that {p}.", None, None, None),
    ("F5", "w4", "dev", "Figure out whether {p}.", "This is true: {p}.", "This is not true: {p}.", None, None, None),
    # F6 answer rule
    ("F6", "w1", "train", "Say yes if {p}; in all remaining cases, say no.", "It is true that {p}.", "It is not true that {p}.", None, None, None),
    ("F6", "w2", "train", "Reply yes if {p}; reply no in every other case.", "It holds that {p}.", "It does not hold that {p}.", None, None, None),
    ("F6", "w3", "train", "Give yes as your answer if {p}; for anything else, give no.", "It is correct that {p}.", "It is not correct that {p}.", None, None, None),
    ("F6", "w4", "dev", "Output yes provided that {p}; output no otherwise.", "This is true: {p}.", "This is not true: {p}.", None, None, None),
    # F9 record decision (dev-only style); w1 is the 6.1 dev example
    ("F9", "w1", "dev", "Should we record that {p}?", "We should record that {p}.", "We should not record that {p}.", None, None, None),
    ("F9", "w2", "dev", "Should the record say that {p}?", "The record should say that {p}.", "The record should not say that {p}.", None, None, None),
    ("F9", "w3", "dev", "Is it right to note down that {p}?", "It is right to note down that {p}.", "It is not right to note down that {p}.", None, None, None),
]

# NEG: C2 PREFIX 3 train / 1 dev; C4 JUDGE 3 / 1; C7 REJECT dev-only x 3 (w1 = 6.1 dev example).
NEG = [
    ("C2", "w1", "train", "Is it contrary to fact that {p}?", "It is contrary to fact that {p}.", "It is not contrary to fact that {p}.", None, None, None, True),
    ("C2", "w2", "train", "Is it factually incorrect that {p}?", "It is factually incorrect that {p}.", "It is not factually incorrect that {p}.", None, None, None, True),
    ("C2", "w3", "train", "Is the following untrue: {p}?", "The following is untrue: {p}.", "The following is not untrue: {p}.", None, None, None, True),
    ("C2", "w4", "dev", "Is it a falsehood that {p}?", "It is a falsehood that {p}.", "It is not a falsehood that {p}.", None, None, None, True),
    ("C4", "w1", "train", "Is the assertion that {p} erroneous?", "The assertion that {p} is erroneous.", "The assertion that {p} is not erroneous.", None, None, None, True),
    ("C4", "w2", "train", "Would saying that {p} be an error?", "Saying that {p} would be an error.", "Saying that {p} would not be an error.", None, None, None, True),
    ("C4", "w3", "train", "Would the statement that {p} misrepresent the {doc}?", "The statement that {p} would misrepresent the {doc}.", "The statement that {p} would not misrepresent the {doc}.",
     "{Scope}, would the statement that {p} be a misrepresentation?", "{Scope}, the statement that {p} would be a misrepresentation.", "{Scope}, the statement that {p} would not be a misrepresentation.", True),
    ("C4", "w4", "dev", "Is the statement that {p} a false one?", "The statement that {p} is a false one.", "The statement that {p} is not a false one.", None, None, None, True),
    ("C7", "w1", "dev", "Should the statement that {p} be rejected?", "The statement that {p} should be rejected.", "The statement that {p} should not be rejected.", None, None, None, False),
    ("C7", "w2", "dev", "Should the view that {p} be rejected as untrue?", "The view that {p} should be rejected as untrue.", "The view that {p} should not be rejected as untrue.", None, None, None, False),
    ("C7", "w3", "dev", "Ought we to reject the idea that {p}?", "We ought to reject the idea that {p}.", "We ought not to reject the idea that {p}.", None, None, None, False),
]

# QN (always grounded: BoolQ, CondaQA). Bodies are written scoped; `text` is the same body unscoped.
# (class, wording, pool, scoped body after "{Scope}, ", scoped decl body, scoped decl_neg body)
QN = [
    ("QA", "w1", "train", "is the question '{q}' one whose answer is no?", "the question '{q}' is one whose answer is no.", "the question '{q}' is not one whose answer is no."),
    ("QA", "w2", "train", "would the question '{q}' be answered in the negative?", "the question '{q}' would be answered in the negative.", "the question '{q}' would not be answered in the negative."),
    ("QA", "w3", "dev", "does the question '{q}' call for a no?", "the question '{q}' calls for a no.", "the question '{q}' does not call for a no."),
    ("QJ", "w1", "train", "would replying yes to '{q}' be an error?", "replying yes to '{q}' would be an error.", "replying yes to '{q}' would not be an error."),
    ("QJ", "w2", "train", "is a yes answer to the question '{q}' mistaken?", "a yes answer to the question '{q}' is mistaken.", "a yes answer to the question '{q}' is not mistaken."),
    ("QJ", "w3", "dev", "would answering '{q}' with yes be incorrect?", "answering '{q}' with yes would be incorrect.", "answering '{q}' with yes would not be incorrect."),
    ("QD", "w1", "dev", "should '{q}' be recorded as a no?", "'{q}' should be recorded as a no.", "'{q}' should not be recorded as a no."),
    ("QD", "w2", "dev", "should a yes answer to '{q}' be rejected?", "a yes answer to '{q}' should be rejected.", "a yes answer to '{q}' should not be rejected."),
]

# QF polar-question frames: 4 train / 1 dev (always grounded).
QF = [
    ("w1", "train", "should the question '{q}' be answered yes?", "the question '{q}' should be answered yes.", "the question '{q}' should not be answered yes."),
    ("w2", "train", "is the question '{q}' one whose answer is yes?", "the question '{q}' is one whose answer is yes.", "the question '{q}' is not one whose answer is yes."),
    ("w3", "train", "would the question '{q}' be answered in the affirmative?", "the question '{q}' would be answered in the affirmative.", "the question '{q}' would not be answered in the affirmative."),
    ("w4", "train", None, "a yes would be the right response to '{q}'.", "a yes would not be the right response to '{q}'."),  # special layout below
    ("w5", "dev", "is answering '{q}' with yes the right call?", "answering '{q}' with yes is the right call.", "answering '{q}' with yes is not the right call."),
]

SCOPE = [
    ("w1", "train", "Judging solely from the {doc}"),
    ("w2", "train", "Using only what the {doc} says"),
    ("w3", "train", "Strictly on the basis of the {doc}"),
    ("w4", "dev", "Taking the {doc} as the sole source"),
]

# Choice instructions: 7 task families x (2 train, 1 dev). (family, sources_allowed, nli option template, rows)
CHOICE = [
    ("intent", ["intent"], "The {agent}'s {doc} is about {}.", [
        ("w1", "train", "Which option matches the request the {agent} is making in this {doc}?", None),
        ("w2", "train", "What is the {agent} trying to get done? Pick the closest option.", None),
        ("w3", "dev", "Select the option that captures the purpose of the {agent}'s {doc}.", None)]),
    ("topic", ["topic"], "The {doc} falls under the category '{}'.", [
        ("w1", "train", "Which category does the subject of this {doc} belong to?", None),
        ("w2", "train", "What kind of thing is this {doc} about? Choose one option.", None),
        ("w3", "dev", "Classify the {doc} according to what it describes.", None)]),
    ("emotion", ["emotion"], "The main emotion in the {doc} is {}.", [
        ("w1", "train", "Which emotion comes through most clearly in this {doc}?", None),
        ("w2", "train", "What feeling is the writer of this {doc} mainly expressing? Pick one.", None),
        ("w3", "dev", "Choose the emotion that best fits the tone of the {doc}.", None)]),
    ("sentiment", ["review", "sentiment"], "The sentiment of the {doc} is {}.", [
        ("w1", "train", "What attitude does the {doc} take overall? Choose one option.", None),
        ("w2", "train", "Which option best captures the overall sentiment of the {doc}?", None),
        ("w3", "dev", "Pick the sentiment that the {doc} conveys.", None)]),
    ("nli3", ["nli", "qa", "fact"], None, [
        ("w1", "train", "Which of these options correctly describes what the {doc} says about the statement?", "{Scope}, which of these options is correct?"),
        ("w2", "train", "Pick the option that matches what the {doc} establishes.", "{Scope}, pick the option that holds."),
        ("w3", "dev", "Decide which option is right given the {doc}.", "{Scope}, decide which option is right.")]),
    ("safety", ["spam", "toxicity", "phishing"], "This {doc} is {}.", [
        ("w1", "train", "Which of these categories does this {doc} fall into?", None),
        ("w2", "train", "Classify this {doc}: which of the options applies to it?", None),
        ("w3", "dev", "Sort this {doc} into one of the listed categories.", None)]),
    ("policy", ["policy"], "The correct decision is {}.", [
        ("w1", "train", "Under the policy, which outcome applies to this case?", "{Scope}, which outcome applies to this case?"),
        ("w2", "train", "Given the rules described, which option is the correct decision for this request?", "{Scope}, which option is the correct decision for this request?"),
        ("w3", "dev", "Apply the policy and choose the resulting decision.", "{Scope}, choose the decision that follows for this case.")]),
]

NONE_OPT = [
    ("w1", "train", "The {doc} matches none of the other options."),
    ("w2", "train", "None of the other listed options applies to this {doc}."),
    ("w3", "train", "Every other option is wrong for this {doc}."),
    ("w4", "dev", "No other option on the list fits the {doc}."),
]

# Choice-2 twins (R4). keys order = [positive, negative]. descriptions: {p}-form; descriptions_q: {q}-form (BoolQ/CondaQA).
CH2 = [
    ("w1", "train", ["yes", "no"], "Which answer is right for this {doc}?", "{Scope}, which answer is right?",
     {"yes": "Yes: {p}.", "no": "No: it does not hold that {p}."},
     {"yes": "One should reply yes to '{q}'.", "no": "One should reply no to '{q}'."}),
    ("w2", "train", ["true", "false"], "Pick the option that is correct about this {doc}.", "{Scope}, pick the option that is correct.",
     {"true": "The statement that {p} comes out true.", "false": "The statement that {p} comes out false."},
     {"true": "Replying yes to '{q}' would be correct.", "false": "Replying yes to '{q}' would be incorrect."}),
    ("w3", "dev", ["accurate", "inaccurate"], "Which option is right about this {doc}?", "{Scope}, which option is right?",
     {"accurate": "This is an accurate reading of the {doc}: {p}.", "inaccurate": "This is an inaccurate reading of the {doc}: {p}."},
     {"accurate": "Answering yes to '{q}' is accurate.", "inaccurate": "Answering yes to '{q}' is inaccurate."}),
]

# Choice-3 descriptions (R5). keys fixed: true / false / cannot tell ({p}-form: NLI, VitaminC);
# question form (CondaQA/BoolQ, DESIGN 3.1/3.3): yes / no / cannot tell.
CH3 = [
    ("w1", "train",
     {"true": "The {doc} establishes that {p}.", "false": "The {doc} rules out that {p}.", "cannot tell": "The {doc} neither establishes nor rules out that {p}."},
     {"yes": "The {doc} settles '{q}' with a yes.", "no": "The {doc} settles '{q}' with a no.", "cannot tell": "The {doc} leaves '{q}' unsettled."}),
    ("w2", "train",
     {"true": "The {doc} makes it certain that {p}.", "false": "The {doc} makes it impossible that {p}.", "cannot tell": "The {doc} leaves it uncertain whether {p}."},
     {"yes": "Reading the {doc}, one would answer '{q}' with yes.", "no": "Reading the {doc}, one would answer '{q}' with no.", "cannot tell": "Reading the {doc}, one could not answer '{q}' either way."}),
    ("w3", "dev",
     {"true": "What the {doc} says confirms that {p}.", "false": "What the {doc} says contradicts the idea that {p}.", "cannot tell": "What the {doc} says is not enough to decide whether {p}."},
     {"yes": "What the {doc} says answers '{q}' with a yes.", "no": "What the {doc} says answers '{q}' with a no.", "cannot tell": "What the {doc} says does not answer '{q}' either way."}),
]

# Score scales (R0/R7/R9). Per construct: 2 train + 1 dev wordings, each as a base entry and a
# polarity-reversed entry whose levels are the SAME anchors in reverse order (V25 MIRROR).
# (construct, dataset, K, sources, grounded, rule_base,
#   [(wording, pool, base_text, reversed_text, levels_low_to_high_of_base, base_scoped, reversed_scoped)])
def stars(n):
    return f"{n} star" if n == 1 else f"{n} stars"


SCORE = [
    ("satisfaction-5", "clothing", 5, ["review"], False, "R0_BASE_SRC", [
        ("w1", "train", "How satisfied is the reviewer with the product?", "How dissatisfied is the reviewer with the product?",
         ["The reviewer is very dissatisfied with the product.", "The reviewer is somewhat dissatisfied with the product.",
          "The reviewer is neither satisfied nor dissatisfied with the product.", "The reviewer is somewhat satisfied with the product.",
          "The reviewer is very satisfied with the product."], None, None),
        ("w2", "train", "How high is the star rating the reviewer gave the product?", "How low is the star rating the reviewer gave the product?",
         [f"The reviewer gave the product {stars(n)} out of 5." for n in range(1, 6)], None, None),
        ("w3", "dev", "Overall, how positive is the reviewer's opinion of the product?", "Overall, how negative is the reviewer's opinion of the product?",
         ["The reviewer's opinion of the product is very negative.", "The reviewer's opinion of the product is fairly negative.",
          "The reviewer's opinion of the product is mixed.", "The reviewer's opinion of the product is fairly positive.",
          "The reviewer's opinion of the product is very positive."], None, None),
    ]),
    ("satisfaction-3", "clothing", 3, ["review"], False, "R9_REBIN", [
        ("w1", "train", "How satisfied is the reviewer with the product overall?", "How dissatisfied is the reviewer with the product overall?",
         ["The reviewer is dissatisfied with the product.", "The reviewer has mixed or neutral feelings about the product.",
          "The reviewer is satisfied with the product."], None, None),
        ("w2", "train", "How high is the star rating the reviewer gave, in three bands?", "How low is the star rating the reviewer gave, in three bands?",
         ["The reviewer gave 1 or 2 stars out of 5.", "The reviewer gave 3 stars out of 5.", "The reviewer gave 4 or 5 stars out of 5."], None, None),
        ("w3", "dev", "How favourable is the reviewer's overall verdict on the product?", "How unfavourable is the reviewer's overall verdict on the product?",
         ["An unfavourable verdict (1 or 2 stars).", "A middling verdict (3 stars).", "A favourable verdict (4 or 5 stars)."], None, None),
    ]),
    ("drug-10", "drug", 10, ["review"], False, "R0_BASE_SRC", [
        ("w1", "train", "How high a rating, from 1 to 10, did the reviewer give this medication?", "How low a rating, from 1 to 10, did the reviewer give this medication?",
         [f"The reviewer rated it {n} out of 10." for n in range(1, 11)], None, None),
        ("w2", "train", "How pleased is the reviewer with this medication, on a 10-point scale?", "How displeased is the reviewer with this medication, on a 10-point scale?",
         ["A rating of 1 out of 10, the worst possible."] + [f"A rating of {n} out of 10." for n in range(2, 10)] + ["A rating of 10 out of 10, the best possible."], None, None),
        ("w3", "dev", "On a scale of 1 to 10, how favourably does the reviewer rate the medication?", "On a scale of 1 to 10, how unfavourably does the reviewer rate the medication?",
         [f"Rated {n} of 10." for n in range(1, 11)], None, None),
    ]),
    ("drug-5", "drug", 5, ["review"], False, "R9_REBIN", [
        ("w1", "train", "How high a rating did the reviewer give this medication, in five bands?", "How low a rating did the reviewer give this medication, in five bands?",
         ["The rating is 1 or 2 out of 10.", "The rating is 3 or 4 out of 10.", "The rating is 5 or 6 out of 10.",
          "The rating is 7 or 8 out of 10.", "The rating is 9 or 10 out of 10."], None, None),
        ("w2", "train", "How satisfied is the reviewer with the medication?", "How dissatisfied is the reviewer with the medication?",
         ["Very dissatisfied (rating 1 to 2 out of 10).", "Dissatisfied (rating 3 to 4 out of 10).", "Middling (rating 5 to 6 out of 10).",
          "Satisfied (rating 7 to 8 out of 10).", "Very satisfied (rating 9 to 10 out of 10)."], None, None),
        ("w3", "dev", "How good is the reviewer's verdict on the medication?", "How bad is the reviewer's verdict on the medication?",
         ["Very poor: rated 1 to 2 out of 10.", "Poor: rated 3 to 4 out of 10.", "Middling: rated 5 to 6 out of 10.",
          "Good: rated 7 to 8 out of 10.", "Excellent: rated 9 to 10 out of 10."], None, None),
    ]),
    ("drug-3", "drug", 3, ["review"], False, "R9_REBIN", [
        ("w1", "train", "How positive is the reviewer's overall rating of the medication?", "How negative is the reviewer's overall rating of the medication?",
         ["Negative (rated 1 to 3 out of 10).", "Mixed (rated 4 to 7 out of 10).", "Positive (rated 8 to 10 out of 10)."], None, None),
        ("w2", "train", "How favourable is the reviewer's rating of this medication?", "How unfavourable is the reviewer's rating of this medication?",
         ["A low rating (1 to 3 out of 10).", "A middling rating (4 to 7 out of 10).", "A high rating (8 to 10 out of 10)."], None, None),
        ("w3", "dev", "How much does the reviewer like this medication, judging by their rating?", "How much does the reviewer dislike this medication, judging by their rating?",
         ["They rated it 1 to 3 out of 10.", "They rated it 4 to 7 out of 10.", "They rated it 8 to 10 out of 10."], None, None),
    ]),
    ("drug-2", "drug", 2, ["review"], False, "R9_REBIN", [
        ("w1", "train", "How high does the reviewer rate this medication?", "How low does the reviewer rate this medication?",
         ["A rating in the lower half (1 to 5 out of 10).", "A rating in the upper half (6 to 10 out of 10)."], None, None),
        ("w2", "train", "How favourably did the reviewer judge the medication overall?", "How unfavourably did the reviewer judge the medication overall?",
         ["An unfavourable verdict (rated 5 or lower out of 10).", "A favourable verdict (rated 6 or higher out of 10)."], None, None),
        ("w3", "dev", "How good was the reviewer's experience with this medication, judging by their rating?", "How bad was the reviewer's experience with this medication, judging by their rating?",
         ["The rating is 5 out of 10 or below.", "The rating is 6 out of 10 or above."], None, None),
    ]),
    ("nli-3", "mnli", 3, ["nli"], True, "R0_BASE_SRC", [
        ("w1", "train", "How well does the {doc} support the statement that {p}?", "How strongly does the {doc} speak against the statement that {p}?",
         ["The {doc} contradicts the statement.", "The {doc} neither supports nor contradicts the statement.", "The {doc} supports the statement."],
         "{Scope}, how well supported is the statement that {p}?", "{Scope}, how strongly contradicted is the statement that {p}?"),
        ("w2", "train", "To what extent is the statement that {p} backed by the {doc}?", "To what extent is the statement that {p} ruled out by the {doc}?",
         ["The statement is ruled out by the {doc}.", "The statement is left open by the {doc}.", "The statement is confirmed by the {doc}."],
         "{Scope}, how firmly backed is the statement that {p}?", "{Scope}, how firmly ruled out is the statement that {p}?"),
        ("w3", "dev", "How far does the {doc} go toward confirming the claim that {p}?", "How far does the {doc} go toward disproving the claim that {p}?",
         ["The {doc} shows the claim to be false.", "The {doc} does not settle the claim.", "The {doc} shows the claim to be true."],
         "{Scope}, how well established is the claim that {p}?", "{Scope}, how thoroughly disproved is the claim that {p}?"),
    ]),
    ("vitaminc-3", "vitaminc", 3, ["fact"], True, "R0_BASE_SRC", [
        ("w1", "train", "How well does the {doc} back up the claim that {p}?", "How strongly does the {doc} undercut the claim that {p}?",
         ["The {doc} refutes the claim.", "The {doc} does not give enough information to judge the claim.", "The {doc} supports the claim."],
         "{Scope}, how well backed up is the claim that {p}?", "{Scope}, how badly undercut is the claim that {p}?"),
        ("w2", "train", "To what degree does the {doc} bear out the claim that {p}?", "To what degree does the {doc} count against the claim that {p}?",
         ["The claim is shown false by the {doc}.", "The claim can be neither confirmed nor refuted from the {doc}.", "The claim is shown true by the {doc}."],
         "{Scope}, how fully borne out is the claim that {p}?", "{Scope}, how fully contradicted is the claim that {p}?"),
        ("w3", "dev", "How far does the {doc} vindicate the claim that {p}?", "How far does the {doc} discredit the claim that {p}?",
         ["The {doc} disproves the claim.", "The {doc} is not enough to decide the claim.", "The {doc} proves the claim."],
         "{Scope}, how clearly vindicated is the claim that {p}?", "{Scope}, how clearly discredited is the claim that {p}?"),
    ]),
    ("emotion-strength-3", "goemotions", 3, ["emotion"], False, "R12_SOFT", [
        ("w1", "train", "How clearly does the {doc} express {target}?", "How far is the {doc} from expressing {target}?",
         ["The {doc} shows no sign of {target}.", "The {doc} shows a faint or mixed sign of {target}.", "The {doc} shows a clear sign of {target}."], None, None),
        ("w2", "train", "How much {target} comes through in the {doc}?", "How free of {target} is the {doc}?",
         ["The {doc} carries no {target}.", "The {doc} carries a trace of {target}.", "The {doc} clearly carries {target}."], None, None),
        ("w3", "dev", "To what degree does the writer convey {target}?", "How little {target} does the writer convey?",
         ["The writer conveys no {target}.", "The writer conveys some {target}.", "The writer conveys strong {target}."], None, None),
    ]),
]

# Conj / disj (R10): 2 train / 1 dev; each entry is one conj + disj wording pair.
CD = [
    ("w1", "train",
     ("Does the {doc} show both that {p} and that {p2}?", "The {doc} shows both that {p} and that {p2}.", "The {doc} does not show both that {p} and that {p2}."),
     ("Does the {doc} show that {p}, or that {p2}, or both?", "The {doc} shows that {p}, or that {p2}, or both.", "The {doc} shows neither that {p} nor that {p2}.")),
    ("w2", "train",
     ("Are both of these true of the {doc}: that {p}, and that {p2}?", "Both of these are true of the {doc}: that {p}, and that {p2}.", "Not both of these are true of the {doc}: that {p}, and that {p2}."),
     ("Is at least one of these true of the {doc}: that {p}, or that {p2}?", "At least one of these is true of the {doc}: that {p}, or that {p2}.", "Not even one of these is true of the {doc}: that {p}, or that {p2}.")),
    ("w3", "dev",
     ("Is it correct to state that {p}, and in addition that {p2}?", "It is correct to state that {p}, and in addition that {p2}.", "It is not correct to state that {p}, and in addition that {p2}."),
     ("Is it correct to state that {p}, or that {p2}, or that both are so?", "It is correct to state that {p}, or that {p2}, or that both are so.", "It is correct to state neither that {p} nor that {p2}.")),
]


def tid(prefix, style, pool, n):
    return f"{prefix}-{style}-{'t' if pool == 'train' else 'd'}{n}"


def build():
    banks = {k: [] for k in ["aff", "neg", "qn", "qf", "scope", "choice_instr", "none_option", "choice2_keys",
                             "choice3", "score_scales", "conj_disj"]}
    # AFF
    counters = {}
    for style, w, pool, text, decl, dneg, st, sd, sdn in AFF:
        k = (style, pool)
        counters[k] = counters.get(k, 0) + 1
        e = noul(tid("AFF", style, pool, counters[k]), "aff", pool, style, w, text, decl, dneg, PROP_FAMILIES,
                 scoped_text=st, scoped_decl=sd, scoped_decl_neg=sdn, negp_ok=True)
        banks["aff"].append(e)
    # NEG: C1 rule entries (no templates of their own)
    for pool in ("train", "dev"):
        banks["neg"].append(base(
            f"NEG-C1-rule-{pool}", "neg", pool, "C1", None, None, kind="rule",
            rule=("C1 CLAUSE: render every AFF frame of the same pool with {p} := {negP} (clause-internal negation "
                  "from the label asset, negP_tr in train, negP_dev in dev). template_id = the AFF id; "
                  "negation_class = C1; decl / decl_neg / nli / scoped_* come from that AFF entry with the same "
                  "substitution; gold R2_NEG. Only on label-asset families (no negP exists for NLI hypotheses, "
                  "VitaminC claims or polar questions). Not usable for double negation."),
            applies_to_bank="aff", sources_allowed=NEGP_FAMILIES, dneg_ok=False))
    counters = {}
    for cls, w, pool, text, decl, dneg, st, sd, sdn, dneg_ok in NEG:
        k = (cls, pool)
        counters[k] = counters.get(k, 0) + 1
        e = noul(tid("NEG", cls, pool, counters[k]), "neg", pool, cls, w, text, decl, dneg, PROP_FAMILIES,
                 scoped_text=st, scoped_decl=sd, scoped_decl_neg=sdn,
                 dneg_ok=dneg_ok,
                 dneg_sources_allowed=NEGP_FAMILIES if dneg_ok else [],
                 dneg_note=("double negation = this template with {p} := {negP} (pool inherited); gold R3_EQUIV"
                            if dneg_ok else "not used for double negation (6.1: dev double negation = C2 + C4 dev wordings)"))
        banks["neg"].append(e)
    # QN
    counters = {}
    for cls, w, pool, body, dbody, dnbody in QN:
        k = (cls, pool)
        counters[k] = counters.get(k, 0) + 1
        text = body[0].upper() + body[1:]
        e = base(tid("QN", cls, pool, counters[k]), "qn", pool, cls, w, text,
                 decl=dbody[0].upper() + dbody[1:], decl_neg=dnbody[0].upper() + dnbody[1:],
                 nli=dbody[0].upper() + dbody[1:], sources_allowed=["qa"], scoped=True,
                 scoped_text="{Scope}, " + body, scoped_decl="{Scope}, " + dbody,
                 scoped_decl_neg="{Scope}, " + dnbody, scoped_nli="{Scope}, " + dbody,
                 dneg_ok=False, dneg_note="polar-question negations have no double-negation form in 6.1")
        banks["qn"].append(e)
    # QF
    counters = {}
    for w, pool, body, dbody, dnbody in QF:
        counters[pool] = counters.get(pool, 0) + 1
        if body is None:   # w4: the question comes first, the scope phrase opens the second sentence
            text = "Question: '{q}' Would a yes be the right response?"
            scoped_text = "Question: '{q}' {Scope}, would a yes be the right response?"
        else:
            text = body[0].upper() + body[1:]
            scoped_text = "{Scope}, " + body
        e = base(f"QF-{'t' if pool == 'train' else 'd'}{counters[pool]}", "qf", pool, "QF", w, text,
                 decl=dbody[0].upper() + dbody[1:], decl_neg=dnbody[0].upper() + dnbody[1:],
                 nli=dbody[0].upper() + dbody[1:], sources_allowed=["qa"], scoped=True,
                 scoped_text=scoped_text, scoped_decl="{Scope}, " + dbody,
                 scoped_decl_neg="{Scope}, " + dnbody, scoped_nli="{Scope}, " + dbody)
        banks["qf"].append(e)
    # SCOPE
    counters = {}
    for w, pool, text in SCOPE:
        counters[pool] = counters.get(pool, 0) + 1
        banks["scope"].append(base(f"SCOPE-{'t' if pool == 'train' else 'd'}{counters[pool]}", "scope", pool,
                                   "SCOPE", w, text, sources_allowed=sorted(GROUNDED),
                                   usage="prefix '{Scope}, ' of scoped_text / scoped_decl on grounded families (R14); same pool as the frame"))
    # CHOICE instructions
    for fam, srcs, nli_opt, rows in CHOICE:
        counters = {}
        for w, pool, text, st in rows:
            counters[pool] = counters.get(pool, 0) + 1
            grounded = bool(GROUNDED & set(srcs))
            banks["choice_instr"].append(base(
                f"CI-{fam}-{'t' if pool == 'train' else 'd'}{counters[pool]}", "choice_instr", pool, fam, w, text,
                nli=nli_opt, sources_allowed=srcs, scoped=st is not None, scoped_text=st,
                scoped_nli=nli_opt if grounded else None))
    # NONE option (key fixed "none of these"; text = its description)
    counters = {}
    for w, pool, text in NONE_OPT:
        counters[pool] = counters.get(pool, 0) + 1
        banks["none_option"].append(base(f"NONE-{'t' if pool == 'train' else 'd'}{counters[pool]}", "none_option",
                                         pool, "NONE", w, text, key="none of these", nli=text,
                                         sources_allowed=["intent", "topic", "emotion"]))
    # CHOICE-2 keys
    counters = {}
    for w, pool, keys, text, st, desc, desc_q in CH2:
        counters[pool] = counters.get(pool, 0) + 1
        banks["choice2_keys"].append(base(
            f"CH2-{'t' if pool == 'train' else 'd'}{counters[pool]}", "choice2_keys", pool, "CH2", w, text,
            keys=keys, key_polarity={keys[0]: "gold(Noul)=1", keys[1]: "gold(Noul)=0"},
            descriptions=desc, descriptions_q=desc_q,
            sources_allowed=PROP_FAMILIES + ["qa"], scoped=True, scoped_text=st,
            note="R4 CHOICE2 twin of a Noul; content in the descriptions ({p}-form, or {q}-form on qa); "
                 "on grounded families use scoped_text (the scope phrase is carried by the instruction)"))
    # CHOICE-3
    counters = {}
    for w, pool, desc, desc_q in CH3:
        counters[pool] = counters.get(pool, 0) + 1
        banks["choice3"].append(base(
            f"CH3-{'t' if pool == 'train' else 'd'}{counters[pool]}", "choice3", pool, "CH3", w, None,
            keys=["true", "false", "cannot tell"], keys_q=["yes", "no", "cannot tell"],
            descriptions=desc, descriptions_q=desc_q, sources_allowed=["nli", "qa", "fact"], scoped=True,
            instruction_bank="choice_instr family nli3 (scoped_text), same pool",
            note="R5 CHOICE3: e/SUPPORTS/YES -> true|yes; c/REFUTES/NO -> false|no; n/NEI/DON'T KNOW -> cannot tell. "
                 "Descriptions name the {doc}, so they stay scoped; the instruction carries {Scope}."))
    # SCORE scales
    for cons, ds, K, srcs, grounded, rule, rows in SCORE:
        counters = {}
        for w, pool, btext, rtext, levels, bst, rst in rows:
            counters[pool] = counters.get(pool, 0) + 1
            n = counters[pool]
            pid = f"SC-{cons}-{'t' if pool == 'train' else 'd'}{n}"
            assert len(levels) == K, (cons, w)
            for pol, text, lv, st in (("base", btext, levels, bst), ("reversed", rtext, list(reversed(levels)), rst)):
                banks["score_scales"].append(base(
                    f"{pid}-{'base' if pol == 'base' else 'rev'}", "score_scales", pool, cons, w, text,
                    construct=cons, dataset=ds, K=K, polarity=pol, pair_id=pid, levels=lv,
                    rule=rule if pol == "base" else "R7_SCORE_REV",
                    sources_allowed=srcs, scoped=st is not None, scoped_text=st,
                    note=("levels low->high of the quantity the instruction asks about; the reversed entry uses the "
                          "base anchors in reverse order and names the opposite pole (R7, V25)"
                          + ("; {target} = Ekman emotion noun (anger, disgust, fear, joy, sadness, surprise), "
                             "never the neutral group" if cons == "emotion-strength-3" else ""))))
    # CONJ / DISJ
    counters = {}
    for w, pool, conj, disj in CD:
        counters[pool] = counters.get(pool, 0) + 1
        banks["conj_disj"].append(base(
            f"CD-{'t' if pool == 'train' else 'd'}{counters[pool]}", "conj_disj", pool, "CONJ_DISJ", w, conj[0],
            decl=conj[1], decl_neg=conj[2], nli=conj[1],
            text_disj=disj[0], decl_disj=disj[1], decl_neg_disj=disj[2], nli_disj=disj[1],
            neg_words_disj=neg_words(disj[0]), sources_allowed=["intent"],
            note="text/decl* = conjunction (R10 CONJ, gold A and B); *_disj = disjunction (R10 DISJ, gold A or B); "
                 "{p2} is the second proposition clause"))
    return banks


def main():
    banks = build()
    for name, rows in banks.items():
        rows = sorted(rows, key=lambda r: r["id"])
        ids = [r["id"] for r in rows]
        assert len(ids) == len(set(ids)), name
        with open(OUT / f"{name}.jsonl", "w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False, sort_keys=False) + "\n")
        print(f"{name:14s} {len(rows):3d} entries "
              f"(train {sum(r['pool'] == 'train' for r in rows)}, dev {sum(r['pool'] == 'dev' for r in rows)})")


if __name__ == "__main__":
    main()
