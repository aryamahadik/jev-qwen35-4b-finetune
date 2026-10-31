"""Shared policy definitions and item helpers for the hard 'policy_a' domain.

All platforms, people, groups and codes are invented. Slurs are always masked
as bracketed placeholders (e.g. "[anti-Roma slur]"); no real slur is written.
"""

# ---------------------------------------------------------------- Loomwell
L_OPTS = {
    "3.1": "3.1 Hateful conduct",
    "3.2": "3.2 Targeted harassment",
    "3.3": "3.3 Violent threats",
    "3.4": "3.4 Self-harm encouragement",
    "3.5": "3.5 Spam",
    "3.6": "3.6 Private information",
}
L_DEF = {
    "3.1": "content that attacks people on the basis of a protected characteristic (race, ethnicity, national origin, religion, caste, sexual orientation, sex, gender identity, disability, serious disease). An attack is dehumanizing language (comparison to animals, insects, filth or disease), a claim of inherent inferiority, a call for exclusion or segregation, or a slur used to describe or address people. Not covered: (a) quoting or reporting hateful content in order to condemn it or raise awareness, where that purpose is clear from the post itself; (b) a member of a group using a reclaimed term for themselves or their own group, not to attack; (c) criticism of religions or ideologies as belief systems, or of governments and organisations; (d) attacks on groups defined by anything not listed, such as age, profession, immigration status, political affiliation, hometown or fandom.",
    "3.2": "content directed at an identifiable private individual that insults, demeans or sexualizes them, or that urges others to contact, pile on or mass-report them. For public figures (elected officials, celebrities, and accounts with more than 100,000 followers) only sexualizing content and calls to pile on are covered; insults and mockery of their public conduct are allowed.",
    "3.3": "a statement of intent, wish or call for serious physical harm to a person or group, including conditional statements. Not covered: obvious hyperbole in a clearly non-serious exchange, clearly labelled fiction, song lyrics or quotes shared without endorsement, and news reporting or discussion of violence.",
    "3.4": "content that encourages, instructs or praises suicide, self-injury or eating-disorder behaviour, including telling a person to harm or kill themselves (abbreviations included). Not covered: first-person accounts of one's own experience, recovery content, and requests for support.",
    "3.5": "unsolicited commercial promotion outside the weekly Promo Thread; identical or near-identical posts in more than three communities within 24 hours; or links disguised to mislead users about their destination.",
    "3.6": "posting another person's non-public personal information (home address, personal phone number, personal email, government ID or financial numbers, real-time location) without their consent. Not covered: contact details a business publishes, information the person has themselves posted publicly on Loomwell, and the official office contact details of public officials.",
}

# ---------------------------------------------------------------- Brindle
B_OPTS = {
    "H1": "H1 Hateful behaviour",
    "B1": "B1 Bullying",
    "V1": "V1 Violent speech",
    "S1": "S1 Suicide and self-harm",
    "C1": "C1 Spam and scams",
    "P1": "P1 Personal data",
}
B_DEF = {
    "H1": "content that attacks people based on a protected attribute: race, ethnicity, national origin, immigration status, religion, sexual orientation, sex, gender identity, age, disability or veteran status. Attacks include dehumanization, harmful stereotypes stated as fact, calls for exclusion, and slurs. Negated, hypothetical, rhetorical-question or 'just joking' framings are judged by what the content as a whole communicates. Allowed: counter-speech, reclaimed terms used by in-group members, and satire whose target is clearly the bigot rather than the group.",
    "B1": "content that degrades, shames or mocks a specific private individual, including mocking their appearance or sharing images of them to invite ridicule. Content about public figures is covered only when it targets their physical appearance or their family members rather than their public role.",
    "V1": "threats, wishes or calls for violence against people or groups, and praise of real violent attacks or their perpetrators. Allowed: clear fiction, trash talk about games or sports matches, self-defence instruction, and news.",
    "S1": "content that promotes, glamorizes or gives methods for suicide or self-harm, or urges someone to harm themselves. Allowed: sharing personal experiences, recovery journeys and seeking help, provided no methods are described.",
    "C1": "fake giveaways, phishing, get-rich-quick schemes, engagement bait (asking viewers to like, comment, share or tag in exchange for a reward, luck or a blessing, or to 'boost' the post), and repetitive unsolicited promotion.",
    "P1": "sharing someone else's private information (home address, phone number, personal email, ID numbers, vehicle licence plates, or content revealing their live location) without consent. Allowed: information the person has already published themselves on any public website or platform, business listings, and public officials' office details.",
}

