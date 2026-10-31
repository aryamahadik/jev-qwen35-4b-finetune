"""LR-21 SciFact mapper (claims_train.jsonl + the abstracts cited by train claims). Recast table below (Opus approves, G-R4 batch).

Own label (expert-written claims, expert evidence annotations; no LM text): per (claim, cited abstract) pair the dataset's label
is SUPPORT / CONTRADICT when the abstract holds rationales for the claim, and NOT ENOUGH INFO when a cited abstract has none.
Recast: pick-one among SUPPORTS / REFUTES / NOT ENOUGH INFO over claim + the full abstract (title + numbered sentences; abstracts
are short, so no span cut is made and a row over the token cap is dropped, never cut). One pair per claim (a claim with evidence
uses one of its evidence abstracts). Balanced equally over the 3 labels (declared). NEVER touched: dev, test claims (quarantine).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import lr_common as lc  # noqa: E402

DATASET = "scifact"
FORM = "lr_scifact_verdict"
FORMS = {FORM: "Does the abstract support the claim, contradict it, or not give enough information?"}
RECAST_TABLE = {
    "dataset_id": "allenai/scifact release/latest data.tar.gz (claims_train.jsonl, corpus.jsonl)", "train_file": "claims_train.jsonl + corpus_train_cited.jsonl",
    "split_field": "file name (dev/test claims quarantined)", "source_label_set": ["SUPPORT", "CONTRADICT", "(cited abstract with no evidence)"],
    "recast_option_set": ["SUPPORTS", "REFUTES", "NOT ENOUGH INFO"], "target_format": "Choice 3",
    "mapping": {"SUPPORT": "SUPPORTS", "CONTRADICT": "REFUTES", "no evidence in a cited abstract": "NOT ENOUGH INFO"},
    "distractor_policy": "all 3 labels shown", "declared_balancing": "round-robin over the 3 labels until a label runs out; one row per abstract and one pair per claim",
    "declared_drops": ["claim without a cited abstract in the corpus", "second claim on an abstract already used (R8)", "abstract over the token cap", "R12 guards / PII"],
    "question_form_ids": [FORM], "span_selection_rule": "whole abstract (no cut)", "expected_token_mean": 330,
}
META = {"dataset": DATASET, "lr_id": "LR-21", "family": "LR-nli", "tier": "A", "cap": 500, "share_alike": False,
        "p1_realism": False, "recast_table": RECAST_TABLE, "native_abstain": "NOT ENOUGH INFO"}
OPTIONS = ["SUPPORTS", "REFUTES", "NOT ENOUGH INFO"]


def read_train(train_dir=None):
    d = lc.guard_train_path(train_dir or lc.raw_train_dir(DATASET))
    corpus = {}
    for r in lc.read_jsonl(os.path.join(d, "corpus_train_cited.jsonl")):
        corpus[int(r["doc_id"])] = r
    for c in lc.read_jsonl(os.path.join(d, "claims_train.jsonl")):
        c["_corpus"] = corpus
        c["_src_line"] = "scifact:%s" % c["id"]
        yield c


def pair_label(claim, doc_id):
    """The dataset's own label for (claim, cited abstract)."""
    ev = claim.get("evidence", {}).get(str(doc_id))
    if not ev:
        return "NOT ENOUGH INFO"
    labs = {e["label"] for e in ev}
    return "SUPPORTS" if labs == {"SUPPORT"} else ("REFUTES" if labs == {"CONTRADICT"} else None)


def render_abstract(doc):
    sents = "\n".join("[%d] %s" % (i, lc.normalise_ws(s)) for i, s in enumerate(doc["abstract"]))
    return "%s\n%s" % (lc.normalise_ws(doc["title"]), sents)


class Mapper(lc.BaseMapper):
    META = META
    FORMS = FORMS

    def build(self, src, ctx):
        corpus = src["_corpus"]
        docs = [int(x) for x in src.get("cited_doc_ids", []) if int(x) in corpus]
        ev_docs = [d for d in docs if str(d) in src.get("evidence", {})]
        pool = ev_docs or docs
        if not pool:
            self.drops.add("no_cited_abstract_in_corpus", src["_src_line"])
            return []
        doc = pool[lc.stable_hash("scifactdoc", self.seed, src["_src_line"]) % len(pool)]
        gold = pair_label(src, doc)
        if gold is None:
            self.drops.add("mixed_labels_in_one_abstract", src["_src_line"])
            return []
        ctxt = "Claim: %s\n\nAbstract:\n%s" % (lc.normalise_ws(src["claim"]), render_abstract(corpus[doc]))
        return [{"form": FORM, "kind": "choice", "context": ctxt, "options": list(OPTIONS), "gold_text": gold,
                 "source_row_id": "%s/doc%d" % (src["_src_line"], doc), "native_abstain": gold == "NOT ENOUGH INFO",
                 "extra": {"doc_id": doc, "label": gold}}]

    def independent_gold(self, src, cand):
        doc = str(cand["extra"]["doc_id"])
        rationales = src.get("evidence", {}).get(doc, [])
        if not rationales:
            return "NOT ENOUGH INFO"
        return {"SUPPORT": "SUPPORTS", "CONTRADICT": "REFUTES"}[rationales[0]["label"]]

    def map_records(self, records, ctx=None, cap=None, select_key=None):
        cap = cap if cap is not None else META["cap"]
        groups = {o: [] for o in OPTIONS}
        for src in records:
            docs = [int(x) for x in src.get("cited_doc_ids", []) if int(x) in src["_corpus"]]
            pool = [d for d in docs if str(d) in src.get("evidence", {})] or docs
            if not pool:
                self.drops.add("no_cited_abstract_in_corpus", src["_src_line"])
                continue
            doc = pool[lc.stable_hash("scifactdoc", self.seed, src["_src_line"]) % len(pool)]
            lab = pair_label(src, doc)
            if lab:
                groups[lab].append((src, doc))

        def make(item):
            src = item[0]
            out = []
            for cand in self.build(src, {}):
                r = self.finish_candidate(src, cand)
                if r:
                    out.append(r)
            return out
        # at most one row per abstract: claims citing the same abstract would otherwise be near-duplicate renderings (R8)
        return lc.round_robin_take(groups, "scifact%s" % self.seed, cap, make, unit_of=lambda it: it[1], unit_limit=1)
