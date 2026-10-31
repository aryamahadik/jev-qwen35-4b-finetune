import json, numpy as np
p = json.load(open("presmoke_steps.json"))[5:39]; c = json.load(open("c1_steps.json"))
ct = c[10:99]
for k in ["rows","twins","n_seq","n_micro","pad_tok","real_tok","max_len","anc_pad_tok"]:
    a = np.mean([o[k] for o in p]); b = np.mean([o[k] for o in ct]); print(f"{k:11s} presmoke {a:9.1f}  C1-replay {b:9.1f}  ratio {a/b if b else float('nan'):.2f}")
tp = np.array([o["t"] for o in p]); tc = np.array([o["t"] for o in ct])
print("measured mean s/step presmoke", tp.mean().round(3), " C1 pilot", tc.mean().round(3), " ratio", (tp.mean()/tc.mean()).round(2))
print("real tokens/sequence presmoke", round(np.sum([o['real_tok'] for o in p])/np.sum([o['n_seq'] for o in p])), " C1", round(np.sum([o['real_tok'] for o in ct])/np.sum([o['n_seq'] for o in ct])))
