"""Build raw rows for CFPB Consumer Complaint narratives (product / issue-within-product).

Source: HF BEE-spoke-data/consumer-finance-complaints, config "has-text", split train (the only split),
        pinned revision 088cc7308d4afc2a880f2329d08e2f7a09188ec6 (a Feb 2024 pull of the CFPB
        Consumer Complaint Database). Copies of the HF card and CFPB terms are in breadth_src/cache/cfpb/.
Licence: CC0 1.0 (HF card "license: cc0-1.0"); the CFPB Consumer Complaint Database is a US-government
         work, public domain in the US with a worldwide CC0 1.0 waiver (github.com/cfpb/ccdb5-api TERMS.md,
         copied to cache/cfpb/TERMS.md; LICENSE copied to cache/cfpb/LICENSE_ccdb5-api).
Texts: consumer-written complaint narratives (published with consent, PII scrubbed to XXXX by CFPB).
Labels: product / sub-product / issue selected by the consumer on the CFPB complaint form (human).

Design:
- Only complaints with Date received < 2022-11-01 (avoid LLM-assisted narratives after ChatGPT).
- Task A "product" (all dates < cutoff): 9 current CFPB products; legacy (pre 2017-04-24) product names are
  merged into their successors (Credit card + Prepaid card -> Credit card or prepaid card, Bank account or
  service -> Checking or savings account, Money transfers + Virtual currency -> Money transfer...,
  Payday loan -> Payday/title/personal loan, Consumer Loan split by sub-product into Vehicle loan or lease
  vs Payday/title/personal loan, Credit reporting -> Credit reporting...). "Other financial service" and
  legacy "Cashing a check without an account" are dropped (no clean successor).
- Task B "issue within product" (2017-04-24 <= date < cutoff, i.e. the current issue taxonomy only):
  7 products, each with its own issue label set; credit-report issues filed under non-reporting products,
  catch-alls ("Other features, terms, or problems") and rare / renamed variants are excluded.
  Credit card issues use only credit-card sub-products (prepaid cards have a different issue list).
- Template letters: every narrative in the pool (all < cutoff) is split into sentences; a sentence of 12+
  words that occurs in 3+ different complaints is a template sentence. A candidate is dropped if it has 2+
  template sentences, 20%+ of its long sentences are template sentences, or its normalised first/last
  160 characters or full text occur in another complaint. Selected rows are also near-dup checked
  against each other (5-word shingle Jaccard > 0.5).
- Texts 150-4000 characters, redaction (XXXX) share <= 20% of characters.
- Label balance: round-robin, least-filled label first (credit reporting is capped by the balance).
- One row per complaint; no complaint appears in both tasks. soft = null (one consumer label).
"""
import collections, glob, hashlib, json, os, random, re

SEED = 20261101
N_MAX = 650
N_PRODUCT = 324
CUTOFF = "2022-11-01"
TAXO_START = "2017-04-24"
REPO = "BEE-spoke-data/consumer-finance-complaints"
REV = "088cc7308d4afc2a880f2329d08e2f7a09188ec6"
CONFIG = "has-text"
SHARDS = [f"has-text/train-0000{i}-of-00003.parquet" for i in range(3)]

HERE = os.path.dirname(os.path.abspath(__file__))
LEAN = os.path.dirname(HERE)
CACHE = os.path.join(HERE, "cache", "cfpb")
OUT = os.path.join(LEAN, "data", "v13_parts", "raw", "cfpb.jsonl")
DEFS_OUT = os.path.join(LEAN, "data", "v13_parts", "defs", "cfpb.json")

META_BASE = {"dataset": REPO, "config": CONFIG, "revision": REV,
             "licence": ("CC0 1.0 / US-government public domain (HF card license: cc0-1.0; "
                         "CFPB ccdb5-api TERMS.md: public domain in the US + CC0 1.0 worldwide waiver)"),
             "split": "train"}

MIN_LEN, MAX_LEN = 150, 4000

