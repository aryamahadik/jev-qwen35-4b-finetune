"""Hand-built b-views for the solver B fixtures (text written by hand from the ROW_SCHEMA grammar; no generator involved)."""
from T65.solver_b import rules as R

DEFS_VULN = ("Definitions. A function is flawed (YES) when a value an attacker controls reaches a sensitive operation without a step that neutralises it for that "
             "operation. A neutralising step counts only if it is made for that kind of operation, is applied to the value that reaches the operation, runs before "
             "the operation on every path, and its result is used. Answer YES for the flawed function, NO for the sound one.")
DEFS_CWE = "Definitions. Pick the class of weakness the function shows. The classes are named by words only."
SOURCE_NOTE = "The parameter `%s` is read from the query string of the request."
STATIC_NOTE = "The function is called by the service for each request it handles."
Q = "Is the function fn_x flawed under the definitions above?"
HEADIMPORTS = "import hashlib\nimport html\nimport os\nimport shlex\nimport sqlite3\nimport ssl\nimport subprocess\nimport tempfile\n"


def vuln_view(code, cls, param="p", yes_first=True, notes=True):
    note = (SOURCE_NOTE % param) if cls in R.DYNAMIC else STATIC_NOTE
    parts = [DEFS_VULN] + ([note] if notes else []) + ["Function (mod_x.py):\n" + code.rstrip("\n") + "\n"]
    context = "\n\n".join(p.rstrip("\n") if i == len(parts) - 1 else p for i, p in enumerate(parts))
    texts = ["YES", "NO"] if yes_first else ["NO", "YES"]
    options = [{"letter": "AB"[i], "text": t} for i, t in enumerate(texts)]
    opt_text = "\n".join("%s) %s" % (o["letter"], o["text"]) for o in options)
    return {"row_id": "b-fixture", "head": "VULN", "sub_block": cls, "rendered": {"context": context, "question": Q, "options_text": opt_text,
            "text": context + "\n\n" + Q + "\n\n" + opt_text}, "options": options,
            "witness_inputs": {"head": "VULN", "class_group": "dynamic" if cls in R.DYNAMIC else "static"}}


def cwe_view(code, order=None):
    words = [R.CLASS_WORDS[c] for c in order] if order else ["path traversal", "OS command injection", "SQL injection", "log injection"]
    options = [{"letter": "ABCD"[i], "text": w} for i, w in enumerate(words)]
    opt_text = "\n".join("%s) %s" % (o["letter"], o["text"]) for o in options)
    context = DEFS_CWE + "\n\nFunction (mod_x.py):\n" + code.rstrip("\n")
    return {"row_id": "b-fixture-c", "head": "CWE", "sub_block": "CWE", "rendered": {"context": context, "question": "Which weakness class?", "options_text": opt_text,
            "text": context + "\n\nWhich weakness class?\n\n" + opt_text}, "options": options, "witness_inputs": {"head": "CWE", "class_group": None}}
