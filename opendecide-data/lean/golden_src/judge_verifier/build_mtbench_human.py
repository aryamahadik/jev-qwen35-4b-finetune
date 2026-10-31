"""Build raw rows for mtbench_human: expert pairwise preference between two chat assistants (MT-Bench human judgments;
Zheng et al., NeurIPS 2023 Datasets & Benchmarks, "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena").

Source : HF lmsys/mt_bench_human_judgments pinned to revision f7d2896d2cc5d80f8b55c2bbc722613555233c25, the 'human'
         split parquet ONLY (the 'gpt4_pair' split holds GPT-4 judgments and is never downloaded). The release has no
         train/test split (counts as train).
Licence: CC BY 4.0 (dataset card README.md at the pinned revision: 'license: cc-by-4.0').
Texts  : the 80 MT-Bench questions (two turns each, written by the LMSYS team) and answers from GPT-4, GPT-3.5,
         Claude-v1, Vicuna-13B, Alpaca-13B and LLaMA-13B (the objects being judged).
Labels : HUMAN pairwise votes (model_a / model_b / tie) by 58 expert judges, mostly graduate students with expertise
         in each question's area. Votes for the same (question, model pair, turn) are pooled across judges and
         presentation orders; kept only if one outcome has a strict majority (> 50%); soft = real vote shares for the
         named assistant.
Rows   : one row per (question, model pair, turn). Presentation order (which model is 'Assistant A') is seeded-random;
         the question names A or B. yes = the named assistant's final answer won the majority; no = the other
         assistant won or the majority was a tie. Turn-2 rows show both full two-turn conversations and ask about the
         second answer.
Filters: states over 9,000 characters dropped (no truncation); decontamination (question text) against label-NLI, local train/dev/eval and JevBench; tie-majority rows
         capped at 20% so the yes share stays >= 40%.
Deterministic (seed 20261209). CPU only.
"""
import collections
import random
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _jv_common as C  # noqa: E402

KEY = "mtbench_human"
SEED = 20261209
REV = "f7d2896d2cc5d80f8b55c2bbc722613555233c25"
BASE = f"https://huggingface.co/datasets/lmsys/mt_bench_human_judgments/resolve/{REV}/"
FILES = {"data/human-00000-of-00001-25f4910818759289.parquet": "4877bc46a40929f4082c3c79593700fb897b1d6c7f4c473032694a01322f5769", "README.md": "4ef7507ea4d9b7b9e85db9c31742e5295c2f6d1b8c712d392705fd641c348fc4"}
LICENCE = (f"CC BY 4.0 (https://huggingface.co/datasets/lmsys/mt_bench_human_judgments/blob/{REV}/README.md, "
           "'license: cc-by-4.0')")
DATASET = "lmsys/mt_bench_human_judgments (human split)"
TIE_CAP = 0.20
MAX_STATE = 9000

Q = {
    "a": "Is Assistant A's final answer better than Assistant B's final answer?",
    "b": "Is Assistant B's final answer better than Assistant A's final answer?",
}


def defs_for(x, y):
    return {
        "yes": f"Assistant {x}'s final answer is better: judged on helpfulness, relevance, accuracy, depth, creativity "
               f"and level of detail (and, for a follow-up, how well it handles the follow-up request in context), it "
               f"beats Assistant {y}'s final answer.",
        "no": f"Assistant {x}'s final answer is not better: Assistant {y}'s final answer is better, or the two are "
              "about equally good (a tie).",
    }


DEFS = {"a": defs_for("A", "B"), "b": defs_for("B", "A")}


def conv_text(conv, name, turn):
    msgs = [m for m in conv]
    if turn == 1:
        q = msgs[0]["content"]
        a = msgs[1]["content"]
        return q, a
    return msgs, None


def render(turn, conv_a, conv_b):
    if turn == 1:
        return (f"User question:\n{C.clean_keep(conv_a[0]['content'])}\n\nAssistant A's answer:\n{C.clean_keep(conv_a[1]['content'])}"
                f"\n\nAssistant B's answer:\n{C.clean_keep(conv_b[1]['content'])}")
    lines = []
    for name, conv in (("A", conv_a), ("B", conv_b)):
        lines.append(f"Conversation with Assistant {name}:")
        for m in conv[:4]:
            role = "User" if m["role"] == "user" else f"Assistant {name}"
            lines.append(f"{role}: {C.clean_keep(m['content'])}")
        lines.append("")
    lines.append("The final answers being compared are each assistant's reply to the user's second message.")
    return "\n".join(lines)


