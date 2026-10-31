"""Build golden rows for oiics_event: which OIICS 2.01 two-digit EVENT code describes how a worker was injured.

Source : CDC/NIOSH NEISS-Work emergency-department injury narratives (2012-2017) with two-digit OIICS event codes,
         released as Dataset.csv (229,820 rows: id, text, sex, age, event) in the official repository
         https://github.com/NASA-Tournament-Lab/CDC-NLP-Occ-Injury-Coding, pinned to commit
         7012b6726c9178ba4914b3de25578a75ad7d3e87 (sha256 below).
Licence: CC0 1.0 / US Government work: README.md 'Public Domain Standard Notice' ("This repository constitutes a
         work of the United States Government and is not subject to domestic copyright protection under 17 USC 105
         ... copyright and related rights in the work worldwide are waived through the CC0 1.0 Universal public
         domain dedication.").
Texts  : NEISS-Work narratives written by trained hospital coders from ED charts (human, 2012-2017, pre-LLM).
Labels : OIICS 2.01 two-digit event codes assigned by NIOSH coders (human).
Split  : the release has no split, but the 2019 CDC/NASA TopCoder competition scored models on 75,864 unlabelled
         narratives, which the HF mirror mayerantoine/injury-narrative-coding@61ac88cc publishes as test.csv. Every
         narrative that appears in that test.csv is EXCLUDED (used only as an exclusion list), so only
         competition-training narratives are used.
Label set: 36 two-digit codes (codes with too few or inconsistent rows are dropped: 10, 20, 29, 30, 40, 49, 50, 59,
         69, 74, 79, 99). Every row shows 12-30 of them: the gold, its hand-listed confusers (same division first),
         then a seeded random fill.
Quality guards (drop only, never relabel):
  1. Claude-written keyword cues (oiics_cues.py): the gold code needs a positive cue; strong cues of a competing
     code must not fire unless OIICS precedence makes the gold win anyway (e.g. an assault that ends in a fall is
     still 11; a fall that ends in hitting a table is still 42); 60/70 ('unspecified') rows must fire no mechanism
     cue at all; 41 rows must not mention a fall unless the fall is negated; knife/ran-over/eye-foreign-body rows
     follow the extra rules below.
  2. Out-of-fold TF-IDF + LR noise filter over the verified pool: rows whose human label gets p < 0.15 while
     another label gets p > 0.6 are dropped.
  3. Exact and near-exact duplicate narratives dropped.
Deterministic (seed 20261203). CPU only.
"""
import collections
import random
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ll_common as C  # noqa: E402
import oiics_cues as Q  # noqa: E402

KEY = "oiics_event"
SEED = 20261203
N_ROWS = 5000
POOL_CAP = 1400
COMMIT = "7012b6726c9178ba4914b3de25578a75ad7d3e87"
URL = f"https://raw.githubusercontent.com/NASA-Tournament-Lab/CDC-NLP-Occ-Injury-Coding/{COMMIT}/"
FILES = {"Dataset.csv": "eed1cd354759897b6ec891c86c40f0c81cb073d33c2c94d6a855c523e564b2ca",
         "README.md": "98508e110b0ec9f14889e4afec0b02939393f8c9e51b18a9316725a2a2c52652"}
TEST_URL = ("https://huggingface.co/datasets/mayerantoine/injury-narrative-coding/resolve/"
            "61ac88cc557f00ba44aa78190116b185bb4b8ac7/test.csv")
TEST_SHA = "d85cedaf37ff488a7381a71abc87fb6c9fae75333939e378924bdbc87486a425"
CACHE = C.CACHE / "oiics"
LICENCE = (f"CC0 1.0 / US Government work (https://github.com/NASA-Tournament-Lab/CDC-NLP-Occ-Injury-Coding/blob/"
           f"{COMMIT}/README.md, 'Public Domain Standard Notice': not subject to copyright under 17 USC 105; "
           "rights waived worldwide through CC0 1.0)")
DATASET = ("CDC/NIOSH NEISS-Work injury narratives with OIICS 2.01 two-digit event codes "
           "(github NASA-Tournament-Lab/CDC-NLP-Occ-Injury-Coding, Dataset.csv)")
QUESTION = "Which OIICS event category describes how this worker's injury happened?"

