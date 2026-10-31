"""rk_resp: which reply / draft / answer best meets an answer key under a stated grading rubric.

Rubrics (all stated in the text):
  cc   correct and complete: every key point stated correctly (equivalent wording counts), nothing contradicts the key
       (statements the key does not cover are ignored); at most one reply qualifies; else 'none of the ...'.
  pts  points: +pc per key point stated correctly, -pw per key point contradicted (even if also stated correctly
       elsewhere), 0 if left out; highest total wins; ties -> the reply sent earliest.
  ess  essential points: a reply fails if it misses or contradicts an essential point or contradicts any key point;
       among passing replies the most other key points stated correctly wins (ties -> sent earliest); none passes ->
       'none of the ...'.
Per-fact status of a reply: 'c' stated correctly, 'w' stated wrongly, 'o' left out, 'cw' stated correctly AND
wrongly (a self-contradiction; counts as contradicted).
"""
import copy
import random

from rk_core import fmt_time
from rk_topics import TOPICS, TOPIC

RUBRICS = ["cc", "pts", "ess"]
WORDS = ["Response", "Reply", "Draft", "Answer"]
GREET = ["Hi there!", "Hello!", "Thanks for getting in touch.", "Good question!", "Hi!", ""]
CLOSE = ["Hope that helps.", "Let us know if you need anything else.", "Best wishes.", "Thanks again.", "", ""]
KEYNAMES = ["Answer key", "Policy excerpt", "Knowledge-base article", "Reference answer", "Official guidance"]
AGENTS = ["Priya", "Tom", "Aisha", "Jonas", "Mei", "Carlos", "Grace", "Omar", "Lena", "Sam"]


def lw_of(word):
    return word.lower()


def plural(w):
    return w[:-1] + "ies" if w.endswith("y") else w + "s"


def none_opt(word):
    return f"none of the {plural(lw_of(word))}"


def fact_ok(st):
    return st == "c"


def contradicted(st):
    return st in ("w", "cw")


def grade(item, statuses=None, key=None):
    """Primary evaluator: returns the winning label or 'NONE'."""
    sts = statuses if statuses is not None else [r["st"] for r in item["resps"]]
    rub = item["rubric"]
    labels = [r["label"] for r in item["resps"]]
    sent = [r["sent"] for r in item["resps"]]
    fids = [f["id"] for f in item["facts"]]
    if rub == "cc":
        ok = [i for i, s in enumerate(sts) if all(s[f] == "c" for f in fids)]
        if not ok:
            return "NONE"
        if len(ok) > 1:
            return "MULTI"
        return labels[ok[0]]
    if rub == "pts":
        pc, pw = item["pc"], item["pw"]
        sc = [sum(pc if s[f] == "c" else (-pw if contradicted(s[f]) else 0) for f in fids) for s in sts]
        best = max(sc)
        cands = [i for i in range(len(sts)) if sc[i] == best]
        return labels[min(cands, key=lambda i: sent[i])]
    ess = item["ess"]
    ok = [i for i, s in enumerate(sts) if all(s[f] == "c" for f in ess) and not any(contradicted(s[f]) for f in fids)]
    if not ok:
        return "NONE"
    cnt = {i: sum(sts[i][f] == "c" for f in fids if f not in ess) for i in ok}
    best = max(cnt.values())
    cands = [i for i in ok if cnt[i] == best]
    return labels[min(cands, key=lambda i: sent[i])]


def rand_status(rng, fids, defects=None):
    s = {}
    for f in fids:
        s[f] = rng.choices(["c", "w", "o", "cw"], weights=[62, 18, 17, 3])[0]
    if defects is not None:
        s = {f: "c" for f in fids}
        for f in rng.sample(fids, defects):
            s[f] = rng.choices(["w", "o", "cw"], weights=[55, 38, 7])[0]
    return s


