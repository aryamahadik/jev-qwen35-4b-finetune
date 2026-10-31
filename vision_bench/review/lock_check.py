"""Fingerprint our five suites with the bench's OWN data_lock.fingerprint (loaded by path, read in full beforehand) and compare to data.lock.json."""
import importlib.util, json, os, sys
R = "/Users/aryamahadik/Documents/jev/vision_bench"
FP = f"{R}/review/tmp/fp"
import shutil; shutil.rmtree(FP, ignore_errors=True); os.makedirs(f"{FP}/images")
S = ["img_sst2", "img_ar_sentiment", "img_pets", "img_vqa_yesno", "img_count"]
with open(f"{FP}/image_cases.jsonl", "w") as out:
    for s in S:
        os.symlink(f"{R}/data/{s}/images", f"{FP}/images/{s}")
        out.write(open(f"{R}/data/{s}/cases.jsonl", encoding="utf-8").read())
spec = importlib.util.spec_from_file_location("bench_data_lock", f"{R}/src/system-one-bench/data_lock.py")
dl = importlib.util.module_from_spec(spec); spec.loader.exec_module(dl)
os.chdir(FP)
got = dl.fingerprint("image_cases.jsonl")["suites"]
lock = json.load(open(dl.LOCK))["image_cases.jsonl"]
for s in S:
    print(s, "n", got[s]["n"], "hash equals data.lock.json:", got[s] == lock["suites"][s])
print("lock suites:", sorted(lock["suites"]), "| lock total sha:", lock["sha256"][:16])
print("results_vision.json data_sha256 of Jev 1.14/1.13 starts 9fcf4def08b3c6b1:", lock["sha256"].startswith("9fcf4def08b3c6b1"))
# total over all 6 suites needs img_refcoco (not rebuilt): recompute with the lock's own refcoco entry
tot = dl.total({**{s: got[s] for s in S}, "img_refcoco": lock["suites"]["img_refcoco"]})
print("total hash with our 5 suites + the lock's refcoco entry == lock total:", tot == lock["sha256"])
# ids / gold sanity
import collections
for s in S:
    cs = [json.loads(l) for l in open(f"{R}/data/{s}/cases.jsonl", encoding="utf-8")]
    ids = [c["id"] for c in cs]
    q = next(iter(cs[0]["questions"].values()))
    ncrit = len(q["criteria"]) if q.get("criteria") else 2
    gl = collections.Counter(str(next(iter(c["gold"].values()))["label"]) for c in cs)
    print(s, "ids unique:", len(set(ids)) == 200, "ids", ids[0], "..", ids[-1], "n_options", ncrit, "gold label counts (top 4):", gl.most_common(4))
