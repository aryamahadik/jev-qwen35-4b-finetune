"""Scratch (never a gate): cue diagnosis of the T27 G6 failures on pickled RowInfos.
  c view (choice, card without question): n-gram coefficients per class + one-feature CV accuracy of T27 request features
  d_meta (yes/no): meta features one at a time + permutation importance of the GBT
usage (from lean/c2_build): ../../.venv/bin/python -B families/T27/work_i2b/diag.py infos.pkl out.txt [--g6]"""
import collections
import json
import pickle
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[3]
for p in (str(C2), str(C2 / "families" / "T27")):
    if p not in sys.path:
        sys.path.insert(0, p)
sys.setrecursionlimit(20000)
import numpy as np  # noqa: E402
import pilot  # noqa: E402
from families.T27 import overlap as OV  # noqa: E402
from families.T27 import plugin as P  # noqa: E402
from families.T27 import vocab as V  # noqa: E402
from sklearn.ensemble import HistGradientBoostingClassifier  # noqa: E402
from sklearn.feature_extraction import DictVectorizer  # noqa: E402
from sklearn.feature_extraction.text import CountVectorizer  # noqa: E402
from sklearn.linear_model import LogisticRegression  # noqa: E402

infos = pickle.load(open(sys.argv[1], "rb"))
OUT = open(sys.argv[2], "w")


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUT.write(s + "\n")
    OUT.flush()


CLS = {"Stop": "stop_ask", "Ignore": "continue", "Do wh": "do_step"}
ch = [i for i in infos if i.row["qtype"] == "choice"]
yn = [i for i in infos if i.row["qtype"] == "noul"]
say("rows", len(infos), "choice", len(ch), "yes/no", len(yn))


def gold_cls(i):
    g = i.row["gold"]
    return "stop_ask" if g.startswith("Stop") else ("continue" if g.startswith("Ignore") else "do_step")


def clause(sp, key):
    v = sp.slots.get(key)
    return None if v is None else v.value[2]


def item_text(k):
    return V.ITEMS.get(k, k)


def line_pos(state, tmpl_text):
    """relative index of the content line that best matches the request template."""
    body = state.split("--- content start ---")[-1].split("--- content end ---")[0].strip().split("\n")
    t = set(re.findall(r"[a-z]+", re.sub(r"\{[A-Z0-9]+\}", " ", tmpl_text.lower())))
    best, bi = -1, 0
    for j, ln in enumerate(body):
        s = set(re.findall(r"[a-z]+", ln.lower()))
        sc = len(t & s) / max(1, len(t))
        if sc > best:
            best, bi = sc, j
    return bi / max(1, len(body) - 1), len(body)


def feats(i):
    sp, m = i.spec, i.row["meta"]
    env = sp.env()
    task = env["TASK"]
    allowed = P.TASK_SCOPE[task]
    ttext = (clause(sp, "TASK") or "").replace("{TARGET}", item_text(env["TARGET"]))
    ustem = OV.stems(ttext + " " + P.allowed_text(allowed))
    f, n = {}, {}
    f["task"], f["task_kind"] = task, ("+".join(sorted(P.allowed_kinds(task))) or "readonly")
    f["task_first"] = ttext.split()[0].lower() if ttext else "-"
    reqs = [k for k in (1, 2) if f"REQ{k}" in sp.slots]
    f["n_req"] = str(len(reqs))
    os_, lens = [], []
    verbs, firsts, acts, scopes, framings, forms = [], [], [], [], [], []
    for k in reqs:
        sem = env[f"REQ{k}"]
        action, fr = P.REQ_SEM[sem]
        tx = (clause(sp, f"REQ{k}") or "").replace(f"{{GATE{k}}}", item_text(env.get(f"GATE{k}", "")))
        verbs.append(action.split(".")[0])
        acts.append(action)
        scopes.append("in" if action in allowed else "out")
        framings.append(fr)
        forms.append(sp.slots[f"REQ{k}"].value[1])
        toks = re.findall(r"[a-z']+", tx.lower())
        firsts.append(toks[0] if toks else "-")
        lens.append(len(toks))
        rs = OV.stems(tx)
        os_.append(len(rs & ustem) / max(1, len(rs)))
        pos, nl = line_pos(i.row["state"], clause(sp, f"REQ{k}") or "")
        n[f"pos{k}"], n[f"o{k}"], n[f"len{k}"] = pos, os_[-1], float(lens[-1])
        f[f"verb{k}"], f[f"obj{k}"], f[f"first{k}"] = verbs[-1], action, firsts[-1]
        f[f"scope{k}"], f[f"framing{k}"], f[f"form{k}"] = scopes[-1], framings[-1], forms[-1]
        f[f"gate_is_target{k}"] = str(env.get(f"GATE{k}") == env["TARGET"]) if fr == "gate" else "plain"
        f[f"just{k}"] = str(env.get(f"JUST{k}"))
        f[f"gate_item{k}"] = str(env.get(f"GATE{k}"))
        f[f"band{k}"] = OV.band(os_[-1])
    f["verbs"], f["firsts"] = "|".join(sorted(verbs)), "|".join(sorted(firsts))
    f["verb_vs_task_kind"] = "|".join(sorted(("same" if v in {P.KIND_OF[a] for a in allowed} else "diff") for v in verbs))
    f["scopes"] = "|".join(sorted(scopes))
    f["framings"] = "|".join(sorted(framings))
    os_ = os_ or [-1.0]
    lens = lens or [0]
    f["band_min"], f["band_max"] = OV.band(min(os_)), OV.band(max(os_))
    n["o_mean"], n["o_max"], n["o_min"] = float(np.mean(os_)), max(os_), min(os_)
    n["len_mean"], n["len_max"] = float(np.mean(lens)), float(max(lens))
    n["pos_mean"] = float(np.mean([n[f"pos{k}"] for k in reqs])) if reqs else -1.0
    n["pos_gap"] = abs(n["pos1"] - n["pos2"]) if len(reqs) == 2 else -1.0
    n["n_lines"] = float(nl) if reqs else 0.0
    n["pos_mean"] = n["pos_mean"] if reqs else -1.0
    n["len_content"] = float(len(i.row["state"].split("--- content start ---")[-1]))
    n["len_task"] = float(len(ttext))
    f["skin"], f["register"] = str(m["c2"].get("skin_id")), str(m["c2"].get("register"))
    f["format_style"], f["layout"], f["defs"] = str(m.get("format_style")), sp.structure.get("layout"), str(m.get("defs_style"))
    f["info"], f["ovl_level"] = env.get("INFO"), str(sp.structure.get("ovl"))
    f["wording"], f["sampler"] = str(m.get("wording_id")), str(m.get("sampler"))
    f["twin_kind"] = str(m.get("twin_kind"))
    for e in m.get("edge") or []:
        f["edge:" + e] = "1"
    imp = re.compile(r"\b(please|now|immediately|urgent|asap|must|need to|kindly)\b", re.I)
    cont = i.row["state"].split("--- content start ---")[-1]
    n["imp_markers"] = float(len(imp.findall(cont)))
    n["n_excl"] = float(cont.count("!"))
    return f, n


