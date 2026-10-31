#!/usr/bin/env python3
"""Independent QC checker for public-1 (endgame-prep-5 QC agent; not the builder). C_DATA_SPEC v4 section 8:
"Public rows pass G1, G6 (on our framings), G7, G10, G12, G13, G15 and a G5 read" (G13 runs in the orchestrator's
counts-only tool; G5 is qc/g5_read.py). Reads only public-1 out/ files, the manifest and the builder's logs (as inputs
to check), prints counts only, never row text, never edits a row. Writes qc/gate_<name>.json.

Population: the two files the mixer binds (out/public1_rows_r1.jsonl = "rows", out/public1_reserve.jsonl =
"reserve"); gates are judged on rows and on rows+reserve ("pool", what the mixer may draw); out/public1_mtdev.jsonl is
used only for the train/dev separation checks.

Usage: qc_gates.py g1 | g15 | bal | g6      (bal = G7 + G10 + G12 + dev separation)

Repair round 1 (PREREG A29 a; 6 Oct): spec 8 exactly, the checker's non-spec add-ons removed:
  - G10: every cell family x wording x bin x negation count must sit in 50 +/- 2 (no small-cell binomial exemption).
    The negation count is checked under both readings used in this repo (negcount.k_syn of the framing question, and
    negcount.k_all of the instructions as mixer.py counts it); a cell fails under either.
  - G6: judged on the spec's separate QC sample (>= 5,000 rows per family from the same generators: the builder's
    tmp/qcs_<ds>.json, never trained). QuALITY has fewer real rows than 5,000 (spec 8 G6 parenthesis), so its QC
    sample is every row its generator emits (rows + reserve). rows and pool results are printed as information.
    5-fold GroupKFold on group_id, best of LR / GBT accuracy <= chance + 2 pp; no p-value condition.
  - G10 gold letter: chi-square p > 0.01 in every option bucket (the 'n >= 5k' exemption removed); 'longest option is
    gold' within +/- 2 pp of 1/k per (dataset, k) bucket as well as per dataset (the per-bucket line was info only)."""
from __future__ import annotations

import collections
import hashlib
import json
import math
import random
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
P1 = HERE.parent
LEAN = P1.parents[2]
PY = "/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python"
SNAP = Path("~/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/"
            "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a").expanduser()
FILES = {"rows": "out/public1_rows_r1.jsonl", "reserve": "out/public1_reserve.jsonl"}
DEV = "out/public1_mtdev.jsonl"
SEED = "public1-qc-prep5"
ABSTAIN = re.compile(r"(?i)\b(none of (the|these)|not (answerable|answered|enough|stated|given|mentioned)|"
                     r"cannot be (answered|determined|told)|can't (be )?(tell|answered)|no answer|unanswerable|"
                     r"neither of (them|these|the (above|options))|not possible to (tell|say))\b")
TOK = re.compile(r"[a-z0-9]+")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def h(*a):
    return hashlib.sha256("|".join(map(str, a)).encode()).hexdigest()


def load(rel):
    return [json.loads(x) for x in open(P1 / rel)]


def parts():
    return {k: load(v) for k, v in FILES.items()}


def log(msg):
    with open(LEAN / "c_build/progress_prep.log", "a") as f:
        f.write(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) + " [prep5] public-1 QC " + msg + "\n")


def dump(name, obj):
    (HERE / f"gate_{name}.json").write_text(json.dumps(obj, indent=1, default=str))


def paras(t):
    return [p.strip() for p in re.split(r"\n\s*\n", t or "") if p.strip()]


def framing_q(r):
    p = paras(r["instructions"])
    return p[-1] if p else ""


def item_q(r):
    p = paras(r["state"])
    if p and p[-1].rstrip().endswith("?"):
        return re.sub(r"^Question:\s*", "", p[-1])
    return ""


def label_yes(r):
    return r["gold"] == 1


def gidx(r):
    """gold option index: choice rows store gold as the option text (raw format), yes/no rows as 1/0."""
    g = r["gold"]
    return r["options"].index(g) if isinstance(g, str) else int(g)


def k_of(r):
    return 2 if r["qtype"] == "noul" else len(r["options"])


# ------------------------------------------------------------------ G1
REQ_TOP = ["id", "group_id", "call_id", "source", "state", "qtype", "instructions", "options", "gold", "role", "card"]
REQ_META = ["family", "spec_id", "card_id", "domain_pack", "sampler", "gen_version", "git_sha", "seed",
            "structure_hash", "difficulty_bin", "crowd_pg", "depth", "deep", "format_style", "wording_id",
            "defs_style", "twin_of", "twin_kind", "text_source", "licence", "edge"]
ALLOWED = {"CC BY-SA 4.0": "share-alike", "CC BY 4.0": "permissive", "Apache-2.0": "permissive"}
# my own must-patterns for the re-read (each official record must still state the licence)
REREAD = {
    "c_pub_squad2": ("https://rajpurkar.github.io/SQuAD-explorer/", [r"CC BY-SA 4\.0|creativecommons\.org/licenses/by-sa/4\.0"]),
    "c_pub_musique": (None, [r"Attribution 4\.0 International"]),
    "c_pub_2wiki": (None, [r"Apache License", r"Version 2\.0"]),
    "c_pub_quality": ("https://nyu-mll.github.io/quality/", [r"CC BY 4\.0"]),
}
OANC = ("https://anc.org/data/oanc/", [r"without restriction"])
QUALITY_TEXT_OK = re.compile(r"Gutenberg|OANC|Slate|CC BY", re.I)


