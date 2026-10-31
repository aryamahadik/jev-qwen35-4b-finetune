"""G4 metamorphic relations (G0 section 5), checked through the independent path: transform the rendered row (or the
structure), parse it back (parse_f6) and re-solve with solver B; the label must change exactly as the relation says.

  M1  option shuffle (choice rows): every permutation's gold letter maps back to the gold option (fmt1 loader_check)
  M2  rename IDs consistently, order-preserving (same fixed-width format): label unchanged
  M4  reorder record lines and rule lines (precedence comes from row 24 inputs, never position): label unchanged
  M6  fill the decisive gap of an open Q-*, C-OUT or C-REC row with one value per region: every fill is settled and the
      settled answers together equal P (outcome) or T (claim)          [structure level, solver B]
  M8  delete a non-gold concrete option (C-OUT, C-REC): a settled row is unchanged; an NEI row stays NEI while P
      overlaps the remaining options, else becomes None-of-these when None is shown (otherwise skipped)
  M9  Q-DET with 'leave open whether' flips the label (complement); 'Is it not the case that the record leaves open
      whether S'' over S negated on its one atom keeps it (equiv)
  M11 switch record dates between ISO and month-name form: label unchanged
  M12 inject an imperative attack line into the record (row 40): label unchanged
"""
from __future__ import annotations

import copy
import random
import re

from . import common  # noqa: F401
from fmt1 import card as fcard

from . import parse_f6 as PF, solver_b as B, gates, canon_f6 as CF
from .common import MONTHS

ID_RX = re.compile(r"\b([A-Z]{2,4})-(\d{4})\b")


def parse_label(row: dict, W: set):
    """Solver B's label for a rendered F6 row (any kind), from the parse alone."""
    kind = row["meta"]["sampler"]
    if kind == "S3":
        S = PF.parse_table_row(row, W)
        vals = B.table_values(S["T"], S["Q"])
        if S["form"] == "c_rec":
            L = S["concrete"]
            inter = [o for o in L if o in vals]
            if len(vals) == 1 and inter:
                return inter[0]
            if not inter:      # same drop rule as gates.label_b (rules kind): G0 s5 M8 (b) skips this case
                if "none" in S["abstain"]:
                    return S["abstain"]["none"]
                raise B.Dropped("None gold not displayed")
            if len(vals) >= 2 and "nei" in S["abstain"]:
                return S["abstain"]["nei"]
            raise B.Dropped("NEI gold not displayed")
        return _yn(S["form"], S["frame"], vals)
    if kind == "S4":
        P = PF.parse_timeline_row(row, W)
        return _yn(P["form"], P["frame"], B.timeline_values(P["S"], P["Q"]))
    S = PF.parse_row(row, W)
    Q = PF.parse_question(S, row)
    if Q["form"] == "c_case":
        PF.parse_facts(S, row, Q["cases"])
        dec = B.decidable(S, Q["cases"])
        cand = dec if Q["frame"] == "c_case_can" else [c for c in Q["cases"] if c not in dec]
        return cand[0] if len(cand) == 1 else None
    PF.parse_facts(S, row, [Q["case"]])
    O = PF.parse_options(S, row, Q)
    return gates.label_b(S, row, Q, O)


def _yn(form, frame, vals):
    if form == "qdet":
        settled = len(vals) == 1
        return (0 if settled else 1) if frame in ("qdet_leave", "qdet_imp") else (1 if settled else 0)
    if form == "qest":
        return 1 if vals == {True} else 0
    return (1 if vals == {True} else 0) if len(vals) == 1 else None


def _map_text(row: dict, fn) -> dict:
    r = copy.deepcopy(row)
    for k in ("state", "instructions", "card"):
        if r.get(k):
            r[k] = fn(r[k])
    if r.get("options"):
        r["options"] = [fn(o) for o in r["options"]]
    if isinstance(r.get("gold"), str):
        r["gold"] = fn(r["gold"])
    return r


# ---------------------------------------------------------------- M2 rename (order-preserving)

def m2_rename(row: dict, rng: random.Random) -> tuple[dict, object]:
    text = " ".join(str(row.get(k) or "") for k in ("state", "instructions", "card")) + " " + \
        " ".join(row.get("options") or [])
    ids = sorted({m.group(0) for m in ID_RX.finditer(text)}, key=lambda x: int(x.split("-")[1]))
    if not ids:
        return None, None
    nums = sorted(rng.sample(range(1000, 10000), len(ids)))
    pre = {p: p for p in {x.split("-")[0] for x in ids}}
    mp = {old: f"{old.split('-')[0]}-{n}" for old, n in zip(ids, nums)}

    def fn(s):
        return ID_RX.sub(lambda m: mp.get(m.group(0), m.group(0)), s)
    r = _map_text(row, fn)
    return r, r["gold"]


