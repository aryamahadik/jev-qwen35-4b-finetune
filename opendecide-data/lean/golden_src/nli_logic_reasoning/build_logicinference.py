"""Build golden v14 rows for "logicinference" (LogicInference; Ontañón et al., ICLR 2022 OSC workshop).

Source : the official generator code, google-research/google-research @ 5b09c22d73a9d35eb6c5d2a99b95677a45053466,
         folder logic_inference_dataset/ (rules.py, inference_problems.py, inference_methods.py,
         example_generation.py, logic_inference_lib.py, splits.py; sha256 of each file recorded in meta). The code is
         run here, CPU only, with a fixed seed (the released dataset is only distributed as this generator).
Licence: Apache-2.0 (header of every generator file and the google-research repository LICENSE).
Texts  : program-generated propositional and first-order inference problems rendered in English by the authors'
         templates; the label follows by construction from the generator's inference chains (no model).
Task   : type-3b problems ("Consider the following premises ... Can we infer the following?") in natural language.
         The generator marks each target as an inference (derivable, or itself a premise), a contradiction (its
         negation is derivable) or unrelated (neither). Two question types, each source example used once:
           * infer : yes/no "can the statement be inferred?"   yes = inference ; no = contradiction or unrelated
           * tfu   : 3-way true / false / undetermined          (inference / contradiction / unrelated)
Filters: problems whose premises are contradictory (ex falso examples, type 3b-cont) are dropped; problems where two
         distinct propositions render to the same English, or where the English would let world knowledge decide a
         formally open or independent proposition (happy/sad, rich/poor, bored/excited, sunny/cloudy/overcast/
         raining/snowing/cold for the same subject), are dropped; 'is itself a premise' targets capped at 5% of the
         inferable rows; single-variable names such as 'x_12' / 'z_3' are shown as 'x' / 'z' (each sentence binds its own variable).
         Problems whose English premise list repeats a sentence are dropped.
Verify : (added by the strict review) every label is re-derived by an INDEPENDENT semantic check of the generator's
         structured formulas: quantifiers are grounded over a finite domain (all constants + one fresh element per
         quantifier occurrence, enough for this single-variable monadic fragment) and sympy's SAT solver decides
         premises |= statement (inference), premises |= not statement (contradiction) or neither (unrelated). Rows
         where the check disagrees with the generator are dropped: the generator's 'unrelated' targets are the base
         rule's spare propositions and about 18% of them are in fact derivable after chaining (e.g. 'S iff P; S or D;
         not P' with target 'D'), and ~0.4% of problems have jointly inconsistent premises the generator missed.
Seed 20261133; dedupe of normalised states.
"""
import importlib
import json
import os
import random
import re
import sys
from collections import Counter
from pathlib import Path

from sympy import Symbol
from sympy.logic.boolalg import And, Equivalent, Implies, Not, Or
from sympy.logic.inference import satisfiable

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as C  # noqa: E402

KEY = "logicinference"
SEED = 20261133
COMMIT = "5b09c22d73a9d35eb6c5d2a99b95677a45053466"
BASE = f"https://raw.githubusercontent.com/google-research/google-research/{COMMIT}/logic_inference_dataset/"
FILES = ["rules.py", "inference_problems.py", "inference_methods.py", "example_generation.py",
         "logic_inference_lib.py", "splits.py"]
LICENCE = ("Apache-2.0 (licence header in every generator file of google-research/google-research/"
           "logic_inference_dataset @ 5b09c22d; repository LICENSE)")
CODE_DIR = C.CACHE_ROOT / "logicinference_code"
N_PROBLEMS = 15000  # raised from 9,000: the semantic check removes ~18% of 'unrelated' targets
N_VARIATIONS = 3
LENGTH_DIST = [0.3, 0.3, 0.25, 0.1, 0.05]
QUOTA = {
    "infer": {"inference": 1500, "contradiction": 750, "unrelated": 750},
    "tfu": {"inference": 1000, "contradiction": 1000, "unrelated": 800},
}
MAX_PREMISE_TARGET_SHARE = 0.05

Q_INFER = ("Treating each sentence as a plain logical proposition (no outside knowledge), can the statement be "
           "logically inferred from the premises?")
Q_TFU = ("Treating each sentence as a plain logical proposition (no outside knowledge), is the statement true, "
         "false, or undetermined given the premises?")