def fetch(url):
    try:
        out = subprocess.run(["curl", "-sL", "--max-time", "40", url], capture_output=True, timeout=60)
        return out.stdout
    except Exception:  # noqa: BLE001
        return b""


def g1():
    P = parts()
    man = json.loads((P1 / "manifest_public1.json").read_text())
    reg = (LEAN / "c_spec/LICENCE_REGISTER.md").read_text()
    reg1 = reg.split("## 3.")[0]                   # register sections 1-2
    res, fail = {}, collections.Counter()
    allrows = [r for v in P.values() for r in v]
    # per-row meta (section 2.4)
    miss = collections.Counter()
    for r in allrows:
        for k in REQ_TOP:
            if k not in r:
                miss["top:" + k] += 1
        for k in REQ_META:
            if k not in r["meta"]:
                miss["meta:" + k] += 1
        ts = r["meta"].get("text_source") or {}
        if not (ts.get("dataset") and ts.get("record_id") and ts.get("split") == "train"):
            miss["text_source_not_train_record"] += 1
        if r["meta"].get("family") != "public":
            miss["family_not_public"] += 1
    res["row_meta_missing"] = dict(miss)
    fail.update({"G1_row_meta:" + k: v for k, v in miss.items()})
    # per-dataset licence record
    ds_res = {}
    for src, d in man["datasets"].items():
        rows = [r for r in allrows if r["source"] == src]
        x = {"rows": len(rows)}
        lic = d["licence"].split(" (")[0].split(";")[0].strip()
        x["licence"] = d["licence"]
        x["licence_allowed"] = lic in ALLOWED
        x["share_alike_flag"] = d.get("share_alike")
        url = d["official_record"]
        commit = (d.get("upstream_commit") or "").split("@")[-1]
        repo = (d.get("upstream_commit") or "").split("@")[0]
        x["has_url_commit"] = bool(url and len(commit) >= 12 and repo)
        # official record named in LICENCE_REGISTER 1-2 (same page, or same repo LICENSE file at a pinned commit)
        reg_ok = url in reg1 or (repo and f"github.com/{repo}/blob/main/LICENSE" in reg1 and url.endswith("/LICENSE"))
        x["record_in_register_1_2"] = bool(reg_ok)
        x["info_commit_in_register"] = commit[:12] in reg1      # info: the register need not carry it
        # every row's meta.licence carries licence + record + commit + text note
        bad = sum(1 for r in rows if not (r["meta"]["licence"].startswith(lic) and "record " in r["meta"]["licence"]
                                         and commit[:12] in r["meta"]["licence"]))
        x["rows_meta_licence_incomplete"] = bad
        x["rows_without_text_note"] = sum(1 for r in rows if "Wikipedia" not in r["meta"]["licence"]
                                          and src != "c_pub_quality")   # QuALITY: per-article check below
        sa_rows = sum(1 for r in rows if r["meta"].get("share_alike"))
        x["rows_share_alike"] = sa_rows
        x["text_licence_note"] = bool(d.get("text_licence"))
        x["parents"] = d.get("parents")
        x["parents_declared"] = isinstance(d.get("parents"), list) and all(isinstance(p, str) for p in d["parents"])
        # saved record copy vs recorded sha; live re-read now
        rr = d.get("licence_record_reread") or {}
        saved = sorted((P1 / "licence_records").glob(Path(rr.get("saved", "none")).name + "*"))
        x["saved_record_sha_match"] = any(sha(p) == rr.get("sha256") for p in saved)
        u, pats = REREAD[src]
        u = u or rr.get("url")
        body = fetch(u)
        txt = body.decode("utf-8", "replace")
        x["reread_now"] = {"url": u, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(),
                           "same_bytes_as_recorded": hashlib.sha256(body).hexdigest() == rr.get("sha256"),
                           "licence_stated": all(re.search(p, txt) for p in pats),
                           "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        ok = (x["licence_allowed"] and x["has_url_commit"] and x["record_in_register_1_2"]
              and not bad and not x["rows_without_text_note"] and x["text_licence_note"] and x["parents_declared"]
              and x["reread_now"]["licence_stated"])
        if ALLOWED.get(lic) == "share-alike" and sa_rows != len(rows):
            ok = False
            x["sa_licence_rows_not_flagged"] = len(rows) - sa_rows
        x["pass"] = bool(ok)
        if not ok:
            fail["G1_dataset:" + src] += 1
        ds_res[src] = x
    res["datasets"] = ds_res
    # QuALITY document-text licence, per item (3.1 v2): every article kept, train split, cleared source
    qa = json.loads((P1 / "logs/quality_articles.json").read_text())
    qrows = [r for r in allrows if r["source"] == "c_pub_quality"]
    arts = collections.Counter(r["meta"]["text_source"]["record_id"].split("_")[0] for r in qrows)
    badq = {a: n for a, n in arts.items() if not (a in qa and qa[a].get("kept") and qa[a].get("split") == "train"
                                                  and QUALITY_TEXT_OK.search(qa[a].get("licence_class", "")))}
    res["quality_text_licence"] = {"articles": len(arts), "by_class": dict(collections.Counter(
        qa[a]["licence_class"].split(" (")[0] for a in arts if a in qa)), "articles_not_cleared": len(badq),
        "rows_not_cleared": sum(badq.values())}
    if badq:
        fail["G1_quality_text_not_cleared"] += sum(badq.values())
    oanc = fetch(OANC[0]).decode("utf-8", "replace")
    res["oanc_terms_reread"] = {"url": OANC[0], "licence_stated": all(re.search(p, oanc) for p in OANC[1])}
    if any(qa[a]["licence_class"].lower().find("oanc") >= 0 for a in arts if a in qa) and \
            not res["oanc_terms_reread"]["licence_stated"]:
        fail["G1_oanc_record"] += 1
    # deny-list (3.H) over every dataset and every declared parent, with the current deny-list program
    q = {"purpose": "public-1 independent QC (prep5): 3.H check of every emitting dataset + declared parents",
         "datasets": {}}
    bq = json.loads((P1 / "denylist/query_public1.json").read_text())["datasets"]
    for i, (src, d) in enumerate(man["datasets"].items()):
        names = [d["dataset"], src.replace("c_pub_", "")]
        for v in bq.values():
            if any(n.lower().replace(" ", "") in (src + d["dataset"]).lower().replace(" ", "") for n in v["names"][:1]):
                names += v["names"]
        q["datasets"][f"{i + 1}_{src}"] = {"names": sorted(set(names)), "datasets": [d["dataset"]],
                                           "domains": [], "parents": d["parents"], "emits_rows": True}
    (HERE / "denylist_query_qc.json").write_text(json.dumps(q, indent=1))
    out = subprocess.run([PY, str(LEAN / "c_src/common/denylist.py"), "check", "--query", str(HERE / "denylist_query_qc.json"),
                          "--out", str(HERE / "denylist_verdicts_qc.json"), "--run", "public1_qc", "--fail-on-taint"],
                         cwd=str(LEAN), capture_output=True, text=True, timeout=600)
    v = json.loads((HERE / "denylist_verdicts_qc.json").read_text()) if (HERE / "denylist_verdicts_qc.json").exists() else {}
    summ = v.get("summary") or {k: v.get(k) for k in ("datasets", "hit", "deny_taint", "no_new_rows", "pass")}
    res["denylist"] = {"exit": out.returncode, "summary": summ,
                       "lines": [ln[:160] for ln in out.stdout.splitlines() if ln.strip().startswith(("HIT", "no-hit", "DENY", "deny"))][:12],
                       "denylist_program_sha256": sha(LEAN / "c_src/common/denylist.py")}
    if out.returncode != 0:
        fail["denylist_exit_%d" % out.returncode] += 1
    res["fail"] = dict(fail)
    res["pass"] = not fail
    dump("g1", res)
    log(f"G1 pass={res['pass']} fail={dict(fail)}")
    print("G1", res["pass"], dict(fail))


