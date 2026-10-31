"""build_di_lang.py: the C2 block DI-LANG (HoVer yes/no + iSarcasmEval task A yes/no and task C 2-option choice). Ruling A61 (b), (c) 5-9, (d), (f).

Run: python -B build_di_lang.py build   (Mac venv python; trusted code imports c2_kit; the downloaded files are read as plain json / csv only)

Deterministic, CPU only, seed 20261013. Reads  DI-LANG/src/** (untrusted) and DI-LANG/work/hotpot_needed.json; writes  DI-LANG/work/build/**.
Nothing here opens a bench/external_quarantine path: the DI exclusion list is the hashed export c2_build/g13_di/record_ids.json (hashes only).
"""
from __future__ import annotations

import csv
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                                  # .../DI-LANG
C2B = ROOT.parents[2]                                # lean/c2_build
sys.path[:0] = [str(HERE), str(C2B)]
import di_lang_lib as L  # noqa: E402
from c2_kit import rows as R  # noqa: E402

SRC, WORK = ROOT / "src", ROOT / "work"
OUT = WORK / "build"
FAMILY = "DI-LANG"
HOVER_MAX, SARC_MAX = 2400, 1200
CAND_X = 1.5
HOVER_CAND = int(HOVER_MAX * CAND_X)               # 3,600 = 1,800 yes + 1,800 no
HOVER_DEV, SARC_DEV = 150, 150
SARC_C_SHARE = 0.35                                 # task C share of the candidates (cap 0.40 of the source, A61 d)
HOP_QUOTA = {2: 870, 3: 620, 4: 310}               # per label; sums to HOVER_CAND / 2
MAX_PER_GROUP = 2                                   # HoVer claims per origin group (hpqa_id) among candidates
TOK_CAP = 2000


# ------------------------------------------------------------------ DI exclusion pre-filter (hashes only; the G13 run itself is separate)
def load_di_ids():
    import di_g13
    ids = json.loads((C2B / "g13_di" / "record_ids.json").read_text(encoding="utf-8"))
    return di_g13, {k: set(v) for k, v in ids.items()}


def near_dup_drop(texts: dict, thr: float = 0.85, k: int = 5) -> set:
    """ids to drop: the later of a pair whose word-5-gram shingle Jaccard >= thr (stand-in for MinHash; exact here). texts: {id: text}"""
    sh = {}
    for i, t in texts.items():
        w = re.findall(r"\w+", t.lower())
        sh[i] = {hash(" ".join(w[j:j + k])) for j in range(max(1, len(w) - k + 1))}
    post = defaultdict(list)
    for i in sorted(sh):
        for s in sh[i]:
            post[s].append(i)
    drop, seen_pairs = set(), set()
    for i in sorted(sh):
        if i in drop:
            continue
        cand = Counter()
        for s in sh[i]:
            p = post[s]
            if len(p) <= 60:
                for j in p:
                    if j > i:
                        cand[j] += 1
        for j, c in cand.items():
            if j in drop:
                continue
            inter = c
            jac = inter / (len(sh[i]) + len(sh[j]) - inter)
            if jac >= thr:
                drop.add(j)
    return drop


# ------------------------------------------------------------------ row assembly
def base_meta(task_id, wording_id, card_id, qform, licence, text_source, *, dev, edge, extra, struct, defs_style):
    return {"family": FAMILY, "spec_id": f"{FAMILY}.{task_id}.v1", "card_id": card_id, "domain_pack": None,
            "sampler": "S5" if dev else FAMILY, "gen_version": "c2_di_lang 1.0 (17 Oct 2026)", "git_sha": "uncommitted", "seed": L.SEED,
            "structure_hash": struct, "difficulty_bin": None, "crowd_pg": None, "depth": 0, "deep": False,
            "format_style": "real-text/" + qform, "wording_id": wording_id, "defs_style": defs_style, "twin_of": None, "twin_kind": None,
            "text_source": text_source, "licence": licence, "edge": sorted(set(edge)), "qform": qform, "dev_only": bool(dev),
            "c2": {"author_mode": "T", "skin_id": wording_id, "register": "real-text", "lexicon_ids": [], "haiku_task_id": None,
                   "haiku_prompt_sha": None, "twin_kind": None, "twin_of": None, "closed_world": True},
            "task_id": task_id, "gold_method": "upstream_human_label", **extra}


