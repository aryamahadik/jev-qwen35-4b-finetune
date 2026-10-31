"""public-1 wording, card and state-style pools (Claude-written templates; no labels). Every entry has a stable id.

Yes/no wordings carry `pol`: "aff" asks the base predicate (gold 1 = predicate holds), "neg" asks its negation
(gold 1 = predicate fails; row role "neg"). Cards come in three definition styles: one_line, rubric, none
(about 15% of rows have no card).
"""
from __future__ import annotations

DEFS_STYLES = ["one_line", "rubric", "none"]
DEFS_WEIGHTS = [0.45, 0.40, 0.15]

# ---------------------------------------------------------------- SQuAD 2.0 -------------------------------------
SQ_YN_WORDINGS = [
    {"id": "sq_yn_w1", "pol": "aff", "text": "Does the passage answer the question?"},
    {"id": "sq_yn_w2", "pol": "aff", "text": "Can the question be answered using only the passage?"},
    {"id": "sq_yn_w3", "pol": "aff", "text": "Is the answer to this question stated in the passage?"},
    {"id": "sq_yn_w4", "pol": "aff", "text": "Going only by the text above, is it possible to answer the question?"},
    {"id": "sq_yn_w5", "pol": "neg", "text": "Does the passage leave the question unanswered?"},
    {"id": "sq_yn_w6", "pol": "neg", "text": "Is it impossible to answer the question from the passage alone?"},
]
SQ_YN_CARDS = {
    ("aff", "one_line"): "- yes: The passage states the answer to the question exactly as it is asked.\n"
                         "- no: The passage does not give that answer: it may mention related facts, but none of them "
                         "answers the question as asked.",
    ("neg", "one_line"): "- yes: The passage does not give the answer to the question as asked, even if it mentions "
                         "related facts.\n- no: The passage states the answer to the question exactly as it is asked.",
    ("aff", "rubric"): "Decide from the passage alone, without outside knowledge.\n1. Find what the question asks for "
                       "(the entity, time, quantity or relation).\n2. If some part of the passage gives that exact "
                       "thing for that exact case, answer yes.\n3. If the passage only covers a different entity, "
                       "period or relation, or contradicts a premise of the question, answer no.",
    ("neg", "rubric"): "Decide from the passage alone, without outside knowledge.\n1. Find what the question asks for "
                       "(the entity, time, quantity or relation).\n2. If some part of the passage gives that exact "
                       "thing for that exact case, answer no.\n3. If the passage only covers a different entity, "
                       "period or relation, or contradicts a premise of the question, answer yes.",
}
SQ_CH_WORDINGS = [
    {"id": "sq_ch_w1", "inv": False, "text": "Which of the following questions does the passage answer?"},
    {"id": "sq_ch_w2", "inv": False, "text": "Only one of these questions can be answered from the passage. Which one?"},
    {"id": "sq_ch_w3", "inv": False, "text": "Pick the question that the passage gives an answer to."},
    {"id": "sq_ch_w4", "inv": True, "text": "Which of these questions is not answered by the passage?"},
    {"id": "sq_ch_w5", "inv": True, "text": "All but one of these questions can be answered from the passage. Which one cannot?"},
    {"id": "sq_ch_w6", "inv": True, "text": "Pick the question that the passage leaves unanswered."},
]
SQ_CH_CARDS = {
    (False, "one_line"): "Exactly one listed question is answered by the passage. A question counts as answered only "
                         "if the passage states its answer for the question exactly as asked.",
    (True, "one_line"): "Exactly one listed question is not answered by the passage. A question counts as answered "
                        "only if the passage states its answer for the question exactly as asked.",
    (False, "rubric"): "For each question: check the entity, time and relation it asks about, then look for a part "
                       "of the passage that answers exactly that. Questions that change a detail of what the passage "
                       "says are not answered. Choose the single question that is answered.",
    (True, "rubric"): "For each question: check the entity, time and relation it asks about, then look for a part "
                      "of the passage that answers exactly that. Questions that change a detail of what the passage "
                      "says are not answered. Choose the single question that is not answered.",
}
SQ_STYLES = [
    {"id": "sq_s1", "yn": "Passage:\n{passage}\n\nQuestion: {question}", "ch": "Passage:\n{passage}"},
    {"id": "sq_s2", "yn": "Text:\n\"\"\"\n{passage}\n\"\"\"\n\nQuestion: {question}", "ch": "Text:\n\"\"\"\n{passage}\n\"\"\""},
    {"id": "sq_s3", "yn": "### Excerpt from the article \"{title}\"\n{passage}\n\n### Question\n{question}",
     "ch": "### Excerpt from the article \"{title}\"\n{passage}"},
    {"id": "sq_s4", "yn": "{{\"source_article\": {title_json}, \"passage\": {passage_json}, \"question\": {question_json}}}",
     "ch": "{{\"source_article\": {title_json}, \"passage\": {passage_json}}}"},
]

