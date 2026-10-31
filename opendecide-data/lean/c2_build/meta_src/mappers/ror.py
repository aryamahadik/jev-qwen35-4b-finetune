"""md_ror mapper (A42-D 8): ROR registry (CC0 1.0). Gold = program function of the record fields types, established, country
code, relationships. Org names are inputs only (institutions). Run from c2_build: python -B meta_src/mappers/ror.py"""
import json, sys
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import mdlib as M  # noqa: E402

RAW = Path(__file__).resolve().parents[1] / "raw" / "ror"
O = []
for l in open(RAW / "orgs.jsonl", encoding="utf-8"):
    o = json.loads(l)
    if o["name"] and o["cc"] and o["cname"] and o["status"] == "active":
        o["id"] = o["id"].rsplit("/", 1)[-1]
        o["ty"] = o["types"][0] if o["types"] and len(o["types"]) == 1 else None
        o["name"] = o["name"].strip()
        O.append(o)
dup = Counter(o["name"] for o in O)
O = [o for o in O if dup[o["name"]] == 1]
ANGLO, EU = {"GB", "CA", "AU", "IE", "NZ"}, {"DE", "FR", "NL", "SE", "CH", "IT", "ES", "PT", "AT", "BE", "DK", "NO", "FI", "PL", "CZ", "GR"}
ASIA = {"CN", "JP", "KR", "IN", "ID", "IR", "TR", "TW", "TH", "MY", "PK", "SG"}


def grp(o):
    c = o["cc"]
    return "US" if c == "US" else "ANGLO" if c in ANGLO else "EU" if c in EU else "ASIA" if c in ASIA else "REST"


GROUPS = ["US", "ANGLO", "EU", "ASIA", "REST"]
TYG = {"education": ["education"], "company": ["company"], "health": ["healthcare"], "np_gov": ["nonprofit", "government"],
       "other": ["other", "facility", "archive", "funder"]}

B = M.Block("md_ror", "research_organisations", "Research Organization Registry (ROR)", "api.ror.org", "CC0 1.0 Universal (data)",
            "https://ror.org/about/", "ROR registry v2 (api.ror.org/v2/organizations)", [RAW / "orgs.jsonl"])
B.form("type", 0, ["What type of organization is {o} ({k})?", "Which type does the registry give for {o} ({k})?"], qtype="choice")
B.form("est_after", 1, ["Was {o} ({k}) established in {T} or after?", "Is {o} ({k}) an organization founded in {T} or later?"])
B.form("est_before", -1, ["Was {o} ({k}) established before {T}?", "Is {o} ({k}) an organization founded before {T}?"])
B.form("loc", 1, ["Is {o} located in {K}?", "Is the country of {o} {K}?"])
B.form("country", 0, ["In which country is {o}?", "Which country is {o} located in?"], qtype="choice")
B.form("rel", 1, ["Does {o} ({k}) have a parent or child organization listed in the registry?",
                  "Is {o} ({k}) linked to a parent or child organization in the registry?"])
B.form("period", 0, ["In which period was {o} ({k}) established?", "Which period holds the founding year of {o} ({k})?"], qtype="choice")
B.form("member", 1, ["Is {o} eligible under this rule?", "Does {o} meet this rule?"])
B.form("group", 0, ["Which group does {o} fall into under these definitions?", "Under the definitions, which group holds {o}?"], qtype="choice")
uses = Counter()
ident = lambda x: x
st2 = lambda o: f"Organization: {o['name']}\nCountry: {o['cname']}"
qa = lambda o: {"o": o["name"], "k": o["cname"]}
N = 26


def period(o):
    y = o["established"]
    return None if y is None else "before 1800" if y < 1800 else "1800-1899" if y < 1900 else "1900-1949" if y < 1950 else "1950-1999" if y < 2000 else "2000 or later"


def lst(S):
    S = list(S)
    return ", ".join(S[:-1]) + " or " + S[-1]


for g in GROUPS:
    pool = [o for o in O if grp(o) == g]
    B.choice_task(f"ror:type:{g}", "type", [o for o in pool if o["ty"]], N, lambda o: o["ty"], ident, st2, qa, g, "other_type", uses, wpow=0.5)
    B.year_task(f"ror:est_after:{g}", "est_after", pool, 14, lambda o: o["established"], True, qa, st2, uses, g)
    B.year_task(f"ror:est_before:{g}", "est_before", pool, 14, lambda o: o["established"], False, qa, st2, uses, g)
    B.choice_task(f"ror:period:{g}", "period", pool, N, period, ident, st2, qa, g, "other_period", uses, kmax=4)
