"""T63 generator: plan (NEAR / EXISTS / LIC cells, oversampled by 15%) and group generation (spec -> records). No rows are written here.

`Ctx(seed, standin, ...)`: standin=True is for tests and the dry run (TEST-ONLY wording pool, FIXTURE export / table allowed); a production
context requires a real wording pool, a real stdlib export (sha-bound, 3 identical runs) and the Opus licence table. The MAL slice is not built.
Opus ruling Q3 (18 Oct): every EX-B row (EX-B1 and EX-B2) is built only from the sha-bound L-0 image-record export and every LIC row only from the hashed
Opus table: with no export / table the generator raises (never a silent fallback), a production context refuses a FIXTURE sha, and rows reach a pool only
through `pool_writer.write_pool` (standin=False, recorded shas, no fixture sha).
"""
import math

from LP_COMMON import plan as plan_mod
from LP_COMMON import util, wording
from LP_COMMON.plan import Ctx as BaseCtx

from . import config as C
from . import exists, lic, near_build, near_plan, pool_writer, rows
from .near import AGE_ORDER  # noqa: F401


def pool_problems(pool):
    """Problems of a T63 wording pool ([] = usable): the shared slot / count / duplicate rules plus the NEAR question: the gold is LOOKALIKE-or-CONFUSION under the
    definitions block, so every NEAR frame must ask that (mention both defined terms). A frame that asks "is there a near name?" is answered YES by the old-legit,
    sibling and two-long-lived NO rows (>= 92% of the NO rows) and contradicts their gold."""
    bad = list(wording.validate(pool, C.FORM_SLOTS))
    bad += wording.frame_problems(pool, "T63-Q-NEAR", require_all=(r"look-?alike", r"confusion"))
    return bad


class Ctx(BaseCtx):
    def __init__(self, seed, standin=False, pool_path=None, pool=None, exports=None, table=None, deny_check=None):
        if pool is None and pool_path is None and standin:
            pool = wording.make_test_pool(C.FORM_SLOTS)
        super().__init__(seed, standin=standin, pool_path=pool_path, pool=pool, deny_check=deny_check)
        if self.pool is None:
            raise wording.PoolError("no wording pool")
        if not standin:
            wording.require_real(self.pool)
            problems = pool_problems(self.pool)
            if problems:
                raise wording.PoolError("the T63 wording pool is not usable: " + "; ".join(problems[:4]))
            if exports is not None:
                exports.require_real()
                pool_writer.refuse_fixture_sha(exports.sha, "stdlib export")         # Opus ruling Q3: a fixture sha never builds a production row
            if table is not None:
                table.require_real()
                pool_writer.refuse_fixture_sha(table.sha, "licence table")
        self.exports, self.table = exports, table
        self.kept_row_ids = None            # set by checked.run: callable -> ids of the rows that survived the drops so far (lets a refill take back a dropped row's LIC cell)
        self.picker = wording.Picker(self.pool, util.rng_for("T63-picker", seed))
        self.cells = lic.CellPicker(table, util.rng_for("T63-cells", seed)) if table is not None else None


# ---- plan ---------------------------------------------------------------------------------------------------------------------------
def _block_cells(sub, n, singles_no, pairs, extra=None):
    """Cells of one sub-block: n rows = YES singles + NO singles + 2 x pairs (a pair = a YES row and a NO row on the same source, G0-lite K7)."""
    extra = extra or {}
    n_pairs = sum(pairs.values())
    n_no_single = sum(singles_no.values())
    yes_single = max(0, n - n_no_single - 2 * n_pairs)
    cells = [dict({"sub": sub, "label": "YES", "kind": None}, **extra) for _ in range(yes_single)]
    for k, v in singles_no.items():
        cells += [dict({"sub": sub, "label": "NO", "kind": k}, **extra) for _ in range(v)]
    for k, v in pairs.items():
        cells += [dict({"sub": sub, "label": "NO", "kind": k, "pair": True}, **extra) for _ in range(v)]
    return cells


def _scaled(d, scale):
    return {k: max(0, int(round(v * scale))) for k, v in d.items()}


