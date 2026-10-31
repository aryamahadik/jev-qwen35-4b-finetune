"""W4 diagnostic: build only head <H> choice rows in memory, G6 choice for them, top LR features of c_card. usage: diag_lr.py B 3000"""
import sys, collections
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[3]; sys.path.insert(0, str(C2))
import numpy as np
import pilot, pilot_loaders as PL
from families.T40 import loader, plugin as TP
H, N = sys.argv[1], int(sys.argv[2])
loader.register()
with PL.open_family("T40") as kit:
    pl = kit.plugin; orig = pl.sample
    def samp(seed, sampler):
        c = TP.design(seed, sampler)
        if not (c["head"] == H and c["kind"] == "ch"): raise ValueError("skip")
        return orig(seed, sampler)
    pl.sample = samp
    b = pilot.build_pilot(kit, N, run_g15=False, max_attempts=40 * N)
    infos = b.infos
    print("rows", len(infos), collections.Counter(pl.label(i.spec) for i in infos))
    r = pilot.g6_choice(infos); print({v: r[v] for v in r if isinstance(r[v], dict)}, r["chance"])
    from sklearn.feature_extraction.text import CountVectorizer
    T, D, Y, Rw = pilot._pair_rows(infos, "c_card_without_question")
    cv = CountVectorizer(analyzer=lambda x: x, min_df=5, binary=True); X = cv.fit_transform(T); Y = np.array(Y)
    lr = pilot._lr().fit(X, Y); co = lr.coef_[0]; names = np.array(cv.get_feature_names_out())
    df = np.asarray(X.sum(0)).ravel()
    sc = co * np.sqrt(df)
    for j in np.argsort(-np.abs(sc))[:25]: print(round(float(co[j]), 3), int(df[j]), names[j])
