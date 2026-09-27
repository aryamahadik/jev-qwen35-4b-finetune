"""Build raw rows for breadth set "topv2" (TOPv2, Task Oriented Parsing v2; Chen et al., EMNLP 2020).

Source   : official release https://dl.fbaipublicfiles.com/topv2/TOPv2_Dataset.zip (V1.1, 03/10/2021;
           zip sha256 e73a13eb32f67f69c630abde549fa153f288564e2703b71492f04cb59b2cae13).
           Only <domain>_train.tsv, LICENSE and README were extracted into breadth_src/cache/topv2/ (sha256 pinned
           below); the *_eval.tsv, *_test.tsv and low_resource_splits files are never extracted or read.
Licence  : CC BY-SA 4.0. README: "Provided under the CC-BY-SA license."; LICENSE file in the official zip is the
           full "Attribution-ShareAlike 4.0 International" legal code.
Provenance: crowd-written utterances (human) annotated with intent/slot parses by trained human annotators
           (TOP, Gupta et al. 2018; TOPv2 domains collected the same way). No model involvement.

Task     : per-domain intent choice. Gold = the top-level IN:* label of the semantic parse.
           Options = all intents of that domain (so sibling intents such as SNOOZE vs SILENCE alarm, ESTIMATED
           ARRIVAL vs DEPARTURE vs DURATION, RESUME vs RESTART timer, REPLAY vs PREVIOUS TRACK vs LOOP are in the
           option list as natural distractors), mapped to readable names.
Dropped  : the whole event domain (after removing UNSUPPORTED it is ~99.9% GET_EVENT: no decision to make);
           all IN:UNSUPPORTED_* labels (they mean "outside the system's ontology", which a reader cannot infer
           from the text and whose rows overlap supported intents, e.g. "silence alarm" as UNSUPPORTED_ALARM);
           intents with < 20 source train rows (SEND_TEXT_MESSAGE, event sub-intents). CANCEL_MESSAGE (30 source rows,
           17 after dedup) is kept with a warning.
Defs     : rewritten after reading source rows (verifier): TOPv2 labels "stop/turn off timer" as PAUSE, "turn off/
           disable/skip alarm" as SILENCE, "repeat the last song" as PREVIOUS (vs REPLAY = this song) and most
           REMOVE_FROM_PLAYLIST rows are "don't play this song / no rap music" (renamed "Remove or block music").
Filters  : utterance 15-4,000 chars; dedup on normalised text within and across domains (texts occurring with
           different domain/intent are dropped); exact-state match and 13-word-run decontamination against our
           data/*.jsonl (never ohs*) and JevBench public files.
Sampling : round-robin over all (domain, intent) labels in a seeded order, at most 700 rows.
Deterministic, seed 20261101.

  .venv/bin/python breadth_src/build_topv2.py
"""
import collections
import glob
import hashlib
import json
import random
import re
import statistics
from pathlib import Path

SEED = 20261101
KEY = "topv2"
MAX_ROWS = 700
MIN_LABEL_ROWS = 20
ZIP_URL = "https://dl.fbaipublicfiles.com/topv2/TOPv2_Dataset.zip"
ZIP_SHA = "e73a13eb32f67f69c630abde549fa153f288564e2703b71492f04cb59b2cae13"
REVISION = f"TOPv2_Dataset.zip V1.1 (2021-03-10) sha256:{ZIP_SHA}"
LICENCE = ("CC BY-SA 4.0 (TOPv2_Dataset.zip README: 'Provided under the CC-BY-SA license.'; LICENSE file: "
           "'Attribution-ShareAlike 4.0 International')")
