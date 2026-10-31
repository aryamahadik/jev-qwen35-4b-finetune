"""Build raw rows for smcalflow_action: how should a calendar assistant handle the user's latest turn?

Source : SMCalFlow 2.0 (Semantic Machines / Microsoft; Andreas et al., TACL 2020), GitHub
         microsoft/task_oriented_dialogue_as_dataflow_synthesis, datasets/SMCalFlow-2.0/train.dataflow_dialogues.jsonl.zip,
         pinned at commit COMMIT (sha256 below). TRAIN file only; valid is never downloaded; there is no public test.
Licence: CC BY-SA 4.0 for the dataset ("The dataset is distributed under the CC BY-SA 4.0 license", README.md at COMMIT,
         step 1 of the reproduction instructions); the repo code is MIT.
Texts  : crowd-written user turns (human-human Wizard-of-Oz collection, 2019); agent turns are the human-authored
         agent responses shipped with the data. No LLM text.
Labels : the program (lispress) that trained annotators wrote for each user turn. The decision label is read off the
         program's top-level action: create / update / delete an event, answer a calendar / weather / place / org-chart /
         date question, accept / revise / reject the pending proposal, respond to an invitation, small talk, pause, or
         one of the "Fence*" refusals (the annotator's reason why the assistant cannot do it). Programs that combine
         several yields ("do"), NewClobber / refer re-runs, FenceOther (catch-all), FenceSwitchTabs (mixed messages),
         FenceTeams / FenceComparison (< 10 rows) and turns tagged "do-not-train" are dropped.
State  : up to the two previous exchanges (User / Assistant) plus the latest user turn. The assistant's reply to the
         latest turn is never shown (it reveals the label).
Review : (strict review) the three Pleasantry* programs are merged into one option (annotators did not separate
         greetings from thanks consistently), and rows whose latest message also carries a cue for a competing option
         are dropped, never relabelled (consistent(): pleasantry without a task word or pending proposal; scope requests
         without reminder / travel / place / people / weather cues; trivia not naming a supported holiday or a relative
         date; travel with a travel cue; aggregations that are not bulk deletions).
Rows   : at most one row per dialogue and one row per normalised latest-user text; labels balanced by round-robin with
         a per-label cap (PER_LABEL). Deterministic (seed SEED).
"""
import collections
import json
import random
import re
import zipfile

import _rd_common as C

KEY = "smcalflow_action"
SEED = 20260929
MAX_ROWS = 4500
PER_LABEL = 400
COMMIT = "bbd16fe69687b1052a7b5937ee7d20b641f2e642"
REL = "datasets/SMCalFlow-2.0/train.dataflow_dialogues.jsonl.zip"
URL = f"https://raw.githubusercontent.com/microsoft/task_oriented_dialogue_as_dataflow_synthesis/{COMMIT}/{REL}"
SHA = "2beb5fd51056999051081300aea33fdf228378fa214f915f6167cb4924e23d28"
LICENCE = ("CC BY-SA 4.0 (https://github.com/microsoft/task_oriented_dialogue_as_dataflow_synthesis/blob/" + COMMIT +
           "/README.md: 'The dataset is distributed under the CC BY-SA 4.0 license')")
INSTR = ("How should the calendar assistant handle the user's latest message, given what the assistant can and cannot do?")

