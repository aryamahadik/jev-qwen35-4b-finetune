"""r2_vision.py: T10 image fast path on the L4 (200-image pack = 100 Pets + 100 VQA yes/no; both views of the choice items).

  r2_vision.py --name T10_native --port 30010 --arms native:1,native:1,native:8,native:8 [--conc-note ...]
  arm syntax  <kind>:<concurrency>   kind = native | exact (client-side resize to the processor's exact target size, PIL bicubic)

Reuses oc1.vision (the 17 Oct harness: prompts, candidate ids, smart_resize arithmetic, scoring). Agreement between arms is
the argmax agreement on the same 200 items; native-vs-native (same server, same concurrency, second pass) is the NOISE FLOOR;
native c1 vs native c8 shows whether concurrency matters. Numbers only; no image or prompt content is printed.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import pathlib
import sys
import threading
import time
from pathlib import Path

_o = pathlib.Path.exists


def _s(self, *a, **k):
    try:
        return _o(self, *a, **k)
    except PermissionError:
        return False


pathlib.Path.exists = _s
H = Path.home()
W = H / "opt_r2"
for p in (str(H / "lean" / "hosting"), str(H / "lean"), str(W)):
    sys.path.insert(0, p)
from oc1 import common as C  # noqa: E402
from oc1 import vision as V  # noqa: E402
from oc1.measure import GpuSampler  # noqa: E402


def prepare(path: Path, kind: str):
    from PIL import Image
    if kind == "native":
        im = Image.open(path)
        im.load()
        h0, w0 = im.size[1], im.size[0]
        h, w = V.smart_resize(h0, w0)
        return path.read_bytes(), (h0, w0), V.visual_tokens(h, w)
    if kind == "exact":
        im = Image.open(path).convert("RGB")
        w0, h0 = im.size
        h, w = V.smart_resize(h0, w0)
        if (h, w) != (h0, w0):
            im = im.resize((w, h), Image.BICUBIC)
        buf = io.BytesIO()
        im.save(buf, format="PNG")
        return buf.getvalue(), (h, w), V.visual_tokens(h, w)
    raise SystemExit(kind)


def run_arm(client_factory, items, pack, kind, conc, warm=6):
    for it in items[:warm]:
        b, hw, pt = prepare(pack / it["image"], kind)
        try:
            V.post_item(client_factory(), it, b, pt)
        except Exception:  # noqa: BLE001
            pass
    recs = [None] * len(items)
    nxt = [0]
    lock = threading.Lock()
    tl = threading.local()

    def cl():
        if getattr(tl, "c", None) is None:
            tl.c = client_factory()
        return tl.c

    def worker():
        while True:
            with lock:
                i = nxt[0]
                nxt[0] += 1
            if i >= len(items):
                return
            it = items[i]
            t0 = time.perf_counter()
            b, hw, pt = prepare(pack / it["image"], kind)
            prep_ms = (time.perf_counter() - t0) * 1000.0
            try:
                r = V.post_item(cl(), it, b, pt)
                p = r["probs"]
                recs[i] = {"id": it["id"], "suite": it["suite"], "ok": True, "pred": max(range(len(p)), key=p.__getitem__),
                           "correct": int(max(range(len(p)), key=p.__getitem__) == it["gold"]), "probs": p, "ms": r["ms"],
                           "prep_ms": prep_ms, "token_mismatch": r["token_mismatch"]}
            except Exception as e:  # noqa: BLE001
                recs[i] = {"id": it["id"], "suite": it["suite"], "ok": False, "err": f"{type(e).__name__}: {str(e)[:80]}"}

    t_start = time.perf_counter()
    th = [threading.Thread(target=worker) for _ in range(conc)]
    for t in th:
        t.start()
    for t in th:
        t.join()
    wall = time.perf_counter() - t_start
    return recs, wall


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--port", type=int, required=True)
    ap.add_argument("--arms", default="native:1,native:1,native:8,native:8")
    ap.add_argument("--ref", default="", help="results dir name whose arm 0 predictions are the reference for agreement")
    a = ap.parse_args()
    if a.port == 30000:
        raise SystemExit("refusing port 30000 (production)")
    import httpx
    pack = W / "data" / "vision_pack"
    items = C.read_jsonl(pack / "items.jsonl")
    out_dir = W / "results" / a.name
    out_dir.mkdir(parents=True, exist_ok=True)
    mk = lambda: httpx.Client(base_url=f"http://127.0.0.1:{a.port}", timeout=300.0)  # noqa: E731
    res = {"name": a.name, "n_items": len(items), "arms": []}
    with GpuSampler(0.5) as gs:
        for k, spec in enumerate(a.arms.split(",")):
            kind, conc = spec.split(":")
            t0w = time.time()
            recs, wall = run_arm(mk, items, pack, kind, int(conc))
            good = [r for r in recs if r["ok"]]
            arm = {"k": k, "kind": kind, "conc": int(conc), "n_ok": len(good), "errors": len(recs) - len(good),
                   "acc": round(100 * sum(r["correct"] for r in good) / max(1, len(good)), 2),
                   "ms": C.summarize([r["ms"] for r in good]), "prep_ms": C.summarize([r["prep_ms"] for r in good]),
                   "wall_s": round(wall, 2), "items_per_s": round(len(good) / wall, 3),
                   "token_mismatches": sum(r["token_mismatch"] for r in good), "gpu": gs.between(t0w, time.time()),
                   "preds": [r.get("pred") for r in recs]}
            res["arms"].append(arm)
            print(f"[{a.name}] arm{k} {kind}:{conc} acc {arm['acc']} p50 {arm['ms'].get('p50')} p95 {arm['ms'].get('p95')} "
                  f"items/s {arm['items_per_s']} mism {arm['token_mismatches']} err {arm['errors']}", flush=True)
    base = res["arms"][0]["preds"]
    for arm in res["arms"]:
        n = sum(1 for x, y in zip(arm["preds"], base) if x is not None and y is not None)
        arm["agree_with_arm0"] = round(sum(1 for x, y in zip(arm["preds"], base) if x is not None and x == y) / max(1, n), 4)
    (out_dir / "vision.json").write_text(json.dumps(res, indent=1))
    print(json.dumps({"arms": [{k: v for k, v in x.items() if k in ("k", "kind", "conc", "acc", "agree_with_arm0")} for x in res["arms"]]}))


if __name__ == "__main__":
    main()
