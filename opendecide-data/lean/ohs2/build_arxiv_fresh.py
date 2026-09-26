"""OHS-2 part "arxiv_fresh" (track F): arXiv papers first submitted on/after 2026-09-21, single-category only.

Tasks (one per archive group, 60 papers each, spread as evenly as availability allows over the chosen categories):
  arxiv_fresh_cs        the 15 cs.* categories with most eligible papers (4 each)
  arxiv_fresh_math      the 12 math.* categories with most eligible papers (5 each)
  arxiv_fresh_stat_eess every stat.* / eess.* category with >= 5 eligible papers
  arxiv_fresh_astro     every astro-ph.* category with >= 5 eligible papers
State = "Title: ...\n\nAbstract: ..." (arXiv's own text, whitespace-normalised). Options = official category names and
card = official descriptions, both from https://arxiv.org/category_taxonomy. Gold = the paper's only category.
No LLM-written text: instructions are one fixed template string. Licence: arXiv metadata is CC0 1.0.

Selection rules (set from category counts only; no model was run and item texts were not used to choose them):
  * v1 `published` date (UTC) >= 2026-09-21; exactly one <category> tag (no cross-lists) and primary == that tag.
    The API lists only the canonical id of an alias pair (math.NA=cs.NA, eess.SY=cs.SY, cs.IT=math.IT,
    math.ST=stat.TH), which is one category, not a cross-list, so such papers stay eligible.
  * catch-all categories excluded (cs.OH, cs.GL, math.GM, stat.OT): their gold is "does not fit elsewhere".
  * withdrawn papers, papers naming a system under test (Jev, OpenDecide, TypeSafe), states outside 20-6,000
    chars, and duplicate titles/abstracts are dropped.
  * categories ranked by eligible count (ties by id); cs/math take the top K, stat+eess/astro take all with >= 5.
  * 60 per task allocated by water-filling (each category gets an equal share, capped by what it has; leftover
    units go to the categories with most papers); sample within each category with random.Random(SEED);
    option order shuffled per row (seeded).

Network: arXiv API with >= 3 s between requests. The fetched pool and taxonomy are cached in ohs2/arxiv_fresh_cache/
so the build is reproducible; pass --fetch to refresh the snapshot.
  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python ohs2/build_arxiv_fresh.py [--fetch]
"""
import hashlib
import html
import json
import random
import re
import sys
import time
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import httpx

SEED = 20261010
PART = "arxiv_fresh"
TRACK = "F"
SPLIT = "ohs2"
MIN_DATE = "2026-09-21"
HERE = Path(__file__).resolve().parent
LEAN = HERE.parent
CACHE = HERE / "arxiv_fresh_cache"
OUT = LEAN / "data" / "ohs2_parts" / f"{PART}.jsonl"
API = "https://export.arxiv.org/api/query"
TAXONOMY_URL = "https://arxiv.org/category_taxonomy"
ARCHIVES = ["cs", "math", "stat", "eess", "astro-ph"]
CATCH_ALL = {"cs.OH", "cs.GL", "math.GM", "stat.OT"}
BANNED_WORDS = re.compile(r"\bjev|jev\b|opendecide|typesafe", re.I)  # also Jev-Mem, NumericJev, JEVQA
# arXiv withdrawal notices ("This paper has been withdrawn by the author...", "Withdrawn."), not any use of the word
# (a bare \bwithdrawn\b dropped real papers, e.g. 2609.26427 "may credit content later withdrawn").
WITHDRAWN = re.compile(r"^\W*withdrawn\b|\b(?:this|the)\s+(?:paper|article|manuscript|submission|preprint|work|version)\s+"
                       r"(?:has\s+been|have\s+been|is|was|is\s+being)\s+withdrawn\b|\bwithdrawn\s+by\s+(?:the\s+)?"
                       r"(?:authors?|arxiv|administrators?|admins?)\b", re.I)
# task -> (archives, number of categories K (None = every category with >= MIN_PER_CLASS eligible papers))
TASKS = {
    "arxiv_fresh_cs": (["cs"], 15),
    "arxiv_fresh_math": (["math"], 12),
    "arxiv_fresh_stat_eess": (["stat", "eess"], None),
    "arxiv_fresh_astro": (["astro-ph"], None),
}
TARGET_PER_TASK = 60
MIN_PER_CLASS = 5  # for the "all eligible" tasks, a category needs at least this many papers to be used
INSTRUCTIONS = "Which arXiv category is this paper filed under?"
NS = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom",
      "os": "http://a9.com/-/spec/opensearch/1.1/"}

_last = [0.0]


