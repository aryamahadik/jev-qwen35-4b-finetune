"""Generator gen_nlr_heuristics (family nli_logic_reasoning): premise/hypothesis entailment pairs that break the
shallow NLI heuristics (lexical overlap, subsequence, constituent - McCoy et al. 2019 style) and add negation,
double negation, factive / implicative verbs, exceptives, "only", "still / no longer", monotonicity and numeric
quantifier boundaries.

Everything is Claude-written: the vocabulary, the templates and this program. No dataset is read and no model is
called. Labels follow by construction from the template (entailed = the hypothesis must be true whenever the premise
is true). Every template emits a FACT-FLIP TWIN: a second row that changes one decisive element (a word, the
argument order or the hypothesis) so that the gold label flips; the twin carries meta.twin_of = rid of its partner.
Symmetric verbs (met, married, ...) are excluded; perception verbs are excluded where attachment could leak.

Output: data/v14_parts/raw/gen_nlr_heuristics.jsonl + defs/gen_nlr_heuristics.json; MANIFEST record.
Deterministic (seed 20261135), CPU only.
"""
import random
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "nli_logic_reasoning"))
import _common as C  # noqa: E402

KEY = "gen_nlr_heuristics"
SEED = 20261135
PAIRS_PER_TEMPLATE = 70
LICENCE = "CC0 1.0 (Claude-written templates and program; no source data)"
INSTRUCTIONS = "Does the premise entail the hypothesis, that is, must the hypothesis be true whenever the premise is true?"
DEFS = {
    "yes": "Whenever the premise is true the hypothesis must also be true, judged by who did what to whom, factive or "
           "implicative verbs, negation, exceptions and quantifier meaning rather than by shared words.",
    "no": "The premise can be true while the hypothesis is false: roles are reversed, the event is only believed, "
          "conditional, possible, attempted or negated, or the quantity or exception is not guaranteed.",
}

NOUNS = [("doctor", "doctors"), ("lawyer", "lawyers"), ("senator", "senators"), ("teacher", "teachers"),
         ("manager", "managers"), ("artist", "artists"), ("banker", "bankers"), ("pilot", "pilots"),
         ("chef", "chefs"), ("author", "authors"), ("judge", "judges"), ("nurse", "nurses"),
         ("tourist", "tourists"), ("student", "students"), ("secretary", "secretaries"), ("athlete", "athletes"),
         ("scientist", "scientists"), ("actor", "actors"), ("professor", "professors"), ("farmer", "farmers"),
         ("architect", "architects"), ("plumber", "plumbers"), ("editor", "editors"), ("coach", "coaches"),
         ("dentist", "dentists"), ("cashier", "cashiers"), ("mechanic", "mechanics"), ("reporter", "reporters"),
         ("soldier", "soldiers"), ("tenant", "tenants"), ("landlord", "landlords"), ("customer", "customers"),
         ("engineer", "engineers"), ("detective", "detectives"), ("librarian", "librarians"),
         ("accountant", "accountants"), ("pharmacist", "pharmacists"), ("gardener", "gardeners")]
# transitive, non-symmetric, agentive: (past, past participle, base, perception?)
VT = [("helped", "helped", "help", 0), ("called", "called", "call", 0), ("thanked", "thanked", "thank", 0),
      ("recommended", "recommended", "recommend", 0), ("advised", "advised", "advise", 0),
      ("admired", "admired", "admire", 0), ("avoided", "avoided", "avoid", 0), ("paid", "paid", "pay", 0),
      ("contacted", "contacted", "contact", 0), ("supported", "supported", "support", 0),
      ("visited", "visited", "visit", 0), ("encouraged", "encouraged", "encourage", 0),
      ("praised", "praised", "praise", 0), ("blamed", "blamed", "blame", 0),
      ("questioned", "questioned", "question", 0), ("invited", "invited", "invite", 0),
      ("warned", "warned", "warn", 0), ("interviewed", "interviewed", "interview", 0),
      ("hired", "hired", "hire", 0), ("saw", "seen", "see", 1), ("heard", "heard", "hear", 1),
      ("noticed", "noticed", "notice", 1), ("criticized", "criticized", "criticize", 0),
      ("consulted", "consulted", "consult", 0), ("thanked", "thanked", "thank", 0)]
