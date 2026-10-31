"""REJECTED in review (29 Sep 2026); main() refuses to run and no raw/defs files exist for this key.
Reason: with every vocabulary word withheld, the assessment text barely determines which rung the editors chose, so
the gold label is not clearly right from the state. A blind read of 16 random rows by the reviewer matched the gold
rung 6/16 times (adjacent confusions such as solid / convincing / compelling and valuable / important dominate), and
a bag-of-words probe (5-fold CV logistic regression over the 4,467 built rows) reached 40.1% exact vs a 35.7%
majority baseline on strength and 41.5% vs 35.9% on significance (recall on 'incomplete' 4%, 'fundamental' 8%).
Hard labels on a near-undecidable ordinal cloze would teach prior-guessing, not decisions. (Licence was fine: CC BY,
stated in eLife's reviewer guide 'Reviewers retain copyright of their review and consent to eLife publishing it using
a Creative Commons Attribution Licence' and the site footer.)

Original description follows.

Build raw rows for elife_assessment: which rung of eLife's controlled vocabulary (significance of findings, or
strength of evidence) did the editors choose, given their own written assessment with the rating words withheld?

Source : eLife public API, https://api.elifesciences.org/reviewed-preprints?per-page=100&page=N (all pages; 4,810
         reviewed preprints on 2026-09-29). The API is live, so the fetched listing is snapshotted once to
         cache/elife_assessment/reviewed_preprints_20260929.json (items sorted by id) and pinned by sha256.
Licence: CC BY 4.0. eLife: content "Subject to a Creative Commons Attribution license, except where otherwise noted"
         (https://elifesciences.org/about/elife-assessments, footer) and "reviewers ... consent to eLife publishing
         [their review] using a Creative Commons Attribution Licence" (https://elifesciences.org/about/peer-review).
Texts  : the eLife Assessment paragraph(s) written by the handling editors and reviewers (human-written); editors'
         notes ('[Editors' note: ...]') are dropped. Titles and preprint text are NOT used.
Labels : the API's structured `significance` and `strength` term lists, i.e. the editors' own rating on eLife's
         vocabularies (significance: useful < valuable < important < fundamental < landmark; strength: inadequate <
         incomplete < solid < convincing < compelling < exceptional). Only records with exactly one term on the
         asked dimension are used (ranges such as 'solid to convincing' are skipped). One editorial decision ->
         soft = null.
Redaction: every whole-word occurrence of all 11 vocabulary words (and their -ly adverbs), including generic uses
         such as 'an important question', is replaced by '[term withheld]', so a blank never reveals which word was
         the rating; a preceding 'a'/'an' becomes 'a(n)' so the article does not reveal the hidden word's first
         letter. Rows are dropped if nothing was redacted.
Exclusions: medRxiv-sourced preprints (8-digit DOI suffix; medRxiv is an OHS source) and anything published on or
         after 2026-08-01 (fresh period). Each record gives ONE row (significance or strength), never both.
Deterministic (seed 20261101); CPU only; no model calls.
"""
import collections
import html
import json
import random
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ord_common as C  # noqa: E402

KEY = "elife_assessment"
SEED = C.SEED
CACHE = C.CACHE / KEY
SNAP = CACHE / "reviewed_preprints_20260929.json"
SNAP_SHA = "3893bf71182cc1d7fc560920223bdcdd5c76c324a731fa938adae2ee3967834c"
API = "https://api.elifesciences.org/reviewed-preprints?per-page=100&page={page}&order=asc"
LICENCE = ("CC BY 4.0: eLife content 'Subject to a Creative Commons Attribution license, except where otherwise "
           "noted' (https://elifesciences.org/about/elife-assessments) and reviewers consent to publication 'using a "
           "Creative Commons Attribution Licence' (https://elifesciences.org/about/peer-review)")
DATASET = "eLife reviewed preprints: eLife Assessments via api.elifesciences.org/reviewed-preprints (snapshot 2026-09-29)"
CUTOFF = "2026-08-01"

