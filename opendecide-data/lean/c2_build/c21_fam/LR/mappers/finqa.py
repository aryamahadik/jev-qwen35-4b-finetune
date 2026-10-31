"""LR-44 FinQA mapper (family LR-tables, long document). Recast table below (Opus approves, G-R6 batch).

Own label: the answer the 11 finance professionals wrote (`qa.answer`), checked against the executed value of their own gold
program (`qa.exe_ans`). Recast: 4-way pick-one over the report excerpt: the gold answer plus THREE near-miss answers made by PROGRAM
from the dataset's own gold program (LR-B4): (a) the last operation swapped (add <-> subtract, multiply <-> divide), (b) the last
step's operands swapped, (c) one numeric operand replaced by another number from the same report; each is re-executed by this
file's evaluator and formatted like the gold (same decimals, % if the gold is a %, same sign / rounding convention).
The annotators' answer strings do not always equal their own executed value (truncation instead of rounding, an absolute value, a %
already in percent units, or plain errors such as 56.25% for a program that executes to 97.66%): the answer must be reproduced by the
program under one of 8 declared conventions (scale 100 or 1 for a % answer; signed or absolute; rounded or truncated), or the item is
dropped and logged (`answer_not_reproduced_by_program`); the near-misses then use the SAME convention. A near-miss that equals the gold after rounding
is not used. The excerpt is built by PROGRAM span selection from the SAME report (LR-B10): every human-annotated supporting fact
(`gold_inds`: text sentences and table rows) + the table header + seeded random other sentences / rows until the token budget is
used, in report order; a report whose supporting facts alone exceed the budget is dropped and logged. Programs with table_* or
greater operations and non-numeric answers are dropped and logged. NEVER touched: dev, test, private_test (quarantine).
"""
import gzip
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import lr_common as lc  # noqa: E402

DATASET = "finqa"
FORM = "lr_finqa_numeric_pick"
FORMS = {FORM: "Which value answers the question, based on the report excerpt?"}
BUDGET_TOKENS = 600
K = 4
RECAST_TABLE = {
    "dataset_id": "FinQA (czyssrs/FinQA) dataset/train.json", "train_file": "train.json.gz",
    "split_field": "file name (dev, test, private_test quarantined)", "source_label_set": ["qa.answer (numeric, optionally %)"],
    "recast_option_set": "gold + 3 program-made near-miss answers (re-executed, same format), shuffled", "target_format": "Choice 4",
    "mapping": {"qa.answer": "gold option"}, "distractor_policy": "operation swap / operand swap / operand replaced from the same report (LR-B4: no distractor equal to the gold after rounding)",
    "declared_balancing": "round-robin over the program's operation signature; gold position balanced",
    "declared_drops": ["table_* or greater operation", "non-numeric answer", "program disagrees with exe_ans", "answer not reproduced by the program under the 8 conventions", "no gold_inds", "gold_inds index out of range",
                       "supporting facts exceed the token budget", "fewer than 3 distinct near-misses", "R12 guards"],
    "question_form_ids": [FORM], "span_selection_rule": "all gold_inds facts + table header + seeded random spans of the same report to 600 tokens (lc.select_spans)",
    "expected_token_mean": 760,
}
META = {"dataset": DATASET, "lr_id": "LR-44", "family": "LR-tables", "tier": "C", "cap": 300, "share_alike": False,
        "p1_realism": False, "recast_table": RECAST_TABLE}
_CALL = re.compile(r"(\w+)\(([^()]*)\)")
_NUM = re.compile(r"-?\d[\d,]*\.?\d*")
_BIN = {"add": lambda a, b: a + b, "subtract": lambda a, b: a - b, "multiply": lambda a, b: a * b,
        "divide": lambda a, b: a / b, "exp": lambda a, b: a ** b}
_SWAP_OP = {"add": "subtract", "subtract": "add", "multiply": "divide", "divide": "multiply"}


def read_train(train_dir=None):
    d = lc.guard_train_path(train_dir or lc.raw_train_dir(DATASET))
    with gzip.open(os.path.join(d, "train.json.gz"), "rt", encoding="utf-8") as f:
        for r in json.load(f):
            r["_src_line"] = "finqa:" + r["id"]
            yield r


def parse_program(prog):
    steps = [(m.group(1), [a.strip() for a in m.group(2).split(",")]) for m in _CALL.finditer(prog or "")]
    return steps


def _val(tok, results):
    if tok.startswith("#"):
        return results[int(tok[1:])]
    if tok.startswith("const_"):
        c = tok[6:]
        return -float(c[1:]) if c.startswith("m") else float(c)
    t = tok.replace(",", "")
    if t.endswith("%"):
        return float(t[:-1]) / 100.0
    return float(t)


