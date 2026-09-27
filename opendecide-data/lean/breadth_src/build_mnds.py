"""Build raw rows for breadth set "mnds" (MN-DS: Multilabeled News Dataset, IPTC Media Topics).

Source   : MN-DS, Petukhova & Fachada, Zenodo record 7394851 (MN-DS-news-classification.csv, 10,917 articles).
           Rows are read from the byte-for-byte HF mirror textminr/mn-ds @ 8b7463539dfa6093998523f7f9fb0b1ea0b867e6
           (train.jsonl, sha256 pinned below; the Zenodo CSV download was too slow to snapshot). Raw snapshot:
           breadth_src/cache/mnds/ (hf_train.jsonl, hf_README.md, zenodo_7394851.json, LICENSE_DATA.txt,
           iptc_mediatopic.json).
Split    : MN-DS has no official split (the paper's validation re-splits at random), so the whole release counts as
           train; the mirror publishes it as its only split, "train".
Licence  : CC BY 4.0. Zenodo record 7394851 metadata ("license": cc-by-4.0) and the record description ("made
           available under a CC-BY 4.0 license (see LICENSE_DATA.txt)"); LICENSE_DATA.txt states CC BY 4.0 (its first
           line names another dataset of the same author, a copy-paste slip; the licence itself is unambiguous).
           The HF mirror card only says "license: cc", so the Zenodo record is the licence of record.
Provenance: human-written news articles from 2019 (NELA-GT-2019 collection: ~215 outlets); category labels were
           assigned manually by the authors ("We manually labelled the articles", Zenodo description) on the IPTC
           NewsCodes Media Topic taxonomy: 17 level-1 and 109 level-2 categories. No model-written text or labels.
           NELA-GT-2019 is not in ohs3/used_sources.json (checked 27 Sep 2026).

Rows (<= 650, one per source article):
- ~340 "level1" rows: 17-way choice over the level-1 topics, round-robin over level-1 labels (20 each), rotating
  over the level-2 children inside each level-1 label so every subtopic is represented.
- ~310 "level2" rows: choice among the level-2 subtopics of the article's own level-1 parent (3-11 options),
  round-robin over all 109 level-2 labels.
State    : "<title>\\n\\n<content>" verbatim (HTML entities decoded); only articles whose full text fits 15-4,000 chars (content >= 200 chars)
           are eligible, so nothing is truncated.
Filters  : duplicate article ids/texts dropped (all copies dropped if their labels disagree); 13-gram + exact-text
           decontamination against every non-held-out jsonl under lean/ and ../data plus JevBench public (never
           ohs*/preds*/results*); dedup vs NewsMTSC (train.jsonl sentences) and News Headlines Sarcasm (train.json
           headlines): article dropped when it contains one of their sentences/headlines (>= 6 words) or its title
           equals one; no two selected articles share a 13-word run. Deterministic, seed 20261101.

  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python breadth_src/build_mnds.py
"""
import collections
import hashlib
import html
import json
import random
import re
import shutil
import statistics
import urllib.request
from pathlib import Path

KEY = "mnds"
SEED = 20261101
MAX_ROWS = 650
N_L1_PER_LABEL = 20                   # 17 x 20 = 340 level-1 rows; the rest are level-2 rows
LEN_RANGE = (15, 4000)
MIN_CONTENT = 200
GRAM = 13
SHORT_MIN = 6                          # min words for sentence/headline containment dedup

HERE = Path(__file__).resolve().parent
LEAN = HERE.parent
ROOT = LEAN.parent
JEV = ROOT.parent
CACHE = HERE / "cache" / KEY
OUT = LEAN / "data" / "v13_parts" / "raw" / f"{KEY}.jsonl"
DEFS_OUT = LEAN / "data" / "v13_parts" / "defs" / f"{KEY}.json"

HF_REPO = "textminr/mn-ds"
HF_REV = "8b7463539dfa6093998523f7f9fb0b1ea0b867e6"
HF_SHA = "2ae98ca5f0ad117739b8c770d1ad5d6a8439ee085a3b7cc475c67c02a17aead6"
LICENCE = ("CC BY 4.0 (Zenodo record 7394851 metadata license=cc-by-4.0 and LICENSE_DATA.txt; "
           "rows via HF mirror textminr/mn-ds)")
DATASET = "MN-DS (Zenodo 7394851, MN-DS-news-classification.csv; HF mirror textminr/mn-ds)"