SIG = ["useful", "valuable", "important", "fundamental", "landmark"]
STR = ["inadequate", "incomplete", "solid", "convincing", "compelling", "exceptional"]
Q = {
    "significance": ("This is an eLife Assessment with its rating words withheld. Which term on eLife's significance "
                     "scale did the editors use for the importance of the study's findings?"),
    "strength": ("This is an eLife Assessment with its rating words withheld. Which term on eLife's strength-of-"
                 "evidence scale did the editors use for how well the data support the claims?"),
}
DEFS = {
    "significance": {
        "useful": "Lowest significance rung: findings of focused importance and scope, useful mainly to specialists "
                  "working on the specific system or question.",
        "valuable": "Findings with theoretical or practical implications for a subfield, of interest to researchers "
                    "in that area but not much beyond it.",
        "important": "Findings with theoretical or practical implications beyond a single subfield, of interest to "
                     "a broad readership across related fields.",
        "fundamental": "Findings that substantially advance understanding of major research questions, changing how "
                       "a field thinks about a central problem.",
        "landmark": "Highest significance rung: findings with profound implications that are expected to have "
                    "widespread influence across fields.",
    },
    "strength": {
        "inadequate": "Lowest strength rung: the methods, data and analyses do not support the primary claims.",
        "incomplete": "The main claims are only partially supported; key controls, analyses or data are missing, so "
                      "the conclusions need more support.",
        "solid": "The methods, data and analyses broadly support the claims, with only minor weaknesses or "
                 "limitations remaining.",
        "convincing": "Appropriate and validated methodology in line with the current state of the art; the claims "
                      "are well supported with no substantive weaknesses.",
        "compelling": "Evidence featuring methods, data and analyses more rigorous than the current state of the "
                      "art, beyond simply convincing.",
        "exceptional": "Highest strength rung: exemplary use of existing approaches that establishes new standards "
                       "for the field.",
    },
}
VOCAB = SIG + STR
TERM_RE = re.compile(r"(?i)\b(?:" + "|".join(VOCAB) + r")(?:ly)?\b")


def fetch_snapshot():
    if not SNAP.exists():
        import requests
        SNAP.parent.mkdir(parents=True, exist_ok=True)
        items, page = [], 1
        while True:
            for attempt in range(5):
                try:
                    r = requests.get(API.format(page=page), timeout=120,
                                     headers={"User-Agent": "opendecide-golden-builder"})
                    r.raise_for_status()
                    d = r.json()
                    break
                except Exception:  # noqa: BLE001
                    time.sleep(3 * (attempt + 1))
            else:
                sys.exit(f"failed page {page}")
            items += d["items"]
            if page * 100 >= d["total"]:
                break
            page += 1
            time.sleep(0.3)
        items.sort(key=lambda x: int(x["id"]))
        SNAP.write_text(json.dumps(items, ensure_ascii=False, sort_keys=True))
    got = C.sha256(SNAP)
    if SNAP_SHA is None:
        print(f"PIN {SNAP.name}: {got}")
    elif got != SNAP_SHA:
        sys.exit(f"sha256 mismatch for {SNAP}: {got}")
    return json.loads(SNAP.read_text())


def strip_html(t):
    t = re.sub(r"<[^>]+>", "", t)
    return html.unescape(t)


def medrxiv(doi):
    suf = doi.split("/")[-1]
    parts = suf.split(".")
    return len(parts) >= 4 and len(parts[3].split("v")[0]) == 8


