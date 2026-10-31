"""Group B raw snapshots (geonames, gbif, fsa, ror). Network. Usage: python -B fetch_b.py <source>
Writes meta_src/raw/<source>/*.json[l]. Deterministic given upstream state; the snapshot date is in SNAPSHOT.json."""
import json, sys, time, random, urllib.request, urllib.parse, zipfile, io, datetime
from pathlib import Path
RAW = Path(__file__).resolve().parents[1] / "raw"
UA = {"User-Agent": "opendecide-c2-build/1.0 (research data build)"}

def get(url, headers=None, tries=4, binary=False):
    import subprocess
    h = dict(UA); h.update(headers or {})
    cmd = ["curl", "-sS", "--fail", "--max-time", "90", url] + sum([["-H", f"{k}: {v}"] for k, v in h.items()], [])
    for k in range(tries):
        try:
            b = subprocess.run(cmd, capture_output=True, check=True).stdout
            return b if binary else json.loads(b)
        except Exception as e:
            if k == tries - 1:
                raise
            time.sleep(2 + 3 * k)

def snap(src, **kw):
    (RAW / src / "SNAPSHOT.json").write_text(json.dumps(dict(kw, fetched_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()), indent=1))

def geonames():
    d = RAW / "geonames"
    b = get("https://download.geonames.org/export/dump/cities15000.zip", binary=True)
    zipfile.ZipFile(io.BytesIO(b)).extract("cities15000.txt", d)
    for f in ("countryInfo.txt", "admin1CodesASCII.txt"):
        (d / f).write_bytes(get("https://download.geonames.org/export/dump/" + f, binary=True))
    snap("geonames", files=["cities15000.txt", "countryInfo.txt", "admin1CodesASCII.txt"])

