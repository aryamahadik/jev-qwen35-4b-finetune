"""families/T30/plugin.py: T30 "clarify or proceed after deduplication" (C2_DATA_SPEC 2.1, 3.5; PREREG_FINAL A37).

A user asks an agent to act on a named target ("please send a payment to Priya"). The row shows the request, a search
listing of 3-6 entries (contacts, files, orders ...) and a rule card that states the matching rule (exact name, letter
for letter), the identity key with its letter-case rule, a consequence table, the decision rule with a batch limit and
a closed-world sentence. The agent's step is one of: go ahead, ask the user which one is meant, or stop and say nothing
matched. It depends on the number of DISTINCT matches after deduplication on the identity key, on the requested
action's consequence class and on the batch limit. Semantics: G0_SPEC.md (frozen sha below).

  solver A   set algebra: the frozenset of normalised identity keys of the name-matched entries, then one lookup in a
             decision table keyed by (count bucket, consequence class, within the batch limit)    paradigm set_algebra
  solver B   solver_b.py: its own parser of the RENDERED row (card regex, four listing containers, skin template);
             the entries go into an in-memory sqlite table, the distinct matches are a GROUP BY over the normalised
             key, the consequence class is a lookup in an action table parsed from the card and the step is one SQL
             CASE expression                                                                      paradigm sql_sqlite
  samplers   S1 forward; S2 label-first with boosted near misses; S3 table-first (listing before the request);
             S4 agent transcript (the listing is a tool output); S5 held out (held-out record types, CSV listing,
             held-out skins)
  questions  ch_next (go ahead / ask closed, plus stop as the abstain-role option on a planned display draw);
             ch_target (which entry, open set from error models plus the abstain option "no single entry"); both
             take their display from choice_plan(): the abstain-role option is gold on 1/k of the rows that show it
             (kit choiceplan; G0 S9, S10). yes/no on predicate "proceed": yn_proceed, yn_no_hold (double
             negation, positive), complements yn_hold (option framing) and yn_not_proceed (syntactic); on predicate
             "ask": yn_ask, complement yn_settle (option framing)
  relations  complement; minimal-edit twin (one slot: the action, the batch limit, the letter-case rule, one entry's
             key or one entry's name); equiv (another skin, register and listing container); inv (an inert note in
             the tool output); G4 metamorphic (reverse the listing, shift dates, rename the requester, add an inert
             entry, rename the requested name with its matches)
The gold never depends on the dates (recency is a decoy), on the order of the listing or on the requester.
Fix iteration 1 (14 Oct 2026, PILOT_VERDICT F1-F4 + kit choiceplan / cards / polarity): the display plans above; the
rules sit in row.card on yes/no rows and the card is shorter (cards.place_rules); twins are drawn so that their gold
shares stay at the cell shares and keep their base's display (TWIN_NEXT, TWIN_NONE_KEEP, YN_REACH); every listing shows
exactly two distinct names whatever the answer; yes/no wordings are screened by c2_kit.polarity (ctx_for).
Code only: nothing here writes a file (A37 f).
"""
from __future__ import annotations

import datetime as dt
import random
from dataclasses import dataclass, replace
from functools import lru_cache
from pathlib import Path

from c2_kit import cards as CARDS
from c2_kit import polarity as POL
from c2_kit import skin as K
from c2_kit import slots as S
from c2_kit.choiceplan import ChoicePlan
from c2_kit.distractors import (build_closed, build_options, error_model, gold_position, register_name, target_rank,
                                uhash)
from c2_kit.plugin import C2Plugin, ContractError, QuestionForm, RelationProposal, Spec, choose_forms
from c2_kit.relations import abstain_twin_kept
from c2_kit.rows import TextBuilder, assemble_row

HERE = Path(__file__).resolve().parent
FAMILY = "T30"

# ------------------------------------------------------------------------------------------------ closed pools
# Program-side seed pools (G0_SPEC.md 2). After A38 they are expanded from Haiku seed pools by program (spec 3.5).
FIRST_NAMES = ("Priya", "Omar", "Lena", "Ravi", "Mira", "Aiko", "Felix", "Grace", "Hugo", "Ines", "Keiko", "Leon",
               "Maya", "Nadia", "Oscar", "Paula", "Quinn", "Rosa", "Sanjay", "Tara", "Uma", "Victor", "Wren", "Yusuf",
               "Zara", "Amara", "Bruno", "Chloe", "Diego", "Farah", "Gideon", "Hana", "Ivan", "Kofi", "Lucia", "Petra",
               "Selin", "Teo", "Noor", "Imani")
NICK_PAIRS = (("Kate", "Katherine"), ("Mike", "Michael"), ("Liz", "Elizabeth"), ("Tom", "Thomas"), ("Bob", "Robert"),
              ("Sam", "Samantha"), ("Alex", "Alexander"), ("Jim", "James"), ("Dan", "Daniel"), ("Nick", "Nicholas"),
              ("Chris", "Christopher"), ("Ben", "Benjamin"), ("Andy", "Andrew"), ("Becky", "Rebecca"),
              ("Jen", "Jennifer"), ("Tony", "Anthony"), ("Jon", "John"), ("Sara", "Sarah"), ("Steven", "Stephen"),
              ("Ann", "Anne"), ("Eric", "Erik"))
PERSON_REFS = FIRST_NAMES + tuple(n for p in NICK_PAIRS for n in p)
LAST_NAMES = ("Shah", "Okafor", "Lindqvist", "Moreau", "Castell", "Brandt", "Ferreira", "Whitcombe", "Anand", "Novak",
              "Haddad", "Kowalski", "Mensah", "Tanaka", "Rossi", "Byrne", "Duarte", "Iqbal", "Jansen", "Kim", "Laine",
              "Murphy", "Nakamura", "Osei", "Petrov", "Reyes", "Sato", "Vance", "Walsh", "Yilmaz", "Zhou", "Abbott")
TEAMS = ("Platform", "Design", "Growth", "Finance", "Support", "Security", "Data", "Mobile", "Research", "Legal")
BANKS = ("Harbor Bank", "Granite Credit Union", "Lakeside Savings", "Summit Trust", "Riverbend Bank", "Cobalt Bank")
BRANDS = ("Northpeak", "Fernway", "Lumen", "Cedarline", "Bluepeak", "Harbor Goods")
LOCATIONS = ("Lab West", "Lab East", "Main Office", "Data Hall", "Annex", "Warehouse")
ORGS = ("acme", "northwind", "harbor", "bluepeak", "cedarline", "fernway", "granite", "lumen", "kestrel", "orchard")
FOLDERS = ("finance", "sales", "legal", "design", "ops", "people", "marketing", "research")
REQUESTERS = ("Morgan Ellis", "Jordan Pike", "Casey Lund", "Riley Shaw", "Avery Stone", "Harper Quill", "Rowan Frost",
              "Skyler Mercer", "Emerson Hale", "Logan Brooks")
DETAIL_POOLS = {"last": LAST_NAMES, "team": TEAMS, "bank": BANKS, "brand": BRANDS, "location": LOCATIONS}


@dataclass(frozen=True)
class RecordType:
    """One record type (a domain pack seed): nouns, the four listing labels (match field, detail, identity key, date),
    the key kind, the six action phrases (each is followed by the name in a request) and the name pools."""
    key: str
    noun: tuple                  # (singular, plural)
    labels: tuple                # (match field, detail field, identity key, date field)
    key_kind: str                # email | path | url | id
    low: tuple                   # low-consequence action phrases
    cons: tuple                  # consequential action phrases
    details: str = "last"        # detail pool (DETAIL_POOLS key, or "owner": a generated full name)
    id_pattern: str = ""         # id keys: "#" is a digit
    person: bool = True          # match field is a first name (nickname traps); else a title (near-miss traps)
    titles: tuple = ()
    near: tuple = ()             # (title, near-miss title) pairs; near-miss titles are never in `titles`
    held_out: bool = False       # S5 only

    @property
    def action_set(self) -> dict:
        return {p: [p] for p in self.low + self.cons}

    def cls(self, phrase: str) -> str:
        if phrase in self.low:
            return "low"
        if phrase in self.cons:
            return "cons"
        raise ContractError(f"{phrase!r} is not an action of {self.key}")


