"""SEM card line registry (G0 3.2 meanings, 3.3 renderings). Variant "a" carries the 3.2 card column text; variant "b"
is a second wording of the same meaning (same operator words). Placeholders: {etype} {S} {D_start} {D_end} {q} {m}
{attr} {values} {item} {pos} {neg}. The card parser (parse.py) reads the same registry file, frozen by sha256.

Topic names (the defs entry name) are fixed per key.
"""
from __future__ import annotations

import hashlib
import json

TOPIC = {
    "SEM-01": "Answer convention", "SEM-02": "Complete record", "SEM-03": "Incomplete record",
    "SEM-04": "Missing values", "SEM-05": "unless", "SEM-06": "only if", "SEM-07": "if ... then",
    "SEM-08": "Numeric bounds", "SEM-09": "half", "SEM-10": "or, nor, both", "SEM-11": "Dates", "SEM-12": "Rounding",
    "SEM-13": "Ties", "SEM-14": "Units", "SEM-15": "Exceptions on rules", "SEM-16": "Corrections",
    "SEM-17": "Value sets", "SEM-18": "Two-state words", "SEM-19": "Failure and absence words",
    "SEM-20": "Statements and authority", "SEM-22": "Quantifiers", "SEM-23": "only, other than, all except",
    "SEM-24": "Duties and permissions", "SEM-25": "Graded words", "SEM-26": "never, no longer, still",
    "SEM-27": "Covered period", "SEM-28": "not only ... but also", "SEM-31": "Thread messages", "SEM-33": "Log states",
}

