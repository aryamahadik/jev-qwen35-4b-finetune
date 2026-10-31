"""Build golden v14 rows for "babi_logic" (bAbI tasks v1.2, en-10k; Weston et al., 2015).

Source : bAbI tasks_1-20_v1-2 tarball (Facebook AI Research), fetched from the long-standing public copy
         https://s3.amazonaws.com/text-datasets/babi_tasks_1-20_v1-2.tar.gz (the dl.fbaipublicfiles.com URL now
         returns 403); sha256 recorded in meta. ONLY en-10k/*_train.txt of tasks 6, 9, 10, 15, 17, 18 are read
         (the *_test.txt files are never read).
Licence: CC BY 3.0, stated in tasks_1-20_v1-2/LICENSE.txt inside the release ("CC License / bAbI tasks data /
         Copyright (c) 2015-present, Facebook, Inc. ... Attribution 3.0 Unported"); the generator code
         (github.com/facebookarchive/bAbI-tasks) is BSD.
Texts  : simulator-generated stories and questions; answers follow by construction (no model).
Tasks  : qa6 yes/no location questions (most recent statement wins), qa9 simple negation ("no longer in", "not in"),
         qa17 positional reasoning (left/right/above/below chains), qa18 size reasoning (bigger / fits inside chains)
         -> yes/no ; qa10 indefinite knowledge ("either in X or Y") -> yes / no / maybe ; qa15 basic deduction
         (species membership + species fear) -> 4-way choice. qa16 (induction) is NOT used: its answers are
         plausible generalisations, not entailments.
Selection: one question per story and every story text used once (the story prefix up to that question is
         the state), yes/no balanced 50/50
         within each task, seed 20261134.
"""
import random
import re
import sys
import tarfile
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as C  # noqa: E402

KEY = "babi_logic"
SEED = 20261134
URL = "https://s3.amazonaws.com/text-datasets/babi_tasks_1-20_v1-2.tar.gz"
LICENCE = ("CC BY 3.0 (tasks_1-20_v1-2/LICENSE.txt inside the official release: 'bAbI tasks data, Copyright (c) "
           "2015-present, Facebook, Inc.', Creative Commons Attribution 3.0 Unported)")
CACHE = C.CACHE_ROOT / "babi"
TASKS = {  # task file stem: (qid, quota per gold label)
    "qa6_yes-no-questions": ("yn", {"yes": 250, "no": 250}),
    "qa9_simple-negation": ("yn", {"yes": 500, "no": 500}),
    "qa17_positional-reasoning": ("yn", {"yes": 350, "no": 350}),
    "qa18_size-reasoning": ("yn", {"yes": 350, "no": 350}),
    "qa10_indefinite-knowledge": ("ynm", {"yes": 400, "no": 400, "maybe": 400}),
    "qa15_basic-deduction": ("deduce", {"cat": 125, "mouse": 125, "sheep": 125, "wolf": 125}),
}
DEFS = {
    "yn": {
        "yes": "Combining the story's statements, the answer is yes. Stated positions are direct (above = directly "
               "above); in questions above/below compare only height and left/right only sideways position; "
               "bigger/fits-inside chain; a person is where the latest statement puts them.",
        "no": "Combining the story's statements in the same way, the answer is no: for example the person has since "
              "moved or is said to be no longer or not there, or the relation holds the other way round.",
    },
    "ynm": {
        "yes": "The most recent statement about the person places them definitely in the asked place.",
        "no": "The most recent statement about the person places them somewhere else, or says they are in one of "
              "two places that does not include the asked place.",
        "maybe": "The most recent statement about the person only says they are in one of two places (either ... or "
                 "...), one of which is the asked place, so it cannot be decided.",
    },
    "deduce": {
        "cat": "Chaining the story's facts (the person belongs to a species, and that species is afraid of cats) "
               "shows the person is afraid of cats.",
        "mouse": "Chaining the story's facts (the person belongs to a species, and that species is afraid of mice) "
                 "shows the person is afraid of mice.",
        "sheep": "Chaining the story's facts (the person belongs to a species, and that species is afraid of sheep) "
                 "shows the person is afraid of sheep.",
        "wolf": "Chaining the story's facts (the person belongs to a species, and that species is afraid of wolves) "
                "shows the person is afraid of wolves.",
    },
}
OPTIONS = {"yn": ["yes", "no"], "ynm": ["yes", "no", "maybe"], "deduce": ["cat", "mouse", "sheep", "wolf"]}
LINE = re.compile(r"^(\d+) (.*)$")


