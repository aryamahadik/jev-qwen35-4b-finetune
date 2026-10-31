"""Shared definitions and item helpers for the hard 'affect' domain (v0.11 HARD track).

Three families: fine-grained emotion (10-28 defined labels incl. close pairs and "neutral"),
stance toward an explicitly named target (favor / against / neither), and service-request intents
for invented services (with "none of these").  All people, organisations, services, places and
ballot measures are invented.  Authored by the teacher (Claude); no external model or dataset is used.
"""

# ----------------------------------------------------------------------------------------------
# Emotion labels.  key == label.  Definitions talk about "the person" so they work for the author
# or for a named speaker.  Every emotion item is written so that its gold is the single best label
# under the FULL 28-label set; any subset that contains the gold is therefore also unambiguous.
# ----------------------------------------------------------------------------------------------
EMO = {
    "admiration": "the person finds a specific person, work, or act impressive or excellent and expresses respect or "
                  "esteem for its quality, skill, or character. Merely agreeing that something is right or "
                  "acceptable is approval, not admiration.",
    "amusement": "the person finds something genuinely funny or entertaining (laughing, being tickled by it). Mocking "
                 "laughter used to criticise is not amusement.",
    "anger": "strong displeasure with hostility toward someone held responsible for a wrong: outrage, fury, blame, "
             "or a demand for consequences or retaliation. Irritation without hostility or outrage is annoyance.",
    "annoyance": "mild to moderate irritation or exasperation at a nuisance, delay, or repeated inconvenience, "
                 "without outrage, fury, or a demand for consequences.",
    "approval": "the person agrees with, endorses, or accepts a decision, opinion, or action as right or acceptable, "
                "without presenting it as impressive or exceptional.",
    "caring": "concern for someone else's wellbeing, with wishes or offers to help, comfort, or protect them.",
    "confusion": "the person does not understand something (what is meant, what happened, or how something works) "
                 "and is uncertain or lost about it.",
    "curiosity": "interest in finding out more about something, wanting to know or explore it, without being lost "
                 "or unable to understand it.",
    "desire": "the person wants to have, get, or do something for themselves; a longing or wish for an object or "
              "experience, as opposed to a general expectation that events will turn out well.",
    "disappointment": "unhappiness because a specific expectation or hope was not met; something turned out worse "
                      "than the person had counted on.",
    "disapproval": "the person judges an action, opinion, or decision to be wrong, unwise, or unacceptable, without "
                   "strong hostility (anger) or revulsion (disgust).",
    "disgust": "revulsion at something physically repugnant (filth, rot, bodily matter) or morally repugnant, "
               "experienced as gross, sickening, or vile.",
    "embarrassment": "self-conscious discomfort about how the person appears to others after an awkward, clumsy, or "
                     "foolish moment in which no one was harmed or wronged.",
    "excitement": "energised, eager anticipation or thrill about something happening now or soon.",
    "fear": "being afraid of a specific danger or threat to safety that is present or imminent.",
    "gratitude": "thankfulness directed at someone for something they did or gave.",
    "grief": "intense sorrow over a significant loss, especially the death of a person or animal.",
    "joy": "happiness, delight, or contentment about how things are or went, not centred on the person's own "
           "achievement (pride) or on escaping a feared outcome (relief).",
    "love": "strong affection or deep attachment toward a person, animal, place, or thing.",
    "nervousness": "anxious worry or unease about an uncertain outcome that has not happened yet, where the person "
                   "is not facing a present or imminent danger.",
    "optimism": "hopefulness or confidence that future events will turn out well.",
    "pride": "satisfaction in an achievement or quality of the person's own, or of someone they are closely "
             "identified with (their child, team, or student).",
    "realization": "the person comes to understand or become aware of something they had not grasped before; the "
                   "moment the penny drops.",
    "relief": "the release of tension after a feared or anxious outcome did not happen or has ended.",
    "remorse": "regret or guilt for something the person did that harmed or wronged someone, often with an apology.",
    "sadness": "sorrow or feeling down that is not centred on a specific unmet expectation (disappointment) or on a "
               "death or other major loss (grief).",
    "surprise": "astonishment at something unexpected, whether good or bad.",
    "neutral": "the person expresses none of the other listed emotions; the text is informational, procedural, or "
               "emotionally flat.",
}
EMO_ORDER = list(EMO)

