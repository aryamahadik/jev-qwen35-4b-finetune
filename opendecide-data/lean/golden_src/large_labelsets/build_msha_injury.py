"""Build golden rows for msha_injury: four large MSHA coding decisions on mine accident / injury / illness reports.

Source : MSHA Open Government Data, Accident Injuries data set (Accidents.zip -> Accidents.txt, pipe-delimited, all
         Form 7000-1 reports since 2000-01-01) + Accidents_Definition_File.txt, downloaded 2026-09-29 from
         https://arlweb.msha.gov/OpenGovernmentData/DataSets/ (the file is regenerated weekly; this builder pins the
         snapshot by sha256 and refuses other bytes).
Licence: US Government work, public domain (17 USC 105): U.S. Department of Labor, Mine Safety and Health
         Administration; https://www.dol.gov/general/aboutdol/copyright ("Materials created by the federal government
         are generally part of the public domain"), data.gov record catalog.data.gov/dataset/msha-accident-injuries-data-set
         (access level public). Narratives are mine-operator reports filed under 30 CFR Part 50 and published by MSHA.
Texts  : NARRATIVE (<= ~600 chars) written by mine operators / contractors; only accidents dated 2000-2021 (pre-LLM).
Labels : MSHA-coded fields from the same record (human coding): INJ_BODY_PART_CD (body part), NATURE_INJURY_CD
         (nature of injury), CLASSIFICATION_CD (accident classification) and MINING_EQUIP_CD (equipment involved).
Split  : no splits -> train.
Tasks  : each report is used for ONE question type only:
           body    : which body part was injured (41 labels; 27 can be gold, 14 distractor-only)
           nature  : nature of the injury (35 labels; 26 can be gold)
           class   : MSHA accident classification (26 labels, 'other' / 'all other illnesses' dropped)
           equip   : type of mining equipment involved (69 labels; about 65 can be gold)
         Every row shows 10-32 options: the gold, hand-listed confusers, then a seeded random fill.
Quality guards (drop only, never relabel): Claude-written keyword cues (msha_lex.py): the human-coded label must be
         the ONLY label of that task whose cue fires in the narrative (compound parts such as 'upper arm' suppress the
         generic 'arm'); task-specific block words (several body parts, fatalities, 'possible' fractures, ...);
         out-of-fold TF-IDF + LR filter per task (p_gold < 0.15 while another label > 0.6 -> drop); exact and
         near-exact duplicate narratives dropped; narratives with personal titles/names, e-mails or phone numbers
         dropped.
Reviewer fixes (round 2): Claude-written definitions for all equipment categories (no raw MSHA lists; timber/nipper
         truck no longer overlaps mine car); coal-drill cue/option without 'electric drill'; fracture and cut cues need
         a body part / wound on the person (msha_lex.py); black-lung vs other-pneumoconiosis definitions state MSHA's
         coding practice; exact near-duplicate pass (C.final_dedup) over all rows.
Deterministic (seed 20261205). CPU only.
"""
import collections
import random
import re
import sys
import zipfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ll_common as C  # noqa: E402
import msha_lex as L  # noqa: E402

KEY = "msha_injury"
SEED = 20261205
BASE = "https://arlweb.msha.gov/OpenGovernmentData/DataSets/"
FILES = {"Accidents.zip": "db5ac677f235e90f6214e6f26ee2b2994e32f01e18124f5165f05b5f741420b6",
         "Accidents_Definition_File.txt": "c7681808dd372b6c5bd95fdf70b01e856e0d2501b7e5d7cc9185f4c4e1f876e5"}
CACHE = C.CACHE / "msha"
LICENCE = ("US Government work, public domain (17 USC 105): U.S. Department of Labor, Mine Safety and Health "
           "Administration open data (https://arlweb.msha.gov/OpenGovernmentData/OGIMSHA.asp; DOL copyright notice "
           "https://www.dol.gov/general/aboutdol/copyright: 'Materials created by the federal government are generally "
           "part of the public domain'; catalog.data.gov/dataset/msha-accident-injuries-data-set, access level public)")
