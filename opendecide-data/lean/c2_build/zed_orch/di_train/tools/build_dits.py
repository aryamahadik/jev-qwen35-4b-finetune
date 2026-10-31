"""DI-TS builder (A61): reads the pinned upstream TRAIN files in DI-TS/src (untrusted data; run with python -I), writes staging files in DI-TS/stage.
Deterministic, CPU only, seed 20261013. Drop-only program checks. Usage: python -I tools/build_dits.py <di_train_dir>"""
import sys, os, json, csv, hashlib, random, collections, re
D = sys.argv[1]
sys.path.insert(0, os.path.join(D, "tools"))
import dits_text as T
from le_check import entails
SRC, STAGE = f"{D}/DI-TS/src", f"{D}/DI-TS/stage"
os.makedirs(STAGE, exist_ok=True)
SEED = T.SEED
PINS = json.load(open(f"{D}/DI-TS/SRC_PINS.json"))
CAND_PER_TASK, DEV_PER_TASK = 900, 60            # 1.5 x the 600 max (A42-D 1.3); 300 dev = 5 tasks x 60
sha = lambda s: hashlib.sha256(s.encode()).hexdigest()
def rng(*k): return random.Random(sha(":".join(map(str, (SEED,) + k))))
def words(s): return re.findall(r"\S+", s.lower())

# ---------------- loaders: one record = dict(rid, group, label, sub, a, b)
def load_le():
    out = []
    for i, l in enumerate(open(f"{SRC}/logical_entailment/data__train.txt", encoding="utf8")):
        p = l.strip().split(",")
        A, B, E = p[0], p[1], int(p[2])
        out.append(dict(rid=f"le:{sha(A+'|'+B)[:16]}", group=f"le:{sha(A)[:12]}", label=OPT_LE[E], sub=None, a=A, b=B, line=i))
    return out
OPT_LE = {1: "A entails B", 0: "A does not entail B"}
def load_cs(n):
    out = []; lab = {"Entailment": "entailment", "Contradiction": "contradiction", "Neutral": "neutral", "E": "entailment", "C": "contradiction", "N": "neutral"}
    for r in csv.DictReader(open(f"{SRC}/temporal_nli/data__cs{n}_train.csv", encoding="utf8")):
        sub = r.get("Type") or r.get("Higher Duration Unit")
        out.append(dict(rid=f"cs{n}:{sha(r['Premise']+'|'+r['Hypothesis'])[:16]}", group=f"cs{n}:{sha(r['Premise'])[:12]}", label=lab[r["Label"]], sub=sub, a=r["Premise"], b=r["Hypothesis"], line=int(r[""])))
    return out
def load_ps():
    d = json.load(open(f"{SRC}/perspectrum/data__dataset__perspectrum_with_answers_v1.0.json"))
    sp = json.load(open(f"{SRC}/perspectrum/data__dataset__dataset_split_v1.0.json"))
    pool = {p["pId"]: p for p in json.load(open(f"{SRC}/perspectrum/data__dataset__perspective_pool_v1.0.json"))}
    out = []
    for x in d:
        if sp.get(str(x["cId"])) != "train": continue            # TRAIN split only
        for p in x["perspectives"]:
            lab = {"SUPPORT": "supports", "UNDERMINE": "undermines"}.get(p["stance_label_3"].upper())
            if lab is None: continue
            pid = p["pids"][0]
            out.append(dict(rid=f"ps:{x['cId']}:{pid}", group=f"ps:{x['cId']}", label=lab, sub=x.get("source"), a=x["text"], b=pool[pid]["text"], line=pid))
    return out

TASKS = {
 "logical_entailment": dict(load=load_le, opts=T.LE_OPTS, defs=T.LE_DEFS, instr=T.LE_INSTR, cap=1, domain="propositional logic (program-generated)", method="upstream_program_label (truth-table entailment, Evans et al. 2018 generator)", pk="logical_entailment",
                            reg="symbolic", fmt=lambda r: f"Proposition A: {r['a']}\nProposition B: {r['b']}"),
 "temporal_cs1": dict(load=lambda: load_cs(1), opts=T.NLI_OPTS3, defs=T.NLI_DEFS, instr=T.CS_INSTR["cs1"], cap=1, domain="temporal expressions NLI: order of days, dates and times (template-generated)", method="upstream_program_label (template construction, Thukral et al. 2021)", pk="temporal_nli",
                      reg="template", fmt=lambda r: f"Statement 1: {r['a']}\nStatement 2: {r['b']}"),
 "temporal_cs2": dict(load=lambda: load_cs(2), opts=T.NLI_OPTS2, defs=T.NLI_DEFS, instr=T.CS_INSTR["cs2"], cap=1, domain="temporal expressions NLI: durations (template-generated)", method="upstream_program_label (template construction, Thukral et al. 2021)", pk="temporal_nli",
                      reg="template", fmt=lambda r: f"Statement 1: {r['a']}\nStatement 2: {r['b']}"),
 "temporal_cs3": dict(load=lambda: load_cs(3), opts=T.NLI_OPTS3, defs=T.NLI_DEFS, instr=T.CS_INSTR["cs3"], cap=1, domain="temporal expressions NLI: magnitudes in different units (template-generated)", method="upstream_program_label (template construction, Thukral et al. 2021)", pk="temporal_nli",
                      reg="template", fmt=lambda r: f"Statement 1: {r['a']}\nStatement 2: {r['b']}"),
 "perspectrum": dict(load=load_ps, opts=T.PS_OPTS, defs=T.PS_DEFS, instr=T.PS_INSTR, cap=2, domain="debate claims and perspectives", method="upstream_human_label (crowd stance votes, Chen et al. 2019)", pk="perspectrum",
                      reg="debate", fmt=lambda r: f"Claim: {r['a']}\nPerspective: {r['b']}"),
}
LICENCE = {
 "logical_entailment": ("Apache-2.0", "google-deepmind/logical-entailment-dataset", "Apache License, Version 2.0 (repo LICENSE)"),
 "temporal_nli": ("CC0-1.0", "kunalkukreja21/temporal-expressions-evaluation-lm", "CC0 1.0 Universal (repo LICENSE)"),
 "perspectrum": ("CC BY-SA 4.0", "CogComp/perspectrum", "Attribution-ShareAlike 4.0 International (data/dataset/license.txt)")}

