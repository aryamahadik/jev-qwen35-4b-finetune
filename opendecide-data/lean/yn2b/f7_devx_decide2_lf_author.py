"""Author the decide2 parse table for devx round 2 (ids r_f7x2_*), from yn2b/f7_devx_blind_packet.jsonl ONLY.

Written by the round-3 arbiter before any devx gold, sidecar or devx builder file was opened. Every LF below is the
author's own reading of the rendered English (instructions + card + options); every fact is quoted from the state.
Label / item atoms are evaluated by decide2 against the HUMAN label of each base text (meta.orig).

Arbiter round 4 (2 Oct 2026): devx round 3 rewrote 4 rows under new ids (r_f7x3_14a_3, 14b_3, 17a_1, 17b_1). Their
LFs (block 'devx round 3' below) were written by the round-4 arbiter from the blind packet text ONLY, before decide2
or the precheck was run on them and before any devx gold, sidecar, relation file, builder or audit file was opened.
The table now also binds every LF to the exact text it was written from ('text_sha256', see devx_text_sha): decide2
refuses a devx row whose state / instructions / card / options differ from that text, so a stale LF can never be
applied to a changed row, whether or not devx renames it.
"""
import hashlib
import json
import sys
from pathlib import Path

LEAN = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
OUT = LEAN / "yn2b" / "f7_devx_decide2_lf.json"


def L(n):
    return ["L", n]


def F(n):
    return ["F", n]


def I(k, n=None):
    return ["I", k] if n is None else ["I", k, n]


def NOT(x, k=1):
    for _ in range(k):
        x = ["NOT", x]
    return x


def AND(*a):
    return ["AND", *a]


def OR(*a):
    return ["OR", *a]


def AMBIG(note, a, b):
    """Two readings of one construction; decide2 refuses the row when they give different values (arbiter A3 / A4).
    Added after the round-3 arbiter saw devx golds: it is applied to EVERY devx exceptive and every 'opposite /
    reverse / contrary' of a universal batch claim, whatever the outcome (rule-driven, not result-driven)."""
    return ["AMBIG", note, a, b]


EXC_NOTE = ("exceptive inclusion condition: literal set-minus reading vs the reading in which the excepted item "
            "has the property (A3)")
OPP_NOTE = "'opposite' of a universal claim: plain denial vs contrary ('the opposite of none is all') (A4)"


def CH(sel, *opts):
    return ["CHOICE", "true" if sel else "false", list(opts)]


SAFER_LEVELS = {
    "mild": ["no incident, no injury", "incident, but no injury", "injury, no first aid or medical care",
             "injury, first aid by a non-medical person"],
    "moderate": ["injury, seen by a medical professional", "injury, emergency department treatment"],
    "severe": ["injury, hospital admission", "death"],
}
HURT = ["injury, no first aid or medical care", "injury, first aid by a non-medical person",
        "injury, seen by a medical professional", "injury, emergency department treatment",
        "injury, hospital admission", "death"]
# 'medical care' and 'home-handled' leave 'death' out on purpose: the card does not say whether a death had care.
# If a base text is labelled 'death' the atom raises (KeyError-free: the value is simply not in either list, so both
# read false); the arbiter checks post hoc that no L10 base text is 'death'.
SAFER_L10 = {
    "hurt": HURT,
    "medical care": ["injury, first aid by a non-medical person", "injury, seen by a medical professional",
                     "injury, emergency department treatment", "injury, hospital admission"],
    "home-handled": ["no incident, no injury", "incident, but no injury", "injury, no first aid or medical care",
                     "injury, first aid by a non-medical person"],
}
WIKI = {
    "Computing desk": "Computing reference desk", "Mathematics desk": "Mathematics reference desk",
    "Language desk": "Language reference desk", "Science desk": "Science reference desk",
    "Entertainment desk": "Entertainment reference desk", "Humanities desk": "Humanities reference desk",
    "COI board": "Conflict of interest noticeboard", "Sources board": "Reliable sources noticeboard",
    "Technical board": "Village pump (technical)", "Fringe board": "Fringe theories noticeboard",
}


def tox(pos, neg):
    return {"type": "tox", "pos": pos, "neg": neg}


