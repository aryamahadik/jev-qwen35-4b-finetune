"""Build raw rows for csc_sarcasm (Conversational Sarcasm Corpus; Jang & Frassinelli 2024).

Source : GitHub CoPsyN/CSC @ f11c92b8d54686f64cf1d92766cef07201efb986, data_full.csv (context, response, speaker
         self-rating and one row per third-party evaluator rating) + LICENSE.
Licence: MIT (LICENSE file of CoPsyN/CSC, "Copyright (c) 2024 CoPsyN").
Texts  : psycholinguistic study; participants read a short scenario about their best friend / colleague "Steve"
         (researcher-written context) and typed what they would reply (human-written responses; 2022-23 lab/online
         study). No model-written text.
Labels : each reply was rated for sarcasm on a 1-6 Likert scale by 6 (part 1) or 4 (part 2) independent evaluators.
Split  : the corpus has no official split, but LeWiDi-2025 (Le-Wi-Di/le-wi-di.github.io @ 546eaab4) made a shared-task
         split; every pair in its CSC_dev.json or CSC_test.json (matched by context id + speaker id) is dropped, so
         only LeWiDi-train pairs are used.
Soft   : per-evaluator binarisation at the scale midpoint: rating 4-6 = sarcastic vote, 1-3 = not;
         soft = share of evaluators voting sarcastic (the speaker's own self-rating is NOT used).
Gold   : yes if >= 2/3 of the evaluators voted sarcastic AND the mean evaluator score is >= 4.0 ('somewhat' or more);
         no if <= 1/3 voted sarcastic AND the mean score is <= 3.0; ties (2/4, 3/6) and vote/mean disagreements
         dropped. (Review 29 Sep: without the mean check ~24% of yes rows had mean < 4, e.g. [4,4,4,1,4,4] on a plainly
         literal complaint, which contradicts the 'no' definition.)
State  : "Situation (Steve is your best friend|colleague): <context>" + "Your reply to Steve: <response>". The
         relationship line restates the experiment condition (interlocutor_relationship), not new content.
Dedup  : one row per reply; exact / near-duplicate replies (word 5-gram Jaccard >= 0.7) within the same context
         dropped; decontaminated against our data, label-NLI, JevBench public and other v14 parts.
Balance: yes share 0.36. Deterministic (seed 20261101).
"""
import collections
import json
import random

import pandas as pd

import _cal_common as C

KEY = "csc_sarcasm"
MAX_ROWS = 4000
YES_SHARE = 0.36
REV = "f11c92b8d54686f64cf1d92766cef07201efb986"
BASE = f"https://raw.githubusercontent.com/CoPsyN/CSC/{REV}/"
FILES = {"data_full.csv": "fd8ca7531887823a315e91f5d0edbcc9ec685a557c333c37f485a15a9e55ad7a",
         "LICENSE": "390830edfee0a5ac38d9f84de152a37bf1f6b3c574a074ea6eaef9ba4db799e0"}
LW_REV = "546eaab420adab3c658813ae3fc7ae9f73cf8f05"
LW_BASE = f"https://raw.githubusercontent.com/Le-Wi-Di/le-wi-di.github.io/{LW_REV}/LeWiDi_3-2025/CSC/"
LW_FILES = {"CSC_dev.json": "e20b142573639c50640b2ab720d79d348005b174e36bc8332fbadbfd53160be5",
            "CSC_test.json": "80b7c33bd11de5bf6637876b73d923735029e8732eda3eba3f7b8b257f7b4181"}
LICENCE = f"MIT (https://github.com/CoPsyN/CSC/blob/{REV}/LICENSE, 'MIT License / Copyright (c) 2024 CoPsyN')"
DATASET = "Conversational Sarcasm Corpus (github CoPsyN/CSC data_full.csv); LeWiDi-2025 dev/test pairs excluded"
CACHE = C.CACHE / KEY

Q = "Is your reply to Steve in this situation sarcastic?"
DEFS = {
    "yes": "At least two-thirds of the independent raters scored the reply 4-6 on a 1-6 sarcasm scale (mean 4+): it says the "
           "opposite of, or something other than, what the speaker really thinks, to mock, tease or criticise "
           "(ironic praise, exaggerated agreement, pointed rhetorical questions).",
    "no": "At most one-third of the raters scored it 4-6 (mean 3 or less): the reply is sincere and meant literally (genuine thanks, "
          "honest criticism, plain information or a real question), even when it is blunt, joking or annoyed.",
}


