"""OHS-1 part "legal" (track U): expert rule application and very large label sets.

Sources (zero-shot, dataset gold only, official wording only):
  * nguha/legalbench (CC BY 4.0 tasks only): hearsay, abercrombie, unfair_tos, overruling, 8 seeded cuad_* tasks
  * coastalcph/lex_glue ledgar: 100-way provision type; the options are the 100 official label names

Changes after verification (v2):
  * function_of_decision_section was DROPPED. Its LegalBench test.tsv is misaligned by one paragraph in many
    places (labels and the Citation column are shifted), so the dataset gold is wrong for many items. We may not
    relabel it ourselves, so it is replaced by `abercrombie` (CC BY 4.0 per LegalBench paper Table 8; 5-way
    rule-application task whose official definitions are in the task prompt).
  * ledgar: LEDGAR labels are the provision headings used by the drafters, so near-synonym labels and multi-topic
    provisions make many golds undecidable from the text. All 100 labels stay in the option list, but gold labels
    are restricted and items filtered (all statistics from LEDGAR train+validation, TF-IDF cosine, nothing trained):
    label level, excluded as gold: (a) catch-all labels; (b) name-synonym / content-overlap clusters;
    (c) label pairs LEDGAR uses for near-identical provisions (cosine >= 0.8; >= 2% of a label's near-duplicates
    and >= 2 cases; both labels excluded; pairs with a catch-all ignored); (d) labels whose provisions have a
    same-label nearest neighbour less than 85% of the time.
    item level: the provision must mention its gold topic (anchor regex from the label name), must not mention
    the topic of a label that LEDGAR confuses with the gold (>= 1% nearest-neighbour confusion, >= 3 cases),
    and its gold must be the label of >= 8 of its 10 nearest train+validation provisions.
  * unfair_tos: LexGLUE/LegalBench mark only (potentially) unfair clauses, so fair arbitration, jurisdiction etc.
    clauses sit in "Other". "Other" items that mention any category topic are removed, and clause fragments
    (< 8 word tokens) are removed from every class.
  * hearsay: exact 41/41 class balance (only 41 Yes items exist in the test split).
  * LegalBench TSV texts had doubled quote escapes ('""economic benefit""'); these are unescaped.
  * overruling / cuad sentences under 8 word tokens (citation fragments such as 'id., citing barnes v') are dropped.

definition_classification is CC BY-SA 4.0 (not CC BY 4.0), so it is skipped by default and replaced by
`overruling` (CC BY 4.0). Pass --with-definition-classification to add it anyway.

Licences were checked per task on 2026-09-26 in github.com/HazyResearch/legalbench/tasks/<task>/README.md;
abercrombie's README is missing there, so its licence is taken from the LegalBench paper (arXiv:2308.11462),
Table 8, which lists Abercrombie under Creative Commons Attribution 4.0.
Re-runnable and deterministic: pinned dataset revisions, seed 20260927. The LEDGAR label statistics take
~3-4 min on CPU the first time and are cached in ohs/cache/ledgar_labelstats_*.json.

Run:  .venv/bin/python lean/ohs/build_legal.py
Out:  lean/data/ohs_parts/legal.jsonl
"""
import argparse
import hashlib
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from huggingface_hub import hf_hub_download

SEED = 20260927
PART = "legal"
TRACK = "U"
HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "data" / "ohs_parts" / f"{PART}.jsonl"
CACHE = HERE / "cache"

LB_ID, LB_REV = "nguha/legalbench", "daec8237410aa23e3faf4bc41ad8b3a7e1696826"
LG_ID, LG_REV = "coastalcph/lex_glue", "c23fdff1a6bf74e0e1a71cb86f1e781d37da888c"
LB_LICENSE_URL = "https://github.com/HazyResearch/legalbench/tree/main/tasks/{task}/README.md"
CC_BY = "CC BY 4.0"
MIN_LEN, MAX_LEN = 20, 6000
MIN_WORDS = 8  # sentence/clause-level LegalBench tasks: drop fragments such as 'by mail : headspace , inc. .'

