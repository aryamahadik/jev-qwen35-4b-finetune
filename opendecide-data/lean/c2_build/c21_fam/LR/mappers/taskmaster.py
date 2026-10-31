"""LR-19 Taskmaster TM-1 / TM-2 / TM-3 mapper (train parts only; TM-4 excluded). Recast table below (Opus approves, G-R3 batch).

Own labels (crowd Wizard-of-Oz and self-dialog annotations):
 (1) TM-3 (TicketTalk) train examples: the shipped train TSV gives the dialogue so far and the TRUE next move: '[PN]...' = the
     assistant calls an API (act), '[A]...' = the assistant speaks (ask / inform). Recast: yes/no "Does the assistant call a tool
     next?" (the plan's ask-vs-act). The target text itself is never shown.
 (2) TM-1 / TM-2 segment annotations: each annotated span carries one annotation name (e.g. restaurant_reservation.time.reservation).
     Recast: pick-one "what kind of information does this highlighted span give?" among the gold name and k-1 hard distractor names
     (k alternating 4 / 8; > 8 labels). A span with two different annotation names is skipped.
NEVER touched: TM-1 dev/test ids, the TM-1 woz hold-out, the TM-2 10% hold-out, TM-3 dev/test shards, TM-3 data/*.json.
"""
import gzip
import glob
import heapq
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import lr_common as lc  # noqa: E402

DATASET = "taskmaster"
F_ACT = "lr_taskmaster_calls_tool"
F_SEG = "lr_taskmaster_span_type"
FORMS = {F_ACT: "Does the assistant call a tool next?", F_SEG: "What kind of information does the highlighted span give?"}
BUDGET = 500
RECAST_TABLE = {
    "dataset_id": "google-research-datasets/Taskmaster TM-1 (self+woz), TM-2, TM-3 train parts",
    "train_file": "tm1_train.json.gz, tm2_*.train.json.gz, tm3_train.tsv.gz",
    "split_field": "TM-1 self: shipped train.csv; TM-1 woz and TM-2: own seeded 10% hold-out; TM-3: shipped splits/train shards",
    "source_label_set": {"tm3": "target prefix [PN] (API call) vs [A] (assistant text)", "seg": "segment annotation name (one per span)"},
    "recast_option_set": {"tm3": ["Yes", "No"], "seg": "gold annotation name + k-1 confusable names"},
    "target_format": "yes/no (tm3) and Choice k in {4, 8} (spans)", "mapping": {"[PN]": "Yes", "[A]": "No"},
    "distractor_policy": "name overlap + TF-IDF logistic confusion on the train span texts",
    "declared_balancing": "tm3: 50/50; spans: round-robin over annotation names; at most 2 rows per dialogue",
    "declared_drops": ["span with 2 different annotation names", "empty span", "history that cannot fit", "R12 guards / PII"],
    "question_form_ids": [F_ACT, F_SEG], "span_selection_rule": "first customer turn + most recent turns (tm3); last 3 utterances (spans)",
    "expected_token_mean": 300, "caps": {F_ACT: 150, F_SEG: 150},
}
META = {"dataset": DATASET, "lr_id": "LR-19", "family": "LR-dialogue", "tier": "A", "cap": 300, "share_alike": False,
        "p1_realism": False, "recast_table": RECAST_TABLE}

_TAG = re.compile(r"<(U|A|PN|PAN|PAV|PR|PRAN|PRAV|C)>")


# ----------------------------------------------------------------------------------------------------------
# reader
# ----------------------------------------------------------------------------------------------------------
def read_train(train_dir=None, tm3=True):
    d = lc.guard_train_path(train_dir or lc.raw_train_dir(DATASET))
    p1 = os.path.join(d, "tm1_train.json.gz")
    if os.path.isfile(p1):
        with gzip.open(p1, "rt", encoding="utf-8") as f:
            for dlg in json.load(f):
                yield {"kind": "dialog", "dlg": dlg, "_src_line": "tm1:" + dlg["conversation_id"]}
    for p in sorted(glob.glob(os.path.join(d, "tm2_*.train.json.gz"))):
        with gzip.open(p, "rt", encoding="utf-8") as f:
            for dlg in json.load(f):
                yield {"kind": "dialog", "dlg": dlg, "_src_line": "tm2:" + dlg["conversation_id"]}
    p3 = os.path.join(d, "tm3_train.tsv.gz")
    if tm3 and os.path.isfile(p3):
        with gzip.open(p3, "rt", encoding="utf-8") as f:
            for i, line in enumerate(f):
                parts = line.rstrip("\n").split("\t")
                if len(parts) != 3:
                    continue
                yield {"kind": "tm3", "input": parts[0], "target": parts[1], "dlg_id": parts[2], "_src_line": "tm3:%s#%d" % (parts[2], i)}


