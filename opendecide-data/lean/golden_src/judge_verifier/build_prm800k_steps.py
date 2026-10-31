"""Build raw rows for prm800k_steps: step-level correctness judging on PRM800K (Lightman et al., "Let's Verify Step
by Step", 2023).

Source : GitHub openai/prm800k pinned to commit 7ecc794703b2877f63226f2477a49b34f9b25163, the Git-LFS file
         prm800k/data/phase2_train.jsonl ONLY (sha256 = LFS oid). phase*_test.jsonl are never downloaded.
Licence: MIT (repo LICENSE at the pinned commit, "Copyright (c) 2023 OpenAI").
Texts  : MATH competition problems (human-written) and step-by-step solutions sampled from a GPT-4 base model; the
         solution steps are the object being judged (as in every judge/verifier set).
Labels : HUMAN step ratings by trained contract labelers following instructions_phase_2.pdf (pinned in the repo):
         +1 Great (correct, verifiable, appropriate, advances), 0 Okay (correct and reasonable but no progress),
         -1 Bad (states something wrong, hard to verify, gibberish/off-topic, derails into an obvious dead end, or a
         final answer that is wrong or does not follow from a complete solution). No model labels are used (the
         pre_generated_verifier_score field is ignored).
Rows   : "state" = the problem, the solution steps before the judged step (all of them rated >= 0 by the labeler, so the
         prefix is error-free by the labels) and the judged step. The judged step is one of
           neg      : the first step the labeler rated -1 (the first error of the trajectory);
           alt_pos  : an alternative next step at the SAME position as a first error, rated +1 (hard positive: same
                      problem and prefix as a flawed step);
           final_pos: a final-answer step rated +1 in a trajectory the labeler finished as a correct solution;
           pos      : an ordinary step rated +1 (later positions preferred);
           okay     : a step rated 0 (correct but stalling: NOT a flaw).
         Two framings (defs qids): 'flaw' ("Does the last step contain a mistake or other flaw that makes it a bad
         step?", yes = -1) and 'ok' ("Is the last step correct and acceptable?", yes = +1/0).
Filters: initial-screening questions (served to every labeler), give_up / bad_problem trajectories, flagged steps and
         unrated completions dropped; identical (problem, prefix, step) items rated by several labelers are merged:
         kept only if all labelers agree on bad vs not-bad (soft = real vote shares when >= 2 labelers); one row per
         source trajectory; at most 2 rows per problem (at most one flawed and one acceptable); states over 7,000
         characters dropped (no truncation); decontamination of problem and judged step against label-NLI, all local
         train/dev/eval files (this drops problems already used by the older judge_prm800k rows) and JevBench.
Deterministic (seed 20261201). CPU only.
"""
import collections
import json
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _jv_common as C  # noqa: E402

KEY = "prm800k_steps"
SEED = 20261201
COMMIT = "7ecc794703b2877f63226f2477a49b34f9b25163"
LFS = f"https://media.githubusercontent.com/media/openai/prm800k/{COMMIT}/prm800k/data/"
RAW = f"https://raw.githubusercontent.com/openai/prm800k/{COMMIT}/"
FILES = {
    "phase2_train.jsonl": (LFS + "phase2_train.jsonl",
                           "1110237feeb51d1bc200cb37b8f965cfdc1036eac7d506094049366fe7dc1089"),
    "LICENSE": (RAW + "LICENSE", "22d61a2226e035da51c56149c3358c36d1f61716435866bc6e6fe0e54c7270db"),
}
LICENCE = (f"MIT (https://github.com/openai/prm800k/blob/{COMMIT}/LICENSE, 'MIT License / Copyright (c) 2023 "
           "OpenAI')")
DATASET = "openai/prm800k (PRM800K phase 2 train labels)"
TARGET = 8000
MAX_STATE = 7000
MIX_POS = {"alt_pos": 0.30, "final_pos": 0.22, "pos": 0.36, "okay": 0.12}

