"""Build raw rows for helpsteer3_pref: pairwise response preference with HUMAN labels (HelpSteer3-Preference; Wang et
al. 2025, arXiv:2505.11475).

Source : HF nvidia/HelpSteer3 pinned to revision f6d145777bcbde96137596340fab89793acd1031, preference/train.jsonl.gz
         ONLY (the validation file is never downloaded).
Licence: CC BY 4.0 (dataset card README.md at the pinned revision: 'license: cc-by-4.0' and "HelpSteer3 is an
         open-source dataset (CC-BY-4.0)").
Texts  : user prompts from ShareGPT (code) and WildChat-1M (general, STEM); two responses per prompt from ~20
         permissively licensed open models (the objects being judged).
Labels : HUMAN pairwise preferences from 3 independent expert annotators (Scale AI; vendors prevented LLM use during
         annotation); overall_preference in -3..3 (negative = Response 1 better). The principle subset (DeepSeek-written
         principles) is NOT used.
Rows   : domains general / stem / code (the multilingual domain is left out). Kept only when every annotator prefers the
         same response (no annotator tie or opposite vote): 'clear' = |overall| >= 2 (about 85% of rows) and 'slight' =
         |overall| = 1 (unanimous slight preference, 15%). Question asks whether a named response is better than the other
         (qid r1 / r2, chosen at random), so yes and no are balanced and position is not a cue.
         soft = real annotator shares favouring the named response.
Filters: states over 9,000 characters dropped (no truncation); exact and near-duplicate prompts (word-set Jaccard >= 0.9
         on the last user turn) dropped; decontamination of the last user turn and both responses against label-NLI, all
         local train/dev/eval files (drops prompts shared with the older HelpSteer2-based judge rows) and JevBench.
Deterministic (seed 20261202). CPU only.
"""
import collections
import gzip
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _jv_common as C  # noqa: E402

KEY = "helpsteer3_pref"
SEED = 20261202
REV = "f6d145777bcbde96137596340fab89793acd1031"
BASE = f"https://huggingface.co/datasets/nvidia/HelpSteer3/resolve/{REV}/"
FILES = {
    "preference/train.jsonl.gz": "32b52e1d378f8dab1e4c9ae549da49a5d6fc0875aeafe3f9139e6053beb906bb",
    "README.md": "d5d46db58e8374937ea284b33b1583a4a465b232bf74b941745d80e3c35fd8ae",
}
LICENCE = (f"CC BY 4.0 (https://huggingface.co/datasets/nvidia/HelpSteer3/blob/{REV}/README.md, 'license: cc-by-4.0'; "
           "'HelpSteer3 is an open-source dataset (CC-BY-4.0)')")
DATASET = "nvidia/HelpSteer3 (preference config, train)"
TARGET = {"general": 2300, "stem": 1300, "code": 1400}
SLIGHT_SHARE = 0.15
MAX_STATE = 9000

Q = {
    "r1": "Is Response 1 a better reply than Response 2 to the user's last message?",
    "r2": "Is Response 2 a better reply than Response 1 to the user's last message?",
}


def defs_for(a, b):
    return {
        "yes": f"Response {a} is the better reply overall: given the whole conversation, it serves the user's last "
               f"message better than Response {b} (more correct and complete, follows every instruction and constraint, "
               "working code, clearer and appropriately concise), even if it has minor flaws of its own.",
        "no": f"Response {b} is the better reply overall: Response {a} is less correct, less complete, ignores an "
              "instruction or constraint, has broken code, or is less clear or needlessly long compared with "
              f"Response {b}.",
    }


DEFS = {"r1": defs_for(1, 2), "r2": defs_for(2, 1)}


def render(context, r1, r2):
    lines = ["Conversation:"]
    for m in context:
        role = "User" if m["role"] == "user" else "Assistant"
        lines.append(f"{role}: {C.clean_keep(m['content'])}")
    lines += ["", "Response 1:", C.clean_keep(r1), "", "Response 2:", C.clean_keep(r2)]
    return "\n".join(lines)


