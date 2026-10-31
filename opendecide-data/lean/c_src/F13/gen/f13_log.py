"""S3 audit log / event ledger (G0 4.3; SEM-19, SEM-29 (log line), SEM-35 (log line), SEM-49). Solver A semantics,
activation operators, typed witnesses of 'Log entries' parts, card fields and event-first samplers. Same contract as
f13_samplers / f13_lc: a sampler returns a doc whose solver-A roles equal its plan, or None.

Model facts (sections are segments, kind 'log', each carrying one unit's mark; dates ISO, times 'HH:MM'; 'no' is the
entry number, a label fixed at generation and never renumbered by position, F13R2-15):
  le_ver  {ft, date, time, no, actor, cfg, vid, status: in force|proposed|draft, value}
  le_app  {ft, date, time, no, actor, vid}                 "<vid> applied" (names one proposed version, SEM-29)
  le_rb   {ft, date, time, no, actor, cfg, vid}            "<cfg> rolled back to <vid>" (SEM-49)
  le_void {ft, date, time, no, actor, target}              "VOID entry <no>"
  le_stat {ft, date, time, no, actor, noun, eid, status}   record status entry (status names = card outcomes)
  le_noop {ft, date, time, no, actor, noun, eid, verb: viewed|comment, user}   no state (F13R3-04)
Replay (solver A step 2): entries of the question's unit (and unmarked ones), not voided, timestamp on or before the
end of the question's date, in (date, time, entry number) order.
"""
from __future__ import annotations

import datetime as _dt

import f13_base as B
import f13_model as M
from f13_samplers import Ctx, _why

UNDET = M.UNDET
LG_QK = ("lg_version", "ag2_config", "lg_status", "lg_count", "ag3_lcount")
LE_FT = ("le_ver", "le_app", "le_rb", "le_void", "le_stat", "le_noop")
TZ = ("UTC", "Central European Time", "Eastern Time", "Pacific Time", "Greenwich Mean Time",
      "Australian Eastern Time", "Mountain Time")
S3_HEADS = ("Log segment {n}", "Event ledger part {n}", "Audit trail extract {n}", "System log block {n}",
            "Ledger page {n}", "Event stream extract {n}")


# ================================================================================================ solver A semantics
def _ents(doc, unit):
    for s in doc["sections"]:
        if s.get("scope") is not None and s.get("scope") != unit:
            continue
        for f in s["facts"]:
            if f["ft"] in LE_FT:
                yield f


def _k(f):
    return (f["date"], f["time"], f["no"])


def _voided(ents):
    return {f["target"] for f in ents if f["ft"] == "le_void"}


def cfg_in_force(doc, cfg, unit, on):
    """SEM-35 (log) + SEM-29 + SEM-49 + SEM-27: the version that took effect most recently on or before the end of
    `on`: an in-force version entry at its own time, a proposed version at its applied entry's time, a rollback target
    (marked in force) again at the rollback's time. Voided entries count as never made."""
    ents = list(_ents(doc, unit))
    vd = _voided(ents)
    vers = {f["vid"]: f for f in ents if f["ft"] == "le_ver" and f["cfg"] == cfg and f["no"] not in vd}
    ev = []
    for f in ents:
        if f["no"] in vd or f["date"] > on:
            continue
        ft = f["ft"]
        if ft == "le_ver" and f["cfg"] == cfg and f["status"] == "in force":
            ev.append((_k(f), f))
        elif ft == "le_app" and f["vid"] in vers and vers[f["vid"]]["status"] == "proposed" and \
                _k(vers[f["vid"]]) < _k(f):
            ev.append((_k(f), vers[f["vid"]]))
        elif ft == "le_rb" and f["cfg"] == cfg and f["vid"] in vers and vers[f["vid"]]["status"] == "in force" and \
                _k(vers[f["vid"]]) < _k(f):
            ev.append((_k(f), vers[f["vid"]]))
    if not ev:
        return None
    return max(ev, key=lambda x: x[0])[1]


def status_of(doc, noun, eid, unit, on):
    ents = list(_ents(doc, unit))
    vd = _voided(ents)
    st = [f for f in ents if f["ft"] == "le_stat" and f["noun"] == noun and f["eid"] == eid and f["no"] not in vd
          and f["date"] <= on]
    return max(st, key=_k)["status"] if st else UNDET


def count_entries(doc, noun, status, unit, on):
    ents = list(_ents(doc, unit))
    vd = _voided(ents)
    return sum(1 for f in ents if f["ft"] == "le_stat" and f["noun"] == noun and f["status"] == status and
               f["no"] not in vd and f["date"] <= on)