def make_row(src, rid_key, gk, state, qtype, instr, options, gold, card, meta):
    rid = f"{src}:{L.sha(rid_key)[:16]}"
    return {"id": rid, "group_id": f"{src}:g:{L.sha(gk)[:14]}", "call_id": f"{src}:{L.sha(rid)[:12]}", "source": src, "state": state,
            "qtype": qtype, "instructions": instr, "options": options, "gold": gold, "role": "base", "card": card, "meta": meta}


# ------------------------------------------------------------------ HoVer
def hover_rows(drops: Counter):
    hov = json.loads((SRC / "hover" / "hover_train_release_v1.1.json").read_text(encoding="utf-8"))
    wiki = json.loads((WORK / "hotpot_needed.json").read_text(encoding="utf-8"))
    di, ids = load_di_ids()
    seen_claim = set()
    pool = []
    for r in hov:
        claim = L.ws(r["claim"])
        if r["label"] not in ("SUPPORTED", "NOT_SUPPORTED"):
            drops["hover:label_unknown"] += 1
            continue
        if r["uid"] in ids["hover_uid"] or r["hpqa_id"] in ids["hover_group"] or di.sha_hex(di.norm(claim)) in ids["hover_claim_sha256"]:
            drops["hover:di_record_id_prefilter"] += 1
            continue
        if claim.lower() in seen_claim:
            drops["hover:exact_duplicate_claim"] += 1
            continue
        seen_claim.add(claim.lower())
        by_title = defaultdict(set)
        bad = None
        for t, i in r["supporting_facts"]:
            sents = wiki.get(t)
            if sents is None:
                bad = "hover:evidence_title_missing"
                break
            if not (0 <= i < len(sents)) or not sents[i].strip():
                bad = "hover:evidence_sentence_missing"
                break
            by_title[t].add(i)
        if bad:
            drops[bad] += 1
            continue
        titles = sorted(by_title, key=lambda t: L.uh("title-order", r["uid"], t))
        passages = [(t, " ".join(L.ws(wiki[t][i]) for i in sorted(by_title[t]))) for t in titles]
        state = "Claim: " + claim + "\n\nPassages:\n\n" + "\n\n".join(f"[{t}]\n{p}" for t, p in passages)
        pool.append({"uid": r["uid"], "hpqa": r["hpqa_id"], "claim": claim, "label": r["label"], "hops": r["num_hops"], "state": state,
                     "n_sent": sum(len(v) for v in by_title.values()), "n_titles": len(by_title), "sf": r["supporting_facts"]})
    # token cap: the state is the gold sentences only, so there is nothing to cut; a row over the cap is dropped
    keep = []
    for p in pool:
        if math.ceil((len(p["state"]) + 2 * 60) / R.CHARS_PER_TOKEN) > TOK_CAP:
            drops["hover:over_2000_tokens"] += 1
        else:
            keep.append(p)
    nd = near_dup_drop({p["uid"]: p["claim"] for p in keep})
    drops["hover:near_duplicate_claim"] += len(nd)
    keep = [p for p in keep if p["uid"] not in nd]
    return keep


