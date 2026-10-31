"""Build raw rows for webred (WebRED: Web Relation Extraction Dataset, Ormandi et al. 2021, Google).

Source : GitHub google-research-datasets/WebRED @3e5e6a43, webred_21.tfrecord ONLY (the "WebRED 2+1" set that the
         paper uses for fine-tuning; webred_5.tfrecord, the paper's evaluation set, is never read). Git-LFS object,
         sha256 pinned. Parsed with a small built-in TFRecord / tf.train.Example reader (no TensorFlow).
Licence: CC BY 4.0 (README.md of the repo, section "License": "This data is licensed by Google LLC under a Creative
         Commons Attribution 4.0 International License").
Texts  : English sentences from many kinds of web pages, with the subject marked SUBJ{...} and object OBJ{...}.
Labels : for each (sentence, subject, object, candidate Wikidata relation), 2 human raters (a 3rd on disagreement)
         judged whether the sentence expresses the relation (num_pos_raters / num_raters).
Tasks  : multi-way relation choice, markers rewritten to <e1> (subject) and <e2> (object); the question names each
         entity by its first marked mention.
  (a) judged sets: the same marked sentence was judged for 2-5 candidate relations. Options = exactly those judged
      candidates + "none of the listed relations" (+ the inverse of the positive relation when it exists, which
      cannot also hold). Every judgement must be unanimous and at most one candidate positive; gold = the positive
      candidate, or "none" when raters rejected every candidate.
  (b) direction sets: a sentence judged (unanimously) to express an asymmetric relation R that has a Wikidata
      inverse (part of / has part, capital / capital of, located in / contains, owned by / owner of, ...). Options =
      R, inverse(R) and "none"; gold = R. The inverse and "none" are false by construction.
Filters: every option must have a Claude-written definition; 8-90 words; a full sentence (capital start, final
         punctuation); no URLs, citation or listing debris (publisher/accessed/reviews/phone); marked spans
         that are generic lower-case nouns (e.g. SUBJ{town}) are rejected; exact/near-duplicate sentences dropped
         (one row per sentence); overlap with FewRel/Few-NERD (OHS-3), label-NLI, local files and other v14 parts
         (incl. redocred) removed. Caps: 230 rows per gold relation, 220 per identical judged-candidate set for "none"
         rows (40 for all-numeric sets such as unemployment rate / compulsory-education age), "none" <= 36% of rows.
         A "none" row is also dropped when the sentence contains a trigger word of a rejected candidate (e.g.
         'neighbouring' for shares border with, 'capital' for capital of): such rejections may be rater misses.
Review fixes (2026-09-29): (1) judged sets that include 'location of formation' (P740) are dropped: raters used it
         inconsistently for supplier/publisher addresses ('Elsevier, Amsterdam' = formation in one row, none in
         another); (2) "none" rows whose rejected candidates include 'headquarters location' are dropped (address
         patterns such as 'St. Jude Medical, St. Paul, MN' were rejected as HQ); (3) rows whose subject and object are
         the same string (e.g. gene DPPIV 'encodes' protein DPPIV) are dropped; (4) reference-list / bibliography
         entries ('Skeggs, B. 2004 ..., London: Routledge', '688 pp.', PhD thesis) are treated as citation debris;
         (5) rows whose gold is 'located in the administrative territorial entity' (P131) while entity 2 is a country
         (or 'country' was a rejected candidate) are dropped: the definition says 'below country level' and raters
         split P131 / country arbitrarily for country tails ('California ... USA').
Deterministic (seed 20261129).
"""
import collections
import random
import re
import struct

import _re_common as C
from build_redocred import REL as DOCRED_REL

KEY = "webred"
COMMIT = "3e5e6a43b468bcf48424e9fdb9f2f8b06373e98f"
URL = f"https://media.githubusercontent.com/media/google-research-datasets/WebRED/{COMMIT}/webred_21.tfrecord"
SHA = "500ff49030ad90b809db3bcd9026517d44596c14b161a7411ee29b43d944c9d8"
LICENCE = (f"CC BY 4.0 (https://github.com/google-research-datasets/WebRED/blob/{COMMIT}/README.md, 'This data is "
           "licensed by Google LLC under a Creative Commons Attribution 4.0 International License')")
