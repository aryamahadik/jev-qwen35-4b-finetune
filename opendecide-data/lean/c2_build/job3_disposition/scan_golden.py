"""JOB3 scan of the C1 golden training set: counts only. Streams golden_train.jsonl, finds choice/yes-no rows whose
option labels/definitions or question mention disposition/action vocabulary. Writes aggregate counts to JSON."""
import json, re, sys, collections
P = "/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/v14_parts/golden_train.jsonl"
WORDS = ["approve", "reject", "escalat", "human review", "human_review", "hold", "refund", "quarantine", "disposition",
         "observe", "continue", "stop", "proceed", "refuse", "block", "allow", "deny", "flag", "take action", "no action",
         "manual review", "pay", "decline", "cancel", "suspend", "revoke", "credential", "compromis", "invoice"]
rx = {w: re.compile(r"\b" + re.escape(w), re.I) for w in WORDS}
src_tot = collections.Counter()
hit = collections.defaultdict(collections.Counter)      # word -> source -> rows (card text or question)
lab = collections.defaultdict(collections.Counter)      # source -> option label words
n = 0
for line in open(P):
    r = json.loads(line); n += 1
    s = r["source"]; src_tot[s] += 1
    txt = (r.get("card") or "") + "\n" + (r.get("instructions") or "")
    for w, p in rx.items():
        if p.search(txt):
            hit[w][s] += 1
out = {"rows": n, "src_tot": src_tot, "hit": {w: dict(c) for w, c in hit.items()}}
json.dump(out, open("scan_golden_counts.json", "w"), indent=0)
print(n)
for w in WORDS:
    c = hit.get(w, {})
    print(w, sum(c.values()), len(c), c.most_common(5))