# ----------------------------------------------------------------------------------------------
# Stance labels
# ----------------------------------------------------------------------------------------------
STANCE = {
    "favor": "the person supports the named target, or clearly implies it should be adopted, succeed, win, or "
             "continue (including through sarcasm aimed at its opponents, or by knocking down arguments against "
             "it). Opposing the target's only rival for the same single decision also counts as favor.",
    "against": "the person opposes or criticises the named target, or clearly implies it should be rejected, fail, "
               "lose, or end (including through sarcasm or mocking faint praise). Supporting a rival option or "
               "candidate for the same single decision also counts as against.",
    "neither": "the person takes no position on the named target itself: they only express views on related "
               "people, organisations, or issues that are not rivals of the target, report other people's views "
               "without endorsing them, ask open questions, or say they are undecided or evenly balanced.",
}
STANCE_ORDER = ["favor", "against", "neither"]

NONE_LABEL = "none of these"

# ----------------------------------------------------------------------------------------------
# Invented services and their intents: service -> list of (label, description)
# Labels never contain ": ".
# ----------------------------------------------------------------------------------------------
SERVICES = {
    "Quillfeather Credit Union": [
        ("freeze card", "temporarily lock a card the member still has or expects to find, so no new transactions go "
                        "through; it can be unlocked later"),
        ("report lost or stolen card", "permanently cancel a card that has been stolen or is gone for good and "
                                       "order a replacement"),
        ("card not arrived", "a new or replacement card that was already ordered has not been delivered"),
        ("card declined", "a card payment or cash withdrawal was refused and the member wants to know why or get it "
                          "working"),
        ("dispute a charge", "challenge a completed transaction the member did not authorise or that the merchant "
                             "got wrong, to get the money back"),
        ("pending charge query", "ask about a transaction or hold that is still pending and has not settled, without "
                                 "disputing it"),
        ("transfer not received", "money sent to or from the member's account has not arrived where expected"),
        ("change PIN", "set a new card PIN or unblock a PIN after too many wrong attempts"),
        ("update contact details", "change the member's address, phone number, or email on file"),
        ("close account", "close a savings or checking account permanently"),
        ("raise card limit", "increase a daily spending or cash-withdrawal limit"),
        ("cash not dispensed", "an ATM debited the account but gave out no cash or too little cash"),
        ("exchange rate query", "ask about the conversion rate or foreign transaction fee applied to a purchase"),
        ("travel notice", "tell the credit union about upcoming travel so card use abroad is not blocked"),
    ],
    "Tandem Pantry": [
        ("missing item", "an item that was ordered and charged for was not in the delivery"),
        ("wrong item", "a different product arrived in place of the one ordered, and it was not a substitution the "
                       "customer accepted"),
        ("damaged item", "an item arrived broken, leaking, crushed, spoiled, or past its use-by date"),
        ("substitution preferences", "set or change how shoppers should replace out-of-stock items in current or "
                                     "future orders"),
        ("change delivery slot", "move a scheduled delivery that has not happened yet to another day or time"),
        ("late delivery", "an order is past its delivery window and has not arrived"),
        ("cancel order", "cancel an order before it is delivered"),
        ("membership billing", "questions or problems with the Pantry Plus subscription fee or its renewal"),
        ("promo code problem", "a discount or promo code did not apply or was applied wrongly"),
        ("driver feedback", "compliment or complaint about the delivery driver's conduct, not about the items"),
        ("refund status", "ask when a refund that was already approved will arrive"),
        ("add to order", "add items to an order that has not been delivered yet"),
    ],
    "Driftwood Stays": [
        ("change reservation dates", "move an existing booking to different dates"),
        ("cancel reservation", "cancel an existing booking"),
        ("check-in instructions", "ask how to get into the property: keys, door codes, directions, or arrival time"),
        ("host unresponsive", "the guest cannot get a reply from the host about a booking"),
        ("listing not as described", "the property lacks features, rooms, or amenities that the listing promised"),
        ("cleanliness complaint", "the property was dirty or not cleaned on arrival"),
        ("security deposit query", "ask about the hold or return of the refundable security deposit"),
        ("payment failed", "a payment for a booking did not go through"),
        ("add guests", "add people to a booking beyond the number originally booked"),
        ("early check-in or late checkout", "ask to arrive earlier or leave later than the standard times"),
        ("refund status", "ask when a refund that was already approved will arrive"),
        ("urgent safety issue", "a present danger at the property: fire, gas smell, flooding, a break-in, or a "
                                "hazard that threatens someone's safety now"),
        ("noise complaint", "neighbours or other guests are making excessive noise"),
    ],
    "Lumen Grid Energy": [
        ("report power outage", "electricity supply is off at the customer's property or street"),
        ("high bill query", "a bill is higher than the customer expected and they want it explained or checked"),
        ("start service", "open a new electricity or gas account at a property where the customer is moving in"),
        ("stop service", "close the account because the customer is leaving a property and not moving within the "
                         "service area"),
        ("transfer service", "move an existing account from one address to another within the service area"),
        ("submit meter reading", "give the customer's own meter reading"),
        ("payment arrangement", "set up an instalment plan or extra time to pay an overdue balance"),
        ("gas emergency", "report a smell of gas, a suspected gas leak, or a damaged gas pipe"),
        ("solar export credit", "questions about credits for electricity the customer's solar panels send to the grid"),
        ("change tariff", "switch to a different pricing plan or rate"),
        ("direct debit setup", "set up, change, or cancel automatic payments from a bank account"),
        ("vegetation near lines", "report trees or branches touching or growing near power lines"),
    ],
    "Parcelwise": [
        ("track parcel", "ask where a parcel is or when it will arrive"),
        ("redirect delivery", "change the address or safe place for a parcel that has not been delivered yet"),
        ("rebook missed delivery", "arrange a new delivery attempt after the courier could not deliver"),
        ("report damaged parcel", "a delivered parcel or its contents arrived damaged"),
        ("report lost parcel", "a parcel shows as delivered but was not received, or has had no updates for a long "
                               "time"),
        ("customs charge query", "questions about import duty, tax, or handling fees charged on a parcel"),
        ("schedule pickup", "book a collection of a parcel the customer is sending"),
        ("cancel shipment", "cancel a shipment the customer booked before it is collected"),
        ("driver complaint", "complain about the courier driver's behaviour or conduct"),
        ("proof of delivery request", "ask for a photo, signature, or other proof that a parcel was delivered"),
    ],
    "Kestrel Mobile": [
        ("no signal or outage", "no network coverage or service at a location, or a suspected network outage"),
        ("mobile data not working", "calls and texts work but mobile internet does not"),
        ("roaming setup", "turn on or ask about using the phone abroad"),
        ("bill dispute", "challenge a specific charge on a bill that the customer believes is wrong"),
        ("upgrade plan", "move to a bigger or more expensive plan"),
        ("downgrade plan", "move to a smaller or cheaper plan"),
        ("port number out", "take the phone number to another provider (request a transfer code)"),
        ("replace SIM or eSIM", "get a new physical SIM or eSIM because the old one is damaged, lost, or needs "
                                "moving to a new phone"),
        ("unlock device", "remove the network lock so the handset works with other providers' SIMs"),
        ("block lost or stolen phone", "bar a lost or stolen handset and its SIM so no one can use them"),
        ("cancel contract", "end the customer's service with Kestrel entirely"),
        ("add a line", "add another phone line or device to the account"),
    ],
    "Stackhouse Cloud": [
        ("site down", "the customer's hosted website or app is unreachable or returning server errors"),
        ("restore from backup", "roll a site or database back to an earlier backup"),
        ("DNS or domain setup", "point a domain at Stackhouse or change DNS records"),
        ("SSL certificate problem", "HTTPS certificate errors, expiry, or certificate installation problems"),
        ("account access", "the customer cannot log in: lost password, locked account, or two-factor problems"),
        ("billing charge query", "questions about a charge or invoice from Stackhouse"),
        ("increase resource quota", "raise storage, memory, or bandwidth limits on the current plan"),
        ("cancel plan", "close the hosting account or stop a plan"),
        ("report abuse", "report a site hosted on Stackhouse that belongs to someone else for spam, phishing, or "
                         "other abuse"),
        ("migrate site in", "move an existing site from another host onto Stackhouse"),
    ],
    "Brightpaw Veterinary": [
        ("book appointment", "schedule a new non-urgent visit"),
        ("reschedule or cancel appointment", "change or cancel an existing appointment"),
        ("urgent care", "the pet has a problem that needs a vet today or right now: poisoning, injury, breathing "
                        "trouble, collapse, or similar"),
        ("prescription refill", "request more of a medication the pet is already prescribed"),
        ("lab results", "ask about test or lab results"),
        ("invoice question", "questions about a bill or charge from the clinic"),
        ("insurance claim form", "ask the clinic to complete or send paperwork for a pet insurance claim"),
        ("vaccination records", "request a copy of the pet's vaccination history"),
        ("boarding booking", "book the pet into the clinic's overnight boarding"),
    ],
}

