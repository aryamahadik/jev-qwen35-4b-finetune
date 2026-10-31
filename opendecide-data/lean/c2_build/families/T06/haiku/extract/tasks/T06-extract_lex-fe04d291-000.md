# T06 extraction task T06-extract_lex-fe04d291-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T06/haiku/extract/answers/T06-extract_lex-fe04d291-000.json

Task: extract_lex; glex-r2; items: 32; outputs expected: 32.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder. Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file, with the Write tool. Inside JSON strings, write a double quote as \" and a line break as \n.

TASK: READ EACH TEXT ALONE and pick the ONE MEANING from the CLOSED LIST that the text expresses. Each item gives a TEXT:
one short store notice or one question about a returns case, with its values already filled in.

Rules:
1. Use only the TEXT and the CLOSED LIST. Do not guess beyond the words, and do not add a condition, a default or any
   fact from outside the text.
2. Copy the chosen meaning exactly, character for character, from the CLOSED LIST. Never write a new meaning.
3. Judge each text on its own words, not on the other items or on the order of the list.
4. Answer every item exactly once.

Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "meaning": "<the chosen meaning, copied exactly>"}, ...]
Copy each qid exactly.

CLOSED LIST (one meaning per line; copy one of these exactly):
- the store promises a full refund on some returns
- the store refuses every return and every refund: all sales are final
- the store refuses returns and refunds of personalised or custom-made items and says nothing about other items
- the store takes returns only for store credit or an exchange and never pays money back

ITEMS (JSON; answer every item, keyed by its qid):
```json
[
 {
  "qid": "q2a130fdbd7",
  "text": "We swap returned items for store credit or an exchange only, and never pay money back."
 },
 {
  "qid": "q21e9d11c39",
  "text": "All items sold are final: nothing is accepted back, and no cash is paid out in any situation."
 },
 {
  "qid": "q66af733b9a",
  "text": "Sales here are final, with nothing taken back and no money paid out."
 },
 {
  "qid": "q867136f1d2",
  "text": "Custom-made and personalised items are excluded from returns and refunds."
 },
 {
  "qid": "qfe32fcb3de",
  "text": "Personalised or custom-made products cannot be returned or refunded."
 },
 {
  "qid": "q116beac48d",
  "text": "Every sale is final. We take nothing back and pay no money back in any case."
 },
 {
  "qid": "q20c7f40c31",
  "text": "Personalised or custom-made items cannot be returned. They also cannot be refunded."
 },
 {
  "qid": "qeb964fc994",
  "text": "In every case, each sale is final. We neither take items back nor pay out any money."
 },
 {
  "qid": "qa6c179190d",
  "text": "Items you send back are swapped only for store credit or an exchange, never for money."
 },
 {
  "qid": "q521a4886c2",
  "text": "Personalised or custom-made items cannot be returned. They cannot be refunded either."
 },
 {
  "qid": "qd9c2ed9748",
  "text": "On any sale you cannot send anything back, and no money is paid out, in any case."
 },
 {
  "qid": "q42f41ebfdb",
  "text": "Personalised or custom-made items: neither returns nor refunds are possible."
 },
 {
  "qid": "q629833b710",
  "text": "Returned items are swapped for store credit or an exchange only. We never pay money back on them."
 },
 {
  "qid": "q43b405dfcc",
  "text": "Every sale is final. We take nothing back and pay no money back to you."
 },
 {
  "qid": "q53443c22c7",
  "text": "Returns: store credit or exchange only, never cash back."
 },
 {
  "qid": "q680bb2f001",
  "text": "You cannot return or be refunded for personalised or custom-made items."
 },
 {
  "qid": "qad63d9bbde",
  "text": "Return an item and you are given store credit or an exchange only, never cash."
 },
 {
  "qid": "q27c626d78d",
  "text": "Returned items are swapped for store credit or an exchange only, and we never pay money back."
 },
 {
  "qid": "qd04daca9c3",
  "text": "Sales are final: the store takes nothing back and pays no money back, in any case."
 },
 {
  "qid": "q97f5e16876",
  "text": "Sales are final in every case: nothing taken back, no money paid back."
 },
 {
  "qid": "qb355bd4dd8",
  "text": "We cannot take back or refund personalised or custom-made items."
 },
 {
  "qid": "qb21d40b262",
  "text": "Personalised or custom-made items are never taken back or refunded."
 },
 {
  "qid": "q3030d72ddd",
  "text": "Returns are handled with store credit or an exchange only. We never send money back to you."
 },
 {
  "qid": "q321a7e1b14",
  "text": "Every sale is final. We take nothing back and pay no money back, in any case."
 },
 {
  "qid": "q8e50461c7c",
  "text": "Personalised items: no returns and no refunds."
 },
 {
  "qid": "q20d7f0bd1e",
  "text": "We swap returns for store credit or an exchange only, never paying money back."
 },
 {
  "qid": "q7d51b987a4",
  "text": "Custom-made or personalised items cannot be returned or refunded."
 },
 {
  "qid": "q5e91e71be0",
  "text": "Anything we take back is replaced with store credit or an exchange only, and no cash is ever paid out."
 },
 {
  "qid": "qe53b2d9cd9",
  "text": "No sale can be returned, and we pay no money back, in any case."
 },
 {
  "qid": "qa9edee1d39",
  "text": "Returned items are swapped for store credit or an exchange only, with no money paid back."
 },
 {
  "qid": "qc2ee3ac9a4",
  "text": "Every sale is final, so nothing is taken back and no money is paid back in any case."
 },
 {
  "qid": "q19ad4be5e9",
  "text": "For a returned item, you are offered store credit or an exchange only, and we never pay money back."
 }
]
```
