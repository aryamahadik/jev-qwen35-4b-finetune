"""T63 EXISTS head: EX-A1 (registry listing), EX-A2 (library version export list), EX-B (pinned-toolchain stdlib export; views B1 visible list,
B2 knowledge) with SOLVER A (membership in the spec's own source) and the stdlib export loader.

Gold (G0-lite section 2.2, Opus T63-B8):
  EX-A1: P in the ASKED registry's listing; the listing is COMPLETE for the alphabetical range [lo, hi] and P lies inside it, so absence is provable.
  EX-A2: module.symbol in the complete export list of library L at version V shown in the row.
  EX-B : name in the hashed export file for (language, module): public names without a leading underscore after a `python -I` import on the pinned
         Linux image / Node built-in exports / Go exported identifiers, 3 identical export runs; a re-exported name counts as present; EX-N1
         negatives are checked against the FULL export of the queried module.
The export file is a PROGRAM output of the L-0 image build (`runner.stdlib_export.*`, names only, sha-bound). A fixture export (tests, dry run) is
flagged `fixture: true` and refused by `ExportSet.require_real()`.

Matched pairs (K7, EXISTS >= 30%): a pair is a YES row and a NO row on the SAME listing / library / module that differ in one edit or one field:
N4 (a one-edit near-miss of the asked name), N2 (A1: the same name asked of the other registry), N1 (A2 / B: the same name asked of another module).
"""
import copy
import json
import re

from LP_COMMON import util

from . import config as C

GENERIC = frozenset(("core", "kit", "lib", "sdk", "utils"))
TOKEN = re.compile(r"[A-Z]+(?![a-z])|[A-Z]?[a-z0-9]+")
VOW, CON = "aeiou", "bdfgklmnprstvz"
SYL = re.compile(r"[bdfgklmnprstvz][aeiou][lnrst]?")


class Reject(Exception):
    pass


def tokens_of(name):
    """Tokens of a name for M-PLAUS: separator parts, camel humps or syllables of a bare stem; the generic suffix words are not tokens."""
    toks, _ = split_name(name.replace("/", "-"))
    return [t.lower() for t in toks if t.lower() not in GENERIC]


class ExportSet(object):
    """{lang: {module: [names]}} + image id + export-run count + declared sha. `sha` is over the canonical content."""

    def __init__(self, data):
        self.data = data
        self.fixture = bool(data.get("fixture", False))
        self.image_id = data.get("image_id")
        self.runs = data.get("export_runs")
        self.langs = {k: {m: sorted(set(v)) for m, v in data["exports"][k].items()} for k in data["exports"]}
        self.sha = util.sha_obj({"image_id": self.image_id, "exports": self.langs})
        if data.get("sha256") and data["sha256"] != self.sha:
            raise ValueError("export file sha does not match its content")

    @classmethod
    def load(cls, path):
        with open(path, "r", encoding="utf-8") as f:
            return cls(json.load(f))

    def require_real(self):
        if self.fixture:
            raise ValueError("a FIXTURE export cannot be used to build rows")
        if self.runs is None or self.runs < 3:
            raise ValueError("the export needs 3 identical runs (T63-B8)")
        if not self.data.get("sha256"):
            raise ValueError("the export file must DECLARE its sha256 (hashed before any row, K2): an undeclared sha cannot be checked against the L-0 image record")
        if not self.image_id:
            raise ValueError("the export file must name the image id it was produced on (K2)")
        return self

    def modules(self, lang):
        return self.langs[lang]


# ---- name surgery ---------------------------------------------------------------------------------------------------------------------
def split_name(name):
    """-> (tokens, seps): separator names split at - _ ; camelCase / PascalCase at humps; bare stems at syllables. seps[i] joins tokens[i], tokens[i+1]."""
    if "-" in name or "_" in name:
        toks = re.split(r"[-_]", name)
        seps = re.findall(r"[-_]", name)
        return toks, seps
    humps = re.findall(r"[A-Z]?[a-z0-9]+|[A-Z]+(?![a-z])", name)
    if len(humps) >= 2 and "".join(humps) == name:
        return humps, [""] * (len(humps) - 1)
    syl = SYL.findall(name.lower())
    if len(syl) >= 2 and "".join(syl) == name.lower():
        # keep the original case of the first letter
        out, pos = [], 0
        for s in syl:
            out.append(name[pos:pos + len(s)])
            pos += len(s)
        return out, [""] * (len(out) - 1)
    return [name], []


