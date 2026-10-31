"""openalex.py: metadata mapper for md_openalex (OpenAlex works; CC0; publisher OurResearch; scholarly publishing).

Upstream fields used as targets (A42-D 8.1): type, publication_year / date, language, open_access.oa_status, is_oa,
is_retracted, cited_by_count, referenced_works_count, authorships count, countries / institutions distinct counts,
primary_location source type, version, biblio pages, primary_topic field / domain. Titles, abstracts, author and
institution names are never used (snapshot keeps counts only). A task = one question template x one field mapping.
"""
from __future__ import annotations

import json
from pathlib import Path

from _common_a import (CHOICE_Q, COUNT_NEG, COUNT_POS, YEAR_NEG, YEAR_POS, Task, bool_task, bucket_task, ch_card,
                       concept_task, eq_task, ge_task, yn_card)

NAME = "openalex"
DOMAIN = "scholarly_publishing"
LICENCE = "CC0 1.0 (OpenAlex works metadata, upstream CC0; program-mapped, no OpenAlex text used as target)"
HEADERS = ["Bibliographic record", "Catalogue entry for a scholarly work", "Index record of a publication", "Scholarly work metadata"]
RAW = Path(__file__).resolve().parent.parent / "raw_a" / "openalex" / "works.json"
REF_YEAR = 2026
GROUPS = {"oa_status": "oa", "is_oa": "oa", "license": "oa", "version": "oa", "venue_oa": "oa", "field": "topic", "domain": "topic",
          "publication_year": "time", "publication_date": "time", "reference_year": "time"}


def load():
    return json.loads(RAW.read_text())


def rid_of(r):
    return r["id"]


def group_of(k):
    return GROUPS.get(k, k)


def pages(r):
    b = r.get("biblio") or {}
    try:
        a, z = int(b["first_page"]), int(b["last_page"])
    except (KeyError, ValueError, TypeError):
        return None
    return z - a + 1 if 0 <= z - a < 2000 else None


def fields_of(r):
    pg = pages(r)
    b = r.get("biblio") or {}
    f = {
        "work_id": ("Work ID", r["id"]), "work_type": ("Work type", r["type"]),
        "publication_year": ("Publication year", str(r["year"]) if r["year"] else None),
        "publication_date": ("Publication date", r["date"]),
        "reference_year": ("Reference year", str(REF_YEAR)),
        "language": ("Language code", r["language"]), "oa_status": ("Open-access status", r["oa_status"]),
        "is_oa": ("Open access flag", "true" if r["is_oa"] else "false"),
        "is_retracted": ("Retracted flag", "true" if r["is_retracted"] else "false"),
        "cited_by_count": ("Citation count", str(r["cited_by"])), "references_count": ("References listed", str(r["refs"])),
        "countries": ("Distinct countries", str(r["n_countries"])), "institutions": ("Distinct institutions", str(r["n_inst"])),
        "authors": ("Authors listed", str(r["n_authors"])), "venue_type": ("Venue type", r["source_type"]),
        "license": ("Licence", r["license"]), "version": ("Version", r["version"]),
        "has_fulltext": ("Full text indexed", "true" if r["has_fulltext"] else "false"),
        "field": ("Topic field", r["field"]), "domain": ("Topic domain", r["domain"]),
        "first_page": ("First page", b.get("first_page")), "last_page": ("Last page", b.get("last_page")),
        "volume": ("Volume", b.get("volume")),
    }
    if r.get("source_name"):
        f["venue"] = ("Venue name", r["source_name"])
    return f


def _field_domain():
    m = {}
    for r in load():
        if r["field"] and r["domain"]:
            m.setdefault(r["field"], set()).add(r["domain"])
    return {k: sorted(v)[0] for k, v in m.items() if len(v) == 1}


