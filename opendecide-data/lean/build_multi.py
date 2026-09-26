"""MULTI: several customer records in one state, the question asks about ONE of them (a documented Jev failure:
accuracy 0.96 -> 0.44 with 5 distractor tickets, github.com/dopeCape/typesafe-ai-test).

eval_multi  target = an in-scope ID core eval message; 3-5 other eval messages as distractor tickets, preferring
            ones whose gold label is among the target's options (the tempting wrong answers). Eval-only format:
            "Ticket #K7Q | customer: Name" headers; "Pick the category that fits ticket #K7Q best." and a yes/no
            about a distractor's label (gold 0) or the target's own label (gold 1).
train_v04   = train_v03 + 600 multi-record states from Banking77/CLINC train messages in a DIFFERENT, train-only
            format ("[message 3] from Name:" + "Which topic best matches message 3?"), choice + yes/no each.
"""
from __future__ import annotations

import json
import string

from build_data import (NAMES, NONE_EVAL, NONE_TRAIN, OUT, TRAIN_CHOICE, Builder, choice_options, frame, intent_prop,
                        load_keys, load_sources, nearest_labels, norm, rng)
from build_train_v03 import NEW_AFF


def tid(rr):
    return "".join(rr.choice(string.ascii_uppercase) for _ in range(1)) + str(rr.randint(1, 9)) + rr.choice(string.ascii_uppercase)


def main():
    ev = [json.loads(l) for l in open(OUT / "eval.jsonl")]
    core = [r for r in ev if r["track"] == "ID" and r["qtype"] == "choice" and r["gold"] != NONE_EVAL]
    msg = lambda r: r["state"].split("\n", 1)[1]
    E = Builder("eval_multi")
    for r in core:
        rr = rng("eval_multi", r["id"])
        others = [o for o in core if o["source"] == r["source"] and o["gold"] != r["gold"]]
        tempting = [o for o in others if o["gold"] in r["options"]]
        rr.shuffle(tempting)
        rest = [o for o in others if o not in tempting]
        rr.shuffle(rest)
        n = rr.randint(3, 5)
        dis = (tempting[:2] + rest)[:n]
        tickets = [(r, True)] + [(d, False) for d in dis]
        rr.shuffle(tickets)
        ids = set()
        blocks, target_id, dis_labels = [], None, []
        for t, is_target in tickets:
            k = tid(rr)
            while k in ids:
                k = tid(rr)
            ids.add(k)
            blocks.append(f"Ticket #{k} | customer: {rr.choice(NAMES)}\n{msg(t)}")
            if is_target:
                target_id = k
            elif t["gold"] in r["options"]:
                dis_labels.append(t["gold"])
        state = "Support inbox export\n\n" + "\n\n".join(blocks)
        meta = {"n_tickets": len(tickets), "clean_id": r["id"], "tempting_in_options": len(dis_labels)}
        E.row(group=r["group_id"], state=state, source=r["source"], track="MULTI", qtype="choice",
              instructions=f"Pick the category that fits ticket #{target_id} best.", options=r["options"], gold=r["gold"],
              role="choice", meta=meta)
        if dis_labels and rr.random() < 0.5:
            x, g = dis_labels[0], 0
        else:
            x, g = r["gold"], 1
        who = "customer" if r["source"] == "banking77" else "user"
        E.row(group=r["group_id"], state=state, source=r["source"], track="MULTI", qtype="noul",
              instructions=f"Is the {who} in ticket #{target_id} asking about {x}?", options=None, gold=g, role="aff",
              meta={**meta, "asks_about_distractor": g == 0})
    rows = E.rows
    with open(OUT / "eval_multi.jsonl", "w") as f:
        for x in rows:
            f.write(json.dumps(x) + "\n")
    calls = {}
    for x in rows:
        calls.setdefault(x["call_id"], {"call_id": x["call_id"], "state": x["state"], "row_ids": []})["row_ids"].append(x["id"])
    with open(OUT / "eval_multi_calls.jsonl", "w") as f:
        for c in calls.values():
            f.write(json.dumps(c) + "\n")
    print(f"eval_multi: {len(rows)} rows, {len(calls)} calls, yes-rate "
          f"{sum(x['gold'] == 1 for x in rows if x['qtype'] == 'noul') / sum(x['qtype'] == 'noul' for x in rows):.2f}")

    # ---------------- train_v04 = v03 + train-only multi-record rows ----------------
    S = load_sources()
    keys = {"banking77": S["b_keys"], "clinc150": S["c_keys"]}
    near = {ds: nearest_labels(keys[ds]) for ds in keys}
    intents = {ds: [k for k, v in keys[ds].items() if v.get("kind") == "intent"] for ds in keys}
    eval_texts = {norm(msg(r)) for r in ev if r["track"] == "ID"}
    pool = {"banking77": [x for x in S["b_tr"] if norm(x["text"]) not in eval_texts],
            "clinc150": [x for x in S["c_tr"] if x["label"] != "oos" and norm(x["text"]) not in eval_texts]}
    T = Builder("train")
    r0 = rng("v04", "multi")
    for j in range(600):
        src = "banking77" if j % 2 == 0 else "clinc150"
        rr = rng("v04", "multi", j)
        target = rr.choice(pool[src])
        opts = choice_options(target["label"], keys[src], near[src], rr, oos_pool=intents[src])
        opt_keys = [keys[src][o]["key"] for o in opts] + [NONE_TRAIN]
        tempting = [x for x in rr.sample(pool[src], 400) if x["label"] in opts and x["label"] != target["label"]][:2]
        others = [x for x in rr.sample(pool[src], 20) if x["label"] != target["label"]]
        dis = (tempting + others)[: rr.randint(2, 5)]
        msgs = [target] + dis
        rr.shuffle(msgs)
        k = msgs.index(target) + 1
        state = "Conversation log\n" + "\n".join(f"[message {i + 1}] from {rr.choice(NAMES)}: {m['text']}" for i, m in enumerate(msgs))
        group = f"g:{src}:multi:{target['source_id']}"
        T.row(group=group, state=state, source=src, track="L3", qtype="choice",
              instructions=rr.choice(TRAIN_CHOICE["intent"]).replace("this customer message", f"message {k}").replace("this request", f"message {k}"),
              options=opt_keys, gold=keys[src][target["label"]]["key"], role="choice", meta={"arm": "multi"})
        if tempting and rr.random() < 0.5:
            x_key, g = keys[src][tempting[0]["label"]]["key"], 0
        else:
            x_key, g = keys[src][target["label"]]["key"], 1
        p = intent_prop(src, x_key).replace("the customer is", f"the sender of message {k} is").replace("the user is", f"the sender of message {k} is")
        T.row(group=group, state=state, source=src, track="L3", qtype="noul", instructions=frame(rr.choice(NEW_AFF), p),
              options=None, gold=g, role="aff", meta={"arm": "multi"})
    base = [json.loads(l) for l in open(OUT / "train_v03.jsonl")]
    ids = {x["id"] for x in base}
    new = [x for x in T.rows if x["id"] not in ids]
    for x in new:
        assert "ticket" not in x["instructions"].lower() and "Ticket #" not in x["state"]
    with open(OUT / "train_v04.jsonl", "w") as f:
        for x in base + new:
            f.write(json.dumps(x) + "\n")
    (OUT / "train_v04_relations.jsonl").write_text((OUT / "train_v03_relations.jsonl").read_text())
    print(f"train_v04: {len(base) + len(new)} rows ({len(new)} multi-record rows added)")
    print("example train instruction:", new[0]["instructions"], "|", new[1]["instructions"])


if __name__ == "__main__":
    main()