DATASET = "WebRED (google-research-datasets/WebRED), webred_21.tfrecord (WebRED 2+1, the fine-tuning set)"
CAP_REL = 230
CAP_NONE_SET = 220
CAP_NONE_NUMERIC = 40
NONE_SHARE = 0.36
NONE = "none of the listed relations"

EXTRA = {  # WebRED relations not in the DocRED set: P-id -> (name, definition)
    "P530": ("diplomatic relation", "The sentence states that entity 1 and entity 2, two states, have official state-to-state relations (embassies, ambassadors, treaties, alliances, state visits); merely naming both countries does not count."),
    "P47": ("shares border with", "The sentence states that entity 1 and entity 2 (countries, regions or places) share a common border ('bordered by', 'neighbouring'); being mentioned together does not count."),
    "P1121": ("oxidation state", "Entity 2 is an oxidation state (e.g. +2, -1) that entity 1, a chemical element, has or can take."),
    "P1279": ("inflation rate", "Entity 2 is the inflation rate (percentage rise in consumer prices) of entity 1, a country or economy."),
    "P1198": ("unemployment rate", "Entity 2 is the unemployment rate (share of the labour force without work) of entity 1, a country, region or city."),
    "P3000": ("marriageable age", "Entity 2 is the minimum legal age at which people may marry in entity 1, a country or jurisdiction."),
    "P2997": ("age of majority", "Entity 2 is the age at which a person legally becomes an adult in entity 1, a country or jurisdiction."),
    "P2404": ("time-weighted average exposure limit", "Entity 2 is the permissible time-weighted average (e.g. 8-hour) workplace exposure limit for entity 1, a chemical substance."),
    "P138": ("named after", "Entity 1 is named after entity 2: entity 2 is the person, place or thing that entity 1's name honours or comes from."),
    "P3270": ("compulsory education (minimum age)", "Entity 2 is the age at which compulsory schooling begins in entity 1, a country or jurisdiction."),
    "P3271": ("compulsory education (maximum age)", "Entity 2 is the age at which compulsory schooling ends in entity 1, a country or jurisdiction."),
    "P2936": ("language used", "Entity 2 is a language used by entity 1 (a community, people, country or organisation) in daily life, worship or official business."),
    "P4841": ("total fertility rate", "Entity 2 is the total fertility rate (average number of children born per woman) of entity 1, a country or region."),
    "P647": ("drafted by", "Entity 1, an athlete, was selected by entity 2, a sports team, in a draft."),
    "P1108": ("electronegativity", "Entity 2 is the electronegativity value of entity 1, a chemical element."),
    "P1532": ("country for sport", "Entity 2 is the country that entity 1, an athlete or sports team, represents in international competition."),
    "P1889": ("different from", "Entity 1 and entity 2 are distinct things that are easily confused (similar names or meanings), and the sentence tells them apart."),
    "P1086": ("atomic number", "Entity 2 is the atomic number (number of protons) of entity 1, a chemical element."),
    "P169": ("chief executive officer", "Entity 2 is the chief executive officer (CEO) of entity 1, a company or organisation."),
    "P1830": ("owner of", "Entity 2 is something (a company, building, team, property or product) that entity 1 owns or owned (the inverse of 'owned by')."),
    "P291": ("place of publication", "Entity 2 is the place where entity 1, a publication such as a book, newspaper or journal, was published."),
    "P2200": ("electric charge", "Entity 2 is the electric charge of entity 1, a particle or ion."),
    "P103": ("native language", "Entity 2 is the first language that entity 1, a person, learned from birth."),
    "P119": ("place of burial", "Entity 2 is the place (cemetery, church, town) where entity 1, a person, is buried."),
    "P451": ("unmarried partner", "Entity 1 and entity 2 are or were a romantic couple without being married (boyfriend, girlfriend, domestic partner)."),
    "P2129": ("IDLH", "Entity 2 is the IDLH value, the airborne concentration immediately dangerous to life or health, for entity 1, a chemical substance."),
    "P2405": ("ceiling exposure limit", "Entity 2 is the ceiling exposure limit, a concentration that must never be exceeded, for entity 1, a chemical substance."),
    "P2407": ("short-term exposure limit", "Entity 2 is the short-term (usually 15-minute) exposure limit for entity 1, a chemical substance."),
    "P1589": ("lowest point", "Entity 2 is the lowest point (lowest elevation) of entity 1, a country, region or landmass."),
    "P466": ("occupant", "Entity 2 is a person, team or organisation that occupies or uses entity 1, a building, stadium or facility (e.g. a team's home ground)."),
    "P750": ("distributor", "Entity 2 distributes entity 1 (a film, product or publication) to the market."),
    "P1148": ("neutron number", "Entity 2 is the number of neutrons in entity 1, an isotope or atomic nucleus."),
    "P2541": ("operating area", "Entity 2 is a geographic area where entity 1, an organisation, company or service, operates."),
    "P2341": ("indigenous to", "Entity 2 is the place or region where entity 1 (a people, language, species or tradition) is native."),
    "P98": ("editor", "Entity 2 is an editor of entity 1 (a publication, periodical, anthology or book)."),
    "P1037": ("director/manager", "Entity 2 is the person who directs or manages entity 1, an organisation (director, manager, head)."),
    "P2998": ("age of candidacy", "Entity 2 is the minimum age at which a person may stand for office in entity 1, a jurisdiction or elected body."),
    "P61": ("discoverer or inventor", "Entity 2 discovered or invented entity 1 (an object, place, law, technique or chemical element)."),
    "P931": ("place served by transport hub", "Entity 2 is the city or area that entity 1, an airport, station or port, serves."),
    "P1408": ("licensed to broadcast to", "Entity 2 is the place that entity 1, a radio or TV station, is licensed to serve."),
    "P1066": ("student of", "Entity 1 was a student or pupil of entity 2, a teacher or mentor."),
    "P802": ("student", "Entity 2 was a student or pupil of entity 1 (the inverse of 'student of')."),
    "P1431": ("executive producer", "Entity 2 was an executive producer of entity 1 (a film, TV series or album)."),
    "P2855": ("VAT-rate", "Entity 2 is the value-added tax (VAT) rate charged in entity 1, a country or territory."),
    "P2257": ("frequency of event", "Entity 2 is how often entity 1, a recurring event, takes place (e.g. every four years, annually)."),
    "P287": ("designed by", "Entity 2 designed entity 1 (a building, vehicle, typeface, product or object)."),
    "P184": ("doctoral advisor", "Entity 2 supervised the doctoral thesis of entity 1."),
    "P2043": ("length", "Entity 2 is the length of entity 1 (e.g. a river, road, bridge or vessel)."),
    "P1346": ("winner", "Entity 2 won entity 1, a competition, award, prize or election (the inverse of 'award received')."),
    "P2999": ("age of consent", "Entity 2 is the legal age of consent to sexual activity in entity 1, a jurisdiction."),
    "P702": ("encoded by", "Entity 2 is the gene that encodes entity 1, a protein or RNA."),
    "P688": ("encodes", "Entity 2 is the protein or RNA product encoded by entity 1, a gene."),
    "P101": ("field of work", "Entity 2 is the field or discipline in which entity 1, a person or organisation, works."),
    "P106": ("occupation", "Entity 2 is the occupation or profession of entity 1, a person."),
    "P641": ("sport", "Entity 2 is the sport that entity 1 (an athlete, team, league or event) plays or is about."),
    "P793": ("significant event", "Entity 2 is a significant event (e.g. a disaster, launch, merger, battle) that happened to or involved entity 1."),
    "P84": ("architect", "Entity 2 is the architect who designed entity 1, a building or structure."),
    "P81": ("connecting line", "Entity 2 is a railway or transit line that serves entity 1, a station or stop."),
    "P407": ("language of work or name", "Entity 2 is the language in which entity 1, a work or name, is written, spoken or published."),
    "P376": ("located on astronomical location", "Entity 2 is the astronomical body (planet, moon, asteroid) on which entity 1, a feature or place, lies."),
    "P3342": ("significant person", "Entity 2 is a person with a notable role in the life or history of entity 1."),
    "P1027": ("conferred by", "Entity 2 is the person or organisation that awards or confers entity 1, a prize, honour or degree."),
}
EXTRA_ALIASES = {"P179": "series"}  # WebRED 'part of the series' == DocRED 'series'
INVERSE = {"P131": "P150", "P150": "P131", "P36": "P1376", "P1376": "P36", "P361": "P527", "P527": "P361",
           "P155": "P156", "P156": "P155", "P749": "P355", "P355": "P749", "P127": "P1830", "P1830": "P127",
           "P1365": "P1366", "P1366": "P1365", "P710": "P1344", "P1344": "P710", "P674": "P1441", "P1441": "P674",
           "P166": "P1346", "P1346": "P166", "P688": "P702", "P702": "P688", "P176": "P1056", "P1056": "P176",
           "P1066": "P802", "P802": "P1066", "P22": "P40", "P25": "P40"}
