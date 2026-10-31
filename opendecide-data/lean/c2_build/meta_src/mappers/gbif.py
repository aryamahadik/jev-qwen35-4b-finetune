"""md_gbif mapper (A42-D 8): GBIF Backbone Taxonomy (CC BY 4.0). Gold = program function of the record fields kingdom, phylum,
class, order, family, rank, extinct, habitats. Taxon names are inputs only. Run from c2_build: python -B meta_src/mappers/gbif.py"""
import json, sys
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import mdlib as M  # noqa: E402

RAW = Path(__file__).resolve().parents[1] / "raw" / "gbif"
T = []
seen = set()
for l in open(RAW / "taxa.jsonl", encoding="utf-8"):
    t = json.loads(l)
    if t["taxonomicStatus"] != "ACCEPTED" or not t.get("canonicalName") or t["key"] in seen or t["nameType"] != "SCIENTIFIC":
        continue
    seen.add(t["key"])
    t["id"] = str(t["key"])
    t["name"] = t["canonicalName"]
    T.append(t)
nm = Counter(t["name"] for t in T)
T = [t for t in T if nm[t["name"]] == 1]
SP = [t for t in T if t["rank"] == "SPECIES"]
KS = ["Animalia", "Plantae", "Fungi"]
B = M.Block("md_gbif", "biodiversity", "GBIF Backbone Taxonomy", "api.gbif.org", "Creative Commons Attribution 4.0 (CC BY 4.0)",
            "http://creativecommons.org/licenses/by/4.0/legalcode", "dataset d7dddbf4-2cf0-4f39-9b2a-bb099caae36c", [RAW / "taxa.jsonl"])
for lv in ("phylum", "class", "order", "family"):
    B.form(lv, 0, [f"To which {lv} does the taxon {{n}} belong?", f"Which {lv} is the taxon {{n}} placed in?"], qtype="choice")
B.form("kingdom", 0, ["To which kingdom does the taxon {n} belong?", "Which kingdom is the taxon {n} placed in?"], qtype="choice")
B.form("rank", 0, ["At which taxonomic rank is the name {n}?", "Which rank does the name {n} have?"], qtype="choice")
for lv in ("family", "order", "class"):
    B.form(f"same_{lv}", 1, [f"Do {{a}} and {{b}} belong to the same {lv}?", f"Are {{a}} and {{b}} placed in the same {lv}?"])
    B.form(f"diff_{lv}", -1, [f"Do {{a}} and {{b}} belong to different {lv.replace('class','classes').replace('family','families').replace('order','orders')}?",
                              f"Are {{a}} and {{b}} placed in different {lv.replace('class','classes').replace('family','families').replace('order','orders')}?"])
B.form("marine", 1, ["Is {n} a marine taxon?", "Does {n} live in the sea?"])
B.form("terrestrial", 1, ["Is {n} a terrestrial taxon?", "Does {n} live on land?"])
B.form("extinct", 1, ["Is the taxon {n} extinct?", "Has the taxon {n} died out?"])
B.form("member", 1, ["Is {n} eligible under the rule?", "Does {n} meet the rule?"])
B.form("group", 0, ["Which group does {n} fall into under the definitions?", "Under the definitions, which group holds {n}?"], qtype="choice")
uses = Counter()
ident = lambda x: x
N = 22
lst = M.lst


def st(t, *levels):
    return "Taxon: " + t["name"] + "".join(f"\n{lv.capitalize()}: {t[lv]}" for lv in levels)


# --- choice: classification
for rk in ("SPECIES", "GENUS", "FAMILY"):
    pool = [t for t in T if t["rank"] == rk and t.get("kingdom")]
    B.choice_task(f"gbif:kingdom:{rk}", "kingdom", pool, N, lambda t: t["kingdom"], ident, lambda t: f"Taxon: {t['name']}",
                  lambda t: {"n": t["name"]}, rk, "other_kingdom", uses, wpow=0.0)
    B.choice_task(f"gbif:rank:{rk}", "rank", [t for t in T if t["rank"] in ("SPECIES", "GENUS", "FAMILY")], N, lambda t: t["rank"].lower(), ident,
                  lambda t: f"Name: {t['name']}", lambda t: {"n": t["name"]}, rk, "other_rank", uses, wpow=0.0) if rk == "SPECIES" else None
