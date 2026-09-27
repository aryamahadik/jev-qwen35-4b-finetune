"""Build raw rows for breadth set "congress_policy" (US Congressional bills, CRS policy area, 115th-117th Congress).

Source   : HF dataset hheiden/us-congress-bill-policy-115_117, revision a46b7d3418d0d4614d449593e732ac34e5848812
           (curated by Hunter Heidenreich from congress.gov). Snapshot saved under breadth_src/cache/congress_policy/
           (README.md + congress_{115,116,117}_bills.parquet, sha256 pinned below).
Licence  : MIT (HF dataset card YAML "license: mit" and "License: MIT" in README.md). The underlying congress.gov
           bill titles, CRS summaries and policy-area terms are US-government works (public domain, 17 U.S.C. 105).
Provenance: summaries are written by Congressional Research Service legislative analysts; each public bill gets
           exactly one Policy Area term assigned by CRS analysts (human). Earliest summary per bill (mostly the
           "introduced" version); bills are 2017-2023. No model involvement.
Split    : the card defines no split (all parquet files load as HF "train"). The curator's leaderboard trains on one
           Congress and tests on the others (3x3 grid), so there is no fixed held-out test partition to avoid;
           we use all three Congresses. The full bill `text` column is never read.

Task     : one choice over the 31 CRS policy areas ("Which policy area best describes this bill?").
State    : the CRS summary, verbatim except that lines left incomplete by the source scrape (bullet lists were lost,
           leaving lead-ins such as "Specifically, the bill:" or lines stopping mid-sentence) are cut back to their
           last complete sentence or dropped (clean_summary; meta.incomplete_lines_cut counts them). If the cleaned
           summary is unusable (body under 10 words, a bare "Constitutional Amendment" header, or over 4,000 chars)
           the bill's official title is used instead if it has >= 6 words and >= 25 chars (meta.text_field says which).
Dropped  : policy areas "Private Legislation" (relief of named individuals; not a topic) and
           "Social Sciences and History" (15 bills in total); bills with no policy area.
Filters  : state 15-4,000 chars; dedup on normalised text (texts occurring with different policy areas are
           dropped, reintroduced identical summaries kept once); at most 2 rows per label sharing the same first
           6 words (limits boilerplate such as post-office namings); exact-state match and 13-word-run
           decontamination against our data/*.jsonl (never ohs*) and JevBench public files.
Sampling : round-robin over the 31 labels in a seeded order, at most 600 rows.
Definitions: written by Claude from the CRS policy-area scope (congress.gov policy-area glossary was not
           retrievable: Cloudflare 403), 8-35 words each; checked against how CRS actually assigns areas in this
           source (e.g. SNAP/school meals -> Agriculture and Food, fisheries -> Public Lands, Endangered Species Act ->
           Environmental Protection, veterans -> Armed Forces, House rule resolutions -> Congress, awareness/
           commemorative resolutions follow their subject rather than Government Operations).
Deterministic, seed 20261101.

  .venv/bin/python breadth_src/build_congress_policy.py
"""
import collections
import glob
import hashlib
import json
import random
import re
import statistics
from pathlib import Path

import pandas as pd

SEED = 20261101
KEY = "congress_policy"
MAX_ROWS = 600
MAX_PER_PREFIX = 2
HF_ID = "hheiden/us-congress-bill-policy-115_117"
REV = "a46b7d3418d0d4614d449593e732ac34e5848812"
REVISION = f"{HF_ID}@{REV}"
LICENCE = ("MIT (HF dataset card hheiden/us-congress-bill-policy-115_117: YAML 'license: mit', README 'License: MIT'); "
           "underlying congress.gov titles/CRS summaries/policy areas are US-government public-domain works")
SHA = {
    "README.md": "c3cc23c50b331a4bad1007e7f7a69a3e2b2ad6436064a4e919529a91ce886e70",
    "congress_115_bills.parquet": "afd692b05d69cc53f773fdde64c0bc16fd183aba34646c72c2c243fafb85af5e",
    "congress_116_bills.parquet": "49af6d3734610c5880e395f450b781f681710cd1a424c1db9a78e94388132163",
    "congress_117_bills.parquet": "4a49e9f329865aee021f429c9340f9fb4eb2b87f8d7529acee7c8644fc195ae0",
}
DROP = {"Private Legislation", "Social Sciences and History"}

