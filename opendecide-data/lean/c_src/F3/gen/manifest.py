"""out/MANIFEST.json: counts, sha256 of every output and code file, sampler / pack / style / wording coverage, the
pool-level balance figures against the F3 targets (final targets are checked on the selected set after G9), gate
results (G3, G4, G15, G18, length, negation quotas, fmt1 guard, sealed check) and problems. Counts only."""
from __future__ import annotations

import collections
import datetime as dt
import glob
import json
import os
import statistics
import sys

from f3common import (F3_DIR, FAMILY, GEN_VERSION, OUT, SPEC_ID, SPEC_SHA256, TMP, sha256_file)

PARTS = {"candidates": "candidates_r1.jsonl", "qc": "qc_sample.jsonl", "dev": "mixdev_S5.jsonl"}


def stats(rows, side):
    sid = {s["id"]: s for s in side}
    n = len(rows)
    yn = [r for r in rows if r["qtype"] == "noul"]
    ch = [r for r in rows if r["qtype"] == "choice"]
    c = collections.Counter
    out = {"rows": n, "yes_no_rows": len(yn), "choice_rows": len(ch),
           "yes_no_share": round(len(yn) / max(1, n), 4),
           "yes_rate_yes_no": round(sum(r["gold"] == 1 for r in yn) / max(1, len(yn)), 4),
           "by_sampler": dict(c(r["meta"]["sampler"] for r in rows)),
           "qt_share": {k: round(v / max(1, n), 4) for k, v in sorted(c(sid[r["id"]]["qt"] for r in rows).items())},
           "cards": len({r["meta"]["card_id"] for r in rows}),
           "packs": len({r["meta"]["domain_pack"] for r in rows}),
           "persona_seeds": len({r["meta"]["persona_seed"] for r in rows}),
           "format_styles": len({r["meta"]["format_style"] for r in rows}),
           "containers": dict(c(sid[r["id"]]["container"] for r in rows)),
           "wordings": len({r["meta"]["wording_id"] for r in rows}),
           "defs_style_rows": dict(c(r["meta"]["defs_style"] for r in rows)),
           "groups_logs": len({r["group_id"] for r in rows}),
           "units": len({r["call_id"] for r in rows}),
           "twin_kind": dict(c(str(r["meta"]["twin_kind"]) for r in rows)),
           "contrast_set_rows_share": round(sum(1 for r in rows if r["meta"]["twin_kind"] in ("fact_flip",
                                                                                               "premise_removal"))
                                            * 2 / max(1, n), 4),
           "attack_rows_share": round(sum(1 for r in rows if r["meta"]["twin_kind"] == "attack") / max(1, n), 4),
           "world_open_rows_share": round(sum(1 for r in rows if sid[r["id"]]["world"] == "open") / max(1, n), 4),
           "rule21_rows_share": round(sum(1 for r in rows if sid[r["id"]]["rule21"]) / max(1, n), 4),
           "inverted_rows_share": round(sum(1 for r in rows if sid[r["id"]]["inverted_card"]) / max(1, n), 4),
           "event_bin_share": {str(k): round(v / max(1, n), 4) for k, v in
                               sorted(c(sid[r["id"]]["event_bin"] for r in rows).items())},
           "depth": dict(sorted(c(r["meta"]["depth"] for r in rows).items())),
           "deep_share": round(sum(1 for r in rows if r["meta"]["deep"]) / max(1, n), 4),
           "decisive_decile": dict(sorted(c(str(sid[r["id"]]["decisive_decile"]) for r in rows).items())),
           "mechanism_on_path": dict(c(m for r in rows for m in sid[r["id"]]["mechanisms"])),
           "real_tokens": {"median": statistics.median(sid[r["id"]]["real_tokens"] for r in rows),
                           "max": max(sid[r["id"]]["real_tokens"] for r in rows)},
           "polarity_yes_bad_share": round(sum(1 for r in yn if _yes_bad(r, sid[r["id"]])) / max(1, len(yn)), 4)}
    buckets = c()
    for r in ch:
        k = len(r["options"])
        buckets[0 if k <= 4 else 1 if k <= 9 else 2 if k <= 19 else 3] += 1
    out["option_bucket_share"] = {lab: round(buckets[i] / max(1, len(ch)), 4) for i, lab in
                                  enumerate(("2-4", "5-9", "10-19", "20-60"))}
    out["status_option_rows_share_of_choice"] = {
        v: round(sum(1 for r in ch if sid[r["id"]]["status_option_row"] and sid[r["id"]]["vocab"] == v)
                 / max(1, len(ch)), 4) for v in ("masked", "swapped")}
    ab = c()
    for r in ch:
        s = sid[r["id"]]
        if s["abstain"]:
            ab[(s["abstain"], s["gold_is_abstain"])] += 1
    out["abstain_rows"] = {f"{k[0]}:{'gold' if k[1] else 'not_gold'}": v for k, v in ab.items()}
    out["neg_form"] = dict(c(str(sid[r["id"]]["neg_form"]) for r in yn))
    return out


def _yes_bad(r, s):
    """'Yes = bad outcome' (B04): the row's polarity tag is computed on the claim as asked, negation included
    (complement twins carry the flipped tag), so a row counts when its tag is 'bad'."""
    return s.get("polarity") == "bad"


def main(problems=None):
    m = {"family": FAMILY, "spec_id": SPEC_ID, "g0_sha256": SPEC_SHA256, "gen_version": GEN_VERSION,
         "written_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
         "binding": {"PREREG_FINAL": "A15, A16, A16.1", "C_DATA_SPEC": "v4 4ca129963bef3e0a",
                     "C_TRAIN_RECIPE": "v4 f4b7915088942f9b", "decoder_io": "908c08d7",
                     "train_decoder": "c2c2d1d6"},
         "files": {}, "parts": {}, "gates": {}, "code": {}, "problems": problems or []}
    for part, fn in PARTS.items():
        p = OUT / fn
        if not p.exists():
            continue
        rows = [json.loads(l) for l in open(p)]
        side = [json.loads(l) for l in open(str(p)[:-6] + ".sidecar.jsonl")]
        for suffix in ("", ".sidecar", ".relations"):
            fp = str(p)[:-6] + suffix + ".jsonl"
            if os.path.exists(fp):
                m["files"][os.path.basename(fp)] = {"sha256": sha256_file(fp),
                                                    "lines": sum(1 for _ in open(fp))}
        m["parts"][part] = stats(rows, side)
        g = str(p)[:-6] + ".gates.json"
        if os.path.exists(g):
            m["gates"][part] = json.load(open(g))
        sq = str(p)[:-6] + ".sealedqc.summary.json"
        if os.path.exists(sq):
            s = json.load(open(sq))
            m["gates"].setdefault(part, {})["sealed_check"] = {k: s.get(k) for k in
                                                                ("rows", "rows_clean", "rows_hit", "rows_report_only",
                                                                 "checker_version", "checker_sha256",
                                                                 "suite_sha256")}
        br = str(p)[:-6] + ".build_report.json"
        if os.path.exists(br):
            b = json.load(open(br))
            m["parts"][part]["build"] = {k: b.get(k) for k in ("logs", "fail", "skips", "alt_check")}
    here = os.path.dirname(os.path.abspath(__file__))
    for f in sorted(glob.glob(os.path.join(here, "*.py"))):
        m["code"][os.path.basename(f)] = sha256_file(f)
    with open(OUT / "MANIFEST.json", "w") as f:
        json.dump(m, f, indent=1)
    return m


if __name__ == "__main__":
    pr = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else []
    main(pr)
