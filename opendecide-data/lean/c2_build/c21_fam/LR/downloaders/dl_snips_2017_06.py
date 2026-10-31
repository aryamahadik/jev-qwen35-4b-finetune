"""LR-14 SNIPS NLU 2017-06-custom-intent-engines ONLY (folders 2016-12 and 2018-01 are excluded).
train/ <- train_<Intent>.json and train_<Intent>_full.json (7 intents); quarantine <- validate_<Intent>.json (the validation split).
Source: https://github.com/snipsco/nlu-benchmark (LICENSE: CC0 1.0 Universal).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import download_common as dc  # noqa: E402

DATASET = "snips_2017_06"
REPO = "snipsco/nlu-benchmark"
BASE = "2017-06-custom-intent-engines"
INTENTS = ["AddToPlaylist", "BookRestaurant", "GetWeather", "PlayMusic", "RateBook", "SearchCreativeWork", "SearchScreeningEvent"]


def run():
    st = dc.Store(DATASET)
    sha = dc.gh_commit_sha(REPO, "master")
    st.log["upstream_commit"] = sha
    tree = {p for p, _ in dc.gh_tree(REPO, sha)}
    n_tr = n_va = 0
    for it in INTENTS:
        for fn, dest, role in (("train_%s.json" % it, "train", None), ("train_%s_full.json" % it, "train", None),
                               ("validate_%s.json" % it, "quar", "validation")):
            p = "%s/%s/%s" % (BASE, it, fn)
            if p not in tree:
                st.log["notes"].append("missing upstream file: " + p)
                continue
            url = dc.raw_url(REPO, sha, p)
            if dest == "train":
                dc.fetch_to(url, st.train_path(fn))
                st.add_train_file(fn, source_urls=[url])
                n_tr += 1
            else:
                dc.fetch_to(url, st.quar_path("validation/" + fn))
                st.add_quar_file("validation/" + fn, role=role, source_urls=[url])
                n_va += 1
    import glob, json
    def texts(root, pat):
        out = []
        for f in glob.glob(os.path.join(root, pat)):
            d = json.loads(open(f, "rb").read().decode("utf-8", "replace"))
            for qs in d.values():
                out.extend("".join(seg.get("text", "") for seg in q["data"]) for q in qs)
        return out
    tr_t, va_t = texts(st.train_dir, "train_*.json"), texts(st.quar_dir, "validation/validate_*.json")
    dc.record_overlap(st, "utterance_text_train_vs_validate", tr_t, va_t)
    st.log["queries"] = {"train_files_queries": len(tr_t), "validate_queries": len(va_t)}
    lic = dc.licence_record(
        DATASET, "LR-14", quote="CC0 1.0 Universal", quote_url="https://github.com/snipsco/nlu-benchmark",
        verify_url="https://raw.githubusercontent.com/%s/%s/LICENSE" % (REPO, sha), licence_class="CC0-1.0",
        provenance="human", tier="A",
        notes="Folder README: queries 'generated for each intent with crowdsourcing methods'. 2016-12 and 2018-01 folders excluded.")
    st.write_licence(lic)
    return st.finish({"counts": {"train_files": n_tr, "validation_files": n_va}})


if __name__ == "__main__":
    print(dc.summarize(run()))