# ----------------------------------------------------------------------------------------------
# Question phrasings.
# {t} target person/message noun phrase, {tp} its possessive, {x} stance target, {s} service,
# {e} emotion label, {c} stance label, {i} intent label.
# ----------------------------------------------------------------------------------------------
EMO_Q = [
    "Which emotion does {t} express?",
    "Using the label definitions, which emotion best describes what is expressed by {t}?",
    "Which emotion label should an annotator assign to {t}?",
    "According to the definitions, what emotion is expressed by {t}?",
    "Pick the label that fits the emotion expressed by {t}.",
    "Under the annotation guideline, how should {t} be labeled for emotion?",
    "Which of these emotions is expressed by {t}?",
    "What is the best emotion tag for {t}?",
]
WHO_Q = [
    "Which participant expresses {e}?",
    "Who in this exchange expresses {e}, as defined?",
    "Whose words should be tagged {e}?",
    "Which person, if any, expresses {e}?",
    "Identify the person who expresses {e}, or answer none of these.",
    "Applying the definition of {e}, which of the listed people shows it?",
]
STANCE_Q = [
    "What is {tp} stance toward {x}?",
    "Which stance does {t} take on {x}?",
    "How should this text be labeled for stance toward {x}?",
    "Toward {x}, is {t} in favor, against, or neither?",
    "Using the stance definitions, classify {tp} position on {x}.",
    "Which label describes where {t} stands on {x}?",
    "Label {tp} stance on {x}.",
    "Applying the definitions, what stance does {t} express toward {x}?",
]
INTENT_Q = [
    "Which intent should {s} route this message to?",
    "What does the customer want {s} to do? Choose the matching intent.",
    "Which intent label fits the customer's request?",
    "Classify this {s} message using the intent list.",
    "Which of the defined intents, if any, does this message express?",
    "Route this request: which {s} intent applies?",
    "Which intent best matches what the customer is asking for?",
    "According to the intent descriptions, how should this message be labeled?",
]
YN_EMO_Q = [
    "Does {t} express {e}, as defined?",
    "Should {t} be tagged with {e}?",
    "Is {e} among the emotions expressed by {t}?",
    "Applying the definition, is {e} expressed by {t}?",
    "Would a careful annotator tag {t} with the label {e}?",
    "Does the definition of {e} fit what {t} expresses?",
]
YN_STANCE_Q = [
    "Is the label \"{c}\" correct for {tp} stance toward {x}?",
    "Should {tp} stance on {x} be labeled \"{c}\"?",
    "Does the \"{c}\" definition fit {tp} position on {x}?",
    "Applying the stance definitions, is {tp} stance toward {x} \"{c}\"?",
    "Would a careful annotator mark {tp} stance toward {x} as \"{c}\"?",
    "Is \"{c}\" the right stance label for {t} with respect to {x}?",
]
YN_INTENT_Q = [
    "Should this message be routed to the \"{i}\" intent?",
    "Does the customer's request match the {s} intent \"{i}\"?",
    "Is \"{i}\" the correct intent for this message?",
    "Applying the intent descriptions, does this request belong under \"{i}\"?",
    "Would {s}'s router be right to label this message \"{i}\"?",
    "Does the message fit the description of \"{i}\"?",
]
NEG_Q = {
    "emo": ["Would it be wrong to tag {t} with {e}?", "Is {e} an incorrect label for {t}?"],
    "stance": ["Would it be wrong to label {tp} stance toward {x} \"{c}\"?",
               "Is \"{c}\" an incorrect stance label for {t} toward {x}?"],
    "intent": ["Would it be wrong to route this message to \"{i}\"?", "Is \"{i}\" the wrong intent for this message?"],
}


