"""negtwins/block_twins.py: the twin builders of the G-block (GB, cap 15,000) and the metadata block (MD, cap 12,000), A42-D 7.1 / 7.2.

One command each, from c2_build, once the block exists (the frozen trained catalogue only; twins <= 5,000 and base rows + twins
<= the block cap; gold = 1 - base gold (complement) / base gold (equiv), never edited; program checks + G-TW 100%):

    python -B -m negtwins.block_twins gb [--apply]        bases = gblock/route_a42d/routed_block.jsonl (route_a42d.py finalize)
                                                          joined to gblock/candidates/*.jsonl; or c2_parts/GB/out/candidates_c2.jsonl
                                                          when the block is already assembled
    python -B -m negtwins.block_twins md [--apply]        bases = c2_parts/MD/out/candidates_c2.jsonl (meta_src/merge_md.py)
    python -B -m negtwins.block_twins md cardtasks        Haiku card-complement tasks for the two-line MD card types (round 1, 2)
    options: --rows FILE...  (any C2-schema rows, dry runs on mapper parts)   --target N

Without --apply the twins go to c2_parts/<B>/negtwins/ (sidecar) and nothing in out/ changes. With --apply the twin rows and
relations are appended to out/candidates_c2.jsonl / .relations.jsonl (earlier twins of this tool are replaced, so a rerun is
idempotent) and the MANIFEST / QC file records are updated; the base QC verdict is untouched, the twin gates are added to it.
A complement twin on a TWO-LINE card needs its base type's card certificate (cardcert_<b>_r1/r2 answers); card-free bases and
yes-only cards (A48 c wrap) need none.
"""
from __future__ import annotations

import datetime
import json
import sys
from collections import Counter
from pathlib import Path

from c2_kit import chunker

from . import checks as K
from . import core as C
from . import frozen as FZ
from . import plan as P
from . import rtw
from . import tasks as T

CB = rtw.CB
DATA = rtw.DATA
GB_DIR = CB / "gblock"
CFG = {"gb": {"cap": 15000, "twin_cap": 5000, "block": "gblock", "source": "c2_gblock", "family": "GB", "dir": DATA / "c2_parts" / "GB"},
       "md": {"cap": 12000, "twin_cap": 5000, "block": "metadata", "source": None, "family": "MD", "dir": DATA / "c2_parts" / "MD"}}
GEN = "tw1"


def read_jsonl(p: Path) -> list:
    return [json.loads(l) for l in p.open(encoding="utf-8") if l.strip()]


def gb_rows(routed: Path) -> list:
    """Routed G-block rows ({id, label, ...}) joined to their candidate text -> C2-shaped base rows (yes/no only)."""
    lab = {r["id"]: r for r in read_jsonl(routed)}
    out = []
    for fn in ("candidates.jsonl", "fix5_candidates.jsonl"):
        for l in (GB_DIR / "candidates" / fn).open(encoding="utf-8"):
            r = json.loads(l)
            x = lab.get(r["id"])
            if x is None or r.get("qtype") != "noul" or x.get("label") not in ("yes", "no"):
                continue
            out.append({"id": r["id"], "group_id": r["group_id"], "call_id": r.get("call_id") or r["group_id"], "source": "c2_gblock",
                        "state": r["state"], "qtype": "noul", "instructions": r["instructions"], "options": None,
                        "gold": 1 if x["label"] == "yes" else 0, "role": "base", "card": r.get("card"), "domain": r.get("domain"),
                        "meta": {"card_id": r.get("card_id"), "domain": r.get("domain"), "task_id": None,
                                 "licence": "the G-block source licence (gblock/SOURCES.md)"}})
    return out


def eligible(rows: list, allow_card_free: bool) -> list:
    out = []
    for r in rows:
        spec = (r.get("meta") or {}).get("neg_spec")
        b = P.base_record(r, "block", spec if spec and spec.get("core") else None, allow_card_free=allow_card_free)
        if b is not None:
            out.append(b)
    return out