# ---------------------------------------------------------------- MuSiQue ---------------------------------------
MU_YN_WORDINGS = [
    {"id": "mu_yn_w1", "pol": "aff", "text": "Do these paragraphs contain enough information to answer the question?"},
    {"id": "mu_yn_w2", "pol": "aff", "text": "Can the question be fully answered by combining facts from the paragraphs?"},
    {"id": "mu_yn_w3", "pol": "aff", "text": "Is every fact needed to answer the question given somewhere in the paragraphs?"},
    {"id": "mu_yn_w4", "pol": "neg", "text": "Is at least one fact needed to answer the question missing from the paragraphs?"},
    {"id": "mu_yn_w5", "pol": "neg", "text": "Would you have to go beyond these paragraphs to answer the question?"},
]
MU_YN_CARDS = {
    ("aff", "one_line"): "- yes: Chaining facts stated in the paragraphs leads to the answer, with every step of the "
                         "chain stated.\n- no: At least one step of the chain is not stated in any paragraph (facts "
                         "about other, similar entities do not count).",
    ("neg", "one_line"): "- yes: At least one step of the chain from the question to its answer is not stated in any "
                         "paragraph (facts about other, similar entities do not count).\n- no: Chaining facts stated "
                         "in the paragraphs leads to the answer, with every step of the chain stated.",
    ("aff", "rubric"): "Break the question into its steps (for example: who made X, then where was that person born). "
                       "For each step, find a paragraph that states it for the exact entity reached by the previous "
                       "step. Answer yes only if every step is found. If any step is missing, answer no. Do not use "
                       "outside knowledge.",
    ("neg", "rubric"): "Break the question into its steps (for example: who made X, then where was that person born). "
                       "For each step, find a paragraph that states it for the exact entity reached by the previous "
                       "step. Answer yes if any step is missing. Answer no only if every step is found. Do not use "
                       "outside knowledge.",
}
MU_CH_WORDINGS = [
    {"id": "mu_ch_w1", "text": "Which of these paragraphs is needed to answer the question?"},
    {"id": "mu_ch_w2", "text": "One of the listed paragraphs supplies a fact that the answer depends on. Which one?"},
    {"id": "mu_ch_w3", "text": "Which paragraph would you have to read to answer the question?"},
    {"id": "mu_ch_w4", "text": "To work out the answer, which of these paragraphs do you use?"},
]
MU_CH_CARDS = {
    "one_line": "Exactly one listed paragraph states a fact on the chain from the question to its answer; the other "
                "listed paragraphs are not used.",
    "rubric": "Work out the chain of facts from the question to its answer. Then check each listed paragraph: pick the "
              "one that states a step of that chain. A paragraph about a similar name or topic that no step needs is "
              "not the answer.",
}
# v1.2 (repair round 1): choice options name the paragraph by its shown number only. With the page title in the
# option, the options-only baseline learned which titles MuSiQue's supporting pages tend to be (G6 0.48-0.52 vs 0.29).
MU_STYLES = [
    {"id": "mu_s1", "para": "[{n}] {title}\n{text}", "join": "\n\n", "wrap": "Paragraphs:\n\n{paras}\n\nQuestion: {question}",
     "opt": "Paragraph {n}"},
    {"id": "mu_s2", "para": "Paragraph {n}: {title}\n{text}", "join": "\n\n", "wrap": "Question: {question}\n\n{paras}",
     "opt": "Paragraph {n}"},
    {"id": "mu_s3", "para": "## {n}. {title}\n{text}", "join": "\n\n", "wrap": "# Reference paragraphs\n\n{paras}\n\n# Question\n{question}",
     "opt": "Section {n}"},
    {"id": "mu_s4", "para": "<doc id=\"{n}\" title=\"{title}\">\n{text}\n</doc>", "join": "\n", "wrap": "{paras}\n\nQuestion: {question}",
     "opt": "doc {n}"},
]

