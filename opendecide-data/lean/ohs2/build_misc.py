"""OHS-2 part "misc" (track U): five public decision tasks from different domains, none of them trained on, used for dev,
used in OHS-1, or reported as a benchmark by GLiClass (the model family Jev appears to build on). None is a
tasksource/zero-shot-label-nli task, but IBM-ArgQ arguments are partly bundled there (Touche23-ValueEval), so every
candidate item found in a label-nli premise is dropped (see argq_stance).

  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python ohs2/build_misc.py

Output: data/ohs2_parts/misc.jsonl (rows) and ohs2/misc_summary.json (per-task counts, licences, skips, audits).

TASKS (all sampled from the labelled TEST split; seed 20261010; equal per-class quotas, so no class exceeds 40%)
  moral_stories      demelin/moral_stories, classification/action+context/norm_distance (MIT). Norm + situation +
                     intention + one action; yes/no "does the action observe the norm" (normative vs divergent action).
                     One action per story (alternating by rank), 60 normative / 60 divergent.
  argq_stance        ibm-research/argument_quality_ranking_30k test (CC-BY-SA 3.0 per card text; HF tag cc-by-3.0).
                     Topic + crowd argument; yes/no "does the argument support the topic" (stance_WA 1 pro / -1 con);
                     only stance_WA_conf >= 0.8; topics interleaved round-robin; 60 pro / 60 con.
                     NOTE: ~5.5k IBM-ArgQ arguments (1,037 of the 5,818 filtered test arguments) are bundled, with a
                     stance label, in tasksource/zero-shot-label-nli task "Touche23-ValueEval" (a forbidden source).
                     Every candidate is therefore scanned against all label-nli premises and dropped on any hit.
  tabfact            TabFact (wenhuchen/Table-Fact-Checking, MIT repo; HF card CC-BY-4.0; tables from Wikipedia).
                     Raw test tables (data/test_id.json) + raw annotated statements (collected_data r1/r2, not the
                     lemmatised HF text); yes/no "is the statement entailed by the table". One statement per table,
                     60 entailed / 60 refuted. Only tables whose raw statements align one-to-one (same count, same
                     label sequence) with the official test release (tokenized_data/test_examples.json) are used: in
                     18 test tables the release dropped raw statements (e.g. "70 + 68 + 70 = 208" ones), and those
                     dropped statements are not part of the official test set.
  big_patent_cpc     NortheasternUniversity/big_patent test (CC-BY-4.0), abstract only; which CPC section (8-way,
                     A-H; section Y dropped, see SKIPPED). Options are the official CPC section titles; the card lists
                     the official CPC class titles of each section (USPTO CPC scheme pages, cached in
                     ohs2/cpc_classes.json on first run). 15 per section.
  medical_abstracts  TimSchopf/medical_abstracts test (CC-BY-SA 3.0, LICENSE in sebischair/Medical-Abstracts-TC-Corpus).
                     Which of the 5 official patient-condition classes; no official label descriptions exist, so
                     card = null. 24 per class.

No LLM-written text: states are the datasets' own texts under their own field names ("Norm:", "Topic:", ...),
options/cards are official label names and official descriptions; instructions are one fixed question per task built
from the official task/label wording (listed in INSTR). Tables are re-joined with " | " instead of "#" (formatting only).

Filters, in rank order (the final set is the first k items by seeded rank that pass): state 20-6,000 characters;
no double-encoded UTF-8 (mojibake) in the source text (hits a few TabFact tables);
exact-duplicate texts dropped (all copies if their labels conflict); no 12-word run shared with any text we trained or
selected on (every data/**/*.jsonl except OHS files); no 12-word run shared with GLiClass training data
(knowledgator/gliclass-v2.0, GLIClass-v1.0, gliclass-v3-logic-dataset), so neither side has seen the items; no 12-word
run shared with any tasksource/zero-shot-label-nli premise (forbidden source). In all three scans the item's core text
(action / argument / statement / abstract) of 6-11 words must also not occur as a contiguous run in any scanned text
(12-word runs cannot catch short arguments or statements).
"""
import argparse
import hashlib
import html
import json
import random
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import httpx
import pyarrow.parquet as pq
from huggingface_hub import HfFileSystem, hf_hub_download