def log_core(doc):
    q = doc["query"]
    on = str(q["date"])
    qk = q["qk"]
    if qk in ("lg_version", "ag2_config"):
        v = cfg_in_force(doc, q["cfg"], q["unit"], on)
        if v is None:
            return UNDET
        return v["vid"] if qk == "lg_version" else v["value"]
    if qk == "lg_status":
        return status_of(doc, q["noun"], q["eid"], q["unit"], on)
    if qk in ("lg_count", "ag3_lcount"):
        return count_entries(doc, q["noun"], q["filt"], q["unit"], on)
    raise ValueError(qk)


def log_activate(d2, sec, nm):
    """One operator per near-miss kind (2.3, F13R2-20): V late (the entry's own date set to the question's date),
    V status (a draft / proposed version marked in force), V void (the VOID entry naming it removed), V rb (the
    rollback that undoes it removed); R (the question's unit set to the segment's); I (the question's record ID set
    to the look-alike)."""
    q = d2["query"]
    if nm["kind"] == "V":
        sub = nm["sub"]
        if sub == "void":
            for s in d2["sections"]:
                s["facts"] = [x for x in s["facts"] if not (x["ft"] == "le_void" and x["target"] == nm["no"])]
            return
        if sub == "rb":
            for s in d2["sections"]:
                s["facts"] = [x for x in s["facts"] if not (x["ft"] == "le_rb" and x["no"] == nm["rb_no"])]
            return
        f = next(x for x in sec["facts"] if x.get("no") == nm["no"])
        if sub == "late":
            f["date"] = str(q["date"])
        else:
            f["status"] = "in force"
    elif nm["kind"] == "R":
        q["unit"] = nm["unit"]
    elif nm["kind"] == "I":
        q["eid"] = nm["id"]


def witness_facts(q, card):
    """Typed completions of a 'Log entries' part (G0 2.4): entries of the queried kind dated on the question's date
    (shared definition with solver B's label-typed witnesses)."""
    on = str(q["date"])
    qk = q["qk"]
    out = []
    if qk in ("lg_version", "ag2_config"):
        for i, v in enumerate((0, 10 ** 6)):
            out.append([{"ft": "le_ver", "date": on, "time": "00:00", "no": i, "actor": "W", "cfg": q["cfg"],
                         "vid": f"W-0.{i + 1}", "status": "in force", "value": v}])
    elif qk == "lg_status":
        for i, o in enumerate(card["outcomes"]):
            out.append([{"ft": "le_stat", "date": on, "time": "00:00", "no": i, "actor": "W", "noun": q["noun"],
                         "eid": q["eid"], "status": o}])
    else:
        out.append([{"ft": "le_stat", "date": on, "time": "00:00", "no": 0, "actor": "W", "noun": q["noun"],
                     "eid": "W-0000", "status": q["filt"]}])
    return out


def log_witness(doc, sec):
    t = sec["trace"]
    k = doc["card"]["scope_kind"]
    unit = t["scope_label"][len(k) + 1:] if t["scope_label"].startswith(k + " ") else None
    if t["label"] != "Log entries":
        return []
    return [{"scope": unit, "facts": fs} for fs in witness_facts(doc["query"], doc["card"])]


# ================================================================================================ card
def log_card(card, pack):
    r = B.rng("f13-logcard", card["card_id"])
    card["log"] = True
    card["has_case"] = False
    card["tz"] = r.choice(TZ)
    card["ent_prefix"] = pack["ents"][0]["prefix"]
    card["cfgs"] = [{"name": f"{a['name']} setting", "attr": a["name"], "unit": a["unit"], "lo": a["lo"],
                     "hi": a["hi"]} for a in card["attrs"][:3]]
    card["actors"] = list(pack["people"] or [])[:8] or ["system"]
    card["fact_kinds"] = ["log entry", "version", "applied entry", "rollback", "VOID entry", "status entry"]
    card["scoped_kinds"] = ["log entry", "version"]
    return card


