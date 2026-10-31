"""Shared helpers for the G-block text build (A39 b): fetch, clean, PII screen, English check, dedupe, write.

Run every tool with `python -I`. Downloads are data, never code.
"""
import hashlib
import html
import json
import random
import re
import ssl
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/gblock")
RAW = ROOT / "raw"
TEXTS = ROOT / "texts"
AUDIT = ROOT / "audit"
try:
    import certifi
    _CTX = ssl.create_default_context(cafile=certifi.where())
except Exception:  # noqa: BLE001
    _CTX = ssl.create_default_context()
UA = "OpenDecide-gblock-builder/0.1 (research dataset build; low rate)"
MIN_W, MAX_W = 40, 400
TARGET = 2500


def fetch(url, data=None, tries=4, sleep=1.0, headers=None, timeout=60):
    h = {"User-Agent": UA, "Accept": "application/json"}
    h.update(headers or {})
    i = 0
    while True:
        try:
            req = urllib.request.Request(url, data=data, headers=h)
            with urllib.request.urlopen(req, timeout=timeout, context=_CTX) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429 and i < 12:
                ra = e.headers.get("retry-after") or "30"
                time.sleep((float(ra) if ra.replace(".", "").isdigit() else 30) + 2)
                i += 1
                continue
            if e.code >= 500 and i < tries:
                time.sleep(sleep * (2 ** i) + random.random())
                i += 1
                continue
            raise
        except Exception:  # noqa: BLE001
            if i >= tries:
                raise
            time.sleep(sleep * (2 ** i) + random.random())
            i += 1


def fetch_json(url, **kw):
    return json.loads(fetch(url, **kw).decode("utf-8"))


_TAG = re.compile(r"<[^>]+>")


def strip_html(s, drop_blocks=("pre", "code", "script", "style", "aside", "blockquote", "table")):
    s = s or ""
    for b in drop_blocks:
        s = re.sub(rf"(?is)<{b}\b[^>]*>.*?</{b}>", " ", s)
    s = re.sub(r"(?i)<br\s*/?>", "\n", s)
    s = re.sub(r"(?i)</(p|div|li|h\d|tr)>", "\n", s)
    s = re.sub(r"(?i)<li[^>]*>", "\n- ", s)
    s = _TAG.sub(" ", s)
    return html.unescape(s)


def clean_ws(s):
    s = unicodedata.normalize("NFKC", s or "")
    s = s.replace("\u00a0", " ").replace("\u200b", "")
    s = re.sub(r"[ \t\r\f\v]+", " ", s)
    s = re.sub(r" *\n *", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def nwords(s):
    return len(s.split())


_SENT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])")


def trim_words(s, max_w=MAX_W):
    """Trim to <= max_w words at a sentence (else paragraph) boundary; '' if no clean cut >= MIN_W."""
    if nwords(s) <= max_w:
        return s
    out, n = [], 0
    for p in s.split("\n"):
        k = nwords(p)
        if n + k <= max_w:
            out.append(p)
            n += k
            continue
        part = []
        for st in _SENT.split(p):
            k2 = nwords(st)
            if n + k2 > max_w:
                break
            part.append(st)
            n += k2
        if part:
            out.append(" ".join(part))
        break
    t = clean_ws("\n".join(out))
    return t if nwords(t) >= MIN_W else ""


EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE = re.compile(r"(?<!\d)(\+?\d{1,2}[\s.-]?)?(\(\d{3}\)|\d{3})[\s.-]\d{3}[\s.-]\d{4}(?!\d)")
USERPATH = re.compile(r"(?i)(c:\\users\\|/home/|/users/)[^\s\\/]+")
HANDLE = re.compile(r"(?<![\w@])@[A-Za-z0-9_][A-Za-z0-9_.-]{1,30}")
URL = re.compile(r"https?://\S+|www\.\S+")
IP = re.compile(r"\b\d{1,3}(\.\d{1,3}){3}\b")


def pii_reason(s):
    if EMAIL.search(s):
        return "email"
    if PHONE.search(s):
        return "phone"
    if USERPATH.search(s):
        return "user_path"
    if IP.search(s):
        return "ip"
    return None


_EN = set("the of and to in is that for it with as on was be are this by at from or have an not which but can you your".split())


def is_english(s, min_ratio=0.08):
    ws = re.findall(r"[A-Za-z']+", s.lower())
    if len(ws) < 20:
        return False
    letters = [ch for ch in s if ch.isalpha()]
    ascii_share = sum(ch.isascii() for ch in letters) / max(1, len(letters))
    if ascii_share < 0.97:
        return False
    return sum(w in _EN for w in ws) / len(ws) >= min_ratio


def words_norm(t):
    return re.findall(r"[^\W_]+", unicodedata.normalize("NFKC", t).lower())


