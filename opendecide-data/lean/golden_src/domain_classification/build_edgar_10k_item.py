"""Build raw rows for edgar_10k_item (EDGAR-CORPUS, Loukas et al., ECONLP 2021): which Form 10-K item a passage is from.

Source : HF eloukas/edgar-corpus (the first author's account), file 2019/train.jsonl ONLY (validate/test never read),
         revision 7e90f0f342569b35213445f809cfaf3b91f9964f (full-file LFS sha256 9f05959f...). To keep the download
         lean only the first PREFIX bytes are fetched (HTTP Range) and only complete JSON lines are parsed; the
         prefix's sha256 is pinned.
Licence: Apache-2.0 (license field of the dataset card README.md at the pinned revision; card: "EDGAR data is publicly
         available"). Texts are annual reports filed with the US SEC (public EDGAR records).
Texts  : human-written 10-K filings for fiscal year 2019, split into items by the authors' EDGAR-CRAWLER.
Labels : the 10-K item the paragraph sits in (document structure written by the filer). Only sections whose text
         starts with the matching "Item N" heading are used (guards against crawler mis-splits).
Paragraphs: 250-1500 chars, starts with a capital, no cross-references to item names / "Item N" / proxy statement /
         "incorporated by reference", digit share <= 12% (no tables), not repeated in another item of the same filing, not
         cross-item boilerplate (> 20% of its word 8-grams occur in paragraphs of a different item in any filing),
         near-duplicates across filings dropped (5-gram MinHash Jaccard >= 0.6). Paragraphs sharing any 12-gram with lex_glue
         LEDGAR / SCOTUS or any LegalBench task dropped (reviewer fix). <= 5 candidate paragraphs per filing (distinct items).
         Noise filter: out-of-fold TF-IDF logistic regression (grouped by filing); a row is dropped (never relabelled)
         when P(its item) < 0.05 while another item has P >= 0.6 (confident disagreement = likely crawler noise).
Tasks  : 14-way choice (Items 1, 1A, 2, 3, 5, 7, 7A, 8, 9A, 10, 11, 12, 13, 14) and yes/no "Is this passage from
         Item Y?" (no-rows ask about a confusable item Y, chosen so that each asked item's yes share stays near 50%). One row per paragraph. Soft: null. Edge 'numeric' when the passage has >= 2 amounts
         ($, %, million/billion, basis points).
Deterministic (seed 20260929). CPU only.
"""
import collections
import json
import random
import re
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

KEY = "edgar_10k_item"
SEED = 20260929
REV = "7e90f0f342569b35213445f809cfaf3b91f9964f"
FULL_SHA = "9f05959fe52a99536c474c8cf61f2197e9bbce6c16b2a1c2dd4a81622e0a8d91"
PREFIX = 400_000_000
PREFIX_SHA = "82196805619fdde2df416a1c3db5e99725b352b6689af3022e42dbec3dc10424"
N_CHOICE = 3600
N_YN = 1600
CACHE = C.CACHE / "edgar"
LICENCE = (f"Apache-2.0 (license field of https://huggingface.co/datasets/eloukas/edgar-corpus/blob/{REV}/README.md); "
           "texts are public SEC EDGAR 10-K filings")
