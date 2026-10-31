"""di_register.py: fetch, pin and export the Decision Index leak-check material for G13 (draft ruling A61 e; module c2_build/di_g13.py).
This is a decontamination program: it is the only code that reads the DI files (bench/external_quarantine/decision_index_03/), it prints counts,
hashes and paths only (never item text), and nothing it writes outside the quarantine folder holds item text (hashes and ids only).

  cd lean && ../.venv/bin/python -B c2_build/g13_di/di_register.py <command>
    pin          the kit pin: fetch hub/0.3/manifest.json and docs/suite.md of github.com/apolinario/decision-index at --commit (default: the current
                 main), log both sha256, write g13_di/kit_pin.json (benchmarks, counts, the manifest's file hashes). Network, no DI item.
    fetch-src    the FULL DI-scored splits that feed a DI block, fetched at the suite.md pins: GSM8K test (openai/gsm8k @740312a, 1,319), HoVer dev
                 (hover-nlp/hover @39b8469, hover_dev_release_v1.1.json, 4,000) and iSarcasmEval test, all tracks (iabufarha/iSarcasmEval @dfc708b,
                 test/task_{A,B,C}_{En,Ar}_test.csv that exist). They are written as JSONL into src_splits/ in the quarantine folder; the hashed
                 record ids (question / claim / tweet text hashes, HoVer uid and hpqa_id) go to g13_di/record_ids.json.
    finalize     g13_di/di_pins.json (what di_g13 reads): per DI file its sha256 / rows, byte-identity with the manifest, per-benchmark counts of a
                 rebuild, the coverage gaps (HLE is gated: "HLE not scanned (gated)"), complete flags; and g13_di/di_never_train.json (the DI files'
                 paths and sha256 for the never-train guard). Run it after fetch-src and again after the suite rebuild.
    export       the hashed exports di_g13 uses: wording8_u64.npy (every word 8-gram of every DI request instruction / criterion string),
                 structure_g13.json (struct_g13 of each request question's state + options) and MANIFEST.json, tied to the pinned DI files.
    status       counts only: which pieces exist.
The primary path of A61 e 2 (the kit's published 0.3 frozen file) does not exist: the suite is not redistributed and the Hub datasets
multimodalart/decision-index-suite-0.x are private (HTTP 401), so the fallback applies: g13_di/di_rebuild.py rebuilds the suite with the kit.
"""
from __future__ import annotations

import argparse
import csv
import datetime
import gzip
import hashlib
import io
import json
import os
import sys
import tempfile
import urllib.request
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent                       # lean/c2_build/g13_di
sys.path.insert(0, str(HERE.parent))
import di_g13 as D  # noqa: E402

g = D.g
REPO = g.REPO
KIT = "apolinario/decision-index"
MANIFEST_PATH, SUITE_MD = "hub/0.3/manifest.json", "docs/suite.md"
# What the manifest and suite.md hash to at the 0.3 edition commit (62d2f51), its merge (9eb2dbe) and main (f5a6e4f, 14 Oct 2026): identical.
EXPECTED_SHA = {MANIFEST_PATH: "e24b2f990ed2220233af19713a13c0a92b3c1756af1991ddf985a3420bf1258c",
                SUITE_MD: "5bc0553574fd39ff9b535022105afec6523a9f96d9431cf95c39d419bfa98039"}
EDITION_COMMITS = ("62d2f51de34a", "9eb2dbe2a358004c8782c66e40a83ac07b953fec")
# suite.md "Edition 0.2": the rows file has 124,971 lines, 1,328 ToolRet and 637 BRIGHT (the retrieval subsets cut the v1 counts of 8,032 and 1,384)
V2_COUNTS = {2: 1328, 36: 637}
GSM8K_V3_ROWS = 2638
SRC_PINS = {
    "gsm8k": {"repo": "openai/gsm8k", "revision": "740312add88f781978c0658806c59bc2815b9866",
              "url": "https://huggingface.co/datasets/openai/gsm8k/resolve/740312add88f781978c0658806c59bc2815b9866/main/test-00000-of-00001.parquet",
              "suite_md": "openai/gsm8k @740312a (Hub): main/test parquet"},
    "hover": {"repo": "hover-nlp/hover", "revision": "39b84697f196308f398a251a7aea9b82ae0f0562",
              "url": "https://raw.githubusercontent.com/hover-nlp/hover/39b84697f196308f398a251a7aea9b82ae0f0562/data/hover/hover_dev_release_v1.1.json",
              "suite_md": "hover-nlp/hover @39b8469, data/hover/hover_dev_release_v1.1.json"},
    "isarcasmeval": {"repo": "iabufarha/iSarcasmEval", "revision": "dfc708b53bde1bb571abfb5692f63231c2232195",
                     "files": [f"test/task_{t}_{lang}_test.csv" for t, lang in (("A", "En"), ("A", "Ar"), ("B", "En"), ("C", "En"), ("C", "Ar"))],
                     "suite_md": "iabufarha/iSarcasmEval @dfc708b, test/task_{A,B,C}_{En,Ar}_test.csv (task B exists in English only)"},
}
EXPECTED_ROWS = {"gsm8k": 1319, "hover": 4000}


def utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _ssl_context():
    """The python.org build has no CA bundle of its own: use certifi when it is installed, else the macOS system bundle."""
    import ssl
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        cafile = "/etc/ssl/cert.pem"
        return ssl.create_default_context(cafile=cafile if os.path.exists(cafile) else None)


def fetch(url: str, timeout: int = 300) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "c2-di-register/1"})
    with urllib.request.urlopen(req, timeout=timeout, context=_ssl_context()) as r:
        return r.read()


def write_json(p: Path, obj) -> str:
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name("." + p.name + ".tmp")
    tmp.write_text(json.dumps(obj, indent=1, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, p)
    return g.sha256_file(p)


def read_json(p: Path, default=None):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


# ---- pin ------------------------------------------------------------------------------------------------------------------
def head_commit() -> str:
    return json.loads(fetch(f"https://api.github.com/repos/{KIT}/commits/main"))["sha"]


def cmd_pin(a) -> dict:
    commit = a.commit or head_commit()
    out = {"repo": f"https://github.com/{KIT}", "commit": commit, "fetched_utc": utc(), "files": {}, "same_at": {}}
    for path in (MANIFEST_PATH, SUITE_MD):
        raw = fetch(f"https://raw.githubusercontent.com/{KIT}/{commit}/{path}")
        out["files"][path] = {"sha256": sha256_bytes(raw), "bytes": len(raw), "expected_sha256": EXPECTED_SHA[path],
                              "as_expected": sha256_bytes(raw) == EXPECTED_SHA[path]}
        if path == MANIFEST_PATH:
            man = json.loads(raw)
    for c in EDITION_COMMITS:                                     # the same two files at the edition commits: the pin does not depend on which was read
        out["same_at"][c] = {p: sha256_bytes(fetch(f"https://raw.githubusercontent.com/{KIT}/{c}/{p}")) == d["sha256"]
                             for p, d in out["files"].items()}
    out.update(edition=man.get("edition"), name=man.get("name"), base_edition=man.get("base_edition"), created_utc=man.get("created_utc"),
               requests=man.get("requests"), scoreable_requests=man.get("scoreable_requests"),
               benchmarks=[{k: b.get(k) for k in ("catalog_id", "dataset", "requests")} for b in man.get("benchmarks", [])],
               added=[{k: b.get(k) for k in ("catalog_id", "dataset", "requests")} for b in man.get("added", [])],
               manifest_files=man.get("files"), retired=man.get("retired"), replaced=man.get("replaced"))
    sha = write_json(HERE / "kit_pin.json", out)
    print(json.dumps({"commit": commit, "edition": out["edition"], "manifest_sha256": out["files"][MANIFEST_PATH]["sha256"],
                      "suite_md_sha256": out["files"][SUITE_MD]["sha256"], "as_expected": all(f["as_expected"] for f in out["files"].values()),
                      "same_at_edition_commits": out["same_at"], "benchmarks": len(out["benchmarks"]), "added": len(out["added"]),
                      "kit_pin_sha256": sha}))
    return out


# ---- fetch-src ------------------------------------------------------------------------------------------------------------
def ids_of(records: dict) -> dict:
    return {k: sorted(v) for k, v in records.items()}


def cmd_fetch_src(a) -> dict:
    root = Path(a.root) if a.root else REPO
    qdir = root / D.SRC_FILES[0].rsplit("/", 1)[0]
    qdir.mkdir(parents=True, exist_ok=True)
    pins, rids = {}, {"gsm8k_question_sha256": set(), "hover_claim_sha256": set(), "hover_uid": set(), "hover_group": set(),
                      "isarcasm_text_sha256": set()}

    def out_path(name: str) -> Path:
        return root / next(f for f in D.SRC_FILES if f.endswith("/" + name))

    # GSM8K test (1,319): question + answer, from the pinned parquet
    p = SRC_PINS["gsm8k"]
    raw = fetch(p["url"])
    import pyarrow.parquet as pq
    tab = pq.read_table(io.BytesIO(raw)).to_pylist()
    with open(out_path("gsm8k_test.jsonl"), "w", encoding="utf-8") as f:
        for r in tab:
            f.write(json.dumps({"question": r["question"], "answer": r["answer"]}, ensure_ascii=False) + "\n")
            rids["gsm8k_question_sha256"].add(D.sha_hex(D.norm(r["question"])))
    pins["gsm8k"] = {**{k: p[k] for k in ("repo", "revision", "url", "suite_md")}, "raw_sha256": sha256_bytes(raw), "rows": len(tab)}
    # HoVer dev (4,000 claims): every field of the record, as released
    p = SRC_PINS["hover"]
    raw = fetch(p["url"])
    recs = json.loads(raw)
    keys = sorted({k for r in recs for k in r})
    with open(out_path("hover_dev.jsonl"), "w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
            rids["hover_claim_sha256"].add(D.sha_hex(D.norm(str(r.get("claim") or ""))))
            if r.get("uid") not in (None, ""):
                rids["hover_uid"].add(str(r["uid"]))
            if r.get("hpqa_id") not in (None, ""):
                rids["hover_group"].add(str(r["hpqa_id"]))
    pins["hover"] = {**{k: p[k] for k in ("repo", "revision", "url", "suite_md")}, "raw_sha256": sha256_bytes(raw), "rows": len(recs),
                     "fields": keys, "uids": len(rids["hover_uid"]), "groups": len(rids["hover_group"])}
    # iSarcasmEval test, every track: each CSV row with its track
    p = SRC_PINS["isarcasmeval"]
    tracks, n = {}, 0
    with open(out_path("isarcasmeval_test.jsonl"), "w", encoding="utf-8") as f:
        for rel in p["files"]:
            url = f"https://raw.githubusercontent.com/{p['repo']}/{p['revision']}/{rel}"
            raw = fetch(url)
            rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
            track = Path(rel).stem.replace("_test", "")
            for r in rows:
                f.write(json.dumps({"track": track, **{k: v for k, v in r.items() if k is not None}}, ensure_ascii=False) + "\n")
                for v in r.values():
                    if isinstance(v, str) and v.strip():
                        rids["isarcasm_text_sha256"].add(D.sha_hex(D.norm(v)))
            tracks[track] = {"url": url, "raw_sha256": sha256_bytes(raw), "rows": len(rows),
                             "columns": sorted(k for k in (rows[0] if rows else {}) if k is not None)}
            n += len(rows)
    pins["isarcasmeval"] = {"repo": p["repo"], "revision": p["revision"], "suite_md": p["suite_md"], "tracks": tracks, "rows": n}
    for name, exp in EXPECTED_ROWS.items():
        pins[name]["expected_rows"], pins[name]["as_expected"] = exp, pins[name]["rows"] == exp
    ids = ids_of(rids)
    write_json(HERE / "record_ids.json", ids)
    out = {"fetched_utc": utc(), "sources": pins, "record_ids": {k: len(v) for k, v in ids.items()},
           "files": {f: {"sha256": g.sha256_file(root / f), "rows": sum(1 for _ in open(root / f, encoding="utf-8"))} for f in D.SRC_FILES}}
    write_json(HERE / "src_pins.json", out)
    print(json.dumps({"rows": {k: v["rows"] for k, v in pins.items()}, "as_expected": {k: pins[k]["as_expected"] for k in EXPECTED_ROWS},
                      "hover_fields": keys, "record_ids": out["record_ids"], "files": {Path(f).name: d for f, d in out["files"].items()}}))
    return out


# ---- finalize -------------------------------------------------------------------------------------------------------------
def gz_stats(p: Path):
    """(gz sha256, uncompressed sha256, rows, {catalog_id: rows}) of one .jsonl.gz, streamed."""
    h_gz, h_raw, n, cat = hashlib.sha256(), hashlib.sha256(), 0, {}
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 22), b""):
            h_gz.update(blk)
    with gzip.open(p, "rb") as f:
        for line in f:
            h_raw.update(line)
            if line.strip():
                n += 1
                try:
                    cid = json.loads(line).get("_evaluation", {}).get("catalog_id")
                except ValueError:
                    cid = None
                cat[cid] = cat.get(cid, 0) + 1
    return h_gz.hexdigest(), h_raw.hexdigest(), n, cat