def _exists_cells(rows_a1, rows_a2, rows_b, rng, with_b=True):
    """EX-A1 / EX-A2 composition is given AT the Opus-ruling-Q5 design sizes (160 / 130 rows: NO kinds in singles and pairs, YES = NO) and scaled by rows / design."""
    cells = []
    s1, s2, sb = rows_a1 / 160.0, rows_a2 / 130.0, rows_b / 250.0
    cells += _block_cells("EX-A1", rows_a1, _scaled({"EX-N2": 13, "EX-N4": 14, "EX-N5": 28}, s1), _scaled({"EX-N2": 16, "EX-N4": 9}, s1))
    cells += _block_cells("EX-A2", rows_a2, _scaled({"EX-N1": 6, "EX-N3": 18, "EX-N4": 2, "EX-N5": 18}, s2), _scaled({"EX-N1": 12, "EX-N4": 9}, s2))
    if with_b:
        langs = util.largest_remainder(rows_b, {"python": 150, "node": 50, "go": 50})
        for lang, nl in langs.items():
            for view in ("B1", "B2"):
                n = nl // 2 if view == "B1" else nl - nl // 2
                f = n / 250.0
                cells += _block_cells("EX-" + view, n, _scaled({"EX-N1": 25, "EX-N4": 15, "EX-N5": 45}, f), _scaled({"EX-N1": 20, "EX-N4": 20}, f),
                                      {"lang": lang, "view": view})
    rng.shuffle(cells)
    levels = plan_mod.level_cycle(len(cells), rng, C.NON_LIC_LEVEL_WEIGHTS)             # Opus ruling Q7b: LIC is all L3, the family composition holds with it
    for c, lv in zip(cells, levels):
        c["target_level"] = lv
    return cells


LIC_KINDS = (("COMPATIBLE", "REVIEW"), ("REVIEW", "INCOMPATIBLE"), ("COMPATIBLE", "INCOMPATIBLE"))


def lic_quota(total, oversample=True):
    """LIC plan sizes for `total` kept family rows (Opus ruling Q5): kept rows per label (38 / 38 / 34 of 110 at 1,200), cells drawn per label (15% oversample, capped at
    LIC_DRAW = 44 / 44 / 40: the hashed table has 40 INCOMPATIBLE cells and a cell is used once), and the one-axis-flip pairs (>= 30% of the kept rows, >= 33 of 110)."""
    kept_n = max(1, int(round(C.BLOCK_ROWS["LIC"] * total / float(C.GENERATED_ROWS))))
    kept = util.largest_remainder(kept_n, C.LIC_ROWS)
    draw = {lab: min(C.LIC_DRAW[lab], plan_mod.oversampled(n) if oversample else n) for lab, n in kept.items()}
    pairs_kept = max(1, int(math.ceil(C.LIC_PAIR_MIN * kept_n / 2.0 - 1e-9)))
    pairs = plan_mod.oversampled(pairs_kept) if oversample else pairs_kept
    return {"kept_rows": kept_n, "kept": kept, "draw": draw, "pairs_kept": pairs_kept, "pairs": pairs}


def _lic_cells(total, rng, oversample=True):
    """LIC groups: pairs (a one-axis flip between two labels) then singles; cells are drawn at generation, stratified by LABEL only. The draw per label is the oversampled
    kept quota capped at the table's real cell counts; the pairs' labels count against the label draws."""
    q = lic_quota(total, oversample)
    alloc = util.largest_remainder(q["pairs"], {"0": 1, "1": 1, "2": 1})
    pairs = []
    for k, key in enumerate(("0", "1", "2")):
        pairs += [LIC_KINDS[k]] * alloc[key]
    rng.shuffle(pairs)
    out, used = [], {lab: 0 for lab in C.LIC_LABELS}
    for i, p in enumerate(pairs):
        out.append({"type": "pair", "labels": list(p), "axis": "mode" if i % 8 < 5 else "id"})     # 5/8 mode pairs (62.5% >= 50%)
        for lab in p:
            used[lab] += 1
    sl = [lab for lab in C.LIC_LABELS for _ in range(max(0, q["draw"][lab] - used[lab]))]
    rng.shuffle(sl)
    lv = (["L1"] * 50 + ["L2"] * 40 + ["L3"] * 30)
    rng.shuffle(lv)
    for i, lab in enumerate(sl):
        out.append({"type": "single", "label": lab, "target_level": lv[i % len(lv)], "mixed": (i % 5) < 3})
    return out


