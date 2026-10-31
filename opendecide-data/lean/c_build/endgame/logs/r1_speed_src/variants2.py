from sim import *
rng = random.Random(7); SCALE = 0.125
J = json.load(open("real_lens_0.125.json")); lens = J["lens"]
allu = []
for b, q in QUOTA.items():
    allu += draw(by_call(pool(b)), int(q * SCALE), rng)
rows = [r for u in allu for r in u]; assert all(r["id"] in lens for r in rows), "draw changed"
print("rows", len(rows), "rows/step check below")
for pad in (256, 64):
    decoder_io.PAD_MULTIPLE = pad
    for mt in (4096, 6144):
        f = []
        for seed in (1, 2, 3): f += simulate(allu, lens, 600, seed, budget=mt)
        s = summ(f); print(f"pad {pad:3d} mt {mt:5d} pad_tok {s['pad_tok']:8.0f} real {s['real_tok']:7.0f} n_micro {s['n_micro']:4.1f} rows {s['rows']}", flush=True)
