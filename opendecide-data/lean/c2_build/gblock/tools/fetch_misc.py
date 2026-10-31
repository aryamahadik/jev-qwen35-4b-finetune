"""bioRxiv abstracts (per-record licence), Art Institute of Chicago descriptions (API licence block),
Ask LibreOffice questions (site licence), OpenStax textbook passages (per-collection licence).
Usage: python -I fetch_misc.py {biorxiv|aic|asklo|openstax}"""
import json
import random
import re
import sys
import time
import urllib.parse
from datetime import date, timedelta

sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/gblock/tools")
import common as C  # noqa: E402

# ------------------------------------------------------------------ bioRxiv
BIO_OK = {"cc_by": "https://creativecommons.org/licenses/by/4.0/",
          "cc0": "https://creativecommons.org/publicdomain/zero/1.0/"}


def biorxiv():
    raw = C.load_raw("biorxiv")
    if raw is None:
        rng = random.Random(5)
        raw, seen = [], set()
        start = date(2021, 1, 1)
        days = [start + timedelta(days=rng.randrange(0, 365 * 5)) for _ in range(400)]
        for d0 in days:
            d1 = d0 + timedelta(days=1)
            url = f"https://api.biorxiv.org/details/biorxiv/{d0.isoformat()}/{d1.isoformat()}/0"
            try:
                js = C.fetch_json(url)
            except Exception as e:  # noqa: BLE001
                print("skip", d0, e)
                continue
            for r in js.get("collection", []):
                if r.get("license") in BIO_OK and r["doi"] not in seen:
                    seen.add(r["doi"])
                    raw.append({k: r.get(k) for k in ("doi", "title", "abstract", "license", "category", "date",
                                                       "version", "type")})
            print(f"  biorxiv {d0}: {len(raw)} permissive", flush=True)
            time.sleep(0.5)
            if len(raw) >= 4200:
                break
        C.save_raw("biorxiv", raw)
    items = []
    for r in raw:
        ab = C.clean_ws(C.strip_html(r.get("abstract") or ""))
        if "$" in ab or "\\" in ab:
            continue
        items.append({"key": r["doi"], "text": f"{C.clean_ws(r.get('title') or '')}\n{ab}",
                      "meta": {"doi": r["doi"], "licence": r["license"], "category": r.get("category"),
                               "date": r.get("date")},
                      "licence_url": BIO_OK[r["license"]]})
    st = C.finish("sci_abstracts", "bioRxiv preprint abstracts (api.biorxiv.org; per-record licence cc_by or cc0)",
                  "per record: https://creativecommons.org/licenses/by/4.0/ or "
                  "https://creativecommons.org/publicdomain/zero/1.0/", items)
    print(json.dumps(st))


# ------------------------------------------------------------------ Art Institute of Chicago
def aic():
    raw = C.load_raw("aic")
    info = None
    if raw is None:
        raw = []
        edges = [0, 20000, 40000, 60000, 80000, 100000, 120000, 140000, 160000, 180000, 200000, 220000, 240000,
                 260000, 300000]
        for lo, hi in zip(edges, edges[1:]):          # the search API pages at most 1,000 hits per query
            for page in range(1, 5):
                q = urllib.parse.urlencode({
                    "query[bool][must][0][exists][field]": "description",
                    "query[bool][must][1][range][id][gte]": lo, "query[bool][must][2][range][id][lt]": hi,
                    "limit": 100, "page": page,
                    "fields": "id,title,description,artwork_type_title,department_title,date_display,"
                              "artist_title,classification_title"})
                js = C.fetch_json(f"https://api.artic.edu/api/v1/artworks/search?{q}")
                info = js.get("info")
                raw += js.get("data", [])
                time.sleep(1.1)
                if len(js.get("data", [])) < 100:
                    break
            print(f"  aic ids {lo}-{hi}: {len(raw)}", flush=True)
        C.save_raw("aic", raw)
        (C.RAW / "aic" / "licence_info.json").write_text(json.dumps(info, indent=1))
    items = []
    for r in raw:
        d = C.clean_ws(C.strip_html(r.get("description") or ""))
        items.append({"key": r["id"], "text": f"{C.clean_ws(r.get('title') or '')}\n{d}",
                      "meta": {"id": r["id"], "artwork_type": r.get("artwork_type_title"),
                               "department": r.get("department_title"), "classification":
                               r.get("classification_title"), "date_display": r.get("date_display")}})
    st = C.finish("museum", "Art Institute of Chicago public API, artwork description field (api.artic.edu)",
                  "https://creativecommons.org/licenses/by/4.0/", items)
    print(json.dumps(st))


