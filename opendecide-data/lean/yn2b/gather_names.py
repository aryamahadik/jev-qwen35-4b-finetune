"""gather_names.py: the name list for check_yn2b.py --names (SPEC.md section 7.7), programs only, CPU only.

SPEC 7.7: no pool name is a substring of any JevBench public string or of OHS-1/2 text; OHS-3 is checked by hash
comparison only (inside check_yn2b.ohs3_blind). This tool only COLLECTS the names; it reads no held-out file.

Names collected, per family (source):
  1. every mv_core.NamePool person ("First Last", first and last from the pool of ANY split) and organisation
     ("Stem <org suffix>") that occurs in a shown text of the assembled rows (state, instructions, options, card);
  2. the family name files the builders wrote: yn2b/names_<key>.json ({source: [names]}; F1, F5);
  3. optional (--f6-build): F6's latent names (officer, name, org, bg_from and names_used), from a deterministic
     in-process rebuild (gen3_def_literal.build_all; nothing is written), as yn2b/f6_precheck.py does;
  4. optional (--devx-build): the people and organisations of reviewer R's devx latents (devx_decontam.devx_names).
Names are checked as the rows show them. A one-word name from a family file (F1 lists its organisation stems, F6 some
item names) is checked alone where a row shows it alone, and in its two-word form where a row shows it next to another
capitalised word ("Heron" shown only as "Heron Energy" is checked as "Heron Energy"); a one-word name no row shows is
not checked. 1 Oct: 7 F1 stems that are also English words or names (Gaman, Helix, Heron, Mason, Minor, Renin, Velox)
occur in JevBench / OHS-1/2 text as words; no F1 row shows any of them alone. Output: JSON
{source: [sorted names]}.

  ../.venv/bin/python yn2b/gather_names.py --train <assembled train> --dev <dev files,...> --devx <devx> \\
        --f6-build --devx-build --out <names.json>
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yn2b_common as yc  # noqa: E402

if str(yc.GEN3) not in sys.path:
    sys.path.insert(0, str(yc.GEN3))

PERSON_RE = re.compile(r"(?=\b([A-Z][a-z]+) ([A-Z][a-z]+)\b)")  # lookahead: overlapping pairs ("A B C" -> AB, BC)


def pool_index():
    """(first names, surnames, stems, org-name regex) over every split's mv_core pool."""
    import mv_core as mv
    P = mv._pools()
    first = set().union(*[set(p["first"]) for p in P.values()])
    last = set().union(*[set(p["last"]) for p in P.values()])
    stems = set().union(*[set(p["stem"]) for p in P.values()])
    suf = sorted(mv._ORG_SUFFIX, key=len, reverse=True)
    org_re = re.compile(r"(?=\b([A-Z][a-z]+) (" + "|".join(re.escape(x) for x in suf) + r")\b)")
    return first, last, stems, org_re


def row_texts(r):
    out = [r.get("state") or "", r.get("instructions") or ""]
    out += [o for o in (r.get("options") or []) if isinstance(o, str)]
    out += [r.get("card") or ""]
    return out


def names_in_text(text, idx):
    """Pool persons ("First Last") and organisations ("Stem Suffix") shown in one text."""
    first, last, stems, org_re = idx
    out = {f"{a} {b}" for a, b in PERSON_RE.findall(text) if a in first and b in last}
    out |= {f"{a} {b}" for a, b in org_re.findall(text) if a in stems}
    return out


def names_in_rows(rows, idx):
    out = defaultdict(set)
    for r in rows:
        for t in row_texts(r):
            out[r["source"]] |= names_in_text(t, idx)
    return out


def family_files(yn2b_dir=yc.YN2B):
    """{source: names} from yn2b/names_*.json (builders' name pools)."""
    out = defaultdict(set)
    for p in sorted(Path(yn2b_dir).glob("names_*.json")):
        obj = json.loads(p.read_text())
        for fam, ns in obj.items():
            out[fam] |= {n for n in ns if isinstance(n, str) and n.strip()}
    return out


