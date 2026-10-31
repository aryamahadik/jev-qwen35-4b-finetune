"""LR-53 ETHICS, MTurk subsets (justice, deontology, virtue, utilitarianism, SHORT commonsense) mapper. Recast table below.

Own labels (MTurk-written scenarios, ETHICS paper): justice label 1 = the claim is reasonable; deontology label 1 = the excuse is
reasonable; virtue label 1 = the trait is exemplified by the scenario; commonsense label 1 = the action is clearly morally wrong
(short rows only; the long Reddit AITA rows were never written to train/); utilitarianism rows are (baseline, less_pleasant) pairs
and the baseline is the more pleasant one. Recast: yes/no questions for the first four, a 2-way pick-one for utilitarianism.
Per subset the yes rate is balanced to 50% (declared); at most 1 row per scenario text for virtue (the same scenario recurs with 5
traits). NEVER touched: test, test_hard, ambig (quarantine).
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import lr_common as lc  # noqa: E402

DATASET = "ethics_mturk"
F_JUS, F_DEO, F_VIR, F_UTL, F_COM = ("lr_ethics_justice", "lr_ethics_deontology", "lr_ethics_virtue", "lr_ethics_utilitarian",
                                     "lr_ethics_commonsense")
FORMS = {F_JUS: "Is the claim reasonable (is it fair to say this person deserves it)?",
         F_DEO: "Is the stated excuse a reasonable response to the request?",
         F_VIR: "Does the person in the scenario show the trait {trait}?",
         F_UTL: "In which situation is the person better off (more pleasant)?",
         F_COM: "Is the action described clearly morally wrong?"}
FILES = {F_JUS: "justice/train.csv", F_DEO: "deontology/train.csv", F_VIR: "virtue/train.csv", F_UTL: "utilitarianism/train.csv",
         F_COM: "commonsense/train.short.csv"}
CAPS = {F_JUS: 140, F_DEO: 140, F_VIR: 120, F_UTL: 100, F_COM: 100}
RECAST_TABLE = {
    "dataset_id": "hendrycks/ethics (MTurk subsets)", "train_file": FILES, "split_field": "file name (test, test_hard, ambig quarantined)",
    "source_label_set": {"justice": "1 reasonable / 0 not", "deontology": "1 reasonable excuse / 0 not", "virtue": "1 trait exemplified / 0 not",
                         "commonsense": "1 clearly wrong / 0 not wrong", "utilitarianism": "baseline more pleasant than less_pleasant"},
    "recast_option_set": {"yes_no": ["Yes", "No"], "utilitarian": "the two scenarios, shuffled"},
    "target_format": "yes/no (4 subsets) and Choice 2 (utilitarianism)",
    "mapping": {"label 1": "Yes", "label 0": "No", "baseline": "gold option"},
    "distractor_policy": "n/a", "declared_balancing": "50% yes per subset; 1 row per virtue scenario",
    "declared_drops": ["empty text", "identical pair (utilitarianism)", "R12 guards"], "question_form_ids": list(FORMS),
    "span_selection_rule": "none", "expected_token_mean": 45, "caps": CAPS,
}
META = {"dataset": DATASET, "lr_id": "LR-53", "family": "LR-reasoning", "tier": "A", "cap": sum(CAPS.values()), "share_alike": False,
        "p1_realism": False, "recast_table": RECAST_TABLE}


def read_train(train_dir=None):
    """Yield {'form', 'row', '_src_line'} for each file of the five MTurk subsets (train files only)."""
    d = lc.guard_train_path(train_dir or lc.raw_train_dir(DATASET))
    for form, rel in FILES.items():
        p = os.path.join(d, rel)
        if not os.path.isfile(p):
            continue
        with open(p, "r", encoding="utf-8", newline="") as f:
            for i, row in enumerate(csv.DictReader(f)):
                yield {"form": form, "row": row, "_src_line": "ethics:%s#%d" % (rel.split("/")[0], i)}


def _yes(row):
    return "Yes" if str(row["label"]).strip() == "1" else "No"


def _virtue_split(sc):
    a, _, b = sc.partition("[SEP]")
    return lc.normalise_ws(a), lc.normalise_ws(b)


class Mapper(lc.BaseMapper):
    META = META
    FORMS = FORMS

    def build(self, src, ctx):
        f, row, sid = src["form"], src["row"], src["_src_line"]
        if f == F_UTL:
            a, b = lc.normalise_ws(row.get("baseline")), lc.normalise_ws(row.get("less_pleasant"))
            if not a or not b or a == b:
                self.drops.add("empty_or_identical_pair", sid)
                return []
            return [{"form": f, "kind": "choice", "context": "", "options": [a, b], "gold_text": a, "source_row_id": sid,
                     "extra": {"subset": "utilitarianism"}}]
        if f == F_JUS:
            ctxt = lc.normalise_ws(row.get("scenario"))
        elif f == F_DEO:
            sc, ex = lc.normalise_ws(row.get("scenario")), lc.normalise_ws(row.get("excuse"))
            ctxt = ("Request: %s\nExcuse: %s" % (sc, ex)) if sc and ex else ""
        elif f == F_VIR:
            sc, tr = _virtue_split(row.get("scenario", ""))
            ctxt = ("Scenario: %s" % sc) if sc and tr else ""
        else:
            ctxt = lc.normalise_ws(row.get("input"))
        if not ctxt:
            self.drops.add("empty_text", sid)
            return []
        slots = {"trait": _virtue_split(row["scenario"])[1]} if f == F_VIR else {}
        return [{"form": f, "kind": "yesno", "context": ctxt, "options": ["Yes", "No"], "gold_text": _yes(row), "source_row_id": sid,
                 "slots": slots, "extra": {"subset": sid.split(":")[1].split("#")[0], "scenario": ctxt if f == F_VIR else None}}]

    def independent_gold(self, src, cand):
        row = src["row"]
        if src["form"] == F_UTL:
            return lc.normalise_ws(row["baseline"])
        return "Yes" if int(str(row["label"]).strip()) == 1 else "No"

    def map_records(self, records, ctx=None, cap=None, select_key=None):
        by_form = {}
        for src in records:
            by_form.setdefault(src["form"], []).append(src)
        rows = []
        for form, items in by_form.items():
            if form == F_UTL:
                groups = {"pair": [(s,) for s in items]}
            else:
                groups = {"Yes": [(s,) for s in items if _yes(s["row"]) == "Yes"], "No": [(s,) for s in items if _yes(s["row"]) == "No"]}

            def make(item, form=form):
                out = []
                for cand in self.build(item[0], {}):
                    r = self.finish_candidate(item[0], cand)
                    if r:
                        out.append(r)
                return out
            unit = (lambda it: lc.normalise_ws(it[0]["row"]["scenario"].partition("[SEP]")[0])) if form == F_VIR else None
            rows += lc.round_robin_take(groups, "ethics%s%s" % (form, self.seed), CAPS[form], make, unit_of=unit,
                                        unit_limit=1 if unit else None)
        return rows
