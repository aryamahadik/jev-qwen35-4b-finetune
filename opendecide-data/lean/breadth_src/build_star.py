"""Build raw rows for star (STAR: A Schema-Guided Dialog Dataset for Transfer Learning, Rasa; Mosig et al. 2020).

Source : GitHub RasaHQ/STAR, git clone pinned at commit REV (cache/star/repo). One JSON file per dialogue in dialogues/.
Licence: MIT (repo LICENSE.txt, "Copyright (c) 2020 Rasa Technologies GmbH").
Provenance: Wizard-of-Oz dialogues typed by MTurk workers (human text). The label is the dialogue's scenario task
         (Scenario.WizardCapabilities[0].Task), assigned by the dataset designers when the human user was given that
         task; no model wrote texts or labels. Not derived from SGD (DSTC8) - independent collection with its own schemas.
Text   : USER text only - the first of the user's first two "utter" events that is not a bare greeting, generic
         help plea or self-introduction. Dialogues whose turn is only a generic request shared by several tasks
         ("I'd like to make a reservation") are dropped, as are 37 off-script dialogues listed in DROP_RIDS
         (found by reading every selected row in verification). Pools are ordered by a seeded hash of the id.
         MultiTask dialogues are skipped (single task only); only CompletionLevel == "Complete" dialogues are used.
Labels : 24 single tasks; the full task set is always offered, so close tasks (ride_book/ride_change/ride_status,
         hotel_book/hotel_search/hotel_service_request, plane_*, restaurant_*, apartment_*, doctor_*, bank_*,
         party_*, spaceship_*) act as hard negatives.
Split  : STAR ships no official train/dev/test split (the paper uses its own cross-validation / zero-shot task
         splits); the whole release is treated as train.
Soft   : null (one designed label per dialogue, no annotator counts).
Deterministic (seed 20261101).
"""
import collections
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

SEED = 20261101
MAX_ROWS = 550
KEY = "star"
HERE = Path(__file__).resolve().parent
LEAN = HERE.parent
CACHE = HERE / "cache" / KEY
REPO = CACHE / "repo"
OUT = LEAN / "data" / "v13_parts" / "raw" / f"{KEY}.jsonl"
DEFS_OUT = LEAN / "data" / "v13_parts" / "defs" / f"{KEY}.json"

GIT_URL = "https://github.com/RasaHQ/STAR.git"
REV = "3058975092cdd09798e4a3a9e4ae135755824545"
LICENCE = "MIT (LICENSE.txt in github.com/RasaHQ/STAR, 'Copyright (c) 2020 Rasa Technologies GmbH')"
INSTRUCTIONS = "What task does the user want the assistant's help with?"

NAMES = {
    "apartment_schedule": "schedule apartment viewing",
    "apartment_search": "search for apartment",
    "bank_balance": "check bank balance",
    "bank_fraud_report": "report bank fraud",
    "doctor_followup": "doctor follow-up instructions",
    "doctor_schedule": "schedule doctor appointment",
    "hotel_book": "book hotel room",
    "hotel_search": "search for hotel",
    "hotel_service_request": "hotel room service request",
    "meeting_schedule": "schedule meeting",
    "party_plan": "plan a party",
    "party_rsvp": "RSVP to a party",
    "plane_book": "book flight",
    "plane_search": "search for flight",
    "restaurant_book": "book restaurant table",
    "restaurant_search": "search for restaurant",
    "ride_book": "book a ride",
    "ride_change": "change or cancel ride",
    "ride_status": "check ride status",
    "spaceship_access_codes": "spaceship access codes",
    "spaceship_life_support": "spaceship life support repair",
    "trip_directions": "trip directions",
    "trivia": "play trivia",
    "weather": "weather forecast",
}
OPTIONS = [NAMES[k] for k in sorted(NAMES)]

