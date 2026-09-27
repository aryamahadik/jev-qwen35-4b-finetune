"""Build raw rows for MAMS-ACSA (aspect-category DETECTION only, restaurant review sentences).

Source: GitHub siat-nlp/MAMS-for-ABSA @ cddcdb0f423b3fdb2c76b70744737abed3a00d17,
        data/MAMS-ACSA/raw/train.xml (TRAIN split only; val.xml / test.xml never touched).
Licence: Apache-2.0 (repo LICENSE file, full Apache License 2.0 text; saved in cache).
Texts: human-written restaurant reviews (Citysearch New York corpus, Ganu et al. 2009), sentence level.
Labels: human annotation by the MAMS authors (Jiang et al., EMNLP 2019), 8 predefined coarse categories.
Snapshot saved under breadth_src/cache/mams_acsa/ (train.xml, LICENSE, README.md).

Design (one row per source sentence; polarity is NOT used - it would duplicate NewsMTSC's taxonomy):
- "choice" rows (~half): sentences with exactly two annotated categories. The question names one of
  them ("Apart from <X>, which other aspect category ...?"); options = the other 7 categories; gold =
  the remaining annotated category (well-posed: exactly one other category is annotated).
  Round-robin over gold categories (least-filled first, cap 40%).
- "yesno" rows (~half): "Does the sentence discuss <category>?" over the 7 concrete categories
  (miscellaneous is a catch-all and is not asked in yes/no form). Balanced over (category, yes/no) cells.
- Lexical evidence filter (candidate filter only, never a label; lexicon follows MAMS's conventions):
  a "no" row, or a choice row whose distractors include a concrete category, is skipped when the sentence has
  evidence for that unannotated category (possible missed label); a positive (yes-row category, choice gold
  and named category, except miscellaneous) is kept only when the sentence has evidence for it (drops clear
  source label errors such as "The waiter kept pestering us for our order ..." tagged price).
- Text clean-up: leading Citysearch section headings "The Food" / "The Scene" / "The Setting" are stripped
  (they run into the sentence and hint the label); sentence-splitter fragments are dropped (unbalanced
  parentheses, or ending in a bare number that is often a cut decimal such as "... but 17.").
- Filters: 15-4000 chars; exact-duplicate sentences (normalised) dropped, all copies if their category
  sets disagree.
- Definitions (defs/mams_acsa.json) follow MAMS's observed conventions: a staff member doing the serving is staff
  (not service; "attentive" 26 staff vs 8 service, "checked" 11 vs 1 in train); portions, reservations and getting
  a table are miscellaneous; drinks and meals are food; the kitchen, bar and seating are place.
"""
import json, os, random, re, collections
import xml.etree.ElementTree as ET

SEED = 20261101
N_MAX = 450
CAP_FRAC = 0.40
CHOICE_FRAC = 0.5
REV = "cddcdb0f423b3fdb2c76b70744737abed3a00d17"
URL_BASE = "https://raw.githubusercontent.com/siat-nlp/MAMS-for-ABSA/" + REV + "/"
FILES = {"train.xml": "data/MAMS-ACSA/raw/train.xml", "LICENSE": "LICENSE", "README.md": "README.md"}

HERE = os.path.dirname(os.path.abspath(__file__))
LEAN = os.path.dirname(HERE)
CACHE = os.path.join(HERE, "cache", "mams_acsa")
RAW = os.path.join(CACHE, "train.xml")
OUT = os.path.join(LEAN, "data", "v13_parts", "raw", "mams_acsa.jsonl")

CATS = ["food", "menu", "staff", "service", "ambience", "place", "price", "miscellaneous"]
YN_CATS = [c for c in CATS if c != "miscellaneous"]
CAT_Q = {"food": "the food", "menu": "the menu", "staff": "the staff", "service": "the service",
         "ambience": "the ambience", "place": "the place (the venue, its location or seating)",
         "price": "the price", "miscellaneous": "a miscellaneous aspect"}