class Deduper:
    """Exact (normalised) and near duplicate filter: drop a text if >= 50% of its word 8-grams were seen before."""

    def __init__(self, n=8, thr=0.5):
        self.n, self.thr = n, thr
        self.full = set()
        self.grams = set()

    def add(self, text):
        ws = words_norm(text)
        key = hashlib.sha1(" ".join(ws).encode()).digest()
        if key in self.full:
            return False
        gs = {hashlib.sha1(" ".join(ws[i:i + self.n]).encode()).digest()[:10] for i in range(max(1, len(ws) - self.n + 1))}
        if gs and len(gs & self.grams) / len(gs) >= self.thr:
            return False
        self.full.add(key)
        self.grams |= gs
        return True


def scrub_pii(t, extra=None):
    """Drop whole sentences that carry an email, phone number, user path or IP (or match `extra`)."""
    out = []
    for p in t.split("\n"):
        keep = [st for st in _SENT.split(p) if not pii_reason(st) and not (extra and extra.search(st))]
        if keep:
            out.append(" ".join(keep))
    return clean_ws("\n".join(out))


HONORIFIC_NAME = re.compile(r"\b(Mr|Mrs|Ms|Miss|Mx)\.? [A-Z][a-z]+")
SENSITIVE = re.compile(r"(?i)\b(alleg\w*|accused|charged with|arrest\w*|convicted|sentenced|pleaded|guilty|"
                       r"murder\w*|homicide|manslaughter|assault\w*|sexual\w*|harass\w*|victim\w*|suspect\w*|"
                       r"died|death of|obituar\w*|funeral|condolence\w*|missing person|inquest|lawsuit|sued|"
                       r"custody|overdose|suicide|abuse\w*|board of inquiry|human rights complaint|stabb\w*|"
                       r"shot dead|shooting|killed|kidnap\w*|rape\w*|trial|testif\w*|jailed|prison\w*)\b")


def private_person_risk(t):
    """News-like text: drop if it names someone with an honorific or is about crime, courts, deaths or abuse
    (the contexts where a private person's data is most likely)."""
    return bool(HONORIFIC_NAME.search(t) or SENSITIVE.search(t))


def finish(domain, source, licence_url, items, seed=20261013, target=TARGET, prefix=None, audit_fields=None,
           scrub_extra=None, drop_fn=None, fix_fn=None):
    """items: list of dicts {key, text, meta}. Clean, screen, dedupe, sample <= target, write texts + audit.
    Returns a stats dict."""
    rng = random.Random(seed)
    rng.shuffle(items)
    stats = {"candidates": len(items), "too_short": 0, "too_long_untrimmable": 0, "pii": 0, "not_english": 0,
             "dup": 0, "kept": 0}
    dd = Deduper()
    keep = []
    for it in items:
        t = clean_ws(it["text"])
        t = URL.sub("", t)
        t = HANDLE.sub("", t)
        t = clean_ws(t)
        t = scrub_pii(t, scrub_extra)
        if fix_fn:
            t = clean_ws(fix_fn(t))
        if drop_fn and drop_fn(t):
            stats["private_person_risk"] = stats.get("private_person_risk", 0) + 1
            continue
        if nwords(t) < MIN_W:
            stats["too_short"] += 1
            continue
        if nwords(t) > MAX_W:
            t = trim_words(t)
            if not t:
                stats["too_long_untrimmable"] += 1
                continue
        if pii_reason(t):
            stats["pii"] += 1
            continue
        if not is_english(t):
            stats["not_english"] += 1
            continue
        if not dd.add(t):
            stats["dup"] += 1
            continue
        keep.append((it, t))
        if len(keep) >= target:
            break
    prefix = prefix or domain
    out_dir = TEXTS / domain
    out_dir.mkdir(parents=True, exist_ok=True)
    AUDIT.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "texts.jsonl", "w") as f, open(AUDIT / f"{domain}_meta.jsonl", "w") as fa:
        for i, (it, t) in enumerate(keep):
            tid = f"{prefix}_{i:05d}"
            f.write(json.dumps({"text_id": tid, "domain": domain, "source": source,
                                "licence_url": it.get("licence_url") or licence_url,
                                "text": t}, ensure_ascii=False) + "\n")
            fa.write(json.dumps({"text_id": tid, "upstream_key": it.get("key"), **(it.get("meta") or {})},
                                ensure_ascii=False) + "\n")
    stats["kept"] = len(keep)
    wc = [nwords(t) for _, t in keep]
    if wc:
        wc.sort()
        stats["words_min_med_max"] = [wc[0], wc[len(wc) // 2], wc[-1]]
    (out_dir / "build_stats.json").write_text(json.dumps({"domain": domain, "source": source,
                                                          "licence_url": licence_url, **stats}, indent=1))
    return stats


def save_raw(name, rows):
    d = RAW / name
    d.mkdir(parents=True, exist_ok=True)
    with open(d / "raw.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def load_raw(name):
    p = RAW / name / "raw.jsonl"
    if not p.exists():
        return None
    return [json.loads(l) for l in open(p) if l.strip()]