# ---- option names and Claude-written definitions (the decision rule the SMCalFlow annotators applied) ----
DEFS = {
    "create a new event": "The user asks to put a new event on their calendar (schedule, add, book, set up a meeting or appointment) and the request is fully supported: one event, named attendees only, no recurrence, no specific conference room.",
    "change an existing event": "The user asks to modify an event that is already on the calendar (reschedule, move, extend, rename, add or remove attendees, change location); not a tweak to an event the assistant has only just proposed and not yet saved.",
    "delete an event": "The user asks to cancel, remove or delete one specific event already on the calendar.",
    "answer a question about the calendar": "The user asks what is on their calendar or about an existing event's details (when, where, how long, who is invited, who accepted, whether they are free), answerable by one lookup.",
    "respond to an event invitation": "The user asks to accept, decline or tentatively accept an invitation to an event someone else organised, possibly with a message to the organiser.",
    "accept the pending proposal": "The assistant has just shown a proposed event or change (or several options) and the user approves it or picks one of the options ('yes', 'looks good', 'the second one'), without changing anything.",
    "revise the pending proposal": "The assistant has just shown an unsaved proposed event, change or cancellation and the user alters it (adds a person, changes time, length or place, or says which event was meant) instead of approving or rejecting it.",
    "reject the pending proposal": "The assistant has just shown a proposed event or change and the user refuses it or tells the assistant not to go ahead, without giving a replacement.",
    "answer a weather question": "The user asks a supported weather question: current or forecast conditions, temperature, rain, snow, sun, wind or humidity for a place and time the forecast covers.",
    "answer a question about a place": "The user asks for supported facts about a named business or place: its address, phone number, website, price level, rating, hours or whether it has a feature (full bar, parking, takeout).",
    "answer a question about a person or team": "The user asks about someone in their organisation's directory: who a person is, their manager, direct reports, team, email address, phone number or office location.",
    "answer a date, time or holiday question": "The user asks for today's or a relative date, the day of the week, the current time, or when a common US holiday or observance falls (e.g. Easter, Halloween, Labor Day, Mother's Day, Tax Day, Kwanzaa).",
    "reply with a pleasantry": "The user only greets, thanks or reacts ('hi', 'thanks', 'ok', 'great job'), makes small talk, or asks for help in general without a concrete calendar request; the assistant just replies politely and offers help.",
    "wait for the user": "The user asks the assistant to hold on or wait while they do something ('wait a minute', 'hold on while I call Stacy'); nothing else is requested.",
    "decline: only one action at a time": "The user asks for two or more actions at once, a bulk action over many events ('clear my calendar'), or an action conditioned on a check ('if I'm free, add...'); only one simple action per turn is possible.",
    "decline: attendee is not a named contact": "The request needs the assistant to identify people who are not given by name in the address book ('my friends', 'coworkers', 'my dad', 'a bank teller'); the assistant can only look up named contacts.",
    "decline: outside the assistant's scope": "The user asks for a service unrelated to calendars, weather, places or the org chart (booking flights or tickets, ordering or buying things, messaging or phoning people, banking, playing music), so the assistant says it can only help with the calendar.",
    "decline: unsupported weather question": "The user asks about weather in a way the forecast cannot answer: explanations ('why do hurricanes happen'), opinions, or open-ended predictions such as when the rain will stop or the next 80-degree day.",
    "ask the user to be more specific": "The user wants something done but leaves out what exactly: which event, or the new time or value ('change dinner time', 'update my Monday meeting'), or sends a fragment that cannot be acted on alone ('select one', 'place it').",
    "decline: reminders and alarms": "The user asks the assistant to set a reminder, alarm or notification (for themselves or others); the assistant cannot do reminders, even when the rest of the request is fine.",
    "decline: message not understandable": "The message is gibberish, random characters, pasted instructions, or a statement with no recognisable request the assistant could act on.",
    "decline: unsupported question about people": "The user asks for personal information the directory does not hold (home address, whether someone is online, someone else's schedule) or about people outside the directory.",
    "decline: recurring events": "The user asks to create or change a recurring or repeated series of events ('every Tuesday', 'the next 3 Saturdays', 'do that on the 18th too'); the assistant cannot schedule recurrences.",
    "decline: unsupported date or time range": "The calendar request uses a time reference the assistant cannot resolve: past periods ('last weekend', 'three weeks ago'), multi-day spans ('all next week', 'for 4 days'), two alternative days, 'the first Saturday in July', or vague parts ('middle of next week').",
    "decline: general-knowledge question": "The user asks a trivia or general-knowledge question (facts, science, maths, seasons, which holidays fall in a period, 'the next holiday', a holiday outside the common US list such as Purim) rather than a calendar fact.",
    "decline: calculations over the calendar": "The user asks for counts, comparisons or aggregates across many events ('how many meetings this week', 'my longest meeting', 'how many free days next month'); the assistant cannot compute them.",
    "decline: specific conference rooms": "The user asks to book or include a specific conference or meeting room ('in Conference Room A'); the assistant cannot book rooms.",
    "decline: directions and travel": "The user asks for directions, routes, traffic, travel time or when to leave to get somewhere; the assistant cannot answer transit questions.",
    "decline: unsupported question about a place": "The user asks about a place something the place lookup does not cover: menus, reservations, crowds, opening today, specific products, or the nearest branch.",
}

