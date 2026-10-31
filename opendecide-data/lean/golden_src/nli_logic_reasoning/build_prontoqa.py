"""Build golden v14 rows for "prontoqa" (PrOntoQA; Saparov & He, ICLR 2023 - the official generator).

Source : github.com/asaparov/prontoqa pinned at commit 0a6412b6fddf46324a1cb96e066dd7b3d89b87d6 (run_experiment.py,
         theory.py, syntax.py, proof.py, fol.py, prompt.py, bad_patterns.txt; sha256 of each file in meta). The
         generator is run here on CPU in its data-only mode (--model-name json, no model is called) with our own
         seed 20261136, so no published test example is reused (the released data use seed 62471893).
Licence: Apache-2.0 (LICENSE file at the root of the repository, same commit).
Texts  : program-generated ontologies ("Every X is a Y", "Ys are not Z") about one individual, rendered by the
         authors' templates; the True/False label follows by construction from the modus-ponens proof (no model).
         Three ontology types: fictional words (wumpus, ...), the true taxonomy, and a FALSE (counterfactual)
         taxonomy ("Animals are moths") where the context must be followed against world knowledge.
Task   : yes/no "given only the context, is the statement true?" (True -> yes, False -> no: the context proves the
         opposite). Hops 1-5 (false ontology 1-3: the generator stalls beyond), random sentence order; relevant distractors for the fictional and false ontologies
         (the generator supports the true ontology only without distractors).
Selection: up to 800 rows per ontology type, yes/no 50/50, dedupe of near-exact states: the key ignores the
         individual's name (Wren / Rex / 131071 ...), the sentence order and 'Every' vs 'Each' (strict review: the
         plain key let 163 name-only / order-only variants of the same true-ontology problem through).
"""
import glob
import json
import os
import random
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as C  # noqa: E402

KEY = "prontoqa"
SEED = 20261136
COMMIT = "0a6412b6fddf46324a1cb96e066dd7b3d89b87d6"
BASE = f"https://raw.githubusercontent.com/asaparov/prontoqa/{COMMIT}/"
FILES = ["run_experiment.py", "theory.py", "syntax.py", "proof.py", "fol.py", "prompt.py", "bad_patterns.txt",
         "LICENSE"]
LICENCE = "Apache-2.0 (LICENSE at root of github.com/asaparov/prontoqa @ 0a6412b6)"
CODE = C.CACHE_ROOT / "prontoqa_code"
TRIALS = 240
PER_ONTOLOGY = {"fictional": 800, "true": 800, "false": 800}
MAX_HOPS = {"fictional": 5, "true": 5, "false": 3}  # the false ontology runs out of concepts beyond 3 hops (generator stalls)
INSTRUCTIONS = ("Using only the statements in the context (even where they contradict real-world facts), is the "
                "statement true?")
DEFS = {
    "yes": "Chaining the context's rules (every X is a Y; Ys are, or are not, Z) from what it says about the "
           "individual proves the statement, even if the context contradicts real-world facts.",
    "no": "Chaining the context's rules from what it says about the individual proves the opposite of the "
          "statement (for example the context says members of a class are not Z).",
}


def near_key(context, stmt):
    """Near-exact duplicate key: individual's name masked, sentence order and Every/Each wording ignored."""
    name = stmt.split(" ", 1)[0]
    def canon(s):
        s = re.sub(r"(?<![A-Za-z0-9])" + re.escape(name) + r"(?![A-Za-z0-9])", "NAME", s)
        s = re.sub(r"^(every|each) ", "every ", s.strip().lower())
        return " ".join(C.words(s))
    sents = sorted(canon(x) for x in context.split(".") if x.strip())
    return " | ".join(sents) + " || " + canon(stmt)