def join_name(toks, seps):
    out = toks[0]
    for t, s in zip(toks[1:], seps):
        out += s + t
    return out


def _syllable_mutation(name, rng):
    """One-edit near-miss that keeps the consonant/vowel structure (so name-shape probes cannot see the edit)."""
    idx = [i for i, ch in enumerate(name) if ch.isalpha()]
    rng.shuffle(idx)
    for i in idx:
        ch = name[i].lower()
        pool = VOW if ch in VOW else (CON if ch in CON else "")
        if not pool:
            continue
        rep = rng.choice([c for c in pool if c != ch])
        out = name[:i] + (rep.upper() if name[i].isupper() else rep) + name[i + 1:]
        if out != name:
            return out
    return None


def compose(names, rng, taken):
    """Plausible hallucination: the first j tokens of one name + the rest of another with the SAME token count (so length and shape follow the
    population of real names; the composition is built from neighbouring entries' tokens). Absent from `taken`."""
    parts = [(n,) + split_name(n) for n in names]
    by_n = {}
    for nm_, toks, seps in parts:
        if len(toks) >= 2:
            by_n.setdefault(len(toks), []).append((nm_, toks, seps))
    keys = [k for k, v in by_n.items() if len(v) >= 2]
    if not keys:
        return None
    for _ in range(60):
        n = rng.choice(keys)
        (a, ta, sa), (b, tb, sb) = rng.sample(by_n[n], 2)
        j = rng.randrange(1, n)
        cand = join_name(ta[:j] + tb[j:], sa)
        if cand not in taken and cand not in (a, b) and cand[0].isalpha():
            return cand
    return None


def plaus_flag(name, neighbours):
    """M-PLAUS: None = no (non-generic) token of the queried name appears in the neighbouring names; low = one token; high = every token (>= 2)."""
    toks = tokens_of(name)
    if not toks:
        return None
    pool = {t for n in neighbours if n != name for t in tokens_of(n)}
    hit = sum(1 for t in toks if t in pool)
    if hit == 0:
        return None
    return "high" if (hit == len(toks) and len(toks) >= 2) else "low"


def _token_neighbours(nm, p, k, rng, tag):
    """k in {0, 1, 2}: names sharing one stem token with p each (M-PLAUS decoration for package-style names)."""
    toks, seps = split_name(p)
    if len(toks) < 3 or k == 0:
        return []
    out = []
    for i in range(k):
        fresh = nm.get("ns.noun.module", "%s-tn%d" % (tag, i))
        t = list(toks)
        t[i % 2] = fresh
        out.append(join_name(t, seps))
    return out


# ---- EX-A1 ------------------------------------------------------------------------------------------------------------------------
def _a1_base(ctx, g, rng, c):
    from LP_COMMON.ns import Names
    nm = Names("T63", "%s/%s" % (ctx.seed, g["seed"]), deny_check=ctx.deny_check)
    n_list = rng.randint(12, 22)
    names, k = [], 0
    while len(names) < n_list and k < 300:
        k += 1
        cand = nm.get("ns.package", "l%d" % k)
        if cand not in names:
            names.append(cand)
    regs = [{"id": "R%d" % (i + 1), "host": nm.get("ns.registry_host", "h%d" % i)} for i in range(3)]
    return nm, names, regs


def _a1_spec(reg, listing, query, kind, label, other, mech):
    return {"head": "EXISTS", "sub": "EX-A1", "registry": reg, "listing": listing, "range": [listing[0], listing[-1]], "query_name": query, "kind": kind,
            "label": label, "other": other, "mech": mech}


