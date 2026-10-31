"""sym_reads.py: the q / flip-q reads and the latency run for symmetrised serving (PREREG A42-D 10). CPU except `latency`, which
only talks to a SGLang server that someone else started (it never starts, stops or restarts one).

symmetrise.py decides adoption from records {"id","set","gold","p","p_flip","pair_id","role","pattern_id"} and a latency record.
This file makes those inputs from the reads:

  items    the three dev sets and their program flips, staged OUTSIDE data/ (a new data/ dev file makes every G13 log stale):
             d1_yesno  the yes/no rows of the D1 full set (the 9 gate dev splits without gate_dev.CONSTRAINT_EXCLUDE)
             gproxy    every yes/no row of the G-proxy (bases and twins)
             pair      the 150 held-out-pattern complement pairs of the G-proxy (a = role q, b = role nq; 10.3: held-out patterns only)
           writes DIR/sym_flip.jsonl (the flip rows: read this as split `sym_flip`, od_gcp.py predict, same flags as the dev read),
           DIR/sym_items_manifest.json (counts, no-flip ids, shas, the flip order) and DIR/trained_pids.json (10.3 check).
           q is NOT read again: p(q) comes from the candidate's existing dev and G-proxy reads.
  records  joins the reads into records.jsonl (+ the calibration set, see --calib), refusing any missing prediction.
  latency  the D9 harness on the served path: plain (one sequence per decision) or sym (q and flip q in ONE /generate call, so the
           shared state prefix is cached), batch 1, p50 / p95 per decision. Run once against C1's server and once against the
           candidate's, then `latency-join` -> {"c1_p50_ms","sym_p50_ms"} for symmetrise.py adopt.
  latency-join --plain lat_c1.json --sym lat_sym.json --out latency.json

Which pattern is "the" serving flip is symmetrise.CatalogueFlipper's fixed order (FAIL_TO, LACK, FRAME_NOT, NEG_FRAME, LEX_PAIR,
frameless first): the flip is a deterministic program, no model call. Rows with a card get the card the trained catalogue exchanges
(negtwins.checks.twin_card); a pattern whose card cannot be exchanged is skipped; no flip = served unsymmetrised.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2B = HERE.parent
LEAN = C2B.parent
for _p in (str(HERE), str(C2B), str(LEAN)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import gate_dev as g  # noqa: E402
import symmetrise as sy  # noqa: E402

SPLITS9 = tuple(g.SPLITS.split(","))
FLIP_SPLIT = "sym_flip"
GPROXY_SPLIT = "pab_gproxy"
GP_ROWS, GP_REL = "data/c2_gproxy/pab_gproxy.jsonl", "data/c2_gproxy/pab_gproxy_relations.jsonl"


class Refused(Exception):
    pass


def guard(*paths) -> None:
    import c2io
    for p in paths:
        why = c2io.refusal(p) if p is not None else None
        if why:
            raise Refused(f"{p} refused: {why}")


def jsonl(p: Path) -> list:
    guard(p)
    try:
        return [json.loads(x) for x in Path(p).read_text().splitlines() if x.strip()]
    except OSError as e:
        raise Refused(f"cannot read {p} ({type(e).__name__})") from None


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def key_d1(split: str, rid: str) -> str:
    return f"d1|{split}|{rid}"


def key_gp(rid: str) -> str:
    return f"gp|{rid}"


def d1_rows(root: Path) -> list:
    """Yes/no rows of the D1 full set, id replaced by the set key (ids repeat across splits)."""
    out = []
    for sp in SPLITS9:
        for r in jsonl(Path(root) / "data" / f"{sp}.jsonl"):
            if r.get("qtype") == "noul" and r.get("source") not in g.CONSTRAINT_EXCLUDE:
                out.append({**r, "orig_id": r["id"], "split": sp, "id": key_d1(sp, r["id"]), "set": "d1_yesno"})
    return out


def gproxy_rows(root: Path) -> tuple:
    rows = [{**r, "orig_id": r["id"], "split": GPROXY_SPLIT, "id": key_gp(r["id"]), "set": "gproxy"}
            for r in jsonl(Path(root) / GP_ROWS) if r.get("qtype") == "noul"]
    rels = [x for x in jsonl(Path(root) / GP_REL) if x.get("type") == "complement"]
    return rows, rels


def trained_pids() -> list:
    from negtwins import core
    return sorted(p.pid for p in core.build_catalogue(None) if not p.held_out and not str(p.pid).startswith("H:"))


def build_items(root: Path, flipper) -> dict:
    d1, (gprows, rels) = d1_rows(root), gproxy_rows(root)
    ids = {r["id"] for r in gprows}
    bad = [x for x in rels if key_gp(x["a"]) not in ids or key_gp(x["b"]) not in ids]
    if bad:
        raise Refused(f"{len(bad)} pair(s) have an endpoint outside the G-proxy yes/no rows")
    flips, none = {}, []
    for r in [*d1, *gprows]:
        f = flipper.flip(r)
        if f is None:
            none.append(r["id"])
        else:
            flips[r["id"]] = f
    dup = [k for k in flips if flips[k]["id"] != k + "::flip"]
    if dup:
        raise Refused(f"flip ids are not <id>::flip for {dup[:2]}")
    return {"d1": d1, "gproxy": gprows, "pairs": rels, "flips": flips, "no_flip": none}


def write_items(root: Path, out_dir: Path, flipper=None) -> dict:
    out_dir = Path(out_dir)
    guard(out_dir, root)
    if (Path(root) / "data") in [out_dir, *out_dir.parents]:
        raise Refused("stage the flip rows outside data/ (a new data/ dev file makes the G13 logs stale)")
    flipper = flipper or sy.CatalogueFlipper()
    it = build_items(Path(root), flipper)
    flip_rows = [{**f, "split": FLIP_SPLIT} for f in it["flips"].values()]
    body = "".join(json.dumps(f, sort_keys=True) + "\n" for f in flip_rows)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "sym_flip.jsonl").write_text(body)
    (out_dir / "trained_pids.json").write_text(json.dumps(trained_pids()))
    pair_rows = sum(1 for x in it["pairs"] if key_gp(x["a"]) in it["flips"]) + sum(1 for x in it["pairs"] if key_gp(x["b"]) in it["flips"])
    man = {"what": "A42-D 10 symmetrisation: flip rows of the three dev sets (q is read from the existing reads)",
           "flip_order": list(sy.OP_ORDER), "sets": {"d1_yesno": len(it["d1"]), "gproxy": len(it["gproxy"]), "pair_rows": 2 * len(it["pairs"])},
           "flipped": {"d1_yesno": sum(r["id"] in it["flips"] for r in it["d1"]), "gproxy": sum(r["id"] in it["flips"] for r in it["gproxy"]),
                       "pair_rows": pair_rows},
           "pairs": len(it["pairs"]), "patterns": len({x.get("pattern") for x in it["pairs"]}),
           "no_flip_ids": len(it["no_flip"]), "flip_rows": len(flip_rows), "flip_file_sha256": sha_bytes(body.encode()),
           "flip_split": FLIP_SPLIT, "read": f"od_gcp.py predict --name <read name> ... --splits {FLIP_SPLIT} (push sym_flip.jsonl to ~/lean/data/ on the VM only)",
           "d1_definition": "noul rows of the 9 gate dev splits without " + ",".join(g.CONSTRAINT_EXCLUDE)}
    (out_dir / "sym_items_manifest.json").write_text(json.dumps(man, indent=1) + "\n")
    return man


# ------------------------------------------------------------------------------------------------ records
def p_yes(probs: dict) -> float:
    return float(probs["yes"])


def build_records(root: Path, name: str, items: dict, calib: str = "select") -> list:
    """records.jsonl for symmetrise.adopt from the reads of read name `name`."""
    root = Path(root)
    with_root = _AtRoot(root)
    with with_root:
        q = {sp: g.load(sp, name) for sp in (*SPLITS9, GPROXY_SPLIT)}
        fl = g.load(FLIP_SPLIT, name)
    miss = [sp for sp, v in q.items() if v is None]
    if miss or fl is None:
        raise Refused(f"no preds of {name} for {miss + ([FLIP_SPLIT] if fl is None else [])}")

    def pq(r):
        v = q[r["split"]].get(r["orig_id"])
        if v is None:
            raise Refused(f"{name}: no prediction for {r['id']}")
        return p_yes(v)

    def pf(r):
        f = items["flips"].get(r["id"])
        if f is None:
            return None
        v = fl.get(f["id"])
        if v is None:
            raise Refused(f"{name}: no flip-q prediction for {f['id']}")
        return p_yes(v)

    recs = []
    for r in items["d1"]:
        base = {"id": r["id"], "gold": int(r["gold"]), "p": pq(r), "p_flip": pf(r)}
        recs.append({**base, "set": "d1_yesno"})
        if calib == "select" and g.half(r["group_id"]) == "select":
            recs.append({**base, "set": "calib"})
    byid = {r["id"]: r for r in items["gproxy"]}
    for r in items["gproxy"]:
        recs.append({"id": r["id"], "set": "gproxy", "gold": int(r["gold"]), "p": pq(r), "p_flip": pf(r)})
    for x in items["pairs"]:
        for role, rid in (("q", x["a"]), ("nq", x["b"])):
            r = byid[key_gp(rid)]
            recs.append({"id": f"{x['pair_id']}|{role}", "set": "pair", "gold": int(r["gold"]), "p": pq(r), "p_flip": pf(r),
                         "pair_id": x["pair_id"], "role": role, "pattern_id": x.get("pattern")})
    return recs


class _AtRoot:
    def __init__(self, root):
        self.root, self.old = root, None

    def __enter__(self):
        self.old, g.ROOT = g.ROOT, self.root

    def __exit__(self, *a):
        g.ROOT = self.old


# ------------------------------------------------------------------------------------------------ latency
def percentile(xs: list, q: float) -> float:
    s = sorted(xs)
    if not s:
        raise ValueError("no samples")
    k = (len(s) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (k - lo)


def measure(read_fn, rows: list, flips: dict, mode: str, warmup: int = 20, clock=time.perf_counter) -> dict:
    """Per-decision wall time in ms at batch 1. `read_fn(list of rows)` is ONE server call for all its sequences.
    plain: read_fn([row]); sym: read_fn([row, flip]) when the row has a flip (one call, the prefix is shared), else read_fn([row])
    (an item without a program flip is served unsymmetrised, 10.1)."""
    if mode not in ("plain", "sym"):
        raise ValueError(mode)
    for r in rows[:warmup]:
        read_fn([r])
    ms, n_pair = [], 0
    for r in rows:
        batch = [r, flips[r["id"]]] if mode == "sym" and r["id"] in flips else [r]
        n_pair += len(batch) == 2
        t = clock()
        read_fn(batch)
        ms.append((clock() - t) * 1000.0)
    return {"mode": mode, "n": len(ms), "n_with_flip": n_pair, "warmup": min(warmup, len(rows)), "p50_ms": round(statistics.median(ms), 3),
            "p95_ms": round(percentile(ms, 0.95), 3), "mean_ms": round(statistics.fmean(ms), 3)}


def join_latency(plain: dict, sym: dict, tol: float = 0.0) -> dict:
    if plain.get("mode") != "plain" or sym.get("mode") != "sym":
        raise Refused("latency-join needs a plain record (C1) and a sym record (candidate)")
    if plain.get("items_sha256") != sym.get("items_sha256"):
        raise Refused("the two latency runs used different item sets")
    if plain.get("served_path") != sym.get("served_path") or not plain.get("served_path"):
        raise Refused("the two latency runs must name one served path (D9: same served path)")
    return {"c1_p50_ms": plain["p50_ms"], "sym_p50_ms": sym["p50_ms"], "ratio": round(sym["p50_ms"] / plain["p50_ms"], 4),
            "served_path": plain["served_path"], "plain": plain, "sym": sym}


def _vm_read_fn(port: int):  # pragma: no cover - needs the VM's SGLang server and fast_read
    import fast_read
    rd = fast_read.Reader(port, None, workers=1, chunk=8, views=1)
    return lambda rows: rd._read_chunk(rows)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=str(LEAN), help=argparse.SUPPRESS)
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("items")
    i.add_argument("--out-dir", default="c2_build/staged/P6-grid/sym")
    r = sub.add_parser("records")
    r.add_argument("--name", required=True, help="the read name of the chosen candidate")
    r.add_argument("--items-dir", default="c2_build/staged/P6-grid/sym")
    r.add_argument("--calib", choices=("select", "none"), default="select")
    r.add_argument("--out", required=True)
    la = sub.add_parser("latency")
    la.add_argument("--mode", choices=("plain", "sym"), required=True)
    la.add_argument("--items-dir", default="c2_build/staged/P6-grid/sym")
    la.add_argument("--port", type=int, default=30000)
    la.add_argument("--served-path", required=True, help="a label for the serving config hash, e.g. the S1 config sha256")
    la.add_argument("--limit", type=int, default=500)
    la.add_argument("--out", required=True)
    j = sub.add_parser("latency-join")
    j.add_argument("--plain", required=True)
    j.add_argument("--sym", required=True)
    j.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    root = Path(a.root)
    ab = lambda x: Path(x) if Path(x).is_absolute() else root / x  # noqa: E731
    try:
        if a.cmd == "items":
            man = write_items(root, ab(a.out_dir))
            print(json.dumps({k: man[k] for k in ("sets", "flipped", "pairs", "no_flip_ids", "flip_rows", "flip_file_sha256")}))
            return 0
        if a.cmd == "records":
            it = build_items(root, sy.CatalogueFlipper())
            recs = build_records(root, a.name, it, a.calib)
            guard(ab(a.out))
            ab(a.out).write_text("".join(json.dumps(x) + "\n" for x in recs))
            print(json.dumps({"records": len(recs)}))
            return 0
        if a.cmd == "latency":  # pragma: no cover
            it = build_items(root, sy.CatalogueFlipper())
            rows = [r for r in it["d1"] if r["id"] in it["flips"]][: a.limit]
            body = "".join(json.dumps(r["id"]) for r in rows).encode()
            res = measure(_vm_read_fn(a.port), rows, it["flips"], a.mode)
            res.update({"served_path": a.served_path, "items_sha256": sha_bytes(body), "port": a.port})
            guard(ab(a.out))
            ab(a.out).write_text(json.dumps(res, indent=1))
            print(json.dumps(res))
            return 0
        res = join_latency(json.loads(ab(a.plain).read_text()), json.loads(ab(a.sym).read_text()))
        guard(ab(a.out))
        ab(a.out).write_text(json.dumps(res, indent=1))
        print(json.dumps({k: res[k] for k in ("c1_p50_ms", "sym_p50_ms", "ratio")}))
        return 0
    except Refused as e:
        print(f"REFUSED: {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