NAMES = {
    "11": "intentional injury by person",
    "12": "injury by person, unintentional or intent unknown",
    "13": "animal or insect related incident",
    "21": "aircraft incident",
    "22": "rail vehicle incident",
    "23": "animal-ridden or non-motorized vehicle incident",
    "24": "pedestrian struck by vehicle",
    "25": "water vehicle incident",
    "26": "roadway motor vehicle incident",
    "27": "non-roadway motorized land vehicle incident",
    "31": "fire",
    "32": "explosion",
    "41": "slip or trip without a fall",
    "42": "fall on same level",
    "43": "fall to lower level",
    "44": "jump to lower level",
    "45": "fall stopped by personal fall arrest system",
    "51": "exposure to electricity",
    "52": "exposure to radiation or noise",
    "53": "exposure to temperature extremes",
    "54": "exposure to air or water pressure change",
    "55": "exposure to other harmful substances",
    "56": "exposure to oxygen deficiency",
    "60": "contact with object or equipment, mechanism unspecified",
    "61": "needlestick without exposure to a harmful substance",
    "62": "struck by object or equipment",
    "63": "struck against object or equipment",
    "64": "caught in or compressed by equipment or objects",
    "65": "struck, caught or crushed in collapsing structure or material",
    "66": "rubbed or abraded by friction, pressure or foreign matter",
    "67": "rubbed, abraded or jarred by vibration",
    "70": "overexertion or bodily reaction, type unspecified",
    "71": "overexertion involving outside sources",
    "72": "repetitive motions involving microtasks",
    "73": "other exertions or bodily reactions",
    "78": "multiple types of overexertion and bodily reaction",
}
DEFS = {
    "11": ("A person deliberately hurt the worker (assault, punching, kicking, biting, stabbing, shooting, choking, "
           "shoving, robbery or a fight, including by patients, inmates or suspects); this outranks any fall, contact "
           "or exposure that followed."),
    "12": ("Another person hurt the worker with no assault or fight described: bumped, collided with, fell or "
           "landed on, grabbed or struck the worker accidentally, during a seizure, a game or while being cared "
           "for."),
    "13": ("An animal or insect caused the injury: bite, sting, scratch, kick, butt, trampling or being knocked "
           "over by an animal; falling from or being thrown by a ridden animal is a non-motorized vehicle incident "
           "instead."),
    "21": ("The injury happened aboard or from an aircraft in operation: turbulence, hard landing, crash, or "
           "parachuting or rappelling from it."),
    "22": ("A rail vehicle (train, trolley, streetcar, subway or mine rail car) caused the injury: collision, "
           "derailment, or sudden movement while the worker was on, under or beside it."),
    "23": ("The worker was riding an animal or a non-motorized vehicle (horse, bull, bicycle, scooter, "
           "skateboard) and fell, was thrown or crashed."),
    "24": ("The worker was on foot, not in or on a vehicle, and was struck, run over or pinned by a moving car, "
           "truck, forklift or other vehicle, on or off the road."),
    "25": ("The worker was on or boarding a boat, barge or ship and was hurt by the vessel's motion, sinking or "
           "collision, or by falling on board, overboard or from the vessel."),
    "26": ("The worker was a driver or passenger of a motorized vehicle in a crash, collision or rollover on a "
           "public road (a motor-vehicle crash), including hitting the inside of the vehicle during it."),
    "27": ("The worker was on or operating a motorized land vehicle or mobile machine away from public traffic "
           "(forklift, tractor, ATV, riding mower, golf cart, loader) that tipped, rolled, crashed or threw them "
           "off."),
    "31": ("An uncontrolled fire caused the injury: burns, smoke inhalation, overheating, or being struck or cut "
           "while fighting or escaping a fire; it outranks the contact, fall or exertion that happened during it."),
    "32": ("An explosion, blast or sudden burst (of a container, tank, tire, battery, aerosol can or pressurized "
           "vessel) caused the injury, including burns or debris from it."),
    "41": ("The worker slipped, tripped, stumbled or lost balance but did NOT fall, and was hurt by the slip itself "
           "or by catching or twisting to recover."),
    "42": ("The worker fell to the floor, ground or other surface they were standing or walking on (slip-and-fall, "
           "trip-and-fall, falling against something at that level); used when no height, stairs, ladder or "
           "vehicle is mentioned."),
    "43": ("The worker fell from a higher place to a lower one: off a ladder, roof, scaffold, stool, chair, "
           "vehicle, dock or platform, down stairs or steps, or into a hole, pit or trench."),
    "44": ("The worker deliberately jumped down from a higher place (truck bed, trailer, dock, ladder, scaffold, "
           "equipment) and was hurt on landing."),
    "45": ("The worker fell or jumped from a height and a personal fall arrest system (harness, lanyard, "
           "lifeline) stopped or caught the fall."),
    "51": ("The worker had an electric shock, electrocution or electrical burn from contact with electric current "
           "(wires, outlets, power lines, tools or equipment)."),
    "52": ("Radiation or noise caused the injury: welding arc flash burns to the eyes, ultraviolet or laser "
           "light, ionizing radiation, or loud noise damaging hearing."),
    "53": ("Extreme heat or cold caused the injury without a fire or explosion: burns or scalds from hot liquids, "
           "steam, food, surfaces or equipment, heat exhaustion or stroke, frostbite or hypothermia."),
    "54": ("A change in air or water pressure caused the injury: barotrauma of the ears or sinuses, decompression "
           "sickness, or altitude illness."),
    "55": ("A harmful substance was touched, inhaled, swallowed or injected: chemicals, caustics, cleaning agents, "
           "fumes, gases, pepper spray, allergens, blood or body fluids, including needlesticks with used or dirty "
           "needles."),
    "56": ("Breathing was blocked or oxygen was lacking: choking on food or an object, drowning, suffocation or "
           "an oxygen-deficient space, with no assault or vehicle incident."),
    "60": ("The worker was cut, punctured, bruised or fractured by contact with an object or equipment, but the "
           "narrative does not say whether they were struck by it, struck against it, caught in it or rubbed by "
           "it."),
    "61": ("The worker was pricked by a needle described as clean, sterile, unused or otherwise free of blood or "
           "other harmful substances (for example a sewing-machine needle)."),
    "62": ("A moving object hit the worker: something fell, was dropped, flew, swung, rolled or slipped onto or "
           "into them, including a tool that slipped in use; the object moved, not the worker (a moving vehicle "
           "hitting a worker on foot is a pedestrian incident)."),
    "63": ("The worker's own movement drove a body part into an object: bumping, banging, hitting or jamming "
           "against something, stepping on a nail or sharp object, or walking into equipment, with no fall."),
    "64": ("A body part was caught, pinched, squeezed, smashed or crushed in, under or between objects or machine "
           "parts (doors, drawers, rollers, gears, loads)."),
    "65": ("A collapsing structure or material struck, caught or buried the worker: trench or excavation "
           "cave-in, or collapse of a ceiling, wall, floor, scaffold or stacked material not set off by an "
           "explosion or fire."),
    "66": ("Friction, pressure or foreign matter caused the injury: blisters, chafing, rope or rug burns, or dust, "
           "dirt, sawdust, metal or other particles getting into the eye without being described as flying into "
           "it."),
    "67": ("Vibration caused the injury: prolonged use of vibrating tools or equipment (jackhammers, grinders), or "
           "being jolted and bounced while operating a vehicle or machine."),
    "70": ("The worker has a strain, sprain or muscle pain from exertion at work, but the narrative does not say "
           "what motion or activity (lifting, pushing, bending, repetitive use) caused it."),
    "71": ("Strain or pain from exerting force on an outside object or person: lifting, pushing, pulling, "
           "carrying, holding, throwing, moving or transferring loads or patients, with no fall or being struck."),
    "72": ("Pain or a disorder from repeating small, low-force motions over time (typing, keying, scanning, "
           "gripping, cutting, using the hands or wrists all day), with no single heavy exertion."),
    "73": ("Injury from the worker's own body motion with no outside load and no fall: bending, reaching, "
           "twisting, kneeling, squatting, climbing, standing up, walking, running or stepping wrong."),
    "78": ("The narrative gives two or more different exertion types together as the cause (for example lifting "
           "and bending, or carrying and twisting), with no other event."),
}
CONFUSERS = {
    "11": ["12", "13", "62", "63", "71", "55"], "12": ["11", "13", "62", "63", "71", "42"],
    "13": ["11", "12", "23", "62", "55"], "21": ["22", "25", "26", "27", "44", "54"],
    "22": ["21", "24", "26", "27", "62"], "23": ["13", "26", "27", "43", "24"],
    "24": ["26", "27", "62", "22", "63"], "25": ["21", "22", "26", "43", "56"],
    "26": ["24", "27", "62", "63", "22", "23"], "27": ["26", "24", "62", "43", "23"],
    "31": ["32", "53", "55", "51"], "32": ["31", "62", "53", "55"],
    "41": ["42", "43", "73", "44", "45"], "42": ["41", "43", "44", "63", "62", "45"],
    "43": ["42", "44", "45", "41", "27"], "44": ["43", "42", "73", "45"], "45": ["43", "44", "42", "41"],
    "51": ["53", "52", "55", "31"], "52": ["66", "55", "53", "51"], "53": ["55", "31", "52", "51", "32"],
    "54": ["56", "55", "21", "25"], "55": ["61", "53", "52", "66", "56"], "56": ["55", "54", "11", "25"],
    "60": ["62", "63", "64", "66", "70", "61"], "61": ["55", "62", "63", "60"],
    "62": ["63", "64", "60", "66", "24", "65"], "63": ["62", "64", "60", "42", "66"],
    "64": ["62", "63", "65", "60", "66"], "65": ["64", "62", "43", "32"], "66": ["62", "63", "52", "55", "60", "67"],
    "67": ["66", "71", "72", "62", "73"], "70": ["71", "73", "72", "78", "60"],
    "71": ["73", "78", "72", "70", "62"], "72": ["71", "73", "78", "70", "67"],
    "73": ["71", "78", "72", "41", "70", "63"], "78": ["71", "73", "72", "70"],
}
DIV = lambda c: c[0]  # noqa: E731
LOWER_PRECEDENCE = {"1": set("4567"), "2": set("4567"), "3": set("4567") , "4": set("67"), "5": set("7"),
                    "6": set("7"), "7": set()}
