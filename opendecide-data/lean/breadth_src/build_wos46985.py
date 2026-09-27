"""Build raw rows for Web of Science WOS-46985 (HDLTex) - paper abstract topic classification.

Source: Mendeley Data "Web of Science Dataset", doi:10.17632/9rw3vkcfy4.6 (version 6, published 2018-03-15),
        file WebOfScience.zip (sha256 b787d484...ccf8a) -> Meta-data/Data.xlsx
        (columns Y1, Y2, Y, Domain, area, keywords, Abstract; 46,985 records).
Licence: CC BY 4.0 - Mendeley Data record field data_licence ("Creative Commons Attribution 4.0 International",
        http://creativecommons.org/licenses/by/4.0), saved in cache/wos46985/dataset_meta.json; ReadMe.txt adds an
        MIT-style permission notice (Copyright (c) 2017 Kamran Kowsari). Cite HDLTex (Kowsari et al., ICMLA 2017).
Provenance: texts are author-written abstracts of published papers (Web of Science); labels are the Web of
        Science domain and the research-area keyword each paper was collected under (no model involved).
Split: the release has no official train/test split (HDLTex splits randomly); the whole Data.xlsx is the pool,
        recorded as split "train". The dataset is not in ohs3/used_sources.json (no held-out/dev/eval/JevBench use).
Snapshot: cache/wos46985/{WebOfScience.zip, ReadMe.txt, dataset_meta.json}; downloaded and sha256-checked if missing.

Design:
- state = Abstract only (never the keywords column). A trailing publisher copyright notice
  ("(C) 2016 Elsevier Ltd. All rights reserved.", "Copyright (c) 2016 John Wiley & Sons", "(C) 2016 American
  Society of Civil Engineers.") is removed because it leaks the publisher/field; everything else is verbatim.
- Two tasks, one row per source record (a record is used at most once):
  * domain (DOMAIN_N rows): 7-way Domain, label-balanced round-robin (so Medical and biochemistry, which are 31%
    and 12% of the source, are capped at 1/7 each); inside a domain, records are drawn round-robin over areas.
    Areas whose domain is ambiguous are not used for this task (Depression/Schizophrenia exist in both Medical and
    Psychology; Medical mental-health areas such as Anxiety or Stress Management read as psychology).
  * area (AREA_N rows): research area within the paper's (given) domain, options = all kept areas of that domain.
    Medical is left out of this task: its 53 area tags are consumer-health keywords with heavy overlap
    (Headache/Migraine, Dementia/Alzheimer's, Depression/Mental Health, Birth Control/Emergency Contraception).
    Gold = the normalised area string (the Y2 code merges unrelated areas, e.g. Analog signal processing +
    Electrical generator, so the area string is the finer, faithful label).
- Areas with fewer than MIN_AREA records are dropped (tiny/noisy tags such as "Structured Storage",
  "Underwater Windmill", "Nano Concrete", "Voltage law").
- Filters: 15-4000 chars after cleaning, must end at a sentence end (a few source abstracts are cut off),
  dedup on normalised text (records whose text repeats are dropped).
- Label confirmation (verifier fix): WOS areas are the search keywords the papers were retrieved with, so some
  records match a keyword in an unrelated sense (e.g. "Attention" papers on potentiometric sensors, "Electricity"
  papers on cacao life-cycle assessment). Only records whose AUTHORS list the area among their own keywords
  (kw_confirmed, with a few spelling variants in AREA_KW_SYN) are used, for both tasks; areas with fewer than
  MIN_CONF confirmed records are dropped.
- Area-name leakage: in the area task, records whose abstract does not contain the area name verbatim are
  preferred ~2:1, so the task is not mostly string matching.
- Copyright notice removal only fires on a real notice (year / publisher / "rights reserved" after the (c)),
  never on list markers such as "(c) MMAS-8 scores"; an opening "(" or "Crown" before the notice is removed too.
"""
import collections, hashlib, json, os, re, random, sys, urllib.request, zipfile