VT = list({v[0]: v for v in VT}.values())
# intransitive: (past, base, compatible manner adverbs)
VI = [("slept", "sleep", ["quietly", "calmly", "briefly"]), ("danced", "dance", ["quickly", "happily", "slowly"]),
      ("laughed", "laugh", ["loudly", "nervously", "quietly", "briefly"]),
      ("waited", "wait", ["quietly", "calmly", "nervously", "patiently"]), ("left", "leave", ["quickly", "quietly", "early"]),
      ("resigned", "resign", ["quietly", "suddenly"]), ("arrived", "arrive", ["late", "early", "quickly"]),
      ("shouted", "shout", ["loudly", "angrily"]), ("smiled", "smile", ["happily", "nervously", "briefly"]),
      ("apologized", "apologize", ["quickly", "briefly", "nervously"]), ("retired", "retire", ["quietly", "early"]),
      ("complained", "complain", ["loudly", "briefly", "angrily"]), ("hesitated", "hesitate", ["briefly", "nervously"]),
      ("stumbled", "stumble", ["slightly", "twice"]), ("cried", "cry", ["quietly", "loudly"]),
      ("relaxed", "relax", ["briefly", "completely"]), ("volunteered", "volunteer", ["quickly", "happily"]),
      ("objected", "object", ["loudly", "calmly", "angrily"])]
# subsective adjectives only (an ADJ noun is always a noun); 'retired' was removed in review: a retired judge may no
# longer count as a judge, which would break the monotonicity labels of adj_drop / any_down / every_restrictor
ADJ = ["tall", "young", "famous", "nervous", "old", "quiet", "experienced", "tired", "local", "foreign",
       "new", "senior", "junior", "cheerful", "anxious"]
PREP = ["near", "behind", "next to", "beside", "in front of"]
FACTIVE = ["knew", "realized", "noticed", "discovered", "learned", "remembered", "regretted", "found out"]
NONFACT = ["believed", "thought", "hoped", "claimed", "suspected", "assumed", "said", "feared", "imagined",
           "guessed", "insisted", "doubted"]
ADV_VER = ["Clearly", "Obviously", "Certainly", "Undoubtedly", "Of course", "Fortunately", "Sadly",
           "Unsurprisingly", "Luckily"]
ADV_NONVER = ["Perhaps", "Probably", "Supposedly", "Maybe", "Allegedly", "Hopefully", "Possibly",
              "Presumably", "Conceivably"]
IMPL_YES = ["managed to", "remembered to", "made sure to", "did not fail to", "took the time to"]
IMPL_NO = ["wanted to", "hoped to", "planned to", "tried to", "promised to", "decided to", "intended to",
           "expected to", "failed to", "forgot to", "refused to", "declined to", "was about to", "offered to"]
SUB_VER = ["Because", "Although", "After", "Since"]
SUB_NONVER = ["If", "Unless", "Even if", "Provided that"]
NAMES = ["Maria", "Omar", "Chen", "Priya", "Lucas", "Fatima", "Tom", "Aisha", "Ivan", "Elena", "Kwame", "Sofia",
         "Diego", "Hana", "Yusuf", "Mei", "Rahul", "Nora", "Pablo", "Zainab", "Grace", "Tariq", "Ingrid", "Kofi",
         "Leila", "Mateo", "Anya", "Samir", "Julia", "Kenji"]
GROUPS = ["passengers", "guests", "students", "players", "employees", "volunteers", "tenants", "runners", "members",
          "delegates", "nurses", "interns", "musicians", "applicants", "residents", "jurors"]
# (3rd person present VP, base VP) for still / no longer
STATES = [("works at the bank", "work at the bank"), ("lives in Lisbon", "live in Lisbon"),
          ("coaches the team", "coach the team"), ("owns the bakery", "own the bakery"),
          ("rents the flat on Hill Street", "rent the flat on Hill Street"), ("chairs the committee", "chair the committee"),
          ("teaches chemistry", "teach chemistry"), ("plays in the orchestra", "play in the orchestra"),
          ("volunteers at the shelter", "volunteer at the shelter"), ("drives a taxi", "drive a taxi"),
          ("manages the pharmacy", "manage the pharmacy"), ("writes for the local paper", "write for the local paper"),
          ("serves on the school board", "serve on the school board"), ("runs the night shift", "run the night shift")]
NUMW = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
        11: "eleven", 12: "twelve"}