# ================================================================================================ helpers
class LogCtx:
    """Per-row timestamp, entry and segment factory. Timestamps are unique per document; entry numbers are given in
    timestamp order at the end (number())."""

    def __init__(self, c):
        self.c, self.r = c, c.r
        self.taken = set()
        self.all = []
        self.vids = set()

    def ts(self, d):
        d = d if isinstance(d, str) else d.isoformat()
        for _ in range(200):
            t = f"{self.r.randint(6, 21):02d}:{self.r.randint(0, 59):02d}"
            if (d, t) not in self.taken:
                self.taken.add((d, t))
                return d, t
        raise RuntimeError("ts")

    def day(self, lo, hi):
        return B.add_days(self.c.base, self.r.randint(lo, hi)).isoformat()

    def days(self, lo, hi, n):
        """n distinct sorted days in [base+lo, base+hi]."""
        if hi - lo + 1 < n:
            return None
        xs = sorted(self.r.sample(range(lo, hi + 1), n))
        return [B.add_days(self.c.base, x).isoformat() for x in xs]

    def e(self, ft, d, **kw):
        date, time = self.ts(d)
        f = {"ft": ft, "date": date, "time": time, "no": None, "actor": self.r.choice(self.c.card["actors"]), **kw}
        self.all.append(f)
        return f

    def seg(self, role, facts, unit, **kw):
        c = self.c
        c.sec_no += 1
        s = {"sid": f"s{c.sec_no:02d}", "heading": self.r.choice(S3_HEADS).format(n=c.sec_no + 1), "kind": "log",
             "scope": unit, "role": role, "facts": sorted(facts, key=lambda f: (f["date"], f["time"])),
             "trace": None}
        s.update(kw)
        return s

    def number(self, sections):
        """Entry numbers in timestamp order (labels), then resolve VOID targets and near-miss entry refs."""
        n = self.r.randint(10000, 70000)
        for f in sorted(self.all, key=lambda f: (f["date"], f["time"])):
            n += self.r.randint(1, 9)
            f["no"] = n
        for f in self.all:
            if f["ft"] == "le_void":
                f["target"] = f.pop("_t")["no"]
        for s in sections:
            nm = s.get("nm")
            if nm:
                for k in ("_f", "_rb"):
                    if k in nm:
                        nm["no" if k == "_f" else "rb_no"] = nm.pop(k)["no"]


def _vals(c, cfg, n, avoid=()):
    lo, hi = cfg["lo"], cfg["hi"]
    pool = list(range(max(lo, 1), hi + 1))
    if len(pool) < n + len(avoid) + 2:
        return None
    out = []
    while len(out) < n:
        v = c.r.choice(pool)
        if v not in out and v not in avoid:
            out.append(v)
    return out


def _header(L, card):
    c = L.c
    c.sec_no += 1
    lines = [f"System: {card['org']} {card['doc_noun']}.", f"Times are given in {card['tz']}.",
             "Each entry gives its time, entry number, actor and text, separated by vertical bars."]
    return {"sid": f"s{c.sec_no:02d}", "heading": "Log header", "kind": "inert", "scope": None, "role": "inert",
            "facts": [{"ft": "inert", "kind": "inert", "text": t, "traced": False} for t in lines], "trace": None}


def _noise(L, card, unit, avoid_cfg=None, avoid_eid=None, avoid_status=None, taken_ids=None, n=(1, 4), lo=0,
           hi=560):
    """Role-less entries on other records / other configurations / no-ops (never on the queried item's state)."""
    r = L.r
    out = []
    for _ in range(r.randint(*n)):
        x = r.random()
        if x < 0.45:
            sts = [o for o in card["outcomes"] if o != avoid_status]
            eid = B.new_id(card["ent_prefix"], 4, r, taken_ids, digits_only=True)
            out.append(L.e("le_stat", L.day(lo, hi), noun=card["item"], eid=eid, status=r.choice(sts)))
        elif x < 0.7 and len(card["cfgs"]) > 1:
            cf = r.choice([g for g in card["cfgs"] if g["name"] != avoid_cfg])
            v = _vals(L.c, cf, 1)
            nv = f"CF-{r.randint(90, 99)}.{r.randint(1, 9)}"
            if v and nv not in L.vids:
                L.vids.add(nv)
                out.append(L.e("le_ver", L.day(lo, hi), cfg=cf["name"], vid=nv, status="in force", value=v[0]))
        else:
            eid = avoid_eid if (avoid_eid and r.random() < 0.5) else B.new_id(card["ent_prefix"], 4, r, taken_ids,
                                                                               digits_only=True)
            out.append(L.e("le_noop", L.day(lo, hi), noun=card["item"], eid=eid,
                           verb=r.choice(["viewed", "comment"]), user=r.choice(card["actors"])))
    return out


DEC_T = (2, 2, 3, 3, 4)  # repair r9-2: total mentions per shown version ID (state entries + no-op decoys)
P_OOO = 1.0  # repair r9-2 (smoke r9e: .5 left gold first 24/165 vs 36.5): share of segments of these rows listed out of time order (SEM-19)


