"""G1 provenance + the 3.1 public rules + deny-list + 7.4 input paths (C_DATA_SPEC v4 8 G1, 3.1, 3.H; LICENCE_REGISTER
section 1). Independent re-run on public-2's current files.
- every row (rows, reserve, dev) carries the 2.4 meta that applies to public rows; text_source.split == 'train';
  meta.licence names the dataset's register licence (allowed list of 3.1);
- every dataset in out/manifest.json has licence URL + upstream commit + licence-file sha256 + a document-text note +
  declared parents; the URL is the register's official record (same repo/file, commit prefix equal);
- the official records are RE-READ upstream now (GitHub LICENSE at the pinned commit, the AI2 DROP zip's license.txt,
  the UCI zips and dataset pages): the sha256 must equal the manifest's (a changed or missing record fails G1);
- deny-list: denylist.py check re-run (qc/gates/denylist_verdicts_recheck.json) passes every dataset, the rebuilt
  deny-list equals c_build/denylist.json, and the query covers every declared parent (bare platform words excepted,
  A16 a); denylist.py paths: every input path ok;
- 3.1: rows per dataset <= 3,000, rows per class <= 500, >= 3 wordings and >= 2 framings per dataset; mix-tuning dev
  pages / passages / records disjoint from train + reserve (Wikipedia sets split by page).
"""
import io
import json
import re
import subprocess
import urllib.request
import zipfile
from collections import Counter, defaultdict

from qclib import DATASETS, FILES, LEAN, OUT, P2, QC, TRAIN_FILES, load_all, write_gate

SCR = QC / "upstream"
META_KEYS = ("family", "spec_id", "card_id", "domain_pack", "sampler", "gen_version", "git_sha", "seed", "structure_hash",
             "difficulty_bin", "crowd_pg", "depth", "deep", "format_style", "wording_id", "defs_style", "twin_of",
             "twin_kind", "text_source", "licence", "edge")
ALLOWED = {"c_pub_hybridqa": "MIT", "c_pub_wikisql": "BSD-3-Clause", "c_pub_drop": "CC BY-SA 4.0",
           "c_pub_uci_car": "CC BY 4.0", "c_pub_uci_nursery": "CC BY 4.0"}
REGISTER = {"c_pub_hybridqa": ("github.com/wenhuchen/HybridQA/blob/", "/LICENSE", "db22fda8c595"),
            "c_pub_wikisql": ("github.com/salesforce/WikiSQL/blob/", "/LICENSE", "cffb42307775"),
            "c_pub_drop": ("ai2-public-datasets.s3.amazonaws.com/drop/drop_dataset.zip", "license.txt", None),
            "c_pub_uci_car": ("archive.ics.uci.edu/dataset/19/car+evaluation", "10.24432/C5JP48", None),
            "c_pub_uci_nursery": ("archive.ics.uci.edu/dataset/76/nursery", "10.24432/C5P88W", None)}
PLATFORM = {"wikipedia"}


def fetch(url, timeout=120):
    """curl (system CA store; the venv's python has no CA bundle: checker fix, run 1 failed with CERTIFICATE_VERIFY)."""
    r = subprocess.run(["curl", "-sSfL", "-m", str(timeout), "-A", "Mozilla/5.0 (public-2 QC licence re-read)", url],
                       capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"curl exit {r.returncode}: {r.stderr[:150]!r}")
    return r.stdout


def sha(b):
    import hashlib
    return hashlib.sha256(b).hexdigest()