DEFS = {
    "schedule apartment viewing": "The user wants to book a time to view a specific apartment or building, giving the apartment name, day and time for the viewing.",
    "search for apartment": "The user wants to find an apartment matching criteria such as number of bedrooms, floor, price budget, elevator or other amenities.",
    "check bank balance": "The user wants to learn the current balance of their bank account, usually after identifying themselves with account number, PIN or security questions.",
    "report bank fraud": "The user wants to report suspicious or unauthorised activity on their bank account, such as unknown transfers, withdrawals or a lost card being used.",
    "doctor follow-up instructions": "The user had a recent appointment and wants to find out or confirm the doctor's orders, such as how often to take their medicine.",
    "schedule doctor appointment": "The user wants to book a new appointment with a doctor, often mentioning symptoms and the doctor and day they prefer.",
    "book hotel room": "The user wants to reserve a room at a named hotel for specific dates, possibly with a custom request such as a balcony.",
    "search for hotel": "The user wants to find a hotel or learn about one, such as its rating, location in town or price, without making a reservation.",
    "hotel room service request": "The user is already staying at a hotel and wants a service delivered to their room at a given time, such as food or a repair.",
    "schedule meeting": "The user wants to set up a meeting with a named person at a specific day and time, often stating its duration and reason.",
    "plan a party": "The user wants to organise and host a party, such as reserving a venue for a day and time, arranging food, drinks or guests.",
    "RSVP to a party": "The user has been invited to someone else's party and wants to confirm attendance, arrival time, number of guests, parking or dietary needs.",
    "book flight": "The user wants to reserve or book a flight they have already picked, usually giving its flight id, rather than searching routes and dates.",
    "search for flight": "The user wants to find flights matching a route, date, airline, seat class or price limit, rather than reserving a flight id they already have.",
    "book restaurant table": "The user wants to reserve a table at a named restaurant for a number of people at a given time.",
    "search for restaurant": "The user wants to find or learn about a restaurant by price range, cuisine, rating, location or delivery, without reserving a table.",
    "book a ride": "The user wants a new taxi, Lyft, Uber or other car to pick them up and take them somewhere, possibly naming a vehicle or driver preference.",
    "change or cancel ride": "The user already booked a ride and wants to modify it, such as changing departure or arrival location or time, or cancel it.",
    "check ride status": "The user already booked a ride and wants to know where it is or why it has not arrived yet.",
    "spaceship access codes": "The user is locked out of a spaceship deck during an attack and needs the onboard computer's help with access or clearance codes to unlock the door.",
    "spaceship life support repair": "The spaceship's life support is failing and the user directs the repair robot to open the sealed engineering deck by tampering with a lock and swapping cables.",
    "trip directions": "The user is lost or wants step-by-step directions to a destination by car, on foot or by public transit, rather than a booked ride.",
    "play trivia": "The user wants to play a trivia game, asking for questions (often starting from a given question number) and giving answers.",
    "weather forecast": "The user wants to know the current or upcoming weather, such as temperature or rain, for their city or another place and day.",
}

USER_WINDOW = 2
# Dialogues where the crowd worker went off-script, so the user text contradicts or ignores the assigned task
# (found by reading every selected row during verification). Dropped by id; the reason is kept per id.
DROP_RIDS = {
    "2642": "spaceship_access_codes dialogue, but the user typed the life-support scenario",
    "4167": "hotel_book dialogue, but the user asks for more towels (a room service request)",
    "216": "hotel_service_request dialogue, but the user asks to book a room",
    "2717": "ride_status dialogue, but the user says 'i want a ride with ID 213' (reads as booking)",
    "1396": "doctor_followup dialogue, but the user orders tacos",
    "4067": "doctor_followup dialogue, off-script joke ('You don't recognize your own mother?')",
    "3985": "apartment_search dialogue, 'Hi, i need a room' reads as a hotel request",
    "2438": "plane_book dialogue, role-play greeting with no task ('I require aid')",
    "585": "plane_book dialogue, text is only 'ARE you THERE!! HELLOOOO!!!'",
    "552": "party_rsvp dialogue, text is only 'Hi, I could use your help please :)'",
    "657": "doctor_schedule dialogue, but the user asks for directions",
    "246": "hotel_service_request dialogue, 'can you help me at the Hyatt Hotel?' fits any hotel task",
    "3106": "ride_change dialogue, but the user asks to get a ride (reads as booking)",
    "789": "ride_book dialogue, 'Get me to my friend's wedding' is the trip_directions scenario wording",
    "4041": "ride_book dialogue, 'I need to get to 5th and Main' fits trip directions equally",
    "1540": "ride_book dialogue, 'i wanna get to Broadway and Main' fits trip directions equally",
    "3435": "ride_book dialogue, 'I want to go to Hospital.' fits trip directions equally",
    "3619": "ride_book dialogue, 'travel to Forbes and Murray from the Hospital' fits trip directions equally",
    "637": "ride_book dialogue, 'travel from Main and Airport to 5th' fits trip directions equally",
    "3639": "trip_directions dialogue, 'help getting from 5th and Main to Forbes and Murray' fits book a ride equally",
    "3841": "plane_book dialogue, text is a bare flight id answer ('710. And you better not screw it up...')",
    "997": "doctor_followup dialogue, but the user asks to book an appointment (schedule task)",
    "1466": "doctor_followup dialogue, but the user asks to make an appointment (schedule task)",
    "1364": "doctor_followup dialogue, but the user asks to book an appointment (schedule task)",
    "1282": "ride_book dialogue, but the user asks for directions",
    "3654": "ride_book dialogue, 'I need to get to Broadway and Main' fits trip directions equally",
    "1367": "ride_book dialogue, 'I would like to travel to Craig and center' fits trip directions equally",
    "2847": "plane_book dialogue, text contains a racial slur",
    "629": "plane_book dialogue, text has no task ('I could use help in having a better day!')",
    "1255": "plane_book dialogue, off-script text with no task",
    "2439": "bank_fraud_report dialogue, 'urgent help with my account' fits balance check equally",
    "3950": "bank_fraud_report dialogue, 'help with my debit card' fits balance check equally",
    "3489": "bank_fraud_report dialogue, 'help with my bank transactions' fits balance check equally",
    "1298": "bank_fraud_report dialogue, 'I need help with my account.' fits balance check equally",
    "314": "restaurant_search dialogue, 'I need a reservation for burger restaurant' reads as booking",
    "1278": "trivia dialogue, text has no task ('Hi i need some fun')",
    "1183": "plane_book dialogue, text is only a greeting ('Helllo!!!!!!!!!! ARe you there???')",
}

