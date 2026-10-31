"""PREREG A28 (b): the spec 6 token cap met by mixer.cap_trim (CPU only, synthetic families; no data files read).

Round r4 (rewritten from test_mixer_a28.py.pre_r4, disclosed): closed-form quotas (spec 6's F13 / 3B 6-7.9K units
first and only while the token share > 30%; then the excess long rows apportioned by largest remainder over the blocks
over their own cap, each quota <= the block's own excess; the stated fallback when a block cannot meet its quota);
composite moves with no search constants (a block whose every single drop breaks a rule is still trimmed); cell
balance, label x bin chi-square, crowd-bin caps and the 2.1 bands / point values hold (checked here independently of
the guard); the true twin-set share (meta.twin_of, base rows included) and the families' quota fields (sidecar) are
guarded; drops follow the seeded order inside each cell (quota units first); public rows change only by same-source
swaps; a mix already under the cap leaves finish() byte-identical to the pre-A28 mixer; A26 (b) refill (short units of
cards already mixed, lowest rows / target first, <= 1.5x target, <= max(12%, pre-trim share) of the realised own rows);
a remainder sets replay = floor(1.5 x realised new rows); determinism. test_token_cap_measures_only_a28 moved here
from test_mixer.py (which has its original test back)."""
import copy
import importlib.util
import json
import math
import re
import sys
import time
from collections import Counter, defaultdict
from importlib.machinery import SourceFileLoader
from pathlib import Path
from types import SimpleNamespace

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import crowd_select as cs  # noqa: E402
import mixer as mx  # noqa: E402
from mixio import InputLog, h64  # noqa: E402

DEFS = ["one-line", "examples", "rubric", "one-line", "examples", "rubric", "one-line", "short"]   # short 12.5%


@pytest.fixture(autouse=True)
def quiet(monkeypatch):
    """Synthetic runs never write the real progress_mixer.log; every run is traced."""
    monkeypatch.setattr(mx, "log", lambda msg: None)
    monkeypatch.setattr(mx, "A28_TRACE", [])
    # synthetic worlds hold 2-4 families, each far above 12% of own rows by construction: refill room comes from
    # 1.5x target only; test_family_share_uses_realised_own_rows sets the spec value back
    monkeypatch.setattr(mx, "OWN_MAX", 1.0)


def idx(i: str) -> int:
    return int(re.sub(r"\D", "", i) or 0)


def yn(i, cid, gold, block, w="wd.A", b=None, **meta):
    m = {"wording_id": w, "licence": "CC0", "format_style": "FS-0001", **meta}
    if b:
        m["difficulty_bin"] = b
    return {"id": i, "call_id": cid, "group_id": "g" + i, "state": "s " + i, "qtype": "noul", "gold": gold,
            "role": "base", "source": "c_own_" + block, "instructions": "Is it allowed?", "options": [],
            "_block": block, "meta": m}


def chk(i, cid, blk, k=5, src=None, g=None, **meta):
    """A choice row with k equal-length options (longest-is-gold neutral); gold position g (default idx % k)."""
    o = [f"o{j:02d}" for j in range(k)]
    return {"id": i, "call_id": cid, "group_id": "g" + i, "state": "s " + i, "qtype": "choice",
            "gold": o[idx(i) % k if g is None else g], "options": list(o), "role": "base",
            "source": src or "c_own_" + blk, "instructions": "Pick one.", "_block": blk,
            "meta": {"licence": "CC0", "format_style": "FS-0001", **meta}}


def fam_pool(fam, sel, extra, bins=None, pg=None):
    """Selected rows + unselected candidates of one family -> (mix rows, own_pool) as family_block builds them."""
    rows = [{k: v for k, v in r.items() if k != "_block"} for r in sel + extra]
    units = cs.units_of(rows, [])
    pool = mx.own_pool(fam, rows, [], units, {r["id"] for r in sel}, bins or {r["id"]: "na" for r in rows}, pg or {})
    return [r | {"_block": fam} for r in sel], pool


def accept(pool, u, tally):
    return pool.rows_of(u, tally)


def shares(rows, nt):
    new = [r for r in rows if r["_block"] != "replay"]
    n, t = len(new), sum(nt[r["id"]] for r in new)
    ln = sum(1 for r in new if nt[r["id"]] >= 2000)
    lt = sum(nt[r["id"]] for r in new if nt[r["id"]] >= 2000)
    return ln / n, lt / t, n


def cap_ok(rs_, ts):
    return rs_ <= 0.09 and ts <= 0.30


def run(rows, pools, targets, nt, ctx=None):
    ntok, rep, ever = dict(nt), {}, {r["id"]: (r["_block"], r) for r in rows}
    ctx = ctx or getattr(pools.get("replay"), "ctx", None)
    mx.A28_TRACE.clear()
    out, rels, probs = mx.cap_trim(rows, [], ntok, pools, ctx, targets, ever, set(), accept, rep)
    return out, probs, rep["a28_cap"], ntok, list(mx.A28_TRACE)


def f13_rows(p, card="c", yn_n=60, ch=((4, 38), (5, 40), (12, 12), (25, 10)), cards=4):
    """The review's deadlock composition: yes/no 0.375 (< 45%), opt_2-4 0.38 (band edge), opt_5-9 0.40 (> 38%),
    opt_10-19 0.12 (band edge), opt_20-60 0.10 (< 12%); gold labels balanced; 4 cards; short card 12.5%."""
    out, i = [], 0
    for j in range(yn_n):
        out.append(yn(f"{p}{i}", f"{p}u{i}", j % 2, "F13", card_id=f"{card}{i % cards}", defs_style=DEFS[i % 8]))
        i += 1
    for k, n in ch:
        for j in range(n):
            out.append(chk(f"{p}{i}", f"{p}u{i}", "F13", k=k, g=j % k, card_id=f"{card}{i % cards}",
                           defs_style=DEFS[i % 8]))
            i += 1
    return out


