"""public-2 rendering helpers: table containers, number formatting, card and wording pools (all Claude-written,
program-filled; every pool entry has a stable id). The pools are written to out/wordings.json and out/cards.jsonl
for the sealed check and the counts-only decontamination of Claude-written seeds (spec 7.2)."""
from __future__ import annotations

import html
import json
from fractions import Fraction

# ---------------------------------------------------------------- numbers


def fmt_num(x) -> str:
    """Render an int/float/Fraction without float noise (at most 4 decimals, trailing zeros removed)."""
    if isinstance(x, Fraction):
        if x.denominator == 1:
            return str(x.numerator)
        s = f"{float(x):.4f}".rstrip("0").rstrip(".")
        return s
    if isinstance(x, bool):
        return str(x)
    if isinstance(x, int):
        return str(x)
    if isinstance(x, float):
        if x.is_integer():
            return str(int(x))
        return f"{x:.4f}".rstrip("0").rstrip(".")
    return str(x)


def to_frac(x) -> Fraction:
    if isinstance(x, Fraction):
        return x
    if isinstance(x, int):
        return Fraction(x)
    return Fraction(str(x))


# ---------------------------------------------------------------- tables

CONTAINERS = ["markdown", "csv", "json_records", "key_value", "html", "pipe_plain"]


def _cell(v):
    return fmt_num(v) if isinstance(v, (int, float, Fraction)) else str(v)


def render_table(header, rows, container, title=None, caption=None):
    head = []
    if title:
        head.append(f"Page: {title}")
    if caption and caption != title:
        head.append(f"Table: {caption}")
    cells = [[_cell(v) for v in r] for r in rows]
    if container == "markdown":
        body = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
        body += ["| " + " | ".join(c.replace("|", "/") for c in r) + " |" for r in cells]
    elif container == "pipe_plain":
        body = [" | ".join(header)] + [" | ".join(c.replace("|", "/") for c in r) for r in cells]
    elif container == "csv":
        import csv
        import io
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator="\n")
        w.writerow(header)
        for r in cells:
            w.writerow(r)
        body = buf.getvalue().rstrip("\n").split("\n")
    elif container == "json_records":
        recs = []
        for r in rows:
            recs.append({h: (v if isinstance(v, (int, float)) and not isinstance(v, bool) else _cell(v))
                         for h, v in zip(header, r)})
        body = [json.dumps(recs, ensure_ascii=False, indent=1)]
    elif container == "key_value":
        body = []
        for i, r in enumerate(cells, 1):
            body.append(f"Record {i}:")
            body += [f"  {h}: {c}" for h, c in zip(header, r)]
    elif container == "html":
        body = ["<table>", "<tr>" + "".join(f"<th>{html.escape(h)}</th>" for h in header) + "</tr>"]
        body += ["<tr>" + "".join(f"<td>{html.escape(c)}</td>" for c in r) + "</tr>" for r in cells]
        body.append("</table>")
    else:
        raise ValueError(container)
    return "\n".join(head + body)


def letters(n):
    import string
    return list(string.ascii_uppercase[:n])


def dump_pools(path_w, path_c, wordings: dict, cards: dict):
    json.dump(wordings, open(path_w, "w"), indent=1, ensure_ascii=False)
    with open(path_c, "w") as f:
        for cid, c in sorted(cards.items()):
            f.write(json.dumps({"id": cid, **c}, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------- yes/no thresholds (shared by WikiSQL and DROP)

INCL = {">=", "<="}
EXCL = {">", "<"}


def holds(x, op, T):
    return {">": x > T, ">=": x >= T, "<": x < T, "<=": x <= T}[op]


def pick_threshold(rng, x, want_yes, step, boundary_ok, boundary_p=0.4):
    """op and T with holds(x, op, T) == want_yes, built so that the comparison word does not predict the label.

    Boundary rows (T == x, 40% where the value allows it): yes -> inclusive op, no -> exclusive op. To cancel that,
    non-boundary rows of the same kind use: yes -> exclusive op; no -> inclusive op with p = b / (1 - b) = 2/3.
    Rows that cannot sit at the boundary draw inclusive / exclusive 50/50 for both labels.
    So P(inclusive | yes) = P(inclusive | no) in each group. Direction (greater / less) is a fair coin."""
    up = rng.random() < 0.5
    if boundary_ok and rng.random() < boundary_p:
        op = (">=" if up else "<=") if want_yes else (">" if up else "<")
        return op, x, True
    if boundary_ok:
        incl = False if want_yes else (rng.random() < boundary_p / (1 - boundary_p))
    else:
        incl = rng.random() < 0.5
    op = (">=" if up else "<=") if incl else (">" if up else "<")
    # greater-type op: yes needs T below x; less-type op: yes needs T above x
    T = x - step if (up == want_yes) else x + step
    if holds(x, op, T) != want_yes:
        return None
    return op, T, False


def pick_ranked(rng, opts, x, k):
    """k distractors (numeric strings) so that the gold's rank among the k + 1 numbers is drawn uniformly from the
    ranks the pool allows (an options-only reader cannot learn 'gold is the second smallest')."""
    below = [o for o in opts if Fraction(o) < x]
    above = [o for o in opts if Fraction(o) > x]
    lo, hi = max(0, k - len(above)), min(k, len(below))
    if lo > hi:
        return None
    r = rng.randint(lo, hi)
    rng.shuffle(below)
    rng.shuffle(above)
    return below[:r] + above[:k - r]
