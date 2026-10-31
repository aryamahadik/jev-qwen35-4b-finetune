"""Build golden rows for uscg_mariner (US Coast Guard merchant mariner credential exams: the National Maritime Center's
published sample examinations, deck and engineering, with answer keys).

Source : official NMC sample-examination PDFs (www.dco.uscg.mil/Portals/9/NMC/pdfs/examinations/q###_*.pdf), the
         latest capture of each exam file; 192 pinned in uscg_mariner_files.json (url, Wayback capture, sha256; made
         by fetch_uscg_mariner.py; the official host refuses non-browser clients, so the byte-exact official files
         come from the Internet Archive's raw captures of those URLs). Six large engineering captures that the archive
         cut at 5 MiB are skipped. Exams that need charts, almanacs, tide/stability tables or plotting (nav problems,
         chart and river-plot exams) were not fetched. NMC re-issues each sample exam with a fresh draw from its
         bank, so earlier distinct captures (since 2024-06-01, pinned in uscg_mariner_extra_files.json, made by
         fetch_uscg_mariner.py --extra) add further official questions; they are read after the latest versions, so a
         question kept from them is one the latest versions do not contain. Each question: number, question, choices
         A-D, 'Correct answer: X'. A file whose parsed question count differs from its answer-key count is skipped
         whole. A published sample exam has no splits -> train.
Licence: US Government work (US Coast Guard, National Maritime Center), public domain (17 U.S.C. 105); USCG website
         policy https://www.uscg.mil/privacypolicy/ (archived 2019-08-21): 'Information presented on this web site in
         the non-logged in domain is considered public information and may be distributed or copied.'
Texts  : questions, choices and keys written by the USCG exam staff for real licensing exams (Rules of the Road,
         deck general/safety, navigation general, lifeboatman, tankship, OIM, and engineering: general subjects,
         steam/motor/gas-turbine plants, electrical, safety and environmental protection, QMED ratings).
Parse  : pdftotext -layout (poppler 26.04.0); repeated page header/footer lines (seen on >= half the pages) removed;
         a question is kept only if it has exactly four choices A-D and a key.
Drops  : questions that need an illustration, diagram, table, chart or curve; questions that need reference material
         (almanac, tide tables, Light List, Coast Pilot, stability/loading manuals, the DEEP/COASTAL DRILLER manuals);
         choices that refer to other choices by letter ('A and B'); rows with duplicate choices; the same question
         and choices with different keys in two exams (both dropped). The same question repeated across exams is
         used once (exact stem, then word 3-gram Jaccard >= 0.9 of the stem, first exam code kept). Decontamination
         vs forbidden label-NLI, local train/dev/eval files, round-1 golden parts and JevBench public.
Rows   : state = credential + exam name + the question (with its 'INLAND ONLY' / 'BOTH INTERNATIONAL & INLAND'
         scope); options = the four choices (original order); gold = the keyed choice; per-row definitions
         (defs/uscg_mariner__<qid>.json) with the rule for exception (NOT/EXCEPT), fill-in-the-blank and 'All/None of
         the above' choices.
Edge   : negation (not / except / never ... in the question), quantifier ('All/None of the above' among the choices),
         units, numeric.
Deterministic (seed 20261205).
"""
import collections
import json
import random
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAMILY, HERE, MAX_OPT_WORDS, UNITS, append_manifest, clean, decon, has_negation, is_all, is_none,  # noqa: E402
                     letter_refs, near_dup_filter, norm, option_defs, qid_of, sha256, show_samples, summary,
                     write_outputs)

KEY = "uscg_mariner"
SEED = 20261205
CACHE = HERE / "cache" / KEY
PINNED = HERE / "uscg_mariner_files.json"
EXTRA = HERE / "uscg_mariner_extra_files.json"  # earlier re-issues of the same exams (fetch_uscg_mariner.py --extra)
LICENCE = ("US Government work, public domain (17 U.S.C. 105; USCG National Maritime Center). USCG web policy "
           "https://www.uscg.mil/privacypolicy/ (Wayback 20190821195025): 'Information presented on this web site in "
           "the non-logged in domain is considered public information and may be distributed or copied.'")
INSTR = "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?"
QSTART = re.compile(r"^\s{0,4}(\d{1,3})\.\s+(\S.*)$")
OPT = re.compile(r"^\s*([A-D])\.\s+(\S.*)$")
ANS = re.compile(r"^\s*Correct answer:\s*([A-D])\s*$")
ILL = re.compile(r"(?i)illustration|diagram|\bshown\b|\bfigure\b|\bpictured\b|\bdrawing\b|\bsketch\b|\bgraph\b|"
                 r"\bchart\b|\btables?\b|\bcurves?\b|\bexhibit\b|\bpictograph|\bpicture\b|\bplate\b")
