"""Build golden rows from MultiWOZ 2.1 system dialogue acts, TRAIN split only.

Source : GitHub budzianowski/multiwoz @ fe0c8e65cfcd8462bd33c86e35f21addc84ca82b, data/MultiWOZ_2.1.zip
         (data.json + system_acts.json). Train = dialogues not in valListFile.txt / testListFile.txt (those lists are
         read only to exclude). MultiWOZ 2.2's T5-assisted act fixes are NOT used.
Licence: MIT (repo LICENSE, "Copyright (c) 2019 Paweł Budzianowski").
Texts  : human-human Wizard-of-Oz chats written by crowd workers (tourist <-> clerk, Cambridge UK).
Labels : system dialogue acts annotated by crowd workers (MultiWOZ FAQ: "Only system utterances are manually annotated
         with dialogue acts"; user acts are heuristic and are never used here).
Tasks  : booking   - yes/no: does the assistant's reply confirm that the requested booking was made?
                     yes = Booking-Book or Train-OfferBooked without Booking-NoBook; no = Booking-NoBook without either.
         match     - yes/no: did the assistant find at least one option meeting everything the customer asked for?
                     no = any <Domain>-NoOffer act (alternatives offered in the same turn -> edge 'exception');
                     yes = Inform with a positive Choice count or Recommend naming an option, no NoOffer/Booking
                     acts, answering a customer turn that asks for or constrains a search.
         Text sanity guards drop turns whose wording contradicts the act (likely missing annotation).
         Each system turn is used by at most one task; near-exact duplicate states (codes/numbers masked)
         are dropped; dialogues whose turns appear in dstc9_track1 kst states are skipped
         (list written by build_dstc9_track1.py, which must run first); non-generic turns that also appear in a
         dstc9_track1 kst state (MultiWOZ near-duplicate dialogues) are not reused.
State  : the customer's turn and the assistant's reply to it.
Deterministic (seed 20261115).
"""
import collections
import json
import random
import re
import zipfile

import _ibs_common as C

KEY = "multiwoz21_sysacts"
SEED = 20261115
COMMIT = "fe0c8e65cfcd8462bd33c86e35f21addc84ca82b"
ZIP_SHA = "8db3f6afe591383b8523b271f07727693e73012ecce47f3ac7987191e09b7523"
LICENSE_SHA = "d84d5c0261e1cfc4b4f10f16497feb217800ae6bf89240ee5622a75f659f5124"
LICENCE = f"MIT (https://github.com/budzianowski/multiwoz/blob/{COMMIT}/LICENSE, 'Copyright (c) 2019 Paweł Budzianowski')"
DATASET = "budzianowski/multiwoz (MultiWOZ 2.1, data.json + system_acts.json)"
CACHE = C.CACHE / "multiwoz"
KST_IDS = C.CACHE / "dstc9" / "kst_mwz_ids.json"
N_PER_TASK = 3000

BOOK_Q = "Does the assistant's reply confirm that the booking the customer asked for was actually made?"
MATCH_Q = "In its reply, did the assistant find at least one option that meets everything the customer asked for?"
BOOK_DEFS = {
    "yes": ("The assistant states that the requested reservation, room, table or train ticket was booked successfully, "
            "usually giving a reference number."),
    "no": ("The assistant says the booking could not be made (unavailable, fully booked, unsuccessful), even if it "
           "offers to try another day, time, length of stay or place."),
}
MATCH_DEFS = {
    "yes": ("The assistant reports, lists or recommends at least one place or train that fits all of the customer's "
            "stated requirements, even if it then asks a follow-up question to narrow the choice."),
    "no": ("The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives "
           "that relax one of them (another area, price range, type, day or time)."),
}

FAIL_TXT = re.compile(r"unsuccessful|unable|fully booked|booked up|not available|unavailable|no availability|"
                      r"couldn't|could not|can't|cannot|can not|sorry|unfortunately|no (rooms|tables|seats)|"
                      r"is full|are full|didn't go through|did not go through|failed", re.I)
NONE_TXT = re.compile(r"there (are|is|were|was) no\b|no (matching|results|such|places|restaurants|hotels|trains|"
                      r"attractions|guesthouses)|nothing (matches|that|available)|(couldn't|could not|can't|cannot|"
                      r"unable to) (find|locate)|don't have any|do not have any|doesn't have any|does not have any|"
                      r"unfortunately|i'm sorry|i am sorry|there aren't|there isn't|none (of|that)", re.I)
