#!/usr/bin/env python
"""score_nd.py: aggregates-only scorer for the sealed new-domains suite v2 (sealed side).

Prints AGGREGATES ONLY (overall, part, split, domain id, qtype), with a paired bootstrap over group_id against a
reference preds file. It never prints per-item results, and suppresses any cell with fewer than 30 items.
Every real look is checked against the look table and appended to sealed_nd/looks.jsonl BEFORE results print.
Before ANY look, suite_v2.jsonl's sha256 is checked against suite_v2.sha256 and manifest_v2.json (refused on mismatch),
and every earlier look in the log must carry the same suite sha256.

B3 block (printed after the score table, same look, same preds files; aggregates only): for the yes/no items of each
set of the table (part/split sets and every domain id), the mean P(yes) and the predicted-yes share (p_yes > 0.5 = yes,
== 0.5 counts half) for the candidate and the reference. Items with a missing/unreadable p_yes are left out of B3
(n shown); cells with fewer than 30 such items are suppressed.

Look table (anything else is refused):
  S1  round-1 candidate vs C1, select split only. Closed once any S2/C/J look exists.
  S2  round-2 candidate vs C1, select split only. Needs a prior S1; closed once a C look exists.
  C   finalist vs C1: confirm split of part A (headline) + all of part A per domain + parts B1, B2 and P.
      Only one C look, ever.
  J   Jev read: Jev preds vs the finalist (the C look's candidate file, same sha256), same scope as C.
      Needs a C look with a recorded "ship" verdict; only one J look, ever.
  The C1 reference preds must be byte-identical (same sha256) across all S1/S2/C looks.

Preds format ("gate format": id -> chosen option / p_yes). Any of:
  - JSONL, one object per line: {"id": ..., "choice": <option string or letter>} or {"id": ..., "p_yes": <0..1>}
    (also accepted keys: chosen, pred, prediction, answer, option, label);
  - one JSON object {id: value}, value = option string / letter / p_yes float / "yes"|"no" / {"choice"|"p_yes": ...}.
  Choice: exact option string (case-insensitive fallback) or option letter A, B, ... in the item's option order.
  Yes/no: p_yes > 0.5 = yes, < 0.5 = no, == 0.5 = half credit; "yes"/"no"/true/false/1/0 accepted.
  Missing or unreadable predictions score 0. Each preds file must cover >= 95% of the look's scope, or it is refused.

Usage:
  score_nd.py look --kind S1 --cand cand.jsonl --cand-name r1_ckpt600 --ref c1.jsonl --ref-name C1 [--note ...]
  score_nd.py verdict --verdict ship|no_ship [--note ...]      # records the verdict on the C look
  score_nd.py status                                           # look log summary (no scores)
  score_nd.py --dry-run                                        # fake preds + temp look log; never touches looks.jsonl
"""
import argparse
import hashlib
import json
import os
import random
import re
import shutil
import sys
import time

import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
SUITE = os.path.join(ROOT, "suite_v2.jsonl")
SHAF = os.path.join(ROOT, "suite_v2.sha256")
MANIFEST = os.path.join(ROOT, "manifest_v2.json")
LOOKS = os.path.join(ROOT, "looks.jsonl")
DRYDIR = os.path.join(ROOT, "build", "freeze_v2", "work", "dryrun")
MIN_CELL = 30
MIN_COVERAGE = 0.95
BOOT = 2000
BOOT_SEED = 7
A_DOMAINS = []  # part-A domain ids, read from manifest_v2.json ("part_a_domains") when the suite is loaded
VALUE_KEYS = ("choice", "chosen", "pred", "prediction", "answer", "option", "label")
FORBIDDEN_FLAGS = ("--per-item", "--per_item", "--items", "--item", "--ids", "--show-items", "--dump", "--details")


class Refused(Exception):
    pass


