"""Build raw rows for bbh_mistake: step-level logical-mistake judging on BIG-Bench Mistake (Tyen et al., Findings of
ACL 2024, "LLMs cannot find reasoning errors, but can correct them given the error location").

Source : GitHub WHGTyen/BIG-Bench-Mistake pinned to commit 9b010ce17150b79411dc31659779d7524c03f436: the five task
         files word_sorting / tracking_shuffled_objects / logical_deduction / multistep_arithmetic / dyck_languages
         .jsonl. The release has no splits (counts as train).
Licence: Apache-2.0 (repo LICENSE at the pinned commit). Task inputs come from BIG-Bench (Apache-2.0).
Texts  : BIG-Bench Hard questions; chain-of-thought traces from PaLM 2 (the object being judged), split into
         'Thought N' steps.
Labels : location of the FIRST logical mistake (0-based; null = no mistake). Human annotators (>= 3 per trace,
         majority label; Krippendorff alpha 0.979-0.998) for four tasks; for Dyck languages mostly the authors'
         rule-based annotator (annotate_dyck_languages.py: the model's stack step is compared with the algorithmic
         stack; label by construction), humans for traces it could not parse. No model labels.
Rows   : one row per trace. The judged step is either the first mistake (flawed) or a step strictly before it (every
         step before the first mistake is correct by the annotation); for traces without a mistake any step, with the
         final answer step preferred. Steps after the first mistake are never judged (they are unlabelled).
         Two framings (qids): 'flaw' ("Does the last thought contain a logical mistake?") and 'ok' ("Is the last
         thought logically correct...?").
Review fixes: traces with no annotated mistake but a wrong final answer are dropped (annotation gaps: 30 such
         traces, e.g. an arithmetic trace whose 'correct' step computes -6 + 5 - 72 = -67); multi-step arithmetic
         rows whose judged 'Let's calculate X = ...' step is re-evaluated exactly (Python arithmetic against X's
         definition in Thought 1) and disagrees with the human label are dropped.
Filters: exact-duplicate inputs dropped; at most 500 traces per task (Dyck languages has 986); decontamination of the question text against label-NLI, local
         train/dev/eval files and JevBench. Balanced to 50% flawed per task where possible.
Deterministic (seed 20261204). CPU only.
"""
import collections
import json
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _jv_common as C  # noqa: E402

KEY = "bbh_mistake"
SEED = 20261204
COMMIT = "9b010ce17150b79411dc31659779d7524c03f436"
BASE = f"https://raw.githubusercontent.com/WHGTyen/BIG-Bench-Mistake/{COMMIT}/"
TASKS = ["word_sorting", "tracking_shuffled_objects", "logical_deduction", "multistep_arithmetic", "dyck_languages"]
SHAS = {"word_sorting.jsonl": "e9deb2c57f7fc87f2d10336bc350c93c599bd3f483e3fb0ffb54854257ef8159", "tracking_shuffled_objects.jsonl": "637282d5721b76fb5a1d3b1eedef0b476b2a6634bd91f281ca69b782a670bd42", "logical_deduction.jsonl": "f521efec7c975558ac6a35e8d66a84bc17ff696865c622bc93604307bc63f0cd", "multistep_arithmetic.jsonl": "b3f9a99e62bdcb758d6cafc531a43f6d6bca6812190cce4f982d1c01ac0767d3", "dyck_languages.jsonl": "38cf1f524d119ce8d12c21d933ed8aa8d82bb5a36c4f6e71ed499ede234512f4", "LICENSE": "c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4", "README.md": "82df2ff95899fa17dcc07378e4cdcc4ed3f17540a75bdf46da74cdf345cdd009", "annotate_dyck_languages.py": "850eb69ffc0e973636a58841e871812e664eac1425ab44eedaddb27e2b9253ab"}
LICENCE = (f"Apache-2.0 (https://github.com/WHGTyen/BIG-Bench-Mistake/blob/{COMMIT}/LICENSE; BIG-Bench task inputs "
           "Apache-2.0)")
DATASET = "WHGTyen/BIG-Bench-Mistake (5 BIG-Bench Hard tasks, first-mistake annotations)"
MAX_PER_TASK = 500  # Dyck has 986 traces; keep the task mix balanced
TASK_NAME = {"word_sorting": "word sorting", "tracking_shuffled_objects": "tracking shuffled objects",
             "logical_deduction": "logical deduction", "multistep_arithmetic": "multi-step arithmetic",
             "dyck_languages": "Dyck languages (bracket completion)"}

