"""Build raw rows for wiki_help_routing: route a Wikipedia help request / report to the right desk or noticeboard.

Source : English Wikipedia project-space archives, fetched with the MediaWiki API (en.wikipedia.org/w/api.php):
           q=refdesk : Wikipedia:Reference desk/Archives/<Desk>/<YYYY Month D> daily archive pages, 6 subject desks
                       (Science, Mathematics, Computing, Humanities, Language, Entertainment; Miscellaneous is left out
                       because it is the catch-all desk and absorbs mis-posts);
           q=venue   : archive pages of 9 help / dispute venues (Reliable sources noticeboard, BLP noticeboard, NPOV
                       noticeboard, No original research noticeboard, Fringe theories noticeboard, Conflict of interest
                       noticeboard, Administrators' noticeboard/Incidents, Village pump (technical), Help desk).
         Every page is pinned by revision id + sha256 of its wikitext in pins_wiki_help_routing.json (first run
         selects pages with a seeded draw, later runs re-fetch exactly those revisions). Only pages whose newest
         signature is before 2022-11-30 are used (pre-LLM-assistant era). No split -> train.
Licence: CC BY-SA 4.0 (and earlier CC BY-SA 3.0 / GFDL) for all Wikipedia text, https://en.wikipedia.org/wiki/Wikipedia:Copyrights
         (attribution = the page histories linked by the pinned revision ids).
Texts  : the opening post of each thread (heading + first message up to the first reply or signature), written by
         the asker / reporter. Signatures, timestamps, diff links, refs and most templates are stripped.
Labels : the desk / venue where the human asker chose to post (and where the volunteers kept it). Threads that say
         they were moved, copied or cross-posted, or that mention another desk / board as the right place, are dropped;
         bot notices (Tech News etc.) and threads under 80 characters are dropped.
Review : (strict review) q=venue posts must carry the explicit issue cue of their own venue and of no other venue
         (STRICT; e.g. an NPOV post about an admin's conduct, or a BLP post by the subject's PR firm, is dropped);
         posts that name another reference desk ("the Science desk") are dropped too.
Rows   : one row per thread; per-option caps; the two question types never share a thread. Deterministic (seed SEED).
"""
import collections
import datetime
import hashlib
import json
import random
import re
import time

import _rd_common as C

KEY = "wiki_help_routing"
SEED = 20260929
API = "https://en.wikipedia.org/w/api.php"
PIN_FILE = C.HERE / "pins_wiki_help_routing.json"
LICENCE = ("CC BY-SA 4.0 / CC BY-SA 3.0 + GFDL (Wikipedia text; https://en.wikipedia.org/wiki/Wikipedia:Copyrights; "
           "pages pinned by revision id)")
CUTOFF = "2022-11-30"
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]

DESKS = {
    "Science": "Questions about the natural and applied sciences: physics, chemistry, biology, medicine and health, astronomy, earth science, engineering and technology (not software).",
    "Mathematics": "Questions about mathematics, statistics, probability, logic and puzzles that need mathematical reasoning.",
    "Computing": "Questions about computers, software, programming, the internet, electronics as used in computing, and IT or device problems.",
    "Humanities": "Questions about history, politics, law, religion, philosophy, economics and finance, society, the arts, literature and geography of human affairs.",
    "Language": "Questions about words and languages: meaning, grammar, spelling, pronunciation, etymology, translation and usage.",
    "Entertainment": "Questions about popular culture: films, television, music, video games, sports, comics, celebrities and other entertainment.",
}
DESK_OPT = {d: f"{d} reference desk" for d in DESKS}

