"""v14 golden, family fact_tables: raw rows for "tatqa" (TAT-QA, Zhu et al., ACL 2021) as yes/no answer verification.

Source : GitHub NExTplusplus/TAT-QA @ 870accc41953dcde885aabeb963d94aabdc0fbc3, dataset_raw/tatqa_dataset_train.json
         ONLY (dev/test are never downloaded). sha256 pinned below; snapshot in cache/tatqa/.
Licence: CC BY 4.0, stated in the repo README.md section "### License" ("The TAT-QA dataset is under the license of
         Creative Commons (CC BY) Attribution 4.0 International"); code is MIT (LICENSE).
Texts  : real annual reports (tables + paragraphs). Questions, answers, derivations, answer type, scale were written
         by human finance-literate annotators (no model-written text or labels).
Rows   : state = table + paragraphs + question + a proposed answer. The proposed answer is either the human gold answer
         (gold "yes" for the "correct?" question) or a program-built wrong answer whose wrongness follows by
         construction from the human gold (gold "no"):
           arithmetic: another cell swapped into the human derivation (wrong year / wrong line item), percent change on
                       the wrong base, sum instead of average (dropped final division), sign flip of a "change",
                       or the right number with the wrong scale (thousand vs million) when the report states the gold
                       scale and never mentions the wrong one;
           span      : another cell of the same row/column, another number from the report in the gold phrase, or the
                       gold answer of a different, unrelated question on the same report;
           multi-span: one item swapped for another cell of the same column/row, or one item dropped (incomplete);
           count     : gold +- 1.
         Every candidate must be clearly different from the gold at the gold's precision (ft_common.clearly_different).
         ~20% of rows ask the negated question "... is the proposed answer wrong?" (gold flips; edge=negation).
Filters: the human answer must be internally consistent (arithmetic derivation re-evaluates to the answer, count equals
         the listed items, spans occur in the table or text); at most 3 questions per report context; exact/near-dup
         states dropped; 13-word-run decontamination of contexts and questions against our local non-held-out files.
         Reviewer fixes (strict review): "change" questions whose years run backwards ("from 2019 to 2018") are dropped
         (sign ambiguous); questions whose thousand/million/billion scale is never stated in the excerpt are dropped;
         sign flips only when the question years are chronological and the dated operand columns give later minus
         earlier; year answers swap only with years, amounts with amounts; swapped text numbers lose trailing
         punctuation ("31," -> "31").
Balance: yes/no balanced inside every (answer type, answer source) stratum.
Deterministic, CPU only (seed 20261101).   ../../../.venv/bin/python build_tatqa.py [--manifest]
"""
import ast
import json
import operator as op
import random
import re
import sys
from collections import Counter, defaultdict

import ft_common as C

KEY = "tatqa"
COMMIT = "870accc41953dcde885aabeb963d94aabdc0fbc3"
BASE = f"https://raw.githubusercontent.com/NExTplusplus/TAT-QA/{COMMIT}/"
FILES = {
    "dataset_raw/tatqa_dataset_train.json": "2df6e722cdbaaa37efcbfb280f5c9a15be29a6ec18f618ef936fe63cc6d07c69",
    "README.md": "85c398173d771a2531abea5b81f3696914296642da2af78c2c34545715c14d5f",
    "LICENSE": "46e27ffbc49c3fd44a9595c2213f8a5f4319a81b53238e49ce1eec39e7e25662",
}
LICENCE = (f"CC BY 4.0 (github.com/NExTplusplus/TAT-QA/blob/{COMMIT}/README.md, section 'License': 'The TAT-QA dataset "
           "is under the license of Creative Commons (CC BY) Attribution 4.0 International'); code MIT (LICENSE)")
CACHE = C.CACHE / "tatqa"
MAX_PER_CONTEXT = 3
NEG_SHARE = 0.2
MAX_STATE = 7000

