"""Aggregate logs/download_<set>.json (tier C) + logs/smoke_tierc.json into logs/TIER_C_SUMMARY.json: licence status, train / quarantine
file counts, row counts, split-overlap COUNTS, downloaded bytes and the sha256 of every code file. Counts and shas only."""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SETS = {"cuad": "LR-23", "ecare": "LR-49", "social_iqa": "LR-48", "quartz": "LR-50", "strategyqa": "LR-52", "finqa": "LR-44",
        "mbpp": "LR-12", "swe_gym": "LR-09", "commitpackft": "LR-11"}


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.isfile(p) else None


def main():
    smoke = {r["dataset"]: r for r in json.load(open(os.path.join(HERE, "logs", "smoke_tierc.json")))} if os.path.isfile(os.path.join(HERE, "logs", "smoke_tierc.json")) else {}
    out = {"common_code": {f: sha(os.path.join(HERE, f)) for f in ("lr_tierc_common.py", "smoke_tierc.py", "deny_evidence.py", "aggregate_tierc_logs.py")},
           "datasets": {}}
    for ds, lr in SETS.items():
        lp = os.path.join(HERE, "logs", "download_%s.json" % ds)
        d = json.load(open(lp)) if os.path.isfile(lp) else None
        ent = {"lr_id": lr}
        if d:
            staged = d.get("staged_file", {}).get("bytes", 0) + sum(v.get("bytes", 0) for k, v in d.items() if k.startswith("upstream_") and isinstance(v, dict))
            ent.update({
                "licence_status": d["licence"]["status"], "licence_class": d["licence"]["licence_class"],
                "licence_page_sha256": d["licence"]["page_sha256"], "licence_record_sha256": d["licence"]["sha256"],
                "licence_fetched_utc": d["licence"]["fetched_utc"],
                "train_files": d["train_total_files"], "train_bytes": d["train_total_bytes"],
                "quarantine_files": d["quarantine_total_files"],
                "quarantine_bytes": sum(e["bytes"] for e in d["quarantine_files"]),
                "quarantine_rows_logged": sum(e.get("rows") or 0 for e in d["quarantine_files"]),
                "train_file_shas": {e["path"]: e["sha256"] for e in d["train_files"]} if len(d["train_files"]) <= 20 else
                {"(%d files)" % len(d["train_files"]): hashlib.sha256("".join(e["sha256"] for e in sorted(d["train_files"], key=lambda e: e["path"])).encode()).hexdigest()},
                "quarantine_file_shas": {e["path"]: e["sha256"] for e in d["quarantine_files"]},
                "split_overlap_counts": d.get("split_overlap_counts"), "counts": d.get("counts"),
                "upstream": d.get("upstream_commit") or d.get("upstream_revision") or d.get("upstream_revision_card"),
                "finished_utc": d["finished_utc"], "notes": d.get("notes"), "train_dropped_fields": d.get("train_dropped_fields"),
                "upstream_bytes_fetched_for_train_side_staging": staged,
            })
        s = smoke.get(ds)
        if s:
            ent["smoke"] = {k: s.get(k) for k in ("rows_at_cap", "rows_available", "available_by_form", "available_yes_rate", "source_records_read",
                                                  "available_is_sample_measurement", "problems", "candidate_(code,test)_pairs_before_execution", "note")}
        ent["code_sha256"] = {"downloader": sha(os.path.join(HERE, "downloaders", "dl_%s.py" % ds)),
                              "mapper": sha(os.path.join(HERE, "mappers", "%s.py" % ds)), "test": sha(os.path.join(HERE, "tests", "test_%s.py" % ds))}
        out["datasets"][ds] = ent
    with open(os.path.join(HERE, "logs", "TIER_C_SUMMARY.json"), "w") as f:
        json.dump(out, f, indent=1)
    for ds, e in out["datasets"].items():
        print("%-14s %-6s licence=%-3s train_files=%-4s train_bytes=%-10s quar_files=%-3s quar_bytes=%-9s" % (
            ds, e["lr_id"], e.get("licence_status"), e.get("train_files"), e.get("train_bytes"), e.get("quarantine_files"), e.get("quarantine_bytes")))


if __name__ == "__main__":
    main()