FENCE = {
    "FenceMultiAction": "decline: only one action at a time",
    "FenceConditional": "decline: only one action at a time",
    "FenceAttendee": "decline: attendee is not a named contact",
    "FenceScope": "decline: outside the assistant's scope",
    "FenceWeather": "decline: unsupported weather question",
    "FenceSpecify": "ask the user to be more specific",
    "FenceReminder": "decline: reminders and alarms",
    "FenceGibberish": "decline: message not understandable",
    "FencePeopleQa": "decline: unsupported question about people",
    "FenceRecurring": "decline: recurring events",
    "FenceDateTime": "decline: unsupported date or time range",
    "FenceTriviaQa": "decline: general-knowledge question",
    "FenceAggregation": "decline: calculations over the calendar",
    "FenceConferenceRoom": "decline: specific conference rooms",
    "FenceNavigation": "decline: directions and travel",
    "FencePlaces": "decline: unsupported question about a place",
}
TOP = {
    "DoNotConfirm": "reject the pending proposal",
    "UserPauseResponse": "wait for the user",
    "PleasantryAnythingElseCombined": "reply with a pleasantry",
    "GenericPleasantry": "reply with a pleasantry",
    "PleasantryCalendar": "reply with a pleasantry",
}
ACCEPT = ("ChooseCreateEvent", "ChooseCreateEventFromConstraint", "ChooseUpdateEvent", "ChooseUpdateEventFromConstraint",
          "ConfirmCreateAndReturnAction", "ConfirmDeleteAndReturnAction", "^(Dynamic) ConfirmAndReturnAction",
          "ConfirmAndReturnAction")
WEATHER = ("WeatherQueryApi", "WeatherAggregate", "WillRain", "WillSnow", "IsSunny", "IsRainy", "IsCloudy", "IsHot",
           "IsCold", "IsWindy", "IsHighUV", "IsStormy", "IsSnowy", "WeatherForEvent", "WeatherPleasantry")
PLACE = ("PlaceHasFeature", "Place.", "FindPlaceMultiResults", "FindPlace ", "PlaceSearchResponse")
PERSON = ("FindManager", "FindReports", "FindTeamOf", "PersonFromRecipient", "Person.")
DATETIME = ("NextHolidayFromToday", "HolidayYear", "(Tomorrow)", "(Today)", "(Now)", "Date.dayOfWeek", "(Yesterday)",
            "Holiday")
PROPOSAL = re.compile(r"(Is this good\?|Does one of these work\?|Is this what you want me to cancel\?|How's this\?|"
                      r"How is this\?|Is this what you're looking for\?|Does this look right\?|"
                      r"Is this the change you want to make\?|Is this the update you want\?|How about now\?|Is that ok\?|"
                      r"Is this the event you want me to decline\?|Here are some times when .{0,80}free)")
PENDING = ("accept the pending proposal", "revise the pending proposal", "reject the pending proposal")
CALENDAR = ("FindEventWrapperWithDefaults", "QueryEventResponse", "Event.", "FindNumNextEvent", "FindLastEvent", "IsFree",
            "AttendeesWith", "ResponseStatus", "AttendeeListHasRecipient", "RecipientAvailability", "EventOnDate",
            "EventDuring")


# Review fix (strict review, round 2): the annotators' Pleasantry* / Fence* choices are noisy near the other options'
# boundaries, so rows whose latest message carries a cue for a competing option are dropped (never relabelled):
PLEAS = re.compile(r"\b(hi|hello|hey|hiya|howdy|good (morning|afternoon|evening|night|job|work)|thanks?|thank you|thx|ty|"
                   r"ok(ay)?|cool|great|good|perfect|awesome|nice|alright|all right|fine|bye|goodbye|see you|help|"
                   r"wonderful|excellent|super|superb|well done|appreciate\w*|sure|no problem|that'?s (all|it)|none|nothing|"
                   r"nope|how are you|what can you do|got it|sounds good|lovely|amazing|fantastic|wow|welcome)\b", re.I)
TASKW = re.compile(r"\b(cancel|delete|remove|add|schedule|create|make|move|change|update|book|remind\w*|meetings?|events?|"
                   r"appointments?|invite|weather|when|where|who|what time)\b", re.I)
NAVW = re.compile(r"(direction|route|traffic|drive|driving|get (there|to|from|home|back)|commute|how (long|far|soon)|"
                  r"travel|leave|walk|\bbus\b|transit|\bmap\b|miles|distance|uber|lyft|taxi|\bcab\b)", re.I)
SCOPE_REQ = re.compile(r"\b(book|order|buy|purchase|text|message|e-?mail|call|phone|inform|tell|let \w+ know|send|play|"
                       r"search|find|look up|google|price|pay|transfer|reserve|reservation|tickets?|flights?|trains?|hotels?|"
                       r"shop\w*|news|music|songs?|balance|account|bank)\b", re.I)
