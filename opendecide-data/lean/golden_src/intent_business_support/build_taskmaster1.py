"""Build golden rows for Taskmaster-1 (Byrne et al., EMNLP 2019), TRAIN only.

Source : GitHub google-research-datasets/Taskmaster @ d92cb6af, TM-1-2019/self-dialogs.json (only ids listed in
         train-dev-test/train.csv; dev.csv/test.csv never downloaded) + TM-1-2019/woz-dialogs.json (the spoken two-person
         dialogs have no official split, so they count as train).
Licence: CC BY 4.0 (TM-1-2019/README.md, COPYRIGHT NOTICE).
Texts  : written self-dialogs by crowd workers; two-person WOz dialogs (crowd user, trained call-centre operator as
         assistant; user speech transcribed, then checked and corrected by human transcribers).
Labels : API-argument span annotations by two crowd annotators per dialog (both kept in the release). Only spans where
         at least two annotations agree exactly are used.
Tasks  : status - yes/no on an ASSISTANT turn: is "<value>" confirmed for the customer's transaction?
                  no  = agreed '<slot>.reject' span (value unavailable / not possible) and the turn states unavailability;
                  yes = agreed '<slot>.accept' span in a turn that confirms the transaction (booked/ordered/set...), is not
                        a read-back question and carries no reject annotation from anyone. Mixed turns (an agreed
                        reject and an agreed accept) give either polarity (edge 'exception').
         role   - yes/no on a USER turn: does "<span>" give the <slot role>? yes = agreed role; no = a clearly different
                  sibling role of the same vertical (e.g. pickup vs destination, restaurant name vs name on the
                  reservation, guests vs time), never one any annotator gave the span. Fuzzy pairs (topping vs
                  preference, drink vs preference) are not used.
         One row per source turn; each turn is used by one task at most.
Deterministic (seed 20261116).
"""
import collections
import json
import random
import re

import _ibs_common as C
import _taskmaster_files as T

KEY = "taskmaster1"
SEED = 20261116
DATASET = "google-research-datasets/Taskmaster (TM-1-2019)"
N_STATUS = 3200
N_ROLE = 3200
CONTEXT = 3  # turns shown (ending with the target turn)