ladders, rows = {}, {}


def pair(n, atoms, yn, choice_a, choice_b, facts_a=None, facts_b=None, atoms_b=None):
    """yn: the 4 yes/no LFs (rows _0.._3), shared by both twins; choice_x: the row-4 LF of each twin."""
    for tw, ch, fa, at in (("a", choice_a, facts_a, atoms), ("b", choice_b, facts_b, atoms_b or atoms)):
        lid = "f7x2_L%02d%s" % (n, tw)
        ladders[lid] = {"atoms": at, "facts": fa or {}}
        for k, lf in enumerate(yn):
            rows["r_f7x2_%02d%s_%d" % (n, tw, k)] = lf
        rows["r_f7x2_%02d%s_4" % (n, tw)] = ch


# ---------------------------------------------------------------------------------------------- single comments
# L01 toxic / non-toxic
pair(1, tox(["toxic"], ["non-toxic"]),
     [L("toxic"),                         # Does the label 'toxic' fit?
      L("non-toxic"),                     # Does the label 'non-toxic' fit?
      NOT(L("non-toxic")),                # does it fail to fit 'non-toxic'?
      NOT(L("non-toxic"), 2)],            # answer no if the reverse of 'non-toxic fits' holds
     CH(False, L("toxic"), F("personal"), L("non-toxic")),            # which label is inapplicable
     CH(False, L("non-toxic"), F("question"), NOT(L("non-toxic"))),   # which label does it fail to match ('flagged')
     facts_a={"personal": [True, "'And you are an ignorant, ignorant person.' addresses the reader as 'you'"]},
     facts_b={"question": [True, "'What are they, pray tell?'"]})

# L02 abusive / civil
pair(2, tox(["abusive"], ["civil"]),
     [L("abusive"),
      AND(L("civil"), NOT(L("abusive"))),          # 'civil' the only one of the two labels that fits
      NOT(L("civil")),                              # wording contradicts the moderator's tag 'civil'
      NOT(NOT(L("civil"), 1))],                     # false that it fails to fit 'civil'
     CH(False, L("abusive"), F("insulting"), L("civil")),       # which label is unsuitable
     CH(True, L("abusive"), F("advertising"), L("civil")),      # which label fits best
     facts_a={"insulting": [True, "'Wrong again genius. ... your smelly bait, troll.' calls the reader 'troll'"]},
     facts_b={"advertising": [False, "'I read that, too. Doesn't change the fact ...' promotes nothing"]})

# L03 hostile / harmless (row 0 has no card: 'demeans, insults or threatens someone' = the hostile line)
T03 = tox(["hostile", "demeans, insults or threatens"],
          ["harmless", "free of insults and threats", "free of insults", "does not insult or threaten anyone"])
pair(3, T03,
     [L("demeans, insults or threatens"),
      NOT(L("hostile")),                            # comment refutes the summary 'the comment is hostile'
      NOT(L("harmless")),                           # refutes a summary saying it is harmless
      NOT(NOT(L("free of insults and threats")))],  # false that it is not free of insults and threats
     CH(True, NOT(L("free of insults")), F("praises_dunham"), F("sunset"), F("asks_question")),
     CH(True, L("does not insult or threaten anyone"), F("stayed_home_thursday"), F("red_marker"),
        F("nobody_saw_bus")),
     facts_a={"praises_dunham": [False, "'resembles that dummy Walter on Jeff Dunham's shows' praises no one"],
              "sunset": [False, "no sunset in the comment"],
              "asks_question": [False, "two statements, no question mark"]},
     facts_b={"stayed_home_thursday": [False, "'I was there on Thursday'"],
              "red_marker": [False, "'a black permanent marker'"],
              "nobody_saw_bus": [False, "'he definitely made it to the bus'; nothing says nobody saw the bus"]})