Q = {
    "flaw": "Does the last step of this partial solution contain a mistake or other flaw that makes it a bad step?",
    "ok": "Is the last step of this partial solution correct and acceptable as a next step?",
}
DEFS = {
    "flaw": {
        "yes": "The last step is a bad step: it states something mathematically wrong (even if most of it is right), "
               "cannot be checked in about 30 seconds, is off-topic or gibberish, leads into an obvious dead end or "
               "loop, or gives a final answer that is wrong or not justified by a complete solution.",
        "no": "The last step has no such flaw: everything it states is correct, quickly verifiable and fits the "
              "earlier steps; this includes steps that only restate, stall or try a reasonable approach that may not "
              "pan out, and steps that catch an earlier slip.",
    },
    "ok": {
        "yes": "The last step is acceptable: everything it states is correct, quickly verifiable and fits the earlier "
               "steps, whether it makes real progress or only restates or stalls; a final answer counts only if it "
               "is correct and follows from a complete solution.",
        "no": "The last step is not acceptable: it states something wrong (even partly), cannot be checked in about "
              "30 seconds, is off-topic or gibberish, leads into an obvious dead end or loop, or gives a wrong, "
              "unjustified or incomplete final answer.",
    },
}


def add_items(items, rec_items, problem, prefix, cand, rid, i):
    for (t2, r2, k2) in cand:
        if not t2:
            continue
        key = (problem, tuple(prefix), t2)
        it = items.get(key)
        if it is None:
            it = items[key] = {"problem": problem, "prefix": list(prefix), "step": t2, "votes": [], "kinds": set(),
                               "recs": [], "pos": i + 1}
        it["votes"].append(r2)
        it["kinds"].add(k2)
        it["recs"].append(rid)
        rec_items[rid].append(key)


def final_answer(text):
    if "# Answer" not in text:
        return None
    return text.split("# Answer", 1)[1].strip()


def _norm_ans(a):
    a = str(a).strip().strip("$").strip()
    a = re.sub(r"\\boxed\{(.*)\}$", r"\1", a)
    for x in ("\\!", "\\,", "\\;", "\\left", "\\right", "^\\circ", "^{\\circ}", "\\%", "%", "$", " ", "\\displaystyle"):
        a = a.replace(x, "")
    a = a.replace("dfrac", "frac").replace("tfrac", "frac")
    a = re.sub(r"\\text\{\s*([^}]*)\}", r"\1", a)
    a = re.sub(r"\\mbox\{\s*([^}]*)\}", r"\1", a)
    a = a.rstrip(".")
    if re.fullmatch(r"-?\d{1,3}(,\d{3})+(\.\d+)?", a):
        a = a.replace(",", "")
    return a.lower()


def same_answer(a, b):
    na, nb = _norm_ans(a), _norm_ans(b)
    if na == nb:
        return True
    try:
        return abs(float(na) - float(nb)) < 1e-9
    except ValueError:
        return False


def step_text(step):
    c = step.get("chosen_completion")
    if c is None:
        return step.get("human_completion")
    return step["completions"][c]["text"]