CAT_SHORT = {c: ("a miscellaneous aspect" if c == "miscellaneous" else "the " + c) for c in CATS}
# Lexical evidence per concrete category (a candidate FILTER only, never a label). Built from MAMS's own
# conventions (e.g. drinks count as food, the kitchen/bar/room as place, a DJ as staff, the tip/check as price).
# Used both ways: (a) a "no" row / choice distractor is skipped when the sentence has evidence for that
# unannotated category (possible missed label); (b) a positive (yes-row category, choice gold and the named
# category) is kept only when the sentence has evidence for it (MAMS has some clearly wrong positive labels,
# e.g. "The waiter kept pestering us for our order ..." tagged price).
TRIGGERS = {
    "food": r"\b(food|foods|dish|dishes|meals?|taste[sd]?|tasty|tasting|delicious|flavou?rs?|flavou?rful|appeti[sz]ers?|entrees?|entr\u00e9es?|desserts?|pizzas?|steaks?|sushi|sashimi|burgers?|pasta|salads?|fish|seafood|chicken|soups?|bread|brunch|breakfast|lunch|dinner|cooked|cooking|cuisine|fare|drinks?|drank|wines?|beers?|coffee|tea|cocktails?|martinis?|margaritas?|sake|sangria|mojitos?|water|soda|cokes?|cake|sauce|meat|ribs|toppings|fries|eggs|cheeses?|lobster|duck|lamb|pork|beef|oysters|noodles|rice|dumplings|tacos|sandwich(es)?|pies?|dim sum|tapas|eat|eats|ate|eating|ingredients|plates?|bottles?|glass(es)?|port|milk|juice|ravioli|scallops?|toast|hot dogs?)\b",
    "menu": r"\b(menus?|selections?|choices?|specials?|options|variety|wine list|list|offer|offers|offerings?|prix fixe|tasting menu|a la carte|items?)\b",
    "staff": r"\b(waiters?|waitor|waitors|waitress(es)?|waitstaff|wait staff|servers?|hostess(es)?|hosts?|staff|managers?|management|bartenders?|chefs?|owners?|busboys?|bus boys?|maitre|ma\u00eetre|cashiers?|clerk|clerck|attendant|employees?|dj|sommelier|personnel|crew|counter guy|musicians?|singers?)\b",
    "service": r"\b(service|serve[sd]?|serving|wait|waited|waiting|slow|slowly|fast|quick|quickly|prompt|promptly|reservations?|tables?|check|order|ordered|ordering|brought|bring|attention|attentive|ignored|rushed|forgot|delivery|delivered|seated|minutes|hours?|took)\b",
    "ambience": r"\b(ambien[cs]e|atmosphere|decor|d\u00e9cor|decorated|music|noisy|noise|loud|romantic|cozy|cosy|vibe|lighting|dim|moody|jazz|entertainment|art|feel|feels|scene|setting|intimate|comfortable|trendy|chic|charming|lounge|candles?|interior|walls?|crowd|crowded|mood)\b",
    "place": r"\b(place|location|neighbou?rhood|tables?|bar|bars|seating|seated|seats?|room|rooms|restaurant|area|space|counter|kitchen|booths?|terrace|garden|patio|bathrooms?|views?|floor|downstairs|upstairs|inside|outside|spot|joint|establishment|entrance|door|window|crowded|packed)\b",
    "price": r"(\$|\b(prices?|priced|pricey|cheap|cheaper|expensive|cost|costs|bill|check|tip|overpriced|value|dollars?|money|pay|paid|charged?|deal|afford|affordable|worth|fee|bucks|penny|reasonabl[ey])\b)",
}
HEADER_RE = re.compile(r"^The (Food|Scene|Setting)\s+(?=[A-Z\"'])")  # Citysearch section headings run into the sentence
META_BASE = {"dataset": "siat-nlp/MAMS-for-ABSA (MAMS-ACSA)", "config": "MAMS-ACSA/raw/train.xml",
             "revision": REV,
             "licence": "Apache-2.0 (github.com/siat-nlp/MAMS-for-ABSA LICENSE file at pinned revision)",
             "split": "train"}


def norm(s):
    return re.sub(r"\s+", " ", s.lower()).strip()


def load():
    if not os.path.exists(RAW):
        import urllib.request
        os.makedirs(CACHE, exist_ok=True)
        for name, path in FILES.items():
            urllib.request.urlretrieve(URL_BASE + path, os.path.join(CACHE, name))
    root = ET.parse(RAW).getroot()
    recs = []
    for i, s in enumerate(root.iter("sentence")):
        cats = [a.get("category") for a in s.iter("aspectCategory")]
        pols = {a.get("category"): a.get("polarity") for a in s.iter("aspectCategory")}
        recs.append({"rid": "train_%04d" % i, "text": HEADER_RE.sub("", s.findtext("text").strip()).strip(),
                     "cats": sorted(set(cats), key=CATS.index), "pols": pols})
    return recs


def triggered(text, cat):
    return re.search(TRIGGERS[cat], text, flags=re.I) is not None


