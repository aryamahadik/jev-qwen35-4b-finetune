"""A43 erratum: the pilot-size G6 null on the MAXIMUM excess over chance (PREREG_FINAL.md, "A43 erratum").

Rebuilds the family's 1,000-row pilot in memory exactly as its runner does (the runner's own main() is run with
--dry-run; pilot.build_pilot is wrapped to force G15 off, pilot.g6 is wrapped to capture the infos and stop), then for
each part (yes_no, choice):
  M = max over the part's views and models of (accuracy - chance)     (yes/no: a, c, d x lr, gbt; choice: a, b, c, d x lr, gbt)
and the same M under >= 200 unit-preserving gold permutations. p = share of null M >= observed M.

Unit-preserving permutation (a unit = one build_unit call: base row, its twins, complements, equiv / inv partners):
  yes/no: per unit, the gold labels of its yes/no rows keep their pattern (complements and twins flip together,
          equiv / inv partners agree); only the unit's orientation changes. Units of the same shape
          (n yes/no rows, n rows equal to the first row's gold) exchange their first-row gold by a random shuffle, so the
          yes rate is preserved exactly.
  choice: per unit, the distinct gold option texts are re-assigned by a uniformly random injective map onto texts that
          every row of the unit that carries it lists as an option. Rows that agreed still agree, twins that differed
          still differ, and every gold is a legal option. (The marginal of gold kinds is not held fixed.)
Features and CV folds do not depend on gold, so the fitted feature matrices are built once and only y changes per draw.

  ../../.venv/bin/python -B zed_orch/g6_null_max.py --family T06 --runner families/T06/run_pilot_i2.py --dir pilot_i2
(from c2_build). Without --runner the family is built through PL.open_family like zed_orch/g6_at_size.py.
Writes <family>/<dir>/A43_NULL_MAX.json."""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse
import importlib.util
import itertools
import json
import multiprocessing as mp
import sys
import time
from collections import defaultdict
from pathlib import Path

sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2))

import numpy as np  # noqa: E402
from scipy import sparse  # noqa: E402
from sklearn.feature_extraction import DictVectorizer  # noqa: E402
from sklearn.feature_extraction.text import HashingVectorizer  # noqa: E402
from sklearn.preprocessing import MaxAbsScaler  # noqa: E402

import pilot  # noqa: E402
import pilot_loaders as PL  # noqa: E402

TOL = 1e-9
G = {}                       # fork-shared state: built once in the parent


class _Captured(BaseException):
    pass


# ================================================================================================ build
def rebuild(family: str, runner: str | None, log):
    """(infos, pilot.g6 result) of the family's pilot rows, built as the runner builds them, G15 off."""
    cap = {}
    orig_build, orig_g6 = pilot.build_pilot, pilot.g6

    def build(kit, n_rows=pilot.N_ROWS, **kw):
        kw["run_g15"] = False
        return orig_build(kit, n_rows, **kw)

    def g6_capture(infos):
        cap["infos"] = infos
        cap["g6"] = orig_g6(infos)
        raise _Captured()

    pilot.build_pilot, pilot.g6 = build, g6_capture
    try:
        if runner:
            spec = importlib.util.spec_from_file_location("g6null_runner", Path(runner).resolve())
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            try:
                mod.main(["--dry-run"])
            except _Captured:
                pass
        else:
            try:
                pilot.run_family(family, pilot.N_ROWS, write=False, run_g15=False, log=log)
            except _Captured:
                pass
    finally:
        pilot.build_pilot, pilot.g6 = orig_build, orig_g6
    if "infos" not in cap:
        raise SystemExit("the runner never reached pilot.g6 (no infos captured)")
    return cap["infos"], cap["g6"]


# ================================================================================================ yes/no
def prep_yes_no(infos):
    yn = [i for i in infos if i.row["qtype"] == "noul"]
    y = np.array([int(i.row["gold"]) for i in yn])
    folds = pilot._folds([i.row["meta"]["card_id"] for i in yn])
    views = {}
    for nm, tx in (("a_question", [i.question for i in yn]), ("c_card_without_question", [i.context for i in yn])):
        Xs = pilot._text_matrix(tx)
        views[nm] = (Xs, pilot._dense(Xs))
    views["d_meta"] = pilot._meta_matrices(yn)
    units = defaultdict(list)
    for k, i in enumerate(yn):
        units[i.unit].append(k)
    classes = defaultdict(list)
    for u, idx in units.items():
        r = y[idx[0]]
        s = int(sum(1 for k in idx if y[k] == r))
        classes[(len(idx), s)].append((idx, int(r)))
    return {"y": y, "folds": folds, "views": views, "classes": classes, "n": len(yn), "chance": 0.5,
            "n_units": len(units)}


def yn_cells(P, y):
    out = {}
    for v, (Xs, Xd) in P["views"].items():
        for m, acc in pilot._cv_binary(Xs, Xd, y, P["folds"]).items():
            out[f"{v}/{m}"] = acc
    return out


