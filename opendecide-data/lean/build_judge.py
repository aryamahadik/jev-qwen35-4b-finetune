"""'Judge the response' rows (the family where v0.7 was too lenient: it said 'yes, fully correct' to flawed answers).
  prm800k    human step labels on math solutions (OpenAI PRM800K, MIT): 'no' if a chosen step was rated wrong
  helpsteer2 human correctness ratings of chat responses (NVIDIA HelpSteer2, CC BY 4.0): 4 -> yes, <=1 -> no
  ifcheck    procedural: a request with explicit constraints + a response; gold computed by a checker
  mathderiv  procedural: a derivation with or without one planted slip (term count, endpoint, arithmetic, method)
Some rows get a negated twin ("does it contain an error?") with a complement relation (A3 consistency loss).
Writes data/judge_train.jsonl + data/judge_train_relations.jsonl.
"""
import ast
import json
import random
import re
from collections import Counter
from pathlib import Path

from datasets import load_dataset

HERE = Path(__file__).resolve().parent
rng = random.Random(20260927)
rows, rels = [], []
POS_Q = ["Is the response fully correct and does it satisfy every explicit requirement of the request?",
         "Does the response answer the request correctly, with no substantive error in any step?",
         "Would a careful reviewer accept this response as completely correct and compliant with all stated constraints?",
         "Is every step and the final result of the response correct, and are all instructions in the request followed?"]
NEG_Q = ["Does the response contain at least one substantive error or miss an explicit requirement?",
         "Should a careful reviewer reject this response because something in it is wrong or a requirement is unmet?"]


def add(src, i, request, response, ok, twin_p=0.3):
    st = f"Request:\n{request.strip()}\n\nResponse:\n{response.strip()}"
    rid = f"r_judge_{src}_{i}"
    base = {"group_id": f"g:judge:{src}:{i}", "call_id": f"c_judge_{src}_{i}", "split": "train", "track": "JUDGE",
            "source": f"judge_{src}", "state": st, "qtype": "noul", "options": None, "meta": {"anchor": False}}
    rows.append({**base, "id": rid, "instructions": rng.choice(POS_Q), "gold": int(ok), "role": "aff"})
    if rng.random() < twin_p:
        rows.append({**base, "id": rid + "_neg", "instructions": rng.choice(NEG_Q), "gold": int(not ok), "role": "neg"})
        rels.append({"type": "complement", "a": rid, "b": rid + "_neg", "track": "train"})


# --- PRM800K -------------------------------------------------------------------------------------------------------
# phase 2: full model solutions; labelers stop at the first wrong step ("found_error") -> 'no' (including solutions
# whose final number is right but a step is wrong); "solution" with the right final answer -> 'yes'.
# phase 1: the labelers' chosen step-by-step path to a finished solution -> 'yes'.
from huggingface_hub import hf_hub_download
load = lambda f: [json.loads(l) for l in open(hf_hub_download("tasksource/PRM800K", f, repo_type="dataset"))]
p2, p1 = load("phase2_test.jsonl"), load("phase1_train.jsonl") + load("phase1_test.jsonl")
rng.shuffle(p2)
rng.shuffle(p1)
per_problem, got = Counter(), {0: 0, 1: 0}
for x in p2:
    q, fr = x["question"], x["label"]["finish_reason"]
    ok = fr == "solution" and q.get("pre_generated_answer") == q["ground_truth_answer"]
    if fr not in ("solution", "found_error") or (fr == "solution" and not ok) or per_problem[q["problem"]] >= 3:
        continue
    sol = "\n".join(q["pre_generated_steps"])
    if len(sol) > 3500 or got[int(ok)] >= 800:
        continue
    add("prm800k", sum(got.values()), q["problem"], sol, ok)
    got[int(ok)] += 1
    per_problem[q["problem"]] += 1
for x in p1:
    if got[1] >= 800:
        break
    lab = x["label"]
    if lab.get("finish_reason") != "solution" or x.get("is_quality_control_question") or x.get("is_initial_screening_question"):
        continue
    texts = []
    for s_ in lab["steps"]:
        c = s_["completions"][s_["chosen_completion"]] if s_.get("chosen_completion") is not None else s_.get("human_completion")
        if not c or c.get("rating") == -1:
            texts = []
            break
        texts.append(c["text"])
    if texts and len("\n".join(texts)) <= 3500 and per_problem[x["question"]["problem"]] < 3:
        add("prm800k", sum(got.values()), x["question"]["problem"], "\n".join(texts), True)
        got[1] += 1
        per_problem[x["question"]["problem"]] += 1

