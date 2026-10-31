"""GEN agreement harness: solver A (the generator's own answer, `label`) versus solver B (c21_fam/GEN/solver_b, blind).

    python3 agree_ab.py --n-per-form 300 --seed agree-1 --out <temp dir> [--split train|dev|both]

Rows are generated IN MEMORY with the lane generator (TEST-ONLY wording pool, provisional names). Nothing but a counts report is written,
and only into the --out directory (use a temp dir). B is called with form / k / carrier / stem / options ONLY.

Per row, two comparisons:
    ANSWER   B's answer option index against A's `label`. Classes: agree, answer_mismatch, b_parse_fail:<code>, b_reject:<code>.
    PARSE    B's parse-back against canon.canonical_spec(row.spec) (gate G-A2). Classes: parse_match, parse_mismatch:<form>:<path>.
Comparator rules (harness side, documented, applied to BOTH sides): numeric strings compare by exact value; the lists that carry no stem order
(LOGIC entities / preds, CA-C4 options, TM-T4 plan tasks) compare as sorted lists; everything else compares in order.
Every disagreement class is reported with counts and up to 3 row ids. No item text is printed or stored.
"""
import argparse
import collections
import hashlib
import json
import os
import re
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "solver_b"))
sys.dont_write_bytecode = True

import canon                                   # noqa: E402  (solver A side: canonical form of a spec)
from builder import Builder                    # noqa: E402
from gen_common import FORMS, GenAllow, make_testonly_pool   # noqa: E402
from b_main import solve_row                   # noqa: E402

from agree_core import NUMERIC, UNORDERED, _key, _num, diff   # noqa: E402,F401  (moved so row_check.py can share them)


def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def collect_shas():
    out = {}
    for sub in ("solver_b", ""):
        d = os.path.join(HERE, sub)
        for fn in sorted(os.listdir(d)):
            p = os.path.join(d, fn)
            if fn.endswith(".py") and os.path.isfile(p):
                out[(sub + "/" if sub else "") + fn] = sha_file(p)
    return out


def build_rows(seed, n_per_form, split, pool_name="test"):
    if pool_name == "real":
        import pool_loader
        pool = pool_loader.load_real_pool()
    else:
        pool = make_testonly_pool()
    rows = []
    for form in FORMS:
        for sp in (("train", "dev") if split == "both" else (split,)):
            b = Builder("%s-%s-%s" % (seed, form, sp), pool, allow=GenAllow(), provisional=True, mode="dry")
            got, i = 0, 0
            while got < n_per_form and i < n_per_form * 8:
                for r in b.unit(form, sp, i, pair_prob=0.35):
                    rows.append(r)
                    got += 1
                i += 1
    return rows


def run(rows):
    per_form = collections.OrderedDict()
    ans_classes = collections.defaultdict(lambda: collections.defaultdict(list))
    parse_classes = collections.defaultdict(lambda: collections.defaultdict(list))
    t0 = time.time()
    for r in rows:
        f = r["form"]
        pf = per_form.setdefault(f, collections.Counter())
        pf["rows"] += 1
        out = solve_row({k: r[k] for k in ("form", "k", "carrier", "stem", "options")})
        if out["status"] != "ok":
            cls = "b_%s:%s" % (out["status"], out["code"])
            ans_classes[f][cls].append(r["row_id"])
            pf[out["status"]] += 1
            continue
        if out["answer_index"] == r["label"]:
            pf["agree"] += 1
        else:
            pf["answer_mismatch"] += 1
            ans_classes[f]["answer_mismatch"].append(r["row_id"])
        a = canon.canonical_spec(r["spec"])
        d = []
        diff(a, out["parse"], "", f, d)
        if d:
            pf["parse_mismatch"] += 1
            for p in sorted(set(d)):
                parse_classes[f][p].append(r["row_id"])
        else:
            pf["parse_match"] += 1
    return per_form, ans_classes, parse_classes, time.time() - t0