def main():
    rng = random.Random(C.SEED)
    for n, sha in FILES.items():
        C.fetch(BASE + n, CACHE / n, sha)
    held = set()
    for n, sha in LW_FILES.items():
        p = C.fetch(LW_BASE + n, CACHE / n, sha)
        for v in json.load(open(p)).values():
            held.add(v["other_info"]["context+speaker"])
    print("LeWiDi dev/test pairs excluded:", len(held))

    d = pd.read_csv(CACHE / "data_full.csv", keep_default_na=False)
    d["pair"] = d.global_context_name.astype(str) + "_" + d.global_speaker.astype(str)
    cands = {"yes": [], "no": []}
    drop = collections.Counter()
    for pair, g in d.groupby("pair", sort=True):
        if pair in held:
            drop["lewidi_dev_test"] += 1
            continue
        g = g.drop_duplicates("global_evaluator")
        ctx = C.clean(g.context_text.iloc[0])
        resp = C.clean(g.response_text.iloc[0])
        if g.response_text.nunique() != 1 or len(C.words(resp)) < 2:
            drop["bad_response"] += 1
            continue
        scores = [int(x) for x in g.sarcasm_score_by_evaluator]
        n = len(scores)
        if n not in (4, 6):
            drop[f"n={n}"] += 1
            continue
        v = sum(s >= 4 for s in scores)
        mean = sum(scores) / n
        if v * 3 >= 2 * n and mean >= 4.0:
            gold = "yes"
        elif v * 3 <= n and mean <= 3.0:
            gold = "no"
        else:
            drop["tie_or_weak"] += 1
            continue
        rel = {"best_friend": "best friend", "colleague": "colleague"}[g.interlocutor_relationship.iloc[0]]
        state = f"Situation (Steve is your {rel}): {ctx}\nYour reply to Steve: {resp}"
        cands[gold].append({"pair": pair, "ctx_id": int(g.global_context_name.iloc[0]), "ctx": ctx, "resp": resp,
                            "state": state, "votes": v, "n": n, "scores": scores,
                            "self": int(g.sarcasm_score_by_speaker.iloc[0]), "ctype": g.context_type.iloc[0]})
    print("candidates:", {k: len(v) for k, v in cands.items()}, "dropped:", dict(drop))

    # contexts are researcher-written and shared by design; overlap checks look at the reply text
    core = {c["pair"]: [c["resp"]] for g in cands for c in cands[g]}
    hits = C.decon(core, KEY)
    hits.update(C.cross_v14(core, {KEY}))
    for g in cands:
        cands[g] = [c for c in cands[g] if c["pair"] not in hits]

    # dedupe replies within a context (a context is shown with ~70 different replies)
    per_ctx = collections.defaultdict(lambda: C.NearDup(thr=0.7))
    for g in cands:
        rng.shuffle(cands[g])
        cands[g].sort(key=lambda c: -abs(c["votes"] / c["n"] - 0.5))  # clearest first
    ny = min(len(cands["yes"]), int(MAX_ROWS * YES_SHARE))
    picked = {"yes": [], "no": []}
    for g, target in (("yes", ny), ("no", MAX_ROWS - ny)):
        for c in cands[g]:
            if len(picked[g]) >= target:
                break
            if per_ctx[c["ctx"]].seen(c["resp"]):
                continue
            picked[g].append(c)
    ny = len(picked["yes"])
    picked["no"] = picked["no"][:int(ny * (1 - YES_SHARE) / YES_SHARE)]

    rows = []
    for g in ("yes", "no"):
        for c in picked[g]:
            e = "sarcasm" if (g == "yes" or c["ctype"] == "non_neutral") else None
            if g == "no" and e is None and C.neg_count(c["resp"]):
                e = "negation"
            rows.append({
                "key": KEY, "rid": f"csc-{c['pair']}", "state": c["state"], "instructions": Q, "options": C.YN,
                "gold": g, "soft": C.soft_yes(c["votes"], c["n"]),
                "meta": {"dataset": DATASET, "config": "data_full.csv", "revision": f"{REV} (LeWiDi split @ {LW_REV})",
                         "licence": LICENCE, "split": "train",
                         "orig_label": {"evaluator_scores_1to6": c["scores"], "speaker_self_score": c["self"],
                                        "context_type": c["ctype"], "context_id": c["ctx_id"]},
                         "family": C.FAMILY, "edge": e},
            })
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, {None: DEFS})
    st = C.summary(KEY, rows)
    C.show_samples(rows, 5)
    C.append_manifest(C.manifest_record(
        KEY, DATASET, LICENCE, rows, "yesno",
        "Soft = share of the 4-6 third-party evaluators rating the reply 4-6 on the 1-6 sarcasm scale (speaker "
        "self-rating not used). Gold for >= 2/3 (mean >= 4) or <= 1/3 (mean <= 3) majorities; ties dropped. LeWiDi-2025 dev/test pairs "
        "excluded. Hard negatives: sincere replies to sarcasm-triggering (non-neutral) scenarios tagged sarcasm.",
        st))


if __name__ == "__main__":
    main()