# ---------------------------------------------------------------- M11 dates

ISO = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
NAMED = re.compile(r"\b(\d{1,2}) (" + "|".join(MONTHS) + r") (\d{4})\b")


def m11_dates(row: dict, rng) -> tuple[dict, object]:
    st = row["state"]
    if ISO.search(st):
        new = ISO.sub(lambda m: f"{int(m.group(3))} {MONTHS[int(m.group(2)) - 1]} {m.group(1)}", st)
    elif NAMED.search(st):
        new = NAMED.sub(lambda m: f"{m.group(3)}-{MONTHS.index(m.group(2)) + 1:02d}-{int(m.group(1)):02d}", st)
    else:
        return None, None
    if new == st:
        return None, None
    r = copy.deepcopy(row)
    r["state"] = new
    return r, row["gold"]


# ---------------------------------------------------------------- M4 reorder (record lines; rule lines)

KV = re.compile(r"^(\s*(?:[-*•+]\s+)?)([^:\n]+?)(:\s+|\s\.{3,}\s)(.+)$")


def _shuffle_table_rows(r: dict, rng) -> bool:
    """Reorder the records of an S3 table (row order never matters; row 23 ties go by ID number)."""
    from fmt1 import pool as fpool
    import json as _json
    st = fpool.style(r["meta"]["format_style"])
    cont = st["container"]
    text = r["state"]
    if cont == "json":
        sk = fpool.skin(st["skin"])["params"]
        m = re.match(r"^(\s*```\w*\n)?(.*?)(\n```\s*)?$", text, flags=re.S)
        data = _json.loads(m.group(2))
        if len(data) < 2:
            return False
        rng.shuffle(data)
        body = _json.dumps(data, ensure_ascii=False, indent=sk["indent"]) if sk["indent"] else \
            _json.dumps(data, ensure_ascii=False)
        r["state"] = (m.group(1) or "") + body + (m.group(3) or "")
        return True
    if cont in ("csv", "markdown_table"):
        lines = text.split("\n")
        idx = [i for i, ln in enumerate(lines) if ln.strip() and not ln.strip().startswith("```")]
        if cont == "markdown_table":
            idx = [i for i in idx if lines[i].strip().startswith("|")]
            # first table only: header + separator + rows until a break
            run, prev = [], None
            for i in idx:
                if prev is not None and i != prev + 1:
                    break
                run.append(i)
                prev = i
            idx = run[2:]
        else:
            idx = idx[1:]
        if len(idx) < 2:
            return False
        seg = [lines[i] for i in idx]
        perm = seg[:]
        rng.shuffle(perm)
        for i, x in zip(idx, perm):
            lines[i] = x
        r["state"] = "\n".join(lines)
        return perm != seg
    return False


def m4_reorder(row: dict, rng) -> tuple[dict, object]:
    r = copy.deepcopy(row)
    changed = False
    if row["meta"]["sampler"] == "S3":
        return (r, row["gold"]) if _shuffle_table_rows(r, rng) else (None, None)
    from fmt1 import pool as fpool
    cont = fpool.style(row["meta"]["format_style"])["container"]
    transcript = cont == "chat_log" or (cont == "email_thread" and fpool.skin(
        fpool.style(row["meta"]["format_style"])["skin"])["params"].get("order") != "single")
    lines = [] if (transcript or cont in ("html_snippet", "markdown_table")) else r["state"].split("\n")
    idx = [i for i, ln in enumerate(lines) if KV.match(ln) and not ln.strip().startswith(("Form:", "From:", "Sent:",
                                                                                           "Sender:", "Posted:"))]
    runs, cur = [], []
    for i in idx:
        if cur and i != cur[-1] + 1:
            runs.append(cur)
            cur = []
        cur.append(i)
    if cur:
        runs.append(cur)
    for run in runs:
        if len(run) >= 2:
            seg = [lines[i] for i in run]
            perm = seg[:]
            rng.shuffle(perm)
            if perm != seg:
                for i, x in zip(run, perm):
                    lines[i] = x
                changed = True
    if lines:
        r["state"] = "\n".join(lines)
    key = "card" if r["qtype"] == "noul" else "instructions"
    cl = (r.get(key) or "").split("\n")
    ridx = [i for i, ln in enumerate(cl) if re.match(r"^\s*(?:[-*•+]\s+)?(?:> )?(Rule \d+: In |Exception to rule)", ln)
            and "outcome table below" not in ln]
    if len(ridx) >= 2:
        seg = [cl[i] for i in ridx]
        perm = seg[:]
        rng.shuffle(perm)
        if perm != seg:
            for i, x in zip(ridx, perm):
                cl[i] = x
            r[key] = "\n".join(cl)
            changed = True
    if not changed:
        return None, None
    return r, row["gold"]


