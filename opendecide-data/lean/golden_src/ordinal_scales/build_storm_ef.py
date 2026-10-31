"""Build raw rows for storm_ef: which Enhanced Fujita (EF) rating did the NWS damage survey give this tornado?

Source : NOAA NCEI Storm Events Database, bulk CSV export
         https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/StormEvents_details-ftp_v1.0_dYYYY_c*.csv.gz,
         years 2007-2024 (EF scale in use from Feb 2007; 2025-2026 left untouched as fresh data). Each yearly file is
         snapshotted under cache/storm_ef/ and pinned by sha256 (NCEI re-creates files monthly; the c-date is pinned).
Licence: US Government work (NOAA / National Weather Service "Storm Data", NWS Directive 10-1605), public domain
         under 17 U.S.C. 105; NCEI ISO metadata gov.noaa.ncdc:C00510 (https://www.ncei.noaa.gov/metadata/geoportal/
         rest/metadata/item/gov.noaa.ncdc:C00510/xml) states the only use constraint: "Cite dataset when used as a
         source."
Texts  : EVENT_NARRATIVE written by NWS meteorologists after the damage survey (human-written). The episode
         narrative is NOT used (it describes the whole outbreak and names other tornadoes' ratings).
Labels : TOR_F_SCALE, the official EF rating assigned by the NWS survey (human expert decision): EF0-EF5, or EFU
         (unknown: no rateable damage). Single survey decision -> soft = null.
Redaction: explicit rating mentions in the narrative ("an EF-1 tornado", "rated EF2", "EF-U", "EF unknown") are
         replaced with "[rating withheld]"; nothing else is changed ('|' line-wrap artefacts become spaces/newlines).
         Wind-speed estimates, damage-indicator codes, path length and width are kept (they are the survey evidence).
Filters: single-segment tornadoes only (TOR_OTHER_WFO / TOR_OTHER_CZ_NAME empty, and no narrative wording about
         crossing into / continuing from another county or parish: a segment's rating can differ from what its
         narrative describes); rows whose largest stated wind estimate lies outside the label's EF wind band are
         dropped; narrative >= 15 words after redaction; rows with any residual
         F-scale token dropped; EF0 rows whose narrative says there was no damage, or names no damage at all, are
         dropped (the EFU convention since 2016 is 'no rateable damage -> EFU', and older offices sometimes used EF0
         for that). Review fixes (29 Sep 2026): wind estimates in 'miles per hour' / knots are also checked against
         the EF band; narratives that name another county/parish or state, a county/state line, or a 'total path
         length' that differs from this segment's length are dropped (they describe damage outside the rated
         segment, e.g. a Talbot County EF1 segment narrating a 61-mile multi-county track).
Balance: per-class caps (EF0/EF1/EF2 1,050 each; all EF3-EF5; EFU 600), dedupe exact + near-exact narratives.
Deterministic (seed 20261101); CPU only; no model calls.
"""
import collections
import random
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ord_common as C  # noqa: E402

