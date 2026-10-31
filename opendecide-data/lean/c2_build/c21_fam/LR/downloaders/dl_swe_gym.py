"""LR-09 SWE-Gym (SWE-Gym/SWE-Gym; Pan et al. 2024): the 2,438 INSTANCES only, never its trajectories or verifiers.
Tier C check C12: per-repo licence of the 11 source repos against the ONE code whitelist (MIT, Apache-2.0, BSD-2-Clause,
BSD-3-Clause, CC0-1.0; Opus LR-M3), looked up on the GitHub licence API (SPDX id as licensee reports it). Rows of a repo that is not
on the whitelist are NOT written (counted, logged). FIELD DROPS (Opus LR-M8, strict A82 4 reading): problem_statement and hints_text
(GitHub issue text written by third parties) and PASS_TO_PASS (an execution list, large, unused). Kept: instance_id, repo,
base_commit, version, created_at, patch, test_patch, FAIL_TO_PASS. The parquet is a single 'train' split (no test split exists).
No split exists, so rule 2 of plan 16.3 applies: a seeded 10% hold-out (dc.holdout_unit on 'swe_gym|<instance_id>') is routed by program into
quarantine/holdout10/ (an internal G13 target, never trained, never opened). The unit is the INSTANCE: holding out a whole repo would
mean 1 of 10 repos (the seeded choice, bokeh, has 26 instances) or 2 of 10 (including pandas, 30% of the rows).
Instance-level G13 against SWE-bench / SWE-bench-Live / SWE-rebench (plan K9) is the registry program's job, not this downloader's.
"""
import os
import sys

import pyarrow.parquet as pq

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import download_common as dc  # noqa: E402
import lr_tierc_common as tc  # noqa: E402

DATASET = "swe_gym"
HF = "SWE-Gym/SWE-Gym"
GH = "SWE-Gym/SWE-Gym"
KEEP = ("instance_id", "repo", "base_commit", "version", "created_at", "patch", "test_patch", "FAIL_TO_PASS")
DROP = ("problem_statement", "hints_text", "PASS_TO_PASS")


def run():
    st = dc.Store(DATASET)
    rev = dc.hf_revision(HF)
    st.log["upstream_revision"] = rev
    url = dc.hf_url(HF, rev, "data/train-00000-of-00001.parquet")
    p, info = st.stage(url, "train.parquet")
    t = pq.read_table(p)
    cols = t.column_names
    rows = t.to_pylist()
    st.log["upstream_train_parquet"] = {"sha256": info["sha256"], "bytes": info["bytes"], "url": url, "columns": cols}
    st.log["train_dropped_fields"] = [c for c in cols if c not in KEEP]
    repos = sorted({r["repo"] for r in rows})
    table = {}
    for rp in repos:
        table[rp] = tc.github_repo_licence(rp)
        table[rp]["whitelisted"] = tc.whitelisted(table[rp]["spdx_id"])
    kept, held, dropped_by_repo, total_by_repo = [], [], {}, {}
    for r in rows:
        total_by_repo[r["repo"]] = total_by_repo.get(r["repo"], 0) + 1
        if not table[r["repo"]]["whitelisted"]:
            dropped_by_repo[r["repo"]] = dropped_by_repo.get(r["repo"], 0) + 1
            continue
        (held if dc.holdout_unit("swe_gym|" + r["instance_id"]) else kept).append({k: r[k] for k in KEEP})
    st.write_quar_json("holdout10/swe_gym_holdout10.jsonl.gz", held, role="holdout10", source_urls=[url], jsonl=True)
    st.write_train_json("train.jsonl.gz", kept, source_urls=[url], jsonl=True,
                        note="whitelisted-repo rows only; fields kept: %s" % ",".join(KEEP))
    rl = st.train_path("REPO_LICENCES.json")
    import json
    with open(rl, "w", encoding="utf-8") as f:
        json.dump({"whitelist": list(tc.CODE_WHITELIST_SPDX), "source": "GET https://api.github.com/repos/<repo>/license (no credentials)",
                   "repos": table, "rows_by_repo": total_by_repo, "rows_dropped_by_repo": dropped_by_repo}, f, indent=2)
    st.add_train_file("REPO_LICENCES.json", source_urls=["https://api.github.com/repos/<repo>/license"], rows=len(table))
    st.clear_staging()
    counts = {"instances_upstream": len(rows), "instances_kept_train": len(kept), "instances_held_out_quarantine": len(held), "instances_dropped_licence": sum(dropped_by_repo.values()),
              "repos": len(repos), "repos_whitelisted": sum(1 for v in table.values() if v["whitelisted"])}
    lic = tc.licence_with_checks(
        DATASET, "LR-09", quote="license: mit",
        quote_url="https://huggingface.co/datasets/SWE-Gym/SWE-Gym", verify_url=dc.hf_card_url(HF, rev),
        licence_class="MIT (HF card) / Apache-2.0 (GitHub repo) + per-repo whitelist filter (REPO_LICENCES.json)", provenance="human",
        notes="Card YAML 'license: mit'; GitHub repo SWE-Gym/SWE-Gym is Apache-2.0 (also_verified). Instances are human GitHub issues, "
              "human gold patches and human tests (SWE-Bench collection procedure). The code in a row keeps its repo's licence, so only "
              "whitelisted repos are written. Mapper labels use the human gold patch only (file lists), not execution lists.",
        also=[{"label": "SWE-Gym GitHub repo (Apache-2.0 badge on the repo page)", "quote": "Apache-2.0 license",
               "url": "https://github.com/SWE-Gym/SWE-Gym"}],
        extra={"repo_licences_file": "REPO_LICENCES.json"})
    st.write_licence(lic)
    return st.finish({"counts": counts})


if __name__ == "__main__":
    print(dc.summarize(run()))
