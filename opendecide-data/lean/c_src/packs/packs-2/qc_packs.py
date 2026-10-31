#!/usr/bin/env python3
"""packs-2 QC: sealed check (by running the id-only checker as a program), pairwise ROUGE-L between packs, and
string-level component export for locating a sealed hit inside a pack.

Never reads the checker's exports or code; reads only its id/hit/kind output. Scratch goes to tmp/.

Usage: ../../../../.venv/bin/python qc_packs.py PACKS.jsonl [--others DIR,...]
v1.1: the ROUGE-L pack text also skips program-derived lexicon parts (key-word forms, state words, inert-context
vocabulary, lint summaries) and the filler items drawn from the shared pool.
Writes tmp/qc/<stem>.* and qc_report.json (counts only).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[2]
PY = str(LEAN.parent / ".venv" / "bin" / "python")
CHECKER = LEAN / "sealed_nd" / "qc" / "sealed_check.py"
TMP = HERE / "tmp" / "qc"


def strings(obj, path=""):
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("id", "sha256", "source_file"):
                continue
            yield from strings(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from strings(v, f"{path}[{i}]")


def entity_strings(p):
    ents = [p["org_name"], p["desk_name"]] + p["jargon_candidates"]
    for e in p["entity_types"]:
        ents += e.get("name_pool", []) + e["ids"]
    return ents


def run_checker(inp: Path, out: Path, summ: Path, entities: bool):
    cmd = [PY, str(CHECKER), str(inp), "--id-field", "id", "--out", str(out), "--summary", str(summ)]
    if entities:
        cmd += ["--structure-fields", "setting", "--entities-field", "qc_entities"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode not in (0, 3):
        raise SystemExit(f"checker failed rc={r.returncode}: {r.stderr[-400:]}")
    s = json.loads(summ.read_text())
    hits = [json.loads(l) for l in out.read_text().splitlines() if l.strip()]
    return s, [h for h in hits if h.get("hit")]


# ---------------------------------------------------------------- ROUGE-L (bit-parallel LCS)

def toks(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def lcs_len(a, b):
    """Bit-parallel LCS length (Hyyro 2004): V' = (V + (V & M)) | (V & ~M); LCS = zero bits of V."""
    if not a or not b:
        return 0
    m = len(b)
    mask = (1 << m) - 1
    pos = {}
    for i, t in enumerate(b):
        pos[t] = pos.get(t, 0) | (1 << i)
    v = mask
    for t in a:
        mm = pos.get(t, 0)
        u = v & mm
        v = ((v + u) | (v & ~mm)) & mask
    return m - bin(v).count("1")


def rouge_l(a, b):
    if not a or not b:
        return 0.0
    l = lcs_len(a, b)
    p, r = l / len(b), l / len(a)
    return 0.0 if l == 0 else 2 * p * r / (p + r)