SHA = {
    "LICENSE": "3b2890eacd851373001c4a14623458e3adaf1b1967939aa9c38a318e28d61c00",
    "README": "5f050132aee99d4901793f9a9a47bc37aa7d68266b44f5c41f0eedbb94da62ff",
    "alarm_train.tsv": "920483ba7ae051f95f69692deb77c80e66a105005ed5e49a3a043e9ffd155db5",
    "messaging_train.tsv": "1f23f321ce36884d05931ca78eeb0823aaae13047d8099ba68e32e8656c2cf02",
    "music_train.tsv": "0abb87d11edc98d4be9b20879ec892d3fdcb0cd8d2bf4da06eef5e997c578d3c",
    "navigation_train.tsv": "b486903314e4d2f011eeeef95f31f1eccdd8bf7aa538a2b003a23f9dd44b0b5a",
    "reminder_train.tsv": "689f0934456b9b85d8d0d256425b86362f2bd349756d531a71958edd1b6e6ac1",
    "timer_train.tsv": "d630abdde12cade9230434714f3f2f0ca8f75c8c00a6b6a5f5dfeb3100cf996f",
    "weather_train.tsv": "fd683b775602ec88d3fc7ca442c060ff33aacb710eaed3e517c8691835ae1018",
}

HERE = Path(__file__).resolve().parent
LEAN = HERE.parent
CACHE = HERE / "cache" / KEY
OUT = LEAN / "data/v13_parts/raw" / f"{KEY}.jsonl"
DEFS = LEAN / "data/v13_parts/defs" / f"{KEY}.json"
JB = LEAN.parents[1] / "bench/jevbench/datasets/public"

QUESTION = {
    "alarm": "What does the user want to do with their alarms?",
    "messaging": "What does the user want to do with messages?",
    "music": "What does the user want the music player to do?",
    "navigation": "What is the user asking for about travel or routes?",
    "reminder": "What does the user want to do with their reminders?",
    "timer": "What does the user want to do with their timer?",
    "weather": "What is the user asking about the weather or sky?",
}