A = {
    "SEM-01": 'Answer Yes if the statement in the question, read exactly as worded (every "not" and every negative word '
              'included), is true of the case; otherwise answer No.',
    "SEM-02": 'The record is complete. It names every {etype} in the case, gives every number, date and category detail '
              'of each of them or marks it not recorded, and lists every statement each party made. A positive '
              'statement that the record does not state, and that no rule makes true, is false: it did not happen and '
              'does not hold. A statement made negative by "not" or by a negative prefix (non-, un-, in-, dis-) holds '
              'exactly when its positive form (the same statement with that negation taken out) does not hold. A '
              'statement it does not list was not made. The one exception is a value the record marks as not '
              'recorded: it has some value the record does not give.',
    "SEM-03": 'The record may be incomplete about facts and events. It names every {etype} in the case; only facts '
              'about them may be missing. Something it does not state, and that does not follow from what it states '
              'and the rules, is unknown, not false.',
    "SEM-04": 'An entry marked "not recorded" (or null) has some value that the record does not give, on a complete '
              'record too: nothing in the record makes a statement about that value true or false. On a record that '
              'may be incomplete, a blank entry means the same. On a complete record, a blank yes/no entry means no.',
    "SEM-05": '"A unless B" means: when B is false, A holds. When B is true, this sentence neither makes A hold nor '
              'makes it fail.',
    "SEM-06": '"A only if B" means A does not hold when B is false. B being true does not by itself make A hold.',
    "SEM-07": '"If B, then A" means B is enough for A; so if A is false, B is false. It says nothing about A when B is '
              'false. The conditions of a rule are the parts of its "if" clause joined by "and"; an "unless" or '
              '"except when" part is not a condition. A condition is met when what it says is true of the case, so a '
              'condition written with "not" or another negative word is met when the thing it denies is false. "At '
              'least q of the conditions of a rule" means at least q of them are met.',
    "SEM-08": 'N itself counts for "at least N", "no fewer than N", "not less than N", "N or more", "reaches N" or '
              '"meets N", and likewise for "at most N", "no more than N", "not more than N" or "up to N". N itself '
              'does not count for "more than N", "over N", "above N" or "exceeds N", nor for "fewer than N", '
              '"less than N", "under N" or "below N". '
              '"Between N1 and N2" includes both. "Exactly N" means equal to N.',
    "SEM-09": '"At least half" includes exactly half. "More than half" does not.',
    "SEM-10": '"Or" means at least one, possibly both. "Either A or B, but not both" means exactly one. "Neither A nor '
              'B" means both are false. "Not both A and B" means at least one is false.',
    "SEM-11": 'Each date is a whole calendar day. "On D" means that day. "Before D" and "after D" exclude D. "On or '
              'before D", "by D", "no later than D" and "not after D" include D. "On or after D", "no earlier than D" '
              'and "not before D" include D; these four negated phrases are date words like "on or before" and "on or '
              'after", not a "not" over a statement. "Between D1 and D2", "from D1 to D2" and "D1 through D2" include '
              'both dates. "In" a month or a year means any day of that month or year. "N days after D" means the Nth '
              'day after D (1 day after D is the next day). "Within N days after D" means from the day after D '
              'through the Nth day after D. "As of D" means at the end of D, counting every entry dated D. A date '
              'range in a question about an event asks whether at least one such event falls on some day of the '
              'range; one is enough. A "not" over such a statement means that no such event falls on a day of the '
              'range. A date range in a question about a single date asks whether that date falls on some day of the '
              'range.',
    "SEM-12": 'Values are compared exactly as written. Nothing is rounded.',
    "SEM-14": 'Every quantity is given with its unit. Questions compare only quantities in the same unit.',
    "SEM-15": 'An exception attached to a rule ("unless B", "except when B") means the rule does not apply when B '
              'holds. It does not make the opposite outcome hold; another rule may still give the outcome. No two '
              'rules in this record give opposite outcomes for the same case.',
    "SEM-16": 'Entries with no named author are records by {S}. Each CORRECTION or VOID names one entry by its own '
              'author. A CORRECTION replaces a value in the entry it names (a holder, a status, a number of days or a '
              'stated value), as if that entry had always said the corrected value; the corrected entry keeps its own '
              'date, its kind and its item. A VOID cancels the entry it names: treat it as never written. Both apply '
              'whatever their own date, also to times before it. Voiding a CORRECTION restores the entry it corrected. '
              'Only entries by {S} make facts true, so a CORRECTION or VOID by anyone else changes no fact; it '
              'changes only what its author stated.',
    "SEM-17": 'Each {etype} has exactly one {attr} at a time, one of: {values}.',
    "SEM-17L": 'An {item} has no {attr} before the first entry that sets it; from that entry\'s date on, it has exactly '
               'one {attr} at a time, one of: {values}.',
    "SEM-18": '"{pos}" has two states only: "{neg}" means exactly "not {pos}".',
    "SEM-19": '"Failed to", "neglected to", "omitted to" and "did not manage to" do X, with no "by D", mean X did not '
              'happen on any day of the period the record covers, wherever the phrase appears (a dated log entry, a '
              'sentence or a question) and whatever the entry\'s own date; they do not say whether X was required. '
              '"Failed to do X by D" means X did not happen on any day from the start of the covered period through D. '
              '"Refused to do X", "declined to do X" and "was prevented from doing X" mean X did not happen on any day '
              'of the period the record covers. "Managed to do X" means X happened. "Lacks Z", "is without Z" and "is '
              'free of Z" mean does not have Z.',
    "SEM-20": 'Statements by {S} are true. Statements by anyone else are only claims: they make nothing true or false. '
              '"X denied that P" and "X ruled out P" mean X stated that P is false. "X confirmed P" means X stated that '
              'P is true. A question about what X stated asks about the latest remaining statement by X about P dated '
              'on or before the asked day; "latest" means the latest date. A statement about P is one that states P or '
              'states that P is false. A VOID or retraction by X of one of its own statements removes that statement, '
              'and a CORRECTION or correction by X replaces what that statement says, as if it had always said that, '
              'whatever the date of the VOID or correction. Nobody else can change what X stated.',
    "SEM-22": 'Quantifiers range over the members of the named group, and the record names every member. "Every" and '
              '"all" mean each member, with no exception. Every group named in a question has at least one member. '
              '"Some" means at least one, possibly all. A direct question "Did any A ...?" asks whether at least one A '
              'did. "No A", "none of the A" and "not any A" mean zero. "Not every A" and "not all A" mean at least one '
              'A does not.',
    "SEM-23": 'The group is exactly the group the question names. "Only A did X" means A did X and no other member of '
              'the group did X. "Did anyone other than A do X?" and "someone other than A did X" are about whether at '
              'least one member of the group other than A did X; the status of A does not matter. "All except A" means '
              'every member of the group other than A did it, and A did not.',
    "SEM-24": '"Must" and "is required to" mean required. "Must not", "may not", "is not permitted to" and "cannot" '
              'mean not permitted. "Need not", "does not have to" and "is not required to" mean not required; they say '
              'nothing about whether it is permitted. "May" and "is permitted to" mean permitted. The rules listed are '
              'all the rules about these actions: an action that no listed rule forbids for the case is permitted, and '
              'an action that no listed rule requires for the case is not required. This line decides whether an '
              'action is required or permitted, on complete and incomplete records alike, ahead of the line on whether '
              'the record is complete. In a table of roles and actions, "required" means the role must do the action '
              '(so it is also permitted), "permitted" means the role may do it and need not, and "forbidden" means the '
              'role must not do it; each cell holds in every case, and no other rule is about a role and action that '
              'the table lists.',
    "SEM-25": '"Hardly any", "scarcely any" and "few" X mean fewer than {q} X. "E barely met T" means the value of E '
              'was at least T and no more than {m} above T. "E barely stayed within C" means the value of E was at '
              'most C and no more than {m} below C.',
    "SEM-26": 'In a question, "never" means on no day from the start of the period the record covers through the '
              'asked day; in the record, "never" means on no day of the covered period. "No longer" means held on '
              'some day before the asked day in that period and does not hold on the asked day. "Still" means held on '
              'some day before the asked day in that period and holds on the asked day. In a dated record entry, "no '
              'longer" and "still" refer to the entry\'s date in place of the asked day. An entry in the record that '
              'says something never happened, no longer holds or still holds is a statement by its author about the '
              'record: it sets no state and changes none.',
    "SEM-27": 'This record covers {D_start} to {D_end}, both included. A question with no stated time asks about the '
              'end of {D_end}. "As of D" in a question makes D the asked day.',
    "SEM-28": '"Not only A but also B" is true exactly when A is true and B is true as well.',
    "SEM-31": 'Only messages by {S} make facts true or false. Each retraction or correction names a message by its own '
              'sender. A retraction cancels the message it names, as if never sent. A correction replaces the value in '
              'the message it names, as if that message had always said it; the corrected message keeps its own date. '
              'Retractions and corrections apply whatever their own date, and they are not themselves messages about '
              'the fact. Of the remaining messages by {S} about one fact, the latest one counts; "latest" means the '
              'latest date. A retraction or correction by another party changes only what that party stated.',
    "SEM-33": 'Each item has three separate states: its holder, its status and whether it is valid. An entry takes '
              'effect on its date and counts for that date. A creation or a transfer sets the holder, a status entry '
              'sets the status, and a "renewed for N days" or "valid for N days" entry sets validity; no entry changes '
              'any other state. A state set by an entry holds from the date of that entry through the day before the '
              'next entry that changes the same state. "Renewed for N days" or "valid for N days" dated D makes the '
              'item valid from D through its last valid day, the Nth day after D; this replaces any last valid day set '
              'by an entry dated before D, even one further on, and no other kind of entry moves the last valid day. '
              'From the day after its last valid day the item has lapsed (it is not valid), and a renewal dated after '
              'that day makes it valid from the date of the renewal. A lapse changes neither the holder nor the status.',
}

