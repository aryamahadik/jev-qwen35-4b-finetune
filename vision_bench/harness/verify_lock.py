"""Compare the rebuilt suites in data/<suite>/ with the bench's data.lock.json (image_cases.jsonl entry).
Same fingerprint as the bench's data_lock.py (formula copied, bench code not run): SHA-256 over each case as canonical JSON
plus '<image path> <sha256 of the file>' lines, in order. The bench path images/<suite>/<n>.<ext> is read from
data/<suite>/images/<n>.<ext>.
Run:  .venv/bin/python -I harness/verify_lock.py
"""
import hashlib
import json
import os

ROOT = "/Users/aryamahadik/Documents/jev/vision_bench"
LOCK = f"{ROOT}/src/system-one-bench/data.lock.json"
SUITES = ["img_sst2", "img_ar_sentiment", "img_pets", "img_vqa_yesno", "img_count"]


def images(x):
    if isinstance(x, dict) and set(x) == {"image"}:
        yield x["image"]
    elif isinstance(x, dict):
        for v in x.values():
            yield from images(v)
    elif isinstance(x, list):
        for v in x:
            yield from images(v)


def local(suite, p):
    return f"{ROOT}/data/{suite}/images/{os.path.basename(p)}"


def fp(suite):
    h, n, img_ok = hashlib.sha256(), 0, 0
    for line in open(f"{ROOT}/data/{suite}/cases.jsonl", encoding="utf-8"):
        c = json.loads(line)
        h.update(json.dumps(c, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode() + b"\n")
        for p in images(c):
            f = local(suite, p)
            sha = hashlib.sha256(open(f, "rb").read()).hexdigest() if os.path.exists(f) else "missing"
            h.update(f"{p} {sha}\n".encode())
        n += 1
    return n, h.hexdigest()


def case_only_fp(suite):
    """Hash of the case JSON alone (items, instructions, options, gold), without image bytes: isolates item/gold identity."""
    h = hashlib.sha256()
    for line in open(f"{ROOT}/data/{suite}/cases.jsonl", encoding="utf-8"):
        c = json.loads(line)
        h.update(json.dumps(c, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode() + b"\n")
    return h.hexdigest()


if __name__ == "__main__":
    lock = json.load(open(LOCK))["image_cases.jsonl"]["suites"]
    for s in SUITES:
        n, got = fp(s)
        want = lock[s]
        print(f"{s:18s} n={n} want_n={want['n']} full_hash_match={got == want['sha256']} got={got[:12]} want={want['sha256'][:12]}")
