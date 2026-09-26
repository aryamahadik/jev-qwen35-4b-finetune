"""OHS-1 part "factsci" (track U): science QA + contrastive fact checking.

(a) PubMedQA (qiaojin/PubMedQA, config pqa_labeled): 150 items from the OFFICIAL
    500-question test set (PMIDs in github.com/pubmedqa/pubmedqa data/test_ground_truth.json;
    the HF config only exposes a single 'train' split holding all 1000 labeled items).
    Choice yes / no / maybe, stratified 50/50/50. State = question + structured abstract
    WITHOUT the conclusion (long_answer), i.e. the paper's reasoning-required setting.
(b) VitaminC (tals/vitaminc, test split): 100 contrastive pairs (200 rows). A pair is two rows
    of the same case_id with an identical claim, different evidence and different labels
    (the dataset's own case pairing). Choice SUPPORTS / REFUTES / NOT ENOUGH INFO.

Re-runnable: deterministic (seed 20260927); overwrites data/ohs_parts/factsci.jsonl.
No LLM text; gold labels and label names come from the datasets.
"""
import json
import os
import random
import re
import sys
import unicodedata
from collections import Counter, defaultdict

import pandas as pd
import requests
from huggingface_hub import hf_hub_download

SEED = 20260927
PART = "factsci"
TRACK = "U"
HERE = os.path.dirname(os.path.abspath(__file__))
LEAN = os.path.dirname(HERE)
OUT_DIR = os.path.join(LEAN, "data", "ohs_parts")
OUT = os.path.join(OUT_DIR, f"{PART}.jsonl")
REL_OUT = os.path.join(OUT_DIR, f"{PART}_relations.jsonl")
CACHE = os.path.join(HERE, "cache")
MIN_CHARS, MAX_CHARS = 20, 6000

N_PUBMEDQA = 150
N_VITC_PAIRS = 100

PUBMEDQA_GT_URL = "https://raw.githubusercontent.com/pubmedqa/pubmedqa/master/data/test_ground_truth.json"
PUBMEDQA_REV = "9001f2853fb87cab8d220904e0de81ac6973b318"
VITC_REV = "be6febb761b0b2807687e61e0b5282e459df2fa0"

VITC_LABELS = ["SUPPORTS", "REFUTES", "NOT ENOUGH INFO"]
# Schuster et al. 2021 (NAACL), Sec. 4: rel(c, s) "can either support c (SUP), refute it (REF),
# or not contain enough information (NEI)". Card lines restate that definition per label.
VITC_CARD = (
    "- SUPPORTS: the observed evidence supports the claim\n"
    "- REFUTES: the observed evidence refutes the claim\n"
    "- NOT ENOUGH INFO: the observed evidence does not contain enough information"
)


def norm(t):
    t = unicodedata.normalize("NFKC", t).lower()
    t = re.sub(r"[^\w\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def ok_len(t):
    return MIN_CHARS <= len(t) <= MAX_CHARS


def pubmedqa_test_ids():
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, "pubmedqa_test_ground_truth.json")
    if not os.path.exists(path):
        r = requests.get(PUBMEDQA_GT_URL, timeout=60)
        r.raise_for_status()
        with open(path, "w") as f:
            f.write(r.text)
    with open(path) as f:
        gt = json.load(f)
    assert len(gt) == 500, len(gt)
    return {int(k): v for k, v in gt.items()}


