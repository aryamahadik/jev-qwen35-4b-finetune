#!/usr/bin/env python
"""OHS-3 builder: medrxiv_category (choice, track F).

Source: medRxiv details API (api.medrxiv.org), preprints listed for 2026-06-01..2026-09-26.
The raw API pages are saved once under ohs3/cache/medrxiv_category/ (snapshot); every later run
reads only the cache, so re-runs give identical rows. Delete the cache to re-snapshot.

Filters (from the pre-registered spec):
  - version == "1", DOI dated 2026 (10.1101/2026.* or 10.64898/2026.*; medRxiv moved new
    DOIs to the 10.64898 prefix in 2026), posted date >= 2026-06-01;
  - licence in {cc_by, cc0, cc_by_nd} (text used verbatim, no redaction);
  - 20 most frequent categories among kept preprints (seeded tie-break);
  - stratified sample, 7-8 per category, 142 rows.
State: "Title: ...\n\nAbstract: ..." from the API's own title and abstract. Only whitespace is
collapsed and a leading "Abstract"/"Summary" label is removed; nothing else is edited.
"""
import hashlib
import json
import random
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import requests

SEED = 20261026
TASK = "medrxiv_category"
N_ITEMS = 142
N_CATS = 20
START, END = "2026-06-01", "2026-09-26"
API = "https://api.medrxiv.org/details/medrxiv/{s}/{e}/{c}/json"
KEEP_LICENCES = {"cc_by", "cc0", "cc_by_nd"}
LICENCE_NAMES = {"cc_by": "CC BY 4.0", "cc0": "CC0 1.0", "cc_by_nd": "CC BY-ND 4.0"}

LEAN = Path(__file__).resolve().parent.parent
CACHE = LEAN / "ohs3" / "cache" / TASK
OUT = LEAN / "data" / "ohs3_parts" / f"{TASK}.jsonl"
SUMMARY = LEAN / "data" / "ohs3_parts" / f"{TASK}_summary.json"

INSTRUCTIONS = "Which medRxiv subject category is this preprint posted under?"

# Author-written definitions (medRxiv publishes subject names only). Written once, frozen.
# Keys are the API's own category strings.
DEFINITIONS = {
    "addiction medicine": "Research on the prevention, diagnosis and treatment of substance use disorders and other addictions.",
    "allergy and immunology": "Research on allergic conditions and disorders of the immune system in patients.",
    "cardiovascular medicine": "Research on diseases of the heart and blood vessels.",
    "dentistry and oral medicine": "Research on the teeth, mouth and oral health.",
    "dermatology": "Research on diseases and conditions of the skin, hair and nails.",
    "emergency medicine": "Research on acute care delivered in emergency departments and pre-hospital settings.",
    "endocrinology": "Research on hormonal and metabolic disorders, including diabetes mellitus.",
    "epidemiology": "Research on the distribution and determinants of disease and health outcomes in populations.",
    "gastroenterology": "Research on diseases of the digestive tract, liver and pancreas.",
    "genetic and genomic medicine": "Research on the role of genes, genetic variation and genomic data in human disease and its care.",
    "geriatric medicine": "Research on the health and medical care of older adults.",
    "health economics": "Research on costs, resource use and economic evaluation in health and health care.",
    "health informatics": "Research on the use of data, digital tools and information systems in health and health care.",
    "health policy": "Research on laws, policies and regulations that shape health and health care.",
    "health systems and quality improvement": "Research on how health services are organised and delivered, and on improving their quality and safety.",
    "hematology": "Research on blood, blood-forming organs and blood disorders.",
    "hiv aids": "Research on HIV infection and AIDS.",
    "infectious diseases": "Research on diseases caused by pathogens such as bacteria, viruses, fungi and parasites, other than HIV/AIDS.",
    "intensive care and critical care medicine": "Research on the care of critically ill patients, usually in intensive care units.",
    "medical education": "Research on the training and education of medical and health professionals.",
    "medical ethics": "Research on ethical questions in medicine, research and health care.",
    "nephrology": "Research on kidney function and kidney diseases.",
    "neurology": "Research on disorders of the brain, spinal cord and nervous system.",
    "nursing": "Research on nursing practice, nursing care and the nursing workforce.",
    "nutrition": "Research on diet, food intake and nutritional status in relation to health.",
    "obstetrics and gynecology": "Research on pregnancy, childbirth and the female reproductive system.",
    "occupational and environmental health": "Research on health effects of workplace and environmental exposures.",
    "oncology": "Research on cancer.",
    "ophthalmology": "Research on the eye and vision disorders.",
    "orthopedics": "Research on the bones, joints, muscles and other parts of the musculoskeletal system.",
    "otolaryngology": "Research on disorders of the ear, nose and throat, and related structures of the head and neck.",
    "pain medicine": "Research on the assessment and management of pain.",
    "palliative medicine": "Research on care that relieves symptoms and suffering in serious or life-limiting illness.",
    "pathology": "Research on the diagnosis of disease through examination of tissues, cells and body fluids.",
    "pediatrics": "Research on the health and medical care of infants, children and adolescents.",
    "pharmacology and therapeutics": "Research on drugs, their effects and their use in treatment.",
    "primary care research": "Research on first-contact, continuing care delivered in general practice and community settings.",
    "psychiatry and clinical psychology": "Research on mental disorders and their psychological and psychiatric assessment and treatment.",
    "public and global health": "Research on protecting and improving the health of communities and populations, locally and worldwide.",
    "radiology and imaging": "Research on medical imaging methods and their use in diagnosis and treatment.",
    "rehabilitation medicine and physical therapy": "Research on restoring function and mobility after illness or injury.",
    "respiratory medicine": "Research on diseases of the lungs and airways.",
    "rheumatology": "Research on autoimmune, inflammatory and other diseases of the joints and connective tissue.",
    "sexual and reproductive health": "Research on sexual health, fertility, contraception and reproduction.",
    "sports medicine": "Research on physical activity, exercise and sport in relation to health and injury.",
    "surgery": "Research on operative treatment and surgical care.",
    "toxicology": "Research on the harmful effects of chemicals, drugs and other substances on people.",
    "transplantation": "Research on the transplantation of organs, tissues and cells.",
    "urology": "Research on the urinary tract and the male reproductive organs.",
    "anesthesia": "Research on anaesthesia, sedation and perioperative care.",
    "forensic medicine": "Research on medical knowledge applied to legal questions, such as causes of death or injury.",
}

