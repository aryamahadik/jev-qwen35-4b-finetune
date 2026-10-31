"""packs-2 shared pools (Claude-written seeds; no third-party text). Used by build_packs.py.

Everything here is invented or generic vocabulary. Person names are common given names and surnames combined by
program, so every full name is an invented person.
"""

GIVEN = """Aaliyah Abel Ada Adaeze Aditi Adrian Agnes Ahmed Aiko Alba Alejandro Amara Ambrose Amelie Anahi Anders Anjali
Ansel Arjun Astrid Aurelio Ayesha Baptiste Beatriz Bettina Bjorn Bongani Bridget Bruno Calla Camille Caspian Celeste
Chidi Chioma Clement Cormac Dagny Dalia Damaris Dariusz Delphine Desmond Dmitri Dorothea Eamon Edda Efua Elio Elodie
Emeka Esme Esteban Eszter Fabian Farah Fatou Felix Fenna Fiona Florin Gaspard Gemma Gideon Gisela Goran Greta Gunnar
Hadley Hamza Hana Harriet Hector Helga Hiro Hugo Ilse Imogen Ines Isak Ivo Jalen Jasmin Jasper Joaquin Jonah Josefa
Jude Junia Kaito Kalinda Kamal Keziah Kiran Klara Kofi Lars Leila Lennox Leonie Lucan Ludmila Lyra Magnus Malik Mariam
Marisol Matteo Maeve Mehmet Mireille Moana Nadia Naoki Nathaniel Neha Niamh Nikolai Noor Odette Oksana Olumide Orla
Osman Pablo Paloma Petra Priya Quentin Rafael Ravi Renata Rhiannon Rohan Rosalind Rufus Sabine Saoirse Selin Senna
Silas Solveig Soren Sunniva Tamsin Tariq Teodor Thandiwe Theo Tobias Ulla Uriel Valentina Vesna Viggo Wanjiru Wendell
Xiomara Yara Yusuf Zainab Zeno Zofia""".split()

SURNAME = """Abernathy Achterberg Adeyemi Ahlgren Alcantara Amundsen Antonelli Arkwright Ashdown Babatunde Balogun
Barrowclough Bastide Beaumont Bekele Bellweather Bergstrom Blackwood Bocanegra Brannigan Brightwater Calloway Carvalho
Castellanos Chakraborty Chen-Whitlock Clairmont Coldwell Corriveau Dabrowski Dalgleish Delacroix Desai Drummond Duvall
Eberhardt Ekwueme Ellingsen Escobedo Farnsworth Fennimore Figueroa Fitzwilliam Fonseca Gallagher Garnier Gethin Ghosh
Goldfarb Gonsalves Greenhalgh Gutierrez Haddad Halvorsen Hartigan Hasegawa Hawthorne Hendricks Holloway Hrabal Iwasaki
Jablonski Jaramillo Jefferies Kaczmarek Kamara Karlsson Kavanagh Kettering Kowalczyk Kuznetsova Lachance Lambrecht
Langford Lindqvist Lockhart Lozano Macaulay Mahlangu Marchetti Masterson Mbeki Mendelsohn Meriwether Montague Moreau
Mwangi Nakamura Navarro Nwachukwu Oakes Ogunleye Okafor Oyelaran Pacheco Pemberton Pettersen Quayle Quintero Radcliffe
Ramaswamy Rasmussen Redfern Rinaldi Rosenthal Rutherford Sakamoto Salgado Sandoval Schaefer Sekibo Shackleton Sorensen
Stanhope Strickland Szabo Takahashi Tanaka-Reyes Thackeray Thornbury Toivonen Trevanion Underwood Valderrama Vance
Vasquez Verhoeven Wainwright Wakefield Wexford Whitcombe Wojcik Yamamoto Yardley Yilmaz Zabala Zelenko Zimmerman""".split()

# Syllables for invented words (jargon candidates and organisation-name stems). Program-combined, then filtered.
ONSETS = ["b", "br", "c", "cr", "d", "dr", "f", "fr", "g", "gr", "h", "j", "k", "kr", "m", "n", "p", "pr", "qu",
          "r", "s", "sk", "st", "t", "tr", "v", "w", "z", "th", "ch", "sh", "pl", "bl", "gl", "fl", "sp"]
