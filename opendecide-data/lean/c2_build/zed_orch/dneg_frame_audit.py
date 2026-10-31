#!/usr/bin/env python3
"""A43 (f) audit (program only, no model): yes/no wordings that negate the interrogative frame over a negated proposition.

For every C2 family it loads the yes/no question forms the family actually uses (frozen lexicon + iteration-2 / redo
supplements), flags a form when (a) its leading interrogative frame is negated and (b) the remaining proposition holds a
negation (c_src/common/negcount, k_all >= 1), and estimates the double-negation share of yes/no rows (pilot.g10 measure:
negcount k_syn >= 2 on the question, over qtype "noul" rows) before and after dropping rows of flagged forms.

Run from c2_build:  .venv/bin/python -B zed_orch/dneg_frame_audit.py
Writes zed_orch/DNEG_FRAME_AUDIT.json, DNEG_FRAME_AUDIT.md, a43f_quarantine.json. Reads only; modifies no family file.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
sys.path.insert(0, str(BUILD.parent / "c_src" / "common"))
import negcount  # noqa: E402

FLOOR = 0.02

# family -> ordered lexicon sources (later wins on the same form_id); each is (relative path, list key | None)
SRC = {
    "T01": [("pools_v2/lexicon_registry.json", "forms"), ("pools_v2/dneg_i2_supplement.json", "lexicon_forms")],
    "T06": [("pools_v2/lexicon.json", "forms")],
    "T07": [("pools/lexicon.json", "forms"), ("pools/redo2/lexicon_add.json", "forms"),
            ("pools/redo3/lexicon_add.json", "forms")],
    "T12": [("pools_v2/lexicon.json", "forms")],
    "T15": [("pools_v2/lexicon.json", "forms")],
    "T23": [("pools_v2/lexicon.json", "forms")],
    "T24": [("pools/lexicon.json", "forms")],
    "T25": [("pools_v2/lexicon.json", "forms")],
    "T26": [("pools_v2/lexicon.json", "registry.forms")],
    "T27": [("pools_v2/lexicon.json", "forms"), ("haiku/ovl_i2/admitted/lexicon_supplement.json", "forms")],
    "T28": [("pools_v2/lexicon.json", "forms")],
    "T29": [("pools/dneg/lexicon_merged.json", "forms")],
    "T30": [("pools/lexicon.json", "forms")],
    "T31": [("pools_v2/lexicon.json", "forms"), ("pools_v2_dneg/lexicon_dneg.json", "forms")],
    "T32": [("pools_v2/lexicon_registry.json", "forms")],
    "T33": [("pools/lexicon.json", "forms"), ("pools/dneg_i2_supplement.json", "lexicon_forms")],
    "T35": [("pools/lexicon.json", "forms")],
    "T19": [("pools_v2/lexicon.json", "forms")],
    "T20": [("pools/lexicon.json", "forms")],
    "T21": [("pools_v2/lexicon.json", "forms")],
    "T36": [("pools_v2/lexicon.json", "forms")],
}
DIRS = {f: (BUILD / ("transfer" if f in ("T19", "T20", "T21", "T36") else "families") / f) for f in SRC}
DIRS["T37b"] = BUILD / "t37b"

# ---------------------------------------------------------------------------------------------------- frame detection
AUX = r"(?:is|are|was|were|does|do|did|has|have|had|can|could|will|would|should|must|may|might)"
GAP_BAN = {"that", "whether", "if", "true", "false", "untrue", "correct", "right", "accurate", "so", "because", "when",
           "which", "who", "case", "whose", "where", "while", "than", "say", "is", "are", "was", "were",
           "does", "do", "did", "has", "have", "had", "can", "could", "will", "would", "should", "must", "may",
           "might"}
RE_CONTRACT = re.compile(r"^(?:\w+n't|cannot)\b", re.I)
RE_ADJ = re.compile(rf"^({AUX})\s+(?:(?:it|that|this)\s+)?(not|untrue|false)\b", re.I)
RE_GAP = re.compile(rf"^({AUX})\s+((?:[\w'\-]+\s+){{1,6}}?)not\b", re.I)


def _norm(t: str) -> str:
    t = t.replace("\u2019", "'").replace("\u2018", "'")
    return re.sub(r"\{[A-Za-z0-9_]+\}", "X", t)


def _starts(t: str):
    yield 0
    for m in re.finditer(r"[,:;]\s+", t):
        yield m.end()


def frame_negated(text: str):
    """(frame string, remainder) when the leading interrogative frame is negated, else None."""
    t = _norm(text)
    for s in _starts(t):
        u = t[s:]
        m = RE_CONTRACT.match(u)
        if m:
            return m.group(0), t[:s] + u[m.end():]
        m = RE_ADJ.match(u)
        if m:
            return m.group(0), t[:s] + u[m.end():]
        m = RE_GAP.match(u)
        if m and not (set(w.lower() for w in re.findall(r"[\w']+", m.group(2))) & GAP_BAN):
            return m.group(0), t[:s] + m.group(2) + u[m.end():]
    return None


def flag_text(text: str) -> dict | None:
    fr = frame_negated(text)
    if not fr:
        return None
    frame, rest = fr
    c = negcount.count(rest)
    if c.k_all < 1:
        return None
    return {"frame": frame, "k_all_rest": c.k_all, "k_syn_rest": c.k_syn,
            "k_syn_text": negcount.count(_norm(text)).k_syn}


# ---------------------------------------------------------------------------------------------------- forms
def load_forms(fam: str) -> dict:
    """{form_id: {text, sem_id, source}} of admitted yes/no question forms."""
    forms = {}
    for rel, key in SRC[fam]:
        p = DIRS[fam] / rel
        if not p.exists():
            continue
        d = json.loads(p.read_text())
        for k in (key or "").split("."):
            if k:
                d = d[k]
        for f in d:
            if not isinstance(f, dict) or "form_id" not in f:
                continue
            kind = f.get("kind") or ("question" if str(f.get("sem_id", "")).startswith("q.") else None)
            if kind != "question":
                continue
            if f.get("status", "admitted") != "admitted":
                forms.pop(f["form_id"], None)
                continue
            if f["sem_id"].split(".")[-1].startswith("yn_"):
                forms[f["form_id"]] = {"text": f["text"], "sem_id": f["sem_id"], "source": rel}
    return forms


def load_t37b() -> dict:
    forms = {}
    for rel in ("pools/t37b_equiv_pool.json", "pools/redo2/t37b_equiv_pool_redo2.json"):
        d = json.loads((DIRS["T37b"] / rel).read_text())
        for i, para in enumerate(d["paraphrases"]):
            if para.get("status") != "admitted":
                continue
            fid = f"t37b-pool|{para['sem']}|{para['haiku_task_id']}"
            forms[fid] = {"text": para["template"], "sem_id": para["sem"], "source": rel}
    return forms


def load_t20_program() -> dict:
    """T20's program-written double-negation wordings (plugin.PROGRAM_DN_WORDINGS; not lexicon forms)."""
    import importlib
    sys.path.insert(0, str(BUILD))
    P = importlib.import_module("transfer.T20.plugin")
    return {f"T20-program-dn-{i}": {"text": t, "sem_id": "yn_double_neg", "source": "plugin.py PROGRAM_DN_WORDINGS"}
            for i, t in enumerate(P.PROGRAM_DN_WORDINGS)}