Q_CORRECT = "Based only on the report's table and text, is the proposed answer to the question correct?"
Q_WRONG = "Based only on the report's table and text, is the proposed answer to the question wrong?"
DEFS = {
    "correct": {
        "yes": "The proposed answer matches what the table and text give for this exact question: the same value at the "
               "precision shown, the same sign or direction, the same unit or scale (%, thousand, million, billion), "
               "and for list answers exactly the right items.",
        "no": "The proposed answer does not match: a different value or item (for example another year's figure or "
              "another line item), a wrong sign or wrong base for a change, a wrong unit or scale such as million "
              "instead of thousand, or a list that misses or adds an item.",
    },
    "wrong": {
        "yes": "It is wrong: the proposed answer differs from what the table and text give for this question, by value "
               "or item, sign or base of a change, unit or scale (for example million instead of thousand), or a list "
               "that misses or adds an item.",
        "no": "It is not wrong: the proposed answer matches what the table and text give for this exact question, with "
              "the same value at the precision shown, the same sign, the same unit or scale, and for lists exactly the "
              "right items.",
    },
}
SCALE_WORD = {"": "", "thousand": " thousand", "million": " million", "billion": " billion", "percent": "%"}
CUES = {
    "thousand": re.compile(r"\bthousands?\b|['’]000|\$\s?000|\(000s?\)|\b000s\b|000['’]s|\$k\b", re.I),
    "million": re.compile(r"\bmillions?\b|[$€£]\s?m\b|\bmn\b|\bin m\b|\(m\)|\$ ?mil", re.I),
    "billion": re.compile(r"\bbillions?\b|[$€£]\s?bn?\b|\bbn\b", re.I),
}
UNIT_ALT = {"thousand": ["million"], "million": ["thousand", "billion"], "billion": ["million"]}
OPS = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv, ast.USub: op.neg, ast.UAdd: op.pos}
OPEN_Q = re.compile(r"\b(what|which|who) (is|was|are|were) (a|an|one|some|any)\b|\bone of\b|\ban example\b|"
                    r"\b(name|list|give|state|mention) (a|an|one|some|any)\b|\bsome of\b|\bexamples?\b|\bsuch as\b|"
                    r"\ba (reason|factor|type|kind|component|cause|method)\b", re.I)
CHANGE_BLOCK = re.compile(r"difference|decrease|increase|decline|growth|rise|fall|drop|reduc|gain|loss", re.I)
YEAR_TOK = re.compile(r"(?<!\d)(19[5-9]\d|20[0-4]\d)(?!\d)")
YEAR_CELL = re.compile(r"^(19[5-9]\d|20[0-4]\d)$")


def reversed_change(question):
    """'change ... from 2019 to 2018' / 'between 2019 and 2018': the sign of the change is ambiguous (literal reading
    vs. the annotators' later-minus-earlier convention), so such questions are dropped (reviewer fix)."""
    if not re.search(r"\bchange\b", question, re.I):
        return False
    ys = [int(y) for y in YEAR_TOK.findall(question)]
    return len(ys) >= 2 and ys[0] > ys[1]


def col_year(table, r, c):
    """Year named in the header cells above (r, c) (first 3 rows), else None."""
    for h in range(min(3, r)):
        if c < len(table[h]):
            m = YEAR_TOK.findall(table[h][c])
            if len(set(m)) == 1:
                return int(m[0])
    return None


def later_minus_earlier(a, b, table):
    """True / False when the table columns of operands a and b name different years, else None."""
    def year_of(v):
        for r, row in enumerate(table):
            for c, cell in enumerate(row):
                x = C.parse_num(cell) if is_numeric_str(cell) else None
                if x is not None and abs(abs(x) - abs(v)) < 1e-9:
                    return col_year(table, r, c)
        return None
    ya, yb = year_of(a), year_of(b)
    if ya is None or yb is None or ya == yb:
        return None
    return ya > yb


