#!/usr/bin/env python3
"""families/T07/merged_pools.py: how the T07 generator loads the v2 pools, and the independent G0 verdict.

A NEW, read-only file. The T07 pools are three layers (build_redo2.py admit, haiku/redo3/admit_redo3.py, G0_SPEC.md
section 7):
  v1      pools/*.json            frozen 13 Oct (freeze_pools.py), read-only, never changed
  redo2   pools/redo2/*_add.json  the supplement written by build_redo2.py admit (the v2 additions; MANIFEST.json)
  redo3   pools/redo3/*_add.json  the last supplement, written by haiku/redo3/admit_redo3.py (packs and yn_misses
                                  wordings only; MANIFEST.json)
Nothing in plugin.py, authoring.py or solver_b.py reads a pool path (the pools feed the generator that runs after the
pilot spec), so there is no path to refresh: the generator must call `load()` below (or merge the same files by the same
rule). `load()` returns all three layers; `load(through="redo2")` is the baseline the redo3 tasks were authored against
(the redo3 builders read it, so their task files stay reproducible after the redo3 freeze). Merge rule (also in
pools/redo2/MANIFEST.json and pools/redo3/MANIFEST.json "merge_rule"):
  packs       v1 packs.json + redo3 packs_add.json (redo2 does not redo packs; redo3 packs are all training)
  skins       v1 skins.json items + redo2 skins_add.json items
  attacks     v1 attacks.json items + redo2 attacks_add.json items
  wordings    v1 wordings.json items + redo2 wordings_add.json items + redo3 wordings_add.json items (each carries its
              admitted form_id)
  documents   v1 documents.json items + redo2 documents_add.json items: ONE text per Mode F brief (a redo2 text carries
              `v1_brief`; a v1 text's `internal_id` is its brief)
  lexicon     v1 lexicon.json forms (statuses unchanged) + redo2 lexicon_add.json forms + redo3 lexicon_add.json forms;
              use only status "admitted"
Every file is checked against the sha256 in its MANIFEST before it is used (a changed pool file raises PoolError).

`verdict(pools)` recomputes every G0 section 4 target line from the merged pool contents (not from the counts the
admit stage printed), plus the G-LEX gate (every form a wording or a Mode F text uses is admitted: 2 distinct
extractors, all agreeing; 3 for the strict kinds, which T07 does not have) and the G3-H bar (>= 98% per register, in each
read pass). Targets are the ones in freeze_pools.py (G0 section 4); none is lowered. READY = no shortfall.

  run (from lean/c2_build):
    /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python families/T07/merged_pools.py
"""
from __future__ import annotations

import functools
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import lexicon as LX  # noqa: E402
from families.T07 import authoring as A  # noqa: E402
from families.T07 import freeze_pools as FZ  # noqa: E402
from families.T07 import plugin as P  # noqa: E402

HERE = Path(__file__).resolve().parent
V1 = HERE / "pools"
R2 = V1 / "redo2"
R3 = V1 / "redo3"
R4 = V1 / "heldout_a54"       # PREREG A54: dev-only (held-out) question wordings; wordings_add.json + lexicon_add.json
LAYERS = ("redo2", "redo3", "heldout_a54")
G3H_BAR = FZ.G3H_BAR


class PoolError(RuntimeError):
    pass


def _json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def _verified(root: Path, manifest: dict, name: str):
    """A pool file, loaded after its sha256 is checked against the manifest that froze it."""
    want = manifest["pool_files"].get(name, {}).get("sha256")
    p = root / name
    if not p.is_file() or want is None:
        raise PoolError(f"{p}: not listed in its MANIFEST or missing")
    if hashlib.sha256(p.read_bytes()).hexdigest() != want:
        raise PoolError(f"{p}: sha256 differs from its MANIFEST (the pool changed after the freeze)")
    return _json(p)


