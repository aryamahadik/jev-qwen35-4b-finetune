"""Build raw rows for casino (CaSiNo negotiation strategy annotations).

Source : HF kchawla123/casino, single split "train" (1030 dialogues), 'annotations' column
         (utterance-level strategy labels for 396 dialogues / 4615 utterances, human annotators).
         Texts are written by crowd workers (MTurk) negotiating with each other; labels are human annotations.
Licence: CC BY 4.0 -- HF dataset card YAML 'license: cc-by-4.0' and GitHub kushalchawla/CaSiNo LICENSE
         ('Attribution 4.0 International').
Rows   : one per annotated utterance (record id = dialogue index : utterance index).
         state = partner's most recent utterance (speaker-aligned via chat_logs ids) + the utterance.
         Single-label utterances -> 10-way choice (round-robin over labels, so non-strategic / small-talk are capped).
         Multi-label utterances  -> yes/no for one strategy (half yes = a gold label, half no = not among gold labels).
Soft   : null (the release has aggregated labels only, no per-annotator votes).
Deterministic (seed 20261101); HF revision pinned and raw snapshot kept (sha256) under cache/casino/.
"""
import collections
import hashlib
import json
import random
import re
import shutil
import statistics
import sys
from pathlib import Path

SEED = 20261101
KEY = "casino"
REPO = "kchawla123/casino"
REV = "290898d2d08b6591db17005504e40ce00ac1028e"
PARQUET = "data/train-00000-of-00001.parquet"
PARQUET_SHA = None  # filled on first snapshot; checked afterwards via cache/casino/SHA256
HERE = Path(__file__).resolve().parent
LEAN = HERE.parent
CACHE = HERE / "cache" / KEY
OUT = LEAN / "data" / "v13_parts" / "raw" / f"{KEY}.jsonl"
DEFS = LEAN / "data" / "v13_parts" / "defs" / f"{KEY}.json"

LICENCE = ("CC BY 4.0 (HF dataset card kchawla123/casino YAML 'license: cc-by-4.0'; "
           "GitHub kushalchawla/CaSiNo LICENSE file 'Attribution 4.0 International')")

MAX_ROWS = 500
N_YESNO = 100
N_CHOICE = MAX_ROWS - N_YESNO

NAME = {
    "small-talk": "small talk",
    "showing-empathy": "showing empathy",
    "promote-coordination": "promoting coordination",
    "no-need": "stating no need",
    "elicit-pref": "asking preferences",
    "uv-part": "undervaluing partner",
    "vouch-fair": "fairness appeal",
    "self-need": "own need",
    "other-need": "others' need",
    "non-strategic": "non-strategic",
}
OPTIONS = list(NAME.values())
STRATS = [c for c in NAME if c != "non-strategic"]
Q_CHOICE = "Which negotiation strategy does the Message use?"
Q_YESNO = 'Does the Message use the negotiation strategy "{}"?'

DEF = {
    "small talk": "Rapport-building talk not about the deal itself, such as greetings, pleasantries, or chatting about the camping trip, weather or activities.",
    "showing empathy": "The speaker acknowledges the partner's personal situation positively or sympathetically, showing understanding or concern for their needs or circumstances.",
    "promoting coordination": "The speaker promotes working together, for example an explicit promise to cooperate or a proposal framed as mutually beneficial for both sides.",
    "stating no need": "The speaker says they do not need an item, often citing their personal circumstances, signalling it can go to the partner.",
    "asking preferences": "The speaker tries to find out the partner's preferences, for example asking which items they need most or least.",
    "undervaluing partner": "The speaker undermines the partner's need for an item, suggesting they do not really require it or could get it elsewhere.",
    "fairness appeal": "The speaker appeals to fairness for their own benefit, calling a deal fair or objecting that an offer is unfair to them.",
    "own need": "The speaker argues that they personally need an item, giving a reason from their own situation, such as health or conditions.",
    "others' need": "The speaker argues for an item by citing the needs of other people, such as family members, children or group members.",
    "non-strategic": "The utterance uses none of the listed strategies, for example plainly stating an offer, accepting, or handling logistics.",
    "yes": "The Message uses the negotiation strategy named in the question, as defined by the CaSiNo strategy annotation scheme.",
    "no": "The Message does not use the negotiation strategy named in the question; it uses other strategies instead.",
}

words = lambda t: re.sub(r"[^a-z0-9]+", " ", t.lower()).split()
norm = lambda t: " ".join(words(t))


def snapshot():
    CACHE.mkdir(parents=True, exist_ok=True)
    local = CACHE / "train-00000-of-00001.parquet"
    card = CACHE / "README.md"
    shaf = CACHE / "SHA256"
    if not local.exists():
        from huggingface_hub import hf_hub_download
        shutil.copy(hf_hub_download(REPO, PARQUET, repo_type="dataset", revision=REV), local)
        shutil.copy(hf_hub_download(REPO, "README.md", repo_type="dataset", revision=REV), card)
    got = hashlib.sha256(local.read_bytes()).hexdigest()
    if shaf.exists():
        if shaf.read_text().split()[0] != got:
            sys.exit(f"sha256 mismatch for {local}: {got}")
    else:
        shaf.write_text(f"{got}  train-00000-of-00001.parquet  {REPO}@{REV}\n")
    return local, got


