"""g13_dev_frame_diag.py: evidence for the G13 c2_mixdev drop pattern (16 Oct 2026; read-only, CPU, no network).
Run from lean/:  ../.venv/bin/python -B c2_build/zed_orch/g13_dev_frame_diag.py T06 T07 ...
For each T-family block it takes the shared items between the block's candidates (state) and ALL C2 mixdev rows
(state): word 10-grams, >=5-word segments, >=5-word options (the decontam_g13 normaliser). It reports the units hit, the
units whose every shared item is (A) asset-independent (appears in training units spanning >= 5 distinct skin / wording /
card / pack values of that family) and/or (C) tiled by the family's program literals (plugin / vocab / fixtures strings cut
at placeholders; spans of >= 2 words, single words only at the item's edges or as a whole literal), and the residual.
It does not reproduce tulu8 / MinHash / embed on states (G13 does). Prints only C2-side text.
"""
import sys
argv=sys.argv[1:]
import json, re, sys, unicodedata, glob, os
from pathlib import Path
from collections import Counter, defaultdict
sys.path.insert(0, "c_build")
import decontam_g13 as g
_W = re.compile(r"[^\W_]+"); SEG = re.compile(r"(?<=[.!?])\s+|\n+")
PH = re.compile(r"\{[^{}]*\}|%\(\w+\)[sd]|%[sd]")
def words(t): return _W.findall(unicodedata.normalize("NFKC", t).lower())
def J(p): return [json.loads(l) for l in open(p)]
def segs(t):
    for s in SEG.split(t):
        w=words(s)
        if len(w)>=5: yield " ".join(w)
def grams(w,n=10):
    for i in range(len(w)-n+1): yield tuple(w[i:i+n])
mixfiles = sorted(glob.glob("data/c2_mixdev.jsonl")+glob.glob("data/c2_parts/*/out/mixdev_S5.jsonl"))
mix=[]
for p in mixfiles: mix += J(p)
E_seg=set(); E_ng=set(); E_opt=set()
for r in mix:
    w=words(r['state']); E_ng|=set(grams(w)); E_seg|=set(segs(r['state']))
    for o in (r.get('options') or []):
        ow=words(o)
        if len(ow)>=5: E_opt.add(" ".join(ow))
CODE=("plugin.py","vocab.py","fixtures.py","builder.py","sources.py","polarity.py","select.py")
def prog_pieces(fam):
    d=Path("c2_build/families")/fam; pcs=[]
    for n in CODE:
        p=d/n
        if p.is_file():
            for t,ln,rt in g._seed_texts(p):
                for piece in PH.split(t):
                    w=words(piece)
                    if w: pcs.append(w)
    return pcs
def pool_pieces(fam):
    d=Path("c2_build/families")/fam/"pools_v2"
    if not d.is_dir(): d=Path("c2_build/families")/fam/"pools"
    pcs=[]
    for p in sorted(d.rglob("*")):
        if p.suffix not in (".jsonl",".json",".txt") or g.SEED_SKIP.search(p.name): continue
        for t,ln,rt in g._seed_texts(p):
            for piece in PH.split(t):
                w=words(piece)
                if w: pcs.append(w)
    return pcs

def assets(r):
    m=r['meta']; c=m.get('c2') or {}
    if isinstance(c,str): c={}
    return {"skin":c.get('skin_id'),"wording":m.get('wording_id'),"card":m.get('card_id'),"pack":m.get('domain_pack')}
out={}
for fam in argv:
    cand=J(f"data/c2_parts/{fam}/out/candidates_c2.jsonl")
    nunits=len({r['call_id'] for r in cand})
    P=prog_pieces(fam)
    spans=set(); whole=set(); 
    for w in P:
        whole.add(tuple(w))
        for L in range(2,min(len(w),10)+1):
            for i in range(len(w)-L+1): spans.add(tuple(w[i:i+L]))
    Pbig=" "+" | ".join(" ".join(w) for w in P)+" "
    def span_ok(t,edge):
        L=len(t)
        if L==1: return edge or (t in whole)
        if L<=10: return t in spans
        return (" "+" ".join(t)+" ") in Pbig
    memo={}
    def tiled(words_):
        key=tuple(words_)
        if key in memo: return memo[key]
        n=len(key); ok=[False]*(n+1); ok[0]=True
        for j in range(1,n+1):
            for i in range(j):
                if ok[i] and span_ok(key[i:j], i==0 or j==n): ok[j]=True; break
        memo[key]=ok[n]; return ok[n]
    iu=defaultdict(set); iv=defaultdict(lambda: defaultdict(set))
    for r in cand:
        a=assets(r); u=r['call_id']; w=words(r['state'])
        items=[("ng"," ".join(x)) for x in set(grams(w)) if x in E_ng]+[("seg",s) for s in set(segs(r['state'])) if s in E_seg]
        for o in (r.get('options') or []):
            ow=" ".join(words(o))
            if len(ow.split())>=5 and ow in E_opt: items.append(("opt",ow))
        for it in items:
            iu[it].add(u)
            for d,v in a.items(): iv[it][d].add(v)
    ndist={d:len({assets(r)[d] for r in cand}-{None}) for d in ("skin","wording","card","pack")}
    def indep(it,K=5):
        return all(n<2 or len(iv[it][d]-{None})>=min(K,n) for d,n in ndist.items())
    ui=defaultdict(list)
    for it,us in iu.items():
        for u in us: ui[u].append(it)
    tl={it:tiled(it[1].split()) for it in iu}
    ind={it:indep(it) for it in iu}
    def resid(fn): return sum(1 for u,its in ui.items() if any(not fn(it) for it in its))
    res={"hit":len(ui),"A indep5":resid(lambda i:ind[i]),"C tiled":resid(lambda i:tl[i]),"A or C":resid(lambda i:ind[i] or tl[i])}
    ri=Counter({it:len(iu[it]) for it in iu if not (ind[it] or tl[it])})
    out[fam]={"units":nunits,**res,"top_resid":[(k,s[:90],v) for (k,s),v in ri.most_common(3)]}
    print(f"{fam}: units {nunits} {res}")
    for (k,s),v in ri.most_common(3): print(f"     [{k}] u={v}: {s[:100]}")