TEMPORAL = {"P569", "P570", "P571", "P576", "P577", "P580", "P582", "P585"}
NUMERIC = {"P1121", "P1279", "P1198", "P3000", "P2997", "P2404", "P3270", "P3271", "P4841", "P1108", "P1086",
           "P2200", "P2129", "P2405", "P2407", "P1148", "P2998", "P2855", "P2043", "P2999"}
GENERIC = {"town", "city", "village", "country", "state", "county", "region", "province", "river", "company",
           "university", "band", "team", "party", "capital", "island", "district", "municipality", "people",
           "government", "nation", "club", "album", "song", "film", "school", "church", "king", "president",
           "he", "she", "it", "they", "his", "her", "its", "their", "we", "i", "you"}
DEBRIS = re.compile(r"https?:|www\.|\bdoi\b|\bISBN\b|\bpp?\.\s?\d|\bvol\.|--|\bet al\b|©|\[\d+\]|\||"
                    r"\baccessed\b|\bretrieved\b|\bpress\b|\bpublish(ing|er|ers)\b|\byelp\b|phone number|"
                    r"tripadvisor|\breviews?\b|\(\s*[A-Z][\w .]+:\s*[^()]*\d{4}\s*\)|``", re.I)
REFERENCE = re.compile(  # bibliography entries (review fix)
    r"^[A-Z][A-Za-z'’\-]+,\s(?:[A-Z]\.\s?-?){1,3}"             # 'Skeggs, B.' / 'Gee, J.P.'
    r"|^\d+\s[A-Z][A-Za-z'’\-]+,\s[A-Z]\."                    # numbered entry '33 Mei, Z.'
    r"|^[A-Z][a-z]+\s[A-Z]{1,2},\s[A-Z][a-z]+\s[A-Z]{1,2}\b"        # Vancouver style 'Dahl E, Johannessen T'
    r"|^[^.]{0,40}\(\d{4}[a-z]?\)[,.]"                               # 'Post (2008), ...'
    r"|^[A-Z][a-z]+,\sand\s[A-Z]\."                                  # 'Klima, and L. Taylor'
    r"|\b\d+\s?pp\b"                                                # page counts '688 pp.'
    r"|\b[A-Z][a-z]+\s?:\s?(?:Routledge|Elsevier|Springer|Wiley|Academic Press|[A-Z][a-z]+ University Press)"
    r"|\(Eds?\.\)|\bStandard Ed\.|\bPh\.?\s?D\.?\s[Tt]hesis|\bPhD\s(?:[Tt]hesis|[Dd]issertation)")
