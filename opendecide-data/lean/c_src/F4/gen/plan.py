"""Card plans (G0 spec 7.1, 7.5) and the unit plan (6, 8): card key, feature plan, printed clause set, styles,
wordings, label names, examples, yes rate; global allocation of selection units to cards by form quotas."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import f4lex as L  # noqa: E402
import packs_f4 as P  # noqa: E402
from sampler import CardPlan, date_of  # noqa: E402

LEAN = HERE.parents[2]
FMT1 = LEAN / "c_src" / "formats" / "formats-1"
sys.path.insert(0, str(FMT1))
from fmt1 import labels as flabels  # noqa: E402
from fmt1 import pool as fpool  # noqa: E402


def uh(*parts):
    h = hashlib.sha256("\x1f".join(str(p) for p in parts).encode()).digest()
    return int.from_bytes(h[:8], "big") / 2 ** 64


def clause_set(world, short, feats, has_yn, has_choice, *, unless=None, trust_list=False, multitype=False,
               attack_clause=False, link_cols=False, containers=(), qtys=True):
    """7.1: core clauses + the clauses of every feature in the card plan."""
    c = set()
    if short:
        c |= {"3s", "24"}
        if has_yn:
            c.add("26")
        if has_choice:
            c.add("31")
        return frozenset(c)
    c |= {"1", "3", "4", "5", "23", "24", "25b"} if world == "OW" else {"2", "3c", "5c", "23", "24", "25b"}
    if has_yn:
        c.add("26")
    if has_choice:
        c.add("31")
    if "exc" in feats:
        c |= {"6", "17"}
        if world == "OW":
            c.add("7a" if unless == "strict" else "7b")
    if "onlyif" in feats and world == "OW":
        c.add("8")
    if "or" in feats or "xor" in feats:
        c.add("9")
    if "kofn" in feats:
        c.add("10")
    if "cmp" in feats and qtys:
        c |= {"11", "14", "15", "16"}
    if "rng" in feats and qtys:
        c |= {"12", "14", "15"}
    if "date" in feats:
        c.add("13")
    if "table" in feats:
        if world == "OW":
            if containers & {"text"}:
                c.add("18.2")
            if containers & {"typed"}:
                c.add("18.3")
        else:
            c.add("18.4")
        if link_cols:
            c.add("18.5")
    if "closure" in feats and world == "OW":
        c.add("18c")
    if "hedge" in feats and world == "OW":
        c |= {"19", "20"}
    if "ehedge" in feats and world == "OW":
        c.add("19")
    if "lookalike" in feats:
        c.add("21")
    if "attrib" in feats:
        c.add("22" if trust_list else "22b")
    if "standing" in feats:
        c.add("25a")
    if "link" in feats and world == "OW":
        c.add("27")
    if multitype:
        c.add("28")
    if attack_clause:
        c.add("29")
    if "masked" in feats:
        c.add("30")
    return frozenset(c)


CONTAINERS = {
    "S1": ("prose", "memo"),
    "S2": ("bullet_sop", "markdown_table", "html_snippet", "memo", "json", "yaml"),
    "S3": ("markdown_table", "html_snippet", "memo", "json", "yaml"),
    "S4": ("bullet_sop", "markdown_table", "memo", "html_snippet", "prose"),
    "S5": ("prose", "memo", "markdown_table", "html_snippet", "bullet_sop"),
}
INLINE = ("prose.plain", "prose.titled_caps", "prose.section_signs")


def styles_for(sampler, bullets, held_out, *, single_ok=False, s4=False):
    out = []
    for s in fpool.styles(held_out=held_out, compat="F4"):
        if s["container"] not in CONTAINERS[sampler] and not (single_ok and s["container"] == "csv"):
            continue
        sk = s["skin"]
        if sk in ("json.lines", "json.array") and not single_ok:
            continue
        if bullets and (s["container"] in ("json", "yaml", "csv", "prose")):
            continue
        if s["container"] == "prose" and (s4 or sampler == "S5") and sk in INLINE and sampler == "S4":
            continue
        if sampler == "S4" and s["container"] == "prose" and sk not in ("prose.lines", "prose.numbered_paras"):
            continue
        out.append(s)
    return out


CLAUSE_COST = {"exc": 140, "link": 15, "cmp": 175, "rng": 50, "date": 91, "or": 58, "xor": 58, "kofn": 18,
               "onlyif": 35, "closure": 79, "hedge": 89, "ehedge": 69, "lookalike": 16, "attrib": 110,
               "standing": 32, "table": 40, "multitype": 28}


def lean_features(pack, W, sampler, inverted, rng, budget):
    """Feature plan under a clause-token budget (7.6 card budget: choice rows print the moved card text twice)."""
    order = ["link", "lookalike", "kofn", "rng", "onlyif", "or", "xor", "date", "closure", "cmp", "exc", "hedge",
             "ehedge"]
    rng.shuffle(order)
    feats = set()
    if sampler == "S3" or inverted:
        feats.add("table")
        budget -= CLAUSE_COST["table"]
    if sampler == "S4":
        feats.add("attrib")
        budget -= 18 if rng.random() < 0.5 else CLAUSE_COST["attrib"]
    for f in order:
        if f in ("onlyif", "closure", "hedge", "ehedge") and W != "OW":
            continue
        if f in ("link",) and (not pack["links"] or inverted):
            continue
        if f == "link":
            feats.add(f)            # cheap clause; 2.3 link quota
            budget -= CLAUSE_COST[f]
            continue
        if f == "rng" and not inverted and CLAUSE_COST[f] <= budget:
            feats.add(f)            # cheapest threshold clause; 2.3 threshold / date quota
            budget -= CLAUSE_COST[f]
            continue
        if f in ("cmp", "rng") and not pack["qty"]:
            continue
        c = CLAUSE_COST[f]
        if c <= budget and rng.random() < 0.6:
            feats.add(f)
            budget -= c
    if inverted and pack["qty"] and "cmp" not in feats and budget >= CLAUSE_COST["cmp"]:
        feats.add("cmp")
    return feats


def make_card(card_no: int, pack: dict, sampler: str, world, short: bool, inverted: bool, rng: random.Random, *,
              held_out=False, forms=None, fewshot=False, lean=None, ds=None):
    pt = pack["types"]
    feats = set()
    W = world
    # --- feature plan
    if short:
        if pack["links"] and rng.random() < 0.6:
            feats.add("link")
    elif lean is not None:
        feats = lean_features(pack, W, sampler, inverted, rng, lean)
    else:
        # 2.3 inference mix (link >= 30%, exception >= 25%, threshold / date >= 20% of derived rows): the yes/no
        # cards carry these features on most cards
        if rng.random() < 0.95:
            feats.add("exc")
        if pack["links"] and not inverted and rng.random() < 0.9:
            feats.add("link")
        if pack["qty"] and rng.random() < (0.85 if inverted else 0.8):
            feats.add("cmp")
        if pack["qty"] and rng.random() < 0.25:
            feats.add("rng")
        if rng.random() < (0.5 if inverted else 0.5):
            feats.add("date")
        if rng.random() < 0.4:
            feats.add("or")
        if rng.random() < 0.25:
            feats.add("xor")
        if W == "OW" and rng.random() < 0.25:
            feats.add("onlyif")
        if W == "OW" and rng.random() < 0.35:
            feats.add("closure")
        if W == "OW" and rng.random() < 0.35:
            feats.add("hedge")
        if W == "OW" and rng.random() < 0.3:
            feats.add("ehedge")
        if rng.random() < 0.4:
            feats.add("lookalike")
        if sampler == "S4" or (sampler == "S5" and rng.random() < 0.5):
            feats.add("attrib")
        if sampler == "S3" or inverted:
            feats.add("table")
    if lean is None and not short and not inverted:
        # card budget for yes/no rows (card printed once): keep the clause text near 900 tokens
        est = (442 if W == "OW" else 313) + 60 + sum(CLAUSE_COST.get(f, 0) for f in feats)
        fl = sorted(feats - {"table", "attrib"})
        rng.shuffle(fl)
        keep_last = ("exc", "link", "cmp", "date")
        fl.sort(key=lambda f: f not in keep_last)     # popped from the end: the inference-mix features go last
        while est > 1100 and fl:
            f = fl.pop()
            feats.discard(f)
            est -= CLAUSE_COST.get(f, 0)
    single_ok = inverted and sampler == "S3" and rng.random() < 0.5
    if single_ok:
        feats.add("standing")
    elif not short and lean is None and rng.random() < 0.12:
        feats.add("standing")
    if lean is not None:
        bullets = "kofn" in feats or ((not single_ok) and rng.random() < 0.4)
    else:
        bullets = (not short) and (not single_ok) and ("standing" not in feats) and rng.random() < 0.55
        if bullets and rng.random() < 0.5:
            feats.add("kofn")
    if single_ok:
        bullets = False
        feats.discard("kofn")
    # --- types
    if inverted:
        k = 1 if rng.random() < 0.5 else 2
    elif "link" in feats:
        k = min(len(pt), rng.choice((2, 2, 3)))
    else:
        k = 1 if rng.random() < 0.3 else min(len(pt), 2)
    if "link" in feats and pack["links"]:
        lk = rng.choice(pack["links"])
        chosen = [lk["from"]] + ([lk["to"]] if lk["to"] != lk["from"] else [])
        others = [i for i in range(len(pt)) if i not in chosen]
        rng.shuffle(others)
        chosen += others[:max(0, k - len(chosen))]
    else:
        chosen = list(range(len(pt)))
        rng.shuffle(chosen)
        chosen = chosen[:k]
    remap = {p: i for i, p in enumerate(chosen)}
    types = [tuple(pt[i]) for i in chosen]
    links = [{"active": l["active"], "passive": l["passive"], "from": remap[l["from"]], "to": remap[l["to"]]}
             for l in pack["links"] if l["from"] in remap and l["to"] in remap] if "link" in feats else []
    if not links:
        feats.discard("link")
    qtys = []
    for q in pack["qty"]:
        t = remap.get(q["type"]) if q["type"] is not None else None
        if q["type"] is not None and t is None:
            continue
        qtys.append({**q, "type": t})
    qtys = qtys[:3]
    if not qtys:
        feats -= {"cmp", "rng"}
    dattrs = [(a, None) for a in pack["dates"][:2]]
    w = pack.get("window")
    lo, hi = dt.date(2041, 1, 1), dt.date(2043, 12, 31)
    if w and isinstance(w, (list, tuple)) and w[0]:
        try:
            lo = date_of(w[0])
            hi = date_of(w[1]) if isinstance(w[1], str) else lo + dt.timedelta(days=int(w[1]))
        except (ValueError, TypeError):
            pass
    if (hi - lo).days < 120:
        hi = lo + dt.timedelta(days=400)
    unless = None
    if "exc" in feats:
        unless = ("strict" if rng.random() < 0.5 else "listc") if W == "OW" else "cw"
    trust_list = "attrib" in feats and rng.random() < 0.5
    tr, un = pack["trusted"][:3], pack["untrusted"][:3]
    if "attrib" in feats and (not tr or not un):
        trust_list = False
    if trust_list:
        trust = ("list", tuple(tr))
    elif "attrib" in feats:
        trust = ("all",)
    else:
        trust = None
    preds = list(pack["preds"])
    rng.shuffle(preds)
    ex_preds = tuple(preds[:3])
    preds = preds[3:]
    ids, looks = P.ids_for_card(f"{pack['pack_id']}#{card_no}", 96, 10)
    ids = ids + [v for _, v in looks]
    forms = forms or {}
    has_yn = any(f.startswith("YN") for f in forms)
    has_ch = any(not f.startswith("YN") for f in forms)
    if any(f in forms for f in ("CH-3", "CH-2")) and not short:
        feats.add("masked")
    attack_clause = rng.random() < 0.5
    link_cols = "table" in feats and bool(links)
    containers = {"text", "typed"} if "table" in feats else set()
    clauses = clause_set(W, short, feats, has_yn, has_ch, unless=unless, trust_list=trust_list,
                         multitype=len(types) > 1, attack_clause=attack_clause and not short,
                         link_cols=link_cols, containers=containers, qtys=bool(qtys))
    # definition style
    if short:
        ds = "short"
    else:
        u = rng.random()
        ds_ = "one_line" if u < 0.22 else ("one_line_examples" if u < 0.82 else "decision_list")
        ds = ds or ds_          # the card plan may fix the style (7.5 card shares)
        if inverted or single_ok:
            ds = "one_line"     # card budget: large-k rows on cards with short moved text
        elif lean is not None and ds == "one_line_examples" and lean < 260:
            ds = "one_line" if rng.random() < 0.5 else "decision_list"
    ex_kinds = ()
    if ds == "one_line_examples":
        kinds = ["fwd"] + (["bwd"] if W == "OW" else []) + (["exc"] if "exc" in feats else [])
        rng.shuffle(kinds)
        ex_kinds = tuple(kinds[:(1 if lean is not None else rng.choice((1, 2)))])
    st = styles_for(sampler, bullets, held_out, single_ok=single_ok, s4=(sampler == "S4"))
    if inverted:
        compact = [s_ for s_ in st if s_["container"] in ("csv", "markdown_table") or s_["skin"] == "memo.internal"]
        st = compact or st
    if not st:
        raise ValueError("no styles")
    st_ids = [s["id"] for s in fpool.card_style_set(st, min(8, len(st)), "F4", pack["pack_id"], str(card_no))]
    fam = sorted({w.split(".")[1] for w in ["wd.F4.A", "wd.F4.B", "wd.F4.C", "wd.F4.D", "wd.F4.E", "wd.F4.F"]})
    wf = "F4." + "ABCDEF"[card_no % 6]
    title = rng.choice([d[:1].upper() + d[1:] for d in pack["docs"]] or list(L.FALLBACK_TITLES)) \
        if rng.random() < 0.8 else rng.choice(L.FALLBACK_TITLES)
    cp = CardPlan(card_id="", sampler=sampler, pack=pack, world=W, short=short, inverted=inverted, types=types,
                  umbrella=tuple(pack["umbrella"]), feats=feats, unless=unless, trust=trust, links=links, qtys=qtys,
                  dattrs=dattrs, window=(lo, hi), sources=(tr, un), preds=preds, ids=ids, looks=looks, forms=forms,
                  yes_rate=rng.uniform(0.2, 0.8), defs_style=ds, fewshot=fewshot, wording_family=wf, styles=st_ids)
    cp.clause_set = clauses
    cp.example_kinds = ex_kinds
    cp.example_preds = ex_preds
    cp.defs_variant = rng.choice(("DV11", "DV12", "DV13", "DV14", "DV15", "DV16"))
    cp.persona_tpl = rng.randrange(len(L.PERSONA_TEMPLATES))
    cp.date_fmt = rng.choice(("dmy", "dmy", "iso", "mdy"))
    cp.title = title
    cp.bullets = bullets
    cp.single_ok = single_ok
    cp.max_conds = 3 if (bullets and not inverted) else 2
    cp.rules_where = "card" if single_ok else "record"
    cp.attack_clause = attack_clause
    cp.fewshot_block = None
    # label names (CH-3 / CH-2): one fixed plain set, one mask scheme and one swap-word set per card
    key = f"{pack['pack_id']}#{card_no}"
    p3 = L.CH3_OPTION_SETS[int(uh("ch3set", key) * len(L.CH3_OPTION_SETS))]
    p2 = L.CH2_OPTION_SETS[int(uh("ch2set", key) * len(L.CH2_OPTION_SETS))]
    scheme = rng.choice(["MS%02d" % i for i in range(1, 21)])
    m3 = flabels.masked_ids(scheme, 3, key + ":3")
    m2 = flabels.masked_ids(scheme, 2, key + ":2")
    excl = list(preds[:40]) + [t for t, _ in types] + list(L.OUTCOME_WORDS)
    try:
        s3 = flabels.swapped_names("mixed", 3, key + ":3", exclude=excl)
        s2 = flabels.swapped_names("mixed", 2, key + ":2", exclude=excl)
    except Exception:
        s3, s2 = ["Amber", "Cobalt", "Willow"], ["Amber", "Cobalt"]
    for w_ in s3 + s2:
        if w_.lower() in L.OUTCOME_WORDS:
            raise ValueError("swap word is an outcome word")
    cp.label_names = {"plain": {"CH-3": p3, "CH-2": p2},
                      "masked": {"CH-3": dict(zip("FRO", m3)), "CH-2": dict(zip("FR", m2))},
                      "swapped": {"CH-3": dict(zip("FRO", s3)), "CH-2": dict(zip("FR", s2))},
                      "scheme": scheme}
    label_schema = (W or "any", tuple(sorted(forms)), p3, p2, scheme, tuple(m3), tuple(s3)) \
        if any(f in forms for f in ("CH-3", "CH-2")) else (W or "any", tuple(sorted(forms)))
    rule_set = (tuple(sorted(clauses)), unless, trust[0] if trust else None)
    cp.card_id = "F4c-" + hashlib.sha256(json.dumps(["F4", sampler, pack["pack_id"], label_schema, rule_set, wf],
                                                    default=str).encode()).hexdigest()[:12]
    cp.label_schema, cp.rule_set = label_schema, rule_set
    return cp