# ------------------------------------------------------------------------------------------------ io
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_suite(suite=SUITE, shaf=SHAF, manifest=MANIFEST):
    """Always verifies the frozen suite_v2 sha256 (suite file vs suite_v2.sha256 vs manifest_v2.json) before use."""
    for p in (suite, shaf, manifest):
        if not os.path.exists(p):
            raise Refused("missing %s: the frozen suite_v2 is incomplete" % os.path.basename(p))
    sha = sha256_file(suite)
    want = open(shaf).read().split()[0]
    man = json.load(open(manifest))
    if sha != want or sha != man.get("suite_sha256"):
        raise Refused("suite_v2.jsonl sha256 does not match suite_v2.sha256 / manifest_v2.json: the frozen suite was changed")
    rows = [json.loads(l) for l in open(suite)]
    A_DOMAINS[:] = list(man["part_a_domains"])
    if sorted({r["meta"]["domain_id"] for r in rows if r["meta"]["part"] == "A"}) != sorted(A_DOMAINS):
        raise Refused("part-A domains in suite_v2.jsonl differ from manifest_v2.json")
    return rows, sha


def read_looks(path):
    if not os.path.exists(path):
        return []
    return [json.loads(l) for l in open(path) if l.strip()]


def append_look(path, rec):
    with open(path, "a") as f:
        f.write(json.dumps(rec) + "\n")
        f.flush()
        os.fsync(f.fileno())


def load_preds(path):
    txt = open(path).read()
    recs = None
    try:
        obj = json.loads(txt)
        if isinstance(obj, dict) and "id" not in obj:
            return {str(k): v for k, v in obj.items()}
        if isinstance(obj, list):
            recs = obj
        elif isinstance(obj, dict):
            recs = [obj]
    except json.JSONDecodeError:
        recs = [json.loads(l) for l in txt.splitlines() if l.strip()]
    out = {}
    for r in recs:
        if isinstance(r, dict) and "id" in r:
            out[str(r["id"])] = r
    return out


def _pick(v, keys):
    if isinstance(v, dict):
        for k in keys:
            if k in v and v[k] is not None:
                return v[k]
        return None
    return v


def resolve_choice(v, options):
    v = _pick(v, VALUE_KEYS)
    if not isinstance(v, str):
        return None
    if v in options:
        return v
    s = v.strip()
    for o in options:
        if o.strip().casefold() == s.casefold():
            return o
    m = re.fullmatch(r"\(?([A-Za-z])\)?[.):]?", s)
    if m:
        i = ord(m.group(1).upper()) - 65
        if 0 <= i < len(options):
            return options[i]
    return None


def resolve_pyes(v):
    if isinstance(v, dict):
        v = v.get("p_yes") if v.get("p_yes") is not None else _pick(v, VALUE_KEYS)
    if isinstance(v, bool):
        return 1.0 if v else 0.0
    if isinstance(v, (int, float)):
        return float(v) if 0.0 <= float(v) <= 1.0 else None
    if isinstance(v, str):
        s = v.strip().lower()
        if s in ("yes", "y", "true"):
            return 1.0
        if s in ("no", "n", "false"):
            return 0.0
        try:
            f = float(s)
            return f if 0.0 <= f <= 1.0 else None
        except ValueError:
            return None
    return None


def score_items(rows, preds):
    """Return per-item score array (kept in memory only), validity mask and Brier array (nan for choice)."""
    sc = np.zeros(len(rows))
    ok = np.zeros(len(rows), dtype=bool)
    br = np.full(len(rows), np.nan)
    for i, r in enumerate(rows):
        v = preds.get(r["id"])
        if r["qtype"] == "choice":
            c = resolve_choice(v, r["options"]) if v is not None else None
            if c is not None:
                ok[i] = True
                sc[i] = 1.0 if c == r["gold"] else 0.0
        else:
            p = resolve_pyes(v) if v is not None else None
            g = int(r["gold"])
            if p is None:
                br[i] = 0.25
            else:
                ok[i] = True
                br[i] = (p - g) ** 2
                sc[i] = 0.5 if p == 0.5 else (1.0 if (p > 0.5) == (g == 1) else 0.0)
    return sc, ok, br


# ------------------------------------------------------------------------------------------------ stats
def _group_arrays(idx, rows, cs, rs):
    groups = {}
    for i in idx:
        groups.setdefault(rows[i]["group_id"], []).append(i)
    keys = sorted(groups)
    gc = np.array([cs[groups[k]].sum() for k in keys])
    gr = np.array([rs[groups[k]].sum() for k in keys])
    gn = np.array([len(groups[k]) for k in keys], dtype=float)
    return gc, gr, gn


