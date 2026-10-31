"""T65 constants (approved G0-lite + Opus batch-1b rulings T65-M1, M2, B1-B7; fixed before any pilot)."""
FAMILY = "T65"
GENERATED_ROWS = 600
PAIRS = 300
HEAD_ROWS_MAX = 75
QUESTION_FORM = {"VULN": "T65-Q-VULN", "CWE": "T65-Q-CWE"}
FORM_SLOTS = {"T65-Q-VULN": ["fn"], "T65-Q-CWE": ["fn"]}
DYNAMIC = ("CWEC-22", "CWEC-78", "CWEC-79", "CWEC-89", "CWEC-117", "CWEC-601")
STATIC = ("CWEC-295", "CWEC-327", "CWEC-377")
CLASSES = DYNAMIC + STATIC
CLASS_PAIRS = {"CWEC-22": 36, "CWEC-78": 42, "CWEC-79": 36, "CWEC-89": 36, "CWEC-117": 24, "CWEC-601": 30, "CWEC-295": 30, "CWEC-327": 36, "CWEC-377": 30}
CLASS_WORDS = {"CWEC-22": "path traversal", "CWEC-78": "OS command injection", "CWEC-79": "cross-site scripting", "CWEC-89": "SQL injection", "CWEC-117": "log injection",
               "CWEC-601": "open redirect", "CWEC-295": "disabled certificate verification", "CWEC-327": "weak password hashing", "CWEC-377": "insecure temporary file"}
NEAREST = {"CWEC-22": ("CWEC-78", "CWEC-601", "CWEC-377"), "CWEC-78": ("CWEC-89", "CWEC-22", "CWEC-117"), "CWEC-79": ("CWEC-117", "CWEC-601", "CWEC-89"),
           "CWEC-89": ("CWEC-78", "CWEC-79", "CWEC-117"), "CWEC-117": ("CWEC-79", "CWEC-89", "CWEC-78"), "CWEC-601": ("CWEC-79", "CWEC-22", "CWEC-295"),
           "CWEC-295": ("CWEC-327", "CWEC-601", "CWEC-377"), "CWEC-327": ("CWEC-295", "CWEC-377", "CWEC-89"), "CWEC-377": ("CWEC-22", "CWEC-327", "CWEC-295")}
DS_IDS = tuple("DS-%d" % i for i in range(1, 7))
NS_IDS = tuple("NS-%d" % i for i in range(1, 5))
DECOY_YES_MIN, NOHARD_NO_MIN, NS3_NO_MIN = 0.40, 0.40, 0.10
CLASS_SHARE = (0.05, 0.15)
PAIR_FLOOR = 0.30
DEFS = {"VULN": ("Definitions. A function is flawed (YES) when a value an attacker controls reaches a sensitive operation without a step that neutralises it for that "
                 "operation. A neutralising step counts only if it is made for that kind of operation, is applied to the value that reaches the operation, runs before "
                 "the operation on every path, and its result is used. Answer YES for the flawed function, NO for the sound one."),
        "CWE": ("Definitions. Pick the class of weakness the function shows. The classes are named by words only.")}
POLICY = {"VULN": ["defs_card.t65.vuln"], "CWE": ["defs_card.t65.cwe"]}
RUNNERS_DYNAMIC = ["runner.canary_harness.python"]
FORBIDDEN_IDS = (["CWEC-%d" % n for n in (22, 78, 79, 89, 117, 295, 327, 377, 601)] + ["DS-%d" % i for i in range(1, 7)] + ["NS-%d" % i for i in range(1, 5)] +
                 ["SAN-22a", "SAN-78a", "SAN-79a", "SAN-89a", "SAN-117a", "SAN-601a", "PAY-22", "PAY-78", "PAY-79", "PAY-89", "PAY-117", "PAY-601", "T65-Q-VULN", "T65-Q-CWE",
                  "M-FLOW", "M-HELP", "M-DECOY", "M-LOOK"])
# registered canary payloads (K14): hashed before the first dynamic row; no other payload exists
PAYLOADS = {"PAY-22": "../canary.txt", "PAY-78": "x; echo canarytoken", "PAY-79": "<b>canarytoken</b>", "PAY-89": "' OR '1'='1",
            "PAY-117": "x\nINFO canarytoken", "PAY-601": "https://canary.example/x"}
BENIGN = {"CWEC-22": "readme.txt", "CWEC-78": "hello", "CWEC-79": "hello", "CWEC-89": "1", "CWEC-117": "hello", "CWEC-601": "/home"}
PAY_OF = {"CWEC-22": "PAY-22", "CWEC-78": "PAY-78", "CWEC-79": "PAY-79", "CWEC-89": "PAY-89", "CWEC-117": "PAY-117", "CWEC-601": "PAY-601"}
BANNED_WORDS = ("vuln", "bad", "good", "safe", "unsafe", "secure", "insecure", "tainted", "clean", "evil", "attack", "exploit", "inject", "malicious", "sanitised", "sanitized",
                "trusted", "untrusted", "fix", "flaw", "cwe")

# files shipped WITH a dynamic job (constants, not generated): the sandbox has no /srv tree, so the served root and the canary file are part of the job
FIXTURES = {"CWEC-22": {"srv/files/readme.txt": "public readme", "srv/files/guide.txt": "public guide", "srv/canary.txt": "CANARY-FILE-CONTENT"}}