# ---------------------------------------------------------------- M12 attack line

def m12_attack(row: dict, rng) -> tuple[dict, object]:
    from .lex import ATTACK_LINES
    from fmt1 import pool as fpool
    cont = fpool.style(row["meta"]["format_style"])["container"]
    st = row["state"]
    if cont not in ("prose", "memo", "bullet_sop", "markdown_table") or st.rstrip().endswith("```"):
        return None, None
    if cont == "memo" and row["meta"]["sampler"] == "S3":
        return None, None
    r = copy.deepcopy(row)
    r["state"] = st.rstrip() + "\n\n" + rng.choice(ATTACK_LINES)
    return r, row["gold"]


# ---------------------------------------------------------------- M9 negation frames (Q-DET)

def m9_frames(row: dict, rng) -> list:
    """[(row', expected)] for 'leave open whether S' (complement) and the dneg frame over S' (equiv)."""
    out = []
    ins = row["instructions"]
    m = re.search(r"Can it be determined whether (.+?)\?", ins)
    if not m or row["qtype"] != "noul":
        return out
    S = m.group(1)
    r1 = copy.deepcopy(row)
    r1["instructions"] = ins.replace(m.group(0), f"Does the record leave open whether {S}?")
    out.append((r1, 1 - row["gold"]))
    neg = None
    for a, b in ((r' is "', r' is not "'), (" is on the ", " is not on the "), (" happened by ", " did not happen by "),
                 (" happened on or before ", " did not happen on or before "),
                 (" happened no later than ", " did not happen no later than "),
                 (" happened before ", " did not happen before ")):
        if a in S and " not " not in S and " no " not in f" {S} ":
            neg = S.replace(a, b, 1)
            break
    if neg:
        r2 = copy.deepcopy(row)
        r2["instructions"] = ins.replace(m.group(0), f"Is it not the case that the record leaves open whether {neg}?")
        out.append((r2, row["gold"]))
    return out


# ---------------------------------------------------------------- M8 option deletion

def m8_delete(row: dict, side: dict, rng) -> tuple[dict, object]:
    if row["qtype"] != "choice" or side["form"] not in ("c_out", "c_rec"):
        return None, None
    ab = {o for o in row["options"] if o in _abstain()}
    conc = [o for o in row["options"] if o not in ab and o != row["gold"]]
    if len(row["options"]) <= 3 or not conc:
        return None, None
    drop = rng.choice(conc)
    r = copy.deepcopy(row)
    r["options"] = [o for o in row["options"] if o != drop]
    if row["card"]:
        r["card"] = "\n".join(ln for ln in row["card"].split("\n") if not ln.startswith(f"- {drop}: ")) or None
    return r, "M8"      # expected computed by the caller from the gold class


def _abstain():
    from .lex import OPTION_TEXT
    return set(OPTION_TEXT["nei"] + OPTION_TEXT["none"] + OPTION_TEXT["nothing"])


# ---------------------------------------------------------------- M6 fill the decisive gap (structure level, solver B)

