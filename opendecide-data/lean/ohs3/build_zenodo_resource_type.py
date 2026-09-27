"""OHS-3 task zenodo_resource_type (label-verification yes/no form, Amendment 1).

Source: Zenodo REST API records (metadata CC0), created 2026-06-01..2026-09-26 with publication_date in the same
range. Labels: Zenodo/InvenioRDM resource-type vocabulary titles (publication and image subtypes kept as their own
labels). Definitions: DataCite Metadata Schema 4.7 resourceTypeGeneral descriptions.

Step 1 (network, once): snapshot everything into ohs3/cache/zenodo_resource_type/ (gzipped verbatim API pages, the
vocabulary, the DataCite page, and a manifest). If the manifest exists the builder never touches the network, so
re-runs give identical rows. Use --refetch to rebuild the snapshot.

Sampling of the snapshot: for every day D in the range, four 6-hour slots of `created` (UTC), each the 25 oldest
records of the slot (sort=oldest; 25 is the unauthenticated page-size cap), all with publication_date in the range.

Step 2 (offline): clean, pick the 20 most frequent labels, stratify 144 items evenly by gold label, and build 72 yes
(asked = gold) and 72 no (asked = seeded different label) rows with asked labels spread evenly.
"""
import datetime as dt
import gzip
import hashlib
import html
import json
import random
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
LEAN = HERE.parent
CACHE = HERE / "cache" / "zenodo_resource_type"
OUT = LEAN / "data" / "ohs3_parts" / "zenodo_resource_type.jsonl"
SUMMARY = LEAN / "data" / "ohs3_parts" / "zenodo_resource_type_summary.json"

TASK = "zenodo_resource_type"
SEED = 20261026
N_ITEMS = 144
N_LABELS = 20
START = dt.date(2026, 6, 1)
END = dt.date(2026, 9, 26)
PUB_Q = "publication_date:[2026-06-01 TO 2026-09-26]"
API = "https://zenodo.org/api/records"
VOCAB_URL = "https://zenodo.org/api/vocabularies/resourcetypes?size=100"
DATACITE_URL = "https://datacite-metadata-schema.readthedocs.io/en/4.7/appendices/appendix-1/resourceTypeGeneral/"
LICENCE = "CC0-1.0 (Zenodo record metadata: \"Metadata is licensed under CC0, except for email addresses\", https://about.zenodo.org/policies/)"
INSTRUCTIONS = 'Does the resource type "{label}" apply to this Zenodo record?'
UA = {"User-Agent": "OpenDecide-OHS3-builder/1.0 (research dataset build; contact via GitHub)"}