def sign_flip_ok(question, tree, table):
    """Sign flip is a safe distractor only when the question years (if any) are chronological and, when the operand
    columns are dated, the human derivation is later minus earlier (else the flipped answer may be the right one)."""
    ys = [int(y) for y in YEAR_TOK.findall(question)]
    if len(ys) >= 2 and ys[0] >= ys[1]:
        return False
    body = tree.body if isinstance(tree, ast.Expression) else tree
    sub = body.left if isinstance(body, ast.BinOp) and isinstance(body.op, ast.Div) else body
    if isinstance(sub, ast.BinOp) and isinstance(sub.op, ast.Sub) and isinstance(sub.left, ast.Constant) \
            and isinstance(sub.right, ast.Constant):
        d = later_minus_earlier(float(sub.left.value), float(sub.right.value), table)
        if d is False:
            return False
    return True


def scale_unstated(scale, ctx_text):
    """The annotated scale (thousand / million / billion) is rendered into every proposed answer; when the excerpt
    never states it, a 'correct' answer cannot be checked (and some annotations are simply wrong, e.g. 'thousand' on
    a EUR-million table), so the question is dropped (reviewer fix)."""
    return scale in CUES and not CUES[scale].search(ctx_text)


def same_kind(a, b):
    """Year cells swap only with year cells, numbers with numbers, text with text (no '$13,346' for a year)."""
    ya, yb = bool(YEAR_CELL.match(a.strip())), bool(YEAR_CELL.match(b.strip()))
    return ya == yb and is_numeric_str(a) == is_numeric_str(b)


def light(s):
    """Sign- and symbol-preserving comparison key (C.norm drops '-' and '%')."""
    return re.sub(r"\s+", " ", s.strip().lower())


def ev(n):
    if isinstance(n, ast.Expression):
        return ev(n.body)
    if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)) and not isinstance(n.value, bool):
        return float(n.value)
    if isinstance(n, ast.BinOp) and type(n.op) in OPS:
        return OPS[type(n.op)](ev(n.left), ev(n.right))
    if isinstance(n, ast.UnaryOp) and type(n.op) in OPS:
        return OPS[type(n.op)](ev(n.operand))
    raise ValueError("bad node")


def clean_deriv(s):
    s = s.replace("−", "-").replace("×", "*").replace("÷", "/").replace("$", "")
    s = s.replace("[", "(").replace("]", ")").replace("\xa0", " ")
    s = re.sub(r"(\d[\d,]*(?:\.\d+)?)\s*%", r"(\1/100)", s)
    s = s.replace(",", "")
    return s.strip()


def parse_deriv(s):
    try:
        tree = ast.parse(clean_deriv(s), mode="eval")
        return tree, ev(tree)
    except Exception:  # noqa: BLE001
        return None, None


def gold_decimals(ans):
    if isinstance(ans, float) and ans.is_integer():
        return 0
    s = repr(ans)
    return len(s.split(".")[1]) if "." in s else 0


def cell_index(table):
    """normalised cell text -> list of (row, col); numeric cells -> list of (value, row, col)."""
    idx, nums = defaultdict(list), []
    for r, row in enumerate(table):
        for c, v in enumerate(row):
            v = C.clean_cell(v, 10_000)
            if not v:
                continue
            idx[C.norm(v)].append((r, c))
            x = C.parse_num(v)
            if x is not None and re.fullmatch(r"[-−(]?\$?\s?\d[\d,]*(\.\d+)?\)?%?", v):
                nums.append((x, r, c))
    return idx, nums


def is_numeric_str(s):
    return C.parse_num(s) is not None and re.fullmatch(r"[-−(]?\$?\s?\d[\d,]*(\.\d+)?\)?%?", s.strip()) is not None


def render_item(s, scale):
    s = C.clean_cell(s, 10_000)
    if scale and is_numeric_str(s):
        if scale == "percent":
            return s if s.endswith("%") else s + "%"
        return s + SCALE_WORD[scale]
    return s


def render_number(v, dec, scale):
    return C.fmt_num(v, dec) + SCALE_WORD[scale]


