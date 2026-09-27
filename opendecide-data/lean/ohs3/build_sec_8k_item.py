#!/usr/bin/env python
"""OHS-3 part: sec_8k_item.

Task: which Form 8-K item does a (single-item) 8-K filing report under?

Source: SEC EDGAR Form 8-K filings (form type exactly "8-K"; amendments excluded) filed
2026-06-01..2026-09-26. The filing list and each filing's `items` field come from the EDGAR
full-text search index (efts.sec.gov/LATEST/search-index); the text comes from the filing's
primary document in sec.gov/Archives. Item titles and definitions come from the official SEC
Form 8-K (https://www.sec.gov/files/form8-k.pdf).

Network access happens only when the local snapshot under ohs3/cache/sec_8k_item/ is incomplete.
SEC fair-access rules require a User-Agent that names the requester and a contact address; it is
read from the environment variable SEC_USER_AGENT (e.g. "OpenDecide research you@example.org")
and never written to the outputs. Requests are throttled to <= 5 per second.
Re-runs on a complete snapshot use no network and give identical rows.

Seed 20261026.
"""
import datetime as dt
import difflib
import hashlib
import json
import os
import random
import re
import subprocess
import sys
import time
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import requests
from bs4 import BeautifulSoup

SEED = 20261026
TASK = "sec_8k_item"
N_ITEMS = 142
START, END = dt.date(2026, 6, 1), dt.date(2026, 9, 26)
MAX_CHARS = 6000
MIN_CHARS = 100          # stricter than the 20-char floor: need some body text
MIN_FILINGS = 5          # an item becomes an option with >= 5 filings (distinct CIKs)
MAX_OPTIONS, MIN_OPTIONS = 20, 3
MAX_SHARE = 0.40
INSTR = "Which Form 8-K item is this filing reported under?"

LEAN = Path(__file__).resolve().parents[1]
CACHE = LEAN / "ohs3" / "cache" / TASK
SEARCH_DIR = CACHE / "search"
DOC_DIR = CACHE / "docs"
FORM_PDF = CACHE / "form8-k.pdf"
DEFS_JSON = CACHE / "item_definitions.json"
MANIFEST = CACHE / "manifest.json"
OUT_DIR = LEAN / "data" / "ohs3_parts"
OUT_ROWS = OUT_DIR / f"{TASK}.jsonl"
OUT_SUMMARY = OUT_DIR / f"{TASK}_summary.json"

EFTS = "https://efts.sec.gov/LATEST/search-index"
FORM_URL = "https://www.sec.gov/files/form8-k.pdf"
LICENCE = ("Public domain / public record: SEC EDGAR filings and SEC.gov content (U.S. government "
           "website; EDGAR filings are public records freely redistributable). Attribution: SEC EDGAR.")