Q_L1 = "Which IPTC Media Topic best describes the main subject of this news article?"
Q_L2 = 'Which "{}" subtopic best describes the main subject of this news article?'

# Definitions written from the official IPTC Media Topic definitions (cv.iptc.org, CC BY 4.0; snapshot
# cache/mnds/iptc_mediatopic.json) and their narrower concepts, under the names MN-DS uses.
DEF_L1 = {
    "arts, culture, entertainment and media": "All forms of arts and entertainment, cultural heritage, customs and traditions, and the news media, broadcasting and publishing.",
    "conflict, war and peace": "Politically or socially motivated violence and protest, military activity, wars, terrorism and geopolitical conflicts, as well as efforts to resolve them and rebuild afterwards.",
    "crime, law and justice": "Rules of behaviour in society and their enforcement: crimes and offenders, police, courts and trials, punishment, legislation and the bodies that administer justice.",
    "disaster, accident and emergency incident": "Natural or man-made events causing death, injury or damage to property, such as accidents, fires and natural catastrophes, and the planning and response to such emergencies.",
    "economy, business and finance": "The planning, production and exchange of wealth: national and regional economies, companies and industries, markets, trade, prices and financial matters.",
    "education": "All aspects of furthering knowledge, formally or informally: schools, teaching and learning, vocational training, religious instruction and parents' groups supporting education.",
    "environment": "The protection, damage and condition of the Earth's ecosystem: climate change, pollution, conservation, natural resources, nature and environmental policy.",
    "health": "All aspects of physical and mental well-being: diseases, treatments, hospitals and clinics, medical professions, health organisations, healthcare policy and animal or plant diseases.",
    "human interest": "Stories told mainly for their emotional or personal appeal about individuals, groups, animals or plants, including achievements, anniversaries and ceremonies.",
    "labour": "Social aspects, rules and conditions of paid work: jobs, employment law, the labour market, worker-employer relations, unions, unemployment and retirement.",
    "lifestyle and leisure": "Activities done for pleasure, relaxation or recreation outside paid work, such as hobbies, travel, eating out, fashion, personal fitness and ways of living.",
    "politics": "The exercise of power locally, nationally and internationally: governments, elections, political parties and processes, government policy, diplomacy, rights and political dissent.",
    "religion and belief": "Belief systems and faiths, religious institutions, leaders, texts, places of worship and events, and relations between religions and between religion and the state.",
    "science and technology": "Human understanding and methodical study of the natural, formal and social sciences, scientific research and institutions, and the practice of technology and engineering.",
    "society": "Concerns, issues and institutions of human social life, such as family, communities, demographics, migration, discrimination, poverty, welfare, values and population groups.",
    "sport": "Competitive physical or mental activity: sports events and results, athletes, clubs and governing bodies, venues, transfers, doping and disciplinary matters, and the business of sport.",
    "weather": "The study, prediction and reporting of meteorological conditions: forecasts, notable weather events, warnings about severe weather and weather statistics.",
}
DEF_L2 = {
    # arts, culture, entertainment and media
    "arts and entertainment": "Creative and performing arts and entertainment, such as music, film, television shows, theatre, visual arts, literature and festivals.",
    "culture": "The ideas, customs, traditions, heritage and way of life of a particular group, nation or people, including cultural institutions and cultural debates.",
    "mass media": "Media addressing a large audience, such as newspapers, television, radio, online news and social media platforms, and the journalists and companies behind them.",
    # conflict, war and peace
    "act of terror": "Violence, usually causing casualties, intended to spread fear in a population for political, religious or ideological aims, such as terrorist bombings or shootings.",
    "armed conflict": "Fighting between opposing groups using weapons, including wars, insurgencies, military offensives and clashes, whether or not war has been formally declared.",
    "civil unrest": "Rallies, demonstrations, strikes, riots or other disturbances by a population, often protesting against a government's or organisation's policies or actions.",
    "coup d'etat": "The overthrow, or attempted overthrow, of an established government by an organised military or political group, usually by force or unconstitutional means.",
    "massacre": "The mass killing of many people, usually unarmed civilians, during hostilities or by an armed group, and its investigation or remembrance.",
    "peace process": "Organised efforts to end a war or conflict, such as ceasefires, peace talks, negotiations, mediation and peace agreements.",
    "post-war reconstruction": "Efforts to rebuild the society, economy, infrastructure or political system of an area after a war or armed conflict.",
    "prisoners of war": "People captured, imprisoned or detained by an enemy side during a military conflict or war, including their treatment, exchange or release.",
    # crime, law and justice
    "crime": "Violations of law by individuals, companies or organisations, such as murder, theft, fraud or assault, and the offences, suspects and victims involved.",
    "judiciary": "The system of courts of law: judges, trials, court rulings and appeals, and the organisation of and appointments to the courts.",
    "justice": "The equitable administration of laws, including punishment, prisons, sentencing, the rights of the accused and whether justice was served.",
    "law": "The codified rules of behaviour: legislation, statutes, constitutional and legal changes, regulations and debates about what the law says.",
    "law enforcement": "Police and other agencies that prevent crime or bring offenders to justice, including arrests, investigations, policing methods and police conduct.",
    # disaster, accident and emergency incident
    "accident and emergency incident": "Sudden unexpected events with harmful consequences, such as road, rail or air crashes, industrial accidents, explosions, fires or drownings.",
    "disaster": "A sudden, unplanned event causing great damage or loss of life, especially natural catastrophes such as earthquakes, floods, hurricanes or wildfires.",
    "emergency incident": "A sudden, unexpected event that requires immediate action to prevent serious consequences, such as a hazardous spill, building collapse or rescue situation.",
    "emergency planning": "Planning in advance for sudden, unplanned events, such as disaster preparedness plans, drills, evacuation plans and early-warning systems.",
    "emergency response": "The efforts of people and organisations to help victims during or right after a disaster or crisis, such as rescue, relief aid and recovery work.",
    # economy, business and finance
    "business information": "News about individual businesses such as companies, corporations or charities: their results, strategy, deals, products, executives and corporate events.",
    "economic sector": "A particular industry or branch of the economy, such as agriculture, energy, manufacturing, retail, transport or financial services, and developments within it.",
    "economy": "Production, consumption, distribution and trade affecting whole countries or regions, such as growth, inflation, recession, trade policy and economic indicators.",
    "market and exchange": "Markets for buying and selling stocks, bonds, currencies, commodities and other goods, including share prices, exchange rates and trading.",
    # education
    "parent organisation": "Groups of parents, such as parent-teacher associations, set up to support, fund or campaign on the educational activities of their children.",
    "religious education": "Instruction by a faith in its own principles and beliefs, such as Sunday school, religious schooling or preparation for religious rites.",
    "school": "Schools as buildings or institutions providing education, such as primary and secondary schools, their pupils, staff, funding, safety and administration.",
    "social learning": "Learning social skills and behaviours by observing and imitating others, including teaching about empathy, emotions and mental health.",
    "teaching and learning": "The process of education itself: curricula, teaching methods, teachers' work, exams, student achievement and how people learn.",
    "vocational education": "Education giving practical training for a particular occupation or trade, such as apprenticeships, technical colleges and career or skills training.",
    # environment
    "climate change": "Changes in the Earth's climate such as global warming, their causes and effects, greenhouse-gas emissions, and efforts or debates to reduce them.",
    "conservation": "Preserving the natural world, such as protecting wilderness areas, endangered species, wildlife habitats, forests and other flora and fauna.",
    "environmental politics": "Government programmes, laws and political debate about environmental issues, such as pollution rules, renewable-energy policy, conservation policy and green activism.",
    "environmental pollution": "Contamination of air, water, soil or other natural resources by harmful substances such as chemicals, plastics, waste or oil spills.",
    "natural resources": "Assets provided by nature without human intervention, such as water, forests, minerals, fossil fuels and land, and their use, extraction and management.",
    "nature": "The natural world itself, such as landscapes, wildlife, plants and natural phenomena, and people's experience of nature.",
    # health
    "diseases and conditions": "Illnesses and health conditions affecting people, such as infections, cancer, heart disease, mental illness or injuries, including outbreaks and their spread.",
    "health facility": "Places where health care is provided, such as hospitals, clinics, care homes and surgeries, including their capacity, staffing and conditions.",
    "health organisations": "Specific health organisations, such as professional medical associations, health charities, non-profits and international bodies like the World Health Organization.",
    "health treatment": "Remedies, therapies, medicines, tests, surgery and other procedures used to prevent, diagnose, manage or cure a health condition.",
    "healthcare policy": "Government programmes and policies on health care, such as health-care funding, insurance, drug policy, public-health measures and health-system reform.",
    "medical profession": "Doctors, nurses and other formally trained health workers, their training, working conditions, conduct and professional regulation.",
    "non-human diseases": "Harmful health conditions affecting animals, plants or microorganisms, such as livestock epidemics, animal-borne diseases or crop and tree diseases.",
    # human interest
    "accomplishment": "Achievements by individuals, groups or animals, such as records broken, awards, remarkable feats or winning a contest, told for their human appeal.",
    "animal": "Stories about animals, including pets, wildlife, insects and livestock, told for their emotional or curiosity value.",
    "anniversary": "The celebration or commemoration of a significant number of years since an event, or since a notable person's birth or death.",
    "ceremony": "Rituals and formal occasions, such as dedications, wreath layings, award ceremonies, royal occasions or the launching of a ship.",
    "people": "Stories about individuals or groups that focus on their personal lives and emotional side, such as celebrities, unusual lives or touching personal events.",
    "plant": "Stories about plants, including flowers, trees, shrubs and gardens, told for their curiosity or emotional appeal.",
    # labour
    "employment": "Having work, usually paid, for a company, organisation or person, including jobs, hiring, working conditions, wages and careers.",
    "employment legislation": "Laws and regulations governing employment, such as minimum wage, working-time, workplace safety and anti-discrimination rules for workers.",
    "labour market": "The supply of and demand for workers in an economy, such as job figures, labour shortages, wage trends and workforce statistics.",
    "labour relations": "The relationship between workers and employers, including collective bargaining, workplace disputes, strikes and negotiations.",
    "retirement": "The years after working life, including pensions, retirement age, retirement savings and the situation of retirees.",
    "unemployment": "Being available for work but without a job, including jobless rates, lay-offs and support for unemployed people.",
    "unions": "Trade unions and other workers' organisations that represent employees and seek better pay and conditions through collective bargaining.",
    # lifestyle and leisure
    "exercise and fitness": "Physical activity done to maintain or improve health and fitness or for enjoyment, such as gym workouts, running, yoga and training routines.",
    "leisure": "Activities done in spare time for pleasure and not competitively, such as hobbies, games, travel, holidays and outings.",
    "lifestyle": "The way a person lives, including their style, fashion, possessions, food and drink, home and personal habits.",
    # politics
    "election": "Choosing government representatives by popular vote: campaigns, candidates, polls, voting, results and electoral systems.",
    "fundamental rights": "Political, social, cultural and economic rights to which all people are entitled, such as free speech, privacy, freedom of assembly and human rights.",
    "government": "The systems, institutions and people that run a state or political entity, such as heads of government, cabinets, parliaments and ministries.",
    "government policy": "Plans and courses of action set out by a government to guide decisions, such as new policies, programmes, budgets and regulatory measures.",
    "international relations": "Relations between countries through diplomacy, negotiation, treaties, summits, sanctions and alliances.",
    "non-governmental organisation": "Groups outside government, such as charities, advocacy groups and NGOs, that lobby, demonstrate or campaign on issues like economics, environment or health.",
    "political crisis": "Political conflict that escalates to the point where governments might fall, such as constitutional stand-offs, impeachment battles or collapsing coalitions.",
    "political dissent": "Individuals or groups who oppose or speak out against a political authority, often at personal risk, including dissidents and political prisoners.",
    "political process": "How politics is conducted: political parties and movements, party leadership, legislative procedure and participation in the affairs of government.",
    # religion and belief
    "interreligious dialogue": "Communication, cooperation and meetings between different religions or faith communities, such as interfaith gatherings and joint declarations.",
    "religious belief": "Belief systems and faiths themselves, such as Christianity, Islam, Judaism, Hinduism or Buddhism, their doctrines, practices and followers.",
    "religious conflict": "Conflicts, tensions or violence arising from religious differences, between religious groups or between religious groups and others.",
    "religious event": "Religious events other than regular festivals or holidays, such as synods, pilgrimages, papal visits, canonisations or special services.",
    "religious facilities": "Places where religious rites are carried out, such as churches, mosques, temples, synagogues and shrines, including their building, damage or closure.",
    "religious institutions and state relations": "Relations between religion and government, such as religious-freedom laws, church taxation, religious symbols in public institutions and state control of religion.",
    "religious leader": "People with a ritual, legal or leading role in a religion, such as popes, bishops, imams, rabbis or clergy, and their actions or statements.",
    "religious text": "Texts regarded as holy or important by a religion, such as the Bible, Quran or Torah, including their interpretation, translation or discovery.",
    # science and technology
    "biomedical science": "The application of biology-based science to medicine, such as medical research, genetics, drug development, biotechnology and health monitoring.",
    "mathematics": "The study of number, structure, space and change, including fields such as algebra, geometry and statistics, and mathematical discoveries or mathematicians.",
    "natural science": "Sciences dealing with matter, energy and the physical world, such as physics, chemistry, biology, geology and astronomy, including space discoveries.",
    "scientific institution": "Institutions that carry out or govern scientific work, such as national academies, research institutes, laboratories, space agencies and scientific societies.",
    "scientific research": "Methodical scientific investigation to explain why things happen or to solve problems, such as studies, experiments, findings and research funding.",
    "scientific standards": "Nationally or internationally agreed rules governing scientific and technical work, such as measurement units, calibration standards and research-integrity rules.",
    "social sciences": "The study of human society, such as sociology, anthropology, psychology, economics, linguistics, history and archaeology.",
    "technology and engineering": "Applied science and engineering, such as computing, software, artificial intelligence, electronics, telecommunications, robotics and energy or transport technology.",
    # society
    "communities": "Groups of people actively sharing a common place, value or interest, and local community life, organisations and initiatives.",
    "demographics": "The study of human populations and their characteristics, such as population size, birth and death rates, ageing and census statistics.",
    "discrimination": "Unfair treatment of people because of their real or perceived group, such as race, sex, sexual orientation, religion, age or disability.",
    "emigration": "People leaving their country of residence to settle permanently elsewhere, including brain drain and emigrant communities abroad.",
    "family": "People related by blood or a legal bond, or who see themselves as a family, including marriage, parenting, children and family life.",
    "immigration": "The movement of people into another country, including migrants, refugees, asylum seekers, border policy and integration.",
    "mankind": "People as a whole and particular population groups, such as children, women, older people, people with disabilities, LGBT people or national minorities.",
    "social condition": "Circumstances affecting people's lives and welfare in society, such as poverty, homelessness, living standards and inequality.",
    "social problem": "Issues of wider societal concern that harm human welfare, such as addiction, abuse, bullying, prostitution, human trafficking or slavery.",
    "values": "Principles and standards of behaviour that guide people's lives and choices, such as ethics, morality, sexual behaviour and debates about death and dying.",
    "welfare": "Help for people in need of food, housing, health or other services, such as social security benefits, charity and social services.",
    # sport
    "bodybuilding": "Competitions where athletes pose to display muscles built through strenuous training, judged on symmetry, muscularity and conditioning, and bodybuilders' training.",
    "competition discipline": "Particular sports as practised in competition, such as football, tennis or athletics, and reports on matches, performances and athletes in them.",
    "disciplinary action in sport": "Fines, suspensions, bans and other penalties imposed by sports bodies or teams on players, coaches or clubs for misconduct.",
    "drug use in sport": "Drug use connected with sport, especially doping, anti-doping tests, violations and bans, as well as permitted medical use.",
    "sport event": "An organised event featuring one or more sports competitions, such as the Olympic Games, a World Cup or a championship tournament.",
    "sport industry": "The commercial side of sport, such as club finances, sponsorship, broadcasting rights, ticketing and sports-related business.",
    "sport organisation": "Bodies that govern or organise sport, such as international federations, national associations, leagues and Olympic committees, and their decisions.",
    "sport venue": "Stadiums, arenas, gymnasiums and other facilities where sports events take place, including their construction, naming and condition.",
    "transfer": "The movement of players or coaches between clubs or teams, including transfer deals, fees, signings, loans and contract negotiations.",
    # weather
    "weather forecast": "Short- or long-term predictions and reports of the upcoming weather for a region, such as daily forecasts and seasonal outlooks.",
    "weather phenomena": "Notable meteorological events and conditions, such as storms, heat waves, snow, tornadoes or droughts, reported or studied for their effects.",
    "weather statistic": "Numerical facts about the weather, such as temperatures, rainfall, pressure, humidity, river levels, tides or record-breaking measurements.",
    "weather warning": "Alerts issued to the public about severe or notable weather in their area, such as storm, flood, heat or snow warnings.",
}


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def fetch():
    CACHE.mkdir(parents=True, exist_ok=True)
    if not (CACHE / "hf_train.jsonl").exists():
        from huggingface_hub import hf_hub_download
        for f in ("train.jsonl", "README.md"):
            shutil.copy(hf_hub_download(HF_REPO, f, repo_type="dataset", revision=HF_REV), CACHE / f"hf_{f}")
    web = {"zenodo_7394851.json": "https://zenodo.org/api/records/7394851",
           "LICENSE_DATA.txt": "https://zenodo.org/api/records/7394851/files/LICENSE_DATA.txt/content",
           "iptc_mediatopic.json": "https://cv.iptc.org/newscodes/mediatopic/?lang=en-GB&format=json"}
    for name, url in web.items():
        if not (CACHE / name).exists():
            urllib.request.urlretrieve(url, CACHE / name)
    assert sha256(CACHE / "hf_train.jsonl") == HF_SHA, "hf_train.jsonl hash mismatch"