# ---------------------------------------------------------------- 2WikiMultihopQA -------------------------------
TW_YN_WORDINGS = [
    {"id": "tw_yn_w1", "pol": "aff", "text": "Based on the paragraphs, answer yes or no: {question}"},
    {"id": "tw_yn_w2", "pol": "aff", "text": "{question} Decide using only the paragraphs."},
    {"id": "tw_yn_w3", "pol": "aff", "text": "Answer using only the facts in the paragraphs. {question}"},
    {"id": "tw_yn_w4", "pol": "aff", "text": "{question}"},
]
TW_YN_CARDS = {
    ("aff", "one_line"): "- yes: The paragraphs show that what the question asks holds (for example, both have the "
                         "same value).\n- no: The paragraphs show that it does not hold (for example, the two values "
                         "differ).",
    ("aff", "rubric"): "1. Find the paragraph about each entity the question names (follow one link if the question "
                       "names an entity through another, such as 'the director of film X').\n2. Read the value the "
                       "question compares (country, nationality, date, place).\n3. Answer yes if the comparison "
                       "holds, no if it does not.",
}
TW_CH_WORDINGS = [
    {"id": "tw_ch_w1", "text": "{question}"},
    {"id": "tw_ch_w2", "text": "Answer the comparison question from the paragraphs: {question}"},
    {"id": "tw_ch_w3", "text": "{question} Choose one of the two options, using only the paragraphs."},
    {"id": "tw_ch_w4", "text": "Using the paragraphs, which option answers this question? {question}"},
]
TW_CH_CARDS = {
    "one_line": "Pick the option that the paragraphs show is the right side of the comparison (for example the "
                "earlier date or the older person).",
    "rubric": "1. Find each option's paragraph (or, for 'the director of film X', the director's paragraph).\n2. Read "
              "the value the question compares.\n3. Pick the option whose value satisfies the comparison.",
}
TW_STYLES = [
    {"id": "tw_s1", "para": "{title}\n{text}", "join": "\n\n", "wrap": "{paras}"},
    {"id": "tw_s2", "para": "Title: {title}\nText: {text}", "join": "\n\n", "wrap": "Paragraphs:\n{paras}"},
    {"id": "tw_s3", "para": "- {title}: {text}", "join": "\n", "wrap": "Background notes:\n{paras}"},
    {"id": "tw_s4", "para": "### {title}\n{text}", "join": "\n\n", "wrap": "{paras}"},
]

# ---------------------------------------------------------------- QuALITY ---------------------------------------
QU_CH_WORDINGS = [
    {"id": "qu_ch_w1", "text": "Read the text and answer the question: {question}"},
    {"id": "qu_ch_w2", "text": "{question}"},
    {"id": "qu_ch_w3", "text": "Question about the document: {question} Choose the best answer."},
    {"id": "qu_ch_w4", "text": "Based on the whole text, {question}"},
]
QU_NOTA_WORDINGS = [
    {"id": "qu_nt_w1", "text": "Read the text and answer the question: {question} If no listed answer is right, choose the none option."},
    {"id": "qu_nt_w2", "text": "{question}"},
    {"id": "qu_nt_w3", "text": "Question about the document: {question} One option may say that none of the answers is correct."},
    {"id": "qu_nt_w4", "text": "Based on the whole text, {question}"},
]
QU_NOTA_STRINGS = ["None of the listed answers is correct", "None of these", "None of the other options is right"]
QU_CH_CARDS = {
    "one_line": "Pick the one answer that the text supports best; the other answers are wrong or less supported.",
    "rubric": "Read the whole text. For each answer, check whether the text supports it, taking the full story or "
              "argument into account rather than one sentence. Pick the answer the text supports best.",
}
QU_NOTA_CARDS = {
    "one_line": "Pick the answer the text supports. If none of the listed answers is supported by the text, pick the "
                "option that says none is correct.",
    "rubric": "Read the whole text. Check each listed answer against it. If one answer is supported by the text, pick "
              "it. Pick the 'none' option only if every other listed answer is wrong according to the text.",
}
QU_STYLES = [
    {"id": "qu_s1", "wrap": "Title: {title}\n\n{article}"},
    {"id": "qu_s2", "wrap": "Document:\n<<<\n{article}\n>>>"},
    {"id": "qu_s3", "wrap": "# {title}\n\n{article}"},
    {"id": "qu_s4", "wrap": "The following text is \"{title}\".\n\n{article}\n\n(End of text.)"},
]

