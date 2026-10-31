"""Build golden rows for ncvec_ham (US FCC amateur radio licence exams: the official NCVEC question pools for the
Technician (Element 2), General (Element 3) and Amateur Extra (Element 4) examinations).

Source : the NCVEC Question Pool Committee's public releases (Word files, sha256 pinned):
         - 2026-2030 Technician Pool and Syllabus Public Release Feb 19 2026.docx
         - General Class Pool and Syllabus 2023-2027 Public Release with 6th Errata Feb 4 2026.docx
         - 2024-2028 Extra Class Question Pool and Syllabus Public Release with 4th Errata Feb 4 2026.docx
         Each question: id, answer key letter, (FCC rule citation), question, four choices A-D. A question pool has no
         splits (it is the whole bank from which exams are drawn) -> counts as train. The older 2022-2026 Technician
         pool is not used (its release page carries no public-domain statement).
Licence: public domain, stated by the pool owner on the official release pages (www.ncvec.org/index.php/...):
         'The NCVEC Question Pool Committee hereby releases into public domain the 2023-2027 General, Element 3,
         Question pool.'; '... hereby releases into public domain the 2024-2028 Element 4 Extra Class Question Pool.';
         'The NCVEC Question Pool Committee (QPC) hereby releases the 2026-2030 Technician Class (Element 2) Question
         Pool into the public domain.'
Texts  : questions and choices written by the volunteer QPC (human-written, human answer keys, reviewed by VECs and
         corrected through published errata; the files used include all errata; withdrawn questions are dropped).
Rows   : state = exam + subelement name + the question; options = the four choices (original order, superscripts and
         subscripts kept as Unicode, e.g. 'P = I² x R'); gold = the keyed choice. Per-row definitions
         (defs/ncvec_ham__<qid>.json) restate each choice and the rule for its type ('All these choices are correct',
         'None of these', exception questions).
Drops  : questions that need a figure or diagram (Figure T-1, G7-1, E5-1, ...); near-duplicate questions across the
         three pools (word 3-gram Jaccard >= 0.9 of question + choices); decontamination vs forbidden label-NLI, local
         train/dev/eval files, round-1 golden parts and JevBench public.
Edge   : negation (a negation cue in the question: not, never, except, ...), quantifier ('All these choices are correct' / 'None of these' among the
         choices), units, numeric.
Deterministic (seed 20261204).
"""
import collections
import html
import json
import random
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAMILY, HERE, UNITS, append_manifest, clean, decon, fetch, has_negation, is_all,  # noqa: E402
                     is_none, near_dup_filter, option_defs, qid_of, show_samples, summary, write_outputs)

KEY = "ncvec_ham"
SEED = 20261204
CACHE = HERE / "cache" / KEY
POOLS = {  # element -> (url, sha256, exam name, release page)
    "T": ("http://ncvec.org/downloads/2026-2030%20Technician%20Pool%20and%20Syllabus%20Public%20Release%20Feb%2019"
          "%202026.docx", "c3bb9ebf46730a9812ae854d12a93f07b7a38f521441e51c451e917ccb9e3a54",
          "Technician class (Element 2) question pool 2026-2030",
          "https://www.ncvec.org/index.php/2026-2030-technician-question-pool"),
    "G": ("http://ncvec.org/downloads/General%20Class%20Pool%20and%20Syllabus%202023-2027%20Public%20Release%20with"
          "%206th%20Errata%20Feb%204%202026.docx", "a07b15d6b9b7aef9e51dae3dd7d37b23de1d7bb410733b7ac6323eaac2f4b396",
          "General class (Element 3) question pool 2023-2027",
          "https://www.ncvec.org/index.php/2023-2027-general-question-pool-release"),
    "E": ("http://ncvec.org/downloads/2024-2028%20Extra%20Class%20Question%20Pool%20and%20Syllabus%20Public%20Release"
          "%20with%204th%20Errata%20Feb%204%202026.docx",
          "581ff3aa4c98bb2a6fcc303fe1ce19beb29bc7d3d02ff7fe5c6162c4c26ce4f7",
          "Amateur Extra class (Element 4) question pool 2024-2028",
          "https://www.ncvec.org/index.php/2024-2028-extra-class-question-pool-release"),
}
LICENCE = ("Public domain (NCVEC Question Pool Committee release pages: https://www.ncvec.org/index.php/2026-2030-"
           "technician-question-pool 'hereby releases the 2026-2030 Technician Class (Element 2) Question Pool into the "
           "public domain'; .../2023-2027-general-question-pool-release 'hereby releases into public domain the "
           "2023-2027 General, Element 3, Question pool'; .../2024-2028-extra-class-question-pool-release 'hereby "
           "releases into public domain the 2024-2028 Element 4 Extra Class Question Pool')")
