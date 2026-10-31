"""3.1 'unused records only' + Wikipedia passage dedup (C_DATA_SPEC v4 3.1), independent re-run on the CURRENT rows,
reserve and dev against C1's golden_train (data/v14_parts/golden_train.jsonl, read by program; the allow-listed file).
Uses public-2's own normaliser / unit / n-gram helpers (p2_common.norm, text_units, ngrams; read, unchanged).
Gated (the builder's documented final-file rules, finalize.py step 3, v1.1):
  - rendered state: a line / sentence unit of >= 8 normalised words equal to one in any golden_train state: 0 rows;
  - rendered state: a 10-gram shared with the named C1 sources (qnli, gd_answer_equiv, gd_hotpotqa_yesno, gd_feverous,
    gd_totto_claims, gd_wtq, boolq): 0 rows;
  - normalised state or normalised instructions equal to a golden_train state / instructions: 0 rows.
Reported: the same unit test at >= 5 words (the builder applied >= 5 to its canonical record text, not rebuilt here).
UCI rows are included (the builder skipped them). Streams golden_train once; memory = the public-2 side only."""
import hashlib
import json
import sys
from collections import Counter, defaultdict

from qclib import FILES, P2, load_all, write_gate

sys.path.insert(0, str(P2))
from p2_common import GOLDEN_TRAIN, NAMED_DEDUP_SOURCES, ngrams, norm, text_units  # noqa: E402


def h(s):
    return hashlib.blake2b(s.encode(), digest_size=8).digest()


def main():
    data = load_all()
    u8, u5, g10, st_eq, ins_eq = defaultdict(set), defaultdict(set), defaultdict(set), defaultdict(set), defaultdict(set)
    for fn in FILES:
        for r in data[fn]:
            rid = f"{fn}:{r['id']}"
            for u in set(text_units(r["state"], 5)):
                u5[h(u)].add(rid)
                if len(u.split()) >= 8:
                    u8[h(u)].add(rid)
            for g in set(ngrams(r["state"], 10)):
                g10[h(g)].add(rid)
            st_eq[h(norm(r["state"]))].add(rid)
            ins_eq[h(norm(r["instructions"]))].add(rid)
    hit = {k: set() for k in ("units8", "units5", "named10", "state_equal", "instructions_equal")}
    n = 0
    with open(GOLDEN_TRAIN) as f:
        for line in f:
            r = json.loads(line)
            st = r.get("state") or ""
            n += 1
            for u in set(text_units(st, 5)):
                k = h(u)
                if k in u5:
                    hit["units5"] |= u5[k]
                    if k in u8:
                        hit["units8"] |= u8[k]
            if r.get("source") in NAMED_DEDUP_SOURCES:
                for g in set(ngrams(st, 10)):
                    k = h(g)
                    if k in g10:
                        hit["named10"] |= g10[k]
            k = h(norm(st))
            if k in st_eq:
                hit["state_equal"] |= st_eq[k]
            k = h(norm(r.get("instructions") or ""))
            if k in ins_eq:
                hit["instructions_equal"] |= ins_eq[k]
    by = {k: dict(Counter(x.split(":")[0] + "|" + x.split(":")[1].split("_")[1] for x in v)) for k, v in hit.items()}
    nums = {"golden_train_rows_streamed": n, "rows_checked": sum(len(v) for v in data.values()),
            "rows_hit": {k: len(v) for k, v in hit.items()}, "rows_hit_by_file_dataset": by}
    ok = not (hit["units8"] or hit["named10"] or hit["state_equal"] or hit["instructions_equal"])
    write_gate("rules31_golden_train_dedup", ok, nums,
               hit_ids={k: sorted(v)[:15] for k, v in hit.items() if v})
    print("gt_dedup", ok, nums["rows_hit"])


if __name__ == "__main__":
    main()