TYPES = {t.key: t for t in (
    RecordType("contact", ("contact", "contacts"), ("first name", "last name", "email", "last contacted"), "email",
               ("look up the phone number of", "draft an email to", "search old emails from"),
               ("send a payment to", "delete the contact card of", "share the client folder with")),
    RecordType("teammate", ("workspace member", "workspace members"), ("display name", "team", "member id",
                                                                       "last active"), "id",
               ("look up the profile of", "draft a direct message to", "search the threads with"),
               ("remove the workspace access of", "transfer the project ownership to", "share the payroll sheet with"),
               details="team", id_pattern="U#######"),
    RecordType("payee", ("payee", "payees"), ("payee name", "bank", "payee id", "last paid"), "id",
               ("look up the saved details of", "draft a payment note for", "search past transfers to"),
               ("send a transfer to", "delete the saved payee", "share the bank statement with"),
               details="bank", id_pattern="PAY-####"),
    RecordType("user", ("user account", "user accounts"), ("first name", "last name", "user id", "last sign in"), "id",
               ("look up the sign-in history of", "draft a password reset note for", "search the audit log for"),
               ("deactivate the account of", "grant admin rights to", "wipe the laptop of"),
               id_pattern="usr_#####"),
    RecordType("order", ("order", "orders"), ("customer first name", "customer last name", "order number",
                                              "order date"), "id",
               ("look up the shipping status of the order from", "draft a delay notice for the order from",
                "search the notes on the order from"),
               ("refund the order from", "cancel the order from", "change the delivery address on the order from"),
               id_pattern="ORD-#####"),
    RecordType("file", ("file", "files"), ("file name", "owner", "path", "last modified"), "path",
               ("open the file", "preview the file", "search inside the file"),
               ("delete the file", "send the outside auditor the file", "overwrite the file"), details="owner",
               person=False,
               titles=("budget-review.xlsx", "roadmap.pdf", "vendor-list.csv", "onboarding-guide.docx",
                       "pricing-model.xlsx", "launch-plan.pptx", "travel-policy.pdf", "hiring-tracker.xlsx",
                       "brand-assets.zip", "meeting-notes.docx", "invoice-template.docx", "board-deck.pptx"),
               near=(("budget-review.xlsx", "budget-review.xls"), ("roadmap.pdf", "roadmap-old.pdf"),
                     ("vendor-list.csv", "vendor-lists.csv"), ("launch-plan.pptx", "launch-plan-draft.pptx"),
                     ("travel-policy.pdf", "travel-policies.pdf"), ("board-deck.pptx", "board-deck-final.pptx"))),
    RecordType("document", ("document", "documents"), ("title", "owner", "doc id", "last edited"), "id",
               ("read the document", "summarize the document", "search the document"),
               ("delete the document", "publish the document", "turn on public link sharing for the document"),
               details="owner", id_pattern="DOC-#####", person=False,
               titles=("Launch plan", "Pricing memo", "Team charter", "Security review", "Partner brief", "Style guide",
                       "Hiring plan", "Product spec", "Research summary", "Event checklist"),
               near=(("Launch plan", "Launch plans"), ("Style guide", "Style guide notes"),
                     ("Pricing memo", "Pricing memos"), ("Product spec", "Product specs"))),
    RecordType("meeting", ("meeting", "meetings"), ("title", "organizer", "event id", "meeting date"), "id",
               ("show the agenda of the meeting", "draft notes for the meeting",
                "look up the attendees of the meeting"),
               ("cancel the meeting", "delete the meeting", "invite the outside vendor to the meeting"),
               details="owner", id_pattern="evt-#####", person=False,
               titles=("Design sync", "Budget review", "Partner call", "Sprint planning", "Hiring panel",
                       "Roadmap review", "Customer demo", "Team retro", "Vendor check-in"),
               near=(("Design sync", "Design sync prep"), ("Partner call", "Partner calls"),
                     ("Customer demo", "Customer demo dry run"), ("Team retro", "Team retro follow-up"))),
    RecordType("repository", ("repository", "repositories"), ("repository name", "owner team", "url", "last push"),
               "url",
               ("read the readme of the repository", "search the code in the repository",
                "draft an issue for the repository"),
               ("delete the repository", "archive the repository", "force-push to the main branch of the repository"),
               details="team", person=False,
               titles=("billing-service", "web-app", "data-pipeline", "auth-gateway", "mobile-client", "docs-site",
                       "search-indexer", "infra-config"),
               near=(("web-app", "web-apps"), ("billing-service", "billing-services"),
                     ("docs-site", "docs-site-legacy"),
                     ("auth-gateway", "auth-gateway-old"))),
    RecordType("product", ("product listing", "product listings"), ("product name", "brand", "sku", "last restocked"),
               "id", ("look up the stock level of", "draft a description for", "search the reviews of"),
               ("delete the listing for", "change the price of", "issue refunds to the buyers of"),
               details="brand", id_pattern="SKU-#####", person=False,
               titles=("Canvas tote", "Trail flask", "Desk lamp", "Wool beanie", "Travel mug", "Linen apron",
                       "Garden gloves", "Notebook set", "Rain jacket"),
               near=(("Travel mug", "Travel mugs"), ("Desk lamp", "Desk lamp shade"),
                     ("Canvas tote", "Canvas tote bag"),
                     ("Rain jacket", "Rain jackets"))),
    # held out (S5 only): mixdev record types
    RecordType("ticket", ("ticket", "tickets"), ("title", "reporter", "ticket id", "last updated"), "id",
               ("read the history of the ticket", "draft a reply on the ticket", "search the comments on the ticket"),
               ("close the ticket", "delete the ticket", "send the outside vendor the ticket"),
               details="owner", id_pattern="TCK-####", person=False, held_out=True,
               titles=("Login page error", "Export times out", "Invoice totals wrong", "Search is slow",
                       "Broken image links", "Password reset loop", "Dark mode glitch", "Upload stalls"),
               near=(("Login page error", "Login page errors"), ("Search is slow", "Search is slow again"),
                     ("Upload stalls", "Upload stalls on mobile"))),
    RecordType("device", ("device", "devices"), ("host label", "location", "asset tag", "last seen"), "id",
               ("check the uptime of", "look up the owner of", "draft a maintenance note for"),
               ("reboot", "wipe", "decommission"),
               details="location", id_pattern="AT-####", person=False, held_out=True,
               titles=("build-runner", "edge-router", "lab-printer", "file-server", "kiosk-east", "backup-node",
                       "badge-reader", "media-encoder"),
               near=(("build-runner", "build-runners"), ("file-server", "file-server-old"),
                     ("edge-router", "edge-router-spare"))),
)}
TRAIN_TYPES = tuple(k for k, t in TYPES.items() if not t.held_out)
HELD_TYPES = tuple(k for k, t in TYPES.items() if t.held_out)
KEY_PIN = {"email": "raw", "path": "raw", "url": "full", "id": "raw"}       # JSON / CSV containers pin the key form

# ------------------------------------------------------------------------------------------------ card and options
NORM_TEXT = {"fold": "with upper and lower case treated as the same",
             "exact": "with upper and lower case treated as different"}
NORM_SET = {k: [v] for k, v in NORM_TEXT.items()}
OTHER_NORM = {"fold": "exact", "exact": "fold"}
CLOSED_WORLD = "The search results are complete; only these rules decide what the agent does."
S4_PREAMBLE = "Agent step: searching the records for the name in the request.\nTool output:\n"
NOTE_PREFIX = "Note attached to the results: "
ACTION_REF = "{ACTION} {REF}"                # request skins write the name right after the action phrase (G0 S16)
STEP_TEXT = {"proceed": "Go ahead without asking the user", "ask": "Ask the user which one is meant",
             "stop": "Stop and tell the user nothing matched"}
STEPS = ("proceed", "ask", "stop")
CLOSED_STEPS = ("proceed", "ask")             # ch_next shows these two always; "stop" is the abstain-role option (G0 S9)
STOP_KEY = "stop"
NONE_KEY = "none"
NO_SINGLE_TEXT = "No single entry: none or several distinct matches"
STYLE_BY_REGISTER = {"json": "json", "ticket": "table", "log": "table", "form": "table", "transcript": "table"}
PARTS = ("NAME", "DETAIL", "KEY", "SEEN")
# The negative / antonym predicates of "go ahead" and "ask" (c2_kit.polarity P1-P3; kit item 3, T35 pilot G5-H): a
# question wording negates syntactically ("should not carry out") OR uses one of these ("hold off"), never both, so
# its literal meaning is the declared polarity of its form. negcount's own implicit cues (deny, lack, prevent ... from,
# refuse to, rule out, without ...) count too. The step names ("ask", "stop") are not negatives: yn_no_hold denies them
# on purpose with two syntactic cues ("need not ask ... need not stop").
NEGATIVE_PREDICATES = (
    r"hold(?:s|ing)?\s+off", r"(?:hold|holds|held|holding)\s+(?:\w+\s+){0,3}?back", r"refrain(?:s|ed|ing)?",
    r"abstain(?:s|ed|ing)?", r"avoid(?:s|ed|ing)?", r"declin(?:e|es|ed|ing)", r"defer(?:s|red|ring)?",
    r"stand(?:s|ing)?\s+down", r"forgo(?:es|ing)?|forwent|forgone", r"bypass(?:es|ed|ing)?",
    r"withh(?:o|e)ld(?:s|ing)?", r"skip(?:s|ped|ping)?", r"leave\s+it\s+alone", r"step\s+back",
    r"pause(?:s|d)?", r"shun(?:s|ned|ning)?", r"forbid(?:s|den|ding)?|forbade", r"prohibit(?:s|ed|ing)?",
    r"bar(?:s|red|ring)?", r"block(?:s|ed|ing)?", r"disallow(?:s|ed|ing)?",
)
CARD_STYLE = "full"                           # the one card phrasing (G0 v3 S13); rules_in_card on yes/no rows


