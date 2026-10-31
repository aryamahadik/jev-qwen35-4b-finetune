"""Fetch only the FEVEROUS Wikipedia pages needed by build_feverous.py (train claims only).

The official page dump (https://fever.ai/download/feverous/feverous-wiki-pages.zip, 9.9 GB, Last-Modified
2022-04-28, 544 members FeverousWikiv1/wiki_NNN.jsonl) is read with HTTP range requests: the zip central directory is
parsed, and a seeded sample of N_MEMBERS members is streamed and inflated in memory. Only pages referenced by some
train claim's evidence are kept, in cache/feverous/pages_subset.jsonl.gz. Nothing else is written to disk.
Per member we record the zip CRC-32, the compressed size and the sha256 of the inflated bytes
(cache/feverous/members.json), so a re-run can be checked byte for byte.
"""
import gzip
import hashlib
import io
import json
import random
import re
import struct
import sys
import zipfile
import zlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

URL = "https://fever.ai/download/feverous/feverous-wiki-pages.zip"
ZIP_SIZE = 9906569155
SEED = 20261101
N_MEMBERS = 96
HERE = Path(__file__).resolve().parent
CACHE = HERE / "cache" / "feverous"
TRAIN = CACHE / "feverous_train_challenges.jsonl"
TRAIN_SHA = "0c29ccba41e27c5b988ca5132085e8d67c7921f265707bea170bfbde12bceee7"
ID_RE = re.compile(r"^(.*?)_(sentence|cell|header_cell|table_caption|item|section|title)(_|$)")


class HttpFile(io.RawIOBase):
    def __init__(self, url, size):
        self.url, self.size, self.pos = url, size, 0
        self.s = requests.Session()

    def seekable(self):
        return True

    def readable(self):
        return True

    def tell(self):
        return self.pos

    def seek(self, off, whence=0):
        self.pos = off if whence == 0 else (self.pos + off if whence == 1 else self.size + off)
        return self.pos

    def readinto(self, b):
        if self.pos >= self.size:
            return 0
        end = min(self.pos + len(b), self.size) - 1
        d = self.s.get(self.url, headers={"Range": f"bytes={self.pos}-{end}"}, timeout=120).content
        b[:len(d)] = d
        self.pos += len(d)
        return len(d)


def page_of(eid):
    m = ID_RE.match(eid)
    return m.group(1) if m else None


def needed_pages():
    assert hashlib.sha256(TRAIN.read_bytes()).hexdigest() == TRAIN_SHA
    need = set()
    with open(TRAIN) as f:
        next(f)  # header line of empty fields
        for line in f:
            d = json.loads(line)
            for ev in d["evidence"]:
                for eid in ev["content"]:
                    p = page_of(eid)
                    if p:
                        need.add(p)
                for ctx in ev["context"].values():
                    for eid in ctx:
                        p = page_of(eid)
                        if p:
                            need.add(p)
    return need


def stream_member(info, need):
    s = requests.Session()
    hdr = s.get(URL, headers={"Range": f"bytes={info.header_offset}-{info.header_offset + 29}"}, timeout=120).content
    assert hdr[:4] == b"PK\x03\x04"
    n_name, n_extra = struct.unpack("<HH", hdr[26:30])
    start = info.header_offset + 30 + n_name + n_extra
    end = start + info.compress_size - 1
    r = s.get(URL, headers={"Range": f"bytes={start}-{end}"}, stream=True, timeout=600)
    r.raise_for_status()
    dec = zlib.decompressobj(-15)
    sha = hashlib.sha256()
    crc = 0
    rest = b""
    kept = []
    for chunk in r.iter_content(1 << 20):
        data = dec.decompress(chunk)
        sha.update(data)
        crc = zlib.crc32(data, crc)
        rest += data
        *lines, rest = rest.split(b"\n")
        for ln in lines:
            if ln.strip():
                o = json.loads(ln)
                if o.get("title") in need:
                    kept.append(o)
    data = dec.flush()
    sha.update(data)
    crc = zlib.crc32(data, crc)
    rest += data
    for ln in rest.split(b"\n"):
        if ln.strip():
            o = json.loads(ln)
            if o.get("title") in need:
                kept.append(o)
    assert crc == info.CRC, (info.filename, crc, info.CRC)
    return info.filename, sha.hexdigest(), kept


def main():
    need = needed_pages()
    print(f"pages referenced by train evidence: {len(need)}", flush=True)
    z = zipfile.ZipFile(io.BufferedReader(HttpFile(URL, ZIP_SIZE), buffer_size=1 << 20))
    members = sorted((i for i in z.infolist() if i.filename.endswith(".jsonl")), key=lambda i: i.filename)
    assert len(members) == 544, len(members)
    rng = random.Random(SEED)
    chosen = sorted(rng.sample(members, N_MEMBERS), key=lambda i: i.filename)
    out = CACHE / "pages_subset.jsonl.gz"
    meta = {}
    n_pages = 0
    with ThreadPoolExecutor(max_workers=6) as ex, gzip.open(out, "wt", encoding="utf-8") as fo:
        for name, sha, kept in ex.map(lambda i: stream_member(i, need), chosen):
            info = next(i for i in chosen if i.filename == name)
            meta[name] = {"crc32": info.CRC, "compress_size": info.compress_size, "file_size": info.file_size,
                          "sha256_inflated": sha, "pages_kept": len(kept)}
            for o in kept:
                o["_member"] = name
                fo.write(json.dumps(o, ensure_ascii=False) + "\n")
            n_pages += len(kept)
            print(f"{name}: kept {len(kept)} pages (total {n_pages})", flush=True)
    (CACHE / "members.json").write_text(json.dumps({"url": URL, "zip_size": ZIP_SIZE, "seed": SEED,
                                                    "n_members": N_MEMBERS, "members": meta}, indent=1))
    print("done", n_pages)


if __name__ == "__main__":
    main()