NEG = re.compile(r"\b(not|no|never|none|nothing|neither|nor)\b|n't|\bcannot\b|unavailable|unsuccessful", re.I)
COUNT = re.compile(r"\b([1-9]\d*|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|"
                   r"fifteen|twenty|thirty|several|many|multiple|numerous|a few|a lot|lots|plenty|various|some)\b", re.I)
# review fix: a 'yes' match reply must not carry contrast/negation wording ('I have three hotels, however, they are
# not 4 star', 'we only have one ... but it is in the east'), which signals a missing NoOffer annotation
CONTRAST_TXT = re.compile(r"\bhowever\b|\bnot\b|n't\b|\bunfortunately\b|\bsorry\b|\binstead\b|\bcannot\b|"
                          r"\bno (other|more|such)\b|\bnone\b|\bneither\b|\bonly\b.{0,40}\bbut\b", re.I)
SEARCH_REQ = re.compile(r"looking for|look for|find|search|need|want|would like|recommend|suggest|\bany\b|is there|"
                        r"are there|do you have|what (kind|type|restaurants|hotels|trains|attractions|places)|"
                        r"which|options|somewhere|some place|a place|prefer|\bin the\b|should (be|have)", re.I)


def near_norm(t):
    """Near-exact duplicate key: reference codes, numbers and times collapse to '#'."""
    t = re.sub(r"\b\w*\d\w*\b", "#", t.lower())
    return re.sub(r"[^a-z#]+", " ", t).strip()


