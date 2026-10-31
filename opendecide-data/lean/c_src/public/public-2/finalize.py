"""public-2 finalize: dedup, length, stratified selection, meta, pools, sidecars, QC report, manifest.

Inputs: tmp/cand_{wikisql,drop,uci,hybridqa}.jsonl (this builder's candidates), tmp/gt_index.npz, the raw train
files (for canonical table text), and an optional drop list (tmp/sealed_drop_ids.json: ids the sealed checker hit).
Outputs (out/): rows_r1.jsonl, reserve_r1.jsonl, dev_mt_r1.jsonl, wordings.jsonl, cards.jsonl, styles.jsonl,
table_hashes.jsonl, qc_report.json, manifest.json.

v1.1 (review public-2 fixes):
- Choice rows: decoder_io (cygnet, schema_branch_mark; A16 908c08d7) shows a choice row's card only as
  '- {option}: {definition}' lines glued to the options. route_choice_card keeps exactly those lines in `card` and moves
  every other card line (rules, model tables, notes, worked examples) into `instructions`, ahead of the wording.
- golden_train dedup also runs on the rendered state (lines/sentences >= 8 words over all sources, 10-grams over the
  spec 3.1 named sources), on top of the canonical-record check.
- Length: real chat render (decoder_io.render_chat, CYGNET_SYSTEM, user_msg under cygnet + schema_branch_mark, Qwen3.5
  tokenizer) < 2,000 tokens, so every public-2 row is a non-long row.
- G10 balance on choice rows uses every displayed option (abstain options included, ties split): longest-is-gold within
  1 pp of mean 1/k per framing; abstain options wrong on 50-60% of the rows that show them. Selection = round robin
  over (gold-rank bucket, wording), then minimal same-key swaps with the leftover pool (repair).
- Meta: spec 2.4 keys (domain_pack, sampler, structure_hash, depth, deep) plus block, c_part, share_alike, card_route,
  as in public-1 and public-3; family "public".
"""
from __future__ import annotations

import hashlib
import json
import math
import statistics
from collections import Counter, defaultdict

from p2_common import (GEN_VERSION, HERE, LEAN, LOGS, OUT, RAW, SEED, TMP, DedupIndex, h64, log_progress, norm,
                       rng_for, sha256_file, text_units, write_jsonl)

TARGETS = {
    "c_pub_hybridqa": {"hq_cell_ch": 550, "hq_row_yn": 450},
    "c_pub_wikisql": {"ws_lookup_ch": 350, "ws_agg_ch": 225, "ws_count_yn": 275, "ws_agg_yn": 300},
    "c_pub_drop": {"drop_thr_yn": 140, "drop_ch": 110},
    "c_pub_uci_car": {"uci_ch": 100, "uci_yn": 100},
    "c_pub_uci_nursery": {"uci_ch": 150, "uci_yn": 150},
}
DEV_TARGETS = {
    "c_pub_hybridqa": {"hq_cell_ch": 18, "hq_row_yn": 17},
    "c_pub_wikisql": {"ws_lookup_ch": 20, "ws_agg_ch": 15, "ws_count_yn": 20, "ws_agg_yn": 20},
    "c_pub_drop": {"drop_thr_yn": 15, "drop_ch": 15},
    "c_pub_uci_car": {"uci_ch": 15, "uci_yn": 15},
    "c_pub_uci_nursery": {"uci_ch": 15, "uci_yn": 15},
}
UCI_CH_GOLD = {"c_pub_uci_car": {"unacceptable": 25, "acceptable": 25, "good": 25, "very good": 25},
               "c_pub_uci_nursery": {"not recommended": 45, "very recommended": 30, "priority": 45,
                                     "special priority": 30}}
RESERVE_FRAC = 0.5
ABSTAIN = ("None of these", "None of the listed values")
MAX_TOKENS = 1999  # real chat-render tokens (decoder_io cygnet + schema_branch_mark): every row is a non-long row
GL_TOL = 0.01      # |share of rows whose gold is the longest option - mean 1/k| <= 1 pp per framing (G10: 2 pp)
AB_HI = 0.50       # abstain-gold share of the rows that show an abstain option: <= 50% (G10: abstain wrong >= 50%)
AB_LO = 0.40       # ... and >= 40%, so abstain-as-gold rows stay (C1 weakness, spec 1)
DECODER_IO_SHA256 = "908c08d752ce8896"  # A16 readout (prefix)
BLOCK = {"c_pub_hybridqa": "3C", "c_pub_wikisql": "3C", "c_pub_drop": "3C", "c_pub_uci_car": "3D",
         "c_pub_uci_nursery": "3D"}
SHARE_ALIKE = {"c_pub_hybridqa": True, "c_pub_wikisql": True, "c_pub_drop": True, "c_pub_uci_car": False,
               "c_pub_uci_nursery": False}
# framing-level step count of the program label (constant per framing, so it carries no label signal)
DEPTH = {"hq_cell_ch": 2, "hq_row_yn": 2, "ws_lookup_ch": 1, "ws_agg_ch": 2, "ws_count_yn": 3, "ws_agg_yn": 3,
         "drop_ch": 2, "drop_thr_yn": 3, "uci_ch": 3, "uci_yn": 4}

RAW_SHA = {}
for line in open(LOGS / "raw_sha256.txt"):
    h, p = line.split(None, 1)
    RAW_SHA[p.strip().split("/")[-1]] = h