def upstream(man):
    """Re-read each official record now; compare with the manifest's sha256 values."""
    SCR.mkdir(exist_ok=True)
    res, ds = {}, man["datasets"]
    for key, repo in (("c_pub_hybridqa", "wenhuchen/HybridQA"), ("c_pub_wikisql", "salesforce/WikiSQL")):
        c = ds[key]["upstream_commit"]
        try:
            b = fetch(f"https://raw.githubusercontent.com/{repo}/{c}/LICENSE")
            (SCR / f"{key}_LICENSE.txt").write_bytes(b)
            res[key] = {"record": f"github.com/{repo}/blob/{c}/LICENSE", "sha256": sha(b),
                        "equals_manifest": sha(b) == ds[key]["licence_file_sha256"],
                        "licence_text": ("MIT License" in b.decode()) if key == "c_pub_hybridqa"
                        else ("Redistribution and use in source and binary forms" in b.decode())}
        except Exception as e:  # noqa: BLE001
            res[key] = {"error": str(e)[:200], "equals_manifest": False}
    try:
        z = fetch("https://ai2-public-datasets.s3.amazonaws.com/drop/drop_dataset.zip", 300)
        zf = zipfile.ZipFile(io.BytesIO(z))
        lic = zf.read("drop_dataset/license.txt")
        (SCR / "c_pub_drop_license.txt").write_bytes(lic)
        res["c_pub_drop"] = {"zip_sha256": sha(z), "zip_equals_manifest": sha(z) == ds["c_pub_drop"]["data_files"]["drop_dataset.zip"],
                             "license_txt_sha256": sha(lic), "equals_manifest": sha(lic) == ds["c_pub_drop"]["licence_file_sha256"],
                             "licence_text": "CC BY-SA 4.0" in lic.decode(errors="replace") or "Attribution-ShareAlike 4.0" in lic.decode(errors="replace"),
                             "train_member_sha256_equals_manifest": sha(zf.read("drop_dataset/drop_dataset_train.json")) == ds["c_pub_drop"]["data_files"]["drop_dataset/drop_dataset_train.json"]}
    except Exception as e:  # noqa: BLE001
        res["c_pub_drop"] = {"error": str(e)[:200], "equals_manifest": False}
    for key, did, slug, zname, member in (("c_pub_uci_car", 19, "car+evaluation", "car+evaluation.zip", "car.data"),
                                          ("c_pub_uci_nursery", 76, "nursery", "nursery.zip", "nursery.data")):
        try:
            page = fetch(f"https://archive.ics.uci.edu/dataset/{did}/{slug}").decode(errors="replace")
            z = fetch(f"https://archive.ics.uci.edu/static/public/{did}/{slug}.zip", 300)
            zf = zipfile.ZipFile(io.BytesIO(z))
            data = zf.read(member)
            (SCR / member).write_bytes(data)
            names = [n for n in zf.namelist() if n.endswith(".names")]
            res[key] = {"page_has_cc_by_4": bool(re.search(r"CC BY 4\.0|Creative Commons Attribution 4\.0", page)),
                        "page_has_doi": REGISTER[key][1] in page,
                        "zip_sha256": sha(z), "zip_equals_manifest": sha(z) == ds[key]["data_files"][zname],
                        "data_sha256_equals_manifest": sha(data) == ds[key]["data_files"][member],
                        "names_file_sha256_equals_manifest_licence_sha": bool(names) and sha(zf.read(names[0])) == ds[key]["licence_file_sha256"]}
            res[key]["equals_manifest"] = res[key]["page_has_cc_by_4"] and res[key]["page_has_doi"] and res[key]["data_sha256_equals_manifest"]
        except Exception as e:  # noqa: BLE001
            res[key] = {"error": str(e)[:200], "equals_manifest": False}
    return res