def row_col_alternatives(table, r, c, header_rows=1):
    """Other non-empty cells in the same row (not the row label column) and the same column (not header rows).
    Skips cells whose identity is ambiguous with the gold cell: same-column cells in a row with an empty label or the
    same label as the gold row, and same-row cells under an empty header or the same header as the gold column."""
    def label(rr):
        return C.norm(table[rr][0]) if table[rr] else ""

    def header(cc):
        return C.norm(" ".join(table[h][cc] for h in range(min(2, len(table))) if cc < len(table[h])))

    out = []
    gh = header(c)
    for cc, v in enumerate(table[r]):
        if cc != c and cc > 0 and C.clean_cell(v):
            hh = header(cc)
            if not hh or hh == gh:
                continue
            out.append(("same_row", r, cc, C.clean_cell(v, 10_000)))
    gl = label(r)
    for rr in range(header_rows, len(table)):
        if rr != r and c < len(table[rr]) and C.clean_cell(table[rr][c]):
            ll = label(rr)
            if c > 0 and (not ll or ll == gl):
                continue
            out.append(("same_col", rr, c, C.clean_cell(table[rr][c], 10_000)))
    return out


def number_tokens(tree):
    """Constant nodes of the derivation, in order."""
    return [n for n in ast.walk(tree) if isinstance(n, ast.Constant)]


def arithmetic_distractors(q, table, nums, ctx_text, g, dec, factor):
    scale = q["scale"]
    tree, _ = parse_deriv(q["derivation"])
    out = []

    def add(val, kind):
        val = val * factor
        if C.clearly_different(val, g, dec):
            out.append((render_number(val, dec, scale), kind, val))

    # (a) operand substitution: a derivation number that is a table cell replaced by a same-row / same-column cell
    consts = number_tokens(tree)
    for k, node in enumerate(consts):
        orig = float(node.value)
        locs = [(r, c) for (x, r, c) in nums if abs(x - orig) < 1e-9 or abs(abs(x) - abs(orig)) < 1e-9]
        if not locs:
            continue
        r, c = locs[0]
        others = {abs(float(n.value)) for j, n in enumerate(consts) if j != k}
        for kind, rr, cc, v in row_col_alternatives(table, r, c):
            x = C.parse_num(v)
            if x is None or not is_numeric_str(v) or abs(abs(x) - abs(orig)) < 1e-9:
                continue
            if abs(x) in others:
                continue  # degenerate: swapping in another operand of the same derivation (e.g. a - a = 0)
            node.value = abs(x) if orig >= 0 else -abs(x)
            try:
                add(ev(tree), "operand_" + kind)
            except Exception:  # noqa: BLE001
                pass
            node.value = orig
    # (b) percent change on the wrong base: (A - B) / B  ->  (A - B) / A
    body = tree.body
    for n in ast.walk(body):
        if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Div) and isinstance(n.left, ast.BinOp) \
                and isinstance(n.left.op, ast.Sub):
            try:
                a, b, den = ev(n.left.left), ev(n.left.right), ev(n.right)
            except Exception:  # noqa: BLE001
                continue
            if abs(den - b) < 1e-9 and abs(a) > 1e-9:
                saved = n.right
                n.right = ast.Constant(value=a)
                try:
                    add(ev(tree), "wrong_base")
                except Exception:  # noqa: BLE001
                    pass
                n.right = saved
    # (c) forgot to divide: (x + y [+ ...]) / k  ->  x + y   (average reported as a sum)
    if isinstance(body, ast.BinOp) and isinstance(body.op, ast.Div) and isinstance(body.right, ast.Constant) \
            and float(body.right.value) in {2.0, 3.0, 4.0, 5.0, 6.0} and isinstance(body.left, ast.BinOp) \
            and isinstance(body.left.op, ast.Add):
        try:
            add(ev(body.left), "sum_not_average")
        except Exception:  # noqa: BLE001
            pass
    # (d) sign flip of a plain "change" question
    if re.search(r"\bchange\b", q["question"], re.I) and not CHANGE_BLOCK.search(q["question"]) and abs(g) > 0 \
            and sign_flip_ok(q["question"], parse_deriv(q["derivation"])[0], table):
        if C.clearly_different(-g, g, dec):
            out.append((render_number(-g, dec, scale), "sign_flip", -g))
    # (e) right number, wrong scale (only when the report states the gold scale and never the wrong one)
    if scale in UNIT_ALT and CUES[scale].search(ctx_text):
        for alt in UNIT_ALT[scale]:
            if not CUES[alt].search(ctx_text):
                out.append((render_number(g, dec, alt), "wrong_scale", None))
    return out