def build_plan(total=C.GENERATED_ROWS, seed=0, oversample=True, with_b=True):
    """Groups for ~`total` kept rows: NEAR / EXISTS / LIC cells scaled from the 1,200-row design, each cell oversampled by 15% (LIC: capped at the table's real cell counts)."""
    scale = total / float(C.GENERATED_ROWS) * (plan_mod.OVERSAMPLE if oversample else 1.0)
    rng = util.rng_for("T63-plan", seed)
    groups = near_plan.build_cells(int(round(C.BLOCK_ROWS["NEAR"] * scale)), seed)
    cells = _exists_cells(int(round(C.BLOCK_ROWS["EX-A1"] * scale)), int(round(C.BLOCK_ROWS["EX-A2"] * scale)),
                          int(round(C.BLOCK_ROWS["EX-B"] * scale)), rng, with_b)
    for i, c in enumerate(cells):
        groups.append({"gid": "T63-EX-%04d" % i, "seed": "ex-%d" % i, "size": 2 if c.get("pair") else 1, "head": "EXISTS", "cell": c})
    lic_groups = [{"gid": "T63-LIC-%04d" % i, "seed": "lic-%d" % i, "size": 2 if c["type"] == "pair" else 1, "head": "LIC", "cell": c}
                  for i, c in enumerate(_lic_cells(total, rng, oversample))]
    row0 = 0
    for g in lic_groups:                       # K10-F: a LIC row's index in the block = its place in gid order (pair / single structure only: no label, no cell)
        g["cell"]["row0"], row0 = row0, row0 + g["size"]
    for g in lic_groups:
        g["cell"]["rows_total"] = row0
    groups.extend(lic_groups)
    rng.shuffle(groups)
    # the LIC pairs are generated BEFORE the LIC singles (positions among the other heads unchanged): the 40 INCOMPATIBLE cells are all used, so a late pair must still
    # find an unused INCOMPATIBLE neighbour
    pos = [i for i, g in enumerate(groups) if g["head"] == "LIC"]
    for i, g in zip(pos, sorted((groups[i] for i in pos), key=lambda g: g["size"] != 2)):
        groups[i] = g
    return groups


# ---- generation ---------------------------------------------------------------------------------------------------------------------
def exists_level(spec):
    m = spec["mech"]
    kind = spec.get("kind")
    flags = [m.get("plaus")]
    kf = None
    if kind in ("EX-N1", "EX-N2"):
        kf = "high" if m.get("xhigh") else "low"
    elif kind == "EX-N3":
        kf = m.get("ver")
    elif kind == "EX-N4":
        kf = "low"
    flags.append(kf)
    return plan_mod.ladder_level(sum(1 for f in flags if f == "low"), sum(1 for f in flags if f == "high"))


def _gen_exists(ctx, g):
    c = g["cell"]
    best, last = None, None
    want = plan_mod.LEVELS.index(c["target_level"])
    for t in range(40):
        gg = dict(g, seed="%s#t%d" % (g["seed"], t))
        try:
            if c["sub"] == "EX-A1":
                specs = exists.gen_a1(ctx, dict(gg, cell=c))
                for sp in specs:
                    sp["mech"]["xhigh"] = bool(sp.get("other")) and sp["kind"] == "EX-N2" and _near_listed(sp)
            elif c["sub"] == "EX-A2":
                cell = dict(c, ver="high" if t % 2 else "low") if c["kind"] == "EX-N3" else c
                specs = exists.gen_a2(ctx, dict(gg, cell=cell))
            else:
                specs = exists.gen_b(ctx, dict(gg, cell=c))
        except exists.Reject as e:
            last = e
            continue
        for sp in specs:
            sp["level"] = exists_level(sp)
        d = abs(plan_mod.LEVELS.index(specs[-1]["level"]) - want)
        if best is None or d < best[0]:
            best = (d, specs)
        if d == 0:
            break
    if best is None:
        raise last or exists.Reject("no spec")
    return best[1]


def _near_listed(spec):
    p = spec["query_name"]
    return any(_edit_leq2(p, n) for n in spec["listing"])


def _edit_leq2(a, b):
    if abs(len(a) - len(b)) > 2:
        return False
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1] <= 2


def _generate_exists(ctx, g):
    specs = _gen_exists(ctx, g)
    pair = len(specs) == 2
    out = []
    for i, spec in enumerate(specs):
        if spec["sub"] in ("EX-B1", "EX-B2"):
            spec["export_sha"] = ctx.exports.sha
        cid = "%s:%s" % (spec["sub"], spec["kind"] or "YES")
        out.append(rows.build_record(ctx, g, spec, i, cid, pair_id=g["gid"] if pair else None,
                                     twin_of=("%s-%s" % (g["gid"], "ab"[1 - i])) if pair else None,
                                     extra_meta={"pair_kind": g["cell"].get("kind") if pair else None}))
    return out