VERT = {
    "uber_lyft": "ride booking",
    "movie_ticket": "movie ticket order",
    "restaurant_reservation": "restaurant reservation",
    "coffee_ordering": "coffee order",
    "pizza_ordering": "pizza order",
    "auto_repair": "car repair appointment",
}
ROLE_TXT = {
    "uber_lyft.location.from": "pickup location (where the ride starts)",
    "uber_lyft.location.to": "destination (where the ride should drop the customer off)",
    "uber_lyft.time.pickup": "pickup time",
    "uber_lyft.time.dropoff": "time the customer needs to arrive at the destination",
    "movie_ticket.name.movie": "title of the movie",
    "movie_ticket.name.theater": "name of the movie theater",
    "movie_ticket.location.theater": "location of the theater (city, neighbourhood or address)",
    "movie_ticket.time.start": "movie showtime",
    "movie_ticket.num.tickets": "number of tickets",
    "restaurant_reservation.name.restaurant": "name of the restaurant",
    "restaurant_reservation.name.reservation": "name the reservation should be under",
    "restaurant_reservation.location.restaurant": "location of the restaurant (city, area or address)",
    "restaurant_reservation.num.guests": "number of people in the party",
    "restaurant_reservation.time.reservation": "time of the reservation",
    "auto_repair.name.store": "name of the repair shop",
    "auto_repair.name.customer": "customer's own name",
    "auto_repair.name.vehicle": "make or model of the vehicle",
    "auto_repair.year.vehicle": "model year of the vehicle",
    "auto_repair.reason.appt": "problem or service the car is being brought in for",
    "pizza_ordering.name.store": "name of the pizza place",
    "pizza_ordering.location.store": "location of the pizza place",
    "pizza_ordering.size.pizza": "size of the pizza",
    "pizza_ordering.type.crust": "type of crust",
    "coffee_ordering.size.drink": "size of the drink",
    "coffee_ordering.name.drink": "drink being ordered",
}
# clearly distinct sibling roles asked for 'no' rows
SIBLINGS = {
    "uber_lyft.location.from": ["uber_lyft.location.to"],
    "uber_lyft.location.to": ["uber_lyft.location.from"],
    "uber_lyft.time.pickup": ["uber_lyft.time.dropoff"],
    "uber_lyft.time.dropoff": ["uber_lyft.time.pickup"],
    "movie_ticket.name.movie": ["movie_ticket.name.theater"],
    "movie_ticket.name.theater": ["movie_ticket.name.movie"],
    "movie_ticket.location.theater": ["movie_ticket.name.theater"],
    "movie_ticket.time.start": ["movie_ticket.num.tickets"],
    "movie_ticket.num.tickets": ["movie_ticket.time.start"],
    "restaurant_reservation.name.restaurant": ["restaurant_reservation.name.reservation"],
    "restaurant_reservation.name.reservation": ["restaurant_reservation.name.restaurant"],
    "restaurant_reservation.num.guests": ["restaurant_reservation.time.reservation"],
    "restaurant_reservation.time.reservation": ["restaurant_reservation.num.guests"],
    "restaurant_reservation.location.restaurant": ["restaurant_reservation.name.restaurant"],
    "auto_repair.name.store": ["auto_repair.name.customer"],
    "auto_repair.name.customer": ["auto_repair.name.store"],
    "auto_repair.name.vehicle": ["auto_repair.year.vehicle", "auto_repair.name.customer"],
    "auto_repair.year.vehicle": ["auto_repair.name.vehicle"],
    "auto_repair.reason.appt": ["auto_repair.name.vehicle"],
    "pizza_ordering.size.pizza": ["pizza_ordering.type.crust"],
    "pizza_ordering.type.crust": ["pizza_ordering.size.pizza"],
    "pizza_ordering.name.store": ["pizza_ordering.location.store"],
    "pizza_ordering.location.store": ["pizza_ordering.name.store"],
    "coffee_ordering.size.drink": ["coffee_ordering.name.drink"],
    "coffee_ordering.name.drink": ["coffee_ordering.size.drink"],
}

STATUS_Q = 'According to the assistant\'s last message, is "{span}" confirmed for the customer\'s {vert}?'
ROLE_Q = 'In the customer\'s last message, does "{span}" give the {role} for this {vert}?'
STATUS_DEFS = {
    "yes": ("The assistant's last message confirms this value as booked, ordered, scheduled or available for the "
            "customer's transaction."),
    "no": ("The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be "
           "done, even if it offers an alternative or confirms other parts of the order."),
}
ROLE_DEFS = {
    "yes": ("The quoted phrase in the customer's last message refers to exactly the detail named in the question, "
            "even if the customer mentions it to rule it out or change it."),
    "no": ("The quoted phrase states a different detail of the order (for example the destination rather than the "
           "pickup point, or the party size rather than the time), so it does not give the detail named."),
}

UNAVAIL = re.compile(r"\b(not|no|sorry|unavailable|sold out|out of|full|fully|booked up|closed|unable|cannot|can't|"
                     r"couldn't|don't|doesn't|isn't|aren't|wasn't|won't|unfortunately|only|nothing|none|discontinued|"
                     r"ran out|run out)\b|n't", re.I)
CONFIRM = re.compile(r"\b(booked|reserved|confirmed|placed|scheduled|ordered|all set|you're set|you are set|set up|"
                     r"have you down|got you down|put you down|purchased|on (its|the) way|will be ready|is ready|"
                     r"has been (made|placed|booked|reserved|scheduled|ordered|confirmed)|your (order|table|ride|"
                     r"reservation|tickets|appointment) (is|has|will)|appointment (is|has been)|made (a|the|your) "
                     r"(reservation|appointment|order))\b", re.I)