def a(adj):
    return ("an " if adj[0] in "aeiou" else "a ") + adj


def cap(s):
    return s[0].upper() + s[1:]


class Slots:
    def __init__(self, rng):
        self.rng = rng

    def nouns(self, k):
        return self.rng.sample(NOUNS, k)

    def vt(self, perception_ok=True):
        pool = [v for v in VT if perception_ok or not v[3]]
        return self.rng.choice(pool)

    def vi(self, k=1):
        return self.rng.sample(VI, k) if k > 1 else self.rng.choice(VI)

    def pick(self, xs, k=1):
        return self.rng.sample(xs, k) if k > 1 else self.rng.choice(xs)


# Each template returns (tag or (tag_row0, tag_row1), [(premise, hypothesis, gold), (premise, hypothesis, gold)]);
# the two rows are fact-flip twins.
def t_swap(s):
    (n1, _), (n2, _) = s.nouns(2)
    v = s.vt()
    p = f"The {n1} {v[0]} the {n2}."
    return None, [(p, f"The {n2} {v[0]} the {n1}.", "no"), (p, f"The {n2} was {v[1]} by the {n1}.", "yes")]


def t_passive(s):
    (n1, _), (n2, _) = s.nouns(2)
    v = s.vt()
    p = f"The {n1} was {v[1]} by the {n2}."
    return None, [(p, f"The {n1} {v[0]} the {n2}.", "no"), (p, f"The {n2} {v[0]} the {n1}.", "yes")]


def t_relobj(s):
    (n1, _), (n2, _) = s.nouns(2)
    v, vi = s.vt(), s.vi()
    rel = s.pick(["who", "that"])
    p = f"The {n1} {rel} the {n2} {v[0]} {vi[0]}."
    return None, [(p, f"The {n1} {v[0]} the {n2}.", "no"), (p, f"The {n2} {v[0]} the {n1}.", "yes")]


def t_relsubj(s):
    (n1, _), (n2, _) = s.nouns(2)
    v, vi = s.vt(), s.vi()
    rel = s.pick(["who", "that"])
    p = f"The {n1} {rel} {v[0]} the {n2} {vi[0]}."
    return None, [(p, f"The {n2} {v[0]} the {n1}.", "no"), (p, f"The {n1} {v[0]} the {n2}.", "yes")]


def t_conj_obj(s):
    (n1, _), (n2, _), (n3, _) = s.nouns(3)
    v = s.vt()
    p = f"The {n1} {v[0]} the {n2} and the {n3}."
    return None, [(p, f"The {n2} {v[0]} the {n3}.", "no"), (p, f"The {n1} {v[0]} the {n3}.", "yes")]


def t_pp_obj(s):
    (n1, _), (n2, _), (n3, _) = s.nouns(3)
    v = s.vt(perception_ok=False)
    pr = s.pick(PREP)
    p = f"The {n1} {v[0]} the {n2} {pr} the {n3}."
    return None, [(p, f"The {n1} {v[0]} the {n3}.", "no"), (p, f"The {n1} {v[0]} the {n2}.", "yes")]


def t_pp_subj(s):
    (n1, _), (n2, _) = s.nouns(2)
    vi = s.vi()
    pr = s.pick(PREP)
    p = f"The {n1} {pr} the {n2} {vi[0]}."
    return None, [(p, f"The {n2} {vi[0]}.", "no"), (p, f"The {n1} {vi[0]}.", "yes")]


def t_rel_subseq(s):
    (n1, _), (n2, _) = s.nouns(2)
    v, vi = s.vt(), s.vi()
    rel = s.pick(["who", "that"])
    p = f"The {n1} {rel} {v[0]} the {n2} {vi[0]}."
    return None, [(p, f"The {n2} {vi[0]}.", "no"), (p, f"The {n1} {vi[0]}.", "yes")]


def t_reduced_rel(s):
    (n1, _), (n2, _) = s.nouns(2)
    v, vi = s.vt(), s.vi()
    p = f"The {n1} {v[1]} by the {n2} {vi[0]}."
    return None, [(p, f"The {n2} {vi[0]}.", "no"), (p, f"The {n1} {vi[0]}.", "yes")]


