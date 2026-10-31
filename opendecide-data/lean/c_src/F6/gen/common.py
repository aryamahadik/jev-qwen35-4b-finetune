"""F6 generator: shared paths, pinned inputs, seeds, progress logging and small helpers (no labels, no rendering).

Binding: G0_SPEC.md rev 8 (frozen, sha256 below), C_DATA_SPEC v4, C_TRAIN_RECIPE v4, PREREG A15 / A16 / A16.1.
Every number in the structures is an int (day numbers, whole smallest units); no float anywhere.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import random
import sys
from pathlib import Path

F6 = Path(__file__).resolve().parents[1]                      # lean/c_src/F6
CSRC = F6.parent                                              # lean/c_src
LEAN = CSRC.parent                                            # lean
GEN = F6 / "gen"
OUT = F6 / "out"
TMP = F6 / "tmp"
FMT1 = CSRC / "formats" / "formats-1"
FMT2 = CSRC / "formats" / "formats-2"
COMMON = CSRC / "common"
PACKS = CSRC / "packs"
PROGRESS = LEAN / "c_build" / "progress_phase2.log"
SPEC = F6 / "G0_SPEC.md"
SPEC_SHA256 = "cd5b79ac0f6fe39e288ff1b47d6f08776ec5f377b45587294a542252e97f57d2"
SPEC_ID = "F6.G0.rev8"
GEN_VERSION = "F6-gen v2.0 (repair r1)"
BASE_SEED = 20261003
SOURCE = "c_f6"
FAMILY = "F6"
LICENCE = "CC0 1.0 (program-generated)"
PINNED = {  # named inputs, read at these sha256s (generator task; A16.1)
    "negcount.py": "79368f465d438617cb64fb57e69c236893b5f686a7bbb6ffd34e7184c40a8091",
    "markers.json": "893e206860de6dde35d82a2e6d49f00ee6f1f8bd492fe71da494953071126b78",
    "denylist.py": "e268d5667f181bbab47428df2b8e2ee6126a5091dc93e12b0a5f7acd09d6e1c6",
}
SEALED_SUITE_SHA256 = "f4ae863720535b6ba27acad51917fe07b4d31344228a1dddb9d98bc3a4deac68"
PY = "/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python"
TOKEN_CAP = 1900          # G0 s1: every F6 row <= 1,900 real tokens, instructions counted twice (A16.1 (g))
TOKEN_CAP_A22 = 7900      # PREREG A22 (6 Oct; tmp/repair/INFEASIBLE_length.md): a unit that fails the 1,900 cap on
A22_ROUND = 7             # every redraw of rounds 0-6 is redrawn from round 7 on under the A16 hard cap (7,900), so
                          # every G0 share and option bucket is kept; the mixer enforces the mix-level long-row cap

for p in (str(FMT1), str(COMMON), str(LEAN), str(GEN.parent)):
    if p not in sys.path:
        sys.path.insert(0, p)


def now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def progress(msg: str) -> None:
    line = f"{now()} [F6] {msg}"
    with open(PROGRESS, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line, flush=True)


def h64(*parts) -> int:
    return int.from_bytes(hashlib.sha256("\x1f".join(str(p) for p in parts).encode()).digest()[:8], "big")


def rng_for(*parts) -> random.Random:
    return random.Random(h64(BASE_SEED, *parts))


def unit(*parts) -> float:
    return h64(*parts) / 2 ** 64


def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def write_jsonl(path, rows) -> int:
    n = 0
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
            n += 1
    return n


def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


def check_pins() -> dict:
    got = {k: sha256_file(COMMON / k) for k in PINNED}
    bad = {k: v[:16] for k, v in got.items() if v != PINNED[k]}
    if bad:
        raise SystemExit(f"pinned input changed: {bad}")
    if sha256_file(SPEC) != SPEC_SHA256:
        raise SystemExit("G0_SPEC.md sha256 differs from the frozen revision 8")
    return got


# ---------------------------------------------------------------- dates (day numbers; row 48: ISO or month name)
EPOCH = _dt.date(1970, 1, 1)
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]


def day(y: int, m: int, d: int) -> int:
    return (_dt.date(y, m, d) - EPOCH).days


def ymd(n: int) -> _dt.date:
    return EPOCH + _dt.timedelta(days=n)


def iso(n: int) -> str:
    return ymd(n).isoformat()


def month_name_date(n: int) -> str:
    d = ymd(n)
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


def days_in_month(y: int, m: int) -> int:
    nxt = _dt.date(y + (m == 12), (m % 12) + 1, 1)
    return (nxt - _dt.date(y, m, 1)).days


def month_bounds(y: int, m: int) -> tuple[int, int]:
    a = day(y, m, 1)
    return a, a + days_in_month(y, m) - 1


def premise_set(fn, rng, card, rec):
    """Repair r1 v3c (G10 twin share): T1 contrast set. fn(rng, card, rec) is a sampler's premise-twin builder and
    returns [settled twin, open base]. With spec['twin2'] a second settled twin is drawn from the same open base with
    a different record (the decisive premise filled another way), and the set is returned as [open base, twin 1,
    twin 2]: one base plus two label-flip twins, each its own row and call_id (XF03).
    Repair r1 v3e: spec['twin_x'] lists further settled twins ([want, label] each), every one a record distinct
    from all earlier rows of the set, added the same way (up to 10 draws each).
    When a planned extra twin is not found, the set keeps the twins found so far, and the rows stay in the planned
    order [open base, twin 1, ...] so each row takes the wording slot planned for its own label (build._wording_slots;
    v3d returned a short set as [settled twin, open base], which swapped the two rows' planned slots). Extra twins
    are tried only while the unit has CPU time to spare (a unit time-out would lose the whole set)."""
    import json
    import time as _t
    t0 = _t.process_time()
    rows = fn(rng, card, rec)
    sp = rec.get("spec") or {}
    if not sp.get("twin2"):
        return rows

    def key(r):
        return json.dumps({"R": r.get("R"), "T": r.get("T")}, sort_keys=True, default=str)

    keys = {key(rows[0])}
    out = [rows[1], rows[0]]
    extra = [[sp.get("twin2_want"), sp.get("twin2_label")]] + list(sp.get("twin_x") or [])
    for want, lab in extra:
        if _t.process_time() - t0 > 2.5:
            break
        sp2 = {**sp, "twin_more": True, "twin_want": sp.get("twin_want") if want is None else want,
               "twin_label": sp.get("twin_label") if lab is None else lab}
        rec2 = {**rec, "spec": sp2}
        found = None
        for _ in range(10):
            if _t.process_time() - t0 > 4.0:      # the unit's CPU limit is 6 s (build.build_one)
                break
            try:
                r2 = fn(rng, card, rec2)
            except Exception as e:  # noqa: BLE001  (a sampler Skip / Reject: try another draw)
                if type(e).__name__ == "UnitTimeout":
                    raise
                continue
            if key(r2[0]) not in keys:
                found = r2[0]
                break
        if found is None:
            break
        keys.add(key(found))
        tw = dict(found)
        tw["spec"] = sp
        out.append(tw)
    return out