def _quoted(phrases: tuple) -> str:
    return f'"{phrases[0]}", "{phrases[1]}" and "{phrases[2]}"'


@lru_cache(maxsize=None)
def card_spec(type_key: str) -> "CARDS.CardSpec":
    """The rule card (program text, G0_SPEC.md S13) as a kit CardSpec: a heading, five bullets, the closed-world
    sentence. Slots: {NORM} (letter-case rule) and {BATCH_MAX} (batch limit). v3 (pilot fix F2) is the v2 card
    (Haiku ambiguity pass H2, H3, H4, H10: one distinct match goes ahead for either class, the limit counts distinct
    matches, the closing sentence names the search results) with the filler words cut: about 25 tokens per copy.
    Every rule, slot, quoted phrase and number is still stated (test_card_v3_keeps_every_marker_of_v2)."""
    rt = TYPES[type_key]
    noun, pl = rt.noun
    match, _detail_label, key, _seen = rt.labels
    items = (
        CARDS.CardItem("match", full="Match: an entry matches only if its " + match + " is exactly the name in the "
                       "request, letter for letter; nicknames, short or long forms and spelling variants do not."),
        CARDS.CardItem("identity", full="Identity: entries with identical " + key + " values, {NORM}, are one "
                       + noun + "; entries with different " + key + " values are different " + pl
                       + ", whatever their other fields say."),
        CARDS.CardItem("consequence", full="Consequence: low-consequence: " + _quoted(rt.low) + ". Consequential: "
                       + _quoted(rt.cons) + "."),
        CARDS.CardItem("decision", full="Decision: no distinct match: stop and tell the user nothing matched. "
                       "Exactly one distinct match: go ahead, whatever the action. Two or more distinct matches: "
                       "consequential action: ask the user which one is meant; low-consequence action: go ahead on "
                       "all of them if there are at most {BATCH_MAX} distinct matches, otherwise ask."),
        CARDS.CardItem("dates", full="Dates never change the decision."),
    )
    return CARDS.CardSpec(FAMILY, items, heads={"full": "Rules for a request that names " + K.article(noun) + " "
                                                + noun + ":"}, tail=CLOSED_WORLD, numbered=False)


def card_template(type_key: str) -> str:
    """The rule card text with its two slots open (G0_SPEC.md S13)."""
    return card_spec(type_key).template(CARD_STYLE)


def listing_template(type_key: str, size: int, style: str) -> tuple:
    """(header line, body template, escape) of the search listing in one container (G0_SPEC.md S14)."""
    rt = TYPES[type_key]
    m, d, k, s = rt.labels
    pin = KEY_PIN[rt.key_kind]
    pl = rt.noun[1]
    idx = range(1, size + 1)
    if style == "lines":
        body = "\n".join(f"- {m}: {{E{i}_NAME}}; {d}: {{E{i}_DETAIL}}; {k}: {{E{i}_KEY}}; {s}: {{E{i}_SEEN}}"
                         for i in idx)
        return f"Search results for {pl}, in the order the tool returned them:", body, "text"
    if style == "table":
        rows = [f"| {m} | {d} | {k} | {s} |", "| --- | --- | --- | --- |"]
        rows += [f"| {{E{i}_NAME}} | {{E{i}_DETAIL}} | {{E{i}_KEY}} | {{E{i}_SEEN}} |" for i in idx]
        return f"Search results for {pl}:", "\n".join(rows), "text"
    if style == "json":
        u = [x.replace(" ", "_") for x in (m, d, k, s)]
        objs = ", ".join('{"%s": {E%d_NAME}, "%s": {E%d_DETAIL}, "%s": {E%d_KEY:%s}, "%s": {E%d_SEEN}}'
                         % (u[0], i, u[1], i, u[2], i, pin, u[3], i) for i in idx)
        return f"Search results for {pl} (JSON):", '{"results": [' + objs + "]}", "json"
    if style == "csv":
        rows = [f"{m},{d},{k},{s}"] + [f"{{E{i}_NAME}},{{E{i}_DETAIL}},{{E{i}_KEY:{pin}}},{{E{i}_SEEN:iso}}"
                                         for i in idx]
        return f"Search results for {pl} (CSV):", "\n".join(rows), "text"
    raise ContractError(f"listing style {style!r}")


def listing_style(sampler: str, register: str) -> str:
    """Label-blind container choice: S5 CSV; a JSON skin gets a JSON listing; S3 a table; else by register."""
    if sampler == "S5":
        return "csv"
    if register == "json":
        return "json"
    if sampler == "S3":
        return "table"
    return STYLE_BY_REGISTER.get(register, "lines")


# ------------------------------------------------------------------------------------------------ sampling knobs
N_CARDS, N_CARDS_HELD = 10, 4               # cards per training sampler (one record type each) / for S5
QFORM_SHARES = (("ch_next", 0.42), ("ch_target", 0.16), ("yn_proceed", 0.10), ("yn_no_hold", 0.03),
                ("yn_hold", 0.05), ("yn_not_proceed", 0.05), ("yn_ask", 0.11), ("yn_settle", 0.08))
STEP_SHARES = (("proceed", 0.42), ("ask", 0.42), ("stop", 0.16))     # ch_next gold (spec 3.5); realised by the plan
TARGET_ZERO = 0.40                          # ch_target: of the none-gold rows, share with no match (else 2-3)
P_FAIL_ASK = 0.72                           # yes/no: when the predicate fails, the other step is ask (or proceed)
SIZES, SIZES_TARGET, SIZES_TARGET_K4 = (3, 4, 4, 5, 5, 6), (4, 5, 6), (5, 5, 6)
BATCH_WEIGHTS = ((1, 0.15), (2, 0.45), (3, 0.40))
ASK_WEIGHTS = (0.6, 0.3, 0.1)               # ask rows: n = lo, lo + 1, lo + 2
P_BATCH = 0.90                              # proceed rows with a low action and limit >= 2: share with n >= 2
P_DUP_ONE, P_DUP_MANY = 0.55, 0.25          # some match listed twice (n = 1 / n >= 2)
P_VAR_ZERO, P_VAR = 0.35, 0.04              # a nickname or near-miss entry (n = 0 / n >= 1)
P_SAME_DETAIL = 0.15                        # two distinct matches share the detail (same full name, other key)
P_CASE_SPLIT = 0.30                         # exact rule: a second distinct match differs from the first by case only
P_CASE_DUP = 0.50                           # fold rule: a duplicate is written in another letter case
S2_BOOST = 0.20                             # S2 label-first: every near-miss probability raised
COMP_RATE, EQUIV_RATE, INV_RATE = 0.40, 0.14, 0.08
# Twin mix (pilot fix F3). A twin's gold is the answer its one edit constructs, so the twin population must not drift
# from the family's gold shares: the options-only and metadata baselines (G6, G7) read any such drift as signal. Twins
# keep their base's option display (a closed set is identical, G-TW; an open set keeps k and shows the abstain option
# only when its base showed it), so a twin never moves the gold onto an option its base hid.
# ch_next: spawn rate and target weights by (k, base step), calibrated on the measured reach of each edit (P -> stop is
# reachable on about 25% of proceed bases, P -> ask 96%, A -> P 80%, stop -> P 100%) so that within every (k, shown)
# cell the twins' gold shares are equal: proceed / ask 1/2 at k = 2, 1/3 each at k = 3 (test_twin_gold_shares).
TWIN_NEXT = {
    (2, "proceed"): (0.71, {"ask": 1.0}),
    (2, "ask"): (0.80, {"proceed": 1.0}),
    (3, "proceed"): (1.00, {"ask": 0.206, "stop": 0.794}),
    (3, "ask"): (0.11, {"proceed": 1.0}),
    (3, "stop"): (0.11, {"proceed": 1.0}),
}
TWIN_YN = 0.60                              # yes/no: share of bases tried (the flip is yes <-> no; no target to draw)
# yes/no: the measured share of bases (by base answer 0 / 1) that have a twin edit; the direction that is easier to
# reach is thinned to the harder one's reach, so a form's twins are half yes, half no
YN_REACH = {"yn_proceed": (0.900, 0.975), "yn_no_hold": (0.899, 0.970), "yn_hold": (0.974, 0.915),
            "yn_not_proceed": (0.973, 0.913), "yn_ask": (0.708, 0.840), "yn_settle": (0.839, 0.690)}
