"""REJECTED by the strict reviewer (2026-09-29); raw/defs deleted, do not re-run into data/v14_parts. Reason: EuroVoc
level-1 domains are assigned from descriptors of the whole act, and the title + Article 1 shown often carries no
evidence for the gold (e.g. 'social questions' for "amending Decision 2008/866/EC as regards its period of
application"; 'international relations' vs an equally plausible 'international organisations' distractor for a UN
convention). Audit: ~20% of yes-rows and ~15% of choice-rows not inferable, before and after an out-of-fold evidence
filter (EVID_YES/EVID_NO below).

Build raw rows for eurlex_domain (MultiEURLEX, Chalkidis et al., EMNLP 2021): EuroVoc domain of an EU legal act.

Source : HF coastalcph/multi_eurlex (the first author's lab), data/multi_eurlex.tar.gz at revision
         2020d0350241461069a54177b639f0e6c7a7a712 (sha256 3a2195bc... = LFS oid, verified while streaming by
         fetch_multieurlex.py). ONLY train.jsonl is read (55,000 acts); dev.jsonl/test.jsonl are skipped unread.
Licence: CC BY-SA 4.0 (license field of the dataset card README.md at the pinned revision); the card's Licensing
         section: EUR-Lex documents, (c) European Union, reusable under Commission Decision 2011/833/EU and CC BY 4.0.
Texts  : English EU legislation (regulations, directives, decisions) from EUR-Lex (human-written).
Labels : EuroVoc level-1 domains (21) derived from the EuroVoc descriptors assigned by the EU Publications Office's
         professional indexers (human). Domain names are the official EuroVoc domain names.
State  : the act's title block + the text of Article 1 (or, if absent, the first recitals), <= ~1,700 chars.
Tasks  : yes/no "Is this act indexed under EuroVoc domain X?" and 4-way "Which of these domains is it indexed under?"
         (exactly one option assigned). Faithfulness of negatives: a "no" domain (and every wrong choice option)
         is never one of the 6 broad cross-cutting domains (EUROPEAN UNION, geography, international relations,
         politics, law, economics) and co-occurs rarely with the act's assigned domains in train
         (P(X | assigned domain) < 0.08 for every assigned domain), so it is not a likely indexing omission.
         Yes/no asks only the 15 specific domains (never the 6 broad ones), with an equal quota of yes and no rows per
         domain (no domain is answerable from its name alone); choice golds are balanced across the 21 domains. Routine act series
         are capped: <= 2 acts per title template (digits/dates removed); near-duplicate states dropped.
Reviewer fix: acts sharing a 12-gram with lex_glue LEDGAR/SCOTUS or LegalBench dropped; textual-evidence filter
         (drop-only): a yes/choice gold needs out-of-fold TF-IDF-LR P(domain | shown text) >= 0.5, and a no-domain or
         wrong option needs P < 0.1, so every gold is visible in the title + Article 1 shown.
Deterministic (seed 20260929). CPU only.
"""
import collections
import itertools
import json
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

KEY = "eurlex_domain"
SEED = 20260929
N_YN = 1800
N_CHOICE = 1500
REV = "2020d0350241461069a54177b639f0e6c7a7a712"
ARCHIVE_SHA = "3a2195bc01c7aea0e302bc7af94f2f55f0c15cdeabfe4e086c083196069a2e83"
CACHE = C.CACHE / "eurlex"
LICENCE = (f"CC BY-SA 4.0 (license field of https://huggingface.co/datasets/coastalcph/multi_eurlex/blob/{REV}/README.md; "
           "EUR-Lex texts (c) European Union, reuse under Decision 2011/833/EU / CC BY 4.0)")