NEG = re.compile(r"\b(not|no|never|none|nothing|neither|nor)\b|n't|\bcannot\b", re.I)
SUFFIX = re.compile(r"\.(accept|reject)$")
ONTO = {}  # vertical id -> required + optional slots (filled from ontology.json in main)


def slot_ok(name):
    """Only slot-level status labels whose slot is in TM-1 ontology.json (not vertical-level 'pizza_ordering.accept')."""
    vert = name.split(".")[0]
    slot = SUFFIX.sub("", name)[len(vert) + 1:]
    return slot in ONTO.get(vert, ())


def agreed_spans(u):
    """Spans whose (>= 2) annotations are identical. Returns list of (text, full_name, start)."""
    out = []
    for s in u.get("segments", []):
        ns = [a["name"] for a in s["annotations"]]
        if len(ns) >= 2 and len(set(ns)) == 1 and s["text"].strip():
            out.append((s["text"].strip(), ns[0], s.get("start_index", 0)))
    return out


def all_names(u):
    return [a["name"] for s in u.get("segments", []) for a in s["annotations"]]


def names_for_text(u, text):
    return {a["name"] for s in u.get("segments", []) if s["text"].strip().lower() == text.lower()
            for a in s["annotations"]}


def spk(s):
    return "Customer" if s == "USER" else "Assistant"


def context(us, i):
    return "\n".join(f"{spk(u['speaker'])}: {u['text'].strip()}" for u in us[max(0, i - CONTEXT + 1):i + 1])


def good_span(t):
    return 1 <= len(t) <= 60 and re.search(r"[A-Za-z0-9]", t) and '"' not in t


