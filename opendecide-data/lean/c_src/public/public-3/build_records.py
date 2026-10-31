#!/usr/bin/env python3
"""public-3 records: parse the pinned train files of 3.2 #13-17 into one record per item, flag every filter, assign the
shared 3E 90/10 part, and write

  tmp/records/<scheme>.jsonl   (text + human annotation + flags; builder-internal)
  out/public3_split_3e.jsonl   (the shared split file: record id, dataset, scheme, file, norm/loose sha256, part;
                                no text) -- the F10 R2-23 / F11 handoff "shared split file for all four datasets",
                                plus Sarcasm v2
  logs/records_stats.json

Filters (flags only describe; the row builders apply them):
  malformed            unparsable label or empty text
  short_lt3_words      loose text has < 3 words
  in_golden_train      spec 3.1 "unused records only": loose full text equals a golden_train state / line, or
                       > 50% of its word 8-grams (texts >= 8 words) or its whole word sequence (3-7 words) occur in a
                       golden_train row of the 3E-adjacent sources (state + instructions + options)
  in_hatexplain_or_sbf GHC / EDOS only (spec 3.2 #16-17, 7.1): loose text equals a HateXplain or SBIC.v2 post (all
                       splits; hashed in-process, never written)
  dup                  duplicate loose text inside the scheme: keep the lowest record only if every copy has the same
                       annotation vector, else drop every copy
  outlet_redacted /    Sarcasm v2: outlet names redacted; a bare 'onion' (not 'the onion') is dropped
  outlet_drop
  sealed_drop          (v1.1) added after this script by flag_sealed_records.py: a sealed-suite hit in public-3's
                       own id-only records check (run_sealed_records.sh) or in formats-2's records check
Dedupe-only inputs are read from raw/dedupe and deleted with raw/ after the build.
"""
from __future__ import annotations

import csv
import io
import json
import re
import sys
import tarfile
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "lib"))
from common3 import (LEAN, LOGS, OUT, RAW, REC, loose_text, norm_text, progress, safe_in, sha, split_part,  # noqa: E402
                     write_jsonl)
import xxhash  # noqa: E402

csv.field_size_limit(1 << 26)
XED_EMO = {1: "anger", 2: "anticipation", 3: "disgust", 4: "fear", 5: "joy", 6: "sadness", 7: "surprise", 8: "trust"}
RELEVANT_GT = {"binj_offensive", "br_convabuse", "br_edos", "br_emobank", "br_ghc", "br_hatemoji_build", "br_mams_acsa",
               "br_sarcasm_headlines", "br_xed_en", "gd_csc_sarcasm", "gd_edos_sexism", "gd_ghc_hate",
               "gd_hatemoji_build_v14", "std_hate", "toxic_conv"}
URL = re.compile(r"(https?://\S+|www\.\S+)", re.I)
HANDLE = re.compile(r"(?<![\w@])@[A-Za-z0-9_]{1,30}")
OUTLET = re.compile(r"\b(the onion|onion\.com|theonion|huffpost|huff post|huffington post|huffingtonpost|huffpo)\b", re.I)
BARE_ONION = re.compile(r"\bonions?\b", re.I)


def h(s: str) -> int:
    return xxhash.xxh64_intdigest(s.encode("utf-8"))


def rid(scheme, native):
    return f"rec.{scheme}.{native}"


