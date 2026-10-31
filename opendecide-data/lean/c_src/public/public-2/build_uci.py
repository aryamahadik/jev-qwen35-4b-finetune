"""UCI Car Evaluation + Nursery candidates (C_DATA_SPEC.md v4 3.2 #12): labels from the published DEX models; the
rules go in the card. Own 90/10 split by record (no official split): bucket 0 of sha256(dataset:line) -> mix-tuning dev.

The card carries the full hierarchical model recovered exactly from the complete truth table (uci_dex.py; 100% of
records reproduced). Solver A = hierarchy evaluation; solver B = the published class of the record; rows are kept only
when they agree (they agree on every record). At most one row per record over both framings (Car has 1,728 records).
Classes are not marked ordinal (spec 2.4): no meta.option_level.
(fix v1.1, review public-2) Choice rows: the model text moves to `instructions` in finalize (decoder_io shows a choice
row's card only as '- {option}: {definition}' lines); masked class codes are written as such lines; wording uci_ch_w1
says "the model above".
"""
from __future__ import annotations

import json

from p2_common import TMP, page_bucket, rng_for, stable_id, log_progress
from uci_dex import CAR, NURSERY, decompose, evaluate, load, child_value

SPEC = {
    "car": {
        "model": CAR, "source": "c_pub_uci_car", "dataset": "UCI Car Evaluation",
        "subject": "car", "decision": "car acceptability",
        "attr_names": {"buying": "buying price", "maint": "maintenance price", "doors": "doors",
                       "persons": "seats (persons carried)", "lug_boot": "luggage boot", "safety": "safety"},
        "val_names": {"vhigh": "very high", "high": "high", "med": "medium", "low": "low", "2": "2", "3": "3",
                      "4": "4", "5more": "5 or more", "more": "more than 4", "small": "small", "big": "big"},
        "class_names": {"unacc": "unacceptable", "acc": "acceptable", "good": "good", "vgood": "very good"},
        "concept_names": {"PRICE": "price grade", "COMFORT": "comfort grade", "TECH": "technical grade"},
        "ch_gold": {"unacc": 25, "acc": 25, "good": 25, "vgood": 25},
        "yn": 100,
    },
    "nursery": {
        "model": NURSERY, "source": "c_pub_uci_nursery", "dataset": "UCI Nursery",
        "subject": "nursery school application", "decision": "admission ranking",
        "attr_names": {"parents": "parents' occupation", "has_nurs": "child's current nursery",
                       "form": "family form", "children": "number of children", "housing": "housing",
                       "finance": "finances", "social": "social conditions", "health": "health"},
        "val_names": {"usual": "usual", "pretentious": "pretentious", "great_pret": "greatly pretentious",
                      "proper": "proper", "less_proper": "less proper", "improper": "improper",
                      "critical": "critical", "very_crit": "very critical", "complete": "complete",
                      "completed": "completed", "incomplete": "incomplete", "foster": "foster", "1": "1",
                      "2": "2", "3": "3", "more": "more than 3", "convenient": "convenient",
                      "less_conv": "less convenient", "inconv": "inconvenient", "nonprob": "not problematic",
                      "slightly_prob": "slightly problematic", "problematic": "problematic",
                      "recommended": "recommended", "priority": "priority", "not_recom": "not recommended"},
        "class_names": {"not_recom": "not recommended", "recommend": "recommended", "very_recom": "very recommended",
                        "priority": "priority", "spec_prior": "special priority"},
        "concept_names": {"EMPLOY": "employment grade", "STRUCTURE": "structure grade",
                          "STRUCT_FINAN": "structure-and-finance grade", "SOC_HEALTH": "social-and-health grade"},
        "ch_gold": {"not_recom": 45, "very_recom": 30, "priority": 45, "spec_prior": 30},
        "yn": 150,
    },
}

GRADES = "ABCDEFG"

W_CH = {
    "uci_ch_w1": "Under the model above, which class does this {subject} get?",
    "uci_ch_w2": "Apply the decision model to the case. Which class results?",
    "uci_ch_w3": "Which outcome does the model assign to this {subject}?",
    "uci_ch_w4": "Work through the model's tables for this case and pick the final class.",
}
W_YN_GE = {
    "uci_ge_w1": "Under the model, does this {subject} get a class of at least '{c}'?",
    "uci_ge_w2": "Is the model's class for this case '{c}' or better?",
    "uci_ge_w3": "Applying the model, does the case reach '{c}' or a better class?",
}
W_YN_EQ = {
    "uci_eq_w1": "Under the model, is this {subject} classed as '{c}'?",
    "uci_eq_w2": "Does the model put this case in the class '{c}'?",
    "uci_eq_w3": "Is '{c}' the class the model gives this case?",
}