def words(t):
    return re.findall(r"[a-z0-9]+", t.lower())


def norm(t):
    return " ".join(words(t))


def grams(w, n=GRAM):
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


def load():
    drop = collections.Counter()
    recs = [json.loads(l) for l in open(CACHE / "hf_train.jsonl", encoding="utf-8") if l.strip()]
    n_src = len(recs)
    by_id = collections.defaultdict(list)
    for r in recs:
        by_id[r["data_id"]].append(r)
    arts, labels_of_text = {}, collections.defaultdict(set)
    for did in sorted(by_id):
        grp = by_id[did]
        labs = {(r["category_level_1"], r["category_level_2"]) for r in grp}
        if len(labs) > 1:
            drop["id with conflicting labels"] += len(grp)
            continue
        if len(grp) > 1:
            drop["duplicate id copies"] += len(grp) - 1
        r = grp[0]
        # decode leftover HTML entities (&apos; &#8217; ...) from the NELA scrape; the text is otherwise verbatim
        title = html.unescape(r.get("title") or "").strip()
        content = html.unescape(r.get("content") or "").strip()
        state = f"{title}\n\n{content}" if title else content
        a = {"rid": str(did), "title": title, "content": content, "state": state,
             "l1": r["category_level_1"], "l2": r["category_level_2"], "source": r.get("source"),
             "date": r.get("date"), "nela_id": r.get("id")}
        arts[a["rid"]] = a
        labels_of_text[norm(state)].add((a["l1"], a["l2"]))
    # same text under different ids: drop all if labels conflict, else keep the lowest id
    seen = set()
    for rid in sorted(arts, key=int):
        k = norm(arts[rid]["state"])
        if len(labels_of_text[k]) > 1:
            drop["same text, conflicting labels"] += 1
            del arts[rid]
        elif k in seen:
            drop["duplicate text"] += 1
            del arts[rid]
        else:
            seen.add(k)
    return arts, n_src, drop


