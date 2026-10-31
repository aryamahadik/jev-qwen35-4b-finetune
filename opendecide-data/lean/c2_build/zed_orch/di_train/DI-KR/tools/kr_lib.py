"""DI-KR (A61 b/d: GSM8K main train, choice head) shared helpers. CPU only, deterministic, seed 20261013. Counts only on stdout.
Source files are untrusted data: read them with `python -I` (scripts live here, in tools/, not in src/)."""
import ast, hashlib, json, math, re, sys
from fractions import Fraction
from pathlib import Path

KR = Path(__file__).resolve().parent.parent            # zed_orch/di_train/DI-KR
C2 = KR.parents[2]                                      # lean/c2_build
LEAN = C2.parent
SRC = KR / "src"
WORK = KR / "work"
SEED = 20261013
BASES = (20261013, 11000000, 12000000, 13000000)        # A50 four-build seed bases (A61 c 7)
sys.path.insert(0, str(C2))


def sha(s):
    return hashlib.sha256(s if isinstance(s, bytes) else s.encode()).hexdigest()


def h(*p):
    return int(sha("|".join(map(str, p))), 16)


def hs(seed, *p):
    return h(seed, *p)


# ------------------------------------------------------------------ pure-arithmetic AST evaluator (no names, no eval)
_OK = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub, ast.UAdd, ast.Mod, ast.FloorDiv)


class Bad(Exception):
    pass


def _ev(n):
    if isinstance(n, ast.Expression):
        return _ev(n.body)
    if isinstance(n, ast.Constant):
        if isinstance(n.value, bool) or not isinstance(n.value, (int, float)):
            raise Bad("const")
        return Fraction(str(n.value))
    if isinstance(n, ast.UnaryOp):
        v = _ev(n.operand)
        if isinstance(n.op, ast.USub):
            return -v
        if isinstance(n.op, ast.UAdd):
            return v
        raise Bad("unary")
    if isinstance(n, ast.BinOp):
        a, b = _ev(n.left), _ev(n.right)
        o = n.op
        if isinstance(o, ast.Add):
            return a + b
        if isinstance(o, ast.Sub):
            return a - b
        if isinstance(o, ast.Mult):
            return a * b
        if isinstance(o, ast.Div):
            if b == 0:
                raise Bad("div0")
            return a / b
        if isinstance(o, ast.Mod):
            if b == 0:
                raise Bad("div0")
            return a % b
        if isinstance(o, ast.FloorDiv):
            if b == 0:
                raise Bad("div0")
            return Fraction(math.floor(a / b))
        if isinstance(o, ast.Pow):
            if b.denominator != 1 or abs(b) > 12 or abs(a) > 10 ** 6:
                raise Bad("pow")
            return a ** int(b)
    raise Bad("node")


def evaluate(expr: str) -> Fraction:
    expr = re.sub(r"(?<=\d),(?=\d{3}\b)", "", expr.strip())
    if not re.fullmatch(r"[0-9.+\-*/()%\s]*", expr) or not expr:
        raise Bad("charset")
    if "%" in expr and not re.search(r"\d\s*%\s*\d|\)\s*%", expr):
        raise Bad("percent")
    tree = ast.parse(expr, mode="eval")
    for n in ast.walk(tree):
        if not isinstance(n, _OK):
            raise Bad("node")
    return _ev(tree)


NUM = re.compile(r"-?\d+(?:\.\d+)?")


def dec_places(s: str) -> int:
    return len(s.split(".", 1)[1]) if "." in s else 0


def parse_num(s: str):
    s = s.strip().replace(",", "").replace("$", "")
    if not NUM.fullmatch(s):
        return None
    return Fraction(s)


ANN = re.compile(r"<<(.*?)>>")


def check_problem(ans: str):
    """-> (ok, reason, info). info: gold str, annotation computed values (Fractions). Pure-arithmetic re-computation of every
    <<expr=value>>; the chain must reach the #### answer (the last annotation's computed value equals it)."""
    if "####" not in ans:
        return False, "no_final_marker", None
    body, fin = ans.rsplit("####", 1)
    gs = fin.strip().replace(",", "").replace("$", "")
    gv = parse_num(gs)
    if gv is None:
        return False, "answer_unparsable", None
    anns = ANN.findall(body)
    if not anns:
        return False, "no_annotations", None
    vals = []
    for a in anns:
        parts = a.split("=")
        if len(parts) < 2:
            return False, "annotation_no_equals", None
        try:
            c = evaluate(parts[0])
        except Bad as e:
            return False, f"expr_{e}", None
        except (SyntaxError, ValueError, ZeroDivisionError, RecursionError):
            return False, "expr_syntax", None
        for st in parts[1:]:
            sv = parse_num(st)
            if sv is None:
                return False, "stated_unparsable", None
            tol = Fraction(1, 2 * 10 ** dec_places(st.strip().replace(",", "").replace("$", "")))
            if abs(c - sv) > tol:
                return False, "recompute_mismatch", None
        vals.append(c)
    tolg = Fraction(1, 2 * 10 ** dec_places(gs))
    if abs(vals[-1] - gv) > tolg:
        if any(abs(v - gv) <= tolg for v in vals):
            return False, "answer_not_last_annotation", None
        return False, "chain_misses_answer", None
    return True, "ok", {"gold": gs, "vals": vals}


def fmt(v: Fraction, d: int) -> str:
    """One number format: d decimal places (0 = integer, no separators)."""
    q = v * 10 ** d
    if q.denominator != 1:
        raise ValueError("not representable")
    n = int(q)
    if d == 0:
        return str(n)
    sign = "-" if n < 0 else ""
    n = abs(n)
    s = str(n).rjust(d + 1, "0")
    return f"{sign}{s[:-d]}.{s[-d:]}"


def representable(v: Fraction, d: int) -> bool:
    return (v * 10 ** d).denominator == 1


def norm_tokens(t):
    return re.findall(r"[a-z0-9]+", t.lower())


def grams(tok, n=5):
    return {" ".join(tok[i:i + n]) for i in range(len(tok) - n + 1)}