def _decoys(L, card, cfg, vids, segs):
    """repair r9-2 (G0 4.3 mention decoys, F13R3-04): no-op entries per shown version ID so that its entry mentions
    reach a common drawn total (a rollback that names the gold no longer makes it the most-mentioned option); each in
    a uniformly drawn segment (any role), dated after the version's own entry."""
    r = L.r
    own = {f["vid"]: f["date"] for f in L.all if f["ft"] == "le_ver" and f["cfg"] == cfg}
    base = {}
    for f in L.all:
        if f["ft"] in ("le_ver", "le_app", "le_rb") and f.get("vid") in vids:
            base[f["vid"]] = base.get(f["vid"], 0) + 1
    for v in vids:
        if v not in own:
            continue
        d0 = (_dt.date.fromisoformat(own[v]) - L.c.base).days
        for _ in range(max(0, r.choice(DEC_T) - base.get(v, 0))):
            sg = r.choice(segs)
            f = L.e("le_noop", L.day(d0 + 1, max(d0 + 2, 600)), noun="version", eid=v, cfg=cfg,
                    verb=r.choice(["viewed", "comment"]), user=r.choice(card["actors"]))
            sg["facts"] = sorted(sg["facts"] + [f], key=lambda f_: (f_["date"], f_["time"]))
    # SEM-19 / MR14: entries may be listed out of time order (timestamps decide); a segment lists its entries in
    # time order only with probability 1 - P_OOO, so the shown earlier versions do not always precede the gold
    for sg in segs:
        if r.random() < P_OOO:
            r.shuffle(sg["facts"])


def _finish(doc, dec, plan, L):
    L.number(doc["sections"])
    A = M.answers(doc)
    if M.CONFLICT in A or UNDET in A or len(A) != 1:
        return _why("lg undet")
    v = next(iter(A))
    if plan.get("value") is not None and v != plan["value"]:
        return _why("lg target")
    if M.option_answer(doc)[0] == "bad":
        return _why("lg bad")
    from f13_samplers import role_doc
    rd = role_doc(doc)
    D = M.decisive_set(rd)
    if sorted(D) != sorted(dec):
        return _why("lg D")
    if not M.sufficient(rd, D):
        return _why("lg suff")
    for s in rd["sections"]:
        if s["role"] == "near_miss":
            if not M.nm_functional(rd, s["sid"]):
                return _why("lg nm " + s["nm"]["kind"] + s["nm"].get("sub", ""))
            if M.option_answer(M.activate(rd, s["sid"]))[0] == "abstain" and rd["query"].get("abstain") != "NONE":
                return _why("lg nm abstain")  # r7: closed choice rows may activate to None (unshown new answer)
    doc["decisive"] = D
    return doc


def _q(plan, card, **kw):
    q = {"skill": "QR", "form": plan["form"], "neg": plan.get("neg", 0), "inner_neg": plan.get("inner_neg", False),
         "abstain": "NEI" if card["world"] == "open" else "NONE"}
    q.update(kw)
    return q


def _shown(plan, r, g, nm_ans, extra):
    """Choice rows: k - 1 shown values (k incl. the abstain option): gold (unless closed gold-abstain), every near-miss
    answer, then distractors from `extra`."""
    k = plan["k"]
    need = ([] if plan.get("abstain_gold") and plan.get("closed") else [g]) + [a for a in nm_ans if a != g]
    need = list(dict.fromkeys(need))
    if len(need) > k - 1:
        return None
    pool = [x for x in dict.fromkeys(extra) if x not in need and x != g]
    r.shuffle(pool)
    sh = need + pool[: k - 1 - len(need)]
    if len(sh) < k - 1:
        return None
    r.shuffle(sh)
    return sh


def _claim(plan, g, nm_ans, r):
    """yn / establish / settle claims. True claims: any near-miss flips them. False claims: the claim is the one
    near-miss answer, so activation makes it true (2.3)."""
    t = plan["truth"]
    if plan["form"] == "establish":
        t = True  # contradicted establish rows have no decisive section; abstain establish rows come from T-D
    if plan.get("inner_neg"):
        return (nm_ans[0] if len(nm_ans) == 1 else None) if t else g
    return g if t else (nm_ans[0] if len(nm_ans) == 1 else None)


def _cfg_ids(r):
    cno = r.randint(11, 89)
    state = {"rev": 0}

    def vid():
        state["rev"] += r.randint(1, 2)
        return f"CF-{cno}.{state['rev']}"
    return vid