SEED = 20261101
N_MAX = 650
DOMAIN_N = 390
AREA_N = N_MAX - DOMAIN_N
MIN_AREA = 60
MIN_CONF = 20  # min records per area whose author keywords confirm the area
ZIP_URL = ("https://data.mendeley.com/public-files/datasets/9rw3vkcfy4/files/"
           "c9ea673d-5542-44c0-ab7b-f1311f7d61df/file_downloaded")
ZIP_SHA = "b787d484bff88b0dcdb3fa291d06ec9d2f025dc2a67ce1045d0c688cd96ccf8a"

HERE = os.path.dirname(os.path.abspath(__file__))
LEAN = os.path.dirname(HERE)
CACHE = os.path.join(HERE, "cache", "wos46985")
ZIP = os.path.join(CACHE, "WebOfScience.zip")
OUT = os.path.join(LEAN, "data", "v13_parts", "raw", "wos46985.jsonl")
DEFS_OUT = os.path.join(LEAN, "data", "v13_parts", "defs", "wos46985.json")

META_BASE = {"dataset": "Web of Science Dataset WOS-46985 (HDLTex, Kowsari et al. 2017)",
             "revision": "Mendeley Data doi:10.17632/9rw3vkcfy4.6, WebOfScience.zip sha256 " + ZIP_SHA,
             "licence": "CC BY 4.0 (Mendeley Data record data_licence; ReadMe.txt MIT-style notice, (c) 2017 Kamran Kowsari)",
             "split": "train"}

DOMAINS = {  # raw Domain (stripped) -> option name
    "CS": "Computer Science", "ECE": "Electrical Engineering", "Psychology": "Psychology",
    "MAE": "Mechanical Engineering", "Civil": "Civil Engineering", "Medical": "Medical Science",
    "biochemistry": "Biochemistry"}
DOMAIN_ORDER = ["Computer Science", "Electrical Engineering", "Mechanical Engineering", "Civil Engineering",
                "Medical Science", "Biochemistry", "Psychology"]
AREA_DOMAINS = ["CS", "ECE", "MAE", "Civil", "Psychology", "biochemistry"]  # Medical excluded from area task
DOMAIN_TASK_EXCLUDE = {  # (domain, area lower) not used for the 7-way domain task
    ("Medical", "depression"), ("Medical", "schizophrenia"), ("Psychology", "depression"),
    ("Psychology", "schizophrenia"), ("Medical", "anxiety"), ("Medical", "mental health"),
    ("Medical", "stress management"), ("Medical", "bipolar disorder"), ("Medical", "addiction"),
    ("Medical", "autism"), ("Medical", "parenting")}

# normalised display names for area strings (keys are lower-cased, whitespace-collapsed source strings)
AREA_NAME_FIX = {
    "network security": "Network security", "computer-aided design": "Computer-aided design",
    "materials engineering": "Materials engineering", "human metabolism": "Human metabolism",
    "ambient intelligence": "Ambient intelligence", "remote sensing": "Remote sensing",
    "rainwater harvesting": "Rainwater harvesting", "water pollution": "Water pollution",
    "suspension bridge": "Suspension bridge", "stealth technology": "Stealth technology",
    "green building": "Green building", "solar energy": "Solar energy",
    "construction management": "Construction management", "smart material": "Smart material",
    "pid controller": "PID controller", "dna/rna sequencing": "DNA/RNA sequencing",
}