def span_distractors(q, table, idx, ctx_text, other_text_answers):
    scale = q["scale"]
    gold = C.clean_cell(q["answer"][0], 10_000)
    gnorm = C.norm(gold)
    out = []
    locs = idx.get(gnorm, [])
    if locs and q["answer_from"] in ("table", "table-text"):
        r, c = locs[0]
        gnum = C.parse_num(gold) if is_numeric_str(gold) else None
        for kind, rr, cc, v in row_col_alternatives(table, r, c):
            vn = C.norm(v)
            if not vn or vn == gnorm or vn in gnorm or gnorm in vn:
                continue
            if gnum is not None:
                x = C.parse_num(v) if is_numeric_str(v) else None
                if x is None or not C.clearly_different(x, gnum, C.decimals_of(gold)):
                    continue
            elif is_numeric_str(v):
                continue  # keep the candidate the same kind as the gold (text for text)
            if not same_kind(gold, v):
                continue  # a year answer is never swapped for an amount (or vice versa): no giveaway distractors
            out.append((render_item(v, scale), "cell_" + kind, None))
        return out
    m = list(C.NUM_RE.finditer(gold))
    if m and q["answer_from"] in ("text", "table-text"):
        # another number from the report placed into the gold phrase
        tok = m[0].group(0).rstrip(",.")
        gnum = C.parse_num(tok)
        pool = []
        for mm in C.NUM_RE.finditer(ctx_text):
            t = mm.group(0).strip().rstrip(",.")  # "August 31, 2019" -> "31", not "31,"
            x = C.parse_num(t)
            if x is None or gnum is None or C.decimals_of(t) != C.decimals_of(tok):
                continue
            if gnum == 0 or not (0.2 <= abs(x) / abs(gnum) <= 5):
                continue  # keep the swapped number of a similar size (plausible, not a giveaway)
            if not C.clearly_different(x, gnum, C.decimals_of(tok), rel=0.05):
                continue
            if (x >= 1900 and x <= 2100) != (gnum >= 1900 and gnum <= 2100):
                continue  # do not mix years with amounts
            new = gold.replace(tok, tok.replace(tok.strip().lstrip("-−($").rstrip(")%"),
                                                 t.strip().lstrip("-−($").rstrip(")%")), 1)
            if C.norm(new) != gnorm:
                pool.append(new)
        for new in sorted(set(pool)):
            out.append((render_item(new, scale), "text_number_swap", None))
        if out:
            return out
    if q["answer_from"] == "text" and not m:
        gw = set(C.words(gold))
        qw = set(C.words(q["question"]))
        for oq, oa in other_text_answers:
            ow = set(C.words(oa))
            if not ow or not gw:
                continue
            if len(gw & ow) / len(gw | ow) >= 0.2 or C.norm(oa) in gnorm or gnorm in C.norm(oa):
                continue
            oqw = set(C.words(oq))
            if len(qw & oqw) / max(1, len(qw | oqw)) >= 0.5:
                continue
            out.append((render_item(oa, scale), "other_question_answer", None))
    return out


