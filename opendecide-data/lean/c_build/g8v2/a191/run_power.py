"""A19.1 (b) power check: do the families' OWN G6 / G7 scripts FAIL planted yes/no cues?

For one family (F2 or F5): build planted copies of the G6/G7 inputs (out/qc_sample.jsonl, out/candidates_r1.jsonl)
with the yes/no cues of c_src/common/g8_aflite.py's power code (same TOKEN, THE_RX, SENT_RX, plant_uniforms, gold-yes
rows only, labels never change):
  token  0.20  ' [ref]' appended to the end of the state (end of the row text)
  swap   0.20  first 'the' -> 'this' in the question (first '?'-sentence of `instructions` that has 'the')
  repeat 0.40  last state sentence repeated (length / redundancy cue, no new words)
5 plant seeds each (0-4, as g8_aflite N_PLANT_SEEDS), plus one unplanted control. A row is marked when it is gold-yes,
can carry the cue and u < strength (u = g8_aflite.plant_uniforms over the file's yes/no rows in file order).
Each variant gets a work dir with out/ (planted jsonl; sidecars symlinked to the family's read-only files) and qc/
(g6.py, g7.py byte-identical copies; qc_lib.py with ONLY the OUT / QC / TMP path constants redirected). The family's
own commands then run there: g6.py qc_sample, g7.py qc_sample, g7.py candidates_r1. Result JSONs + logs are copied
to --res. Never writes inside c_src/.
Usage: run_power.py --fam F2 --work /tmp/a191work --res <dir> [--jobs 8] [--variants control,token_s0] [--build-only]
"""
import argparse, json, os, re, shutil, subprocess, sys, time, hashlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.dont_write_bytecode = True
LEAN = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
sys.path.insert(0, str(LEAN / "c_src/common"))
import g8_aflite as G8  # noqa: E402  (cue definitions only)

CUES = (("token", 0.20), ("swap", 0.20), ("repeat", 0.40))
SEEDS = range(G8.N_PLANT_SEEDS)
NAMES = ("qc_sample", "candidates_r1")
T0 = time.time()


def log(m):
    print(f"[{time.time() - T0:7.1f}s] {m}", flush=True)


def plant_row(r, cue):
    """-> planted copy of row r, or None if r cannot carry the cue. Mirrors g8_aflite.cue_views on raw fields."""
    r = json.loads(json.dumps(r))
    st = r["state"]
    if cue == "token":
        r["state"] = st.rstrip() + " " + G8.TOKEN
        return r
    if cue == "repeat":
        sn = " ".join(st.split()); sents = [x for x in G8.SENT_RX.split(sn) if x.strip()]
        if not sents:
            return None
        r["state"] = st.rstrip() + " " + sents[-1]
        return r
    if cue == "swap":
        ins = r["instructions"]
        for line in ins.strip().split("\n"):
            for s in G8.SENT_RX.split(line):
                if "?" in s and G8.THE_RX.search(s):
                    i = ins.find(s); assert i >= 0
                    s2 = G8.THE_RX.sub("this", s, count=1)
                    r["instructions"] = ins[:i] + s2 + ins[i + len(s):]
                    return r
        return None
    raise ValueError(cue)


def build_out(fam, odir, cue, seed, strength):
    """Write planted copies of both files into odir; -> plant record."""
    src = LEAN / f"c_src/{fam}/out"; odir.mkdir(parents=True, exist_ok=True); rec = {}
    for nm in NAMES:
        lines = open(src / f"{nm}.jsonl").read().splitlines()
        rows = [json.loads(l) for l in lines]
        yn = [i for i, r in enumerate(rows) if r["qtype"] == "noul"]
        out = list(lines); marked = []; elig = 0
        if cue is not None:
            u = G8.plant_uniforms(len(yn), "yes_no", cue, seed)
            for a, i in enumerate(yn):
                r = rows[i]
                if int(r["gold"]) != 1:
                    continue
                pr = plant_row(r, cue)
                if pr is None:
                    continue
                elig += 1
                if u[a] < strength:
                    out[i] = json.dumps(pr, ensure_ascii=False); marked.append(r["id"])
        (odir / f"{nm}.jsonl").write_text("\n".join(out) + "\n")
        for p in src.glob(f"{nm}.*"):  # read-only sidecars (F5 polarity, relations, ...)
            if p.name != f"{nm}.jsonl" and not (odir / p.name).exists():
                os.symlink(p, odir / p.name)
        rec[nm] = {"n_rows": len(rows), "n_yes_no": len(yn), "n_gold_yes": sum(int(rows[i]["gold"]) for i in yn),
                   "n_eligible": elig, "n_marked": len(marked),
                   "marked_ids_sha1": hashlib.sha1("\n".join(marked).encode()).hexdigest(),
                   "in_sha256": hashlib.sha256((src / f"{nm}.jsonl").read_bytes()).hexdigest()}
    return rec


