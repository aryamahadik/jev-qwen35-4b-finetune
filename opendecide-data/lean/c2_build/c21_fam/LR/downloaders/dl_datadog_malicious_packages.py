"""LR-04 DataDog malicious-software-packages-dataset: ONLY the per-ecosystem samples/<eco>/manifest.json label files
(package name -> null for malicious-intent, or the list of compromised versions). The encrypted payload ZIPs under
samples/** are NEVER fetched, opened or executed. No split exists: own seeded 10% hold-out by package name -> quarantine.
LR-B5: rows are T63 realism rows; LR-04 maps nothing before the T63 G0-lite is approved (see the mapper).
Source: https://github.com/DataDog/malicious-software-packages-dataset (Apache-2.0).
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import download_common as dc  # noqa: E402

DATASET = "datadog_malicious_packages"
REPO = "DataDog/malicious-software-packages-dataset"
_MANIFEST = re.compile(r"^samples/[^/]+/manifest\.json$")


def run():
    st = dc.Store(DATASET)
    sha = dc.gh_commit_sha(REPO, "main")
    st.log["upstream_commit"] = sha
    # the repo tree is too large for the tree API (truncated), so the four ecosystems named in the README are fetched directly
    paths = ["samples/%s/manifest.json" % e for e in ("npm", "pypi", "ide_extensions", "ai-skills")]
    counts = {}
    for p in sorted(paths):
        eco = p.split("/")[1]
        url = dc.raw_url(REPO, sha, p)
        tmp = st.quar_path("_staging/%s.manifest.json" % eco)
        dc.fetch_to(url, tmp)
        with open(tmp, "r", encoding="utf-8") as f:
            d = json.load(f)
        train = {k: v for k, v in d.items() if not dc.holdout_unit("datadog|%s|%s" % (eco, k))}
        hold = {k: v for k, v in d.items() if dc.holdout_unit("datadog|%s|%s" % (eco, k))}
        st.write_train_json("%s.manifest.train.json" % eco, train, source_urls=[url], rows=len(train))
        st.write_quar_json("%s.manifest.holdout10.json" % eco, hold, role="own_frozen_holdout_10pct", source_urls=[url], rows=len(hold))
        counts[eco] = {"all": len(d), "train": len(train), "holdout": len(hold)}
    st.clear_staging()
    page = "https://raw.githubusercontent.com/%s/%s/README.md" % (REPO, sha)
    lic = dc.licence_record(
        DATASET, "LR-04", quote="This dataset is released under the Apache-2.0 license.",
        quote_url="https://github.com/DataDog/malicious-software-packages-dataset", verify_url=page,
        licence_class="Apache-2.0", provenance="human", tier="A",
        notes="Publisher claim: packages 'manually triaged by a human' (README FAQ). Payload code keeps its original licence "
              "and is never used. Selection bias disclosed by the publisher (mostly one ruleset).")
    st.write_licence(lic)
    return st.finish({"counts": counts})


if __name__ == "__main__":
    print(dc.summarize(run()))