DEFS = {
    "infer": {
        "yes": "The statement follows with certainty from the premises by valid steps (modus ponens, modus tollens, "
               "disjunctive syllogism, instantiating 'for all', chaining conditionals, and so on), or is itself a "
               "premise.",
        "no": "The statement does not follow: the premises either imply its negation or leave it open (for "
              "example affirming the consequent, or a proposition the premises never constrain).",
    },
    "tfu": {
        "true": "The premises logically imply the statement, so it must be true whenever all the premises are true.",
        "false": "The premises logically imply the negation of the statement, so it must be false whenever all the "
                 "premises are true.",
        "undetermined": "The premises imply neither the statement nor its negation, so it could be true or false "
                        "(for example affirming the consequent, or a claim the premises never constrain).",
    },
}
GOLD = {
    "infer": {"inference": "yes", "contradiction": "no", "unrelated": "no"},
    "tfu": {"inference": "true", "contradiction": "false", "unrelated": "undetermined"},
}
# groups of English predicates whose everyday meaning would decide each other for the same subject
CLASH = [{"happy", "sad"}, {"rich", "poor"}, {"bored", "excited"},
         {"sunny", "cloudy", "overcast", "raining", "snowing", "cold"}]
INPUT_RE = re.compile(r"^Consider the following premises\. (.*)\. Can we infer the following from them\? "
                      r"(?:If we can, name the inference rule being used: )?(.*)\.$", re.S)
VAR_RE = re.compile(r"\b([a-z])_\d+\b")


def load_generator():
    CODE_DIR.mkdir(parents=True, exist_ok=True)
    shas = {}
    for f in FILES:
        p = C.fetch(BASE + f, CODE_DIR / f)
        shas[f] = C.sha256_file(p)
    sys.path.insert(0, str(CODE_DIR))
    mods = {m: importlib.import_module(m) for m in
            ["logic_inference_lib", "inference_methods", "rules", "inference_problems", "example_generation"]}
    return mods, shas


def nl_props_for(problem, rules):
    bindings = {}
    out = []
    for prop in problem.propositions:
        if isinstance(prop, str):
            out.append(rules.generate_nl_proposition(prop, [], bindings))
        else:
            out.append(rules.generate_nl_proposition(prop[0], prop[1:], bindings))
    return out


def clash(nl_props):
    """True if two propositions share a CLASH group for the same subject (or both are weather words)."""
    seen = {}
    for p in nl_props:
        s = p[0]  # assertive form, e.g. "Linda is happy", "it is sunny", "x_3 is rich"
        m = re.match(r"^(it|[A-Za-z_0-9]+) is (?:an? )?([a-z ]+)$", s)
        if not m:
            continue
        subj, pred = m.group(1), m.group(2).strip()
        for gi, g in enumerate(CLASH):
            if pred in g:
                key = ("weather", gi) if gi == 3 else (subj if not subj.startswith("x") else "x", gi)
                if key in seen and seen[key] != pred:
                    return True
                seen[key] = pred
    return False


def unify_var(sentence):
    """'For all z_3, z_3 ...' -> 'For all z, z ...' when the sentence binds exactly one variable."""
    vs = {m.group(0) for m in VAR_RE.finditer(sentence)}
    if len(vs) == 1:
        return VAR_RE.sub(lambda m: m.group(1), sentence)
    return sentence


def _is_var(t):
    return isinstance(t, str) and t.startswith("var ")


def _consts(f, acc):
    """Constants (individual names such as 'a_8') occurring in a structured formula."""
    if isinstance(f, list):
        if len(f) == 2 and all(isinstance(x, str) for x in f) and f[0] not in ("~", "forall", "exists"):
            if not _is_var(f[1]):
                acc.add(f[1])
            return acc
        for x in f:
            if isinstance(x, list):
                _consts(x, acc)
    return acc


def _n_quant(f):
    if not isinstance(f, list):
        return 0
    return (1 if f and f[0] in ("forall", "exists") else 0) + sum(_n_quant(x) for x in f if isinstance(x, list))


