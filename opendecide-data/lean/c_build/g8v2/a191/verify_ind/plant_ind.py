"""Independent verifier re-plant (A19.1 b): F5, one cue x seed, written without run_power.py.
Uses only g8_aflite's TOKEN / THE_RX / SENT_RX / plant_uniforms. Gold-yes rows only; labels unchanged."""
import json, sys, hashlib, os, shutil, re
from pathlib import Path
LEAN = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
sys.path.insert(0, str(LEAN / "c_src/common")); sys.dont_write_bytecode = True
import g8_aflite as G8
cue, seed, d = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
W = Path(__file__).resolve().parent / f"F5_{cue}_s{seed}"; src = LEAN / "c_src/F5/out"
for sub in ("out", "qc", "tmp/chk"):
    (W / sub).mkdir(parents=True, exist_ok=True)
def apply(r):
    if cue == "token":
        r["state"] = r["state"].rstrip() + " " + G8.TOKEN; return True
    if cue == "repeat":
        ss = [x for x in G8.SENT_RX.split(" ".join(r["state"].split())) if x.strip()]
        if not ss: return False
        r["state"] = r["state"].rstrip() + " " + ss[-1]; return True
    if cue == "swap":
        q = [s for line in r["instructions"].strip().split("\n") for s in G8.SENT_RX.split(line) if "?" in s]
        for s in q:
            if G8.THE_RX.search(s):
                r["instructions"] = r["instructions"].replace(s, G8.THE_RX.sub("this", s, count=1), 1); return True
        return False
rec = {}
for nm in ("qc_sample", "candidates_r1"):
    raw = (src / f"{nm}.jsonl").read_text().splitlines()
    rows = [json.loads(l) for l in raw]
    part = [i for i, r in enumerate(rows) if r["qtype"] == "noul"]
    u = G8.plant_uniforms(len(part), "yes_no", cue, seed)
    marked, elig, yes = [], 0, 0
    out = list(raw)
    for a, i in enumerate(part):
        r = json.loads(raw[i])
        if int(r["gold"]) != 1: continue
        yes += 1
        if not apply(r): continue
        elig += 1
        if u[a] < d:
            out[i] = json.dumps(r, ensure_ascii=False); marked.append(r["id"])
    (W / "out" / f"{nm}.jsonl").write_text("\n".join(out) + "\n")
    for p in src.glob(f"{nm}.*"):
        t = W / "out" / p.name
        if p.name != f"{nm}.jsonl" and not t.exists(): os.symlink(p, t)
    # check: planted rows differ only in the cue field, labels identical
    chg = [(json.loads(a), json.loads(b)) for a, b in zip(raw, out) if a != b]
    assert all(x["gold"] == y["gold"] and x["id"] == y["id"] for x, y in chg)
    flds = {k for x, y in chg for k in x if x[k] != y[k]}
    rec[nm] = dict(n=len(rows), yes=yes, elig=elig, marked=len(marked), frac=round(len(marked) / max(elig, 1), 4),
                   changed_fields=sorted(flds), sha1=hashlib.sha1("\n".join(marked).encode()).hexdigest())
q = LEAN / "c_src/F5/qc"
for f in ("g6.py", "g7.py"): shutil.copyfile(q / f, W / "qc" / f)
lib = (q / "qc_lib.py").read_text()
lib = lib.replace('OUT = F5 / "out"', f'OUT = Path("{W}/out")').replace('QC = F5 / "qc"', f'QC = Path("{W}/qc")').replace('TMP = F5 / "tmp/chk"', f'TMP = Path("{W}/tmp/chk")')
(W / "qc" / "qc_lib.py").write_text(lib)
json.dump(rec, open(W / "plant_ind.json", "w"), indent=1); print(json.dumps(rec))
