"""formats-2: run the id-only sealed checker (lean/sealed_nd/qc/sealed_check.py, as a program; never read its exports)
on every output, and write tmp/sealed/hits.json (ids and hit kinds only). JSON (non-JSONL) outputs are checked through
one-object-per-line views in tmp/sealed/."""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter

from common_f2 import HERE, LEAN, progress, sha_file

CHECKER = LEAN / "sealed_nd" / "qc" / "sealed_check.py"
PY = "/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python"
SD = HERE / "tmp" / "sealed"
SUITE = "f4ae863720535b6ba27acad51917fe07b4d31344228a1dddb9d98bc3a4deac68"


def views():
    out = {}
    SD.mkdir(parents=True, exist_ok=True)
    reg = json.load(open(HERE / "locales" / "registers.json"))
    loc = json.load(open(HERE / "locales" / "locales.json"))
    lex = json.load(open(HERE / "codebooks" / "lexicon.json"))
    for name, rows in (("registers", reg["registers"]), ("locales", loc["locales"])):
        p = SD / f"view_{name}.jsonl"
        with open(p, "w") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        out[f"locales/{name}.json"] = p
    p = SD / "view_lexicon.jsonl"
    with open(p, "w") as f:
        for d in lex["lexicons"]:
            for t in d["templates"]:
                f.write(json.dumps({"id": t["id"], "template": t["template"]}, ensure_ascii=False) + "\n")
            for v in d["values"]:
                f.write(json.dumps({"id": v["id"], "value": v["value"], "gloss": v["gloss"]}, ensure_ascii=False) + "\n")
            f.write(json.dumps({"id": d["id"], "dimension": d["dimension"], "names": d.get("names")},
                               ensure_ascii=False) + "\n")
            # every other text field too (review formats-2: connectives and NOT semantics were left out of the view)
            f.write(json.dumps({"id": d["id"] + ".connectives", "connectives": d.get("connectives"),
                                "not_semantics": d.get("not_semantics")}, ensure_ascii=False) + "\n")
    out["codebooks/lexicon.json"] = p
    return out


def main(which=None):
    files = {f"wordings/{n}": HERE / "wordings" / n for n in ("family_pools.jsonl", "public_pools.jsonl")}
    files.update({f"locales/{n}": HERE / "locales" / n for n in (
        "spelling_us_gb.jsonl", "vocab_us_gb.jsonl", "date_formats.jsonl", "time_formats.jsonl",
        "number_formats.jsonl", "currencies.jsonl", "units.jsonl")})
    files["codebooks/codebooks.jsonl"] = HERE / "codebooks" / "codebooks.jsonl"
    files.update(views())
    files.update({f"records/{s}.jsonl": HERE / "records" / f"{s}.jsonl"
                  for s in ("xed", "mams_acsa", "mams_atsa", "ghc", "edos")})
    if which:
        files = {k: v for k, v in files.items() if any(w in k for w in which)}
    res = {}
    for key, path in files.items():
        tag = key.replace("/", "__")
        out = SD / f"{tag}.sealedqc.jsonl"
        summ = SD / f"{tag}.summary.json"
        cmd = [PY, str(CHECKER), str(path), "--id-field", "id", "--out", str(out), "--summary", str(summ),
               "--workers", "4"]
        if key.startswith("records/"):
            cmd += ["--skip-fields", "norm_sha256,loose_sha256,flags,source_file,split,dataset,scheme"]
        p = subprocess.run(cmd, capture_output=True, text=True)
        if p.returncode not in (0, 3):
            raise SystemExit(f"checker failed on {key}: rc {p.returncode}")
        s = json.load(open(summ))
        if s.get("suite_sha256") != SUITE:
            raise SystemExit(f"checker suite sha mismatch on {key}")
        hits, kinds = [], Counter()
        n = 0
        with open(out) as f:
            for line in f:
                r = json.loads(line)
                n += 1
                kn = lambda k: k.get("kind") if isinstance(k, dict) else k  # noqa: E731
                if r.get("hit"):
                    hk = [kn(k) for k in r.get("hit_kinds") or []]
                    hits.append({"id": r["id"], "kinds": hk})
                    kinds.update(hk)
                for k in r.get("report_kinds") or []:
                    kinds["report:" + kn(k)] += 1
        res[key] = {"rows": n, "hits": len(hits), "hit_ids": hits, "kinds": dict(kinds),
                    "input_sha256": sha_file(path), "checker_sha256": s.get("checker_sha256")}
        print(f"{key}: rows {n} hits {len(hits)} kinds {dict(kinds)}")
    prev = {}
    hp = SD / "hits.json"
    if which and hp.exists():
        prev = json.load(open(hp))
    prev.update(res)
    json.dump(prev, open(hp, "w"), indent=1)
    progress("run_sealed: " + "; ".join(f"{k} {v['rows']} rows / {v['hits']} hits" for k, v in res.items()))


if __name__ == "__main__":
    main(sys.argv[1:] or None)