VENUES = {  # option -> (title pattern, archive number range, definition)
    "Reliable sources noticeboard": ("Wikipedia:Reliable sources/Noticeboard/Archive {n}", (60, 340),
        "Whether a particular source (outlet, book, website, paper) is reliable enough to cite for a given statement in an article."),
    "Biographies of living persons noticeboard": ("Wikipedia:Biographies of living persons/Noticeboard/Archive{n}", (60, 330),
        "Problems with content about a living (or recently dead) person: unsourced or defamatory claims, privacy, undue negative material about them."),
    "Neutral point of view noticeboard": ("Wikipedia:Neutral point of view/Noticeboard/Archive {n}", (10, 95),
        "Whether an article's wording, weight or balance is biased or gives undue weight to one viewpoint, when sourcing itself is not the issue."),
    "No original research noticeboard": ("Wikipedia:No original research/Noticeboard/Archive {n}", (5, 45),
        "Whether article content goes beyond what sources say: editors' own analysis, synthesis of several sources into a new conclusion, or unsourced interpretation."),
    "Fringe theories noticeboard": ("Wikipedia:Fringe theories/Noticeboard/Archive {n}", (10, 85),
        "Articles promoting or giving undue credence to fringe, pseudoscientific or conspiracy ideas that depart from mainstream scholarship."),
    "Conflict of interest noticeboard": ("Wikipedia:Conflict of interest/Noticeboard/Archive {n}", (20, 175),
        "Editors who appear to edit about themselves, their employer, clients or products (paid or undisclosed promotional editing)."),
    "Administrators' noticeboard/Incidents": ("Wikipedia:Administrators' noticeboard/IncidentArchive{n}", (300, 1080),
        "Urgent or chronic user-conduct problems that need an administrator to act: harassment, disruption, personal attacks, block evasion or misuse of tools."),
    "Village pump (technical)": ("Wikipedia:Village pump (technical)/Archive {n}", (60, 195),
        "Technical problems and questions about the site's software: bugs, templates, gadgets, scripts, rendering, bots, tools and MediaWiki features."),
    "Help desk": ("Wikipedia:Help desk/Archives/{date}", None,
        "Questions about how to use or edit Wikipedia itself: creating articles, citing, formatting, uploading images, account and editing problems."),
}
REFDESK_Q = "Which Wikipedia Reference Desk should this question be posted to?"
VENUE_Q = "Which Wikipedia noticeboard or help page is the right place for this post?"
REF_PER_DESK, REF_PAGES_PER_DESK = 440, 180
VENUE_CAP, VENUE_PAGES_MAX = 260, 40

MOVED = re.compile(r"(moved|copied|transferred|transcluded|relocated) (here )?(from|to)|originally (posted|asked)|cross-?post|"
                   r"also (posted|asked|raised) (at|on)|forum ?shop|wrong (desk|venue|board|noticeboard|place|forum)|"
                   r"(better|best) (asked|place|venue|suited)|reference desk|help desk|teahouse|village pump|"
                   r"noticeboard", re.I)
DESK_NAME = re.compile(r"\b(science|mathematics|maths?|computing|humanities|language|entertainment|miscellaneous|misc)"
                       r" (desk|RD)\b", re.I)  # review fix: posts naming another desk ("a question on the Science desk")
ABBR = re.compile(r"\b(RSN|BLPN|BLP/N|NPOVN|NPOV/N|NORN|NOR/N|FTN|FT/N|COIN|COI/N|ANI|AN/I|VPT|VP/T|WP:AN|WP:HD|WP:RD)\b")
EDITING = re.compile(r"\b(my (article|draft|page|user ?page)|(create|creating|write|writing|start|submit) (an?|my|the|new) (article|page|draft)|"
                     r"edit(ing)? (wikipedia|this page|the article|an article)|upload(ing|ed)? (an? )?(image|photo|file|picture)|"
                     r"sandbox|infobox|talk page|speedy deletion|articles for creation)\b", re.I)
WIKI_CUE = re.compile(r"\b(wikipedia|wiki|article|edit(ing|ed|s)?|editor|draft|citations?|cite|references?|upload(ing|ed)?|"
                      r"account|user ?name|template|infobox|talk page|sandbox|page|userpage|revert(ed)?|deleted)\b", re.I)