COUNTRY = re.compile(  # country names / demonyms used to catch P131 golds with a country tail (review fix)
    r"^(?:the\s)?(?:U\.?S\.?A?\.?|United States(?: of America)?|America|American|UK|U\.K\.|United Kingdom|Britain|"
    r"Great Britain|British|England|English|Scotland|Scottish|Wales|Welsh|Northern Ireland|Ireland|Irish|Canada|"
    r"Canadian|Australia|Australian|New Zealand|India|Indian|China|Chinese|Japan|Japanese|Germany|German|France|"
    r"French|Italy|Italian|Spain|Spanish|Portugal|Mexico|Mexican|Brazil|Russia|Russian|Poland|Polish|Netherlands|"
    r"Dutch|Belgium|Sweden|Swedish|Norway|Norwegian|Denmark|Danish|Finland|Austria|Switzerland|Swiss|Greece|Greek|"
    r"Turkey|Turkish|Iran|Iraq|Israel|Egypt|Nigeria|Kenya|South Africa|Argentina|Chile|Peru|Colombia|Venezuela|"
    r"Pakistan|Bangladesh|Indonesia|Philippines|Vietnam|Thailand|Malaysia|Korea|South Korea|North Korea|Taiwan|"
    r"Ukraine|Czech Republic|Hungary|Romania|Bulgaria|Serbia|Croatia|Uganda|Tanzania|Ghana|Ethiopia|Morocco|Algeria|"
    r"Saudi Arabia|Afghanistan|Nepal|Sri Lanka|Cuba|Jamaica|Iceland|Estonia|Latvia|Lithuania|Slovakia|Slovenia)$",
    re.I)
