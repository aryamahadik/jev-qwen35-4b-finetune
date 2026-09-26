"""v0.11 SELECTION GATE: new-corpus, unseen-label-set dev set ("NC").

Never trained on, never the held-out test. Built from the BTZSC benchmark (btzsc/btzsc on Hugging Face, Aarab,
ICLR 2026), using only subsets whose underlying corpora OpenDecide has never touched and that are not OHS-1 sources.
Each item: one text with exactly one correct label, a choice over the subset's FULL label set, and a card whose
definitions are the BTZSC hypotheses (verbatim). Gold = the BTZSC positive pair (labels == 1), i.e. the source
dataset's own label.

Subsets used (origin checked in code against the original release where one is loadable; see ORIGIN):
  capsotu (21 CAP policy topics), manifesto (56 MARPOR categories), empathetic (32 emotions), appreviews (2),
  trueteacher (2), biasframes_offensive / _intent / _sex (2 each), financialphrasebank (3).
Subsets NOT used and why: agnews, rottentomatoes, imdb, emotiondair (our dev/eval sources); amazonpolarity, yelpreviews,
  yahootopics, banking77, massive (trained on); wikitoxic_* (not in the requested clean list; toxicity is close to
  civil_comments / toxic_conversations which we train on); bundles (sentiment/emotion/intent/topic/all) duplicate the above.

Decontamination: drops any candidate whose text shares a 12-word run (or, for texts under 12 words, its whole
normalised text) with any state already in lean/data (train, dev, eval files) or data/v11_parts.
Held-out files are NEVER opened (data/ohs*.jsonl, data/ohs_parts/, lean/ohs/, JevBench/bench): the subsets used here are
not OHS-1 source datasets (PREREG_OHS.md: arXiv 2026, LegalBench, LEDGAR, ScoNe, This-is-not-a-dataset, HateCheck,
PubMedQA, VitaminC, GoEmotions, SGD), so no overlap is possible by construction.

Option strings never contain ": " (the card is "- <option>: <definition>" and consumers split on the first ": "), so
MARPOR "X: Positive/Negative" labels are shown as "X (positive)/(negative)". TrueTeacher items that share an article
share a group_id.

Writes data/v11_parts/dev_nc.jsonl (split "dev", track "NC") and data/v11_parts/dev_nc_summary.json.
Deterministic (seed 20261001); re-runnable.
  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python build_v11_devnc.py
"""
from __future__ import annotations

import hashlib
import json
import random
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd
from huggingface_hub import hf_hub_download

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
OUT_DIR = DATA / "v11_parts"
OUT = OUT_DIR / "dev_nc.jsonl"
SUMMARY = OUT_DIR / "dev_nc_summary.json"
SEED = 20261001
N_PER = 112          # texts per subset (9 subsets -> ~1,000 rows)
NGRAM = 12
MIN_WORDS = 4
REPO = "btzsc/btzsc"


def rng(*parts) -> random.Random:
    h = hashlib.sha256(":".join([str(SEED), *map(str, parts)]).encode()).hexdigest()
    return random.Random(int(h[:16], 16))


def sid(*parts) -> str:
    return hashlib.sha1("|".join(map(str, parts)).encode()).hexdigest()[:12]


def words(t: str) -> list[str]:
    return re.sub(r"[^a-z0-9]+", " ", str(t).lower()).split()


def norm(t: str) -> str:
    return " ".join(words(t))