def report(per_form, ans_classes, parse_classes):
    lines = []
    tot = collections.Counter()
    sub = collections.defaultdict(collections.Counter)
    sbmap = {"AR": "ARITH", "LG": "LOGIC", "CA": "CAUSAL", "TM": "TEMPORAL", "TB": "TABLE"}
    for f, c in per_form.items():
        tot.update(c)
        sub[sbmap[f[:2]]].update(c)
    lines.append("%-6s %6s %6s %7s %7s %6s %6s | agree%% of rows | parse-match%% of ok" % ("form", "rows", "agree", "ans_mis", "pfail", "rej", "pmis"))
    for f, c in per_form.items():
        ok = c["agree"] + c["answer_mismatch"]
        lines.append("%-6s %6d %6d %7d %7d %6d %6d | %6.2f%%        | %6.2f%%" % (
            f, c["rows"], c["agree"], c["answer_mismatch"], c["parse_fail"], c["reject"], c["parse_mismatch"],
            100.0 * c["agree"] / c["rows"], 100.0 * c["parse_match"] / max(1, ok)))
    lines.append("")
    for sb, c in sub.items():
        ok = c["agree"] + c["answer_mismatch"]
        lines.append("%-9s rows=%d agree=%d (%.3f%%) answer_mismatch=%d parse_fail=%d reject=%d parse_match=%d (%.3f%% of ok)" % (
            sb, c["rows"], c["agree"], 100.0 * c["agree"] / c["rows"], c["answer_mismatch"], c["parse_fail"], c["reject"], c["parse_match"],
            100.0 * c["parse_match"] / max(1, ok)))
    ok = tot["agree"] + tot["answer_mismatch"]
    lines.append("ALL       rows=%d agree=%d (%.3f%%) answer_mismatch=%d parse_fail=%d reject=%d parse_match=%d (%.3f%% of ok)" % (
        tot["rows"], tot["agree"], 100.0 * tot["agree"] / tot["rows"], tot["answer_mismatch"], tot["parse_fail"], tot["reject"], tot["parse_match"],
        100.0 * tot["parse_match"] / max(1, ok)))
    lines.append("")
    lines.append("ANSWER disagreement classes (form, class, count, up to 3 row ids)")
    for f, d in ans_classes.items():
        for cls, ids in sorted(d.items()):
            lines.append("  %-6s %-48s %5d  %s" % (f, cls, len(ids), ",".join(ids[:3])))
    lines.append("PARSE-BACK mismatch classes (form, path, count, up to 3 row ids)")
    for f, d in parse_classes.items():
        for p, ids in sorted(d.items()):
            lines.append("  %-6s %-56s %5d  %s" % (f, p, len(ids), ",".join(ids[:3])))
    return "\n".join(lines), tot


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-per-form", type=int, default=300)
    ap.add_argument("--seed", default="agree-1")
    ap.add_argument("--split", default="both", choices=["train", "dev", "both"])
    ap.add_argument("--pool", default="test", choices=["test", "real"], help="test = the TEST-ONLY wording pool, real = pools/*.json")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    if os.path.abspath(args.out).startswith(os.path.abspath(HERE)) and "reports" not in os.path.abspath(args.out):
        print("refusing to write into the generator directory; use a temp dir or solver_b/reports")
        return 2
    os.makedirs(args.out, exist_ok=True)
    rows = build_rows(args.seed, args.n_per_form, args.split, args.pool)
    per_form, ans_classes, parse_classes, secs = run(rows)
    text, tot = report(per_form, ans_classes, parse_classes)
    print(text)
    shas = collect_shas()
    rep = {"seed": args.seed, "n_per_form": args.n_per_form, "split": args.split, "rows": len(rows), "seconds_b": round(secs, 1),
           "per_form": dict((f, dict(c)) for f, c in per_form.items()),
           "answer_classes": dict((f, dict((k, {"n": len(v), "ids": v[:3]}) for k, v in d.items())) for f, d in ans_classes.items()),
           "parse_classes": dict((f, dict((k, {"n": len(v), "ids": v[:3]}) for k, v in d.items())) for f, d in parse_classes.items()),
           "file_sha256": shas}
    with open(os.path.join(args.out, "agree_%s.json" % args.seed), "w") as fh:
        json.dump(rep, fh, indent=1, sort_keys=True)
    with open(os.path.join(args.out, "agree_%s.txt" % args.seed), "w") as fh:
        fh.write(text + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