# ---------------------------------------------------------------------------------------------------- rows
def latest_rows(fdir: Path):
    for sub in ("pilot_i2", "pilot_i1", "pilot"):
        p = fdir / sub / "rows.jsonl"
        if p.exists():
            return sub, [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
    return None, []


def question_of(r: dict) -> str:
    lines = [x for x in (r.get("instructions") or "").split("\n") if x.strip()]
    return lines[-1] if lines else ""


def dneg_share(qs: list) -> tuple:
    n = len(qs)
    k = sum(1 for q in qs if negcount.count(q).k_syn >= 2)
    return k, n, (k / n if n else None)


def find_key(o, key):
    if isinstance(o, dict):
        if key in o:
            return o[key]
        for v in o.values():
            r = find_key(v, key)
            if r is not None:
                return r
    elif isinstance(o, list):
        for v in o:
            r = find_key(v, key)
            if r is not None:
                return r
    return None


def audit(fam: str) -> dict:
    fdir = DIRS[fam]
    forms = load_t37b() if fam == "T37b" else load_forms(fam)
    if fam == "T20":
        forms.update(load_t20_program())
    flagged = {}
    for fid, f in sorted(forms.items()):
        fl = flag_text(f["text"])
        if fl:
            flagged[fid] = {"text": f["text"], "sem_id": f["sem_id"], **fl}
    sub, rows = latest_rows(fdir)
    yn = [r for r in rows if r.get("qtype") == "noul"]
    fids = set(flagged)
    yn_ids = set(forms)
    n_mapped = 0
    rows_hit = []
    for r in yn:
        c2 = (r.get("meta") or {}).get("c2") or {}
        ids = set(c2.get("lexicon_ids") or [])
        wid = str((r.get("meta") or {}).get("wording_id"))
        mapped = bool(ids & yn_ids) or any(f in wid for f in yn_ids)
        n_mapped += mapped
        hit = bool(ids & fids) or any(f in wid for f in fids)
        direct = flag_text(question_of(r)) is not None
        hit = hit or (not mapped and direct)     # row of a program-written / unlisted wording: judged by its own text
        rows_hit.append((r, hit, direct, mapped))
    qs = [question_of(r) for r in yn]
    k0, n0, s0 = dneg_share(qs)
    keep = [question_of(r) for r, h, d, m in rows_hit if not h]
    k1, n1, s1 = dneg_share(keep)
    direct_keep = [question_of(r) for r, h, d, m in rows_hit if not (h or d)]
    k2, n2, s2 = dneg_share(direct_keep)
    rep = None
    for rp in (fdir / (sub or "pilot") / "PILOT_REPORT.json",):
        if rp.exists():
            try:
                v = find_key(json.loads(rp.read_text()), "double_negation_share")
                rep = v.get("value") if isinstance(v, dict) else v
            except Exception:
                pass
    return {
        "rows_source": f"{sub}/rows.jsonl" if sub else None, "yes_no_forms": len(forms), "flagged_forms": len(flagged),
        "flagged": flagged,
        "yes_no_rows": n0, "rows_mapped_to_a_form": n_mapped, "rows_of_flagged_forms": n0 - n1,
        "rows_flagged_by_direct_frame_check": sum(1 for r, h, d, m in rows_hit if d),
        "dneg_rows_before": k0, "dneg_share_before": s0, "pilot_report_share": rep,
        "yes_no_rows_after": n1, "dneg_rows_after": k1, "dneg_share_after": s1,
        "dneg_share_after_if_direct_check_also_applied": s2,
        "below_2pct_after": (s1 is not None and s1 < FLOOR),
        "below_2pct_before": (s0 is not None and s0 < FLOOR),
    }


def main():
    fams = sorted(SRC) + ["T37b"]
    out = {"rule": "A43 (f): frame negated AND remaining proposition negated (negcount k_all >= 1)",
           "floor": FLOOR, "families": {}, "notes": [
               "Forms: admitted question forms whose sem_id local name starts with yn_ in the frozen lexicon plus the "
               "iteration-2 / redo supplements (see SRC in the script); T37b: admitted pool paraphrase templates.",
               "Rows: pilot_i2/rows.jsonl else pilot_i1 else pilot; a row is a flagged-form row when its "
               "meta.c2.lexicon_ids (or meta.wording_id) holds a flagged form id. Share = negcount k_syn >= 2 on the "
               "question (last instruction line), over qtype noul rows, as pilot.g10.",
               "'after' is an estimate: flagged rows are removed, no replacement rows are drawn. "
               "dneg_share_after_if_direct_check_also_applied also drops rows whose own question text has the banned "
               "shape (catches rows from non-lexicon sources such as program-written T37b partners).",
               "T40, T41, T42 have no pilot rows and no frozen pools yet: not audited."]}
    quar = {}
    for f in fams:
        a = audit(f)
        out["families"][f] = a
        quar[f] = sorted(a["flagged"])
    (HERE / "DNEG_FRAME_AUDIT.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    (HERE / "a43f_quarantine.json").write_text(json.dumps(quar, indent=1))
    pc = lambda x: "n/a" if x is None else f"{100 * x:.2f}%"  # noqa: E731
    L = ["# A43 (f) double-negation frame audit", "",
         "Flag = negated interrogative frame AND negation in the remaining proposition (negcount k_all >= 1). "
         "Share = k_syn >= 2 on yes/no rows (pilot.g10 measure) from the latest pilot rows; after = flagged-form rows "
         "removed (estimate, no redraw). Floor 2% (spec 3.0).", "",
         "| family | yes/no forms | flagged | dneg share before | after | below 2%? |", "|---|---|---|---|---|---|"]
    for f in fams:
        a = out["families"][f]
        L.append(f"| {f} | {a['yes_no_forms']} | {a['flagged_forms']} | {pc(a['dneg_share_before'])} | "
                 f"{pc(a['dneg_share_after'])} | {'YES' if a['below_2pct_after'] else 'no'} |")
    L += ["", "Rows source and checks per family are in `DNEG_FRAME_AUDIT.json` (rows_source, pilot_report_share, "
          "rows_mapped_to_a_form, dneg_share_after_if_direct_check_also_applied). "
          "Quarantine list for full generation: `a43f_quarantine.json`."]
    (HERE / "DNEG_FRAME_AUDIT.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[5:]))
    for f in fams:
        a = out["families"][f]
        print(f, a["rows_source"], "rows", a["yes_no_rows"], "mapped", a["rows_mapped_to_a_form"],
              "flaggedrows", a["rows_of_flagged_forms"], "direct", a["rows_flagged_by_direct_frame_check"],
              "pilot", a["pilot_report_share"], "directAfter", pc(a["dneg_share_after_if_direct_check_also_applied"]))


if __name__ == "__main__":
    main()