DATASET = "MSHA Accident Injuries data set (arlweb.msha.gov/OpenGovernmentData/DataSets/Accidents.zip), 2000-2021 reports"
YEARS = (2000, 2021)
QUOTA = {"class": 1700, "equip": 1200, "nature": 1700, "body": 1900}
ORDER = ["class", "equip", "nature", "body"]
COLS = {"body": "INJ_BODY_PART_CD", "nature": "NATURE_INJURY_CD", "class": "CLASSIFICATION_CD",
        "equip": "MINING_EQUIP_CD"}
QUESTIONS = {
    "body": "Which part of the body was injured in this mine accident report?",
    "nature": "What is the nature of the injury described in this mine accident report?",
    "class": "Which MSHA accident classification fits the circumstances that most directly caused this mine accident?",
    "equip": "Which type of mining equipment was involved in this mine accident?",
}
OPT_RANGE = {"body": (10, 30), "nature": (10, 28), "class": (10, 26), "equip": (12, 32)}

EQUIP_NOTES = {
    "28": "Hand tools with no motor or air/hydraulic power: hammers, sledges, wrenches, bars, knives, chisels, pliers.",
    "29": "Hand-held tools with a motor or air/hydraulic power: impact wrenches, angle grinders, chain saws, power drills.",
    "44": "Large off-road haul trucks used inside the mine or pit (rigid-frame or articulated rock trucks).",
    "45": "Ore haulage trucks licensed for public highways (over-the-road dump trucks and tractor-trailers).",
    "67": "Light and support trucks: service, utility, pickup, water, fuel and lube trucks (not ore haulage).",
    "24": "Wheeled loaders with a front bucket: front-end loaders, tractor-shovels, payloaders, highlifts, skip loaders.",
    "33": "Underground load-haul-dump machines and scoops (scooptrams, transloaders, battery scoops).",
    "23": "Forklifts, telehandlers, lift trucks and skid-steer loaders (e.g. Bobcat) used to lift and move loads.",
    "53": "Hand-held or leg-supported rock drills: jacklegs, airlegs, stopers, drifters and jackhammers.",
    "09": "Drills mounted on a carriage or vehicle: jumbos, air-track and rubber-tired drills, drill rigs.",
    "35": "The longwall cutting machine itself: the shearer or plow.",
    "36": "Longwall roof supports and parts other than the cutter: shields, ram jacks, Dowdy jacks, Duke.",
    "14": "Cranes, cherry pickers, boom trucks and scissor trucks used to lift loads.",
    "38": "Man lifts, lift baskets, basket scalers and self-propelled hydraulic booms that raise workers.",
    "19": "Shaft or slope conveyances that carry people or material: elevators, skips, cages, buckets, slope cars.",
    "30": "Hoisting and lifting devices that are not conveyances: hoists, car droppers, hydraulic jacks, car retrievers.",
    "12": "Continuous miners, tunnel borers and road headers that cut coal or rock at the face.",
    "54": "Roof and rock bolting machines, pinners and truss bolters.",
    "61": "Underground shuttle cars, buggies and ram cars that haul from the miner to the belt.",
    "37": "Vehicles that carry miners: mantrips, mancars, personnel carriers, porta-buses, jeeps, jitneys, ATVs.",
    "13": "Belt conveyors and their parts: belt feeders, stage loaders, hopper shakers, belt structure, pulleys.",
    "15": "Crushers, breakers and feeder breakers that break rock or coal into smaller pieces.",
    "39": "Grinding mills: rod, ball, autogenous, pug and hammer mills.",
    "58": "Screens, vibrators, shakers, rock screeners and scalpers that size material.",
    "60": "Digging machines: power shovels, backhoes, trackhoes, excavators and draglines.",
    "08": "Bulldozers, dozers, crawler tractors and push cats.",
    "70": "Welding and cutting equipment: welding machines, arc welders, air-arc, cutting torches.",
    "05": "Stationary shop machines: bench grinders, drill presses, band and table saws, sandblasters.",
    # reviewer fix (round 2): Claude-written definitions for the categories that were only MSHA's raw list
    "01": "Aerial trams and tramways: cars or buckets hung from an overhead cable that carry material or people.",
    "02": "Air compressors, stationary or portable (towed), that supply compressed air, including their belts, tanks and caps.",
    "03": "Airplanes and helicopters used for mine work or travel.",
    "04": "Auger machines, auger drills and highwall miners that bore coal out of an exposed seam or highwall.",
    "06": "Hand-held blow pipes, blow guns and air lances that blast compressed air to clean or free material.",
    "07": "Boats, barges, tugboats, skiffs and other watercraft.",
    "10": "Chutes: inclined troughs or spouts that material slides down between bins, conveyors, crushers or trucks.",
    "11": "Classifiers that separate particles by size or density in water: screw, spiral and cyclone classifiers.",
    "16": "Chain cutting machines (undercutters) that cut a slot in the coal face before blasting; not continuous miners.",
    "17": "Machines that cut or split dimension-stone blocks and slabs: gang, wire and block saws, guillotines, hydrosplitters.",
    "18": "Dredges: floating plants that dig sand, gravel or other material from under water.",
    "20": "Coal drills: face drills (often mobile or post-mounted) that bore shot holes in the coal for blasting.",
    "21": "Fans: mine ventilation, exhaust and auxiliary fans, and portable or circulating fans, with their blades, guards and cords.",
    "22": "Flotation cells and filters (filter presses, disc or drum filters) in mineral processing plants.",
    "25": "Gathering-arm (Joy) loaders, Conway loaders and other coal loading machines at the face.",
    "26": "Grizzlies: heavy bar grates over hoppers or feeders that scalp oversize rock from bulk material.",
    "27": "Gunite and shotcrete machines that spray concrete or mortar onto rock surfaces.",
    "30": "Hoists other than air hoists (chain, electric and overhead hoists), car droppers, hydraulic jacks and car retrievers.",
    "31": "Hydraulic jets and monitors: high-pressure water nozzles used to wash down or mine material.",
    "32": "Machines named as impactors (impact crushers that break rock with fast-spinning hammers or blow bars).",
    "34": "Rail-mounted locomotives (battery, trolley, diesel or air motors) that pull mine cars on track.",
    "40": "Milling machinery, block presses (making concrete or stone blocks) and ballast machines.",
    "41": "Timber trucks and nipper trucks that carry timbers and supplies to the working places.",
    "42": "Rail cars that carry ore, coal or rock: mine cars, ore and coal cars, rail cars, boxcars and hopper cars.",
    "43": "Mucking machines (overshot loaders, Cryderman muckers) that load broken rock in shafts, drifts or tunnels.",
    "46": "Packaging machines: baggers and bagging machines, bag sewing machines and palletizers.",
    "47": "Machines that load blasting agents into drill holes: pneumatic ANFO or prill loaders, powder buggies, driller-loaders.",
    "48": "Pumps: slurry, sump, water and other pumps, including their motors, hoses and piping.",
    "49": "Raise borers and raise drills that bore a vertical or steep opening between mine levels.",
    "50": "Raise climbers (for example Alimak): platforms that climb a rail up a raise carrying miners and equipment.",
    "51": "Raw coal storage structures, tipples and dump bins where coal is dumped, stored and loaded out.",
    "52": "Motor graders (road graders, motor patrols) with a long blade used to level and maintain haul roads.",
    "55": "Rock dusting machines and trickle dusters that spread inert rock dust in underground coal mines.",
    "56": "Rotary dumps that turn rail cars over to empty them, and dump rails.",
    "57": "Earth-moving scrapers (pan, tractor and elevating scrapers, scraper loaders); not slusher or scraper hoists.",
    "63": "Slushers (scraper or slusher hoists): winch-pulled scraper buckets that drag broken ore along a drift or stope.",
    "64": "Tamping machines and tampers that pack ballast under track or compact material.",
    "65": "Track equipment used to lay or repair rail track or re-rail cars: re-railers, track jacks, track shifters.",
    "66": "Tractors (farm, yard, earth-moving or tractor units not named as tractor-trailers or semis) and supply cars.",
    "68": "Tuggers, air winches, air hoists, air jacks and electric or hand-cranked winches used to pull or lift loads.",
    "69": "Washers: log, sand, coal and fine-material washers that clean mined material, and pressure or hot-water washers.",
    "71": "Other machines with no category of their own, such as wheelbarrows, well-drilling rigs and post-hole augers.",
}


