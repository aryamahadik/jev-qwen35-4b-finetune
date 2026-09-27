"""Build raw rows for convabuse (ConvAbuse: abuse toward conversational agents, Cercas Curry et al., EMNLP 2021).

Source : GitHub amandacurry/convabuse, 2_splits/ConvAbuseEMNLPtrain.csv at commit
         c0a9469f48956e868276c605d499010ea3c7c0d0 (2024-01-11, the commit that added LICENSE). Snapshot pinned by sha256
         under cache/convabuse/. The valid and test splits are never downloaded.
Licence: CC BY 4.0, repo LICENSE file ("Attribution 4.0 International"); GitHub API licence key cc-by-4.0.
Texts  : real user messages typed to two deployed chatbots (CarbonBot on Facebook Messenger and an ELIZA web bot);
         labels by expert annotators (gender-studies / psychology trained), 2-7 per item. No model-written text.
State  : the conversation window the annotators saw: previous chatbot turn, previous user turn, chatbot turn, and the
         final user message (the one that was labelled). "_" placeholders (conversation start) are omitted.
Label sets (each source record is used for exactly one question):
  abuse    yes/no  : majority of annotators rate -1..-3 (abusive) vs 1/0 (not abusive / ambiguous), as in the paper's
                     binary task; ties dropped. soft = share of annotators voting abusive.
  severity choice  : the 5-point is_abuse scale (1, 0, -1, -2, -3); gold = unique plurality; soft = vote shares.
  type     choice  : among annotators who rated the item abusive, abuse type (sexual harassment, sexism, intellectual,
                     homophobic, racist, ableist; no type ticked = general); majority-abusive items only; records
                     where any annotator ticked "transphobic" (no option for it; header mislabels annotators 7-8's
                     transphobic columns as Annotator6_*) are kept out of this task so that tick is never miscounted
                     as general; each
                     annotator's vote split evenly over the types they ticked; gold = unique argmax with share >= 0.5.
  target   choice  : among abusive raters, target (system/agent, individual, generalised); majority-abusive items only;
                     gold = unique argmax with share >= 0.5.
Repeat annotations ("0, 0" cells from the intra-annotator agreement study) use the annotator's first judgement.
Emoji  : the CSV stores emoji as <span class='emoji-bytes' data-emoji-bytes='[..]'> HTML; decoded back to the emoji.
Dedup  : exact normalised state dedup, and at most 2 records per identical final user message (so e.g. at most two
         "fuck you" rows, each with a different context); duplicates keep the copy with the most annotators.
Deterministic (seed 20261101).
"""
import collections
import hashlib
import json
import random
import re
import sys
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20261101
MAX_ROWS = 500
KEY = "convabuse"
HERE = Path(__file__).resolve().parent
LEAN = HERE.parent
CACHE = HERE / "cache" / KEY
OUT = LEAN / "data" / "v13_parts" / "raw" / f"{KEY}.jsonl"

COMMIT = "c0a9469f48956e868276c605d499010ea3c7c0d0"
BASE = f"https://raw.githubusercontent.com/amandacurry/convabuse/{COMMIT}/"
FILES = {
    "2_splits/ConvAbuseEMNLPtrain.csv": "23abab3eff791d0e8cac681cec15a5ef299ed052699e4fca762d1d4640c36936",
    "LICENSE": "9e5f1b3c610b9c2da5c313bf81d577a7d1acec686bdb0384edefa6df0f90cd94",
    "README.md": "d4b9ef012143b89b00e8a02d1e0eee4b5179b4270f895c9b02de2101a6e34c05",
}
LICENCE = ("CC BY 4.0 (repo LICENSE file 'Attribution 4.0 International', github.com/amandacurry/convabuse/blob/"
           f"{COMMIT}/LICENSE; GitHub licence key cc-by-4.0)")

ANNS = [f"Annotator{i}" for i in range(1, 9)]
SEV = ["1", "0", "-1", "-2", "-3"]
ABUSIVE = ["-1", "-2", "-3"]
SEV_NAME = {"1": "not abusive", "0": "ambiguous", "-1": "mildly abusive", "-2": "strongly abusive",
            "-3": "very strongly abusive"}
