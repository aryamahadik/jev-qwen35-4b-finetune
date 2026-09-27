"""Build raw rows for the Steam Review Aspect Dataset (yes/no per review aspect).

Source: HF ilos-vigil/steam-review-aspect-dataset @ c02f7348f1e8d6813e1752616ed8ea8ba50638eb,
        data/train/data-00000-of-00001.arrow (TRAIN split only, 900 reviews; the 200-row test split is never read).
Licence: CC BY 4.0 (HF card YAML "license: cc-by-4.0" and the card's "License" section).
Texts: English Steam user reviews (human-written, SRec snapshot of 21 Feb 2024).
Labels: 8 multi-label aspects, annotated by hand by the dataset author (single human annotator);
        "Recommended" is the reviewer's own Steam recommendation. No model-generated text or labels.
Snapshot saved under breadth_src/cache/steam_aspect/ (README.md, train arrow, train dataset_info.json).

Design:
- One row per source review; each review is asked about exactly one aspect.
- Cells = (aspect, yes/no); 8 aspects x 2 labels = 16 cells with an equal quota (~22 each), filled
  smallest-pool-first so yes/no is 50/50 overall and every aspect gets about 44 rows.
- The aspect definition from the card is written into the question, so the generic yes/no option
  definitions work for every aspect. Card rule: an aspect counts even when mentioned implicitly or only
  by its absence.
- Question wording (verifier pass): Price/Visual/Technical/Suggestion clarified from the card table and the
  train-split label pattern (e.g. 'wait for a sale' buying advice is Suggestion=0 in 12 of 14 train reviews).
- Filters: cleaned_review 15-4000 chars, dedup on normalised text. soft = null (single annotator).
"""
import json, os, random, re, collections

SEED = 20261101
N_MAX = 350
REV = "c02f7348f1e8d6813e1752616ed8ea8ba50638eb"
REPO = "ilos-vigil/steam-review-aspect-dataset"
ARROW_REMOTE = "data/train/data-00000-of-00001.arrow"

HERE = os.path.dirname(os.path.abspath(__file__))
LEAN = os.path.dirname(HERE)
CACHE = os.path.join(HERE, "cache", "steam_aspect")
ARROW = os.path.join(CACHE, "train_data-00000-of-00001.arrow")
OUT = os.path.join(LEAN, "data", "v13_parts", "raw", "steam_aspect.jsonl")

ASPECTS = ["Recommended", "Story", "Gameplay", "Visual", "Audio", "Technical", "Price", "Suggestion"]
QUESTIONS = {
    "Recommended": "Does the reviewer recommend this game?",
    "Story": "Does this review mention the game's story (plot, characters, lore, world-building or other storytelling)?",
    "Gameplay": "Does this review mention the game's gameplay (controls, mechanics, interactivity, difficulty or other gameplay setup)?",
    "Visual": "Does this review mention the game's visuals (graphics, aesthetics, art style, animation, visual effects or other visual elements)?",
    "Audio": "Does this review mention the game's audio (sound design, music, voice acting or other auditory elements)?",
    "Technical": "Does this review mention technical aspects of the game (bugs, crashes, performance or frame rate, OS or controller support, overall functionality)?",
    "Price": "Does this review mention the price of the game or of its additional content (cost, value for money, sales or discounts, being free, microtransactions)?",
    "Suggestion": "Does this review suggest a change or improvement to the game itself (something to add, fix or remove, or an external factor such as its price or publisher)? Buying advice to other players, such as waiting for a sale, does not count as a suggestion.",
}
OPTIONS = ["yes", "no"]
META_BASE = {"dataset": REPO, "config": "default", "revision": REV,
             "licence": "CC BY 4.0 (HF card YAML license: cc-by-4.0 and card 'License' section)",
             "split": "train"}


def norm(s):
    return re.sub(r"\s+", " ", s.lower()).strip()


