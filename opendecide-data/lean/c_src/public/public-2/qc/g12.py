"""G12 dedup (C_DATA_SPEC v4 8 G12), independent re-run over public-2's rows + reserve + dev together.
- exact hash: sha256 of the model-visible row (qtype, card, instructions, state, options): 0 duplicates;
- MinHash near-dups (datasketch, MIT): word 5-gram shingles of question + state + options (as the F8 / F11 checkers:
  the card is not part of the text; public-2 moved choice-row card text such as the UCI DEX model into
  `instructions`, so instruction LINES shared by >= 20 rows (card / template text) are left out of the question),
  128 permutations, LSH threshold 0.9, each candidate pair verified by exact shingle Jaccard >= 0.9; planned twins
  (shared group_id / call_id / twin_of) allowed; 'keep one' => 0 near-dup pairs may remain. The same test on the
  FULL text (instructions + state + options) is run and reported (report-only), every pair categorised;
- structure hash: one surface form per meta.structure_hash (no planned twins or format variants in public-2);
- also reported: rows sharing the same normalised question text + same record (re-asks)."""
import hashlib
import json
import re
from collections import Counter, defaultdict

from datasketch import MinHash, MinHashLSH

from qclib import FILES, load_all, write_gate


def norm(s):
    return re.sub(r"[^0-9a-z]+", " ", str(s).lower()).strip()


def near_dups(rows, text):
    lsh = MinHashLSH(threshold=0.9, num_perm=128)
    sh, mh, grp = {}, {}, {}
    for fn, r in rows:
        w = norm(text(r)).split()
        s = {" ".join(w[i:i + 5]) for i in range(max(1, len(w) - 4))}
        m = MinHash(num_perm=128)
        for g in s:
            m.update(g.encode())
        rid = f"{fn}:{r['id']}"
        sh[rid], mh[rid] = s, m
        grp[rid] = {r["group_id"], r["call_id"], str(r["meta"].get("twin_of"))}
        lsh.insert(rid, m)
    pairs, seen = [], set()
    for rid in sh:
        for o in lsh.query(mh[rid]):
            if o == rid or (o, rid) in seen:
                continue
            seen.add((rid, o))
            a, b = sh[rid], sh[o]
            j = len(a & b) / max(1, len(a | b))
            if j >= 0.9 and not ((grp[rid] & grp[o]) - {"None"}):
                pairs.append([rid, o, round(j, 3)])
    return pairs


def categorise(pairs, by):
    c = Counter()
    for a, b, _ in pairs:
        ra, rb = by[a], by[b]
        c["|".join([ra["source"][6:], ra["meta"]["framing"], "same_ins" if ra["instructions"] == rb["instructions"]
                    else "diff_ins", "same_state" if ra["state"] == rb["state"] else "diff_state",
                    "same_gold" if ra["gold"] == rb["gold"] else "diff_gold"])] += 1
    return dict(c)


def main():
    data = load_all()
    rows = [(fn, r) for fn in FILES for r in data[fn]]
    by = {f"{fn}:{r['id']}": r for fn, r in rows}
    lf = Counter(ln for _, r in rows for ln in set(r["instructions"].split("\n")))
    shared = {ln for ln, v in lf.items() if v >= 20}

    def q_text(r):
        q = "\n".join(ln for ln in r["instructions"].split("\n") if ln not in shared)
        return q + " " + r["state"] + " " + " ".join(r["options"] or [])
    full = near_dups(rows, lambda r: r["instructions"] + " " + r["state"] + " " + " ".join(r["options"] or []))
    pairs = near_dups(rows, q_text)
    ex = Counter()
    for _, r in rows:
        ex[hashlib.sha256(json.dumps([r["qtype"], r.get("card"), r["instructions"], r["state"], r["options"]],
                                     ensure_ascii=False).encode()).hexdigest()] += 1
    exact_dups = sum(v - 1 for v in ex.values() if v > 1)
    st = Counter(r["meta"]["structure_hash"] for _, r in rows)
    st_dups = {k: v for k, v in st.items() if v > 1}
    by_file_pairs = Counter(tuple(sorted((p[0].split(":")[0], p[1].split(":")[0]))) for p in pairs)
    nums = {"rows": len(rows), "exact_duplicates": exact_dups, "shared_instruction_lines_left_out": len(shared),
            "near_dup_pairs_jaccard_ge_0.9": len(pairs), "near_dup_pairs_by_kind": categorise(pairs, by),
            "report_only_full_text_pairs": len(full), "report_only_full_text_pairs_by_kind": categorise(full, by), "near_dup_pairs_by_files": {"&".join(k): v for k, v in by_file_pairs.items()},
            "structure_hash_shared": len(st_dups), "structure_hash_max_rows": max(st.values())}
    ok = exact_dups == 0 and not pairs and not st_dups
    write_gate("G12", ok, nums, near_dup_examples=pairs[:20], structure_dup_examples=list(st_dups.items())[:10])
    print("G12", ok, nums)


if __name__ == "__main__":
    main()
