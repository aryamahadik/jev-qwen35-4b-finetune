"""Build golden v14 rows for "conditionalqa" (ConditionalQA; Sun, Cohen & Salakhutdinov, ACL 2022).

Source : github.com/haitian-sun/ConditionalQA pinned at commit 77bd295952daf415548b3244db10880d3d55cfe0,
         v1_0/train.json and v1_0/documents.json ONLY (dev.json / test_no_answer.json never downloaded).
Licence: CC BY-SA 4.0, stated on the official dataset page https://haitian-sun.github.io/conditionalqa/
         ("CC BY-SA 4.0 License", getting-started section). Documents are gov.uk guidance pages (Open Government
         Licence v3.0, compatible).
Texts  : questions and scenarios written by crowd workers who read the gov.uk page; answers, conditions and
         not-answerable flags annotated by humans (no model).
Task   : 4-way decision for yes/no questions: yes / no (unconditional) ; depends on unstated conditions (the gold
         answer carries conditions, or yes and no both apply under different conditions) ; not answerable (the
         official not_answerable flag, kept only for questions phrased as yes/no questions).
         Span (non yes/no) answers are dropped.
State  : the whole gov.uk document (headings, paragraphs, list items and table rows rendered as text) + the
         scenario + the question. Documents longer than 20,000 characters are dropped (not truncated), so every
         condition stays visible.
Seed 20261130; dedupe of normalised states; word 13-gram decontamination against our local dev/eval files.
"""
import json
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as C  # noqa: E402

KEY = "conditionalqa"
SEED = 20261130
COMMIT = "77bd295952daf415548b3244db10880d3d55cfe0"
BASE = f"https://raw.githubusercontent.com/haitian-sun/ConditionalQA/{COMMIT}/v1_0/"
LICENCE = ("CC BY-SA 4.0 (official page https://haitian-sun.github.io/conditionalqa/ , 'CC BY-SA 4.0 License'); "
           "documents: gov.uk, Open Government Licence v3.0")
CACHE = C.CACHE_ROOT / "conditionalqa"
MAX_DOC_CHARS = 20000
OPTIONS = ["yes", "no", "depends on unstated conditions", "not answerable"]
INSTRUCTIONS = "Applying the guidance document to the user's scenario, what is the answer to the user's question?"
DEFS = {
    "yes": "The document, applied to the facts in the scenario, answers yes with no requirement left open: every "
           "condition that matters is met or settled by the scenario.",
    "no": "The document, applied to the facts in the scenario, answers no with no requirement left open.",
    "depends on unstated conditions": "The document answers yes or no only if further requirements it names are "
                                      "met (or gives yes in one case and no in another), and the scenario does not "
                                      "say which case applies.",
    "not answerable": "The document does not contain the information needed to answer this question for this "
                      "scenario, so neither yes nor no is supported.",
}
AUX = r"(can|could|do|does|did|is|are|am|was|were|will|would|should|shall|must|may|might|has|have|had)"
YN_START = re.compile(rf"^\s*{AUX}\b", re.I)
YN_AFTER_CLAUSE = re.compile(rf"^\s*(if|as|since|given|after|now|so|because|when|while|although|though)\b[^?]*,\s*"
                             rf"{AUX}\b", re.I)
WH = re.compile(r"\b(what|which|who|whom|whose|how|when|where|why)\b", re.I)


def is_yes_no_question(q):
    """Only questions phrased as yes/no questions (used to keep not-answerable items comparable)."""
    q2 = re.sub(r"^\s*(when|while)\b[^,]*,", "", q)  # a leading 'when ...,' clause is not a wh-question
    if WH.search(q2):
        return False
    return bool(YN_START.search(q) or YN_AFTER_CLAUSE.search(q))


NEG = re.compile(r"\b(not|no|never|without|none|neither|nor)\b|n['’]t\b", re.I)
TAG = re.compile(r"<[^>]+>")


def render(contents):
    out = []
    for s in contents:
        m = re.match(r"\s*<(\w+)", s)
        tag = m.group(1).lower() if m else "p"
        txt = C.clean(TAG.sub(" ", s)).replace(" ,", ",").replace(" .", ".")
        if not txt:
            continue
        if tag == "h1":
            out.append(f"\n# {txt}")
        elif tag == "h2":
            out.append(f"\n## {txt}")
        elif tag in ("h3", "h4"):
            out.append(f"\n### {txt}")
        elif tag == "li":
            out.append(f"- {txt}")
        elif tag == "tr":
            out.append(f"| {txt} |")
        else:
            out.append(txt)
    return "\n".join(out).strip()


