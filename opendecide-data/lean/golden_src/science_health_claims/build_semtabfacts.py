"""Build raw rows for semtabfacts_sci (SEM-TAB-FACTS, SemEval-2021 Task 9 sub-task A: statement verification against
tables from scientific articles; Wang, Mahajan, Danilevsky & Rosenthal, SemEval 2021, arXiv:2105.13995).

Source : official task site https://sites.google.com/view/sem-tab-facts , "Training data: Manual annotations"
         Google Drive file id 1yObzEEZJ8qM7ZjrMcbtKZ-jofpL820ft (v1.3.2), pinned by sha256. Only the MANUAL TRAINING
         set is used (v1.3.2/output/*.xml: tables + labelled statements). The auto-generated training set (template
         statements), the development set and the test sets are never downloaded.
Licence: CC BY 4.0 (task site, Data section: "By downloading the data or by accessing it any manner, you agree to
         abide by the CC BY-4.0 license"); the tables come from open-access Elsevier ScienceDirect articles published
         under CC BY 4.0 (paper sec. 3.1).
Texts  : tables (caption, cells, legend) from peer-reviewed scientific articles; statements written by Appen BPO
         crowd workers (aggregation, superlative, count, comparative, unique, 'all', caption/common-sense types) plus
         natural in-text sentences, all human-written.
Labels : entailed / refuted by the writer, then DOUBLY VERIFIED by a separate crowd verification task; only
         statements whose verified label matched were kept (paper sec. 3.2). The manual train set has no 'unknown'.
Question: "Is the statement supported by the table?"  entailed -> yes, refuted -> no.
State  : "Table caption: ...", the table as a pipe grid (row/column spans expanded so every cell sits under its
         header), optional "Table notes:" legend, then "Statement: ...". Tables whose rendering exceeds 6,000
         characters are skipped (no truncation, which could remove the evidence cell).
Review fix (strict reviewer, 29 Sep): the manual set also holds sentences copied from the ARTICLE TEXT around the
         table, all typed 'entailed' ("These results suggest ...", "... are summarised in Table 3", "Recently it was
         in the news that ..."), which the table alone cannot verify; a 35-row audit found ~1 in 9 yes labels wrong
         for this reason. Statements are now dropped (both labels) when they look like article prose (a Table/Figure/
         citation reference, first person, a discourse opener such as 'However,' / 'These results', or >= 30 words)
         or when fewer than half of their content words (crowd template words such as 'types', 'highest',
         'categories' excluded) occur in the caption, cells or notes.
Balance: all refuted statements kept; entailed statements sampled (seeded) so yes is ~60%.
Dedupe : exact/near-duplicate statements within a table dropped; decontamination (label-NLI incl. tabfact-like
         sets, local train/dev/eval, JevBench public) on statement and caption.
Key    : 'semtabfacts_sci' (not 'semtabfacts'): the fact_tables family has also cached this zip; the distinct key
         avoids overwriting each other's raw/defs files. If both parts exist at compile time, keep one of them.
Deterministic (seed 20261119). CPU only.
"""
import collections
import glob
import random
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _shc_common as C  # noqa: E402

KEY = "semtabfacts_sci"
SEED = 20261119
ZIP_URL = "https://drive.usercontent.google.com/download?id=1yObzEEZJ8qM7ZjrMcbtKZ-jofpL820ft&export=download&confirm=t"
ZIP_SHA = "f03598353de9b8463747d1e39e8b4e5c3ad154e6058cc1d2202826bfe5ba1bae"
LICENCE = ("CC BY 4.0 (official task site https://sites.google.com/view/sem-tab-facts, Data: 'By downloading the data "
           "or by accessing it any manner, you agree to abide by the CC BY-4.0 license'; tables from CC BY 4.0 "
           "open-access Elsevier articles)")