# Verified task licences (LegalBench task READMEs). Every cuad_* task is CC BY 4.0.
LB_LICENSE = {"hearsay": CC_BY, "unfair_tos": CC_BY, "overruling": CC_BY, "abercrombie": CC_BY,
              "function_of_decision_section": CC_BY, "definition_classification": "CC BY-SA 4.0"}
LB_LICENSE_SRC = {"abercrombie": "LegalBench paper arXiv:2308.11462, Table 8 (task README not present on GitHub)"}

# unfair_tos label descriptions: the first sentence of each category's definition in Lippi et al. (2019),
# "CLAUDETTE: an automated detector of potentially unfair clauses in online terms of service", Sec. 3
# (arXiv:1805.01217; checked verbatim against the paper text). "Other" is from the LegalBench unfair_tos README.
UNFAIR_TOS_OPTIONS = ["Arbitration", "Unilateral change", "Content removal", "Jurisdiction", "Choice of law",
                      "Limitation of liability", "Unilateral termination", "Contract by using", "Other"]
UNFAIR_TOS_CARD = {
    "Arbitration": "The arbitration clause requires or allows the parties to resolve their disputes through an "
                   "arbitration process, before the case could go to court.",
    "Unilateral change": "The unilateral change clause specifies the conditions under which the service provider "
                         "could amend and modify the terms of service and/or the service itself.",
    "Content removal": "The content removal gives the provider a right to modify/delete user’s content, including "
                       "in-app purchases, and sometimes specifies the conditions under which the service provider "
                       "may do so.",
    "Jurisdiction": "The jurisdiction clause stipulates what courts will have the competence to adjudicate disputes "
                    "under the contract.",
    "Choice of law": "The choice of law clause specifies what law will govern the contract, meaning also what law "
                     "will be applied in potential adjudication of a dispute arising under the contract.",
    "Limitation of liability": "The limitation of liability clause stipulates that the duty to pay damages is "
                               "limited or excluded, for certain kind of losses, under certain conditions.",
    "Unilateral termination": "The unilateral termination clause gives provider the right to suspend and/or "
                              "terminate the service and/or the contract, and sometimes details the circumstances "
                              "under which the provider claims to have a right to do so.",
    "Contract by using": "The contract by using clause stipulates that the consumer is bound by the terms of use of "
                         "a specific service, simply by using the service, without even being required to mark "
                         "that he or she has read and accepted them.",
    "Other": "Corresponds to clauses in agreements which don't fit into these categories.",
}
# LegalBench unfair_tos README: task headline + the sentence on what the categories mean
# (README: "The first eight categories correspond to clauses that would potentially be deemed potentially unfair.
# The last category (Other) ..."; reworded only so it does not depend on option order.)
UNFAIR_TOS_Q = ("Given a clause from a terms-of-service contract, determine the category the clause belongs to. "
                "All categories except Other correspond to clauses that would potentially be deemed potentially "
                "unfair; Other corresponds to clauses in agreements which don't fit into these categories.")
# "Other" clauses that touch any category topic are ambiguous (the source only labels unfair clauses of a
# category, so fair arbitration / jurisdiction / liability ... clauses are "Other"). Keep only clearly off-topic ones.
UNFAIR_TOS_TOPIC = re.compile(
    r"arbitrat|jurisdiction|court|forum|venue|dispute|govern|\blaws?\b|liab|damage|indemn|warrant|disclaim|responsib|risk|"
    r"terminat|suspend|cancel|disable|deactivat|amend|modif|chang|updat|revis|remov|delet|content|"
    r"by using|by accessing|use of the|your use|accept|agree to (?:these|this|the) terms|binding")

ABERCROMBIE_OPTIONS = ["generic", "descriptive", "suggestive", "arbitrary", "fanciful"]
ABERCROMBIE_Q = "What is the type of mark?"  # verbatim from the LegalBench abercrombie prompt

# lex_glue dataset card, LEDGAR: "Each label represents the single main topic (theme) of the corresponding
# contract provision."
LEDGAR_Q = "Which label represents the single main topic (theme) of this contract provision?"
LEDGAR_LICENSE = CC_BY
LEDGAR_LICENSE_NOTE = ("coastalcph/lex_glue HF card YAML: cc-by-4.0 (its 'Licensing Information' section says "
                       "'[More Information Needed]'); original LEDGAR (Tuggener et al., LREC 2020) calls the corpus "
                       "'freely available' without naming a licence; texts are public SEC EDGAR filings.")