DOMAINS = {  # EuroVoc level-1 concept id: (official domain name, definition)
    "100142": ("politics", "Political framework, parties, elections, parliaments, political rights, public safety, "
                           "executive power and the public service."),
    "100143": ("international relations", "International affairs, development-cooperation policy, international "
                                          "security, defence and relations with third countries."),
    "100144": ("EUROPEAN UNION", "The EU itself: its institutions and civil service, EU law and legal acts as such, "
                                 "EU budget and finance, enlargement and European construction."),
    "100145": ("law", "Sources and branches of law, civil and criminal law, justice and courts, legal procedure, "
                      "international law and fundamental rights."),
    "100146": ("economics", "Economic policy and conditions, growth, regional policy, economic structure, national "
                            "accounts and economic analysis."),
    "100147": ("trade", "Trade and tariff policy, customs duties, import and export arrangements, international "
                        "trade, marketing, consumption and distribution."),
    "100148": ("finance", "Monetary matters, banking and credit, capital movements, investment, public finance, "
                          "budgets, taxation and prices."),
    "100149": ("social questions", "Family, migration, population, social affairs and protection, health and "
                                   "medicine, housing and town planning."),
    "100150": ("education and communications", "Education and training, culture and religion, media and "
                                                "communications, information technology and documentation."),
    "100151": ("science", "Natural and applied sciences and the humanities as fields of knowledge (e.g. life "
                          "sciences, physical sciences), not industrial research programmes."),
    "100152": ("business and competition", "Business organisation and legal forms of companies, management, "
                                           "accounting, and competition rules (cartels, state aid, mergers)."),
    "100153": ("employment and working conditions", "Employment and the labour market, working conditions, pay, "
                                                    "labour law and industrial relations."),
    "100154": ("transport", "Transport policy and organisation of land, rail, road, maritime, inland waterway, air "
                            "and space transport."),
    "100155": ("environment", "Environmental policy, the natural environment, pollution, waste and nature "
                              "protection."),
    "100156": ("agriculture, forestry and fisheries", "Agricultural policy and structures, farming and its means of "
                                                      "production, forestry and fisheries."),
    "100157": ("agri-foodstuffs", "Plant and animal products, processed agricultural produce, beverages, sugar, "
                                  "foodstuffs and food technology."),
    "100158": ("production, technology and research", "Production, technical regulations and standards, "
                                                      "technology, research and intellectual property."),
    "100159": ("energy", "Energy policy, coal and mining, oil and gas, electricity, nuclear and renewable energy."),
    "100160": ("industry", "Industrial policy and sectors: chemicals, iron and steel and metals, mechanical and "
                           "electrical engineering, building, wood, textiles and other industries."),
    "100161": ("geography", "Named places: Member States and their regions, European and non-European countries, "
                            "economic and political groupings of countries, overseas territories."),
    "100162": ("international organisations", "Specific international bodies: United Nations and its agencies, "
                                              "European and other intergovernmental or non-governmental "
                                              "organisations."),
}
BROAD = {"100144", "100161", "100143", "100142", "100145", "100146"}
Q_CHOICE = "Which of these EuroVoc domains is this EU legal act indexed under?"
EVID_YES = 0.5
EVID_NO = 0.1


def make_state(text):
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    title = []
    for ln in lines:
        if re.match(r"^(THE |Having regard|HAVE ADOPTED|HAS ADOPTED|Whereas)", ln):
            break
        title.append(ln)
        if len(title) >= 6:
            break
    body = ""
    try:
        i = lines.index("Article 1")
        body = "Article 1: " + " ".join(lines[i + 1:i + 8])
    except ValueError:
        try:
            i = next(j for j, ln in enumerate(lines) if ln.startswith("Whereas"))
            body = "Recitals: " + " ".join(lines[i + 1:i + 8])
        except StopIteration:
            return None
    body = body[:1100]
    if len(body) == 1100:
        body = body[:body.rfind(" ")] + " ..."
    t = "\n".join(title)[:600]
    if len(t) < 30 or len(body) < 80:
        return None
    return f"{t}\n{body}"


