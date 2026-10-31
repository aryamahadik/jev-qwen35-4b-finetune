"""F2 gates over the written outputs: G15 (check_rows, loader round trip under random permutations, relation units,
real-tokenizer lengths with `instructions` counted twice by the layout), G18 (no option_level), negcount quotas,
G4 metamorphic relations (>= 3 per sampler, 100% on >= 1,000 rows each), G3 re-run, and balance statistics.

Run: .venv/bin/python -m gen.gates [--files ...]  (writes out/gates_report.json)
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import random
import re
import sys
from collections import Counter, defaultdict

from . import canon, rowkit, solve_b
from .common import LEAN, OUT, TMP, progress, read_jsonl, write_json
from .parse import parse_row

FILES = {"candidates": "candidates_r1.jsonl", "qc": "qc_sample.jsonl", "mixdev": "mixdev_S5.jsonl"}


def _dio():
    sys.path.insert(0, str(LEAN))
    import decoder_io as dio
    dio.STYLE, dio.LAYOUT = "cygnet", "schema_branch_mark"
    return dio


def _perm(rid, n, k):
    rng = random.Random(int.from_bytes(hashlib.sha256(f"F2-g15:{rid}:{k}".encode()).digest()[:8], "big"))
    p = list(range(n))
    rng.shuffle(p)
    return p


def g15(rows, tok, dio, td):
    """check_rows; gold letter maps back under 3 random option orders (MR1 too); tokens on the rendered chat."""
    from .render import fcard
    probs = Counter()
    toks = []
    td.check_rows(rows)
    over = []
    for r in rows:
        n = len(r["options"]) if r["qtype"] == "choice" else 2
        r["_loader_perm_ok"] = True
        for k in range(3):
            res = fcard.loader_check(r, perm=_perm(r["id"], n, k), check_rows=False)
            if not res["ok"]:
                probs["loader_perm:" + res["problems"][0][:40]] += 1
                r["_loader_perm_ok"] = False
                break
        p = _perm(r["id"], n, 0)
        if n > len(dio.WIDE):
            import string as _s
            dio.WIDE = list(_s.ascii_uppercase) + [a + b for a in _s.ascii_uppercase for b in _s.ascii_uppercase]
        prompt = dio.user_msg(r, p)
        t = len(tok(dio.render_chat(tok, dio.CYGNET_SYSTEM, prompt), add_special_tokens=False)["input_ids"])
        toks.append(t)
        r["_tok"] = t
        if t > 7900:
            probs["over_7900"] += 1
        if t >= 1900:
            over.append(r["id"])
        if r["meta"].get("option_level") is not None:
            probs["option_level_present"] += 1
    toks.sort()
    return {"problems": dict(probs), "rows": len(rows), "tokens_max": toks[-1] if toks else 0,
            "tokens_median": toks[len(toks) // 2] if toks else 0, "rows_ge_1900": len(over), "ge_1900_ids": over[:20],
            "rows_ge_2000": sum(1 for t in toks if t >= 2000)}


def units(rows, rels):
    by = defaultdict(list)
    for r in rows:
        by[r["call_id"]].append(r)
    probs = Counter()
    for cid, us in by.items():
        if len(us) > 3:
            probs["unit_over_3"] += 1
        if any(u.get("_tok", 0) >= 2000 for u in us) and len(us) > 2:
            probs["long_unit_over_2"] += 1
    ids = {r["id"]: r for r in rows}
    for x in rels:
        if x["a"] not in ids or x["b"] not in ids:
            probs["relation_dangling"] += 1
        elif ids[x["a"]]["call_id"] != ids[x["b"]]["call_id"]:
            probs["relation_split_unit"] += 1
    return {"units": len(by), "max_unit": max((len(v) for v in by.values()), default=0), "problems": dict(probs)}


def question_sentence(instr):
    """The row's question sentence, read back from `instructions` without the generator: the last sentence that ends
    with "?" and names a value or an entity id (wording and note sentences carry neither)."""
    sents = []
    for ln in instr.split("\n"):
        for part in re.split(r"(?<=[.!:])\s+", ln):
            part = part.strip()
            while "?" in part:
                j = part.find("?")
                sents.append(part[:j + 1].strip())
                part = part[j + 1:].strip()
    sents = [x for x in sents if re.search(r"\d", x)]
    return sents[-1] if sents else None


def negcount_recount(rows):
    """k_syn and k_all recomputed by the shared negcount on the question sentence read back from the row; must equal
    the logged "syn:" and "cue:" tags on 100% of yes/no rows."""
    sys.path.insert(0, str(LEAN))
    from c_src.common.negcount import count as nc
    agree, n = 0, 0
    for r in rows:
        if r["qtype"] != "noul":
            continue
        n += 1
        q = question_sentence(r["instructions"])
        e = r["meta"]["edge"]
        syn = int(next(t for t in e if t.startswith("syn:"))[4:])
        cue = int(next(t for t in e if t.startswith("cue:"))[4:])
        if q is not None:
            c = nc(q)
            agree += int((c.k_syn, c.k_all) == (syn, cue))
    return {"yes_no_rows": n, "tags_agree": agree, "rate": round(agree / max(1, n), 6)}


def negation(rows, rels):
    yn = [r for r in rows if r["qtype"] == "noul"]
    tag = lambda r, p: next((t for t in r["meta"]["edge"] if t.startswith(p)), None)  # noqa: E731
    syn = [int(tag(r, "syn:").split(":")[1]) for r in yn]
    by = defaultdict(list)
    for r in yn:
        by[r["call_id"]].append(r)
    dneg_with_aff = 0
    for r in yn:
        k = int(tag(r, "syn:").split(":")[1])
        if k >= 2:
            unit = by[r["call_id"]]
            if any(int(tag(u, "syn:").split(":")[1]) == 0 and u["id"] != r["id"] for u in unit):
                dneg_with_aff += 1
    n = len(yn) or 1
    return {"yes_no_rows": len(yn), "k_syn_ge1_share": round(sum(1 for k in syn if k >= 1) / n, 4),
            "k_syn_ge2_with_affirmative_twin_share": round(dneg_with_aff / n, 4),
            "pass": sum(1 for k in syn if k >= 1) / n >= 0.10 and dneg_with_aff / n >= 0.02}


# ----------------------------------------------------------------------------------------------------------------- G4

def _solve_row(row):
    LPp = parse_row(row)
    Pp = canon.canonize(LPp)
    names = [o["name"] for o in LPp["q"]["outs"]] if LPp["q"].get("kind") == "outcome" else LPp.get("_names")
    r = solve_b.solve(Pp, options=row.get("options"), names=names)
    if row["qtype"] == "noul":
        lab = 1 if r[1] else 0
    else:
        lab = rowkit.answer_text(row, LPp, r[0], r[1])
    return canon.structure_hash(Pp), lab, LPp


def _sub_all(row, a, b):
    r2 = copy.deepcopy(row)
    for k in ("state", "instructions", "card"):
        if r2.get(k):
            r2[k] = r2[k].replace(a, b)
    if r2.get("options"):
        r2["options"] = [o.replace(a, b) for o in r2["options"]]
    if isinstance(r2.get("gold"), str):
        r2["gold"] = r2["gold"].replace(a, b)
    return r2


ID_RX = re.compile(r"\b([A-Z]{2,4})-(\d{4})\b")


def mr_rename(row):
    """MR2: a consistent rename of the entity ID (every occurrence) leaves the structure hash and the label unchanged."""
    m = ID_RX.search(row.get("instructions") or "") or ID_RX.search(row.get("state") or "")
    if not m:
        return None
    old = m.group(0)
    new = f"{m.group(1)}-{(int(m.group(2)) + 4321) % 9000 + 1000}"
    if new in (row.get("state") or "") + (row.get("instructions") or ""):
        return None
    r2 = _sub_all(row, old, new)
    h1, l1, _ = _solve_row(row)
    h2, l2, _ = _solve_row(r2)
    return h1 == h2 and l1 == (l2 if row["qtype"] == "noul" else l2.replace(new, old) if isinstance(l2, str) else l2)


YEAR_RX = re.compile(r"\b(20[34]\d)\b")
_MON = "January|February|March|April|May|June|July|August|September|October|November|December"
# years inside the three U4 date forms only (ISO, "<day> <Month> <year>", "<Month> <day>, <year>"); a bare 20xx
# number elsewhere is an amount, not a year
DATE_YEAR_RX = [re.compile(r"\b()(20[34]\d)(?=-\d\d-\d\d\b)"),
                re.compile(r"\b(\d{1,2} (?:" + _MON + r") )(20[34]\d)\b"),
                re.compile(r"\b((?:" + _MON + r") \d{1,2}, )(20[34]\d)\b")]


def _shift_years(t):
    if not t:
        return t
    for rx in DATE_YEAR_RX:
        t = rx.sub(lambda m: m.group(1) + str(int(m.group(2)) + 28), t)
    return t


def mr_dateshift(row):
    """MR5: every date moved by +28 years (weekdays repeat; 2031-2049 -> 2059-2077): label unchanged."""
    txt = (row.get("state") or "") + (row.get("instructions") or "") + (row.get("card") or "")
    if not any(rx.search(txt) for rx in DATE_YEAR_RX):
        return None
    r2 = copy.deepcopy(row)
    sh = _shift_years
    for k in ("state", "instructions", "card"):
        r2[k] = sh(r2.get(k))
    if r2.get("options"):
        r2["options"] = [sh(o) for o in r2["options"]]
    if isinstance(r2.get("gold"), str):
        r2["gold"] = sh(r2["gold"])
    h1, l1, _ = _solve_row(row)
    h2, l2, _ = _solve_row(r2)
    return l2 == r2["gold"] if row["qtype"] == "choice" else l1 == l2


MONEY_T = re.compile(r"(\d+(?:\.\d+)?) ([A-Za-z]+)(?=( or more| or less)?\?)")


def mr_threshold(row):
    """MR8: on a threshold question, moving T away from the compared value never flips the label towards the other
    side of the comparison: raising T can only flip yes -> no for >= / > (no -> yes for <= / <), negations reversed."""
    if row["qtype"] != "noul":
        return None
    h, lab, LPp = _solve_row(row)
    q = LPp.get("q", {})
    if q.get("kind") != "thr":
        return None
    T = q["T"]
    from decimal import Decimal
    unit = Decimal("0.01") if "." in str(T) else Decimal(1)
    ins = row["instructions"]
    ts = f"{T:f}" if isinstance(T, Decimal) else str(T)
    qs = question_sentence(ins)
    if not qs or qs.count(ts) != 1 or ins.count(qs) != 1:
        return None
    ok = True
    for d in (unit * 7, -unit * 7):
        T2 = T + d
        if T2 <= 0:
            continue
        t2 = f"{T2.quantize(unit):f}"
        r2 = copy.deepcopy(row)
        r2["instructions"] = ins.replace(qs, qs.replace(ts, t2))    # T moves in the question sentence only
        h2, l2, _ = _solve_row(r2)
        aff1 = lab if q.get("neg", 0) % 2 == 0 else 1 - lab
        aff2 = l2 if q.get("neg", 0) % 2 == 0 else 1 - l2
        up = q["cmp"] in ("ge", "gt")
        if d > 0 and up and aff2 > aff1:
            ok = False
        if d < 0 and up and aff2 < aff1:
            ok = False
        if d > 0 and not up and aff2 < aff1:
            ok = False
        if d < 0 and not up and aff2 > aff1:
            ok = False
    return ok


def mr_twins(rows):
    """MR3 inert, MR9 negation, MR10 boundary, MR11 clause flip, MR13 attack: relations between a base and its twins."""
    ids = {r["id"]: r for r in rows}
    res = defaultdict(lambda: [0, 0])
    for r in rows:
        k = r["meta"].get("twin_kind")
        b = ids.get(r["meta"].get("twin_of"))
        if not k or b is None:
            continue
        try:
            hb, lb, _ = _solve_row(b)
            ht, lt, _ = _solve_row(r)
        except Exception:
            res[k][1] += 1
            continue
        if k in ("inert", "attack"):
            ok = hb == ht and lb == lt
        elif k == "neg":
            ok = lt == 1 - lb
        elif k == "dneg":
            ok = lt == lb
        elif k in ("boundary", "clause_flip"):
            ok = lt != lb and lt == r["gold"]
        else:
            continue
        res[k][0] += int(ok)
        res[k][1] += 1
    return {k: {"pass": v[0], "n": v[1]} for k, v in res.items()}


def g4(rows, per_sampler_min=1000):
    by = defaultdict(list)
    for r in rows:
        by[r["meta"]["sampler"]].append(r)
    out = {}
    for s, rs in sorted(by.items()):
        st = defaultdict(lambda: [0, 0])
        for r in rs:
            for name, fn in (("MR1_option_shuffle", mr_shuffle), ("MR2_rename", mr_rename),
                             ("MR5_date_shift", mr_dateshift), ("MR8_threshold", mr_threshold)):
                try:
                    v = fn(r)
                except Exception as e:
                    v = False
                if v is None:
                    continue
                st[name][0] += int(bool(v))
                st[name][1] += 1
        tw = mr_twins(rs)
        for k, v in tw.items():
            st[f"twin_{k}"] = [v["pass"], v["n"]]
        lp = [r.get("_loader_perm_ok") for r in rs if r.get("_loader_perm_ok") is not None]
        if lp:
            st["MR1_loader_permutation"] = [sum(lp), len(lp)]
        out[s] = {k: {"pass": v[0], "n": v[1], "rate": round(v[0] / v[1], 4) if v[1] else None} for k, v in st.items()}
        out[s]["rows"] = len(rs)
        out[s]["relations_tested"] = sum(1 for v in st.values() if v[1])
        out[s]["all_relations_100pct"] = all(v[0] == v[1] for v in st.values())
        out[s]["relations_at_100pct_on_ge_1000"] = sum(1 for k, v in st.items() if v[1] >= per_sampler_min and v[0] == v[1])
        out[s]["g4_pass"] = (len(rs) >= per_sampler_min and out[s]["relations_tested"] >= 3
                             and out[s]["all_relations_100pct"])
    return out


def g3_all(rows):
    """G3 re-run from the written files: parse the rendered row, canonical structure hash == meta.structure_hash
    (solver A's, logged at generation), and solver B on the parsed problem == the row's gold."""
    fails = Counter()
    for r in rows:
        try:
            h, lab, _ = _solve_row(r)
        except Exception as e:
            fails["parse_or_solve:" + type(e).__name__] += 1
            continue
        if h != r["meta"]["structure_hash"]:
            fails["hash_differs"] += 1
        if lab != r["gold"]:
            fails["label_differs"] += 1
    return {"rows": len(rows), "fails": dict(fails), "pass_rate": round(1 - sum(fails.values()) / max(1, len(rows)), 6)}


def mr_shuffle(row):
    """MR1 on choice rows: the option list in a random order; solver B on the parsed row picks the same option text.
    CL rows are skipped here: their case references must follow the case order of `state` (parser rule), so a CL
    shuffle is only the display permutation, which MR1_loader_permutation (G15) tests on every row."""
    if row["qtype"] != "choice" or row["meta"]["card_id"].split(".")[-2] == "CL":
        return None
    r2 = copy.deepcopy(row)
    rng = random.Random(int.from_bytes(hashlib.sha256(("F2-mr1:" + row["id"]).encode()).digest()[:8], "big"))
    rng.shuffle(r2["options"])
    h2, l2, _ = _solve_row(r2)
    return l2 == row["gold"]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="")
    a = ap.parse_args(argv)
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", local_files_only=True)
    dio = _dio()
    import train_decoder as td
    rep = {}
    allrows = {}
    for key, fn in FILES.items():
        p = OUT / fn.replace(".jsonl", f"{a.tag}.jsonl")
        rows = read_jsonl(p)
        relp = OUT / fn.replace(".jsonl", f"{a.tag}.relations.jsonl")
        rels = read_jsonl(relp) if relp.exists() else []
        progress(f"gates: {key} {len(rows)} rows")
        rep[key] = {"g15": g15(rows, tok, dio, td), "units": units(rows, rels)}
        progress(f"gates: {key} G3 re-run")
        rep[key]["g3"] = g3_all(rows)
        rep[key]["negcount_recount"] = negcount_recount(rows)
        if key != "mixdev":
            rep[key]["negation"] = negation(rows, rels)
        allrows[key] = rows
    progress("gates: G4 metamorphic")
    rep["g4_train_files"] = g4(allrows["candidates"] + allrows["qc"])
    s5x = TMP / "g4_s5_rows.jsonl"
    s5rows = read_jsonl(s5x) if s5x.exists() else []
    rep["g4_s5_extra_rows_g15"] = g15(s5rows, tok, dio, td)     # loader permutation (MR1) on the extra S5 rows too
    rep["g4_s5"] = g4([r for r in allrows["mixdev"] if r["meta"]["sampler"] == "S5"] + s5rows)
    rep["g4_s5"]["note"] = ("S5 = 460 dev items (400 S5 + 60 sweep) + the extra S5 rows generated for G4 only "
                            "(tmp/g4_s5_rows.jsonl, never an output)")
    rep["g4_sweep_items_s1_s4"] = g4([r for r in allrows["mixdev"] if r["meta"]["sampler"] != "S5"], per_sampler_min=0)
    rep["g4_sweep_items_s1_s4"]["note"] = ("report only: 60 sweep items per training sampler; those generators are "
                                           "G4-tested on the training files (g4_train_files)")
    rep["g18"] = {"option_level_rows": sum(1 for k in allrows for r in allrows[k] if r["meta"].get("option_level") is not None)}
    write_json(OUT / f"gates_report{a.tag}.json", rep)
    progress("gates: done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