DEAL_ACTS = {"Submit-Deal", "Accept-Deal", "Reject-Deal", "Walk-Away"}


def speakers(chat_logs, ann):
    """Speaker id (mturk_agent_1/2) for each annotated utterance, by in-order alignment to chat_logs.
    Needed because consecutive annotated utterances are sometimes by the same speaker (30 cases)."""
    chats = [c for c in chat_logs if c["text"] not in DEAL_ACTS]
    out, j = [], 0
    for text, _ in ann:
        while j < len(chats) and chats[j]["text"].strip() != text.strip():
            j += 1
        if j == len(chats):
            sys.exit(f"cannot align annotated utterance to chat_logs: {text[:80]!r}")
        out.append(chats[j]["id"])
        j += 1
    return out


def main():
    import pandas as pd
    local, sha = snapshot()
    df = pd.read_parquet(local)

    stats = collections.Counter()
    seen = set()
    single = collections.defaultdict(list)
    multi = []
    for di, r in enumerate(df.itertuples(index=False)):
        ann = list(r.annotations)
        spk = speakers(r.chat_logs, ann) if ann else []
        for ui, (text, lab) in enumerate(ann):
            labs = [x for x in lab.split(",") if x]
            if not labs or any(x not in NAME for x in labs):
                stats["bad_label_drop"] += 1
                continue
            t = text.strip()
            if not (15 <= len(t) <= 4000):
                stats["len_drop"] += 1
                continue
            n = norm(t)
            if n in seen:
                stats["dup_drop"] += 1
                continue
            seen.add(n)
            # partner's most recent annotated utterance before this one (skip the speaker's own earlier turns)
            prev = next((ann[k][0].strip() for k in range(ui - 1, -1, -1) if spk[k] != spk[ui]), None)
            state = (f"Partner's previous message: {prev}\nMessage: {t}" if prev else f"Message: {t}")
            if len(state) > 4000:
                stats["len_drop"] += 1
                continue
            rec = {"rid": f"train:{di}:{ui}", "state": state, "labels": labs, "orig": lab}
            if len(labs) == 1:
                single[labs[0]].append(rec)
            else:
                multi.append(rec)

    rng = random.Random(SEED)

    def row(rec, q, opts, gold, qtype, asked=None):
        meta = {"dataset": "CaSiNo (Campsite Negotiation Dialogues) strategy annotations",
                "config": "default (annotations column)", "revision": REV, "parquet_sha256": sha,
                "licence": LICENCE, "split": "train", "orig_label": rec["orig"], "qtype": qtype,
                "all_labels": [NAME[x] for x in rec["labels"]]}
        if asked:
            meta["asked_label"] = asked
        return {"key": KEY, "rid": rec["rid"], "state": rec["state"], "instructions": q,
                "options": opts, "gold": gold, "soft": None, "meta": meta}

    # choice: round-robin over the 10 labels
    for k in sorted(single):
        rng.shuffle(single[k])
    labels = sorted(single)
    rows = []
    i = 0
    while len(rows) < N_CHOICE and any(single[k] for k in labels):
        k = labels[i % len(labels)]
        if single[k]:
            rec = single[k].pop()
            rows.append(row(rec, Q_CHOICE, OPTIONS, NAME[k], "choice"))
        i += 1

    # yes/no on multi-label utterances, alternating yes/no, cycling over strategies
    rng.shuffle(multi)
    n_yn = 0
    i = 0
    tries = 0
    while n_yn < N_YESNO and multi and tries < 10000:
        tries += 1
        want_yes = i % 2 == 0
        code = STRATS[(i // 2) % len(STRATS)]
        i += 1
        j = next((j for j, r in enumerate(multi) if (code in r["labels"]) == want_yes
                  and "non-strategic" not in r["labels"]), None)
        if j is None:
            continue
        rec = multi.pop(j)
        rows.append(row(rec, Q_YESNO.format(NAME[code]), ["yes", "no"], "yes" if want_yes else "no",
                        "yesno", NAME[code]))
        n_yn += 1

    rng.shuffle(rows)
    assert len({r["rid"] for r in rows}) == len(rows)
    for w, d in DEF.items():
        assert 8 <= len(d.split()) <= 35, (w, len(d.split()))
    assert set(OPTIONS) | {"yes", "no"} == set(DEF)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    DEFS.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    DEFS.write_text(json.dumps(DEF, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"wrote {len(rows)} rows -> {OUT}")
    print("filter stats:", dict(stats), "| single pool:", {k: len(v) + 0 for k, v in single.items()}, "| multi left:", len(multi))
    gold = collections.Counter(r["gold"] for r in rows)
    print("gold:", dict(gold), f"max share {max(gold.values()) / len(rows):.1%}")
    print("choice gold:", dict(collections.Counter(r["gold"] for r in rows if r["meta"]["qtype"] == "choice")))
    print("yesno asked:", dict(collections.Counter((r["meta"]["asked_label"], r["gold"]) for r in rows if r["meta"]["qtype"] == "yesno")))
    print("soft coverage: 0 (CaSiNo releases aggregated labels only, no annotator counts)")
    L = [len(r["state"]) for r in rows]
    print(f"chars min {min(L)} median {statistics.median(L)} mean {statistics.mean(L):.1f} max {max(L)}")


if __name__ == "__main__":
    main()