def load_xed():
    out = []
    with open(safe_in(RAW / "xed/en-annotated.tsv"), encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.rstrip("\n")
            if not line.strip():
                continue
            text, _, lab = line.rpartition("\t")
            nums = [int(x) for x in re.findall(r"\d+", lab)]
            labs = sorted({XED_EMO[x] for x in nums if x in XED_EMO})
            bad = any(x not in XED_EMO for x in nums) or not labs or not text.strip()
            out.append({"id": rid("xed", f"a{i:05d}"), "dataset": "xed_en", "scheme": "xed", "record_id": f"a{i}",
                        "file": "AnnotatedData/en-annotated.tsv", "text": text, "ann": {"emotions": labs},
                        "_bad": bad})
    with open(safe_in(RAW / "xed/neu_en.txt"), encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.rstrip("\n")
            if not line.strip():
                continue
            lab, _, text = line.partition("\t")
            out.append({"id": rid("xed", f"n{i:05d}"), "dataset": "xed_en", "scheme": "xed", "record_id": f"n{i}",
                        "file": "AnnotatedData/neu_en.txt", "text": text, "ann": {"emotions": ["neutral"]},
                        "_bad": lab.strip() not in {"9", "0"} or not text.strip()})
    return out


def load_mams_acsa():
    out = []
    root = ET.parse(safe_in(RAW / "mams/acsa_train.xml")).getroot()
    for i, s in enumerate(root.iter("sentence")):
        text = s.findtext("text") or ""
        asp = [(a.get("category"), a.get("polarity")) for a in s.iter("aspectCategory")]
        cats = [c for c, _ in asp]
        out.append({"id": rid("mams_acsa", f"{i:05d}"), "dataset": "mams", "scheme": "mams_acsa", "record_id": str(i),
                    "file": "data/MAMS-ACSA/raw/train.xml", "text": text, "ann": {"aspects": sorted([list(x) for x in asp])},
                    "_bad": len(set(cats)) != len(cats) or len(asp) < 1 or not text.strip()})
    return out


def _count_word(text, term):
    return len(re.findall(r"(?<!\w)" + re.escape(term.lower()) + r"(?!\w)", text.lower())) if term else 0


def load_mams_atsa():
    out = []
    root = ET.parse(safe_in(RAW / "mams/atsa_train.xml")).getroot()
    for i, s in enumerate(root.iter("sentence")):
        text = s.findtext("text") or ""
        terms = []
        for a in s.iter("aspectTerm"):
            t = a.get("term")
            fr, to = int(a.get("from")), int(a.get("to"))
            terms.append({"term": t, "from": fr, "to": to, "polarity": a.get("polarity"),
                          "n_word": _count_word(text, t), "span_ok": text[fr:to] == t})
        low = [t["term"].lower() for t in terms]
        out.append({"id": rid("mams_atsa", f"{i:05d}"), "dataset": "mams", "scheme": "mams_atsa", "record_id": str(i),
                    "file": "data/MAMS-ATSA/raw/train.xml", "text": text,
                    "ann": {"terms": terms, "terms_unique": len(set(low)) == len(low)},
                    "_bad": len(terms) < 1 or not text.strip()})
    return out


def load_ghc():
    out = []
    with open(safe_in(RAW / "ghc/ghc_train.tsv"), encoding="utf-8", newline="") as f:
        rd = csv.DictReader(f, delimiter="\t")
        assert rd.fieldnames == ["text", "hd", "cv", "vo"], rd.fieldnames
        for i, r in enumerate(rd):
            try:
                v = {k: int(r[k]) for k in ("hd", "cv", "vo")}
                bad = any(x not in (0, 1) for x in v.values())
            except (KeyError, ValueError, TypeError):
                v, bad = {}, True
            out.append({"id": rid("ghc", f"{i:05d}"), "dataset": "ghc", "scheme": "ghc", "record_id": str(i),
                        "file": "Data/ghc_train.tsv", "text": r.get("text") or "", "ann": v,
                        "_bad": bad or not (r.get("text") or "").strip()})
    return out


def load_edos():
    out, skipped = [], Counter()
    with open(safe_in(RAW / "edos/edos_labelled_aggregated.csv"), encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            if r.get("split") != "train":
                skipped[r.get("split")] += 1
                continue                                  # dev / test rows are dropped before any other read
            v = {"label_sexist": r["label_sexist"], "label_category": r["label_category"],
                 "label_vector": r["label_vector"]}
            out.append({"id": rid("edos", r["rewire_id"].replace("sexism2022_english-", "")), "dataset": "edos",
                        "scheme": "edos", "record_id": r["rewire_id"], "file": "data/edos_labelled_aggregated.csv",
                        "text": r["text"], "ann": v, "_bad": not r["text"].strip()})
    return out, dict(skipped)


def load_sarcasm():
    out = []
    p = safe_in(RAW / "sarcasm/Sarcasm_Headlines_Dataset_v2.json")
    with open(p, encoding="utf-8") as f:
        for i, line in enumerate(f):
            if not line.strip():
                continue
            d = json.loads(line)
            text = d.get("headline") or ""
            lab = d.get("is_sarcastic")
            red, n = OUTLET.subn("[outlet]", text)
            drop = bool(BARE_ONION.search(red))
            out.append({"id": rid("sarcasm_v2", f"{i:05d}"), "dataset": "sarcasm_v2", "scheme": "sarcasm_v2",
                        "record_id": str(i), "file": "Sarcasm_Headlines_Dataset_v2.json", "text": red,
                        "text_orig_norm_sha256": sha(norm_text(text)),
                        "ann": {"is_sarcastic": lab}, "_bad": lab not in (0, 1) or not text.strip(),
                        "_outlet_redacted": n > 0, "_outlet_drop": drop})
    return out


def placeholders(r):
    """GHC: handles and URLs become placeholders (EDOS already uses [USER] / [URL])."""
    if r["scheme"] != "ghc":
        return 0
    t, n1 = URL.subn("[URL]", r["text"])
    t, n2 = HANDLE.subn("[USER]", t)
    r["text"] = t
    return n1 + n2


def vec_key(r):
    a, s = r["ann"], r["scheme"]
    if s == "xed":
        return tuple(a["emotions"])
    if s == "mams_acsa":
        return tuple(tuple(x) for x in a["aspects"])
    if s == "mams_atsa":
        return tuple(sorted((t["term"].lower(), t["polarity"]) for t in a["terms"]))
    if s == "ghc":
        return tuple(sorted(a.items()))
    if s == "sarcasm_v2":
        return (a["is_sarcastic"],)
    return (a["label_sexist"], a["label_category"], a["label_vector"])


def hx_sbf_hashes():
    hs = set()
    hx = json.load(open(safe_in(RAW / "dedupe/hatexplain_dataset.json"), encoding="utf-8"))
    for v in hx.values():
        t = loose_text(" ".join(v.get("post_tokens") or []))
        if t:
            hs.add(h(t))
    n_hx = len(hs)
    with tarfile.open(safe_in(RAW / "dedupe/SBIC.v2.tgz")) as tf:
        for m in tf.getmembers():
            if m.isfile() and m.name.endswith(".csv"):
                txt = tf.extractfile(m).read().decode("utf-8", "replace")
                for r in csv.DictReader(io.StringIO(txt)):
                    t = loose_text(r.get("post") or "")
                    if t:
                        hs.add(h(t))
    return hs, {"hatexplain_posts": n_hx, "sbic_posts_added": len(hs) - n_hx}


def golden_index(records):
    full, lines = set(), set()
    rel_tok = []
    n = 0
    src_rel = Counter()
    p = safe_in(LEAN / "data" / "v14_parts" / "golden_train.jsonl")
    with open(p, encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            n += 1
            st = d.get("state") or ""
            if not isinstance(st, str):
                st = json.dumps(st, ensure_ascii=False)
            ins = d.get("instructions") or ""
            if not isinstance(ins, str):
                ins = json.dumps(ins, ensure_ascii=False)
            full.add(h(loose_text(st)))
            for ln in (st + "\n" + ins).split("\n"):
                lt = loose_text(ln)
                if lt:
                    lines.add(h(lt))
            if d.get("source") in RELEVANT_GT:
                src_rel[d["source"]] += 1
                opts = d.get("options") or []
                if not isinstance(opts, list):
                    opts = [str(opts)]
                rel_tok.append(loose_text(st + " \n " + ins + " \n " + " \n ".join(map(str, opts))).split())
    g8 = set()
    for toks in rel_tok:
        for i in range(len(toks) - 7):
            g8.add(h(" ".join(toks[i:i + 8])))
    used = set()
    by_len = defaultdict(list)
    for r in records:
        lt = loose_text(r["text"])
        if not lt:
            continue
        hv = h(lt)
        if hv in full or hv in lines:
            used.add(r["id"])
            continue
        toks = lt.split()
        if len(toks) >= 8:
            grams = [h(" ".join(toks[i:i + 8])) for i in range(len(toks) - 7)]
            if sum(g in g8 for g in grams) * 2 > len(grams):
                used.add(r["id"])
        elif len(toks) >= 1:
            by_len[len(toks)].append((r["id"], " ".join(toks)))
    for L, items in by_len.items():
        gl = set()
        for toks in rel_tok:
            for i in range(len(toks) - L + 1):
                gl.add(h(" ".join(toks[i:i + L])))
        for i_, t in items:
            if h(t) in gl:
                used.add(i_)
    return used, {"golden_rows": n, "relevant_rows": len(rel_tok), "relevant_sources": dict(src_rel)}


def main():
    progress("build_records: parse pinned train files")
    xed = load_xed()
    acsa = load_mams_acsa()
    atsa = load_mams_atsa()
    ghc = load_ghc()
    edos, edos_skipped = load_edos()
    sar = load_sarcasm()
    n_ph = Counter()
    for r in ghc:
        n_ph["ghc_placeholder_subs"] += placeholders(r)
    allr = xed + acsa + atsa + ghc + edos + sar
    hs, hstat = hx_sbf_hashes()
    used, gstat = golden_index(allr)
    progress(f"build_records: {len(allr)} records parsed; golden_train used {len(used)}")
    dup = {}
    for scheme in ("xed", "mams_acsa", "mams_atsa", "ghc", "edos", "sarcasm_v2"):
        by = defaultdict(list)
        for r in allr:
            if r["scheme"] == scheme and not r["_bad"]:
                by[loose_text(r["text"])].append(r)
        for t, members in by.items():
            if len(members) == 1:
                continue
            vecs = {vec_key(m) for m in members}
            keep = min(members, key=lambda m: (m["file"], int(re.sub(r"\D", "", m["record_id"]) or 0)))
            for m in members:
                dup[m["id"]] = {"n": len(members), "consistent": len(vecs) == 1, "keep": len(vecs) == 1 and m is keep}
    stats = {"edos_non_train_rows_skipped": edos_skipped, "dedupe_hashes": hstat, "golden_train": gstat,
             "placeholders": dict(n_ph), "schemes": {}}
    split_rows = []
    for scheme in ("xed", "mams_acsa", "mams_atsa", "ghc", "edos", "sarcasm_v2"):
        rows, c = [], Counter()
        for r in allr:
            if r["scheme"] != scheme:
                continue
            lt = loose_text(r["text"])
            d = dup.get(r["id"])
            flags = {"malformed": r["_bad"], "short_lt3_words": len(lt.split()) < 3,
                     "in_golden_train": r["id"] in used,
                     "dup_drop": bool(d) and not d["keep"]}
            if scheme in ("ghc", "edos"):
                flags["in_hatexplain_or_sbf"] = h(lt) in hs
            if scheme == "sarcasm_v2":
                flags["outlet_redacted"] = r["_outlet_redacted"]
                flags["outlet_drop"] = r["_outlet_drop"]
            part = split_part(r["text"])
            o = {k: v for k, v in r.items() if not k.startswith("_")}
            o["norm_sha256"] = sha(norm_text(r["text"]))
            o["loose_sha256"] = sha(lt)
            o["part"] = part
            o["flags"] = flags
            o["eligible"] = not any(v for k, v in flags.items() if k != "outlet_redacted")
            rows.append(o)
            c["records"] += 1
            c[f"part_{part}"] += 1
            c[f"eligible_{part}"] += o["eligible"]
            for k, v in flags.items():
                c[k] += bool(v)
            split_rows.append({"id": o["id"], "dataset": o["dataset"], "scheme": scheme, "record_id": o["record_id"],
                               "file": o["file"], "norm_sha256": o["norm_sha256"], "loose_sha256": o["loose_sha256"],
                               "part": part})
        c["sha256"] = write_jsonl(REC / f"{scheme}.jsonl", rows)
        stats["schemes"][scheme] = dict(c)
    stats["split_file_sha256"] = write_jsonl(OUT / "public3_split_3e.jsonl", split_rows)
    stats["split_rule"] = ('part = "dev" if int(sha256("c-pub-3e-split|" + loose_text(text))[:8], 16) % 10 == 0 '
                           'else "train"; loose_text = formats-2 loose_text (NFKC, straight quotes, casefold, '
                           'non-word runs -> space); text = the record text after public-3 redaction (Sarcasm outlet '
                           'names) / placeholders (GHC URLs, handles)')
    # cross-check vs formats-2 record pools (ids and normalized-text hashes only)
    xc = {}
    f2 = LEAN / "c_src" / "formats" / "formats-2" / "records"
    mine = {r["id"]: r for r in allr}
    for scheme in ("xed", "mams_acsa", "mams_atsa", "ghc", "edos"):
        p = f2 / f"{scheme}.jsonl"
        if not p.exists():
            xc[scheme] = "formats-2 file missing"
            continue
        n = same_id = same_norm = 0
        with open(safe_in(p), encoding="utf-8") as f:
            for line in f:
                o = json.loads(line)
                n += 1
                m = mine.get(o["id"])
                if m is None:
                    continue
                same_id += 1
                same_norm += o.get("norm_sha256") == sha(norm_text(m["text"]))
        xc[scheme] = {"formats2_records": n, "mine": sum(1 for r in allr if r["scheme"] == scheme),
                      "same_id": same_id, "same_norm_sha256": same_norm}
    stats["formats2_crosscheck"] = xc
    (LOGS / "records_stats.json").write_text(json.dumps(stats, indent=1))
    progress("build_records: done " + json.dumps({k: {"records": v["records"], "eligible_train": v.get("eligible_train", 0),
                                                       "eligible_dev": v.get("eligible_dev", 0)}
                                                   for k, v in stats["schemes"].items()}))


if __name__ == "__main__":
    main()
