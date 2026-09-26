"""Helpers for the v0.12 HARD 'intent_c' item author (speaker intent and
pragmatics in workplace chats, social posts, game chat, reviews and community
boards): intent to demean or offend and its target (group, individual, no one),
reported speech, criticism of ideas, reclaimed in-group terms, banter, satire,
sarcasm, hyperbole vs veiled threats, indirect requests and masked dog whistles.
All platforms, people, brands and places are invented.
Slurs and hateful codes are never written; states mask them ("[slur for ...]",
"[marker N-2]") and describe their meaning in a reference list when needed.
Rationale comments in item files (# why:) are for auditing only and never
reach the rows.
"""


def C(key, instructions, state, options, gold, difficulty, twin=None, ordered=False):
    """Choice item. options: list of (option, definition)."""
    return dict(key=key, qtype="choice", role="choice", instructions=instructions,
                state=state.strip(), options=options, gold=gold,
                difficulty=difficulty, twin=twin, ordered=ordered)


def Y(key, instructions, state, card, gold, difficulty, twin=None, role="aff"):
    """Yes/no item. card: list of (term, definition). gold 1 = yes."""
    return dict(key=key, qtype="noul", role=role, instructions=instructions,
                state=state.strip(), card=card, gold=gold,
                difficulty=difficulty, twin=twin)


def T(edits, gold, instructions=None):
    """Minimal-pair twin: list of (old, new) replacements on the state."""
    return dict(edits=edits, gold=gold, instructions=instructions)


# Shared intent labels. Definitions are written to be mutually exclusive.
INTENT = {
    "insult an individual": "the speaker means to belittle, mock or offend a specific person (named, addressed or clearly identifiable) for who they are or what they did.",
    "demean a group": "the speaker openly means to belittle or offend people because they belong to a group defined by ethnicity, religion, nationality, gender, sexual orientation, disability, age or a similar shared trait.",
    "coded attack on a group": "the speaker uses an innocent-looking word, number, symbol or phrase whose established meaning demeans a group.",
    "threaten": "the speaker seriously states or implies that unlawful harm or intimidation will come to a person, their safety, property or livelihood, including veiled or conditional warnings; announcing lawful steps such as complaints, reviews or legal claims is not threatening.",
    "hyperbole": "the speaker uses exaggerated violent or extreme wording to express a feeling, with no real intent that anyone be harmed.",
    "friendly banter": "playful teasing between people on friendly terms, where the teased person is in on it and nothing demeaning about who they are is meant.",
    "joke without a target": "the main point is a joke or pun that belittles no person or group and uses no violent or extreme wording.",
    "satire": "the speaker imitates or exaggerates a position, in the voice of its supporters, so that the position itself looks absurd.",
    "criticise an idea or policy": "the speaker argues directly (not by imitation) against a belief, rule, decision, product or organisation's conduct, without demeaning the people involved.",
    "report someone else's words": "the main point of the message is to relay, quote or document what someone else said or wrote, without adopting it.",
    "reclaimed in-group use": "a member of a group uses a term once aimed against that group, about themselves or fellow members, with no demeaning intent.",
    "request": "the main point is to get someone to do something, whether asked directly or only hinted at.",
    "complain": "the speaker voices dissatisfaction (plainly or sarcastically) with a service, product or situation, without demeaning anyone, without violent or extreme wording, and without trying to get anyone to take a specific action.",
    "self-deprecation": "the speaker makes fun of themselves.",
    "praise": "the speaker sincerely expresses approval or admiration of someone or something.",
    "none of these": "the message fits none of the other listed intents.",
}

TARGET = {
    "a group": "people singled out because of a shared characteristic such as ethnicity, religion, nationality, gender, sexual orientation, disability or age.",
    "the addressee": "the specific person the message is sent or replied to.",
    "a specific third person": "an identifiable individual who is not the addressee.",
    "an idea, policy or product": "a belief, rule, decision, product or organisation's conduct, rather than people.",
    "the speaker": "the speaker themself.",
    "no one": "the message carries no negative intent toward anyone or anything.",
}


def pick(table, *names):
    return [(n, table[n]) for n in names]