def hover_split(pool):
    """Own dev = whole origin groups drawn first (seeded); candidates: <= MAX_PER_GROUP per group, 50% yes."""
    groups = defaultdict(list)
    for p in pool:
        groups[p["hpqa"]].append(p)
    order = sorted(groups, key=lambda g: L.uh("hover-dev-group", g))
    dev_groups, dev_pool = [], []
    for g in order:
        dev_groups.append(g)
        dev_pool += groups[g]
        if len(dev_pool) >= 260:
            break
    ys = sorted([p for p in dev_pool if p["label"] == "SUPPORTED"], key=lambda p: L.uh("hover-dev-pick", p["uid"]))[:HOVER_DEV // 2]
    ns = sorted([p for p in dev_pool if p["label"] != "SUPPORTED"], key=lambda p: L.uh("hover-dev-pick", p["uid"]))[:HOVER_DEV // 2]
    dev = ys + ns
    dev_set = set(dev_groups)
    train = [p for p in pool if p["hpqa"] not in dev_set]
    by_g = defaultdict(list)
    for p in sorted(train, key=lambda p: L.uh("hover-cand", p["uid"])):
        by_g[p["hpqa"]].append(p)
    capped = [p for g in by_g.values() for p in g[:MAX_PER_GROUP]]
    capped.sort(key=lambda p: L.uh("hover-cand-order", p["uid"]))
    # label x hops quotas (the same hop mix for yes and no, so the number of passages carries no label signal): 870 / 620 / 310 per label for 2 / 3 / 4 hops
    y, n = [], []
    for h, q in HOP_QUOTA.items():
        y += [p for p in capped if p["label"] == "SUPPORTED" and p["hops"] == h][:q]
        n += [p for p in capped if p["label"] != "SUPPORTED" and p["hops"] == h][:q]
    return dev, sorted(y + n, key=lambda p: L.uh("hover-final-order", p["uid"])), dev_set, len(train)


def hover_to_rows(items, dev):
    out = []
    order = sorted(items, key=lambda p: L.uh("hover-assign", p["uid"]))
    for k, p in enumerate(order):
        w = k % len(L.HOVER_Q)                                           # exact round-robin: each wording 20%
        yi, ni = L.uh("hover-card-y", p["uid"]) % len(L.HOVER_YES), L.uh("hover-card-n", p["uid"]) % len(L.HOVER_NO)
        cid = f"di_lang.hover:y{yi}n{ni}"
        edge = [f"hops{p['hops']}", f"titles{min(p['n_titles'], 4)}"] + (["long_evidence"] if len(p["state"]) > 1500 else [])
        meta = base_meta(L.HOVER_TASK, f"HV_Q{w}", cid, "HV_SUPPORT", L.HOVER_LICENCE,
                         "hover-nlp/hover train (39b84697) + HotpotQA 2017 Wikipedia abstracts", dev=dev, edge=edge,
                         extra={"uid": p["uid"], "hpqa_id": p["hpqa"], "source_record_id": p["uid"], "num_hops": p["hops"],
                                "label_src": p["label"]},
                         struct=L.sha(p["state"])[:16], defs_style="rules_in_card")
        out.append(make_row("c2_di_hover", "hover|" + p["uid"], "hover|" + p["hpqa"], p["state"], "noul", L.HOVER_Q[w], None,
                            1 if p["label"] == "SUPPORTED" else 0, L.card(L.HOVER_YES[yi], L.HOVER_NO[ni]), meta))
    return out


# ------------------------------------------------------------------ iSarcasmEval (English train)
def sarc_pool(drops: Counter):
    di, ids = load_di_ids()
    raw = list(csv.DictReader(open(SRC / "isarc" / "train.En.csv", encoding="utf-8", newline="")))
    pool, seen = [], set()
    for k, r in enumerate(raw):
        tw = r["tweet"].strip()
        if not tw:
            drops["isarcasm:empty_tweet"] += 1
            continue
        key = L.ws(tw).lower()
        if key in seen:
            drops["isarcasm:exact_duplicate_tweet"] += 1
            continue
        seen.add(key)
        if di.sha_hex(di.norm(tw)) in ids["isarcasm_text_sha256"] or (r["rephrase"].strip() and di.sha_hex(di.norm(r["rephrase"])) in ids["isarcasm_text_sha256"]):
            drops["isarcasm:di_record_id_prefilter"] += 1
            continue
        sar = int(r["sarcastic"])
        reph = L.ws(r["rephrase"]) if r["rephrase"].strip() else ""
        if sar and (not reph or reph.lower() == key):
            drops["isarcasm:sarcastic_without_distinct_rephrase"] += 1
            sar_c_ok = False
        else:
            sar_c_ok = bool(sar)
        cats = [c for c in ("sarcasm", "irony", "satire", "understatement", "overstatement", "rhetorical_question") if r.get(c) == "1"]
        pool.append({"rec": f"isarc_train_en_{k}", "tweet": tw, "tweet1": L.ws(tw), "sar": sar, "reph": reph, "c_ok": sar_c_ok, "cats": cats,
                     "nl": "\n" in tw})
    nd = near_dup_drop({p["rec"]: p["tweet1"] for p in pool}, thr=0.85)
    drops["isarcasm:near_duplicate_tweet"] += len(nd)
    return [p for p in pool if p["rec"] not in nd]


def sarc_split(pool):
    """Own dev: 150 records (task A 49 yes + 49 no, task C 52). Candidates: every other sarcastic record is used once (A-yes or C), A-no matches A-yes."""
    sar = sorted([p for p in pool if p["sar"] and p["c_ok"]], key=lambda p: L.uh("sarc-order", p["rec"]))
    non = sorted([p for p in pool if not p["sar"]], key=lambda p: L.uh("sarc-order", p["rec"]))
    nc_dev = round(SARC_DEV * SARC_C_SHARE)                           # 52
    na_dev = SARC_DEV - nc_dev                                        # 98 -> 49 yes + 49 no
    dev_c, sar = sar[:nc_dev], sar[nc_dev:]
    dev_ay, sar = sar[:na_dev // 2], sar[na_dev // 2:]
    dev_an, non = non[:na_dev // 2], non[na_dev // 2:]
    # candidates: s sarcastic records left -> c task C + y task A yes, y task A no, c = SHARE * N, N = 2y + c
    s = len(sar)
    y = int(s / (1 + (SARC_C_SHARE / (1 - SARC_C_SHARE)) * 2))        # y + c = s with c = 2y * share/(1-share)
    c = s - y
    # exact N and share: c / (2y + c) must be <= SARC_C_SHARE
    while c / (2 * y + c) > SARC_C_SHARE + 1e-9:
        y += 1
        c = s - y
    cand_c, cand_ay = sar[:c], sar[c:c + y]
    cand_an = non[:y]
    return {"dev": {"C": dev_c, "Ay": dev_ay, "An": dev_an}, "cand": {"C": cand_c, "Ay": cand_ay, "An": cand_an}}


def sarc_rows(parts, dev):
    out = []
    allp = [("C", p) for p in parts["C"]] + [("A", p) for p in parts["Ay"] + parts["An"]]
    order = sorted(allp, key=lambda t: L.uh("sarc-assign", t[0], t[1]["rec"]))
    cnt = Counter()
    for k, (kind, p) in enumerate(order):
        cnt[kind] += 1
        j = cnt[kind] - 1                                            # per-task round-robin: exact 20% wordings, 50% gold positions
        if kind == "A":
            w = j % len(L.SARC_A_Q)
            pre = L.SARC_A_PREFIX[L.uh("sarc-prefix", p["rec"]) % len(L.SARC_A_PREFIX)]
            yi, ni = L.uh("sarc-card-y", p["rec"]) % len(L.SARC_A_YES), L.uh("sarc-card-n", p["rec"]) % len(L.SARC_A_NO)
            edge = (["has_newline"] if p["nl"] else []) + [f"cat_{c}" for c in p["cats"]]
            meta = base_meta(L.SARC_A_TASK, f"SA_Q{w}", f"di_lang.isarcasm.A:y{yi}n{ni}", "SA_SARCASM", L.SARC_LICENCE,
                             "iabufarha/iSarcasmEval train.En.csv (dfc708b)", dev=dev, edge=edge,
                             extra={"source_record_id": p["rec"], "record_id": p["rec"], "label_src": "sarcastic=%d" % p["sar"], "task_kind": "A"},
                             struct=L.sha(p["tweet"])[:16], defs_style="rules_in_card")
            out.append(make_row("c2_di_isarcasm", "isarc|" + p["rec"], "isarc|" + p["rec"], f"{pre} {p['tweet']}", "noul",
                                L.SARC_A_Q[w], None, p["sar"], L.card(L.SARC_A_YES[yi], L.SARC_A_NO[ni]), meta))
        else:
            w = j % len(L.SARC_C_Q)
            si = L.uh("sarc-cstate", p["rec"]) % len(L.SARC_C_STATE)
            first_gold = (j % 2 == 0)
            sa, pl = p["tweet1"], p["reph"]
            opts = [sa, pl] if first_gold else [pl, sa]
            edge = ["task_C"] + [f"cat_{c}" for c in p["cats"]] + (["whitespace_normalised"] if p["nl"] else [])
            meta = base_meta(L.SARC_C_TASK, f"SC_Q{w}", None, "SC_PICK", L.SARC_LICENCE,
                             "iabufarha/iSarcasmEval train.En.csv (dfc708b)", dev=dev, edge=edge,
                             extra={"source_record_id": p["rec"], "record_id": p["rec"], "label_src": "sarcastic tweet vs author rephrase",
                                    "task_kind": "C", "gold_pos": 0 if first_gold else 1},
                             struct=L.sha(sa + "|" + pl)[:16], defs_style="rules_in_state")
            out.append(make_row("c2_di_isarcasm", "isarc|" + p["rec"], "isarc|" + p["rec"], L.SARC_C_STATE[si], "choice", L.SARC_C_Q[w],
                                opts, sa, None, meta))
    return out


# ------------------------------------------------------------------ main
def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def validate(rows):
    probs = defaultdict(list)
    for r in rows:
        r2 = json.loads(json.dumps(r))
        r2["meta"]["licence"] = R.LICENCE                           # validate_row pins the family licence string; the block's licences are per source
        for p in R.validate_row(r2, training=not r["meta"]["dev_only"]):
            probs[p].append(r["id"])
    return probs


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    drops = Counter()
    pool = hover_rows(drops)
    hdev, hcand, dev_groups, n_train_pool = hover_split(pool)
    sp = sarc_pool(drops)
    parts = sarc_split(sp)
    rows_c = hover_to_rows(hcand, False) + sarc_rows(parts["cand"], False)
    rows_d = hover_to_rows(hdev, True) + sarc_rows(parts["dev"], True)
    probs = validate(rows_c + rows_d)
    ids = Counter(r["id"] for r in rows_c + rows_d)
    dup_ids = [i for i, c in ids.items() if c > 1]
    write_jsonl(OUT / "candidates_raw.jsonl", rows_c)
    write_jsonl(OUT / "dev_raw.jsonl", rows_d)
    rep = {"hover_pool_after_filters": len(pool), "hover_train_pool_after_dev_groups": n_train_pool, "hover_dev_groups": len(dev_groups),
           "hover_candidates": len(hcand), "hover_dev": len(hdev), "sarc_pool": len(sp),
           "sarc_cand_counts": {k: len(v) for k, v in parts["cand"].items()}, "sarc_dev_counts": {k: len(v) for k, v in parts["dev"].items()},
           "candidates": len(rows_c), "dev": len(rows_d), "drops": dict(drops), "validate_problems": {k: len(v) for k, v in probs.items()},
           "duplicate_ids": len(dup_ids)}
    (OUT / "build_report.json").write_text(json.dumps(rep, indent=1), encoding="utf-8")
    print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    if sys.argv[1:] == ["build"]:
        main()
    else:
        raise SystemExit("usage: build_di_lang.py build")