HERE = Path(__file__).resolve().parent          # lean/ohs2
LEAN = HERE.parent
D = LEAN / "data"
OUT = D / "ohs2_parts" / "misc.jsonl"
SUMMARY = HERE / "misc_summary.json"
CPC_CACHE = HERE / "cpc_classes.json"
SEED = 20261010
N_PER_TASK = 120
MIN_CH, MAX_CH = 20, 6000
GRAM = 12

REV = {
    "demelin/moral_stories": "b830cf56eb00bc4edd1860dd544a192216eb3587",
    "ibm-research/argument_quality_ranking_30k": "590726b3765b1b90c5e53a17e3b1f77d92d3aa8a",
    "NortheasternUniversity/big_patent": "2a5336492ddc4e21cebd3865fd2a7e8b070bfede",
    "TimSchopf/medical_abstracts": "d6afbd7ff4eb215db2470980023d7d7a3dfee7dc",
    "wenhuchen/Table-Fact-Checking": "2ab782ba42b5808076ac91fec846473aa5315a79",  # GitHub commit
    "knowledgator/gliclass-v2.0": "93d3cdc82257a9e821f4b21d08e3dc81979bb653",
    "knowledgator/GLIClass-v1.0": "b0047758976bc0a911882e1722ff8d888a6acdd0",
    "knowledgator/gliclass-v3-logic-dataset": "ee8e07d42c1f95a4421ae78498eec23aec74f1d7",
    "tasksource/zero-shot-label-nli": "ee693dba923b5d5484aa9232b7357c5e45dd39b8",
}
ZSL_FILES = ["data/train-00000-of-00002-970172c89e89b5df.parquet", "data/train-00001-of-00002-509e762f01abeb95.parquet",
             "data/validation-00000-of-00001-79d9ba1d8f02bef0.parquet", "data/test-00000-of-00001-c260d1ee78ad6397.parquet"]
CORE_MIN_WORDS = 6  # shorter core texts are too generic to count as an item match
LICENCE = {
    "moral_stories": "MIT (HF card and GitHub demelin/moral_stories)",
    "argq_stance": "CC-BY-SA 3.0 (card licensing text: (c) IBM 2014, CC-BY-SA 3.0; HF metadata tag cc-by-3.0)",
    "tabfact": "CC-BY-4.0 (HF card); MIT (GitHub repo); tables from Wikipedia (CC-BY-SA)",
    "big_patent_cpc": "CC-BY-4.0 (HF card); CPC titles from USPTO CPC scheme pages (US government work)",
    "medical_abstracts": "CC-BY-SA 3.0 (HF card and LICENSE file in GitHub sebischair/Medical-Abstracts-TC-Corpus)",
}
INSTR = {
    "moral_stories": "Does the action observe the norm?",
    "argq_stance": "Does the argument support the topic?",
    "tabfact": "Is the statement entailed by the table?",
    "big_patent_cpc": "Which CPC section does this patent belong to?",
    "medical_abstracts": "Which class of patient condition does this medical abstract describe?",
}
# official descriptions, verbatim from the dataset cards (see each task's docstring line)
CARD = {
    # HF card "Dataset Summary" of demelin/moral_stories
    "moral_stories": ("- normative action: An action by the actor that fulfills the intention and observes the norm.\n"
                      "- divergent action: An action by the actor that fulfills the intention and diverges from the norm."),
    # HF card of the IBM dataset: "asked to contribute one supporting and one contesting argument", "stance ... (pro or con)"
    "argq_stance": "- pro: supporting argument\n- con: contesting argument",
    # TabFact README: statements "are classified as ENTAILED and REFUTED" (no longer definitions exist)
    "tabfact": None,
    "medical_abstracts": None,
}
CPC_SECTIONS = "ABCDEFGH"  # Y dropped (cross-sectional tagging, see SKIPPED)
MED_LABELS = {1: "neoplasms", 2: "digestive system diseases", 3: "nervous system diseases", 4: "cardiovascular diseases",
              5: "general pathological conditions"}  # the dataset's own "labels" subset (checked at load)
