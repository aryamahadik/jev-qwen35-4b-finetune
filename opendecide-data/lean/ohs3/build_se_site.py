"""OHS-3 task "se_site" (track F, wide choice, 40 options): which Stack Exchange site was this question posted on?

Source: Stack Exchange API 2.3 (unauthenticated). Questions created on each site's main page between
2026-06-01 00:00 UTC (fromdate=1780272000) and the snapshot time recorded in cache/se_site/fetch_info.json.
Licence: each post's own `content_license` (only CC BY-SA posts kept). Site names and `audience` strings come from
/2.3/sites (official, written by Stack Exchange); card = "- <site name>: <audience>". No author-written definitions.

Label universe (fixed from question counts only, before any item text was read):
  * /2.3/sites entries with site_type == "main_site", excluding meta sites (meta.stackexchange.com = "meta",
    agents.meta.stackoverflow).
  * Overlap groups count as one site; the member with the oldest launch_date is kept, the others are dropped whole:
    {superuser, askubuntu, unix}, {math, mathoverflow.net}, {stats, datascience, ai},
    {stackoverflow, softwareengineering, codereview}, {english, ell}, {travel, expatriates}.
  * count = `total` of /2.3/questions?fromdate=2026-06-01&todate=<snapshot> (all questions created in the window).
  * sites with count >= 40, ranked by count (ties: api_site_parameter), top 40 kept.

Item pool per site: page 1 (100 newest) of the window, plus, for sites with more than 100 questions, one extra page of
100 ending at a seeded random time inside the window (so items are not all from the last days of September).
Item filters: content_license starts with "CC BY-SA"; not closed (a closed question may be off-topic, so its site
label is not reliable); score >= 0 (drops spam/unclear posts); state 20-6,000 chars; exact and
normalised-whitespace duplicates dropped, and a normalised title seen on two different sites (cross-posts) is
dropped on both.

State = "Title: <title>\n\n<body as plain text>". The body HTML is converted to text (tags removed, entities decoded,
code and list text kept, image tags dropped). Redactions (listed per row in meta.redactions):
  * any URL or bare domain of the Stack Exchange network (stackexchange.com, stackoverflow.com, superuser.com,
    serverfault.com, askubuntu.com, mathoverflow.net, stackapps.com, sstatic.net, stack.imgur.com) -> "[link]"
  * the question's own site named in text: "<name> Stack Exchange", "<name> SE", "<name>.SE", "<param>.SE",
    "<param>.stackexchange" and, for brand names that are not ordinary words (see BRAND_NAMES), the bare name
    -> "[this site]". Tags and the site name are never shown.
  * "<name> community" -> "[this site] community"; per-site community abbreviations in SITE_MARKERS (MathOverflow:
    MO -> [this site], MSE/math.SE -> [another site]; Puzzling: PSE -> [this site]).

Sampling: 142 items, stratified: floor(142/40) = 3 per site, the remaining 22 given to sites in seeded order
(random.Random(SEED)); within a site, random.Random(f"{SEED}:{site}").sample. Option order shuffled per row (seeded).

Network: only when the cache is missing (or --fetch). Raw API responses are saved under ohs3/cache/se_site/raw/, so
re-runs give identical rows.
  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python ohs3/build_se_site.py [--fetch]
"""
import hashlib
import html
import json
import random
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

import requests

SEED = 20261026
SPLIT = "ohs3"
TASK = "se_site"
TRACK = "F"
N_ITEMS = 142
N_SITES = 40
MIN_COUNT = 40
FROMDATE = 1780272000  # 2026-06-01T00:00:00Z
INSTRUCTIONS = "Which Stack Exchange site was this question posted on?"
OVERLAP_GROUPS = [
    ["superuser", "askubuntu", "unix"],
    ["math", "mathoverflow.net"],
    ["stats", "datascience", "ai"],
    ["stackoverflow", "softwareengineering", "codereview"],
    ["english", "ell"],
    ["travel", "expatriates"],
]
API = "https://api.stackexchange.com/2.3"

LEAN = Path(__file__).resolve().parents[1]
CACHE = LEAN / "ohs3" / "cache" / TASK
RAW = CACHE / "raw"
OUT = LEAN / "data" / "ohs3_parts" / f"{TASK}.jsonl"
SUMMARY = LEAN / "data" / "ohs3_parts" / f"{TASK}_summary.json"

SE_DOMAINS = r"(?:[\w-]+\.)*(?:stackexchange\.com|stackoverflow\.com|superuser\.com|serverfault\.com|askubuntu\.com|" \
             r"mathoverflow\.net|stackapps\.com|sstatic\.net|stack\.imgur\.com)"
URL_RE = re.compile(r"(?:https?://)?" + SE_DOMAINS + r"(?:/[^\s)\]>\"']*)?", re.I)