def tasks():
    T = []
    n = [0]

    def add(t):
        T.append(t)

    # --- card-free yes/no -------------------------------------------------------------------------------------
    for thr in (2, 10, 25, 50, 100):
        add(ge_task(f"oa_cited_ge_{thr}", ["cited_by_count"], lambda r: r["cited_by"], thr,
                    fmt={"things": "citations", "thing": "citation"}, why=f"cited_by_count >= {thr}"))
    for thr in (5, 20, 50):
        add(ge_task(f"oa_refs_ge_{thr}", ["references_count"], lambda r: r["refs"], thr,
                    fmt={"things": "references", "thing": "reference"}, why=f"referenced_works_count >= {thr}"))
    for thr in (2, 5, 10):
        add(ge_task(f"oa_authors_ge_{thr}", ["authors"], lambda r: r["n_authors"], thr, elig=lambda r: r["n_authors"] > 0,
                    fmt={"things": "authors", "thing": "author"}, why=f"len(authorships) >= {thr}"))
    add(ge_task("oa_inst_ge_2", ["institutions"], lambda r: r["n_inst"], 2, fmt={"things": "institutions", "thing": "institution"},
                why="institutions_distinct_count >= 2"))
    add(ge_task("oa_countries_ge_2", ["countries"], lambda r: r["n_countries"], 2, fmt={"things": "countries", "thing": "country"},
                why="countries_distinct_count >= 2"))
    for y in (2000, 2005, 2010, 2015, 2020):
        add(ge_task(f"oa_year_ge_{y}", ["publication_year"], lambda r: r["year"], y, pos=YEAR_POS, neg=YEAR_NEG,
                    fmt={"verb": "published", "what": "publication"}, why=f"publication_year >= {y}"))
    for v in ("article", "preprint", "book-chapter", "dataset", "review"):
        add(eq_task(f"oa_type_is_{v.replace('-', '_')}", ["work_type"], lambda r: r["type"], v, "work type", why=f"type == {v}"))
    for v in ("de", "es", "fr"):
        add(eq_task(f"oa_lang_is_{v}", ["language"], lambda r: r["language"], v, "language code", elig=lambda r: bool(r["language"]),
                    why=f"language == {v}"))
    for v in ("gold", "green", "hybrid", "bronze", "closed"):
        add(eq_task(f"oa_status_is_{v}", ["oa_status"], lambda r: r["oa_status"], v, "open-access status", why=f"oa_status == {v}"))
    add(bool_task("oa_retracted", ["is_retracted"], lambda r: bool(r["is_retracted"]), "retracted",
                  ["Is this work flagged as retracted?", "Does the retracted flag read true?", "Is the retracted flag set for this work?"],
                  ["Is it true that this work is not flagged as retracted?", "Is it true that the retracted flag is not set for this work?"],
                  why="is_retracted"))
    for thr in (5, 10, 20):
        add(Task(f"oa_pages_ge_{thr}", "yn", ["first_page", "last_page"], pred=lambda r, t=thr: pages(r) >= t,
                 elig=lambda r: pages(r) is not None, pos=["Does the page range cover {n} or more pages (last minus first, plus one)?",
                                                           "Is the page span, counting both end pages, at least {n}?"],
                 neg=["Does the page range cover fewer than {n} pages (last minus first, plus one)?",
                      "Is the page span, counting both end pages, below {n}?"], fmt={"n": thr},
                 why=f"last_page - first_page + 1 >= {thr}"))
    add(bool_task("oa_cited_gt_refs", ["cited_by_count", "references_count"], lambda r: r["cited_by"] > r["refs"], "",
                  ["Is the citation count higher than the number of references listed?", "Does the work have more citations than references?"],
                  ["Is the citation count below the number of references listed?", "Does the work have fewer citations than references?"],
                  elig=lambda r: r["cited_by"] != r["refs"], why="cited_by_count > referenced_works_count"))
    add(bool_task("oa_authors_gt_inst", ["authors", "institutions"], lambda r: r["n_authors"] > r["n_inst"], "",
                  ["Does the entry list more authors than distinct institutions?", "Is the author count higher than the institution count?"],
                  ["Does the entry list fewer authors than distinct institutions?", "Is the author count below the institution count?"],
                  elig=lambda r: r["n_authors"] != r["n_inst"] and r["n_inst"] > 0, why="len(authorships) > institutions_distinct_count"))
    add(bool_task("oa_oa_and_cited10", ["is_oa", "cited_by_count"], lambda r: bool(r["is_oa"]) and r["cited_by"] >= 10, "",
                  ["Is the open access flag true and the citation count 10 or more?",
                   "Does the work have both a true open access flag and at least 10 citations?"],
                  ["Is it true that the work does not meet both conditions: open access flag true and 10 or more citations?"],
                  why="is_oa and cited_by_count >= 10"))

    # --- carded yes/no (the card defines the concept) -----------------------------------------------------------
    for thr in (10, 50, 200):
        add(concept_task(f"oa_c_highly_cited_{thr}", ["cited_by_count"], lambda r, t=thr: r["cited_by"] >= t, "highly cited",
                         yn_card(f"the citation count is {thr} or more", f"the citation count is below {thr}"),
                         why=f"cited_by_count >= {thr}"))
    add(concept_task("oa_c_free_to_read", ["oa_status"], lambda r: r["oa_status"] != "closed", "free to read",
                     yn_card("the open-access status is gold, green, hybrid, bronze or diamond", "the open-access status is closed"),
                     why="oa_status != closed"))
    add(concept_task("oa_c_fully_open_venue", ["oa_status"], lambda r: r["oa_status"] in ("gold", "diamond"), "published in a fully open venue",
                     yn_card("the open-access status is gold or diamond", "the status is green, hybrid, bronze or closed"),
                     why="oa_status in {gold, diamond}"))
    for yrs in (5, 10):
        add(concept_task(f"oa_c_recent_{yrs}y", ["publication_year", "reference_year"], lambda r, y=yrs: REF_YEAR - r["year"] <= y, "recent",
                         yn_card(f"the publication year is within {yrs} years of the reference year (reference year minus publication year is at most {yrs})",
                                 f"the reference year minus the publication year is more than {yrs}"), why=f"{REF_YEAR} - year <= {yrs}"))
    for thr in (5, 10):
        add(concept_task(f"oa_c_large_team_{thr}", ["authors"], lambda r, t=thr: r["n_authors"] >= t, "a large-team paper",
                         yn_card(f"the entry lists {thr} or more authors", f"the entry lists fewer than {thr} authors"),
                         elig=lambda r: r["n_authors"] > 0, why=f"len(authorships) >= {thr}"))
    add(concept_task("oa_c_international", ["countries"], lambda r: r["n_countries"] >= 2, "an international collaboration",
                     yn_card("two or more distinct countries are listed", "zero or one country is listed"), why="countries_distinct_count >= 2"))
    add(concept_task("oa_c_version_of_record", ["version"], lambda r: r["version"] == "publishedVersion", "a version of record",
                     yn_card("the version field reads publishedVersion", "the version field reads submittedVersion or acceptedVersion"),
                     why="version == publishedVersion"))

    # --- choice heads --------------------------------------------------------------------------------------------
    for tag, b1, b2, b3 in (("a", 1, 10, 100), ("b", 5, 25, 250)):
        add(bucket_task(f"oa_ch_citation_class_{tag}", ["cited_by_count"],
                        lambda r, b1=b1, b2=b2, b3=b3: "none" if r["cited_by"] == 0 else "low" if r["cited_by"] < b2 else "moderate" if r["cited_by"] < b3 else "high",
                        ["none", "low", "moderate", "high"], "citation class",
                        defs=[("none", "Pick this when the citation count is 0."), ("low", f"Pick this when the count is from 1 to {b2 - 1}."),
                              ("moderate", f"Pick this when the count is from {b2} to {b3 - 1}."), ("high", f"Pick this when the count is {b3} or more.")],
                        why=f"cited_by_count bins 0 / 1-{b2 - 1} / {b2}-{b3 - 1} / {b3}+"))
    add(bucket_task("oa_ch_decade", ["publication_year"], lambda r: "before 1990s" if r["year"] < 1995 else "1995-2004" if r["year"] < 2005 else "2005-2014" if r["year"] < 2015 else "2015-2026",
                    ["before 1990s", "1995-2004", "2005-2014", "2015-2026"], "publication period", why="publication_year bins"))
    add(bucket_task("oa_ch_quarter", ["publication_date"], lambda r: f"Q{(int(r['date'][5:7]) - 1) // 3 + 1}", ["Q1", "Q2", "Q3", "Q4"],
                    "calendar quarter of the publication date", elig=lambda r: bool(r["date"]) and not r["date"].endswith("-01-01"),
                    why="month of publication_date -> quarter"))
    add(bucket_task("oa_ch_team_size", ["authors"], lambda r: "solo" if r["n_authors"] == 1 else "small" if r["n_authors"] <= 4 else "large" if r["n_authors"] <= 10 else "consortium",
                    ["solo", "small", "large", "consortium"], "team size class", elig=lambda r: r["n_authors"] > 0,
                    defs=[("solo", "Pick this when exactly 1 author is listed."), ("small", "Pick this when 2 to 4 authors are listed."),
                          ("large", "Pick this when 5 to 10 authors are listed."), ("consortium", "Pick this when more than 10 authors are listed.")],
                    why="len(authorships) bins"))
    colour = {"gold": "fully open venue", "diamond": "fully open venue", "green": "free copy elsewhere", "hybrid": "free copy elsewhere",
              "bronze": "free copy elsewhere", "closed": "no free copy"}
    add(bucket_task("oa_ch_access_group", ["oa_status"], lambda r: colour[r["oa_status"]], ["fully open venue", "free copy elsewhere", "no free copy"],
                    "access group", ordered=False, k=3,
                    defs=[("fully open venue", "Pick this when the open-access status is gold or diamond."),
                          ("free copy elsewhere", "Pick this when the status is green, hybrid or bronze."), ("no free copy", "Pick this when the status is closed.")],
                    why="oa_status -> group"))
    fam = {"article": "journal-style", "review": "journal-style", "letter": "journal-style", "editorial": "journal-style", "erratum": "journal-style",
           "book": "book-style", "book-chapter": "book-style", "dissertation": "book-style", "preprint": "open-draft or data", "dataset": "open-draft or data"}
    add(bucket_task("oa_ch_type_family", ["work_type"], lambda r: fam[r["type"]], ["journal-style", "book-style", "open-draft or data"], "type family",
                    ordered=False, k=3, elig=lambda r: r["type"] in fam,
                    defs=[("journal-style", "Pick this when the work type is article, review, letter, editorial or erratum."),
                          ("book-style", "Pick this when the type is book, book-chapter or dissertation."),
                          ("open-draft or data", "Pick this when the type is preprint or dataset.")], why="type -> family"))
    fd = _field_domain()
    doms = ["Physical Sciences", "Social Sciences", "Health Sciences", "Life Sciences"]
    flist = {d: sorted(f for f, x in fd.items() if x == d) for d in doms}
    add(bucket_task("oa_ch_topic_domain", ["field"], lambda r: fd[r["field"]], doms, "topic domain", ordered=False, k=4,
                    elig=lambda r: r["field"] in fd,
                    defs=[(d, "Pick this when the topic field is one of: " + "; ".join(flist[d]) + ".") for d in doms], why="field -> domain (upstream pairing)"))
    add(bucket_task("oa_ch_length_class", ["first_page", "last_page"], lambda r: "short" if pages(r) <= 4 else "medium" if pages(r) <= 14 else "long",
                    ["short", "medium", "long"], "length class", elig=lambda r: pages(r) is not None,
                    defs=[("short", "Pick this when the page span (last minus first, plus one) is 1 to 4 pages."),
                          ("medium", "Pick this when the span is 5 to 14 pages."), ("long", "Pick this when the span is 15 pages or more.")],
                    why="page span bins"))
    add(bucket_task("oa_ch_ref_density", ["references_count"], lambda r: "no references" if r["refs"] == 0 else "few" if r["refs"] < 20 else "many" if r["refs"] < 60 else "very many",
                    ["no references", "few", "many", "very many"], "reference load",
                    defs=[("no references", "Pick this when 0 references are listed."), ("few", "Pick this when 1 to 19 are listed."),
                          ("many", "Pick this when 20 to 59 are listed."), ("very many", "Pick this when 60 or more are listed.")], why="references count bins"))
    return T
