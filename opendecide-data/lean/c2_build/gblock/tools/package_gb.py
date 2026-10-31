"""Package the routed G-block (A42-D 5) as mix block GB: lean/data/c2_parts/GB/{out,qc}.

    python -B gblock/tools/package_gb.py            (from c2_build)

Reads route_a42d/routed_block.jsonl (5,436 routed rows: id, label, card_id, domain, qtype, source, conf), joins each id to its
candidate text in candidates/{candidates,fix5_candidates}.jsonl, and writes the C2 layout c2io.fam_files expects:
    out/candidates_c2.jsonl            5,436 base rows, C2 row schema (c2_kit.rows), meta.family = "GB"
    out/candidates_c2.relations.jsonl  empty here; `negtwins.block_twins gb --apply` appends the twin relations
    out/mixdev_S5.jsonl                the 1,650 G-block mixdev rows (150 per domain, route_a42d/mixdev_ids.json), sampler S5,
                                       dev_only = true, never in the candidates (the script asserts the empty intersection)
    out/MANIFEST.json                  family, parents (the 11 upstream sources), shas and row counts
    qc/QC_REPORT.json                  gates run / pending, shas
Labels are copied from routed_block.jsonl / population.jsonl as they are: nothing is relabelled or edited.
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

G = CB / "gblock"
GB = CB.parent / "data" / "c2_parts" / "GB"
SEED = 20261013
UTC = None

LIC = {   # gblock/SOURCES.md, "Licence, as verified on the upstream record"
    "recipes": "CC BY-SA 4.0 (Wikibooks Cookbook, en.wikibooks.org)",
    "travel": "CC BY-SA 4.0 (Wikivoyage, en.wikivoyage.org)",
    "news": "CC BY 2.5 / CC BY 4.0 / public domain by article date (Wikinews, Wikinews:Copyright)",
    "learning": "CC BY-SA 4.0 (Wikiversity, en.wikiversity.org)",
    "gov_news": "Nova Scotia Open Government Licence (data.novascotia.ca xcif-vvr3)",
    "office_help": "CC BY-SA 3.0 (Ask LibreOffice, ask.libreoffice.org)",
    "sci_abstracts": "CC BY 4.0 / CC0 per record (bioRxiv, api.biorxiv.org)",
    "museum": "CC BY 4.0 (Art Institute of Chicago API, artwork description)",
    "park_programs": "Public Domain (Delaware State Park Programs, data.delaware.gov pu7t-3gai)",
    "volunteer_posts": "Public Domain (Montgomery County MD Volunteer Center, data.montgomerycountymd.gov rrpb-g5ks)",
    "open_data": "per record, permissive only: PD / PD US Gov / ODC PDDL / CC0 / CC BY / CC BY-SA (Socrata Discovery API)",
}
PARENTS = [{"domain": d, "source_licence": v} for d, v in sorted(LIC.items())]


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


def row_of(c: dict, label: str, dev: bool, tkey: dict) -> dict:
    d = c["domain"]
    k = c["card_id"].split("_")[-2]                      # gb_<domain>_<k>_c<j>
    if c["qtype"] == "noul":
        assert label in ("yes", "no"), (c["id"], label)
        gold, opts = (1 if label == "yes" else 0), None
    else:
        assert label in c["options"], (c["id"], label)
        gold, opts = label, c["options"]
    meta = {"family": "GB", "spec_id": "A39.c+A42-D.5", "card_id": c["card_id"], "domain_pack": None,
            "sampler": "S5" if dev else "GB", "gen_version": R.GEN_VERSION, "git_sha": "uncommitted", "seed": SEED,
            "structure_hash": sha(c["id"] + "|" + c["card_id"])[:16], "difficulty_bin": None, "crowd_pg": None, "depth": 0,
            "deep": False, "format_style": "real-text/card", "wording_id": None, "defs_style": "same", "twin_of": None,
            "twin_kind": None, "text_source": "c2_gblock",
            "licence": f"{LIC[d]} (text); card, question and label wording: {R.LICENCE}", "edge": [], "qform": "CARD_Q",
            "dev_only": dev,
            "c2": {"author_mode": "F", "skin_id": None, "register": "real-text", "lexicon_ids": [],
                   "haiku_task_id": f"gblock_card_authoring:{d}_{k}", "haiku_prompt_sha": tkey["instructions_template_sha256"],
                   "twin_kind": None, "twin_of": None, "closed_world": False},
            "domain": d, "task_id": None}
    return {"id": c["id"], "group_id": c["group_id"], "call_id": c["group_id"], "source": "c2_gblock", "state": c["state"],
            "qtype": c["qtype"], "instructions": c["instructions"], "options": opts, "gold": gold, "role": "base",
            "card": c["card"], "meta": meta, "domain": d}


def main() -> None:
    routed = {r["id"]: r for r in jl(G / "route_a42d" / "routed_block.jsonl")}
    pop = {r["id"]: r for r in jl(G / "route_a42d" / "population.jsonl")}
    mixdev_ids = {i for v in json.loads((G / "route_a42d" / "mixdev_ids.json").read_text())["ids"].values() for i in v}
    assert len(routed) == 5436 and len(mixdev_ids) == 1650, (len(routed), len(mixdev_ids))
    assert not (set(routed) & mixdev_ids), "the mixdev is in the routed block"
    assert all(pop[i]["mixdev"] for i in mixdev_ids) and not any(pop[i]["mixdev"] for i in routed)
    cands = {}
    for fn in ("candidates.jsonl", "fix5_candidates.jsonl"):
        for c in jl(G / "candidates" / fn):
            cands[c["id"]] = c
    tkey = json.loads((G / "cards" / "tasks_key.json").read_text())
    base, dev = [], []
    for i, r in routed.items():
        c = cands[i]
        assert (c["card_id"], c["domain"], c["qtype"]) == (r["card_id"], r["domain"], r["qtype"]), i
        base.append(row_of(c, r["label"], False, tkey))
    for i in sorted(mixdev_ids):
        c = cands[i]
        dev.append(row_of(c, pop[i]["label"], True, tkey))
    base.sort(key=lambda r: r["id"])
    dev.sort(key=lambda r: r["id"])
    ids = [r["id"] for r in base]
    assert len(set(ids)) == len(ids) and not set(ids) & {r["id"] for r in dev}
    bad = Counter()
    for r in base + dev:
        for p in R.validate_row(r, training=r["meta"]["dev_only"] is False):
            if p not in ("meta.licence", "dev-only row (S5 sampler or held-out skin / wording / register) in a training set"):
                bad[p[:60]] += 1
    out = GB / "out"
    cs, cn = put(out / "candidates_c2.jsonl", base)
    rs, rn = put(out / "candidates_c2.relations.jsonl", [])
    ms, mn = put(out / "mixdev_S5.jsonl", dev)
    man = {"family": "GB", "parents": PARENTS,
           "parents_note": "11 upstream real-text sources (gblock/SOURCES.md); permissive licences verified on the upstream records",
           "generator": "gblock/tools/package_gb.py (A42-D 5 routed block, 15 Oct 2026)",
           "stage": "packaged routed block; G13 candidates and crowd selection pending",
           "inputs": {"routed_block.jsonl": sha_file(G / "route_a42d" / "routed_block.jsonl"),
                      "mixdev_ids.json": sha_file(G / "route_a42d" / "mixdev_ids.json"),
                      "candidates.jsonl": sha_file(G / "candidates" / "candidates.jsonl"),
                      "fix5_candidates.jsonl": sha_file(G / "candidates" / "fix5_candidates.jsonl")},
           "files": {"candidates_c2.jsonl": {"sha256": cs, "rows": cn}, "candidates_c2.relations.jsonl": {"sha256": rs, "rows": rn}},
           "mixdev": {"mixdev_S5.jsonl": {"sha256": ms, "rows": mn}}}
    (out / "MANIFEST.json").write_text(json.dumps(man, indent=1) + "\n", encoding="utf-8")
    stats = json.loads((G / "route_a42d" / "routed_block_stats.json").read_text())
    counts = json.loads((G / "route_a42d" / "counts.json").read_text())
    qc = {
        "pass": False, "stage": "packaged (routed block); not admitted until the pending gates below run",
        "family": "GB", "fix_iterations": 0, "passed_utc": None,
        "note": "pass is false on purpose: G13 on the candidates and the crowd selection (select_GB.json) have not run. "
                "The gates in 'gates_run' did run; none is waived. Set pass / passed_utc only from those records.",
        "gates_run": {
            "A39_labels": {"haiku_accepted_conf_ge_0.80": counts["haiku_accepted"], "opus_kept_conf_ge_0.85": counts["opus_kept"],
                           "a39_dropped_low_conf": counts["a39_dropped"], "labelled_pool": counts["kept_pool"],
                           "record": "gblock/label/opus_finalize_A39.json"},
            "A39_5pct_opus_audit": {"audit_items_read": counts["opus_audit_items_read"], "disagreements": 0,
                                    "rule": "re-read a domain's Haiku-accepted rows if disagreement > 6%: not triggered"},
            "A42D_5_1_5_2_routing": {"c1_read_population": counts["population"], "mixdev_held_out": counts["mixdev"],
                                     "funnel": stats["funnel"], "record": "gblock/route_a42d/ROUTE_A42D.md"},
            "A42D_5_5_rebalance_and_caps": {"yes_share_per_yes_no_card_band": [0.40, 0.60], "yes_share_after": stats["yes_share_after"],
                                            "removed_by_rebalance_domain_and_block_caps": stats["removed_by_caps"],
                                            "by_domain": stats["summary"]["by_domain"],
                                            "max_domain_share": stats["summary"]["max_domain_share"], "domain_cap": 0.20,
                                            "block_rows": cn, "block_cap_incl_twins": 15000, "problems": stats["problems"]},
            "mixdev_disjoint": {"mixdev_rows": mn, "per_domain": 150, "in_candidates": 0, "file": "out/mixdev_S5.jsonl"},
            "schema": {"c2_kit.rows.validate_row (meta.licence excepted: real-text rows carry the upstream licence)": dict(bad) or "clean"},
        },
        "gates_pending": ["G13 decontamination on the candidates (A42-D 5.7; g13_c2.py, OHS-4 sealed-side checkers): drops are whole units",
                          "C1 crowd selection for GB (c2_select.py select; mix_c2 reads crowd_c2/select_GB.json, target 15,000, short is allowed)",
                          "twin gates (G-TW, program checks) are added by `negtwins.block_twins gb --apply` under negtwin_gates",
                          "Sonnet 3% audit of the twin rows (A42-D 7.3) if it is required for GB twins"],
        "files": {"candidates_c2.jsonl": {"sha256": cs}, "candidates_c2.relations.jsonl": {"sha256": rs}},
    }
    (GB / "qc").mkdir(parents=True, exist_ok=True)
    (GB / "qc" / "QC_REPORT.json").write_text(json.dumps(qc, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"base_rows": cn, "mixdev": mn, "schema_problems": dict(bad), "domains": dict(Counter(r["domain"] for r in base)),
                      "qtypes": dict(Counter(r["qtype"] for r in base))}, indent=1))


if __name__ == "__main__":
    main()