def main():
    CODE.mkdir(parents=True, exist_ok=True)
    shas = {}
    for f in FILES:
        p = C.fetch(BASE + f, CODE / f)
        shas[f] = C.sha256_file(p)
    assert "Apache License" in (CODE / "LICENSE").read_text()
    outdir = CODE / "out"
    for ont in PER_ONTOLOGY:
        od = outdir / ont
        od.mkdir(parents=True, exist_ok=True)
        for old in glob.glob(str(od / "*.json")) + glob.glob(str(CODE / f"*seed{SEED}.json")):
            os.remove(old)
        cmd = [sys.executable, str(CODE / "run_experiment.py"), "--model-name", "json", "--model-size", "dummy",
               "--ordering", "random", "--num-trials", str(TRIALS), "--few-shot-examples", "0", "--ontology", ont,
               "--min-hops", "1", "--max-hops", str(MAX_HOPS[ont]), "--hops-skip", "1", "--deduction-rule", "ModusPonens",
               "--seed", str(SEED)]
        if ont == "true":  # the generator supports the true ontology only without distractors
            cmd += ["--distractors", "none", "--test-distractors", "none"]
        env = dict(os.environ, PYTHONHASHSEED="0")
        # run_experiment.py reads bad_patterns.txt from the cwd and writes its json there
        r = subprocess.run(cmd, cwd=CODE, env=env, capture_output=True, text=True)
        assert r.returncode == 0, r.stderr[-2000:]
        made = glob.glob(str(CODE / f"*seed{SEED}.json"))
        assert made, r.stdout[-2000:]
        for f in made:
            os.replace(f, od / Path(f).name)

    cands = defaultdict(list)
    seen = set()
    for f in sorted(glob.glob(str(outdir / "*" / f"*seed{SEED}.json"))):
        name = Path(f).name
        hops = int(name.split("hop")[0])
        ont = Path(f).parent.name
        for ex_id, ex in json.load(open(f)).items():
            t = ex["test_example"]
            q = t["query"]
            assert q.startswith("True or false: "), q
            stmt = q[len("True or false: "):]
            state = f"Context: {t['question']}\n\nStatement: {stmt}"
            k = near_key(t["question"], stmt)
            if k in seen:
                continue
            seen.add(k)
            cands[(ont, t["answer"])].append({"ont": ont, "hops": hops, "ex": ex_id, "state": state, "stmt": stmt,
                                             "answer": t["answer"], "file": name})
    print("candidates:", {k: len(v) for k, v in cands.items()})

    rng = random.Random(SEED)
    out = []
    for ont, n in PER_ONTOLOGY.items():
        for ans in ("True", "False"):
            pool = sorted(cands[(ont, ans)], key=lambda c: (c["hops"], c["ex"]))
            rng.shuffle(pool)
            # spread over hop counts
            byhop = defaultdict(list)
            for c in pool:
                byhop[c["hops"]].append(c)
            pick, hops = [], sorted(byhop)
            while len(pick) < n // 2 and any(byhop[h] for h in hops):
                for h in hops:
                    if byhop[h] and len(pick) < n // 2:
                        pick.append(byhop[h].pop())
            for c in pick:
                neg = " not " in f" {c['stmt']} "
                edge = ("hypothetical" if ont == "false" else "negation" if neg else
                        "multi_hop" if c["hops"] >= 2 else None)
                out.append({
                    "key": KEY,
                    "rid": f"prontoqa_s{SEED}_{ont}_{c['hops']}hop_{c['ex']}",
                    "state": c["state"],
                    "instructions": INSTRUCTIONS,
                    "options": ["yes", "no"],
                    "gold": "yes" if c["answer"] == "True" else "no",
                    "soft": None,
                    "meta": {"dataset": "github.com/asaparov/prontoqa (generator, json mode)",
                             "config": f"ModusPonens, {ont} ontology, {c['hops']} hops, " + ("no distractors" if ont == "true" else "relevant distractors"),
                             "revision": COMMIT, "licence": LICENCE, "split": "train", "orig_label": c["answer"],
                             "family": C.FAMILY, "edge": edge, "hops": c["hops"], "generator_seed": SEED,
                             "code_sha256": shas},
                })
    rng.shuffle(out)
    C.validate_rows(KEY, out, {None: DEFS})
    C.write_rows(KEY, out)
    C.write_defs(KEY, DEFS)
    share = C.report(KEY, out)
    print("per ontology / hops:", dict(Counter((r["meta"]["config"].split(",")[1].strip(), r["meta"]["hops"])
                                               for r in out)))
    e = Counter(r["meta"]["edge"] for r in out)
    C.append_manifest({
        "key": KEY, "family": C.FAMILY, "dataset": "PrOntoQA generator (ModusPonens; fictional / true / false "
                                                   "ontologies), own seed", "licence": LICENCE,
        "rows": len(out), "qtype": "yesno", "yesno_share": round(share, 4), "edge_tags": sorted(k for k in e if k),
        "notes": "Exact-label syllogistic chains with negated properties and distractor concepts; one third uses a "
                 "counterfactual taxonomy so the model must follow the given premises over world knowledge.",
    })
    if "--show" in sys.argv:
        C.show_samples(out, 6)


if __name__ == "__main__":
    main()