# ch_target twins that move the gold onto "No single entry" are kept at this rate by plan.k (kit relations.
# abstain_twin_kept; the twin search then looks for an edit that names another entry), so the abstain key stays at 1/k
# in the (k, shown) cells over ALL emitted rows (unthinned twins were 85% abstain and lifted the row share to 39%).
TWIN_NONE_KEEP = {3: 0.20, 4: 0.10}
TWIN_TARGET = 0.50                          # ch_target: share of abstain-showing bases tried
FREE_OPTIONS = "plan:free"                  # spec marker: a twin / G4 variant builds options without the length rank
MARKERS = (FREE_OPTIONS,)
# Choice display plans (c2_kit.choiceplan; pilot fixes F1 and the kit's abstain lesson): the abstain-role option is
# gold on 1/k of the rows that show it, in every (k, shown) cell, and the show rate sets its overall gold share.
SHOW_STOP = 0.55                            # ch_next: "stop" shown on 55% of bases, gold on 1/3 of them: 18% of bases and
#                                             16% of the emitted rows (spec 3.5): the k = 2 cell has more twins
SHOW_TARGET = 0.70                          # ch_target: "No single entry" shown on 70%; 1/k gold: 20.4% of the rows
TARGET_K = (3, 4)                           # ch_target option counts (label-blind draw; G0 S10)
MAX_SIZE = 7
BIG = 99
TRIES = 400                                 # structure draws under a fixed plan (c2_kit.choiceplan.realize uses 400)

# Error models (every wrong option names one; G0_SPEC.md S17).
for _name, _text in (
        ("dedup_count_entries", "counts the entries that carry the name instead of the distinct identity keys"),
        ("dedup_opposite_case_rule", "compares identity keys with the opposite letter-case rule"),
        ("dedup_nickname_counts", "counts a nickname, short or long form or spelling variant of the name as a match"),
        ("dedup_ignore_consequence", "treats every action as low-consequence"),
        ("dedup_ignore_batch_limit", "goes ahead on all distinct matches of a low-consequence action, whatever the "
                                     "batch limit"),
        ("dedup_ask_on_repeated_name", "asks whenever two or more entries carry the name, even when they are one "
                                       "record"),
        ("dedup_guess_most_recent", "acts on the most recently dated match instead of asking"),
        ("dedup_guess_on_no_match", "goes ahead with a guessed entry (a near name or the latest) when no entry "
                                    "matches exactly"),
        ("dedup_stop_on_duplicates", "treats duplicate entries of one record as conflicting data and stops"),
        ("dedup_always_confirm", "asks the user before acting, whatever the number of distinct matches"),
        ("dedup_ask_on_no_match", "asks the user instead of stopping when no entry matches"),
        ("dedup_stop_on_ambiguity", "stops instead of asking or going ahead when several distinct records match"),
        ("dedup_full_name_match", "compares the requested name with the full name (first and last) instead of the "
                                  "stated name field"),
        ("dedup_first_listed", "takes the first listed entry as the target"),
        ("dedup_last_listed", "takes the last listed entry as the target"),
        ("dedup_most_recent_entry", "takes the most recently dated entry as the target, whatever its name"),
        ("dedup_oldest_entry", "takes the oldest dated entry as the target, whatever its name")):
    register_name(_name, _text)


# ------------------------------------------------------------------------------------------------ facts
@dataclass(frozen=True)
class Entry:
    name: str
    detail: str
    key: str
    seen: dt.date


@dataclass(frozen=True)
class Facts:
    rt: RecordType
    entries: tuple
    ref: str
    action: str
    cls: str
    norm: str
    b: int
    user: str


def facts(spec: Spec) -> Facts:
    v = spec.env()
    rt = TYPES[spec.structure["type"]]
    es = tuple(Entry(v[f"E{i}_NAME"], v[f"E{i}_DETAIL"], v[f"E{i}_KEY"], v[f"E{i}_SEEN"])
               for i in range(1, spec.structure["entries"] + 1))
    return Facts(rt, es, v["REF"], v["ACTION"], rt.cls(v["ACTION"]), v["NORM"], v["BATCH_MAX"], v["USER"])


def _variants(rt: RecordType, name: str) -> set:
    pairs = NICK_PAIRS if rt.person else rt.near
    return {b if a == name else a for a, b in pairs if name in (a, b)}


def _ident(key: str, norm: str) -> str:
    return key.lower() if norm == "fold" else key


def _groups(entries, ref: str, norm: str, also=()) -> dict:
    """Construction side (twins, error models, tags): {identity: [positions]} of the entries named `ref` (or a name in
    `also`), in listing order. Solver A does not use this (it is a frozenset over a generator)."""
    out: dict = {}
    for i, e in enumerate(entries):
        if e.name == ref or e.name in also:
            out.setdefault(_ident(e.key, norm), []).append(i)
    return out


def _decide(n: int, cls: str, b: int) -> str:
    if n == 0:
        return "stop"
    if n == 1:
        return "proceed"
    return "ask" if cls == "cons" or n > b else "proceed"


def _predict(qform: str, idents: list, cls: str, b: int):
    """The answer a construction implies (twin predictions): from the identity list, the class and the limit."""
    if qform == "ch_target":
        return idents[0] if len(idents) == 1 else NONE_KEY
    step = _decide(len(idents), cls, b)
    if qform == "ch_next":
        return step
    q = T30Plugin.QFORMS[qform]
    holds = step == q.predicate
    return int(holds if q.polarity == 1 else not holds)


# Solver A's own tables: (count bucket 0 / 1 / 2+, class, count <= limit) -> step; question -> answer.
DECISION_TABLE = {
    (0, "low", True): "stop", (0, "low", False): "stop", (0, "cons", True): "stop", (0, "cons", False): "stop",
    (1, "low", True): "proceed", (1, "low", False): "proceed", (1, "cons", True): "proceed",
    (1, "cons", False): "proceed",
    (2, "low", True): "proceed", (2, "low", False): "ask", (2, "cons", True): "ask", (2, "cons", False): "ask",
}
QUESTION_TABLE = {
    "ch_next": lambda step: step,
    "yn_proceed": lambda step: 1 if step == "proceed" else 0,
    "yn_no_hold": lambda step: 1 if step == "proceed" else 0,
    "yn_hold": lambda step: 0 if step == "proceed" else 1,
    "yn_not_proceed": lambda step: 0 if step == "proceed" else 1,
    "yn_ask": lambda step: 1 if step == "ask" else 0,
    "yn_settle": lambda step: 0 if step == "ask" else 1,
}


# ------------------------------------------------------------------------------------------------ helpers
def _kronecker(d: int) -> tuple:
    """The R_d sequence's increments (1/phi, 1/phi^2, ...) with phi^(d + 1) = phi + 1: jointly low-discrepancy in d
    dimensions, so every cell the plan draws (qform x display x gold x rank) holds its share on any run of seeds."""
    phi = 2.0
    for _ in range(200):
        phi = (1.0 + phi) ** (1.0 / (d + 1))
    return tuple(phi ** -(j + 1) for j in range(d))


WEYL_ALPHAS = _kronecker(9)
W_GOLD, W_QFORM, W_SHOW, W_K, W_RANK, W_COMP, W_EXTRA, W_TWIN, W_TWIN_TARGET = range(9)


def _weyl(seed: int, sampler: str, which: int) -> float:
    """Low-discrepancy draw per seed (gold, question form, display, option count, length rank, and the unit-level
    relation draws: complement, equiv / inv, twin, twin target): shares hold tightly on any run of seeds, so a
    1,000-row pilot does not drift from the G10 bands by chance. Each draw is a function of the row key's parts only
    (never of the structure drawn after it)."""
    return (seed * WEYL_ALPHAS[which] + uhash(FAMILY, "weyl", sampler, which)) % 1.0


def row_key_of(seed: int, sampler: str, qform: str) -> str:
    return f"{FAMILY}|{seed}|{sampler}|{qform}"


def choice_plan(seed: int, sampler: str, qform: str):
    """The display plan of a choice row (None for yes/no), drawn from the row key's parts before any structure
    (c2_kit.choiceplan; G0 S9, S10). ch_next: closed set proceed / ask plus the abstain-role option "stop" shown on
    SHOW_STOP of the rows (k = 3, else 2), gold on 1/k of the rows that show it. ch_target: k in TARGET_K, the
    abstain option "No single entry" shown on SHOW_TARGET of the rows, gold on 1/k of the rows that show it, and the
    gold's visible-length rank among the other options uniform. Label-first: the sampler draws a structure whose
    solver-A gold agrees with the plan; nothing is relabelled."""
    key = row_key_of(seed, sampler, qform)
    if qform == "ch_next":
        show = _weyl(seed, sampler, W_SHOW) < SHOW_STOP
        k = 3 if show else 2
        gold_abstain = bool(show and _weyl(seed, sampler, W_GOLD) < 1.0 / 3.0)
        return ChoicePlan(key, k, show, gold_abstain, gold_position(key, k), None if gold_abstain else 0,
                          1.0 / 3.0 if show else 0.0, "shuffle", 2)
    if qform == "ch_target":
        k = TARGET_K[min(len(TARGET_K) - 1, int(_weyl(seed, sampler, W_K) * len(TARGET_K)))]
        show = _weyl(seed, sampler, W_SHOW) < SHOW_TARGET
        gold_abstain = bool(show and _weyl(seed, sampler, W_GOLD) < 1.0 / k)
        n_ord = k - int(show)
        rank = None if gold_abstain else min(n_ord - 1, int(_weyl(seed, sampler, W_RANK) * n_ord))
        return ChoicePlan(key, k, show, gold_abstain, gold_position(key, k), rank, 1.0 / k if show else 0.0,
                          "shuffle", None)
    return None