def card_batch(types: dict, tag: str, r: int):
    return T._batch("polarity", T.card_items(types), f"negtw-cardcert-{tag}-r{r}-{GEN}", T.CARD_PROMPT)


def card_tasks(bases: list, tag: str) -> dict:
    types = {b["type"]: (b["defs"][0], b["defs"][1]) for b in bases if not b["one_sided"] and not b["card_free"]}
    out = {}
    for r in (1, 2):
        b = card_batch(types, tag, r)
        root = T.HERE / "haiku" / f"cardcert_{tag}_r{r}"
        if (root / "TASKS.json").exists() and json.loads((root / "TASKS.json").read_text())["batch_id"] != b.batch_id:
            rtw._supersede(root)
        out[r] = T._write(root, b, f"Haiku card-complement read ({tag})", T.POL_FORMAT, f"polarity:negtw_cardcert_{tag}", extra={"n_types": len(types)})
    return out


def certified(bases: list, tag: str):
    types = {b["type"]: (b["defs"][0], b["defs"][1]) for b in bases if not b["one_sided"] and not b["card_free"]}
    if not types:
        return set()
    reads = []
    for r in (1, 2):
        b, root = card_batch(types, tag, r), T.HERE / "haiku" / f"cardcert_{tag}_r{r}"
        files = sorted((root / "answers").glob("*.json")) if (root / "answers").exists() else []
        if not files:
            return None
        ans, probs = chunker.load_answers(b, {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in files})
        if probs:
            raise RuntimeError(f"{root.name}: {probs[:3]}")
        reads.append(T.relations(ans))
    return {k for k, v in T.card_decide(reads[0], reads[1]).items() if v}