DOMAIN_DEFS = {
    "Computer Science": "Research on computation and software: algorithms, data structures, programming, databases, networks and security, graphics, vision, machine learning and computing systems.",
    "Electrical Engineering": "Research on electricity and electronics: electric circuits and power networks, electricity supply, motors and generators, signal processing, control systems, amplifiers, microcontrollers and satellite radio.",
    "Mechanical Engineering": "Research on machines, mechanics and energy: machine design (including electric machines), CAD, manufacturing, fluid mechanics, hydraulics, thermodynamics, engines, engineering materials and strength of materials.",
    "Civil Engineering": "Research on infrastructure and the built environment: construction management, bridges, geotextiles and smart materials, water supply and pollution, green buildings, solar energy, remote sensing, smart environments and radar stealth materials.",
    "Medical Science": "Clinical and health research on human diseases and conditions: diagnosis, treatment, drugs, patient outcomes and public health for specific illnesses or health topics.",
    "Biochemistry": "Research on the molecules and processes of living cells: molecular and cell biology, genetics, enzymes, metabolism, immunology, and lab techniques such as PCR and blotting.",
    "Psychology": "Research on the human mind and behaviour: cognition, perception, social behaviour, development, personality and psychological disorders studied from a psychological perspective.",
}

AREA_DEFS = {
    # Computer Science
    "Computer vision": "Getting computers to interpret images or video: object detection and recognition, tracking, scene understanding, 3D reconstruction and visual pattern analysis.",
    "Machine learning": "Algorithms that learn from data: classification, regression, clustering, neural networks, kernel methods, and learning theory or training procedures.",
    "Network security": "Protecting computer networks and systems: intrusion detection, attacks and defences, malware, authentication, access control and secure communication protocols.",
    "Cryptography": "Mathematical techniques for securing information: encryption schemes, digital signatures, hash functions, key exchange, cryptanalysis and provable security.",
    "Operating systems": "Software that manages computer hardware and resources: scheduling, memory management, file systems, virtualization, kernels and system-level resource control.",
    "Computer graphics": "Generating and rendering images and shapes by computer: rendering, meshes, geometric modelling, animation, visualization and shading.",
    "Image processing": "Algorithms that operate on digital images as pixels: denoising, enhancement, segmentation, compression, filtering, restoration and feature extraction.",
    "Parallel computing": "Running computations simultaneously on many processors or cores: multicore and GPU programming, parallel algorithms, speedup and high-performance computing.",
    "Relational databases": "Storing and querying structured data in tables: SQL, query processing and optimization, schemas, transactions, indexing and database management systems.",
    "Software engineering": "Methods for building and maintaining software: requirements, design, testing, defects, maintenance, effort estimation, development processes and tools.",
    "Distributed computing": "Networked computers working together: cloud and grid computing, peer-to-peer systems, consensus, fault tolerance and distributed resource allocation.",
    "Symbolic computation": "Computer algebra: exact manipulation of mathematical expressions, symbolic or closed-form solutions of equations, polynomial systems and exact solutions of nonlinear differential equations.",
    "Algorithm design": "Designing and analysing algorithms: computational complexity, approximation, optimization and graph algorithms, heuristics, and proofs of efficiency or correctness.",
    "Computer programming": "Writing and reasoning about programs: programming languages, compilers, program analysis, code generation, and programming education or practices.",
    "Data structures": "Ways of organising data for efficient access and update: trees, graphs, hashing, indexes and queues, and their time and space trade-offs.",
    "Bioinformatics": "Computational methods for biological data: sequence and genome analysis, protein data, biological databases and software tools for molecular biology.",
    # Electrical Engineering
    "Electricity": "Electric power and energy as a resource: electricity generation (including renewables and fuel cells), grids, markets, pricing, consumption, and the costs or emissions of electricity use.",
    "Electrical circuits": "Design and analysis of electric circuits built from components such as resistors, capacitors, inductors and transistors, including circuit models and simulation.",
    "Digital control": "Control systems implemented with sampled, discrete-time signals on digital hardware: discrete controllers, sampled-data systems and networked control.",
    "System identification": "Building mathematical models of dynamic systems from measured input-output data: parameter estimation, model structure selection and identification algorithms.",
    "Electrical network": "Interconnected electrical components or power networks analysed as a whole: network topology, power flow, monitoring and reliability of power networks, and resistor networks studied as graphs.",
    "Microcontroller": "Small programmable computers embedded in devices: microcontroller-based designs, embedded systems, sensor interfacing and low-power control hardware.",
    "Analog signal processing": "Processing continuous-time signals with analog circuits: analog filters, mixers, oscillators, converters and analog front ends.",
    "Electrical generator": "Machines that convert mechanical energy into electrical energy: generators and alternators, including wind or hydro generators, and their design and control.",
    "Electric motor": "Machines that convert electrical energy into mechanical motion: motor design, drives, speed and torque control, and motor fault diagnosis.",
    "Satellite radio": "Radio communication through satellites: satellite links and broadcasting, antennas, channel modelling and satellite communication systems.",
    "Control engineering": "The control-engineering discipline in general: designing feedback systems that make dynamic systems behave as desired (stability, robust, adaptive, nonlinear control), automation, and control engineering education and laboratories.",
    "Signal-flow graph": "Graph representations of signal relations in a system: signal-flow graphs, Mason's gain rule and graph-based analysis of circuits or control loops.",
    "State space representation": "Modelling dynamic systems with state variables and first-order equations: state-space models, observers, controllability, observability and state estimation.",
    "PID controller": "Proportional-integral-derivative feedback controllers: PID tuning, PID-based control designs and their performance in industrial or physical systems.",
    "Operational amplifier": "Op-amp based circuits: amplifier design, op-amp configurations, integrators, comparators and analog circuits built around operational amplifiers.",
    # Mechanical Engineering
    "Computer-aided design": "Using software to design and model parts and products: CAD models, geometric and parametric design, design automation and computer-aided engineering tools.",
    "Hydraulics": "Flow of water and other liquids and its engineering: hydraulic systems, pumps and valves, pipe and channel flow, thermal-hydraulics of reactors, and water transport in plants.",
    "Manufacturing engineering": "Processes and systems for making products: machining, production planning, additive manufacturing, process optimization and manufacturing quality.",
    "Machine design": "Designing machines and their parts: mechanisms, gears, bearings, shafts, robotic handling devices and electrical machines such as motors, with their dynamics, reliability and optimization.",
    "Fluid mechanics": "Behaviour of liquids and gases in motion or at rest: flows, turbulence, boundary layers, transport phenomena and computational fluid dynamics.",
    "Internal combustion engine": "Engines that burn fuel inside a cylinder: combustion, emissions, fuels, and the performance and efficiency of diesel and gasoline engines.",
    "Thermodynamics": "Energy, heat and work in physical systems: thermodynamic cycles, entropy, heat transfer, refrigeration and energy-conversion efficiency.",
    "Materials engineering": "Engineering materials, their processing and properties: alloys, composites, ceramics, microstructure and material performance.",
    "Strength of materials": "How structural members respond to loads: stress, strain, deformation, fracture, fatigue and failure of beams, plates and components.",
    # Civil Engineering
    "Ambient intelligence": "Electronic environments that sense and respond to people: smart homes, sensor networks, context-aware and assisted-living systems.",
    "Geotextile": "Permeable fabrics used in soil and civil works: geotextiles and geosynthetics for reinforcement, filtration, drainage and erosion control.",
    "Remote sensing": "Observing the earth from satellites, aircraft or drones: image analysis, land-cover mapping and monitoring of the environment or structures.",
    "Rainwater harvesting": "Collecting and storing rainwater for use: rooftop and runoff harvesting systems, storage tanks, water supply and stormwater management.",
    "Water pollution": "Contamination of rivers, lakes, groundwater or seas: pollutants, water-quality assessment, pollution sources and wastewater treatment.",
    "Suspension bridge": "Bridges hung from cables between towers: cable and deck behaviour, wind and seismic response, and structural analysis of suspension and cable-supported bridges.",
    "Stealth technology": "Making objects hard to detect by radar or other sensors: radar-absorbing and shielding materials, radar cross-section reduction and low-observable design.",
    "Green building": "Environmentally sustainable buildings: energy-efficient building design, green certification, sustainable materials and building energy consumption.",
    "Solar energy": "Harnessing sunlight for power or heat: photovoltaic systems, solar thermal collectors, solar radiation and integration of solar energy.",
    "Construction management": "Planning and managing construction projects: scheduling, cost, safety, contracts, productivity and project delivery in the construction industry.",
    "Smart material": "Materials whose properties change in response to stimuli: shape-memory alloys, piezoelectric and self-sensing materials, and their structural uses.",
    # Psychology
    "Prejudice": "Negative attitudes and biases toward social groups: stereotypes, discrimination, racism, sexism and intergroup attitudes.",
    "Social cognition": "How people process and apply information about others and social situations: attributions, social judgments, theory of mind and social attitudes.",
    "Person perception": "How people form impressions of individuals: judging the traits, faces, trustworthiness, attractiveness or emotions of other people.",
    "Nonverbal communication": "Communication without words: facial expressions, gestures, gaze, body language, tone of voice and touch.",
    "Prosocial behavior": "Voluntary actions that benefit others: helping, cooperation, altruism, generosity, volunteering and empathy-driven behaviour.",
    "Leadership": "Leaders and leading in groups and organizations: leadership styles, leader effectiveness, followers and organizational outcomes.",
    "Eating disorders": "Disordered eating and related conditions: anorexia, bulimia, binge eating, body-image concerns and their treatment.",
    "Depression": "Depressive disorder and depressive symptoms: low mood, risk factors, assessment and psychological treatment of depression.",
    "Borderline personality disorder": "A personality disorder marked by unstable emotions, relationships and self-image, impulsivity and self-harm; its features, causes and therapy.",
    "Seasonal affective disorder": "Depression that recurs with the seasons, usually in winter: seasonal mood patterns, light exposure, circadian rhythms and light therapy.",
    "Schizophrenia": "Psychotic disorder with hallucinations, delusions and cognitive impairment: symptoms, cognition, risk factors and treatment of schizophrenia and psychosis.",
    "Antisocial personality disorder": "Persistent disregard for the rights of others: psychopathy, conduct problems, aggression, criminal behaviour and callous-unemotional traits.",
    "Media violence": "Effects of violent media content: violent video games, television or films and their links to aggression, desensitization and behaviour.",
    "Prenatal development": "Development before birth: fetal growth and prenatal exposures such as maternal stress, substances or nutrition, and their later outcomes.",
    "Child abuse": "Maltreatment of children: physical, sexual or emotional abuse and neglect, its consequences, detection and prevention.",
    "Gender roles": "Social expectations about how women and men behave: gender stereotypes, gender identity, division of labour and gender differences.",
    "False memories": "Remembering events that did not happen or remembering them wrongly: misinformation effects, suggestibility, eyewitness errors and memory reconstruction.",
    "Attention": "Selecting and focusing on information: attentional control, visual attention, distraction, vigilance and attention deficits.",
    "Problem-solving": "How people find solutions to problems: reasoning strategies, insight, creativity, planning, social problem solving, and teaching problem-solving skills (for example in mathematics).",
    # Biochemistry
    "Molecular biology": "The molecular basis of biological activity: DNA, RNA and protein structure and function, and gene expression and its regulation at the molecular level.",
    "Cell biology": "Structure and function of cells: organelles, cell signalling, division, death and migration, and other cellular processes.",
    "Human metabolism": "Chemical processes that sustain the human body: energy, glucose, lipid and amino-acid metabolism, nutrition and metabolic disorders.",
    "Immunology": "The immune system and immune responses: antibodies, T and B cells, inflammation, defence against infection, vaccines and autoimmunity.",
    "Genetics": "Genes, heredity and variation: mutations, polymorphisms, inheritance, genetic association studies (GWAS), population genetics and genome analysis.",
    "Enzymology": "Enzymes and how they work: catalytic mechanisms, kinetics, enzyme structure, inhibition, and enzyme engineering or applications.",
    "Polymerase chain reaction": "PCR-based methods that amplify DNA: PCR assays, real-time quantitative PCR, primer design and PCR-based detection or diagnosis.",
    "Northern blotting": "Detecting specific RNA molecules separated by gel electrophoresis and transferred to a membrane; studies of RNA or gene expression using this technique.",
    "Southern blotting": "Detecting specific DNA sequences separated by gel electrophoresis and transferred to a membrane; DNA analysis studies using this technique.",
}