# (a) catch-all labels: never a decidable gold when a specific label also fits.
LEDGAR_CATCH_ALL = ["General", "Miscellaneous", "Agreements"]
# (b) label-name synonyms / content-overlap clusters among the 100 official names (verifier examples included).
LEDGAR_NAME_CLUSTERS = [
    ["Successors", "Assigns", "Assignments", "Binding Effects"], ["Defined Terms", "Definitions"],
    ["Amendments", "Modifications"], ["Waivers", "No Waivers", "Waiver Of Jury Trials"],
    ["Indemnifications", "Indemnity"], ["Taxes", "Tax Withholdings", "Withholdings"],
    ["Governing Laws", "Applicable Laws"], ["Organizations", "Existence", "Powers", "Authority", "Qualifications"],
    ["Integration", "Entire Agreements"], ["Costs", "Expenses", "Fees"], ["Effective Dates", "Effectiveness"],
    ["Consents", "Approvals", "Authorizations"], ["Books", "Records"],
    ["Jurisdictions", "Consent To Jurisdiction", "Submission To Jurisdiction", "Venues"],
    ["Employment", "Positions", "Duties"], ["Representations", "Warranties"], ["Enforceability", "Enforcements"],
    ["Interpretations", "Construction"], ["Headings", "Titles"], ["Terms", "Terminations"],
    ["Vesting", "Forfeitures"]]
# (c) data-driven near-duplicate label pairs
NN_COS, NN_RATE, NN_MIN = 0.8, 0.02, 2
# (d) LEDGAR's own consistency: share of a label's train+val provisions whose nearest other provision has the same
# label (leave-one-out 1-NN). Labels below SELF_MIN are too heading-dependent to be decided from the text.
SELF_MIN = 0.85
# (e) confusable label pairs: >= CONF_RATE of either label's provisions have the other label as nearest neighbour
CONF_RATE, CONF_MIN = 0.01, 3
# per-item convention check
KNN_K, KNN_MIN = 10, 8
# Topic anchors (lower-cased regex), taken from each official label name (stem, plus the standard term of art
# where the name is abstract). Item filter: the provision must mention its gold topic, and must not mention the
# topic of a label that LEDGAR confuses with the gold label (e). Catch-all labels have no anchor.
LEDGAR_ANCHOR = {
    "Adjustments": r"adjust", "Agreements": None, "Amendments": r"amend", "Anti-Corruption Laws": r"corrupt|brib",
    "Applicable Laws": r"applicable law", "Approvals": r"approv", "Arbitration": r"arbitra",
    "Assignments": r"assign", "Assigns": r"assign", "Authority": r"authori", "Authorizations": r"authori",
    "Base Salary": r"salary", "Benefits": r"benefit", "Binding Effects": r"binding", "Books": r"\bbooks?\b",
    "Brokers": r"broker", "Capitalization": r"capitali", "Change In Control": r"change (?:in|of) control",
    "Closings": r"\bclos(?:e|es|ed|ing)\b", "Compliance With Laws": r"complian|\bcompl(?:y|ies|ied)\b",
    "Confidentiality": r"confidential", "Consent To Jurisdiction": r"jurisdiction", "Consents": r"consent",
    "Construction": r"constru", "Cooperation": r"cooperat", "Costs": r"\bcosts?\b", "Counterparts": r"counterpart",
    "Death": r"death|\bdie[sd]?\b", "Defined Terms": r"defin", "Definitions": r"defin", "Disability": r"disab",
    "Disclosures": r"disclos", "Duties": r"\bdut(?:y|ies)\b", "Effective Dates": r"effective date",
    "Effectiveness": r"effective", "Employment": r"employ", "Enforceability": r"enforc", "Enforcements": r"enforc",
    "Entire Agreements": r"entire agreement", "Erisa": r"erisa", "Existence": r"exist", "Expenses": r"expense",
    "Fees": r"\bfees?\b", "Financial Statements": r"financial statement", "Forfeitures": r"forfeit",
    "Further Assurances": r"further", "General": None, "Governing Laws": r"govern", "Headings": r"heading",
    "Indemnifications": r"indemn", "Indemnity": r"indemn", "Insurances": r"insur",
    "Integration": r"integrat|entire agreement",
    "Intellectual Property": r"intellectual property|patent|trademark|copyright",
    "Interests": r"interest", "Interpretations": r"interpret", "Jurisdictions": r"jurisdiction",
    "Liens": r"\bliens?\b", "Litigations": r"litigat|\bactions?\b|proceeding|\bsuits?\b", "Miscellaneous": None,
    "Modifications": r"modif", "No Conflicts": r"conflict", "No Defaults": r"default", "No Waivers": r"waive",
    "Non-Disparagement": r"disparag", "Notices": r"notice", "Organizations": r"organiz",
    "Participations": r"participa", "Payments": r"payment|\bpa(?:y|ys|id)\b", "Positions": r"position",
    "Powers": r"power", "Publicity": r"public", "Qualifications": r"qualif", "Records": r"record",
    "Releases": r"releas", "Remedies": r"remed", "Representations": r"represent", "Sales": r"\bsale|\bsell|\bsold\b",
    "Sanctions": r"sanction", "Severability": r"sever|invalid|unenforceab", "Solvency": r"solven",
    "Specific Performance": r"specific performance", "Submission To Jurisdiction": r"jurisdiction|submi",
    "Subsidiaries": r"subsidiar", "Successors": r"successor", "Survival": r"surviv", "Tax Withholdings": r"withh",
    "Taxes": r"\btax", "Terminations": r"terminat", "Terms": r"\bterm\b", "Titles": r"\btitle",
    "Transactions With Affiliates": r"affiliate", "Use Of Proceeds": r"proceeds", "Vacations": r"vacation",
    "Venues": r"venue", "Vesting": r"\bvest", "Waiver Of Jury Trials": r"jury", "Waivers": r"waive",
    "Warranties": r"warrant", "Withholdings": r"withh"}


