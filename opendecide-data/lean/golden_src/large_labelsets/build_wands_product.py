"""Build golden rows for wands_product: which furniture or lighting product class a retail product listing belongs to.

Source : WANDS - Wayfair ANnotation DataSet (Chen et al., ECIR 2022), github.com/wayfair/WANDS pinned to commit
         3b74dcf4ba29ab8ff3e6a50b5b09fc627cb882b5, dataset/product.csv (42,994 products; sha256 pinned). Only the
         product catalogue is used (never the query/relevance judgements).
Licence: MIT (https://github.com/wayfair/WANDS/blob/3b74dcf4ba29ab8ff3e6a50b5b09fc627cb882b5/LICENSE,
         'Copyright (c) 2021 ecir2022').
Texts  : product names and descriptions written for the Wayfair catalogue (human, released 2021, pre-LLM).
Labels : Wayfair's product_class for the product (catalogue taxonomy assigned by Wayfair / suppliers, human).
         Only single-class products whose top-level category is Furniture or Lighting and whose class has >= 40
         products are used: 49 classes. No splits -> train.
State  : 'Product: <name>' + 'Description: <description>' (description cut at 110 words). product_features are not
         shown (they contain a 'producttype' field that names the class).
Quality: out-of-fold TF-IDF + LR model trained on the other listings must rank the listing's own class first
         (p_gold >= 0.35), which drops mislabelled or multi-purpose listings (e.g. a coffee-table set filed as a
         coffee table); exact and near-exact duplicate descriptions (colour/size variants of one design) dropped;
         at most 32 rows per class. Options: 12-28 classes (gold, hand-listed confusable siblings, seeded fill).
Deterministic (seed 20261211). CPU only.
"""
import collections
import random
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ll_common as C  # noqa: E402

KEY = "wands_product"
SEED = 20261211
PER_CLASS = 32
COMMIT = "3b74dcf4ba29ab8ff3e6a50b5b09fc627cb882b5"
BASE = f"https://raw.githubusercontent.com/wayfair/WANDS/{COMMIT}/"
FILES = {"dataset/product.csv": "d993926254572e6eba96c8fd87cc549a17fb91ad3748308036eee4cf92b10ac6",
         "LICENSE": "e3ce14610132897db9f64e21d7871a7a60c0bc04364ec61e4faa99643c5072d6"}
CACHE = C.CACHE / "wands"
LICENCE = f"MIT (https://github.com/wayfair/WANDS/blob/{COMMIT}/LICENSE, 'Copyright (c) 2021 ecir2022')"
DATASET = "WANDS - Wayfair ANnotation DataSet (github wayfair/WANDS, dataset/product.csv), Furniture and Lighting classes"
QUESTION = "Which product category should this retail listing be filed under?"

