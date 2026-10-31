"""Build raw rows for clickbait16 (Webis Clickbait Corpus 2016; Potthast et al., ECIR 2016).

Source : Zenodo record 3251557 (deposited by the Webis group), corpus-webis-clickbait-16.zip (md5 from the record and
         sha256 pinned): problems/<id>/<id>.json (tweet as returned by the Twitter API) and truth/annotator{A,B,C}.csv.
Licence: CC BY 4.0 (Zenodo record metadata "license": "cc-by-4.0", https://zenodo.org/records/3251557).
Texts  : 2,992 tweets from the top-20 news publishers on Twitter (2014-2015), human-written.
Labels : three independent annotators judged every tweet on a 4-point scale (none / weak / medium / strong
         clickbait); the README discretises medium/strong as a clickbait vote. No split -> train.
Soft   : share of the 3 annotators voting clickbait (medium or strong).
Gold   : unanimous tweets only (3/3 yes, 0/3 no); 2-vs-1 tweets are dropped.
State  : the tweet text (the retweeted text for retweets); HTML entities unescaped; t.co links removed; tweets under 4 words dropped.
Balance: yes share ~0.42. Deterministic (seed 20261101).
"""
import collections
import html
import json
import random
import re
import zipfile

import _cal_common as C

KEY = "clickbait16"
URL = "https://zenodo.org/api/records/3251557/files/corpus-webis-clickbait-16.zip/content"
ZIP_SHA = "ceb6d5ed977968552c911bf0968bf3125efe9846091c75ef387a43a74b9a3f55"
ZIP_MD5 = "md5:7ae5a128350eecbcbad182ade4f42585"
LICENCE = ("CC BY 4.0 (Zenodo record https://zenodo.org/records/3251557 metadata 'license: cc-by-4.0'; Webis Clickbait "
           "Corpus 2016, deposited by the Webis group)")
DATASET = "Webis-Clickbait-16 (Zenodo 3251557), three annotators per tweet"
CACHE = C.CACHE / KEY
YES_SHARE = 0.42

Q = "Is this news-publisher tweet clickbait, written to lure readers into clicking rather than to inform them?"
DEFS = {
    "yes": "All 3 annotators rated the tweet medium or strong clickbait: it teases or withholds the key fact ('this', "
           "'here's why', 'you won't believe'), exaggerates, or baits curiosity so the reader must click to learn "
           "what it is about.",
    "no": "None of the 3 annotators rated it medium or strong clickbait: the tweet states its news informatively (who "
          "did what), so a reader learns the point without clicking; an emotive topic, a quote or a mild question "
          "alone does not make it clickbait.",
}
URLS = re.compile(r"https?:/*\S*")  # also truncated links ("http:/", "https:")


def main():
    rng = random.Random(C.SEED)
    z = C.fetch(URL, CACHE / "corpus-webis-clickbait-16.zip", ZIP_SHA)
    votes = collections.defaultdict(dict)
    tweets = {}
    with zipfile.ZipFile(z) as zf:
        for a in "ABC":
            for line in zf.read(f"webis-clickbait-16/truth/annotator{a}.csv").decode().splitlines():
                if line.strip():
                    tid, lab = line.split(",")[:2]
                    votes[tid][a] = lab.strip()
        for n in zf.namelist():
            if n.startswith("webis-clickbait-16/problems/") and n.endswith(".json"):
                t = json.loads(zf.read(n))
                src = t.get("retweeted_status") or t
                tweets[str(t["id_str"])] = (src.get("text", ""), t.get("user", {}).get("screen_name", ""))
    cands = {"yes": [], "no": []}
    drop = collections.Counter()
    for tid in sorted(votes):
        v = votes[tid]
        if len(v) != 3 or tid not in tweets:
            drop["incomplete"] += 1
            continue
        k = sum(x in ("medium", "strong") for x in v.values())
        text = C.clean(URLS.sub("", html.unescape(tweets[tid][0])))
        if len(C.words(text)) < 4:
            drop["short"] += 1
            continue
        if k == 3:
            cands["yes"].append((tid, text, k, v))
        elif k == 0:
            cands["no"].append((tid, text, k, v))
        else:
            drop["split_vote"] += 1
    print("candidates:", {g: len(x) for g, x in cands.items()}, "dropped:", dict(drop))
    core = {tid: [text] for g in cands for tid, text, _, _ in cands[g]}
    hits = C.decon(core, KEY)
    hits.update(C.cross_v14(core, {KEY}))
    nd = C.NearDup(thr=0.7)
    picked = {}
    for g in ("yes", "no"):
        rng.shuffle(cands[g])
        picked[g] = []
        for c in cands[g]:
            if c[0] in hits or nd.seen(c[1]):
                continue
            picked[g].append(c)
    ny = len(picked["yes"])
    picked["no"] = picked["no"][:int(ny * (1 - YES_SHARE) / YES_SHARE)]
    rows = []
    for g in ("yes", "no"):
        for tid, text, k, v in picked[g]:
            e = None
            if C.neg_count(text):
                e = "negation"
            elif C.NUM.search(text):
                e = "numeric"
            rows.append({
                "key": KEY, "rid": f"cb16-{tid}", "state": text, "instructions": Q, "options": C.YN, "gold": g,
                "soft": C.soft_yes(k, 3),
                "meta": {"dataset": DATASET, "config": "truth/annotator{A,B,C}.csv",
                         "revision": f"zenodo:3251557 ({ZIP_MD5}; zip sha256 {ZIP_SHA})", "licence": LICENCE,
                         "split": "train", "orig_label": {"annotators": v}, "family": C.FAMILY, "edge": e},
            })
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, {None: DEFS})
    st = C.summary(KEY, rows)
    C.show_samples(rows, 5)
    C.append_manifest(C.manifest_record(
        KEY, DATASET, LICENCE, rows, "yesno",
        "Soft = share of the 3 annotators rating the tweet medium/strong clickbait (README discretisation). Only "
        "unanimous tweets kept (soft 1.0/0.0); complements clickbait17 (2014-15 tweets, different annotators).", st))


if __name__ == "__main__":
    main()