# Claude-written verifier cues for the venue question: the gold venue's cue must appear; confusable pairs are excluded.
VCUE = {
    "Reliable sources noticeboard": r"\b(reliab\w*|sources?|citations?|cite[sd]?|publisher|journal|newspaper|website|blog|book|press)\b",
    "Biographies of living persons noticeboard": r"\b(living|biograph\w*|BLP|defam\w*|libel\w*|privacy|personal (life|information)|his|her|he|she|born|family|wife|husband)\b",
    "Neutral point of view noticeboard": r"\b(neutral\w*|NPOV|POV|bias\w*|balance\w*|undue|weight|slant\w*|tone|one-sided|whitewash\w*|puffery|critici\w*|controvers\w*)\b",
    "No original research noticeboard": r"(original research|\bOR\b|\bSYNTH\b|synthesis|\bsynth\w*|own (research|analysis|interpretation)|primary sources?|interpret\w*|unsourced (claim|analysis|conclusion))",
    "Fringe theories noticeboard": r"\b(fringe|pseudo\w*|conspirac\w*|alternative medicine|paranormal|ufo\w*|creationis\w*|quack\w*|homeopath\w*|astrolog\w*|cryptozoolog\w*|psychic|supernatural|hoax|mainstream)\b",
    "Conflict of interest noticeboard": r"\b(COI|conflict of interest|paid|promot\w*|advert\w*|employ\w*|company|PR|marketing|autobiograph\w*|spam\w*|undisclosed|client)\b",
    "Administrators' noticeboard/Incidents": r"\b(block\w*|harass\w*|attack\w*|disrupt\w*|vandal\w*|edit[- ]?war\w*|sock\w*|threat\w*|incivil\w*|uncivil|abus\w*|ban(ned)?|troll\w*|hound\w*|admin\w*|behaviou?r|insult\w*|stalk\w*)\b",
    "Village pump (technical)": r"\b(template|script|gadget|bug|css|javascript|lua|module|tool\w*|bots?|render\w*|display\w*|browser|preview|visualeditor|api|phabricator|error|button|software|mediawiki|server|page ?load|watchlist|link\w*|font|mobile)\b",
    "Help desk": None,
}
VCONFLICT = {
    "Biographies of living persons noticeboard": ["Conflict of interest noticeboard", "Fringe theories noticeboard"],
    "Neutral point of view noticeboard": ["Conflict of interest noticeboard", "Fringe theories noticeboard"],
    "Reliable sources noticeboard": ["Fringe theories noticeboard", "Conflict of interest noticeboard"],
    "No original research noticeboard": ["Fringe theories noticeboard", "Conflict of interest noticeboard"],
    "Conflict of interest noticeboard": ["Fringe theories noticeboard"],
    "Fringe theories noticeboard": ["Conflict of interest noticeboard"],
}
# Review fix (strict review, round 2): the loose cues above still let ~25% of venue posts through that fit a second
# venue as well (NPOV vs ANI, BLP vs COI, ...). A post is kept only if it carries the explicit issue cue of its own
# venue and of no other venue (Claude-written strict cues; the label is still the venue the poster chose).
STRICT = {
 "Reliable sources noticeboard": r"(reliab\w*|\bRS\b|unreliable|self-published|\bSPS\b|deprecat\w*|is (this|it|the) (source|site|website|book|paper) |as a source|usable source|acceptable source)",
 "Biographies of living persons noticeboard": r"(living (person|people)|\bBLP\b|defam\w*|libel\w*|slander\w*|privacy|date of birth|birth ?date|biography of)",
 "Neutral point of view noticeboard": r"(neutral\w*|\bNPOV\b|\bPOV\b|\bbias(ed)?\b|undue weight|\bundue\b|one-sided|whitewash\w*|puffery|non-neutral|balanced?\b)",
 "No original research noticeboard": r"(original research|\bOR\b|\bSYNTH\b|synthesis|improper synth\w*|own (research|analysis|interpretation|conclusion))",
 "Fringe theories noticeboard": r"(fringe|pseudo\w*|conspirac\w*|alternative medicine|paranormal|\bufos?\b|creationis\w*|quack\w*|homeopath\w*|astrolog\w*|cryptozoolog\w*|psychic|supernatural)",
 "Conflict of interest noticeboard": r"(\bCOI\b|conflict of interest|paid edit\w*|paid contribut\w*|undisclosed|autobiograph\w*|works? for (the|a|this)|employee|public relations|\bPR (firm|agency)|marketing (team|department|agency))",
 "Administrators' noticeboard/Incidents": r"(block(ed|ing)?\b|harass\w*|personal attack\w*|disrupt\w*|vandal\w*|edit[- ]?war\w*|sock\w*|threat\w*|incivil\w*|uncivil|abusive|\bban(ned)?\b|troll\w*|hound\w*|stalk\w*|legal threat|admin(istrator)? (action|attention|intervention))",
 "Village pump (technical)": r"(\btemplates?\b|\bscripts?\b|gadget\w*|\bbugs?\b|\bcss\b|javascript|\blua\b|\bmodules?\b|\bbots?\b|render\w*|browser|visualeditor|visual editor|\bapi\b|phabricator|error message|mediawiki|server|watchlist|\bfonts?\b|\bmobile\b|preferences|toolserver|special:)",
 "Help desk": r"(how (do|can|should) (i|we|you)|how to\b|is it possible to|can (i|someone|anyone) (please )?(help|tell|explain)|i('m| am) (new|trying)|my (article|draft|page|account|user ?name|edit)|create (an?|my|the) (article|page|account)|upload\w*)",
}
STRICT_RX = {k: re.compile(v, 0 if k == "No original research noticeboard" else re.I) for k, v in STRICT.items()}
VCUE_RX = {k: (re.compile(v, re.I if k not in ("No original research noticeboard",) else 0) if v else None) for k, v in VCUE.items()}
TS = re.compile(r"(\d{1,2}):(\d{2}), (\d{1,2}) (" + "|".join(MONTHS) + r") (\d{4}) \(UTC\)")