def t_conj_subj(s):
    (n1, _), (n2, _) = s.nouns(2)
    vi = s.vi()
    return None, [(f"Either the {n1} or the {n2} {vi[0]}.", f"The {n2} {vi[0]}.", "no"),
                  (f"Both the {n1} and the {n2} {vi[0]}.", f"The {n2} {vi[0]}.", "yes")]


def t_disj_clause(s):
    (n1, _), (n2, _) = s.nouns(2)
    v1, v2 = s.vi(2)
    return "hypothetical", [(f"Either the {n1} {v1[0]}, or the {n2} {v2[0]}.", f"The {n2} {v2[0]}.", "no"),
                            (f"The {n1} {v1[0]}, and the {n2} {v2[0]}.", f"The {n2} {v2[0]}.", "yes")]


def t_adj_drop(s):
    (n1, _), (n2, _) = s.nouns(2)
    v = s.vt()
    adj = s.pick(ADJ)
    return None, [(f"The {n1} {v[0]} {a(n2)}.", f"The {n1} {v[0]} {a(adj)} {n2}.", "no"),
                  (f"The {n1} {v[0]} {a(adj)} {n2}.", f"The {n1} {v[0]} {a(n2)}.", "yes")]


def t_any_down(s):
    (n1, _), (_, p2) = s.nouns(2)
    v = s.vt()
    adj = s.pick(ADJ)
    return "negation", [(f"The {n1} did not {v[2]} any {adj} {p2}.", f"The {n1} did not {v[2]} any {p2}.", "no"),
                        (f"The {n1} did not {v[2]} any {p2}.", f"The {n1} did not {v[2]} any {adj} {p2}.", "yes")]


def t_every_restrictor(s):
    (n1, _), = s.nouns(1)
    vi = s.vi()
    adj = s.pick(ADJ)
    return "quantifier", [(f"Every {adj} {n1} {vi[0]}.", f"Every {n1} {vi[0]}.", "no"),
                          (f"Every {n1} {vi[0]}.", f"Every {adj} {n1} {vi[0]}.", "yes")]


def t_manner(s):
    (_, p1), = s.nouns(1)
    vi = s.vi()
    adv = s.pick(vi[2])
    return "quantifier", [(f"No {p1} {vi[0]} {adv}.", f"No {p1} {vi[0]}.", "no"),
                          (f"No {p1} {vi[0]}.", f"No {p1} {vi[0]} {adv}.", "yes")]


def t_factive(s):
    (n1, _), (n2, _), (n3, _) = s.nouns(3)
    v = s.vt()
    nf, f = s.pick(NONFACT), s.pick(FACTIVE)
    h = f"The {n2} {v[0]} the {n3}."
    return "reported_speech", [(f"The {n1} {nf} that the {n2} {v[0]} the {n3}.", h, "no"),
                               (f"The {n1} {f} that the {n2} {v[0]} the {n3}.", h, "yes")]


def t_sent_adv(s):
    (n1, _), (n2, _) = s.nouns(2)
    v = s.vt()
    h = f"The {n1} {v[0]} the {n2}."
    return "hypothetical", [(f"{s.pick(ADV_NONVER)}, the {n1} {v[0]} the {n2}.", h, "no"),
                            (f"{s.pick(ADV_VER)}, the {n1} {v[0]} the {n2}.", h, "yes")]


def t_subord_ante(s):
    (n1, _), (n2, _), (n3, _) = s.nouns(3)
    vi, v = s.vi(), s.vt()
    h = f"The {n1} {vi[0]}."
    return "hypothetical", [(f"{s.pick(SUB_NONVER)} the {n1} {vi[0]}, the {n2} {v[0]} the {n3}.", h, "no"),
                            (f"{s.pick(SUB_VER)} the {n1} {vi[0]}, the {n2} {v[0]} the {n3}.", h, "yes")]


def t_subord_main(s):
    (n1, _), (n2, _), (n3, _) = s.nouns(3)
    vi, v = s.vi(), s.vt()
    h = f"The {n2} {v[0]} the {n3}."
    nonver = s.pick(["If", "Provided that"])  # 'even if' / 'unless' excluded here: they suggest the consequent
    return "hypothetical", [(f"{nonver} the {n1} {vi[0]}, the {n2} {v[0]} the {n3}.", h, "no"),
                            (f"{s.pick(SUB_VER)} the {n1} {vi[0]}, the {n2} {v[0]} the {n3}.", h, "yes")]


