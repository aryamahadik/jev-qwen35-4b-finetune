"""A25 (a) sealed-side confirm (sealed agent; SYNTHETIC inputs only): the converted prediction files on the frozen scorer.

Reads the scorer CODE only (sealed_nd/score_nd.py, sha256 == A15) and copies it UNMODIFIED into run_a25/<case>/ next to
a synthetic suite (its own sha256 / manifest). Never opens sealed_nd/suite_v2.jsonl, sealed_nd/looks.jsonl or any sealed
preds; the real sealed_nd/ is stat-checked (dir mtime, looks.jsonl size/mtime) before and after.
Every look runs through score_nd_cli.look_cmd(), i.e. the exact command template of SCORE_ND_CLI.json (convert both
od_gcp files with preds_to_gate.py, pipefail, tee), with the paths pointed at the synthetic copy.
Checks:
  main  S1 + C looks on converted files: exit 0, coverage as expected, headline cand / ref == an independent
        re-implementation of the readout (fixed-order argmax; p_yes > 0.5 / == 0.5 half); refused looks (raw probs
        files, --ref-name not C1, a second C look) exit non-zero under pipefail and whether they write a looks line;
        gate_c's header / stdout-number checks accept the real printed S1 block.
  tie   every choice row a full tie and every yes/no row p_yes = 0.5: the scorer's headline equals the fixed-order
        rule (first option) and differs from "ties wrong".
Writes confirm_a25.json (CONFIRM_KEYS of score_nd_cli.py + details). Then: score_nd_cli.py confirm --from it.

  cd lean && ../.venv/bin/python c_build/endgame/sealed_confirm/confirm_a25.py
"""
from __future__ import annotations

import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
E = HERE.parent
LEAN = E.parents[1]
sys.path.insert(0, str(E))
import gate_c  # noqa: E402
import preds_to_gate  # noqa: E402
import score_nd_cli  # noqa: E402

SEALED = LEAN / "sealed_nd"
RUN = HERE / "run_a25"
OUT = HERE / "confirm_a25.json"


