#!/usr/bin/env python3
"""public-3 manifest: counts, licences, parents, deny-list verdicts, sealed-check results, filter counts and sha256 of
every output. Also writes
  out/public3_g5_sample_ids.json       G5 blind read: 100 rows per dataset, stratified by framing and gold
  out/public3_record_claims.jsonl      record-claim handoff (ids and text hashes only) for the orchestrator's ledger:
                                       one "public3_direct" row per record a public-3 row uses, plus (v1.1, fix 4)
                                       one "public3_text_alias" row per other record id (public-3 or formats-2
                                       records) whose loose text equals a direct claim's (MAMS ACSA vs ATSA copies of
                                       one sentence, XED annotated vs neutral lines, EDOS re-posts)
  out/public3_class_allocation.json    per-class row counts of the direct 3E rows (F10 AR24 headroom basis; 3.1 caps)
Never prints row text."""
from __future__ import annotations

import datetime
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[2]
sys.path.insert(0, str(HERE / "lib"))
from common3 import (GEN_VERSION, LOGS, LONG_TOKENS, OUT, REC, SEED, TMP, row_tokens, safe_in, stable_shuffle,  # noqa: E402
                     write_jsonl)

F2_REC = LEAN / "c_src" / "formats" / "formats-2" / "records"
TOKENIZER_SOURCE = ("Qwen/Qwen3.5-4B tokenizer.json (Hugging Face snapshot 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a; "
                    "the same sha256 as the local HF cache copy); used for row_tokens = tokens(state, instructions, card, "
                    "options) + 160 overhead, and for the G15 real-tokenizer length of the rendered prompt")


def fsha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


DS_INFO = {
    "c_pub_xed": {"spec_row": "3.2 #13", "dataset": "XED English", "block": "3E", "target_r1": 600,
                  "licence": "CC BY 4.0", "share_alike": False, "record_keys": ["xed_readme"],
                  "downloads": ["xed_annotated", "xed_neutral"],
                  "official_record": "https://github.com/Helsinki-NLP/XED (README last line; no LICENSE file)",
                  "upstream_commit": "Helsinki-NLP/XED@76666d251f147cf518071bef4f8415dab6b96115",
                  "parents": ["OPUS OpenSubtitles"],
                  "text_licence": "OpenSubtitles lines via OPUS: no text licence found (OPUS page 404); third-party text under a clean dataset licence (register 6, not a blocker)",
                  "split_rule": "no official split: own 90/10 by line via the shared 3E split (keyed on loose text); never the fi or projected files",
                  "schemes": ["xed"]},
    "c_pub_mams": {"spec_row": "3.2 #14", "dataset": "MAMS (ACSA + ATSA)", "block": "3E", "target_r1": 750,
                   "licence": "Apache-2.0", "share_alike": False, "record_keys": ["mams_license", "mams_readme"],
                   "downloads": ["mams_acsa", "mams_atsa"],
                   "official_record": "https://github.com/siat-nlp/MAMS-for-ABSA/blob/master/LICENSE (repo covers data/)",
                   "upstream_commit": "siat-nlp/MAMS-for-ABSA@cddcdb0f423b3fdb2c76b70744737abed3a00d17",
                   "parents": ["Citysearch New York restaurant reviews (Ganu et al. 2009)"],
                   "text_licence": "Citysearch restaurant reviews: third-party text (register 6). May share a review pool with DI's ACOS: counts-only dedupe by the orchestrator",
                   "split_rule": "train.xml only (val, test never downloaded); our own 10% of train for mix-tuning dev",
                   "schemes": ["mams_acsa", "mams_atsa"]},
    "c_pub_sarcasm": {"spec_row": "3.2 #15", "dataset": "News Headlines Sarcasm v2", "block": "3E", "target_r1": 350,
                      "licence": "CC BY 4.0", "share_alike": False, "record_keys": ["sarcasm_kaggle_view"],
                      "downloads": ["sarcasm_v2"],
                      "official_record": "https://www.kaggle.com/datasets/rmisra/news-headlines-dataset-for-sarcasm-detection (creator's Kaggle page, structured licence field; decision 6 default)",
                      "upstream_commit": "Kaggle dataset 30764, version 2 (3 Jul 2019); file Sarcasm_Headlines_Dataset_v2.json",
                      "parents": ["The Onion headlines", "HuffPost headlines"],
                      "text_licence": "The Onion and HuffPost headlines: third-party text (register 6); outlet names redacted, article links never used",
                      "split_rule": "no official split: own 90/10 by record via the shared 3E split",
                      "schemes": ["sarcasm_v2"],
                      "owner_override_note": "if the owner reads decision 6 as covering Kaggle pages, Sarcasm v2 goes out and its 350 r1 rows go to XED +175 and GHC +175 (not applied: default stands)"},
    "c_pub_edos": {"spec_row": "3.2 #17", "dataset": "EDOS", "block": "3E", "target_r1": 350,
                   "licence": "CC0 1.0", "share_alike": False, "record_keys": ["edos_license", "edos_readme"],
                   "downloads": ["edos_labelled"],
                   "official_record": "https://github.com/rewire-online/edos/blob/main/LICENSE",
                   "upstream_commit": "rewire-online/edos@b1f1fbcca9d42de0395432ada8fcfb5c35f68c77",
                   "parents": ["Gab posts (pushshift dump)", "Reddit posts"],
                   "text_licence": "Gab and Reddit posts: third-party text; CC0 covers Rewire's rights only (register 6)",
                   "split_rule": "edos_labelled_aggregated.csv split == train only (dev and test rows dropped at parse); our own 10% of train for mix-tuning dev; the per-annotator file is not read (register row 17 does not list it)",
                   "schemes": ["edos"]},
}



