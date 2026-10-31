"""STD domain 'evidence': claim verification with contrastive evidence (v0.11 parts).

Every item is a triple: one claim and one evidence template whose slot is filled three ways,
so the three passages differ minimally (a number, date, qualifier, negation, scope word or
hedge) and give SUPPORTS / REFUTES / NOT ENOUGH INFO. Some triples need a small calculation or
comparison (kind "calc"). All subjects are invented; all text is newly written by Claude as the
teacher (no external model, no dataset text).

Writes:
  data/v11_parts/std/evidence.jsonl        (with gold)
  data/v11_parts/std/evidence.blind.jsonl  (identical rows, gold removed)
Deterministic and re-runnable.
"""
import hashlib
import json
import random
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
OUT = HERE / "data" / "v11_parts" / "std"
DOMAIN = "evidence"
SRC = f"std_{DOMAIN}"
SEED = 20261102

S, R, N = "SUPPORTS", "REFUTES", "NOT ENOUGH INFO"
LABELS = (S, R, N)
DEFS = {
    S: "the evidence, taken on its own, shows the claim is true: every part of the claim, "
       "including its numbers, dates, qualifiers (all, only, first, most, never) and scope, is "
       "stated in the passage or follows from it by simple arithmetic or comparison.",
    R: "the evidence, taken on its own, shows the claim is false: at least one part of the claim "
       "conflicts with what the passage states or with what follows from it by simple arithmetic "
       "or comparison.",
    N: "the evidence neither shows the claim true nor shows it false: the passage leaves open at "
       "least one part the claim depends on (for example it covers a different date, place, group "
       "or measure, reports a plan, nomination, attempt, design or correlation instead of the "
       "outcome, or omits a figure the calculation needs), and nothing in it conflicts with the "
       "claim. Do not fill gaps with outside knowledge or guesses about what is likely.",
}

PHRASINGS = [
    "Does the evidence support the claim, refute it, or leave it undecided?",
    "Judge the claim using only the evidence passage.",
    "Based solely on the evidence, what is the verdict on this claim?",
    "Fact-check the claim against the evidence provided.",
    "Using the definitions, how does the evidence bear on the claim?",
    "Read the evidence and decide the status of the claim.",
    "Which verdict does the passage justify for the claim?",
    "Verify the claim. Rely only on the evidence given, not on outside knowledge.",
    "Given this evidence, is the claim backed, contradicted, or unresolved?",
]