def t_implicative(s):
    (n1, _), (n2, _) = s.nouns(2)
    v = s.vt(perception_ok=False)  # 'refused to hear' etc. read oddly: perception is not volitional
    y, n = s.pick(IMPL_YES), s.pick(IMPL_NO)
    h = f"The {n1} {v[0]} the {n2}."
    tags = ("hypothetical", "double_negation" if y.startswith("did not") else "hypothetical")
    return tags, [(f"The {n1} {n} {v[2]} the {n2}.", h, "no"), (f"The {n1} {y} {v[2]} the {n2}.", h, "yes")]


def t_negation(s):
    (n1, _), (n2, _) = s.nouns(2)
    v = s.vt()
    h = f"The {n1} {v[0]} the {n2}."
    return "double_negation", [(f"The {n1} did not {v[2]} the {n2}.", h, "no"),
                               (f"It is not true that the {n1} did not {v[2]} the {n2}.", h, "yes")]


def t_neg_swap(s):
    (n1, _), (n2, _) = s.nouns(2)
    v = s.vt()
    p = f"The {n1} did not {v[2]} the {n2}."
    return "negation", [(p, f"The {n2} did not {v[2]} the {n1}.", "no"), (p, f"The {n2} was not {v[1]} by the {n1}.", "yes")]


def t_never(s):
    (n1, _), (n2, _) = s.nouns(2)
    v = s.vt()
    h = f"The {n1} {v[0]} the {n2} at least once."
    return "double_negation", [(f"The {n1} never {v[0]} the {n2}.", h, "no"),
                               (f"It is not the case that the {n1} never {v[0]} the {n2}.", h, "yes")]


def t_all_some(s):
    g = s.pick(GROUPS)
    vi = s.vi()
    return "quantifier", [(f"Some of the {g} {vi[0]}.", f"All of the {g} {vi[0]}.", "no"),
                          (f"All of the {g} {vi[0]}.", f"Some of the {g} {vi[0]}.", "yes")]


def t_not_all(s):
    g = s.pick(GROUPS)
    vi = s.vi()
    p = f"Not all of the {g} {vi[0]}."
    return "quantifier", [(p, f"None of the {g} {vi[0]}.", "no"), (p, f"Some of the {g} did not {vi[1]}.", "yes")]


def t_more_than(s):
    g = s.pick(GROUPS)
    vi = s.vi()
    k = s.rng.randint(2, 11)
    h = f"At least {NUMW[k]} of the {g} {vi[0]}."
    return "numeric", [(f"At least {NUMW[k - 1]} of the {g} {vi[0]}.", h, "no"),
                       (f"More than {NUMW[k - 1]} of the {g} {vi[0]}.", h, "yes")]


def t_at_least_boundary(s):
    g = s.pick(GROUPS)
    vi = s.vi()
    k = s.rng.randint(2, 11)
    h = f"More than {NUMW[k]} of the {g} {vi[0]}."
    return "numeric", [(f"At least {NUMW[k]} of the {g} {vi[0]}.", h, "no"),
                       (f"At least {NUMW[k + 1]} of the {g} {vi[0]}.", h, "yes")]


def t_exactly(s):
    g = s.pick(GROUPS)
    vi = s.vi()
    k = s.rng.randint(3, 10)
    h = f"At most {NUMW[k + 1]} of the {g} {vi[0]}."
    return "numeric", [(f"At least {NUMW[k]} of the {g} {vi[0]}.", h, "no"),
                       (f"Exactly {NUMW[k]} of the {g} {vi[0]}.", h, "yes")]


def t_fewer(s):
    g = s.pick(GROUPS)
    vi = s.vi()
    k = s.rng.randint(3, 11)
    h = f"Fewer than {NUMW[k]} of the {g} {vi[0]}."
    return "numeric", [(f"At most {NUMW[k]} of the {g} {vi[0]}.", h, "no"),
                       (f"At most {NUMW[k - 1]} of the {g} {vi[0]}.", h, "yes")]


def t_except(s):
    g = s.pick(GROUPS)
    x = s.pick(NAMES)
    vi = s.vi()
    h = f"{x} {vi[0]}."
    return "exception", [(f"All of the {g} except {x} {vi[0]}.", h, "no"),
                         (f"All of the {g}, including {x}, {vi[0]}.", h, "yes")]


