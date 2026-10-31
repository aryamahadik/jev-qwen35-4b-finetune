"""v14 golden, family fact_tables: raw rows for "finqa" (FinQA, Chen et al., EMNLP 2021) as yes/no answer verification.

Source : GitHub czyssrs/FinQA @ 0f16e2867befa6840783e58be38c9efb9229d742, dataset/train.json ONLY (dev/test/private
         test are never downloaded). sha256 pinned below; snapshot in cache/finqa/.
Licence: MIT (LICENSE at the repo root, "Copyright (c) 2021 Zhiyu Chen"; the repo holds the dataset).
Texts  : S&P 500 earnings-report pages (FinTabNet): text before the table, the table, text after it. Questions, the
         reasoning program and the answer were written by financial experts (no model-written text or labels).
Rows   : state = report text + table + question + a proposed answer; the proposed answer is either the human answer
         (gold "yes" for "correct?") or a wrong answer computed by re-running the expert's own program with one
         realistic slip (gold "no"): another table cell of the same row (other year) or column (other line item) or
         another number from the same evidence sentence swapped in, percent change on the wrong base, sum instead of
         average, sign flip of a plain "change", or the opposite answer to a yes/no comparison. Candidates must be
         clearly different at the precision of the human answer and are rendered in exactly the human answer's format.
         ~20% of rows ask the negated question "... is the proposed answer wrong?" (gold flips; edge=negation).
Filters: numeric/yes-no answers only; the human answer must equal the executed program (within its rounding);
         long pages keep every expert evidence sentence (gold_inds) with 2 neighbours on each side and mark cuts
         with "[...]"; at most 3 questions per page; exact/near-dup states dropped; 13-word-run decontamination of
         page text and questions against our local non-held-out files. yes/no balanced per program shape.
         Reviewer fixes (strict review): "change" questions whose years run backwards ("between 2013 and 2012") are
         dropped (sign ambiguous); sign flips only when the question years are chronological and the dated operand
         columns of the first subtract() give later minus earlier.
Deterministic, CPU only (seed 20261101).   ../../../.venv/bin/python build_finqa.py [--manifest]
"""
import json
import random
import re
import sys
from collections import Counter, defaultdict

import ft_common as C

KEY = "finqa"
COMMIT = "0f16e2867befa6840783e58be38c9efb9229d742"
BASE = f"https://raw.githubusercontent.com/czyssrs/FinQA/{COMMIT}/"
FILES = {
    "dataset/train.json": "49f237eb9779b569473b26b08048867d04635a7cc39ad6a7a5664c55bb428db6",
    "LICENSE": "92c0e67bd762c15c07ba60de09558338315a8ebf99aac4f51f487179809ac087",
}
LICENCE = f"MIT (github.com/czyssrs/FinQA/blob/{COMMIT}/LICENSE, 'Copyright (c) 2021 Zhiyu Chen'; repo holds the dataset)"
CACHE = C.CACHE / "finqa"
MAX_PER_PAGE = 3
NEG_SHARE = 0.2
MAX_STATE = 6500
WINDOW = 2