def _boot_delta(gc, gr, gn, rng):
    G = len(gn)
    out = np.empty(BOOT)
    step = 250
    for s in range(0, BOOT, step):
        ix = rng.integers(0, G, size=(min(step, BOOT - s), G))
        out[s:s + ix.shape[0]] = (gc[ix].sum(1) - gr[ix].sum(1)) / gn[ix].sum(1)
    return out


def cell(name, idx, rows, cs, rs, cb, rb, seed):
    idx = list(idx)
    n = len(idx)
    if n < MIN_CELL:
        return {"cell": name, "n": n, "suppressed": True}
    gc, gr, gn = _group_arrays(idx, rows, cs, rs)
    rng = np.random.default_rng(seed)
    d = _boot_delta(gc, gr, gn, rng)
    ii = np.array(idx)
    yn = [i for i in idx if rows[i]["qtype"] == "noul"]
    res = {"cell": name, "n": n, "groups": len(gn), "cand": float(cs[ii].mean()), "ref": float(rs[ii].mean()),
           "delta": float(cs[ii].mean() - rs[ii].mean()), "lo": float(np.percentile(d, 2.5)),
           "hi": float(np.percentile(d, 97.5)), "p_pos": float((d > 0).mean())}
    if len(yn) >= MIN_CELL:
        res["brier_cand"] = float(np.nanmean(cb[yn]))
        res["brier_ref"] = float(np.nanmean(rb[yn]))
    return res


def macro_cell(name, dom_idx, rows, cs, rs, seed):
    doms = [d for d, ix in dom_idx.items() if len(ix) >= MIN_CELL]
    if len(doms) < 2:
        return {"cell": name, "n": 0, "suppressed": True}
    deltas, cands, refs = [], [], []
    for k, d in enumerate(doms):
        ix = dom_idx[d]
        gc, gr, gn = _group_arrays(ix, rows, cs, rs)
        deltas.append(_boot_delta(gc, gr, gn, np.random.default_rng(seed + 1000 + k)))
        cands.append(cs[ix].mean())
        refs.append(rs[ix].mean())
    dm = np.mean(np.vstack(deltas), axis=0)
    return {"cell": name, "n": sum(len(dom_idx[d]) for d in doms), "groups": len(doms), "cand": float(np.mean(cands)),
            "ref": float(np.mean(refs)), "delta": float(np.mean(cands) - np.mean(refs)),
            "lo": float(np.percentile(dm, 2.5)), "hi": float(np.percentile(dm, 97.5)), "p_pos": float((dm > 0).mean())}


def build_cells(kind, rows, cs, rs, cb, rb):
    part = lambda r: r["meta"]["part"]  # noqa: E731
    dom = lambda r: r["meta"]["domain_id"]  # noqa: E731
    I = range(len(rows))
    cells = []
    seed = BOOT_SEED

    def add(name, idx):
        nonlocal seed
        seed += 1
        cells.append(cell(name, idx, rows, cs, rs, cb, rb, seed))

    if kind in ("S1", "S2"):
        sel = [i for i in I if rows[i]["split"] == "nd_select"]
        A = [i for i in sel if part(rows[i]) == "A"]
        add("A select (headline, micro)", A)
        cells.append(macro_cell("A select (macro over domains)", {d: [i for i in A if dom(rows[i]) == d] for d in A_DOMAINS},
                                rows, cs, rs, BOOT_SEED + 500))
        for q in ("choice", "noul"):
            add("A select qtype=%s" % q, [i for i in A if rows[i]["qtype"] == q])
        for d in A_DOMAINS:
            add("A select %s" % d, [i for i in A if dom(rows[i]) == d])
        for p in ("P", "B1", "B2"):
            add("%s select" % p, [i for i in sel if part(rows[i]) == p])
        for d in ("P1", "P2", "P3"):
            add("P select %s" % d, [i for i in sel if dom(rows[i]) == d])
        add("all parts select", sel)
    else:  # C, J
        A_all = [i for i in I if part(rows[i]) == "A"]
        A = [i for i in A_all if rows[i]["split"] == "nd_confirm"]
        add("A confirm (headline, micro)", A)
        cells.append(macro_cell("A confirm (macro over domains)", {d: [i for i in A if dom(rows[i]) == d] for d in A_DOMAINS},
                                rows, cs, rs, BOOT_SEED + 500))
        for q in ("choice", "noul"):
            add("A confirm qtype=%s" % q, [i for i in A if rows[i]["qtype"] == q])
        for d in A_DOMAINS:
            add("A confirm %s" % d, [i for i in A if dom(rows[i]) == d])
        add("A all splits (micro)", A_all)
        cells.append(macro_cell("A all splits (macro over domains)",
                                {d: [i for i in A_all if dom(rows[i]) == d] for d in A_DOMAINS}, rows, cs, rs, BOOT_SEED + 600))
        for d in A_DOMAINS:
            add("A all splits %s" % d, [i for i in A_all if dom(rows[i]) == d])
        for p in ("P", "B1", "B2"):
            add("%s all splits" % p, [i for i in I if part(rows[i]) == p])
        for d in ("P1", "P2", "P3"):
            add("P all splits %s" % d, [i for i in I if dom(rows[i]) == d])
        for p in ("P", "B1", "B2"):
            for q in ("choice", "noul"):
                add("%s all splits qtype=%s" % (p, q), [i for i in I if part(rows[i]) == p and rows[i]["qtype"] == q])
    return cells


