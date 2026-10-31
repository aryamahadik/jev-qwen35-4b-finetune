"""COMMIT output gates on out/{candidates_r1, qc_sample, mixdev_S5}: G2/G3 (solver B per type on the rendered row vs
gold, round-trip parse and leak checks), G4 (metamorphic relations through solver B, >= 3 per type, 100% on
>= 1,000 rows), G15 (train_decoder.check_rows, fmt1 loader_check under 3 random option orders, units <= 3 rows,
counted length <= 1,999 and real-tokenizer length <= 7,900 with instructions counted twice), G18 (ordinal rows),
negcount checks and quotas, mixer bookkeeping checks (S5 disjointness, format_style). Writes qc/gates_<split>.json
and prints a short summary. Usage: run_gates.py [cand qc dev]"""
from __future__ import annotations

import collections
import json
import random
import re
import sys
from decimal import ROUND_HALF_EVEN, Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "gen"))
import common as C  # noqa: E402
import core as K  # noqa: E402
import frame as FR  # noqa: E402
import gate as G  # noqa: E402
import match as M  # noqa: E402
import render as RD  # noqa: E402
import route as R  # noqa: E402
import score as S  # noqa: E402
import texts as T  # noqa: E402
import triage as TR  # noqa: E402

sys.path.insert(0, str(C.CSRC / "common"))
import negcount  # noqa: E402
from fmt1 import card as fcard  # noqa: E402

FILES = {"cand": "candidates_r1", "qc": "qc_sample", "dev": "mixdev_S5"}
NEG_FRAME = re.compile(r"(?i)\b(is it not true|isn't it|is it false that)\b")


def read(path):
    p = C.OUT / path
    return [json.loads(l) for l in open(p)] if p.exists() else []


def typ_of(r):
    return r["source"][len("commit_"):]


_CARDS = None


def cards():
    global _CARDS
    if _CARDS is None:
        d = json.load(open(C.OUT / "cards.json"))
        _CARDS = {c["card_id"]: c for part in d.values() for lst in part.values() for c in lst}
    return _CARDS


def solve_B(r, side):
    t = typ_of(r)
    rec = FR.rec(r["meta"]["text_source"]["record_id"])
    if t == "route":
        return R.B_solve(r, rec, cards()[r["meta"]["card_id"]]["areas"])
    if t == "triage":
        return TR.B_solve(r, rec, side["option_types"])
    if t == "score":
        return S.B_solve(r)
    if t == "gate":
        return G.B_solve_inverted(r) if r["qtype"] == "choice" else G.B_solve(r, rec)
    return M.B_solve_inverted(r) if r["qtype"] == "choice" else M.B_solve(r)


def safe_B(r, side):
    try:
        return solve_B(r, side)
    except Exception as e:  # noqa: BLE001
        return "ERR:" + type(e).__name__ + ":" + str(e)[:60]


# ---------------------------------------------------------------------------------------------------------------
# metamorphic transforms (G4)

FENCE = re.compile(r"```diff\n(.*?)\n```", re.S)


def file_order_shuffle(r, seed):
    st = r["state"]
    m = FENCE.search(st)
    if not m:
        return None
    lines = m.group(1).split("\n")
    starts = [i for i, ln in enumerate(lines) if ln == K.ROUTE_SEP or
              (ln.startswith("--- ") and i + 1 < len(lines) and lines[i + 1].startswith("+++ "))]
    if len(starts) < 2 or starts[0] != 0:
        return None
    blocks = [lines[a:b] for a, b in zip(starts, starts[1:] + [len(lines)])]
    rng = random.Random(seed)
    order = list(range(len(blocks)))
    while order == sorted(order):
        rng.shuffle(order)
    body = "\n".join(ln for j in order for ln in blocks[j])
    return {**r, "state": st[:m.start(1)] + body + st[m.end(1):]}


def option_shuffle(r, seed):
    if r["qtype"] != "choice" or len(r["options"]) < 2:
        return None
    o = list(r["options"])
    rng = random.Random(seed)
    while o == r["options"]:
        rng.shuffle(o)
    return {**r, "options": o}


INERT = ["This card is kept in the team handbook.", "The team reviews this card once a year.",
         "Questions about this card go to the maintainers."]
CLASS_LINE = re.compile(r"(?:^|\W)[A-Za-z][A-Za-z ]*? files: .+\.$")