NUCLEI = ["a", "e", "i", "o", "u", "ai", "ea", "ou", "y", "ee", "oa", "au"]
CODAS = ["", "", "", "n", "r", "s", "t", "m", "nd", "rt", "sk", "x", "ck", "lt", "rn", "mp", "v"]

# Morphology hints an invented word must not carry (F10: no "-phobia", "mal-", "-itis" style hints).
BANNED_AFFIX_PATTERNS = [r"^mal", r"^mis", r"^un", r"^non", r"^dis", r"^anti", r"^pre", r"^post", r"^sub", r"^super",
                         r"^over", r"^under", r"^hyper", r"^hypo", r"^pseudo", r"^neo", r"^re", r"^de", r"^in", r"^im",
                         r"^ir", r"^il", r"itis$", r"phobia$", r"ology$", r"ism$", r"ist$", r"less$", r"ness$",
                         r"ment$", r"tion$", r"sion$", r"able$", r"ible$", r"ful$", r"ous$", r"ish$", r"ize$",
                         r"ise$", r"ity$", r"cide$", r"phile$", r"oid$", r"osis$", r"emia$", r"algia$", r"ectomy$",
                         r"gram$", r"graph$", r"scope$", r"meter$", r"ward$", r"wise$", r"ly$", r"er$", r"est$",
                         r"ed$", r"ing$", r"s$"]

# Generic inert attributes (never decisive in any pack rule). Each pack adds its own pack-specific inert items too.
GENERIC_INERT = [
    "folder_colour | cat | blue; green; grey; yellow; orange",
    "printed_copies | int | 1..6 copies",
    "intake_weekday | cat | Monday; Tuesday; Wednesday; Thursday; Friday",
    "form_font | cat | serif; sans; monospace",
    "staff_badge_colour | cat | teal; maroon; slate; amber",
    "meeting_room | cat | Room 2; Room 4; Room 7; Room 9",
    "envelope_size | cat | letter; legal; large",
    "cover_sheet_style | cat | plain; striped; boxed",
    "desk_number | int | 1..24 desks",
    "notebook_page | int | 1..180 pages",
    "pen_colour | cat | black; blue; green",
    "file_tab_position | cat | left; centre; right",
    "weather_at_intake | cat | sunny; cloudy; rainy; windy",
    "lobby_screen_slide | int | 1..12 slides",
    "parking_level | cat | P1; P2; P3; P4",
    "coffee_order_of_clerk | cat | espresso; latte; tea; water",
    "staple_count | int | 1..5 staples",
    "fax_cover_page_count | int | 1..3 pages",
    "printer_tray | cat | tray 1; tray 2; manual feed",
    "hallway_mural_theme | cat | birds; rivers; mountains; city",
]

# Base action set (F12 closed action set; each pack adds its own domain actions). lexeme = synonyms.
BASE_ACTIONS = "look up = find, retrieve; create = open, start; update = edit, change; cancel = call off; " \
               "attach = add file; notify = alert, message; export = download; assign = allocate"

# Unit synonyms (F12: unit words and synonyms come only from the pack lexicon; no currency symbols).
UNIT_SYNONYMS = {
    "days": ["day"], "business days": ["business day", "working days"], "hours": ["hour", "hrs"],
    "minutes": ["minute", "mins"], "weeks": ["week"], "months": ["month"], "years": ["year"],
    "miles": ["mile"], "kilometres": ["kilometre", "km"], "percent": ["per cent", "pct"],
    "dollars": ["dollar", "USD"], "euros": ["euro", "EUR"], "pounds sterling": ["pound", "GBP"],
    "points": ["point", "pts"], "nights": ["night"], "guests": ["guest"], "seats": ["seat"],
    "pages": ["page"], "copies": ["copy"], "items": ["item"], "rooms": ["room"], "units": ["unit"],
    "credits": ["credit"], "sessions": ["session"], "visits": ["visit"], "people": ["persons"],
    "square feet": ["sq ft"], "square metres": ["sq m"], "kilograms": ["kilogram", "kg"],
    "tables": ["table"], "covers": ["cover"], "claims": ["claim"], "employees": ["employee", "staff members"],
    "students": ["student"], "courses": ["course"], "documents": ["document"], "entries": ["entry"],
    "lines": ["line"], "trips": ["trip"], "desks": ["desk"], "slides": ["slide"], "staples": ["staple"],
}

