"""Government open-data portals (Socrata SODA API). Licence is read from each dataset's own metadata record.
Usage: python -I fetch_socrata.py {ns_news|de_parks|mc_volunteer}"""
import json
import re
import sys
import time
import urllib.parse

sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/gblock/tools")
import common as C  # noqa: E402

PERMISSIVE = {"Nova Scotia Open Government Licence", "Public Domain", "Public Domain U.S. Government",
              "Creative Commons 1.0 Universal (Public Domain Dedication)"}


def licence(host, ds):
    d = C.fetch_json(f"https://{host}/api/views/{ds}.json")
    lic = (d.get("license") or {})
    return {"name": lic.get("name"), "termsLink": lic.get("termsLink"), "licenseId": d.get("licenseId"),
            "dataset_name": d.get("name"), "attribution": d.get("attribution")}


def pull(host, ds, select, page=5000):
    rows, off = [], 0
    while True:
        q = urllib.parse.urlencode({"$select": select, "$limit": page, "$offset": off, "$order": ":id"})
        chunk = C.fetch_json(f"https://{host}/resource/{ds}.json?{q}")
        rows += chunk
        print(f"  {host}/{ds}: {len(rows)}", flush=True)
        if len(chunk) < page:
            break
        off += page
        time.sleep(0.5)
    return rows


def get(name, host, ds, select):
    lic = licence(host, ds)
    assert lic["name"] in PERMISSIVE, lic
    raw = C.load_raw(name)
    if raw is None:
        raw = pull(host, ds, select)
        C.save_raw(name, raw)
    return lic, raw


NS_TAIL = re.compile(r"(?is)(\n\s*-30-.*$|\n\s*FOR BROADCAST USE.*$|\n\s*Media Contacts?\s*:.*$|"
                     r"\n\s*Source\s*:.*$|\n\s*Contact\s*:.*$)")


def ns_news():
    host, ds = "data.novascotia.ca", "xcif-vvr3"
    lic, raw = get("ns_news", host, ds, "department,subject,contents,timestamp,url")
    items = []
    for r in raw:
        c = r.get("contents") or ""
        c = re.sub(r"^[^\n]*--[^\n]*\n-{5,}\s*\n", "", c)       # "DEPT--Title" + dashes header
        c = re.sub(r"^\s*[A-Z][A-Z/&,.'() -]+--[^\n]*\n", "", c)  # "DEPT--Title" header without dashes
        c = NS_TAIL.sub("", c)
        c = re.sub(r"(?m)^\s*-{5,}\s*$", "", c)
        c = re.sub(r"(?<!\n)\n(?!\n)", " ", c.replace("\r", ""))      # unwrap hard line breaks
        title = (r.get("subject") or "").strip()
        items.append({"key": r.get("url") or title, "text": f"{title}\n{c}",
                      "meta": {"department": r.get("department"), "timestamp": r.get("timestamp"),
                               "url": r.get("url")}})
    st = C.finish("gov_news", f"News Releases Issued by Government of Nova Scotia ({host}, dataset {ds})",
                  lic["termsLink"] or "https://novascotia.ca/opendata/licence.asp", items,
                  drop_fn=C.private_person_risk)
    print(json.dumps({"licence": lic, **st}))


CONTACT = re.compile(r"(?i)\b(contact|call|e-?mail|phone|register at|questions\?)\b")


def de_parks():
    host, ds = "data.delaware.gov", "pu7t-3gai"
    lic, raw = get("de_parks", host, ds, "id,park,programtitle,start_date,description")
    items = [{"key": r.get("id"), "text": f"{(r.get('programtitle') or '').strip()}\n{r.get('description') or ''}",
              "meta": {"park": r.get("park"), "start_date": r.get("start_date")}} for r in raw]
    st = C.finish("park_programs", f"Delaware State Park Programs ({host}, dataset {ds})",
                  f"https://{host}/api/views/{ds}.json (licence: {lic['name']})", items, scrub_extra=CONTACT)
    print(json.dumps({"licence": lic, **st}))


def _spacing(t):
    t = re.sub(r"([a-z\)])\.([A-Z][a-z])", r"\1. \2", t)
    t = re.sub(r"([a-z]):([A-Z])", r"\1: \2", t)
    return re.sub(r"(?m)^\*+\s*", "", t)