Q_CORRECT = "Based only on the filing excerpt and its table, is the proposed answer to the question correct?"
Q_WRONG = "Based only on the filing excerpt and its table, is the proposed answer to the question wrong?"
DEFS = {
    "correct": {
        "yes": "The proposed answer equals what the excerpt and table give for this exact question, computed from the "
               "right figures (right year, right line item, right base), with the same sign and matching the value at "
               "the precision shown.",
        "no": "The proposed answer does not equal the correct result: it uses a wrong figure (another year, line item or "
              "number), the wrong base for a percentage change, a sum instead of an average, the wrong sign, or the "
              "opposite yes/no conclusion.",
    },
    "wrong": {
        "yes": "It is wrong: the proposed answer differs from the correct result for this question, for example a wrong "
               "figure (another year, line item or number), the wrong base for a percentage change, a sum instead of an "
               "average, the wrong sign, or the opposite yes/no conclusion.",
        "no": "It is not wrong: the proposed answer equals what the excerpt and table give for this exact question, "
              "from the right figures and base, with the same sign and matching the value at the precision shown.",
    },
}
ANS_RE = re.compile(r"^(?P<pre>\$\s?)?(?P<num>-?\d*\.?\d+)(?P<suf>%| million| billion| thousand)?$")
CHANGE_BLOCK = re.compile(r"difference|decrease|increase|decline|growth|grow|rise|fall|drop|reduc|gain|loss", re.I)
OPEN_Q = re.compile(r"\b(an example|one of|such as|examples?)\b", re.I)
YEAR_TOK = re.compile(r"(?<!\d)(19[5-9]\d|20[0-4]\d)(?!\d)")


def reversed_change(question):
    """'change ... between 2013 and 2012': the sign of the change is ambiguous (literal reading vs. the experts'
    later-minus-earlier convention), so such questions are dropped (reviewer fix)."""
    if not re.search(r"\bchange\b", question, re.I):
        return False
    ys = [int(y) for y in YEAR_TOK.findall(question)]
    return len(ys) >= 2 and ys[0] > ys[1]


def sign_flip_ok(question, steps, table):
    """Sign flip is a safe distractor only when the question years (if any) are chronological and, when both
    operands of the first subtract() are table cells under dated columns, the program is later minus earlier."""
    ys = [int(y) for y in YEAR_TOK.findall(question)]
    if len(ys) >= 2 and ys[0] >= ys[1]:
        return False
    sub = next((args for op, args in steps if op == "subtract"), None)
    if sub and all(k == "num" for k, _ in sub):
        years = []
        for _, v in sub:
            y = None
            for r in range(1, len(table)):
                for c in range(1, len(table[r])):
                    x = C.parse_num(table[r][c])
                    if x is not None and abs(abs(x) - abs(v)) < 1e-9 and c < len(table[0]):
                        m = set(YEAR_TOK.findall(table[0][c]))
                        y = int(m.pop()) if len(m) == 1 else None
                        break
                if y is not None:
                    break
            years.append(y)
        if None not in years and years[0] < years[1]:
            return False
    return True


def detok(s):
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r" ([.,;:!?%])", r"\1", s)
    s = re.sub(r"\( ", "(", s)
    s = re.sub(r" \)", ")", s)
    s = re.sub(r"\$ (?=[-\d.(])", "$", s)
    s = re.sub(r" (n't|'s|'re|'ve|'ll|'d)\b", r"\1", s)
    return s


def parse_arg(a):
    a = a.strip()
    if a.startswith("#"):
        return ("ref", int(a[1:]))
    if a.startswith("const_"):
        v = a[6:]
        return ("const", -1.0 if v == "m1" else float(v))
    x = C.parse_num(a)
    if x is not None and re.fullmatch(r"-?\$?\d[\d,]*(\.\d+)?%?|-?\.\d+%?", a):
        return ("num", x / 100 if a.endswith("%") else x)
    return ("name", a)


def parse_program(p):
    steps = []
    for m in re.finditer(r"([a-z_]+)\(([^()]*)\)", p):
        args = [parse_arg(x) for x in m.group(2).split(",")]
        steps.append([m.group(1), args])
    if not steps or re.sub(r"[a-z_]+\([^()]*\)", "", p).replace(",", "").strip() not in ("", "EOF"):
        return None
    return steps


def table_row_values(table, name):
    for row in table[1:]:
        if row and C.norm(row[0]) == C.norm(name):
            vals = [C.parse_num(v) for v in row[1:]]
            vals = [v for v in vals if v is not None]
            return vals or None
    return None