# Official item titles as printed in Form 8-K (cross-checked against the PDF at build time).
TITLES = {
    "1.01": "Entry into a Material Definitive Agreement",
    "1.02": "Termination of a Material Definitive Agreement",
    "1.03": "Bankruptcy or Receivership",
    "1.04": "Mine Safety - Reporting of Shutdowns and Patterns of Violations",
    "1.05": "Material Cybersecurity Incidents",
    "2.01": "Completion of Acquisition or Disposition of Assets",
    "2.02": "Results of Operations and Financial Condition",
    "2.03": "Creation of a Direct Financial Obligation or an Obligation under an Off-Balance Sheet Arrangement of a Registrant",
    "2.04": "Triggering Events That Accelerate or Increase a Direct Financial Obligation or an Obligation under an Off-Balance Sheet Arrangement",
    "2.05": "Costs Associated with Exit or Disposal Activities",
    "2.06": "Material Impairments",
    "3.01": "Notice of Delisting or Failure to Satisfy a Continued Listing Rule or Standard; Transfer of Listing",
    "3.02": "Unregistered Sales of Equity Securities",
    "3.03": "Material Modification to Rights of Security Holders",
    "4.01": "Changes in Registrant's Certifying Accountant",
    "4.02": "Non-Reliance on Previously Issued Financial Statements or a Related Audit Report or Completed Interim Review",
    "5.01": "Changes in Control of Registrant",
    "5.02": "Departure of Directors or Certain Officers; Election of Directors; Appointment of Certain Officers; Compensatory Arrangements of Certain Officers",
    "5.03": "Amendments to Articles of Incorporation or Bylaws; Change in Fiscal Year",
    "5.04": "Temporary Suspension of Trading Under Registrant's Employee Benefit Plans",
    "5.05": "Amendments to the Registrant's Code of Ethics, or Waiver of a Provision of the Code of Ethics",
    "5.06": "Change in Shell Company Status",
    "5.07": "Submission of Matters to a Vote of Security Holders",
    "5.08": "Shareholder Director Nominations",
    "6.01": "ABS Informational and Computational Material",
    "6.02": "Change of Servicer or Trustee",
    "6.03": "Change in Credit Enhancement or Other External Support",
    "6.04": "Failure to Make a Required Distribution",
    "6.05": "Securities Act Updating Disclosure",
    "6.06": "Static Pool",
    "7.01": "Regulation FD Disclosure",
    "8.01": "Other Events",
    "9.01": "Financial Statements and Exhibits",
}
SECTION_TITLES = [
    "Registrant's Business and Operations", "Financial Information", "Securities and Trading Markets",
    "Matters Related to Accountants and Financial Statements", "Corporate Governance and Management",
    "Asset-Backed Securities", "Regulation FD", "Other Events", "Financial Statements and Exhibits",
]
NON_SUBSTANTIVE = {"9.01"}


# ----------------------------------------------------------------------------- network
class Net:
    def __init__(self):
        self.ua = os.environ.get("SEC_USER_AGENT", "").strip()
        self.last = 0.0
        self.n = 0

    def get(self, url, params=None, binary=False):
        if not self.ua or "@" not in self.ua:
            sys.exit("SEC_USER_AGENT is not set (needs a name and contact e-mail, per SEC fair-access "
                     "rules), and the local snapshot is incomplete. Set it and re-run.")
        for attempt in range(6):
            wait = 0.2 - (time.time() - self.last)
            if wait > 0:
                time.sleep(wait)
            self.last = time.time()
            self.n += 1
            r = requests.get(url, params=params, timeout=60,
                             headers={"User-Agent": self.ua, "Accept-Encoding": "gzip, deflate"})
            if r.status_code == 200:
                return r.content if binary else r.text
            if r.status_code in (403, 429, 500, 502, 503, 504):
                time.sleep(2 ** attempt * 2)
                continue
            if r.status_code == 404:
                return None
            r.raise_for_status()
        raise RuntimeError(f"giving up on {url} {params}")


def load_manifest():
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text())
    return {}


def save_manifest(m):
    MANIFEST.write_text(json.dumps(m, indent=1, sort_keys=True))


def utcnow():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ----------------------------------------------------------------------------- search snapshot
def snapshot_search(net, man):
    SEARCH_DIR.mkdir(parents=True, exist_ok=True)
    if man.get("search_complete"):
        return
    man.setdefault("search_started_utc", utcnow())
    day = START
    while day <= END:
        ds = day.isoformat()
        f = SEARCH_DIR / f"{ds}.json"
        if not f.exists():
            hits, frm, total = [], 0, None
            while True:
                txt = net.get(EFTS, params={"forms": "8-K", "dateRange": "custom",
                                            "startdt": ds, "enddt": ds, "from": frm})
                d = json.loads(txt)
                total = d["hits"]["total"]["value"]
                page = d["hits"]["hits"]
                hits.extend(page)
                frm += len(page)
                if not page or frm >= total or frm >= 9900:
                    break
            f.write_text(json.dumps({"date": ds, "total": total, "fetched_utc": utcnow(),
                                     "hits": hits}, sort_keys=True))
            print(f"search {ds}: {len(hits)}/{total}", flush=True)
        day += dt.timedelta(days=1)
    man["search_complete"] = True
    man["search_finished_utc"] = utcnow()
    save_manifest(man)


