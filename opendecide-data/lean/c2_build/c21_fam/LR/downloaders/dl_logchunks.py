"""LR-05 LogChunks (Zenodo 3632351, CC BY 4.0): 797 Travis CI logs, 80 repos, human-labelled failure chunk.
No split exists: own seeded 10% hold-out BY REPO (<owner>@<name>) -> quarantine. train/ <- logchunks_train.zip
(readme, build-failure-reason XML + logs of the 90% repos, validation csv rows of those repos, repositories.txt filtered).
Source: https://zenodo.org/records/3632351
"""
import csv
import io
import os
import re
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import download_common as dc  # noqa: E402

DATASET = "logchunks"
URL = "https://zenodo.org/api/records/3632351/files/LogChunks.zip/content"
PAGE = "https://zenodo.org/records/3632351"
_REPO_IN_PATH = re.compile(r"/(?:logs|build-failure-reason)/[^/]+/([^/]+?)(?:\.xml)?(?:/|$)")


def repo_of(name):
    m = _REPO_IN_PATH.search("/" + name)
    return m.group(1) if m and "@" in m.group(1) else None


def run():
    st = dc.Store(DATASET)
    path, info = st.stage(URL, "LogChunks.zip")
    st.log["staged_file"] = {"sha256": info["sha256"], "bytes": info["bytes"], "url": URL}
    train_repos, hold_repos = set(), set()
    tr = st.train_path("logchunks_train.zip")
    hq = st.quar_path("logchunks_holdout_repos.zip")
    os.makedirs(os.path.dirname(hq), exist_ok=True)
    n_logs_tr = n_logs_ho = 0
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tr, "w", zipfile.ZIP_DEFLATED) as ztr, \
            zipfile.ZipFile(hq, "w", zipfile.ZIP_DEFLATED) as zho:
        names = [n for n in zin.namelist() if not n.startswith("__MACOSX") and not n.endswith("/") and ".DS_Store" not in n]
        all_repos = {repo_of(n) for n in names if repo_of(n)}
        hold_repos = dc.holdout_set(all_repos, "logchunks")        # exactly ceil(10% of 80) = 8 repos
        train_repos = all_repos - hold_repos
        for n in names:
            r = repo_of(n)
            if r:
                if r in hold_repos:
                    zho.writestr(n, zin.read(n))
                    n_logs_ho += n.endswith(".log")
                else:
                    ztr.writestr(n, zin.read(n))
                    n_logs_tr += n.endswith(".log")
            elif n.endswith("readme.md") and n.count("/") == 1:
                ztr.writestr(n, zin.read(n))
            elif n.endswith("repositories.txt"):
                txt = zin.read(n).decode("utf-8", "replace")
                keep = [ln for ln in txt.splitlines() if any(ln.strip().replace("/", "@") == t for t in train_repos) or not ln.strip()]
                ztr.writestr(n, "\n".join(keep) + "\n")
            elif n.endswith("developer-crossvalidation.csv"):
                txt = zin.read(n).decode("utf-8", "replace")
                rd = csv.reader(io.StringIO(txt))
                hdr = next(rd)
                io_ = io.StringIO()
                w = csv.writer(io_)
                w.writerow(hdr)
                io_i, io_n = hdr.index("repository_owner"), hdr.index("repository_name")
                for row in rd:
                    if len(row) > io_n and ("%s@%s" % (row[io_i], row[io_n])) in train_repos:
                        w.writerow(row)
                ztr.writestr(n, io_.getvalue())
            # log-collection/*.rb / sql tool files are not data and are not copied
    st.add_train_file("logchunks_train.zip", source_urls=[PAGE], rows=n_logs_tr, note="rows = .log files of the 90% repos")
    st.add_quar_file("logchunks_holdout_repos.zip", role="own_frozen_holdout_by_repo", source_urls=[PAGE], rows=n_logs_ho)
    st.clear_staging()
    lic = dc.licence_record(
        DATASET, "LR-05", quote="Creative Commons Attribution 4.0 International", quote_url=PAGE, verify_url=PAGE,
        licence_class="CC-BY-4.0", provenance="human", tier="A",
        notes="Failure chunks labelled manually and validated with the original developers (Brandt et al., MSR 2020).")
    st.write_licence(lic)
    return st.finish({"counts": {"train_repos": len(train_repos), "holdout_repos": len(hold_repos),
                                 "train_logs": n_logs_tr, "holdout_logs": n_logs_ho}})


if __name__ == "__main__":
    print(dc.summarize(run()))
