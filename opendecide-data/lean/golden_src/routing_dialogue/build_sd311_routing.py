"""Build raw rows for sd311_routing: route a resident's City of San Diego "Get It Done" 311 report.

Source : City of San Diego Open Data Portal, dataset "Get It Done Reports" (https://data.sandiego.gov/datasets/get-it-done-311/),
         files get_it_done_requests_closed_2020_datasd.csv and ..._closed_2021_datasd.csv from seshat.datasd.org
         (downloaded 2026-09-29; sha256 pinned below; a changed file stops the build). No split -> train.
Licence: Open Data Commons Public Domain Dedication and License (ODC-PDDL), stated on the dataset page
         (https://data.sandiego.gov/datasets/get-it-done-311/, "License: View License" -> https://opendefinition.org/licenses/odc-pddl/).
Texts  : public_description = "the description submitted by the reporting party" (residents; only case_origin Mobile /
         Web / Phone / Email; worker-app and crew-generated tickets dropped). All reports are from 2020-2021, before LLM
         chat assistants. Machine-translated reports ("Translated: ..."), texts with phone numbers, e-mail addresses or
         URLs, and duplicate child tickets (service_request_parent_id set) are dropped.
Labels : service_name (the request type the ticket was worked under; each maps to one City crew) and, for graffiti,
         the referral recorded by City staff (status Referred + referred-to agency) or the in-house crew. Human choices.
Filter : the labels are noisy (residents pick the category), so a Claude-written cue lexicon is used as a verifier: a
         row is kept only if the text has a cue for its gold option and no cue for any other option of that question.
         The remaining difficulty is in the near-miss pairs (pothole vs pavement, signal outage vs signal timing, public vs
         private graffiti, weeds vs vegetation encroachment vs trees, blocked drain vs polluted runoff vs flooding, ...).
Review : (strict review) cue bugs fixed: "at&?t" matched inside words (Regatta, attached) -> word-bounded AT&T / ATT;
         private cues now match plurals (dumpsters, buildings) but not "city/public property"; "run off" / irrigation
         count as runoff cues; q=service public graffiti needs a positive right-of-way cue (street, sidewalk, sign, pole,
         utility box, ...), and graffiti with both a private cue and another agency's cue is dropped.
Tasks  : q=service (which of 24 request types / crews) and q=graffiti_owner (which crew or agency removes the graffiti;
         utility-box referrals to SDG&E / AT&T / Cox are merged because the owner is not visible from the text). Each
         source record is used once. Per-option cap SERVICE_CAP / OWNER_CAP. Deterministic (seed SEED).
"""
import collections
import csv
import random
import re

import _rd_common as C

KEY = "sd311_routing"
SEED = 20260929
SERVICE_CAP = 125
OWNER_CAP = 190
BASE = "https://seshat.datasd.org/get_it_done_reports/"
FILES = {
    "get_it_done_requests_closed_2020_datasd.csv": None,
    "get_it_done_requests_closed_2021_datasd.csv": None,
}
PIN_FILE = C.HERE / "pins_sd311_routing.json"
LICENCE = ("ODC-PDDL public domain dedication (dataset page https://data.sandiego.gov/datasets/get-it-done-311/ "
           "'License' -> https://opendefinition.org/licenses/odc-pddl/)")
ORIGINS = {"Mobile", "Web", "Phone", "Email"}

GRAFF = r"(graff?itt?i|grafitti|grafiti|\btag(ged|ging|s)?\b|tagger|spray[- ]?paint)"
# review fix: plurals (dumpsters, buildings, ...) and "city/public property" no longer count as private cues
PRIVATE = (r"\b(business|store|shop|building|house|residence|apartment|condo|church|restaurant|market|gas station|"
           r"garage|private|(?<!city )(?<!public )property|properties|warehouse|motel|hotel|office|dumpster|storefront|"
           r"liquor|7-?eleven|laundromat|construction|fence)(e?s)?\b|\b(my|our|his|her|their|a|the) home\b")

