"""Names-only list of C1 training sources from golden_train.jsonl (fields source, meta.dataset, meta.hf_id)."""
import json, sys
from collections import Counter
p = sys.argv[1]; out = sys.argv[2]
c = Counter()
with open(p) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        m = r.get("meta") or {}
        for k, v in (("source", r.get("source")), ("meta.dataset", m.get("dataset")), ("meta.hf_id", m.get("hf_id"))):
            if isinstance(v, str) and v.strip():
                c[(k, v.strip())] += 1
names = sorted({v for (_, v) in c})
json.dump({"from": p, "fields": ["source", "meta.dataset", "meta.hf_id"], "n_names": len(names), "names": names},
          open(out, "w"), indent=1)
print(len(names))
