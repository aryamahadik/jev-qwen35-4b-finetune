"""Mapper: md_cordis_h2020 (CORDIS, EU research projects under Horizon 2020, 2014-2020; the 11th source of group C).

Licence (verified upstream, 15 Oct 2026): the data.europa.eu dataset record "cordish2020projects" attaches to the project
CSV (https://cordis.europa.eu/data/cordis-h2020projects-csv.zip) the licence "COM_REUSE, European Commission reuse
notice" = Commission Decision 2011/833/EU (http://data.europa.eu/eli/dec/2011/833/oj); the Commission legal notice
(https://commission.europa.eu/legal-notice_en) states that EU-owned content is licensed under CC BY 4.0.
Run (from lean/c2_build):  nice -n 10 .venv/bin/python -B meta_src/mappers/md_cordis_h2020.py
Input: meta_src/raw/cordis/x/project.csv (untrusted download, semicolon CSV, decimal comma). Output:
data/c2_md_parts/md_cordis_h2020/. No names of persons or organisations are used; titles only in the title tasks.
"""
import csv
import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mdkit_c as K  # noqa: E402

SRC = "md_cordis_h2020"
RAW = K.META_SRC / "raw" / "cordis" / "x" / "project.csv"
LIC = {"name": "Commission reuse notice (Decision 2011/833/EU); EU-owned content CC BY 4.0", "url": "http://data.europa.eu/eli/dec/2011/833/oj",
       "dataset_url": "https://cordis.europa.eu/data/cordis-h2020projects-csv.zip",
       "verified": "data.europa.eu record cordish2020projects lists COM_REUSE for this CSV; commission.europa.eu/legal-notice_en says CC BY 4.0",
       "legal_notice_url": "https://commission.europa.eu/legal-notice_en"}
N = 16
GROUPS = ["research and innovation (RIA, IA)", "coordination and support (CSA)", "Marie Sklodowska-Curie (MSCA)", "European Research Council (ERC)",
          "SME instrument (SME)", "other schemes"]


def sgroup(s):
    if s.startswith("MSCA"):
        return GROUPS[2]
    if s.startswith("ERC"):
        return GROUPS[3]
    if s.startswith("SME"):
        return GROUPS[4]
    if s in ("RIA", "IA", "CS2-RIA", "CS2-IA"):
        return GROUPS[0]
    if s == "CSA":
        return GROUPS[1]
    return GROUPS[5]


def num(x):
    return float(x.replace(",", "."))


def plus_years(d, y):
    try:
        return d.replace(year=d.year + y)
    except ValueError:
        return d.replace(year=d.year + y, month=3, day=1)


def load():
    csv.field_size_limit(10 ** 9)
    out = []
    for r in csv.DictReader(open(RAW, encoding="utf-8", newline=""), delimiter=";"):
        try:
            s, e = dt.date.fromisoformat(r["startDate"]), dt.date.fromisoformat(r["endDate"])
            tot, ec = num(r["totalCost"]), num(r["ecMaxContribution"])
        except (ValueError, KeyError, AttributeError):
            continue
        if not (r["fundingScheme"] and r["topics"] and e > s and tot > 0 and 0 < ec <= tot * 1.0001 and r["title"] and r["acronym"]):
            continue
        out.append({"id": r["id"], "scheme": r["fundingScheme"], "group": sgroup(r["fundingScheme"]), "topic": r["topics"], "s": s, "e": e,
                    "tot": tot, "ec": ec, "title": r["title"], "acr": r["acronym"]})
    return out


def money(x):
    return f"{x:.2f}".rstrip("0").rstrip(".") + " EUR"


def state(mode="all"):
    def f(t):
        L = [("Project ID", t["id"])]
        if mode == "title":
            L += [("Title", K.clip(t["title"], 140))]
        elif mode == "acr":
            L += [("Acronym", t["acr"])]
        else:
            L += [("Programme", "Horizon 2020"), ("Funding scheme", t["scheme"]), ("Call topic", t["topic"]),
                  ("Start date", t["s"].isoformat()), ("End date", t["e"].isoformat()), ("Total cost", money(t["tot"])),
                  ("EC maximum contribution", money(t["ec"]))]
        return K.kv(L)
    return f