SENTENCE = re.compile(r"^[\"'“(]?[A-Z0-9].*[.!?][\"'”)]?$", re.S)
KEYWORDS = {  # trigger words: a unanimous "not expressed" judgement next to one of these is not trusted
    "P47": re.compile(r"border|neighbo|adjacent|bounded|adjoin", re.I),
    "P530": re.compile(r"embass|ambassador|diplomat|treaty|relations|alliance|allies|bilateral|sanction|state visit", re.I),
    "P36": re.compile(r"capital|seat of", re.I), "P1376": re.compile(r"capital|seat of", re.I),
    "P19": re.compile(r"\bborn\b|native of|birth", re.I), "P20": re.compile(r"\bdied\b|death", re.I),
    "P26": re.compile(r"married|wife|husband|spouse|widow", re.I), "P159": re.compile(r"headquarter|based in|\bHQ\b", re.I),
    "P740": re.compile(r"formed|founded|established", re.I), "P37": re.compile(r"official", re.I),
    "P1198": re.compile(r"unemploy|jobless", re.I), "P1279": re.compile(r"inflation", re.I),
}
Q = ('Which relation from entity 1 ("{h}", marked <e1>) to entity 2 ("{t}", marked <e2>) does the sentence express? '
     'Read each option as entity 1 -> entity 2.')


# ---------------------------------------------------------------------------------- minimal TFRecord reader
def _varint(b, i):
    r = s = 0
    while True:
        x = b[i]
        i += 1
        r |= (x & 0x7F) << s
        s += 7
        if not x & 0x80:
            return r, i


def _fields(b):
    i = 0
    while i < len(b):
        k, i = _varint(b, i)
        f, w = k >> 3, k & 7
        if w == 0:
            v, i = _varint(b, i)
        elif w == 2:
            n, i = _varint(b, i)
            v = b[i:i + n]
            i += n
        elif w == 5:
            v = b[i:i + 4]
            i += 4
        elif w == 1:
            v = b[i:i + 8]
            i += 8
        else:
            raise ValueError(w)
        yield f, w, v


def _example(b):
    out = {}
    for _, _, feats in _fields(b):                 # Example.features
        for _, _, entry in _fields(feats):         # Features.feature (map entry)
            key = val = None
            for f3, _, v3 in _fields(entry):
                if f3 == 1:
                    key = v3.decode()
                else:
                    val = v3
            for kind, _, lst in _fields(val):      # Feature oneof: 1 bytes, 2 float, 3 int64
                vals = []
                for _, w5, v5 in _fields(lst):
                    if kind == 1:
                        vals.append(v5.decode("utf-8"))
                    elif kind == 3 and w5 == 2:
                        j = 0
                        while j < len(v5):
                            x, j = _varint(v5, j)
                            vals.append(x)
                    elif kind == 3:
                        vals.append(v5)
                out[key] = vals
    return out


def read_tfrecord(path):
    with open(path, "rb") as f:
        while True:
            h = f.read(8)
            if len(h) < 8:
                break
            n = struct.unpack("<Q", h)[0]
            f.read(4)
            d = f.read(n)
            f.read(4)
            yield _example(d)


# ----------------------------------------------------------------------------------------------------------
def names():
    nm = {}
    for pid, (n, d) in DOCRED_REL.items():
        nm[pid] = (n, d)
    nm.update(EXTRA)
    return nm


