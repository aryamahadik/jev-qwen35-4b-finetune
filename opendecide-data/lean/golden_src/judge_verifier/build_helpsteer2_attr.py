"""Build raw rows for helpsteer2_attr: attribute-specific response judging with HUMAN ratings (HelpSteer2; Wang et al.
2024, arXiv:2406.08673).

Source : HF nvidia/HelpSteer2 pinned to revision 990b2711a36180dd19d9c94b8627844866f8982a: train.jsonl.gz (the train
         split: prompt, response, mean attribute scores) and disagreements/disagreements.jsonl.gz (the individual
         annotator scores behind each mean). Only (prompt, response) pairs present in train.jsonl.gz are used; the
         validation file and the preference file are never read.
Licence: CC BY 4.0 (dataset card README.md at the pinned revision: 'license: cc-by-4.0'; "HelpSteer2 is an
         open-source Helpfulness Dataset (CC-BY-4.0)").
Texts  : ShareGPT-style user prompts (29% multi-turn) with responses from permissively licensed models (the objects
         being judged).
Labels : HUMAN Likert 0-4 ratings from 3-5 Scale AI annotators (outliers filtered by NVIDIA) per attribute, following
         the guidelines in the paper's appendix. Three yes/no questions, each decided only where EVERY annotator is
         on the same side of the guideline boundary:
           correct : correctness >= 3 for all annotators and mean >= 3.5 ('completely' or 'mostly correct, no
                     misleading information or hallucinations') = yes; <= 2 for all ('mix of correct and incorrect'
                     or worse) = no.
           verbose : verbosity >= 3 for all ('moderately long' / 'verbose' for what was asked) = yes; <= 1 for all
                     ('pretty short' / 'succinct') = no; 'average length' (2) is never used.
           coherent: coherence 4 for all ('perfectly coherent and clear') = yes; <= 2 for all ('a little unclear',
                     contradictions, or worse) = no.
         soft = real annotator shares on each side (unanimous by construction).
Filters: one row per prompt (the two responses to a prompt are never both used); states over 9,000 characters
         dropped (no truncation); exact/near-duplicate prompts dropped; decontamination of prompt and response against
         label-NLI, all local train/dev/eval files (drops prompts already used by the older judge_helpsteer2 rows,
         whose question was overall correctness) and JevBench; cross-check against other v14 parts.
Deterministic (seed 20261203). CPU only.
"""
import collections
import gzip
import json
import random
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _jv_common as C  # noqa: E402

KEY = "helpsteer2_attr"
SEED = 20261203
REV = "990b2711a36180dd19d9c94b8627844866f8982a"
BASE = f"https://huggingface.co/datasets/nvidia/HelpSteer2/resolve/{REV}/"
FILES = {
    "train.jsonl.gz": "c0d7e91d738d42e8a08070db26c4c09a9c7631308e1f0fd380ff43d130c9f713",
    "disagreements/disagreements.jsonl.gz": "53435e0e2926620bf08ce91f278d7368ee6903f416a47764fe8839f3b71b3ab4",
    "README.md": "835effb9e7d9cd0e8b7b8c1816d1d97a8961a036543108e4a0b6a5e22712ff7b",
}
LICENCE = (f"CC BY 4.0 (https://huggingface.co/datasets/nvidia/HelpSteer2/blob/{REV}/README.md, 'license: cc-by-4.0'; "
           "'HelpSteer2 is an open-source Helpfulness Dataset (CC-BY-4.0)')")
DATASET = "nvidia/HelpSteer2 (train split + individual annotator scores from disagreements.jsonl.gz)"
TARGET = {"correct": 3400, "verbose": 1300, "coherent": 900}
MAX_STATE = 9000

Q = {
    "correct": "Is the response's content correct, with no false, misleading or hallucinated information and at most "
               "minor details missing?",
    "verbose": "Is the response longer or more detailed than what the user's request calls for?",
    "coherent": "Is the response perfectly clear and self-consistent throughout, with no contradictions or confusing "
                "parts?",
}
DEFS = {
    "correct": {
        "yes": "Completely or mostly correct: everything stated is accurate, with no false, misleading or hallucinated "
               "information, and any requested task is done; at most a small amount of useful information is missing.",
        "no": "Not correct: the response mixes correct and incorrect information, contains misleading claims or "
              "hallucinations (even minor ones), is mostly wrong or incomplete, or does the wrong task or only part "
              "of it.",
    },
    "verbose": {
        "yes": "Longer than needed: moderately long or verbose for what was asked, with extra detail, restatement or "
               "wordiness (rich but unrequested detail also counts), judged relative to the request, not absolute "
               "length.",
        "no": "Short relative to the request: succinct or pretty short, giving what was asked with little or no extra "
              "material (an incorrect answer can still be succinct).",
    },
    "coherent": {
        "yes": "Perfectly coherent and clear: self-consistent throughout, no contradictions, and the writing flows "
               "logically so it is easy to follow.",
        "no": "Not fully coherent: at least a little unclear or inconsistent, e.g. contradictions, run-on or confusing "
              "statements, repetition that breaks the flow, style changes, or hard-to-follow sections.",
    },
}