def execute(steps, table):
    res = []
    for op, args in steps:
        vals = []
        for kind, v in args:
            if kind == "ref":
                if v >= len(res):
                    return None
                vals.append(res[v])
            elif kind in ("num", "const"):
                vals.append(v)
            else:
                vals.append(v)
        try:
            if op in ("add", "subtract", "multiply", "divide", "exp", "greater"):
                a, b = float(vals[0]), float(vals[1])
                r = {"add": lambda: a + b, "subtract": lambda: a - b, "multiply": lambda: a * b,
                     "divide": lambda: a / b, "exp": lambda: a ** b, "greater": lambda: "yes" if a > b else "no"}[op]()
            elif op.startswith("table_"):
                row = table_row_values(table, vals[0])
                if not row:
                    return None
                r = {"table_max": max, "table_min": min, "table_sum": sum,
                     "table_average": lambda x: sum(x) / len(x)}[op](row)
            else:
                return None
        except Exception:  # noqa: BLE001
            return None
        res.append(r)
    return res[-1] if res else None


def answer_shape(ans):
    m = ANS_RE.match(ans.strip())
    if not m:
        return None
    num = m.group("num")
    return {"pre": m.group("pre") or "", "suf": m.group("suf") or "", "value": float(num),
            "dec": len(num.split(".")[1]) if "." in num else 0, "bare_point": num.lstrip("-").startswith(".")}


def render(v, shape):
    s = C.fmt_num(v, shape["dec"], commas=False)
    if shape["bare_point"]:
        s = re.sub(r"^(-?)0\.", r"\1.", s)
    return shape["pre"] + s + shape["suf"]


def number_cells(table):
    out = []
    for r, row in enumerate(table):
        for c, v in enumerate(row):
            x = C.parse_num(v)
            if x is not None and c > 0 and r > 0 and re.fullmatch(r"\$?\s?-?\d[\d,]*(\.\d+)?%?", v.strip()):
                out.append((x, r, c))
    return out


def alternatives(table, r, c):
    def label(rr):
        return C.norm(table[rr][0]) if table[rr] else ""

    def header(cc):
        return C.norm(table[0][cc]) if cc < len(table[0]) else ""

    out = []
    for cc, v in enumerate(table[r]):
        if cc != c and cc > 0 and header(cc) and header(cc) != header(c):
            x = C.parse_num(v)
            if x is not None and re.fullmatch(r"\$?\s?-?\d[\d,]*(\.\d+)?%?", v.strip()):
                out.append(("same_row", x))
    for rr in range(1, len(table)):
        if rr != r and c < len(table[rr]) and label(rr) and label(rr) != label(r):
            v = table[rr][c]
            x = C.parse_num(v)
            if x is not None and re.fullmatch(r"\$?\s?-?\d[\d,]*(\.\d+)?%?", v.strip()):
                out.append(("same_col", x))
    return out


