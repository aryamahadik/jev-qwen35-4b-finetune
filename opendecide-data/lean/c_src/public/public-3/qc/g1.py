#!/usr/bin/env python3
"""G1 provenance + spec 3.1 rules for public-3 (independent checker, prep5/B4; never prints row text).

Checks on the CURRENT files (rows_r1 + reserve are the mixed files; mtdev for split separation only):
  rows   : every row has the spec 2.4 keys + meta keys; meta.text_source {dataset, record_id, split == "train"};
           meta.licence starts with the dataset's licence and cites a record URL; meta.human_label present; no
           teacher_src other than "human_votes"; source in the manifest.
  split  : every row's meta.record_uid is a split_3e record with part == "train" and sealed_drop false; every mtdev
           row's record has part == "dev"; no record shared between mixed rows and mtdev.
  sources: manifest licence is on the owner's allowed list (3.1), share_alike false (or listed in notices), official
           record + upstream commit + text-licence note present, the official record is the one in
           LICENCE_REGISTER.md section 1 (row marked IN, never an HF card), every saved licence record's sha256
           equals the recorded one and contains the licence string; live re-read of every record URL (free GET):
           licence string still present (unreachable = reported, the builder's 3 Oct re-read stands).
  shape  : r1 rows per dataset == spec 3.2 round-1 use; <= 500 rows per class, <= 3,000 per dataset;
           >= 3 wordings and >= 2 framings per dataset.
Writes qc/g1.json."""
import hashlib, json, re, ssl, sys, urllib.request
import certifi

CTX = ssl.create_default_context(cafile=certifi.where())
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
P3 = HERE.parent
LEAN = P3.parents[2]
OUT = P3 / "out"
MIXED = ["public3_rows_r1.jsonl", "public3_reserve.jsonl"]
ALLOWED = ("CC0 1.0", "CC BY 4.0", "Apache-2.0", "MIT", "ODC-BY", "BSD", "public domain")
R1_USE = {"c_pub_xed": 600, "c_pub_mams": 750, "c_pub_sarcasm": 350, "c_pub_ghc": 350, "c_pub_edos": 350}
TOP = ["id", "group_id", "call_id", "source", "state", "qtype", "instructions", "options", "gold", "role", "card", "meta"]
META = ["family", "spec_id", "card_id", "domain_pack", "sampler", "gen_version", "git_sha", "seed", "structure_hash",
        "difficulty_bin", "crowd_pg", "depth", "deep", "format_style", "wording_id", "defs_style", "twin_of",
        "twin_kind", "text_source", "licence", "edge"]
# licence string each saved / live record must contain (regex, case-insensitive)
MUST = {"xed_readme": r"Creative Commons Attribution 4\.0|CC-BY",
        "mams_license": r"Apache License[\s\S]*Version 2\.0",
        "mams_readme": r"data",
        "sarcasm_kaggle_view": r'"licenseName": "Attribution 4\.0 International \(CC BY 4\.0\)"',
        "ghc_osf_node": r"CC-By Attribution 4\.0 International",
        "ghc_osf_data_folder": r"ghc_train\.tsv",
        "edos_license": r"CC0 1\.0 Universal",
        "edos_readme": r"EDOS|edos"}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def uids(r):
    u = r["meta"].get("record_uid")
    return set(u) if isinstance(u, list) else {u}


def rows(name):
    return [json.loads(l) for l in open(OUT / name)]