DATASETS = {
    "c_pub_hybridqa": {
        "spec_id": "C_DATA_SPEC v4 3.2 #7", "domain": "hybridqa", "name": "HybridQA",
        "licence": ("MIT, annotations (https://github.com/wenhuchen/HybridQA/blob/"
                    "db22fda8c5951438fade3c69d75b350335ba93b3/LICENSE, sha256 "
                    f"{RAW_SHA.get('hybridqa_LICENSE.txt', '')[:16]}); train file released_data/train.traced.json "
                    f"sha256 {RAW_SHA.get('hybridqa_train.traced.json', '')[:16]}; tables and passages from "
                    "wenhuchen/WikiTables-WithLinks@dc066e1a6d52 (no LICENSE: Wikipedia text, CC BY-SA; SA: private "
                    "training only, notices file)"),
        "parents": ["WikiTables-WithLinks", "Wikipedia"],
    },
    "c_pub_wikisql": {
        "spec_id": "C_DATA_SPEC v4 3.2 #8", "domain": "wikisql", "name": "WikiSQL",
        "licence": ("BSD-3-Clause (https://github.com/salesforce/WikiSQL/blob/"
                    "cffb423077756d04c1bac5bcd45167c86903fbcb/LICENSE, sha256 "
                    f"{RAW_SHA.get('wikisql_LICENSE.txt', '')[:16]}; data.tar.bz2 in the repo, sha256 "
                    f"{RAW_SHA.get('wikisql_data.tar.bz2', '')[:16]}, train members only); Wikipedia tables CC BY-SA "
                    "(SA: private training only, notices file)"),
        "parents": ["WikiTables corpus", "Wikipedia"],
    },
    "c_pub_drop": {
        "spec_id": "C_DATA_SPEC v4 3.2 #11", "domain": "drop", "name": "DROP",
        "licence": ("CC BY-SA 4.0 (drop_dataset/license.txt inside the official AI2 zip "
                    "https://ai2-public-datasets.s3.amazonaws.com/drop/drop_dataset.zip, zip sha256 "
                    f"{RAW_SHA.get('drop_dataset.zip', '')[:16]}, license.txt sha256 "
                    f"{RAW_SHA.get('license.txt', '')[:16]}; train member only); Wikipedia passages; SA: private "
                    "training only, notices file"),
        "parents": ["Wikipedia"],
    },
    "c_pub_uci_car": {
        "spec_id": "C_DATA_SPEC v4 3.2 #12", "domain": "uci_car", "name": "UCI Car Evaluation",
        "licence": ("CC BY 4.0 (https://archive.ics.uci.edu/dataset/19/car+evaluation, DOI 10.24432/C5JP48; "
                    f"car+evaluation.zip sha256 {RAW_SHA.get('uci_car.zip', '')[:16]}); DEX model by Marko Bohanec "
                    "(credit in the notices file); labels = the published model's classes"),
        "parents": ["DEX hierarchical decision models (Bohanec, Rajkovic)"],
    },
    "c_pub_uci_nursery": {
        "spec_id": "C_DATA_SPEC v4 3.2 #12", "domain": "uci_nursery", "name": "UCI Nursery",
        "licence": ("CC BY 4.0 (https://archive.ics.uci.edu/dataset/76/nursery, DOI 10.24432/C5P88W; "
                    f"nursery.zip sha256 {RAW_SHA.get('uci_nursery.zip', '')[:16]}); DEX model by Vladislav "
                    "Rajkovic et al. with M. Olave and M. Bohanec (credit in the notices file); labels = the "
                    "published model's classes"),
        "parents": ["DEX hierarchical decision models (Bohanec, Rajkovic)"],
    },
}


def load_cands():
    rows = []
    for name in ("cand_hybridqa", "cand_wikisql", "cand_drop", "cand_uci"):
        with open(TMP / f"{name}.jsonl") as f:
            rows += [json.loads(l) for l in f]
    return rows


# ------------------------------------------------------------------ canonical record text (dedup, table hashes)

def wikisql_tables(ids):
    out = {}
    with open(RAW / "data" / "train.tables.jsonl") as f:
        for line in f:
            t = json.loads(line)
            if t["id"] in ids:
                out[t["id"]] = t
    return out


def canonical_text(r, ws_tabs):
    x = r["_x"]
    if r["source"] == "c_pub_wikisql":
        t = ws_tabs[x["table_id"]]
        return "\n".join([" | ".join(map(str, t["header"]))] + [" | ".join(map(str, row)) for row in t["rows"]])
    return x.get("record_text") or r["state"]


def table_hash(header, rows, title):
    cells = sorted({norm(str(c)) for row in rows for c in row})
    return {"title_header": hashlib.sha256((norm(title or "") + "||" + "|".join(norm(str(h)) for h in header)).encode()).hexdigest(),
            "cellset": hashlib.sha256("␟".join(cells).encode()).hexdigest(),
            "full": hashlib.sha256((norm(title or "") + "||" + "|".join(norm(str(h)) for h in header) + "||" + "␟".join(cells)).encode()).hexdigest()}


# ------------------------------------------------------------------ tokens

def hq_table_hash(tid):
    """HybridQA table hash from the pinned WikiTables-WithLinks file: the local raw copy if present, else the cache
    written from v1's table_hashes.jsonl (same pinned files), else a fresh fetch at the pinned commit."""
    from p2_common import detok
    p = RAW / "wtwl" / "tables_tok" / f"{tid}.json"
    cache_p = TMP / "hq_table_hash_cache.json"
    if not p.exists():
        cache = json.load(open(cache_p)) if cache_p.exists() else {}
        if tid in cache:
            return cache[tid]
        import requests
        from hq_fetch import BASE
        resp = requests.get(f"{BASE}/tables_tok/{tid}.json", timeout=60)
        resp.raise_for_status()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(resp.content)
    tj = json.load(open(p))
    return table_hash([detok(h[0]) for h in tj["header"]], [[detok(c[0]) for c in row] for row in tj["data"]],
                      detok(tj.get("title") or ""))