KEY = "storm_ef"
SEED = C.SEED
CACHE = C.CACHE / KEY
BASE = "https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/"
FILES = {
    "StormEvents_details-ftp_v1.0_d2007_c20260323.csv.gz": "e8289daa871946230862e2ca0d119195df7108e4a680fe83e3d419f3f21a7524",
    "StormEvents_details-ftp_v1.0_d2008_c20260323.csv.gz": "c97260e82760b17bc571d55e1ca1f5073ccc0558b774313d46dddc3e1ef39b37",
    "StormEvents_details-ftp_v1.0_d2009_c20260323.csv.gz": "c04d6e0173153475440cb614bd019287986c74c311c61864478f9087d7d1b357",
    "StormEvents_details-ftp_v1.0_d2010_c20260323.csv.gz": "d109f8a6ab1a71e70f60fe42d30a0e31f370c904e248a51e5fe85573f904878e",
    "StormEvents_details-ftp_v1.0_d2011_c20260323.csv.gz": "be3b40cd098a879be12c2c3e614700560bd537e6178bba8b1aaf099f665dda40",
    "StormEvents_details-ftp_v1.0_d2012_c20260323.csv.gz": "673db47f6dc9e97e06ffec3b628f5341c128f594d9b247bd07bad2e8397ebac3",
    "StormEvents_details-ftp_v1.0_d2013_c20260323.csv.gz": "4fa4036ed1c7ea9a779d5a5841d18de08596c423920189a9e6173488d1a98260",
    "StormEvents_details-ftp_v1.0_d2014_c20260323.csv.gz": "410b457b1b9628cfd63292848a626482a88714c8bd8c45d56a0469f9de05d078",
    "StormEvents_details-ftp_v1.0_d2015_c20260323.csv.gz": "c4a5a24b8c69ad2b6b867790ce298f5b642a60516c9fce5550a8d2f67cd7bf2e",
    "StormEvents_details-ftp_v1.0_d2016_c20260323.csv.gz": "d8e1389897df3557e74ba36820357f6962a7c0ca922595400fe74d883f7a5036",
    "StormEvents_details-ftp_v1.0_d2017_c20260519.csv.gz": "bd3ca72b71544222cba8aa2b29eb3f0efe050d3330a0c408e208befb66881750",
    "StormEvents_details-ftp_v1.0_d2018_c20260323.csv.gz": "19702480f50cd2a8dacce5e57891feba156afb87b1ea5cbb4eaeda69d2b964a4",
    "StormEvents_details-ftp_v1.0_d2019_c20260323.csv.gz": "f5043ecc776818b0feffdf1e0fcbaf63329db0635eab1057c7b8ba00ef332e3b",
    "StormEvents_details-ftp_v1.0_d2020_c20260323.csv.gz": "895c56fd46991c4d9a135d67558dc4b447a02a2314efac0ace645135b98f9c9d",
    "StormEvents_details-ftp_v1.0_d2021_c20260323.csv.gz": "60c1daf96dbe8eafd48c80df5b70df51a0125ab95d467ee7009a646761d57715",
    "StormEvents_details-ftp_v1.0_d2022_c20260625.csv.gz": "7d6b79d0049a6edec96b061738289daddba90be26fc9afe7b0a6fd617f21452e",
    "StormEvents_details-ftp_v1.0_d2023_c20260323.csv.gz": "713784bed40d9e5a95b1d6240a654f865f3ef97703713105c7b35437270da134",
    "StormEvents_details-ftp_v1.0_d2024_c20260728.csv.gz": "2070b83eccab041b36360ab73645b9a249c3eefc5b92b5b3fc0cbba4d9fcc09c",
}
LICENCE = ("US Government work, public domain (17 U.S.C. 105; NOAA/NWS Storm Data per NWS Directive 10-1605); NCEI "
           "metadata gov.noaa.ncdc:C00510 (https://www.ncei.noaa.gov/metadata/geoportal/rest/metadata/item/"
           "gov.noaa.ncdc:C00510/xml) use constraint: 'Cite dataset when used as a source.'")
DATASET = "NOAA NCEI Storm Events Database (StormEvents_details bulk CSV, 2007-2024), tornado events"

QUESTION = ("Based on this National Weather Service storm-survey narrative, which Enhanced Fujita (EF) rating was "
            "assigned to the tornado?")
LEVELS = ["EFU (unrated)", "EF0", "EF1", "EF2", "EF3", "EF4", "EF5"]  # ordered: not rateable, then weakest -> strongest
LABEL2OPT = {"EFU": "EFU (unrated)", "EF0": "EF0", "EF1": "EF1", "EF2": "EF2", "EF3": "EF3", "EF4": "EF4",
             "EF5": "EF5"}
