"""F8 fact-sentence, field and table templates (step-4 wording pool for state text; G0 spec 2, 5, 8.1-8.5).

Each template has an id and slots. The renderer fills them; the G3 parser loads gen/data/facts.json (dumped from this
module) and builds its own regular expressions from the templates, so it never imports renderer code.
Slots: {ID} {case} {cases} {H} {E} {F} {cat} {v} {amtname} {money} {p} {lo} {hi} {n} {units} {event} {action}
Every template passes the record-status lint: 'recorded' appears only in the marker form '<fact> was not recorded'.
"""
from __future__ import annotations

import json

from common import DATA

SENT = {
    # bayes population data (S1 neutral / S4 narrative variants)
    "cnt": ["Of past {cases} classed '{H}', {a} show '{E}' and {b} do not.",
            "Among past {cases} classed '{H}', {a} show '{E}' and {b} do not."],
    "cnt_e": ["Of the {n} past {cases} that show '{E}', {a} are classed '{H}'."],
    "cnt_ne": ["Of the {n} past {cases} that do not show '{E}', {a} are classed '{H}'."],
    "base": ["{p} of {cases} are classed '{H}'.", "Over past years, {p} of {cases} have been classed '{H}'."],
    "lik": ["Among {cases} classed '{H}', {p} show '{E}'.", "Of the {cases} classed '{H}', {p} show '{E}'."],
    "lik_nr": ["Among {cases} classed '{H}', the share that show '{E}' was not recorded."],
    "lik_rng": ["Among {cases} classed '{H}', the share that show '{E}' is at least {lo} and at most {hi}."],
    "joint": ["{p} of all {cases} are classed '{H}' and show '{E}'."],
    "sig_yes": ["{ID} shows '{E}'.", "The {case} {ID} shows '{E}'."],
    "sig_no": ["{ID} does not show '{E}'.", "The {case} {ID} does not show '{E}'."],
    # points facts
    "f_yes": ["{ID} shows '{F}'.", "The {case} {ID} shows '{F}'."],
    "f_no": ["{ID} does not show '{F}'.", "The {case} {ID} does not show '{F}'."],
    "f_nr": ["Whether {ID} shows '{F}' was not recorded."],
    "cat": ["The {cat} of {ID} is '{v}'."],
    "amt": ["The {amtname} of {ID} is {money}."],
    "amt_nr": ["The {amtname} of {ID} was not recorded."],
    "amt_rng": ["The {amtname} of {ID} is at least {lo} and at most {hi}."],
    # outcomes (expected), loss mode and net mode
    "out": ["For {ID}, the chance of '{event}' is {p}, with a loss of {money}.",
            "For {ID}, '{event}' has a chance of {p} and would cost {money}."],
    "out_net": ["For {ID}, the chance of '{event}' is {p}, with a net amount of {money}."],
    "outp_nr": ["For {ID}, the chance of '{event}' was not recorded; the loss if it happens is {money}."],
    "outp_rng": ["For {ID}, the chance of '{event}' is at least {lo} and at most {hi}."],
    "outa_nr": ["For {ID}, the chance of '{event}' is {p}; the loss if it happens was not recorded."],
    "outa_rng": ["For {ID}, the loss if '{event}' happens is at least {lo} and at most {hi}."],
    "outp_nr_net": ["For {ID}, the chance of '{event}' was not recorded; the net amount if it happens is {money}."],
    "outa_nr_net": ["For {ID}, the chance of '{event}' is {p}; the net amount if it happens was not recorded."],
    "outa_rng_net": ["For {ID}, the net amount if '{event}' happens is at least {lo} and at most {hi}."],
    "cost": ["The own cost of {ID} is {money}.", "{ID} has an own cost of {money}."],
    "act": ["Action {ID} is '{action}'."],
    # chance of one event per entity (rank, matrix)
    "ch": ["For {ID}, the chance of '{event}' is {p}."],
    "ch_nr": ["For {ID}, the chance of '{event}' was not recorded."],
    "ch_rng": ["For {ID}, the chance of '{event}' is at least {lo} and at most {hi}."],
    "loss": ["For {ID}, the loss if '{event}' happens is {money}."],
    # expected number
    "en": ["{ID} has {n} {units}; for each one, the chance of '{event}' is {p}."],
    # count table caption sentence
    "cnt_cap": ["The table below counts past {cases} by class and by whether they show '{E}'."],
    "tbl_cap": ["In the table below, chance and loss refer to '{event}'."],
    "tbl_cap_ch": ["In the table below, chance refers to '{event}'."],
    # S5 tree (held out): branch lines
    "tree_branch": ["If {ID} is classed '{H}' (chance {p}):"],
    "tree_leaf": ["it shows '{E}' with chance {p}."],
}

FIELDS = {
    "id": "reference",
    "shows": "shows",
}

TABLE_COLS = {
    "counts": ["Class", "Showed the sign", "Did not show the sign"],
    "rates": ["Class", "Share of all cases", "Share showing the sign"],
    "outcomes": ["Reference", "Event", "Chance", "Loss"],
    "outcomes_net": ["Reference", "Event", "Chance", "Net amount"],
    "chance_loss": ["Reference", "Chance", "Loss"],
    "chance": ["Reference", "Chance"],
    "actions": ["Reference", "Action", "Own cost", "Chance", "Loss"],
}


def dump() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    with open(DATA / "facts.json", "w", encoding="utf-8") as f:
        json.dump({"SENT": SENT, "FIELDS": FIELDS, "TABLE_COLS": TABLE_COLS}, f, indent=1, ensure_ascii=False)


if __name__ == "__main__":
    dump()
    print("facts.json written")