# ---------- Task A: product ----------
P_CR = "Credit reporting or credit repair"
P_DC = "Debt collection"
P_MO = "Mortgage"
P_CC = "Credit card or prepaid card"
P_CS = "Checking or savings account"
P_SL = "Student loan"
P_VL = "Vehicle loan or lease"
P_MT = "Money transfer, virtual currency, or money service"
P_PL = "Payday, title, or personal loan"
PRODUCTS = [P_CR, P_DC, P_MO, P_CC, P_CS, P_SL, P_VL, P_MT, P_PL]
PRODUCT_MAP = {
    "Credit reporting, credit repair services, or other personal consumer reports": P_CR,
    "Credit reporting": P_CR,
    "Debt collection": P_DC,
    "Mortgage": P_MO,
    "Credit card or prepaid card": P_CC, "Credit card": P_CC, "Prepaid card": P_CC,
    "Checking or savings account": P_CS, "Bank account or service": P_CS,
    "Student loan": P_SL,
    "Vehicle loan or lease": P_VL,
    "Money transfer, virtual currency, or money service": P_MT, "Money transfers": P_MT,
    "Virtual currency": P_MT,
    "Payday loan, title loan, or personal loan": P_PL, "Payday loan": P_PL,
}
CONSUMER_LOAN_SUB = {"Vehicle loan": P_VL, "Vehicle lease": P_VL, "Installment loan": P_PL,
                     "Title loan": P_PL, "Personal line of credit": P_PL, "Pawn loan": P_PL}


def map_product(prod, sub):
    if prod == "Consumer Loan":
        return CONSUMER_LOAN_SUB.get(sub)
    if prod == "Bank account or service" and sub == "Cashing a check without an account":
        return None
    return PRODUCT_MAP.get(prod)


# ---------- Task B: issue within product ----------
INV = "Problem with a credit reporting company's investigation"
ISSUES = {  # source product -> {source issue: option name}
    "Debt collection": {k: k for k in [
        "Attempts to collect debt not owed", "Written notification about debt",
        "Took or threatened to take negative or legal action", "False statements or representation",
        "Communication tactics", "Threatened to contact someone or share information improperly"]},
    "Mortgage": {k: k for k in [
        "Trouble during payment process", "Struggling to pay mortgage",
        "Applying for a mortgage or refinancing an existing mortgage", "Closing on a mortgage"]},
    "Checking or savings account": {k: k for k in [
        "Managing an account", "Closing an account", "Opening an account",
        "Problem with a lender or other company charging your account",
        "Problem caused by your funds being low"]},
    "Credit reporting, credit repair services, or other personal consumer reports": {
        "Incorrect information on your report": "Incorrect information on your report",
        "Problem with a credit reporting company's investigation into an existing problem": INV,
        "Improper use of your report": "Improper use of your report",
        "Unable to get your credit report or credit score": "Unable to get your credit report or credit score",
        "Problem with fraud alerts or security freezes": "Problem with fraud alerts or security freezes",
        "Credit monitoring or identity theft protection services":
            "Credit monitoring or identity theft protection services"},
    "Vehicle loan or lease": {k: k for k in [
        "Managing the loan or lease", "Problems at the end of the loan or lease",
        "Struggling to pay your loan", "Getting a loan or lease"]},
    "Student loan": {k: k for k in [
        "Dealing with your lender or servicer", "Struggling to repay your loan", "Getting a loan"]},
    "Credit card or prepaid card": {k: k for k in [
        "Problem with a purchase shown on your statement", "Fees or interest", "Getting a credit card",
        "Problem when making payments", "Closing your account",
        "Advertising and marketing, including promotional offers", "Trouble using your card",
        "Struggling to pay your bill"]},
}
CC_SUBS = {"General-purpose credit card or charge card", "Store credit card"}
ISSUE_Q = {
    "Debt collection": "Which issue is this debt collection complaint about?",
    "Mortgage": "Which issue is this mortgage complaint about?",
    "Checking or savings account": "Which issue is this checking or savings account complaint about?",
    "Credit reporting, credit repair services, or other personal consumer reports":
        "Which issue is this credit reporting complaint about?",
    "Vehicle loan or lease": "Which issue is this vehicle loan or lease complaint about?",
    "Student loan": "Which issue is this student loan complaint about?",
    "Credit card or prepaid card": "Which issue is this credit card complaint about?",
}
PRODUCT_Q = "Which financial product is this consumer complaint about?"


# ---------- text utils ----------
XRUN = re.compile(r"X{2,}")
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")