def get(url, **params):
    for attempt in range(6):
        wait = 3.1 - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        try:
            r = httpx.get(url, params=params, timeout=120, follow_redirects=True,
                          headers={"User-Agent": "opendecide-ohs2-builder (research benchmark)"})
            if r.status_code == 200:
                return r.text
            print(f"  HTTP {r.status_code}, retry {attempt + 1}", file=sys.stderr)
        except httpx.HTTPError as e:
            print(f"  {type(e).__name__}, retry {attempt + 1}", file=sys.stderr)
        time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"failed: {url} {params}")


def fetch_taxonomy():
    t = get(TAXONOMY_URL)
    pat = re.compile(r'<h4>([a-z\-]+(?:\.[A-Za-z\-]+)?) <span>\((.*?)\)</span></h4>\s*</div>\s*<div class="column">(.*?)</div>', re.S)
    cats = {}
    for cid, name, desc in pat.findall(t):
        d = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", desc))).strip()
        cats[cid] = {"name": html.unescape(name).strip(), "description": d}
    arch = {}  # archive display names, e.g. stat -> Statistics
    for gid, gname in re.findall(r'id="accordion-head-grp_([a-z\-]+)">.*?</span>\s*(.*?)\s*</button>', t, re.S):
        arch[gid] = html.unescape(gname).strip()
    return {"categories": cats, "groups": arch, "fetched": datetime.now(timezone.utc).isoformat()}


def norm(s):
    return re.sub(r"\s+", " ", s or "").strip()


def fetch_archive(arch):
    q = f"cat:{arch}.* AND submittedDate:[{MIN_DATE.replace('-', '')}0000 TO 202612312359]"
    out, start, total, page = {}, 0, None, 500
    while total is None or start < total:
        for tries in range(5):
            x = get(API, search_query=q, start=start, max_results=page, sortBy="submittedDate", sortOrder="ascending")
            root = ET.fromstring(x)
            total = int(root.find("os:totalResults", NS).text)
            entries = root.findall("a:entry", NS)
            if entries or start >= total:
                break
            print(f"  empty page at {start}/{total}, retrying", file=sys.stderr)
        for e in entries:
            aid = e.find("a:id", NS).text.rsplit("/abs/", 1)[-1]
            base = re.sub(r"v\d+$", "", aid)
            out[base] = {"arxiv_id": base, "version_id": aid, "title": norm(e.find("a:title", NS).text),
                         "abstract": norm(e.find("a:summary", NS).text), "published": e.find("a:published", NS).text,
                         "updated": e.find("a:updated", NS).text,
                         "primary": e.find("arxiv:primary_category", NS).get("term"),
                         "categories": [c.get("term") for c in e.findall("a:category", NS)]}
        print(f"  {arch}: {start + len(entries)}/{total}", file=sys.stderr)
        start += page
    return list(out.values())