def _ensure_near(spec, rng):
    """Single EX-A1 rows (YES, EX-N2, EX-N5): list ONE near-miss neighbour (one syllable-letter edit) of the QUERY, so that "a listed name one edit away" is
    present on every such row whatever the label (EX-N4 rows carry it by construction: the asked name's original is listed). The old per-label random rate
    (42% on YES rows only) left the nearest-listed-distance feature at AUC 0.61 (T63-K8)."""
    q, lst = spec["query_name"], spec["listing"]
    if any(n != q and _edit1(q, n) for n in lst):
        return spec
    for _ in range(40):
        nb = _syllable_mutation(q, rng)
        if nb and nb != q and nb not in lst:
            new = sorted(set(lst) | {nb})
            spec["listing"], spec["range"] = new, [new[0], new[-1]]
            return spec
    raise Reject("no near-miss neighbour")


def _edit1(a, b):
    if a == b:
        return False
    if len(a) == len(b):
        return sum(1 for x, y in zip(a, b) if x != y) == 1
    if abs(len(a) - len(b)) == 1:
        s_, l_ = (a, b) if len(a) < len(b) else (b, a)
        return any(l_[:i] + l_[i + 1:] == s_ for i in range(len(l_)))
    return False


def _edge_free(specs):
    """The asked name lies STRICTLY inside the shown range for both labels (a YES name at the first or last position of a complete range, never a NO name,
    was a position cue: T63-K8 pos_edge feature)."""
    for sp in specs:
        lst, q = sp["listing"], sp["query_name"]
        if not (lst[0] < q < lst[-1]):
            raise Reject("query at the edge of the complete range")
    return specs


def gen_a1(ctx, g):
    specs = _gen_a1_raw(ctx, g)
    if len(specs) == 1 and specs[0]["kind"] in (None, "EX-N2", "EX-N5"):
        rng = ctx.rng("exa1near", g["seed"])
        specs = [_ensure_near(specs[0], rng)]
    return _edge_free(specs)


def _gen_a1_raw(ctx, g):
    c = g["cell"]
    rng = ctx.rng("exa1", g["seed"])
    nm, names, regs = _a1_base(ctx, g, rng, c)
    reg = rng.choice(regs)
    kind, label, pair = c["kind"], c["label"], c.get("pair")
    k_share = rng.choice((0, 0, 1, 2))
    if label == "YES" and not pair:
        p = rng.choice(names[1:-1] if len(names) > 3 else names)
    elif kind == "EX-N2":
        p = nm.get("ns.package", "x%d" % rng.randrange(10 ** 6))
    else:
        p = rng.choice(names[1:-1] if len(names) > 3 else names)
    extra = _token_neighbours(nm, p, k_share, rng, "a1") if p else []
    base_names = sorted(set(names) | set(extra) | ({p} if (kind != "EX-N2" and (label == "YES" or pair)) else set()))
    lo, hi = base_names[0], base_names[-1]
    decoy_other = None
    if label == "YES" and not pair and rng.random() < 0.23:          # a second registry block on YES rows at the rate N2 rows carry one (K8 has-other feature)
        oreg2 = rng.choice([r for r in regs if r["id"] != reg["id"]])
        on2 = set()
        j = 0
        while len(on2) < rng.randint(8, 14):
            j += 1
            cand = nm.get("ns.package", "d%d" % j)
            if cand != p:
                on2.add(cand)
        on2 = sorted(on2)
        decoy_other = {"registry": oreg2, "listing": on2, "range": [on2[0], on2[-1]]}
    mech = lambda q, lst: {"plaus": plaus_flag(q, lst), "kind": kind}
    if kind == "EX-N2":
        if not (lo < p < hi):
            raise Reject("N2 outside range")
        oreg = rng.choice([r for r in regs if r["id"] != reg["id"]])
        onames = {p}
        j = 0
        while len(onames) < rng.randint(8, 14):
            j += 1
            onames.add(nm.get("ns.package", "o%d" % j))
        onames = sorted(onames)
        no = _a1_spec(reg, base_names, p, kind, "NO", {"registry": oreg, "listing": onames, "range": [onames[0], onames[-1]]}, mech(p, base_names))
        if not pair:
            return [no]
        yes = _a1_spec(oreg, onames, p, None, "YES", {"registry": reg, "listing": base_names, "range": [lo, hi]}, mech(p, onames))
        return [yes, no]
    if label == "YES" and not pair:
        return [_a1_spec(reg, base_names, p, None, "YES", decoy_other, mech(p, base_names))]
    if kind == "EX-N4":
        for _ in range(60):
            q = _syllable_mutation(p, rng)
            if q and q not in base_names and lo < q < hi:
                break
        else:
            raise Reject("N4")
    elif kind == "EX-N5":
        for _ in range(60):
            q = compose(base_names, rng, set(base_names))
            if q and lo < q < hi:
                break
        else:
            raise Reject("N5")
    else:
        raise Reject("kind")
    no = _a1_spec(reg, base_names, q, kind, "NO", None, mech(q, base_names))
    if not pair:
        return [no]
    yes = _a1_spec(reg, base_names, p, None, "YES", None, mech(p, base_names))
    return [yes, no]


