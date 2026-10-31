"""formats-2: build the instruction wording pools and the register / locale tables.

Outputs (every object carries a stable `id`):
  wordings/family_pools.jsonl   F1-F13 and COMMIT.<type> pools (spec 2.1 / 6: >= 30 per family, >= 5 per card)
  wordings/public_pools.jsonl   the 14 public datasets (spec 3.1 / 6: >= 3 per dataset; here 7)
  locales/*.json(l)             registers, locales, US/GB spelling and vocabulary, date / time / number formats,
                                currencies, units
Lints (all must pass; the build fails otherwise): negcount k_syn = k_all = 0, the banned operator list, family bans,
length, and ROUGE-L < 0.7 between every pair of wordings (both spellings).
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict

from common_f2 import HERE, progress, write_json, write_jsonl
from lint_f2 import lint_text, rouge_pairs, tokens
import locales_src as L
from wordings_src_a import POOLS_A
from wordings_src_b import POOLS_B
from wordings_src_c import POOLS_C
from wordings_src_d import PUBLIC

OUTW = HERE / "wordings"
OUTL = HERE / "locales"
REG_BY_LETTER = {r["wording_family"]: r["name"] for r in L.REGISTERS}
F12_FORMS = ["C-OUT", "C-ACT", "C-TOOL", "C-PARAM", "C-DEFECT", "C-VALUE", "C-INV", "Y-CALLX", "Y-ASK", "Y-FIT",
             "Y-DIRECT", "Y-VALID", "Y-CORRECT"]
F12_GEN_REG = ["formal", "plain", "plain", "plain", "casual", "procedural", "terse", "formal"]


# ------------------------------------------------------------------ spelling maps
def spelling_pairs():
    out = []
    for v in sorted(set(L.IZE_VERBS)):
        stem = v[:-3]
        for us_suf, gb_suf in (("ize", "ise"), ("izes", "ises"), ("ized", "ised"), ("izing", "ising")):
            out.append((stem + us_suf, stem + gb_suf, "ize_ise", False, "GB -ize (Oxford) is also correct"))
        if v in L.IZATION:
            out.append((stem + "ization", stem + "isation", "ize_ise", False, "GB -ization (Oxford) is also correct"))
            out.append((stem + "izations", stem + "isations", "ize_ise", False, ""))
    for v in L.YZE_VERBS:
        stem = v[:-3]
        for us_suf, gb_suf in (("yze", "yse"), ("yzes", "yses"), ("yzed", "ysed"), ("yzing", "ysing")):
            out.append((stem + us_suf, stem + gb_suf, "yze_yse", False, ""))
    out += list(L.PAIRS)
    seen, uniq = set(), []
    for p in out:
        if p[0] not in seen:
            seen.add(p[0])
            uniq.append(p)
    return uniq


def _case_like(src, word):
    if src.isupper() and len(src) > 1:
        return word.upper()
    if src[:1].isupper():
        return word[:1].upper() + word[1:]
    return word


def make_converter(pairs, direction):
    m = {}
    for us, gb, cat, sense, note in pairs:
        if sense or " " in us or " " in gb:
            continue
        a, b = (us, gb) if direction == "us2gb" else (gb, us)
        m[a.lower()] = b
    rx = re.compile(r"\b(" + "|".join(sorted(map(re.escape, m), key=len, reverse=True)) + r")\b", re.I)

    def conv(text):
        return rx.sub(lambda mo: _case_like(mo.group(0), m[mo.group(0).lower()]), text)
    return conv


# ------------------------------------------------------------------ wordings
def family_rows(to_us, to_gb):
    rows = []
    for pools in (POOLS_A, POOLS_B, POOLS_C):
        for pool, fams in pools.items():
            fam = pool.split(".")[0]
            ctype = pool.split(".")[1] if pool.startswith("COMMIT.") else None
            for wf, lst in fams.items():
                for i, (forms, text) in enumerate(lst, 1):
                    if pool == "F12":
                        reg = F12_GEN_REG[i - 1] if wf == "GEN" else ("formal" if i == 1 else "plain")
                    else:
                        reg = REG_BY_LETTER[wf]
                    rows.append({"id": f"wd.{pool}.{wf}.{i:02d}", "kind": "family", "pool": pool, "family": fam,
                                 "commit_type": ctype, "wording_family": f"{pool}.{wf}", "register": reg,
                                 "forms": [forms], "text": to_us(text), "text_gb": to_gb(text),
                                 "position": "instructions, before the question"})
    return rows


def public_rows(to_us, to_gb):
    rows = []
    for ds, fams in PUBLIC.items():
        for wf, lst in fams.items():
            for i, (forms, reg, text) in enumerate(lst, 1):
                rows.append({"id": f"wd.pub.{ds}.{i:02d}", "kind": "public", "pool": f"PUB.{ds}", "dataset": ds,
                             "wording_family": f"PUB.{ds}.{wf}", "register": reg, "forms": [forms],
                             "text": to_us(text), "text_gb": to_gb(text),
                             "position": "instructions, before the question"})
    return rows


def usable_counts(rows):
    """Per pool x wording family x form: wordings usable on that form (form-specific + 'any')."""
    out = defaultdict(dict)
    by = defaultdict(list)
    for r in rows:
        by[(r["pool"], r["wording_family"])].append(r)
    for (pool, wf), rs in by.items():
        forms = sorted({f for r in rs for f in r["forms"] if f != "any"})
        if pool == "F12":
            continue
        if not forms:
            forms = ["any"]
        for f in forms:
            out[pool].setdefault(wf, {})[f] = sum(1 for r in rs if f in r["forms"] or "any" in r["forms"])
    # F12: per form, its own wordings + GEN (any)
    f12 = [r for r in rows if r["pool"] == "F12"]
    if f12:
        gen = sum(1 for r in f12 if r["forms"] == ["any"])
        for f in F12_FORMS:
            out["F12"][f"F12.{f}"] = {f: sum(1 for r in f12 if r["forms"] == [f]) + gen,
                                      "form_specific": sum(1 for r in f12 if r["forms"] == [f])}
    return dict(out)


def main():
    pairs = spelling_pairs()
    to_gb = make_converter(pairs, "us2gb")
    to_us = make_converter(pairs, "gb2us")
    fam = family_rows(to_us, to_gb)
    pub = public_rows(to_us, to_gb)
    allw = fam + pub
    problems = []
    for r in allw:
        for t in {r["text"], r["text_gb"]}:
            for p in lint_text(t, r["family"] if r["kind"] == "family" else None):
                problems.append((r["id"], p))
        r["has_gb_variant"] = r["text"] != r["text_gb"]
        r["n_words"] = len(tokens(r["text"]))
    ids = Counter(r["id"] for r in allw)
    problems += [(i, "duplicate id") for i, n in ids.items() if n > 1]
    texts = Counter(r["text"].lower() for r in allw)
    problems += [(t[:40], "duplicate text") for t, n in texts.items() if n > 1]
    # G11: every pair of different wordings, every spelling variant against every other (US-US, US-GB, GB-GB),
    # under both tokenizers (lint_f2.rouge_pairs)
    rp = rouge_pairs([(r["id"], r["text"]) for r in allw] +
                     [(r["id"], r["text_gb"]) for r in allw if r["has_gb_variant"]])
    problems += [(f"{a}~{b}", f"rouge-l {s}") for a, b, s in rp]
    near = rouge_pairs([(r["id"], r["text"]) for r in allw] +
                       [(r["id"], r["text_gb"]) for r in allw if r["has_gb_variant"]], thr=0.6)
    rouge_max = {"pairs_ge_0.6": len(near), "max": max((x[2] for x in near), default=None),
                 "max_pair": max(near, key=lambda x: x[2])[:2] if near else None}
    if problems:
        for p in problems:
            print("PROBLEM", p)
        raise SystemExit(f"{len(problems)} wording problems")
    # quotas
    quota = {}
    for pool in sorted({r["pool"] for r in fam}):
        n = sum(1 for r in fam if r["pool"] == pool)
        quota[pool] = {"wordings": n, "ok_ge_30": n >= 30}
    for ds in sorted(PUBLIC):
        n = sum(1 for r in pub if r["dataset"] == ds)
        quota[f"PUB.{ds}"] = {"wordings": n, "ok_ge_3": n >= 3,
                              "framings": sorted({f for r in pub if r["dataset"] == ds for f in r["forms"]})}
    usable = usable_counts(allw)
    short = [(p, wf, f, n) for p, d in usable.items() for wf, fs in d.items() for f, n in fs.items()
             if f != "form_specific" and n < 5]
    if short:
        raise SystemExit(f"usable-per-card shortfall: {short}")
    sha_f = write_jsonl(OUTW / "family_pools.jsonl", fam)
    sha_p = write_jsonl(OUTW / "public_pools.jsonl", pub)
    # locales
    out = {}
    out["registers.json"] = write_json(OUTL / "registers.json", {"id": "registers.v1", "registers": L.REGISTERS})
    sp = [{"id": f"sp.{i:04d}", "us": us, "gb": gb, "category": cat, "sense_dependent": sense, "note": note}
          for i, (us, gb, cat, sense, note) in enumerate(pairs, 1)]
    out["spelling_us_gb.jsonl"] = write_jsonl(OUTL / "spelling_us_gb.jsonl", sp)
    vo = [{"id": f"vo.{i:03d}", "us": us, "gb": gb, "sense_dependent_or_ambiguous": amb, "note": note}
          for i, (us, gb, amb, note) in enumerate(L.VOCAB, 1)]
    out["vocab_us_gb.jsonl"] = write_jsonl(OUTL / "vocab_us_gb.jsonl", vo)
    out["date_formats.jsonl"] = write_jsonl(OUTL / "date_formats.jsonl", L.DATE_FORMATS)
    out["time_formats.jsonl"] = write_jsonl(OUTL / "time_formats.jsonl", L.TIME_FORMATS)
    out["number_formats.jsonl"] = write_jsonl(OUTL / "number_formats.jsonl", L.NUMBER_FORMATS)
    cur = [{"id": f"cur.{c}", "code": c, "name": n, "symbol": s, "unambiguous_forms": u, "minor_units": m,
            "ambiguous_symbol": a} for c, n, s, u, m, a in L.CURRENCIES]
    out["currencies.jsonl"] = write_jsonl(OUTL / "currencies.jsonl", cur)
    un = [{"id": i, "dimension": d, "name_us": nu, "name_gb": ng, "symbol": s, "to_si_base": f, "system": sy,
           "ambiguous": a, "note": no} for i, d, nu, ng, s, f, sy, a, no in L.UNITS] + L.TEMPERATURE
    out["units.jsonl"] = write_jsonl(OUTL / "units.jsonl", un)
    out["locales.json"] = write_json(OUTL / "locales.json", {"id": "locales.v1", "locales": L.LOCALES})
    # every locale reference resolves
    ids_d = {d["id"] for d in L.DATE_FORMATS}
    ids_t = {d["id"] for d in L.TIME_FORMATS}
    ids_n = {d["id"] for d in L.NUMBER_FORMATS}
    ids_c = {c[0] for c in L.CURRENCIES}
    for loc in L.LOCALES:
        assert set(loc["dates"]) <= ids_d and loc["default_date"] in ids_d, loc["id"]
        assert set(loc["times"]) <= ids_t and loc["number"] in ids_n and loc["percent"] in ids_n, loc["id"]
        assert loc["currency"] in ids_c, loc["id"]
    rep = {"family_pools_sha256": sha_f, "public_pools_sha256": sha_p, "quota": quota, "usable": usable,
           "counts": {"family_wordings": len(fam), "public_wordings": len(pub),
                      "with_gb_variant": sum(r["has_gb_variant"] for r in allw),
                      "registers": Counter(r["register"] for r in allw)},
           "locale_files_sha256": out,
           "locale_counts": {"spelling_pairs": len(sp), "vocab_pairs": len(vo), "date_formats": len(L.DATE_FORMATS),
                             "time_formats": len(L.TIME_FORMATS), "number_formats": len(L.NUMBER_FORMATS),
                             "currencies": len(cur), "units": len(un), "locales": len(L.LOCALES),
                             "registers": len(L.REGISTERS)},
           "lints": "negcount k=0, banned operator list, family bans (F4 G0 7.5 closed list, F8 G0 section 5), "
                    "length 2-70 words, ROUGE-L < 0.7 between every pair of wordings (every US / GB variant pair, "
                    "under both the builder tokenizer and a plain \\w+ tokenizer)",
           "rouge_max": rouge_max}
    write_json(HERE / "tmp" / "wordings_build.json", rep)
    progress(f"build_wordings: {len(fam)} family wordings in {len(quota) - len(PUBLIC)} pools, {len(pub)} public "
             f"wordings in {len(PUBLIC)} datasets; locales {json.dumps(rep['locale_counts'])}")
    print(json.dumps(rep["counts"], default=str))


if __name__ == "__main__":
    sys.path.insert(0, str(HERE))
    main()