# extra tolerated strong cues (gold code -> codes whose strong cues do not block it)
EXTRA_TOL = {"11": {"55"}, "31": {"53", "55"}, "32": {"53", "55", "62"}, "78": {"71"}, "13": {"23"}}

CRE = {c: [re.compile(p) for p in ps] for c, ps in Q.CUES.items()}
SRE = {c: [re.compile(p) for p in ps] for c, ps in Q.STRONG.items()}
NO_FALL = re.compile(Q.NO_FALL)
KNIFE = re.compile(r"\b(KNIFE|KNIVES|BOX ?CUTTER|RAZOR|BLADE|SCISSORS|SLICER|MANDOLINE|EXACTO|UTILITY KNIFE)\b")
SLIPPED_TOOL = re.compile(Q.CUES["62"][4])
RANOVER = re.compile(r"\b(RAN|RUN|ROLLED|DROVE|BACKED) OVER\b")
EYE_FB = re.compile(r"\bEYES?\b.*\b(FB|FOREIGN BODY|SOMETHING|DEBRIS|DUST|PARTICLE|SAWDUST|METAL|SPLINTER|SAND|DIRT|RUST)\b|\b(FB|FOREIGN BODY|SOMETHING|DEBRIS|DUST|PARTICLE|SAWDUST|METAL|SPLINTER|SAND|DIRT|RUST)\b.*\bEYES?\b")
FLY = re.compile(r"\b(FLEW|FLYING|FLUNG|BLEW|BLOWN|PROPELLED|KICKED UP|SHOT (IN|INTO)|SPLASH\w*|SPRAY\w*|POPPED|SPARKS?|RICOCHET\w*)\b|\b(HIT|STRUCK) (HIM |HER )?IN THE EYE")
FELL_IN = re.compile(r"\b(FELL|FALLING|DROPPED|CAME DOWN|DRIPPED)\b")
VEH_OCC = re.compile(r"\b(DRIVER|DRIVING|DROVE|PASSENGER|RESTRAINED|SEAT ?BELT|IN (HIS|HER|A|THE) (CAR|TRUCK|VEHICLE|VAN|BUS|CAB))\b")
ON_FOOT = re.compile(r"\b(PEDESTRIAN|ON FOOT|WALKING|DIRECTING TRAFFIC|FLAGGING|STANDING (IN|ON|NEXT|BESIDE|BEHIND)|CROSSING)\b")
BOAT_EVENT = re.compile(r"\b(FELL|FALL|WAVE|WAVES|SINK|SANK|SINKING|JUMPED|THROWN|CAPSIZ\w*|COLLI\w*|ROUGH|OVERBOARD|SLIPPED)\b")


