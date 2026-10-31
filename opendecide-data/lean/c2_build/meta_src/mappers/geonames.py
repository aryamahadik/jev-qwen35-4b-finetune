"""md_geonames mapper (A42-D 8): GeoNames cities15000 gazetteer (CC BY 4.0) -> metadata tasks.
Gold = a program function of the upstream fields population, dem, timezone, feature code, country code, admin1 code,
countryInfo capital. Run from c2_build: python -B meta_src/mappers/geonames.py"""
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mdlib as M  # noqa: E402

RAW = Path(__file__).resolve().parents[1] / "raw" / "geonames"
CONT = {"AF": "Africa", "AS": "Asia", "EU": "Europe", "NA": "North America", "SA": "South America", "OC": "Oceania"}

ctry = {}
for l in open(RAW / "countryInfo.txt", encoding="utf-8"):
    if l.startswith("#") or not l.strip():
        continue
    f = l.rstrip("\n").split("\t")
    ctry[f[0]] = {"name": f[4], "capital": f[5], "cont": f[8]}
adm1 = {}
for l in open(RAW / "admin1CodesASCII.txt", encoding="utf-8"):
    f = l.rstrip("\n").split("\t")
    adm1[f[0]] = f[2]
cities = []
for l in open(RAW / "cities15000.txt", encoding="utf-8"):
    f = l.rstrip("\n").split("\t")
    cc = f[8]
    if cc not in ctry or ctry[cc]["cont"] not in CONT:
        continue
    cities.append({"id": f[0], "name": f[1], "ascii": f[2], "code": f[7], "cc": cc, "a1": f[10], "pop": int(f[14] or 0),
                   "dem": int(f[16]) if f[16].lstrip("-").isdigit() else None, "tz": f[17], "cont": ctry[cc]["cont"],
                   "country": ctry[cc]["name"]})
cnt_cc = Counter((c["name"], c["cc"]) for c in cities)
cnt_glob = Counter(c["name"] for c in cities)
cities = [c for c in cities if cnt_cc[(c["name"], c["cc"])] == 1 and c["pop"] >= 15000]
POOL = [c for c in cities if c["pop"] >= 60000]
by_cont = defaultdict(list)
for c in POOL:
    by_cont[c["cont"]].append(c)

B = M.Block("md_geonames", "geography", "GeoNames cities15000 gazetteer", "download.geonames.org",
            "Creative Commons Attribution 4.0 (CC BY 4.0)", "https://www.geonames.org/export/",
            "export/dump/cities15000.zip", [RAW / "cities15000.txt", RAW / "countryInfo.txt", RAW / "admin1CodesASCII.txt"])

B.form("pop_gt", 1, ["Does {c} ({k}) have more than {T} inhabitants?", "Is the population of {c} ({k}) above {T}?",
                     "Do more than {T} people live in {c} ({k})?"])
B.form("pop_le", -1, ["Does {c} ({k}) have at most {T} inhabitants?", "Is the population of {c} ({k}) at most {T}?"])
B.form("capital", 1, ["Is {c} the capital of {k}?", "Is {c} the capital city of {k}?", "Does {k} have {c} as its capital?"])
B.form("not_capital", -1, ["Is it true that {c} is not the capital of {k}?",
                           "Is it correct that {c} is not the capital city of {k}?"])
B.form("elev_gt", 1, ["Is {c} ({k}) located above {T} m?", "Does {c} ({k}) lie higher than {T} m above sea level?"])
B.form("elev_le", -1, ["Is {c} ({k}) located at most {T} m above sea level?", "Is the elevation of {c} ({k}) at most {T} m?"])
B.form("member", 1, ["Is {c} eligible under this rule?", "Does {c} meet this rule?"])
B.form("tz", 0, ["Which time zone does {c} use?", "Which time zone is {c} in?"], qtype="choice")
B.form("country", 0, ["In which country is the city of {c}?", "Which country is {c} in?"], qtype="choice")
B.form("region", 0, ["In which first-level region ({kind}) of {k} is {c}?", "Which first-level region ({kind}) of {k} contains {c}?"], qtype="choice")

uses = Counter()


def avail(cap=2):
    return lambda e: uses[e["id"]] < cap


def ctx_state(c, key):
    if int(M.h(key, c["id"])[:4], 16) % 2:
        return f"City: {c['name']}\nCountry: {c['country']}", "record"
    return f"{c['name']} is a city in {c['country']}.", "sentence"


def num_task(task, qform, pool, n, field, above_form, minv=1, slice_name=""):
    B.task(task, qform, "yes/no", "none", slice_name or task.split(":")[-1])
    rng = M.R(task)
    ents = [c for c in pool if c[field] is not None and c[field] >= minv and uses[c["id"]] < 2]
    for c, T, yes in M.thr_first(ents, field, M.balanced(n, rng), rng, above_form):
        q, wid = B.say(qform, c["id"], c=c["name"], k=c["country"], T=M.fmt_int(T))
        st, fmt = ctx_state(c, task)
        if B.add(task, c["id"], st, q, int(yes), wording_id=wid, fmt=fmt):
            uses[c["id"]] += 1


