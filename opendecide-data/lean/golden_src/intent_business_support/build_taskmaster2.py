"""Build golden rows for Taskmaster-2 (2020) search dialogs, all dialogs (no official split -> counts as train).

Source : GitHub google-research-datasets/Taskmaster @ d92cb6af, TM-2-2020/data/{flights,hotels,restaurant-search,
         movies}.json (+ ontology/). music, sports and food-ordering are not used (overlapping or fuzzy roles).
Licence: CC BY 4.0 (TM-2-2020/README.md, COPYRIGHT NOTICE).
Texts  : spoken two-person Wizard-of-Oz dialogs (crowd user, trained call-centre operator as assistant); user speech
         transcribed and then checked/corrected by human transcribers.
Labels : crowd span annotations of the search variables (one annotation layer in the release).
Task   : role - yes/no on a USER turn: is "<span>" a mention of <role>? yes = the annotated role; no = a clearly
         different sibling role of the same search (departure city vs destination, outbound vs return date, check-in vs
         check-out, guests vs rooms, cuisine vs meal, price vs rating, genre/person vs title, streaming service vs
         theater location). Pairs where annotators were inconsistent in a manual check (hotel stars vs guest rating,
         dish vs cuisine, artist/track/album) are not used. Spans must sit on word boundaries and occur once in the turn;
         the span text must carry exactly one role everywhere in the dialogue (both speakers); date roles need a
         cue (leave/return, check in/out, from/until) in the customer turn or the assistant turn before it; one row per
         user turn; duplicated dialog ids are used once.
Deterministic (seed 20261117).
"""
import collections
import json
import random
import re

import _ibs_common as C
import _taskmaster_files as T

KEY = "taskmaster2"
SEED = 20261117
DATASET = "google-research-datasets/Taskmaster (TM-2-2020)"
N_ROWS = 3600
CONTEXT = 3
FILES = ["flights", "hotels", "restaurant-search", "movies"]
DOMAIN_TXT = {"flights": "flight search", "hotels": "hotel search", "restaurant-search": "restaurant search",
              "movies": "movie search"}

ROLE_TXT = {
    "flight_search.origin": "departure city (where the trip starts)",
    "flight_search.destination1": "destination (where the customer wants to fly to)",
    "flight_search.date.depart_origin": "outbound departure date",
    "flight_search.date.return": "return date",
    "flight_search.seating_class": "cabin class (economy, premium, business or first)",
    "flight_search.stops": "number of stops or layovers",
    "hotel_search.check-in_date": "check-in date",
    "hotel_search.check-out_date": "check-out date",
    "hotel_search.num.guests": "number of guests",
    "hotel_search.num.rooms": "number of rooms",
    "hotel_search.price_range": "price limit or price range",
    "hotel_search.star_rating": "hotel star rating",
    "restaurant.type.food": "type of cuisine or food",
    "restaurant.type.meal": "meal or occasion (breakfast, lunch, dinner, brunch, dessert)",
    "restaurant.price_range": "price range",
    "restaurant.rating": "rating or review score",
    "movie_search.genre": "genre or kind of movie",
    "movie_search.name.movie": "title of a specific movie",
    "movie_search.real_person": "actor, director or other real person",
    "movie_search.streaming_service": "streaming service or rental platform",
    "movie_search.location.theater": "place to look for theaters (city, area or neighbourhood)",
}
SIBLINGS = {
    "flight_search.origin": ["flight_search.destination1"],
    "flight_search.destination1": ["flight_search.origin"],
    "flight_search.date.depart_origin": ["flight_search.date.return"],
    "flight_search.date.return": ["flight_search.date.depart_origin"],
    "flight_search.seating_class": ["flight_search.stops"],
    "flight_search.stops": ["flight_search.seating_class"],
    "hotel_search.check-in_date": ["hotel_search.check-out_date"],
    "hotel_search.check-out_date": ["hotel_search.check-in_date"],
    "hotel_search.num.guests": ["hotel_search.num.rooms"],
    "hotel_search.num.rooms": ["hotel_search.num.guests"],
    "hotel_search.price_range": ["hotel_search.star_rating"],
    "hotel_search.star_rating": ["hotel_search.price_range"],
    "restaurant.type.food": ["restaurant.type.meal"],
    "restaurant.type.meal": ["restaurant.type.food"],
    "restaurant.price_range": ["restaurant.rating"],
    "restaurant.rating": ["restaurant.price_range"],
    "movie_search.genre": ["movie_search.name.movie"],
    "movie_search.real_person": ["movie_search.name.movie"],
    "movie_search.name.movie": ["movie_search.genre", "movie_search.real_person"],
    "movie_search.streaming_service": ["movie_search.location.theater"],
    "movie_search.location.theater": ["movie_search.streaming_service"],
}
ROLE_Q = 'In the customer\'s last message, is "{span}" a mention of the {role} for this {dom}?'
ROLE_DEFS = {
    "yes": ("The quoted phrase in the customer's last message refers to exactly the detail named in the question, "
            "even if the customer mentions it to rule it out (e.g. 'not horror' still mentions a genre)."),
    "no": ("The quoted phrase refers to a different detail of the search (e.g. the destination rather than the "
           "departure city, the return rather than the outbound date, or the meal rather than the cuisine)."),
}
DATEY = {"flight_search.date.depart_origin", "flight_search.date.return", "hotel_search.check-in_date",
         "hotel_search.check-out_date"}