SCOPE_OTHER = re.compile(r"\b(timers?|alarms?|remind\w*|notif\w*|prior to|conference rooms?|weather|rain\w*|snow\w*|"
                         r"temperature|holidays?|restaurants?|nearby|near me|address|hours|open|places? to|when was|last time|"
                         r"my (dad|mom|mother|father|wife|husband|friends?|family|son|daughter|boss|brother|sister|kids?|doctor)|"
                         r"teams?|coworkers?|help|home|numbers?)\b", re.I)
TRIVIA_OTHER = re.compile(r"\b(what (day|date|time) is it|(date|day) after|today|tomorrow|tonight|yesterday|this week|"
                          r"next week|calendar|am i|do i|did i|my|me)\b", re.I)
HOLIDAYS = re.compile(r"(halloween|easter|valentine|thanksgiving|labou?r day|memorial day|mother'?s day|father'?s day|"
                      r"independence day|fourth of july|4th of july|st\.? patrick|saint patrick|flag day|\bmlk\b|"
                      r"martin luther king|black friday|veteran'?s'? day|president'?s'? day|earth day|tax day|kwanzaa|"
                      r"good friday|new year|groundhog|april fool|ash wednesday|election day|palm sunday|mardi gras|"
                      r"columbus day|patriot day|christmas)", re.I)


def consistent(lab, utt, ctx):
    """False when the latest message also fits a competing option's definition (row dropped, label never changed)."""
    if lab == "reply with a pleasantry":
        last = ctx[-1] if ctx else ""
        return bool(PLEAS.search(utt)) and not TASKW.search(utt) and not (last.startswith("Assistant: ")
                                                                           and PROPOSAL.search(last))
    if lab == "decline: outside the assistant's scope":
        return bool(SCOPE_REQ.search(utt)) and not SCOPE_OTHER.search(utt) and not NAVW.search(utt)
    if lab == "decline: general-knowledge question":
        return not HOLIDAYS.search(utt) and not TRIVIA_OTHER.search(utt)
    if lab == "decline: directions and travel":
        return bool(NAVW.search(utt)) and not re.search(r"\baddress", utt, re.I)
    if lab == "decline: calculations over the calendar":
        return not re.search(r"\b(delete|remove|cancel|clear)\b", utt, re.I)
    return True


def classify(lp):
    """Map an SMCalFlow 2.0 lispress program to one decision option (or None = drop)."""
    head = re.match(r"\(\s*([^\s()]+)", lp)
    head = head.group(1) if head else lp
    if head in FENCE:
        return FENCE[head]
    if head in TOP:
        return TOP[head]
    if head.startswith("Fence") or head.startswith("Pleasantry"):
        return None  # FenceOther / FenceSwitchTabs / FenceTeams / FenceComparison / other pleasantries
    if "(do " in lp:
        return None  # several yields in one turn
    i = lp.find("(Yield ")
    if i < 0:
        return None
    body = lp[i + len("(Yield "):]
    if body.startswith("(Execute "):
        inner = body[len("(Execute "):]
        if inner.startswith("(ReviseConstraint"):
            return "revise the pending proposal"
        if any(inner.startswith("(" + a) for a in ACCEPT):
            return "accept the pending proposal"
        return None  # NewClobber / refer re-runs
    if body.startswith("(CreateCommitEventWrapper"):
        return "create a new event"
    if body.startswith("(UpdateCommitEventWrapper"):
        return "change an existing event"
    if body.startswith("(DeleteCommitEventWrapper"):
        return "delete an event"
    if body.startswith("(EventAttendance") or body.startswith("(ForwardEventWrapper"):
        return "respond to an event invitation" if body.startswith("(EventAttendance") else None
    if any(w in body for w in WEATHER):
        return "answer a weather question"
    if any(w in body for w in PLACE):
        return "answer a question about a place"
    if any(w in body for w in CALENDAR):
        return "answer a question about the calendar"
    if any(w in body for w in PERSON):
        return "answer a question about a person or team"
    if any(w in body for w in DATETIME):
        return "answer a date, time or holiday question"
    return None


EDGE = {
    "decline: only one action at a time": "quantifier",
    "decline: attendee is not a named contact": "exception",
    "decline: recurring events": "exception",
    "decline: specific conference rooms": "exception",
    "decline: reminders and alarms": "exception",
    "decline: calculations over the calendar": "quantifier",
    "decline: unsupported date or time range": "temporal",
    "ask the user to be more specific": "ambiguous",
    "reject the pending proposal": "negation",
    "accept the pending proposal": "implicit",
    "revise the pending proposal": "implicit",
    "decline: unsupported weather question": "exception",
    "decline: unsupported question about a place": "exception",
    "decline: unsupported question about people": "exception",
}


