#!/usr/bin/env python3
"""Non-sealed name check (clear text, nothing sealed is read): compares each candidate's name, publisher, host and upstream id
with (a) the 330 C1 source names (gblock/checks/c1_source_names.json), (b) the deny-list entries and their clear aliases
(data/c_parts/denylist.json; the OHS-3 part is hashed there and is not touched), (c) the G-block source list words.
Prints 'id CLEAR' or 'id OVERLAP <what matched>'. Run from lean/c2_build:  ../../.venv/bin/python -B meta_src/c1_denylist_check.py
Matching: an alias or C1 name hits when its compact token form (>= 5 chars) is a contiguous token span of an identifier field."""
import json, re
from pathlib import Path
HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[1]
tok = lambda t: re.findall(r"[a-z0-9]+", t.lower())
def span(needle, hay):
    n = len(needle)
    return n > 0 and any(hay[i:i + n] == needle for i in range(len(hay) - n + 1))
c1 = json.loads((HERE.parent / "gblock/checks/c1_source_names.json").read_text())["names"]
dl = json.loads((LEAN / "data/c_parts/denylist.json").read_text())["entries"]
terms = []
for n in c1:
    for part in re.split(r"[(),]", n):
        t = tok(part)
        if len("".join(t)) >= 5: terms.append(("c1", " ".join(t), t))
for e in dl:
    for a in [e.get("name") or ""] + [x.split(":", 1)[-1] for x in e.get("aliases", [])]:
        t = tok(a)
        if len("".join(t)) >= 5: terms.append(("deny:" + (e.get("name") or "")[:40], " ".join(t), t))
gblock = ["novascotia", "delaware", "montgomerycountymd", "wikibooks", "wikivoyage", "wikinews", "wikiversity", "libreoffice", "biorxiv", "artic", "socrata"]
for s in json.loads((HERE / "gproxy" / "SOURCES.json").read_text())["sources"]:
    fields = [s["name"], s["publisher"], s["host"], s["upstream_id"]] + s.get("other_hosts", [])
    hits = set()
    for f in fields:
        ft = tok(f)
        for kind, joined, t in terms:
            if span(t, ft) and joined not in ("data", "database"):
                hits.add(f"{kind}:{joined}")
        for g in gblock:
            if g in "".join(ft) and g != "socrata":
                hits.add("gblock:" + g)
    print(s["id"], "OVERLAP " + "; ".join(sorted(hits)) if hits else "CLEAR")