# ------------------------------------------------------------------ subset specs
# option: BTZSC label_text -> option string shown to the model (None = keep label_text verbatim)
SPECS = {
    "capsotu": dict(
        instructions="Which policy topic is this excerpt from a US presidential speech mainly about?",
        wrap="Speech excerpt:\n{t}", option=None,
        origin="Comparative Agendas Project coding of US State of the Union speeches (via Laurer et al.); not an OHS source, never used"),
    "manifesto": dict(
        instructions="Which policy category does this passage from a political party manifesto fall under?",
        wrap="Manifesto excerpt:\n{t}",
        option=lambda labs: {l: re.sub(r": (Positive|Negative)$", lambda m: f" ({m.group(1).lower()})", l) for l in labs},
        origin="Manifesto Project (MARPOR) coded quasi-sentences (via Laurer et al.); not an OHS source, never used"),
    "empathetic": dict(
        instructions="What is the main emotion in this dialogue?",
        wrap="Dialogue:\n{t}", option=None,
        origin="EmpatheticDialogues (Rashkin et al. 2019, facebook/empathetic_dialogues); distinct from GoEmotions; never used"),
    "appreviews": dict(
        instructions="What sentiment does this app review express?",
        wrap="App review:\n{t}", option=None,
        origin="sealuzh/app_reviews (Grano et al. 2017, open-source Android apps on Google Play); not Amazon; never used"),
    "trueteacher": dict(
        instructions="Is the summary factually consistent with the full article?",
        wrap="{t}", option={"factually_consistent": "factually consistent", "factually_inconsistent": "factually inconsistent"},
        origin="google/trueteacher (CNN/DailyMail articles + model summaries; label from the dataset, which was produced by "
               "a FLAN-PaLM 540B teacher, so expect some label noise); not VitaminC; never used"),
    "biasframes_offensive": dict(
        instructions="Could this post be considered offensive, disrespectful, or toxic?",
        wrap="Post:\n{t}", option={"offensive": "offensive", "not_offensive": "not offensive"},
        origin="Social Bias Frames (Sap et al. 2020; Reddit, Gab, Stormfront, Founta/Davidson/Waseem tweets); not HateCheck, "
               "not TweetEval; never used"),
    "biasframes_intent": dict(
        instructions="Was this post intended to be offensive or disrespectful?",
        wrap="Post:\n{t}", option={"intent": "intended to offend", "not_intent": "not intended to offend"},
        origin="Social Bias Frames (Sap et al. 2020); see biasframes_offensive"),
    "biasframes_sex": dict(
        instructions="Does this post contain allusions to sexual content?",
        wrap="Post:\n{t}", option={"sex": "sexual content", "not_sex": "no sexual content"},
        origin="Social Bias Frames (Sap et al. 2020); see biasframes_offensive"),
    "financialphrasebank": dict(
        instructions="What is the sentiment of this financial news sentence from an investor's point of view?",
        wrap="Financial news sentence:\n{t}", option=None,
        origin="Financial PhraseBank (Malo et al. 2014, takala/financial_phrasebank); not the TFNS tweets; never used"),
}
SKIPPED_SUBSETS = {
    "agnews": "our dev source (devzs)", "rottentomatoes": "our dev source (devp)", "imdb": "our eval source (eval_opi)",
    "emotiondair": "our dev source (devzs, dair-ai emotion)", "amazonpolarity": "trained on (amazon_polarity)",
    "yelpreviews": "trained on (yelp_polarity)", "yahootopics": "trained on (yahoo_answers_topics)",
    "banking77": "trained on", "massive": "trained on (amazon_massive_intent)",
    "wikitoxic_insult": "not in the clean list; toxicity near civil_comments/toxic_conversations (trained)",
    "wikitoxic_obscene": "same as wikitoxic_insult", "wikitoxic_threat": "same as wikitoxic_insult",
    "wikitoxic_toxicaggregated": "same as wikitoxic_insult",
    "sentiment/emotion/intent/topic/all": "convenience bundles duplicating base subsets",
}
FORBIDDEN_SOURCE_PAT = re.compile(
    r"legalbench|cuad|maud|hearsay|abercrombie|lexglue|ledgar|ecthr|scotus|unfair|scone|not.a.dataset|hatecheck|pubmedqa|"
    r"vitaminc|goemotion|go_emotion|schema.guided|sgd|arxiv|tweet|rotten|sms|tfns|ag_?news|dair|enron|climate|\bcb\b|bbc|"
    r"deysi|sst|imdb", re.I)


def load_subset(name: str) -> pd.DataFrame:
    return pd.read_parquet(hf_hub_download(REPO, f"{name}/test-00000-of-00001.parquet", repo_type="dataset"))


def label_card(df: pd.DataFrame) -> dict[str, str]:
    """label_text -> the BTZSC hypothesis used when that label is the correct one (must be unique)."""
    pos = df[df["labels"] == 1]
    hyp = pos.groupby("label_text")["hypothesis"].agg(lambda x: sorted(set(x)))
    out = {}
    for lab, hs in hyp.items():
        assert len(hs) == 1, (lab, hs)
        out[lab] = hs[0].strip()
    # every label must appear as a candidate; make sure the positive-hypothesis map covers the full label set
    assert set(out) == set(df["label_text"].unique()), "label set / hypothesis map mismatch"
    assert len(set(out.values())) == len(out), "two labels share one hypothesis"
    return out


def single_label_items(df: pd.DataFrame, n_labels: int):
    """Texts with exactly one positive pair and the full candidate set; returns [(text, gold_label_text)]."""
    g = df.groupby("text").agg(n=("labels", "size"), pos=("labels", "sum"))
    ok = g[(g["pos"] == 1) & (g["n"] == n_labels)].index
    pos = df[(df["labels"] == 1) & (df["text"].isin(set(ok)))]
    return list(zip(pos["text"], pos["label_text"])), int((g["pos"] != 1).sum() + ((g["pos"] == 1) & (g["n"] != n_labels)).sum())


