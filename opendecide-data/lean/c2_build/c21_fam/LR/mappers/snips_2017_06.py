"""LR-14 SNIPS NLU 2017-06-custom-intent-engines mapper (train_*.json and train_*_full.json). Recast table below.

Own labels: the crowd-written query's intent (the file's key) and its annotated slot spans (`entity`). Forms:
(1) intent pick-one: all 7 intents shown (<= 8 labels, LR-B1); (2) "which value fills slot X": gold = the annotated span,
distractors = the other annotated spans of the SAME utterance plus random contiguous word spans of the same utterance
(same example only, LR-B10); k = 4 where possible, 3 minimum; an utterance whose slot occurs twice is skipped (ambiguous).
NEVER touched: validate_*.json (quarantine); the 2016-12 and 2018-01 folders.
"""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import lr_common as lc  # noqa: E402

DATASET = "snips_2017_06"
F_INTENT = "lr_snips_intent"
F_SLOT = "lr_snips_slot_value"
FORMS = {F_INTENT: "Which intent does this request express?", F_SLOT: "In this request, which value fills the slot {slot}?"}
RECAST_TABLE = {
    "dataset_id": "snipsco/nlu-benchmark 2017-06-custom-intent-engines", "train_file": "train_<Intent>.json, train_<Intent>_full.json",
    "split_field": "file name (validate_* is quarantined)", "source_label_set": ["intent = key; slot = segment.entity"],
    "recast_option_set": {"intent": "all 7 intents", "slot": "gold span + program-chosen spans of the same utterance"},
    "target_format": "Choice 7 (intent) and Choice 3-4 (slot)", "mapping": {"file key": "intent", "segment with entity": "slot value"},
    "distractor_policy": "slot: other annotated spans of the utterance, then random word spans of the same utterance",
    "declared_balancing": "intent: round-robin over intents; slot: round-robin over entity names",
    "declared_drops": ["utterance with the slot twice", "fewer than 2 distractor spans", "U+FFFD in text", "duplicates", "R12 guards"],
    "question_form_ids": [F_INTENT, F_SLOT], "span_selection_rule": "same utterance only", "expected_token_mean": 40,
    "caps": {F_INTENT: 200, F_SLOT: 200},
}
META = {"dataset": DATASET, "lr_id": "LR-14", "family": "LR-intent", "tier": "A", "cap": 400, "share_alike": False,
        "p1_realism": False, "recast_table": RECAST_TABLE}


def read_train(train_dir=None):
    d = lc.guard_train_path(train_dir or lc.raw_train_dir(DATASET))
    for p in sorted(glob.glob(os.path.join(d, "train_*.json"))):
        with open(p, "rb") as f:
            data = json.loads(f.read().decode("utf-8", errors="replace"))
        for intent, queries in data.items():
            for i, q in enumerate(queries):
                yield {"intent": intent, "data": q["data"], "_src_line": "%s#%d" % (os.path.basename(p), i)}


def flatten(data):
    """-> (text, [(entity, start, end)]) by walking the segments with a running offset."""
    text, spans, pos = "", [], 0
    for seg in data:
        t = seg.get("text", "")
        if seg.get("entity"):
            spans.append((seg["entity"], pos, pos + len(t)))
        text += t
        pos += len(t)
    return text, spans


def _slot_name(e):
    return e.replace("_", " ")


