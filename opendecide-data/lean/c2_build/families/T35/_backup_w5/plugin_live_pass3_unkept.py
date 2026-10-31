"""families/T35/plugin.py: T35 "path-rule access, robots-style" (C2_DATA_SPEC 2.1, 3.2; PREREG_FINAL A37).

A robots.txt file (1-6 groups, 1-8 Allow / Disallow lines with "*" and a final "$"), a crawler product token, a URL
and, on some rows, the fetch status of robots.txt. Yes/no forms ask whether the crawler may fetch the URL; the choice
form asks which line decides. The card states every rule (RFC 9309 semantics, written out; the card is the only law):
group choice, prefix matching with "*" and "$", percent-decoding of ASCII unreserved characters only, longest pattern
wins, Allow wins a tie at equal length, no applying match = may fetch, and the robots.txt status overrides the lines
(4xx = fetch anything, 5xx or no response = fetch nothing). Yes/no rows carry the card in row.card (printed once as the
definitions block); choice rows keep it in the instructions. Semantics: G0_SPEC.md (frozen sha below; ambiguity pass
H1-H33).

  solver A   trie longest match: the applying lines go into one character trie ("*" and "$" are trie edges); one
             depth-first walk of the decoded path collects every matching line; the longest pattern wins, Allow on a
             tie; group choice through a token index; status by integer class      paradigm trie_longest_match
  solver B   solver_b.py: its own parser of the RENDERED row; each line compiled to a regular expression and tested
             one by one; an explicit pairwise length comparison picks the decider; table lookups for status and
             question                                                              paradigm regex_compile
  samplers   S1 forward; S2 label-first near-miss; S3 table-first (rules as a table); S4 group conflicts and fetch
             status; S5 held out (rules as JSON, held-out skins)
  questions  yn_fetch (and yn_double_neg, its double-negation form); complements yn_skip (antonym),
             yn_not_allowed (syntactic), yn_prevented (implicit);
             ch_line "which line decides" (open set from error models + "no line matches")
  relations  complement; minimal-edit twin (the deciding line's effect, or the fetch status); equiv (another rules
             container and skin); inv (one attack line); G4 metamorphic (rename the site, token case, shuffle lines,
             add an inert line, percent-encode a path character, rotate groups)
  packs      G0 section 6: T35Plugin() reads the frozen pools by default (load_pools: sha256 = pools/manifest.json):
             8 program packs + 40 Haiku site packs (8 held out: S5 only), 8 program + 48 Haiku operators. The program
             slugs Haiku section and page names into path segments and file names (slug, page_endings). Card =
             sampler + pack: training packs are dealt over S1-S4 by a hash of the pack id (card_packs); the pack of a
             row comes from its seed alone, before any outcome is tried. PACKS / OPERATORS are stand-ins for tests.
  fix iter 1 (14 Oct 2026; PILOT_VERDICT F1-F4, G0 v4): F1 wording polarity (c2_kit.polarity; no admitted double-negation
             wording passes yet, so yn_double_neg is not drawn); F2 4xx / 5xx statuses capped (they decide alone, so G6's
             metadata view reads them), a status line stays on ~15% of rows; F3 the ch_line display plan (ChoicePlan: k,
             "no line matches" gold exactly 1/k, position, length rank) fixed by the seed's place in a stratified stream
             before any structure, look-alike wrong lines, no query string; F4 46.6% choice base slots (the 70/30 split is
             of ROWS); cards: full / compact / short styles, the status item only with a status line, rules placed by
             cards.place_rules (yes/no row.card, choice instructions).
urllib.robotparser is never used (spec 3.2). Code only: nothing here writes a file (A37 f); it reads the frozen pools.
"""
from __future__ import annotations

import hashlib
import json
import random
import re
import string
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlsplit

from c2_kit import cards as CARDS
from c2_kit import polarity as POL
from c2_kit import skin as K
from c2_kit import slots as S
from c2_kit.choiceplan import ChoicePlan
from c2_kit.distractors import build_options, error_model, register_name, uhash
from c2_kit.lexicon import question_sem
from c2_kit.plugin import C2Plugin, ContractError, QuestionForm, RelationProposal, Spec, choose_forms
from c2_kit.rows import TextBuilder, assemble_row

HERE = Path(__file__).resolve().parent
FAMILY = "T35"

EFFECTS = {"allow": ["Allow"], "disallow": ["Disallow"]}
EFFECT_KEYS = ("allow", "disallow")
STATUS = {"200": ["200 OK"], "401": ["401 Unauthorized"], "403": ["403 Forbidden"], "404": ["404 Not Found"],
          "410": ["410 Gone"], "500": ["500 Internal Server Error"], "502": ["502 Bad Gateway"],
          "503": ["503 Service Unavailable"], "unreachable": ["no response (server unreachable)"]}
STATUS_4XX = ("401", "403", "404", "410")
STATUS_5XX = ("500", "502", "503", "unreachable")
PURPOSES = {"indexing": ["search indexing"], "archiving": ["web archiving"], "prices": ["price comparison"],
            "accessibility": ["accessibility checks"], "links": ["link checking"], "research": ["academic research"],
            "previews": ["link previews"]}
UNRESERVED = frozenset(string.ascii_letters + string.digits + "-._~")
HEX = frozenset(string.hexdigits)
NONE_KEY = "none"
NONE_TEXT = "No applying line matches (so the crawler may fetch the URL)"
LONGEST_SEM = "prec.robots_longest"
TIE_SEM = "prec.robots_tie_allow"
POS_FORM = "yn_fetch"
DOUBLE_NEG_FORM = "yn_double_neg"   # positive polarity, two syntactic negations (spec 3.0: >= 2% of yes/no)
NEG_FORMS = ("yn_skip", "yn_not_allowed", "yn_prevented")
CHOICE_FORM = "ch_line"
# The negative / antonym predicates of "may fetch" (c2_kit.polarity rule P1-P3; pilot G5-H fix F1). A question wording
# negates the permission syntactically ("not allowed", "not permitted") OR uses one of these, never both: "is it not
# the case that they do not bar the crawler ...?" reads "yes = the crawler may NOT fetch", the reverse of
# yn_double_neg (3 confirmed wrong golds). negcount's own implicit cues (deny, lack, prevent ... from, refuse to,
# rule out, without ...) count too; these are the ones negcount does not list.
NEGATIVE_PREDICATES = (
    r"bar(?:s|red|ring)?", r"block(?:s|ed|ing)?", r"clos(?:e|es|ed|ing)", r"exclud(?:e|es|ed|ing)",
    r"forbid(?:s|den|ding)?|forbade", r"prohibit(?:s|ed|ing)?", r"ban(?:s|ned|ning)?", r"stop(?:s|ped|ping)?",
    r"(?:keep|keeps|kept|keeping)\s+(?:\w+\s+){0,3}?(?:away|out|clear|off)",
    r"(?:hold|holds|held|holding)\s+(?:\w+\s+){0,3}?back", r"off-limits", r"out\s+of\s+bounds",
    r"breach(?:es|ed|ing)?", r"violat(?:e|es|ed|ing|ion)", r"skip(?:s|ped|ping)?", r"pass(?:es|ed|ing)?\s+over",
    r"(?:stay|stays|stayed|staying)\s+(?:out|clear|away)", r"disallow(?:s|ed|ing)?", r"leave\s+it\s+alone",
    r"restrict(?:s|ed|ing)?", r"withh(?:o|e)ld(?:s|ing)?", r"reject(?:s|ed|ing)?",
)
MAX_LINES = 8
MAX_GROUPS = 6
MAX_TRIES = 1000
RELAX_AFTER = 0       # A45 b: a ch_line file with more groups than planned is trimmed, not rejected (relax-after-300 was tried: G6 choice b_options lr 0.337)

# shares (G0_SPEC.md section 3)
# F4 (pilot verdict): the 70% yes/no share of spec 3.2 is measured on ROWS. Yes/no bases carry about 2.2 rows each (partners
# and twins), choice bases about 1.2, so 46.6% of the base slots are choice (N_CHOICE_SLOTS of W_SLOTS); the 70/30 row
# split then follows. Slots are stratified per sampler (blocks of W_SLOTS seeds), not drawn independently: at ~300 choice
# rows an independent draw moves G10's gold-is-longest by +/- 2.6 pp (one SD) against a +/- 2 pp bar.
W_SLOTS = 88                    # seeds per slot block (per sampler)
N_CHOICE_SLOTS = 41             # choice bases per block (46.6%)
P_DOUBLE_NEG = 0.12             # 4-base blocks whose positive-polarity yes/no bases use the double-negation form
CARD_SHARES = {"full": 0.20, "compact": 0.65, "short": 0.15}   # card styles (G0 M17-M18); short is the spec 3.0 15%
P_NONMATCH_ALLOW = 0.30         # yes/no rows whose lines allow: by no matching line (else an Allow line decides)
P_COMPLEMENT = 0.45             # yes/no bases that get a complement partner
P_TWIN = 0.90                   # yes/no bases that get a minimal-edit twin (when one exists)
P_TWIN_FROM_200 = 0.10          # a base that shows a 2xx status takes the status twin (-> 4xx / 5xx) with this chance
P_EQUIV = 0.13
P_INV = 0.09
NEG_PARTNER = (("yn_skip", 0.40), ("yn_not_allowed", 0.30), ("yn_prevented", 0.30))
P_PAIR = {"allow": 0.08, "disallow": 0.22, "nomatch": 0.20}   # identical-pattern pairs that do not decide
P_NEAR_OPP = 0.8          # longer near misses (no match) take the losing effect (G6: longest-line cue)
P_SUPPORT = 1.0           # shorter matching same-effect supporters, relative to p_short_opp (G6: majority)
P_UNRELATED = 0.30        # an unrelated line in the applying group
P_UNREL_SAME = 0.8        # ... with the deciding effect
P_CAPS = 0.60            # URL paths with one capitalised segment or file name (label-blind): lines with capitals
                          # then match as often as other lines, and case near misses go both ways (review fix: with
                          # all-lowercase paths a capital marked a non-matching line, gold on 2.9% of its showings)

CLOSED_WORLD = ("The file is the robots.txt of the URL's site, and the file, the request and these rules are complete: "
                "nothing else changes the answer.")
CARD_BODY = {   # G0_SPEC.md M17-M19 (ambiguity pass H7, H10-H12: applying lines, own default item); styles full, compact, short
    "full": ('Robots rules (they decide this request):\n'
             '1. Group: a group applies if one of its User-agent values equals the crawler\'s product token, '
             'ignoring case (equal, not just a prefix). All applying groups are combined. If none applies, the "*" '
             'group applies; if there is none, no group applies. The lines of the applying groups are the applying '
             'lines; no other line counts.\n'
             '2. Path: the URL from the first "/" after the host, query included (the path to check). Decode each '
             '"%XX" that encodes an ASCII letter, digit, "-", ".", "_" or "~"; keep every other "%XX" as written.\n'
             '3. Match: a line matches if its pattern matches the start of the path. "*" matches any run of '
             'characters (even empty, even "/"); a final "$" means the path must end there; every other character '
             'must match exactly, case-sensitive.\n'
             '4. {LONGEST}\n'
             '5. {TIE}\n'
             '6. If no applying line matches, the crawler may fetch the URL.\n'),
    "compact": ('Robots rules:\n'
                '1. Group: a group applies if a User-agent value equals the crawler\'s token, ignoring case (equal, '
                'not a prefix); all applying groups are combined. If none applies, the "*" group applies; if there is '
                'none, no group applies. Their lines are the applying lines; no other line counts.\n'
                '2. Path: the URL from the first "/" after the host, query included. Decode each "%XX" for an ASCII '
                'letter, digit, "-", ".", "_" or "~"; keep every other "%XX" as written.\n'
                '3. Match: a line matches if its pattern matches the start of the path: "*" matches any run (even '
                'empty, even "/"); a final "$" means the path must end there; every other character must match '
                'exactly, case-sensitive.\n'
                '4. {LONGEST}\n'
                '5. {TIE}\n'
                '6. If no applying line matches, the crawler may fetch the URL.\n'),
    "short": ('Robots rules, short form:\n'
              '- Group: the groups whose User-agent value equals the crawler\'s token (case ignored; all combined), '
              'else the "*" group, else none; only their lines apply.\n'
              '- Path: the URL from the first "/" after the host, query included; decode "%XX" only for ASCII '
              'letters, digits, "-", ".", "_" and "~".\n'
              '- Match: a pattern matches the start of the path; "*" is any run ("/" and empty included); a final '
              '"$" means the path ends there; case matters.\n'
              '- {LONGEST}\n'
              '- {TIE}\n'
              '- No applying line matches: may fetch.\n'),
}
CARD_STATUS = {   # the status item: on a card only when the request block shows a fetch status (G0 M17: a rule the answer cannot need is not stated)
    "full": ('7. robots.txt fetch status, which overrides items 1-6: 2xx or none shown: use the lines. 4xx: the '
             'crawler may fetch any URL on the site. 5xx or no response: it may fetch none.\n'),
    "compact": ('7. robots.txt fetch status overrides items 1-6: 2xx or none shown: use the lines; 4xx: it may fetch '
                'any URL; 5xx or no response: it may fetch none.\n'),
    "short": ('- robots.txt status (overrides the lines): 4xx: may fetch any URL; 5xx or no response: may fetch '
              'none; 2xx or none shown: use the lines.\n'),
}