def equip_def(code, orig):
    if code in EQUIP_NOTES:
        return EQUIP_NOTES[code]
    return "Equipment in MSHA's category: " + orig.strip().rstrip(".") + "."


CONFUSE = {
    "body": {"100": ["150", "160", "110", "140", "170"], "121": ["122", "120", "140"], "122": ["121", "120", "600"],
             "130": ["140", "144", "143"], "141": ["142", "140", "144"], "142": ["141", "143", "140", "200"],
             "143": ["140", "142", "144"], "150": ["100", "160", "170"], "200": ["420", "450", "142"],
             "310": ["311", "313", "312", "314", "350"], "311": ["310", "450", "312", "314"],
             "312": ["311", "313", "310", "314"], "313": ["320", "312", "310", "314"], "320": ["313", "330", "350"],
             "330": ["340", "320", "350"], "340": ["330", "320", "350"], "420": ["200", "440", "460", "430"],
             "430": ["420", "410", "460", "450"], "440": ["420", "410", "511", "460"], "450": ["311", "200", "430"],
             "510": ["511", "512", "513", "514", "550"], "511": ["510", "440", "512", "514"],
             "512": ["513", "511", "510", "514"], "513": ["512", "520", "510", "514"], "520": ["530", "513", "550"],
             "530": ["520", "540", "550"], "540": ["530", "520", "550"]},
    "nature": {"180": ["310", "100", "220", "170"], "220": ["200", "170", "330", "160"], "330": ["260", "270", "200"],
               "160": ["310", "170", "220"], "120": ["130", "301", "360", "304"], "130": ["120", "190", "320"],
               "301": ["360", "120", "210"], "360": ["301", "210", "120"], "210": ["360", "301"],
               "100": ["180", "170", "220"], "200": ["220", "330"], "260": ["330", "270"], "310": ["180", "160", "320"],
               "140": ["350", "160"], "240": ["380"], "293": ["294", "290", "291"], "294": ["293", "290", "291"],
               "250": ["230", "280"], "190": ["130", "380", "150"], "270": ["330", "200"], "340": ["350", "280"],
               "170": ["220", "160", "100"], "320": ["310", "130", "180"], "280": ["110", "130"],
               "110": ["280", "130"], "230": ["250"]},
    "class": {"07": ["06", "05", "02"], "06": ["07", "05"], "05": ["07", "06", "09"], "09": ["10", "18", "11", "05"],
              "10": ["09", "17", "20"], "11": ["12", "09"], "12": ["11", "17", "13"], "13": ["12", "17", "02"],
              "17": ["10", "12", "13", "01"], "18": ["19", "20", "09"], "19": ["18", "20"], "20": ["18", "19", "09"],
              "01": ["08", "17", "14"], "08": ["14", "01", "03"], "14": ["08", "04", "03"], "03": ["04", "14", "17"],
              "04": ["03", "14", "08"], "02": ["07", "16", "13"], "16": ["15", "02"], "15": ["16", "02"],
              "26": ["29", "28", "31"], "27": ["28", "29", "30"], "28": ["27", "29", "26"], "29": ["28", "27", "26"],
              "30": ["31", "29"], "31": ["30", "26"]},
    "equip": {"44": ["45", "67", "24", "57"], "45": ["44", "67"], "67": ["44", "45", "37"], "24": ["23", "33", "60", "08"],
              "23": ["24", "33", "38"], "33": ["24", "61", "43"], "61": ["33", "42", "34"], "34": ["42", "61", "37"],
              "37": ["67", "34", "61"], "54": ["12", "53", "09"], "12": ["54", "35", "25"], "35": ["36", "12"],
              "36": ["35", "30"], "53": ["09", "54", "29"], "09": ["53", "54"], "14": ["38", "30"], "38": ["14", "23"],
              "19": ["30", "68"], "13": ["58", "15", "10"], "15": ["39", "58", "32"], "58": ["26", "15", "13"],
              "60": ["24", "08", "57"], "08": ["60", "24", "52"], "52": ["57", "08"], "57": ["52", "60"],
              "28": ["29", "05"], "29": ["28", "05", "70"], "70": ["29", "05"], "05": ["29", "28"],
              "48": ["02", "21"], "02": ["48", "06"], "46": ["40", "13"], "55": ["27", "06"], "18": ["07", "31"],
              "04": ["09", "12"], "06": ["02", "29"], "17": ["40", "05"]},
}