DEFS = {
    "EFU (unrated)": "No rating could be assigned because the tornado struck no rateable damage indicator (for example "
                     "it stayed over open fields, water or unpopulated land); used for confirmed tornadoes with no "
                     "surveyable damage.",
    "EF0": "Estimated 3-second gust 65-85 mph: light damage such as shingles or siding peeled, gutters damaged, "
           "branches broken and shallow-rooted trees pushed over; some damage to at least one indicator is required.",
    "EF1": "Estimated gust 86-110 mph: moderate damage such as roofs badly stripped, mobile homes overturned or badly "
           "damaged, exterior doors lost, windows broken and many trees snapped or uprooted.",
    "EF2": "Estimated gust 111-135 mph: considerable damage such as roofs torn off well-built houses, frame houses "
           "shifted on foundations, mobile homes destroyed, large trees snapped or uprooted, cars lifted.",
    "EF3": "Estimated gust 136-165 mph: severe damage such as entire stories of well-built houses destroyed, major "
           "damage to large buildings, trains overturned, trees debarked, heavy cars lifted and thrown.",
    "EF4": "Estimated gust 166-200 mph: devastating damage such as well-constructed houses and whole frame houses "
           "leveled, cars thrown and large debris becoming airborne missiles.",
    "EF5": "Estimated gust over 200 mph: incredible damage such as strong frame houses leveled and swept clean off "
           "their foundations, reinforced-concrete structures critically damaged, car-sized missiles thrown far.",
}
CAPS = {"EF0": 1050, "EF1": 1050, "EF2": 1050, "EF3": 10**6, "EF4": 10**6, "EF5": 10**6, "EFU": 600}

RATING = re.compile(
    r"(?i)\(?\b(?:e\.?f)[- ]?(?:[0-5](?![0-9])|u\b|unknown\b|zero\b|one\b|two\b|three\b|four\b|five\b)\)?"
    r"(?:\s*\((?:e\.?f)?[- ]?[0-5u]\))?")
RESIDUAL = re.compile(r"(?i)\b(?:e\.?f[- ]?\d|e\.?f[- ]?u\b|f[- ]?[0-5]\b|f-?scale\b)")
NO_DAMAGE = re.compile(r"(?i)\bno (?:known |reported |observed |visible |discernible |significant |apparent )?damage\b|"
                       r"\b(?:did not|didn't) (?:cause|produce|do|result in) (?:any )?(?:known )?damage\b|"
                       r"\bcaused no damage\b|\bno damage (?:was|were) (?:found|observed|reported|noted)\b|"
                       r"\bno damage indicators?\b")
WIND_UNIT = r"(mph|m\.p\.h\.?|miles per hour|miles an hour|knots|kts|kt)"
MPH = re.compile(r"(?i)\b\d{2,3}\s*(?:-|to)?\s*(?:\d{2,3}\s*)?" + WIND_UNIT + r"(?![a-z])")
MPH_NUMS = re.compile(r"(?i)(\d{2,3})(?:\s*(?:-|to)\s*(\d{2,3}))?\s*" + WIND_UNIT + r"(?![a-z])")
# review fix (29 Sep): a narrative that names another county/parish or another state, or whose 'total path length'
# differs from this segment's length, describes damage outside the rated segment -> its label may not match the text
COUNTY_NAME = re.compile(r"\b((?:[A-Z][a-zA-Z.'\u2019]+\s){1,3})(?:County|Parish|Counties|Parishes|county|parish|Co\.)\b")
DIRWORDS = re.compile(r"^(?:(?:in|of|into|from|the|western|eastern|northern|southern|central|north|south|east|west|"
                      r"northeast|northeastern|northwest|northwestern|southeast|southeastern|southwest|southwestern|"
                      r"extreme|far|rural|and|across|through|near|to|nearby|adjacent|neighboring|neighbouring)\s+)+", re.I)
STATES = ("Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|Florida|Georgia|Hawaii|Idaho|"
          "Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland|Massachusetts|Michigan|Minnesota|"
          "Mississippi|Missouri|Montana|Nebraska|Nevada|New Hampshire|New Jersey|New Mexico|New York|North Carolina|"
          "North Dakota|Ohio|Oklahoma|Oregon|Pennsylvania|Rhode Island|South Carolina|South Dakota|Tennessee|Texas|"
          "Utah|Vermont|Virginia|Washington|West Virginia|Wisconsin|Wyoming")
