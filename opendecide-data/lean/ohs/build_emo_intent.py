"""OHS-1 part "emo_intent" (track U: unseen label sets).

(a) GoEmotions (google-research-datasets/go_emotions, config "simplified", TEST split):
    Reddit comments with exactly one gold label, choice over all 28 official
    labels (27 emotions + neutral). High-agreement filter (the "simplified" gold
    only needs 2 raters, which is noisy): joined with the "raw" config on id,
    the gold emotion must be chosen by >= 3 raters AND by a strict majority of
    the raters, and no rater may have flagged the comment "example_very_unclear".
    Card = the emotion definitions from Appendix A of Demszky et al. 2020
    (arXiv:2005.00547), copied verbatim; "neutral" has no definition there, so
    its card line is the paper's own rater instruction sentence for Neutral
    (Section 3.3, verbatim). Rare classes (grief, pride, relief, nervousness,
    embarrassment) have only 1-4 test items that pass the filter, so they are
    under-represented; we stay on the test split rather than mix in validation.
(b) Schema-Guided Dialogue (DSTC8 SGD, official GitHub repo, TEST split; the HF
    copy google-research-datasets/schema_guided_dstc8 is script-only):
    user turns where a new active intent starts, only for test services that are
    NOT in the train schema. State = the last two turns (system turn + user
    turn; only the user turn when it opens the dialogue).
    Options = every intent of every test-schema service in the dialogue's
    domains (domain = service-name prefix, e.g. Hotels_2 + Hotels_4; names
    de-duplicated), shuffled per item with a fixed seed, + "none of these" last.
    Card = the official schema intent descriptions.
    Gold-quality filters (SGD user turns are crowd paraphrases of simulator acts
    and sometimes do not say what the annotated intent is):
      - the user turn touches exactly one service (one frame);
      - the intent start is explicit: the user's own INFORM_INTENT act for that
        intent, or AFFIRM_INTENT answering the system's OFFER_INTENT for it;
      - lexical cue check against the same-domain alternatives (INTENT_CUES):
        a non-default intent needs its own cue in the text, and no same-domain
        alternative's cue may appear (e.g. a FindBus turn that asks for
        "tickets", a one-way flight turn that never says "one way");
      - the two turns shown must name the gold domain (DOMAIN_ANCHORS);
      - a short manual exclusion list (SGD_EXCLUDE / GOEMO_EXCLUDE) for items
        whose source gold is contradicted by the text on reading.
    "none of these" rows (NONE_FRAC of the part): the gold domain's intents
    are replaced by the intents of one other test-schema domain that is not in
    the dialogue and not in a related domain group (DOMAIN_GROUPS), chosen with
    a per-item seed and matching the gold domain's intent count when possible;
    the gold is then "none of these". Only dialogues whose other domains are
    also unrelated to the gold domain are used for these rows.
    Caveat for Track U: the SGD label NAMES and descriptions are new to our
    training, but several intent CONCEPTS (set alarm, share location, book a
    hotel/restaurant/flight, play music, transfer money, ...) do appear as
    CLINC150/MASSIVE labels in our training data.

No LLM text anywhere: states, labels and descriptions all come from the datasets
or the paper; only the short question templates below are ours.

Re-runnable: raw downloads are cached under $OHS_RAW_CACHE (default
~/.cache/ohs_raw; the SGD test dialogues are ~108 MB so they stay out of the repo).

    .venv/bin/python ohs/build_emo_intent.py
"""
import collections
import glob
import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import sys

import requests

SEED = 20260927
PART = "emo_intent"
HERE = os.path.dirname(os.path.abspath(__file__))
LEAN = os.path.dirname(HERE)
OUT_DIR = os.path.join(LEAN, "data", "ohs_parts")
OUT = os.path.join(OUT_DIR, PART + ".jsonl")
RAW = os.environ.get("OHS_RAW_CACHE", os.path.expanduser("~/.cache/ohs_raw"))

N_GOEMO = 150
N_SGD = 200
NONE_FRAC = 0.20          # share of SGD rows whose gold is "none of these"
MIN_LEN, MAX_LEN = 20, 6000
MAX_SHARE = 0.40
GOEMO_MIN_VOTES = 3       # raters who chose the gold emotion

# ---------------------------------------------------------------- GoEmotions
GOEMO_HF = "google-research-datasets/go_emotions"
GOEMO_PAPER = "https://arxiv.org/pdf/2005.00547"