def main():
    raise SystemExit("elife_assessment was REJECTED in review (gold rung not decidable from the redacted text); "
                     "see the module docstring")
    items = fetch_snapshot()
    stats = collections.Counter()
    stats["items"] = len(items)
    recs = []
    for it in items:
        a = it.get("elifeAssessment") or {}
        pub = (it.get("published") or "")[:10]
        if not pub or pub >= CUTOFF:
            stats["drop_fresh"] += 1
            continue
        if medrxiv(it.get("doi", "")):
            stats["drop_medrxiv"] += 1
            continue
        paras = [strip_html(p.get("text", "")) for p in a.get("content", []) if p.get("type") == "paragraph"]
        paras = [C.clean(p) for p in paras if p.strip() and not p.strip().startswith("[Editors")
                 and not p.strip().startswith("[Editor")]
        text = "\n\n".join(paras)
        if len(C.words(text)) < 30:
            stats["drop_short"] += 1
            continue
        red, n = TERM_RE.subn("[term withheld]", text)
        # 'a' / 'an' before a blank would reveal whether the hidden word starts with a vowel
        red = re.sub(r"\b([Aa])n? \[term withheld\]", r"\1(n) [term withheld]", red)
        if n == 0:
            stats["drop_no_term_in_text"] += 1
            continue
        sig = [s.lower() for s in a.get("significance", [])]
        stg = [s.lower() for s in a.get("strength", [])]
        dims = {}
        if len(sig) == 1 and sig[0] in SIG:
            dims["significance"] = sig[0]
        if len(stg) == 1 and stg[0] in STR:
            dims["strength"] = stg[0]
        if not dims:
            stats["drop_no_single_term"] += 1
            continue
        subj = ", ".join(s["name"] for s in it.get("subjects", []))
        state = (f"eLife Assessment of a reviewed preprint (subject area: {subj or 'not stated'}); every eLife "
                 f"rating word is shown as [term withheld].\n\n{red}")
        recs.append({"rid": f"elife-rp-{it['id']}", "state": state, "text": text, "dims": dims, "sig": sig,
                     "stg": stg, "pub": pub, "n_red": n})
    stats["candidates"] = len(recs)
    rng = random.Random(SEED)
    rng.shuffle(recs)
    nd = C.NearDup(thr=0.7)
    uniq = []
    for x in recs:
        if nd.seen(x["text"]):
            stats["drop_near_dup"] += 1
            continue
        uniq.append(x)
    hits = C.decon({x["rid"]: [x["text"]] for x in uniq}, KEY)
    hits.update(C.cross_v14({x["rid"]: [x["text"]] for x in uniq}, {KEY}))
    stats["drop_decon"] = len(hits)
    uniq = [x for x in uniq if x["rid"] not in hits]

    # assign each record to ONE question: rare levels first so they are not lost, then alternate
    rare = {"significance": {"useful", "fundamental", "landmark"},
            "strength": {"inadequate", "compelling", "exceptional"}}
    assigned = {"significance": [], "strength": []}
    rest = []
    for x in uniq:
        rq = [q for q, v in x["dims"].items() if v in rare[q]]
        if len(x["dims"]) == 1:
            q = next(iter(x["dims"]))
            assigned[q].append(x)
        elif rq:
            assigned[rng.choice(sorted(rq))].append(x)
        else:
            rest.append(x)
    for x in rest:
        q = "significance" if len(assigned["significance"]) <= len(assigned["strength"]) else "strength"
        assigned[q].append(x)

    rows = []
    for q, xs in assigned.items():
        cnt = collections.Counter(x["dims"][q] for x in xs)
        # cap the top class at 45% of the question's rows
        top_lab, _ = cnt.most_common(1)[0]
        others = sum(v for k, v in cnt.items() if k != top_lab)
        cap = int(others * 45 / 55)
        kept_top = 0
        opts = SIG if q == "significance" else STR
        for x in xs:
            lab = x["dims"][q]
            if lab == top_lab:
                if kept_top >= cap:
                    stats[f"drop_cap_{q}"] += 1
                    continue
                kept_top += 1
            edge = []
            if len(x["sig"]) + len(x["stg"]) > 2:
                edge.append("ambiguous")  # the other dimension is a range
            if re.search(r"(?i)\b(?:however|although|while|but|despite|limitations?|weakness)", x["text"]):
                edge.append("conflicting_evidence")
            if C.neg_count(x["text"]) >= 2:
                edge.append("negation")
            rows.append({
                "key": KEY, "rid": x["rid"], "state": x["state"], "instructions": Q[q], "options": opts,
                "gold": lab, "soft": None,
                "meta": {"dataset": DATASET, "config": f"question={q}; all vocabulary words redacted",
                         "revision": f"api snapshot 2026-09-29; sha256:{SNAP_SHA}", "licence": LICENCE,
                         "split": "train", "orig_label": {"significance": x["sig"], "strength": x["stg"],
                                                          "published": x["pub"]},
                         "family": C.FAMILY, "edge": C.edge_join(edge), "defs": q, "seed": SEED},
            })
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, DEFS)
    print(dict(stats))
    st = C.summary(KEY, rows)
    C.show_samples(rows, n=5, seed=3)
    rec = C.manifest_record(
        KEY, DATASET, LICENCE, rows, "choice (ordinal: significance 5 levels / strength of evidence 6 levels)",
        "eLife editors' written assessments of reviewed preprints with all vocabulary words redacted; decide the "
        "significance rung (useful..landmark) or the strength-of-evidence rung (inadequate..exceptional) they chose; "
        "one row per record; medRxiv-sourced and post-2026-08-01 items excluded; top class capped at 45%.", st)
    return rows, rec


if __name__ == "__main__":
    rows, rec = main()
    if "--manifest" in sys.argv:
        C.append_manifest(rec)
        print("manifest record appended")