class Mapper(lc.BaseMapper):
    META = META
    FORMS = FORMS

    def build(self, src, ctx):
        text, spans = flatten(src["data"])
        text_c = lc.normalise_ws(text)
        if not text_c or "�" in text:
            self.drops.add("empty_or_bad_encoding", src["_src_line"])
            return []
        form = ctx["form"]
        sid = "snips:%s" % src["_src_line"]
        if form == F_INTENT:
            labels = ctx["labels"]
            return [{"form": F_INTENT, "kind": "choice", "context": text_c, "options": list(labels), "gold_text": src["intent"],
                     "source_row_id": sid, "extra": {"label": src["intent"]}}]
        # slot form
        ent = ctx["entity"]
        mine = [s for s in spans if s[0] == ent]
        if len(mine) != 1 or text != "".join(seg.get("text", "") for seg in src["data"]) or lc.normalise_ws(text) != text:
            # keep exact offsets valid: only utterances whose text has no whitespace normalisation difference
            if len(mine) != 1:
                self.drops.add("slot_not_unique", src["_src_line"])
                return []
        e, a, b = mine[0]
        gold = text[a:b].strip()
        if not gold:
            return []
        others = [text[s:t].strip() for (en, s, t) in spans if en != ent and text[s:t].strip() and text[s:t].strip() != gold]
        words = text.split()
        n = max(1, len(gold.split()))
        rng = lc.seeded_rng("snipsslot", self.seed, sid)
        rand = []
        for i in range(0, max(0, len(words) - n + 1)):
            cand = " ".join(words[i:i + n]).strip(" .,!?;:")
            if cand and cand != gold and gold not in cand and cand not in gold and cand not in others:
                rand.append(cand)
        rng.shuffle(rand)
        dist = []
        for c in others + rand:
            if c not in dist:
                dist.append(c)
            if len(dist) == 3:
                break
        if len(dist) < 2:
            self.drops.add("too_few_distractor_spans", src["_src_line"])
            return []
        return [{"form": F_SLOT, "kind": "choice", "context": text_c, "options": [gold] + dist, "gold_text": gold,
                 "source_row_id": sid, "slots": {"slot": _slot_name(ent)}, "extra": {"entity": ent, "span": [a, b]}}]

    def independent_gold(self, src, cand):
        if cand["form"] == F_INTENT:
            return src["intent"]
        pos, text, hit = 0, "", None
        for seg in src["data"]:
            t = seg.get("text", "")
            if seg.get("entity") == cand["extra"]["entity"]:
                hit = (pos, pos + len(t))
            text += t
            pos += len(t)
        return text[hit[0]:hit[1]].strip()

    def map_records(self, records, ctx=None, cap=None, select_key=None):
        recs, seen = [], set()
        for src in records:
            text, _ = flatten(src["data"])
            key = (lc.normalise_ws(text).lower(), src["intent"])
            if key in seen:
                self.drops.add("duplicate_item", src["_src_line"])
                continue
            seen.add(key)
            recs.append(src)
        caps = RECAST_TABLE["caps"]
        labels = sorted({r["intent"] for r in recs})
        rows = []
        # intent form: round-robin over intents
        by = {}
        for r in sorted(recs, key=lambda r: lc.stable_hash("snipsi", self.seed, r["_src_line"])):
            by.setdefault(r["intent"], []).append(r)
        n = 0
        while n < caps[F_INTENT] and any(by.values()):
            for it in sorted(by):
                if by[it] and n < caps[F_INTENT]:
                    src = by[it].pop()
                    for cand in self.build(src, {"form": F_INTENT, "labels": labels}):
                        row = self.finish_candidate(src, cand)
                        if row:
                            rows.append(row)
                            n += 1
        # slot form: round-robin over entity names
        by = {}
        for r in sorted(recs, key=lambda r: lc.stable_hash("snipss", self.seed, r["_src_line"])):
            _, spans = flatten(r["data"])
            cnt = {}
            for e, _, _ in spans:
                cnt[e] = cnt.get(e, 0) + 1
            for e, c in cnt.items():
                if c == 1:
                    by.setdefault(e, []).append(r)
        n = 0
        used = set()
        while n < caps[F_SLOT] and any(by.values()):
            progressed = False
            for e in sorted(by):
                while by[e] and n < caps[F_SLOT]:
                    src = by[e].pop()
                    if src["_src_line"] in used:
                        continue
                    for cand in self.build(src, {"form": F_SLOT, "entity": e}):
                        row = self.finish_candidate(src, cand)
                        if row:
                            rows.append(row)
                            n += 1
                            used.add(src["_src_line"])
                            progressed = True
                    break
            if not progressed and not any(by.values()):
                break
        return rows