# a date role is only used when the customer turn or the assistant turn just before it says which date it is
DATE_CUE = {
    "flight_search.date.depart_origin": re.compile(r"leav|depart|fly(ing)? out|outbound|head(ing)? out|take off|"
                                                   r"going (out|there)|travel(l)?ing (on|out)", re.I),
    "flight_search.date.return": re.compile(r"return|\bback\b|come home|coming home|fly(ing)? home|inbound", re.I),
    "hotel_search.check-in_date": re.compile(r"check(ing)?[ -]?in|arriv|starting|\bfrom\b|get there", re.I),
    "hotel_search.check-out_date": re.compile(r"check(ing)?[ -]?out|until|\btill\b|through|leav|depart", re.I),
}
NEG = re.compile(r"\b(not|no|never|none|nothing|neither|nor|without|except)\b|n't", re.I)
# review fix: spans cut mid-phrase ('tomorrow and I want to', 'a kid so I', 'from me', 'I want a single to four')
BAD_SPAN = re.compile(r"\b(to|and|so|or|but|want|the|a|an|of)$|\bso i$|^(from|i want|i'd like|i would like)\b", re.I)


def spk(s):
    return "Customer" if s == "USER" else "Assistant"


def main():
    paths = {f: T.fetch(f"TM-2-2020/data/{f}.json") for f in FILES}
    T.fetch("TM-2-2020/README.md")
    rng = random.Random(SEED)
    stats = collections.Counter()
    cands, seen_ids = [], set()
    for f in FILES:
        for d in json.load(open(paths[f])):
            if d["conversation_id"] in seen_ids:
                stats["dup_dialog_drop"] += 1
                continue
            seen_ids.add(d["conversation_id"])
            us = d["utterances"]
            # dialogue-level consistency: the same text must never carry another role anywhere in the dialogue
            dlg_roles = collections.defaultdict(set)
            for u in us:
                for s in u.get("segments", []):
                    for a in s["annotations"]:
                        dlg_roles[s["text"].strip().lower()].add(a["name"].strip())
            for i, u in enumerate(us):
                if u["speaker"] != "USER":
                    continue
                text = u["text"]
                if not (2 <= len(text.split()) <= 70):
                    continue
                by_text = collections.defaultdict(set)
                for s in u.get("segments", []):
                    for a in s["annotations"]:
                        by_text[s["text"].strip().lower()].add(a["name"].strip())
                opts = []
                for s in u.get("segments", []):
                    names = [a["name"].strip() for a in s["annotations"]]
                    t = s["text"].strip()
                    if len(names) != 1 or names[0] not in SIBLINGS or len(by_text[t.lower()]) != 1:
                        continue
                    if dlg_roles[t.lower()] != {names[0]}:
                        stats["dialogue_role_conflict_drop"] += 1
                        continue
                    if names[0] in DATE_CUE:
                        prev = us[i - 1]["text"] if i > 0 and us[i - 1]["speaker"] != "USER" else ""
                        if not DATE_CUE[names[0]].search(prev + " " + text):
                            stats["date_no_cue_drop"] += 1
                            continue
                    st, en = s["start_index"], s["end_index"]
                    # span on word boundaries (drops truncated spans such as 'depart today on the 2')
                    if text[st:en].strip() != t or (st > 0 and text[st - 1].isalnum()) or \
                            (en < len(text) and text[en].isalnum()):
                        stats["span_boundary_drop"] += 1
                        continue
                    if not (2 <= len(t) <= 50) or text.lower().count(t.lower()) != 1 or '"' in t or BAD_SPAN.search(t):
                        continue
                    opts.append((t, names[0]))
                if opts:
                    t, role = rng.choice(opts)
                    cands.append((f, d, i, t, role))
    stats["cands"] = len(cands)

    rng.shuffle(cands)
    by_role = collections.defaultdict(list)
    for c in cands:
        by_role[c[4]].append(c)
    order, k, roles = [], 0, sorted(by_role)
    while any(by_role.values()):
        r = roles[k % len(roles)]
        if by_role[r]:
            order.append(by_role[r].pop())
        k += 1

    rows, seen = [], set()
    n_lab, flip = {"yes": 0, "no": 0}, collections.Counter()
    for f, d, i, t, role in order:
        if len(rows) >= N_ROWS:
            break
        lab = "yes" if flip[role] % 2 == 0 else "no"
        if n_lab[lab] >= N_ROWS // 2:
            lab = "no" if lab == "yes" else "yes"
        asked = role if lab == "yes" else rng.choice(SIBLINGS[role])
        us = d["utterances"]
        st = "\n".join(f"{spk(u['speaker'])}: {u['text'].strip()}" for u in us[max(0, i - CONTEXT + 1):i + 1])
        n = C.norm(st)
        if n in seen:
            continue
        seen.add(n)
        text = us[i]["text"]
        if NEG.search(text):
            edge = "negation"
        elif role in DATEY or asked in DATEY:
            edge = "temporal"
        elif re.search(r"\d", t) or role.endswith(("num.guests", "num.rooms")):
            edge = "numeric"
        else:
            edge = None
        rows.append({
            "key": KEY, "rid": f"{d['conversation_id']}_u{i}_role", "state": st,
            "instructions": ROLE_Q.format(span=t, role=ROLE_TXT[asked], dom=DOMAIN_TXT[f]),
            "options": ["yes", "no"], "gold": lab, "soft": None,
            "meta": {"dataset": DATASET, "config": f"TM-2-2020/data/{f}.json; task=role",
                     "revision": f"git:{T.COMMIT}; sha256 {f}.json:{T.SHA['TM-2-2020/data/' + f + '.json'][:16]}",
                     "licence": T.licence("TM-2-2020"), "split": "train",
                     "orig_label": {"span": t, "annotated_role": role, "asked_role": asked,
                                    "instruction_id": d.get("instruction_id")},
                     "family": C.FAMILY, "edge": edge, "defs": "role"}})
        n_lab[lab] += 1
        flip[role] += 1

    rng.shuffle(rows)
    C.write_rows(rows, KEY)
    C.write_defs(ROLE_DEFS, KEY, "role")
    print(dict(stats))
    print("roles used:", dict(collections.Counter(r["meta"]["orig_label"]["annotated_role"] for r in rows)))
    C.report(rows)


if __name__ == "__main__":
    main()
