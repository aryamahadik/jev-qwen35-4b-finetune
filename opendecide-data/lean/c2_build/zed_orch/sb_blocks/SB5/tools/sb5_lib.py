"""SB5 shared helpers (A58, UCI 293 Arabic tweet polarity). CPU only, deterministic, seed 20261013. Counts only on stdout."""
import gzip, hashlib, json, re, sys, unicodedata
from pathlib import Path

SB5 = Path(__file__).resolve().parent.parent
C2 = SB5.parent.parent.parent                    # lean/c2_build
LEAN = C2.parent
SEED = 20261013
ARCH = SB5 / "src/rar_out/Twitter"
WORK = SB5 / "work"
BENCH = Path("/Users/aryamahadik/Documents/jev/vision_bench")
sys.path.insert(0, str(C2))

def sha(s):
    return hashlib.sha256(s if isinstance(s, bytes) else s.encode()).hexdigest()

def h(*p):
    return int(sha("|".join(map(str, (SEED, *p)))), 16)

AR = re.compile(r"[؀-ۿݐ-ݿ]")
TASH = re.compile(r"[ً-ٰٟـ]")
URL = re.compile(r"https?://\S+|www\.\S+", re.I)
MENT = re.compile(r"@\w+")
TOK = re.compile(r"[^\W_]+")

def clean(t):
    t = unicodedata.normalize("NFC", t.replace("﻿", "").replace("\xa0", " "))
    return " ".join(t.split())

def norm_tokens(t):
    t = unicodedata.normalize("NFKC", t)
    t = URL.sub(" ", t); t = MENT.sub(" ", t); t = TASH.sub("", t)
    t = re.sub("[أإآٱ]", "ا", t).replace("ى", "ي").replace("ة", "ه")
    return TOK.findall(t.lower())

def grams(tok, n=5):
    return {" ".join(tok[i:i + n]) for i in range(len(tok) - n + 1)}

def load_archive():
    """-> list of {rid,label,text,enc,file_sha}; one tweet per file."""
    out = []
    for lab, d in (("pos", "Positive"), ("neg", "Negative")):
        for p in sorted((ARCH / d).glob("*.txt")):
            b = p.read_bytes()
            try:
                s, enc = b.decode("utf-8-sig"), "utf-8"
            except UnicodeDecodeError:
                s, enc = b.decode("cp1256"), "cp1256"
            out.append({"rid": p.stem, "label": lab, "text": clean(s), "enc": enc, "file_sha": sha(b)[:16]})
    return out

class Index:
    """Match index over segments: exact normalised string, 5-gram inverted index (Jaccard / containment)."""
    def __init__(self):
        self.exact, self.inv, self.segs = {}, {}, []
        self.n_seg = 0
    def add(self, name, text):
        tok = norm_tokens(text)
        if not tok or not AR.search(text):
            return
        self.n_seg += 1
        key = " ".join(tok)
        self.exact.setdefault(key, name)
        g = grams(tok)
        if g:
            i = len(self.segs); self.segs.append((name, g))
            for x in g:
                self.inv.setdefault(x, set()).add(i)
    def hit(self, text):
        tok = norm_tokens(text)
        if not tok:
            return None
        key = " ".join(tok)
        if key in self.exact:
            return ("exact", self.exact[key])
        g = grams(tok)
        if not g:
            return None
        cand = set()
        for x in g:
            cand |= self.inv.get(x, set())
        for i in cand:
            name, sg = self.segs[i]
            inter = len(g & sg)
            if inter / len(g | sg) >= 0.8:
                return ("near", name)
            if inter / min(len(g), len(sg)) >= 0.8:
                return ("contained", name)
        return None

def strings_of(o, out):
    if isinstance(o, str): out.append(o)
    elif isinstance(o, dict):
        for v in o.values(): strings_of(v, out)
    elif isinstance(o, list):
        for v in o: strings_of(v, out)
    return out

def segments(o):
    for s in strings_of(o, []):
        yield s
        if "\n" in s:
            for ln in s.splitlines():
                if ln.strip(): yield ln
