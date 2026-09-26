"""OHS-1 part "arxiv2026" (track F): arXiv primary-category classification on a
fresh corpus (papers first submitted 2026-08-01 .. 2026-09-20, i.e. after
Qwen3.5's 16 Feb 2026 release).

Source: arXiv API (export.arxiv.org/api/query), metadata is CC0. Only papers
whose category list contains exactly ONE category (no cross-lists) are used, so
the gold label is unambiguous: that single category.

Four archive groups, each with 8-15 official subject classes, all used as
options (official names from https://arxiv.org/category_taxonomy, card = the
official descriptions from the same page):
  q-bio      Quantitative Biology                             10 options
  cond-mat   Condensed Matter                                  9 options
  econ+q-fin Economics + Quantitative Finance                 11 options
             (q-fin.EC is officially "an alias for econ.GN"; the API files
              such papers under econ.GN, so q-fin.EC is folded into econ.GN
              and not offered as a separate option)
  physics    Physics-group archives that have no subject
             classes: gr-qc, hep-ex, hep-lat, hep-ph, hep-th,
             math-ph, nucl-ex, nucl-th, quant-ph               9 options
cs.* (40) and math.* (32) exceed the 8-15 limit, stat.* (6) and astro-ph.* (6)
fall below it, so they are not used.

60 papers per group (240 rows), balanced over subject classes by water-filling
(classes with few single-category papers give their share to the others).
Seed 20260927. Re-runnable: raw API pages are cached in ohs/cache/arxiv/.

Output: data/ohs_parts/arxiv2026.jsonl
"""
import os, re, sys, json, html, random, unicodedata
from collections import Counter, OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import arxiv_fetch as af  # noqa: E402
import requests  # noqa: E402

LEAN = os.path.dirname(HERE)
OUT_DIR = os.path.join(LEAN, "data", "ohs_parts")
OUT = os.path.join(OUT_DIR, "arxiv2026.jsonl")
TAXO_URL = "https://arxiv.org/category_taxonomy"
TAXO_CACHE = os.path.join(HERE, "cache", "category_taxonomy.html")

PART = "arxiv2026"
SEED = 20260927
DATE_FROM, DATE_TO = "20260801", "20260920"
PER_GROUP = 60
MIN_LEN, MAX_LEN = 20, 6000
QUESTION = "Which arXiv category is the primary subject of this paper?"
LICENSE = "CC0 1.0 (arXiv metadata: https://info.arxiv.org/help/api/tou.html)"

# group key -> (source short name, human name, option category ids in taxonomy order)
GROUPS = OrderedDict([
    ("q-bio", ("arxiv2026_qbio", "Quantitative Biology (q-bio.*)",
               ["q-bio.BM", "q-bio.CB", "q-bio.GN", "q-bio.MN", "q-bio.NC",
                "q-bio.OT", "q-bio.PE", "q-bio.QM", "q-bio.SC", "q-bio.TO"])),
    ("cond-mat", ("arxiv2026_condmat", "Condensed Matter (cond-mat.*)",
                  ["cond-mat.dis-nn", "cond-mat.mes-hall", "cond-mat.mtrl-sci",
                   "cond-mat.other", "cond-mat.quant-gas", "cond-mat.soft",
                   "cond-mat.stat-mech", "cond-mat.str-el", "cond-mat.supr-con"])),
    ("econ+q-fin", ("arxiv2026_econqfin", "Economics + Quantitative Finance (econ.*, q-fin.*)",
                    ["econ.EM", "econ.GN", "econ.TH",
                     "q-fin.CP", "q-fin.GN", "q-fin.MF", "q-fin.PM",
                     "q-fin.PR", "q-fin.RM", "q-fin.ST", "q-fin.TR"])),
    ("physics", ("arxiv2026_physics", "Physics-group archives without subject classes",
                 ["gr-qc", "hep-ex", "hep-lat", "hep-ph", "hep-th",
                  "math-ph", "nucl-ex", "nucl-th", "quant-ph"])),
])
PLACEHOLDER_DESC = {"description coming soon"}


def load_taxonomy():
    if not os.path.exists(TAXO_CACHE):
        os.makedirs(os.path.dirname(TAXO_CACHE), exist_ok=True)
        r = requests.get(TAXO_URL, timeout=60, headers={"User-Agent": af.UA})
        r.raise_for_status()
        open(TAXO_CACHE, "w", encoding="utf-8").write(r.text)
    t = open(TAXO_CACHE, encoding="utf-8").read()
    pat = re.compile(r'<h4>([a-zA-Z\-]+(?:\.[A-Za-z\-]+)?) <span>\((.*?)\)</span></h4>\s*</div>\s*'
                     r'<div class="column"><p>(.*?)</p>', re.S)
    taxo = {}
    for cid, name, desc in pat.findall(t):
        name = " ".join(html.unescape(name).split())
        desc = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", desc)).split())
        # the page repeats the archive name at the start of a few descriptions
        # (e.g. "General Relativity and Quantum Cosmology Areas of ...")
        if desc.startswith(name + " ") and len(desc) > len(name) + 20:
            desc = desc[len(name) + 1:]
        taxo[cid] = (name, desc)
    return taxo


