"""VOICE agreement harness: solver A (verbalizer, span_check, wer: the lane's own) against solver B (VOICE/solver_b, blind).

    python3 agree_voice.py --out <temp dir> [--seed S] [--n-strings 1500] [--n-alter 2000] [--n-benign 1200] [--n-variants 6000]

Everything is generated IN MEMORY from the lane's TEST-ONLY scaffolding (planted.py, synthetic sources, TEST tables). No audio, no TTS,
no ASR, no real row. Only a counts report is written, into --out (use a temp dir). No utterance text is printed or stored.

Sections
  C1  V-C1 verbalizer round trip: B's denormaliser against the source tokens, on A's verbalizer output, per stratum.
  C4  V-C4 planted-edit suite: B's and A's recall on planted alterations (Wilson lower bound), false alarms on benign equivalents,
      A-versus-B verdict agreement (bar 99.5 percent), per planted-edit table.
  VAR A-versus-B verdicts on whole variants (generator-A style renderings and generator-B noised text, all four strata): agreement and
      disagreement classes; WER agreement (V-D7 style: median absolute difference, share within 0.5 pp) under B's two readings of SCHEMA
      section 4 (fine tokens = the literal reading, white-space tokens = what A charges), and WER-band agreement.
"""
import argparse
import collections
import hashlib
import json
import math
import os
import random
import statistics
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "GEN"))
sys.path.insert(0, os.path.join(HERE, "solver_b"))
sys.dont_write_bytecode = True

import disfluency as DF                         # noqa: E402  (solver A side)
import noiser as NS                             # noqa: E402
import planted as PT                            # noqa: E402
import span_check as SC                         # noqa: E402
import verbalizer as V                          # noqa: E402
import vcommon as C                             # noqa: E402
import wer as W                                 # noqa: E402
from gen_common import RowNamer                 # noqa: E402

import vb_check as BC                           # noqa: E402  (solver B)
import vb_wer as BW                             # noqa: E402
from vb_denorm import denormalise, DenormError  # noqa: E402

STRATA = ["V-NL", "V-DICT-LIT", "V-DICT-NAT", "V-NUM"]


def wilson_lower(k, n, z=1.96):
    if n == 0:
        return 0.0
    p = k / float(n)
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    a = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - a) / d


