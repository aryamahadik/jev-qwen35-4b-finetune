"""Summarise A19.1 (b) power results -> POWER_G6G7.json. A cue is caught by a gate when the gate's YES/NO verdict
FAILS on the planted copy (F2 also has choice rows, which the cues never touch; their verdict is the control's and is
reported separately). G7 runs on qc_sample and candidates_r1 as the families run it; G7 fails if either run fails."""
import json, sys, hashlib
from pathlib import Path

A = Path(__file__).resolve().parent
CUES = (("token", 0.20), ("swap", 0.20), ("repeat", 0.40))
SEEDS = range(5)


def g6_verdict(fam, d):
    if fam == "F2":
        yn = {k: v for k, v in d["yes_no"].items() if isinstance(v, dict)}
        return {"yes_no_pass": all(v["pass"] for v in yn.values()), "overall_pass": d["pass"],
                "best_acc": {k: round(v["best"], 4) for k, v in yn.items()},
                "failing": [k for k, v in yn.items() if not v["pass"]]}
    return {"yes_no_pass": d["pass"], "overall_pass": d["pass"], "max_gated": d["max_gated"],
            "failing": [k for k, v in d["gated"].items() if v > 0.52]}


def g7_verdict(fam, d):
    if fam == "F2":
        yf = [f for f in d["fails"] if f["part"] == "yes_no"]
        return {"yes_no_pass": not yf, "overall_pass": d["pass"], "n_fail_yes_no": len(yf), "n_fail": d["n_fail"],
                "top_yes_no": [(f["feature"], f["n"], f["yes_rate"]) for f in yf[:3]]}
    return {"yes_no_pass": d["pass"], "overall_pass": d["pass"], "n_fail_yes_no": d["n_fail"], "n_fail": d["n_fail"],
            "top_yes_no": [(f["feature"], f["n"], f["share_major"]) for f in d["fails"][:3]]}


def load_variant(fam, v):
    rd = A / f"results_{fam}" / v
    g6 = json.load(open(rd / ("g6.json" if fam == "F2" else "g6_qc_sample.json")))
    g7 = {nm: json.load(open(rd / f"g7_{nm}.json")) for nm in ("qc_sample", "candidates_r1")}
    v6 = g6_verdict(fam, g6); v7 = {nm: g7_verdict(fam, d) for nm, d in g7.items()}
    plant = json.load(open(rd / "plant.json"))
    return {"G6": v6, "G7": v7, "G7_yes_no_pass": all(x["yes_no_pass"] for x in v7.values()),
            "marked": {k: f"{x['n_marked']}/{x['n_yes_no']}" for k, x in plant["files"].items()}}


def main():
    out = {"ruling": "PREREG_FINAL Amendment A19.1 (b)", "caught_rule": "gate's yes/no verdict FAILS on the planted copy",
           "cues": {c: s for c, s in CUES}, "seeds": list(SEEDS), "families": {}}
    tf = A / "TFIDF.json"
    tfd = json.load(open(tf)) if tf.exists() else None
    allok = True
    for fam in ("F2", "F5"):
        ctl = load_variant(fam, "control"); fo = {"control": ctl, "cues": {}}
        for cue, s in CUES:
            per = {v: load_variant(fam, f"{cue}_s{v}") for v in SEEDS}
            k6 = sum(not p["G6"]["yes_no_pass"] for p in per.values())
            k7 = sum(not p["G7_yes_no_pass"] for p in per.values())
            kany = sum((not p["G6"]["yes_no_pass"]) or (not p["G7_yes_no_pass"]) for p in per.values())
            c = {"strength": s, "G6_caught": f"{k6}/5", "G7_caught": f"{k7}/5", "G6_or_G7_caught": f"{kany}/5",
                 "ok_ge_4": max(k6, k7) >= 4 or kany >= 4, "per_seed": per}
            if tfd:
                tk = sum(not tfd["planted"][fam][f"{cue}_s{v}"]["pass"] for v in SEEDS)
                c["TFIDF_caught"] = f"{tk}/5"; c["TFIDF_ok_ge_4"] = tk >= 4
            fo["cues"][cue] = c; allok &= c["ok_ge_4"]
        out["families"][fam] = fo
    out["all_caught_ge_4_by_G6_or_G7"] = allok
    if tfd:
        out["tfidf"] = {"tool": tfd["tool"], "tool_sha256": tfd["tool_sha256"], "rule": tfd["rule"],
                        "unplanted": tfd["unplanted"],
                        "all_planted_caught_ge_4": all(out["families"][f]["cues"][c]["TFIDF_ok_ge_4"]
                                                       for f in ("F2", "F5") for c, _ in CUES)}
    out["script_sha256"] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (A / "run_power.py", A / "summarize.py")}
    (A / "POWER_G6G7.json").write_text(json.dumps(out, indent=1))
    for fam, fo in out["families"].items():
        print(fam, "control G6 yn_pass", fo["control"]["G6"]["yes_no_pass"], "G7 yn_pass", fo["control"]["G7_yes_no_pass"])
        for cue, c in fo["cues"].items():
            print(fam, cue, c["strength"], "G6", c["G6_caught"], "G7", c["G7_caught"], "any", c["G6_or_G7_caught"],
                  "TFIDF", c.get("TFIDF_caught"))
    print("all_caught", allok)


if __name__ == "__main__":
    main()
