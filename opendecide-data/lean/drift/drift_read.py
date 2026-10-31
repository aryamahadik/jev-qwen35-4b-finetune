"""Option-order drift test on DEV choice rows only (never OHS). Reads one adapter on every choice row of the dev
splits under a seeded ROTATION of the options (k in 1..n-1, like the OHS-3 recipe's rotated twins):
  rot      : the rotated view, single read            -> compare with the identity read (preds_<s>/<name>_parity)
  rot_tta  : the rotated view + its reversal, averaged -> compare with the identity TTA read (preds_<s>/<name>_tta)
Writes <out>/<name>__<split>__<view>.jsonl ({"id", "probs"} keyed by original option names). Imports decoder_io
read-only from --lean; writes nothing into it."""
import argparse, hashlib, json, random, sys, time
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--lean", required=True)
ap.add_argument("--name", required=True)
ap.add_argument("--base", required=True)
ap.add_argument("--revision", required=True)
ap.add_argument("--splits", default="dev,dev_claims,dev_nc,dev_negwords,devp_card,devzs,hard_dev,pg_dev,taskbank_dev")
ap.add_argument("--out", required=True)
ap.add_argument("--seed", default="drift20260930")
a = ap.parse_args()
sys.path.insert(0, a.lean)
import decoder_io  # noqa: E402

out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
decoder_io.STYLE = "cygnet"
t0 = time.time()
model, tok = decoder_io.load(a.base, "cuda", adapter=str(Path(a.lean) / "models" / a.name), revision=a.revision)
model = model.merge_and_unload(); model.eval()
print(json.dumps({"loaded": a.name, "sec": round(time.time() - t0), "layout": decoder_io.LAYOUT,
                  "load": decoder_io.LOAD_INFO}, default=str), flush=True)


def rot(r):
    n = len(r["options"])
    rng = random.Random(int.from_bytes(hashlib.sha256(f"{a.seed}:{r['id']}".encode()).digest()[:8], "big"))
    k = rng.randint(1, n - 1)
    return [(j + k) % n for j in range(n)]


for s in a.splits.split(","):
    rows = [json.loads(l) for l in open(Path(a.lean) / "data" / f"{s}.jsonl")]
    rows = [r for r in rows if r["qtype"] == "choice" and len(r["options"]) >= 2]
    perms = [rot(r) for r in rows]
    for view, kw in (("rot", {}), ("rot_tta", {"tta_choice": True, "tta_noul": False})):
        t = time.time()
        P = decoder_io.predict(model, tok, rows, dev="cuda", perms=perms, **kw)
        with open(out / f"{a.name}__{s}__{view}.jsonl", "w") as f:
            for r, p in zip(rows, P):
                f.write(json.dumps({"id": r["id"], "probs": p}) + "\n")
        print(f"{s} {view}: {len(rows)} rows in {time.time() - t:.0f}s", flush=True)
print("DONE", round(time.time() - t0), flush=True)
