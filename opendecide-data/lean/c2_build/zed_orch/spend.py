"""Estimated Anthropic API spend for the Zed orchestration thread and all of its subagent threads (read-only).

Token counts come from Zed's local threads.db. Prices are ASSUMED list prices per 1M tokens (input, output); cache
writes are 1.25x input and cache reads 0.1x input. Calibrate with CALIBRATION (console $ / estimate) when the owner
reports the real console number.
"""
import json, sqlite3, sys, zstandard
from collections import defaultdict
DB = "/Users/aryamahadik/Library/Application Support/Zed/threads/threads.db"
ROOT = sys.argv[1] if len(sys.argv) > 1 else "01e71618-d54d-4929-8250-005267193512"
PRICES = {"opus": (5.0, 25.0), "sonnet": (3.0, 15.0), "haiku": (1.0, 5.0)}
CALIBRATION = 0.54  # owner 15 Oct ~09:00 UTC: $38 left when raw was ~$301 -> real $162 (x0.538)
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
rows = con.execute("select id, parent_id, data from threads").fetchall()
kids = defaultdict(list)
data = {}
for tid, pid, blob in rows:
    kids[pid].append(tid)
    data[tid] = blob
def walk(t):
    yield t
    for k in kids.get(t, []):
        yield from walk(k)
dz = zstandard.ZstdDecompressor()
tot = defaultdict(lambda: defaultdict(int))
n_threads = defaultdict(int)
for t in walk(ROOT):
    d = json.loads(dz.decompress(data[t], max_output_size=500_000_000))
    model = ((d.get("model") or {}).get("model") or "unknown")
    fam = next((f for f in PRICES if f in model), "opus")
    n_threads[fam] += 1
    for k, v in (d.get("cumulative_token_usage") or {}).items():
        tot[fam][k] += v
grand = 0.0
for fam, u in tot.items():
    pin, pout = PRICES[fam]
    usd = (u["input_tokens"] * pin + u["output_tokens"] * pout + u["cache_creation_input_tokens"] * pin * 1.25
           + u["cache_read_input_tokens"] * pin * 0.1) / 1e6 * CALIBRATION
    grand += usd
    print(f"{fam:7s} threads={n_threads[fam]:4d} out={u['output_tokens']:>11,} cache_w={u['cache_creation_input_tokens']:>12,} "
          f"cache_r={u['cache_read_input_tokens']:>14,} est=${usd:8.2f}")
print(f"TOTAL estimated spend ${grand:.2f} (assumed list prices x{CALIBRATION})")