def load_filings():
    """One record per accession: the primary 8-K document hit, form exactly '8-K'."""
    by_adsh = {}
    for f in sorted(SEARCH_DIR.glob("*.json")):
        for h in json.loads(f.read_text())["hits"]:
            s = h["_source"]
            if s.get("form") != "8-K" or s.get("file_type") != "8-K":
                continue
            adsh, fname = h["_id"].split(":", 1)
            rec = {"adsh": adsh, "file": fname, "ciks": s.get("ciks") or [],
                   "names": s.get("display_names") or [], "file_date": s.get("file_date"),
                   "period_ending": s.get("period_ending"), "items": s.get("items") or [],
                   "sequence": s.get("sequence")}
            old = by_adsh.get(adsh)
            if old is None or (rec["sequence"] or 99, rec["file"]) < (old["sequence"] or 99, old["file"]):
                by_adsh[adsh] = rec
    return [by_adsh[k] for k in sorted(by_adsh)]


# ----------------------------------------------------------------------------- definitions
def norm_title(t):
    t = t.replace("\u2019", "'").replace("\u2013", "-").replace("\u2014", "-")
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()


def pdf_text():
    try:
        return subprocess.run(["pdftotext", "-layout", str(FORM_PDF), "-"], check=True,
                              capture_output=True, text=True).stdout
    except (FileNotFoundError, subprocess.CalledProcessError):
        from pypdf import PdfReader
        return "\n".join(p.extract_text() or "" for p in PdfReader(str(FORM_PDF)).pages)