def plain_rows(fam, p, n_yn, n_ch, k=4, card="c", cards=8, w="wd.A"):
    out = []
    for j in range(n_yn):
        out.append(yn(f"{p}{j}", f"{p}u{j}", j % 2, fam, w=w, card_id=f"{card}{j % cards}", defs_style=DEFS[j % 8]))
    for j in range(n_ch):
        i = n_yn + j
        out.append(chk(f"{p}{i}", f"{p}u{i}", fam, k=k, g=j % k, card_id=f"{card}{i % cards}",
                       defs_style=DEFS[i % 8]))
    return out


def replay_ctx(n_src=3, per=100):
    lt, units, rows = [], [], []
    for s in range(n_src):
        for i in range(per):
            rid = f"rp{s}_{i}"
            lt.append({"id": rid, "qtype": "noul", "role": "base", "gold": i % 2})
            units.append({"id": rid, "rows": [len(lt) - 1], "source": f"src{s}"})
            rows.append(yn(rid, rid, i % 2, "replay") | {"source": f"src{s}"})
    uid = {x["id"]: u for u, x in enumerate(units)}
    pool = mx.Pool("replay", uid, lambda r: r["source"], {}, None, None, None, None)
    return rows, {"lt": lt, "units": units, "sticky": set()}, pool


