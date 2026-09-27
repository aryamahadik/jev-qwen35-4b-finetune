"""Build raw rows for 'hatemoji_build' (HatemojiBuild, Kirk et al. 2021, "Hatemoji: A Test Suite and
Adversarially-Generated Dataset for Benchmarking and Detecting Emoji-based Hate").

Source   : GitHub HannahKirk/Hatemoji at commit a626f63216158748d072e581efc00267031f4404,
           HatemojiBuild/train.csv ONLY (validation.csv, test.csv and the HatemojiCheck folder are never
           downloaded or read). Raw snapshot: breadth_src/cache/hatemoji_build/train.csv (+ README.md, LICENSE).
Licence  : CC BY 4.0 - repo LICENSE file ("Attribution 4.0 International") and README ("It is licensed under
           CC-BY-4.0"); the HF card HannahRoseKirk/HatemojiBuild also states cc-by-4.0.
Provenance: texts written by trained human annotators on Dynabench (human-and-model-in-the-loop: humans wrote
           adversarial entries against a classifier; the model never generated text). label_gold = majority of
           three human annotators; type/target assigned by humans. No LLM involvement.

Two tasks (every source record appears at most once, in one task):
- yesno  "Is this post hateful?"  -> original/perturbation contrast pairs (both members in train, opposite
         gold labels), both members kept together, filling the file up to 400 rows (~200 rows, 50/50).
- choice "Which option best describes this post?" over 5 options {not hateful, derogation, animosity,
         dehumanization, threatening language} -> round-robin over the four hate types, 40 rows per option.
         While 'not hateful' is below 40, each hate-type draw takes a whole contrast pair (hateful member +
         its not-hateful perturbation, kept together); afterwards hate types are drawn from records whose
         matched perturbation is not in the train split (natural singletons), so no pair is ever split.

Rules applied
- Text length 15-4,000 chars (both pair members must pass for a pair unit); text kept verbatim.
- Dedup: normalised exact duplicates dropped (texts that appear with conflicting labels dropped entirely).
- Decontamination vs HateCheck (OHS-1 held-out source; Paul/hatecheck @9d2ac89d test.csv read ONLY as an
  exclusion list, never as data): drop records whose normalised text equals a HateCheck case.
- Decontamination vs DynaHate R1-R4 (Vidgen et al. 2021; the `dynahate` task of the forbidden tasksource label-NLI
  set; github bvidgen/Dynamically-Generated-Hate-Speech-Dataset @36f9dc84, v0.2.3 csv read ONLY as an exclusion
  list): drop records whose normalised text equals a DynaHate entry.
- Decontamination vs our own files (SELECTION.md rule 9): every non-held-out *.jsonl under lean/ and
  opendecide-data/data/ plus JevBench public (ohs*/preds*/results* paths never opened; this dataset's own rows
  skipped): drop a record if its emoji-stripped word string (>= 3 words) equals any string there, or if it shares a
  13-word run with one.
- target (cryptic multi-group codes) is kept only in meta, not used as a task.
- Soft labels: the release gives only the majority gold, no per-annotator counts -> soft = null.
- Deterministic, seed 20261101.
"""
import hashlib
import json
import os
import random
import re
import shutil
import unicodedata
from collections import Counter

import pandas as pd
import requests
from huggingface_hub import hf_hub_download

SEED = 20261101
KEY = "hatemoji_build"
REPO = "github.com/HannahKirk/Hatemoji"
REV = "a626f63216158748d072e581efc00267031f4404"
RAW = "https://raw.githubusercontent.com/HannahKirk/Hatemoji/{rev}/{path}"
HATECHECK_REPO = "Paul/hatecheck"
HATECHECK_REV = "9d2ac89df04254e5c427bcc8d61b6d6c83a1f59b"
DYNAHATE_URL = ("https://raw.githubusercontent.com/bvidgen/Dynamically-Generated-Hate-Speech-Dataset/"
                "36f9dc849626bc2f6d2e1c2861db556294a2a947/Dynamically%20Generated%20Hate%20Dataset%20v0.2.3.csv")
DYNAHATE_SHA256 = "6e0aa7e598ab5b648cb1f0b48626a3e5f2e39a5abbd9fee998efa5a0b6cab4ca"
GRAM = 13
LICENCE = ("CC BY 4.0 (GitHub HannahKirk/Hatemoji LICENSE 'Attribution 4.0 International' and README "
           "'licensed under CC-BY-4.0'; HF card HannahRoseKirk/HatemojiBuild license: cc-by-4.0)")
MAX_ROWS = 400
PER_CHOICE_LABEL = 40

Q_YESNO = "Is this post hateful?"
YESNO = ["yes", "no"]
Q_CHOICE = "Which option best describes this post?"
TYPE_NAME = {
    "none": "not hateful",
    "derogation": "derogation",
    "animosity": "animosity",
    "dehumanizinglanguage": "dehumanization",
    "threateninglanguage": "threatening language",
}
CHOICE = ["not hateful", "derogation", "animosity", "dehumanization", "threatening language"]
HATE_TYPES = ["derogation", "animosity", "dehumanization", "threatening language"]