DEFS = {
    "Accent Chairs": "Single upholstered or wooden chairs for living rooms and bedrooms (armchairs, club, wingback, slipper chairs) that do not recline or rock.",
    "Recliners": "Chairs whose back reclines with a footrest that extends, manually or powered, including lift and rocker recliners.",
    "Indoor Chaise Lounges": "Long indoor chairs with an extended seat that supports the legs for lounging.",
    "Ottomans": "Upholstered footstools, poufs and cubes used as footrests or extra seating, with or without storage.",
    "Benches": "Long backless or low-backed seats for several people, for entryways, bedrooms or dining, not outdoor.",
    "Office Chairs": "Desk chairs for working at a desk, usually swivel, height-adjustable and on casters (task, executive, mesh chairs).",
    "Dining Chairs": "Chairs sold for use at a dining or kitchen table, often in sets of two or more.",
    "Bar Stools": "Tall stools or chairs for bar-height or counter-height surfaces (about 24-30 inch seats).",
    "Coffee & Cocktail Tables": "A single low table placed in front of a sofa.",
    "End Tables": "A single small table placed beside a sofa or chair (side tables, C-tables, accent tables).",
    "Sofa & Console Tables": "A long narrow table placed behind a sofa or against a wall or in an entryway.",
    "Plant & Telephone Tables": "Small stands or tables made to hold plants or a telephone (plant stands, pedestals).",
    "Living Room Table Sets": "A set of two or more matching living-room tables sold together (e.g. coffee table plus end tables, nesting tables).",
    "Dining Tables": "A dining or kitchen table sold on its own, without chairs.",
    "Dining Table Sets": "A dining or kitchen table sold together with matching chairs or benches.",
    "Kitchen Islands": "Freestanding kitchen islands and carts providing extra counter space and storage.",
    "Poker & Casino Tables": "Tables made for card, poker and casino games, often with felt tops and chip trays.",
    "Beds": "Complete bed frames with headboard (panel, platform, sleigh, canopy, storage beds), not headboards alone.",
    "Headboards": "A headboard sold on its own, attached to a bed frame or wall.",
    "Daybeds & Guest Beds": "Daybeds, futons and other beds that double as seating or fold away for guests, including trundle daybeds.",
    "Dressers & Chests": "Bedroom storage with stacked drawers: dressers, chests of drawers and lingerie chests.",
    "Accent Chests / Cabinets": "Decorative chests and cabinets for storage and display in living spaces (accent cabinets, curio chests).",
    "Nightstands": "Small tables or cabinets placed beside a bed, usually with a drawer or shelf.",
    "Armoires & Wardrobes": "Tall freestanding cabinets with doors for hanging and storing clothes.",
    "Jewelry Armoires": "Freestanding or wall-mounted cabinets with compartments and hooks for storing jewelry, often with a mirror.",
    "Sideboards & Buffets": "Long low dining-room cabinets with doors and drawers for serving and storing dishware.",
    "TV Stands & Entertainment Centers": "Stands, consoles and wall units made to hold a television and media equipment.",
    "Bookcases": "Shelving units for books and display (standard, etagere, ladder, cube and corner bookcases).",
    "Office Storage Cabinets": "Office cabinets for files and supplies (filing cabinets, storage cabinets, lateral files).",
    "Bars & Bar Sets": "Home bar furniture: bar cabinets, bar carts, home bars and bar sets with stools.",
    "Desks": "Desks and workstations for working or writing (writing, computer, executive, standing desks).",
    "Makeup Vanities": "Makeup or dressing tables with a mirror, often sold with a stool.",
    "Sofas": "A single sofa or loveseat (couch) with a back and arms, not a sectional or a multi-piece set.",
    "Sectionals": "Sofas made of connected sections forming an L, U or modular shape.",
    "Living Room Sets": "A set of several matching seating pieces sold together (e.g. sofa plus loveseat and chair).",
    "Chairmats": "Floor mats placed under office chairs to protect carpet or hard floors.",
    "Projector Screens": "Screens for displaying images from a projector (manual, electric, fixed-frame, portable).",
    "Chandeliers": "Ceiling-hung light fixtures with several arms or lights suspended from a chain or rod, including pendant chandeliers.",
    "Flush Mount Lighting": "Ceiling light fixtures mounted directly against or close to the ceiling (flush and semi-flush mounts).",
    "Wall Sconces": "Indoor light fixtures mounted on a wall (not vanity bath bars and not outdoor fixtures).",
    "Vanity Lighting": "Bathroom vanity lights: wall-mounted bars or fixtures with several lights above or beside a mirror.",
    "Table Lamps": "Portable lamps that stand on a table, desk or nightstand, plugged into an outlet.",
    "Outdoor Wall Lights": "Weather-rated light fixtures mounted on an exterior wall (porch lights, outdoor sconces).",
    "Outdoor Lanterns & Lamps": "Freestanding or hanging outdoor lanterns and lamps, often solar or candle powered, not wall-mounted.",
    "Landscape Lighting": "Low outdoor lights for paths, gardens and yards (path lights, spotlights, well lights, deck lights).",
    "Under Cabinet Lighting": "Slim light fixtures or strips mounted under kitchen cabinets or shelves.",
    "Ceiling Fans": "Ceiling-mounted fans, with or without a light kit.",
    "Light Bulbs": "Replacement bulbs (LED, incandescent, halogen, fluorescent) sold on their own.",
    "Lighting Shades": "Replacement shades for lamps and light fixtures, sold on their own.",
}
CONFUSE = {
    "Accent Chairs": ["Recliners", "Indoor Chaise Lounges", "Dining Chairs", "Office Chairs", "Ottomans"],
    "Recliners": ["Accent Chairs", "Sofas", "Indoor Chaise Lounges"],
    "Indoor Chaise Lounges": ["Accent Chairs", "Daybeds & Guest Beds", "Benches", "Sofas"],
    "Ottomans": ["Benches", "Accent Chairs", "Coffee & Cocktail Tables"],
    "Benches": ["Ottomans", "Dining Chairs", "Indoor Chaise Lounges"],
    "Office Chairs": ["Dining Chairs", "Accent Chairs", "Chairmats", "Bar Stools"],
    "Dining Chairs": ["Bar Stools", "Accent Chairs", "Dining Table Sets", "Office Chairs"],
    "Bar Stools": ["Dining Chairs", "Bars & Bar Sets", "Office Chairs"],
    "Coffee & Cocktail Tables": ["End Tables", "Living Room Table Sets", "Sofa & Console Tables", "Ottomans"],
    "End Tables": ["Coffee & Cocktail Tables", "Nightstands", "Plant & Telephone Tables", "Living Room Table Sets"],
    "Sofa & Console Tables": ["Coffee & Cocktail Tables", "End Tables", "Sideboards & Buffets", "TV Stands & Entertainment Centers"],
    "Plant & Telephone Tables": ["End Tables", "Sofa & Console Tables", "Bookcases"],
    "Living Room Table Sets": ["Coffee & Cocktail Tables", "End Tables", "Living Room Sets"],
    "Dining Tables": ["Dining Table Sets", "Kitchen Islands", "Desks", "Poker & Casino Tables"],
    "Dining Table Sets": ["Dining Tables", "Dining Chairs", "Bars & Bar Sets"],
    "Kitchen Islands": ["Dining Tables", "Bars & Bar Sets", "Sideboards & Buffets"],
    "Poker & Casino Tables": ["Dining Tables", "Dining Table Sets"],
    "Beds": ["Headboards", "Daybeds & Guest Beds"],
    "Headboards": ["Beds", "Daybeds & Guest Beds"],
    "Daybeds & Guest Beds": ["Beds", "Sofas", "Indoor Chaise Lounges"],
    "Dressers & Chests": ["Nightstands", "Accent Chests / Cabinets", "Armoires & Wardrobes"],
    "Accent Chests / Cabinets": ["Dressers & Chests", "Sideboards & Buffets", "Bookcases", "Office Storage Cabinets"],
    "Nightstands": ["End Tables", "Dressers & Chests", "Accent Chests / Cabinets"],
    "Armoires & Wardrobes": ["Jewelry Armoires", "Dressers & Chests", "Accent Chests / Cabinets"],
    "Jewelry Armoires": ["Armoires & Wardrobes", "Makeup Vanities", "Accent Chests / Cabinets"],
    "Sideboards & Buffets": ["Accent Chests / Cabinets", "TV Stands & Entertainment Centers", "Bars & Bar Sets", "Sofa & Console Tables"],
    "TV Stands & Entertainment Centers": ["Sideboards & Buffets", "Bookcases", "Sofa & Console Tables"],
    "Bookcases": ["Office Storage Cabinets", "TV Stands & Entertainment Centers", "Accent Chests / Cabinets"],
    "Office Storage Cabinets": ["Bookcases", "Accent Chests / Cabinets", "Desks"],
    "Bars & Bar Sets": ["Bar Stools", "Sideboards & Buffets", "Kitchen Islands"],
    "Desks": ["Makeup Vanities", "Dining Tables", "Office Storage Cabinets"],
    "Makeup Vanities": ["Desks", "Jewelry Armoires", "Dressers & Chests"],
    "Sofas": ["Sectionals", "Living Room Sets", "Daybeds & Guest Beds", "Recliners"],
    "Sectionals": ["Sofas", "Living Room Sets"],
    "Living Room Sets": ["Sofas", "Sectionals", "Living Room Table Sets"],
    "Chairmats": ["Office Chairs"], "Projector Screens": ["TV Stands & Entertainment Centers"],
    "Chandeliers": ["Flush Mount Lighting", "Wall Sconces", "Ceiling Fans"],
    "Flush Mount Lighting": ["Chandeliers", "Ceiling Fans", "Wall Sconces"],
    "Wall Sconces": ["Vanity Lighting", "Outdoor Wall Lights", "Flush Mount Lighting"],
    "Vanity Lighting": ["Wall Sconces", "Flush Mount Lighting"],
    "Table Lamps": ["Lighting Shades", "Outdoor Lanterns & Lamps", "Wall Sconces"],
    "Outdoor Wall Lights": ["Wall Sconces", "Outdoor Lanterns & Lamps", "Landscape Lighting"],
    "Outdoor Lanterns & Lamps": ["Outdoor Wall Lights", "Landscape Lighting", "Table Lamps"],
    "Landscape Lighting": ["Outdoor Lanterns & Lamps", "Outdoor Wall Lights", "Under Cabinet Lighting"],
    "Under Cabinet Lighting": ["Landscape Lighting", "Light Bulbs", "Vanity Lighting"],
    "Ceiling Fans": ["Flush Mount Lighting", "Chandeliers"],
    "Light Bulbs": ["Lighting Shades", "Under Cabinet Lighting"], "Lighting Shades": ["Light Bulbs", "Table Lamps"],
}


