"""Build golden rows for codah (CODAH: COmmonsense Dataset Adversarially-authored by Humans; Chen et al. 2019).

Source : github.com/Websail-NU/CODAH @ acf7ffa4041ade86c6f7dd2f92fb08c957350280, data/full_data.tsv (2,776 questions).
         The release has no train/dev/test split (only cross-validation folds made by the user), so by the spec's rule
         the whole file counts as train.
Licence: ODC-BY 1.0 -- repository README.md: "The CODAH dataset is made available under the Open Data Commons
         Attribution License: http://opendatacommons.org/licenses/by/1.0/".
Texts  : sentence-completion questions written adversarially by crowd workers (prompt + 1 correct + 3 incorrect
         completions, all human-written), human accuracy 95.3%. Category codes from the authors: i idioms, r reference,
         p polysemy, n negation, q quantitative, o other.
Tasks  : every row shows the beginning and all four lettered endings (the task is "most sensible of the four").
         - yes/no (default defs): 'Among the listed endings, is (X) "..." the most sensible continuation?' 50% gold.
         - choice (defs qid "choice"): 'Which listed ending continues the text most sensibly?' A-D.
Dedupe : one row per distinct prompt text (95 repeated prompts dropped); near-duplicate questions (same gold ending,
         prompt word-Jaccard >= 0.75, ending-word Jaccard >= 0.8; added in review 29 Sep 2026) dropped, contrast twins
         with a different gold kept; decontamination vs forbidden label-NLI,
         local train/dev/eval files and JevBench public.
Edge   : from the authors' category codes: n -> negation (double_negation if two negations act on each other),
         q -> numeric, p/r -> ambiguous (polysemy / reference), i -> implicit (idiom); o -> surface cues or null.
Deterministic (seed 20261118).
"""
import collections
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as C  # noqa: E402

KEY = "codah"
SEED = 20261118
N_YN = 2000
COMMIT = "acf7ffa4041ade86c6f7dd2f92fb08c957350280"
BASE = f"https://raw.githubusercontent.com/Websail-NU/CODAH/{COMMIT}/"
CACHE = C.HERE / "cache" / KEY
FILES = {
    "full_data.tsv": (BASE + "data/full_data.tsv", "96689f2abf2f09eb91af50e2d8f92bb553e157601908a1cee83fe68670b5c3ea"),
    "README.md": (BASE + "README.md", "c5b753cb86a57dfb369d9132afb0eb43eacb82b05229c496ec3816e0d3cd8fb4"),
}
LICENCE = (f"ODC-BY 1.0 (github.com/Websail-NU/CODAH/blob/{COMMIT}/README.md: 'The CODAH dataset is made available "
           "under the Open Data Commons Attribution License: http://opendatacommons.org/licenses/by/1.0/')")
LET = C.letters(4)
DEFS = {
    "yes": "The named ending is the listed continuation that makes the most sense: read after the beginning, it "
           "describes what would ordinarily be true or happen next, fits who and what the beginning is about, and "
           "respects any negation, number, idiom or double meaning in it.",
    "no": "Another listed ending makes more sense: the named ending contradicts the beginning, is about the wrong "
          "person or thing, misreads a word, idiom or quantity, or describes something absurd or unrelated.",
}
DEFS_CHOICE = {L: f"Ending ({L}) is the listed continuation that makes the most sense after the beginning: it "
                  f"describes what would ordinarily be true or happen next and respects any negation, number, idiom "
                  f"or double meaning in the beginning." for L in LET}
CAT_EDGE = [("n", "negation"), ("q", "numeric"), ("p", "ambiguous"), ("r", "ambiguous"), ("i", "implicit")]


def edge(cat, text):
    for code, tag in CAT_EDGE:
        if code in cat:
            if tag == "negation" and C.is_double_negation(text):
                return "double_negation"
            return tag
    return C.edge(text, ("double_negation", "negation", "units", "numeric", "quantifier"))


