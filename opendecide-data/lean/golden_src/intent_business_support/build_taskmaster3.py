"""Build golden rows for Taskmaster-3 / TicketTalk (movie-ticketing self-dialogs), TRAIN split only.

Source : GitHub google-research-datasets/Taskmaster @ d92cb6af, TM-3-2020/data/data_*.json; train ids are the last
         column of TM-3-2020/splits/train/train-*.tsv (dev/test split files are never downloaded).
Licence: CC BY 4.0 (TM-3-2020/README.md, COPYRIGHT NOTICE).
Texts  : self-dialogs written by crowd workers (both roles). 'Auto template' scenarios are partly pre-written by the
         dataset authors (agent turns) with crowd-written customer turns; they are capped at about a seventh of each class (repetitive agent turns).
Labels : outcome of the dialog from the annotated API calls plus the scenario the worker was given:
         yes = a book_tickets call with status 'success' and a scenario that is not a no-purchase scenario;
         no  = no book_tickets call at all AND a scenario whose instructions require that no tickets are bought
               ('Options Unavailable', 'Deferred Purchase', 'Theaters temporarily closed', 'No theaters nearby',
               'Auto template 4 no purchase as movie not playing locally'). Scenario/API conflicts are dropped.
Task   : purchase - yes/no: by the end of the conversation, has the customer actually bought movie tickets?
         One row per dialog; full dialog text as the state (<= 3500 chars); yes/no balanced.
Deterministic (seed 20261118).
"""
import collections
import json
import random

import _ibs_common as C
import _taskmaster_files as T

KEY = "taskmaster3"
SEED = 20261118
DATASET = "google-research-datasets/Taskmaster (TM-3-2020, TicketTalk)"
N_ROWS = 4000
MAX_CHARS = 3500
NO_SCEN = {"Options Unavailable", "Deferred Purchase", "Theaters temporarily closed", "No theaters nearby",
           "Auto template 4 no purchase as movie not playing locally"}
CHANGE_SCEN = {"Time Change", "Movie Change", "Tickets Change", "Theater Change", "Screening Change",
               "Misunderstanding", "Mishearing", "Change of movie with static variables",
               "Change of movie with predefined values", "Time Change with user made up values"}

PURCHASE_Q = "By the end of this conversation, has the customer actually bought movie tickets?"
PURCHASE_DEFS = {
    "yes": ("The agent completes a ticket purchase for the customer within this conversation, even if earlier "
            "choices were unavailable or changed along the way."),
    "no": ("No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is "
           "available or open, or the purchase is only saved or scheduled for later."),
}


def main():
    split_files = T.fetch_prefix("TM-3-2020/splits/train/")
    data_files = T.fetch_prefix("TM-3-2020/data/")
    T.fetch("TM-3-2020/README.md")
    train_ids = set()
    for p in split_files.values():
        with open(p, encoding="utf-8") as f:
            for line in f:
                train_ids.add(line.rstrip("\n").split("\t")[-1])
    rng = random.Random(SEED)
    stats = collections.Counter()
    pools = {("yes", False): [], ("yes", True): [], ("no", False): [], ("no", True): []}
    seen_ids = set()
    for rel in sorted(data_files):
        for d in json.load(open(data_files[rel])):
            cid = d["conversation_id"]
            if cid not in train_ids or cid in seen_ids:
                continue  # TRAIN ONLY
            seen_ids.add(cid)
            scen = d["scenario"].strip()
            auto = scen.lower().startswith("auto")
            books = [a for u in d["utterances"] for a in u.get("apis", []) if a["name"] == "book_tickets"]
            ok_book = any((a.get("response") or {}).get("status") == "success" for a in books)
            if scen in NO_SCEN:
                if books:
                    stats["no_scenario_with_booking_drop"] += 1
                    continue
                lab = "no"
            elif ok_book:
                lab = "yes"
            else:
                stats["unclear_outcome_drop"] += 1
                continue
            us = [u for u in d["utterances"] if u["text"].strip()]
            state = "\n".join(("Customer: " if u["speaker"] == "user" else "Agent: ") +
                              " ".join(u["text"].replace("\\r", " ").split()) for u in us)
            if not (200 <= len(state) <= MAX_CHARS) or len(us) < 6:
                stats["length_drop"] += 1
                continue
            pools[(lab, auto)].append((cid, scen, state))
    for k in sorted(pools):
        pools[k].sort()
        rng.shuffle(pools[k])
        stats[f"pool_{k[0]}_{'auto' if k[1] else 'free'}"] = len(pools[k])

    n_no_free = len(pools[("no", False)])
    n_no = min(N_ROWS // 2, n_no_free + min(len(pools[("no", True)]), n_no_free // 6))
    per = {}
    per[("no", False)] = min(n_no_free, n_no)
    per[("no", True)] = n_no - per[("no", False)]
    per[("yes", True)] = min(len(pools[("yes", True)]), per[("no", True)])
    per[("yes", False)] = n_no - per[("yes", True)]

    rows, seen = [], set()
    for (lab, auto), n in sorted(per.items()):
        k = 0
        for cid, scen, state in pools[(lab, auto)]:
            if k >= n:
                break
            nn = C.norm(state)
            if nn in seen:
                continue
            seen.add(nn)
            if lab == "no":
                edge = "hypothetical" if scen == "Deferred Purchase" else "negation"
            elif scen in CHANGE_SCEN:
                edge = "exception"
            elif len(state) > 2000:
                edge = "long_context"
            else:
                edge = None
            rows.append({
                "key": KEY, "rid": f"{cid}_purchase", "state": state, "instructions": PURCHASE_Q,
                "options": ["yes", "no"], "gold": lab, "soft": None,
                "meta": {"dataset": DATASET, "config": "TM-3-2020/data; train ids from splits/train; task=purchase",
                         "revision": f"git:{T.COMMIT}; sha256 per file in _taskmaster_files.SHA",
                         "licence": T.licence("TM-3-2020"), "split": "train",
                         "orig_label": {"scenario": scen, "book_tickets_success": lab == "yes"},
                         "family": C.FAMILY, "edge": edge, "defs": "purchase"}})
            k += 1
    rng.shuffle(rows)
    C.write_rows(rows, KEY)
    C.write_defs(PURCHASE_DEFS, KEY, "purchase")
    print(dict(stats))
    print("scenarios:", collections.Counter((r["gold"], r["meta"]["orig_label"]["scenario"]) for r in rows).most_common(12))
    C.report(rows)


if __name__ == "__main__":
    main()
