"""formats-2: real-text record pools for the spec 2.3 codebook variants (F10 S7, F11 S7).

Inputs (pinned upstream files, downloaded to tmp/raw/, deleted after the build; sha256 in the manifest):
  XED English      Helsinki-NLP/XED@76666d251f14  AnnotatedData/en-annotated.tsv, AnnotatedData/neu_en.txt
  MAMS ACSA/ATSA   siat-nlp/MAMS-for-ABSA@cddcdb0f423b  data/MAMS-ACSA/raw/train.xml, data/MAMS-ATSA/raw/train.xml
  GHC              OSF edua3  Data/ghc_train.tsv (ghc_test.tsv is never downloaded)
  EDOS             rewire-online/edos@b1f1fbcca9d4  data/edos_labelled_aggregated.csv, split == train only
                   (the per-annotator file is NOT read: register row 17 does not list it; X15 pending)
Dedupe-only inputs (hashed in-process, never written, never printed): HateXplain dataset.json, SBIC.v2 (all splits),
golden_train.jsonl (`state`, plus the record-bearing sources for n-gram containment).

Output: records/<scheme>.jsonl, one object per train record with a stable id, the text, the released human
annotation vector, normalized-text hashes and filter flags. Flags only describe; builders apply the orchestrator's
XED/90-10 split file and the record-claim ledger (neither exists yet).
"""
from __future__ import annotations

import csv
import io
import json
import re
import sys
import tarfile
import xml.etree.ElementTree as ET
from collections import defaultdict

from common_f2 import (HERE, LEAN, TMP, loose_text, norm_text, progress, safe_path, sha, sha_file, write_json,
                       write_jsonl)

RAW = TMP / "raw"
OUT = HERE / "records"
csv.field_size_limit(1 << 26)

XED_EMO = {1: "anger", 2: "anticipation", 3: "disgust", 4: "fear", 5: "joy", 6: "sadness", 7: "surprise", 8: "trust"}
RELEVANT_GT = {"br_edos", "gd_edos_sexism", "br_ghc", "gd_ghc_hate", "br_mams_acsa", "br_xed_en", "binj_offensive",
               "std_hate"}

UPSTREAM = {
    "xed_en": {"repo": "https://github.com/Helsinki-NLP/XED", "commit": "76666d251f147cf518071bef4f8415dab6b96115",
               "licence": "CC BY 4.0 (https://github.com/Helsinki-NLP/XED@76666d251f14)",
               "files": {"AnnotatedData/en-annotated.tsv": "xed_en-annotated.tsv", "AnnotatedData/neu_en.txt":
                         "xed_neu_en.txt", "README.md": "xed_README.md"},
               "parents": ["OPUS OpenSubtitles"]},
    "mams": {"repo": "https://github.com/siat-nlp/MAMS-for-ABSA", "commit": "cddcdb0f423b3fdb2c76b70744737abed3a00d17",
             "licence": "Apache-2.0 (https://github.com/siat-nlp/MAMS-for-ABSA/blob/master/LICENSE@cddcdb0f423b)",
             "files": {"data/MAMS-ACSA/raw/train.xml": "mams_acsa_train.xml",
                       "data/MAMS-ATSA/raw/train.xml": "mams_atsa_train.xml", "LICENSE": "mams_LICENSE"},
             "parents": ["Citysearch New York restaurant reviews (Ganu et al. 2009)"]},
    "ghc": {"repo": "https://osf.io/edua3/", "commit": "OSF node modified 2022-04-12; file ghc_train.tsv modified "
            "2021-03-03 (OSF sha256 c82a2733...)", "licence": "CC BY 4.0 (https://osf.io/edua3/ node licence "
            "'CC-By Attribution 4.0 International')", "files": {"Data/ghc_train.tsv": "ghc_train.tsv"},
            "parents": ["Gab (gab.ai posts)"]},
    "edos": {"repo": "https://github.com/rewire-online/edos", "commit": "b1f1fbcca9d42de0395432ada8fcfb5c35f68c77",
             "licence": "CC0 1.0 (https://github.com/rewire-online/edos/blob/main/LICENSE@b1f1fbcca9d4)",
             "files": {"data/edos_labelled_aggregated.csv": "edos_labelled_aggregated.csv", "LICENSE": "edos_LICENSE",
                       "README.md": "edos_README.md"},
             "parents": ["Gab (pushshift dump)", "Reddit"]},
}