# v2.0 (repair r1): datasets dropped by a spec 8 dataset-level rule (kept for the record; no rows)
DROPPED_DS = {
    "c_pub_ghc": {"spec_row": "3.2 #16", "dataset": "Gab Hate Corpus", "block": "3E", "target_r1": 350,
                  "licence": "CC BY 4.0", "share_alike": False, "record_keys": ["ghc_osf_node", "ghc_osf_data_folder"],
                  "downloads": ["ghc_train"],
                  "official_record": "https://osf.io/edua3/ (node licence via the OSF API)",
                  "upstream_commit": "OSF node edua3 (modified 2022-04-12); Data/ghc_train.tsv (modified 2021-03-03, OSF sha256 c82a2733...)",
                  "parents": ["Gab posts (gab.ai)"],
                  "text_licence": "gab.ai posts: third-party text (register 6); URLs and @handles replaced by [URL] / [USER]",
                  "split_rule": "ghc_train.tsv only (ghc_test.tsv never downloaded); our own 10% of train for mix-tuning dev",
                  "schemes": ["ghc"],
                  "dropped": "spec 8 G5 (public rows, dataset-level): the independent G5 read of 6 Oct found 10/100 clearly wrong golds (> 8%); every flagged gold equals the released ghc_train.tsv majority label (dataset label noise); ghc_train.tsv has no vote shares, so no program-level record selection can separate them",
                  "rows_go_to": "F11 (spec 3.2: a 3E set with no named fallback sends its rows to F11), 350 r1 rows, logged in the mixer report"},
}

def code_files():
    """sha256 of every builder file (scripts, lib, shell); the aggregate equals assemble.code_sha() (the *.py set),
    whose 16-hex prefix is in every row's meta.git_sha."""
    files = sorted(list(HERE.glob("*.py")) + list((HERE / "lib").glob("*.py")))
    agg = hashlib.sha256()
    for f in files:
        agg.update(f.name.encode())
        agg.update(f.read_bytes())
    per = {str(f.relative_to(HERE)): fsha(f) for f in files + sorted(HERE.glob("*.sh"))}
    return {"aggregate_sha256": agg.hexdigest(), "aggregate_rule": "sha256 over sorted *.py + lib/*.py of (file name, "
            "bytes); = assemble.code_sha(), prefix in meta.git_sha", "files": per,
            "gen_version": GEN_VERSION}