# ---------------------------------------------------------------- Qasper ----------------------------------------
QA_ANS_WORDINGS = [
    {"id": "qa_an_w1", "pol": "aff", "text": "Does the paper give enough information to answer the question?"},
    {"id": "qa_an_w2", "pol": "aff", "text": "Can the question be answered from this paper's text?"},
    {"id": "qa_an_w3", "pol": "aff", "text": "Is the answer to the question found in the paper?"},
    {"id": "qa_an_w4", "pol": "neg", "text": "Is the question left unanswered by the paper?"},
]
QA_ANS_CARDS = {
    ("aff", "one_line"): "- yes: The paper's text (including its tables and captions) contains the answer.\n- no: "
                         "The paper does not contain the answer; related discussion does not count.",
    ("neg", "one_line"): "- yes: The paper does not contain the answer; related discussion does not count.\n- no: "
                         "The paper's text (including its tables and captions) contains the answer.",
    ("aff", "rubric"): "Look for the specific information the question asks for (a dataset, number, method detail or "
                       "result). Answer yes if the paper states it. Answer no if the paper never states it, even if "
                       "it discusses the topic.",
    ("neg", "rubric"): "Look for the specific information the question asks for (a dataset, number, method detail or "
                       "result). Answer no if the paper states it. Answer yes if the paper never states it, even if "
                       "it discusses the topic.",
}
QA_YN_WORDINGS = [
    {"id": "qa_yn_w1", "pol": "aff", "text": "{question} Answer from the paper only."},
    {"id": "qa_yn_w2", "pol": "aff", "text": "Based on the paper, answer yes or no: {question}"},
    {"id": "qa_yn_w3", "pol": "aff", "text": "{question}"},
]
QA_YN_CARDS = {
    ("aff", "one_line"): "- yes: The paper shows that what the question asks is the case.\n- no: The paper shows it "
                         "is not the case.",
}
QA_SEC_WORDINGS = [
    {"id": "qa_sc_w1", "text": "Which section of the paper contains the evidence that answers the question?"},
    {"id": "qa_sc_w2", "text": "Where in the paper is the information needed to answer the question?"},
    {"id": "qa_sc_w3", "text": "To answer the question, which section would you read?"},
]
QA_SEC_CARDS = {
    "one_line": "Exactly one listed section holds the passage that answers the question.",
    "rubric": "Find the passage that answers the question, then pick the section it belongs to. A section that only "
              "mentions the topic is not the answer.",
}
QA_STYLES = [
    {"id": "qa_s1", "wrap": "Paper: {title}\n\n{body}\n\nQuestion: {question}"},
    {"id": "qa_s2", "wrap": "Question: {question}\n\n# {title}\n\n{body}"},
    {"id": "qa_s3", "wrap": "<paper title=\"{title}\">\n{body}\n</paper>\n\nQuestion: {question}"},
]


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
                    out.append({"id": f"{name}:{x.get('id', i)}", "kind": name, **{k: v for k, v in x.items() if k != 'id'}})
                else:
                    out.append({"id": f"{name}:{i}", "kind": name, "text": x})
        elif isinstance(val, dict):
            for k, v in val.items():
                key = k if isinstance(k, str) else "|".join(map(str, k))
                out.append({"id": f"{name}:{key}", "kind": name, "text": v})
    return out