# domain -> {IN code: (option name, definition)}
LABELS = {
    "alarm": {
        "CREATE_ALARM": ("Set a new alarm", "The user asks to create or schedule a new alarm, possibly with a time, date or recurrence, e.g. 'wake me up at 6 tomorrow'."),
        "GET_ALARM": ("Check existing alarms", "The user asks for information about alarms already set: which alarms exist, when one goes off, or how long until it rings."),
        "DELETE_ALARM": ("Delete an alarm", "The user asks to cancel, delete or remove one or more existing alarms so they no longer exist; merely turning an alarm off is silencing it."),
        "UPDATE_ALARM": ("Change an alarm", "The user asks to modify an existing alarm, such as moving it to another time, adding minutes to it, changing its days or making it repeat."),
        "SILENCE_ALARM": ("Silence or turn off an alarm", "The user asks to turn off, stop, disable, dismiss or skip an alarm, ringing or upcoming, without deleting it and without snoozing it."),
        "SNOOZE_ALARM": ("Snooze an alarm", "The user asks to snooze an alarm, postponing its ring for a short period so it sounds again later."),
    },
    "messaging": {
        "SEND_MESSAGE": ("Send a message", "The user asks to write and send a text, voice or video message to one or more people or groups."),
        "GET_MESSAGE": ("Read or check messages", "The user asks to read, show or find messages, or asks whether a message was sent or received."),
        "REACT_MESSAGE": ("React to a message", "The user asks to put a reaction on an existing message, such as a like, heart, laugh or sad face."),
        "IGNORE_MESSAGE": ("Ignore a message", "The user asks to ignore a message they received: not reply to it, not have it read out, or disregard the notification."),
        "CANCEL_MESSAGE": ("Cancel a message", "The user asks to cancel, stop or quit a message they are sending or composing, so it is not sent."),
    },
    "music": {
        "PLAY_MUSIC": ("Play music", "The user asks to start playing music: a song, artist, album, genre, playlist or radio station."),
        "SKIP_TRACK_MUSIC": ("Skip to the next track", "The user asks to skip the current song and move forward to the next or a later track."),
        "REPLAY_MUSIC": ("Replay the current track", "The user asks to play this current song, album or playlist again from the beginning; asking for the last or previous song again is going back instead."),
        "PREVIOUS_TRACK_MUSIC": ("Go back to the previous track", "The user asks to go back to or hear again the last or previous song, album or station, the one before the current one, e.g. 'repeat the last song'."),
        "PAUSE_MUSIC": ("Pause the music", "The user asks to pause playback temporarily so it can be resumed from the same point."),
        "STOP_MUSIC": ("Stop the music", "The user asks to stop or turn off the music or station entirely, ending playback."),
        "REMOVE_FROM_PLAYLIST_MUSIC": ("Remove or block music", "The user asks to remove a song, artist or genre from a playlist or from what gets played, e.g. 'don't play this song again' or 'no rap music'."),
        "START_SHUFFLE_MUSIC": ("Shuffle music", "The user asks to play songs, an album, artist or playlist in random shuffled order."),
        "CREATE_PLAYLIST_MUSIC": ("Create a playlist", "The user asks to make a new playlist, optionally naming it or saying which songs to put in it."),
        "ADD_TO_PLAYLIST_MUSIC": ("Add to a playlist", "The user asks to add a song, artist or album to an existing playlist."),
        "LOOP_MUSIC": ("Loop the music", "The user asks to put a song, album or playlist on continuous repeat, or to keep playing it, so it loops rather than playing once more."),
        "LIKE_MUSIC": ("Like the music", "The user approves of a song, artist or channel so it is marked as liked: a thumbs up, favouriting it, or saving it to their library."),
        "DISLIKE_MUSIC": ("Dislike the music", "The user rates a song or artist negatively, such as a thumbs down or saying they do not like it, so it is marked as disliked."),
    },
    "navigation": {
        "GET_INFO_TRAFFIC": ("Traffic information", "The user asks about traffic conditions, such as congestion, jams, accidents, delays or closures on a road or route."),
        "GET_ESTIMATED_DURATION": ("Travel time", "The user asks how long a trip will take, i.e. the expected duration of travel between places."),
        "GET_DIRECTIONS": ("Directions or route", "The user asks for directions or the best or fastest route to get somewhere, possibly by a travel mode."),
        "GET_DISTANCE": ("Distance", "The user asks how far it is between two places, in miles, kilometres or similar."),
        "GET_ESTIMATED_ARRIVAL": ("Arrival time", "The user asks when they will arrive, or whether leaving at some time gets them there by a deadline."),
        "GET_ESTIMATED_DEPARTURE": ("Departure time", "The user asks when they need to leave in order to arrive somewhere at a given time."),
        "GET_INFO_ROAD_CONDITION": ("Road conditions", "The user asks about the physical state of roads, e.g. flooding, ice, snow, construction damage or obstructions."),
        "UPDATE_DIRECTIONS": ("Change or reroute directions", "The user asks to change the current route, e.g. for a detour, alternate route or avoiding something ahead."),
        "GET_LOCATION": ("Find a place", "The user asks to find or locate a place, such as the nearest gas station, store or stop, or their own current location, not features along a route."),
        "GET_INFO_ROUTE": ("Route features", "The user asks what is on or along a route or road, such as tolls, detours, rail crossings, bike lanes, gas stations or attractions along the way."),
    },
    "reminder": {
        "CREATE_REMINDER": ("Create a reminder", "The user asks to set a new reminder for themselves or others about a task or event, often with a time."),
        "DELETE_REMINDER": ("Delete a reminder", "The user asks to cancel, delete or remove one or more existing reminders."),
        "GET_REMINDER": ("Look up reminders", "The user asks to see or check which reminders exist, for a time period, person or topic."),
        "UPDATE_REMINDER_DATE_TIME": ("Change a reminder's time", "The user asks to move an existing reminder to a different date or time."),
        "GET_REMINDER_DATE_TIME": ("Ask when a reminder is", "The user asks for the date or time at which a particular existing reminder is set."),
        "UPDATE_REMINDER": ("Change a reminder in general", "The user asks to edit an existing reminder in a way that is not only a new time or only a new task, e.g. its recurrence, who it is for, or unspecified changes."),
        "UPDATE_REMINDER_TODO": ("Change a reminder's task", "The user asks to change what an existing reminder is about, replacing or adding the item, task or activity it names, e.g. adding an item to a list reminder."),
        "GET_REMINDER_LOCATION": ("Ask where a reminder is", "The user asks for the place or address attached to a reminder or its event."),
        "GET_REMINDER_AMOUNT": ("Count reminders", "The user asks how many reminders they have, overall or for a period or topic."),
        "HELP_REMINDER": ("Get help with reminders", "The user asks how to use the reminder feature or for guidance on doing something with reminders."),
    },
    "timer": {
        "CREATE_TIMER": ("Start a new timer", "The user asks to set or start a new countdown timer for some duration, often for a named activity."),
        "GET_TIMER": ("Check a timer", "The user asks about an existing timer, such as how much time is left or how long it has run."),
        "PAUSE_TIMER": ("Pause a timer", "The user asks to pause, hold, stop or turn off a running timer so it stops counting, without cancelling, ending or deleting it."),
        "ADD_TIME_TIMER": ("Add time to a timer", "The user asks to extend a running timer by adding extra minutes or seconds to it."),
        "DELETE_TIMER": ("Cancel a timer", "The user asks to cancel, end, clear, delete or remove a timer entirely; merely stopping a running timer is pausing it."),
        "RESUME_TIMER": ("Resume a timer", "The user asks to continue a paused timer from where it stopped."),
        "RESTART_TIMER": ("Restart a timer", "The user asks to restart or reset a timer so it counts again from its beginning or from a new starting value."),
        "UPDATE_TIMER": ("Change a timer's settings", "The user asks to change or edit an existing timer, usually setting it to a different total duration or start, rather than adding or removing time."),
        "SUBTRACT_TIME_TIMER": ("Take time off a timer", "The user asks to shorten a running timer by removing some minutes or seconds from it."),
    },
    "weather": {
        "GET_WEATHER": ("Weather conditions or forecast", "The user asks about current or forecast weather, such as temperature, rain, snow, wind or humidity somewhere."),
        "GET_SUNSET": ("Sunset time", "The user asks when the sun will set, or about sunset, on some day or at some place."),
        "GET_SUNRISE": ("Sunrise time", "The user asks when the sun will rise, or about sunrise, on some day or at some place."),
    },
}