# Verbatim from Appendix A "Emotion Definitions" of Demszky et al. (2020),
# arXiv:2005.00547 (extracted with pdftotext; re-verified against the PDF in
# verify_goemo_definitions() whenever pdftotext is available).
GOEMO_DEFS = {
    "admiration": "Finding something impressive or worthy of respect.",
    "amusement": "Finding something funny or being entertained.",
    "anger": "A strong feeling of displeasure or antagonism.",
    "annoyance": "Mild anger, irritation.",
    "approval": "Having or expressing a favorable opinion.",
    "caring": "Displaying kindness and concern for others.",
    "confusion": "Lack of understanding, uncertainty.",
    "curiosity": "A strong desire to know or learn something.",
    "desire": "A strong feeling of wanting something or wishing for something to happen.",
    "disappointment": "Sadness or displeasure caused by the nonfulfillment of one’s hopes or expectations.",
    "disapproval": "Having or expressing an unfavorable opinion.",
    "disgust": "Revulsion or strong disapproval aroused by something unpleasant or offensive.",
    "embarrassment": "Self-consciousness, shame, or awkwardness.",
    "excitement": "Feeling of great enthusiasm and eagerness.",
    "fear": "Being afraid or worried.",
    "gratitude": "A feeling of thankfulness and appreciation.",
    "grief": "Intense sorrow, especially caused by someone’s death.",
    "joy": "A feeling of pleasure and happiness.",
    "love": "A strong positive emotion of regard and affection.",
    "nervousness": "Apprehension, worry, anxiety.",
    "optimism": "Hopefulness and confidence about the future or the success of something.",
    "pride": "Pleasure or satisfaction due to ones own achievements or the achievements of those with whom one is closely associated.",
    "realization": "Becoming aware of something.",
    "relief": "Reassurance and relaxation following release from anxiety or distress.",
    "remorse": "Regret or guilty feeling.",
    "sadness": "Emotional pain, sorrow.",
    "surprise": "Feeling astonished, startled by something unexpected.",
}
# Appendix A has no entry for Neutral; this is the paper's own instruction to
# raters about when to pick Neutral (Section 3.3 "Instructions"), verbatim.
GOEMO_NEUTRAL = ("If raters were not certain about any emotion being expressed, "
                 "they were asked to select Neutral.")

# ---------------------------------------------------------------- SGD
SGD_REPO = "https://raw.githubusercontent.com/google-research-datasets/dstc8-schema-guided-dialogue/master"
SGD_N_TEST_FILES = 34
NONE_OPT = "none of these"

# Domains whose intents could plausibly serve the same user request; a
# "none of these" row never borrows a substitute domain from the gold
# domain's group (and its dialogue's other domains must be outside it too).
DOMAIN_GROUPS = [
    {"Buses", "Flights", "Trains", "RentalCars", "RideSharing"},  # getting somewhere
    {"Hotels", "Homes"},                                          # a place to stay / live
    {"Events", "Travel", "Movies", "Media", "Music"},             # something to do / watch / hear
]

# Lexical cues per intent name (lower-cased text). "need": regexes that must
# all match when the intent is the gold (empty = the default/search intent of
# its service, no cue needed). "alt": regex that must NOT match when the intent
# is a same-domain alternative to the gold. Checked on the user turn (for an
# INFORM_INTENT start) or on system+user turn (for an AFFIRM_INTENT start).
_FIND = (r"\b(find|finding|search\w*|look(ing)?\s+(for|up|into|around)|look\s+up"
         r"|check\s+(for|out|what|if)|browse|explore|discover\w*)\b")
_SUGG = r"\b(suggest\w*|recommend\w*|propos\w*)\b"
_BUY = r"\b(buy\w*|bought|purchas\w*|book\w*|reserv\w*|tickets?)\b"
_RES = r"\b(reserv\w*|book\w*)\b"
_ROUND = (r"\bround[\s-]?trip\w*|\bfull\s+circle\b|\breturn\w*|\bcom(e|ing)\s+back\b"
          r"|\bback\s+(on|home)\b|\btwo[\s-]?way\b|\bboth\s+ways\b")
_VISIT = r"\b(visit\w*|tour\w*|schedul\w*|viewing)\b|\bsee\s+(the|this|that|it|a)\b"
_HOTEL = r"\b(hotels?|rooms?|accommodat\w*|motels?)\b"
_PLAY_M = r"\b(play\w*|watch\w*|stream\w*|start\w*|view\w*)\b|\bsee\s+(it|that|this|the\s+(movie|film))\b"
_PLAY_MU = r"\b(play\w*|listen\w*|hear\w*|cast\w*|start\w*|stream\w*)\b|\bput\s+(it\s+)?on\b"
_REQ = (r"\brequest\w*|\bask\w*\s+(for|\w+\s+(for|to\s+send))\b|\bowe[sd]?\b|\bcollect\w*"
        r"|\breceiv\w*")