COPYRIGHT_RE = re.compile(  # candidate start of a publisher notice (optional "(" / "Crown" prefix is removed too)
    r"\s*\(?\s*(?:Crown\s+)?(?:(?:Copyright\s*)?(?:\(C\)|\(c\)|©)|Copyright\b|Published by\s+[A-Z])")
NOTICE_OK = re.compile(  # the candidate must look like a real notice (not a list marker such as "(c) MMAS-8 scores")
    r"^\s*\(?\s*(?:Crown\s+)?(?:Copyright\s*)?(?:\(C\)|\(c\)|©)?\s*(?:Copyright\s*)?"
    r"(?:(?:19|20)\d\d|by\s|The Authors?\b|Published by\s|"
    r"[A-Z][^.;]{0,80}?(?:rights reserved|Published|Elsevier|Wiley|Springer|Society|Association|IEEE|Taylor|SAGE"
    r"|Journals?\b|Press\b|Authors?\b|Ltd|Inc\b|B\.V\.|Institute|Media\b|LLC|Publishing|Federation|Academy|College"
    r"|Foundation|Ministry|Council|University|Government))")
SENT_END = tuple('.?!)]"\'')

# author-keyword forms that confirm an area (besides the area name itself), lower case
AREA_KW_SYN = {
    "Polymerase chain reaction": ["pcr"], "Northern blotting": ["northern blot"],
    "Southern blotting": ["southern blot"], "Signal-flow graph": ["signal flow graph"],
    "State space representation": ["state space", "state-space"], "Problem-solving": ["problem solving"],
    "False memories": ["false memory"], "Operational amplifier": ["op-amp", "opamp", "op amp"],
    "Human metabolism": ["metabolism"], "Electrical circuits": ["electrical circuit", "electric circuit"],
    "Electrical generator": ["electric generator", "electrical generator"],
    "Strength of materials": ["strength of material"], "Materials engineering": ["material engineering"],
}


