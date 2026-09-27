"""OHS-3 part: openfda_recall_class (natural yes/no: is this FDA recall Class I?).

Source: openFDA enforcement reports for food, drug and device, report_date 2026-06-01..2026-09-26, CC0.
Input is ONLY the frozen raw snapshot in ohs3/cache/openfda_recall_class/ (made once by
ohs3/fetch_openfda_snapshot.py; pages saved verbatim, sha256 in manifest.json). Re-runs give identical rows.

Rules (from the task spec and ohs3/selection_criteria.md):
- One product row per recall event (dedupe by event_id). An event whose products carry different
  classifications offers one candidate per class it has; each event is used at most once. Scarce classes are
  drawn first (Class I, then Class III, then Class II), so a mixed event is never used twice.
- "Not Yet Classified" rows are dropped.
- Gold 1 = Class I, gold 0 = Class II or Class III. 72 / 72, with the 0 side split 36 / 36 between II and III
  where the pool allows, and the sample spread as evenly as possible over food / drug / device
  (48 each target; shortfalls are water-filled to the other types).
- State = product_type + product_description + reason_for_recall, the source's own text. Only whitespace is
  normalised. Every other field (classification, codes, firm, dates, status ...) is left out.
- Any "Class I/II/III" or "Class 1/2/3" string in the text is replaced by "Class [REDACTED]" and listed in meta.
- Card: the official FDA definition of Class I (21 CFR 7.3(m)(1)).
- Track: F only when report_date AND recall_initiation_date are on/after 2026-06-01 (earlier-initiated recalls
  may have public firm notices before the cutoff), else U.
- Seed 20261026.
"""
import collections
import hashlib
import json
import random
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parent
CACHE = HERE / "cache" / "openfda_recall_class"
OUT = LEAN / "data" / "ohs3_parts" / "openfda_recall_class.jsonl"
SUMMARY = LEAN / "data" / "ohs3_parts" / "openfda_recall_class_summary.json"

TASK = "openfda_recall_class"
SEED = 20261026
N_POS, N_NEG = 72, 72
TYPES = ["food", "drug", "device"]
MIN_CH, MAX_CH = 20, 6000
TRACK_CUTOFF = "20260601"

INSTRUCTIONS = "Is this FDA recall classified as Class I?"
ASKED_LABEL = "Class I"
CLASS_I_DEF = ("A situation in which there is a reasonable probability that the use of, or exposure to, "
               "a violative product will cause serious adverse health consequences or death.")
CARD = f"- {ASKED_LABEL}: {CLASS_I_DEF}"
LABEL_SOURCE = ("Official: 21 CFR 7.3(m)(1) (eCFR, https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/"
                "part-7/subpart-A/section-7.3); same wording on fda.gov 'Recalls Background and Definitions' "
                "(https://www.fda.gov/safety/industry-guidance-recalls/recalls-background-and-definitions)")
LICENCE = "CC0 1.0 (openFDA data, https://open.fda.gov/license/)"

CLASS_RE = re.compile(r"(?i)\bclass\s*(?:III|II|I|3|2|1)\b(?![\w-])")
sha = lambda s: hashlib.sha256(s.encode()).hexdigest()