for tg, types in TYG.items():
    pool = [o for o in O if o["ty"] in types]
    cc = Counter(o["cname"] for o in pool)
    B.task(f"ror:loc:{tg}", "loc", "yes/no", "none", tg)
    rng = M.R("loc", tg)
    ents = list(pool)
    rng.shuffle(ents)
    coins = M.balanced(N, rng)
    got = 0
    for o in ents:
        if got == N:
            break
        if uses[o["id"]] >= 2:
            continue
        yes = coins[got]
        K = o["cname"] if yes else M.draw_set(Counter({a: w for a, w in cc.items() if a != o["cname"]}), 1, rng)[0]
        q, wid = B.say("loc", o["id"], o=o["name"], K=K)
        if B.add(f"ror:loc:{tg}", o["id"], f"Organization: {o['name']}", q, int(yes), wording_id=wid):
            uses[o["id"]] += 1
            got += 1
    if tg in ("education", "health", "np_gov", "other"):
        B.choice_task(f"ror:country:{tg}", "country", pool, N, lambda o: o["cname"], ident, lambda o: f"Organization: {o['name']}",
                      lambda o: {"o": o["name"]}, tg, "other_country", uses, wpow=0.7)
# relationships (balanced pools: with / without parent-child link)
for tg in ("education", "health", "other"):
    task = f"ror:rel:{tg}"
    B.task(task, "rel", "yes/no", "none", tg)
    rng = M.R(task)
    pool = [o for o in O if o["ty"] in TYG[tg] and uses[o["id"]] < 2]
    pos = [o for o in pool if any(r in ("parent", "child") for r in o["rel"])]
    neg = [o for o in pool if not any(r in ("parent", "child") for r in o["rel"])]
    rng.shuffle(pos); rng.shuffle(neg)
    n_ = min(N, 2 * len(pos))
    for i, yes in enumerate(M.balanced(n_, rng)):
        lst_ = pos if yes else neg
        if not lst_:
            continue
        o = lst_.pop()
        q, wid = B.say("rel", o["id"], o=o["name"], k=o["cname"])
        if B.add(task, o["id"], f"Organization: {o['name']}\nCountry: {o['cname']}", q, int(yes), wording_id=wid):
            uses[o["id"]] += 1
# card tasks (membership; value drawn first, coin only decides membership)
tyc = Counter(o["ty"] for o in O if o["ty"])
ccn = Counter(o["cname"] for o in O)
for g in GROUPS[:3]:
    task = f"ror:member_type:{g}"
    B.task(task, "member", "yes/no", "rules_in_card", g)
    M.member_yn(B, task, "member", [o for o in O if grp(o) == g and o["ty"]], lambda o: o["ty"], None, N, 2, M.R(task), tyc,
                lambda o: f"Organization: {o['name']}\nCountry: {o['cname']}\nType (record): {o['ty']}", lambda o: {"o": o["name"]},
                lambda S: f"- yes: The organization's type is {lst(S)}.\n- no: The organization has any other type.", uses, 6)
for tg in ("education", "company", "health"):
    task = f"ror:member_country:{tg}"
    B.task(task, "member", "yes/no", "rules_in_card", tg)
    M.member_yn(B, task, "member", [o for o in O if o["ty"] in TYG[tg]], lambda o: o["cname"], None, N, 3, M.R(task), ccn, st2,
                lambda o: {"o": o["name"]}, lambda S: f"- yes: The organization is located in {lst(S)}.\n- no: The organization is located in any other country.", uses, 6)
LAB = ["Group A", "Group B", "Group C", "None of these groups"]
for tg in ("education", "company", "np_gov", "health"):
    task = f"ror:group:{tg}"
    B.task(task, "group", "choice", "rules_in_card", tg)
    rng = M.R(task)
    ents = [o for o in O if o["ty"] in TYG[tg] and uses[o["id"]] < 6]
    rng.shuffle(ents)
    cls, pos, got = M.positions(N, 4, rng), M.positions(N, 4, rng), 0
    for o in ents:
        if got == N:
            break
        c, v = cls[got], o["cname"]
        others = M.draw_set(Counter({a: w for a, w in ccn.items() if a != v}), 9, rng)
        sets = [others[0:3], others[3:6], others[6:9]]
        if c < 3:
            sets[c][rng.randrange(3)] = v
        card = "\n".join([f"- {LAB[j]}: {lst(sets[j])}" for j in range(3)] + ["- None of these groups: any other country"])
        order = [x for x in LAB if x != LAB[c]]
        rng.shuffle(order)
        opts = order[:]
        opts.insert(pos[got], LAB[c])
        q, wid = B.say("group", o["id"], o=o["name"])
        if B.add(task, o["id"], st2(o), q, LAB[c], options=opts, card=card, wording_id=wid, depth=1, opt_err={x: "wrong_group" for x in order}):
            uses[o["id"]] += 1
            got += 1

if __name__ == "__main__":
    qc = B.finalize()
    print(json.dumps({k: qc[k] for k in ("rows", "tasks", "rows_per_task", "yes_no_share", "yes_share_in_yes_no", "card_free_share",
                                         "problems", "per_task_yes_dev_max", "max_near_dup_jaccard_in_task", "partial_input")}, default=str))