# (key, kind, edit, claim, evidence template with {0}, S fill, R fill, N fill)
ITEMS = [
    ("e01", "contrastive", "date/hedge",
     "The Merrow Bridge was completed before 1900.",
     "The Merrow Bridge is a five-span sandstone arch bridge that carries the old coach road over "
     "the river Averne. Work on the piers began in 1894 under the county surveyor Edwin Carle, and "
     "the final span was {0}. The bridge was widened on its downstream side in 1936.",
     "closed and opened to traffic in 1898",
     "closed and opened to traffic in 1903",
     "due to be closed in 1898, the date set in Carle's contract"),
    ("e02", "contrastive", "scope",
     "Every station on the Kessel Valley line has step-free access from the street to the platform.",
     "The Kessel Valley line runs 41 km between Orton Market and Hale Point and serves eleven "
     "stations. A rebuilding programme completed in 2019 added lifts and ramps, and {0}.",
     "all eleven stations now have step-free routes from street level to every platform",
     "all but two of the eleven stations now have step-free routes from street level to every platform",
     "all eleven stations now have step-free routes from street level to the ticket hall"),
    ("e03", "contrastive", "negation",
     "The Ossery shrew hibernates through the winter.",
     "The Ossery shrew is a small insectivore of damp upland heath. Like most shrews it has a very "
     "high metabolic rate. {0} Individuals rarely live longer than fourteen months.",
     "It spends the coldest months in hibernation in a grass-lined burrow, emerging in early April.",
     "It does not hibernate; instead it forages beneath the snow throughout the winter.",
     "Captive individuals kept in heated enclosures stay active all year, but no winter field "
     "observations have been published."),
    ("e04", "calc", "number/comparison",
     "The steamer Calloway Star was larger than its sister ship, the Calloway Moon.",
     "The Calloway Star and the Calloway Moon were passenger steamers built at the Pellam yard for "
     "the Northern Isles service. The Star, launched in 1911, measured 2,140 gross register tons. "
     "The Moon, launched two years later, {0}.",
     "measured 1,980 gross register tons",
     "measured 2,305 gross register tons",
     "carried 40 more passengers than the Star"),
    ("e05", "contrastive", "hedge",
     "Mara Oyelaran's novel The Salt Ledger won the Harwick Prize.",
     "The Salt Ledger is the second novel by Mara Oyelaran, published in 2016. Set in a declining "
     "fishing port, it follows three generations of a family of net-makers. The book {0}, and it "
     "has been translated into nine languages.",
     "was awarded the Harwick Prize for fiction that year",
     "was shortlisted for the Harwick Prize for fiction that year, which went instead to Deren "
     "Pike's Quarry Hill",
     "was shortlisted for the Harwick Prize for fiction that year"),
    ("e06", "contrastive", "number/date",
     "In 2021, wind turbines on Lindqvist Bay itself generated more than half of the electricity "
     "consumed on the island.",
     "Lindqvist Bay is an island municipality of about 9,000 people connected to the mainland grid "
     "by a single undersea cable. Wind turbines on the island's western ridge generated {0} of the "
     "electricity consumed locally, with the remainder imported through the cable.",
     "58 percent in 2021",
     "47 percent in 2021",
     "58 percent in 2023"),
    ("e07", "contrastive", "scope",
     "The city of Tarsin has a population of over one million.",
     "Tarsin is the capital of the inland province of Vell and its main rail junction. According "
     "to the 2020 census, {0}, making it the largest urban area in the province.",
     "the city proper had 1,140,000 inhabitants",
     "the city proper had 914,000 inhabitants",
     "the wider metropolitan area, including eleven satellite towns, had 1,140,000 inhabitants"),
    ("e08", "contrastive", "number/qualifier",
     "Brackenford Rovers did not lose a home league match in the 1987-88 season.",
     "Brackenford Rovers finished second in the Midland Combination in 1987-88, a point behind the "
     "champions. Their home record that season was {0}, and the club's top scorer, Alan Tully, "
     "scored 23 league goals.",
     "fourteen wins and six draws from twenty matches",
     "fourteen wins, five draws and one defeat from twenty matches",
     "the best in the division"),
    ("e09", "contrastive", "hedge/negation",
     "Corvain's national assembly banned single-use plastic bags in 2018.",
     "Plastic bag regulation in Corvain dates from a 2011 levy of two cents per bag at supermarket "
     "checkouts. In 2018 the national assembly {0} a full ban on single-use plastic bags, including "
     "bags made of so-called biodegradable blends.",
     "approved",
     "voted down",
     "debated"),
    ("e10", "calc", "date",
     "The astronomer Ilse Varrow was over 70 when she discovered the comet that bears her name.",
     "Ilse Varrow (born 1881) was a self-taught astronomer who observed from a private observatory "
     "in the hills above Gessin. She {0}. The comet has an orbital period of about 94 years.",
     "found Comet Varrow on the night of 3 March 1953, using a 20 cm refractor",
     "found Comet Varrow on the night of 3 March 1949, using a 20 cm refractor",
     "found Comet Varrow in the year her observatory was rebuilt after a fire"),
    ("e11", "contrastive", "comparison/date",
     "The Halden Tower is the tallest building in Mirecourt.",
     "The Halden Tower is a 46-storey office building in the Quay district of Mirecourt, completed "
     "in 2009. It rises to 188 metres. {0}",
     "No other building in the city exceeds 150 metres.",
     "The Brisson Centre, finished two years later on the opposite bank, reaches 204 metres.",
     "It was the tallest building in the city when it opened."),
    ("e12", "contrastive", "qualifier",
     "The Pellworth ferry was the first vehicle ferry to operate on the Sarne estuary.",
     "The Pellworth ferry began carrying cars and horse-drawn carts across the Sarne estuary in "
     "1924, replacing a rowing-boat service. {0} It was withdrawn after the Sarne road bridge "
     "opened in 1967.",
     "No vehicle crossing of the estuary had existed before it.",
     "A chain ferry at Oldmere, a few kilometres upstream, had taken carts across the estuary since "
     "the 1880s.",
     "It was the first ferry on the estuary to be powered by a diesel engine."),
    ("e13", "contrastive", "number/scope",
     "The Harlow Fields trial enrolled more than 2,000 patients.",
     "The Harlow Fields trial tested whether a daily low-dose regimen of the drug calvenide reduced "
     "the rate of second strokes. {0} across 31 hospitals between 2012 and 2015; results were "
     "published in 2019.",
     "Investigators enrolled 2,418 patients",
     "Investigators enrolled 1,862 patients",
     "Investigators screened 2,418 patients for eligibility"),
    ("e14", "contrastive", "causal",
     "The closure of the Dunmore paper mill caused the fall in Dunmore's population during the 1990s.",
     "Dunmore's paper mill, once the town's largest employer, closed in 1991 with the loss of 640 "
     "jobs. Between the 1991 and 2001 censuses the town's population fell from 14,200 to 12,900. {0}",
     "The regional statistics office found that the fall was driven almost entirely by households "
     "that had depended on mill wages moving away.",
     "The regional statistics office found that the fall was driven by the closure of the town's "
     "army barracks in 1993, and that most former mill workers stayed and found other local jobs.",
     "The town's population had also been falling slowly during the 1980s, while the mill was still "
     "open."),
    ("e15", "contrastive", "date",
     "The Ostrander Institute was founded in the nineteenth century.",
     "The Ostrander Institute is a private research library specialising in maritime law. {0} by "
     "the shipping magnate Cornelius Ostrander, whose collection of charts and legal papers formed "
     "its core. It moved to its present building on Wharf Street in 1952.",
     "It was founded in 1897",
     "It was founded in 1901",
     "Its charter was drafted in 1897"),
    ("e16", "calc", "number/unit",
     "Lake Varda is deeper than 300 feet.",
     "Lake Varda is a glacial lake in the Orrin Hills covering about 14 square kilometres. {0} It "
     "freezes over in most winters.",
     "Its maximum depth is 97 metres.",
     "Its maximum depth is 88 metres.",
     "Its mean depth is 88 metres."),
    ("e17", "contrastive", "scope",
     "All members of the Ferrant Quartet studied at the Vosberg Conservatory.",
     "The Ferrant Quartet is a string quartet formed in 2004 and based in Lorne. {0} The quartet has "
     "recorded the complete string quartets of Anton Keel.",
     "All four players met as students at the Vosberg Conservatory.",
     "Three of the players met as students at the Vosberg Conservatory; the cellist, Hana Roos, "
     "trained privately.",
     "Its first violinist and violist met as students at the Vosberg Conservatory."),
    ("e18", "contrastive", "date/negation",
     "The Castell line still runs passenger trains to Rhoswen.",
     "The Castell line was built in 1868 to carry slate from the quarries at Rhoswen to the coast. "
     "{0} A heritage group has restored the station building at Rhoswen as a museum.",
     "Passenger trains have run on the line since 1873 and continue to serve Rhoswen today.",
     "Passenger trains ran on the line from 1873 until 1964, when the route closed.",
     "Passenger trains were introduced on the line in 1873."),
    ("e19", "calc", "number/date",
     "Annual visits to Kerrow Gorge park more than doubled between 2010 and 2020.",
     "Kerrow Gorge became a regional park in 2008. The park recorded {0}. A visitor centre opened "
     "at the southern entrance in 2016.",
     "about 61,000 visits in 2010 and about 134,000 in 2020",
     "about 61,000 visits in 2010 and about 118,000 in 2020",
     "about 61,000 visits in 2010 and about 134,000 in 2019"),
    ("e20", "contrastive", "hedge/negation",
     "The Orvel Dam produces hydroelectric power.",
     "The Orvel Dam is a 62-metre concrete gravity dam on the river Tamsk, completed in 1978 mainly "
     "to control seasonal flooding downstream. {0}",
     "A 40-megawatt power station at its base has fed the regional grid since 1981.",
     "It has no turbines, and water is released only through the spillway and irrigation outlets.",
     "A 40-megawatt power station at its base was proposed in 2015."),
    ("e21", "contrastive", "number/qualifier",
     "A female Ganley aphid can produce at least 60 offspring in her lifetime.",
     "The Ganley aphid is a sap-feeding insect and a pest of field beans. Like many aphids, females "
     "reproduce without mating during summer. {0}",
     "Laboratory studies found that a single female produces between 60 and 90 young over her life.",
     "Laboratory studies found that a single female produces at most 45 young over her life.",
     "Laboratory studies found that a single female can produce up to five young per day."),
    ("e22", "calc", "date",
     "Ruth Allard served as governor of Tessin Province for more than eight years.",
     "Ruth Allard, a former schoolteacher, was elected governor of Tessin Province in November 1994 "
     "and took office in January 1995. {0}",
     "She left office in March 2003, when she resigned to join the national senate.",
     "She left office in January 2002, when she resigned to join the national senate.",
     "She was re-elected once and resigned during her second term to join the national senate."),
    ("e23", "contrastive", "entity",
     "The painter Joris Hemmel was born in Aalsted.",
     "Joris Hemmel (1742-1803) was a landscape painter known for his winter river scenes. {0} He "
     "trained in the workshop of Pieter Voss and later settled in the capital.",
     "He was born in the river town of Aalsted, where his father worked as a dyer.",
     "He was born in Oudwijk and moved to Aalsted at the age of twelve, when his father took work "
     "there as a dyer.",
     "His father, the dyer Hendrik Hemmel, was born in Aalsted."),
    ("e24", "calc", "scope/number",
     "A majority of Glenmore's registered voters voted in favour of the merger in the 2019 "
     "referendum.",
     "In the 2019 referendum on merging Glenmore with the neighbouring parish of Ashby, {0}. The "
     "merger took effect in April 2020.",
     "turnout was 81 percent of the 6,400 registered voters and 68 percent of those voting backed "
     "the proposal",
     "turnout was 58 percent of the 6,400 registered voters and 68 percent of those voting backed "
     "the proposal",
     "68 percent of those voting backed the proposal"),
    ("e25", "contrastive", "negation/entity",
     "The Veller lizard is venomous.",
     "The Veller lizard is a heavy-bodied lizard of the coastal scrub of the Draskan peninsula, "
     "reaching about 45 cm in length. {0} It feeds mainly on eggs, beetles and carrion.",
     "Like its close relative the ringed skink, it delivers venom through grooved teeth in the "
     "lower jaw.",
     "Unlike its close relative the ringed skink, it has no venom glands, and its bite, though "
     "painful, is harmless.",
     "Its close relative, the ringed skink, delivers venom through grooved teeth in the lower jaw."),
    ("e26", "calc", "number",
     "The Arlen express averages more than 150 km/h between Arlen and Port Cassis.",
     "The Arlen express is a daily service on the electrified coastal main line. {0}, with two "
     "intermediate stops.",
     "It covers the 312 km from Arlen to Port Cassis in 1 hour 55 minutes",
     "It covers the 312 km from Arlen to Port Cassis in 2 hours 20 minutes",
     "It reaches a top speed of 200 km/h on the 312 km run from Arlen to Port Cassis"),
    ("e27", "contrastive", "entity/correlation",
     "The Tolland Hoard was buried by Roman soldiers.",
     "The Tolland Hoard is a collection of 1,300 silver coins found by a farmer in 1987. The latest "
     "coins date from AD 260. {0}",
     "Inscribed lead tags found with the coins record that they were the pay chest of a Roman "
     "cavalry unit, buried by its own soldiers during a raid.",
     "Analysis of the pot and the tags found with it shows that the coins were buried by a local "
     "farming family, not by soldiers.",
     "A Roman cavalry fort stood two kilometres from the find spot at the time the coins were "
     "buried."),
    ("e28", "contrastive", "number/measure",
     "The same club has won the Rennick Cup more than ten times.",
     "The Rennick Cup is an annual knockout rowing competition for clubs on the Ashwater, first "
     "held in 1921. {0}",
     "Ashwater Boat Club holds the record with fourteen wins, the most recent in 2018.",
     "Ashwater Boat Club holds the record with nine wins, the most recent in 2018.",
     "Ashwater Boat Club has reached the final more than twenty times."),
    ("e29", "contrastive", "entity/role",
     "Henrik Salo is the chief executive of Norrvik Shipping.",
     "Norrvik Shipping is a container line headquartered in Saltholm, operating 38 vessels. {0} The "
     "company was listed on the Saltholm exchange in 1998.",
     "Henrik Salo has been its chief executive since 2017.",
     "Henrik Salo was its chief executive from 2009 to 2017, when he was succeeded by Ada Lind.",
     "Henrik Salo has chaired its board since 2017."),
    ("e30", "calc", "measure",
     "Wheat yields in the Merrin district fell by more than 10 percent from 2018 to 2019.",
     "The Merrin district is the main wheat-growing area of the Upper Salt basin. {0}, a drop that "
     "the agriculture ministry blamed on a late spring frost.",
     "Average yields went from 6.2 tonnes per hectare in 2018 to 5.4 tonnes in 2019",
     "Average yields went from 6.2 tonnes per hectare in 2018 to 5.7 tonnes in 2019",
     "Total wheat output went from 412,000 tonnes in 2018 to 356,000 tonnes in 2019"),
    ("e31", "contrastive", "scope/comparison",
     "The Sarn cave system is the longest cave system in Varenia.",
     "The Sarn cave system lies beneath the limestone plateau of northern Varenia. Explorers have "
     "surveyed 87 km of its passages. {0}",
     "No other known cave in Varenia exceeds 40 km.",
     "It is the second-longest in the country after the Morrow system, which exceeds 110 km.",
     "It is the longest cave system in the northern half of the country."),
    ("e32", "contrastive", "hedge/negation",
     "The 1932 Dellan expedition reached the summit of Mount Ivra.",
     "The 1932 Dellan expedition was the first organised attempt on Mount Ivra, the highest peak of "
     "the Coron range. {0}",
     "After six weeks on the mountain, two of its members stood on the summit on 14 August.",
     "After six weeks on the mountain, bad weather forced it to turn back 300 metres below the "
     "summit.",
     "After six weeks on the mountain, two of its members set out for the summit on 14 August."),
    ("e33", "calc", "number/comparison",
     "Orsk has a higher population density than Varm.",
     "Orsk and Varm are neighbouring market towns on the Pell plain. Orsk has 18,000 inhabitants in "
     "an area of 12 square kilometres, {0}.",
     "while Varm has 26,000 inhabitants in 21 square kilometres",
     "while Varm has 26,000 inhabitants in 15 square kilometres",
     "while Varm has 26,000 inhabitants"),
    ("e34", "contrastive", "qualifier",
     "The Lanthorn Fair is always held in July.",
     "The Lanthorn Fair is a lantern-making festival held in the old town of Bressay each summer. {0}",
     "By a rule laid down in its founding charter, it always takes place on the last weekend of July.",
     "It usually takes place on the last weekend of July, but in years with a late harvest it moves "
     "to early August.",
     "The 2022 fair took place on the last weekend of July."),
    ("e35", "calc", "date/hedge",
     "The Karst Observatory opened before its larger rival at Mount Pell.",
     "The Karst Observatory, with its 1.2-metre telescope, {0}. The observatory at Mount Pell, home "
     "to a 2-metre instrument, opened in 1968.",
     "opened in 1961",
     "opened in 1974",
     "was designed in 1961"),
    ("e36", "contrastive", "scope",
     "Parking is free on every street in central Halloway on Sundays.",
     "Halloway council charges for on-street parking in the central zone from 8 am to 6 pm, Monday "
     "to Saturday. {0}",
     "No charges apply anywhere in the zone on Sundays.",
     "On Sundays parking is free except on Market Street and Quay Road, where charges apply every "
     "day.",
     "On Sundays the council's multi-storey car parks are free."),
    ("e37", "contrastive", "number/measure",
     "The Glassford Library holds more than a million printed volumes.",
     "The Glassford Library is the main research library of the University of Tarn. {0}. It moved "
     "into its current building in 1964.",
     "Its stacks contain about 1.3 million printed volumes",
     "Its stacks contain about 940,000 printed volumes",
     "Its catalogue lists about 1.3 million items, including maps, photographs and sound recordings"),
    ("e38", "contrastive", "hedge/negation",
     "The Harnet Act made it illegal to fish in the Loy estuary during the spawning season.",
     "The Harnet Act of 1911 regulated inland and estuary fisheries in the county of Loy. {0}",
     "Among its provisions, it banned all fishing in the Loy estuary between March and June, when "
     "salmon spawn there.",
     "A ban on fishing in the Loy estuary during the spawning season was debated, but the final act "
     "left the estuary open all year and only limited net sizes.",
     "Among its provisions, it limited the size of nets used in the Loy estuary."),
    ("e39", "contrastive", "comparison/scope",
     "St Aldric's is the oldest church in Wendham.",
     "St Aldric's is a stone parish church in the market square of Wendham. Its nave dates from "
     "about 1140 and its tower from the fifteenth century. {0}",
     "No other church in the town has fabric earlier than 1300.",
     "The church of St Ebba, on the castle mound, contains walls dating from the 1080s.",
     "It is the oldest building in the market square."),
    ("e40", "calc", "number/scope",
     "The Travers family gave more than 50,000 pounds to the Ashcombe hospital appeal.",
     "The Ashcombe hospital appeal raised money for a new children's wing between 1998 and 2001. {0}",
     "Its largest private donors were Margaret Travers, who gave 32,000 pounds, and her brother Tom "
     "Travers, who gave 21,500 pounds.",
     "Its largest private donors were Margaret Travers, who gave 32,000 pounds, and her brother Tom "
     "Travers, who gave 15,500 pounds; no other member of the family contributed.",
     "Its largest private donors were Margaret Travers, who gave 32,000 pounds, and her brother Tom "
     "Travers, who gave 15,500 pounds."),
    ("e41", "contrastive", "qualifier/date",
     "The Carrow Marathon has been held every year since 1985.",
     "The Carrow Marathon is a road race through the lowland villages of the Carrow valley, first "
     "run in 1985 with 212 finishers. {0}",
     "It has been staged annually ever since, and the 2023 race had more than 4,000 finishers.",
     "Apart from 2001, when it was cancelled during a livestock-disease outbreak, it has been staged "
     "annually, and the 2023 race had more than 4,000 finishers.",
     "The 2023 race, the largest so far, had more than 4,000 finishers."),
    ("e42", "contrastive", "hedge/entity",
     "The fresco in the Oriel chapel was painted by Tommaso Brena.",
     "The Oriel chapel fresco depicts the Flight into Egypt and was uncovered beneath whitewash in "
     "1956. {0}",
     "A signed contract of 1487 in the town archive records Tommaso Brena's payment for painting it.",
     "Once credited to Tommaso Brena, it was shown in 1990 to be the work of his pupil Nicolo Sarto, "
     "whose signature was found under a later repair.",
     "Its style resembles that of Tommaso Brena, who worked in the town in the 1480s."),
    ("e43", "contrastive", "measure/order",
     "By area, Ferra is the third-largest island in the Velmar archipelago.",
     "The Velmar archipelago consists of seven inhabited islands and many uninhabited islets. {0}",
     "By area, the largest islands are Hollin (212 km2), Skarra (147 km2), Ferra (96 km2) and Dunn "
     "(58 km2).",
     "By area, the largest islands are Hollin (212 km2), Ferra (147 km2), Skarra (96 km2) and Dunn "
     "(58 km2).",
     "By population, the largest islands are Hollin, Skarra, Ferra and Dunn."),
    ("e44", "contrastive", "date/scope",
     "Cranleigh College admitted women from its foundation.",
     "Cranleigh College was founded in 1869 as a teacher-training college. {0}",
     "Its first intake of forty students included eleven women.",
     "It admitted only men until 1921, when the first six women enrolled.",
     "By 1921 women made up a third of its students."),
    ("e45", "calc", "number",
     "Brenna spends more on its public library per resident than Coldstream does.",
     "The neighbouring towns of Brenna and Coldstream each run a single public library. {0}",
     "In 2022 Brenna, with 20,000 residents, spent 900,000 crowns on its library, while "
     "Coldstream, with 32,000 residents, spent 1.2 million.",
     "In 2022 Brenna, with 20,000 residents, spent 900,000 crowns on its library, while "
     "Coldstream, with 24,000 residents, spent 1.2 million.",
     "In 2022 Brenna spent 900,000 crowns on its library, while Coldstream spent 1.2 million."),
    ("e46", "contrastive", "negation/hedge",
     "The Mossley Hall estate was sold to the National Heritage Board.",
     "Mossley Hall is a Georgian country house set in 300 hectares of parkland. After the death of "
     "the last baronet in 1978, {0}",
     "his heirs sold the house and park to the National Heritage Board, which opened them to the "
     "public in 1981.",
     "his heirs turned down an offer from the National Heritage Board and sold the estate to a "
     "hotel group in 1981.",
     "his heirs opened talks with the National Heritage Board about the estate's future."),
    ("e47", "contrastive", "scope",
     "The silver hornbeam is native to the Arden Hills.",
     "The silver hornbeam is a deciduous tree with pale, smooth bark, widely planted in parks for its "
     "autumn colour. {0}",
     "Its natural range is restricted to limestone slopes in the Arden Hills and neighbouring "
     "valleys.",
     "It is native to the mountains of the far south and was introduced to the Arden Hills as an "
     "ornamental in the 1800s.",
     "Large plantings of it line the roads through the Arden Hills."),
    ("e48", "calc", "date",
     "The Treaty of Hollen was signed less than a year after the Border War began.",
     "The Border War between Estria and Calm began with the Estrian crossing of the river Doss on "
     "12 May 1831. {0}",
     "Fighting ended after the battle of Mell Ford, and the Treaty of Hollen was signed on 2 March "
     "1832.",
     "Fighting ended after the battle of Mell Ford, and the Treaty of Hollen was signed on 30 June "
     "1832.",
     "Fighting ended after the battle of Mell Ford on 2 March 1832, and the Treaty of Hollen "
     "followed."),
    ("e49", "contrastive", "scope",
     "The Kelder vaccine reduced hospital admissions among adults over 65.",
     "The Kelder vaccine against the Tarn respiratory virus was tested in a two-year randomised "
     "trial of 18,000 adults. {0}",
     "Among participants over 65, those given the vaccine were admitted to hospital 42 percent less "
     "often than those given a placebo.",
     "Among participants over 65, those given the vaccine were admitted to hospital as often as "
     "those given a placebo; the benefit was confined to younger adults.",
     "Across all ages, those given the vaccine were admitted to hospital 42 percent less often than "
     "those given a placebo."),
    ("e50", "contrastive", "date/hedge",
     "The Irvane Canal opened in the 1790s.",
     "The Irvane Canal links the coalfields around Brough with the port of Selham, a distance of "
     "38 km. {0} It carried coal until 1955.",
     "It was authorised by parliament in 1788 and opened to traffic in 1794.",
     "It was authorised by parliament in 1794 and opened to traffic in 1802.",
     "It was authorised by parliament in 1794, and digging began the following spring."),
    ("e51", "calc", "number/measure",
     "The Ryn is more than twice as long as the Aske.",
     "The Ryn and the Aske both rise on the Hallow moors and flow east to the sea. {0}",
     "The Ryn runs for 143 km and the Aske for 68 km.",
     "The Ryn runs for 143 km and the Aske for 76 km.",
     "The Ryn drains an area more than twice as large as the Aske's."),
    ("e52", "contrastive", "hedge/status",
     "The Pinder frog is officially classified as extinct.",
     "The Pinder frog is a small tree frog known from cloud forest on the slopes of Mount Pinder. It "
     "was last seen in 1994. {0}",
     "Following repeated surveys that found no trace of it, it was formally listed as extinct in "
     "2019.",
     "Despite repeated surveys that found no trace of it, it is still listed as critically "
     "endangered rather than extinct.",
     "Repeated surveys since then have found no trace of it."),
    ("e53", "contrastive", "number/qualifier",
     "The Keel family owns a majority of the shares in Brandt Mills.",
     "Brandt Mills is a flour milling company founded in 1890 by Otto Brandt. {0}",
     "Descendants of Otto's partner, Hugo Keel, together hold 54 percent of its shares.",
     "Descendants of Otto's partner, Hugo Keel, together hold 38 percent of its shares, making them "
     "the largest single group of shareholders.",
     "Descendants of Otto's partner, Hugo Keel, are the largest single group of shareholders."),
    ("e54", "contrastive", "negation/hedge",
     "Prime Minister Oda Brask attended the 1998 Coldhaven summit.",
     "The 1998 Coldhaven summit brought together the leaders of the six Northern Rim states to agree "
     "a common fisheries policy. {0}",
     "Prime Minister Oda Brask led her country's delegation and signed the final communique.",
     "Prime Minister Oda Brask stayed at home because of a government crisis, and her foreign "
     "minister signed the final communique in her place.",
     "Oda Brask, then prime minister, had pressed for the summit to be held."),
    ("e55", "calc", "number",
     "The Vellan Hawks averaged more than 20,000 spectators per home game in 2022.",
     "The Vellan Hawks play their home games at the Tarn Road stadium, which holds 26,000. {0}",
     "In 2022 the club drew a total of 357,000 spectators to its 17 home games.",
     "In 2022 the club drew a total of 323,000 spectators to its 17 home games.",
     "In 2022 the club drew a total of 357,000 spectators to its home games."),
    ("e56", "contrastive", "date/status",
     "The Lynde lighthouse is still in operation.",
     "The Lynde lighthouse stands on a granite skerry at the mouth of Lynde Sound and was first lit "
     "in 1856. {0}",
     "Automated in 1987, it continues to guide vessels into the sound.",
     "It was taken out of service in 1987, after a new light on the headland replaced it.",
     "It was automated in 1987, when its last keepers left."),
    ("e57", "contrastive", "entity/scope",
     "The original 1908 building of the Holt Street school was designed by Clara Venn.",
     "The Holt Street school opened in 1908 and was extended in 1931. {0}",
     "The original building was designed by Clara Venn, one of the first women to practise "
     "architecture in the city.",
     "The original building was designed by the city architect Samuel Ord; Clara Venn designed the "
     "1931 extension.",
     "The 1931 extension was designed by Clara Venn, one of the first women to practise "
     "architecture in the city."),
    ("e58", "calc", "number",
     "Women made up more than a third of the Varn city council after the 2021 election.",
     "The 2021 election to the Varn city council returned {0}.",
     "17 women among its 45 members",
     "14 women among its 45 members",
     "17 women, more than at any previous election"),
    ("e59", "contrastive", "negation/scope",
     "Keswin Brewery's beers are brewed at its original site on Mill Lane.",
     "Keswin Brewery was founded in 1872 on Mill Lane in the town of Keswin. {0}",
     "It still brews all its beers there, in a brewhouse rebuilt in 1990.",
     "Brewing moved to an industrial estate outside the town in 1990, and the Mill Lane buildings "
     "are now flats.",
     "Its visitor centre and shop remain on Mill Lane."),
    ("e60", "calc", "comparison/scope",
     "Tove Lindahl set a national record in the 800 metres at the 2014 championships.",
     "Tove Lindahl won the 800 metres at the 2014 national championships in a time of 1:58.9. {0}",
     "This beat the previous national record of 1:59.4, set in 1987.",
     "The national record, 1:57.6, had stood since 1987 and was not broken until 2019.",
     "It was the fastest time recorded at the championships since 1987."),
    ("e61", "contrastive", "hedge/negation",
     "Darrow cheese has protected designation of origin status.",
     "Darrow cheese is a hard sheep's-milk cheese made on upland farms in the Darrow region. {0}",
     "Since 2012 its name has been protected by a designation of origin, so only cheese made in the "
     "region may be sold as Darrow.",
     "An application for a protected designation of origin was rejected in 2012, and cheese sold "
     "under the same name is made elsewhere.",
     "Producers applied for a protected designation of origin in 2012."),
    ("e62", "contrastive", "date/number",
     "Fewer than 1,000 people lived on Skell Island in 1901.",
     "Skell Island lies 12 km off the coast and was once home to a herring fleet. {0} Today it has "
     "140 permanent residents.",
     "Its population peaked at 1,310 in 1871 and had fallen to 870 by the 1901 census.",
     "Its population peaked at 1,310 in 1901 and had fallen to 870 by 1931.",
     "Its population peaked at 1,310 in 1871 and had fallen to 870 by 1931."),
    ("e63", "calc", "date/comparison",
     "The composer Liesl Arn was older than her collaborator Piet Holm.",
     "Liesl Arn and Piet Holm wrote four operettas together between 1921 and 1930. {0}",
     "Arn was born in 1884 and Holm in 1891.",
     "Arn was born in 1893 and Holm in 1887.",
     "Arn was born in 1884 and Holm died in 1941."),
    ("e64", "contrastive", "qualifier",
     "The Quenby wind farm is owned entirely by the town of Quenby.",
     "The Quenby wind farm's eight turbines were installed on the ridge above the town in 2015. {0}",
     "The farm is wholly owned by Quenby town council, which uses the income to fund local "
     "services.",
     "The town council owns a 30 percent stake; the rest belongs to the energy company Westvolt.",
     "The farm was built with a loan arranged by Quenby town council."),
    ("e65", "calc", "measure",
     "Unemployment in Tolva rose by more than 2 percentage points between 2019 and 2020.",
     "Tolva's economy depends heavily on its car-parts factories. {0}",
     "The unemployment rate rose from 4.8 percent in 2019 to 7.1 percent in 2020.",
     "The unemployment rate rose from 4.8 percent in 2019 to 6.5 percent in 2020.",
     "The number of unemployed people rose by 45 percent between 2019 and 2020."),
    ("e66", "contrastive", "negation",
     "The first crossing of the Hessen ice cap, in 1974, was made with dog teams.",
     "In the spring of 1974 a party of four led by Anna Brekke made the first crossing of the "
     "Hessen ice cap, covering 540 km in 38 days. {0}",
     "They hauled their sledges with the help of two teams of twelve dogs.",
     "They hauled their sledges themselves, without dogs or machines.",
     "Dog teams had been used on every earlier attempt, all of which failed."),
    ("e67", "contrastive", "scope/hedge",
     "Weston Airport handles international flights.",
     "Weston Airport is a single-runway airport 8 km south of the town, opened in 1969. {0}",
     "Besides domestic services to the capital, it has scheduled flights to three foreign cities.",
     "It handles only domestic flights, mainly to the capital, as it lacks passport and customs "
     "facilities.",
     "Its runway was lengthened in 2011 so that it can take the larger jets used on international "
     "routes."),
    ("e68", "calc", "date",
     "More than a century separates the founding of Haldor University and the opening of its "
     "medical school.",
     "Haldor University was founded in 1712 by a charter of the regional diet. {0}",
     "Its medical school opened in 1838.",
     "Its medical school opened in 1795.",
     "Its medical school is housed in a building completed in 1838."),
    ("e69", "contrastive", "number/measure",
     "The Senna tunnel is longer than 20 kilometres.",
     "The Senna tunnel carries the main railway under the Senna massif between Ovre and Castra. {0}",
     "Opened in 1998, it is 23.4 km long.",
     "Opened in 1998, it is 17.6 km long.",
     "Opened in 1998, it cut the rail distance between Ovre and Castra by 20 km."),
    ("e70", "contrastive", "negation/hedge",
     "The Merrit Company admitted responsibility for the 2016 Coldwater oil spill.",
     "In August 2016 about 1,200 tonnes of crude oil leaked from a pipeline near Coldwater, fouling "
     "30 km of coast. The pipeline was operated by the Merrit Company. {0}",
     "In a statement that September, the company accepted that its own maintenance failures had "
     "caused the leak.",
     "In a statement that September, the company denied fault, blaming damage caused by a "
     "contractor's excavator.",
     "In 2018 the company paid 40 million crowns into a clean-up fund."),
    ("e71", "calc", "number",
     "The Lorrin reservoir holds enough water to supply the city of Esk for a full year.",
     "The Lorrin reservoir was built in 1962 to supply the city of Esk. {0}",
     "It holds 95 million cubic metres; the city uses about 70 million cubic metres a year.",
     "It holds 95 million cubic metres; the city uses about 130 million cubic metres a year.",
     "It holds 95 million cubic metres, making it the largest reservoir in the province."),
    ("e72", "calc", "date/comparison",
     "The temple at Arsa is older than the fortress at Dunvik.",
     "The temple at Arsa {0}, while the fortress at Dunvik was raised around 450 BC.",
     "was built around 620 BC",
     "was built around 310 BC",
     "is decorated in a style that flourished from about 700 to 300 BC"),
    ("e73", "contrastive", "scope",
     "Ines Morro was the first person to swim across the Kessel Strait.",
     "The Kessel Strait is 34 km wide at its narrowest point and known for its cold currents. {0}",
     "Ines Morro made the first recorded crossing by any swimmer in 1926, taking 15 hours.",
     "Ines Morro became the first woman to swim across it in 1926, eleven years after the first "
     "crossing by Emil Sand.",
     "Ines Morro became the first woman to swim across it in 1926."),
    ("e74", "contrastive", "number/measure",
     "The Pollard Foundation gives away more than 5 million crowns a year.",
     "The Pollard Foundation funds music teaching in rural schools. {0}",
     "Its grants in each of the past five years have totalled between 6 and 7 million crowns.",
     "Its grants in each of the past five years have totalled between 3 and 4 million crowns.",
     "It holds an endowment of 90 million crowns and spends only the investment income."),
]