def _sym(f, env, dom):
    """Ground a structured formula over the finite domain `dom` into a sympy boolean expression."""
    if isinstance(f, str):
        return Symbol("A:" + f)
    op = f[0]
    if op == "~":
        return Not(_sym(f[1], env, dom))
    if op in ("and", "or", "->", "<->"):
        a, b = _sym(f[1], env, dom), _sym(f[2], env, dom)
        return {"and": And, "or": Or, "->": Implies, "<->": Equivalent}[op](a, b)
    if op in ("forall", "exists"):
        parts = [_sym(f[2], dict(env, **{f[1]: d}), dom) for d in dom]
        return And(*parts) if op == "forall" else Or(*parts)
    if len(f) == 1:
        return Symbol("A:" + op)
    assert len(f) == 2, f
    arg = env[f[1]] if _is_var(f[1]) else f[1]
    return Symbol(f"P:{op}({arg})")


def semantic_status(premises, target):
    """Independent check: 'inference' / 'contradiction' / 'unrelated', or 'inconsistent' premises."""
    cs = set()
    for p in list(premises) + [target]:
        _consts(p, cs)
    k = sum(_n_quant(p) for p in premises) + _n_quant(target)
    dom = sorted(cs) + [f"_w{i}" for i in range(max(1, k))]
    g = And(*[_sym(p, {}, dom) for p in premises])
    t = _sym(target, {}, dom)
    if not satisfiable(g):
        return "inconsistent"
    if not satisfiable(And(g, Not(t))):
        return "inference"
    if not satisfiable(And(g, t)):
        return "contradiction"
    return "unrelated"


def chain_len(targets, etype):
    if etype.endswith("premise"):
        return 0
    n = targets.count("rom the fact that")
    return max(n, 1)


