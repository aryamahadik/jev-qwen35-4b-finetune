"""HybridQA: pick candidate train questions (one per table) and fetch only their tables + linked passages from
WikiTables-WithLinks at a pinned commit (the repo is ~800 MB; per-file fetch keeps raw small).

Train split only (released_data/train.traced.json). Pages are split 90/10 by normalized page title (spec 3.1):
bucket 0 -> mix-tuning dev candidates, buckets 1-9 -> training candidates.
"""
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import requests

from p2_common import RAW, TMP, log_progress, page_bucket, rng_for

WTWL_SHA = "dc066e1a6d5281511d8b73a6107d5ad2824cc2b2"
BASE = f"https://raw.githubusercontent.com/wenhuchen/WikiTables-WithLinks/{WTWL_SHA}"
OUTD = RAW / "wtwl"

BAD_Q = re.compile(r"\b(how many|how much|number of|not|n't|never|no longer|except|other than|besides|excluding|"
                   r"second|third|fourth|fifth|neither|nor|without|apart from|aside from|instead|total|average|"
                   r"combined|difference|sum|percent|percentage)\b", re.I)


def page_of(table_id):
    return re.sub(r"_\d+$", "", table_id).replace("_", " ")


def pick():
    data = json.load(open(RAW / "hybridqa_train.traced.json"))
    by_table = {}
    for q in data:
        nodes = q.get("answer-node") or []
        a = (q.get("answer-text") or "").strip()
        qs = q.get("question") or ""
        if len(nodes) != 1 or not a or a.lower() in ("yes", "no"):
            continue
        if not (5 <= len(qs.split()) <= 40) or not (1 <= len(a.split()) <= 8):
            continue
        if BAD_Q.search(qs):
            continue
        by_table.setdefault(q["table_id"], []).append(q)
    rng = rng_for("hq_pick")
    tables = sorted(by_table)
    rng.shuffle(tables)
    train_t = [t for t in tables if page_bucket(page_of(t)) != 0]
    dev_t = [t for t in tables if page_bucket(page_of(t)) == 0]
    # need ~ (1,000 rows + 50% reserve) x 1.45 over-fetch for drops, + dev
    want_train, want_dev = 2200, 160
    sel = train_t[:want_train] + dev_t[:want_dev]
    picks = {t: by_table[t] for t in sel}
    json.dump({"train_tables": train_t[:want_train], "dev_tables": dev_t[:want_dev],
               "n_tables_eligible": len(tables), "n_train_eligible": len(train_t), "n_dev_eligible": len(dev_t)},
              open(TMP / "hq_pick.json", "w"))
    return sel


def fetch_one(tid):
    out = {}
    for kind in ("tables_tok", "request_tok"):
        p = OUTD / kind / f"{tid}.json"
        if p.exists() and p.stat().st_size > 0:
            continue
        p.parent.mkdir(parents=True, exist_ok=True)
        url = f"{BASE}/{kind}/{requests.utils.quote(tid)}.json"
        for attempt in range(4):
            try:
                r = requests.get(url, timeout=30)
                if r.status_code == 200:
                    p.write_bytes(r.content)
                    break
                out[kind] = r.status_code
                if r.status_code == 404:
                    break
            except Exception as e:  # noqa: BLE001
                out[kind] = str(e)[:80]
            time.sleep(1 + attempt)
    return tid, out


def pick_more(n_more):
    """Additional train tables (same deterministic order, after the first pick) that have a question whose single
    answer node is a table cell (the hq_cell_ch framing)."""
    d = json.load(open(TMP / "hq_pick.json"))
    data = json.load(open(RAW / "hybridqa_train.traced.json"))
    cell_tables = set()
    for q in data:
        nodes = q.get("answer-node") or []
        if len(nodes) == 1 and nodes[0][3] == "table" and not BAD_Q.search(q.get("question") or ""):
            cell_tables.add(q["table_id"])
    by_table = {}
    for q in data:
        by_table.setdefault(q["table_id"], 1)
    rng = rng_for("hq_pick")
    tables = sorted(t for t in by_table)
    # same eligible universe and order as pick(): rebuild it
    elig = set()
    for q in data:
        nodes = q.get("answer-node") or []
        a = (q.get("answer-text") or "").strip()
        qs = q.get("question") or ""
        if len(nodes) != 1 or not a or a.lower() in ("yes", "no"):
            continue
        if not (5 <= len(qs.split()) <= 40) or not (1 <= len(a.split()) <= 8) or BAD_Q.search(qs):
            continue
        elig.add(q["table_id"])
    tables = sorted(elig)
    rng.shuffle(tables)
    train_t = [t for t in tables if page_bucket(page_of(t)) != 0]
    have = set(d["train_tables"])
    more = [t for t in train_t if t not in have and t in cell_tables][:n_more]
    d["train_tables_more"] = more
    json.dump(d, open(TMP / "hq_pick.json", "w"))
    return more


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--more":
        sel = pick_more(int(sys.argv[2]))
        fails = {}
        with ThreadPoolExecutor(16) as ex:
            for tid, err in ex.map(fetch_one, sel):
                if err:
                    fails[tid] = err
        log_progress(f"HybridQA fetch (more, cell-answer tables): {len(sel)} tables, {len(fails)} failures")
        print(len(sel), "more tables;", len(fails), "failures")
        return 0
    sel = pick()
    print("tables to fetch", len(sel), flush=True)
    fails = {}
    t0 = time.time()
    with ThreadPoolExecutor(16) as ex:
        for i, (tid, err) in enumerate(ex.map(fetch_one, sel)):
            if err:
                fails[tid] = err
            if (i + 1) % 200 == 0:
                print(i + 1, "fetched", len(fails), "fails", round(time.time() - t0), "s", flush=True)
    json.dump(fails, open(TMP / "hq_fetch_fails.json", "w"))
    log_progress(f"HybridQA fetch: {len(sel)} tables (+passages) from WikiTables-WithLinks@{WTWL_SHA[:12]}, "
                 f"{len(fails)} failures, {round(time.time() - t0)} s")


if __name__ == "__main__":
    sys.exit(main())