# ---------------------------------------------------------------- fetch (cached)

_last = [0.0]


def api_get(path, params, key):
    """GET with on-disk cache keyed by `key`. Returns the parsed JSON."""
    fp = RAW / f"{key}.json"
    if fp.exists():
        return json.loads(fp.read_text())
    if not ALLOW_NET[0]:
        raise SystemExit(f"cache miss for {key}; run with --fetch")
    wait = max(0.0, _last[0] - time.time())
    time.sleep(wait + 0.15)
    r = requests.get(f"{API}{path}", params=params, timeout=60)
    d = r.json()
    if "error_id" in d:
        raise SystemExit(f"API error on {key}: {d}")
    _last[0] = time.time() + float(d.get("backoff", 0))
    RAW.mkdir(parents=True, exist_ok=True)
    fp.write_text(json.dumps(d, ensure_ascii=False, sort_keys=True))
    QUOTA[0] = d.get("quota_remaining", QUOTA[0])
    return d


ALLOW_NET = [False]
QUOTA = [None]


def fetch():
    CACHE.mkdir(parents=True, exist_ok=True)
    info_p = CACHE / "fetch_info.json"
    if info_p.exists():
        info = json.loads(info_p.read_text())
    else:
        ALLOW_NET[0] = True
        now = int(time.time())
        info = {"snapshot_todate": now - now % 3600, "fetch_started": datetime.now(timezone.utc).isoformat()}
        info_p.write_text(json.dumps(info, indent=1))
    todate = info["snapshot_todate"]
    if "--fetch" in sys.argv or not (RAW / "done.flag").exists():
        ALLOW_NET[0] = True

    flt = api_get("/filters/create", {"base": "withbody", "include": ".total;question.content_license;question.closed_date;"
                                      "question.closed_reason;question.migrated_from", "unsafe": "false"}, "filter")
    filt = flt["items"][0]["filter"]

    sites, page = [], 1
    while True:
        d = api_get("/sites", {"page": page, "pagesize": 100}, f"sites_p{page}")
        sites += d["items"]
        if not d.get("has_more"):
            break
        page += 1

    main = {s["api_site_parameter"]: s for s in sites if s.get("site_type") == "main_site" and not re.search(r"(^|\.)meta(\.|$)", s["api_site_parameter"]) and "//meta." not in s["site_url"]}
    dropped = set()
    for g in OVERLAP_GROUPS:
        present = [p for p in g if p in main]
        keep = min(present, key=lambda p: (main[p]["launch_date"], p))
        dropped |= set(present) - {keep}
    universe = sorted(p for p in main if p not in dropped)

    first = {}
    for p in universe:
        first[p] = api_get("/questions", {"site": p, "fromdate": FROMDATE, "todate": todate, "sort": "creation",
                                          "order": "desc", "pagesize": 100, "page": 1, "filter": filt}, f"q_{p}_p1")
    counts = {p: first[p].get("total", 0) for p in universe}
    ranked = sorted((p for p in universe if counts[p] >= MIN_COUNT), key=lambda p: (-counts[p], p))
    chosen = sorted(ranked[:N_SITES])

    extra = {}
    for p in chosen:
        if counts[p] > 100:
            t = random.Random(f"{SEED}:{p}:todate").randint(FROMDATE + 86400, todate)
            extra[p] = (t, api_get("/questions", {"site": p, "fromdate": FROMDATE, "todate": t, "sort": "creation",
                                                  "order": "desc", "pagesize": 100, "page": 1, "filter": filt},
                                   f"q_{p}_rand"))
    if ALLOW_NET[0] and QUOTA[0] is not None:
        (RAW / "done.flag").write_text("ok")
        info.update({"fetch_finished": datetime.now(timezone.utc).isoformat(), "filter": filt,
                     "quota_remaining_after": QUOTA[0], "n_requests_cached": len(list(RAW.glob("*.json")))})
        info_p.write_text(json.dumps(info, indent=1))
    return info, main, dropped, universe, counts, ranked, chosen, first, extra


# ---------------------------------------------------------------- text

BLOCK = {"p", "div", "pre", "blockquote", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "table", "tr", "hr"}


class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.pre = [], 0

    def handle_starttag(self, tag, attrs):
        if tag == "br":
            self.out.append("\n")
        elif tag == "li":
            self.out.append("\n- ")
        elif tag in BLOCK:
            self.out.append("\n\n")
        if tag == "pre":
            self.pre += 1
        elif tag in ("td", "th"):
            self.out.append(" | ")

    def handle_endtag(self, tag):
        if tag == "pre":
            self.pre -= 1
        if tag in BLOCK:
            self.out.append("\n\n")

    def handle_data(self, data):
        self.out.append(data if self.pre else re.sub(r"[ \t\r\n]+", " ", data))


