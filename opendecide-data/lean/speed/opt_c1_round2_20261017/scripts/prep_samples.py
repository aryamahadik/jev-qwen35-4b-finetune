"""Mac: pick 500 utterances per set (seeded random, after the Open-ASR-leaderboard filters) and write 16 kHz flac + manifest.
usage: prep_samples.py <set> ; sets: ls_clean ls_other tedlium ami earnings22 slurp
Outputs under assets/samples/<set>/{manifest.jsonl, audio/<id>.flac}. Manifest rows: id, ref (raw), ref_norm, dur_s (no audio text elsewhere)."""
import sys, os, glob, json, random
import pyarrow.parquet as pq, soundfile as sf, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from r2common import *
A = os.path.join(os.path.dirname(__file__), "..", "assets")
S = sys.argv[1]; N = int(os.environ.get("N", 500)); SEED = int(os.environ.get("SEED", 20261017)); OUTNAME = os.environ.get("OUTNAME", S)
files = {
  "ls_clean": f"{A}/data/oasr/librispeech/test.clean-*.parquet", "ls_other": f"{A}/data/oasr/librispeech/test.other-*.parquet",
  "ami": f"{A}/data/oasr/ami/test-*.parquet", "earnings22": f"{A}/data/oasr/earnings22/test-*.parquet",
  "tedlium": f"{A}/data/tedlium/data/test-*.parquet", "slurp": f"{A}/data/slurp/data/test-*.parquet"}[S]
fl = sorted(glob.glob(files)); assert fl, files
out = f"{A}/samples/{OUTNAME}"; os.makedirs(out + "/audio", exist_ok=True)

def meta_rows():
    """(file_idx, row_idx, id, text) without decoding audio."""
    rows = []
    for fi, f in enumerate(fl):
        cols = pq.ParquetFile(f).schema_arrow.names
        tcol = "text" if "text" in cols else ("transcript" if "transcript" in cols else "sentence")
        idc = "id"
        t = pq.read_table(f, columns=[c for c in [idc, tcol] if c in cols])
        ids = t.column(idc).to_pylist(); tx = t.column(tcol).to_pylist()
        for ri, (i, x) in enumerate(zip(ids, tx)):
            rows.append((fi, ri, str(i), x))
    return rows

rows = meta_rows()
def keep(r):
    t = r[3] or ""
    if S == "tedlium":
        if "ignore_time_segment_in_scoring" in t or "inter_segment_gap" in r[2]:
            return False
    if S != "slurp":
        if not norm_text(clean(t)).strip():
            return False
    return True
def clean(t):
    if S == "tedlium":
        t = t.replace(" '", "'").replace("<unk>", "").replace("  ", " ").strip()
    return t
rows = [r for r in rows if keep(r)]
print(S, "eligible rows", len(rows))
rng = random.Random(SEED)
if S == "slurp":   # one random recording per distinct utterance id, then 500 distinct utterances
    by = {}
    for r in rows:
        by.setdefault(r[2], []).append(r)
    ids = sorted(by); rng.shuffle(ids)
    pick = [rng.choice(by[i]) for i in ids[:N]]
else:
    pick = rng.sample(rows, N)
pick.sort()
man = []
for fi in sorted({p[0] for p in pick}):
    pf = pq.ParquetFile(fl[fi]); t = pf.read()
    d = {(p[1]): p for p in pick if p[0] == fi}
    cols = t.schema.names
    for ri in sorted(d):
        a = t.column("audio")[ri].as_py()
        x = decode_audio(a)
        uid = f"{OUTNAME}_{fi}_{ri}"
        sf.write(f"{out}/audio/{uid}.flac", x, SR, subtype="PCM_16")
        raw = d[ri][3]
        rec = {"uid": uid, "src_id": d[ri][2], "ref": clean(raw), "ref_norm": "" if S == "slurp" else norm_text(clean(raw)), "dur_s": round(len(x) / SR, 3)}
        if S == "slurp":
            rec["intent"] = t.column("intent")[ri].as_py()
        man.append(rec)
with open(f"{out}/manifest.jsonl", "w") as f:
    for m in man:
        f.write(json.dumps(m) + "\n")
print(S, "wrote", len(man), "utts,", round(sum(m["dur_s"] for m in man) / 3600, 2), "h audio")