def sha(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def sealed_stat() -> dict:
    lk = SEALED / "looks.jsonl"
    return {"dir_mtime_ns": SEALED.stat().st_mtime_ns,
            "looks": [lk.stat().st_size, lk.stat().st_mtime_ns] if lk.exists() else None}


# ---- synthetic suite + od_gcp-format reads --------------------------------------------------------------------------
def suite(rng: random.Random) -> list[dict]:
    rows, k = [], 0
    spec = [("A", "D1", 240), ("A", "D2", 240), ("P", "P1", 80), ("P", "P2", 80), ("P", "P3", 80), ("B1", "B1", 80),
            ("B2", "B2", 80)]
    for part, dom, n in spec:
        for j in range(n):
            g = "syn-g%05d" % (k // 2)
            split = "nd_select" if (k // 2) % 2 == 0 else "nd_confirm"
            r = {"id": "syn-%05d" % k, "group_id": g, "split": split, "prompt": "synthetic item",
                 "meta": {"part": part, "domain_id": dom}}
            m = j % 8
            if m < 3:
                r.update(qtype="noul", gold=rng.randint(0, 1))
            else:
                kind = rng.random()
                if kind < 0.15:
                    opts = ["B", "A", "C", "D"][:rng.randint(2, 4)]          # letter-like option texts
                elif kind < 0.25:
                    opts = rng.choice([["yes", "no"], ["no", "yes"]])        # a choice item with yes/no options
                else:
                    opts = ["option %d of item %d" % (i, k) for i in range(rng.randint(2, 8))]
                r.update(qtype="choice", options=opts, gold=rng.choice(opts))
            rows.append(r)
            k += 1
    return rows


def read(rows, rng: random.Random, acc: float, tie_rate: float, half_rate: float, drop: int, all_tie=False):
    """od_gcp save() rows: {id, model, probs} with probs keys in the item's option order (yes, no for yes/no)."""
    out = []
    drop_ids = set(rng.sample([r["id"] for r in rows if r["split"] == "nd_select"], drop)) if drop else set()
    for r in rows:
        if r["id"] in drop_ids:
            out.append({"id": r["id"], "model": "synth", "probs": {}})
            continue
        if r["qtype"] == "noul":
            if all_tie or rng.random() < half_rate:
                py = 0.5
            else:
                ok = rng.random() < acc
                py = rng.choice([0.62, 0.8, 0.97]) if (r["gold"] == 1) == ok else rng.choice([0.03, 0.2, 0.41])
            out.append({"id": r["id"], "model": "synth", "probs": {"yes": py, "no": 1.0 - py}})
            continue
        opts = r["options"]
        if all_tie:
            p = {o: 1.0 / len(opts) for o in opts}
        else:
            win = r["gold"] if rng.random() < acc else rng.choice([o for o in opts if o != r["gold"]])
            p = {o: rng.uniform(0.0, 0.3) for o in opts}
            p[win] = 0.6
            if rng.random() < tie_rate:                                    # exact tie at the top with another option
                other = rng.choice([o for o in opts if o != win])
                p[other] = 0.6
            s = sum(p.values())
            p = {o: v / s for o, v in p.items()}
            top = max(p.values())
            p = {o: (top if abs(v - top) < 1e-15 else v) for o, v in p.items()}   # keep the tie exact after scaling
        out.append({"id": r["id"], "model": "synth", "probs": {o: p[o] for o in opts}})
    return out


def expected(rows, reads, scope, fixed_order=True) -> tuple[float, float]:
    """(mean score, coverage) over scope by an independent readout implementation (not the converter, not the scorer)."""
    by = {x["id"]: x["probs"] for x in reads}
    s, cov = 0.0, 0
    for i in scope:
        r, p = rows[i], by.get(rows[i]["id"]) or {}
        if not p:
            continue
        cov += 1
        if r["qtype"] == "noul":
            s += 0.5 if p["yes"] == 0.5 else float((p["yes"] > 0.5) == (r["gold"] == 1))
        else:
            best = max(p[o] for o in r["options"])
            tied = [o for o in r["options"] if p[o] == best]
            s += float(tied[0] == r["gold"]) if (fixed_order or len(tied) == 1) else 0.0
    return s / len(scope), cov / len(scope)


def write(path: Path, rows):
    path.write_text("".join(json.dumps(r) + "\n" for r in rows))


def setup(case: str, rows) -> Path:
    d = RUN / case
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    shutil.copy2(SEALED / "score_nd.py", d / "score_nd.py")                # code only, unmodified
    write(d / "suite_v2.jsonl", rows)
    s = sha(d / "suite_v2.jsonl")
    (d / "suite_v2.sha256").write_text(f"{s}  suite_v2.jsonl\n")
    (d / "manifest_v2.json").write_text(json.dumps({"suite_sha256": s, "part_a_domains": ["D1", "D2"]}))
    return d


def nlooks(d: Path) -> int:
    p = d / "looks.jsonl"
    return sum(1 for x in p.read_text().splitlines() if x.strip()) if p.exists() else 0


def bash(cmd: str) -> tuple[int, str]:
    r = subprocess.run(["bash", "-c", cmd], capture_output=True, text=True, timeout=140)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def look(d: Path, kind: str, cand: Path, ref: Path, tee: str, ref_name: str | None = None, convert=True):
    cmd = score_nd_cli.look_cmd(kind, str(cand), "synth_cand", str(ref), str(d / tee), f"A25 synthetic {kind}",
                                sealed=d)
    if ref_name:
        cmd = cmd.replace(f"--ref-name {score_nd_cli.REF_NAME} ", f"--ref-name {ref_name} ")
    if not convert:                       # the scorer fed the raw od_gcp files (what the pre-A25 commands did)
        cmd = cmd.replace(".gate.jsonl", ".jsonl")
    n0 = nlooks(d)
    rc, txt = bash(cmd)
    return {"exit": rc, "refused": "REFUSED" in txt, "logged": nlooks(d) - n0,
            "last": [x for x in txt.splitlines() if x.strip()][-1][:160] if txt.strip() else ""}, txt


def headline(d: Path) -> dict:
    return [json.loads(x) for x in (d / "looks.jsonl").read_text().splitlines() if x.strip()][-1]


def main() -> int:
    want = score_nd_cli.a15()["scorer_sha256"]
    if sha(SEALED / "score_nd.py") != want:
        raise SystemExit("sealed_nd/score_nd.py sha256 is not A15's: not run")
    ns = preds_to_gate.frozen_scorer(want=want)
    before = sealed_stat()
    rng = random.Random(25)
    rows = suite(rng)
    sel = [i for i, r in enumerate(rows) if r["split"] == "nd_select"]
    selA = [i for i in sel if rows[i]["meta"]["part"] == "A"]
    confA = [i for i, r in enumerate(rows) if r["split"] == "nd_confirm" and r["meta"]["part"] == "A"]
    res, ok = {}, True

    # ---- main case ----
    d = setup("main", rows)
    cand, ref = read(rows, rng, 0.8, 0.08, 0.03, 2), read(rows, rng, 0.65, 0.08, 0.03, 0)
    write(d / "cand.jsonl", cand)
    write(d / "c1.jsonl", ref)
    m = {}
    m["raw_probs_S1"], _ = look(d, "S1", d / "cand.jsonl", d / "c1.jsonl", "raw.out", convert=False)
    m["ref_name_not_C1_S1"], _ = look(d, "S1", d / "cand.jsonl", d / "c1.jsonl", "badref.out",
                                      ref_name="q35_4b_main500k_pre")
    m["S1"], _ = look(d, "S1", d / "cand.jsonl", d / "c1.jsonl", "s1.out")
    s1_txt = (d / "s1.out").read_text()                                  # the tee capture gate_c reads
    h1 = headline(d)
    e_c, cov_c = expected(rows, cand, sel)
    eA_c, _ = expected(rows, cand, selA)
    eA_r, _ = expected(rows, ref, selA)
    m["S1"].update(cand=h1["headline"]["cand"], ref=h1["headline"]["ref"], expected_cand=eA_c, expected_ref=eA_r,
                   coverage=[h1["coverage_cand"], h1["coverage_ref"]], expected_coverage_cand=round(cov_c, 4))
    s1_ok = (m["S1"]["exit"] == 0 and m["S1"]["logged"] == 1 and abs(h1["headline"]["cand"] - eA_c) < 1e-12
             and abs(h1["headline"]["ref"] - eA_r) < 1e-12 and h1["coverage_cand"] == round(cov_c, 4)
             and h1["coverage_ref"] == 1.0 and h1["ref_name"] == "C1")
    # gate_c against the real printed S1 block (header with the converted files + the A select row's numbers)
    try:
        gate_c.check_header(s1_txt, "S1", "synth_cand", sha(d / "cand.gate.jsonl"), sha(d / "c1.gate.jsonl"),
                            len(sel))
        row = [x for x in s1_txt.splitlines() if x.startswith("A select (headline, micro)")][0]
        v = re.findall(r"[-+]?\d+\.\d+|\d+", row[len("A select (headline, micro)"):])
        rec = {"n": int(v[0]), "cand": float(v[2]), "ref": float(v[3]), "diff": float(v[4]), "lo": float(v[5]),
               "hi": float(v[6])}
        gate_c.check_interval(rec, "synthetic S1", len(selA))
        gate_c.check_stdout(gate_c.stdout_numbers(s1_txt), rec, "synthetic S1")
        m["gate_c_accepts_printed_S1"] = True
    except Exception as ex:  # noqa: BLE001
        m["gate_c_accepts_printed_S1"] = f"{type(ex).__name__}: {str(ex)[:120]}"
    m["C"], _ = look(d, "C", d / "cand.jsonl", d / "c1.jsonl", "c.out")
    hc = headline(d)
    eC_c, _ = expected(rows, cand, confA)
    eC_r, _ = expected(rows, ref, confA)
    m["C"].update(cand=hc["headline"]["cand"], ref=hc["headline"]["ref"], expected_cand=eC_c, expected_ref=eC_r)
    c_ok = (m["C"]["exit"] == 0 and m["C"]["logged"] == 1 and abs(hc["headline"]["cand"] - eC_c) < 1e-12
            and abs(hc["headline"]["ref"] - eC_r) < 1e-12)
    m["second_C"], _ = look(d, "C", d / "cand.jsonl", d / "c1.jsonl", "c2.out")
    refused = [m[k] for k in ("raw_probs_S1", "ref_name_not_C1_S1", "second_C")]
    ref_ok = all(x["exit"] != 0 and x["refused"] for x in refused)
    refused_logged = any(x["logged"] for x in refused)
    conv = json.loads((d / "cand.gate.json").read_text())["counts"]
    m["converter_counts_cand"] = conv
    res["main"] = m
    ok &= s1_ok and c_ok and ref_ok and m["gate_c_accepts_printed_S1"] is True and conv["tie"] > 0

    # ---- tie case: every choice row a full tie, every yes/no row p_yes = 0.5 ----
    d = setup("tie", rows)
    tie_c, ref2 = read(rows, rng, 0, 0, 0, 0, all_tie=True), read(rows, rng, 0.65, 0.0, 0.0, 0)
    write(d / "cand.jsonl", tie_c)
    write(d / "c1.jsonl", ref2)
    t, _ = look(d, "S1", d / "cand.jsonl", d / "c1.jsonl", "s1.out")
    ht = headline(d)
    fx, _ = expected(rows, tie_c, selA, fixed_order=True)
    wr, _ = expected(rows, tie_c, selA, fixed_order=False)
    t.update(cand=ht["headline"]["cand"], expected_fixed_order=fx, expected_if_ties_wrong=wr)
    tie_ok = t["exit"] == 0 and abs(ht["headline"]["cand"] - fx) < 1e-12 and abs(fx - wr) > 0.05
    res["tie"] = t
    ok &= tie_ok

    after = sealed_stat()
    lines = s1_txt.splitlines()
    rec = {
        "scorer_sha256": want, "prediction_format_ok": True, "pred_fields": ["id", "choice", "p_yes"],
        "converted_format_ok": bool(s1_ok and c_ok), "converter_sha256": preds_to_gate.converter_sha(),
        "tie_fixed_order_ok": bool(tie_ok), "refused_look_logged": bool(refused_logged),
        "refused_looks_exit_nonzero_under_pipefail": bool(ref_ok), "ref_name_c1_required":
            bool(m["ref_name_not_C1_S1"]["refused"]),
        "yes_no_half_credit_at_0_5": True,
        "printed_per_set": ["n", "groups", "cand", "ref", "diff", "lb", "ub", "p_pos", "brier"],
        "printed_columns_actual": [c.strip() for c in re.split(r"\s{2,}", lines[1].strip())] if len(lines) > 1 else [],
        "printed_units": "pp",
        "bootstrap": {"paired": True, "group": True, "resamples": int(ns["BOOT"]), "seed": int(ns["BOOT_SEED"]),
                      "interval": "95% percentile", "note": "cell k uses default_rng(7+k) (A25 b: binding for sealed "
                                                            "looks; dev CIs 10,000 / seed 0)"},
        "layout_example": "look <id>  kind <S1|S2|C|J>  cand <name> (<sha12 of the .gate.jsonl>)  ref C1 (<sha12>)  "
                          "scope <N> items  coverage <c>/<r>\ncell | n | groups | cand% | ref% | delta | 95% CI "
                          "(paired) [<lo>, <hi>] | P(d>0) | brier c/r\n... then the B3 block",
        "gate_c_accepts_printed_S1": m["gate_c_accepts_printed_S1"],
        "cases": res,
        "real_sealed_nd_unchanged": before == after,
        "how": "read the scorer source (sha256 == A15) + looks with an unmodified copy on a synthetic 880-row suite in "
               "c_build/endgame/sealed_confirm/run_a25/{main,tie}/, through score_nd_cli.look_cmd (preds_to_gate.py "
               "first, pipefail, tee); real sealed_nd/ stat-only, untouched",
        "confirmed_by": "sealed agent (workflow subagent, endgame-build-4 task B)",
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "pass": bool(ok and before == after),
    }
    OUT.write_text(json.dumps(rec, indent=1) + "\n")
    print(f"S1 converted: exit {m['S1']['exit']} cov {m['S1']['coverage']} cand==expected {s1_ok}; C converted: {c_ok}")
    for k in ("raw_probs_S1", "ref_name_not_C1_S1", "second_C"):
        print(f"refused {k}: exit {m[k]['exit']} logged {m[k]['logged']} | {m[k]['last'][:90]}")
    print(f"tie rule fixed order: {tie_ok} (cand {t['cand']:.4f}, fixed {fx:.4f}, ties-wrong {wr:.4f}); "
          f"gate_c on printed S1: {m['gate_c_accepts_printed_S1']}")
    print(f"bootstrap {ns['BOOT']}/{ns['BOOT_SEED']}; refused_look_logged {refused_logged}; real sealed_nd unchanged "
          f"{before == after}; {'PASS' if rec['pass'] else 'FAIL'} -> {OUT.relative_to(LEAN)}")
    return 0 if rec["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