def html_to_text(s):
    p = Text()
    p.feed(s)
    p.close()
    t = "".join(p.out)
    t = "\n".join(line.rstrip() for line in t.split("\n"))
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


# Bare site names that are brands, not ordinary words, so naming them in text gives the label away.
BRAND_WORDS = re.compile(r"stack|overflow|exchange|super user|server fault|ask ubuntu|cross validated|arqade|"
                         r"seasoned advice|ask different|mathoverflow", re.I)


def redact(text, site):
    red = Counter()
    name = html.unescape(site["name"])
    param = site["api_site_parameter"]

    def sub(pat, rep, t, tag):
        n_t, k = re.subn(pat, rep, t)
        if k:
            red[tag] += k
        return n_t

    text = sub(URL_RE, "[link]", text, "se_url")
    alts = [re.escape(name) + r"\s*(?:Stack\s*Exchange|SE\b|\.SE\b)"]
    alts.append(r"\b" + re.escape(param) + r"\s*(?:\.SE\b|\.stackexchange\b|\s+Stack\s*Exchange)")
    alts.append(re.escape(name) + r"(?=\s+community\b)")  # "ask the <site> community" names the site
    if BRAND_WORDS.search(name):
        alts.append(re.escape(name))
    text = sub(re.compile(r"(?<![\w.])(?:" + "|".join(alts) + r")(?![\w])", re.I), "[this site]", text, "site_name")
    for pat, rep in SITE_MARKERS.get(param, []):
        text = sub(pat, rep, text, "site_abbrev")
    return text, dict(red)


# Community abbreviations that point at the posting site (own-site nicknames, and the sister site users cross-post
# from). Case-sensitive and per site only, because the same letters are ordinary words elsewhere (MO = molecular
# orbital, MSE = mean squared error). Added by the OHS-3 verifier after a leakage scan of the built states.
SITE_MARKERS = {
    "mathoverflow.net": [(re.compile(r"\bMO\b"), "[this site]"),
                         (re.compile(r"\b(?:MSE|M\.SE|[Mm]ath\.?\s?SE|Math Stack Exchange)\b"), "[another site]")],
    "puzzling": [(re.compile(r"\b(?:PSE|P\.SE|PSE's)\b"), "[this site]")],
}


def norm(s):
    return " ".join(re.findall(r"\w+", s.lower()))


def sid(*parts):
    return hashlib.sha1("|".join(map(str, parts)).encode()).hexdigest()[:12]


# ---------------------------------------------------------------- build

