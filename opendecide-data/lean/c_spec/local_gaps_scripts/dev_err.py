"""C1 (q35_4b_main500k) vs 4B-E (q35_4b_pxE_fresh) error breakdown on the 9 dev gate splits (dev only, read-only)."""
import glob, json, sys
import numpy as np
import pandas as pd

LEAN = "/Users/aryamahadik/Documents/jev/opendecide-data/lean"
SP = "/private/tmp/claude-501/-Users-aryamahadik-Documents-jev/73bb87c6-8519-454d-98bb-7961fcde73b9/scratchpad"
sys.path.insert(0, LEAN)
import gate_dev as G  # read-only import

C, R = "q35_4b_main500k", "q35_4b_pxE_fresh"
splits = G.SPLITS.split(",")
rows = G.complete_rows(splits, C, R)
gr = pd.DataFrame(rows)
feats = []
for sp in splits:
    for l in open(f"{SP}/feat_dev_{sp}_0.jsonl"):
        f = json.loads(l); f["split"] = sp; feats.append(f)
ft = pd.DataFrame(feats)
df = gr.merge(ft.drop(columns=["source", "qtype", "group_id"]), on=["split", "id"], how="left", validate="1:1")
assert len(df) == len(gr) == 8143 and df.state_chars.notna().all()

golden = pd.read_pickle(f"{SP}/golden.pkl")
gsrc = set(golden.source.unique())
df["unseen_frozen"] = df.source.isin(G.UNSEEN_FROZEN_ROWS).astype(int)
df["c1_seen_name"] = df.source.map(lambda s: int(bool(G.source_seen(s, gsrc))))

FAM = {"clinc150": "intent (clinc/banking)", "banking77": "intent (clinc/banking)",
       "ag_news": "topic news", "bbc": "topic news", "btzsc_capsotu": "political topic (capsotu/manifesto)",
       "btzsc_manifesto": "political topic (capsotu/manifesto)",
       "rotten_tomatoes": "sentiment", "btzsc_appreviews": "sentiment", "btzsc_financialphrasebank": "sentiment",
       "emotion": "emotion", "btzsc_empathetic": "emotion", "irony": "irony/sarcasm",
       "hate": "hate/offensive", "btzsc_biasframes_offensive": "hate/offensive",
       "btzsc_biasframes_intent": "hate/offensive", "btzsc_biasframes_sex": "hate/offensive",
       "spam": "spam", "climate": "climate risk/opportunity (stance-like)", "cb": "NLI (cb)",
       "btzsc_trueteacher": "factual consistency (trueteacher)",
       "tb_mixtral": "synthetic zero-shot tasks (tb)", "tb_label_nli": "synthetic zero-shot tasks (tb)"}
df["fam"] = df.source.map(lambda s: FAM.get(s, "hard_* expert-written" if s.startswith("hard_") else
                                            ("pg_* policy generators" if s.startswith("pg_") else s)))
df["yn"] = (df.qtype == "noul").astype(int)
df["negq"] = (df.neg_syn + df.neg_lex).clip(0, 2)
tb = [0, 256, 512, 1024, 2048, 1e9]
df["tokbin"] = pd.cut(df.prompt_tok, tb, labels=["<256", "256-512", "512-1K", "1-2K", ">2K"])
df["optbin"] = pd.cut(df.n_opt, [0, 2, 3, 5, 9, 20, 1000], labels=["2", "3", "4-5", "6-9", "10-20", "21+"])


def pyes(p):
    return float(p.get("yes", 0.0)) if p else np.nan


df["pyes_c"] = [pyes(p) if q == "noul" else np.nan for p, q in zip(df.p_c, df.qtype)]
df["pyes_r"] = [pyes(p) if q == "noul" else np.nan for p, q in zip(df.p_r, df.qtype)]
df["pmax_c"] = [max(p.values()) if p else np.nan for p in df.p_c]


def pred(p, opts, q):
    if q == "noul":
        return "yes" if float(p.get("yes", 0)) > 0.5 else "no"
    v = {o: float(p.get(o, 0.0)) for o in opts}
    return max(v, key=v.get)


df["pred_c"] = [pred(p, o, q) for p, o, q in zip(df.p_c, df.options, df.qtype)]
df["pred_r"] = [pred(p, o, q) for p, o, q in zip(df.p_r, df.options, df.qtype)]
df.to_pickle(f"{SP}/dev.pkl")


def tab(col, sub=None, boots=2000, minn=1):
    d = df if sub is None else df[sub]
    out = []
    for k, g in d.groupby(col, observed=True):
        if len(g) < minn:
            continue
        b = G.group_boot(g[["group_id", "ok_c", "ok_r"]].to_dict("records"), boots=boots)
        out.append({col: k, "n": len(g), "C1": round(b["cand"], 1), "4B-E": round(b["ref"], 1), "diff": round(b["diff"], 1),
                    "CI": f"[{b['lo']:+.1f}, {b['hi']:+.1f}]", "C1_err": int(len(g) - g.ok_c.sum()),
                    "err_share%": round(100 * (len(g) - g.ok_c.sum()) / (len(d) - d.ok_c.sum()), 1)})
    return pd.DataFrame(out)