def norm(s):
    return re.sub(r"\s+", " ", str(s)).strip()


def area_name(raw):
    k = norm(raw).lower()
    if k in AREA_NAME_FIX:
        return AREA_NAME_FIX[k]
    s = norm(raw)
    return s[0].upper() + s[1:]


def clean_abstract(s):
    s = str(s).strip()
    # remove a publisher copyright notice and anything after it (only if it starts in the last 40% of the text
    # and looks like a real notice); what follows such a notice is a lay summary or publisher boilerplate
    for m in COPYRIGHT_RE.finditer(s):
        if m.start() >= 0.6 * len(s) and NOTICE_OK.match(s[m.start():]):
            return s[:m.start()].rstrip(), True
    return s, False


def kw_confirmed(area, keywords):
    """True if the authors' own keyword list names the area (human confirmation of the retrieval-keyword label)."""
    kws = [norm(k).lower() for k in str(keywords).split(";")]
    forms = [area.lower()] + AREA_KW_SYN.get(area, [])
    return any(f in k for f in forms for k in kws if k)


def ensure_snapshot():
    if not os.path.exists(ZIP):
        os.makedirs(CACHE, exist_ok=True)
        urllib.request.urlretrieve(ZIP_URL, ZIP)
    h = hashlib.sha256(open(ZIP, "rb").read()).hexdigest()
    if h != ZIP_SHA:
        sys.exit("sha256 mismatch for WebOfScience.zip: " + h)