def distractors(qa, steps, table, gold_text_sents, shape, factor):
    gv = shape["value"]
    out = []
    consts = [(i, j, v) for i, (op, args) in enumerate(steps) for j, (k, v) in enumerate(args) if k == "num"]
    all_vals = {abs(v) for _, _, v in consts}
    cells = number_cells(table)

    def run_with(i, j, newv):
        st = [[op, list(args)] for op, args in steps]
        st[i][1][j] = ("num", newv)
        return execute(st, table)

    def add(val, kind):
        if isinstance(val, str) or val is None:
            return
        val = val * factor
        if C.clearly_different(val, gv, shape["dec"]):
            out.append((render(val, shape), kind))

    for i, j, v in consts:
        locs = [(r, c) for (x, r, c) in cells if abs(abs(x) - abs(v)) < 1e-9]
        if locs:
            r, c = locs[0]
            for kind, x in alternatives(table, r, c):
                if abs(x) in all_vals or abs(abs(x) - abs(v)) < 1e-9:
                    continue
                add(run_with(i, j, abs(x) if v >= 0 else -abs(x)), "operand_" + kind)
        else:
            for sent in gold_text_sents:
                nums = [C.parse_num(m.group(0)) for m in C.NUM_RE.finditer(sent)]
                if not any(n is not None and abs(abs(n) - abs(v)) < 1e-9 for n in nums):
                    continue
                for n in nums:
                    if n is None or abs(n) in all_vals or v == 0 or not (0.2 <= abs(n) / abs(v) <= 5):
                        continue
                    if (1900 <= abs(n) <= 2100) != (1900 <= abs(v) <= 2100):
                        continue
                    add(run_with(i, j, abs(n) if v >= 0 else -abs(n)), "operand_text")
    # wrong base: subtract(a, b) ... divide(#k, b) -> divide(#k, a)
    for k, (op, args) in enumerate(steps):
        if op == "subtract" and all(a[0] == "num" for a in args):
            for i2, (op2, args2) in enumerate(steps):
                if op2 == "divide" and args2[0] == ("ref", k) and args2[1][0] == "num" \
                        and abs(args2[1][1] - args[1][1]) < 1e-9:
                    st = [[o, list(a)] for o, a in steps]
                    st[i2][1][1] = ("num", args[0][1])
                    add(execute(st, table), "wrong_base")
    # sum instead of average: table_average -> table_sum ; divide(#k add-chain, const n) -> #k
    for i, (op, args) in enumerate(steps):
        if op == "table_average" and i == len(steps) - 1:
            st = [[o, list(a)] for o, a in steps]
            st[i][0] = "table_sum"
            add(execute(st, table), "sum_not_average")
        if op == "divide" and i == len(steps) - 1 and args[0][0] == "ref" and steps[args[0][1]][0] == "add" \
                and args[1][0] == "num" and args[1][1] in (2.0, 3.0, 4.0, 5.0):
            add(execute(steps[:args[0][1] + 1], table), "sum_not_average")
    # sign flip of a plain "change"
    q = qa["question"]
    if re.search(r"\bchange\b", q, re.I) and not CHANGE_BLOCK.search(q) and gv != 0 and sign_flip_ok(q, steps, table):
        if C.clearly_different(-gv, gv, shape["dec"]):
            out.append((render(-gv, shape), "sign_flip"))
    return out


def trim_text(sents, keep_idx):
    """Keep sentences in keep_idx (+-WINDOW); '[...]' marks every cut."""
    keep = set()
    for i in keep_idx:
        keep |= set(range(max(0, i - WINDOW), min(len(sents), i + WINDOW + 1)))
    out, last = [], -1
    for i, s in enumerate(sents):
        if i in keep:
            if i != last + 1:
                out.append("[...]")
            out.append(s)
            last = i
    if last != len(sents) - 1 and sents:
        out.append("[...]")
    return out