ITEMS = {  # section key: (option name, heading regex, definition)
    "1": ("Item 1 - Business", r"item\s*1\b(?!\s*[ab0-9])",
          "Describes what the company does: its history, products and services, segments, customers, markets, "
          "competition, suppliers, intellectual property, employees and the regulation it operates under."),
    "1A": ("Item 1A - Risk Factors", r"item\s*1a\b",
           "Lists material risks and uncertainties, phrased as what could go wrong and how it could adversely "
           "affect the business, results, or the stock (not a report of actual results)."),
    "2": ("Item 2 - Properties", r"item\s*2\b",
          "Describes the physical properties the company owns or leases: offices, plants, stores, land, mines or "
          "reserves, with locations, sizes, uses and adequacy."),
    "3": ("Item 3 - Legal Proceedings", r"item\s*3\b",
          "Describes pending or threatened lawsuits, government investigations, regulatory or environmental "
          "proceedings involving the company, and their status."),
    "5": ("Item 5 - Market for Common Equity", r"item\s*5\b",
          "Covers the company's stock: where it trades, ticker, holders of record, dividend policy, share "
          "repurchases, unregistered sales of equity and the stock performance graph."),
    "7": ("Item 7 - MD&A", r"item\s*7\b(?!\s*a)",
          "Management's discussion and analysis: explains period results and why they changed, segment "
          "performance, liquidity, cash flows, capital resources, outlook, and the judgments behind critical "
          "accounting estimates."),
    "7A": ("Item 7A - Market Risk Disclosures", r"item\s*7a\b",
           "Quantifies exposure to market risks (interest-rate, foreign-currency, commodity, equity price), "
           "hedging and derivatives, often with sensitivity figures such as the effect of a 1% rate change."),
    "8": ("Item 8 - Financial Statements and Notes", r"item\s*8\b",
          "The audited financial statements: the auditor's report and the notes stating accounting policies and "
          "detailing balances, debt, leases, taxes, equity and other line items (rules and amounts, not management's "
          "narrative on performance)."),
    "9A": ("Item 9A - Controls and Procedures", r"item\s*9a\b",
           "Management's evaluation of disclosure controls and internal control over financial reporting, the "
           "framework used (e.g. COSO), material weaknesses and changes in controls."),
    "10": ("Item 10 - Directors, Officers and Governance", r"item\s*10\b",
           "Identifies directors and executive officers with their backgrounds, board committees, the code of "
           "ethics and other corporate-governance matters."),
    "11": ("Item 11 - Executive Compensation", r"item\s*11\b",
           "Describes how executives and directors are paid: salary, bonus, equity awards, employment and "
           "severance agreements, and compensation tables or philosophy."),
    "12": ("Item 12 - Security Ownership", r"item\s*12\b",
           "Reports who beneficially owns the company's shares (major holders, directors, officers) and securities "
           "authorised under equity compensation plans."),
    "13": ("Item 13 - Related Transactions and Director Independence", r"item\s*13\b",
           "Describes transactions between the company and its insiders or their affiliates (related-party "
           "dealings, loans, leases) and which directors are independent."),
    "14": ("Item 14 - Principal Accountant Fees", r"item\s*14\b",
           "Reports fees paid to the independent auditor (audit, audit-related, tax, other) and the audit "
           "committee's pre-approval policies."),
}
CONFUSE = {"1": ["1A", "7", "2"], "1A": ["7", "1", "7A"], "2": ["1", "7"], "3": ["8", "1A"], "5": ["7", "12"],
           "7": ["8", "1A", "7A", "1"], "7A": ["7", "1A", "8"], "8": ["7", "7A"], "9A": ["8", "14"],
           "10": ["11", "13"], "11": ["10", "12"], "12": ["11", "5"], "13": ["10", "11"], "14": ["9A", "13"]}
XREF = re.compile(
    r"\bitem\s*\d|risk factors|management[’'`s]*\s+discussion|legal proceedings|controls and procedures|"
    r"executive compensation|security ownership|related transactions|principal account|market risk|"
    r"financial statements and supplementary|proxy statement|incorporated (herein )?by reference|"
    r"market for (the )?registrant|unresolved staff|directors, executive officers|form 10-k|this report|annual report",
    re.I)
Q_CHOICE = "Which item of a company's Form 10-K annual report does this passage come from?"


def fetch_prefix():
    path = CACHE / "2019_train_prefix.jsonl"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        url = f"https://huggingface.co/datasets/eloukas/edgar-corpus/resolve/{REV}/2019/train.jsonl"
        with requests.get(url, headers={"Range": f"bytes=0-{PREFIX - 1}"}, stream=True, timeout=300) as r:
            r.raise_for_status()
            with open(path, "wb") as f:
                for b in r.iter_content(1 << 20):
                    f.write(b)
    sha = C.sha256_file(path)
    if PREFIX_SHA and sha != PREFIX_SHA:
        sys.exit(f"sha256 mismatch {sha}")
    return path, sha


def paragraphs(key, text):
    lines = [ln.strip() for ln in text.split("\n")]
    if not lines or not re.match(r"^\s*" + ITEMS[key][1], lines[0], re.I):
        return None
    out = []
    for ln in lines[1:]:
        if not (250 <= len(ln) <= 1500) or not ln[0].isupper():
            continue
        if XREF.search(ln):
            continue
        if sum(ch.isdigit() for ch in ln) / len(ln) > 0.12:
            continue
        if not re.search(r"[.;:]\s*$", ln):
            continue
        out.append(ln)
    return out


