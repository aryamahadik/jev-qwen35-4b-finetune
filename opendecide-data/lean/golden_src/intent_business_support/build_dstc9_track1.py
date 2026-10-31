"""Build golden rows for DSTC9 Track 1 (Beyond Domain APIs: knowledge-seeking turns), TRAIN split only.

Source : GitHub alexa/alexa-with-dstc9-track1-dataset @ 7ebb4c767b64826c1ac0f8bae409c0fab9cc0ae4:
         data/train/logs.json, data/train/labels.json, data/knowledge.json (val/ and data_eval/ never downloaded).
         MultiWOZ 2.1 (budzianowski/multiwoz @ fe0c8e65, MIT) is read only to map each DSTC9 dialogue to its MultiWOZ id,
         so that dialogues built on MultiWOZ validation/test dialogues are dropped and the multiwoz builder can avoid
         reusing the dialogues whose turns appear here.
Licence: Apache-2.0 (repo LICENSE file + README badge; NOTICE "Copyright Amazon.com, Inc. or its affiliates").
Texts  : MultiWOZ 2.1 human-human chats plus crowd-written knowledge-seeking user turns inserted by crowd workers;
         FAQ snippets collected from FAQ web pages; responses written by crowd workers from the snippet (Kim et al. 2020).
Labels : (kst) target = True for the inserted knowledge-seeking turns, False for original MultiWOZ user turns
         (label by construction of the corpus, not model-made).
         (faq_answer) the polarity of the crowd worker's knowledge-grounded response ("Yes, ..." / "No, ...") to a polar,
         non-negated customer question whose FAQ body itself does not start with yes/no (so the answer must be inferred).
Tasks  : kst        - yes/no: does the latest customer message need the FAQ documents rather than the booking database?
                      At most one positive and one negative instance per dialogue, with non-overlapping 5-turn windows;
                      only dialogues in MultiWOZ-partition 0; parking/wifi/internet turns dropped (those topics sit in
                      both the database and the FAQ pages, so the label is ambiguous); negatives whose MultiWOZ system
                      reply says the information is not available are dropped (off-database questions labelled False).
         faq_answer - yes/no: based only on the FAQ entry, is the answer to the customer's question yes?
                      Instances used by kst are not reused; <= 10 rows per FAQ snippet; unique questions.
Deterministic (seed 20261114).
"""
import collections
import json
import random
import re
import zipfile

import _ibs_common as C

KEY = "dstc9_track1"
SEED = 20261114
COMMIT = "7ebb4c767b64826c1ac0f8bae409c0fab9cc0ae4"
BASE = f"https://raw.githubusercontent.com/alexa/alexa-with-dstc9-track1-dataset/{COMMIT}/"
FILES = {
    "LICENSE": "09e8a9bcec8067104652c168685ab0931e7868f9c8284b66f5ae6edae5f1130b",
    "data/knowledge.json": "c8490242c23101c4e7c3e3482acd1d6dbf26c788f62c0c87fcaf622ee5360372",
    "data/train/logs.json": "39a87aafdc70e4adde0fc2e9b6e4caa3ab6ce8668bd7d17ea73b4534d7fa41d3",
    "data/train/labels.json": "615eac39a48f9068a30a92eff03092e301b20c43121cb5198acf8b3d67557d4e",
}
MWZ_COMMIT = "fe0c8e65cfcd8462bd33c86e35f21addc84ca82b"
MWZ_ZIP_SHA = "8db3f6afe591383b8523b271f07727693e73012ecce47f3ac7987191e09b7523"
LICENCE = (f"Apache-2.0 (https://github.com/alexa/alexa-with-dstc9-track1-dataset/blob/{COMMIT}/LICENSE and README "
           "licence badge; NOTICE 'Copyright Amazon.com, Inc. or its affiliates'); dialogues from MultiWOZ 2.1, MIT "
           f"(https://github.com/budzianowski/multiwoz/blob/{MWZ_COMMIT}/LICENSE)")
