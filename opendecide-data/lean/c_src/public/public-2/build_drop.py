"""DROP candidates (C_DATA_SPEC.md v4 3.2 #11: numeric comparisons as yes/no thresholds). Train split only
(drop_dataset_train.json). Split 90/10 by passage id (DROP gives no page title; a passage is one Wikipedia excerpt).

Gold = the crowd's number answer. Support filter (keeps the label checkable against the passage, never changes it):
the number is stated in the passage, or is the sum / difference of two stated numbers (or 100 minus one), or the
question is a count question with an answer of at most 12.
Framings: drop_thr_yn (answer vs threshold T, 40% at the exact boundary) and drop_ch (number options: gold + passage
numbers and off-by-one errors; abstain on some rows).
"""
from __future__ import annotations

import json
import re
from fractions import Fraction

from p2_common import RAW, TMP, page_bucket, rng_for, stable_id, log_progress
from render import fmt_num, holds, pick_ranked, pick_threshold

DATASET = "DROP"
SOURCE = "c_pub_drop"
WORDNUM = {w: i for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen "
                                      "fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}

W_THR = {
    "drop_thr_w1": "Is the number the question asks for {op} {T}?",
    "drop_thr_w2": "Based on the passage, is the answer to the question {op} {T}?",
    "drop_thr_w3": "Does the answer to the question come to {op} {T}?",
    "drop_thr_w4": "Working only from the passage, is the requested number {op} {T}?",
}
W_CH = {
    "drop_ch_w1": "Which number answers the question?",
    "drop_ch_w2": "Pick the answer to the question from the options.",
    "drop_ch_w3": "Using the passage, choose the correct number.",
    "drop_ch_w4": "Select the option the passage supports as the answer.",
}
OPP = {">": ["more than", "greater than", "above"], ">=": ["at least", "no less than"],
       "<": ["less than", "below", "fewer than"], "<=": ["at most", "no more than"]}
CARDS = {
    "drop_card_line_ch": {"style": "one_line", "qtype": "choice",
                          "text": "Answer from the passage only: the answer is a number worked out from facts the "
                                  "passage states."},
    "drop_card_rubric_ch": {"style": "rubric", "qtype": "choice",
                            "text": "Rules:\n- Use only facts stated in the passage; no outside knowledge.\n"
                                    "- Count, add, subtract or compare the stated facts as the question asks.\n"
                                    "- Pick 'None of these' only when no listed number is the answer."},
    "drop_card_line_yn": {"style": "one_line", "qtype": "noul",
                          "text": "- yes: the number that answers the question makes the stated comparison true.\n"
                                  "- no: it makes the comparison false."},
    "drop_card_rubric_yn": {"style": "rubric", "qtype": "noul",
                            "text": "- yes: the number that answers the question (worked out only from the passage) "
                                    "makes the stated comparison true.\n- no: that number makes the comparison "
                                    "false.\nComparison words: 'more than', 'greater than', 'above', 'less than', "
                                    "'fewer than' and 'below' exclude the threshold itself; 'at least', 'no less "
                                    "than', 'at most' and 'no more than' include it."},
}

NUM_RE = re.compile(r"(?<![\w.])-?\d{1,3}(?:,\d{3})+(?:\.\d+)?|(?<![\w.])-?\d+(?:\.\d+)?")


def passage_numbers(p):
    out = set()
    for m in NUM_RE.findall(p):
        try:
            out.add(Fraction(m.replace(",", "")))
        except ValueError:
            pass
    for w in re.findall(r"[A-Za-z]+", p):
        if w.lower() in WORDNUM:
            out.add(Fraction(WORDNUM[w.lower()]))
    return out


def supported(q, gold, nums):
    if gold in nums:
        return "stated"
    nl = sorted(nums)
    if len(nl) <= 80:
        for a in nl:
            if Fraction(100) - a == gold:
                return "hundred_minus"
            for b in nl:
                if a - b == gold or (a + b == gold and a <= b):
                    return "pair"
    if re.match(r"\s*how many\b", q, re.I) and not re.search(r"\b(yards?|points?|percent|years?|people|"
                                                             r"%|households|families|men|women|soldiers|troops)\b",
                                                             q, re.I) and gold.denominator == 1 and 0 < gold <= 12:
        return "count"
    return None


def threshold(rng, x, want_yes):
    if x.denominator == 1:
        step = Fraction(rng.choice([1, 1, 2, 3, 5]) if abs(x) >= 6 else rng.choice([1, 1, 2]))
    else:
        step = Fraction(rng.choice([1, 2, 5]), 10) if abs(x) < 10 else Fraction(rng.choice([1, 2, 3]))
    r = pick_threshold(rng, x, want_yes, step, boundary_ok=True)
    if not r:
        return None
    op, T, _ = r
    if T < 0:
        return None
    return op, T


def pick_card(rng, qtype):
    u = rng.random()
    if u < 0.15:
        return None
    sfx = "ch" if qtype == "choice" else "yn"
    return f"drop_card_line_{sfx}" if u < 0.55 else f"drop_card_rubric_{sfx}"


def build(targets, dev_target, out_path):
    d = json.load(open(RAW / "drop_dataset" / "drop_dataset_train.json"))
    pids = sorted(d)
    rng0 = rng_for("drop_order")
    rng0.shuffle(pids)
    want = {f: int(targets[f] * 1.6) + 15 for f in targets}
    dev_want = {f: dev_target[f] * 2 + 5 for f in targets}
    have = {(p, f): 0 for p in ("train", "dev") for f in targets}
    stats = {"passages": 0, "no_number": 0, "unsupported": 0, "kept": 0, "support": {}}
    cands = []
    for pid in pids:
        p = d[pid]
        passage = re.sub(r"\s+", " ", p["passage"]).strip()
        if len(passage.split()) > 420:
            continue
        part = "dev" if page_bucket(pid) == 0 else "train"
        stats["passages"] += 1
        nums = passage_numbers(passage)
        rng = rng_for("drop", pid)
        qas = list(p["qa_pairs"])
        rng.shuffle(qas)
        for qa in qas:
            a = qa["answer"]
            if not a.get("number") or a.get("spans") or any(a["date"].values()):
                stats["no_number"] += 1
                continue
            try:
                gold = Fraction(a["number"].replace(",", ""))
            except ValueError:
                continue
            if gold < 0 or not (4 <= len(qa["question"].split()) <= 40):
                continue
            sup = supported(qa["question"], gold, nums)
            if not sup:
                stats["unsupported"] += 1
                continue
            frs = [f for f in targets if have[(part, f)] < (want[f] if part == "train" else dev_want[f])]
            if not frs:
                break
            frs.sort(key=lambda f: have[(part, f)] / (want[f] if part == "train" else dev_want[f]))
            fr = frs[0]
            row = make_row(fr, pid, qa, passage, gold, nums, rng)
            if not row:
                continue
            row["_x"].update(part=part, page=pid, support=sup)
            stats["support"][sup] = stats["support"].get(sup, 0) + 1
            have[(part, fr)] += 1
            cands.append(row)
            break  # one question per passage
        if all(have[("train", f)] >= want[f] and have[("dev", f)] >= dev_want[f] for f in targets):
            break
    stats["kept"] = len(cands)
    stats["have"] = {f"{p}:{f}": n for (p, f), n in have.items()}
    with open(out_path, "w") as f:
        for r in cands:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    log_progress(f"DROP candidates: {json.dumps(stats)}")
    return stats


def make_row(fr, pid, qa, passage, gold, nums, rng):
    state = f"Passage:\n{passage}\n\nQuestion: {qa['question'].strip()}"
    common = dict(record_id=f"{pid}:{qa['query_id']}", x=fmt_num(gold), record_text=passage)
    if fr == "drop_thr_yn":
        want_yes = rng.random() < 0.5
        th = threshold(rng, gold, want_yes)
        if not th:
            return None
        op, T = th
        wid = rng.choice(sorted(W_THR))
        instr = W_THR[wid].format(op=rng.choice(OPP[op]), T=fmt_num(T))
        g = int(holds(gold, op, T))
        cid = pick_card(rng, "noul")
        return row_obj(fr, pid, qa, state, "noul", instr, None, g, cid, wid,
                       dict(common, op=op, T=fmt_num(T), boundary=(T == gold)))
    # choice: distractors are passage numbers and numbers computed from two passage numbers (sum or difference),
    # so neither "the option not in the passage" nor "the middle of a +-1 run" points to the gold
    pnum = sorted(n for n in nums if n >= 0 and fmt_num(n) != fmt_num(gold))
    comp = set()
    small = sorted(nums)[:60]
    for a in small:
        for b in small:
            for v in (a - b, a + b):
                if v >= 0 and v not in nums and fmt_num(v) != fmt_num(gold):
                    comp.add(v)
    scale = max(abs(gold), Fraction(1))
    comp = sorted(comp, key=lambda v: abs(v - gold))[:8]
    pnum = sorted(pnum, key=lambda v: abs(v - gold) / scale)[:8]
    rng.shuffle(comp)
    rng.shuffle(pnum)
    gold_in_passage = gold in nums
    n_comp = 1 if gold_in_passage else 2
    cand = []
    for n in comp[:n_comp] + pnum + comp[n_comp:]:
        s_ = fmt_num(n)
        if s_ != fmt_num(gold) and s_ not in cand:
            cand.append(s_)
    k = rng.randint(2, 4)
    if len(cand) < k:
        return None
    cand = pick_ranked(rng, cand, gold, k)
    if not cand:
        return None
    abstain = rng.random() < 0.2
    abstain_gold = abstain and rng.random() < 0.4
    lead = cand[:k] + ([] if abstain_gold else [fmt_num(gold)])
    rng.shuffle(lead)
    opts = lead + (["None of these"] if abstain else [])
    g = "None of these" if abstain_gold else fmt_num(gold)
    wid = rng.choice(sorted(W_CH))
    cid = pick_card(rng, "choice")
    return row_obj(fr, pid, qa, state, "choice", W_CH[wid], opts, g, cid, wid,
                   dict(common, abstain_shown=abstain, gold_is_abstain=abstain_gold, k=len(opts)))


def row_obj(fr, pid, qa, state, qtype, instr, options, gold, cid, wid, extra):
    return {
        "id": stable_id("pub_drop_", fr, qa["query_id"]),
        "group_id": "g:pub:drop:" + pid,
        "call_id": stable_id("c_pub_drop_", fr, qa["query_id"]),
        "source": SOURCE,
        "state": state,
        "qtype": qtype,
        "instructions": instr,
        "options": options,
        "gold": gold,
        "role": "aff" if qtype == "noul" else "choice",
        "card": CARDS[cid]["text"] if cid else None,
        "meta": {},
        "_x": dict(framing=fr, card_id=cid, wording_id=wid, container="prose", **extra),
    }


if __name__ == "__main__":
    print(build({"drop_thr_yn": 140, "drop_ch": 110}, {"drop_thr_yn": 15, "drop_ch": 15}, TMP / "cand_drop.jsonl"))
