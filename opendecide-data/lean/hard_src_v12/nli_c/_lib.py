"""Helpers for the hard 'nli_c' item author (natural language inference on
realistic paragraphs: news briefs, emails, meeting minutes, reports, chats and
tickets). Traps: negation scope, downward-entailing quantifiers, exceptives,
presupposition triggers, factive vs non-factive verbs, modals, conditionals and
counterfactuals, temporal order, numeric comparison, coreference, and reported
vs endorsed speech. All people, organisations, products and places are invented.
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


# Shared label sets -----------------------------------------------------------

NLI3 = [
    ("entailment", "a careful reader who accepts as true everything the passage asserts in its own voice must also accept the hypothesis as true."),
    ("contradiction", "accepting as true everything the passage asserts in its own voice requires rejecting the hypothesis as false."),
    ("neutral", "the passage, taken as true, still allows the hypothesis to be either true or false."),
]

REL5 = [
    ("entailed", "the author, in their own voice (including through factive verbs such as know, realise or regret, and through presuppositions), commits to the hypothesis being true."),
    ("contradicted", "the author, in their own voice, commits to the hypothesis being false."),
    ("attributed only", "the author commits neither way, but the passage presents the hypothesis or its negation as the claim, belief, hope or allegation of a named person or body."),
    ("conditional only", "the author commits neither way and attributes neither, but states that the hypothesis will or would hold if a condition the passage leaves unresolved is met."),
    ("not settled", "none of the other four descriptions applies."),
]

ESTABLISH = ("Establish", "the passage, taken as true, guarantees the statement; a statement that is only likely, only claimed or believed by someone, only required or planned, or only conditional on an unresolved event is not established.")
FACTIVE = ("Factive verb", "a verb such as know, realise, regret or discover whose complement the writer commits to as true; non-factive verbs such as believe, claim, suspect or expect carry no such commitment.")
PRESUP = ("Presupposition", "background content that a trigger word takes for granted and that survives negation, e.g. 'stopped X-ing' takes for granted that X-ing used to happen, 'again' that it happened before.")
IMPLICATIVE = ("Implicative verb", "a verb such as manage or fail whose use settles whether the complement happened: 'managed to X' means X happened, 'failed to X' or 'did not manage to X' means X did not happen; 'tried to X' settles nothing.")
QUANT = ("Downward-entailing quantifier", "a quantifier such as no, few, at most or not all, which licenses inferences from a larger set to any of its members or subsets rather than the other way round.")
EXCEPT = ("Exceptive", "'all/every/no X except Y' says the statement holds of every X other than Y and does not hold of Y.")
MODAL = ("Modal", "might and could mark possibility, must and should mark obligation or expectation; neither shows that the event actually happened.")
COND = ("Conditional", "'if A then B' establishes B only when the passage also establishes A; a counterfactual 'had A happened, B would have' takes for granted that A did not happen.")
REPORTED = ("Reported speech", "a claim the passage attributes to someone ('X said/claims/alleges that ...') without the writer endorsing it.")
