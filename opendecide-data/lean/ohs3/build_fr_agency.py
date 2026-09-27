"""OHS-3 part builder: fr_agency (WIDE choice task, 40 options, track F).

Source: Federal Register API v1 (US government work, public domain, 17 U.S.C. 105).
Documents published 2026-06-01..2026-09-26, frozen as a raw snapshot under
ohs3/cache/fr_agency/ (documents.json, agencies.json, snapshot_meta.json). If the
cache exists it is used as-is, so re-runs give identical rows. Delete the cache only
to take a new snapshot (which would change the test).

Label = top-level parent agency (follow parent_id to the root) of every agency listed
on the document. Label definition = the agency's official 'description' from
/api/v1/agencies. State = title + abstract with agency self-names redacted to [AGENCY].

No model, no LLM API, no model outputs are used.
"""
import datetime
import hashlib
import json
import os
import random
import re
import ssl
import sys
import time
import urllib.request
from collections import Counter, defaultdict

TASK = "fr_agency"
SEED = 20261026
N_ITEMS = 142
N_LABELS = 40
MIN_PER_LABEL = 5
MIN_LABELS = 27
MIN_ABSTRACT = 100          # "short abstract" threshold (characters, after whitespace normalisation)
DATE_FROM, DATE_TO = "2026-06-01", "2026-09-26"
HERE = os.path.dirname(os.path.abspath(__file__))
LEAN = os.path.dirname(HERE)
CACHE = os.path.join(HERE, "cache", TASK)
OUT = os.path.join(LEAN, "data", "ohs3_parts", f"{TASK}.jsonl")
OUT_SUM = os.path.join(LEAN, "data", "ohs3_parts", f"{TASK}_summary.json")
API = "https://www.federalregister.gov/api/v1"
LICENCE = "Public domain (US government work, 17 U.S.C. 105); Federal Register API v1"
INSTRUCTIONS = "Which federal department or independent agency issued this Federal Register document?"
TOKEN = "[AGENCY]"
ACRONYM_KINDS = ("short_name", "slug_acronym")
FULL_NAME_KINDS = ("name", "name_natural_order", "raw_name")
# FR short_names that are ordinary abbreviations in running text (Army Department short_name "USA")
NOT_AGENCY_ACRONYMS = {"USA", "US"}
# Verification fix (frozen): official self-names that the FR agency list does not contain but that the
# agencies use for themselves in FR text. Added to the redaction lexicon (kind 'alias') for every document.
EXTRA_ALIASES = {
    491: ["United States Trade Representative", "U.S. Trade Representative", "Trade Representative"],  # USTR
    188: ["Board of Governors of the Federal Reserve System", "Federal Reserve Board", "Federal Reserve"],  # Fed
    378: ["DoN"],                                        # Department of the Navy's own acronym (FR short_name is USN)
    199: ["Commissioner of Food and Drugs"],             # FDA head's statutory title (like 'Secretary of X')
}
# Verification fix (frozen): generic self-nouns an agency uses for itself that are not in its FR name/description.
EXTRA_SELF_NOUNS = {188: ("Board",)}                     # 'The Board invites comment' (Federal Reserve Board)


# ----------------------------------------------------------------------------- snapshot
def _get(url):
    import certifi
    ctx = ssl.create_default_context(cafile=certifi.where())
    for i in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "opendecide-ohs3-builder"})
            with urllib.request.urlopen(req, timeout=120, context=ctx) as r:
                return json.load(r)
        except Exception as e:  # noqa
            print("retry", url[:80], e, file=sys.stderr)
            time.sleep(5 * (i + 1))
    raise SystemExit(f"download failed: {url}")