DATASET = "SEM-TAB-FACTS (SemEval-2021 Task 9), manual training set v1.3.2"
QUESTION = "Is the statement supported by the table?"
DEFS = {
    "yes": "Everything the statement says is true according to the table's cells, caption and notes, including any "
           "counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or "
           "paraphrased row and column names do not matter.",
    "no": "The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or "
          "'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or "
          "group.",
}
MAX_STATE = 6000
YES_TARGET = 0.60
# --- review fix: article-prose and grounding screens (see docstring)
PROSE_REF = re.compile(r"\b(?:Tables?|Tab\.|Figs?\.?|Figures?|Eqs?\.?|Equations?|Sections?|Supplementary|Appendix)\s*\(?\s*"
                       r"[0-9IVXS]|\(\s*(?:Tables?|Figs?\.?|Figures?|see)\b|\bet al\b|\(\s*[;,]?\s*\)|\(\s*;|"
                       r"\[\s*\d+(?:\s*[,–-]\s*\d+)*\s*\]")
PROSE_WE = re.compile(r"\b(?:we|our|us)\b", re.I)
PROSE_OPEN = re.compile(r"^(?:Thus|However|Therefore|Moreover|Furthermore|In addition|Additionally|Consequently|Hence|"
                        r"Interestingly|Notably|In contrast|Similarly|Although|Whereas|As expected|As shown|As can be seen|"
                        r"As a result|Finally|Overall,|In summary|In general|Taken together|Accordingly|Nevertheless|"
                        r"Nonetheless|On the other hand|In this study|In the present study|These results|This result|"
                        r"These findings|This finding|This suggests|This indicates|The results|Our)\b")
TEMPLATE = set("""the a an and of in to with was is were at for on but than as from by had has have did does which who that
or not it they be been are this these there their its each all any more most less least highest lowest high low value
values table tables different type types category categories column columns row rows number numbers total given
contains contain containing observed same unique every greater lesser compared compare comparison respectively
mentioned having count sum average mean list listed shows show showing presented entries entry data only both none
equal equals ranges range between whose maximum minimum max min lower higher larger smaller largest smallest biggest
bigger also under over into one two three four five six seven eight nine ten eleven twelve first second third last
other others another about above below his her them then when where while what can could will would should may might
must being no nor so such very much many few several some whereas case cases corresponding respective overall
specified shown present presents presenting describe describes described includes include including included consist
consists consisting""".split())


def prose_like(stmt):
    return bool(PROSE_REF.search(stmt) or PROSE_WE.search(stmt) or PROSE_OPEN.search(stmt) or len(stmt.split()) >= 30)


def grounding(stmt, head):
    """Share of the statement's content words (template words excluded) found in the caption/cells/notes."""
    hw = set(re.findall(r"[a-z]+", head.lower()))
    ws = [w for w in re.findall(r"[a-z]+", stmt.lower()) if len(w) >= 3 and w not in TEMPLATE]
    if len(ws) < 3:
        return 1.0

    def hit(w):
        return (w in hw or w.rstrip("s") in hw or w + "s" in hw or w.rstrip("es") in hw
                or any(len(w) >= 6 and h.startswith(w[:6]) for h in hw))
    return sum(hit(w) for w in ws) / len(ws)


def txt(s):
    return " ".join((s or "").split())


def render(table):
    rows = table.findall("row")
    cells = []
    nrows = ncols = 0
    for r in rows:
        for c in r.findall("cell"):
            rs, re_, cs, ce = (int(c.get(k)) for k in ("row-start", "row-end", "col-start", "col-end"))
            cells.append((rs, re_, cs, ce, txt(c.get("text"))))
            nrows, ncols = max(nrows, re_ + 1), max(ncols, ce + 1)
    if not cells or nrows > 80 or ncols > 20:
        return None
    grid = [["" for _ in range(ncols)] for _ in range(nrows)]
    for rs, re_, cs, ce, t in cells:
        for i in range(rs, re_ + 1):
            for j in range(cs, ce + 1):
                if not grid[i][j]:
                    grid[i][j] = t
    lines = ["| " + " | ".join(x.replace("|", "/") for x in row) + " |" for row in grid if any(row)]
    return "\n".join(lines)