# ----------------------------------------------------------------------------------------------------------
# rendering
# ----------------------------------------------------------------------------------------------------------
def render_tm3_input(inp):
    """TM-3 tagged prefix -> readable lines. Text before the first <C> is metadata and is dropped."""
    if "<C>" in inp:
        inp = inp.split("<C>", 1)[1]
    toks = _TAG.split(inp)
    # toks = [pre, tag, text, tag, text, ...]
    lines, i = [], 1
    call = None
    res = None

    def flush_call():
        nonlocal call
        if call:
            lines.append("[tool call: %s(%s)]" % (call["name"], ", ".join("%s=%s" % a for a in call["args"])))
            call = None

    def flush_res():
        nonlocal res
        if res:
            lines.append("[tool result: %s -> %s]" % (res["name"], ", ".join("%s=%s" % a for a in res["vals"])))
            res = None
    while i < len(toks) - 1:
        tag, text = toks[i], toks[i + 1].strip()
        if tag in ("U", "A"):
            flush_call(); flush_res()
            lines.append("%s: %s" % ("Customer" if tag == "U" else "Assistant", lc.normalise_ws(text)))
        elif tag == "PN":
            flush_call(); flush_res()
            call = {"name": text, "args": []}
        elif tag == "PAN" and call is not None:
            call["args"].append([text, ""])
        elif tag == "PAV" and call is not None and call["args"]:
            call["args"][-1] = (call["args"][-1][0], lc.normalise_ws(text))
        elif tag == "PR":
            flush_call(); flush_res()
            res = {"name": text, "vals": []}
        elif tag == "PRAN" and res is not None:
            res["vals"].append([text, ""])
        elif tag == "PRAV" and res is not None and res["vals"]:
            k, v = res["vals"][-1]
            res["vals"][-1] = (k, (v + ", " if v else "") + lc.normalise_ws(text))
        i += 2
    flush_call(); flush_res()
    return lines


def _fit_lines(lines, budget=BUDGET):
    if not lines:
        return None
    if lc.approx_tokens("\n".join(lines)) <= budget:
        return "\n".join(lines)
    first = next((i for i, l in enumerate(lines) if l.startswith("Customer:")), 0)
    head, tail, used = [lines[first]], [], lc.approx_tokens(lines[first]) + 8
    for ln in reversed(lines[first + 1:]):
        t = lc.approx_tokens(ln)
        if used + t > budget:
            break
        tail.append(ln)
        used += t
    return "\n".join(head + ["[... earlier turns omitted ...]"] + list(reversed(tail))) if tail else None


def seg_items(rec):
    """-> list of (label, utterance index, segment index) for spans with exactly one annotation name and a non-empty text."""
    out = []
    for ui, u in enumerate(rec["dlg"]["utterances"]):
        for si, s in enumerate(u.get("segments") or []):
            names = {a.get("name") for a in s.get("annotations", []) if a.get("name")}
            if len(names) == 1 and (s.get("text") or "").strip():
                out.append((next(iter(names)), ui, si))
    return out


