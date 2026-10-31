"""F9 repair r2: visible option kinds and yes/no question-ID features of a finished row (C_DATA_SPEC 8 G6 / G7: option
kinds = abstain kind, longest / shortest, numeric max / min, in the text, first / last in the text among the options,
named in the question, record-set size and closest-to-the-others set (F9-A35); yes/no: the question's looked-up ID
listed / unlisted, above / below every listed ID of its prefix, on the first / last ID line), read from the rendered
row exactly as a reader sees it. The builder keeps, per cell, the running gold-minus-chance residual of each kind
(choice rows) and the yes-minus-no count of each ID feature (yes/no rows) inside a bound by accept / reject
(CardBuilder.kind_ok / cell_ok), the same way it holds P(yes) per wording x k_all (R3-SC2) and per frame (r1b)."""
import re

ID_RX = re.compile(r"\b([A-Z][A-Z0-9]{0,6})-(\d{2,7})\b")
_NUM = re.compile(r"[$€£¥]?\s?(-?\d+(?:\.\d+)?)(?:\s*[A-Za-z%°/][A-Za-z%°/ ]{0,19})?")
KIND_BOUND, KIND_Z = 1.5, 1.0  # per shard and cell: a row may not push |gold hits - sum of m/k| past
# KIND_BOUND + KIND_Z x the cell's chance sd (a row that moves the residual back toward 0 is always kept)


def abstain_kind(o):
    o = o.strip()
    if o == "none of these":
        return "none_of_these"
    if o == "cannot be determined":
        return "cbd"
    if o.startswith("no such "):
        return "no_record"
    if o.startswith("two or more ") and o.endswith(" tie"):
        return "tie"
    return None


def as_num(o):
    m = _NUM.fullmatch(o.strip().replace(",", ""))
    return float(m.group(1)) if m else None


def first_pos(state, o):
    if len(o) < 2:
        return -1
    m = re.search(r"(?<![\w-])" + re.escape(o) + r"(?![\w-])", state)
    return m.start() if m else -1


def set_ids(o):
    if not o.endswith(" only"):
        return None
    parts = re.split(r",\s*(?:and\s+)?|\s+and\s+", o[:-5])
    return frozenset(p.strip() for p in parts if p.strip())


def opt_kinds(state, opts, qtext):
    """Per option, the set of its visible kinds (as a reader of the rendered row sees them)."""
    ls = [len(o) for o in opts]
    q = (qtext or "").lower()
    nums = [as_num(o) for o in opts]
    nv = [x for x in nums if x is not None]
    pos = [first_pos(state, o) for o in opts]
    ok = sorted(p for p in pos if p >= 0)
    sets = [set_ids(o) for o in opts]
    if sum(x is not None for x in sets) >= 2:
        sets = [frozenset() if (x is None and abstain_kind(o) == "no_record") else x for x, o in zip(sets, opts)]
    sv = [x for x in sets if x is not None]
    cen, dist = None, None
    if len(sv) >= 3:
        dist = [sum(len(a ^ b) for b in sv) if a is not None else None for a in sets]
        cen = min(d for d in dist if d is not None)
    out = []
    for i, o in enumerate(opts):
        k = set()
        ak = abstain_kind(o)
        if ak:
            k.add("abstain")
            k.add("abstain_" + ak)
        if ls[i] == max(ls):
            k.add("longest")
        if ls[i] == min(ls):
            k.add("shortest")
        if nums[i] is not None and len(nv) >= 2:
            if nums[i] == max(nv):
                k.add("num_max")
            if nums[i] == min(nv):
                k.add("num_min")
        if pos[i] >= 0:
            k.add("in_text")
            if len(ok) >= 2:
                if pos[i] == ok[0]:
                    k.add("first_in_text")
                if pos[i] == ok[-1]:
                    k.add("last_in_text")
        if len(o) >= 3 and o.lower() in q:
            k.add("in_question")
        if sets[i] is not None:
            k.add(f"set_size={len(sets[i])}")
            if cen is not None and dist[i] == cen:
                k.add("set_center")
        out.append(k)
    return out


def kind_deltas(row, side, frame):
    """{cell: (gold-hit minus m/k, chance variance)} of a finished choice row; cells = kind, (frame, kind), (depth, kind), (k, kind)."""
    opts = list(row.get("options") or [])
    if not opts or row["gold"] not in opts:
        return {}
    k = len(opts)
    kinds = opt_kinds(row["state"], opts, side.get("qtext") or "")
    gi = opts.index(row["gold"])
    kb = str(k) if k <= 5 else ("6-9" if k <= 9 else "10+")
    dep = str(row["meta"].get("depth"))
    allk = set().union(*kinds)
    out = {}
    for kd in allk:
        m = sum(kd in x for x in kinds)
        d = (1.0 if kd in kinds[gi] else 0.0) - m / k
        for c in (("K", kd), ("F", frame, kd), ("D", dep, kd), ("B", kb, kd)):
            out[c] = (d, (m / k) * (1 - m / k))
    return out


def kind_bad(res, var, deltas):
    """Cells a row would push past the bound KIND_BOUND + KIND_Z * sd (sd = the cell's running chance sd), only when
    the row moves the residual away from 0."""
    bad = []
    for c, (d, w) in deltas.items():
        r0 = res.get(c, 0.0)
        r1 = r0 + d
        if abs(r1) > KIND_BOUND + KIND_Z * var.get(c, 0.0) ** 0.5 and abs(r1) > abs(r0) + 1e-9:
            bad.append(c)
    return bad


def yn_id_feats(state, qtext):
    """Visible looked-up-ID features of a yes/no row (the G7 nuisance features of 1.9 / 5)."""
    qids = list(ID_RX.finditer(qtext or ""))
    if not qids:
        return []
    qi, pre = qids[0].group(0), qids[0].group(1)
    same = [int(m.group(2)) for m in ID_RX.finditer(state) if m.group(1) == pre]
    f = ["qid_listed" if qi in state else "qid_unlisted"]
    if same and int(qids[0].group(2)) > max(same):
        f.append("qid_above_all")
    if same and int(qids[0].group(2)) < min(same):
        f.append("qid_below_all")
    firsts = [m.group(0) for m in (ID_RX.search(ln) for ln in state.split("\n")) if m]
    if firsts:
        if firsts[0] == qi:
            f.append("qid_first_line")
        if firsts[-1] == qi:
            f.append("qid_last_line")
    return f
