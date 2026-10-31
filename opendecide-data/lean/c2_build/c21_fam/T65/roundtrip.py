"""T65 render round trip (generator-side; NOT solver B): the function text parses (ast.parse, parse only), contains no CVE / GHSA / NVD string and no CWE number
(guard F2, K9), no banned label word in OUR identifiers or comments (K5; standard-library API names are exempt), and the stored witness is complete."""
import ast
import io
import re
import tokenize

from . import config as C

STD = {"os", "path", "join", "basename", "html", "escape", "shlex", "quote", "subprocess", "run", "shell", "capture_output", "text", "stdout", "sqlite3", "connect", "cursor",
       "execute", "fetchall", "open", "read", "close", "strip", "lower", "replace", "lstrip", "len", "ssl", "create_default_context", "check_hostname", "verify_mode",
       "CERT_NONE", "CERT_REQUIRED", "minimum_version", "TLSVersion", "TLSv1_2", "hashlib", "md5", "sha256", "pbkdf2_hmac", "hexdigest", "encode", "hex", "tempfile", "mktemp",
       "mkstemp", "mkdtemp", "gettempdir", "suffix", "ValueError", "password", "filename", "echo", "x", "c"}
F2 = re.compile(r"\b(CVE-\d+|GHSA-\w+|NVD)\b|\bCWE[-_ ]?\d+", re.I)


def identifiers(src):
    tree = ast.parse(src)
    ids = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.FunctionDef):
            ids.add(n.name)
            ids.update(a.arg for a in n.args.args)
        elif isinstance(n, ast.Name):
            ids.add(n.id)
        elif isinstance(n, ast.Attribute):
            ids.add(n.attr)
        elif isinstance(n, ast.arg):
            ids.add(n.arg)
    return ids


def check(rec):
    bad = []
    spec = rec["spec"]
    src = spec["source_text"]
    try:
        ids = identifiers(src)
    except SyntaxError:
        return ["syntax"]
    if F2.search(rec["rendered"]["text"]):
        bad.append("F2")
    for i in ids - STD:
        if any(w in i.lower() for w in C.BANNED_WORDS):
            bad.append("banned_word:" + i)
    if any(t.type == tokenize.COMMENT for t in tokenize.generate_tokens(io.StringIO(src).readline)):
        bad.append("comment_present")                      # generated code carries no comments (parity by construction, K5)
    if rec["head"] == "VULN" and spec["cls"] in C.DYNAMIC:
        w = spec["witness"]
        if not w or not w["ok"] or (w["runs"] or 0) < 3 or w["payload_id"] != C.PAY_OF[spec["cls"]]:
            bad.append("witness_incomplete")
    return bad