def grade(concept_vals_n, v):
    return GRADES[v]


def card_text(spec, tables, style, examples, masked=None):
    m = spec["model"]
    an, vn, cn, kn = spec["attr_names"], spec["val_names"], spec["class_names"], spec["concept_names"]
    cls_order = list(m["classes"])
    order_best = list(reversed(cls_order))
    name = (lambda c: masked[c]) if masked else (lambda c: cn[c])
    L = [f"Decision model for the {spec['decision']} (a published hierarchical rule model). Compute the "
         f"grades bottom-up; grade A is the best grade of each table."]
    if masked:
        # (fix v1.1) code definitions as '- {code}: {class name}' lines: on a choice row finalize keeps exactly these
        # lines in the card, where decoder_io.card_defs prints each one on its option line ("A. K3: very good")
        L += [f"- {masked[c]}: {cn[c]}" for c in order_best]
    L.append("Classes from best to worst: " + ", ".join(name(c) for c in order_best) + ".")

    def dn(x):
        return an.get(x) or kn.get(x)

    def dv(x, v):
        return vn[v] if x in an else GRADES[v]

    def dom(c):
        return list(range(len(m["attrs"][c]))) if c in m["attrs"] else list(range(tables[c]["n_values"]))

    def val_of(c, i):
        return m["attrs"][c][i] if c in m["attrs"] else i

    def label(c, i):
        return vn[m["attrs"][c][i]] if c in m["attrs"] else GRADES[i]

    def out_name(concept, v):
        return name(v) if concept == "__top__" else GRADES[v]

    def concept_lines(concept, t):
        ch = t["children"]
        tab = {tuple(dom_index(c, v) for c, v in zip(ch, k)): val for k, val in t["table"].items()}
        out = []
        if style == "grid":
            if len(ch) == 2:
                out.append(grid(ch[0], ch[1], lambda i, j: tab[(i, j)], concept))
            else:
                for k in dom(ch[-1]):
                    sub = ch[:-1]
                    out.append(f"When {dn(ch[-1])} is {label(ch[-1], k)}:")
                    if len(sub) == 2:
                        out.append(grid(sub[0], sub[1], lambda i, j, k=k: tab[(i, j, k)], concept))
                    else:
                        out.append(grid3(sub, k, tab, concept))
        else:
            for val, cubes in cover(ch, tab):
                conds = []
                for c, idxs in zip(ch, cubes):
                    if len(idxs) == len(dom(c)):
                        continue
                    conds.append(f"{dn(c)} is " + " or ".join(label(c, i) for i in idxs))
                out.append(f"- {out_name(concept, val)} if " + " and ".join(conds) if conds
                           else f"- {out_name(concept, val)} in every other case")
        return out

    def dom_index(c, v):
        return m["attrs"][c].index(v) if c in m["attrs"] else v

    def grid(a, b, f, concept):
        head = "| " + dn(a) + " \\ " + dn(b) + " | " + " | ".join(label(b, j) for j in dom(b)) + " |"
        sep = "|" + "|".join("---" for _ in range(len(dom(b)) + 1)) + "|"
        rows = ["| " + label(a, i) + " | " + " | ".join(out_name(concept, f(i, j)) for j in dom(b)) + " |"
                for i in dom(a)]
        return "\n".join([head, sep] + rows)

    def grid3(sub, k, tab, concept):
        # three children left: one grid per value of the middle one
        parts = []
        for jj in dom(sub[1]):
            parts.append(f"  and {dn(sub[1])} is {label(sub[1], jj)}:")
            parts.append(grid(sub[0], sub[2], lambda i, j, jj=jj: tab[(i, jj, j, k)], concept))
        return "\n".join(parts)

    def cover(ch, tab):
        """Greedy exact cover of each output value by cubes (one value subset per child)."""
        import itertools as it
        doms = [dom(c) for c in ch]
        subsets = [[tuple(x) for r in range(1, len(d) + 1) for x in it.combinations(d, r)] for d in doms]
        res = []
        vals = sorted(set(tab.values()), key=repr)
        # the most frequent value becomes the default ("in every other case") and goes last
        freq = {v: sum(1 for x in tab.values() if x == v) for v in vals}
        default = max(vals, key=lambda v: (freq[v], repr(v)))
        for val in [v for v in vals if v != default]:
            todo = {k for k, x in tab.items() if x == val}
            cubes = []
            while todo:
                best, bc = None, -1
                for cube in it.product(*subsets):
                    pts = list(it.product(*cube))
                    if any(tab[p] != val for p in pts):
                        continue
                    cov = sum(1 for p in pts if p in todo)
                    if cov > bc or (cov == bc and len(pts) > len(list(it.product(*best)))):
                        best, bc = cube, cov
                cubes.append(best)
                todo -= set(it.product(*best))
            res += [(val, c) for c in cubes]
        res.append((default, tuple(tuple(d) for d in doms)))
        return res

    for concept, t in list(tables.items()):
        if concept == "__top__":
            continue
        L.append("")
        L.append(f"{kn[concept].capitalize()} (from {', '.join(dn(c) for c in t['children'])}):")
        L += concept_lines(concept, t)
    top = tables["__top__"]
    L.append("")
    L.append("Final class (from " + ", ".join(kn[c] for c in top["children"]) + "):")
    L += concept_lines("__top__", {"children": top["children"], "table": top["table"]})
    if examples:
        L.append("")
        for ex in examples:
            L.append("Worked example: " + ex)
    return "\n".join(L)