# ---------------------------------------------------------------- Kestrel
K_CODES = [
    ("HS-1", "Dehumanization", "comparing a protected group (race, ethnicity, nationality, religion, sexual orientation, gender identity, sex, disability) to animals, vermin, disease or filth, or calling its members subhuman."),
    ("HS-2", "Inferiority or criminality claims", "stating that a protected group is inherently inferior, stupid, criminal or dangerous."),
    ("HS-3", "Exclusion calls", "calling for a protected group to be excluded, segregated, deported or denied access to games, servers or services."),
    ("HS-4", "Slur use", "using a slur against a person or to describe a protected group. Excludes in-group reclaimed use and quoting a slur to report or condemn it."),
    ("HS-5", "Hateful codes", "using a code, number, symbol or dog-whistle phrase on the Kestrel watch-list (1488, 88, echo brackets around names, 'grey tide' meaning Ostrevan migrants) to promote hate."),
    ("HR-1", "Insults to a player", "degrading insults aimed at a specific player."),
    ("HR-2", "Sexual harassment", "unwanted sexual remarks, requests or images aimed at a specific person."),
    ("HR-3", "Brigading", "organizing or urging others to target a specific player, stream, server or review page."),
    ("HR-4", "Persistent contact", "contacting a player again, including from another account, after that player has blocked the sender or asked them to stop."),
    ("HR-5", "Voice-chat recording", "posting a recording of a player's voice chat without their consent."),
    ("VT-1", "Direct threat", "the sender states an intent to physically harm a specific person."),
    ("VT-2", "Incitement", "calling on others to physically harm a person or group."),
    ("VT-3", "Glorifying attacks", "praising real-world mass-casualty attacks or their perpetrators."),
    ("VT-4", "Swatting", "threatening, planning or encouraging false emergency reports to someone's location."),
    ("SH-1", "Encouraging self-harm", "telling someone to hurt or kill themselves, including 'kys' used in that sense."),
    ("SH-2", "Self-harm methods", "sharing methods or instructions for suicide or self-injury."),
    ("SH-3", "Pro-eating-disorder", "promoting or coaching starvation, purging or extreme restriction."),
    ("SP-1", "Commercial spam", "unsolicited advertising, including gold-selling, boosting and coaching services."),
    ("SP-2", "Scams and phishing", "fake giveaways, credential-harvesting links, or pretending to be Kestrel staff."),
    ("SP-3", "Chat flooding", "sending the same or near-identical message more than 8 times within 60 seconds."),
    ("PI-1", "Address or location exposure", "revealing a person's home address, school, or real-time location."),
    ("PI-2", "Contact details exposure", "revealing a person's phone number or personal email address."),
    ("PI-3", "Identity or financial numbers", "revealing full or partial government ID, bank or card numbers."),
    ("PI-4", "Real-name exposure", "linking a pseudonymous player to their legal name when they have not made that link public themselves."),
    ("CH-1", "Cheat promotion", "selling, linking or advertising cheats, hacks or exploits."),
    ("IM-1", "Impersonation", "pretending to be another specific player or creator (impersonating Kestrel staff is SP-2)."),
    ("EV-1", "Ban evasion", "using another account to play or chat while one's own account is under a Kestrel suspension or ban."),
]
K_OPT = {c: f"{c} {n}" for c, n, _ in K_CODES}
K_DEF = {c: d for c, _, d in K_CODES}
K_RULE = ("Code-book rule 2: assign exactly one code. If a message fits codes from more than one family, use the "
          "family that comes first in this order: VT, SH, HS, PI, HR, CH, SP, IM, EV. Within a family, use the "
          "lowest-numbered code that fits. Use \"none of these\" if no listed code fits.")

# ---------------------------------------------------------------- Meridian
M_OPTS = {
    "4.1": "§4.1 Discriminatory remarks",
    "4.2": "§4.2 Bullying and intimidation",
    "4.3": "§4.3 Threats",
    "4.4": "§4.4 Sexual harassment",
    "4.5": "§4.5 Confidential data",
    "4.6": "§4.6 Solicitation",
}
M_DEF = {
    "4.1": "remarks that demean or stereotype a person or group because of race, colour, religion, sex, pregnancy, sexual orientation, gender identity, national origin, age (40 and over), disability, genetic information or veteran status, including jokes and 'banter'. Does not include good-faith discussion of diversity policy, or quoting a remark in order to report it.",
    "4.2": "belittling, humiliating or intimidating a colleague, including ridiculing them or their work in front of others. A civil critique of work quality, given privately or in a normal review, is not bullying.",
    "4.3": "any statement threatening physical harm to a person, or referring to bringing a weapon to work, even if framed as a joke.",
    "4.4": "unwelcome sexual comments, advances, or sexual content directed at or shared with colleagues, including remarks about a colleague's body or clothing that carry a sexual meaning.",
    "4.5": "sharing customer personal data, or a colleague's home address, personal phone number, health information or salary, anywhere other than the system authorised for that data.",
    "4.6": "selling, advertising or fundraising for non-work purposes in any channel other than #marketplace, and more than one such post per person per calendar week in #marketplace.",
}