SMALL = {"and", "of", "or", "in", "except", "including", "the"}


def display_name(cat):
    """Readable option label from the API's lowercase category string."""
    special = {"hiv aids": "HIV/AIDS", "infectious diseases": "Infectious Diseases (except HIV/AIDS)"}
    if cat in special:
        return special[cat]
    words = cat.split()
    return " ".join(w if (i and w in SMALL) else w[:1].upper() + w[1:] for i, w in enumerate(words))


def h12(*parts):
    return hashlib.sha1("|".join(map(str, parts)).encode()).hexdigest()[:12]


# ---------------------------------------------------------------- snapshot
def fetch_snapshot():
    manifest = CACHE / "manifest.json"
    if manifest.exists():
        return json.loads(manifest.read_text())
    CACHE.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    cursor, total, pages = 0, None, []
    sess = requests.Session()
    while total is None or cursor < total:
        url = API.format(s=START, e=END, c=cursor)
        for attempt in range(6):
            try:
                r = sess.get(url, timeout=90)
                r.raise_for_status()
                d = r.json()
                break
            except Exception as ex:  # noqa: BLE001
                print(f"retry {attempt} {url}: {ex}", file=sys.stderr)
                time.sleep(3 * (attempt + 1))
        else:
            raise SystemExit(f"failed {url}")
        msg = d["messages"][0]
        if total is None:
            total = int(msg["total"])
        n = len(d.get("collection", []))
        fn = f"page_{cursor:05d}.json"
        (CACHE / fn).write_text(json.dumps(d, ensure_ascii=False))
        pages.append({"cursor": cursor, "file": fn, "count": n, "url": url})
        if n == 0:
            break
        cursor += n
        time.sleep(0.3)
    m = {
        "api": API.format(s=START, e=END, c="<cursor>"),
        "snapshot_started_utc": started,
        "snapshot_finished_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "total_reported": total,
        "pages": pages,
    }
    manifest.write_text(json.dumps(m, indent=1))
    return m


def load_records(m):
    recs = []
    for p in m["pages"]:
        d = json.loads((CACHE / p["file"]).read_text())
        recs.extend(d.get("collection", []))
    return recs