def load(v1: Path = V1, r2: Path = R2, r3: Path | None = None, through: str = "heldout_a54", r4: Path | None = None) -> dict:
    """The merged v2 pools: {packs, skins, attacks, wordings, documents, lexicon, g3h, records, manifests}.
    through="heldout_a54" (default) merges every layer; "redo3" stops before the A54 held-out wording layer; "redo2"
    stops before the redo3 supplement (the baseline the redo3 tasks were authored against). r3 / r4 default to the
    folders next to r2 (pools/redo3, pools/heldout_a54)."""
    if through not in LAYERS:
        raise PoolError(f"through must be one of {LAYERS}, not {through!r}")
    r3 = Path(r3) if r3 is not None else Path(r2).parent / "redo3"
    m1, m2 = _json(v1 / "MANIFEST.json"), _json(r2 / "MANIFEST.json")
    if m1["g0_sha256"] != m2["g0_sha256"] or m1["g0_sha256"] != P.T07Plugin.G0_SHA256_AUTHORED:
        raise PoolError("G0 spec sha256 differs between v1, redo2 and plugin.py")
    f1 = {n: _verified(v1, m1, n) for n in ("packs.json", "skins.json", "attacks.json", "wordings.json",
                                            "documents.json", "lexicon.json", "g3h_record.json")}
    f2 = {n: _verified(r2, m2, n) for n in ("skins_add.json", "attacks_add.json", "wordings_add.json",
                                            "documents_add.json", "lexicon_add.json", "g3h_record.json")}
    docs = f1["documents.json"]["items"] + f2["documents_add.json"]["items"]
    briefs = [d.get("v1_brief") or d["internal_id"] for d in docs]
    dup = sorted(b for b, n in Counter(briefs).items() if n > 1)
    if dup:
        raise PoolError(f"more than one Mode F text for brief(s) {dup[:3]}")
    pools = {
        "packs": f1["packs.json"]["packs"],
        "skins": f1["skins.json"]["items"] + f2["skins_add.json"]["items"],
        "attacks": f1["attacks.json"]["items"] + f2["attacks_add.json"]["items"],
        "wordings": f1["wordings.json"]["items"] + f2["wordings_add.json"]["items"],
        "documents": docs,
        "lexicon": f1["lexicon.json"]["forms"] + f2["lexicon_add.json"]["forms"],
        "canonical_status_r2": f2["lexicon_add.json"]["canonical_status_r2"],
        "g3h": {"v1": f1["g3h_record.json"]["registers"], "redo2": f2["g3h_record.json"]["registers"]},
        "manifests": {"v1": m1, "redo2": m2},
    }
    if through == "redo2":
        return pools
    m3 = _json(r3 / "MANIFEST.json")
    if m3["g0_sha256"] != P.T07Plugin.G0_SHA256_AUTHORED:
        raise PoolError("G0 spec sha256 differs between redo3 and plugin.py")
    add = {n: _verified(r3, m3, n) for n in REDO3_FILES}
    pools = merge_redo3(pools, add, m3)
    if through == "redo3":
        return pools
    r4 = Path(r4) if r4 is not None else Path(r2).parent / "heldout_a54"
    m4 = _json(r4 / "MANIFEST.json")
    if m4["g0_sha256"] != P.T07Plugin.G0_SHA256_AUTHORED:
        raise PoolError("G0 spec sha256 differs between heldout_a54 and plugin.py")
    add4 = {n: _verified(r4, m4, n) for n in HELDOUT_FILES}
    return merge_heldout(pools, add4, m4)


REDO3_FILES = ("packs_add.json", "wordings_add.json", "lexicon_add.json")
HELDOUT_FILES = ("wordings_add.json", "lexicon_add.json")


def merge_heldout(pools: dict, add: dict, manifest: dict) -> dict:
    """The A54 supplement (held-out question wordings and their admitted forms) added on top of v1 + redo2 + redo3. Pure.
    Ids and texts must be new, every row must be held out, and every wording's form must be in the supplement."""
    words, forms = add["wordings_add.json"]["items"], add["lexicon_add.json"]["forms"]
    for key, rows, field in (("wordings", words, "wording_id"), ("lexicon", forms, "form_id")):
        taken = {x[field] for x in pools[key]}
        dup = sorted(x[field] for x in rows if x[field] in taken)
        if dup or len({x[field] for x in rows}) != len(rows):
            raise PoolError(f"heldout_a54 {key}: an id repeats an earlier one or another A54 one {dup[:3]}")
    texts = {_norm_text(x["text"]) for x in pools["wordings"]}
    if any(_norm_text(x["text"]) in texts for x in words):
        raise PoolError("heldout_a54 wordings: a text repeats an earlier wording")
    if not all(x["held_out"] for x in words) or not all(f["held_out"] and f["status"] == "admitted" for f in forms) \
            or {w["form_id"] for w in words} - {f["form_id"] for f in forms}:
        raise PoolError("heldout_a54: every row must be held out, admitted and have its form in the supplement")
    return dict(pools, wordings=pools["wordings"] + words, lexicon=pools["lexicon"] + forms,
                manifests=dict(pools["manifests"], heldout_a54=manifest))


def _norm_text(t: str) -> str:
    return " ".join(t.casefold().split())