DATASET = "alexa/alexa-with-dstc9-track1-dataset (DSTC9 Track 1, augmented MultiWOZ 2.1)"
CACHE = C.CACHE / "dstc9"
MWZ_CACHE = C.CACHE / "multiwoz"
Q1_IDS_OUT = CACHE / "kst_mwz_ids.json"  # MultiWOZ ids whose turns appear in kst states (read by build_multiwoz21)

N_KST = 5000
N_FAQ = 3600
PER_DOC = 10  # max faq_answer rows per FAQ snippet
WINDOW = 5  # turns shown for kst (target user turn + up to 4 previous turns)

KST_Q = ("Does the customer's latest message need an answer from the business's FAQ and policy pages, rather than "
         "from the booking database or a booking action?")
FAQ_Q = "Based only on this FAQ entry, is the answer to the customer's question yes?"

DB_HEADER = (
    "Booking database (what the assistant can look up or book without the FAQ pages): hotels - name, area, price "
    "range, star rating, hotel or guesthouse, parking and internet (yes/no), address, phone, postcode, room booking; "
    "restaurants - name, food type, area, price range, address, phone, postcode, table booking; attractions - name, "
    "type, area, entrance fee, opening hours, address, phone, postcode; trains - departure, destination, day, leave and "
    "arrive times, duration, ticket price, train ID, seat booking; taxis - pickup, destination, times, car type, "
    "contact number.")

KST_DEFS = {
    "yes": ("The latest customer message asks about something the booking database does not hold (a policy, service "
            "or amenity detail such as pets, check-in times, payment, cancellations, discounts, accessibility or "
            "menu), so the FAQ pages must answer it."),
    "no": ("The latest customer message can be handled with the listed booking-database fields or a search or booking "
           "action, or it asks for no information at all (giving details, confirming, choosing, thanking)."),
}
FAQ_DEFS = {
    "yes": ("The FAQ entry implies the customer's question should be answered yes, including a yes that comes with a "
            "condition or limit (for example pets allowed only in a basket, or a service offered for a fee)."),
    "no": ("The FAQ entry does not support a yes: the thing is not offered, allowed or the case (even without saying "
           "'no', e.g. 'cash only' versus paying by card), or only other options are listed."),
}

PARK_WIFI = re.compile(r"park|wi-?fi|internet", re.I)
# FAQ docs whose topic is also a booking-database action (train 'Can I reserve a seat on the train?' vs the DB's
# train seat booking; MultiWOZ negatives say 'please reserve 3 seats'), so the kst label is ambiguous (review fix)
KST_AMBIG_DOCS = {("train", "*", "3")}
NO_INFO_REPLY = re.compile(r"(do not|don't|dont) have (that|any|this|the)? ?(information|info)|no information|"
                           r"not (sure|certain)|(don't|do not) know|unable to (find|locate) (that|this|any) info|"
                           r"(information|info) (is )?(not|isn't) (available|listed)|not listed|don't see (that|any) info",
                           re.I)
QUESTIONISH = re.compile(r"\?|^\W*(what|which|where|when|how|who|why|do|does|did|is|are|was|were|can|could|will|"
                         r"would|may|should|have|has)\b", re.I)
POLAR = re.compile(r"^(do|does|did|is|are|was|were|can|could|will|would|may|might|should|shall|have|has)\b", re.I)
NEG = re.compile(r"\b(not|no|never|without|none|nothing|nobody|neither|nor)\b|n't|\bcannot\b", re.I)
RESP_YES = re.compile(r"^\W*(yes|yeah|yep|absolutely|certainly|of course)\b", re.I)
RESP_NO = re.compile(r"^\W*(no|nope|unfortunately|sadly|sorry|i'm sorry|i am sorry|i'm afraid|i am afraid)\b", re.I)
BODY_YN = re.compile(r"^\W*(yes|no)\b", re.I)
COND = re.compile(r"\b(but|however|only|except|unless|as long as|must|provided|subject to|if|extra|fee|charge|"
                  r"up to|at least|maximum|limited)\b", re.I)
STOP = set("a an the i you we they it he she is are was were be to of in on at for with and or do does did can could "
           "will would may might should my your our their this that there here have has any some me us please "
           "about what which how get also know like just want need there's i'm".split())