def load():
    import pandas as pd
    ensure_snapshot()
    with zipfile.ZipFile(ZIP) as z, z.open("Meta-data/Data.xlsx") as f:
        df = pd.read_excel(f)
    return df


def round_robin(pools, n, rng):
    """pools: {label: {sub: [records]}} -> pick n records, balanced over labels, round-robin over subs."""
    out = []
    lab_iters = {}
    for lab, subs in pools.items():
        keys = sorted(subs)
        rng.shuffle(keys)
        for k in keys:
            rng.shuffle(subs[k])
        lab_iters[lab] = [keys, {k: 0 for k in keys}, 0]  # sub order, per-sub index, next sub pointer
    counts = collections.Counter()
    exhausted = set()
    labs = sorted(pools)
    while len(out) < n and len(exhausted) < len(labs):
        lab = min((l for l in labs if l not in exhausted), key=lambda l: (counts[l], l))
        keys, idx, ptr = lab_iters[lab]
        got = None
        for _ in range(len(keys)):
            k = keys[ptr % len(keys)]; ptr += 1
            if idx[k] < len(pools[lab][k]):
                got = pools[lab][k][idx[k]]; idx[k] += 1
                break
        lab_iters[lab][2] = ptr
        if got is None:
            exhausted.add(lab); continue
        out.append((lab, got)); counts[lab] += 1
    return out


