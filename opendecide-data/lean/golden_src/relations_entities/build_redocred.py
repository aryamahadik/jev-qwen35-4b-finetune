"""Build raw rows for redocred (Re-DocRED: DocRED train documents with revised, completed relation annotations).

Source : GitHub tonytan48/Re-DocRED @ccfb54f5 (Tan et al., EMNLP 2022), data/train_revised.json ONLY (dev/test never
         read). sha256 pinned. The documents are the 3,053 human-annotated DocRED train documents (Yao et al. 2019):
         English Wikipedia lead sections with human-annotated entity mentions and relation triples over 96 Wikidata
         properties; Re-DocRED annotators re-checked every document and added missing triples (human-verified).
Licence: MIT (https://github.com/tonytan48/Re-DocRED/blob/ccfb54f5ddf5836027c87badda10f6dfc56efaac/LICENSE,
         "Copyright (c) 2023 tonytan48"); DocRED itself is MIT too (github thunlp/DocRED LICENSE).
Task   : relation classification as a multi-way decision. State = a window of 1-4 consecutive sentences from one
         document that covers all human evidence sentences of the triple, with EVERY mention of the head entity
         wrapped in <e1>...</e1> and every mention of the tail entity in <e2>...</e2>. Options = the gold relation, 2-9
         relation types that are type-compatible with the pair (same DocRED head/tail entity types) and never
         co-annotated with the gold in this corpus, plus "none of the listed relations". Hard near-misses are
         preferred: the inverse relation (part of / has part, capital / capital of, follows / followed by, ...) is
         always offered when it is type-compatible.
         About 12% of rows are "none" rows: the pair's annotated relation(s) are REMOVED from the option list, so the
         correct answer is "none of the listed relations" (distractors exclude everything the pair's relations are
         ever co-annotated with, so no listed option can be true).
Safety : only triples that carry DocRED evidence sentences are used (Re-DocRED's added triples have none, so their
         supporting text is unknown); every relation annotated for the pair (symmetric relations in both directions)
         is excluded from the distractors; relations co-annotated with the gold on >= 1% of either relation's pairs, and
         a hand list of implied relations, are never distractors. P1001 is never used with a person head (DocRED uses
         it inconsistently there), P1198 (2 triples) is dropped, and a P131 or P205 triple whose pair also has P17 (country
         tail) is only asked as 'country'. Review fix (2026-09-29): triples whose (head type, tail type) signature covers < 3%
         of that relation's annotated triples are dropped (type-implausible annotations such as place of death -> a
         hockey team, country -> a person); a team a player is a member of is never offered as 'employer'.
Dedupe : windows inside one document never overlap (each sentence is shown at most once in the whole dataset);
         exact/near-duplicate windows dropped. Sentences overlapping FewRel or Few-NERD (OHS-3 sources, Wikipedia),
         the label-NLI tasks, local train/dev/eval files or other v14 parts are removed before windows are built, and
         (review fix) the finished multi-sentence window is checked again as a whole, so a 10-word run that crosses a
         sentence boundary is caught too.
Deterministic (seed 20261129).
"""
import collections
import itertools
import json
import random

import _re_common as C

KEY = "redocred"
COMMIT = "ccfb54f5ddf5836027c87badda10f6dfc56efaac"
URL = f"https://raw.githubusercontent.com/tonytan48/Re-DocRED/{COMMIT}/data/train_revised.json"
SHA = "c40a137a1c57f3e2daaf5ebf511eaa1518f9305ffaa3052d46271921a91826f2"
LICENCE = (f"MIT (https://github.com/tonytan48/Re-DocRED/blob/{COMMIT}/LICENSE, 'Copyright (c) 2023 tonytan48'; "
           "underlying DocRED: MIT, https://github.com/thunlp/DocRED/blob/master/LICENSE)")
DATASET = "Re-DocRED (tonytan48/Re-DocRED, revised DocRED), data/train_revised.json"
TARGET = 7600
CAP_PER_REL = 340
NONE_SHARE = 0.12
MAX_WIN = 4
NONE = "none of the listed relations"