folds_for = lambda xs: pilot._folds([i.row["meta"]["card_id"] for i in xs])  # noqa: E731


def cv_acc(X, y, folds, model):
    pred = np.empty(len(y), dtype=object)
    for tr, te in folds:
        if len(set(y[tr])) < 2:
            pred[te] = y[tr][0]
            continue
        pred[te] = model().fit(X[tr], y[tr]).predict(X[te])
    return float((pred == y).mean())


def one_feature_table(rows, y, folds, top=25, base=None):
    names_c = sorted({k for f, _ in rows for k in f})
    names_n = sorted({k for _, n in rows for k in n})
    res = []
    for k in names_c:
        d = [{k: f.get(k, "NA")} for f, _ in rows]
        if len({x[k] for x in d}) < 2 or len({x[k] for x in d}) > 400:
            continue
        X = DictVectorizer(sparse=True).fit_transform(d).tocsr()
        res.append((cv_acc(X, y, folds, lambda: LogisticRegression(C=1.0, max_iter=300)), k, "cat"))
    for k in names_n:
        X = np.array([[n.get(k, -1.0)] for _, n in rows])
        if np.ptp(X) == 0:
            continue
        res.append((cv_acc(X, y, folds, lambda: HistGradientBoostingClassifier(max_iter=40, max_depth=2, random_state=0)), k, "num"))
    res.sort(reverse=True)
    return res[:top]


# ------------------------------------------------------------------------------------------------ c view (choice)
say("\n===== CHOICE c view =====")
rowsF = [feats(i) for i in ch]
y = np.array([gold_cls(i) for i in ch])
say("gold shares", dict(collections.Counter(y)))
folds = folds_for(ch)
if "--g6" in sys.argv:
    r = pilot.g6_choice(ch)
    say("g6_choice", json.dumps(r))

say("\n-- top 30 n-grams per class (multinomial LR on context unigrams+bigrams, min_df 30, binary)")
cvz = CountVectorizer(ngram_range=(1, 2), min_df=30, binary=True, token_pattern=r"[A-Za-z0-9'-]+")
Xc = cvz.fit_transform([i.context for i in ch]).tocsr()
for C in (1.0,):
    acc = cv_acc(Xc, y, folds, lambda: LogisticRegression(C=C, max_iter=400))
    say(f"row-level multinomial LR on context n-grams: CV acc {acc:.4f} (chance 0.333)")
lr = LogisticRegression(C=1.0, max_iter=400).fit(Xc, y)
names = np.array(cvz.get_feature_names_out())
for ci, c in enumerate(lr.classes_):
    o = np.argsort(-lr.coef_[ci])[:30]
    say(f"[{c}]", "; ".join(f"{names[j]} {lr.coef_[ci][j]:.2f}" for j in o))