def main():
    if os.environ.get("PYTHONHASHSEED") != "0":  # make any set/hash ordering inside the generator reproducible
        os.execve(sys.executable, [sys.executable] + sys.argv, dict(os.environ, PYTHONHASHSEED="0"))
    mods, shas = load_generator()
    lib, rules, ip, eg = (mods["logic_inference_lib"], mods["rules"], mods["inference_problems"],
                          mods["example_generation"])
    random.seed(SEED)
    rules.precompute_rules()
    problems = ip.generate_multistep_problems(N_PROBLEMS, length_distribution=LENGTH_DIST)
    print(f"problems generated: {len(problems)}")

    cands, drop = [], Counter()
    seen = set()
    for pi, prob in enumerate(problems):
        if prob.contains_contradiction:
            drop["contradictory premises"] += 1
            continue
        for vi, var in enumerate(ip.generate_problem_renaming_variations(prob, N_VARIATIONS)):
            prem = list(var.premises)
            random.shuffle(prem)
            v2 = lib.InferenceProblem(prem, var.inferences, var.contradictions, var.unrelated, var.propositions,
                                      var.contains_contradiction)
            nl = nl_props_for(v2, rules)
            assertive = [p[0] for p in nl]
            if len(set(assertive)) != len(assertive):
                drop["duplicate English proposition"] += 1
                continue
            if clash(nl):
                drop["world-knowledge clash"] += 1
                continue
            ex = eg.generate_example_type_3b(v2, nl, answer_at_the_end=False)
            if ex is None:
                continue
            et = ex.example_type
            if et.endswith("cont"):
                drop["3b-cont"] += 1
                continue
            kind = ("inference" if et in ("3b", "3b-premise") else
                    "contradiction" if et in ("3b-no", "3b-no-1") else
                    "unrelated" if et == "3b-unrelated" else None)
            assert kind, et
            m = INPUT_RE.match(ex.inputs)
            assert m, ex.inputs
            premises = [unify_var(s.strip()) for s in m.group(1).split(". ")]
            target = unify_var(m.group(2).strip())
            if len({C.norm(p) for p in premises}) != len(premises):
                drop["repeated premise sentence"] += 1
                continue
            # independent semantic re-check of the label (structured target recovered from its rendering)
            tgt_txt = m.group(2).strip()
            structs = ([x[0] for x in v2.inferences] + [x[0] for x in v2.contradictions] + list(v2.unrelated) +
                       list(v2.premises))
            match = [f for f in structs if rules.capitalize(rules.render_language_clause(
                f, v2.propositions, nl)) == tgt_txt]
            sts = {semantic_status(list(v2.premises), f) for f in match}
            if len(sts) != 1:
                drop["semantic check: target not recovered"] += 1
                continue
            sem = sts.pop()
            if sem != kind:
                drop[f"semantic check: generator says {kind}, premises give {sem}"] += 1
                continue
            state = "Premises:\n" + "\n".join(f"{i + 1}. {p}." for i, p in enumerate(premises)) + \
                    f"\n\nStatement: {target}."
            k = C.norm(state)
            if k in seen:
                continue
            seen.add(k)
            cands.append({"pi": pi, "vi": vi, "kind": kind, "etype": et, "state": state, "target": target,
                          "premises": premises, "chain": chain_len(ex.targets, et), "targets": ex.targets})
    print("dropped:", dict(drop))
    print("candidates by type:", dict(Counter(c["etype"] for c in cands)))

    rng = random.Random(SEED)
    rng.shuffle(cands)
    # one example per (problem, variation) and at most 2 per problem, across both question types
    per_prob, used_pv = Counter(), set()
    pools = {k: [c for c in cands if c["kind"] == k] for k in ("inference", "contradiction", "unrelated")}
    ptr = Counter()
    got = Counter()
    premise_targets = 0
    picked = []
    need = [(q, k) for q in QUOTA for k in QUOTA[q]]
    active = list(need)
    while active:
        for qk in list(active):
            q, k = qk
            placed = False
            while ptr[k] < len(pools[k]):
                c = pools[k][ptr[k]]
                ptr[k] += 1
                if (c["pi"], c["vi"]) in used_pv or per_prob[c["pi"]] >= 2:
                    continue
                if c["etype"] == "3b-premise":
                    lim = MAX_PREMISE_TARGET_SHARE * (QUOTA["infer"]["inference"] + QUOTA["tfu"]["inference"])
                    if premise_targets >= lim:
                        continue
                    premise_targets += 1
                used_pv.add((c["pi"], c["vi"]))
                per_prob[c["pi"]] += 1
                picked.append((q, c))
                got[qk] += 1
                placed = True
                break
            if not placed or got[qk] >= QUOTA[q][k]:
                active.remove(qk)
    print("picked:", dict(got))

    def edge(c):
        if c["kind"] == "unrelated":
            return "missing_info"
        if re.search(r"\bnot\b|n't\b", c["target"]):
            return "negation"
        if c["chain"] >= 2:
            return "multi_hop"
        if any(re.match(r"(For all|There is at least one)", p) for p in c["premises"] + [c["target"]]):
            return "quantifier"
        return None

    out = []
    for q, c in picked:
        out.append({
            "key": KEY,
            "rid": f"logicinference_s{SEED}_p{c['pi']}_v{c['vi']}",
            "state": c["state"],
            "instructions": Q_INFER if q == "infer" else Q_TFU,
            "options": ["yes", "no"] if q == "infer" else ["true", "false", "undetermined"],
            "gold": GOLD[q][c["kind"]],
            "soft": None,
            "meta": {"dataset": "github.com/google-research/google-research/tree/master/logic_inference_dataset",
                     "config": "type 3b (natural language), generated", "revision": COMMIT, "licence": LICENCE,
                     "split": "train", "orig_label": c["etype"], "family": C.FAMILY, "edge": edge(c), "defs": q,
                     "chain_len": c["chain"], "generator_seed": SEED, "code_sha256": shas},
        })
    rng.shuffle(out)
    C.validate_rows(KEY, out, DEFS)
    C.write_rows(KEY, out)
    for q, d in DEFS.items():
        C.write_defs(KEY, d, qid=q)
    share = C.report(KEY, out)
    print("chain lengths:", dict(Counter(r["meta"]["chain_len"] for r in out)))
    e = Counter(r["meta"]["edge"] for r in out)
    C.append_manifest({
        "key": KEY, "family": C.FAMILY, "dataset": "LogicInference generator (google-research), type 3b",
        "licence": LICENCE, "rows": len(out),
        "qtype": "mixed: yes/no 'can it be inferred?' (infer) + 3-way true/false/undetermined (tfu)",
        "yesno_share": round(share, 4) if share is not None else None, "edge_tags": sorted(k for k in e if k),
        "notes": "Exact-label propositional + monadic first-order deduction in English (modus tollens, disjunctive "
                 "syllogism, biconditionals, universal/existential instantiation, fallacies such as affirming the "
                 "consequent -> undetermined). Contradictory-premise problems and world-knowledge clashes removed; every "
                 "label re-verified by an independent SAT check (generator-mislabelled unrelated targets dropped).",
    })
    if "--show" in sys.argv:
        C.show_samples(out, 6)


if __name__ == "__main__":
    main()