def derivation(spec, tables, rec, masked=None):
    m = spec["model"]
    kn, cn = spec["concept_names"], spec["class_names"]
    parts = [", ".join(f"{spec['attr_names'][a]} {spec['val_names'][rec[a]]}" for a in m["attrs"])]
    steps = [f"{kn[c]} {GRADES[child_value(m, tables, c, rec)]}" for c in m["concepts"]]
    final = evaluate(m, tables, rec)
    return f"{parts[0]} -> " + "; ".join(steps) + f" -> class {masked[final] if masked else cn[final]}"


def render_case(spec, rec, container, rng):
    m = spec["model"]
    an, vn = spec["attr_names"], spec["val_names"]
    items = [(an[a], vn[rec[a]]) for a in m["attrs"]]
    if container == "key_value":
        return "Case:\n" + "\n".join(f"  {k}: {v}" for k, v in items)
    if container == "json":
        return "Case: " + json.dumps(dict(items), ensure_ascii=False)
    if container == "markdown":
        return ("| " + " | ".join(k for k, _ in items) + " |\n|" + "|".join("---" for _ in items) + "|\n| "
                + " | ".join(v for _, v in items) + " |")
    return f"The {spec['subject']} under review has " + "; ".join(f"{k}: {v}" for k, v in items) + "."