INTENT_CUES = {
    "FindBus": {"need": [], "alt": _FIND + r"|\bany\s+bus"},
    "BuyBusTicket": {"need": [_BUY + r"|\bseats?\b"], "alt": _BUY + r"|\bseats?\b"},
    "FindEvents": {"need": [], "alt": _FIND + r"|\b(something|things)\s+(\w+\s+)?to\s+do\b"
                                      r"|\bany\s+(events?|concerts?|shows?|plays?)\b"
                                      r"|\bwhat'?s\s+(happening|going\s+on)"},
    "BuyEventTickets": {"need": [_BUY], "alt": _BUY},
    "SearchOnewayFlight": {"need": [r"\bone[\s-]?way\b"], "alt": r"\bone[\s-]?way\b"},
    "SearchRoundtripFlights": {"need": [_ROUND], "alt": _ROUND},
    "FindHomeByArea": {"need": [], "alt": _FIND + r"|\bplace\s+to\s+(live|rent)\b"},
    "ScheduleVisit": {"need": [_VISIT], "alt": _VISIT},
    "SearchHotel": {"need": [_HOTEL], "alt": _FIND + r"|\bany\s+hotels?\b"},
    "ReserveHotel": {"need": [_RES, _HOTEL], "alt": _RES},
    "SearchHouse": {"need": [r"\bhouses?\b"], "alt": r"\b(houses?|homes?)\b"},
    "BookHouse": {"need": [r"\bhouses?\b"], "alt": r"\b(houses?|homes?)\b"},
    "FindMovies": {"need": [], "alt": _FIND + "|" + _SUGG
                                      + r"|\bany\s+(good\s+|nice\s+)?(online\s+)?(movies|films)\b"},
    "PlayMovie": {"need": [_PLAY_M], "alt": _PLAY_M},
    "BuyMovieTickets": {"need": [_BUY], "alt": _BUY},
    "GetTimesForMovie": {"need": [r"\btimes?\b"],
                         "alt": r"\bshow\s*times?\b|\bwhat\s+time\b|\btimes?\b|\bshowing\w*"
                                r"|\bscreening\w*|\btheat(er|re)s?\b|\bcinemas?\b"},
    "LookupMusic": {"need": [_FIND + "|" + _SUGG], "alt": _FIND + "|" + _SUGG},
    "PlayMedia": {"need": [_PLAY_MU], "alt": _PLAY_MU},
    "MakePayment": {"need": [r"\b(make|making|send\w*|pay|paying|transfer\w*)\b"],
                    "alt": r"\b(pay|paying)\b|\bsend\w*\s+(money|cash|\$|\d|some)"},
    "RequestPayment": {"need": [_REQ], "alt": _REQ},
    "GetCarsAvailable": {"need": [], "alt": _FIND + r"|\bavailab\w*|\bany\s+(rental\s+)?cars?\b|\boptions?\b"},
    "ReserveCar": {"need": [_RES], "alt": _RES},
    "FindRestaurants": {"need": [], "alt": _FIND + "|" + _SUGG + r"|\bany\s+(good\s+|nice\s+)?restaurants?\b"},
    "ReserveRestaurant": {"need": [r"\b(reserv\w*|book\w*|tables?)\b"], "alt": r"\b(reserv\w*|book\w*|tables?)\b"},
    "FindProvider": {"need": [], "alt": _FIND + "|" + _SUGG},
    "BookAppointment": {"need": [r"\b(book\w*|appointments?|schedul\w*|reserv\w*|sessions?)\b"],
                        "alt": r"\b(book\w*|appointments?|schedul\w*|reserv\w*|sessions?)\b"},
    "FindTrains": {"need": [], "alt": _FIND + r"|\bany\s+trains?\b|\bavailab\w*"},
    "GetTrainTickets": {"need": [_BUY + r"|\bseats?\b"], "alt": _BUY + r"|\bseats?\b"},
    "GetAlarms": {"need": [r"\balarms\b|\b(my|current|existing)\s+alarm\b|\bwhat\s+alarm|\bany\s+alarm"],
                  "alt": r"\b(show|check|see|view|list|current|existing)\b|\btell\s+me\s+about\b"
                         r"|\bwhat\s+alarms\b|\bmy\s+alarms\b"},
    "AddAlarm": {"need": [r"\b(set\w*|add\w*|creat\w*|new|make|wake\s+me)\b"],
                 "alt": r"\b(add\w*|creat\w*)\b|\bnew\s+alarm|\bset\s+(up\s+)?(an|a\s+new|another|one\s+more)\s+alarm"
                        r"|\bwake\s+me"},
    "ShareLocation": {"need": [r"\b(shar\w*|send\w*|locat\w*|address)\b"], "alt": r"\b(shar\w*|locat\w*)\b"},
    "GetRide": {"need": [r"\b(ride|cab|taxi)\b"], "alt": r"\b(ride|cab|taxi)\b"},
    "FindAttractions": {"need": [], "alt": r"\battractions?\b"},
    "GetWeather": {"need": [r"\bweather\b"], "alt": r"\bweather\b"},
}

