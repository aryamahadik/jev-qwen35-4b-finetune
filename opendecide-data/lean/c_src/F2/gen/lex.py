"""The F2 phrase lexicon: surface phrase -> SEM id (3.3). The parser owns it (it compiles these templates into regexes
and maps each match to its SEM id and slots); the renderer only fills templates, so every rendered clause parses
through it. Templates use {slot} placeholders; SLOT_RX gives each slot's regex. Closed operator lexicons (CMP, OP,
TF, N1) are G0 semantics (XF17).
"""
from __future__ import annotations

import re

# ----------------------------------------------------------------------------------------------------------------- slots

LBL = r"[A-Za-z][A-Za-z0-9'\-]*(?: [A-Za-z0-9'\-]+)*?"
NUM = r"\d+(?:\.\d+)?"
SLOT_RX = {
    "lbl": LBL, "num": NUM, "int": r"\d+", "money": NUM + r" [A-Za-z]+", "pct": NUM + r"%",
    "cur": r"[A-Za-z]+", "id": r"[A-Z]{2,4}-\d{3,6}", "date": r"[A-Za-z0-9 ,\-()]+?",
    "word": r"[a-z]+", "text": r"[^\n]+?", "cmp": r"[a-z ]+?", "unit": r"[A-Za-z][A-Za-z\- ]*?",
}


def slot_type(name: str) -> str:
    base = re.sub(r"\d+$", "", name)
    return {"res": "lbl", "base": "lbl", "q": "lbl", "r": "lbl", "lc": "lbl", "tot": "lbl", "pct": "lbl", "fee": "lbl",
            "cap": "lbl", "min": "lbl", "fixed": "lbl", "gross": "lbl", "ded": "lbl", "f": "lbl", "erate": "lbl",
            "grate": "lbl", "echarge": "lbl", "gcharge": "lbl", "step": "lbl", "item": "lbl", "kind": "lbl",
            "listed": "lbl", "amt": "lbl", "ent": "lbl", "tbl": "lbl", "evt": "lbl", "act": "lbl", "per": "lbl",
            "n": "int", "k": "num", "x": "num", "u": "text", "units": "unit", "unit": "unit", "v": "text",
            "c": "text", "c1": "text", "c2": "text", "T": "text", "id": "id", "cmpph": "cmp", "nei": "text",
            "steps": "text", "lines": "text", "range": "text", "name": "text", "hl": "word", "whole": "text",
            "N": "int", "K": "int", "M": "int", "days": "text", "list": "text"}.get(base, "text")


_RX_CACHE = {}


def compile_tpl(tpl: str, anchored=False):
    key = (tpl, anchored)
    if key in _RX_CACHE:
        return _RX_CACHE[key]
    parts = re.split(r"(\{[A-Za-z0-9_]+\})", tpl)
    out, seen = [], set()
    for p in parts:
        m = re.fullmatch(r"\{([A-Za-z0-9_]+)\}", p)
        if m:
            nm = m.group(1)
            if nm in seen:
                out.append(f"(?P={nm})")
            else:
                seen.add(nm)
                out.append(f"(?P<{nm}>{SLOT_RX[slot_type(nm)]})")
        else:
            out.append(re.escape(p))
    rx = "".join(out)
    if anchored:
        rx = "^" + rx + "$"
    c = re.compile(rx)
    _RX_CACHE[key] = c
    return c


def fill(tpl: str, **kw) -> str:
    out = tpl
    for k, v in kw.items():
        out = out.replace("{" + k + "}", str(v))
    if re.search(r"\{[A-Za-z0-9_]+\}", out):
        raise KeyError(f"unfilled slot in {out!r}")
    return out


# ----------------------------------------------------------------------------------------------------------------- world

W0 = ("These are all the rules. No other fee, discount, cap or exception applies, and a charge is due only when a "
      "listed rule makes it due.")
W1 = ("The record lists every charge, payment and event that happened: a charge it does not list was not made, and a "
      "condition it does not mention did not happen.")
W2 = ("Every charge, payment and event that happened is listed, and every other fact the rules use is given or shown "
      "as \"not recorded\". A field shown as \"not recorded\" is unknown: an unknown amount can be any amount of 0 or "
      "more, to the {u}; an unknown count any whole number of 0 or more; an unknown date any calendar date, except "
      "where a sentence of the record bounds that date; an unknown category any listed category; an unknown yes/no "
      "fact either. If the answer depends on an unknown field, choose \"{nei}\".")
