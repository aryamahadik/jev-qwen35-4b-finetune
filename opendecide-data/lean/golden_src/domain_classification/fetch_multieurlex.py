"""Stream coastalcph/multi_eurlex data/multi_eurlex.tar.gz (pinned revision) and keep only what the eurlex builder
needs: from train.jsonl ONLY the celex_id, the English text and the EuroVoc concept labels (dev/test are skipped
unread); any EuroVoc descriptor/name files are saved verbatim. The sha256 of the full archive is computed while
streaming and checked against the LFS oid of the pinned revision. Nothing else is written to disk."""
import hashlib
import json
import sys
import tarfile
from pathlib import Path

import requests

REV = "2020d0350241461069a54177b639f0e6c7a7a712"
LFS_SHA = "3a2195bc01c7aea0e302bc7af94f2f55f0c15cdeabfe4e086c083196069a2e83"
OUT = Path(__file__).resolve().parent / "cache" / "eurlex"


class HashReader:
    def __init__(self, raw):
        self.raw, self.h, self.n = raw, hashlib.sha256(), 0

    def read(self, n=-1):
        b = self.raw.read(n)
        self.h.update(b)
        self.n += len(b)
        return b


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    url = f"https://huggingface.co/datasets/coastalcph/multi_eurlex/resolve/{REV}/data/multi_eurlex.tar.gz"
    with requests.get(url, stream=True, timeout=600) as r:
        r.raise_for_status()
        r.raw.decode_content = False
        hr = HashReader(r.raw)
        with tarfile.open(fileobj=hr, mode="r|gz") as tf:
            for m in tf:
                print("member:", m.name, m.size, flush=True)
                base = Path(m.name).name
                if not m.isfile():
                    continue
                if base == "train.jsonl":
                    f = tf.extractfile(m)
                    n = 0
                    with open(OUT / "train_en.jsonl", "w") as out:
                        for line in f:
                            d = json.loads(line)
                            out.write(json.dumps({"celex_id": d["celex_id"], "text": d["text"].get("en"),
                                                  "eurovoc_concepts": d["eurovoc_concepts"]}, ensure_ascii=False) + "\n")
                            n += 1
                    print("train docs:", n, flush=True)
                elif base.endswith(".json") and m.size < 50_000_000:
                    (OUT / base).write_bytes(tf.extractfile(m).read())
                # dev.jsonl / test.jsonl: skipped unread
        while hr.read(1 << 20):
            pass
    sha = hr.h.hexdigest()
    print("archive bytes:", hr.n, "sha256:", sha)
    (OUT / "archive_sha256.txt").write_text(sha + "\n")
    if sha != LFS_SHA:
        sys.exit("sha256 mismatch vs LFS oid")


if __name__ == "__main__":
    main()
