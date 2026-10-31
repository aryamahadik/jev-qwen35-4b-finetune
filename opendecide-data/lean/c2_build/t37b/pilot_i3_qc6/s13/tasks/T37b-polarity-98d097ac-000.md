# T37b polarity judgement T37b-polarity-98d097ac-000 (family T37b)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i3_qc6/s13/answers/T37b-polarity-98d097ac-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 24. Answers expected: 24 (one per item, each with that item's qid).

## Instructions

Each item holds two yes/no questions, question_a and question_b, that will be asked about the same text with the same definitions. Reply 'same' if a correct yes to question_a always goes with a correct yes to question_b and a correct no with a correct no; 'opposite' if a correct yes to one always goes with a correct no to the other; 'unclear' if neither holds for certain or a question is ungrammatical. Reply with JSON: a list of objects {"qid": <qid>, "relation": "same" | "opposite" | "unclear"}.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "relation": "same" | "opposite" | "unclear"}. Exactly the keys qid and relation. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "qd96d20c3ef",
  "question_a": "Does the evidence support the claim?",
  "question_b": "Does the evidence fail to support the claim?"
 },
 {
  "qid": "q84fd337f2c",
  "question_a": "Does the assistant's reply confirm that the booking the customer asked for was actually made?",
  "question_b": "Does the assistant's reply fail to confirm that the booking the customer asked for was actually made?"
 },
 {
  "qid": "qbc7ae6cbea",
  "question_a": "Is this post hateful?",
  "question_b": "Is it right to say that this post isn't hateful?"
 },
 {
  "qid": "q9c52131a46",
  "question_a": "Of these two statements, does Statement 2 go against common sense?",
  "question_b": "Is it the case that, of these two statements, Statement 2 doesn't go against common sense?"
 },
 {
  "qid": "qf5bb52e551",
  "question_a": "Is the action being judged acceptable according to common social norms?",
  "question_b": "Is it the case that the action being judged isn't acceptable according to common social norms?"
 },
 {
  "qid": "q25c9bee000",
  "question_a": "According to the assistant's last message, is \"tomorrow\" confirmed for the customer's car repair appointment?",
  "question_b": "Would it be correct to say that, according to the assistant's last message, \"tomorrow\" is not confirmed for the customer's car repair appointment?"
 },
 {
  "qid": "qc1b1ef1beb",
  "question_a": "Does this paragraph make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "question_b": "Is it true that this paragraph doesn't make the contrarian climate claim that climate science or the climate movement is unreliable?"
 },
 {
  "qid": "q437bb3361d",
  "question_a": "Is the statement supported by the table?",
  "question_b": "Is the statement contradicted by the table?"
 },
 {
  "qid": "q07b38cd601",
  "question_a": "Is the statement supported by the table?",
  "question_b": "Is it true that the statement is not supported by the table?"
 },
 {
  "qid": "q7dfedd54f7",
  "question_a": "Does the evidence contradict the claim?",
  "question_b": "Does the evidence fail to contradict the claim?"
 },
 {
  "qid": "qb5f2758392",
  "question_a": "Is the statement supported by the table?",
  "question_b": "Would it be correct to say that the statement isn't supported by the table?"
 },
 {
  "qid": "q323d0f04be",
  "question_a": "Is the statement supported by the table?",
  "question_b": "Is it correct that the statement is not supported by the table?"
 },
 {
  "qid": "q55b06860be",
  "question_a": "Of these two statements, does Statement 2 go against common sense?",
  "question_b": "Of these two statements, does Statement 1 go against common sense?"
 },
 {
  "qid": "q2483427bd4",
  "question_a": "Does this paragraph make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "question_b": "Is it accurate to say that this paragraph doesn't make the contrarian climate claim that climate science or the climate movement is unreliable?"
 },
 {
  "qid": "qff6fb32f66",
  "question_a": "Is the action being judged wrong according to common social norms?",
  "question_b": "Is the action being judged acceptable according to common social norms?"
 },
 {
  "qid": "q60e284712a",
  "question_a": "Is the action being judged acceptable according to common social norms?",
  "question_b": "Is the action being judged wrong according to common social norms?"
 },
 {
  "qid": "q66c556e290",
  "question_a": "Of these two statements, does Statement 1 go against common sense?",
  "question_b": "Is it true that, of these two statements, Statement 1 doesn't go against common sense?"
 },
 {
  "qid": "q0dd3a59b5f",
  "question_a": "Of these two statements, does Statement 1 go against common sense?",
  "question_b": "Of these two statements, does Statement 2 go against common sense?"
 },
 {
  "qid": "qcbc1b6f4aa",
  "question_a": "Is the action being judged wrong according to common social norms?",
  "question_b": "Is the action being judged okay according to common social norms?"
 },
 {
  "qid": "q4f3dd4e60d",
  "question_a": "By the end of this conversation, has the customer actually bought movie tickets?",
  "question_b": "Is it true that, by the end of this conversation, the customer has not actually bought movie tickets?"
 },
 {
  "qid": "qaea8cc197e",
  "question_a": "Of these two statements, does Statement 2 go against common sense?",
  "question_b": "Of these two statements, does Statement 2 agree with common sense?"
 },
 {
  "qid": "qe602dff2de",
  "question_a": "Is the statement supported by the table?",
  "question_b": "Is it correct that the statement isn't supported by the table?"
 },
 {
  "qid": "qec7cca25ba",
  "question_a": "Does this vehicle safety complaint report that the vehicle was actually involved in a crash?",
  "question_b": "Does this vehicle safety complaint fail to report that the vehicle was actually involved in a crash?"
 },
 {
  "qid": "qd6b077bcaf",
  "question_a": "Does this vehicle safety complaint report that the vehicle actually caught fire?",
  "question_b": "Is it right to say that this vehicle safety complaint does not report that the vehicle actually caught fire?"
 }
]