def fetch_all():
    shas = {}
    for rel, sha in FILES.items():
        shas[rel] = C.fetch(BASE + rel, CACHE / rel, sha)
    C.fetch(f"https://github.com/budzianowski/multiwoz/raw/{MWZ_COMMIT}/data/MultiWOZ_2.1.zip",
            MWZ_CACHE / "MultiWOZ_2.1.zip", MWZ_ZIP_SHA)
    return shas


def load_multiwoz():
    with zipfile.ZipFile(MWZ_CACHE / "MultiWOZ_2.1.zip") as z:
        data = json.loads(z.read("MultiWOZ_2.1/data.json"))
        val = set(z.read("MultiWOZ_2.1/valListFile.txt").decode().split())
        test = set(z.read("MultiWOZ_2.1/testListFile.txt").decode().split())
    return data, val, test


def segment(logs):
    """Instances are prefixes ending at each user turn; a dialogue starts at a 1-turn instance."""
    dlg, cur = [], -1
    for i, l in enumerate(logs):
        if len(l) == 1:
            cur += 1
        else:
            prev = logs[i - 1]
            assert l[:len(prev)] == prev or len(l) == 1, i
        dlg.append(cur)
    return dlg


def map_dialogues(logs, dlg, mwz):
    """DSTC9 dialogue index -> MultiWOZ id (every MultiWOZ turn must appear, in order, in the DSTC9 dialogue)."""
    by_first = collections.defaultdict(list)
    for k, d in mwz.items():
        by_first[d["log"][0]["text"].strip()].append(k)
    last = {}
    for i, g in enumerate(dlg):
        last[g] = i
    out = {}
    for g, i in last.items():
        texts = [t["text"].strip() for t in logs[i]]
        # the last instance ends at the final user turn; MultiWOZ dialogues end with a system turn -> compare prefix
        hits = []
        for k in by_first.get(texts[0], []):
            mt = [t["text"].strip() for t in mwz[k]["log"]]
            it = iter(texts)
            if all(any(x == y for y in it) for x in mt[:-1]):  # ordered subsequence
                hits.append(k)
        if len(hits) == 1:
            out[g] = hits[0]
    return out


def content_words(t):
    return {w for w in re.findall(r"[a-z]+", t.lower()) if w not in STOP and len(w) > 2}


def speaker(s):
    return "Customer" if s == "U" else "Assistant"


