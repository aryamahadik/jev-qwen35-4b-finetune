"""T28 i1 diagnostic: G6 on the cached 5k build, whole and by question form."""
import pickle, sys, json
sys.dont_write_bytecode = True
sys.path.insert(0, ".")
import pilot
infos, stats = pickle.load(open(sys.argv[1], "rb"))
ch = [i for i in infos if i.row["qtype"] == "choice"]
yn = [i for i in infos if i.row["qtype"] == "noul"]
print("rows", len(infos), "choice", len(ch), "yn", len(yn))
def show(name, r):
    keys = [k for k in r if k.startswith(("a_", "b_", "c_", "d_"))]
    ex = {k: (r[k]["lr"] - r["chance"], r[k]["gbt"] - r["chance"]) for k in keys}
    print(name, "n", r["n"], "chance", r["chance"], {k: "lr %+.3f gbt %+.3f" % v for k, v in ex.items()})
show("choice ALL", pilot.g6_choice(ch))
for q in ("ch_verdict", "ch_rule", "ch_inverted"):
    sub = [i for i in ch if i.row["meta"]["qform"] == q]
    if len(sub) >= 40:
        show(q, pilot.g6_choice(sub))
r = pilot.g6_yes_no(yn)
print("yn", {k: v for k, v in r.items() if k in ("a_question", "c_card_without_question", "d_meta")})
