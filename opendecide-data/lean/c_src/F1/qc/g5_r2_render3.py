"""G5 compact render v3 (check:F1): same 600 ids (qc/g5_r2_sample_ids.json), model view only (decoder_io.user_msg,
cygnet + schema_branch_mark, canonical order). Token saving without changing meaning: card items lose their list /
numbering markers and separator style (format only); items whose normalised text occurs in >= 15% of the sampled
card rows are printed once in tmp/qc/g5_r2/std.txt as Sn and referenced by id + term; the rest are inline. The first
copy of the instructions + options (repeated verbatim after the text) is replaced by a marker. Writes
tmp/qc/g5_r2/dNNN.txt (10 rows each). Counts only."""
import json, re
from collections import Counter
import qc_lib as q

rows, _ = q.load("candidates_r1")
by = {r["id"]: r for r in rows}
pick = json.load(open(q.QC / "g5_r2_sample_ids.json"))
d = q.TMP / "g5_r2"
P = re.compile(r"^(?:\s*(?:[-*>•]|\d+(?:\.\d+)*[.)]?|Step \d+:|\(\d+\)|[a-z]\))\s+)+")
S = re.compile(r"^([A-Z][A-Za-z/ ()0-9'-]{1,40}?)\s*(?: = | \| | :: |: )")


def items(c):
    out = []
    for l in c.split("\n"):
        if out and (l.startswith((" ", "\t")) or not l.strip()):
            out[-1] += "\n" + l
        else:
            out.append(l)
    res = []
    for it in out:
        if not it.strip():
            continue
        ls = it.split("\n"); h = S.sub(lambda m: m.group(1) + ": ", P.sub("", ls[0].strip()))
        rest = [P.sub("", l.strip()) for l in ls[1:] if l.strip()]
        res.append("\n  ".join([h] + rest))
    return res


cards = {i: items(by[i]["card"]) for i in pick if by[i].get("card") and by[i]["card"] in q.model_view(by[i])}
freq = Counter(x for v in cards.values() for x in set(v))
std = {x: f"S{j}" for j, (x, n) in enumerate(sorted(((x, n) for x, n in freq.items() if n >= 0.15 * len(cards)),
                                                    key=lambda t: -t[1]))}
term = lambda x: x.split(":")[0][:28] if ":" in x[:45] else x[:28]
for b in range(0, 600, 10):
    with open(d / f"d{b // 10:03d}.txt", "w") as f:
        for i in range(b, b + 10):
            r = by[pick[i]]; m = q.model_view(r)
            if pick[i] in cards:
                its = cards[pick[i]]
                s_ref = " ".join(f"{std[x]}({term(x)})" for x in its if x in std)
                own = "\n".join(x for x in its if x not in std)
                m = m.replace(r["card"], f"[CARD; standard items: {s_ref}]\n{own}\n[END CARD]", 1)
            t = m.find("\nText:\n"); head, tail = m[:t], m[t:]
            ins = r["instructions"].strip(); k = head.find(ins)
            if k >= 0 and ins in tail:
                m = head[:k] + "[QUESTION+OPTIONS: see the copy after the text]" + tail
            f.write(f"\n######## ROW {i}\n{m}\n")
with open(d / "std.txt", "w") as f:
    for x, sid in std.items():
        f.write(f"{sid}: {x}\n")
print(json.dumps({"card_rows": len(cards), "std_items": len(std), "distinct_items": len(freq)}))
