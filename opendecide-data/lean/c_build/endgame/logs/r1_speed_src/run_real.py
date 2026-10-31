from sim import *
t0 = time.time(); rng = random.Random(7); SCALE = float(sys.argv[1]) if len(sys.argv) > 1 else 0.125
allu, lens, stats = [], {}, {}
for b, q in QUOTA.items():
    rows = pool(b); units = by_call(rows)
    got = draw(units, int(q * SCALE), rng); rs = [r for u in got for r in u]
    L = lengths(rs); lens.update(L); v = sorted(L.values())
    stats[b] = {"pool_rows": len(rows), "drawn": len(rs), "tok_mean": round(st.mean(v)), "tok_med": v[len(v)//2],
                "tok_p90": v[int(.9*len(v))], "choice": round(sum(r["qtype"] == "choice" for r in rs)/len(rs), 2),
                "rows_per_unit": round(len(rs)/len(got), 2)}
    allu += got
    print(b, stats[b], round(time.time()-t0), flush=True)
json.dump({"lens": lens, "stats": stats}, open(f"real_lens_{SCALE}.json", "w"))
tot = sum(QUOTA.values()); rows = [r for u in allu for r in u]
print("rows", len(rows), "token-weighted mean/row", round(sum(lens[r["id"]] for r in rows)/len(rows)))
for seed in (1, 2, 3):
    f = simulate(allu, lens, 600, seed); print("seed", seed, summ(f), flush=True)
print("sec", round(time.time()-t0))