# ------------------------------------------------------------------ origin verification
def verify_origins(subsets: dict[str, pd.DataFrame]) -> dict:
    """Check BTZSC texts against the original releases where they are loadable. Returns per-subset notes and, for
    biasframes, the SBF dataSource of each post (recorded in meta)."""
    res, sbf_src = {}, {}
    pos = lambda s: [t for t, l in zip(subsets[s]["text"], subsets[s]["labels"]) if l == 1]
    try:
        ar = pd.read_parquet(hf_hub_download("sealuzh/app_reviews", "data/train-00000-of-00001.parquet", repo_type="dataset"))
        col = ar["review"]
    except Exception:
        from datasets import load_dataset
        col = load_dataset("sealuzh/app_reviews", split="train")["review"]
    s = {norm(x) for x in col}
    p = pos("appreviews")
    res["appreviews"] = f"{sum(norm(t) in s for t in p)}/{len(p)} texts found in sealuzh/app_reviews"
    for sp in ["train", "validation", "test"]:
        d = pd.read_parquet(hf_hub_download("allenai/social_bias_frames", f"default/{sp}/0000.parquet", repo_type="dataset",
                                            revision="refs/convert/parquet"))
        for post, src in zip(d["post"], d["dataSource"]):
            sbf_src.setdefault(norm(post), src)
    for b in ["biasframes_offensive", "biasframes_intent", "biasframes_sex"]:
        p = pos(b)
        res[b] = f"{sum(norm(t) in sbf_src for t in p)}/{len(p)} posts found in allenai/social_bias_frames (unmatched are dropped)"
    tt = pd.read_parquet(hf_hub_download("google/trueteacher", "default/train/0000.parquet", repo_type="dataset",
                                         revision="refs/convert/parquet"))
    tts = {norm(x) for x in tt["summary"]}
    p = pos("trueteacher")
    summ = [norm(t.split("\n\nFull article:")[0].replace("Summary:", "")) for t in p]
    res["trueteacher"] = f"{sum(x in tts for x in summ)}/{len(p)} summaries found in google/trueteacher"
    ed = set()
    for sp in ["train", "validation", "test"]:
        d = pd.read_parquet(hf_hub_download("facebook/empathetic_dialogues", f"default/{sp}/0000.parquet", repo_type="dataset",
                                            revision="refs/convert/parquet"))
        ed |= {norm(str(x).replace("_comma_", ",")) for x in d["prompt"]}
    p = pos("empathetic")
    ctx = [norm(t.split("\n")[0].replace("Context:", "")) for t in p]
    res["empathetic"] = f"{sum(c in ed for c in ctx)}/{len(p)} situation prompts found in facebook/empathetic_dialogues"
    z = zipfile.ZipFile(hf_hub_download("takala/financial_phrasebank", "data/FinancialPhraseBank-v1.0.zip", repo_type="dataset"))
    fpb = set()
    for n in z.namelist():
        if "Sentences" in n and n.endswith(".txt"):
            fpb |= {norm(l.rsplit("@", 1)[0]) for l in z.read(n).decode("latin-1").splitlines() if "@" in l}
    p = pos("financialphrasebank")
    res["financialphrasebank"] = f"{sum(norm(t) in fpb for t in p)}/{len(p)} sentences found in Financial PhraseBank v1.0"
    res["capsotu"] = "content check only (US State of the Union text, CAP major topics); no public mirror loaded"
    res["manifesto"] = "content check only (party manifesto quasi-sentences, MARPOR categories); no public mirror loaded"
    return res, sbf_src


# ------------------------------------------------------------------ decontamination
def contamination_index(cands: dict[str, list[str]]):
    """Candidate n-gram keys (n = 12, or the whole text if shorter) -> set of candidate ids."""
    keys = defaultdict(set)
    for cid, texts in cands.items():
        for t in texts:
            w = words(t)
            n = min(NGRAM, len(w))
            for i in range(len(w) - n + 1):
                keys[(n, " ".join(w[i:i + n]))].add(cid)
    return keys


def is_heldout(p: Path) -> bool:
    """Held-out test files (OHS-1) are never opened, not even for hashing."""
    rel = p.resolve().relative_to(DATA.resolve())
    return rel.parts[0].lower().startswith("ohs") or any(x.lower() in ("ohs", "ohs_parts", "bench") for x in rel.parts)


