#!/usr/bin/env python3
"""packs-4: draw O*NET persona seeds by program (C_DATA_SPEC v4 2.1 F4).

Titles only, from the O*NET 31.0 main occupation file (occupation_data.csv; never the alternate-titles or SOC
direct-match file). Fixed seed; spread over the O*NET major groups (round-robin over a seeded shuffle of the 23
groups, one title per visit, no title twice). "All Other" catch-all titles are skipped (they name no role).
The theme of pack i is THEMES[i % 5] (program-assigned, so no pack's theme is hand-picked against its seed).
Output: persona_draw.json (pack id, O*NET code, title, major group, theme). Descriptions are never read or stored.
"""
import csv, hashlib, json, random, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "tmp" / "raw" / "onet_occupation_data_31_0.csv"
N = int(sys.argv[1]) if len(sys.argv) > 1 else 84
SEED_STR = "packs-4:onet31:20261003"
THEMES = ["fictional_org", "invented_tech", "game_league", "space_colony", "fantasy_guild"]

def main():
    raw = RAW.read_bytes()
    rows = list(csv.DictReader(raw.decode("utf-8-sig").splitlines()))
    titles = [(r["O*NET-SOC Code"].strip(), r["Title"].strip()) for r in rows if "All Other" not in r["Title"]]
    seed = int(hashlib.sha256(SEED_STR.encode()).hexdigest()[:16], 16)
    rng = random.Random(seed)
    groups = {}
    for code, title in titles:
        groups.setdefault(code[:2], []).append((code, title))
    order = sorted(groups)
    rng.shuffle(order)
    for g in order:
        rng.shuffle(groups[g])
    out, i = [], 0
    while len(out) < N:
        g = order[i % len(order)]
        pos = i // len(order)
        if pos < len(groups[g]):
            code, title = groups[g][pos]
            k = len(out)
            out.append({"id": f"p4-{k + 1:03d}", "persona_seed": code, "onet_title": title,
                        "major_group": g, "theme": THEMES[k % len(THEMES)]})
        i += 1
    doc = {"id": "packs-4.persona_draw", "source": "O*NET 31.0 Database, occupation_data.csv (main titles only)",
           "source_url": "https://www.onetcenter.org/dl_files/database/db_31_0_csv/occupation_data.csv",
           "licence": "CC BY 4.0 (https://www.onetcenter.org/license_db.html); O*NET is a trademark of USDOL/ETA",
           "source_sha256": hashlib.sha256(raw).hexdigest(), "seed_string": SEED_STR, "n": N,
           "excluded": "titles containing 'All Other'", "draws": out}
    (HERE / "persona_draw.json").write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
    print(len(out), "draws;", len({d['major_group'] for d in out}), "major groups")

if __name__ == "__main__":
    main()