# ------------------------------------------------------------------ G15
def g15():
    sys.path.insert(0, str(LEAN))
    sys.path.insert(0, str(LEAN / "c_src/formats/formats-1"))
    from fmt1 import card as fcard
    dio = fcard._dio()
    td = fcard._td()
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(str(SNAP), local_files_only=True)
    P = parts()
    P["dev"] = load(DEV)
    res, fail = {}, collections.Counter()
    for p, rows in P.items():
        x = collections.Counter()
        for kd in (0.0, 0.5):
            try:
                td.check_rows(rows, kd=kd)
                x[f"check_rows_kd{kd}_ok"] = 1
            except Exception as e:  # noqa: BLE001
                fail[f"G15_check_rows:{p}:kd{kd}"] += 1
                res.setdefault("errors", []).append(f"{p} kd{kd}: {str(e)[:160]}")
        kinds = collections.Counter()
        lens = collections.defaultdict(list)
        tokn = {}
        for r in rows:
            ms = [r["card"]] if r.get("card") else []
            ok = True
            for s in range(3):     # three independent random option orders per row
                rng = random.Random(h(SEED, "g15", s, r["id"]))
                n = k_of(r)
                perm = list(range(n))
                rng.shuffle(perm)
                c = fcard.loader_check(r, must_show=ms, perm=perm, check_rows=False)
                if not c["ok"]:
                    ok = False
                    for pr in c["problems"]:
                        kinds[f"{r['source']}|{r['qtype']}|{pr[:50]}"] += 1
            x["rows"] += 1
            x["loader_ok"] += ok
            dio.STYLE, dio.LAYOUT = "cygnet", "schema_branch_mark"
            lr = dio.as_letter_row(r)
            perm = list(range(len(lr["options"])))
            random.Random(h(SEED, "len", r["id"])).shuffle(perm)
            txt = dio.render_chat(tok, dio.CYGNET_SYSTEM, dio.user_msg(r, perm))
            n = len(tok(txt, add_special_tokens=False)["input_ids"])
            tokn[r["id"]] = n
            lens[r["source"]].append(n)
        units = collections.defaultdict(list)
        for r in rows:
            units[r["call_id"]].append(r["id"])
        big = [u for u, ids in units.items() if len(ids) > 3]
        long_big = [u for u, ids in units.items() if len(ids) > 2 and any(tokn[i] >= 2000 for i in ids)]
        over = sum(1 for v in tokn.values() if v > 7900)
        res[p] = {**dict(x), "loader_fail_kinds": dict(kinds), "units": len(units),
                  "max_rows_per_call_unit": max(len(v) for v in units.values()),
                  "units_over_3_rows": len(big), "units_with_row_ge2000_over_2_rows": len(long_big),
                  "rows_over_7900_tokens": over,
                  "real_tokens": {s: {"n": len(v), "median": sorted(v)[len(v) // 2], "max": max(v),
                                      "ge2000": sum(t >= 2000 for t in v)} for s, v in lens.items()}}
        if x["loader_ok"] != x["rows"]:
            fail[f"G15_loader:{p}"] += x["rows"] - x["loader_ok"]
        if big:
            fail[f"G15_unit_gt3:{p}"] += len(big)
        if long_big:
            fail[f"G15_long_unit_gt2:{p}"] += len(long_big)
        if over:
            fail[f"G15_len_gt7900:{p}"] += over
    res["read_20_per_dataset"] = "covered by the G5 read (qc/g5_read.py renders decoder_io.user_msg; >= 100 per dataset)"
    res["fail"] = dict(fail)
    res["pass"] = not fail
    dump("g15", res)
    log(f"G15 pass={res['pass']} fail={dict(fail)}")
    print("G15", res["pass"], dict(fail))


# ------------------------------------------------------------------ G7 / G10 / G12 / separation
def binom_sf(k, n, p):
    """P(X >= k), X ~ Bin(n, p)."""
    from scipy.stats import binom
    return float(binom.sf(k - 1, n, p))


def grams(text):
    t = TOK.findall((text or "").lower())
    return set(t) | {a + " " + b for a, b in zip(t, t[1:])}


def opt_meta(r, j):
    L = [len(o) for o in r["options"]]
    mx, mn = max(L), min(L)
    return {f"longest={L[j] == mx}", f"shortest={L[j] == mn}", f"abstain={bool(ABSTAIN.search(r['options'][j]))}",
            f"lenbin={min(9, L[j] // 20)}", f"digits={bool(re.search(r'[0-9]', r['options'][j]))}"}


def row_meta(r):
    m = r["meta"]
    return {f"{k}={m.get(k)}" for k in ("wording_id", "card_id", "format_style", "defs_style", "card_route", "depth",
                                        "deep", "twin_kind", "domain_pack", "sampler")} | {
        f"k={k_of(r)}", f"statelen={min(20, len(r['state']) // 1000)}", f"iq_len={min(10, len(item_q(r)) // 20)}"}


def g7_set(rows):
    """One-sided binomial per feature, p0 = 1/k, Bonferroni alpha 0.01 over all features tested in this set."""
    yn = [r for r in rows if r["qtype"] == "noul"]
    ch = [r for r in rows if r["qtype"] == "choice"]
    tests = []                       # (feature, n, hits, p0)
    # yes/no: every visible-text unigram/bigram (state + instructions + card) and row metadata, vs each label
    cnt = collections.defaultdict(lambda: [0, 0])
    for r in yn:
        fs = {"t:" + g for g in grams(r["state"] + " " + r["instructions"] + " " + (r.get("card") or ""))}
        fs |= {"m:" + g for g in row_meta(r)}
        for f in fs:
            cnt[f][0] += 1
            cnt[f][1] += label_yes(r)
    for f, (n, y) in cnt.items():
        tests.append(("yn|yes|" + f, n, y, 0.5))
        tests.append(("yn|no|" + f, n, n - y, 0.5))
    cw = collections.defaultdict(lambda: [0, 0])          # within one wording: feature vs label
    for r in yn:
        w = r["meta"].get("wording_id")
        for g in grams(item_q(r) + " " + (r.get("card") or "")):
            cw[(w, g)][0] += 1
            cw[(w, g)][1] += label_yes(r)
    for (w, g), (n, y) in cw.items():
        tests.append((f"ynw|{w}|yes|t:{g}", n, y, 0.5))
        tests.append((f"ynw|{w}|no|t:{g}", n, n - y, 0.5))
    # choice: option-level text features and option metadata vs "this option is gold", p0 = 1/k (per k bucket);
    # row metadata vs gold position (p0 = 1/k)
    cc = collections.defaultdict(lambda: [0, 0])
    for r in ch:
        k = len(r["options"])
        for j, o in enumerate(r["options"]):
            fs = {"o:" + g for g in grams(o)} | {"om:" + g for g in opt_meta(r, j)}
            for f in fs:
                cc[(k, f)][0] += 1
                cc[(k, f)][1] += (j == gidx(r))
    for (k, f), (n, y) in cc.items():
        tests.append((f"ch|k{k}|" + f, n, y, 1.0 / k))
    M = max(1, len(tests))
    thr = 0.01 / M
    fails = []
    for f, n, y, p0 in tests:
        if y / n <= p0 or n < 5:
            continue
        p = binom_sf(y, n, p0)
        if p < thr:
            fails.append((f, n, y, round(y / n, 4), p))
    fails.sort(key=lambda t: t[4])
    return {"yn_rows": len(yn), "choice_rows": len(ch), "features_tested": M, "alpha_per_test": thr,
            "failing_features": len(fails), "top_failing": [[f[:70], n, y, fr, f"{p:.2e}"] for f, n, y, fr, p in fails[:15]]}


def g10_set(rows):
    sys.path.insert(0, str(LEAN / "c_src/common"))
    import negcount
    from scipy.stats import chisquare
    out, fail = {}, collections.Counter()
    yn = [r for r in rows if r["qtype"] == "noul"]
    cells = collections.defaultdict(lambda: [0, 0])
    agg = collections.defaultdict(lambda: [0, 0])
    for r in yn:
        ks = negcount.k_syn(framing_q(r))
        c = (r["source"], r["meta"].get("wording_id"), r["meta"].get("difficulty_bin"), ks)
        cells[c][0] += 1
        cells[c][1] += label_yes(r)
        agg[r["source"]][0] += 1
        agg[r["source"]][1] += label_yes(r)
    # spec 8 G10 exactly: aggregate yes rate 50% +/- 2 in EVERY cell family x wording x bin x negation count (no
    # small-cell exemption). Two readings of the negation count: k_syn(framing question) (cells above) and
    # k_all(instructions) (as mixer.py counts it); a cell outside the band under either reading fails.
    mc = collections.defaultdict(lambda: [0, 0])
    for r in yn:
        c = (r["source"], str(r["meta"].get("wording_id")), str(r["meta"].get("difficulty_bin")),
             negcount.k_all(r["instructions"]))
        mc[c][0] += 1
        mc[c][1] += label_yes(r)
    band_all = {"|".join(map(str, c)): [n, y, round(y / n, 4)] for c, (n, y) in mc.items()
                if abs(y / n - 0.5) > 0.02 + 1e-12}
    band_syn = {"|".join(map(str, c)): [n, y, round(y / n, 4)] for c, (n, y) in cells.items()
                if abs(y / n - 0.5) > 0.02 + 1e-12}
    out["yes_rate_by_dataset"] = {s: round(y / n, 4) for s, (n, y) in agg.items()}
    out["yn_cells_k_all"] = len(mc)
    out["yn_cells_k_syn"] = len(cells)
    out["min_cell_n"] = min([n for n, _ in list(mc.values()) + list(cells.values())], default=0)
    out["cells_outside_50pm2_k_all"] = band_all
    out["cells_outside_50pm2_k_syn"] = band_syn
    if band_all or band_syn:
        fail["G10_yes_rate_cells"] += len(band_all) + len(band_syn)
    # item-question negation (info): yes rate by k_syn of the item question
    iq = collections.defaultdict(lambda: [0, 0])
    for r in yn:
        k = negcount.k_syn(item_q(r)) if item_q(r) else -1
        iq[(r["source"], k)][0] += 1
        iq[(r["source"], k)][1] += label_yes(r)
    out["info_yes_rate_by_item_question_negation"] = {f"{s}|{k}": [n, round(y / n, 3)] for (s, k), (n, y) in iq.items()}
    ch = [r for r in rows if r["qtype"] == "choice"]
    by_k = collections.defaultdict(list)
    for r in ch:
        by_k[(r["source"], len(r["options"]))].append(r)
    gl, lg, ab = {}, {}, {}
    for (s, k), rs in by_k.items():
        obs = [0] * k
        for r in rs:
            obs[gidx(r)] += 1
        p = float(chisquare(obs).pvalue)  # repair r1: every option bucket (no small-n exemption; spec 8 G10)
        gl[f"{s}|k{k}"] = {"n": len(rs), "counts": obs, "chi2_p": p}
        if p is not None and p <= 0.01:
            fail["G10_gold_letter"] += 1
        lw = 0.0
        for r in rs:
            L = [len(o) for o in r["options"]]
            mx = max(L)
            t = [j for j, x in enumerate(L) if x == mx]
            lw += (gidx(r) in t) / len(t)
        rate = lw / len(rs)
        lg[f"{s}|k{k}"] = {"n": len(rs), "longest_is_gold": round(rate, 4), "chance": round(1 / k, 4)}
        if abs(rate - 1 / k) > 0.02 + 1e-12:  # repair r1: spec 8 G10 '1/k' read per option bucket too (gating)
            fail["G10_longest_gold_bucket"] += 1
        shown = [r for r in rs if any(ABSTAIN.search(o) for o in r["options"])]
        if shown:
            wrong = sum(1 for r in shown if not ABSTAIN.search(r["options"][gidx(r)]))
            ab[f"{s}|k{k}"] = {"rows_showing": len(shown), "abstain_wrong_share": round(wrong / len(shown), 4)}
            if wrong / len(shown) < 0.5:
                fail["G10_abstain"] += 1
    lfam = {}
    for s in sorted({r["source"] for r in ch}):
        rs = [r for r in ch if r["source"] == s]
        lw = sum((gidx(r) in [j for j, o in enumerate(r["options"]) if len(o) == max(map(len, r["options"]))]) /
                 sum(1 for o in r["options"] if len(o) == max(map(len, r["options"]))) for r in rs)
        ek = sum(1 / len(r["options"]) for r in rs)
        lfam[s] = {"n": len(rs), "longest_is_gold": round(lw / len(rs), 4), "mean_1_over_k": round(ek / len(rs), 4),
                   "diff_pp": round(100 * (lw - ek) / len(rs), 2)}
        if abs(lw - ek) / len(rs) > 0.02:
            fail["G10_longest_gold"] += 1
    out["longest_is_gold_per_dataset"] = lfam
    out["gold_letter"] = gl
    out["longest_is_gold"] = lg
    out["abstain"] = ab
    att = sum(1 for r in rows if any("attack" in str(e) or "inject" in str(e) for e in (r["meta"].get("edge") or [])))
    out["attack_rows"] = att
    out["fail"] = dict(fail)
    return out


def norm_txt(s):
    return re.sub(r"\s+", " ", (s or "").lower()).strip()


def g12_set(rows):
    from datasketch import MinHash, MinHashLSH
    out, fail = {}, collections.Counter()
    ex = collections.Counter(h(r["qtype"], norm_txt(r.get("card")), norm_txt(r["instructions"]), norm_txt(r["state"]),
                               "\x1f".join(norm_txt(o) for o in (r["options"] or []))) for r in rows)
    out["exact_dupe_rows"] = sum(n - 1 for n in ex.values() if n > 1)
    if out["exact_dupe_rows"]:
        fail["G12_exact"] += out["exact_dupe_rows"]
    # MinHash near-dups: word 5-gram shingles of question paragraph + state + options (spec 7.2: Jaccard >= 0.8),
    # verified by exact shingle Jaccard; pairs inside one planned set (same group_id) are allowed
    lsh = MinHashLSH(threshold=0.8, num_perm=128)
    sh = {}
    for r in rows:
        w = (framing_q(r) + " " + r["state"] + " " + " ".join(r["options"] or [])).lower().split()
        s = {" ".join(w[i:i + 5]) for i in range(max(1, len(w) - 4))}
        m = MinHash(num_perm=128, seed=1)
        for x in s:
            m.update(x.encode())
        sh[r["id"]] = s
        lsh.insert(r["id"], m)
        r["_mh"] = m
    by = {r["id"]: r for r in rows}
    pairs, inside = set(), 0
    for r in rows:
        for o in lsh.query(r["_mh"]):
            if o <= r["id"]:
                continue
            a, b = sh[r["id"]], sh[o]
            j = len(a & b) / max(1, len(a | b))
            if j >= 0.8:
                if by[o]["group_id"] == r["group_id"] or by[o]["call_id"] == r["call_id"]:
                    inside += 1
                else:
                    pairs.add((r["id"], o))
    for r in rows:
        r.pop("_mh", None)
    out["near_dup_pairs_cross_group"] = len(pairs)
    out["near_dup_pairs_inside_planned_group"] = inside
    if pairs:
        fail["G12_near_dup"] += len(pairs)
    # structure hash: one surface form per structure (except planned twins / format variants = same group_id)
    st = collections.defaultdict(set)
    for r in rows:
        st[r["meta"]["structure_hash"]].add(r["group_id"])
    coll = sum(1 for v in st.values() if len(v) > 1)
    out["structure_hash_values"] = len(st)
    out["structure_hash_across_groups"] = coll
    if coll:
        fail["G12_structure"] += coll
    # same item question + same state in two groups (a second surface form of one item)
    iq = collections.defaultdict(set)
    for r in rows:
        iq[h(norm_txt(framing_q(r)), norm_txt(item_q(r)), norm_txt(r["state"]))].add(r["group_id"])
    out["same_item_text_across_groups"] = sum(1 for v in iq.values() if len(v) > 1)
    if out["same_item_text_across_groups"]:
        fail["G12_item_across_groups"] += out["same_item_text_across_groups"]
    out["fail"] = dict(fail)
    return out


def separation(pool, dev):
    """3.1 / 10 S7: train+reserve vs mix-tuning dev share no group_id, record, normalised state, structure_hash or
    Wikipedia page title (pages are split train/dev by title)."""
    def keys(r):
        ts = r["meta"].get("text_source") or {}
        return {"group": r["group_id"], "record": f"{r['source']}|{ts.get('record_id')}",
                "state": h(norm_txt(r["state"])), "structure": r["meta"]["structure_hash"]}
    dk = collections.defaultdict(set)
    for r in dev:
        for k, v in keys(r).items():
            dk[k].add(v)
    clash = collections.Counter()
    for r in pool:
        for k, v in keys(r).items():
            if v in dk[k]:
                clash[k] += 1

    def ptitles(r):
        t = r["meta"].get("page_title")
        return set(t) if isinstance(t, list) else ({t} if t else set())
    dt = set().union(*(ptitles(r) for r in dev if r["source"] != "c_pub_quality"))
    clash["page_title"] = sum(1 for r in pool if r["source"] != "c_pub_quality" and ptitles(r) & dt)
    qa_dev = {r["meta"]["text_source"]["record_id"].split("_")[0] for r in dev if r["source"] == "c_pub_quality"}
    clash["quality_article"] = sum(1 for r in pool if r["source"] == "c_pub_quality"
                                   and r["meta"]["text_source"]["record_id"].split("_")[0] in qa_dev)
    return {k: v for k, v in clash.items()}


def bal():
    P = parts()
    pool = P["rows"] + P["reserve"]
    dev = load(DEV)
    res, fail = {}, collections.Counter()
    for scope, rows in (("rows", P["rows"]), ("pool", pool)):
        g10 = g10_set(rows)
        res[f"G10_{scope}"] = g10
        fail.update({f"{k}:{scope}": v for k, v in g10["fail"].items()})
        g12 = g12_set([dict(r) for r in rows])
        res[f"G12_{scope}"] = g12
        fail.update({f"{k}:{scope}": v for k, v in g12["fail"].items()})
        g7 = {}
        for s in sorted({r["source"] for r in rows}):
            g7[s] = g7_set([r for r in rows if r["source"] == s])
            if g7[s]["failing_features"]:
                fail[f"G7:{scope}:{s}"] += g7[s]["failing_features"]
        g7["all_public1"] = g7_set(rows)
        if g7["all_public1"]["failing_features"]:
            fail[f"G7:{scope}:all"] += g7["all_public1"]["failing_features"]
        res[f"G7_{scope}"] = g7
    sep = separation(pool, dev)
    res["dev_separation"] = sep
    if any(sep.values()):
        fail["dev_separation"] += sum(sep.values())
    res["fail"] = dict(fail)
    res["pass"] = not fail
    dump("bal", res)
    log(f"G7/G10/G12/sep pass={res['pass']} fail={dict(fail)}")
    print("BAL", res["pass"], dict(fail))


# ------------------------------------------------------------------ G6
def g6():
    import numpy as np
    from sklearn.decomposition import TruncatedSVD
    from sklearn.ensemble import HistGradientBoostingClassifier
    from sklearn.feature_extraction import DictVectorizer
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GroupKFold

    def lr():
        return LogisticRegression(C=1.0, max_iter=3000, solver="liblinear")

    def gbt():
        return HistGradientBoostingClassifier(max_iter=200, learning_rate=0.08, max_leaf_nodes=31, random_state=0)

    def text_X(texts):
        tv = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=200000, sublinear_tf=True)
        try:
            Xs = tv.fit_transform(texts).tocsr()
        except ValueError:          # empty vocabulary (a constant or empty view)
            return None, None
        nc = max(2, min(64, Xs.shape[1] - 1, Xs.shape[0] - 1))
        if Xs.shape[1] < 3:
            return Xs, Xs.toarray()
        return Xs, TruncatedSVD(nc, random_state=0).fit_transform(Xs)

    def dict_X(ds):
        dv = DictVectorizer()
        X = dv.fit_transform(ds).tocsr()
        return X, X.toarray()

    def cv_rows(Xs, Xd, y, g):
        """row-level label (yes/no): accuracy of LR (sparse) and GBT (dense), 5-fold grouped CV."""
        res = {}
        nf = min(5, len(set(g)))
        for nm, X, mk in (("lr", Xs, lr), ("gbt", Xd, gbt)):
            pred = np.zeros(len(y))
            for tr, te in GroupKFold(nf).split(X, y, g):
                if len(set(y[tr])) < 2:
                    pred[te] = y[tr][0]
                    continue
                pred[te] = mk().fit(X[tr], y[tr]).predict(X[te])
            res[nm] = round(float((pred == y).mean()), 4)
        return res

    def cv_opts(Xs, Xd, yp, prow, g):
        """option-level scoring for choice rows: the top-scored option per row is the prediction (ties split)."""
        res = {}
        nf = min(5, len(set(g)))
        for nm, X, mk in (("lr", Xs, lr), ("gbt", Xd, gbt)):
            sc = np.zeros(len(yp))
            for tr, te in GroupKFold(nf).split(X, yp, g):
                sc[te] = mk().fit(X[tr], yp[tr]).predict_proba(X[te])[:, 1]
            by = collections.defaultdict(list)
            for i, (ri, s) in enumerate(zip(prow, sc)):
                by[ri].append((round(float(s), 9), yp[i]))
            acc = []
            for lst in by.values():
                top = max(s for s, _ in lst)
                tied = [t for s, t in lst if s == top]
                acc.append(sum(tied) / len(tied))
            res[nm] = round(float(np.mean(acc)), 4)
        return res

    def verdict(r, chance, n):
        best = max(r.values())
        return {**r, "chance": round(chance, 4), "best": best, "n": n, "pass": bool(best <= chance + 0.02)}

    P = parts()
    res, fail = {}, collections.Counter()
    qcs, qc_files = [], {}
    for ds in ("squad2", "musique", "2wiki"):
        f = P1 / "tmp" / f"qcs_{ds}.json"
        rs = json.loads(f.read_text())["qc"]
        qc_files[f.name] = {"sha256": sha(f), "rows": len(rs)}
        used = {r["group_id"] for r in P["rows"] + P["reserve"]} | {r["group_id"] for r in load(DEV)}
        assert not any(r["group_id"] in used for r in rs), f"QC sample {ds} shares a group with rows/reserve/dev"
        qcs += rs
    qcs += [r for r in P["rows"] + P["reserve"] if r["source"] == "c_pub_quality"]
    res["qc_sample_files"] = qc_files
    for scope, rows_all in (("qc_sample", qcs), ("pool", P["rows"] + P["reserve"]), ("rows", P["rows"])):
        out = {}
        for s in sorted({r["source"] for r in rows_all}):
            for qt in ("noul", "choice"):
                rs = [r for r in rows_all if r["source"] == s and r["qtype"] == qt]
                if not rs:
                    continue
                g = np.array([r["group_id"] for r in rs])
                cell = {}
                if qt == "noul":
                    y = np.array([int(label_yes(r)) for r in rs])
                    chance = max(y.mean(), 1 - y.mean())
                    views = {"a_question_only": [framing_q(r) + " || " + item_q(r) for r in rs],
                             "c_card_without_question": [r.get("card") or "" for r in rs],
                             "a_question_x_wording": [" ".join(f"{r['meta'].get('wording_id')}_{t}" for t in
                                                               TOK.findall((framing_q(r) + " " + item_q(r)).lower()))
                                                      for r in rs]}
                    for v, texts in views.items():
                        Xs, Xd = text_X(texts)
                        cell[v] = verdict(cv_rows(Xs, Xd, y, g), chance, len(rs)) if Xs is not None else {"constant_view": True, "pass": True}
                    Xs, Xd = dict_X([{f: 1.0 for f in row_meta(r)} | {"statelen": len(r["state"]), "iqlen": len(item_q(r)),
                                                                     "npara": len(paras(r["state"]))} for r in rs])
                    cell["d_metadata_only"] = verdict(cv_rows(Xs, Xd, y, g), chance, len(rs))
                    cell["b_options_only"] = {"constant_view": "Yes/No", "pass": True}
                else:
                    chance = float(np.mean([1 / len(r["options"]) for r in rs]))
                    prow, gp, yp, otext, ometa, qtext, ctext = [], [], [], [], [], [], []
                    for i, r in enumerate(rs):
                        for j, o in enumerate(r["options"]):
                            prow.append(i)
                            gp.append(r["group_id"])
                            yp.append(int(j == gidx(r)))
                            otext.append(o)
                            ometa.append({f: 1.0 for f in opt_meta(r, j)} | {"len": len(o), "words": len(o.split()),
                                         "len_rank": sorted(len(x) for x in r["options"]).index(len(o))})
                            qtext.append(framing_q(r) + " || " + item_q(r) + " || " + o)
                            ctext.append((r.get("card") or "") + " || " + o)
                    gp, yp = np.array(gp), np.array(yp)
                    for v, texts in (("b_options_only", otext), ("a_question_plus_option", qtext),
                                     ("c_card_without_question_plus_option", ctext)):
                        Xs, Xd = text_X(texts)
                        cell[v] = verdict(cv_opts(Xs, Xd, yp, prow, gp), chance, len(rs))
                    Xs, Xd = dict_X(ometa)
                    cell["d_metadata_only"] = verdict(cv_opts(Xs, Xd, yp, prow, gp), chance, len(rs))
                for v, x in cell.items():
                    if not x.get("pass") and scope == "qc_sample":
                        fail[f"G6:{scope}:{s}:{qt}:{v}"] += 1
                    elif not x.get("pass"):
                        res.setdefault("info_fail_small_n", {})[f"{scope}:{s}:{qt}:{v}"] = x["best"]
                out[f"{s}|{qt}"] = cell
                log(f"G6 {scope} {s} {qt} done")
        res[scope] = out
    res["note"] = ("spec 8 G6: accuracy <= chance + 2 pp, 5-fold grouped CV (group_id), LR on tf-idf 1-2 grams and "
                   "GBT on SVD/dense, judged on the separate QC sample (>= 5,000 rows per Wikipedia set from the same "
                   "generators, tmp/qcs_<ds>.json; QuALITY: all its rows + reserve, fewer than 5,000 real rows). "
                   "pool / rows (n < 5,000) are information only")
    res["fail"] = dict(fail)
    res["pass"] = not fail
    dump("g6", res)
    log(f"G6 pass={res['pass']} fail={dict(fail)}")
    print("G6", res["pass"], dict(fail))


if __name__ == "__main__":
    {"g1": g1, "g15": g15, "bal": bal, "g6": g6}[sys.argv[1]]()