# ---------------------------------------------------------------- snapshot
def _get(url, params=None):
    for attempt in range(8):
        r = requests.get(url, params=params, headers=UA, timeout=90)
        if r.status_code == 429 or r.status_code >= 500:
            wait = 5
            reset = r.headers.get("X-RateLimit-Reset")
            if reset:
                wait = max(2, int(reset) - int(time.time()) + 1)
            time.sleep(min(wait, 90) * (1 + attempt // 3))
            continue
        r.raise_for_status()
        rem = r.headers.get("X-RateLimit-Remaining")
        reset = r.headers.get("X-RateLimit-Reset")
        if rem is not None and int(rem) <= 1 and reset:
            time.sleep(max(1, int(reset) - int(time.time()) + 1))
        return r
    raise RuntimeError(f"failed: {url} {params}")


def fetch_snapshot():
    CACHE.mkdir(parents=True, exist_ok=True)
    (CACHE / "pages").mkdir(exist_ok=True)
    man = {"fetched_start_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
           "api": API, "publication_date_query": PUB_Q, "pages": []}
    r = _get(VOCAB_URL)
    (CACHE / "vocab_resourcetypes.json").write_bytes(r.content)
    man["vocab"] = {"url": VOCAB_URL, "sha256": hashlib.sha256(r.content).hexdigest()}
    r = _get(DATACITE_URL)
    (CACHE / "datacite_4.7_resourceTypeGeneral.html").write_bytes(r.content)
    man["datacite"] = {"url": DATACITE_URL, "sha256": hashlib.sha256(r.content).hexdigest()}
    d = START
    while d <= END:
        nxt = d + dt.timedelta(days=1)
        bounds = [f"{d}T00:00:00", f"{d}T06:00:00", f"{d}T12:00:00", f"{d}T18:00:00", f"{nxt}T00:00:00"]
        for slot in range(4):
            a, b = bounds[slot], bounds[slot + 1]
            q = f"created:[{a} TO {b}}} AND {PUB_Q}"
            params = {"q": q, "sort": "oldest", "size": 25, "page": 1}
            r = _get(API, params)
            body = r.content
            name = f"{d}_s{slot}.json.gz"
            (CACHE / "pages" / name).write_bytes(gzip.compress(body, mtime=0))
            js = json.loads(body)
            man["pages"].append({"file": name, "url": r.url, "q": q, "n": len(js["hits"]["hits"]),
                                 "total": js["hits"]["total"], "sha256": hashlib.sha256(body).hexdigest()})
            print(name, len(js["hits"]["hits"]), js["hits"]["total"], flush=True)
            time.sleep(0.5)
        d = nxt
    man["fetched_end_utc"] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    (CACHE / "manifest.json").write_text(json.dumps(man, indent=1))


# ---------------------------------------------------------------- definitions
def datacite_defs():
    s = (CACHE / "datacite_4.7_resourceTypeGeneral.html").read_text()
    defs = {}
    for m in re.finditer(r"<h2>([A-Za-z]+)<a[^>]*>[^<]*</a></h2>\s*<p><strong>Description:</strong>(.*?)</p>", s, re.S):
        defs[m.group(1)] = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", m.group(2)))).strip()
    return defs


# DataCite's "Other" entry reads only "If selected, supply a value for ResourceType." (a usage note), so these three
# definitions are author-written once and frozen (listed in the summary).
AUTHOR_DEFS = {
    "other": "A resource that is not covered by any other resource type in the vocabulary.",
    "publication-other": "A publication (textual resource) that is not covered by any other publication subtype.",
    "image-other": "An image (visual representation other than text) that is not covered by any other image subtype.",
}


def label_table():
    """id -> (label, definition, datacite general used)."""
    voc = json.loads((CACHE / "vocab_resourcetypes.json").read_text())["hits"]["hits"]
    dc = datacite_defs()
    titles = Counter(h["title"]["en"] for h in voc)
    tab = {}
    for h in voc:
        rid, title = h["id"], h["title"]["en"]
        label = title
        if titles[title] > 1 and "-" in rid:  # duplicate titles ("Other"): name the parent type
            label = f"{title} ({rid.split('-')[0]})"
        props = h.get("props", {})
        gen, typ = props.get("datacite_general", ""), props.get("datacite_type", "")
        camel = re.sub(r"[^A-Za-z]", "", title.title())
        use = camel if camel in dc else gen  # DataCite 4.7 has its own general type (e.g. Poster) -> use it
        if use not in dc:
            raise KeyError(f"no DataCite definition for {rid} ({use})")
        definition = dc[use]
        if rid in AUTHOR_DEFS:  # DataCite "Other" has only a usage note, no definition
            tab[rid] = (label, AUTHOR_DEFS[rid], "author-written")
            continue
        if use != camel:  # label is a subtype of a broader DataCite type: say so
            definition += f" (DataCite resourceTypeGeneral {use}" + (f"; resourceType \"{typ}\")" if typ else ")")
        tab[rid] = (label, definition, use)
    return tab


# ---------------------------------------------------------------- cleaning
def strip_html(s):
    s = re.sub(r"(?i)<br\s*/?>|</p>|</li>|</h\d>|</div>", "\n", s or "")
    s = re.sub(r"(?i)<li[^>]*>", "- ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s).replace("\xa0", " ")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r" *\n *", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def norm(s):
    return re.sub(r"\s+", " ", s).strip().lower()


def load_records():
    man = json.loads((CACHE / "manifest.json").read_text())
    recs = {}
    for p in man["pages"]:
        body = gzip.decompress((CACHE / "pages" / p["file"]).read_bytes())
        assert hashlib.sha256(body).hexdigest() == p["sha256"], p["file"]
        for h in json.loads(body)["hits"]["hits"]:
            recs[h["id"]] = h
    return man, list(recs.values())


def rid_of(md):
    rt = md.get("resource_type") or {}
    return rt.get("type", "") + (f"-{rt['subtype']}" if rt.get("subtype") else "")


def cut_state(title, desc):
    head = f"Title: {title}\n\nDescription: "
    s = head + desc
    if len(s) > 6000:  # trim at a sentence/line boundary, never mid-word
        room = 6000 - len(head) - 4
        cut = desc[:room]
        k = max(cut.rfind("\n"), cut.rfind(". "))
        cut = cut[:k + 1] if k > room * 0.6 else cut[:cut.rfind(" ")]
        s = head + cut.rstrip() + " ..."
    return s


def main():
    if "--refetch" in sys.argv or not (CACHE / "manifest.json").exists():
        fetch_snapshot()
    man, raw = load_records()
    tab = label_table()
    stats = {"raw_unique_records": len(raw)}

    # created >= 2026-06-01, publication_date in range, known resource type
    recs = []
    for h in raw:
        md = h["metadata"]
        pd = md.get("publication_date", "")
        if not (h["created"][:10] >= "2026-06-01" and "2026-06-01" <= pd[:10] <= "2026-09-26"):
            continue
        rid = rid_of(md)
        if rid not in tab:
            continue
        recs.append(h)
    stats["in_range_known_type"] = len(recs)
    recs.sort(key=lambda h: (h["created"], h["id"]))  # earliest first for "keep the earliest"

    kept, seen_title, seen_concept, seen_desc = [], set(), set(), set()
    drop = Counter()
    for h in recs:
        md = h["metadata"]
        title = strip_html(md.get("title", ""))
        desc = strip_html(md.get("description", ""))
        if len(desc) < 20:
            drop["empty_or_short_description"] += 1
            continue
        # track F: the text must be first published in range. A later version (index > 0) of a concept may repeat
        # text from an earlier version created before 2026-06-01, so keep only first versions (index 0).
        ver = ((md.get("relations") or {}).get("version") or [{}])[0]
        if ver.get("index", 0) != 0:
            drop["not_first_version_of_concept"] += 1
            continue
        c = h.get("conceptrecid") or str(h["id"])
        if c in seen_concept:
            drop["version_duplicate_conceptrecid"] += 1
            continue
        seen_concept.add(c)
        if norm(title) in seen_title:
            drop["duplicate_title"] += 1
            continue
        seen_title.add(norm(title))
        if norm(desc) in seen_desc:
            drop["duplicate_description"] += 1
            continue
        seen_desc.add(norm(desc))
        state = cut_state(title, desc)
        if not (20 <= len(state) <= 6000):
            drop["state_length"] += 1
            continue
        kept.append((h, rid_of(md), state))
    stats["dropped"] = dict(drop)
    stats["clean_pool"] = len(kept)

    freq = Counter(r for _, r, _ in kept)
    top = [r for r, _ in sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[:N_LABELS]]
    stats["clean_pool_label_freq"] = {tab[r][0]: n for r, n in freq.most_common()}
    labels = {r: tab[r][0] for r in top}
    assert len(set(labels.values())) == len(labels)

    rng = random.Random(SEED)
    # --- stratify gold evenly over the 20 labels
    base, rem = divmod(N_ITEMS, len(top))
    order = sorted(top)
    rng.shuffle(order)
    quota = {r: base + (1 if i < rem else 0) for i, r in enumerate(order)}
    by = defaultdict(list)
    for h, r, s in kept:
        if r in labels:
            by[r].append((h, r, s))
    short = {labels[r]: (len(by[r]), quota[r]) for r in top if len(by[r]) < quota[r]}
    if short:  # give missing quota to the labels with spare items (fewest assigned first), keeping the total
        for r in top:
            quota[r] = min(quota[r], len(by[r]))
        need = N_ITEMS - sum(quota.values())
        while need > 0:
            rich = sorted([r for r in top if len(by[r]) > quota[r]], key=lambda r: (quota[r], r))
            quota[rich[0]] += 1
            need -= 1
    items = []
    for r in sorted(top):
        pool = sorted(by[r], key=lambda x: x[0]["id"])
        items += rng.sample(pool, quota[r])

    # --- yes/no split: exactly half, and within each gold label as even as possible
    rng.shuffle(items)
    items.sort(key=lambda x: x[1])
    yes_flags, carry = [], 0
    for r in sorted(top):
        grp = [x for x in items if x[1] == r]
        n = len(grp)
        k = n // 2
        if n % 2:
            k += carry
            carry = 1 - carry
        flags = [1] * k + [0] * (n - k)
        rng.shuffle(flags)
        yes_flags += flags
    assert sum(yes_flags) == N_ITEMS // 2, sum(yes_flags)

    def related(a, b):
        # parent/child in the vocabulary (e.g. publication vs publication-article), or two image subtypes
        # (figure/plot/diagram/drawing/photo overlap and share one DataCite definition): both could apply
        same = a.split("-")[0] == b.split("-")[0]
        return same and ("-" not in a or "-" not in b or a.startswith("image"))

    asked_n = Counter()
    for (h, r, s), f in zip(items, yes_flags):
        if f:
            asked_n[r] += 1
    idx = list(range(len(items)))
    rng.shuffle(idx)
    asked = {}
    for i in idx:
        h, r, s = items[i]
        if yes_flags[i]:
            asked[i] = r
            continue
        cands = [c for c in top if c != r and not related(c, r)]
        m = min(asked_n[c] for c in cands)
        pick = rng.choice(sorted(c for c in cands if asked_n[c] == m))
        asked[i] = pick
        asked_n[pick] += 1

    snap = f"{man['fetched_start_utc']} .. {man['fetched_end_utc']}"
    rows = []
    for i, (h, r, s) in enumerate(items):
        a = asked[i]
        md = h["metadata"]
        rec_id = str(h["id"])
        gid = f"g:{TASK}:{rec_id}"
        rid_ = "r_" + hashlib.sha256(f"{TASK}|{rec_id}|{a}".encode()).hexdigest()[:12]
        cid = "c_" + hashlib.sha256(f"{TASK}|call|{rec_id}".encode()).hexdigest()[:12]
        rows.append({
            "id": rid_, "group_id": gid, "call_id": cid, "split": "ohs3", "track": "F", "source": TASK,
            "state": s, "qtype": "noul", "instructions": INSTRUCTIONS.format(label=labels[a]),
            "options": None, "gold": 1 if a == r else 0, "role": "aff",
            "card": f"- {labels[a]}: {tab[a][1]}",
            "meta": {
                "task": TASK, "dataset": "Zenodo REST API records", "record_id": rec_id,
                "conceptrecid": h.get("conceptrecid"), "doi": h.get("doi") or md.get("doi"),
                "url": f"https://zenodo.org/records/{rec_id}", "api_url": f"https://zenodo.org/api/records/{rec_id}",
                "publication_date": md.get("publication_date"), "created": h["created"],
                "record_revision": h.get("revision"), "resource_type_id": r, "original_label": labels[r],
                "asked_label": labels[a], "asked_resource_type_id": a,
                "definition_source": f"DataCite Metadata Schema 4.7 resourceTypeGeneral: {tab[a][2]}",
                "licence": LICENCE, "record_content_licence": (md.get("license") or {}).get("id"),
                "snapshot_utc": snap,
            },
        })
    rows.sort(key=lambda x: x["id"])
    assert len({x["group_id"] for x in rows}) == len(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    gold_c = Counter(x["gold"] for x in rows)
    L = [len(x["state"]) for x in rows]
    summ = {
        "task": TASK, "rows": len(rows), "qtype": "noul", "form": "label-verification yes/no (Amendment 1)",
        "track": "F", "gold_balance": {"yes(1)": gold_c[1], "no(0)": gold_c[0]},
        "gold_label_counts": dict(sorted(Counter(x["meta"]["original_label"] for x in rows).items())),
        "asked_label_counts": dict(sorted(Counter(x["meta"]["asked_label"] for x in rows).items())),
        "asked_label_counts_no_rows": dict(sorted(Counter(x["meta"]["asked_label"] for x in rows if x["gold"] == 0).items())),
        "label_set": {labels[r]: {"resource_type_id": r, "definition": tab[r][1], "datacite_general": tab[r][2]}
                      for r in top},
        "created_range": [min(x["meta"]["created"] for x in rows), max(x["meta"]["created"] for x in rows)],
        "publication_date_range": [min(x["meta"]["publication_date"] for x in rows),
                                   max(x["meta"]["publication_date"] for x in rows)],
        "state_chars": {"min": min(L), "max": max(L), "mean": round(sum(L) / len(L))},
        "licence": LICENCE,
        "record_content_licences_in_rows": dict(Counter(x["meta"]["record_content_licence"] for x in rows).most_common()),
        "source": {"api": API, "query": f"created:[D+6h*k TO D+6h*(k+1)}} AND {PUB_Q}, sort=oldest, size=25, page=1, "
                   "four 6h slots per day, 2026-06-01..2026-09-26",
                   "snapshot_utc": snap, "pages": len(man["pages"]), "manifest": str(CACHE / "manifest.json"),
                   "vocabulary": VOCAB_URL, "definitions": DATACITE_URL},
        "labels_source": "official: Zenodo/InvenioRDM resource-type vocabulary titles (live API vocabulary); "
                         "definitions from DataCite Metadata Schema 4.7 resourceTypeGeneral descriptions",
        "author_written_definitions": {labels[r]: tab[r][1] for r in top if tab[r][2] == "author-written"},
        "seed": SEED, "cleaning": stats,
        "notes": [
            "Duplicate vocabulary title 'Other' is disambiguated by parent type, e.g. 'Other (publication)'.",
            "Where DataCite 4.7 has a general type matching the Zenodo title (e.g. Poster, Presentation), its "
            "definition is used; otherwise the definition of Zenodo's mapped datacite_general, with the mapping "
            "noted in the card.",
            "Wrong asked labels are never a parent/child of the gold in the vocabulary (e.g. 'Publication' vs "
            "'Journal article') nor another image subtype when the gold is an image type, since both could apply.",
            "States: 'Title: ...\\n\\nDescription: ...', HTML stripped, source text only; trimmed at a sentence "
            "boundary with ' ...' only if above 6,000 chars.",
            "Labels are uploader-chosen on Zenodo, so some gold labels are noisy (e.g. Preprint vs Journal article, "
            "a paper filed as Poster).",
            "Only record metadata (title, description) is used; Zenodo licenses all metadata CC0. The record's own "
            "content licence (files) varies and is kept in meta.record_content_licence; a few are NC/ND, which "
            "does not apply to the metadata text.",
            "Snapshot: unauthenticated API caps page size at 25, so the pool is 25 records x 4 six-hour created "
            "slots x 118 days (11,800 records), the oldest in each slot; not a uniform random sample of Zenodo.",
            "Extra cleaning beyond the spec: exact/normalised duplicate descriptions dropped (section 8 dedup).",
            "Track F: only first versions of a Zenodo concept (metadata.relations.version index 0) are kept. Later "
            "versions can carry text first published before 2026-06-01 (verification found 10 such rows in the "
            "first build, concepts dating back to 2024-2026-05), so they are dropped.",
            "Instructions are one fixed template with the asked label filled in.",
        ],
    }
    SUMMARY.write_text(json.dumps(summ, indent=1, ensure_ascii=False))
    print(json.dumps(summ, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