def main():
    shas = fetch_all()
    logs = json.load(open(CACHE / "data/train/logs.json"))
    labels = json.load(open(CACHE / "data/train/labels.json"))
    know = json.load(open(CACHE / "data/knowledge.json"))
    assert len(logs) == len(labels)
    mwz, val, test = load_multiwoz()
    dlg = segment(logs)
    dmap = map_dialogues(logs, dlg, mwz)
    stats = collections.Counter()
    stats["dialogues"] = max(dlg) + 1
    stats["mapped"] = len(dmap)
    ok_dlg = {g for g, k in dmap.items() if k not in val and k not in test}
    stats["mapped_train"] = len(ok_dlg)
    rng = random.Random(SEED)

    # ---------------- kst: knowledge-seeking turn detection ----------------
    per_dlg = collections.defaultdict(lambda: {"pos": [], "neg": []})
    for i, (l, y) in enumerate(zip(logs, labels)):
        g = dlg[i]
        if g not in ok_dlg or C.mwz_partition(dmap[g]) != 0:
            continue
        text = l[-1]["text"].strip()
        if l[-1]["speaker"] != "U" or not (3 <= len(text.split()) <= 60):
            stats["kst_len_drop"] += 1
            continue
        if PARK_WIFI.search(text):
            stats["kst_parkwifi_drop"] += 1
            continue
        if y["target"] and any((k["domain"], str(k["entity_id"]), str(k["doc_id"])) in KST_AMBIG_DOCS
                               for k in y["knowledge"]):
            stats["kst_ambig_doc_drop"] += 1
            continue
        if not y["target"]:
            nxt = logs[i + 1] if i + 1 < len(logs) and dlg[i + 1] == g else None
            reply = nxt[len(l)]["text"] if nxt is not None and len(nxt) > len(l) else ""
            if NO_INFO_REPLY.search(reply):
                stats["kst_noinfo_reply_drop"] += 1
                continue
            per_dlg[g]["neg"].append(i)
        else:
            per_dlg[g]["pos"].append(i)

    def window_state(i):
        turns = logs[i][-WINDOW:]
        conv = "\n".join(f"{speaker(t['speaker'])}: {t['text'].strip()}" for t in turns)
        return f"{DB_HEADER}\n\nConversation (the last line is the customer's latest message):\n{conv}"

    kst_pos, kst_neg = [], []
    for g in sorted(per_dlg):
        p, n = per_dlg[g]["pos"], per_dlg[g]["neg"]
        rng.shuffle(p)
        # prefer question-like negatives (harder), keep some plain ones
        qn = [i for i in n if QUESTIONISH.search(logs[i][-1]["text"].strip())]
        pn = [i for i in n if i not in set(qn)]
        rng.shuffle(qn)
        rng.shuffle(pn)
        neg_order = qn + pn if rng.random() < 0.7 else pn + qn
        pi = p[0] if p else None
        ni = None
        for cand in neg_order:
            if pi is None or abs(len(logs[cand]) - len(logs[pi])) >= WINDOW + 1:
                ni = cand
                break
        if pi is not None:
            kst_pos.append(pi)
        if ni is not None:
            kst_neg.append(ni)
    rng.shuffle(kst_pos)
    rng.shuffle(kst_neg)
    n_bal = min(len(kst_pos), len(kst_neg), N_KST // 2)
    kst_pos, kst_neg = kst_pos[:n_bal], kst_neg[:n_bal]

    rows, seen = [], set()
    used_kst, kst_mwz = set(), set()
    for i in kst_pos + kst_neg:
        y = labels[i]
        st = window_state(i)
        n = C.norm(st)
        if n in seen:
            stats["kst_dup_drop"] += 1
            continue
        seen.add(n)
        used_kst.add(i)
        kst_mwz.add(dmap[dlg[i]])
        text = logs[i][-1]["text"].strip()
        edge = None
        if y["target"] and not QUESTIONISH.search(text):
            edge = "implicit"
        elif len(st) > 1500:
            edge = "long_context"
        orig = {"target": y["target"], "mwz_dialogue": dmap[dlg[i]]}
        if y["target"]:
            orig["knowledge"] = y["knowledge"]
        rows.append({
            "key": KEY, "rid": f"dstc9_train_{i}_kst", "state": st, "instructions": KST_Q,
            "options": ["yes", "no"], "gold": "yes" if y["target"] else "no", "soft": None,
            "meta": {"dataset": DATASET, "config": "data/train logs+labels; task=knowledge-seeking turn detection",
                     "revision": f"git:{COMMIT}; sha256 logs:{shas['data/train/logs.json'][:16]} "
                                 f"labels:{shas['data/train/labels.json'][:16]}",
                     "licence": LICENCE, "split": "train", "orig_label": orig, "family": C.FAMILY, "edge": edge,
                     "defs": "kst"}})

    # ---------------- faq_answer: yes/no answer implied by the FAQ entry ----------------
    cands = {"yes": [], "no": []}
    for i, (l, y) in enumerate(zip(logs, labels)):
        if not y["target"] or i in used_kst or dlg[i] not in ok_dlg:
            continue
        q = l[-1]["text"].strip()
        if q.count("?") != 1:
            stats["faq_multi_q_drop"] += 1
            continue
        # the question sentence: last sentence ending with '?'
        sents = re.split(r"(?<=[.!?])\s+", q)
        qs = [s for s in sents if s.endswith("?")]
        if not qs:
            continue
        qsent = qs[-1].strip()
        if not POLAR.match(qsent) or NEG.search(q) or not (4 <= len(qsent.split()) <= 25):
            stats["faq_not_polar_or_neg_drop"] += 1
            continue
        kn = y["knowledge"][0]
        ent = know[kn["domain"]][str(kn["entity_id"])]
        doc = ent["docs"][str(kn["doc_id"])]
        body, resp = doc["body"].strip(), y["response"].strip()
        if BODY_YN.match(body):
            stats["faq_body_yesno_drop"] += 1
            continue
        pol = "yes" if RESP_YES.match(resp) else "no" if RESP_NO.match(resp) else None
        if pol is None:
            stats["faq_resp_unclear_drop"] += 1
            continue
        first_clause = re.split(r"[.,;!]", resp, maxsplit=2)
        fc = " ".join(first_clause[:2]) if pol == "yes" else ""
        if pol == "yes" and NEG.search(fc.replace("Yes", "")):  # "Yes, ... not ..." in the first clause -> unclear
            stats["faq_resp_conflict_drop"] += 1
            continue
        cands[pol].append((i, q, kn, ent, doc))

    def faq_state(q, kn, ent, doc):
        who = ent.get("name")
        if who:
            who = who.title() if who.isupper() else who
            head = f"FAQ entry ({kn['domain']}: {who})"
        else:
            head = f"FAQ entry (Cambridge {kn['domain']} service)"
        return f"{head}\nQ: {doc['title'].strip()}\nA: {doc['body'].strip()}\n\nCustomer question: {q}"

    faq_rows = {"yes": [], "no": []}
    per_doc = collections.Counter()
    seen_q = set()
    for pol in ("yes", "no"):
        rng.shuffle(cands[pol])
    order = [("yes", c) for c in cands["yes"]] + [("no", c) for c in cands["no"]]
    for pol, (i, q, kn, ent, doc) in order:
        dk = (kn["domain"], str(kn["entity_id"]), str(kn["doc_id"]))
        nq = C.norm(q)
        if nq in seen_q or per_doc[dk] >= PER_DOC:
            continue
        st = faq_state(q, kn, ent, doc)
        if C.norm(st) in seen:
            continue
        seen_q.add(nq)
        seen.add(C.norm(st))
        per_doc[dk] += 1
        faq_rows[pol].append((i, st, q, kn, doc))
    n_bal = min(len(faq_rows["yes"]), len(faq_rows["no"]), N_FAQ // 2)
    for pol in ("yes", "no"):
        for i, st, q, kn, doc in faq_rows[pol][:n_bal]:
            body = doc["body"]
            if NEG.search(body):
                edge = "negation"
            elif pol == "no":
                edge = "implicit"  # the no follows from 'free', 'cash only', a list of other options, ...
            elif COND.search(body):
                edge = "exception"
            else:
                cw = content_words(q)
                ov = len(cw & content_words(doc["title"] + " " + body)) / max(1, len(cw))
                edge = "implicit" if ov < 0.34 else None
            rows.append({
                "key": KEY, "rid": f"dstc9_train_{i}_faq", "state": st, "instructions": FAQ_Q,
                "options": ["yes", "no"], "gold": pol, "soft": None,
                "meta": {"dataset": DATASET, "config": "data/train labels + knowledge.json; task=FAQ-implied yes/no",
                         "revision": f"git:{COMMIT}; sha256 labels:{shas['data/train/labels.json'][:16]} "
                                     f"knowledge:{shas['data/knowledge.json'][:16]}",
                         "licence": LICENCE, "split": "train",
                         "orig_label": {"response": labels[i]["response"], "knowledge": kn,
                                        "mwz_dialogue": dmap[dlg[i]]},
                         "family": C.FAMILY, "edge": edge, "defs": "faq_answer"}})

    rng.shuffle(rows)
    C.write_rows(rows, KEY)
    C.write_defs(KST_DEFS, KEY, "kst")
    C.write_defs(FAQ_DEFS, KEY, "faq_answer")
    with open(Q1_IDS_OUT, "w") as f:
        json.dump(sorted(kst_mwz), f)
    print(dict(stats))
    print(f"kst candidates: pos={len(kst_pos)} neg={len(kst_neg)}; faq candidates: "
          f"yes={len(cands['yes'])} no={len(cands['no'])} after caps yes={len(faq_rows['yes'])} no={len(faq_rows['no'])}")
    C.report(rows)


if __name__ == "__main__":
    main()