# ---------------------------------------------------------------- Quillon
Q_TIERS = [
    ("Tier 1", "spam, or a mild insult aimed at a user (e.g. 'idiot', 'clown')."),
    ("Tier 2", "a slur, a hateful stereotype about a protected group, degrading harassment of a user, or encouragement of self-harm that is not aimed at a specific person."),
    ("Tier 3", "dehumanization of a protected group, telling a specific person to harm or kill themselves, sexual harassment, or exposing someone's phone number or email address."),
    ("Tier 4", "a credible threat of violence, exposing someone's home address or real-time location, or praise of a mass-casualty attack."),
    ("no violation", "the content breaches none of the tier descriptions."),
]
Q_TIER_TEXT = ("Quillon severity tiers (protected groups: race, ethnicity, national origin, religion, sexual orientation, "
               "gender identity, sex, disability; quoting hateful content to condemn or report it is not a violation):\n"
               + "\n".join(f"{t}: {d}" for t, d in Q_TIERS[:4]))
Q_ACTIONS = [
    ("no action", "the content does not violate policy."),
    ("remove only", "a Tier 1 violation by an account with no strikes in the 90 days before the violation."),
    ("remove and strike", "a Tier 1 violation by an account with one or more strikes in the previous 90 days, or a Tier 2 violation by an account with at most one strike in the previous 90 days."),
    ("7-day suspension", "a Tier 2 violation by an account with two or more strikes in the previous 90 days, or any Tier 3 violation."),
    ("permanent ban", "any Tier 4 violation, or any violation by an account that already has three or more strikes in the previous 90 days."),
]


def card_lines(pairs):
    return "\n".join(f"- {o}: {d}" for o, d in pairs)


def L_card(keys, none=False):
    pairs = [(L_OPTS[k], L_DEF[k]) for k in keys]
    if none:
        pairs.append(("none of these", "the post breaches none of the sections listed above."))
    return card_lines(pairs)


def L_options(keys):
    return [L_OPTS[k] for k in keys] + ["none of these"]


def B_card(keys, none=False):
    pairs = [(B_OPTS[k], B_DEF[k]) for k in keys]
    if none:
        pairs.append(("none of these", "the content breaches none of the standards listed above."))
    return card_lines(pairs)


def B_options(keys):
    return [B_OPTS[k] for k in keys] + ["none of these"]


def K_card(codes, none=False):
    pairs = [(K_OPT[c], K_DEF[c]) for c in codes]
    if none:
        pairs.append(("none of these", "no listed code fits the message."))
    return card_lines(pairs)


def K_options(codes):
    return [K_OPT[c] for c in codes] + ["none of these"]


K_ALL = [c for c, _, _ in K_CODES]


def M_card(keys, none=False):
    pairs = [(M_OPTS[k], M_DEF[k]) for k in keys]
    if none:
        pairs.append(("none of these", "the message breaches none of the clauses listed above."))
    return card_lines(pairs)


def M_options(keys):
    return [M_OPTS[k] for k in keys] + ["none of these"]


def Q_action_card():
    return card_lines(Q_ACTIONS)


Q_ACTION_OPTS = [a for a, _ in Q_ACTIONS]
Q_TIER_OPTS = [t for t, _ in Q_TIERS]


def Q_tier_card():
    return card_lines(Q_TIERS)


# ---------------------------------------------------------------- helpers
def Y(q, state, gold, diff, card, twin=None, role="aff"):
    """Yes/no item. gold 1 = yes. twin = (subs, new_gold[, new_q])."""
    return dict(qtype="noul", q=q, state=state, gold=gold, diff=diff, card=card,
                options=None, twin=twin, role=role)


def C(q, state, options, gold, diff, card, twin=None, shuffle=False):
    """Choice item. gold is an option string. twin = (subs, new_gold[, new_q])."""
    assert gold in options, (gold, options)
    return dict(qtype="choice", q=q, state=state, gold=gold, diff=diff, card=card,
                options=options, twin=twin, role="choice", shuffle=shuffle)