# L04 insulting / insult-free
pair(4, tox(["insulting"], ["insult-free"]),
     [L("insulting"),
      NOT(L("insulting")),                          # does the comment not insult, mock, swear at or threaten anyone
      NOT(L("insult-free")),                        # key: yes = the claim 'insult-free' fails
      NOT(NOT(L("insult-free")))],                  # reverse of 'insult-free' unsupported
     CH(True, F("trump_unpopular_anywhere"), NOT(L("insult-free")), F("names_alaska_governor"),
        F("praises_george_w")),
     CH(False, NOT(L("insult-free")), L("insult-free"), F("about_doctors")),   # needs review / insult-free / about doctors
     facts_a={"trump_unpopular_anywhere": [False, "'Trump ain't all that popular here' (here, not anywhere)"],
              "names_alaska_governor": [False, "George W is named as winning Alaska, not as its governor"],
              "praises_george_w": [False, "'the idiot, George W'"]},
     facts_b={"about_doctors": [True, "'I don't see doctors like that. My doctor asks ...'"]})

# L05 offensive / inoffensive
pair(5, tox(["offensive"], ["inoffensive"]),
     [L("offensive"),
      L("inoffensive"),
      L("inoffensive"),                             # side sentence 'Ignore informal spelling.'
      NOT(NOT(L("inoffensive")))],                  # answer no if it refutes the tag 'inoffensive'
     CH(True, L("inoffensive"), NOT(L("inoffensive")), F("praise")),       # inoffensive / escalated / praise
     CH(False, L("inoffensive"), NOT(L("inoffensive")), F("friendly")),    # inoffensive / escalated / friendly
     facts_a={"praise": [False, "'Are you ever going to give it up? Moronic!'"]},
     facts_b={"friendly": [True, "'They are coming out of the woodwork my friend.'"]})

# L06 attack / no attack
pair(6, tox(["attack"], ["no attack"]),
     [L("attack"),
      NOT(L("attack")),                             # answer no if 'attack' fits
      NOT(L("no attack")),                          # claim that it fits 'no attack' is unfounded
      NOT(NOT(L("no attack")))],                    # untrue that it fails to match 'no attack'
     CH(False, L("no attack"), L("attack"), F("ends_exclamation")),
     CH(False, L("no attack"), F("hope"), NOT(L("no attack"))),            # no attack / hope / held
     facts_a={"ends_exclamation": [True, "ends with 'Don't deny it!'"]},
     facts_b={"hope": [True, "'Let's hope this one proves not to be true!'"]})

# L07 rude / respectful
pair(7, tox(["rude"], ["respectful", "free of insults"]),
     [L("rude"),
      L("respectful"),
      NOT(NOT(L("rude"))),                          # wording refutes 'the comment is not rude'
      NOT(NOT(NOT(L("rude"))))],                    # untrue that it contradicts the note 'isn't rude'
     CH(True, F("thanks_flowers"), F("lacks_praise_for_addressee"), F("asks_question"), F("names_judge")),
     CH(False, F("predicts_eu_end"), F("time_frame"), F("mentions_eu"), NOT(L("free of insults"))),
     facts_a={"thanks_flowers": [False, "no thanks in the comment"],
              "lacks_praise_for_addressee": [True, "Ms. Flowers is called 'stupid'; no praise"],
              "asks_question": [False, "one statement, no question mark"],
              "names_judge": [False, "no judge named"]},
     facts_b={"predicts_eu_end": [True, "'This is the end of the european union'"],
              "time_frame": [True, "'it will be gone in a year or 2'"],
              "mentions_eu": [True, "'the european union'"]})

# ---------------------------------------------------------------------------------------------- SaferProducts
S08 = {"type": "safer", "map": SAFER_LEVELS}
pair(8, S08,
     [L("severe"),
      OR(L("mild"), L("moderate")),
      NOT(NOT(L("severe"))),                        # report contradicts the note 'level isn't severe'
      NOT(NOT(NOT(L("severe"))))],                  # unfounded to say the report cannot rule out 'severe'
     CH(True, NOT(L("severe")), L("mild"), NOT(NOT(L("severe")))),          # non-severe / mild / top
     CH(True, NOT(L("severe")), L("mild"), L("severe")))