def tokenizer():
    from transformers import AutoTokenizer
    return AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", local_files_only=True)


def decoder_io_pinned():
    """lean/decoder_io.py (A16 readout 908c08d7), run as a program in the served prompt: cygnet + schema_branch_mark."""
    import sys
    p = LEAN / "decoder_io.py"
    got = sha256_file(p)
    if not got.startswith(DECODER_IO_SHA256):
        raise SystemExit(f"decoder_io.py sha256 {got[:16]} is not the A16 readout {DECODER_IO_SHA256}")
    if str(LEAN) not in sys.path:
        sys.path.insert(0, str(LEAN))
    import decoder_io as dio
    dio.STYLE, dio.LAYOUT = "cygnet", "schema_branch_mark"
    return dio


def real_tokens(tok, dio, r):
    """Prompt tokens of the real chat render (system + user turn, generation prompt, thinking off)."""
    row = {k: r[k] for k in ("qtype", "state", "instructions", "options", "gold", "card")}
    text = dio.render_chat(tok, dio.CYGNET_SYSTEM, dio.user_msg(row))
    return len(tok(text, add_special_tokens=False)["input_ids"])


def is_def_line(line, options):
    """A '- {option}: {definition}' card line that decoder_io.card_defs prints on the option line of a choice row."""
    return line.startswith("- ") and ": " in line and line[2:].split(": ", 1)[0] in options


def route_choice_card(r):
    """Choice rows: keep only '- {option}: {definition}' lines in the card; every other card line moves, in order, into
    instructions ahead of the wording (decoder_io prints instructions in the schema and again after the text).
    Yes/no rows are untouched (decoder_io prints their card whole under 'Definitions:')."""
    x = r["_x"]
    if r["qtype"] != "choice" or not r.get("card"):
        x["card_route"] = "card" if r.get("card") else None
        return r
    keep, move = [], []
    for ln in r["card"].split("\n"):
        (keep if is_def_line(ln, r["options"]) else move).append(ln)
    moved = "\n".join(move).strip("\n")
    x["card_text_v1"] = r["card"]
    x["moved_card"] = moved or None
    if moved:
        r["instructions"] = moved + "\n\n" + r["instructions"]
    r["card"] = "\n".join(keep) or None
    x["card_route"] = ("instructions+option_lines" if keep else "instructions") if moved else "option_lines"
    return r


# ------------------------------------------------------------------ selection

def gold_longest(r):
    """'Longest option is gold' credit over EVERY displayed option (abstain options included; v1.1): 1/m when the gold
    is one of the m longest options (by characters), else 0. Its mean is compared with mean 1/k (G10)."""
    if r["qtype"] != "choice":
        return 0.0
    L = [len(o) for o in r["options"]]
    return 1.0 / L.count(max(L)) if len(r["gold"]) == max(L) else 0.0


def gold_longest_ex_abstain(r):
    """v1 measure, kept for the report only: abstain options and abstain-gold rows left out."""
    if r["qtype"] != "choice" or r["gold"] in ABSTAIN:
        return 0.0
    opts = [o for o in r["options"] if o not in ABSTAIN]
    L = [len(o) for o in opts]
    g = opts.index(r["gold"])
    return 1.0 / L.count(max(L)) if L[g] == max(L) else 0.0


def k_eff(r):
    return len(r["options"])


def shows_abstain(r):
    return r["qtype"] == "choice" and any(o in ABSTAIN for o in r["options"])


def bal_stats(rows):
    S = sum(gold_longest(r) for r in rows)
    E = sum(1 / k_eff(r) for r in rows)
    ab = sum(1 for r in rows if shows_abstain(r))
    abg = sum(1 for r in rows if shows_abstain(r) and r["gold"] in ABSTAIN)
    return [S, E, len(rows), ab, abg]


def bal_cost(st, ab_lo=AB_LO):
    """Rows by which a choice set misses the G10 targets (0 = balanced)."""
    S, E, n, ab, abg = st
    c = max(0.0, abs(S - E) - GL_TOL * n)
    if ab:
        c += max(0.0, abg - AB_HI * ab) + max(0.0, ab_lo * ab - abg)
    return c


def trim(chosen, ab_lo=0.0):
    """Reserve only: when no swap is left (the leftover pool is empty), drop the row whose removal lowers the G10 cost
    most until the reserve meets the targets; dropped rows are simply not kept. Deterministic."""
    chosen = list(chosen)
    dropped = 0
    st = bal_stats(chosen)
    while chosen and bal_cost(st, ab_lo) > 1e-9:
        cur = bal_cost(st, ab_lo)
        best, arg = cur - 1e-9, None
        for i, c in enumerate(chosen):
            ac = shows_abstain(c)
            nst = [st[0] - gold_longest(c), st[1] - 1 / k_eff(c), st[2] - 1, st[3] - ac,
                   st[4] - (ac and c["gold"] in ABSTAIN)]
            v = bal_cost(nst, ab_lo)
            if v < best:
                best, arg = v, i
        if arg is None:
            break
        chosen.pop(arg)
        st = bal_stats(chosen)
        dropped += 1
    return chosen, dropped


