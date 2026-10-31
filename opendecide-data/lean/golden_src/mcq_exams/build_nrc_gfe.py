"""Build golden rows for nrc_gfe (US Nuclear Regulatory Commission Generic Fundamentals Examination question banks:
the written fundamentals exam for nuclear reactor operator licences).

Source : the NRC GFE question banks, November 2020 edition, PWR (191 components, 192 reactor theory, 193
         thermodynamics) and BWR (291/292/293), pinned in nrc_gfe_files.json (official nrc.gov URL, Internet Archive raw
         capture, sha256; made by fetch_nrc_gfe.py because nrc.gov refuses non-browser clients). Each item: TOPIC
         (K/A catalogue number), KNOWLEDGE, QID (with the matching question id in the other bank), question, choices
         A-D, ANSWER. A question bank has no splits -> train.
Licence: US Government work, public domain (17 U.S.C. 105). NRC site disclaimer https://www.nrc.gov/site-help/
         disclaimer.html (Wayback 20230120195335): "NRC's website constitutes a U.S. Government Work under federal
         copyright law and as such, it is not subject to copyright. It is freely available for non-exclusive rights in
         publication or reproduction for any purpose, in any form, and there are no restrictions on use."
Texts  : questions and keys written by NRC examiners for real licensing exams (human-written, human keys).
Parse  : pdftotext -layout (poppler 26.04.0); page headers/footers dropped (footer topic names kept as the topic).
         Superscripts lost by text extraction are restored only where unambiguous: 'N x 10NN' -> 'N x 10^NN',
         '10-N percent/seconds' -> '10^-N ...', ft2/ft3/cm2/cm3 -> ft²/ft³/cm²/cm³.
Drops  : questions that need a figure, drawing, graph, curve, table or diagram ('Refer to the drawing ...'); items
         laid out as a table (multi-column choices such as '5,000   10,000' under column headers); items
         without exactly four choices; the same question in the PWR and BWR banks is used once (QID cross-reference,
         exact text, then word 3-gram Jaccard >= 0.9 of the question), and dropped if the two banks key it
         differently; decontamination vs forbidden label-NLI, local train/dev/eval files, round-1 golden parts and
         JevBench public.
Rows   : state = exam + plant type + topic + the question; options = the four choices (original order); gold = the
         keyed choice; per-row definitions (defs/nrc_gfe__<qid>.json), with the two-blank rule ('increase;
         decreased' fills the blanks in order).
Edge   : negation, quantifier ('All of the above' ...), units, numeric; multi_hop is not claimed.
Deterministic (seed 20261206).
"""
import collections
import json
import random
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAMILY, HERE, MAX_OPT_WORDS, UNITS, append_manifest, clean, decon, has_negation,  # noqa: E402
                     is_all, is_none, letter_refs, near_dup_filter, norm, option_defs, qid_of, sha256, show_samples,
                     summary, write_outputs)

KEY = "nrc_gfe"
SEED = 20261206
CACHE = HERE / "cache" / KEY
PINNED = HERE / "nrc_gfe_files.json"
LICENCE = ("US Government work, public domain (17 U.S.C. 105; US Nuclear Regulatory Commission). NRC site disclaimer "
           "https://www.nrc.gov/site-help/disclaimer.html (Wayback 20230120195335): \"NRC's website constitutes a U.S. "
           "Government Work under federal copyright law and as such, it is not subject to copyright. It is freely "
           "available ... for any purpose, in any form, and there are no restrictions on use.\"")
INSTR = "Which answer choice is correct for this NRC reactor operator licensing exam question?"
HDR = re.compile(r"^\s*(NRC Generic Fundamentals Examination Question Bank--(PWR|BWR)|(January|February|March|April|"
                 r"May|June|July|August|September|October|November|December) \d{4})\s*$")
FOOT = re.compile(r"^\s*-\d+-\s+(\S.*?)\s*$")
FIG = re.compile(r"(?i)refer to|figure|drawing|\bshown\b|\bgraph\b|\bcurves?\b|\btables?\b|mollier|diagram|sketch|"
                 r"\bplot\b|\bexhibit\b")