def sample(rng):
    topic = rng.choice(TOPICS)
    facts = list(topic["facts"])
    if rng.random() < 0.25:
        facts.pop(rng.randrange(len(facts)))
    rng.shuffle(facts)
    key = {}
    for f in facts:
        key[f["id"]] = rng.choice(f["vals"]) if f["kind"] == "val" else rng.random() < 0.5
    rub = rng.choices(RUBRICS, weights=[45, 30, 25])[0]
    word = rng.choice(WORDS if topic["area"] in ("exam administration", "school science", "cooking class")
                      else WORDS[:3])
    n = rng.choices([3, 4, 5, 6], weights=[25, 35, 28, 12])[0]
    fids = [f["id"] for f in facts]
    item = {"topic": topic["key"], "facts": [{"id": f["id"]} for f in facts], "key": key, "rubric": rub,
            "word": word, "resps": [], "pc": 1, "pw": 1, "ess": []}
    if rub == "pts":
        item["pc"], item["pw"] = rng.choice([(1, 1), (2, 1), (1, 2), (2, 3), (3, 1)])
    if rub == "ess":
        item["ess"] = rng.sample(fids, rng.choice([1, 2, 2]))
    sts = []
    if rub == "cc":
        g = rng.randrange(n) if rng.random() < 0.8 else None
        for i in range(n):
            if i == g:
                sts.append({f: "c" for f in fids})
            else:
                sts.append(rand_status(rng, fids, defects=1 if rng.random() < 0.6 else rng.randint(1, len(fids))))
    else:
        for i in range(n):
            sts.append(rand_status(rng, fids, defects=None if rng.random() < 0.5 else rng.randint(0, 2)))
    base = rng.randrange(8 * 60, 17 * 60)
    times = rng.sample(range(base, base + 240), n)
    agents = rng.sample(AGENTS, n)
    for i in range(n):
        item["resps"].append({"label": f"{word} {i + 1}", "st": sts[i], "sent": times[i], "agent": agents[i]})
    # surface choices per response and fact
    for r in item["resps"]:
        r["wrong"] = {}
        r["say"] = {}
        r["eq"] = {}
        for f in facts:
            fid = f["id"]
            r["say"][fid] = rng.randrange(len(f["say"] if f["kind"] == "val" else f["say_t"]))
            if f["kind"] == "val":
                others = [v for v in f["vals"] if v != key[fid]]
                r["wrong"][fid] = rng.choice(others)
                r["eq"][fid] = rng.random() < 0.3
        r["greet"] = rng.choice(GREET)
        r["close"] = rng.choice(CLOSE)
        r["extras"] = rng.sample(topic["extras"], rng.choice([0, 0, 1, 1, 2]))
        r["order"] = rng.random()
        r["shuffle"] = rng.randrange(10 ** 6)
    item["r"] = {"keyname": rng.randrange(len(KEYNAMES)), "q": rng.randrange(1000), "rub": rng.randrange(3),
                 "tstyle": rng.randint(0, 1), "layout": rng.randrange(3), "ask": rng.randrange(3)}
    return item


def fact_def(item, fid):
    return next(f for f in TOPIC[item["topic"]]["facts"] if f["id"] == fid)


def clause(item, r, fid, correct):
    f = fact_def(item, fid)
    k = item["key"][fid]
    if f["kind"] == "val":
        v = k if correct else r["wrong"][fid]
        if correct and r["eq"].get(fid) and f["eq"].get(v):
            v = f["eq"][v][r["say"][fid] % len(f["eq"][v])]
        return f["say"][r["say"][fid]].format(v=v)
    truth = k if correct else (not k)
    lst = f["say_t"] if truth else f["say_f"]
    return lst[r["say"][fid] % len(lst)]


def sentence(c):
    return c[0].upper() + c[1:] + "."


def response_text(item, r):
    rng = random.Random(r["shuffle"])
    parts = []
    for f in item["facts"]:
        fid = f["id"]
        st = r["st"][fid]
        if st == "c":
            parts.append(sentence(clause(item, r, fid, True)))
        elif st == "w":
            parts.append(sentence(clause(item, r, fid, False)))
        elif st == "cw":
            parts.append(sentence(clause(item, r, fid, True)))
            parts.append(sentence(clause(item, r, fid, False)))
    parts += list(r["extras"])
    rng.shuffle(parts)
    # a self-contradiction must not be adjacent-with-correction; shuffling keeps both as plain statements
    if not parts:
        parts = ["Please check our website for details."]
    body = " ".join(parts)
    if r["greet"]:
        body = r["greet"] + " " + body
    if r["close"]:
        body = body + " " + r["close"]
    return body


def key_lines(item):
    out = []
    for f in item["facts"]:
        fd = fact_def(item, f["id"])
        k = item["key"][f["id"]]
        s = fd["key"].format(v=k) if fd["kind"] == "val" else (fd["key_t"] if k else fd["key_f"])
        if f["id"] in item["ess"]:
            s += " (essential)"
        out.append(s)
    return out


