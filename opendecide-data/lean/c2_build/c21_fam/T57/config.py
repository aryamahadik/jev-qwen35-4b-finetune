"""T57 PATCH-VERDICT constants (approved G0-lite + Opus rulings C1, C2, (a)-(g); fixed before any pilot)."""
FAMILY = "T57"
ROWS_TOTAL = 3000

HEADS = ("VERDICT", "BEST4", "TESTSEL", "LOCALISE")
HEAD_ROWS = {"VERDICT": 1000, "BEST4": 800, "TESTSEL": 400, "LOCALISE": 800}
HEAD_SHARE = {h: n / 3000.0 for h, n in HEAD_ROWS.items()}
QUESTION_FORM = {"VERDICT": "T57-Q-VERDICT", "BEST4": "T57-Q-BEST4", "TESTSEL": "T57-Q-TESTSEL", "LOCALISE": "T57-Q-LOCALISE"}
DEFS_CARD = {"VERDICT": "defs_card.t57.verdict", "BEST4": "defs_card.t57.best4", "TESTSEL": "defs_card.t57.testsel",
             "LOCALISE": "defs_card.t57.localise"}
TASK_FRAME_FORM = "T57-TC-FRAME"          # wording pool form for the task-card frame (not a guard category)
COMMENT_FORMS = ("T57-CM-NEUTRAL", "T57-CM-FIXED")   # comment pools: neutral remark / assertive "fixed ..." claim

LANG_SPLIT = {  # per head: python, js+ts, go, bash (rows)
    "VERDICT": (750, 90, 80, 80), "BEST4": (600, 72, 64, 64), "TESTSEL": (300, 36, 32, 32), "LOCALISE": (600, 72, 64, 64)}
LANG_SHARE = {"python": 0.72, "javascript": 0.06, "typescript": 0.04, "go": 0.09, "bash": 0.09}      # slack inside the cap (<= 0.75) and floors (>= 0.08)
PYTHON_CAP = 0.75

CORRECT_RATE_RANGE = (0.40, 0.60)
REASON_MIX = {"PARTIAL": 0.40, "REGRESSION": 0.35, "NOFIX": 0.25}
NOFIX_MAX, REASON_MAX = 0.25, 0.45
LETTER_TOL = 0.03
ALTFIX_MIN_OF_BEST4_CORRECT = 0.30
PAIR_FLOOR, NEARMISS_PAIR_FLOOR, TWIN_OR_ALTFIX_FLOOR = 0.30, 0.15, 0.10
DECOY_SHARE_OF_INCORRECT = 0.15
COMMENT_RATE = 0.30
COMMENT_GAP_MAX = 0.03
RENAME_TWIN_SHARE = 0.35
ORDER_COPIES = 0.20
WITH_OUTPUTS_COPIES = 0.25
REUSE_PER_MODULE_PER_HEAD, REUSE_PER_MODULE = 4, 8
MAX_DIFF_LINES = 15
CAND_PER_BEST4 = (4, 5)
MUTANTS_PER_LOCALISE = 2.5

# gate b (strength): T_s fixed by the 50-module pilot under the rule written before the pilot
TS_PROPOSAL, TS_FLOOR = 0.90, 0.80
TS_PILOT_MODULES = {"python": 38, "js+ts": 4, "go": 4, "bash": 4}
TS_PILOT_SHARE_REQUIRED = 0.70
TS_NONPY_EXTENSION = 20
MODULE_STRENGTH_PASS_SHARE = 0.85          # at least 85% of generated modules clear T_s
UNDECIDED_MAX = 0.25                       # > 25% undecided mutants drops the module
MIN_STRENGTH_MUTANTS = 6                   # fewer decidable mutants than this: strength is not measurable, module dropped
STRENGTH_POOL_SIZE = 16

WITNESS_RUNS_SUITE = 2                     # sandbox default for suites (the T57 G0-lite does not ask for 3)
DOMAIN_MIN, DOMAIN_MAX = 25, 5000
TOKEN_MEAN_MAX, TOKEN_CAP, TOKEN_OVER_1024_MAX = 800, 1536, 0.10
OUTPUT_CAP_TOKENS = 256
YIELD_FLOOR = 0.80

BIN_AUC_MAX, BIN_UPPER_MAX = 0.55, 0.60
K4_ACC_MAX, K4_UPPER_MAX = 0.28, 0.31
K3_ACC_MAX, K3_UPPER_MAX = 1 / 3 + 0.03, 1 / 3 + 0.06          # reason head (k = 3): 36.3% / 39.3%

LANGUAGES = ("python", "javascript", "typescript", "go", "bash")
RUNNER = {"python": "runner.pytest", "javascript": "runner.node_test", "typescript": "runner.node_test", "go": "runner.go_test",
          "bash": "runner.bash_driver"}
CARRIERS = {
    "VERDICT": ["TASK_CARD", "SRC_FILE", "VISIBLE_TEST", "PATCH_DIFF"],
    "BEST4": ["TASK_CARD", "SRC_FILE", "VISIBLE_TEST", "PATCH_DIFF", "OPTIONS"],
    "TESTSEL": ["TASK_CARD", "SRC_FILE", "PATCH_DIFF", "OPTIONS"],
    "LOCALISE": ["TASK_CARD", "SRC_FILE", "VISIBLE_TEST", "OPTIONS"],
}
PINS_PENDING = True
CLASSES = ("NOFIX", "REGRESSION", "PARTIAL", "CORRECT")          # precedence order of the first rule that applies