def load():
    if not os.path.exists(ARROW):
        from huggingface_hub import hf_hub_download
        import shutil
        os.makedirs(CACHE, exist_ok=True)
        p = hf_hub_download(REPO, ARROW_REMOTE, repo_type="dataset", revision=REV)
        shutil.copy(p, ARROW)
    from datasets import Dataset
    return Dataset.from_file(ARROW)


def main():
    rng = random.Random(SEED)
    ds = load()
    drop = collections.Counter()
    recs, seen = [], set()
    for i, r in enumerate(ds):
        t = r["cleaned_review"]
        if not t or not (15 <= len(t) <= 4000):
            drop["length"] += 1; continue
        k = norm(t)
        if k in seen:
            drop["dup"] += 1; continue
        seen.add(k)
        labs = [int(round(x)) for x in r["labels"]]
        assert len(labs) == 8 and set(labs) <= {0, 1}
        recs.append({"idx": i, "appid": r["appid"], "text": t, "labs": labs})
    rng.shuffle(recs)

    cells = [(a, y) for a in range(8) for y in (1, 0)]
    pools = {c: [r for r in recs if r["labs"][c[0]] == c[1]] for c in cells}
    quota = {c: N_MAX // len(cells) for c in cells}
    for c in cells[: N_MAX - sum(quota.values())]:
        quota[c] += 1
    used, chosen = set(), []
    fill = collections.Counter()
    # smallest pool first, so scarce cells (e.g. Suggestion=yes) are not starved
    for c in sorted(cells, key=lambda c: (len(pools[c]), c)):
        for r in pools[c]:
            if fill[c] >= quota[c]:
                break
            if r["idx"] in used:
                continue
            used.add(r["idx"]); chosen.append((r, c)); fill[c] += 1
    # top up (only if some cell was short): least-filled label, then least-filled aspect
    while len(chosen) < N_MAX:
        lab_n = collections.Counter(c[1] for _, c in chosen)
        asp_n = collections.Counter(c[0] for _, c in chosen)
        order = sorted(cells, key=lambda c: (lab_n[c[1]], asp_n[c[0]], c))
        got = False
        for c in order:
            r = next((r for r in pools[c] if r["idx"] not in used), None)
            if r:
                used.add(r["idx"]); chosen.append((r, c)); got = True; break
        if not got:
            break

    rng.shuffle(chosen)
    rows = []
    for r, (a, y) in chosen:
        meta = dict(META_BASE)
        meta.update({"orig_label": y, "aspect": ASPECTS[a], "all_aspect_labels": dict(zip(ASPECTS, r["labs"])),
                     "appid": r["appid"], "row_index": r["idx"], "annotators": 1})
        rows.append({
            "key": "steam_aspect",
            "rid": f"train-{r['idx']}",
            "state": r["text"],
            "instructions": QUESTIONS[ASPECTS[a]],
            "options": OPTIONS,
            "gold": "yes" if y == 1 else "no",
            "soft": None,
            "meta": meta,
        })
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    lab = collections.Counter(r["gold"] for r in rows)
    L = sorted(len(r["state"]) for r in rows)
    print("source train records:", len(ds), "dropped:", dict(drop), "usable:", len(recs))
    print("rows:", len(rows), "labels:", dict(lab), "max share: %.3f" % (max(lab.values()) / len(rows)))
    print("per aspect (yes/no):", {ASPECTS[a]: (fill[(a, 1)], fill[(a, 0)]) for a in range(8)}
          if len(chosen) == sum(fill.values()) else
          dict(collections.Counter((r["meta"]["aspect"], r["gold"]) for r in rows)))
    print("soft coverage: 0/%d (single annotator)" % len(rows))
    print("len chars min/median/mean/max: %d/%d/%.0f/%d" % (L[0], L[len(L) // 2], sum(L) / len(L), L[-1]))
    print("unique rids:", len({r["rid"] for r in rows}))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
