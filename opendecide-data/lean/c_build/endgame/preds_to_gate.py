"""A25 (a): the pre-registered converter from od_gcp.py save() preds to the frozen A15 scorer's gate format.

od_gcp.py writes {"id", "model", "probs": {<option text | yes | no>: p}} (the 6.0 served readout, view-aggregated, the
probs keys in the item's option order). The frozen scorer (sealed_nd/score_nd.py, sha 953a3363...) reads only
{"id", "choice"} / {"id", "p_yes"}; an unconverted file scores coverage 0 and the look is REFUSED. Fixed rules:
  - choice row (probs keys other than exactly {yes, no}): {"id", "choice": the argmax option text}. A tie for the top
    probability (exact float equality) goes to the FIRST tied option in the readout's fixed order (the probs key order
    = the item's option order; gate_dev.argmax_label's max() over r["options"]). Ties are counted and reported.
  - yes/no row (probs keys exactly {yes, no}): {"id", "p_yes": probs["yes"], "choice": argmax by the same rule}.
    p_yes is the one read as served (no renormalisation); the frozen scorer reads p_yes first on a yes/no item
    (> 0.5 yes, < 0.5 no, == 0.5 half credit) and reads "choice" only on a choice item whose options are yes / no.
  - a row with no probs or a non-finite p: written as nothing (the scorer's coverage check counts it missing).
Output: <stem>.gate.jsonl beside the input, plus <stem>.gate.json = {src_sha256, out_sha256, converter_sha256, counts}.
Sealed text (option strings) is handled by program only: this prints COUNTS ONLY, never an id or an option.

  ../.venv/bin/python c_build/endgame/preds_to_gate.py <preds.jsonl> [--out <path>]   # convert (exit 2 = refused)
  ../.venv/bin/python c_build/endgame/preds_to_gate.py check <preds.jsonl>             # record + sha256s still match
  ../.venv/bin/python c_build/endgame/preds_to_gate.py prove                           # A25 (a) dev-side proof

prove: on C1's dev reads (c_build/preread/preread_c1/preds_<split>/q35_4b_main500k_pre{,_perm,_served}.jsonl; never
the sealed reads) each file is converted in memory and scored row by row with the FROZEN scorer's own score_items()
(source sha256-checked against A15, compiled from its bytes; nothing written into sealed_nd/), and compared with
gate_dev.score() (the dev-side readout accuracy). PASS = every row's score and every yes/no Brier term identical.
Writes c_build/endgame/logs/preds_to_gate_dev_proof.json (counts and sha256s only).
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[1]
YN = frozenset(("yes", "no"))
PROOF = HERE / "logs/preds_to_gate_dev_proof.json"
PREREAD_C1 = LEAN / "c_build/preread/preread_c1"
C1_PRE = "q35_4b_main500k_pre"
A15_RE = re.compile(r"scorer `score_nd\.py`, sha256 `([0-9a-f]{64})`")


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def converter_sha() -> str:
    return sha(Path(__file__).resolve())


def top(v: dict) -> tuple[str, int]:
    """(first key holding the top probability in the probs' own key order, number of keys tied at the top)."""
    best = max(v.values())
    tied = [k for k, x in v.items() if x == best]
    return tied[0], len(tied)


def convert_row(r: dict) -> tuple[dict | None, bool]:
    """(gate row or None, tie?)."""
    p = r.get("probs")
    if not isinstance(p, dict) or not p:
        return None, False
    try:
        v = {str(k): float(x) for k, x in p.items()}
    except (TypeError, ValueError):
        return None, False
    if not all(math.isfinite(x) for x in v.values()):
        return None, False
    choice, n_top = top(v)
    if set(v) == YN:
        return {"id": r["id"], "p_yes": v["yes"], "choice": choice}, n_top > 1
    return {"id": r["id"], "choice": choice}, n_top > 1


def convert_rows(lines) -> tuple[list[dict], dict, set]:
    seen, rows, models = set(), [], set()
    n = {"rows": 0, "yes_no": 0, "choice": 0, "tie": 0, "no_probs": 0}
    for line in lines:
        if not line.strip():
            continue
        r = json.loads(line)
        if not isinstance(r, dict) or "id" not in r or "probs" not in r:
            raise ValueError("not od_gcp save() format ({id, model, probs})")
        if r["id"] in seen:
            raise ValueError("duplicate id")
        seen.add(r["id"])
        models.add(r.get("model"))
        n["rows"] += 1
        c, tie = convert_row(r)
        if c is None:
            n["no_probs"] += 1
            continue
        n["tie"] += tie
        n["yes_no" if "p_yes" in c else "choice"] += 1
        rows.append(c)
    if len(models) > 1:
        raise ValueError("more than one model name in one preds file")
    return rows, n, models


def out_paths(src: Path, out: Path | None = None) -> tuple[Path, Path]:
    o = out or src.with_name((src.name[:-len(".jsonl")] if src.name.endswith(".jsonl") else src.name) + ".gate.jsonl")
    return o, o.with_name(o.name[:-len(".jsonl")] + ".json")


def convert(src: Path, out: Path | None = None) -> dict:
    src = Path(src)
    o, rp = out_paths(src, out)
    with open(src) as f:
        rows, n, models = convert_rows(f)
    tmp = o.with_name(o.name + ".tmp")
    with open(tmp, "w") as f:
        for c in rows:
            f.write(json.dumps(c) + "\n")
    tmp.replace(o)
    rec = {"what": "preds_to_gate.py (A25 a): od_gcp probs -> A15 scorer gate format (choice = argmax, a top tie -> the "
                   "first tied option in the readout's fixed order; yes/no -> p_yes as served, plus choice)",
           "src": src.name, "src_sha256": sha(src), "out": o.name, "out_sha256": sha(o),
           "converter_sha256": converter_sha(), "model": next(iter(models), None), "counts": n}
    rp.write_text(json.dumps(rec, indent=1) + "\n")
    return rec


def check(src: Path, out: Path | None = None) -> str | None:
    """None if <stem>.gate.jsonl is convert(src) by THIS converter (record + both sha256 match), else the problem."""
    o, rp = out_paths(Path(src), out)
    try:
        rec = json.loads(rp.read_text())
    except Exception:  # noqa: BLE001
        return f"{rp.name} missing (run preds_to_gate.py)"
    if not Path(src).exists() or rec.get("src_sha256") != sha(Path(src)):
        return f"{rp.name}: source preds changed since conversion"
    if not o.exists() or rec.get("out_sha256") != sha(o):
        return f"{o.name} missing or changed since conversion"
    if rec.get("converter_sha256") != converter_sha():
        return f"{rp.name}: written by another converter version"
    return None


# ---- A25 (a) dev-side proof -----------------------------------------------------------------------------------------
def a15_scorer_sha(prereg: Path = LEAN / "PREREG_FINAL.md") -> str:
    s = set(A15_RE.findall(prereg.read_text()))
    if len(s) != 1:
        raise SystemExit(f"A15 scorer sha256 found {len(s)} times in {prereg.name}")
    return s.pop()


def frozen_scorer(path: Path = LEAN / "sealed_nd/score_nd.py", want: str | None = None) -> dict:
    """The A15 scorer's namespace, compiled from its bytes after the sha256 check (no import: no __pycache__ in
    sealed_nd/). Only score_items() is used; it touches no file."""
    b = Path(path).read_bytes()
    want = want or a15_scorer_sha()
    if hashlib.sha256(b).hexdigest() != want:
        raise SystemExit(f"{path}: sha256 is not A15's; not used")
    ns = {"__name__": "score_nd_frozen", "__file__": str(path)}
    exec(compile(b, str(path), "exec"), ns)  # noqa: S102  (frozen, sha-pinned code)
    return ns


def prove_file(rows_by_id: dict, lines, score_items, gd_score) -> dict:
    gate, n, _ = convert_rows(lines)
    preds = {str(g["id"]): g for g in gate}
    raw = {str(json.loads(x)["id"]): json.loads(x)["probs"] for x in lines if x.strip()}
    ids = [i for i in rows_by_id]
    suite = [{"id": str(i), "qtype": "choice" if rows_by_id[i]["qtype"] != "noul" else "noul",
              "options": rows_by_id[i].get("options"), "gold": rows_by_id[i]["gold"]} for i in ids]
    sc, ok, br = score_items(suite, preds)
    dev = [gd_score(rows_by_id[i], raw.get(str(i))) for i in ids]
    acc_dev = sum(d[0] for d in dev)
    mism = sum(1 for s, d in zip(sc, dev) if float(s) != float(d[0]))
    yn = [(b, d[1]) for b, d, r in zip(br, dev, suite) if r["qtype"] == "noul"]
    br_mism = sum(1 for b, d in yn if d is None or abs(float(b) - float(d)) > 1e-12)
    sums = [abs(p.get("yes", 0) + p.get("no", 0) - 1) for p in raw.values() if set(p) == YN]
    yn_choice = sum(1 for r in suite if r["qtype"] == "choice" and set(r["options"] or []) == YN)
    return {"rows": len(ids), "covered": int(ok.sum()), "acc_dev": round(100 * acc_dev / len(ids), 4),
            "acc_scorer": round(100 * float(sc.sum()) / len(ids), 4), "correct_dev": int(acc_dev),
            "correct_scorer": float(sc.sum()), "row_mismatches": mism, "yes_no_rows": len(yn),
            "brier_mismatches": br_mism, "ties": n["tie"], "max_abs_pyes_plus_pno_minus_1": max(sums, default=0.0),
            "choice_rows_with_yes_no_options": yn_choice}


def prove(root: Path = PREREAD_C1, data: Path = LEAN / "data", out: Path = PROOF) -> int:
    sys.path.insert(0, str(LEAN))
    import gate_dev  # noqa: E402  (pinned; score() = the dev-side readout accuracy, ties and missing = wrong)
    want = a15_scorer_sha()
    score_items = frozen_scorer(want=want)["score_items"]
    res, inputs, ok_all = {}, {}, True
    for d in sorted(Path(root).glob("preds_*")):
        sp = d.name[len("preds_"):]
        rows = {}
        for line in open(data / f"{sp}.jsonl"):
            r = json.loads(line)
            rows[r["id"]] = r
        res[sp] = {}
        for f in sorted(d.glob(f"{C1_PRE}*.jsonl")):
            if f.name.endswith(".gate.jsonl"):
                continue
            tag = f.name[len(C1_PRE):-len(".jsonl")] or "_pre"
            lines = f.read_text().splitlines()
            x = prove_file(rows, lines, score_items, gate_dev.score)
            x["pass"] = (x["row_mismatches"] == 0 and x["brier_mismatches"] == 0 and x["covered"] == x["rows"]
                         and x["correct_dev"] == x["correct_scorer"])
            ok_all &= x["pass"]
            res[sp][tag] = x
            inputs[f"{d.name}/{f.name}"] = sha(f)
        print(f"{sp:14s} " + "  ".join(f"{t.strip('_')}: n {x['rows']} dev {x['acc_dev']:.2f} scorer "
                                        f"{x['acc_scorer']:.2f} mism {x['row_mismatches']}/{x['brier_mismatches']} "
                                        f"ties {x['ties']}" for t, x in res[sp].items()))
    rec = {"what": "A25 (a) proof: preds_to_gate.py + the frozen A15 scorer's score_items reproduce gate_dev.score's "
                   "dev-side readout accuracy row by row on C1's dev reads (never sealed preds)",
           "converter_sha256": converter_sha(), "scorer_sha256": want,
           "gate_dev_sha256": sha(LEAN / "gate_dev.py"), "inputs_sha256": inputs, "by_split": res,
           "files": sum(len(v) for v in res.values()), "pass": bool(ok_all and inputs),
           "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rec, indent=1) + "\n")
    print(f"{rec['files']} files; {'PASS' if rec['pass'] else 'FAIL'} -> {out}")
    return 0 if rec["pass"] else 1


def proof_problem(path: Path = PROOF) -> str | None:
    """None if the dev-side proof record passed for THIS converter and the A15 scorer, else the problem."""
    try:
        rec = json.loads(Path(path).read_text())
    except Exception:  # noqa: BLE001
        return "preds_to_gate dev proof missing (run preds_to_gate.py prove)"
    if rec.get("pass") is not True:
        return "preds_to_gate dev proof did not pass"
    if rec.get("converter_sha256") != converter_sha():
        return "preds_to_gate dev proof was made with another converter version (re-run prove)"
    if rec.get("scorer_sha256") != a15_scorer_sha():
        return "preds_to_gate dev proof was made with a scorer that is not A15's"
    return None


def main(argv=None) -> int:
    a = list(sys.argv[1:] if argv is None else argv)
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        return 0 if a else 2
    if a[0] == "prove":
        return prove()
    if a[0] == "check":
        e = check(Path(a[1]))
        print(e or "OK")
        return 1 if e else 0
    out = None
    if "--out" in a:
        i = a.index("--out")
        out = Path(a[i + 1])
        del a[i:i + 2]
    try:
        rec = convert(Path(a[0]), out)
    except (ValueError, KeyError, json.JSONDecodeError) as e:
        print(f"REFUSED: {type(e).__name__}: {str(e)[:80]}")
        return 2
    print("preds_to_gate", json.dumps(rec["counts"]), "out_sha256", rec["out_sha256"][:12])
    return 0


if __name__ == "__main__":
    sys.exit(main())