def pdf_text(path):
    return subprocess.run(["pdftotext", "-layout", "-enc", "UTF-8", str(path), "-"], capture_output=True,
                          check=True).stdout.decode("utf8")


def fix_sup(t):
    t = re.sub(r"(\d)\s*x\s*10(-?\d{1,2})\b", r"\1 x 10^\2", t)
    t = re.sub(r"\b10-(\d{1,2})(\s+(percent|seconds?|%))", r"10^-\1\2", t)
    t = re.sub(r"\b(ft|cm|in|m)([23])\b", lambda m: m.group(1) + {"2": "²", "3": "³"}[m.group(2)], t)
    return t


def parse_bank(path):
    qs, cur, names, pending = [], None, {}, []
    for l in pdf_text(path).replace("\f", "\n").splitlines():
        s = l.strip()
        m = FOOT.match(l)
        if m and not re.match(r"^[A-D]\.", s):
            for q in pending:  # footer names the topic of the questions on that page
                names.setdefault(q["topic"], m.group(1))
            pending = []
            continue
        if HDR.match(l):
            continue
        m = re.match(r"^TOPIC:\s*(\d+)", s)
        if m:
            cur = {"topic": m.group(1), "body": []}
            continue
        if cur is None:
            continue
        m = re.match(r"^KNOWLEDGE:\s*(.*)", s)
        if m:
            cur["ka"] = m.group(1)
            continue
        m = re.match(r"^QID:\s*(\S+)\s*(\((\S+)\))?", s)
        if m:
            cur["qid"], cur["xref"] = m.group(1), m.group(3)
            continue
        m = re.match(r"^ANSWER:\s*([A-D])\.?\s*$", s)
        if m:
            cur["key"] = m.group(1)
            qs.append(cur)
            pending.append(cur)
            cur = None
            continue
        if re.match(r"^[A-D]\.\s+\S.*\S\s{3,}\S", s):  # a column gap inside a choice: table-style choices
            cur["tabular"] = True
        cur["body"].append(s)
    out = []
    for q in qs:
        stem, opts, last = [], {}, None
        for s in q["body"]:
            m = re.match(r"^([A-D])\.\s+(.*)$", s)
            if m and m.group(1) not in opts and len(opts) == ord(m.group(1)) - 65:
                opts[m.group(1)], last = [m.group(2)], m.group(1)
            elif s:
                (opts[last] if opts else stem).append(s)
        out.append({"topic": q["topic"], "ka": q.get("ka"), "qid": q.get("qid"), "xref": q.get("xref"),
                    "tabular": q.get("tabular", False),
                    "key": q["key"], "stem": fix_sup(clean(" ".join(stem))),
                    "options": [fix_sup(clean(" ".join(opts[k]))) for k in sorted(opts)]})
    return out, names


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
    stats = collections.Counter()
    cands, keyed = [], collections.defaultdict(set)
    banks, names = {}, {}
    for name in sorted(pin):
        p = CACHE / name
        if sha256(p) != pin[name]["sha256"]:
            sys.exit(f"sha256 mismatch {p}")
        banks[name], nm = parse_bank(p)
        for t, v in nm.items():  # PWR 19xyyy and BWR 29xyyy share the K/A topic names
            names.setdefault(t[1:], v)
    for name in sorted(pin):
        plant = "PWR" if name.startswith("19") else "BWR"
        qs = banks[name]
        stats[f"{name}_parsed"] = len(qs)
        for q in qs:
            text = q["stem"] + " " + " ".join(q["options"])
            if len(q["options"]) != 4 or not all(q["options"]) or len(q["stem"]) < 15 or not q["qid"]:
                stats["malformed"] += 1
                continue
            if FIG.search(text):
                stats["needs_figure_or_table"] += 1
                continue
            if q["tabular"]:
                stats["table_style_choices"] += 1
                continue
            if any(letter_refs(o, 4) for o in q["options"]) or max(len(o.split()) for o in q["options"]) > MAX_OPT_WORDS:
                stats["letter_or_long_choice"] += 1
                continue
            if len({norm(o) for o in q["options"]}) < 4:
                stats["duplicate_choices"] += 1
                continue
            gold = q["options"]["ABCD".index(q["key"])]
            ids = {q["qid"]} | ({q["xref"]} if q["xref"] else set())
            keyed[(norm(q["stem"]), tuple(sorted(norm(o) for o in q["options"])))].add(norm(gold))
            cands.append({"rid": f"nrcgfe_{q['qid']}", "ids": ids, "plant": plant, "file": name,
                          "topic": q["topic"], "topic_name": names.get(q["topic"][1:], ""), "ka": q["ka"],
                          "stem": q["stem"], "options": q["options"], "key": q["key"], "gold": gold})
    n0 = len(cands)
    cands = [c for c in cands if len(keyed[(norm(c["stem"]), tuple(sorted(norm(o) for o in c["options"])))]) == 1]
    stats["conflicting_keys"] = n0 - len(cands)
    # the same question in both banks (QID cross-reference): keep the PWR copy (files sort 19x before 29x)
    seen_ids, uniq = set(), []
    for c in cands:
        if c["ids"] & seen_ids:
            stats["cross_bank_duplicate"] += 1
            continue
        seen_ids |= c["ids"]
        uniq.append(c)
    print(f"banks: {dict(stats)}; candidates={len(uniq)}")
    uniq = near_dup_filter(uniq, lambda c: c["stem"], thresh=0.9, strip_numbers=False)
    print(f"after near-duplicate stems: {len(uniq)}")
    hits = decon({c["rid"]: [c["stem"]] for c in uniq})
    uniq = [c for c in uniq if c["rid"] not in hits]
    print(f"after decon: {len(uniq)}")

    rows, defs = [], {}
    for c in uniq:
        q = qid_of(c["rid"])
        defs[q] = option_defs(c["stem"], c["options"], kind="exam")
        topic = f", topic: {c['topic_name']}" if c["topic_name"] else ""
        state = (f"US NRC reactor operator licensing exam (Generic Fundamentals Examination), {c['plant']} question "
                 f"bank{topic}.\n\nQuestion: {c['stem']}")
        rows.append({
            "key": KEY, "rid": c["rid"], "state": state, "instructions": INSTR, "options": c["options"],
            "gold": c["gold"], "soft": None,
            "meta": {"dataset": "US NRC Generic Fundamentals Examination question banks (November 2020)",
                     "config": f"{c['file']}; topic {c['topic']} {c['ka'] or ''}; QID {'/'.join(sorted(c['ids']))}",
                     "revision": f"{pin[c['file']]['url']} @ web.archive.org/web/{pin[c['file']]['wayback']}id_; "
                                 f"sha256:{pin[c['file']]['sha256']}",
                     "licence": LICENCE, "split": "train", "orig_label": {"key": c["key"]}, "family": FAMILY,
                     "edge": edge_of(c["stem"], c["options"]), "defs": q, "seed": SEED}})
    random.Random(SEED).shuffle(rows)
    write_outputs(KEY, rows, defs)
    s = summary(KEY, rows)
    show_samples(rows, defs, n=5, seed=8)
    mix = collections.Counter(r["meta"]["config"][:1] + "9x" for r in rows)
    append_manifest({
        "key": KEY, "family": FAMILY,
        "dataset": "US NRC Generic Fundamentals Examination question banks, Nov 2020 (PWR 191/192/193, BWR 291/292/293)",
        "licence": LICENCE, "rows": len(rows), "qtype": "choice (4 answer choices; per-row option definitions)",
        "yesno_share": 0.0, "edge_tags": sorted(k for k in s["edges"] if k),
        "notes": ("real reactor-operator licensing exam questions (components, reactor theory, thermodynamics) keyed "
                  "by the NRC; many are cause-effect and two-blank 'increase/decrease' decisions; figure/table "
                  "questions dropped; PWR/BWR duplicates used once; unambiguous lost superscripts restored; "
                  f"bank mix {dict(mix)}; gold position {dict(sorted(s['pos'].items()))}.")})


if __name__ == "__main__":
    main()
