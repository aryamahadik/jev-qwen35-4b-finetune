"""T63 constants (from the approved G0-lite and its Opus batch-1b rulings; every value fixed before any pilot)."""
FAMILY = "T63"
GENERATED_ROWS = 1200                      # NEAR 550 + EXISTS 540 (EX-A 290, EX-B 250) + LIC 110 (MAL 1,000 is an L-R dataset slice, NOT built here: T63-M3)
# Opus ruling Q5 (18 Oct, before any pool rows): the hashed Opus table holds only 40 INCOMPATIBLE cells and a cell is used once, so LIC shrinks 200 -> 110 and the freed 90 rows go
# to the seeded blocks (NEAR +50, EX-A +40: EX-A1 160, EX-A2 130). EX-B stays 250. The family stays 1,200 rows. No bar changes.

HEADS = ("NEAR", "EXISTS", "LIC")
BLOCK_ROWS = {"NEAR": 550, "EX-A1": 160, "EX-A2": 130, "EX-B": 250, "LIC": 110}
PILOT_ROWS = {"NEAR": 275, "EX-A": 145, "EX-B": 125, "LIC": 55}      # pilot = 600 (T63-B5 / GV10, amended by Opus ruling Q5)
QUESTION_FORM = {"NEAR": "T63-Q-NEAR", "EXISTS": "T63-Q-EXISTS", "LIC": "T63-Q-LIC"}
FORM_SLOTS = {"T63-Q-NEAR": ["pkg", "registry"], "T63-Q-EXISTS": ["name", "scope"], "T63-Q-LIC": ["dep", "project"]}

# --- NEAR (section 2.1) --------------------------------------------------------------------------------------------------------
NM_T = ("NM-T1", "NM-T2", "NM-T3", "NM-T4", "NM-T5", "NM-T6", "NM-T7", "NM-T8")
NM_R = ("NM-R1", "NM-R2", "NM-R3", "NM-R4")
AGE = ("A0", "A1", "A2", "A3")             # < 30 days / < 1 year / 1-4 years / > 4 years (strict class order)
DL = ("D0", "D1", "D2")
ESTABLISHED = ("A2", "A3")                 # established = age class >= A2 AND downloads class D2
ECOSYSTEMS = ("pip", "npm", "cargo", "go")
ECO_PROG = {"pip": "prog.pip", "npm": "prog.npm", "cargo": "prog.cargo", "go": "prog.go"}   # yarn is on the family list, unused by default
YES_SHARE = (0.45, 0.55)
NM_T_YES_SHARE = (0.05, 0.25)              # each of NM-T1..NM-T8 as a share of YES
NM_R4_MAX = 0.08                           # unrelated NO rows
NO_NEAR_MIN = 0.92                         # NO rows carrying NM-R1..NM-R3
MAX_TABLE_ENTRIES = 14
SNAPSHOT_FORMATS = ("TBL-CSV", "TBL-JSON", "TBL-KV", "TBL-PIPE", "TBL-TSV")

# --- EXISTS (section 2.2) ------------------------------------------------------------------------------------------------------
EX_N = ("EX-N1", "EX-N2", "EX-N3", "EX-N4", "EX-N5")
EX_N_DEFINED = {"EX-A1": ("EX-N2", "EX-N4", "EX-N5"), "EX-A2": ("EX-N1", "EX-N3", "EX-N4", "EX-N5"), "EX-B1": ("EX-N1", "EX-N4", "EX-N5"),
                "EX-B2": ("EX-N1", "EX-N4", "EX-N5")}
EX_N4_MAX = 0.30
EX_N_MAX = 0.40
EX_N_MIN = 0.15                            # N1, N2, N3, N5 each >= 15% of the NO rows of sub-blocks where defined
EX_B_LANG_ROWS = {"python": 150, "node": 50, "go": 50}
EX_B_LANG_SHARE = {"python": 0.60, "node": 0.20, "go": 0.20}
EX_LIST_MAX = 40