def rid(scheme, native):
    return f"rec.{scheme}.{native}"


def load_xed():
    out = []
    p = safe_path(RAW / "xed_en-annotated.tsv")
    with open(p, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.rstrip("\n")
            if not line.strip():
                continue
            text, _, lab = line.rpartition("\t")
            labs = sorted({XED_EMO[int(x)] for x in re.findall(r"\d+", lab) if int(x) in XED_EMO})
            bad = [x for x in re.findall(r"\d+", lab) if int(x) not in XED_EMO]
            out.append({"id": rid("xed", f"a{i:05d}"), "dataset": "xed_en", "scheme": "xed", "record_id": f"a{i}",
                        "source_file": "AnnotatedData/en-annotated.tsv", "line": i, "split": "train",
                        "text": text, "ann": {"emotions": labs}, "_bad": bool(bad) or not labs, "_file": "annotated"})
    p = safe_path(RAW / "xed_neu_en.txt")
    with open(p, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.rstrip("\n")
            if not line.strip():
                continue
            lab, _, text = line.partition("\t")
            out.append({"id": rid("xed", f"n{i:05d}"), "dataset": "xed_en", "scheme": "xed", "record_id": f"n{i}",
                        "source_file": "AnnotatedData/neu_en.txt", "line": i, "split": "train", "text": text,
                        "ann": {"emotions": ["neutral"]}, "_bad": lab.strip() not in {"9", "0"} or not text.strip(),
                        "_file": "neutral"})
    return out


def load_mams_acsa():
    out = []
    root = ET.parse(safe_path(RAW / "mams_acsa_train.xml")).getroot()
    for i, s in enumerate(root.iter("sentence")):
        text = s.findtext("text") or ""
        asp = [(a.get("category"), a.get("polarity")) for a in s.iter("aspectCategory")]
        cats = [c for c, _ in asp]
        out.append({"id": rid("mams_acsa", f"{i:05d}"), "dataset": "mams", "scheme": "mams_acsa", "record_id": str(i),
                    "source_file": "data/MAMS-ACSA/raw/train.xml", "split": "train", "text": text,
                    "ann": {"aspects": sorted([list(x) for x in asp])},
                    "_bad": len(set(cats)) != len(cats) or len(asp) < 1, "_file": "acsa"})
    return out


def _count_sub(text, term):
    return text.lower().count(term.lower()) if term else 0


def _count_word(text, term):
    if not term:
        return 0
    return len(re.findall(r"(?<!\w)" + re.escape(term.lower()) + r"(?!\w)", text.lower()))


def load_mams_atsa():
    out = []
    root = ET.parse(safe_path(RAW / "mams_atsa_train.xml")).getroot()
    for i, s in enumerate(root.iter("sentence")):
        text = s.findtext("text") or ""
        terms = []
        for a in s.iter("aspectTerm"):
            t = a.get("term")
            terms.append({"term": t, "from": int(a.get("from")), "to": int(a.get("to")), "polarity": a.get("polarity"),
                          "n_sub": _count_sub(text, t), "n_word": _count_word(text, t),
                          "span_ok": text[int(a.get("from")):int(a.get("to"))] == t})
        low = [t["term"].lower() for t in terms]
        out.append({"id": rid("mams_atsa", f"{i:05d}"), "dataset": "mams", "scheme": "mams_atsa", "record_id": str(i),
                    "source_file": "data/MAMS-ATSA/raw/train.xml", "split": "train", "text": text,
                    "ann": {"terms": terms, "terms_unique": len(set(low)) == len(low)},
                    "_bad": len(terms) < 1, "_file": "atsa"})
    return out


def load_ghc():
    out = []
    with open(safe_path(RAW / "ghc_train.tsv"), encoding="utf-8", newline="") as f:
        rd = csv.DictReader(f, delimiter="\t")
        for i, r in enumerate(rd):
            try:
                v = {k: int(r[k]) for k in ("hd", "cv", "vo")}
                bad = any(x not in (0, 1) for x in v.values())
            except (KeyError, ValueError, TypeError):
                v, bad = {}, True
            out.append({"id": rid("ghc", f"{i:05d}"), "dataset": "ghc", "scheme": "ghc", "record_id": str(i),
                        "source_file": "Data/ghc_train.tsv", "split": "train", "text": r.get("text") or "",
                        "ann": v, "_bad": bad or not (r.get("text") or "").strip(), "_file": "train"})
    return out


def load_edos():
    out, skipped = [], defaultdict(int)
    with open(safe_path(RAW / "edos_labelled_aggregated.csv"), encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            if r.get("split") != "train":
                skipped[r.get("split")] += 1
                continue                                  # dev / test rows are dropped before any other read
            v = {"label_sexist": r["label_sexist"], "label_category": r["label_category"],
                 "label_vector": r["label_vector"]}
            out.append({"id": rid("edos", r["rewire_id"].replace("sexism2022_english-", "")), "dataset": "edos",
                        "scheme": "edos", "record_id": r["rewire_id"], "source_file":
                        "data/edos_labelled_aggregated.csv", "split": "train", "text": r["text"], "ann": v,
                        "_bad": not r["text"].strip(), "_file": "aggregated"})
    return out, dict(skipped)


def vec_key(r):
    a = r["ann"]
    s = r["scheme"]
    if s == "xed":
        return tuple(a["emotions"])
    if s == "mams_acsa":
        return tuple(tuple(x) for x in a["aspects"])
    if s == "mams_atsa":
        return tuple(sorted((t["term"].lower(), t["polarity"]) for t in a["terms"]))
    if s == "ghc":
        return tuple(sorted(a.items()))
    return (a["label_sexist"], a["label_category"], a["label_vector"])


def hx_sbf_hashes():
    hs = set()
    hx = json.load(open(safe_path(RAW / "dedupe" / "hatexplain_dataset.json"), encoding="utf-8"))
    for v in hx.values():
        t = loose_text(" ".join(v.get("post_tokens") or []))
        if t:
            hs.add(sha(t))
    n_hx = len(hs)
    with tarfile.open(safe_path(RAW / "dedupe" / "SBIC.v2.tgz")) as tf:
        for m in tf.getmembers():
            if m.isfile() and m.name.endswith(".csv"):
                txt = tf.extractfile(m).read().decode("utf-8", "replace")
                for r in csv.DictReader(io.StringIO(txt)):
                    t = loose_text(r.get("post") or "")
                    if t:
                        hs.add(sha(t))
    return hs, n_hx, len(hs) - n_hx


def golden_index(records):
    """Hash index of golden_train: loose full-state and loose line hashes (all rows), plus word n-gram containment
    over the record-bearing sources. Returns the set of record ids found in golden_train, and counts."""
    full, lines = set(), set()
    rel_tok = []
    n = 0
    p = safe_path(LEAN / "data" / "v14_parts" / "golden_train.jsonl")
    with open(p, encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            n += 1
            st = d.get("state") or ""
            if not isinstance(st, str):
                st = json.dumps(st, ensure_ascii=False)
            full.add(sha(loose_text(st)))
            for ln in st.split("\n"):
                lt = loose_text(ln)
                if lt:
                    lines.add(sha(lt))
            if d.get("source") in RELEVANT_GT:
                rel_tok.append(loose_text(st).split())
    g8 = set()
    for toks in rel_tok:
        for i in range(len(toks) - 7):
            g8.add(hash(tuple(toks[i:i + 8])))
    by_len = defaultdict(list)
    used = set()
    for r in records:
        lt = loose_text(r["text"])
        h = sha(lt)
        if h in full or h in lines:
            used.add(r["id"])
            continue
        toks = lt.split()
        if len(toks) >= 8:
            grams = [hash(tuple(toks[i:i + 8])) for i in range(len(toks) - 7)]
            if sum(g in g8 for g in grams) * 2 > len(grams):
                used.add(r["id"])
        elif len(toks) >= 3:
            by_len[len(toks)].append((r["id"], tuple(toks)))
    for L, items in by_len.items():
        gl = set()
        for toks in rel_tok:
            for i in range(len(toks) - L + 1):
                gl.add(tuple(toks[i:i + L]))
        for i_, t in items:
            if t in gl:
                used.add(i_)
    return used, {"golden_rows": n, "relevant_rows": len(rel_tok)}


def main():
    progress("build_records: parse raw files")
    xed = load_xed()
    acsa = load_mams_acsa()
    atsa = load_mams_atsa()
    ghc = load_ghc()
    edos, edos_skipped = load_edos()
    allr = xed + acsa + atsa + ghc + edos
    hs, n_hx, n_sbf = hx_sbf_hashes()
    progress(f"build_records: {len(allr)} train records parsed; scanning golden_train for the unused check")
    used, gstat = golden_index(allr)
    # duplicate texts (norm_text) per scheme; XED twice: union of both files (F10) and annotated only (F11)
    groups = {"xed_union": [r for r in xed], "xed_ann": [r for r in xed if r["_file"] == "annotated"],
              "mams_acsa": acsa, "mams_atsa": atsa, "ghc": ghc, "edos": edos}
    dup = {}
    for g, rs in groups.items():
        by = defaultdict(list)
        for r in rs:
            if not r["_bad"]:
                by[norm_text(r["text"])].append(r)
        for t, members in by.items():
            vecs = {vec_key(m) for m in members}
            keep = min(members, key=lambda m: (m["source_file"], int(re.sub(r"\D", "", m["record_id"]) or 0)))
            for m in members:
                dup.setdefault(m["id"], {})[g] = {"n": len(members), "consistent": len(vecs) == 1,
                                                  "keep": len(vecs) == 1 and m is keep}
    counts = {}
    for scheme in ("xed", "mams_acsa", "mams_atsa", "ghc", "edos"):
        rows = []
        c = defaultdict(int)
        for r in allr:
            if r["scheme"] != scheme:
                continue
            nt = norm_text(r["text"])
            lt = loose_text(r["text"])
            flags = {"malformed": r["_bad"], "in_golden_train": r["id"] in used, "short_lt3_words": len(lt.split()) < 3}
            if scheme in ("ghc", "edos"):
                flags["in_hatexplain_or_sbf"] = sha(lt) in hs
            d = dup.get(r["id"], {})
            if scheme == "xed":
                flags["dup_union"] = d.get("xed_union")
                if r["_file"] == "annotated":
                    flags["dup_annotated_only"] = d.get("xed_ann")
            else:
                flags["dup"] = d.get(scheme)
            o = {k: v for k, v in r.items() if not k.startswith("_")}
            o["xed_file"] = r["_file"] if scheme == "xed" else None
            if scheme != "xed":
                del o["xed_file"]
            o["norm_sha256"] = sha(nt)
            o["loose_sha256"] = sha(lt)
            o["flags"] = flags
            rows.append(o)
            c["records"] += 1
            for k, v in flags.items():
                if v is True:
                    c[k] += 1
        counts[scheme] = dict(c)
        shaf = write_jsonl(OUT / f"{scheme}.jsonl", rows)
        counts[scheme]["sha256"] = shaf
    raw = {}
    for ds, u in UPSTREAM.items():
        for up, local in u["files"].items():
            raw[f"{ds}:{up}"] = sha_file(RAW / local)
    write_json(TMP / "records_build.json", {"counts": counts, "edos_non_train_rows_skipped": edos_skipped,
                                             "dedupe_hashes": {"hatexplain_posts": n_hx, "sbf_posts_added": n_sbf},
                                             "golden_train": gstat, "raw_sha256": raw, "upstream": UPSTREAM})
    progress(f"build_records: done {json.dumps({k: v.get('records') for k, v in counts.items()})}")


if __name__ == "__main__":
    sys.path.insert(0, str(HERE))
    main()