def load(fetch):
    CACHE.mkdir(exist_ok=True)
    tp, pp = CACHE / "taxonomy.json", CACHE / "pool.jsonl"
    if fetch or not (tp.exists() and pp.exists()):
        tax = fetch_taxonomy()
        pool = {}
        for a in ARCHIVES:
            for x in fetch_archive(a):
                pool[x["arxiv_id"]] = x
        tp.write_text(json.dumps(tax, indent=1, ensure_ascii=False))
        pp.write_text("".join(json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n" for x in sorted(pool.values(), key=lambda x: x["arxiv_id"])))
        (CACHE / "fetch_info.json").write_text(json.dumps({"fetched": datetime.now(timezone.utc).isoformat(), "pool": len(pool),
                                                           "query": f"cat:<archive>.* AND submittedDate >= {MIN_DATE}"}, indent=1))
    return json.loads(tp.read_text()), [json.loads(l) for l in open(pp)]


def sid(*parts):
    return hashlib.sha1("|".join(map(str, parts)).encode()).hexdigest()[:12]


def allocate(avail, total):
    """Water-filling: hand out `total` one at a time to the category with the fewest so far (ties: more available,
    then id), skipping categories that are exhausted."""
    alloc = {c: 0 for c in avail}
    for _ in range(total):
        open_ = sorted((c for c in avail if alloc[c] < avail[c]), key=lambda c: (alloc[c], -avail[c], c))
        if not open_:
            break
        alloc[open_[0]] += 1
    return alloc


def option_name(cid, tax):
    """Official category name; stat.* names are generic ("Applications", "Methodology"), so they carry the official
    archive name in parentheses, e.g. "Applications (Statistics)"."""
    name = tax["categories"][cid]["name"]
    if cid.startswith("stat."):
        name = f"{name} ({tax['groups'].get('stat', 'Statistics')})"
    return name


def main():
    tax, pool = load("--fetch" in sys.argv)
    skipped = Counter()
    elig = defaultdict(list)
    seen_t, seen_a = set(), set()
    for x in sorted(pool, key=lambda x: x["arxiv_id"]):
        if x["published"][:10] < MIN_DATE:
            skipped["submitted_before_2026-09-21"] += 1; continue
        if len(x["categories"]) != 1 or x["categories"][0] != x["primary"]:
            skipped["cross_listed"] += 1; continue
        c = x["primary"]
        if c.split(".")[0] not in ARCHIVES or c not in tax["categories"]:
            skipped["other_archive"] += 1; continue
        if c in CATCH_ALL:
            skipped["catch_all_category"] += 1; continue
        if WITHDRAWN.search(x["abstract"]) or len(x["abstract"]) < 20:
            skipped["withdrawn_or_empty"] += 1; continue
        if BANNED_WORDS.search(x["title"] + " " + x["abstract"]):
            skipped["mentions_system_under_test"] += 1; continue
        state = f"Title: {x['title']}\n\nAbstract: {x['abstract']}"
        if not 20 <= len(state) <= 6000:
            skipped["length"] += 1; continue
        kt, ka = " ".join(re.findall(r"[a-z0-9]+", x["title"].lower())), " ".join(re.findall(r"[a-z0-9]+", x["abstract"].lower()))
        if kt in seen_t or ka in seen_a:
            skipped["duplicate"] += 1; continue
        seen_t.add(kt); seen_a.add(ka)
        elig[c].append({**x, "state": state})

    rows, report = [], {}
    for task, (archs, K) in TASKS.items():
        counts = sorted(((len(v), c) for c, v in elig.items() if c.split(".")[0] in archs), key=lambda t: (-t[0], t[1]))
        usable = [c for n, c in counts if n >= MIN_PER_CLASS]
        cats = sorted(usable[:K] if K else usable)
        alloc = allocate({c: len(elig[c]) for c in cats}, TARGET_PER_TASK)
        names = {c: option_name(c, tax) for c in cats}
        assert len(set(names.values())) == len(names), names
        rng = random.Random(f"{SEED}:{task}")
        per = {}
        for c in cats:
            pick = rng.sample(sorted(elig[c], key=lambda x: x["arxiv_id"]), alloc[c])
            per[c] = len(pick)
            for x in pick:
                rid = "r_" + sid(SEED, SPLIT, PART, task, x["arxiv_id"])
                opts = [names[k] for k in cats]
                random.Random(f"{SEED}:{rid}").shuffle(opts)
                inv = {v: k for k, v in names.items()}
                card = "\n".join(f"- {o}: {tax['categories'][inv[o]]['description'] or o}" for o in opts)
                rows.append({"id": rid, "group_id": f"g:{PART}:{x['arxiv_id']}", "call_id": "c_" + sid(SPLIT, x["state"]),
                             "split": SPLIT, "track": TRACK, "source": task, "state": x["state"], "qtype": "choice",
                             "instructions": INSTRUCTIONS, "options": opts, "gold": names[c], "role": "choice", "card": card,
                             "meta": {"part": PART, "task": task, "arxiv_id": x["arxiv_id"], "version": x["version_id"],
                                      "category": c, "published": x["published"], "url": f"https://arxiv.org/abs/{x['arxiv_id']}",
                                      "licence": "CC0-1.0 (arXiv metadata)"}})
        n = sum(per.values())
        report[task] = {"source": f"arXiv API ({'+'.join(a + '.*' for a in archs)}), v1 submitted >= {MIN_DATE}",
                        "licence": "CC0-1.0 (arXiv metadata); taxonomy text from arxiv.org/category_taxonomy",
                        "split": "none (live API snapshot, see ohs2/arxiv_fresh_cache/fetch_info.json)", "n": n,
                        "options": {c: names[c] for c in cats}, "per_class": per,
                        "max_class_share": round(max(per.values()) / n, 3) if n else None,
                        "eligible_per_category": {c: m for m, c in counts},
                        "not_used_categories": [c for m, c in counts if c not in cats]}
    random.Random(SEED).shuffle(rows)
    # validation
    assert len({r["id"] for r in rows}) == len(rows)
    assert len({r["group_id"] for r in rows}) == len(rows)
    for r in rows:
        assert r["gold"] in r["options"] and len(set(r["options"])) == len(r["options"])
        assert 20 <= len(r["state"]) <= 6000
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows))
    summ = {"part": PART, "rows": len(rows), "tasks": report, "skipped_pool": dict(skipped), "pool": len(pool)}
    (CACHE / "summary.json").write_text(json.dumps(summ, indent=1, ensure_ascii=False))
    print(json.dumps(summ, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