def text_aliases(direct_uids, recmeta):
    """For each directly claimed record: every other record id (public-3 records, all six schemes; formats-2 records,
    five schemes) whose loose_sha256 equals the claim's loose_sha256 under public-3's text or formats-2's text of the
    same id (GHC texts differ by public-3's [URL] / [USER] placeholders). Ids and hashes only."""
    p3_by = defaultdict(set)
    for rid, m in recmeta.items():
        p3_by[m["loose_sha256"]].add(rid)
    f2_loose, f2_by, f2_elig = {}, defaultdict(set), {}
    for s in ("xed", "mams_acsa", "mams_atsa", "ghc", "edos"):
        with open(safe_in(F2_REC / f"{s}.jsonl"), encoding="utf-8") as f:
            for line in f:
                o = json.loads(line)
                f2_loose[o["id"]] = o["loose_sha256"]
                f2_by[o["loose_sha256"]].add(o["id"])
                e = o.get("eligible") or {}
                pre = e.get("eligible_pre_x15") if isinstance(e.get("eligible_pre_x15"), dict) else {}
                # F10 / F11 eligible now, or eligible once formats-2's EDOS X15 block lifts (eligible_pre_x15)
                f2_elig[o["id"]] = bool(e.get("F10_S7") or e.get("F11_S7") or pre.get("F10_S7") or pre.get("F11_S7"))
    out = {}
    for x in direct_uids:
        hs = {recmeta[x]["loose_sha256"]}
        if x in f2_loose:
            hs.add(f2_loose[x])
        al = set()
        for h in hs:
            al |= p3_by.get(h, set()) | f2_by.get(h, set())
        al.discard(x)
        out[x] = sorted(al)
    return out, f2_elig


def primary_class(r):
    m, src = r["meta"], r["source"]
    h = m["human_label"]
    if src == "c_pub_xed":
        return "|".join(h["emotions"])
    if src == "c_pub_mams":
        if r["qtype"] == "noul":
            return f"{m['asked_polarity']}:{'match' if m['predicate_holds'] else 'other'}"
        if "asked_polarity" in m:
            return f"which:{m['asked_polarity']}"
        g = {"favorable": "positive", "unfavorable": "negative", "no opinion expressed": "neutral"}.get(r["gold"], r["gold"])
        return g
    if src == "c_pub_sarcasm":
        if r["qtype"] == "noul":
            return f"sarcastic={h['is_sarcastic']}"
        return "pair:" + ("one_sincere" if m["inverted"] else "one_sarcastic")
    if src == "c_pub_ghc":
        return "hate" if (h["hd"] or h["cv"]) else ("vo_only" if h["vo"] else "none")
    if src == "c_pub_edos":
        return h["label_category"]
    return "?"


