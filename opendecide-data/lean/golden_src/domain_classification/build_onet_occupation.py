"""Build raw rows for onet_occupation (O*NET 31.0 Database, US Department of Labor / ETA, August 2026 release).

Question types (each task statement is used in at most one row):
  choice : three duties of one occupation -> which occupation (the gold + 2-5 sibling occupations of the same SOC
           minor group; if the minor group is too small, filled from the same major group).
  yes/no : an occupation title + three duties -> are these duties of that occupation? yes = its own duties;
           no = three duties of a sibling occupation (same minor group, else same major group).
Source : https://www.onetcenter.org/dl_files/database/db_31_0_text.zip (sha256 pinned). No splits -> train.
Licence: CC BY 4.0 ("Read Me.txt" in the zip and https://www.onetcenter.org/license_db.html). Attribution: O*NET 31.0
         Database, U.S. Department of Labor, Employment and Training Administration; used verbatim, rows re-grouped.
Texts  : human-written O*NET task statements (from incumbent surveys and occupational experts / analysts).
Labels : the occupation each task statement is listed under (by construction of the database, human-curated).
Quality: confusers are never the same detailed SOC code (parent/child O*NET occupations) and never an occupation
         whose task profile is near-identical (TF-IDF centroid cosine >= 0.5). Every shown duty is distinctive (max
         TF-IDF cosine to any task of every other occupation in the row < 0.25) and no closer to another row
         occupation's official description than to its owner's. Positives: duties not generic (a similar task,
         cos >= 0.25, exists in <= 4 other occupations) and >= 1 duty echoes the owner's description (cos >= 0.06).
         Negatives (a sibling's duties under another title) are stricter: not generic (<= 2 other occupations),
         cos to every task of the named occupation < 0.2, cos to its description < 0.03, every duty echoes the true
         owner's description (cos >= 0.05). Core tasks preferred; task texts shared by several
         occupations are never used.
Definitions: the official O*NET occupation descriptions (CC BY 4.0), first sentences up to ~60 words.
Deterministic (seed 20260929). CPU only.
"""
import collections
import random
import re
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

KEY = "onet_occupation"
SEED = 20260929
URL = "https://www.onetcenter.org/dl_files/database/db_31_0_text.zip"
ZIP_SHA = "6883548adf5fde64cf6f801b35d15519c9225f2732c3cab0e281c652d16b23a9"
CACHE = C.CACHE / "onet"
LICENCE = ("CC BY 4.0 (db_31_0_text/Read Me.txt; https://www.onetcenter.org/license_db.html). Source: O*NET 31.0 "
           "Database, U.S. Department of Labor, Employment and Training Administration; re-grouped by the builder")
Q_CHOICE = "Which occupation performs all of the listed duties?"
Q_YN = "Are the listed duties part of the job of the occupation named above?"
DEFS_YN = {
    "yes": ("The duties are tasks of the named occupation: they describe that occupation's own characteristic work "
            "as the occupation is defined."),
    "no": ("The duties describe a different occupation's characteristic work (often a related job in the same field) "
           "and are not tasks the named occupation performs."),
}
SIM_TASK = 0.25
SIM_OCC = 0.5


def short_def(desc, max_words=60):
    sents = re.split(r"(?<=[.!?])\s+", desc.strip())
    out = []
    for s in sents:
        if out and len(" ".join(out + [s]).split()) > max_words:
            break
        out.append(s)
    return " ".join(out)