HERE = os.path.dirname(os.path.abspath(__file__))
LEAN = os.path.dirname(HERE)
CACHE = os.path.join(HERE, "cache", KEY)
OUT = os.path.join(LEAN, "data", "v13_parts", "raw", f"{KEY}.jsonl")
ROOT = os.path.dirname(LEAN)
JEV = os.path.dirname(ROOT)


def norm(s):
    s = unicodedata.normalize("NFKC", s).lower()
    return re.sub(r"\s+", " ", s).strip()


def snapshot():
    os.makedirs(CACHE, exist_ok=True)
    for path in ("HatemojiBuild/train.csv", "LICENSE", "README.md"):  # never validation/test/HatemojiCheck
        dst = os.path.join(CACHE, os.path.basename(path))
        if not os.path.exists(dst):
            r = requests.get(RAW.format(rev=REV, path=path), timeout=120)
            r.raise_for_status()
            with open(dst, "wb") as fh:
                fh.write(r.content)
    return os.path.join(CACHE, "train.csv")


def hatecheck_norms():
    ddir = os.path.join(CACHE, "decontam")
    os.makedirs(ddir, exist_ok=True)
    dst = os.path.join(ddir, "hatecheck_cases.csv")
    if not os.path.exists(dst):
        shutil.copy(hf_hub_download(HATECHECK_REPO, "test.csv", repo_type="dataset", revision=HATECHECK_REV), dst)
    hc = pd.read_csv(dst)
    return {norm(t) for t in hc["test_case"].astype(str)}


def words(t):
    return re.sub(r"[\W_]+", " ", t.casefold()).split()


def dynahate_norms():
    dst = os.path.join(CACHE, "decontam", "dynahate_v0.2.3.csv")
    if not os.path.exists(dst):
        r = requests.get(DYNAHATE_URL, timeout=300)
        r.raise_for_status()
        with open(dst, "wb") as fh:
            fh.write(r.content)
    with open(dst, "rb") as fh:
        assert hashlib.sha256(fh.read()).hexdigest() == DYNAHATE_SHA256, "DynaHate snapshot changed"
    return {norm(t) for t in pd.read_csv(dst, keep_default_na=False)["text"].astype(str)}


def scan_files():
    fs = set()
    for base in (LEAN, os.path.join(ROOT, "data")):
        for dp, dns, fns in os.walk(base):
            rel = os.path.relpath(dp, base).lower().split(os.sep)
            if any(x.startswith(("ohs", "preds", "results")) or x in ("cache", ".venv") for x in rel if x != "."):
                dns[:] = []
                continue
            dns[:] = [d for d in dns if not d.lower().startswith(("ohs", "preds", "results")) and d not in ("cache", ".venv")]
            for fn in fns:
                p = os.path.join(dp, fn)
                if fn.endswith(".jsonl") and not fn.lower().startswith(("ohs", "preds", "results")) \
                        and os.path.realpath(p) != os.path.realpath(OUT):
                    fs.add(p)
    jb = os.path.join(JEV, "bench", "jevbench", "datasets", "public")
    if os.path.isdir(jb):
        fs |= {os.path.join(jb, f) for f in os.listdir(jb) if f.endswith(".jsonl")}
    return sorted(fs)


def strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values():
            yield from strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from strings(v)