REF = re.compile(r"(?i)\b(use|using|refer to|see|according to|consult)\b[^.?]{0,60}\b(almanac|tide tables?|tidal current|"
                 r"light list|coast pilot|bowditch|pub\.? ?\d|sight reduction|stability|data book|reference book|"
                 r"loading manual|manual|trim and stability|hydrostatic|capacity plan|operating manual|extract)|"
                 r"\bDRILLER\b|GRAND HAVEN|reference material|\bextract\b")


def pdf_text(path):
    return subprocess.run(["pdftotext", "-layout", "-enc", "UTF-8", str(path), "-"], capture_output=True,
                          check=True).stdout.decode("utf8")


def parse_exam(path):
    t = pdf_text(path)
    pages = t.split("\f")
    freq = collections.Counter()
    for pg in pages:
        for l in {x.strip() for x in pg.splitlines() if x.strip()}:
            freq[l] += 1
    npg = len([pg for pg in pages if pg.strip()])
    hdr = {l for l, c in freq.items() if c >= max(2, npg * 0.5) and not (ANS.match(l) or OPT.match(l) or QSTART.match(l))}
    head = [x.strip() for x in pages[0].splitlines() if x.strip()]
    endorse = head[head.index("U.S.C.G. Merchant Marine Exam") + 1] if "U.S.C.G. Merchant Marine Exam" in head else ""
    title = next((x for x in head if re.match(r"^Q\d{3}\b", x)), "")
    title = re.sub(r"^Q\d{3}\s*", "", title).strip()
    lines = []
    for pg in pages:
        for l in pg.splitlines():
            s = l.strip()
            if not s or s in hdr or re.match(r"^(\d{1,2}/\d{1,2}/\d{4}\s+)?Page \d+ of \d+$", s):
                continue
            lines.append(l.rstrip())
    qs, cur, expect = [], None, 1
    for l in lines:
        m = ANS.match(l)
        if m and cur:
            cur["key"] = m.group(1)
            qs.append(cur)
            cur = None
            continue
        m = QSTART.match(l)
        if m and int(m.group(1)) == expect and cur is None:
            cur = {"n": expect, "stem": [m.group(2).strip()], "opts": {}}
            expect += 1
            continue
        if cur is None:
            continue
        m = OPT.match(l)
        if m and m.group(1) not in cur["opts"] and len(cur["opts"]) == ord(m.group(1)) - 65:
            cur["opts"][m.group(1)] = [m.group(2).strip()]
        elif cur["opts"]:
            cur["opts"][list(cur["opts"])[-1]].append(l.strip())
        else:
            cur["stem"].append(l.strip())
    n_keys = len(re.findall(r"Correct answer:", t))
    out = [{"n": q["n"], "stem": clean(" ".join(q["stem"])), "key": q["key"],
            "options": [clean(" ".join(q["opts"][k])) for k in sorted(q["opts"])]} for q in qs]
    return endorse, title, out, n_keys


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
    pin = json.loads(PINNED.read_text())
    extra = json.loads(EXTRA.read_text()) if EXTRA.exists() else []
    files = [(code, dict(rec, path=CACHE / rec["file"], tag=code)) for code, rec in sorted(pin.items())]
    files += [(rec["code"], dict(rec, path=CACHE / "extra" / rec["file"], tag=f"{rec['code']}_{rec['wayback']}"))
              for rec in sorted(extra, key=lambda r: (r["code"], r["wayback"]), reverse=True)]
    stats = collections.Counter()
    cands = []
    for code, rec in files:
        p = rec["path"]
        if rec.get("missing") or rec.get("truncated"):
            stats["truncated_or_missing_files"] += 1
            continue
        if sha256(p) != rec["sha256"]:
            sys.exit(f"sha256 mismatch {p}")
        try:
            endorse, title, qs, n_keys = parse_exam(p)
        except subprocess.CalledProcessError:
            stats["unreadable_files"] += 1
            continue
        if len(qs) != n_keys or not qs:  # a layout this parser does not follow exactly: skip the whole file
            stats["files_layout_mismatch"] += 1
            continue
        stats["files_used"] += 1
        stats["parsed"] += len(qs)
        for q in qs:
            text = q["stem"] + " " + " ".join(q["options"])
            if len(q["options"]) != 4 or not all(q["options"]) or len(q["stem"]) < 15:
                stats["malformed"] += 1
            elif ILL.search(text):
                stats["needs_illustration_or_table"] += 1
            elif REF.search(q["stem"]):
                stats["needs_reference_material"] += 1
            elif any(letter_refs(o, 4) for o in q["options"]):
                stats["letter_combination_choice"] += 1
            elif max(len(o.split()) for o in q["options"]) > MAX_OPT_WORDS:
                stats["choice_over_40_words"] += 1
            elif len({norm(o) for o in q["options"]}) < 4:
                stats["duplicate_choices"] += 1
            else:
                cands.append({"rid": f"uscg_{rec['tag']}_{q['n']:03d}", "code": code, "file": rec["file"],
                              "wayback": rec["wayback"], "sha": rec["sha256"], "url": rec["url"], "endorse": endorse, "title": title,
                              "stem": q["stem"], "options": q["options"], "key": q["key"],
                              "gold": q["options"]["ABCD".index(q["key"])]})
    # same question + choices keyed differently in two exams -> drop all copies
    keyed = collections.defaultdict(set)
    for c in cands:
        keyed[(norm(c["stem"]), tuple(sorted(norm(o) for o in c["options"])))].add(norm(c["gold"]))
    bad = {k for k, v in keyed.items() if len(v) > 1}
    n0 = len(cands)
    cands = [c for c in cands if (norm(c["stem"]), tuple(sorted(norm(o) for o in c["options"]))) not in bad]
    stats["conflicting_keys"] = n0 - len(cands)
    print(f"exams: {dict(stats)}; candidates={len(cands)}")
    cands = near_dup_filter(cands, lambda c: c["stem"], thresh=0.9, strip_numbers=False)
    print(f"after cross-exam dedupe (exact + near-duplicate stems): {len(cands)}")
    hits = decon({c["rid"]: [c["stem"]] for c in cands})
    cands = [c for c in cands if c["rid"] not in hits]
    print(f"after decon: {len(cands)}")

    rows, defs = [], {}
    for c in cands:
        q = qid_of(c["rid"])
        defs[q] = option_defs(c["stem"], c["options"], kind="exam")
        state = (f"U.S. Coast Guard merchant mariner credential exam ({c['endorse']}), {c['title']}.\n\n"
                 f"Question: {c['stem']}")
        rows.append({
            "key": KEY, "rid": c["rid"], "state": state, "instructions": INSTR, "options": c["options"],
            "gold": c["gold"], "soft": None,
            "meta": {"dataset": "USCG National Maritime Center sample examinations (merchant mariner credentials)",
                     "config": f"{c['file']} (capture {c['wayback']}); question {c['rid'].rsplit('_', 1)[1]}; 4-way answer choice",
                     "revision": f"{c['url']} @ web.archive.org/web/"
                                 f"{c['wayback']}id_; sha256:{c['sha']}",
                     "licence": LICENCE, "split": "train", "orig_label": {"key": c["key"]}, "family": FAMILY,
                     "edge": edge_of(c["stem"], c["options"]), "defs": q, "seed": SEED}})
    random.Random(SEED).shuffle(rows)
    write_outputs(KEY, rows, defs)
    s = summary(KEY, rows)
    show_samples(rows, defs, n=5, seed=3)
    mix = collections.Counter("engineering" if r["rid"][6] in "5678" else "deck" for r in rows)
    mix["from_earlier_versions"] = sum(r["rid"].count("_") == 3 for r in rows)
    append_manifest({
        "key": KEY, "family": FAMILY,
        "dataset": (f"USCG National Maritime Center merchant mariner sample examinations ({stats['files_used']} exam "
                    "PDFs: the latest issue of each deck/engineering exam + earlier re-issues since 2024-06)"),
        "licence": LICENCE, "rows": len(rows), "qtype": "choice (4 answer choices; per-row option definitions)",
        "yesno_share": 0.0, "edge_tags": sorted(k for k in s["edges"] if k),
        "notes": ("real licensing-exam questions keyed by the USCG (Rules of the Road incl. INLAND/INTERNATIONAL "
                  "scope, deck safety, navigation, cargo, lifeboat, tankship, OIM, marine engineering and QMED); "
                  "questions needing illustrations, tables, charts or reference books dropped; conflicting keys "
                  "dropped; each question used once across exams; "
                  f"mix {dict(mix)}; gold position {dict(sorted(s['pos'].items()))}.")})


if __name__ == "__main__":
    main()
