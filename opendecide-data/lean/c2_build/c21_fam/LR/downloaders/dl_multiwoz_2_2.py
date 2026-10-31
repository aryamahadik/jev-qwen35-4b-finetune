"""LR-18 MultiWOZ 2.2 (budzianowski/multiwoz, MIT). train/ <- data/MultiWOZ_2.2/train/dialogues_*.json, schema.json and the
TRAIN dialogues' entries of dialog_acts.json (that file holds acts for all splits: it is staged in quarantine and filtered
by train dialogue id); dev/ and test/ dialogues -> quarantine. Source: https://github.com/budzianowski/multiwoz
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import download_common as dc  # noqa: E402

DATASET = "multiwoz_2_2"
REPO = "budzianowski/multiwoz"
BASE = "data/MultiWOZ_2.2"


def run():
    st = dc.Store(DATASET)
    sha = dc.gh_commit_sha(REPO, "master")
    st.log["upstream_commit"] = sha
    tree = [p for p, _ in dc.gh_tree(REPO, sha) if p.startswith(BASE + "/")]
    train_ids = set()
    other_ids = []
    counts = {}
    for p in sorted(tree):
        rel = p[len(BASE) + 1:]
        url = dc.raw_url(REPO, sha, p)
        if rel.startswith("train/") and rel.endswith(".json"):
            dc.fetch_to(url, st.train_path(rel))
            with open(st.train_path(rel), "r", encoding="utf-8") as f:
                dl = json.load(f)
            train_ids.update(d["dialogue_id"] for d in dl)
            st.add_train_file(rel, source_urls=[url], rows=len(dl))
            counts["train_dialogues"] = counts.get("train_dialogues", 0) + len(dl)
        elif (rel.startswith("dev/") or rel.startswith("test/")) and rel.endswith(".json"):
            dc.fetch_to(url, st.quar_path(rel))
            n = len(json.load(open(st.quar_path(rel), "r", encoding="utf-8")))
            st.add_quar_file(rel, role=rel.split("/")[0], source_urls=[url], rows=n)
            k = rel.split("/")[0] + "_dialogues"
            counts[k] = counts.get(k, 0) + n
            other_ids.extend(x["dialogue_id"] for x in json.load(open(st.quar_path(rel), "r", encoding="utf-8")))
        elif rel == "schema.json":
            dc.fetch_to(url, st.train_path(rel))
            st.add_train_file(rel, source_urls=[url])
    dc.record_overlap(st, "dialogue_id_train_vs_dev_test", train_ids, other_ids)
    au = dc.raw_url(REPO, sha, BASE + "/dialog_acts.json")
    path, info = st.stage(au, "dialog_acts.json")
    with open(path, "r", encoding="utf-8") as f:
        acts = json.load(f)
    tr_acts = {k: v for k, v in acts.items() if k in train_ids}
    st.write_train_json("dialog_acts.train.json", tr_acts, source_urls=[au], rows=len(tr_acts))
    st.log["staged_file"] = {"sha256": info["sha256"], "bytes": info["bytes"], "url": au, "all_entries": len(acts)}
    st.clear_staging()
    lic = dc.licence_record(
        DATASET, "LR-18",
        quote="It is released by Paweł Budzianowski from Cambridge Dialogue Systems Group under the MIT License.",
        quote_url="https://github.com/budzianowski/multiwoz", verify_url="https://raw.githubusercontent.com/%s/%s/README.md" % (REPO, sha),
        licence_class="MIT", provenance="human", tier="A", quote_alternatives=["The MIT License (MIT)"],
        notes="Human-human Wizard-of-Oz. System acts hand-annotated (only these are used; user acts are heuristic). "
              "The repo LICENSE file ('The MIT License (MIT)') is the code licence; the README states the dataset is released under it.")
    st.write_licence(lic)
    return st.finish({"counts": counts})


if __name__ == "__main__":
    print(dc.summarize(run()))