def main():
    paths = T.fetch_prefix("TM-1-2019")
    for v in json.load(open(paths["TM-1-2019/ontology.json"])).values():
        ONTO[v["id"]] = set(v["required"]) | set(v["optional"])
    sd = json.load(open(paths["TM-1-2019/self-dialogs.json"]))
    wz = json.load(open(paths["TM-1-2019/woz-dialogs.json"]))
    train_ids = {l.strip().strip(",") for l in open(paths["TM-1-2019/train-dev-test/train.csv"]) if l.strip()}
    dialogs = [("self", d) for d in sd if d["conversation_id"] in train_ids] + [("woz", d) for d in wz]
    rng = random.Random(SEED)
    stats = collections.Counter()
    stats["dialogs"] = len(dialogs)

    status_c = {"yes": [], "no": []}
    role_pos = []
    for src, d in dialogs:
        us = d["utterances"]
        for i, u in enumerate(us):
            text = u["text"].strip()
            if not (2 <= len(text.split()) <= 90):
                continue
            ag = [(t, n, st) for t, n, st in agreed_spans(u) if good_span(t)]
            if u["speaker"] == "ASSISTANT":
                rej = [(t, n) for t, n, _ in ag if n.endswith(".reject") and slot_ok(n)]
                acc = [(t, n) for t, n, _ in ag if n.endswith(".accept") and slot_ok(n)]
                any_rej = any(n.endswith(".reject") for n in all_names(u))
                if rej and UNAVAIL.search(text):
                    t, n = max(rej, key=lambda x: len(x[0]))
                    mixed = bool(acc) and CONFIRM.search(text) is not None
                    status_c["no"].append((src, d, i, t, n, mixed))
                    if mixed:
                        ta, na = max(acc, key=lambda x: len(x[0]))
                        if ta.lower() not in {x[0].lower() for x in rej}:
                            status_c["yes"].append((src, d, i, ta, na, True))
                elif acc and not any_rej and CONFIRM.search(text) and "?" not in text:
                    t, n = max(acc, key=lambda x: len(x[0]))
                    status_c["yes"].append((src, d, i, t, n, False))
            else:
                cands = []
                for t, n, st in ag:
                    role = SUFFIX.sub("", n)
                    if role not in SIBLINGS:
                        continue
                    # every annotation on this text (any annotator) must carry the same role
                    roles = {SUFFIX.sub("", x) for x in names_for_text(u, t)}
                    if roles != {role}:
                        stats["role_disagree_drop"] += 1
                        continue
                    if text.lower().count(t.lower()) != 1:
                        continue
                    cands.append((t, role))
                if cands:
                    t, role = rng.choice(cands)
                    role_pos.append((src, d, i, t, role))

    # ---- status rows: one row per assistant turn, balanced ----
    rows, seen, used_turns = [], set(), set()

    def add(src, d, i, qid, question, gold, orig, edge):
        st = context(d["utterances"], i)
        n = C.norm(st)
        tk = (d["conversation_id"], i)
        if n in seen or tk in used_turns:
            return False
        seen.add(n)
        used_turns.add(tk)
        rows.append({
            "key": KEY, "rid": f"{d['conversation_id']}_u{i}_{qid}", "state": st, "instructions": question,
            "options": ["yes", "no"], "gold": gold, "soft": None,
            "meta": {"dataset": DATASET, "config": f"TM-1-2019 {src}-dialogs; task={qid}",
                     "revision": f"git:{T.COMMIT}; sha256 {src}-dialogs.json:"
                                 f"{T.SHA['TM-1-2019/' + ('self' if src == 'self' else 'woz') + '-dialogs.json'][:16]}",
                     "licence": T.licence("TM-1-2019"), "split": "train", "orig_label": orig,
                     "family": C.FAMILY, "edge": edge, "defs": qid}})
        return True

    for lab in ("yes", "no"):
        rng.shuffle(status_c[lab])
    n_st = {"yes": 0, "no": 0}
    target = min(len(status_c["yes"]), len(status_c["no"]), N_STATUS // 2)
    for lab in ("no", "yes"):
        for src, d, i, t, n, mixed in status_c[lab]:
            if n_st[lab] >= target:
                break
            vert = VERT[n.split(".")[0]]
            text = d["utterances"][i]["text"]
            edge = "exception" if mixed else ("negation" if lab == "no" and NEG.search(text) else
                                              "implicit" if lab == "no" else None)
            if add(src, d, i, "status", STATUS_Q.format(span=t, vert=vert), lab,
                   {"span": t, "annotation": n, "agreed_annotators": ">=2"}, edge):
                n_st[lab] += 1
    stats["status_cands_yes"], stats["status_cands_no"] = len(status_c["yes"]), len(status_c["no"])

    # ---- role rows: yes = asked role is the agreed role; no = a distinct sibling role ----
    pos = role_pos
    rng.shuffle(pos)
    by_role = collections.defaultdict(list)
    for c in pos:
        by_role[c[4]].append(c)
    # round-robin over roles so no role dominates; alternate yes/no within each role
    order, k = [], 0
    roles = sorted(by_role)
    while any(by_role.values()):
        r = roles[k % len(roles)]
        if by_role[r]:
            order.append(by_role[r].pop())
        k += 1
    n_role = {"yes": 0, "no": 0}
    flip = collections.Counter()
    for src, d, i, t, role in order:
        if n_role["yes"] + n_role["no"] >= N_ROLE:
            break
        lab = "yes" if flip[role] % 2 == 0 else "no"
        if n_role[lab] >= N_ROLE // 2:
            lab = "no" if lab == "yes" else "yes"
        asked = role if lab == "yes" else rng.choice(SIBLINGS[role])
        vert = VERT[role.split(".")[0]]
        edge = None
        if NEG.search(d["utterances"][i]["text"]):
            edge = "negation"
        elif re.search(r"\d", t):
            edge = "numeric"
        if add(src, d, i, "role", ROLE_Q.format(span=t, role=ROLE_TXT[asked], vert=vert), lab,
               {"span": t, "agreed_role": role, "asked_role": asked}, edge):
            n_role[lab] += 1
            flip[role] += 1

    rng.shuffle(rows)
    C.write_rows(rows, KEY)
    C.write_defs(STATUS_DEFS, KEY, "status")
    C.write_defs(ROLE_DEFS, KEY, "role")
    print(dict(stats))
    print("role candidates:", len(pos), dict(collections.Counter(c[4] for c in pos)))
    C.report(rows)


if __name__ == "__main__":
    main()
