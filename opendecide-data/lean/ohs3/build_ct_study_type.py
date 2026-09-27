"""OHS-3 part: ct_study_type (natural yes/no, track F).

Source: ClinicalTrials.gov API v2 (NLM). Studies first posted 2026-06-01..2026-09-26.
Question: is the study Interventional? Gold 1 = INTERVENTIONAL, 0 = OBSERVATIONAL (72/72).
EXPANDED_ACCESS and missing study types are dropped.

Determinism: the first run downloads every page of the query and saves the raw API pages (gzipped) plus fetch
metadata under ohs3/cache/ct_study_type/. Every later run reads only that snapshot, so rows are identical.
Sampling seed: 20261026.

No model predictions, results or LLM APIs are used.
"""
import gzip
import hashlib
import json
import random
import re
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import requests

LEAN = Path(__file__).resolve().parents[1]
CACHE = LEAN / "ohs3" / "cache" / "ct_study_type"
OUT = LEAN / "data" / "ohs3_parts" / "ct_study_type.jsonl"
SUMMARY = LEAN / "data" / "ohs3_parts" / "ct_study_type_summary.json"

TASK = "ct_study_type"
SEED = 20261026
N_PER_CLASS = 72
DATE_LO, DATE_HI = "2026-06-01", "2026-09-26"
API = "https://clinicaltrials.gov/api/v2/studies"
PARAMS = {
    "query.term": f"AREA[StudyFirstPostDate]RANGE[{DATE_LO},{DATE_HI}]",
    "fields": "NCTId,BriefTitle,BriefSummary,StudyType,StudyFirstPostDate",
    "pageSize": "1000",
    "countTotal": "true",
}
LICENCE = ("ClinicalTrials.gov data: NLM terms and conditions (https://clinicaltrials.gov/about-site/terms-conditions); "
           "freely usable with attribution to ClinicalTrials.gov / U.S. National Library of Medicine; the record may be "
           "changed by its sponsor, so the snapshot time is recorded.")
ATTRIBUTION = "Source: ClinicalTrials.gov, U.S. National Library of Medicine (API v2)."

# Official ClinicalTrials.gov protocol data element definition (https://clinicaltrials.gov/policy/protocol-definitions#StudyType),
# copied verbatim from the page as served on 2026-09-26.
DEF_URL = "https://clinicaltrials.gov/policy/protocol-definitions#StudyType"
ASKED_LABEL = "Interventional"
ASKED_DEF = ("Participants are assigned prospectively to an intervention or interventions according to a protocol to "
             "evaluate the effect of the intervention(s) on biomedical or other health related outcomes.")
OTHER_DEF_FOR_RECORD = ("Observational: Studies in human beings in which biomedical and/or health outcomes are assessed in "
                        "pre-defined groups of individuals. Participants in the study may receive diagnostic, therapeutic, "
                        "or other interventions, but the investigator does not assign specific interventions to the study "
                        "participants. This includes when participants receive interventions as part of routine medical "
                        "care, and a researcher studies the effect of the intervention.")
INSTRUCTIONS = "Is this study interventional?"
CARD = f"- {ASKED_LABEL}: {ASKED_DEF}"

# Label-cue redaction. Applied in order, case-insensitive (RCT case-sensitive). Each match -> "[STUDY]".
REDACTIONS = [
    ("rct_phrase", re.compile(r"\b(?:randomi[sz]ed,?\s+)?(?:(?:double|single|triple)[- ]blind(?:ed)?,?\s+)?"
                              r"(?:placebo[- ])?(?:controlled|clinical)\s+trials?\b", re.I)),
    ("rct_abbrev", re.compile(r"\bRCTs?\b")),
    ("interventional", re.compile(r"\b(?:non[- ]?)?interventional(?:\s+(?:clinical\s+)?stud(?:y|ies))?\b", re.I)),
    ("observational", re.compile(r"\b(?:non[- ]?)?observational(?:\s+stud(?:y|ies))?\b", re.I)),
    # label-word variants found in verification: "clinical observation study", "intervention study/trial", "non-intervention"
    ("observation_study", re.compile(r"\b(?:clinical\s+)?observation\s+stud(?:y|ies)\b", re.I)),
    ("intervention_study", re.compile(r"\b(?:non[- ]?)?intervention\s+(?:stud(?:y|ies)|trials?)\b", re.I)),
    ("non_intervention", re.compile(r"\bnon[- ]?intervention\b", re.I)),
]
MD_ESC = re.compile(r"\\([\\`*_{}\[\]()#+\-.!<>|~=^])")

sha = lambda s: hashlib.sha256(s.encode()).hexdigest()