# ================================================================================================ samplers
def lg_cfg(card, pack, plan, seed):
    """plan kind qrv (Q-R version ID, 1 decisive segment) | ag2c (AG-2 configuration value; k_cons K1 proposed +
    applied | K2 void | K3 rollback | K12 = K1 + K2). nm_kinds subset of late, prop, draft, void, rb, R."""
    c = Ctx(card, pack, seed)
    r = c.r
    L = LogCtx(c)
    unit = r.choice(card["units"])
    cfg = r.choice(card["cfgs"])
    X = cfg["name"]
    vid = _cfg_ids(r)
    Dq = B.add_days(c.base, r.randint(600, 800)).isoformat()
    ag2 = plan["kind"] == "ag2c"
    kc = plan.get("k_cons")
    nmk = list(plan["nm_kinds"])
    if ag2:
        nmk = [k for k in nmk if k in ("late", "prop", "draft", "R")]
        if kc in ("K2", "K3", "K12"):
            nmk = [k for k in nmk if k in ("late", "R")]
    n_prev = r.choice([1, 1, 2, 3])
    if plan["form"] == "choice":
        n_prev = max(n_prev, plan["k"] - 2)
    # day plan: prev .. E* in [0, 300]; then up to 7 ordered event days in (E*, Dq)
    ds = L.days(0, 300, n_prev + 1)
    mid = L.days(320, 580, 8)
    if ds is None or mid is None:
        return None
    vals = _vals(c, cfg, n_prev + 8)
    if vals is None:
        return _why("lg vals")
    vi = iter(vals)
    taken_ids = set()
    dec_secs, nm_secs, other = [], [], []
    A_f = []
    prev = [L.e("le_ver", ds[i], cfg=X, vid=vid(), status="in force", value=next(vi)) for i in range(n_prev)]
    A_f += prev
    ans = (lambda f: f["vid"]) if not ag2 else (lambda f: f["value"])
    mi = iter(mid)
    if kc in ("K1", "K12"):
        star = L.e("le_ver", ds[n_prev], cfg=X, vid=vid(), status="proposed", value=next(vi))
        A_f.append(star)
        app = L.e("le_app", next(mi), vid=star["vid"])
        B_f = [app]
    else:
        star = L.e("le_ver", ds[n_prev], cfg=X, vid=vid(), status="in force", value=next(vi))
        A_f.append(star)
        B_f = None
    g = ans(star)
    nm_ans = []
    segs = []
    secA = L.seg("decisive", A_f + _noise(L, card, unit, avoid_cfg=X, taken_ids=taken_ids, n=(0, 3)), unit)
    segs.append(secA)
    dec_ids = [secA["sid"]]
    if B_f is not None:
        secB = L.seg("decisive", B_f + _noise(L, card, unit, avoid_cfg=X, taken_ids=taken_ids, n=(1, 3)), unit)
        segs.append(secB)
        dec_ids.append(secB["sid"])
    if kc in ("K2", "K12"):
        vp = L.e("le_ver", next(mi), cfg=X, vid=vid(), status="in force", value=next(vi))
        vo = L.e("le_void", next(mi), _t=vp)
        sC = L.seg("near_miss", [vp] + _noise(L, card, unit, avoid_cfg=X, taken_ids=taken_ids, n=(0, 2)), unit,
                   nm={"kind": "V", "sub": "void", "log": True, "_f": vp})
        sD = L.seg("decisive", [vo] + _noise(L, card, unit, avoid_cfg=X, taken_ids=taken_ids, n=(1, 3)), unit)
        segs += [sC, sD]
        dec_ids.append(sD["sid"])
        nm_ans.append(ans(vp))
    if kc == "K3":
        vp = L.e("le_ver", next(mi), cfg=X, vid=vid(), status="in force", value=next(vi))
        rb = L.e("le_rb", next(mi), cfg=X, vid=star["vid"])
        sC = L.seg("near_miss", [vp] + _noise(L, card, unit, avoid_cfg=X, taken_ids=taken_ids, n=(0, 2)), unit,
                   nm={"kind": "V", "sub": "rb", "log": True, "_rb": rb})
        sD = L.seg("decisive", [rb] + _noise(L, card, unit, avoid_cfg=X, taken_ids=taken_ids, n=(1, 3)), unit)
        segs += [sC, sD]
        dec_ids.append(sD["sid"])
        nm_ans.append(ans(vp))
    # optional near-misses (Q-R and extra AG-2 ones); rollback pair first so later activations stay latest
    order = [k for k in ("rb", "void", "prop", "draft") if k in nmk]
    for k in order:
        if k == "rb":
            vp = L.e("le_ver", next(mi), cfg=X, vid=vid(), status="in force", value=next(vi))
            rb = L.e("le_rb", next(mi), cfg=X, vid=star["vid"])
            segs.append(L.seg("near_miss", [vp, rb] + _noise(L, card, unit, avoid_cfg=X, taken_ids=taken_ids,
                                                             n=(0, 2)), unit,
                              nm={"kind": "V", "sub": "rb", "log": True, "_rb": rb}))
        elif k == "void":
            vp = L.e("le_ver", next(mi), cfg=X, vid=vid(), status="in force", value=next(vi))
            vo = L.e("le_void", next(mi), _t=vp)
            segs.append(L.seg("near_miss", [vp, vo] + _noise(L, card, unit, avoid_cfg=X, taken_ids=taken_ids,
                                                             n=(0, 2)), unit,
                              nm={"kind": "V", "sub": "void", "log": True, "_f": vp}))
        else:
            vp = L.e("le_ver", next(mi), cfg=X, vid=vid(), status="proposed" if k == "prop" else "draft",
                     value=next(vi))
            segs.append(L.seg("near_miss", [vp] + _noise(L, card, unit, avoid_cfg=X, taken_ids=taken_ids, n=(0, 2)),
                              unit, nm={"kind": "V", "sub": "status", "log": True, "_f": vp}))
        nm_ans.append(ans(vp))
    if "late" in nmk:
        dl = B.add_days(_dt.date.fromisoformat(Dq), r.randint(3, 150)).isoformat()
        vp = L.e("le_ver", dl, cfg=X, vid=vid(), status="in force", value=next(vi))
        segs.append(L.seg("near_miss", [vp] + _noise(L, card, unit, avoid_cfg=X, taken_ids=taken_ids, n=(0, 2)),
                          unit, nm={"kind": "V", "sub": "late", "log": True, "_f": vp}))
        nm_ans.append(ans(vp))
    if "R" in nmk:
        u2 = r.choice([u for u in card["units"] if u != unit])
        vid2 = _cfg_ids(r)
        n2 = r.choice([1, 2])
        d2s = L.days(0, 580, n2)
        v2 = _vals(c, cfg, n2, avoid=[x for x in vals])
        if v2 is None:
            return _why("lg vals2")
        fs = [L.e("le_ver", d2s[i], cfg=X, vid=vid2(), status="in force", value=v2[i]) for i in range(n2)]
        if any(f["vid"] in {x["vid"] for x in L.all if x["ft"] == "le_ver" and x not in fs} for f in fs):
            return _why("lg vid clash")
        segs.append(L.seg("near_miss", fs + _noise(L, card, u2, avoid_cfg=X, taken_ids=taken_ids, n=(0, 2)), u2,
                          nm={"kind": "R", "log": True, "unit": u2}))
        nm_ans.append(ans(fs[-1]))
    if not any(s["role"] == "near_miss" for s in segs):
        return _why("lg no nm")
    if len(set(nm_ans)) != len(nm_ans) or g in nm_ans:
        return _why("lg nm dup")
    # role-less segments: other units / other configurations / records / no-ops
    for _ in range(r.randint(1, 3)):
        u = r.choice(card["units"])
        fs = _noise(L, card, u, avoid_cfg=X, taken_ids=taken_ids, n=(2, 5), hi=580)
        if fs:
            segs.append(L.seg("other", fs, u))
    r.shuffle(segs)
    sections = [_header(L, card)] + segs
    extra = [ans(f) for f in prev] + [ans(f) for f in L.all if f["ft"] == "le_ver" and f["cfg"] == X]
    # repair r8 (G0 3.3 A44 / F-DOC): no unstated filler values; every config-value option is a stated document value
    plan = dict(plan, closed=card["world"] == "closed")
    q = _q(plan, card, qk="ag2_config" if ag2 else "lg_version", cfg=X, unit=unit, date=Dq)
    if ag2:
        q["vunit"] = cfg["unit"]
    if plan["form"] == "choice":
        sh = _shown(plan, r, g, nm_ans, extra)
        if sh is None:
            return _why("lg shown")
        q["shown"] = sh
    else:
        cv = _claim(plan, g, nm_ans, r)
        if cv is None:
            return _why("lg claim")
        q["claim"] = {"value": cv}
        q["shown"] = [g] + nm_ans
    plan["value"] = g
    if not ag2:
        _decoys(L, card, X, q["shown"] if plan["form"] == "choice" else [g] + nm_ans, segs)
    doc = {"card": card, "sections": sections, "query": q, "case": None,
           "title": f"{card['org']} {card['doc_noun']}"}
    return _finish(doc, dec_ids, plan, L)