def gold_a1(spec):
    return "YES" if spec["query_name"] in spec["listing"] else "NO"


# ---- EX-A2 ------------------------------------------------------------------------------------------------------------------------
def _versions(rng, n):
    major, minor = rng.randint(1, 4), rng.randint(0, 6)
    return ["%d.%d.0" % (major, minor + i) for i in range(n)]


def _a2_spec(lib, V, exports, qmod, sym, kind, label, hist, mech):
    return {"head": "EXISTS", "sub": "EX-A2", "library": lib, "version": V, "exports": exports, "query_module": qmod, "query_symbol": sym,
            "kind": kind, "label": label, "history": hist, "mech": mech}


def gen_a2(ctx, g):
    from LP_COMMON.ns import Names
    c = g["cell"]
    rng = ctx.rng("exa2", g["seed"])
    nm = Names("T63", "%s/%s" % (ctx.seed, g["seed"]), deny_check=ctx.deny_check)
    lib = nm.get("ns.package", "lib")
    mods = [nm.get("ns.noun.module", "m%d" % i) for i in range(rng.randint(3, 4))]
    if len(set(mods)) < len(mods):
        raise Reject("module names collide")
    versions = _versions(rng, 4)
    pool, j = [], 0
    while len(pool) < 36:
        j += 1
        s = nm.get("ns.noun.symbol", "s%d" % j)
        if s not in pool:
            pool.append(s)
    exports = {m: sorted(rng.sample(pool, rng.randint(4, 8))) for m in mods}
    shown_idx = 2
    V = versions[shown_idx]
    hist = {v: {m: list(exports[m]) for m in mods} for v in versions}
    kind, label, pair = c["kind"], c["label"], c.get("pair")
    qmod = mods[rng.randrange(len(mods))]
    taken = {s for m in mods for s in exports[m]}
    allsyms = sorted(taken)
    if sum(len(v) for v in exports.values()) > C.EX_LIST_MAX:
        raise Reject("list too long")
    mech = lambda q, ver=None, xhigh=False: {"plaus": plaus_flag(q, allsyms), "kind": kind, "ver": ver, "xhigh": xhigh}
    if label == "YES" and not pair:
        sym = rng.choice(exports[qmod])
        return [_a2_spec(lib, V, exports, qmod, sym, None, "YES", hist, mech(sym))]
    if kind == "EX-N1":
        sym = rng.choice(exports[qmod])
        others = [m for m in mods if m != qmod and sym not in exports[m]]
        if not others:
            raise Reject("N1")
        m2 = rng.choice(others)
        holders = [m for m in mods if sym in exports[m]]
        no = _a2_spec(lib, V, exports, m2, sym, kind, "NO", hist, mech(sym, xhigh=len(holders) >= 2))
        if not pair:
            # a single N1 row: a symbol of another module asked of this module
            return [no]
        yes = _a2_spec(lib, V, exports, qmod, sym, None, "YES", hist, mech(sym))
        return [yes, no]
    if kind == "EX-N3":
        sym = nm.get("ns.noun.symbol", "v%d" % rng.randrange(10 ** 6))
        if sym in taken:
            raise Reject("N3")
        gap = c.get("ver", "low")
        h2 = copy.deepcopy(hist)
        src = versions[shown_idx - 1] if gap == "high" else versions[0]    # present one version before the shown one, or two or more versions ago
        h2[src][qmod] = sorted(h2[src][qmod] + [sym])
        return [_a2_spec(lib, V, exports, qmod, sym, kind, "NO", h2, mech(sym, ver=gap))]
    if kind == "EX-N4":
        sym0 = rng.choice(exports[qmod])
        for _ in range(60):
            sym = _syllable_mutation(sym0, rng)
            if sym and sym not in taken:
                break
        else:
            raise Reject("N4")
        no = _a2_spec(lib, V, exports, qmod, sym, kind, "NO", hist, mech(sym))
        if not pair:
            return [no]
        return [_a2_spec(lib, V, exports, qmod, sym0, None, "YES", hist, mech(sym0)), no]
    if kind == "EX-N5":
        sym = compose(sorted(taken), rng, taken)
        if not sym:
            raise Reject("N5")
        return [_a2_spec(lib, V, exports, qmod, sym, kind, "NO", hist, mech(sym))]
    raise Reject("kind")