# Manual adjudication (builder review of every sampled row): items whose
# source gold is contradicted by, or not determined by, the text shown.
# key -> reason. Excluded items are replaced by the next item of the same class.
GOEMO_EXCLUDE = {
    "goemo:eedvwoz": "writer tells someone they should be embarrassed: disapproval/disgust, "
                     "not the writer's embarrassment",
    "goemo:eed7qb0": "'I'm more interested in why there are goldfish...' is curiosity, not excitement",
    "goemo:ede7p7v": "sarcastic 'I love how having high standards is used as an insult': not love",
    "goemo:eda854m": "sarcastic mock apology 'I'm so sorry the internet has inconvenienced you': "
                     "not remorse",
    "goemo:edz2b6d": "'I'm sorry your trust has been that badly broken' is sympathy "
                     "(caring/sadness), not regret or guilt",
    "goemo:ef1r7bj": "'I'm wondering why this sub just started worshiping them' is curiosity, "
                     "not surprise",
    "goemo:ee3er1y": "'This sounds an awful lot like khorne......' shows no clear disgust",
    "goemo:edd2cj3": "sarcastic 'My dad loves playing sport...slam dunking my arse': not the "
                     "writer's love",
    "goemo:ed9d7vj": "'Sorry I dropped this /s' is a sarcasm-tagged meme: not remorse",
}
SGD_EXCLUDE = {
    "sgd:14_00003:turn0": "'I'd like to see several films online': FindMovies vs PlayMovie "
                          "not determined by the text",
}

# The two-turn state must name the gold domain (so e.g. "yes, book the
# tickets" cannot be read as bus, train or event tickets).
DOMAIN_ANCHORS = {
    "Alarm": r"\balarms?\b",
    "Buses": r"\bbus(es)?\b",
    "Events": r"\b(events?|concerts?|shows?|plays?|games?|match(es)?|musicals?|theat(er|re)s?)\b"
              r"|\b(things?|something)\s+(\w+\s+)?to\s+do\b",
    "Flights": r"\b(flights?|fly|flying|plane|airlines?|airport)\b",
    "Homes": r"\b(propert(y|ies)|apartments?|house|home|visit)\b|\bplace\s+(\w+\s+)?(to\s+)?live",
    "Hotels": r"\b(hotels?|rooms?|accommodat\w*|motels?)\b",
    "Media": r"\b(movies?|films?)\b",
    "Messaging": r"\b(locat\w*|address)\b",
    "Movies": r"\b(movies?|films?|cinemas?|theat(er|re)s?)\b",
    "Music": r"\b(songs?|music|albums?|tracks?|singer|band)\b",
    "Payment": r"\$|\b(pay\w*|money|transfer\w*|transaction|bucks|dollars|funds)\b",
    "RentalCars": r"\b(cars?|vehicle|suv|sedan|rental)\b",
    "Restaurants": r"\b(restaurants?|tables?|eat|dinner|lunch|breakfast|food|dine|dining|diner|meal)\b",
    "RideSharing": r"\b(cab|ride|taxi)\b",
    "Services": r"\b(therapist|psycholog\w*|psychiatr\w*|counsel\w*|appointment|doctor|stylist|salon)\b",
    "Trains": r"\b(trains?|rail\w*|locomotives?)\b",
    "Travel": r"\b(attractions?|sightsee\w*|museums?|parks?)\b",
    "Weather": r"\b(weather|rain\w*|forecast|temperature)\b",
}


def norm(t):
    t = t.lower()
    t = re.sub(r"[^0-9a-z]+", " ", t)
    return " ".join(t.split())


def hkey(*parts):
    """Stable per-item sort key (seeded hash), so excluding one item never
    reshuffles any other class."""
    return hashlib.sha1(("%d:" % SEED + ":".join(map(str, parts))).encode()).hexdigest()