def b3_sets(kind, rows):
    """The table's part/split sets and every domain id (same scope as the score cells), as (name, idx) pairs."""
    part = lambda r: r["meta"]["part"]  # noqa: E731
    dom = lambda r: r["meta"]["domain_id"]  # noqa: E731
    I = range(len(rows))
    out = []
    if kind in ("S1", "S2"):
        sel = [i for i in I if rows[i]["split"] == "nd_select"]
        A = [i for i in sel if part(rows[i]) == "A"]
        out.append(("A select", A))
        out += [("A select %s" % d, [i for i in A if dom(rows[i]) == d]) for d in A_DOMAINS]
        out += [("%s select" % p, [i for i in sel if part(rows[i]) == p]) for p in ("P", "B1", "B2")]
        out += [("P select %s" % d, [i for i in sel if dom(rows[i]) == d]) for d in ("P1", "P2", "P3")]
        out.append(("all parts select", sel))
    else:
        A_all = [i for i in I if part(rows[i]) == "A"]
        A = [i for i in A_all if rows[i]["split"] == "nd_confirm"]
        out.append(("A confirm", A))
        out += [("A confirm %s" % d, [i for i in A if dom(rows[i]) == d]) for d in A_DOMAINS]
        out.append(("A all splits", A_all))
        out += [("A all splits %s" % d, [i for i in A_all if dom(rows[i]) == d]) for d in A_DOMAINS]
        out += [("%s all splits" % p, [i for i in I if part(rows[i]) == p]) for p in ("P", "B1", "B2")]
        out += [("P all splits %s" % d, [i for i in I if dom(rows[i]) == d]) for d in ("P1", "P2", "P3")]
        out.append(("all parts", list(I)))
    return out


def pyes_array(rows, preds):
    """p_yes per yes/no item (nan for choice items and for missing/unreadable predictions); memory only."""
    p = np.full(len(rows), np.nan)
    for i, r in enumerate(rows):
        if r["qtype"] != "noul":
            continue
        v = preds.get(r["id"])
        x = resolve_pyes(v) if v is not None else None
        if x is not None:
            p[i] = x
    return p


def b3_cells(kind, rows, cp, rp):
    out = []
    for name, idx in b3_sets(kind, rows):
        yn = [i for i in idx if rows[i]["qtype"] == "noul"]
        c = {"cell": name, "n_yesno": len(yn)}
        for tag, p in (("cand", cp), ("ref", rp)):
            v = p[yn] if yn else np.array([])
            v = v[~np.isnan(v)]
            c["n_" + tag] = int(len(v))
            if len(v) >= MIN_CELL:
                c[tag + "_mean_pyes"] = float(v.mean())
                c[tag + "_pred_yes"] = float(np.where(v > 0.5, 1.0, np.where(v == 0.5, 0.5, 0.0)).mean())
        c["suppressed"] = len(yn) < MIN_CELL or "cand_mean_pyes" not in c or "ref_mean_pyes" not in c
        out.append(c)
    return out