def build_pubmedqa(rng):
    p = hf_hub_download("qiaojin/PubMedQA", "pqa_labeled/train-00000-of-00001.parquet",
                        repo_type="dataset", revision=PUBMEDQA_REV)
    df = pd.read_parquet(p)
    gt = pubmedqa_test_ids()
    df = df[df.pubid.isin(gt.keys())].copy()
    assert len(df) == 500, len(df)
    mism = int((df.pubid.map(gt) != df.final_decision).sum())
    assert mism == 0, f"{mism} PubMedQA labels disagree with official test ground truth"

    items, seen, drops = [], set(), Counter()
    for r in df.sort_values("pubid").itertuples():
        ctx, labs = list(r.context["contexts"]), list(r.context["labels"])
        paras = [f"{l}: {c.strip()}" if l else c.strip() for c, l in zip(ctx, labs)]
        abstract = "\n\n".join(paras)
        state = f"Question:\n{r.question.strip()}\n\nAbstract:\n{abstract}"
        if not ok_len(state):
            drops["length"] += 1
            continue
        k = norm(abstract)
        if k in seen:
            drops["duplicate"] += 1
            continue
        seen.add(k)
        items.append(dict(pubid=int(r.pubid), question=r.question.strip(), state=state,
                          gold=r.final_decision, meshes=list(r.context["meshes"]),
                          section_labels=labs))

    by = defaultdict(list)
    for it in items:
        by[it["gold"]].append(it)
    labels = ["yes", "no", "maybe"]
    avail = {l: len(by[l]) for l in labels}
    # Balanced thirds (max class share 33.3% <= 40%); if a class is short, others fill up to the 40% cap.
    cap = int(0.4 * N_PUBMEDQA)
    quota = {l: min(avail[l], N_PUBMEDQA // 3) for l in labels}
    while sum(quota.values()) < N_PUBMEDQA:
        grow = [l for l in labels if quota[l] < min(avail[l], cap)]
        if not grow:
            break
        for l in grow:
            if sum(quota.values()) < N_PUBMEDQA:
                quota[l] += 1
    chosen = []
    for l in labels:
        pool = sorted(by[l], key=lambda x: x["pubid"])
        chosen += rng.sample(pool, quota[l])
    rng.shuffle(chosen)
    info = dict(pool_after_filters=len(items), available_by_class=avail, drops=dict(drops))
    return chosen, info


def vitc_state(evidence, claim):
    return f"Evidence:\n{evidence.strip()}\n\nClaim:\n{claim}"


def build_vitaminc(rng):
    p = hf_hub_download("tals/vitaminc", "test.jsonl", repo_type="dataset", revision=VITC_REV)
    df = pd.read_json(p, lines=True, dtype={"case_id": str, "wiki_revision_id": str, "unique_id": str})
    for c in ("claim", "evidence"):
        # U+FFFD is an encoding artefact in the source (usually a lost non-breaking space).
        df[c] = df[c].str.replace("\ufffd", " ", regex=False)

    pairs, drops = [], Counter()
    for (cid, claim), sub in df.groupby(["case_id", "claim"], sort=True):
        if len(sub) != 2:
            if len(sub) > 2:
                drops["claim_group_size_gt2"] += 1
            continue
        a, b = sub.sort_values("unique_id").to_dict("records")
        if a["label"] == b["label"]:
            continue
        if norm(a["evidence"]) == norm(b["evidence"]):
            drops["same_evidence"] += 1
            continue
        if not (ok_len(claim.strip()) and ok_len(a["evidence"]) and ok_len(b["evidence"])):
            drops["length"] += 1
            continue
        combo = tuple(sorted([a["label"], b["label"]], key=VITC_LABELS.index))
        pairs.append(dict(case_id=cid, claim=claim.strip(), rows=[a, b], combo=combo,
                          revision_type=a["revision_type"]))

    # strata: (label combo, revision type)
    strata = defaultdict(list)
    for pr in pairs:
        strata[(pr["combo"], pr["revision_type"])].append(pr)
    avail = {f"{'+'.join(k[0])}|{k[1]}": len(v) for k, v in sorted(strata.items())}

    # Class shares in rows: S = n_SR + n_SN, R = n_SR + n_RN, N = n_SN + n_RN.
    # SUPPORTS <= 40% of rows  <=>  n_SR + n_SN <= 4 * n_RN. REFUTES+NEI pairs are rare (22, real
    # revisions only, in 19 cases), so take all of them (allowing the 3 cases that hold two such
    # pairs to contribute both), then split the rest evenly between SUPPORTS+REFUTES
    # (half real, half synthetic) and SUPPORTS+NEI. Other strata: one pair per case.
    SR, SN, RN = ("SUPPORTS", "REFUTES"), ("SUPPORTS", "NOT ENOUGH INFO"), ("REFUTES", "NOT ENOUGH INFO")
    chosen, used_claims, used_states, case_n = [], set(), set(), Counter()

    def take(key, quota, per_case):
        pool = sorted(strata[key], key=lambda x: (x["case_id"], x["claim"]))
        rng.shuffle(pool)
        got = 0
        for pr in pool:
            if got >= quota:
                break
            kc = norm(pr["claim"])
            ks = [norm(vitc_state(r["evidence"], pr["claim"])) for r in pr["rows"]]
            if case_n[pr["case_id"]] >= per_case:
                drops["case_already_used"] += 1
                continue
            if kc in used_claims or any(k in used_states for k in ks):
                drops["dedup_claim_or_state"] += 1
                continue
            used_claims.add(kc)
            used_states.update(ks)
            case_n[pr["case_id"]] += 1
            pr["pair_no"] = case_n[pr["case_id"]]
            chosen.append(pr)
            got += 1
        if got < quota:
            print(f"WARNING vitaminc stratum {key} short: {got}/{quota}", file=sys.stderr)
        return got

    n_rn = take((RN, "real"), 25, per_case=2)
    rest = min(N_VITC_PAIRS - n_rn, 4 * n_rn)
    n_sr = rest // 2
    n_sn = rest - n_sr
    quota = {(RN, "real"): n_rn, (SR, "real"): n_sr - n_sr // 2, (SR, "synthetic"): n_sr // 2,
             (SN, "real"): n_sn}
    for key in [(SR, "real"), (SR, "synthetic"), (SN, "real")]:
        quota[key] = take(key, quota[key], per_case=1)
    rng.shuffle(chosen)
    info = dict(pairs_available_by_stratum=avail, pair_quota={f"{'+'.join(k[0])}|{k[1]}": v for k, v in quota.items()},
                drops=dict(drops))
    return chosen, info


def main():
    rng = random.Random(SEED)
    pmq, pmq_info = build_pubmedqa(rng)
    vit, vit_info = build_vitaminc(rng)

    rows, call_of_state = [], {}

    def add(state, **kw):
        n = len(rows)
        if state not in call_of_state:
            call_of_state[state] = f"c_ohs_{PART}_{len(call_of_state)}"
        row = {"id": f"r_ohs_{PART}_{n}", "group_id": kw.pop("group_id"),
               "call_id": call_of_state[state], "split": "ohs", "track": TRACK,
               "source": kw.pop("source"), "state": state}
        row.update(kw)
        rows.append(row)

    for it in pmq:
        add(it["state"], source="pubmedqa", group_id=f"g:ohs:{PART}:pubmedqa_{it['pubid']}",
            qtype="choice", instructions=it["question"], options=["yes", "no", "maybe"],
            gold=it["gold"], role="choice",
            meta={"license": "MIT", "hf_id": "qiaojin/PubMedQA", "hf_config": "pqa_labeled",
                  "hf_revision": PUBMEDQA_REV,
                  "split_used": "test (official 500-PMID PubMedQA test set from github.com/pubmedqa/pubmedqa "
                                "data/test_ground_truth.json; HF exposes it inside the single 'train' split)",
                  "source_id": str(it["pubid"]), "setting": "reasoning-required (conclusion/long_answer withheld)",
                  "section_labels": it["section_labels"], "meshes": it["meshes"]})

    for pr in vit:
        for role_i, r in enumerate(pr["rows"]):
            state = vitc_state(r["evidence"], pr["claim"])
            add(state, source="vitaminc", group_id=f"g:ohs:{PART}:vitaminc_{pr['case_id']}",
                qtype="choice",
                instructions="Does the evidence support the claim, refute it, or not contain enough information?",
                options=list(VITC_LABELS), gold=r["label"], role="choice", card=VITC_CARD,
                meta={"license": "CC BY-SA 3.0 (Wikipedia-derived; see tals/vitaminc LICENSE)",
                      "hf_id": "tals/vitaminc", "hf_revision": VITC_REV, "split_used": "test",
                      "source_id": r["unique_id"], "case_id": pr["case_id"],
                      "wiki_revision_id": str(r.get("wiki_revision_id") or "") if r.get("wiki_revision_id") == r.get("wiki_revision_id") else "", "page": r["page"],
                      "revision_type": r["revision_type"], "pair_index": role_i,
                      "pair_id": f"{pr['case_id']}:{pr['pair_no']}",
                      "pair_labels": list(pr["combo"]),
                      "card_source": "Schuster et al. 2021 Sec. 4 definition of rel(c,s): support / refute / not contain enough information"})

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    if os.path.exists(REL_OUT):  # contrastive pairs are neither equiv nor complement: no relations
        os.remove(REL_OUT)

    # checks
    assert len({r["id"] for r in rows}) == len(rows)
    for r in rows:
        assert r["gold"] in r["options"]
        assert MIN_CHARS <= len(r["state"]) <= MAX_CHARS + 200
    st2call = defaultdict(set)
    for r in rows:
        st2call[r["state"]].add(r["call_id"])
    assert all(len(v) == 1 for v in st2call.values())
    g = defaultdict(list)
    for r in rows:
        if r["source"] == "vitaminc":
            g[r["group_id"]].append(r)
    for v in g.values():
        byp = defaultdict(list)
        for r in v:
            byp[r["meta"]["pair_id"]].append(r)
        assert all(len(x) == 2 and x[0]["gold"] != x[1]["gold"] for x in byp.values())

    summ = {}
    for src in ("pubmedqa", "vitaminc"):
        sub = [r for r in rows if r["source"] == src]
        c = Counter(r["gold"] for r in sub)
        summ[src] = {"rows": len(sub), "groups": len({r["group_id"] for r in sub}),
                     "n_options": len(sub[0]["options"]),
                     "class_balance": {k: f"{v} ({v / len(sub):.1%})" for k, v in c.most_common()},
                     "state_chars": {"min": min(len(r["state"]) for r in sub),
                                     "median": sorted(len(r["state"]) for r in sub)[len(sub) // 2],
                                     "max": max(len(r["state"]) for r in sub)}}
    summ["pubmedqa"]["build"] = pmq_info
    summ["vitaminc"]["build"] = vit_info
    summ["vitaminc"]["revision_type"] = dict(Counter(r["meta"]["revision_type"] for r in rows if r["source"] == "vitaminc"))
    summ["vitaminc"]["pair_combos"] = dict(Counter("+".join(p["combo"]) for p in vit))
    summ["total_rows"] = len(rows)
    summ["out"] = OUT
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    main()
