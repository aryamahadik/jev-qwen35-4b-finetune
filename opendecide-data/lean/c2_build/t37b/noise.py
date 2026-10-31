"""t37b/noise.py: the replay-source noise screen of Ruling A45 (b). Drop only, never relabel, no bar loosened.

Three rules, all of them only remove (a template, a source or a base is left out; no gold is ever set or changed):
  1. A base needs a blind answer equal to its human gold. A missing / unreadable blind answer is a drop
     (builder.decide; select.eligible(allow_ids=...)).
  2. A wording template whose disagreement rate is above 3% is blocked (select.plan_block(blocked_templates=...)); a
     source whose disagreement rate is above 3% is dropped from T37b (select.eligible(deny_sources=...)).
     Disagreement = a blind read that does not equal the human gold (an abstention counts, as in g5h.score).
  3. Replay rows: a row is dropped from the replay when both blind reads disagree with the human gold, or when one
     disagrees and the other abstains (score_row). The drop list is a G13-style drop file ({"drop_ids": [...]}) that
     `mix_c2.py --decontam-drops` consumes (mixer.decontam_drop_ids drops the whole unit of each id).

Evidence for rule 2: the noise screen's reads of the whole replay pool of a source when they exist (load_screen);
before them, the pilot's own sample (pilot_evidence: the G5-H partner reads and the S13 blind base read of the same
100 units of pilot_i1_full). A source with a noise-screen rate always uses that rate (more reads supersede the sample).
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

BAR = 0.03                      # spec 6.3 G5-H template quarantine bar, applied here to sources too (A45 b)


def score_row(gold, reads: list) -> dict:
    """gold 0 / 1; reads: two normalised answers (1 / 0 / None for an abstention or invalid answer).
    status: clean (both equal gold) | drop (both disagree, or one disagrees and the other abstains) |
            split (one agrees, one disagrees) | abstain (no read disagrees, at least one abstains) | unread."""
    if len(reads) != 2 or any(r == "unread" for r in reads):
        return {"status": "unread", "drop": False, "clean": False}
    dis = [r is not None and r != gold for r in reads]
    ok = [r is not None and r == gold for r in reads]
    ab = [r is None for r in reads]
    drop = (all(dis)) or (any(dis) and any(ab))
    clean = all(ok)
    status = "clean" if clean else "drop" if drop else "split" if any(dis) else "abstain"
    return {"status": status, "drop": drop, "clean": clean}


def rate_table(counts: dict) -> dict:
    """{key: [n, bad]} -> {key: {"n", "bad", "rate"}}."""
    return {k: {"n": n, "bad": b, "rate": (b / n) if n else 0.0} for k, (n, b) in sorted(counts.items())}


def over_bar(table: dict, bar: float = BAR) -> list:
    """Keys whose disagreement rate is strictly above the bar (no minimum count: g5h.score quarantines the same way)."""
    return sorted(k for k, d in table.items() if d["n"] and d["rate"] > bar)


def pilot_evidence(pdir: Path) -> dict:
    """Disagreement counts from a pilot folder (pilot_i1_full): a unit is 'bad' when the G5-H reads of its partner row
    do not both equal the gold, or the S13 blind solver's BASE answer is missing or differs from the human base gold.
    Returns {"by_template": {key: [n, bad]}, "by_source": {...}, "bad_rows": [...], "units": n}."""
    pdir = Path(pdir)
    rows = {}
    for line in (pdir / "rows.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            rows[r["id"]] = r
    per = json.loads((pdir / "g5h" / "adjudication_key.json").read_text(encoding="utf-8"))["per_row"]
    s13 = {}
    p13 = pdir / "s13" / "s13_scored.json"
    if p13.is_file():
        for u in json.loads(p13.read_text(encoding="utf-8"))["units"].values():
            s13[u["row"]] = u
    tpl, src, bad_rows, bad_bases = {}, {}, [], []
    for rid, v in per.items():
        r = rows.get(rid)
        if r is None:
            continue
        t = r["meta"]["t37b"]
        bad = not all(v["agree_gold"])
        u = s13.get(rid)
        if u is not None:
            yb = u["blind"][0]
            bad = bad or yb is None or yb != u["base_gold"]
        for d, k in ((tpl, t["template"]), (src, t["base_source"])):
            c = d.setdefault(k, [0, 0])
            c[0] += 1
            c[1] += int(bad)
        if bad:
            bad_rows.append(rid)
            bad_bases.append(t["base_id"])
    return {"by_template": tpl, "by_source": src, "bad_rows": sorted(bad_rows), "bad_base_ids": sorted(bad_bases),
            "units": len(per)}


def screen_from_pilot(pdir: Path, bar: float = BAR) -> dict:
    ev = pilot_evidence(pdir)
    tt, st = rate_table(ev["by_template"]), rate_table(ev["by_source"])
    return {"bar": bar, "units": ev["units"], "templates": tt, "sources": st,
            "blocked_templates": over_bar(tt, bar), "sample_sources_over_bar": over_bar(st, bar),
            "bad_rows": ev["bad_rows"], "bad_base_ids": ev["bad_base_ids"]}


def load_screen(path: Path) -> dict:
    """The noise screen's scores file (noise_screen/score_reads.py): clean_ids, drop_ids, per-source counts."""
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    for k in ("clean_ids", "drop_ids", "sources"):
        if k not in d:
            raise ValueError(f"{path}: not a noise-screen scores file (missing {k})")
    return d


def sources_over_bar(screen_sources: dict, bar: float = BAR, stat: str = "not_clean") -> list:
    """Sources whose noise-screen rate is above the bar. stat "not_clean" (default, the g5h.score reading: a read that is
    not the human gold, abstentions included, over the rows both readers read) or "drop" (the replay drop rule: both
    reads dispute the gold, or one disputes and one abstains)."""
    if stat not in ("not_clean", "drop"):
        raise ValueError(stat)
    return sorted(s for s, d in screen_sources.items() if d["n_read"] and d[stat] / d["n_read"] > bar)


def combine_sources(screen: dict | None, bar: float = BAR, stat: str = "not_clean") -> list:
    """Sources dropped from T37b. Only the noise screen's reads of the replay pool measure a per-source rate. The
    pilot sample (1 to 13 units per source) cannot: at fewer than 34 units one disagreement is already above 3%, and
    dropping the five sources it names leaves 9 sources under the 10% source cap, so the plan collapses to 9 rows
    (measured, 15 Oct). Without a screen no source is dropped here; the templates and bases the sample flags are."""
    return sources_over_bar(screen["sources"], bar, stat) if screen else []