def eligible(a):
    return (LEN_RANGE[0] <= len(a["state"]) <= LEN_RANGE[1] and len(a["content"]) >= MIN_CONTENT
            and norm(a["content"]) != norm(a["title"]))


def is_heldout(rel):
    return any(x.lower().startswith(("ohs", "preds", "results")) for x in rel.parts)


def scan_files():
    fs = set()
    for base in (LEAN, ROOT / "data"):
        for p in base.rglob("*.jsonl"):
            rel = p.relative_to(base)
            if is_heldout(rel) or "cache" in rel.parts or ".venv" in rel.parts or p.resolve() == OUT.resolve():
                continue
            fs.add(p)
    fs |= set((JEV / "bench/jevbench/datasets/public").glob("*.jsonl"))
    return sorted(fs)


def strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values():
            yield from strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from strings(v)


def decontaminate(arts):
    """13-word runs / exact text of our articles vs every non-held-out jsonl; returns {rid: first hit file}."""
    owner, exact = collections.defaultdict(set), collections.defaultdict(set)
    for a in arts.values():
        w = words(a["state"])
        exact[" ".join(w)].add(a["rid"])
        exact[" ".join(words(a["content"]))].add(a["rid"])
        for g in grams(w):
            owner[g].add(a["rid"])
    hit, seen, files = {}, set(), scan_files()
    for f in files:
        with open(f, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    x = json.loads(line)
                except Exception:  # noqa: BLE001
                    continue
                for t in strings(x):
                    if len(t) < 15:
                        continue
                    h = hash(t)
                    if h in seen:
                        continue
                    seen.add(h)
                    w = words(t)
                    for rid in exact.get(" ".join(w), ()):
                        hit.setdefault(rid, f.name)
                    for i in range(len(w) - GRAM + 1):
                        for rid in owner.get(" ".join(w[i:i + GRAM]), ()):
                            hit.setdefault(rid, f.name)
    return hit, len(files)


def news_dedup(arts):
    """Drop articles containing a NewsMTSC train sentence or a Sarcasm-headlines train headline (>= 6 words),
    or whose title equals one. Returns {rid: which set}."""
    refs = []
    p = HERE / "cache" / "newsmtsc" / "train.jsonl"
    if p.exists():
        refs += [("newsmtsc", json.loads(l)["sentence"]) for l in open(p, encoding="utf-8") if l.strip()]
    p = HERE / "cache" / "sarcasm_headlines" / "train.json"
    if p.exists():
        refs += [("sarcasm_headlines", json.loads(l)["headline"]) for l in open(p, encoding="utf-8") if l.strip()]
    for name in ("newsmtsc.jsonl", "sarcasm_headlines.jsonl"):
        p = OUT.parent / name
        if p.exists():
            refs += [(name[:-6], json.loads(l)["state"]) for l in open(p, encoding="utf-8") if l.strip()]
    short, long_ = collections.defaultdict(set), {}
    for src, t in refs:
        w = words(t)
        if len(w) < SHORT_MIN:
            continue
        if len(w) >= GRAM:
            for g in grams(w):
                long_.setdefault(g, src)
        short[len(w)].add((" ".join(w), src))
    short_idx = {n: {s: src for s, src in v} for n, v in short.items() if n < GRAM}
    titles = {s: src for n, v in short.items() for s, src in v}
    hit = {}
    for rid, a in arts.items():
        if norm(a["title"]) in titles:
            hit[rid] = titles[norm(a["title"])]
            continue
        w = words(a["state"])
        g = next((long_[x] for x in grams(w) if x in long_), None)
        if g:
            hit[rid] = g
            continue
        for n, idx in short_idx.items():
            m = next((idx[" ".join(w[i:i + n])] for i in range(len(w) - n + 1) if " ".join(w[i:i + n]) in idx), None)
            if m:
                hit[rid] = m
                break
    return hit, len(refs)


def row(a, level, options):
    q = Q_L1 if level == "level1" else Q_L2.format(a["l1"])
    gold = a["l1"] if level == "level1" else a["l2"]
    assert gold in options
    return {"key": KEY, "rid": a["rid"], "state": a["state"], "instructions": q, "options": options,
            "gold": gold, "soft": None,
            "meta": {"dataset": DATASET, "config": level if level == "level1" else f"level2:{a['l1']}",
                     "revision": f"{HF_REPO}@{HF_REV}", "licence": LICENCE, "split": "train",
                     "orig_label": f"{a['l1']} > {a['l2']}", "category_level_1": a["l1"],
                     "category_level_2": a["l2"], "outlet": a["source"], "date": a["date"],
                     "nela_id": a["nela_id"], "qtype": "choice"}}


def main():
    fetch()
    rng = random.Random(SEED)
    arts, n_src, drop = load()
    n_unique = len(arts)
    for rid in [r for r, a in arts.items() if not eligible(a)]:
        drop["length / empty body"] += 1
        del arts[rid]
    hit, n_files = decontaminate(arts)
    for rid in hit:
        arts.pop(rid, None)
    drop["13-gram/exact overlap with our files"] = len(hit)
    nh, n_refs = news_dedup(arts)
    for rid in nh:
        arts.pop(rid, None)
    drop["overlap with NewsMTSC / Sarcasm headlines"] = len(nh)
    print(f"source rows {n_src}; unique articles {n_unique}; pool {len(arts)}; drops {dict(drop)}")
    print(f"decontam: {n_files} files scanned; hit files {collections.Counter(hit.values()).most_common(6)}")
    print(f"news dedup: {n_refs} reference sentences/headlines; hits {collections.Counter(nh.values())}")

    children = collections.defaultdict(list)
    for a in arts.values():
        if a["l2"] not in children[a["l1"]]:
            children[a["l1"]].append(a["l2"])
    for l1 in children:
        children[l1].sort()
    L1 = sorted(children)
    assert set(L1) == set(DEF_L1), set(L1) ^ set(DEF_L1)
    assert set(DEF_L2) == {c for v in children.values() for c in v}, set(DEF_L2) ^ {c for v in children.values() for c in v}
    assert not set(DEF_L1) & set(DEF_L2)

    queues = collections.defaultdict(list)
    for rid in sorted(arts, key=int):
        queues[(arts[rid]["l1"], arts[rid]["l2"])].append(rid)
    for q in queues.values():
        rng.shuffle(q)

    used_grams, rows = set(), []

    def take(key):
        while queues[key]:
            a = arts[queues[key].pop(0)]
            g = grams(words(a["state"]))
            if g & used_grams:
                continue
            used_grams.update(g)
            return a
        return None

    # 1) level-1 rows: round-robin over level-1 labels, rotating over each label's children
    pos = {l1: 0 for l1 in L1}
    n_l1 = collections.Counter()
    active = set(L1)
    while active and sum(n_l1.values()) < N_L1_PER_LABEL * len(L1):
        for l1 in L1:
            if l1 not in active:
                continue
            if n_l1[l1] >= N_L1_PER_LABEL:
                active.discard(l1)
                continue
            a = None
            for _ in range(len(children[l1])):
                c = children[l1][pos[l1] % len(children[l1])]
                pos[l1] += 1
                a = take((l1, c))
                if a:
                    break
            if a is None:
                active.discard(l1)
                continue
            rows.append(row(a, "level1", L1))
            n_l1[l1] += 1

    # 2) level-2 rows: round-robin over all level-2 labels (shuffled order), options = siblings under the parent
    l2_keys = sorted(queues)
    rng.shuffle(l2_keys)
    active = [k for k in l2_keys]
    while active and len(rows) < MAX_ROWS:
        nxt = []
        for k in active:
            if len(rows) >= MAX_ROWS:
                break
            a = take(k)
            if a is None:
                continue
            rows.append(row(a, "level2", children[k[0]]))
            nxt.append(k)
        active = nxt

    order = list(range(len(rows)))
    rng.shuffle(order)
    rows = [rows[i] for i in order]

    defs = {**DEF_L1, **DEF_L2}
    for k, d in defs.items():
        assert 8 <= len(d.split()) <= 35, (k, len(d.split()))
    assert len({r["rid"] for r in rows}) == len(rows)
    assert len({norm(r["state"]) for r in rows}) == len(rows)
    assert all(LEN_RANGE[0] <= len(r["state"]) <= LEN_RANGE[1] for r in rows)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    DEFS_OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    DEFS_OUT.write_text(json.dumps(defs, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    # report
    lv = collections.Counter(r["meta"]["config"].split(":")[0] for r in rows)
    print(f"wrote {len(rows)} rows -> {OUT}  ({dict(lv)}); defs {len(defs)} -> {DEFS_OUT}")
    g1 = collections.Counter(r["gold"] for r in rows if r["meta"]["config"] == "level1")
    print("level1 gold counts:", dict(sorted(g1.items())))
    print(f"level1 max share: {max(g1.values()) / sum(g1.values()):.3f}")
    g2 = collections.Counter(r["gold"] for r in rows if r["meta"]["config"] != "level1")
    print(f"level2: {len(g2)} distinct gold labels, per-label min/max {min(g2.values())}/{max(g2.values())}")
    per_q = collections.defaultdict(collections.Counter)
    for r in rows:
        if r["meta"]["config"] != "level1":
            per_q[r["meta"]["config"]][r["gold"]] += 1
    worst = max(max(c.values()) / sum(c.values()) for c in per_q.values())
    print(f"level2 questions: {len(per_q)}; worst per-question max label share {worst:.3f}")
    allc = collections.Counter((r["meta"]["category_level_1"], r["meta"]["category_level_2"]) for r in rows)
    print(f"level-2 categories covered overall: {len(allc)}/109")
    print(f"soft-label coverage: 0/{len(rows)} (one manual label per article, no annotator counts)")
    L = sorted(len(r["state"]) for r in rows)
    print(f"state chars min/median/mean/max: {L[0]}/{L[len(L) // 2]}/{statistics.mean(L):.0f}/{L[-1]}")
    print("outlets:", len({r["meta"]["outlet"] for r in rows}), "top:",
          collections.Counter(r["meta"]["outlet"] for r in rows).most_common(5))


if __name__ == "__main__":
    main()