GREET_TOK = {"hello", "hallo", "helo", "hellow", "hi", "hii", "hey", "heya", "hiya", "howdy", "yo", "greetings",
             "good", "morning", "afternoon", "evening", "day", "there", "sir", "madam", "assistant", "computer",
             "robot", "bot", "ok", "okay", "um", "uh", "so", "yes", "and"}
GENERIC = {"", "how are you", "how are you doing", "how are you today", "can you help me", "could you help me",
           "can you help", "can you please help me", "could you please help me", "i need help", "i need some help",
           "help", "help me", "please help", "please help me", "i need your help", "are you there", "anyone there",
           "is anyone there", "how is it going", "whats up", "what s up", "i need assistance",
           "i need some assistance", "can i get some help", "i have a question", "i need help please"}


def ensure_repo():
    if not REPO.exists():
        CACHE.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "-q", GIT_URL, str(REPO)], check=True)
    head = subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True, text=True,
                          check=True).stdout.strip()
    if head != REV:
        subprocess.run(["git", "-C", str(REPO), "checkout", "-q", REV], check=True)


# Words that carry no task content (help pleas, fillers, self-introductions). A turn made only of these,
# greetings and a self-introduction ("I'm Alexis", "My name is Jane Doe") cannot identify the task, so the
# builder moves on to the user's next turn. The lists are label-agnostic (applied to every dialogue).
FILLER = {"i", "im", "id", "ill", "need", "needs", "some", "help", "helps", "please", "pls", "can", "could", "would",
          "you", "me", "my", "anyone", "anybody", "someone", "going", "to", "or", "what", "whats", "out", "already",
          "like", "assistance", "assist", "question", "a", "an", "have", "the", "with", "something", "am", "is",
          "are", "there", "get", "go", "in", "on", "here", "very", "serious", "desperate", "situation", "trouble",
          "urgent", "urgently", "emergency", "now", "quickly", "asap", "right", "fellow", "traveler", "traveller",
          "it", "its", "this", "that", "do", "for", "hurry", "up", "want", "please", "thank", "thanks", "if",
          "much", "really", "just", "kid", "buddy", "friend", "sir", "maam", "well", "oh", "hmm", "yeah", "ya",
          "how", "doing", "today", "your", "be", "of", "will", "able", "hope", "wondering", "was"}
NAME_INTRO = re.compile(r"\b(?:[Mm]y\s+name(?:\s+is|'s)?|[Nn]ame'?s|[Nn]ame\s+is|I\s+am|I'm|Im|[Tt]his\s+is|[Ii]t'?s)\s+"
                        r"[A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)?|\b[A-Z][a-z]+\s+here\b")


def is_greeting(text):
    t = NAME_INTRO.sub(" ", text)
    t = re.sub(r"[^a-z ]+", " ", t.lower().replace("'", ""))
    words = t.split()
    while words and words[0] in GREET_TOK:
        words.pop(0)
    rest = " ".join(words)
    return rest in GENERIC or all(w in GREET_TOK or w in FILLER for w in words)


# Generic request words shared by several tasks ("I'd like to make a reservation", "I need an appointment",
# "I need to make a request"): with nothing else, the turn fits hotel, restaurant, flight, doctor, apartment or
# meeting equally, so the gold is not recoverable from the text and the dialogue is dropped (label-agnostic rule).
AMBIG = {"make", "reservation", "reservations", "reserve", "book", "booking", "appointment", "appt", "schedule",
         "request", "information", "info", "find", "search", "searching", "looking", "look", "set", "something",
         "and", "some", "an", "one"}