B = {
    "SEM-01": 'Read the statement in the question exactly as it is worded, with every "not" and every negative word. '
              'Answer Yes if that statement is true of the case; otherwise answer No.',
    "SEM-02": 'This record is complete: it names every {etype} in the case, gives each number, date and category '
              'detail or marks it not recorded, and lists every statement each party made. A positive statement that '
              'the record does not state, and that no rule makes true, is false: it did not happen and does not hold. '
              'A statement made negative by "not" or by a negative prefix (non-, un-, in-, dis-) holds exactly when '
              'its positive form (the statement with that negation taken out) does not hold. A statement not listed '
              'was not made. One exception: a value marked not recorded has some value that the record does not give.',
    "SEM-03": 'This record may be incomplete about facts and events, but it names every {etype} in the case, so only '
              'facts about them may be missing. Anything it does not state, and that does not follow from what it '
              'states and the rules, is unknown, not false.',
    "SEM-04": 'A value marked "not recorded" (or null) is some value that the record does not give, on a complete '
              'record too, so nothing in the record makes a statement about it true or false. On a record that may be '
              'incomplete, a blank entry means the same. On a complete record, a blank yes/no entry means no.',
    "SEM-05": 'In "A unless B": when B is false, A holds. When B is true, the sentence neither makes A hold nor makes '
              'it fail.',
    "SEM-06": 'In "A only if B": when B is false, A does not hold. B being true does not by itself make A hold.',
    "SEM-07": 'In "If B, then A", B is enough for A, so if A is false, B is false; when B is false, the rule says '
              'nothing about A. The conditions of a rule are the parts of its "if" clause joined by "and"; an "unless" '
              'or "except when" part is not a condition. A condition is met when what it says is true of the case, so '
              'a condition written with "not" or another negative word is met when the thing it denies is false. "At '
              'least q of the conditions of a rule" means at least q of them are met.',
    "SEM-08": 'These include N: "at least N", "no fewer than N", "not less than N", "N or more", "reaches N", "meets '
              'N", "at most N", "no more than N", "not more than N" and "up to N". These exclude N: "more than N", '
              '"over N", "above N", "exceeds N", "fewer than N", "less than N", "under N" and "below N". "Between N1 '
              'and N2" includes both. "Exactly N" means equal to N.',
    "SEM-09": '"At least half" includes exactly half; "more than half" does not.',
    "SEM-10": '"Or" means at least one, possibly both. "Either A or B, but not both" means exactly one. "Neither A nor '
              'B" means A is false and B is false. "Not both A and B" means at least one of them is false.',
    "SEM-12": 'Nothing is rounded: values are compared exactly as written.',
    "SEM-14": 'Each quantity is given with its unit, and questions compare only quantities in the same unit.',
    "SEM-15": 'An exception attached to a rule ("unless B", "except when B") means that rule does not apply when B '
              'holds. It does not make the opposite outcome hold, and another rule may still give the outcome. No two '
              'rules in this record give opposite outcomes for the same case.',
    "SEM-17": 'At any time each {etype} has exactly one {attr}, one of: {values}.',
    "SEM-18": '"{pos}" has two states only, and "{neg}" means exactly "not {pos}".',
    "SEM-22": 'Quantifiers range over the members of the named group, and the record names every member. "Every" and '
              '"all" mean each member, with no exception, and every group named in a question has at least one '
              'member. "Some" means at least one, possibly all. A direct question "Did any A ...?" asks whether at '
              'least one A did. "No A", "none of the A" and "not any A" mean zero. "Not every A" and "not all A" mean '
              'at least one A does not.',
    "SEM-27": 'The record covers {D_start} to {D_end}, both included. A question with no stated time asks about the '
              'end of {D_end}, and "as of D" in a question makes D the asked day.',
    "SEM-28": '"Not only A but also B" means that A is true and B is true.',
}

