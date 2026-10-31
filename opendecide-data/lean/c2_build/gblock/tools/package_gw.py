"""Package G-block wave 2 + W8 (A40, A40 addendum) as mix block GW: lean/data/c2_parts/GW/{out,qc}.

    python -B gblock/tools/package_gw.py            (from c2_build)

Reads gblock/wave2/final_kept_A40.jsonl (7,295 ids: W1-W7 after the A40 (c) cascade and the seeded 1,200 cap) and
final_kept_w8.jsonl (1,200 ids) and joins each id to its candidate text in wave2/candidates/{candidates,w8_candidates}.jsonl.
Writes the C2 layout c2io.fam_files expects:
    out/candidates_c2.jsonl            8,495 base rows, C2 row schema (c2_kit.rows), meta.family = "GW", meta.domain = the
                                       wave-2 type ("W1_injection" ...). The candidate's own meta is kept under meta.wave2.
    out/candidates_c2.relations.jsonl  empty (no twin relation among wave-2 rows)
    out/MANIFEST.json                  family, parents (upstream sources), shas and row counts
    qc/QC_REPORT.json                  gates run / pending (pass is false until G7, G8 AFLite, G13 and the crowd selection run)
No mixdev: A40 defines none for wave 2 (reported in the QC record). Gold is copied from the candidate as it is; nothing is
relabelled. call_id = the row's own id: wave-2 scenario groups hold up to 55 rows and G15 allows <= 3 rows per call_id (the
scenario stays in meta.wave2 / group_id).
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

CB = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(CB))
from c2_kit import rows as R  # noqa: E402

W2 = CB / "gblock" / "wave2"
GW = CB.parent / "data" / "c2_parts" / "GW"
SEED = 20261013
TYPES = {"W1": "W1_injection", "W2": "W2_pii", "W3": "W3_rag_faithfulness", "W4": "W4_off_topic", "W5": "W5_search_relevance",
         "W6": "W6_commit_type", "W7": "W7_tool_routing", "W8": "W8_complaint_routing"}
CAP_TYPE, CAP_TOTAL = 1200, 9200                 # A40 (d) and the A40 addendum


def sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def jl(p: Path) -> list:
    return [json.loads(l) for l in p.open(encoding="utf-8") if l.strip()]


def put(p: Path, rows: list) -> tuple:
    p.parent.mkdir(parents=True, exist_ok=True)
    t = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    p.write_text(t, encoding="utf-8")
    return sha(t), len(rows)


def row_of(c: dict) -> dict:
    om = c["meta"]
    t = om["type"]
    qt = c["qtype"]
    if qt == "noul":
        assert c["gold"] in (0, 1) and c["options"] is None, c["id"]
    else:
        assert c["gold"] in c["options"], c["id"]
    haiku = bool(om.get("haiku_task_id"))
    meta = {"family": "GW", "spec_id": "A40+A40-addendum", "card_id": f"gw_{t}_{sha(c['card'] or '')[:8]}", "domain_pack": None,
            "sampler": "GW", "gen_version": R.GEN_VERSION, "git_sha": "uncommitted", "seed": SEED,
            "structure_hash": sha(c["id"] + "|" + str(c["group_id"]))[:16], "difficulty_bin": None, "crowd_pg": None, "depth": 0,
            "deep": False, "format_style": "wave2/card", "wording_id": om.get("wording_id"), "defs_style": "same", "twin_of": None,
            "twin_kind": None, "text_source": "c2_wave2", "licence": om["licence"], "edge": [],
            "qform": "CARD_Q", "dev_only": False,
            "c2": {"author_mode": "F" if haiku else "T", "skin_id": None, "register": "real-text" if t in ("W2", "W3", "W5", "W6") else "authored",
                   "lexicon_ids": [], "haiku_task_id": om.get("haiku_task_id") if haiku else None,
                   "haiku_prompt_sha": om.get("haiku_task_sha256") if haiku else None, "twin_kind": None, "twin_of": None,
                   "closed_world": False},
            "domain": TYPES[t], "task_id": om.get("haiku_task_id"),
            "wave2": {k: v for k, v in om.items() if k not in ("licence",)}}
    return {"id": c["id"], "group_id": c["group_id"], "call_id": c["id"], "source": "c2_wave2", "state": c["state"], "qtype": qt,
            "instructions": c["instructions"], "options": c["options"] if qt != "noul" else None, "gold": c["gold"], "role": "base",
            "card": c["card"], "meta": meta, "domain": TYPES[t]}


def parents(rows: list) -> list:
    """Declared upstream sources: per type the distinct licence families (Socrata datasets are grouped)."""
    out = {}
    for r in rows:
        w = r["meta"]["wave2"]
        t = w["type"]
        lic = r["meta"]["licence"]
        key = lic.split(";")[0].strip()
        if "api/views/" in key:
            key = "Socrata per record (" + key.split("(licence:")[-1].strip(" )") + ")" if "(licence:" in key else "Socrata per record"
        if key.startswith("commit message from "):
            out[(t, key)] = {"domain": TYPES[t], "source": key.replace("commit message from ", "").split(" (")[0],
                             "source_licence": key.split("(")[-1].rstrip(")")}
        else:
            out[(t, key)] = {"domain": TYPES[t], "source_licence": key}
    return sorted(out.values(), key=lambda d: (d["domain"], d.get("source", ""), d["source_licence"]))


def main() -> None:
    kept = jl(W2 / "final_kept_A40.jsonl") + jl(W2 / "final_kept_w8.jsonl")
    ids = [k["id"] for k in kept]
    assert len(ids) == len(set(ids)) == 8495, len(ids)
    cands = {}
    for fn in ("candidates.jsonl", "w8_candidates.jsonl"):
        for c in jl(W2 / "candidates" / fn):
            cands[c["id"]] = c
    rows = sorted((row_of(cands[i]) for i in ids), key=lambda r: r["id"])
    per_type = Counter(r["meta"]["wave2"]["type"] for r in rows)
    assert max(per_type.values()) <= CAP_TYPE and len(rows) <= CAP_TOTAL, per_type
    bad = Counter()
    for r in rows:
        for p in R.validate_row(r, training=True):
            if p != "meta.licence":                      # real-text rows carry the upstream licence (as GB)
                bad[p[:70]] += 1
    cs, cn = put(GW / "out" / "candidates_c2.jsonl", rows)
    rs, rn = put(GW / "out" / "candidates_c2.relations.jsonl", [])
    fin = {p.name: sha_file(p) for p in (W2 / "final_kept_A40.jsonl", W2 / "final_kept_w8.jsonl", W2 / "candidates" / "candidates.jsonl",
                                          W2 / "candidates" / "w8_candidates.jsonl")}
    man = {"family": "GW", "parents": parents(rows), "parents_note": "wave-2 authored text (Haiku 5.5; no public benchmark item copied) "
           "+ real G-block texts (W2, W3, W5) + permissive-repo commit messages (W6); licences verified at fetch (wave2/ROUTE.md)",
           "generator": "gblock/tools/package_gw.py (A40 wave 2 + W8, 15 Oct 2026)",
           "stage": "packaged; G13 candidates, G7 / G8 shortcut screen and the crowd selection pending", "inputs": fin,
           "files": {"candidates_c2.jsonl": {"sha256": cs, "rows": cn}, "candidates_c2.relations.jsonl": {"sha256": rs, "rows": rn}},
           "mixdev": None, "mixdev_note": "A40 defines no wave-2 mixdev"}
    (GW / "out" / "MANIFEST.json").write_text(json.dumps(man, indent=1) + "\n", encoding="utf-8")
    fa = json.loads((W2 / "opus_finalize_A40.json").read_text())
    fw = json.loads((W2 / "opus_finalize_w8.json").read_text())
    g7f = GW / "qc" / "G7_GW.json"
    g7 = json.loads(g7f.read_text()) if g7f.exists() else None
    labels = {t: dict(Counter(str(r["gold"]) if r["qtype"] == "noul" else "choice" for r in rows if r["meta"]["wave2"]["type"] == t)) for t in TYPES}
    qc = {"pass": False, "stage": "packaged (A40 wave 2 + W8); not admitted until the pending gates below run", "family": "GW",
          "fix_iterations": 0, "passed_utc": None,
          "note": "pass is false on purpose: G7, G8 AFLite, G13 on the candidates and the crowd selection (select_GW.json) have not "
                  "run. The gates in 'gates_run' did run; none is waived. Set pass / passed_utc only from those records.",
          "gates_run": {
              "A40_c_cascade": {"haiku_kept_conf_ge_0.80_W1_W7": 9073, "opus_kept_conf_ge_0.85_W1_W7": 431, "w8_haiku_kept": 1574, "w8_opus_kept": 54,
                                "records": ["gblock/wave2/opus_finalize_A40.json", "gblock/wave2/opus_finalize_w8.json"],
                                "final_kept_sha256": {k: v for k, v in fin.items() if k.startswith("final_kept")}},
              "A40_c_5pct_audit": {"W1_W5_W7": "0% disagreement", "W6": "1/17 = 5.9% (< 6% rule)", "W8": "0/79"},
              "A40_d_caps": {"per_type": dict(per_type), "type_cap": CAP_TYPE, "total": cn, "total_cap": CAP_TOTAL},
              "schema": {"c2_kit.rows.validate_row (training=True; meta.licence excepted: real-text rows carry the upstream licence)": dict(bad) or "clean"},
              "gold_labels_per_type": labels,
              **({"G7_style_screen": {"record": "qc/G7_GW.json", "tool": "gblock/tools/gw_g7.py", "verdicts": g7["verdicts"],
                                      "note": "no official wave-2 G7 code existed; this is pilot.g7's helpers on wave-2 rows (model-visible features only). Fails are reported, not acted on: flagged items / templates are dropped and the type rebalanced by the orchestrator's ruling"}}
                 if g7 else {})},
          "gates_pending": ["G7 feature z-test on W1 W3 W4 W5 W7 W8 (+ report W2 W6): ran as gw_g7.py (see gates_run.G7_style_screen); fails on W1, W4, W5, W7 (and report W2, W6) are NOT yet acted on: drops + seeded rebalance pending",
                            "G8 AFLite < 10% predictable (c_src/common/g8_aflite.py has adapters for F1-F6 only; no wave-2 adapter exists)",
                            "G13 decontamination on the candidates (g13_c2.py over c2io.ALL_TARGETS, incl. OHS-4 sealed-side checkers): drops are whole units",
                            "C1 crowd selection for GW (c2_select.py select --fam GW; mix_c2 reads crowd_c2/select_GW.json, target 9,200, short is allowed)"],
          "files": {"candidates_c2.jsonl": {"sha256": cs}, "candidates_c2.relations.jsonl": {"sha256": rs}}}
    (GW / "qc").mkdir(parents=True, exist_ok=True)
    (GW / "qc" / "QC_REPORT.json").write_text(json.dumps(qc, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"rows": cn, "per_type": dict(per_type), "schema_problems": dict(bad), "parents": len(man["parents"])}, indent=1))


if __name__ == "__main__":
    main()
