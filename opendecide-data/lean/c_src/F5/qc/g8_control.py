"""G8 controls (report-only, independent F5 checker): rerun the gated grouped-by-card AFLite-lite on the cached MiniLM
embeddings with (a) labels permuted globally and (b) labels shuffled within card, 2 seeds each, to show how much of the
grouped predictable share is reached by label-free prediction stability. Writes qc/g8_control_<name>.json."""
import json, sys
import numpy as np
import qc_lib as L
sys.argv += [] if len(sys.argv) > 1 else ["candidates_r1"]
import g8
NAME = sys.argv[1]
rows = L.load(NAME); X = np.load(L.TMP / f"g8/emb_{NAME}.npy")
y = np.array([int(r["gold"]) for r in rows]); cards = [r["meta"]["card_id"] for r in rows]
out = {"set": NAME, "note": "report-only controls for the gated grouped run; gate verdict unchanged"}
for s in (0, 1):
    rng = np.random.default_rng(100 + s)
    out[f"grouped_global_permute_s{s}"] = g8.aflite(X, rng.permutation(y), cards, "grouped"); g8.log(out[f"grouped_global_permute_s{s}"])
    yn = y.copy()
    for c in set(cards):
        ix = np.array([i for i, cc in enumerate(cards) if cc == c]); yn[ix] = rng.permutation(y[ix])
    out[f"grouped_within_card_shuffle_s{s}"] = g8.aflite(X, yn, cards, "grouped"); g8.log(out[f"grouped_within_card_shuffle_s{s}"])
json.dump(out, open(L.QC / f"g8_control_{NAME}.json", "w"), indent=1); g8.log("done")