def card_variants(opts, defs, k=16):
    combos = [(i,) for i in range(4)]
    allc = [c for c in __import__("itertools").product(range(4), repeat=len(opts))]
    r = random.Random(SEED); r.shuffle(allc)
    return allc[:k]

def near_key(s): 
    w = words(s); return {" ".join(w[i:i+3]) for i in range(max(1, len(w)-2))}

def balanced_sample(recs, n, r, cap):
    """label-balanced, round-robin over sub buckets, <= cap per group; returns list."""
    labs = sorted({x["label"] for x in recs}); per = {l: n // len(labs) for l in labs}
    for l in labs[: n - sum(per.values())]: per[l] += 1
    chosen = []; used = collections.Counter()
    for l in labs:
        by = collections.defaultdict(list)
        for x in recs:
            if x["label"] == l: by[x["sub"]].append(x)
        for v in by.values(): r.shuffle(v)
        keys = sorted(by, key=str); r.shuffle(keys)
        got = 0; idx = {k: 0 for k in keys}
        while got < per[l] and any(idx[k] < len(by[k]) for k in keys):
            for k in keys:
                while idx[k] < len(by[k]):
                    x = by[k][idx[k]]; idx[k] += 1
                    if used[x["group"]] < cap:
                        used[x["group"]] += 1; chosen.append(x); got += 1; break
                if got >= per[l]: break
    return chosen

def make_row(task, spec, rec, dev, wi, ci):
    rid = "c2_dits:" + sha(task + "|" + rec["rid"])[:14]
    r = rng("row", rec["rid"])
    opts = list(spec["opts"]); r.shuffle(opts)                       # gold position uniform by a seeded shuffle
    instr = spec["instr"][wi]
    combos = card_variants(spec["opts"], spec["defs"])
    # card lists options in the displayed order
    idx = {o: combos[ci][i] for i, o in enumerate(spec["opts"])}
    card = "\n".join(f"- {o}: {spec['defs'][o][idx[o]]}" for o in opts)
    lic = LICENCE[spec["pk"]]
    meta = {"family": "DI-TS", "spec_id": "DI-TS.v1", "card_id": f"dits:{task}:c{ci}", "domain_pack": None, "sampler": "S5" if dev else None,
            "gen_version": "c2-di-ts 1.0 (17 Oct 2026, A61)", "git_sha": "uncommitted", "seed": SEED, "structure_hash": sha(spec["fmt"](rec))[:16],
            "difficulty_bin": None, "crowd_pg": None, "depth": 0, "deep": False, "format_style": "pair", "wording_id": f"{task}:w{wi}", "defs_style": "rules_in_card",
            "twin_of": None, "twin_kind": None, "text_source": spec["pk"], "licence": lic[0], "edge": [], "qform": task, "dev_only": bool(dev),
            "c2": {"author_mode": "T", "skin_id": f"DI-TS-{task}", "register": spec["reg"], "lexicon_ids": [], "haiku_task_id": None, "haiku_prompt_sha": None, "twin_kind": None, "twin_of": None, "closed_world": True},
            "source": "c2_dits", "task_id": f"dits:{task}", "domain": spec["domain"], "gold_method": spec["method"], "record_id": rec["rid"],
            "licence_url": f"https://github.com/{lic[1]}", "licence_record": lic[2], "upstream_commit": PINS[spec["pk"]]["commit"], "src_group": rec["group"], "sub": rec["sub"]}
    return {"id": rid, "group_id": "c2_dits:g:" + sha(rec["group"])[:12], "call_id": rid, "source": "c2_dits", "state": spec["fmt"](rec), "qtype": "choice", "instructions": instr,
            "options": opts, "gold": rec["label"], "role": "base", "card": card, "meta": meta}

def main():
    rep = {"seed": SEED, "tasks": {}}; dev_rows, cand_rows = [], []
    for task, spec in TASKS.items():
        recs = spec["load"](); n0 = len(recs)
        # exact dedupe on source record (one row per source record)
        seen = set(); u = []
        for x in recs:
            if x["rid"] in seen: continue
            seen.add(x["rid"]); u.append(x)
        dropped = {"exact_dup": n0 - len(u)}
        if task == "temporal_cs3":                  # upstream template bug: 'minutess' (8,628 of 42,240 rows): drop-only text-defect check
            ok = [x for x in u if "minutess" not in x["a"] + x["b"]]
            dropped["upstream_text_defect_minutess"] = len(u) - len(ok); u = ok
        # program gold check (LE only): drop-only
        if task == "logical_entailment":
            ok = []; bad = 0
            for x in u:
                e, _ = entails(x["a"], x["b"])
                if (OPT_LE[1] if e else OPT_LE[0]) == x["label"]: ok.append(x)
                else: bad += 1
            dropped["le_truth_table_mismatch"] = bad; u = ok
        # dev first (held-out groups, stratified by label), before any read
        r = rng("dev", task); groups = sorted({x["group"] for x in u}); r.shuffle(groups)
        by_group = collections.defaultdict(list)
        for x in u: by_group[x["group"]].append(x)
        labs = sorted({x["label"] for x in u}); per = {l: DEV_PER_TASK // len(labs) for l in labs}
        for l in labs[: DEV_PER_TASK - sum(per.values())]: per[l] += 1
        dev = []; devg = set(); got = collections.Counter()
        for g in groups:
            c = [x for x in by_group[g] if got[x["label"]] < per[x["label"]]]
            if c:
                x = r.choice(c); dev.append(x); devg.add(g); got[x["label"]] += 1
            if len(dev) >= DEV_PER_TASK: break
        # remove dev groups, and (LE) every record sharing a formula with a dev record
        devforms = {s for x in dev for s in (x["a"], x["b"])} if task == "logical_entailment" else set()
        pool = [x for x in u if x["group"] not in devg and not ({x["a"], x["b"]} & devforms)]
        pool_n = len(pool)
        r2 = rng("cand", task); pool.sort(key=lambda x: x["rid"])
        cands = balanced_sample(pool, CAND_PER_TASK, r2, spec["cap"])
        # near-duplicate drop (word 3-gram Jaccard >= 0.9 within the task's candidates and vs dev)
        keep = []; sig = []; nd = 0
        for x in dev + cands:
            k = near_key(spec["fmt"](x)); isdup = False
            for k2 in sig:
                if len(k & k2) / max(1, len(k | k2)) >= 0.9: isdup = True; break
            if isdup and x in cands: nd += 1; continue
            sig.append(k); keep.append(x)
        cands = [x for x in keep if x in cands]
        dropped["near_duplicate"] = nd
        def assign(lst, tag):
            order = list(range(len(lst))); rng("assign", task, tag).shuffle(order)
            o2 = list(range(len(lst))); rng("assign2", task, tag).shuffle(o2)
            w, c = {}, {}
            for pos, i in enumerate(order): w[i] = pos % len(spec["instr"])
            for pos, i in enumerate(o2): c[i] = pos % 16
            return w, c
        for lst, out, isdev, tag in ((dev, dev_rows, True, "dev"), (cands, cand_rows, False, "cand")):
            w, c = assign(lst, tag)
            for i, x in enumerate(lst): out.append(make_row(task, spec, x, isdev, w[i], c[i]))
        rep["tasks"][task] = {"source_records": n0, "after_exact_dedupe": len(u), "dev_groups": len(devg), "pool_after_dev_removal": pool_n, "dev_rows": len(dev), "candidate_rows": len(cands), "drops": dropped,
                              "cand_label_counts": dict(collections.Counter(x["label"] for x in cands)), "dev_label_counts": dict(collections.Counter(x["label"] for x in dev))}
    def wr(path, rows):
        with open(path, "w", encoding="utf8") as f:
            for x in rows: f.write(json.dumps(x, ensure_ascii=False) + "\n")
        return sha(open(path, encoding="utf8").read())
    rep["files"] = {"candidates_stage.jsonl": {"rows": len(cand_rows), "sha256": wr(f"{STAGE}/candidates_stage.jsonl", cand_rows)},
                    "mixdev_S5_stage.jsonl": {"rows": len(dev_rows), "sha256": wr(f"{STAGE}/mixdev_S5_stage.jsonl", dev_rows)}}
    json.dump(rep, open(f"{STAGE}/BUILD_REPORT.json", "w"), indent=1)
    print(json.dumps({k: (v if k != "tasks" else {t: {a: b for a, b in d.items() if a in ("source_records","candidate_rows","dev_rows","drops","cand_label_counts")} for t, d in v.items()}) for k, v in rep.items()}, indent=1))
main()