def rubric_text(item):
    w = lw_of(item["word"])
    wp = plural(w)
    rub = item["rubric"]
    v = item["r"]["rub"]
    if rub == "cc":
        return ["Grading rule: a {w} passes only if it is correct and complete, meaning it states every point in the "
                "key and none of its statements contradicts the key. Statements about things the key does not cover "
                "are ignored, and different wording with the same meaning is fine.",
                "A {w} counts as correct and complete when it covers every key point and says nothing that contradicts "
                "the key; extra remarks the key does not mention are ignored, and equivalent wording is accepted.",
                "Only a correct and complete {w} may be sent: all key points present, no statement contradicting the "
                "key (anything the key does not address is ignored; equivalent wording is fine)."][v].format(w=w)
    if rub == "pts":
        pc, pw = item["pc"], item["pw"]
        return [f"Scoring: +{pc} for each key point a {w} states correctly, -{pw} for each key point it contradicts "
                f"(even if it also states that point correctly elsewhere), 0 for points it leaves out. The highest "
                f"score wins; if tied, the {w} sent earliest wins. Statements the key does not cover are ignored.",
                f"Each {w} earns {pc} point(s) per key point stated correctly and loses {pw} point(s) per key point it "
                f"gets wrong or contradicts anywhere; omitted points score 0. Highest total wins, ties going to the "
                f"earliest-sent {w}. Remarks outside the key are ignored.",
                f"Rubric: correct key point = +{pc}; contradicted key point = -{pw} (a point both stated correctly and "
                f"contradicted counts as contradicted); missing = 0. Pick the highest-scoring {w}; ties go to the one "
                f"sent first. Anything the key does not cover is ignored."][v]
    return [f"Grading: a {w} fails if it leaves out or contradicts any point marked (essential), or contradicts any "
            f"other key point. Among the {wp} that pass, choose the one that states the most of the non-essential "
            f"key points; if tied, the {w} sent earliest. If no {w} passes, none is chosen. Statements the key does "
            f"not cover are ignored.",
            f"Essential points must all be stated correctly and no key point may be contradicted; {wp} that break "
            f"either rule are out. The remaining {w} covering the most other key points is chosen (ties: sent "
            f"earliest). If every {w} is out, none is chosen. Remarks outside the key are ignored.",
            f"Pass/fail first: every (essential) point stated correctly and nothing contradicting the key. Then rank "
            f"passing {wp} by how many other key points they state correctly, earliest-sent first on ties. No "
            f"passing {w} means none is chosen. Extra remarks the key does not mention are ignored."][v]


def render(item):
    topic = TOPIC[item["topic"]]
    r = item["r"]
    w = item["word"]
    who = topic["who"]
    ask = topic["ask"]
    org = topic["org"][0].upper() + topic["org"][1:]
    head = [f"{org} - {topic['area']}\n{who[0].upper() + who[1:]} asked: \"{ask}\"",
            f"Question from {who} to {topic['org']}: \"{ask}\"",
            f"Ticket ({topic['area']}, {topic['org']}): \"{ask}\""][r["ask"]]
    kn = KEYNAMES[r["keyname"]]
    key = f"{kn} ({topic['ref']}):\n" + "\n".join(f"- {x}" for x in key_lines(item))
    rub = rubric_text(item)
    lines = []
    for resp in item["resps"]:
        t = fmt_time(resp["sent"], r["tstyle"])
        txt = response_text(item, resp)
        if r["layout"] == 0:
            lines.append(f"{resp['label']} (sent {t} by {resp['agent']}): {txt}")
        elif r["layout"] == 1:
            lines.append(f"{resp['label']} - {resp['agent']}, sent {t}\n\"{txt}\"")
        else:
            lines.append(f"[{resp['label']} | {t} | {resp['agent']}]\n{txt}")
    sep = "\n\n" if r["layout"] else "\n"
    state = f"{head}\n\n{key}\n\n{rub}\n\n" + sep.join(lines)
    return state, question(item), options(item)


