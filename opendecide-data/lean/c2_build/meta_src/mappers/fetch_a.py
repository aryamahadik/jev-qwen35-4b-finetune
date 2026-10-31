"""fetch_a.py: small polite snapshots of openalex / musicbrainz / worldbank / usgs for the A42-D 8 metadata mappers.

Run: ../../.venv/bin/python -B meta_src/mappers/fetch_a.py <source>   (network; stdlib only)
Output: meta_src/raw_a/<source>/*.json (untrusted upstream data; never executed).
Rate limits: OpenAlex list calls cost 0.0001 USD each against the free 0.10 USD/day IP budget (about 40 calls here);
MusicBrainz 1 request per 1.2 s with a contact User-Agent; World Bank and USGS are unmetered (a few dozen calls).
"""
import json
import ssl
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

RAW = Path(__file__).resolve().parent.parent / "raw_a"
CTX = ssl.create_default_context(cafile="/etc/ssl/cert.pem")  # system bundle; verification stays on
UA = "OpenDecideResearchMapper/1.0 (jaypatil.duke@gmail.com)"


def get(url, params=None, tries=3, pause=0.0):
    if params:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=60, context=CTX) as r:
                data = json.loads(r.read().decode("utf-8"))
            time.sleep(pause)
            return data
        except Exception as e:  # noqa: BLE001
            print("retry", k, str(e)[:120], file=sys.stderr)
            time.sleep(3 + 5 * k)
    raise RuntimeError("fetch failed: " + url[:150])


def openalex():
    out = RAW / "openalex"
    sel = ("id,doi,type,publication_year,publication_date,language,open_access,is_retracted,cited_by_count,"
           "referenced_works_count,countries_distinct_count,institutions_distinct_count,has_fulltext,"
           "primary_location,biblio,primary_topic,authorships,is_paratext,fwci")
    works, n = [], 0
    strata = []
    for t in ("article", "preprint", "book-chapter", "review", "dataset", "book", "dissertation", "letter",
              "editorial", "erratum", "report", "standard"):
        for yr in ("1990-01-01:2004-12-31", "2005-01-01:2014-12-31", "2015-01-01:2020-12-31", "2021-01-01:2026-09-30"):
            strata.append((t, yr, 100 if t in ("article", "preprint", "book-chapter") else 60))
    for (t, yr, per) in strata:
        a, b = yr.split(":")
        flt = f"type:{t},from_publication_date:{a},to_publication_date:{b},language:en|fr|de|es|pt|zh|ru|it"
        d = get("https://api.openalex.org/works", {"filter": flt, "sample": per, "seed": 20261015 + n, "per-page": per,
                                                     "select": sel, "mailto": "jaypatil.duke@gmail.com"}, pause=0.3)
        for w in d.get("results", []):
            # keep only non-personal fields; author and institution names are dropped here
            auth = w.get("authorships") or []
            ps = w.get("primary_location") or {}
            src = ps.get("source") or {}
            works.append({
                "id": w["id"].rsplit("/", 1)[-1], "doi": (w.get("doi") or "").replace("https://doi.org/", "") or None,
                "type": w.get("type"), "year": w.get("publication_year"), "date": w.get("publication_date"),
                "language": w.get("language"), "oa_status": (w.get("open_access") or {}).get("oa_status"),
                "is_oa": (w.get("open_access") or {}).get("is_oa"), "is_retracted": w.get("is_retracted"),
                "cited_by": w.get("cited_by_count"), "refs": w.get("referenced_works_count"),
                "n_countries": w.get("countries_distinct_count"), "n_inst": w.get("institutions_distinct_count"),
                "has_fulltext": w.get("has_fulltext"), "n_authors": len(auth),
                "source_type": src.get("type"), "source_name": src.get("display_name"),
                "source_is_oa": src.get("is_oa"), "source_is_in_doaj": src.get("is_in_doaj"),
                "license": ps.get("license"), "version": ps.get("version"),
                "biblio": {k: v for k, v in (w.get("biblio") or {}).items() if v},
                "field": ((w.get("primary_topic") or {}).get("field") or {}).get("display_name"),
                "domain": ((w.get("primary_topic") or {}).get("domain") or {}).get("display_name"),
                "is_paratext": w.get("is_paratext"), "fwci": w.get("fwci"),
                "corresponding": any(x.get("is_corresponding") for x in auth),
            })
        n += 1
    # retracted works (a rare class): a few extra calls
    for k in range(4):
        d = get("https://api.openalex.org/works", {"filter": "is_retracted:true,from_publication_date:2005-01-01",
                                                     "sample": 100, "seed": 7000 + k, "per-page": 100, "select": sel}, pause=0.3)
        for w in d.get("results", []):
            ps = w.get("primary_location") or {}
            src = ps.get("source") or {}
            auth = w.get("authorships") or []
            works.append({"id": w["id"].rsplit("/", 1)[-1], "doi": (w.get("doi") or "").replace("https://doi.org/", "") or None,
                          "type": w.get("type"), "year": w.get("publication_year"), "date": w.get("publication_date"),
                          "language": w.get("language"), "oa_status": (w.get("open_access") or {}).get("oa_status"),
                          "is_oa": (w.get("open_access") or {}).get("is_oa"), "is_retracted": w.get("is_retracted"),
                          "cited_by": w.get("cited_by_count"), "refs": w.get("referenced_works_count"),
                          "n_countries": w.get("countries_distinct_count"), "n_inst": w.get("institutions_distinct_count"),
                          "has_fulltext": w.get("has_fulltext"), "n_authors": len(auth), "source_type": src.get("type"),
                          "source_name": src.get("display_name"), "source_is_oa": src.get("is_oa"),
                          "source_is_in_doaj": src.get("is_in_doaj"), "license": ps.get("license"),
                          "version": ps.get("version"), "biblio": {k2: v for k2, v in (w.get("biblio") or {}).items() if v},
                          "field": ((w.get("primary_topic") or {}).get("field") or {}).get("display_name"),
                          "domain": ((w.get("primary_topic") or {}).get("domain") or {}).get("display_name"),
                          "is_paratext": w.get("is_paratext"), "fwci": w.get("fwci"),
                          "corresponding": any(x.get("is_corresponding") for x in auth)})
    seen, uniq = set(), []
    for w in works:
        if w["id"] not in seen:
            seen.add(w["id"])
            uniq.append(w)
    (out / "works.json").write_text(json.dumps(uniq))
    print("openalex works", len(uniq))


