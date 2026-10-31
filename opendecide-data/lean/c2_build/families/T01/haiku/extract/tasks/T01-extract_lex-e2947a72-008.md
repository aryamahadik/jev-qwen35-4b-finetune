# T01 extraction task T01-extract_lex-e2947a72-008

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T01/haiku/extract/answers/T01-extract_lex-e2947a72-008.json

Task kind: extract_lex; read: glex-r2; items: 25; outputs expected: 25.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder. Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file, with the Write tool. Inside JSON strings, write a double quote as \" and a line break as \n.

TASK: READ EACH TEXT ALONE and pick the ONE CHOICE whose meaning the text expresses. Each item gives a TEXT (a short
question, a rule clause or a comparison phrase, with its values already filled in) and CHOICES (a list of meanings).

Rules:
1. Use only the TEXT and its CHOICES. Do not guess beyond the words, and do not add a condition, a default or any
   fact from outside the text.
2. Copy the chosen CHOICE exactly, character for character, from that item's own list. Never write a new meaning.
3. Answer every item exactly once.

Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "meaning": "<the chosen choice, copied exactly>"}, ...]
Copy each qid exactly.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "q4e9a251e40",
  "text": "greater than $0.01",
  "choices": [
   "less than or equal to the bound",
   "strictly less than the bound",
   "greater than or equal to the bound",
   "strictly greater than the bound"
  ]
 },
 {
  "qid": "qb5369602b7",
  "text": "Does the cash rule let the day in ledger call_7f3a close without a cash report?",
  "choices": [
   "asks for the first date on which a loss would be covered",
   "asks whether the loss is covered",
   "asks whether the purchase request does not need written quotes",
   "asks whether the response counts as received on time",
   "asks on which date the office counts the response as received",
   "asks for the due date of the response under the response rule",
   "asks for the last date on which the filing is still in time",
   "asks whether the person failed to file in time, that is, filed after the final day",
   "asks whether the filing was made in time",
   "asks whether a cash report is required for the day",
   "asks whether the filing was made late, after the final day",
   "asks whether the person is over the stay limit in the checked period",
   "asks whether the rule lets the day close without a cash report",
   "asks how many days present fall inside the checked period",
   "asks whether the loss is not covered",
   "asks whether the filing was not made in time",
   "asks whether the loss happened during the waiting period",
   "asks whether the person is within the stay limit (at most the limit) in the checked period",
   "asks whether the rule lets the purchase request go ahead without written quotes",
   "asks whether the person is not over the stay limit in the checked period",
   "asks whether the response counts as received late, after the due date",
   "asks whether the purchase request needs written quotes",
   "asks for the total the purchase rule compares with its threshold, new request included",
   "asks whether the response was not on time",
   "asks which of the day's totals call for a cash report",
   "asks whether no cash report is required for the day"
  ]
 },
 {
  "qid": "q4eb04bb868",
  "text": "Would the purchase rule let log call_7f3a proceed without written quotes?",
  "choices": [
   "asks whether no cash report is required for the day",
   "asks whether a cash report is required for the day",
   "asks for the total the purchase rule compares with its threshold, new request included",
   "asks for the last date on which the filing is still in time",
   "asks whether the response counts as received late, after the due date",
   "asks which of the day's totals call for a cash report",
   "asks whether the person is within the stay limit (at most the limit) in the checked period",
   "asks whether the purchase request needs written quotes",
   "asks whether the loss happened during the waiting period",
   "asks for the due date of the response under the response rule",
   "asks whether the person failed to file in time, that is, filed after the final day",
   "asks whether the filing was made in time",
   "asks how many days present fall inside the checked period",
   "asks whether the filing was not made in time",
   "asks whether the rule lets the purchase request go ahead without written quotes",
   "asks whether the filing was made late, after the final day",
   "asks whether the loss is not covered",
   "asks on which date the office counts the response as received",
   "asks whether the person is over the stay limit in the checked period",
   "asks whether the person is not over the stay limit in the checked period",
   "asks whether the rule lets the day close without a cash report",
   "asks whether the purchase request does not need written quotes",
   "asks whether the response counts as received on time",
   "asks whether the response was not on time",
   "asks whether the loss is covered",
   "asks for the first date on which a loss would be covered"
  ]
 },
 {
  "qid": "q51a0d1e55a",
  "text": "inside 7 days counted from the later of these dates",
  "choices": [
   "a period counted from the later of two dates",
   "a cap on the days present in each calendar year",
   "a waiting period whose first day is its start date",
   "a waiting period whose first day is the day after its start date",
   "a cap on the days present in every rolling period of the stated length",
   "a period counted from the earlier of two dates"
  ]
 },
 {
  "qid": "q61e95f5254",
  "text": "What total for Brightwell Supply is compared with the threshold when a new request is included in that total under the purchase rule?",
  "choices": [
   "asks whether the response counts as received on time",
   "asks whether the rule lets the purchase request go ahead without written quotes",
   "asks whether the person is over the stay limit in the checked period",
   "asks whether the rule lets the day close without a cash report",
   "asks which of the day's totals call for a cash report",
   "asks whether the purchase request does not need written quotes",
   "asks for the last date on which the filing is still in time",
   "asks whether the filing was made in time",
   "asks for the due date of the response under the response rule",
   "asks whether the person failed to file in time, that is, filed after the final day",
   "asks whether the purchase request needs written quotes",
   "asks whether the filing was made late, after the final day",
   "asks whether the person is not over the stay limit in the checked period",
   "asks whether the loss is not covered",
   "asks how many days present fall inside the checked period",
   "asks whether the loss is covered",
   "asks whether the loss happened during the waiting period",
   "asks for the total the purchase rule compares with its threshold, new request included",
   "asks whether no cash report is required for the day",
   "asks whether the filing was not made in time",
   "asks whether the person is within the stay limit (at most the limit) in the checked period",
   "asks whether a cash report is required for the day",
   "asks for the first date on which a loss would be covered",
   "asks whether the response counts as received late, after the due date",
   "asks on which date the office counts the response as received",
   "asks whether the response was not on time"
  ]
 },
 {
  "qid": "q470464ad9b",
  "text": "According to the rule card, is it true that no cash report is required for 28 February 2026 in the ledger of Brightwell Supply?",
  "choices": [
   "asks for the total the purchase rule compares with its threshold, new request included",
   "asks whether the person failed to file in time, that is, filed after the final day",
   "asks whether the loss happened during the waiting period",
   "asks whether the person is over the stay limit in the checked period",
   "asks whether the loss is covered",
   "asks whether the person is not over the stay limit in the checked period",
   "asks whether the person is within the stay limit (at most the limit) in the checked period",
   "asks which of the day's totals call for a cash report",
   "asks whether a cash report is required for the day",
   "asks on which date the office counts the response as received",
   "asks whether the loss is not covered",
   "asks whether the filing was made in time",
   "asks whether the response counts as received on time",
   "asks whether the purchase request needs written quotes",
   "asks whether the response counts as received late, after the due date",
   "asks whether the filing was not made in time",
   "asks for the due date of the response under the response rule",
   "asks whether the purchase request does not need written quotes",
   "asks whether no cash report is required for the day",
   "asks how many days present fall inside the checked period",
   "asks for the last date on which the filing is still in time",
   "asks whether the response was not on time",
   "asks for the first date on which a loss would be covered",
   "asks whether the rule lets the purchase request go ahead without written quotes",
   "asks whether the rule lets the day close without a cash report",
   "asks whether the filing was made late, after the final day"
  ]
 },
 {
  "qid": "q9a2e85782f",
  "text": "Is it allowed to close 28 February 2026 in ledger call_7f3a without a cash report under the cash rule?",
  "choices": [
   "asks for the due date of the response under the response rule",
   "asks which of the day's totals call for a cash report",
   "asks whether the rule lets the day close without a cash report",
   "asks whether the response counts as received late, after the due date",
   "asks on which date the office counts the response as received",
   "asks whether a cash report is required for the day",
   "asks for the first date on which a loss would be covered",
   "asks whether the loss is not covered",
   "asks whether the person is within the stay limit (at most the limit) in the checked period",
   "asks for the last date on which the filing is still in time",
   "asks whether the person failed to file in time, that is, filed after the final day",
   "asks whether the purchase request does not need written quotes",
   "asks whether the filing was made late, after the final day",
   "asks whether the person is not over the stay limit in the checked period",
   "asks whether no cash report is required for the day",
   "asks whether the response was not on time",
   "asks whether the filing was made in time",
   "asks for the total the purchase rule compares with its threshold, new request included",
   "asks how many days present fall inside the checked period",
   "asks whether the response counts as received on time",
   "asks whether the loss happened during the waiting period",
   "asks whether the person is over the stay limit in the checked period",
   "asks whether the filing was not made in time",
   "asks whether the purchase request needs written quotes",
   "asks whether the rule lets the purchase request go ahead without written quotes",
   "asks whether the loss is covered"
  ]
 },
 {
  "qid": "q3d5fc717e5",
  "text": "within 7 days counted forward from the later among these dates",
  "choices": [
   "a cap on the days present in each calendar year",
   "a waiting period whose first day is the day after its start date",
   "a waiting period whose first day is its start date",
   "a cap on the days present in every rolling period of the stated length",
   "a period counted from the earlier of two dates",
   "a period counted from the later of two dates"
  ]
 },
 {
  "qid": "q65bf769205",
  "text": "a figure of $0.01 or greater",
  "choices": [
   "strictly less than the bound",
   "greater than or equal to the bound",
   "strictly greater than the bound",
   "less than or equal to the bound"
  ]
 },
 {
  "qid": "q82dc21d9ca",
  "text": "any total of $0.01 or greater",
  "choices": [
   "greater than or equal to the bound",
   "strictly greater than the bound",
   "strictly less than the bound",
   "less than or equal to the bound"
  ]
 },
 {
  "qid": "q49f4c5f877",
  "text": "Is it true that the Dana Okafor in case call_7f3a was not filed in time under the filing rule?",
  "choices": [
   "asks how many days present fall inside the checked period",
   "asks for the last date on which the filing is still in time",
   "asks whether the person failed to file in time, that is, filed after the final day",
   "asks whether the rule lets the purchase request go ahead without written quotes",
   "asks which of the day's totals call for a cash report",
   "asks whether the response was not on time",
   "asks whether the person is within the stay limit (at most the limit) in the checked period",
   "asks whether the filing was not made in time",
   "asks whether the person is not over the stay limit in the checked period",
   "asks on which date the office counts the response as received",
   "asks for the due date of the response under the response rule",
   "asks for the total the purchase rule compares with its threshold, new request included",
   "asks whether the loss is covered",
   "asks whether the filing was made late, after the final day",
   "asks whether the response counts as received on time",
   "asks whether the purchase request does not need written quotes",
   "asks whether no cash report is required for the day",
   "asks whether a cash report is required for the day",
   "asks whether the loss happened during the waiting period",
   "asks whether the response counts as received late, after the due date",
   "asks whether the purchase request needs written quotes",
   "asks whether the rule lets the day close without a cash report",
   "asks whether the loss is not covered",
   "asks whether the person is over the stay limit in the checked period",
   "asks whether the filing was made in time",
   "asks for the first date on which a loss would be covered"
  ]
 },
 {
  "qid": "q3af4d8ebcf",
  "text": "any figure at or above $0.01",
  "choices": [
   "strictly greater than the bound",
   "greater than or equal to the bound",
   "less than or equal to the bound",
   "strictly less than the bound"
  ]
 },
 {
  "qid": "q5e23feeefb",
  "text": "According to the rule card, is a cash report required for 28 February 2026, the day under review in the ledger of Brightwell Supply?",
  "choices": [
   "asks whether the person is within the stay limit (at most the limit) in the checked period",
   "asks whether the response counts as received late, after the due date",
   "asks for the first date on which a loss would be covered",
   "asks whether the loss is covered",
   "asks for the total the purchase rule compares with its threshold, new request included",
   "asks whether the response was not on time",
   "asks whether the loss is not covered",
   "asks whether the person is not over the stay limit in the checked period",
   "asks how many days present fall inside the checked period",
   "asks whether the rule lets the day close without a cash report",
   "asks whether the purchase request needs written quotes",
   "asks whether a cash report is required for the day",
   "asks for the due date of the response under the response rule",
   "asks whether the response counts as received on time",
   "asks whether the filing was made late, after the final day",
   "asks which of the day's totals call for a cash report",
   "asks on which date the office counts the response as received",
   "asks whether the person is over the stay limit in the checked period",
   "asks whether no cash report is required for the day",
   "asks whether the purchase request does not need written quotes",
   "asks whether the person failed to file in time, that is, filed after the final day",
   "asks whether the loss happened during the waiting period",
   "asks whether the rule lets the purchase request go ahead without written quotes",
   "asks for the last date on which the filing is still in time",
   "asks whether the filing was not made in time",
   "asks whether the filing was made in time"
  ]
 },
 {
  "qid": "qb0739886fd",
  "text": "Must ledger call_7f3a include a cash report under the cash rule?",
  "choices": [
   "asks whether the purchase request does not need written quotes",
   "asks whether the person is within the stay limit (at most the limit) in the checked period",
   "asks whether the person failed to file in time, that is, filed after the final day",
   "asks whether the loss is not covered",
   "asks whether a cash report is required for the day",
   "asks whether no cash report is required for the day",
   "asks whether the filing was made late, after the final day",
   "asks how many days present fall inside the checked period",
   "asks for the total the purchase rule compares with its threshold, new request included",
   "asks for the last date on which the filing is still in time",
   "asks whether the response counts as received on time",
   "asks whether the filing was made in time",
   "asks whether the purchase request needs written quotes",
   "asks for the first date on which a loss would be covered",
   "asks whether the response counts as received late, after the due date",
   "asks for the due date of the response under the response rule",
   "asks on which date the office counts the response as received",
   "asks whether the filing was not made in time",
   "asks whether the person is over the stay limit in the checked period",
   "asks whether the rule lets the day close without a cash report",
   "asks whether the person is not over the stay limit in the checked period",
   "asks whether the response was not on time",
   "asks whether the loss happened during the waiting period",
   "asks whether the rule lets the purchase request go ahead without written quotes",
   "asks whether the loss is covered",
   "asks which of the day's totals call for a cash report"
  ]
 },
 {
  "qid": "q47f120395c",
  "text": "According to the rule card, is the person in record call_7f3a within the stay limit, with the limit itself counting as within?",
  "choices": [
   "asks how many days present fall inside the checked period",
   "asks whether the filing was not made in time",
   "asks whether the person is within the stay limit (at most the limit) in the checked period",
   "asks whether the filing was made late, after the final day",
   "asks whether the person is over the stay limit in the checked period",
   "asks for the due date of the response under the response rule",
   "asks which of the day's totals call for a cash report",
   "asks for the first date on which a loss would be covered",
   "asks whether the loss happened during the waiting period",
   "asks whether the person failed to file in time, that is, filed after the final day",
   "asks on which date the office counts the response as received",
   "asks whether the response counts as received on time",
   "asks whether the rule lets the purchase request go ahead without written quotes",
   "asks whether the person is not over the stay limit in the checked period",
   "asks whether no cash report is required for the day",
   "asks for the total the purchase rule compares with its threshold, new request included",
   "asks whether the purchase request does not need written quotes",
   "asks for the last date on which the filing is still in time",
   "asks whether the purchase request needs written quotes",
   "asks whether the rule lets the day close without a cash report",
   "asks whether the filing was made in time",
   "asks whether the loss is covered",
   "asks whether the response was not on time",
   "asks whether the loss is not covered",
   "asks whether the response counts as received late, after the due date",
   "asks whether a cash report is required for the day"
  ]
 },
 {
  "qid": "qcf60ef275f",
  "text": "equal to or above $0.01",
  "choices": [
   "greater than or equal to the bound",
   "strictly less than the bound",
   "strictly greater than the bound",
   "less than or equal to the bound"
  ]
 },
 {
  "qid": "qf57318221b",
  "text": "Is Dana Okafor, under the stay rule, over the stay limit for the window ending on 29 February 2028?",
  "choices": [
   "asks whether a cash report is required for the day",
   "asks for the last date on which the filing is still in time",
   "asks whether the response counts as received late, after the due date",
   "asks on which date the office counts the response as received",
   "asks whether the person failed to file in time, that is, filed after the final day",
   "asks whether the rule lets the purchase request go ahead without written quotes",
   "asks for the due date of the response under the response rule",
   "asks whether no cash report is required for the day",
   "asks whether the loss is covered",
   "asks whether the purchase request needs written quotes",
   "asks whether the filing was made in time",
   "asks for the first date on which a loss would be covered",
   "asks whether the person is within the stay limit (at most the limit) in the checked period",
   "asks whether the filing was made late, after the final day",
   "asks whether the response counts as received on time",
   "asks which of the day's totals call for a cash report",
   "asks whether the filing was not made in time",
   "asks whether the loss happened during the waiting period",
   "asks whether the loss is not covered",
   "asks whether the person is not over the stay limit in the checked period",
   "asks whether the person is over the stay limit in the checked period",
   "asks whether the response was not on time",
   "asks how many days present fall inside the checked period",
   "asks whether the rule lets the day close without a cash report",
   "asks for the total the purchase rule compares with its threshold, new request included",
   "asks whether the purchase request does not need written quotes"
  ]
 },
 {
  "qid": "qcc8d668f96",
  "text": "a waiting period of 7 days counted from the day after its start date",
  "choices": [
   "a cap on the days present in every rolling period of the stated length",
   "a cap on the days present in each calendar year",
   "a waiting period whose first day is the day after its start date",
   "a period counted from the earlier of two dates",
   "a period counted from the later of two dates",
   "a waiting period whose first day is its start date"
  ]
 },
 {
  "qid": "q8e48d7ab84",
  "text": "Under the card's rule, did the Dana Okafor for case call_7f3a fail to be lodged by the deadline?",
  "choices": [
   "asks whether the response counts as received late, after the due date",
   "asks which of the day's totals call for a cash report",
   "asks for the last date on which the filing is still in time",
   "asks whether the person is within the stay limit (at most the limit) in the checked period",
   "asks whether the response was not on time",
   "asks for the total the purchase rule compares with its threshold, new request included",
   "asks whether the filing was made late, after the final day",
   "asks whether a cash report is required for the day",
   "asks whether the loss is covered",
   "asks whether the filing was not made in time",
   "asks whether the response counts as received on time",
   "asks how many days present fall inside the checked period",
   "asks for the due date of the response under the response rule",
   "asks whether the filing was made in time",
   "asks whether no cash report is required for the day",
   "asks whether the purchase request does not need written quotes",
   "asks whether the rule lets the day close without a cash report",
   "asks on which date the office counts the response as received",
   "asks whether the person failed to file in time, that is, filed after the final day",
   "asks for the first date on which a loss would be covered",
   "asks whether the purchase request needs written quotes",
   "asks whether the loss happened during the waiting period",
   "asks whether the loss is not covered",
   "asks whether the person is over the stay limit in the checked period",
   "asks whether the person is not over the stay limit in the checked period",
   "asks whether the rule lets the purchase request go ahead without written quotes"
  ]
 },
 {
  "qid": "q1471168d35",
  "text": "According to the rule card, on which date does the office count the response to notice call_7f3a as received under the receipt rule?",
  "choices": [
   "asks whether the loss is not covered",
   "asks whether the loss happened during the waiting period",
   "asks for the total the purchase rule compares with its threshold, new request included",
   "asks whether the person is within the stay limit (at most the limit) in the checked period",
   "asks whether the loss is covered",
   "asks whether the rule lets the day close without a cash report",
   "asks whether the filing was made in time",
   "asks whether the filing was not made in time",
   "asks whether no cash report is required for the day",
   "asks whether the response counts as received late, after the due date",
   "asks for the last date on which the filing is still in time",
   "asks whether the person is over the stay limit in the checked period",
   "asks whether the response counts as received on time",
   "asks whether the rule lets the purchase request go ahead without written quotes",
   "asks whether a cash report is required for the day",
   "asks whether the person is not over the stay limit in the checked period",
   "asks which of the day's totals call for a cash report",
   "asks whether the purchase request needs written quotes",
   "asks whether the response was not on time",
   "asks for the due date of the response under the response rule",
   "asks whether the purchase request does not need written quotes",
   "asks whether the filing was made late, after the final day",
   "asks for the first date on which a loss would be covered",
   "asks how many days present fall inside the checked period",
   "asks on which date the office counts the response as received",
   "asks whether the person failed to file in time, that is, filed after the final day"
  ]
 },
 {
  "qid": "q121d833e97",
  "text": "Under the card's rule, was the Dana Okafor in case call_7f3a filed in time, on or before the final day?",
  "choices": [
   "asks whether the filing was made late, after the final day",
   "asks whether the person is not over the stay limit in the checked period",
   "asks for the due date of the response under the response rule",
   "asks whether the purchase request needs written quotes",
   "asks whether the filing was made in time",
   "asks whether a cash report is required for the day",
   "asks whether the loss happened during the waiting period",
   "asks for the last date on which the filing is still in time",
   "asks how many days present fall inside the checked period",
   "asks whether the person is within the stay limit (at most the limit) in the checked period",
   "asks for the total the purchase rule compares with its threshold, new request included",
   "asks whether the filing was not made in time",
   "asks whether the purchase request does not need written quotes",
   "asks whether the response was not on time",
   "asks whether the person failed to file in time, that is, filed after the final day",
   "asks whether the loss is not covered",
   "asks whether the person is over the stay limit in the checked period",
   "asks whether the rule lets the purchase request go ahead without written quotes",
   "asks whether the response counts as received late, after the due date",
   "asks whether the response counts as received on time",
   "asks on which date the office counts the response as received",
   "asks whether the rule lets the day close without a cash report",
   "asks whether the loss is covered",
   "asks for the first date on which a loss would be covered",
   "asks whether no cash report is required for the day",
   "asks which of the day's totals call for a cash report"
  ]
 },
 {
  "qid": "q3d4febe7a8",
  "text": "According to the rule card, what is the latest date on which the Brightwell Supply can be filed in time?",
  "choices": [
   "asks whether the purchase request does not need written quotes",
   "asks for the total the purchase rule compares with its threshold, new request included",
   "asks whether the person is not over the stay limit in the checked period",
   "asks whether the loss is covered",
   "asks for the last date on which the filing is still in time",
   "asks whether the filing was made in time",
   "asks whether the rule lets the day close without a cash report",
   "asks whether the filing was not made in time",
   "asks whether no cash report is required for the day",
   "asks whether the purchase request needs written quotes",
   "asks whether the response counts as received on time",
   "asks whether the person failed to file in time, that is, filed after the final day",
   "asks on which date the office counts the response as received",
   "asks whether the response was not on time",
   "asks whether the loss happened during the waiting period",
   "asks whether the person is within the stay limit (at most the limit) in the checked period",
   "asks which of the day's totals call for a cash report",
   "asks whether the loss is not covered",
   "asks whether the response counts as received late, after the due date",
   "asks for the first date on which a loss would be covered",
   "asks whether the filing was made late, after the final day",
   "asks for the due date of the response under the response rule",
   "asks whether a cash report is required for the day",
   "asks how many days present fall inside the checked period",
   "asks whether the person is over the stay limit in the checked period",
   "asks whether the rule lets the purchase request go ahead without written quotes"
  ]
 },
 {
  "qid": "q6d682c9291",
  "text": "Under the card's rule, how many days present for Brightwell Supply fall inside the checked window ending on the reference date?",
  "choices": [
   "asks how many days present fall inside the checked period",
   "asks whether the response counts as received late, after the due date",
   "asks whether the response counts as received on time",
   "asks whether the loss happened during the waiting period",
   "asks whether the person is within the stay limit (at most the limit) in the checked period",
   "asks whether the purchase request needs written quotes",
   "asks whether no cash report is required for the day",
   "asks for the first date on which a loss would be covered",
   "asks whether the filing was made late, after the final day",
   "asks whether the rule lets the purchase request go ahead without written quotes",
   "asks whether a cash report is required for the day",
   "asks whether the response was not on time",
   "asks whether the loss is covered",
   "asks for the last date on which the filing is still in time",
   "asks whether the person failed to file in time, that is, filed after the final day",
   "asks whether the filing was not made in time",
   "asks which of the day's totals call for a cash report",
   "asks whether the purchase request does not need written quotes",
   "asks whether the filing was made in time",
   "asks whether the loss is not covered",
   "asks for the total the purchase rule compares with its threshold, new request included",
   "asks on which date the office counts the response as received",
   "asks whether the person is over the stay limit in the checked period",
   "asks whether the person is not over the stay limit in the checked period",
   "asks for the due date of the response under the response rule",
   "asks whether the rule lets the day close without a cash report"
  ]
 },
 {
  "qid": "q3c4aedd2d0",
  "text": "anything strictly greater than $0.01",
  "choices": [
   "strictly greater than the bound",
   "less than or equal to the bound",
   "strictly less than the bound",
   "greater than or equal to the bound"
  ]
 },
 {
  "qid": "q14c44f5c90",
  "text": "Going by the record, is it true that Brightwell Supply did not file the Dana Okafor for case call_7f3a in time?",
  "choices": [
   "asks whether the filing was made in time",
   "asks whether the loss happened during the waiting period",
   "asks whether the purchase request needs written quotes",
   "asks whether the loss is covered",
   "asks whether the response counts as received on time",
   "asks on which date the office counts the response as received",
   "asks whether a cash report is required for the day",
   "asks whether the rule lets the day close without a cash report",
   "asks which of the day's totals call for a cash report",
   "asks for the last date on which the filing is still in time",
   "asks for the first date on which a loss would be covered",
   "asks whether the filing was not made in time",
   "asks whether the filing was made late, after the final day",
   "asks whether the response was not on time",
   "asks whether the person is over the stay limit in the checked period",
   "asks whether the loss is not covered",
   "asks whether the person failed to file in time, that is, filed after the final day",
   "asks for the due date of the response under the response rule",
   "asks whether the person is not over the stay limit in the checked period",
   "asks whether no cash report is required for the day",
   "asks for the total the purchase rule compares with its threshold, new request included",
   "asks whether the response counts as received late, after the due date",
   "asks how many days present fall inside the checked period",
   "asks whether the rule lets the purchase request go ahead without written quotes",
   "asks whether the purchase request does not need written quotes",
   "asks whether the person is within the stay limit (at most the limit) in the checked period"
  ]
 }
]