for k in KS:
    for rk in ("SPECIES", "FAMILY"):
        pool = [t for t in T if t["kingdom"] == k and t["rank"] == rk]
        for lv, ctx in (("phylum", ()), ("class", ("phylum",))):
            if rk == "FAMILY" and lv == "class" and k == "Fungi":
                continue
            B.choice_task(f"gbif:{lv}:{k}:{rk}", lv, [t for t in pool if t.get(lv)], N, lambda t, lv=lv: t.get(lv), ident,
                          lambda t, ctx=ctx: st(t, "kingdom", *ctx), lambda t: {"n": t["name"]}, f"{k}/{rk}", f"other_{lv}_same_kingdom", uses, wpow=0.5)
    pool = [t for t in SP if t["kingdom"] == k]
    B.choice_task(f"gbif:order:{k}", "order", [t for t in pool if t.get("order")], N, lambda t: t.get("order"), ident,
                  lambda t: st(t, "kingdom", "class"), lambda t: {"n": t["name"]}, k, "other_order", uses, wpow=0.5)
    B.choice_task(f"gbif:family:{k}", "family", [t for t in pool if t.get("family")], N, lambda t: t.get("family"), ident,
                  lambda t: st(t, "kingdom", "order"), lambda t: {"n": t["name"]}, k, "other_family", uses, wpow=0.5)

# --- same / different level (form is a coin; pairs: yes = same group, no = a hard neighbour in the next level up)
UP = {"family": "order", "order": "class", "class": "phylum"}
for k in KS:
    for lv in ("family", "order", "class"):
        task = f"gbif:pair_{lv}:{k}"
        B.task(task, f"same_{lv}", "yes/no", "none", f"{k}/{lv}")
        rng = M.R(task)
        pool = [t for t in SP if t["kingdom"] == k and t.get(lv) and t.get(UP[lv])]
        grp = defaultdict(list)
        for t in pool:
            grp[t[lv]].append(t)
        parent = defaultdict(set)
        for g, ts in grp.items():
            parent[ts[0][UP[lv]]].add(g)
        multi = [g for g, ts in grp.items() if len(ts) >= 2]
        negg = [x for x in grp if len(parent[grp[x][0][UP[lv]]]) >= 2]
        if not multi or not negg:
            continue
        got = 0
        for gold in M.balanced(N, rng):
            f = ("same_" if rng.random() < 0.5 else "diff_") + lv
            yes = bool(gold) if f.startswith("same") else (not gold)     # 'same group' pair?
            for _ in range(60):
                g = rng.choice(multi) if yes else rng.choice(negg)
                a = rng.choice(grp[g])
                if yes:
                    cand = [t for t in grp[g] if t["id"] != a["id"] and t["genus"] != a["genus"]] or [t for t in grp[g] if t["id"] != a["id"]]
                else:
                    sib = [x for x in parent[a[UP[lv]]] if x != g]
                    cand = [t for x in sib for t in grp[x]]
                if not cand or uses[a["id"]] >= 2:
                    continue
                b = rng.choice(cand)
                if uses[b["id"]] >= 2:
                    continue
                pair = sorted([a["id"], b["id"]])
                x, y = (a, b) if rng.random() < .5 else (b, a)
                gold = int(gold)
                q, wid = B.say(f, "|".join(pair), a=x["name"], b=y["name"])
                if B.add(task, "|".join(pair), f"Taxa: {x['name']}; {y['name']}", q, gold, wording_id=wid, qform=f):
                    uses[a["id"]] += 1; uses[b["id"]] += 1
                    got += 1
                    break