def card_template(style: str, with_status: bool) -> str:
    """The card text of a style (a {LONGEST} / {TIE} template): its items, the status item when the request shows a fetch
    status, and the closed-world sentence last."""
    return CARD_BODY[style] + (CARD_STATUS[style] if with_status else "") + CLOSED_WORLD


RAW_HEAD = "robots.txt of the site:\n=== begin robots.txt ==="
RAW_TAIL = "=== end robots.txt ==="
TABLE_HEAD = ("robots.txt of the site, one table row per line (rows with the same group number form one group):\n"
              "| group | line | value |\n|---|---|---|")
JSON_HEAD = "robots.txt of the site, as parsed into JSON by the site's tools:"   # key "pattern" (H22), not "path"
REQUEST_TPL = ("Fetch request:\n- crawler product token: {UA}\n- URL: {URL}\n"
               "- path to check (query included): {PATH:raw}")
STATUS_LINE = "\n- robots.txt fetch status: {STATUS}"


@dataclass(frozen=True)
class Pack:
    """A domain pack (site type): site names, path segments and file names. A program pack writes them directly; a
    Haiku site pack (pools/packs.json) gives site names and plain-word section and page names, which the program slugs
    into path segments and file names (pack_from_pool; G0 section 6). Either way the program writes every path,
    pattern, URL and status (spec 3.2). held_out packs feed S5 only, and S5 only them."""
    pack_id: str
    sites: tuple
    segs: tuple
    files: tuple
    held_out: bool = False


PACKS = (
    Pack("t35-garden-shop", ("Larkspur Gardens", "Fennel Row Nursery", "Copperbeech Growers"),
         ("plants", "seeds", "tools", "cart", "checkout", "account", "care-guides", "wholesale", "search"),
         ("index.html", "catalog.pdf", "spring-list.html", "photo.jpg")),
    Pack("t35-bookshop", ("Quillmere Books", "Harbor Lantern Books", "Ashgrove Booksellers"),
         ("books", "authors", "events", "cart", "account", "staff-picks", "search", "used", "gift-cards"),
         ("index.html", "reading-list.pdf", "signing.html", "cover.jpg")),
    Pack("t35-local-news", ("Tidewater Courier", "Millbrook Ledger", "Ridgeway Herald"),
         ("news", "opinion", "archive", "drafts", "press", "media", "tag", "live", "search"),
         ("story.html", "print.pdf", "gallery.jpg", "feed.xml")),
    Pack("t35-recipes", ("Brambleworth Kitchen", "Saffron Lane Recipes", "Oatfield Table"),
         ("recipes", "menus", "videos", "print", "members", "collections", "drafts", "search"),
         ("index.html", "card.pdf", "step-photo.jpg", "list.json")),
    Pack("t35-city-portal", ("Eastmere City Portal", "Kingsford Town Hall", "Larchmont Civic Office"),
         ("permits", "council", "minutes", "forms", "staff", "notices", "intranet", "search"),
         ("index.html", "agenda.pdf", "form.pdf", "map.png")),
    Pack("t35-bike-shop", ("Harrowgate Cycles", "Spokewright Bikes", "Fellside Wheels"),
         ("bikes", "parts", "repairs", "booking", "rentals", "cart", "account", "search"),
         ("index.html", "price-list.pdf", "fit-guide.html", "frame.jpg")),
    Pack("t35-museum", ("Gallowhill Museum", "Westerby Art House", "Cobblestone Heritage Trust"),
         ("collection", "exhibitions", "tickets", "press", "images", "members", "research", "search"),
         ("index.html", "floor-plan.pdf", "object.html", "scan.jpg")),
    Pack("t35-forum", ("Riverlight Forum", "Pinecrest Boards", "Lowmoor Community"),
         ("threads", "users", "private", "messages", "attachments", "tags", "admin", "search"),
         ("index.html", "rules.html", "export.json", "avatar.png")),
)
PACK_BY_ID = {p.pack_id: p for p in PACKS}
OPERATORS = (("Fernhill Labs", "FernhillBot"), ("Ostrander Data", "OstraBot"), ("Maplewick Search", "MaplewickBot"),
             ("Corvid Analytics", "CorvidCrawler"), ("Pellucid Archive", "PellucidArchiver"),
             ("Saltmarsh Research", "SaltmarshSpider"), ("Brightloom Prices", "BrightloomBot"),
             ("Kestrel Links", "KestrelLinkBot"))
OTHER_AGENTS = ("Ravenscan", "Duskcrawl", "Heronbot", "Lumenfetch", "Thistlebot", "Moorhen-Crawler", "Gullwing",
                "Sedgebot")
LOOKALIKE_SUFFIXES = ("-Image", "-News", "-Mobile", "-Ads", "-Video")
QUERY_KEYS = ("q", "page", "sort", "ref", "sessionid", "lang")
QUERY_VALUES = ("spring", "2", "new", "home", "a1b2", "en", "price", "15")
INERT = ("/legacy-feeds/", "/old-staging/", "/wp-snapshots/", "/tmp-exports/", "/beta-labs/", "/cgi-old/")
MODES = ("named", "star", "combined", "nogroup")

# ------------------------------------------------------------------------------------------------ pools (G0 section 6)
POOLS = HERE / "pools"
POOL_FILES = ("packs.json", "operators.json")
TRAIN_SAMPLERS = ("S1", "S2", "S3", "S4")
MIN_TRAIN_PACKS = 25                       # spec 3.0: every family uses >= 25 packs, one pack per card
SITE_PACK_SHAPE = (3, 8, 4)                # a Haiku site pack: 3 site names, 8 section names, 4 page names
WORDS_RE = re.compile(r"[a-z]+(?: [a-z]+)*")              # a Haiku section or page name: plain lowercase words
SLUG_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")         # a slug: letters, digits and "-" only
TOKEN_RE = re.compile(r"[A-Z][A-Za-z]{5,15}")             # a product token: CamelCase letters, 6-16 of them
PAGE_ENDINGS = (".html", ".pdf", ".jpg", ".png", ".json", ".xml")   # never ".txt": no request is for /robots.txt (H17)
INERT_SEGS = frozenset(p.strip("/").split("/")[0] for p in INERT)
PATH_BUDGET = 24                # characters of a path's segments + file name (query excluded); see _gen_path


def slug(words: str) -> str:
    """A section or page name -> a path segment: its words joined by "-". The result must hold only letters, digits
    and "-" (lowercase); anything else is refused, never repaired."""
    s = "-".join(words.split()) if isinstance(words, str) else ""
    if not SLUG_RE.fullmatch(s):
        raise ContractError(f"slug of {words!r}: lowercase letters, digits and '-' only")
    return s


def page_endings(pack_id: str, n: int = 4) -> tuple:
    """The file endings of a pack's pages, in page order: n different ones from PAGE_ENDINGS in an order hashed from
    the pack id alone (fixed per pack before any row is drawn, so label-blind)."""
    if not 1 <= n <= len(PAGE_ENDINGS):
        raise ContractError(f"pack {pack_id}: {n} pages (1-{len(PAGE_ENDINGS)})")
    return tuple(sorted(PAGE_ENDINGS, key=lambda e: uhash(FAMILY, "ending", pack_id, e))[:n])


def pack_from_pool(rec: dict) -> Pack:
    """One frozen Haiku site pack (a pools/packs.json record) -> a Pack: sections slugged into path segments, pages
    slugged and given their endings (page_endings). A record that breaks the G0 section 6 shape is refused."""
    pid = rec.get("pack_id") if isinstance(rec, dict) else None
    if not isinstance(pid, str) or not re.fullmatch(r"[A-Za-z0-9-]+", pid):
        raise ContractError(f"site pack {pid!r}: pack_id")
    names, secs, pages = rec.get("site_names"), rec.get("sections"), rec.get("pages")
    for field, items, k in (("site_names", names, SITE_PACK_SHAPE[0]), ("sections", secs, SITE_PACK_SHAPE[1]),
                            ("pages", pages, SITE_PACK_SHAPE[2])):
        if not (isinstance(items, list) and len(items) == k and len(set(items)) == k
                and all(isinstance(x, str) for x in items)):
            raise ContractError(f"site pack {pid}: {field} must be {k} distinct strings")
    for nm in names:
        try:
            S.name_slot(nm)                                   # G-SL value rules (no digit, no negation cue)
            S.url_slot(f"https://{_host(nm)}/")               # the host is a reserved example name
        except S.SlotError as e:
            raise ContractError(f"site pack {pid}: {e}") from None
    for x in secs + pages:
        if not WORDS_RE.fullmatch(x):
            raise ContractError(f"site pack {pid}: {x!r} is not plain lowercase words")
    segs = tuple(slug(x) for x in secs)
    if INERT_SEGS & set(segs):
        raise ContractError(f"site pack {pid}: a section slug equals an inert G4 pattern")
    files = tuple(slug(x) + e for x, e in zip(pages, page_endings(pid, len(pages))))
    held = rec.get("held_out")
    if not isinstance(held, bool):
        raise ContractError(f"site pack {pid}: held_out must be true or false")
    return Pack(pid, tuple(names), segs, files, held)


def token_problems(tokens) -> list:
    """M4: group choice is equality, never prefix, so no product token (OTHER_AGENTS included) may equal or be a
    prefix of another, ignoring case; a look-alike group (token + suffix) then never names another crawler."""
    low = [t.lower() for t in tokens]
    return [f"tokens {a!r} / {b!r}: equal or a prefix, ignoring case" for i, a in enumerate(low) for b in low[i + 1:]
            if a.startswith(b) or b.startswith(a)]


def pool_problems(packs, operators) -> list:
    """Every pack and operator rule the sampler relies on (G0 section 6); empty = usable."""
    probs = []
    ids = [p.pack_id for p in packs]
    if len(set(ids)) != len(ids):
        probs.append("pack ids repeat")
    sites = [s for p in packs for s in p.sites]
    if len(set(sites)) != len(sites):
        probs.append("a site name is in two packs")
    for p in packs:
        if len(p.sites) < 2 or len(set(p.segs)) != len(p.segs) or len(p.segs) < 3 or not p.files \
                or len(set(p.files)) != len(p.files):
            probs.append(f"pack {p.pack_id}: >= 2 sites, >= 3 distinct segments, distinct file names")
        if len({_host(s) for s in p.sites}) != len(p.sites):
            probs.append(f"pack {p.pack_id}: two sites share a host (the first word of the name)")
        for x in p.segs + p.files:
            if not re.fullmatch(r"[a-z0-9]+(?:[-.][a-z0-9]+)*", x) or x.endswith(".txt"):
                probs.append(f"pack {p.pack_id}: path piece {x!r}")
    names = [o for o, _t in operators]
    if len(set(names)) != len(names) or set(names) & set(sites):
        probs.append("operator names repeat or equal a site name")
    for o, t in operators:
        try:
            S.name_slot(o)
            S.id_slot(t)
        except S.SlotError as e:                              # the G-SL value rules
            probs.append(f"operator {o!r} / {t!r}: {e}")
        if not TOKEN_RE.fullmatch(t):
            probs.append(f"token {t!r}: CamelCase letters, 6-16")
    probs += token_problems([t for _o, t in operators] + list(OTHER_AGENTS))
    return probs


def load_pools(root: Path = POOLS) -> tuple:
    """(packs, operators) for a build: the 8 program packs + every frozen Haiku site pack, the 8 program operators +
    every Haiku operator. Each pool file must hash to its sha256 in pools/manifest.json (the files are frozen and
    never rewritten here); >= 25 training packs and >= 1 held-out pack (S5), or the load is refused."""
    man = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    docs = {}
    for name in POOL_FILES:
        raw = (root / name).read_bytes()
        if hashlib.sha256(raw).hexdigest() != man.get("sha256", {}).get(name):
            raise ContractError(f"pools/{name}: sha256 differs from pools/manifest.json (frozen pool changed)")
        docs[name] = json.loads(raw.decode("utf-8"))
    packs = PACKS + tuple(pack_from_pool(r) for r in docs["packs.json"])
    ops = []
    for r in docs["operators.json"]:
        if r.get("held_out") is not False:
            raise ContractError(f"operator {r.get('operator')!r}: G0 defines training operators only")
        ops.append((r["operator"], r["token"]))
    n_train = sum(not p.held_out for p in packs)
    if n_train < MIN_TRAIN_PACKS or n_train == len(packs):
        raise ContractError(f"{n_train} training packs (>= {MIN_TRAIN_PACKS}) and "
                            f"{len(packs) - n_train} held-out packs (>= 1)")
    return packs, OPERATORS + tuple(ops)