def t_nobody_except(s):
    x = s.pick(NAMES)
    vi = s.vi()
    h = f"{x} {vi[0]}."
    return "exception", [(f"Nobody {vi[0]}, not even {x}.", h, "no"), (f"Nobody except {x} {vi[0]}.", h, "yes")]


def t_only(s):
    x, y = s.pick(NAMES, 2)
    vi = s.vi()
    h = f"{y} {vi[0]}."
    return "exception", [(f"Only {x} {vi[0]}.", h, "no"), (f"Both {x} and {y} {vi[0]}.", h, "yes")]


def t_still(s):
    x = s.pick(NAMES)
    vp = s.pick(STATES)
    h = f"{x} {vp[0]}."
    return "temporal", [(f"{x} no longer {vp[0]}.", h, "no"), (f"{x} still {vp[0]}.", h, "yes")]


def t_used_to(s):
    x = s.pick(NAMES)
    vp = s.pick(STATES)
    h = f"{x} {vp[0]}."
    return "temporal", [(f"{x} used to {vp[1]}.", h, "no"),
                        (f"{x} started to {vp[1]} last year and still does.", h, "yes")]


TEMPLATES = [t_swap, t_passive, t_relobj, t_relsubj, t_conj_obj, t_pp_obj, t_pp_subj, t_rel_subseq, t_reduced_rel,
             t_conj_subj, t_disj_clause, t_adj_drop, t_any_down, t_every_restrictor, t_manner, t_factive, t_sent_adv,
             t_subord_ante, t_subord_main, t_implicative, t_negation, t_neg_swap, t_never, t_all_some, t_not_all, t_more_than,
             t_at_least_boundary, t_exactly, t_fewer, t_except, t_nobody_except, t_only, t_still, t_used_to]


def main():
    rng = random.Random(SEED)
    s = Slots(rng)
    out, seen = [], set()
    per = Counter()
    for t in TEMPLATES:
        tries = 0
        while per[t.__name__] < PAIRS_PER_TEMPLATE and tries < PAIRS_PER_TEMPLATE * 50:
            tries += 1
            tag, pair = t(s)
            states = [f"Premise: {p}\nHypothesis: {h}" for p, h, _ in pair]
            ks = [C.norm(x) for x in states]
            if any(k in seen for k in ks) or ks[0] == ks[1]:
                continue
            assert {g for _, _, g in pair} == {"yes", "no"}, t.__name__
            seen.update(ks)
            i = per[t.__name__]
            per[t.__name__] += 1
            base = f"{KEY}_{t.__name__[2:]}_{i:03d}"
            rids = [f"{base}_{g}" for _, _, g in pair]
            for j, ((p, h, g), st) in enumerate(zip(pair, states)):
                row_tag = tag[j] if isinstance(tag, tuple) else tag
                out.append({
                    "key": KEY, "rid": rids[j], "state": st, "instructions": INSTRUCTIONS, "options": ["yes", "no"],
                    "gold": g, "soft": None,
                    "meta": {"dataset": "generated (golden_src/gen/gen_nlr_heuristics.py)", "config": t.__name__[2:],
                             "revision": f"seed {SEED}", "licence": LICENCE, "split": "train", "orig_label": g,
                             "family": C.FAMILY, "edge": row_tag, "twin_of": rids[1 - j], "generator_seed": SEED},
                })
    print("pairs per template:", dict(per))
    rng.shuffle(out)
    C.validate_rows(KEY, out, {None: DEFS})
    C.write_rows(KEY, out)
    C.write_defs(KEY, DEFS)
    share = C.report(KEY, out)
    e = Counter(r["meta"]["edge"] for r in out)
    C.append_manifest({
        "key": KEY, "family": C.FAMILY, "dataset": "generated: HANS-style heuristic-breaking entailment pairs",
        "licence": LICENCE, "rows": len(out), "qtype": "yesno", "yesno_share": round(share, 4),
        "edge_tags": sorted(k for k in e if k),
        "notes": "34 Claude-written templates (lexical overlap, subsequence, constituent, factive vs non-factive, "
                 "implicatives, sentence adverbs, conditionals, negation / double negation, monotonicity, numeric "
                 "boundaries, exceptives, only, still / no longer), every row with a fact-flip twin (meta.twin_of).",
    })
    if "--show" in sys.argv:
        C.show_samples(out, 12)


if __name__ == "__main__":
    main()