def norm(s):
    s = XRUN.sub(" x ", s).lower()
    s = re.sub(r"\d", "0", s)
    s = re.sub(r"[^a-z0 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def h8(s):
    return int.from_bytes(hashlib.blake2b(s.encode("utf-8"), digest_size=8).digest(), "big")


def long_sent_hashes(text):
    out = set()
    for sent in SENT_SPLIT.split(text):
        n = norm(sent)
        if n.count(" ") >= 11:
            out.add(h8(n))
    return out


def x_share(text):
    return sum(len(m) for m in XRUN.findall(text)) / max(1, len(text))


def shingles(n):
    w = n.split()
    return {" ".join(w[i:i + 5]) for i in range(max(1, len(w) - 4))}


# ---------- load (streamed; texts kept only for pool prefixes) ----------
META_COLS = ["Date received", "Product", "Sub-product", "Issue", "Complaint ID"]
TXT = "Consumer complaint narrative"
POOL_PREFIX = 600  # candidates kept per label (far more than the ~40 needed)


def shard_paths():
    from huggingface_hub import hf_hub_download
    return [hf_hub_download(REPO, f, repo_type="dataset", revision=REV) for f in SHARDS]


def iter_batches(cols):
    import pyarrow.parquet as pq
    for path in shard_paths():
        pf = pq.ParquetFile(path)
        for b in pf.iter_batches(batch_size=50000, columns=cols):
            d = b.to_pydict()
            yield d


def main():
    import numpy as np
    rng = random.Random(SEED)

    # pass 1: metadata + template statistics (hashes only)
    meta = []  # (complaint_id, date, product, sub, issue)
    from array import array
    sent_h, head_h, tail_h, full_h = array("Q"), array("Q"), array("Q"), array("Q")
    for d in iter_batches(META_COLS + [TXT]):
        for k in range(len(d["Complaint ID"])):
            t, dt = d[TXT][k], d["Date received"][k]
            if t is None or dt is None or dt >= CUTOFF:
                continue
            meta.append((d["Complaint ID"][k], dt, d["Product"][k], d["Sub-product"][k], d["Issue"][k]))
            n = norm(t)
            head_h.append(h8(n[:160])); tail_h.append(h8(n[-160:])); full_h.append(h8(n))
            sent_h.extend(long_sent_hashes(t))
            if len(meta) % 200000 == 0:
                print(f"  hashed {len(meta)}", flush=True)
    print(f"pool (< {CUTOFF}, has narrative): {len(meta)}", flush=True)

    def counter(arr):
        u, c = np.unique(np.frombuffer(arr, dtype=np.uint64), return_counts=True)
        return u, c

    def lookup(uc, x):
        u, c = uc
        j = np.searchsorted(u, np.uint64(x))
        return int(c[j]) if j < len(u) and u[j] == np.uint64(x) else 0

    sent_uc = counter(sent_h); del sent_h
    head_uc, tail_uc, full_uc = counter(head_h), counter(tail_h), counter(full_h)
    del head_h, tail_h, full_h

    # deterministic order: sort by complaint id, then shuffle
    meta.sort(key=lambda m: m[0])
    ids = [m[0] for m in meta]; dates = [m[1] for m in meta]; prods = [m[2] for m in meta]
    subs = [m[3] for m in meta]; issues = [m[4] for m in meta]
    del meta
    order = list(range(len(ids)))
    rng.shuffle(order)
    prod_pool = collections.defaultdict(list)
    issue_pool = collections.defaultdict(lambda: collections.defaultdict(list))
    for i in order:
        p = map_product(prods[i], subs[i])
        if p is not None and len(prod_pool[p]) < POOL_PREFIX:
            prod_pool[p].append(i)
        if dates[i] >= TAXO_START and prods[i] in ISSUES:
            if prods[i] == "Credit card or prepaid card" and subs[i] not in CC_SUBS:
                continue
            lab = ISSUES[prods[i]].get(issues[i])
            if lab is not None and len(issue_pool[prods[i]][lab]) < POOL_PREFIX:
                issue_pool[prods[i]][lab].append(i)

    # pass 2: fetch texts for pool members only
    need = {ids[i]: i for pl in prod_pool.values() for i in pl}
    need.update({ids[i]: i for dd in issue_pool.values() for pl in dd.values() for i in pl})
    texts = {}
    for d in iter_batches(["Complaint ID", TXT]):
        for cid, t in zip(d["Complaint ID"], d[TXT]):
            if cid in need:
                texts[need[cid]] = t
    print(f"texts fetched for pool prefixes: {len(texts)}", flush=True)

    drop = collections.Counter()

    def ok_text(t):
        if not (MIN_LEN <= len(t) <= MAX_LEN):
            drop["length"] += 1; return False
        if x_share(t) > 0.20:
            drop["redaction"] += 1; return False
        n = norm(t)
        if len(n) < 100:
            drop["too_little_text"] += 1; return False
        if (lookup(full_uc, h8(n)) > 1 or lookup(head_uc, h8(n[:160])) > 1
                or lookup(tail_uc, h8(n[-160:])) > 1):
            drop["dup_or_template_edge"] += 1; return False
        hs = long_sent_hashes(t)
        shared = sum(1 for x in hs if lookup(sent_uc, x) >= 3)
        if shared >= 2 or (hs and shared / len(hs) >= 0.2):
            drop["template_sentences"] += 1; return False
        return True

    used = set()
    chosen_sh = []
    rows = []

    def take(pool_list, ptr):
        """advance pointer to next usable record; return index or None"""
        while ptr[0] < len(pool_list):
            i = pool_list[ptr[0]]; ptr[0] += 1
            if i in used:
                continue
            t = texts[i]
            if not ok_text(t):
                continue
            sh = shingles(norm(t))
            if any(len(sh & s) / max(1, len(sh | s)) > 0.5 for s in chosen_sh):
                drop["near_dup_selected"] += 1; continue
            used.add(i); chosen_sh.append(sh)
            return i
        return None

    def round_robin(pools, labels, n_total, emit):
        cap = int(n_total * 0.40) if len(labels) > 2 else n_total
        counts = collections.Counter()
        ptrs = {l: [0] for l in labels}
        exhausted = set()
        while sum(counts.values()) < n_total and len(exhausted) < len(labels):
            l = min((x for x in labels if x not in exhausted), key=lambda x: (counts[x], labels.index(x)))
            if counts[l] >= cap:
                exhausted.add(l); continue
            i = take(pools[l], ptrs[l])
            if i is None:
                exhausted.add(l); continue
            counts[l] += 1
            emit(i, l)
        return counts

    # Task B first (smaller pools), then Task A
    n_issue = N_MAX - N_PRODUCT
    n_labels = {p: len(set(ISSUES[p].values())) for p in ISSUES}
    tot_labels = sum(n_labels.values())
    alloc, acc = {}, 0
    for k, p in enumerate(ISSUES):
        alloc[p] = (n_issue - acc) if k == len(ISSUES) - 1 else round(n_issue * n_labels[p] / tot_labels)
        acc += alloc[p]

    issue_counts = {}
    for p in ISSUES:
        labs = list(dict.fromkeys(ISSUES[p].values()))

        def emit(i, l, p=p, labs=labs):
            rows.append({"key": "cfpb", "rid": f"complaint-{ids[i]}", "state": texts[i],
                         "instructions": ISSUE_Q[p], "options": labs, "gold": l, "soft": None,
                         "meta": dict(META_BASE, task="issue", product=p, date_received=dates[i],
                                      orig_label={"product": prods[i], "sub_product": subs[i],
                                                  "issue": issues[i]})})
        issue_counts[p] = round_robin(issue_pool[p], labs, alloc[p], emit)

    def emit_prod(i, l):
        rows.append({"key": "cfpb", "rid": f"complaint-{ids[i]}", "state": texts[i],
                     "instructions": PRODUCT_Q, "options": list(PRODUCTS), "gold": l, "soft": None,
                     "meta": dict(META_BASE, task="product", date_received=dates[i],
                                  orig_label={"product": prods[i], "sub_product": subs[i],
                                              "issue": issues[i]})})
    prod_counts = round_robin(prod_pool, PRODUCTS, N_MAX - len(rows), emit_prod)

    rng.shuffle(rows)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # report
    print(f"wrote {len(rows)} rows -> {OUT}")
    print("drops (over examined candidates):", dict(drop))
    print(f"\nTask product: {sum(prod_counts.values())}")
    for l in PRODUCTS:
        print(f"  {prod_counts[l]:4d}  {l}")
    legacy = sum(1 for r in rows if r["meta"]["task"] == "product" and r["meta"]["orig_label"]["product"]
                 not in {"Credit reporting, credit repair services, or other personal consumer reports",
                         "Debt collection", "Mortgage", "Credit card or prepaid card", "Checking or savings account",
                         "Student loan", "Vehicle loan or lease",
                         "Money transfer, virtual currency, or money service",
                         "Payday loan, title loan, or personal loan"})
    print(f"  (legacy product names merged: {legacy})")
    for p in ISSUES:
        c = issue_counts[p]
        print(f"\nTask issue / {p}: {sum(c.values())} (alloc {alloc[p]})")
        for l, n in sorted(c.items(), key=lambda x: -x[1]):
            print(f"  {n:4d}  {l}")
    lens = sorted(len(r["state"]) for r in rows)
    print(f"\nsoft coverage: {sum(r['soft'] is not None for r in rows)}/{len(rows)}")
    print(f"length chars: min {lens[0]} p25 {lens[len(lens)//4]} median {lens[len(lens)//2]} "
          f"p75 {lens[3*len(lens)//4]} max {lens[-1]} mean {sum(lens)/len(lens):.0f}")
    yrs = collections.Counter(r["meta"]["date_received"][:4] for r in rows)
    print("years:", dict(sorted(yrs.items())))


if __name__ == "__main__":
    main()