def build(which: str, rows: list, target: int | None = None, apply: bool = False) -> dict:
    cfg = CFG[which]
    pats, pairs = FZ.load_trained()
    old = [r for r in rows if (r.get("meta") or {}).get("negtwin")]
    base_rows = [r for r in rows if not (r.get("meta") or {}).get("negtwin")]
    room = max(0, min(cfg["twin_cap"], cfg["cap"] - len(base_rows)))
    target = min(target or room, room)
    bases = eligible(base_rows, allow_card_free=which == "md")
    cert = certified(bases, which)
    rep = {"block": cfg["family"], "base_rows": len(base_rows), "eligible_bases": len(bases), "twin_room": room,
           "types": len({b["type"] for b in bases}), "card_free_bases": sum(1 for b in bases if b["card_free"]),
           "one_sided_bases": sum(1 for b in bases if b["one_sided"]), "two_line_bases": sum(1 for b in bases if not b["one_sided"] and not b["card_free"]),
           "cards_certified": None if cert is None else len(cert)}
    if not bases or target <= 0:
        return rep | {"twins": 0, "note": "no eligible base or no room under the block cap"}
    plan, prep = P.plan_block(bases, pats, pairs, block=cfg["block"], n_target=target, certified=cert or set(), seed=f"negtw-plan-{which}-v1",
                              trim=False)          # GB / MD: the T37b rule (re-plan at the realised size until the caps hold)
    out, base_of, dropped = [], {}, Counter()
    for b, p, t in plan:
        if rtw.twin_checks(b["core"], t, p, pairs):
            dropped["program check"] += 1
            continue
        src = cfg["source"] or b["row"]["source"]
        src = src if src.startswith("c2_") else "c2_" + src             # the merged MD block already carries c2_ sources
        r = rtw.c2_row(K.twin_row(b["row"], b["pre"], t, p, block=which), b["row"], p, source=src, family=cfg["family"])
        bm = b["row"].get("meta") or {}
        r["meta"]["domain"], r["meta"]["task_id"] = bm.get("domain") or b["row"].get("domain"), bm.get("task_id")
        if b["row"].get("domain"):
            r["domain"] = b["row"]["domain"]
        v = rtw.validate(r, b["row"])
        if v:
            dropped["schema: " + v[0][:40]] += 1
            continue
        out.append(r)
        base_of[r["id"]] = b["row"]
    gtw = K.g_tw([(base_of[r["id"]], r) for r in out])
    out.sort(key=lambda r: r["id"])
    rel = [{"a": r["meta"]["twin_of"], "b": r["id"], "type": r["role"]} for r in out]
    rep |= {"twins": len(out), "plan": prep, "dropped": dict(dropped), "g_tw": {k: gtw[k] for k in ("n_pairs", "violations", "pass")},
            "report": rtw.report_of(out, {p.pid: p for p in pats}) if out else {}, "block_rows_after": len(base_rows) + len(out),
            "caps_ok": len(out) <= cfg["twin_cap"] and len(base_rows) + len(out) <= cfg["cap"]}
    d = cfg["dir"]
    (d / "negtwins").mkdir(parents=True, exist_ok=True)
    (d / "negtwins" / "twins_c2.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out), encoding="utf-8")
    (d / "negtwins" / "twins_c2.relations.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rel), encoding="utf-8")
    (d / "negtwins" / "TWIN_REPORT.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    if apply and gtw["pass"]:
        apply_to_block(d, out, rel, rep)
    return rep


def apply_to_block(d: Path, twins: list, rel: list, rep: dict) -> None:
    cand, relf, man, qc = d / "out" / "candidates_c2.jsonl", d / "out" / "candidates_c2.relations.jsonl", d / "out" / "MANIFEST.json", d / "qc" / "QC_REPORT.json"
    rows = [r for r in read_jsonl(cand) if not (r.get("meta") or {}).get("negtwin")] + twins
    ids_old_twins = {r["id"] for r in read_jsonl(cand) if (r.get("meta") or {}).get("negtwin")}
    rels = [x for x in (read_jsonl(relf) if relf.exists() else []) if x["b"] not in ids_old_twins] + rel
    ct, rt = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), "".join(json.dumps(x) + "\n" for x in rels)
    cand.write_text(ct, encoding="utf-8")
    relf.write_text(rt, encoding="utf-8")
    files = {"candidates_c2.jsonl": {"sha256": C.sha(ct), "rows": len(rows)}, "candidates_c2.relations.jsonl": {"sha256": C.sha(rt), "rows": len(rels)}}
    for f in (man, qc):
        if f.exists():
            m = json.loads(f.read_text())
            m["files"] = {**(m.get("files") or {}), **files}
            if f == qc:
                m["negtwin_gates"] = {"tool": "negtwins.block_twins " + GEN, "twins": len(twins), "g_tw": rep["g_tw"], "caps_ok": rep["caps_ok"],
                                      "utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
            f.write_text(json.dumps(m, indent=1) + "\n", encoding="utf-8")


def main(argv=None) -> int:
    a = list(sys.argv[1:] if argv is None else argv)
    which = a[0]
    cfg = CFG[which]
    if "--rows" in a:
        i = a.index("--rows") + 1
        files = []
        while i < len(a) and not a[i].startswith("--"):
            files.append(Path(a[i]))
            i += 1
        rows = [r for f in files for r in read_jsonl(f)]
    elif which == "gb" and not (cfg["dir"] / "out" / "candidates_c2.jsonl").exists():
        rows = gb_rows(GB_DIR / "route_a42d" / "routed_block.jsonl")
    else:
        rows = read_jsonl(cfg["dir"] / "out" / "candidates_c2.jsonl")
    if len(a) > 1 and a[1] == "cardtasks":
        bases = eligible([r for r in rows if not (r.get("meta") or {}).get("negtwin")], which == "md")
        print(json.dumps({r: {k: m[k] for k in ("batch_id", "n_tasks", "n_items")} for r, m in card_tasks(bases, which).items()}))
        return 0
    tgt = int(a[a.index("--target") + 1]) if "--target" in a else None
    rep = build(which, rows, tgt, "--apply" in a)
    print(json.dumps({k: v for k, v in rep.items() if k != "report"}, indent=1)[:3000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