pair(9, S08,
     [L("mild"),
      NOT(L("mild")),                               # say no if 'mild' fits
      NOT(NOT(L("mild"))),                          # grounds to reject the note 'level isn't mild'
      NOT(NOT(NOT(L("mild"))))],                    # false that the report doesn't rule out 'mild'
     CH(True, NOT(NOT(L("mild"))), NOT(L("mild")), L("severe")),            # low / non-mild / severe
     CH(False, NOT(L("moderate")), F("knife_folded"), F("three_stitches"), F("urgent_care")),
     facts_b={"knife_folded": [True, "'ended up folding onto my index finger'"],
              "three_stitches": [True, "'requiring 3 stitches'"],
              "urgent_care": [True, "'at a local Urgent Care Clinic'"]})
S10 = {"type": "safer", "map": SAFER_L10}
pair(10, S10,
     [L("hurt"),
      NOT(L("medical care")),                       # report describes no medical care for anyone
      NOT(L("home-handled")),                       # false that 'home-handled' fits
      NOT(NOT(NOT(L("hurt"))))],                    # unjustified: report does not show that not a single person was hurt
     CH(False, NOT(NOT(L("hurt"))), NOT(L("hurt")), F("appliance")),        # injury report / unhurt / appliance
     CH(True, F("stroller_blue"), F("thumb_crushed"), NOT(NOT(L("hurt"))), F("admitted")),
     facts_a={"appliance": [True, "'Bosch dishwasher'"]},
     facts_b={"stroller_blue": [False, "'Red single britax b- agile stroller'"],
              "thumb_crushed": [False, "'my right hand fifth digit was crushed' (the little finger)"],
              "admitted": [False, "'I went to urgent care'; no admission"]})

# ---------------------------------------------------------------------------------------------- wiki routing
W = {"type": "wiki", "map": WIKI}
pair(11, W,
     [L("Computing desk"),
      OR(L("Mathematics desk"), L("Language desk"), L("Science desk")),
      NOT(NOT(L("Computing desk"))),                # grounds to reject 'the Computing desk fails to suit it'
      NOT(NOT(NOT(L("Computing desk"))))],          # opposite of 'Computing isn't the only desk' unsupported
     CH(True, F("asks_printer"), L("Language desk"), NOT(L("Science desk")), F("heading_wikipedia")),
     CH(True, L("Computing desk"), NOT(L("Computing desk")), L("Mathematics desk")),   # Computing / elsewhere / Maths
     facts_a={"asks_printer": [False, "asks about the language used with punched cards"],
              "heading_wikipedia": [False, "'Heading: What programming language did Punched cards use?'"]})
pair(12, W,
     [L("Language desk"),
      NOT(L("Language desk")),                      # asks about something other than words, grammar, meanings, usage
      NOT(NOT(L("Language desk"))),                 # fails to fit 'off-topic for Language'
      NOT(NOT(NOT(L("Language desk"))))],           # fails to refute 'unsuited to the Language desk'
     CH(False, NOT(L("Language desk")), L("Language desk"), F("asks_question")),
     CH(False, NOT(NOT(L("Language desk"))), F("asks_finale"), F("names_crane"), F("names_passions")),
     facts_a={"asks_question": [True, "'What would you call someone who studies carnivals?'"]},
     facts_b={"asks_finale": [True, "'in the series finale of Passions?'"],
              "names_crane": [True, "'Alistair Crane'"],
              "names_passions": [True, "'Passions'"]})
pair(13, W,
     [L("Sources board"),
      NOT(F("asks_cite_website")),                  # false that it asks whether a website can be cited (no card)
      NOT(NOT(L("Sources board"))),                 # fails to fit 'elsewhere' (= a listed board other than Sources)
      NOT(NOT(NOT(L("Sources board"))))],           # grounds to dismiss the denial of 'unsuited to Sources'
     CH(False, F("asks_sikhiwiki"), AND(NOT(L("Sources board")), L("COI board")), F("mentions_historian"),
        F("point_editor")),
     CH(True, F("asks_cite_website"), F("broken_template"), F("names_fringe"),
        AND(NOT(L("Sources board")), L("COI board"))),
     facts_a={"asks_cite_website": [True, "'Is sikhiwiki.org a reliable source for anything?'"],
              "asks_sikhiwiki": [True, "'Is sikhiwiki.org a reliable source for anything?'"],
              "mentions_historian": [True, "'Karam Singh (historian)'"],
              "point_editor": [True, "'I'd like to be able to point the editor towards a discussion'"]},
     facts_b={"asks_cite_website": [False, "'... was written by GAWRDpr, Obvious COI problem.' asks about no source"],
              "broken_template": [False, "no template mentioned"],
              "names_fringe": [False, "no fringe theory named"]})