def cid(instr, state, options):
    h = hashlib.sha1(json.dumps([instr, state, options], ensure_ascii=False).encode()).hexdigest()
    return "c_" + h[:12]


def build():
    keys = [it[0] for it in ITEMS]
    assert len(keys) == len(set(keys)), "duplicate keys"
    rows, n = [], 0
    for i, (key, kind, edit, claim, tmpl, fs, fr, fn) in enumerate(ITEMS):
        assert tmpl.count("{0}") == 1, key
        rng = random.Random(f"{SEED}:{key}")
        options = list(LABELS)
        rng.shuffle(options)  # same order within a triple, so each triple uses every gold position once
        card = "\n".join(f"- {o}: {DEFS[o]}" for o in options)
        instr = PHRASINGS[i % len(PHRASINGS)]
        gid = f"g:{SRC}:{key}"
        base_id = None
        for gold, fill in ((S, fs), (R, fr), (N, fn)):
            ev = tmpl.replace("{0}", fill)
            state = f"Claim:\n{claim}\n\nEvidence:\n{ev}"
            n += 1
            rid = f"r_{SRC}_{n}"
            meta = {"domain": DOMAIN, "kind": kind, "edit": edit, "item": key}
            if base_id is None:
                base_id = rid
            else:
                meta["twin_of"] = base_id
            rows.append({
                "id": rid, "group_id": gid, "call_id": cid(instr, state, options),
                "split": "train", "track": "STD", "source": SRC, "state": state,
                "qtype": "choice", "instructions": instr, "options": options, "gold": gold,
                "role": "choice", "card": card, "meta": meta,
            })
    return rows