class Mapper(lc.BaseMapper):
    META = META
    FORMS = FORMS

    # -- builders --------------------------------------------------------------------------------------------
    def build(self, src, ctx):
        if src["kind"] == "tm3":
            lines = render_tm3_input(src["input"])
            txt = _fit_lines(lines)
            tgt = src["target"]
            if txt is None or not (tgt.startswith("[PN]") or tgt.startswith("[A]")):
                self.drops.add("tm3_unusable_example", src["_src_line"])
                return []
            gold = "Yes" if tgt.startswith("[PN]") else "No"
            return [{"form": F_ACT, "kind": "yesno", "context": txt, "options": ["Yes", "No"], "gold_text": gold,
                     "source_row_id": src["_src_line"], "extra": {"dialog": src["dlg_id"]}}]
        label, ui, si = ctx["item"]
        dlg = src["dlg"]
        u = dlg["utterances"][ui]
        span = lc.normalise_ws(u["segments"][si]["text"])
        lines = ["%s: %s" % ("Customer" if x["speaker"] == "USER" else "Assistant", lc.normalise_ws(x["text"]))
                 for x in dlg["utterances"][max(0, ui - 2):ui + 1]]
        txt = _fit_lines(lines + ['Highlighted span: "%s"' % span], BUDGET)
        if txt is None or not span:
            self.drops.add("seg_unusable", src["_src_line"])
            return []
        labels = ctx["labels"]
        k = self.ksched.next(len(labels))
        sid = "%s#%d.%d" % (src["_src_line"], ui, si)
        dist = ctx["chooser"].choose(label, k, key=sid, text=txt)
        return [{"form": F_SEG, "kind": "choice", "context": txt, "options": [label] + dist, "gold_text": label,
                 "source_row_id": sid, "k_full": len(labels), "extra": {"dialog": src["_src_line"], "span": span}}]

    def independent_gold(self, src, cand):
        if cand["form"] == F_ACT:
            return "Yes" if src["target"].startswith("[PN]") else "No"
        ui, si = [int(x) for x in cand["source_row_id"].rsplit("#", 1)[1].split(".")]
        segs = src["dlg"]["utterances"][ui]["segments"][si]
        return sorted({a["name"] for a in segs["annotations"]})[0]

    # -- selection -------------------------------------------------------------------------------------------
    def map_records(self, records, ctx=None, cap=None, select_key=None):
        caps = RECAST_TABLE["caps"]
        seg_groups, seg_texts, tm3_heaps = {}, [], {"Yes": [], "No": []}
        keep = 6 * caps[F_ACT]
        for rec in records:
            if rec["kind"] == "dialog":
                for lab, ui, si in seg_items(rec):
                    seg_groups.setdefault(lab, []).append((rec, (lab, ui, si)))
            else:
                lab = "Yes" if rec["target"].startswith("[PN]") else ("No" if rec["target"].startswith("[A]") else None)
                if lab is None:
                    continue
                h = lc.stable_hash("tm3", self.seed, rec["_src_line"])
                heap = tm3_heaps[lab]
                if len(heap) < keep:
                    heapq.heappush(heap, (-h, rec["_src_line"], rec))
                elif -h > heap[0][0]:
                    heapq.heapreplace(heap, (-h, rec["_src_line"], rec))
        rows = []
        # ---- TM-3 act / ask ----
        groups = {k: [t[2] for t in sorted(v, key=lambda t: -t[0])] for k, v in tm3_heaps.items()}
        groups = {k: [(r,) for r in v] for k, v in groups.items()}

        def make3(item):
            rec = item[0]
            out = []
            for cand in self.build(rec, {}):
                r = self.finish_candidate(rec, cand)
                if r:
                    out.append(r)
            return out
        rows += lc.round_robin_take(groups, "tm3%s" % self.seed, caps[F_ACT], make3, unit_of=lambda it: it[0]["dlg_id"], unit_limit=2)
        # ---- spans ----
        if seg_groups:
            labels = sorted(seg_groups)
            chooser = lc.DistractorChooser(labels)
            sample_texts, sample_labels = [], []
            for lab in labels:
                for rec, (l, ui, si) in sorted(seg_groups[lab], key=lambda t: lc.stable_hash("segfit", self.seed, t[0]["_src_line"], t[1][1], t[1][2]))[:40]:
                    u = rec["dlg"]["utterances"][ui]
                    sample_texts.append(lc.normalise_ws(u["text"]) + " || " + lc.normalise_ws(u["segments"][si]["text"]))
                    sample_labels.append(lab)
            chooser.fit(sample_texts, sample_labels, seed=self.seed)

            def make_seg(item):
                rec, it = item
                out = []
                for cand in self.build(rec, {"item": it, "labels": labels, "chooser": chooser}):
                    r = self.finish_candidate(rec, cand)
                    if r:
                        out.append(r)
                return out
            rows += lc.round_robin_take(seg_groups, "seg%s" % self.seed, caps[F_SEG], make_seg,
                                        unit_of=lambda it: it[0]["_src_line"], unit_limit=2)
        return rows