def fires(text):
    allc = {c for c, ps in CRE.items() if any(p.search(text) for p in ps)}
    strong = {c for c, ps in SRE.items() if any(p.search(text) for p in ps)}
    return allc, strong


def verify(gold, text):
    """Return None if the row passes the consistency guard, else a short reason (drop)."""
    allc, strong = fires(text)
    if gold not in allc and gold not in ("11",):
        return "no_gold_cue"
    if gold == "11" and "11" not in strong:
        return "no_strong_11"
    tol = {c for c in CRE if DIV(c) in LOWER_PRECEDENCE[DIV(gold)]} | EXTRA_TOL.get(gold, set())
    for c in strong:
        if c != gold and c not in tol:
            return f"strong_{c}"
    if gold == "12" and "11" in allc:
        return "cue_11"
    if gold == "41":
        if "42" in allc and not NO_FALL.search(text):
            return "fall_mentioned"
        if not NO_FALL.search(text) and not re.search(r"\b(TWIST|WRENCH|STRAIN|PULLED|JERK|CAUGHT|ROLLED|INVERT)", text):
            return "41_unclear"
    if gold in ("42", "43") and NO_FALL.search(text):
        return "fall_negated"
    if gold == "42" and ("43" in allc or "44" in allc):
        return "elevation_cue"
    if gold == "24" and (VEH_OCC.search(text) or not ON_FOOT.search(text) and not re.search(r"\b(STRUCK|HIT|RUN OVER|RAN OVER|PINNED|KNOCKED DOWN)\b", text)):
        return "24_occupant"
    if gold == "26" and (ON_FOOT.search(text) or "26" not in strong):
        return "26_unclear"
    if gold == "22" and ({"42", "43"} & allc) and not re.search(r"\b(MOV\w*|JERK\w*|START\w*|STOPP\w*|COLLI\w*|DERAIL\w*|HIT|STRUCK|LURCH\w*)\b", text):
        return "22_plain_fall"
    if gold == "45" and not re.search(r"\b(CAUGHT|STOPPED|PREVENT\w*|HANGING|HUNG|SLOWED|BROKE (HIS |HER |THE )?FALL|ARRESTED|SUSPENDED|DANGLING)\b", text):
        return "45_no_arrest"
    if gold == "25" and not BOAT_EVENT.search(text):
        return "25_no_vessel_event"
    if gold in ("60", "62", "63") and KNIFE.search(text) and not (gold == "62" and SLIPPED_TOOL.search(text)):
        return "knife_ambiguous"
    if gold in ("62", "60", "63") and RANOVER.search(text):
        return "ranover_ambiguous"
    if EYE_FB.search(text):
        if gold == "62" and not (FLY.search(text) or FELL_IN.search(text)):
            return "eye_fb_not_flying"
        if gold == "66" and (FLY.search(text) or FELL_IN.search(text)):
            return "eye_fb_flying_or_fell"
    if gold == "60":
        spec = {c for c in allc if DIV(c) in "123456" and c != "60"}
        if spec:
            return "60_has_mechanism"
    if gold == "70":
        spec = {c for c in allc if c != "70"}
        if spec:
            return "70_has_mechanism"
    if gold in ("71", "72", "73", "78") and (allc & {"42", "43", "62", "63", "64", "11", "12", "13", "26", "31", "32", "53", "55"}):
        return "7x_other_event"
    if gold == "71" and "78" in allc:
        return "multi_exertion"
    if gold == "73" and ("71" in allc or "78" in allc):
        return "outside_load"
    if gold == "72" and ("71" in allc or "73" in allc):
        return "72_mixed"
    if gold == "63" and ({"42", "43"} & allc):
        return "63_fall"
    if gold == "62" and ({"42"} & allc) and not re.search(r"\b(FELL|FALLEN|FALLING|DROPPED|CAME DOWN) (ON|ONTO)\b", text):
        return "62_fall"
    return None