def sha_file(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def collect_shas():
    out = {}
    sb = os.path.join(HERE, "solver_b")
    for fn in sorted(os.listdir(sb)):
        if fn.endswith(".py"):
            out["solver_b/" + fn] = sha_file(os.path.join(sb, fn))
    out["agree_voice.py"] = sha_file(os.path.join(HERE, "agree_voice.py"))
    for fn in ("verbalizer.py", "planted.py", "span_check.py", "wer.py", "numwords.py", "noiser.py", "disfluency.py", "vcommon.py"):
        out["A:" + fn] = sha_file(os.path.join(HERE, fn))
    return out


# ---------------------------------------------------------------------------------------------------------------------
# C1

def section_c1(n_strings, seed):
    lex = C.test_lexicon()
    vb = V.Verbalizer(lex)
    rng = random.Random(seed)
    strings = PT.verbalizer_test_strings(n_strings, seed=seed)
    res = collections.OrderedDict()
    for st in STRATA:
        r = collections.Counter()
        styles = collections.Counter()
        for s in strings:
            try:
                d = vb.verbalize(s, [], st, rng)
            except Exception:
                r["unbuildable_strings"] += 1
                continue
            r["strings"] += 1
            want = [t.lower() for t in d["source_tokens"]]
            r["tokens"] += len(want)
            try:
                got = denormalise(V.public_view(d))
            except DenormError:
                r["b_error_strings"] += 1
                continue
            if len(got) != len(want):
                r["token_count_differs_strings"] += 1
                continue
            bad = [i for i in range(len(want)) if got[i] != want[i]]
            r["token_mismatches"] += len(bad)
            if bad:
                r["mismatch_strings"] += 1
                for i in bad[:3]:
                    sty = [g["style"] for g in d["segments"] if g["src"] == i]
                    styles[sty[0] if sty else "?"] += 1
        r["styles_of_mismatch"] = dict(styles)
        res[st] = dict(r)
    return res


# ---------------------------------------------------------------------------------------------------------------------
# C4

def section_c4(n_alter, n_benign, seed):
    cases = PT.planted_suite(n_alter, n_benign, seed)
    per_edit = collections.OrderedDict()
    tot = collections.Counter()
    dis = collections.Counter()
    for c in cases:
        kb = BC.check(c["doc"], c["hyp"])
        ka = SC.check_doc(c["doc"], c["hyp"])["kept"]
        e = per_edit.setdefault(c["edit"], collections.Counter())
        e["n"] += 1
        e["expect_kept"] += c["expect_kept"]
        e["A_kept"] += ka
        e["B_kept"] += kb
        tot["n"] += 1
        tot["agree"] += (ka == kb)
        if not c["expect_kept"]:
            tot["alter"] += 1
            tot["A_dropped"] += (not ka)
            tot["B_dropped"] += (not kb)
        else:
            tot["benign"] += 1
            tot["A_false_alarm"] += (not ka)
            tot["B_false_alarm"] += (not kb)
        if ka != kb:
            dis[(c["edit"], "A_kept" if ka else "A_dropped")] += 1
    out = {"n": tot["n"], "alterations": tot["alter"], "benign": tot["benign"],
           "agreement": tot["agree"] / float(tot["n"]),
           "B_recall": tot["B_dropped"] / float(max(1, tot["alter"])), "B_recall_wilson_lower": wilson_lower(tot["B_dropped"], tot["alter"]),
           "A_recall": tot["A_dropped"] / float(max(1, tot["alter"])), "A_recall_wilson_lower": wilson_lower(tot["A_dropped"], tot["alter"]),
           "B_false_alarm": tot["B_false_alarm"] / float(max(1, tot["benign"])), "A_false_alarm": tot["A_false_alarm"] / float(max(1, tot["benign"])),
           "disagreement_classes": dict(("%s|%s" % k, v) for k, v in dis.items()),
           "per_edit": dict((k, dict(v)) for k, v in per_edit.items())}
    return out


# ---------------------------------------------------------------------------------------------------------------------
# VAR

def section_var(n_variants, seed):
    table = NS.ConfusionTable({"version": 1, "key_source": "identity", "source": "TEST-ONLY", "n_ref": 1, "dels": {}, "ins": {},
                               "homophones": NS.TEST_HOMOPHONES,
                               "subs": {"delete": [["deleted", 3]], "cache": [["cash", 5]], "folder": [["holder", 2]], "build": [["built", 4]]}})
    rng = random.Random(seed)
    tot = collections.Counter()
    by = collections.OrderedDict()
    dis = collections.Counter()
    wd_fine, wd_coarse = [], []
    wer_over = collections.Counter()
    band_dis = collections.Counter()
    for k in range(n_variants):
        namer = RowNamer("var-%s-%d" % (seed, k))
        stratum = STRATA[(k // 2) % len(STRATA)]
        doc = PT.make_doc(rng, namer, k, stratum)
        doc, _ops = DF.apply_disfluency(doc, DF.TEST_TABLE, rng)
        gen = "A" if k % 2 == 0 else "B"
        if gen == "A":
            hyp = PT.join_chunks(PT.render_chunks(doc, rng), rng)
        else:
            p = rng.choice([0.03, 0.08, 0.15, 0.3])
            hyp, _ = NS.noise_doc(doc, p, table, rng)
        ra = SC.check_doc(doc, hyp)
        rb = BC.check_detail(doc, hyp)
        key = (gen, stratum)
        c = by.setdefault(key, collections.Counter())
        c["n"] += 1
        c["agree"] += (ra["kept"] == rb["kept"])
        c["A_kept"] += ra["kept"]
        c["B_kept"] += rb["kept"]
        if ra["kept"] != rb["kept"]:
            dis[(gen, stratum, "A_kept" if ra["kept"] else "A_dropped", ",".join(sorted(set(rb["reasons"] or ra["reasons"]))))] += 1
        wf = BW.wer(doc, hyp, fine=True)
        wc = BW.wer(doc, hyp, fine=False)
        wd_fine.append(abs(wf - ra["wer"]))
        wd_coarse.append(abs(wc - ra["wer"]))
        ba, bb = W.band_of(ra["wer"]), BW.band_of(wc)
        c["band_agree_coarse"] += (ba == bb)
        c["band_agree_fine"] += (ba == BW.band_of(wf))
        if abs(wc - ra["wer"]) > 0.005:
            wer_over[(gen, stratum)] += 1
            # diagnostic only (not part of B's definition): does collapsing adjacent doubled hypothesis words reconcile B with A?
            toks = hyp.split()
            collapsed = " ".join(t for i, t in enumerate(toks) if i == 0 or t.lower() != toks[i - 1].lower())
            tot["over_0.5pp"] += 1
            if abs(BW.wer(doc, collapsed, fine=False) - ra["wer"]) <= 0.005:
                tot["over_0.5pp_reconciled_by_collapsing_doubled_hyp_words"] += 1
    n = sum(c["n"] for c in by.values())
    ag = sum(c["agree"] for c in by.values())

    def stats(v):
        v = sorted(v)
        return {"median": statistics.median(v), "p95": v[int(0.95 * (len(v) - 1))], "p99": v[int(0.99 * (len(v) - 1))], "max": v[-1],
                "share_within_0.5pp": sum(1 for x in v if x <= 0.005) / float(len(v)),
                "share_within_1pp": sum(1 for x in v if x <= 0.01) / float(len(v))}
    return {"n": n, "verdict_agreement": ag / float(n),
            "by_generator_stratum": dict(("%s|%s" % k, dict(v)) for k, v in by.items()),
            "disagreement_classes": dict(("|".join(k), v) for k, v in dis.items()),
            "wer_abs_diff_fine_tokens": stats(wd_fine), "wer_abs_diff_whitespace_tokens": stats(wd_coarse),
            "wer_over_0.5pp_whitespace_by_class": dict(("%s|%s" % k, v) for k, v in wer_over.items()),
            "wer_over_0.5pp_diagnostic": {"cases": tot["over_0.5pp"],
                                          "reconciled_by_collapsing_doubled_hyp_words": tot["over_0.5pp_reconciled_by_collapsing_doubled_hyp_words"]},
            "band_agreement_whitespace": sum(c["band_agree_coarse"] for c in by.values()) / float(n),
            "band_agreement_fine": sum(c["band_agree_fine"] for c in by.values()) / float(n)}


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--n-strings", type=int, default=1500)
    ap.add_argument("--n-alter", type=int, default=2000)
    ap.add_argument("--n-benign", type=int, default=1200)
    ap.add_argument("--n-variants", type=int, default=6000)
    args = ap.parse_args(argv)
    if os.path.abspath(args.out).startswith(os.path.abspath(HERE)) and "reports" not in os.path.abspath(args.out):
        print("refusing to write into the lane directory; use a temp dir or solver_b/reports")
        return 2
    os.makedirs(args.out, exist_ok=True)
    t0 = time.time()
    rep = {"seed": args.seed}
    rep["C1_verbalizer_round_trip"] = section_c1(args.n_strings, args.seed)
    rep["C4_planted_suite"] = section_c4(args.n_alter, args.n_benign, args.seed)
    rep["VAR_variants"] = section_var(args.n_variants, args.seed)
    rep["seconds"] = round(time.time() - t0, 1)
    rep["file_sha256"] = collect_shas()
    with open(os.path.join(args.out, "agree_voice_seed%d.json" % args.seed), "w") as fh:
        json.dump(rep, fh, indent=1, sort_keys=True)
    print(json.dumps(rep, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