def gold_a2(spec):
    return "YES" if spec["query_symbol"] in spec["exports"].get(spec["query_module"], ()) else "NO"


# ---- EX-B -------------------------------------------------------------------------------------------------------------------------
LANG_OF = {"python": "python", "node": "javascript", "go": "go"}


def _b_spec(ex, lang, mod, name, view, kind, label, rng, xhigh=False):
    full = ex.modules(lang)[mod]
    shown = rng_range = None
    if view == "B1":
        import bisect
        srt = sorted(full)
        if len(srt) <= C.EX_LIST_MAX:
            shown = srt
            if not (srt[0] <= name <= srt[-1]):
                raise Reject("name outside the complete list")
        else:
            pos = bisect.bisect_left(srt, name)
            lo_i = max(0, min(pos - rng.randint(5, 30), len(srt) - C.EX_LIST_MAX))
            window = srt[lo_i:lo_i + C.EX_LIST_MAX]
            if not (window[0] <= name <= window[-1]):
                raise Reject("name outside window")
            shown, rng_range = window, [window[0], window[-1]]
    return {"head": "EXISTS", "sub": "EX-" + view, "lang": lang, "module": mod, "query_name": name, "view": view, "shown": shown,
            "range": rng_range, "kind": kind, "label": label, "export_sha": ex.sha, "image_id": ex.image_id,
            "mech": {"plaus": plaus_flag(name, full), "kind": kind, "xhigh": xhigh}}


def gen_b(ctx, g):
    c = g["cell"]
    ex = ctx.exports
    if ex is None:
        raise ValueError("EX-B rows (EX-B1 and EX-B2) need the sha-bound L-0 image-record stdlib export; none supplied")
    rng = ctx.rng("exb", g["seed"])
    lang, view, kind, label, pair = c["lang"], c["view"], c["kind"], c["label"], c.get("pair")
    mods = {m: v for m, v in ex.modules(lang).items() if len(v) >= 6}
    if not mods:
        raise Reject("no modules")
    mod = rng.choice(sorted(mods))
    full = mods[mod]
    taken = set(full)
    if label == "YES" and not pair:
        return [_b_spec(ex, lang, mod, rng.choice(full), view, None, "YES", rng)]
    if kind == "EX-N1":
        name = rng.choice(full)
        hold = [m for m, v in mods.items() if name in v]
        cand = [m for m, v in mods.items() if name not in set(v)]            # B8: the asked module's FULL export is checked
        if not cand:
            raise Reject("N1")
        m2 = rng.choice(sorted(cand))
        no = _b_spec(ex, lang, m2, name, view, kind, "NO", rng, xhigh=len(hold) >= 2)
        if not pair:
            return [no]
        return [_b_spec(ex, lang, mod, name, view, None, "YES", rng), no]
    if kind == "EX-N4":
        name0 = rng.choice(full)
        for _ in range(60):
            name = _syllable_mutation(name0, rng)
            if name and name not in taken:
                break
        else:
            raise Reject("N4")
        no = _b_spec(ex, lang, mod, name, view, kind, "NO", rng)
        if not pair:
            return [no]
        return [_b_spec(ex, lang, mod, name0, view, None, "YES", rng), no]
    if kind == "EX-N5":
        name = compose(full, rng, taken)
        if not name:
            raise Reject("N5")
        return [_b_spec(ex, lang, mod, name, view, kind, "NO", rng)]
    raise Reject("kind")


def gold_b(spec, ex):
    return "YES" if spec["query_name"] in set(ex.modules(spec["lang"]).get(spec["module"], ())) else "NO"