HERE = Path(__file__).resolve().parent
LEAN = HERE.parent
CACHE = HERE / "cache" / KEY
OUT = LEAN / "data/v13_parts/raw" / f"{KEY}.jsonl"
DEFS = LEAN / "data/v13_parts/defs" / f"{KEY}.json"
JB = LEAN.parents[1] / "bench/jevbench/datasets/public"

QUESTION = "Which policy area best describes this US congressional bill as a whole?"

LABELS = {
    "Agriculture and Food": "Farming and food: crops, livestock, farm programs and subsidies, agricultural research and trade, food supply and safety, and food assistance and nutrition programs such as SNAP and school meals.",
    "Animals": "Animals themselves: animal welfare and cruelty, pets and domestic animals, veterinary care, and wildlife conservation for particular species; commercial fisheries and Endangered Species Act regulation belong elsewhere.",
    "Armed Forces and National Security": "The military and national defense: armed forces personnel and operations, defense spending and procurement, military bases, intelligence activities, war powers, and veterans' benefits, health care and services.",
    "Arts, Culture, Religion": "Arts, humanities and culture: museums, music, literature, cultural institutions and heritage, commemorative works about culture, and religion, religious organizations or observances.",
    "Civil Rights and Liberties, Minority Issues": "Protection of civil rights and liberties: discrimination based on race, sex, religion, disability or sexual orientation, minority groups' concerns, privacy, free speech, and equal rights.",
    "Commerce": "Domestic business and commerce: corporations, small businesses, consumer protection, product safety, advertising and marketing, bankruptcy, intellectual property, and economic development of industries.",
    "Congress": "The workings of Congress itself: members and their conduct, House and Senate rules and procedures, resolutions setting floor-debate rules for other bills, committees, congressional staff, oversight powers, and the Capitol.",
    "Crime and Law Enforcement": "Crime and its control: criminal offenses and penalties, police and law-enforcement agencies, firearms, drug crimes, prisons and corrections, criminal procedure, and victims of crime.",
    "Economics and Public Finance": "The federal budget and the economy: appropriations and the budget process, government spending, debt limit and deficits, and overall economic conditions and policy, excluding taxation.",
    "Education": "Education at all levels: schools, colleges and universities, teachers and students, curricula, student loans and financial aid, and federal education programs and funding.",
    "Emergency Management": "Preparing for, responding to and recovering from disasters and emergencies: hurricanes, floods, wildfires, earthquakes, FEMA, disaster relief and assistance, emergency communications, and preparedness for attacks or other threats.",
    "Energy": "Energy supply and use: oil, natural gas, coal, nuclear power, electricity and the power grid, renewable energy, energy efficiency and conservation, and fuel prices.",
    "Environmental Protection": "Environmental quality and pollution control: air and water pollution, climate change and greenhouse emissions, hazardous waste and toxic substances, environmental regulation, endangered species protection, and ecosystem protection.",
    "Families": "Family life and relationships: marriage, adoption, foster care and child welfare, child care, child support, family violence prevention, and services supporting families and their members.",
    "Finance and Financial Sector": "Banking and financial markets: banks and credit unions, securities and investment, insurance including flood insurance, credit and lending, consumer finance, currency and commemorative coins, and financial regulation.",
    "Foreign Trade and International Finance": "Trade and money flows with other countries: tariffs and duties, imports and exports, trade agreements and remedies, customs, foreign investment, and international monetary matters.",
    "Government Operations and Politics": "How the federal government runs: agencies and their organization, federal employees and contracting, federal property, the President, elections and campaign finance, government records, the Postal Service and post-office namings.",
    "Health": "Health care and public health: health insurance, Medicare and Medicaid, prescription drugs, diseases, medical research, hospitals and providers, mental health, and substance-use treatment.",
    "Housing and Community Development": "Housing and communities: housing affordability and availability, mortgages and home ownership, public and assisted housing, homelessness, and urban or rural community development programs.",
    "Immigration": "Entry and status of foreign nationals: visas, citizenship and naturalization, refugees and asylum, border and immigration enforcement, detention and deportation, and rights of immigrants.",
    "International Affairs": "US relations with other countries and international bodies: diplomacy, foreign aid, sanctions, arms sales, treaties, human rights abroad, and conflicts or events in foreign nations.",
    "Labor and Employment": "Work and workers: wages and hours, workplace safety, labor unions and collective bargaining, job training, unemployment, pensions and employee benefits, and workplace discrimination or leave.",
    "Law": "The courts and the legal system: federal courts and judges, civil actions and liability, judicial procedure and evidence, the legal profession, and constitutional or legal questions not tied to another area.",
    "Native Americans": "Matters concerning American Indians, Alaska Natives and Native Hawaiians: tribal governments and recognition, tribal lands and trust property, treaty rights, and federal programs for Native communities.",
    "Public Lands and Natural Resources": "Federal lands and natural resources: national parks, forests and wilderness, land conveyances and boundaries, monuments and historic sites, fisheries and marine resources, mining and minerals, and outdoor recreation areas.",
    "Science, Technology, Communications": "Science, technology and communications: scientific research and development, space, computing and cybersecurity, the internet, telecommunications, broadcasting and media, and science agencies.",
    "Social Welfare": "Public assistance and social services: Social Security and SSI, cash aid to low-income people, aid to older adults and persons with disabilities, anti-poverty programs, and volunteer and charitable service.",
    "Sports and Recreation": "Sports and leisure: professional, amateur and college athletics, the Olympics, athlete safety and integrity, recreational activities, and sporting events or achievements.",
    "Taxation": "Federal taxes: income, payroll, excise, estate and gift taxes, tax credits, deductions and exemptions, amendments to the Internal Revenue Code, and tax administration by the IRS.",
    "Transportation and Public Works": "Transportation systems and infrastructure: highways, roads and bridges, public transit, railroads, aviation and airports, maritime shipping, motor vehicle safety, and public works construction.",
    "Water Resources Development": "Water projects and management: dams and reservoirs, irrigation and water supply, flood control, navigation channels and harbors, river basins, and Army Corps or Bureau of Reclamation projects.",
}

