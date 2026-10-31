"""Tiny dry run: build 20 in-memory voice examples from SYNTHETIC test sources (no real row, no audio, no TTS, no ASR).
Generator-A conditions are stood in for by the test ASR-style renderer in planted.py (equivalence-preserving forms) and generator B
by the confusion-table noiser with a TEST table. Prints one line each; never writes a file.
    python3 dryrun.py [--show]"""
import random
import sys

import disfluency as DF
import noiser as NS
import planted as PT
import span_check as SC
import wer as W
from gen_common import RowNamer
from vcommon import STRATA


def build_examples(n=20, seed="vdry-1"):
    rng = random.Random(seed)
    table = NS.ConfusionTable({"version": 1, "key_source": "identity", "source": "TEST-ONLY", "n_ref": 1, "dels": {}, "ins": {}, "homophones": NS.TEST_HOMOPHONES,
                               "subs": {"delete": [["deleted", 3]], "cache": [["cash", 5]], "folder": [["holder", 2]], "build": [["built", 4]]}})
    out = []
    for k in range(n):
        namer = RowNamer("%s-%d" % (seed, k))
        stratum = STRATA[:2][k % 2] if k % 5 else "V-NUM"
        doc = PT.make_doc(rng, namer, k, stratum)
        doc, ops = DF.apply_disfluency(doc, DF.TEST_TABLE, rng)
        gen = "A" if k % 2 == 0 else "B"
        if gen == "A":
            chunks = PT.render_chunks(doc, rng)
            hyp = PT.join_chunks(chunks, rng)
        else:
            hyp, _ = NS.noise_doc(doc, 0.06, table, rng)
        res = SC.check_doc(doc, hyp)
        out.append({"stratum": stratum, "generator": gen, "hyp": hyp, "ref": " ".join(doc["tokens"]), "wer": res["wer"], "band": W.band_of(res["wer"]),
                    "kept": res["kept"], "reasons": res["reasons"], "disfluency_ops": [o[0] for o in ops]})
    return out


def main(argv):
    ex = build_examples()
    for e in ex:
        print("%-10s gen=%s wer=%.3f band=%-4s kept=%-5s disfl=%s %s" % (e["stratum"], e["generator"], e["wer"], e["band"], e["kept"], ",".join(e["disfluency_ops"]) or "-", e["reasons"] or ""))
        if "--show" in argv:
            print("   REF", e["ref"])
            print("   HYP", e["hyp"])
    print("%d examples (TEST-ONLY sources; not rows; no audio)" % len(ex))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