def build_definitions(net, man):
    if DEFS_JSON.exists():
        return json.loads(DEFS_JSON.read_text())
    if not FORM_PDF.exists():
        data = net.get(FORM_URL, binary=True)
        if not data or not data.startswith(b"%PDF"):
            sys.exit("could not download the official Form 8-K PDF")
        FORM_PDF.write_bytes(data)
        man["form_pdf_fetched_utc"] = utcnow()
        save_manifest(man)
    text = pdf_text()
    text = text.replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    lines = [re.sub(r"\s+", " ", l).strip() for l in text.splitlines()]
    head_re = re.compile(r"^Item\s+(\d\.\d\d)\.?\s+(.*)$")
    stop_re = re.compile(r"^(Item\s+\d\.\d\d\b|Section\s+\d+\.|Instructions?\b|SIGNATURES?$|"
                         r"GENERAL INSTRUCTIONS)", re.I)
    defs = {}
    for i, l in enumerate(lines):
        m = head_re.match(l)
        if not m or m.group(1) not in TITLES:
            continue
        code = m.group(1)
        want = norm_title(TITLES[code])
        # title may wrap onto the next line(s)
        title_txt, j = m.group(2), i + 1
        while len(norm_title(title_txt)) < len(want) and j < len(lines) and lines[j] \
                and want.startswith(norm_title(title_txt + " " + lines[j])[: len(norm_title(title_txt)) + 1]):
            title_txt += " " + lines[j]
            j += 1
        if not norm_title(title_txt).startswith(want[: max(12, len(want) // 2)]):
            continue
        body = []
        while j < len(lines):
            if lines[j] == "":
                if body and len(" ".join(body)) > 150:
                    break
                j += 1
                continue
            if stop_re.match(lines[j]) or re.fullmatch(r"\d+", lines[j]):
                if body:
                    break
                j += 1
                continue
            body.append(lines[j])
            j += 1
        b = ""
        for piece in body:  # re-join PDF lines; a line-end hyphen joins without a space
            b = (b + piece) if b.endswith("-") or not b else (b + " " + piece)
        b = re.sub(r"^((\([a-z0-9]+\)|\d+\.)\s*)+", "", b).strip()
        if len(b) < 40:
            continue
        # keep the last (requirements-section) occurrence
        defs[code] = {"title_in_pdf": re.sub(r"\.$", "", title_txt.strip()), "text": b}
    out = {}
    for code, d in defs.items():
        t = d["text"]
        # first sentence (or up to the first colon that opens a list), capped at 400 chars
        s = None
        for m in re.finditer(r"[.:](?=\s|$)", t):
            if m.end() < 40:
                continue
            if re.search(r"(\bU\.S|\bU\.S\.C|\bNo|\bInc|\bCo|\be\.g|\bi\.e|\bCFR \d+|\b[A-Z])$", t[:m.start()]):
                continue
            s = t[:m.end()] if m.end() <= 450 else None
            break
        if s is None:
            s = t[:400].rsplit(" ", 1)[0] + " ..."
        if s.endswith(":"):
            s = s[:-1] + " ..."
        out[code] = {"title": TITLES[code], "title_in_pdf": d["title_in_pdf"],
                     "title_matches_pdf": norm_title(d["title_in_pdf"]).startswith(norm_title(TITLES[code])),
                     "definition": s, "source": FORM_URL}
    DEFS_JSON.write_text(json.dumps(out, indent=1, sort_keys=True))
    return out


# ----------------------------------------------------------------------------- text cleaning
SMALL = {"a", "an", "the", "of", "or", "and", "into", "in", "to", "under", "with", "on", "for",
         "that", "by", "from", "as"}


def title_regex(title):
    words = re.findall(r"[A-Za-z0-9]+", title)
    parts = []
    for w in words:
        if w.lower() in SMALL or not w[0].isalpha():
            parts.append(f"(?i:{re.escape(w)})")
        else:
            parts.append(f"{re.escape(w[0].upper())}(?i:{re.escape(w[1:])})" if len(w) > 1 else re.escape(w))
    # allow flexible punctuation / whitespace (incl. curly apostrophes, dashes) between words
    return r"(?<![A-Za-z])" + r"[^A-Za-z0-9]{0,6}".join(parts) + r"(?![A-Za-z])"


def title_variants(t, min_part_words=4):
    """The full official title, plus each ';'-separated part with >= 4 words (short generic parts
    such as 'Election of Directors' or 'Transfer of Listing' are ordinary phrases and are kept)."""
    v = {t}
    if ";" in t:
        v |= {p.strip() for p in t.split(";") if len(p.split()) >= min_part_words}
    return sorted(v, key=len, reverse=True)


TITLE_PATTERNS = [re.compile(title_regex(v)) for _t in TITLES.values() for v in title_variants(_t)
                  if len(v.split()) >= 2]
ITEM_NUM_RE = re.compile(r"\b(ITEMS?|Items?)(\s|\xa0)*(\d{1,2}\.\d{2})(\s?\([a-z0-9]{1,3}\))*")
TITLE_NORMS = sorted({norm_title(v) for _t in TITLES.values() for v in title_variants(_t)}, key=len, reverse=True)
TITLE_CI_RES = [re.compile(r"(?i)^" + title_regex(v).replace("(?<![A-Za-z])", "")) for v in
                sorted({v.strip() for _t in TITLES.values()
                        for v in ([_t] + (_t.split(";") if ";" in _t else []))}, key=len, reverse=True)]


def is_title_line(l):
    """A short line that is (a case variant of) an official item title, e.g. a sentence-case heading."""
    n = norm_title(l)
    if not n or len(l) > 250:
        return False
    n2 = re.sub(r"^(\(?[a-z0-9]{1,3}\)\s*)+", "", n)
    for t in TITLE_NORMS:
        for cand in (n, n2):
            if cand == t or difflib.SequenceMatcher(None, cand, t).ratio() >= 0.9:
                return True
    return False
ITEM_LIST_RE = re.compile(r"(?<=X\.XX)(\s*(?:,|and|or|&)\s*)(\d{1,2}\.\d{2})\b")
HEAD_LINE_RE = re.compile(r"^\s*ITEM\s*\d{1,2}\.\d{2}", re.I)
SECTION_LINE_RE = re.compile(
    r"^\s*SECTION\s+\d{1,2}\s*[.:\-\u2013\u2014]?\s*(" + "|".join(re.escape(s) for s in SECTION_TITLES)
    + r")\s*\.?\s*$", re.I)
COVER_END_RE = re.compile(r"(emerging growth company|Section\s+13\(a\)\s+of\s+the\s+Exchange\s+Act)", re.I)
END_RE = re.compile(r"^\s*(SIGNATURES?|EXHIBIT\s+INDEX|INDEX\s+TO\s+EXHIBITS|Pursuant to the requirements of "
                    r"the Securities Exchange Act)\b", re.I)
BLOCK_TAGS = ["p", "div", "br", "tr", "li", "h1", "h2", "h3", "h4", "h5", "h6", "table", "center",
              "blockquote", "pre", "hr", "ul", "ol", "dl", "dt", "dd", "section", "article"]


def html_to_lines(html):
    BR = "\u2029"  # block-break marker; raw newlines in the HTML source are only wrapping
    soup = BeautifulSoup(html, "html.parser")
    for t in soup.find_all(["script", "style", "head", "title"]):
        t.decompose()
    for t in soup.find_all(lambda x: x.name and x.name.lower() in ("ix:header",)):
        t.decompose()
    for t in soup.find_all(style=re.compile(r"display\s*:\s*none", re.I)):
        t.decompose()
    for t in soup.find_all(BLOCK_TAGS):
        t.insert_before(BR)
        t.insert_after(BR)
    # one table row = one line, cells separated by a space (innermost rows first)
    for tr in reversed(soup.find_all("tr")):
        cells = [re.sub(r"\s+", " ", c.get_text("").replace(BR, " ")).strip()
                 for c in tr.find_all(["td", "th"], recursive=False)]
        tr.replace_with(BR + " ".join(c for c in cells if c) + BR)
    text = soup.get_text("")
    text = unicodedata.normalize("NFKC", text).replace("\u200b", "").replace("\ufeff", "")
    lines = [re.sub(r"\s+", " ", l).strip() for l in text.split(BR)]
    lines = [l for l in lines if l]
    merged = []
    for l in lines:
        if merged and re.fullmatch(r"(?i)items?", merged[-1]) and re.match(r"\d{1,2}\.\d{2}\b", l):
            merged[-1] = merged[-1] + " " + l
        else:
            merged.append(l)
    return merged


def clean_filing(html, label=None):
    """Return (state, info) or (None, reason). With `label`, the document's own Item headings
    (other than 9.01) must be exactly that item, so the gold agrees with the text as well as
    with the EDGAR items metadata."""
    lines = html_to_lines(html)
    if not lines:
        return None, "empty"
    # start: the first item heading after the cover page
    cover_end = 0
    for i, l in enumerate(lines[:200]):
        if COVER_END_RE.search(l):
            cover_end = i
    start = None
    for i in range(cover_end, len(lines)):
        if HEAD_LINE_RE.match(lines[i]):
            start = i
            break
    if start is None:
        return None, "no_item_heading"
    # end: signature block / exhibit index / Item 9.01 heading
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if END_RE.match(lines[i]) or re.match(r"^\s*ITEM\s*9\.01", lines[i], re.I):
            end = i
            break
    body = lines[start:end]
    if label is not None:
        codes = set()
        for l in body:
            mh = re.match(r"^\s*ITEMS?\s*(\d{1,2})\.(\d{2})", l, re.I)
            if mh:
                codes.add(f"{int(mh.group(1))}.{mh.group(2)}")
        if codes - NON_SUBSTANTIVE != {label}:
            return None, "heading_item_mismatch"
    out = []
    for l in body:
        if SECTION_LINE_RE.match(l) or is_title_line(l):
            continue
        after_item = bool(HEAD_LINE_RE.match(l))
        l = ITEM_NUM_RE.sub(lambda m: m.group(1) + " X.XX", l)
        l = ITEM_LIST_RE.sub(lambda m: m.group(1) + "X.XX", l)
        if after_item:
            # heading on the same line as body text: drop the title in any letter case
            m = re.match(r"^\s*(ITEMS?|Items?)\s+X\.XX[\s.:\-\u2013\u2014]*", l)
            rest = l[m.end():] if m else l
            for p in TITLE_CI_RES:
                mm = p.match(rest)
                if mm:
                    rest = rest[mm.end():]
                    break
            l = rest
        out.append(l)
    # titles quoted anywhere (also across line breaks), then drop lines left without content
    joined = "\n".join(out)
    for p in TITLE_PATTERNS:
        joined = p.sub(" ", joined)
    out = []
    for l in joined.split("\n"):
        l = re.sub(r"[ \t]{2,}", " ", l).strip()
        l = re.sub(r"^(\s*[.:;,\-\u2013\u2014]\s*)+", "", l)
        left = re.sub(r"(?i)items?\s*x\.xx", "", l)
        left = re.sub(r"^(\s*\(?[a-z0-9]{1,3}\)\s*)+", "", left)
        if not re.search(r"[A-Za-z0-9]", left) or is_title_line(l):
            continue
        out.append(l)
    # re-flow lines that the HTML layout broke mid-sentence (whitespace only)
    flowed = []
    for l in out:
        if flowed:
            prev = flowed[-1]
            if not re.search(r"[.:;!?\"\u201d)]$", prev) and (
                    re.match(r"[a-z(\u201c\"]", l)):
                flowed[-1] = prev + " " + l
                continue
        flowed.append(l)
    text = "\n".join(flowed).strip()
    if len(text) > MAX_CHARS:
        cut = text[:MAX_CHARS]
        ends = [m.end() for m in re.finditer(r"[.!?][\"')\]]?(?=\s)", cut)]
        if cut.endswith((".", "!", "?")):
            ends.append(len(cut))
        if not ends or ends[-1] < MAX_CHARS // 2:
            return None, "no_sentence_boundary"
        text = cut[: ends[-1]].strip()
    if len(text) < MIN_CHARS:
        return None, "too_short"
    return text, "ok"


# ----------------------------------------------------------------------------- build
def hid(prefix, *parts):
    return prefix + hashlib.sha1("|".join(("ohs3", TASK) + parts).encode()).hexdigest()[:12]


def doc_url(rec):
    return (f"https://www.sec.gov/Archives/edgar/data/{int(rec['ciks'][0])}/"
            f"{rec['adsh'].replace('-', '')}/{rec['file']}")


def fetch_doc(net, man, rec):
    DOC_DIR.mkdir(parents=True, exist_ok=True)
    f = DOC_DIR / f"{rec['adsh']}.htm"
    miss = DOC_DIR / f"{rec['adsh']}.missing"
    if f.exists():
        return f.read_bytes().decode("utf-8", errors="replace")
    if miss.exists():
        return None
    data = net.get(doc_url(rec), binary=True)
    if data is None:
        miss.write_text("404\n")
        return None
    f.write_bytes(data)
    man.setdefault("docs_fetched_utc", {})[rec["adsh"]] = utcnow()
    return data.decode("utf-8", errors="replace")


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    net = Net()
    man = load_manifest()
    snapshot_search(net, man)
    defs = build_definitions(net, man)

    filings = load_filings()
    single = []
    for r in filings:
        subst = sorted(set(r["items"]) - NON_SUBSTANTIVE)
        if len(subst) == 1 and subst[0] in TITLES and r["ciks"]:
            r["label"] = subst[0]
            single.append(r)
    # frequency = distinct CIKs per item
    cik_per_item = defaultdict(set)
    for r in single:
        cik_per_item[r["label"]].add(r["ciks"][0])
    freq = Counter({k: len(v) for k, v in cik_per_item.items()})
    ranked = sorted(freq, key=lambda k: (-freq[k], k))
    options_codes = [k for k in ranked if freq[k] >= MIN_FILINGS][:MAX_OPTIONS]
    assert len(options_codes) >= MIN_OPTIONS, options_codes
    missing_defs = [c for c in options_codes if c not in defs]
    if missing_defs:
        sys.exit(f"no official definition parsed for items {missing_defs}; inspect {FORM_PDF}")
    bad_titles = [c for c in options_codes if not defs[c]["title_matches_pdf"]]
    if bad_titles:
        sys.exit(f"hard-coded titles do not match the official PDF for items {bad_titles}; inspect {FORM_PDF}")

    rng = random.Random(SEED)
    pools = {c: [r for r in single if r["label"] == c] for c in options_codes}
    for c in options_codes:
        pools[c].sort(key=lambda r: r["adsh"])
        rng.shuffle(pools[c])

    # equal allocation, rarest item first; one filing per company (any shared CIK)
    K = len(options_codes)
    quota = {c: N_ITEMS // K for c in options_codes}
    for c in sorted(options_codes, key=lambda k: (-freq[k], k))[: N_ITEMS - sum(quota.values())]:
        quota[c] += 1
    order = sorted(options_codes, key=lambda k: (freq[k], k))
    used_ciks, chosen, skipped = set(), defaultdict(list), Counter()
    ptr = {c: 0 for c in options_codes}

    def fill(c, want):
        while len(chosen[c]) < want and ptr[c] < len(pools[c]):
            r = pools[c][ptr[c]]
            ptr[c] += 1
            if used_ciks & set(r["ciks"]):
                skipped["dup_cik"] += 1
                continue
            html = fetch_doc(net, man, r)
            if html is None:
                skipped["doc_missing"] += 1
                continue
            state, why = clean_filing(html, label=c)
            if state is None:
                skipped[why] += 1
                continue
            used_ciks.update(r["ciks"])
            chosen[c].append((r, state))

    try:
        for c in order:
            fill(c, quota[c])
        # redistribute any shortfall to classes that still have filings, keeping the 40% cap
        short = N_ITEMS - sum(len(v) for v in chosen.values())
        cap = int(MAX_SHARE * N_ITEMS)
        while short > 0:
            progressed = False
            for c in sorted(options_codes, key=lambda k: (len(chosen[k]), -freq[k], k)):
                if short <= 0:
                    break
                if len(chosen[c]) >= cap or ptr[c] >= len(pools[c]):
                    continue
                before = len(chosen[c])
                fill(c, before + 1)
                if len(chosen[c]) > before:
                    short -= 1
                    progressed = True
            if not progressed:
                break
    finally:
        save_manifest(man)

    snap = f"search {man.get('search_started_utc')}..{man.get('search_finished_utc')}"
    rows = []
    for c in options_codes:
        for r, state in chosen[c]:
            opts = [TITLES[k] for k in options_codes]
            orng = random.Random(f"{SEED}|{r['adsh']}")
            orng.shuffle(opts)
            code_of = {TITLES[k]: k for k in options_codes}
            card = "\n".join(f"- {o}: {defs[code_of[o]]['definition']}" for o in opts)
            rows.append({
                "id": hid("r_", r["adsh"]),
                "group_id": f"g:{TASK}:{r['adsh']}",
                "call_id": hid("c_", "call", INSTR, state, json.dumps(opts, ensure_ascii=False)),
                "split": "ohs3",
                "track": "F",
                "source": TASK,
                "state": state,
                "qtype": "choice",
                "instructions": INSTR,
                "options": opts,
                "gold": TITLES[c],
                "role": "choice",
                "card": card,
                "meta": {
                    "task": TASK, "part": TASK,
                    "dataset": "SEC EDGAR Form 8-K filings (EDGAR full-text search index + Archives primary document)",
                    "snapshot": snap,
                    "doc_fetched_utc": man.get("docs_fetched_utc", {}).get(r["adsh"]),
                    "licence": LICENCE,
                    "accession": r["adsh"], "cik": r["ciks"][0], "ciks": r["ciks"],
                    "company": r["names"][0] if r["names"] else None,
                    "filing_date": r["file_date"], "period_ending": r["period_ending"],
                    "items_original": r["items"], "original_label": c,
                    "primary_document": r["file"], "url": doc_url(r),
                    "filing_index_url": (f"https://www.sec.gov/Archives/edgar/data/{int(r['ciks'][0])}/"
                                         f"{r['adsh'].replace('-', '')}/{r['adsh']}-index.htm"),
                },
            })
    rows.sort(key=lambda x: x["id"])
    assert len({x["group_id"] for x in rows}) == len(rows)
    assert len({x["id"] for x in rows}) == len(rows)
    for x in rows:
        assert x["gold"] in x["options"] and len(set(x["options"])) == len(x["options"])
        assert [l.split(": ", 1)[0][2:] for l in x["card"].split("\n")] == x["options"]
        assert "X.XX" not in x["gold"] and not re.search(r"(?i)\bitems?\s*\d{1,2}\.\d{2}", x["state"])
    assert all(MIN_CHARS <= len(x["state"]) <= MAX_CHARS for x in rows)
    bal = Counter(x["gold"] for x in rows)
    assert max(bal.values()) <= MAX_SHARE * len(rows), bal

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_ROWS, "w") as f:
        for x in rows:
            f.write(json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n")
    dates = sorted(x["meta"]["filing_date"] for x in rows)
    summary = {
        "task": TASK, "rows": len(rows), "target": N_ITEMS, "qtype": "choice", "track": "F",
        "n_options": len(options_codes),
        "options": [{"item": k, "title": TITLES[k], "filings_distinct_cik": freq[k],
                     "definition": defs[k]["definition"], "title_matches_pdf": defs[k]["title_matches_pdf"]}
                    for k in options_codes],
        "class_balance": {f"{k} {TITLES[k]}": bal.get(TITLES[k], 0) for k in options_codes},
        "max_class_share": round(max(bal.values()) / len(rows), 3),
        "filing_date_range": [dates[0], dates[-1]],
        "source_window": [START.isoformat(), END.isoformat()],
        "snapshot": {"search_started_utc": man.get("search_started_utc"),
                     "search_finished_utc": man.get("search_finished_utc"),
                     "form_pdf_fetched_utc": man.get("form_pdf_fetched_utc"),
                     "cache_dir": os.path.relpath(CACHE, LEAN)},
        "pool": {"filings_8k": len(filings), "single_substantive_item": len(single),
                 "item_freq_distinct_cik": dict(sorted(freq.items())), "skipped_while_sampling": dict(skipped)},
        "licence": LICENCE,
        "labels_source": f"official Form 8-K ({FORM_URL}): item titles; definition = first sentence of the item's requirement text",
        "author_written_definitions": [],
        "provenance": "filing list/items: " + EFTS + " (forms=8-K, one query per filing day, paged); text: sec.gov/Archives primary document; per-row accession/CIK/url in meta",
        "seed": SEED,
        "processing": [
            "form type exactly 8-K (8-K/A excluded); primary document (file_type 8-K) only",
            "kept filings whose items list has exactly one item other than 9.01; label = that item",
            "options = items with >= 5 distinct-CIK filings, top 20 by frequency; equal allocation per item, rarest first; one filing per company (no shared CIK)",
            "state = primary document text from the first 'Item N.NN' heading after the cover page, up to the signature block / exhibit index / Item 9.01 heading",
            "removed: cover page, Item N.NN headings, 'Section N <section title>' headings, official item titles wherever quoted in title case or caps (also each ';' part of a multi-part title that has >= 4 words), and short lines that are a case variant of a title (e.g. a sentence-case heading)",
            "item numbers mentioned in the body are masked as 'Item X.XX' (e.g. 'this Item X.XX')",
            "hidden inline-XBRL header removed; truncated to 6,000 chars at a sentence boundary; states under 100 chars dropped",
        ],
        "uncertain": [
            "Filings are company-authored public records on EDGAR; treated as public domain/public record per SEC practice (no per-filing licence).",
            "Card definitions are the first sentence of each item's official requirement text (cut with '...' at a list colon or after ~400 chars), so multi-part items (e.g. 5.02, 5.03) are only partly described by it; titles are official.",
            "Boilerplate that is typical of an item (e.g. the 'shall not be deemed filed' language of 7.01/2.02) is source text and was kept.",
            "Filings from the last day of the window may be incomplete in the search snapshot (snapshot taken on that day).",
        ],
    }
    OUT_SUMMARY.write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    print(json.dumps(summary, indent=1, ensure_ascii=False))
    print(f"network requests this run: {net.n}", file=sys.stderr)


if __name__ == "__main__":
    main()