def poss(t):
    return t + ("'" if t.endswith("s") and not t.endswith("'s") and t[0].isupper() else "'s")


# ----------------------------------------------------------------------------------------------
# Item constructors
# ----------------------------------------------------------------------------------------------
def E(key, state, gold, diff, near=(), t="the author", q=None, twin=None, n=None):
    """Emotion choice item. gold: emotion label. near: labels that must appear as distractors.
    n: total option count (10-28); chosen deterministically if None."""
    assert gold in EMO, (key, gold)
    for k in near:
        assert k in EMO, (key, k)
    return dict(kind="emo", key=key, state=state, gold=gold, diff=diff, near=list(near), t=t, q=q, twin=twin, n=n)


def W(key, state, people, emo, gold, diff, extra=(), q=None, twin=None):
    """Who-expresses item: options = people + none of these. gold: a person or NONE_LABEL.
    extra: other emotion labels whose definitions go in the card as near misses."""
    assert emo in EMO and (gold in people or gold == NONE_LABEL), (key, gold)
    return dict(kind="who", key=key, state=state, people=list(people), emo=emo, gold=gold, diff=diff,
                extra=list(extra), q=q, twin=twin)


def S(key, state, x, gold, diff, t="the author", q=None, twin=None):
    """Stance choice item toward target x."""
    assert gold in STANCE, (key, gold)
    return dict(kind="stance", key=key, state=state, x=x, gold=gold, diff=diff, t=t, q=q, twin=twin)