def inert_sentence(r, seed):
    """Inert sentence MR: one neutral line appended to the card; the answer must not move."""
    rng = random.Random(seed)
    if r.get("card"):
        return {**r, "card": r["card"] + "\n" + rng.choice(INERT)}
    return {**r, "instructions": rng.choice(INERT) + "\n" + r["instructions"]}


def class_reorder(r, seed):
    """Rule reorder MR (gate): the class-list lines of the card swap places; the answer must not move."""
    for fld in ("card", "instructions"):
        lines = (r[fld] or "").split("\n")
        idx = [i for i, ln in enumerate(lines) if CLASS_LINE.search(ln) and "Hold rule" not in ln and "'" not in ln]
        if len(idx) >= 2:
            vals = [lines[i] for i in idx]
            rng = random.Random(seed)
            perm = list(vals)
            while perm == vals:
                rng.shuffle(perm)
            for i, v in zip(idx, perm):
                lines[i] = v
            return {**r, fld: "\n".join(lines)}
    return None


def case_plain(r):
    """Match: upper-case whole plain words of the shown message (never a code-shaped word); asserts the code-name
    set is unchanged."""
    st = r["state"]
    m = FENCE.search(st)
    pre = st[:m.start()]
    before = sorted(w.strip("`").lower() for w in M.B_words(pre) if M.B_code_shaped(w))

    def up(mm):
        w = mm.group(0)
        return w.upper() if w.isalpha() and w.islower() and len(w) >= 3 else w
    pre2 = re.sub(r"(?<![\w`/.])[A-Za-z]+(?![\w`/.])", up, pre)
    after = sorted(w.strip("`").lower() for w in M.B_words(pre2) if M.B_code_shaped(w))
    if before != after:
        return "names_changed"
    return {**r, "state": pre2 + st[m.start():]}


def g4(rows, sides, rels, rep):
    by = {r["id"]: r for r in rows}
    gold_ok = {}
    tested = collections.defaultdict(set)
    res = collections.defaultdict(collections.Counter)

    def chk(t, mr, rid, got, exp):
        tested[t].add(rid)
        res[t][mr + (":pass" if got == exp else ":fail")] += 1

    for r in rows:
        t = typ_of(r)
        s = sides[r["id"]]
        if r["meta"]["input_view"] == "message_diff" and t in ("route", "gate", "match", "score") and \
                not (t in ("gate", "match") and r["qtype"] == "choice"):
            x = file_order_shuffle(r, "g4fo" + r["id"])
            if x is not None:
                chk(t, "file_order", r["id"], safe_B(x, s), r["gold"])
        x = option_shuffle(r, "g4os" + r["id"])
        if x is not None:
            chk(t, "option_shuffle", r["id"], safe_B(x, s), r["gold"])
        chk(t, "inert_sentence", r["id"], safe_B(inert_sentence(r, "g4in" + r["id"]), s), r["gold"])
        if t == "gate":
            x = class_reorder(r, "g4cr" + r["id"])
            if x is not None:
                chk(t, "class_reorder", r["id"], safe_B(x, s), r["gold"])
        if t == "match" and r["qtype"] == "noul":
            x = case_plain(r)
            if x == "names_changed":
                res[t]["case_plain:skipped_names_changed"] += 1
            else:
                chk(t, "case_plain", r["id"], safe_B(x, s), r["gold"])
        tk = r["meta"].get("twin_kind")
        if tk in ("swapped_name", "class_edit", "threshold") or (t == "score" and r["meta"].get("twin_of")):
            base = by.get(r["meta"]["twin_of"])
            if base is not None:
                name = {"swapped_name": "definition_swap", "class_edit": "class_edit",
                        "threshold": "threshold_edit"}.get(tk, "cut_edit")
                chk(t, name, r["id"], (safe_B(r, s), r["gold"] != base["gold"]), (r["gold"], True))
    for rel in rels:
        a, b = by.get(rel["a"]), by.get(rel["b"])
        if a is None or b is None:
            continue
        t = typ_of(a)
        ga, gb = safe_B(a, sides[a["id"]]), safe_B(b, sides[b["id"]])
        kind = rel["type"]
        if kind == "complement":
            chk(t, "polarity_complement", b["id"], (ga, gb), (a["gold"], 1 - a["gold"]))
        elif kind == "equiv":
            chk(t, "double_negation_equiv", b["id"], (ga, gb), (a["gold"], a["gold"]))
        elif kind == "inv":
            chk(t, "attack_inv", b["id"], (ga, gb), (a["gold"], a["gold"]))
        elif kind == "flip":
            chk(t, "message_swap", b["id"], (ga, gb, a["gold"] != b["gold"]), (a["gold"], b["gold"], True))
        elif kind == "swap":
            chk(t, "definition_swap_rel", b["id"], (gb, a["gold"] != b["gold"]), (b["gold"], True))
    out = {}
    for t in sorted(res):
        mrs = sorted({k.rsplit(":", 1)[0] for k in res[t] if k.endswith((":pass", ":fail"))})
        fails = sum(v for k, v in res[t].items() if k.endswith(":fail"))
        out[t] = {"mrs": mrs, "n_mrs": len(mrs), "rows_tested": len(tested[t]), "fails": fails,
                  "detail": dict(res[t]),
                  "pass": fails == 0 and len(mrs) >= 3 and len(tested[t]) >= 1000}
    rep["G4"] = out