def norm(t):
    return re.sub(r"\W+", " ", t.lower()).strip()


def n_words(t):
    return len(re.findall(r"[A-Za-z0-9]+", t))


def lb_text(t):
    """LegalBench TSV text: strip and undo the doubled quote escaping left in some files ('""x""' -> '"x"')."""
    return str(t).strip().replace('""', '"')


def lb_meta():
    p = hf_hub_download(LB_ID, "task_metadata.json", repo_type="dataset", revision=LB_REV)
    return json.load(open(p))


def lb_split(task, split):
    p = hf_hub_download(LB_ID, f"data/{task}/{split}.tsv", repo_type="dataset", revision=LB_REV)
    return pd.read_csv(p, sep="\t", dtype=str, keep_default_na=False)


def lb_question(meta, task):
    """Zero-shot task prompt without the text slot / answer cue (LegalBench task_metadata has no demos)."""
    ins = meta[task]["instruction"]
    if task == "hearsay":  # '<definition>\n\n{{text}} Is there hearsay?\nA:'
        head, tail = ins.split("{{text}}")
        return head.strip() + " " + tail.replace("A:", "").strip()
    return ins.split("\n\n")[0].strip()


def clean_pool(df, text_col, label_col, train_texts=(), text_fn=str.strip, min_words=0, keep_fn=None):
    """Length filter, fragment filter, drop test texts that also appear in the few-shot train split,
    dedupe on normalized text. keep_fn(text, label) -> reason string to drop, or None to keep."""
    seen, drop = set(norm(text_fn(t)) for t in train_texts), Counter()
    keep = []
    for _, r in df.iterrows():
        t = text_fn(str(r[text_col]))
        if len(t) < MIN_LEN:
            drop["too_short"] += 1
            continue
        if len(t) > MAX_LEN:
            drop["too_long"] += 1
            continue
        if min_words and n_words(t) < min_words:
            drop[f"fragment_lt{min_words}w"] += 1
            continue
        if keep_fn:
            why = keep_fn(t, r[label_col])
            if why:
                drop[why] += 1
                continue
        k = norm(t)
        if k in seen:
            drop["duplicate"] += 1
            continue
        seen.add(k)
        keep.append((t, r[label_col], r))
    return keep, dict(drop)