def f6_names():
    import f6_precheck as f6
    import gen3_def_literal as g
    return {"gd_gen3_def_literal": set(f6.pool_names(g.build_all()))}


def devx_names():
    import build_devx as bd
    import devx_decontam as dd
    out = defaultdict(set)
    for fam, n in dd.devx_names(bd.build(list(bd.MODULES))):
        out[fam].add(n)
    return out


CAP_RE = re.compile(r"[A-Z][a-z]+")


def single_name_forms(rows_by_family, names):
    """{family: names to check for its one-word names}: a one-word name is checked alone when a row shows it alone
    (no capitalised word right before or after it, across one space); every occurrence next to a capitalised word is
    checked in that two-word form instead ("Heron Energy", "Gaman Primary"). A one-word name no row shows is dropped."""
    out = {}
    for fam, ns in names.items():
        single = {n for n in ns if len(n.split()) == 1}
        if not single:
            continue
        got = set()
        for r in rows_by_family.get(fam, []):
            for t in row_texts(r):
                toks = [(m.group(0), m.start(), m.end()) for m in CAP_RE.finditer(t)]
                for j, (w, a, b) in enumerate(toks):
                    if w not in single or (a and t[a - 1].isalpha()) or (b < len(t) and t[b].isalpha()):
                        continue
                    prev = toks[j - 1] if j and toks[j - 1][2] == a - 1 and t[a - 1] == " " else None
                    nxt = toks[j + 1] if j + 1 < len(toks) and toks[j + 1][1] == b + 1 and t[b] == " " else None
                    if prev:
                        got.add(f"{prev[0]} {w}")
                    if nxt:
                        got.add(f"{w} {nxt[0]}")
                    if not prev and not nxt:
                        got.add(w)
        out[fam] = got
    return out


def gather(rows, extra=()):
    """Pool persons / organisations shown in the rows, plus the extra name sets (family files, F6, devx); one-word
    extra names only when shown alone (see the module docstring)."""
    idx = pool_index()
    out = names_in_rows(rows, idx)
    ext = defaultdict(set)
    for e in extra:
        for fam, ns in e.items():
            ext[fam] |= set(ns)
    by_fam = defaultdict(list)
    for r in rows:
        by_fam[r["source"]].append(r)
    forms = single_name_forms(by_fam, ext)
    for fam, ns in ext.items():
        out[fam] |= {n for n in ns if len(n.split()) > 1} | forms.get(fam, set())
    return {f: sorted(v) for f, v in sorted(out.items())}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--train", required=True, help="assembled train rows (path)")
    ap.add_argument("--dev", default="", help="comma list of assembled dev files (paths)")
    ap.add_argument("--devx", default="", help="assembled devx rows (path)")
    ap.add_argument("--f6-build", action="store_true")
    ap.add_argument("--devx-build", action="store_true")
    ap.add_argument("--no-family-files", action="store_true")
    ap.add_argument("--family-dir", default=str(yc.YN2B), help="where the names_*.json files are")
    ap.add_argument("--out", required=True)
    ap.add_argument("--overwrite", action="store_true")
    a = ap.parse_args(argv)
    rows = yc.read_jsonl(a.train)
    for p in [x for x in a.dev.split(",") if x] + ([a.devx] if a.devx else []):
        rows += yc.read_jsonl(p)
    extra = [] if a.no_family_files else [family_files(a.family_dir)]
    if a.f6_build:
        extra.append(f6_names())
    if a.devx_build:
        extra.append(devx_names())
    res = gather(rows, extra)
    yc.write_json(yc.guard_out(a.out, overwrite=a.overwrite), res)
    print(json.dumps({f: len(v) for f, v in res.items()}))
    return res


if __name__ == "__main__":
    main()