def clean(t):
    return re.sub(r"\s+", " ", (t or "").replace("__BREAK", " ")).strip()


def main():
    zpath = C.CACHE / KEY / "train.dataflow_dialogues.jsonl.zip"
    sha = C.fetch(URL, zpath, SHA)
    assert set(DEFS) >= set(FENCE.values()) | set(TOP.values())
    opts = sorted(DEFS)
    stats = collections.Counter()
    cands = collections.defaultdict(list)  # label -> [(dialogue_id, turn_index, state, utt, program)]
    with zipfile.ZipFile(zpath) as z:
        name = [n for n in z.namelist() if n.endswith("train.dataflow_dialogues.jsonl")][0]
        for line in z.open(name):
            d = json.loads(line)
            turns = d["turns"]
            for t in turns:
                stats["turns"] += 1
                if "do-not-train" in t["tags"]:
                    stats["do_not_train"] += 1
                    continue
                lab = classify(t["lispress"])
                if lab is None:
                    stats["unmapped_or_dropped"] += 1
                    continue
                utt = clean(t["user_utterance"]["original_text"])
                if len(utt) < 2:
                    continue
                k = t["turn_index"]
                prev = [p for p in turns if p["turn_index"] < k][-2:]
                ctx = []
                for p in prev:
                    ctx.append("User: " + clean(p["user_utterance"]["original_text"]))
                    a = clean((p.get("agent_utterance") or {}).get("original_text"))
                    if a:
                        ctx.append("Assistant: " + a)
                if not consistent(lab, utt, ctx):
                    stats["dropped_competing_cue"] += 1
                    continue
                if lab in PENDING:
                    last_agent = [c for c in ctx if c.startswith("Assistant: ")][-1:] if ctx else []
                    if not last_agent or not ctx[-1].startswith("Assistant: ") or not PROPOSAL.search(ctx[-1]):
                        stats["pending_without_visible_proposal"] += 1
                        continue  # the proposal must be the assistant's last turn
                state = ("\n".join(ctx) + "\n" if ctx else "") + "User (latest message): " + utt
                cands[lab].append((d["dialogue_id"], k, state, utt, t["lispress"]))
    rng = random.Random(SEED)
    for lab in sorted(cands):
        cands[lab].sort(key=lambda x: (x[0], x[1]))
        rng.shuffle(cands[lab])
    # one row per dialogue and per normalised latest-user text; rarest labels choose first
    used_dlg, used_utt, rows_by = set(), set(), collections.defaultdict(list)
    for lab in sorted(cands, key=lambda l: (len(cands[l]), l)):
        for did, k, state, utt, lp in cands[lab]:
            if len(rows_by[lab]) >= PER_LABEL:
                break
            nu = C.norm(utt)
            if did in used_dlg or nu in used_utt or not nu:
                continue
            used_dlg.add(did)
            used_utt.add(nu)
            rows_by[lab].append((did, k, state, utt, lp))
    pools = {lab: list(reversed(v)) for lab, v in rows_by.items()}
    picked = C.round_robin(pools, MAX_ROWS)
    picked_by = collections.defaultdict(list)
    for x in picked:
        picked_by[classify(x[4])].append(x)
    rows = []
    for lab in sorted(picked_by):
        for did, k, state, utt, lp in picked_by[lab]:
            edge = EDGE.get(lab)
            if edge is None and state.count("\n") >= 3:
                edge = "long_context" if len(state) > 700 else None
            rows.append({
                "key": KEY, "rid": f"{did}#{k}", "state": state, "instructions": INSTR, "options": opts, "gold": lab,
                "soft": None,
                "meta": {"dataset": "SMCalFlow 2.0 (microsoft/task_oriented_dialogue_as_dataflow_synthesis)",
                         "config": "datasets/SMCalFlow-2.0/train.dataflow_dialogues.jsonl.zip; top-level program action",
                         "revision": f"git:{COMMIT}; sha256:{sha}", "licence": LICENCE, "split": "train",
                         "orig_label": {"lispress": lp[:400]}, "family": C.FAMILY, "edge": edge, "seed": SEED}})
    rows = C.cap_label(rows, lambda r: r["gold"], 0.5)
    rng.shuffle(rows)
    rows = C.near_dedupe(rows)
    out, rows = C.write_rows(rows, KEY)
    C.write_defs({o: DEFS[o] for o in opts}, KEY)
    print(dict(stats))
    print("candidates per label:", {k: len(v) for k, v in sorted(cands.items())})
    print(f"wrote {len(rows)} -> {out}")
    C.report(rows)


if __name__ == "__main__":
    main()