OTHER_STATE = re.compile(r"\b(?:into|from|out of|across|over|entering|entered|crossing|crossed)\s+(?:the\s+)?(?:state of\s+)?"
                         r"(?:(?:north|south|east|west|northern|southern|eastern|western|extreme|far)\w*\s+)?"
                         r"(" + STATES + r")\b(?!\s+(?:Road|Rd|Street|St|Avenue|Ave|Highway|Hwy|Route|Drive|Dr|Lane|Ln|"
                         r"Blvd|City|Beach|Crossing|County|Parish|State Route|[0-9]))")
BORDER = re.compile(r"(?i)\b(?:state|county|parish) (?:line|border|boundary)\b|\bborder of\b|\b(?:county|parish)/")
TOTAL_LEN = re.compile(r"(?i)\b(?:total|entire|overall|whole)\s+(?:tornado\s+)?(?:damage\s+)?(?:path|track)?\s*"
                       r"(?:length|path|track)?\D{0,40}?(\d+(?:\.\d+)?)\s*(?:miles?|mi\b)")
# review fix: EF0 needs some damage to a damage indicator (definition); narratives with no damage at all are EFU-like
DAMAGE = re.compile(r"(?i)damag|\btrees?\b|\broofs?\b|snapp|uproot|destroy|\bblown\b|debris|\blimbs?\b|branch|shingle|"
                    r"siding|\bbarns?\b|\bsheds?\b|outbuild|power ?(?:lines?|poles?)|\bcrops?\b|\bcorn\b|fence|overturn|"
                    r"toppl|\bbroke|lofted|tossed|knocked|flipp|collaps|\bdowned\b|\bdown(?:ed)? (?:trees|limbs|power)|"
                    r"\bpivots?\b|irrigation|\bgrain bins?\b|\bsilos?\b|\bcarport|\bthrew\b|\bthrown\b|\bscour")
# narratives of tornadoes that cross a county/parish line describe damage outside the rated segment
CROSS = re.compile(r"(?i)\b(?:moved|continued|crossed|entered|tracked|passed|moving|crossing|entering)\s+(?:\w+\s+){0,3}"
                   r"(?:in)?to\s+(?:\w+\s+){0,2}(?:county|parish|state)\b|\bfrom\s+(?:\w+\s+){1,2}(?:county|parish)\b|"
                   r"\b(?:county|parish|state) line\b|\bcontinuation\b|\bsee storm data\b|\bsegment\b|"
                   r"\b(?:county|parish) portion\b|\binto (?:\w+\s+){0,2}(?:county|parish)\b")
BAND = {"EF0": (0, 85), "EF1": (86, 110), "EF2": (111, 135), "EF3": (136, 165), "EF4": (166, 200), "EF5": (201, 999)}


def wind_mismatch(nar, lab):
    """True if the largest wind estimate (>= 60 mph) stated in the narrative falls outside the label's EF band."""
    if lab not in BAND:
        return False
    nums = []
    for m in MPH_NUMS.finditer(nar):
        f = 1.151 if m.group(3).lower().startswith(("knot", "kt")) else 1.0  # knots -> mph
        nums += [int(round(int(x) * f)) for x in m.groups()[:2] if x]
    nums = [n for n in nums if n >= 60]
    if not nums:
        return False
    lo, hi = BAND[lab]
    return not (lo - 2 <= max(nums) <= hi + 2)


def other_area(nar, cz_name, state):
    """True if the narrative names a county/parish other than this row's own, a state border / county line, or says
    the tornado moved into / came from another state (review fix, 29 Sep 2026)."""
    own = re.sub(r"[^a-z]", "", cz_name.lower())
    for m in COUNTY_NAME.finditer(nar):
        nm = re.sub(r"[^a-z]", "", DIRWORDS.sub("", m.group(1).strip()).lower())
        if nm and nm not in own and own not in nm:
            return True
    if BORDER.search(nar):
        return True
    for m in OTHER_STATE.finditer(nar):
        if m.group(1).lower() != state.lower():
            return True
    return False