CATLIST = "The {f} is one of: {list}."
NEI_TEXTS = ["Cannot be determined", "Not enough information", "Cannot tell from the record"]
NONE_TEXT = "None of the listed {kind}"

# ----------------------------------------------------------------------------------------------------------------- money core

F_MUL = "The {lc} is the {q} times the {r}."
F_PERK = "The {lc} is the {r} for each {k} {units} of {q}."
F_SUM = "The {tot} is the sum of {lines}."
F_DISC = "The {res} is the {base} after the {pct}."
R8 = "A discount of p% on an amount means paying (100 - p)% of that amount."
F_FEE = "The {fee} is the {pct} of the {base}."
F_FEE_X6 = "The {fee} is the {pct} of the {base} {hl} the {step}."      # X6: hl = after | before
F_FEE_TOT = "The {tot} is the {base} plus the {fee}."
F_PCTOF = "The {res} is the {pct} of the {base}."
F_CAP = "The {res} is the {base}, capped at the {cap}."
F_MIN = "The {res} is the {base}, with a minimum of the {min}."
X4_CAP = "The cap of the {cap} is per {per}."
X4_MIN = "The minimum of the {min} is per {per}."
X4_ORDER = "The minimum is applied after the cap."
F_ADD = "The {tot} adds the {fixed} to the {base}."
U5 = "Deduction lines are listed as positive amounts and are subtracted."
F_DED = "The {res} is the {gross} minus {lines}."
X8 = "The final {res} owed cannot go below 0."
X5 = {"succ": "Discounts are applied one after the other, each to the amount left after the previous one.",
      "added": "Discount percentages are added together and applied once."}
F_DISC2 = "The {res} is the {base} after the {pct1} and the {pct2}."
X7 = {"include": ("Listed prices include the {fee}. The price before the {fee} is the {listed} x 100 / (100 + the "
                  "{pct}), and the {fee} is the {listed} minus the price before the {fee}."),
      "before": "Listed prices are before the {fee}; the {fee} is the {pct} of the {listed} and is added to it."}
X1 = "Apply the steps in this order: {steps}."
F_DISC_X1 = "The {pct} is a discount on the running amount."
F_ADD_X1 = "The {fixed} is added to the running amount."
F_RESULT_X1 = "The {res} is the {base} after these steps."
X1_SEP = ", then "
R1 = {"half_up": "Round the {res} to the nearest multiple of {u}; an exact half rounds up.",
      "half_even": "Round the {res} to the nearest multiple of {u}; an exact half rounds to the even multiple of {u}.",
      "floor": ("Always round the {res} down to a multiple of {u}; a value that is already a multiple of {u} does "
                "not change."),
      "ceiling": ("Always round the {res} up to a multiple of {u}; a value that is already a multiple of {u} does "
                  "not change.")}
R2 = {"final": "Round only the final {res}.", "line": "Round each line as the rounding rule says, then add the lines."}
R3 = {"rounded": "Every comparison made after the {res} is rounded uses the rounded {res}.",
      "unrounded": ("Every comparison uses the {res} computed with no rounding step at all; rounding changes only "
                    "the reported {res}.")}
R4 = "Do not round any step except where a rule says so."
R5 = {"ceil": "For each line, each started {unit} is charged as a full {unit}.",
      "floor": "For each line, only complete {units} are charged.",
      "exact": "For each line, the number of {units} is charged exactly as stated; no part of a {unit} is rounded."}
U3 = {"pro_rata": "For each line, a part of {k} {units} is charged pro rata.",
      "full_k": "For each line, a part of {k} {units} is charged as a full {k} {units}."}
OP_MONEY = ("A {item} is owed when its amount worked out under these rules, after every rounding, cap, minimum, "
            "discount and waiver, is more than 0.")

