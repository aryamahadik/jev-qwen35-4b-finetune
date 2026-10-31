import json, numpy as np
s = json.load(open("presmoke_steps.json"))
T = s[5:39]  # the 34 timed steps
t = np.array([o["t"] for o in T])
for k in ["rows","twins","n_seq","n_micro","pad_tok","real_tok","attn","max_len"]:
    x = np.array([o[k] for o in T], float); print(f"{k:9s} mean {x.mean():9.1f}  r={np.corrcoef(x,t)[0,1]:+.2f}")
def fit(cols):
    X = np.column_stack([np.array([o[c] for o in T], float) for c in cols] + [np.ones(len(T))])
    b, *_ = np.linalg.lstsq(X, t, rcond=None); r = t - X @ b
    print(cols, "coef", np.round(b, 6).tolist(), "R2", round(1 - r.var()/t.var(), 3), "rmse", round(r.std(), 3))
    return b
fit(["pad_tok"]); fit(["real_tok"]); fit(["pad_tok","n_micro"]); fit(["n_micro"]); fit(["pad_tok","attn"])
print("mean t", t.mean().round(3), "median", np.median(t).round(3))