def total_len_differs(nar, tor_length):
    try:
        seg = float(tor_length)
    except (TypeError, ValueError):
        return bool(TOTAL_LEN.search(nar))
    for m in TOTAL_LEN.finditer(nar):
        v = float(m.group(1))
        if abs(v - seg) > max(0.3, 0.1 * max(v, seg)):
            return True
    return False


def redact(text):
    t = str(text).replace("||", "\n\n").replace("|", " ")
    t = re.sub(r"(?<=\w)\ufffd+(?=s\b)", "'", t)  # broken curly apostrophes in the NCEI export
    t = RATING.sub("[rating withheld]", t)
    t = re.sub(r"(\[rating withheld\])(?:\s*\[rating withheld\])+", r"\1", t)
    t = re.sub(r"(?i)(\[rating withheld\])\s*\((?:unknown|u|unrated|not rated)\)", r"\1", t)  # '(unknown)' = EFU
    return C.clean(t)


def fmt_num(x, unit):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    if v != v or v <= 0:
        return None
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return f"{s} {unit[:-1] if s == '1' else unit}"


def main():
    frames = []
    for name, sha in FILES.items():
        p = C.fetch(BASE + name, CACHE / name, sha)
        df = pd.read_csv(p, low_memory=False, dtype=str,
                         usecols=["EVENT_ID", "EPISODE_ID", "EVENT_TYPE", "YEAR", "MONTH_NAME", "STATE", "CZ_NAME",
                                  "CZ_TYPE", "TOR_F_SCALE", "TOR_LENGTH", "TOR_WIDTH", "TOR_OTHER_WFO",
                                  "TOR_OTHER_CZ_NAME", "EVENT_NARRATIVE"])
        frames.append(df[df.EVENT_TYPE == "Tornado"])
    t = pd.concat(frames, ignore_index=True)
    stats = collections.Counter()
    stats["tornado_records"] = len(t)
    recs = []
    for r in t.itertuples(index=False):
        lab = str(r.TOR_F_SCALE)
        if lab not in LABEL2OPT:
            stats["drop_not_ef"] += 1
            continue
        if isinstance(r.TOR_OTHER_WFO, str) or isinstance(r.TOR_OTHER_CZ_NAME, str):
            stats["drop_multi_segment"] += 1
            continue
        if not isinstance(r.EVENT_NARRATIVE, str):
            stats["drop_no_narrative"] += 1
            continue
        nar = redact(r.EVENT_NARRATIVE)
        if len(C.words(nar)) < 15:
            stats["drop_short"] += 1
            continue
        if RESIDUAL.search(nar):
            stats["drop_residual_rating"] += 1
            continue
        if "\ufffd" in nar:
            stats["drop_encoding"] += 1
            continue
        if CROSS.search(nar):
            stats["drop_crosses_county"] += 1
            continue
        if other_area(nar, str(r.CZ_NAME), str(r.STATE)):
            stats["drop_names_other_county_or_state"] += 1
            continue
        if total_len_differs(nar, r.TOR_LENGTH):
            stats["drop_total_length_differs"] += 1
            continue
        if wind_mismatch(nar, lab):
            stats["drop_wind_vs_rating"] += 1
            continue
        if lab == "EF0" and (NO_DAMAGE.search(nar) or not DAMAGE.search(nar)):
            stats["drop_ef0_no_damage"] += 1
            continue
        where = str(r.CZ_NAME).title()
        if str(r.CZ_TYPE) == "C":
            where += " Parish" if str(r.STATE).upper() == "LOUISIANA" else " County"
        head = (f"NWS Storm Data tornado entry ({str(r.MONTH_NAME).title()} {r.YEAR}, {where}, "
                f"{str(r.STATE).title()}).")
        dims = [x for x in (("path length " + fmt_num(r.TOR_LENGTH, "miles")) if fmt_num(r.TOR_LENGTH, "miles") else None,
                            ("maximum path width " + fmt_num(r.TOR_WIDTH, "yards")) if fmt_num(r.TOR_WIDTH, "yards") else None)
                if x]
        if dims:
            head += " Survey: " + "; ".join(dims) + "."
        state = head + "\n\n" + nar
        recs.append({"rid": f"stormevents-{r.EVENT_ID}", "state": state, "narr": nar, "label": lab,
                     "year": int(r.YEAR), "episode": str(r.EPISODE_ID)})
    stats["candidates"] = len(recs)

    rng = random.Random(SEED)
    recs.sort(key=lambda x: x["rid"])
    rng.shuffle(recs)
    nd = C.NearDup(thr=0.7)
    kept = []
    for x in recs:
        if nd.seen(x["narr"]):
            stats["drop_near_dup"] += 1
            continue
        kept.append(x)

    # sample per class over a generous pool, then decontaminate the pool, then cap
    pools = collections.defaultdict(list)
    for x in kept:
        pools[x["label"]].append(x)
    pool = []
    for lab, xs in pools.items():
        pool += xs[: int(CAPS[lab] * 1.3) + 50]
    hits = C.decon({x["rid"]: [x["narr"]] for x in pool}, KEY)
    hits.update(C.cross_v14({x["rid"]: [x["narr"]] for x in pool}, {KEY}))
    stats["drop_decon"] = len(hits)
    pool = [x for x in pool if x["rid"] not in hits]
    per = collections.defaultdict(list)
    for x in pool:
        per[x["label"]].append(x)
    chosen = []
    for lab in sorted(per):
        chosen += per[lab][: CAPS[lab]]

    rows = []
    for x in chosen:
        nar = x["narr"]
        edge = []
        if x["label"] == "EFU":
            edge.append("missing_info")
        if MPH.search(nar):
            edge.append("numeric")
        if C.neg_count(nar) >= 1:
            edge.append("negation")
        if len(x["state"]) > 2500:
            edge.append("long_context")
        rows.append({
            "key": KEY,
            "rid": x["rid"],
            "state": x["state"],
            "instructions": QUESTION,
            "options": LEVELS,
            "gold": LABEL2OPT[x["label"]],
            "soft": None,
            "meta": {
                "dataset": DATASET,
                "config": "EVENT_TYPE=Tornado, single-segment, EVENT_NARRATIVE with explicit EF ratings redacted",
                "revision": "; ".join(f"{n}:sha256:{s}" for n, s in list(FILES.items())[:1]) +
                            f"; ... ({len(FILES)} yearly files, all sha256-pinned in build_storm_ef.py)",
                "licence": LICENCE,
                "split": "train",
                "orig_label": {"TOR_F_SCALE": x["label"], "year": x["year"], "episode_id": x["episode"]},
                "family": C.FAMILY,
                "edge": C.edge_join(edge),
                "seed": SEED,
            },
        })
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, {None: DEFS})
    print(dict(stats))
    st = C.summary(KEY, rows)
    C.show_samples(rows, n=5, seed=11)
    rec = C.manifest_record(
        KEY, DATASET, LICENCE, rows, "choice (7-level ordinal: EFU, EF0-EF5)",
        "NWS damage-survey narratives of single-segment US tornadoes 2007-2024; decide the official EF rating (EFU = "
        "no rateable damage); explicit rating mentions redacted, wind estimates / damage indicators / path size kept; "
        "EF0 rows that state or show no damage dropped for EFU consistency; review fixes: narratives naming another "
        "county/parish/state or a different total path length dropped, wind estimates in mph/miles per hour/knots "
        "checked against the EF band; capped per class (EF3-EF5 all kept).",
        st)
    return rows, rec


if __name__ == "__main__":
    rows, rec = main()
    if "--manifest" in sys.argv:
        C.append_manifest(rec)
        print("manifest record appended")