TYPES = {"sex_harassment": "sexual harassment", "sexist": "sexism", "intellectual": "intellectual insult",
         "homophobic": "homophobia", "racist": "racism", "ableist": "ableism"}
GENERAL = "general insult or hostility"
TARGETS = {"target.system": "the chatbot", "target.individual": "another person",
           "target.generalised": "a group of people"}

TASKS = {
    "abuse": {"q": "Is the user's last message abusive?", "options": ["yes", "no"]},
    "severity": {"q": "How abusive is the user's last message?",
                 "options": [SEV_NAME[s] for s in SEV]},
    "type": {"q": "What kind of abuse is in the user's last message?",
             "options": list(TYPES.values()) + [GENERAL]},
    "target": {"q": "Who is the abuse in the user's last message aimed at?",
               "options": list(TARGETS.values())},
}
# per-task row budgets and per-label caps (filled in this order; each record used once)
TARGET_MAX_SYSTEM_SHARE = 0.4
SEV_PER_LABEL = 32
TYPE_ROWS = 110
ABUSE_YES_MAX = 200
ABUSE_NO_SHARE = 0.6  # "no" may fill up to 60% of the yes/no task
MAX_PER_USER_MSG = 2


def fetch(rel, sha):
    path = CACHE / Path(rel).name
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(BASE + rel, path)
    got = hashlib.sha256(path.read_bytes()).hexdigest()
    if got != sha:
        sys.exit(f"sha256 mismatch for {path}: {got}")
    return path


def norm(t):
    return re.sub(r"\s+", " ", t).strip().lower()


def cell(r, a, c):
    v = r.get(f"{a}_{c}", "").strip()
    return None if v == "" else int(v.split(",")[0])


EMOJI_SPAN = re.compile(r"<span class='emoji-bytes' data-emoji-bytes='\[([0-9, ]+)\]'></span>")


def fix_emoji(t):
    """The export stores emoji as HTML spans holding their UTF-8 bytes; turn them back into the emoji."""
    return EMOJI_SPAN.sub(lambda m: bytes(int(b) for b in m.group(1).split(",")).decode("utf-8", "replace"), t)


def fmt_state(r):
    lines = []
    for col, who in (("prev_agent", "Chatbot"), ("prev_user", "User"), ("agent", "Chatbot"), ("user", "User")):
        t = fix_emoji(r[col]).strip()
        if t and t != "_":
            lines.append(f"{who}: {t}")
    return "\n".join(lines)


def round_robin(pools, n, cap_share=None):
    """Take up to n rows round-robin over labels; optional per-label cap as share of n."""
    labels = sorted(pools)
    cap = None if cap_share is None else max(1, int(cap_share * n))
    taken = collections.Counter()
    out, i = [], 0
    while len(out) < n and any(pools[k] and (cap is None or taken[k] < cap) for k in labels):
        k = labels[i % len(labels)]
        if pools[k] and (cap is None or taken[k] < cap):
            out.append(pools[k].pop())
            taken[k] += 1
        i += 1
    return out