def run_program(steps):
    """Execute the binary-op program; returns the final float or raises ValueError for anything unsupported."""
    res = []
    for op, args in steps:
        if op not in _BIN or len(args) != 2:
            raise ValueError("unsupported op %s" % op)
        a, b = _val(args[0], res), _val(args[1], res)
        try:
            v = _BIN[op](a, b)
        except (ZeroDivisionError, OverflowError):
            raise ValueError("arith")
        if isinstance(v, complex) or math.isnan(v) or math.isinf(v):
            raise ValueError("arith")
        res.append(v)
    if not res:
        raise ValueError("empty")
    return res[-1]


def answer_style(ans):
    """(is_percent, decimals, has_commas) of a numeric answer string, else None."""
    t = lc.normalise_ws(ans)
    m = re.match(r"^-?[\d,]*\.?(\d*)(%?)$", t)
    if not m or not re.search(r"\d", t):
        return None
    return (m.group(2) == "%", len(m.group(1)), "," in t)


def _quant(x, dec, mode):
    f = 10 ** dec
    if mode == "trunc":
        return math.trunc(x * f) / f
    return math.floor(abs(x) * f + 0.5) / f * (1 if x >= 0 else -1)


def fmt(value, style, conv=None):
    """Format `value` like an answer of `style`; conv = (scale, absflag, mode); default = fraction*100 for %, signed, rounded."""
    pct, dec, commas = style
    scale, absflag, mode = conv or ((100.0 if pct else 1.0), False, "round")
    v = value * scale
    if absflag:
        v = abs(v)
    v = _quant(v, dec, mode)
    s = ("{:,.%df}" if commas else "{:.%df}") % dec
    s = s.format(v)
    if s.startswith("-") and float(s.replace(",", "")) == 0:
        s = s[1:]
    return s + ("%" if pct else "")


def conventions(style):
    pct = style[0]
    return [(sc, ab, md) for sc in ((100.0, 1.0) if pct else (1.0,)) for ab in (False, True) for md in ("round", "trunc")]


def match_convention(answer, value):
    """The first declared convention under which `value` reproduces the answer string, else None."""
    style = answer_style(answer)
    if style is None:
        return None
    want = lc.normalise_ws(answer)
    for conv in conventions(style):
        if fmt(value, style, conv) == want:
            return conv
    return None


def render_row(cells):
    return " | ".join(lc.normalise_ws(c) for c in cells)


def evidence_spans(src):
    pre, post, table = src.get("pre_text") or [], src.get("post_text") or [], src.get("table") or []
    spans, kinds = [], []
    for s in pre:
        spans.append(lc.normalise_ws(s)); kinds.append(("pre", s))
    for i, row in enumerate(table):
        spans.append(render_row(row)); kinds.append(("row", i))
    for s in post:
        spans.append(lc.normalise_ws(s)); kinds.append(("post", s))
    return spans, kinds


def gold_indices(src, spans, kinds):
    gi = (src.get("qa") or {}).get("gold_inds") or {}
    idx = set()
    sent_pos = {}
    for k, (kind, ref) in enumerate(kinds):
        if kind in ("pre", "post"):
            sent_pos.setdefault(lc.normalise_ws(ref), []).append(k)
    for key, val in gi.items():
        if key.startswith("table_"):
            try:
                i = int(key.split("_", 1)[1])
            except ValueError:
                return None
            tgt = [k for k, (kind, ref) in enumerate(kinds) if kind == "row" and ref == i]
            if not tgt:
                return None
            idx.add(tgt[0])
        elif key.startswith("text_"):
            # the value is the sentence itself: locate it in pre/post text
            hit = sent_pos.get(lc.normalise_ws(val))
            if not hit:
                return None
            idx.add(hit[0])
        else:
            return None
    return sorted(idx)


def near_misses(steps, style, gold_value, evidence_numbers, seed_key):
    """Candidate wrong values (floats) made by program from the gold program; formatted + de-duplicated by the caller."""
    cands = []
    last_i = len(steps) - 1
    op, args = steps[last_i]
    if op in _SWAP_OP:
        cands.append(("op_swap", steps[:last_i] + [(_SWAP_OP[op], args)]))
    if op in ("subtract", "divide", "exp"):
        cands.append(("operand_swap", steps[:last_i] + [(op, [args[1], args[0]])]))
    # operand replaced: numeric literal args only (not #k, not const_); the replacement is a number of the SAME report in the same
    # magnitude band (within 10x of the operand it replaces), nearest in log-magnitude first, so a wrong answer stays plausible
    lits = [(i, j) for i, (o, a) in enumerate(steps) for j, t in enumerate(a) if not t.startswith("#") and not t.startswith("const_")]
    pool = sorted(evidence_numbers)
    for i, j in lits:
        try:
            orig = abs(float(steps[i][1][j].replace(",", "").rstrip("%")))
        except ValueError:
            continue
        if orig == 0:
            continue

        def band(n):
            try:
                x = abs(float(n))
            except ValueError:
                return None
            return abs(math.log10(x / orig)) if x > 0 and x != orig and 0.1 <= x / orig <= 10 else None
        near = sorted((b, lc.stable_hash("finqa-op", seed_key, i, j, n), n) for n in pool for b in [band(n)] if b is not None)
        for _, _, n in near[:4]:
            new = [(o, list(a)) for o, a in steps]
            new[i][1][j] = n
            cands.append(("operand_replace", new))
    out = []
    for name, st in cands:
        try:
            v = run_program(st)
        except (ValueError, IndexError):
            continue
        if gold_value != 0 and v != 0 and not (1e-3 <= abs(v / gold_value) <= 1e3):
            continue                       # an absurd magnitude is not a near-miss
        if v == 0 and gold_value != 0:
            continue
        out.append(v)
    return out


