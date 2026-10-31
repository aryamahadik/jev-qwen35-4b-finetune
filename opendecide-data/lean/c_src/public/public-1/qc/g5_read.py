#!/usr/bin/env python3
"""Independent public-1 G5 blind read helper (flag-only; QC agent, not the builder).
Sample: spec 8 sizes (100 per dataset, 300 for SQuAD 2.0), drawn by this checker from rows_r1 + reserve in sha256
order of ("public1-qc-g5", id). Shows only what the model sees: decoder_io.user_msg (cygnet, schema_branch_mark)
under a seeded random option order, plus the gold letter (so the reader can flag it). Never edits a row.
Usage: g5_read.py sample | measure | show <ds> <start> <count> | win <ds> <idx> [chars] | mark <ds> "i:v,..." | tally
show: lines already shown for this dataset (card, rules, markers) are not repeated; option lines always print.
win:  the question, options and gold of one sampled row plus the passage paragraphs of the SAME rendered prompt that
      share the most content words with the question and options (long articles; reading aid, text unchanged).
mark: record flag-only verdicts (ok | wrong | amb) to qc/g5_verdicts.jsonl; tally: counts per dataset vs the bar."""
import hashlib, json, random, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
P1 = HERE.parent
LEAN = P1.parents[2]
sys.path.insert(0, str(LEAN / "c_src/formats/formats-1"))
from fmt1 import card as fcard  # pinned decoder_io (sha checked)
N = {"c_pub_squad2": 300, "c_pub_musique": 100, "c_pub_2wiki": 100, "c_pub_quality": 100}
FILES = ["out/public1_rows_r1.jsonl", "out/public1_reserve.jsonl"]
import re
OPT = re.compile(r"^[A-Z]{1,2}\. ")
STOP = set("that this with from what which their there these those about into than then them they were have been when where whose would could should while being does other after before because between".split())

def rows():
    out = {}
    for f in FILES:
        for l in open(P1 / f):
            r = json.loads(l); r["_file"] = f; out[r["id"]] = r
    return out

def h(*a):
    return hashlib.sha256("|".join(map(str, a)).encode()).hexdigest()

def sample(rs):
    s = {}
    for ds, n in N.items():
        ids = sorted((i for i, r in rs.items() if r["source"] == ds), key=lambda i: h("public1-qc-g5", i))
        s[ds] = ids[:n]
    return s

def render(r):
    dio = fcard._dio(); dio.STYLE, dio.LAYOUT = "cygnet", "schema_branch_mark"
    lr = dio.as_letter_row(r)
    perm = list(range(len(lr["options"]))); random.Random(h("g5perm", r["id"])).shuffle(perm)
    msg = dio.user_msg(r, perm)
    chk = fcard.loader_check(r, perm=perm, check_rows=False)
    return msg, chk["gold_letter"]