Q = {
    "flaw": "Does the last thought in this chain of reasoning contain a logical mistake?",
    "ok": "Is the last thought in this chain of reasoning logically correct, given the question and the earlier thoughts?",
}
DEFS = {
    "flaw": {
        "yes": "The last thought contains a logical mistake: something it states or derives is wrong given the question "
               "and the earlier (correct) thoughts, e.g. a wrong arithmetic result, a misread or dropped item, a wrong "
               "swap or position, a wrong ordering, or a wrong bracket on the stack.",
        "no": "The last thought is logically correct: everything it states or derives follows correctly from the "
              "question and the earlier thoughts; wording, restating the task, or planning without new claims is not "
              "a mistake.",
    },
    "ok": {
        "yes": "The last thought is logically correct: everything it states or derives follows correctly from the "
               "question and the earlier thoughts; wording, restating the task, or planning without new claims is not "
               "a mistake.",
        "no": "The last thought contains a logical mistake: something it states or derives is wrong given the question "
              "and the earlier thoughts, e.g. a wrong arithmetic result, a misread or dropped item, a wrong swap or "
              "position, a wrong ordering, or a wrong bracket on the stack.",
    },
}
EDGE = {"word_sorting": "quantifier", "tracking_shuffled_objects": "temporal", "logical_deduction": "multi_hop",
        "multistep_arithmetic": "numeric", "dyck_languages": "long_context"}


_ARITH_OK = re.compile(r"[0-9\s+\-*()]+")


def _ev(expr):
    expr = expr.strip()
    if not expr or not _ARITH_OK.fullmatch(expr):
        return None
    try:
        return eval(expr, {"__builtins__": {}}, {})  # digits, + - * and brackets only (checked above)
    except Exception:
        return None


def arith_check(steps, k):
    """Exact check of a multistep-arithmetic step 'Let's calculate X = e0 = e1 = ... = v.': True if every expression
    has the value of e0, False if any differs, None if the step is not of that form or e0 is not X's definition as
    written in Thought 1 (then the step cannot be checked on its own)."""
    m = re.match(r"^Let's calculate ([A-Z]) = (.*?)\.?\s*$", steps[k].strip())
    if not m:
        return None
    parts = m.group(2).split(" = ")
    if f"{m.group(1)} = {parts[0].strip()}" not in " ".join(steps[0].split()):
        return None
    vals = [_ev(p) for p in parts]
    if any(v is None for v in vals):
        return None
    return all(v == vals[0] for v in vals)


def render(task, inp, steps, k):
    lines = [f"Task: {TASK_NAME[task]}", "", "Question:", inp.strip(), ""]
    if k:
        lines.append("Reasoning so far:")
        for i in range(k):
            lines.append(f"Thought {i + 1}: {steps[i].strip()}")
    else:
        lines.append("Reasoning so far: (none)")
    lines += ["", f"Last thought (Thought {k + 1}):", steps[k].strip()]
    return "\n".join(lines)