def own_file_hits(recs, eids):
    """Exact (emoji-stripped, >= 3 words) or 13-word-run overlap of our texts with any string in our other files."""
    exact, owner = {}, {}
    for eid in eids:
        w = words(recs[eid].text)
        if len(w) >= 3:
            exact.setdefault(" ".join(w), set()).add(eid)
        for i in range(len(w) - GRAM + 1):
            owner.setdefault(" ".join(w[i:i + GRAM]), set()).add(eid)
    hit, seen = {}, set()
    for f in scan_files():
        with open(f, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if KEY in line or "HatemojiBuild" in line:   # this dataset's own rows in merged files
                    continue
                try:
                    x = json.loads(line)
                except Exception:  # noqa: BLE001
                    continue
                for t in strings(x):
                    if len(t) < 15 or t in seen:
                        continue
                    seen.add(t)
                    w = words(t)
                    for eid in exact.get(" ".join(w), ()):
                        hit.setdefault(eid, f)
                    if len(w) >= GRAM and owner:
                        for i in range(len(w) - GRAM + 1):
                            for eid in owner.get(" ".join(w[i:i + GRAM]), ()):
                                hit.setdefault(eid, f)
    return hit


def main():
    df = pd.read_csv(snapshot(), dtype={"text": str, "matched_text": str}, keep_default_na=False)
    df.columns = [c.replace(".", "_") for c in df.columns]
    assert set(df["split"]) == {"train"}
    recs = {int(r.entry_id): r for r in df.itertuples(index=False)}
    stats = Counter()

    # --- record-level filters
    hc = hatecheck_norms()
    dh = dynahate_norms()
    labels_by_norm = {}
    for r in recs.values():
        labels_by_norm.setdefault(norm(r.text), set()).add(int(r.label_gold))
    ok, seen = set(), set()
    for eid in sorted(recs):
        r = recs[eid]
        n = norm(r.text)
        if not (15 <= len(r.text) <= 4000):
            stats["drop_length"] += 1
        elif int(r.label_gold) != (r.type != "none"):
            stats["drop_label_type_mismatch"] += 1
        elif len(labels_by_norm[n]) > 1:
            stats["drop_conflicting_label"] += 1
        elif n in hc:
            stats["drop_hatecheck_overlap"] += 1
        elif n in dh:
            stats["drop_dynahate_overlap"] += 1
        elif n in seen:
            stats["drop_duplicate"] += 1
        else:
            seen.add(n)
            ok.add(eid)
    hits = own_file_hits(recs, ok)
    for eid in sorted(hits):
        ok.discard(eid)
        stats["drop_own_file_overlap"] += 1
    for f, c in sorted(Counter(os.path.relpath(v, JEV) for v in hits.values()).items()):
        print("  own-file overlap:", c, f)

    # --- units: contrast pairs (both members in train and both pass) and singletons (partner not in train)
    pairs, singles = [], []
    for eid in sorted(ok):
        mid = int(recs[eid].matched_id)
        if mid in recs:
            if mid in ok and eid < mid and int(recs[eid].label_gold) != int(recs[mid].label_gold):
                pairs.append((eid, mid))
        else:
            singles.append(eid)
    rng = random.Random(SEED)
    rng.shuffle(pairs)
    rng.shuffle(singles)

    def tname(eid):
        return TYPE_NAME[recs[eid].type]

    def row(eid, task):
        r = recs[eid]
        lab = int(r.label_gold)
        if task == "yesno":
            q, opts, gold = Q_YESNO, YESNO, ("yes" if lab == 1 else "no")
        else:
            q, opts, gold = Q_CHOICE, CHOICE, tname(eid)
        return {
            "key": KEY,
            "rid": f"train.csv:entry_id={eid}",
            "state": r.text,
            "instructions": q,
            "options": opts,
            "gold": gold,
            "soft": None,
            "meta": {"dataset": "HatemojiBuild (" + REPO + ", HatemojiBuild/train.csv)", "config": task,
                     "revision": REV, "licence": LICENCE, "split": "train",
                     "orig_label": {"label_gold": lab, "type": r.type, "target": r.target,
                                    "set": r.set, "round_set": r.round_set,
                                    "matched_id": int(r.matched_id)}},
        }

    # --- choice task first (it needs the rare hate types), round-robin over hate types
    by_type_pair = {t: [p for p in pairs if tname(p[0] if recs[p[0]].label_gold == 1 else p[1]) == t]
                    for t in HATE_TYPES}
    by_type_single = {t: [e for e in singles if tname(e) == t] for t in HATE_TYPES}
    used = set()
    choice_rows = []
    cnt = Counter()
    order = HATE_TYPES[:]
    rng.shuffle(order)
    progressed = True
    while progressed and any(cnt[t] < PER_CHOICE_LABEL for t in HATE_TYPES):
        progressed = False
        for t in order:
            if cnt[t] >= PER_CHOICE_LABEL:
                continue
            if cnt["not hateful"] < PER_CHOICE_LABEL:
                pool = by_type_pair[t]
                while pool and (pool[0][0] in used or pool[0][1] in used):
                    pool.pop(0)
                if pool:
                    a, b = pool.pop(0)
                    for e in (a, b):
                        used.add(e)
                        choice_rows.append(row(e, "choice"))
                        cnt[tname(e)] += 1
                    progressed = True
                    continue
            pool = by_type_single[t]
            if pool:
                e = pool.pop(0)
                used.add(e)
                choice_rows.append(row(e, "choice"))
                cnt[t] += 1
                progressed = True

    # --- yes/no task: whole contrast pairs up to MAX_ROWS in total
    yesno_rows = []
    for a, b in pairs:
        if len(choice_rows) + len(yesno_rows) + 2 > MAX_ROWS:
            break
        if a in used or b in used:
            continue
        used.update((a, b))
        yesno_rows += [row(a, "yesno"), row(b, "yesno")]

    rows = choice_rows + yesno_rows
    assert len({r["rid"] for r in rows}) == len(rows)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    L = sorted(len(r["state"]) for r in rows)
    print("source rows:", len(recs), "filter stats:", dict(stats), "kept:", len(ok))
    print("contrast pairs:", len(pairs), "singletons:", len(singles))
    print("written:", len(rows), "->", OUT)
    print("yesno labels:", dict(Counter(r["gold"] for r in yesno_rows)))
    print("choice labels:", dict(Counter(r["gold"] for r in choice_rows)))
    print("soft coverage:", sum(r["soft"] is not None for r in rows), "/", len(rows))
    print("length chars min/median/mean/max:", L[0], L[len(L) // 2], round(sum(L) / len(L), 1), L[-1])


if __name__ == "__main__":
    main()