words = lambda t: re.sub(r"[^a-z0-9]+", " ", t.lower()).split()
norm = lambda t: " ".join(words(t))


def check_cache():
    for name, sha in SHA.items():
        p = CACHE / name
        assert p.exists(), (f"missing {p}: hf_hub_download('{HF_ID}', '{name}', repo_type='dataset', "
                            f"revision='{REV}', local_dir='breadth_src/cache/{KEY}')")
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        assert h == sha, f"{name} sha256 mismatch {h}"


END = ('.', ')', '"', '?', '!', "'", '\u201d', '\u2019')
SENT_SPLIT = re.compile(r"(?<=[a-z0-9)]{2}[.!?])\s+(?=[A-Z(])")


def clean_summary(s):
    """The source summaries lost their bullet lists when scraped, leaving lead-in lines that stop mid-sentence
    ("Specifically, the bill:", "... the bill also requires the VA to"). Keep complete sentences only: a line not
    ending in terminal punctuation is cut back to its last complete sentence, or dropped if it has none. The first
    line is kept as a header when it is the short title (<= 25 words, not a "This ..." sentence).
    Returns (text, body_words, n_cut)."""
    lines = [l.strip() for l in s.split("\n") if l.strip()]
    out, body, cut = [], 0, 0
    for i, l in enumerate(lines):
        if not l.endswith(END):
            if i == 0 and len(lines) > 1 and len(l.split()) <= 25 and not l.startswith("This "):
                out.append(l)  # title header
                continue
            cut += 1
            sents = SENT_SPLIT.split(l)
            while sents and not sents[-1].endswith(END):
                sents.pop()
            if not sents:
                continue
            l = " ".join(sents)
        out.append(l)
        body += len(words(l))
    return "\n".join(out), body, cut


def usable_summary(s, body):
    return body >= 10 and len(s) <= 4000 and norm(s) != "constitutional amendment"


def load():
    """Return ({norm: rec}, stats). rec = {rid, text, label, field, congress}."""
    recs, bad, st = {}, set(), collections.Counter()
    for c in (115, 116, 117):
        df = pd.read_parquet(CACHE / f"congress_{c}_bills.parquet",
                             columns=["b_id", "congress", "title", "summary", "policy_area"])
        for r in df.sort_values("b_id").itertuples(index=False):
            st["source_rows"] += 1
            lab = r.policy_area if isinstance(r.policy_area, str) else None
            if lab in DROP or lab is None:
                st["drop_label_not_used"] += 1
                continue
            assert lab in LABELS, lab
            summ = (r.summary or "").strip() if isinstance(r.summary, str) else ""
            title = (r.title or "").strip() if isinstance(r.title, str) else ""
            summ, body, cut = clean_summary(summ)
            if usable_summary(summ, body):
                text, field = summ, "summary"
                st["summary_lines_cut"] += bool(cut)
            elif len(words(title)) >= 6 and len(title) >= 25:
                text, field, cut = title, "title", 0
            else:
                st["drop_no_usable_text"] += 1
                continue
            st[f"field_{field}"] += 1
            if not (15 <= len(text) <= 4000):
                st["drop_length"] += 1
                continue
            k = norm(text)
            if k in bad:
                st["drop_conflict"] += 1
                continue
            if k in recs:
                if recs[k]["label"] != lab:
                    bad.add(k)
                    del recs[k]
                    st["drop_conflict"] += 2
                else:
                    st["drop_duplicate"] += 1
                continue
            recs[k] = {"rid": r.b_id, "text": text, "label": lab, "field": field, "congress": int(r.congress),
                       "cut": cut}
    return recs, st