def fmt_b3(cells):
    out = ["B3 (yes/no items only; aggregates): mean P(yes) and predicted-yes share, candidate vs reference",
           "%-38s %7s %7s %7s %10s %10s %10s %10s" % ("set", "n_yn", "n_cand", "n_ref", "cand_mP", "cand_yes%",
                                                     "ref_mP", "ref_yes%")]
    for c in cells:
        if c["suppressed"]:
            out.append("%-38s %7d  (suppressed: fewer than %d scored yes/no items)" % (c["cell"], c["n_yesno"], MIN_CELL))
            continue
        out.append("%-38s %7d %7d %7d %10.4f %10.2f %10.4f %10.2f" % (
            c["cell"], c["n_yesno"], c["n_cand"], c["n_ref"], c["cand_mean_pyes"], 100 * c["cand_pred_yes"],
            c["ref_mean_pyes"], 100 * c["ref_pred_yes"]))
    return "\n".join(out)


def scope_idx(kind, rows):
    if kind in ("S1", "S2"):
        return [i for i, r in enumerate(rows) if r["split"] == "nd_select"]
    return list(range(len(rows)))  # C/J: confirm A + all of A + B1 + B2 + P = the whole suite


def fmt_cells(cells):
    out = ["%-38s %6s %6s %7s %7s %8s %18s %7s %s" % ("cell", "n", "groups", "cand%", "ref%", "delta", "95% CI (paired)", "P(d>0)", "brier c/r")]
    for c in cells:
        if c.get("suppressed"):
            out.append("%-38s %6d  (suppressed: fewer than %d items)" % (c["cell"], c["n"], MIN_CELL))
            continue
        b = ""
        if "brier_cand" in c:
            b = "%.4f/%.4f" % (c["brier_cand"], c["brier_ref"])
        out.append("%-38s %6d %6d %7.2f %7.2f %+8.2f %18s %7.3f %s" % (
            c["cell"], c["n"], c["groups"], 100 * c["cand"], 100 * c["ref"], 100 * c["delta"],
            "[%+.2f, %+.2f]" % (100 * c["lo"], 100 * c["hi"]), c["p_pos"], b))
    return "\n".join(out)


# ------------------------------------------------------------------------------------------------ look table
def check_table(kind, looks, cand_sha, ref_sha, ref_name, suite_sha):
    L = [x for x in looks if x.get("type") == "look"]
    kinds = [x["kind"] for x in L]
    V = [x for x in looks if x.get("type") == "verdict"]
    if kind not in ("S1", "S2", "C", "J"):
        raise Refused("look kind %r is not in the look table (S1, S2, C, J)" % kind)
    other = [x["look_id"] for x in L if x.get("suite_sha256") != suite_sha]
    if other:
        raise Refused("the look log holds looks on a different suite (sha256) than suite_v2: looks %s" % other)
    if cand_sha == ref_sha:
        raise Refused("candidate and reference preds are the same file")
    if kind == "S1" and any(k in ("S2", "C", "J") for k in kinds):
        raise Refused("S1 is closed: an S2, C or J look already exists")
    if kind == "S2":
        if "S1" not in kinds:
            raise Refused("S2 needs a prior S1 look")
        if any(k in ("C", "J") for k in kinds):
            raise Refused("S2 is closed: a C look already exists")
    if kind == "C" and "C" in kinds:
        raise Refused("a C look already exists; a second C look is refused")
    if kind in ("S1", "S2", "C"):
        if ref_name != "C1":
            raise Refused("%s looks compare against C1 only (pass --ref-name C1 with C1's preds)" % kind)
        prior = [x for x in L if x["kind"] in ("S1", "S2", "C")]
        if prior and prior[0]["ref_sha256"] != ref_sha:
            raise Refused("the C1 reference preds differ (sha256) from the ones used in look %d" % prior[0]["look_id"])
    if kind == "J":
        if "J" in kinds:
            raise Refused("a J look already exists; a second J look is refused")
        c = [x for x in L if x["kind"] == "C"]
        if not c:
            raise Refused("J needs a C look first")
        v = [x for x in V if x["look_id"] == c[0]["look_id"]]
        if not v or v[-1]["verdict"] != "ship":
            raise Refused("J needs a recorded 'ship' verdict on the C look (score_nd.py verdict --verdict ship)")
        if ref_sha != c[0]["cand_sha256"]:
            raise Refused("J's reference must be the finalist preds scored in the C look (same sha256)")