def card_packs(packs) -> dict:
    """{sampler: packs}. Card = sampler + pack (spec 3.0: one pack per card): the training packs, ordered by a hash of
    the pack id, are dealt round robin over S1-S4, so each sits in exactly one training sampler; S5 gets the held-out
    packs and no other."""
    train = sorted((p for p in packs if not p.held_out), key=lambda p: uhash(FAMILY, "card", p.pack_id))
    out = {s: tuple(train[i::len(TRAIN_SAMPLERS)]) for i, s in enumerate(TRAIN_SAMPLERS)}
    out["S5"] = tuple(p for p in packs if p.held_out)
    return out


@dataclass(frozen=True)
class Cfg:
    """Sampler shape parameters (G0_SPEC.md section 3). Every display choice is label-blind."""
    containers: tuple
    modes: tuple              # weights for MODES
    p_status: float           # yes/no bases that show a fetch status line (spec 3.2: about 15% of rows overall)
    p_ns: float               # ... of which the status is 4xx / 5xx (it then decides alone; G6 caps these rows, F2)
    p_tie: float              # Allow-decided rows that get an equal-length Disallow partner
    p_first_wrong: float      # rows whose first listed matching line is put first on purpose
    p_conflict: float         # the non-applying group gives the opposite outcome
    p_percent: float          # URL path holds %XX codes
    p_short_opp: float        # a shorter matching line of the opposite effect
    p_decoy_tie: float        # an equal-length opposite line that does not match
    n_near: tuple             # near-miss lines (draw)
    n_other: tuple            # unrelated agent groups (draw)


CFG = {
    "S1": Cfg(("robots",), (0.42, 0.43, 0.07, 0.08), 0.12, 0.08, 0.80, 0.10, 0.15, 0.10, 0.45, 0.25, (0, 1, 1, 2),
              (0, 0, 1, 1, 2)),
    "S2": Cfg(("robots",), (0.45, 0.55, 0.0, 0.0), 0.12, 0.08, 0.90, 0.30, 0.10, 0.08, 0.70, 0.35, (1, 1, 2), (0, 1)),
    "S3": Cfg(("table",), (0.42, 0.43, 0.07, 0.08), 0.12, 0.08, 0.80, 0.10, 0.15, 0.10, 0.45, 0.25, (0, 1, 1, 2),
              (0, 0, 1, 1, 2)),
    "S4": Cfg(("robots",), (0.38, 0.30, 0.16, 0.16), 0.30, 0.09, 0.65, 0.10, 0.50, 0.10, 0.45, 0.20, (0, 1, 1),
              (1, 1, 2, 2)),
    "S5": Cfg(("json",), (0.42, 0.43, 0.07, 0.08), 0.12, 0.08, 0.80, 0.10, 0.15, 0.10, 0.45, 0.25, (0, 1, 1, 2),
              (0, 0, 1, 1, 2)),
}

for _name, _text in (
        ("robots_disallow_wins_tie", "lets the Disallow line win a tie in pattern length"),
        ("robots_allow_wins", "lets the longest matching Allow line win, whatever the Disallow lines say"),
        ("robots_length_literals_only", "measures pattern length without the '*' and '$' characters"),
        ("robots_star_group_over_named", "uses the '*' group although a group names the crawler"),
        ("robots_lookalike_group", "uses a group whose token only looks like the crawler's token"),
        ("robots_first_group_only", "uses only the first of several groups that name the crawler"),
        ("robots_merge_star_group", "adds the '*' group's lines to the crawler's own group"),
        ("robots_ignore_end_anchor", "ignores a final '$' and matches the pattern as a plain prefix"),
        ("robots_star_stops_at_slash", "lets '*' match any run except '/'"),
        ("robots_whole_path", "requires the pattern to match the whole path, not just its start"),
        ("robots_no_percent_decode", "matches against the path without decoding its %XX codes"),
        ("robots_path_case_ignored", "ignores letter case when matching a pattern to the path"),
        ("robots_query_ignored", "matches against the path with its query string removed")):
    register_name(_name, _text)


# ------------------------------------------------------------------------------------------------ semantics (A side)

def raw_path(url: str) -> str:
    """The URL from the first "/" after the host, query included, exactly as written (no decoding)."""
    sp = urlsplit(url)
    return (sp.path or "/") + (f"?{sp.query}" if sp.query else "")


def decode(raw: str) -> str:
    """Decode each %XX that stands for an unreserved character (letter, digit, - . _ ~); keep every other %XX."""
    out, i, n = [], 0, len(raw)
    while i < n:
        if raw[i] == "%" and i + 3 <= n and raw[i + 1] in HEX and raw[i + 2] in HEX:
            ch = chr(int(raw[i + 1:i + 3], 16))
            if ch in UNRESERVED:
                out.append(ch)
                i += 3
                continue
        out.append(raw[i])
        i += 1
    return "".join(out)


class _Node:
    __slots__ = ("kids", "star", "ends", "anchored")

    def __init__(self):
        self.kids, self.star, self.ends, self.anchored = {}, None, [], []


def _trie(patterns: dict) -> _Node:
    """One character trie over {line no: pattern}; "*" is a star edge, a final "$" marks an anchored end."""
    root = _Node()
    for n, pat in patterns.items():
        anchored = pat.endswith("$")
        node = root
        for c in (pat[:-1] if anchored else pat):
            if c == "*":
                if node.star is None:
                    node.star = _Node()
                node = node.star
            else:
                node = node.kids.setdefault(c, _Node())
        (node.anchored if anchored else node.ends).append(n)
    return root


def _trie_hits(root: _Node, path: str) -> set:
    """Every line whose pattern matches the start of `path` (an anchored one: all of it), by one DFS of the trie."""
    hits, seen, stack, n = set(), set(), [(root, 0)], len(path)
    while stack:
        node, i = stack.pop()
        if (id(node), i) in seen:
            continue
        seen.add((id(node), i))
        hits.update(node.ends)
        if i == n:
            hits.update(node.anchored)
        if node.star is not None:
            stack.extend((node.star, j) for j in range(i, n + 1))
        if i < n and path[i] in node.kids:
            stack.append((node.kids[path[i]], i + 1))
    return hits


def status_class(key) -> str:
    if key is None:
        return "2xx"
    return "5xx" if key == "unreachable" else f"{int(key) // 100}xx"


@dataclass(frozen=True)
class Decision:
    allowed: bool          # the answer to "may the crawler fetch the URL?"
    by: str                # status_4xx | status_5xx | line | nomatch | nogroup
    rules_allowed: bool    # what the lines alone decide (status ignored)
    rules_by: str          # line | nomatch | nogroup
    winners: tuple         # longest matching lines of the winning effect (one on every ch_line row)
    tie: bool              # an Allow and a Disallow line share the longest length
    matched: tuple         # matching applying lines, file order
    applying: tuple        # applying lines, file order
    how: str               # named | star | none


def applying(spec: Spec) -> tuple:
    """(applying line numbers in file order, how): token index lookup, else the "*" groups, else nothing."""
    env = spec.env()
    index: dict = {}
    for gi, g in enumerate(spec.structure["groups"]):
        for a in g["agents"]:
            index.setdefault("*" if a == "*" else env[a].lower(), set()).add(gi)
    named = index.get(env["UA"].lower())
    chosen = sorted(named or index.get("*") or ())
    how = "named" if named else ("star" if chosen else "none")
    return tuple(n for gi in chosen for n in spec.structure["groups"][gi]["lines"]), how


def decide(spec: Spec) -> Decision:
    env = spec.env()
    lines, how = applying(spec)
    path = decode(raw_path(env["URL"]))
    hits = _trie_hits(_trie({n: env[f"P{n}"] for n in lines}), path)
    matched = tuple(n for n in lines if n in hits)
    if not matched:
        rules_allowed, rules_by, winners, tie = True, ("nogroup" if how == "none" else "nomatch"), (), False
    else:
        best = max(len(env[f"P{n}"]) for n in matched)
        top = [n for n in matched if len(env[f"P{n}"]) == best]
        effects = {env[f"E{n}"] for n in top}
        win = "allow" if "allow" in effects else "disallow"
        winners = tuple(n for n in top if env[f"E{n}"] == win)
        rules_allowed, rules_by, tie = win == "allow", "line", effects == {"allow", "disallow"}
    cls = status_class(env.get("STATUS"))
    if cls == "4xx":
        allowed, by = True, "status_4xx"
    elif cls == "5xx":
        allowed, by = False, "status_5xx"
    else:
        allowed, by = rules_allowed, rules_by
    return Decision(allowed, by, rules_allowed, rules_by, winners, tie, matched, lines, how)


def line_key(env: dict, n: int) -> str:
    return f"{env[f'E{n}']}:{env[f'P{n}']}"


def key_text(key: str) -> str:
    eff, pat = key.split(":", 1)
    return f"{EFFECTS[eff][0]}: {pat}"


def key_allowed(key: str) -> bool:
    return key == NONE_KEY or key.startswith("allow:")


def answer_for(qform: str, allowed: bool):
    """Yes/no answer from the outcome (twin predictions use it with the constructed outcome)."""
    if qform in (POS_FORM, DOUBLE_NEG_FORM):
        return int(allowed)
    if qform in NEG_FORMS:
        return int(not allowed)
    raise ContractError(f"{qform} is not a yes/no form")


# ------------------------------------------------------------------------------------------------ error-model matcher

def vmatch(pat: str, path: str, *, dollar=True, star_slash=True, whole=False, icase=False) -> bool:
    """A plain recursive matcher with one switch per named mistake (error models, tags, generation checks). The
    gold never uses it: solver A's gold is the trie; tests check vmatch() with default switches equals the trie."""
    anchored = False
    if pat.endswith("$"):
        pat = pat[:-1]
        anchored = dollar
    if icase:
        pat, path = pat.lower(), path.lower()
    n, m_ = len(path), len(pat)

    @lru_cache(maxsize=None)
    def m(i: int, j: int) -> bool:
        if i == m_:
            return j == n if (anchored or whole) else True
        if pat[i] == "*":
            if m(i + 1, j):
                return True
            return j < n and (star_slash or path[j] != "/") and m(i, j + 1)
        return j < n and path[j] == pat[i] and m(i + 1, j + 1)

    return m(0, 0)


def _named_groups(spec: Spec) -> list:
    env = spec.env()
    me = env["UA"].lower()
    return [g for g in spec.structure["groups"] if any(a != "*" and env[a].lower() == me for a in g["agents"])]


def _lookalike(a: str, me: str) -> bool:
    a, me = a.lower(), me.lower()
    return a != me and (a.startswith(me) or me.startswith(a))


def variant_lines(spec: Spec, groups: str):
    """The lines a reader uses under one group-selection mistake (None: the mistake does not apply)."""
    env = spec.env()
    allg = spec.structure["groups"]
    named = _named_groups(spec)
    star = [g for g in allg if "*" in g["agents"]]
    if groups == "rule":
        return list(applying(spec)[0])
    if groups == "star_over_named":
        return [n for g in star for n in g["lines"]] if named and star else None
    if groups == "merge_star":
        return sorted(n for g in named + star for n in g["lines"]) if named and star else None
    if groups == "first_group_only":
        return list(named[0]["lines"]) if len(named) >= 2 else None
    if groups == "lookalike":
        look = [g for g in allg if any(a != "*" and _lookalike(env[a], env["UA"]) for a in g["agents"])]
        return [n for g in look for n in g["lines"]] if look and not named else None
    raise ValueError(groups)


def variant_key(spec: Spec, *, groups="rule", path="decoded", pick="longest", **mkw):
    """The deciding line key (or NONE_KEY) a reader making one named mistake would give; None if it does not apply."""
    env = spec.env()
    lines = variant_lines(spec, groups)
    if lines is None:
        return None
    raw = raw_path(env["URL"])
    subject = {"decoded": decode(raw), "raw": raw, "no_query": decode(raw).split("?", 1)[0]}[path]
    m = [n for n in lines if vmatch(env[f"P{n}"], subject, **mkw)]
    if not m:
        return NONE_KEY
    if pick == "first":
        return line_key(env, m[0])
    if pick == "last":
        return line_key(env, m[-1])
    if pick in ("effect_order", "allow_wins"):
        pool = [n for n in m if env[f"E{n}"] == ("disallow" if pick == "effect_order" else "allow")] or m
        best = max(len(env[f"P{n}"]) for n in pool)
        return line_key(env, next(n for n in pool if len(env[f"P{n}"]) == best))
    size = (lambda n: sum(1 for c in env[f"P{n}"] if c not in "*$")) if pick == "literal_len" else \
        (lambda n: len(env[f"P{n}"]))
    best = max(size(n) for n in m)
    top = [n for n in m if size(n) == best]
    prefer = "disallow" if pick == "tie_disallow" else "allow"
    pool = [n for n in top if env[f"E{n}"] == prefer] or top
    return line_key(env, pool[0])