def yn_permute(P, rng):
    y = P["y"].copy()
    for members in P["classes"].values():
        refs = [r for _, r in members]
        new = rng.permutation(refs)
        for (idx, r), r2 in zip(members, new):
            if r2 != r:
                y[idx] = 1 - y[idx]
    return y


# ================================================================================================ choice
def prep_choice(infos):
    ch = [i for i in infos if i.row["qtype"] == "choice"]
    chance = float(np.mean([1.0 / len(i.row["options"]) for i in ch])) if ch else None
    groups_row = [i.row["meta"]["card_id"] for i in ch]
    views = {}
    for view in ("a_question", "b_options", "c_card_without_question", "d_meta"):
        T, D, _Y, Rw = pilot._pair_rows(ch, view)
        Rw = np.array(Rw)
        Xs = HashingVectorizer(n_features=2 ** 18, analyzer=lambda x: x, alternate_sign=False, norm="l2").transform(T)
        Xd = DictVectorizer(sparse=False).fit_transform(D)
        folds = pilot._folds([groups_row[ri] for ri in Rw])
        lr_mats = []
        for tr, te in folds:
            sca = MaxAbsScaler().fit(Xd[tr])
            lr_mats.append((sparse.hstack([Xs[tr], sparse.csr_matrix(sca.transform(Xd[tr]))]).tocsr(),
                            sparse.hstack([Xs[te], sparse.csr_matrix(sca.transform(Xd[te]))]).tocsr()))
        views[view] = {"Xd": Xd, "Rw": Rw, "folds": folds, "lr": lr_mats}
    opt_text = []
    for ri, i in enumerate(ch):
        opt_text += list(i.row["options"])
    opt_text = np.array(opt_text, dtype=object)
    units = defaultdict(list)
    for ri, i in enumerate(ch):
        units[i.unit].append(ri)
    unit_assign = []
    for u, rows in units.items():
        golds = list(dict.fromkeys(ch[ri].row["gold"] for ri in rows))
        cands = []
        for g in golds:
            c = None
            for ri in rows:
                if ch[ri].row["gold"] == g:
                    o = list(ch[ri].row["options"])
                    c = o if c is None else [x for x in c if x in o]
            cands.append(c)
        feas = [a for a in itertools.islice(itertools.product(*cands), 20000) if len(set(a)) == len(a)]
        unit_assign.append((rows, golds, feas))
    gold0 = [i.row["gold"] for i in ch]
    k_opts = [len(i.row["options"]) for i in ch]
    return {"views": views, "opt_text": opt_text, "unit_assign": unit_assign, "gold0": gold0, "n": len(ch),
            "chance": chance, "k_opts": k_opts, "n_units": len(units)}


def ch_Y(P, gold):
    """pointwise labels in _pair_rows order (rows in order, options in order)"""
    Y = []
    pos = 0
    for ri, g in enumerate(gold):
        k = P["k_opts"][ri]
        Y += [int(t == g) for t in P["opt_text"][pos:pos + k]]
        pos += k
    return np.array(Y)


def ch_cells(P, gold):
    Yall = ch_Y(P, gold)
    out = {}
    for view, V in P["views"].items():
        Y, Rw, Xd, folds = Yall, V["Rw"], V["Xd"], V["folds"]
        for nm in ("lr", "gbt"):
            sc = np.zeros(len(Y))
            for f, (tr, te) in enumerate(folds):
                if len(set(Y[tr])) < 2:
                    continue
                if nm == "lr":
                    Xtr, Xte = V["lr"][f]
                    sc[te] = pilot._lr().fit(Xtr, Y[tr]).predict_proba(Xte)[:, 1]
                else:
                    sc[te] = pilot._gbt().fit(Xd[tr], Y[tr]).predict_proba(Xd[te])[:, 1]
            best = defaultdict(list)
            for s, ri, yy in zip(sc, Rw, Y):
                best[ri].append((s, yy))
            acc = np.zeros(P["n"])
            for ri, lst in best.items():
                m = max(s for s, _ in lst)
                top = [yy for s, yy in lst if s >= m - 1e-12]
                acc[ri] = sum(top) / len(top)
            out[f"{view}/{nm}"] = float(acc.mean())
    return out


def ch_permute(P, rng):
    gold = list(P["gold0"])
    for rows, golds, feas in P["unit_assign"]:
        a = feas[rng.integers(len(feas))]
        m = dict(zip(golds, a))
        for ri in rows:
            gold[ri] = m[P["gold0"][ri]]
    return gold


# ================================================================================================ draws
def one_draw(d):
    rng = np.random.default_rng(G["seed"] * 1_000_003 + d)
    out = {}
    if G.get("yes_no"):
        P = G["yes_no"]
        out["yes_no"] = max(yn_cells(P, yn_permute(P, rng)).values()) - P["chance"]
    if G.get("choice"):
        P = G["choice"]
        out["choice"] = max(ch_cells(P, ch_permute(P, rng)).values()) - P["chance"]
    return d, out