def main():
    rng = random.Random(SEED)
    cache = C.CACHE / "mtbench"
    rel = "data/human-00000-of-00001-25f4910818759289.parquet"
    C.fetch(BASE + rel, cache / "human.parquet", FILES[rel])
    C.fetch(BASE + "README.md", cache / "README.md", FILES["README.md"])
    df = pd.read_parquet(cache / "human.parquet")
    stats = collections.Counter()
    groups = collections.defaultdict(list)
    convs = {}
    for r in df.itertuples(index=False):
        m1, m2 = sorted([r.model_a, r.model_b])
        k = (int(r.question_id), m1, m2, int(r.turn))
        if r.winner == "tie":
            v = "tie"
        else:
            w = r.model_a if r.winner == "model_a" else r.model_b
            v = "m1" if w == m1 else "m2"
        groups[k].append(v)
        ca, cb = list(r.conversation_a), list(r.conversation_b)
        convs.setdefault(k, {})
        convs[k][r.model_a] = ca
        convs[k][r.model_b] = cb
    stats["groups"] = len(groups)
    items = []
    for k, votes in sorted(groups.items()):
        c = collections.Counter(votes)
        top, n_top = c.most_common(1)[0]
        if n_top / len(votes) <= 0.5:
            stats["drop_no_majority"] += 1
            continue
        qid_, m1, m2, turn = k
        items.append({"k": k, "votes": votes, "top": top, "conv": convs[k], "m1": m1, "m2": m2, "turn": turn,
                      "q": convs[k][m1][0]["content"]})
    hits = C.decon({f"{i['k']}": [i["q"]] for i in items}, cache_name=KEY)
    items = [i for i in items if f"{i['k']}" not in hits]
    stats["after_decon"] = len(items)
    rng.shuffle(items)
    ties = [i for i in items if i["top"] == "tie"]
    wins = [i for i in items if i["top"] != "tie"]
    n_tie = min(len(ties), int(TIE_CAP / (1 - TIE_CAP) * len(wins)))
    items = wins + ties[:n_tie]
    stats["tie_rows"] = n_tie
    rows = []
    win_i = 0
    for it in sorted(items, key=lambda i: i["k"]):
        # presentation order: seeded coin flip for which model is Assistant A
        if rng.random() < 0.5:
            ma, mb = it["m1"], it["m2"]
        else:
            ma, mb = it["m2"], it["m1"]
        winner = None if it["top"] == "tie" else (it["m1"] if it["top"] == "m1" else it["m2"])
        if winner is None:
            qid = "a" if rng.random() < 0.5 else "b"
        else:
            # alternate between naming the winner and the loser so yes/no are balanced among decided rows
            name_winner = win_i % 2 == 0
            win_i += 1
            winner_letter = "a" if winner == ma else "b"
            qid = winner_letter if name_winner else ("b" if winner_letter == "a" else "a")
        named = ma if qid == "a" else mb
        gold = "yes" if winner == named else "no"
        n_named = sum(1 for v in it["votes"] if v != "tie" and (it["m1"] if v == "m1" else it["m2"]) == named)
        soft = {"yes": round(n_named / len(it["votes"]), 4), "no": round(1 - n_named / len(it["votes"]), 4)}
        state = render(it["turn"], it["conv"][ma], it["conv"][mb])
        if len(state) > MAX_STATE:
            stats["drop_long"] += 1
            continue
        e = "multi_hop" if it["turn"] == 2 else ("long_context" if len(state) > 4000 else None)
        if it["top"] == "tie":
            e = "ambiguous"
        qn, m1, m2, turn = it["k"]
        rows.append({
            "key": KEY, "rid": f"mtb-q{qn}-t{turn}-{m1}-vs-{m2}", "state": state, "instructions": Q[qid],
            "options": C.YN, "gold": gold, "soft": soft,
            "meta": {"dataset": DATASET, "config": "human split", "revision": f"hf:{REV}; sha256:{FILES[rel]}",
                     "licence": LICENCE, "split": "train",
                     "orig_label": {"question_id": qn, "turn": turn, "assistant_A": ma, "assistant_B": mb,
                                    "votes": collections.Counter(
                                        "tie" if v == "tie" else (it["m1"] if v == "m1" else it["m2"])
                                        for v in it["votes"])},
                     "family": C.FAMILY, "edge": e, "defs": qid},
        })
    for r in rows:
        r["meta"]["orig_label"]["votes"] = dict(r["meta"]["orig_label"]["votes"])
    # identical states (e.g. two models giving the same answer text) are kept once
    seen, uniq = set(), []
    for r in rows:
        k = C.norm(r["state"])
        if k in seen:
            stats["drop_dup_state"] += 1
            continue
        seen.add(k)
        uniq.append(r)
    rows = uniq
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, DEFS)
    st = C.summary(KEY, rows)
    print("stats:", dict(stats), "| decon:", len(hits))
    print("n votes:", dict(collections.Counter(len(g) for g in groups.values())))
    C.show_samples(rows, n=4, seed=19)
    C.append_manifest(C.manifest_record(
        KEY, DATASET, LICENCE, rows, "yesno",
        "Expert HUMAN pairwise preference (grad-student judges) between chat assistants on the 80 two-turn MT-Bench "
        "questions; votes pooled per (question, pair, turn), strict majority required, soft = vote shares; "
        "presentation order randomised; no = other assistant better OR tie (tie-majority rows capped at 20%, "
        "tagged ambiguous); turn-2 rows judge the follow-up answer in context. GPT-4-judge split never used.", st))


if __name__ == "__main__":
    main()
