"""musicbrainz.py: metadata mapper for md_musicbrainz (MusicBrainz release groups; core data CC0; music).

Upstream fields used as targets: first-release-date, primary-type, secondary-types, artist-credit count, release count,
tags (genre tags), disambiguation presence, release statuses, title shape. Artist names are never kept (snapshot drops
them at fetch). Titles appear in the state only; golds that read the title are surface properties (word count, first word,
digit, first letter).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from _common_a import (COUNT_NEG, COUNT_POS, EQ_NEG, EQ_POS, YEAR_NEG, YEAR_POS, Task, bool_task, bucket_task, concept_task, eq_task, ge_task, yn_card)

NAME = "musicbrainz"
DOMAIN = "music"
LICENCE = "CC0 1.0 (MusicBrainz core data, release-group entity; MetaBrainz Foundation)"
HEADERS = ["Music catalogue entry", "Release-group record", "Discography database row", "Entry from a music metadata database"]
RAW = Path(__file__).resolve().parent.parent / "raw_a" / "musicbrainz" / "release_groups.json"
GROUPS = {"first_release_date": "date", "primary_type": "ptype", "secondary_types": "stype"}
HAS_SEC_POS = ["Is '{v}' listed among the secondary types?", "Does the secondary type list include '{v}'?"]
HAS_SEC_NEG = ["Is it true that '{v}' is not listed among the secondary types?", "Is it true that the secondary type list does not include '{v}'?"]


def load():
    return [x for x in json.loads(RAW.read_text()) if x["title"] and x["first_release_date"] and x["primary_type"]]


def rid_of(r):
    return r["id"]


def group_of(k):
    return GROUPS.get(k, k)


def year(r):
    return int(r["first_release_date"][:4])


def prec(r):
    return {4: "year", 7: "month", 10: "day"}.get(len(r["first_release_date"]))


def fields_of(r):
    return {
        "release_group_id": ("Release group ID", r["id"]), "title": ("Title", r["title"]), "first_release_date": ("First release date", r["first_release_date"]),
        "primary_type": ("Primary type", r["primary_type"]), "secondary_types": ("Secondary types", ", ".join(r["secondary_types"]) if r["secondary_types"] else "none"),
        "credits": ("Artist credits", str(r["n_credits"])), "releases": ("Releases in group", str(r["n_releases"])),
        "tags": ("Genre tags", ", ".join(r["tags"]) if r["tags"] else "none"), "tag_count": ("Genre tag count", str(len(r["tags"]))),
        "disambiguation": ("Disambiguation comment", "present" if r["disambiguation"] else "none"), "statuses": ("Release statuses", ", ".join(r["statuses"]) if r["statuses"] else None),
    }


def tasks():
    T = []
    add = T.append
    for y in (1970, 1980, 1990, 2000, 2010, 2020):
        add(ge_task(f"mb_year_ge_{y}", ["first_release_date"], year, y, pos=YEAR_POS, neg=YEAR_NEG, fmt={"verb": "first released", "what": "first-release"}, why=f"year(first-release-date) >= {y}"))
    add(bool_task("mb_has_day", ["first_release_date"], lambda r: prec(r) == "day", "", ["Does the first release date include the day of the month?", "Is the first release date given as a full year-month-day date?"],
                  ["Is it true that the first release date does not include the day of the month?", "Is it true that the first release date is not given as a full year-month-day date?"],
                  elig=lambda r: prec(r) is not None, why="len(date) == 10"))
    add(bool_task("mb_has_month", ["first_release_date"], lambda r: prec(r) in ("month", "day"), "", ["Does the first release date include the month?", "Is the month part of the first release date given?"],
                  ["Is it true that the first release date does not include the month?", "Is it true that the month part of the first release date is not given?"],
                  elig=lambda r: prec(r) is not None, why="len(date) >= 7"))
    for v in ("Album", "Single", "EP", "Other", "Broadcast"):
        add(eq_task(f"mb_ptype_is_{v.lower()}", ["primary_type"], lambda r: r["primary_type"], v, "primary type", why=f"primary-type == {v}"))
    for v in ("Live", "Compilation", "Soundtrack", "Remix", "Demo"):
        add(Task(f"mb_stype_has_{v.lower()}", "yn", ["secondary_types"], pred=lambda r, v=v: v in r["secondary_types"], pos=HAS_SEC_POS, neg=HAS_SEC_NEG, fmt={"v": v}, why=f"{v} in secondary-types"))
    add(bool_task("mb_has_secondary", ["secondary_types"], lambda r: bool(r["secondary_types"]), "", ["Does the entry list at least one secondary type?", "Is any secondary type recorded for the entry?"],
                  ["Is it true that no secondary type is recorded for the entry?", "Is it true that the entry lists no secondary type?"], why="len(secondary-types) > 0"))
    add(ge_task("mb_credits_ge_2", ["credits"], lambda r: r["n_credits"], 2, fmt={"things": "artist credits", "thing": "artist-credit"}, why="len(artist-credit) >= 2"))
    for n in (2, 3, 5):
        add(ge_task(f"mb_releases_ge_{n}", ["releases"], lambda r: r["n_releases"], n, fmt={"things": "releases in the group", "thing": "release"}, why=f"releases >= {n}"))
    for n in (1, 3, 5):
        add(ge_task(f"mb_tags_ge_{n}", ["tag_count"], lambda r: len(r["tags"]), n, fmt={"things": "genre tags", "thing": "genre-tag"}, why=f"tags >= {n}"))
    for v in ("rock", "electronic", "pop", "punk", "hip hop", "jazz"):
        add(Task(f"mb_tag_is_{v.replace(' ', '_')}", "yn", ["tags"], pred=lambda r, v=v: v in r["tags"],
                 pos=["Is '{v}' one of the genre tags?", "Does the genre tag list include '{v}'?"], neg=["Is it true that '{v}' is not one of the genre tags?", "Is it true that the genre tag list does not include '{v}'?"],
                 fmt={"v": v}, why=f"{v} in tags"))
    for n in (3, 5):
        add(ge_task(f"mb_title_words_ge_{n}", ["title"], lambda r: len(r["title"].split()), n, fmt={"things": "words in the title", "thing": "title-word"}, why=f"len(title.split()) >= {n}"))
    add(bool_task("mb_title_the", ["title"], lambda r: r["title"].lower().startswith("the "), "", ["Does the title start with the word 'The'?", "Is 'The' the first word of the title?"],
                  ["Is it true that the title does not start with the word 'The'?", "Is it true that 'The' is not the first word of the title?"], why="title starts with 'The '"))
    add(bool_task("mb_title_digit", ["title"], lambda r: bool(re.search(r"\d", r["title"])), "", ["Does the title contain a digit?", "Is there at least one digit character in the title?"],
                  ["Is it true that the title contains no digit?", "Is it true that no digit character appears in the title?"], why="digit in title"))
    add(ge_task("mb_title_len_ge_20", ["title"], lambda r: len(r["title"]), 20, fmt={"things": "characters in the title", "thing": "title-length"}, why="len(title) >= 20"))
    add(bool_task("mb_has_disamb", ["disambiguation"], lambda r: bool(r["disambiguation"]), "", ["Does the entry carry a disambiguation comment?", "Is a disambiguation comment recorded for this entry?"],
                  ["Is it true that the entry carries no disambiguation comment?", "Is it true that no disambiguation comment is recorded for this entry?"], why="disambiguation non-empty"))
    for v in ("Official", "Promotion", "Bootleg"):
        add(Task(f"mb_status_has_{v.lower()}", "yn", ["statuses"], pred=lambda r, v=v: v in r["statuses"], elig=lambda r: bool(r["statuses"]),
                 pos=["Does the release status list include '{v}'?", "Is '{v}' among the release statuses?"], neg=["Is it true that the release status list does not include '{v}'?", "Is it true that '{v}' is not among the release statuses?"],
                 fmt={"v": v}, why=f"{v} in statuses"))
    add(bool_task("mb_single_2000", ["primary_type", "first_release_date"], lambda r: r["primary_type"] == "Single" and year(r) >= 2000, "",
                  ["Is the primary type Single and the first release year 2000 or later?", "Does the entry have both the primary type Single and a first release year of 2000 or later?"],
                  ["Is it true that the entry does not have both the primary type Single and a first release year of 2000 or later?"], why="Single and year >= 2000"))
    add(bool_task("mb_album_multi", ["primary_type", "releases"], lambda r: r["primary_type"] == "Album" and r["n_releases"] >= 2, "",
                  ["Is the primary type Album and the release count 2 or more?", "Does the entry have both the primary type Album and 2 or more releases?"],
                  ["Is it true that the entry does not have both the primary type Album and 2 or more releases?"], why="Album and releases >= 2"))
    # carded concepts
    add(concept_task("mb_c_studio_style", ["primary_type", "secondary_types"], lambda r: r["primary_type"] == "Album" and not r["secondary_types"], "a plain album",
                     yn_card("the primary type is Album and no secondary type is listed", "the primary type is not Album or at least one secondary type is listed"), why="Album and no secondary"))
    add(concept_task("mb_c_short_format", ["primary_type"], lambda r: r["primary_type"] in ("EP", "Single"), "a short-format release", yn_card("the primary type is EP or Single", "the primary type is Album, Broadcast or Other"),
                     elig=lambda r: r["primary_type"] in ("EP", "Single", "Album", "Broadcast", "Other"), why="type in EP, Single"))
    add(concept_task("mb_c_pre_2000", ["first_release_date"], lambda r: year(r) < 2000, "from the pre-2000 era", yn_card("the first release year is before 2000", "the first release year is 2000 or later"), why="year < 2000"))
    add(concept_task("mb_c_reissued", ["releases"], lambda r: r["n_releases"] >= 3, "widely reissued", yn_card("the group holds 3 or more releases", "the group holds fewer than 3 releases"), why="releases >= 3"))
    add(concept_task("mb_c_collab", ["credits"], lambda r: r["n_credits"] >= 2, "a collaboration", yn_card("two or more artist credits are listed", "exactly one artist credit is listed"), why="credits >= 2"))
    add(concept_task("mb_c_well_tagged", ["tag_count"], lambda r: len(r["tags"]) >= 4, "well tagged", yn_card("4 or more genre tags are listed", "fewer than 4 genre tags are listed"), why="tags >= 4"))
    add(concept_task("mb_c_official_only", ["statuses"], lambda r: r["statuses"] == ["Official"], "official-only", yn_card("the status list is exactly Official", "the status list holds anything else or more than one status"),
                     elig=lambda r: bool(r["statuses"]), why="statuses == [Official]"))
    # choice heads
    add(bucket_task("mb_ch_decade", ["first_release_date"], lambda r: "1960s or earlier" if year(r) < 1970 else f"{year(r) // 10 * 10}s", ["1960s or earlier", "1970s", "1980s", "1990s", "2000s", "2010s", "2020s"], "decade of the first release",
                    ordered=False, k=5, why="year -> decade"))
    add(bucket_task("mb_ch_ptype", ["primary_type"], lambda r: r["primary_type"], ["Album", "Single", "EP", "Other", "Broadcast"], "primary type", ordered=False, k=4, why="primary-type"))
    add(bucket_task("mb_ch_precision", ["first_release_date"], lambda r: {"year": "year only", "month": "year and month", "day": "full date"}[prec(r)], ["year only", "year and month", "full date"], "date precision",
                    elig=lambda r: prec(r) is not None, why="len(date)"))
    add(bucket_task("mb_ch_release_count", ["releases"], lambda r: "single release" if r["n_releases"] == 1 else "a few" if r["n_releases"] <= 3 else "many", ["single release", "a few", "many"], "release-count class",
                    defs=[("single release", "Pick this when the group holds exactly 1 release."), ("a few", "Pick this for 2 or 3 releases."), ("many", "Pick this for 4 or more releases.")], why="releases bins"))
    add(bucket_task("mb_ch_tag_load", ["tag_count"], lambda r: "untagged" if not r["tags"] else "lightly tagged" if len(r["tags"]) <= 2 else "richly tagged", ["untagged", "lightly tagged", "richly tagged"], "tagging level",
                    defs=[("untagged", "Pick this when no genre tag is listed."), ("lightly tagged", "Pick this for 1 or 2 genre tags."), ("richly tagged", "Pick this for 3 or more genre tags.")], why="tags bins"))
    fam = {"Live": "live or demo", "Demo": "live or demo", "Compilation": "compilation or mix", "Remix": "compilation or mix", "DJ-mix": "compilation or mix", "Mixtape/Street": "compilation or mix",
           "Soundtrack": "soundtrack or spoken", "Spokenword": "soundtrack or spoken", "Interview": "soundtrack or spoken"}
    add(bucket_task("mb_ch_stype_family", ["secondary_types"], lambda r: fam[r["secondary_types"][0]], ["live or demo", "compilation or mix", "soundtrack or spoken"], "secondary-type family", ordered=False, k=3,
                    elig=lambda r: len(r["secondary_types"]) == 1 and r["secondary_types"][0] in fam,
                    defs=[("live or demo", "Pick this when the only secondary type is Live or Demo."), ("compilation or mix", "Pick this when it is Compilation, Remix, DJ-mix or Mixtape/Street."),
                          ("soundtrack or spoken", "Pick this when it is Soundtrack, Spokenword or Interview.")], why="single secondary type -> family"))
    add(bucket_task("mb_ch_title_initial", ["title"], lambda r: "A-F" if r["title"][0].upper() < "G" else "G-M" if r["title"][0].upper() < "N" else "N-S" if r["title"][0].upper() < "T" else "T-Z",
                    ["A-F", "G-M", "N-S", "T-Z"], "alphabetical block of the title's first letter", elig=lambda r: r["title"][0].isascii() and r["title"][0].isalpha(), why="first letter"))
    add(bucket_task("mb_ch_title_length", ["title"], lambda r: "one word" if len(r["title"].split()) == 1 else "two or three words" if len(r["title"].split()) <= 3 else "four or more words",
                    ["one word", "two or three words", "four or more words"], "title length class", why="word count"))
    add(bucket_task("mb_ch_era", ["first_release_date"], lambda r: "before 1980" if year(r) < 1980 else "1980-1999" if year(r) < 2000 else "2000-2014" if year(r) < 2015 else "2015 or later", ["before 1980", "1980-1999", "2000-2014", "2015 or later"],
                    "era", defs=[("before 1980", "Pick this when the first release year is before 1980."), ("1980-1999", "Pick this for 1980 to 1999."), ("2000-2014", "Pick this for 2000 to 2014."), ("2015 or later", "Pick this for 2015 and later.")], why="year bins"))
    return T