# exceptions (UN1, O1, O2, O3; OR1, OR2; X2; X3)
G_O2 = "Exception {n} applies if {c}."
G_UN1 = "Exception {n} applies unless {c}. If {c}, exception {n} does not apply and nothing applies instead."
G_O1 = "Exception {n} applies only if {c1} and {c2}. When all of these conditions hold, exception {n} applies."
G_O3 = ("Exception {n} applies only if {c1} or {c2} (either or both). When at least one of these holds, "
        "exception {n} applies.")
J_AND = "{c1} and {c2}"
J_OR1 = "{c1} or {c2} (either or both)"
J_OR2 = "either {c1} or {c2}, but not both"
C_IS = "the {f} is {v}"
C_NUM = "the {f} is {cmpph} {x}"
C_NUM_POST = "the {f} is {x} {cmpph}"       # "<X> or more" / "<X> or less"
X2 = {"rate": {"replace": "When exception {n} applies, the {erate} replaces the {grate}.",
               "add": "When exception {n} applies, the {erate} is added to the {grate}."},
      "add": {"add": "When exception {n} applies, the {echarge} is added to the {gcharge}.",
              "replace": "When exception {n} applies, the {echarge} replaces the {gcharge}."}}
X3 = {"alone_lower": ("If more than one exception applies, compute the final {res} with each one alone and use the one "
                      "that gives the lower final {res}; if two give the same final {res}, use the one with the lower "
                      "exception number."),
      "alone_higher": ("If more than one exception applies, compute the final {res} with each one alone and use the one "
                       "that gives the higher final {res}; if two give the same final {res}, use the one with the "
                       "lower exception number."),
      "fold_rate": ("If more than one exception applies, apply all of them in exception-number order; each one acts on the "
                    "rate left by the ones before it, so a later replacing rule replaces the rate an earlier one set."),
      "fold_charge": ("If more than one exception applies, apply all of them in exception-number order; each one acts on "
                      "the charge left by the ones before it.")}

# card-rule comparators (CMP1-CMP3; card rules may also use "a minimum of" / "up to" / "a maximum of", F2 never does)
CMP_CARD = {"ge": ["at least", "no less than"], "gt": ["more than", "over"], "le": ["at most", "no more than"],
            "lt": ["less than", "under"]}
CMP_CARD_POST = {"ge": "or more", "le": "or less"}

# B1 outcome tables written in the card (named outcomes), meanings per band
B1_SENT = {"upper": ("Each band covers the amounts over its lower edge up to and including its upper edge; the lowest "
                     "band covers every amount up to and including its upper edge, and the highest band every amount "
                     "over its lower edge. A blank edge cell means the band has no edge on that side."),
           "lower": ("Each band covers the amounts from its lower edge up to but not including its upper edge; the "
                     "lowest band covers every amount under its upper edge, and the highest band every amount of its "
                     "lower edge or more. A blank edge cell means the band has no edge on that side.")}
OUT_INTRO = "The {res} sets the {kind} as follows."
OUT_RANGE = {"upper": {"low": "up to and including {hi}", "mid": "over {lo} up to and including {hi}", "high": "over {lo}"},
             "lower": {"low": "under {hi}", "mid": "from {lo} up to but not including {hi}", "high": "{lo} or more"}}
OUT_ITEM = "{name}: {range}"

# ----------------------------------------------------------------------------------------------------------------- questions
# Question-side comparators (Q1): CMP1-CMP3 only, never "up to", "a maximum of", "a minimum of"; never split.
Q_CMP = {
    "ge": [("at least", "pre", False), ("no less than", "pre", True), ("{T} or more", "post", False)],
    "gt": [("more than", "pre", False), ("over", "pre", False), ("above", "pre", False)],
    "le": [("at most", "pre", False), ("no more than", "pre", True), ("{T} or less", "post", False)],
    "lt": [("less than", "pre", False), ("under", "pre", False), ("below", "pre", False)],
}
Q_CMP_VERB = {  # TF-complement verb forms (never fronted with do-support)
    "ge": [("reaches", False)], "gt": [("exceeds", False)], "le": [("does not exceed", True)],
    "lt": [("falls short of", False), ("fails to reach", True)],
}
NEGATABLE = {"at least", "over", "above", "at most", "under", "below", "{T} or more", "{T} or less"}
TF_FRAMES = ["Is it true that {P}?", "Is it the case that {P}?", "Is the following true: {P}?"]
OPN = "it is not the case that "     # the operator cue at the start of P (one N1 cue)