# --- HelpSteer2 ----------------------------------------------------------------------------------------------------
hs = load_dataset("nvidia/HelpSteer2", split="train")
cand = [x for x in hs if len(x["response"]) < 3000 and len(x["prompt"]) < 2500 and "<extra_id" not in x["prompt"]]
yes = [x for x in cand if int(x["correctness"]) == 4 and int(x["helpfulness"]) >= 3]
no = [x for x in cand if int(x["correctness"]) <= 1]
rng.shuffle(yes)
rng.shuffle(no)
for i, x in enumerate(yes[:450] + no[:450]):
    add("helpsteer2", i, x["prompt"], x["response"], int(x["correctness"]) == 4)

# --- procedural instruction-constraint checks ---------------------------------------------------------------------
TOPICS = ["why regular backups matter", "how to prepare for a job interview", "the benefits of cycling to work",
          "how a refund request is handled", "tips for writing a clear bug report", "why sleep affects focus",
          "how to plan a small team offsite", "what to check before signing a lease", "how to reduce cloud costs",
          "the basics of composting at home", "how to onboard a new colleague", "choosing a password manager"]
SENTS = ["Start by listing what you actually need.", "Keep a written record of every decision.", "Small steps add up quickly.",
         "Ask for feedback early and often.", "Check the details twice before you commit.", "Plan for the worst case.",
         "Budget a little more time than you expect.", "Automate the parts you repeat.", "Share the plan with everyone involved.",
         "Review the results after a week.", "Remove anything that is not essential.", "Write down the next action clearly."]


def ifcheck(i):
    topic = rng.choice(TOPICS)
    n = rng.choice([3, 4, 5])
    word = rng.choice(["checklist", "priority", "evidence", "schedule", "owner"])
    banned = rng.choice(["very", "just", "really", "simply"])
    ending = rng.choice(["Hope this helps.", "Good luck!", "That is all."])
    cons = rng.sample(["bullets", "include", "ban", "ending", "lower", "maxwords"], 3)
    maxw = rng.choice([45, 60, 80])
    req = f"Write a short answer about {topic}."
    txt = {"bullets": f" Use exactly {n} bullet points starting with '- '.", "include": f" Use the word '{word}' at least once.",
           "ban": f" Do not use the word '{banned}'.", "ending": f" End with the exact sentence '{ending}'",
           "lower": " Write everything in lowercase.", "maxwords": f" Use at most {maxw} words in total."}
    req += "".join(txt[c] for c in cons)
    lines = rng.sample(SENTS, n)
    if "include" in cons:
        lines[rng.randrange(n)] = lines[0].rstrip(".") + f" and keep a {word}."
    resp = [f"- {l}" for l in lines] if "bullets" in cons else [" ".join(lines)]
    if "ending" in cons:
        resp.append(ending)
    out = "\n".join(resp)
    if "lower" in cons:
        out = out.lower()
    ok = rng.random() < 0.5
    if not ok:  # break exactly one constraint, subtly
        c = rng.choice(cons)
        if c == "bullets":
            out = out.replace("- ", "", 1) if rng.random() < 0.5 else out + f"\n- {rng.choice(SENTS)}"
        elif c == "include":
            out = re.sub(rf"\b{word}\b", "list", out)
        elif c == "ban":
            out = out.replace(". ", f". It is {banned} useful. ", 1) if ". " in out else out.replace("\n", f" It is {banned} useful.\n", 1)
        elif c == "ending":
            out = out.replace(ending if "lower" not in cons else ending.lower(), ending.rstrip(".!") + " for now.")
        elif c == "lower":
            out = out[0].upper() + out[1:] if out[0] != "-" else out.replace("- ", "- ", 1).replace(out[2], out[2].upper(), 1)
        elif c == "maxwords":
            out = out + " " + " ".join(rng.sample(SENTS, 6))
    # the checker decides the gold (never trusts the construction)
    words = len(re.findall(r"\S+", out))
    checks = {"bullets": sum(1 for l in out.splitlines() if l.startswith("- ")) == n and all(l.startswith("- ") for l in out.splitlines()
                                                                                              if l and not l.lower().startswith(ending.lower()[:5])),
              "include": re.search(rf"\b{word}\b", out, re.I) is not None, "ban": re.search(rf"\b{banned}\b", out, re.I) is None,
              "ending": out.strip().endswith(ending if "lower" not in cons else ending.lower()),
              "lower": out == out.lower(), "maxwords": words <= maxw}
    add("ifcheck", i, req, out, all(checks[c] for c in cons))


