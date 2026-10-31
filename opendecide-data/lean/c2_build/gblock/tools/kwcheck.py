"""Hash-level check of candidate source names / hosts against the OHS-4 sealed keyword hashes (FORMAT.md rule).
Prints only which candidate keys hit (no hash detail is meaningful beyond that)."""
import hashlib, json, re, sys
from urllib.parse import urlsplit
KW = sys.argv[1]; CAND = sys.argv[2]
H = {json.loads(l)["hash"] for l in open(KW) if l.strip()}
STRIP = ".,;:!?\"'()[]{}<>"
def runs(text):
    t = re.sub(r"\s+", " ", text.strip().lower()).split(" ")
    for i in range(len(t)):
        for n in range(1, 9):
            if i + n <= len(t):
                s = " ".join(t[i:i + n]).strip(STRIP)
                if len(s) >= 4:
                    yield s
def hosts(u):
    h = urlsplit(u if "//" in u else "//" + u).netloc.lower()
    out = {h}
    out.add(h[4:] if h.startswith("www.") else "www." + h)
    return out
c = json.load(open(CAND))
res = {}
for k, v in c.items():
    strs = [v.get("name", "")] + list(v.get("names", [])) + list(v.get("domains", [])) + [v.get("url", "")]
    cand = set()
    for s in strs:
        if not s: continue
        cand |= set(runs(s))
        if "." in s: cand |= hosts(s)
    hit = sorted(x for x in cand if hashlib.sha256(x.encode()).hexdigest() in H)
    res[k] = len(hit)
print(json.dumps(res))