SKIPPED = {
    "ETHICS (hendrycks/ethics)": "bundled in tasksource/zero-shot-label-nli (ethics/commonsense, deontology, justice, "
                                 "virtue), a forbidden source; replaced by Moral Stories (MIT)",
    "20 Newsgroups": "reported as a zero-shot benchmark on the GLiClass v3 model cards (Jev side benchmark-exposed); "
                     "no clear licence (SetFit copy has none); replaced by BigPatent CPC sections",
    "SNIPS (and snips_built_in_intents)": "used in our dev_zs (benayas/snips), in the tasksource label-nli bundle and "
                                          "trained on (tbz_snips_built_in_intents), and a GLiClass v3 benchmark",
    "ATIS": "LDC-distributed; licence of the HF copies unclear",
    "FOMC hawkish/dovish (gtfintechlab)": "CC-BY-NC 4.0 (non-commercial)",
    "LIAR": "in the tasksource label-nli bundle; licence unknown; label depends on outside facts",
    "SciCite / ACL-ARC citation intent": "in the tasksource label-nli bundle and trained on (tbz_scicite, "
                                         "tbz_citation_intent)",
    "PUBHEALTH (health_fact)": "in the tasksource label-nli bundle and trained on (tbz_health_fact)",
    "Climate-FEVER": "licence not stated anywhere (HF card 'unknown')",
    "SciFact / AVeriTeC": "non-commercial licences",
    "WiCE": "evidence is Common Crawl web text under third-party copyright",
    "BigPatent section Y": "Y is a cross-sectional tagging section (climate tech, ICT impact, former USPC art), "
                           "not a subject-matter section, so abstract-only gold is ill-defined",
}

MOJIBAKE = re.compile("[ÃÂ]|[ãâ][\u0080-¿]|â€")
words = lambda t: re.sub(r"[^a-z0-9]+", " ", t.lower()).split()
norm = lambda t: " ".join(words(t))
sha = lambda s: hashlib.sha256(s.encode()).hexdigest()


def grams(text, n=GRAM):
    w = words(text)
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


def rng_for(task):
    return random.Random(f"{SEED}:{task}")


def hf_file(repo, path):
    return hf_hub_download(repo, path, repo_type="dataset", revision=REV[repo])


def gh(path, as_json=True):
    url = f"https://raw.githubusercontent.com/wenhuchen/Table-Fact-Checking/{REV['wenhuchen/Table-Fact-Checking']}/{path}"
    for attempt in range(5):
        try:
            r = httpx.get(url, timeout=120, follow_redirects=True)
            r.raise_for_status()
            return r.json() if as_json else r.text
        except Exception:  # noqa: BLE001
            if attempt == 4:
                raise
            time.sleep(2 ** attempt)


# ---------------------------------------------------------------- pools: list of dicts {key, label, state, text, meta}
def dedup(pool):
    """Drop exact duplicates by normalised text; drop every copy when their labels disagree."""
    by = defaultdict(list)
    for x in pool:
        by[norm(x["dedup_text"])].append(x)
    out, n_dup, n_conf = [], 0, 0
    for k, xs in by.items():
        if len({x["label"] for x in xs}) > 1:
            n_conf += len(xs)
            continue
        n_dup += len(xs) - 1
        out.append(min(xs, key=lambda x: x["key"]))
    return sorted(out, key=lambda x: x["key"]), {"duplicates_dropped": n_dup, "label_conflicts_dropped": n_conf}


def pool_moral():
    p = hf_file("demelin/moral_stories", "data/classification/action+context/norm_distance/test.jsonl")
    stories = defaultdict(dict)
    for l in open(p):
        r = json.loads(l)
        lab = int(r["label"])
        act = r["moral_action"] if lab == 1 else r["immoral_action"]
        stories[r["ID"][:-1]][lab] = (r, act)
    pool = []
    for sid, d in stories.items():
        for lab, (r, act) in d.items():
            state = (f"Norm:\n{r['norm']}\n\nSituation:\n{r['situation']}\n\nIntention:\n{r['intention']}\n\n"
                     f"Action:\n{act}")
            pool.append({"key": r["ID"], "story": sid, "label": lab, "state": state, "dedup_text": state, "core": act,
                         "meta": {"orig_id": r["ID"], "label_name": "normative action" if lab else "divergent action"}})
    return pool, {"raw_rows": sum(len(d) for d in stories.values()), "stories": len(stories)}