def stratified(pool, n, rng, per_class_cap=None, max_share=0.4):
    """Round-robin over classes (random class order) so the sample is as balanced as the data allows.
    Binary tasks are exactly balanced (if one class is short, the other is cut to the same size)."""
    by = defaultdict(list)
    for it in pool:
        by[it[1]].append(it)
    labels = sorted(by)
    for lab in labels:
        rng.shuffle(by[lab])
    rng.shuffle(labels)
    if per_class_cap:
        cap = per_class_cap
    elif len(labels) == 2:
        cap = min(-(-n // 2), min(len(v) for v in by.values()))
    else:
        cap = max(-(-n // len(labels)), int(max_share * n))
    take = Counter()
    while sum(take.values()) < n:
        moved = False
        for lab in labels:
            if sum(take.values()) >= n:
                break
            if take[lab] < min(cap, len(by[lab])):
                take[lab] += 1
                moved = True
        if not moved:
            break
    return [it for lab in labels for it in by[lab][: take[lab]]]


class Writer:
    def __init__(self):
        self.rows, self.calls = [], {}

    def add(self, *, source, source_item, header, text, qtype, question, options, gold, card, meta):
        state = f"{header}:\n{text}"
        key = hashlib.sha1(state.encode()).hexdigest()
        if key not in self.calls:
            self.calls[key] = f"c_ohs_{PART}_{len(self.calls) + 1:04d}"
        n = len(self.rows) + 1
        row = {"id": f"r_ohs_{PART}_{n:04d}", "group_id": f"g:ohs:{PART}:{source_item}",
               "call_id": self.calls[key], "split": "ohs", "track": TRACK, "source": source, "state": state,
               "qtype": qtype, "instructions": question, "options": options, "gold": gold,
               "role": "choice" if qtype == "choice" else "aff", "meta": meta}
        if card:
            row["card"] = card
        self.rows.append(row)


def lb_base_meta(task):
    return {"license": LB_LICENSE.get(task, CC_BY),
            "license_source": LB_LICENSE_SRC.get(task, LB_LICENSE_URL.format(task=task)),
            "hf_id": LB_ID, "config": task, "revision": LB_REV, "split_used": "test", "task": task}


def lb_yesno(w, meta, task, n, rng, header, source, report, extra_meta=(), min_words=0):
    test, train = lb_split(task, "test"), lb_split(task, "train")
    pool, drops = clean_pool(test, "text", "answer", train["text"].tolist(), text_fn=lb_text, min_words=min_words)
    picked = stratified(pool, n, rng)
    q = lb_question(meta, task)
    for text, ans, r in picked:
        m = lb_base_meta(task)
        m.update({"source_id": r["index"], "answer": ans})
        m.update({k: r[k] for k in extra_meta})
        w.add(source=source, source_item=f"{task}:{r['index']}", header=header, text=text, qtype="noul",
              question=q, options=None, gold=1 if ans == "Yes" else 0, card=None, meta=m)
    report[task] = {"hf_id": LB_ID, "config": task, "license": LB_LICENSE.get(task, CC_BY), "split_used": "test",
                    "n_items": len(picked), "n_options": "yes/no", "question": q,
                    "class_balance": dict(Counter(a for _, a, _ in picked)),
                    "pool_class_counts": dict(Counter(a for _, a, _ in pool)), "pool_after_filters": len(pool),
                    "dropped": drops}
    return picked


def lb_choice(w, meta, task, n, rng, header, source, options, question, card_map, report, text_col="text",
              extra_meta=(), min_words=0, keep_fn=None):
    test, train = lb_split(task, "test"), lb_split(task, "train")
    assert set(test["answer"]) <= set(options), set(test["answer"]) - set(options)
    pool, drops = clean_pool(test, text_col, "answer", train[text_col].tolist(), text_fn=lb_text,
                             min_words=min_words, keep_fn=keep_fn)
    picked = stratified(pool, n, rng)
    card = "\n".join(f"- {o}: {card_map[o]}" for o in options if o in card_map) or None
    for text, ans, r in picked:
        m = lb_base_meta(task)
        m["source_id"] = r["index"]
        m.update({k.lower(): r[k] for k in extra_meta})
        w.add(source=source, source_item=f"{task}:{r['index']}", header=header, text=text, qtype="choice",
              question=question, options=list(options), gold=ans, card=card, meta=m)
    report[task] = {"hf_id": LB_ID, "config": task, "license": LB_LICENSE[task], "split_used": "test",
                    "n_items": len(picked), "n_options": len(options), "question": question,
                    "class_balance": dict(Counter(a for _, a, _ in picked)),
                    "pool_class_counts": dict(Counter(a for _, a, _ in pool)), "pool_after_filters": len(pool),
                    "dropped": drops, "card": bool(card)}


def abercrombie_card(meta):
    """Official definitions from the abercrombie prompt: 'A mark is generic if it is ...'."""
    head = meta["abercrombie"]["instruction"].split("{{text}}")[0]
    out = {}
    for m in re.finditer(r"(A mark is (\w+) if [^.]*\.)", head):
        out[m.group(2)] = m.group(1)
    assert sorted(out) == sorted(ABERCROMBIE_OPTIONS), out
    return out


def unfair_tos_keep(text, label):
    if label == "Other" and UNFAIR_TOS_TOPIC.search(text.lower()):
        return "other_mentions_category_topic"
    return None


# ---------------------------------------------------------------- LEDGAR
def ledgar_load(split):
    p = hf_hub_download(LG_ID, f"ledgar/{split}-00000-of-00001.parquet", repo_type="dataset", revision=LG_REV)
    return p, pd.read_parquet(p)


def ledgar_vectorizer(ref_texts):
    from sklearn.feature_extraction.text import TfidfVectorizer  # unsupervised similarity only, nothing trained
    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_df=0.5, sublinear_tf=True, dtype=np.float32)
    return vec, vec.fit_transform(ref_texts)


def ledgar_label_stats(names, R, lab):
    """One pass over train+val (cosine on TF-IDF), cached (deterministic, ~3-4 min on CPU):
    pairs: for each label a, among a's provisions that have a near-duplicate (cosine >= NN_COS) elsewhere, the
           share whose near-duplicates include label b;
    nn1:   leave-one-out nearest neighbour label counts (a -> label of a provision's most similar other provision)."""
    cache = CACHE / f"ledgar_labelstats_{LG_REV[:8]}_cos{NN_COS}.json"
    if cache.exists():
        return json.load(open(cache))
    has, cross, nn1 = Counter(), Counter(), Counter()
    RT = R.T.tocsr()
    for s in range(0, R.shape[0], 1000):
        S = (R[s:s + 1000] @ RT).toarray()
        idx = np.arange(S.shape[0])
        S[idx, idx + s] = -1.0  # never match itself
        for i, j in enumerate(S.argmax(1)):
            nn1[(int(lab[s + i]), int(lab[j]))] += 1
        qi, qj = np.nonzero(S >= NN_COS)
        for i in np.unique(qi):
            a = int(lab[s + i])
            has[a] += 1
            for b in set(lab[qj[qi == i]].tolist()):
                if b != a:
                    cross[(a, int(b))] += 1
    tot = Counter(int(x) for x in lab)
    out = {"pairs": [{"a": names[a], "b": names[b], "n": c, "a_with_neardup": has[a], "rate": round(c / has[a], 4)}
                     for (a, b), c in sorted(cross.items())],
           "nn1": [{"a": names[a], "b": names[b], "n": c, "a_total": tot[a], "rate": round(c / tot[a], 4)}
                   for (a, b), c in sorted(nn1.items())]}
    CACHE.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(cache, "w"), indent=0)
    return out


def ledgar(w, n, rng, report):
    p, te = ledgar_load("test")
    names = json.loads(pq.read_schema(p).metadata[b"huggingface"])["info"]["features"]["label"]["names"]
    assert len(names) == 100 and set(LEDGAR_ANCHOR) == set(names)
    ref = pd.concat([ledgar_load("train")[1], ledgar_load("validation")[1]]).reset_index(drop=True)
    vec, R = ledgar_vectorizer(ref["text"])
    lab = ref["label"].values
    stats = ledgar_label_stats(names, R, lab)

    # ---- label level: which labels may be gold
    ca = set(LEDGAR_CATCH_ALL)
    data_edges = [e for e in stats["pairs"] if e["a"] not in ca and e["b"] not in ca
                  and e["rate"] >= NN_RATE and e["n"] >= NN_MIN]
    self_agree = {e["a"]: e["rate"] for e in stats["nn1"] if e["a"] == e["b"]}
    name_lab = {x for c in LEDGAR_NAME_CLUSTERS for x in c}
    assert name_lab <= set(names) and ca <= set(names)
    excluded = {x: "catch_all" for x in LEDGAR_CATCH_ALL}
    for x in sorted(name_lab):
        excluded.setdefault(x, "name_synonym_cluster")
    for e in data_edges:
        for x in (e["a"], e["b"]):
            excluded.setdefault(x, f"near_duplicate_label_pair ({e['a']} -> {e['b']}: {e['rate']:.3f})")
    for x in names:
        if self_agree.get(x, 0) < SELF_MIN:
            excluded.setdefault(x, f"low_1nn_self_agreement ({self_agree.get(x, 0):.2f} < {SELF_MIN})")
    allowed = [x for x in names if x not in excluded]
    # confusable partners of each allowed label (either direction), used by the item-level topic check
    partners = defaultdict(set)
    for e in stats["nn1"]:
        if e["a"] != e["b"] and e["rate"] >= CONF_RATE and e["n"] >= CONF_MIN and not ({e["a"], e["b"]} & ca):
            partners[e["a"]].add(e["b"])
            partners[e["b"]].add(e["a"])
    partners = {x: sorted(partners[x]) for x in allowed}
    rx = {k: re.compile(v) for k, v in LEDGAR_ANCHOR.items() if v}

    def topic_check(t, name):
        if name not in allowed:
            return "gold_label_excluded"
        low = t.lower()
        if not rx[name].search(low):
            return "gold_topic_not_mentioned"
        if any(rx[b].search(low) for b in partners[name]):
            return "mentions_confusable_label_topic"
        return None

    df = te.reset_index().rename(columns={"index": "row"})
    df["name"] = df["label"].map(lambda i: names[i])
    pool, drops = clean_pool(df, "text", "name", keep_fn=topic_check)
    # ---- item level: gold must be the label of >= KNN_MIN of the KNN_K nearest train+val provisions
    Q = vec.transform([t for t, _, _ in pool])
    gold_ids = np.array([int(r["label"]) for _, _, r in pool])
    agree = []
    for s in range(0, Q.shape[0], 500):
        S = (Q[s:s + 500] @ R.T).toarray()
        top = np.argsort(-S, axis=1, kind="stable")[:, :KNN_K]
        agree.extend(int(x) for x in (lab[top] == gold_ids[s:s + 500, None]).sum(1))
    kept = []
    for it, a in zip(pool, agree):
        if a >= KNN_MIN:
            kept.append(it + (a,))
        else:
            drops["knn_gold_disagreement"] = drops.get("knn_gold_disagreement", 0) + 1
    n_lab = len({l for _, l, _, _ in kept})
    cap = 1 if n_lab >= n else -(-n // n_lab)
    picked = stratified(kept, n, rng, per_class_cap=cap)
    for text, name, r, a in picked:
        m = {"license": LEDGAR_LICENSE, "license_note": LEDGAR_LICENSE_NOTE,
             "license_source": "https://huggingface.co/datasets/coastalcph/lex_glue", "hf_id": LG_ID,
             "config": "ledgar", "revision": LG_REV, "split_used": "test", "task": "ledgar",
             "source_id": int(r["row"]), "label_id": int(r["label"]), "knn_gold_agreement": f"{a}/{KNN_K}"}
        w.add(source="lexglue_ledgar", source_item=f"ledgar:test:{int(r['row'])}", header="Contract provision",
              text=text, qtype="choice", question=LEDGAR_Q, options=list(names), gold=name, card=None, meta=m)
    cb = Counter(l for _, l, _, _ in picked)
    report["ledgar"] = {"hf_id": LG_ID, "config": "ledgar", "license": LEDGAR_LICENSE,
                        "license_note": LEDGAR_LICENSE_NOTE, "split_used": "test", "n_items": len(picked),
                        "n_options": len(names), "question": LEDGAR_Q,
                        "class_balance": f"{len(cb)} distinct gold labels, max {max(cb.values())} items per label",
                        "gold_labels": dict(sorted(cb.items())), "allowed_gold_labels": allowed,
                        "allowed_1nn_self_agreement": {x: self_agree[x] for x in allowed},
                        "confusable_partners": partners, "excluded_gold_labels": excluded,
                        "data_edges": data_edges, "pool_after_filters": len(kept), "dropped": drops}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--with-definition-classification", action="store_true",
                    help="also add definition_classification (CC BY-SA 4.0, excluded by default)")
    args = ap.parse_args()

    meta = lb_meta()
    w, report = Writer(), {}

    lb_yesno(w, meta, "hearsay", 90, random.Random(SEED), "Fact pattern", "legalbench_hearsay", report,
             extra_meta=("slice",))
    report["hearsay"]["slice_balance"] = dict(Counter(r["meta"]["slice"] for r in w.rows
                                                      if r["meta"].get("task") == "hearsay"))
    report["hearsay"]["note"] = ("only 41 Yes items in the test split -> exact 41/41 balance. LegalBench labels "
                                 "party admissions as hearsay (FRE 801(d)(2) calls them non-hearsay); this matches "
                                 "the one-line definition given in the question, so kept.")

    ab_card = abercrombie_card(meta)
    lb_choice(w, meta, "abercrombie", 60, random.Random(SEED), "Mark", "legalbench_abercrombie",
              ABERCROMBIE_OPTIONS, ABERCROMBIE_Q, ab_card, report)
    report["abercrombie"]["note"] = "replaces function_of_decision_section (misaligned gold in the source file)"

    lb_choice(w, meta, "unfair_tos", 80, random.Random(SEED), "Clause", "legalbench_unfair_tos",
              UNFAIR_TOS_OPTIONS, UNFAIR_TOS_Q, UNFAIR_TOS_CARD, report, min_words=MIN_WORDS,
              keep_fn=unfair_tos_keep)

    lb_yesno(w, meta, "overruling", 40, random.Random(SEED), "Sentence", "legalbench_overruling", report,
             min_words=MIN_WORDS)
    report["overruling"]["note"] = "substitute for definition_classification (CC BY-SA 4.0)"
    if args.with_definition_classification:
        lb_yesno(w, meta, "definition_classification", 40, random.Random(SEED), "Sentence",
                 "legalbench_definition_classification", report, min_words=MIN_WORDS)

    cuad_all = sorted(t for t in meta if t.startswith("cuad_"))
    cuad = sorted(random.Random(SEED).sample(cuad_all, 8))
    for t in cuad:
        lb_yesno(w, meta, t, 10, random.Random(SEED), "Clause", "legalbench_cuad", report,
                 extra_meta=("document_name",), min_words=MIN_WORDS)

    ledgar(w, 60, random.Random(SEED), report)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w") as f:
        for r in w.rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    skipped = {"function_of_decision_section":
               "dropped: LegalBench test.tsv gold is shifted by one paragraph in many places (labels and Citation "
               "column misaligned); replaced by abercrombie"}
    if not args.with_definition_classification:
        skipped["definition_classification"] = "CC BY-SA 4.0, not CC BY 4.0 -> replaced by overruling"
    summary = {"part": PART, "track": TRACK, "out": str(OUT), "n_rows": len(w.rows), "n_calls": len(w.calls),
               "seed": SEED, "cuad_tasks_chosen": cuad, "skipped": skipped, "tasks": report}
    print(json.dumps(summary, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