def norm_text(s):
    s = unicodedata.normalize("NFKC", s).lower()
    return re.sub(r"[^0-9a-z]+", " ", s).strip()


def is_withdrawn(e):
    c = e["comment"].lower()
    a = e["abstract"].lower()
    return ("withdrawn" in c or a.startswith("this paper has been withdrawn")
            or a.startswith("withdrawn") or "this submission has been withdrawn" in a)


def in_window(e):
    d = e["published"][:10].replace("-", "")
    return DATE_FROM <= d <= DATE_TO


def allocate(avail, total, rng):
    """Water-filling: equal shares, capped by availability, leftovers redistributed."""
    alloc = {c: 0 for c in avail}
    remaining = total
    active = sorted(c for c in avail if avail[c] > 0)
    while remaining > 0 and active:
        share = remaining // len(active)
        if share == 0:
            for c in rng.sample(active, remaining):
                alloc[c] += 1
            remaining = 0
            break
        for c in active:
            give = min(share, avail[c] - alloc[c])
            alloc[c] += give
            remaining -= give
        active = [c for c in active if alloc[c] < avail[c]]
    return alloc


def main():
    taxo = load_taxonomy()
    rng = random.Random(SEED)
    seen_text = set()
    rows, summary = [], OrderedDict()
    n = 0
    for gkey, (source, gname, cats) in GROUPS.items():
        missing = [c for c in cats if c not in taxo]
        assert not missing, missing
        options = ["%s (%s)" % (taxo[c][0], c) for c in cats]
        opt_of = dict(zip(cats, options))
        card_lines, no_desc = [], []
        for c in cats:
            d = taxo[c][1]
            if d.lower() in PLACEHOLDER_DESC or not d:
                no_desc.append(c)  # official page has no description yet
                continue
            card_lines.append("- %s: %s" % (opt_of[c], d))
        card = "\n".join(card_lines)

        pools, drops = {}, Counter()
        for c in cats:
            total, entries = af.fetch_all(c, DATE_FROM, DATE_TO)
            pool = []
            for e in entries:
                if len(e["categories"]) != 1 or e["categories"][0] != c:
                    drops["cross_listed_or_other_primary"] += 1
                    continue
                if not in_window(e):
                    drops["outside_date_window"] += 1
                    continue
                if is_withdrawn(e):
                    drops["withdrawn"] += 1
                    continue
                state = "Title: %s\n\nAbstract: %s" % (e["title"], e["abstract"])
                if not (MIN_LEN <= len(state) <= MAX_LEN):
                    drops["length"] += 1
                    continue
                e = dict(e, state=state)
                pool.append(e)
            # dedupe on normalized text inside the pool (keep lowest arXiv id)
            pool.sort(key=lambda x: x["arxiv_id"])
            uniq, keys = [], set()
            for e in pool:
                k = norm_text(e["title"] + " " + e["abstract"])
                if k in keys or k in seen_text:
                    drops["duplicate_text"] += 1
                    continue
                keys.add(k)
                uniq.append(e)
            pools[c] = uniq

        avail = {c: len(pools[c]) for c in cats}
        alloc = allocate(avail, PER_GROUP, rng)
        picked = []
        for c in cats:
            chosen = rng.sample(pools[c], alloc[c]) if alloc[c] else []
            picked.extend((c, e) for e in chosen)
        rng.shuffle(picked)

        for c, e in picked:
            k = norm_text(e["title"] + " " + e["abstract"])
            assert k not in seen_text
            seen_text.add(k)
            n += 1
            row = {
                "id": "r_ohs_%s_%d" % (PART, n),
                "group_id": "g:ohs:%s:%s" % (PART, e["arxiv_id"]),
                "call_id": "c_ohs_%s_%d" % (PART, n),
                "split": "ohs",
                "track": "F",
                "source": source,
                "state": e["state"],
                "qtype": "choice",
                "instructions": QUESTION,
                "options": options,
                "gold": opt_of[c],
                "role": "choice",
                "card": card,
                "meta": {
                    "license": LICENSE,
                    "hf_id": None,
                    "data_source": "arXiv API (export.arxiv.org/api/query)",
                    "split_used": "arXiv API: submittedDate %s-%s, single-category papers only"
                                  % (DATE_FROM, DATE_TO),
                    "source_id": "arXiv:%s" % e["arxiv_id"],
                    "arxiv_id": e["arxiv_id"],
                    "arxiv_version": e["version"],
                    "submitted": e["published"],
                    "last_updated": e["updated"],
                    "category": c,
                    "archive_group": gkey,
                    "abs_url": "https://arxiv.org/abs/%s" % e["arxiv_id"],
                    "card_missing_official_description": no_desc,
                },
            }
            rows.append(row)

        bal = Counter(c for c, _ in picked)
        summary[gkey] = {
            "source": source,
            "group_name": gname,
            "n_items": len(picked),
            "n_options": len(options),
            "available_single_category_papers": avail,
            "class_balance": {c: bal.get(c, 0) for c in cats},
            "max_class_share": round(max(bal.values()) / len(picked), 3) if picked else None,
            "dropped": dict(drops),
            "card_missing_official_description": no_desc,
        }

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(json.dumps({"out": OUT, "n_rows": len(rows), "tasks": summary}, indent=1))


if __name__ == "__main__":
    main()
