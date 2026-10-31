"""F13 layout (G0 2.7, section 1 length row): document length bin + target, decisive / near-miss / other deciles,
inert fill from the pack (no filler: every inert sentence is pack domain content), real-token measure of the rendered
`state` (fmt1 render_state in the row's style) and decile depths (token offset of the section's first role fact)."""
from __future__ import annotations

import bisect
import copy

import f13_base as B
import f13_canon as C
import f13_text as T

BINS = ((2000, 3999), (4000, 5999), (6000, 7900))
CAP = 7850
INERT_HEADS = ("Contacts", "Staff", "Weekly routine", "Glossary", "Stock lists", "Routine steps", "Office notes",
               "Records room", "Visitors", "Training log")


def reachable_bins(overhead: int) -> list:
    return [i for i, (lo, _) in enumerate(BINS) if lo + overhead <= CAP]


def draw_target(r, weights, overhead):
    bins = reachable_bins(overhead)
    if not bins:
        return None
    w = [weights[i] for i in bins]
    b = r.choices(bins, weights=w)[0]
    lo, hi = BINS[b]
    return b, r.randint(lo, min(hi, CAP - overhead))


def bin_of(n: int):
    for i, (lo, hi) in enumerate(BINS):
        if lo <= n <= hi:
            return i
    return None


def anchors(sec: dict, card: dict, names: dict) -> list:
    """Strings that locate the first role fact of a section in the rendered state (first match wins)."""
    if sec.get("trace"):
        t = sec["trace"]
        return [f"{t['label']} ({t['scope_label']})"]
    if any(f["ft"] == "table" for f in sec["facts"]):
        h = sec["heading"]
        sl = C.slug(h)
        return [f"{h}:", f"### {h}", f">{h}<", f'"{sl}"', f"\n{sl}:", h]
    for f in sec["facts"]:
        if f["ft"] == "case":
            cid = f.get("cid") or ""
            return [cid, cid.lower().replace("-", "_"), cid.lower()]
        if f["ft"] != "inert":
            return [T.fact_lines(f, card, names)[0]]
    return [sec["facts"][0]["text"]] if sec["facts"] else []


def _ftext(f, card, names):
    if f["ft"] == "table":
        return "\n".join(" ".join(str(x) for x in row) for row in f["rows"])
    return T.fact_lines(f, card, names)[0]


def depths(state: str, doc: dict, names: dict) -> dict:
    """sid -> decile (0-9) of the section's first role fact; None when not found."""
    offs = B.offsets(state)
    n = len(offs)
    out = {}
    for s in doc["sections"]:
        pos = -1
        for a in anchors(s, doc["card"], names):
            if a:
                pos = state.find(a)
                if pos < 0:
                    import json
                    pos = state.find(json.dumps(a)[1:-1])
            if pos >= 0:
                break
        if pos < 0:
            out[s["sid"]] = None
            continue
        ti = bisect.bisect_right(offs, pos) - 1
        out[s["sid"]] = min(9, int(10 * max(ti, 0) / n))
    return out


def inert_sections(ctx, n_sent: int, forbidden=()) -> list:
    pool = T.inert_pool(ctx.pack, ctx.card, ctx.r, n_sent, forbidden)
    secs, i = [], 0
    while i < len(pool):
        k = ctx.r.randint(2, 6)
        facts = [{"ft": "inert", "kind": "inert", "text": t, "traced": False} for t in pool[i:i + k]]
        i += k
        ctx.sec_no += 1
        secs.append({"sid": f"i{ctx.sec_no:02d}", "heading": f"{ctx.r.choice(INERT_HEADS)} ({ctx.sec_no})",
                     "kind": "inert", "scope": None, "role": "inert", "facts": facts, "trace": None})
    return secs


def render_state(doc, style, names) -> str:
    _, _, render = B.fmt1()
    return render.render_state(T.doc_ir(doc, names), style)


FIT_MAX = 600
FIT_TRIES = 8


def _fit_window(d2, order, key, inert, ii, inert_tok, style, names, target, lo, hi, n):
    """repair r10 L4a (G10 length bin 6,000-7,900 short on every sampler): the served-length cap leaves a narrow
    bin-2 window (often < 200 tokens) and appending whole inert sections overshoots it (S2 probe: every failed bin-2
    placement had its deciles right and the state 4-130 tokens above the window), so the job fell back to a lower
    bin. Drop one inert section (preferred) or swap one for a shorter unused one so the state lands inside [lo, hi];
    deciles are re-checked on the new render. Deterministic (no random draws)."""
    mid = (lo + hi) / 2
    keyids = {s["sid"] for s in key}
    tok_of = {id(s): t for s, t in zip(inert, inert_tok)}
    kpos = [i for i, s in enumerate(order) if s["sid"] in keyids]
    last_key = max(kpos) if kpos else -1
    cands = []
    for i, s in enumerate(order):
        t = tok_of.get(id(s))
        if t is None:
            continue
        pen = 0 if i > last_key else 40
        cands.append((abs((n - t) - mid) + pen, i, None))
        for j in range(ii, min(len(inert), ii + 40)):
            if inert_tok[j] < t:
                cands.append((abs((n - t + inert_tok[j]) - mid) + pen + 30, i, j))
    cands.sort(key=lambda x: (x[0], x[1], -1 if x[2] is None else x[2]))
    for _, i, j in cands[:FIT_TRIES]:
        o2 = list(order)
        if j is None:
            del o2[i]
        else:
            o2[i] = inert[j]
        d3 = copy.copy(d2)
        d3["sections"] = o2
        st = render_state(d3, style, names)
        n3 = B.n_tok(st)
        if not (lo <= n3 <= hi and n3 >= 2000):
            continue
        dep = depths(st, d3, names)
        if all(dep.get(s["sid"]) == target[s["sid"]] for s in key if s["role"] in ("decisive", "near_miss")):
            return d3, st, dep, n3
    return None