def main():
    C.fetch(f"https://github.com/budzianowski/multiwoz/raw/{COMMIT}/data/MultiWOZ_2.1.zip",
            CACHE / "MultiWOZ_2.1.zip", ZIP_SHA)
    C.fetch(f"https://raw.githubusercontent.com/budzianowski/multiwoz/{COMMIT}/LICENSE", CACHE / "LICENSE", LICENSE_SHA)
    with zipfile.ZipFile(CACHE / "MultiWOZ_2.1.zip") as z:
        data = json.loads(z.read("MultiWOZ_2.1/data.json"))
        acts = json.loads(z.read("MultiWOZ_2.1/system_acts.json"))
        val = set(z.read("MultiWOZ_2.1/valListFile.txt").decode().split())
        test = set(z.read("MultiWOZ_2.1/testListFile.txt").decode().split())
    assert KST_IDS.exists(), "run build_dstc9_track1.py first"
    kst_ids = set(json.load(open(KST_IDS)))
    rng = random.Random(SEED)
    stats = collections.Counter()
    # MultiWOZ has near-duplicate dialogues: a turn that also sits in a dstc9_track1 kst window is not reused unless
    # it is generic (the same text occurs in 3+ MultiWOZ dialogues, e.g. 'Booking was successful. ...')
    turn_dlgs = collections.defaultdict(set)
    for did, d in data.items():
        for t in d["log"]:
            turn_dlgs[" ".join(t["text"].lower().split())].add(did)
    kst_turns = set()
    for line in open(C.RAW / "dstc9_track1.jsonl"):
        r = json.loads(line)
        if r["meta"]["defs"] == "kst":
            for ln in r["state"].split("\n"):
                if ": " in ln:
                    kst_turns.add(" ".join(ln.split(": ", 1)[1].lower().split()))

    cands = {("booking", "yes"): [], ("booking", "no"): [], ("match", "yes"): [], ("match", "no"): []}
    for did in sorted(data):
        if did in val or did in test:
            continue  # TRAIN ONLY
        stats["train_dialogues"] += 1
        if did in kst_ids:
            stats["skip_used_in_dstc9"] += 1
            continue
        log = data[did]["log"]
        dacts = acts.get(did.replace(".json", ""), {})
        per = collections.defaultdict(list)
        for t, a in dacts.items():
            if not isinstance(a, dict):
                continue
            ti = int(t) * 2 - 1
            if ti >= len(log):
                stats["act_index_out_of_range"] += 1
                continue
            text, prev = log[ti]["text"].strip(), log[ti - 1]["text"].strip()
            names = set(a)
            # alignment sanity: a booking reference in the acts must appear in the text
            refs = [v for n, sv in a.items() for s, v in sv if s == "Ref" and v not in ("none", "?")]
            if refs and not any(r.strip().lower() in text.lower() for r in refs):
                stats["ref_not_in_text_drop"] += 1
                continue
            if not (3 <= len(text.split()) <= 80 and 2 <= len(prev.split()) <= 80):
                continue
            book = "Booking-Book" in names or "Train-OfferBooked" in names
            nobook = "Booking-NoBook" in names
            if book and not nobook and not FAIL_TXT.search(text):
                per[("booking", "yes")].append((ti, names))
            elif nobook and not book and FAIL_TXT.search(text):
                per[("booking", "no")].append((ti, names))
            nooffer = [n for n in names if n.endswith("-NoOffer")]
            alt = [n for n in names if n.split("-")[0] not in ("general", "Booking")
                   and n.split("-")[1] in ("Inform", "Recommend", "Select", "OfferBook")]
            has_booking = any(n.startswith("Booking-") for n in names) or "Train-OfferBooked" in names
            if nooffer and not has_booking:
                per[("match", "no")].append((ti, names))
            elif not nooffer and not has_booking:
                good = False
                for n, sv in a.items():
                    dom, act = n.split("-")
                    if dom in ("general", "Booking"):
                        continue
                    # a concrete recommended option, or a positive count of matching options
                    if act == "Recommend" and any(s in ("Name", "Id") for s, v in sv):
                        good = True
                    if act == "Inform" and any(s == "Choice" and COUNT.search(v) for s, v in sv):
                        good = True
                if good and not NONE_TXT.search(text) and not CONTRAST_TXT.search(text) and SEARCH_REQ.search(prev):
                    per[("match", "yes")].append((ti, names))
        used_ti = set()
        for task in ("booking", "match"):
            # every system turn is its own source record; a turn is used by at most one task, and 2-turn windows of
            # different system turns never overlap (the turn before a system turn is a customer turn)
            for lab in ("no", "yes"):
                for ti, names in per[(task, lab)]:
                    if ti in used_ti:
                        continue
                    used_ti.add(ti)
                    cands[(task, lab)].append((did, ti, names))

    # near-exact dedupe of candidate states (per corpus), then balance yes/no per task
    seen = set()
    for key_ in sorted(cands):
        rng.shuffle(cands[key_])
        kept = []
        for did, ti, names in cands[key_]:
            log = data[did]["log"]
            state = f"Customer: {log[ti - 1]['text'].strip()}\nAssistant: {log[ti]['text'].strip()}"
            shared = [" ".join(log[j]["text"].lower().split()) for j in (ti - 1, ti)]
            if any(t in kst_turns and len(turn_dlgs[t]) < 3 for t in shared):
                stats["shared_with_dstc9_drop"] += 1
                continue
            nn = near_norm(state)
            if nn in seen:
                stats["dup_state_drop"] += 1
                continue
            seen.add(nn)
            kept.append((did, ti, names, state))
        cands[key_] = kept
    out = []
    for task in ("booking", "match"):
        ys, ns = cands[(task, "yes")], cands[(task, "no")]
        n = min(len(ys), len(ns), N_PER_TASK // 2)
        stats[f"{task}_cands_yes"], stats[f"{task}_cands_no"] = len(ys), len(ns)
        for lab, lst in (("yes", ys[:n]), ("no", ns[:n])):
            for did, ti, names, state in lst:
                text = data[did]["log"][ti]["text"]
                edge = None
                if lab == "no":
                    alt = [x for x in names if x.split("-")[0] not in ("general", "Booking")
                           and x.split("-")[1] in ("Inform", "Recommend", "Select", "OfferBook")]
                    if task == "match" and alt:
                        edge = "exception"
                    elif NEG.search(text):
                        edge = "negation"
                    else:
                        edge = "implicit"
                out.append({
                    "key": KEY, "rid": f"{did.replace('.json', '')}_t{ti}_{task}", "state": state,
                    "instructions": BOOK_Q if task == "booking" else MATCH_Q,
                    "options": ["yes", "no"], "gold": lab, "soft": None,
                    "meta": {"dataset": DATASET, "config": f"MultiWOZ_2.1 system_acts; task={task}",
                             "revision": f"git:{COMMIT}; sha256 MultiWOZ_2.1.zip:{ZIP_SHA}",
                             "licence": LICENCE, "split": "train",
                             "orig_label": {"dialogue": did, "turn": ti, "system_acts": sorted(names)},
                             "family": C.FAMILY, "edge": edge, "defs": task}})
    rng.shuffle(out)
    C.write_rows(out, KEY)
    C.write_defs(BOOK_DEFS, KEY, "booking")
    C.write_defs(MATCH_DEFS, KEY, "match")
    print(dict(stats))
    C.report(out)


if __name__ == "__main__":
    main()
