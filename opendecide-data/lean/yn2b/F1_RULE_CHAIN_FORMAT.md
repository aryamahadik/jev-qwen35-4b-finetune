# F1 `gen3_rule_chain`: the rendered text, for the independent decide2

Input for agent E (SPEC 8.1: `golden_src/gen3/v3_rule_chain.py`, `decide2_row(raw_row) -> "yes" | "no" | option`).
It describes only what a row shows. It does not describe how the generator decides. Every rule a reader needs is
printed in each document's own General clauses. Rows are in `data/v14_parts/yn2b_raw/gen3_rule_chain.jsonl` (train)
and `.../dev/gen3_rule_chain.jsonl`. A row's card is `data/v14_parts/yn2b_defs/gen3_rule_chain__<meta.defs>.json`.

## 1. Row types

`meta.pack` names the row type:

| `meta.pack` | Part | What it is |
|---|---|---|
| `a_<family>` | F1a | A rule document plus a case file |
| `nb_<pack>` | F1b | A numeric claim check |

**F1a families:** municipal_fee, leave_handbook, warranty_returns, shipping_tariff, pharmacy_formulary,
grant_eligibility, data_retention, it_change, hoa_bylaws, and school_transport (dev only). Their nouns, flags and
outcome texts are in `golden_src/gen3/rc_skins.py`. That file holds only the vocabulary, with no logic.

**Other meta fields:**
- `meta.renderer` is the document style: code, handbook, faq, table or contract (dev only).
- `meta.fmt` is the case-file format: json, markdown, kv, prose, email, `log:<order>` or `table:<layout>`.
- `meta.qkind` is yn, choice or jb.
- `meta.tpl` is the question template.

## 2. F1a documents

### Clause labels

| Style | Clause label | Reference in text |
|---|---|---|
| code | `p.i` | `section p.i` |
| contract | `p.i` | `clause p.i` |
| handbook | `Rule k.` | `Rule k` |
| faq | `Qk.` (a question) then `Ak.` | `answer k` |
| table | `Ck.` | `Ck` |

In the table style, the category limits are a grid under the heading `Table 1 - Category limits`.

### Format details

- **One clause per line.** Section headings carry no rules.
- **json format.** The document is the list `document`, one line per item. The case file is the object `case`, and
  `correspondence` holds the attack plants.
- **Other formats.** The document comes first. The case file follows a blank line and a heading: `Case file`,
  `Case summary`, `Correspondence` (email) or `Case log`.

### Two wordings

Train documents and dev_iid documents use the train wording. dev_holdout documents use the held-out wording. Both
wordings state the same rules. The pairs (train → held-out) are:

| Clause | Train wording | Held-out wording |
|---|---|---|
| Counting rule | "Periods in this X are counted in calendar days: …" | "All periods in this X run in calendar days; …" |
| Holidays | "The public holidays for this X are D1, D2 and D3." | "This X treats these dates as public holidays: …" |
| Order of grounds | "If more than one ground for refusal applies …, the ground stated first … is the one recorded." | "… the ground that appears first … is the one entered." |
| Missing facts | "A fact that the case file does not show is treated as not established …" | "Anything the case file does not show counts as not established …" |
| Precedence | "Where the general limit and a category limit both apply …, the category limit prevails." / "… the one that appears later in this X prevails." / "… the lower of the two applies." | "If both … cover …, the category limit takes priority." / "… the one placed later … takes priority." / "… the smaller limit is used." |
| Named precedence | "Where A and B both set a limit for …, B prevails." | "If A and B both set a limit for …, B takes priority." |
| Definition | `"Term" means <subject> is <cmp>.` | `In this X, "Term" refers to <subject> is <cmp>.` |
| Eligibility via a term | `<def_req>.` | `<def_req>, and in no other case.` |
| Eligibility, direct | "<grant_vp> only if <elig noun> is <cmp>." | "… only where …" |
| Time requirement | "The <req> must be received <time phrase>." | "Each <req> has to arrive <time phrase>." |
| Documents | "The <req> must include <docs>." | "Each <req> has to come with <docs>." |
| Waiver exception | "<Ref> does not apply[ to <cats>][ if <conds>]." | "<Ref> is set aside[ for <cats>][ where <conds>]." |
| Period exception | "[For <cats>,][ If <conds>,] the period in <ref> is N [business ]days instead." | "… where … becomes N days." |
| Exception to an exception | Same form as the waiver exception | Same form as the waiver exception |
| Exclusion | "<deny_vp>[ for <cats>] if <conds>." | "… where <conds>." |
| Amendment | `Amendment k, in force from D: in <ref>, "old" is replaced by "new".` | `Amendment k (starting D) changes <ref> so that "old" becomes "new".` |
| Amendment of a table row | "… the limit for <cats> changes from A to B" | "… the limit for <cats> goes from A to B" |
| Withdrawn amendment | `Amendment k, which was to come into force on D, was withdrawn before that date; in <ref>, … under it.` | `Amendment k was withdrawn before its planned start on D; it would have changed <ref> so that ….` |
| General limit | "<Benefit> may not be more than A for one <req>." | "<Benefit> is capped at A for each <req>." |
| Category limits | "The category limits are: <cats>, A; <cats>, B." | "Category limits apply as follows: <cats> at A; …" |

The contract style says "shall" where the others say "must" or "has to".

**How to tell an exception from an exception to an exception.** Both read "<Ref> does not apply …". The clause is an
exception to an exception when <Ref> points at an exception.

**Distractors that never apply:**
- `Former provision, repealed with effect from D and no longer in force: "…"`
- `Repealed on D and kept for reference only: "…"`
- A requirement written "For a <other request type>, the <req> must also include …". The case's request type is
  always the entitlement's type, so this requirement never applies to it.
- Procedure sentences.
- Unused definitions.

### Exact phrasings

- **cmp:** "at least N u", "more than N u", "at most N u" or "less than N u". N may be a decimal.
- **Time phrase, documents due before the event:** "at least|more than N [business ]days before <event>".
- **Time phrase, documents due after the event:** "no later than|before the Nth [business ]day after <event>".
- **conds:** atoms joined by " and ". Each atom is either:
  - a flag's positive phrase; or
  - "<amount noun> is at least|more than|at most|less than A".
- **cats:** category plural labels joined by ", " and " and ".

## 3. The rules as the documents state them

- **Counting.** Day counts are calendar or business days. Business days are Monday to Friday minus the listed
  holidays.
  - "N days before X" is the date N (business) days before X.
  - "the Nth day after X" is the date N (business) days after X.
  - "at least" and "no later than" include that date. "more than … before" and "before the Nth day after" exclude it.
- **Exceptions.** An exception applies only to the clause it names, and only when every condition holds and no
  exception to it applies.
  - A category list ("to/for <cats>") is a condition: the case's category must be one of them.
  - A waiver exception makes the named requirement or exclusion not apply.
  - A period exception replaces the named time requirement's period.
- **Amendments.**
  - An amendment applies to requests received on or after its date.
  - A withdrawn amendment never applies.
  - When several amendments change one figure, the latest one in force on the received date counts.
- **Missing facts.** A fact the case file does not show is not established. A document not shown as included is not
  included.
- **Outcome.**
  - A requirement that fails gives that requirement's refusal outcome.
  - An exclusion that applies gives the exclusion outcome.
  - Otherwise the request is granted. It is cut to the limit that applies when the amount requested is more than that
    limit (PARTIAL); otherwise it is granted in full (FULL).
  - The limit is the general limit and/or the row of the case's category in the category limits. When both exist,
    the precedence rule picks one.
  - Rows never have two refusal grounds at once.

### The six outcome kinds

Each family's own outcome texts for these kinds are in `rc_skins.SKINS[family]["outcomes"]`.

