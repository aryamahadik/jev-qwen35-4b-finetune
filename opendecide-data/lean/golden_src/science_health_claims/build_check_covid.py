"""Build raw rows for check_covid (Check-COVID: Fact-Checking COVID-19 News Claims with Scientific Evidence;
ACL Findings 2023, arXiv:2305.18265; github posuer/Check-COVID).

Source : GitHub posuer/Check-COVID pinned to commit 3ae70f8cac4df13a3ce56878e20d8e76790e422d.
         Check-COVID/train/covidCheck_train_composed+extracted.json (TRAIN ONLY; dev/test never read) and
         Check-COVID/corpus.json (the CORD-19 abstracts the evidence sentences index into).
Licence: MIT ("Copyright (c) 2023 Columbia University", LICENSE file at the pinned commit).
Texts  : claims are either extracted verbatim from news articles (journalist-written, is_auth=True) or composed by the
         expert annotators; evidence = the annotator-selected sentence(s) of a peer-reviewed abstract. Human only (the
         paper uses GPT-3.5 only as an evaluated baseline, never to write or label data).
Labels : expert annotation, SUPPORT / REFUTE / NOTENOUGHINFO, with the rationale sentence ids.
Design :
  * Claims come in groups of (SUPPORT claim, REFUTE claim, NEI) that share one evidence set: the REFUTE claim is a
    minimal fact-flip of the SUPPORT claim (a changed number, direction, quantifier or negation). We keep SUPPORT and
    REFUTE rows as twin pairs (meta.twin_of links them) so the decisive detail is learnt, not the topic.
  * NOTENOUGHINFO rows are DROPPED: a 20-row audit found several NEI evidence sentences that plainly support or refute
    the claim (e.g. "Speech droplets ... likely mode of transmission" labelled NEI for "can transmit by speaking"),
    so NEI cannot be mapped to a precise yes/no.
  * State = only the annotated evidence sentences (not the title or the rest of the abstract), then the claim.
  * Each group is assigned (seeded, alternating after shuffle) to ONE question so both twins share the question:
      support : "Does the evidence support the claim?"      SUPPORT -> yes, REFUTE -> no
      refute  : "Does the evidence contradict the claim?"   REFUTE -> yes, SUPPORT -> no
  * Decontamination (label-NLI incl. health_fact, local train/dev/eval, JevBench public) and exact/near dedupe.
Deterministic (seed 20261114). CPU only.
"""
import collections
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _shc_common as C  # noqa: E402

KEY = "check_covid"
SEED = 20261114
COMMIT = "3ae70f8cac4df13a3ce56878e20d8e76790e422d"
BASE = f"https://raw.githubusercontent.com/posuer/Check-COVID/{COMMIT}/"
FILES = {
    "Check-COVID/train/covidCheck_train_composed+extracted.json":
        "1af4b5e364129631b49a9132cadcd4f1b4937c90bef22ba0c08242be1630858b",
    "Check-COVID/corpus.json": "2a56084b933f28ec02781a9e501082683ca4b9c4c1c6c8530190d6fb0002ce42",
    "LICENSE": "ead1a5b6c71fc912da18df21ba3a0a6b713da2b13939cbb2f02fb97c06fb99eb",
}
LICENCE = (f"MIT (https://github.com/posuer/Check-COVID/blob/{COMMIT}/LICENSE, "
           "'Copyright (c) 2023 Columbia University')")
DATASET = "Check-COVID (github posuer/Check-COVID)"

QUESTIONS = {
    "support": "Does the evidence support the claim?",
    "refute": "Does the evidence contradict the claim?",
}
DEFS = {
    "support": {
        "yes": "The evidence sentences back up the claim's central assertion, directly or by simple inference: same "
               "direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even "
               "if the scientific wording is hedged ('suggests', 'is consistent with').",
        "no": "The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, "
              "percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not "
              "support the claim as stated.",
    },
    "refute": {
        "yes": "The evidence shows the claim is false: it states the opposite direction of effect, a clearly different "
               "number or share, or contradicts a quantifier ('all', 'only', 'none'), negation or group named in the "
               "claim.",
        "no": "The evidence does not show the claim to be false: it agrees with the claim's central assertion (same "
              "direction, compatible numbers after ordinary rounding, compatible population), even if hedged.",
    },
}


