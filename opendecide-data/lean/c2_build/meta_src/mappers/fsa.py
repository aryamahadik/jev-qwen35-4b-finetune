"""md_fsa mapper (A42-D 8): UK Food Hygiene Rating Scheme open data (OGL v3.0). Gold = program function of the record
fields BusinessType, LocalAuthorityName, RatingValue, RatingDate, scores.{Hygiene, Structural, ConfidenceInManagement}.
Business names, addresses, postcodes and ids are never read into a row. Run from c2_build: python -B meta_src/mappers/fsa.py"""
import json, sys
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import mdlib as M  # noqa: E402

RAW = Path(__file__).resolve().parents[1] / "raw" / "fsa"
E = []
for l in open(RAW / "establishments.jsonl", encoding="utf-8"):
    f = json.loads(l)
    sc = f.get("scores") or {}
    if f["rating"] in "012345" and len(f["rating"]) == 1 and f["scheme"] == "FHRS" and f.get("rdate") and all(isinstance(sc.get(k), int) for k in ("Hygiene", "Structural", "ConfidenceInManagement")):
        E.append({"id": str(f["fhrsid"]), "bt": f["bt"], "rating": f["rating"], "month": int(f["rdate"][5:7]), "la": f["la"],
                  "h": sc["Hygiene"], "s": sc["Structural"], "c": sc["ConfidenceInManagement"]})
LAS = sorted({e["la"] for e in E})
LAG = {la: i % 14 for i, la in enumerate(sorted(LAS, key=lambda x: M.h("la", x)))}
by_g = defaultdict(list)
for e in E:
    by_g[LAG[e["la"]]].append(e)

B = M.Block("md_fsa", "food_safety", "Food Hygiene Rating Scheme (FHRS) open data", "api.ratings.food.gov.uk",
            "Open Government Licence v3.0", "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
            "dataset 38dd8d6a-5ab1-4f50-b753-ab33288e3200", [RAW / "establishments.jsonl", RAW / "authorities.json"])
B.form("member", 1, ["Is this establishment eligible under the rule?", "Does this establishment meet the rule?"])
B.form("group", 0, ["Which group does this establishment fall into under the definitions?", "Under the definitions, which group holds this establishment?"], qtype="choice")
B.form("month_h1", 1, ["Was the rating given in the first half of the year?", "Does the rating date fall in January to June?"])
B.form("month_h2", 1, ["Was the rating given in the second half of the year?", "Does the rating date fall in July to December?"])
B.form("cmp_hs", 1, ["Is the hygiene score higher than the structural score?", "Does the hygiene score exceed the structural score?"])
B.form("cmp_sh", 1, ["Is the structural score higher than the hygiene score?", "Does the structural score exceed the hygiene score?"])
B.form("pass3", 1, ["Does the rating meet the pass mark of 3 or higher?", "Is the rating at least 3?"])
B.form("below3", -1, ["Does the rating fall below the pass mark of 3?", "Is the rating lower than 3?"])
B.form("hilo", 0, ["Which of the three scores is the highest?", "Which score has the largest value?",
                   "Which of the three scores is the lowest?", "Which score has the smallest value?"], qtype="choice")
uses = Counter()
N, NF = 24, 26
rec = lambda e: f"Food hygiene record\nBusiness type: {e['bt']}\nLocal authority: {e['la']}\nRating: {e['rating']}"
q0 = lambda e: {}
btc = Counter({k: v ** 0.5 for k, v in Counter(e["bt"] for e in E).items()})
lac = Counter({la: 1 for la in LAS})
rtc = Counter({k: v ** 0.5 for k, v in Counter(e["rating"] for e in E).items()})
lst = M.lst

for g in range(8):
    task = f"fsa:member_bt:g{g:02d}"
    B.task(task, "member", "yes/no", "rules_in_card", f"g{g:02d}")
    M.member_yn(B, task, "member", by_g[g], lambda e: e["bt"], None, N, 3, M.R(task), btc, rec, q0,
                lambda S: f"- yes: The business type is {lst(S)}.\n- no: The business type is any other type.", uses, 4)
    task = f"fsa:group_bt:g{g:02d}"
    M.group_choice(B, task, "group", by_g[(g + 7) % 14], lambda e: e["bt"], btc, N, rec, q0, uses, "the business type is", f"g{(g + 7) % 14:02d}", 4)