def load():
    paths = {f: C.fetch(BASE + f, CACHE / f, sha)[0] for f, sha in FILES.items()}
    z = zipfile.ZipFile(paths["Accidents.zip"])
    df = pd.read_csv(z.open("Accidents.txt"), sep="|", dtype=str, encoding="latin-1", keep_default_na=False)
    return df


def tables(df):
    """label tables per task: code -> (name, definition, cue or None)."""
    eq = df.groupby("MINING_EQUIP_CD")["MINING_EQUIP"].first().to_dict()
    equip = {}
    for c, name in L.EQUIP_NAMES.items():
        equip[c] = (name, equip_def(c, eq.get(c, name)), L.EQUIP_CUES.get(c))
    return {"body": L.BODY, "nature": L.NATURE, "class": L.CLASS, "equip": equip}


CLASS09_BLOCK = re.compile(r"\b(COLLAPS\w*|CAVED|ROLLED|SLID|TRIPPED|SLIPPED|FELL (OFF|FROM|DOWN|ONTO|TO THE)|KNOCK\w*|STRUCK BY)\b")
PII = re.compile(r"\b(MR|MRS|MS|DR)\.? [A-Z][A-Za-z]+|@|\b\d{3}[-. ]\d{3}[-. ]\d{4}\b|\bSSN\b")