# ------------------------------------------------------------------ Ask LibreOffice (Discourse)
def asklo():
    raw = C.load_raw("ask_libreoffice")
    if raw is None:
        raw, before, n_q = [], None, 0
        for i in range(700):
            url = "https://ask.libreoffice.org/posts.json" + (f"?before={before}" if before else "")
            js = C.fetch_json(url)
            posts = js.get("latest_posts", [])
            if not posts:
                break
            for p in posts:
                if p.get("post_number") == 1 and not p.get("hidden") and not p.get("deleted_at"):
                    raw.append({k: p.get(k) for k in ("id", "topic_id", "topic_title", "cooked", "created_at",
                                                       "category_id", "post_number")})
            before = min(p["id"] for p in posts)
            if i % 20 == 0:
                print(f"  asklo page {i}: {len(raw)} questions (before={before})", flush=True)
            time.sleep(1.2)
            if len(raw) >= 6000:
                break
        C.save_raw("ask_libreoffice", raw)
    items = []
    for r in raw:
        body = C.clean_ws(C.strip_html(r.get("cooked") or ""))
        body = re.sub(r"(?im)^\s*(thanks?( you)?|thx|regards|cheers)[^\n]{0,40}$", "", body)
        items.append({"key": r["topic_id"], "text": f"{C.clean_ws(r.get('topic_title') or '')}\n{body}",
                      "meta": {"topic_id": r["topic_id"], "category_id": r.get("category_id"),
                               "created_at": r.get("created_at")}})
    st = C.finish("office_help", "Ask LibreOffice community Q&A, question posts (ask.libreoffice.org)",
                  "https://creativecommons.org/licenses/by-sa/3.0/", items)
    print(json.dumps(st))


# ------------------------------------------------------------------ OpenStax (GitHub osbooks repos, CNXML)
OS_BOOKS = ["osbooks-principles-management", "osbooks-introduction-sociology", "osbooks-entrepreneurship",
            "osbooks-business-ethics", "osbooks-introduction-business", "osbooks-organizational-behavior",
            "osbooks-principles-marketing", "osbooks-psychology", "osbooks-lifespan-development",
            "osbooks-college-success-bundle", "osbooks-workplace-software-skills",
            "osbooks-introduction-political-science", "osbooks-principles-economics-bundle",
            "osbooks-introduction-anthropology", "osbooks-introduction-philosophy", "osbooks-nutrition"]
CC_BY = re.compile(r"creativecommons\.org/licenses/by/4\.0")


def gh_tree(repo):
    for br in ("main", "master"):
        try:
            return br, C.fetch_json(f"https://api.github.com/repos/openstax/{repo}/git/trees/{br}?recursive=1",
                                    headers={"Accept": "application/vnd.github+json"})
        except Exception:  # noqa: BLE001
            continue
    return None, None


def raw_gh(repo, br, path):
    return C.fetch(f"https://raw.githubusercontent.com/openstax/{repo}/{br}/{path}").decode("utf-8")