# P-id -> (option name, definition). Definitions read entity 1 = <e1>, entity 2 = <e2>.
REL = {
    "P6": ("head of government", "Entity 2 is the head of government (prime minister, premier, mayor, chief minister) of entity 1, a country, state, province or city."),
    "P17": ("country", "Entity 2 is the sovereign country in which entity 1 (a place, building, organisation, event or object, not a person) is located or to which it belongs."),
    "P19": ("place of birth", "Entity 2 is the place (city, town, region or country) where entity 1, a person, was born."),
    "P20": ("place of death", "Entity 2 is the place (city, town, region or country) where entity 1, a person, died."),
    "P22": ("father", "Entity 2 is the father of entity 1."),
    "P25": ("mother", "Entity 2 is the mother of entity 1."),
    "P26": ("spouse", "Entity 1 and entity 2 are or were married to each other (husband or wife); engagement or an unmarried partnership does not count."),
    "P27": ("country of citizenship", "Entity 2 is a country of which entity 1, a person, is or was a citizen or national, stated directly or through a nationality word such as 'a Swedish singer'."),
    "P30": ("continent", "Entity 2 is the continent on which entity 1 (a place, country or region) is located."),
    "P31": ("instance of", "Entity 1 is a particular individual example of the class or kind named by entity 2 (e.g. a specific ceremony is an instance of an award ceremony series)."),
    "P35": ("head of state", "Entity 2 is the head of state (president, monarch, emperor or similar) of entity 1, a country or state."),
    "P36": ("capital", "Entity 2 is the capital city or seat of government of entity 1 (a country, state, province or region)."),
    "P37": ("official language", "Entity 2 is an official language of entity 1 (a country, region or organisation)."),
    "P39": ("position held", "Entity 2 is a political, religious, military or other office that entity 1, a person, holds or held."),
    "P40": ("child", "Entity 2 is a son or daughter of entity 1."),
    "P50": ("author", "Entity 2 is the writer or author of entity 1, a written work such as a book, story, article, poem or comic."),
    "P54": ("member of sports team", "Entity 1, an athlete or player, plays or played for entity 2, a sports team or club."),
    "P57": ("director", "Entity 2 directed entity 1 (a film, TV episode, play, music video or video game)."),
    "P58": ("screenwriter", "Entity 2 wrote the screenplay or script of entity 1 (a film, TV series or episode)."),
    "P69": ("educated at", "Entity 1 studied at or graduated from entity 2, a school, college, university or other educational institution."),
    "P86": ("composer", "Entity 2 composed the music of entity 1 (a song, opera, film score or other musical work)."),
    "P102": ("member of political party", "Entity 1 is or was a member of entity 2, a political party."),
    "P108": ("employer", "Entity 1 works or worked for entity 2 (a company, university, agency, newspaper or other organisation) as an employee."),
    "P112": ("founded by", "Entity 2 founded or co-founded entity 1 (an organisation, company, band, movement or settlement)."),
    "P118": ("league", "Entity 1, a sports team or player, competes or competed in entity 2, a sports league or division."),
    "P123": ("publisher", "Entity 2 is the company or organisation that published entity 1 (a book, comic, video game, periodical or other publication)."),
    "P127": ("owned by", "Entity 2 owns or owned entity 1 (a company, building, team, vehicle, brand or property)."),
    "P131": ("located in the administrative territorial entity", "Entity 1 lies within entity 2, an administrative division below country level, such as a city, county, district, state or province."),
    "P136": ("genre", "Entity 2 is the artistic or literary genre or style of entity 1 (a work, musician or band), e.g. synthpop, jazz, science fiction."),
    "P137": ("operator", "Entity 2 operates or runs entity 1 (a facility, vehicle, airport, stadium, service or installation)."),
    "P140": ("religion", "Entity 2 is the religion, church or religious denomination that entity 1 (a person, organisation or place) follows or belongs to."),
    "P150": ("contains administrative territorial entity", "Entity 2 is an administrative division (such as a state, province, county, district or city) that lies inside entity 1."),
    "P155": ("follows", "Entity 1 comes directly after entity 2 in a sequence or series (entity 2 is its immediate predecessor), e.g. the next album, episode or edition."),
    "P156": ("followed by", "Entity 1 comes directly before entity 2 in a sequence or series (entity 2 is its immediate successor), e.g. the next album, episode or edition."),
    "P159": ("headquarters location", "Entity 2 is the city or place where entity 1, an organisation or company, has its headquarters or main base."),
    "P161": ("cast member", "Entity 2 is an actor or performer who appears in entity 1 (a film, play, TV series or show)."),
    "P162": ("producer", "Entity 2 produced entity 1 (a film, album, song, record or TV show)."),
    "P166": ("award received", "Entity 1 received or won entity 2, an award, prize, medal or honour."),
    "P170": ("creator", "Entity 2 created entity 1 (an artwork, character, series, game or other work) in a general sense, when no more specific role such as author or director is meant."),
    "P171": ("parent taxon", "Entity 2 is the higher biological taxon (genus, family, order, ...) that entity 1, a taxon, belongs to."),
    "P172": ("ethnic group", "Entity 2 is an ethnic group that entity 1 (a person) belongs to, or that makes up the population of entity 1 (a place)."),
    "P175": ("performer", "Entity 2 is the singer, band, musician or actor who performs entity 1 (a song, album, role or show)."),
    "P176": ("manufacturer", "Entity 2 manufactures or manufactured entity 1 (a product, vehicle, aircraft, weapon or device)."),
    "P178": ("developer", "Entity 2 developed entity 1 (software, a video game, an operating system or a technology)."),
    "P179": ("series", "Entity 1 is one installment of entity 2, a series (book, film, TV, game or product series)."),
    "P190": ("sister city", "Entity 1 and entity 2 are twinned towns or sister cities with a formal partnership."),
    "P194": ("legislative body", "Entity 2 is the legislature (parliament, congress, assembly, council) of entity 1, a country, state or city."),
    "P205": ("basin country", "Entity 2 is a country in the drainage basin or shore area of entity 1, a lake, river or sea."),
    "P206": ("located in or next to body of water", "Entity 1 lies in, on or beside entity 2, a sea, lake, river, bay or other body of water."),
    "P241": ("military branch", "Entity 1 (a person or military unit) serves or served in entity 2, a branch of the armed forces such as an army, navy or air force."),
    "P264": ("record label", "Entity 2 is the record label that releases or released music by entity 1 (a musician, band or album)."),
    "P272": ("production company", "Entity 2 is a company that produced entity 1 (a film, TV series or show)."),
    "P276": ("location", "Entity 2 is the place where entity 1 (an event, object, collection or structure) is or took place, when no more specific location relation applies."),
    "P279": ("subclass of", "Entity 1 is a more specific kind of entity 2: every instance of entity 1 is also an instance of entity 2 (a class-to-class relation)."),
    "P355": ("subsidiary", "Entity 2 is a subsidiary company or subordinate organisation owned or controlled by entity 1."),
    "P361": ("part of", "Entity 1 is a part, component, section or member of entity 2 (e.g. a region of a larger area, an episode of a season, a musician in a band)."),
    "P364": ("original language of film or TV show", "Entity 2 is the language in which entity 1 (a film, TV show or other audiovisual work) was originally made."),
    "P400": ("platform", "Entity 2 is a platform (game console, operating system or computer system) on which entity 1, software or a video game, runs or was released."),
    "P403": ("mouth of the watercourse", "Entity 2 is the river, lake or sea into which entity 1, a river or stream, flows."),
    "P449": ("original network", "Entity 2 is the TV or radio network or channel that originally broadcast entity 1."),
    "P463": ("member of", "Entity 1 is a member of entity 2, an organisation, group, band, club, league or alliance."),
    "P488": ("chairperson", "Entity 2 is the chair, president or leader presiding over entity 1, an organisation."),
    "P495": ("country of origin", "Entity 2 is the country where entity 1 (a work, product, band, cuisine or tradition) comes from or was created."),
    "P527": ("has part", "Entity 2 is a part, component, section or member of entity 1 (the inverse of 'part of')."),
    "P551": ("residence", "Entity 2 is a place where entity 1, a person, lives or lived."),
    "P569": ("date of birth", "Entity 2 is the date or year on which entity 1, a person, was born."),
    "P570": ("date of death", "Entity 2 is the date or year on which entity 1, a person, died."),
    "P571": ("inception", "Entity 2 is the date or year when entity 1 (an organisation, place, band, work or object) was founded, established, formed or created."),
    "P576": ("dissolved, abolished or demolished", "Entity 2 is the date or year when entity 1 ceased to exist: it was dissolved, disbanded, abolished, closed or demolished."),
    "P577": ("publication date", "Entity 2 is the date or year when entity 1 (a book, song, album, film, game or other work) was first published or released."),
    "P580": ("start time", "Entity 2 is the date or year when entity 1 (an event, period, conflict, office term or state of affairs) began."),
    "P582": ("end time", "Entity 2 is the date or year when entity 1 (an event, period, conflict or state of affairs) ended."),
    "P585": ("point in time", "Entity 2 is the date or year at which entity 1, a single event or occurrence (e.g. an election or ceremony), took place."),
    "P607": ("conflict", "Entity 1 (a person, military unit or country) fought or served in entity 2, a war, battle or other armed conflict."),
    "P674": ("characters", "Entity 2 is a character who appears in entity 1 (a book, film, myth, game or other work)."),
    "P676": ("lyrics by", "Entity 2 wrote the lyrics (the words) of entity 1, a song or other musical work."),
    "P706": ("located on terrain feature", "Entity 1 is located on entity 2, a landform such as an island, peninsula, mountain range, valley or plain."),
    "P710": ("participant", "Entity 2 (a person, group, country or organisation) took part in entity 1, an event such as a war, battle, election or competition."),
    "P737": ("influenced by", "Entity 1 (a person, work or idea) was influenced by entity 2."),
    "P740": ("location of formation", "Entity 2 is the place where entity 1 (a band, group, company or organisation) was formed or founded."),
    "P749": ("parent organization", "Entity 2 is the parent organisation that owns or controls entity 1 (the inverse of 'subsidiary')."),
    "P800": ("notable work", "Entity 2 is a notable work (book, film, song, album, artwork or scientific work) created by or closely associated with entity 1."),
    "P807": ("separated from", "Entity 1 split off from or became independent of entity 2."),
    "P840": ("narrative location", "Entity 2 is the place where the story of entity 1 (a book, film, play or series) is set."),
    "P937": ("work location", "Entity 2 is a city, region or country where entity 1, a person, worked or was professionally active."),
    "P1001": ("applies to jurisdiction", "Entity 1 (an office, law, court, agency or institution) has authority in, applies to or operates for entity 2, a country, state or territory."),
    "P1056": ("product or material produced", "Entity 2 is a product, material or service that entity 1, a company or organisation, makes or produces."),
    "P1336": ("territory claimed by", "Entity 2 is a country or state that claims entity 1, a territory, as its own."),
    "P1344": ("participant of", "Entity 1 (a person, group, country or organisation) took part in entity 2, an event such as a war, battle, election or tournament."),
    "P1365": ("replaces", "Entity 1 replaced or superseded entity 2 (entity 2 was the earlier holder, office, body or thing that entity 1 took the place of)."),
    "P1366": ("replaced by", "Entity 1 was replaced or superseded by entity 2 (entity 2 is the later holder, office, body or thing that took its place)."),
    "P1376": ("capital of", "Entity 1 is the capital city or seat of government of entity 2 (a country, state, province or region)."),
    "P1412": ("languages spoken, written or signed", "Entity 2 is a language that entity 1, a person, speaks, writes, sings or signs."),
    "P1441": ("present in work", "Entity 1 (a character, person, creature or thing) appears in entity 2, a work such as a book, film, myth or game."),
    "P3373": ("sibling", "Entity 1 and entity 2 are siblings: brothers or sisters, including half-siblings."),
}
SYMMETRIC = {"P26", "P3373", "P190"}
INVERSE = {"P361": "P527", "P527": "P361", "P36": "P1376", "P1376": "P36", "P155": "P156", "P156": "P155",
           "P131": "P150", "P150": "P131", "P355": "P749", "P749": "P355", "P1365": "P1366", "P1366": "P1365",
           "P710": "P1344", "P1344": "P710", "P22": "P40", "P25": "P40", "P40": "P22", "P50": "P800",
           "P674": "P1441", "P1441": "P674", "P112": "P800"}
