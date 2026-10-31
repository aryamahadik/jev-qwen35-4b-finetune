#!/usr/bin/env python3
"""A42-D 12 G-proxy builder (CPU only, no network, no model). NEVER TRAINED ON.

Reads the three upstream snapshots in raw/ (fetched 15 Oct 2026, see SOURCES.json) and writes
  lean/data/c2_gproxy/gproxy_rows.jsonl   one yes/no row per record (C2 row format, plus meta.source / source_doc / dataset)
  lean/data/c2_gproxy/gproxy_build_report.json
Run from lean/c2_build:  nice -n 10 ../../.venv/bin/python -B meta_src/gproxy/build.py

Design (all by construction, nothing relabelled):
  * Sources: gp_ourairports (aviation), gp_wwpdb (structural biology), gp_eurostat (official statistics).
  * A TASK is a few question VARIANTS. Each variant has its own predicate over a record (for example "elevation above
    2000 ft" and "elevation 2000 ft or lower"); gold = the variant's predicate on the record, computed by program from the
    upstream fields that the row's state shows. No negation word is used in any wording (A43 f holds trivially); every
    wording is still run through c2_kit.polarity.problems and a failing variant would be dropped before sampling.
  * Per slot the variant and the wanted gold are drawn from hashes of (task, slot) only, then a record is drawn from the
    matching pool, so the question wording carries no information about the gold beyond the record itself.
  * Style: 'card' rows state the rule in a two-line card (- yes: / - no:, swap-safe, no negation word) and ask a short
    question about a defined term; 'free' rows (card-free) put the rule in the question. Card-free share >= 30% per source.
  * Yes share 40-50% per source (hash-dithered per task), none above 40% of rows, one row per upstream record,
    cluster = meta.source_doc (airport ident / PDB id / Eurostat dataset+country).
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE.parents[1]
LEAN = BUILD.parent
sys.path.insert(0, str(BUILD))
from c2_kit import polarity  # noqa: E402  (kit polarity checks, read-only import)

SEED = "gproxy-v1-15oct2026"
OUT = LEAN / "data" / "c2_gproxy" / "gproxy_rows.jsonl"
REPORT = LEAN / "data" / "c2_gproxy" / "gproxy_build_report.json"
SNAPSHOT = "2026-10-15"
SCALE = 1.2                          # row-count multiplier on every task (>= 2,000 rows after the noise check)
SRC_SCALE = {"gp_wwpdb": 1.0}      # PDB pair-base tasks are extra; keeps every source well under 40%
CARD_SHARE = 0.7                    # share of card-able slots that get a card (card-free share is then >= 45% of those)
YES_TARGET = 0.46
GPROXY_LICENCE = "see meta.source_licence (upstream licence verified 15 Oct 2026; never trained)"


def H(*parts) -> int:
    return int(hashlib.sha256("|".join(str(p) for p in (SEED,) + parts).encode()).hexdigest()[:12], 16)


def U(*parts) -> float:
    return H(*parts) / float(16 ** 12)


def sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def fmt_num(x: float) -> str:
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    return f"{x:g}"


# ---------------------------------------------------------------------------------------------------------- sources
SOURCES = json.loads((HERE / "SOURCES.json").read_text())["sources"]
SRC = {s["id"]: s for s in SOURCES}

CONT = {"EU": "Europe", "NA": "North America", "AS": "Asia", "AF": "Africa", "SA": "South America", "OC": "Oceania"}


def load_airports() -> list:
    recs, seen = [], set()
    with open(HERE / "raw/ourairports/airports.csv", encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            if not r["ident"] or r["ident"] in seen:
                continue
            seen.add(r["ident"])
            try:
                lat, lon = float(r["latitude_deg"]), float(r["longitude_deg"])
            except ValueError:
                continue
            el = r["elevation_ft"].strip()
            try:
                elev = float(el) if el else None
            except ValueError:
                elev = None
            recs.append({"key": r["ident"], "doc": "ourairports:" + r["ident"], "ident": r["ident"], "name": r["name"].strip(),
                         "type": r["type"], "lat": lat, "lon": lon, "elev": elev, "cont": r["continent"],
                         "country": r["iso_country"], "region": r["iso_region"], "muni": r["municipality"].strip(),
                         "sched": r["scheduled_service"], "iata": r["iata_code"].strip()})
    return recs


def load_pdb() -> list:
    recs = []
    lines = (HERE / "raw/wwpdb/entries.idx").read_text(encoding="utf-8", errors="replace").split("\n")
    for ln in lines[2:]:
        p = ln.split("\t")
        if len(p) < 8 or not re.fullmatch(r"[0-9A-Z]{4}", p[0]):
            continue
        m = re.fullmatch(r"(\d\d)/(\d\d)/(\d\d)", p[2].strip())
        if not m:
            continue
        yy = int(m.group(3))
        year = 1900 + yy if yy >= 70 else 2000 + yy
        try:
            res = float(p[6]) if p[6].strip() else None
        except ValueError:
            res = None
        if res is not None and res <= 0:
            res = None
        recs.append({"key": p[0], "doc": "wwpdb:" + p[0], "id": p[0], "klass": p[1].strip(), "date": f"{year}-{m.group(1)}-{m.group(2)}",
                     "year": year, "title": p[3].strip(), "org": p[4].strip(), "res": res, "exp": p[7].strip()})
    return recs


EURO_SKIP_GEO = {"EU", "EA"}


def load_eurostat() -> list:
    recs = []
    for fp in sorted((HERE / "raw/eurostat").glob("*.json")):
        d = json.loads(fp.read_text())
        if "id" not in d:
            continue
        ids, size = d["id"], d["size"]
        pos, lab = {}, {}
        for dim in ids:
            c = d["dimension"][dim]["category"]
            idx = c["index"]
            if isinstance(idx, list):
                idx = {k: i for i, k in enumerate(idx)}
            pos[dim] = {k: v for k, v in idx.items()}
            lab[dim] = c.get("label", {})
        strides, s = {}, 1
        for dim, n in reversed(list(zip(ids, size))):
            strides[dim] = s
            s *= n
        inv = {dim: {v: k for k, v in pos[dim].items()} for dim in ids}
        vals = d["value"]
        items = vals.items() if isinstance(vals, dict) else enumerate(vals)
        code = fp.stem
        for flat, v in items:
            if v is None:
                continue
            flat = int(flat)
            cats = {}
            rem = flat
            for dim, n in zip(ids, size):
                cats[dim] = inv[dim][(flat // strides[dim]) % n]
            geo = cats.get("geo", "")
            if len(geo) != 2 or geo in EURO_SKIP_GEO or not re.fullmatch(r"\d{4}", cats.get("time", "")):
                continue
            series = tuple((dim, cats[dim]) for dim in ids if dim not in ("geo", "time", "freq"))
            sdesc = [(d["dimension"][dim].get("label", dim), lab[dim].get(c, c)) for dim, c in series]
            recs.append({"ds": code, "key": f"{code}|{sha(str(series))[:6]}|{geo}|{cats['time']}", "doc": f"eurostat:{code}:{geo}",
                         "title": d["label"], "series": series, "sdesc": sdesc, "geo": geo,
                         "geo_name": lab["geo"].get(geo, geo), "year": int(cats["time"]), "v": float(v)})
    return recs


# ---------------------------------------------------------------------------------------------------------- tasks
def airport_state(r: dict) -> str:
    return (f"Airport record (OurAirports registry).\nName: {r['name']}\nIdent: {r['ident']}\nType: {r['type']}\n"
            f"Municipality: {r['muni'] or 'unknown'}; country: {r['country']}; region: {r['region']}; continent: {r['cont']}\n"
            f"Latitude: {r['lat']:g}; longitude: {r['lon']:g}\n"
            f"Field elevation (ft): {fmt_num(r['elev']) if r['elev'] is not None else 'unknown'}\n"
            f"Scheduled service: {r['sched']}\nIATA code: {r['iata'] or 'none'}")


def pdb_state(r: dict) -> str:
    return (f"Protein Data Bank entry {r['id']} (wwPDB entry index).\nTitle: {r['title']}\nClassification: {r['klass']}\n"
            f"Deposition date: {r['date']}\nSource organism: {r['org'] or 'missing'}\n"
            f"Reported resolution (Angstrom): {fmt_num(r['res']) if r['res'] is not None else 'missing'}\n"
            f"Experimental method: {r['exp']}")


def euro_head(r: dict) -> str:
    lines = [f"Eurostat table {r['ds']}: {r['title']}."]
    for k, v in r["sdesc"]:
        lines.append(f"{k}: {v}")
    return "\n".join(lines)


def V(free, pred, card=None):
    """One question variant. free = wording with the rule inside; card = (core question, yes line, no line) or None."""
    return {"free": free, "pred": pred, "card": card}


def airport_tasks() -> list:
    T = []
    big = lambda r: r["type"] in ("large_airport", "medium_airport")
    T.append(dict(id="A.sched", n=48, elig=lambda r: True, variants=[
        V("Does this airport have scheduled commercial service?", lambda r: r["sched"] == "yes",
          ("Does this airport have regular airline service?", "The record lists scheduled service as yes.", "The record lists scheduled service as no."))]))
    for t in (500, 1000, 2000, 3000, 5000, 7000):
        T.append(dict(id=f"A.elev{t}", n=36, elig=lambda r: r["elev"] is not None, variants=[
            V(f"Is the field elevation above {t} ft?", lambda r, t=t: r["elev"] > t,
              ("Is this airport located at a high altitude?", f"The field elevation is above {t} ft.", f"The field elevation is {t} ft or lower.")),
            V(f"Is the field elevation {t} ft or lower?", lambda r, t=t: r["elev"] <= t,
              ("Is this airport located at a low altitude?", f"The field elevation is {t} ft or lower.", f"The field elevation is above {t} ft."))]))
    T.append(dict(id="A.major", n=60, elig=lambda r: True, variants=[
        V("Is this a large or medium airport?", big,
          ("Is this airport a major airport?", "The airport type is large_airport or medium_airport.", "The airport type is small_airport, heliport, seaplane_base, balloonport or closed.")),
        V("Is this record a small airport, heliport, seaplane base, balloonport or closed airport?", lambda r: not big(r),
          ("Is this airport a minor airport?", "The airport type is small_airport, heliport, seaplane_base, balloonport or closed.", "The airport type is large_airport or medium_airport."))]))
    T.append(dict(id="A.iata", n=50, elig=lambda r: True, variants=[
        V("Does this airport have an IATA code?", lambda r: bool(r["iata"]),
          ("Does this airport have an airline code?", "The IATA code field is filled.", "The IATA code field is empty.")),
        V("Is the IATA code field of this airport empty?", lambda r: not r["iata"],
          ("Is this airport without an airline code?", "The IATA code field is empty.", "The IATA code field is filled."))]))
    T.append(dict(id="A.north", n=40, elig=lambda r: r["lat"] != 0, variants=[
        V("Is this airport in the Northern Hemisphere?", lambda r: r["lat"] > 0,
          ("Is this airport a northern airport?", "The latitude is above 0 degrees.", "The latitude is below 0 degrees.")),
        V("Is this airport in the Southern Hemisphere?", lambda r: r["lat"] < 0,
          ("Is this airport a southern airport?", "The latitude is below 0 degrees.", "The latitude is above 0 degrees."))]))
    T.append(dict(id="A.east", n=30, elig=lambda r: r["lon"] != 0, variants=[
        V("Is this airport in the Eastern Hemisphere?", lambda r: r["lon"] > 0, None),
        V("Is this airport in the Western Hemisphere?", lambda r: r["lon"] < 0, None)]))
    for c, nm in CONT.items():
        T.append(dict(id=f"A.cont{c}", n=24, elig=lambda r: True, variants=[V(f"Is this airport located in {nm}?", lambda r, c=c: r["cont"] == c, None)]))
    for c in ("EU", "NA", "AS"):
        T.append(dict(id=f"A.majorcont{c}", n=26, elig=lambda r: True, variants=[
            V(f"Is this a large or medium airport in {CONT[c]}?", lambda r, c=c: big(r) and r["cont"] == c, None)]))
    T.append(dict(id="A.closed", n=30, elig=lambda r: True, variants=[V("Is this airport record marked as closed?", lambda r: r["type"] == "closed", None)]))
    T.append(dict(id="A.heli", n=30, elig=lambda r: True, variants=[V("Is this record a heliport?", lambda r: r["type"] == "heliport", None)]))
    T.append(dict(id="A.schedhigh", n=40, elig=lambda r: r["elev"] is not None, variants=[
        V("Does this airport have scheduled service and a field elevation above 1000 ft?", lambda r: r["sched"] == "yes" and r["elev"] > 1000, None)]))
    return T


def pb(tid, n, elig, core, pred, yes, no):
    """Card-only task whose core question has a DO / COP / HAVE / MOD shape that negtwins parses (bases for the 150 pairs)."""
    return dict(id=tid, n=n, card_only=True, elig=elig, variants=[V(core, pred, (core, yes, no))])


def airport_pair_tasks() -> list:
    a = lambda r: True
    el = lambda r: r["elev"] is not None
    ALL = "large_airport, medium_airport, small_airport, heliport, seaplane_base or balloonport"
    return [
        pb("A.pb.iata_list", 12, a, "Does this airport list an IATA code?", lambda r: bool(r["iata"]), "The IATA code field is filled.", "The IATA code field is empty."),
        pb("A.pb.elev_show", 12, a, "Does this record show a field elevation?", lambda r: r["elev"] is not None, "The field elevation is given.", "The field elevation is unknown."),
        pb("A.pb.muni_name", 12, a, "Does this record name a municipality?", lambda r: bool(r["muni"]), "The municipality field is filled.", "The municipality field is unknown."),
        pb("A.pb.sched_offer", 12, a, "Does this airport offer scheduled service?", lambda r: r["sched"] == "yes", "The record lists scheduled service as yes.", "The record lists scheduled service as no."),
        pb("A.pb.sched_provide", 12, a, "Does this airport provide scheduled service?", lambda r: r["sched"] == "yes", "The record lists scheduled service as yes.", "The record lists scheduled service as no."),
        pb("A.pb.elev_state", 12, el, "Does this record state an elevation above 1000 ft?", lambda r: r["elev"] > 1000, "The field elevation is above 1000 ft.", "The field elevation is 1000 ft or lower."),
        pb("A.pb.iata_listed", 12, a, "Is an IATA code listed for this airport?", lambda r: bool(r["iata"]), "The IATA code field is filled.", "The IATA code field is empty."),
        pb("A.pb.elev_given", 12, a, "Is a field elevation given for this airport?", lambda r: r["elev"] is not None, "The field elevation is given.", "The field elevation is unknown."),
        pb("A.pb.sched_avail", 12, a, "Is scheduled service available at this airport?", lambda r: r["sched"] == "yes", "The record lists scheduled service as yes.", "The record lists scheduled service as no."),
        pb("A.pb.located_eu", 12, a, "Is this record located in Europe?", lambda r: r["cont"] == "EU", "The continent field is EU.", "The continent field is NA, AS, AF, SA, OC or AN."),
        pb("A.pb.closed", 12, a, "Is this record closed?", lambda r: r["type"] == "closed", "The airport type is closed.", "The airport type is " + ALL + "."),
        pb("A.pb.handle", 12, a, "Can this airport handle scheduled flights?", lambda r: r["sched"] == "yes", "The record lists scheduled service as yes.", "The record lists scheduled service as no."),
        pb("A.pb.been_closed", 12, a, "Has this record been marked as closed?", lambda r: r["type"] == "closed", "The airport type is closed.", "The airport type is " + ALL + "."),
        pb("A.pb.been_given", 12, a, "Has this airport been given an IATA code?", lambda r: bool(r["iata"]), "The IATA code field is filled.", "The IATA code field is empty."),
    ]


def pdb_pair_tasks() -> list:
    a = lambda r: True
    xray, em, nmr = "X-RAY DIFFRACTION", "ELECTRON MICROSCOPY", "SOLUTION NMR"
    single = lambda r: r["exp"] in (xray, em, nmr)
    word = lambda w: (lambda r: re.search(r"(?<![A-Z0-9])" + w + r"(?![A-Z0-9])", r["title"].upper()) is not None)
    return [
        pb("P.pb.res_report", 10, a, "Does this entry report a resolution?", lambda r: r["res"] is not None, "A resolution value is given.", "The resolution field is missing."),
        pb("P.pb.org_list", 10, a, "Does this entry list a source organism?", lambda r: bool(r["org"]), "The source organism field is filled.", "The source organism field is missing."),
        pb("P.pb.title_include", 10, a, "Does the title include the word KINASE?", word("KINASE"), "The title contains the word KINASE.", "The word KINASE is absent from the title."),
        pb("P.pb.title_mention", 10, a, "Does the title mention the word COMPLEX?", word("COMPLEX"), "The title contains the word COMPLEX.", "The word COMPLEX is absent from the title."),
        pb("P.pb.res_show", 10, lambda r: r["res"] is not None, "Does this entry show a resolution below 2.0 Angstrom?", lambda r: r["res"] < 2.0, "The reported resolution is below 2.0 Angstrom.", "The reported resolution is 2.0 Angstrom or more."),
        pb("P.pb.method_state", 10, single, "Does this record state X-ray diffraction as the method?", lambda r: r["exp"] == xray, "The experimental method is X-RAY DIFFRACTION.", "The experimental method is ELECTRON MICROSCOPY or SOLUTION NMR."),
        pb("P.pb.res_reported", 10, a, "Is a resolution reported for this structure?", lambda r: r["res"] is not None, "A resolution value is given.", "The resolution field is missing."),
        pb("P.pb.org_listed", 10, a, "Is the source organism listed for this entry?", lambda r: bool(r["org"]), "The source organism field is filled.", "The source organism field is missing."),
        pb("P.pb.based_em", 10, single, "Is this entry based on electron microscopy?", lambda r: r["exp"] == em, "The experimental method is ELECTRON MICROSCOPY.", "The experimental method is X-RAY DIFFRACTION or SOLUTION NMR."),
        pb("P.pb.been_dep", 10, a, "Has this entry been deposited after 2010?", lambda r: r["year"] > 2010, "The deposition year is after 2010.", "The deposition year is 2010 or earlier."),
    ]


def pdb_tasks(recs: list) -> list:
    T = []
    xray, em, nmr = "X-RAY DIFFRACTION", "ELECTRON MICROSCOPY", "SOLUTION NMR"
    single = lambda r: r["exp"] in (xray, em, nmr)
    T.append(dict(id="P.xray", n=44, elig=single, variants=[
        V("Was this structure determined by X-ray diffraction?", lambda r: r["exp"] == xray,
          ("Was this structure solved by crystallography?", "The experimental method is X-RAY DIFFRACTION.", "The experimental method is ELECTRON MICROSCOPY or SOLUTION NMR."))]))
    T.append(dict(id="P.em", n=40, elig=single, variants=[V("Was this structure determined by electron microscopy?", lambda r: r["exp"] == em, None)]))
    T.append(dict(id="P.nmr", n=40, elig=single, variants=[V("Was this structure determined by solution NMR?", lambda r: r["exp"] == nmr, None)]))
    for t in (1.0, 1.5, 2.0, 2.5, 3.0, 3.5):
        ts = fmt_num(t) if t != int(t) else f"{t:.1f}"
        T.append(dict(id=f"P.res{ts}", n=34, elig=lambda r: r["res"] is not None, variants=[
            V(f"Is the reported resolution below {ts} Angstrom?", lambda r, t=t: r["res"] < t,
              ("Is this structure a high-resolution structure?", f"The reported resolution is below {ts} Angstrom.", f"The reported resolution is {ts} Angstrom or more.")),
            V(f"Is the reported resolution {ts} Angstrom or more?", lambda r, t=t: r["res"] >= t,
              ("Is this structure a low-resolution structure?", f"The reported resolution is {ts} Angstrom or more.", f"The reported resolution is below {ts} Angstrom."))]))
    for y in (2000, 2005, 2010, 2015, 2020):
        T.append(dict(id=f"P.year{y}", n=30, elig=lambda r: True, variants=[
            V(f"Was this entry deposited after {y}?", lambda r, y=y: r["year"] > y,
              ("Is this entry a recent entry?", f"The deposition year is after {y}.", f"The deposition year is {y} or earlier.")),
            V(f"Was this entry deposited in {y} or earlier?", lambda r, y=y: r["year"] <= y,
              ("Is this entry an older entry?", f"The deposition year is {y} or earlier.", f"The deposition year is after {y}."))]))
    cls = [k for k, _ in Counter(r["klass"] for r in recs).most_common(7)]
    for k in cls:
        T.append(dict(id="P.class." + re.sub(r"\W+", "_", k), n=26, elig=lambda r: True, variants=[
            V(f"Is the classification of this entry {k}?", lambda r, k=k: r["klass"] == k, None)]))
    T.append(dict(id="P.human", n=40, elig=lambda r: bool(r["org"]), variants=[
        V("Does the source organism field list Homo sapiens?", lambda r: "homo sapiens" in r["org"].lower(),
          ("Is this entry a human-derived entry?", "The source organism field includes Homo sapiens.", "The source organism field names only other organisms."))]))
    for w in ("COMPLEX", "KINASE", "DNA", "RECEPTOR"):
        T.append(dict(id=f"P.word{w}", n=30, elig=lambda r: True, variants=[
            V(f"Does the title contain the word {w}?", lambda r, w=w: re.search(r"(?<![A-Z0-9])" + w + r"(?![A-Z0-9])", r["title"].upper()) is not None, None)]))
    return T


def sig2(x: float) -> float:
    return float(f"{x:.2g}")


def euro_series(recs: list) -> dict:
    out = defaultdict(list)
    for r in recs:
        out[(r["ds"], r["series"])].append(r)
    return out


# ---------------------------------------------------------------------------------------------------------- sampling
def check_variants(tasks: list, source: str, dropped: list) -> None:
    """Kit polarity check on every wording (core question of card rows and free wording). A failing variant is dropped."""
    for t in tasks:
        keep = []
        for v in t["variants"]:
            texts = [v["free"]] + ([v["card"][0]] if v["card"] else [])
            bad = [p for x in texts for p in polarity.problems(x, +1)]
            if bad:
                dropped.append({"source": source, "task": t["id"], "free": v["free"], "problems": bad})
            else:
                keep.append(v)
        t["variants"] = keep


def split_pools(task: dict, recs: list):
    """{variant index: ([records with pred True], [records with pred False])}, in hash order of (task, record)."""
    el = [r for r in recs if task["elig"](r)]
    el.sort(key=lambda r: H("pool", task["id"], r["key"]))
    pools = {}
    for i, v in enumerate(task["variants"]):
        t, f = [], []
        for r in el:
            (t if v["pred"](r) else f).append(r)
        pools[i] = (t, f)
    return pools


def sample_task(task: dict, recs: list, used: set, source: str, state_fn, rows: list, stats: Counter):
    pools = split_pools(task, recs)
    n = int(round(task["n"] * SCALE * SRC_SCALE.get(source, 1.0)))
    n_yes = int(math.floor(n * YES_TARGET + U("yes", task["id"])))
    slots = sorted(range(n), key=lambda s: H("slot", task["id"], s))
    want_yes = set(slots[:n_yes])
    ptr = {(i, g): 0 for i in pools for g in (0, 1)}
    for s in range(n):
        vi = H("variant", task["id"], s) % len(task["variants"])
        v = task["variants"][vi]
        g = 1 if s in want_yes else 0
        pool = pools[vi][0 if g == 1 else 1]
        k = ptr[(vi, g)]
        while k < len(pool) and pool[k]["key"] in used:
            k += 1
        if k >= len(pool):
            stats["pool_exhausted"] += 1
            continue
        r = pool[k]
        ptr[(vi, g)] = k + 1
        used.add(r["key"])
        use_card = v["card"] is not None and (task.get("card_only") or U("card", task["id"], s) < CARD_SHARE)
        if use_card:
            core, yes_l, no_l = v["card"]
            instr, card = core, f"- yes: {yes_l}\n- no: {no_l}"
        else:
            instr, card = v["free"], None
        rows.append({"rec": r, "task": task["id"], "variant": vi, "gold": g, "instr": instr, "card": card, "slot": s})


def make_row(item: dict, source: str, state_fn) -> dict:
    r = item["rec"]
    s = SRC[source]
    doc = r["doc"]
    rid = f"{source}:{sha(item['task'] + '|' + r['key'] + '|' + str(item['variant']))[:16]}"
    meta = {"family": "GP", "spec_id": "GPROXY.v1", "card_id": None, "domain_pack": s["domain"], "sampler": "G-PROXY",
            "gen_version": "gproxy build.py v1 (15 Oct 2026)", "git_sha": "uncommitted", "seed": SEED,
            "structure_hash": sha(doc)[:16], "difficulty_bin": None, "crowd_pg": None, "depth": None, "deep": None,
            "format_style": "record/text", "wording_id": None, "defs_style": "card" if item["card"] else "none",
            "twin_of": None, "twin_kind": None, "text_source": s["name"], "licence": GPROXY_LICENCE, "edge": [],
            "qform": item["task"], "dev_only": True, "never_train": True,
            "source": source, "source_doc": doc, "dataset": s["name"], "source_licence": s["licence_name"],
            "source_licence_url": s["licence_url"], "snapshot": SNAPSHOT, "task": item["task"], "variant": item["variant"],
            "card_style": "card" if item["card"] else "free"}
    return {"id": rid, "group_id": f"{source}:g:{sha(doc)[:16]}", "call_id": f"{source}:{sha(rid)[:12]}", "source": source,
            "state": state_fn(item), "qtype": "noul", "instructions": item["instr"], "options": None, "gold": item["gold"],
            "role": "base", "card": item["card"], "meta": meta}


def build_source(source: str, tasks: list, recs: list, state_fn, dropped: list, stats: Counter) -> list:
    check_variants(tasks, source, dropped)
    items, used = [], set()
    for t in tasks:
        sample_task(t, recs, used, source, state_fn, items, stats)
    return [make_row(it, source, state_fn) for it in items]


def build_euro(recs: list, dropped: list, stats: Counter) -> list:
    ser = euro_series(recs)
    # threshold tasks: <= 3 series per dataset, chosen by hash, >= 25 values
    by_ds = defaultdict(list)
    for (ds, sr), rs in ser.items():
        if len(rs) >= 25:
            by_ds[ds].append((ds, sr))
    chosen = []
    for ds, keys in sorted(by_ds.items()):
        keys.sort(key=lambda k: H("series", str(k)))
        chosen += keys[:3]
    tasks = []
    for ds, sr in chosen:
        rs = ser[(ds, sr)]
        med = sig2(statistics.median(r["v"] for r in rs))
        t = fmt_num(med)
        tasks.append(dict(id=f"E.thr.{ds}.{sha(str(sr))[:6]}", n=7, series=(ds, sr), elig=lambda r, ds=ds, sr=sr: r["ds"] == ds and r["series"] == sr, variants=[
            V(f"Is the reported value above {t}?", lambda r, med=med: r["v"] > med,
              ("Is this value a high value for the series?", f"The reported value is above {t}.", f"The reported value is {t} or lower.")),
            V(f"Is the reported value {t} or lower?", lambda r, med=med: r["v"] <= med,
              ("Is this value a low value for the series?", f"The reported value is {t} or lower.", f"The reported value is above {t}.")),
            V(f"Does this record show a value above {t}?", lambda r, med=med: r["v"] > med,
              (f"Does this record show a value above {t}?", f"The reported value is above {t}.", f"The reported value is {t} or lower."))]))
    for t in tasks:
        t["key"] = t["id"]
    for t in tasks:
        check_variants([t], "gp_eurostat", dropped)
    idx = {(r["ds"], r["series"], r["geo"], r["year"]): r for r in recs}
    geos = defaultdict(list)                   # (ds, series, year) -> geo codes
    for r in recs:
        geos[(r["ds"], r["series"], r["year"])].append(r["geo"])
    used, items = set(), []
    for t in tasks:
        sample_task(t, recs, used, "gp_eurostat", None, items, stats)
    rows_out = list(items)
    # year-on-year and country-pair tasks: one task per dataset
    dss = sorted({r["ds"] for r in recs})
    yo, pr = [], []
    for ds in dss:
        rs = [r for r in recs if r["ds"] == ds]
        cand_y, cand_p = [], []
        for r in rs:
            k = 1 + H("gap", ds, str(r["series"]), r["geo"], r["year"]) % 4
            o = idx.get((ds, r["series"], r["geo"], r["year"] - k))
            if o:
                cand_y.append({"key": f"Y|{ds}|{sha(str(r['series']))[:6]}|{r['geo']}|{r['year']}", "doc": f"eurostat:{ds}:{r['geo']}", "r": r, "o": o})
            others = sorted(g for g in geos[(ds, r["series"], r["year"])] if g != r["geo"])
            if others:
                og = others[H("partner", ds, str(r["series"]), r["geo"], r["year"]) % len(others)]
                cand_p.append({"key": f"P|{ds}|{sha(str(r['series']))[:6]}|{r['geo']}|{og}|{r['year']}", "doc": f"eurostat:{ds}:{r['geo']}",
                               "r": r, "o": idx[(ds, r["series"], og, r["year"])]})
        yo.append(dict(id=f"E.yoy.{ds}", n=14, elig=lambda c: True, cands=cand_y, kind="yoy"))
        pr.append(dict(id=f"E.pair.{ds}", n=9, elig=lambda c: True, cands=cand_p, kind="pair"))
    for t in yo + pr:
        if len(t["cands"]) < 40:
            stats["euro_task_skipped"] += 1
            continue
        yoy = t["kind"] == "yoy"
        a_txt = (lambda c: f"the value for {c['r']['year']} higher than the value for {c['o']['year']}") if yoy else \
            (lambda c: f"the value for {c['r']['geo_name']} higher than the value for {c['o']['geo_name']}")
        b_txt = (lambda c: f"the value for {c['r']['year']} lower than or equal to the value for {c['o']['year']}") if yoy else \
            (lambda c: f"the value for {c['r']['geo_name']} lower than or equal to the value for {c['o']['geo_name']}")
        # polarity check on a sample wording of each variant
        for tag, fn in (("a", a_txt), ("b", b_txt)):
            txt = "Is " + fn(t["cands"][0]) + "?"
            bad = polarity.problems(txt, +1)
            if bad:
                dropped.append({"source": "gp_eurostat", "task": t["id"], "free": txt, "problems": bad})
                stats["euro_variant_dropped"] += 1
        pool_sorted = sorted(t["cands"], key=lambda c: H("pool", t["id"], c["key"]))
        n = int(round(t["n"] * SCALE))
        n_yes = int(math.floor(n * YES_TARGET + U("yes", t["id"])))
        slots = sorted(range(n), key=lambda s: H("slot", t["id"], s))
        want_yes = set(slots[:n_yes])
        pa = [[c for c in pool_sorted if c["r"]["v"] > c["o"]["v"]], [c for c in pool_sorted if not c["r"]["v"] > c["o"]["v"]]]   # variant a: True / False
        ptr = {}
        for s in range(n):
            vi = H("variant", t["id"], s) % 2
            g = 1 if s in want_yes else 0
            # variant a true = pa[0]; variant b true = pa[1]
            pool = pa[0] if (vi == 0) == (g == 1) else pa[1]
            k = ptr.get(id(pool), 0)
            while k < len(pool) and pool[k]["key"] in used:
                k += 1
            if k >= len(pool):
                stats["pool_exhausted"] += 1
                continue
            c = pool[k]
            ptr[id(pool)] = k + 1
            used.add(c["key"])
            fn = a_txt if vi == 0 else b_txt
            r, o = c["r"], c["o"]
            rec = {"key": c["key"], "doc": c["doc"], "r": r, "o": o, "kind": t["kind"]}
            rows_out.append({"rec": rec, "task": t["id"], "variant": vi, "gold": g, "instr": "Is " + fn(c) + "?", "card": None, "slot": s})
    return rows_out


def euro_val(x: dict) -> str:
    return fmt_num(x["v"]) if abs(x["v"]) >= 1 else f"{x['v']:g}"


def euro_state(it: dict) -> str:
    r = it["rec"]
    val = euro_val
    if "o" not in r:
        return euro_head(r) + f"\nCountry: {r['geo_name']}\nYear: {r['year']}\nValue: {val(r)}"
    a, b = r["r"], r["o"]
    if r["kind"] == "yoy":
        return euro_head(a) + f"\nCountry: {a['geo_name']}\n{b['year']} value: {val(b)}\n{a['year']} value: {val(a)}"
    return euro_head(a) + f"\nYear: {a['year']}\nCountry {a['geo_name']}: {val(a)}\nCountry {b['geo_name']}: {val(b)}"


# ---------------------------------------------------------------------------------------------------------- main
def main():
    dropped, stats = [], Counter()
    rows = []
    ap = load_airports()
    rows += build_source("gp_ourairports", airport_tasks() + airport_pair_tasks(), ap, lambda it: airport_state(it["rec"]), dropped, stats)
    pdb = load_pdb()
    rows += build_source("gp_wwpdb", pdb_tasks(pdb) + pdb_pair_tasks(), pdb, lambda it: pdb_state(it["rec"]), dropped, stats)
    eu = load_eurostat()
    eitems = build_euro(eu, dropped, stats)
    for it in eitems:
        rows.append(make_row(it, "gp_eurostat", euro_state))
    # final deterministic order, id uniqueness
    rows.sort(key=lambda r: H("order", r["id"]))
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids)), "duplicate ids"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    # report
    per = defaultdict(lambda: Counter())
    for r in rows:
        c = per[r["source"]]
        c["rows"] += 1
        c["yes"] += r["gold"]
        c["card_free"] += r["card"] is None
        c["clusters"] = 0
    clusters = defaultdict(set)
    for r in rows:
        clusters[r["source"]].add(r["meta"]["source_doc"])
    # polarity / A43(f) audit of every instruction
    pol_bad, neg_words = [], re.compile(r"\b(not|no|never|n't|without|neither|nor)\b|n't", re.I)
    for r in rows:
        probs = polarity.problems(r["instructions"], +1)
        rd = polarity.read(r["instructions"])
        if probs or rd.k_syn or rd.lexical or rd.frame not in ("plain", "explicit") or neg_words.search(r["instructions"]):
            pol_bad.append({"id": r["id"], "text": r["instructions"], "problems": probs, "frame": rd.frame})
    n = len(rows)
    rep = {"seed": SEED, "snapshot": SNAPSHOT, "rows": n, "yes_share": round(sum(r["gold"] for r in rows) / n, 4),
           "card_free_share": round(sum(r["card"] is None for r in rows) / n, 4),
           "per_source": {s: {"rows": c["rows"], "share_of_rows": round(c["rows"] / n, 4), "yes_share": round(c["yes"] / c["rows"], 4),
                              "card_free_share": round(c["card_free"] / c["rows"], 4), "clusters": len(clusters[s])} for s, c in per.items()},
           "tasks": len({r["meta"]["task"] for r in rows}), "stats": dict(stats), "variants_dropped_by_polarity": dropped,
           "polarity_or_negation_failures": pol_bad[:20], "n_polarity_or_negation_failures": len(pol_bad),
           "note": "no final hash recorded: the Haiku noise check (A42-D 12.3) comes first"}
    REPORT.write_text(json.dumps(rep, indent=1) + "\n")
    print(json.dumps({k: rep[k] for k in ("rows", "yes_share", "card_free_share", "per_source", "tasks", "stats", "n_polarity_or_negation_failures")}, indent=1))


if __name__ == "__main__":
    main()
