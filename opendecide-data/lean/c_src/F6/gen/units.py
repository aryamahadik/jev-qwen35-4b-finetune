"""Unit planning (repair r1): row specs of one (card, form) -> unit specs (single / T1 premise pair / Q-DET negation
triple / attack pair), with labels planned per (card, frame) and twins that consume a spec of the same frame, k and
display, so that every frame, display and gold-class marginal keeps its planned value (G10, G6a; F6-QC-3/7/11).

Rules (G0 s1, s6; C_DATA_SPEC 2.1):
- Frames are allocated first (label-free), then labels: per (card, frame) the yes count is round(n_f x card rate),
  so the per-card rate is the drawn U[20, 80] rate and every frame sits at the card-weighted rate (complementary
  card pairs keep the aggregate at 50%).
- A premise pair is one open row and its settled twin in the SAME frame (1 yes + 1 no). A triple is qdet (L),
  qdet_leave (1 - L), qdet_dneg (L). An attack pair is two rows of one frame and one label.
- Attack, premise and triple choices never read a label (attack is drawn before the gold class is looked at).
- n_gaps is drawn per unit from one distribution for every role (s6 'Gaps'); the settled rows of pass 2 take the
  full gap signature (kind@position multiset) of an open row of the same card and n (build.run).
"""
from __future__ import annotations

from .common import rng_for

YN = ("qdet", "qest", "qplain")
P_TRIPLE = 0.24       # share of Q-DET rows that sit in a negation triple (x 3 rows)
P_PREMISE_YN = 1.0   # share of open-label yes/no rows (premise-capable frames) that get a settled twin
P_PREMISE_CH = 1.0   # share of NEI-gold C-OUT / C-REC rows and gap-gold C-GAP rows that get a settled twin
P_PREMISE_CGAP = False  # repair r1 v3f: C-GAP takes no premise sets (see plan_choice)
P_TWIN2_YN = 1.0      # repair r1 v3c (G10 twin share 22 +/- 2): share of premise pairs that take a SECOND settled twin
P_TWIN2_CH = 1.0      # from a settled spec of the same frame (yes/no) or k / display / gold class (choice) left as a
                      # single; the set is one open base + two label-flip twins (XF03 contrast set; own call_ids)
MAX_EXTRA_YN = 2      # repair r1 v3f: 2 (C-GAP sets removed, twin share); v3e (G10 twin share 18.1% < 20 on the v3d pool): settled twins beyond the second,
MAX_EXTRA_CH = 1      # taken from the settled specs still left (same frame / same k-display-gold key) while any are
                      # left; twin 2 probability 0.75 -> 1.0. Label-free: twins only consume planned specs.
P_ATTACK = 0.10       # share of units on attack cards that become an attack pair (label-free)
PREMISE_FRAMES = ("qdet", "qdet_leave", "qdet_imp", "qdet_dneg", "qest_est", "qest_show", "qest_det")


def n_gaps_draw(rng, form, k=None, table=False, sampler=None):
    if form == "c_gap":
        return k - 1
    if sampler == "S2":                 # every S2 row: two gaps (open: witness + case-split trap; settled: two traps)
        return 2
    if table == "pure":                 # repair r1 v3c: a pure outcome-table card has one off-path attribute, so a settled
        return 1                        # row can show one gap; open and settled rows there both show exactly one (s6)
    if table:
        return rng.choices([1, 2], weights=[0.55, 0.45])[0]
    return rng.choices([1, 2, 3], weights=[0.4, 0.35, 0.25])[0]


def _alloc(n, weights: dict, rng) -> list:
    """Proportional allocation of n rows to frames (largest remainder), shuffled."""
    tot = sum(weights.values())
    raw = {f: n * w / tot for f, w in weights.items()}
    cnt = {f: int(v) for f, v in raw.items()}
    rest = sorted(weights, key=lambda f: -(raw[f] - cnt[f]))
    for f in rest[: n - sum(cnt.values())]:
        cnt[f] += 1
    out = [f for f, c in cnt.items() for _ in range(c)]
    rng.shuffle(out)
    return out


def frame_weights(form, frames):
    if form == "qdet":
        w = {"qdet": 0.50, "qdet_dneg": 0.25}
        if "qdet_imp" in frames:
            w.update({"qdet_leave": 0.15, "qdet_imp": 0.10})
        else:
            w["qdet_leave"] = 0.25
        return w
    if form == "qest":
        w = {"qest_det": 0.30}
        if "qest_show" in frames:
            w.update({"qest_est": 0.45, "qest_show": 0.25})
        else:
            w["qest_est"] = 0.70
        return w
    return {"qplain_true": 1.0}


def open_label(frame):
    """The label of an open (|T| = 2) row in this frame."""
    return 1 if frame in ("qdet_leave", "qdet_imp") else 0


