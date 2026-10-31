# Haiku REDO-2 task T19-redo2-packs-000 (family T19, kind author_pack): 2 item(s), 2 candidates each

Read this whole file. It is the only file you may open: do not open, list, search or write any other file or folder. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/transfer/T19/haiku/redo2/answers/T19-redo2-packs-000.json

## Answer contract (exact)

The answer file holds ONE JSON array with exactly 2 object(s), one per item below, every qid exactly once (any order). Each object has exactly two keys: "qid" (the item's qid, copied exactly) and "packs" (a list of exactly 2 different pack objects: 2 alternative candidates for that item, each complete on its own and each following every rule below; inside a string write \n for a line break and \" for a double quote).
Valid JSON only: no text before or after the array, no comments, no code fence, no other keys.

Literal example of the required shape:

[
  {"qid": "q157273b52e", "packs": [{"sites": [...], "auditors": [...], "controls": [...]}, {"sites": [...], "auditors": [...], "controls": [...]}]},
  ...
]

How the candidates are used: a program checks each candidate against the rules below in the order you wrote them and keeps the first one that meets every check; the others are thrown away. So every candidate must follow every rule, and the candidates of one item must be clearly different from each other.

## Instructions

You invent "packs": the made-up setting of one invented organisation whose sites get a routine records review. A program later builds reading puzzles from your packs; you never see the puzzles. Each item gives a short brief (the kind of organisation). Write 2 alternative packs per item.

A pack is a JSON object with exactly these three keys:
- "sites": 4 different site names of this organisation. Each is 2-4 words: an invented place or street name with capital letters, then a plain lower-case word for the kind of place, for example "Larch Street depot", "Corran Yard", "Fellside campus", "Ridgeway branch". Letters, spaces, hyphens and apostrophes only.
- "auditors": 4 different invented person names, a first name and a family name, each word capitalised (for example "Priya Raman").
- "controls": 8 different routine checks the organisation runs at its sites, each 2-4 lower-case words that name the check itself (for example "fire drill", "badge audit", "backup restore test", "key rotation", "visitor log audit"). Letters and spaces only.

Word rules for every name (a program rejects a pack that breaks one):
1. No digits, no number words or ordinals (one, two, first, second, half, double, single, dozen ...).
2. A site name never uses any of these words: office, warehouse, store, data, centre, center, cloud, hybrid, premises, public, internal, personal, payment (they are reserved for the site's profile).
3. No word that judges or reports a state or an outcome: approved, valid, invalid, failed, failure, success, complete, completed, done, finished, pending, open, closed, active, late, current, missing, verified, confirmed, accepted, rejected, resolved, settled, outstanding, breached, ok, okay, fine, clean, in order, up to date, on track, at risk, problem, issue, concern, finding.
4. No word about time or frequency: daily, weekly, monthly, yearly, annual, annually, morning, evening, night, early, last, next, new, old, now, today.
5. No negative word: not, no, non, never, none, without, nothing, lack, un- words such as "unlocked".
6. No modal or quantity word: may, must, can, will, should, need, able, all, every, each, any, some, both, only, more, most, many, few, extra, total, whole, full, maximum, minimum, main, general.
7. Person names are never ordinary English words (no "Will", "May", "Hope", "Grace", "Summer", "Joy").
8. Invent everything: no real company, brand, product, town, street or famous person, and none of the example names above. No name of a pack may contain another name of the same pack.

Answer: follow the answer contract at the top of this file (2 packs per item, each complete on its own and each following every rule). Use \n for line breaks inside a text. Every pack must differ clearly from every other pack you write, also from the other packs of the same item (not one word swapped).

## Redo note

REDO NOTE (added for this redo; every rule above still holds). Earlier packs for the items below were thrown away by the program's word check. Write completely new packs. Causes to avoid:
- A routine-check name with a status word ("block") or a quantity word ("bulk"), and a check name with a capital letter (an abbreviation such as "ID"). Check names are 2-4 lower-case words, letters and spaces only, no abbreviation.
- Reserved words. The check throws away a pack whose names use any of these words (any letter case):
  - number words: billion, dozen, dozens, eight, eighteen, eighth, eighty, eleven, fifteen, fifth, fifty, first, five, forty, four, fourteen, fourth, half, hundred, million, nine, nineteen, ninety, ninth, one, second, seven, seventeen, seventh, seventy, six, sixteen, sixth, sixty, ten, tenth, third, thirteen, thirty, thousand, three, thrice, twelve, twenty, twice, two, zero
  - time words: afternoon, afterwards, ago, already, annually, asap, currently, daily, earlier, evening, formerly, hourly, immediately, last, lately, later, midday, midnight, monthly, morning, next, night, noon, now, overnight, past, previously, recently, shortly, soon, today, tomorrow, tonight, upcoming, weekend, weekly, yearly, yesterday, yet
  - quantity words: additional, another, bulk, bunch, couple, double, entire, entirely, extra, few, fewer, fewest, handful, least, less, lots, majority, many, maximum, minimum, minority, more, most, much, multiple, numerous, pair, partial, partially, percent, percentage, plenty, quarter, several, single, total, triple, various, whole
  - quantifiers: all, always, any, anybody, anyone, anything, both, each, either, every, everybody, everyone, everything, neither, never, no, nobody, none, nothing, often, only, rarely, seldom, some, somebody, someone, something, sometimes, usually, whenever
  - modal words: able, allowed, can, cannot, could, forbidden, gotta, mandatory, may, might, must, mustn, need, needed, needs, optional, ought, permitted, prohibited, required, shall, should, shouldn, unable, will, would
  - hedges: allegedly, almost, apparently, appear, appeared, appears, approximately, assume, assumed, assumes, believe, guess, likely, maybe, nearly, perhaps, possibly, presumably, probably, reportedly, roughly, seem, seemed, seemingly, seems, somewhat, supposedly, suspect, think, uncertain, unlikely, unsure
  - status words: accept, accepted, active, allow, allowed, approval, approve, approved, authorised, authorized, block, blocked, breached, broken, cancel, canceled, cancelled, closed, complete, completed, confirm, confirmation, confirmed, delivered, denial, denied, deny, done, eligibility, eligible, entitled, expire, failure, fake, finished, fraud, fraudulent, genuine, grant, granted, inactive, ineligible, invalid, kept, late, legitimate, ok, okay, open, opened, outstanding, paid, pending, processed, queued, refund, refunded, reject, rejected, resolved, revoke, revoked, settled, succeeded, success, successful, successfully, superseded, unauthorised, unauthorized, unpaid, unresolved, unverified, valid, verified, void, waive, waived
  - condition words: except, excluding, if, instead, otherwise, provided, providing, regardless, unless
  - in site names also the profile words: center, centre, cloud, data, hybrid, internal, office, payment, personal, premise, premises, public, store, warehouse, on-premises, on
  - by meaning: any word built on "comply"; the verbs "apply", "cover", "expire" and "lapse" in any form; the verb for not succeeding, in any form; the verb for succeeding at a test or for handing something along to someone, in any form (write "hand over" or "hand to"); the noun for a hole or a missing piece, and its plural; the word for being behind a time limit (over + due); and the word "non"
- No negative word or prefix in any name (no "non", "un-" words). Before you write the file, read every text once more, word by word, against the rules and this note.

## Items (2; one JSON object per line)

```json
[
{"qid": "q157273b52e", "brief": "An invented organisation: a dairy cooperative. Invent its site names, its review staff and the routine checks it runs at its sites, to fit it."},
{"qid": "q672c66b1fd", "brief": "An invented organisation: a print works. Invent its site names, its review staff and the routine checks it runs at its sites, to fit it."}
]
```
