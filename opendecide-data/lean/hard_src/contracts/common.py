"""Shared definitions and item helpers for the hard 'contracts' domain (v0.11 HARD track).

All companies, products, people, arbitral bodies and websites are invented. Governing-law
jurisdictions are real places (that is what such clauses name) but no real organisation is quoted.
Authored by the teacher (Claude); no external model or dataset is used.
"""

# key -> (option label, definition). Labels never contain ": ".
DEFS = {
    "LOL": ("limitation of liability",
            "caps the amount one party can recover from the other (for example, limited to fees paid) or excludes "
            "liability for whole categories of loss or for specified events. Clauses that only disclaim warranties, "
            "excuse performance for events beyond a party's control (force majeure), require insurance, allocate "
            "third-party claims (indemnity), or merely preserve liability do not qualify."),
    "UC": ("unilateral change",
           "lets one party change the terms, fees, rates, or features of the agreement at its own discretion, leaving "
           "the other party only to accept (including by continued use) or leave. Changes that need the other "
           "party's affirmative agreement, and price changes fixed in advance by a formula or schedule, do not qualify."),
    "TWC": ("termination without cause",
            "lets a party end the agreement, subscription, or account at its discretion (for convenience, for any "
            "reason or no reason) without needing a breach, fault, or other specified triggering event. Termination "
            "for breach, non-payment, insolvency, policy violation, inactivity, or another specified event, and "
            "simple expiry or non-renewal at the end of a term, do not qualify."),
    "COL": ("choice of law",
            "states which jurisdiction's law governs the agreement or disputes about it. Clauses that only choose "
            "the court, venue, or arbitration forum where disputes are heard, or that only preserve mandatory "
            "statutory rights, do not qualify."),
    "ARB": ("arbitration",
            "requires, or lets either party unilaterally compel, that disputes be decided by binding arbitration "
            "before a neutral arbitrator or tribunal instead of in court (a class-action waiver attached to such a "
            "clause is part of it). Negotiation or mediation steps, non-binding or advisory processes, decisions made "
            "by one of the parties, arbitration that needs both parties' later consent, and court-selection clauses "
            "do not qualify."),
    "CR": ("content removal",
           "gives the provider the right to remove, delete, hide, unpublish, or refuse to publish content that users "
           "post or upload. Suspending or closing whole accounts, monitoring without a removal right, users deleting "
           "their own content, and licenses the user grants over content do not qualify."),
    "DS": ("data sharing",
           "permits the provider to disclose, sell, or transfer users' personal information (information linked to "
           "an identifiable user, such as contact details, activity, or location) to third parties, including "
           "service providers, affiliates, advertisers, partners, insurers, or a buyer of the business. Clauses "
           "covering only collection, internal use, storage, security, or retention, sharing of de-identified or "
           "aggregate data, or promises not to share, do not qualify."),
    "AR": ("auto-renewal",
           "makes the agreement or subscription renew or continue automatically for a further term unless a party "
           "cancels or gives notice of non-renewal. Options to renew that require a party to act, and fixed terms "
           "that simply end, do not qualify."),
    # near-miss categories
    "FS": ("forum selection",
           "names the courts or venue where lawsuits must or may be brought. Clauses that only name the governing "
           "law, or that send disputes to arbitration, do not qualify."),
    "IND": ("indemnification",
            "requires one party to defend, hold harmless, or reimburse the other for claims brought by third parties "
            "and the resulting losses or costs."),
    "WD": ("warranty disclaimer",
           "disclaims or excludes promises or implied warranties about quality, fitness, accuracy, or uninterrupted "
           "operation (for example, 'as is'). Caps or exclusions of damages do not qualify."),
    "FM": ("force majeure",
           "excuses a party's delay or failure to perform when caused by events beyond its reasonable control."),
    "ASG": ("assignment",
            "governs whether and how a party may transfer its rights or obligations under the agreement to someone else."),
    "CONF": ("confidentiality",
             "obliges a party to keep the other party's non-public business information secret and to use it only "
             "for permitted purposes."),
    "LIC": ("content license",
            "has the user grant the provider rights to use, copy, modify, display, or distribute content the user submits."),
    "TFC": ("termination for cause",
            "lets a party end the agreement or account because of a breach, non-payment, insolvency, policy "
            "violation, inactivity, or another specified triggering event."),
    "CAW": ("class action waiver",
            "waives the right to bring or join class, consolidated, or representative actions, without sending "
            "disputes to arbitration."),
    "DR": ("data retention",
           "states how long the provider keeps user data or when it deletes it."),
    "PAY": ("payment terms",
            "sets when and how fees are invoiced and paid, including due dates, late-payment interest, and payment methods."),
    "NS": ("non-solicitation",
           "restricts a party from hiring or soliciting the other party's employees or customers."),
    "AUD": ("audit rights",
            "lets a party inspect the other party's records, facilities, or systems to verify compliance."),
    "SEV": ("severability",
            "keeps the rest of the agreement in force if one provision is found invalid or unenforceable."),
    "NOT": ("notices",
            "specifies how and where formal notices under the agreement must be delivered."),
    "EXC": ("exclusivity",
            "requires a party to deal only with the other party for specified goods, services, or territory."),
    "EA": ("entire agreement",
           "states that the written agreement supersedes all prior discussions and agreements on its subject."),
    "SLA": ("service levels",
            "sets measurable performance or availability commitments and the credits or remedies for missing them."),
    "NONE": ("none of these", "the provision meets none of the definitions above."),
}