def gold_position_repair(rows, seed_tag):
    """G10 'gold letter uniform per option bucket' on the stored option order (the trainer re-permutes options; this
    only keeps the stored order free of a position signal). Per option-count bucket with >= 2k rows, while the
    chi-square p < 0.2: move the gold of one row from the most over-used position to the least used allowed position
    by swapping it with the option there; buckets are per dataset x framing x option count. Abstain options never move
    (they stay last); rows whose numeric options are
    sorted are never touched (a swap would mark the gold). Deterministic; returns the number of rows changed."""
    from scipy.stats import chisquare

    def sorted_numeric(o):
        try:
            v = [float(x.replace(",", "")) for x in o if x not in ABSTAIN]
        except ValueError:
            return False
        return v == sorted(v) or v == sorted(v, reverse=True)
    changed = set()
    by = defaultdict(list)
    for r in rows:
        if r["qtype"] == "choice":
            by[(r["source"], r["meta"]["framing"], len(r["options"]))].append(r)
    for (_, _, k), g in sorted(by.items()):
        if len(g) < 2 * k:
            continue
        g = sorted(g, key=lambda r: hashlib.sha256(f"{seed_tag}:{r['id']}".encode()).hexdigest())
        for _ in range(len(g)):
            cnt = [0] * k
            for r in g:
                cnt[r["options"].index(r["gold"])] += 1
            if float(chisquare(cnt).pvalue) >= 0.2:
                break
            moved = False
            for hi in sorted(range(k), key=lambda i: -cnt[i]):
                for r in g:
                    o = r["options"]
                    if o.index(r["gold"]) != hi or r["gold"] in ABSTAIN or sorted_numeric(o):
                        continue
                    free = [i for i in range(k) if o[i] not in ABSTAIN and cnt[i] < cnt[hi] - 1]
                    if not free:
                        continue
                    lo = min(free, key=lambda i: (cnt[i], i))
                    o[hi], o[lo] = o[lo], o[hi]
                    changed.add(r["id"])
                    moved = True
                    break
                if moved:
                    break
            if not moved:
                break
    return len(changed)


def repair(chosen, rest, keyfs, ab_lo=AB_LO):
    """Minimal swaps: while the chosen set misses the G10 targets, make the single swap (chosen row out, leftover row in,
    same key) that lowers the cost most; keys are tried from the strictest (same gold-rank bucket and wording) to the
    loosest. Deterministic. Returns (chosen, rest, number of swaps)."""
    chosen, rest = list(chosen), list(rest)
    st = bal_stats(chosen)
    swaps = 0
    for kf in keyfs:
        while bal_cost(st, ab_lo) > 1e-9:
            idx = defaultdict(list)
            for j, d in enumerate(rest):
                idx[kf(d)].append(j)
            cur = bal_cost(st, ab_lo)
            best, arg = cur - 1e-9, None
            for i, c in enumerate(chosen):
                gc, kc = gold_longest(c), 1 / k_eff(c)
                ac, agc = shows_abstain(c), shows_abstain(c) and c["gold"] in ABSTAIN
                for j in idx.get(kf(c), ()):
                    d = rest[j]
                    ad = shows_abstain(d)
                    nst = [st[0] - gc + gold_longest(d), st[1] - kc + 1 / k_eff(d), st[2],
                           st[3] - ac + ad, st[4] - agc + (ad and d["gold"] in ABSTAIN)]
                    v = bal_cost(nst, ab_lo)
                    if v < best:
                        best, arg = v, (i, j)
            if arg is None:
                break
            i, j = arg
            chosen[i], rest[j] = rest[j], chosen[i]
            st = bal_stats(chosen)
            swaps += 1
    return chosen, rest, swaps


SWAPS = Counter()