def edge_tag(gold, text):
    allc, _ = fires(text)
    if gold in ("60", "70"):
        return "missing_info"
    if gold == "41" and NO_FALL.search(text):
        return "negation"
    if gold in ("11", "13", "26", "31", "32", "42", "43", "44") and (allc & {"62", "63", "64", "71", "42", "43"} - {gold}):
        return "exception"
    return None


def clean(t):
    return re.sub(r"\s+", " ", t).strip()


def main():
    paths = {}
    for f, sha in FILES.items():
        paths[f], _ = C.fetch(URL + f, CACHE / f, sha)
    tpath, _ = C.fetch(TEST_URL, CACHE / "hf_test.csv", TEST_SHA)
    df = pd.read_csv(paths["Dataset.csv"], dtype=str, keep_default_na=False)
    test_texts = set(pd.read_csv(tpath, dtype=str, keep_default_na=False)["text"])
    test_norm = {C.norm(t) for t in test_texts}
    print("rows:", len(df), "competition-test narratives:", len(test_texts))
    df = df[~df["text"].isin(test_texts)]
    df = df[~df["text"].map(C.norm).isin(test_norm)]
    print("after test exclusion:", len(df))
    df = df[df["event"].isin(NAMES)]
    df["text"] = df["text"].map(clean)
    df = df[df["text"].str.len() >= 30]
    df = df.sort_values("id", key=lambda s: s.astype(int))
    # exact dedup on normalised text (keep first id); conflicting-label duplicates dropped entirely
    lab_by_norm = collections.defaultdict(set)
    for t, e in zip(df["text"], df["event"]):
        lab_by_norm[C.norm(t)].add(e)
    df = df[df["text"].map(lambda t: len(lab_by_norm[C.norm(t)]) == 1)].drop_duplicates(subset="text")
    df = df[~df["text"].map(C.norm).duplicated()]
    print("usable train narratives:", len(df))

    rng = random.Random(SEED)
    reasons = collections.Counter()
    pools = collections.defaultdict(list)
    for rid, text, ev in zip(df["id"], df["text"], df["event"]):
        why = verify(ev, text)
        if why:
            reasons[why] += 1
            continue
        pools[ev].append((rid, text, ev))
    print("guard drops:", dict(reasons.most_common()))
    print("verified per code:", {c: len(v) for c, v in sorted(pools.items())})
    cand = []
    for c in sorted(pools):
        v = pools[c]
        rng.shuffle(v)
        cand += v[:POOL_CAP]
    keep, pg, po = C.oof_filter([t for _, t, _ in cand], [e for _, _, e in cand], seed=SEED, min_gold=0.15,
                                max_other=0.6)
    print("OOF drops:", sum(not k for k in keep), "of", len(cand))
    pools = collections.defaultdict(list)
    for (rid, text, ev), k in zip(cand, keep):
        if k:
            pools[ev].append((rid, text, ev))
    for c in pools:
        rng.shuffle(pools[c])
        pools[c].reverse()  # round_robin pops from the end
    nd = C.NearDup(thr=0.8, n=3)
    chosen = []
    labels = sorted(pools)
    i = 0
    while len(chosen) < N_ROWS and any(pools[c] for c in labels):
        c = labels[i % len(labels)]
        i += 1
        while pools[c]:
            rid, text, ev = pools[c].pop()
            if nd.seen(text):
                continue
            chosen.append((rid, text, ev))
            break
    all_names = [NAMES[c] for c in sorted(NAMES)]
    rows = []
    for rid, text, ev in chosen:
        opts = C.option_subset(NAMES[ev], all_names, [NAMES[x] for x in CONFUSERS[ev]], rng, lo=12, hi=30)
        rows.append({
            "key": KEY, "rid": f"neiss-work:{rid}", "state": text, "instructions": QUESTION, "options": opts,
            "gold": NAMES[ev], "soft": None,
            "meta": {"dataset": DATASET, "config": "OIICS 2.01 two-digit event (36 codes)",
                     "revision": f"git:{COMMIT}; sha256:{FILES['Dataset.csv']}; competition test excluded via "
                                 f"HF mayerantoine/injury-narrative-coding@61ac88cc test.csv sha256:{TEST_SHA}",
                     "licence": LICENCE, "split": "train", "orig_label": ev, "family": C.FAMILY,
                     "edge": edge_tag(ev, text)},
        })
    rows = C.final_dedup(rows)  # reviewer fix: exact near-duplicate pass (LSH misses pairs)
    rng.shuffle(rows)
    out = C.write_rows(KEY, rows)
    C.write_defs(KEY, {NAMES[c]: DEFS[c] for c in NAMES})
    print("wrote", out)
    C.summary(rows)
    print(dict(collections.Counter(r["meta"]["orig_label"] for r in rows).most_common()))
    C.show(rows, 8, seed=1)


if __name__ == "__main__":
    main()