if __name__ == "__main__":
    rs = rows(); sp = HERE / "g5_sample_qc.json"
    if sys.argv[1] == "sample":
        s = sample(rs); json.dump(s, open(sp, "w"), indent=0)
        b = json.load(open(P1 / "out/public1_g5_sample_ids.json"))
        print({ds: {"n": len(v), "in_rows_r1": sum(rs[i]["_file"].endswith("rows_r1.jsonl") for i in v),
                    "overlap_builder_list": len(set(v) & set(b[ds]["ids"]))} for ds, v in s.items()})
    elif sys.argv[1] == "measure":
        s = json.load(open(sp))
        for ds, v in s.items():
            L = [len(render(rs[i])[0]) for i in v]
            print(ds, "chars total", sum(L), "median", sorted(L)[len(L)//2], "max", max(L))
    elif sys.argv[1] == "show":
        ds, a, n = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
        seenp = HERE / "tmp" / f"g5_seen_{ds}.json"; seenp.parent.mkdir(exist_ok=True)
        seen = set(json.load(open(seenp))) if seenp.exists() and a > 0 else set()
        for k, i in enumerate(json.load(open(sp))[ds][a:a + n]):
            m, g = render(rs[i])
            out, mine = [], set()
            L = [x.strip() for x in m.splitlines() if x.strip()]
            fq = set()
            for j, x in enumerate(L):
                if OPT.match(x) and j and not OPT.match(L[j - 1]) and L[j - 1] != "Options:":
                    fq.add(L[j - 1])
                if x == "Options:" and j:
                    fq.add(L[j - 1])
            for x in m.splitlines():
                x = x.strip()
                if not x or x.startswith("Options: A.") or x in mine:
                    continue
                if OPT.match(x) or x.endswith("?") or x in fq or x not in seen:
                    out.append(x)
                seen.add(x); mine.add(x)
            print(f"=== #{a+k} {rs[i]['qtype']} GOLD={g} :: " + " / ".join(out))
        json.dump(sorted(seen), open(seenp, "w"))
    elif sys.argv[1] == "win":
        import math
        ds, idx = sys.argv[2], int(sys.argv[3]); budget = int(sys.argv[4]) if len(sys.argv) > 4 else 3500
        i = json.load(open(sp))[ds][idx]; r = rs[i]
        m, g = render(r)
        st = r["state"]
        rest = m.replace(st, " ") if st in m else m
        L = [x.strip() for x in rest.splitlines() if x.strip()]
        opts = [x for x in L if OPT.match(x)]
        qs = [x for x in L if x.startswith("Question about") or x.startswith("Based on") or x.endswith("?")
              or x.startswith("Read the whole") or x.startswith("Pick the")]
        ins = [x.strip() for x in re.split(r"\n\s*\n", r["instructions"]) if x.strip()]
        qs = qs + ([" ".join(ins[-1].split())] if ins else [])
        seenq = []
        for x in qs:
            if x not in seenq:
                seenq.append(x)
        print(f"=== #{idx} {r['meta'].get('twin_kind')} GOLD={g} :: " + " / ".join(seenq) + " || " + " | ".join(opts))
        words = set(w for w in re.findall(r"[a-z]{4,}", (" ".join(seenq[-2:] + opts)).lower()) if w not in STOP)
        ps = [p_ for p_ in re.split(r"\n\s*\n", st) if p_.strip()]
        chunks, cur = [], []
        for j, p_ in enumerate(ps):
            cur.append(j)
            if sum(len(ps[k]) for k in cur) >= 900:
                chunks.append(cur); cur = []
        if cur:
            chunks.append(cur)
        ctext = [" ".join(ps[k] for k in c).lower() for c in chunks]
        df = {w: sum(1 for t in ctext if w in t) for w in words}
        idf = {w: math.log((1 + len(chunks)) / (1 + df[w])) for w in words if df[w]}
        sc = sorted(((sum(v for w, v in idf.items() if w in t), ci) for ci, t in enumerate(ctext)), reverse=True)
        keep, tot = set(), 0
        for s_, ci in sc:
            ln = sum(len(ps[k]) for k in chunks[ci])
            if tot + ln > budget and keep:
                continue
            keep.add(ci); tot += ln
        print(f"[text: {len(ps)} paragraphs, {len(st)} chars; showing {len(keep)} of {len(chunks)} chunks]")
        for ci in sorted(keep):
            t = " ".join(" ".join(ps[k].split()) for k in chunks[ci])
            if len(t) > budget * 1.2:      # one huge paragraph: show the sentences that hold query words (+ next)
                sents = re.split(r"(?<=[.!?])\s+", t)
                top = sorted(idf, key=lambda w: -idf[w])[:12]
                pick = set()
                for j, se in enumerate(sents):
                    if any(w in se.lower() for w in top):
                        pick.update({j, j + 1})
                out, n = [], 0
                for j in sorted(pick):
                    if j < len(sents) and n + len(sents[j]) <= budget:
                        out.append(sents[j]); n += len(sents[j])
                t = " ... ".join(out)
            print(f"[c{ci}] " + t)
    elif sys.argv[1] == "kw":          # paragraphs of the SAME rendered text that contain given words (reading aid)
        ds, idx, kws = sys.argv[2], int(sys.argv[3]), [k.lower() for k in sys.argv[4].split(",")]
        budget = int(sys.argv[5]) if len(sys.argv) > 5 else 3000
        r = rs[json.load(open(sp))[ds][idx]]
        ps = [p_ for p_ in re.split(r"\n\s*\n", r["state"]) if p_.strip()]
        tot = 0
        for j, p_ in enumerate(ps):
            if any(k in p_.lower() for k in kws):
                t = " ".join(p_.split())
                if tot + len(t) > budget:
                    print("[budget reached]"); break
                print(f"[p{j}] {t}"); tot += len(t)
    elif sys.argv[1] == "titles":       # which paragraphs a row shows (headers only), for twin rows
        ds = sys.argv[2]
        for k in sys.argv[3].split(","):
            i = json.load(open(sp))[ds][int(k)]
            m, g = render(rs[i])
            hd = [x.strip()[:70] for x in m.splitlines() if re.match(r"\s*(<doc |\[\d+\] |## \d+\. |Paragraph \d+: |# Reference)", x)]
            print(f"#{k} GOLD={g} :: " + " | ".join(hd))
    elif sys.argv[1] == "mark":
        ds = sys.argv[2]; ids = json.load(open(sp))[ds]
        with open(HERE / "g5_verdicts.jsonl", "a") as f:
            for t in sys.argv[3].split(","):
                k, v = t.split(":")[:2]
                assert v in ("ok", "wrong", "amb", "unv"), v
                a, _, b = k.partition("-")
                for kk in range(int(a), int(b or a) + 1):
                    f.write(json.dumps({"ds": ds, "idx": kk, "id": ids[kk], "v": v}) + "\n")
    elif sys.argv[1] == "tally":
        last = {}
        for l in open(HERE / "g5_verdicts.jsonl"):
            x = json.loads(l); last[(x["ds"], x["idx"])] = x["v"]
        import collections
        c = collections.defaultdict(collections.Counter)
        for (ds, _), v in last.items():
            c[ds][v] += 1
        print({ds: dict(v) for ds, v in c.items()})