def main():
    paths = {rel: fetch(rel, sha) for rel, sha in FILES.items()}
    df = pd.read_csv(paths["2_splits/ConvAbuseEMNLPtrain.csv"], dtype=str, keep_default_na=False)
    recs = df.to_dict("records")
    stats = collections.Counter()

    items = []
    for r in recs:
        rid = str(int(float(r["example_id"])))
        state = fmt_state(r)
        user = fix_emoji(r["user"]).strip()
        if not (15 <= len(state) <= 4000) or user in ("", "_"):
            stats["len_drop"] += 1
            continue
        ann = [a for a in ANNS if cell(r, a, "is_abuse.1") is not None]
        sev_of = {}
        for a in ann:
            v = [cell(r, a, f"is_abuse.{s}") for s in SEV]
            assert sum(v) == 1, (rid, a, v)
            sev_of[a] = SEV[v.index(1)]
        n = len(ann)
        votes = collections.Counter(sev_of.values())
        n_ab = sum(votes[s] for s in ABUSIVE)
        ab_ann = [a for a in ann if sev_of[a] in ABUSIVE]
        type_share = collections.Counter()
        tgt_share = collections.Counter()
        for a in ab_ann:
            ts = [TYPES[t] for t in TYPES if cell(r, a, t) == 1] or [GENERAL]
            for t in ts:
                type_share[t] += 1 / len(ts)
            gs = [TARGETS[t] for t in TARGETS if cell(r, a, t) == 1]
            for t in gs:
                tgt_share[t] += 1 / len(gs)
        trans = any(str(v).strip().startswith("1") for k, v in r.items() if "transphobic" in k)
        items.append({"rid": rid, "state": state, "trans": trans, "user": norm(user), "n": n, "votes": votes, "n_ab": n_ab,
                      "ab_ann": len(ab_ann), "type_share": type_share, "tgt_share": tgt_share,
                      "sev_of": {a: sev_of[a] for a in ann}, "bot": r["bot"]})

    # dedup: exact normalised state, and at most MAX_PER_USER_MSG records per identical final user message
    rng = random.Random(SEED)
    items.sort(key=lambda x: int(x["rid"]))
    rng.shuffle(items)
    # prefer the copy with more annotators (more reliable soft label) for duplicated messages
    items.sort(key=lambda x: -x["n"])
    seen_state, per_msg, uniq = set(), collections.Counter(), []
    for it in items:
        ns = norm(it["state"])
        if ns in seen_state:
            stats["dup_state_drop"] += 1
            continue
        if per_msg[it["user"]] >= MAX_PER_USER_MSG:
            stats["dup_msg_cap_drop"] += 1
            continue
        seen_state.add(ns)
        per_msg[it["user"]] += 1
        uniq.append(it)
    items = uniq
    items.sort(key=lambda x: int(x["rid"]))
    rng.shuffle(items)

    def unique_argmax(c, min_share=None, total=None):
        m = c.most_common()
        if not m or (len(m) > 1 and abs(m[0][1] - m[1][1]) < 1e-9):
            return None
        if min_share is not None and m[0][1] / total < min_share:
            return None
        return m[0][0]

    def soft_of(c, options, total):
        return {o: round(c.get(o, 0) / total, 4) for o in options}

    used = set()
    rows = {}

    def emit(it, task, gold, soft, orig):
        used.add(it["rid"])
        return {"key": KEY, "rid": it["rid"], "state": it["state"], "instructions": TASKS[task]["q"],
                "options": TASKS[task]["options"], "gold": gold, "soft": soft,
                "meta": {"dataset": "ConvAbuse (Cercas Curry, Abercrombie & Rieser, EMNLP 2021)",
                         "config": f"2_splits/ConvAbuseEMNLPtrain.csv; task={task}; bot={it['bot']}",
                         "revision": f"github:{COMMIT}", "licence": LICENCE, "split": "train",
                         "orig_label": orig}}

    majority_abusive = [it for it in items if it["n_ab"] * 2 > it["n"] and it["ab_ann"] > 0]

    # 1) target: all non-system golds, system capped at 40%
    pools = collections.defaultdict(list)
    for it in majority_abusive:
        g = unique_argmax(it["tgt_share"], 0.5, it["ab_ann"])
        if g is None:
            continue
        pools[g].append(it)
    for k in pools:
        pools[k].reverse()
    sys_lab = TARGETS["target.system"]
    rare = [(it, k) for k in sorted(pools) if k != sys_lab for it in pools[k]]
    n_sys = min(len(pools[sys_lab]), int(TARGET_MAX_SYSTEM_SHARE / (1 - TARGET_MAX_SYSTEM_SHARE) * len(rare)))
    target_rows = rare + [(it, sys_lab) for it in pools[sys_lab][::-1][:n_sys]]
    rows["target"] = [emit(it, "target", g, soft_of(it["tgt_share"], TASKS["target"]["options"], it["ab_ann"]),
                           {"abusive_raters": it["ab_ann"], "raters": it["n"],
                            "target_votes": {k: round(v, 3) for k, v in it["tgt_share"].items()}})
                      for it, g in target_rows]

    # 2) severity: round-robin over the 5-point scale, SEV_PER_LABEL each
    pools = collections.defaultdict(list)
    for it in items:
        if it["rid"] in used:
            continue
        g = unique_argmax(it["votes"])
        if g is None:
            continue
        pools[g].append(it)
    sev_rows = []
    for k in pools:
        pools[k] = pools[k][::-1]
        take = pools[k][-SEV_PER_LABEL:]
        pools[k] = take
    for it in round_robin(pools, SEV_PER_LABEL * len(SEV)):
        g = unique_argmax(it["votes"])
        sev_rows.append(emit(it, "severity", SEV_NAME[g],
                             {SEV_NAME[s]: round(it["votes"].get(s, 0) / it["n"], 4) for s in SEV},
                             {"is_abuse_votes": {s: it["votes"].get(s, 0) for s in SEV}, "raters": it["n"]}))
    rows["severity"] = sev_rows

    # 3) type: majority-abusive items, round-robin, no label above 40%
    pools = collections.defaultdict(list)
    for it in majority_abusive:
        if it["rid"] in used or it["trans"]:
            continue
        g = unique_argmax(it["type_share"], 0.5, it["ab_ann"])
        if g is None:
            continue
        pools[g].append(it)
    for k in pools:
        pools[k].reverse()
    type_rows = []
    for it in round_robin(pools, TYPE_ROWS, cap_share=0.4):
        g = unique_argmax(it["type_share"], 0.5, it["ab_ann"])
        type_rows.append(emit(it, "type", g, soft_of(it["type_share"], TASKS["type"]["options"], it["ab_ann"]),
                              {"abusive_raters": it["ab_ann"], "raters": it["n"],
                               "type_votes": {k: round(v, 3) for k, v in it["type_share"].items()}}))
    rows["type"] = type_rows

    # 4) abuse yes/no: remaining majority-abusive = yes; strict-majority non-abusive = no (same count)
    budget = MAX_ROWS - sum(len(v) for v in rows.values())
    yes = [it for it in items if it["rid"] not in used and it["n_ab"] * 2 > it["n"]]
    no = [it for it in items if it["rid"] not in used and it["n_ab"] * 2 < it["n"]]
    n_yes = min(len(yes), ABUSE_YES_MAX, budget // 2)
    n_no = min(len(no), budget - n_yes, int(n_yes * ABUSE_NO_SHARE / (1 - ABUSE_NO_SHARE)))
    ab_rows = []
    for it, g in [(x, "yes") for x in yes[:n_yes]] + [(x, "no") for x in no[:n_no]]:
        p = it["n_ab"] / it["n"]
        ab_rows.append(emit(it, "abuse", g, {"yes": round(p, 4), "no": round(1 - p, 4)},
                            {"is_abuse_votes": {s: it["votes"].get(s, 0) for s in SEV}, "raters": it["n"]}))
    rows["abuse"] = ab_rows

    out = [r for t in ("abuse", "severity", "type", "target") for r in rows[t]][:MAX_ROWS]
    assert len({r["rid"] for r in out}) == len(out)
    rng.shuffle(out)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"source train records={len(recs)} usable after filters/dedup={len(items)} "
          f"majority-abusive={len(majority_abusive)} drops={dict(stats)}")
    print(f"wrote {len(out)} rows -> {OUT}")
    for t in ("abuse", "severity", "type", "target"):
        rs = [r for r in out if r["instructions"] == TASKS[t]["q"]]
        if not rs:
            continue
        cnt = collections.Counter(r["gold"] for r in rs)
        agree = sum(max(r["soft"], key=r["soft"].get) == r["gold"] for r in rs)
        print(f"  [{t}] n={len(rs)} soft argmax==gold {agree}/{len(rs)}; per label:",
              {k: f"{v} ({v / len(rs):.0%})" for k, v in cnt.most_common()})
    cnt = collections.Counter(r["gold"] for r in out)
    print("overall top label share:", f"{cnt.most_common(1)[0][0]} {cnt.most_common(1)[0][1] / len(out):.1%}")
    print(f"soft coverage: {sum(r['soft'] is not None for r in out)}/{len(out)}")
    lens = [len(r["state"]) for r in out]
    print(f"state length chars: min={min(lens)} median={int(np.median(lens))} mean={np.mean(lens):.0f} max={max(lens)}")


if __name__ == "__main__":
    main()