# ---------------------------------------------------------------------------------------------------------------

def e_target_level(r, eps):
    ol = r["meta"]["option_level"]
    k = len(r["options"])
    e = sum(Decimal(ol[o]) * (Decimal(1 - eps) * (1 if o == r["gold"] else 0) + Decimal(eps) / k)
            for o in r["options"])
    return int(e.quantize(Decimal(1), rounding=ROUND_HALF_EVEN))


def question_of(r, side):
    qid = side["qid"]
    for kind, lst in T.Q.items():
        for q in lst:
            if q[0] == qid:
                txt = q[1]
                if "{x}" in txt:
                    txt = txt.format(x=side.get("asked_option"))
                return txt, q[2]
    return None, None


_WT = None


def _wtext():
    global _WT
    if _WT is None:
        _WT = {w["id"]: w["text"] for t in ("route", "triage", "score", "gate", "match")
               for f in ("yn", "choice") for w in FR.wordings(t, f)}
    return _WT


def run(split, rep_all, do_g4=True):
    name = FILES[split]
    rows = read(f"{name}.jsonl")
    sides = {s["id"]: s for s in read(f"{name}.sidecar.jsonl")}
    rels = read(f"{name}.rel.jsonl")
    rep = {"rows": len(rows), "by_type": dict(collections.Counter(typ_of(r) for r in rows)),
           "by_type_view": dict(collections.Counter(f"{typ_of(r)}:{r['meta']['input_view']}:{r['qtype']}"
                                                    for r in rows))}
    fail = collections.Counter()
    # G2 / G3
    g2 = collections.Counter()
    for r in rows:
        s = sides.get(r["id"])
        if s is None:
            fail["G1_no_sidecar"] += 1
            continue
        b = safe_B(r, s)
        g2[typ_of(r) + (":ok" if b == r["gold"] else ":mismatch")] += 1
        if b != r["gold"]:
            fail["G2G3_mismatch:" + typ_of(r) + ":" + (b[:40] if isinstance(b, str) and b.startswith("ERR")
                                                         else "value")] += 1
    rep["G2G3"] = dict(g2)
    # negcount per row + quotas
    yn = [r for r in rows if r["qtype"] == "noul"]
    k1 = k2t = 0
    for r in yn:
        s = sides[r["id"]]
        q, kq = question_of(r, s)
        if q is None or q not in r["instructions"]:
            fail["question_missing"] += 1
            continue
        if NEG_FRAME.search(q):
            fail["negated_frame"] += 1
        wt = _wtext().get(r["meta"].get("wording_id"), "")
        if "?" in wt and not FR.CANON_QID.match(s.get("qid") or ""):
            fail["polar_wording_on_negated_or_inverted_question"] += 1
        ks = negcount.k_syn(q)
        if ks != s.get("k_syn", 0) or ks != kq:
            fail["negcount_mismatch"] += 1
        if ks >= 1:
            k1 += 1
        if ks >= 2 and r["meta"].get("twin_of"):
            k2t += 1
    rep["negation"] = {"yn_rows": len(yn), "k_syn>=1": k1, "share_k1": round(k1 / max(1, len(yn)), 4),
                       "k_syn>=2_with_aff_twin": k2t, "share_k2": round(k2t / max(1, len(yn)), 4),
                       "quota_pass": (k1 / max(1, len(yn)) >= 0.10 and k2t / max(1, len(yn)) >= 0.02)}
    # G15
    td = fcard._td()
    try:
        td.check_rows(rows)
        rep["check_rows"] = "ok"
    except Exception as e:  # noqa: BLE001
        rep["check_rows"] = "FAIL " + str(e)[:200]
        fail["G15_check_rows"] += 1
    tok = RD.Tok()
    lens = collections.defaultdict(list)
    for r in rows:
        rng = random.Random(C.sha256("g15" + r["id"]))
        n = len(r["options"]) if r["qtype"] == "choice" else 2
        ok = True
        for _ in range(3):
            perm = list(range(n))
            rng.shuffle(perm)
            res = fcard.loader_check(r, perm=perm, check_rows=False)
            ok &= bool(res["ok"])
        if not ok:
            fail["G15_loader"] += 1
        c = tok.count(r, perm)
        lens[typ_of(r)].append(c)
        if c > 1999:
            fail["len>1999"] += 1
        if c > 7900:
            fail["len>7900"] += 1
    rep["counted_len"] = {t: {"mean": round(sum(v) / len(v)), "median": sorted(v)[len(v) // 2], "max": max(v)}
                          for t, v in lens.items()}
    units = collections.Counter(r["call_id"] for r in rows)
    rep["max_unit_rows"] = max(units.values()) if units else 0
    if rep["max_unit_rows"] > 3:
        fail["unit>3"] += 1
    # G18
    n_ord = 0
    for r in rows:
        ol = r["meta"].get("option_level")
        if ol is None:
            continue
        n_ord += 1
        why = td.ordinal_problem(r)
        if why:
            fail["G18_ordinal_problem"] += 1
            continue
        for eps in (0.05, 0.08):
            if e_target_level(r, eps) != ol[r["gold"]]:
                fail["G18_E_target"] += 1
    rep["G18"] = {"ordinal_rows": n_ord, "non_score_ordinal": sum(1 for r in rows if r["meta"].get("option_level")
                                                                  is not None and typ_of(r) != "score")}
    if rep["G18"]["non_score_ordinal"]:
        fail["G18_non_score"] += 1
    # meta / bookkeeping
    for r in rows:
        if not r["meta"].get("format_style"):
            fail["no_format_style"] += 1
        if split == "dev" and r["meta"]["sampler"] != "S5":
            fail["dev_not_S5"] += 1
        if split != "dev" and r["meta"]["sampler"] == "S5":
            fail["S5_in_training"] += 1
    if do_g4 and split != "dev":
        g4(rows, sides, rels, rep)
        for t, v in rep["G4"].items():
            if not v["pass"]:
                fail["G4_" + t] += 1
    rep["relations"] = {"n": len(rels), "by_type": dict(collections.Counter(x["type"] for x in rels))}
    rep["fail"] = dict(fail)
    rep["pass"] = not fail
    rep_all[split] = rep
    with open(HERE / f"gates_{split}.json", "w") as f:
        json.dump(rep, f, indent=1)
    print(split, "rows", len(rows), "pass", rep["pass"], "fail", dict(fail), flush=True)
    return rows


def cross(rep_all):
    """Mixer rule 4 and A52: training rows share no group_id, normalised state, structure_hash or domain_pack with
    mixdev; candidates and qc_sample share no commit."""
    cand, qc, dev = (read(f"{FILES[s]}.jsonl") for s in ("cand", "qc", "dev"))
    norm = lambda s: re.sub(r"\s+", " ", s).strip().lower()
    out = {}
    for nm, tr in (("cand", cand), ("qc", qc)):
        for key, f in (("group_id", lambda r: r["group_id"]), ("state", lambda r: norm(r["state"])),
                       ("structure_hash", lambda r: r["meta"]["structure_hash"]),
                       ("domain_pack", lambda r: r["meta"]["domain_pack"])):
            out[f"{nm}_vs_dev_{key}"] = len({f(r) for r in tr} & {f(r) for r in dev})
    rc = {r["meta"]["text_source"]["record_id"] for r in cand}
    rq = {r["meta"]["text_source"]["record_id"] for r in qc}
    out["cand_qc_shared_commits"] = len(rc & rq)
    out["pass"] = all(v == 0 for v in out.values())
    rep_all["cross"] = out
    print("cross", out, flush=True)


if __name__ == "__main__":
    splits = sys.argv[1:] or ["cand", "qc", "dev"]
    FR.index()
    rep_all = {}
    for sp in splits:
        run(sp, rep_all)
    if len(splits) == 3:
        cross(rep_all)
    p = HERE / "gates_summary.json"
    old = json.load(open(p)) if p.exists() else {}
    old.update(rep_all)
    with open(p, "w") as f:
        json.dump(old, f, indent=1)
    print("GATES_DONE", flush=True)
