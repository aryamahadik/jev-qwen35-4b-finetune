#!/usr/bin/env python
"""OHS-3 part: uk_wq_answering_body (choice, track F).

Source: UK Parliament Written Questions API, questions tabled 2026-06-01..2026-09-26
        (Open Parliament Licence v3.0).
Labels: answeringBodyName, capped at the 20 most frequent bodies in the snapshot.
Cards:  GOV.UK organisation "what we do" text (www.gov.uk/api/content/government/organisations/<slug>,
        details.body), Open Government Licence v3.0.

Determinism: the first run saves a raw snapshot under ohs3/cache/uk_wq_answering_body/ (all API pages
and the GOV.UK organisation records). Later runs read only the snapshot, so rows are identical.
Pass --refresh to re-download (this changes the snapshot).

No model predictions, results or LLM APIs are used.
"""
import argparse
import datetime as dt
import gzip
import hashlib
import html
import json
import random
import re
import sys
import time
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import requests

LEAN = Path(__file__).resolve().parents[1]
CACHE = LEAN / "ohs3" / "cache" / "uk_wq_answering_body"
OUT_DIR = LEAN / "data" / "ohs3_parts"
OUT = OUT_DIR / "uk_wq_answering_body.jsonl"
SUMMARY = OUT_DIR / "uk_wq_answering_body_summary.json"

TASK = "uk_wq_answering_body"
SEED = 20261026
N_ITEMS = 142
N_LABELS = 20
DATE_FROM, DATE_TO = "2026-06-01", "2026-09-26"
API = "https://questions-statements-api.parliament.uk/api/writtenquestions/questions"
PAGE = 1000  # the API accepts take=1000; same records as take=100 pages, fewer requests
GOVUK_CONTENT = "https://www.gov.uk/api/content/government/organisations/{slug}"
GOVUK_ORG = "https://www.gov.uk/api/organisations/{slug}"
UA = {"User-Agent": "OpenDecide-OHS3-builder (research; public data)"}

LICENCE_Q = "Open Parliament Licence v3.0 (https://www.parliament.uk/site-information/copyright-parliament/open-parliament-licence/)"
LICENCE_CARD = "Open Government Licence v3.0 (GOV.UK content)"
INSTRUCTIONS = "Which government department answers this parliamentary written question?"

# answeringBodyId -> GOV.UK organisation slug (fixed by hand from GOV.UK organisation pages; a body missing
# here or without a GOV.UK "what we do" text would get a frozen author-written definition instead).
SLUGS = {
    53: "cabinet-office",
    60: "department-for-education",
    215: "department-for-energy-security-and-net-zero",
    13: "department-for-environment-food-rural-affairs",
    27: "department-for-transport",
    29: "department-for-work-pensions",
    17: "department-of-health-and-social-care",
    208: "foreign-commonwealth-development-office",
    14: "hm-treasury",
    1: "home-office",
    11: "ministry-of-defence",
    7: "ministry-of-housing-communities-local-government",
    54: "ministry-of-justice",
    21: "northern-ireland-office",
    2: "scotland-office",
    28: "wales-office",
    88: "attorney-generals-office",
    220: "department-for-business-innovation-science-and-trade",
    10: "department-for-digital-culture-media-and-sport",
    31: "office-for-equality-and-opportunity",  # supports the Minister for Women and Equalities
    214: "department-for-business-and-trade",
    216: "department-for-science-innovation-and-technology",
    217: "department-for-culture-media-and-sport",
}

# Machinery-of-government change inside the window (July 2026): DBT (214) and DSIT (216) were replaced by the
# Department for Business, Innovation, Science and Trade (220), and DCMS (217) by the Department for Digital,
# Culture, Media and Sport (10; digital moved from DSIT). The API shows no question tabled to 214/216/217 after
# 2026-07-14, and GOV.UK marks DCMS (217) as 'replaced' on 2026-07-20. A June question to DSIT or DBT would now
# go to 220 or 10, so its gold cannot be decided from the text next to the successor options. Questions answered
# by these superseded bodies are dropped, and they are not labels. Same-id renames are merged under the latest
# name (id 88: 'Attorney General' -> "Attorney General's Office"). Checked against the data in main().
SUPERSEDED = {214: "Department for Business and Trade", 216: "Department for Science, Innovation and Technology",
              217: "Department for Culture, Media and Sport"}