def main():
    data = load_all()
    man = json.load(open(OUT / "manifest.json"))
    nums, fails = {}, []
    # rows: meta, split, licence
    miss, split_bad, lic_bad, src_bad = Counter(), Counter(), Counter(), Counter()
    for fn in FILES:
        for r in data[fn]:
            m = r["meta"]
            for k in META_KEYS:
                if k not in m:
                    miss[k] += 1
            ts = m.get("text_source") or {}
            if ts.get("split") != "train" or not ts.get("record_id") or not ts.get("dataset"):
                split_bad[fn] += 1
            if r["source"] not in DATASETS:
                src_bad[r["source"]] += 1
            elif ALLOWED[r["source"]] not in str(m.get("licence")):
                lic_bad[r["source"]] += 1
    nums["row_meta"] = {"rows_checked": sum(len(v) for v in data.values()), "missing_meta_keys": dict(miss),
                        "text_source_not_train": dict(split_bad), "licence_mismatch": dict(lic_bad),
                        "unknown_source": dict(src_bad)}
    if miss or split_bad or lic_bad or src_bad:
        fails.append("row_meta")
    # dataset records
    ds, rec = man["datasets"], {}
    for key in DATASETS:
        d = ds.get(key, {})
        url, c = d.get("licence_record", ""), str(d.get("upstream_commit", ""))
        a, b, cpref = REGISTER[key]
        ok = (bool(url) and bool(c) and bool(re.fullmatch(r"[0-9a-f]{64}", d.get("licence_file_sha256", "")))
              and bool(d.get("document_text")) and bool(man["parents_declared"].get(key)) and a in url
              and (b in url) and (cpref is None or c.startswith(cpref)) and ("train" in str(d.get("split_used", "")) or key.startswith("c_pub_uci")))
        rec[key] = {"url": url[:120], "commit": c[:40], "register_record_match": ok}
        if not ok:
            fails.append(f"record:{key}")
    nums["dataset_records"] = rec
    local = {sha(p.read_bytes()): p.name for p in (P2 / "licences").iterdir() if p.is_file()}
    nums["local_licence_copies"] = {k: local.get(ds[k]["licence_file_sha256"]) for k in DATASETS}
    if not all(nums["local_licence_copies"].values()):
        fails.append("local_licence_copy")
    up = upstream(man)
    nums["upstream_reread_now"] = up
    for key in DATASETS:
        if not up.get(key, {}).get("equals_manifest") or up.get(key, {}).get("licence_text") is False:
            fails.append(f"upstream:{key}")
    # deny-list re-run (made by denylist.py check in its own process, see qc/logs/denylist.log)
    ver = json.load(open(QC / "gates" / "denylist_verdicts_recheck.json"))
    import hashlib
    rebuilt = hashlib.sha256(open(QC / "gates" / "denylist_rebuilt.json", "rb").read()).hexdigest()
    canon = hashlib.sha256(open(LEAN / "c_build" / "denylist.json", "rb").read()).hexdigest()
    q = json.load(open(OUT / "denylist_query_public2.json"))["datasets"]
    qparents = {p.lower() for v in q.values() for p in v.get("parents", [])}
    uncovered = sorted({p for v in man["parents_declared"].values() for p in v
                        if p.lower() not in PLATFORM and not any(p.lower() in x or x in p.lower() for x in qparents)})
    vd = ver.get("verdicts", ver)
    counts = ver.get("counts", {})
    nums["denylist"] = {"counts": counts, "rebuilt_equals_c_build_denylist": rebuilt == canon,
                        "denylist_sha256": rebuilt, "query_datasets": sorted(q), "parents_not_in_query": uncovered}
    if counts.get("pass") != 5 or counts.get("hit", 1) != 0 or rebuilt != canon:
        fails.append("denylist")
    if uncovered:
        fails.append("denylist_parents")
    paths = [str(OUT / f"{fn}.jsonl") for fn in FILES] + [str(P2 / "tmp" / f"cand_{n}.jsonl") for n in
                                                          ("drop", "hybridqa", "uci", "wikisql")]
    pr = subprocess.run([str(LEAN.parent / ".venv/bin/python"), str(LEAN / "c_src/common/denylist.py"), "paths"] + paths,
                        capture_output=True, text=True)
    nums["input_paths_74"] = {"exit": pr.returncode, "paths": len(paths), "refused": pr.stdout.count("REFUSED")}
    if pr.returncode != 0:
        fails.append("input_paths")
    # 3.1 rules
    tr = data["rows_r1"]
    per = defaultdict(lambda: {"rows": 0, "classes": Counter(), "wordings": set(), "framings": set()})
    for r in tr:
        p = per[r["source"]]
        p["rows"] += 1
        p["classes"][("yn", r["gold"]) if r["qtype"] == "noul" else ("ch", r["gold"])] += 1
        p["wordings"].add(r["meta"]["wording_id"])
        p["framings"].add(r["meta"]["framing"])
    r31 = {}
    for k, p in per.items():
        mc = p["classes"].most_common(1)[0]
        r31[k] = {"rows": p["rows"], "max_class": [str(mc[0]), mc[1]], "wordings": len(p["wordings"]),
                  "framings": len(p["framings"])}
        if p["rows"] > 3000 or mc[1] > 500 or len(p["wordings"]) < 3 or len(p["framings"]) < 2:
            fails.append(f"rules31:{k}")
    nums["rules_3_1_rows_r1"] = r31
    # dev vs train + reserve split keys
    th = {}
    for line in open(OUT / "table_hashes.jsonl"):
        t = json.loads(line)
        th[t["id"]] = t

    def key(r):
        s, rid = r["source"], r["meta"]["text_source"]["record_id"]
        if s == "c_pub_hybridqa":
            return ("page", re.sub(r"_\d+$", "", th[r["id"]]["table_id"])) if r["id"] in th else ("rec", rid)
        if s == "c_pub_wikisql":
            return ("table", th[r["id"]]["table_id"]) if r["id"] in th else ("rec", rid)
        if s == "c_pub_drop":
            return ("passage", rid.split(":")[0])
        return ("record", rid)
    sets = {fn: defaultdict(set) for fn in FILES}
    nokey = Counter()
    for fn in FILES:
        for r in data[fn]:
            k = key(r)
            if k[0] == "rec" and r["source"] in ("c_pub_hybridqa", "c_pub_wikisql"):
                nokey[fn] += 1
            sets[fn][r["source"]].add(k)
    overlap = {s: len(sets["dev_mt_r1"][s] & (sets["rows_r1"][s] | sets["reserve_r1"][s])) for s in DATASETS}
    # WikiSQL is split by page title; the page title is part of the title_header hash's input only, so compare
    # the per-row title_header hashes too (a shared page with the same header would show here)
    tth = {fn: {th[r["id"]]["title_header"] for r in data[fn] if r["id"] in th and r["source"] == "c_pub_wikisql"} for fn in FILES}
    overlap["c_pub_wikisql_title_header"] = len(tth["dev_mt_r1"] & (tth["rows_r1"] | tth["reserve_r1"]))
    rec_overlap = {}
    for a in FILES:
        for b in FILES:
            if a < b:
                ra = {r["meta"]["text_source"]["record_id"] for r in data[a]}
                rb = {r["meta"]["text_source"]["record_id"] for r in data[b]}
                rec_overlap[f"{a}&{b}"] = len(ra & rb)
    nums["split_disjoint"] = {"dev_vs_train_reserve_shared_keys": overlap, "rows_without_table_key": dict(nokey),
                              "record_id_overlap_between_files": rec_overlap}
    if any(overlap.values()) or any(rec_overlap.values()):
        fails.append("dev_split")
    ok = not fails
    write_gate("G1", ok, nums, fails=fails)
    print("G1", ok, fails)


if __name__ == "__main__":
    main()