def main():
    rng = random.Random(SEED)
    cache = C.CACHE / "semtabfacts"
    zpath = C.fetch(ZIP_URL, cache / "manual_train.zip", ZIP_SHA)
    out_dir = cache / "extracted"
    if not (out_dir / "v1.3.2" / "output").exists():
        with zipfile.ZipFile(zpath) as z:
            for n in z.namelist():
                if n.startswith("v1.3.2/output/") and n.endswith(".xml"):
                    z.extract(n, out_dir)
    stats = collections.Counter()
    recs = []
    for f in sorted(glob.glob(str(out_dir / "v1.3.2" / "output" / "*.xml"))):
        doc = Path(f).stem
        root = ET.parse(f).getroot()
        for t in root.findall("table"):
            tid = t.get("id")
            cap = txt(t.find("caption").get("text")) if t.find("caption") is not None else ""
            grid = render(t)
            if grid is None:
                stats["drop_table_shape"] += 1
                continue
            leg = t.find("legend")
            legend = txt(leg.get("text")) if leg is not None else ""
            head = (f"Table caption: {cap}\n" if cap else "") + grid + (f"\nTable notes: {legend}" if legend else "")
            seen = []
            for s in t.iter("statement"):
                st_text = txt(s.get("text"))
                typ = s.get("type")
                if typ not in ("entailed", "refuted") or len(st_text) < 8:
                    stats["drop_bad_statement"] += 1
                    continue
                if prose_like(st_text):
                    stats["drop_article_prose"] += 1
                    continue
                if grounding(st_text, head) < 0.5:
                    stats["drop_ungrounded"] += 1
                    continue
                ws = set(C.norm(st_text).split())
                if any(len(ws & o) / max(1, len(ws | o)) >= 0.9 for o in seen):
                    stats["drop_near_dup_statement"] += 1
                    continue
                seen.append(ws)
                state = f"{head}\n\nStatement: {st_text}"
                if len(state) > MAX_STATE:
                    stats["drop_too_long"] += 1
                    continue
                recs.append({"rid": f"{doc}|{tid}|{s.get('id')}", "state": state, "statement": st_text,
                             "caption": cap, "gold": "yes" if typ == "entailed" else "no", "type": typ,
                             "doc": doc, "table": tid})
    stats["cands"] = len(recs)
    core = {r["rid"]: [r["statement"]] + ([r["caption"]] if len(r["caption"].split()) >= 10 else []) for r in recs}
    hits = C.decon(core, cache_name=KEY)
    recs = [r for r in recs if r["rid"] not in hits]
    yes = [r for r in recs if r["gold"] == "yes"]
    no = [r for r in recs if r["gold"] == "no"]
    yes.sort(key=lambda r: r["rid"])
    rng.shuffle(yes)
    yes = yes[:int(len(no) * YES_TARGET / (1 - YES_TARGET))]
    rows = []
    for r in sorted(yes + no, key=lambda r: r["rid"]):
        e = C.edge(r["statement"], order=("double_negation", "negation", "quantifier"), default="table")
        rows.append({
            "key": KEY, "rid": r["rid"], "state": r["state"], "instructions": QUESTION, "options": C.YN,
            "gold": r["gold"], "soft": None,
            "meta": {"dataset": DATASET, "config": "manual training annotations, v1.3.2/output/*.xml",
                     "revision": f"gdrive:1yObzEEZJ8qM7ZjrMcbtKZ-jofpL820ft; sha256:{ZIP_SHA}", "licence": LICENCE,
                     "split": "train", "orig_label": {"type": r["type"], "document": r["doc"], "table": r["table"]},
                     "family": C.FAMILY, "edge": e},
        })
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, {None: DEFS})
    st = C.summary(KEY, rows)
    print("stats:", dict(stats), "| decon:", len(hits))
    print("tables:", len({(r['meta']['orig_label']['document'], r['meta']['orig_label']['table']) for r in rows}))
    C.show_samples(rows, n=5, seed=9)
    C.append_manifest(C.manifest_record(
        KEY, DATASET, LICENCE, rows, "yesno",
        "Crowd-written statements about tables from CC BY scientific articles, labels doubly verified; table rendered "
        "as a span-expanded pipe grid with caption and notes; yes ~60% after sampling entailed statements. NOTE: "
        "fact_tables has also cached this dataset; if it builds its own part, keep only one at compile. Article-prose "
        "statements (unverifiable from the table, all typed entailed) and ungrounded statements dropped.", st))


if __name__ == "__main__":
    main()