pd.set_option("display.width", 250)
pd.set_option("display.max_rows", 200)
res = {}
print("ALL", G.point(rows))
for name, col, sub in [("split", "split", None), ("family", "fam", None), ("qtype_role", None, None),
                       ("ynform", "ynform", df.yn == 1), ("yn_gold", "yn_gold", df.yn == 1),
                       ("neg_yn", "negq", df.yn == 1), ("neg_choice", "negq", df.yn == 0),
                       ("optbin_choice", "optbin", df.yn == 0), ("tokbin", "tokbin", None),
                       ("has_card", "has_card", None), ("renamed_choice", "renamed", df.yn == 0),
                       ("nei_opt_choice", "has_nei_opt", df.yn == 0), ("gold_nei_choice", "gold_nei", df.yn == 0),
                       ("gold_noneof_choice", "gold_noneof", df.yn == 0), ("noneof_opt_choice", "has_noneof_opt", df.yn == 0),
                       ("ordinal_choice", "ordinal", df.yn == 0), ("unseen_frozen", "unseen_frozen", None),
                       ("c1_seen_name", "c1_seen_name", None), ("fmt", "fmt", None),
                       ("source", "source", None)]:
    if name == "qtype_role":
        df["qr"] = df.qtype + ":" + df.role
        t = tab("qr")
    else:
        t = tab(col, sub)
    res[name] = t
    print(f"\n== {name}")
    print(t.sort_values("C1").to_string(index=False))
# cross: role x unseen, neg x unseen, family x qtype
for nm, cols in [("role_x_unseen", ["role", "unseen_frozen"]), ("fam_x_qtype", ["fam", "qtype"]),
                 ("neg_x_unseen_yn", ["negq", "unseen_frozen"])]:
    d = df if nm != "neg_x_unseen_yn" else df[df.yn == 1]
    g = d.groupby(cols, observed=True).agg(n=("ok_c", "size"), C1=("ok_c", "mean"), E=("ok_r", "mean"))
    g["C1"] = (100 * g.C1).round(1); g["E"] = (100 * g.E).round(1); g["diff"] = (g.C1 - g.E).round(1)
    print(f"\n== {nm}"); print(g.to_string())
yn = df[df.yn == 1]
for who in ["c", "r"]:
    p = yn[f"pyes_{who}"]; gold = yn.yn_gold
    fy = ((p > 0.5) & (gold == 0)).sum(); fn = ((p <= 0.5) & (gold == 1)).sum()
    print(f"\n{who}: yes/no errors: false-yes {fy}, false-no {fn}; mean P(yes) {p.mean():.3f}; gold-yes share {gold.mean():.3f};"
          f" pred-yes share {(p > 0.5).mean():.3f}; Brier {((p - gold) ** 2).mean():.4f}")
# overconfidence of C1 errors
err = df[df.ok_c == 0]
print("\nC1 errors:", len(err), "share with max prob > 0.9:", round((err.pmax_c > 0.9).mean(), 3),
      "> 0.99:", round((err.pmax_c > 0.99).mean(), 3))
ok = df[df.ok_c == 1]
print("C1 correct share with max prob > 0.9:", round((ok.pmax_c > 0.9).mean(), 3))
# choice error kinds
ch = df[df.yn == 0].copy()
che = ch[ch.ok_c == 0]
nei_re = __import__("re").compile(r"not enough|undetermined|unknown|cannot be determined|neither|neutral|none of", __import__("re").I)
che_pred_nei = che.pred_c.map(lambda s: bool(nei_re.search(s)))
che_gold_nei = che.gold.map(lambda s: bool(nei_re.search(str(s))))
print("\nchoice errors:", len(che), "pred abstain-type (NEI/neutral/none) while gold is not:", int((che_pred_nei & ~che_gold_nei).sum()),
      "gold abstain-type but predicted a content label:", int((~che_pred_nei & che_gold_nei).sum()))
# ordinal off-by-one
od = che[che.ordinal == 1]
if len(od):
    dist = [abs(o.index(p) - o.index(g)) for p, g, o in zip(od.pred_c, od.gold, od.options)]
    print("ordinal choice errors:", len(od), "off-by-one share:", round(np.mean([x == 1 for x in dist]), 3))
# disagreement
print("\nC1 right / E wrong:", int(((df.ok_c == 1) & (df.ok_r == 0)).sum()), " C1 wrong / E right:",
      int(((df.ok_c == 0) & (df.ok_r == 1)).sum()), " both wrong:", int(((df.ok_c == 0) & (df.ok_r == 0)).sum()))
pd.to_pickle(res, f"{SP}/dev_tabs.pkl")
