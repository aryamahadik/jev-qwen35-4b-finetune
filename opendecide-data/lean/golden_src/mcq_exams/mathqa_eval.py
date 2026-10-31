"""Evaluator for MathQA annotated_formula programs (nested prefix calls such as divide(multiply(48, const_1000), 9)).
Used only to VERIFY AQuA-RAT golds (build_aqua_rat.py): an item is kept when an independent MathQA annotator's program
computes the AQuA gold value. Operation semantics follow the MathQA operation list; operations not implemented here make
the evaluation return None, which drops the item (conservative).
"""
import math, re

def _fact(x):
    if x < 0 or x > 170 or abs(x - round(x)) > 1e-9:
        raise ValueError
    return float(math.factorial(int(round(x))))

def _int(x):
    if abs(x - round(x)) > 1e-9:
        raise ValueError
    return int(round(x))

OPS = {
    "add": lambda a, b: a + b, "subtract": lambda a, b: a - b, "multiply": lambda a, b: a * b,
    "divide": lambda a, b: a / b, "power": lambda a, b: a ** b, "sqrt": lambda a: math.sqrt(a),
    "inverse": lambda a: 1 / a, "negate": lambda a: -a, "factorial": _fact, "floor": lambda a: float(math.floor(a)),
    "reminder": lambda a, b: a % b, "log": lambda a: math.log(a), "max": max, "min": min,
    "gcd": lambda a, b: float(math.gcd(_int(a), _int(b))), "lcm": lambda a, b: float(math.lcm(_int(a), _int(b))),
    "choose": lambda n, k: float(math.comb(_int(n), _int(k))), "permutation": lambda n, k: float(math.perm(_int(n), _int(k))),
    "rectangle_area": lambda a, b: a * b, "rectangle_perimeter": lambda a, b: 2 * (a + b),
    "square_area": lambda a: a * a, "square_perimeter": lambda a: 4 * a, "circle_area": lambda r: math.pi * r * r,
    "circumface": lambda r: 2 * math.pi * r, "volume_cube": lambda a: a ** 3, "surface_cube": lambda a: 6 * a * a,
    "cube_edge_by_volume": lambda v: v ** (1 / 3), "square_edge_by_perimeter": lambda p: p / 4,
    "square_edge_by_area": lambda a: math.sqrt(a), "volume_cylinder": lambda r, h: math.pi * r * r * h,
    "volume_rectangular_prism": lambda a, b, c: a * b * c,
    "surface_rectangular_prism": lambda a, b, c: 2 * (a * b + b * c + a * c),
    "triangle_area": lambda b, h: b * h / 2, "triangle_perimeter": lambda a, b, c: a + b + c,
    "triangle_area_three_edges": lambda a, b, c: (lambda s: math.sqrt(s * (s - a) * (s - b) * (s - c)))((a + b + c) / 2),
    "rhombus_area": lambda d1, d2: d1 * d2 / 2, "quadrilateral_area": lambda d, h1, h2: d * (h1 + h2) / 2,
    "speed": lambda d, t: d / t, "volume_sphere": lambda r: 4 / 3 * math.pi * r ** 3,
    "surface_sphere": lambda r: 4 * math.pi * r * r, "volume_cone": lambda r, h: math.pi * r * r * h / 3,
    "surface_cylinder": lambda r, h: 2 * math.pi * r * (r + h), "negate_prob": lambda p: 1 - p,
    "original_price_before_gain": lambda g, p: p * 100 / (100 + g), "original_price_before_loss": lambda l, p: p * 100 / (100 - l),
    "p_after_gain": lambda g, p: p * (100 + g) / 100, "stream_speed": lambda a, b: (a - b) / 2,
    "speed_in_still_water": lambda a, b: (a + b) / 2, "diagonal": lambda a, b: math.sqrt(a * a + b * b),
    "rhombus_perimeter": lambda a: 4 * a,
}
CONST = {"pi": math.pi, "deg_to_rad": math.pi / 180}


def _atom(tok):
    tok = tok.strip()
    if tok.startswith("const_"):
        k = tok[6:]
        if k in CONST:
            return CONST[k]
        return float(k.replace("_", "."))
    return float(tok)


def evaluate(formula):
    """Evaluate a MathQA annotated_formula (nested prefix calls). None if it cannot be evaluated."""
    s = formula.strip().rstrip("|").strip()
    pos = 0

    def parse():
        nonlocal pos
        m = re.match(r"\s*([a-z_]+)\s*\(", s[pos:])
        if m and m.group(1) in OPS:
            name = m.group(1)
            pos += m.end()
            args = []
            while True:
                args.append(parse())
                while pos < len(s) and s[pos] == " ":
                    pos += 1
                if pos < len(s) and s[pos] == ",":
                    pos += 1
                    continue
                if pos < len(s) and s[pos] == ")":
                    pos += 1
                    break
                raise ValueError("bad syntax")
            return OPS[name](*args)
        m = re.match(r"\s*([A-Za-z0-9_.\-]+)", s[pos:])
        if not m:
            raise ValueError("bad atom")
        pos += m.end()
        return _atom(m.group(1))
    try:
        v = parse()
        if pos != len(s.strip()):
            while pos < len(s) and s[pos] in " )":
                pos += 1
            if pos != len(s):
                return None
        if isinstance(v, complex) or v != v or abs(v) == float("inf"):
            return None
        return float(v)
    except Exception:  # noqa: BLE001
        return None