class Wiki:
    def __init__(self):
        import requests
        self.s = requests.Session()
        self.s.headers["User-Agent"] = C.UA + " (Wikipedia archive reader; low volume)"
        self.last = 0.0

    def get(self, params):
        for i in range(8):
            wait = 2.0 - (time.time() - self.last)
            if wait > 0:
                time.sleep(wait)
            self.last = time.time()
            r = self.s.get(API, params={**params, "format": "json", "formatversion": 2, "maxlag": 5}, timeout=120)
            if r.status_code == 200:
                try:
                    j = r.json()
                    if "error" not in j:
                        return j
                except ValueError:
                    pass
            time.sleep(10 * (i + 1))
        raise RuntimeError(f"API failed: {params}")

    def pages(self, titles=None, revids=None):
        """Return {title: (revid, content)} for existing pages."""
        p = {"action": "query", "prop": "revisions", "rvprop": "content|ids", "rvslots": "main"}
        if titles:
            p["titles"] = "|".join(titles)
        else:
            p["revids"] = "|".join(str(r) for r in revids)
        j = self.get(p)
        out = {}
        for pg in j["query"].get("pages", []):
            if pg.get("missing") or not pg.get("revisions"):
                continue
            rv = pg["revisions"][0]
            out[pg["title"]] = (rv["revid"], rv["slots"]["main"]["content"])
        return out


def cache_path(title):
    return C.CACHE / KEY / (hashlib.sha1(title.encode()).hexdigest() + ".json")