for cont in CONT:
    num_task(f"geonames:pop_gt:{cont}", "pop_gt", by_cont[cont], 13, "pop", True)
    num_task(f"geonames:pop_le:{cont}", "pop_le", by_cont[cont], 13, "pop", False)
for cont in ("EU", "AS", "AF"):
    num_task(f"geonames:elev_gt:{cont}", "elev_gt", by_cont[cont], 13, "dem", True, minv=20)
for cont in ("NA", "SA", "OC"):
    num_task(f"geonames:elev_le:{cont}", "elev_le", by_cont[cont], 13, "dem", False, minv=20)

# ---- capitals: country-paired (one capital row and one non-capital row per country, so the country is gold-neutral)
for qform, conts in (("capital", [["EU"], ["AS"], ["AF"], ["NA"], ["SA", "OC"]]), ("not_capital", [["EU"], ["AS", "OC"], ["AF", "NA", "SA"]])):
    for cs in conts:
        task = f"geonames:{qform}:{'+'.join(cs)}"
        B.task(task, qform, "yes/no", "none", "+".join(cs))
        rng = M.R(task)
        cl = [k for k, v in ctry.items() if v["cont"] in cs]
        rng.shuffle(cl)
        rows = 0
        for k in cl:
            caps = [c for c in cities if c["cc"] == k and c["code"] == "PPLC"]
            non = [c for c in POOL if c["cc"] == k and c["code"] != "PPLC" and uses[c["id"]] < 2]
            if not caps or not non:
                continue
            cap = max(caps, key=lambda c: c["pop"])
            nc = rng.choice(non)
            for c in (cap, nc):
                gold = int(c is cap) if qform == "capital" else int(c is not cap)
                q, wid = B.say(qform, c["id"], c=c["name"], k=c["country"])
                if B.add(task, c["id"], f"City: {c['name']}\nCountry: {c['country']}" if rng.random() < .5 else f"{c['name']}, {c['country']}",
                         q, gold, wording_id=wid, edge=["capital_pair"]):
                    rows += 1
                    uses[c["id"]] += 1
            if rows >= 16:
                break

# ---- choice (options-first: every option is gold 1/k of the times it appears)
def choice_task(task, qform, pool, n, val, label, state_fn, qargs, slice_name, errname, kmax=4):
    B.task(task, qform, "choice", "none", slice_name)
    rng = M.R(task)
    ebv = defaultdict(list)
    for e in pool:
        if val(e) is not None:
            ebv[val(e)].append(e)
    counter = Counter({v: len(x) for v, x in ebv.items()})
    k = min(kmax, len(counter))
    for e, g, S in M.options_first(counter, ebv, n, k, rng, avail()):
        q, wid = B.say(qform, e["id"], c=e["name"], **qargs(e))
        if B.add(task, e["id"], state_fn(e), q, label(g), options=[label(o) for o in S], wording_id=wid,
                 opt_err={label(o): errname for o in S if o != g}):
            uses[e["id"]] += 1


tzf = defaultdict(Counter)
for c in POOL:
    tzf[c["cc"]][c["tz"]] += 1
multi = sorted([k for k in ctry if len(tzf[k]) >= 3], key=lambda k: -sum(tzf[k].values()))[:6]
ident = lambda x: x
for cont in CONT:
    choice_task(f"geonames:tz:{cont}", "tz", by_cont[cont], 13, lambda e: e["tz"], ident,
                lambda e: f"City: {e['name']}\nCountry: {e['country']}", lambda e: {}, cont, "tz_same_continent")
for grp in (["EU"], ["AS"], ["AF"], ["NA"], ["SA", "OC"]):
    choice_task(f"geonames:country:{'+'.join(grp)}", "country", [c for c in POOL if c["cont"] in grp and cnt_glob[c["name"]] == 1], 13,
                lambda e: e["country"], ident, lambda e: f"City: {e['name']}", lambda e: {}, "+".join(grp), "country_same_continent")
for k in multi:
    choice_task(f"geonames:tz:cc_{k}", "tz", [c for c in POOL if c["cc"] == k], 13, lambda e: e["tz"], ident,
                lambda e: f"City: {e['name']}\nCountry: {e['country']}", lambda e: {}, ctry[k]["name"], "tz_same_country")
KIND = {"US": "state", "CN": "province", "IN": "state", "BR": "state", "RU": "federal subject", "FR": "region", "DE": "state",
        "JP": "prefecture", "GB": "country of the UK", "IT": "region", "ES": "autonomous community", "MX": "state"}