MAIN = ["LOL", "UC", "TWC", "COL", "ARB", "CR", "DS", "AR"]
NEAR = ["FS", "IND", "WD", "FM", "ASG", "CONF", "LIC", "TFC", "CAW", "DR", "PAY", "NS", "AUD", "SEV", "NOT", "EXC",
        "EA", "SLA"]

# Question phrasings. {t} target, {c} category label, {a} article for {c}.
CHOICE_Q = [
    "Which category best describes {t}?",
    "Using the definitions provided, how should {t} be classified?",
    "What type of clause is {t}?",
    "Which label should the contract abstraction record for {t}?",
    "Which of these clause types does {t} fall under?",
    "Pick the category that fits {t}.",
    "How would a careful contract reviewer tag {t}?",
    "Into which category should {t} be filed?",
    "Applying the category definitions, which type of provision is {t}?",
    "Which clause category, if any, applies to {t}?",
]
YES_Q = [
    "Does {t} qualify as {a} {c} clause under the definition given?",
    "Is {t} {a} {c} clause?",
    "Applying the definition provided, should {t} be tagged \"{c}\"?",
    "Would a careful reviewer label {t} as {c}?",
    "Does {t} meet the definition of {c}?",
    "Should {t} be counted as {a} {c} provision?",
    "Is it correct to classify {t} as {c}?",
    "Based on the definition, does {t} fall under {c}?",
]
NEG_Q = [
    "Would it be wrong to tag {t} as {c}?",
    "Is it incorrect to classify {t} as {a} {c} clause?",
    "Does {t} fall outside the definition of {c}?",
]
SEC_Q = [
    "Which provision, if any, is {a} {c} clause?",
    "Which of the quoted provisions meets the definition of {c}?",
    "Where in the excerpt is the {c} clause, if there is one?",
    "Which provision should be tagged \"{c}\"?",
    "Identify the provision that qualifies as {c}, or answer none of these.",
    "Which of these provisions contains {a} {c} term?",
]


def article(label):
    if label.startswith(("uni", "use", "eu")):
        return "a"
    return "an" if label[0] in "aeiou" else "a"


def C(key, state, opts, gold, diff, t="the quoted clause", q=None, twin=None, keep_order=False):
    """Category choice item. opts: category keys (NONE appended if listed). gold: a key in opts."""
    assert gold in opts, (key, gold, opts)
    return dict(kind="cat", key=key, state=state, opts=opts, gold=gold, diff=diff, t=t, q=q, twin=twin,
                keep_order=keep_order)


def Y(key, state, cat, truth, diff, t, q=None, twin=None, neg=False, extra=()):
    """Yes/no item: does target t belong to category cat? truth 1/0 (before any negated phrasing)."""
    return dict(kind="yn", key=key, state=state, cat=cat, truth=truth, diff=diff, t=t, q=q, twin=twin, neg=neg,
                extra=list(extra))


def S(key, state, sections, cat, gold, diff, q=None, twin=None, extra=()):
    """Section-locator choice item: which quoted provision is a `cat` clause? gold: a section label or NONE."""
    assert gold in sections or gold == "NONE", (key, gold)
    return dict(kind="sec", key=key, state=state, sections=sections, cat=cat, gold=gold, diff=diff, q=q, twin=twin,
                extra=list(extra))


def T(subs, gold, q=None, t=None):
    """Minimal-pair twin: list of (old, new) substitutions applied to the state; new gold (key/label/truth)."""
    return dict(subs=subs, gold=gold, q=q, t=t)