def parse(text):
    """Yield (story_index, question_index, prefix_statements, question, answer, supporting line texts)."""
    story, lines_by_id = [], {}
    si = -1
    qi = 0
    for raw in text.splitlines():
        m = LINE.match(raw.strip())
        if not m:
            continue
        n, rest = int(m.group(1)), m.group(2)
        if n == 1:
            story, lines_by_id = [], {}
            si += 1
            qi = 0
        if "\t" in rest:
            q, a, sup = (rest.split("\t") + ["", ""])[:3]
            sup_txt = [lines_by_id.get(int(s), "") for s in sup.split() if s.isdigit()]
            yield si, qi, list(story), q.strip(), a.strip(), sup_txt
            qi += 1
        else:
            story.append(rest.strip())
            lines_by_id[n] = rest.strip()


def edge_of(stem, ans, sup):
    if stem.startswith("qa9"):
        return "negation" if any(re.search(r"\bno longer\b|\bnot\b", s) for s in sup) else "temporal"
    if stem.startswith("qa10"):
        return "missing_info" if ans == "maybe" else "temporal"
    if stem.startswith("qa6"):
        return "temporal"
    return "multi_hop"


def instruction_of(stem, q):
    q = q.strip()
    if stem.startswith("qa15"):
        m = re.match(r"What is (\w+) afraid of\?", q)
        name = m.group(1).capitalize()
        return f"Based only on the story, what is {name} afraid of?"
    return f"Based only on the story, answer this question: {q}"


def main():
    tgz = C.fetch(URL, CACHE / "babi_tasks_1-20_v1-2.tar.gz")
    sha = C.sha256_file(tgz)
    texts = {}
    with tarfile.open(tgz) as tf:
        lic = tf.extractfile("tasks_1-20_v1-2/LICENSE.txt").read().decode()
        assert "Attribution 3.0" in lic
        for stem in TASKS:
            texts[stem] = tf.extractfile(f"tasks_1-20_v1-2/en-10k/{stem}_train.txt").read().decode()
    print(f"tarball sha256 {sha[:16]}...")

    rng = random.Random(SEED)
    out = []
    seen = set()
    for stem, (qid, quota) in TASKS.items():
        by_story = defaultdict(list)
        for si, qi, story, q, a, sup in parse(texts[stem]):
            by_story[si].append((qi, story, q, a, sup))
        stories = sorted(by_story)
        rng.shuffle(stories)
        got = Counter()
        for si in stories:
            if all(got[k] >= v for k, v in quota.items()):
                break
            cands = [c for c in by_story[si] if c[3] in quota and got[c[3]] < quota[c[3]]]
            if not cands:
                continue
            # prefer the label that is furthest from its quota
            cands.sort(key=lambda c: (got[c[3]] / quota[c[3]], c[0]))
            best = [c for c in cands if got[c[3]] / quota[c[3]] == got[cands[0][3]] / quota[cands[0][3]]]
            qi, story, q, a, sup = rng.choice(best)
            state = "Story:\n" + "\n".join(story)
            ins = instruction_of(stem, q)
            k = C.norm(state)  # one row per distinct story text across all tasks (no duplicated states)
            if k in seen:
                continue
            seen.add(k)
            got[a] += 1
            out.append({
                "key": KEY,
                "rid": f"babi_{stem.split('_')[0]}_train_s{si}_q{qi}",
                "state": state,
                "instructions": ins,
                "options": OPTIONS[qid],
                "gold": a,
                "soft": None,
                "meta": {"dataset": "bAbI tasks v1.2 (Facebook AI Research), en-10k", "config": stem,
                         "revision": f"tasks_1-20_v1-2 tarball sha256 {sha}", "licence": LICENCE, "split": "train",
                         "orig_label": a, "family": C.FAMILY, "edge": edge_of(stem, a, sup), "defs": qid},
            })
        print(stem, dict(got))
    rng.shuffle(out)
    C.validate_rows(KEY, out, DEFS)
    C.write_rows(KEY, out)
    for q, d in DEFS.items():
        C.write_defs(KEY, d, qid=q)
    share = C.report(KEY, out)
    e = Counter(r["meta"]["edge"] for r in out)
    C.append_manifest({
        "key": KEY, "family": C.FAMILY, "dataset": "bAbI tasks v1.2 en-10k train (tasks 6, 9, 10, 15, 17, 18)",
        "licence": LICENCE, "rows": len(out),
        "qtype": "mixed: yes/no (yn: tasks 6/9/17/18) + yes/no/maybe (ynm: task 10) + 4-way deduction (task 15)",
        "yesno_share": round(share, 4) if share is not None else None, "edge_tags": sorted(k for k in e if k),
        "notes": "Exact-label toy reasoning: negation ('no longer', 'not in'), indefinite knowledge -> maybe, "
                 "state tracking (most recent statement wins), transitive positional and size chains, syllogistic "
                 "deduction. Kept small on purpose (simple language).",
    })
    if "--show" in sys.argv:
        C.show_samples(out, 6)


if __name__ == "__main__":
    main()
