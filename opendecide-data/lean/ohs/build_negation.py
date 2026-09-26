#!/usr/bin/env python
"""OHS-1 part "negation" (track C): natural negation and contrast sets, where the negation is in the data itself.

  (a) ScoNe-NLI test (tasksource/scone, CC0-1.0): 30 complete six-condition contrast sets = 180 choice rows.
      The HF mirror ships only 5 of the 6 test conditions (it has no one_scoped file), so the sixth condition
      (one_scoped = NMoNLI) is read from the official ScoNe GitHub repo pinned to a commit; the 5 HF files are
      checked cell-for-cell against the same commit before use.
  (b) This is not a Dataset (HiTZ/This-is-not-a-dataset, Apache-2.0) test: 60 knowledge triples (test_id) x 3 rows
      = 180 yes/no rows. Each triple is one statement in its affirmative form, its verbal negation ("not") and its
      non-verbal negation ("never" / "no" / "in no context"), all taken verbatim from the dataset.
      Complement relations link an affirmative row to its direct verbal negation (non-modal templates only).
  (c) HateCheck (Paul/hatecheck, CC-BY-4.0) test: 5 cases per functionality x 29 functionalities = 145 yes/no rows,
      card = the paper's definition of hate speech. The sampled negated-hate cases (F14 negate_neg_nh, "I don't hate X")
      pull in their own hateful reference case when it passes the filters, so natural negation pairs exist in-sample.

Rules: dataset gold labels only, official label wording only, zero-shot, seed 20260927, test split, length 20..6000,
dedup on normalized text. Re-runnable: downloads are cached (HF cache + ohs/_cache).

Usage:  .venv/bin/python ohs/build_negation.py
Output: data/ohs_parts/negation.jsonl, data/ohs_parts/negation_relations.jsonl; JSON summary on stdout.
"""
import io
import json
import os
import random
import re
import unicodedata
from collections import Counter, defaultdict

import pandas as pd
import requests
from huggingface_hub import hf_hub_download

SEED = 20260927
PART = "negation"
TRACK = "C"
HERE = os.path.dirname(os.path.abspath(__file__))
LEAN = os.path.dirname(HERE)
OUT_DIR = os.path.join(LEAN, "data", "ohs_parts")
CACHE = os.path.join(HERE, "_cache")
MIN_LEN, MAX_LEN = 20, 6000

SEEN = set()  # normalized texts already used anywhere in this part (dedup across tasks)