def pool_argq():
    import pandas as pd
    df = pd.read_csv(hf_file("ibm-research/argument_quality_ranking_30k", "test.csv"))
    raw = len(df)
    df = df[(df["set"] == "test") & (df["stance_WA"].isin([1, -1])) & (df["stance_WA_conf"] >= 0.8)]
    pool = []
    for i, r in df.iterrows():
        arg, topic = str(r["argument"]).strip(), str(r["topic"]).strip()
        state = f"Topic:\n{topic}\n\nArgument:\n{arg}"
        pool.append({"key": f"{i:05d}", "topic": topic, "label": 1 if r["stance_WA"] == 1 else 0, "state": state,
                     "dedup_text": state, "core": arg,
                     "meta": {"row": int(i), "label_name": "pro" if r["stance_WA"] == 1 else "con",
                              "stance_WA_conf": float(r["stance_WA_conf"]), "WA": float(r["WA"])}})
    return pool, {"raw_rows": raw, "after_conf_filter": len(pool)}


def pool_tabfact():
    test_ids = gh("data/test_id.json")
    r1, r2 = gh("collected_data/r1_training_all.json"), gh("collected_data/r2_training_all.json")
    official = gh("tokenized_data/test_examples.json")  # the official (lemmatised) test release
    assert set(official) == set(test_ids) and not set(r1) & set(r2)
    pool, misaligned = [], []
    for tid in test_ids:
        src, d = ("r1", r1) if tid in r1 else ("r2", r2)
        stmts, labs, caption = d[tid]
        # raw statements map to the official test set by position only when the table kept all of them
        aligned = [int(x) for x in labs] == [int(x) for x in official[tid][1]]
        if not aligned:
            misaligned.append(tid)
        for j, (s, lab) in enumerate(zip(stmts, labs)):
            pool.append({"key": f"{tid}#{j}", "table": tid, "label": int(lab), "statement": s.strip(), "caption": caption,
                         "round": src, "core": s.strip(), "official": aligned})
    return pool, {"test_tables": len(test_ids), "raw_statements": len(pool),
                  "official_test_statements": sum(len(v[0]) for v in official.values()),
                  "tables_not_aligned_with_official_release": sorted(misaligned)}


def tab_state(x, cache={}):
    tid = x["table"]
    if tid not in cache:
        cache[tid] = gh(f"data/all_csv/{tid}", as_json=False)
    rows = [" | ".join(c.strip() for c in line.split("#")) for line in cache[tid].strip().split("\n")]
    return f"Table caption: {x['caption']}\n\nTable:\n" + "\n".join(rows) + f"\n\nStatement:\n{x['statement']}"


def pool_patent():
    fs = HfFileSystem()
    pool = []
    for s in CPC_SECTIONS:
        path = f"datasets/NortheasternUniversity/big_patent@{REV['NortheasternUniversity/big_patent']}/{s.lower()}/test-00000-of-00001.parquet"
        with fs.open(path, "rb", block_size=1 << 22) as f:
            col = pq.ParquetFile(f).read(columns=["abstract"]).column(0).to_pylist()
        for i, a in enumerate(col):
            a = a.strip()
            pool.append({"key": f"{s}{i:05d}", "label": s, "state": f"Patent abstract:\n{a}", "dedup_text": a, "core": a,
                         "meta": {"orig_index": i, "cpc_section": s}})
    return pool, {"raw_rows": len(pool), "by_section": dict(Counter(x["label"] for x in pool))}


def pool_medical():
    lab = pq.read_table(hf_file("TimSchopf/medical_abstracts", "labels/train-00000-of-00001.parquet")).to_pylist()
    assert {r["condition_label"]: r["condition_name"] for r in lab} == MED_LABELS, lab
    rows = pq.read_table(hf_file("TimSchopf/medical_abstracts", "data/test-00000-of-00001.parquet")).to_pylist()
    pool = []
    for i, r in enumerate(rows):
        a = r["medical_abstract"].strip()
        pool.append({"key": f"{i:05d}", "label": MED_LABELS[r["condition_label"]], "state": f"Medical abstract:\n{a}",
                     "dedup_text": a, "core": a, "meta": {"orig_index": i, "condition_label": r["condition_label"]}})
    return pool, {"raw_rows": len(pool)}