def I(key, state, service, intents, gold, diff, q=None, twin=None, none=True):
    """Intent choice item. intents: labels from SERVICES[service] (order is shuffled by the builder).
    gold: an intent label or NONE_LABEL."""
    labs = [l for l, _ in SERVICES[service]]
    for i in intents:
        assert i in labs, (key, i)
    assert gold in intents or (none and gold == NONE_LABEL), (key, gold)
    return dict(kind="intent", key=key, state=state, service=service, intents=list(intents), gold=gold, diff=diff,
                q=q, twin=twin, none=none)


def YE(key, state, e, truth, diff, t="the author", extra=(), q=None, twin=None, neg=False):
    return dict(kind="yn", fam="emo", key=key, state=state, lab=e, truth=truth, diff=diff, t=t, extra=list(extra),
                q=q, twin=twin, neg=neg)


def YS(key, state, x, c, truth, diff, t="the author", q=None, twin=None, neg=False):
    return dict(kind="yn", fam="stance", key=key, state=state, lab=c, x=x, truth=truth, diff=diff, t=t, extra=[],
                q=q, twin=twin, neg=neg)


def YI(key, state, service, i, truth, diff, extra=(), q=None, twin=None, neg=False):
    return dict(kind="yn", fam="intent", key=key, state=state, lab=i, service=service, truth=truth, diff=diff,
                extra=list(extra), q=q, twin=twin, neg=neg)


def T(subs, gold, x=None, t=None, q=None):
    """Minimal-pair twin: (old, new) substitutions applied to the state (each old must occur exactly once);
    new gold (label / person / 0-1 truth).  x or t optionally change the question's target."""
    return dict(subs=subs, gold=gold, x=x, t=t, q=q)