def load_or_fetch(wiki, pins, titles, batch):
    """Content for titles: from cache when pinned, else fetched (and pinned). Returns {title: content}."""
    out, need, need_rev = {}, [], []
    for t in titles:
        cp = cache_path(t)
        if t in pins and cp.exists():
            c = json.loads(cp.read_text())["content"]
            assert hashlib.sha256(c.encode()).hexdigest() == pins[t]["sha256"], t
            out[t] = c
        elif t in pins:
            if pins[t]["revid"]:
                need_rev.append(t)
        elif t not in pins:
            need.append(t)
    for i in range(0, len(need_rev), batch):
        chunk = need_rev[i:i + batch]
        got = wiki.pages(revids=[pins[t]["revid"] for t in chunk])
        for t, (rid, c) in got.items():
            assert hashlib.sha256(c.encode()).hexdigest() == pins[t]["sha256"], t
            cache_path(t).parent.mkdir(parents=True, exist_ok=True)
            cache_path(t).write_text(json.dumps({"title": t, "revid": rid, "content": c}))
            out[t] = c
    for i in range(0, len(need), batch):
        chunk = need[i:i + batch]
        got = wiki.pages(titles=chunk)
        for t in chunk:
            if t not in got:
                pins[t] = {"revid": None, "sha256": None}
                continue
            rid, c = got[t]
            pins[t] = {"revid": rid, "sha256": hashlib.sha256(c.encode()).hexdigest()}
            cache_path(t).parent.mkdir(parents=True, exist_ok=True)
            cache_path(t).write_text(json.dumps({"title": t, "revid": rid, "content": c}))
            out[t] = c
        PIN_FILE.write_text(json.dumps(pins, indent=0, sort_keys=True) + "\n")
    return out


def strip_templates(s):
    """Replace a few inline templates by their text and drop every other template (brace-matched)."""
    s = re.sub(r"\{\{\s*(?:u|user|ping|re|reply to|yo|replyto)\s*\|([^{}|]*)(?:\|[^{}]*)?\}\}", r"\1", s, flags=re.I)
    s = re.sub(r"\{\{\s*(?:tq|tqq|talkquote|xt|!xt|green|quote|q)\s*\|(?:1=)?([^{}]*)\}\}", r'"\1"', s, flags=re.I)
    s = re.sub(r"\{\{\s*(?:cite|citation)[^{}]*?\|\s*title\s*=\s*([^|{}]*)[^{}]*\}\}", r"(source: \1)", s, flags=re.I)
    s = re.sub(r"\{\{\s*(?:la|pagelinks|article|al|lw)\s*\|([^{}|]*)[^{}]*\}\}", r"\1", s, flags=re.I)
    s = re.sub(r"\{\{\s*(?:userlinks|userlinks-abuse|user5|vandal|ul|user-multi|checkuser|IPvandal|ipuser)\s*\|([^{}|]*)[^{}]*\}\}",
               r"\1", s, flags=re.I)
    out, depth, i = [], 0, 0
    while i < len(s):
        if s.startswith("{{", i):
            depth += 1
            i += 2
        elif s.startswith("}}", i) and depth:
            depth -= 1
            i += 2
        else:
            if depth == 0:
                out.append(s[i])
            i += 1
    return "".join(out)