QT = {"cc": ["Which {w} is correct and complete according to the key?",
             "Under the grading rule, which {w} passes?",
             "Which {w} may be sent, given that only a correct and complete one is allowed?",
             "Checked against the key, which {w} is both correct and complete?",
             "Which {w} meets the grading rule stated above?"],
      "pts": ["Which {w} wins under the scoring rubric?",
              "Applying the rubric exactly, which {w} scores highest (after the tie rule)?",
              "Which {w} should be chosen according to the scoring rules?",
              "Which {w} comes out on top when scored against the key?"],
      "ess": ["Which {w} should be chosen under the grading rules?",
              "Applying the essential-point rule and the ranking, which {w} is selected?",
              "Which {w} is picked according to the grading instructions?",
              "Following the pass/fail rule and then the ranking, which {w} wins?"]}


def question(item):
    tl = QT[item["rubric"]]
    return tl[item["r"]["q"] % len(tl)].format(w=lw_of(item["word"]))


def options(item):
    labs = [r["label"] for r in item["resps"]]
    if item["rubric"] in ("cc", "ess"):
        labs.append(none_opt(item["word"]))
    return labs


def gold_option(item, out):
    return none_opt(item["word"]) if out == "NONE" else out


def edges(item):
    e = ["quantifier"]
    if item["rubric"] in ("pts", "ess"):
        e.append("numeric")
        e.append("temporal")
    if any(r["st"][f["id"]] == "cw" for r in item["resps"] for f in item["facts"]):
        e.append("conflicting_evidence")
    if any(fact_def(item, f["id"])["kind"] == "bool" for f in item["facts"]):
        e.append("negation")
    if any(r["eq"].get(f["id"]) and fact_def(item, f["id"]).get("eq", {}).get(item["key"][f["id"]])
           and r["st"][f["id"]] in ("c", "cw") for r in item["resps"] for f in item["facts"]):
        e.append("units")
    e.append("multi_hop")
    return list(dict.fromkeys(e))


# ------------------------------------------------------------------------------------------------ twins
def twin(item, rng, base_out):
    """One fact changes: one reply's statement on one key point, or one value in the key."""
    cands = []
    fids = [f["id"] for f in item["facts"]]
    for i, r in enumerate(item["resps"]):
        for f in fids:
            for ns in ("c", "w", "o", "cw"):
                if ns == r["st"][f] or (ns == "cw" and rng.random() < 0.7):
                    continue
                it2 = copy.deepcopy(item)
                it2["resps"][i]["st"][f] = ns
                o2 = grade(it2)
                if o2 not in (base_out, "MULTI"):
                    cands.append((it2, {"type": "reply", "reply": r["label"], "fact": f, "old": r["st"][f],
                                        "new": ns}, o2, 1.0))
    for f in item["facts"]:
        fd = fact_def(item, f["id"])
        if fd["kind"] != "val":
            continue
        for v in fd["vals"]:
            if v == item["key"][f["id"]]:
                continue
            if any(r0["st"][f["id"]] == "cw" for r0 in item["resps"]):
                continue
            it2 = copy.deepcopy(item)
            old = it2["key"][f["id"]]
            it2["key"][f["id"]] = v
            # replies that stated the old value correctly now state it wrongly, and replies whose wrong value is v
            # now state it correctly (their surface text is unchanged)
            ok = True
            for r2 in it2["resps"]:
                st = r2["st"][f["id"]]
                if st in ("w", "cw") and r2["wrong"][f["id"]] == v:
                    if st == "cw":
                        ok = False
                        break
                    r2["st"][f["id"]] = "c"
                    r2["wrong"][f["id"]] = old
                    r2["eq"][f["id"]] = False
                elif st == "c":
                    if r2["eq"].get(f["id"]) and fd["eq"].get(old):
                        ok = False  # an equivalent rendering of the old value would need re-wording
                        break
                    r2["st"][f["id"]] = "w"
                    r2["wrong"][f["id"]] = old
                elif st in ("w", "cw"):
                    pass  # still wrong under the new key (its value differs from v)
            if not ok:
                continue
            for r2 in it2["resps"]:
                if r2["st"][f["id"]] == "cw" and r2["wrong"][f["id"]] == v:
                    ok = False
            if not ok:
                continue
            o2 = grade(it2)
            if o2 not in (base_out, "MULTI"):
                cands.append((it2, {"type": "key", "fact": f["id"], "old": old, "new": v}, o2, 2.5))
    if not cands:
        return None
    wts = [c[3] * (0.35 if c[2] == "NONE" else 1.0) for c in cands]
    it2, desc, o2, _ = rng.choices(cands, weights=wts)[0]
    return it2, desc, o2


def build(rng):
    it = sample(rng)
    out = grade(it)
    if out == "MULTI":
        return None
    return it, out