# Greetings, sign-offs and header patterns for register prose (F11); {org} and {desk} are filled per pack.
GREETINGS = ["Hello {desk} team,", "Good morning to the team,", "Hi all,", "Dear colleagues,", "Team,", "Good afternoon,"]
SIGNOFFS = ["Thanks, {desk}", "Regards, {org}", "Best, {desk}", "With thanks, the {desk}", "Kind regards,"]
HEADERS = ["{org} | {doc}", "{doc} - {desk}", "INTERNAL: {doc}", "{org} {doc} (working copy)", "{doc} | {scope}"]

# Words that look affixal but whose affix does not negate the stem (global exception list for the affix lint).
NOT_NEG_AFFIX = set("""invoice income discount interest install inform information index input inspect inspection
intake insurance insured insurer interview internal into invest investment issue unit united universal until under
understand understood union unique update upload usual disburse disbursement dispatch display distance district
dispute discuss discussion distribute distribution disclose disclosure dismiss dismissal dissolve dissolution
imprint import important improve improvement impact impose impound include included inclusion incident increase
increment indemnity independent indicate industry infant initial initiate injury inner inquiry insert inside insight
instance instant instead institute instruct instruction instrument intend intent interim intern interpreter interval
invite invitation involve iron irrigation islander island illustrate illustration image immediate immigration
mission missing misc nonprofit nonstop pointless regardless timeless unless endless wireless homeless boundless
dispense dispenser dissertation discharge discipline disciplinary discretion discretionary
disposal dispose dispatcher distinct inventory inventor invoiced invoicing invest instalment installment inbound
indoor incoming inline incumbent incurred incur inherit inheritance injection inmate innovation inpatient intensive
interstate intranet intramural imaging infusion
including indexed informed inspected installed invoices
individual insure intensity indemnify
ireland units unite informational inland disclosed importance important""".split())

# F7 filler Booleans (v1.1; Z02, U01): office and building trivia named like factors (affirmative, no banned stem),
# event = something that happened, state = a condition as of the report date. Each pack draws 5 + 5 by program
# (fixed seed), skipping any item that shares a word stem with the pack's rubric concept sets.
FILLER_EVENTS = """lobby ferns watered; window blinds cleaned; group photo taken; coffee machine descaled;
printer toner swapped; carpet vacuumed; fire drill held; fridge emptied; mural repainted; doormat replaced;
light bulb changed; noticeboard tidied; recycling bins emptied; table lamp repaired; kettle replaced;
welcome poster hung; umbrella stand moved; fern repotted; whiteboard wiped; mailroom shelves dusted;
birthday cake shared; hallway clock reset; air vents dusted; cabinet hinges oiled; window boxes filled;
flag raised; car park swept; bike rack painted; vending machine restocked; office radio retuned;
logo sign polished; stair rail painted; spare chairs stacked; reception sofa cleaned; aquarium cleaned;
holiday lights hung; trophy shelf dusted; carpet tiles swapped; bookshelf assembled; wall calendar changed;
ceiling fan fixed; water cooler refilled; corkboard pinned; window cleaner visited; gardener visited;
lift mirror polished; entrance mat shaken; pigeon nest moved; pantry restocked with tea; hedge trimmed;
garden bench painted; snow shovelled from the steps; skylight cleaned; cuttings potted; jigsaw finished;
clock battery changed; leaflet rack dusted; lobby piano tuned; office cat fed; bird feeder filled""".replace("\n", " ")
FILLER_STATES = """radio playing; heating switched on; ceiling fan running; lobby music on; hallway lamps dimmed;
fan heater humming; aquarium lit; flower vase on the counter; office dog present; bowl of mints at reception;
screen saver showing birds; hallway rug striped; wall clock fast; blinds half closed; potted fern thriving;
café menu pinned up; coat rack crowded; umbrella stand by the entrance; sun on the front counter;
lobby fountain running; door wreath hung up; chalkboard sign outside; paper lanterns up; kettle warm;
framed map on the wall; canteen soup hot; garden bench green; hallway smelling of coffee; lift music playing;
window sill dusty; carpet freshly shampooed; ivy trailing; lobby television on; table football out;
puzzle box on the shelf; bunting across the hallway; candle jar on the sill; pot of pens by the till;
painting crooked; tea towels drying; jacket on the chair; rain on the windows; ceiling tile stained;
vending machine humming; balloon tied to a chair; lunch smells in the corridor""".replace("\n", " ")