def main():
    rng = random.Random(SEED)
    cache = C.CACHE / KEY
    paths = {rel: C.fetch(BASE + rel, cache / Path(rel).name, sha) for rel, sha in FILES.items()}
    corpus = {}
    for line in open(paths["Check-COVID/corpus.json"]):
        d = json.loads(line)
        corpus[d["cord_id"]] = d
    recs = [json.loads(l) for l in open(paths["Check-COVID/train/covidCheck_train_composed+extracted.json"])]
    stats = collections.Counter(r["label"] for r in recs)

    groups = collections.defaultdict(list)
    for r in recs:
        if r["label"] == "NOTENOUGHINFO":
            continue
        sents = corpus[r["cord_id"]]["abstract"]
        ev_ids = sorted({e["sent_index"] for e in r["evidence_set"]})
        ev = " ".join(C.clean(sents[i]) for i in ev_ids)
        claim = C.clean(r["claim"])
        if len(ev) < 40 or len(claim) < 15 or ev.startswith("["):
            stats["drop_short_or_junk"] += 1
            continue
        groups[r["id"].rsplit("_", 1)[0]].append({"rid": r["id"], "label": r["label"], "claim": claim, "ev": ev,
                                                 "n_ev": len(ev_ids), "is_auth": bool(r["is_auth"]),
                                                 "cord_id": r["cord_id"], "types": [e["type"] for e in r["evidence_set"]]})

    # pair SUPPORT/REFUTE members sharing the same evidence set inside each group
    pairs = []
    for g, members in sorted(groups.items()):
        by_ev = collections.defaultdict(dict)
        for m in members:
            by_ev[m["ev"]].setdefault(m["label"], m)
        for ev, d in sorted(by_ev.items()):
            if "SUPPORT" in d and "REFUTE" in d and C.norm(d["SUPPORT"]["claim"]) != C.norm(d["REFUTE"]["claim"]):
                pairs.append((d["SUPPORT"], d["REFUTE"]))
            else:
                stats["unpaired"] += len(d)

    # decontamination on claims and evidence
    core = {}
    for s, r in pairs:
        core[s["rid"]] = [s["claim"], s["ev"]]
        core[r["rid"]] = [r["claim"], r["ev"]]
    hits = C.decon(core, cache_name=KEY)
    pairs = [(s, r) for s, r in pairs if s["rid"] not in hits and r["rid"] not in hits]

    rng.shuffle(pairs)
    rows = []
    for i, (s, r) in enumerate(pairs):
        qid = "support" if i % 2 == 0 else "refute"
        for m, twin in ((s, r), (r, s)):
            if qid == "support":
                gold = "yes" if m["label"] == "SUPPORT" else "no"
            else:
                gold = "yes" if m["label"] == "REFUTE" else "no"
            state = f"Evidence (from the abstract of a scientific article):\n{m['ev']}\n\nClaim: {m['claim']}"
            e = C.edge(m["claim"], order=("double_negation", "negation", "quantifier", "units", "numeric", "temporal"))
            if e is None and m["n_ev"] >= 2:
                e = "multi_hop"
            rows.append({
                "key": KEY, "rid": m["rid"], "state": state, "instructions": QUESTIONS[qid], "options": C.YN,
                "gold": gold, "soft": None,
                "meta": {"dataset": DATASET, "config": "Check-COVID/train/covidCheck_train_composed+extracted.json",
                         "revision": f"git:{COMMIT}; sha256:{FILES['Check-COVID/train/covidCheck_train_composed+extracted.json']}",
                         "licence": LICENCE, "split": "train",
                         "orig_label": {"label": m["label"], "claim_type": "extracted (journalist)" if m["is_auth"]
                                        else "composed (annotator)", "cord_id": m["cord_id"],
                                        "evidence_types": m["types"]},
                         "family": C.FAMILY, "edge": e, "defs": qid, "twin_of": twin["rid"]},
            })
    # exact / near dedupe of states. Twins differ only by the flipped detail, so near-duplicates are only looked for
    # among rows with the SAME source label (a twin pair is never collapsed; true re-uses of a claim/evidence are).
    def block(x):
        ws = sorted(w for w in set(C.norm(x["state"]).split()) if len(w) >= 5)[:2] or ["_"]
        return [x["meta"]["orig_label"]["label"] + ":" + w for w in ws]

    rows = C.near_dup_filter(rows, lambda x: x["state"], thresh=0.9, block_of=block)
    keep_rids = {x["rid"] for x in rows}
    for x in rows:
        if x["meta"]["twin_of"] not in keep_rids:
            x["meta"]["twin_of"] = None
    rng.shuffle(rows)

    C.write_outputs(KEY, rows, {q: DEFS[q] for q in DEFS})
    st = C.summary(KEY, rows)
    print("source label counts / drops:", dict(stats), "| pairs:", len(pairs), "| decon hits:", len(hits))
    print("claim types:", dict(collections.Counter(x["meta"]["orig_label"]["claim_type"] for x in rows)))
    C.show_samples(rows, n=5, seed=3)
    C.append_manifest(C.manifest_record(
        KEY, DATASET + ", train split", LICENCE, rows, "yesno",
        "Expert-annotated COVID-19 news claims vs sentence-level evidence from peer-reviewed abstracts; SUPPORT/REFUTE "
        "fact-flip twin pairs (same evidence, one flipped detail) kept together under one of two questions "
        "(support? / contradict?); NEI dropped after audit showed unreliable NEI labels; evidence = rationale "
        "sentences only.", st))


if __name__ == "__main__":
    main()
