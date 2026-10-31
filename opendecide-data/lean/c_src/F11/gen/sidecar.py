"""S7 cap-class sidecar (G0 S7, K07 / X2): one line per real-text row {id, dataset, scheme, record_id, cap_class}
next to each output file (out/<name>.sidecar.jsonl). Never in meta.

Cap class: MAMS ACSA (named category, its polarity); MAMS ATSA (named target's polarity); XED each emotion in the
line's set (the row counts once toward each). Read from the output rows and the pinned records file (s7b loader).
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import lex  # noqa: E402
import s7b  # noqa: E402
from check import strip_question_block  # noqa: E402
from common import OUT, progress  # noqa: E402

NAMES = ("candidates_r1", "qc_sample", "mixdev_S5")
TG = {"aspect": "mams_acsa", "target": "mams_atsa"}


def target_of(question):
    for qk in [k for k in lex.Q if k.startswith("s7_") and k.endswith("_mams")]:
        pat = re.escape(lex.Q[qk])
        for ph, rx in (("{K}", r"(?P<K>.+?)"), ("{T}", r"(?P<T>.+?)"), ("{target}", r"(?P<tg>\w+)")):
            pat = pat.replace(re.escape(ph), rx)
        m = re.fullmatch(pat, question)
        if m:
            return m.group("tg"), m.group("T")
    raise ValueError("no MAMS question frame")


def main():
    for name in NAMES:
        out, cc = [], Counter()
        for line in open(OUT / f"{name}.jsonl"):
            r = json.loads(line)
            ts = r["meta"].get("text_source")
            if not ts:
                continue
            rid = ts["record_id"]
            if ts["dataset"] == "xed_en":
                rec = s7b.loader("xed")[0][str(rid)]
                scheme, cls = "xed", [f"xed:{e}" for e in sorted(rec["ann"]["emotions"])]
            else:
                _, q = strip_question_block(r["instructions"])
                tg, T = target_of(q)
                scheme = TG[tg]
                comb, _ = s7b.annotation(scheme, rid, T)
                cls = [f"mams_acsa:{T}:{comb[0]}"] if scheme == "mams_acsa" else [f"mams_atsa:{comb[0]}"]
            out.append({"id": r["id"], "dataset": ts["dataset"], "scheme": scheme, "record_id": str(rid),
                        "cap_class": cls})
            cc.update(cls)
        with open(OUT / f"{name}.sidecar.jsonl", "w") as f:
            for x in out:
                f.write(json.dumps(x, ensure_ascii=False) + "\n")
        progress(f"sidecar {name}: {len(out)} real-text rows, {len(cc)} cap classes, max per class "
                 f"{max(cc.values()) if cc else 0}")
        print(name, len(out), "classes", len(cc), "max", cc.most_common(1))


if __name__ == "__main__":
    main()