# ---------------------------------------------------------------------------------------------- batches
C4 = [I(k) for k in range(1, 5)]
pair(14, {"type": "tox_batch"},
     [["ANY", *C4],
      NOT(["ANY", *C4]),                            # key: yes = the claim 'at least one is toxic' fails
      NOT(["NONE", *C4]),                           # false that the batch is only non-toxic comments
      AMBIG(OPP_NOTE, NOT(NOT(["NONE", *C4])), NOT(["ALL", *C4]))],   # grounds to dismiss the opposite of 'not a single one is toxic'
     CH(True, AMBIG(EXC_NOTE, AND(NOT(I(1)), NOT(I(2)), NOT(I(4))), AND(I(3), NOT(I(1)), NOT(I(2)), NOT(I(4)))),
        ["ALL", *C4], ["NONE", *C4], I(1)),
     CH(False, F("c2_alaskans"), NOT(["ALL", *[NOT(i) for i in C4]]), F("c3_uber"), F("c4_fuel_cells")),
     facts_b={"c2_alaskans": [True, "Comment 2: 'I hope  Alaskans will enjoy'"],
              "c3_uber": [True, "Comment 3: 'allow über'"],
              "c4_fuel_cells": [True, "Comment 4: 'Hydrogen fuel cells'"]})
C5 = [I(k) for k in range(1, 6)]
pair(15, {"type": "tox_batch"},
     [["ATLEAST", 3, *C5],
      NOT(["ATMOST", 2, *C5]),                      # false that no more than two are toxic
      NOT(["ATMOST", 2, *C5]),                      # answer no if no more than two are toxic
      NOT(NOT(["ATMOST", 2, *C5]))],                # reverse of 'not fewer than three' borne out
     CH(True, ["EXACTLY", 2, *C5], ["ATMOST", 1, *C5], NOT(["ALL", *[NOT(i) for i in C5]]), ["ALL", *C5]),
     CH(True, I(2), ["ATLEAST", 3, *C5], ["ATMOST", 1, *C5], NOT(["ATMOST", 1, *C5])))
R2 = [I(1, "hurt"), I(2, "hurt")]
pair(16, {"type": "safer_batch", "map": {"hurt": HURT}},
     [AND(*R2),
      NOT(AND(*R2)),
      NOT(NOT(AND(*R2))),
      NOT(NOT(NOT(AND(*R2))))],                     # unjustified: reports do not show that not both ...
     CH(False, F("r1_golf_cart_stop"), ["NONE", *R2], F("r2_rash_neck"), F("r2_sports")),
     CH(True, NOT(["NONE", *R2]), F("r1_toy_upright"), F("r2_doctor_hand"), F("r1_names_store")),
     facts_a={"r1_golf_cart_stop": [True, "Report 1: 'bringing the golf cart to an abrupt stop'"],
              "r2_rash_neck": [True, "Report 2: 'a red, painful, papular rash on my neck'"],
              "r2_sports": [True, "Report 2: 'during sports'"]},
     facts_b={"r1_toy_upright": [False, "Report 1: 'This item tips over backwards'"],
              "r2_doctor_hand": [False, "Report 2 mentions pain to the hand; no doctor"],
              "r1_names_store": [False, "Report 1 says 'Check Amazon reviews'; it does not say where the rocker "
                                        "was bought"]})