def run_draws(n_draws, workers, tmpdir: Path, log, t0) -> dict:
    """os.fork workers (the sandbox forbids multiprocessing semaphores); each writes its draws to a temp json."""
    files, pids = [], []
    for w in range(workers):
        mine = list(range(w, n_draws, workers))
        f = tmpdir / f"_g6null_w{w}.json"
        files.append(f)
        pid = os.fork()
        if pid == 0:
            code = 0
            try:
                res = {}
                for d in mine:
                    res[d] = one_draw(d)[1]
                    f.write_text(json.dumps(res))
            except BaseException:  # noqa: BLE001
                import traceback
                traceback.print_exc()
                code = 1
            os._exit(code)
        pids.append(pid)
    while pids:
        time.sleep(15)
        done = 0
        for f in files:
            try:
                done += len(json.loads(f.read_text()))
            except (OSError, ValueError):
                pass
        log(f"draws {done}/{n_draws} ({time.time() - t0:.0f}s)")
        for pid in list(pids):
            r, st = os.waitpid(pid, os.WNOHANG)
            if r:
                pids.remove(pid)
                if st:
                    raise SystemExit(f"worker {pid} failed (status {st})")
    out = {}
    for f in files:
        out.update({int(k): v for k, v in json.loads(f.read_text()).items()})
        f.unlink()
    if len(out) != n_draws:
        raise SystemExit(f"only {len(out)} of {n_draws} draws finished")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--family", required=True)
    ap.add_argument("--runner", default=None, help="the family's pilot runner (path); default: PL.open_family")
    ap.add_argument("--dir", required=True, help="pilot dir name under the family folder, e.g. pilot_i2")
    ap.add_argument("--draws", type=int, default=200)
    ap.add_argument("--seed", type=int, default=43)
    ap.add_argument("--workers", type=int, default=max(1, min(8, (os.cpu_count() or 2) - 2)))
    a = ap.parse_args(argv)
    log = lambda m: print(time.strftime("%H:%M:%S"), m, file=sys.stderr, flush=True)  # noqa: E731
    t0 = time.time()
    infos, rep = rebuild(a.family, a.runner, log)
    log(f"built {len(infos)} rows in {time.time() - t0:.0f}s")
    G["seed"] = a.seed
    obs, meta, check = {}, {}, {}
    for part, prep, cells, getgold in (("yes_no", prep_yes_no, yn_cells, lambda P: P["y"]),
                                       ("choice", prep_choice, ch_cells, lambda P: P["gold0"])):
        P = prep(infos)
        if not P["n"] or P["n"] < 20 or P["chance"] is None:
            continue
        G[part] = P
        c = cells(P, getgold(P))
        obs[part] = {"M": max(c.values()) - P["chance"], "cells": c, "chance": P["chance"]}
        meta[part] = {"n": P["n"], "units": P["n_units"], "chance": round(P["chance"], 4)}
        rp = rep[part]
        check[part] = all(abs(round(v, 4) - rp[k.split("/")[0]][k.split("/")[1]]) < 1e-9 for k, v in c.items())
        log(f"{part}: observed M={obs[part]['M']:.4f} (matches pilot.g6: {check[part]})")
    parts = list(obs)
    null = {p: [] for p in parts}
    results = run_draws(a.draws, a.workers, Path(PL.family_dir(a.family), a.dir), log, t0)
    for d in range(a.draws):
        for p in parts:
            null[p].append(results[d][p])
    qs = (0, 5, 25, 50, 75, 90, 95, 99, 100)
    res = {"family": a.family, "dir": a.dir, "statistic": "M = max over views and models of (accuracy - chance)",
           "draws": a.draws, "seed": a.seed, "runner": a.runner, "seed_base": pilot.SEED_BASE,
           "n_rows": len(infos), "g15": "off", "bar_excess": 0.02,
           "permutation": "unit-preserving gold permutation (yes/no: shape-class shuffle of unit orientation; "
                          "choice: injective re-assignment of the unit's gold option texts); see g6_null_max.py",
           "observed_matches_pilot_g6": check, "parts": {}, "seconds": round(time.time() - t0)}
    for p in parts:
        nm = np.array(null[p])
        k = int((nm >= obs[p]["M"] - TOL).sum())
        res["parts"][p] = {**meta[p], "observed_M": round(obs[p]["M"], 4),
                           "observed_cells": {c: round(v, 4) for c, v in obs[p]["cells"].items()},
                           "null_quantiles": {f"q{q}": round(float(np.percentile(nm, q)), 4) for q in qs},
                           "null_mean": round(float(nm.mean()), 4), "null_sd": round(float(nm.std()), 4),
                           "n_null_ge_observed": k, "p": round(k / a.draws, 4), "p_plus1": round((k + 1) / (a.draws + 1), 4),
                           "above_bar": bool(obs[p]["M"] > 0.02 + 1e-12), "null_M": [round(float(x), 4) for x in nm]}
    out = Path(PL.family_dir(a.family), a.dir, "A43_NULL_MAX.json")
    out.write_text(json.dumps(res, indent=1))
    log(f"wrote {out}")
    print(json.dumps({p: {k: v for k, v in res["parts"][p].items() if k in ("observed_M", "p", "above_bar")}
                      for p in parts}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