for k, kind in KIND.items():
    pl = [c for c in POOL if c["cc"] == k and f"{k}.{c['a1']}" in adm1]
    choice_task(f"geonames:region:{k}", "region", pl, 13, lambda e, k=k: adm1.get(f"{k}.{e['a1']}"), ident,
                lambda e: f"City: {e['name']}\nCountry: {e['country']}", lambda e, k=k, kind=kind: {"k": e["country"], "kind": kind},
                ctry[k]["name"], "region_same_country")

# ---- card tasks: membership rules (neutral by construction: the value is drawn first, the coin only decides membership)
def lst(S):
    S = list(S)
    return ", ".join(S[:-1]) + " or " + S[-1]


cfreq = Counter(c["country"] for c in cities)
tzfreq = Counter(c["tz"] for c in cities)
codefreq = Counter({"PPLC": 1, "PPLA": 1, "PPLA2": 1, "PPLA3": 1, "PPL": 1})
for cont in CONT:
    task = f"geonames:member_country:{cont}"
    B.task(task, "member", "yes/no", "rules_in_card", cont)
    M.member_yn(B, task, "member", [c for c in cities if c["cont"] == cont], lambda e: e["country"], None, 22, 3, M.R(task), cfreq,
                lambda e: f"Place: {e['name']}\nCountry: {e['country']}", lambda e: {"c": e["name"]},
                lambda S: f"- yes: The place's country is {lst(S)}.\n- no: The place's country is any other country.", uses, 6)
for grp in (["EU"], ["AS"], ["AF", "NA", "SA", "OC"]):
    task = f"geonames:member_tz:{'+'.join(grp)}"
    B.task(task, "member", "yes/no", "rules_in_card", "+".join(grp))
    ents = [c for c in cities if c["cont"] in grp]
    cnt = Counter(c["tz"] for c in ents if tzfreq[c["tz"]] >= 3)
    M.member_yn(B, task, "member", [c for c in ents if c["tz"] in cnt], lambda e: e["tz"], None, 22, 3, M.R(task), cnt,
                lambda e: f"Place: {e['name']}\nCountry: {e['country']}\nTime zone (record): {e['tz']}", lambda e: {"c": e["name"]},
                lambda S: f"- yes: The place's time zone is {lst(S)}.\n- no: The place's time zone is any other.", uses, 6)
for i, kset in enumerate((2, 3)):
    task = f"geonames:member_code:k{kset}"
    B.task(task, "member", "yes/no", "rules_in_card", f"k{kset}")
    ents = []
    for code in codefreq:
        ents += [c for c in cities if c["code"] == code][:400]
    M.member_yn(B, task, "member", ents, lambda e: e["code"], None, 22, kset, M.R(task), codefreq,
                lambda e: f"Place: {e['name']}\nCountry: {e['country']}\nFeature code (record): {e['code']}", lambda e: {"c": e["name"]},
                lambda S: f"- yes: The place's feature code is {lst(S)}.\n- no: The place's feature code is any other code.", uses, 6)

B.form("group", 0, ["Which group does the country of {c} belong to under these definitions?", "Under the definitions, which group holds the country where {c} lies?"], qtype="choice")
LAB = ["Group A", "Group B", "Group C"]
for grp in (["EU"], ["AS"], ["AF"], ["NA", "SA", "OC"]):
    task = f"geonames:group:{'+'.join(grp)}"
    B.task(task, "group", "choice", "rules_in_card", "+".join(grp))
    rng = M.R(task)
    ents = [c for c in cities if c["cont"] in grp and uses[c["id"]] < 6]
    rng.shuffle(ents)
    cls = M.positions(22, 4, rng)          # gold class: 0-2 = group A-C, 3 = none
    pos = M.positions(22, 4, rng)
    got = 0
    for e in ents:
        if got == 22:
            break
        c, v = cls[got], e["country"]
        pool = Counter({a: w for a, w in cfreq.items() if a != v})
        others = M.draw_set(pool, 9, rng)
        sets = [others[0:3], others[3:6], others[6:9]]
        if c < 3:
            sets[c][rng.randrange(3)] = v
        card = "\n".join([f"- {LAB[j]}: {lst(sets[j])}" for j in range(3)] + ["- None of these groups: any other country"])
        gold = LAB[c] if c < 3 else "None of these groups"
        order = [x for x in LAB + ["None of these groups"] if x != gold]
        rng.shuffle(order)
        opts = order[:]
        opts.insert(pos[got], gold)
        q, wid = B.say("group", e["id"], c=e["name"])
        if B.add(task, e["id"], f"Place: {e['name']}\nCountry: {e['country']}", q, gold, options=opts, card=card, wording_id=wid, depth=1,
                 opt_err={o: "wrong_group" for o in order}):
            uses[e["id"]] += 1
            got += 1

if __name__ == "__main__":
    import json
    qc = B.finalize()
    print(json.dumps({k: qc[k] for k in ("rows", "tasks", "rows_per_task", "yes_no_share", "yes_share_in_yes_no", "card_free_share",
                                         "problems", "per_task_yes_dev_max", "max_near_dup_jaccard_in_task", "partial_input")}, default=str))