def select(cands, n, rng, src, fr, pairs=True, tag=""):
    """Stratified pick: yes/no -> equal labels, round-robin over wordings inside each label; choice -> round-robin
    over (gold-rank bucket, wording), then repair() to the G10 targets; UCI choice -> class quota first, repair keeps
    every class count."""
    rng.shuffle(cands)
    chosen = []
    ab_lo = AB_LO if tag == "rows" else 0.0  # the 40% floor keeps abstain-as-gold rows in the training rows
    if cands and cands[0]["qtype"] == "noul" and not pairs:
        for g, m in ((1, n // 2), (0, n - n // 2)):
            chosen += round_robin([c for c in cands if c["gold"] == g], m, key=lambda c: c["_x"]["wording_id"])
        return chosen
    if cands and cands[0]["qtype"] == "noul":
        # pairs: every cell (comparison kind x wording) contributes the same number of yes and no rows, so the yes
        # rate is exactly 50% per wording and per comparison kind; inside a cell, UCI rows rotate over the asked class
        def kind(c):
            x = c["_x"]
            if "op" in x:
                return "incl" if x["op"] in (">=", "<=") else "excl"
            return x.get("form") or "-"
        cells = defaultdict(lambda: ([], []))
        for c in cands:
            cells[(kind(c), c["_x"]["wording_id"])][c["gold"]].append(c)
        for key in cells:
            for lst in cells[key]:
                rr = round_robin(lst, len(lst), key=lambda c: c["_x"].get("asked") or "-")
                lst[:] = rr[::-1]
        keys = sorted(cells)
        need = n // 2
        while need > 0 and any(cells[k][0] and cells[k][1] for k in keys):
            for k in keys:
                if need > 0 and cells[k][0] and cells[k][1]:
                    chosen += [cells[k][1].pop(), cells[k][0].pop()]
                    need -= 1
        if n % 2 and any(cells[k][0] for k in keys):
            chosen.append(next(cells[k][0].pop() for k in keys if cells[k][0]))
        return chosen
    if src in UCI_CH_GOLD:
        tot = sum(UCI_CH_GOLD[src].values())
        quotas = {cls: int(round(n * q / tot)) for cls, q in UCI_CH_GOLD[src].items()}
        while sum(quotas.values()) < n:
            quotas[max(quotas, key=lambda c: UCI_CH_GOLD[src][c] - quotas[c] * tot / n)] += 1
        for cls, m in quotas.items():
            pool = [c for c in cands if c["_x"]["published_name"] == cls]
            chosen += round_robin(pool, m, key=lambda c: c["_x"]["wording_id"])
        ids = {c["id"] for c in chosen}
        rest = [c for c in cands if c["id"] not in ids]
        chosen, _, sw = repair(chosen, rest, [lambda c: (c["_x"]["published_name"], c["_x"]["wording_id"]),
                                              lambda c: c["_x"]["published_name"]], ab_lo=ab_lo)
        SWAPS[f"{tag}:{src}:{fr}"] += sw
        if tag == "reserve":
            chosen, dr = trim(chosen)
            SWAPS[f"{tag}:{src}:{fr}:trimmed"] += dr
        return chosen

    def rank_bucket(c):
        if fr not in ("ws_agg_ch", "drop_ch") or c["gold"] in ABSTAIN:
            return "-"
        nums = sorted(float(o) for o in c["options"] if o not in ABSTAIN)
        r = nums.index(float(c["gold"])) / max(1, len(nums) - 1)
        return "low" if r < 0.34 else "mid" if r < 0.67 else "high"
    byw = defaultdict(list)
    for c in cands:
        byw[(rank_bucket(c), c["_x"]["wording_id"])].append(c)
    keys = sorted(byw)
    while len(chosen) < n and any(byw.values()):
        for k in keys:
            if byw[k] and len(chosen) < n:
                chosen.append(byw[k].pop())
    ids = {c["id"] for c in chosen}
    rest = [c for c in cands if c["id"] not in ids]
    chosen, _, sw = repair(chosen, rest, [lambda c: (rank_bucket(c), c["_x"]["wording_id"]),
                                          lambda c: c["_x"]["wording_id"], lambda c: 0], ab_lo=ab_lo)
    SWAPS[f"{tag}:{src}:{fr}"] += sw
    if tag == "reserve":
        chosen, dr = trim(chosen)
        SWAPS[f"{tag}:{src}:{fr}:trimmed"] += dr
    return chosen


def round_robin(pool, m, key):
    by = defaultdict(list)
    for c in pool:
        by[key(c)].append(c)
    keys = sorted(by)
    out = []
    while len(out) < m and any(by.values()):
        for k in keys:
            if by[k] and len(out) < m:
                out.append(by[k].pop())
    return out


# ------------------------------------------------------------------ final row

def structure_key(r):
    """Canonical problem of a row (spec 7.2 #6 / G12): dataset record + framing + what is asked (threshold, asked row
    or class); options, wording, container and card are surface form."""
    x = r["_x"]
    return "|".join(str(v) for v in (r["source"], x["framing"], x["record_id"], x.get("asked"), x.get("asked_row"),
                                      x.get("op"), x.get("T"), x.get("form")))


def finalize_row(r, mt_dev=False, c_part="train_r1"):
    x = r["_x"]
    ds = DATASETS[r["source"]]
    edge = []
    if "op" in x:
        edge.append("threshold")
        if x.get("boundary"):
            edge.append("boundary")
    if x.get("abstain_shown"):
        edge.append("abstain_shown")
    if x.get("gold_is_abstain"):
        edge.append("abstain_gold")
    if x.get("masked"):
        edge.append("masked_labels")
    if x.get("with_examples"):
        edge.append("worked_examples")
    if r["source"].startswith("c_pub_uci"):
        edge.append("rule_card")
    defs_style = x.get("defs_style") or (CARD_STYLE.get(x.get("card_id")) if x.get("card_id") else "none")
    meta = {
        "family": "public",
        "block": BLOCK[r["source"]],
        "c_part": c_part,
        "spec_id": ds["spec_id"],
        "dataset": ds["name"],
        "domain": ds["domain"],
        "framing": x["framing"],
        "card_id": x.get("card_id"),
        "card_route": x.get("card_route"),
        "domain_pack": None,
        "sampler": None,
        "wording_id": x["wording_id"],
        "defs_style": defs_style,
        "format_style": x.get("container"),
        "gen_version": GEN_VERSION,
        "git_sha": BUILDER_SHA,
        "seed": SEED,
        "structure_hash": hashlib.sha256(("struct|" + structure_key(r)).encode()).hexdigest()[:16],
        "difficulty_bin": None,  # G9 (crowd scoring on the free L4) fills these if the orchestrator applies it
        "crowd_pg": None,
        "depth": DEPTH[x["framing"]],
        "deep": False,
        "licence": ds["licence"],
        "share_alike": SHARE_ALIKE[r["source"]],
        "text_source": {"dataset": ds["name"], "record_id": x["record_id"], "split": "train"},
        "edge": edge,
        "twin_of": None,
        "twin_kind": None,
    }
    if mt_dev:
        meta["c_part"] = "mix_tuning_dev"
        meta["mt_dev"] = True
        meta["mt_dev_part"] = "public_own_10pct"
    out = {k: r[k] for k in ("id", "group_id", "call_id", "source", "state", "qtype", "instructions", "options",
                             "gold", "role", "card")}
    out["meta"] = meta
    return out


CARD_STYLE = {}
BUILDER_SHA = None


def builder_sha():
    h = hashlib.sha256()
    for name in sorted(["p2_common.py", "render.py", "uci_dex.py", "build_uci.py", "build_wikisql.py", "build_drop.py",
                        "build_hybridqa.py", "hq_fetch.py", "build_gt_index.py", "finalize.py", "qc_g15.py"]):
        h.update(name.encode())
        h.update(open(HERE / name, "rb").read())
    return "uncommitted-builder-sha256:" + h.hexdigest()[:16]


# ------------------------------------------------------------------ QC (G10 balance, G7-lite, G12, sizes)

def g7_lite(rows):
    """One-sided binomial test per unigram/bigram of instructions + metadata feature on yes/no rows, per source.
    Bonferroni at alpha 0.01; p0 = 0.5. Returns failing features (names only, counts)."""
    fails = {}
    by_src = defaultdict(list)
    for r in rows:
        if r["qtype"] == "noul":
            by_src[r["source"]].append(r)
    for src, rs in by_src.items():
        feats = defaultdict(lambda: [0, 0])
        for r in rs:
            w = norm(r["instructions"]).split()
            f = set(w) | {" ".join(w[i:i + 2]) for i in range(len(w) - 1)}
            m = r["meta"]
            f |= {f"wording={m['wording_id']}", f"card={m['card_id']}", f"style={m['format_style']}",
                  f"defs={m['defs_style']}"} | {f"edge={e}" for e in m["edge"] if e != "boundary"}
            for ft in f:
                feats[ft][r["gold"]] += 1
        nf = len(feats)
        alpha = 0.01 / max(1, nf)
        bad = []
        for ft, (n0, n1) in feats.items():
            n = n0 + n1
            if n < 20:
                continue
            k = max(n0, n1)
            p = binom_sf(k, n)  # P(X >= k), p0 = 0.5, one side (the majority side)
            if 2 * p < alpha:
                bad.append((ft, n, round(k / n, 3)))
        fails[src] = {"features_tested": nf, "fails": sorted(bad, key=lambda b: -b[1])[:20]}
    return fails


def binom_sf(k, n):
    # exact upper tail with log-space sums
    lg = math.lgamma
    tot = 0.0
    for i in range(k, n + 1):
        tot += math.exp(lg(n + 1) - lg(i + 1) - lg(n - i + 1) - n * math.log(2))
    return tot


def _by(rows, f):
    d = defaultdict(list)
    for r in rows:
        d[f(r)].append(r)
    return d


def gold_position_p(ch):
    """Chi-square p of the stored gold position, per option-count bucket (G10: uniform, p > 0.01)."""
    from scipy.stats import chisquare
    out = {}
    for k, g in sorted(_by(ch, lambda r: len(r["options"])).items()):
        cnt = [0] * k
        for r in g:
            cnt[r["options"].index(r["gold"])] += 1
        out[k] = {"n": len(g), "p": round(float(chisquare(cnt).pvalue), 4)}
    return out


def qc_report(rows, tok_counts):
    rep = {}
    by_src = defaultdict(list)
    for r in rows:
        by_src[r["source"]].append(r)
    for src, rs in sorted(by_src.items()):
        yn = [r for r in rs if r["qtype"] == "noul"]
        ch = [r for r in rs if r["qtype"] == "choice"]
        wy = defaultdict(lambda: [0, 0])
        for r in yn:
            wy[r["meta"]["wording_id"]][r["gold"]] += 1
        ab = [r for r in ch if "abstain_shown" in r["meta"]["edge"]]
        lens = [tok_counts[r["id"]] for r in rs]
        rep[src] = {
            "rows": len(rs), "yes_no": len(yn), "choice": len(ch),
            "yes_rate": round(sum(r["gold"] for r in yn) / max(1, len(yn)), 4),
            "yes_rate_by_wording": {k: round(v[1] / sum(v), 3) for k, v in sorted(wy.items())},
            "framings": dict(Counter(r["meta"]["framing"] for r in rs)),
            "wordings": len({r["meta"]["wording_id"] for r in rs}),
            "defs_styles": dict(Counter(r["meta"]["defs_style"] for r in rs)),
            "format_styles": dict(Counter(r["meta"]["format_style"] for r in rs)),
            "option_counts": dict(Counter(len(r["options"]) for r in ch)),
            "gold_longest_rate": round(sum(gold_longest(r) for r in ch) / max(1, len(ch)), 4),
            "gold_longest_expected": round(sum(1 / k_eff(r) for r in ch) / max(1, len(ch)), 4),
            "gold_longest_diff_pp": round(100 * (sum(gold_longest(r) for r in ch) - sum(1 / k_eff(r) for r in ch)) / max(1, len(ch)), 2),
            "gold_longest_diff_pp_by_framing": {fr: round(100 * (sum(gold_longest(r) for r in g) - sum(1 / k_eff(r) for r in g)) / len(g), 2)
                                                for fr, g in sorted(_by(ch, lambda r: r["meta"]["framing"]).items())},
            "gold_longest_ex_abstain_v1_measure": round(sum(gold_longest_ex_abstain(r) for r in ch if r["gold"] not in ABSTAIN) / max(1, sum(1 for r in ch if r["gold"] not in ABSTAIN)), 4),
            "abstain_rows": len(ab),
            "abstain_wrong_rate": round(sum(1 for r in ab if r["gold"] not in ABSTAIN) / max(1, len(ab)), 3),
            "gold_position_chi2_p_by_k": gold_position_p(ch),
            "card_route": dict(Counter(str(r["meta"]["card_route"]) for r in rs)),
            "max_class_count": max(Counter(str(r["gold"]) for r in rs).values()),
            "tokens_median": statistics.median(lens) if lens else 0, "tokens_max": max(lens) if lens else 0,
            "rows_ge_2000_tokens": sum(1 for x in lens if x >= 2000),
            "boundary_share_yn": round(sum("boundary" in r["meta"]["edge"] for r in yn) / max(1, len(yn)), 3),
        }
    return rep


def main():
    global BUILDER_SHA
    BUILDER_SHA = builder_sha()
    for mod in ("build_wikisql", "build_drop", "build_hybridqa"):
        m = __import__(mod)
        for cid, c in m.CARDS.items():
            CARD_STYLE[cid] = c["style"]
    cands = load_cands()
    sealed_drop = set()
    p = TMP / "sealed_drop_ids.json"
    if p.exists():
        sealed_drop = set(json.load(open(p)))
    stats = Counter()
    # UCI: readable class name for stratification
    for r in cands:
        if r["source"].startswith("c_pub_uci"):
            from build_uci import SPEC
            key = r["_x"]["dataset_key"]
            r["_x"]["published_name"] = SPEC[key]["class_names"][r["_x"]["published_class"]]
    # 1) drop sealed-check hits
    cands = [r for r in cands if r["id"] not in sealed_drop or stats.update(["sealed_drop"])]
    # 2) unique ids and exact-state dedup (G12)
    seen_id, seen_state, keep = set(), set(), []
    for r in cands:
        ns = norm(r["state"]) + "||" + norm(r["instructions"])
        if r["id"] in seen_id or ns in seen_state:
            stats["dup_drop"] += 1
            continue
        seen_id.add(r["id"])
        seen_state.add(ns)
        keep.append(r)
    cands = keep
    # 3) golden_train dedup (unit hashes over all sources + 10-grams over the spec 3.1 named sources)
    ws_tabs = wikisql_tables({r["_x"]["table_id"] for r in cands if r["source"] == "c_pub_wikisql"})
    idx = DedupIndex()
    keep = []
    for r in cands:
        if r["source"].startswith("c_pub_uci"):
            keep.append(r)
            continue
        txt = canonical_text(r, ws_tabs)
        if idx.unit_hits(txt) or idx.gram_hits(txt):
            stats[f"golden_train_drop:{r['source']}"] += 1
            continue
        # v1.1: the rendered state too (lines/sentences >= 8 words over all sources; 10-grams over the named sources)
        if idx.unit_hits(r["state"], 8) or idx.gram_hits(r["state"]):
            stats[f"golden_train_drop_rendered:{r['source']}"] += 1
            continue
        keep.append(r)
    cands = keep
    # 3b) choice rows: card text decoder_io would hide moves into instructions (v1.1)
    for r in cands:
        route_choice_card(r)
    # 4) real-tokenizer length of the real chat render (v1.1)
    tok = tokenizer()
    dio = decoder_io_pinned()
    tok_counts = {}
    keep = []
    for r in cands:
        n = real_tokens(tok, dio, r)
        tok_counts[r["id"]] = n
        if n > MAX_TOKENS:
            stats[f"too_long:{r['source']}"] += 1
            continue
        keep.append(r)
    cands = keep
    # 5) dev items: no shared >=5-word line/sentence with any train candidate text; then select
    train_units = set()
    for r in cands:
        if r["_x"]["part"] == "train" and not r["source"].startswith("c_pub_uci"):
            train_units |= {h64(u) for u in text_units(canonical_text(r, ws_tabs))}
    sel_rows, reserve, dev = [], [], []
    for src, frs in TARGETS.items():
        for fr, n in frs.items():
            pool = [r for r in cands if r["source"] == src and r["_x"]["framing"] == fr and r["_x"]["part"] == "train"]
            got = select(list(pool), n, rng_for("select", src, fr), src, fr, tag="rows")
            if len(got) < n:
                stats[f"short:{src}:{fr}"] = n - len(got)
            ids = {r["id"] for r in got}
            rest = [r for r in pool if r["id"] not in ids]
            rest = select(rest, int(n * RESERVE_FRAC), rng_for("reserve", src, fr), src, fr, tag="reserve") if rest else []
            sel_rows += got
            reserve += rest
            dpool = [r for r in cands if r["source"] == src and r["_x"]["framing"] == fr and r["_x"]["part"] == "dev"]
            if not src.startswith("c_pub_uci"):
                dpool = [r for r in dpool if not ({h64(u) for u in text_units(canonical_text(r, ws_tabs))} & train_units)]
            dsel = select(list(dpool), DEV_TARGETS[src][fr], rng_for("dev", src, fr), src, fr, pairs=False, tag="dev")
            dev += dsel
    final = [finalize_row(r) for r in sel_rows]
    res = [finalize_row(r, c_part="train_r1_reserve") for r in reserve]
    devf = [finalize_row(r, mt_dev=True) for r in dev]
    for nm, lst in (("rows", final), ("reserve", res), ("dev", devf)):
        stats[f"gold_position_moved:{nm}"] = gold_position_repair(lst, f"pos:{nm}")
    # G1-style structural check against the shared raw format
    need = ["id", "group_id", "call_id", "source", "state", "qtype", "instructions", "options", "gold", "role",
            "card", "meta"]
    for r in final + res + devf:
        assert all(k in r for k in need), r["id"]
        assert r["qtype"] in ("noul", "choice")
        if r["qtype"] == "noul":
            assert r["gold"] in (0, 1) and r["options"] is None and r["role"] == "aff"
        else:
            assert r["gold"] in r["options"] and len(set(r["options"])) == len(r["options"]) and r["role"] == "choice"
        assert not any(k.lower().startswith("jev") for k in r) and not any(k.lower().startswith("jev") for k in r["meta"])
    assert len({r["id"] for r in final + res + devf}) == len(final + res + devf)
    assert not ({r["group_id"] for r in devf} & {r["group_id"] for r in final + res})
    OUT.mkdir(exist_ok=True)
    sha = {
        "rows_r1.jsonl": write_jsonl(OUT / "rows_r1.jsonl", final),
        "reserve_r1.jsonl": write_jsonl(OUT / "reserve_r1.jsonl", res),
        "dev_mt_r1.jsonl": write_jsonl(OUT / "dev_mt_r1.jsonl", devf),
    }
    # pools: wordings, cards, styles (every entry has a stable id)
    import build_drop
    import build_hybridqa
    import build_uci
    import build_wikisql
    wl = []
    for mod, ds in ((build_wikisql, "WikiSQL"), (build_drop, "DROP"), (build_hybridqa, "HybridQA"), (build_uci, "UCI")):
        for nm in dir(mod):
            if nm.startswith("W_") and isinstance(getattr(mod, nm), dict):
                for wid, txt in getattr(mod, nm).items():
                    wl.append({"id": wid, "dataset": ds, "pool": nm, "text": txt})
    for mod, ds in ((build_wikisql, "WikiSQL"), (build_drop, "DROP"), (build_hybridqa, "HybridQA")):
        for nm, ops in (("OPP", getattr(mod, "OPP", {})), ("COUNT_OPP", getattr(mod, "COUNT_OPP", {}))):
            for op, words in ops.items():
                for i, w in enumerate(words):
                    wl.append({"id": f"{ds.lower()}_{nm.lower()}_{op}_{i}", "dataset": ds, "pool": nm, "text": w})
    sha["wordings.jsonl"] = write_jsonl(OUT / "wordings.jsonl", wl)
    cards = {}
    for r in final + res + devf:
        if r["card"]:
            cid = "card_" + hashlib.sha256(r["card"].encode()).hexdigest()[:16]
            cards.setdefault(cid, {"id": cid, "card_id": r["meta"]["card_id"], "source": r["source"],
                                   "defs_style": r["meta"]["defs_style"], "route": "card", "text": r["card"]})
    for r in sel_rows + reserve + dev:  # v1.1: card text moved into a choice row's instructions (same pool, own id)
        mv = r["_x"].get("moved_card")
        if mv:
            cid = "card_" + hashlib.sha256(mv.encode()).hexdigest()[:16]
            cards.setdefault(cid, {"id": cid, "card_id": r["_x"]["card_id"], "source": r["source"],
                                   "defs_style": r["_x"].get("defs_style") or CARD_STYLE.get(r["_x"].get("card_id")),
                                   "route": "instructions", "text": mv})
    sha["cards.jsonl"] = write_jsonl(OUT / "cards.jsonl", sorted(cards.values(), key=lambda c: c["id"]))
    from render import CONTAINERS
    styles = [{"id": f"p2_style_{c}", "container": c, "used_by": "WikiSQL/HybridQA tables"} for c in CONTAINERS] + \
             [{"id": f"p2_style_case_{c}", "container": c, "used_by": "UCI case"} for c in ("key_value", "json", "markdown", "prose")] + \
             [{"id": "p2_style_prose_passage", "container": "prose", "used_by": "DROP passage"}]
    sha["styles.jsonl"] = write_jsonl(OUT / "styles.jsonl", styles)
    # table hashes (for the orchestrator's TabFact table-hash check, spec 7.2 #9)
    th = []
    hq_t = {}
    for r in sel_rows + reserve + dev:
        x = r["_x"]
        if r["source"] == "c_pub_wikisql":
            t = ws_tabs[x["table_id"]]
            th.append({"id": r["id"], "source": r["source"], "table_id": x["table_id"],
                       **table_hash(t["header"], t["rows"], t.get("page_title"))})
        elif r["source"] == "c_pub_hybridqa":
            if x["table_id"] not in hq_t:
                hq_t[x["table_id"]] = hq_table_hash(x["table_id"])
            th.append({"id": r["id"], "source": r["source"], "table_id": x["table_id"], **hq_t[x["table_id"]]})
    sha["table_hashes.jsonl"] = write_jsonl(OUT / "table_hashes.jsonl", th)
    rep = {"rows": qc_report(final, tok_counts), "reserve": qc_report(res, tok_counts),
           "dev": qc_report(devf, tok_counts),
           "g7_lite_rows": g7_lite(final), "filter_counts": dict(stats), "repair_swaps": dict(SWAPS),
           "tokenizer": "Qwen/Qwen3.5-4B (local cache); tokens = the real chat render: decoder_io.render_chat("
                        "CYGNET_SYSTEM, user_msg) under OD_STYLE=cygnet, LAYOUT=schema_branch_mark (A16 908c08d7)"}
    json.dump(rep, open(OUT / "qc_report.json", "w"), indent=1)
    sha["qc_report.json"] = sha256_file(OUT / "qc_report.json")
    json.dump({"sha256": sha, "builder": BUILDER_SHA, "counts": {
        "rows_r1": dict(Counter(r["source"] for r in final)),
        "reserve_r1": dict(Counter(r["source"] for r in res)),
        "dev_mt_r1": dict(Counter(r["source"] for r in devf)),
        "rows_r1_by_framing": dict(Counter(f"{r['source']}:{r['meta']['framing']}" for r in final)),
        "rows_r1_by_label": dict(Counter(f"{r['source']}:{r['qtype']}:{r['gold'] if r['qtype'] == 'noul' else 'choice'}" for r in final)),
    }, "filters": dict(stats), "repair_swaps": dict(SWAPS)}, open(TMP / "finalize_summary.json", "w"), indent=1)
    log_progress(f"finalize: rows {len(final)}, reserve {len(res)}, dev {len(devf)}, filters {json.dumps(dict(stats))}")
    print(json.dumps({"rows": len(final), "reserve": len(res), "dev": len(devf), "filters": dict(stats)}))


if __name__ == "__main__":
    main()
