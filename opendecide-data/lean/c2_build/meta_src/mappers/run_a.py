"""run_a.py <source>: build rows for one group-A metadata source (CPU only). Writes lean/data/c2_md_parts/<source>/."""
import importlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common_a as C  # noqa: E402

LEAN = Path(__file__).resolve().parents[3]
URLS = {"openalex": ("https://help.openalex.org/hc/en-us/articles/24397762024087-Pricing", "https://api.openalex.org/works"),
        "musicbrainz": ("https://musicbrainz.org/doc/About/Data_License", "https://musicbrainz.org/ws/2/release-group"),
        "worldbank": ("https://datacatalog.worldbank.org/public-licenses", "https://search.worldbank.org/api/v2/projects"),
        "usgs": ("https://www.usgs.gov/information-policies-and-instructions/copyrights-and-credits", "https://earthquake.usgs.gov/fdsnws/event/1/query")}


def main(name):
    m = importlib.import_module(name)
    tasks = m.tasks()
    probs = C.check_wordings(tasks)
    if probs:
        for p in probs[:30]:
            print("WORDING PROBLEM", p)
        print(len(probs), "wording problems")
        sys.exit(1)
    recs = m.load()
    rows, rels, rep = C.build_source("md_" + m.NAME, licence_url=URLS[m.NAME][0], dataset_url=URLS[m.NAME][1], domain=m.DOMAIN, licence=m.LICENCE, headers=m.HEADERS, recs=recs, rid_of=m.rid_of,
                                     fields_of=m.fields_of, group_of=m.group_of, tasks=tasks, seed_tag="A1", per_task=getattr(m, "PER_TASK", (10, 15)), ch_range=getattr(m, "CH_RANGE", (22, 30)))
    man = C.write_source(m.NAME, LEAN / "data" / "c2_md_parts" / m.NAME, rows, rels, tasks, rep,
                         {"domain": m.DOMAIN, "licence": m.LICENCE, "n_tasks_defined": len(tasks), "snapshot_records": len(recs),
                          "snapshot_note": "polite API snapshot taken 15 Oct 2026 (meta_src/raw_a); names of people dropped at fetch"})
    print(json.dumps(man["audit"], indent=1))


main(sys.argv[1])
