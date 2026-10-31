"""symmetrise.py: A42-D item 10, symmetrised serving of yes/no items and its adoption checks. CPU only.

Served estimate (10.1):  p = 1/2 [ p(q) + 1 - p(flip q) ]  on yes/no items that have a program-made flip; the cached
prefix is shared at serving. The flip is a DETERMINISTIC PROGRAM from the trained negation catalogue of item 7
(c2_build/negtwins/); no Claude call happens at test time. Items without a program flip are served unsymmetrised.

Interface (so this file does not depend on the catalogue's final shape):
  Flipper.flip(item: dict) -> dict | None     item has "id" and "instruction"; returns the flipped item (a complement twin:
                                              gold(flip) = 1 - gold(item)) with "id" = id + "::flip", or None (no flip).
  CatalogueFlipper wraps negtwins.core (split_instruction, apply, build_catalogue): complement patterns of the TRAINED
  catalogue only (held-out patterns are never used for serving, 10.3), tried in a fixed order (frameless FAIL_TO / LACK
  first, then FRAME_NOT, NEG_FRAME, LEX_PAIR; ties by pattern id). Which pattern is "the" flip is a serving choice of the
  orchestrator: pass a different order with order=... or your own Flipper.

Adoption (10.2), on dev = the G-proxy + the 150 complement pairs built from HELD-OUT negation patterns (<= 5 pairs per
pattern, none of them in the trained catalogue, 10.3). Adopt only if ALL hold:
  (1) complement violation falls by >= 0.02 (violation = share of pairs (q, not-q) answered the same way);
  (2) no loss on BOTH the G-proxy and the D1 yes/no rows: accuracy change (sym - plain) >= 0 and calibrated Brier change <= 0
      (temperature fitted per mode on the "calib" records when given, else T = 1 and the report says so);
  (3) D9: p50 latency of the symmetrised path <= 1.05 x C1's p50 (spec 7.2 c7). If it fails, it is not adopted.
If adopted the candidate is "C2 + symmetrisation": one served path, frozen with item 9 (10.4).

  symmetrise.py make-flips --items in.jsonl --out flips.jsonl [--no-flip-out nf.json]    (reads: run flips.jsonl as items)
  symmetrise.py adopt --records recs.jsonl --latency lat.json --out ADOPT.json [--catalogue-pids pids.json]
records.jsonl: {"id","set": "gproxy"|"d1_yesno"|"pair"|"calib", "gold": 0|1, "p": p(yes), "p_flip": p(yes) of the flip or
  null, "pair_id", "role": "q"|"nq", "pattern_id"}  (a "pair" row's p_flip is the program flip of THAT row's question)
latency.json: {"c1_p50_ms": x, "sym_p50_ms": y}
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[1]
OP_ORDER = ("FAIL_TO", "LACK", "FRAME_NOT", "NEG_FRAME", "LEX_PAIR")
VIOL_DROP, D9_RATIO, MAX_PER_PATTERN = 0.02, 1.05, 5
EPS = 1e-6


def sym_p(p: float, p_flip: float | None) -> float:
    return p if p_flip is None else 0.5 * (p + 1.0 - p_flip)


class Flipper:
    def flip(self, item: dict):  # pragma: no cover - interface
        raise NotImplementedError


class CatalogueFlipper(Flipper):
    def __init__(self, lex: dict | None = None, order=OP_ORDER, pairs: dict | None = None):
        sys.path.insert(0, str(LEAN / "c2_build"))
        from negtwins import checks, core
        self.core, self.checks, self.pairs = core, checks, pairs or {}
        cat = [p for p in core.build_catalogue(lex) if p.relation == "complement" and not p.held_out]
        self.patterns = sorted(cat, key=lambda p: (order.index(p.op) if p.op in order else 99, bool(p.frame), p.pid))

    def flip(self, item: dict):
        """The program flip of a yes/no item. Real dev / G-proxy rows carry the question under "instructions" (the test
        fixtures under "instruction"); both are read, and the flip keeps the key it found. A row with a card gets the
        card the trained catalogue exchanges for a complement (negtwins.checks.twin_card, the T37b swap rule); a pattern
        whose card cannot be exchanged is skipped, so a flip never pairs a negated question with the base's card."""
        key = "instructions" if "instructions" in item else "instruction"
        sp = self.core.split_instruction(item.get(key, "") or "")
        if sp is None:
            return None
        pre, core_q = sp
        card = item.get("card")
        for p in self.patterns:
            try:
                twin, _ = self.core.apply(core_q, p, self.pairs)
            except Exception:  # noqa: BLE001 - a pattern that cannot parse this question simply does not apply
                continue
            if not twin:
                continue
            new_card = card
            if (card or "").strip():
                new_card = self.checks.twin_card(card, p.relation)
                if new_card is None:
                    continue
            out = {**item, "id": f"{item['id']}::flip", key: pre + twin, "flip_of": item["id"], "flip_pattern": p.pid}
            if "card" in item:
                out["card"] = new_card
            if "gold" in item and p.relation == "complement" and str(item["gold"]) in ("0", "1"):
                out["gold"] = type(item["gold"])(1 - int(item["gold"])) if not isinstance(item["gold"], str) else str(1 - int(item["gold"]))
            return out
        return None


def make_flips(items: list, flipper: Flipper) -> tuple:
    flips, none = [], []
    for it in items:
        f = flipper.flip(it)
        (flips if f else none).append(f if f else it["id"])
    return flips, none


# ------------------------------------------------------------------------------------------------ metrics
def clip(p: float) -> float:
    return min(1 - EPS, max(EPS, p))


