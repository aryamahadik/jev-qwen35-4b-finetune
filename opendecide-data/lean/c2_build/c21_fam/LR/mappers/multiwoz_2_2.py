"""LR-18 MultiWOZ 2.2 mapper (train split; hand-annotated SYSTEM acts only). Recast table below (Opus approves, G-R3 batch).

Own label: for each SYSTEM turn the corrected dialog_acts.json lists the system's dialogue acts (hand-annotated in 2.2).
Recast: yes/no "Does the assistant need to ask the user for a missing value in its next turn?" = the system turn carries
a '*-Request' act (Restaurant-Request, Hotel-Request, Train-Request, Booking-Request, Taxi-Request, ...). Context = the
dialogue before that turn. USER-turn acts (heuristic) are never read. Balanced 50/50 by declared stratification, at most 2
rows per dialogue. NEVER touched: dev, test dialogues (quarantine).
"""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import lr_common as lc  # noqa: E402

DATASET = "multiwoz_2_2"
FORM = "lr_multiwoz_needs_ask"
FORMS = {FORM: "Does the assistant need to ask the user for a missing value in its next turn?"}
BUDGET = 500
RECAST_TABLE = {
    "dataset_id": "budzianowski/multiwoz data/MultiWOZ_2.2 train", "train_file": "train/dialogues_*.json + dialog_acts.train.json",
    "split_field": "directory (train/ only); acts file filtered by train dialogue id in the downloader",
    "source_label_set": ["system dialog_act names, e.g. Restaurant-Request, Hotel-Inform"], "recast_option_set": ["Yes", "No"],
    "target_format": "yes/no", "mapping": {"any act name ending -Request": "Yes", "otherwise": "No"},
    "distractor_policy": "n/a", "declared_balancing": "50/50 yes/no; at most 2 rows per dialogue; no-rows spread over first act domain",
    "declared_drops": ["system turn with no acts entry", "first turn (empty history)", "R12 guards / PII"],
    "question_form_ids": [FORM], "span_selection_rule": "first user turn + most recent turns within the budget",
    "expected_token_mean": 220, "never_read": ["acts of USER turns"],
}
META = {"dataset": DATASET, "lr_id": "LR-18", "family": "LR-dialogue", "tier": "A", "cap": 500, "share_alike": False,
        "p1_realism": False, "recast_table": RECAST_TABLE}


def read_train(train_dir=None):
    d = lc.guard_train_path(train_dir or lc.raw_train_dir(DATASET))
    with open(os.path.join(d, "dialog_acts.train.json"), "r", encoding="utf-8") as f:
        acts = json.load(f)
    for p in sorted(glob.glob(os.path.join(d, "train", "dialogues_*.json"))):
        with open(p, "r", encoding="utf-8") as f:
            for dlg in json.load(f):
                dlg["_acts"] = acts.get(dlg["dialogue_id"], {})
                dlg["_src_line"] = dlg["dialogue_id"]
                yield dlg


def _history(turns, upto):
    lines = ["%s: %s" % ("User" if t["speaker"] == "USER" else "Assistant", lc.normalise_ws(t["utterance"])) for t in turns[:upto]]
    if not lines:
        return None
    if lc.approx_tokens("\n".join(lines)) <= BUDGET:
        return "\n".join(lines)
    head, tail, used = [lines[0]], [], lc.approx_tokens(lines[0]) + 8
    for ln in reversed(lines[1:]):
        t = lc.approx_tokens(ln)
        if used + t > BUDGET:
            break
        tail.append(ln)
        used += t
    return "\n".join(head + ["[... earlier turns omitted ...]"] + list(reversed(tail))) if tail else None


def _is_request(act_names):
    return any(a.endswith("-Request") for a in act_names)


class Mapper(lc.BaseMapper):
    META = META
    FORMS = FORMS

    def build(self, src, ctx):
        i = ctx["turn"]
        t = src["turns"][i]
        a = src["_acts"].get(str(t["turn_id"]))
        if t["speaker"] != "SYSTEM" or not a:
            self.drops.add("no_system_acts", src["_src_line"])
            return []
        hist = _history(src["turns"], i)
        if hist is None:
            self.drops.add("empty_history", src["_src_line"])
            return []
        gold = "Yes" if _is_request(a["dialog_act"].keys()) else "No"
        return [{"form": FORM, "kind": "yesno", "context": hist, "options": ["Yes", "No"], "gold_text": gold,
                 "source_row_id": "multiwoz:%s#%d" % (src["_src_line"], i),
                 "extra": {"acts": sorted(a["dialog_act"].keys())}}]

    def independent_gold(self, src, cand):
        i = int(cand["source_row_id"].rsplit("#", 1)[1])
        acts = src["_acts"][str(src["turns"][i]["turn_id"])]["dialog_act"]
        return "Yes" if any(k.split("-")[-1] == "Request" for k in acts) else "No"

    def map_records(self, records, ctx=None, cap=None, select_key=None):
        cap = cap if cap is not None else META["cap"]
        groups = {"Yes": [], "No": []}
        for dlg in records:
            for i, t in enumerate(dlg["turns"]):
                if t["speaker"] != "SYSTEM" or i == 0:
                    continue
                a = dlg["_acts"].get(str(t["turn_id"]))
                if not a:
                    continue
                groups["Yes" if _is_request(a["dialog_act"].keys()) else "No"].append((dlg, i))

        def make(item):
            dlg, i = item
            out = []
            for cand in self.build(dlg, {"turn": i}):
                r = self.finish_candidate(dlg, cand)
                if r:
                    out.append(r)
            return out
        return lc.round_robin_take(groups, "multiwoz%s" % self.seed, cap, make, unit_of=lambda it: it[0]["_src_line"], unit_limit=2)