# --- habitat (form is a coin) and extinct
for i in range(2):
    task = f"gbif:habitat:{i}"
    B.task(task, "marine", "yes/no", "none", str(i))
    rng = M.R(task)
    pool = [t for t in SP if t.get("habitats") and len(t["habitats"]) == 1 and uses[t["id"]] < 2]
    rng.shuffle(pool)
    for yes in M.balanced(N, rng):
        f = rng.choice(["marine", "terrestrial"])
        want = f.upper() if f == "marine" else "TERRESTRIAL"
        for t in pool:
            if uses[t["id"]] < 2 and (task, t["id"]) not in B.used and ((t["habitats"][0] == want) == yes):
                q, wid = B.say(f, t["id"], n=t["name"])
                if B.add(task, t["id"], f"Taxon: {t['name']}\nKingdom: {t['kingdom']}", q, int(yes), wording_id=wid, qform=f):
                    uses[t["id"]] += 1
                    break
for i, pool0 in enumerate((SP, T)):
    task = f"gbif:extinct:{i}"
    B.task(task, "extinct", "yes/no", "none", str(i))
    rng = M.R(task)
    pos = [t for t in pool0 if t.get("extinct") is True and uses[t["id"]] < 2]
    neg = [t for t in pool0 if t.get("extinct") is False and uses[t["id"]] < 2]
    rng.shuffle(pos); rng.shuffle(neg)
    for yes in M.balanced(min(N, 2 * min(len(pos), len(neg))), rng):
        t = (pos if yes else neg).pop()
        q, wid = B.say("extinct", t["id"], n=t["name"])
        if B.add(task, t["id"], f"Taxon: {t['name']}\nKingdom: {t['kingdom']}", q, int(yes), wording_id=wid):
            uses[t["id"]] += 1

# --- card tasks (membership; value drawn first)
clc = Counter(t["class"] for t in SP if t.get("class"))
kgc = Counter(t["kingdom"] for t in T)
for k in KS + ["Chromista"]:
    pool = [t for t in SP if t["kingdom"] == k and t.get("class")]
    cc = Counter({c: n for c, n in Counter(t["class"] for t in pool).items() if n >= 3})
    pool = [t for t in pool if t["class"] in cc]
    task = f"gbif:member_class:{k}"
    B.task(task, "member", "yes/no", "rules_in_card", k)
    M.member_yn(B, task, "member", pool, lambda t: t["class"], None, N, 3, M.R(task), cc, lambda t: st(t, "kingdom", "class"),
                lambda t: {"n": t["name"]}, lambda S: f"- yes: The taxon's class is {lst(S)}.\n- no: The taxon's class is any other class.", uses, 6, uniform=True)
    if k != "Fungi":
        M.group_choice(B, f"gbif:group_class:{k}", "group", pool, lambda t: t["class"], cc, N, lambda t: st(t, "kingdom", "class"),
                       lambda t: {"n": t["name"]}, uses, "the class is", k, 6, uniform=True)
for rk in ("SPECIES", "GENUS"):
    pool = [t for t in T if t["rank"] == rk and t.get("kingdom")]
    task = f"gbif:member_kingdom:{rk}"
    B.task(task, "member", "yes/no", "rules_in_card", rk)
    M.member_yn(B, task, "member", pool, lambda t: t["kingdom"], None, N, 2, M.R(task), Counter({k: 1 for k in kgc}),
                lambda t: f"Taxon: {t['name']}\nKingdom: {t['kingdom']}\nRank: {t['rank'].lower()}", lambda t: {"n": t["name"]},
                lambda S: f"- yes: The taxon's kingdom is {lst(S)}.\n- no: The taxon's kingdom is any other kingdom.", uses, 6, uniform=True)

if __name__ == "__main__":
    qc = B.finalize()
    print(json.dumps({k: qc[k] for k in ("rows", "tasks", "rows_per_task", "yes_no_share", "yes_share_in_yes_no", "card_free_share", "dropped_short_tasks",
                                         "problems", "per_task_yes_dev_max", "max_near_dup_jaccard_in_task", "partial_input")}, default=str))