def fetch_snapshot():
    CACHE.mkdir(parents=True, exist_ok=True)
    pages, token, i = [], None, 0
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    ver = requests.get("https://clinicaltrials.gov/api/v2/version", timeout=60).json()
    while True:
        p = dict(PARAMS)
        if token:
            p["pageToken"] = token
        for attempt in range(5):
            try:
                resp = requests.get(API, params=p, timeout=120)
                resp.raise_for_status()
                raw = resp.content
                break
            except Exception as e:  # noqa: BLE001
                print(f"retry {attempt}: {e}", file=sys.stderr)
                time.sleep(3 * (attempt + 1))
        else:
            raise SystemExit("download failed")
        (CACHE / f"page_{i:03d}.json.gz").write_bytes(gzip.compress(raw, mtime=0))
        d = json.loads(raw)
        pages.append(d)
        token = d.get("nextPageToken")
        i += 1
        if not token:
            break
    meta = {"api": API, "params": PARAMS, "pages": i, "totalCount": pages[0].get("totalCount"),
            "api_version": ver, "fetched_at_utc": started,
            "finished_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    (CACHE / "fetch_meta.json").write_text(json.dumps(meta, indent=1))


def load_snapshot():
    if not (CACHE / "fetch_meta.json").exists():
        fetch_snapshot()
    meta = json.loads((CACHE / "fetch_meta.json").read_text())
    studies, page_hashes = [], {}
    for i in range(meta["pages"]):
        f = CACHE / f"page_{i:03d}.json.gz"
        raw = gzip.decompress(f.read_bytes())
        page_hashes[f.name] = sha(raw.decode())
        studies += json.loads(raw)["studies"]
    return meta, studies, page_hashes


def clean(s):
    s = MD_ESC.sub(r"\1", s or "")
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    s = re.sub(r"[ \t]+\n", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def redact(s, log):
    for name, rx in REDACTIONS:
        for m in rx.finditer(s):
            log.append({"rule": name, "text": m.group(0)})
        s = rx.sub("[STUDY]", s)
    return s


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", s.lower())).strip()


def main():
    meta, studies, page_hashes = load_snapshot()
    drops = Counter()
    pool = {"INTERVENTIONAL": [], "OBSERVATIONAL": []}
    seen_state, seen_sum, seen_nct = set(), set(), set()
    for st in sorted(studies, key=lambda x: x["protocolSection"]["identificationModule"]["nctId"]):
        ps = st["protocolSection"]
        nct = ps["identificationModule"]["nctId"]
        stype = ps.get("designModule", {}).get("studyType")
        date = ps.get("statusModule", {}).get("studyFirstPostDateStruct", {}).get("date", "")
        title = clean(ps["identificationModule"].get("briefTitle"))
        summ = clean(ps.get("descriptionModule", {}).get("briefSummary"))
        if nct in seen_nct:
            drops["duplicate_nct"] += 1; continue
        seen_nct.add(nct)
        if stype not in pool:
            drops[f"study_type_{stype}"] += 1; continue
        if not (DATE_LO <= date <= DATE_HI):
            drops["first_post_date_out_of_range"] += 1; continue
        if not title or not summ:
            drops["missing_title_or_summary"] += 1; continue
        log = []
        state = f"Title: {redact(title, log)}\n\nSummary: {redact(summ, log)}"
        if not (20 <= len(state) <= 6000):
            drops["state_length"] += 1; continue
        ns, nsum = norm(state), norm(summ)
        if ns in seen_state or nsum in seen_sum:
            drops["duplicate_text"] += 1; continue
        seen_state.add(ns); seen_sum.add(nsum)
        pool[stype].append({"nct": nct, "date": date, "stype": stype, "state": state, "redactions": log})

    rng = random.Random(SEED)
    picked = {}
    for k in sorted(pool):
        items = list(pool[k])
        rng.shuffle(items)
        if len(items) < N_PER_CLASS:
            raise SystemExit(f"not enough {k}: {len(items)}")
        picked[k] = items[:N_PER_CLASS]
    chosen = picked["INTERVENTIONAL"] + picked["OBSERVATIONAL"]
    rng.shuffle(chosen)

    rows = []
    for it in chosen:
        gid = f"g:ohs3:{TASK}:{it['nct']}"
        rows.append({
            "id": "r_" + sha(f"ohs3:{TASK}:row:{it['nct']}")[:12],
            "group_id": gid,
            "call_id": "c_" + sha(f"ohs3:{TASK}:call:{it['nct']}")[:12],
            "split": "ohs3",
            "track": "F",
            "source": TASK,
            "state": it["state"],
            "qtype": "noul",
            "instructions": INSTRUCTIONS,
            "options": None,
            "gold": 1 if it["stype"] == "INTERVENTIONAL" else 0,
            "role": "aff",
            "card": CARD,
            "meta": {
                "task": TASK,
                "dataset": "ClinicalTrials.gov API v2",
                "NCTId": it["nct"],
                "StudyFirstPostDate": it["date"],
                "StudyType": it["stype"],
                "original_label": it["stype"],
                "asked_label": ASKED_LABEL,
                "url": f"https://clinicaltrials.gov/study/{it['nct']}",
                "api_url": f"https://clinicaltrials.gov/api/v2/studies/{it['nct']}",
                "snapshot_utc": meta["fetched_at_utc"],
                "api_data_timestamp": meta["api_version"].get("dataTimestamp"),
                "api_version": meta["api_version"].get("apiVersion"),
                "licence": LICENCE,
                "attribution": ATTRIBUTION,
                "redactions": it["redactions"],
            },
        })

    # checks
    assert len(rows) == 2 * N_PER_CLASS
    assert len({r["id"] for r in rows}) == len(rows) == len({r["group_id"] for r in rows}) == len({r["call_id"] for r in rows})
    assert len({r["state"] for r in rows}) == len(rows)
    g = Counter(r["gold"] for r in rows)
    assert g[1] == g[0] == N_PER_CLASS
    for r in rows:
        assert 20 <= len(r["state"]) <= 6000
        s = r["state"]
        assert not re.search(r"interventional|observational", s, re.I), r["id"]
        assert not re.search(r"clinical\s+trial|controlled\s+trial|\bRCTs?\b", s, re.I), r["id"]
        assert not re.search(r"observation\s+stud|intervention\s+(?:stud|trial)|non[- ]?intervention\b", s, re.I), r["id"]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows)
    OUT.write_text(text)

    red_rows = [r for r in rows if r["meta"]["redactions"]]
    rule_counts = Counter(x["rule"] for r in rows for x in r["meta"]["redactions"])
    red_by_class = Counter(r["gold"] for r in red_rows)
    lens = sorted(len(r["state"]) for r in rows)
    dates = sorted(r["meta"]["StudyFirstPostDate"] for r in rows)
    trial_left = Counter(r["gold"] for r in rows if re.search(r"\btrials?\b", r["state"], re.I))
    summary = {
        "task": TASK,
        "rows": len(rows),
        "qtype": "noul",
        "track": "F",
        "class_balance": {"gold_1_INTERVENTIONAL": g[1], "gold_0_OBSERVATIONAL": g[0]},
        "asked_label": ASKED_LABEL,
        "instructions": INSTRUCTIONS,
        "card": CARD,
        "label_definitions_source": f"official: ClinicalTrials.gov protocol data element definitions, Study Type ({DEF_URL})",
        "other_label_official_definition_for_record": OTHER_DEF_FOR_RECORD,
        "author_written_definitions": [],
        "source": "ClinicalTrials.gov API v2 (U.S. National Library of Medicine)",
        "query": {"api": API, "params": PARAMS},
        "snapshot": {"fetched_at_utc": meta["fetched_at_utc"], "finished_at_utc": meta["finished_at_utc"],
                     "api_version": meta["api_version"], "totalCount": meta["totalCount"], "pages": meta["pages"],
                     "cache_dir": str(CACHE.relative_to(LEAN)), "page_sha256": page_hashes},
        "licence": LICENCE,
        "attribution": ATTRIBUTION,
        "first_post_date_range_of_items": [dates[0], dates[-1]],
        "query_date_range": [DATE_LO, DATE_HI],
        "pool": {"studies_in_snapshot": len(studies),
                 "eligible_INTERVENTIONAL": len(pool["INTERVENTIONAL"]),
                 "eligible_OBSERVATIONAL": len(pool["OBSERVATIONAL"]),
                 "dropped": dict(drops)},
        "sampling": f"per class: sort eligible by NCTId, random.Random({SEED}).shuffle, take first {N_PER_CLASS}; rows then shuffled with the same RNG",
        "state_format": "Title: <BriefTitle>\\n\\nSummary: <BriefSummary> (markdown backslash escapes removed, whitespace normalised; no other edits)",
        "state_length": {"min": lens[0], "median": lens[len(lens) // 2], "max": lens[-1]},
        "redaction": {
            "replacement": "[STUDY]",
            "rules": {n: rx.pattern for n, rx in REDACTIONS},
            "rows_with_redaction": len(red_rows),
            "rows_with_redaction_by_gold": {"1": red_by_class[1], "0": red_by_class[0]},
            "matches_by_rule": dict(rule_counts),
            "per_row_log": "meta.redactions",
        },
        "ids": sorted(r["meta"]["NCTId"] for r in rows),
        "output_sha256": sha(text),
        "uncertain": [
            "Track F means first posted on ClinicalTrials.gov on/after 2026-06-01; the sponsor may have written the text earlier or posted it in another registry.",
            "Redaction covers the label words (interventional/observational, incl. non-), 'clinical trial(s)', '(randomized) controlled trial(s)' with blind/placebo modifiers, and 'RCT'. The bare word 'trial', 'randomized', 'placebo', 'cohort', 'registry' etc. are left as content, so many items remain decidable from design words; "
            f"rows still containing the word 'trial': gold1={trial_left[1]}, gold0={trial_left[0]}.",
            "The NLM brief-summary templates differ by type ('The goal of this clinical trial is to learn if ...' vs 'The goal of this observational study is to learn about ...'); after redaction both read 'The goal of this [STUDY] is ...' but the verb pattern ('learn if ... works' vs 'learn about') can remain.",
            "Records can be edited by sponsors after the snapshot; the cached raw pages are the frozen reference.",
        ],
    }
    SUMMARY.write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    print(json.dumps({k: v for k, v in summary.items() if k not in ("ids",)}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