def scan_contamination(cands: dict[str, list[str]]):
    keys = contamination_index(cands)
    ns = sorted({n for n, _ in keys})
    first = defaultdict(set)  # first word -> lengths to try
    for n, k in keys:
        first[k.split(" ", 1)[0]].add(n)
    files = sorted(p for p in DATA.rglob("*.jsonl") if p.resolve() != OUT.resolve() and not is_heldout(p))
    hit, seen_states, scanned = set(), set(), []
    for f in files:
        nrows = 0
        with open(f) as fh:
            for line in fh:
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                if not isinstance(r, dict):
                    continue
                st = r.get("state")
                if not isinstance(st, str):
                    continue
                nrows += 1
                h = hashlib.sha1(st.encode()).digest()
                if h in seen_states:
                    continue
                seen_states.add(h)
                w = words(st)
                for i, tok in enumerate(w):
                    if tok not in first:
                        continue
                    for n in first[tok]:
                        if i + n <= len(w):
                            ids = keys.get((n, " ".join(w[i:i + n])))
                            if ids:
                                hit |= ids
        if nrows:
            scanned.append(str(f.relative_to(HERE)))
    return hit, scanned, len(seen_states), ns


# ------------------------------------------------------------------ build
def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name in SPECS:
        assert not FORBIDDEN_SOURCE_PAT.search(name), name
    dfs = {name: load_subset(name) for name in SPECS}
    for name, df in dfs.items():
        assert set(df["dataset_id"].unique()) == {name}, (name, df["dataset_id"].unique())
    origin_checks, sbf_src = verify_origins(dfs)

    skipped = Counter()
    pools, cards = {}, {}
    for name, df in dfs.items():
        cards[name] = label_card(df)
        items, n_bad = single_label_items(df, len(cards[name]))
        skipped[f"{name}: not exactly one correct label / incomplete candidate set"] += n_bad
        keep = []
        for t, lab in items:
            t = t.strip()
            if len(words(t)) < MIN_WORDS:
                skipped[f"{name}: under {MIN_WORDS} words"] += 1
                continue
            if name.startswith("biasframes") and norm(t) not in sbf_src:
                skipped[f"{name}: post not matched to allenai/social_bias_frames"] += 1
                continue
            keep.append((t, lab))
        pools[name] = sorted(set(keep))

    # the same normalised text must not appear with two different labels (within or across subsets)
    labs_by_text = defaultdict(set)
    for name, items in pools.items():
        for t, lab in items:
            labs_by_text[norm(t)].add((name, lab))

    # stratified candidate order: shuffle within label, then round-robin over labels (sorted), per subset
    ordered = {}
    for name, items in pools.items():
        r = rng("devnc", name)
        by = defaultdict(list)
        for t, lab in items:
            if len({l for s, l in labs_by_text[norm(t)] if s == name}) > 1:
                skipped[f"{name}: same text with two labels"] += 1
                continue
            by[lab].append(t)
        for lab in by:
            r.shuffle(by[lab])
        labs = sorted(by)
        seq, i = [], 0
        while any(i < len(by[l]) for l in labs):
            for l in labs:
                if i < len(by[l]):
                    seq.append((by[l][i], l))
            i += 1
        ordered[name] = seq

    # decontaminate a generous prefix of each ordered list (enough to fill N_PER after drops)
    cand = {}
    for name, seq in ordered.items():
        for j, (t, lab) in enumerate(seq[:N_PER * 4]):
            cand[f"{name}#{j}"] = [t]
    hit, scanned, n_states, ns = scan_contamination(cand)

    rows, used_texts = [], set()
    for name, seq in ordered.items():
        spec, card_map = SPECS[name], cards[name]
        o_spec = spec["option"]
        opt = o_spec(sorted(card_map)) if callable(o_spec) else (o_spec or {k: k for k in card_map})
        assert set(opt) == set(card_map)
        assert len(set(opt.values())) == len(opt), f"{name}: option strings collide"
        assert not any(": " in o or "\n" in o or o != o.strip() for o in opt.values()), f"{name}: bad option string"
        labels_all = sorted(card_map)
        chosen = []
        for j, (t, lab) in enumerate(seq):
            if len(chosen) == N_PER:
                break
            if j >= N_PER * 4:
                raise RuntimeError(f"{name}: candidate prefix exhausted")
            if f"{name}#{j}" in hit:
                skipped[f"{name}: overlaps existing train/dev/eval/OHS state (12-gram or exact)"] += 1
                continue
            if norm(t) in used_texts:
                skipped[f"{name}: text already used by another subset"] += 1
                continue
            used_texts.add(norm(t))
            chosen.append((t, lab))
        if len(chosen) < N_PER:
            skipped[f"{name}: only {len(chosen)} items available"] += 0
        for t, lab in chosen:
            th = sid("devnc", name, norm(t))
            rr = rng("devnc", name, th)
            opts = [opt[l] for l in labels_all]
            rr.shuffle(opts)
            inv = {opt[l]: l for l in labels_all}
            card = "\n".join(f"- {o}: {card_map[inv[o]]}" for o in opts)
            state = spec["wrap"].format(t=t)
            # same underlying item -> same group: TrueTeacher summaries of one article share the article's group
            gkey = sid("devnc", name, norm(t.split("\n\nFull article:", 1)[1])) if name == "trueteacher" else th
            group = f"g:btzsc_{name}:{gkey}"
            key = f"dev_nc|{group}|choice|{spec['instructions']}"
            meta = {"benchmark": "btzsc", "btzsc_subset": name, "btzsc_label_text": lab, "n_options": len(opts),
                    "hf_id": REPO, "hf_config": name, "hf_split": "test", "card_source": "BTZSC hypotheses (verbatim)"}
            if name.startswith("biasframes"):
                meta["sbf_dataSource"] = sbf_src.get(norm(t))
            if name == "trueteacher":
                meta["label_note"] = "TrueTeacher labels were produced by a FLAN-PaLM 540B teacher (dataset gold, not human)"
            rows.append({"id": "r_" + sid(SEED, key, hashlib.sha1(state.encode()).hexdigest()[:8]),
                         "group_id": group, "call_id": "c_" + sid(SEED, "dev_nc", state), "split": "dev", "track": "NC",
                         "source": f"btzsc_{name}", "state": state, "qtype": "choice",
                         "instructions": spec["instructions"], "options": opts, "gold": opt[lab], "role": "choice",
                         "card": card, "meta": meta})

    rows.sort(key=lambda r: r["id"])
    assert len({r["id"] for r in rows}) == len(rows)
    assert len({r["call_id"] for r in rows}) == len(rows)
    for r in rows:
        assert r["gold"] in r["options"] and r["options"].count(r["gold"]) == 1
        assert len(set(r["options"])) == len(r["options"])
        assert len(r["card"].splitlines()) == len(r["options"])
        # the card must parse the way decoder_io.card_defs / run_jev.card_defs parse it (split on the first ": ")
        parsed = dict(line[2:].split(": ", 1) for line in r["card"].splitlines())
        assert list(parsed) == r["options"] and all(v.strip() for v in parsed.values()), r["id"]
    with open(OUT, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    src = Counter(r["source"] for r in rows)
    summary = {
        "files": {"rows": str(OUT), "summary": str(SUMMARY), "script": str(Path(__file__).resolve())},
        "n_rows": len(rows),
        "rows_by_source": dict(sorted(src.items())),
        "rows_by_track": dict(Counter(r["track"] for r in rows)),
        "rows_by_qtype": dict(Counter(r["qtype"] for r in rows)),
        "rows_by_role": dict(Counter(r["role"] for r in rows)),
        "rows_by_split": dict(Counter(r["split"] for r in rows)),
        "n_groups": len({r["group_id"] for r in rows}),
        "option_count_histogram": dict(sorted(Counter(len(r["options"]) for r in rows).items())),
        "label_balance": {s: dict(sorted(Counter(r["gold"] for r in rows if r["source"] == s).items(), key=lambda x: -x[1]))
                          for s in sorted(src)},
        "labels_covered": {s: f"{len({r['gold'] for r in rows if r['source'] == s})}/{len(cards[s[len('btzsc_'):]])}"
                           for s in sorted(src)},
        "state_words_median": {s: sorted(len(r["state"].split()) for r in rows if r["source"] == s)[src[s] // 2] for s in sorted(src)},
        "origin_checks": origin_checks,
        "origins": {k: v["origin"] for k, v in SPECS.items()},
        "decontam": {"method": f"{NGRAM}-word run, or whole normalised text if shorter (n used: {ns})",
                     "heldout_files_opened": "none (data/ohs*, ohs_parts/, lean/ohs/, bench/ are never read)",
                     "unique_states_scanned": n_states, "files_scanned": scanned},
        "skipped": dict(sorted((k, v) for k, v in skipped.items() if v)),
        "skipped_subsets": SKIPPED_SUBSETS,
        "costs": {"openrouter_usd": 0.0, "note": "no LLM calls; cards are BTZSC hypotheses verbatim"},
        "seed": SEED,
    }
    SUMMARY.write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