def main():
    rng = random.Random(SEED)
    df = load()
    drop = collections.Counter()
    recs, seen = [], set()
    n_copy = 0
    for i, r in df.iterrows():
        dom = norm(r["Domain"]); area_raw = norm(r["area"])
        text, stripped = clean_abstract(r["Abstract"])
        if not (15 <= len(text) <= 4000):
            drop["length"] += 1; continue
        if not text.endswith(SENT_END):  # source abstract cut off mid-sentence (or residue of a notice)
            drop["no_sentence_end"] += 1; continue
        key = re.sub(r"\W+", " ", text.lower()).strip()
        if key in seen:
            drop["dup_text"] += 1; continue
        seen.add(key)
        n_copy += stripped
        an = area_name(area_raw)
        recs.append({"rid": "row%05d" % i, "dom": dom, "area_raw": area_raw, "area": an,
                     "text": text, "stripped": stripped, "kw_ok": kw_confirmed(an, r["keywords"]),
                     "named": an.lower() in text.lower(),
                     "orig": {"Y1": int(r["Y1"]), "Y2": int(r["Y2"]), "Y": int(r["Y"]),
                              "Domain": dom, "area": area_raw}})
    area_count = collections.Counter((x["dom"], x["area"]) for x in recs)
    conf_count = collections.Counter((x["dom"], x["area"]) for x in recs if x["kw_ok"])
    kept_areas = {k for k, c in area_count.items() if c >= MIN_AREA and conf_count[k] >= MIN_CONF}
    small = sorted(k for k in area_count if k not in kept_areas)
    n_unconf = sum(not x["kw_ok"] for x in recs)
    # the area label is the search keyword the paper was retrieved with; keep only records whose authors also list
    # that area among their own keywords (drops e.g. "Attention" papers on potentiometric sensors)
    recs = [x for x in recs if (x["dom"], x["area"]) in kept_areas and x["kw_ok"]]

    # --- area-within-domain task (Medical excluded) ---
    area_opts = {d: sorted({a for (dd, a) in kept_areas if dd == d}) for d in AREA_DOMAINS}
    for d in AREA_DOMAINS:
        for a in area_opts[d]:
            assert a in AREA_DEFS, ("missing definition", d, a)
    per_dom = {d: AREA_N // len(AREA_DOMAINS) + (1 if j < AREA_N % len(AREA_DOMAINS) else 0)
               for j, d in enumerate(AREA_DOMAINS)}
    used = set()
    area_rows = []
    for d in AREA_DOMAINS:
        pools = collections.defaultdict(lambda: collections.defaultdict(list))
        for x in recs:
            if x["dom"] == d:
                # two sub-pools of records that do not name the area verbatim, one that does -> ~2:1 in the picks
                sub = "named" if x["named"] else ("plain%d" % (len(pools[x["area"]]["plain0"]) >
                                                             len(pools[x["area"]]["plain1"])))
                pools[x["area"]][sub].append(x)
        picked = round_robin(pools, per_dom[d], rng)
        for a, x in picked:
            used.add(x["rid"])
            area_rows.append(("area", d, x))

    # --- 7-way domain task ---
    pools = collections.defaultdict(lambda: collections.defaultdict(list))
    for x in recs:
        if x["rid"] in used or (x["dom"], x["area"].lower()) in DOMAIN_TASK_EXCLUDE:
            continue
        pools[DOMAINS[x["dom"]]][x["area"]].append(x)
    dom_rows = [("domain", x["dom"], x) for lab, x in round_robin(pools, DOMAIN_N, rng)]

    rows = dom_rows + area_rows
    rng.shuffle(rows)
    out = []
    for task, d, x in rows:
        if task == "domain":
            instr = "Which research domain does this paper abstract belong to?"
            options = list(DOMAIN_ORDER)
            gold = DOMAINS[d]
        else:
            instr = "This is the abstract of a %s paper. Which research area within %s is it about?" % (
                DOMAINS[d], DOMAINS[d])
            options = list(area_opts[d])
            gold = x["area"]
        assert gold in options
        meta = dict(META_BASE)
        meta.update({"config": "WOS46985 Meta-data/Data.xlsx; task=" + ("domain-7way" if task == "domain"
                                                                         else "area-within-" + d),
                     "orig_label": x["orig"],
                     "text_cleaning": "trailing publisher copyright notice removed" if x["stripped"] else "none"})
        out.append({"key": "wos46985", "rid": x["rid"] + (":domain" if task == "domain" else ":area"),
                    "state": x["text"], "instructions": instr, "options": options, "gold": gold,
                    "soft": None, "meta": meta})
    assert len({o["rid"].split(":")[0] for o in out}) == len(out)  # one row per source record
    assert len(out) <= N_MAX

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        for o in out:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
    defs = dict(DOMAIN_DEFS)
    for d in AREA_DOMAINS:
        for a in area_opts[d]:
            defs[a] = AREA_DEFS[a]
    os.makedirs(os.path.dirname(DEFS_OUT), exist_ok=True)
    with open(DEFS_OUT, "w", encoding="utf-8") as f:
        json.dump(defs, f, ensure_ascii=False, indent=1)

    # --- report ---
    print("source records", len(df), "| kept pool", len(recs), "| drops", dict(drop),
          "| copyright notices stripped in pool", n_copy)
    print("unconfirmed (area not in author keywords) records dropped:", n_unconf)
    print("dropped areas (<%d records or <%d keyword-confirmed):" % (MIN_AREA, MIN_CONF), small)
    print("area task rows naming the gold area verbatim: %d/%d" % (sum(x["named"] for _, _, x in area_rows), len(area_rows)))
    print("rows written", len(out), "->", OUT)
    print("domain task:", len(dom_rows), dict(sorted(collections.Counter(DOMAINS[d] for _, d, _ in dom_rows).items())))
    print("area task:", len(area_rows))
    for d in AREA_DOMAINS:
        c = collections.Counter(x["area"] for t, dd, x in area_rows if dd == d)
        print("  %s: %d rows, %d options, max label share %.2f" % (d, sum(c.values()), len(area_opts[d]),
                                                                 max(c.values()) / sum(c.values())))
    gc = collections.Counter(o["gold"] for o in out)
    print("max gold share overall %.3f (%s)" % (max(gc.values()) / len(out), gc.most_common(1)[0][0]))
    print("soft coverage 0/%d" % len(out))
    L = sorted(len(o["state"]) for o in out)
    print("length chars min %d p50 %d mean %.0f max %d" % (L[0], L[len(L) // 2], sum(L) / len(L), L[-1]))
    wl = [len(v.split()) for v in defs.values()]
    print("defs", len(defs), "words min %d max %d" % (min(wl), max(wl)), "->", DEFS_OUT)


if __name__ == "__main__":
    main()