TOP = re.compile(r"^\[IN:([A-Z_]+)\s")
words = lambda t: re.sub(r"[^a-z0-9]+", " ", t.lower()).split()
norm = lambda t: " ".join(words(t))


def check_cache():
    for name, sha in SHA.items():
        p = CACHE / name
        assert p.exists(), (f"missing {p}: download {ZIP_URL} (sha256 {ZIP_SHA}) and extract only "
                            "LICENSE, README and the <domain>_train.tsv files into breadth_src/cache/topv2/")
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        assert h == sha, f"{name} sha256 mismatch {h}"
    assert not list(CACHE.glob("*_test.tsv")) and not list(CACHE.glob("*_eval.tsv")), "test/eval files in cache"


def load():
    """Return ({norm: rec}, stats). rec = {rid, text, domain, code}."""
    recs, bad, st = {}, set(), collections.Counter()
    for dom in LABELS:
        with open(CACHE / f"{dom}_train.tsv", encoding="utf-8", newline="") as fh:
            for ln, line in enumerate(fh, 1):
                if ln == 1:
                    continue
                d, utt, parse = line.rstrip("\r\n").split("\t")
                assert d == dom
                m = TOP.match(parse)
                st["source_rows"] += 1
                if not m:
                    st["drop_no_top_intent"] += 1
                    continue
                code = m.group(1)
                if code not in LABELS[dom]:
                    st["drop_label_not_used"] += 1
                    continue
                utt = utt.strip()
                if not (15 <= len(utt) <= 4000) or len(words(utt)) < 2:
                    st["drop_length"] += 1
                    continue
                k = norm(utt)
                if k in bad:
                    st["drop_conflict"] += 1
                    continue
                if k in recs:
                    if (recs[k]["domain"], recs[k]["code"]) != (dom, code):
                        bad.add(k)
                        del recs[k]
                        st["drop_conflict"] += 2
                    else:
                        st["drop_duplicate"] += 1
                    continue
                recs[k] = {"rid": f"{dom}_train.tsv:{ln}", "text": utt, "domain": dom, "code": code}
    return recs, st