def main():
    rng = random.Random(SEED)
    cache = C.CACHE / "helpsteer3"
    paths = {rel: C.fetch(BASE + rel, cache / ("preference_train.jsonl.gz" if rel.endswith("gz") else rel), sha)
             for rel, sha in FILES.items()}
    stats = collections.Counter()
    cands = []
    with gzip.open(paths["preference/train.jsonl.gz"], "rt") as f:
        for ln, line in enumerate(f):
            o = json.loads(line)
            stats["rows"] += 1
            if o["domain"] not in TARGET:
                stats["drop_domain"] += 1
                continue
            p = o["overall_preference"]
            s = [x["score"] for x in o["individual_preference"]]
            if p == 0 or len(s) < 2 or not all(x != 0 and (x > 0) == (p > 0) for x in s):
                stats["drop_not_unanimous"] += 1
                continue
            ctx = o["context"]
            if not ctx or ctx[-1]["role"] != "user":
                stats["drop_ctx"] += 1
                continue
            r1, r2 = o["response1"], o["response2"]
            if not r1.strip() or not r2.strip() or C.norm(r1) == C.norm(r2):
                stats["drop_resp"] += 1
                continue
            state = render(ctx, r1, r2)
            if len(state) > MAX_STATE:
                stats["drop_long"] += 1
                continue
            cands.append({"rid": f"hs3-train-{ln}", "domain": o["domain"], "lang": o["language"], "p": p, "scores": s,
                          "last": C.clean(ctx[-1]["content"]), "r1": r1, "r2": r2, "state": state,
                          "ctx_text": " ".join(C.clean(m["content"]) for m in ctx),
                          "turns": sum(m["role"] == "user" for m in ctx),
                          "strength": "clear" if abs(p) >= 2 else "slight"})
    stats["cands"] = len(cands)

    # near-duplicate prompts (last user turn), keep first in a seeded order
    cands.sort(key=lambda c: c["rid"])
    rng.shuffle(cands)
    cands = C.near_dup_filter(cands, lambda c: c["last"] if len(c["last"].split()) >= 4 else c["state"][:600],
                              thresh=0.9)
    stats["after_neardup"] = len(cands)
    core = {c["rid"]: [c["last"], c["r1"], c["r2"]] for c in cands}
    hits = C.decon(core, cache_name=KEY)
    # helpsteer2_attr is de-overlapped against this set in its own builder (it runs after this one)
    xhits = C.cross_v14({c["rid"]: [c["ctx_text"]] for c in cands if len(c["ctx_text"].split()) >= 8},
                        own_keys={KEY, "helpsteer2_attr"})
    cands = [c for c in cands if c["rid"] not in hits and c["rid"] not in xhits]
    stats["after_decon"] = len(cands)

    chosen = []
    for dom, n in TARGET.items():
        pool = [c for c in cands if c["domain"] == dom]
        slight = [c for c in pool if c["strength"] == "slight"]
        clear = [c for c in pool if c["strength"] == "clear"]
        n_sl = min(len(slight), int(round(n * SLIGHT_SHARE)))
        take = slight[:n_sl] + clear[:n - n_sl]
        stats[f"sel_{dom}"] = len(take)
        chosen += take

    rows = []
    # alternate which response the question names, balanced within each (domain, winner) cell
    cells = collections.defaultdict(list)
    for c in chosen:
        cells[(c["domain"], c["p"] > 0)].append(c)
    for cell in sorted(cells):
        lst = cells[cell]
        for i, c in enumerate(lst):
            qid = "r1" if i % 2 == 0 else "r2"
            named_wins = (c["p"] < 0) if qid == "r1" else (c["p"] > 0)
            gold = "yes" if named_wins else "no"
            n_fav = sum((x < 0) if qid == "r1" else (x > 0) for x in c["scores"])
            soft = {"yes": round(n_fav / len(c["scores"]), 4), "no": round(1 - n_fav / len(c["scores"]), 4)}
            e = "long_context" if len(c["state"]) > 4000 else (
                "ambiguous" if c["strength"] == "slight" else C.edge(c["last"], order=(
                    "double_negation", "negation", "quantifier", "units", "numeric"), default=None))
            rows.append({
                "key": KEY, "rid": c["rid"], "state": c["state"], "instructions": Q[qid], "options": C.YN,
                "gold": gold, "soft": soft,
                "meta": {"dataset": DATASET, "config": f"preference/train.jsonl.gz; domain={c['domain']}",
                         "revision": f"hf:{REV}; sha256:{FILES['preference/train.jsonl.gz']}",
                         "licence": LICENCE, "split": "train",
                         "orig_label": {"overall_preference": c["p"], "individual_scores": c["scores"],
                                        "domain": c["domain"], "language": c["lang"], "user_turns": c["turns"]},
                         "family": C.FAMILY, "edge": e, "defs": qid},
            })
    rows.sort(key=lambda r: r["rid"])
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, DEFS)
    st = C.summary(KEY, rows)
    print("stats:", dict(stats), "| decon:", len(hits), "| cross_v14:", len(xhits))
    print("strength:", dict(collections.Counter(abs(r["meta"]["orig_label"]["overall_preference"]) for r in rows)))
    print("domain:", dict(collections.Counter(r["meta"]["orig_label"]["domain"] for r in rows)))
    C.show_samples(rows, n=5, seed=12)
    C.append_manifest(C.manifest_record(
        KEY, DATASET, LICENCE, rows, "yesno",
        "Pairwise response preference with HUMAN expert labels (3 annotators, LLM use barred); general/STEM/code only; "
        "kept only when all annotators prefer the same response (|overall|>=2, plus 15% unanimous 'slightly better' "
        "rows tagged ambiguous); question names Response 1 or 2 (balanced) so position is not a cue; soft = annotator "
        "shares; multi-turn conversations kept whole (<=9k chars); decon drops prompts already in judge_helpsteer2.", st))


if __name__ == "__main__":
    main()