def render(prompt, response):
    parts = prompt.split("<extra_id_1>")
    lines = ["Conversation:", f"User: {C.clean_keep(parts[0])}"]
    for p in parts[1:]:
        role, _, text = p.partition("\n")
        role = role.strip()
        lines.append(f"{'Assistant' if role == 'Assistant' else 'User'}: {C.clean_keep(text)}")
    lines += ["", "Response to judge (the assistant's reply to the last user message):", C.clean_keep(response)]
    return "\n".join(lines)


def decide(attr, vals):
    if len(vals) < 2:
        return None
    m = statistics.mean(vals)
    if attr == "correct":
        if min(vals) >= 3 and m >= 3.5:
            return "yes"
        if max(vals) <= 2:
            return "no"
    elif attr == "verbose":
        if min(vals) >= 3:
            return "yes"
        if max(vals) <= 1:
            return "no"
    elif attr == "coherent":
        if min(vals) == 4:
            return "yes"
        if max(vals) <= 2:
            return "no"
    return None


COL = {"correct": "correctness", "verbose": "verbosity", "coherent": "coherence"}


def main():
    rng = random.Random(SEED)
    cache = C.CACHE / "helpsteer2"
    paths = {rel: C.fetch(BASE + rel, cache / Path(rel).name, sha) for rel, sha in FILES.items()}
    stats = collections.Counter()
    train = [json.loads(l) for l in gzip.open(paths["train.jsonl.gz"], "rt")]
    ind = {}
    for l in gzip.open(paths["disagreements/disagreements.jsonl.gz"], "rt"):
        o = json.loads(l)
        ind[(o["prompt"], o["response"])] = o
    by_prompt = collections.defaultdict(list)
    for i, r in enumerate(train):
        o = ind.get((r["prompt"], r["response"]))
        if o is None:
            stats["no_individual"] += 1
            continue
        state = render(r["prompt"], r["response"])
        if len(state) > MAX_STATE:
            stats["drop_long"] += 1
            continue
        if not r["response"].strip():
            stats["drop_empty"] += 1
            continue
        labs = {}
        for q, col in COL.items():
            g = decide(q, o[col])
            if g:
                labs[q] = (g, o[col])
        if not labs:
            stats["no_clear_label"] += 1
            continue
        by_prompt[r["prompt"]].append({"rid": f"hs2-train-{i}", "prompt": r["prompt"], "response": r["response"],
                                       "state": state, "labs": labs, "means": {c: r[c] for c in COL.values()},
                                       "multi": "<extra_id_1>" in r["prompt"]})
    prompts = sorted(by_prompt)
    rng.shuffle(prompts)
    last = {p: C.clean(p.split("<extra_id_1>")[-1].partition("\n")[2] if "<extra_id_1>" in p else p) for p in prompts}
    items = [{"p": p, "last": last[p]} for p in prompts]
    items = C.near_dup_filter(items, lambda x: x["last"] if len(x["last"].split()) >= 4 else x["p"], thresh=0.9)
    prompts = [x["p"] for x in items]
    stats["prompts_after_neardup"] = len(prompts)
    core = {}
    for p in prompts:
        for c in by_prompt[p]:
            core[c["rid"]] = [last[p], c["response"]]
    hits = C.decon(core, cache_name=KEY)
    # whole prompt (all turns) against the other v14 parts, incl. helpsteer3_pref (built before this set)
    full = {c["rid"]: C.clean(p.replace("<extra_id_1>", " ")) for p in prompts for c in by_prompt[p]}
    xhits = C.cross_v14({rid: [full[rid]] for rid in core if len(full[rid].split()) >= 8}, own_keys={KEY})
    # prompts repeated in helpsteer3_pref (same ShareGPT prompt; exact match for short prompts, 10-word run otherwise)
    hs3 = C.RAW_DIR / "helpsteer3_pref.jsonl"
    if hs3.exists():
        g3, e3 = set(), set()
        for line in open(hs3):
            conv = json.loads(line)["state"].split("\n\nResponse 1:")[0]
            for turn in conv.split("\nUser: ")[1:] + [conv.split("\n", 1)[-1]]:
                e3.add(C.norm(turn.split("\nAssistant: ")[0].replace("User: ", "", 1)))
            w = C.words(conv)
            g3 |= {hash(tuple(w[i:i + C.RUN])) for i in range(max(0, len(w) - C.RUN + 1))}
        for p in prompts:
            turns = [C.norm(x.partition("\n")[2] if i else x) for i, x in enumerate(p.split("<extra_id_1>"))]
            w = C.words("Conversation: User: " + " ".join(p.split("<extra_id_1>")))
            if any(t in e3 for t in turns if t) or any(hash(tuple(w[i:i + C.RUN])) in g3
                                                       for i in range(max(0, len(w) - C.RUN + 1))):
                for c in by_prompt[p]:
                    xhits.setdefault(c["rid"], "v14:helpsteer3_pref(prompt)")
    stats["decon_hits"] = len(hits)
    stats["xv14_hits"] = len(xhits)

    # candidate pools per (question, gold); each prompt is used once
    pools = collections.defaultdict(list)
    for p in prompts:
        for c in by_prompt[p]:
            if c["rid"] in hits or c["rid"] in xhits:
                continue
            for q, (g, vals) in c["labs"].items():
                pools[(q, g)].append((p, c, vals))
    for k in pools:
        rng.shuffle(pools[k])
    stats.update({f"pool_{q}_{g}": len(v) for (q, g), v in pools.items()})
    used_p = set()
    rows = []

    def take(q, g, want):
        got = 0
        for p, c, vals in pools[(q, g)]:
            if got >= want:
                break
            if p in used_p:
                continue
            used_p.add(p)
            got += 1
            share_yes = {"correct": sum(v >= 3 for v in vals), "verbose": sum(v >= 3 for v in vals),
                         "coherent": sum(v == 4 for v in vals)}[q] / len(vals)
            if len(c["state"]) > 4000:
                e = "long_context"
            elif c["multi"]:
                e = "multi_hop"
            else:
                e = C.edge(last[p], order=("double_negation", "negation", "quantifier", "units", "numeric"),
                           default=None)
            rows.append({
                "key": KEY, "rid": f"{c['rid']}-{q}", "state": c["state"], "instructions": Q[q], "options": C.YN,
                "gold": g, "soft": {"yes": round(share_yes, 4), "no": round(1 - share_yes, 4)},
                "meta": {"dataset": DATASET, "config": f"train.jsonl.gz + disagreements; attribute={COL[q]}",
                         "revision": f"hf:{REV}; sha256:{FILES['train.jsonl.gz']}",
                         "licence": LICENCE, "split": "train",
                         "orig_label": {"attribute": COL[q], "individual_scores": vals, "mean_scores": c["means"]},
                         "family": C.FAMILY, "edge": e, "defs": q},
            })
        stats[f"sel_{q}_{g}"] = got
        return got

    # per question: the scarcer side first (up to half the target), then the other side capped at 1.5x of it
    for q in sorted(TARGET, key=lambda q: min(len(pools[(q, "yes")]), len(pools[(q, "no")]))):
        sides = sorted(("yes", "no"), key=lambda g: len(pools[(q, g)]))
        n1 = take(q, sides[0], TARGET[q] // 2)
        take(q, sides[1], min(TARGET[q] - n1, int(n1 * 1.5)))
    rows.sort(key=lambda r: r["rid"])
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, DEFS)
    st = C.summary(KEY, rows)
    print("stats:", dict(stats))
    C.show_samples(rows, n=6, seed=13)
    C.append_manifest(C.manifest_record(
        KEY, DATASET, LICENCE, rows, "yesno",
        "Attribute-specific judging with HUMAN Likert ratings (3-5 annotators): correct? (guideline boundary 3 vs 2: "
        "no misleading info/hallucination), longer than the request calls for? (3-4 vs 0-1), perfectly coherent? "
        "(4 vs <=2); every annotator must be on the same side; soft = annotator shares; one row per prompt; "
        "multi-turn conversations kept whole; decon drops prompts already in judge_helpsteer2 (overall-correctness "
        "framing).", st))


if __name__ == "__main__":
    main()