# option -> (service_names, cue regex, definition)
SERVICE = {
    "pothole repair": (["Pothole"], r"\bpot ?holes?\b",
        "A distinct hole or pit in the asphalt of a street or alley that needs patching; broad cracking, sinking or worn surfaces go to pavement repair."),
    "pavement repair or resurfacing": (["Pavement Maintenance"],
        r"(resurfac|repav|re-pav|slurry|asphalt|pavement|road surface|street surface|uneven (street|road)|sinking (street|road)|sinkhole|crumbling (street|road)|cracks? in the (street|road))",
        "Street or alley surface that is cracked, crumbling, sunken, uneven or worn and needs asphalt repair or resurfacing, rather than one discrete pothole."),
    "sidewalk repair": (["Sidewalk Repair Issue"],
        r"sidewalk.{0,40}(crack|lift|raised|uneven|broken|trip|heav|buckl|displac|damaged|missing)|(crack|lift|raised|uneven|broken|trip|heav|buckl|displac|damaged).{0,40}sidewalk",
        "Damaged public sidewalk concrete: cracked, lifted, raised by roots, broken or uneven slabs that create a trip hazard; not things blocking the sidewalk."),
    "street light repair": (["Street Light Maintenance"], r"(street ?lights?|streetlights?|light poles?|lamp ?posts?|street lamps?)",
        "A street light that is out, flickering, on during the day, or whose pole is knocked down or damaged; traffic signals are not street lights."),
    "traffic signal malfunction": (["Traffic Signal Issue"],
        r"((traffic|stop) ?(light|signal)s?|\bsignals?\b|ped(estrian)? (push )?(button|signal|head)|walk (sign|signal|light)|crosswalk (signal|light|button)).{0,60}(out\b|not working|flashing|blinking|broken|malfunction|stuck|dark|damaged|knocked|dead|doesn'?t work|isn'?t working|not functioning|no power)",
        "A traffic or pedestrian signal that is out, dark, flashing, stuck, damaged or has a broken push button, i.e. the equipment itself fails."),
    "traffic signal timing": (["Traffic Signal Timing"],
        r"(timing|\btimed\b|too (long|short)|green (light|arrow)|left[- ]turn (arrow|signal|light)|light cycle|signal cycle|never (turns|changes) green|doesn'?t (detect|sense)|sensor|only \d+ cars|backed up)",
        "A working signal whose timing is a problem: waits too long, greens too short, turn arrows or sensors not giving enough time, causing backups."),
    "traffic sign repair": (["Traffic Sign Maintenance"],
        r"\bsigns?\b.{0,50}(down|missing|knocked|bent|faded|damaged|fallen|stolen|broken|leaning|turned|twisted|obstructed|blocked|replace|gone)|(down|missing|knocked|bent|faded|damaged|fallen|stolen|broken|leaning|twisted).{0,30}\bsigns?\b",
        "An existing traffic or street sign that is knocked down, missing, bent, faded, turned or blocked from view and needs repair or replacement."),
    "new sign, crosswalk or traffic-calming request": (["Traffic Engineering"],
        r"(speed (hump|bump|table|cushion)s?|traffic calming|(install|add|request(ing)?|need(s|ed)?|put in)( a| an| more)? (new )?(stop signs?|crosswalks?|4[- ]way stop|four[- ]way stop|signs?|speed)|new (stop )?signs?)",
        "A request for something new: a stop sign, crosswalk, speed hump, signage or other traffic-safety change to be evaluated by traffic engineers."),
    "lane striping, curb paint or guardrail repair": (["ROW Maintenance"],
        r"(strip(e|es|ing)\b|lane (lines?|markings?)|re-?paint|curb (paint|colou?r)|faded (red|white|yellow|green|blue)? ?curb|guard ?rails?|chain ?link fence|reflectors?|bott'?s dots)",
        "Upkeep of road markings and roadside hardware: faded lane striping or curb paint, damaged guardrails, barriers or city fences."),
    "graffiti on public property": (["Graffiti"], GRAFF,
        "Graffiti on public right-of-way property (streets, sidewalks, curbs, signs, poles, utility boxes, bridges, alleys), removed by the City's graffiti crew, when the report does not place it on private property."),
    "graffiti on private property": (["Graffiti - Code Enforcement"], GRAFF,
        "Graffiti on a private business, building, home, fence or dumpster, handled by code enforcement so the property owner removes it."),
    "illegal dumping": (["Illegal Dumping"],
        r"(dump(ed|ing)|couch|sofa|mattress(es)?|furniture|appliance|refrigerator|fridge|\btv\b|television|construction debris|pile of (trash|junk|debris)|abandoned (items|furniture|trash))",
        "Trash, furniture, mattresses, appliances or debris left on a public street, sidewalk, alley or lot by someone, not bins awaiting pickup."),
    "missed trash or recycling pickup": (["Missed Collection"],
        r"((not|n'?t|never|was not|were not)( been)? (picked up|collected|emptied|serviced)|missed (pick ?up|collection|my|our|the)|skipped (my|our|the)|no pick ?up)",
        "The City's scheduled collection skipped a household's trash, recycling or green-waste container on its collection day."),
    "waste on private property": (["Waste on Private Property"],
        r"(yard|property|house|home|lot|neighbou?r|apartment|backyard|front yard|premises).{0,60}(trash|junk|debris|garbage|rubbish|rats|hoard)|(trash|junk|debris|garbage|rubbish|hoard).{0,60}(yard|property|house|home|neighbou?r|premises)",
        "Trash, junk or debris accumulating on private property (a yard, lot or building grounds) that the owner must clean up, not dumping in the street."),
    "shared scooter or bike problem": (["Shared Mobility Device"],
        r"(scooters?|\bbirds?\b|\blime\b|e-?bikes?|dockless|jump bikes?|razor|\bspin\b|rental bikes?)",
        "A rented dockless scooter or e-bike left blocking a sidewalk, parked illegally, dumped or damaged; the operator is told to move it."),
    "homeless encampment": (["Encampment"],
        r"(encampments?|homeless|\btents?\b|\bcamp(ing|ed|s)?\b|transients?|living (in|on|under)|sleeping (on|in|under))",
        "People camping or living in tents, structures or on sidewalks, canyons or parks with belongings, reported for outreach and clean-up."),
    "parking violation": (["Parking"],
        r"(park(ed|ing)\b|72[- ]?h(ou)?rs?|hasn'?t (been )?moved|not moved|abandoned (car|vehicle|truck|van|rv|boat|trailer)|blocking (my |the )?driveway|red (zone|curb)|expired (tags|registration)|handicap(ped)? (spot|space|parking))",
        "A vehicle parked illegally or stored on the street: over 72 hours, in a red or other restricted zone, blocking a driveway, or abandoned."),
    "tree trimming or fallen tree": (["Tree Maintenance"],
        r"(\btrees?\b|branch(es)?|\blimbs?\b|palm fronds?|\bfronds\b|stumps?)",
        "A street tree in the public right-of-way that needs trimming, has fallen or hanging limbs or fronds, is dead, or should be evaluated for removal."),
    "overgrown weeds": (["Weed Cleanup"], r"(\bweeds?\b|tall grass|dry brush|dead brush|brush clearance|overgrown grass)",
        "Weeds, tall grass or dry brush growing on public land (medians, canyons, city lots, road edges) that need clearing, often as a fire risk."),
    "vegetation blocking the sidewalk": (["Right-of-Way Code Enforcement"],
        r"(bush(es)?|shrubs?|hedges?|ivy|bougainvillea|plants?|vegetation).{0,60}(block|encroach|overhang|hanging over|obstruct|over the sidewalk|onto the sidewalk|into the sidewalk|walkway)",
        "Bushes, hedges or plants from a private property growing over or blocking the public sidewalk; the owner is ordered to cut them back."),
    "street sweeping": (["Street Sweeping"], r"(sweep(ing|er|ers)?\b|street clean(ing)?)",
        "A request for the street sweeper: dirt, leaves, glass or debris along streets and gutters, or a missed or needed sweeping route."),
    "clogged or damaged storm drain": (["Stormwater"],
        r"(storm ?drains?|drain(age)? (is )?(clogged|blocked|damaged|broken|backed up|full)|catch basin|culvert|drainage (ditch|channel)|\binlet\b|drain grate)",
        "A storm drain, inlet, grate, culvert or drainage channel that is clogged, full of debris or damaged."),
    "polluted runoff or illegal discharge": (["Stormwater Code Enforcement"],
        r"(discharg|runoff|run-off|run off|irrigat|(washing|hosing|pouring|dumping|draining|rinsing).{0,40}(into|down|in) (the )?(street|gutter|drain|storm)|\boil\b|\bgrease\b|concrete (washout|slurry)|sewage|over-?irrigat|over ?water|pollut)",
        "Someone letting pollutants reach the storm drains: washing, hosing or pouring paint, oil, grease, concrete, sewage or irrigation water into the street or gutter."),
    "flooded street": (["Street Flooded"],
        r"(flood(ed|ing)?|standing water|ponding|puddl|water (is )?(pooling|pooled|collecting)|water (in|on|across) the (street|road))",
        "Water standing or flowing across a street or intersection (ponding, flooding, a water break) rather than a blocked drain being the reported issue."),
    "dead animal pickup": (["Dead Animal"], r"(\bdead\b|carcass|deceased|road ?kill)",
        "A dead animal on a street, sidewalk or public area that needs to be picked up."),
}
OWNER = {  # option -> (referral keys, cue regex, definition)
    "City graffiti crew": (["<city>"],
        r"\b(sidewalks?|streets?|curbs?|alley|signs?|light poles?|bridges?|retaining wall|overpass|underpass|bench|trash cans?|street lights?)\b",
        "Graffiti on City right-of-way or City street furniture (sidewalks, curbs, street signs, light poles, alleys, bridges, public walls), removed by the City's own crew."),
    "Park and Recreation Department": (["Park and Recreation"],
        r"\b(parks?|playgrounds?|rec(reation)? center|trails?|canyons?|open space|ball ?fields?|pool|restrooms?|comfort station|picnic)\b",
        "Graffiti inside a City park, playground, recreation center, trail or open-space canyon, handled by the Parks and Recreation Department."),
    "property owner via code enforcement": (["<private>"], PRIVATE,
        "Graffiti on a private business, building, house, fence or dumpster; code enforcement notifies the owner, who must remove it."),
    "utility company that owns the box or pole": (["Graffiti ? SDGE Poles and Boxes", "Graffiti ? ATT Telephone Booths / Cable Box",
                                                   "Graffiti ? Cox Communications"],
        r"(util(ity)? (box|boxes|cabinet|pole)|electric(al)? (box|boxes|cabinet)|green (box|boxes|cabinet)|cable (box|boxes)|telephone (box|pole)|phone (box|pole)|power (box|pole)|transformer|junction box|\bsdg&?e\b|\bat&t\b|\batt\b|\bcox\b)",
        "Graffiti on a utility box, cabinet, transformer or pole owned by a utility (SDG&E, AT&T or Cox); the report is referred to that company."),
    "Caltrans": (["Caltrans San Diego"],
        r"(freeways?|fwy|highways?|on-? ?ramps?|off-? ?ramps?|interstate|\bi-? ?(5|8|15|805)\b|\bsr-? ?\d+|\b(5|8|15|805|163|52|94|54|125|56|905)\s?(north|south|east|west|nb|sb|eb|wb)\b|sound ?wall)",
        "Graffiti on state highway property (freeways, on- and off-ramps, freeway signs, sound walls, overpasses on state routes), referred to Caltrans."),
    "Metropolitan Transit System": (["Graffiti ? SDMTS"],
        r"(trolley|bus (stop|bench|shelter)s?|\bmts\b|transit (center|station)|\bstation\b)",
        "Graffiti on transit property (trolley stations and tracks, bus stops, benches and shelters), referred to the Metropolitan Transit System."),
    "US Postal Service": (["Graffiti ? US Postal Services"], r"(mail ?box(es)?|\busps\b|post office|postal|mail (drop|collection) box)",
        "Graffiti on a blue mailbox, postal collection box or post office, referred to the US Postal Service."),
    "San Diego Unified School District": (["San Diego Unified School District"],
        r"\b(schools?|elementary|middle school|high school|campus)\b",
        "Graffiti on a public school's buildings, fences or grounds, referred to the San Diego Unified School District."),
    "Port of San Diego": (["Graffiti ? Port of San Diego"],
        r"(harbor|embarcadero|shelter island|\bport\b|bayfront|marina|seaport|tuna harbor|waterfront|bay ?side)",
        "Graffiti on Port of San Diego tidelands (Harbor Drive waterfront, Embarcadero, Shelter Island, marinas, bayfront parks), referred to the Port."),
}
Q_SERVICE = "Which City of San Diego 311 request type (and so which crew) should this resident's report be routed to?"
Q_OWNER = "Which crew or agency should this graffiti report be routed to for removal?"
PII = re.compile(r"(\b\d{3}[-.\s)]+\d{3}[-.\s]+\d{4}\b|@|https?://|www\.)", re.I)