def expected_counts(kit: dict) -> dict:
    exp = {b["catalog_id"]: (b["dataset"], b["requests"]) for b in kit.get("benchmarks", [])}
    for cid, n in V2_COUNTS.items():
        if cid in exp:
            exp[cid] = (exp[cid][0], n)
    exp.update({b["catalog_id"]: (b["dataset"], b["requests"]) for b in kit.get("added", [])})
    return exp


def cmd_finalize(a) -> dict:
    root = Path(a.root) if a.root else REPO
    kit = read_json(HERE / "kit_pin.json", {})
    src = read_json(HERE / "src_pins.json", {})
    mfiles = kit.get("manifest_files") or {}
    pins = {"version": 1, "built_utc": utc(), "kit": {k: kit.get(k) for k in ("repo", "commit", "edition", "name", "base_edition", "requests")}
            | {"manifest_sha256": ((kit.get("files") or {}).get(MANIFEST_PATH) or {}).get("sha256"),
               "suite_md_sha256": ((kit.get("files") or {}).get(SUITE_MD) or {}).get("sha256")}}
    # ---- di03_public
    files, total, cat_all, ident = {}, {}, {}, {}
    for rel in D.DI03_FILES:
        p = root / rel
        if not p.is_file():
            continue
        gz, raw, rows, cat = gz_stats(p)
        name = Path(rel).name
        files[rel] = {"sha256": gz, "uncompressed_sha256": raw, "rows": rows}
        ident[name] = raw == (mfiles.get(name) or {}).get("uncompressed_sha256")
        for c, n in cat.items():
            cat_all[c] = cat_all.get(c, 0) + n
    exp = expected_counts(kit)
    # the 0.3 rows of GSM8K are in gsm8k-rows.jsonl.gz (2,638); the 0.2 GSM8K rows in selected-rows are a superset-only extra
    gaps, counts = [], {}
    for cid, (ds, n_exp) in sorted(exp.items(), key=lambda kv: (kv[0] is None, kv[0])) if files else []:
        got = cat_all.get(cid, 0)
        counts[str(cid)] = {"dataset": ds, "expected": n_exp, "rebuilt": got}
        if cid == 45 and got == 0:
            gaps.append(D.HLE_GAP)
        elif got == 0:
            gaps.append(f"{ds} not scanned (not rebuilt)")
        elif got < n_exp:
            gaps.append(f"{ds}: {got} of {n_exp} requests rebuilt")
    if files and not exp:
        gaps.append("kit_pin.json has no benchmark list: run di_register.py pin")
    missing = [Path(r).name for r in D.DI03_FILES if r not in files]
    if missing:
        gaps.append(f"files not rebuilt yet: {', '.join(missing)}" if files else "not rebuilt yet: none of the three DI files exists")
    pins["di03_public"] = {
        "complete": bool(files) and not missing and all(x == D.HLE_GAP for x in gaps) and sum(f["rows"] for f in files.values()) > 0,
        "build": "published" if files and all(ident.values()) else "rebuilt", "byte_identical": ident, "files": files,
        "per_benchmark": counts, "gaps": gaps, "gsm8k_v3_rows": cat_all.get(30),
        "note": "primary path (the kit's published frozen file) does not exist: the suite is not redistributed, the Hub datasets are private; "
                "fallback = suite rebuild with the kit in bench/external_quarantine/decision_index_03/ (g13_di/di_rebuild.py)"}
    # ---- di_src_splits
    sfiles, srows = {}, {}
    for rel in D.SRC_FILES:
        p = root / rel
        if p.is_file():
            sfiles[rel] = {"sha256": g.sha256_file(p), "rows": sum(1 for _ in open(p, encoding="utf-8"))}
    srcs = src.get("sources") or {}
    sgaps = [f"{n}: {srcs.get(n, {}).get('rows')} rows, expected {e}" for n, e in EXPECTED_ROWS.items() if srcs.get(n, {}).get("rows") != e]
    sgaps += [f"{Path(r).name} missing" for r in D.SRC_FILES if r not in sfiles]
    pins["di_src_splits"] = {"complete": not sgaps and bool(sfiles), "files": sfiles, "gaps": sgaps,
                             "sources": {k: {kk: vv for kk, vv in v.items() if kk != "tracks"} | ({"tracks": {t: {"rows": d["rows"], "raw_sha256": d["raw_sha256"]}
                                                                                                          for t, d in v["tracks"].items()}} if "tracks" in v else {})
                                         for k, v in srcs.items()}}
    sha = write_json(D.PINS, pins)
    # ---- the never-train fragment: the DI files' paths + sha256, merged into the mixer's guard
    nt = {"what": "A61 e 2: the DI quarantine files are never training inputs (mix_c2.merge_di_never_train)", "built_utc": utc(),
          "files": [{"path": str(root / r), "sha256": d["sha256"]} for t in D.TARGETS for r, d in pins[t]["files"].items()],
          "names": list(D.TARGETS)}
    write_json(D.NEVER_TRAIN, nt)
    print(json.dumps({"di_pins_sha256": sha, "di03_public": {"complete": pins["di03_public"]["complete"], "build": pins["di03_public"]["build"],
                                                              "files": len(files), "gaps": gaps[:12]},
                      "di_src_splits": {"complete": pins["di_src_splits"]["complete"], "files": len(sfiles), "gaps": sgaps},
                      "never_train_entries": len(nt["files"])}))
    return pins