def norm(t):
    t = unicodedata.normalize("NFKC", str(t)).lower()
    t = re.sub(r"[^\w\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def ok_len(t):
    return MIN_LEN <= len(str(t).strip()) <= MAX_LEN


# ----------------------------------------------------------------------------------------------------------------
# (a) ScoNe-NLI
# ----------------------------------------------------------------------------------------------------------------
SCONE_HF = "tasksource/scone"
SCONE_GH = "selenashe/ScoNe"
SCONE_SHA = "b02532a2f4185c6118a57a148455e0750592d8c8"  # main as of 2023-07-13
SCONE_CONDS = ["no_negation", "one_not_scoped", "one_scoped", "one_scoped_one_not_scoped", "two_not_scoped", "two_scoped"]
# label relative to the no_negation label: True = same, False = flipped (the scope pattern from the ScoNe paper)
SCONE_SAME = {"no_negation": True, "one_not_scoped": True, "one_scoped": False,
              "one_scoped_one_not_scoped": False, "two_not_scoped": True, "two_scoped": True}
SCONE_OPTS = {"entailment": "follows from the passage", "neutral": "does not necessarily follow"}


def gh_csv(cond):
    os.makedirs(os.path.join(CACHE, "scone"), exist_ok=True)
    p = os.path.join(CACHE, "scone", f"{SCONE_SHA[:10]}_{cond}.csv")
    if not os.path.exists(p):
        url = f"https://raw.githubusercontent.com/{SCONE_GH}/{SCONE_SHA}/scone_nli/test/{cond}.csv"
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        with open(p, "w") as f:
            f.write(r.text)
    return pd.read_csv(p)


def std_cols(d):
    if "sentence1_edited" not in d.columns:  # one_scoped.csv uses the un-suffixed names (per the ScoNe README)
        d = d.rename(columns={"sentence1": "sentence1_edited", "sentence2": "sentence2_edited", "gold_label": "gold_label_edited"})
    return d


def load_scone():
    dfs, origin = {}, {}
    for c in SCONE_CONDS:
        gh = std_cols(gh_csv(c))
        try:
            hf = std_cols(pd.read_csv(hf_hub_download(SCONE_HF, f"{c}_test.csv", repo_type="dataset")))
            cols = ["sentence1_edited", "sentence2_edited", "gold_label_edited"]
            assert hf[cols].equals(gh[cols]), f"HF and GitHub ScoNe differ for {c}"
            dfs[c], origin[c] = hf, f"hf:{SCONE_HF}/{c}_test.csv"
        except Exception as e:  # missing on HF (one_scoped) -> official repo
            if "differ" in str(e):
                raise
            dfs[c], origin[c] = gh, f"github:{SCONE_GH}@{SCONE_SHA[:10]}/scone_nli/test/{c}.csv"
    n = len(dfs["no_negation"])
    for c in SCONE_CONDS:
        d = dfs[c]
        assert len(d) == n
        assert (d.sentence1_lex.values == dfs["no_negation"].sentence1_lex.values).all(), c
        assert (d.sentence2_lex.values == dfs["no_negation"].sentence2_lex.values).all(), c
    return dfs, origin, n


def build_scone(rows_out, report):
    dfs, origin, n = load_scone()
    base = dfs["no_negation"]
    sets, anomalies = [], 0
    for i in range(n):
        items = []
        for c in SCONE_CONDS:
            r = dfs[c].iloc[i]
            items.append((c, str(r.sentence1_edited).strip(), str(r.sentence2_edited).strip(), str(r.gold_label_edited).strip()))
        base_lab = items[0][3]
        pattern_ok = all((lab == base_lab) == SCONE_SAME[c] for c, _, _, lab in items)
        anomalies += (not pattern_ok)
        valid = all(lab in SCONE_OPTS for *_, lab in items) and all(ok_len(p + " " + h) for _, p, h, _ in items)
        keys = [norm(p) + " || " + norm(h) for _, p, h, _ in items]
        valid = valid and len(set(keys)) == len(keys)
        sets.append(dict(i=i, items=items, keys=keys, base_label=base_lab, tmpl=int(base.group_index.iloc[i]),
                         lexpair=frozenset([str(base.sentence1_lex.iloc[i]), str(base.sentence2_lex.iloc[i])]),
                         lex=[str(base.sentence1_lex.iloc[i]), str(base.sentence2_lex.iloc[i])], valid=valid))
    rng = random.Random(SEED)
    tmpls = sorted({s["tmpl"] for s in sets})
    per_t = 30 // len(tmpls)  # 6 base templates -> 5 sets each
    chosen, used_lex = [], set()
    for k, t in enumerate(tmpls):
        # alternate 3/2 and 2/3 entailment-first vs neutral-first sets -> 15/15 overall -> 90/90 labels
        n_ent = (per_t + 1) // 2 if k % 2 == 0 else per_t // 2
        want = {"entailment": n_ent, "neutral": per_t - n_ent}
        for lab, m in want.items():
            cand = [s for s in sets if s["tmpl"] == t and s["base_label"] == lab and s["valid"]]
            rng.shuffle(cand)
            got = 0
            for s in cand:
                if got == m:
                    break
                if (t, s["lexpair"]) in used_lex or any(k_ in SEEN for k_ in s["keys"]):
                    continue
                chosen.append(s); used_lex.add((t, s["lexpair"])); SEEN.update(s["keys"]); got += 1
            assert got == m, f"ScoNe template {t} label {lab}: only {got}/{m}"
    chosen.sort(key=lambda s: s["i"])
    for s in chosen:
        set_id = f"scone_test_{s['i']}"
        for c, p, h, lab in s["items"]:
            rows_out.append(dict(
                _gid=set_id, source="scone", state=f"Passage:\n{p}\n\nStatement:\n{h}", qtype="choice",
                instructions="Does the statement follow from the passage?",
                options=[SCONE_OPTS["entailment"], SCONE_OPTS["neutral"]], gold=SCONE_OPTS[lab], role="choice",
                meta={"license": "CC0-1.0", "hf_id": SCONE_HF, "split_used": "test",
                      "source_id": f"{c}#row{s['i']}", "set_id": set_id, "condition": c, "nli_label": lab,
                      "base_template": s["tmpl"], "lex_pair": s["lex"], "file": origin[c]}))
    golds = Counter(r["gold"] for r in rows_out if r["source"] == "scone")
    report["scone"] = {
        "hf_id": SCONE_HF, "license": "CC0-1.0", "split_used": "test",
        "n_items": len(chosen) * 6, "n_contrast_sets": len(chosen), "n_options": 2,
        "class_balance": dict(golds),
        "sets_by_base_template": dict(Counter(s["tmpl"] for s in chosen)),
        "sets_by_no_negation_label": dict(Counter(s["base_label"] for s in chosen)),
        "note": (f"HF mirror lacks the one_scoped test condition; taken from official github {SCONE_GH}@{SCONE_SHA[:10]} "
                 f"(same CC0 dataset). The 5 HF test files were verified identical to that commit. "
                 f"{anomalies}/{n} source sets deviate from the expected scope label pattern; "
                 f"{sum(1 for s in chosen if not all((lab == s['base_label']) == SCONE_SAME[c] for c, _, _, lab in s['items']))} chosen sets deviate."),
    }


# ----------------------------------------------------------------------------------------------------------------
# (b) This is not a Dataset
# ----------------------------------------------------------------------------------------------------------------
TINAD_HF = "HiTZ/This-is-not-a-dataset"
TINAD_FILE = "data/test-00000-of-00001-b22f6f6322e8a2f0.parquet"


def tinad_key(s, loose=False):
    """Map a sentence to its affirmative skeleton so an affirmation and its negations share a key.
    strict: "in any/no context" <-> "in certain contexts"; loose: context phrases dropped altogether."""
    s = unicodedata.normalize("NFKC", s).lower().strip().rstrip(".").strip()
    s = re.sub(r"\bin (?:any|no) context\b", "in certain contexts", s)
    if loose:
        s = re.sub(r"\bin certain contexts\b", " ", s).strip()
    s = re.sub(r"^(?:not a single|no) ", "", s)
    s = re.sub(r"\bdoes (?:not|never) (\w+)", lambda m: m.group(1) + ("es" if m.group(1).endswith(("s", "sh", "ch", "x")) else "s"), s)
    s = re.sub(r"\bdo (?:not|never) (\w+)", r"\1", s)
    s = re.sub(r"\b(?:not|never) ", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"^(?:a|an) ", "", s)
    return s


def build_tinad(rows_out, rels_out, report):
    df = pd.read_parquet(hf_hub_download(TINAD_HF, TINAD_FILE, repo_type="dataset"))
    df = df.reset_index().rename(columns={"index": "row_idx"})
    df["sentence"] = df.sentence.astype(str).str.strip()
    df = df[df.sentence.map(ok_len)]
    df["key_strict"] = df.sentence.map(tinad_key)
    df["key_loose"] = df.sentence.map(lambda x: tinad_key(x, loose=True))
    rng = random.Random(SEED)
    # candidate triples per test_id: same key, same isDistractor, one row per negation_type.
    # strict key first; a test_id with no strict triple falls back to the loose key (context phrase ignored).
    cands, match = defaultdict(list), {}
    for kind in ("key_strict", "key_loose"):
        for (tid, key, dis), g in df.groupby(["test_id", kind, "isDistractor"], sort=True):
            if match.get(tid, kind) != kind:
                continue
            by = {nt: g[g.negation_type == nt] for nt in ("affirmation", "verbal", "non_verbal")}
            if any(len(v) == 0 for v in by.values()):
                continue
            cands[tid].append((key, by)); match[tid] = kind
    pat_of = df.drop_duplicates("test_id").set_index("test_id").pattern.to_dict()
    all_pats = sorted(df.pattern.unique())
    pats = sorted({pat_of[t] for t in cands})
    skipped_pats = sorted(set(all_pats) - set(pats))
    tids_by_pat = {p: sorted(t for t in cands if pat_of[t] == p) for p in pats}
    for p in pats:
        rng.shuffle(tids_by_pat[p])
    # round-robin allocation of 60 test_ids across patterns (small patterns take what they have)
    alloc, total = Counter(), 60
    while sum(alloc.values()) < total:
        progressed = False
        for p in pats:
            if sum(alloc.values()) >= total:
                break
            if alloc[p] < len(tids_by_pat[p]):
                alloc[p] += 1; progressed = True
        if not progressed:
            break
    order = []
    for p in pats:
        order += tids_by_pat[p]  # shuffled; we walk until alloc[p] triples are accepted (skipping dedup clashes)
    n_true = n_rows = 0
    taken = Counter()
    chosen = []
    walk = order[:]
    rng.shuffle(walk)
    for tid in walk:
        p = pat_of[tid]
        if taken[p] >= alloc[p]:
            continue
        opts = []
        for key, by in cands[tid]:
            a = by["affirmation"].sample(1, random_state=rng.randrange(2**31)).iloc[0]
            v = by["verbal"].sample(1, random_state=rng.randrange(2**31)).iloc[0]
            nv = by["non_verbal"].sample(1, random_state=rng.randrange(2**31)).iloc[0]
            trip = [a, v, nv]
            if len({norm(x.sentence) for x in trip}) < 3 or any(norm(x.sentence) in SEEN for x in trip):
                continue
            opts.append(trip)
        if not opts:
            continue
        # keep the running yes-rate near 50%: prefer triples that move it toward 0.5
        def dist(trip):
            t = n_true + sum(int(bool(x.label)) for x in trip)
            return abs(t / (n_rows + 3) - 0.5)
        best = min(dist(t) for t in opts)
        trip = rng.choice([t for t in opts if dist(t) - best < 1e-9])
        SEEN.update(norm(x.sentence) for x in trip)
        n_true += sum(int(bool(x.label)) for x in trip); n_rows += 3
        taken[p] += 1
        chosen.append((tid, trip))
    assert len(chosen) == total, f"TINAD: only {len(chosen)} triples"
    chosen.sort(key=lambda z: z[0])
    for tid, trip in chosen:
        ids = []
        for x in trip:
            rows_out.append(dict(
                _gid=f"tinad_test_{tid}", source="this_is_not_a_dataset", state=f"Statement:\n{x.sentence}", qtype="noul",
                instructions="Is this statement true?", options=None, gold=int(bool(x.label)), role="aff",
                meta={"license": "Apache-2.0", "hf_id": TINAD_HF, "split_used": "test", "source_id": f"test#{int(x.row_idx)}",
                      "test_id": int(tid), "pattern": x.pattern, "pattern_id": int(x.pattern_id),
                      "negation_type": x.negation_type, "semantic_type": x.semantic_type,
                      "syntactic_scope": x.syntactic_scope, "is_distractor": bool(x.isDistractor),
                      "triple_match": match[tid].replace("key_", "")}))
            ids.append(len(rows_out) - 1)
        a, v = trip[0], trip[1]
        modal = " may " in f" {a.sentence.lower()} " or " may " in f" {v.sentence.lower()} "
        if bool(a.label) != bool(v.label) and not modal and match[tid] == "key_strict":
            rels_out.append(("complement", ids[0], ids[1]))
    tr = [r for r in rows_out if r["source"] == "this_is_not_a_dataset"]
    report["this_is_not_a_dataset"] = {
        "hf_id": TINAD_HF, "license": "Apache-2.0", "split_used": "test",
        "n_items": len(tr), "n_triples": len(chosen), "n_options": "yes/no",
        "class_balance": {"yes(true)": sum(r["gold"] for r in tr), "no(false)": sum(1 - r["gold"] for r in tr)},
        "triples_by_pattern": dict(taken),
        "rows_by_negation_type": dict(Counter(r["meta"]["negation_type"] for r in tr)),
        "triples_distractor": sum(1 for _, t in chosen if bool(t[0].isDistractor)),
        "triples_by_match": dict(Counter(match[t].replace("key_", "") for t, _ in chosen)),
        "patterns_skipped": skipped_pats,
        "note": ("Triple = one statement's affirmative + verbal negation + non-verbal negation (same test_id, same object), "
                 "matched by stripping negation markers (strict: 'in any/no context' <-> 'in certain contexts'; loose fallback "
                 "only when a test_id has no strict triple: context phrase ignored); group_id = test_id. Complement relations "
                 "only between an affirmative row and its direct non-modal verbal negation, strict matches, opposite gold."
                 + (f" Patterns with no affirmative/verbal/non-verbal triple were skipped: {skipped_pats}." if skipped_pats else "")),
    }


# ----------------------------------------------------------------------------------------------------------------
# (c) HateCheck
# ----------------------------------------------------------------------------------------------------------------
HC_HF = "Paul/hatecheck"
HC_PER_FUNC = 5
# Röttger et al. 2021 (ACL), "Definition of Hate Speech"; only "to define hate speech as abuse" -> "Hate speech is abuse".
HC_CARD = ("- hateful: Hate speech is abuse that is targeted at a protected group or at its members for being a part of "
           "that group. We define protected groups based on age, disability, gender identity, familial status, pregnancy, "
           "race, national or ethnic origins, religion, sex or sexual orientation, which broadly reflects international "
           "legal consensus (particularly the UK's 2010 Equality Act, the US 1964 Civil Rights Act and the EU's Charter "
           "of Fundamental Rights).")


def pick_diverse(df, k, rng, preferred=()):
    """k rows: preferred case_ids first, then spread over target identities, seeded."""
    out = [r for _, r in df[df.case_id.isin(list(preferred))].iterrows()][:k]
    rest = df[~df.case_id.isin([r.case_id for r in out])].sample(frac=1.0, random_state=rng.randrange(2**31))
    used_t = Counter(str(r.target_ident) for r in out)
    while len(out) < k and len(rest):
        m = min(used_t[str(t)] for t in rest.target_ident)
        r = rest[rest.target_ident.map(lambda t: used_t[str(t)] == m)].iloc[0]
        out.append(r); used_t[str(r.target_ident)] += 1
        rest = rest[rest.case_id != r.case_id]
    return out


def build_hatecheck(rows_out, report):
    df = pd.read_csv(hf_hub_download(HC_HF, "test.csv", repo_type="dataset"))
    df["test_case"] = df.test_case.astype(str).str.strip()
    n0 = len(df)
    df = df[df.test_case.map(ok_len)]
    n_short = n0 - len(df)
    df = df[~df.test_case.map(norm).isin(SEEN)]
    df = df[~df.test_case.map(norm).duplicated()]
    rng = random.Random(SEED)
    funcs = sorted(df.functionality.unique())
    first = "negate_neg_nh"
    picked = {first: pick_diverse(df[df.functionality == first], HC_PER_FUNC, rng)}
    want_refs = {int(r.ref_case_id) for r in picked[first] if pd.notna(r.ref_case_id)}
    for f in funcs:
        if f == first:
            continue
        picked[f] = pick_diverse(df[df.functionality == f], HC_PER_FUNC, rng, preferred=sorted(want_refs))
    case2row = {}
    for f in funcs:
        for r in picked[f]:
            SEEN.add(norm(r.test_case))
            rows_out.append(dict(
                _gid=f"hatecheck_{int(r.case_id)}", source="hatecheck", state=f"Message:\n{r.test_case}", qtype="noul",
                instructions="Is this message hateful?", options=None, gold=int(r.label_gold == "hateful"), role="aff",
                card=HC_CARD,
                meta={"license": "CC-BY-4.0", "hf_id": HC_HF, "split_used": "test", "source_id": f"case_{int(r.case_id)}",
                      "functionality": f, "label_gold": r.label_gold,
                      "target_ident": None if pd.isna(r.target_ident) else r.target_ident,
                      "direction": None if pd.isna(r.direction) else r.direction,
                      "templ_id": int(r.templ_id), "ref_case_id": None if pd.isna(r.ref_case_id) else int(r.ref_case_id)}))
            case2row[int(r.case_id)] = len(rows_out) - 1
    n_pairs = 0
    for idx in case2row.values():
        m = rows_out[idx]["meta"]
        ref = m["ref_case_id"]
        if ref is not None and ref in case2row:
            m["contrast_with_idx"] = case2row[ref]  # resolved to a row id at write time
            n_pairs += 1
    hc = [r for r in rows_out if r["source"] == "hatecheck"]
    report["hatecheck"] = {
        "hf_id": HC_HF, "license": "CC-BY-4.0", "split_used": "test (only split)",
        "n_items": len(hc), "n_functionalities": len(funcs), "n_options": "yes/no",
        "class_balance": {"yes(hateful)": sum(r["gold"] for r in hc), "no(non-hateful)": sum(1 - r["gold"] for r in hc)},
        "dropped_under_20_chars_from_pool": n_short,
        "in_sample_contrast_pairs": n_pairs,
        "note": ("5 per functionality as specified -> 18 hateful vs 11 non-hateful functionalities = 62/38 yes/no; the 40% "
                 "cap cannot hold for yes/no and was not forced (HateCheck is scored per functionality). "
                 "Card = paper's hate speech definition (one-verb adaptation). Sampled negate_neg_nh cases pull in their "
                 "hateful reference case when it passes filters (meta.contrast_with)."),
    }


# ----------------------------------------------------------------------------------------------------------------
def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    SEEN.clear()
    rows, rels, report = [], [], {}
    build_scone(rows, report)
    build_tinad(rows, rels, report)
    build_hatecheck(rows, report)

    call_of, out = {}, []
    for n, r in enumerate(rows):
        rid = f"r_ohs_{PART}_{n}"
        if r["state"] not in call_of:
            call_of[r["state"]] = f"c_ohs_{PART}_{len(call_of)}"
        row = {"id": rid, "group_id": f"g:ohs:{PART}:{r['_gid']}", "call_id": call_of[r["state"]], "split": "ohs",
               "track": TRACK, "source": r["source"], "state": r["state"], "qtype": r["qtype"],
               "instructions": r["instructions"], "options": r["options"], "gold": r["gold"], "role": r["role"]}
        if r.get("card"):
            row["card"] = r["card"]
        row["meta"] = r["meta"]
        out.append(row)
    for row in out:
        if "contrast_with_idx" in row["meta"]:
            row["meta"]["contrast_with"] = out[row["meta"].pop("contrast_with_idx")]["id"]
    rel_rows = [{"type": t, "a": out[a]["id"], "b": out[b]["id"], "track": "OHS"} for t, a, b in rels]

    # sanity checks
    assert len({r["id"] for r in out}) == len(out)
    for r in out:
        assert MIN_LEN <= len(r["state"]) and r["track"] == TRACK
        if r["qtype"] == "choice":
            assert r["gold"] in r["options"] and 2 <= len(r["options"]) <= 255
        else:
            assert r["gold"] in (0, 1) and r["options"] is None
    by_id = {r["id"]: r for r in out}
    for x in rel_rows:
        assert by_id[x["a"]]["gold"] != by_id[x["b"]]["gold"]

    p = os.path.join(OUT_DIR, f"{PART}.jsonl")
    with open(p, "w") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    pr = os.path.join(OUT_DIR, f"{PART}_relations.jsonl")
    with open(pr, "w") as f:
        for x in rel_rows:
            f.write(json.dumps(x) + "\n")
    report["_files"] = {"rows": p, "relations": pr, "n_rows": len(out), "n_relations": len(rel_rows),
                        "n_calls": len(call_of), "n_groups": len({r["group_id"] for r in out})}
    print(json.dumps(report, indent=1, default=str))


if __name__ == "__main__":
    main()