for g, g2 in ((8, 9), (10, 11), (12, 13)):
    pool = by_g[g] + by_g[g2]
    task = f"fsa:member_la:g{g:02d}"
    B.task(task, "member", "yes/no", "rules_in_card", f"g{g:02d}+g{g2:02d}")
    M.member_yn(B, task, "member", pool, lambda e: e["la"], None, N, 3, M.R(task), lac, rec, q0,
                lambda S: f"- yes: The local authority is {lst(S)}.\n- no: The local authority is any other.", uses, 4)
    task = f"fsa:group_la:g{g:02d}"
    M.group_choice(B, task, "group", pool, lambda e: e["la"], lac, N, rec, q0, uses, "the local authority is", f"g{g:02d}+g{g2:02d}", 4)
    task = f"fsa:member_rating:g{g:02d}"
    B.task(task, "member", "yes/no", "rules_in_card", f"g{g:02d}+g{g2:02d}")
    M.member_yn(B, task, "member", pool, lambda e: e["rating"], None, N, 2, M.R(task), rtc, rec, q0,
                lambda S: f"- yes: The rating is {lst(S)}.\n- no: The rating is any other value.", uses, 4)
    task = f"fsa:group_rating:g{g:02d}"
    M.group_choice(B, task, "group", pool, lambda e: e["rating"], rtc, N, rec, q0, uses, "the rating is", f"g{g:02d}+g{g2:02d}", 4, setsize=1)


def two_form(task, forms, pool, n, cond, state_fn, slice_name):
    """Card-free yes/no where the question form is a coin (so the state alone never fixes the answer)."""
    B.task(task, forms[0], "yes/no", "none", slice_name)
    rng = M.R(task)
    ents = [e for e in pool if uses[e["id"]] < 3]
    rng.shuffle(ents)
    got = 0
    for yes in M.balanced(n, rng):
        f = rng.choice(forms)
        for e in ents:
            if uses[e["id"]] < 3 and (task, e["id"]) not in B.used and cond(f, e) == yes:
                q, wid = B.say(f, e["id"])
                if B.add(task, e["id"], state_fn(e), q, int(yes), wording_id=wid, qform=f):
                    uses[e["id"]] += 1
                    got += 1
                    break
    return got


for i in range(2):
    pool = by_g[i] + by_g[i + 2]
    two_form(f"fsa:month:{i}", ["month_h1", "month_h2"], pool, NF, lambda f, e: (e["month"] <= 6) == (f == "month_h1"),
             lambda e: f"Food hygiene record\nBusiness type: {e['bt']}\nRating date: {['January','February','March','April','May','June','July','August','September','October','November','December'][e['month']-1]} (rating {e['rating']})", f"g{i}+g{i+2}")
for i in range(4):
    pool = [e for e in by_g[4 + i] + by_g[(8 + i) % 14] if e["h"] != e["s"]]
    two_form(f"fsa:cmp:{i}", ["cmp_hs", "cmp_sh"], pool, NF, lambda f, e: (e["h"] > e["s"]) == (f == "cmp_hs"),
             lambda e: f"Food hygiene record\nBusiness type: {e['bt']}\nHygiene score: {e['h']}\nStructural score: {e['s']}\nConfidence in management score: {e['c']}", f"p{i}")
for i in range(2):
    pool = [e for g in range(6, 14) for e in by_g[g]]
    two_form(f"fsa:pass:{i}", ["pass3", "below3"], pool, NF, lambda f, e: (int(e["rating"]) >= 3) == (f == "pass3"), rec, f"g{i}")

NAMES = ["hygiene score", "structural score", "confidence in management score"]
for i in range(6):
    task = f"fsa:hilo:{i}"
    B.task(task, "hilo", "choice", "none", f"p{i}")
    rng = M.R(task)
    pool = by_g[i] + by_g[(i + 7) % 14] + by_g[(i + 3) % 14]
    cls, hl = M.positions(NF, 3, rng), [rng.random() < 0.5 for _ in range(NF)]
    ents = list(pool)
    rng.shuffle(ents)
    got = 0
    for e in ents:
        if got == NF:
            break
        v = [e["h"], e["s"], e["c"]]
        hi = hl[got]
        best = max(v) if hi else min(v)
        if v.count(best) != 1 or len(set(v)) < 2 or v.index(best) != cls[got] or uses[e["id"]] >= 3:
            continue
        txt = ["Which of the three scores is the highest?", "Which score has the largest value?"] if hi else ["Which of the three scores is the lowest?", "Which score has the smallest value?"]
        q = txt[int(M.h(task, e["id"])[:2], 16) % 2]
        opts = NAMES[:]
        rng.shuffle(opts)
        if B.add(task, e["id"], f"Food hygiene record\nBusiness type: {e['bt']}\nHygiene score: {e['h']}\nStructural score: {e['s']}\nConfidence in management score: {e['c']}",
                 q, NAMES[cls[got]], options=opts, wording_id=f"md_fsa.hilo#{int(hi)}", opt_err={o: "other_score" for o in opts if o != NAMES[cls[got]]}):
            uses[e["id"]] += 1
            got += 1

if __name__ == "__main__":
    qc = B.finalize()
    print(json.dumps({k: qc[k] for k in ("rows", "tasks", "rows_per_task", "yes_no_share", "yes_share_in_yes_no", "card_free_share",
                                         "problems", "per_task_yes_dev_max", "max_near_dup_jaccard_in_task", "partial_input")}, default=str))
