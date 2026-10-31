"""Self-test of the exclusion index: a known bench / pin segment must hit, a one-token-dropped copy must hit, an UCI tweet must not."""
import gzip, json, random, sys
sys.path.insert(0, ".")
from sb5_lib import *
segs = []
for l in gzip.open(SB5 / "bench_pins/mteb__tweet_sentiment_multilingual/test/arabic.jsonl.gz", "rt", encoding="utf-8"):
    segs.append(json.loads(l)["text"])
ix = Index()
for s in segs: ix.add("t", s)
rng = random.Random(1); pick = [s for s in segs if len(norm_tokens(s)) >= 8]; rng.shuffle(pick); pick = pick[:40]
exact = sum(bool(ix.hit(s)) for s in pick)
drop1 = sum(bool(ix.hit(" ".join(s.split()[1:]))) for s in pick)
neg = sum(bool(ix.hit(r["text"])) for r in load_archive())
out = {"pins_segments": len(segs), "probe": len(pick), "exact_hits": exact, "drop_first_token_hits": drop1, "uci_tweets_hit": neg}
json.dump(out, open(WORK / "exclusion_selftest.json", "w"), indent=1); print(out)