def _generate_lic(ctx, g):
    c = g["cell"]
    tb = ctx.table
    if tb is None:
        raise ValueError("LIC rows need the hashed Opus licence table (T63-LIC-TABLE); none supplied")
    picker = ctx.cells
    rnd = int(g["gid"].split("~r")[1]) if "~r" in g["gid"] else 0
    if rnd and ctx.kept_row_ids is not None:
        picker.release_unkept(ctx.kept_row_ids(), before_round=rnd)         # Opus ruling Q5: the cell of a dropped row is free again for this refill
    # K10-F: the row index of the format draw. A refill (round rnd) takes a fresh index range, so a retired group is never re-worded.
    gnum = int(g["gid"].split("~r")[0].split("-")[-1])
    row0 = c["row0"] if "row0" in c else 2 * gnum
    rows_total = c.get("rows_total", 2 * (gnum + 1))
    cells = []
    try:
        if c["type"] == "pair":
            la, lb = c["labels"]
            cell_a, cell_b = _pair_cells(picker, tb, c["axis"], la, lb)
            cells, twin = [cell_a, cell_b], True
        else:
            flag = {"L1": None, "L2": "low", "L3": "high", "L4": "high"}[c["target_level"]]
            try:
                cell = picker.single(c["label"], want_mixed=c["mixed"] or None, flag=flag)
            except lic.Reject:
                cell = picker.single(c["label"])
            cells, twin = [cell], False
        recs = []
        for i, cell in enumerate(cells):
            flag = picker.flag(cell)
            level = plan_mod.ladder_level(1 if flag == "low" else 0, 1 if flag == "high" else 0)
            spec = {"head": "LIC", "dep": cell[0], "project": cell[1], "use": cell[2], "dist": cell[3], "label": tb.label(*cell), "level": level,
                    "mech": {"cell": flag}, "table_sha": tb.sha, "axis": c.get("axis"),
                    "mixed_pair": picker.mixed(cell)}
            recs.append(rows.build_record(ctx, g, spec, i, "LC:%s" % lic.key(*cell), pair_id=g["gid"] if twin else None,
                                          twin_of=("%s-%s" % (g["gid"], "ab"[1 - i])) if twin else None,
                                          extra_meta={"card_layout": C.LIC_CARD_LAYOUT, "field_order": C.LIC_FIELD_ORDER},
                                          lic_index=row0 + i + rnd * rows_total))
    except Exception:
        picker.release(cells)                                                  # a builder error after the draw gives the cells back
        raise
    for rec, cell in zip(recs, cells):
        picker.register(rec["row_id"], rec["group_id"], cell, rnd)
    return recs


def _pair_cells(picker, tb, axis_kind, la, lb):
    axes = ("use", "dist") if axis_kind == "mode" else ("dep", "proj")
    lst = picker._by_label[la]
    for _ in range(min(len(lst), 600)):
        cell = lst[picker._ptr[la] % len(lst)]
        picker._ptr[la] += 1
        if cell in picker.used:
            continue
        nbs = [nb for ax, nb in tb.neighbours(cell) if ax in axes and nb not in picker.used and tb.label(*nb) == lb]
        if nbs:
            other = picker.rng.choice(sorted(nbs))
            picker.used.update((cell, other))
            return cell, other
    raise lic.Reject("no pair")


def _generate_near(ctx, g):
    last = None
    for t in range(12):
        try:
            gg = dict(g, seed="%s#t%d" % (g["seed"], t))
            specs = near_build.build_group(ctx, gg)
            break
        except near_build.Reject as e:
            last = e
    else:
        raise last
    rng = ctx.rng("fmt", g["seed"])
    fmt = rng.choice(C.SNAPSHOT_FORMATS)
    pair = len(specs) == 2
    out = []
    for i, s in enumerate(specs):
        cid = s.get("relation") or s.get("no_kind")
        if s.get("relation") and s.get("no_kind"):
            cid = s["no_kind"]
        extra = {"label_kind": s["label"], "t8_variant": s.get("t8_variant"), "flip_field": s.get("flip_field"),
                 "relation": s.get("relation"), "no_kind": s.get("no_kind")}
        out.append(rows.build_record(ctx, g, s, i, cid, fmt=fmt, pair_id=g["gid"] if pair else None,
                                     twin_of=("%s-%s" % (g["gid"], "ab"[1 - i])) if pair else None, extra_meta=extra))
    return out


def generate_group(ctx, g):
    if g["head"] == "NEAR":
        return _generate_near(ctx, g)
    if g["head"] == "EXISTS":
        return _generate_exists(ctx, g)
    return _generate_lic(ctx, g)