# relations that can be true together with the key relation even when the corpus annotated only one of them
IMPLIED = [("P36", "P150"), ("P1376", "P131"), ("P1376", "P17"), ("P36", "P17"), ("P131", "P17"), ("P150", "P17"),
           ("P361", "P463"), ("P527", "P463"), ("P361", "P30"), ("P361", "P131"), ("P361", "P706"),
           ("P361", "P179"), ("P527", "P150"), ("P710", "P1344"), ("P607", "P1344"), ("P607", "P710"),
           ("P50", "P170"), ("P57", "P170"), ("P58", "P170"), ("P86", "P170"), ("P162", "P170"), ("P175", "P170"),
           ("P86", "P676"), ("P86", "P175"), ("P676", "P175"), ("P162", "P175"), ("P57", "P58"), ("P57", "P162"),
           ("P58", "P162"), ("P161", "P175"), ("P178", "P123"), ("P178", "P176"), ("P123", "P127"),
           ("P127", "P749"), ("P127", "P137"), ("P749", "P137"), ("P112", "P127"), ("P112", "P488"),
           ("P108", "P463"), ("P108", "P69"), ("P108", "P937"), ("P108", "P1001"), ("P463", "P102"),
           ("P463", "P54"), ("P463", "P118"), ("P54", "P118"), ("P241", "P463"), ("P241", "P108"),
           ("P19", "P551"), ("P20", "P551"), ("P19", "P937"), ("P20", "P937"), ("P551", "P937"), ("P19", "P20"),
           ("P27", "P551"), ("P27", "P937"), ("P27", "P1001"), ("P27", "P172"), ("P27", "P1412"),
           ("P276", "P131"), ("P276", "P17"), ("P276", "P706"), ("P276", "P206"), ("P276", "P840"),
           ("P159", "P131"), ("P159", "P17"), ("P159", "P740"), ("P159", "P276"), ("P740", "P131"), ("P740", "P17"),
           ("P495", "P17"), ("P205", "P17"), ("P206", "P706"), ("P403", "P206"), ("P1001", "P17"),
           ("P1001", "P131"), ("P155", "P1365"), ("P156", "P1366"), ("P571", "P577"), ("P571", "P580"),
           ("P577", "P580"), ("P580", "P585"), ("P582", "P585"), ("P571", "P585"), ("P576", "P582"),
           ("P31", "P279"), ("P31", "P361"), ("P279", "P361"), ("P140", "P279"), ("P6", "P35"), ("P35", "P39"),
           ("P6", "P39"), ("P488", "P39"), ("P800", "P1441"), ("P172", "P1412"), ("P37", "P1412"),
           ("P37", "P172"), ("P364", "P495"), ("P364", "P37"), ("P1336", "P131"), ("P1336", "P17"),
           ("P807", "P361"), ("P807", "P1365"), ("P1056", "P176"), ("P1056", "P178"), ("P272", "P162"),
           ("P272", "P449"), ("P449", "P127"), ("P264", "P127"), ("P136", "P279"), ("P166", "P1344"), ("P54", "P108"),
           ("P737", "P1441"), ("P674", "P527"), ("P1441", "P361"), ("P40", "P3373"), ("P22", "P26"), ("P25", "P26")]
