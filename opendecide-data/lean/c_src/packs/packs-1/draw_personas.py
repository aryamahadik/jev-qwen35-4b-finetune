#!/usr/bin/env python3
"""packs-1: draw O*NET persona seeds by program (C_DATA_SPEC v4 2.1, F4).

Titles only, from the O*NET 31.0 main occupation file (occupation_data.csv; never the alternate-titles or SOC
direct-match file). Fixed seed, spread over the O*NET major groups of this agent's quarter of the setting space
(industry and operations: manufacturing, logistics, utilities, construction, agriculture as a business, retail ops).
The group rule and the quotas below were fixed before the draw. Titles containing "All Other" are skipped.
Output: persona_draw.json (drawn seeds in order + ordered spares per group for replacements).
"""
import csv
import hashlib
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEED = 20261003
SRC = HERE / "tmp" / "occupation_data.csv"
SRC_URL = "https://www.onetcenter.org/dl_files/database/db_31_0_csv/occupation_data.csv"
LICENCE_URL = "https://www.onetcenter.org/license_db.html"

# (group id, code prefixes, quota). Prefix match on the O*NET-SOC code.
GROUPS = [
    ("11-ops-managers", ["11-1021", "11-3013", "11-3051", "11-3061", "11-3071", "11-9013", "11-9021", "11-9041"], 7),
    ("13-business-ops", ["13-102", "13-1051", "13-108", "13-1041.01"], 5),
    ("17-engineering", ["17-"], 9),
    ("19-technicians", ["19-4012", "19-4013", "19-4031", "19-4042", "19-4043", "19-4051", "19-5011", "19-5012"], 3),
    ("41-retail-wholesale", ["41-1011", "41-1012", "41-2011", "41-2021", "41-2022", "41-2031", "41-4011",
                             "41-4012"], 5),
    ("43-material-scheduling", ["43-5"], 7),
    ("45-farming-fishing-forestry", ["45-"], 7),
    ("47-construction-extraction", ["47-"], 10),
    ("49-install-maint-repair", ["49-"], 10),
    ("51-production", ["51-"], 14),
    ("53-transport-material-moving", ["53-"], 11),
]


def main():
    raw = SRC.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    rows = list(csv.DictReader(raw.decode("utf-8").splitlines()))
    out = {"source": {"name": "O*NET 31.0 Database, Occupation Data (main occupation titles)", "url": SRC_URL,
                      "licence": "CC BY 4.0", "licence_record": LICENCE_URL, "sha256": sha, "rows": len(rows),
                      "fields_used": ["O*NET-SOC Code", "Title"]},
           "seed": SEED, "rule": "prefix groups + quotas fixed before the draw; 'All Other' titles skipped",
           "groups": [], "drawn": []}
    used = set()
    for gid, prefixes, quota in GROUPS:
        elig = sorted({(r["O*NET-SOC Code"], r["Title"]) for r in rows
                       if any(r["O*NET-SOC Code"].startswith(p) for p in prefixes) and "All Other" not in r["Title"]})
        rs = random.Random(int(hashlib.sha256(f"packs-1:{SEED}:{gid}".encode()).hexdigest(), 16))
        order = elig[:]
        rs.shuffle(order)
        order = [x for x in order if x[0] not in used]
        drawn, spares = order[:quota], order[quota:]
        used.update(c for c, _ in drawn)
        out["groups"].append({"group": gid, "prefixes": prefixes, "quota": quota, "eligible": len(elig),
                              "spares": [{"onet_code": c, "onet_title": t} for c, t in spares]})
        for c, t in drawn:
            out["drawn"].append({"group": gid, "onet_code": c, "onet_title": t})
    (HERE / "persona_draw.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print(f"drawn {len(out['drawn'])} seeds from {len(rows)} titles; sha256 {sha[:16]}")


if __name__ == "__main__":
    sys.exit(main())