def multispan_distractors(q, table, idx):
    scale = q["scale"]
    items = [C.clean_cell(a, 10_000) for a in q["answer"]]
    norms = [C.norm(a) for a in items]
    out = []
    for i, it in enumerate(items):
        locs = idx.get(norms[i], [])
        if not locs:
            continue
        r, c = locs[0]
        for kind, rr, cc, v in row_col_alternatives(table, r, c):
            vn = C.norm(v)
            if not vn or any(vn == n or vn in n or n in vn for n in norms):
                continue
            if not same_kind(it, v):
                continue
            if is_numeric_str(it) and not C.clearly_different(C.parse_num(v), C.parse_num(it), C.decimals_of(it)):
                continue
            new = items[:i] + [v] + items[i + 1:]
            out.append(("; ".join(render_item(x, scale) for x in new), "item_swap_" + kind, None))
    if not out and len(items) >= 2:
        for i in range(len(items)):
            new = items[:i] + items[i + 1:]
            out.append(("; ".join(render_item(x, scale) for x in new), "item_dropped", None))
    return out


def consistent(q, table_text, para_text):
    t = q["answer_type"]
    if t == "arithmetic":
        tree, v = parse_deriv(q["derivation"])
        if tree is None or not isinstance(q["answer"], (int, float)):
            return None
        g = float(q["answer"])
        tol = max(0.006 * abs(g), 0.011)
        if abs(v - g) <= tol:
            return 1.0
        if abs(v * 100 - g) <= tol:
            return 100.0
        return None
    if t == "count":
        items = [x for x in q["derivation"].split("##") if x.strip()]
        try:
            return 1.0 if int(float(q["answer"])) == len(items) and len(items) >= 1 else None
        except Exception:  # noqa: BLE001
            return None
    ans = q["answer"] if isinstance(q["answer"], list) else [q["answer"]]
    if not ans or (t == "span" and len(ans) != 1):
        return None
    hay = C.norm(table_text + " " + para_text)
    for a in ans:
        n = C.norm(str(a))
        if not n or f" {n} " not in f" {hay} ":
            return None
    return 1.0