# ------------------------------------------------------------------------------------------------ generation helpers

def _host(site: str) -> str:
    """M3 <site-slug>: the site name's first word, lowercased (G0 section 6; a pack's sites differ in it, so a rename
    moves the host). Short hosts and PATH_BUDGET keep rows from Haiku packs inside the H28 length budget."""
    return site.split()[0].lower() + ".example"


def ok_pattern(p: str) -> bool:
    if not p.startswith("/") or "**" in p or "*$" in p or "$" in p[:-1] or any(c in p for c in " \t{}`"):
        return False
    for i, c in enumerate(p):
        if c == "%" and not (i + 2 < len(p) and p[i + 1] in HEX and p[i + 2] in HEX):
            return False
    return True


def _cuts(dp: str) -> list:
    return sorted({i + 1 for i, c in enumerate(dp) if c == "/"} | {len(dp)})


def _matching(rng: random.Random, dp: str) -> list:
    """Patterns that match the decoded path dp (checked with vmatch)."""
    c = [dp[:k] for k in _cuts(dp)]
    if len(dp) >= 3:
        c.append(dp[:rng.randint(2, len(dp))])
    c.append(dp + "$")
    if len(dp) >= 4:
        i = rng.randint(1, len(dp) - 2)
        j = rng.randint(i + 1, len(dp) - 1)
        c.append(dp[:i] + "*" + dp[j:rng.randint(j + 1, len(dp))])
    base, _, query = dp.partition("?")
    dot = base.rfind(".")
    if dot > base.rfind("/") and not query:
        c.append("/*" + base[dot:] + "$")
    if query:
        c.append("/*?" + query.split("=", 1)[0] + "=")
    c.append("/")
    out = []
    for p in c:
        if p not in out and ok_pattern(p) and vmatch(p, dp):
            out.append(p)
    return out


def _same_len_alt(rng: random.Random, pat: str, dp: str):
    """A different pattern of the same length that still matches dp: one literal character becomes "*"."""
    anchored = pat.endswith("$")
    body = pat[:-1] if anchored else pat
    idx = [i for i in range(1, len(body)) if body[i] not in "*%" and body[i - 1] != "*"
           and (i + 1 >= len(body) or body[i + 1] != "*") and not (anchored and i == len(body) - 1)]
    rng.shuffle(idx)
    for i in idx:
        alt = pat[:i] + "*" + pat[i + 1:]
        if ok_pattern(alt) and vmatch(alt, dp) and len(alt) == len(pat):
            return alt
    return None


def near_miss_typed(rng: random.Random, dp: str, pack: Pack) -> dict:
    """Patterns that look close to dp but do not match it, by kind: typo, case (one letter's case flipped), anchor
    ("$" too early), extend (one wrong extra character), query_anchor (the path without its query, then "$"),
    sibling (another directory), ext (another file extension). Each is checked with vmatch."""
    c: dict = {k: [] for k in ("typo", "case", "anchor", "extend", "query_anchor", "sibling", "ext")}
    ks = _cuts(dp) + ([rng.randint(3, len(dp))] if len(dp) >= 3 else [])
    for k in ks:
        pre = dp[:k]
        letters = [i for i in range(1, k) if pre[i].isalpha()]
        if letters:
            i = rng.choice(letters)
            ch = pre[i]
            new = rng.choice([x for x in "aeiourstln" if x != ch.lower()])
            c["typo"].append(pre[:i] + new + pre[i + 1:])
            c["case"].append(pre[:i] + ch.swapcase() + pre[i + 1:])
        if k < len(dp):
            c["anchor"].append(pre + "$")
            c["extend"].append(pre + rng.choice([x for x in string.ascii_lowercase if x != dp[k].lower()]))
    base, _, query = dp.partition("?")
    if query:
        c["query_anchor"].append(base + "$")
    others = [s for s in pack.segs if not dp.startswith("/" + s)]
    if others:
        c["sibling"].append("/" + rng.choice(others) + "/")
    c["ext"].append("/*" + rng.choice([e for e in PAGE_ENDINGS if not base.endswith(e)]) + "$")
    out = {}
    for kind, pats in c.items():
        keep = []
        for p in pats:
            if p not in keep and ok_pattern(p) and not vmatch(p, dp):
                keep.append(p)
        out[kind] = keep
    return out


def _near_miss(rng: random.Random, dp: str, pack: Pack, exclude=()) -> list:
    out = []
    for kind, pats in near_miss_typed(rng, dp, pack).items():
        if kind not in exclude:
            out += [p for p in pats if p not in out]
    return out


BAIT_KINDS = ("case", "anchor", "query_anchor")      # near misses that error models read as matches
NEAR_EXCLUDE = BAIT_KINDS + ("ext",)    # ch_line: the non-option near lines are not the baits, and have no "/*.ext$" form (its
                                       # extension token marked a file with many near lines, i.e. a "no line" row)
BAIT_WEIGHT = {"case": 0.5, "anchor": 0.3, "query_anchor": 0.2}   # both "$" kinds end in "$": deciders do so 40%
N_NEAR_CHOICE = (0, 1, 1, 2, 2)                                  # ch_line line rows: near-miss lines in the applying group
N_NEAR_NONE = (2, 3, 3, 4, 4)                                    # ch_line "no line" rows: more near lines, since line rows hold the decider
                                                                 # and its supporters: both kinds of file have as many lines (G6 meta view)
P_TIE_CHOICE = 0.60                                              # ch_line: Allow-decided rows that get an equal-length Disallow partner (tie trap 30%: G0 section 3)
P_DOLLAR_BAIT = 0.20                                             # a ch_line row gets one "$" bait (early anchor / query anchor)
P_DECIDER_DOLLAR = 0.40                                          # a ch_line decider is an "$"-ended pattern (when one exists)
P_NONE_DOLLAR_OTHER = 0.25                                       # A45 d: "$" share of the matching line a no-line row's conflict group shows
P_NONE_DOLLAR_BASE = 0.15                                        # A45 d: same for the base of its case bait
P_DOLLAR_BAIT_NONE = 0.05                                        # A45 d: a "no line" row's "$" bait (its shown lines carry the gold-line profile)
BAIT_WEIGHT_NONE = {"case": 0.8, "anchor": 0.15, "query_anchor": 0.05}
CH_LINES = (6, 7, 8)                                       # ch_line: planned rule-line count of the file (A44 d), any gold
CH_GROUPS = (2, 3)                                   # ch_line: planned group count of the file (A44 d), any gold
P_CHOICE_CONFLICT = 0.40                                         # ch_line: the non-applying group gives the opposite outcome


def _case_flip(rng: random.Random, pat: str, dp: str):
    """pat with one letter's case swapped (outside a %XX code), or None when no flip leaves a pattern that misses dp
    but matches it ignoring case. A capital goes to lowercase when the pattern has one, else a letter goes to
    capital: so the flipped line shows a capital about as often as a decider does."""
    letters = [i for i, c in enumerate(pat) if c.isalpha() and "%" not in pat[max(0, i - 2):i]]
    caps = [i for i in letters if pat[i].isupper()]
    pool = caps or letters
    rng.shuffle(pool)
    for i in pool:
        v = pat[:i] + pat[i].swapcase() + pat[i + 1:]
        if ok_pattern(v) and not vmatch(v, dp) and vmatch(v, dp, icase=True):
            return v
    return None


def decider_like(rng: random.Random, dp: str, m=None, pd: float = P_DECIDER_DOLLAR) -> str:
    """A pattern matching dp drawn exactly like a ch_line decider (profile first: "$"-ended with P_DECIDER_DOLLAR when one
    exists), so any line a "no line" file shows as a look-alike has the gold line's surface profile (A45 d, T35 pass 3)."""
    cands = m if m is not None else _matching(rng, dp)
    longish = [p for p in cands if len(p) >= 4] or cands
    dollar = [p for p in longish if p.endswith("$")]
    if dollar and rng.random() < pd:
        return rng.choice(dollar)
    return rng.choice([p for p in longish if not p.endswith("$")] or longish)


def bait_lines(rng: random.Random, dp: str, n: int, none: bool = False) -> list:
    """Up to n (effect, pattern) baits for a ch_line row, one per kind (an error model returns one line, so two of a kind
    waste an option): a flipped-case line, an early-"$" line (a matching pattern + "$" that stops before the path
    ends) and, with a query, the path without its query + "$". Each is made from a MATCHING pattern drawn like the
    deciders (stars, "$" and queries at the deciders' own rates), not cut from the path as a bare prefix: G6 / G7's
    options-only view read the bare-prefix baits as wrong (no "*", often "$"; pilot residual after F3)."""
    m = [p for p in _matching(rng, dp) if len(p) >= MIN_PATTERN]
    made = {}
    if none and m:          # A45 d: the bases are drawn as the deciders are (profile first), not uniformly from the matching patterns
        m = [decider_like(rng, dp, m, P_NONE_DOLLAR_BASE) for _ in range(8)]
        m = list(dict.fromkeys(m))
    for t in rng.sample(m, len(m)):
        v = _case_flip(rng, t, dp)
        if v:
            made["case"] = v
            break
    for t in rng.sample(m, len(m)):
        if not t.endswith(("$", "*")) and ok_pattern(t + "$") and not vmatch(t + "$", dp):
            made["anchor"] = t + "$"
            break
    if "?" in dp:
        b = dp.partition("?")[0] + "$"
        if ok_pattern(b) and not vmatch(b, dp):
            made["query_anchor"] = b
    dollar = [k for k in ("anchor", "query_anchor") if k in made]
    if dollar:                                  # at most one "$" bait, and only on some rows: deciders end in "$" about 30%
        keep = rng.choice(dollar) if rng.random() < (P_DOLLAR_BAIT_NONE if none else P_DOLLAR_BAIT) else None
        for k in dollar:
            if k != keep:
                del made[k]
    kinds = []                                  # a weighted draw without replacement
    pool = {k: (BAIT_WEIGHT_NONE if none else BAIT_WEIGHT)[k] for k in made}
    while pool and len(kinds) < n:
        v, acc = rng.random() * sum(pool.values()), 0.0
        for k, w in pool.items():
            acc += w
            if v < acc:
                kinds.append(k)
                del pool[k]
                break
    return [(rng.choice(EFFECT_KEYS), made[k]) for k in kinds]


def _unrelated(rng: random.Random, dp: str, pack: Pack) -> str:
    others = [s for s in pack.segs if not dp.startswith("/" + s)] or ["unused"]
    s = rng.choice(others)
    p = rng.choice(("/" + s + "/", "/" + s, "/" + s + "/*" + rng.choice(PAGE_ENDINGS), "/*/" + s + "/"))
    return p if not vmatch(p, dp) else "/" + s + "-old/"


def _gen_path(rng: random.Random, pack: Pack, query: bool = True) -> str:
    """1-3 segments + an optional file name + an optional query; trailing segments are dropped while segments + file
    pass PATH_BUDGET characters (G0 section 6, H28: slugged Haiku names are about twice as long as program ones)."""
    segs = rng.sample(pack.segs, rng.choice((1, 2, 2, 3)))
    r = rng.random()
    file = rng.choice(pack.files) if r < 0.45 else None
    while len(segs) > 1 and len("/".join(segs)) + (len(file) + 1 if file else 0) > PATH_BUDGET:
        segs.pop()                      # G0 section 6: slugged Haiku names are long; one segment always stays
    if rng.random() < P_CAPS:                           # one segment or the file name capitalised (label-blind)
        i = rng.randrange(len(segs) + (file is not None))
        if i < len(segs):
            segs[i] = segs[i][:1].upper() + segs[i][1:]
        else:
            file = file[:1].upper() + file[1:]
    p = "/" + "/".join(segs)
    if file is not None:
        p += "/" + file
    elif r < 0.75:
        p += "/"
    if rng.random() < 0.30 and query:
        p += "?" + rng.choice(QUERY_KEYS) + "=" + rng.choice(QUERY_VALUES)
    return p


def percent_encode(raw: str, positions) -> str:
    return "".join(f"%{ord(ch):02X}" if i in positions else ch for i, ch in enumerate(raw))


def encodable(raw: str) -> list:
    """Positions of unreserved characters outside existing %XX codes (and after the leading "/")."""
    inside = set()
    for i in range(len(raw) - 2):
        if raw[i] == "%" and raw[i + 1] in HEX and raw[i + 2] in HEX:
            inside |= {i, i + 1, i + 2}
    return [i for i in range(1, len(raw)) if raw[i] in UNRESERVED and i not in inside]


MIN_PATTERN = 4                 # a wrong line's pattern is at least this long (root lines are never shown as wrong options)
_EXT = tuple(PAGE_ENDINGS)