def mc_volunteer():
    host, ds = "data.montgomerycountymd.gov", "rrpb-g5ks"
    lic, raw = get("mc_volunteer", host, ds,
                   "id,agencyname,needtitle,needdetails,needhoursdescription,needagerequirements,qualifications,"
                   "interests,dateadded")
    items = []
    for r in raw:
        parts = [(r.get("needtitle") or "").strip(), r.get("needdetails") or ""]
        for k, lab in (("needhoursdescription", "Hours"), ("needagerequirements", "Age requirement"),
                       ("qualifications", "Qualifications")):
            v = (r.get(k) or "").strip()
            if v:
                parts.append(f"{lab}: {v}")
        items.append({"key": r.get("id"), "text": "\n".join(parts),
                      "meta": {"agency": r.get("agencyname"), "interests": r.get("interests"),
                               "dateadded": r.get("dateadded")}})
    st = C.finish("volunteer_posts", f"Montgomery County Volunteer Center Registered Opportunities ({host}, dataset {ds})",
                  f"https://{host}/api/views/{ds}.json (licence: {lic['name']})", items, scrub_extra=CONTACT,
                  fix_fn=_spacing, drop_fn=lambda t: bool(C.HONORIFIC_NAME.search(t)))
    print(json.dumps({"licence": lic, **st}))


OD_OK = {"Public Domain": None, "Public Domain U.S. Government": "https://www.usa.gov/government-works",
         "Creative Commons 1.0 Universal (Public Domain Dedication)": "https://creativecommons.org/publicdomain/zero/1.0/",
         "Creative Commons Attribution 4.0 International": "https://creativecommons.org/licenses/by/4.0/",
         "Creative Commons Attribution 3.0 Unported": "https://creativecommons.org/licenses/by/3.0/",
         "Creative Commons Attribution | Share Alike 4.0 International": "https://creativecommons.org/licenses/by-sa/4.0/",
         "Creative Commons Attribution | Share Alike 3.0 Unported": "https://creativecommons.org/licenses/by-sa/3.0/",
         "Open Data Commons Public Domain Dedication and License": "https://opendatacommons.org/licenses/pddl/1-0/"}
OD_SKIP_PORTALS = {"data.novascotia.ca", "data.delaware.gov", "data.montgomerycountymd.gov"}


def open_data():
    raw = C.load_raw("socrata_catalog")
    if raw is None:
        raw, scroll = [], None
        for i in range(400):
            q = {"only": "datasets", "limit": 1000}
            if scroll:
                q["scroll_id"] = scroll
            js = C.fetch_json("https://api.us.socrata.com/api/catalog/v1?" + urllib.parse.urlencode(q))
            res = js.get("results", [])
            if not res:
                break
            for r in res:
                m, rs = r.get("metadata", {}), r.get("resource", {})
                if m.get("license") in OD_OK and m.get("domain") not in OD_SKIP_PORTALS:
                    raw.append({"id": rs.get("id"), "domain": m.get("domain"), "name": rs.get("name"),
                                "description": rs.get("description"), "license": m.get("license"),
                                "category": (r.get("classification") or {}).get("domain_category"),
                                "permalink": r.get("permalink")})
            scroll = res[-1]["resource"]["id"]
            print(f"  catalog page {i}: {len(raw)} permissive", flush=True)
            time.sleep(0.5)
        C.save_raw("socrata_catalog", raw)
    items = []
    for r in raw:
        desc = C.clean_ws(C.strip_html(r.get("description") or ""))
        lic_url = OD_OK[r["license"]] or f"https://{r['domain']}/api/views/{r['id']}.json (licence: Public Domain)"
        items.append({"key": f"{r['domain']}/{r['id']}", "text": f"{C.clean_ws(r.get('name') or '')}\n{desc}",
                      "licence_url": lic_url,
                      "meta": {"portal": r["domain"], "id": r["id"], "licence": r["license"],
                               "category": r.get("category")}})
    st = C.finish("open_data", "Socrata open-data portals: dataset descriptions with a permissive licence on the "
                  "record (Socrata Discovery API, api.us.socrata.com)", "per record", items,
                  drop_fn=lambda t: bool(C.HONORIFIC_NAME.search(t)))
    print(json.dumps(st))


if __name__ == "__main__":
    {"ns_news": ns_news, "de_parks": de_parks, "mc_volunteer": mc_volunteer, "open_data": open_data}[sys.argv[1]]()