def run_look(kind, cand, cand_name, ref, ref_name, note=None, looks_path=LOOKS, dry=False, suite_paths=None):
    rows, suite_sha = load_suite(*(suite_paths or ()))  # sha256 verified before anything else
    cand_sha, ref_sha = sha256_file(cand), sha256_file(ref)
    looks = read_looks(looks_path)
    check_table(kind, looks, cand_sha, ref_sha, ref_name, suite_sha)
    cp, rp = load_preds(cand), load_preds(ref)
    scope = scope_idx(kind, rows)
    cs, cok, cb = score_items(rows, cp)
    rs, rok, rb = score_items(rows, rp)
    cov_c = float(cok[scope].mean())
    cov_r = float(rok[scope].mean())
    if cov_c < MIN_COVERAGE or cov_r < MIN_COVERAGE:
        raise Refused("preds coverage too low for this look's scope (cand %.3f, ref %.3f; need >= %.2f)" % (cov_c, cov_r, MIN_COVERAGE))
    cells = build_cells(kind, rows, cs, rs, cb, rb)
    b3 = b3_cells(kind, rows, pyes_array(rows, cp), pyes_array(rows, rp))
    look_id = 1 + max([x["look_id"] for x in looks if x.get("type") == "look"], default=0)
    head = cells[0]
    rec = {"type": "look", "look_id": look_id, "kind": kind, "time": time.strftime("%Y-%m-%dT%H:%M:%S"),
           "cand_name": cand_name, "cand_sha256": cand_sha, "ref_name": ref_name, "ref_sha256": ref_sha,
           "suite_sha256": suite_sha, "scope_items": len(scope), "coverage_cand": round(cov_c, 4),
           "coverage_ref": round(cov_r, 4), "headline": {k: head.get(k) for k in ("cell", "n", "cand", "ref", "delta", "lo", "hi")},
           "note": note, "dry_run": dry}
    append_look(looks_path, rec)  # logged before anything prints
    print("look %d  kind %s  cand %s (%s)  ref %s (%s)  scope %d items  coverage %.3f/%.3f%s" % (
        look_id, kind, cand_name, cand_sha[:12], ref_name, ref_sha[:12], len(scope), cov_c, cov_r,
        "  [DRY RUN, fake preds]" if dry else ""))
    print(fmt_cells(cells))
    print(fmt_b3(b3))
    return look_id


def record_verdict(verdict, note=None, looks_path=LOOKS, look_id=None):
    looks = read_looks(looks_path)
    c = [x for x in looks if x.get("type") == "look" and x["kind"] == "C"]
    if not c:
        raise Refused("no C look to attach a verdict to")
    lid = c[0]["look_id"]
    if look_id is not None and look_id != lid:
        raise Refused("verdicts attach to the C look only (look %d)" % lid)
    if any(x.get("type") == "verdict" and x["look_id"] == lid for x in looks):
        raise Refused("a verdict is already recorded for the C look")
    if verdict not in ("ship", "no_ship"):
        raise Refused("verdict must be ship or no_ship")
    append_look(looks_path, {"type": "verdict", "look_id": lid, "verdict": verdict,
                             "time": time.strftime("%Y-%m-%dT%H:%M:%S"), "note": note})
    print("verdict %s recorded for C look %d" % (verdict, lid))


def status(looks_path=LOOKS):
    looks = read_looks(looks_path)
    if not looks:
        print("no looks recorded")
    for x in looks:
        if x.get("type") == "look":
            print("look %d %s %s cand=%s(%s) ref=%s(%s)" % (x["look_id"], x["kind"], x["time"], x["cand_name"],
                                                           x["cand_sha256"][:12], x["ref_name"], x["ref_sha256"][:12]))
        elif x.get("type") == "verdict":
            print("verdict %s on look %d (%s)" % (x["verdict"], x["look_id"], x["time"]))