def line_profile(key: str) -> tuple:
    """The surface profile of a line key: its pattern has "*", ends with "$", has "?", has a capital letter, ends with a
    file ending, ends with "/", has a digit; and its effect is Allow (what a reader can see in the option text without
    the file)."""
    pat = key.split(":", 1)[1]
    return ("*" in pat, pat.endswith("$"), "?" in pat, any(c.isupper() for c in pat), pat.rstrip("$").endswith(_EXT),
            pat.rstrip("$").endswith("/"), any(c.isdigit() for c in pat), key.startswith("allow:"))


_WORD = re.compile(r"[a-z0-9]+(?:['-][a-z0-9]+)*")


def line_distance(a: str, b: str) -> int:
    """How far two line keys look apart: 10 per differing pattern flag, 40 for a different effect (the wrong lines were
    58% Disallow against a 50% Allow gold: ties and "opposite" lines), 3 per word (alphanumeric run) of difference,
    plus the visible length difference."""
    pa, pb = line_profile(a), line_profile(b)
    wa, wb = len(_WORD.findall(key_text(a).lower())), len(_WORD.findall(key_text(b).lower()))
    return (10 * sum(x != y for x, y in zip(pa[:-1], pb[:-1])) + 40 * (pa[-1] != pb[-1]) + 3 * abs(wa - wb)
            + abs(len(key_text(a)) - len(key_text(b))))


def strat(sampler: str, name: str, idx: int, n: int) -> int:
    """A value of range(n) for the idx-th item of a stream, each value exactly once in every block of n consecutive
    indices (a seeded permutation per block). Label-blind: it reads the sampler, the stream name and the index only.
    Stratifying (rather than drawing each item alone) keeps the realised shares of a ~1,000-row pilot on their plan:
    an independent draw of the choice rows' abstain gold moves G10's gold-is-longest by +/- 2.6 pp (1 SD at ~300
    rows) against a +/- 2 pp bar."""
    blk, pos = divmod(idx, n)
    order = sorted(range(n), key=lambda v: uhash(FAMILY, "strat", name, sampler, blk, v))
    return order[pos]


def slot_of(sampler: str, seed: int) -> tuple:
    """(kind, index): whether this seed's base is a choice or a yes/no base, and its index among that kind in the
    sampler's seed order. Each block of W_SLOTS seeds holds exactly N_CHOICE_SLOTS choice bases, at seeded places."""
    blk, pos = divmod(seed, W_SLOTS)
    order = sorted(range(W_SLOTS), key=lambda i: uhash(FAMILY, "slot", sampler, blk, i))
    choice = frozenset(order[:N_CHOICE_SLOTS])
    mine = pos in choice
    before = sum(1 for i in range(pos) if (i in choice) == mine)
    per = N_CHOICE_SLOTS if mine else W_SLOTS - N_CHOICE_SLOTS
    return ("choice" if mine else "yesno"), blk * per + before


def choice_plan(sampler: str, seed: int) -> ChoicePlan:
    """The display plan of a ch_line row (c2_kit.choiceplan.ChoicePlan; F3 of the pilot verdict), fixed by the seed's
    place in its sampler's stream before any structure is drawn: the option count k (3 or 4, "no line matches"
    included, always shown), whether the gold IS "no line matches" (exactly 1/k in every block of k rows of that k), the
    gold's position (uniform per k) and its visible-length rank among the line options (uniform). The sampler then
    draws structure until solver A's gold agrees (label-first); nothing is ever relabelled."""
    kind, c = slot_of(sampler, seed)
    if kind != "choice":
        raise ContractError(f"T35 {sampler} seed {seed} is a yes/no base, not a choice row")
    k = (3, 4)[strat(sampler, "ch_k", c, 2)]
    j = c // 2                                     # index among the rows of this k (every pair holds one of each)
    gold_abstain = strat(sampler, f"ch_ab{k}", j, k) == 0
    pos = strat(sampler, f"ch_pos{k}", j, k)
    rank = None if gold_abstain else strat(sampler, f"ch_rank{k}", j, k - 1)
    return ChoicePlan(f"{FAMILY}|{seed}|{sampler}|{CHOICE_FORM}", k, True, gold_abstain, pos, rank, 1.0 / k)


def _case_variant(rng: random.Random, tok: str) -> str:
    v = rng.choice((tok.lower(), tok.upper(), tok[:1].lower() + tok[1:]))
    return v if v != tok else tok.swapcase()


# ------------------------------------------------------------------------------------------------ the plugin