SUPERSEDED_LAST_DATE = "2026-07-14"

def get_json(url, params=None, tries=6):
    for k in range(tries):
        try:
            r = requests.get(url, params=params, headers=UA, timeout=120)
            if r.status_code == 404:
                return None
            r.raise_for_status()
            return r.json()
        except Exception as e:  # noqa: BLE001
            if k == tries - 1:
                raise
            print(f"retry {k+1} {url}: {e}", file=sys.stderr)
            time.sleep(3 * (k + 1))


# ---------------------------------------------------------------- snapshot
def fetch_questions():
    params = {"tabledWhenFrom": DATE_FROM, "tabledWhenTo": DATE_TO, "take": PAGE, "skip": 0}
    first = get_json(API, params)
    total = first["totalResults"]
    recs = {r["value"]["id"]: r["value"] for r in first["results"]}
    skip = PAGE
    while skip < total:
        params["skip"] = skip
        d = get_json(API, params)
        for r in d["results"]:
            recs[r["value"]["id"]] = r["value"]
        skip += PAGE
        print(f"  fetched {min(skip, total)}/{total} (unique {len(recs)})", file=sys.stderr)
    return total, recs


def snapshot(refresh=False):
    qpath = CACHE / "questions.jsonl.gz"
    mpath = CACHE / "snapshot_meta.json"
    if qpath.exists() and mpath.exists() and not refresh:
        meta = json.loads(mpath.read_text())
        with gzip.open(qpath, "rt", encoding="utf-8") as f:
            recs = [json.loads(l) for l in f]
        return meta, recs
    CACHE.mkdir(parents=True, exist_ok=True)
    started = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    # the API's default order can shift while paging; repeat until every id is collected
    for attempt in range(4):
        total, recs = fetch_questions()
        if len(recs) >= total:
            break
        print(f"  attempt {attempt}: {len(recs)} unique of {total}; refetching", file=sys.stderr)
    recs = [recs[k] for k in sorted(recs)]
    with gzip.open(qpath, "wt", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    meta = {
        "api": API,
        "params": {"tabledWhenFrom": DATE_FROM, "tabledWhenTo": DATE_TO, "take": PAGE},
        "snapshot_started_utc": started,
        "snapshot_finished_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "total_results_reported": total,
        "unique_records": len(recs),
        "sha256_questions_jsonl_gz_payload": hashlib.sha256(
            "\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in recs).encode()).hexdigest(),
        "licence": LICENCE_Q,
    }
    mpath.write_text(json.dumps(meta, indent=1))
    return meta, recs


def org_snapshot(bodies, refresh=False):
    opath = CACHE / "govuk_organisations.json"
    cached = json.loads(opath.read_text()) if opath.exists() and not refresh else {}
    changed = False
    for b in bodies:
        slug = SLUGS.get(b)  # b is an answeringBodyId
        if not slug or slug in cached:
            continue
        content = get_json(GOVUK_CONTENT.format(slug=slug))
        org = get_json(GOVUK_ORG.format(slug=slug))
        cached[slug] = {
            "fetched_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "content_url": GOVUK_CONTENT.format(slug=slug),
            "org_url": GOVUK_ORG.format(slug=slug),
            "title": (content or {}).get("title"),
            "description": (content or {}).get("description"),
            "body": ((content or {}).get("details") or {}).get("body"),
            "acronym": ((content or {}).get("details") or {}).get("acronym"),
            "public_updated_at": (content or {}).get("public_updated_at"),
            "web_url": (org or {}).get("web_url"),
            "format": (org or {}).get("format"),
        }
        changed = True
    if changed:
        opath.write_text(json.dumps(cached, indent=1, ensure_ascii=False, sort_keys=True))
    return cached


LIST_TRUNC = 255  # the list endpoint cuts questionText at 255 characters; full text comes from /questions/{id}


def skeleton(s):
    return re.sub(r"[\W_]+", "", unicodedata.normalize("NFKC", s or "")).lower()


def full_text_snapshot(ids, refresh=False):
    """Full question records for the picked ids (the list endpoint truncates questionText)."""
    fpath = CACHE / "full_questions.json"
    cached = json.loads(fpath.read_text()) if fpath.exists() and not refresh else {}
    changed = False
    for q in ids:
        if str(q) in cached:
            continue
        d = get_json(f"{API}/{q}")["value"]
        cached[str(q)] = {"fetched_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                          "questionText": d["questionText"], "answeringBodyId": d["answeringBodyId"],
                          "answeringBodyName": d["answeringBodyName"], "dateTabled": d["dateTabled"],
                          "isWithdrawn": d["isWithdrawn"]}
        changed = True
    if changed:
        fpath.write_text(json.dumps(cached, indent=1, ensure_ascii=False, sort_keys=True))
    return cached


# ---------------------------------------------------------------- text
def strip_html(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = html.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return re.sub(r"\s+([.,;:])", r"\1", s)


BOILER = re.compile(r"^\S+ works with the |\bis an? (non-)?ministerial department\b|\bsupported by \d+ (agencies|public bodies)"
                    r"|\bis a (ministerial|non-ministerial) (department|government department)\b", re.I)


def what_we_do(org):
    """GOV.UK 'what we do' text: the organisation page body paragraphs, minus the
    'X is a ministerial department, supported by N agencies' boilerplate line."""
    if not org or not org.get("body"):
        return None
    paras = re.findall(r"<p>(.*?)</p>", org["body"], flags=re.S)
    keep = [strip_html(p) for p in paras if not BOILER.search(strip_html(p))]
    keep = [p for p in keep if p]
    return " ".join(keep) if keep else None


# Leading "To ask the <office>," clause, from the fixed list of offices seen in the snapshot.
# Lords: "To ask His Majesty's Government ..." is kept verbatim (no department cue).
OFFICES = [
    r"Secretary of State for (?:Health and Social Care|Defence|Housing, Communities and Local Government|Transport|"
    r"the Home Department|Environment, Food and Rural Affairs|Education|Foreign, Commonwealth and Development Affairs|"
    r"Justice|Work and Pensions|Energy Security and Net Zero|Business and Trade|Business, Innovation, Science and Trade|"
    r"Science, Innovation and Technology|Digital, Culture, Media and Sport|Culture, Media and Sport|Northern Ireland|"
    r"Wales|Scotland|Women and Equalities)",
    r"Chancellor (?:of|for) the Exchequer",
    r"Minister (?:for|of) (?:the )?Cabinet Office",
    r"Chancellor of the Duchy of Lancaster",
    r"Minister for Women and Equalities",
    r"Attorney General",
    r"Solicitor General",
]
LEAD = re.compile(r"^\W*To ask (?:the )?(?:" + "|".join(OFFICES) + r")\s*,\s*", re.I)
HMG = re.compile(r"^\W*To ask His Majesty'?s Government\b", re.I)

# Department names / minister titles / short names for each label body (by answeringBodyId).
TITLES = {
    17: ["Department of Health and Social Care", "Secretary of State for Health and Social Care", "Health Secretary",
         "Health and Social Care Secretary", "DHSC"],
    11: ["Ministry of Defence", "Secretary of State for Defence", "Defence Secretary", "MoD", "MOD"],
    7: ["Ministry of Housing, Communities and Local Government", "Secretary of State for Housing, Communities and Local Government",
        "Housing Secretary", "MHCLG"],
    27: ["Department for Transport", "Secretary of State for Transport", "Transport Secretary", "DfT"],
    1: ["Home Office", "Secretary of State for the Home Department", "Home Department", "Home Secretary"],
    13: ["Department for Environment, Food and Rural Affairs", "Secretary of State for Environment, Food and Rural Affairs",
         "Environment Secretary", "Defra", "DEFRA"],
    14: ["Treasury", "HM Treasury", "His Majesty's Treasury", "Chancellor of the Exchequer", "Chancellor for the Exchequer",
         "Chief Secretary to the Treasury", "Exchequer Secretary to the Treasury", "Economic Secretary to the Treasury",
         "Financial Secretary to the Treasury", "HMT"],
    53: ["Cabinet Office", "Minister for the Cabinet Office", "Minister of the Cabinet Office", "Minister for Cabinet Office",
         "Chancellor of the Duchy of Lancaster"],
    60: ["Department for Education", "Secretary of State for Education", "Education Secretary", "DfE"],
    208: ["Foreign, Commonwealth and Development Office", "Secretary of State for Foreign, Commonwealth and Development Affairs",
          "Foreign Secretary", "Foreign Office", "FCDO"],
    54: ["Ministry of Justice", "Secretary of State for Justice", "Justice Secretary", "Lord Chancellor", "MoJ", "MOJ"],
    29: ["Department for Work and Pensions", "Secretary of State for Work and Pensions", "Work and Pensions Secretary", "DWP"],
    215: ["Department for Energy Security and Net Zero", "Secretary of State for Energy Security and Net Zero",
          "Energy Secretary", "DESNZ"],
    220: ["Department for Business, Innovation, Science and Trade", "Secretary of State for Business, Innovation, Science and Trade",
          "Business Secretary", "DBIST", "BIST"],
    10: ["Department for Digital, Culture, Media and Sport", "Secretary of State for Digital, Culture, Media and Sport",
         "Culture Secretary", "DCMS"],
    31: ["Women and Equalities", "Minister for Women and Equalities", "Secretary of State for Women and Equalities",
         "Office for Equality and Opportunity", "Government Equalities Office", "Minister for Women", "Minister for Equalities",
         "OEO", "GEO"],
    21: ["Northern Ireland Office", "Secretary of State for Northern Ireland", "Northern Ireland Secretary", "NIO"],
    88: ["Attorney General's Office", "Attorney General", "Solicitor General", "Law Officers", "AGO"],
    28: ["Wales Office", "Secretary of State for Wales", "Office of the Secretary of State for Wales", "Welsh Secretary",
         "Wales Secretary"],
    2: ["Scotland Office", "Secretary of State for Scotland", "Office of the Secretary of State for Scotland",
        "Scottish Secretary", "Scotland Secretary"],
}
# Superseded predecessors (not labels): their names point to a successor option (e.g. "previously DSIT and DBT
# staff" -> DBIST), so they are redacted too.
TITLES.update({
    214: ["Department for Business and Trade", "Secretary of State for Business and Trade", "DBT"],
    216: ["Department for Science, Innovation and Technology", "Secretary of State for Science, Innovation and Technology",
          "Science Secretary", "Technology Secretary", "DSIT"],
    217: ["Department for Culture, Media and Sport", "Secretary of State for Culture, Media and Sport"],
})
CASE_SENSITIVE = {"DBT", "DSIT", "MoD", "MOD", "MoJ", "MOJ", "DfE", "DfT", "Defra", "DEFRA", "HMT", "OEO", "GEO", "NIO", "AGO", "BIST",
                  "DBIST", "DCMS", "DHSC", "MHCLG", "FCDO", "DWP", "DESNZ"}


def title_variants(bid, name):
    v = set(TITLES.get(bid, [])) | {name}
    v |= {x.replace(" and ", " & ") for x in v} | {x.replace("'", "’") for x in v}
    return sorted(v, key=len, reverse=True)


def redact(text, bodies):
    """Replace department names / minister titles / standard short names of EVERY label body (bodies: list of
    (answeringBodyId, name)) with [DEPARTMENT]. Symmetric, so a verbatim name never marks a non-gold option."""
    reds = []
    variants = sorted({v for bid, name in bodies for v in title_variants(bid, name)}, key=lambda v: (-len(v), v))
    for v in variants:
        flags = 0 if v in CASE_SENSITIVE else re.I
        pat = re.compile(r"(?<![\w\[])" + re.escape(v).replace(r"\ ", r"\s+") + r"(?![\w\]])", flags)

        def sub(m):
            reds.append(m.group(0))
            return "[DEPARTMENT]"
        text = pat.sub(sub, text)
    return text, reds


def clean_state(qtext, bodies):
    """Returns (state, stripped_lead, redactions) or None if the leading clause is of an unknown form."""
    t = strip_html(qtext)
    lead = None
    if HMG.match(t):
        t = t.lstrip("﻿?​ ").strip()
    else:
        m = LEAD.match(t)
        if not m:
            return None
        lead = m.group(0).strip()
        t = t[m.end():]
        t = t[:1].upper() + t[1:] if t else t
    t, reds = redact(t, bodies)
    return t.strip(), lead, reds


def norm(s):
    s = re.sub(r"\[DEPARTMENT\]", " ", s.lower())
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def near_dup(a, b):
    """Near-identical multi-part questions: token Jaccard >= 0.6 or one text contains the other."""
    ta, tb = set(a.split()), set(b.split())
    if not ta or not tb:
        return False
    if a in b or b in a:
        return True
    return len(ta & tb) / len(ta | tb) >= 0.6


def hid(*xs):
    return hashlib.sha1("|".join(map(str, xs)).encode()).hexdigest()[:12]


# ---------------------------------------------------------------- build
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args()

    smeta, recs = snapshot(args.refresh)
    print(f"snapshot: {len(recs)} records", file=sys.stderr)

    elig = [r for r in recs if not r.get("isWithdrawn") and r.get("questionText") and r.get("answeringBodyId")
            and DATE_FROM <= (r.get("dateTabled") or "")[:10] <= DATE_TO]

    # canonical name per answeringBodyId = name on its latest-tabled record (merges same-id renames)
    latest = {}
    for r in sorted(elig, key=lambda r: (r["dateTabled"], r["id"])):
        latest[r["answeringBodyId"]] = r["answeringBodyName"].strip()
    names_by_id = defaultdict(Counter)
    for r in elig:
        names_by_id[r["answeringBodyId"]][r["answeringBodyName"].strip()] += 1
    merged_renames = {latest[i]: dict(c) for i, c in names_by_id.items() if len(c) > 1}

    # check the superseded set against the data
    last_date = defaultdict(str)
    for r in elig:
        last_date[r["answeringBodyId"]] = max(last_date[r["answeringBodyId"]], r["dateTabled"][:10])
    for i in SUPERSEDED:
        assert last_date[i] <= SUPERSEDED_LAST_DATE, (i, last_date[i])
    dropped_superseded = Counter(latest[r["answeringBodyId"]] for r in elig if r["answeringBodyId"] in SUPERSEDED)
    elig = [r for r in elig if r["answeringBodyId"] not in SUPERSEDED]

    freq = Counter(r["answeringBodyId"] for r in elig)
    # top 20 bodies, ties broken by a seeded shuffle (random.Random(3))
    ids = sorted(freq)
    random.Random(3).shuffle(ids)
    tie_rank = {n: k for k, n in enumerate(ids)}
    top = sorted(freq, key=lambda n: (-freq[n], tie_rank[n]))[:N_LABELS]
    cutoff = freq[top[-1]]
    next_out = sorted((i for i in freq if i not in top), key=lambda n: (-freq[n], tie_rank[n]))[:3]
    name = {i: latest[i] for i in freq}

    orgs = org_snapshot(top, args.refresh)

    # cards
    defs, def_src = {}, {}
    AUTHOR = {}  # frozen author-written definitions, only for a body without GOV.UK text (none needed)
    for i in top:
        slug = SLUGS.get(i)
        d = what_we_do(orgs.get(slug)) if slug else None
        if d:
            defs[i] = d
            def_src[name[i]] = {
                "source": "official: GOV.UK organisation page 'what we do' (content API details.body)",
                "govuk_title": orgs[slug].get("title"), "slug": slug,
                "url": orgs[slug].get("web_url") or f"https://www.gov.uk/government/organisations/{slug}",
                "content_api": orgs[slug]["content_url"], "fetched_utc": orgs[slug]["fetched_utc"],
                "public_updated_at": orgs[slug].get("public_updated_at")}
        elif i in AUTHOR:
            defs[i] = AUTHOR[i]
            def_src[name[i]] = {"source": "author-written (frozen)"}
        else:
            raise SystemExit(f"no definition for body {i} {name[i]!r} (slug {slug})")

    # candidate items
    label_bodies = [(i, name[i]) for i in sorted(top)] + [(i, n) for i, n in sorted(SUPERSEDED.items())]
    by_body = defaultdict(list)
    lead_unmatched = Counter()
    for r in elig:
        i = r["answeringBodyId"]
        if i not in defs:
            continue
        out = clean_state(r["questionText"], label_bodies)
        if out is None:
            lead_unmatched[name[i]] += 1  # unknown leading form: skip rather than risk a cue
            continue
        state, lead, reds = out
        if not (20 <= len(state) <= 6000):
            continue
        by_body[i].append({"r": r, "state": state, "lead": lead, "reds": reds})

    # round-robin questions: the same member tabling a near-identical question to more than one body
    # (e.g. "how much has his Department spent on ..." to every department). The answering body cannot be
    # decided from such a text, so all copies are dropped. Checked over all eligible records, all bodies.
    by_member_all = defaultdict(list)
    for r in elig:
        t = strip_html(r["questionText"])
        m = LEAD.match(t)
        t = t[m.end():] if m else t
        by_member_all[r.get("askingMemberId")].append((r["answeringBodyId"], r["id"], set(norm(t).split()), norm(t)))
    round_robin = set()
    for mem, lst in by_member_all.items():
        for a in range(len(lst)):
            for b in range(a + 1, len(lst)):
                if lst[a][0] != lst[b][0]:
                    ta, tb = lst[a][2], lst[b][2]
                    if ta and tb and (lst[a][3] == lst[b][3] or len(ta & tb) / len(ta | tb) >= 0.6):
                        round_robin |= {lst[a][1], lst[b][1]}
    rr_dropped = Counter()
    for i in list(by_body):
        keep = [it for it in by_body[i] if it["r"]["id"] not in round_robin]
        rr_dropped[name[i]] = len(by_body[i]) - len(keep)
        by_body[i] = keep

    # dedupe: exact normalised text across the task; near-identical questions by the same member within a body
    seen_norm = set()
    for i in sorted(by_body):
        kept, by_member = [], defaultdict(list)
        for it in sorted(by_body[i], key=lambda x: x["r"]["id"]):
            n = norm(it["state"])
            if n in seen_norm:
                continue
            mem = it["r"].get("askingMemberId")
            if any(near_dup(n, o) for o in by_member[mem]):
                continue
            seen_norm.add(n)
            by_member[mem].append(n)
            kept.append(it)
        by_body[i] = kept

    # stratified: equal per label, remainder to labels in seeded order; one item per member per body if possible
    rng = random.Random(SEED)
    base, rem = divmod(N_ITEMS, len(top))
    order = sorted(top)
    rng.shuffle(order)
    quota = {i: base + (1 if k < rem else 0) for k, i in enumerate(order)}
    picked = []
    for i in sorted(top):
        pool = list(by_body[i])
        rng.shuffle(pool)
        chosen, members = [], set()
        for it in pool:
            if len(chosen) == quota[i]:
                break
            m = it["r"].get("askingMemberId")
            if m in members:
                continue
            members.add(m)
            chosen.append(it)
        for it in pool:
            if len(chosen) == quota[i]:
                break
            if not any(it is c for c in chosen):
                chosen.append(it)
        if len(chosen) < quota[i]:
            raise SystemExit(f"body {name[i]} has only {len(chosen)} eligible items")
        picked += [(i, it) for it in chosen]

    # full question text for the picked items (list endpoint truncates at 255 chars)
    full = full_text_snapshot(sorted(it["r"]["id"] for _, it in picked), args.refresh)
    n_truncated = 0
    for i, it in picked:
        r, f = it["r"], full[str(it["r"]["id"])]
        assert f["answeringBodyId"] == i and not f["isWithdrawn"], r["id"]
        # the list endpoint also folds a few characters (nbsp, narrow nbsp, non-breaking hyphen), so compare the
        # alphanumeric skeletons
        ca, cb = skeleton(r["questionText"]), skeleton(f["questionText"])
        if len(r["questionText"]) >= LIST_TRUNC:
            n_truncated += 1
            assert cb.startswith(ca), r["id"]
        else:
            assert ca == cb, r["id"]
        out = clean_state(f["questionText"], label_bodies)
        assert out is not None and 20 <= len(out[0]) <= 6000, r["id"]
        it["state"], it["lead"], it["reds"] = out

    labels = [name[i] for i in top]
    card_line = {name[i]: f"- {name[i]}: {defs[i]}" for i in top}
    rows = []
    for i, it in picked:
        r = it["r"]
        opts = sorted(labels)
        random.Random(f"{SEED}:{r['id']}").shuffle(opts)
        rows.append({
            "id": "r_" + hid(TASK, r["id"], "row"),
            "group_id": f"g:{TASK}:{r['id']}",
            "call_id": "c_" + hid(TASK, r["id"], "call"),
            "split": "ohs3",
            "track": "F",
            "source": TASK,
            "state": it["state"],
            "qtype": "choice",
            "instructions": INSTRUCTIONS,
            "options": opts,
            "gold": name[i],
            "role": "choice",
            "card": "\n".join(card_line[o] for o in opts),
            "meta": {
                "task": TASK,
                "dataset": "UK Parliament Written Questions API",
                "question_id": r["id"],
                "uin": r.get("uin"),
                "dateTabled": r.get("dateTabled"),
                "answeringBodyName": r["answeringBodyName"],
                "answeringBodyId": i,
                "original_label": r["answeringBodyName"],
                "house": r.get("house"),
                "url": f"https://questions-statements.parliament.uk/written-questions/detail/{r['dateTabled'][:10]}/{r.get('uin')}",
                "api_record": f"https://questions-statements-api.parliament.uk/api/writtenquestions/questions/{r['id']}",
                "snapshot_utc": smeta["snapshot_finished_utc"],
                "licence": LICENCE_Q,
                "card_source": def_src[name[i]]["url"],
                "card_licence": LICENCE_CARD,
                "stripped_lead": it["lead"],
                "redactions": it["reds"],
            },
        })
    random.Random(SEED + 1).shuffle(rows)

    # checks
    keys = {"id", "group_id", "call_id", "split", "track", "source", "state", "qtype", "instructions", "options",
            "gold", "role", "card", "meta"}
    assert len({r["group_id"] for r in rows}) == len(rows) == N_ITEMS
    assert len({norm(r["state"]) for r in rows}) == len(rows)
    bal = Counter(r["gold"] for r in rows)
    assert max(bal.values()) / len(rows) <= 0.40
    for r in rows:
        assert set(r) == keys and r["gold"] in r["options"] and 20 <= len(r["state"]) <= 6000
        assert not re.match(r"^\W*To ask the", r["state"], re.I)
        for n in [name[i] for i in top] + list(SUPERSEDED.values()):  # no label/predecessor name left in any state
            assert not re.search(re.escape(n), r["state"], re.I), (r["meta"]["question_id"], r["state"])

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")

    dates = sorted(r["meta"]["dateTabled"][:10] for r in rows)
    summary = {
        "task": TASK,
        "rows": len(rows),
        "qtype": "choice",
        "role": "choice",
        "n_options": len(labels),
        "options": sorted(labels),
        "track": "F",
        "split": "ohs3",
        "seed": SEED,
        "instructions": INSTRUCTIONS,
        "class_balance": dict(sorted(bal.items())),
        "max_class_share": round(max(bal.values()) / len(rows), 4),
        "house_counts": dict(Counter(r["meta"]["house"] for r in rows)),
        "date_range_items": [dates[0], dates[-1]],
        "source_window_requested": [DATE_FROM, DATE_TO],
        "source": "UK Parliament Written Questions API",
        "access": f"{API}?tabledWhenFrom={DATE_FROM}&tabledWhenTo={DATE_TO}&take={PAGE}&skip=N",
        "snapshot": smeta,
        "full_text_fetched_for_picked": len(picked),
        "picked_truncated_in_list_api": n_truncated,
        "snapshot_files": [str((CACHE / "questions.jsonl.gz").relative_to(LEAN)),
                           str((CACHE / "full_questions.json").relative_to(LEAN)),
                           str((CACHE / "govuk_organisations.json").relative_to(LEAN))],
        "licence": LICENCE_Q,
        "card_licence": LICENCE_CARD,
        "eligible_records_before_superseded_drop": len(elig) + sum(dropped_superseded.values()),
        "dropped_superseded_bodies": dict(dropped_superseded),
        "merged_same_id_renames": merged_renames,
        "label_frequency_top20": {name[i]: freq[i] for i in top},
        "cutoff_frequency": cutoff,
        "next_bodies_below_cutoff": {name[i]: freq[i] for i in next_out},
        "pool_after_filters_dedupe": {name[i]: len(by_body[i]) for i in top},
        "lead_clause_unmatched_skipped": dict(lead_unmatched),
        "round_robin_dropped": dict(rr_dropped),
        "label_definitions": def_src,
        "author_written_definitions": {},
        "redacted_rows": sum(1 for r in rows if r["meta"]["redactions"]),
        "redaction_counts": dict(Counter(x for r in rows for x in r["meta"]["redactions"])),
        "builder_notes": [
            "State = full questionText (from /questions/{id}; the list endpoint truncates at 255 chars), HTML stripped, leading 'To ask the <office>,' clause removed (fixed office list; "
            "records with an unknown leading form are skipped). 'To ask His Majesty's Government ...' (Lords) kept verbatim.",
            "Department names, minister titles and standard short names/acronyms of ALL 20 label bodies (not only the "
            "gold), and of the superseded DBT/DSIT/DCMS(217), replaced by '[DEPARTMENT]' (logged in meta.redactions), so a "
            "name never marks a non-gold option or points to a successor.",
            "Labels = answeringBodyId. Same-id renames merged under the latest name. Bodies superseded by the July 2026 "
            "machinery-of-government change (DBT 214, DSIT 216, DCMS 217; no question after 2026-07-14) dropped with "
            "their questions, because their successors (DBIST 220, DDCMS 10) are in the option set.",
            "Top 20 answering bodies by frequency in the frozen snapshot (tie-break random.Random(3)); stratified 7-8 "
            "per body, remainder by seeded order; one item per asking member per body where possible.",
            "Round-robin filter: a question is dropped if the same member tabled a near-identical question (token "
            "Jaccard >= 0.6 or same normalised text) to a different answering body, since the body cannot be told "
            "from the text.",
            "Dedupe: exact normalised text across the task; near-identical (token Jaccard >= 0.6 or containment) "
            "questions by the same member within a body.",
            "Card definitions: GOV.UK organisation page body paragraphs minus the 'is a ministerial department, "
            "supported by N agencies' boilerplate. 'Women and Equalities' uses the GOV.UK Office for Equality and "
            "Opportunity page (the office that supports the Minister for Women and Equalities).",
        ],
    }
    SUMMARY.write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    print(json.dumps(summary, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