def _share(table: tuple, u: float) -> str:
    acc = 0.0
    for k, w in table:
        acc += w
        if u < acc:
            return k
    return table[-1][0]


def _weighted(rng: random.Random, items: list):
    total = sum(w for _, w in items)
    x, acc = rng.random() * total, 0.0
    for k, w in items:
        acc += w
        if x < acc:
            return k
    return items[-1][0]


def _card_rate(sampler: str, card: int) -> float:
    """Per-card gold-yes rate in [0.2, 0.8] (spec 3.0); cards come in antithetic pairs, so the mean is 0.5."""
    h = uhash(FAMILY, "card_rate", sampler, card // 2)
    return 0.2 + 0.6 * (h if card % 2 == 0 else 1.0 - h)


def _detail(rng: random.Random, rt: RecordType, avoid=()) -> str:
    pool = DETAIL_POOLS.get(rt.details)
    if pool is None:
        while True:
            d = f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}"
            if d not in avoid:
                return d
    return rng.choice([d for d in pool if d not in avoid])


def _new_key(rng: random.Random, rt: RecordType, name: str, detail: str, used: set) -> str:
    """A fresh identity key, distinct from every key in `used` after case folding (added to `used`)."""
    for _ in range(200):
        if rt.key_kind == "email":
            local = f"{name}.{detail}" if rng.random() < 0.7 else f"{name[0]}{detail}"
            k = f"{local}@{rng.choice(ORGS)}.example".lower()
        elif rt.key_kind == "path":
            k = f"/{rng.choice(FOLDERS)}/{name}"
        elif rt.key_kind == "url":
            k = f"https://git.example/{rng.choice(ORGS)}/{name}"
        else:
            k = "".join(str(rng.randrange(10)) if c == "#" else c for c in rt.id_pattern)
        if k.lower() not in used:
            used.add(k.lower())
            return k
    raise ContractError(f"{rt.key}: no fresh key for {name!r}")


def _case_variant(key: str, kind: str) -> str:
    """The same key in another letter case (equal under the fold rule, different under the exact rule)."""
    if kind == "email":
        local, dom = key.split("@", 1)
        out = ".".join(p[:1].upper() + p[1:] for p in local.split(".")) + "@" + dom
    elif kind == "path":
        parts = key.split("/")
        parts[1] = parts[1].capitalize()
        out = "/".join(parts)
    elif kind == "url":
        parts = key.split("/")
        parts[3] = parts[3].capitalize()
        out = "/".join(parts)
    else:
        out = key.swapcase()
    if out == key or out.lower() != key.lower():
        raise ContractError(f"no case variant for {key!r}")
    return out


def _key_slot(rt: RecordType, key: str) -> S.Slot:
    if rt.key_kind in ("email", "path"):
        return S.glob_slot(key)
    if rt.key_kind == "url":
        return S.url_slot(key)
    return S.id_slot(key)


def _pick_ref(rng: random.Random, rt: RecordType, variant: bool) -> tuple:
    if not variant:
        return rng.choice(PERSON_REFS if rt.person else rt.titles), None
    a, b = rng.choice(NICK_PAIRS if rt.person else rt.near)
    return (a, b) if rng.random() < 0.5 else (b, a)


def _other_names(rng: random.Random, rt: RecordType, ref: str, var, k: int) -> list:
    """k distinct non-matching names that are neither the requested name nor one of its variants."""
    bad = {ref, var} | _variants(rt, ref)
    pool = [x for x in (FIRST_NAMES if rt.person else rt.titles) if x not in bad]
    return rng.sample(pool, k)


def _fresh_name(rng: random.Random, rt: RecordType, avoid: set):
    """A name outside `avoid` that is no variant of any name in `avoid` (G4 renames, inert entries)."""
    pool = [x for x in (FIRST_NAMES if rt.person else rt.titles)
            if x not in avoid and not (_variants(rt, x) & avoid)]
    return rng.choice(pool) if pool else None


def _distinct(rng: random.Random, qform: str, step: str, low: bool, b: int, size: int) -> int:
    """The number of distinct matches n that realises the target (every target is feasible in every cell)."""
    if qform == "ch_target":
        if step == "one":
            return 1
        if step == "zero":
            return 0
        return rng.choice([k for k in (2, 3) if k <= size - 2])
    if step == "stop":
        return 0
    if step == "proceed":
        return rng.randint(2, b) if low and b >= 2 and rng.random() < P_BATCH else 1
    lo = b + 1 if low else 2
    return _weighted(rng, list(zip(range(lo, min(4, size - 1) + 1), ASK_WEIGHTS)))