def main():
    fm = json.loads((LOGS / "fetch_manifest.json").read_text())
    files = json.loads((LOGS / "final_files.json").read_text())
    fstats = json.loads((LOGS / "final_stats.json").read_text())
    rs_all = {n: [json.loads(l) for l in open(OUT / n)] for n in ("public3_rows_r1.jsonl", "public3_reserve.jsonl",
                                                                   "public3_mtdev.jsonl")}
    main_rows = rs_all["public3_rows_r1.jsonl"]
    recstats = json.loads((LOGS / "records_stats.json").read_text())
    selfc = json.loads((LOGS / "selfcheck_final_main.json").read_text())
    per = {}
    for src, info in DS_INFO.items():
        rs = [r for r in main_rows if r["source"] == src]
        fr = Counter(r["id"].split("-")[2] for r in rs)
        yn = [r for r in rs if r["qtype"] == "noul"]
        ch = [r for r in rs if r["qtype"] == "choice"]
        toks = [row_tokens(r) for r in rs]
        per[src] = {
            **{k: v for k, v in info.items() if k not in ("record_keys", "downloads", "schemes")},
            "licence_record_reread": {k: {"url": fm["licence_records"][k]["url"], "utc": fm["licence_records"][k]["read_utc"],
                                          "sha256": fm["licence_records"][k]["sha256"],
                                          "checks_pass": fm["licence_records"][k]["pass"],
                                          "saved": f"licence_records/{k}"} for k in info["record_keys"]},
            "download": {k: {"url": fm["downloads"][k]["url"].split("?")[0], "sha256": fm["downloads"][k]["archive_sha256"],
                             "bytes": fm["downloads"][k]["archive_bytes"],
                             "files": {f: v["sha256"] for f, v in fm["downloads"][k]["files"].items()}}
                         for k in info["downloads"]},
            "records_filter_counts": {s: {k: v for k, v in recstats["schemes"][s].items() if k != "sha256"}
                                      for s in info["schemes"]},
            "rows_r1": len(rs),
            "rows_reserve": sum(r["source"] == src for r in rs_all["public3_reserve.jsonl"]),
            "rows_mtdev": sum(r["source"] == src for r in rs_all["public3_mtdev.jsonl"]),
            "framings": dict(fr),
            "yes_no_rows": len(yn), "yes_rate": round(sum(r["gold"] for r in yn) / len(yn), 4) if yn else None,
            "neg_wording_rows": sum(r["role"] == "neg" for r in yn),
            "twin_rows": sum(1 for r in rs if r["meta"].get("twin_of")),
            "choice_rows": len(ch), "option_counts": dict(Counter(len(r["options"]) for r in ch)),
            "cards": len({r["meta"]["card_id"] for r in rs}),
            "wordings": len({r["meta"]["wording_id"] for r in rs}),
            "defs_styles": dict(Counter(r["meta"]["defs_style"] for r in rs)),
            "defs_styles_by_qtype": {q: dict(Counter(r["meta"]["defs_style"] for r in rs if r["qtype"] == q))
                                     for q in ("noul", "choice")},
            "card_render": dict(Counter(r["meta"]["card_render"] for r in rs)),
            "rows_with_card": sum(1 for r in rs if r["card"]),
            "format_styles": len({r["meta"]["format_style"] for r in rs}),
            "groups": len({r["group_id"] for r in rs}),
            "tokens_total": sum(toks), "tokens_median": sorted(toks)[len(toks) // 2] if toks else 0,
            "tokens_max": max(toks) if toks else 0, "rows_ge_2000_tokens": sum(t >= LONG_TOKENS for t in toks),
            "soft_targets_human_votes": sum(1 for r in rs if r["meta"].get("teacher_src") == "human_votes"),
            "classes_main": dict(Counter(primary_class(r) for r in rs)),
        }
    # class allocation (F10 AR24 headroom; 3.1 caps: <= 3,000 rows per dataset in r2, <= 500 per class)
    alloc = {}
    for src in DS_INFO:
        a = {}
        for n, rs in rs_all.items():
            a[n] = dict(Counter(primary_class(r) for r in rs if r["source"] == src))
        a["records_claimed"] = len({x for rs in rs_all.values() for r in rs if r["source"] == src
                                    for x in (r["meta"]["record_uid"] if isinstance(r["meta"]["record_uid"], list)
                                              else [r["meta"]["record_uid"]])})
        a["r1_rows_main"] = sum(r["source"] == src for r in main_rows)
        a["r2_plan_rows_direct"] = 2 * a["r1_rows_main"]
        a["max_class_rows_r1_main"] = max(a["public3_rows_r1.jsonl"].values())
        alloc[src] = a
    alloc_doc = {"id": "public3_class_allocation", "note": "Direct 3E rows only (codebook rows of F10/F11 S7, F5 and the S5 arm count toward the same "
                         "per-dataset 3,000-row and per-class 500-row caps; the mixer sums them). Classes: XED = the "
                         "line's emotion set; MAMS = asked polarity x match (yn), gold polarity (choice), which:<pol>; "
                         "Sarcasm = label (yn) or pair kind (choice); GHC = hate (hd or cv) / vo_only / none; "
                         "EDOS = label_category.",
                 "allocation": alloc}
    (OUT / "public3_class_allocation.json").write_text(json.dumps(alloc_doc, indent=1))
    # record claims (ids and hashes only)
    recmeta = {}
    for s in ("xed", "mams_acsa", "mams_atsa", "ghc", "edos", "sarcasm_v2"):
        with open(REC / f"{s}.jsonl", encoding="utf-8") as f:
            for line in f:
                o = json.loads(line)
                recmeta[o["id"]] = {"dataset": o["dataset"], "scheme": o["scheme"], "record_id": o["record_id"],
                                    "file": o["file"], "norm_sha256": o["norm_sha256"],
                                    "loose_sha256": o["loose_sha256"], "part": o["part"]}
    claims = {}
    seg_of = {"public3_rows_r1.jsonl": "train_r1", "public3_reserve.jsonl": "train_r1_reserve",
              "public3_mtdev.jsonl": "mix_tuning_dev"}
    for n, rs in rs_all.items():
        for r in rs:
            for x in (r["meta"]["record_uid"] if isinstance(r["meta"]["record_uid"], list) else [r["meta"]["record_uid"]]):
                c = claims.setdefault(x, {"id": "claim.pub3." + x, "record_uid": x, **recmeta[x], "claim_kind": "public3_direct",
                                          "segment": seg_of[n], "group_id": r["group_id"], "row_ids": []})
                assert c["group_id"] == r["group_id"]
                c["row_ids"].append(r["id"])
    direct = sorted(claims.values(), key=lambda c: c["record_uid"])
    assert len({c["loose_sha256"] for c in direct}) == len(direct)
    aliases, f2_elig = text_aliases([c["record_uid"] for c in direct], recmeta)
    alias_rows, alias_seen, alias_stats = [], {}, Counter()
    for c in direct:
        al = [a for a in aliases[c["record_uid"]] if a not in claims]
        alias_stats["alias_is_direct_claim_skipped"] += len(aliases[c["record_uid"]]) - len(al)
        c["claim_kind"] = "public3_direct"
        c["text_alias_uids"] = al
        for a in al:
            assert a in recmeta, a                       # formats-2 ids are public-3 ids (same id scheme)
            assert a not in alias_seen, (a, "alias of two claims")
            alias_seen[a] = c["record_uid"]
            m = recmeta[a]
            alias_rows.append({"id": "claim.pub3." + a, "record_uid": a, **m, "claim_kind": "public3_text_alias",
                               "alias_of": c["record_uid"], "segment": c["segment"], "group_id": c["group_id"],
                               "row_ids": []})
            alias_stats[f"alias_{m['scheme']}"] += 1
            alias_stats[f"alias_formats2_eligible_{m['scheme']}"] += f2_elig.get(a, False)
    claim_rows = sorted(direct + alias_rows, key=lambda c: c["record_uid"])
    assert len({c["record_uid"] for c in claim_rows}) == len(claim_rows)
    write_jsonl(OUT / "public3_record_claims.jsonl", claim_rows)
    # G5 sample ids
    g5 = {}
    for src in DS_INFO:
        rs = [r for r in main_rows if r["source"] == src]
        strata = defaultdict(list)
        for r in stable_shuffle(rs, "g5", src):
            strata[(r["id"].split("-")[2], str(r["gold"]) if r["qtype"] == "noul" else primary_class(r))].append(r["id"])
        pick, i = [], 0
        keys = sorted(strata)
        while len(pick) < min(100, len(rs)):
            k = keys[i % len(keys)]
            if strata[k]:
                pick.append(strata[k].pop())
            i += 1
        g5[src] = {"n": len(pick), "bar": "drop the dataset if > 8% clearly wrong (dataset-level decision only)",
                   "ids": pick}
    (OUT / "public3_g5_sample_ids.json").write_text(json.dumps({"id": "public3_g5_sample_ids", "datasets": g5}, indent=1))
    den = json.loads((HERE / "denylist/verdicts_public3.json").read_text())
    sealed = {}
    for p in ("templates", "dev", "reserve", "main"):
        s = json.loads((TMP / f"stage_{p}.sealedqc.summary.json").read_text())
        h = [json.loads(l) for l in open(TMP / f"stage_{p}.sealedqc.jsonl")]
        sealed[p] = {"rows": len(h), "hit_rows": sum(bool(o["hit"]) for o in h),
                     "hit_kinds": dict(Counter(k["kind"] for o in h for k in o["hit_kinds"])),
                     "report_only_rows": sum(1 for o in h if o.get("report_kinds")),
                     "report_kinds": dict(Counter(k["kind"] for o in h for k in o.get("report_kinds", []))),
                     "checker_sha256": s.get("checker_sha256"), "suite_sha256": s.get("suite_sha256"),
                     "input_sha256": s.get("input_sha256")}
    sealed_final = {}
    for f in sorted((LOGS / "sealed_final").glob("*.summary.json")):
        base = f.name[:-len(".summary.json")]
        s = json.loads(f.read_text())
        h = [json.loads(l) for l in open(LOGS / "sealed_final" / f"{base}.sealedqc.jsonl")]
        sealed_final[base + ".jsonl"] = {"rows": len(h), "hit_rows": sum(bool(o["hit"]) for o in h),
                                         "report_only_rows": sum(1 for o in h if o.get("report_kinds")),
                                         "report_kinds": dict(Counter(k["kind"] for o in h for k in o.get("report_kinds", []))),
                                         "checker_sha256": s.get("checker_sha256"), "suite_sha256": s.get("suite_sha256"),
                                         "input_sha256": s.get("input_sha256")}
    outputs = {}
    for p in sorted(OUT.glob("*")):
        outputs[p.name] = {"sha256": fsha(p), "bytes": p.stat().st_size,
                           "rows": sum(1 for _ in open(p)) if p.suffix == ".jsonl" else None}
    man = {
        "id": "manifest_public3",
        "builder": "public-3 (C_DATA_SPEC v4 3.2 #13-17, block 3E)",
        "created_utc": datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "plan": {"PREREG_FINAL": "A15 suite sha f4ae863720535b6ba27acad51917fe07b4d31344228a1dddb9d98bc3a4deac68; A16 C plan",
                 "C_DATA_SPEC.md": fsha(LEAN / "c_spec/C_DATA_SPEC.md"),
                 "C_TRAIN_RECIPE.md": fsha(LEAN / "c_spec/C_TRAIN_RECIPE.md"),
                 "LICENCE_REGISTER.md": fsha(LEAN / "c_spec/LICENCE_REGISTER.md")},
        "seed": SEED,
        "gen_version": GEN_VERSION,
        "changes_v2_0": [
            "repair r1 (PREREG A29 a), G6 root causes fixed at the builder: MAMS yes/no asked two aspects of one sentence with one polarity, so the asked aspect x polarity carried the gold (aspect-polarity priors); MAMS choice asked one aspect whose prior the question named; EDOS / Sarcasm yes/no drew the card (defs style) and format per record, so card x gold was balanced only on average",
            "fix: matched sets. MAMS acsayn / atsayn = quads (2 sentences x 2 aspects; each aspect question yes on one sentence and no on the other), acsach / atsach = triplets (one aspect, gold positive / negative / neutral); EDOS yn and Sarcasm yn = (positive, negative) state-flip pairs; EDOS ch5 / ch4 = one post per class. A set shares wording, card, guidance, defs style, format style and option order (each position gold once), and its states share one G6 length bucket. Every row keeps its own call_id; meta.match_set names the set and twin_of chains it (a sealed drop removes and refills the whole set)",
            "MAMS atsawh dropped (its options are the sentence's own terms: no matched set possible); its rows moved to acsach / atsach",
            "GHC dropped by the spec 8 G5 dataset-level rule (10/100 clearly wrong > 8%); its 350 r1 rows go to F11 per spec 3.2 (DROPPED_DS)",
            "Sarcasm ch root cause: 'longest headline is gold' and the gold position were balanced only over the whole framing, so wording (direct / inverted) and metadata x length-rank / position cells were not (metadata x option-kind view 2.6 pp over chance on the first v2.0 draft); fix: matched sets of k rows (one wording, defs style, format style) in which each length rank (characters, no ties) and each position is gold exactly once",
            "Sarcasm ch: a headline matching the G10 abstain pattern (can't, unknown, not sure, ...) is never a choice option (it may still be a yes/no state)",
            "XED: code unchanged (rows identical to v1.1)",
            "labels: still the released human annotations mapped by program; no row edited, relabelled or picked by hand"],
        "dropped_datasets": DROPPED_DS,
        "changes_v1_1": [
            "fix 1: Sarcasm choice state of style sar_s3 is a literal (never formatted): single braces, so the JSON state parses (47 rows: 34 main, 10 reserve, 3 mtdev); assemble.validate parses every JSON-style state",
            "fix 2: choice-row cards hold only '- {option}: {definition}' lines (the only card lines decoder_io shows on a choice row in cygnet / schema_branch_mark); every other choice guidance (headers, rubric steps, task notes; Sarcasm ch, MAMS ATSA-which, GHC / XED / EDOS / MAMS rubric) moved into instructions before the question wording; Sarcasm ch and ATSA-which rows have card null (their options carry no definitions); meta.card_render records where card text shows; make_row and assemble refuse a hidden choice-card line; G15 loader_check (formats-1 fmt1.card) passes on every row",
            "fix 3: the GHC choice options and option-definition cards live in lib/pools.py (GHC_CH_OPTIONS, GHC_CH_CARDS, GHC_CH_GUIDES); the stale 4-option export is gone; public3_templates.jsonl re-exported and sealed-checked",
            "fix 4: record claims add one public3_text_alias row per other record id (public-3 or formats-2 records) whose loose text equals a direct claim's (MAMS ACSA vs ATSA copies, XED, EDOS, Sarcasm copies); consumer rule: skip every record_uid in the file and every record whose loose / norm sha256 equals a claim's",
            "fix 5: sealed_drop flag (public-3's own id-only records check + formats-2's record drops) on tmp/records and on every row of the shared split file; the 6 GHC ids are never eligible; build_rows removes them after its shuffle, so v1.0's draw is kept",
            "fix 6: manifest lists the builder code sha256 (aggregate = the meta.git_sha prefix, and per file) and the tokenizer sha256 and source",
            "unchanged from v1.0: row ids, groups, call ids, options and their order, gold, roles, counts, G5 sample ids, class allocation, direct claims; labels untouched"],
        "code": code_files(),
        "tokenizer": {"file": "tmp/tokenizer.json", "sha256": fsha(TMP / "tokenizer.json"),
                      "bytes": (TMP / "tokenizer.json").stat().st_size, "source": TOKENIZER_SOURCE},
        "row_format": "C_DATA_SPEC 2.4 top-level keys exactly (id, group_id, call_id, source, state, qtype, instructions, options, gold, role, card, meta); qtype noul (gold 1 = yes; role aff / neg) or choice (gold = option string; role choice). Every row has its own call_id (question-flip contrast twins, no relation units); twins share group_id and point at each other in meta.twin_of. No meta.teacher (no human vote shares in the allowed files: GHC ghc_train.tsv and EDOS aggregated file carry majority labels only; XED, MAMS and Sarcasm carry single labels). No meta.option_level (no public ordinal rows in round 1)",
        "outputs": outputs,
        "counts": {"rows_r1": len(main_rows), "target_r1_this_builder": 2400,
                   "reserve": len(rs_all["public3_reserve.jsonl"]), "mix_tuning_dev": len(rs_all["public3_mtdev.jsonl"]),
                   "records_claimed": len(direct), "claim_rows": len(claim_rows),
                   "text_alias_claim_rows": len(alias_rows)},
        "datasets": per,
        "selfcheck_g10_main": "logs/selfcheck_final_main.json",
        "selfcheck_summary": {k: {a: b for a, b in v.items() if a in ("rows", "yes_rate", "max_wording_yes_dev_pp",
                                                                         "gold_max_share", "wording_x_gold_chi2_p",
                                                                         "longest_is_gold_rate", "mean_inv_k")}
                              for k, v in selfc.items() if not k.startswith("_")},
        "shared_split_3e": {"file": "out/public3_split_3e.jsonl", "rule": recstats["split_rule"],
                            "covers": "every record of XED English (annotated + neutral files), MAMS ACSA, MAMS ATSA, GHC train, EDOS train, Sarcasm v2; ids equal formats-2 records ids (cross-check in logs/records_stats.json)",
                            "formats2_crosscheck": recstats["formats2_crosscheck"],
                            "handoff": "F10 R2-23 / F11 'orchestrator-owned XED split file' / spec 10 public mtdev: dev-part records feed only the mix-tuning dev. Every record with sealed_drop true (sealed-suite hit in public-3's or formats-2's id-only records check) is out for every consumer",
                            "sealed_drop": recstats.get("sealed_drop")},
        "record_claims": {"file": "out/public3_record_claims.jsonl",
                          "rule": "one record per group, one loose text per record across all public-3 rows; reserve records stay claimed until the orchestrator releases them at freeze. claim_kind public3_direct = a record a public-3 row uses; public3_text_alias = another record id (public-3 or formats-2 records) with the same loose text as a direct claim (alias_of), claimed with it",
                          "consumer_rule": "skip every record_uid in this file (direct and text-alias rows), and any other record whose loose_sha256 or norm_sha256 equals a claim row's",
                          "alias_stats": dict(alias_stats),
                          "ledger": "the orchestrator's record-claim ledger did not exist at build time; this file is public-3's claim set for it"},
        "class_allocation": "out/public3_class_allocation.json",
        "denylist": {"program": "c_src/common/denylist.py", "program_sha256": den["program_sha256"],
                     "version": den["version"], "aliases_sha256": den["aliases_sha256"],
                     "denylist_sha256": den["denylist_sha256"], "query": "denylist/query_public3.json",
                     "query_sha256": den["query_sha256"], "verdicts": "denylist/verdicts_public3.json",
                     "verdicts_sha256": fsha(HERE / "denylist/verdicts_public3.json"), "counts": den["counts"],
                     "verdicts_by_dataset": {k: {"verdict": v["verdict"],
                                                 "parent_no_new_rows_pass": v.get("parent_no_new_rows_pass")}
                                             for k, v in den["verdicts"].items()},
                     "input_paths_check": "denylist.py paths on every input path (raw files, golden_train, formats-2 records, tokenizer): all ok (logs/denylist_paths.stdout)",
                     "dedupe_only_inputs": "HateXplain dataset.json (hate-alert/HateXplain@01d742279dac) and SBIC.v2.tgz: hashed in-process for the spec 3.2 #16-17 / 7.1 exact-text dedupe of GHC and EDOS; never rows, never written; deleted with raw/"},
        "sealed_check": {"checker": "lean/sealed_nd/qc/sealed_check.py (run as a program; exports never read)",
                         "staged_files": sealed, "assembly": fstats, "final_files_recheck": sealed_final,
                         "rule": "every blocking hit dropped (twin partner too) and main refilled from the same dataset x framing x unit-size x label-signature reserve; report-only kinds are not hits"},
        "golden_train_dedupe": "spec 3.1 unused records: loose full text equal to a golden_train state or line (all 204 sources), or > 50% of its word 8-grams (>= 8 words) / its whole word sequence (3-7 words) inside a golden_train row of the 3E-adjacent sources (br_xed_en, br_mams_acsa, br_sarcasm_headlines, gd_csc_sarcasm, br_ghc, gd_ghc_hate, br_edos, gd_edos_sexism, binj_offensive, std_hate, toxic_conv, br_convabuse, br_hatemoji_build, gd_hatemoji_build_v14, br_emobank) -> not used; counts per scheme in datasets.*.records_filter_counts",
        "not_done_here": ["counts-only 12-gram / 7.2 decontamination vs OHS-1/2/3, sealed exports, DI tests (incl. ACOS for MAMS), JevBench: orchestrator",
                          "G9 crowd scoring (difficulty_bin, crowd_pg are null): free L4",
                          "G5 blind read: out/public3_g5_sample_ids.json lists the samples (100 per dataset)",
                          "G6/G7/G8/G12/G15 QC agent (selfcheck covers the G10 balance only); meta.option_level: none (no public ordinal rows in round 1)",
                          "F10/F11 2.3 codebook rows on the same datasets: not built here; they must skip every record_uid in out/public3_record_claims.jsonl (direct and public3_text_alias rows) and every record whose loose_sha256 / norm_sha256 equals a claim's, skip every sealed_drop record, and use out/public3_split_3e.jsonl"],
        "notices_file_entries": ["XED (Ohman et al. 2020; Helsinki-NLP; CC BY 4.0; OpenSubtitles lines via OPUS)",
                                 "MAMS (Jiang et al. 2019; siat-nlp; Apache-2.0; Citysearch restaurant reviews)",
                                 "News Headlines Dataset for Sarcasm Detection v2 (Rishabh Misra; CC BY 4.0; The Onion and HuffPost headlines)",
                                 "Gab Hate Corpus (Kennedy et al.; OSF edua3; CC BY 4.0; gab.ai posts)",
                                 "EDOS (Kirk et al. 2023; Rewire; CC0 1.0; Gab and Reddit posts)"],
        "share_alike_sources": [],
        "raw_cleanup": "raw downloads (incl. the dedupe-only HateXplain and SBIC files) deleted after the build (logs/cleanup.log); licence records, sha256 logs and tmp/records kept",
    }
    (HERE / "manifest_public3.json").write_text(json.dumps(man, indent=1, ensure_ascii=False))
    print(json.dumps(man["counts"]), json.dumps({k: v["rows_r1"] for k, v in per.items()}))


if __name__ == "__main__":
    main()