def cnxml_passages(x):
    title = re.search(r"<title>(.*?)</title>", x, re.S)
    title = C.clean_ws(re.sub(r"<[^>]+>", "", title.group(1))) if title else ""
    x = re.sub(r"(?s)<(m:math|math|note|exercise|table|figure|media|equation|example|solution|problem|"
               r"glossary|code|preformat)\b.*?</\1>", " ", x)
    paras = []
    for m in re.finditer(r"(?s)<para\b[^>]*>(.*?)</para>", x):
        t = C.clean_ws(C.strip_html(m.group(1)))
        if C.nwords(t) >= 15 and not re.search(r"[{}\\]", t):
            paras.append(t)
    out, cur = [], []
    for p in paras:
        cur.append(p)
        n = sum(C.nwords(c) for c in cur)
        if n >= 90:
            out.append("\n".join(cur))
            cur = []
    if cur and sum(C.nwords(c) for c in cur) >= 40:
        out.append("\n".join(cur))
    return title, out


def openstax():
    raw = C.load_raw("openstax")
    if raw is None:
        rng = random.Random(6)
        raw, lic_log = [], {}
        for repo in OS_BOOKS:
            br, tree = gh_tree(repo)
            time.sleep(1.0)
            if not tree:
                print("  no repo", repo, flush=True)
                continue
            paths = [t["path"] for t in tree.get("tree", [])]
            colls = [p for p in paths if p.startswith("collections/") and p.endswith(".xml")]
            mods = [p for p in paths if re.fullmatch(r"modules/m\d+/index\.cnxml", p)]
            ok_books = []
            for cpath in colls:
                cx = raw_gh(repo, br, cpath)
                lic = re.search(r'<md:license[^>]*url="([^"]+)"', cx)
                lic_url = lic.group(1) if lic else None
                lic_log[f"{repo}/{cpath}"] = lic_url
                if lic_url and CC_BY.search(lic_url):
                    ok_books.append((cpath, set(re.findall(r'document="(m\d+)"', cx)), lic_url))
            print(f"  {repo}: {len(mods)} modules, permissive collections {[(c, len(s)) for c, s, _ in ok_books]}",
                  flush=True)
            allowed = {}
            for cpath, ms, lic_url in ok_books:
                for m in ms:
                    allowed[m] = (cpath, lic_url)
            mods = [p for p in mods if p.split("/")[1] in allowed]
            rng.shuffle(mods)
            for p in mods[:110]:
                mid = p.split("/")[1]
                try:
                    x = raw_gh(repo, br, p)
                except Exception as e:  # noqa: BLE001
                    print("   skip", p, e)
                    continue
                mlic = re.search(r'<md:license[^>]*url="([^"]+)"', x)
                if mlic and not CC_BY.search(mlic.group(1)):
                    continue
                title, passages = cnxml_passages(x)
                for k, ps in enumerate(passages):
                    raw.append({"repo": repo, "module": mid, "collection": allowed[mid][0],
                                "licence_url": allowed[mid][1], "title": title, "k": k, "text": ps})
                time.sleep(0.15)
            print(f"  {repo}: {len(raw)} passages so far", flush=True)
        C.save_raw("openstax", raw)
        (C.RAW / "openstax" / "licences.json").write_text(json.dumps(lic_log, indent=1))
    rng = random.Random(7)
    by_mod = {}
    for r in raw:
        by_mod.setdefault((r["repo"], r["module"]), []).append(r)
    items = []
    for (repo, mid), rs in by_mod.items():
        rng.shuffle(rs)
        for r in rs[:3]:
            items.append({"key": f"{repo}/{mid}#{r['k']}", "text": f"{r['title']}\n{r['text']}",
                          "meta": {"repo": repo, "module": mid, "collection": r["collection"],
                                   "licence_url": r["licence_url"]}})
    st = C.finish("textbooks", "OpenStax textbooks (github.com/openstax osbooks-* repositories, CNXML modules)",
                  "https://creativecommons.org/licenses/by/4.0/", items)
    print(json.dumps(st))


if __name__ == "__main__":
    {"biorxiv": biorxiv, "aic": aic, "asklo": asklo, "openstax": openstax}[sys.argv[1]]()
