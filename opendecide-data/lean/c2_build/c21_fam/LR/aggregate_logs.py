"""Aggregate logs/download_*.json into logs/TIER_A_SUMMARY.json: per dataset licence status, train / quarantine file counts, row
counts, split-overlap COUNTS, and the sha256 of every code file (common, downloader, mapper, test). Counts and shas only."""
import glob
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
MAP = {"aya_redteaming_en": "LR-01", "gandalf_summarization": "LR-02", "juliet_1_3": "LR-03", "datadog_malicious_packages": "LR-04",
       "logchunks": "LR-05", "hwu64": "LR-13", "snips_2017_06": "LR-14", "abcd": "LR-17", "multiwoz_2_2": "LR-18",
       "taskmaster": "LR-19", "scifact": "LR-21", "qasper": "LR-30", "commonsenseqa": "LR-47", "ethics_mturk": "LR-53",
       "boardgameqa": "LR-54"}


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.isfile(p) else None


def main():
    out = {"datasets": {}, "common_code": {f: sha(os.path.join(HERE, f)) for f in ("lr_common.py", "download_common.py", "smoke_real_train.py")}}
    for ds, lr in MAP.items():
        lp = os.path.join(HERE, "logs", "download_%s.json" % ds)
        d = json.load(open(lp)) if os.path.isfile(lp) else None
        ent = {"lr_id": lr}
        if d:
            ent.update({
                "licence_status": d["licence"]["status"], "licence_class": d["licence"]["licence_class"],
                "licence_page_sha256": d["licence"]["page_sha256"], "licence_record_sha256": d["licence"]["sha256"],
                "licence_fetched_utc": d["licence"]["fetched_utc"],
                "train_files": d["train_total_files"], "train_bytes": d["train_total_bytes"],
                "train_rows_logged": sum(e.get("rows") or 0 for e in d["train_files"]),
                "quarantine_files": d["quarantine_total_files"], "quarantine_rows_logged": sum(e.get("rows") or 0 for e in d["quarantine_files"]),
                "train_file_shas": {e["path"]: e["sha256"] for e in d["train_files"]} if len(d["train_files"]) <= 20 else
                {"(%d files)" % len(d["train_files"]): hashlib.sha256("".join(e["sha256"] for e in sorted(d["train_files"], key=lambda e: e["path"])).encode()).hexdigest()},
                "quarantine_file_shas": {e["path"]: e["sha256"] for e in d["quarantine_files"]} if len(d["quarantine_files"]) <= 20 else
                {"(%d files)" % len(d["quarantine_files"]): hashlib.sha256("".join(e["sha256"] for e in sorted(d["quarantine_files"], key=lambda e: e["path"])).encode()).hexdigest()},
                "split_overlap_counts": d.get("split_overlap_counts"), "counts": d.get("counts"),
                "upstream": d.get("upstream_commit") or d.get("upstream_revision"), "finished_utc": d["finished_utc"], "notes": d.get("notes"),
            })
        ent["code_sha256"] = {
            "downloader": sha(os.path.join(HERE, "downloaders", "dl_%s.py" % ds)),
            "mapper": sha(os.path.join(HERE, "mappers", "%s.py" % ds)),
            "test": sha(os.path.join(HERE, "tests", "test_%s.py" % ds)),
        }
        out["datasets"][ds] = ent
    with open(os.path.join(HERE, "logs", "TIER_A_SUMMARY.json"), "w") as f:
        json.dump(out, f, indent=1)
    for ds, e in out["datasets"].items():
        print("%-28s %-6s licence=%-18s train_files=%-4s train_rows=%-7s quar_files=%-3s" % (
            ds, e["lr_id"], e.get("licence_status"), e.get("train_files"), e.get("train_rows_logged"), e.get("quarantine_files")))


if __name__ == "__main__":
    main()