def contam(recs, n=13):
    """Norm keys equal to a state in, or sharing a 13-word run with, our data/*.jsonl (not ohs*) or JevBench."""
    grams = collections.defaultdict(set)
    for k in recs:
        w = k.split()
        for i in range(len(w) - n + 1):
            grams[" ".join(w[i:i + n])].add(k)
    files = sorted(f for f in glob.glob(str(LEAN / "data" / "*.jsonl")) if not Path(f).name.startswith("ohs"))
    files += sorted(glob.glob(str(JB / "*.jsonl")))
    hit = set()
    for f in files:
        with open(f, encoding="utf-8") as fh:
            for line in fh:
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                st = r.get("state") if isinstance(r, dict) else None
                if isinstance(st, str) and norm(st) in recs:
                    hit.add(norm(st))
                if grams:
                    w = words(line.replace("\\n", " "))
                    for i in range(len(w) - n + 1):
                        g = " ".join(w[i:i + n])
                        if g in grams:
                            hit |= grams[g]
    return hit, len(files)


def main():
    check_cache()
    rng = random.Random(SEED)
    recs, st = load()
    hit, nfiles = contam(recs)
    for k in hit:
        recs.pop(k, None)
    st["drop_decontam"] = len(hit)

    pools = collections.defaultdict(list)
    for k in sorted(recs):
        r = recs[k]
        pools[(r["domain"], r["code"])].append(r)
    labels = []
    for dom, m in LABELS.items():
        for code in m:
            if len(pools[(dom, code)]) < MIN_LABEL_ROWS:
                print(f"WARNING: {dom}/{code} has only {len(pools[(dom, code)])} eligible rows")
            labels.append((dom, code))
    for lab in labels:
        rng.shuffle(pools[lab])
    order = labels[:]
    rng.shuffle(order)

    rows, idx = [], collections.Counter()
    while len(rows) < MAX_ROWS:
        added = False
        for lab in order:
            if len(rows) >= MAX_ROWS:
                break
            if idx[lab] < len(pools[lab]):
                r = pools[lab][idx[lab]]
                idx[lab] += 1
                added = True
                dom, code = lab
                opts = [v[0] for v in LABELS[dom].values()]
                rows.append({
                    "key": KEY, "rid": r["rid"], "state": r["text"], "instructions": QUESTION[dom],
                    "options": opts, "gold": LABELS[dom][code][0], "soft": None,
                    "meta": {"dataset": "TOPv2 (Task Oriented Parsing v2, Chen et al. 2020)", "config": dom,
                             "revision": REVISION, "licence": LICENCE, "split": "train",
                             "orig_label": f"IN:{code}"}})
        if not added:
            break
    rng.shuffle(rows)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    DEFS.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    defs = {}
    for m in LABELS.values():
        for name, d in m.values():
            assert name not in defs or defs[name] == d, f"option name clash: {name}"
            n = len(d.split())
            assert 8 <= n <= 35, (name, n)
            defs[name] = d
    DEFS.write_text(json.dumps(defs, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # report
    print(f"stats: {dict(st)}; eligible after filters: {len(recs)}; decontam scanned {nfiles} files")
    print(f"wrote {len(rows)} rows -> {OUT}")
    by_dom = collections.Counter(r["meta"]["config"] for r in rows)
    print("per domain:", dict(by_dom))
    lab_c = collections.Counter((r["meta"]["config"], r["gold"]) for r in rows)
    for (dom, g), c in sorted(lab_c.items()):
        print(f"  {dom:10s} {g:34s} {c:3d}  ({c / by_dom[dom]:.0%} of domain)")
    print(f"max share of one label within its domain: {max(c / by_dom[d] for (d, _), c in lab_c.items()):.0%}")
    print(f"soft-label coverage: {sum(r['soft'] is not None for r in rows)}/{len(rows)}")
    L = [len(r["state"]) for r in rows]
    print(f"state length chars: min {min(L)} median {statistics.median(L)} mean {statistics.mean(L):.1f} max {max(L)}")
    print(f"defs: {len(defs)} -> {DEFS}")


if __name__ == "__main__":
    main()