def snapshot():
    paths = [os.path.join(CACHE, f) for f in ("agencies.json", "documents.json", "snapshot_meta.json")]
    if all(os.path.exists(p) for p in paths):
        return [json.load(open(p)) for p in paths]
    os.makedirs(CACHE, exist_ok=True)
    snap = datetime.datetime.now(datetime.timezone.utc).isoformat()
    ag = _get(f"{API}/agencies")
    fields = ["document_number", "title", "abstract", "agencies", "type", "publication_date", "html_url"]
    url = (f"{API}/documents.json?conditions[publication_date][gte]={DATE_FROM}"
           f"&conditions[publication_date][lte]={DATE_TO}"
           + "".join(f"&fields[]={f}" for f in fields) + "&per_page=1000&order=oldest")
    url = url.replace("[", "%5B").replace("]", "%5D")
    first, pages, docs, d = url, [], [], None
    while url:
        d = _get(url)
        pages.append(url)
        docs += d["results"]
        url = d.get("next_page_url")
    meta = {"snapshot_utc": snap, "agencies_url": f"{API}/agencies", "documents_first_url": first,
            "page_urls": pages, "api_count": d["count"], "n_docs": len(docs), "n_agencies": len(ag)}
    for p, obj in zip(paths, (ag, docs, meta)):
        json.dump(obj, open(p, "w"), indent=0)
    return ag, docs, meta


# ----------------------------------------------------------------------------- redaction
STOP = {"of", "and", "the", "for", "on", "in", "to", "from", "a", "an", "at", "by", "with", "or", "&"}
INVERT_HEADS = ("Department", "Office", "Bureau", "Corps", "Service", "Administration", "Agency",
                "Commission", "Board", "Council", "Institute", "Division", "Center", "Program", "Directorate")
# generic self-reference nouns ("The Commission hereby gives notice", "the Board", "the Service")
SELF_NOUNS = ("Commission", "Board", "Bureau", "Service", "Department", "Agency", "Corporation", "Foundation",
              "Council", "Committee", "Office", "Endowment", "Mint", "Institute", "Authority", "Administration",
              "Archives", "Corps", "Guard", "Trust", "Staff", "Center")
RAW_ID_LESS_OK = re.compile(r"^(department|office) of\b|(commission|board|administration|service|agency|bureau)\W*$", re.I)


def _norm_ws(s):
    return re.sub(r"\s+", " ", (s or "").replace(" ", " ")).strip()


def slug_acronym(slug):
    words = [w for w in slug.split("-") if w and w not in STOP]
    return "".join(w[0] for w in words).upper()


def name_forms(name):
    """The FR 'name' plus its natural word order (FR inverts, e.g. 'Transportation Department')."""
    name = _norm_ws(name)
    forms = {name}
    if "," not in name:
        for head in INVERT_HEADS:
            if name.endswith(" " + head) and len(name) > len(head) + 1:
                core = name[: -len(head) - 1]
                forms |= {f"{head} of {core}", f"{head} of the {core}"}
    else:  # 'Trade Representative, Office of United States' -> 'Office of United States Trade Representative'
        a, b = [x.strip() for x in name.split(",", 1)]
        m = re.match(r"^(Office|Bureau|Department|Commission) of (the )?(.*)$", b)
        if m:
            forms |= {f"{m.group(1)} of {m.group(3)} {a}", f"{m.group(1)} of the {m.group(3)} {a}"}
    return forms


def build_lexicon(agencies, docs):
    """Returns list of (pattern_text, kind, agency_id, case_sensitive)."""
    lex = {}

    def add(text, kind, aid, cs):
        text = _norm_ws(text).rstrip(":").strip()
        if len(text) < 2:
            return
        key = (text if cs else text.lower())
        if key not in lex or len(kind) < len(lex[key][1]):
            lex[key] = (text, kind, aid, cs)

    for a in agencies:
        for f in name_forms(a["name"]):
            multi = len(f.split()) > 1
            add(f, "name" if f == _norm_ws(a["name"]) else "name_natural_order", a["id"], not multi)
        for sn in re.split(r"/", a.get("short_name") or ""):
            sn = sn.strip()
            if sn:
                add(sn, "short_name", a["id"], len(sn.split()) == 1)
        sa = slug_acronym(a["slug"])
        if len(sa) >= 3:
            add(sa, "slug_acronym", a["id"], True)
        for al in EXTRA_ALIASES.get(a["id"], []):
            add(al, "alias", a["id"], len(al.split()) == 1)
    ids = {a["id"] for a in agencies}
    for d in docs:  # the printed agency names in the documents themselves (source's own naming)
        for x in d["agencies"]:
            raw = _norm_ws(x.get("raw_name"))
            if not raw or ";" in raw:
                continue
            if x.get("id") in ids or RAW_ID_LESS_OK.search(raw.rstrip(":")):
                add(raw, "raw_name", x.get("id"), False)
    return list(lex.values())