def main():
    path, psha = fetch_prefix()
    print("prefix sha256:", psha)
    filings = []
    with open(path, "rb") as f:
        for raw in f:
            try:
                filings.append(json.loads(raw))
            except Exception:
                break  # the last, cut-off line
    print("complete filings in prefix:", len(filings))
    rng = random.Random(SEED)
    stats = collections.Counter()
    per_filing = []
    for d in filings:
        paras = {}
        for k in ITEMS:
            t = d.get(f"section_{k}") or ""
            ps = paragraphs(k, t)
            if ps is None:
                stats[f"bad_heading_{k}"] += 1 if t else 0
                continue
            paras[k] = ps
        cnt = collections.Counter(C.norm(p) for ps in paras.values() for p in ps)
        paras = {k: [p for p in ps if cnt[C.norm(p)] == 1] for k, ps in paras.items()}
        paras = {k: ps for k, ps in paras.items() if ps}
        if paras:
            per_filing.append((d["filename"], d["cik"], paras))
    # cross-item boilerplate filter: drop a paragraph if > 20% of its word 8-grams also occur in paragraphs that sit
    # in a DIFFERENT item (any filing) -- e.g. accounting-policy text repeated in MD&A and in the notes.
    gram_items = collections.defaultdict(set)
    for _, _, paras in per_filing:
        for k, ps in paras.items():
            for p in ps:
                for g in C.ngrams(p, 8):
                    gram_items[hash(g)].add(k)
    cross = 0
    for n_, (fname, cik, paras) in enumerate(per_filing):
        keep = {}
        for k, ps in paras.items():
            kp = []
            for p in ps:
                gs = C.ngrams(p, 8)
                shared = sum(1 for g in gs if gram_items[hash(g)] - {k})
                if gs and shared / len(gs) > 0.2:
                    cross += 1
                    continue
                kp.append(p)
            if kp:
                keep[k] = kp
        per_filing[n_] = (fname, cik, keep)
    stats["cross_item_boilerplate"] = cross
    per_filing = [x for x in per_filing if x[2]]
    per_filing.sort()
    rng.shuffle(per_filing)
    # assign up to 4 items per filing, always preferring the globally scarcest items
    taken = collections.Counter()
    nd = C.NearDup(0.6)
    recs = []
    for fname, cik, paras in per_filing:
        n = 0
        for k in sorted(paras, key=lambda k: (taken[k], rng.random())):
            if n >= 5:
                break
            ps = paras[k][:]
            rng.shuffle(ps)
            for p in ps:
                if not nd.seen(p):
                    recs.append({"file": fname, "cik": cik, "item": k, "text": p})
                    taken[k] += 1
                    n += 1
                    break
    print("candidates per item:", dict(sorted(taken.items())), dict(stats))
    # Reviewer fix (2026-09-29): drop any selected paragraph sharing a 12-gram with lex_glue LEDGAR (OHS-1 source; SEC
    # EDGAR contract provisions), lex_glue SCOTUS (forbidden label-NLI task) or any LegalBench task (all forbidden).
    bad = C.forbidden_legal_hits({j: [r["text"]] for j, r in enumerate(recs)},
                                 ["lexglue_ledgar", "lexglue_scotus", "legalbench_all"])
    recs = [r for j, r in enumerate(recs) if j not in bad]
    print("forbidden-legal 12-gram overlap dropped:", len(bad))
    # confident-disagreement noise filter (labels are never changed, rows are only dropped): out-of-fold TF-IDF
    # logistic regression grouped by filing, trained on the selected paragraphs plus up to 2 extra paragraphs per
    # item per filing; drop a selected paragraph if P(its item) < 0.05 while another item has P >= 0.6.
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GroupKFold
    import numpy as np
    sel = {(r["file"], r["text"]) for r in recs}
    extra = []
    for fname, cik, paras in per_filing:
        for k, ps in paras.items():
            for p in [p for p in ps if (fname, p) not in sel][:2]:
                extra.append({"file": fname, "item": k, "text": p})
    allr = recs + extra
    Xv = TfidfVectorizer(sublinear_tf=True, ngram_range=(1, 2), min_df=3, max_features=200000).fit_transform(
        [r["text"] for r in allr])
    y = np.array([r["item"] for r in allr])
    groups = np.array([r["file"] for r in allr])
    labels = sorted(ITEMS)
    oof = np.zeros((len(recs), len(labels)))
    for tr, te in GroupKFold(n_splits=5).split(Xv, y, groups):
        clf = LogisticRegression(max_iter=2000, C=4.0).fit(Xv[tr], y[tr])
        te_sel = te[te < len(recs)]
        if len(te_sel):
            pr = clf.predict_proba(Xv[te_sel])
            oof[te_sel] = pr[:, [list(clf.classes_).index(c) for c in labels]]
    flagged = 0
    kept = []
    for i, r in enumerate(recs):
        pt = oof[i, labels.index(r["item"])]
        if pt < 0.05 and oof[i].max() >= 0.6:
            flagged += 1
            continue
        kept.append(r)
    print(f"noise filter: dropped {flagged} of {len(recs)} (oof accuracy "
          f"{np.mean([labels[oof[i].argmax()] == r['item'] for i, r in enumerate(recs)]):.3f})")
    recs = kept
    by_item = collections.defaultdict(list)
    for r in recs:
        by_item[r["item"]].append(r)
    for k in by_item:
        rng.shuffle(by_item[k])
    total = N_CHOICE + N_YN
    cap = total // len(ITEMS) + 1
    # take round-robin (equal share) up to the total
    pool, i = [], 0
    keys = sorted(ITEMS, key=lambda k: len(by_item[k]))
    while len(pool) < total and any(by_item[k] for k in keys):
        k = keys[i % len(keys)]
        if by_item[k] and sum(1 for r in pool if r["item"] == k) < cap * 2:
            pool.append(by_item[k].pop())
        i += 1
    rng.shuffle(pool)
    rows = []
    n_yes = n_no = 0
    ask_yes, ask_no = collections.Counter(), collections.Counter()
    opts = sorted(v[0] for v in ITEMS.values())
    for j, r in enumerate(pool):
        k = r["item"]
        base = {"key": KEY, "rid": f"edgar2019-{r['file']}-{k}", "soft": None}
        meta = {"dataset": "eloukas/edgar-corpus (EDGAR-CORPUS)", "revision": f"hf:{REV}; file 2019/train.jsonl "
                f"(full sha256:{FULL_SHA}); prefix bytes 0-{PREFIX - 1} sha256:{psha}", "licence": LICENCE,
                "split": "train", "orig_label": {"section": f"section_{k}", "cik": r["cik"], "filename": r["file"]},
                "family": C.FAMILY, "seed": SEED,
                "edge": "numeric" if len(re.findall(r"\$\s?\d[\d,.]*|\d[\d,.]*\s?%|\d[\d,.]*\s(?:million|billion|basis points)",
                                                    r["text"])) >= 2 else None}
        if j < N_YN:
            want_yes = n_yes <= n_no
            if want_yes:
                asked = k
            else:
                # keep every asked item's yes share near 50%: among the confusable items take the one most in
                # deficit of "no" rows; if none is in deficit, any other item that is
                pool_c = [c for c in CONFUSE[k] if ask_yes[c] - ask_no[c] > 0] or \
                    [c for c in sorted(ITEMS) if c != k and ask_yes[c] - ask_no[c] > 0] or CONFUSE[k]
                asked = max(pool_c, key=lambda c: (ask_yes[c] - ask_no[c], rng.random()))
            name = ITEMS[asked][0]
            gold = "yes" if asked == k else "no"
            (ask_yes if gold == "yes" else ask_no)[asked] += 1
            n_yes += gold == "yes"
            n_no += gold == "no"
            rows.append({**base, "state": r["text"],
                         "instructions": f"Does this passage come from {name} of a company's Form 10-K annual report?",
                         "options": ["yes", "no"], "gold": gold,
                         "meta": {**meta, "config": f"yes/no asked={asked}", "defs": f"item{asked}",
                                  "orig_label": {**meta["orig_label"], "asked_item": asked}}})
        else:
            rows.append({**base, "state": r["text"], "instructions": Q_CHOICE, "options": opts,
                         "gold": ITEMS[k][0], "meta": {**meta, "config": "choice 14 items"}})
    rng.shuffle(rows)
    C.write_rows(KEY, rows)
    C.write_defs(KEY, {v[0]: v[2] for v in ITEMS.values()})
    for k, (name, _, d) in ITEMS.items():
        others = ", ".join(ITEMS[c][0] for c in CONFUSE[k])
        C.write_defs(f"{KEY}__item{k}", {
            "yes": f"The passage sits in {name}: {d}",
            "no": f"The passage sits in a different item of the 10-K (for example {others}), not in {name}.",
        })
    C.summary(rows)
    print(collections.Counter(r["meta"]["orig_label"]["section"] for r in rows))


if __name__ == "__main__":
    main()