for i in range(900):
    ifcheck(i)


# --- procedural math derivations with or without one slip -----------------------------------------------------------
def mathderiv(i):
    kind = rng.choice(["series", "percent", "days"])
    ok = rng.random() < 0.5
    if kind == "series":
        a, b = sorted(rng.sample(range(5, 400), 2))
        n = b - a + 1
        s = n * (a + b) // 2
        n2, s2 = n, s
        slip = None if ok else rng.choice(["count", "arith", "method"])
        if slip == "count":
            n2 = b - a
            s2 = n2 * (a + b) // 2
        if slip == "arith":
            s2 = s + rng.choice([-10, 10, -1, 1, 100])
        verify = (f"Check: sum(1..{b}) - sum(1..{a - 1}) = {b * (b + 1) // 2} - {(a - 1) * a // 2} = {s2}." if slip != "method"
                  else f"Check: ({a} + {b}) / 2 x {n2} = {s2}, the same result.")
        req = (f"Find the sum of all integers from {a} through {b} inclusive. Show the number of terms and an arithmetic-series "
               f"calculation, then verify with a different method.")
        resp = f"Number of terms: {n2}. Average term: ({a} + {b}) / 2 = {(a + b) / 2:g}. Sum = {(a + b) / 2:g} x {n2} = {s2}.\n{verify}"
        good = slip is None or (slip == "arith" and s2 == s)
        if slip == "arith":  # the check line must still show the (correct) difference so the slip is visible
            resp = f"Number of terms: {n}. Average term: ({a} + {b}) / 2 = {(a + b) / 2:g}. Sum = {(a + b) / 2:g} x {n} = {s2}.\n" \
                   f"Check: sum(1..{b}) - sum(1..{a - 1}) = {b * (b + 1) // 2} - {(a - 1) * a // 2} = {s2}."
            good = False
        add("mathderiv", i, req, resp, good)
    elif kind == "percent":
        old, new = rng.randint(40, 900), rng.randint(40, 900)
        pct = round((new - old) / old * 100, 1)
        slip = None if ok else rng.choice(["base", "arith"])
        p2 = round((new - old) / new * 100, 1) if slip == "base" else (round(pct + rng.choice([-2, 2, -0.5, 0.5]), 1) if slip else pct)
        req = f"A price changed from ${old} to ${new}. Give the percentage change relative to the original price, to one decimal place."
        resp = f"Change = {new} - {old} = {new - old}. Percentage change = {new - old} / {new if slip == 'base' else old} x 100 = {p2}%."
        add("mathderiv", i, req, resp, p2 == pct)
    else:
        import datetime as dt
        d1 = dt.date(2025, 1, 1) + dt.timedelta(days=rng.randint(0, 300))
        k = rng.randint(3, 90)
        d2 = d1 + dt.timedelta(days=k)
        inclusive = rng.random() < 0.5
        truth = k + 1 if inclusive else k
        ans = truth if ok else truth + rng.choice([-1, 1])
        req = (f"How many days are there from {d1:%B %d, %Y} to {d2:%B %d, %Y}, " +
               ("counting both the first and the last day?" if inclusive else "not counting the first day?"))
        resp = f"From {d1:%b %d} to {d2:%b %d} is {k} days apart" + (f", and counting both ends gives {ans} days." if inclusive
                                                                     else f", so the answer is {ans} days.")
        add("mathderiv", i, req, resp, ans == truth)


for i in range(900):
    mathderiv(i)

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids))
(HERE / "data/judge_train.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
(HERE / "data/judge_train_relations.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rels))
print(len(rows), "rows", len(rels), "relations", Counter((r["source"], r["gold"]) for r in rows if r["role"] == "aff"))