def convert(s):
    """SUBJ{..} -> <e1>..</e1>, OBJ{..} -> <e2>..</e2>; returns (state, subj_spans, obj_spans) or None."""
    subj = re.findall(r"SUBJ\{(.*?)\}", s)
    obj = re.findall(r"OBJ\{(.*?)\}", s)
    if not subj or not obj:
        return None
    t = re.sub(r"SUBJ\{(.*?)\}", r"<e1>\1</e1>", s)
    t = re.sub(r"OBJ\{(.*?)\}", r"<e2>\1</e2>", t)
    if "{" in C.strip_markers(t) or "}" in C.strip_markers(t):
        return None
    return C.clean(t), subj, obj


def main():
    rng = random.Random(C.SEED)
    path = C.fetch(URL, C.CACHE / KEY / "webred_21.tfrecord", SHA)
    ex = list(read_tfrecord(path))
    assert len(ex) == 107819, len(ex)
    NM = names()
    assert len({v[0] for v in NM.values()}) == len(NM)
    groups = collections.defaultdict(list)
    for e in ex:
        groups[e["sentence"][0]].append(e)

    def unanimous(e):
        return e["num_raters"][0] >= 2 and e["num_pos_raters"][0] in (0, e["num_raters"][0])

    stats = collections.Counter()
    cands = []
    for s, g in sorted(groups.items()):
        pids = [e["relation_id"][0] for e in g]
        if len(set(pids)) != len(pids):
            stats["dup_relation"] += 1
            continue
        if not all(p in NM for p in pids):
            stats["undefined_relation"] += 1
            continue
        conv = convert(s)
        if conv is None:
            stats["markers"] += 1
            continue
        state, subj, obj = conv
        plain = C.strip_markers(state)
        nw = len(C.words(plain))
        if nw < 8 or nw > 90 or DEBRIS.search(plain) or not SENTENCE.match(plain):
            stats["length_or_debris"] += 1
            continue
        if REFERENCE.search(plain):
            stats["reference_entry"] += 1
            continue
        if "P740" in pids:
            stats["formation_hq_confusion"] += 1
            continue
        if subj[0].strip().lower() == obj[0].strip().lower():
            stats["same_string_pair"] += 1
            continue
        if any(m.strip().lower() in GENERIC for m in subj + obj):
            stats["generic_mention"] += 1
            continue
        if not all(unanimous(e) for e in g):
            stats["not_unanimous"] += 1
            continue
        pos = [e["relation_id"][0] for e in g if e["num_pos_raters"][0] > 0]
        if len(pos) > 1:
            stats["multi_positive"] += 1
            continue
        if len(g) >= 2:
            kind = "judged"
            gold = pos[0] if pos else None
            opts = sorted(pids)
            if gold and INVERSE.get(gold) in NM and INVERSE[gold] not in opts:
                opts.append(INVERSE[gold])
        else:
            if not pos or pos[0] not in INVERSE or INVERSE[pos[0]] not in NM:
                stats["single_unusable"] += 1
                continue
            kind = "direction"
            gold = pos[0]
            opts = [gold, INVERSE[gold]]
        if gold is None and any(KEYWORDS.get(p) and KEYWORDS[p].search(plain) for p in pids):
            stats["none_but_keyword"] += 1   # a rejected candidate's trigger word is present: possible rater miss
            continue
        if gold == "P131" and ("P17" in pids or COUNTRY.match(obj[0].strip())):
            stats["p131_country_tail"] += 1  # conflicts with the 'below country level' definition
            continue
        if gold is None and "P159" in pids:
            stats["none_with_hq"] += 1       # HQ rejections of 'Company, City' address patterns are unreliable
            continue
        cands.append({"sent": s, "state": state, "plain": plain, "subj": subj[0].strip(), "obj": obj[0].strip(),
                      "kind": kind,
                      "gold": gold, "opts": opts, "judged": sorted(pids),
                      "votes": {e["relation_id"][0]: [e["num_pos_raters"][0], e["num_raters"][0]] for e in g},
                      "url": g[0]["url"][0]})
    print("candidates:", len(cands), collections.Counter(c["kind"] for c in cands), dict(stats))

    # decontamination (sentence text)
    core = {str(i): [c["plain"]] for i, c in enumerate(cands)}
    hits = C.decon(core, KEY, extra_texts=C.ohs3_wiki_texts())
    hits.update(C.cross_v14(core, {KEY}))
    cands = [c for i, c in enumerate(cands) if str(i) not in hits]
    print("after decon:", len(cands))

    rng.shuffle(cands)
    # judged sets first (they carry real negative judgements), then direction rows
    cands.sort(key=lambda c: 0 if c["kind"] == "judged" else 1)
    nd = C.NearDup(thr=0.7)
    per_gold = collections.Counter()
    per_none_set = collections.Counter()
    pos_rows, none_rows = [], []
    for c in cands:
        g = c["gold"]
        if g is None:
            sig = tuple(c["judged"])
            cap = CAP_NONE_NUMERIC if set(sig) <= NUMERIC else CAP_NONE_SET
            if per_none_set[sig] >= cap:
                continue
        elif per_gold[g] >= CAP_REL:
            continue
        if nd.seen(c["plain"]):
            continue
        if g is None:
            per_none_set[tuple(c["judged"])] += 1
            none_rows.append(c)
        else:
            per_gold[g] += 1
            pos_rows.append(c)
    n_none = min(len(none_rows), int(NONE_SHARE / (1 - NONE_SHARE) * len(pos_rows)))
    sel = pos_rows + none_rows[:n_none]
    print("positive:", len(pos_rows), "none available:", len(none_rows), "none kept:", n_none)

    rows = []
    for c in sel:
        opts = [NM[p][0] for p in c["opts"]]
        rng.shuffle(opts)
        opts.append(NONE)
        gold = NM[c["gold"]][0] if c["gold"] else NONE
        tags = []
        rel_ids = set(c["opts"])
        if rel_ids & NUMERIC:
            tags.append("numeric")
        if rel_ids & TEMPORAL:
            tags.append("temporal")
        if c["gold"] is None:
            tags.append("missing_info")
        if C.NEG.search(c["plain"]):
            tags.append("negation")
        if C.REPORTED.search(c["plain"]):
            tags.append("reported_speech")
        rows.append({
            "key": KEY,
            "rid": f"webred21:{C.sha256_text(c['sent'])[:16]}",
            "state": c["state"],
            "instructions": Q.format(h=c["subj"], t=c["obj"]),
            "options": opts,
            "gold": gold,
            "soft": None,
            "meta": {"dataset": DATASET,
                     "config": ("judged candidate set (every option except the inverse and 'none' was rated)"
                                if c["kind"] == "judged" else "direction set: rated relation vs its Wikidata inverse"),
                     "revision": f"git:{COMMIT}; sha256:{SHA}", "licence": LICENCE, "split": "train",
                     "orig_label": {"votes_pos_of_total": c["votes"], "gold_pid": c["gold"], "url": c["url"]},
                     "family": C.FAMILY, "edge": C.edge_join(tags)},
        })
    rng.shuffle(rows)
    used = {o for r in rows for o in r["options"]}
    defs = {n: d for n, d in NM.values() if n in used}
    defs[NONE] = ("The sentence expresses none of the listed relations from entity 1 to entity 2: the entities may only "
                  "be mentioned together, related in another way, or related only in the reverse direction.")
    C.write_outputs(KEY, rows, {None: defs})
    st = C.summary(KEY, rows)
    print("kinds:", collections.Counter(r["meta"]["config"][:6] for r in rows))
    C.show_samples(rows, 5)
    notes = ("WebRED 2+1 (web sentences, 2-3 human raters per sentence x candidate relation; the WebRED-5 eval set is "
             "never read). (a) sentences rated for 2-5 candidate relations: options = the rated candidates (+ the "
             "positive's inverse) + 'none of the listed relations', gold = the unanimous positive or none; (b) "
             "unanimous positives of an asymmetric relation: options = relation, its Wikidata inverse, none. Only "
             "unanimous judgements; none <= 36%; 230 rows per relation; citation debris and generic marked nouns "
             "dropped; FewRel/Few-NERD (OHS-3), label-NLI, local and other v14 overlaps removed."
             " Review fixes: P740 (formation) sets, none rows with a rejected HQ candidate, same-string pairs, bibliography entries and P131 golds with a country tail dropped.")
    C.append_manifest(C.manifest_record(KEY, DATASET, LICENCE, rows, "choice (relation type or none, 3-6 options)",
                                        notes, st))


if __name__ == "__main__":
    main()