class T35Plugin(C2Plugin):
    FAMILY = FAMILY
    TIER = "agent"
    G0_LITE = HERE / "G0_SPEC.md"
    G0_SHA256 = "c5078d6d65b98a08d79ccba3a0ad0660345bfec0b0088fb392c4e7a1324a8c35"   # G0_SPEC.md v6 (v5: edf1f2d0...; v4: ccc537cc...; v3: f3be54bc...)
    G0_AMBIGUITY_PASS = {   # the one blind Haiku ambiguity pass (G0_SPEC.md section 7), resolved as H1-H33
        "task_id": "c2-data-stage-a/amb:T35", "n_points": 33,
        "points_sha256": "3cdbfe0449b432d42169e5a8c82083878bf193b39e869ba5f767762b8311f252",
        "points_file": "haiku/ambiguity/amb_T35_points.json",
        "g0_v1_sha256": "204f3be105e9e15a505ee8a35ce8439df43450946d54a90a82b44b08e5bdb228"}
    SAMPLERS = ("S1", "S2", "S3", "S4", "S5")
    HELD_OUT_SAMPLERS = ("S5",)
    PARADIGM_A = "trie_longest_match"
    PARADIGM_B = "regex_compile"
    SOLVER_B_MODULE = "families.T35.solver_b"
    QFORMS = {q.qform: q for q in (
        QuestionForm(POS_FORM, "noul", "may_fetch", 1, yes_is_bad=False),
        QuestionForm(DOUBLE_NEG_FORM, "noul", "may_fetch", 1, yes_is_bad=False),
        QuestionForm("yn_skip", "noul", "may_fetch", -1, "antonym", yes_is_bad=True),
        QuestionForm("yn_not_allowed", "noul", "may_fetch", -1, "syntactic", yes_is_bad=True),
        QuestionForm("yn_prevented", "noul", "may_fetch", -1, "implicit", yes_is_bad=True),
        QuestionForm(CHOICE_FORM, "choice", answer_set="open", abstain=True),
    )}
    LABEL_WORDS = ("allow", "allowed", "disallow", "disallowed", "permitted", "forbidden", "blocked", "barred",
                   "skip", "off-limits", "may fetch")
    CLOSED_WORLD_SENTENCE = CLOSED_WORLD
    REGISTERS = ("memo", "chat", "email", "ticket", "faq", "log", "json", "pr_review", "transcript", "wiki")
    HELD_OUT_REGISTERS = ("transcript", "wiki")
    GSL_EXCEPTIONS: dict = {}
    NAME_ALLOW = ("URL", "Allow", "Disallow", "User")
    POLARITY_CHECK = True                 # c2_kit.polarity: yes/no wordings must read with their form's polarity
    POLARITY_NEGATIVES = NEGATIVE_PREDICATES

    def __init__(self, lexicon=None, packs=None, operators=None):
        """packs / operators None: the frozen pools (load_pools(): 8 program + 40 Haiku site packs, 8 of them held out
        for S5; 8 program + 48 Haiku operators). Passing PACKS / OPERATORS gives the program-only stand-ins (tests;
        S5 then has no pack). Every pack and operator is checked (pool_problems) before any row is drawn."""
        super().__init__(lexicon)
        if packs is None or operators is None:
            pool_packs, pool_ops = load_pools()
            packs = pool_packs if packs is None else packs
            operators = pool_ops if operators is None else operators
        self.packs, self.operators = tuple(packs), tuple(operators)
        probs = pool_problems(self.packs, self.operators)
        if probs:
            raise ContractError("T35 packs / operators: " + "; ".join(probs[:5]))
        self.pack_by_id = {p.pack_id: p for p in self.packs}
        self.card_packs = card_packs(self.packs)
        self.double_neg_ok = self._clean_forms(DOUBLE_NEG_FORM)
        self._screened: list = []                  # [(ctx, screened ctx, {wording id: problems})]

    def _clean_forms(self, qform: str) -> dict:
        """{held_out: True when the lexicon holds an admitted question form of `qform` with that held-out flag (or, for
        True, any flag: S5 falls back to training wordings) whose wording passes the polarity rule}. Label-blind: the
        pool, not a row. Without a lexicon (contract checks) both are True."""
        if self.lexicon is None:
            return {False: True, True: True}
        sem = question_sem(FAMILY, qform)
        ok = [f for f in self.lexicon.forms.values() if f.sem_id == sem and self.lexicon.status(f.form_id) == "admitted"
              and not POL.form_problems(self, qform, f.text)]
        return {False: any(not f.held_out for f in ok), True: bool(ok)}

    def ctx_for(self, spec: Spec, ctx):
        """The kit context without the wordings that break the polarity rule (c2_kit.polarity; G5-H fix F1), so neither
        render() nor the pipeline's complement partner can pick one. Cached per context object."""
        for c, screened, _bad in self._screened:
            if c is ctx:
                return screened
        screened, bad = POL.screen(ctx, self)
        self._screened.append((ctx, screened, bad))
        return screened

    def quarantined_wordings(self, ctx) -> dict:
        """{wording skin id: polarity problems} for the wordings ctx_for() leaves out of `ctx`."""
        self.ctx_for(None, ctx)
        return next(bad for c, _s, bad in self._screened if c is ctx)

    def card_pack(self, seed: int, sampler: str) -> Pack:
        """The pack (so the card) of a row: from the sampler's packs by a hash of the seed alone, drawn before the
        plan's outcome is tried, so no retry can steer the pack toward a label."""
        pool = self.card_packs.get(sampler, ())
        if not pool:
            raise ContractError(f"T35 {sampler}: no pack (S5 needs the held-out packs of load_pools())")
        return pool[int(uhash(FAMILY, "pack", sampler, seed) * len(pool))]

    # ------------------------------------------------------------------------------------------- sampling
    def _clause(self, sem: str, rng: random.Random) -> S.Slot:
        if self.lexicon is None:
            raise ContractError("T35 needs its lexicon registry (T35Plugin(lexicon=...))")
        ids = sorted(f for f, x in self.lexicon.forms.items() if x.sem_id == sem and x.kind == "precedence"
                     and self.lexicon.status(f) == "admitted")
        if not ids:
            raise ContractError(f"no admitted precedence form for {sem}")
        return self.lexicon.clause(rng.choice(ids), bind={})

    @staticmethod
    def _cell(sampler: str, y: int) -> tuple:
        """Label-first balance: in every block of 4 consecutive yes/no bases (y = their index in the sampler's stream)
        each (outcome, polarity) cell appears once."""
        c = strat(sampler, "cell", y, 4)
        return bool(c & 1), bool(c >> 1)

    def _plan(self, seed: int, sampler: str) -> tuple:
        """(qform, outcome target, status key or None, rules kind, rules effect) drawn before any text. The base is a
        choice or a yes/no base by its place in the sampler's stratified stream (slot_of); a choice row's target
        (no line / Allow line / Disallow line) comes from its ChoicePlan (F3: no line = 1/k)."""
        u = lambda *k: uhash(FAMILY, sampler, seed, *k)       # noqa: E731
        cfg = CFG[sampler]
        rng = random.Random(f"{FAMILY}|plan|{sampler}|{seed}")
        kind0, idx = slot_of(sampler, seed)
        if kind0 == "choice":
            plan = choice_plan(sampler, seed)
            if plan.gold_abstain:
                target = "none"
            else:
                target = ("allow", "disallow")[strat(sampler, f"ch_eff{plan.k}", idx // 2, 2)]
            status = "200" if u("status_show") < cfg.p_status * 0.6 else None
            kind, eff = ("nomatch", "allow") if target == "none" else ("line", target)
            return CHOICE_FORM, target, status, kind, eff
        allowed, negative = self._cell(sampler, idx)
        # A44 d: a status trap is a whole block of 4 yes/no bases. The block's (outcome, polarity) cells are the gold drawn
        # first (each once: gold yes and gold no on both polarities); the status class is then derived from the outcome (4xx =
        # may fetch, 5xx = may not), so each status class meets both polarities and both golds, and the code alone predicts
        # nothing. Positive frames only (A43 f): the pair is yn_fetch ("may it fetch?") and yn_skip ("must it skip?").
        trap = uhash(FAMILY, "trap", sampler, idx // 4) < cfg.p_status * cfg.p_ns
        if negative and trap:
            qform = "yn_skip"
        elif trap:
            qform = POS_FORM
        elif negative:
            # one negative form per block of 4 yes/no bases (both negative bases of the block share it; each of the three
            # forms comes once in every 3 blocks): the block's two negative bases hold both outcomes, so every negative
            # form is exactly 50% yes. Drawn per row, the forms' yes rates wandered +/- 5 pp and G6's metadata and question
            # views read the qform (accuracy 54% with the qform alone, first pilot_i1 run)
            qform = NEG_FORMS[strat(sampler, "negform", idx // 4, len(NEG_FORMS))]
        else:
            block_dn = uhash(FAMILY, "double_neg", sampler, idx // 4) < P_DOUBLE_NEG   # both outcomes of a block
            # no admitted double-negation wording passes the polarity rule (the 20 frozen ones all fail it): the block
            # asks the positive form, so no unit is drawn that render() could not word (label-blind: pool state only)
            dn_ok = self.double_neg_ok[sampler in self.HELD_OUT_SAMPLERS]
            qform = DOUBLE_NEG_FORM if block_dn and dn_ok else POS_FORM
        status = None
        if trap:                                           # F2 cap kept: 4xx / 5xx on p_status * p_ns of the bases
            pool = STATUS_4XX if allowed else STATUS_5XX
            status = pool[int(u("status_code") * len(pool))]
        elif u("status_show") < cfg.p_status * (1 - cfg.p_ns) / (1 - cfg.p_status * cfg.p_ns):
            status = "200"                                 # a status line still shows on p_status of the bases in all
        if status not in (None, "200"):
            r = rng.random()                                   # the lines' own outcome, independent of the status
            kind, eff = ("nomatch", "allow") if r < 0.2 else ("line", "allow" if r < 0.55 else "disallow")
        elif allowed:
            kind, eff = ("nomatch", "allow") if u("nomatch") < P_NONMATCH_ALLOW else ("line", "allow")
        else:
            kind, eff = "line", "disallow"
        return qform, ("allow" if allowed else "disallow"), status, kind, eff

    def sample(self, seed: int, sampler: str) -> Spec:
        if sampler not in self.SAMPLERS:
            raise ContractError(f"sampler {sampler}")
        qform, target, status, kind, eff = self._plan(seed, sampler)
        pack = self.card_pack(seed, sampler)
        rng = random.Random(f"{FAMILY}|{sampler}|{seed}")
        for i in range(MAX_TRIES):
            spec = self._draw(rng, seed, sampler, pack, qform, status, kind, eff, relax=i >= RELAX_AFTER)
            if spec is not None:
                self._assert_target(spec, qform, target, status)
                return spec
        raise ContractError(f"T35 {sampler} seed {seed}: no spec reached its planned outcome")

    @staticmethod
    def _assert_target(spec: Spec, qform: str, target: str, status) -> None:
        """A45 b: the realised spec decides exactly what the plan said, whatever status row (4xx / 5xx / 200 / none) it is."""
        d = decide(spec)
        if qform == CHOICE_FORM:
            ok = d.by == ("nomatch" if target == "none" else "line") and (target == "none" or d.allowed == (target == "allow"))
        else:
            ok = d.allowed == (target == "allow")
        if not ok:
            raise ContractError(f"T35 {spec.sampler} seed {spec.seed}: decide() = {d.allowed}/{d.by} but the plan was {target} "
                                f"(status {status})")

    def _applying_lines(self, rng, dp, kind, eff, cfg, pack, baits: int = 0) -> list:
        """The applying group's lines for a planned outcome. Effects of the lines that do not decide are drawn
        so that the file's effect mix does not give the label away (G6): the losers that make the first-match and
        tie traps are paired with same-effect supporters, near misses take either effect, and identical-pattern
        Allow/Disallow pairs appear on both outcomes."""
        lines = []
        pair_p = P_PAIR[eff] if kind == "line" else P_PAIR["nomatch"]
        if kind == "line":
            cands = _matching(rng, dp)
            longish = [p for p in cands if len(p) >= 4] or cands
            dollar = [p for p in longish if p.endswith("$")]
            if baits and dollar and rng.random() < P_DECIDER_DOLLAR:     # ch_line: "$" deciders as often as "$" wrong lines
                d = rng.choice(dollar)
            elif baits:
                d = rng.choice([p for p in longish if not p.endswith("$")] or longish)
            else:
                d = rng.choice(longish)
            opp = "disallow" if eff == "allow" else "allow"
            lines.append((eff, d, "decider"))
            p_tie = P_TIE_CHOICE if baits else cfg.p_tie     # ch_line: the Disallow tie partner is the one effect-skewed wrong line
            if eff == "allow" and rng.random() < p_tie:
                alt = d if rng.random() < 0.15 else (_same_len_alt(rng, d, dp) or d)
                if baits and "*" not in d:      # ch_line: the tie partner shows a "*" only when the decider does
                    alt = d
                lines.append(("disallow", alt, "tie"))
            short = [p for p in cands if len(p) < len(d)]
            free = (lambda: rng.choice(EFFECT_KEYS)) if baits else None    # ch_line: a wrong line's effect is a coin flip
            if short and rng.random() < cfg.p_short_opp:
                lines.append((free() if baits else opp, rng.choice(short), "short"))
            if short and rng.random() < cfg.p_short_opp * P_SUPPORT:
                lines.append((free() if baits else eff, rng.choice(short), "support"))
            if short and rng.random() < pair_p:
                q = rng.choice(short)
                lines += [("allow", q, "pair"), ("disallow", q, "pair")]
            for _ in range(rng.choice(N_NEAR_CHOICE if baits else cfg.n_near)):
                nm = _near_miss(rng, dp, pack, NEAR_EXCLUDE if baits else ())
                longer = [p for p in nm if len(p) >= len(d)] or nm
                if longer:
                    lines.append((free() if baits else (opp if rng.random() < P_NEAR_OPP else eff), rng.choice(longer),
                                  "near"))
            if rng.random() < cfg.p_decoy_tie:
                eq = [p for p in _near_miss(rng, dp, pack, NEAR_EXCLUDE if baits else ()) if len(p) == len(d)]
                if eq:
                    lines.append((free() if baits else opp, rng.choice(eq), "decoy"))
            if rng.random() < P_UNRELATED:
                lines.append((free() if baits else (eff if rng.random() < P_UNREL_SAME else opp),
                              _unrelated(rng, dp, pack), "unrelated"))
        else:
            nm = _near_miss(rng, dp, pack, NEAR_EXCLUDE if baits else ()) or [_unrelated(rng, dp, pack)]
            for _ in range(rng.choice(N_NEAR_NONE if baits else (1, 2, 2, 3))):
                lines.append((rng.choice(EFFECT_KEYS), rng.choice(nm), "near"))
            if rng.random() < pair_p:
                q = rng.choice(nm)
                lines += [("allow", q, "pair"), ("disallow", q, "pair")]
            if baits and rng.random() < P_UNRELATED:        # ch_line: a "no line" file looks like a line file
                lines.append((rng.choice(EFFECT_KEYS), _unrelated(rng, dp, pack), "unrelated"))
        if baits:
            lines += [(e, p, "bait") for e, p in bait_lines(rng, dp, baits, none=kind != "line")]
        out, seen = [], set()
        for e, p, r in lines:
            if (e, p) not in seen:
                seen.add((e, p))
                out.append((e, p, r))
        losers = [x for x in out if x[2] in ("tie", "short")]
        rng.shuffle(out)
        if losers and rng.random() < cfg.p_first_wrong:
            first = rng.choice(losers)
            out.remove(first)
            out.insert(0, first)
        return [(e, p) for e, p, _ in out]

    def _other_lines(self, rng, dp, pack, outcome_allowed: bool, conflict: bool, gl: bool = False) -> list:
        """Lines of a group that does not apply. In that group alone the outcome is the opposite one (conflict) or
        the same one; an extra unrelated line never matches."""
        group_allowed = (not outcome_allowed) if conflict else outcome_allowed
        m = _matching(rng, dp)
        pick = (lambda: decider_like(rng, dp, m, P_NONE_DOLLAR_OTHER)) if gl else (lambda: rng.choice(m))      # gl: a "no line" ch_line row (A45 d)
        if gl:                  # a "no line" ch_line row: the matching line of the conflict group takes a coin-flip effect (shown lines: 50% Allow)
            out = [(rng.choice(EFFECT_KEYS), pick())]
        elif not group_allowed:
            out = [("disallow", pick())]
        elif rng.random() < 0.6:
            out = [("allow", pick())]
        else:
            out = [(rng.choice(EFFECT_KEYS), rng.choice(_near_miss(rng, dp, pack) or [_unrelated(rng, dp, pack)]))]
        if rng.random() < 0.35:
            out.append((rng.choice(EFFECT_KEYS), _unrelated(rng, dp, pack)))
        return out

    def _draw(self, rng, seed, sampler, pack, qform, status, kind, eff, relax=False):
        cfg = CFG[sampler]
        site = rng.choice(pack.sites)
        operator, token = rng.choice(self.operators)
        # ch_line rows carry no query string: a line that cuts into one ("?sessionid=a1b2") or a bait without it ("$") is
        # gold at another rate than a path line (options-only G6 reads the query keys: sessionid 46% against 29%); the
        # query rule stays on the yes/no rows
        dp = _gen_path(rng, pack, query=qform != CHOICE_FORM)
        percent = rng.random() < cfg.p_percent
        if percent and rng.random() < 0.25:
            q = dp.find("?")
            inner = [i for i, c in enumerate(dp) if c == "/" and 0 < i < (q if q >= 0 else len(dp)) - 1]
            if inner:
                i = rng.choice(inner)
                dp = dp[:i] + "%2F" + dp[i + 1:]
        raw = dp
        if percent:
            pos = encodable(dp)[:10]
            if pos:
                raw = percent_encode(dp, set(rng.sample(pos, min(len(pos), rng.choice((1, 1, 2))))))
        rules_allowed = kind == "nomatch" or eff == "allow"
        mode = rng.choices(MODES, weights=cfg.modes)[0]
        if mode == "nogroup" and kind != "nomatch":
            mode = "star"
        choice = qform == CHOICE_FORM
        baits = rng.choice((1, 2, 3)) if choice else 0
        gl = choice and kind == "nomatch"
        p_conflict = max(cfg.p_conflict, P_CHOICE_CONFLICT) if choice else cfg.p_conflict
        app = self._applying_lines(rng, dp, kind, eff, cfg, pack, baits)
        # the non-applying groups' outcome is a conflict with the file's own; a ch_line "no line" row (outcome: may fetch) would
        # always get Disallow lines there, which made the wrong lines 55% Disallow against a 50% Allow gold, so its
        # reference outcome is a coin flip
        oa = (rng.random() < 0.5) if (choice and kind == "nomatch") else rules_allowed
        groups, side = [], None                     # side: index of the non-applying conflict group of the base file
        if mode in ("named", "combined"):
            tv = [token if rng.random() < 0.7 else _case_variant(rng, token) for _ in range(2)]
            if mode == "combined" and len(app) >= 2:
                cut = rng.randint(1, len(app) - 1)
                groups += [([tv[0]], app[:cut]), ([tv[1]], app[cut:])]
            else:
                agents = [tv[0]]
                if rng.random() < 0.2:
                    agents.insert(rng.randint(0, 1), rng.choice(OTHER_AGENTS))
                groups.append((agents, app))
            if rng.random() < 0.85:
                side = len(groups)
                groups.append((["*"], self._other_lines(rng, dp, pack, oa, rng.random() < p_conflict, gl)))
        elif mode == "star":
            groups.append((["*"], app))
            if rng.random() < p_conflict:
                side = len(groups)
                groups.append(([token + rng.choice(LOOKALIKE_SUFFIXES)],
                               self._other_lines(rng, dp, pack, oa, True, gl)))
        else:
            look = token + rng.choice(LOOKALIKE_SUFFIXES)
            groups.append(([look], self._other_lines(rng, dp, pack, oa, rng.random() < p_conflict, gl)))
        n_pre = len(groups)
        for _ in range(rng.choice(cfg.n_other)):
            groups.append(([rng.choice(OTHER_AGENTS)], self._other_lines(rng, dp, pack, rules_allowed,
                                                                          rng.random() < 0.5)))
        if choice and relax:
            # A45 b: the planned group count (A44 d) is drawn from the seed alone. A file that holds more groups than the plan
            # (S4 draws 1-2 extra groups on top of the applying and the conflict group) used to be rejected, and a plan of 2
            # groups was almost never reachable (seeds 900027, 900031, 900101, 900107, 900112 failed after 1000 tries). The
            # surplus is dropped instead (only after RELAX_AFTER rejected tries, so seeds that reach the plan by redrawing keep their i3 files): the extra other-agent groups first, then the non-applying conflict group. The drop
            # looks at the plan and the group order only, never at the gold; the applying group is never dropped.
            plan_g = CH_GROUPS[int(uhash(FAMILY, "ch_ngroups", sampler, seed) * len(CH_GROUPS))]
            while len(groups) > plan_g and len(groups) > n_pre:
                groups.pop()
            if len(groups) > plan_g and side is not None:
                groups.pop(side)                                # the "*" / look-alike conflict group of the base file
        rng.shuffle(groups)
        if choice:        rng.shuffle(groups)
        if choice:
            # A44 d: the file's size (rule lines, groups) is planned from the seed alone, before the gold (target) matters, and the
            # drawn file is padded up to it with never-matching lines / other-agent groups (rejected when it is already bigger).
            # Without this the "no line matches" rows had more lines and more groups than line rows, and G6's metadata view
            # (n_lines, depth) told the abstain option's rows apart (d_meta gbt 0.334 against 0.311).
            groups = self._pad_to_plan(rng, dp, pack, groups,
                                       CH_LINES[int(uhash(FAMILY, "ch_nlines", sampler, seed) * len(CH_LINES))],
                                       CH_GROUPS[int(uhash(FAMILY, "ch_ngroups", sampler, seed) * len(CH_GROUPS))])
            if groups is None:
                return None
        if len(groups) > MAX_GROUPS or sum(len(ls) for _, ls in groups) > MAX_LINES:
            return None
        if any(not ls for _, ls in groups):
            return None
        slots, sgroups, ln, an = {}, [], 0, 0
        seen_lines, seen_agents = set(), set()
        for agents, lines in groups:
            ag = []
            for a in agents:
                if a == "*":
                    ag.append("*")
                    continue
                if a.lower() != token.lower() and a.lower() in seen_agents:
                    return None
                seen_agents.add(a.lower())
                an += 1
                slots[f"A{an}"] = S.id_slot(a)
                ag.append(f"A{an}")
            ls = []
            for e, p in lines:
                if (e, p) in seen_lines:
                    return None                                   # every line of the file is distinct
                seen_lines.add((e, p))
                ln += 1
                slots[f"E{ln}"] = S.category_slot(e, EFFECTS)
                slots[f"P{ln}"] = S.glob_slot(p)
                ls.append(ln)
            sgroups.append({"agents": ag, "lines": ls})
        card = CARDS.draw_style(f"{FAMILY}|{sampler}|{seed}", CARD_SHARES)
        slots.update({"UA": S.id_slot(token), "URL": S.url_slot(f"https://{_host(site)}{raw}"),
                      "SITE": S.name_slot(site), "OPERATOR": S.name_slot(operator),
                      "PURPOSE": S.category_slot(rng.choice(sorted(PURPOSES)), PURPOSES),
                      "LONGEST": self._clause(LONGEST_SEM, rng), "TIE": self._clause(TIE_SEM, rng)})
        if status is not None:
            slots["STATUS"] = S.category_slot(status, STATUS)
        structure = {"groups": sgroups, "container": rng.choice(cfg.containers), "card": card}
        # card = sampler + pack (G0 section 6); the card style (M17 / M18) is a row's display choice, not a card
        spec = self.derive(Spec(FAMILY, sampler, seed, f"{FAMILY}:{sampler}:{pack.pack_id}", qform, slots,
                                structure=structure, pack=pack.pack_id))
        d = decide(spec)
        if d.rules_allowed != rules_allowed or (kind == "line") != (d.rules_by == "line"):
            return None
        if qform == CHOICE_FORM and not self._choice_ok(spec, d):
            return None
        return spec

    @staticmethod
    def _pad_to_plan(rng, dp, pack, groups, plan_l: int, plan_g: int):
        """The groups padded to exactly plan_l rule lines in plan_g groups: new groups are other-agent groups of one unrelated
        line, the remaining lines are unrelated lines (never matching) in random groups; None when the file is already
        bigger than the plan or no unused other agent is left."""
        n_l, n_g = sum(len(ls) for _, ls in groups), len(groups)
        if n_g > plan_g or n_l > plan_l or plan_l - n_l < plan_g - n_g:
            return None
        used = {a.lower() for ags, _ in groups for a in ags}
        free = [a for a in OTHER_AGENTS if a.lower() not in used]
        rng.shuffle(free)
        out = [(list(a), list(ls)) for a, ls in groups]
        for _ in range(plan_g - n_g):
            if not free:
                return None
            out.append(([free.pop()], [(rng.choice(EFFECT_KEYS), _unrelated(rng, dp, pack))]))
        for _ in range(plan_l - n_l - (plan_g - n_g)):
            out[rng.randrange(len(out))][1].append((rng.choice(EFFECT_KEYS), _unrelated(rng, dp, pack)))
        rng.shuffle(out)
        return out

    def _choice_ok(self, spec: Spec, d: Decision) -> bool:
        """ch_line rows: a 2xx status, one deciding line (or none), option texts distinct beyond letter case, and
        enough error-model lines for the option count drawn from the row key."""
        if d.by not in ("line", "nomatch", "nogroup") or (d.by == "line" and len(d.winners) != 1):
            return False
        env = spec.env()
        texts = [key_text(line_key(env, n)).casefold() for g in spec.structure["groups"] for n in g["lines"]]
        if len(set(texts)) != len(texts):
            return False                                   # option texts must differ beyond letter case
        return self._enough_distractors(spec)

    def _enough_distractors(self, spec: Spec) -> bool:
        return self._line_options(spec, self.solve_a(spec)) is not None

    def _line_options(self, spec: Spec, ans):
        """The k options of a ch_line row from its ChoicePlan (k, gold position and length rank fixed before the
        structure; "no line matches" always shown; options ordered by visible length). strict_plan: the sampler only
        keeps structures whose gold agrees with the plan, so a PlanMismatch here is a sampler bug, never relabelled.
        The wrong lines are look-alikes of the reference line (matched_models)."""
        return build_options(spec, ans, self.matched_models(spec, ans), row_key=self.row_key(spec),
                             render_key=key_text, abstain=(NONE_KEY, NONE_TEXT),
                             plan=choice_plan(spec.sampler, spec.seed), length_balance=True, strict_plan=True)

    def matched_models(self, spec: Spec, ans) -> dict:
        """The error models restricted to LOOK-ALIKE outputs (G6 / G7 choice, F3 residual). The wrong lines a row shows
        are the candidates nearest to its reference line in surface profile (a "*", a final "$", a "?", a capital, a
        file ending, a final "/") and then in visible length, on each side of the gold as its planned rank asks. The
        reference is the gold line; on a "no line matches" row (no gold line) it is the candidate first in a hash order
        of the row key. Without this the wrong lines told themselves from the deciders by surface alone (a bait is
        longer, star-free and often anchored; a supporter is a short root line: "/" was gold on 1 of 98 showings, a
        line with "*" was gold 35% of its showings against 21% for a wrong one), which lifts every options-only view
        far above chance. Label-blind: the reference is the gold only on a line row; no display choice reads the label."""
        models = self.error_models()
        plan = choice_plan(spec.sampler, spec.seed)
        if (ans == NONE_KEY) != plan.gold_abstain:      # a gold that disagrees with the plan (a broken solver A): build_options
            return models                               # raises PlanMismatch under strict_plan, a render error the gate counts
        outs = {name: m.fn(spec) for name, m in models.items()}
        key = self.row_key(spec)
        cands = {a for a in outs.values() if a not in (None, NONE_KEY, ans) and len(a.split(":", 1)[1]) >= MIN_PATTERN}
        h = lambda a: uhash(FAMILY, "sel", key, a)                                       # noqa: E731
        if ans == NONE_KEY:
            keep: set = set()
            if cands:
                ref = min(cands, key=lambda a: uhash(FAMILY, "ref", key, a))
                keep = set(sorted(cands, key=lambda a: (line_distance(a, ref), h(a)))[:plan.k - 1])
        else:
            gt = key_text(ans)
            order = lambda a: (len(key_text(a)), key_text(a))                           # noqa: E731
            cands = {a for a in cands if key_text(a).casefold() != gt.casefold()}
            n = plan.k - 2
            lo, hi = plan.rank, n - plan.rank
            below = sorted((a for a in cands if order(a) < order(ans)), key=lambda a: (line_distance(a, ans), h(a)))
            above = sorted((a for a in cands if order(a) > order(ans)), key=lambda a: (line_distance(a, ans), h(a)))
            keep = set(below[:lo]) | set(above[:hi])
        return {name: error_model(name, (lambda s, v=outs[name]: v if v in keep or v in (None, NONE_KEY, ans) else None),
                                  m.describe) for name, m in models.items()}

    def derive(self, spec: Spec) -> Spec:
        """Printed intermediate: the path to check (raw, from the URL). Trap tags and depth are recomputed too, so a
        twin's meta.edge describes the twin."""
        raw = raw_path(spec.slots["URL"].value)
        s = spec.replace(derived={"PATH": S.glob_slot(raw)}, derived_deps={"PATH": ("URL",)})
        d = decide(s)
        env = s.env()
        tags = []
        if d.rules_by == "line" and d.tie:
            tags.append("tie")
        if d.rules_by == "line" and env[f"E{d.matched[0]}"] != ("allow" if d.rules_allowed else "disallow"):
            tags.append("first_match_loses")
        for g in ("star_over_named", "lookalike", "first_group_only"):
            k = variant_key(s, groups=g)
            if k is not None and key_allowed(k) != d.rules_allowed:
                tags.append("group_conflict")
                break
        if status_class(env.get("STATUS")) != "2xx":
            tags.append("status")
        if "%" in raw:
            tags.append("percent")
        if d.how == "none":
            tags.append("no_group")
        if len(_named_groups(s)) >= 2:
            tags.append("combined")
        if any(a != "*" and env[a] != env["UA"] and env[a].lower() == env["UA"].lower()
               for g in s.structure["groups"] for a in g["agents"]):
            tags.append("token_case")
        if status_class(env.get("STATUS")) != "2xx":
            depth = 1
        else:
            depth = 1 + int(len(s.structure["groups"]) > 1) + int("%" in raw)
        return s.replace(tags=tuple(tags), depth=depth, deep=depth > 2)

    # ------------------------------------------------------------------------------------------- solver A
    def solve_a(self, spec: Spec):
        d = decide(spec)
        if spec.qform != CHOICE_FORM:
            return answer_for(spec.qform, d.allowed)
        if d.by in ("nomatch", "nogroup"):
            return NONE_KEY
        if d.by != "line" or len(d.winners) != 1:
            raise ContractError("ch_line needs a 2xx status and exactly one deciding line")
        return line_key(spec.env(), d.winners[0])

    def canonical(self, spec: Spec) -> dict:
        env = spec.env()
        groups = [{"agents": ["*" if a == "*" else env[a] for a in g["agents"]],
                   "lines": [[env[f"E{n}"], env[f"P{n}"]] for n in g["lines"]]} for g in spec.structure["groups"]]
        return {"groups": groups, "crawler": env["UA"], "url": env["URL"], "path": env["PATH"],
                "status": env.get("STATUS"), "longest_rule": env["LONGEST"], "tie_rule": env["TIE"],
                "site": env["SITE"], "operator": env["OPERATOR"], "purpose": env["PURPOSE"], "qform": spec.qform}

    def canonical_for(self, spec: Spec, author_mode: str) -> dict:
        c = self.canonical(spec)
        return c if author_mode == "T" else {k: v for k, v in c.items() if k not in ("site", "operator", "purpose")}

    def extract_view(self, spec: Spec) -> dict:
        c = self.canonical(spec)
        return {k: c[k] for k in ("site", "operator", "purpose")}

    def extract_fields(self, spec: Spec) -> list:
        from c2_kit.g3h import Field
        return [Field("site", "name", "the website the crawler wants to visit, as written"),
                Field("operator", "name", "the organisation that runs the crawler, as written"),
                Field("purpose", "category", "what the crawler collects pages for", spec.slots["PURPOSE"].params)]

    # ------------------------------------------------------------------------------------------- render
    @staticmethod
    def row_key(spec: Spec) -> str:
        return f"{spec.family}|{spec.seed}|{spec.sampler}|{spec.qform}"

    def _rules_block(self, tb: TextBuilder, spec: Spec, slots: dict, forms: dict) -> None:
        groups = spec.structure["groups"]
        c = spec.structure["container"]
        if c == "robots":
            out = [RAW_HEAD]
            for gi, g in enumerate(groups):
                if gi:
                    out.append("")
                out += ["User-agent: *" if a == "*" else f"User-agent: {{{a}}}" for a in g["agents"]]
                out += [f"{{E{n}}}: {{P{n}:raw}}" for n in g["lines"]]
            out.append(RAW_TAIL)
            tb.add("state", K.fill("\n".join(out), slots, forms))
        elif c == "table":
            out = [TABLE_HEAD]
            for gi, g in enumerate(groups, 1):
                out += [f"| {gi} | User-agent | {'*' if a == '*' else '{' + a + '}'} |" for a in g["agents"]]
                out += [f"| {gi} | {{E{n}}} | {{P{n}:raw}} |" for n in g["lines"]]
            tb.add("state", K.fill("\n".join(out), slots, forms))
        elif c == "json":
            parts = []
            for g in groups:
                ua = ", ".join('"*"' if a == "*" else f'"{{{a}}}"' for a in g["agents"])
                ls = ", ".join(f'{{"type": "{{E{n}}}", "pattern": "{{P{n}:raw}}"}}' for n in g["lines"])
                parts.append(f'  {{"user_agents": [{ua}], "lines": [{ls}]}}')
            tpl = '{"groups": [\n' + ",\n".join(parts) + "\n]}"
            tb.add("state", JSON_HEAD + "\n")
            tb.add("state", K.fill(tpl, slots, forms, escape="json"))
        else:
            raise ContractError(f"container {c!r}")

    def render(self, spec: Spec, ctx, *, skin=None, wording=None, forms=None, attack=None):
        key = self.row_key(spec)
        held = spec.sampler in self.HELD_OUT_SAMPLERS
        ctx = self.ctx_for(spec, ctx)                  # never pick a wording that breaks the polarity rule
        skin = skin or ctx.pick(FAMILY, "skin", key, held_out=held)
        if wording is None:
            try:                                       # S5 (mixdev) rows take held-out wordings when the pool has one
                wording = ctx.pick(FAMILY, "wording", key, qform=spec.qform, held_out=held)
            except LookupError:
                if not held:
                    raise
                wording = ctx.pick(FAMILY, "wording", key, qform=spec.qform)
        if wording.qform != spec.qform:
            raise ContractError(f"wording {wording.skin_id} asks {wording.qform}, spec asks {spec.qform}")
        forms = forms or choose_forms(spec, key)
        slots = spec.all_slots()
        tb = TextBuilder()
        tb.add("state", skin.fill(slots, forms), skin_id=skin.skin_id)
        tb.add("state", "\n\n")
        self._rules_block(tb, spec, slots, forms)
        tb.add("state", "\n\n")
        tb.add("state", K.fill(REQUEST_TPL + (STATUS_LINE if "STATUS" in spec.slots else ""), slots, forms))
        if attack is not None:
            tb.add("state", "\n\n").add("state", attack.fill(slots, forms), skin_id=attack.skin_id)
        choice = spec.qform == CHOICE_FORM
        # G0 M21, H28: the served layout prints row.card once, on yes/no rows only (their definitions block); a choice
        # row keeps the card at the head of its instructions (printed twice, but its only place). place_rules does both.
        placed = CARDS.place_rules(tb, K.fill(card_template(spec.structure["card"], "STATUS" in spec.slots), slots, forms),
                                   self.QFORMS[spec.qform].qtype)
        tb.add("instructions", wording.fill(slots, forms), skin_id=wording.skin_id)
        ans = self.solve_a(spec)
        os_ = None
        if choice:
            os_ = self._line_options(spec, ans)
            if os_ is None:
                raise K.RenderError("fewer error-model lines than the drawn option count")
        style = CARDS.defs_style(placed, spec.structure["card"])
        return assemble_row(self, spec, tb, answer=ans, option_set=os_, skin=skin, wording=wording, forms=forms,
                            attack=attack, defs_style=style)

    # ------------------------------------------------------------------------------------------- relations
    def relations(self, spec: Spec) -> list:
        out = []
        q = self.QFORMS[spec.qform]
        u = lambda *k: uhash(FAMILY, "rel", spec.sampler, spec.seed, *k)   # noqa: E731
        if q.qtype == "noul":
            # the complement and its partner form are drawn per block of 4 yes/no bases (the block's two bases of a polarity
            # hold both outcomes), so each partner form gets as many yes as no golds (same reason as the negative forms)
            b = slot_of(spec.sampler, spec.seed)[1] // 4
            if strat(spec.sampler, "comp", b, 20) < round(P_COMPLEMENT * 20):
                if spec.qform == DOUBLE_NEG_FORM:
                    partner = "yn_not_allowed"          # one negation cue fewer: an exact syntactic complement
                elif q.polarity == 1:
                    v, partner = strat(spec.sampler, "partner", b, 10) / 10, NEG_PARTNER[-1][0]
                    acc = 0.0
                    for f, share in NEG_PARTNER:
                        acc += share
                        if v < acc - 1e-9:
                            partner = f
                            break
                else:
                    partner = POS_FORM
                out.append(RelationProposal("complement", qform=partner))
            if u("twin") < P_TWIN:
                t = self._twin(spec)
                if t is not None:
                    out.append(t)
        x = u("extra")
        if x < P_EQUIV:
            new = {"robots": "table", "table": "robots", "json": "robots"}[spec.structure["container"]]
            out.append(RelationProposal("equiv", spec=spec.replace(structure={**spec.structure, "container": new}),
                                        note=f"rules as {new}"))
        elif x < P_EQUIV + P_INV:
            out.append(RelationProposal("inv"))
        meta = self._metamorphic(spec)
        if spec.qform == CHOICE_FORM:            # keep the transforms whose rows can still show k named options
            meta = [m for m in meta if self._enough_distractors(self.derive(m.spec))]
        return out + meta

    def _twin(self, spec: Spec):
        """Exactly one input slot changes and the outcome flips; the prediction comes from the construction:
        a status twin moves the fetch status into the class that fixes the opposite outcome (4xx: fetch anything,
        5xx: fetch nothing); an effect twin flips the effect of the one deciding line (the longest matching line
        keeps its length, so after the flip its effect decides: Allow wins any tie, and a lone longest Disallow
        has no Allow at its length). No effect twin when the flipped line already exists (the twin file would hold
        one (effect, pattern) pair twice, which M1 forbids)."""
        d = decide(spec)
        env = spec.env()
        kinds = []
        # F2: a 4xx / 5xx status decides alone, so every row that shows one (a twin too) feeds G6's metadata view. A base
        # that already shows 4xx / 5xx has no line twin, so it takes the status twin; a base that shows a 2xx status takes it
        # rarely (P_TWIN_FROM_200); a base with no status never does (adding a slot is not a one-slot edit).
        if "STATUS" in spec.slots and (status_class(env["STATUS"]) != "2xx" or
                                       uhash(FAMILY, "twin200", spec.sampler, spec.seed) < P_TWIN_FROM_200):
            kinds.append("status")
        lines = {(env[f"E{m}"], env[f"P{m}"]) for g in spec.structure["groups"] for m in g["lines"]}
        if d.by == "line" and len(d.winners) == 1:
            n = d.winners[0]
            flipped = ("disallow" if env[f"E{n}"] == "allow" else "allow", env[f"P{n}"])
            if flipped not in lines:            # an emitted twin keeps M1: every (effect, pattern) pair distinct (H33)
                kinds.append("effect")
        pat = self._pattern_twin(spec, d, lines) if d.by == "nomatch" else None
        if pat is not None:
            kinds.append("pattern")
        if not kinds:
            return None
        kind = kinds[int(uhash(FAMILY, "twinkind", spec.sampler, spec.seed) * len(kinds))]
        if kind == "status":
            pool = STATUS_5XX if d.allowed else STATUS_4XX
            new = pool[int(uhash(FAMILY, "twinstatus", spec.sampler, spec.seed) * len(pool))]
            twin, changed = spec.with_slot("STATUS", S.category_slot(new, STATUS)), "STATUS"
        elif kind == "pattern":
            twin, changed = spec.with_slot(f"P{pat[0]}", S.glob_slot(pat[1])), f"P{pat[0]}"
        else:
            twin, changed = spec.with_slot(f"E{n}", S.category_slot(flipped[0], EFFECTS)), f"E{n}"
        return RelationProposal("twin", spec=self.derive(twin), changed_slot=changed,
                                expect=answer_for(spec.qform, not d.allowed), note=f"{kind} twin")

    def _pattern_twin(self, spec: Spec, d: Decision, lines: set):
        """(line number, pattern) for the third twin kind (F4 follow-up): a row where no applying line matches (the crawler
        may fetch) has no deciding line to flip, so twins skewed toward "may fetch" (allowed rows had a twin 61% of the
        time, blocked rows 96%) and every qform's yes rate with them. One slot changes: the pattern of an applying
        Disallow line becomes a pattern that matches the path. No other applying line matches, so that line alone
        decides and the outcome is "may not fetch" (checked by G-TW, as for every twin). None when no applying Disallow
        line exists or no matching pattern is free (M1: every (effect, pattern) pair stays distinct)."""
        env = spec.env()
        cand = [n for n in d.applying if env[f"E{n}"] == "disallow"]
        if not cand or d.how == "none":
            return None
        rng = random.Random(f"{FAMILY}|ptwin|{spec.sampler}|{spec.seed}")
        free = [p for p in _matching(rng, decode(raw_path(env["URL"]))) if len(p) >= MIN_PATTERN
                and ("disallow", p) not in lines]
        return (rng.choice(cand), rng.choice(free)) if free else None

    def _metamorphic(self, spec: Spec) -> list:
        """G4 relations (checked, never emitted); each predicts the same answer."""
        env = spec.env()
        out = []
        same = lambda s, note: RelationProposal("metamorphic", spec=s, expect="same", note=note)   # noqa: E731
        pack = self.pack_by_id[spec.pack]
        site = next(s for s in pack.sites if s != env["SITE"])
        url = f"https://{_host(site)}{raw_path(env['URL'])}"
        out.append(same(spec.replace(slots={**spec.slots, "SITE": S.name_slot(site), "URL": S.url_slot(url)}),
                        "rename the site (and its host)"))
        tok = env["UA"]
        out.append(same(spec.with_slot("UA", S.id_slot(tok.swapcase())), "change the letter case of the token"))
        groups = spec.structure["groups"]
        shuffled = [{**g, "lines": sorted(g["lines"], key=lambda n: uhash(FAMILY, "shuffle", spec.seed, n))}
                    for g in groups]
        if shuffled != groups:
            out.append(same(spec.replace(structure={**spec.structure, "groups": shuffled}), "shuffle lines"))
        if len(groups) > 1:
            rot = groups[1:] + groups[:1]
            out.append(same(spec.replace(structure={**spec.structure, "groups": rot}), "rotate the groups"))
        n_new = 1 + max(int(k[1:]) for k in spec.slots if k[0] == "E" and k[1:].isdigit())
        app, _ = applying(spec)
        gi = next((i for i, g in enumerate(groups) if app and app[0] in g["lines"]), 0)
        pats = {env[f"P{n}"] for g in groups for n in g["lines"]}
        dpath = decode(raw_path(env["URL"]))
        inert = next((p for p in sorted(INERT, key=lambda p: uhash(FAMILY, "inert", spec.seed, p))
                      if p not in pats and not vmatch(p, dpath)), None)     # a literal pattern the path misses (H33)
        if inert is not None:
            g2 = [dict(g, lines=list(g["lines"]) + ([n_new] if i == gi else [])) for i, g in enumerate(groups)]
            eff = EFFECT_KEYS[int(uhash(FAMILY, "inert_eff", spec.seed) * 2)]
            s = spec.replace(slots={**spec.slots, f"E{n_new}": S.category_slot(eff, EFFECTS),
                                    f"P{n_new}": S.glob_slot(inert)},
                             structure={**spec.structure, "groups": g2})
            out.append(same(s, "add an inert line"))
        raw = raw_path(env["URL"])
        pos = encodable(raw)
        if pos:
            i = pos[int(uhash(FAMILY, "pct", spec.seed) * len(pos))]
            host = env["URL"][: len(env["URL"]) - len(raw)]
            out.append(same(spec.with_slot("URL", S.url_slot(host + percent_encode(raw, {i}))),
                            "percent-encode one unreserved path character"))
        return out

    # ------------------------------------------------------------------------------------------- error models
    def error_models(self) -> dict:
        def ch(**kw):
            return lambda s: variant_key(s, **kw) if s.qform == CHOICE_FORM else None

        def only_if(test, **kw):
            return lambda s: variant_key(s, **kw) if s.qform == CHOICE_FORM and test(s) else None

        has_anchor = lambda s: any(v.value.endswith("$") for k, v in s.slots.items()                 # noqa: E731
                                   if k[0] == "P" and k[1:].isdigit())
        has_pct = lambda s: "%" in raw_path(s.env()["URL"])                                         # noqa: E731
        has_query = lambda s: "?" in raw_path(s.env()["URL"])                                       # noqa: E731
        spec_models = {
            "first_match": ch(pick="first"),
            "last_match": ch(pick="last"),
            "effect_order": ch(pick="effect_order"),
            "robots_disallow_wins_tie": ch(pick="tie_disallow"),
            "robots_allow_wins": ch(pick="allow_wins"),
            "robots_length_literals_only": ch(pick="literal_len"),
            "robots_star_group_over_named": ch(groups="star_over_named"),
            "robots_lookalike_group": ch(groups="lookalike"),
            "robots_first_group_only": ch(groups="first_group_only"),
            "robots_merge_star_group": ch(groups="merge_star"),
            "robots_ignore_end_anchor": only_if(has_anchor, dollar=False),
            "robots_star_stops_at_slash": ch(star_slash=False),
            "robots_whole_path": ch(whole=True),
            "robots_no_percent_decode": only_if(has_pct, path="raw"),
            "robots_path_case_ignored": ch(icase=True),
            "robots_query_ignored": only_if(has_query, path="no_query"),
        }
        return {name: error_model(name, fn) for name, fn in spec_models.items()}
