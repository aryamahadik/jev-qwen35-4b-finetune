"""Build raw rows for clickbait17 (Webis Clickbait Corpus 2017; Potthast et al., ECIR 2018 / Clickbait Challenge 2017).

Source : Zenodo record 5530410 (Webis-Clickbait-17, deposited by the Webis group), files
         clickbait17-train-170331.zip (2,459 posts) and clickbait17-train-170630.zip (19,538 posts; the challenge's
         public "validation" release, folder clickbait17-validation-170630). The test release
         clickbait17-test-170720.zip (the benchmark test set, evaluated on TIRA) is NEVER downloaded or read.
         Only the two members instances.jsonl and truth.jsonl are pulled out of each zip with HTTP range requests
         (the zips are ~1 GB of images); the Zenodo md5 of each zip and the sha256 of each extracted member are pinned.
Licence: CC BY 4.0 (Zenodo record metadata "license": "cc-by-4.0", https://zenodo.org/records/5530410).
Texts  : tweets posted by 27 major US news publishers (Nov 2016 - Jun 2017), human-written.
Labels : five Amazon Mechanical Turk annotators per post rated it on a 4-point scale: not (0.0), slightly (0.33),
         considerably (0.66) or heavily (1.0) clickbaiting (truthJudgments). No model labels.
Soft   : per-annotator binarisation: an annotator votes "yes" iff their rating is considerably/heavily (>= 0.66);
         soft = {"yes": votes/5, "no": 1 - votes/5}.
Gold   : clear majorities only: yes = at least 4 of 5 annotators voted clickbait, no = at most 1 of 5 did; the rows must
         also agree with the official truthClass (mean >= 0.5). 3/5 and 2/5 posts are dropped (a read of 3/5 posts
         found plain news headlines such as "Renters outnumber owners in half of U.S. cities" labelled clickbait).
Cleaning: HTML entities unescaped ("&amp;" -> "&") and URLs removed (review fix, 29 Sep); empty posts, posts under
         4 words, posts that are only a URL/handle, exact and near-duplicate posts
         (word 5-gram Jaccard >= 0.7) dropped; decontaminated against our data, label-NLI and JevBench public.
Balance: yes share 0.36 (all clear clickbait posts are used; clear non-clickbait fills the rest). Deterministic (seed 20261101).
"""
import collections
import hashlib
import html
import io
import json
import random
import re
import zipfile

import requests

import _cal_common as C

KEY = "clickbait17"
MAX_ROWS = 8000
YES_SHARE = 0.36
RECORD = "5530410"
ZIPS = {  # zip name -> (zenodo md5 of the whole zip, {member: sha256})
    "clickbait17-train-170331.zip": ("md5:738075eaf9c4d3af9c16808f5d16ce00", {
        "clickbait17-train-170331/instances.jsonl": None,
        "clickbait17-train-170331/truth.jsonl": None}),
    "clickbait17-train-170630.zip": ("md5:8f074f3f035393b81a559bfc8bd9a467", {
        "clickbait17-validation-170630/instances.jsonl": None,
        "clickbait17-validation-170630/truth.jsonl": None}),
}
PINS = json.loads((C.HERE / "pins_clickbait17.json").read_text()) if (C.HERE / "pins_clickbait17.json").exists() else {}
URL = "https://zenodo.org/api/records/{rec}/files/{name}/content"
LICENCE = ("CC BY 4.0 (Zenodo record https://zenodo.org/records/5530410 metadata 'license: cc-by-4.0'; "
           "Webis Clickbait Corpus 2017, deposited by the Webis group)")
DATASET = "Webis-Clickbait-17 (Zenodo 5530410): clickbait17-train-170331 + clickbait17-train-170630 (never the test release)"
CACHE = C.CACHE / KEY

Q = "Is this news-publisher tweet clickbait, written to lure readers into clicking rather than to inform them?"
DEFS = {
    "yes": "At least 4 of 5 annotators rated the post considerably or heavily clickbaiting: it teases or withholds the "
           "key fact ('this', 'here's why', 'you won't believe'), exaggerates, or baits curiosity so the reader must "
           "click to learn what it is about.",
    "no": "At most 1 of 5 annotators rated it considerably or heavily clickbaiting: the post states its news "
          "informatively (who did what), so a reader learns the point without clicking; an emotive topic, a quote or "
          "a mild question alone does not make it clickbait.",
}


class HttpFile(io.RawIOBase):
    """Seekable read-only view of a remote file through HTTP range requests (used to read single zip members)."""

    def __init__(self, url):
        self.url, self.s = url, requests.Session()
        r = self.s.head(url, allow_redirects=True, timeout=120)
        r.raise_for_status()
        self.size, self.pos = int(r.headers["content-length"]), 0

    def seekable(self):
        return True

    def readable(self):
        return True

    def tell(self):
        return self.pos

    def seek(self, off, whence=0):
        self.pos = off if whence == 0 else self.pos + off if whence == 1 else self.size + off
        return self.pos

    def readinto(self, b):
        if self.pos >= self.size:
            return 0
        end = min(self.pos + len(b), self.size) - 1
        for _ in range(5):
            r = self.s.get(self.url, headers={"Range": f"bytes={self.pos}-{end}"}, timeout=300)
            if r.status_code == 206:
                break
        r.raise_for_status()
        data = r.content
        b[:len(data)] = data
        self.pos += len(data)
        return len(data)