def main():
    zpath, zsha = C.fetch(URL, CACHE / "db_31_0_text.zip", ZIP_SHA)
    print("zip sha256:", zsha)
    z = zipfile.ZipFile(zpath)
    ts = pd.read_csv(z.open("db_31_0_text/Task Statements.txt"), sep="\t", dtype=str)
    oc = pd.read_csv(z.open("db_31_0_text/Occupation Data.txt"), sep="\t", dtype=str)
    title = dict(zip(oc["O*NET-SOC Code"], oc["Title"]))
    desc = dict(zip(oc["O*NET-SOC Code"], oc["Description"]))
    ts["Task"] = ts["Task"].str.strip()
    ts["n"] = ts["Task"].map(C.norm)
    dup = ts.groupby("n")["O*NET-SOC Code"].transform("nunique") > 1
    print("tasks:", len(ts), "shared across occupations (dropped):", int(dup.sum()))
    ts = ts[~dup & (ts["Task"].str.split().str.len() >= 5)].reset_index(drop=True)
    assert len(set(title.values())) == len(title)

    vec = TfidfVectorizer(stop_words="english", sublinear_tf=True, ngram_range=(1, 2), min_df=2)
    vec.fit(list(ts["Task"]) + [title[c] + ". " + desc[c] for c in title])
    X = vec.transform(ts["Task"])
    # genericness: number of OTHER occupations having a task with cosine >= 0.25 to this task
    S = (X @ X.T).tocsr()
    codes = ts["O*NET-SOC Code"].values
    generic = np.zeros(len(ts), dtype=int)
    for i in range(len(ts)):
        row = S.getrow(i)
        generic[i] = len(set(codes[row.indices[row.data >= 0.25]]) - {codes[i]})
    D = {c: vec.transform([title[c] + ". " + desc[c]]) for c in title}
    occ_rows = collections.defaultdict(list)
    for i, code in enumerate(ts["O*NET-SOC Code"]):
        occ_rows[code].append(i)
    occs = sorted(c for c in occ_rows if len(occ_rows[c]) >= 6)
    cent = {}
    for c in occs:
        v = np.asarray(X[occ_rows[c]].mean(axis=0)).ravel()
        cent[c] = v / (np.linalg.norm(v) + 1e-12)

    def occ_sim(a, b):
        return float(cent[a] @ cent[b])

    def confusers(a):
        same_minor = [b for b in occs if b[:4] == a[:4] and b[:7] != a[:7] and occ_sim(a, b) < SIM_OCC]
        if len(same_minor) >= 2:
            return same_minor, "minor"
        same_major = [b for b in occs if b[:2] == a[:2] and b[:7] != a[:7] and occ_sim(a, b) < SIM_OCC]
        return same_major, "major"

    rng = random.Random(SEED)
    used = set()

    def pick_tasks(owner, others, k=3, neg=False):
        """k unused tasks of `owner` (core first), distinctive vs every task of the other row occupations
        (cos < SIM_TASK) and no closer to another row occupation's official description than to the owner's.
        Positives (yes rows, choice rows): not generic (a task with cos >= 0.25 exists in <= 4 other occupations)
        and >= 1 duty clearly echoes the owner's description (cos >= 0.06).
        Negatives (a sibling's duties shown under another title): not generic (<= 2 other occupations), cos to every
        task of the named occupation < 0.2, cos to its description < 0.03, and every duty echoes the true owner's
        description (cos >= 0.05)."""
        cand = [i for i in occ_rows[owner] if i not in used and generic[i] <= (2 if neg else 4)]
        if not cand or not others:
            return None
        oth = [j for o in others for j in occ_rows[o]]
        sims = (X[cand] @ X[oth].T).toarray().max(axis=1)
        own_d = (X[cand] @ D[owner].T).toarray().ravel()
        oth_d = np.max(np.hstack([(X[cand] @ D[o].T).toarray() for o in others]), axis=1)
        ok = []
        for i, s, od, xd in zip(cand, sims, own_d, oth_d):
            if s >= (0.2 if neg else SIM_TASK) or xd > od:
                continue
            if neg and (xd >= 0.03 or od < 0.05):
                continue
            ok.append((ts.at[i, "Task Type"] != "Core", -od, rng.random(), i, od))
        if len(ok) < k:
            return None
        ok.sort()
        chosen = ok[:k]
        if not neg and chosen[0][4] < 0.06:
            return None
        return [x[3] for x in chosen]

    def fmt(idx):
        return "\n".join("- " + ts.at[i, "Task"] for i in idx)

    rows = []
    stats = collections.Counter()
    order = occs[:]
    rng.shuffle(order)
    # pass 1: yes/no (one yes + one no per asked occupation), pass 2-3: choice rows
    for a in order:
        conf, lvl = confusers(a)
        if not conf:
            stats["no_confuser"] += 1
            continue
        # contrastive pair around one sibling b: no-row = b's duties under a's title; yes-row = a's own duties
        # that are distinctive against b
        cands = conf[:]
        rng.shuffle(cands)
        for b in cands:
            idx = pick_tasks(b, [a], neg=True)
            if idx:
                used.update(idx)
                rows.append(("yn", a, b, idx, lvl, None))
                break
        else:
            stats["no_negative"] += 1
            b = cands[0]
        idx = pick_tasks(a, [b])
        if idx:
            used.update(idx)
            rows.append(("yn", a, a, idx, lvl, None))
        else:
            stats["no_positive"] += 1
    for _ in range(2):
        for a in order:
            conf, lvl = confusers(a)
            if len(conf) < 2:
                continue
            opts = rng.sample(conf, min(len(conf), rng.choice([2, 3, 4, 5])))
            idx = pick_tasks(a, opts)
            while not idx and len(opts) > 2:  # retry with fewer confusers
                opts = opts[:-1]
                idx = pick_tasks(a, opts)
            if not idx:
                stats["choice_no_tasks"] += 1
                continue
            used.update(idx)
            rows.append(("choice", a, a, idx, lvl, opts))

    out = []
    for kind, asked, owner, idx, lvl, opts in rows:
        rid = f"onet31-{owner}-" + "-".join(ts.at[i, "Task ID"] for i in idx)
        if kind == "yn":
            state = f"Occupation: {title[asked]}\nDuties:\n{fmt(idx)}"
            gold = "yes" if owner == asked else "no"
            ex = {"instructions": Q_YN, "options": ["yes", "no"], "gold": gold}
            cfg = f"yes/no duties-of-occupation; confuser level={lvl}"
            ex["defs"] = "yn"
        else:
            options = sorted([title[asked]] + [title[o] for o in opts])
            state = f"Duties:\n{fmt(idx)}"
            ex = {"instructions": Q_CHOICE, "options": options, "gold": title[asked]}
            cfg = f"choice occupation among {len(options)} ({lvl} group siblings)"
        out.append({"key": KEY, "rid": rid, "state": state, **ex, "soft": None,
                    "meta": {"dataset": "O*NET 31.0 Database (onetcenter.org)", "config": cfg,
                             "revision": f"O*NET 31.0 (Aug 2026); sha256:{zsha}", "licence": LICENCE,
                             "split": "train (no official split)",
                             "orig_label": {"asked": asked, "task_owner": owner,
                                            "task_ids": [ts.at[i, "Task ID"] for i in idx]},
                             "family": C.FAMILY, "edge": None, "seed": SEED}})
        if "defs" in ex:
            out[-1]["meta"]["defs"] = ex.pop("defs")
            del out[-1]["defs"]
    rng.shuffle(out)
    assert len({r["rid"] for r in out}) == len(out)
    C.write_rows(KEY, out)
    defs_choice = {title[c]: short_def(desc[c]) for c in occs}
    C.write_defs(KEY, defs_choice)
    C.write_defs(f"{KEY}__yn", DEFS_YN)
    print(dict(stats))
    C.summary(out)
    print("choice option counts:", collections.Counter(len(r["options"]) for r in out if r["options"] != ["yes", "no"]))


if __name__ == "__main__":
    main()