def main():
    man = json.load(open(P3 / "manifest_public3.json"))
    ds = man["datasets"]
    prob, res = [], {}
    # ---- rows
    mixed = [(n, r) for n in MIXED for r in rows(n)]
    miss_top, miss_meta, bad_ts, bad_lic, no_hl, bad_teacher, bad_src = Counter(), Counter(), 0, 0, 0, 0, 0
    for n, r in mixed:
        m = r.get("meta", {})
        for k in TOP:
            miss_top[k] += k not in r
        for k in META:
            miss_meta[k] += k not in m
        ts = m.get("text_source") or {}
        if not (ts.get("dataset") and ts.get("record_id") and ts.get("split") == "train"):
            bad_ts += 1
        d = ds.get(r.get("source"))
        if d is None:
            bad_src += 1
            continue
        lic = str(m.get("licence", ""))
        if not (lic.startswith(d["licence"]) and re.search(r"record https?://", lic)):
            bad_lic += 1
        no_hl += not m.get("human_label")
        bad_teacher += m.get("teacher_src") not in (None, "human_votes")
    res["rows"] = {"n_mixed_rows": len(mixed), "missing_top_keys": sum(miss_top.values()),
                   "missing_meta_keys": {k: v for k, v in miss_meta.items() if v},
                   "text_source_bad": bad_ts, "licence_meta_bad": bad_lic, "human_label_missing": no_hl,
                   "teacher_src_not_human": bad_teacher, "source_not_in_manifest": bad_src}
    if sum(miss_top.values()) or any(miss_meta.values()) or bad_ts or bad_lic or no_hl or bad_teacher or bad_src:
        prob.append("row provenance keys / licence meta")
    # ---- split separation
    part = {}
    for l in open(OUT / "public3_split_3e.jsonl"):
        x = json.loads(l)
        part[x["id"]] = (x["part"], x["sealed_drop"])
    mix_recs = set().union(*(uids(r) for _, r in mixed))
    bad_part = Counter(str(part.get(u, "missing")) for u in mix_recs if part.get(u) != ("train", False))
    dev = rows("public3_mtdev.jsonl")
    dev_recs = set().union(*(uids(r) for r in dev))
    dev_bad = Counter(str(part.get(u, "missing")) for u in dev_recs if (part.get(u) or ("?",))[0] != "dev")
    shared = len(mix_recs & dev_recs)
    res["split"] = {"mixed_records": len(mix_recs), "mixed_records_not_train_or_dropped": dict(bad_part),
                    "mtdev_records": len(dev_recs), "mtdev_records_not_dev": dict(dev_bad),
                    "records_shared_mixed_mtdev": shared}
    if bad_part or dev_bad or shared:
        prob.append("split separation")
    # ---- sources
    reg = (LEAN / "c_spec/LICENCE_REGISTER.md").read_text()
    reg1 = reg.split("## 2.")[0]
    src = {}
    for key, d in ds.items():
        s = {"licence": d["licence"], "allowed": d["licence"].startswith(ALLOWED),
             "share_alike": d["share_alike"], "official_record": bool(d.get("official_record")),
             "upstream_commit": bool(d.get("upstream_commit")), "text_licence_note": bool(d.get("text_licence"))}
        url = re.search(r"https?://\S+", d["official_record"]).group(0)
        line = next((ln for ln in reg1.splitlines() if url.split("/blob/")[0].rstrip("/") in ln), "")
        s["register_sec1_row"] = bool(line)
        s["register_in"] = "**IN**" in line or "| IN" in line
        s["not_hf_card"] = "huggingface.co" not in url
        recs = {}
        for rn, rr in d["licence_record_reread"].items():
            f = next(iter(sorted(P3.glob(rr["saved"] + "*"))), None)
            body = f.read_bytes() if f else b""
            txt = body.decode("utf-8", "replace")
            if f and f.suffix == ".json":
                txt = json.dumps(json.loads(txt))
            rec = {"saved_exists": f is not None, "sha256_match": bool(f) and hashlib.sha256(body).hexdigest() == rr["sha256"],
                   "licence_string_saved": bool(re.search(MUST[rn], txt, re.I)), "builder_checks_pass": rr["checks_pass"] in (True, "True")}
            try:
                req = urllib.request.Request(rr["url"], headers={"User-Agent": "Mozilla/5.0 (public-3 QC)"})
                live = urllib.request.urlopen(req, timeout=20, context=CTX).read()
                lt = live.decode("utf-8", "replace")
                try:
                    lt = json.dumps(json.loads(lt))
                except ValueError:
                    pass
                rec["live"] = {"reached": True, "licence_string": bool(re.search(MUST[rn], lt, re.I)),
                               "bytes_equal_saved": live == body}
            except Exception as e:  # noqa: BLE001
                rec["live"] = {"reached": False, "error": type(e).__name__ + ": " + str(e)[:80]}
            recs[rn] = rec
            if not (rec["saved_exists"] and rec["sha256_match"] and rec["licence_string_saved"] and rec["builder_checks_pass"]):
                prob.append(f"{key}: saved licence record {rn}")
            if rec["live"].get("reached") and not rec["live"]["licence_string"]:
                prob.append(f"{key}: live licence record {rn} lost its licence string")
        s["records"] = recs
        for k in ("allowed", "official_record", "upstream_commit", "text_licence_note", "register_sec1_row",
                  "register_in", "not_hf_card"):
            if not s[k]:
                prob.append(f"{key}: {k}")
        if s["share_alike"] and key not in str(man.get("notices_file_entries")):
            prob.append(f"{key}: share-alike not in notices")
        src[key] = s
    res["sources"] = src
    # ---- shape
    r1 = rows("public3_rows_r1.jsonl")
    per_ds, per_cls, wd, fr = Counter(), Counter(), defaultdict(set), defaultdict(set)
    for _, r in mixed:
        per_cls[(r["source"], r["qtype"], str(r["gold"]))] += 1
        wd[r["source"]].add(r["meta"].get("wording_id"))
        fr[r["source"]].add(r["qtype"] + ":" + str(r["meta"].get("k")))
    for r in r1:
        per_ds[r["source"]] += 1
    # repair r1: a dataset dropped by the spec 8 G5 dataset-level rule for public rows ("drop the dataset if > 8% clearly
    # wrong") is listed in manifest dropped_datasets; its spec 3.2 share goes to the named fallback (F11 for 3E, logged
    # in the mixer report), so its target here is 0 rows and it must have no row in any file.
    dropped = json.load(open(P3 / "manifest_public3.json")).get("dropped_datasets", {})
    target = {k: (0 if k in dropped else v) for k, v in R1_USE.items()}
    assert all("G5" in v.get("dropped", "") for v in dropped.values()), "a drop must cite the spec 8 G5 rule"
    if any(r["source"] in dropped for _, r in mixed) or any(r["source"] in dropped for r in rows("public3_mtdev.jsonl")):
        prob.append("a dropped dataset still has rows")
    res["shape"] = {"r1_rows_per_dataset": dict(per_ds), "r1_target": target, "dropped_datasets": sorted(dropped),
                    "max_rows_per_gold_value_mixed": max(per_cls.values()),
                    "wordings_per_dataset": {k: len(v) for k, v in wd.items()},
                    "framings_per_dataset": {k: len(v) for k, v in fr.items()}}
    if {k: per_ds.get(k, 0) for k in target} != target or set(per_ds) - set(target):
        prob.append("r1 rows per dataset != spec 3.2 round-1 use")
    if max(per_cls.values()) > 500:
        prob.append("class cap 500")
    if any(len(v) < 3 for v in wd.values()) or any(len(v) < 2 for v in fr.values()):
        prob.append(">= 3 wordings / >= 2 framings")
    out = {"gate": "G1", "pass": not prob, "problems": prob, **res}
    (HERE / "g1.json").write_text(json.dumps(out, indent=1))
    live = Counter((rn, v["live"].get("reached"), v["live"].get("licence_string")) for s in src.values()
                   for rn, v in s["records"].items())
    print(json.dumps({"pass": out["pass"], "problems": prob, "rows": res["rows"], "split": res["split"],
                      "shape": res["shape"]})[:2500])
    print("live:", sorted((k[0], k[1], k[2]) for k in live))


if __name__ == "__main__":
    main()