LEAK = ("support", "refute", "not enough", "enough info", "insufficient")


def validate(rows):
    errs = []
    need = {"id", "group_id", "call_id", "split", "track", "source", "state", "qtype",
            "instructions", "options", "gold", "role", "card", "meta"}
    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        errs.append("duplicate ids")
    text2cid, states = {}, Counter()
    for r in rows:
        k = json.dumps([r["instructions"], r["state"], r["options"]], ensure_ascii=False)
        if text2cid.setdefault(k, r["call_id"]) != r["call_id"]:
            errs.append(f"{r['id']}: same text, different call_id")
        states[r["state"]] += 1
    if len(set(text2cid.values())) != len(text2cid):
        errs.append("call_id collision")
    if max(states.values()) > 1:
        errs.append("duplicate states")
    byid = {r["id"]: r for r in rows}
    for r in rows:
        rid = r["id"]
        if set(r) != need:
            errs.append(f"{rid}: keys")
        if (r["split"], r["track"], r["source"], r["qtype"], r["role"]) != \
                ("train", "STD", SRC, "choice", "choice"):
            errs.append(f"{rid}: fixed fields")
        if not rid.startswith(f"r_{SRC}_"):
            errs.append(f"{rid}: id prefix")
        if sorted(r["options"]) != sorted(LABELS) or r["gold"] not in r["options"]:
            errs.append(f"{rid}: options/gold")
        names = [ln[2:].split(": ", 1)[0] for ln in r["card"].split("\n")]
        if names != r["options"]:
            errs.append(f"{rid}: card/options mismatch")
        ev = r["state"].split("\n\nEvidence:\n", 1)[1].lower()
        for w in LEAK:
            if w in ev:
                errs.append(f"{rid}: leak word '{w}' in evidence")
        if "{" in r["state"] or "}" in r["state"]:
            errs.append(f"{rid}: unfilled slot")
        tw = r["meta"].get("twin_of")
        if tw:
            b = byid[tw]
            if b["group_id"] != r["group_id"] or b["gold"] == r["gold"] or b["call_id"] == r["call_id"]:
                errs.append(f"{rid}: bad twin")
    gc = Counter(r["gold"] for r in rows)
    if max(gc.values()) - min(gc.values()) > 0:
        errs.append(f"label imbalance {gc}")
    pc = Counter(r["options"].index(r["gold"]) for r in rows)
    if max(pc.values()) / len(rows) > 0.40:
        errs.append(f"gold position skew {pc}")
    if len({r["instructions"] for r in rows}) < 6:
        errs.append("fewer than 6 phrasings")
    return errs


def main():
    rows = build()
    errs = validate(rows)
    if errs:
        print("VALIDATION FAILED")
        for e in errs:
            print("  ", e)
        sys.exit(1)
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / f"{DOMAIN}.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(OUT / f"{DOMAIN}.blind.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps({k: v for k, v in r.items() if k != "gold"}, ensure_ascii=False) + "\n")
    print(json.dumps({
        "rows": len(rows), "groups": len({r["group_id"] for r in rows}),
        "gold": dict(Counter(r["gold"] for r in rows)),
        "gold_position": dict(sorted(Counter(r["options"].index(r["gold"]) for r in rows).items())),
        "kind_rows": dict(Counter(r["meta"]["kind"] for r in rows)),
        "phrasings": len({r["instructions"] for r in rows}),
        "unique_call_ids": len({r["call_id"] for r in rows}),
    }))


if __name__ == "__main__":
    main()
