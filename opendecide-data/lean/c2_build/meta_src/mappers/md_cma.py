"""Mapper: md_cma (Cleveland Museum of Art Open Access, CC0; the single museum source of the block, md_met is not used).

Run (from lean/c2_build):  nice -n 10 .venv/bin/python -B meta_src/mappers/md_cma.py
Input: meta_src/raw/cma/p_*.json (API pages, records with share_license_status CC0; untrusted download).
Output: data/c2_md_parts/md_cma/. Gold = a program over the record's own fields, every field it reads is printed in the
state. Privacy: no artist, donor or tombstone text; the credit line is reduced to its first word; the title appears only in
the title tasks.
"""
import glob
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mdkit_c as K  # noqa: E402

SRC = "md_cma"
LIC = {"name": "Creative Commons Zero (CC0)", "url": "https://github.com/ClevelandMuseumArt/openaccess",
       "dataset_url": "https://openaccess-api.clevelandart.org/api/artworks/",
       "verified": "repo README waives all copyright via CC0; every record used carries share_license_status CC0"}
N = 15
TYPE_GROUP = {
    "paintings": ["Painting", "Portrait Miniature"],
    "works on paper and books": ["Print", "Drawing", "Photograph", "Portfolio", "Manuscript", "Bound Volume", "Calligraphy"],
    "sculpture and carving": ["Sculpture", "Ivory", "Jade", "Stone", "Mask", "Glyptic", "Wood"],
    "textiles and dress": ["Textile", "Lace", "Embroidery", "Garment", "Tapestry", "Velvet", "Basketry", "Leather"],
    "metal, ceramic and glass wares": ["Ceramic", "Metalwork", "Arms and Armor", "Jewelry", "Coins", "Glass", "Silver", "Enamel", "Lacquer", "Vessels", "Lamp"],
    "furniture and other objects": ["Furniture and woodwork", "Funerary Equipment", "Miscellaneous", "Musical Instrument", "Tools and Equipment"]}
T2G = {t: g for g, ts in TYPE_GROUP.items() for t in ts}
MEDIUM = [("oil paint", ["oil"]), ("ink, watercolor or tempera", ["ink", "watercolor", "gouache", "tempera", "wash"]),
          ("metal", ["bronze", "gold", "silver", "iron", "copper", "brass", "steel", "pewter", "gilt"]),
          ("stone", ["marble", "limestone", "granite", "sandstone", "alabaster", "stone", "jade", "basalt"]),
          ("ceramic or glass", ["porcelain", "earthenware", "stoneware", "ceramic", "glaze", "clay", "terracotta", "glass", "faience"]),
          ("textile", ["silk", "wool", "linen", "cotton", "embroider", "velvet", "tapestry"])]


def medium_class(t):
    s = t["technique"].lower()
    for name, kws in MEDIUM:
        if any(k in s for k in kws):
            return name
    return "other"


def era(y):
    return "before 1000" if y < 1000 else "1000 to 1499" if y < 1500 else "1500 to 1799" if y < 1800 else "1800 to 1899" if y < 1900 else "1900 or later"


def load():
    out = []
    for f in sorted(glob.glob(str(K.META_SRC / "raw" / "cma" / "p_*.json"))):
        try:
            d = json.load(open(f))["data"]
        except Exception:
            continue
        for r in d:
            if r.get("share_license_status") != "CC0":
                continue
            try:
                e0, e1 = int(r["creation_date_earliest"]), int(r["creation_date_latest"])
            except (TypeError, ValueError, KeyError):
                continue
            m = r.get("measurements") or ""
            mm = re.search(r"Unframed: ([\d.]+) x ([\d.]+) cm", m) or re.match(r"([\d.]+) x ([\d.]+) cm", m)
            acc = re.match(r"^(\d{4})\.", r.get("accession_number") or "")
            cul = r.get("culture")
            cul = "; ".join(cul) if isinstance(cul, list) else (cul or "")
            if not (1 <= e0 <= e1 <= 2026) or not r.get("technique") or r.get("type") not in T2G or not r.get("department"):
                continue
            h = float(mm.group(1)) if mm else None
            w = float(mm.group(2)) if mm else None
            cl = (r.get("creditline") or "").split(" ")[0].strip(",;.")
            out.append({"id": str(r["id"]), "acc": r["accession_number"], "accy": int(acc.group(1)) if acc else None,
                        "type": r["type"], "coll": r.get("collection") or "", "tech": r["technique"], "technique": r["technique"],
                        "culture": cul, "dtext": r.get("creation_date") or "", "e0": e0, "e1": e1, "meas": m if mm else None,
                        "h": h, "w": w, "credit": cl, "dept": r["department"], "title": r.get("title") or ""})
    return out