# ---------------------------------------------------------------- CPC official titles (cached once from USPTO)
def cpc_classes():
    if CPC_CACHE.exists():
        return json.loads(CPC_CACHE.read_text())
    clean = lambda x: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", x))).strip()
    out = {"source": "https://www.uspto.gov/web/patents/classification/cpc/html/cpc-<S>.html",
           "fetched": time.strftime("%Y-%m-%d"), "sections": {}}
    for s in CPC_SECTIONS:
        t = httpx.get(out["source"].replace("<S>", s), timeout=60, follow_redirects=True).text
        title = clean(re.search(r"<title>CPC Scheme - " + s + r" (.*?)</title>", t).group(1))
        found = re.findall(r'<table class="classItem[^"]*" id="(' + s + r'\d\d)"><tr>.*?<td class="symbol">.*?'
                           r'<div class="class-title">(.*?)<span class="date-revised">', t, flags=re.S)
        classes, seen = [], set()
        for code, ttl in found:
            if code not in seen:
                seen.add(code)
                classes.append([code, clean(ttl)])
        out["sections"][s] = {"title": title, "classes": classes}
    CPC_CACHE.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    return out


def cpc_card():
    cpc = cpc_classes()
    names, lines = {}, []
    for s in CPC_SECTIONS:
        sec = cpc["sections"][s]
        names[s] = sec["title"].lower()
        keep = [t for c, t in sec["classes"] if not t.startswith("SUBJECT MATTER NOT OTHERWISE PROVIDED FOR")
                and not t.startswith("INDEXING SCHEME")]
        lines.append(f"- {names[s]}: " + " | ".join(t.lower() for t in keep))
    return names, "\n".join(lines)


# ---------------------------------------------------------------- contamination checks (lazy, on ranked candidates)
def touched_texts():
    """Every text we trained, tuned, or selected on: all data/**/*.jsonl except OHS files."""
    seen = set()
    for p in sorted(D.rglob("*.jsonl")):
        rel = p.relative_to(D).as_posix()
        if rel.startswith("ohs") or "/ohs" in rel:
            continue
        for l in open(p):
            try:
                x = json.loads(l)
            except Exception:  # noqa: BLE001
                continue
            if not isinstance(x, dict):
                continue
            for k in ("state", "text", "instructions"):
                t = x.get(k)
                if isinstance(t, str) and len(t) > 40:
                    h = hash(t)
                    if h not in seen:
                        seen.add(h)
                        yield t


def gliclass_texts():
    """GLiClass training texts (Jev side)."""
    fs = HfFileSystem()
    for fn in ["data/train-00000-of-00003.parquet", "data/train-00001-of-00003.parquet", "data/train-00002-of-00003.parquet"]:
        p = hf_file("knowledgator/gliclass-v2.0", fn)
        pf = pq.ParquetFile(p)
        for i in range(pf.num_row_groups):
            for t in pf.read_row_group(i, columns=["text"]).column(0).to_pylist():
                if t:
                    yield t
    p = hf_file("knowledgator/gliclass-v3-logic-dataset", "data/train-00000-of-00001.parquet")
    for t in pq.read_table(p, columns=["text"]).column(0).to_pylist():
        if t:
            yield t
    raw = open(hf_file("knowledgator/GLIClass-v1.0", "zero-class-whole.json"), encoding="utf-8").read()
    dec, i = json.JSONDecoder(), raw.index("[") + 1
    while True:
        while i < len(raw) and raw[i] in " \n\r\t,":
            i += 1
        if i >= len(raw) or raw[i] == "]":
            break
        obj, i = dec.raw_decode(raw, i)
        if isinstance(obj, dict) and obj.get("text"):
            yield obj["text"]
    del fs


def label_nli_texts():
    """tasksource/zero-shot-label-nli premises (forbidden source; bundles e.g. IBM-ArgQ arguments via Touche23-ValueEval)."""
    for fn in ZSL_FILES:
        t = pq.read_table(hf_file("tasksource/zero-shot-label-nli", fn), columns=["premise"]).column(0).to_pylist()
        seen = set()
        for x in t:
            if x and x not in seen:
                seen.add(x)
                yield x