def norm_ws(s):
    s = (s or "").replace("\r", "")
    s = re.sub(r"[ \t ]+", " ", s)
    s = re.sub(r" *\n *", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def redact(text, field, log):
    def sub(m):
        log.append({"field": field, "original": m.group(0)})
        return "Class [REDACTED]"
    return CLASS_RE.sub(sub, text)


def make_state(r):
    log = []
    desc = redact(norm_ws(r["product_description"]), "product_description", log)
    reason = redact(norm_ws(r["reason_for_recall"]), "reason_for_recall", log)
    state = (f"Product type: {norm_ws(r['product_type'])}\n\n"
             f"Product description:\n{desc}\n\n"
             f"Reason for recall:\n{reason}")
    return state, log


def waterfill(n, caps, order):
    """Split n as evenly as possible over keys with caps; remainders go to keys in `order`."""
    alloc = {k: 0 for k in caps}
    left = n
    while left > 0:
        open_keys = [k for k in order if alloc[k] < caps[k]]
        if not open_keys:
            break
        share = max(1, left // len(open_keys))
        for k in open_keys:
            if left == 0:
                break
            give = min(share, caps[k] - alloc[k], left)
            alloc[k] += give
            left -= give
    return alloc


def load_snapshot():
    manifest = json.loads((CACHE / "manifest.json").read_text())
    rows = {t: [] for t in TYPES}
    for p in manifest["pages"]:
        body = (CACHE / p["file"]).read_bytes()
        assert hashlib.sha256(body).hexdigest() == p["sha256"], f"snapshot changed: {p['file']}"
        t = p["file"].split("_skip")[0]
        rows[t].extend(json.loads(body)["results"])
    for t in TYPES:
        tot = {p["total"] for p in manifest["pages"] if p["file"].startswith(t + "_")}
        assert len(tot) == 1 and len(rows[t]) == tot.pop(), f"incomplete snapshot for {t}"
    return manifest, rows


def main():
    manifest, raw = load_snapshot()
    rng = random.Random(SEED)
    type_order = TYPES[:]
    rng.shuffle(type_order)  # seeded order for remainders

    stats = {"raw_product_rows": {t: len(raw[t]) for t in TYPES}}
    # candidates[(type, cls)] = list of dicts, one per event
    cands = collections.defaultdict(list)
    n_events, mixed_events, dropped = {}, {}, collections.Counter()
    seen_states = {}
    for t in TYPES:
        by_ev = collections.defaultdict(list)
        for r in raw[t]:
            if not (TRACK_CUTOFF <= r["report_date"] <= "20260926"):
                dropped["report_date_out_of_range"] += 1
                continue
            if r["classification"] not in ("Class I", "Class II", "Class III"):
                dropped[f"classification={r['classification']}"] += 1
                continue
            by_ev[r["event_id"]].append(r)
        n_events[t] = len(by_ev)
        mixed_events[t] = sum(1 for v in by_ev.values() if len({x["classification"] for x in v}) > 1)
        for ev in sorted(by_ev, key=int):
            by_cls = collections.defaultdict(list)
            for r in by_ev[ev]:
                by_cls[r["classification"]].append(r)
            for cls in sorted(by_cls):
                pool = sorted(by_cls[cls], key=lambda x: x["recall_number"])
                # representative product row: seeded per event, independent of iteration order
                ok = []
                for r in pool:
                    st, log = make_state(r)
                    if MIN_CH <= len(st) <= MAX_CH:
                        ok.append((r, st, log))
                    else:
                        dropped["state_length"] += 1
                if not ok:
                    continue
                r, st, log = random.Random(f"{SEED}|{t}|{ev}|{cls}").choice(ok)
                key = re.sub(r"\s+", " ", st).strip().lower()
                if key in seen_states and seen_states[key] != ev:
                    dropped["duplicate_state_other_event"] += 1
                    continue
                seen_states[key] = ev
                cands[(t, cls)].append({"type": t, "cls": cls, "event_id": ev, "row": r, "state": st,
                                        "redactions": log, "mixed": len(by_cls) > 1})
    avail = {f"{t}|{c}": len(cands[(t, c)]) for t in TYPES for c in ("Class I", "Class II", "Class III")}
    stats.update({"events_after_filters": n_events, "events_with_mixed_classification": mixed_events,
                  "dropped": dict(dropped), "available_events_by_type_class": avail})

    # ---- allocation
    per_type_target = (N_POS + N_NEG) // len(TYPES)
    pos = waterfill(N_POS, {t: len(cands[(t, "Class I")]) for t in TYPES}, type_order)
    neg_caps = {t: len(cands[(t, "Class II")]) + len(cands[(t, "Class III")]) for t in TYPES}
    neg_pref = {t: min(neg_caps[t], max(0, per_type_target - pos[t])) for t in TYPES}
    neg = waterfill(N_NEG, neg_pref, type_order)
    if sum(neg.values()) < N_NEG:  # top up beyond the even target where needed
        extra = waterfill(N_NEG - sum(neg.values()), {t: neg_caps[t] - neg[t] for t in TYPES}, type_order)
        neg = {t: neg[t] + extra[t] for t in TYPES}
    n3_target = N_NEG // 2
    c3 = waterfill(n3_target, {t: min(len(cands[(t, "Class III")]), neg[t]) for t in TYPES}, type_order)
    c2 = {t: neg[t] - c3[t] for t in TYPES}
    for t in TYPES:
        assert c2[t] <= len(cands[(t, "Class II")]), f"not enough Class II for {t}"
    alloc = {"Class I": pos, "Class III": c3, "Class II": c2}
    stats["allocation"] = alloc

    # ---- sampling (scarce classes first; an event is used once)
    used_events = set()
    chosen = []
    for cls in ("Class I", "Class III", "Class II"):
        for t in TYPES:
            pool = [c for c in cands[(t, cls)] if (t, c["event_id"]) not in used_events]
            k = alloc[cls][t]
            assert len(pool) >= k, f"pool too small for {t} {cls}: {len(pool)} < {k}"
            pick = random.Random(f"{SEED}|sample|{t}|{cls}").sample(pool, k)
            for c in pick:
                used_events.add((t, c["event_id"]))
            chosen.extend(pick)

    rows = []
    for c in chosen:
        r = c["row"]
        gold = 1 if c["cls"] == "Class I" else 0
        rn = r["recall_number"]
        rows.append({
            "id": "r_" + sha(f"ohs3|{TASK}|{rn}")[:12],
            "group_id": f"g:ohs3:{TASK}:{c['type']}:{c['event_id']}",
            "call_id": "c_" + sha(c["state"])[:12],
            "split": "ohs3",
            # F only if the recall itself became public on/after the cutoff: the enforcement report is dated
            # report_date, but firm press releases / notices with the same product text can predate it and
            # appear from recall_initiation_date. Conservative: both dates must be >= cutoff.
            "track": "F" if (r["report_date"] >= TRACK_CUTOFF
                             and (r.get("recall_initiation_date") or "") >= TRACK_CUTOFF) else "U",
            "source": TASK,
            "state": c["state"],
            "qtype": "noul",
            "instructions": INSTRUCTIONS,
            "options": None,
            "gold": gold,
            "role": "aff",
            "card": CARD,
            "meta": {
                "task": TASK,
                "dataset": f"openFDA {c['type']} enforcement reports (api.fda.gov/{c['type']}/enforcement.json)",
                "url": f"https://api.fda.gov/{c['type']}/enforcement.json?search=recall_number:%22{rn}%22",
                "recall_number": rn,
                "event_id": c["event_id"],
                "report_date": r["report_date"],
                "recall_initiation_date": r.get("recall_initiation_date"),
                "classification": c["cls"],
                "product_type": r["product_type"],
                "endpoint": c["type"],
                "label_name": ASKED_LABEL,
                "event_has_mixed_classification": c["mixed"],
                "redactions": c["redactions"],
                "snapshot_fetched_utc": manifest["fetched_utc"],
                "openfda_last_updated": manifest["pages"][0]["last_updated"],
                "licence": LICENCE,
            },
        })

    # ---- validation
    assert len(rows) == N_POS + N_NEG, len(rows)
    assert len({r["id"] for r in rows}) == len(rows), "duplicate ids"
    assert len({r["group_id"] for r in rows}) == len(rows), "duplicate group ids"
    assert len({r["call_id"] for r in rows}) == len(rows), "duplicate states"
    assert sum(r["gold"] for r in rows) == N_POS
    for r in rows:
        assert MIN_CH <= len(r["state"]) <= MAX_CH
        assert not CLASS_RE.search(r["state"]), r["id"]
        assert set(r) == {"id", "group_id", "call_id", "split", "track", "source", "state", "qtype",
                          "instructions", "options", "gold", "role", "card", "meta"}
    rows.sort(key=lambda r: r["id"])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    body = "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows)
    OUT.write_text(body)

    cls_counts = collections.Counter(r["meta"]["classification"] for r in rows)
    type_counts = collections.Counter(r["meta"]["endpoint"] for r in rows)
    type_cls = collections.Counter(f"{r['meta']['endpoint']}|{r['meta']['classification']}" for r in rows)
    dates = sorted(r["meta"]["report_date"] for r in rows)
    lens = sorted(len(r["state"]) for r in rows)
    summary = {
        "task": TASK, "split": "ohs3", "qtype": "noul", "rows": len(rows), "seed": SEED,
        "gold_balance": {"1 (Class I)": sum(r["gold"] for r in rows),
                         "0 (Class II or III)": sum(1 - r["gold"] for r in rows)},
        "classification_counts": dict(sorted(cls_counts.items())),
        "product_type_counts": dict(sorted(type_counts.items())),
        "product_type_x_class": dict(sorted(type_cls.items())),
        "track": dict(collections.Counter(r["track"] for r in rows)),
        "report_date_range_sample": [dates[0], dates[-1]],
        "query_date_range": ["20260601", "20260926"],
        "state_chars": {"min": lens[0], "median": lens[len(lens) // 2], "max": lens[-1]},
        "instructions": INSTRUCTIONS,
        "card": CARD,
        "label_definition_source": LABEL_SOURCE,
        "author_written_definitions": [],
        "licence": LICENCE,
        "provenance": {
            "snapshot_dir": str(CACHE.relative_to(LEAN)),
            "snapshot_fetched_utc": manifest["fetched_utc"],
            "openfda_meta_last_updated": manifest["pages"][0]["last_updated"],
            "pages": manifest["pages"],
            "recall_numbers": sorted(r["meta"]["recall_number"] for r in rows),
        },
        "state_fields": ["product_type", "product_description", "reason_for_recall"],
        "redactions": [{"id": r["id"], "recall_number": r["meta"]["recall_number"], "redactions": r["meta"]["redactions"]}
                       for r in rows if r["meta"]["redactions"]],
        "build_stats": stats,
        "output_sha256": sha(body),
    }
    SUMMARY.write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    print(json.dumps({k: v for k, v in summary.items() if k != "provenance"}, indent=1))


if __name__ == "__main__":
    main()