def main():
    recs = load()
    key = lambda t: t["id"]
    print("records", len(recs))
    B = K.Builder(SRC, "research funding (EU)", LIC)
    st = state()
    byg = {g: [t for t in recs if t["group"] == g] for g in GROUPS}

    def yn(tid, pool, pairs, ga, card, n=N, field="", state_fn=st, **fmt):
        qa, qb = K.pair_fns(pairs, tid, key, **fmt)
        B.yn(tid, pool, key, state_fn, qa, qb, ga, lambda t: not ga(t), card, n, field)

    def eur(v):
        return f"{v:,} EUR"
    # 1. EC contribution thresholds
    for A in (50000, 100000, 250000, 500000, 1000000, 2000000, 5000000, 10000000):
        card = K.yn_card(f"the EC maximum contribution is greater than {eur(A)}.", f"the EC maximum contribution is {eur(A)} or less.") if A in (250000, 2000000) else None
        yn(f"ec.all.{A}", recs, [("Is the EC maximum contribution above {a}?", "Is the EC maximum contribution {a} or less?"),
                                 ("Does the EC contribute more than {a} to this project?", "Does the EC contribute {a} or less to this project?")],
           lambda t, A=A: t["ec"] > A, card, field="ecMaxContribution", a=eur(A))
    for g, thr in ((GROUPS[0], (1000000, 5000000)), (GROUPS[1], (500000, 2000000)), (GROUPS[2], (200000, 1000000)),
                   (GROUPS[3], (1500000, 2500000)), (GROUPS[4], (60000, 1000000))):
        for A in thr:
            yn(f"ec.{g.split()[0]}.{A}", byg[g], [("Is the EC maximum contribution above {a}?", "Is the EC maximum contribution {a} or less?")],
               lambda t, A=A: t["ec"] > A, None, field="ecMaxContribution", a=eur(A))
    # 2. duration in whole years
    for D in (1, 2, 3, 4, 5):
        yn(f"dur.{D}", recs, [("Does the project run longer than {D} years?", "Does the project run {D} years or less?"),
                              ("Is the end date later than {D} years after the start date?", "Is the end date within {D} years of the start date?")],
           lambda t, D=D: t["e"] > plus_years(t["s"], D),
           K.yn_card(f"the End date is later than the Start date plus {D} years (same month and day).", f"the End date is on or before the Start date plus {D} years."), field="startDate,endDate", D=D)
    # 3. start before year Y
    for Y in (2015, 2016, 2017, 2018, 2019, 2020):
        yn(f"startbefore.{Y}", recs, [("Did the project start before {Y}?", "Did the project start in {Y} or later?")],
           lambda t, Y=Y: t["s"] < dt.date(Y, 1, 1), None, field="startDate", Y=Y)
    for Y in (2018, 2020, 2022):
        yn(f"endafter.{Y}", recs, [("Does the project end after the year {Y}?", "Does the project end in {Y} or earlier?")],
           lambda t, Y=Y: t["e"].year > Y, None, field="endDate", Y=Y)
    yn("firsthalf", recs, [("Does the project start in the first half of a year, January to June?", "Does the project start in the second half of a year, July to December?")],
       lambda t: t["s"].month <= 6, None, field="startDate")
    yn("endsdec", recs, [("Does the project end in December?", "Does the project end in a month from January to November?")],
       lambda t: t["e"].month == 12, None, field="endDate")
    # 4. cost share
    yn("fullfund", recs, [("Does the EC contribution equal the total cost?", "Is the EC contribution smaller than the total cost?")],
       lambda t: abs(t["ec"] - t["tot"]) < 0.5, K.yn_card("the EC maximum contribution equals the total cost (within 0.5 EUR).", "the EC maximum contribution is smaller than the total cost."), field="ecMaxContribution,totalCost")
    yn("share70", recs, [("Does the EC cover at least 70 percent of the total cost?", "Does the EC cover less than 70 percent of the total cost?")],
       lambda t: t["ec"] >= 0.7 * t["tot"], K.yn_card("EC maximum contribution divided by total cost is 0.7 or more.", "that ratio is below 0.7."), field="ecMaxContribution,totalCost")
    # 5. topic prefixes
    for pre, nm in (("MSCA", "a Marie Sklodowska-Curie (MSCA)"), ("ERC", "a European Research Council (ERC)"), ("EIC", "a European Innovation Council (EIC)")):
        yn(f"topic.{pre}", recs, [("Is the call topic {nm} topic?", "Does the call topic come from a different programme part than {nm}?")],
           lambda t, pre=pre: t["topic"].split("-")[0] == pre, K.yn_card(f"the call topic code starts with {pre} followed by a hyphen or ends right after {pre}.", f"the call topic code starts with something else."), field="topics", nm=nm)
    # 6. titles / acronyms
    sT, sA = state("title"), state("acr")
    for k in (5, 10, 15):
        yn(f"titlelen.{k}", recs, [("Does the project title have more than {k} words?", "Does the project title have {k} words or fewer?")],
           lambda t, k=k: len(t["title"].split()) > k, None, state_fn=sT, field="title", k=k)
    yn("titlecolon", recs, [("Does the title contain a colon?", "Is the title a colon-free text?")],
       lambda t: ":" in t["title"], None, state_fn=sT, field="title")
    for k in (5, 8):
        yn(f"acrlen.{k}", recs, [("Does the acronym have more than {k} characters?", "Does the acronym have {k} characters or fewer?")],
           lambda t, k=k: len(t["acr"]) > k, None, state_fn=sA, field="acronym", k=k)
    # 7. choices
    B.choice("scheme.group", recs, key, st, "Which group does the funding scheme belong to?", GROUPS, lambda t: t["group"],
             K.choice_card({GROUPS[0]: "scheme RIA, IA, CS2-RIA or CS2-IA", GROUPS[1]: "scheme CSA", GROUPS[2]: "any scheme code that starts with MSCA",
                            GROUPS[3]: "any scheme code that starts with ERC", GROUPS[4]: "any scheme code that starts with SME", GROUPS[5]: "every other scheme code"}), 24, "fundingScheme")
    fam = lambda t: (t["topic"].split("-")[0] if t["topic"].split("-")[0] in ("MSCA", "ERC", "EIC", "SMEInst", "ICT") else "other")
    B.choice("topic.family", recs, key, st, "Which programme part does the call topic code start with?", ["MSCA", "ERC", "EIC", "SMEInst", "ICT", "other"], fam,
             K.choice_card({"MSCA": "code starts with MSCA", "ERC": "code starts with ERC", "EIC": "code starts with EIC", "SMEInst": "code starts with SMEInst",
                            "ICT": "code starts with ICT", "other": "any other first part"}), 24, "topics")
    band = lambda v: "under 100 thousand" if v < 1e5 else "100 thousand to under 1 million" if v < 1e6 else "1 million to under 5 million" if v < 5e6 else "5 million or more"
    bopts = ["under 100 thousand", "100 thousand to under 1 million", "1 million to under 5 million", "5 million or more"]
    B.choice("ec.band", recs, key, st, "Which band holds the EC maximum contribution (in EUR)?", bopts, lambda t: band(t["ec"]), None, 20, "ecMaxContribution")
    B.choice("cost.band", recs, key, st, "Which band holds the total cost (in EUR)?", bopts, lambda t: band(t["tot"]), None, 20, "totalCost")
    dur = lambda t: "up to 2 years" if t["e"] <= plus_years(t["s"], 2) else "over 2 up to 4 years" if t["e"] <= plus_years(t["s"], 4) else "over 4 years"
    B.choice("dur.band", recs, key, st, "Which band holds the project length?", ["up to 2 years", "over 2 up to 4 years", "over 4 years"], dur,
             K.choice_card({"up to 2 years": "the End date is on or before the Start date plus 2 years", "over 2 up to 4 years": "later than 2 years but on or before Start date plus 4 years",
                            "over 4 years": "later than the Start date plus 4 years"}), 20, "startDate,endDate")
    sy = lambda t: "2014 to 2016" if t["s"].year <= 2016 else "2017 to 2018" if t["s"].year <= 2018 else "2019 to 2020" if t["s"].year <= 2020 else "2021 or later"
    B.choice("start.band", recs, key, st, "Which period holds the start year?", ["2014 to 2016", "2017 to 2018", "2019 to 2020", "2021 or later"], sy, None, 20, "startDate")
    sh = lambda t: "all of it" if abs(t["ec"] - t["tot"]) < 0.5 else "70 percent to under 100 percent" if t["ec"] >= 0.7 * t["tot"] else "under 70 percent"
    B.choice("share.band", recs, key, st, "How much of the total cost does the EC contribution cover?", ["all of it", "70 percent to under 100 percent", "under 70 percent"], sh,
             K.choice_card({"all of it": "contribution equals total cost (within 0.5 EUR)", "70 percent to under 100 percent": "ratio from 0.7 up to below 1",
                            "under 70 percent": "ratio below 0.7"}), 20, "ecMaxContribution,totalCost")
    q = lambda t: "Q1 (January to March)" if t["s"].month <= 3 else "Q2 (April to June)" if t["s"].month <= 6 else "Q3 (July to September)" if t["s"].month <= 9 else "Q4 (October to December)"
    B.choice("start.quarter", recs, key, st, "Which quarter of the year does the project start in?", ["Q1 (January to March)", "Q2 (April to June)", "Q3 (July to September)", "Q4 (October to December)"], q, None, 20, "startDate")
    B.choice("end.quarter", recs, key, st, "Which quarter of the year does the project end in?", ["Q1 (January to March)", "Q2 (April to June)", "Q3 (July to September)", "Q4 (October to December)"],
             lambda t: q({"s": t["e"]}), None, 20, "endDate")
    man = B.write("CORDIS Horizon 2020 project CSV (data.europa.eu licence COM_REUSE; legal notice CC BY 4.0), fields are inputs and gold.",
                  {"licence_record": {"data_europa_record": "https://data.europa.eu/api/hub/search/datasets/cordish2020projects", "decision": "http://data.europa.eu/eli/dec/2011/833/oj",
                                      "legal_notice": "https://commission.europa.eu/legal-notice_en", "name_check": "PASS (source_name_check.py, OHS-4 and OHS-4+AC prelim, 15 Oct 2026)",
                                      "other_candidates": "md_nasa_exoplanets and md_cms_hospitals: upstream licence statement not found (acknowledgement page only / no licence field); NSF and ClinicalTrials: not verified"}})
    print(man["report"])


if __name__ == "__main__":
    main()