# reverse-pair relation -> relations it makes true for (entity 1 -> entity 2)
REV_IMPLIES = {"P40": {"P22", "P25"}, "P22": {"P40"}, "P25": {"P40"}, "P361": {"P527"}, "P527": {"P361", "P463"},
               "P463": {"P527"}, "P36": {"P1376", "P131"}, "P1376": {"P36", "P150"}, "P150": {"P131"},
               "P131": {"P150", "P36"}, "P155": {"P156"}, "P156": {"P155"}, "P355": {"P749", "P127"},
               "P749": {"P355"}, "P127": {"P355"}, "P1365": {"P1366"}, "P1366": {"P1365"}, "P710": {"P1344", "P607"},
               "P1344": {"P710"}, "P607": {"P710"}, "P674": {"P1441"}, "P1441": {"P674"}, "P800": {"P50", "P170", "P86", "P57", "P175"},
               "P50": {"P800"}, "P170": {"P800"}, "P86": {"P800"}, "P57": {"P800"}, "P175": {"P800"}, "P112": {"P800"},
               "P6": {"P39"}, "P35": {"P39"}, "P488": {"P39"}}
TEMPORAL = {"P569", "P570", "P571", "P576", "P577", "P580", "P582", "P585"}
Q = ('Which relation from entity 1 ("{h}", marked <e1>) to entity 2 ("{t}", marked <e2>) does the passage state? '
     'Read each option as entity 1 -> entity 2.')