# ---- export ---------------------------------------------------------------------------------------------------------------
def cmd_export(a) -> dict:
    root = Path(a.root) if a.root else REPO
    pins = D.load_pins()
    if not (pins.get("di03_public") or {}).get("files"):
        raise SystemExit("export: no di03_public files in g13_di/di_pins.json (run finalize after the rebuild)")
    chunks, buf, structs, nreq, nstr = [], [], set(), 0, 0
    for rel in D.DI03_FILES:
        p = root / rel
        if not p.is_file():
            continue
        with gzip.open(p, "rt", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                row = json.loads(line)
                nreq += 1
                for s in D.request_wording(row):
                    ws = D.words(s)
                    if len(ws) >= D.GRAM:
                        buf += D.gram_u64(ws)
                        nstr += 1
                        if len(buf) > 2_000_000:
                            chunks.append(np.unique(np.array(buf, np.uint64)))
                            buf = []
                structs |= D.request_structs(row)
    if buf:
        chunks.append(np.unique(np.array(buf, np.uint64)))
    w8 = np.unique(np.concatenate(chunks)) if chunks else np.array([], np.uint64)
    np.save(D.DI_DIR / "wording8_u64.npy", w8)
    (D.DI_DIR / "structure_g13.json").write_text(json.dumps(sorted(structs)), encoding="utf-8")
    ids = read_json(D.DI_DIR / "record_ids.json", {})
    man = {"built_utc": utc(), "derived_from": D.pinned_files(pins), "requests_read": nreq, "wording_strings": nstr,
           "files": {n: {"sha256": g.sha256_file(D.DI_DIR / n)} for n in D.DiExports.FILES},
           "counts": {"wording8": len(w8), "structure_g13": len(structs), **{k: len(v) for k, v in ids.items()}},
           "what": "hashed exports of the DI 0.3 public suite and the DI source splits for g13_c2 (A61 e); no item text"}
    write_json(D.EXPORT_MANIFEST, man)
    print(json.dumps({"requests_read": nreq, "wording_strings": nstr, "wording8": len(w8), "structure_g13": len(structs),
                      "manifest_sha256": g.sha256_file(D.EXPORT_MANIFEST)}))
    return man


def cmd_status(a) -> dict:
    pins = D.load_pins()
    out = {"kit_pin": (HERE / "kit_pin.json").is_file(), "src_pins": (HERE / "src_pins.json").is_file(), "di_pins": D.PINS.is_file(),
           "exports": {n: (D.DI_DIR / n).is_file() for n in D.DiExports.FILES + ("MANIFEST.json",)},
           "targets": {n: {"gap": D.gap_for(n, pins)} for n in D.TARGETS}, "never_train": D.NEVER_TRAIN.is_file()}
    print(json.dumps(out))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pin")
    p.add_argument("--commit")
    for c in ("fetch-src", "finalize", "export", "status"):
        q = sub.add_parser(c)
        q.add_argument("--root", help="repo root for the quarantine files (tests only)")
    a = ap.parse_args(argv)
    return {"pin": cmd_pin, "fetch-src": cmd_fetch_src, "finalize": cmd_finalize, "export": cmd_export, "status": cmd_status}[a.cmd](a)


if __name__ == "__main__":
    main()