def state(show_title=False):
    def f(t):
        L = []
        if show_title:
            L.append(("Title", K.clip(t["title"], 90)))
        L += [("Accession number", t["acc"]), ("Object type", t["type"]), ("Collection", t["coll"] or "not listed"),
              ("Technique", K.clip(t["tech"], 90)), ("Culture", K.clip(t["culture"], 60) or "not listed"),
              ("Date text", t["dtext"]), ("Date range", f"{t['e0']} to {t['e1']}"),
              ("Measurements", K.clip(t["meas"], 150) if t["meas"] else "not listed"), ("Credit line, first word", t["credit"])]
        return K.kv(L)
    return f


def main():
    recs = load()
    key = lambda t: t["id"]
    print("records", len(recs))
    B = K.Builder(SRC, "art / museum collections", LIC)
    st = state()
    grp = {"all": recs, "paintings": [t for t in recs if t["type"] == "Painting"],
           "works on paper": [t for t in recs if t["type"] in ("Print", "Drawing", "Photograph")],
           "sculpture": [t for t in recs if t["type"] == "Sculpture"],
           "wares": [t for t in recs if T2G[t["type"]] == "metal, ceramic and glass wares"]}

    def yn(tid, pool, pairs, ga, card, n=N, field="creation_date_earliest", state_fn=st, **fmt):
        qa, qb = K.pair_fns(pairs, tid, key, **fmt)
        B.yn(tid, pool, key, state_fn, qa, qb, ga, lambda t: not ga(t), card, n, field)

    # 1. begun before T
    for T in (500, 1000, 1300, 1500, 1700, 1800, 1900):
        card = K.yn_card(f"the first year of the Date range is earlier than {T}.", f"the first year of the Date range is {T} or later.") if T in (1300, 1700) else None
        yn(f"begun.all.{T}", grp["all"], [("Was this work begun before the year {T}?", "Was this work begun in the year {T} or later?"),
                                          ("Does the work's date range start before {T}?", "Does the work's date range start in {T} or later?")],
           lambda t, T=T: t["e0"] < T, card, T=T)
    for g in ("paintings", "works on paper", "sculpture", "wares"):
        for T in (1500, 1800, 1900):
            yn(f"begun.{g}.{T}", grp[g], [("Was this work begun before the year {T}?", "Was this work begun in the year {T} or later?")],
               lambda t, T=T: t["e0"] < T, None, T=T)
    # 2. span
    for S in (10, 25, 50, 100):
        yn(f"span.{S}", recs, [("Does the date range cover more than {S} years?", "Does the date range cover {S} years or fewer?"),
                               ("Is the gap between the first and last year above {S} years?", "Is the gap between the first and last year {S} years or less?")],
           lambda t, S=S: t["e1"] - t["e0"] > S,
           K.yn_card(f"the last year minus the first year of the Date range is more than {S}.", f"the last year minus the first year of the Date range is {S} or less."), field="creation_date_latest", S=S)
    for tag, pool in (("all", recs), ("paintings", grp["paintings"])):
        cent = lambda y: (y - 1) // 100 + 1
        yn(f"onecentury.{tag}", pool, [("Does the whole date range fall inside one century?", "Does the date range reach into two or more centuries?")],
           lambda t: cent(t["e0"]) == cent(t["e1"]),
           K.yn_card("the first and last year of the Date range lie in the same century (years 1 to 100 are the 1st century, 1801 to 1900 the 19th).", "the first and last year lie in different centuries."), field="creation_date")
    # 3. accession year
    for Y in (1930, 1960, 1990):
        yn(f"accyear.{Y}", [t for t in recs if t["accy"]], [("Was the object accessioned in {Y} or later?", "Was the object accessioned before {Y}?"),
                                                           ("Does the accession number start with a year of {Y} or later?", "Does the accession number start with a year before {Y}?")],
           lambda t, Y=Y: t["accy"] >= Y, K.yn_card(f"the four-digit year at the start of the accession number is {Y} or later.", f"that year is earlier than {Y}."),
           field="accession_number", Y=Y)
    # 4. credit line first word
    for w, nm in (("Gift", "a gift"), ("Bequest", "a bequest"), ("Purchase", "a purchase")):
        yn(f"credit.{w.lower()}", recs, [("Is the credit line of this kind: {nm}?", "Is the credit line of a kind that differs from {nm}?")],
           lambda t, w=w: t["credit"].startswith(w), K.yn_card(f"the first word of the credit line is {w}.", f"the first word of the credit line is a different word."),
           field="creditline", nm=nm)
    # 5. height
    hp = [t for t in recs if t["h"]]
    for H in (10, 30, 60, 100):
        yn(f"height.{H}", hp, [("Is the unframed height above {H} cm?", "Is the unframed height {H} cm or less?")],
           lambda t, H=H: t["h"] > H, K.yn_card(f"the first number of the unframed size (height) is greater than {H} cm.", f"the first number of the unframed size is {H} cm or less."),
           field="measurements.unframed.height", H=H)
    yn("wider", [t for t in hp if t["h"] != t["w"]], [("Is the unframed width larger than the height?", "Is the unframed height larger than the width?")],
       lambda t: t["w"] > t["h"], K.yn_card("the second unframed number (width) is larger than the first (height).", "the first unframed number (height) is larger than the second."), field="measurements")
    # 6. medium keywords
    for kw in ("oil", "ink", "bronze", "porcelain"):
        yn(f"tech.{kw}", recs, [("Does the technique text mention {kw}?", "Is {kw} missing from the technique text?")],
           lambda t, kw=kw: kw in t["tech"].lower(), K.yn_card(f"the Technique line contains the letters '{kw}' in any case.", f"the Technique line has no '{kw}'."),
           field="technique", kw=kw)
    # 7. title
    sT = state(True)
    for k in (2, 4, 6):
        yn(f"titlelen.{k}", [t for t in recs if t["title"]], [("Does the title have more than {k} words?", "Does the title have {k} words or fewer?")],
           lambda t, k=k: len(t["title"].split()) > k, None, state_fn=sT, field="title", k=k)
    for w in ("Portrait", "Landscape"):
        yn(f"title.{w.lower()}", [t for t in recs if t["title"]], [("Does the title contain the word {w}?", "Is the word {w} absent from the title?")],
           lambda t, w=w: w.lower() in re.findall(r"[a-z]+", t["title"].lower()), None, state_fn=sT, field="title", w=w)
    yn("circa", [t for t in recs if t["dtext"]], [("Does the date text start with the letter c and a full stop, marking an approximate date?", "Is the date text an exact date, with the c. mark missing?")],
       lambda t: t["dtext"].lower().startswith("c."), K.yn_card("the Date text begins with 'c.' (circa).", "the Date text does not begin with 'c.'."), field="creation_date")
    yn("hasculture", recs, [("Does the record list a culture?", "Is the culture left unlisted?")], lambda t: bool(t["culture"]),
       None, field="culture")
    # 8. choices
    B.choice("era.first", recs, key, st, lambda t: ["In which era does the work's first year fall?", "Which era band holds the first year of the date range?"][K.hx(K.SEED, "q", t["id"]) % 2],
             ["before 1000", "1000 to 1499", "1500 to 1799", "1800 to 1899", "1900 or later"], lambda t: era(t["e0"]), None, 20, "creation_date_earliest")
    B.choice("era.last", recs, key, st, "Which era band holds the last year of the date range?",
             ["before 1000", "1000 to 1499", "1500 to 1799", "1800 to 1899", "1900 or later"], lambda t: era(t["e1"]), None, 20, "creation_date_latest")
    tgcard = K.choice_card({g: "object types " + ", ".join(ts) for g, ts in TYPE_GROUP.items()})
    B.choice("typegroup", recs, key, st, "Which group does the object type belong to?", list(TYPE_GROUP), lambda t: T2G[t["type"]], tgcard, 20, "type")
    B.choice("typegroup.paper", [t for t in recs if T2G[t["type"]] in ("works on paper and books", "paintings", "sculpture and carving")], key, st,
             "Into which group does the object type fall?", ["paintings", "works on paper and books", "sculpture and carving"], lambda t: T2G[t["type"]], tgcard, 18, "type")
    mcard = K.choice_card({"oil paint": "the Technique text contains 'oil' (checked first)", "ink, watercolor or tempera": "else it contains ink, watercolor, gouache, tempera or wash",
                           "metal": "else it contains bronze, gold, silver, iron, copper, brass, steel, pewter or gilt", "stone": "else it contains marble, limestone, granite, sandstone, alabaster, stone, jade or basalt",
                           "ceramic or glass": "else it contains porcelain, earthenware, stoneware, ceramic, glaze, clay, terracotta, glass or faience", "textile": "else it contains silk, wool, linen, cotton, embroider, velvet or tapestry",
                           "other": "none of the words above appear"})
    mopts = [m for m, _ in MEDIUM] + ["other"]
    B.choice("medium", recs, key, st, "Which medium class does the technique text fall into?", mopts, medium_class, mcard, 24, "technique")
    B.choice("medium.paper", grp["works on paper"] + grp["paintings"], key, st, "Which medium class does the technique text fall into?", mopts, medium_class, mcard, 20, "technique")
    cr = {"Gift": "the first word of the credit line is Gift", "Bequest": "the first word is Bequest", "Purchase": "the first word is Purchase", "other": "any other first word"}
    B.choice("credit.kind", recs, key, st, "Which kind of acquisition does the credit line show?", list(cr), lambda t: t["credit"] if t["credit"] in ("Gift", "Bequest", "Purchase") else "other",
             K.choice_card(cr), 20, "creditline")
    sz = lambda h: "under 20 cm" if h < 20 else "20 to 59 cm" if h < 60 else "60 to 119 cm" if h < 120 else "120 cm or more"
    B.choice("size.height", hp, key, st, "Which size class holds the unframed height?", ["under 20 cm", "20 to 59 cm", "60 to 119 cm", "120 cm or more"], lambda t: sz(t["h"]), None, 20, "measurements")
    B.choice("size.width", hp, key, st, "Which size class holds the unframed width?", ["under 20 cm", "20 to 59 cm", "60 to 119 cm", "120 cm or more"], lambda t: sz(t["w"]), None, 20, "measurements")
    dec = lambda y: f"{y // 10 * 10}s"
    ap = [t for t in recs if t["accy"] and 1910 <= t["accy"] <= 2019]
    B.choice("accdecade", ap, key, st, "Which decade does the accession number year fall in?", [f"{d}s" for d in range(1910, 2020, 10)],
             lambda t: dec(t["accy"]), None, 20, "accession_number")
    deps = ["Medieval Art", "Prints", "Japanese Art", "Chinese Art", "Textiles", "Drawings", "Photography", "Greek and Roman Art"]
    dp = [t for t in recs if t["dept"] in deps]
    B.choice("dept.coll", dp, key, st, "Which curatorial department holds the work?", deps, lambda t: t["dept"], None, 24, "department")
    B.choice("dept.coll2", dp, key, st, "Which department of the museum looks after this object?", deps, lambda t: t["dept"], None, 24, "department")
    man = B.write("Cleveland Museum of Art Open Access API (CC0), first 15,000 records by id order, CC0-flagged only.")
    print(man["report"])


if __name__ == "__main__":
    main()