def is_ambiguous_generic(text):
    t = NAME_INTRO.sub(" ", text)
    words = re.sub(r"[^a-z ]+", " ", t.lower().replace("'", "")).split()
    return all(w in GREET_TOK or w in FILLER or w in AMBIG for w in words)


def norm(t):
    return re.sub(r"\s+", " ", t).strip().lower()


def main():
    ensure_repo()
    by_label = collections.defaultdict(list)
    skipped = collections.Counter()
    for f in sorted((REPO / "dialogues").glob("*.json"), key=lambda p: int(p.stem)):
        d = json.loads(f.read_text())
        sc = d["Scenario"]
        if sc.get("MultiTask"):
            skipped["multitask"] += 1
            continue
        if d.get("CompletionLevel") != "Complete":
            skipped["incomplete"] += 1
            continue
        caps = sc.get("WizardCapabilities") or []
        if len(caps) != 1 or caps[0]["Task"] not in NAMES:
            skipped["bad_caps"] += 1
            continue
        task = caps[0]["Task"]
        if str(d["DialogueID"]) in DROP_RIDS:
            skipped["drop_list"] += 1
            continue
        # Only the user's first USER_WINDOW utterances are considered: later turns are answers to the wizard's
        # questions ("May 2", "710") that no longer state the task.
        utts = [e["Text"] for e in d["Events"] if e.get("Agent") == "User" and e.get("Action") == "utter"
                and (e.get("Text") or "").strip()][:USER_WINDOW]
        turn = next((u.strip() for u in utts if not is_greeting(u)), None)
        if turn is None:
            skipped["no_user_turn"] += 1
            continue
        if is_ambiguous_generic(turn):
            skipped["ambiguous_generic"] += 1
            continue
        if not (15 <= len(turn) <= 4000):
            skipped["length"] += 1
            continue
        by_label[task].append({"rid": str(d["DialogueID"]), "text": turn, "happy": sc.get("Happy")})

    # Order each label's pool by a seeded hash of the dialogue id (not rng.shuffle of the pool), so dropping one
    # dialogue only brings in the next candidate and does not reshuffle every other pick.
    for lab in sorted(by_label):
        by_label[lab].sort(key=lambda c: hashlib.md5(f"{SEED}:{c['rid']}".encode()).hexdigest())
    labels = sorted(by_label)
    seen, rows, idx = set(), [], {l: 0 for l in labels}
    while len(rows) < MAX_ROWS:
        progressed = False
        for lab in labels:
            if len(rows) >= MAX_ROWS:
                break
            pool = by_label[lab]
            while idx[lab] < len(pool):
                c = pool[idx[lab]]
                idx[lab] += 1
                k = norm(c["text"])
                if k in seen:
                    skipped["dup"] += 1
                    continue
                seen.add(k)
                rows.append({
                    "key": KEY, "rid": c["rid"], "state": c["text"], "instructions": INSTRUCTIONS,
                    "options": OPTIONS, "gold": NAMES[lab], "soft": None,
                    "meta": {"dataset": "RasaHQ/STAR", "config": "dialogues (single-task, Complete, first user turn)",
                             "revision": REV, "licence": LICENCE, "split": "train", "orig_label": lab},
                })
                progressed = True
                break
        if not progressed:
            break

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w") as fo:
        for r in rows:
            fo.write(json.dumps(r, ensure_ascii=False) + "\n")
    DEFS_OUT.parent.mkdir(parents=True, exist_ok=True)
    assert set(DEFS) == set(OPTIONS)
    DEFS_OUT.write_text(json.dumps(DEFS, indent=1, ensure_ascii=False) + "\n")

    cnt = collections.Counter(r["gold"] for r in rows)
    lens = sorted(len(r["state"]) for r in rows)
    print(f"rows={len(rows)} labels={len(cnt)} pool={ {l: len(v) for l, v in by_label.items()} }")
    print("skipped:", dict(skipped))
    for k, v in sorted(cnt.items(), key=lambda x: -x[1]):
        print(f"  {k:32s} {v:4d} ({100 * v / len(rows):.1f}%)")
    print("soft coverage: 0.0 (no annotator counts)")
    print(f"len chars min={lens[0]} median={lens[len(lens) // 2]} mean={sum(lens) / len(lens):.0f} max={lens[-1]}")
    dw = [len(v.split()) for v in DEFS.values()]
    print(f"def words min={min(dw)} max={max(dw)}")


if __name__ == "__main__":
    sys.exit(main())
