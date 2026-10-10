"""A5 item 4 (prereg_drafts/AMENDMENTS_1oct.md section 5; READOUT_DEV.md section 1): the shipped temperatures of ONE
model for its exact OHS-3 primary readout, from its dev reads. CPU only; reads stored dev predictions of the 9 gate
splits; no OHS file is opened. Written so the shipped 4B's T values (4B-E, C1 or C4 = q35_4b_main500k_fix2) come
from one fixed rule, whichever model the gate ships.

  python prep89/t_rule_check.py --model MODEL --noul NAME --choice NAME[+NAME2] [--choice-lt10 NAME]
                                [--choice-single NAME] [--json OUT]

  --model   the model these reads are of (= models.<k>.name in the OHS-3 config). Every read whose preds meta names
            its adapter (load.adapters) must be of this model, else the script stops
  --noul    the single read whose yes/no rows are served (the standard od_gcp predict read)
  --choice  the read whose choice rows are served: for the A5 (a) 2-view readout, the od_gcp predict --tta-choice read
            (identity + exact reversal, averaged); NAME+NAME2 averages two reads in probability space (a proxy only:
            not a served readout, so the OHS-3 config check refuses it)
  --choice-lt10   readout 2view_ge10: choice rows with < 10 options come from this (single) read, rows with >= 10 from
                  --choice (the 2-view read)
  --choice-single the single read's choice rows: also fits T_single.choice (the identity-view secondary file
                  <name>_1v_cal); T_single.noul is the yes/no T above (the same single read)
--json OUT is the config's models.<k>.T_fit_log. It records the reads (preds sha256 per split, adapter and view flags
from their metas), the readout they form, the splits (dev only) and the ship values; ohs3_lib.check_fit_logs
(ohs3_preflight.py, and every real OHS-3 run) checks that the config's T_primary / T_single equal them.

Rule (fixed before any OHS-3 run; T grid 0.50-2.00, step 0.05; fit = lowest NLL of the gold option on POOLED
DEV-SELECT of the 9 splits, first T on ties, as gate_dev.fit_T; evaluated on dev-confirm):
  yes/no : ship the fitted T only if T != 1 AND pooled dev-confirm yes/no Brier improves by >= 0.002 AND no split's
           dev-confirm yes/no Brier worsens by more than 0.003 (A5 item 4 as drafted); else T = 1.00
  choice : ship the fitted T only if T != 1 AND pooled dev-confirm choice NLL improves by >= 0.002 nats per row AND no
           split's dev-confirm choice NLL worsens by more than 0.005 (READOUT_DEV.md, proposed choice rule); else 1.00
Check against READOUT_DEV.md: 4B-E (--noul q35_4b_pxE_fresh --choice q35_4b_pxE_tta) gives fits 0.90 / 1.00 and ships
1.00 / 1.00; the main run (--noul q35_4b_main500k --choice q35_4b_main500k+q35_4b_main500k_perm) gives 0.95 / 1.05 and
ships 1.00 / 1.00.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

LEAN = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(LEAN))
import gate_dev as G  # noqa: E402  (read-only: half, SPLITS, load)

SPLITS = G.SPLITS.split(",")
GRID_A5 = [round(0.50 + 0.05 * i, 2) for i in range(31)]
NOUL_MIN_GAIN, NOUL_MAX_SPLIT_WORSE = 0.002, 0.003
CHOICE_MIN_GAIN, CHOICE_MAX_SPLIT_WORSE = 0.002, 0.005
ROOT = [LEAN]  # data/ and preds_<split>/ live here (--root: a test tree with the same layout)


def set_root(p):
    ROOT[0] = Path(p).resolve()
    G.ROOT = ROOT[0]


def keys_of(r):
    return ["yes", "no"] if r["qtype"] == "noul" else r["options"]


def read(names, sp):
    """{id: probs} of one read, or the probability-space average of several (NAME+NAME2)."""
    ps = []
    for n in names:
        p = G.load(sp, n)
        if p is None:
            sys.exit(f"t_rule_check: preds_{sp}/{n}.jsonl missing")
        ps.append(p)
    if len(ps) == 1:
        return ps[0]
    return {i: {k: sum(float(p[i].get(k, 0.0)) for p in ps) / len(ps) for k in ps[0][i]} for i in ps[0]}


def data_rows(sp):
    with open(ROOT[0] / "data" / f"{sp}.jsonl") as f:
        return [json.loads(l) for l in f]


def primary_raw(sp, noul, choice, lt10=None):
    """{id: probs} of the A5 primary readout BEFORE T on one split: yes/no rows from the noul read, choice rows from the
    choice read (rows with < 10 options from lt10 when given: readout 2view_ge10). Every row must be present."""
    Pn, Pc = read(noul, sp), read(choice, sp)
    Pl = read(lt10, sp) if lt10 else None
    out = {}
    for r in data_rows(sp):
        if r["qtype"] == "noul":
            P = Pn
        else:
            P = Pl if (Pl is not None and len(r["options"]) < 10) else Pc
        if r["id"] not in P:
            sys.exit(f"t_rule_check: a read has no prediction for {sp}/{r['id']}: reads must be complete")
        out[r["id"]] = P[r["id"]]
    return out


def rows_of(qtype, names, lt10=None):
    out = []
    for sp in SPLITS:
        P = read(names, sp)
        Pl = read(lt10, sp) if lt10 else None
        for r in data_rows(sp):
            if r["qtype"] != qtype:
                continue
            src = Pl if (Pl is not None and qtype == "choice" and len(r["options"]) < 10) else P
            if r["id"] not in src:
                sys.exit(f"t_rule_check: {'+'.join(names)} has no prediction for {sp}/{r['id']}: must be complete")
            out.append({"split": sp, "half": G.half(r["group_id"]), "qtype": qtype, "gold": r["gold"],
                        "options": r.get("options"), "p": src[r["id"]]})
    return out


def logmat(rs):
    items = []
    for x in rs:
        ks = keys_of(x)
        gi = (0 if x["gold"] == 1 else 1) if x["qtype"] == "noul" else ks.index(x["gold"])
        items.append(([math.log(max(float(x["p"].get(k, 0.0)), 1e-12)) for k in ks], gi))
    L = np.full((len(items), max(len(l) for l, _ in items)), -np.inf)
    for i, (l, _) in enumerate(items):
        L[i, :len(l)] = l
    return L, np.array([g for _, g in items])


def scaled(L, T):
    Z = L / T
    E = np.exp(Z - Z.max(1, keepdims=True))
    return E / E.sum(1, keepdims=True)


def nll(rs, T):
    L, gi = logmat(rs)
    Q = scaled(L, T)
    return float(-np.log(np.maximum(Q[np.arange(len(gi)), gi], 1e-12)).mean())


def brier(rs, T):
    L, _ = logmat(rs)
    Q = scaled(L, T)
    return float(((Q[:, 0] - np.array([float(x["gold"]) for x in rs])) ** 2).mean())


def fit(rs):
    best, bt = math.inf, 1.0
    for T in GRID_A5:
        v = nll(rs, T)
        if v < best:
            best, bt = v, T
    return bt


def decide(qtype, names, lt10=None):
    rs = rows_of(qtype, names, lt10)
    sel, conf = [x for x in rs if x["half"] == "select"], [x for x in rs if x["half"] == "confirm"]
    T = fit(sel)
    metric = brier if qtype == "noul" else nll
    gain = metric(conf, 1.0) - metric(conf, T)
    per = {}
    for sp in SPLITS:
        c = [x for x in conf if x["split"] == sp]
        if c:
            per[sp] = {"n": len(c), "raw": metric(c, 1.0), "T": metric(c, T)}
    worst = max(v["T"] - v["raw"] for v in per.values())
    gmin, wmax = (NOUL_MIN_GAIN, NOUL_MAX_SPLIT_WORSE) if qtype == "noul" else (CHOICE_MIN_GAIN, CHOICE_MAX_SPLIT_WORSE)
    ship = T if (T != 1.0 and gain >= gmin - 1e-12 and worst <= wmax + 1e-12) else 1.0
    return {"read": "+".join(names) + (f" (<10 options: {'+'.join(lt10)})" if lt10 else ""),
            "metric": "brier" if qtype == "noul" else "nll", "n_select": len(sel),
            "n_confirm": len(conf), "T_fit_select": T, "confirm_raw": metric(conf, 1.0), "confirm_T": metric(conf, T),
            "pooled_gain": gain, "worst_split_worsening": worst, "min_gain": gmin, "max_split_worsening": wmax,
            "per_split": per, "ship_T": ship}


# ------------------------------------------------------------------ provenance (what the OHS-3 config check reads)

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def read_info(name):
    """One stored dev read: sha256 of its preds file per split, and from its metas (od_gcp predict writes them) the
    adapter (basename of load.adapters; None when an old meta does not record it) and its views:
      view (choice rows): "2view" (tta or tta_choice), "single" (no TTA), "permuted" (perm_seed), "unknown" (no flags);
      noul_view (yes/no rows): "single" (tta and tta_noul both false), "swapped" (tta or tta_noul: letters swapped and
      averaged, not the served yes/no read), "permuted", "unknown".
    A value that differs between splits is "mixed"."""
    sha, ads, kinds, nkinds = {}, set(), set(), set()
    for sp in SPLITS:
        f = ROOT[0] / f"preds_{sp}" / f"{name}.jsonl"
        if not f.exists():
            sys.exit(f"t_rule_check: preds_{sp}/{name}.jsonl missing")
        sha[sp] = sha256_file(f)
        mf = f.with_name(f"{name}.meta.json")
        m = json.loads(mf.read_text()) if mf.exists() else {}
        a = (m.get("load") or {}).get("adapters")
        ads.add(None if not a else "+".join(Path(x).name for x in a))
        tta, tc, tn = m.get("tta"), m.get("tta_choice"), m.get("tta_noul")
        if m.get("perm_seed") is not None:
            kinds.add("permuted")
            nkinds.add("permuted")
            continue
        kinds.add("2view" if (tta is True or tc is True) else "single" if (tta is False and tc is False) else "unknown")
        nkinds.add("swapped" if (tta is True or tn is True) else "single" if (tta is False and tn is False)
                   else "unknown")
    one = lambda s: s.pop() if len(s) == 1 else "mixed"  # noqa: E731
    return {"sha256": sha, "adapter": one(ads), "view": one(kinds), "noul_view": one(nkinds)}


def choice_readout(choice, lt10, infos):
    """The A5 readout the choice reads form: 2view / single / 2view_ge10, "proxy" (a NAME+NAME2 average) or "unknown"."""
    if len(choice) > 1:
        return "proxy"
    v = infos[choice[0]]["view"]
    if lt10:
        return "2view_ge10" if v == "2view" and len(lt10) == 1 and infos[lt10[0]]["view"] == "single" else (
            "proxy" if len(lt10) > 1 else "unknown")
    return v if v in ("2view", "single") else "unknown"


def provenance(a, noul, choice, lt10, single):
    names = sorted(set(noul + choice + (lt10 or []) + (single or [])))
    infos = {n: read_info(n) for n in names}
    if a.model:
        bad = {n: i["adapter"] for n, i in infos.items() if i["adapter"] not in (None, a.model)}
        if bad:
            sys.exit(f"t_rule_check: reads of another adapter than --model {a.model}: {bad}")
    return {"model": a.model, "reads": infos, "choice_readout": choice_readout(choice, lt10, infos),
            "noul_read": "+".join(noul), "noul_read_view": infos[noul[0]]["noul_view"] if len(noul) == 1 else "proxy",
            "choice_single_read": "+".join(single) if single else None,
            "choice_single_view": (infos[single[0]]["view"] if len(single) == 1 else "proxy") if single else None,
            "splits": SPLITS, "dev_only": all(not s.startswith("ohs") for s in SPLITS),
            "tool": {"path": "prep89/t_rule_check.py", "sha256": sha256_file(Path(__file__))}}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--model", default=None, help="the model the reads are of (the config's models.<k>.name)")
    ap.add_argument("--noul", required=True)
    ap.add_argument("--choice", required=True)
    ap.add_argument("--choice-lt10", default=None, help="2view_ge10: the single read for choice rows with < 10 options")
    ap.add_argument("--choice-single", default=None, help="the single read's choice rows: fits T_single.choice too")
    ap.add_argument("--root", default=None, help="a tree with data/ and preds_<split>/ (tests); default lean/")
    ap.add_argument("--json", default=None)
    a = ap.parse_args(argv)
    if a.root:
        set_root(a.root)
    noul, choice = a.noul.split("+"), a.choice.split("+")
    lt10 = a.choice_lt10.split("+") if a.choice_lt10 else None
    single = a.choice_single.split("+") if a.choice_single else None
    res = {"rule": "A5 item 4 (yes/no) + READOUT_DEV.md choice rule; grid 0.50-2.00; fit on pooled dev-select",
           "noul": decide("noul", noul), "choice": decide("choice", choice, lt10)}
    if single:
        res["choice_single"] = decide("choice", single)
    for qt, d in (("yes/no", res["noul"]), ("choice", res["choice"])) + (
            (("choice (single read)", res["choice_single"]),) if single else ()):
        print(f"{qt:6s} read {d['read']}: T(select) {d['T_fit_select']:.2f}; dev-confirm {d['metric']} "
              f"{d['confirm_raw']:.4f} -> {d['confirm_T']:.4f} (gain {d['pooled_gain']:+.4f}, needs >= {d['min_gain']}); "
              f"worst split {d['worst_split_worsening']:+.4f} (<= {d['max_split_worsening']}) -> ship T = {d['ship_T']:.2f}")
    res["ship"] = {"T_noul": res["noul"]["ship_T"], "T_choice": res["choice"]["ship_T"]}
    if single:
        res["ship"]["T_choice_single"] = res["choice_single"]["ship_T"]
    res["args"] = {"model": a.model, "noul": a.noul, "choice": a.choice, "choice_lt10": a.choice_lt10,
                   "choice_single": a.choice_single}
    res["provenance"] = provenance(a, noul, choice, lt10, single)
    print(f"SHIP: T_noul = {res['ship']['T_noul']:.2f}, T_choice = {res['ship']['T_choice']:.2f}"
          + (f", T_choice_single = {res['ship']['T_choice_single']:.2f}" if single else "")
          + f"  (model {a.model}; choice readout {res['provenance']['choice_readout']})")
    if a.json:
        Path(a.json).write_text(json.dumps(res, indent=1) + "\n")
    return res


if __name__ == "__main__":
    main()
