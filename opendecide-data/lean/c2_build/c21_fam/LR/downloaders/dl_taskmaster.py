"""LR-19 Taskmaster TM-1, TM-2, TM-3 (google-research-datasets/Taskmaster, CC BY 4.0; TM-4 excluded).
TM-1: self-dialogs.json + woz-dialogs.json are staged in quarantine. The shipped train/dev/test id lists cover the SELF
      dialogues only: self-dialogs are split by PROGRAM with train.csv (everything not on the train list -> quarantine);
      woz-dialogs have no shipped split: own seeded 10% hold-out by conversation_id -> quarantine, the rest -> train/.
TM-2: no split exists: own seeded 10% hold-out by conversation_id -> quarantine; the rest -> train/.
TM-3: the shipped splits/train/*.tsv shards are concatenated in order into train/tm3_train.tsv.gz (examples: dialogue prefix
      -> next move, with the dialogue id); splits/dev and splits/test shards -> quarantine. The un-split data/*.json is not fetched.
Source: https://github.com/google-research-datasets/Taskmaster
"""
import gzip
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import download_common as dc  # noqa: E402

DATASET = "taskmaster"
REPO = "google-research-datasets/Taskmaster"
TM2 = ["flights", "food-ordering", "hotels", "movies", "music", "restaurant-search", "sports"]


def run():
    st = dc.Store(DATASET)
    sha = dc.gh_commit_sha(REPO, "master")
    st.log["upstream_commit"] = sha
    tree = [p for p, _ in dc.gh_tree(REPO, sha)]
    U = lambda p: dc.raw_url(REPO, sha, p)  # noqa: E731
    counts = {}

    # ---- TM-1 ----
    ids = {}
    for sp in ("train", "dev", "test"):
        url = U("TM-1-2019/train-dev-test/%s.csv" % sp)
        path, _ = st.stage(url, "tm1_%s.csv" % sp)
        ids[sp] = set(re.findall(r"dlg-[0-9a-f-]{36}", open(path, "r", encoding="utf-8").read()))
    counts["tm1_ids"] = {k: len(v) for k, v in ids.items()}
    tm1_train, tm1_rest = [], []
    for name in ("self-dialogs.json", "woz-dialogs.json"):
        url = U("TM-1-2019/" + name)
        path, info = st.stage(url, name)
        with open(path, "r", encoding="utf-8") as f:
            dl = json.load(f)
        for d in dl:
            d["_tm1_file"] = name
            if name == "self-dialogs.json":
                is_train = d["conversation_id"] in ids["train"]
            else:
                is_train = not dc.holdout_unit("taskmaster1woz|%s" % d["conversation_id"])
            (tm1_train if is_train else tm1_rest).append(d)
    dc.record_overlap(st, "tm1_self_conversation_id_train_vs_not_train", [d["conversation_id"] for d in tm1_train if d["_tm1_file"] == "self-dialogs.json"],
                      [d["conversation_id"] for d in tm1_rest if d["_tm1_file"] == "self-dialogs.json"])
    st.write_train_json("tm1_train.json.gz", tm1_train, source_urls=[U("TM-1-2019/self-dialogs.json"), U("TM-1-2019/woz-dialogs.json")], rows=len(tm1_train))
    st.write_quar_json("tm1_not_train.json.gz", tm1_rest, role="self_dev_test_plus_woz_holdout10", rows=len(tm1_rest))
    counts["tm1_train_dialogues"], counts["tm1_not_train_dialogues"] = len(tm1_train), len(tm1_rest)
    ont = U("TM-1-2019/ontology.json")
    dc.fetch_to(ont, st.train_path("tm1_ontology.json"))
    st.add_train_file("tm1_ontology.json", source_urls=[ont])
    del tm1_train, tm1_rest

    # ---- TM-2 ----
    n_tr = n_ho = 0
    for dom in TM2:
        url = U("TM-2-2020/data/%s.json" % dom)
        path, _ = st.stage(url, "tm2_%s.json" % dom)
        with open(path, "r", encoding="utf-8") as f:
            dl = json.load(f)
        tr = [d for d in dl if not dc.holdout_unit("taskmaster2|%s" % d["conversation_id"])]
        ho = [d for d in dl if dc.holdout_unit("taskmaster2|%s" % d["conversation_id"])]
        st.write_train_json("tm2_%s.train.json.gz" % dom, tr, source_urls=[url], rows=len(tr))
        st.write_quar_json("tm2_%s.holdout10.json.gz" % dom, ho, role="own_frozen_holdout_10pct", source_urls=[url], rows=len(ho))
        n_tr += len(tr)
        n_ho += len(ho)
        o = U("TM-2-2020/ontology/%s.json" % dom)
        dc.fetch_to(o, st.train_path("tm2_ontology_%s.json" % dom))
        st.add_train_file("tm2_ontology_%s.json" % dom, source_urls=[o])
    counts["tm2_train_dialogues"], counts["tm2_holdout_dialogues"] = n_tr, n_ho
    st.clear_staging()

    # ---- TM-3 ----
    for part in ("train", "dev", "test"):
        shards = sorted(p for p in tree if p.startswith("TM-3-2020/splits/%s/" % part) and p.endswith(".tsv"))
        if part == "train":
            out = st.train_path("tm3_train.tsv.gz")
            with gzip.open(out, "wb", compresslevel=6) as g:
                for p in shards:
                    tmp = st.quar_path("_staging/" + os.path.basename(p))
                    info = dc.fetch_to(U(p), tmp)
                    with open(tmp, "rb") as f:
                        g.write(f.read())
                    st.log.setdefault("tm3_train_shards", []).append({"shard": os.path.basename(p), "sha256": info["sha256"], "bytes": info["bytes"]})
                    os.remove(tmp)
            with gzip.open(out, "rb") as g:
                nl = sum(blk.count(b"\n") for blk in iter(lambda: g.read(1 << 22), b""))
            counts["tm3_train_newlines"] = nl
            st.add_train_file("tm3_train.tsv.gz", source_urls=[U(p) for p in shards[:1]] + ["...%d shards" % len(shards)], note="cat of %d train shards in name order" % len(shards))
        else:
            for p in shards:
                rel = "tm3_%s/%s" % (part, os.path.basename(p))
                dc.fetch_to(U(p), st.quar_path(rel))
                st.add_quar_file(rel, role=part, source_urls=[U(p)])
    st.clear_staging()

    # ---- licence: the README of each folder carries the CC BY 4.0 statement ----
    q = "made available under the Creative Commons Attribution 4.0 License"
    recs = []
    for folder in ("TM-1-2019", "TM-2-2020", "TM-3-2020"):
        recs.append(dc.licence_record(DATASET, "LR-19", quote=q, quote_url="https://github.com/%s/tree/master/%s" % (REPO, folder),
                                      verify_url=U(folder + "/README.md"), licence_class="CC-BY-4.0", provenance="human", tier="A"))
    main = dict(recs[2])
    main["per_folder"] = [{"folder": f, "status": r["status"], "page_sha256": r["page_sha256"], "fetched_utc": r["fetched_utc"]}
                          for f, r in zip(("TM-1-2019", "TM-2-2020", "TM-3-2020"), recs)]
    main["status"] = "OK" if all(r["status"] == "OK" for r in recs) else "QUOTE_NOT_VERIFIED"
    main["notes"] = "Crowd Wizard-of-Oz and self-dialogs (Byrne et al.). TM-4 excluded. TM-3 'TicketTalk'."
    st.write_licence(main)
    return st.finish({"counts": counts})


if __name__ == "__main__":
    print(dc.summarize(run()))