def main():
    rng = random.Random(SEED)
    paths = {n: C.fetch(u, CACHE / n, s) for n, (u, s) in FILES.items()}
    assert "Open Data Commons Attribution License" in paths["README.md"].read_text()
    lines = [l.rstrip("\n").split("\t") for l in open(paths["full_data.tsv"], encoding="utf-8")]
    assert len(lines) == 2776 and all(len(x) == 7 for x in lines)
    recs, seen = [], set()
    for i, x in enumerate(lines):
        cat, prompt, ends, gi = x[0].strip() or "o", C.clean(x[1]), [C.clean(e) for e in x[2:6]], int(x[6])
        if len({C.norm(e) for e in ends}) < 4 or not all(ends) or len(C.words(prompt)) < 3:
            continue
        k = C.norm(prompt)
        if k in seen:
            continue
        seen.add(k)
        recs.append({"rid": f"full_data_{i:04d}", "cat": cat, "prompt": prompt, "ends": ends, "gi": gi})
    print(f"records={len(lines)} usable (distinct prompts, 4 distinct endings)={len(recs)}")
    # near-duplicate questions (typo / one-word variants of the same item: 'penguin is is an exception', 'to see a
    # movie' / 'to a movie'): same gold ending, prompt word-Jaccard >= 0.75 and ending-word Jaccard >= 0.8. Contrast
    # twins whose gold differs (e.g. Germany/Scotland swapped -> Saarbrucken/Edinburgh) are kept.
    kept, n_nd = [], 0
    for r in recs:
        pw, ew, g = set(C.words(r["prompt"])), set(C.words(" ".join(r["ends"]))), C.norm(r["ends"][r["gi"]])
        if any(g == k[2] and len(pw & k[0]) / len(pw | k[0]) >= 0.75 and len(ew & k[1]) / len(ew | k[1]) >= 0.8
               for k in (x["_sig"] for x in kept)):
            n_nd += 1
            continue
        r["_sig"] = (pw, ew, g)
        kept.append(r)
    recs = kept
    for r in recs:
        del r["_sig"]
    print(f"near-duplicate questions dropped: {n_nd}; left {len(recs)}")
    hits = C.decon({r["rid"]: [r["prompt"] + " " + r["ends"][r["gi"]], r["prompt"]] for r in recs})
    print("decon drops:", dict(collections.Counter(hits.values())))
    recs = [r for r in recs if r["rid"] not in hits]

    rng.shuffle(recs)
    meta0 = {"dataset": "CODAH (Websail-NU/CODAH)", "config": "data/full_data.tsv (release has no splits: counts as train)",
             "revision": f"git:{COMMIT}; sha256:{FILES['full_data.tsv'][1]}", "licence": LICENCE,
             "split": "train", "family": C.FAMILY}

    def state(r):
        e = "\n".join(f"({L}) {t}" for L, t in zip(LET, r["ends"]))
        return f"Beginning: {r['prompt']} ...\n\nPossible endings:\n{e}"

    rows = []
    yn, ch = recs[:N_YN], recs[N_YN:]
    flags = [True] * (len(yn) // 2) + [False] * (len(yn) - len(yn) // 2)
    rng.shuffle(flags)
    for r, ask_gold in zip(yn, flags):
        ai = r["gi"] if ask_gold else rng.choice([i for i in range(4) if i != r["gi"]])
        rows.append({"key": KEY, "rid": r["rid"], "state": state(r),
                     "instructions": f'Among the listed endings, is ({LET[ai]}) "{r["ends"][ai]}" the most sensible '
                                     f'continuation of the beginning?',
                     "options": C.YN, "gold": "yes" if ask_gold else "no", "soft": None,
                     "meta": dict(meta0, orig_label={"category": r["cat"], "answer": LET[r["gi"]], "asked": LET[ai]},
                                  edge=edge(r["cat"], r["prompt"] + " " + r["ends"][r["gi"]]))})
    for r in ch:
        rows.append({"key": KEY, "rid": r["rid"], "state": state(r),
                     "instructions": "Which listed ending continues the beginning most sensibly?",
                     "options": LET, "gold": LET[r["gi"]], "soft": None,
                     "meta": dict(meta0, defs="choice", orig_label={"category": r["cat"], "answer": LET[r["gi"]]},
                                  edge=edge(r["cat"], r["prompt"] + " " + r["ends"][r["gi"]]))})
    rng.shuffle(rows)
    out = C.write_outputs(KEY, rows, {None: DEFS, "choice": DEFS_CHOICE})
    s = C.summary(KEY, rows)
    print("wrote", len(rows), "->", out)
    C.show_samples(rows, 5, seed=SEED)
    C.append_manifest({
        "key": KEY, "family": C.FAMILY, "dataset": "CODAH (Websail-NU/CODAH full_data.tsv; no splits -> train)",
        "licence": LICENCE, "rows": len(rows), "qtype": "yesno+choice", "yesno_share": s["yes_share"],
        "edge_tags": sorted(t for t in s["edges"] if t),
        "notes": (f"Adversarially human-authored commonsense sentence completion. {s['n_yn']} yes/no 'is (X) the most "
                  f"sensible of the listed endings' + {s['n_ch']} 4-way letter choice (defs qid 'choice'). Edge tags "
                  f"from the authors' category codes (idiom/reference/polysemy/negation/quantitative)."),
    })


if __name__ == "__main__":
    main()