def overlap_scan(cands, texts, label, cores=None):
    """cands: {cid: text}, cores: {cid: core text}. Returns {cid: reason} for candidates sharing a normalised text or a
    12-word run with a scanned text, or whose core text (CORE_MIN_WORDS..11 words) occurs as a contiguous run in it."""
    gram_owner = defaultdict(set)
    full = {}
    for cid, t in cands.items():
        full.setdefault(norm(t), set()).add(cid)
        for g in grams(t):
            gram_owner[g].add(cid)
    core_owner, short_by_first = defaultdict(set), defaultdict(set)
    for cid, c in (cores or {}).items():
        wc = words(c)
        if CORE_MIN_WORDS <= len(wc) < GRAM:  # longer cores are covered by the 12-word runs of the state
            core_owner[" ".join(wc)].add(cid)
            short_by_first[wc[0]].add(len(wc))
    hit, n, t0 = {}, 0, time.time()
    for t in texts:
        n += 1
        nt = norm(t)
        for cid in full.get(nt, ()):
            hit.setdefault(cid, f"{label}: exact text")
        w = nt.split()
        for i in range(len(w) - GRAM + 1):
            g = " ".join(w[i:i + GRAM])
            if g in gram_owner:
                for cid in gram_owner[g]:
                    hit.setdefault(cid, f"{label}: shared 12-word run")
        for i, x in enumerate(w):
            for L in short_by_first.get(x, ()):
                for cid in core_owner.get(" ".join(w[i:i + L]), ()):
                    hit.setdefault(cid, f"{label}: core text contained")
        if n % 200000 == 0:
            print(f"  {label}: scanned {n:,} texts ({time.time() - t0:.0f}s), hits {len(hit)}", flush=True)
    print(f"  {label}: scanned {n:,} texts, {len(hit)} candidate hits", flush=True)
    return hit, n


# ---------------------------------------------------------------- selection
def rank_binary_alternating(pool, unit_key, rng):
    """One item per unit (story/table): units in seeded order, the wanted label alternates by rank."""
    units = defaultdict(list)
    for x in pool:
        units[x[unit_key]].append(x)
    order = sorted(units)
    rng.shuffle(order)
    ranked = []
    for r, u in enumerate(order):
        want = 1 if r % 2 == 0 else 0
        xs = sorted(units[u], key=lambda x: x["key"])
        pref = [x for x in xs if x["label"] == want] or xs
        ranked.append(rng.choice(pref))
    return ranked


def rank_interleaved(pool, group_key, rng):
    """Seeded order inside each group, groups interleaved round-robin (spreads topics)."""
    groups = defaultdict(list)
    for x in pool:
        groups[x[group_key]].append(x)
    names = sorted(groups)
    rng.shuffle(names)
    for g in names:
        groups[g].sort(key=lambda x: x["key"])
        rng.shuffle(groups[g])
    ranked, i = [], 0
    while any(i < len(groups[g]) for g in names):
        ranked += [groups[g][i] for g in names if i < len(groups[g])]
        i += 1
    return ranked


def rank_plain(pool, rng):
    xs = sorted(pool, key=lambda x: x["key"])
    rng.shuffle(xs)
    return xs


def select(ranked, labels, quota, ok):
    got = {l: [] for l in labels}
    rejects = Counter()
    for x in ranked:
        if len(got[x["label"]]) >= quota:
            continue
        why = ok(x)
        if why:
            rejects[why] += 1
            continue
        got[x["label"]].append(x)
        if all(len(v) >= quota for v in got.values()):
            break
    short = {l: quota - len(v) for l, v in got.items() if len(v) < quota}
    assert not short, f"not enough items: {short}"
    return [x for l in labels for x in got[l]], rejects


