"""usgs.py: metadata mapper for md_usgs (USGS Earthquake Catalog, ComCat; US public domain; geoscience / natural hazards).

Upstream fields used as targets: mag, magType, type, tsunami, felt, alert, net, sig, time, place, nst, gap, depth and the
epicentre latitude / longitude. All gold is a program function of the printed fields. Event pages, names and free text are
not used.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from _common_a import (COUNT_NEG, COUNT_POS, EQ_NEG, EQ_POS, Task, bool_task, bucket_task, concept_task, eq_task, ge_task, yn_card)

NAME = "usgs"
DOMAIN = "geoscience_hazards"
LICENCE = "US Public Domain (USGS-authored data; ComCat via fdsnws event service)"
HEADERS = ["Earthquake catalogue entry", "Seismic event record", "Event summary from a seismic network catalogue", "Catalogue row for a seismic event"]
RAW = Path(__file__).resolve().parent.parent / "raw_a" / "usgs" / "events.json"
GROUPS = {"magnitude": "mag", "significance": "mag", "latitude": "geo", "longitude": "geo", "place": "geo", "origin_time": "time"}
MAG_POS = ["Is the magnitude {n} or higher?", "Does the event have a magnitude of at least {n}?", "Is the reported magnitude at least {n}?"]
MAG_NEG = ["Is the magnitude below {n}?", "Is the reported magnitude less than {n}?", "Does the event have a magnitude lower than {n}?"]
DEPTH_POS = ["Is the focal depth {n} km or more?", "Does the event lie at a depth of at least {n} km?", "Is the depth at least {n} km?"]
DEPTH_NEG = ["Is the focal depth less than {n} km?", "Is the depth below {n} km?", "Does the event lie at a depth of less than {n} km?"]


def load():
    return [e for e in json.loads(RAW.read_text()) if e["mag"] is not None and e["depth"] is not None and e["lat"] is not None]


def rid_of(r):
    return r["id"]


def group_of(k):
    return GROUPS.get(k, k)


def dt(r):
    return datetime.fromtimestamp(r["time"] / 1000, tz=timezone.utc)


def region(r):
    p = r["place"] or ""
    return p.rsplit(",", 1)[-1].strip() if "," in p else None


def dist(r):
    m = re.match(r"(\d+) km ", r["place"] or "")
    return int(m.group(1)) if m else None


def fields_of(r):
    return {
        "event_id": ("Event ID", r["id"]), "magnitude": ("Magnitude", f"{r['mag']:.1f}"), "magnitude_type": ("Magnitude type", r["magType"]),
        "event_type": ("Event type", r["type"]), "tsunami_flag": ("Tsunami flag", str(r["tsunami"])),
        "felt_reports": ("Felt reports", str(r["felt"]) if r["felt"] is not None else "none recorded"),
        "pager_alert": ("PAGER alert", r["alert"] or "none"), "network": ("Contributing network", r["net"]),
        "significance": ("Significance score", str(r["sig"])), "origin_time": ("Origin time (UTC)", dt(r).strftime("%Y-%m-%d %H:%M:%S")),
        "place": ("Location description", r["place"]), "latitude": ("Latitude", f"{r['lat']:.3f}"), "longitude": ("Longitude", f"{r['lon']:.3f}"),
        "depth_km": ("Depth (km)", f"{r['depth']:.1f}"), "azimuthal_gap": ("Azimuthal gap (deg)", str(int(r["gap"])) if r["gap"] is not None else None),
        "stations": ("Stations used", str(r["nst"]) if r["nst"] is not None else None),
    }


def M(r):
    return round(r["mag"], 1)


def tasks():
    T = []
    add = T.append
    for thr in (4.0, 5.0, 5.5, 6.0, 6.5, 7.0):
        add(ge_task(f"us_mag_ge_{thr}", ["magnitude"], lambda r: M(r), thr, pos=MAG_POS, neg=MAG_NEG, why=f"mag >= {thr}"))
    for thr in (10, 35, 70, 150, 300):
        add(ge_task(f"us_depth_ge_{thr}", ["depth_km"], lambda r: round(r["depth"], 1), thr, pos=DEPTH_POS, neg=DEPTH_NEG, why=f"depth >= {thr} km"))
    for thr in (100, 250, 500, 1000):
        add(ge_task(f"us_sig_ge_{thr}", ["significance"], lambda r: r["sig"], thr, fmt={"things": "significance points", "thing": "significance"},
                    why=f"sig >= {thr}"))
    for thr in (10, 100):
        add(ge_task(f"us_felt_ge_{thr}", ["felt_reports"], lambda r: r["felt"], thr, elig=lambda r: r["felt"] is not None,
                    fmt={"things": "felt reports", "thing": "felt-report"}, why=f"felt >= {thr}"))
    add(ge_task("us_stations_ge_50", ["stations"], lambda r: r["nst"], 50, elig=lambda r: r["nst"] is not None,
                fmt={"things": "stations used", "thing": "station"}, why="nst >= 50"))
    add(ge_task("us_gap_ge_180", ["azimuthal_gap"], lambda r: r["gap"], 180, elig=lambda r: r["gap"] is not None,
                pos=["Is the azimuthal gap {n} degrees or more?", "Does the azimuthal gap reach at least {n} degrees?"],
                neg=["Is the azimuthal gap less than {n} degrees?", "Is the azimuthal gap below {n} degrees?"], why="gap >= 180"))
    add(bool_task("us_tsunami_flag", ["tsunami_flag"], lambda r: r["tsunami"] == 1, "", ["Is the tsunami flag set to 1?", "Does the entry carry a tsunami flag of 1?"],
                  ["Is it true that the tsunami flag is not 1?", "Is it true that the entry does not carry a tsunami flag of 1?"], why="tsunami == 1"))
    add(bool_task("us_has_alert", ["pager_alert"], lambda r: r["alert"] is not None, "", ["Does the entry have a PAGER alert level?", "Is a PAGER alert level recorded for the event?"],
                  ["Is it true that no PAGER alert level is recorded for the event?", "Is it true that the PAGER alert reads none?"], why="alert is not null"))
    for v in ("us", "ak", "pr", "nc", "ci"):
        add(eq_task(f"us_net_is_{v}", ["network"], lambda r: r["net"], v, "contributing network code", why=f"net == {v}"))
    for v in ("mb", "ml", "mww", "md"):
        add(eq_task(f"us_magtype_is_{v}", ["magnitude_type"], lambda r: r["magType"], v, "magnitude type", why=f"magType == {v}"))
    add(eq_task("us_type_is_earthquake", ["event_type"], lambda r: r["type"], "earthquake", "event type", why="type == earthquake"))
    add(bool_task("us_north", ["latitude"], lambda r: r["lat"] > 0, "", ["Is the epicentre in the northern hemisphere (latitude above 0)?", "Is the latitude positive?"],
                  ["Is it true that the epicentre is not in the northern hemisphere (latitude above 0)?", "Is it true that the latitude is not positive?"], why="lat > 0"))
    add(bool_task("us_east", ["longitude"], lambda r: r["lon"] > 0, "", ["Is the epicentre east of the prime meridian (longitude above 0)?", "Is the longitude positive?"],
                  ["Is it true that the epicentre is not east of the prime meridian (longitude above 0)?", "Is it true that the longitude is not positive?"], why="lon > 0"))
    add(bool_task("us_tropics", ["latitude"], lambda r: abs(r["lat"]) <= 23.4, "", ["Is the epicentre inside the tropical band (absolute latitude up to 23.4)?",
                                                                                 "Does the absolute latitude stay within 23.4 degrees?"],
                  ["Is it true that the epicentre is not inside the tropical band (absolute latitude up to 23.4)?", "Is it true that the absolute latitude does not stay within 23.4 degrees?"],
                  why="abs(lat) <= 23.4"))
    add(bool_task("us_weekend", ["origin_time"], lambda r: dt(r).weekday() >= 5, "", ["Did the origin time (UTC) fall on a Saturday or Sunday?", "Was the event on a weekend in UTC?"],
                  ["Is it true that the origin time (UTC) did not fall on a Saturday or Sunday?", "Is it true that the event was not on a weekend in UTC?"], why="weekday >= 5"))
    add(bool_task("us_first_half_year", ["origin_time"], lambda r: dt(r).month <= 6, "", ["Did the event occur in January to June (UTC)?", "Is the origin month between January and June?"],
                  ["Is it true that the event did not occur in January to June (UTC)?", "Is it true that the origin month is not between January and June?"], why="month <= 6"))
    add(bool_task("us_first_half_day", ["origin_time"], lambda r: dt(r).hour < 12, "", ["Did the event occur from 00:00 to 11:59 UTC?", "Is the origin hour between 0 and 11 UTC?"],
                  ["Is it true that the event did not occur from 00:00 to 11:59 UTC?", "Is it true that the origin hour is not between 0 and 11 UTC?"], why="hour < 12"))
    add(bool_task("us_m5_deep", ["magnitude", "depth_km"], lambda r: M(r) >= 5.0 and r["depth"] >= 70, "",
                  ["Is the magnitude at least 5.0 while the depth is 70 km or more?", "Does the event have both a magnitude of 5.0 or higher and a depth of 70 km or more?"],
                  ["Is it true that the event does not have both a magnitude of 5.0 or higher and a depth of 70 km or more?"], why="mag >= 5 and depth >= 70"))
    add(bool_task("us_m55_felt10", ["magnitude", "felt_reports"], lambda r: M(r) >= 5.5 and r["felt"] >= 10, "", ["Is the magnitude at least 5.5 while 10 or more felt reports were filed?",
                  "Does the event have both a magnitude of 5.5 or higher and 10 or more felt reports?"],
                  ["Is it true that the event does not have both a magnitude of 5.5 or higher and 10 or more felt reports?"], elig=lambda r: r["felt"] is not None,
                  why="mag >= 5.5 and felt >= 10"))
    add(bool_task("us_m6_tsunami", ["magnitude", "tsunami_flag"], lambda r: M(r) >= 6.0 and r["tsunami"] == 1, "",
                  ["Is the magnitude at least 6.0 while the tsunami flag is 1?", "Does the event have both a magnitude of 6.0 or higher and a tsunami flag of 1?"],
                  ["Is it true that the event does not have both a magnitude of 6.0 or higher and a tsunami flag of 1?"], why="mag >= 6 and tsunami == 1"))
    for v in ("Japan", "Indonesia", "Chile", "Alaska", "Philippines", "Tonga"):
        add(eq_task(f"us_region_is_{v.lower()}", ["place"], region, v, "last comma-separated part of the location description",
                    elig=lambda r: region(r) is not None, why=f"place.rsplit(',')[-1] == {v}"))
    for thr in (25, 100, 200):
        add(ge_task(f"us_dist_ge_{thr}", ["place"], dist, thr, elig=lambda r: dist(r) is not None,
                    pos=["Does the location description put the epicentre {n} km or more from the named place?", "Is the stated distance to the named place at least {n} km?"],
                    neg=["Does the location description put the epicentre less than {n} km from the named place?", "Is the stated distance to the named place below {n} km?"],
                    why=f"leading distance in place >= {thr}"))
    # carded concepts
    add(concept_task("us_c_shallow", ["depth_km"], lambda r: r["depth"] <= 70, "a shallow-focus event", yn_card("the depth is 70 km or less", "the depth is more than 70 km"), why="depth <= 70"))
    add(concept_task("us_c_very_shallow", ["depth_km"], lambda r: r["depth"] <= 20, "a very shallow event", yn_card("the depth is 20 km or less", "the depth is more than 20 km"), why="depth <= 20"))
    add(concept_task("us_c_strong", ["magnitude"], lambda r: M(r) >= 6.0, "a strong earthquake", yn_card("the magnitude is 6.0 or higher", "the magnitude is below 6.0"), why="mag >= 6"))
    add(concept_task("us_c_felt_widely", ["felt_reports"], lambda r: r["felt"] >= 100, "widely felt", yn_card("100 or more felt reports were filed", "fewer than 100 felt reports were filed"),
                     elig=lambda r: r["felt"] is not None, why="felt >= 100"))
    add(concept_task("us_c_significant", ["significance"], lambda r: r["sig"] >= 600, "a significant event", yn_card("the significance score is 600 or more", "the significance score is below 600"), why="sig >= 600"))
    add(concept_task("us_c_well_recorded", ["stations"], lambda r: r["nst"] >= 40, "well recorded", yn_card("40 or more stations were used", "fewer than 40 stations were used"),
                     elig=lambda r: r["nst"] is not None, why="nst >= 40"))
    add(concept_task("us_c_damaging", ["magnitude", "depth_km"], lambda r: M(r) >= 5.5 and r["depth"] <= 70, "potentially damaging",
                     yn_card("the magnitude is 5.5 or higher and the depth is 70 km or less", "the magnitude is below 5.5 or the depth is more than 70 km"), why="mag >= 5.5 and depth <= 70"))
    add(concept_task("us_c_poor_coverage", ["azimuthal_gap"], lambda r: r["gap"] >= 180, "poorly covered by stations", yn_card("the azimuthal gap is 180 degrees or more", "the azimuthal gap is below 180 degrees"),
                     elig=lambda r: r["gap"] is not None, why="gap >= 180"))
    # choice heads
    add(bucket_task("us_ch_depth_class", ["depth_km"], lambda r: "shallow" if r["depth"] < 70 else "intermediate" if r["depth"] < 300 else "deep", ["shallow", "intermediate", "deep"],
                    "depth class", defs=[("shallow", "Pick this when the depth is under 70 km."), ("intermediate", "Pick this when the depth is from 70 km up to under 300 km."),
                                         ("deep", "Pick this when the depth is 300 km or more.")], why="depth bins"))
    add(bucket_task("us_ch_mag_class", ["magnitude"], lambda r: "minor" if M(r) < 4 else "light" if M(r) < 5 else "moderate" if M(r) < 6 else "strong" if M(r) < 7 else "major",
                    ["minor", "light", "moderate", "strong", "major"], "magnitude class",
                    defs=[("minor", "Pick this when the magnitude is below 4.0."), ("light", "Pick this for 4.0 up to below 5.0."), ("moderate", "Pick this for 5.0 up to below 6.0."),
                          ("strong", "Pick this for 6.0 up to below 7.0."), ("major", "Pick this for 7.0 or higher.")], why="mag bins"))
    add(bucket_task("us_ch_quadrant", ["latitude", "longitude"], lambda r: ("north" if r["lat"] > 0 else "south") + ("east" if r["lon"] > 0 else "west"),
                    ["northeast", "northwest", "southeast", "southwest"], "map quadrant", ordered=False, k=4,
                    defs=[("northeast", "Pick this when latitude is above 0 and longitude is above 0."), ("northwest", "Pick this when latitude is above 0 and longitude is 0 or below."),
                          ("southeast", "Pick this when latitude is 0 or below and longitude is above 0."), ("southwest", "Pick this when latitude is 0 or below and longitude is 0 or below.")],
                    why="signs of lat, lon"))
    add(bucket_task("us_ch_network", ["network"], lambda r: r["net"], ["us", "ak", "pr", "nc", "ci"], "contributing network code", ordered=False, k=4, why="net"))
    mt = {"mb": "body-wave", "ml": "local", "md": "local", "mww": "moment", "mwr": "moment", "mwc": "moment", "mw": "moment"}
    add(bucket_task("us_ch_magtype_group", ["magnitude_type"], lambda r: mt[r["magType"]], ["body-wave", "local", "moment"], "magnitude scale family", ordered=False, k=3,
                    elig=lambda r: r["magType"] in mt, defs=[("body-wave", "Pick this when the magnitude type is mb."), ("local", "Pick this when the type is ml or md."),
                                                              ("moment", "Pick this when the type is mww, mwr, mwc or mw.")], why="magType -> family"))
    add(bucket_task("us_ch_alert", ["pager_alert"], lambda r: r["alert"], ["green", "yellow", "orange", "red"], "PAGER alert level", ordered=False, k=4,
                    elig=lambda r: r["alert"] is not None, why="alert"))
    add(bucket_task("us_ch_sig_class", ["significance"], lambda r: "minor" if r["sig"] < 100 else "notable" if r["sig"] < 300 else "important" if r["sig"] < 600 else "major",
                    ["minor", "notable", "important", "major"], "significance class",
                    defs=[("minor", "Pick this when the score is below 100."), ("notable", "Pick this for 100 up to below 300."), ("important", "Pick this for 300 up to below 600."),
                          ("major", "Pick this for 600 or more.")], why="sig bins"))
    add(bucket_task("us_ch_season", ["origin_time"], lambda r: {12: "Dec-Feb", 1: "Dec-Feb", 2: "Dec-Feb", 3: "Mar-May", 4: "Mar-May", 5: "Mar-May", 6: "Jun-Aug", 7: "Jun-Aug", 8: "Jun-Aug",
                                                                    9: "Sep-Nov", 10: "Sep-Nov", 11: "Sep-Nov"}[dt(r).month], ["Dec-Feb", "Mar-May", "Jun-Aug", "Sep-Nov"],
                    "three-month block of the origin date (UTC)", ordered=False, k=4, why="month -> block"))
    add(bucket_task("us_ch_utc_slot", ["origin_time"], lambda r: "00-05" if dt(r).hour < 6 else "06-11" if dt(r).hour < 12 else "12-17" if dt(r).hour < 18 else "18-23",
                    ["00-05", "06-11", "12-17", "18-23"], "six-hour UTC slot", why="hour bins"))
    add(bucket_task("us_ch_dist_class", ["place"], lambda r: "within 10 km" if dist(r) <= 10 else "11 to 50 km" if dist(r) <= 50 else "51 to 150 km" if dist(r) <= 150 else "over 150 km",
                    ["within 10 km", "11 to 50 km", "51 to 150 km", "over 150 km"], "distance class of the named place", elig=lambda r: dist(r) is not None,
                    defs=[("within 10 km", "Pick this when the stated distance is 10 km or less."), ("11 to 50 km", "Pick this for 11 to 50 km."), ("51 to 150 km", "Pick this for 51 to 150 km."),
                          ("over 150 km", "Pick this for more than 150 km.")], why="leading distance bins"))
    return T