def merge_redo3(pools: dict, add: dict, manifest: dict) -> dict:
    """The redo3 supplement (packs_add / wordings_add / lexicon_add, each as loaded) added to the v1 + redo2 pools. Pure:
    `pools` is not changed. Ids and texts must be new (PoolError otherwise): the supplement only adds."""
    packs, words, forms = add["packs_add.json"]["items"], add["wordings_add.json"]["items"], add["lexicon_add.json"]["forms"]
    for key, rows, field in (("packs", packs, "pack_id"), ("wordings", words, "wording_id"),
                             ("lexicon", forms, "form_id")):
        taken = {x[field] for x in pools[key]}
        dup = sorted(x[field] for x in rows if x[field] in taken)
        if dup or len({x[field] for x in rows}) != len(rows):
            raise PoolError(f"redo3 {key}: an id repeats an earlier one or another redo3 one {dup[:3]}")
    texts = {_norm_text(x["text"]) for x in pools["wordings"]}
    if any(_norm_text(x["text"]) in texts for x in words):
        raise PoolError("redo3 wordings: a text repeats an earlier wording")
    stores = {p["store"].casefold() for p in pools["packs"]}
    if any(p["store"].casefold() in stores for p in packs):
        raise PoolError("redo3 packs: a store name repeats an earlier pack")
    return dict(pools, packs=pools["packs"] + packs, wordings=pools["wordings"] + words,
                lexicon=pools["lexicon"] + forms, manifests=dict(pools["manifests"], redo3=manifest))


def _short(rows: list, name: str, want: int, got: int, note: str = "") -> None:
    if got < want:
        r = {"item": name, "target": want, "admitted": got, "short_by": want - got}
        if note:
            r["note"] = note
        rows.append(r)


def glex_problems(pools: dict) -> list:
    """G-LEX on the merged lexicon: a form is admitted only with >= required distinct extractors that all picked its
    sem (a dissent rejects for good); every wording and every Mode F canonical sentence must use an admitted form."""
    probs, forms = [], {f["form_id"]: f for f in pools["lexicon"]}
    for fid, f in forms.items():
        need = 3 if f["kind"] in LX.STRICT_KINDS else 2
        ex = f["extractions"]
        agree = len({e for e, s in ex if s == f["sem_id"]})
        if f["status"] == "admitted" and (any(s != f["sem_id"] for _, s in ex) or agree < need):
            probs.append(f"{fid}: marked admitted without {need}/{need} agreeing extractors")
        if f["status"] != "admitted" and not any(s != f["sem_id"] for _, s in ex) and agree >= need \
                and f.get("status") != "unit_fail":
            probs.append(f"{fid}: {f['status']} although {agree} extractors agree")
    for w in pools["wordings"]:
        f = forms.get(w["form_id"])
        if f is None or f["status"] != "admitted" or f["text"] != w["text"]:
            probs.append(f"wording {w['wording_id']}: form {w['form_id']} is not an admitted form of its text")
    for d in pools["documents"]:
        for fid in d["lexicon_form_ids"]:
            f = forms.get(fid)
            if f is None or f["status"] != "admitted":
                probs.append(f"document {d['doc_id']}: canonical form {fid} is not admitted")
    return probs


@functools.lru_cache(maxsize=None)
def _whole_re(surface: str):
    return re.compile(r"(?<![a-z])" + re.escape(surface) + r"(?![a-z])")


def _whole(surface: str, name: str) -> bool:
    return _whole_re(surface).search(name.casefold()) is not None


def pack_problems(pools: dict) -> list:
    """G0 section 4 / S2 on the merged packs, from their contents: every pack passes authoring.lint_pack; the packs in
    pool order pass authoring.check_packs (none would be dropped: no surface names another dimension, no store or
    customer name holds a surface of the packs before it, store names are new); and, for the packs a redo3 round added
    (piece id t07r3.*), the direction check_packs does not look at: no earlier or later store / customer name (seed
    names included) holds one of their surfaces and none of their names holds a surface of another pack. v1 is frozen
    and is not re-judged in that direction (one v1 customer name holds a v1 level word)."""
    packs, probs = pools["packs"], []
    for p in packs:
        probs += [f"{p['pack_id']}: {x}" for x in A.lint_pack(p, len(p["ladder"]))]
    _kept, dropped = A.check_packs(packs)
    probs += [f"{d['pack']['pack_id']}: S2 uniqueness clash {d['clash']} holds {d['holds']} store_taken "
              f"{d['store_taken']}" for d in dropped]
    new = [p for p in packs if str(p.get("piece_id", "")).startswith("t07r3.")]
    if new:
        names = ([p["store"] for p in packs] + [c for p in packs for c in p["customers"]] + list(P.STORES) +
                 list(P.STORES_HELD) + list(P.CUSTOMERS) + list(getattr(P, "CUSTOMERS_HELD", ())))
        surf = lambda p: {s.casefold() for f in ("ladder", "regions", "categories") for s in p[f]}  # noqa: E731
        for p in new:
            own = {n for n in (p["store"], *p["customers"])}
            for n in names:
                hit = sorted(s for s in surf(p) if _whole(s, n))
                if hit and n not in own:
                    probs.append(f"{p['pack_id']}: surface {hit} is a whole word of the name {n!r}")
            others = set().union(*(surf(q) for q in packs if q is not p), set(A._all_surfaces()))
            held = sorted((n, s) for n in own for s in others if _whole(s, n))
            if held:
                probs.append(f"{p['pack_id']}: its own name holds another pack's surface {held[:3]}")
    return probs