def temper(p: float, T: float) -> float:
    p = clip(p)
    return 1 / (1 + math.exp(-math.log(p / (1 - p)) / T))


def brier(ps: list, ys: list, T: float = 1.0) -> float:
    return sum((temper(p, T) - y) ** 2 for p, y in zip(ps, ys)) / len(ps)


def fit_T(ps: list, ys: list) -> float:
    grid = [0.5 + 0.05 * i for i in range(51)]
    return min(grid, key=lambda T: (brier(ps, ys, T), T))


def served(r: dict, sym: bool) -> float:
    return sym_p(r["p"], r.get("p_flip")) if sym else r["p"]


def accuracy(rows: list, sym: bool) -> float:
    return sum((served(r, sym) > 0.5) == (r["gold"] == 1) for r in rows) / len(rows)


def violation(rows: list, sym: bool) -> tuple:
    by = defaultdict(dict)
    for r in rows:
        by[r["pair_id"]][r["role"]] = r
    full = [v for v in by.values() if "q" in v and "nq" in v]
    return (sum((served(v["q"], sym) > 0.5) == (served(v["nq"], sym) > 0.5) for v in full) / len(full) if full else None,
            len(full))


def check_pairs(rows: list, trained_pids: set | None) -> list:
    p, per = [], Counter()
    seen = set()
    for r in rows:
        if r["pair_id"] not in seen:
            seen.add(r["pair_id"])
            per[r.get("pattern_id")] += 1
    p += [f"pattern {k!r}: {v} pairs > {MAX_PER_PATTERN}" for k, v in per.items() if v > MAX_PER_PATTERN]
    if None in per:
        p.append("a pair has no pattern_id")
    if trained_pids is not None:
        p += [f"pair pattern {k!r} is in the trained catalogue (10.3: held-out patterns only)" for k in per if k in trained_pids]
    return p


def adopt(records: list, latency: dict, trained_pids: set | None = None) -> dict:
    S = defaultdict(list)
    for r in records:
        S[r["set"]].append(r)
    need = [k for k in ("gproxy", "d1_yesno", "pair") if not S[k]]
    if need:
        return {"adopt": False, "problems": [f"no records for {need}"]}
    calib = S.get("calib") or []
    T = {}
    for mode, sym in (("plain", False), ("sym", True)):
        T[mode] = fit_T([served(r, sym) for r in calib], [r["gold"] for r in calib]) if calib else 1.0
    out, probs = {"temperature": T, "calibrated": bool(calib)}, check_pairs(S["pair"], trained_pids)
    v0, npair = violation(S["pair"], False)
    v1, _ = violation(S["pair"], True)
    out["pairs"] = npair
    out["violation"] = {"plain": v0, "sym": v1, "drop": None if v0 is None else round(v0 - v1, 6), "needed": VIOL_DROP}
    ok = {"violation_drop": v0 is not None and v0 - v1 >= VIOL_DROP - 1e-12}
    for name in ("gproxy", "d1_yesno"):
        rows, ys = S[name], [r["gold"] for r in S[name]]
        da = accuracy(rows, True) - accuracy(rows, False)
        db = brier([served(r, True) for r in rows], ys, T["sym"]) - brier([served(r, False) for r in rows], ys, T["plain"])
        out[name] = {"n": len(rows), "flipped": sum(r.get("p_flip") is not None for r in rows),
                     "acc_change": round(da, 6), "brier_change": round(db, 6)}
        ok[f"{name}_acc"], ok[f"{name}_brier"] = da >= -1e-12, db <= 1e-12
    c1, sy = latency.get("c1_p50_ms"), latency.get("sym_p50_ms")
    out["d9"] = {"c1_p50_ms": c1, "sym_p50_ms": sy, "ratio": None if not (c1 and sy) else round(sy / c1, 4), "max": D9_RATIO}
    ok["d9_latency"] = bool(c1 and sy and sy <= D9_RATIO * c1)
    out["checks"], out["problems"] = ok, probs
    out["adopt"] = all(ok.values()) and not probs
    out["name"] = "C2 + symmetrisation" if out["adopt"] else "C2 (plain; symmetrisation not adopted)"
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("make-flips")
    m.add_argument("--items", required=True)
    m.add_argument("--out", required=True)
    m.add_argument("--no-flip-out", default=None)
    d = sub.add_parser("adopt")
    d.add_argument("--records", required=True)
    d.add_argument("--latency", required=True)
    d.add_argument("--out", required=True)
    d.add_argument("--catalogue-pids", default=None)
    a = ap.parse_args(argv)
    if a.cmd == "make-flips":
        items = [json.loads(x) for x in Path(a.items).read_text().splitlines() if x.strip()]
        flips, none = make_flips(items, CatalogueFlipper())
        Path(a.out).write_text("".join(json.dumps(f) + "\n" for f in flips))
        if a.no_flip_out:
            Path(a.no_flip_out).write_text(json.dumps(none))
        print(json.dumps({"items": len(items), "flipped": len(flips), "no_flip": len(none)}))
        return 0
    recs = [json.loads(x) for x in Path(a.records).read_text().splitlines() if x.strip()]
    pids = set(json.loads(Path(a.catalogue_pids).read_text())) if a.catalogue_pids else None
    res = adopt(recs, json.loads(Path(a.latency).read_text()), pids)
    Path(a.out).write_text(json.dumps(res, indent=2))
    print(json.dumps({k: res.get(k) for k in ("adopt", "name", "checks", "problems")}))
    return 0 if res["adopt"] else 1


if __name__ == "__main__":
    sys.exit(main())
