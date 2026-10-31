"""Build golden rows for naics_subsector: which NAICS 2022 subsector (3-digit industry code) a business activity is in.

Source : U.S. Census Bureau, 2022 NAICS Index File (https://www.census.gov/naics/2022NAICS/2022_NAICS_Index_File.xlsx,
         20,398 index entries, each an activity/product description with its 6-digit 2022 NAICS code) and the
         2-6 digit code/title list (https://www.census.gov/naics/2022NAICS/2-6%20digit_2022_Codes.xlsx), sha256 pinned.
Licence: US Government work, public domain (17 USC 105): the NAICS United States 2022 manual and index are
         published by the Executive Office of the President, Office of Management and Budget, and the U.S. Census
         Bureau (https://www.census.gov/naics/).
Texts  : the index item descriptions, written by Census/ECPC classification staff (human, 2022 edition; the NAICS
         index is maintained by hand, no model involvement).
Labels : the NAICS code the index assigns to each entry (by construction of the classification); the builder keeps
         the first 3 digits (96 subsectors). No splits -> train.
Options: 12-32 subsectors per row: the gold, the other subsectors of the same sector, the usual make / wholesale /
         retail / service neighbours of that sector (SECTOR_CONFUSE), then a seeded random fill.
Quality: the index has idiosyncratic placements, so an entry is kept only when an out-of-fold TF-IDF + LR model
         trained on the other entries also ranks its subsector first (p_gold >= 0.3); this drops entries whose
         wording is typical of another subsector; exact and near-exact
         duplicates (word-bigram Jaccard >= 0.6) dropped; at most 24 rows per subsector (round robin).
Edge   : entries with an '(except ...)' clause are tagged 'exception'.
Definitions: Claude-written one-sentence subsector definitions (naics_defs.py).
Deterministic (seed 20261209). CPU only.
"""
import collections
import random
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ll_common as C  # noqa: E402
import naics_defs as N  # noqa: E402

KEY = "naics_subsector"
SEED = 20261209
PER_CLASS = 26
BASE = "https://www.census.gov/naics/2022NAICS/"
FILES = {"2022_NAICS_Index_File.xlsx": ("2022_NAICS_Index_File.xlsx", None),
         "2-6_digit_2022_Codes.xlsx": ("2-6%20digit_2022_Codes.xlsx", None)}
SHAS = {"2022_NAICS_Index_File.xlsx": "6506b37b9546dd9cec1f8b79e0b38b68e547a5cce5fd6f8332d35024dbd6cd63", "2-6_digit_2022_Codes.xlsx": "be12ba41002803359f49181c9bf33a03fbd08578f4f4a4c0bbad7aadaaea0316"}
CACHE = C.CACHE / "naics"
LICENCE = ("US Government work, public domain (17 USC 105): North American Industry Classification System, United "
           "States 2022, Executive Office of the President / Office of Management and Budget and U.S. Census Bureau "
           "(https://www.census.gov/naics/; files https://www.census.gov/naics/2022NAICS/2022_NAICS_Index_File.xlsx "
           "and 2-6 digit_2022_Codes.xlsx)")
DATASET = "U.S. Census Bureau 2022 NAICS Index File (census.gov/naics/2022NAICS/2022_NAICS_Index_File.xlsx)"
QUESTION = "Which NAICS 2022 subsector does a business whose primary activity is described here belong to?"


def main():
    paths = {}
    for local, (remote, _) in FILES.items():
        paths[local], _ = C.fetch(BASE + remote, CACHE / local, SHAS[local])
    ix = pd.read_excel(paths["2022_NAICS_Index_File.xlsx"], dtype=str)
    ix.columns = ["code", "desc"]
    cd = pd.read_excel(paths["2-6_digit_2022_Codes.xlsx"], dtype=str)
    cd.columns = ["seq", "code", "title", "a", "b"]
    cd = cd.dropna(subset=["code"])
    titles = {c: t.strip() for c, t in zip(cd["code"], cd["title"]) if len(c) == 3}
    assert set(titles) == set(N.DEFS), set(titles) ^ set(N.DEFS)
    names = {c: f"{c} {titles[c]}" for c in titles}
    ix = ix.dropna()
    ix["desc"] = ix["desc"].str.strip().str.replace(r"\s+", " ", regex=True)
    ix["sub"] = ix["code"].str[:3]
    ix = ix[ix["sub"].isin(titles)]
    # descriptions listed under two different subsectors are ambiguous -> drop
    nsub = ix.groupby(ix["desc"].map(C.norm))["sub"].nunique()
    amb = set(nsub[nsub > 1].index)
    ix = ix[~ix["desc"].map(C.norm).isin(amb)].drop_duplicates(subset="desc")
    print("index entries:", len(ix), "ambiguous dropped:", len(amb))
    rng = random.Random(SEED)
    recs = list(zip(ix["code"], ix["desc"], ix["sub"]))
    recs.sort()
    keep, pg, po = C.oof_filter([r[1] for r in recs], [r[2] for r in recs], seed=SEED, min_gold=0.15, max_other=0.6)
    # stricter than the other builders: the index has idiosyncratic placements, so an entry is kept only when the
    # held-out lexical model also ranks its subsector first (p_gold >= 0.3 and >= every other subsector)
    keep = [k and g >= 0.3 and g >= o for k, g, o in zip(keep, pg, po)]
    print("OOF drops:", sum(not k for k in keep), "of", len(recs))
    recs = [r for r, k in zip(recs, keep) if k]
    rng.shuffle(recs)
    nd = C.NearDup(thr=0.6, n=2)
    pools = collections.defaultdict(list)
    for code, desc, sub in recs:
        if len(pools[sub]) >= PER_CLASS or len(desc.split()) < 2:
            continue
        if nd.seen(desc):
            continue
        pools[sub].append((code, desc, sub))
    all_names = [names[c] for c in sorted(names)]
    rows = []
    for sub in sorted(pools):
        sector = sub[:2]
        siblings = [c for c in sorted(titles) if c[:2] == sector or (sector in ("31", "32", "33") and c[0] == "3")
                    or (sector in ("44", "45") and c[:2] in ("44", "45")) or (sector in ("48", "49") and c[:2] in ("48", "49"))]
        for code, desc, _ in pools[sub]:
            conf = [c for c in siblings if c != sub]
            rng.shuffle(conf)
            extra = [c for c in N.SECTOR_CONFUSE.get(sector, []) if c in titles and c != sub]
            conf = conf[:10] + extra
            opts = C.option_subset(names[sub], all_names, [names[c] for c in conf], rng, lo=12, hi=32)
            edge = "exception" if re.search(r"\(except\b|\bexcept\b", desc) else None
            rows.append({
                "key": KEY, "rid": f"naics2022-index:{code}:{C.norm(desc)[:80]}", "state": desc,
                "instructions": QUESTION, "options": opts, "gold": names[sub], "soft": None,
                "meta": {"dataset": DATASET, "config": "96 NAICS 2022 subsectors (3-digit)",
                         "revision": "NAICS 2022 index file; sha256 " + SHAS["2022_NAICS_Index_File.xlsx"],
                         "licence": LICENCE, "split": "train", "orig_label": code, "family": C.FAMILY,
                         "edge": edge},
            })
    rows = C.final_dedup(rows)  # reviewer fix: exact near-duplicate pass (LSH misses pairs)
    rng.shuffle(rows)
    out = C.write_rows(KEY, rows)
    C.write_defs(KEY, {names[c]: N.DEFS[c] for c in names})
    print("wrote", out)
    C.summary(rows)
    C.show(rows, 8, seed=5)


if __name__ == "__main__":
    main()