P3L = [I(k, "Language desk") for k in (1, 2, 3)]
pair(17, {"type": "wiki_batch", "map": WIKI},
     [["ANY", *P3L],
      AMBIG(EXC_NOTE, AND(NOT(I(1, "Language desk")), NOT(I(2, "Language desk"))),
            AND(I(3, "Language desk"), NOT(I(1, "Language desk")), NOT(I(2, "Language desk")))),
      NOT(["NONE", *P3L]),                          # answer no if no post belongs at the Language desk
      NOT(NOT(["NONE", *P3L]))],                    # unfounded to dispute the note 'no post here is Language'
     CH(True, ["ALL", *[I(k, "Mathematics desk") for k in (1, 2, 3)]], I(1, "Humanities desk"),
        NOT(I(2, "Language desk")),
        AMBIG(EXC_NOTE, AND(NOT(I(1, "Mathematics desk")), NOT(I(2, "Mathematics desk"))),
              AND(I(3, "Mathematics desk"), NOT(I(1, "Mathematics desk")), NOT(I(2, "Mathematics desk"))))),
     CH(False, F("p1_colorblind"), F("p2_hebrew"), ["NONE", *[I(k, "Science desk") for k in (1, 2, 3)]],
        F("p3_formula")),
     facts_b={"p1_colorblind": [True, "Post 1: 'How do scientists \"know\" that?' (animals color-blind)"],
              "p2_hebrew": [True, "Post 2: 'When was the Hebrew calendar created?'"],
              "p3_formula": [True, "Post 3: 'What formula could I use?'"]})

# ---------------------------------------------------------------------------------------------- invented records
REC = {"type": "record"}
pair(18, REC,
     [F("asks_refund"),
      NOT(F("asks_refund")),                        # grounds to dispute 'Customer asks for a refund'
      NOT(NOT(F("asks_refund"))),                   # answer no if the customer doesn't ask for a refund
      NOT(NOT(NOT(F("asks_refund"))))],             # false that the thread is not free of a refund request
     CH(True, F("other_request"), NOT(F("other_request")), F("praise")),       # other request / billing / praise
     CH(False, F("other_request"), NOT(F("other_request")), F("complaint")),   # other request / billing / complaint
     facts_a={"asks_refund": [True, "'Please send my money back to the card I paid with.'"],
              "other_request": [False, "the only request is the money back"],
              "praise": [False, "no thanks for a good order; the lid arrived cracked"]},
     facts_b={"asks_refund": [False, "'Please send me a new kettle in its place.'"],
              "other_request": [True, "'Please send me a new kettle in its place.'"],
              "complaint": [True, "'arrived on Tuesday with a cracked lid'"]})
pair(19, REC,
     [F("asks_refund"),
      NOT(NOT(F("asks_refund"))),                   # rule 1: must not refund unless asked -> allowed iff asked
      NOT(NOT(F("asks_refund"))),                   # refutes 'need not be escalated' (rule 2: escalate iff asked)
      NOT(F("note_claims_refund"))],                # the triage note makes no claim of a refund request
     CH(False, F("by_chat"), F("lamp_broken"), F("ticket_55_2190"), NOT(F("asks_refund"))),
     CH(True, F("asks_refund"), F("asks_refund"), NOT(F("asks_refund")), F("lamp_broken")),
     facts_a={"asks_refund": [True, "'I would like my money back, please.'"],
              "note_claims_refund": [True, "'Triage note: topic = refund request'"],
              "by_chat": [True, "'Channel: chat'"],
              "lamp_broken": [True, "'the lamp inside is broken'"],
              "ticket_55_2190": [True, "'Ticket: 55-2190'"]},
     facts_b={"asks_refund": [False, "'Could you pass this on to the courier?'; no refund asked"],
              "note_claims_refund": [False, "'Triage note: topic = packaging; refund wanted = no'"],
              "lamp_broken": [False, "'the lamp inside works'"]})
pair(20, REC,
     [F("receipt"),
      NOT(F("receipt")),                            # answer no if 'documented' fits
      NOT(NOT(F("receipt"))),                       # 'undocumented' fails to fit
      NOT(NOT(NOT(F("receipt"))))],                 # record fails to bear out the reverse of 'undocumented fits'
     CH(False, F("receipt"), NOT(F("receipt")), F("expense")),            # documented / undocumented / expense
     CH(False, NOT(F("receipt")), F("expense"), NOT(NOT(F("receipt")))),  # undocumented / expense / payable
     facts_a={"receipt": [True, "'\"receipt\": \"scan_0412.pdf\"'"],
              "expense": [True, "'\"claim_id\": \"EXP-30771\"' ... 'amount_eur'"]},
     facts_b={"receipt": [False, "'\"receipt\": null'"],
              "expense": [True, "'\"claim_id\": \"EXP-30771\"' ... 'amount_eur'"]})