def main():
    sys.exit("eurlex_domain was REJECTED in review (see docstring); not building.")
    sha = (CACHE / "archive_sha256.txt").read_text().strip()
    assert sha == ARCHIVE_SHA, "run fetch_multieurlex.py first"
    docs = [json.loads(l) for l in open(CACHE / "train_en.jsonl")]  # TRAIN ONLY
    freq = collections.Counter()
    co = collections.Counter()
    for d in docs:
        L = d["eurovoc_concepts"]["level_1"]
        freq.update(L)
        co.update(itertools.permutations(L, 2))
    cond = {(a, b): co[(a, b)] / freq[a] for (a, b) in co}  # P(b | a)
    rng = random.Random(SEED)
    docs.sort(key=lambda d: d["celex_id"])
    rng.shuffle(docs)
    nd = C.NearDup(0.6)
    tmpl = collections.Counter()
    stats = collections.Counter()
    recs = []
    for d in docs:
        L = set(d["eurovoc_concepts"]["level_1"])
        if not L or not d["text"]:
            continue
        st = make_state(d["text"])
        if st is None:
            stats["no_state"] += 1
            continue
        tkey = re.sub(r"\d+", "#", re.sub(r"\bof \d{1,2} \w+ \d{4}", "", C.norm(st.split("\n")[2] if st.count("\n") >= 2 else st)))[:80]
        if tmpl[tkey] >= 2:
            stats["template_cap"] += 1
            continue
        if nd.seen(st):
            stats["near_dup"] += 1
            continue
        tmpl[tkey] += 1
        far = [x for x in DOMAINS if x not in L and x not in BROAD and all(cond.get((a, x), 0) < 0.08 for a in L)]
        recs.append({"celex": d["celex_id"], "state": st, "labels": L, "far": far})
    print("usable acts:", len(recs), dict(stats))
    # Reviewer fix (2026-09-29), 1/2: drop acts sharing a 12-gram with lex_glue LEDGAR / SCOTUS or any LegalBench task.
    bad = C.forbidden_legal_hits({r["celex"]: [r["state"]] for r in recs},
                                 ["lexglue_ledgar", "lexglue_scotus", "legalbench_all"])
    recs = [r for r in recs if r["celex"] not in bad]
    print("forbidden-legal 12-gram overlap dropped:", len(bad))
    # Reviewer fix (2026-09-29), 2/2: textual-evidence filter (drop-only, never relabels). Indexers assign ~4 level-1
    # domains from descriptors of the WHOLE act (annexes included); many are not visible in the title + Article 1
    # shown here (e.g. 'production, technology and research' for a tobacco-premium deadline act). An out-of-fold
    # TF-IDF logistic regression per domain (5 folds over all usable train acts) estimates how consistently acts with
    # this kind of text carry the domain. A domain may be the gold of a yes-row or a choice-row only if P >= EVID_YES;
    # a domain may be asked in a no-row or be a wrong choice option only if P < EVID_NO.
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import KFold
    import numpy as np
    ids = sorted(DOMAINS)
    Xv = TfidfVectorizer(sublinear_tf=True, ngram_range=(1, 2), min_df=3, max_features=200000).fit_transform(
        [r["state"] for r in recs])
    Y = np.array([[int(c in r["labels"]) for c in ids] for r in recs])
    P = np.zeros(Y.shape)
    for tr, te in KFold(n_splits=5, shuffle=True, random_state=SEED).split(Y):
        for j in range(len(ids)):
            clf = LogisticRegression(max_iter=2000, C=4.0).fit(Xv[tr], Y[tr, j])
            P[te, j] = clf.predict_proba(Xv[te])[:, 1]
    for i, r in enumerate(recs):
        r["p"] = {c: float(P[i, j]) for j, c in enumerate(ids)}
    print("evidence: mean OOF P(assigned)=%.3f, share of assigned domains with P>=%.1f: %.3f" % (
        P[Y == 1].mean(), EVID_YES, (P[Y == 1] >= EVID_YES).mean()))

    def weighted_pick(cands):
        w = [1.0 / freq[c] for c in cands]
        return rng.choices(sorted(cands), weights=[1.0 / freq[c] for c in sorted(cands)])[0] if w else None

    rows = []
    asked = sorted(x for x in DOMAINS if x not in BROAD)  # yes/no asks only the 15 specific domains
    per = N_YN // (2 * len(asked))
    yes_ct, no_ct = collections.Counter(), collections.Counter()
    n_ch = 0
    for r in recs:
        meta = {"dataset": "coastalcph/multi_eurlex (MultiEURLEX)", "revision": f"hf:{REV}; sha256:{ARCHIVE_SHA}",
                "licence": LICENCE, "split": "train",
                "orig_label": {"celex_id": r["celex"], "level_1": sorted(DOMAINS[x][0] for x in r["labels"])},
                "family": C.FAMILY, "edge": "long_context" if len(r["state"]) > 1500 else None, "seed": SEED}
        want_yes = sum(yes_ct.values()) <= sum(no_ct.values())
        ys = [c for c in asked if c in r["labels"] and yes_ct[c] < per and r["p"][c] >= EVID_YES]
        ns = [c for c in r["far"] if no_ct[c] < per and r["p"][c] < EVID_NO]
        x = None
        if want_yes and ys:
            x = min(ys, key=lambda c: (yes_ct[c], freq[c]))
        elif not want_yes and ns:
            x = min(ns, key=lambda c: (no_ct[c], -max(cond.get((a, c), 0) for a in r["labels"]), c))
        if x is not None:
            gold = "yes" if x in r["labels"] else "no"
            (yes_ct if gold == "yes" else no_ct)[x] += 1
            name = DOMAINS[x][0]
            rows.append({"key": KEY, "rid": f"eurlex-{r['celex']}", "state": r["state"],
                         "instructions": f"Is this EU legal act indexed under the EuroVoc domain '{name}'?",
                         "options": ["yes", "no"], "gold": gold, "soft": None,
                         "meta": {**meta, "config": f"yes/no asked={name}", "defs": f"d{x}"}})
            continue
        far_ok = [c for c in r["far"] if r["p"][c] < EVID_NO]
        golds = [c for c in sorted(r["labels"]) if r["p"][c] >= EVID_YES]
        if n_ch < N_CHOICE and len(far_ok) >= 3 and golds:
            g = min(golds, key=lambda c: (sum(1 for q in rows if q["gold"] == DOMAINS[c][0]), freq[c]))
            negs = rng.sample(sorted(far_ok), 3)
            opts = sorted(DOMAINS[c][0] for c in [g] + negs)
            n_ch += 1
            rows.append({"key": KEY, "rid": f"eurlex-{r['celex']}", "state": r["state"], "instructions": Q_CHOICE,
                         "options": opts, "gold": DOMAINS[g][0], "soft": None,
                         "meta": {**meta, "config": "choice 4 domains (1 assigned)"}})
    # per-domain balance: trim the larger side so every asked domain has a yes share within [0.35, 0.65]
    drop = set()
    for x in asked:
        name = DOMAINS[x][0]
        ys = [i for i, q in enumerate(rows) if q["meta"]["config"] == f"yes/no asked={name}" and q["gold"] == "yes"]
        ns = [i for i, q in enumerate(rows) if q["meta"]["config"] == f"yes/no asked={name}" and q["gold"] == "no"]
        small, big = sorted([ys, ns], key=len)
        keep = int(len(small) * 65 / 35)
        drop.update(big[keep:])
        yes_ct[x], no_ct[x] = (len(ys), min(len(ns), keep)) if ys is small else (min(len(ys), keep), len(ns))
    rows = [q for i, q in enumerate(rows) if i not in drop]
    print("trimmed for per-domain balance:", len(drop))
    rng.shuffle(rows)
    C.write_rows(KEY, rows)
    C.write_defs(KEY, {name: d for name, d in DOMAINS.values()})
    for x, (name, d) in DOMAINS.items():
        C.write_defs(f"{KEY}__d{x}", {
            "yes": f"EU indexers filed the act under '{name}': at least one of its main subjects is in this domain ({d})",
            "no": f"None of the act's main subjects is in '{name}' ({d}); the act is indexed under other domains.",
        })
    C.summary(rows)
    print("asked yes/no (yes, no):", {DOMAINS[k][0]: (yes_ct[k], no_ct[k]) for k in asked})
    print("choice gold:", collections.Counter(r["gold"] for r in rows if r["options"] != ["yes", "no"]).most_common())


if __name__ == "__main__":
    main()
