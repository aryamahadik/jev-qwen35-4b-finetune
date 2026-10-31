"""F6 build driver: candidates (1.5x r1), the G6 QC sample, and the S5 mix-tuning dev items.

  python -m gen.build <set> [--workers 8] [--limit N]      set in {cand, qc, dev}

Each unit (one row, a premise-twin pair, a Q-DET negation triple or an attack pair) is built, rendered by fmt1,
loader-checked, length-checked and round-tripped through the G3 parser + solver B inside the worker. Length overruns
are rejected and redrawn (G0 s1); a G3 failure is logged as a generator bug and the unit is not emitted.
"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import random
import time
import traceback
from collections import Counter

from . import common as C
from .common import rng_for, OUT, TMP, progress, write_jsonl, TOKEN_CAP, TOKEN_CAP_A22, A22_ROUND
from . import plan

YN = ("qdet", "qest", "qplain")
SETS = {"cand": {"scale": 1.5, "tag": "cand"}, "qc": {"scale": 1.65, "tag": "qc"}, "dev": {"scale": 1.0, "tag": "dev"}}

_CTX = {}


def _init():
    from . import packs_f6, styles_f6, toklen
    _CTX["W"] = {w["text"] for w in styles_f6.wording_pool()}
    toklen.tok()


def _card(cd: dict):
    key = cd["card_id"]
    if key not in _CTX:
        from . import packs_f6
        pk = packs_f6.pack(cd["pack"])
        smp, schema = cd["sampler"], cd["schema"]
        if smp == "S5":
            from . import s5
            _CTX[key] = s5.make_card(key, schema, pk)
        elif smp in ("S1", "S2"):
            from . import s_rules
            _CTX[key] = s_rules.make_card(key, smp, "c_out" if schema == "c_out_t" else schema, pk,
                                         table=schema == "c_out_t")
        elif smp == "S3":
            from . import s3
            _CTX[key] = s3.make_card(key, schema, pk)
        else:
            from . import s4
            _CTX[key] = s4.make_card(key, schema, pk)
    wof = cd.get("wording_of")
    if wof and _CTX[key].get("_wording_of") != wof:     # repair r1 v3b: complementary-rate pair shares one set
        from . import styles_f6 as ST
        _CTX[key]["wordings"] = ST.card_wordings(wof, True)
        _CTX[key]["_wording_of"] = wof
    return _CTX[key]


def pair_wordings(cards: list, yr: dict) -> int:
    """Repair r1 v3b (G10 yes rate per wording): yes/no cards whose drawn rates are complementary (r, 1 - r; the
    multiset is kept by plan.yes_rates / rate_assign) share one wording set, so every wording's aggregate yes rate is
    the mean of r and 1 - r. Label-free at row level; returns the number of pairs."""
    yn = sorted((c for c in cards if c["schema"] == "yn" and c["card_id"] in yr), key=lambda c: c["card_id"])
    free = list(yn)
    n = 0
    while free:
        a = free.pop(0)
        ra = yr[a["card_id"]]
        if abs(ra - 0.5) < 1e-9:
            continue
        j = min(range(len(free)), key=lambda i: abs(yr[free[i]["card_id"]] - (1 - ra)), default=None)
        if j is None or abs(yr[free[j]["card_id"]] - (1 - ra)) > 1e-6:
            continue
        b = free.pop(j)
        b["wording_of"] = a["card_id"]
        n += 1
    return n


def card_profile(card: dict) -> tuple:
    """Card-level text features (switch-set drivers) used to pair cards for complementary yes rates."""
    out = []
    P = card.get("P") or {}
    for k in ("world", "unless", "onlyif", "exc", "sub", "mode", "cmp_family", "order_gaps", "date_style"):
        if k in P:
            out.append(f"P.{k}={P[k]}")
    if P.get("ev_tag"):
        out.append(f"tag.counts={P['ev_tag'].get('counts')}")
    for k in ("world", "cls", "member", "blank", "cmp_family", "ambiguous", "plans", "date_style", "defs_style"):
        if k in card:
            out.append(f"{k}={card[k]}")
    for k in card.get("kinds") or []:
        out.append(f"kind={k}")
    for q in card.get("qs") or []:
        out.append(f"round={q.get('R')}")
    return tuple(sorted(out))


def shape_key(card: dict) -> tuple:
    """Card features that decide which gap kinds a card can show (world, card mode, tag, plans, units)."""
    P = card.get("P") or {}
    return (card.get("world") or P.get("world"), P.get("mode"), bool(P.get("ev_tag")), card.get("cls"),
            card.get("plans"), card.get("ambiguous"), bool(P.get("unless")), bool(P.get("onlyif")))


def group_of(form: str) -> str:
    return "yn" if form in YN else form


def unit_specs(spec_group: list, card: dict, yes_rate: float | None, set_tag: str) -> list:
    """Row specs of one (card, form) -> unit specs (gen.units: frames and labels planned per card and frame, twins
    consume a spec of the same frame / k / display, n_gaps drawn for every role alike)."""
    from . import units as U
    form = spec_group[0]["form"]
    twins = set_tag != "dev"
    if form in YN:
        us = U.plan_yn(spec_group, card, yes_rate if yes_rate is not None else 0.5, set_tag, twins=twins)
    else:
        us = U.plan_choice(spec_group, card, set_tag, twins=twins)
    return _wording_slots(us, card, form, set_tag)


def _wording_slots(us: list, card: dict, form: str, set_tag: str) -> list:
    """Repair r1 v3b (G10 yes rate per wording, G11 >= 5 wordings per card): each planned row gets a wording slot by
    rotation inside its card, never by hash. Yes/no rows rotate per planned label (each wording carries the card's
    own yes rate; complementary-rate cards share one wording set, run()), choice rows rotate over the card's rows in
    plan order (gold classes are drawn independently of the order). emit.pick_wording reads spec['wslots'][ridx]."""
    from .common import h64
    nw = max(1, len(card.get("wordings") or []))
    cnt = {}
    for u in us:
        n_rows = max(1, len(u.get("consumes") or [u.get("sid")]))
        if form in YN:
            L = u.get("label", 0)
            tw = u.get("twin")
            tl = u.get("twin_label", 1 - L)   # v3c: rows are [settled twin, open base] for a pair and
            labs = (([L, tl, u.get("twin2_label", tl)] + [tl if x[1] is None else x[1] for x in u.get("twin_x", [])]
                     if u.get("twin2") else [tl, L]) if tw == "premise"
                    else [L, 1 - L, L] if tw == "triple" else [L] * n_rows)   # [open base, twin, twin 2] for a set of 3
        else:
            labs = ["c"] * n_rows
        slots = []
        for lb in labs:
            c = cnt.get(lb)
            if c is None:
                c = h64("wslot", set_tag, card["card_id"], form, str(lb)) % nw
            slots.append(c % nw)
            cnt[lb] = c + 1
        u["wslots"] = slots
    return us


class UnitTimeout(Exception):
    pass


def _alarm(signum, frame):
    raise UnitTimeout("unit time limit")


def build_one(args):
    """Worker: build, render and gate one unit within a time limit (a slow draw is redrawn in a later round)."""
    import signal
    import time as _t
    t0 = _t.time()
    # a CPU-time limit (ITIMER_PROF), so a loaded machine does not turn slow wall-clock into failed units
    signal.signal(signal.SIGPROF, _alarm)
    signal.setitimer(signal.ITIMER_PROF, 6.0)
    try:
        try:
            r = _build_one(args)
        finally:
            signal.setitimer(signal.ITIMER_PROF, 0)
    except UnitTimeout:           # also a late alarm that lands in the finally clause
        r = {"ok": False, "why": "timeout", "sid": args[1]["sid"]}
    r["secs"] = round(_t.time() - t0, 2)
    return r


def _build_one(args):
    """Build, render and gate one unit. Returns {"ok", "rows", "sides", "rels", "why"}."""
    cd, sp, set_tag, git_sha = args
    if not _CTX:
        _init()
    from . import emit as E, gates, toklen
    card = _card(cd)
    smp = cd["sampler"]
    last = None
    for attempt in range(2):
        uid = f"{sp['sid']}-r{sp.get('round', 0)}-a{attempt}"
        try:
            if smp in ("S1", "S2", "S5"):
                from . import s_rules
                shape = None
                if smp == "S2":
                    from . import s2
                    shape = s2.shape
                recs = s_rules.build_rules_unit(card, sp, uid, shape=shape)
            elif smp == "S3":
                from . import s3
                recs = s3.build_unit(card, sp, uid)
            else:
                from . import s4
                recs = s4.build_unit(card, sp, uid)
        except Exception as e:  # noqa: BLE001  (Skip / Reject / Drop: redraw)
            last = f"build:{type(e).__name__}:{str(e)[:80]}"
            continue
        base_id = f"F6{set_tag}-{sp['sid']}"
        depth = max(r.get("depth", 1) for r in recs)
        rows, sides, rels = [], [], []
        ok = True
        for i, rec in enumerate(recs):
            rec["ridx"] = i
            rid = f"{base_id}-{i}"
            shared = sp["twin"] in ("triple", "attack")
            ids = {"id": rid, "group_id": base_id, "call_id": base_id if shared else f"{base_id}-c{i}",
                   "block": base_id, "seed": C.h64(C.BASE_SEED, uid), "depth": depth, "deep": False,
                   "git_sha": git_sha, "role": "twin" if i > 0 else "base"}
            if i > 0:
                ids["twin_of"] = f"{base_id}-0"
                ids["twin_kind"] = {"premise": "premise", "attack": "attack"}.get(sp["twin"]) or \
                    ("neg" if rec.get("rel") == "complement" else "dneg")
            try:
                if smp == "S5":
                    from . import s5
                    row, side = s5.emit(card, rec, ids)
                elif smp in ("S1", "S2"):
                    row, side = E.emit_rules(card, rec, ids)
                elif smp == "S3":
                    from . import s3
                    row, side = s3.emit(card, rec, ids)
                else:
                    from . import s4
                    row, side = s4.emit(card, rec, ids)
            except Exception as e:  # noqa: BLE001
                last = f"emit:{type(e).__name__}:{str(e)[:100]}"
                ok = False
                break
            n = toklen.row_len(row)
            cap = sp.get("cap", TOKEN_CAP)     # repair r1 v3d: A22 fallback cap on late rounds (see _rounds)
            if n > cap:
                last = f"length:{n}"
                ok = False
                break
            pt = toklen.prompt_len(row)
            if pt > cap:                 # repair r1: the prompt the model sees (decoder_io.user_msg) also <= cap
                last = f"length:prompt:{pt}"
                ok = False
                break
            side["tokens"] = n
            side["prompt_tokens"] = pt
            side["spec"] = {k: v for k, v in sp.items() if k not in ("consumes", "sig_pool")}
            g3 = gates.g3_row(row, side, _CTX["W"])
            side["g3"] = g3
            if g3:
                return {"ok": False, "why": "G3:" + "; ".join(g3)[:300], "g3_bug": True, "sid": sp["sid"]}
            rows.append(row)
            sides.append(side)
        if not ok:
            continue
        if sp["twin"] in ("triple", "attack") and len(rows) > 2 and \
                any(max(sd.get("tokens", 0), sd.get("prompt_tokens", 0)) >= 2000 for sd in sides):
            last = "length:long-unit"         # spec: a call unit with a row >= 2,000 tokens holds <= 2 rows (G15)
            continue
        if sp["twin"] == "triple":
            rels = [{"a": rows[0]["id"], "b": rows[1]["id"], "type": "complement"},
                    {"a": rows[0]["id"], "b": rows[2]["id"], "type": "equiv"}]
        elif sp["twin"] == "attack":
            rels = [{"a": rows[0]["id"], "b": rows[1]["id"], "type": "inv"}]
        return {"ok": True, "rows": rows, "sides": sides, "rels": rels, "sid": sp["sid"]}
    return {"ok": False, "why": last, "sid": sp["sid"]}


def sig_of(side: dict) -> tuple:
    """Gap signature of a row: the sorted kind@position multiset of its visible gaps (s6 'Gaps')."""
    return tuple(sorted(f"{k}@{p}" for k, p in zip(side.get("gap_kinds") or [], side.get("gap_positions") or [])))


def is_open(side: dict) -> bool:
    f = side["form"]
    if f in YN:
        return bool(side.get("t_set")) and len(side["t_set"]) == 2
    if f in ("c_out", "c_rec"):
        return len(side.get("p_set") or []) >= 2
    if f == "c_gap":
        return side.get("gold_class") == "gap"
    return False


CH_SET_FORMS = ("c_out", "c_rec")
DEGRADE = {4: "extras", 6: "twin2", 8: "split"}   # round -> what a still-failing C-OUT / C-REC premise set gives up


def settled_single(cd, us, j, set_tag):
    """Repair r1 v3f (G10 abstain display per k): the j-th consumed spec of a C-OUT / C-REC premise set, as its own
    settled single. A twin consumes a planned spec of the same k, display and gold class 'concrete' (units.plan_choice),
    so when that twin is not realised the spec is built as a single instead of being lost: every planned display and
    gold-class count is kept (v3e lost 59 NEI-shown rows at k 3-6 with failed sets: NEI shown 0.185 at k = 3 vs 0.30).
    Same spec fields, own sid, own n_gaps draw (same distribution as every row, units.n_gaps_draw), the wording slot
    planned for that row; built in pass 2 with the gap signature of an open row like every settled row."""
    from . import units as U
    card = _card(cd)
    sid = us["consumes"][j]
    u = {k: v for k, v in us.items() if k not in ("twin2", "twin_x", "consumes", "wslots", "sig", "sig_pool", "round",
                                                   "cap")}
    u.update(sid=sid, seed=C.h64("single", sid) % (1 << 31), twin=None, consumes=[sid], role="settled",
             gold="concrete", wslots=[(us.get("wslots") or [0])[min(j, len(us.get("wslots") or [0]) - 1)]],
             n_gaps=U.n_gaps_draw(rng_for("ngaps", set_tag, sid), us["form"], us.get("k"),
                                  table=("pure" if (card.get("P") or {}).get("pure_table") else bool(card.get("table"))),
                                  sampler=card.get("sampler")))
    return u


def cross_card_twins(by_group, cards_by, set_tag):
    """Repair r1 v3f (G10 twin share 22 +/- 2): C-OUT / C-REC premise twins across cards. units.plan_choice pairs an
    NEI-gold open row with a concrete-gold spec of the same k and display on its own card only; at the sparse k of
    k >= 7 many cards have no such spec left (v3f plan: 42 C-OUT + 9 C-REC NEI-gold rows with no twin). Here a base
    that still lacks twins takes, level by level (twin 1 for every base first, then twin 2, then one more), a
    concrete-gold single of the same sampler, card schema, form, k and display from another card; the twin row is
    built on the base's card (a T1 twin shares its base's card and record), so the card's row count moves by one,
    and every k, display and gold-class count is unchanged. Label-free: reads planned gold classes only, as
    plan_choice does. Wording slots are re-rotated on every card that changed. Returns the number of twins taken."""
    from . import units as U
    rng = rng_for("xcard_twins", set_tag)
    pools = {}
    for (cid, form), us_list in by_group.items():
        if form not in CH_SET_FORMS:
            continue
        cd = cards_by[cid]
        pools.setdefault((cd["sampler"], cd["schema"], form), []).append((cid, form))
    changed = set()
    n = 0
    for pk in sorted(pools):
        gkeys = pools[pk]
        free = {}
        for g in gkeys:
            for u in by_group[g]:
                if u.get("twin") is None and u.get("gold") == "concrete":
                    free.setdefault((u.get("k"), u.get("nei"), u.get("none")), []).append((g, u))
        for lst in free.values():
            rng.shuffle(lst)
        bases = [(g, u) for g in gkeys for u in by_group[g]
                 if u.get("gold") == "nei" and u.get("twin") in (None, "premise") and U.P_PREMISE_CH > 0]
        rng.shuffle(bases)
        drop = set()
        for lev in range(2 + U.MAX_EXTRA_CH):
            for g, u in bases:
                if len(u["consumes"]) != 1 + lev or (lev == 0 and u.get("twin") is not None):
                    continue
                lst = free.get((u.get("k"), u.get("nei"), u.get("none"))) or []
                # another card's single (on its own card plan_choice already had its chance)
                cand = next(((gg, v) for gg, v in reversed(lst) if gg != g and id(v) not in drop), None)
                if cand is None:
                    continue
                lst.remove(cand)
                gg, v = cand
                drop.add(id(v))
                u["consumes"].append(v["sid"])
                if lev == 0:
                    u["twin"] = "premise"
                elif lev == 1:
                    u["twin2"] = True
                else:
                    u.setdefault("twin_x", []).append([None, None])
                changed |= {g, gg}
                n += 1
        for g in gkeys:
            by_group[g] = [u for u in by_group[g] if id(u) not in drop]
    for g in changed:
        cid, form = g
        by_group[g] = _wording_slots(by_group[g], _card(cards_by[cid]), form, set_tag)
    return n


def _degrade(cd, us, tg, what):
    """Shrink a failing C-OUT / C-REC premise set (no spec is dropped: the specs it gives up come back as settled
    singles). 'extras': keep base + 2 twins; 'twin2': keep base + 1 twin; 'split': the base alone (open single)."""
    keep = {"extras": 3, "twin2": 2, "split": 1}[what]
    if len(us["consumes"]) <= keep:
        return us, []
    spilled = [settled_single(cd, us, j, tg) for j in range(keep, len(us["consumes"]))]
    us2 = dict(us, consumes=us["consumes"][:keep], wslots=(us.get("wslots") or [])[:keep])
    us2.pop("twin_x", None)
    if keep < 3:
        us2.pop("twin2", None)
    if keep == 1:
        us2["twin"] = None
    return us2, spilled


def _rounds(set_name, todo_jobs, workers, t, label, spill=None):
    """Build jobs in up to 14 rounds; a failed unit is redrawn with a new round seed (same spec: no relaxation of
    k, display, gold class, n_gaps or signature, so no marginal moves with failures). Repair r1 v3f: with spill (a
    list), a C-OUT / C-REC premise set still failing at a DEGRADE round gives up its last twins, whose specs are
    appended to spill as settled singles (built in pass 2)."""
    res, last_fail = [], []
    jobs = list(todo_jobs)
    todo = jobs
    for rnd in range(10):
        if not todo:
            break
        got = []
        with mp.get_context("fork").Pool(workers, initializer=_init) as pool:
            for i, r in enumerate(pool.imap_unordered(build_one, todo, chunksize=2)):
                got.append(r)
                if (i + 1) % 500 == 0:
                    print(f"{label} round {rnd}: {i + 1}/{len(todo)} {time.time() - t:.0f}s", flush=True)
        res += [r for r in got if r["ok"] or r.get("g3_bug")]
        failed = {r["sid"] for r in got if not r["ok"] and not r.get("g3_bug")}
        last_fail = [r for r in got if not r["ok"] and not r.get("g3_bug")]
        if not failed:
            break
        todo = []
        new_jobs = []
        for cd, us, tg, gs in jobs:
            if us["sid"] in failed:
                us2 = {**us, "round": rnd + 1}
                if spill is not None and us.get("twin") == "premise" and us.get("form") in CH_SET_FORMS and \
                        rnd + 1 in DEGRADE:
                    us2, sp_out = _degrade(cd, us2, tg, DEGRADE[rnd + 1])
                    spill += [(cd, x, tg, gs) for x in sp_out]
                if rnd + 1 >= A22_ROUND:          # PREREG A22: keep every share and bucket; rows <= 7,900 tokens
                    us2["cap"] = TOKEN_CAP_A22
                if us2.get("sig_pool") and (rnd + 1) % 4 == 0:     # keep a hard signature for 3 more rounds first
                    pl = us2["sig_pool"]
                    us2["sig"] = list(pl[C.h64(us2["sid"], rnd + 1) % len(pl)])
                todo.append((cd, us2, tg, gs))
                new_jobs.append((cd, us2, tg, gs))
            else:
                new_jobs.append((cd, us, tg, gs))
        jobs = new_jobs
        progress(f"build {set_name} {label}: round {rnd} done, {len(failed)} units to redraw")
    return res + last_fail, jobs


def run(set_name: str, workers: int, limit: int | None, samplers: tuple):
    C.check_pins()
    git_sha = _git_sha()
    cfg = SETS[set_name]
    if set_name == "dev":
        cards = plan.plan_dev_cards()
        specs = plan.plan_dev_specs(cards)
        samplers = ("S5",)
    else:
        cards = plan.plan_cards()
        specs = plan.plan_specs(cards, cfg["scale"], cfg["tag"])
    cards_by = {c["card_id"]: c for c in cards}
    _init()
    yr = plan.yes_rates(cards, cfg["tag"], {c["card_id"]: card_profile(_card(c)) for c in cards
                                            if c["schema"] == "yn" and c["sampler"] in samplers})
    npair = pair_wordings(cards, yr)
    progress(f"wording sets shared by {npair} complementary-rate card pairs")
    jobs = []
    groups = {}
    for s in specs:
        if s["sampler"] in samplers:
            groups.setdefault((s["card"], s["form"]), []).append(s)
    by_group = {}
    for (cid, form), grp in sorted(groups.items()):
        by_group[(cid, form)] = unit_specs(grp, _card(cards_by[cid]), yr.get(cid), cfg["tag"])
    nx = cross_card_twins(by_group, cards_by, cfg["tag"]) if set_name != "dev" else 0
    progress(f"build {set_name}: {nx} C-OUT / C-REC twins taken across cards")
    for (cid, form), us_list in by_group.items():
        cd = cards_by[cid]
        for us in us_list:
            jobs.append((cd, us, cfg["tag"], git_sha))
    if limit:
        random.Random(0).shuffle(jobs)
        jobs = jobs[:limit]
    # pass 1: units whose base row is open (and C-CASE); pass 2: settled-base units, each taking the gap signature of
    # a pass-1 open row of the same card, group and n_gaps (s6: the visible-gap distribution is the same for settled
    # and open rows; F6-QC-1/2)
    p1 = [j for j in jobs if j[1].get("role") in ("open", "case")]
    p2 = [j for j in jobs if j[1].get("role") not in ("open", "case")]
    progress(f"build {set_name}: {len(jobs)} units planned for samplers {','.join(samplers)} "
             f"(pass 1 open {len(p1)}, pass 2 settled {len(p2)})")
    t = time.time()
    spill = []
    res1, jobs1 = _rounds(set_name, p1, workers, t, "pass1", spill=spill)
    # repair r1 v3f: twins of a realised C-OUT / C-REC set that premise_set could not draw (the set kept the twins
    # found so far, rows [open base, twin 1, ...]) come back as settled singles, so no planned spec is lost
    nrow = {r["sid"]: len(r["rows"]) for r in res1 if r.get("ok")}
    for cd, us, tg, gs in jobs1:
        n = nrow.get(us["sid"])
        if n and us.get("twin") == "premise" and us.get("form") in CH_SET_FORMS and n < len(us["consumes"]):
            spill += [(cd, settled_single(cd, us, j, tg), tg, gs) for j in range(n, len(us["consumes"]))]
    progress(f"build {set_name}: {len(spill)} C-OUT / C-REC twin specs re-planned as settled singles")
    p2 = p2 + spill
    pool_c, pool_s = {}, {}
    for r in res1:
        if not r.get("ok"):
            continue
        for sd in r["sides"]:
            if is_open(sd):
                sg = sig_of(sd)
                if "gap:closure@list" in sg:      # an open-list membership gap exists only on open rows (S3)
                    continue
                cid = sd["spec"]["card"]
                grp = group_of(sd["form"])
                pool_c.setdefault((cid, grp, len(sg)), []).append(sg)
                pool_s.setdefault((cards_by[cid]["sampler"], grp, len(sg), shape_key(_card(cards_by[cid]))),
                                  []).append(sg)
    p2b = []
    nfb = 0
    for cd, us, tg, gs in p2:
        grp = group_of(us["form"])
        n = us.get("n_gaps")
        pl = pool_c.get((cd["card_id"], grp, n)) or pool_s.get((cd["sampler"], grp, n, shape_key(_card(cd))))
        us = dict(us)
        if pl:
            pl = sorted(pl)
            us["sig_pool"] = pl
            us["sig"] = list(pl[C.h64(us["sid"], 0) % len(pl)])
        else:
            nfb += 1
        p2b.append((cd, us, tg, gs))
    progress(f"build {set_name}: pass 1 done ({sum(1 for r in res1 if r.get('ok'))} units ok); signature pools "
             f"{len(pool_c)} card cells; pass 2 units without a pool {nfb}")
    res2, jobs2 = _rounds(set_name, p2b, workers, t, "pass2")
    return res1 + res2, jobs1 + jobs2


def _git_sha() -> str:
    import subprocess
    try:
        return subprocess.run(["git", "-C", str(C.LEAN), "rev-parse", "HEAD"], capture_output=True,
                              text=True).stdout.strip()[:12] or "none"
    except Exception:  # noqa: BLE001
        return "none"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("set", choices=["cand", "qc", "dev"])
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--samplers", default="S1,S2,S3,S4")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    res, jobs = run(a.set, a.workers, a.limit, tuple(a.samplers.split(",")))
    ok = [r for r in res if r["ok"]]
    bad = [r for r in res if not r["ok"]]
    why = Counter((r.get("why") or "")[:60] for r in bad)
    rows = [x for r in ok for x in r["rows"]]
    sides = [x for r in ok for x in r["sides"]]
    rels = [x for r in ok for x in r["rels"]]
    tag = a.out or a.set
    TMP.mkdir(exist_ok=True)
    write_jsonl(TMP / f"build_{tag}_rows.jsonl", rows)
    write_jsonl(TMP / f"build_{tag}_side.jsonl", sides)
    write_jsonl(TMP / f"build_{tag}_rels.jsonl", rels)
    write_jsonl(TMP / f"build_{tag}_fail.jsonl", bad)
    g3b = sum(1 for r in bad if r.get("g3_bug"))
    progress(f"build {tag}: units ok {len(ok)} / {len(res)}, rows {len(rows)}, G3 bugs {g3b}, "
             f"failures {dict(why.most_common(6))}")


if __name__ == "__main__":
    main()