def main():
    rng = random.Random(SEED)
    recs = load()
    drop = collections.Counter()
    by_text = collections.OrderedDict()
    for r in recs:
        if not (15 <= len(r["text"]) <= 4000):
            drop["length"] += 1; continue
        if any(c not in CATS for c in r["cats"]):
            drop["unknown_cat"] += 1; continue
        if r["text"].count("(") != r["text"].count(")"):  # sentence-splitter fragment (cut inside a parenthesis)
            drop["unbalanced_paren"] += 1; continue
        if re.search(r"(?<![\$:\d])\s\d+\.$", r["text"]):  # often cut at a decimal point ("... but 17.")
            drop["ends_bare_number"] += 1; continue
        if re.search(r"\bbar none\b", r["text"], flags=re.I):  # idiom mis-tagged as place (bar) in source
            drop["bar_none_idiom"] += 1; continue
        by_text.setdefault(norm(r["text"]), []).append(r)
    pool = []
    for k, rs in by_text.items():
        if len({tuple(r["cats"]) for r in rs}) > 1:
            drop["dup_conflict"] += len(rs); continue
        drop["dup_exact"] += len(rs) - 1
        pool.append(rs[0])
    rng.shuffle(pool)

    used = set()
    rows = []
    # ---- choice rows: exactly 2 categories, name one, ask the other
    n_choice = int(N_MAX * CHOICE_FRAC)
    cap_c = int(n_choice * CAP_FRAC)
    cand = collections.defaultdict(list)  # gold -> [(rec, named)]
    for r in pool:
        if len(r["cats"]) != 2:
            continue
        absent = [c for c in YN_CATS if c not in r["cats"]]
        if any(triggered(r["text"], c) for c in absent):
            continue
        if any(not triggered(r["text"], c) for c in r["cats"] if c != "miscellaneous"):
            drop["choice_no_pos_evidence"] += 1; continue
        a, b = r["cats"]
        cand[b].append((r, a)); cand[a].append((r, b))
    cnt = collections.Counter(); idx = collections.Counter(); exhausted = set()
    while sum(cnt.values()) < n_choice and len(exhausted) < len(CATS):
        g = min((c for c in CATS if c not in exhausted), key=lambda c: (cnt[c], CATS.index(c)))
        lst = cand[g]
        while idx[g] < len(lst) and lst[idx[g]][0]["rid"] in used:
            idx[g] += 1
        if idx[g] >= len(lst) or cnt[g] >= cap_c:
            exhausted.add(g); continue
        r, named = lst[idx[g]]; idx[g] += 1
        used.add(r["rid"]); cnt[g] += 1
        opts = [c for c in CATS if c != named]
        rows.append({"key": "mams_acsa", "rid": r["rid"], "state": r["text"],
                     "instructions": "Apart from %s, which other aspect category of the restaurant does this "
                                     "review sentence discuss?" % CAT_SHORT[named],
                     "options": opts, "gold": g, "soft": None,
                     "meta": dict(META_BASE, orig_label={"categories": r["cats"], "qtype": "choice",
                                                         "named": named})})
    # ---- yes/no rows: balanced over (category, answer) cells
    n_yn = N_MAX - len(rows)
    cells = [(c, a) for c in YN_CATS for a in ("yes", "no")]
    ycand = {cell: [] for cell in cells}
    for r in pool:
        for c in YN_CATS:
            if c in r["cats"]:
                if triggered(r["text"], c):
                    ycand[(c, "yes")].append(r)
            elif not triggered(r["text"], c):
                ycand[(c, "no")].append(r)
    ycnt = collections.Counter(); yidx = collections.Counter(); yex = set()
    while len(rows) < N_MAX and len(yex) < len(cells):
        # least-filled answer first, then least-filled cell within it
        ans_tot = {a: sum(ycnt[(c, a)] for c in YN_CATS) for a in ("yes", "no")}
        cell = min((x for x in cells if x not in yex),
                   key=lambda x: (ans_tot[x[1]], ycnt[x], cells.index(x)))
        lst = ycand[cell]
        while yidx[cell] < len(lst) and lst[yidx[cell]]["rid"] in used:
            yidx[cell] += 1
        if yidx[cell] >= len(lst):
            yex.add(cell); continue
        r = lst[yidx[cell]]; yidx[cell] += 1
        used.add(r["rid"]); ycnt[cell] += 1
        c, a = cell
        rows.append({"key": "mams_acsa", "rid": r["rid"], "state": r["text"],
                     "instructions": "Does this restaurant review sentence discuss %s?" % CAT_Q[c],
                     "options": ["yes", "no"], "gold": a, "soft": None,
                     "meta": dict(META_BASE, orig_label={"categories": r["cats"], "qtype": "yesno",
                                                         "asked": c})})
    rng.shuffle(rows)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    # ---- report
    print("source sentences:", len(recs), "pool after filters:", len(pool), "drops:", dict(drop))
    print("rows written:", len(rows), "->", OUT)
    qt = collections.Counter(r["meta"]["orig_label"]["qtype"] for r in rows)
    print("qtype:", dict(qt))
    print("choice gold:", dict(collections.Counter(r["gold"] for r in rows if r["options"] != ["yes", "no"])))
    print("yesno gold:", dict(collections.Counter(r["gold"] for r in rows if r["options"] == ["yes", "no"])))
    print("yesno cells:", {"%s/%s" % k: v for k, v in sorted(ycnt.items())})
    allg = collections.Counter(r["gold"] for r in rows)
    print("overall gold:", dict(allg), "max share: %.1f%%" % (100 * max(allg.values()) / len(rows)))
    print("soft coverage: %d/%d" % (sum(r["soft"] is not None for r in rows), len(rows)))
    L = sorted(len(r["state"]) for r in rows)
    print("length chars: min %d median %d mean %.0f max %d" % (L[0], L[len(L) // 2], sum(L) / len(L), L[-1]))
    assert len({r["rid"] for r in rows}) == len(rows)
    assert len({norm(r["state"]) for r in rows}) == len(rows)


if __name__ == "__main__":
    main()