def main():
    paths = {rel: C.fetch(BASE + rel, CACHE / rel.split("/")[-1], sha) for rel, sha in FILES.items()}
    data = json.load(open(paths["dataset/train.json"]))  # TRAIN ONLY
    rng = random.Random(C.SEED)
    drop = Counter()
    cands = []
    for r in data:
        qa = r["qa"]
        ans = str(qa.get("answer", "")).replace("\\n", "").strip()
        table = [[detok(v) for v in row] for row in r["table"]]
        if len(table) < 2:
            drop["no table"] += 1
            continue
        steps = parse_program(qa.get("program", ""))
        if steps is None:
            drop["unparsable program"] += 1
            continue
        if reversed_change(qa["question"]):
            drop["change question with reversed years (sign ambiguous)"] += 1
            continue
        ex = execute(steps, table)
        if ans in ("yes", "no"):
            if ex != ans:
                drop["inconsistent human answer"] += 1
                continue
            shape, factor = None, 1.0
        else:
            shape = answer_shape(ans)
            if shape is None or ex is None or isinstance(ex, str):
                drop["non-numeric or unexecutable answer"] += 1
                continue
            gv, tol = shape["value"], max(0.5 * 10 ** (-shape["dec"]) + 1e-9, 0.005 * abs(shape["value"]))
            if abs(ex - gv) <= tol:
                factor = 1.0
            elif shape["suf"] == "%" and abs(ex * 100 - gv) <= tol:
                factor = 100.0
            else:
                drop["inconsistent human answer"] += 1
                continue
        pre = [detok(s) for s in r["pre_text"]]
        post = [detok(s) for s in r["post_text"]]
        gold = qa.get("gold_inds", {})
        gold_text_idx = sorted(int(k.split("_")[1]) for k in gold if k.startswith("text_"))
        allsents = pre + post
        gold_sents = [allsents[i] for i in gold_text_idx if i < len(allsents)]
        table_txt = C.render_table(table)
        full = "\n".join(pre) + "\n" + table_txt + "\n" + "\n".join(post)
        if len(full) + len(qa["question"]) + 200 > MAX_STATE:
            pre_k = trim_text(pre, [i for i in gold_text_idx if i < len(pre)])
            post_k = trim_text(post, [i - len(pre) for i in gold_text_idx if i >= len(pre)])
            trimmed = True
        else:
            pre_k, post_k, trimmed = pre, post, False
        if shape is None:
            dis = [("no" if ans == "yes" else "yes", "yesno_flip")]
            gold_txt = ans
        else:
            gold_txt = ans
            dis = distractors(qa, steps, table, gold_sents, shape, factor)
            dis = [d for d in dis if d[0].strip() != gold_txt]
        if OPEN_Q.search(qa["question"]):
            dis = []
        shape_key = "yes/no comparison" if shape is None else "+".join(o for o, _ in steps)
        if shape is not None and len(steps) > 2:
            shape_key = "3+ steps"
        cands.append({"rid": r["id"], "page": r["filename"], "question": detok(qa["question"]), "gold_txt": gold_txt,
                      "dis": sorted(set(dis)), "pre": pre_k, "post": post_k, "table_txt": table_txt,
                      "trimmed": trimmed, "stratum": shape_key, "program": qa["program"], "answer": ans,
                      "from_table": any(k.startswith("table_") for k in gold),
                      "from_text": any(k.startswith("text_") for k in gold)})

    docs = {}
    for cd in cands:
        docs["p:" + cd["rid"]] = "\n".join(cd["pre"]) + "\n" + cd["table_txt"] + "\n" + "\n".join(cd["post"])
        docs["q:" + cd["rid"]] = cd["question"]
    hit = C.local_decontam(docs)
    n0 = len(cands)
    cands = [cd for cd in cands if "p:" + cd["rid"] not in hit and "q:" + cd["rid"] not in hit]
    drop["13-gram overlap"] = n0 - len(cands)

    by_page = defaultdict(list)
    for cd in cands:
        by_page[cd["page"]].append(cd)
    pool = []
    for page in sorted(by_page):
        lst = sorted(by_page[page], key=lambda c: c["rid"])
        rng.shuffle(lst)
        lst.sort(key=lambda c: not c["dis"])
        seen_q, chosen = set(), []
        for cd in lst:
            nq = C.norm(cd["question"])
            if nq in seen_q:
                continue
            seen_q.add(nq)
            chosen.append(cd)
            if len(chosen) >= MAX_PER_PAGE:
                break
        drop["over per-page cap / dup question"] += len(lst) - len(chosen)
        pool += chosen

    by_st = defaultdict(list)
    for cd in pool:
        by_st[cd["stratum"]].append(cd)
    rows = []
    for st in sorted(by_st):
        lst = by_st[st]
        rng.shuffle(lst)
        can_no = [cd for cd in lst if cd["dis"]]
        k = min(len(can_no), len(lst) // 2)
        no_ids = {cd["rid"] for cd in can_no[:k]}
        yes = [cd for cd in lst if cd["rid"] not in no_ids][:k]
        drop["stratum balance"] += len(lst) - 2 * k
        for cd in can_no[:k]:
            kinds = sorted({d[1] for d in cd["dis"]})
            kind = rng.choice(kinds)
            rows.append((cd, rng.choice(sorted(d[0] for d in cd["dis"] if d[1] == kind)), False, kind))
        for cd in yes:
            rows.append((cd, cd["gold_txt"], True, "human_gold"))

    rows.sort(key=lambda x: x[0]["rid"])
    rng.shuffle(rows)
    n_neg = int(round(NEG_SHARE * len(rows)))
    out, seen = [], set()
    for i, (cd, ans_txt, is_gold, kind) in enumerate(rows):
        negq = i < n_neg
        parts = ["Company filing excerpt"]
        if cd["pre"]:
            parts.append("Text before the table:\n" + "\n".join(cd["pre"]))
        parts.append("Table:\n" + cd["table_txt"])
        if cd["post"]:
            parts.append("Text after the table:\n" + "\n".join(cd["post"]))
        state = "\n".join(parts) + f"\n\nQuestion: {cd['question']}\nProposed answer: {ans_txt}"
        if len(state) > MAX_STATE + 1500:
            drop["state too long"] += 1
            continue
        ns = C.norm(state)
        if ns in seen:
            drop["duplicate state"] += 1
            continue
        seen.add(ns)
        gold = ("yes" if not is_gold else "no") if negq else ("yes" if is_gold else "no")
        edges = []
        if negq:
            edges.append("negation")
        if cd["from_table"] and cd["from_text"]:
            edges.append("multi_hop")
        if cd["stratum"] != "yes/no comparison":
            edges.append("numeric")
        if len(state) > 3500:
            edges.append("long_context")
        if cd["from_table"]:
            edges.append("table")
        prio = ["negation", "multi_hop", "numeric", "long_context", "table"]
        edge = next((e for e in prio if e in edges), None)
        out.append({
            "key": KEY, "rid": cd["rid"], "state": state, "instructions": Q_WRONG if negq else Q_CORRECT,
            "options": ["yes", "no"], "gold": gold, "soft": None,
            "meta": {"dataset": "czyssrs/FinQA (github)", "config": "dataset/train.json",
                     "revision": f"git:{COMMIT}; sha256:{FILES['dataset/train.json']}", "licence": LICENCE,
                     "split": "train", "orig_label": {"answer": cd["answer"], "program": cd["program"]},
                     "family": C.FAMILY, "edge": edge, "edge_all": edges, "defs": "wrong" if negq else "correct",
                     "proposed_is_gold": is_gold, "distractor": kind, "context_id": cd["page"],
                     "trimmed_context": cd["trimmed"]},
        })

    summ = C.check_rows(KEY, out)
    print("drops:", dict(drop))
    print("distractor kinds:", dict(Counter(r["meta"]["distractor"] for r in out)))
    print("strata:", dict(Counter(r["meta"]["orig_label"]["program"].count("(") for r in out)))
    C.write_outputs(KEY, out, DEFS)
    if "--manifest" in sys.argv:
        C.append_manifest({
            "key": KEY, "family": C.FAMILY, "dataset": "czyssrs/FinQA (train)", "licence": LICENCE,
            "rows": summ["rows"], "qtype": "yesno", "yesno_share": round(summ["yesno_share"], 4),
            "edge_tags": summ["edge_tags"],
            "notes": ("Answer verification on earnings-report pages (text+table). Yes rows = expert answer (checked "
                      "against the executed expert program); no rows = the expert program re-run with one realistic "
                      "slip (other year/line item/number, wrong base, sum vs average, sign flip, flipped comparison). "
                      "20% negated question. <=3 questions/page; balanced per program shape; 13-gram decontam."),
        })


if __name__ == "__main__":
    main()
