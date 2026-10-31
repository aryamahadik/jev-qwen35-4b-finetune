# G0-lite R00: expense auto-approval (kit reference family; never written, never trained)

One page, as C2_DATA_SPEC 6.2 item 3 asks: a semantics table, one ambiguity listing, one resolution, then frozen.
R00 exists to show the format and to test the kit; it is not one of the 17 C2 families.

## 1. Semantics table

| # | Item | Semantics (exact) |
|---|---|---|
| S1 | Facts | employee (name), expense id (id), category (closed set: travel; catering = meals; software), amount (integer cents, USD, `$`), limit (integer cents), comparator clause (lexicon sem `cmp.le` or `cmp.lt`, bound = the limit), window N (count of days, N in {7, 14, 30, 45, 60, 90}; S5: {10, 21}), purchase date, receipt date, filing date (dates, no time of day) |
| S2 | Printed intermediate | days from purchase to filing = filing date - purchase date, in whole days (always printed in the record block) |
| S3 | Amount test | `cmp.le`: amount <= limit. `cmp.lt`: amount < limit. Equality is decisive: at `cmp.le` an amount equal to the limit passes |
| S4 | Window test | the purchase date is day 0; the claim passes when its day number (S2) is <= N. Day N passes, day N + 1 fails |
| S5 | Decision | auto-approved iff S3 and S4 both pass; otherwise manual review. Closed world: "The record is complete: no other rule or fact applies." |
| S6 | Receipt date | narrative only; never an anchor. Reading it as the anchor is the error model `wrong_anchor` |
| S7 | yn_approved | yes iff auto-approved |
| S8 | yn_review (antonym complement of S7) | yes iff manual review |
| S9 | yn_not_approved (syntactic complement of S7) | yes iff not auto-approved |
| S10 | ch_outcome | options {Auto-approved, Manual review} (closed set, card order shuffled by row key) |
| S11 | ch_deadline | gold = purchase date + N days (the last day that passes S4). Options: gold + outputs of `count_day0` (P + N - 1), `off_by_one_late` (P + N + 1), `wrong_anchor` (receipt + N, only when receipt != purchase); k = 4, else 3 |
| S12 | Rule sentence (program text) | "Expense rule: an expense is auto-approved when both of these hold: its amount is {CMP}, and the claim is filed at most {N_DAYS} after the purchase date (count the purchase date as day 0). Any other expense goes to manual review. The record is complete: no other rule or fact applies." |
| S13 | Record block (program text) | "Expense record {ID}:" then the lines "- amount:", "- purchase date:", "- claim filed:", "- days from purchase to filing:" |
| S14 | Skins | Mode T skins declare EMPLOYEE, CATEGORY and RECEIPT_DATE (they may repeat any record fact, which must then read the same). Mode F skins carry those three facts verbatim; G3-H extracts them |
| S15 | Error models | ignore_window, ignore_amount, add_exclusive_endpoint (cmp.lt read as cmp.le), drop_inclusive_endpoint (cmp.le read as cmp.lt), wrong_anchor, count_day0, off_by_one_late |
| S16 | Depth | 2 unstated operations (amount test, window test); the day count is printed |
| S17 | Relations | complement on every yn_approved row (antonym 60%, syntactic 40%); minimal-edit twin on amount (to limit + 1 / limit / limit - 1 as the comparator needs) or filing date (to day N or N + 1); equiv into another register; inv with one attack line; G4: rename employee, change category, shift every date by 7 days (deadline shifts by 7) |
| S18 | Solvers | A: rule AST (rules.And / Cmp / Fn days_between) via rules.evaluate. B: enumerate the window day by day and test membership; integer-cents difference table for the comparator; its own question table |

## 2. Ambiguity listing (one pass)

1. "at most N days after the purchase date": does day N count? (S4: yes; the card says day 0 is the purchase date.)
2. "below $X" at an amount of exactly $X? (S3: fails; `cmp.lt` is strict.)
3. Could the receipt date be read as the start of the window? (S6: never; it is the `wrong_anchor` error model.)
4. "{X} or less" vs "less than {X}": two different sems; the lexicon unit test proves no text matches both.

## 3. Resolution

All four are fixed by S3, S4 and S6 as written, and the card states each rule in the rule sentence (S12). Frozen;
the sha256 is R00.G0_SHA256 in r00.py, and validate_plugin() refuses the plugin if this file changes.