pair(21, REC,
     [F("delivered"),
      NOT(F("delivered")),                          # status 'with the carrier' (exactly one of two statuses)
      NOT(F("delivered")),                          # denial of 'parcel was delivered' borne out
      NOT(F("delivered"), 4)],                      # untrue that the log fails to bear out the opposite of 'never delivered'
     CH(True, NOT(F("delivered")), NOT(NOT(F("signed"))), F("label_5_may"), F("asked_text")),
     CH(False, NOT(NOT(F("delivered"))), NOT(F("delivered")), F("scanned")),   # closed / undelivered / scanned
     facts_a={"delivered": [True, "'13:31  delivered; signed by R. Binley'"],
              "signed": [True, "'signed by R. Binley'"],
              "label_5_may": [False, "'2026-05-03 08:14  label printed'"],
              "asked_text": [False, "'customer had asked for a call before delivery'"]},
     facts_b={"delivered": [False, "'13:31  delivery attempt failed; parcel taken back to Hollins depot'"],
              "scanned": [True, "'parcel scanned at Hollins depot'"]})
pair(22, REC,
     [F("approved"),
      NOT(F("bot_1116_claims_unapproved")),         # false that the 11:16 message claims 'unapproved'
      NOT(NOT(F("approved"))),                      # false that the request is unapproved
      NOT(NOT(NOT(F("approved"))))],                # false that the chat doesn't show that it is unapproved
     CH(True, F("manager_out"), F("logged_6602"), NOT(NOT(F("approved"))), F("payroll")),
     CH(False, NOT(F("approved")), NOT(NOT(F("approved"))), F("logged")),       # unapproved / cleared / logged
     facts_a={"approved": [True, "'[11:15] Bemis Belov: Approved, go ahead.'"],
              "bot_1116_claims_unapproved": [False, "'[11:16] IT bot: Status changed: approved.'"],
              "manager_out": [False, "'Approved, go ahead.'"],
              "logged_6602": [False, "'Request logged as ACC-6620.'"],
              "payroll": [False, "'edit access to the Q3 budget sheet'"]},
     facts_b={"approved": [False, "'I'm out today, I'll look at it tomorrow.' / 'Status unchanged: unapproved.'"],
              "bot_1116_claims_unapproved": [True, "'[11:16] IT bot: Status unchanged: unapproved.'"],
              "logged": [True, "'Request logged as ACC-6620.'"]})

# ---------------------------------------------------------------------------------------------- devx round 3
# Arbiter round 4. devx round 3 rewrote these 4 rows (new ids r_f7x3_*); the other 216 rows are byte for byte the
# round-2 packet (checked field by field against data/v14_parts/f7_devx_r2_backup/f7_devx_blind_packet.jsonl), so
# their LFs above still apply. The stale round-2 LFs of the 4 rewritten rows are removed.
for _stale in ("r_f7x2_14a_3", "r_f7x2_14b_3", "r_f7x2_17a_1", "r_f7x2_17b_1"):
    del rows[_stale]
for _tw in "ab":
    # r_f7x3_14*_3: "Consider the opposite of the next claim. Claim: not a single comment is toxic. Does the batch
    # give grounds to dismiss that opposite?" The card defines it: "here 'the opposite' of a claim means its plain
    # negation", and "the comments settle every claim asked about here" (so 'grounds to dismiss X' = X is false).
    # Claim = NONE; its opposite = NOT NONE; yes = that opposite is false. With the definition in the card there is
    # one reading (the contrary reading of A4 is excluded by the card), so no AMBIG.
    rows["r_f7x3_14%s_3" % _tw] = NOT(NOT(["NONE", *C4]))

    # r_f7x3_17*_1: "Is it true that no post apart from Post 3 belongs at either of the Language and Mathematics
    # desks?" A negative exceptive, so AMBIG by rule (A3): reading A = literal set-minus (neither Post 1 nor Post 2
    # is a Language or Mathematics post); reading B = A plus the inclusion condition (Post 3 is a Language or
    # Mathematics post). 'belongs at either of X and Y' under 'no' = belongs at X or at Y.
    def _lm(k):
        return OR(I(k, "Language desk"), I(k, "Mathematics desk"))
    _lit = AND(NOT(_lm(1)), NOT(_lm(2)))
    rows["r_f7x3_17%s_1" % _tw] = AMBIG(EXC_NOTE, _lit, AND(_lm(3), _lit))