def exclusion_graph(docs):
    cnt, co = collections.Counter(), collections.Counter()
    for doc in docs:
        g = collections.defaultdict(set)
        for l in doc["labels"]:
            g[(l["h"], l["t"])].add(l["r"])
        for rs in g.values():
            for r in rs:
                cnt[r] += 1
            for a, b in itertools.permutations(rs, 2):
                co[(a, b)] += 1
    excl = collections.defaultdict(set)
    for (a, b), c in co.items():
        if c / cnt[a] >= 0.01 or c / cnt[b] >= 0.01:
            excl[a].add(b)
            excl[b].add(a)
    for a, b in IMPLIED:
        excl[a].add(b)
        excl[b].add(a)
    return excl


def main():
    rng = random.Random(C.SEED)
    path = C.fetch(URL, C.CACHE / KEY / "train_revised.json", SHA)
    docs = json.loads(path.read_text())  # TRAIN ONLY
    assert len(docs) == 3053
    rels_seen = {l["r"] for d in docs for l in d["labels"]}
    assert rels_seen - {"P1198"} <= set(REL), rels_seen - set(REL)
    assert len({v[0] for v in REL.values()} | {NONE}) == len(REL) + 1

    excl = exclusion_graph(docs)
    # type signatures
    sig = collections.defaultdict(collections.Counter)
    rsig = collections.defaultdict(collections.Counter)  # relation -> (head type, tail type) counts
    for doc in docs:
        V = doc["vertexSet"]
        for l in doc["labels"]:
            sig[(V[l["h"]][0]["type"], V[l["t"]][0]["type"])][l["r"]] += 1
            rsig[l["r"]][(V[l["h"]][0]["type"], V[l["t"]][0]["type"])] += 1

    # ---- sentence-level decontamination (FewRel / Few-NERD / label-NLI / local files / other v14 parts)
    sent_text = {}
    for di, doc in enumerate(docs):
        for si, s in enumerate(doc["sents"]):
            sent_text[f"{di}:{si}"] = C.detok(s)
    core = {k: [v] for k, v in sent_text.items()}
    ohs3 = C.ohs3_wiki_texts()
    hits = C.decon(core, KEY, extra_texts=ohs3)
    hits.update(C.cross_v14(core, {KEY}))
    bad = set(hits)
    print("bad sentences:", len(bad), dict(collections.Counter(v.split(":")[0] for v in hits.values())))

    # ---- candidates
    cands = collections.defaultdict(list)
    stats = collections.Counter()
    for di, doc in enumerate(docs):
        V = doc["vertexSet"]
        pair_rels = collections.defaultdict(set)
        for l in doc["labels"]:
            pair_rels[(l["h"], l["t"])].add(l["r"])
            if l["r"] in SYMMETRIC:
                pair_rels[(l["t"], l["h"])].add(l["r"])
        for l in doc["labels"]:
            r, h, t = l["r"], l["h"], l["t"]
            if r == "P1198" or not l.get("evidence"):
                stats["no_evidence"] += 1
                continue
            ht, tt = V[h][0]["type"], V[t][0]["type"]
            if r == "P1001" and ht == "PER":
                stats["p1001_person"] += 1
                continue
            if r in ("P131", "P205") and "P17" in pair_rels[(h, t)]:
                # Re-DocRED also tags country tails with P131 (and P205 on non-water heads such as provinces); such
                # pairs are asked as 'country' (P17) only
                stats["p131_p205_country_tail"] += 1
                continue
            if rsig[r][(ht, tt)] / sum(rsig[r].values()) < 0.03:
                stats["rare_type_signature"] += 1   # type-implausible annotation (review fix)
                continue
            ev = sorted(set(l["evidence"]))
            lo, hi = ev[0], ev[-1]
            hs = {m["sent_id"] for m in V[h]}
            ts = {m["sent_id"] for m in V[t]}
            if not any(lo <= s <= hi for s in hs) or not any(lo <= s <= hi for s in ts):
                # extend to the nearest mentions if the evidence window misses one entity
                need = [min(hs, key=lambda s: (0 if lo <= s <= hi else min(abs(s - lo), abs(s - hi)))),
                        min(ts, key=lambda s: (0 if lo <= s <= hi else min(abs(s - lo), abs(s - hi))))]
                lo, hi = min([lo] + need), max([hi] + need)
            if hi - lo + 1 > MAX_WIN:
                stats["window_too_long"] += 1
                continue
            win = list(range(lo, hi + 1))
            if any(f"{di}:{s}" in bad for s in win):
                stats["decon"] += 1
                continue
            # mention spans inside the window, no overlap between head and tail spans
            spans = []
            for m in V[h]:
                if lo <= m["sent_id"] <= hi:
                    spans.append((m["sent_id"], m["pos"][0], m["pos"][1], "e1"))
            for m in V[t]:
                if lo <= m["sent_id"] <= hi:
                    spans.append((m["sent_id"], m["pos"][0], m["pos"][1], "e2"))
            spans = sorted(set(spans))
            clash = False
            for a, b in zip(spans, spans[1:]):
                if a[0] == b[0] and b[1] < a[2]:
                    clash = True
            if clash:
                stats["mention_overlap"] += 1
                continue
            cands[r].append({"di": di, "h": h, "t": t, "r": r, "win": win, "spans": spans, "ev": ev,
                             "pair": sorted(pair_rels[(h, t)]), "rev": sorted(pair_rels[(t, h)]), "ht": ht, "tt": tt})
    print("candidate triples:", sum(len(v) for v in cands.values()), dict(stats))

    # ---- selection: round-robin over relations (rarest first), windows never overlap inside a document
    for r in sorted(cands):
        cands[r].sort(key=lambda c: (c["di"], c["h"], c["t"]))
        rng.shuffle(cands[r])
    used = collections.defaultdict(set)
    picked = []
    per_rel = collections.Counter()
    ptr = {r: 0 for r in cands}
    order = sorted(cands, key=lambda r: (len(cands[r]), r))
    while len(picked) < TARGET:
        progressed = False
        for r in order:
            if len(picked) >= TARGET or per_rel[r] >= CAP_PER_REL:
                continue
            while ptr[r] < len(cands[r]):
                c = cands[r][ptr[r]]
                ptr[r] += 1
                if used[c["di"]] & set(c["win"]):
                    continue
                used[c["di"]] |= set(c["win"])
                picked.append(c)
                per_rel[r] += 1
                progressed = True
                break
        if not progressed:
            break
    print("picked:", len(picked), "relations:", len(per_rel))

    # ---- rows
    none_ids = set()
    by_rel = collections.defaultdict(list)
    for i, c in enumerate(picked):
        by_rel[c["r"]].append(i)
    n_none = int(round(NONE_SHARE * len(picked)))
    pool = [i for r in sorted(by_rel) for i in by_rel[r] if per_rel[r] >= 20]
    rng.shuffle(pool)
    none_ids = set(pool[:n_none])

    nd = C.NearDup(thr=0.7)
    rows = []
    for i, c in enumerate(picked):
        doc = docs[c["di"]]
        V = doc["vertexSet"]
        # build marked text
        marks = collections.defaultdict(list)
        for sid, a, b, tag in c["spans"]:
            marks[(sid, a)].append(f"<{tag}>")
            marks[(sid, b - 1, "end")].append(f"</{tag}>")
        sents = []
        for sid in c["win"]:
            toks = list(doc["sents"][sid])
            for j in range(len(toks)):
                pre = "".join(marks.get((sid, j), []))
                post = "".join(marks.get((sid, j, "end"), []))
                toks[j] = pre + toks[j] + post
            sents.append(C.detok(toks))
        state = " ".join(sents)
        plain = C.strip_markers(state)
        if nd.seen(plain):
            continue
        # display names: first marked mention of each entity in the window
        def first(tag):
            for sid, a, b, tg in c["spans"]:
                if tg == tag:
                    return C.detok(doc["sents"][sid][a:b])
        hname, tname = first("e1"), first("e2")
        is_none = i in none_ids
        forbid = set(c["pair"])
        for pr in c["pair"]:
            forbid |= excl[pr]
        for pr in c["rev"]:  # what the reverse pair (entity 2 -> entity 1) implies for this direction
            forbid |= REV_IMPLIES.get(pr, set())
            if pr in SYMMETRIC:
                forbid.add(pr)
        compat = [r for r, n in sig[(c["ht"], c["tt"])].most_common() if n >= 5 and r in REL]
        compat = [r for r in compat if r not in forbid and r != "P1198" and not (r == "P1001" and c["ht"] == "PER")]
        if len(compat) < 3:
            extra = collections.Counter()
            for (a, b), cc in sig.items():
                if a == c["ht"]:
                    extra.update(cc)
            compat += [r for r, n in extra.most_common() if n >= 5 and r in REL and r not in forbid and r not in compat
                       and r != "P1198" and not (r == "P1001" and c["ht"] == "PER")]
        k = rng.randint(4, 9) if not is_none else rng.randint(5, 9)
        dis = []
        inv = INVERSE.get(c["r"])
        if inv and inv in compat:
            dis.append(inv)
        head = compat[:12]
        rng.shuffle(head)
        for r in head + compat[12:]:
            if len(dis) >= k:
                break
            if r not in dis:
                dis.append(r)
        if len(dis) < 2:
            continue
        opts = ([] if is_none else [c["r"]]) + dis
        rng.shuffle(opts)
        options = [REL[r][0] for r in opts] + [NONE]
        gold = NONE if is_none else REL[c["r"]][0]
        # edges
        tags = []
        same_sent = any(sa == sb for sa, _, _, ta in c["spans"] if ta == "e1" for sb, _, _, tb in c["spans"] if tb == "e2")
        if len(c["ev"]) >= 2 and not same_sent:
            tags.append("multi_hop")
        if c["r"] in TEMPORAL:
            tags.append("temporal")
        if c["tt"] == "NUM":
            tags.append("numeric")
        if is_none:
            tags.append("missing_info")
        if len(c["win"]) >= 4 or len(plain) > 900:
            tags.append("long_context")
        if C.NEG.search(plain):
            tags.append("negation")
        rows.append({
            "key": KEY,
            "rid": f"{c['di']}:{c['h']}-{c['t']}:{c['r']}",
            "state": state,
            "instructions": Q.format(h=hname, t=tname),
            "options": options,
            "gold": gold,
            "soft": None,
            "meta": {"dataset": DATASET, "config": f"doc={doc['title']}; sentences {c['win'][0]}-{c['win'][-1]}"
                     + ("; gold relation removed from the options (none row)" if is_none else ""),
                     "revision": f"git:{COMMIT}; sha256:{SHA}", "licence": LICENCE, "split": "train",
                     "orig_label": {"relation": c["r"], "relation_name": REL[c["r"]][0], "pair_relations": c["pair"],
                                    "evidence": c["ev"], "head_type": c["ht"], "tail_type": c["tt"]},
                     "family": C.FAMILY, "edge": C.edge_join(tags)},
        })
    # review fix: re-check each finished window as a whole (10-word runs that cross a sentence boundary)
    wcore = {r["rid"]: [C.strip_markers(r["state"])] for r in rows}
    whits = C.decon(wcore, KEY + "_windows", extra_texts=ohs3)
    whits.update(C.cross_v14(wcore, {KEY}))
    print("window-level overlaps dropped:", len(whits), dict(collections.Counter(v.split(":")[0] for v in whits.values())))
    rows = [r for r in rows if r["rid"] not in whits]
    rng.shuffle(rows)
    defs = {v[0]: v[1] for v in REL.values()}
    defs[NONE] = ("The passage states none of the other listed relations from entity 1 to entity 2: the pair may be "
                  "related in a way that is not listed, only in the reverse direction, or not at all.")
    C.write_outputs(KEY, rows, {None: defs})
    st = C.summary(KEY, rows)
    C.show_samples(rows, 5)
    notes = ("Re-DocRED train (Wikipedia leads; DocRED human mentions + triples, human-revised). Relation "
             "classification: 1-4 sentence window covering the DocRED evidence, all head/tail mentions marked "
             "<e1>/<e2>; options = gold + 4-9 type-compatible relations never co-annotated with it (inverse relation "
             f"always offered when compatible) + 'none of the listed relations'; ~{int(NONE_SHARE * 100)}% none rows "
             "with the pair's relations removed. Only evidence-bearing triples; windows never overlap inside a "
             f"document; max {CAP_PER_REL} rows per relation; sentences overlapping FewRel/Few-NERD (OHS-3), "
             "label-NLI, local files or other v14 parts dropped."
             " Review fixes: whole windows re-checked for overlaps; P205 pairs with P17 asked as country; triples with a rare (<3%) type signature dropped; team never offered as employer.")
    C.append_manifest(C.manifest_record(KEY, DATASET, LICENCE, rows, "choice (relation type, 4-11 options)", notes, st))


if __name__ == "__main__":
    main()