Q_DIRECT = ["Is the {res} for {id} {cmpT}?", "For {id}, is the {res} {cmpT}?"]
P_THR = "the {res} for {id} is {cmpT}"
P_THR_NEG = "the {res} for {id} is not {cmpT}"
P_THR_VERB = "the {res} for {id} {verbT}"
Q_VALUE = ["What is the {res} for {id}?", "How much is the {res} for {id}?", "Which amount is the {res} for {id}?"]
Q_OUTCOME = ["Which {kind} applies to {id}?", "What {kind} does {id} get?"]
Q_OWED_DIRECT = ["Is a {item} owed on {id}?"]
P_OWED = "a {item} is owed on {id}"
P_OWED_NEG = ["no {item} is owed on {id}", "a {item} is not owed on {id}"]
Q_CASES = ["Which case has a {res} that is {cmpT}?", "For which case is the {res} {cmpT}?"]

NOTE_YN = ["Answer yes or no.", "Reply with Yes or No.", "Give a yes or no answer."]
NOTE_CH = ["Pick one option.", "Choose the matching option.", "Answer with one option."]

# ----------------------------------------------------------------------------------------------------------------- bands (S3)
BT_INTRO = "The band table in the record gives each band's name, lower edge, upper edge and rate."
B2 = {"marginal": ("Each rate applies only to the part of the {amt} inside its band: the part above the band's lower "
                   "edge, up to its upper edge (for the lowest band, from 0 up to its upper edge)."),
      "flat": "The rate of the band that the whole {amt} falls in applies to the whole {amt}."}
RATE_KIND = {"pct": "Each band's rate is a percentage of the {amt} it applies to.",
             "unit": "Each band's rate is an amount per {unit} of the {amt} it applies to.",
             "flat": "Each band's rate is a flat fee, and that fee is the {charge}."}
BAND_CHARGE = "The {charge} is worked out from the band table for the {amt}."
X10 = ("When the {f} is {v}, the {item} pays the rate of the band with the next lower edges than the band its {amt} "
       "falls in; in the lowest band nothing changes. Band edges do not change.")
Q_BAND = ["Which band does the {amt} for {id} fall in?", "In which band is the {amt} for {id}?"]
Q_CASES_BAND = ["Which case has a {amt} that falls in {band}?"]

# ----------------------------------------------------------------------------------------------------------------- dates (S4, S5)
D1 = "All dates are calendar dates in one time zone; the time of day does not matter."
D4A = ("The {act} must happen no later than {N} calendar days after the {evt}. The day of the {evt} is not counted, so "
       "the last allowed day is {N} calendar days after it.")
D4B = "The {act} must happen on or before the {Nth} calendar day, counting the day of the {evt} as day 1."
D15 = ("A {act} on or before the last allowed day is on time, also when it is on or before the day of the {evt}; a "
       "{act} after the last allowed day is late.")
D6A = ("A business day is a day from Monday to Friday that is not a holiday. The holidays are exactly the dates on the "
       "record's holiday line; when that line says \"none\", there are no holidays.")
D6B = ("The {act} must happen no later than {N} business days after the {evt}. Counting starts on the day after the "
       "{evt}; the {Nth} business day is the last allowed day.")
D7 = {"fwd": "If the {dl} falls on a day that is not a business day, it moves to the next business day.",
      "back": "If the {dl} falls on a day that is not a business day, it moves to the previous business day.",
      "none": "If the {dl} falls on a day that is not a business day, it does not move."}
D8 = ("{M} months after a date is the same day number {M} months later, also when that date is the last day of its "
      "month; if that month has no such day, use the last day of that month. Then apply the roll rule, if there is one.")
D8_RULE = "The {act} must happen no later than {M} months after the {evt}; that date is the last allowed day."
D12 = {"pre": ("{G} the last allowed day moves {K} {unit} later. Count the {K} {unit} from the last allowed day found "
               "before any roll; then apply the roll rule once."),
       "post": ("{G} the last allowed day moves {K} {unit} later. Count the {K} {unit} from the last allowed day after "
                "the roll; then apply the roll rule again.")}
