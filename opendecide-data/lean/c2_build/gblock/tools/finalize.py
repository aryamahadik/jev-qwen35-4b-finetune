"""Final pass: cross-domain duplicate check, audit-file sync (audit rows only for kept texts), schema check, summary.
Usage: python -I finalize.py"""
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/gblock/tools")
import common as C  # noqa: E402

G = C.ROOT
KEYS = ["text_id", "domain", "source", "licence_url", "text"]


def norm(t):
    return " ".join(re.findall(r"[^\W_]+", unicodedata.normalize("NFKC", t).lower()))


def main():
    seen, summary, problems = {}, {}, []
    for d in sorted(p for p in (G / "texts").iterdir() if p.is_dir()):
        rows = [json.loads(l) for l in open(d / "texts.jsonl") if l.strip()]
        keep = []
        for r in rows:
            if list(r.keys()) != KEYS:
                problems.append(f"{r.get('text_id')}: keys {list(r.keys())}")
            wc = C.nwords(r["text"])
            if not (C.MIN_W <= wc <= C.MAX_W):
                problems.append(f"{r['text_id']}: {wc} words")
            if C.pii_reason(r["text"]):
                problems.append(f"{r['text_id']}: pii {C.pii_reason(r['text'])}")
            h = hashlib.sha1(norm(r["text"]).encode()).hexdigest()
            if h in seen:
                problems.append(f"{r['text_id']}: duplicate of {seen[h]} (dropped)")
                continue
            seen[h] = r["text_id"]
            keep.append(r)
        if len(keep) != len(rows):
            with open(d / "texts.jsonl", "w") as f:
                for r in keep:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
        ids = {r["text_id"] for r in keep}
        ap = G / "audit" / f"{d.name}_meta.jsonl"
        arows = [json.loads(l) for l in open(ap) if l.strip()]
        arows = [a for a in arows if a["text_id"] in ids]
        with open(ap, "w") as f:
            for a in arows:
                f.write(json.dumps(a, ensure_ascii=False) + "\n")
        wc = sorted(C.nwords(r["text"]) for r in keep)
        st = json.loads((d / "build_stats.json").read_text())
        summary[d.name] = {"texts": len(keep), "source": keep[0]["source"] if keep else None,
                           "licences": dict(Counter(r["licence_url"] for r in keep).most_common(3)),
                           "words_min_med_max": [wc[0], wc[len(wc) // 2], wc[-1]] if wc else None,
                           "audit_rows": len(arows), "build": {k: v for k, v in st.items()
                                                               if k not in ("domain", "source", "licence_url")}}
    out = {"domains": len(summary), "texts_total": sum(v["texts"] for v in summary.values()),
           "per_domain": summary, "problems": problems}
    (G / "checks" / "summary.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(json.dumps({"domains": out["domains"], "texts_total": out["texts_total"],
                      "per_domain": {k: v["texts"] for k, v in summary.items()}, "problems": problems[:20],
                      "n_problems": len(problems)}, indent=1))


if __name__ == "__main__":
    main()
