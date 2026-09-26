"""Polite, cached arXiv API fetcher used by build_arxiv2026.py.

Every raw API page is cached under ohs/cache/arxiv/ so re-runs are offline and
deterministic. At least 3 s between live requests (arXiv API terms of use).
"""
import os, re, time, json, hashlib
import xml.etree.ElementTree as ET
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache", "arxiv")
API = "http://export.arxiv.org/api/query"
UA = "ohs-benchmark-builder/0.1 (research benchmark; polite 3s delay)"
NS = {"a": "http://www.w3.org/2005/Atom",
      "arxiv": "http://arxiv.org/schemas/atom",
      "os": "http://a9.com/-/spec/opensearch/1.1/"}
_last = [0.0]


def _get(params):
    key = hashlib.sha1(json.dumps(params, sort_keys=True).encode()).hexdigest()[:16]
    path = os.path.join(CACHE, key + ".xml")
    if os.path.exists(path):
        return open(path, encoding="utf-8").read()
    os.makedirs(CACHE, exist_ok=True)
    for attempt in range(6):
        wait = 3.2 - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        try:
            r = requests.get(API, params=params, timeout=180, headers={"User-Agent": UA})
            _last[0] = time.time()
            if r.status_code == 200 and "<feed" in r.text:
                return r.text, path
        except requests.RequestException as e:
            _last[0] = time.time()
            print("  retry after error:", e)
        time.sleep(5 * (attempt + 1))
    raise RuntimeError("arXiv API failed for %r" % (params,))


def parse(xml):
    root = ET.fromstring(xml)
    total = int(root.find("os:totalResults", NS).text)
    out = []
    for e in root.findall("a:entry", NS):
        aid_url = e.find("a:id", NS).text.strip()
        m = re.search(r"abs/(.+?)(v\d+)?$", aid_url)
        cats = [c.get("term") for c in e.findall("a:category", NS)]
        prim = e.find("arxiv:primary_category", NS)
        com = e.find("arxiv:comment", NS)
        out.append({
            "arxiv_id": m.group(1),
            "version": (m.group(2) or "").lstrip("v"),
            "title": " ".join(e.find("a:title", NS).text.split()),
            "abstract": " ".join(e.find("a:summary", NS).text.split()),
            "categories": cats,
            "primary": prim.get("term") if prim is not None else None,
            "published": e.find("a:published", NS).text,
            "updated": e.find("a:updated", NS).text,
            "comment": " ".join(com.text.split()) if com is not None and com.text else "",
        })
    return total, out


def fetch_all(cat, date_from, date_to, page=1000):
    """All entries with `cat` in their category list, submitted in [date_from, date_to]."""
    q = "cat:%s AND submittedDate:[%s0000 TO %s2359]" % (cat, date_from, date_to)
    entries, start, total = [], 0, None
    while True:
        params = {"search_query": q, "start": start, "max_results": page,
                  "sortBy": "submittedDate", "sortOrder": "ascending"}
        got = None
        for attempt in range(4):
            res = _get(params)
            xml = res if isinstance(res, str) else res[0]
            t, es = parse(xml)
            expected = min(page, max(t - start, 0))
            if es or expected == 0:
                got = (t, es)
                if not isinstance(res, str):  # cache only complete, non-empty pages
                    open(res[1], "w", encoding="utf-8").write(xml)
                break
            # arXiv API sometimes returns an empty page transiently; retry uncached
            print("  empty page for %s start=%d (total=%d), retrying" % (cat, start, t))
            time.sleep(6)
        if got is None:
            raise RuntimeError("persistent empty page for %s start=%d" % (cat, start))
        total, es = got
        entries.extend(es)
        start += page
        if start >= total or not es:
            break
    return total, entries