def fetch(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return path
    os.makedirs(os.path.dirname(path), exist_ok=True)
    r = requests.get(url, timeout=300)
    r.raise_for_status()
    tmp = path + ".part"
    with open(tmp, "wb") as f:
        f.write(r.content)
    os.replace(tmp, path)
    return path


def rr_sample(pools, n, rng, id_fn, key_fn=None, used=None):
    """Round-robin stratified sampling: one item per class per round, class
    order reshuffled every round (rng), items within a class taken in seeded
    hash order. Classes end up within 1 of each other except classes that run
    out. key_fn(item) -> key that must stay unique across the sample (and
    across `used`, which is updated in place)."""
    pools = {k: collections.deque(sorted(v, key=lambda it: hkey(id_fn(it))))
             for k, v in pools.items()}
    used = set() if used is None else used
    out = []
    classes = sorted(pools)
    while len(out) < n and any(pools.values()):
        order = classes[:]
        rng.shuffle(order)
        for c in order:
            while pools[c]:
                it = pools[c].popleft()
                key = key_fn(it) if key_fn else None
                if key is not None and key in used:
                    continue
                if key is not None:
                    used.add(key)
                out.append((c, it))
                break
            if len(out) >= n:
                break
    return out


def check_share(golds, name):
    c = collections.Counter(golds)
    top, k = c.most_common(1)[0]
    share = k / len(golds)
    assert share <= MAX_SHARE, (name, top, share)
    return c


def verify_goemo_definitions():
    """Re-extract Appendix A from the paper PDF and check GOEMO_DEFS matches."""
    if not shutil.which("pdftotext"):
        return "skipped (pdftotext not installed)"
    try:
        pdf = fetch(GOEMO_PAPER, os.path.join(RAW, "goemotions", "2005.00547.pdf"))
    except Exception as e:  # offline re-run: keep embedded copy
        return "skipped (paper download failed: %s)" % e
    txt = subprocess.run(["pdftotext", pdf, "-"], capture_output=True, text=True).stdout
    i = txt.index("Emotion Definitions")
    j = txt.index("Taxonomy Selection", i)
    block = " ".join(txt[i + len("Emotion Definitions"):j].split())
    block = re.sub(r"\s+B$", "", block)
    names = list(GOEMO_DEFS)
    pos, found = 0, {}
    starts = []
    for nm in names:
        m = re.compile(r"(?:^|\s)" + nm + r"\s+(?=[A-Z])").search(block, pos)
        assert m, nm
        starts.append((nm, m.start(), m.end()))
        pos = m.end()
    for k, (nm, s, e) in enumerate(starts):
        end = starts[k + 1][1] if k + 1 < len(starts) else len(block)
        found[nm] = block[e:end].strip()
    bad = {k: (found[k], GOEMO_DEFS[k]) for k in names if found[k] != GOEMO_DEFS[k]}
    assert not bad, bad
    return "ok (27/27 definitions match the PDF)"


def goemo_rater_stats(names):
    """Per comment id from the 'raw' config (one row per rater): votes per
    label, number of raters, number of 'example_very_unclear' flags."""
    from datasets import load_dataset
    df = load_dataset(GOEMO_HF, "raw")["train"].to_pandas()
    g = df.groupby("id")
    return g[names].sum(), g.size(), g["example_very_unclear"].sum()


def build_goemo(rng):
    from datasets import load_dataset
    ds = load_dataset(GOEMO_HF, "simplified")["test"]
    names = ds.features["labels"].feature.names
    assert len(names) == 28 and names[-1] == "neutral"
    assert list(GOEMO_DEFS) == names[:-1]
    votes, n_raters, unclear = goemo_rater_stats(names)
    # normalized-text -> set of label tuples, over the whole test split
    seen = collections.defaultdict(set)
    for ex in ds:
        seen[norm(ex["text"])].add(tuple(sorted(ex["labels"])))
    pools = collections.defaultdict(list)
    stats = collections.Counter()
    for ex in ds:
        if len(ex["labels"]) != 1:
            stats["multi_label"] += 1
            continue
        lab = names[ex["labels"][0]]
        i = ex["id"]
        if i not in n_raters.index:
            stats["no_raw_ratings"] += 1
            continue
        v, n, u = int(votes.at[i, lab]), int(n_raters[i]), int(unclear[i])
        if v < GOEMO_MIN_VOTES:
            stats["gold_votes_lt_3"] += 1
            continue
        if 2 * v <= n:
            stats["gold_not_strict_majority"] += 1
            continue
        if u:
            stats["rater_flagged_very_unclear"] += 1
            continue
        if "goemo:" + i in GOEMO_EXCLUDE:
            stats["manual_exclude"] += 1
            continue
        t = ex["text"].strip()
        if not (MIN_LEN <= len(t) <= MAX_LEN):
            stats["length"] += 1
            continue
        if len(seen[norm(t)]) > 1:
            stats["dup_conflicting_labels"] += 1
            continue
        pools[lab].append(dict(ex, _votes=v, _raters=n))
    picked = rr_sample(pools, N_GOEMO, rng, id_fn=lambda ex: ex["id"],
                       key_fn=lambda ex: norm(ex["text"]))
    card = "\n".join(["- %s: %s" % (k, v) for k, v in GOEMO_DEFS.items()]
                     + ["- neutral: " + GOEMO_NEUTRAL])
    rows = []
    for lab, ex in picked:
        rows.append({
            "source": "go_emotions",
            "_gid": "goemo:" + ex["id"],
            "state": "Reddit comment:\n" + ex["text"].strip(),
            "qtype": "choice",
            "instructions": "Which emotion does the writer of this comment express?",
            "options": list(names),
            "gold": lab,
            "role": "choice",
            "card": card,
            "meta": {"license": "apache-2.0", "hf_id": GOEMO_HF, "config": "simplified",
                     "split_used": "test", "source_id": ex["id"],
                     "filter": "exactly one gold label; gold chosen by >=3 raters and a "
                               "strict majority (raw config); no 'very unclear' flag",
                     "gold_votes": ex["_votes"], "n_raters": ex["_raters"],
                     "text_note": "Reddit comment (Reddit terms apply to the text); "
                                  "may be offensive",
                     "card_source": "Demszky et al. 2020 (arXiv:2005.00547) Appendix A; "
                                    "neutral line = Section 3.3 rater instruction"},
        })
    info = {"pool_sizes_after_filters": {k: len(v) for k, v in sorted(pools.items())},
            "dropped": dict(stats)}
    return rows, info


def load_sgd():
    base = os.path.join(RAW, "sgd")
    tr_schema = json.load(open(fetch(SGD_REPO + "/train/schema.json",
                                     os.path.join(base, "train", "schema.json"))))
    te_schema = json.load(open(fetch(SGD_REPO + "/test/schema.json",
                                     os.path.join(base, "test", "schema.json"))))
    dialogues = []
    for i in range(1, SGD_N_TEST_FILES + 1):
        fn = "dialogues_%03d.json" % i
        dialogues += json.load(open(fetch(SGD_REPO + "/test/" + fn,
                                          os.path.join(base, "test", fn))))
    return tr_schema, te_schema, dialogues


def domain(service):
    return service.split("_")[0]


def group_of(dom):
    return next((g for g in DOMAIN_GROUPS if dom in g), {dom})


def cue_problem(gold, alts, text):
    t = text.lower()
    for rx in INTENT_CUES[gold]["need"]:
        if not re.search(rx, t):
            return "no_gold_cue"
    for a in alts:
        if re.search(INTENT_CUES[a]["alt"], t):
            return "alt_cue"
    return None


def build_sgd(rng):
    tr_schema, te_schema, dialogues = load_sgd()
    train_services = {s["service_name"] for s in tr_schema}
    svc = {s["service_name"]: s for s in te_schema}
    unseen = sorted(s for s in svc if s not in train_services)
    dom_services = collections.defaultdict(list)
    for s in sorted(svc):
        dom_services[domain(s)].append(s)
    all_domains = sorted(dom_services)
    for s in svc.values():
        for it in s["intents"]:
            assert it["name"] in INTENT_CUES, it["name"]
    assert set(all_domains) <= set(DOMAIN_ANCHORS), set(all_domains) - set(DOMAIN_ANCHORS)

    def domain_intents(dom, prefer):
        """(name, description) for every test-schema service of `dom`,
        de-duplicated by name; the description comes from the first service in
        `prefer` that has the name, else from the first service in name order."""
        out = collections.OrderedDict()
        order = [s for s in prefer if domain(s) == dom] + dom_services[dom]
        for s in order:
            for it in svc[s]["intents"]:
                out.setdefault(it["name"], it["description"])
        return list(out.items())

    def names_by_domain(doms):
        m = collections.defaultdict(set)
        for dm in doms:
            for s in dom_services[dm]:
                for it in svc[s]["intents"]:
                    m[it["name"]].add(dm)
        return m

    stats = collections.Counter()
    cands = collections.defaultdict(list)
    state_count = collections.Counter()
    for d in dialogues:
        doms = list(dict.fromkeys(domain(s) for s in d["services"]))
        cross = [n for n, ds_ in names_by_domain(doms).items() if len(ds_) > 1]
        prev = set()
        turns = d["turns"]
        for ti, t in enumerate(turns):
            if t["speaker"] != "USER":
                continue
            cur = {(f["service"], f["state"]["active_intent"]) for f in t["frames"]
                   if f["state"]["active_intent"] != "NONE"}
            new = cur - prev
            if cur:
                prev = cur
            if len(new) != 1:
                continue
            s, intent = next(iter(new))
            if s in train_services:
                continue
            stats["new_intent_turns_unseen_service"] += 1
            if cross:  # same intent name in two domains of this dialogue
                stats["skip_cross_domain_name_collision"] += 1
                continue
            if len(t["frames"]) != 1:
                stats["skip_user_turn_touches_2_services"] += 1
                continue
            acts = t["frames"][0]["actions"]
            sys_t = turns[ti - 1] if ti > 0 and turns[ti - 1]["speaker"] == "SYSTEM" else None
            if any(a["act"] == "INFORM_INTENT" and a["values"] == [intent] for a in acts):
                how = "INFORM_INTENT"
                cue_text = t["utterance"]
            elif (any(a["act"] == "AFFIRM_INTENT" for a in acts) and sys_t is not None
                  and any(a["act"] == "OFFER_INTENT" and a["values"] == [intent]
                          for f in sys_t["frames"] if f["service"] == s
                          for a in f["actions"])):
                how = "AFFIRM_INTENT"
                cue_text = sys_t["utterance"] + " " + t["utterance"]
            else:
                stats["skip_intent_start_not_explicit"] += 1
                continue
            gdom = domain(s)
            gold_dom_intents = domain_intents(gdom, [s] + d["services"])
            alts = [n for n, _ in gold_dom_intents if n != intent]
            prob = cue_problem(intent, alts, cue_text)
            if prob:
                stats["skip_" + prob] += 1
                continue
            two_turns = ((sys_t["utterance"] + " ") if sys_t is not None else "") + t["utterance"]
            if not re.search(DOMAIN_ANCHORS[gdom], two_turns.lower()):
                stats["skip_gold_domain_not_named"] += 1
                continue
            other_doms = [dm for dm in doms if dm != gdom]
            pos_opts = list(gold_dom_intents)
            for dm in other_doms:
                pos_opts += domain_intents(dm, d["services"])
            if len({n for n, _ in pos_opts}) < 3:  # 1-2 intents: near-trivial choice
                stats["skip_fewer_than_3_intents"] += 1
                continue
            sid = "%s:turn%d" % (d["dialogue_id"], ti)
            if "sgd:" + sid in SGD_EXCLUDE:
                stats["manual_exclude"] += 1
                continue
            lines = []
            if sys_t is not None:
                lines.append("System: " + sys_t["utterance"].strip())
            lines.append("User: " + t["utterance"].strip())
            state = "Dialogue (latest turns):\n" + "\n".join(lines)
            if not (MIN_LEN <= len(state) <= MAX_LEN):
                stats["length"] += 1
                continue
            state_count[norm(state)] += 1
            # "none of these" variant: swap the gold domain for an unrelated one
            none_opts, sub = None, None
            bad = group_of(gdom)
            if not any(dm in bad for dm in other_doms):
                other_opts = [o for dm in other_doms for o in domain_intents(dm, d["services"])]
                other_names = {n for n, _ in other_opts}
                elig = [dm for dm in all_domains
                        if dm not in doms and dm not in bad
                        and not ({n for n, _ in domain_intents(dm, [])} & (other_names | {intent}))]
                if elig:
                    k = len(gold_dom_intents)
                    best = min(abs(len(domain_intents(dm, [])) - k) for dm in elig)
                    elig = [dm for dm in elig if abs(len(domain_intents(dm, [])) - k) == best]
                    sub = random.Random(hkey("sub", sid)).choice(elig)
                    none_opts = domain_intents(sub, []) + other_opts
                    if len(none_opts) < 3:
                        none_opts, sub = None, None
            cands[s + "/" + intent].append({
                "dialogue_id": d["dialogue_id"], "turn": ti, "sid": sid, "service": s,
                "intent": intent, "services": d["services"], "how": how,
                "pos_opts": pos_opts, "none_opts": none_opts, "sub_domain": sub,
                "state": state, "first_turn": ti == 0})
    # drop states that occur more than once in the pool (dedup on normalized text)
    for k in list(cands):
        before = len(cands[k])
        cands[k] = [c for c in cands[k] if state_count[norm(c["state"])] == 1]
        stats["dup_state"] += before - len(cands[k])
    n_none = round(N_SGD * NONE_FRAC)
    used = set()
    picked = [(c, it, False) for c, it in
              rr_sample(cands, N_SGD - n_none, rng, id_fn=lambda c: c["sid"],
                        key_fn=lambda c: c["dialogue_id"], used=used)]
    none_pools = {k: [c for c in v if c["none_opts"]] for k, v in cands.items()}
    picked += [(c, it, True) for c, it in
               rr_sample(none_pools, n_none, rng, id_fn=lambda c: c["sid"],
                         key_fn=lambda c: c["dialogue_id"], used=used)]
    picked.sort(key=lambda x: hkey("order", x[1]["sid"]))
    rows = []
    for cls, c, is_none in picked:
        opts = list(c["none_opts"] if is_none else c["pos_opts"])
        random.Random(hkey("opts", c["sid"])).shuffle(opts)
        names = [n for n, _ in opts]
        assert len(names) == len(set(names))
        assert (c["intent"] in names) != is_none
        rows.append({
            "source": "sgd",
            "_gid": "sgd:" + c["dialogue_id"],
            "state": c["state"],
            "qtype": "choice",
            "instructions": "Which intent does the user's last message start? "
                            "If no listed intent fits, answer \"none of these\".",
            "options": names + [NONE_OPT],
            "gold": NONE_OPT if is_none else c["intent"],
            "role": "choice",
            "card": "\n".join("- %s: %s" % (n, desc) for n, desc in opts),
            "meta": {"license": "cc-by-sa-4.0",
                     "hf_id": "google-research-datasets/schema_guided_dstc8",
                     "data_from": "github.com/google-research-datasets/dstc8-schema-guided-dialogue (HF copy is script-only)",
                     "split_used": "test",
                     "source_id": c["sid"],
                     "source_gold_intent": c["intent"],
                     "gold_service": c["service"], "dialogue_services": c["services"],
                     "service_unseen_in_train": True, "first_turn": c["first_turn"],
                     "intent_start_act": c["how"],
                     "option_scope": ("gold domain replaced by unrelated domain '%s' + the "
                                      "dialogue's other domains" % c["sub_domain"]) if is_none
                                     else "all test-schema services of the dialogue's domains",
                     "none_row": is_none,
                     "concept_note": "label names/descriptions unseen in our training; some "
                                     "intent concepts overlap CLINC150/MASSIVE labels"},
        })
    info = {"unseen_test_services": unseen,
            "n_none_rows": sum(1 for *_, x in picked if x),
            "candidates_per_class": {k: len(v) for k, v in sorted(cands.items())},
            "none_eligible_per_class": {k: len(v) for k, v in sorted(none_pools.items())},
            "counts": dict(stats)}
    return rows, info


def main():
    ver = verify_goemo_definitions()
    print("GoEmotions definitions:", ver)
    g_rows, g_info = build_goemo(random.Random(SEED))
    s_rows, s_info = build_sgd(random.Random(SEED))
    rows = g_rows + s_rows
    # global dedup on normalized state text
    seen = set()
    for r in rows:
        k = norm(r["state"])
        assert k not in seen, r["state"][:80]
        seen.add(k)
    out = []
    for n, r in enumerate(rows):
        gid = r.pop("_gid")
        assert r["gold"] in r["options"]
        assert len(r["options"]) == len(set(r["options"])) <= 255
        out.append({
            "id": "r_ohs_%s_%04d" % (PART, n),
            "group_id": "g:ohs:%s:%s" % (PART, gid),
            "call_id": "c_ohs_%s_%04d" % (PART, n),
            "split": "ohs",
            "track": "U",
            **r,
        })
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    summ = {}
    for src, rs, info in (("go_emotions", g_rows, g_info), ("sgd", s_rows, s_info)):
        c = check_share([r["gold"] for r in rs], src)
        nopt = collections.Counter(len(r["options"]) for r in rs)
        summ[src] = {"n": len(rs), "n_options": dict(sorted(nopt.items())),
                     "max_class_share": round(c.most_common(1)[0][1] / len(rs), 3),
                     "class_balance": dict(sorted(c.items())), **info}
    summ["sgd"]["first_turn_items"] = sum(r["meta"]["first_turn"] for r in s_rows)
    summ["sgd"]["intent_start_act"] = dict(collections.Counter(
        r["meta"]["intent_start_act"] for r in s_rows))
    summ["sgd"]["gold_position"] = dict(sorted(collections.Counter(
        r["options"].index(r["gold"]) for r in s_rows).items()))
    summ["goemo_definitions_check"] = ver
    summ["out"] = OUT
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    sys.exit(main())