def clean(t):
    t = re.sub(r"\s+", " ", t).strip()
    return t


def main():
    df = load()
    print("all reports:", len(df))
    df = df[df["CAL_YR"].str.isdigit()]
    df = df[df["CAL_YR"].astype(int).between(*YEARS)]
    df["NARR"] = df["NARRATIVE"].map(clean)
    df = df[df["NARR"].str.len().between(60, 700)]
    df = df[~df["NARR"].str.contains(PII)]
    # exact dedup (normalised); duplicated narratives dropped entirely (often multi-victim copies with different codes)
    nn = df["NARR"].map(C.norm)
    df = df[~nn.duplicated(keep=False)].copy()
    df["T"] = df["NARR"].str.upper().str.replace(r"[^A-Z0-9 ]", " ", regex=True).str.replace(r"\s+", " ", regex=True)
    print("usable 2000-2021 narratives:", len(df))
    tabs = tables(df)
    comp = {t: {c: re.compile(v[2]) for c, v in tab.items() if v[2]} for t, tab in tabs.items()}
    block = {"body": re.compile(L.BODY_BLOCK), "nature": re.compile(L.NATURE_BLOCK)}

    rng = random.Random(SEED)
    recs = list(zip(df["DOCUMENT_NO"], df["NARR"], df["T"], *[df[COLS[t]] for t in ORDER], df["DEGREE_INJURY_CD"]))
    rng.shuffle(recs)
    cand = {t: collections.defaultdict(list) for t in ORDER}
    stats = {t: collections.Counter() for t in ORDER}
    for rec in recs:
        doc, narr, T = rec[:3]
        golds = dict(zip(ORDER, rec[3:7]))
        for t in ORDER:
            g = golds[t]
            if g not in comp[t]:
                stats[t]["gold_not_checkable"] += 1
                continue
            if t in block and block[t].search(T):
                stats[t]["blocked"] += 1
                continue
            hits = {c for c, p in comp[t].items() if p.search(T)}
            if t == "class" and g == "09" and CLASS09_BLOCK.search(T):
                stats[t]["handling_other_event"] += 1
                continue
            if t == "class" and g == "11" and re.search(r"\bPOWER(ED)? (WHEEL ?BARROW|CART|DOLLY)", T):
                stats[t]["powered_cart"] += 1
                continue
            if t == "body":
                if hits & {"311", "313"}:
                    hits.discard("310")
                if "513" in hits:
                    hits.discard("510")
                if "130" in hits and re.search(r"\bEYE ?(BOLT|HOOK|LET)|\bEYE OF\b", T):
                    stats[t]["eye_object"] += 1
                    continue
            if t == "nature" and "320" in hits and hits & {"180", "310", "120", "130", "301"}:
                hits.discard("320")
                hits.add("x")  # dust-in-eye with a named wound is unclear
            if hits != {g}:
                stats[t]["cue_mismatch" if g not in hits else "several_cues"] += 1
                continue
            stats[t]["ok"] += 1
            cand[t][g].append((doc, narr, g, rec[7]))
    for t in ORDER:
        print(t, dict(stats[t]), {c: len(v) for c, v in sorted(cand[t].items())})

    used = set()
    nd = C.NearDup(thr=0.6, n=3)
    rows = []
    for t in ORDER:
        tab = tabs[t]
        pool = []
        for c in sorted(cand[t]):
            v = [x for x in cand[t][c] if x[0] not in used][:900]
            pool += v
        keep, _, _ = C.oof_filter([x[1] for x in pool], [x[2] for x in pool], seed=SEED, min_gold=0.15, max_other=0.6)
        print(f"[{t}] OOF drops: {sum(not k for k in keep)} of {len(pool)}")
        pools = collections.defaultdict(list)
        for x, k in zip(pool, keep):
            if k:
                pools[x[2]].append(x)
        for c in pools:
            pools[c].reverse()
        labels = sorted(pools)
        chosen, i = [], 0
        while len(chosen) < QUOTA[t] and any(pools[c] for c in labels):
            c = labels[i % len(labels)]
            i += 1
            while pools[c]:
                x = pools[c].pop()
                if x[0] in used or nd.seen(x[1]):
                    continue
                chosen.append(x)
                used.add(x[0])
                break
        all_names = [tab[c][0] for c in sorted(tab)]
        lo, hi = OPT_RANGE[t]
        for doc, narr, g, degree in chosen:
            conf = [tab[c][0] for c in CONFUSE[t].get(g, []) if c in tab]
            opts = C.option_subset(tab[g][0], all_names, conf, rng, lo=lo, hi=hi)
            edge = None
            if t == "body" and g in ("100", "310", "510"):
                edge = "missing_info"
            elif t == "class" and degree == "00":
                edge = "implicit"  # accident with no injury: classify the event itself
            rows.append({
                "key": KEY, "rid": f"msha:{doc}:{t}", "state": narr, "instructions": QUESTIONS[t], "options": opts,
                "gold": tab[g][0], "soft": None,
                "meta": {"dataset": DATASET, "config": f"task={t} ({COLS[t]})",
                         "revision": f"snapshot 2026-09-29; sha256 Accidents.zip:{FILES['Accidents.zip']}",
                         "licence": LICENCE, "split": "train", "orig_label": {"code": g, "task": t},
                         "family": C.FAMILY, "edge": edge},
            })
    rows = C.final_dedup(rows)  # reviewer fix: exact near-duplicate pass (LSH misses pairs)
    rng.shuffle(rows)
    out = C.write_rows(KEY, rows)
    for t in ORDER:
        C.write_defs(f"{KEY}__{t}", {v[0]: v[1] for v in tabs[t].values()})
    for r in rows:
        r["meta"]["defs"] = r["meta"]["config"].split("=")[1].split(" ")[0]
    C.write_rows(KEY, rows)
    print("wrote", out)
    C.summary(rows)
    for t in ORDER:
        C.show([r for r in rows if r["meta"]["orig_label"]["task"] == t], 3, seed=3)


if __name__ == "__main__":
    main()