def load_pins():
    import json
    return json.loads(PIN_FILE.read_text()) if PIN_FILE.exists() else {}


def main():
    import json
    pins = load_pins()
    shas = {}
    for fn in FILES:
        path = C.CACHE / KEY / fn
        sha = C.fetch(BASE + fn, path, pins.get(fn))
        shas[fn] = sha
    if not pins:
        PIN_FILE.write_text(json.dumps(shas, indent=1) + "\n")
    svc_cue = {o: re.compile(v[1], re.I) for o, v in SERVICE.items()}
    own_cue = {o: re.compile(v[1], re.I) for o, v in OWNER.items()}
    priv = re.compile(PRIVATE, re.I)
    graff = re.compile(GRAFF, re.I)
    svc_of = {s: o for o, v in SERVICE.items() for s in v[0]}
    ref_of = {s: o for o, v in OWNER.items() for s in v[0]}
    stats = collections.Counter()
    seen = set()
    svc_pool, own_pool = collections.defaultdict(list), collections.defaultdict(list)
    for fn in FILES:
        with open(C.CACHE / KEY / fn, newline="", encoding="utf-8", errors="replace") as f:
            for r in csv.DictReader(f):
                stats["rows"] += 1
                if r["case_origin"] not in ORIGINS or r.get("service_request_parent_id"):
                    continue
                if not r["date_requested"] or r["date_requested"][:10] >= "2022-11-30":
                    continue
                t = re.sub(r"\s+", " ", r.get("public_description") or "").strip()
                if not (25 <= len(t) <= 500) or len(t.split()) < 5:
                    continue
                if (t.lower().startswith(("translated", "there was an unplanned")) or PII.search(t) or "?" * 3 in t
                        or re.search(r"\b(Mr|Mrs|Ms|Miss)\.? [A-Z]", t)):
                    stats["drop_pii_or_translated"] += 1
                    continue
                n = C.norm(t)
                if n in seen:
                    continue
                seen.add(n)
                sname, status = r["service_name"], r["status"]
                ref = re.sub(r" at \S+@\S+.*$", "", (r.get("referred") or "")).replace("This report has been referred to ", "").strip()
                rec = {"rid": r["service_request_id"], "text": t, "service": sname, "detail": r.get("service_name_detail") or "",
                       "status": status, "referred": ref, "year": r["date_requested"][:4]}
                # graffiti owner question
                if sname in ("Graffiti", "Graffiti - Code Enforcement") and graff.search(t):
                    if status == "Referred":
                        own = ref_of.get(ref)
                    elif sname == "Graffiti - Code Enforcement":
                        own = "property owner via code enforcement"
                    else:
                        own = "City graffiti crew"
                    if own:
                        hits = {o for o, rx in own_cue.items() if rx.search(t)}
                        if hits == {own}:
                            own_pool[own].append(rec)
                            continue
                        stats["owner_cue_mismatch"] += 1
                # service question (only tickets the City itself closed)
                o = svc_of.get(sname)
                if o is None:
                    continue
                hits = {x for x, rx in svc_cue.items() if rx.search(t)}
                if "graffiti on public property" in hits or "graffiti on private property" in hits:
                    hits -= {"graffiti on public property", "graffiti on private property"}
                    if priv.search(t) and any(own_cue[x].search(t) for x in OWNER
                                              if x not in ("City graffiti crew", "property owner via code enforcement")):
                        stats["graffiti_public_private_conflict"] += 1  # review fix: e.g. utility box next to a gas station
                        continue
                    if priv.search(t):
                        hits.add("graffiti on private property")
                    elif (own_cue["City graffiti crew"].search(t)
                          or own_cue["utility company that owns the box or pole"].search(t)):
                        hits.add("graffiti on public property")
                    else:  # review fix: public needs a positive right-of-way cue (brand-name stores slipped through)
                        stats["graffiti_no_public_cue"] += 1
                        continue
                if hits == {o}:
                    svc_pool[o].append(rec)
                else:
                    stats["service_cue_mismatch"] += 1
    rng = random.Random(SEED)
    for pools in (svc_pool, own_pool):
        for k in pools:
            pools[k].sort(key=lambda x: x["rid"])
            rng.shuffle(pools[k])
    svc_opts, own_opts = sorted(SERVICE), sorted(OWNER)
    rows = []

    def mk(rec, q, gold, opts, instr):
        edge = None
        tl = rec["text"].lower()
        if gold == "missed trash or recycling pickup":
            edge = "negation"
        elif gold == "parking violation" and re.search(r"72|days|weeks|months|hasn'?t (been )?moved", tl):
            edge = "temporal"
        elif gold in ("graffiti on private property", "property owner via code enforcement", "vegetation blocking the sidewalk",
                      "waste on private property"):
            edge = "exception"
        return {"key": KEY, "rid": f"{rec['rid']}", "state": rec["text"], "instructions": instr, "options": opts,
                "gold": gold, "soft": None,
                "meta": {"dataset": "City of San Diego Get It Done 311 reports (data.sandiego.gov get-it-done-311)",
                         "config": f"q={q}; closed_{rec['year']} file", "revision": "sha256:" + "; ".join(f"{k}={v}" for k, v in shas.items()),
                         "licence": LICENCE, "split": "train",
                         "orig_label": {"service_name": rec["service"], "service_name_detail": rec["detail"],
                                        "status": rec["status"], "referred": rec["referred"]},
                         "family": C.FAMILY, "edge": edge, "defs": q, "seed": SEED}}
    for o in own_opts:
        for rec in own_pool[o][:OWNER_CAP]:
            rows.append(mk(rec, "graffiti_owner", o, own_opts, Q_OWNER))
    for o in svc_opts:
        for rec in svc_pool[o][:SERVICE_CAP]:
            rows.append(mk(rec, "service", o, svc_opts, Q_SERVICE))
    rows = C.cap_label(rows, lambda r: r["gold"], 0.5)
    rng.shuffle(rows)
    rows = C.near_dedupe(rows)
    out, rows = C.write_rows(rows, KEY)
    C.write_defs({o: SERVICE[o][2] for o in svc_opts}, KEY, "service")
    C.write_defs({o: OWNER[o][2] for o in own_opts}, KEY, "graffiti_owner")
    print(dict(stats))
    print("service pool:", {k: len(v) for k, v in sorted(svc_pool.items())})
    print("owner pool:", {k: len(v) for k, v in sorted(own_pool.items())})
    print(f"wrote {len(rows)} -> {out}")
    C.report(rows)


if __name__ == "__main__":
    main()