class Mapper(lc.BaseMapper):
    META = META
    FORMS = FORMS

    def build(self, src, ctx):
        sid = src["_src_line"]
        qa = src.get("qa") or {}
        style = answer_style(qa.get("answer", ""))
        if style is None:
            self.drops.add("non_numeric_answer", sid)
            return []
        steps = parse_program(qa.get("program"))
        if not steps or any(op not in _BIN for op, _ in steps):
            self.drops.add("unsupported_program_op", sid)
            return []
        try:
            val = run_program(steps)
        except (ValueError, IndexError, KeyError):
            self.drops.add("program_not_executable", sid)
            return []
        exe = qa.get("exe_ans")
        gold_text = lc.normalise_ws(qa["answer"])
        if not isinstance(exe, (int, float)) or abs(exe - val) > 1e-4 * max(1.0, abs(exe)):
            self.drops.add("program_disagrees_with_exe_ans", sid)
            return []
        conv = match_convention(gold_text, val)
        if conv is None:
            self.drops.add("answer_not_reproduced_by_program", sid)
            return []
        spans, kinds = evidence_spans(src)
        gidx = gold_indices(src, spans, kinds)
        if gidx is None:
            self.drops.add("gold_ind_out_of_range_or_unmatched", sid)
            return []
        if not gidx:
            self.drops.add("no_gold_inds", sid)
            return []
        if any(kinds[k][0] == "row" for k in gidx):
            hdr = [k for k, (kind, ref) in enumerate(kinds) if kind == "row" and ref == 0]
            gidx = sorted(set(gidx) | set(hdr))
        chosen, info = lc.select_spans(spans, gidx, BUDGET_TOKENS, key="%s|%s" % (sid, self.seed))
        if chosen is None:
            self.drops.add("supporting_facts_exceed_budget", sid)
            return []
        text_nums = set()
        for s in spans:
            for m in _NUM.findall(s):
                t = m.replace(",", "").rstrip(".")
                if t and t not in ("-",):
                    text_nums.add(t)
        gold_fmt = fmt(val, style, conv)
        wrong = []
        for v in near_misses(steps, style, val, text_nums, sid + str(self.seed)):
            s = fmt(v, style, conv)
            if s != gold_fmt and s != gold_text and s not in wrong:
                wrong.append(s)
        if len(wrong) < K - 1:
            self.drops.add("fewer_than_3_near_misses", sid)
            return []
        wrong = sorted(wrong, key=lambda s: lc.stable_hash("finqa-pick", self.seed, sid, s))[:K - 1]
        body = "\n".join(spans[k] for k in chosen)
        context = "Report excerpt:\n%s\n\nQuestion: %s" % (body, lc.normalise_ws(qa["question"]))
        return [{"form": FORM, "kind": "choice", "context": context, "options": [gold_text] + wrong, "gold_text": gold_text,
                 "source_row_id": sid, "extra": {"signature": "-".join(op for op, _ in steps), "span_info": info}}]

    def independent_gold(self, src, cand):
        # independent route: does the dataset's own EXECUTED value `exe_ans` (not this file's evaluator) reproduce its answer string?
        qa = src["qa"]
        return lc.normalise_ws(qa["answer"]) if match_convention(qa["answer"], qa["exe_ans"]) is not None else None

    def map_records(self, records, ctx=None, cap=None, select_key=None):
        cap = cap if cap is not None else META["cap"]
        groups, seen = {}, set()
        for src in records:
            k = (src["id"], lc.normalise_ws((src.get("qa") or {}).get("question")).lower())
            if k in seen:
                self.drops.add("duplicate_item", src.get("_src_line"))
                continue
            seen.add(k)
            sig = "-".join(op for op, _ in parse_program((src.get("qa") or {}).get("program"))) or "?"
            groups.setdefault(sig, []).append((src,))

        def make(item):
            out = []
            for cand in self.build(item[0], {}):
                r = self.finish_candidate(item[0], cand)
                if r:
                    out.append(r)
            return out
        return lc.round_robin_take(groups, "finqa%s" % self.seed, cap, make)