def verdict(pools: dict) -> dict:
    """Every G0 target line against the merged pools. {"ready": bool, "shortfalls": [...], "gates": {...}}."""
    short: list = []
    c1 = pools["manifests"]["v1"]["counts"]
    pk = pools["packs"]
    _short(short, "packs training (S24)", FZ.PACK_NEEDED["training"], sum(not p["held_out"] for p in pk))
    _short(short, "packs held out (S24)", FZ.PACK_NEEDED["held_out"], sum(p["held_out"] for p in pk))
    _short(short, "packs asked (G0 section 4)", FZ.PACK_ASKED, len(pk),
           "S24 minimum (32 training + 4 held out) is met; only the 60 asked line is short")
    skin_reg = Counter(s["register"] for s in pools["skins"])
    for r, want in FZ.MODE_T_TARGET.items():
        _short(short, f"Mode T skins {r}", want, skin_reg.get(r, 0))
    doc_reg = Counter(d["register"] for d in pools["documents"])
    for r, want in sorted(c1["documents_mode_f"]["planned_by_register"].items()):
        _short(short, f"Mode F texts {r}", want, doc_reg.get(r, 0))
    _short(short, "attack lines (G0 section 4)", FZ.ATTACK_TARGET, len(pools["attacks"]))
    adm = [f for f in pools["lexicon"] if f["status"] == "admitted"]
    canon = Counter(f["sem_id"] for f in adm if f["origin"] in ("canonical", "canonical_r2"))
    para = Counter(f["sem_id"] for f in adm if f["origin"] in ("haiku_form", "haiku_form_r2"))
    for s in sorted(P.SEMS):
        _short(short, f"canonical forms {s}", FZ.CANON_PER_SEM, canon.get(s, 0))
        _short(short, f"Haiku paraphrases {s} (>=6 admitted)", FZ.PARAPHRASE_ADMIT, para.get(s, 0))
    w = Counter((x["qform"], x["held_out"]) for x in pools["wordings"])
    for q in FZ.QFORMS:
        _short(short, f"wordings training {q}", FZ.WORDING_TARGET["training"][q], w.get((q, False), 0))
        _short(short, f"wordings held out {q}", FZ.WORDING_TARGET["held_out"][q], w.get((q, True), 0))
    glex = glex_problems(pools)
    g3h = {}
    for rnd, regs in pools["g3h"].items():
        for reg, d in regs.items():
            g3h[f"{rnd}:{reg}"] = {"n": d["n"], "ok": d["ok"], "rate": round(d["ok"] / d["n"], 4),
                                   "pass": d["ok"] / d["n"] >= G3H_BAR}
    packp = pack_problems(pools)
    gates = {"G-LEX": {"pass": not glex, "problems": glex[:10],
                       "forms": Counter(f["status"] for f in pools["lexicon"])},
             "G3-H": {"bar": G3H_BAR, "pass": all(v["pass"] for v in g3h.values()), "per_register": g3h},
             "packs (G0 S2 uniqueness, lint_pack)": {"pass": not packp, "problems": packp[:10]}}
    return {"ready": not short and all(g["pass"] for g in gates.values()), "shortfalls": short,
            "n_shortfalls": len(short), "gates": gates,
            "counts": {"packs": len(pk), "packs_training": sum(not p["held_out"] for p in pk),
                       "packs_held_out": sum(p["held_out"] for p in pk), "skins": dict(sorted(skin_reg.items())),
                       "documents": dict(sorted(doc_reg.items())),
                       "attacks": len(pools["attacks"]), "wordings": len(pools["wordings"]),
                       "lexicon_admitted": len(adm)}}


def main() -> int:
    v = verdict(load())
    print(json.dumps(v, indent=1))
    print("READY" if v["ready"] else f"SHORT: {v['n_shortfalls']} target line(s) short")
    return 0 if v["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
