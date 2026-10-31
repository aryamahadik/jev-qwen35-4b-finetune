"""T42c constants (from the approved G0-lite and its Opus rulings; values are fixed before any pilot)."""
FAMILY = "T42c"
ROWS_TOTAL = 3000

HEADS = ("OUT4", "EQV2", "TFAIL2")
HEAD_SHARE = {"OUT4": 0.40, "EQV2": 0.30, "TFAIL2": 0.30}
QUESTION_FORM = {"OUT4": "T42c-Q-OUT4", "EQV2": "T42c-Q-EQV2", "TFAIL2": "T42c-Q-TFAIL2"}

# language shares of the 3,000 rows: Python <= 75%; JS/TS >= 8% together (TS only if the Node type-stripping self-test
# passes, otherwise its share folds into JS); Go >= 8%; bash >= 8%
LANG_SHARE = {"python": 0.72, "javascript": 0.06, "typescript": 0.04, "go": 0.09, "bash": 0.09}      # slack inside the cap (<= 0.75) and floors (>= 0.08)
LANG_FLOOR = {"javascript+typescript": 0.08, "go": 0.08, "bash": 0.08}
PYTHON_CAP = 0.75

STEP_BINS = ("lt10", "mid", "gt40")                       # <10, 10-40, >40 executed steps
STEP_BIN_SHARE = {"lt10": 0.30, "mid": 0.40, "gt40": 0.30}
STEP_BIN_FLOOR = 0.15

OUT4_EXC_SHARE = 0.25                                       # 20-30% overall, >= 15% in each non-Python language
OUT4_EXC_RANGE = (0.20, 0.30)
OUT4_EXC_NONPY_FLOOR = 0.15
OUT4_LETTER_TOL = 0.03
YES_RATE_RANGE = (0.40, 0.60)
PAIR_FLOOR = 0.30
INVARIANT_FLOOR = 0.15
NEARMISS_FLOOR = 0.10
EQ_YES_MAX_SHARE = 0.30                                      # no construction above 30% of YES rows
MUT_MAX_SHARE_OF_NO = 0.25                                   # no mutator class above 25% of NO rows
HARD_NO_MIN_SHARE = 0.20                                     # >= 20% of NO rows differ on <= 2% of the domain
HARD_NO_MAX_DIFF = 0.02
DISTRACTOR_KIND_MAX_SHARE = 0.60
CUSTOM_EXC_MAX_SHARE = 0.20                                  # custom exception classes <= 20% of exception rows
ORDER_INVARIANCE_COPIES = 0.20                               # extra copies with a random non-identity permutation
REUSE_PER_MODULE_PER_HEAD = 4
REUSE_PER_MODULE = 6
YIELD_FLOOR = 0.80
CANDIDATES_PER_KEPT = 1.5
WITNESS_RUNS = 3
DOMAIN_MIN, DOMAIN_MAX = 25, 5000
ASSERTIONS_RANGE = (1, 4)
TOKEN_MEAN_MAX, TOKEN_CAP, TOKEN_OVER_1024_MAX = 800, 1536, 0.10
WORDINGS_MIN, WORDING_MAX_SHARE = 50, 0.02

# probe bars (PRE-FREEZE KILL gates): binary AUC <= 0.55 with 97.5th-percentile bound <= 0.60; k = 4 accuracy <= 28%,
# bound <= 31%. Fixed here, before any pilot.
BIN_AUC_MAX, BIN_UPPER_MAX = 0.55, 0.60
K4_ACC_MAX, K4_UPPER_MAX = 0.28, 0.31

LANGUAGES = ("python", "javascript", "typescript", "go", "bash")

RUNNER_OF_LANG = {"python": "runner.python_isolated", "javascript": "runner.node_test", "typescript": "runner.node_test",
                  "go": "runner.go_test", "bash": "runner.bash_posix_test"}
CARRIERS = {"OUT4": ["SRC_FILE", "CALL_SPEC", "OPTIONS", "QUESTION_FORM"],
            "EQV2": ["SRC_FILE", "PROGRAM_PAIR", "DOMAIN_DECL", "QUESTION_FORM"],
            "TFAIL2": ["SRC_FILE", "TEST_FILE", "QUESTION_FORM"]}

# the toolchain patch versions / digests are copied from the L-0 image record into the family record before the first
# non-Python row ("pins go into the G0-lites before any non-Python row"); candidates (unreviewed) are in
# c21_infra/sandbox/pins.env. Nothing here invents a pin.
PINS_PENDING = True