# the same on the CONTENT only after removing item words that equal the task's words (request region)
say("\n-- one-feature CV accuracy on T27 request features (chance 0.333; top 25)")
for acc, k, kind in one_feature_table(rowsF, y, folds):
    say(f"  {acc:.4f}  {k} ({kind})")

say("\n-- class mix by key features")
for k in ("verbs", "scopes", "framings", "band_max", "band_min", "ovl_level", "n_req", "verb_vs_task_kind", "layout", "format_style",
          "gate_is_target1", "gate_is_target2", "info"):
    tab = collections.defaultdict(collections.Counter)
    for (f, _), c in zip(rowsF, y):
        tab[f.get(k, "NA")][c] += 1
    say(f"{k}:")
    for v, cnt in sorted(tab.items(), key=lambda kv: -sum(kv[1].values()))[:14]:
        t = sum(cnt.values())
        say(f"   {v:42s} n={t:5d}  stop {cnt['stop_ask']/t:.2f} cont {cnt['continue']/t:.2f} do {cnt['do_step']/t:.2f}")
say("\n-- numeric means by class")
for k in sorted({k for _, n in rowsF for k in n}):
    say(f"  {k:12s}", {c: round(float(np.mean([n.get(k, 0) for (_, n), yy in zip(rowsF, y) if yy == c])), 3) for c in ("stop_ask", "continue", "do_step")})
say("\n-- action verb (kind) frequency per class: first token of the request clause")
for slot in ("first1",):
    tab = collections.defaultdict(collections.Counter)
    for (f, _), c in zip(rowsF, y):
        tab[f.get(slot)][c] += 1
    for v, cnt in sorted(tab.items(), key=lambda kv: -sum(kv[1].values()))[:20]:
        t = sum(cnt.values())
        say(f"   {v:14s} n={t:5d}  stop {cnt['stop_ask']/t:.2f} cont {cnt['continue']/t:.2f} do {cnt['do_step']/t:.2f}")

# ------------------------------------------------------------------------------------------------ d_meta (yes/no)
say("\n===== YES/NO d_meta =====")
yr = np.array([int(i.row["gold"]) for i in yn])
yfolds = folds_for(yn)
if "--g6" in sys.argv:
    r = pilot.g6_yes_no(yn)
    say("g6_yes_no", json.dumps({k: r.get(k) for k in ("n", "yes_rate", "a_question", "c_card_without_question", "d_meta", "d_meta_drivers")}))
feats_m = []
for i in yn:
    c, n_ = pilot.meta_features(i)
    feats_m.append({**c, **n_})
dv = DictVectorizer(sparse=False)
Xd = dv.fit_transform(feats_m)
for rep in range(1):
    acc = cv_acc(Xd, yr, yfolds, lambda: HistGradientBoostingClassifier(max_iter=100, max_depth=3, random_state=0))
    say(f"d_meta GBT CV acc (sklearn default-ish) {acc:.4f}")
from sklearn.inspection import permutation_importance  # noqa: E402
g = HistGradientBoostingClassifier(max_iter=100, max_depth=3, random_state=0).fit(Xd, yr)
pi = permutation_importance(g, Xd, yr, n_repeats=3, random_state=0, scoring="accuracy")
o = np.argsort(-pi.importances_mean)[:12]
say("permutation importance (train acc drop):", [(dv.feature_names_[j], round(float(pi.importances_mean[j]), 4)) for j in o])
say("one-feature CV (meta features alone; top 15):")
res = []
for k in feats_m[0]:
    if isinstance(feats_m[0][k], str):
        X = DictVectorizer(sparse=True).fit_transform([{k: f[k]} for f in feats_m]).tocsr()
        res.append((cv_acc(X, yr, yfolds, lambda: LogisticRegression(max_iter=300)), k))
    else:
        X = np.array([[f[k]] for f in feats_m])
        res.append((cv_acc(X, yr, yfolds, lambda: HistGradientBoostingClassifier(max_iter=40, max_depth=2, random_state=0)), k))
for a, k in sorted(res, reverse=True)[:15]:
    say(f"  {a:.4f} {k}")
say("one-feature CV with T27 request features on yes/no (chance 0.5; top 20):")
rowsY = [feats(i) for i in yn]
for acc, k, kind in one_feature_table(rowsY, yr, yfolds, top=20):
    say(f"  {acc:.4f}  {k} ({kind})")
say("yes rate by qform:")
tab = collections.defaultdict(list)
for i in yn:
    tab[i.row["meta"]["qform"]].append(int(i.row["gold"]))
for k, v in tab.items():
    say(f"   {k:16s} n={len(v)} yes={np.mean(v):.3f}")
say("numeric meta means by gold:")
for k in ("len_state", "len_ins", "len_card", "len_q", "n_numbers", "n_lines", "depth"):
    j = dv.feature_names_.index(k)
    say(f"  {k:10s} gold1 {Xd[yr == 1, j].mean():.1f}  gold0 {Xd[yr == 0, j].mean():.1f}  sd {Xd[:, j].std():.1f}")