def fsa():
    d = RAW / "fsa"
    H = {"x-api-version": "2", "Accept": "application/json"}
    auth = get("https://api.ratings.food.gov.uk/Authorities/basic", H)["authorities"]
    json.dump(auth, open(d / "authorities.json", "w"))
    fhrs = [a for a in auth if a["SchemeType"] == 1 and a["EstablishmentCount"] >= 400]
    rnd = random.Random(20261015); rnd.shuffle(fhrs)
    out = open(d / "establishments.jsonl", "w")
    n = 0
    for a in fhrs[:90]:
        pn = 1 + rnd.randrange(max(1, a["EstablishmentCount"] // 300))
        u = f"https://api.ratings.food.gov.uk/Establishments?localAuthorityId={a['LocalAuthorityId']}&pageSize=300&pageNumber={pn}"
        try:
            es = get(u, H)["establishments"]
        except Exception as e:
            print("skip", a["Name"], e); continue
        for e in es:
            # drop every personal/address/contact/name field: keep categorical, date and score fields only
            out.write(json.dumps({"fhrsid": e.get("FHRSID"), "bt": e.get("BusinessType"), "btid": e.get("BusinessTypeID"),
                "rating": e.get("RatingValue"), "rdate": e.get("RatingDate"), "scheme": e.get("SchemeType"),
                "la": e.get("LocalAuthorityName"), "laid": a["LocalAuthorityId"], "scores": e.get("scores"),
                "newrating": e.get("NewRatingPending")}) + "\n"); n += 1
        time.sleep(0.3)
    out.close()
    snap("fsa", rows=n, authorities=len(auth))

def ror():
    d = RAW / "ror"
    out = open(d / "orgs.jsonl", "w"); seen = set(); n = 0
    def page(filt, pg):
        nonlocal n
        u = "https://api.ror.org/v2/organizations?page=%d" % pg + ("&filter=" + urllib.parse.quote(filt, safe=":,") if filt else "")
        for o in get(u).get("items", []):
            if o["id"] in seen: continue
            seen.add(o["id"]); n += 1
            loc = (o.get("locations") or [{}])[0].get("geonames_details", {})
            out.write(json.dumps({"id": o["id"], "types": o.get("types"), "status": o.get("status"), "established": o.get("established"),
                "cc": loc.get("country_code"), "cname": loc.get("country_name"),
                "nnames": len(o.get("names", [])), "nlinks": len(o.get("links", [])), "rel": [r.get("type") for r in o.get("relationships", [])],
                "ntypes": len(o.get("types") or []), "ndomains": len(o.get("domains", [])),
                "ext": [e["type"] for e in o.get("external_ids", [])],
                "name": next((x["value"] for x in o.get("names", []) if "ror_display" in x.get("types", [])), None)}) + "\n")
        time.sleep(0.4)
    for t in ("education", "company", "government", "healthcare", "nonprofit", "facility", "archive", "funder", "other"):
        for pg in range(1, 7 if t in ("education", "company", "nonprofit", "government", "healthcare") else 5):
            page("types:" + t, pg)
    for cc in "US GB DE FR JP CN IN BR CA AU IT ES NL SE CH KR RU PL TR MX ZA AR NG EG IR ID PT AT BE DK NO FI IE NZ".split():
        for pg in (1, 2, 3):
            page("locations.geonames_details.country_code:" + cc, pg)
    out.close(); snap("ror", rows=n)

def gbif():
    d = RAW / "gbif"; K = "d7dddbf4-2cf0-4f39-9b2a-bb099caae36c"
    base = f"https://api.gbif.org/v1/species/search?datasetKey={K}"
    rnd = random.Random(20261015); out = open(d / "taxa.jsonl", "w"); seen = set(); n = 0
    keep = ["key", "kingdom", "phylum", "class", "order", "family", "genus", "species", "canonicalName", "taxonomicStatus", "rank",
            "extinct", "habitats", "numDescendants", "acceptedKey", "accepted", "kingdomKey", "classKey", "familyKey", "genusKey", "nameType"]
    def q(extra, label, lim=60):
        nonlocal n
        r = get(f"{base}&limit={lim}&{extra}")
        for t in r.get("results", []):
            if t["key"] in seen: continue
            seen.add(t["key"]); n += 1
            out.write(json.dumps(dict({k: t.get(k) for k in keep}, q=label)) + "\n")
        time.sleep(0.25)
        return r
    classes = []
    for kg in (1, 5, 6, 3, 4, 7, 2):
        for off in (0, 300):
            r = get(f"{base}&limit=300&offset={off}&rank=CLASS&status=ACCEPTED&highertaxonKey={kg}")
            classes += [(t["key"], t.get("kingdom")) for t in r["results"] if t.get("kingdom") == r["results"][0].get("kingdom")]
            time.sleep(0.25)
    byk = {}
    for ck, kg in classes:
        byk.setdefault(kg, []).append(ck)
    quota = {"Animalia": 40, "Plantae": 30, "Fungi": 22, "Chromista": 8, "Bacteria": 5, "Protozoa": 3, "Archaea": 2}
    sel = []
    for kg, n_ in quota.items():
        v = byk.get(kg, [])
        rnd.shuffle(v)
        sel += [(c, kg) for c in v[:n_]]
    for ck, kg in sel:
        for rank, status, lim in (("SPECIES", "ACCEPTED", 14), ("SPECIES", "SYNONYM", 8), ("FAMILY", "ACCEPTED", 10), ("GENUS", "ACCEPTED", 10)):
            try:
                cnt = get(f"{base}&limit=1&rank={rank}&status={status}&highertaxonKey={ck}")["count"]
                if cnt == 0: continue
                off = rnd.randrange(max(1, min(cnt, 9000) - lim))
                q(f"rank={rank}&status={status}&highertaxonKey={ck}&offset={off}", f"{ck}:{rank}:{status}", lim)
            except Exception as e:
                print("skip", ck, rank, e)
    for rank in ("KINGDOM", "PHYLUM", "ORDER", "SUBSPECIES", "VARIETY"):
        try:
            cnt = get(f"{base}&limit=1&rank={rank}&status=ACCEPTED")["count"]
            for i in range(3):
                q(f"rank={rank}&status=ACCEPTED&offset={rnd.randrange(max(1, min(cnt, 9000) - 60))}", f"any:{rank}", 40)
        except Exception as e:
            print("skip", rank, e)
    out.close(); snap("gbif", rows=n, classes=len(classes))

if __name__ == "__main__":
    globals()[sys.argv[1]]()