def _pat(text, cs):
    esc = re.escape(text).replace(r"\ ", r"\s+")
    return r"(?<![A-Za-z0-9])" + esc + r"(?![A-Za-z0-9])"


class Redactor:
    """Collects every lexicon match in the text (fast substring prefilter, then a word-bounded regex per
    entry), keeps the longest match at each place (leftmost-longest, non-overlapping), replaces with TOKEN."""

    def __init__(self, lexicon):
        self.lex = []
        for text, kind, aid, cs in sorted(lexicon, key=lambda t: (-len(t[0]), t[0])):
            flags = 0 if cs else re.I
            self.lex.append((text, kind, aid, cs, text if cs else text.lower(), re.compile(_pat(text, cs), flags)))
        dept_cores = set()
        for text, kind, aid, cs, _, _ in self.lex:
            m = re.match(r"^Department of (the )?(.+)$", text, re.I)
            if m and kind != "short_name":
                dept_cores.add(m.group(2))
        cores = sorted(dept_cores, key=lambda s: (-len(s), s))
        self.sec_rx = re.compile(r"(?<![A-Za-z])(Secretary of )(?:the )?(?:" + "|".join(
            re.escape(c) for c in cores) + r")(?![A-Za-z])", re.I)

    @staticmethod
    def _accept(text, s, e, entry):
        t, kind = entry[0], entry[1]
        if not text[s].isupper() and not text[s].isdigit():  # names must start capitalised in the text
            return False
        if len(t) <= 2 and kind == "short_name" and text[max(0, s - 2): s] == ", ":
            return False  # 2-letter code after ', ' = postal code in an address (e.g. 'Washington, DC')
        return True

    def matches(self, text, skip_acr=frozenset()):
        low = text.lower()
        spans = []
        for entry in self.lex:
            key = entry[4]
            if entry[1] in ACRONYM_KINDS and (entry[0] in skip_acr or entry[0] in NOT_AGENCY_ACRONYMS):
                continue
            if key not in (text if entry[3] else low):
                continue
            for m in entry[5].finditer(text):
                if self._accept(text, m.start(), m.end(), entry):
                    spans.append((m.start(), m.end(), entry))
        spans.sort(key=lambda x: (x[0], -(x[1] - x[0])))
        out, last = [], -1
        for s, e, entry in spans:
            if s >= last:
                if True:  # 'National Credit Union Administration Board', 'NCUA Board' -> one span
                    ext = re.match(r" (?:" + "|".join(SELF_NOUNS) + r")(?![A-Za-z\-])", text[e:])
                    if ext:
                        e += ext.end()
                out.append((s, e, entry))
                last = e
        return out

    def _local_non_agency_acronyms(self, text):
        """Acronyms the text itself defines for something that is not an agency name, e.g.
        'Emergency Alert System (EAS)', 'Norfolk Southern Corporation (NSC)'. These are not redacted
        in that document even if an FR agency uses the same letters as its short_name."""
        full_ends = {e for s, e, entry in self.matches(text) if entry[1] in FULL_NAME_KINDS}
        skip = set()
        for m in re.finditer(r"\(\s*[\"“]?([A-Z][A-Za-z]{1,9})[\"”]?\s*\)", text):
            q = m.start()
            while q > 0 and text[q - 1] == " ":
                q -= 1
            if text[max(0, q - 2): q] in ("'s", "’s"):   # "Office of Management and Budget's (OMB)"
                q -= 2
            if q not in full_ends:
                skip.add(m.group(1))
        return skip

    @staticmethod
    def _term_fits_name(term, name, context):
        """Word term: a word of the name or of up to 50 chars before it ('Board of Governors of the ...').
        Acronym term: its capitals appear in order among the initials of the matched name (or of the
        capitalised words in the 50 chars before it, ending with the name's last word)."""
        words = re.findall(r"[A-Za-z]+", name)
        caps = [c for c in term if c.isupper()]
        if len(caps) == 1:                                  # 'Commission', 'Board', 'Commerce', 'Treasury'
            return term in words or (term in SELF_NOUNS and term in re.findall(r"[A-Za-z]+", context))
        if len(caps) >= 2:                                  # acronym: capitals in order among the word initials
            initials = [w[0].upper() for w in words]
            it = iter(initials)
            if all(c in it for c in caps):
                return True
            # 'United States International Trade Commission (USITC)': capitalised words just before the name
            cw = [w[0] for w in re.findall(r"[A-Za-z]+", context) if w[0].isupper()]
            it = iter(cw)
            return all(c in it for c in caps) and caps[-1] == (initials[-1] if initials else "")
        return False

    def _defined_terms(self, text, skip_acr):
        """Short names the document defines for an agency right after naming it:
        'Department of Transportation (DOT)', 'Securities and Exchange Commission (the "Commission")'."""
        terms = set()
        for s, e, entry in self.matches(text, skip_acr):
            pm = re.match(r"(?:['’]s)?\s*\(([^()]{1,60})\)", text[e: e + 80])
            if not pm:
                continue
            for part in re.split(r"\s+or\s+|,\s*|;\s*", pm.group(1)):
                part = part.strip().strip("\"'“”‘’").strip()
                part = re.sub(r"^(the|The|operating as|doing business as|also known as)\s+", "", part).strip("\"'“”‘’ ")
                if (re.fullmatch(r"[A-Z][A-Za-z&.\-]{1,14}", part) and part not in {"U.S.", "US"}
                        and self._term_fits_name(part, text[s:e], text[max(0, s - 50):e])):
                    terms.add(part)
        return terms

    def redact(self, fields, self_nouns=(), own_acr=()):
        """fields: dict name->text; self_nouns: generic nouns this document's own agencies use for
        themselves; own_acr: FR acronyms (short_name / slug acronym) of the document's own agencies.
        Returns (dict, log, kept_acronyms)."""
        self_rx = re.compile(r"(?<![A-Za-z\-])(" + "|".join(sorted(self_nouns)) + r")(?![A-Za-z\-])") if self_nouns else None
        # own-agency acronym inside a longer code token ('HUDCAPS', 'GSAR', '66VA53') or in another case
        # before a form number ('Ferc-555')
        acr_parts = []
        for a in sorted(set(own_acr), key=lambda s: (-len(s), s)):
            ea = re.escape(a)
            if len(a) >= 3:
                acr_parts += [r"\d+" + ea + r"[A-Z0-9]*", ea + r"[A-Z0-9]+",
                              re.escape(a[0]) + "(?i:" + re.escape(a[1:]) + r")(?=-\d)"]
            elif len(a) == 2:
                acr_parts.append(r"\d+" + ea + r"\d+")
        acr_rx = re.compile(r"(?<![A-Za-z0-9])(?:" + "|".join(acr_parts) + r")(?![A-Za-z0-9])") if acr_parts else None

        def self_ref_ok(text, m):
            """Standalone generic self-reference ('the Commission', 'further Board order'), not part of a
            longer proper name ('Postal Service', 'Board of Trade', 'Commission Determination')."""
            before = text[: m.start()]
            pw = re.search(r"(\S+)\s+$", before)
            if pw is None:
                if before.strip():
                    return False
            else:
                w = pw.group(1)
                if w[0].isupper() and w not in ("The",) and not w.endswith((".", ":", ";")):
                    return False
                if w.endswith(("]",)):  # '[AGENCY] Board' is handled by name-span extension
                    return False
            after = text[m.end():]
            if re.match(r" (?:of|on|for|to the) [A-Z]", after) or re.match(r" [A-Z][a-z]", after):
                return False
            return True
        joined = "\n".join(fields.values())
        skip_acr = frozenset(self._local_non_agency_acronyms(joined))
        defined = sorted(self._defined_terms(joined, skip_acr), key=lambda s: (-len(s), s))
        drx = re.compile("|".join(_pat(t, True) for t in defined)) if defined else None
        out, log = {}, []
        for fname, text in fields.items():
            def sec_sub(m):
                log.append({"field": fname, "matched": m.group(0), "rule": "secretary_of_department",
                            "agency_id": None, "replaced_with": m.group(1) + TOKEN})
                return m.group(1) + TOKEN
            text = self.sec_rx.sub(sec_sub, text)
            parts, pos = [], 0
            for s, e, entry in self.matches(text, skip_acr):
                parts += [text[pos:s], TOKEN]
                log.append({"field": fname, "matched": text[s:e], "rule": entry[1], "agency_id": entry[2],
                            "lexicon_entry": entry[0]})
                pos = e
            text = "".join(parts) + text[pos:]
            if acr_rx is not None:
                def asub(m):
                    log.append({"field": fname, "matched": m.group(0), "rule": "own_acronym_variant",
                                "agency_id": None})
                    return TOKEN
                text = acr_rx.sub(asub, text)
            if drx is not None:
                def dsub(m):
                    log.append({"field": fname, "matched": m.group(0), "rule": "defined_self_name",
                                "agency_id": None})
                    return TOKEN
                text = drx.sub(dsub, text)
            if self_rx is not None:
                def ssub(m):
                    if not self_ref_ok(m.string, m):
                        return m.group(0)
                    ctx = m.string[max(0, m.start() - 20): m.end() + 20]
                    log.append({"field": fname, "matched": m.group(0), "rule": "generic_self_reference",
                                "agency_id": None, "context": ctx})
                    return TOKEN
                text = self_rx.sub(ssub, text)
            out[fname] = text
        kept = sorted(a for a in skip_acr if any(a == en[0] for en in self.lex if en[1] in ACRONYM_KINDS))
        return out, log, kept