# ---------------------------------------------------------------- rows
def make_row(task, source, x, qtype, options, gold, card, extra_meta):
    state = x["state"]
    return {
        "id": "r_" + sha(f"ohs2|misc|{task}|{x['key']}")[:12],
        "group_id": f"g:ohs2:{task}:{x['key']}",
        "call_id": "c_" + sha(state)[:12],
        "split": "ohs2",
        "track": "U",
        "source": source,
        "state": state,
        "qtype": qtype,
        "instructions": INSTR[task],
        "options": options,
        "gold": gold,
        "role": "choice" if qtype == "choice" else "aff",
        "card": card,
        "meta": {"part": "misc", "task": task, "orig_split": "test", "licence": LICENCE[task], **x.get("meta", {}),
                 **extra_meta},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reserve", type=int, default=2, help="candidates per slot sent to the contamination scans")
    args = ap.parse_args()

    tasks = {}
    # pools + ranking (ranking never depends on contamination results, only on the seed)
    pm, im = pool_moral()
    pm, dm = dedup([x for x in pm if MIN_CH <= len(x["state"]) <= MAX_CH])
    tasks["moral_stories"] = dict(ranked=rank_binary_alternating(pm, "story", rng_for("moral_stories")), labels=[1, 0],
                                  info={**im, **dm, "dataset": "demelin/moral_stories",
                                        "config": "classification/action+context/norm_distance"})
    pa, ia = pool_argq()
    pa, da = dedup([x for x in pa if MIN_CH <= len(x["state"]) <= MAX_CH])
    tasks["argq_stance"] = dict(ranked=rank_interleaved(pa, "topic", rng_for("argq_stance")), labels=[1, 0],
                                info={**ia, **da, "dataset": "ibm-research/argument_quality_ranking_30k", "config": "test.csv"})
    pt, it = pool_tabfact()
    rk = rank_binary_alternating(pt, "table", rng_for("tabfact"))
    tasks["tabfact"] = dict(ranked=rk, labels=[1, 0], lazy_state=True,
                            info={**it, "dataset": "TabFact (GitHub wenhuchen/Table-Fact-Checking)",
                                  "config": "data/test_id.json + collected_data/r1,r2 + data/all_csv"})
    pp, ip = pool_patent()
    pp, dp = dedup([x for x in pp if MIN_CH <= len(x["state"]) <= MAX_CH])
    tasks["big_patent_cpc"] = dict(ranked=rank_plain(pp, rng_for("big_patent_cpc")), labels=list(CPC_SECTIONS),
                                   info={**ip, **dp, "dataset": "NortheasternUniversity/big_patent", "config": "a..h test, abstract"})
    pd_, id_ = pool_medical()
    pd_, dd = dedup([x for x in pd_ if MIN_CH <= len(x["state"]) <= MAX_CH])
    tasks["medical_abstracts"] = dict(ranked=rank_plain(pd_, rng_for("medical_abstracts")), labels=list(MED_LABELS.values()),
                                      info={**id_, **dd, "dataset": "TimSchopf/medical_abstracts", "config": "default test"})

    # reserve = first (reserve x quota) ranked candidates per label; TabFact states are built only for these
    reserve, cores = {}, {}
    for task, t in tasks.items():
        quota = N_PER_TASK // len(t["labels"])
        per = Counter()
        keep = []
        for x in t["ranked"]:
            if per[x["label"]] < args.reserve * quota:
                per[x["label"]] += 1
                keep.append(x)
        if t.get("lazy_state"):
            seen_n = set()
            kk = []
            for x in keep:
                x["state"] = tab_state(x)
                x["dedup_text"] = x["state"]
                x["meta"] = {"table_id": x["table"], "statement_index": int(x["key"].split("#")[1]), "round": x["round"],
                             "label_name": "entailed" if x["label"] else "refuted"}
                if MIN_CH <= len(x["state"]) <= MAX_CH and norm(x["state"]) not in seen_n:
                    seen_n.add(norm(x["state"]))
                    kk.append(x)
            keep = kk
        t["reserve"] = keep
        for x in keep:
            reserve[f"{task}|{x['key']}"] = x["state"]
            cores[f"{task}|{x['key']}"] = x["core"]
    print(f"reserve candidates: {len(reserve)}", flush=True)

    hits_ours, n_ours = overlap_scan(reserve, touched_texts(), "ours", cores)
    hits_jev, n_jev = overlap_scan(reserve, gliclass_texts(), "gliclass", cores)
    hits_nli, n_nli = overlap_scan(reserve, label_nli_texts(), "label_nli", cores)

    names, patent_card = cpc_card()
    rows, summary = [], {"seed": SEED, "n_per_task": N_PER_TASK, "length_chars": [MIN_CH, MAX_CH],
                         "scanned_texts": {"ours_unique": n_ours, "gliclass": n_jev, "label_nli_premises": n_nli}, "revisions": REV, "tasks": {},
                         "skipped": SKIPPED}
    for task, t in tasks.items():
        quota = N_PER_TASK // len(t["labels"])

        def ok(x, task=task):
            if not (MIN_CH <= len(x["state"]) <= MAX_CH):
                return "length"
            if MOJIBAKE.search(x["state"]):  # a few TabFact tables carry double-encoded UTF-8 in the source files
                return "mojibake in source text"
            if x.get("official") is False:
                return "tabfact: table not aligned with the official test release"
            cid = f"{task}|{x['key']}"
            return hits_ours.get(cid) or hits_jev.get(cid) or hits_nli.get(cid)
        chosen, rejects = select(t["reserve"], t["labels"], quota, ok)
        for x in chosen:
            if task == "moral_stories":
                rows.append(make_row(task, "moral_stories", x, "noul", None, x["label"], CARD[task], {}))
            elif task == "argq_stance":
                rows.append(make_row(task, "ibm_argq30k_stance", x, "noul", None, x["label"], CARD[task], {}))
            elif task == "tabfact":
                rows.append(make_row(task, "tabfact", x, "noul", None, x["label"], CARD[task], {}))
            elif task == "big_patent_cpc":
                opts = [names[s] for s in CPC_SECTIONS]
                rows.append(make_row(task, "big_patent_cpc", x, "choice", opts, names[x["label"]], patent_card,
                                     {"label_name": names[x["label"]]}))
            else:
                opts = list(MED_LABELS.values())
                rows.append(make_row(task, "medical_abstracts", x, "choice", opts, x["label"], CARD[task],
                                     {"label_name": x["label"]}))
        trows = [r for r in rows if r["meta"]["task"] == task]
        bal = Counter(str(r["gold"]) for r in trows)
        summary["tasks"][task] = {
            "source": trows[0]["source"], "licence": LICENCE[task], "orig_split": "test", "n": len(trows),
            "qtype": trows[0]["qtype"], "options": trows[0]["options"] or ["yes (1)", "no (0)"],
            "balance": dict(bal), "max_class_share": round(max(bal.values()) / len(trows), 3),
            "instructions": INSTR[task], "card_chars": len(trows[0]["card"] or ""),
            "state_chars": {"min": min(len(r["state"]) for r in trows), "max": max(len(r["state"]) for r in trows),
                            "mean": round(sum(len(r["state"]) for r in trows) / len(trows))},
            "rejected_in_rank_order": dict(rejects),
            "reserve_hits": {"ours": sorted(k.split("|", 1)[1] for k in hits_ours if k.startswith(task + "|")),
                             "gliclass": sorted(k.split("|", 1)[1] for k in hits_jev if k.startswith(task + "|")),
                             "label_nli": sorted(k.split("|", 1)[1] for k in hits_nli if k.startswith(task + "|"))},
            **t["info"],
        }

    # validation (same checks as build_ohs.py)
    assert len({r["id"] for r in rows}) == len(rows), "duplicate ids"
    by_call = defaultdict(set)
    for r in rows:
        assert r["qtype"] in ("choice", "noul")
        if r["qtype"] == "choice":
            assert r["gold"] in r["options"] and len(set(r["options"])) == len(r["options"]) and 2 <= len(r["options"]) <= 255
        else:
            assert r["gold"] in (0, 1) and r["options"] is None
        assert MIN_CH <= len(r["state"]) <= MAX_CH
        by_call[r["call_id"]].add(r["state"])
    assert all(len(s) == 1 for s in by_call.values()), "a call_id spans different states"
    assert len({norm(r["state"]) for r in rows}) == len(rows), "duplicate states"
    for task, s in summary["tasks"].items():
        assert s["max_class_share"] <= 0.4 or s["qtype"] == "noul" and s["max_class_share"] == 0.5, task

    OUT.parent.mkdir(parents=True, exist_ok=True)
    rows.sort(key=lambda r: (r["meta"]["task"], r["id"]))
    text = "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows)
    OUT.write_text(text)
    summary["rows"] = len(rows)
    summary["sha256"] = hashlib.sha256(text.encode()).hexdigest()
    SUMMARY.write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    print(json.dumps({k: {kk: v[kk] for kk in ("n", "balance", "rejected_in_rank_order", "reserve_hits")}
                      for k, v in summary["tasks"].items()}, indent=1))
    print(f"wrote {len(rows)} rows -> {OUT}")


if __name__ == "__main__":
    sys.exit(main())