def clean(s):
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    s = re.sub(r"<ref[^>]*/>|<ref[^>]*>.*?</ref>", " ", s, flags=re.S | re.I)
    s = strip_templates(s)
    s = re.sub(r"\{\|.*?\|\}", " [table] ", s, flags=re.S)
    s = re.sub(r"\[\[(?:User|User talk|Special:Contributions|Special:Contribs|Talk:User)[^\]]*\]\]", " ", s, flags=re.I)
    s = re.sub(r"\[\[(?:File|Image|Category):[^\]]*\]\]", " ", s, flags=re.I)
    s = re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]", r"\1", s)
    s = re.sub(r"\[\[([^\]]*)\]\]", r"\1", s)
    s = re.sub(r"\[https?://\S*(?:diff|oldid)=\S*(?:\s+([^\]]*))?\]", " [diff] ", s)
    s = re.sub(r"\[https?://\S+\s+([^\]]+)\]", r"\1", s)
    s = re.sub(r"\[?https?://\S+\]?", " <link> ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("'''", "").replace("''", "")
    s = TS.sub(" ", s)
    s = re.sub(r"[—-]*\s*Preceding (unsigned|undated) comment( was)? added (by|at)\b.*$", " ", s, flags=re.I | re.M)
    s = re.sub(r"\(\s*•\s*\)", " ", s)
    s = re.sub(r"\(\s*(?:[·•]\s*)+(?:e-?mail)?\s*\)", " ", s)
    s = re.sub(r"(?:--|—)?\s*\(\s*[^()\n]{1,40}\s*\)\s*;[\s;]*$", " ", s)
    s = re.sub(r"\s*\|\s*$", "", s)
    s = re.sub(r"\(\s*(talk|contribs|talk \| contribs)?\s*\)", " ", s)
    s = re.sub(r"(--|—|&mdash;|&nbsp;)\s*$", " ", s.strip())
    s = re.sub(r"&[a-z]+;", " ", s)
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    return s.strip(" \n-—~")


def first_posts(wikitext):
    """Yield (heading, first post, newest timestamp in thread) for each level-2 section."""
    parts = re.split(r"(?m)^==(?!=)\s*(.+?)\s*==\s*$", wikitext)
    for k in range(1, len(parts) - 1, 2):
        head, body = parts[k].strip(), parts[k + 1]
        stamps = [datetime.date(int(m.group(5)), MONTHS.index(m.group(4)) + 1, int(m.group(3))) for m in TS.finditer(body)]
        lines, keep = body.split("\n"), []
        for ln in lines:
            if re.match(r"^\s*[:*#]*:", ln) or re.match(r"^\s*=", ln):
                break
            keep.append(ln)
            if "(UTC)" in ln:
                break
        yield head, "\n".join(keep), (max(stamps) if stamps else None)


def thread_rows(title, wikitext, opt, q, stats):
    out = []
    for head, post, newest in first_posts(wikitext):
        if newest is None or newest.isoformat() >= CUTOFF:
            stats["no_date_or_late"] += 1
            continue
        h = clean(head)
        t = clean(post)
        if h.lower().startswith(("tech news", "archive", "wikipedia signpost")) or "MediaWiki message delivery" in post:
            stats["bot"] += 1
            continue
        if len(t) < (40 if q == "refdesk" else 80):
            stats["short"] += 1
            continue
        if q == "refdesk" and EDITING.search(t):
            stats["refdesk_about_editing"] += 1
            continue
        if opt == "Help desk" and not WIKI_CUE.search(t + " " + h):
            stats["helpdesk_not_about_wikipedia"] += 1
            continue
        if q == "venue" and VCUE_RX.get(opt) is not None:
            full = h + "\n" + t
            if not VCUE_RX[opt].search(full):
                stats["venue_cue_missing"] += 1
                continue
            if any(VCUE_RX[c].search(full) for c in VCONFLICT.get(opt, [])):
                stats["venue_cue_conflict"] += 1
                continue
        if q == "venue" and {k for k, rx in STRICT_RX.items() if rx.search(h + "\n" + t)} != {opt}:
            stats["venue_strict_cue_not_exclusive"] += 1
            continue
        if MOVED.search(t) or MOVED.search(h) or ABBR.search(t) or ABBR.search(h) or DESK_NAME.search(t + " " + h):
            stats["moved_or_venue_mention"] += 1
            continue
        if len(t) > 1400:
            cut = t[:1400]
            t = cut[:cut.rfind(". ") + 1] if ". " in cut[700:] else cut
            t = t.rstrip() + " [...]"
        state = (f"Heading: {h}\n" if h else "") + t
        rid = hashlib.sha1(f"{title}#{head}#{post[:200]}".encode()).hexdigest()[:16]
        out.append({"rid": rid, "state": state, "opt": opt, "q": q, "title": title, "date": newest.isoformat()})
    return out


def main():
    rng = random.Random(SEED)
    pins = json.loads(PIN_FILE.read_text()) if PIN_FILE.exists() else {}
    wiki = Wiki()
    stats = collections.Counter()
    ref_pool, venue_pool = collections.defaultdict(list), collections.defaultdict(list)
    # --- reference desks: seeded dates 2008-2021
    for desk in sorted(DESKS):
        dates, r2 = [], random.Random(f"{SEED}:{desk}")
        while len(dates) < REF_PAGES_PER_DESK:
            d = datetime.date(2008, 1, 1) + datetime.timedelta(days=r2.randrange((datetime.date(2021, 12, 31) - datetime.date(2008, 1, 1)).days))
            if d not in dates:
                dates.append(d)
        titles = [f"Wikipedia:Reference desk/Archives/{desk}/{d.year} {MONTHS[d.month - 1]} {d.day}" for d in dates]
        got = load_or_fetch(wiki, pins, titles, 20)
        for t in titles:
            if t in got:
                ref_pool[desk] += thread_rows(t, got[t], DESK_OPT[desk], "refdesk", stats)
    # --- venues: seeded archive numbers until the cap is reachable
    for opt in sorted(VENUES):
        pat, rngn, _ = VENUES[opt]
        r2 = random.Random(f"{SEED}:{opt}")
        if rngn is None:
            cands = []
            while len(cands) < VENUE_PAGES_MAX:
                d = datetime.date(2010, 1, 1) + datetime.timedelta(days=r2.randrange((datetime.date(2021, 12, 31) - datetime.date(2010, 1, 1)).days))
                t = pat.format(date=f"{d.year} {MONTHS[d.month - 1]} {d.day}")
                if t not in cands:
                    cands.append(t)
        else:
            nums = list(range(rngn[0], rngn[1] + 1))
            r2.shuffle(nums)
            cands = [pat.format(n=n) for n in nums[:VENUE_PAGES_MAX]]
        pool = []
        for i in range(0, len(cands), 5):
            if len(pool) >= VENUE_CAP * 1.6:
                break
            chunk = cands[i:i + 5]
            got = load_or_fetch(wiki, pins, chunk, 20 if rngn is None else 5)
            for t in chunk:
                if t in got:
                    pool += thread_rows(t, got[t], opt, "venue", stats)
        venue_pool[opt] = pool
    PIN_FILE.write_text(json.dumps(pins, indent=0, sort_keys=True) + "\n")
    # --- rows
    seen, rows = set(), []
    for pools, cap, opts_all, q, instr in ((venue_pool, VENUE_CAP, sorted(VENUES), "venue", VENUE_Q),
                                           (ref_pool, REF_PER_DESK, sorted(DESK_OPT.values()), "refdesk", REFDESK_Q)):
        for k in sorted(pools):
            items = sorted(pools[k], key=lambda x: x["rid"])
            rng.shuffle(items)
            n = 0
            for it in items:
                nn = C.norm(it["state"])
                if nn in seen or n >= cap:
                    continue
                seen.add(nn)
                n += 1
                edge = "long_context" if len(it["state"]) > 1100 else None
                rows.append({"key": KEY, "rid": it["rid"], "state": it["state"], "instructions": instr, "options": opts_all,
                             "gold": it["opt"], "soft": None,
                             "meta": {"dataset": "English Wikipedia help-desk and noticeboard archives (MediaWiki API)",
                                      "config": f"q={q}; page={it['title']}",
                                      "revision": f"revid:{pins[it['title']]['revid']}; sha256:{pins[it['title']]['sha256']}",
                                      "licence": LICENCE, "split": "train",
                                      "orig_label": {"page": it["title"], "thread_date": it["date"]},
                                      "family": C.FAMILY, "edge": edge, "defs": q, "seed": SEED}})
    rows = C.cap_label(rows, lambda r: r["gold"], 0.5)
    rng.shuffle(rows)
    rows = C.near_dedupe(rows)
    out, rows = C.write_rows(rows, KEY)
    C.write_defs({DESK_OPT[d]: v for d, v in DESKS.items()}, KEY, "refdesk")
    C.write_defs({o: v[2] for o, v in VENUES.items()}, KEY, "venue")
    print(dict(stats))
    print("refdesk pool:", {k: len(v) for k, v in sorted(ref_pool.items())})
    print("venue pool:", {k: len(v) for k, v in sorted(venue_pool.items())})
    print(f"wrote {len(rows)} -> {out}")
    C.report(rows)


if __name__ == "__main__":
    main()
