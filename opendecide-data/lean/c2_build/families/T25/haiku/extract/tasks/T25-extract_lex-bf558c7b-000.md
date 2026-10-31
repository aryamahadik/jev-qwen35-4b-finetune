# Haiku G-LEX extraction task T25-extract_lex-bf558c7b-000 (family T25, read1, blind meaning pick)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T25/haiku/extract/answers/T25-extract_lex-bf558c7b-000.json

The answer is one JSON object with exactly 50 keys, one per item below: each key is that item's qid, and each value is the meaning you copied from the closed list.

## Instructions

You name the meaning of short English question lines. Read your task file, which is one Markdown file: it holds these instructions, a closed list of meanings, and a JSON list of items. Each item has an opaque 'qid' and a 'text' (one question line, with any placeholder already filled in). For every item, read its text and pick the ONE meaning in the closed list that the question asks. Copy that meaning exactly as written, character for character. Judge each text on its own words, not on the other items or on the order of the list. Write ONE JSON object to the answer file that your instructions name: its keys are the qid values of ALL items in your task file, and each value is the copied meaning (a string). Valid JSON only: double quotes, no comments, no trailing commas. Do not open any other file.

CLOSED LIST (one meaning per line):
- asks whether the claimed value fails to equal the value the rule settles on, by one negation
- asks whether the claimed value equals the value the rule settles on
- asks whether the claimed value differs from the value the rule settles on, by an antonym
- asks, with two negations, whether the claimed value equals the value the rule settles on
- asks whether the rule settles on a value other than the claimed one
- asks which single source sets the attribute under the rule, or that none does
- asks which value of the attribute the rule settles on, or that it is not determinable


## Items (50; one JSON object per line)

```json
[
{"qid": "q47d2e4630c", "text": "Which of the listed sources does the value for the exhibition closing date come from under the stated rules?"},
{"qid": "q63f1ccc30a", "text": "Applying the stated rules to these sources, which value does the fact end up with?"},
{"qid": "qf6e1115dff", "text": "Applying the stated rules to these sources, which value do they settle on for the fact?"},
{"qid": "qaf830b429e", "text": "Which value for the term start date is settled by the listed sources under the stated rules?"},
{"qid": "q862433bf2f", "text": "According to the rules given, what value for the registration fee is settled by the listed sources?"},
{"qid": "q58a2807dde", "text": "According to the rules given, which listed source do they take the value of the parcel collection window from?"},
{"qid": "q60605732ab", "text": "Under the stated rules, which listed source should the minimum visitor age value be taken from?"},
{"qid": "q5e8d33c32f", "text": "Going by the listed sources, which source do the stated rules draw the value from?"},
{"qid": "q625ee3f81d", "text": "According to the rules given, what value of the advance booking window comes out from the listed sources?"},
{"qid": "q9017103570", "text": "Going by the listed sources, from which source do the stated rules draw the value of the fact?"},
{"qid": "q0f0543bd48", "text": "Going by the listed sources, what value of the fact is fixed by the stated rules?"},
{"qid": "q6c2059873e", "text": "Going by the listed sources, what does the fact come to under the stated rules?"},
{"qid": "q54be4ca598", "text": "According to the rules given, which value of the late return fee do the listed sources settle on?"},
{"qid": "q4abac777dd", "text": "Going by the listed sources, which value of the fact do the stated rules settle on?"},
{"qid": "q49106a1a65", "text": "Applying the stated rules to these sources, which source do they take the fact's value from?"},
{"qid": "q2886e916d1", "text": "Under the stated rules, which value of the consultation fee do the listed sources land on?"},
{"qid": "q1b8745cbd0", "text": "Under the stated rules, which value for the minimum mooring term is settled from the listed sources?"},
{"qid": "q00b6a8ff75", "text": "According to the rules given, from which listed source is the value of the swim course start date taken?"},
{"qid": "q246173fea7", "text": "Under the stated rules, which of the listed sources sets the hire period value?"},
{"qid": "qbeae99a51c", "text": "Which value do the listed sources settle on for the fact, according to the stated rules?"},
{"qid": "qf94a1220e0", "text": "Applying the stated rules to these sources, which listed source does the settled value come from?"},
{"qid": "qe48f7ad1cc", "text": "According to the rules given, which listed source supplies the value for the season opening date?"},
{"qid": "q2836b5daa6", "text": "What value for the swim course start date do the listed sources yield under the rules given?"},
{"qid": "qb7913ea4fe", "text": "Going by the listed sources, which value do the stated rules settle on for this fact?"},
{"qid": "q16b3e2ea7f", "text": "According to the rules given, which value for the arrival date is settled from the listed sources?"},
{"qid": "qbb5cceb7bb", "text": "Which value for the parcel allowance do the listed sources settle on under the stated rules?"},
{"qid": "qac00ed683f", "text": "Under the stated rules, what is the settled value of the desk rental fee from the listed sources?"},
{"qid": "q663bfa847e", "text": "Applying the stated rules to these sources, which value of the fact do the rules settle on?"},
{"qid": "q5db65dba4c", "text": "Applying the stated rules to these sources, which value for the fact do the rules settle on?"},
{"qid": "q362463eb64", "text": "Applying the stated rules to these sources, from which listed source is the fact's value taken?"},
{"qid": "qf355b75ffe", "text": "Judging by these sources, which value would the stated rules settle on for the fact?"},
{"qid": "q05cdb995d5", "text": "According to the rules given, what settled value for the warranty period comes out of the listed sources?"},
{"qid": "q1fcd6d81a9", "text": "Under the stated rules, which listed source supplies the value for the table fee?"},
{"qid": "q9cb84f35ac", "text": "Which value of the arrival date is settled by the listed sources under the stated rules?"},
{"qid": "q9ae32b3955", "text": "Under the stated rules, at which value do the listed sources settle the late return fee?"},
{"qid": "q54d7c64667", "text": "Which listed source do the stated rules take the value of this fact from?"},
{"qid": "q5a1e076982", "text": "Looking at the listed sources, which value does the fact settle on under the stated rules?"},
{"qid": "q9478d4f0ef", "text": "Which listed source is the value for the warranty period taken from under the stated rules?"},
{"qid": "q0da7fa1d91", "text": "Applying the stated rules to these sources, what value of the fact comes out as the settled answer?"},
{"qid": "qdd4110d8f3", "text": "Going by the listed sources, which of them do the stated rules take the fact's value from?"},
{"qid": "q59b4129f79", "text": "Under the stated rules, which listed source does the cancellation period value come from?"},
{"qid": "qd57accb5bd", "text": "Which listed source do the stated rules draw the fact's value from?"},
{"qid": "q808d16452c", "text": "What value of the fact do the stated rules settle on from the listed sources?"},
{"qid": "q2257ceb462", "text": "Applying the stated rules to these sources, what value comes out as the settled answer for the fact?"},
{"qid": "q81629b2253", "text": "Which of the listed sources provides the camera hire price value, according to the rules given?"},
{"qid": "q0055359db7", "text": "Going by the listed sources, which value of the fact is settled under the stated rules?"},
{"qid": "qf2047469f2", "text": "Going by the listed sources, which source do the stated rules take the fact's value from?"},
{"qid": "q1f86e51a11", "text": "Under the stated rules, what value of the custom cake deposit is settled by the listed sources?"},
{"qid": "qf93c7ec1c0", "text": "Which of the listed sources do the stated rules rely on for the value of this fact?"},
{"qid": "qd746306747", "text": "Going by the listed sources, what value do the stated rules settle on for the fact?"}
]
```
