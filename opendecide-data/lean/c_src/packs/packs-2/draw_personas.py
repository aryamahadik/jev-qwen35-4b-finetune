#!/usr/bin/env python3
"""packs-2: draw O*NET persona seeds by program (C_DATA_SPEC v4 2.1, F4).

Titles only, from the O*NET 31.0 main occupation file (occupation_data.csv; never the alternate-titles or SOC
direct-match file). Fixed seed. This agent's quarter is services and professions; each of its 8 sectors has an
explicit list of eligible main-title codes (fixed before the draw, each code in exactly one sector), spread over the
O*NET major groups 11, 13, 21, 23, 25, 29, 31, 35, 39, 41 and 43. Titles containing "All Other" are never eligible.
Each sector draws QUOTA seeds in a seeded order; the remaining eligible codes are ordered spares (replacements for
packs dropped by the sealed check). Output: persona_draw.json.
"""
import csv
import hashlib
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEED = 20261003
QUOTA = 10
SRC = HERE / "tmp" / "occupation_data.csv"
SRC_URL = "https://www.onetcenter.org/dl_files/database/db_31_0_csv/occupation_data.csv"
LICENCE_URL = "https://www.onetcenter.org/license_db.html"

SECTORS = [
    ("hc", "healthcare_admin", ["11-9111.00", "29-2072.00", "29-9021.00", "43-6013.00", "31-9092.00", "43-3021.00",
                                "29-1141.00", "11-9121.01", "21-1094.00", "31-9094.00", "43-4111.00", "21-1091.00",
                                "43-4071.00"]),
    ("lg", "legal_practice_admin", ["23-2011.00", "43-6012.00", "23-1011.00", "23-1012.00", "43-4031.00",
                                    "23-2093.00", "23-1022.00", "43-3031.00", "11-3012.00", "25-4011.00",
                                    "43-9022.00", "43-6011.00", "43-4021.00"]),
    ("ed", "education_admin", ["11-9031.00", "11-9032.00", "11-9033.00", "21-1012.00", "25-4022.00", "25-4031.00",
                               "43-4121.00", "25-9031.00", "25-3031.00", "25-9044.00", "43-6014.00", "25-1081.00",
                               "25-3011.00"]),
    ("hs", "hospitality", ["11-9081.00", "11-9051.00", "43-4081.00", "39-6012.00", "13-1121.00", "35-9031.00",
                           "35-1012.00", "43-4181.00", "11-9179.02", "39-7011.00", "41-3041.00", "11-9072.00",
                           "35-1011.00", "39-1014.00"]),
    ("fo", "finance_ops", ["11-3031.01", "11-3031.00", "13-2011.00", "43-3051.00", "43-3011.00", "13-2041.00",
                           "13-2031.00", "43-3061.00", "13-1023.00", "13-2099.04", "43-4041.00", "13-2054.00",
                           "43-3071.00", "43-4141.00"]),
    ("in", "insurance_ops", ["13-1031.00", "13-1032.00", "13-2053.00", "43-9041.00", "41-3021.00", "43-4051.00",
                             "13-2022.00", "13-2061.00", "43-9061.00", "11-9199.02", "13-1041.07", "13-1041.00"]),
    ("re", "real_estate_admin", ["11-9141.00", "41-9021.00", "41-9022.00", "13-2023.00", "43-4131.00",
                                 "13-2072.00", "11-3013.00", "41-2021.00", "43-4171.00", "13-1111.00",
                                 "13-2052.00", "43-4141.00"]),
    ("hr", "human_resources", ["11-3121.00", "13-1071.00", "43-4161.00", "11-3111.00", "13-1141.00", "11-3131.00",
                               "13-1151.00", "13-1075.00", "13-1041.03", "43-4199.00", "13-1082.00",
                               "43-1011.00"]),
]


def main():
    raw = SRC.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    rows = list(csv.DictReader(raw.decode("utf-8").splitlines()))
    title = {r["O*NET-SOC Code"]: r["Title"] for r in rows}
    seen = {}
    for code_, sec, codes in SECTORS:
        for c in codes:
            if c in seen and seen[c] != sec:
                # a code listed in two sectors keeps the first sector only (fixed rule)
                continue
            seen[c] = sec
    out = {"source": {"name": "O*NET 31.0 Database, Occupation Data (main occupation titles)", "url": SRC_URL,
                      "licence": "CC BY 4.0", "licence_record": LICENCE_URL, "sha256": sha, "rows": len(rows),
                      "fields_used": ["O*NET-SOC Code", "Title"]},
           "seed": SEED, "quota_per_sector": QUOTA,
           "rule": "explicit eligible code list per sector, fixed before the draw; each code in one sector; "
                   "'All Other' titles never eligible; seeded order; first QUOTA drawn, rest ordered spares",
           "sectors": [], "drawn": []}
    for code_, sec, codes in SECTORS:
        elig = [c for c in codes if seen.get(c) == sec and c in title and "All Other" not in title[c]]
        missing = [c for c in codes if c not in title]
        if missing:
            raise SystemExit(f"codes not in the O*NET file: {missing}")
        order = sorted(set(elig))
        rs = random.Random(int(hashlib.sha256(f"packs-2:{SEED}:{sec}".encode()).hexdigest(), 16))
        rs.shuffle(order)
        drawn, spares = order[:QUOTA], order[QUOTA:]
        if len(drawn) < QUOTA:
            raise SystemExit(f"{sec}: only {len(drawn)} eligible")
        out["sectors"].append({"sector": sec, "code": code_, "eligible": len(elig),
                               "major_groups": sorted({c[:2] for c in elig}),
                               "spares": [{"onet_code": c, "onet_title": title[c]} for c in spares]})
        for i, c in enumerate(drawn, 1):
            out["drawn"].append({"sector": sec, "slot": f"{code_}-{i:02d}", "onet_code": c, "onet_title": title[c],
                                 "major_group": c[:2]})
    (HERE / "persona_draw.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    groups = sorted({d["major_group"] for d in out["drawn"]})
    print(f"drawn {len(out['drawn'])} seeds over major groups {groups}; source sha256 {sha[:16]}")
    for d in out["drawn"]:
        print(d["slot"], d["onet_code"], d["onet_title"])


if __name__ == "__main__":
    sys.exit(main())
