"""LR-17 ABCD mapper (asappresearch/abcd v1.1 train split). Recast table below (Opus approves, G-R3 batch).

Own labels: the dataset's per-turn Targets (program-derived from the human-human dialogue and the agent's button log):
Nextstep Selection (take_action / retrieve_utterance; this release has no end_conversation target on agent turns) and
Action Prediction (the button the agent clicked, 30 values). Recast: (1) "what does the agent do next?" pick-one among 2 options
over the dialogue so far (balanced 50/50, declared); (2) "which button does the agent click next?" pick-one, 30 actions
> 8 so gold + 3/7 hard distractor actions (k alternating 4/8). Context = the ORIGINAL (not delexed) turns before the target
turn, long histories keep the first customer turn and the most recent turns within the budget ("[... earlier turns omitted ...]").
NEVER touched: dev, test (quarantine); utterances.json (pools all splits).
"""
import gzip
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import lr_common as lc  # noqa: E402

DATASET = "abcd"
F_NEXT = "lr_abcd_next_step"
F_ACT = "lr_abcd_action"
FORMS = {F_NEXT: "What does the agent do next?", F_ACT: "Which action does the agent take next?"}
NEXT_TEXT = {"take_action": "take an action in the support system", "retrieve_utterance": "reply to the customer in the chat"}
BUDGET = 600
RECAST_TABLE = {
    "dataset_id": "asappresearch/abcd data/abcd_v1.1.json.gz key 'train' (8,034 dialogues)", "train_file": "abcd_v1.1.train.json.gz",
    "split_field": "top-level key (program-split in the downloader)",
    "source_label_set": {"next": ["take_action", "retrieve_utterance"], "action": "30 button names (targets[2])"},
    "recast_option_set": {"next": NEXT_TEXT, "action": "gold action + k-1 confusable actions"},
    "target_format": "Choice 2 (next step) and Choice k in {4, 8} (action)", "mapping": {"targets[1]": "next step", "targets[2]": "action"},
    "distractor_policy": "name overlap + TF-IDF logistic confusion on train histories",
    "declared_balancing": "next: 50/50 by class; action: round-robin over the 30 actions; at most 3 rows per dialogue",
    "declared_drops": ["empty history", "history that cannot fit the budget even with the last turn", "R12 guards / PII"],
    "question_form_ids": [F_NEXT, F_ACT], "span_selection_rule": "first customer turn + most recent turns", "expected_token_mean": 420,
    "caps": {F_NEXT: 350, F_ACT: 350},
}
META = {"dataset": DATASET, "lr_id": "LR-17", "family": "LR-dialogue", "tier": "A", "cap": 700, "share_alike": False,
        "p1_realism": False, "recast_table": RECAST_TABLE}
SPEAKER = {"customer": "Customer", "agent": "Agent", "action": "System"}


def read_train(train_dir=None):
    d = lc.guard_train_path(train_dir or lc.raw_train_dir(DATASET))
    with gzip.open(os.path.join(d, "abcd_v1.1.train.json.gz"), "rt", encoding="utf-8") as f:
        for c in json.load(f):
            c["_src_line"] = str(c["convo_id"])
            yield c


def history_text(original, upto):
    """Turns [0, upto) as text lines within BUDGET tokens: first customer turn + the most recent turns."""
    lines = ["%s: %s" % (SPEAKER.get(sp, sp), lc.normalise_ws(tx)) for sp, tx in original[:upto]]
    if not lines:
        return None
    if lc.approx_tokens("\n".join(lines)) <= BUDGET:
        return "\n".join(lines)
    first = next((i for i, (sp, _) in enumerate(original[:upto]) if sp == "customer"), 0)
    head = [lines[first]]
    tail = []
    used = lc.approx_tokens(head[0]) + 8
    for ln in reversed(lines[first + 1:]):
        t = lc.approx_tokens(ln)
        if used + t > BUDGET:
            break
        tail.append(ln)
        used += t
    if not tail:
        return None
    return "\n".join(head + ["[... earlier turns omitted ...]"] + list(reversed(tail)))


class Mapper(lc.BaseMapper):
    META = META
    FORMS = FORMS

    def build(self, src, ctx):
        i, form = ctx["turn"], ctx["form"]
        t = src["delexed"][i]
        txt = history_text(src["original"], i)
        if txt is None:
            self.drops.add("empty_or_unfittable_history", src["_src_line"])
            return []
        sid = "abcd:%s#%d" % (src["_src_line"], i)
        if form == F_NEXT:
            lab = t["targets"][1]
            return [{"form": F_NEXT, "kind": "choice", "context": txt, "options": [NEXT_TEXT[k] for k in sorted(NEXT_TEXT)],
                     "gold_text": NEXT_TEXT[lab], "source_row_id": sid, "extra": {"label": lab}}]
        lab = t["targets"][2]
        labels = ctx["labels"]
        k = self.ksched.next(len(labels))
        dist = ctx["chooser"].choose(lab, k, key=sid, text=txt)
        return [{"form": F_ACT, "kind": "choice", "context": txt, "options": [lab] + dist, "gold_text": lab,
                 "source_row_id": sid, "k_full": len(labels), "extra": {"label": lab}}]

    def independent_gold(self, src, cand):
        i = int(cand["source_row_id"].rsplit("#", 1)[1])
        tg = src["delexed"][i]["targets"]
        if cand["form"] == F_NEXT:
            return NEXT_TEXT[tg[1]]
        return tg[2]

    def map_records(self, records, ctx=None, cap=None, select_key=None):
        convos = list(records)
        caps = RECAST_TABLE["caps"]
        # items: (convo, turn index, label) per form
        nxt, act = {}, {}
        for c in convos:
            for i, t in enumerate(c["delexed"]):
                if t["speaker"] == "customer":
                    continue
                if t["targets"][1] in NEXT_TEXT:
                    nxt.setdefault(t["targets"][1], []).append((c, i))
                if t["targets"][2]:
                    act.setdefault(t["targets"][2], []).append((c, i))
        rows = []
        for form, groups, label_names in ((F_NEXT, nxt, None), (F_ACT, act, sorted(act))):
            chooser = None
            if form == F_ACT:
                chooser = lc.DistractorChooser(label_names)
                sample = []
                for lab, items in groups.items():
                    for c, i in sorted(items, key=lambda t: lc.stable_hash("abcdfit", self.seed, t[0]["_src_line"], t[1]))[:60]:
                        sample.append((history_text(c["original"], i) or "", lab))
                chooser.fit([s[0] for s in sample], [s[1] for s in sample], seed=self.seed)
            for g in groups.values():
                g.sort(key=lambda t: lc.stable_hash("abcd", form, self.seed, t[0]["_src_line"], t[1]))
            names = sorted(groups, key=lambda l: lc.stable_hash("abcdl", self.seed, l))
            per_convo = {}
            n = 0
            while n < caps[form] and any(groups.values()):
                for lab in names:
                    if n >= caps[form]:
                        break
                    while groups[lab]:
                        c, i = groups[lab].pop()
                        if per_convo.get((form, c["_src_line"]), 0) >= 3:
                            continue
                        made = False
                        for cand in self.build(c, {"form": form, "turn": i, "labels": label_names, "chooser": chooser}):
                            r = self.finish_candidate(c, cand)
                            if r:
                                rows.append(r)
                                n += 1
                                made = True
                                per_convo[(form, c["_src_line"])] = per_convo.get((form, c["_src_line"]), 0) + 1
                        if made:
                            break
        return rows