def main():
    info, main_sites, dropped, universe, counts, ranked, chosen, first, extra = fetch()
    todate = info["snapshot_todate"]
    names = {p: html.unescape(main_sites[p]["name"]) for p in chosen}
    assert len(set(names.values())) == len(names)
    aud = {p: html.unescape(main_sites[p]["audience"]).strip() for p in chosen}

    raw = defaultdict(dict)
    for p in chosen:
        for q in first[p]["items"] + (extra[p][1]["items"] if p in extra else []):
            raw[p][q["question_id"]] = q

    skipped = Counter()
    cand = defaultdict(list)
    title_sites = defaultdict(set)
    for p in chosen:
        for q in raw[p].values():
            title_sites[norm(html.unescape(q["title"]))].add(p)
    seen_state = set()
    for p in chosen:
        for qid in sorted(raw[p]):
            q = raw[p][qid]
            if not (FROMDATE <= q["creation_date"] <= todate):
                skipped["outside_window"] += 1; continue
            lic = q.get("content_license") or ""
            if not lic.startswith("CC BY-SA"):
                skipped["licence_not_cc_by_sa"] += 1; continue
            if q.get("closed_date"):
                skipped["closed"] += 1; continue
            if q.get("score", 0) < 0:
                skipped["negative_score"] += 1; continue
            title = html.unescape(q["title"]).strip()
            if len(title_sites[norm(title)]) > 1:
                skipped["cross_posted_title"] += 1; continue
            body = html_to_text(q.get("body", ""))
            state, red = redact(f"Title: {title}\n\n{body}", main_sites[p])
            if not 20 <= len(state) <= 6000 or len(body) < 1:
                skipped["length"] += 1; continue
            k = norm(state)
            if k in seen_state:
                skipped["duplicate"] += 1; continue
            seen_state.add(k)
            cand[p].append({"q": q, "state": state, "red": red, "lic": lic})

    base = N_ITEMS // N_SITES
    order = list(chosen)
    random.Random(SEED).shuffle(order)
    alloc = {p: min(base, len(cand[p])) for p in chosen}
    left = N_ITEMS - sum(alloc.values())
    while left > 0:  # remainder in seeded order, one extra per site per round
        low = min(alloc[p] for p in order if alloc[p] < len(cand[p])) if any(alloc[p] < len(cand[p]) for p in order) else None
        if low is None:
            break
        for p in order:
            if left and alloc[p] == low and alloc[p] < len(cand[p]):
                alloc[p] += 1; left -= 1

    snap_iso = datetime.fromtimestamp(todate, timezone.utc).isoformat().replace("+00:00", "Z")
    rows, per = [], {}
    for p in chosen:
        pick = random.Random(f"{SEED}:{p}").sample(cand[p], alloc[p])
        per[names[p]] = len(pick)
        for c in pick:
            q = c["q"]
            rid = "r_" + sid(SEED, SPLIT, TASK, p, q["question_id"])
            opts = [names[x] for x in chosen]
            random.Random(f"{SEED}:{rid}").shuffle(opts)
            inv = {v: k for k, v in names.items()}
            card = "\n".join(f"- {o}: {aud[inv[o]]}" for o in opts)
            rows.append({
                "id": rid, "group_id": f"g:{TASK}:{p}:{q['question_id']}", "call_id": "c_" + sid(SPLIT, c["state"]),
                "split": SPLIT, "track": TRACK, "source": TASK, "state": c["state"], "qtype": "choice",
                "instructions": INSTRUCTIONS, "options": opts, "gold": names[p], "role": "choice", "card": card,
                "meta": {"task": TASK, "dataset": "Stack Exchange API 2.3 /questions (main site)",
                         "question_id": q["question_id"], "site": p, "site_url": main_sites[p]["site_url"],
                         "link": q.get("link"), "content_license": c["lic"],
                         "creation_date": datetime.fromtimestamp(q["creation_date"], timezone.utc).isoformat()
                         .replace("+00:00", "Z"),
                         "original_label": p, "snapshot_todate": snap_iso,
                         "licence": f"{c['lic']} (per post; attribution: Stack Exchange contributors, see link)",
                         "redactions": c["red"]}})
    random.Random(SEED).shuffle(rows)

    n = len(rows)
    assert len({r["id"] for r in rows}) == n and len({r["group_id"] for r in rows}) == n
    for r in rows:
        assert r["gold"] in r["options"] and len(set(r["options"])) == len(r["options"]) == len(chosen)
        assert 20 <= len(r["state"]) <= 6000
        assert not URL_RE.search(r["state"])
    assert max(per.values()) / n <= 0.40

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows))
    dates = sorted(r["meta"]["creation_date"] for r in rows)
    summary = {
        "task": TASK, "split": SPLIT, "track": TRACK, "qtype": "choice", "n": n, "n_options": len(chosen),
        "instructions": INSTRUCTIONS,
        "source": "Stack Exchange API 2.3, /questions?site=<site>&fromdate=1780272000&todate=<snapshot>&sort=creation"
                  "&order=desc (unauthenticated), /sites for names, audience, launch_date",
        "snapshot": {"fromdate": "2026-06-01T00:00:00Z", "todate": snap_iso, **info},
        "licence": "CC BY-SA (per post content_license; " + ", ".join(
            f"{k}: {v}" for k, v in sorted(Counter(r["meta"]["content_license"] for r in rows).items())) + ")",
        "labels_source": "official: site name and 'audience' string from /2.3/sites (no author-written definitions)",
        "options": {names[p]: {"site": p, "audience": aud[p], "launch_date": main_sites[p]["launch_date"],
                               "questions_in_window": counts[p]} for p in chosen},
        "per_class": per, "max_class_share": round(max(per.values()) / n, 3),
        "item_creation_date_range": [dates[0], dates[-1]],
        "eligible_per_site": {names[p]: len(cand[p]) for p in chosen},
        "pool_per_site": {names[p]: len(raw[p]) for p in chosen},
        "extra_page_todate": {p: datetime.fromtimestamp(extra[p][0], timezone.utc).isoformat() for p in sorted(extra)},
        "skipped": dict(skipped),
        "redactions": dict(sum((Counter(r["meta"]["redactions"]) for r in rows), Counter())),
        "rows_with_redaction": sum(1 for r in rows if r["meta"]["redactions"]),
        "universe": {"main_sites": len(main_sites), "overlap_dropped": sorted(dropped),
                     "sites_counted": len(universe), "sites_with_ge_40": len(ranked),
                     "next_below_cut": [(p, counts[p]) for p in ranked[N_SITES:N_SITES + 5]]},
        "question_ids": {names[p]: sorted(r["meta"]["question_id"] for r in rows if r["meta"]["site"] == p)
                         for p in chosen},
        "seed": SEED,
    }
    SUMMARY.write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    print(json.dumps({k: summary[k] for k in ("n", "per_class", "max_class_share", "item_creation_date_range",
                                               "skipped", "redactions", "universe")}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