def contam(recs, n=13):
    """Norm keys equal to a state in, or sharing a 13-word run with, our data/*.jsonl (not ohs*) or JevBench."""
    grams = collections.defaultdict(set)
    for k in recs:
        w = k.split()
        for i in range(len(w) - n + 1):
            grams[" ".join(w[i:i + n])].add(k)
    files = sorted(f for f in glob.glob(str(LEAN / "data" / "*.jsonl")) if not Path(f).name.startswith("ohs"))
    files += sorted(glob.glob(str(JB / "*.jsonl")))
    hit = set()
    for f in files:
        with open(f, encoding="utf-8") as fh:
            for line in fh:
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                st = r.get("state") if isinstance(r, dict) else None
                if isinstance(st, str) and norm(st) in recs:
                    hit.add(norm(st))
                w = words(line.replace("\\n", " "))
                for i in range(len(w) - n + 1):
                    g = " ".join(w[i:i + n])
                    if g in grams:
                        hit |= grams[g]
    return hit, len(files)


def main():
    check_cache()
    rng = random.Random(SEED)
    recs, st = load()
    hit, nfiles = contam(recs)
    for k in hit:
        recs.pop(k, None)
    st["drop_decontam"] = len(hit)

    pools = collections.defaultdict(list)
    for k in sorted(recs):
        pools[recs[k]["label"]].append(recs[k])
    labels = list(LABELS)
    for lab in labels:
        rng.shuffle(pools[lab])
    order = labels[:]
    rng.shuffle(order)

    rows, idx, pref = [], collections.Counter(), collections.Counter()
    while len(rows) < MAX_ROWS:
        added = False
        for lab in order:
            if len(rows) >= MAX_ROWS:
                break
            while idx[lab] < len(pools[lab]):
                r = pools[lab][idx[lab]]
                idx[lab] += 1
                p = (lab, " ".join(words(r["text"])[:6]))
                if pref[p] >= MAX_PER_PREFIX:
                    st["skip_prefix_cap"] += 1
                    continue
                pref[p] += 1
                added = True
                rows.append({
                    "key": KEY, "rid": r["rid"], "state": r["text"], "instructions": QUESTION,
                    "options": labels, "gold": lab, "soft": None,
                    "meta": {"dataset": "US Congress bills 115-117, CRS policy area (Heidenreich; congress.gov)",
                             "config": f"congress_{r['congress']}", "revision": REVISION, "licence": LICENCE,
                             "split": "train", "orig_label": lab, "text_field": r["field"],
                             "incomplete_lines_cut": r["cut"]}})
                break
        if not added:
            break
    rng.shuffle(rows)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    DEFS.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    for name, d in LABELS.items():
        n = len(d.split())
        assert 8 <= n <= 35, (name, n)
    DEFS.write_text(json.dumps(LABELS, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # report
    print(f"stats: {dict(st)}; eligible after filters: {len(recs)}; decontam scanned {nfiles} files")
    print(f"wrote {len(rows)} rows -> {OUT}")
    lab_c = collections.Counter(r["gold"] for r in rows)
    for g in labels:
        print(f"  {g:45s} {lab_c[g]:3d}  pool {len(pools[g])}")
    print(f"max label share: {max(lab_c.values()) / len(rows):.1%}")
    print("per congress:", dict(sorted(collections.Counter(r["meta"]["config"] for r in rows).items())))
    print("text field:", dict(collections.Counter(r["meta"]["text_field"] for r in rows)))
    print(f"soft-label coverage: {sum(r['soft'] is not None for r in rows)}/{len(rows)}")
    L = [len(r["state"]) for r in rows]
    print(f"state length chars: min {min(L)} median {statistics.median(L)} mean {statistics.mean(L):.1f} max {max(L)}")
    print(f"defs: {len(LABELS)} -> {DEFS}")


if __name__ == "__main__":
    main()