# --- LIC (section 2.3) ---------------------------------------------------------------------------------------------------------
LIC_LABELS = ("COMPATIBLE", "REVIEW", "INCOMPATIBLE")
LIC_ROWS = {"COMPATIBLE": 38, "REVIEW": 38, "INCOMPATIBLE": 34}             # kept quota (Opus ruling Q5): 34.5 / 34.5 / 30.9%
LIC_DRAW = {"COMPATIBLE": 44, "REVIEW": 44, "INCOMPATIBLE": 40}             # at most this many cells drawn per label (15% oversample, capped: the table has 40 INCOMPATIBLE cells)
LIC_USE = {"LC-USE-1": "vendored source copy", "LC-USE-2": "static link", "LC-USE-3": "dynamic link", "LC-USE-4": "separate process",
           "LC-USE-5": "dev-time tool only"}
LIC_DIST = {"LC-DIST-1": "distributed to others", "LC-DIST-2": "internal only", "LC-DIST-3": "offered as a network service"}
LIC_TEMPLATE_ID = "t63.lic.v1"             # the LIC template id (K10-F: a constant of the format draw)
LIC_CARD_LAYOUT = "lic.card.v1"            # the K10 format features (card layout, field order, wording id): layout and order are fixed by ROW_SCHEMA.md (solver B reads them), so only the
LIC_FIELD_ORDER = "dep,project,use,dist"   # wording id varies, and it is a seeded random draw that never sees the label (Opus ruling Q7a and its follow-up)
LIC_PAIR_MIN = 0.30
LIC_AXIS_FLIP_MIN = 0.50                   # >= 50% of one-axis-flip pairs flip on usage mode or distribution (not on a licence id)
LIC_MIXED_PAIR_MIN = 0.40                  # >= 40% of rows from (dependency, project) pairs whose 15 mode x distribution cells hold >= 2 labels

# --- sizes / ladder / gates -----------------------------------------------------------------------------------------------------
PAIR_FLOOR = {"NEAR": 0.50, "EXISTS": 0.30, "LIC": 0.30, "FAMILY": 0.30}
REUSE_PER_GROUP = 3                        # <= 3 rows per snapshot / library history, <= 1 per licence cell
DEV_SHARE = 0.10
BIN_AUC_MAX, BIN_UPPER_MAX = 0.55, 0.60
FORMAT_ONLY_BAL_ACC, FORMAT_ONLY_UPPER = 1 / 3.0 + 0.03, 1 / 3.0 + 0.06

# names (guard categories) per head; every name must be on manifest v1.2 AND on T63's own list
POLICY = {"NEAR": ["card.t63.registry_resolve", "defs_card.t63.near"], "EXISTS": ["defs_card.t63.exists"], "LIC": ["defs_card.t63.licence"]}
CARRIERS = {"NEAR": ["SNAPSHOT_TABLE", "QUERY_LINE", "QUESTION_FORM"],
            "EXISTS": ["QUESTION_FORM"],
            "LIC": ["LICENCE_CARD", "QUESTION_FORM"]}
LANG_OF_ECO = {"pip": "python", "npm": "javascript", "cargo": None, "go": "go"}

# internal ids that must never reach a rendered row
FORBIDDEN_IDS = (list(NM_T) + list(NM_R) + list(EX_N) + ["EX-A1", "EX-A2", "EX-B1", "EX-B2", "T63-Q-NEAR", "T63-Q-EXISTS", "T63-Q-LIC",
                 "T63-LIC-TABLE", "SEG-GOLD"] + list(LIC_USE) + list(LIC_DIST) +
                 ["M-PLAUS", "M-XREG", "M-EDIT", "M-SIB", "M-VER", "M-CELL"])

# --- ladder (K12), Opus ruling Q7b: every LIC row is L3 (M-CELL HIGH on the hashed table: every cell is one axis from a flip; L4 needs two HIGH mechanisms), so NEAR and EXISTS
# plan their levels to land the FAMILY composition L1 20 / L2 30 / L3 30 / L4 20 with LIC's share of the family all at L3. No narrower distance measure is invented for LIC.
LADDER_TARGET = {"L1": 0.20, "L2": 0.30, "L3": 0.30, "L4": 0.20}
LIC_SHARE = BLOCK_ROWS["LIC"] / float(GENERATED_ROWS)
NON_LIC_LEVEL_WEIGHTS = tuple((LADDER_TARGET[lv] - (LIC_SHARE if lv == "L3" else 0.0)) / (1.0 - LIC_SHARE) for lv in ("L1", "L2", "L3", "L4"))