INSTR = "Which answer choice is correct for this FCC amateur radio licence exam question?"
SUP = str.maketrans("0123456789+-=()n", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿ")
SUB = str.maketrans("0123456789+-=()", "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎")
ID = re.compile(r"^([TGE]\d[A-Z]\d\d)\s*\(([A-D])\)\s*(\[.*\])?\s*$")
FIG = re.compile(r"(?i)\bfigure\b|\bdiagram\b|\bschematic\b|\billustrat")


def paragraphs(path):
    x = zipfile.ZipFile(path).read("word/document.xml").decode("utf8")
    out = []
    for para in re.findall(r"<w:p[ >].*?</w:p>", x, flags=re.S):
        s = ""
        for run in re.findall(r"<w:r[ >].*?</w:r>", para, flags=re.S):
            t = html.unescape("".join(re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>", run)))
            if not t and "<w:tab/>" in run:
                t = " "
            va = re.search(r'<w:vertAlign w:val="(\w+)"', run)
            if va and t.strip():
                if va.group(1) == "superscript":
                    t = t.translate(SUP) if all(c in "0123456789+-=()n" for c in t) else "^(" + t + ")"
                elif va.group(1) == "subscript":
                    t = t.translate(SUB) if all(c in "0123456789+-=()" for c in t) else "_(" + t + ")"
            s += t
        out.append(clean(s))
    return out


def parse_pool(path):
    ps = paragraphs(path)
    deleted, subs = set(), {}
    for x in ps:
        m = re.match(r"^([TGE]\d[A-Z]\d\d)\s*[–-]+\s*(question deleted|removed from use|withdrawn)", x, re.I)
        if m:
            deleted.add(m.group(1))
        m = re.match(r"^SUBELEMENT ([TGE]\d)\s*[–-]\s*(.+?)\s*-?\s*\[", x)
        if m and m.group(1) not in subs:
            subs[m.group(1)] = m.group(2).strip(" -–").replace("’", "'")
    qs, i = {}, 0
    while i < len(ps):
        m = ID.match(ps[i])
        if not m:
            i += 1
            continue
        j, block = i + 1, []
        while j < len(ps) and ps[j] != "~~" and not ID.match(ps[j]):
            if ps[j]:
                block.append(ps[j])
            j += 1
        opts, stem = {}, []
        for b in block:
            mm = re.match(r"^([A-D])\.\s*(.*)$", b)
            if mm and mm.group(1) not in opts and len(opts) == ord(mm.group(1)) - 65:
                opts[mm.group(1)] = mm.group(2).strip()
            elif not opts:
                stem.append(b)
            else:
                opts[list(opts)[-1]] += " " + b
        if len(opts) == 4 and stem:  # errata headers without choices never qualify; the pool body comes last
            qs[m.group(1)] = {"id": m.group(1), "key": m.group(2), "cite": (m.group(3) or "").strip("[]"),
                              "stem": " ".join(stem), "options": [clean(opts[k]) for k in "ABCD"]}
        i = j
    return qs, deleted, subs


def edge_of(stem, options):
    if has_negation(stem):
        return "negation"
    if any(is_all(o) or is_none(o) for o in options):
        return "quantifier"
    text = stem + " " + " ".join(options)
    if UNITS.search(text):
        return "units"
    if re.search(r"\d", text):
        return "numeric"
    return None


def main():
    stats = collections.Counter()
    recs = []
    for el, (url, sha, exam, _page) in POOLS.items():
        p = fetch(url, CACHE / Path(url.replace("%20", " ")).name, sha)
        qs, deleted, subs = parse_pool(p)
        stats[f"{el}_parsed"] = len(qs)
        for qid, q in sorted(qs.items()):
            if qid in deleted:
                stats["withdrawn"] += 1
                continue
            if FIG.search(q["stem"]) or any(FIG.search(o) for o in q["options"]):
                stats["needs_figure"] += 1
                continue
            if len({o.lower() for o in q["options"]}) < 4 or not all(q["options"]):
                stats["bad_options"] += 1
                continue
            sub = subs.get(qid[:2], "").capitalize()
            state = f"FCC amateur radio licence exam: {exam}.\nSubelement: {sub}.\n\nQuestion: {q['stem']}"
            recs.append({"rid": f"ncvec_{qid}", "qid": qid, "state": state, "stem": q["stem"], "options": q["options"],
                         "gold": q["options"]["ABCD".index(q["key"])], "key": q["key"], "cite": q["cite"],
                         "exam": exam})
    print(f"parsed: {dict(stats)}; candidates={len(recs)}")
    recs = near_dup_filter(recs, lambda r: r["stem"] + " || " + " | ".join(r["options"]), thresh=0.9,
                           strip_numbers=False)
    print(f"after near-dup: {len(recs)}")
    hits = decon({r["rid"]: [r["stem"]] for r in recs})
    recs = [r for r in recs if r["rid"] not in hits]
    print(f"after decon: {len(recs)}")

    rows, defs = [], {}
    for r in recs:
        q = qid_of(r["rid"])
        defs[q] = option_defs(r["stem"], r["options"], kind="exam")
        rows.append({
            "key": KEY, "rid": r["rid"], "state": r["state"], "instructions": INSTR, "options": r["options"],
            "gold": r["gold"], "soft": None,
            "meta": {"dataset": "NCVEC amateur radio question pools (ncvec.org): " + r["exam"],
                     "config": "4-way answer choice; pool question " + r["qid"] + (f" (FCC rule {r['cite']})" if r["cite"] else ""),
                     "revision": "sha256:" + POOLS[r["qid"][0]][1], "licence": LICENCE, "split": "train",
                     "orig_label": {"id": r["qid"], "key": r["key"]}, "family": FAMILY,
                     "edge": edge_of(r["stem"], r["options"]), "defs": q, "seed": SEED}})
    random.Random(SEED).shuffle(rows)
    write_outputs(KEY, rows, defs)
    s = summary(KEY, rows)
    show_samples(rows, defs, n=5, seed=5)
    append_manifest({
        "key": KEY, "family": FAMILY,
        "dataset": "NCVEC FCC amateur radio question pools: Technician 2026-2030, General 2023-2027, Extra 2024-2028",
        "licence": LICENCE, "rows": len(rows), "qtype": "choice (4 answer choices; per-row option definitions)",
        "yesno_share": 0.0, "edge_tags": sorted(k for k in s["edges"] if k),
        "notes": ("official licence-exam question banks (rules, operating practice, electronics, RF safety) written "
                  "and keyed by the NCVEC Question Pool Committee, errata applied, withdrawn and figure questions "
                  "dropped; every usable question used once; 'All these choices are correct' / exception questions "
                  f"kept as edge cases; gold position {dict(sorted(s['pos'].items()))}.")})


if __name__ == "__main__":
    main()
