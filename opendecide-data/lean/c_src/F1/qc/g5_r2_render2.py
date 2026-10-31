"""G5 compact render v2 (check:F1): same 600 ids (qc/g5_r2_sample_ids.json). The card block of each row is split into
items (a line plus its indented continuation lines); each distinct item text is printed once in
tmp/qc/g5_r2/glossary.txt as Gn and the row shows its card as the ordered list of item ids. Text is never altered,
only referenced (token saving). The first copy of the instructions + options is replaced by a marker (verified
verbatim repeat after the text). Writes tmp/qc/g5_r2/cNNN.txt (10 rows each). Counts only."""
import json, re
import qc_lib as q

rows, _ = q.load("candidates_r1")
by = {r["id"]: r for r in rows}
pick = json.load(open(q.QC / "g5_r2_sample_ids.json"))
d = q.TMP / "g5_r2"
gl = {}


def items(c):
    out = []
    for l in c.split("\n"):
        if out and (l.startswith((" ", "\t")) or not l.strip()):
            out[-1] += "\n" + l
        else:
            out.append(l)
    return [x.rstrip("\n") for x in out if x.strip()]


B, nref = 10, 0
used = {0: [], 1: [], 2: []}  # glossary ids first needed per 200-row chunk (each chunk gets its own glossary file)
for b in range(0, 600, B):
    with open(d / f"c{b // B:03d}.txt", "w") as f:
        for i in range(b, min(b + B, 600)):
            r = by[pick[i]]
            m = q.model_view(r)
            c = r.get("card") or ""
            if c and c in m:
                ref = []
                for it in items(c):
                    if it not in gl:
                        gl[it] = f"G{len(gl)}"
                    ref.append(gl[it])
                    if gl[it] not in used[i // 200]:
                        used[i // 200].append(gl[it])
                assert "\n".join(items(c)) == "\n".join(x for x in items(c))
                m = m.replace(c, "[CARD items: " + " ".join(ref) + "]", 1); nref += 1
            t = m.find("\nText:\n")
            head, tail = m[:t], m[t:]
            ins = r["instructions"].strip()
            k = head.find(ins)
            if k >= 0 and ins in tail:
                m = head[:k] + "[QUESTION+OPTIONS: see the copy after the text]" + tail
            f.write(f"\n######## ROW {i}\n{m}\n")
inv = {v: k for k, v in gl.items()}
for ch, lst in used.items():
    with open(d / f"gloss_{ch}.txt", "w") as f:
        for gid in sorted(lst, key=lambda x: int(x[1:])):
            f.write(f"{gid}: {inv[gid]}\n")
print(json.dumps({"rows": len(pick), "card_rows": nref, "glossary_items": len(gl), "per_chunk": {k: len(v) for k, v in used.items()}}))