def gold_of(x):
    if x["not_answerable"]:
        return "not answerable"
    ans = x["answers"]
    kinds = {a[0].strip().lower() for a in ans}
    if not kinds <= {"yes", "no"}:
        return None  # span answer
    cond = any(a[1] for a in ans)
    if len(kinds) > 1 or cond:
        return "depends on unstated conditions"
    return kinds.pop()


def main():
    tr = C.fetch(BASE + "train.json", CACHE / "train.json")
    dc = C.fetch(BASE + "documents.json", CACHE / "documents.json")
    sha = {"train.json": C.sha256_file(tr), "documents.json": C.sha256_file(dc)}
    train = json.load(open(tr))
    docs = {d["url"]: d for d in json.load(open(dc))}
    print(f"train questions {len(train)}, documents {len(docs)}")

    rows, drop = [], Counter()
    for x in train:
        g = gold_of(x)
        if g is None:
            drop["span answer"] += 1
            continue
        if g == "not answerable" and not is_yes_no_question(x["question"]):
            drop["not-answerable, not a yes/no question"] += 1
            continue
        d = docs.get(x["url"])
        if d is None:
            drop["no document"] += 1
            continue
        body = render(d["contents"])
        if len(body) > MAX_DOC_CHARS:
            drop["document > 20k chars"] += 1
            continue
        state = (f"Guidance document: {C.clean(d['title'])}\n{body}\n\n"
                 f"User's scenario: {C.clean(x['scenario'])}\nUser's question: {C.clean(x['question'])}")
        x.update(gold=g, state=state, doclen=len(body))
        rows.append(x)
    print("dropped:", dict(drop), "kept:", len(rows))

    # dedupe (the same scenario+question is never asked twice about one page)
    seen, uniq = set(), []
    for x in rows:
        k = C.norm(x["state"])
        if k in seen:
            continue
        seen.add(k)
        uniq.append(x)
    rows = uniq

    pats = {x["id"]: C.ngrams(C.words(x["scenario"] + " " + x["question"]), 13) for x in rows}
    hits = C.local_hits(set().union(*pats.values()))
    rows = [x for x in rows if not (pats[x["id"]] & hits)]

    rng = random.Random(SEED)
    rng.shuffle(rows)

    def edge(x):
        g = x["gold"]
        if g in ("depends on unstated conditions", "not answerable"):
            return "missing_info"
        if x["doclen"] > 8000:
            return "long_context"
        if NEG.search(x["question"]):
            return "negation"
        return None

    out = []
    for x in rows:
        out.append({
            "key": KEY,
            "rid": f"conditionalqa_{x['id']}",
            "state": x["state"],
            "instructions": INSTRUCTIONS,
            "options": OPTIONS,
            "gold": x["gold"],
            "soft": None,
            "meta": {"dataset": "github.com/haitian-sun/ConditionalQA", "config": "v1_0", "revision": COMMIT,
                     "licence": LICENCE, "split": "train",
                     "orig_label": {"answers": x["answers"], "not_answerable": x["not_answerable"]},
                     "family": C.FAMILY, "edge": edge(x), "source_url": x["url"], "source_sha256": sha},
        })
    C.validate_rows(KEY, out, {None: DEFS})
    C.write_rows(KEY, out)
    C.write_defs(KEY, DEFS)
    C.report(KEY, out)
    e = Counter(r["meta"]["edge"] for r in out)
    C.append_manifest({
        "key": KEY, "family": C.FAMILY, "dataset": "ConditionalQA v1.0 (train)", "licence": LICENCE,
        "rows": len(out), "qtype": "choice (yes / no / depends on unstated conditions / not answerable)",
        "yesno_share": None, "edge_tags": sorted(k for k in e if k),
        "notes": "Human questions over full gov.uk guidance pages; conditional answers (requirements the scenario "
                 "does not settle) mapped to 'depends'; long documents kept whole (<=20k chars), never truncated.",
    })
    if "--show" in sys.argv:
        C.show_samples(out, 5)


if __name__ == "__main__":
    main()