| Kind | What happened |
|---|---|
| INELIG | The eligibility requirement fails |
| LATE | The time requirement fails |
| DOCS | The document requirement fails |
| EXCL | An exclusion applies |
| PARTIAL | Granted, cut to the limit |
| FULL | Granted in full |

### Case-file fields

- Reference.
- The person, by role.
- Category: the singular label.
- Request type.
- The eligibility figure.
- The event date.
- Received: the date the request was received.
- The document field: included or not included. It is absent when the document is not shown.
- Every flag: yes or no.
- The amount requested.
- Optional: "Decision recorded: <outcome text>" on judge rows.
- Optional: a "Linked file …" line. This is a separate case and is never used.

Dates are written as 2026-03-14, 14 March 2026 or March 14, 2026. In the log format, the received date is a
`received: …` line.

The prose case file states the same facts as sentences:
- Train wording: "The expected attendance is 240 people." and "The application was received on …".
- Held-out wording: "The file gives … as …" and "It is recorded that …".

## 4. Questions

| Row | Question | Answer |
|---|---|---|
| yn `pos*` / `jdg*` | Is the outcome "X"? / Is the recorded decision consistent with, supported by, or in line with the document? | yes iff the outcome is X, or the recorded decision equals the outcome |
| yn `inv*` / `jinv1` | The same proposition, negated ("different from", "at odds with") | The inverse |
| choice `out*` / `mir_*` | The outcome | The option equal to the outcome's text. "None of the outcomes listed" when it is absent |
| choice `dec*` | The clause whose deletion alone changes the outcome | Options are "<Ref> (<what>)". "None of the clauses listed" when that clause is not among them |
| choice `amt*` | Ascending ranges | The range that holds the amount granted |
| jb | `jbq1` / `jbj1`: the two options are the proposition and its negation. `jbf1` / `jbjf1`: the options are "yes, this holds" / "no, this does not hold" | The true option |

**The amount granted:**
- FULL: the amount requested.
- PARTIAL: the limit.
- Refusals never get amount questions.

**Attack rows** (`meta.view == "attack"`) carry an untrusted note:
- in the json `correspondence` list;
- as one more email;
- as a markdown `Correspondence` section; or
- as "Note attached to the file by …" at the end.

The note never changes the answer.

## 5. F1b claims

**Evidence lines:**
- "As of D, <source> reported <figure>[ for the first|second period][ for <entity>]."
- "On D, <source> revised that figure from A to B." Only the latest revision of a figure counts.

**Where the claim is:**

| Format | Claim | Fact-check log (judge rows) |
|---|---|---|
| json | key `claim` | key `fact_check_log`, which is null otherwise |
| kv | `claim` | `fact_check_log` |
| prose / log | "Claim: …" | "Fact-check log entry: …" |
| markdown | `## Claim` section | a `## Fact-check log` section |

**Claim forms:**

| Kind | Claim | Figure compared |
|---|---|---|
| threshold | "<Subject>[ as of D] was at least \| more than \| at most \| less than C." | The figure as of D: the latest report on or before D |
| unit | Same as threshold, with C in the converted unit | The figure times the card's factor ("For this check, 1 tonne = 1,000 kilograms.") |
| about | "<Subject>[ as of D] was about C." | True iff \|figure − C\| ≤ the tolerance in the card ("within T of N, counting both ends") |
| pct | "<Subject> rose \| fell by at least … P% from the first period to the second period." | (second − first) / first × 100, with the sign of rose / fell |
| difference | "<E1> had at least … C more … than <E2>." | E1 − E2 |
| sum | "Taken together, <E1> and <E2> had at least … C …" | E1 + E2 |

**Rules that apply to every claim:**
- Figures are used exactly as printed, with no rounding.
- The card holds every rule that applies.

**Questions:**
- `bpos*`: yes iff the claim holds.
- `binv1`: the inverse.
- `bjdg*`: yes iff the log entry (SUPPORTED or NOT SUPPORTED) matches the truth.
- `bjinv1`: the inverse.