def main():
    rng = random.Random(SEED)
    cache = C.CACHE / "prm800k"
    path = C.fetch(FILES["phase2_train.jsonl"][0], cache / "phase2_train.jsonl", FILES["phase2_train.jsonl"][1])
    C.fetch(FILES["LICENSE"][0], cache / "LICENSE", FILES["LICENSE"][1])
    stats = collections.Counter()

    # item key -> {"problem", "prefix", "step", "votes": [rating...], "kinds": set, "recs": [record ids]}
    items = {}
    rec_items = collections.defaultdict(list)  # record id -> [item keys]
    with open(path) as f:
        for ln, line in enumerate(f):
            o = json.loads(line)
            stats["records"] += 1
            if o["is_initial_screening_question"]:
                stats["drop_screening"] += 1
                continue
            fr = o["label"]["finish_reason"]
            if fr not in ("found_error", "solution"):
                stats[f"drop_{fr}"] += 1
                continue
            problem = C.clean(o["question"]["problem"])
            rid = f"p2-{ln}"
            steps = o["label"]["steps"]
            gt = o["question"].get("ground_truth_answer") or ""
            # a finished solution counts as verified-correct only if its final answer matches the MATH ground truth
            correct_solution = False
            if fr == "solution" and steps:
                last = steps[-1]
                lc = last.get("chosen_completion")
                if lc is not None and last["completions"][lc].get("rating") == 1:
                    ans = final_answer(last["completions"][lc]["text"])
                    correct_solution = ans is not None and same_answer(ans, gt)
                if not correct_solution:
                    stats["solution_answer_mismatch"] += 1
            prefix = []
            for i, s in enumerate(steps):
                comps = s["completions"]
                ch = s.get("chosen_completion")
                if ch is None:
                    # phase 2: the step where the labeler found the first error has no chosen completion; completion 0
                    # is the pre-generated step (rated -1), the others are alternatives rated after the error
                    if fr != "found_error" or i != len(steps) - 1 or s.get("human_completion") is not None:
                        break
                    orig = comps[0]
                    if orig.get("rating") != -1 or orig.get("flagged"):
                        stats["drop_errstep_unclear"] += 1
                        break
                    cand = [(C.clean(orig["text"]), -1, "neg")]
                    for c in comps[1:]:
                        if c.get("rating") is None or c.get("flagged"):
                            continue
                        ct = C.clean(c["text"])
                        cand.append((ct, c["rating"], {1: "alt_pos", 0: "alt_okay", -1: "alt_neg"}[c["rating"]]))
                    add_items(items, rec_items, problem, prefix, cand, rid, i)
                    stats["error_steps"] += 1
                    break
                chosen = comps[ch]
                r = chosen.get("rating")
                if r is None or chosen.get("flagged"):
                    break
                t = C.clean(chosen["text"])
                if r == -1:  # should not happen for a chosen step in phase 2; treat as the first error
                    add_items(items, rec_items, problem, prefix, [(t, -1, "neg")], rid, i)
                    break
                if r == 0:
                    kind = "okay"
                elif i == len(steps) - 1 and correct_solution and "# Answer" in t:
                    kind = "final_pos"
                elif correct_solution:
                    kind = "pos"
                else:
                    kind = "pos_unverified"  # +1 step in a trajectory that later fails: not used as a positive
                add_items(items, rec_items, problem, prefix, [(t, r, kind)], rid, i)
                prefix.append(t)
    stats["items"] = len(items)

    # merge votes: all labelers must agree on bad (-1) vs not bad (0/+1)
    cands = []
    for key, it in items.items():
        bad = sum(v == -1 for v in it["votes"])
        n = len(it["votes"])
        if 0 < bad < n:
            stats["drop_disagree"] += 1
            continue
        ks = it["kinds"]
        if bad == n:
            kind = "neg"
        elif all(v == 1 for v in it["votes"]) and "alt_pos" in ks:
            kind = "alt_pos"
        elif all(v == 1 for v in it["votes"]) and "final_pos" in ks:
            kind = "final_pos"
        elif all(v == 0 for v in it["votes"]) and ks & {"okay", "alt_okay"}:
            kind = "okay"
        elif ks & {"pos", "final_pos", "alt_pos"}:  # mix of 0 and +1 in a verified context: acceptable
            kind = "pos"
        else:  # only +1 steps from trajectories that later fail, or 0/+1 mixes without a verified context
            stats["drop_unverified_pos"] += 1
            continue
        it["kind"] = kind
        it["n"] = n
        it["state"] = render(it)
        if len(it["state"]) > MAX_STATE:
            stats["drop_long"] += 1
            continue
        it["iid"] = C._thash(it["state"])[:16]
        cands.append(it)
    stats["cands"] = len(cands)

    # decontaminate problem + judged step (cheap: few distinct problems)
    core = {}
    for it in cands:
        core[it["iid"]] = [it["problem"], it["step"]]
    hits = C.decon(core, cache_name=KEY)
    cands = [it for it in cands if it["iid"] not in hits]
    stats["after_decon"] = len(cands)

    # selection: one row per record, <= 1 neg and <= 1 acceptable per problem
    cands.sort(key=lambda it: it["iid"])
    rng.shuffle(cands)
    by_kind = collections.defaultdict(list)
    for it in cands:
        by_kind[it["kind"]].append(it)
    # prefer later positions for plain positives (more context, harder)
    by_kind["pos"].sort(key=lambda it: -min(it["pos"], 12) + rng.random() * 4)
    n_neg = TARGET // 2
    quotas = {k: int(round(v * (TARGET - n_neg))) for k, v in MIX_POS.items()}
    used_rec, used_prob_neg, used_prob_pos, used_state = set(), set(), set(), set()
    chosen = []

    def take(kind, quota, prob_set):
        got = 0
        for it in by_kind[kind]:
            if got >= quota:
                break
            if it["problem"] in prob_set or it["state"] in used_state:
                continue
            rec = next((r for r in it["recs"] if r not in used_rec), None)
            if rec is None:
                continue
            used_rec.add(rec)
            prob_set.add(it["problem"])
            used_state.add(it["state"])
            it["rec"] = rec
            chosen.append(it)
            got += 1
        return got

    # alternative positives first (they are the scarce, hard ones); then negatives, then the rest
    got = {"alt_pos": take("alt_pos", quotas["alt_pos"], used_prob_pos)}
    got["neg"] = take("neg", n_neg, used_prob_neg)
    for k in ("final_pos", "okay", "pos"):
        got[k] = take(k, quotas[k], used_prob_pos)
    short = (n_neg + sum(quotas.values())) - sum(got.values())
    if short > 0:  # top up acceptable side from plain positives
        got["pos"] += take("pos", short, used_prob_pos)
    stats.update({f"sel_{k}": v for k, v in got.items()})

    rows = []
    n_acc = sum(1 for it in chosen if it["kind"] != "neg")
    n_bad = len(chosen) - n_acc
    for it in sorted(chosen, key=lambda it: it["iid"]):
        qid = "flaw" if rng.random() < 0.5 else "ok"
        bad = it["kind"] == "neg"
        gold = ("yes" if bad else "no") if qid == "flaw" else ("no" if bad else "yes")
        soft = None
        if it["n"] >= 2:  # all agree by construction -> unanimous shares
            soft = {gold: 1.0, ("no" if gold == "yes" else "yes"): 0.0}
        rows.append({
            "key": KEY, "rid": f"{it['rec']}-s{it['pos']}-{it['iid'][:8]}", "state": it["state"],
            "instructions": Q[qid], "options": C.YN, "gold": gold, "soft": soft,
            "meta": {"dataset": DATASET, "config": "prm800k/data/phase2_train.jsonl (step labels)",
                     "revision": f"git:{COMMIT}; sha256:{FILES['phase2_train.jsonl'][1]}",
                     "licence": LICENCE, "split": "train",
                     "orig_label": {"step_ratings": it["votes"], "kind": it["kind"], "step_index": it["pos"]},
                     "family": C.FAMILY, "edge": edge_of(it), "defs": qid},
        })
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, {q: DEFS[q] for q in DEFS})
    st = C.summary(KEY, rows)
    print("stats:", dict(stats), "| decon hits:", len(hits), "| n_bad", n_bad, "n_acc", n_acc)
    print("kinds:", dict(collections.Counter(r["meta"]["orig_label"]["kind"] for r in rows)))
    C.show_samples(rows, n=5, seed=11)
    C.append_manifest(C.manifest_record(
        KEY, DATASET, LICENCE, rows, "yesno",
        "Step-level verification of GPT-4-sampled MATH solutions with HUMAN step ratings (+1/0/-1, phase-2 labeler "
        "instructions). Judged step = first error (-1), a +1 alternative at the same position as a first error (hard "
        "positive, same prefix), a +1 final answer of a finished correct solution, a +1 ordinary step, or a 0 "
        "'okay' step (correct but stalling = not a flaw). Two framings (flaw? / acceptable?); prefix steps all "
        "rated >= 0; multi-labeler items kept only when unanimous; one row per trajectory, <= 2 per problem; "
        "screening questions and give-up/bad-problem trajectories dropped; decon removes problems already in "
        "judge_prm800k.", st))


def render(it):
    lines = [f"Problem:\n{it['problem']}", ""]
    if it["prefix"]:
        lines.append("Solution steps so far:")
        for i, s in enumerate(it["prefix"], 1):
            lines.append(f"Step {i}: {s}")
    else:
        lines.append("Solution steps so far: (none)")
    lines.append("")
    lines.append(f"Last step (Step {len(it['prefix']) + 1}):\n{it['step']}")
    return "\n".join(lines)


def edge_of(it):
    if len(it["state"]) > 3500:
        return "long_context"
    if len(it["prefix"]) >= 6:
        return "multi_hop"
    return C.edge(it["step"], order=("double_negation", "negation", "quantifier", "units"), default=None)


if __name__ == "__main__":
    main()