# ------------------------------------------------------------------------------------------------ dry run
def _fake_preds(rows, path, acc, seed, coverage=1.0, string_share=0.1):
    rng = random.Random(seed)
    with open(path, "w") as f:
        for r in rows:
            if rng.random() > coverage:
                continue
            if r["qtype"] == "choice":
                o = r["options"]
                pick = r["gold"] if rng.random() < acc else rng.choice(o)
                if rng.random() < string_share:
                    f.write(json.dumps({"id": r["id"], "choice": pick}) + "\n")
                else:
                    f.write(json.dumps({"id": r["id"], "choice": chr(65 + o.index(pick))}) + "\n")
            else:
                right = rng.random() < acc
                p = rng.uniform(0.55, 0.99) if (r["gold"] == 1) == right else rng.uniform(0.01, 0.45)
                f.write(json.dumps({"id": r["id"], "p_yes": round(p, 3)}) + "\n")


def dry_run():
    if os.path.exists(DRYDIR):
        shutil.rmtree(DRYDIR)
    os.makedirs(DRYDIR)
    looks_before = sha256_file(LOOKS) if os.path.exists(LOOKS) else None
    rows, suite_sha = load_suite()
    P = lambda n: os.path.join(DRYDIR, n)  # noqa: E731
    _fake_preds(rows, P("c1.jsonl"), 0.62, 1)
    _fake_preds(rows, P("c1_other.jsonl"), 0.62, 99)
    _fake_preds(rows, P("r1a.jsonl"), 0.66, 2)
    _fake_preds(rows, P("r1b.jsonl"), 0.64, 3)
    _fake_preds(rows, P("r2.jsonl"), 0.68, 4)
    _fake_preds(rows, P("jev.jsonl"), 0.60, 5)
    _fake_preds(rows, P("sparse.jsonl"), 0.70, 6, coverage=0.5)
    lp = P("looks_dryrun.jsonl")
    results = []

    def expect(label, should_pass, fn):
        try:
            fn()
            ok = should_pass
            msg = "ran"
        except Refused as e:
            ok = not should_pass
            msg = "refused: %s" % e
        results.append((label, ok, msg))
        print("  -> [%s] %s: %s" % ("PASS" if ok else "FAIL", label, msg))

    L = lambda k, c, cn, r, rn: (lambda: run_look(k, P(c), cn, P(r), rn, looks_path=lp, dry=True))  # noqa: E731
    print("== DRY RUN (fake preds, temp look log; looks.jsonl untouched) ==")
    expect("S2 before any S1 is refused", False, L("S2", "r2.jsonl", "r2", "c1.jsonl", "C1"))
    expect("unknown look kind is refused", False, L("X", "r1a.jsonl", "r1a", "c1.jsonl", "C1"))
    expect("S1 vs non-C1 reference is refused", False, L("S1", "r1a.jsonl", "r1a", "r1b.jsonl", "r1b"))
    expect("S1 with low-coverage preds is refused", False, L("S1", "sparse.jsonl", "sparse", "c1.jsonl", "C1"))
    expect("S1 round-1 candidate A vs C1", True, L("S1", "r1a.jsonl", "r1a", "c1.jsonl", "C1"))
    expect("S1 round-1 candidate B vs C1", True, L("S1", "r1b.jsonl", "r1b", "c1.jsonl", "C1"))
    expect("S1 with a changed C1 preds file is refused", False, L("S1", "r1a.jsonl", "r1a", "c1_other.jsonl", "C1"))
    expect("S2 round-2 candidate vs C1", True, L("S2", "r2.jsonl", "r2", "c1.jsonl", "C1"))
    expect("S1 after S2 is refused", False, L("S1", "r1a.jsonl", "r1a", "c1.jsonl", "C1"))
    expect("J before any C look is refused", False, L("J", "jev.jsonl", "jev", "r2.jsonl", "r2"))
    expect("verdict before any C look is refused", False, lambda: record_verdict("ship", looks_path=lp))
    expect("C finalist vs C1", True, L("C", "r2.jsonl", "r2", "c1.jsonl", "C1"))
    expect("second C look is refused", False, L("C", "r1a.jsonl", "r1a", "c1.jsonl", "C1"))
    expect("S2 after C is refused", False, L("S2", "r1b.jsonl", "r1b", "c1.jsonl", "C1"))
    expect("J before a ship verdict is refused", False, L("J", "jev.jsonl", "jev", "r2.jsonl", "r2"))
    expect("verdict ship on the C look", True, lambda: record_verdict("ship", looks_path=lp))
    expect("second verdict is refused", False, lambda: record_verdict("no_ship", looks_path=lp))
    expect("J with a reference other than the finalist is refused", False, L("J", "jev.jsonl", "jev", "c1.jsonl", "C1"))
    expect("J Jev vs finalist", True, L("J", "jev.jsonl", "jev", "r2.jsonl", "r2"))
    expect("second J look is refused", False, L("J", "jev.jsonl", "jev", "r2.jsonl", "r2"))
    # suite integrity: a changed suite copy and a look log from another suite are both refused
    with open(SUITE, "rb") as f:
        data = bytearray(f.read())
    data[-2] = ord(" ") if data[-2] != ord(" ") else ord("}")
    with open(P("suite_tampered.jsonl"), "wb") as f:
        f.write(bytes(data))
    expect("S1 on a tampered suite copy is refused", False,
           lambda: run_look("S1", P("r1a.jsonl"), "r1a", P("c1.jsonl"), "C1", looks_path=P("looks_t.jsonl"), dry=True,
                            suite_paths=(P("suite_tampered.jsonl"), SHAF, MANIFEST)))
    with open(P("looks_other.jsonl"), "w") as f:
        f.write(json.dumps({"type": "look", "look_id": 1, "kind": "S1", "suite_sha256": "0" * 64, "cand_sha256": "x",
                            "ref_sha256": "y", "ref_name": "C1"}) + "\n")
    expect("S1 with a look log from a different suite is refused", False,
           lambda: run_look("S1", P("r1a.jsonl"), "r1a", P("c1.jsonl"), "C1", looks_path=P("looks_other.jsonl"), dry=True))
    man = json.load(open(MANIFEST))
    gate = "no layout gate (suite_v2 layout_rules_ok=%s, item_rules_ok=%s); suite sha256 %s verified" % (
        man.get("layout_rules_ok"), man.get("item_rules_ok"), suite_sha[:16])
    n_ok = sum(1 for _, ok, _ in results if ok)
    shutil.rmtree(DRYDIR)
    looks_after = sha256_file(LOOKS) if os.path.exists(LOOKS) else None
    print("== DRY RUN SUMMARY: %d/%d checks behaved as expected; looks.jsonl untouched: %s; gate: %s ==" % (
        n_ok, len(results), looks_before == looks_after, gate))
    return n_ok == len(results) and looks_before == looks_after