def clean(t):
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"\s+([,.!?;:])", r"\1", t).replace(" 's", "'s").replace(" n't", "n't")
    return t


def main():
    paths = {f: C.fetch(BASE + f, CACHE / Path(f).name, sha)[0] for f, sha in FILES.items()}
    df = pd.read_csv(paths["dataset/product.csv"], sep="\t", dtype=str, keep_default_na=False)
    df = df.rename(columns={"category hierarchy": "ch"})
    df["top"] = df["ch"].str.split(" / ").str[0]
    df = df[df["product_class"].isin(DEFS) & df["top"].isin(["Furniture", "Lighting"])]
    df = df[df["product_description"].str.split().str.len() >= 12]
    df["name"] = df["product_name"].map(clean)
    df["desc"] = df["product_description"].map(clean).map(lambda t: " ".join(t.split()[:110]))
    df = df.drop_duplicates(subset="desc")
    print("candidate products:", len(df), "classes:", df["product_class"].nunique())
    assert set(df["product_class"]) == set(DEFS), set(DEFS) - set(df["product_class"])
    df = df.sort_values("product_id", key=lambda s: s.astype(int))
    texts = [f"{n} || {d}" for n, d in zip(df["name"], df["desc"])]
    keep, pg, po = C.oof_filter(texts, list(df["product_class"]), seed=SEED, min_gold=0.15, max_other=0.6)
    keep = [k and g >= 0.35 and g >= o for k, g, o in zip(keep, pg, po)]
    print("OOF drops:", sum(not k for k in keep), "of", len(keep))
    recs = [(pid, n, d, c) for (pid, n, d, c), k in zip(zip(df["product_id"], df["name"], df["desc"], df["product_class"]), keep) if k]
    rng = random.Random(SEED)
    rng.shuffle(recs)
    nd = C.NearDup(thr=0.6, n=5)
    pools = collections.defaultdict(list)
    for pid, n, d, c in recs:
        if len(pools[c]) >= PER_CLASS or nd.seen(d):
            continue
        pools[c].append((pid, n, d, c))
    labels = sorted(DEFS)
    rows = []
    for c in labels:
        for pid, n, d, _ in pools[c]:
            opts = C.option_subset(c, labels, CONFUSE.get(c, []), rng, lo=12, hi=28)
            rows.append({
                "key": KEY, "rid": f"wands:{pid}", "state": f"Product: {n}\nDescription: {d}",
                "instructions": QUESTION, "options": opts, "gold": c, "soft": None,
                "meta": {"dataset": DATASET, "config": "49 Wayfair product classes (Furniture + Lighting)",
                         "revision": f"git:{COMMIT}; sha256:{FILES['dataset/product.csv']}", "licence": LICENCE,
                         "split": "train", "orig_label": c, "family": C.FAMILY, "edge": None},
            })
    rows = C.final_dedup(rows)  # reviewer fix: exact near-duplicate pass (LSH misses pairs)
    rng.shuffle(rows)
    out = C.write_rows(KEY, rows)
    C.write_defs(KEY, DEFS)
    print("wrote", out)
    C.summary(rows)
    C.show(rows, 6, seed=6)


if __name__ == "__main__":
    main()