def world(public_same_source_short=False):
    """F13 all long (a third 6.5K); F11 half long, with short same-cell pool units; F1 12% long (over its own cap);
    F3 all short with a deep pool; public: 12 QuALITY 6.5K rows, the rest short; reserve: QuALITY rows (long, or
    short when asked) + short rows of another source; 300 replay rows."""
    nt, rows, pools = {}, [], {}
    rows_r, ctx, pools["replay"] = replay_ctx()
    pools["replay"].ctx = ctx
    rows += rows_r
    f13 = f13_rows("t")
    f13x = f13_rows("tx", card="c", yn_n=10, ch=((4, 4), (5, 4)))
    f11 = plain_rows("F11", "k", 120, 80, k=3, card="k")
    f11x = plain_rows("F11", "kx", 60, 40, k=3, card="k")
    f1 = plain_rows("F1", "a", 300, 0, card="a")
    f1x = plain_rows("F1", "ax", 100, 0, card="a")
    f3 = plain_rows("F3", "b", 200, 200, card="b")
    f3x = plain_rows("F3", "bx", 150, 150, card="b")
    pub = [chk(f"p{i}", f"pu{i}", "public", src="c_pub_quality" if i < 12 else "c_pub_x",
               **({"block": "3B"} if i < 12 else {})) for i in range(300)]
    res = [chk(f"q{i}", f"qu{i}", "public", src="c_pub_quality", block="3B") for i in range(10)]
    res += [chk(f"y{i}", f"yu{i}", "public", src="c_pub_x") for i in range(50)]
    for r in rows:
        nt[r["id"]] = 500
    for i, r in enumerate(f13 + f13x):
        nt[r["id"]] = 6500 if i % 3 == 0 else 3000
    for i, r in enumerate(f11):
        nt[r["id"]] = 2600 if (i // 2) % 2 == 0 else 600            # long rows of both labels
    for i, r in enumerate(f11x):
        nt[r["id"]] = 2600 if i % 4 == 0 else 600
    for i, r in enumerate(f1):
        nt[r["id"]] = 2500 if i < 36 else 600
    for r in f1x + f3 + f3x:
        nt[r["id"]] = 600
    for i, r in enumerate(pub):
        nt[r["id"]] = 6500 if i < 12 else 500
    for i, r in enumerate(res):
        nt[r["id"]] = (500 if public_same_source_short else 4000) if i < 10 else 500
    for fam, sel, extra in (("F13", f13, f13x), ("F11", f11, f11x), ("F1", f1, f1x), ("F3", f3, f3x)):
        mr, pools[fam] = fam_pool(fam, sel, extra)
        rows += mr
    rows += pub
    pools["public"] = mx.public_pool([{k: v for k, v in r.items() if k != "_block"} for r in res])
    targets = dict(cs.TARGET_R1) | {"F13": 160, "F11": 200, "F1": 300, "F3": 400}
    return rows, pools, targets, nt


# ------------------------------------------------------------------ independent checks (no mixer guard code)

def strata(rows_f):
    out = defaultdict(Counter)
    for r in rows_f:
        b = (r.get("meta") or {}).get("difficulty_bin") or "na"
        out[cs.stratum(r, b)][cs.label_class(r)] += 1
    return out


def imbalance(s, c):
    k = cs.n_classes(s)
    return max(c[j] for j in range(k)) - min(c[j] for j in range(k)) if k >= 2 else 0


def comp(rows_f):
    """Spec 2.1 shares from the rows themselves."""
    n = len(rows_f)
    ch = [r for r in rows_f if r["qtype"] == "choice"]
    out = {"yes_no_share": (n - len(ch)) / n}
    for b in ("2-4", "5-9", "10-19", "20-60") if ch else ():
        out["opt_" + b] = sum(1 for r in ch if cs.opt_bucket(len(r["options"])) == b) / len(ch)
    out["short_or_no_card"] = sum(1 for r in rows_f if r["meta"].get("defs_style") in ("short", "none")) / n
    return out


def band_ok(v0, v1, band):
    """Each edge of a band is a rule: met before -> met after; missed before -> not missed by more. A point value
    (p, p): not further from p than before."""
    if band[0] == band[1]:
        return abs(v1 - band[0]) <= abs(v0 - band[0]) + 1e-12
    for o0, o1 in ((band[0] - v0, band[0] - v1), (v0 - band[1], v1 - band[1])):
        if o1 > 1e-12 and (o0 <= 1e-12 or o1 > o0 + 1e-12):
            return False
    return True


def by_block(rows):
    out = defaultdict(list)
    for r in rows:
        out[r["_block"]].append(r)
    return out


def check_rules_kept(before, after, nt):
    """Cell balance (crowd_select tolerance), chi-square, bands: what held before holds after; nothing worse."""
    b0, b1 = by_block(before), by_block(after)
    for fam in [f for f in cs.FAMS if f in b0]:
        s0, s1 = strata(b0[fam]), strata(b1[fam])
        for s, c in s1.items():
            tol = 1 if s[0] == "ord" else max(2, 0.02 * sum(c.values()))
            i0, i1 = imbalance(s, s0.get(s, Counter())), imbalance(s, c)
            assert i1 <= max(tol, i0), (fam, s, i0, i1)
        p0, p1 = mx.label_bin_p(b0[fam]), mx.label_bin_p(b1[fam])
        if p0 and min(p0) > 0.01:
            assert not p1 or min(p1) > 0.01, (fam, p1)
        c0, c1 = comp(b0[fam]), comp(b1[fam])
        for name, v0 in c0.items():
            band = mx.COMP[name]
            if name not in c1:
                continue
            if name == "yes_no_share" and not 0 < v0 < 1:
                continue
            assert band_ok(v0, c1[name], band), (fam, name, v0, c1[name])


# ------------------------------------------------------------------ token_cap (moved here from test_mixer.py)

def mk(i, cid, block="F1", **kw):
    return {"id": i, "call_id": cid, "_block": block, "source": "c_own_F1", "qtype": "noul", "gold": 1,
            "role": "base", "meta": {"licence": "CC0"}, **kw}


def test_token_cap_measures_only_a28():
    """PREREG A28 (b): finish() calls token_cap with spec6=False: it measures the cap (and returns rows over 7,900);
    the F13 / 3B 6-7.9K rule and the trim run in cap_trim (whole units, guards, A26 b refills). Moved from
    tests/test_mixer.py (A28 edit, disclosed in r4) with spec6=False added; test_mixer.py has its original
    test_token_cap_drops_long_f13_first back, which calls the default spec6=True path."""
    rows = [mk(f"r{i}", f"c{i}", block="replay") for i in range(10)]
    rows += [mk(f"n{i}", f"d{i}") for i in range(80)]
    rows += [mk(f"L{i}", f"e{i}", block="F13") for i in range(20)]
    ntok = {r["id"]: 500 for r in rows} | {f"L{i}": 6500 for i in range(20)} | {"n0": 8000}
    rep = {}
    drop, probs = mx.token_cap(rows, ntok, rep, spec6=False)
    assert drop == {"n0"} and rep["token_cap"]["dropped_for_cap"] == 0
    assert rep["token_cap"]["long_row_share"] == 0.21 and len(probs) == 3    # rows, tokens, one row over 7,900


def test_token_cap_spec6_whole_units():
    """spec6=True: a unit with a 6-7.9K F13 row leaves whole (its short partner too)."""
    rows = [mk(f"n{i}", f"d{i}") for i in range(80)]
    rows += [mk(f"L{i}", f"e{i}", block="F13") for i in range(20)] + [mk(f"P{i}", f"e{i}", block="F13")
                                                                      for i in range(20)]
    ntok = {r["id"]: 500 for r in rows} | {f"L{i}": 6500 for i in range(20)}
    drop, probs = mx.token_cap(rows, ntok, {})
    assert all((f"P{d[1:]}" in drop) for d in drop if d.startswith("L")) and drop


# ------------------------------------------------------------------ the cap, exactly as specified

def p_units(rows):
    units = defaultdict(list)
    for r in rows:
        units[(r["_block"], r["call_id"])].append(r)
    return units


def test_cap_met_closed_form_quotas():
    rows, pools, targets, nt = world()
    before = shares(rows, nt)
    assert not cap_ok(*before[:2])
    out, probs, info, ntok, tr = run(rows, pools, targets, nt)
    r1, t1, n1 = shares(out, ntok)
    assert cap_ok(r1, t1) and info["after"]["cap_met"] and not probs, probs
    assert info["after"]["long_row_share"] == round(r1, 4) and info["after"]["long_token_share"] == round(t1, 4)
    phases = [m["phase"] for m in tr if m["phase"] in ("p1", "p2")]
    assert phases == sorted(phases) and "p1" in phases and "p2" in phases        # spec 6's bin first
    units = p_units(rows)
    for m in tr:
        if m["phase"] == "p1":                                       # p1: only while long tokens > 30%
            assert m["cap_before"][1] > 0.30 and m["block"] in ("F13", "public")
            if m["kind"] == "drop":                                  # a move starts with a 6-7.9K unit
                assert any(6000 <= nt[r["id"]] <= 7900 for r in units[m["units"][0]])
        elif m["phase"] == "p2":
            assert not cap_ok(*m["cap_before"])                      # never a move once the cap holds
            assert any(nt[r["id"]] >= 2000 for r in units[m["units"][0]])
    for e in info["plan"]:                                           # closed form: largest remainder by weight
        cap_w = {b: w for b, w in e["weights"].items() if w > 0}
        exp = {b: q for b, q in mx.largest_remainder(cap_w, min(e["need"], sum(cap_w.values()))).items() if q > 0}
        assert e["quotas"] == exp and all(q <= cap_w[b] for b, q in exp.items())
        for f in e["fallback"]:                                      # fallback: same rule over the blocks left
            assert sum(f["to"].values()) <= f["short"]
    p2 = [e["measure"] for e in info["plan"] if e["phase"] == "p2"]
    assert p2 and p2[0] == "rows" and p2 == sorted(p2)               # the row cap first, then tokens if still over
    # every block: rules kept; public per source unchanged and never a reserve row of another source
    check_rules_kept(rows, out, ntok)
    pc = lambda rr: Counter(r["source"] for r in rr if r["_block"] == "public")       # noqa: E731
    assert pc(out) == pc(rows) and not any(r["id"].startswith(("y", "q")) for r in out)
    assert info["public_rows_by_source_changed"] == {} and info["expected"]["public_delta"] == 0
    assert any(e["why"].get("public", "").startswith("no swap") for e in info["plan"])   # public's quota moved on
    # refills: short rows of cards already in the family's mix; families <= 1.5x target
    ids0 = {r["id"] for r in rows}
    cards0 = {(r["_block"], r["meta"].get("card_id")) for r in rows if r["_block"] in cs.FAMS}
    new = [r for r in out if r["id"] not in ids0]
    assert new and all(ntok[r["id"]] < 2000 and (r["_block"], r["meta"]["card_id"]) in cards0 for r in new)
    cnt = Counter(r["_block"] for r in out)
    assert all(cnt[f] <= 1.5 * targets[f] for f in ("F13", "F11", "F1", "F3"))
    assert cnt["F13"] < 160 and info["trims_by_block"]["F13"]["dropped_rows"] > 0
    assert info["guard_audit_break_count"] == 0
    # realised totals match the report and the share expectations
    assert n1 == sum(v for b, v in cnt.items() if b != "replay") == info["after"]["new_rows"]
    assert info["expected"]["total_delta"] == -info["remainder_rows"] - info["replay_cut"]
    assert sum(info["expected"]["family_delta"].values()) == info["expected"]["own_delta"]


def test_quota_never_takes_a_block_below_its_own_cap():
    """Quotas <= each block's own excess (long rows - floor(9% x rows)); only blocks over their own cap get one."""
    rows, pools, targets, nt = world()
    out, probs, info, ntok, tr = run(rows, pools, targets, nt)
    for e in info["plan"]:
        if e["phase"] == "p2":
            assert set(e["weights"]) <= {"F1", "F11", "F13", "public"} and "F3" not in e["weights"]
            for b, d in e["delivered"].items():
                assert d <= e["weights"][b] + 2                      # whole units: at most one unit over
    long_f1 = sum(1 for r in out if r["_block"] == "F1" and ntok[r["id"]] >= 2000)
    assert long_f1 >= 27                                             # never trimmed below its own 9% (27 of 300)
    for m in tr:
        if m["phase"] == "p2" and m["kind"] in ("drop", "swap"):
            assert m["own_before"][0] > 0.09 or m["own_before"][1] > 0.30


def test_f13_deadlock_is_trimmed_by_composite_moves():
    """Every single F13 drop breaks a rule, yet the trim meets the cap and keeps every rule."""
    rows, pools, targets, nt = world()
    rows = [r for r in rows if r["_block"] in ("replay", "F13", "F3")]
    pools = {k: pools[k] for k in ("F13", "F3")}
    st = mx.A28State(rows, nt)
    refused = 0
    for rr in p_units([r for r in rows if r["_block"] == "F13"]).values():
        st.move(out=rr)
        refused += not st.passes()
        st.rollback()
    assert refused == len(p_units([r for r in rows if r["_block"] == "F13"]))   # no single drop is allowed
    out, probs, info, ntok, tr = run(rows, pools, targets, nt)
    assert info["after"]["cap_met"] and not probs, probs
    assert info["trims_by_block"]["F13"]["dropped_rows"] > 100
    first = next(m for m in tr if m["kind"] == "drop" and m["block"] == "F13")
    assert len(first["units"]) > 1                                   # a composite move
    check_rules_kept(rows, out, ntok)


def test_drops_follow_seeded_order_inside_each_cell():
    rows, pools, targets, nt = world()
    out, probs, info, ntok, tr = run(rows, pools, targets, nt)
    units = p_units(rows)
    for ph in ("p1", "p2"):
        quota = (lambda u: any(mx.spec6_bin(r, nt) for r in units[u])) if ph == "p1" else \
            (lambda u: any(nt[r["id"]] >= 2000 for r in units[u]))
        seq = defaultdict(list)
        for m in tr:
            if m["phase"] == ph and m["kind"] == "drop":
                for u in m["units"]:
                    seq[(u[0], mx._csig(pools[u[0]], units[u]))].append(u)
        for (b, c), us in seq.items():
            rank = [(not quota(u), h64(mx.SEED, "a28", ph, *u)) for u in us]
            assert rank == sorted(rank), (ph, b, c)                  # seeded order, quota units first, per cell


def test_public_same_source_swaps_only():
    """A public long unit leaves only for a short reserve row of the same source."""
    rows, pools, targets, nt = world(public_same_source_short=True)
    out, probs, info, ntok, tr = run(rows, pools, targets, nt)
    pc = lambda rr: Counter(r["source"] for r in rr if r["_block"] == "public")       # noqa: E731
    assert pc(out) == pc(rows) and info["public_rows_by_source_changed"] == {}
    swapped = [r for r in out if r["id"].startswith("q")]
    assert swapped and all(r["source"] == "c_pub_quality" and ntok[r["id"]] < 2000 for r in swapped)
    assert not any(r["id"].startswith("y") for r in out)
    assert all(m["kind"] == "swap" for m in tr if m["block"] == "public")


def test_refill_lowest_rows_per_target_first_and_room():
    rows, pools, targets, nt = world()
    targets["F3"] = 800                                                 # F3 is at 400 / 800: it fills first
    out, probs, info, ntok, tr = run(rows, pools, targets, nt)
    ref = [m for m in tr if m["kind"] == "refill"]
    assert ref and ref[0]["block"] == "F3"
    lim = info["family_rows_target_limit"]
    assert all(v[0] <= v[2] <= 1.5 * v[1] for v in lim.values())


def share_world():
    """Nine short families (F2: 124 rows, F3-F10: 100; F3 with a short pool) and F13 (110 rows, all long): every family
    under 12% of the 1,034 own rows; F13's freed rows can go to F3 only up to 12% of the realised own rows, and F2
    (no pool) passes 12% once the own rows fall."""
    nt, rows, pools = {}, [], {}
    rows_r, ctx, pools["replay"] = replay_ctx()
    pools["replay"].ctx = ctx
    rows += rows_r
    for r in rows_r:
        nt[r["id"]] = 500
    for f in ("F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10"):
        n = 62 if f == "F2" else 50                                   # F2: 124 rows, 11.99% of own rows
        sel = plain_rows(f, f.lower() + "s", n, n, k=4, card=f.lower())
        extra = plain_rows(f, f.lower() + "x", 40, 40, k=4, card=f.lower()) if f == "F3" else []
        for r in sel + extra:
            nt[r["id"]] = 600
        mr, pools[f] = fam_pool(f, sel, extra)
        rows += mr
    f13 = f13_rows("t", yn_n=40, ch=((4, 28), (5, 30), (12, 6), (25, 6)))
    for i, r in enumerate(f13):
        nt[r["id"]] = 6500 if i % 3 == 0 else 3000
    mr, pools["F13"] = fam_pool("F13", f13, [])
    rows += mr
    targets = dict(cs.TARGET_R1) | {f: 100 for f in ("F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10")} | \
        {"F13": 110}
    return rows, pools, targets, nt


def test_family_share_uses_realised_own_rows(monkeypatch):
    """Spec 2.1 12%: judged on the realised own rows (never the planned ones); a refill that would take a family past
    max(12%, its pre-trim share) of them is given back; the rest lowers the total (replay = 1.5 x new rows)."""
    monkeypatch.setattr(mx, "OWN_MAX", 0.12)
    rows, pools, targets, nt = share_world()
    out, probs, info, ntok, tr = run(rows, pools, targets, nt)
    own0 = sum(1 for r in rows if r["_block"] in cs.FAMS)
    own1 = sum(1 for r in out if r["_block"] in cs.FAMS)
    assert info["own_rows"] == [own0, own1] and own0 == 1034
    assert info["after"]["cap_met"] and not probs, probs
    cnt = Counter(r["_block"] for r in out)
    assert info["refilled_rows_by_family"].get("F3", 0) > 0 and info["remainder_rows"] > 0
    assert (cnt["F3"] + 2) / (own1 + 2) > 0.12                        # F3's refills stopped at 12% (share binding)
    assert info["trims_by_block"]["F2"]["share12_rows"] > 0          # F2 above 12% once own rows fell: whole units
    for f, (n1, tgt, lim, s1, s0) in info["family_rows_target_limit"].items():
        assert n1 == cnt[f] and s1 == round(n1 / own1, 4) and n1 / own1 <= max(0.12, s0) + 1e-12, f
    assert info["replay_cut"] == max(0, 300 - math.floor(1.5 * shares(out, ntok)[2]))       # replay <= 1.5x new


def test_remainder_sets_replay_to_1_5x_realised_new_rows():
    rows_r, ctx, rpool = replay_ctx(per=700)
    rows, pools, targets, nt = world()
    rows = [r for r in rows if r["_block"] != "replay"] + rows_r
    for r in rows_r:
        nt[r["id"]] = 500
    for f in ("F3", "F1", "F11"):                                     # shallow pools: few short refill units
        pools[f].cands = {"": pools[f].cands[""][:6]}
    for r in rows:                                                     # short QuALITY rows: the cap stays reachable
        if r.get("source") == "c_pub_quality":
            nt[r["id"]] = 500
    pools["replay"] = rpool
    out, probs, info, ntok, tr = run(rows, pools, targets, nt, ctx)
    rem = info["remainder_rows"]
    r1, t1, n1 = shares(out, ntok)
    rep_rows = [r for r in out if r["_block"] == "replay"]
    assert rem > 0 and cap_ok(r1, t1) and not probs, probs
    assert len(rep_rows) == math.floor(1.5 * n1) == info["replay_after"]["rows"]      # replay = 60% of the total
    assert info["replay_cut"] == 2100 - len(rep_rows) > 0
    rs = mx.rs_mod()
    kept_ids = {r["id"] for r in rep_rows}
    for s in range(3):                                                 # per source: a prefix of the sampler order
        us = [u for u, x in enumerate(ctx["units"]) if x["source"] == f"src{s}"]
        order = [ctx["units"][u]["id"] for u in rs.unit_order(ctx["lt"], ctx["units"], us)]
        kept = [x for x in order if x in kept_ids]
        assert kept == order[:len(kept)]
    exp = info["expected"]
    assert exp["total_delta"] == -rem - info["replay_cut"] and exp["replay_delta"] == -info["replay_cut"]


def test_deterministic():
    a = run(*copy.deepcopy(world()))
    b = run(*copy.deepcopy(world()))
    assert [r["id"] for r in a[0]] == [r["id"] for r in b[0]]
    assert json.dumps(a[2], sort_keys=True, default=str) == json.dumps(b[2], sort_keys=True, default=str)


def test_no_search_constants():
    """r4: the trim has no step-count or search-size constants (CHAIN_MAX, CHAIN_TRIES, STALL_MAX, PROBE_MAX) and no
    invented proxy tolerance (DRIFT)."""
    for name in ("CHAIN_MAX", "CHAIN_TRIES", "STALL_MAX", "PROBE_MAX", "DRIFT"):
        assert not hasattr(mx, name), name


def test_report_names_rule_and_side_file_quotas():
    rows, pools, targets, nt = world()
    out, probs, info, ntok, tr = run(rows, pools, targets, nt)
    assert info["rule"] == mx.A28_RULE and "6-7.9K" in info["rule"] and "A28 (b)" in info["rule"]
    assert info["guard"]["side_file_quotas"] == mx.SIDE_FILE_QUOTAS
    ct = info["composition_touched"]["F13"]
    c0 = Counter(r["meta"]["card_id"] for r in rows if r["_block"] == "F13")
    c1 = Counter(r["meta"]["card_id"] for r in out if r["_block"] == "F13")
    assert ct["card_tv"] == round(mx.card_tv(c0, c1), 4)
    assert "twin_set_rows" in ct["before"] and ct["bands"]["twin_set_rows"] == [0.2, 0.25]
    assert info["over_cap_blocks_before"] and "F13" in info["over_cap_blocks_before"]
    for b, t in info["trims_by_block"].items():                       # the proportional-slice bound held
        assert t["dropped_rows"] - t["share12_rows"] <= t["drop_bound_rows"]
    json.dumps(info)                                                   # the report is plain JSON (dryrun / mix_report)


def test_share_checks_public_never_takes_a28_delta():
    tg = dict(cs.TARGET_R1)
    by = Counter({"replay": 90000, "public": 8000, "COMMIT": 6000, "F1": 5400})
    sh, pr = mx.share_checks(by, 5400, 45250, 8750, tg, ["F1"], {"public_delta": -750, "total_delta": 0})
    assert sh["public"] == [8000, 8750] and "share public: 8,000 rows vs spec 8,750" in pr
    sh, pr = mx.share_checks(by, 5400, 45250, 8750, tg, ["F1"], {"own_delta": -100, "family_delta": {"F1": -100}})
    assert any(p.startswith("share own: 5,400 rows vs 45,150 expected after the A28 (b) trim") and
               "(spec 45,250, delta -100)" in p for p in pr)
    sh, pr = mx.share_checks(by, 5400, 45250, 8750, tg, ["F1"], {})
    assert "share own: 5,400 rows vs spec 45,250" in pr and "spec_before_a28" not in sh


# ------------------------------------------------------------------ r4: true twin sets and the families' quota fields

def twin_world(long_in_sets=False):
    """F9: 400 rows, 24% in label-flip twin sets (48 base + flip-twin pairs, short), 60 long rows outside the sets
    (15%, over its own 9%); F13: all long, a deep short pool elsewhere (F3) for refills."""
    nt, rows, pools = {}, [], {}
    rows_r, ctx, pools["replay"] = replay_ctx()
    pools["replay"].ctx = ctx
    rows += rows_r
    for r in rows_r:
        nt[r["id"]] = 500
    f9 = plain_rows("F9", "n", 200, 200, k=4, card="n")
    for j in range(48):                                              # pairs inside the yes/no rows (other gold)
        base, tw = f9[2 * j], f9[2 * j + 1]
        tw["meta"]["twin_of"] = base["id"]
    for r in f9:
        nt[r["id"]] = 600
    ch = [r for r in f9 if r["qtype"] == "choice"]
    for r in (ch[:60] if not long_in_sets else ch[:60]):
        nt[r["id"]] = 2600
    f9x = plain_rows("F9", "nx", 40, 40, k=4, card="n")
    f13 = f13_rows("t")
    f13x = f13_rows("tx", card="c", yn_n=10, ch=((4, 4), (5, 4)))
    f3 = plain_rows("F3", "b", 200, 200, card="b")
    f3x = plain_rows("F3", "bx", 150, 150, card="b")
    for i, r in enumerate(f13 + f13x):
        nt[r["id"]] = 6500 if i % 3 == 0 else 3000
    for r in f9x + f3 + f3x:
        nt[r["id"]] = 600
    for fam, sel, extra in (("F9", f9, f9x), ("F13", f13, f13x), ("F3", f3, f3x)):
        mr, pools[fam] = fam_pool(fam, sel, extra)
        rows += mr
    targets = dict(cs.TARGET_R1) | {"F9": 400, "F13": 160, "F3": 400}
    return rows, pools, targets, nt


def true_twin_share(rows_f):
    """Independent count: rows whose twin_of names a row in the mix with another gold, plus those base rows."""
    by = {r["id"]: r for r in rows_f}
    mem = set()
    for r in rows_f:
        b = r["meta"].get("twin_of")
        if b in by and str(by[b]["gold"]) != str(r["gold"]):
            mem |= {r["id"], b}
    return len(mem) / len(rows_f)


def test_twin_set_band_uses_true_sets():
    rows, pools, targets, nt = twin_world()
    f9 = [r for r in rows if r["_block"] == "F9"]
    assert abs(true_twin_share(f9) - 0.24) < 1e-9
    out, probs, info, ntok, tr = run(rows, pools, targets, nt)
    f9b = [r for r in out if r["_block"] == "F9"]
    s1 = true_twin_share(f9b)
    assert info["after"]["cap_met"] and not probs, probs
    assert 0.20 <= s1 <= 0.25, s1                                     # in band before -> in band after
    ct = info["composition_touched"]["F9"]
    assert ct["before"]["twin_set_rows"] == 0.24 and ct["after"]["twin_set_rows"] == round(s1, 4)
    st = mx.A28State(rows, nt)                                         # dropping one base row takes its twin out too
    pair = [r for r in rows if r["id"] in ("n0",)]
    st.move(out=pair)
    assert st.c[("blk", "F9")]["tset"] == 96 - 2
    st.rollback()
    assert st.c[("blk", "F9")]["tset"] == 96


def side_world():
    """F4: 400 rows, choice rows with masked labels on 12% (in the 10-15% band) and yes/no rows with yes = bad outcome
    on 50%; 124 long rows (31%: the 24 masked choice rows and 100 plain ones); F3: 800 short rows with a short pool
    (refills). The quota fields live only in the sidecar (ctx['sidecar'])."""
    nt, rows, pools = {}, [], {}
    rows_r, ctx, pools["replay"] = replay_ctx()
    pools["replay"].ctx = ctx
    rows += rows_r
    for r in rows_r:
        nt[r["id"]] = 500
    f4 = plain_rows("F4", "m", 200, 200, k=4, card="m")
    f4x = plain_rows("F4", "mx", 60, 60, k=4, card="m")
    side = {}
    ch = [r for r in f4 if r["qtype"] == "choice"]
    for i, r in enumerate(ch):
        side[r["id"]] = {"label_form": "masked" if i < 24 else "plain"}
        nt[r["id"]] = 2600 if i < 124 else 600
    for i, r in enumerate(r for r in f4 if r["qtype"] == "noul"):
        side[r["id"]] = {"yes_bad": i % 4 < 2}
        nt[r["id"]] = 600
    for r in f4x:
        side[r["id"]] = {"label_form": "plain"} if r["qtype"] == "choice" else {"yes_bad": False}
        nt[r["id"]] = 600
    f3 = plain_rows("F3", "b", 400, 400, card="b")
    f3x = plain_rows("F3", "bx", 150, 150, card="b")
    for r in f3 + f3x:
        nt[r["id"]] = 600
    for fam, sel, extra in (("F4", f4, f4x), ("F3", f3, f3x)):
        mr, pools[fam] = fam_pool(fam, sel, extra)
        rows += mr
    targets = dict(cs.TARGET_R1) | {"F4": 400, "F3": 800}
    return rows, pools, targets, nt, side


def test_sidecar_quotas_guarded():
    rows, pools, targets, nt, side = side_world()
    ntok, rep, ever = dict(nt), {}, {r["id"]: (r["_block"], r) for r in rows}
    mx.A28_TRACE.clear()
    ctx = dict(pools["replay"].ctx, sidecar=side)
    out, rels, probs = mx.cap_trim(rows, [], ntok, pools, ctx, targets, ever, set(), accept, rep)
    info = rep["a28_cap"]
    assert info["after"]["cap_met"] and not probs, probs

    def masked(rr):
        ch = [r for r in rr if r["_block"] == "F4" and r["qtype"] == "choice"]
        return sum(1 for r in ch if side[r["id"]]["label_form"] == "masked") / len(ch)

    def ybad(rr):
        y = [r for r in rr if r["_block"] == "F4" and r["qtype"] == "noul"]
        return sum(1 for r in y if side[r["id"]]["yes_bad"]) / len(y)
    assert masked(rows) == 0.12 and 0.10 <= masked(out) <= 0.15        # band kept (independent count)
    assert 0.45 <= ybad(out) <= 0.55
    ct = info["composition_touched"]["F4"]
    assert ct["before"]["masked_of_choice"] == 0.12 and ct["after"]["masked_of_choice"] == round(masked(out), 4)
    assert info["trims_by_block"]["F4"]["long_rows_removed"] > 0
    assert info["guard_audit_break_count"] == 0


def test_band_rules():
    """(lo, hi): each edge its own rule; (p, p): no further from p (no tolerance assumed)."""
    assert mx.band_excess(0.22, 0.24, (0.20, 0.25)) == 0
    assert mx.band_excess(0.22, 0.26, (0.20, 0.25)) > 0               # left the band
    assert mx.band_excess(0.27, 0.26, (0.20, 0.25)) == 0              # out of band, moved closer
    assert mx.band_excess(0.27, 0.28, (0.20, 0.25)) > 0               # out of band, further away
    assert mx.band_excess(0.27, 0.19, (0.20, 0.25)) > 0               # crossed out the other side
    assert mx.band_excess(0.06, 0.045, (0.05, 0.05)) == 0             # point: closer (crossing allowed)
    assert mx.band_excess(0.06, 0.061, (0.05, 0.05)) > 0              # point: further
    assert mx.band_excess(0.05, 0.0500001, (0.05, 0.05)) > 0


def test_sidecar_flags_reads_family_fields(tmp_path, monkeypatch):
    for fam, rows_ in (("F10", [{"id": "a", "mode": "neutral", "fewshot_card": True, "yes_bad": True, "x": 1}]),
                       ("F3", [{"id": "b", "vocab": "swapped", "polarity": "bad", "inverted_card": False}])):
        d = tmp_path / fam / "out"
        d.mkdir(parents=True)
        (d / "candidates_r1.sidecar.jsonl").write_text("\n".join(json.dumps(x) for x in rows_) + "\n")
    monkeypatch.setattr(cs, "fam_dir", lambda fam: tmp_path / fam)
    side = mx.sidecar_flags(InputLog(), ["F10", "F3", "F1"])
    assert side == {"a": {"mode": "neutral", "fewshot_card": True, "yes_bad": True},
                    "b": {"vocab": "swapped", "polarity": "bad", "inverted_card": False}}
    ra = {"id": "a", "_block": "F10", "meta": {}}
    rb = {"id": "b", "_block": "F3", "meta": {}}
    assert mx.quota_flags(ra, side["a"]) == ("masked", True, True, None)
    assert mx.quota_flags(rb, side["b"]) == ("swapped", True, None, False)
    assert mx.quota_flags({"id": "c", "_block": "F7", "meta": {"label_form": "masked"}}, None)[0] == "masked"


# ------------------------------------------------------------------ finish(): under the cap = the pre-A28 mixer

def load_pre():
    p = HERE.parent / "mixer.py.pre_a28"
    if not p.exists():
        pytest.skip("mixer.py.pre_a28 backup not present")
    spec = importlib.util.spec_from_loader("mixer_pre_a28", SourceFileLoader("mixer_pre_a28", str(p)))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_finish(mod, monkeypatch, make):
    rows, pools, targets, nt = make()
    got = {}
    monkeypatch.setattr(mod, "log", lambda msg: None)

    class HO:
        def __init__(self, *a):
            pass

        def clash(self, r):
            return False

    monkeypatch.setattr(mod, "dev_items", lambda ilog, fams: {})
    monkeypatch.setattr(mod, "HeldOut", HO)
    monkeypatch.setattr(mod, "decontam_drop_ids", lambda ilog, files: (set(), []))
    monkeypatch.setattr(mod, "denylist_query", lambda new, parents: {})
    monkeypatch.setattr(mod, "run_denylist", lambda ilog, q, rep, final=False: set())
    monkeypatch.setattr(mod, "replay_denylist_check", lambda ilog, rows, rep: [])
    monkeypatch.setattr(mod, "token_counts", lambda ilog, rr, chunk=2000: [nt[r["id"]] for r in rr])
    monkeypatch.setattr(mod, "e2_final", lambda ctx, rows, rep: [])

    def gates(a, ilog, rep, probs, rows, rels, ntok, ho, exp_pub, targets, fams, fb, t0):
        got.update(rows=rows, rels=rels, rep=rep, probs=probs)
        return rep
    monkeypatch.setattr(mod, "gates", gates)
    a = SimpleNamespace(final=False, decontam_drops=[])
    mod.finish(a, InputLog(), {}, [], rows, [], {}, pools, {"lt": [], "units": [], "sticky": set()}, 300, targets,
               ["F1", "F3", "F11", "F13"], {}, time.time())
    return got


def under_cap():
    rows, pools, targets, nt = world()
    for r in rows:                                               # shorten: a few long rows, under both caps
        if r["_block"] != "replay" and nt[r["id"]] >= 2000 and h64("u", r["id"]) % 10 > 0:
            nt[r["id"]] = 700
    for p in pools.values():
        for c in p.cands.values():
            for u in c:
                for r in p.raw_of(u):
                    nt[r["id"]] = min(nt[r["id"]], 700)
    big = next(r for r in rows if r["_block"] == "F1")
    nt[big["id"]] = 8000                                         # one row over 7,900: dropped and refilled (G15)
    assert cap_ok(*shares([r for r in rows if r["id"] != big["id"]], nt)[:2])
    return rows, pools, targets, nt


def test_under_cap_byte_identical_to_pre_a28(monkeypatch):
    old = load_pre()
    a = run_finish(old, monkeypatch, under_cap)
    b = run_finish(mx, monkeypatch, under_cap)
    assert json.dumps(a["rows"], sort_keys=True) == json.dumps(b["rows"], sort_keys=True)
    assert json.dumps(a["rels"], sort_keys=True) == json.dumps(b["rels"], sort_keys=True)
    assert a["probs"] == b["probs"]
    ra = {k: v for k, v in a["rep"].items()}
    rb = {k: v for k, v in b["rep"].items() if k != "a28_cap"}
    assert json.dumps(ra, sort_keys=True, default=str) == json.dumps(rb, sort_keys=True, default=str)
    assert b["rep"]["a28_cap"]["applied"] is False and b["rep"]["refill"]["F1"]["refilled_rows"] == 1


def test_over_cap_through_finish_token_cap_report(monkeypatch):
    got = run_finish(mx, monkeypatch, world)
    info, tc = got["rep"]["a28_cap"], got["rep"]["token_cap"]
    assert info["applied"] and info["after"]["cap_met"]
    assert not any(p.startswith("token cap") or p.startswith("A28") for p in got["probs"])
    assert tc["long_row_share"] <= 0.09 and tc["long_token_share"] <= 0.30
    assert tc["before"] == [info["before"]["long_row_share"], info["before"]["long_token_share"]]
    assert tc["before"][0] > 0.09 and tc["dropped_for_cap"] == sum(t["dropped_rows"]
                                                                    for t in info["trims_by_block"].values()) > 0