# ------------------------------------------------------------------------------------------------ the plugin
class T30Plugin(C2Plugin):
    FAMILY = FAMILY
    TIER = "agent"
    G0_LITE = HERE / "G0_SPEC.md"
    G0_SHA256 = "ff45fbb0700a8a6e729261b5e30398fcf8d8360407141a9f77f1aebc2f84a181"   # frozen v3 (14 Oct 2026; v2 bddfd817...)
    G0_AMBIGUITY_PASS = ("c2-data-stage-a amb:T30 (Haiku 5.5, 13 Oct 2026; 37 points H1-H37; "
                         "haiku/ambiguity/amb_T30.json)")
    SAMPLERS = ("S1", "S2", "S3", "S4", "S5")
    HELD_OUT_SAMPLERS = ("S5",)
    PARADIGM_A = "set_algebra"
    PARADIGM_B = "sql_sqlite"
    SOLVER_B_MODULE = "families.T30.solver_b"
    QFORMS = {q.qform: q for q in (
        QuestionForm("ch_next", "choice", answer_set="closed", abstain=True),
        QuestionForm("ch_target", "choice", answer_set="open", abstain=True),
        QuestionForm("yn_proceed", "noul", "proceed", 1, yes_is_bad=False),
        QuestionForm("yn_no_hold", "noul", "proceed", 1, yes_is_bad=False),
        QuestionForm("yn_hold", "noul", "proceed", -1, "option_framing", yes_is_bad=True),
        QuestionForm("yn_not_proceed", "noul", "proceed", -1, "syntactic", yes_is_bad=True),
        QuestionForm("yn_ask", "noul", "ask", 1, yes_is_bad=True),
        QuestionForm("yn_settle", "noul", "ask", -1, "option_framing", yes_is_bad=False),
    )}
    LABEL_WORDS = ("proceed", "go ahead", "ask", "clarify", "clarifying", "stop", "nothing matched",
                   "which one is meant", "no single entry")
    CLOSED_WORLD_SENTENCE = CLOSED_WORLD
    REGISTERS = ("memo", "chat", "email", "ticket", "json", "yaml", "log", "form", "transcript", "voicemail")
    HELD_OUT_REGISTERS = ("transcript", "voicemail")
    GSL_EXCEPTIONS: dict = {}
    NAME_ALLOW = ("Agent",)
    POLARITY_CHECK = True                 # c2_kit.polarity: yes/no wordings must read with their form's polarity
    POLARITY_NEGATIVES = NEGATIVE_PREDICATES

    def __init__(self, lexicon=None):
        super().__init__(lexicon)
        self._screened: list = []         # [(ctx, screened ctx, {wording id: problems})]

    def ctx_for(self, spec, ctx):
        """The kit context without the wordings that break the polarity rule (c2_kit.polarity), so neither render()
        nor the pipeline's complement partner can pick one. Label-blind (reads wordings, never a row); cached."""
        for c, screened, _bad in self._screened:
            if c is ctx:
                return screened
        screened, bad = POL.screen(ctx, self)
        self._screened.append((ctx, screened, bad))
        return screened

    def quarantined_wordings(self, ctx) -> dict:
        """{wording skin id: polarity problems} for the wordings ctx_for() leaves out of `ctx`."""
        self.ctx_for(None, ctx)
        return next(bad for c, _s, bad in self._screened if c is ctx)

    # ------------------------------------------------------------------------------------------- sampling
    def sample(self, seed: int, sampler: str) -> Spec:
        if sampler not in self.SAMPLERS:
            raise ContractError(f"sampler {sampler}")
        rng = random.Random(f"{FAMILY}|{sampler}|{seed}")
        held = sampler in self.HELD_OUT_SAMPLERS
        pool = HELD_TYPES if held else TRAIN_TYPES
        card = seed % (N_CARDS_HELD if held else N_CARDS)
        rt = TYPES[pool[card % len(pool)]]
        qform = _share(QFORM_SHARES, _weyl(seed, sampler, W_QFORM))
        plan = choice_plan(seed, sampler, qform)                 # the choice display, before any structure (G0 S9, S10)
        boost = S2_BOOST if sampler == "S2" else 0.0
        # display and rule draws first (label-blind): listing size, batch limit, action, letter-case rule, requester
        # ch_target: the listing is large enough for the planned option count (k - 1 wrong keys from distinct entries
        # when the abstain option is hidden); the size depends on the plan's k only, never on the gold
        low = rng.random() < 0.5
        b = _weighted(rng, list(BATCH_WEIGHTS))
        # the listing is never all matches (F4: two distinct names whatever the answer): on a low-consequence row the
        # most matches any answer needs is b + 1 (ask), so its size is at least b + 2 (a function of the class and the
        # limit, both drawn before the answer)
        sizes = SIZES_TARGET_K4 if qform == "ch_target" and plan.k >= 4 else (
            SIZES_TARGET if qform == "ch_target" else SIZES)
        size = rng.choice([x for x in sizes if x >= (b + 2 if low else 3)])
        action = rng.choice(rt.low if low else rt.cons)
        norm = "fold" if rt.key_kind == "email" else rng.choice(("fold", "exact"))
        user = rng.choice(REQUESTERS)
        # then the target answer, then a listing that realises it (a ch_target listing the drawn option count cannot
        # fill is redrawn from the same stream: G0 S10)
        for _ in range(TRIES):
            step = self._target(qform, _weyl(seed, sampler, W_GOLD), _card_rate(sampler, card), rng, plan)
            n = _distinct(rng, qform, step, low, b, size)
            ref, rows = self._entries(rng, rt, qform, n, size, norm, boost)
            days = rng.sample(range(0, 350), size)
            slots = {"USER": S.name_slot(user), "REF": S.name_slot(ref),
                     "ACTION": S.category_slot(action, rt.action_set), "NORM": S.category_slot(norm, NORM_SET),
                     "BATCH_MAX": S.count_slot(b)}
            for i, (nm, det, key) in enumerate(rows, 1):
                slots[f"E{i}_NAME"] = S.name_slot(nm)
                slots[f"E{i}_DETAIL"] = S.name_slot(det)
                slots[f"E{i}_KEY"] = _key_slot(rt, key)
                slots[f"E{i}_SEEN"] = S.date_slot(dt.date(2026, 1, 1) + dt.timedelta(days=days[i - 1]))
            spec = self.derive(Spec(FAMILY, sampler, seed, f"{FAMILY}:{sampler}:c{card:02d}", qform, slots,
                                    structure={"type": rt.key, "entries": size}, depth=2,
                                    pack=f"t30.{rt.key}.{sampler}.c{card:02d}"))
            if self._options_ok(spec):
                return spec
        raise ContractError(f"no ch_target listing fills the planned options (seed {seed} / {sampler})")

    def _target(self, qform: str, u: float, rate: float, rng: random.Random, plan=None) -> str:
        """The target before any listing exists: a step (ch_next, yes/no) or a match class (ch_target). A choice row
        takes its target from the display plan: the abstain-role answer iff the plan says so, else the other answers
        (ch_next: proceed / ask halves of the same low-discrepancy draw; ch_target: exactly one distinct match)."""
        if qform == "ch_next":
            if plan.gold_abstain:
                return "stop"
            return "proceed" if u < (2.0 / 3.0 if plan.show_abstain else 0.5) else "ask"
        if qform == "ch_target":
            if plan.gold_abstain:
                return "zero" if rng.random() < TARGET_ZERO else "many"
            return "one"
        q = self.QFORMS[qform]
        yes = u < rate
        holds = yes if q.polarity == 1 else not yes
        if q.predicate == "proceed":
            return "proceed" if holds else ("ask" if rng.random() < P_FAIL_ASK else "stop")
        return "ask" if holds else ("proceed" if rng.random() < P_FAIL_ASK else "stop")

    def _entries(self, rng, rt, qform, n, size, norm, boost) -> tuple:
        """(ref, [(name, detail, key)] in listing order) with exactly n distinct matches. Pilot fix F4: the listing
        always shows exactly two distinct names, whatever the answer. With a match (n >= 1) every non-matching entry
        carries one other name (a nickname or near-miss title when the trap is on); with no match (n = 0) the
        non-matching entries carry two. Before, the non-matching entries all had fresh names, so the number of distinct
        names (60% ask at one or two, 62% stop at six) gave the answer to any model that counts name tokens."""
        reserve = 2 if qform == "ch_target" else 1
        extra = 0
        if n >= 1 and rng.random() < (P_DUP_ONE if n == 1 else P_DUP_MANY) + boost:
            extra = 1 if rng.random() < 0.8 else 2
        extra = max(0, min(extra, size - n - reserve)) if n >= 1 else 0
        n_other = size - n - extra
        variant = n_other >= 1 and rng.random() < (P_VAR_ZERO if n == 0 else P_VAR) + boost
        ref, var = _pick_ref(rng, rt, variant)
        used: set = set()
        ids: list = []
        split = (n >= 2 and norm == "exact" and rt.key_kind != "email" and qform != "ch_target"
                 and rng.random() < P_CASE_SPLIT + boost)
        for j in range(n):
            if j == 1 and split:
                ids.append((ids[0][0], _case_variant(ids[0][1], rt.key_kind)))
                continue
            same = j > 0 and rng.random() < P_SAME_DETAIL + boost
            det = ids[0][0] if same else _detail(rng, rt, avoid=[d for d, _ in ids])
            ids.append((det, _new_key(rng, rt, ref, det, used)))
        out = [(ref, d, k) for d, k in ids]
        for _ in range(extra):
            d, k = ids[rng.randrange(n)]
            if norm == "fold" and rng.random() < P_CASE_DUP + boost:
                k = _case_variant(k, rt.key_kind)
            out.append((ref, d, k))
        k_names = 1 if n >= 1 else min(2, n_other)
        names = ([var] if variant else []) + _other_names(rng, rt, ref, var, k_names - int(variant))
        others = names + [rng.choice(names) for _ in range(n_other - len(names))]
        for nm in others:
            det = _detail(rng, rt)
            out.append((nm, det, _new_key(rng, rt, nm, det, used)))
        rng.shuffle(out)
        if qform == "ch_target" and n == 1 and out[0][0] == ref and out[-1][0] == ref:
            out[0], out[1] = out[1], out[0]     # keeps a non-target first or last entry (>= 1 wrong option)
        return ref, out

    def derive(self, spec: Spec) -> Spec:
        """No printed intermediates (the distinct count is the task); recompute the trap tags from the facts."""
        return spec.replace(tags=tuple(sorted(set(self._tags(spec)) | {t for t in spec.tags if t in MARKERS})))

    def _tags(self, spec: Spec) -> tuple:
        f = facts(spec)
        g = _groups(f.entries, f.ref, f.norm)
        n, m = len(g), sum(len(v) for v in g.values())
        t = set()
        if m > n:
            t.add("dup_collapse")
        if any(len({f.entries[i].key for i in v}) > 1 for v in g.values()):
            t.add("case_dup")
        if n >= 2:
            t.add("same_name_diff_id")
            dets = [f.entries[v[0]].detail for v in g.values()]
            if len(set(dets)) < len(dets):
                t.add("same_full_name")
            if len({k.lower() for k in g}) < n:
                t.add("case_split")
        if n == 0:
            t.add("no_match")
        var = _variants(f.rt, f.ref)
        if any(e.name in var for e in f.entries):
            t.add("nickname" if f.rt.person else "near_miss_name")
        if f.cls == "low" and 2 <= n <= f.b:
            t.add("low_batch_proceed")
        if f.cls == "low" and n >= 2 and n in (f.b, f.b + 1):
            t.add("batch_limit_edge")
        return tuple(sorted(t))

    # ------------------------------------------------------------------------------------------- solver A
    def solve_a(self, spec: Spec):
        f = facts(spec)
        fold = f.norm == "fold"
        ids = frozenset(e.key.casefold() if fold else e.key for e in f.entries if e.name == f.ref)
        if spec.qform == "ch_target":
            return min(ids) if len(ids) == 1 else NONE_KEY
        step = DECISION_TABLE[(min(len(ids), 2), f.cls, len(ids) <= f.b)]
        return QUESTION_TABLE[spec.qform](step)

    def canonical(self, spec: Spec) -> dict:
        f = facts(spec)
        rt = f.rt
        return {"noun": rt.noun[0], "noun_pl": rt.noun[1], "labels": list(rt.labels), "low_actions": list(rt.low),
                "cons_actions": list(rt.cons), "norm": f.norm, "batch_max": f.b, "user": f.user, "ref": f.ref,
                "action": f.action, "entries": [[e.name, e.detail, e.key, e.seen.isoformat()] for e in f.entries],
                "qform": spec.qform}

    def canonical_for(self, spec: Spec, author_mode: str) -> dict:
        if author_mode != "T":
            raise ContractError("T30 v1 is Mode T only: the decisive request slots need the template parser")
        return self.canonical(spec)

    # ------------------------------------------------------------------------------------------- render
    def render(self, spec: Spec, ctx, *, skin=None, wording=None, forms=None, attack=None):
        key = row_key_of(spec.seed, spec.sampler, spec.qform)
        held = spec.sampler in self.HELD_OUT_SAMPLERS
        ctx = self.ctx_for(spec, ctx)                  # never pick a wording that breaks the polarity rule (kit P1-P3)
        skin = skin or ctx.pick(FAMILY, "skin", key, held_out=held)
        if skin.author_mode != "T":
            raise ContractError(f"skin {skin.skin_id}: T30 v1 renders Mode T skins only")
        if ACTION_REF not in skin.text:                     # G0 S16: each action phrase ends where the name goes
            raise ContractError(f"skin {skin.skin_id}: writes {{ACTION}} and {{REF}} apart")
        if wording is None:                     # S5 prefers held-out wordings (mixdev); training rows never use them
            try:
                wording = ctx.pick(FAMILY, "wording", key, qform=spec.qform, held_out=held)
            except LookupError:
                if not held:
                    raise
                wording = ctx.pick(FAMILY, "wording", key, qform=spec.qform)
        if wording.qform != spec.qform:
            raise ContractError(f"wording {wording.skin_id} asks {wording.qform}, spec asks {spec.qform}")
        forms = forms or choose_forms(spec, key)
        slots = spec.all_slots()
        rt = TYPES[spec.structure["type"]]
        style = listing_style(spec.sampler, skin.register)
        tb = TextBuilder()

        def request():
            tb.add("state", skin.fill(slots, forms), skin_id=skin.skin_id)

        def listing():
            head, body, escape = listing_template(rt.key, spec.structure["entries"], style)
            if spec.sampler == "S4":
                tb.add("state", S4_PREAMBLE)
            tb.add("state", head + "\n").add("state", K.fill(body, slots, forms, escape=escape))
            if attack is not None:
                tb.add("state", "\n" + NOTE_PREFIX).add("state", attack.fill(slots, forms), skin_id=attack.skin_id)

        if spec.sampler == "S3":
            listing()
            tb.add("state", "\n\n")
            request()
        else:
            request()
            tb.add("state", "\n\n")
            listing()
        # the rules: yes/no rows print row.card once (the served prompt's definitions block), choice rows keep them
        # at the head of the instructions, the only place a choice row prints them (pilot fix F2; kit cards.place_rules)
        field = CARDS.place_rules(tb, K.fill(card_template(rt.key), slots, forms), self.QFORMS[spec.qform].qtype)
        tb.add("instructions", wording.fill(slots, forms), skin_id=wording.skin_id)
        ans = self.solve_a(spec)
        os_ = None
        if spec.qform == "ch_next":
            plan = choice_plan(spec.seed, spec.sampler, spec.qform)
            # the closed pair proceed / ask, plus "stop" as the abstain-role option on the plan's display draw (always
            # shown when it is the gold); the order is a label-blind permutation of the row key (twins keep it, G-TW)
            os_ = build_closed(spec, ans, list(CLOSED_STEPS), self.error_models(), row_key=key,
                               render_key=STEP_TEXT.__getitem__, abstain=(STOP_KEY, STEP_TEXT[STOP_KEY]),
                               show_abstain=plan.show_abstain)
        elif spec.qform == "ch_target":
            os_ = self._target_options(spec, ans)
            if os_ is None:
                raise K.RenderError("ch_target: too few error-model answers for the planned option count")
        return assemble_row(self, spec, tb, answer=ans, option_set=os_, skin=skin, wording=wording, forms=forms,
                            attack=attack, format_style=f"{skin.register}/{style}",
                            defs_style=CARDS.defs_style(field, CARD_STYLE),
                            edge=[t for t in spec.tags if t not in MARKERS])

    # ------------------------------------------------------------------------------------------- relations
    def _target_options(self, spec: Spec, ans):
        """The ch_target options from the display plan (G0 S10): k, the abstain display, the gold position and the
        gold's visible-length rank all come from the plan, which was drawn from the row key before the structure. A
        base row must agree with the plan (PlanMismatch otherwise: draw another structure, never relabel). A twin or a
        G4 variant (marker plan:free) adapts the plan to its constructed gold and keeps k, the display and the
        position; its options are not length-balanced (it is never a sample of the plan). None when the error models
        cannot fill the plan: the spec is resampled (sample) or the twin edit is skipped (_twin), never re-tried with
        a smaller k or with the abstain option forced on."""
        key = row_key_of(spec.seed, spec.sampler, spec.qform)
        f = facts(spec)
        surface: dict = {}
        for e in f.entries:
            surface.setdefault(_ident(e.key, f.norm), e.key)
        free = FREE_OPTIONS in spec.tags
        plan = choice_plan(spec.seed, spec.sampler, spec.qform)
        return build_options(spec, ans, self.error_models(), row_key=key, render_key=surface.__getitem__,
                             abstain=(NONE_KEY, NO_SINGLE_TEXT), plan=plan, length_balance=not free,
                             strict_plan=not free)

    def _options_ok(self, spec: Spec) -> bool:
        return spec.qform != "ch_target" or self._target_options(spec, self.solve_a(spec)) is not None

    def relations(self, spec: Spec) -> list:
        out = []
        q = self.QFORMS[spec.qform]
        if q.qtype == "noul" and _weyl(spec.seed, spec.sampler, W_COMP) < COMP_RATE:
            out.append(RelationProposal("complement", qform=self._partner(spec)))
        u = _weyl(spec.seed, spec.sampler, W_EXTRA)
        if u < EQUIV_RATE:
            out.append(RelationProposal("equiv"))
        elif u < EQUIV_RATE + INV_RATE:
            out.append(RelationProposal("inv"))
        rate, target = self._twin_draw(spec)
        if _weyl(spec.seed, spec.sampler, W_TWIN) < rate:
            t = self._twin(spec, target)
            if t is not None:
                out.append(t)
        return out + [m for m in self._metamorphic(spec) if self._options_ok(self.derive(m.spec))]

    def _partner(self, spec: Spec) -> str:
        """The complement form: same predicate, opposite polarity; syntactic pairs differ by one negation cue."""
        u = uhash(FAMILY, "complement_kind", spec.sampler, spec.seed)
        return {"yn_proceed": "yn_hold" if u < 0.6 else "yn_not_proceed", "yn_no_hold": "yn_not_proceed",
                "yn_hold": "yn_proceed", "yn_not_proceed": "yn_proceed" if u < 0.6 else "yn_no_hold",
                "yn_ask": "yn_settle", "yn_settle": "yn_ask"}[spec.qform]

    def _twin_draw(self, spec: Spec) -> tuple:
        """(spawn rate, target answer or None) of this base row's minimal-edit twin, from the row key and the display
        plan only (G0 S2 Relations). ch_next: the twin's step is drawn from the TWIN_NEXT weights of its (k, base
        step) cell; ch_target: bases that hide the abstain option have no twin (the twin would have to show it);
        yes/no: the flip is the only choice."""
        q = self.QFORMS[spec.qform]
        if q.qtype == "noul":
            reach = YN_REACH[spec.qform]
            return TWIN_YN * min(reach) / reach[self.solve_a(spec)], None
        plan = choice_plan(spec.seed, spec.sampler, spec.qform)
        if spec.qform == "ch_target":
            return (TWIN_TARGET if plan.show_abstain else 0.0), None
        rate, weights = TWIN_NEXT[(plan.k, self.solve_a(spec))]
        u, acc = _weyl(spec.seed, spec.sampler, W_TWIN_TARGET), 0.0
        for step, w in weights.items():
            acc += w
            if u < acc:
                return rate, step
        return rate, step

    def _twin(self, spec: Spec, target=None):
        """Exactly one input slot changes; the prediction comes from the edited construction (_groups + _decide),
        never from solve_a. The first edit (in a seeded order) that changes the answer is used; with `target`, the
        first edit whose predicted answer is that target."""
        f = facts(spec)
        g0 = _groups(f.entries, f.ref, f.norm)
        base = _predict(spec.qform, list(g0), f.cls, f.b)
        rng = random.Random(f"{FAMILY}|twin|{spec.sampler}|{spec.seed}")
        kinds = sorted(("action", "batch", "split", "merge", "rename_in", "rename_out", "norm"),
                       key=lambda k: uhash(FAMILY, "twin_kind", spec.sampler, spec.seed, k))
        for kind in kinds:
            edit = self._edit(kind, spec, f, g0, rng)
            if edit is None:
                continue
            slot, new, entries, cls, b, norm = edit
            want = _predict(spec.qform, list(_groups(entries, f.ref, norm)), cls, b)
            if want == base or (target is not None and want != target):
                continue
            if spec.qform == "ch_target" and not abstain_twin_kept(
                    f"{FAMILY}|{spec.sampler}|{spec.seed}", base, want, NONE_KEY,
                    TWIN_NONE_KEEP[choice_plan(spec.seed, spec.sampler, spec.qform).k]):
                continue
            twin = self.derive(spec.with_slot(slot, new).replace(tags=(*spec.tags, FREE_OPTIONS)))
            if not self._options_ok(twin):
                continue                                    # the planned option count cannot be filled on the twin
            return RelationProposal("twin", spec=twin, changed_slot=slot, expect=want, note=f"twin {kind}")
        return None

    def _edit(self, kind, spec, f, g0, rng):
        """(slot, new slot, edited entries, class, limit, letter-case rule) for one edit kind, or None."""
        rt, n, es = f.rt, len(g0), list(f.entries)
        singles = [v[0] for v in g0.values() if len(v) == 1]
        if kind == "action":
            other = "cons" if f.cls == "low" else "low"
            phrase = rng.choice(rt.cons if other == "cons" else rt.low)
            return "ACTION", S.category_slot(phrase, rt.action_set), es, other, f.b, f.norm
        if kind == "batch":
            if f.cls != "low" or n < 2:
                return None
            nb = n - 1 if n <= f.b else n
            if not 1 <= nb <= 3:
                return None
            return "BATCH_MAX", S.count_slot(nb), es, f.cls, nb, f.norm
        if kind == "split":
            dups = [i for v in g0.values() for i in v[1:]]
            if not dups:
                return None
            i = rng.choice(dups)
            k = _new_key(rng, rt, es[i].name, es[i].detail, {e.key.lower() for e in es})
        elif kind == "merge":
            if n < 2 or not singles:
                return None
            i = rng.choice(singles)
            same = [v[0] for v in g0.values() if v[0] != i and es[v[0]].detail == es[i].detail]
            if not same:
                return None
            k = es[rng.choice(same)].key
        elif kind == "rename_in":
            idents = [_ident(e.key, f.norm) for e in es]
            pool = [i for i, e in enumerate(es)
                    if e.name != f.ref and idents[i] not in g0 and idents.count(idents[i]) == 1]
            if not pool:
                return None
            i = rng.choice(pool)
            es[i] = replace(es[i], name=f.ref)
            return f"E{i + 1}_NAME", S.name_slot(f.ref), es, f.cls, f.b, f.norm
        elif kind == "rename_out":
            if not singles:
                return None
            i = rng.choice(singles)
            taken = {e.name for e in es}
            vs = sorted(_variants(rt, f.ref) - taken)
            new = vs[0] if vs else _fresh_name(rng, rt, taken | {f.ref})
            if new is None:
                return None
            es[i] = replace(es[i], name=new)
            return f"E{i + 1}_NAME", S.name_slot(new), es, f.cls, f.b, f.norm
        elif kind == "norm":
            if rt.key_kind == "email" or spec.qform == "ch_target":
                return None
            other = OTHER_NORM[f.norm]
            return "NORM", S.category_slot(other, NORM_SET), es, f.cls, f.b, other
        else:
            raise ContractError(f"twin kind {kind}")
        es[i] = replace(es[i], key=k)
        return f"E{i + 1}_KEY", _key_slot(rt, k), es, f.cls, f.b, f.norm

    def _metamorphic(self, spec: Spec) -> list:
        """G4 (checked, never emitted): order, dates, requester, an inert entry and the name itself never matter."""
        f = facts(spec)
        rt, size = f.rt, len(f.entries)
        rng = random.Random(f"{FAMILY}|g4|{spec.sampler}|{spec.seed}")
        out = []
        rev = {f"E{i}_{p}": spec.slots[f"E{size + 1 - i}_{p}"] for i in range(1, size + 1) for p in PARTS}
        free = (*spec.tags, FREE_OPTIONS)          # G4 variants are checked, never emitted: no length-rank constraint
        out.append(RelationProposal("metamorphic", spec=spec.replace(slots={**spec.slots, **rev}, tags=free),
                                    expect="same", note="reverse the listing order"))
        shift = {f"E{i}_SEEN": S.date_slot(e.seen + dt.timedelta(days=30)) for i, e in enumerate(f.entries, 1)}
        out.append(RelationProposal("metamorphic", spec=spec.replace(slots={**spec.slots, **shift}, tags=free),
                                    expect="same", note="shift every date by 30 days"))
        other = next(u for u in REQUESTERS if u != f.user)
        out.append(RelationProposal("metamorphic", spec=spec.with_slot("USER", S.name_slot(other)).replace(tags=free),
                                    expect="same", note="rename the requester"))
        names = {e.name for e in f.entries} | {f.ref} | _variants(rt, f.ref)
        if size < MAX_SIZE:
            nm = _fresh_name(rng, rt, names)
            if nm is not None:
                det = _detail(rng, rt)
                key = _new_key(rng, rt, nm, det, {e.key.lower() for e in f.entries})
                seen = max(e.seen for e in f.entries) + dt.timedelta(days=1)
                j = size + 1
                add = {f"E{j}_NAME": S.name_slot(nm), f"E{j}_DETAIL": S.name_slot(det), f"E{j}_KEY": _key_slot(rt, key),
                       f"E{j}_SEEN": S.date_slot(seen)}
                out.append(RelationProposal("metamorphic", spec=spec.replace(
                    slots={**spec.slots, **add}, structure={**spec.structure, "entries": j}, tags=free),
                    expect="same", note="add an inert, most recent entry"))
        new_ref = _fresh_name(rng, rt, names)
        if new_ref is not None:
            ren = {"REF": S.name_slot(new_ref)}
            ren.update({f"E{i}_NAME": S.name_slot(new_ref) for i, e in enumerate(f.entries, 1) if e.name == f.ref})
            out.append(RelationProposal("metamorphic", spec=spec.replace(slots={**spec.slots, **ren}, tags=free),
                                        expect="same", note="rename the requested name and every entry that carries it"))
        return out

    # ------------------------------------------------------------------------------------------- error models
    def error_models(self) -> dict:
        def on(next_fn=None, target_fn=None):
            def run(spec):
                if spec.qform == "ch_next" and next_fn is not None:
                    return next_fn(facts(spec))
                if spec.qform == "ch_target" and target_fn is not None:
                    return target_fn(facts(spec))
                return None
            return run

        def n_of(f, norm=None, also=()):
            return len(_groups(f.entries, f.ref, norm or f.norm, also))

        def carrying(f):
            return sum(e.name == f.ref for e in f.entries)

        def single(groups):
            return next(iter(groups)) if len(groups) == 1 else NONE_KEY

        def ident_at(f, i):
            return _ident(f.entries[i].key, f.norm)

        def latest(f, positions):
            return max(positions, key=lambda i: f.entries[i].seen)

        fns = {
            "dedup_count_entries": on(lambda f: _decide(carrying(f), f.cls, f.b)),
            "dedup_opposite_case_rule": on(lambda f: _decide(n_of(f, OTHER_NORM[f.norm]), f.cls, f.b)),
            "dedup_nickname_counts": on(lambda f: _decide(n_of(f, also=_variants(f.rt, f.ref)), f.cls, f.b),
                                        lambda f: single(_groups(f.entries, f.ref, f.norm, _variants(f.rt, f.ref)))),
            "dedup_ignore_consequence": on(lambda f: _decide(n_of(f), "low", f.b)),
            "dedup_ignore_batch_limit": on(lambda f: _decide(n_of(f), f.cls, BIG)),
            "dedup_ask_on_repeated_name": on(lambda f: "ask" if carrying(f) >= 2 else None),
            "dedup_guess_most_recent": on(
                lambda f: "proceed" if n_of(f) >= 2 else None,
                lambda f: ident_at(f, latest(f, [i for v in _groups(f.entries, f.ref, f.norm).values() for i in v]))
                if n_of(f) >= 2 else None),
            "dedup_guess_on_no_match": on(lambda f: "proceed" if n_of(f) == 0 else None),
            "dedup_stop_on_duplicates": on(lambda f: "stop" if carrying(f) > n_of(f) else None),
            "dedup_always_confirm": on(lambda f: "ask"),
            "dedup_ask_on_no_match": on(lambda f: "ask" if n_of(f) == 0 else None),
            "dedup_stop_on_ambiguity": on(lambda f: "stop" if n_of(f) >= 2 else None),
            "dedup_full_name_match": on(lambda f: _decide(sum(f"{e.name} {e.detail}" == f.ref for e in f.entries),
                                                          f.cls, f.b) if f.rt.details == "last" else None),
            "dedup_first_listed": on(None, lambda f: ident_at(f, 0)),
            "dedup_last_listed": on(None, lambda f: ident_at(f, len(f.entries) - 1)),
            "dedup_most_recent_entry": on(None, lambda f: ident_at(f, latest(f, range(len(f.entries))))),
            "dedup_oldest_entry": on(None, lambda f: ident_at(f, min(range(len(f.entries)),
                                                                     key=lambda i: f.entries[i].seen))),
        }
        return {k: error_model(k, fn) for k, fn in fns.items()}