ORDER = ["SEM-01", "SEM-02", "SEM-03", "SEM-24", "SEM-04", "SEM-05", "SEM-06", "SEM-07", "SEM-15", "SEM-08", "SEM-09",
         "SEM-10", "SEM-11", "SEM-12", "SEM-14", "SEM-16", "SEM-17", "SEM-18", "SEM-19", "SEM-20", "SEM-22", "SEM-23",
         "SEM-25", "SEM-26", "SEM-27", "SEM-28", "SEM-31", "SEM-33"]


def rendering(key, variant, **kw):
    src = B if variant == "b" and key in B else A
    return src[key].format(**kw)


def registry():
    """The frozen rendering registry the card parser reads: {key: [template, ...]}."""
    reg = {}
    for k, v in A.items():
        reg.setdefault(k.replace("SEM-17L", "SEM-17"), []).append(v)
    for k, v in B.items():
        reg.setdefault(k, []).append(v)
    return reg


def registry_sha256():
    return hashlib.sha256(json.dumps(registry(), sort_keys=True).encode()).hexdigest()


# examples for the one-line + examples style (other entities of the pack, never the row's base; correct by SEM rules)
EXAMPLES = {
    "SEM-01": ['If {x} is {w}, the statement "{x} is not {w}" is false, so the answer is No.'],
    "SEM-08": ['A value of {n} {u} is at least {n} {u}, and it is not more than {n} {u}.'],
    "SEM-10": ['If {x} is {w} and is not {w2}, then "{x} is {w} or {w2}" is true.'],
    "SEM-12": ['A value written as {n} {u} is compared as {n} {u}.'],
    "SEM-14": ['A quantity in {u} is compared only with other quantities in {u}.'],
    "SEM-28": ['"{x} is not only {w} but also {w2}" is true only when {x} is {w} and {x} is {w2}.'],
    "SEM-18": ['If {x} is {w}, then "{x} is {neg}" is false.'],
}