def m6_fill(side: dict) -> tuple[bool, str] | None:
    from . import solver_a as A, rules_gen as G, s_rules
    kind = side["kind"]
    st = side["struct"]
    if kind == "rules":
        if side["form"] not in ("qdet", "qest", "qplain", "c_out") or not st.get("case"):
            return None
        R, case, claim = st["R"], st["case"], st.get("claim")
        try:
            base = B.possible(R, case, claim)
        except B.Dropped:
            return False, "base drop"
        if len(base) < 2:
            return None
        dec = [d for d in A.decisive_gaps(R, case, claim) if d in [tuple(g) if isinstance(g, list) else g
                                                                     for g in [x for x, _ in G.visible_gaps(R, case)]]]
        if len(dec) != 1:
            return False, f"decisive gaps {len(dec)}"
        g = dec[0]
        got = set()
        for v in A.var_regions(R, case)[g]:
            R2 = s_rules._fill(R, case, g, v, allow_false_fact=True)
            if R2 is None:
                continue
            try:
                P2 = B.possible(R2, case, claim)
            except B.Dropped:
                return False, "fill drop"
            if len(P2) != 1:
                return False, "fill not settled"
            got |= P2
        return (got == base, "fills != P/T") if got != base else (True, "")
    if kind == "table":
        T, Q = st["T"], st["Q"]
        if side["form"] not in ("qdet", "qest", "qplain", "c_rec"):
            return None
        vals = B.table_values(T, Q)
        if len(vals) < 2:
            return None
        dec = A.table_decisive(T, Q)
        if len(dec) != 1 or dec[0][0] == "list":
            return None
        rid, cid = dec[0]
        got = set()
        for v in A.table_regions(T, cid, Q):
            T2 = A._fill_table(T, rid, cid, v)
            v2 = B.table_values(T2, Q)
            if len(v2) != 1:
                return False, "fill not settled"
            got |= v2
        return (got == vals, "fills != T")
    if kind == "timeline":
        from . import s4
        S, Q = st["S"], st["Q"]
        vals = B.timeline_values(S, Q)
        if len(vals) < 2:
            return None
        dec = s4.decisive(S, Q)
        if len(dec) != 1:
            return False, "decisive"
        got = set()
        for fill in s4._fills(S, dec[0]):
            if fill[0] == "none":
                continue
            S2 = s4._apply(S, dec[0], fill)
            try:
                v2 = B.timeline_values(S2, Q)
            except B.Dropped:
                continue
            if len(v2) != 1:
                return False, "fill not settled"
            got |= v2
        return (got <= vals and bool(got), "fills outside T")
    return None


# ---------------------------------------------------------------- driver

def run_row(row: dict, side: dict, W: set, rng: random.Random) -> dict:
    """{relation: 'pass' | 'fail:<why>' | 'skip'} for one row."""
    res = {}
    # M1: three random permutations through fmt1 loader_check (gold letter maps back)
    if row["qtype"] == "choice":
        ok = True
        for i in range(3):
            n = len(row["options"])
            perm = list(range(n))
            rng.shuffle(perm)
            c = fcard.loader_check(row, perm=perm, check_rows=False)
            ok = ok and c["ok"]
        res["M1"] = "pass" if ok else "fail:loader"
    for name, fn in (("M2", m2_rename), ("M4", m4_reorder), ("M11", m11_dates), ("M12", m12_attack)):
        try:
            r2, exp = fn(row, rng)
        except Exception as e:  # noqa: BLE001
            res[name] = f"fail:transform {type(e).__name__}"
            continue
        if r2 is None:
            res[name] = "skip"
            continue
        try:
            got = parse_label(r2, W)
        except Exception as e:  # noqa: BLE001
            res[name] = f"fail:{type(e).__name__}:{str(e)[:60]}"
            continue
        res[name] = "pass" if got == exp else f"fail:label {got!r} != {exp!r}"
    if side["form"] == "qdet":
        for i, (r2, exp) in enumerate(m9_frames(row, rng)):
            nm = "M9c" if i == 0 else "M9e"
            try:
                got = parse_label(r2, W)
                res[nm] = "pass" if got == exp else f"fail:label {got!r} != {exp!r}"
            except Exception as e:  # noqa: BLE001
                res[nm] = f"fail:{type(e).__name__}:{str(e)[:60]}"
    r2, _ = m8_delete(row, side, rng)
    if r2 is not None:
        try:
            got = parse_label(r2, W)
            gc = side["gold_class"]
            if gc == "concrete":
                ok = got == row["gold"]
            elif gc == "nei":
                ok = got in (row["gold"],) or got in _abstain()
            else:
                ok = got == row["gold"]
            res["M8"] = "pass" if ok else f"fail:label {got!r}"
        except B.Dropped as e:
            # NEI row whose deleted option was the last listed possible outcome while None is not shown: the
            # relation skips this case (G0 s5 M8 (b))
            res["M8"] = "skip" if side["gold_class"] == "nei" and "not displayed" in str(e) else f"fail:Dropped:{e}"
        except Exception as e:  # noqa: BLE001
            res["M8"] = f"fail:{type(e).__name__}:{str(e)[:60]}"
    try:
        m6 = m6_fill(side)
    except Exception as e:  # noqa: BLE001
        m6 = (False, f"{type(e).__name__}:{str(e)[:60]}")
    if m6 is not None:
        res["M6"] = "pass" if m6[0] else f"fail:{m6[1]}"
    return res