def build(out_path, dev_n=15):
    cands, stats = [], {}
    for key, spec in SPEC.items():
        m = spec["model"]
        recs = load(m)
        _RECS[key] = recs
        tables = decompose(m, recs)
        assert all(evaluate(m, tables, r) == c for _, r, c in recs)
        rng = rng_for("uci", key)
        idx = list(range(len(recs)))
        rng.shuffle(idx)
        train = [i for i in idx if page_bucket(f"{key}:{recs[i][0]}") != 0]
        dev = [i for i in idx if page_bucket(f"{key}:{recs[i][0]}") == 0]
        by_cls = {}
        for i in train:
            by_cls.setdefault(recs[i][2], []).append(i)
        used = set()
        # examples for cards: a fixed set of train records never used as rows
        ex_pool = [by_cls[c].pop() for c in m["classes"] for _ in range(2) if len(by_cls.get(c, [])) > 30]
        used.update(ex_pool)
        plan = []
        for c, n in spec["ch_gold"].items():
            take = int(n * 1.5) + 2
            got = by_cls[c][:take]
            by_cls[c] = by_cls[c][take:]
            plan += [("uci_ch", i) for i in got]
        # yes/no records: same class stratification as the choice rows (records never reused)
        n_yn = int(spec["yn"] * 2.2) + 4
        share = {c: n / sum(spec["ch_gold"].values()) for c, n in spec["ch_gold"].items()}
        for c in spec["ch_gold"]:
            take = int(n_yn * share[c]) + 1
            plan += [("uci_yn", i) for i in by_cls[c][:take]]
            by_cls[c] = by_cls[c][take:]
        dev_by = {}
        for i in dev:
            dev_by.setdefault(recs[i][2], []).append(i)
        devplan = []
        for c in spec["ch_gold"]:
            devplan += [("uci_ch", i) for i in dev_by.get(c, [])[:dev_n // 2 + 2]]
            devplan += [("uci_yn", i) for i in dev_by.get(c, [])[dev_n // 2 + 2:dev_n + 4]]
        for part, pl in (("train", plan), ("dev", devplan)):
            for fr, i in pl:
                row = make_row(key, spec, tables, recs[i], fr, ex_pool, rng_for("uci_row", key, recs[i][0], fr))
                row["_x"]["part"] = part
                row["_x"]["page"] = f"{key}:{recs[i][0]}"
                cands.append(row)
        stats[key] = {"records": len(recs), "train_records": len(train), "dev_records": len(dev),
                      "plan_train": len(plan), "plan_dev": len(devplan),
                      "tables": {c: len(t["table"]) for c, t in tables.items()}}
    with open(out_path, "w") as f:
        for r in cands:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    log_progress(f"UCI candidates: {json.dumps(stats)}")
    return stats


_RECS = {}


def make_row(key, spec, tables, rec_t, fr, ex_pool, rng):
    line_no, rec, published = rec_t
    m = spec["model"]
    a_cls = evaluate(m, tables, rec)  # solver A
    assert a_cls == published  # solver B: the published class
    style = rng.choice(["grid", "rules"])
    masked = None
    if fr == "uci_ch" and rng.random() < 0.15:
        codes = [f"K{i + 1}" for i in range(len(m["classes"]))]
        rng.shuffle(codes)
        masked = dict(zip(m["classes"], codes))
    exs = []
    container = rng.choice(["key_value", "json", "markdown", "prose"])
    cn = spec["class_names"]
    order_best = list(reversed(m["classes"]))
    if fr == "uci_ch":
        opts = [masked[c] if masked else cn[c] for c in m["classes"]]
        rng.shuffle(opts)
        gold = masked[published] if masked else cn[published]
        wid = rng.choice(sorted(W_CH))
        instr = W_CH[wid].format(subject=spec["subject"])
        qtype = "choice"
        extra = {"masked": bool(masked), "k": len(opts)}
    else:
        form = rng.choice(["ge", "eq"])
        want_yes = rng.random() < 0.5
        if form == "ge" and ((want_yes and published == order_best[-1]) or (not want_yes and published == order_best[0])):
            form = "eq"
        if form == "eq":
            asked = published if want_yes else rng.choice([c for c in spec["ch_gold"] if c != published])
            g = int(asked == published)
            wid = rng.choice(sorted(W_YN_EQ))
            instr = W_YN_EQ[wid].format(subject=spec["subject"], c=cn[asked])
        else:
            rank = {c: i for i, c in enumerate(order_best)}  # 0 = best
            ok = [c for c in order_best[:-1] if (rank[published] <= rank[c]) == want_yes]
            assert ok
            asked = rng.choice(ok)
            g = int(rank[published] <= rank[asked])
            wid = rng.choice(sorted(W_YN_GE))
            instr = W_YN_GE[wid].format(subject=spec["subject"], c=cn[asked])
        opts, gold, qtype = None, g, "noul"
        extra = {"form": form, "asked": asked}
    with_ex = rng.random() < 0.5
    if with_ex:
        pick = rng.sample(ex_pool, k=rng.choice([1, 2]))
        all_recs = _RECS[key]
        exs = [derivation(spec, tables, all_recs[j][1], masked) for j in pick]
    card = card_text(spec, tables, style, exs, masked)
    state = render_case(spec, rec, container, rng)
    cid = f"uci_{key}_{style}" + ("_masked" if masked else "") + ("_ex" if exs else "")
    rid = f"{spec['model']['file']}:{line_no + 1}"
    return {
        "id": stable_id(f"pub_uci_{key}_", fr, line_no),
        "group_id": f"g:pub:uci_{key}:{line_no + 1}",
        "call_id": stable_id(f"c_pub_uci_{key}_", fr, line_no),
        "source": spec["source"],
        "state": state,
        "qtype": qtype,
        "instructions": instr,
        "options": opts,
        "gold": gold,
        "role": "aff" if qtype == "noul" else "choice",
        "card": card,
        "meta": {},
        "_x": dict(framing=fr, card_id=cid, wording_id=wid, container=container, record_id=rid,
                   published_class=published, dataset_key=key, record_text=state, defs_style=style,
                   with_examples=bool(exs), **extra),
    }


if __name__ == "__main__":
    print(build(TMP / "cand_uci.jsonl"))
