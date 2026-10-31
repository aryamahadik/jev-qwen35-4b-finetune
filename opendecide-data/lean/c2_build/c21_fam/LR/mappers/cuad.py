"""LR-23 CUAD v1 mapper (family LR-nli, long document). Recast table below (Opus approves, G-R4 batch).

Own label: the law-student / lawyer annotation of each contract for each of the 41 clause categories: a category has answer spans
(char offsets in the contract) or it has none anywhere in the contract (is_impossible). Recast: yes/no "does this contract
EXCERPT contain a clause of the stated type?". The excerpt is built by PROGRAM span selection from the SAME contract only
(LR-B10): the contract is cut into fixed ~700-character windows (exact offsets); a YES excerpt keeps EVERY window that overlaps an
answer span of the category plus seeded random other windows of the same contract until the token budget is used; a NO excerpt
is made for a (contract, category) pair with NO answer anywhere in the contract (the lawyers' contract-level 'no clause'), from
seeded random windows with one anchor window chosen the same way as a gold window (so the two kinds are built identically). Windows
are shown in document order as numbered segments. A YES whose answer spans do not match the contract text at the stated offset, or
whose gold windows alone exceed the budget, is dropped and logged (never cut). NEVER touched: test.json (quarantine).
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import lr_common as lc  # noqa: E402

DATASET = "cuad"
FORM = "lr_cuad_clause_present"
FORMS = {FORM: "Does the contract excerpt contain a clause of the stated type?"}
WINDOW_CHARS = 700
BUDGET_TOKENS = 650
RECAST_TABLE = {
    "dataset_id": "CUAD v1 (TheAtticusProject/cuad data.zip) train_separate_questions.json", "train_file": "train_separate_questions.json",
    "split_field": "file name (test.json quarantined; CUADv1.json not kept)",
    "source_label_set": ["category has >= 1 annotated answer span", "category has none (is_impossible, no entry with answers)"],
    "recast_option_set": ["Yes", "No"], "target_format": "yes/no",
    "mapping": {"annotated answer spans exist for the category": "Yes (excerpt keeps every window overlapping an answer)",
                "no answer anywhere in the contract": "No (random windows of the same contract)"},
    "distractor_policy": "same-contract windows only (seeded random); YES keeps all gold windows",
    "declared_balancing": "50% yes (equal YES and NO counts); round-robin over the 41 categories inside each side",
    "declared_drops": ["answer offset does not match text", "gold windows exceed token budget", "category not parsed", "R12 guards (PII: emails, phones in contract text)"],
    "question_form_ids": [FORM], "span_selection_rule": "700-char windows; all gold windows + seeded random windows to 650 tokens (lc.select_spans)",
    "expected_token_mean": 760,
}
META = {"dataset": DATASET, "lr_id": "LR-23", "family": "LR-nli", "tier": "C", "cap": 500, "share_alike": False,
        "p1_realism": False, "recast_table": RECAST_TABLE}

_CAT = re.compile(r'related to "(.*?)" that should be reviewed')
_DET = re.compile(r"Details:\s*(.*)$", re.S)


def category_of(question):
    m = _CAT.search(question or "")
    return m.group(1) if m else None


def details_of(question):
    m = _DET.search(question or "")
    return lc.normalise_ws(m.group(1)) if m else ""


def read_train(train_dir=None):
    """Yield one record per contract: {title, context, qas (raw list), _src_line}."""
    d = lc.guard_train_path(train_dir or lc.raw_train_dir(DATASET))
    with open(os.path.join(d, "train_separate_questions.json"), "r", encoding="utf-8") as f:
        obj = json.load(f)
    for doc in obj["data"]:
        for p in doc["paragraphs"]:
            yield {"title": doc["title"], "context": p["context"], "qas": p["qas"], "_src_line": "cuad:" + doc["title"]}


def windows(text, size=WINDOW_CHARS):
    """Fixed windows with exact offsets: [(start, end)], each end snapped forward to the next whitespace."""
    out, i, n = [], 0, len(text)
    while i < n:
        j = min(n, i + size)
        while j < n and not text[j].isspace():
            j += 1
        if text[i:j].strip():
            out.append((i, j))
        i = j
    return out


def category_table(src):
    """{category: {'details': str, 'answers': [(start, text)]}} from the raw qas list."""
    cats = {}
    for qa in src["qas"]:
        c = category_of(qa["question"])
        if c is None:
            continue
        e = cats.setdefault(c, {"details": details_of(qa["question"]), "answers": []})
        for a in qa.get("answers") or []:
            e["answers"].append((a["answer_start"], a["text"]))
    return cats


class Mapper(lc.BaseMapper):
    META = META
    FORMS = FORMS

    def build(self, src, ctx):
        """ctx: {'category': str}. One candidate for one (contract, category)."""
        cat = ctx["category"]
        sid = "%s::%s" % (src["_src_line"], cat)
        table = ctx.get("table") or category_table(src)
        e = table[cat]
        text = src["context"]
        wins = windows(text)
        spans = [lc.normalise_ws(text[a:b]) for a, b in wins]
        has = bool(e["answers"])
        if has:
            gold = set()
            for st, t in e["answers"]:
                if text[st:st + len(t)] != t:
                    self.drops.add("answer_offset_mismatch", sid)
                    return []
                en = st + len(t)
                for k, (a, b) in enumerate(wins):
                    if a < en and b > st:
                        gold.add(k)
            gold_idx = sorted(gold)
            if not gold_idx:
                self.drops.add("answer_offset_mismatch", sid)
                return []
        else:
            rng = lc.seeded_rng("cuad-anchor", sid, self.seed)
            gold_idx = [rng.randrange(len(spans))] if spans else []
            if not gold_idx:
                self.drops.add("empty_contract", sid)
                return []
        chosen, info = lc.select_spans(spans, gold_idx, BUDGET_TOKENS, key="%s|%s" % (sid, self.seed))
        if chosen is None:
            self.drops.add("gold_windows_exceed_budget", sid)
            return []
        body = "\n\n".join("[Segment %d]\n%s" % (i + 1, spans[k]) for i, k in enumerate(chosen))
        context = "Clause type: %s\nWhat to look for: %s\n\nContract excerpt:\n%s" % (cat, e["details"], body)
        return [{"form": FORM, "kind": "yesno", "context": context, "options": ["Yes", "No"], "gold_text": "Yes" if has else "No",
                 "source_row_id": sid, "extra": {"contract": src["title"], "category": cat, "has_clause": has, "span_info": info,
                                                  "n_windows_contract": len(wins)}}]

    def independent_gold(self, src, cand):
        cat = cand["extra"]["category"]
        needle = '"%s"' % cat
        return "Yes" if any(qa.get("answers") for qa in src["qas"] if needle in qa["question"] and not qa.get("is_impossible")) else "No"

    def map_records(self, records, ctx=None, cap=None, select_key=None):
        cap = cap if cap is not None else META["cap"]
        side = {"Yes": {}, "No": {}}
        recs = {}
        for src in records:
            table = category_table(src)
            recs[src["_src_line"]] = (src, table)
            for cat, e in table.items():
                side["Yes" if e["answers"] else "No"].setdefault(cat, []).append((src["_src_line"], cat))
        half = cap // 2
        rows = []
        for lab in ("Yes", "No"):
            groups = {c: list(v) for c, v in side[lab].items()}

            def make(item):
                src, table = recs[item[0]]
                out = []
                for cand in self.build(src, {"category": item[1], "table": table}):
                    r = self.finish_candidate(src, cand)
                    if r:
                        out.append(r)
                return out
            part = lc.round_robin_take(groups, "cuad%s%s" % (lab, self.seed), half, make)
            rows.append(part)
        n = min(len(rows[0]), len(rows[1]))          # equal YES / NO counts (yes rate exactly 50%)
        return rows[0][:n] + rows[1][:n]