# ----------------------------------------------------------------------------- build
def hid(prefix, s):
    return prefix + hashlib.sha1(s.encode()).hexdigest()[:12]


def main():
    agencies, docs, snapmeta = snapshot()
    A = {a["id"]: a for a in agencies}

    def top(i):
        seen = set()
        while A[i]["parent_id"] is not None and A[i]["parent_id"] in A and i not in seen:
            seen.add(i)
            i = A[i]["parent_id"]
        return i

    drops = Counter()
    pool = []
    seen_num = set()
    for d in sorted(docs, key=lambda d: d["document_number"]):
        if d["document_number"] in seen_num:
            drops["duplicate_document_number"] += 1
            continue
        seen_num.add(d["document_number"])
        if not (DATE_FROM <= d["publication_date"] <= DATE_TO):
            drops["outside_date_range"] += 1
            continue
        ags = d.get("agencies") or []
        if not ags or any(x.get("id") not in A for x in ags):
            drops["agency_without_api_id"] += 1
            continue
        tops = {top(x["id"]) for x in ags}
        if len(tops) != 1:
            drops["multiple_top_level_parents"] += 1
            continue
        ab = _norm_ws(d.get("abstract"))
        if len(ab) < MIN_ABSTRACT:
            drops["null_or_short_abstract"] += 1
            continue
        title = _norm_ws(d.get("title"))
        if not title:
            drops["no_title"] += 1
            continue
        pool.append({"doc": d, "top": tops.pop(), "title": title, "abstract": ab})

    counts = Counter(p["top"] for p in pool)
    eligible = [k for k, v in counts.items() if v >= MIN_PER_LABEL
                and _norm_ws(A[k].get("description"))]
    no_desc = [A[k]["name"] for k, v in counts.items() if v >= MIN_PER_LABEL and not _norm_ws(A[k].get("description"))]
    # 40 most frequent; ties broken by a seeded shuffle (random.Random(3), as in selection_criteria s.5)
    tie = sorted(eligible)
    random.Random(3).shuffle(tie)
    tie_rank = {k: i for i, k in enumerate(tie)}
    ranked = sorted(eligible, key=lambda k: (-counts[k], tie_rank[k]))
    labels = ranked[:N_LABELS]
    boundary = counts[labels[-1]]
    tied_out = [A[k]["name"] for k in ranked[N_LABELS:] if counts[k] == boundary]
    assert len(labels) >= MIN_LABELS, len(labels)
    label_name = {k: _norm_ws(A[k]["name"]) for k in labels}
    label_desc = {k: _norm_ws(A[k]["description"]) for k in labels}

    red = Redactor(build_lexicon(agencies, docs))

    def self_nouns_for(d):
        """Generic nouns the document's own agencies use for themselves: head nouns in their FR names or
        printed names, plus capitalised nouns used in their official descriptions (not 'Administration', which there
        often means the presidential Administration)."""
        nouns = set()
        for x in d["agencies"]:
            a = A[x["id"]]
            words = set(re.findall(r"[A-Za-z]+", f"{a['name']} {x.get('raw_name') or ''}".title()))
            nouns |= {n for n in SELF_NOUNS if n in words}
            for n in SELF_NOUNS:
                if n != "Administration" and re.search(rf"\b{n}\b", a.get("description") or ""):
                    nouns.add(n)
            nouns |= set(EXTRA_SELF_NOUNS.get(x["id"], ()))
        return tuple(sorted(nouns))

    def own_acronyms_for(d):
        acr = set()
        for x in d["agencies"]:
            a = A[x["id"]]
            for sn in (a.get("short_name") or "").split("/"):
                sn = sn.strip()
                if re.fullmatch(r"[A-Z]{2,}", sn) and sn not in NOT_AGENCY_ACRONYMS:
                    acr.add(sn)
            sa = slug_acronym(a["slug"])
            if len(sa) >= 3:
                acr.add(sa)
        return tuple(sorted(acr))

    # redact + dedupe (exact and whitespace-normalised state, and identical abstract)
    by_label = defaultdict(list)
    seen_state, seen_abs = set(), set()
    for p in pool:
        if p["top"] not in label_name:
            continue
        r, log, kept = red.redact({"title": p["title"], "abstract": p["abstract"]}, self_nouns_for(p["doc"]),
                                 own_acronyms_for(p["doc"]))
        state = f"Title: {r['title']}\n\nAbstract: {r['abstract']}"
        ns = _norm_ws(state).lower()
        na = _norm_ws(p["abstract"]).lower()
        if ns in seen_state or na in seen_abs:
            drops["duplicate_state_or_abstract"] += 1
            continue
        seen_state.add(ns)
        seen_abs.add(na)
        if not (20 <= len(state) <= 6000):
            drops["state_length"] += 1
            continue
        if len(_norm_ws(r["abstract"].replace(TOKEN, ""))) < 60:
            drops["abstract_mostly_redacted"] += 1
            continue
        p.update(state=state, redactions=log, kept=kept)
        by_label[p["top"]].append(p)

    rng = random.Random(SEED)
    lab_order = sorted(labels, key=lambda k: label_name[k])
    rng.shuffle(lab_order)
    base, extra = divmod(N_ITEMS, len(labels))
    quota = {k: base + (1 if i < extra else 0) for i, k in enumerate(lab_order)}
    for k in lab_order:  # if a label cannot fill its quota, move the remainder along the seeded order
        short = quota[k] - len(by_label[k])
        if short > 0:
            quota[k] -= short
            for k2 in lab_order:
                if k2 != k and len(by_label[k2]) > quota[k2] and short > 0:
                    quota[k2] += 1
                    short -= 1

    chosen = []
    for k in lab_order:
        cands = sorted(by_label[k], key=lambda p: p["doc"]["document_number"])
        rng.shuffle(cands)
        chosen += cands[: quota[k]]
    chosen.sort(key=lambda p: p["doc"]["document_number"])

    options_all = [label_name[k] for k in sorted(labels, key=lambda k: label_name[k])]
    rows = []
    for p in chosen:
        d = p["doc"]
        num = d["document_number"]
        opts = options_all[:]
        random.Random(f"{SEED}|{TASK}|{num}").shuffle(opts)
        name2id = {label_name[k]: k for k in labels}
        card = "\n".join(f"- {o}: {label_desc[name2id[o]]}" for o in opts)
        rows.append({
            "id": hid("r_", f"ohs3|{TASK}|{num}"),
            "group_id": f"g:{TASK}:{num}",
            "call_id": hid("c_", f"ohs3|{TASK}|{num}|call"),
            "split": "ohs3",
            "track": "F",
            "source": TASK,
            "state": p["state"],
            "qtype": "choice",
            "instructions": INSTRUCTIONS,
            "options": opts,
            "gold": label_name[p["top"]],
            "role": "choice",
            "card": card,
            "meta": {
                "task": TASK,
                "dataset": "Federal Register API v1 (federalregister.gov)",
                "document_number": num,
                "html_url": d["html_url"],
                "api_url": f"{API}/documents/{num}.json",
                "publication_date": d["publication_date"],
                "document_type": d.get("type"),
                "original_agencies": [{"id": x.get("id"), "name": x.get("name"), "raw_name": x.get("raw_name"),
                                       "parent_id": x.get("parent_id"), "slug": x.get("slug")}
                                      for x in d["agencies"]],
                "top_level_agency_id": p["top"],
                "top_level_agency_slug": A[p["top"]]["slug"],
                "original_label": label_name[p["top"]],
                "label_definition_source": f"{API}/agencies/{p['top']} (field 'description')",
                "snapshot_utc": snapmeta["snapshot_utc"],
                "licence": LICENCE,
                "redactions": p["redactions"],
                "not_redacted_acronyms": p["kept"],
            },
        })

    assert len({r["group_id"] for r in rows}) == len(rows)
    assert all(20 <= len(r["state"]) <= 6000 for r in rows)
    bal = Counter(r["gold"] for r in rows)
    assert max(bal.values()) / len(rows) <= 0.40
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")

    rule_counts = Counter(x["rule"] for r in rows for x in r["meta"]["redactions"])
    matched_counts = Counter(x["matched"] for r in rows for x in r["meta"]["redactions"])
    dates = sorted(r["meta"]["publication_date"] for r in rows)
    summary = {
        "task": TASK,
        "rows": len(rows),
        "qtype": "choice",
        "n_options": len(options_all),
        "track": "F",
        "split": "ohs3",
        "seed": SEED,
        "instructions": INSTRUCTIONS,
        "source": "Federal Register API v1, documents published 2026-06-01..2026-09-26",
        "licence": LICENCE,
        "snapshot": {k: snapmeta[k] for k in ("snapshot_utc", "agencies_url", "documents_first_url", "api_count",
                                               "n_docs", "n_agencies")},
        "cache_files": {f: hashlib.sha256(open(os.path.join(CACHE, f), "rb").read()).hexdigest()
                        for f in ("agencies.json", "documents.json", "snapshot_meta.json")},
        "publication_date_range_rows": [dates[0], dates[-1]],
        "label_definitions": "official: 'description' field of each top-level agency from /api/v1/agencies "
                             "(whitespace normalised only); no author-written definitions",
        "class_balance": dict(sorted(bal.items(), key=lambda kv: (-kv[1], kv[0]))),
        "max_class_share": round(max(bal.values()) / len(rows), 4),
        "labels": [{"name": label_name[k], "agency_id": k, "slug": A[k]["slug"], "pool_docs": counts[k],
                    "after_dedupe": len(by_label[k]), "rows": bal[label_name[k]]} for k in ranked[:N_LABELS]],
        "eligible_labels_ge5": len(eligible),
        "labels_tied_at_boundary_left_out": tied_out,
        "boundary_count": boundary,
        "eligible_without_description": no_desc,
        "filters": {"pool_after_filters": len(pool), "drops": dict(drops), "min_abstract_chars": MIN_ABSTRACT},
        "state_chars": {"min": min(len(r["state"]) for r in rows), "max": max(len(r["state"]) for r in rows)},
        "card_chars": {"min": min(len(r["card"]) for r in rows), "max": max(len(r["card"]) for r in rows)},
        "redactions": {"rows_with_redaction": sum(1 for r in rows if r["meta"]["redactions"]),
                       "total": sum(rule_counts.values()), "by_rule": dict(rule_counts),
                       "by_matched_text": dict(matched_counts.most_common())},
        "redaction_rules": [
            "Lexicon from all /api/v1/agencies entries (parents and sub-agencies): FR 'name' (case-insensitive if "
            "multi-word, must start capitalised in text), its natural word order for inverted FR names "
            "('X Department' -> 'Department of X' / 'Department of the X'; same for Office, Bureau, Service, etc.), "
            "short_name (split on '/'), slug-derived acronym (initials of slug words minus stop words, >=3 letters).",
            "Printed agency names (raw_name) from the snapshot documents' own agency lists (entries with an API id, "
            "or id-less entries shaped like 'Department/Office of ...' or ending in Commission/Board/etc.).",
            "Short names the text defines right after an agency name in parentheses, e.g. '(DOT)', "
            "'(the \"Commission\")', are redacted everywhere in that document ('defined_self_name').",
            "Generic self-references (Commission, Board, Bureau, Service, Department, Agency, ...) standing alone, "
            "e.g. 'The Commission hereby', 'further Board order', are redacted to [AGENCY] when the noun is a word in "
            "the name of one of the document's own listed agencies or a capitalised word in that agency's official "
            "description ('Administration' only from names). Not redacted when part of a longer proper name "
            "(capitalised word before or after, or followed by 'of/on/for X'). A self-noun right after a full agency "
            "name ('... Administration Board') is folded into that [AGENCY]. Parenthetical 'operating as X' names "
            "count as defined self-names.",
            "'Secretary of (the) X' where 'Department of X' is an agency name -> 'Secretary of [AGENCY]'.",
            "Exception: an agency short_name/slug acronym is kept in a document whose text defines it, in "
            "parentheses, for a phrase that is not an agency name (e.g. 'Emergency Alert System (EAS)'); "
            "logged in meta.not_redacted_acronyms. 'USA'/'US' (Army Department short_name) are never redacted.",
            "Exception: a 2-letter short_name preceded by ', ' (address postal code such as 'Washington, DC') is kept.",
            "Verification fix: a frozen alias list (EXTRA_ALIASES) adds official self-names missing from the FR agency "
            "list: 'United States Trade Representative' / 'U.S. Trade Representative' / 'Trade Representative' (USTR), "
            "'Board of Governors of the Federal Reserve System' / 'Federal Reserve Board' / 'Federal Reserve' (Fed), "
            "'DoN' (Navy), 'Commissioner of Food and Drugs' (FDA); 'Board' is a generic self-noun for the Fed.",
            "Verification fix: an acronym (short_name or slug acronym) of the document's own listed agencies inside a "
            "longer code token ('HUDCAPS', 'GSAR', '66VA53') or in another case before a form number ('Ferc-555') "
            "is replaced by [AGENCY] ('own_acronym_variant').",
            "All matches replaced by '[AGENCY]'; every replacement logged in meta.redactions.",
        ],
        "uncertain": [
            "Interpretation choices (not fixed by the spec): 'short abstract' = under 100 characters; documents with "
            "any agency entry lacking an API id are dropped (212 docs, e.g. id-less 'Office of the Secretary'); the "
            "40th-place tie at 11 docs is broken by random.Random(3) (selection_criteria s.5), leaving out the tied "
            "labels listed in labels_tied_at_boundary_left_out.",
            "Redaction is lexicon-based (FR agency list plus the frozen alias list), so sub-unit names/acronyms that are "
            "not FR agencies stay visible, e.g. NMFS, NEFSC, VHA, BJS, NCSES, OIRA, 'Enforcement Bureau'; statute and "
            "program names (Federal Deposit Insurance Act, National Credit Union Share Insurance Fund) and topic words "
            "(Veterans, Postal, marine mammals) are content and are kept. 'a Commission Determination' (ITC title "
            "formula) is kept because the noun is followed by a capitalised word.",
            "Generic self-reference redaction depends on the document's own agency names/descriptions (i.e. on the "
            "label); it removes the cue noun, but whether a noun was redacted is itself weakly label-dependent.",
            "Some short_names used for redaction are also ordinary abbreviations; those defined in the same text "
            "for a non-agency phrase are kept (meta.not_redacted_acronyms: EAC, EAS, NSC, FAR in 4 rows); "
            "'USA'/'US' (Army short_name) are never redacted.",
            "Card is long (~36k chars): 40 official FR agency descriptions in full (whitespace normalised).",
            "Many states are generic Paperwork Reduction Act / meeting notices whose agency is hard to infer after "
            "redaction; this is kept as sampled (no filtering on difficulty).",
            "FR 'abstract' for 2026-09-24..26 documents may still be revised by the FR after the snapshot; the "
            "cached snapshot is the frozen version.",
        ],
        "out": OUT,
    }
    json.dump(summary, open(OUT_SUM, "w"), indent=1, ensure_ascii=False)
    print(json.dumps({k: summary[k] for k in ("rows", "n_options", "max_class_share", "boundary_count",
                                              "labels_tied_at_boundary_left_out", "filters", "state_chars",
                                              "card_chars")}, indent=1))
    print(json.dumps(summary["redactions"]["by_rule"]))


if __name__ == "__main__":
    main()