D12_IF = "If {c},"
D12_UNLESS = "Unless {c},"
CNT_CAL = "The {cnt} is the number of calendar days from the {d1} to the {d2}."
CNT_BUS = "The {cnt} is the number of business days from the {d1} to the {d2}."
D5 = {"excl": "Count the {d2} but not the {d1}.", "both": "Count both the {d1} and the {d2}."}
D14 = {"after": "Count the business days after the {d1} up to and including the {d2}.",
       "both": "Count the business days from the {d1} to the {d2}, both included."}
D16 = ("\"K calendar days after the last allowed day\" means the date K calendar days later; the last allowed day "
       "itself is not counted.")
B1_DATE = {"upper": ("Each window covers the dates after its earlier edge up to and including its later edge; the first "
                     "window covers every date up to and including its later edge, and the last window every date "
                     "after its earlier edge."),
           "lower": ("Each window covers the dates from its earlier edge up to but not including its later edge; the "
                     "first window covers every date before its later edge, and the last window every date on or after "
                     "its earlier edge.")}
WIN_INTRO = "The {act} date sets the {kind} as follows."
WIN_RANGE = {"upper": {"low": "up to and including {b}", "mid": "after {a} up to and including {b}", "high": "after {a}"},
             "lower": {"low": "before {b}", "mid": "from {a} up to but not including {b}", "high": "on or after {a}"}}
WIN_EDGE0 = "the last allowed day"
WIN_EDGEK = "{k} calendar days after the last allowed day"
D17 = ("The settlement date is {N} calendar days after the {per}; the day of the {per} is not counted. If the "
       "settlement date falls on a day that is not a business day, the roll rule applies to it.")
STRIP_NOTE = "calendar"
HOL_NOTE = "holidays"

Q_ONTIME = ["Was the {act} for {id} on time?", "Did the {act} for {id} meet its deadline?"]
Q_LATE = ["Was the {act} for {id} late?", "Did the {act} for {id} miss its deadline?"]
P_ONTIME = ["the {act} for {id} was on time", "the {act} for {id} met its deadline"]
P_LATE = ["the {act} for {id} was late", "the {act} for {id} missed its deadline"]
P_ONTIME_NEG = ["the {act} for {id} was not on time", "the {act} for {id} failed to meet its deadline"]
P_LATE_NEG = ["the {act} for {id} was not late"]
Q_LASTDAY = ["What is the last allowed day for the {act} for {id}?", "Which date is the last allowed day for the {act} for {id}?"]
Q_COUNT = ["What is the {cnt} for {id}?", "How many days is the {cnt} for {id}?"]
Q_WINDOW = ["Which {wkind} applies to the {act} for {id}?", "What {wkind} does the {act} for {id} fall in?"]
Q_CASES_LATE = ["Which case missed its deadline?", "Which case was late?"]
Q_SETTLE = ["What is the settlement date for {id}?"]

# ----------------------------------------------------------------------------------------------------------------- statements (S5)
STMT_INTRO = "The statement lists each line with its quantity, rate and amount."
M3 = "A blank cell in the amount column means nothing was charged on that line."
M4 = ("An amount shown as \"computed\" is the line's amount worked out from its quantity and rate by the pricing rule "
      "for that line ({rules}), before any rounding, cap or minimum; rounding, caps and minimums then apply to it as to "
      "a printed amount.")
M4_RULES = {"b4": "the overtime rule for {type} lines, or else quantity x rate", "plain": "quantity x rate"}
B4 = ("For {type} lines: in each line, units up to and including the {X}th are paid at the line's rate; each unit after "
      "the {X}th is paid at {m} times that rate.")
GROSS = "The {gross} is the sum of the amounts of the {types} lines."
NET_DED = "The {net} is the {gross} minus the {pd} and minus the amounts of the {deds} lines."
NET_NODED = "The {net} is the {gross} minus the {pd}."
PCTDED = {"floor": "The {pd} is the {pct} of the {gross}, with a minimum of the {lim}.",
          "cap": "The {pd} is the {pct} of the {gross}, capped at the {lim}."}
X4_STMT = {"floor": "The minimum of the {lim} is per statement.", "cap": "The cap of the {lim} is per statement."}
COMPUTED_MARK = "computed"
R2_STMT_LINE = "Round each line and the {pd} as the rounding rule says, then combine them."
