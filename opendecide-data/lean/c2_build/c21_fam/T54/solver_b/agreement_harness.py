"""T54 solver A vs solver B agreement harness. IN MEMORY ONLY: it calls the lane generator's generate_in_memory (stand-in names),
compares solver B to the gold the generator stored (solver A), and prints counts. It writes no rows and prints no item text.

Usage:  python3 -I solver_b/agreement_harness.py [total_per_seed] [seed ...]
"""
import collections
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FAM = os.path.dirname(HERE)
ROOT = os.path.dirname(FAM)
for p in (HERE, ROOT, FAM):
    if p not in sys.path:
        sys.path.insert(0, p)

import t54_solver_b as sb  # noqa: E402
import t54_render_b as rb  # noqa: E402


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def run(total=1000, seeds=("b-agree-1",)):
    import t54_generator as gen  # the lane generator (solver A inside); imported by the harness only, never by solver B
    n = 0
    per_sb = collections.Counter()
    agree_sb = collections.Counter()
    letter_bad = collections.Counter()
    classes = collections.Counter()
    flag_counts = collections.Counter()
    abstains = collections.Counter()
    r_agree, r_dis, r_abs, r_cls = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
    fidelity = collections.Counter()
    for seed in seeds:
        recs = gen.generate_in_memory(total=total, seed=seed, standin=True)
        for r in recs:
            res = sb.solve(r)
            s = r["sub_block"]
            n += 1
            per_sb[s] += 1
            for fl in res.flags:
                flag_counts[(s, fl)] += 1
            if res.abstain:
                abstains[(s, res.abstain)] += 1
            # ---- render-fidelity parse (text only) versus the stored letter
            kind, val = rb.solve_text(s, r["rendered"]["text"])
            tag = None
            if s == "s1_need4":
                try:
                    ul = rb.user_lines(rb.parse(r["rendered"]["text"])["conv"])
                except rb.Abstain:
                    ul = []
                ent = r["intent"].get("entity")
                for a in r["intent"].get("args", []):
                    if a["source"] != "user_turn" or not a.get("required"):
                        continue
                    if rb.stated(ul, a["param"], ent):
                        continue
                    if a["param"] == ent + "_id" and any(rb.re.search(r"\bthe " + ent + r" [a-z]{3}-\d+", l) for l in ul[:-1]):
                        continue  # id given by an earlier mention (reference form)
                    tag = "stated_value_missing_from_render"
                if r["gold"] == "NO_TOOL" and r["intent"].get("type") == "tool":
                    try:
                        P = rb.parse(r["rendered"]["text"])
                        rk = rb.req_kind(rb.request_of(rb.user_lines(P["conv"])))[0]
                        sib = [t for t in P["tools"].values() if t["entity"] == r["intent"]["entity"] and t["rw"] == "read" and t["group"] in ("get", "check")]
                        if rk in ("fetch", "fetch_ref") and sib:
                            tag = "fetch_form_no_tool_with_get_or_check_sibling_listed"
                    except rb.Abstain:
                        pass
            if s == "s5_argground":
                for a in r["call"]["args"]:
                    if a["prov"].get("kind") == "wrong_role" and ("     %s: %s" % (a["param"], a["value"])) in r["rendered"]["text"]:
                        tag = "wrong_role_value_rendered_under_the_same_key"
            if tag:
                fidelity[(s, tag)] += 1
            if kind == "abstain":
                r_abs[(s, val, tag or "-")] += 1
            elif val == r["gold_letter"]:
                r_agree[s] += 1
            else:
                r_dis[s] += 1
                r_cls[(s, "A=" + str(r["gold"] if s not in ("s2_pick", "s6_parseq") else "<option>"), r.get("entry"), tag or "-")] += 1
            if res.label == r["gold"]:
                agree_sb[s] += 1
                if res.letter != r["gold_letter"]:
                    letter_bad[s] += 1
            else:
                classes[(s, "A=" + str(r["gold"] if s not in ("s2_pick", "s6_parseq") else "<option>"),
                         "B=" + str(res.label if s not in ("s2_pick", "s6_parseq") else ("<option>" if res.label else None)),
                         r.get("entry"), r.get("perturb"), res.abstain or "-")] += 1
    return dict(n=n, per_sb=dict(per_sb), agree_sb=dict(agree_sb), letter_mismatch=dict(letter_bad),
                classes=classes, flags=flag_counts, abstains=abstains, r_agree=dict(r_agree), r_dis=dict(r_dis),
                r_abs=r_abs, r_cls=r_cls, fidelity=fidelity)


def main(argv):
    total = int(argv[1]) if len(argv) > 1 else 1000
    seeds = tuple(argv[2:]) or ("b-agree-1",)
    out = run(total, seeds)
    agree = sum(out["agree_sb"].values())
    print("rows", out["n"], "agree", agree, "agreement %.4f%%" % (100.0 * agree / max(1, out["n"])))
    for s in sorted(out["per_sb"]):
        a = out["agree_sb"].get(s, 0)
        print("  %-14s n=%5d agree=%5d  %.3f%%  letter_mismatch=%d" % (s, out["per_sb"][s], a, 100.0 * a / out["per_sb"][s],
                                                                         out["letter_mismatch"].get(s, 0)))
    print("disagreement classes (count):")
    for k, c in sorted(out["classes"].items(), key=lambda kv: -kv[1]):
        print("  ", c, k)
    print("B abstains:", dict(out["abstains"]))
    print("B consistency/spec-gap flags:", dict(out["flags"]))
    print("RENDER-FIDELITY PARSE (text only; abstain is not a disagreement):")
    for s in sorted(out["per_sb"]):
        a, d = out["r_agree"].get(s, 0), out["r_dis"].get(s, 0)
        ab = sum(c for (ss, _, _), c in out["r_abs"].items() if ss == s)
        dec = a + d
        print("  %-14s decided=%5d agree=%5d disagree=%4d abstain=%4d  agree_of_decided=%.3f%%  coverage=%.1f%%" % (
            s, dec, a, d, ab, 100.0 * a / max(1, dec), 100.0 * dec / out["per_sb"][s]))
    print("  render disagreement classes:")
    for k, c in sorted(out["r_cls"].items(), key=lambda kv: -kv[1]):
        print("    ", c, k)
    print("  render abstain classes:")
    for k, c in sorted(out["r_abs"].items(), key=lambda kv: -kv[1]):
        print("    ", c, k)
    print("  record-vs-text fidelity tags:", dict(out["fidelity"]))
    print("sha256 solver_b:", sha(os.path.join(HERE, "t54_solver_b.py")))
    print("sha256 render_b:", sha(os.path.join(HERE, "t54_render_b.py")))
    print("sha256 generator:", sha(os.path.join(FAM, "t54_generator.py")))
    print("sha256 solver_a:", sha(os.path.join(FAM, "t54_solver_a.py")))


if __name__ == "__main__":
    main(sys.argv)
