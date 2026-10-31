"""REJECTED IN STRICT REVIEW (see rejected.json): ~15-20% wrong yes/no golds (polarity copied on negated rules,
hidden-evidence scenarios, denying-the-antecedent convention). main() refuses to run; raw/defs were deleted.

Build golden v14 rows for "sharc" (ShARC: Shaping Answers with Rules through Conversation; Saeidi et al., EMNLP 2018).

Source : official release zip https://sharc-data.github.io/data/sharc1-official.zip, taken from the site repo
         github.com/sharc-data/sharc-data.github.io pinned at commit 6e20dfe400a4da33aa9b671b29154dd4ce14dec4
         (sha256 of the zip is recorded in meta). ONLY json/sharc_train.json is read; sharc_dev.json and the
         (now public) sharc_test.json are never opened.
Licence: CC BY-SA 3.0, stated on the official data page https://sharc-data.github.io/data.html
         ("Dataset distribution under CC BY-SA 3.0", same repo/commit).
Texts  : rule snippets copied from government web pages (gov.uk, benefits.gov, humanservices.gov.au, irs.gov, ...);
         questions, scenarios and follow-up question/answer dialogues written by crowd workers; the answer label
         (Yes / No / Irrelevant / a follow-up question) is the crowd annotation (human, no model).
Task   : given the rule text, the user's question, the user's scenario and the follow-ups already answered, decide
         the reply: yes / no / irrelevant (rule text does not govern the question) / need more information (the gold
         reply is a follow-up question, i.e. an undecided condition remains).
Filters: negative-SCENARIO utterances (scenario pasted from an unrelated dialogue, listed in
         negative_sample_utterance_ids/sharc_negative_scenario_utterance_ids.txt) are dropped; negative-QUESTION
         utterances are the official "Irrelevant" class and are kept. Identical inputs with different gold replies are
         dropped (both). At most 16 rows per rule tree, dedupe of normalised states, word 13-gram decontamination
         against our local dev/eval files.
Balance: yes / no / need more information about equal, irrelevant capped (1,100). Seed 20261129.
"""
import json
import random
import re
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as C  # noqa: E402

KEY = "sharc"
SEED = 20261129
COMMIT = "6e20dfe400a4da33aa9b671b29154dd4ce14dec4"
URL = f"https://raw.githubusercontent.com/sharc-data/sharc-data.github.io/{COMMIT}/data/sharc1-official.zip"
LICENCE = ("CC BY-SA 3.0 (official data page https://sharc-data.github.io/data.html, 'Dataset distribution under "
           "CC BY-SA 3.0'; repo sharc-data/sharc-data.github.io @ 6e20dfe4)")
CACHE = C.CACHE_ROOT / "sharc"
QUOTA = {"yes": 2300, "no": 2300, "need more information": 2300, "irrelevant": 1100}
PER_TREE = 16
OPTIONS = ["yes", "no", "irrelevant", "need more information"]
INSTRUCTIONS = ("Using only the rule text, the user's scenario and the follow-up answers already given, what is the "
                "correct reply to the user's question?")
DEFS = {
    "yes": "The rule text governs the question and the scenario plus follow-up answers already settle it as yes: every "
           "condition needed for yes is met (for an either/or condition, one satisfied branch is enough).",
    "no": "The rule text governs the question and the known facts already settle it as no: a required condition is "
          "failed or an exclusion applies, even if other conditions are still unknown.",
    "irrelevant": "The rule text does not govern the user's question at all (it is about something else), so it "
                  "cannot answer the question either way.",
    "need more information": "The rule text governs the question, but the answer still depends on a condition that "
                             "neither the scenario nor any follow-up answer settles, so a clarifying question must "
                             "be asked first.",
}

EXC = re.compile(r"\b(unless|except|excluding|exempt|however|but not|won['’]t be|isn['’]t|doesn['’]t apply|"
                 r"does not apply|not eligible|can['’]t|cannot|only if)\b", re.I)
NEG = re.compile(r"\b(not|no|never|without|none|neither|nor)\b|n['’]t\b", re.I)
NUM = re.compile(r"\d")


def label(x):
    a = x["answer"].strip()
    if a in ("Yes", "No", "Irrelevant"):
        return a.lower()
    return "need more information"


def state_of(x):
    snip = x["snippet"].strip()
    lines = ["Rule text:", snip, "", f"User's question: {C.clean(x['question'])}",
             f"User's scenario: {C.clean(x['scenario']) if x['scenario'].strip() else '(none given)'}",
             "Follow-up questions already asked and answered:"]
    if x["history"]:
        for h in x["history"]:
            lines.append(f"- {C.clean(h['follow_up_question'])} {C.clean(h['follow_up_answer'])}")
    else:
        lines.append("(none)")
    return "\n".join(lines)