def main():
    rng = random.Random(SEED)
    cache = C.CACHE / "bbmistake"
    for rel, sha in SHAS.items():
        C.fetch(BASE + rel, cache / rel, sha)
    stats = collections.Counter()
    recs = []
    seen = set()
    for t in TASKS:
        for i, line in enumerate(open(cache / f"{t}.jsonl")):
            o = json.loads(line)
            n = " ".join(o["input"].split())  # raw (bracket sequences normalise to nothing)
            if n in seen:
                stats["dup_input"] += 1
                continue
            seen.add(n)
            steps = [s for s in o["steps"]]
            if not steps or any(not s.strip() for s in steps):
                stats["bad_steps"] += 1
                continue
            if o["mistake_index"] is None and " ".join(str(o.get("answer") or "").split()) != " ".join(
                    str(o["target"]).split()):
                # review fix: 'no mistake' but a wrong final answer is an annotation gap (e.g. arithmetic trace 1:
                # B = (-6 + 5 - 72) ... = -70 left unlabelled), so its steps cannot be trusted as correct
                stats["drop_nomistake_wrong_answer"] += 1
                continue
            recs.append({"rid": f"{t}-{i}", "task": t, "input": o["input"], "steps": steps,
                         "m": o["mistake_index"], "target": o["target"], "answer": o.get("answer")})
    hits = C.decon({r["rid"]: [r["input"]] for r in recs}, cache_name=KEY)
    recs = [r for r in recs if r["rid"] not in hits]
    stats["after_decon"] = len(recs)

    rows = []
    for t in TASKS:
        pool = sorted([r for r in recs if r["task"] == t], key=lambda r: r["rid"])
        rng.shuffle(pool)
        pool = pool[:MAX_PER_TASK]
        can_flaw = [r for r in pool if r["m"] is not None]
        can_ok = [r for r in pool if r["m"] is None or r["m"] > 0]
        n = len(pool)
        # choose which traces give a flawed row: as close to half as possible
        n_flaw = min(len(can_flaw), n // 2)
        # traces that can only be flawed (mistake at step 0) must be flawed; traces without mistakes must be ok
        must_flaw = [r for r in pool if r["m"] == 0]
        flex = [r for r in pool if r["m"] is not None and r["m"] > 0]
        chosen_flaw = set(r["rid"] for r in must_flaw[:n_flaw])
        for r in flex:
            if len(chosen_flaw) >= n_flaw:
                break
            chosen_flaw.add(r["rid"])
        for r in pool:
            if r["rid"] in chosen_flaw:
                k, bad = r["m"], True
            elif r["m"] == 0:
                stats["skip_m0_surplus"] += 1
                continue
            else:
                hi = (r["m"] - 1) if r["m"] is not None else len(r["steps"]) - 1
                if r["m"] is None and rng.random() < 0.5:
                    k = hi  # the final-answer step of a mistake-free trace
                else:
                    # later steps are harder: sample from the second half of the allowed range
                    lo = hi // 2
                    k = rng.randint(lo, hi)
                bad = False
            if t == "multistep_arithmetic":
                ok_calc = arith_check(r["steps"], k)
                if ok_calc is not None and ok_calc == bad:  # exact evaluation disagrees with the human label
                    stats["drop_arith_label_conflict"] += 1
                    continue
            qid = "flaw" if rng.random() < 0.5 else "ok"
            gold = ("yes" if bad else "no") if qid == "flaw" else ("no" if bad else "yes")
            state = render(t, r["input"], r["steps"], k)
            rows.append({
                "key": KEY, "rid": f"{r['rid']}-t{k + 1}", "state": state, "instructions": Q[qid],
                "options": C.YN, "gold": gold, "soft": None,
                "meta": {"dataset": DATASET, "config": f"{t}.jsonl",
                         "revision": f"git:{COMMIT}; sha256:{SHAS[t + '.jsonl']}", "licence": LICENCE,
                         "split": "train",
                         "orig_label": {"mistake_index": r["m"], "judged_step_index": k, "task": t,
                                        "trace_answer": r["answer"], "target": r["target"],
                                        "annotation": "rule-based (authors' script) or human" if t == "dyck_languages"
                                        else "human (>=3 annotators, majority)"},
                         "family": C.FAMILY, "edge": EDGE[t] if len(state) <= 4000 else "long_context",
                         "defs": qid},
            })
    rows.sort(key=lambda r: r["rid"])
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, DEFS)
    st = C.summary(KEY, rows)
    print("stats:", dict(stats), "| decon:", len(hits))
    by = collections.defaultdict(collections.Counter)
    for r in rows:
        bad = (r["gold"] == "yes") == (r["meta"]["defs"] == "flaw")
        by[r["meta"]["orig_label"]["task"]]["flawed" if bad else "correct"] += 1
    print("per task:", {k: dict(v) for k, v in by.items()})
    C.show_samples(rows, n=5, seed=14)
    C.append_manifest(C.manifest_record(
        KEY, DATASET, LICENCE, rows, "yesno",
        "Step-level logical-mistake judging on PaLM 2 chain-of-thought traces for 5 BIG-Bench Hard tasks: the judged "
        "thought is the annotated FIRST mistake or a thought strictly before it (correct by the annotation); steps "
        "after the first mistake never judged. Human labels (>=3 annotators, alpha >= 0.98) for 4 tasks; Dyck "
        "languages mostly by the authors' rule-based stack checker (label by construction). One row per trace; two "
        "framings (mistake? / correct?).", st))


if __name__ == "__main__":
    main()