def build_qc(fam, wdir):
    q = LEAN / f"c_src/{fam}/qc"; qd = wdir / "qc"; qd.mkdir(parents=True, exist_ok=True)
    for f in ("g6.py", "g7.py"):
        shutil.copyfile(q / f, qd / f)
    lib = (q / "qc_lib.py").read_text(); rep = {
        f'OUT = {fam} / "out"': f'OUT = Path("{wdir}/out")',
        f'QC = {fam} / "qc"': f'QC = Path("{wdir}/qc")',
        f'TMP = {fam} / "tmp/chk"': f'TMP = Path("{wdir}/tmp/chk")'}
    n = 0
    for a, b in rep.items():
        if a in lib:
            lib = lib.replace(a, b); n += 1
    assert n == (3 if fam == "F5" else 2), (fam, n)
    (qd / "qc_lib.py").write_text(lib)


def variants():
    v = [("control", None, None, 0.0)]
    for cue, s in CUES:
        for seed in SEEDS:
            v.append((f"{cue}_s{seed}", cue, seed, s))
    return v


def run_task(fam, wroot, res, vname, script, arg):
    wd = wroot / vname; rd = res / vname; rd.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1",
               MKL_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")
    tag = f"{script[:-3]}_{arg}"; t = time.time()
    with open(rd / f"{tag}.log", "w") as lf:
        rc = subprocess.call([sys.executable, script, arg], cwd=wd / "qc", stdout=lf, stderr=subprocess.STDOUT, env=env)
    outs = {"g6.py": ["g6.json", f"g6_{arg}.json"], "g7.py": [f"g7_{arg}.json"]}[script]
    for o in outs:
        if (wd / "qc" / o).exists():
            shutil.copyfile(wd / "qc" / o, rd / o)
    log(f"{fam} {vname} {tag} rc={rc} {time.time() - t:.0f}s")
    return rc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fam", required=True, choices=("F2", "F5"))
    ap.add_argument("--work", required=True); ap.add_argument("--res", required=True)
    ap.add_argument("--jobs", type=int, default=2); ap.add_argument("--variants", default="")
    ap.add_argument("--build-only", action="store_true")
    a = ap.parse_args()
    fam = a.fam; wroot = Path(a.work) / fam; res = Path(a.res)
    for p in (wroot, res):
        assert "c_src" not in str(p.resolve()), p
    res.mkdir(parents=True, exist_ok=True)
    vs = [v for v in variants() if not a.variants or v[0] in a.variants.split(",")]
    for vname, cue, seed, s in vs:
        wd = wroot / vname
        rec = build_out(fam, wd / "out", cue, seed, s); build_qc(fam, wd); (wd / "tmp/chk").mkdir(parents=True, exist_ok=True)
        (res / vname).mkdir(parents=True, exist_ok=True)
        json.dump({"variant": vname, "cue": cue, "seed": seed, "strength": s, "files": rec},
                  open(res / vname / "plant.json", "w"), indent=1)
        log(f"built {vname} " + " ".join(f"{k}:{v['n_marked']}/{v['n_eligible']}" for k, v in rec.items()))
    if a.build_only:
        return
    tasks = [(v[0], "g6.py", "qc_sample") for v in vs] + [(v[0], "g7.py", nm) for v in vs for nm in NAMES]
    with ThreadPoolExecutor(a.jobs) as ex:
        rcs = list(ex.map(lambda t: run_task(fam, wroot, res, *t), tasks))
    json.dump({"fam": fam, "tasks": [list(t) + [rc] for t, rc in zip(tasks, rcs)], "seconds": round(time.time() - T0)},
              open(res / "RUN.json", "w"), indent=1)
    log(f"done rc_max={max(rcs)}")
    sys.exit(1 if max(rcs) else 0)


if __name__ == "__main__":
    main()