def pack_text(p, generated=False):
    """Claude-written text of a pack (program-generated pools excluded unless asked)."""
    skip = {"ids", "lookalike_pairs", "name_pool", "jargon_candidates", "id_format", "persona_seed", "parents",
            "licence", "third_party", "split", "gen_version", "field_lexicon", "register", "currency",
            "date_window", "pack_agent", "quarter", "sector", "slot", "concept_groups", "disjointness_list",
            "predicate", "key_words", "key_word_forms", "state_words", "forms_dropped_as_markers",
            "inert_context_vocab", "f10_f7_lint", "name_lint", "entity", "members", "filler_items"}

    def walk(o, key=""):
        if key in skip and not generated:
            return
        if isinstance(o, str):
            yield o
        elif isinstance(o, dict):
            for k, v in o.items():
                if k in ("id", "sha256", "source_file", "key", "type", "kind", "value_type", "entity", "role",
                         "sign", "concept_group"):
                    continue
                yield from walk(v, k)
        elif isinstance(o, list):
            for v in o:
                yield from walk(v, key)
    return " ".join(walk(p))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("packs")
    ap.add_argument("--others", default="", help="comma list of other pack JSONL files for the cross ROUGE-L check")
    a = ap.parse_args(argv)
    TMP.mkdir(parents=True, exist_ok=True)
    src = Path(a.packs)
    packs = [json.loads(l) for l in src.read_text().splitlines() if l.strip()]
    stem = src.stem
    # 1) whole packs with entity field
    qc_in = TMP / f"{stem}.qc_in.jsonl"
    with qc_in.open("w") as fh:
        for p in packs:
            q = dict(p)
            q["qc_entities"] = entity_strings(p)
            fh.write(json.dumps(q, ensure_ascii=False) + "\n")
    s1, h1 = run_checker(qc_in, TMP / f"{stem}.sealedqc.jsonl", TMP / f"{stem}.sealedqc.summary.json", True)
    # 2) component strings (one object per string) to locate hits
    comp = TMP / f"{stem}.components.jsonl"
    n = 0
    with comp.open("w") as fh:
        for p in packs:
            for path, s in strings(p):
                fh.write(json.dumps({"id": f"{p['id']}#{path}", "text": s}, ensure_ascii=False) + "\n")
                n += 1
    s2, h2 = run_checker(comp, TMP / f"{stem}.components.sealedqc.jsonl",
                         TMP / f"{stem}.components.sealedqc.summary.json", False)
    # 3) ROUGE-L within the file and against others
    texts = {p["id"]: toks(pack_text(p)) for p in packs}
    ids = list(texts)
    worst, over = 0.0, []
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            r = rouge_l(texts[ids[i]], texts[ids[j]])
            worst = max(worst, r)
            if r >= 0.7:
                over.append([ids[i], ids[j], round(r, 3)])
    settings = {p["id"]: toks(p["setting"]) for p in packs}
    worst_set = 0.0
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            worst_set = max(worst_set, rouge_l(settings[ids[i]], settings[ids[j]]))
    cross = {"files": [], "worst": 0.0, "over_0_7": []}
    for f in [x for x in a.others.split(",") if x]:
        oth = [json.loads(l) for l in Path(f).read_text().splitlines() if l.strip()]
        cross["files"].append({"path": f, "packs": len(oth)})
        ot = {o.get("id", str(k)): toks(pack_text(o)) for k, o in enumerate(oth)}
        for i in ids:
            for k, t in ot.items():
                r = rouge_l(texts[i], t)
                cross["worst"] = max(cross["worst"], r)
                if r >= 0.7:
                    cross["over_0_7"].append([i, k, round(r, 3)])
    rep = {
        "input": str(src.relative_to(HERE)) if src.is_relative_to(HERE) else str(src),
        "input_sha256": hashlib.sha256(src.read_bytes()).hexdigest(),
        "packs": len(packs),
        "sealed_check": {
            "checker_sha256": s1.get("checker_sha256"), "suite_sha256": s1.get("suite_sha256"),
            "p_vocab_loaded": s1["settings"].get("p_vocab_loaded"),
            "whole_packs": {"rows": s1["rows"], "rows_hit": s1["rows_hit"],
                            "kinds": {k: v["rows"] for k, v in s1["kinds"].items() if v["rows"]}},
            "components": {"rows": s2["rows"], "rows_hit": s2["rows_hit"],
                           "kinds": {k: v["rows"] for k, v in s2["kinds"].items() if v["rows"]}},
            "hit_pack_ids": sorted({h["id"] for h in h1}),
            "hit_component_ids": sorted({h["id"] for h in h2}),
        },
        "rouge_l": {"pairs": len(ids) * (len(ids) - 1) // 2, "worst_pack_pair": round(worst, 4),
                    "over_0_7": over, "worst_setting_pair": round(worst_set, 4), "cross": cross},
    }
    out = HERE / "tmp" / "qc" / f"{stem}.qc_report.json"
    out.write_text(json.dumps(rep, indent=1) + "\n")
    print(json.dumps(rep["sealed_check"], indent=1))
    print(json.dumps({k: v for k, v in rep["rouge_l"].items() if k != "cross"}),
          json.dumps({"cross_worst": cross["worst"], "cross_over": len(cross["over_0_7"])}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