def lg_status(card, pack, plan, seed):
    """Record status as of D (Q-R): one decisive segment holds the record's status entries; near-misses late
    (entry after D), void (voided entry), I (look-alike record ID)."""
    c = Ctx(card, pack, seed)
    r = c.r
    L = LogCtx(c)
    unit = r.choice(card["units"])
    noun = card["item"]
    taken_ids = set()
    eid = B.new_id(card["ent_prefix"], 4, r, taken_ids, digits_only=True)
    Dq = B.add_days(c.base, r.randint(600, 800)).isoformat()
    outs = card["outcomes"]
    n_prev = r.choice([0, 1, 1, 2])
    ds = L.days(0, 300, n_prev + 1)
    mid = L.days(320, 580, 4)
    seq = []
    for i in range(n_prev + 1):
        seq.append(r.choice([o for o in outs if o != (seq[-1] if seq else None)]))
    g = seq[-1]
    A_f = [L.e("le_stat", ds[i], noun=noun, eid=eid, status=seq[i]) for i in range(n_prev + 1)]
    segs = [L.seg("decisive", A_f + _noise(L, card, unit, avoid_eid=eid, taken_ids=taken_ids, n=(0, 3)), unit)]
    dec_ids = [segs[0]["sid"]]
    nm_ans = []
    others = [o for o in outs if o != g]
    r.shuffle(others)
    oi = iter(others * 2)
    mi = iter(mid)
    vs = plan.get("vsplit", 0)  # r11 L6: split void (VOID entry alone in a second decisive segment, G0 4.3)
    for k in plan["nm_kinds"]:
        if k == "void":
            fp = L.e("le_stat", next(mi), noun=noun, eid=eid, status=next(oi))
            vo = L.e("le_void", next(mi), _t=fp)
            if vs > 0:
                vs -= 1
                sD = L.seg("decisive", [vo] + _noise(L, card, unit, avoid_eid=eid, taken_ids=taken_ids, n=(1, 3)),
                           unit)
                segs.append(sD)
                dec_ids.append(sD["sid"])
                segs.append(L.seg("near_miss", [fp] + _noise(L, card, unit, avoid_eid=eid, taken_ids=taken_ids,
                                                             n=(0, 2)), unit,
                                  nm={"kind": "V", "sub": "void", "log": True, "_f": fp}))
            else:
                segs.append(L.seg("near_miss", [fp, vo] + _noise(L, card, unit, avoid_eid=eid, taken_ids=taken_ids,
                                                                 n=(0, 2)), unit,
                                  nm={"kind": "V", "sub": "void", "log": True, "_f": fp}))
            nm_ans.append(fp["status"])
        elif k == "late":
            dl = B.add_days(_dt.date.fromisoformat(Dq), r.randint(3, 150)).isoformat()
            fp = L.e("le_stat", dl, noun=noun, eid=eid, status=next(oi))
            segs.append(L.seg("near_miss", [fp] + _noise(L, card, unit, avoid_eid=eid, taken_ids=taken_ids, n=(0, 2)),
                              unit, nm={"kind": "V", "sub": "late", "log": True, "_f": fp}))
            nm_ans.append(fp["status"])
        elif k == "I":
            e2 = B.lookalike(eid, r, taken_ids)
            if e2 is None:
                return None
            taken_ids.add(e2)
            s2 = next(oi)
            fs = [L.e("le_stat", L.day(0, 580), noun=noun, eid=e2, status=s2)]
            segs.append(L.seg("near_miss", fs + _noise(L, card, unit, avoid_eid=eid, taken_ids=taken_ids, n=(0, 2)),
                              unit, nm={"kind": "I", "log": True, "id": e2}))
            nm_ans.append(s2)
    if not nm_ans:
        return _why("lg no nm")
    if len(set(nm_ans)) != len(nm_ans):
        return _why("lg nm dup")
    for _ in range(r.randint(1, 3)):
        u = r.choice(card["units"])
        fs = _noise(L, card, u, avoid_eid=eid, taken_ids=taken_ids, n=(2, 5), hi=580)
        if fs:
            segs.append(L.seg("other", fs, u))
    r.shuffle(segs)
    sections = [_header(L, card)] + segs
    plan = dict(plan, closed=card["world"] == "closed")
    q = _q(plan, card, qk="lg_status", noun=noun, eid=eid, unit=unit, date=Dq)
    if plan["form"] == "choice":
        sh = _shown(plan, r, g, nm_ans, list(outs))
        if sh is None:
            return _why("lg shown")
        q["shown"] = sh
    else:
        cv = _claim(plan, g, nm_ans, r)
        if cv is None:
            return _why("lg claim")
        q["claim"] = {"value": cv}
        q["shown"] = list(outs)
    plan["value"] = g
    doc = {"card": card, "sections": sections, "query": q, "case": None,
           "title": f"{card['org']} {card['doc_noun']}"}
    return _finish(doc, dec_ids, plan, L)


