"""Records the G5 blind read (C_DATA_SPEC v4 8 G5; public rows: 100 rows per dataset, dataset-level decisions only,
drop the dataset if > 8% clearly wrong). Reader: an independent Claude session (endgame-prep-5 B4 checker; not a
public-2 author), flag-only: no label was set, edited or chosen. Read: the sample of qc/g5_sample_ids.json, rendered by
qc/g5_render.py exactly as the model sees it (decoder_io.user_msg, cygnet / schema_branch_mark) plus the gold letter.
Flags below are sample positions -> row ids; reasons are short and never quote row text."""
import json

from qclib import DATASETS, QC, sha256_file, write_gate

BAR = 0.08
FLAGS = {  # dataset -> {"wrong": {pos: reason}, "ambiguous": {pos: reason}}
    "c_pub_drop": {
        "wrong": {67: "upstream DROP noise: question is about a different game than the passage (join verified correct "
                      "against the raw zip: the query id belongs to this passage)",
                  68: "count of TD passes in the passage is 5; gold option says 4 (no correct option shown)",
                  82: "passage gives the season total through five games incl. this one; gold adds this game again"},
        "ambiguous": {12: "total points depends on unstated extra points (passage-only sum 42 vs real 47)",
                      32: "'years span these events' has no single reading; 464 is also stated",
                      72: "'months after' 26 Apr -> 18 May: 0 full months vs 1 calendar month (both options shown)",
                      97: "question mixes the 1438 grant and the 1453 marriage; gold uses 1438",
                      99: "passage gives 1908-1911 as the aftermath period, not the revolution's length"}},
    "c_pub_hybridqa": {
        "wrong": {53: "no shown passage has the birth date asked; gold option is the notability of a professor whose "
                      "passage gives a different birth date (upstream answer-node noise)"},
        "ambiguous": {14: "two shown passages (black and white pepper) carry the same 5 mm text; two options fit",
                      30: "the deciding fact ('greenest region in Europe') is not in the shown passage (excerpt)",
                      39: "two options' engine passages both name Société des Moteurs Le Rhône",
                      40: "swimming also had six events per the shown passages; two options fit",
                      83: "the shown evidence does not say which season Southern California won"}},
    "c_pub_wikisql": {
        "wrong": {},
        "ambiguous": {19: "two options have a 'Decision' method (exact-match rule picks the gold; natural reading "
                          "admits both)"}},
    "c_pub_uci_car": {"wrong": {}, "ambiguous": {}},
    "c_pub_uci_nursery": {"wrong": {}, "ambiguous": {}},
}


def main():
    s = json.load(open(QC / "g5_sample_ids.json"))
    nums, fails = {}, []
    for ds in DATASETS:
        ids = s["sample"][ds]
        f = FLAGS[ds]
        w, a = len(f["wrong"]), len(f["ambiguous"])
        nums[ds] = {"read": len(ids), "clearly_wrong": w, "clearly_wrong_rate": round(w / len(ids), 4),
                    "ambiguous": a, "ambiguous_rate": round(a / len(ids), 4),
                    "dataset_decision": "keep" if w / len(ids) <= BAR else "DROP (> 8% clearly wrong)",
                    "flagged": {"wrong": {ids[k]: v for k, v in f["wrong"].items()},
                                "ambiguous": {ids[k]: v for k, v in f["ambiguous"].items()}}}
        if len(ids) < 100 or w / len(ids) > BAR:
            fails.append(ds)
    nums["sample_file_sha256"] = sha256_file(QC / "g5_sample_ids.json")
    nums["notes"] = ["UCI rows: every row re-derived by hand through the shown DEX tables (and by program in "
                     "labels_roundtrip: 0 mismatches)",
                     "WikiSQL rows: every value / count / sum / min / max re-computed from the shown table",
                     "the ambiguous <= 1% bar applies to own families; public rows are judged at dataset level only "
                     "(spec 8 G5); ambiguous counts are reported for the record",
                     "observation (not a gate): HybridQA passages are short excerpts; 1 of 100 rows lost its deciding "
                     "sentence (pos 30)"]
    write_gate("G5", not fails, nums, fails=fails, reader="independent Claude session, flag-only",
               bar="drop a dataset if > 8% of its 100-row read is clearly wrong (spec 8 G5, public rows)")
    print("G5", not fails, {d: (nums[d]["clearly_wrong"], nums[d]["ambiguous"]) for d in DATASETS})


if __name__ == "__main__":
    main()
