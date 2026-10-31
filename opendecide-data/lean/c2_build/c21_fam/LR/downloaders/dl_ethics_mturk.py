"""LR-53 ETHICS, MTurk subsets only (justice, deontology, virtue, utilitarianism, SHORT commonsense; hendrycks/ethics, MIT).
train/ <- <subset>/train.csv for the four MTurk subsets and commonsense/train.csv FILTERED to is_short == True (the long
commonsense rows are Reddit AITA posts, third-party social-platform text, excluded by A82 4 / the inventory: they are dropped
here and never written to train/). test.csv, test_hard.csv and (commonsense) ambig.csv of every subset -> quarantine.
Source: https://huggingface.co/datasets/hendrycks/ethics
"""
import csv
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import download_common as dc  # noqa: E402

DATASET = "ethics_mturk"
REPO = "hendrycks/ethics"
SUBSETS = ["justice", "deontology", "virtue", "utilitarianism", "commonsense"]


def run():
    st = dc.Store(DATASET)
    rev = dc.hf_revision(REPO)
    st.log["upstream_revision"] = rev
    counts = {}
    for sub in SUBSETS:
        url = dc.hf_url(REPO, rev, "data/%s/train.csv" % sub)
        path, info = st.stage(url, "%s_train.csv" % sub)
        raw = open(path, "r", encoding="utf-8", newline="").read()
        if sub == "commonsense":
            rd = csv.DictReader(io.StringIO(raw))
            keep = [r for r in rd if str(r.get("is_short")).strip().lower() == "true"]
            counts["commonsense_all_train"] = len(raw.splitlines()) - 1
            out = io.StringIO()
            w = csv.DictWriter(out, fieldnames=rd.fieldnames)
            w.writeheader()
            w.writerows(keep)
            os.makedirs(os.path.dirname(st.train_path("commonsense/train.short.csv")), exist_ok=True)
            with open(st.train_path("commonsense/train.short.csv"), "w", encoding="utf-8", newline="") as f:
                f.write(out.getvalue())
            st.add_train_file("commonsense/train.short.csv", source_urls=[url], rows=len(keep), note="is_short == True rows only")
            counts["commonsense_short_train"] = len(keep)
        else:
            os.makedirs(os.path.dirname(st.train_path(sub + "/train.csv")), exist_ok=True)
            with open(st.train_path(sub + "/train.csv"), "w", encoding="utf-8", newline="") as f:
                f.write(raw)
            n = len(list(csv.reader(io.StringIO(raw)))) - 1
            st.add_train_file(sub + "/train.csv", source_urls=[url], rows=n)
            counts[sub + "_train"] = n
        for extra in ("test.csv", "test_hard.csv", "ambig.csv"):
            if extra == "ambig.csv" and sub != "commonsense":
                continue
            u = dc.hf_url(REPO, rev, "data/%s/%s" % (sub, extra))
            rel = "%s/%s" % (sub, extra)
            dc.fetch_to(u, st.quar_path(rel))
            n = len(list(csv.reader(open(st.quar_path(rel), "r", encoding="utf-8", newline="")))) - 1
            st.add_quar_file(rel, role=extra.replace(".csv", ""), source_urls=[u], rows=n)
    st.clear_staging()
    lic = dc.licence_record(
        DATASET, "LR-53", quote="license: mit", quote_url="https://huggingface.co/datasets/hendrycks/ethics",
        verify_url=dc.hf_card_url(REPO, rev), licence_class="MIT", provenance="human", tier="A",
        notes="MTurk-written scenarios. Long commonsense rows (Reddit AITA) excluded at download.")
    st.write_licence(lic)
    return st.finish({"counts": counts})


if __name__ == "__main__":
    print(dc.summarize(run()))