LAST = {}


def place(doc: dict, ctx, style: dict, names: dict, S_target: int, bin_idx: int, forbidden=(), tries: int = 30,
          hi_cap: int | None = None, dseed=None):
    """Arrange sections so every decisive / near-miss / other section sits at its drawn decile and the rendered
    state is inside the bin (>= 2,000 tokens). Returns (doc, state, depth map) or None."""
    r = ctx.r
    key = [s for s in doc["sections"] if s["role"] in ("decisive", "near_miss", "other")]
    # repair r15 (G10 decisive decile cells S4|2-4K 9th decile 4.8%, S3|6-7.9K, S4|4-6K, S6|4-6K on r9 cand): decisive
    # deciles come from the job's own stream (dseed: same draw over the bin draws, the tries and the build retries) and
    # are never redrawn, so a decile that a long decisive section cannot reach is not swapped for a reachable one;
    # the retry changes the document instead (G0 2.7: deciles drawn first, then the layout is assembled).
    rd = B.rng("f13-dec", dseed) if dseed is not None else r
    dec_fixed = {}
    for s in key:
        if s["role"] == "decisive":
            free = [d for d in range(10) if d not in dec_fixed.values()] or list(range(10))
            dec_fixed[s["sid"]] = rd.choice(free)

    def draw(distinct_all):
        used = set(dec_fixed.values())
        target = {}
        for s in key:
            if s["role"] == "decisive":
                d = dec_fixed[s["sid"]]
            elif distinct_all and s["role"] == "near_miss":
                free = [d for d in range(10) if d not in used] or list(range(10))
                d = r.choice(free)
                used.add(d)
            else:
                d = r.randrange(10)
            target[s["sid"]] = d
        return target
    target = draw(False)
    lo, hi = BINS[bin_idx]
    if hi_cap is not None:  # repair r1: aim inside the window the served-length cap leaves
        hi = min(hi, hi_cap)
        if hi < lo:
            return None
    inert = inert_sections(ctx, max(40, S_target // 14), forbidden)
    scale = 1.0
    for t_ in range(tries):
        if t_ and t_ % 6 == 0:
            target = draw(True)
        per_tok = {s["sid"]: B.n_tok("\n".join(_ftext(f, doc["card"], names) for f in s["facts"]
                                               if f["ft"] != "case") or s["heading"]) + 12 for s in key}
        inert_tok = [B.n_tok("\n".join(f["text"] for f in s["facts"])) + 10 for s in inert]
        per_tok = {k: v * scale for k, v in per_tok.items()}
        inert_tok = [v * scale for v in inert_tok]
        order, cum, ii = [], 0, 0
        for s in sorted(key, key=lambda s: (target[s["sid"]], r.random())):
            want = (target[s["sid"]] + r.uniform(0.2, 0.8)) / 10 * S_target
            while cum < want and ii < len(inert):
                order.append(inert[ii])
                cum += inert_tok[ii]
                ii += 1
            order.append(s)
            cum += per_tok[s["sid"]]
        while cum < S_target and ii < len(inert):
            order.append(inert[ii])
            cum += inert_tok[ii]
            ii += 1
        d2 = copy.copy(doc)
        d2["sections"] = order
        state = render_state(d2, style, names)
        n = B.n_tok(state)
        dep = depths(state, d2, names)
        ok_bin = lo <= n <= hi and n >= 2000
        ok_dec = all(dep.get(s["sid"]) == target[s["sid"]] for s in key if s["role"] in ("decisive", "near_miss"))
        if ok_bin and ok_dec:
            d2["deciles"] = {s["sid"]: target[s["sid"]] for s in key}
            d2["state_tokens"] = n
            return d2, state, dep
        if ok_dec and n > hi and n - hi <= FIT_MAX:
            fit = _fit_window(d2, order, key, inert[:len(inert_tok)], ii, inert_tok, style, names, target, lo, hi, n)
            if fit is not None:
                d3, state3, dep3, n3 = fit
                d3["deciles"] = {s["sid"]: target[s["sid"]] for s in key}
                d3["state_tokens"] = n3
                return d3, state3, dep3
        LAST["why"] = (n, lo, hi, sum(dep.get(s["sid"]) != target[s["sid"]] for s in key
                                      if s["role"] in ("decisive", "near_miss")), len(key))
        # adjust: calibrate the token estimate on the real render; add inert content when the pool ran out
        scale *= n / max(cum, 1)
        if ii >= len(inert) and n < lo:
            inert += inert_sections(ctx, max(10, (S_target - n) // 14 + 5), forbidden)
    return None