def main():
    paths = {rel: C.fetch(BASE + rel, CACHE / rel.split("/")[-1], sha) for rel, sha in FILES.items()}
    data = json.load(open(paths["dataset_raw/tatqa_dataset_train.json"]))  # TRAIN ONLY
    rng = random.Random(C.SEED)
    drop = Counter()
    ctxs = []
    for x in data:
        table = [[C.clean_cell(v, 10_000) for v in row] for row in x["table"]["table"]]
        paras = [C.clean_cell(p["text"], 100_000) for p in sorted(x["paragraphs"], key=lambda p: p["order"])]
        paras = [p for p in paras if p]
        table_text = C.render_table(table)
        para_text = "\n".join(paras)
        ctx_text = table_text + "\n" + para_text
        idx, nums = cell_index(table)
        text_ans = [(q["question"], C.clean_cell(q["answer"][0], 10_000)) for q in x["questions"]
                    if q["answer_type"] == "span" and q["answer_from"] == "text" and isinstance(q["answer"], list)]
        cands = []
        for q in x["questions"]:
            factor = consistent(q, table_text, para_text)
            if factor is None:
                drop["inconsistent human answer"] += 1
                continue
            if reversed_change(q["question"]):
                drop["change question with reversed years (sign ambiguous)"] += 1
                continue
            if scale_unstated(q["scale"], ctx_text):
                drop["answer scale not stated in the excerpt"] += 1
                continue
            if q["answer_type"] == "count" and not re.search(r"\bhow many\b|\bnumber of\b", q["question"], re.I):
                drop["count answer to a non-count question ('Which years ...?' -> '1')"] += 1
                continue
            t = q["answer_type"]
            if t == "arithmetic":
                g = float(q["answer"])
                dec = gold_decimals(q["answer"])
                gold_txt = render_number(g, dec, q["scale"])
                dis = arithmetic_distractors(q, table, nums, ctx_text, g, dec, factor)
            elif t == "count":
                n = int(float(q["answer"]))
                gold_txt = str(n)
                dis = [(str(n + 1), "count_plus_one", None)] + ([(str(n - 1), "count_minus_one", None)] if n > 1 else [])
            elif t == "span":
                gold_txt = render_item(q["answer"][0], q["scale"])
                dis = span_distractors(q, table, idx, para_text + "\n" + table_text,
                                       [(oq, oa) for oq, oa in text_ans if oq != q["question"]])
            else:
                gold_txt = "; ".join(render_item(a, q["scale"]) for a in q["answer"])
                dis = multispan_distractors(q, table, idx)
            if t in ("span", "multi-span") and C.norm(gold_txt) in ("yes", "no"):
                dis = [("No" if C.norm(gold_txt) == "yes" else "Yes", "yesno_flip", None)]
            if OPEN_Q.search(q["question"]):
                dis = []  # open question ("what is a factor ...", "examples"): other items may also be right
            dis = [d for d in dis if light(d[0]) != light(gold_txt) and d[0].strip()]
            cands.append({"q": q, "gold_txt": gold_txt, "dis": dis, "stratum": (t, q["answer_from"])})
        ctxs.append({"uid": x["table"]["uid"], "table_text": table_text, "para_text": para_text, "cands": cands})

    # local decontamination (contexts and questions)
    docs = {}
    for cx in ctxs:
        docs["ctx:" + cx["uid"]] = cx["table_text"] + "\n" + cx["para_text"]
        for cd in cx["cands"]:
            docs["q:" + cd["q"]["uid"]] = cd["q"]["question"]
    hit = C.local_decontam(docs)
    kept_ctx = []
    for cx in ctxs:
        if "ctx:" + cx["uid"] in hit:
            drop["13-gram overlap (context)"] += len(cx["cands"])
            continue
        n0 = len(cx["cands"])
        cx["cands"] = [cd for cd in cx["cands"] if "q:" + cd["q"]["uid"] not in hit]
        drop["13-gram overlap (question)"] += n0 - len(cx["cands"])
        kept_ctx.append(cx)

    # per context: up to MAX_PER_CONTEXT questions, distinct normalised questions, diverse answer types
    pool = []
    for cx in sorted(kept_ctx, key=lambda c: c["uid"]):
        cands = sorted(cx["cands"], key=lambda cd: cd["q"]["uid"])
        rng.shuffle(cands)
        cands.sort(key=lambda cd: (not cd["dis"],))  # candidates that can be a "no" row first (stable)
        chosen, seen_q, seen_t = [], set(), Counter()
        for cd in sorted(cands, key=lambda cd: seen_t[cd["stratum"][0]]):
            nq = C.norm(cd["q"]["question"])
            if nq in seen_q or seen_t[cd["stratum"][0]] >= 2:
                continue
            chosen.append(cd)
            seen_q.add(nq)
            seen_t[cd["stratum"][0]] += 1
            if len(chosen) >= MAX_PER_CONTEXT:
                break
        drop["over per-context cap"] += len(cands) - len(chosen)
        for cd in chosen:
            cd["ctx"] = cx
            pool.append(cd)

    # label assignment balanced per stratum: half "no" (needs a distractor), half "yes"
    by_stratum = defaultdict(list)
    for cd in pool:
        by_stratum[cd["stratum"]].append(cd)
    rows = []
    for st in sorted(by_stratum):
        lst = by_stratum[st]
        rng.shuffle(lst)
        can_no = [cd for cd in lst if cd["dis"]]
        k = min(len(can_no), len(lst) // 2)
        no_set = {id(cd) for cd in can_no[:k]}
        yes = [cd for cd in lst if id(cd) not in no_set][:k]
        drop["stratum balance"] += len(lst) - 2 * k
        for cd in can_no[:k]:
            # prefer distractors with the gold's sign (a lone minus sign must not give the label away);
            # sign_flip keeps its purpose-built opposite sign
            gneg = cd["gold_txt"].startswith("-")
            dis = [d for d in cd["dis"] if d[1] == "sign_flip" or d[0].startswith("-") == gneg] or cd["dis"]
            kinds = sorted({d[1] for d in dis})
            kind = rng.choice(kinds)
            txt = rng.choice(sorted(d[0] for d in dis if d[1] == kind))
            rows.append((cd, txt, False, kind))
        for cd in yes:
            rows.append((cd, cd["gold_txt"], True, "human_gold"))

    out, seen_state = [], set()
    rows.sort(key=lambda r: r[0]["q"]["uid"])
    rng.shuffle(rows)
    n_neg = int(round(NEG_SHARE * len(rows)))
    for i, (cd, ans_txt, is_gold, kind) in enumerate(rows):
        q, cx = cd["q"], cd["ctx"]
        negq = i < n_neg
        state = (f"Company annual report excerpt\nTable:\n{cx['table_text']}\nText:\n{cx['para_text']}\n\n"
                 f"Question: {C.clean_cell(q['question'], 10_000)}\nProposed answer: {ans_txt}")
        if len(state) > MAX_STATE:
            drop["state too long"] += 1
            continue
        ns = C.norm(state)
        if ns in seen_state:
            drop["duplicate state"] += 1
            continue
        seen_state.add(ns)
        correct = is_gold
        gold = ("yes" if not correct else "no") if negq else ("yes" if correct else "no")
        t = q["answer_type"]
        edges = []
        if negq:
            edges.append("negation")
        if kind == "wrong_scale":
            edges.append("units")
        if kind == "item_dropped":
            edges.append("quantifier")
        if q["answer_from"] == "table-text":
            edges.append("multi_hop")
        if t in ("arithmetic", "count"):
            edges.append("numeric")
        if q["answer_from"] in ("table", "table-text"):
            edges.append("table")
        if len(state) > 3500:
            edges.append("long_context")
        prio = ["units", "negation", "quantifier", "multi_hop", "numeric", "long_context", "table"]
        edge = next((e for e in prio if e in edges), None)
        out.append({
            "key": KEY, "rid": q["uid"], "state": state,
            "instructions": Q_WRONG if negq else Q_CORRECT,
            "options": ["yes", "no"], "gold": gold, "soft": None,
            "meta": {"dataset": "NExTplusplus/TAT-QA (github)", "config": "dataset_raw/tatqa_dataset_train.json",
                     "revision": f"git:{COMMIT}; sha256:{FILES['dataset_raw/tatqa_dataset_train.json']}",
                     "licence": LICENCE, "split": "train",
                     "orig_label": {"answer": q["answer"], "answer_type": t, "answer_from": q["answer_from"],
                                    "scale": q["scale"], "derivation": q["derivation"]},
                     "family": C.FAMILY, "edge": edge, "edge_all": edges, "defs": "wrong" if negq else "correct",
                     "proposed_is_gold": is_gold, "distractor": kind, "context_id": cx["uid"]},
        })

    summ = C.check_rows(KEY, out)
    print("drops:", dict(drop))
    print("distractor kinds:", dict(Counter(r["meta"]["distractor"] for r in out)))
    print("strata:", dict(Counter((r["meta"]["orig_label"]["answer_type"], r["meta"]["orig_label"]["answer_from"],
                                   r["meta"]["proposed_is_gold"]) for r in out)))
    C.write_outputs(KEY, out, DEFS)
    if "--manifest" in sys.argv:
        C.append_manifest({
            "key": KEY, "family": C.FAMILY, "dataset": "NExTplusplus/TAT-QA (train)", "licence": LICENCE,
            "rows": summ["rows"], "qtype": "yesno", "yesno_share": round(summ["yesno_share"], 4),
            "edge_tags": summ["edge_tags"],
            "notes": ("Answer verification over real annual-report tables+text. Yes rows = human gold answer; no rows = "
                      "program-built wrong answers from the human derivation (wrong cell/year, wrong base, sum vs "
                      "average, sign flip, wrong scale, swapped/dropped list item, count +-1). 20% negated question "
                      "('is it wrong?'). <=3 questions per report; balanced per answer-type stratum; 13-gram decontam."),
        })


if __name__ == "__main__":
    main()