# ---------------------------------------------------------------- text
ABS_LABEL = re.compile(r"^\s*(abstract\s*/\s*summary|abstract|summary)\s*[:.]?\s*", re.I)


def clean(s):
    return re.sub(r"\s+", " ", (s or "")).strip()


def make_state(title, abstract):
    t = clean(title)
    a = clean(abstract)
    # remove only a leading bare label ("Abstract", "Abstract/Summary", "Summary") when it is
    # followed by the start of a sentence (so "Summary statistics ..." is left untouched)
    m = ABS_LABEL.match(a)
    if m and a[m.end():m.end() + 1].isupper():
        a = a[m.end():]
    return f"Title: {t}\n\nAbstract: {a}", t, a


DOI_RE = re.compile(r"^10\.(1101|64898)/2026\.(\d\d)\.(\d\d)\.")


def main():
    m = fetch_snapshot()
    recs = load_records(m)
    n_raw = len(recs)

    drops = Counter()
    by_doi = {}
    for r in recs:
        doi = r.get("doi", "")
        if str(r.get("version")) != "1":
            drops["version!=1"] += 1
            continue
        if not DOI_RE.match(doi):
            drops["doi_not_2026"] += 1
            continue
        if r.get("date", "") < START or r.get("date", "") > END:
            drops["date_out_of_range"] += 1
            continue
        if r.get("license") not in KEEP_LICENCES:
            drops[f"licence:{r.get('license') or 'empty'}"] += 1
            continue
        cat = clean(r.get("category", "")).lower()
        if not cat:
            drops["no_category"] += 1
            continue
        state, t, a = make_state(r.get("title"), r.get("abstract"))
        if len(t) < 5 or len(a) < 200:
            drops["short_title_or_abstract"] += 1
            continue
        if len(state) > 6000:
            drops["state_over_6000"] += 1
            continue
        if doi in by_doi:
            drops["duplicate_doi"] += 1
            continue
        by_doi[doi] = dict(r, _cat=cat, _state=state)

    # dedup by normalised title (keep the earliest DOI)
    seen_titles, kept = {}, []
    for doi in sorted(by_doi):
        r = by_doi[doi]
        key = re.sub(r"\W+", " ", r["title"].lower()).strip()
        if key in seen_titles:
            drops["duplicate_title"] += 1
            continue
        seen_titles[key] = doi
        kept.append(r)

    cat_counts = Counter(r["_cat"] for r in kept)
    rng = random.Random(SEED)
    tieb = {c: rng.random() for c in sorted(cat_counts)}
    top = sorted(cat_counts, key=lambda c: (-cat_counts[c], tieb[c]))[:N_CATS]
    missing = [c for c in top if c not in DEFINITIONS]
    if missing:
        raise SystemExit(f"no frozen definition for: {missing}")

    # per-category quota: 142 = 20*7 + 2 -> two seeded categories get 8
    base, extra = divmod(N_ITEMS, N_CATS)
    rng = random.Random(SEED + 1)
    plus = set(rng.sample(sorted(top), extra))
    quota = {c: base + (1 if c in plus else 0) for c in top}

    pool = defaultdict(list)
    for r in kept:
        if r["_cat"] in quota:
            pool[r["_cat"]].append(r)
    chosen = []
    for c in sorted(top):
        items = sorted(pool[c], key=lambda r: r["doi"])
        random.Random(f"{SEED}|{c}").shuffle(items)
        if len(items) < quota[c]:
            raise SystemExit(f"category {c} has only {len(items)} items")
        chosen.extend(items[: quota[c]])

    options_all = [display_name(c) for c in top]
    card_lines = {display_name(c): f"- {display_name(c)}: {DEFINITIONS[c]}" for c in top}
    assert len(set(options_all)) == len(options_all)

    rows = []
    for r in sorted(chosen, key=lambda r: r["doi"]):
        doi = r["doi"]
        opts = list(options_all)
        random.Random(f"{SEED}|opts|{doi}").shuffle(opts)
        gold = display_name(r["_cat"])
        rows.append({
            "id": "r_" + h12("ohs3", TASK, doi, "row"),
            "group_id": f"g:{TASK}:{doi}",
            "call_id": "c_" + h12("ohs3", TASK, doi, "call"),
            "split": "ohs3",
            "track": "F",
            "source": TASK,
            "state": r["_state"],
            "qtype": "choice",
            "instructions": INSTRUCTIONS,
            "options": opts,
            "gold": gold,
            "role": "choice",
            "card": "\n".join(card_lines[o] for o in opts),
            "meta": {
                "task": TASK,
                "dataset": "medRxiv details API",
                "doi": doi,
                "version": r["version"],
                "date": r["date"],
                "license": r["license"],
                "licence_name": LICENCE_NAMES[r["license"]],
                "category": r["category"],
                "type": r.get("type"),
                "url": f"https://www.medrxiv.org/content/{doi}v1",
                "api_url": f"https://api.medrxiv.org/details/medrxiv/{doi}",
                "snapshot_utc": m["snapshot_finished_utc"],
            },
        })
    rng = random.Random(SEED + 2)
    rng.shuffle(rows)

    # checks
    assert len({r["group_id"] for r in rows}) == len(rows)
    assert len({r["id"] for r in rows}) == len(rows)
    bal = Counter(r["gold"] for r in rows)
    assert max(bal.values()) / len(rows) <= 0.40
    for r in rows:
        assert 20 <= len(r["state"]) <= 6000
        assert r["gold"] in r["options"]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")

    lens = [len(r["state"]) for r in rows]
    summary = {
        "task": TASK,
        "rows": len(rows),
        "qtype": "choice",
        "n_options": len(options_all),
        "track": "F",
        "seed": SEED,
        "source": "medRxiv details API",
        "api": m["api"],
        "snapshot_started_utc": m["snapshot_started_utc"],
        "snapshot_finished_utc": m["snapshot_finished_utc"],
        "snapshot_pages": len(m["pages"]),
        "api_total_reported": m["total_reported"],
        "raw_records": n_raw,
        "eligible_after_filters": len(kept),
        "drop_counts": dict(sorted(drops.items())),
        "eligible_licence_counts": dict(Counter(r["license"] for r in kept)),
        "row_licence_counts": dict(Counter(r["meta"]["license"] for r in rows)),
        "date_range_rows": [min(r["meta"]["date"] for r in rows), max(r["meta"]["date"] for r in rows)],
        "doi_prefix_counts_rows": dict(Counter(r["meta"]["doi"].split("/")[0] for r in rows)),
        "top20_categories_eligible_counts": {c: cat_counts[c] for c in top},
        "class_balance": dict(sorted(bal.items())),
        "max_class_share": round(max(bal.values()) / len(rows), 4),
        "state_chars": {"min": min(lens), "max": max(lens), "mean": round(sum(lens) / len(lens), 1)},
        "instructions": INSTRUCTIONS,
        "labels_source": "author-written: medRxiv publishes subject names only; one neutral definition per "
                         "category written once and frozen in this script (DEFINITIONS).",
        "author_written_definitions": {display_name(c): DEFINITIONS[c] for c in top},
        "option_label_note": "Option labels are the API category strings in title case; 'hiv aids' -> "
                             "'HIV/AIDS', 'infectious diseases' -> 'Infectious Diseases (except HIV/AIDS)' "
                             "(the medRxiv site's subject name). meta.category keeps the raw API string.",
        "text_edits": "State = title + abstract from the API, verbatim except whitespace collapse and removal of "
                      "a leading 'Abstract'/'Abstract/Summary'/'Summary' label. JATS section headings run into "
                      "the text in the API (e.g. 'BackgroundWe ...'); left as-is (no edits, ND-safe).",
        "uncertain": [
            "Spec said DOI 10.1101/2026.*; medRxiv now issues new DOIs under 10.64898/2026.*, so both prefixes "
            "are accepted (version 1, posted date >= 2026-06-01).",
            "Licence 'cc0_ng' (CC0, apparently a no-copyright/government variant) is not in the spec's keep "
            "list and was dropped, as were empty licence strings.",
            "Some API records have version '0' (listed but not version 1); dropped by the version==1 rule.",
            "Category is chosen by the submitting authors on medRxiv, so some items could plausibly fit "
            "another listed category (e.g. Epidemiology vs Public and Global Health).",
        ],
        "output": str(OUT),
    }
    SUMMARY.write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    print(json.dumps(summary, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