def lg_count(card, pack, plan, seed):
    """Q-T count (kind qtc, 1 decisive segment) and AG-3 cross-segment count (kind ag3c, 2-3 decisive segments, the
    segments acting as the table's parts): entries for the unit that set a record's status to S, as of D.
    plan: value (gold count 1-8), shown, n_dec, nm_kinds subset of late, void, R."""
    c = Ctx(card, pack, seed)
    r = c.r
    L = LogCtx(c)
    unit = r.choice(card["units"])
    noun = card["item"]
    S = r.choice(card["outcomes"])
    others = [o for o in card["outcomes"] if o != S]
    taken_ids = set()
    Dq = B.add_days(c.base, r.randint(600, 800)).isoformat()
    g = plan["value"]
    nd = plan["n_dec"]
    if g < nd:
        return _why("lg count < parts")
    cuts = sorted(r.sample(range(1, g), nd - 1)) if nd > 1 else []
    sizes = [b - a for a, b in zip([0] + cuts, cuts + [g])]
    segs, dec_ids = [], []
    for k in sizes:
        fs = [L.e("le_stat", L.day(0, 580), noun=noun, eid=B.new_id(card["ent_prefix"], 4, r, taken_ids, True),
                  status=S) for _ in range(k)]
        fs += [L.e("le_stat", L.day(0, 580), noun=noun, eid=B.new_id(card["ent_prefix"], 4, r, taken_ids, True),
                   status=r.choice(others)) for _ in range(r.randint(0, 3))]
        s = L.seg("decisive", fs + _noise(L, card, unit, avoid_status=S, taken_ids=taken_ids, n=(0, 2)), unit)
        segs.append(s)
        dec_ids.append(s["sid"])
    shown = plan["shown"]
    for k in plan["nm_kinds"]:
        if k == "late":
            dl = B.add_days(_dt.date.fromisoformat(Dq), r.randint(3, 150)).isoformat()
            fp = L.e("le_stat", dl, noun=noun, eid=B.new_id(card["ent_prefix"], 4, r, taken_ids, True), status=S)
            segs.append(L.seg("near_miss", [fp] + _noise(L, card, unit, avoid_status=S, taken_ids=taken_ids,
                                                         n=(0, 2)), unit,
                              nm={"kind": "V", "sub": "late", "log": True, "_f": fp}))
        elif k == "void":
            fp = L.e("le_stat", L.day(0, 560), noun=noun, eid=B.new_id(card["ent_prefix"], 4, r, taken_ids, True),
                     status=S)
            vo = L.e("le_void", L.day(570, 590), _t=fp)
            if (vo["date"], vo["time"]) <= (fp["date"], fp["time"]):
                return _why("lg void order")
            if plan.get("vsplit"):  # r11 L6: VOID entry in a second decisive segment (qtc only; never on ag3c)
                sD = L.seg("decisive", [vo] + _noise(L, card, unit, avoid_status=S, taken_ids=taken_ids, n=(1, 3)),
                           unit)
                segs.append(sD)
                dec_ids.append(sD["sid"])
                segs.append(L.seg("near_miss", [fp] + _noise(L, card, unit, avoid_status=S, taken_ids=taken_ids,
                                                             n=(0, 2)), unit,
                                  nm={"kind": "V", "sub": "void", "log": True, "_f": fp}))
            else:
                segs.append(L.seg("near_miss", [fp, vo] + _noise(L, card, unit, avoid_status=S, taken_ids=taken_ids,
                                                                 n=(0, 2)), unit,
                                  nm={"kind": "V", "sub": "void", "log": True, "_f": fp}))
        elif k == "R":
            u2 = r.choice([u for u in card["units"] if u != unit])
            pool = [x for x in shown if x != g and x >= 1 and x != g + 1]
            if not pool:
                return _why("lg R pool")
            c2 = r.choice(pool)
            fs = [L.e("le_stat", L.day(0, 580), noun=noun, eid=B.new_id(card["ent_prefix"], 4, r, taken_ids, True),
                      status=S) for _ in range(c2)]
            segs.append(L.seg("near_miss", fs + _noise(L, card, u2, avoid_status=S, taken_ids=taken_ids, n=(0, 2)),
                              u2, nm={"kind": "R", "log": True, "unit": u2}))
    if not any(s["role"] == "near_miss" for s in segs):
        return _why("lg no nm")
    for _ in range(r.randint(1, 3)):
        u = r.choice(card["units"])
        fs = _noise(L, card, u, avoid_status=S, taken_ids=taken_ids, n=(2, 5), hi=580)
        if fs:
            segs.append(L.seg("other", fs, u))
    r.shuffle(segs)
    sections = [_header(L, card)] + segs
    q = _q(plan, card, qk="ag3_lcount" if plan["kind"] == "ag3c" else "lg_count", noun=noun, filt=S, unit=unit,
           date=Dq, shown=list(shown))
    q["skill"] = "QT"
    doc = {"card": card, "sections": sections, "query": q, "case": None,
           "title": f"{card['org']} {card['doc_noun']}"}
    return _finish(doc, dec_ids, plan, L)


def log_part_label(doc, s):
    """('Log entries', '<scope kind> <unit>') for a decisive segment replaced by a T-D part trace."""
    if s.get("kind") != "log" or not s.get("scope"):
        return None
    return ("Log entries", f"{doc['card']['scope_kind']} {s['scope']}")
