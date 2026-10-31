"""T66 constants (approved G0-lite + Opus batch-1b rulings T66-M1, M2, B1-B9; fixed before any pilot)."""
FAMILY = "T66"
GENERATED_ROWS = 800
HEAD_ROWS = {"MERGE": 300, "SEMVER": 300, "MSG": 200}
QUESTION_FORM = {"MERGE": "T66-Q-MERGE", "SEMVER": "T66-Q-SEMVER", "MSG": "T66-Q-MSG"}
FORM_SLOTS = {"T66-Q-MERGE": ["stem"], "T66-Q-SEMVER": ["api"], "T66-Q-MSG": ["stem"]}
LABELS = {"MERGE": ("YES", "NO"), "SEMVER": ("BREAKING", "SAFE"), "MSG": ("YES", "NO")}
LANGS = ("python",)                                  # javascript / typescript / go / bash: LanguagePending until the L-0 image record is appended (T66-B9)
LANG_SHARE_TARGET = {"python": 0.72, "javascript": 0.10, "go": 0.10, "bash": 0.08}
PAIR_FLOOR = {"MERGE": 0.60, "SEMVER": 0.40, "MSG": 1.0, "FAMILY": 0.30}
REUSE_PER_MODULE_PER_HEAD, REUSE_PER_MODULE = 4, 6
BIN_AUC_MAX, BIN_UPPER_MAX = 0.55, 0.60
RK_NO_SHARE = {"RK1+RK2_max": 0.25, "RK3+RK4_min": 0.25, "RK7_min": 0.40, "RK8_max": 0.10}
CF_SHARE = (0.08, 0.20)
SV_MIN_SHARE, SV_MAX_BREAKING_SHARE = 0.03, 0.20
TRIVIAL_NO_MIN = 0.25
HARD_OVERLAP_MIN = 0.30
DEFS = {
    "MERGE": ("Definitions. A merge conflict shows the file with our side, the base and their side between markers. The tests of side A and side B are shown. "
              "Answer YES if every test of both files passes on the proposed resolved file, otherwise NO."),
    "SEMVER": ("Definitions. The old and the new version of an API are shown with the caller snippets written against the old API. Answer BREAKING if at least one "
               "of the shown callers fails on the new API, otherwise SAFE. Only the shown callers count."),
    "MSG": ("Definitions. A commit message describes a diff when it describes the one change that alters what the code does; a message that describes only a "
            "formatting, comment or docstring edit of the same diff does not. Answer YES if the message describes this diff, otherwise NO."),
}
POLICY = {"MERGE": ["defs_card.t66.merge"], "SEMVER": ["defs_card.t66.semver"], "MSG": ["defs_card.t66.message"]}
CARRIERS = {"MERGE": ["CONFLICT_VIEW", "RESOLUTION", "SIDE_TEST_A", "SIDE_TEST_B", "TEST_FILE", "SRC_FILE", "QUESTION_FORM"],
            "SEMVER": ["API_PAIR", "PROGRAM_PAIR", "CALLER_SNIPPETS", "BUMP_FIELD", "TEST_FILE", "SRC_FILE", "QUESTION_FORM"],
            "MSG": ["DIFF", "COMMIT_MESSAGE", "QUESTION_FORM"]}
RUNNERS = ["runner.pytest", "runner.python_isolated"]
FORBIDDEN_IDS = (["CF-%d" % i for i in range(1, 8)] + ["RK%d" % i for i in range(1, 9)] + ["SV-C%d" % i for i in range(1, 13)] + ["CH-%d" % i for i in range(1, 11)] +
                 ["CH-trivial", "T66-Q-MERGE", "T66-Q-SEMVER", "T66-Q-MSG", "M-SEMB", "M-ORDER", "M-FAR", "M-LOOK", "M-BUMP", "M-MULTI", "M-OVL"])
