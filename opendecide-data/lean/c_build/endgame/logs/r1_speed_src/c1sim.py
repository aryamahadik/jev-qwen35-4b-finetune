from sim import *
t0 = time.time(); rng = random.Random(11)
rows = read_jsonl(LEAN + "/data/v14_parts/golden_train.jsonl")
got = draw(by_call(rows), 16000, rng); rs = [r for u in got for r in u]; del rows
L = lengths(rs); v = sorted(L.values())
print("C1 drawn", len(rs), "tok mean", round(st.mean(v)), "med", v[len(v)//2], "choice", round(sum(r['qtype']=='choice' for r in rs)/len(rs),2), round(time.time()-t0), flush=True)
for mt in (8192, 10240):
    f = []
    for seed in (1, 2, 3): f += simulate(got, L, 600, seed, budget=mt)
    print("C1 mt", mt, summ(f), flush=True)
json.dump({"lens": L}, open("c1_lens.json", "w"))