def fetch_members():
    CACHE.mkdir(parents=True, exist_ok=True)
    pins = dict(PINS)
    out = {}
    for zname, (md5, members) in ZIPS.items():
        need = [m for m in members if not (CACHE / m).exists()]
        if need:
            url = URL.format(rec=RECORD, name=zname)
            meta = requests.get(f"https://zenodo.org/api/records/{RECORD}", timeout=120).json()
            got = {f["key"]: f["checksum"] for f in meta["files"]}
            assert got[zname] == md5, (zname, got.get(zname), md5)
            z = zipfile.ZipFile(io.BufferedReader(HttpFile(url), buffer_size=1 << 22))
            for m in need:
                (CACHE / m).parent.mkdir(parents=True, exist_ok=True)
                with z.open(m) as src, open(CACHE / m, "wb") as dst:
                    dst.write(src.read())
        for m in members:
            h = C.sha256(CACHE / m)
            if m in pins:
                assert pins[m] == h, f"sha256 mismatch {m}: {h} != {pins[m]}"
            else:
                pins[m] = h
                print("PIN", m, h)
            out[m] = h
    if pins != PINS:
        (C.HERE / "pins_clickbait17.json").write_text(json.dumps(pins, indent=1) + "\n")
    return out


def load():
    recs = {}
    for zname, (_, members) in ZIPS.items():
        folder = sorted(members)[0].split("/")[0]
        inst = {}
        with open(CACHE / folder / "instances.jsonl") as f:
            for line in f:
                o = json.loads(line)
                inst[o["id"]] = o
        with open(CACHE / folder / "truth.jsonl") as f:
            for line in f:
                t = json.loads(line)
                o = inst[t["id"]]
                recs[t["id"]] = (o, t, folder)
    return recs


BAD = re.compile(r"^(\W|@\w+|#\w+|https?://\S+)*$")
URLS = re.compile(r"https?:/*\S*")  # also truncated links ("http:/", "https:")


def main():
    rng = random.Random(C.SEED)
    shas = fetch_members()
    recs = load()
    print("records:", len(recs))
    cands = {"yes": [], "no": []}
    drop = collections.Counter()
    for pid in sorted(recs):
        o, t, folder = recs[pid]
        text = C.clean(URLS.sub("", html.unescape(" ".join(o["postText"]))))
        if not text or BAD.match(text) or len(C.words(text)) < 4:
            drop["short/empty"] += 1
            continue
        j = t["truthJudgments"]
        if len(j) != 5:
            drop["not5"] += 1
            continue
        votes = sum(x >= 0.66 for x in j)
        if votes >= 4 and t["truthClass"] == "clickbait":
            gold = "yes"
        elif votes <= 1 and t["truthClass"] == "no-clickbait":
            gold = "no"
        else:
            drop["unclear(2-3 of 5 or class mismatch)"] += 1
            continue
        cands[gold].append((pid, text, votes, t, folder))
    print("candidates:", {k: len(v) for k, v in cands.items()}, "dropped:", dict(drop))

    core = {pid: [text] for g in cands for pid, text, *_ in cands[g]}
    hits = C.decon(core, KEY)
    hits.update(C.cross_v14(core, {KEY}, exact_min=3))  # short posts too: 170331 re-uses Webis-16 tweets
    for g in cands:
        cands[g] = [c for c in cands[g] if c[0] not in hits]

    # clearest first within each label (unanimous before 4/5 or 1/5), random order inside a tier
    for g in cands:
        rng.shuffle(cands[g])
        cands[g].sort(key=lambda c: -abs(c[2] - 2.5))
    nd = C.NearDup(thr=0.7)
    n_yes_target = int(MAX_ROWS * YES_SHARE)
    picked = {"yes": [], "no": []}
    for g, target in (("yes", n_yes_target), ("no", MAX_ROWS - n_yes_target)):
        for c in cands[g]:
            if len(picked[g]) >= target:
                break
            if nd.seen(c[1]):
                continue
            picked[g].append(c)
    # keep the yes share at YES_SHARE if yes ran short
    ny = len(picked["yes"])
    nn = min(len(picked["no"]), int(ny * (1 - YES_SHARE) / YES_SHARE))
    picked["no"] = picked["no"][:nn]

    folder_zip = {sorted(m)[0].split("/")[0]: z for z, (_, m) in ZIPS.items()}
    rows = []
    for g in ("yes", "no"):
        for pid, text, votes, t, folder in picked[g]:
            e = None
            if C.neg_count(text):
                e = "negation"
            elif C.NUM.search(text):
                e = "numeric"
            elif C.QUANT.search(text):
                e = "quantifier"
            rows.append({
                "key": KEY, "rid": f"cb17-{pid}", "state": text, "instructions": Q, "options": C.YN, "gold": g,
                "soft": C.soft_yes(votes, 5),
                "meta": {"dataset": DATASET, "config": folder, "revision": f"zenodo:{RECORD} ({ZIPS[folder_zip[folder]][0]}; member "
                         f"sha256 {shas[folder + '/instances.jsonl'][:16]}.., {shas[folder + '/truth.jsonl'][:16]}..)",
                         "licence": LICENCE, "split": "train",
                         "orig_label": {"truthJudgments": [round(x, 2) for x in t["truthJudgments"]],
                                        "truthClass": t["truthClass"], "votes_ge_0.66": votes},
                         "family": C.FAMILY, "edge": e},
            })
    rng.shuffle(rows)
    defs = {None: DEFS}
    C.write_outputs(KEY, rows, defs)
    st = C.summary(KEY, rows)
    C.show_samples(rows, 5)
    C.append_manifest(C.manifest_record(
        KEY, DATASET, LICENCE, rows, "yesno",
        "Soft = share of the 5 MTurk annotators rating the post considerably/heavily clickbaiting (>= 0.66 on the "
        "0/0.33/0.66/1 scale). Gold only for clear majorities (>= 4/5 yes, <= 1/5 no) that agree with truthClass; "
        "2/5-3/5 posts dropped. Test release never read. Near-dup + decon (local data, label-NLI, JevBench, other v14).",
        st))


if __name__ == "__main__":
    main()