TEXT_KEYS = ("state", "instructions", "card", "options")


def devx_text_sha(r):
    """sha256 of the rendered text an LF was written from (same function as v3_nested_negation.devx_text_sha)."""
    return hashlib.sha256(json.dumps([r.get(k) for k in TEXT_KEYS], ensure_ascii=False,
                                     sort_keys=True).encode("utf-8")).hexdigest()


packet = [json.loads(x) for x in open(LEAN / "yn2b" / "f7_devx_blind_packet.jsonl")]
ids = {r["id"] for r in packet}
lids = {r["ladder_id"] for r in packet}
assert set(rows) == ids, (sorted(ids - set(rows))[:5], sorted(set(rows) - ids)[:5])
assert set(ladders) == lids
for r in packet:
    lf = rows[r["id"]]
    if r["qtype"] == "choice":
        assert lf[0] == "CHOICE" and len(lf[2]) == len(r["options"]), r["id"]
    else:
        assert lf[0] != "CHOICE", r["id"]

# Bind every LF to the text it was written from. The r_f7x2_* LFs were written from the round-2 packet: each of those
# rows must still be byte for byte the round-2 text (else its LF is stale and the build stops here).
R2_PACKET = LEAN / "data" / "v14_parts" / "f7_devx_r2_backup" / "f7_devx_blind_packet.jsonl"
r2 = {json.loads(x)["id"]: json.loads(x) for x in open(R2_PACKET)}
text_sha = {}
for r in packet:
    h = devx_text_sha(r)
    if r["id"].startswith("r_f7x2_"):
        assert r["id"] in r2 and devx_text_sha(r2[r["id"]]) == h, ("stale round-2 LF", r["id"])
    else:
        assert r["id"].startswith("r_f7x3_"), r["id"]
    text_sha[r["id"]] = h
assert set(text_sha) == set(rows)

doc = ("devx parse table for decide2 (ids r_f7x2_* from devx round 2, r_f7x3_* from devx round 3). The r_f7x2_* LFs "
       "were authored by the round-3 arbiter from yn2b/f7_devx_blind_packet.jsonl ONLY (id, ladder_id, orig, qtype, "
       "state, instructions, card, options); no devx gold, sidecar, relation file, builder or audit file was opened "
       "before that table was written and hashed. "
       "Per ladder: atoms (how label / item atoms are read from the human label(s) of meta.orig) and facts (bool, "
       "quote from the state). Per row: the LF of 'yes' (yes/no rows) or CHOICE(select, [option LFs]). "
       "Ops: NOT, AND, OR, ANY, NONE, ALL, ATLEAST k, ATMOST k, EXACTLY k, L (label), I (batch item), F (fact). "
       "AMBIG(note, A, B) holds two readings of one construction and is refused when they differ: every devx "
       "exceptive (r_f7x2_14a_4 option 1, r_f7x3_17*_1, r_f7x2_17a_4 option 4; arbiter A3). The round-3 AMBIG "
       "wrappers were added after the golds were seen (disclosed in yn2b/F7_OBJECTIONS.md, arbiter round 3); every "
       "other r_f7x2_* LF is unchanged from the version hashed before any gold was opened (sha256 407c27f1...). "
       "The 4 r_f7x3_* LFs were written by the round-4 arbiter from the blind packet text only, before any decide2 "
       "or precheck run on them (yn2b/F7_OBJECTIONS.md, arbiter round 4). text_sha256: per row, the sha256 of "
       "json.dumps([state, instructions, card, options], ensure_ascii=False, sort_keys=True) of the text the LF was "
       "written from; decide2 refuses a devx row whose text differs.")
OUT.write_text(json.dumps({"_doc": doc, "ladders": ladders, "rows": rows, "text_sha256": text_sha}, indent=1,
                          ensure_ascii=False) + "\n")
print("wrote", OUT, len(ladders), "ladders", len(rows), "rows", len(text_sha), "text hashes")