def musicbrainz():
    out = RAW / "musicbrainz"
    qs = []
    for ptype, per_decade in (("album", 8), ("single", 5), ("ep", 5)):
        for lo, hi in (("1960", "1969"), ("1970", "1979"), ("1980", "1989"), ("1990", "1999"), ("2000", "2009"),
                       ("2010", "2019"), ("2020", "2026")):
            for off in range(0, per_decade * 0 + 100, 100):
                qs.append((f"primarytype:{ptype} AND firstreleasedate:[{lo} TO {hi}]", off))
    for sec in ("live", "compilation", "soundtrack", "remix", "demo", "dj-mix", "mixtape/street", "spokenword", "interview"):
        for lo, hi in (("1960", "1999"), ("2000", "2026")):
            qs.append((f"secondarytype:\"{sec}\" AND firstreleasedate:[{lo} TO {hi}]", 0))
    for ptype in ("broadcast", "other"):
        qs.append((f"primarytype:{ptype} AND firstreleasedate:[1950 TO 2026]", 0))
    items = []
    for q, off in qs:
        d = get("https://musicbrainz.org/ws/2/release-group", {"query": q, "limit": 100, "offset": off, "fmt": "json"}, pause=1.3)
        for g in d.get("release-groups", []):
            ac = g.get("artist-credit") or []
            items.append({
                "id": g["id"], "title": g.get("title"), "first_release_date": g.get("first-release-date") or None,
                "primary_type": g.get("primary-type"), "secondary_types": g.get("secondary-types") or [],
                "n_credits": len(ac), "n_releases": len(g.get("releases") or []), "release_count": g.get("count"),
                "disambiguation": g.get("disambiguation") or None,
                "tags": [t["name"] for t in (g.get("tags") or [])][:8],
                "statuses": sorted({r.get("status") for r in (g.get("releases") or []) if r.get("status")}),
                "various_artists": any((a.get("artist") or {}).get("id") == "89ad4ac3-39f7-470e-963a-56509c546377" for a in ac),
            })
    seen, uniq = set(), []
    for w in items:
        if w["id"] not in seen:
            seen.add(w["id"])
            uniq.append(w)
    (out / "release_groups.json").write_text(json.dumps(uniq))
    print("musicbrainz release groups", len(uniq))


def worldbank():
    out = RAW / "worldbank"
    fl = ("id,project_name,status,lendinginstr,lendinginstrtype,totalcommamt,totalamt,boardapprovaldate,closingdate,"
          "regionname,countryshortname,countrycode,mjsector_namecode,sector_namecode,mjtheme_namecode,theme_namecode,"
          "projectstatusdisplay,envassesmentcategorycode,approvalfy,prodlinetext,supplementprojectflg,ibrdcommamt,idacommamt,"
          "grantamt,projectfinancialtype,sector1")
    items = []
    for os_ in range(0, 22729, 500):
        d = get("https://search.worldbank.org/api/v2/projects", {"format": "json", "rows": 500, "os": os_, "fl": fl}, pause=0.5)
        items += list((d.get("projects") or {}).values())
    (out / "projects.json").write_text(json.dumps(items))
    print("worldbank projects", len(items))


def usgs():
    out = RAW / "usgs"
    parts = []
    for name, q in (("m45_2025", {"minmagnitude": 4.5, "starttime": "2025-01-01", "endtime": "2026-01-01", "limit": 20000}),
                    ("m25_2026", {"minmagnitude": 2.5, "starttime": "2026-05-01", "endtime": "2026-09-30", "limit": 20000}),
                    ("m6_2010", {"minmagnitude": 6.0, "starttime": "2010-01-01", "endtime": "2025-01-01", "limit": 20000})):
        d = get("https://earthquake.usgs.gov/fdsnws/event/1/query", dict(q, format="geojson", orderby="time"), pause=1.0)
        for f in d.get("features", []):
            p = f["properties"]
            c = f["geometry"]["coordinates"]
            parts.append({"id": f["id"], "mag": p.get("mag"), "magType": p.get("magType"), "type": p.get("type"),
                          "status": p.get("status"), "tsunami": p.get("tsunami"), "felt": p.get("felt"), "alert": p.get("alert"),
                          "net": p.get("net"), "sig": p.get("sig"), "time": p.get("time"), "place": p.get("place"),
                          "cdi": p.get("cdi"), "mmi": p.get("mmi"), "nst": p.get("nst"), "gap": p.get("gap"), "rms": p.get("rms"),
                          "lon": c[0], "lat": c[1], "depth": c[2], "set": name})
    (out / "events.json").write_text(json.dumps(parts))
    print("usgs events", len(parts))


if __name__ == "__main__":
    dict(openalex=openalex, musicbrainz=musicbrainz, worldbank=worldbank, usgs=usgs)[sys.argv[1]]()