# variant "c": compact wording of the same meanings (same operator phrases; every clause of A kept)
C = {
    "SEM-01": 'Answer Yes if the statement in the question, read exactly as worded with every "not" and every negative '
              'word, is true of the case; otherwise answer No.',
    "SEM-02": 'The record is complete: it names every {etype} in the case, gives every number, date and category detail '
              'of each or marks it not recorded, and lists every statement each party made. A positive statement '
              'that the record does not state and no rule makes true is false (it did not happen, it does not hold). '
              'A statement made negative by "not" or a negative prefix (non-, un-, in-, dis-) holds exactly when its '
              'positive form does not. An unlisted statement was not made. Exception: a value marked not recorded '
              'has some value the record does not give.',
    "SEM-03": 'The record may be incomplete about facts and events. It names every {etype} in the case; only facts '
              'about them may be missing. What it does not state, and what does not follow from what it states and '
              'the rules, is unknown, not false.',
    "SEM-04": '"Not recorded" (or null) means some value the record does not give, on a complete record too; nothing '
              'in the record makes a statement about it true or false. On a record that may be incomplete a blank '
              'means the same; on a complete record a blank yes/no entry means no.',
    "SEM-11": 'Dates are whole calendar days. "On D" is that day. "Before D" and "after D" exclude D. "On or before D", '
              '"by D", "no later than D" and "not after D" include D, and so do "on or after D", "no earlier than D" '
              'and "not before D"; these four negated phrases are date words, not a "not" over a statement. "Between '
              'D1 and D2", "from D1 to D2" and "D1 through D2" include both dates. "In" a month or a year means any '
              'day of it. "N days after D" is the Nth day after D (1 day after D is the next day); "within N days '
              'after D" is the day after D through the Nth day after D. "As of D" is the end of D, counting every '
              'entry dated D. For an event, a date range asks whether at least one such event falls on some day of '
              'the range (one is enough), and a "not" over it means no such event does; for a single date, it asks '
              'whether that date falls on some day of the range.',
    "SEM-16": 'Entries with no named author are records by {S}. A CORRECTION or VOID names one entry by its own author. '
              'A CORRECTION replaces a value of that entry (a holder, a status, a number of days or a stated value) as '
              'if it had always said so; the entry keeps its date, kind and item. A VOID cancels the entry: treat it '
              'as never written. Both apply whatever their own date, also to earlier times. Voiding a CORRECTION '
              'restores the entry it corrected. Only entries by {S} make facts true, so a CORRECTION or VOID by anyone '
              'else changes only what its author stated.',
    "SEM-19": '"Failed to", "neglected to", "omitted to" and "did not manage to" do X, with no "by D", mean X did not '
              'happen on any day of the covered period, wherever the phrase appears and whatever its entry date; they '
              'do not say whether X was required. "Failed to do X by D": X did not happen on any day from the start '
              'of the period through D. "Refused to", "declined to" and "was prevented from" doing X: X did not happen '
              'on any day of the covered period. "Managed to do X": X happened. "Lacks Z", "is without Z" and "is free '
              'of Z": does not have Z.',
    "SEM-20": 'Statements by {S} are true; statements by anyone else are only claims and make nothing true or false. '
              '"X denied that P" and "X ruled out P": X stated that P is false. "X confirmed P": X stated that P is '
              'true. A question about what X stated asks about the latest (by date) remaining statement by X about P '
              'dated on or before the asked day; a statement about P states P or states that P is false. X\'s own '
              'VOID or retraction removes that statement and X\'s own CORRECTION or correction replaces what it says, '
              'whatever their date. Nobody else can change what X stated.',
    "SEM-33": 'Each item has three separate states: holder, status and validity. An entry takes effect on its date and '
              'counts for that date. A creation or transfer sets the holder, a status entry sets the status, and a '
              '"renewed for N days" or "valid for N days" entry sets validity; no entry changes another state. A '
              'state holds from its entry date through the day before the next entry that changes the same state. '
              '"Renewed (or valid) for N days" dated D makes the item valid from D through its last valid day, the '
              'Nth day after D; this replaces any last valid day set by an entry dated before D, even a later one, '
              'and nothing else moves the last valid day. From the day after the last valid day the item has lapsed '
              '(not valid), and a renewal dated after that makes it valid from its date. A lapse changes neither '
              'holder nor status.',
    "SEM-26": 'In a question, "never" means on no day from the start of the covered period through the asked day; in '
              'the record, on no day of the covered period. "No longer": held on some day before the asked day in '
              'that period and does not hold on it. "Still": held on some day before the asked day in that period '
              'and holds on it. In a dated record entry, "no longer" and "still" refer to the entry date. A record '
              'entry saying something never happened, no longer holds or still holds is a statement by its author: '
              'it sets and changes no state.',
    "SEM-24": '"Must" and "is required to": required. "Must not", "may not", "is not permitted to" and "cannot": not '
              'permitted. "Need not", "does not have to" and "is not required to": not required, saying nothing about '
              'permission. "May" and "is permitted to": permitted. The listed rules are all the rules about these '
              'actions: an action no listed rule forbids for the case is permitted, and one no listed rule requires '
              'is not required. This line decides required and permitted on complete and incomplete records alike, '
              'ahead of the line on completeness. In a table of roles and actions, "required" means the role must do '
              'it (so it is also permitted), "permitted" means it may and need not, and "forbidden" means it must '
              'not; each cell holds in every case, and no other rule is about a tabled role and action.',
    "SEM-07": '"If B, then A": B is enough for A, so if A is false, B is false; it says nothing about A when B is false. '
              'A rule\'s conditions are the parts of its "if" clause joined by "and" (an "unless" or "except when" part '
              'is not one). A condition is met when what it says is true of the case, so one written with "not" or '
              'another negative word is met when what it denies is false. "At least q of the conditions of a rule": '
              'at least q of them are met.',
    "SEM-31": 'Only messages by {S} make facts true or false. A retraction or correction names a message by its own '
              'sender: a retraction cancels it as if never sent; a correction replaces its value as if it had always '
              'said so, and the message keeps its date. They apply whatever their own date and are not messages '
              'about the fact. Of the remaining messages by {S} about one fact, the latest (by date) counts. A '
              'retraction or correction by another party changes only what that party stated.',
}


def rendering(key, variant, **kw):  # noqa: F811  (redefined with variant c)
    if variant == "c" and key in C:
        return C[key].format(**kw)
    src = B if variant == "b" and key in B else A
    return src[key].format(**kw)


def registry():  # noqa: F811
    reg = {}
    for src in (A, B, C):
        for k, v in src.items():
            reg.setdefault(k.replace("SEM-17L", "SEM-17"), []).append(v)
    return reg
