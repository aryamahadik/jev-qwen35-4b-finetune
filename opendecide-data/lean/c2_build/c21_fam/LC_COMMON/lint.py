"""Generator lint (K12): no clocks, randomness, environment reads, network, filesystem outside /work, absolute paths,
or order-dependent printing in a rendered source file. The IR has none of these constructs, so a hit means a renderer or
atom bug; the lint runs on every kept row's rendered text (static, CPU, data only).
"""
import re

COMMON = [r"/etc/", r"/proc/", r"/sys/", r"/home/", r"/tmp/", r"/dev/", r"~/", r"https?://"]
PATTERNS = {
    "python": [r"\bimport\s+(time|random|os|sys|datetime|secrets|uuid|subprocess|socket|threading|multiprocessing|pathlib|shutil|tempfile|glob)\b",
               r"\bfrom\s+(time|random|os|datetime|secrets|uuid|subprocess|socket)\b", r"\bopen\(", r"\binput\(", r"\bprint\(",
               r"\b(eval|exec|__import__)\(", r"\bhash\("],
    "javascript": [r"\bDate\b", r"Math\.random", r"\bprocess\b", r"require\(\s*['\"](fs|os|child_process|crypto|net|http|path)['\"]",
                   r"\bsetTimeout\b", r"\bsetInterval\b", r"\bperformance\b", r"\beval\(", r"\bnew Function\b", r"console\."],
    "go": [r"\"(time|math/rand|os|os/exec|net|net/http|crypto/rand|io/ioutil|path/filepath|syscall|unsafe|runtime)\"", r"\btime\.", r"\brand\.",
           r"\bos\.", r"\bgo func\b", r"\bselect\s*\{", r"\bfmt\.Print"],
    "bash": [r"\$RANDOM", r"\$SECONDS", r"\bdate\b", r"\bcurl\b", r"\bwget\b", r"\bnc\b", r"\bssh\b", r"\bsleep\b", r"\$\$", r"`", r"\beval\b",
             r"\bread\b", r"\benv\b", r"\bprintenv\b", r"\bls\b", r"\bfind\b", r"\bhostname\b", r"\buname\b"],
}
PATTERNS["typescript"] = PATTERNS["javascript"]

_CACHE = {}


def _compiled(lang):
    if lang not in _CACHE:
        _CACHE[lang] = [re.compile(p) for p in PATTERNS[lang] + COMMON]
    return _CACHE[lang]


def lint_text(lang, text):
    """List of (pattern, line number) hits; [] = clean."""
    hits = []
    for ln, line in enumerate(text.splitlines(), 1):
        for rx in _compiled(lang):
            if rx.search(line):
                hits.append((rx.pattern, ln))
    return hits


def lint_files(lang, files):
    out = {}
    for path, text in files.items():
        if path in ("go.mod", "vendor/modules.txt"):
            continue
        h = lint_text(lang, text)
        if h:
            out[path] = h
    return out