# ------------------------------------------------------------------------------------------------ cli
def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    for a in argv:
        if a.split("=")[0] in FORBIDDEN_FLAGS:
            print("REFUSED: score_nd.py never prints per-item results (%s)" % a)
            return 2
    if "--dry-run" in argv:
        return 0 if dry_run() else 1
    ap = argparse.ArgumentParser(description="aggregates-only scorer for the sealed new-domains suite v2")
    sub = ap.add_subparsers(dest="cmd", required=True)
    lk = sub.add_parser("look")
    lk.add_argument("--kind", required=True)
    lk.add_argument("--cand", required=True)
    lk.add_argument("--cand-name", required=True)
    lk.add_argument("--ref", required=True)
    lk.add_argument("--ref-name", required=True)
    lk.add_argument("--note")
    vd = sub.add_parser("verdict")
    vd.add_argument("--verdict", required=True, choices=["ship", "no_ship"])
    vd.add_argument("--look-id", type=int)
    vd.add_argument("--note")
    sub.add_parser("status")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "look":
            run_look(a.kind, a.cand, a.cand_name, a.ref, a.ref_name, note=a.note)
        elif a.cmd == "verdict":
            record_verdict(a.verdict, note=a.note, look_id=a.look_id)
        else:
            status()
    except Refused as e:
        print("REFUSED: %s" % e)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
