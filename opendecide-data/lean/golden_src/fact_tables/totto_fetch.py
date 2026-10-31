"""Fetch a deterministic sample of ToTTo TRAIN examples for build_totto.py (train member only).

https://storage.googleapis.com/totto-public/totto_data.zip (187,724,372 bytes, Last-Modified 2021-08-25, md5
bjQY6SdF32vX/jpTUBHfLg==) holds train, dev and unlabeled test; only the member totto_data/totto_train_data.jsonl is
read, with HTTP range requests (dev/test bytes are never downloaded). It is inflated in memory and checked against
the zip CRC-32; the sha256 of the inflated member is recorded. Kept: examples whose md5(example_id) % KEEP_MOD == 0,
with a non-empty final sentence and <= 60 table rows -> cache/totto/train_sample.jsonl.gz.
"""
import gzip
import hashlib
import io
import json
import struct
import zipfile
import zlib

import requests

from feverous_fetch import HttpFile
from ft_common import CACHE

URL = "https://storage.googleapis.com/totto-public/totto_data.zip"
SIZE = 187724372
MEMBER = "totto_data/totto_train_data.jsonl"
KEEP_MOD = 5
OUT = CACHE / "totto" / "train_sample.jsonl.gz"


def main():
    z = zipfile.ZipFile(io.BufferedReader(HttpFile(URL, SIZE), buffer_size=1 << 16))
    info = z.getinfo(MEMBER)
    s = requests.Session()
    hdr = s.get(URL, headers={"Range": f"bytes={info.header_offset}-{info.header_offset + 29}"}, timeout=60).content
    n_name, n_extra = struct.unpack("<HH", hdr[26:30])
    start = info.header_offset + 30 + n_name + n_extra
    r = s.get(URL, headers={"Range": f"bytes={start}-{start + info.compress_size - 1}"}, stream=True, timeout=600)
    r.raise_for_status()
    dec = zlib.decompressobj(-15)
    sha, crc, rest = hashlib.sha256(), 0, b""
    n = kept = 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(OUT, "wt", encoding="utf-8") as fo:
        def handle(ln):
            nonlocal n, kept
            if not ln.strip():
                return
            n += 1
            o = json.loads(ln)
            if int(hashlib.md5(str(o["example_id"]).encode()).hexdigest(), 16) % KEEP_MOD:
                return
            anns = o.get("sentence_annotations") or []
            if not anns or not anns[0].get("final_sentence", "").strip() or len(o["table"]) > 60:
                return
            fo.write(json.dumps(o, ensure_ascii=False) + "\n")
            kept += 1

        for chunk in r.iter_content(1 << 20):
            data = dec.decompress(chunk)
            sha.update(data)
            crc = zlib.crc32(data, crc)
            rest += data
            *lines, rest = rest.split(b"\n")
            for ln in lines:
                handle(ln)
        data = dec.flush()
        sha.update(data)
        crc = zlib.crc32(data, crc)
        rest += data
        for ln in rest.split(b"\n"):
            handle(ln)
    assert crc == info.CRC, (crc, info.CRC)
    meta = {"url": URL, "zip_size": SIZE, "member": MEMBER, "crc32": info.CRC, "file_size": info.file_size,
            "sha256_inflated": sha.hexdigest(), "keep_mod": KEEP_MOD, "examples": n, "kept": kept}
    (CACHE / "totto" / "member.json").write_text(json.dumps(meta, indent=1))
    print(meta)


if __name__ == "__main__":
    main()