def edge_of(x, gold):
    if gold == "need more information":
        return "missing_info"
    if gold == "irrelevant":
        return None
    if x["evidence"]:
        return "implicit"
    txt = x["snippet"] + " " + x["question"]
    if EXC.search(txt):
        return "exception"
    if NEG.search(x["snippet"]):
        return "negation"
    if NUM.search(x["snippet"] + " " + x["scenario"]):
        return "numeric"
    return None


def main():
    if "--force-rejected" not in sys.argv:
        raise SystemExit("sharc was REJECTED in review (label noise); see golden_src/nli_logic_reasoning/rejected.json")
    z = C.fetch(URL, CACHE / "sharc1-official.zip")
    sha = C.sha256_file(z)
    with zipfile.ZipFile(z) as zf:
        train = json.loads(zf.read("sharc1-official/json/sharc_train.json"))
        negs = set(zf.read("sharc1-official/negative_sample_utterance_ids/"
                           "sharc_negative_scenario_utterance_ids.txt").decode().split())
    print(f"zip sha256 {sha[:16]}..., train utterances {len(train)}")

    rows = [x for x in train if x["utterance_id"] not in negs]
    print(f"dropped negative-scenario utterances: {len(train) - len(rows)}")

    # identical inputs with conflicting replies -> drop all copies
    by_state = defaultdict(list)
    for x in rows:
        x["gold"] = label(x)
        x["state"] = state_of(x)
        x["ns"] = C.norm(x["state"])
        by_state[x["ns"]].append(x)
    conflict = {k for k, v in by_state.items() if len({y["gold"] for y in v}) > 1}
    rows = [x for x in rows if x["ns"] not in conflict]
    print(f"conflicting identical inputs dropped: {len(conflict)} states")
    seen, uniq = set(), []
    for x in sorted(rows, key=lambda y: y["utterance_id"]):
        if x["ns"] in seen:
            continue
        seen.add(x["ns"])
        uniq.append(x)
    rows = uniq
    print(f"unique states: {len(rows)}")

    # decontam: user-written question+scenario and follow-up turns vs our dev/eval files (13-grams / whole >= 8 words)
    pats = {}
    for x in rows:
        ws = C.words(x["question"] + " " + x["scenario"])
        ps = C.ngrams(ws, 13)
        qs = C.words(x["question"])
        if len(qs) >= 8:
            ps.add(" ".join(qs))
        pats[x["utterance_id"]] = ps
    snip_pats = {}
    for x in rows:
        snip_pats.setdefault(x["tree_id"], C.ngrams(C.words(x["snippet"]), 13))
    hits = C.local_hits(set().union(*pats.values(), *snip_pats.values()))
    rows = [x for x in rows if not (pats[x["utterance_id"]] & hits) and not (snip_pats[x["tree_id"]] & hits)]
    print(f"after decontam: {len(rows)}")

    rng = random.Random(SEED)
    rng.shuffle(rows)
    pools = defaultdict(list)
    for x in rows:
        pools[x["gold"]].append(x)
    print("pool sizes:", {k: len(v) for k, v in pools.items()})
    picked = C.balanced_pick(pools, QUOTA, rng, key_fn=lambda x: x["tree_id"],
                             cap_fn=lambda g, x, t: g[t] < PER_TREE)

    out = []
    for x in picked:
        out.append({
            "key": KEY,
            "rid": f"sharc_train_{x['utterance_id']}",
            "state": x["state"],
            "instructions": INSTRUCTIONS,
            "options": OPTIONS,
            "gold": x["gold"],
            "soft": None,
            "meta": {"dataset": "https://sharc-data.github.io (sharc1-official.zip)", "config": "sharc1-official",
                     "revision": COMMIT, "licence": LICENCE, "split": "train", "orig_label": x["answer"],
                     "family": C.FAMILY, "edge": edge_of(x, x["gold"]), "tree_id": x["tree_id"],
                     "source_url": x["source_url"], "source_sha256": sha},
        })
    rng.shuffle(out)
    C.validate_rows(KEY, out, {None: DEFS})
    C.write_rows(KEY, out)
    C.write_defs(KEY, DEFS)
    C.report(KEY, out)
    print("distinct trees:", len({r["meta"]["tree_id"] for r in out}))
    e = Counter(r["meta"]["edge"] for r in out)
    C.append_manifest({
        "key": KEY, "family": C.FAMILY, "dataset": "ShARC (sharc1-official, train)", "licence": LICENCE,
        "rows": len(out), "qtype": "choice (yes / no / irrelevant / need more information)", "yesno_share": None,
        "edge_tags": sorted(k for k in e if k),
        "notes": "Human rule-application decisions over government eligibility rules (conditions, either/or, "
                 "exclusions); need-more-information = crowd reply was a clarifying question. Negative-scenario "
                 "utterances dropped; <=16 rows per rule tree; dev/test never read.",
    })
    if "--show" in sys.argv:
        C.show_samples(out, 5)


if __name__ == "__main__":
    main()