def plan_yn(specs, card, rate, tag, twins=True):
    form = specs[0]["form"]
    rng = rng_for("plan_yn", tag, card["card_id"], form)
    frames = _alloc(len(specs), frame_weights(form, card.get("frames") or []), rng)
    rows = [dict(sp, frame=fr) for sp, fr in zip(specs, frames)]
    by = {}
    for i, r in enumerate(rows):
        by.setdefault(r["frame"], []).append(i)
    used = set()
    units = []
    # --- triples (Q-DET only, cards whose S can take 'not' on one atom)
    if twins and form == "qdet" and card.get("triple_ok", True):
        nt = min(int(P_TRIPLE * len(rows)), len(by.get("qdet", [])), len(by.get("qdet_leave", [])),
                 len(by.get("qdet_dneg", [])))
        for j in range(nt):
            a, b, c = by["qdet"][j], by["qdet_leave"][j], by["qdet_dneg"][j]
            used |= {a, b, c}
            units.append({"twin": "triple", "idx": [a, b, c]})
    # --- attack pairs (label-free), then premise pairs, then singles
    free = [i for i in range(len(rows)) if i not in used]
    att = bool(card.get("attack")) and twins
    pending = {}
    for i in free:
        pending.setdefault(rows[i]["frame"], []).append(i)
    for fr, ix in pending.items():
        ix = list(ix)
        while ix:
            i = ix.pop(0)
            if att and ix and rng.random() < P_ATTACK:
                units.append({"twin": "attack", "idx": [i, ix.pop(0)]})
            else:
                units.append({"twin": None, "idx": [i]})
    # --- labels: per frame yes target, triples first, then fill singles/attacks
    Y = {f: round(len(ix) * rate) for f, ix in by.items()}
    lab = {}
    for u in units:
        if u["twin"] == "triple":
            L = 1 if rng.random() < rate else 0
            a, b, c = u["idx"]
            lab[a], lab[b], lab[c] = L, 1 - L, L
    got = {f: sum(lab.get(i, 0) for i in ix) for f, ix in by.items()}
    slots = [u for u in units if u["twin"] in (None, "attack")]
    rng.shuffle(slots)
    for u in slots:
        f = rows[u["idx"][0]]["frame"]
        need = Y[f] - got[f]
        w = len(u["idx"])
        L = 1 if need >= w or (need > 0 and rng.random() < need / w) else 0
        for i in u["idx"]:
            lab[i] = L
        got[f] += L * w
    # --- premise pairs: an open-label single + a settled-label single of the same frame -> one pair unit
    singles = {}
    for u in units:
        if u["twin"] is None:
            i = u["idx"][0]
            singles.setdefault((rows[i]["frame"], lab[i]), []).append(u)
    for fr in PREMISE_FRAMES:
        ol = open_label(fr)
        op = singles.get((fr, ol), [])
        st = singles.get((fr, 1 - ol), [])
        # Q-EST: open No rows are half of the No rows (G0 s6), so at most half of them take a settled twin
        share = 0.5 if fr.startswith("qest") else P_PREMISE_YN
        npair = min(int(round(share * len(op))), len(st)) if twins else 0
        for j in range(npair):
            uo, us = op[j], st[j]
            uo["twin"] = "premise"
            uo["idx"] = [uo["idx"][0], us["idx"][0]]
            us["twin"] = "_merged"
        if twins:                          # repair r1 v3c/v3e: extra settled twins from the settled singles left
            pairs = [u for u in op[:npair]]    # in this frame, one per pair per level (twin 2, then 3, ...)
            left = st[npair:]
            for lev in range(1 + MAX_EXTRA_YN):
                for uo in pairs:
                    if not left:
                        break
                    if len(uo["idx"]) == 2 + lev and rng.random() < P_TWIN2_YN:
                        us = left.pop(0)
                        uo["idx"].append(us["idx"][0])
                        us["twin"] = "_merged"
    units = [u for u in units if u["twin"] != "_merged"]
    # --- wants (T targets): Q-DET settled 50/50 true/false; Q-EST No 50/50 refuted/open
    cnt_tf = [0]
    qest_open_from_pairs = sum(1 for u in units if u["twin"] == "premise" and form == "qest")
    qest_no = sum(1 for i in range(len(rows)) if lab[i] == 0) if form == "qest" else 0
    open_budget = [max(0, qest_no // 2 - qest_open_from_pairs)]

    def want_of(i, role_hint=None):
        fr, L = rows[i]["frame"], lab[i]
        if form == "qdet":
            is_open = (L == open_label(fr))
            if is_open:
                return "open"
            cnt_tf[0] += 1
            return "true" if cnt_tf[0] % 2 else "false"
        if form == "qest":
            if L == 1:
                return "true"
            if role_hint == "open":
                return "open"
            if open_budget[0] > 0:
                open_budget[0] -= 1
                return "open"
            return "false"
        return "true" if L == 1 else "false"

    out = []
    for u in units:
        ix = u["idx"]
        base = dict(rows[ix[0]])
        base.update(label=lab[ix[0]], twin=u["twin"], consumes=[rows[i]["sid"] for i in ix])
        if u["twin"] == "premise":
            base["want"] = "open"
            base["twin_want"] = want_of(ix[1])
            base["twin_label"] = lab[ix[1]]
            if len(ix) >= 3:
                base["twin2"] = True
                base["twin2_want"] = want_of(ix[2])
                base["twin2_label"] = lab[ix[2]]
                base["twin_x"] = [[want_of(i), lab[i]] for i in ix[3:]]     # repair r1 v3e: twins 3, 4, ...
        elif u["twin"] == "triple":
            base["want"] = want_of(ix[0])
            base["frames3"] = [rows[i]["frame"] for i in ix]
        else:
            base["want"] = want_of(ix[0])
        base["role"] = "open" if base["want"] == "open" else "settled"
        base["n_gaps"] = n_gaps_draw(rng_for("ngaps", tag, base["sid"]), form, table=("pure" if (card.get("P") or {}).get("pure_table") else bool(card.get("table"))),
                                     sampler=card.get("sampler"))
        out.append(base)
    return out


def plan_choice(specs, card, tag, twins=True):
    form = specs[0]["form"]
    rng = rng_for("plan_ch", tag, card["card_id"], form)
    att = bool(card.get("attack")) and twins       # every choice form (G10: attack vs gold class over choice rows)
    rows = [dict(s) for s in specs]
    order = list(range(len(rows)))
    rng.shuffle(order)
    key = (lambda r: (r.get("k"), r.get("nei"), r.get("none"), r.get("gold")))
    pool = {}
    for i in order:
        pool.setdefault(key(rows[i]), []).append(i)
    used = set()
    out = []

    def take(k):
        lst = pool.get(k, [])
        while lst:
            j = lst.pop()
            if j not in used:
                used.add(j)
                return j
        return None

    for i in order:
        if i in used:
            continue
        used.add(i)
        r = rows[i]
        u = dict(r, twin=None, consumes=[r["sid"]])
        if att and rng.random() < P_ATTACK:                      # label-free: drawn before the gold class is read
            u["twin"] = "attack"         # the attack twin is an extra row (it consumes no spec), so attack presence
                                         # never depends on the gold class or on a matching spec being left
        if u["twin"] is None:
            # repair r1 v3f (G7 'opt:of'): no premise sets on C-GAP. A C-GAP trap arm needs a gap of the decisive
            # gap's kind at its position, which only value gaps find, so every realised C-GAP set had a value-gap gold
            # ('the value of the A of E'; 24 of 24 v3e set bases vs 1/(k-1) expected) while the balance weights
            # (gen/cgap_balance.json) are fitted on single records. C-GAP open rows need no twin row (G0 s8, M13).
            prem_gold = {"c_out": "nei", "c_rec": "nei", "c_gap": "gap" if P_PREMISE_CGAP else None}.get(form)
            if twins and prem_gold and r.get("gold") == prem_gold and rng.random() < P_PREMISE_CH:
                tw_gold = "nothing" if form == "c_gap" else "concrete"
                j = take((r.get("k"), r.get("nei"), r.get("none"), tw_gold))
                if j is not None:
                    u["twin"] = "premise"
                    u["consumes"].append(rows[j]["sid"])
        g = r.get("gold")
        if form in ("c_out", "c_rec"):
            u["role"] = {"concrete": "settled", "nei": "open"}.get(g) or \
                ("open" if rng_for("none_role", tag, r["sid"]).random() < 0.5 else "settled")
        elif form == "c_gap":
            u["role"] = "open" if g == "gap" else "settled"
        else:
            u["role"] = "case"
        u["n_gaps"] = n_gaps_draw(rng_for("ngaps", tag, r["sid"]), form, r.get("k"), table=("pure" if (card.get("P") or {}).get("pure_table") else bool(card.get("table"))),
                                  sampler=card.get("sampler"))
        out.append(u)
    if twins:
        # repair r1 v3c/v3e: twins 2, 3, ... are added only after every base has its first twin, level by level, from
        # the settled singles of the same k / display / gold-class key still left (a scarce key, e.g. C-GAP
        # 'nothing', is never spent on one base's extra twins while another base has none). Label-free.
        free = {}
        for u in out:
            if u.get("twin") is None:
                free.setdefault((u.get("k"), u.get("nei"), u.get("none"), u.get("gold")), []).append(u)
        tw_gold = "nothing" if form == "c_gap" else "concrete"
        prem = [u for u in out if u.get("twin") == "premise"]
        drop = set()
        for lev in range(1 + MAX_EXTRA_CH):
            for u in prem:
                key = (u.get("k"), u.get("nei"), u.get("none"), tw_gold)
                if len(u["consumes"]) != 2 + lev or not free.get(key) or rng.random() >= P_TWIN2_CH:
                    continue
                v = free[key].pop()
                drop.add(id(v))
                u["consumes"].append(v["sid"])
                if lev == 0:
                    u["twin2"] = True
                else:
                    u.setdefault("twin_x", []).append([None, None])
        out = [u for u in out if id(u) not in drop]
    return out
