"""g13_attr.py: attribution of the batch-4 G13 candidate drops (c2_mixdev and ohs4_hash keyword) and rows-left estimates.

Analysis only (16 Oct 2026). CPU, no network. Nothing G13-official is run or written; the engine (c_build/decontam_g13.py)
and the wrapper (c2_build/g13_c2.py) are imported READ-ONLY. Run from lean/:

    ../.venv/bin/python -B c2_build/zed_orch/g13_attr/g13_attr.py [--blocks T24 T25 ...] [--out PATH]

What it does (see the JSON "method" block for the exact definitions):
  1  Rebuild the batch-4 c2_mixdev set (sha256-checked against each log) and re-run the engine's c2_mixdev scan on every
     block's candidates (g.TrainIndex / g.Scan, per eval text), then the wrapper's own A53 waiver (X.a53_apply). The
     per-method unit counts must equal the logs' (they do: asserted, "verified_against_logs").
  2  Attribute every BINDING c2_mixdev unit: dev file (own / other family), field and item kind, provenance class of its
     non-waived shared items (program literal / lexicon rule or wording template / skin-document-attack prose / pack or
     entity value / composite / residual), whole-row duplicates.
  3  T25: the exact_full duplicates.
  4  ohs4_hash keyword hits: the hit runs (never stored as text), their origin in OUR code constants and pools (file, list
     name, entry), counts per family.
  5  Rows-left estimates per short family for (i) mixdev rebuilt dev-only, (ii) colliding vocabulary removed, (iii) a
     top-up generation.
No item or row text is written to the JSON: ids, short hashes, counts, list names and (for vocabulary entries of our own
generators) the entry strings only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import attr_core as A  # noqa: E402
import attr_prov as P  # noqa: E402

X, g = A.X, A.g
c2io = A.c2io

PROGRAM_BLOCKS = [b for b in A.BLOCKS if b not in ("GB", "GW", "MD")]
SHORT = ["T24", "T25", "T06", "T07", "T23", "T26", "T28", "T12"]     # the families named in the brief (+ at the line)
OUT_DEFAULT = HERE / "g13_attr.json"


def h8(*parts) -> str:
    return hashlib.sha1("\x1f".join(map(str, parts)).encode()).hexdigest()[:8]


# ------------------------------------------------------------------------------------------------------------------------
# part 1/2: the c2_mixdev scan, A53, attribution of the binding units
# ------------------------------------------------------------------------------------------------------------------------
def coarse_class(c: dict) -> str:
    """Six reporting classes of a classified item (see attr_prov): frame_values (program literal / numerals),
    lexicon_template (rule-clause or wording forms), prose (skin / document / attack text), pack_vocab (pack, entity pools),
    mixed (needs more than one of the three pool groups), residual (words no piece holds)."""
    if c["mode"] == "residual":
        return "residual"
    ks = set(c["kinds"]) - {"code", "number"}
    grp = set()
    for k in ks:
        grp.add("lexicon_template" if k in ("lexicon", "wording") else "prose" if k in ("skin", "document", "attack")
                else "pack_vocab")
    if not grp:
        return "frame_values"
    return next(iter(grp)) if len(grp) == 1 else "mixed"


def attribute_block(B: str, dev: dict, dev_inv: dict, st, S: dict | None = None) -> dict:
    t0 = time.time()
    rows = A.load_block(B)
    sc = A.scan_block(B, rows, dev)
    units, uh = sc["units"], sc["hits"]
    umap = {u["key"]: u for u in units}
    rows_of = {u["key"]: len(u["rows"]) for u in units}
    by = A.hits_for_a53(uh)
    pre = {m: len(d) for m, d in sorted(by.items())}
    bind, a53 = A.apply_a53(B, units, uh, st)
    post = {m: len(d) for m, d in sorted(bind.items())}
    log = A.log_of(B)
    logc = {m: v["units"] for m, v in (log["counts_by_target_and_method"].get("c2_mixdev") or {}).items() if m != "embed"}
    verified = (post == logc)
    M = sorted({k for d in bind.values() for k in d})
    Mset = set(M)
    hit_units = sorted({k for d in by.values() for k in d})
    ent = (a53["blocks"].get("c2_mixdev") or {}).get(B, {})
    eligible = bool(ent.get("eligible"))
    pre_ok = (ent.get("precondition") or {}).get("ok")
    si = A.shared_items(B, rows, units, st)
    items = si["items"]

    def nonwaived(it):
        i = items[it]
        return not (i["indep"] or i["tiled"])

    # --- cause items per binding unit ------------------------------------------------------------------------------
    # cause = the NON-WAIVED shared items (neither asset-independent nor tiled by program literals) when the block has a
    # program inventory; a unit whose items are all waivable (T25: precondition fails) or that has no computable item
    # falls back to all its items / its scan hits. Blocks without an inventory (GB, GW, MD): all shared items.
    has_ctx = si["ctx"] is not None
    cause, no_item, cat = {}, [], {}
    for k in M:
        its = si["unit_items"][k]
        nw = {it for it in its if nonwaived(it)}
        if not its:
            cause[k], cat[k] = set(), "no_computable_shared_item"
            no_item.append(k)
        elif not has_ctx:
            cause[k], cat[k] = set(its), "shared_items_no_waiver_inventory"
        elif nw:
            cause[k], cat[k] = nw, "non_frame_items"
        else:
            cause[k], cat[k] = set(its), "frame_only_blocked_by_precondition"
    # consistency: for an eligible block, binding == hit and not (items and all waived)
    if eligible:
        chk = {k for k in hit_units if not (si["unit_items"][k] and all(not nonwaived(it) for it in si["unit_items"][k]))}
        assert chk == Mset, f"{B}: A53 re-derivation differs from the wrapper's ({len(chk)} vs {len(Mset)})"
    # what would be waived if the A53 precondition held (T25; GB / GW have no program inventory, so none)
    would = {k for k in hit_units if si["unit_items"][k] and all(not nonwaived(it) for it in si["unit_items"][k])} \
        if si["ctx"] is not None else set()
    forced_binding = sorted(set(hit_units) - would) if si["ctx"] is not None else sorted(hit_units)

    # --- (a) dev file attribution (cause-based; scan hits for units with no computable item) ------------------------
    def cause_dev(k):
        if cause[k]:
            s = set()
            for it in cause[k]:
                s |= dev_inv.get(it, set())
            return s
        return {(h[0], h[1]) for h in uh.get(k, [])}
    by_file_units, by_file_excl, combo = defaultdict(set), Counter(), Counter()
    dev_row_units = defaultdict(set)
    for k in M:
        cd = cause_dev(k)
        fams = {f for f, _ in cd}
        for f in fams:
            by_file_units[f].add(k)
        for fr in cd:
            dev_row_units[fr].add(k)
        combo["own_only" if fams == {B} else "other_only" if B not in fams else "own+other"] += 1
        if len(fams) == 1:
            by_file_excl[next(iter(fams))] += 1
    dr_sorted = sorted(dev_row_units.items(), key=lambda x: -len(x[1]))
    own_dev_rows = len(dev.get(B, []))
    inv_rows = {f: len({r for ff, r in dev_row_units if ff == f}) for f in {f for f, _ in dev_row_units}}
    # greedy cover of binding units by dev rows (how few dev rows explain the binding set)
    rem, picked, curve = set(M), [], []
    while rem and len(picked) < 400:
        fr, us = max(dev_row_units.items(), key=lambda x: len(x[1] & rem))
        got = us & rem
        if not got:
            break
        rem -= got
        picked.append(fr)
        if len(picked) in (1, 5, 10, 20, 30, 50, 75, 100, 150):
            curve.append((len(picked), len(Mset) - len(rem)))
    # --- (b) fields and item kinds -----------------------------------------------------------------------------------
    field_c, kind_c, meth_c, tf_c = Counter(), Counter(), Counter(), Counter()
    ufields, ukinds, uclasses = {}, {}, {}
    rit = {}

    def row_it(r):
        if r["id"] not in rit:
            s = X._a53_text_items(r["state"], True, True, False) if isinstance(r.get("state"), str) else set()
            o = set()
            for opt in r.get("options") or []:
                if isinstance(opt, str):
                    o |= X._a53_text_items(opt, False, True, True)
            rit[r["id"]] = (s, o)
        return rit[r["id"]]
    item_line, item_rep = {}, {}
    for k in M:
        fs, ks = set(), set()
        for it in cause[k]:
            ks.add(it[0])
            for r in umap[k]["rows_src"]:
                s, o = row_it(r)
                if it in s:
                    fs.add("state")
                    item_rep.setdefault(it, r)
                if it in o:
                    fs.add("option")
        if not cause[k]:
            fs = {("state" if h[2] == "S" else "option") for h in uh.get(k, [])}
            ks = {"whole_text:" + "+".join(sorted({h[3] for h in uh.get(k, [])}))}
        field_c["+".join(sorted(fs)) or "?"] += 1
        ufields[k], ukinds[k] = sorted(fs), sorted(ks)
        for x in ks:
            kind_c[x] += 1
        for m in {h[3] for h in uh.get(k, [])}:
            meth_c[m] += 1
        for tfld in {h[4] for h in uh.get(k, [])}:
            tf_c[tfld] += 1
    # line types of the state items (one representative training row per item; program blocks, first 4000 items by units)
    icount = Counter(it for k in M for it in cause[k])
    if B in PROGRAM_BLOCKS:
        for it, _n in icount.most_common(4000):
            if it in item_rep and it[0] in ("ng", "seg"):
                item_line[it] = sorted(A.state_lines_of(item_rep[it]["state"], it))
    ltc = Counter()
    for k in M:
        s = set()
        for it in cause[k]:
            s |= set(item_line.get(it, []))
        for x in s:
            ltc[x] += 1
    # --- (d) whole-row duplicates (against the whole dev set) -------------------------------------------------------
    dev_all = [r for rs in dev.values() for r in rs]
    dev_full = {(A.norm_state(r), A.norm_opts(r)): r["id"] for r in dev_all}
    dev_state = {A.norm_state(r) for r in dev_all}
    dev_sg = {g.struct_g13(r.get("state"), r.get("options")) for r in dev_all} - {None}
    dup = Counter()
    dup_units = defaultdict(set)
    for u in units:
        for r in u["rows_src"]:
            ns, no = A.norm_state(r), A.norm_opts(r)
            if (ns, no) in dev_full:
                dup_units["whole_row"].add(u["key"])
            if ns in dev_state:
                dup_units["state_text"].add(u["key"])
            if g.struct_g13(r.get("state"), r.get("options")) in dev_sg:
                dup_units["struct_g13_names_abstracted"].add(u["key"])
    wr = {k: len(v) for k, v in dup_units.items()}
    wr_in_M = {k: len(v & Mset) for k, v in dup_units.items()}
    # exact_full by (eval kind, training field) over the binding units
    ef = Counter()
    for k in M:
        for h in uh.get(k, []):
            if h[3] == "exact_full":
                ef[("state" if h[2] == "S" else "option", h[4])] += 1
    ef_units = len({k for k in M for h in uh.get(k, []) if h[3] == "exact_full"})
    ef_texts = defaultdict(set)
    for k in M:
        for h in uh.get(k, []):
            if h[3] == "exact_full":
                ef_texts[h[5]].add(k)
    ef_list = []
    for u_, ks_ in sorted(ef_texts.items(), key=lambda x: -len(x[1]))[:8]:
        ws_ = tuple(X.words(sc["idx"].raw[u_]))
        tl = bool(si["ctx"] and si["ctx"].tiled(" ".join(ws_)))
        ef_list.append({"text_id": h8(" ".join(ws_)), "words": len(ws_), "binding_units": len(ks_),
                        "tiled_by_program_literals": tl,
                        "training_field": sorted({f for _fam, _rid, _ek, m_, f, uu in
                                                  [h for k in ks_ for h in uh[k]] if m_ == "exact_full" and uu == u_})})
    ef_distinct = len(ef_texts)
    # effect of the drops on the labels: rows that offer / have as gold an option text hit by exact_full (a fixed option label)
    drop_set = set(log["drop_ids"])
    const = {" ".join(X.words(sc["idx"].raw[u_])) for u_ in ef_texts}
    chrows = [r for r in rows if r.get("qtype") == "choice" and isinstance(r.get("options"), list)]
    nn = lambda t: " ".join(X.words(t)) if isinstance(t, str) else ""  # noqa: E731
    off_all = [r for r in chrows if any(nn(o) in const for o in r["options"])]
    gold_all = [r for r in chrows if nn(r.get("gold")) in const]
    nl = [r for r in rows if r.get("qtype") == "noul" and isinstance(r.get("gold"), int)]
    label_effect = {
        "choice_rows": len(chrows), "choice_rows_left": sum(1 for r in chrows if r["id"] not in drop_set),
        "choice_rows_offering_a_hit_option_text": len(off_all),
        "of_which_left": sum(1 for r in off_all if r["id"] not in drop_set),
        "choice_rows_with_hit_option_text_as_gold": len(gold_all),
        "of_which_gold_left": sum(1 for r in gold_all if r["id"] not in drop_set),
        "noul_rows": len(nl), "noul_rows_left": sum(1 for r in nl if r["id"] not in drop_set),
        "noul_gold1_share_all": round(sum(r["gold"] for r in nl) / max(1, len(nl)), 3),
        "noul_gold1_share_left": round(sum(r["gold"] for r in nl if r["id"] not in drop_set) /
                                       max(1, sum(1 for r in nl if r["id"] not in drop_set)), 3)}
    # --- (c) provenance of the non-waived items ------------------------------------------------------------------------
    cls_items, cls_units = Counter(), Counter()
    cls_pure = Counter()
    item_cls = {}
    lex_overlap = None
    if B in PROGRAM_BLOCKS:
        inv = P.Inventory(B)
        for k in M:
            for it in cause[k]:
                if it not in item_cls:
                    c = inv.classify(tuple(it[1].split()))
                    item_cls[it] = (coarse_class(c), P.kind_group(c), c)
        for it, (cc, kg, c) in item_cls.items():
            cls_items[cc] += 1
        for k in M:
            s = {item_cls[it][0] for it in cause[k]}
            uclasses[k] = sorted(s)
            for x in s:
                cls_units[x] += 1
            cls_pure[next(iter(s)) if len(s) == 1 else ("mixed_classes" if s else "no_item_unit")] += 1
        # fine signature counts per item (not text)
        sigi = Counter(item_cls[it][1] for it in item_cls)
        GRP = {"lexicon": "lexicon_template", "wording": "lexicon_template", "skin": "prose", "document": "prose",
               "attack": "prose", "pack": "pack_vocab", "entity": "pack_vocab"}

        def flags(it):
            c = item_cls[it][2]
            ws = it[1].split()
            f = {"num": any(P.is_value(w) for w in ws), "resid": c["mode"] == "residual", "need": set(), "alt": set(), "frame": False}
            if c["mode"] == "contiguous":
                f["frame"] = "code" in c["kinds"]
                f["alt"] = {GRP[k] for k in c["kinds"] if k in GRP}
            else:
                f["need"] = {GRP[k] for k in c["kinds"] if k in GRP}
            return f
        fl = {it: flags(it) for it in item_cls}

        def freed_by(group):
            return {k for k in M if cause[k] and all(group in fl[it]["need"] or fl[it]["alt"] == {group} for it in cause[k]
                                                    if not fl[it]["frame"] and not fl[it]["resid"]) and
                    all(not fl[it]["frame"] and not fl[it]["resid"] for it in cause[k])}
        freed_sets = {"numerals_disjoint": {k for k in M if cause[k] and all(fl[it]["num"] for it in cause[k])}}
        for grp_ in ("lexicon_template", "prose", "pack_vocab"):
            freed_sets[f"{grp_}_held_out"] = freed_by(grp_)
        freed_sets["any_pool_group_or_numerals"] = {k for k in M if cause[k] and all(
            fl[it]["num"] or (not fl[it]["frame"] and not fl[it]["resid"] and (fl[it]["need"] or fl[it]["alt"])) for it in cause[k])}
        freed_sets["lexicon_and_numerals"] = {k for k in M if cause[k] and all(
            fl[it]["num"] or (not fl[it]["frame"] and not fl[it]["resid"] and ("lexicon_template" in fl[it]["need"] or fl[it]["alt"] == {"lexicon_template"}))
            for it in cause[k])}
        freed_if = {n: {"units": len(v), "rows": sum(rows_of[k] for k in v)} for n, v in freed_sets.items()}
        tk = Counter()
        for it, (cc_, kg_, c_) in item_cls.items():
            if cc_ == "lexicon_template":
                ks_ = set(c_["kinds"])
                tk["rule_clause_forms" if "lexicon" in ks_ and "wording" not in ks_ else "question_wordings" if "wording" in ks_
                   and "lexicon" not in ks_ else "both"] += 1
        template_items_by_kind = dict(tk)
        items_num = sum(1 for it in fl if fl[it]["num"])
        lc, lv = set(), set()
        for r in rows:
            lc |= set(((r["meta"].get("c2") or {}).get("lexicon_ids")) or [])
        for r in dev.get(B, []):
            lv |= set(((r["meta"].get("c2") or {}).get("lexicon_ids")) or [])
        nq = lambda s: {x for x in s if not x.startswith("q.")}  # noqa: E731
        lex_overlap = {"dev_forms": len(lv), "dev_forms_shared_with_candidates": len(lv & lc),
                       "dev_rule_forms": len(nq(lv)), "dev_rule_forms_shared": len(nq(lv) & nq(lc)),
                       "dev_question_forms": len(lv) - len(nq(lv)),
                       "dev_question_forms_shared": len((lv & lc)) - len(nq(lv) & nq(lc))}
    else:
        sigi, freed_sets, freed_if, items_num, template_items_by_kind = Counter(), {}, {}, None, {}
    # top cause items by units (ids only)
    ic = Counter()
    for k in M:
        for it in cause[k]:
            ic[it] += 1
    top_items = [{"item": h8(*it), "kind": it[0], "words": len(it[1].split()), "units": n,
                  "dev_rows": len(dev_inv.get(it, ())), "dev_files": sorted({f for f, _ in dev_inv.get(it, ())}),
                  "rows_in_candidates": items[it]["rows"], "dims": items[it]["dims"],
                  "class": (item_cls[it][0] if it in item_cls else None),
                  "group": (item_cls[it][1] if it in item_cls else None)} for it, n in ic.most_common(12)]
    # greedy item cover of the binding units
    cover, rem2 = [], set(k for k in M if cause[k])
    iu = defaultdict(set)
    for k in rem2:
        for it in cause[k]:
            iu[it].add(k)
    if len(iu) > 5000:                                   # keep the cover loop fast on the big real-text blocks
        iu = {it: us for it, us in iu.items() if len(us) >= 2}
    tot2 = len(rem2)
    while rem2 and iu and len(cover) < 60:
        it = max(iu, key=lambda i: len(iu[i] & rem2))
        got = iu[it] & rem2
        if not got:
            break
        rem2 -= got
        cover.append((len(cover) + 1, tot2 - len(rem2)))
    real_text = None
    if B not in PROGRAM_BLOCKS:
        stem = lambda c: re.sub(r"_c\d+$", "", c or "")  # noqa: E731
        devmeta = {r["id"]: r.get("meta") or {} for r in dev_all}
        same = Counter()
        pairs = Counter()
        for k in M:
            tm = [(r.get("meta") or {}) for r in umap[k]["rows_src"]]
            cd = cause_dev(k)
            dm = [devmeta[rid] for _f, rid in cd if rid in devmeta]
            flags = set()
            if any(t.get("domain") and t.get("domain") == d.get("domain") for t in tm for d in dm):
                flags.add("same_domain")
            if any(t.get("task_id") and t.get("task_id") == d.get("task_id") for t in tm for d in dm):
                flags.add("same_task_id")
            if any(t.get("card_id") and stem(t.get("card_id")) == stem(d.get("card_id")) for t in tm for d in dm):
                flags.add("same_card_stem")
            same["+".join(sorted(flags)) or "none"] += 1
            for t in tm[:1]:
                for d in dm[:1]:
                    pairs[(str(t.get("domain")), str(d.get("domain")))] += 1
        real_text = {"binding_units_by_shared_source_flags": dict(same),
                     "top_train_domain_x_dev_domain_units": [[a, b, n] for (a, b), n in pairs.most_common(8)]}
    # --- result -------------------------------------------------------------------------------------------------------
    pre_units = len(hit_units)
    res = {
        "rows": len(rows), "units": len(units), "log_drop_units": log["drop_units"], "log_drop_rows": len(log["drop_ids"]),
        "rows_left": len(rows) - len(log["drop_ids"]), "target": c2io.ALL_TARGETS.get(B),
        "scan_pre_waiver_units_by_method": pre, "binding_units_by_method": post, "log_units_by_method": logc,
        "verified_against_logs": verified, "units_hit_pre_waiver": pre_units, "binding_units": len(M),
        "binding_rows": sum(rows_of[k] for k in M), "waived_units": pre_units - len(M),
        "a53": {"eligible": eligible, "precondition_ok": pre_ok, "why": ent.get("why"),
                "shared_values": (ent.get("precondition") or {}).get("shared_values"),
                "units_waived": ent.get("units_waived"), "units_binding": ent.get("units_binding")},
        "binding_if_precondition_held": {"units": len(forced_binding), "rows": sum(rows_of[k] for k in forced_binding),
                                         "freed_units": len(would), "freed_rows": sum(rows_of[k] for k in would)},
        "units_with_no_computable_shared_item": len(no_item),
        "binding_unit_categories": dict(Counter(cat.values())),
        "real_text_overlap": real_text,
        "a_dev_file": {"binding_units_by_dev_file": {f: len(v) for f, v in sorted(by_file_units.items(), key=lambda x: -len(x[1]))},
                       "exclusive_single_file": dict(by_file_excl), "own_vs_other": dict(combo),
                       "dev_rows_involved": inv_rows, "own_dev_rows": own_dev_rows,
                       "top_dev_rows_units": [len(u) for _, u in dr_sorted[:5]],
                       "dev_rows_to_cover_binding": curve},
        "b_field_and_kind": {"cause_field_units": dict(field_c), "cause_item_kind_units": dict(kind_c),
                             "state_line_type_units": dict(ltc), "training_field_of_scan_hits_units": dict(tf_c),
                             "scan_methods_units": dict(meth_c),
                             "instructions_and_card": "not part of the c2_mixdev comparison (A25 c): 0 binding units"},
        "c_provenance": {"distinct_cause_items": len(ic), "items_by_class": dict(cls_items), "units_with_class": dict(cls_units),
                         "units_by_pure_class": dict(cls_pure), "items_by_signature": dict(sigi.most_common(14)),
                         "lexicon_form_overlap_dev_vs_candidates": lex_overlap,
                         "items_containing_a_numeral_or_short_id": items_num,
                         "lexicon_template_items_by_kind": template_items_by_kind,
                         "units_freed_if_held_out_diagnostic": freed_if,
                         "item_cover_curve_units_vs_items": cover[:12] + cover[-1:] if cover else []},
        "d_whole_row": {"candidate_units_with_whole_row_duplicate_of_a_dev_row": wr.get("whole_row", 0),
                        "candidate_units_with_state_text_equal_to_a_dev_state": wr.get("state_text", 0),
                        "candidate_units_with_names_abstracted_structure_equal": wr.get("struct_g13_names_abstracted", 0),
                        "of_which_binding": wr_in_M, "exact_full_units_in_binding": ef_units,
                        "exact_full_distinct_training_texts": ef_distinct, "exact_full_top_texts": ef_list,
                        "label_effect_of_all_drops_and_option_constants": label_effect,
                        "exact_full_by_eval_kind_and_training_field_hits": {f"{a}/{b}": n for (a, b), n in ef.items()}},
        "top_cause_items": top_items,
        "wall_s": round(time.time() - t0, 1),
    }
    unit_records = []
    for k in M:
        cd = cause_dev(k)
        unit_records.append({
            "block": B, "unit": k, "rows": umap[k]["rows"], "category": cat[k],
            "dev_files": sorted({f for f, _ in cd}), "own_family_dev": any(f == B for f, _ in cd),
            "other_family_dev": sorted({f for f, _ in cd if f != B}), "dev_rows": len(cd),
            "fields": ufields.get(k), "item_kinds": ukinds.get(k), "n_cause_items": len(cause[k]),
            "item_classes": uclasses.get(k), "scan_methods": sorted({h[3] for h in uh.get(k, [])}),
            "exact_full": any(h[3] == "exact_full" for h in uh.get(k, []))})
    keep = {"unit_records": unit_records, "freed_sets": freed_sets, "M": M, "hit_units": hit_units, "forced_binding": forced_binding, "rows_of": rows_of, "units": [u["key"] for u in units],
            "umap_rows": {u["key"]: u["rows"] for u in units}, "cause": cause, "si": si, "umap": umap, "uh": uh}
    return res, keep


# ------------------------------------------------------------------------------------------------------------------------
# part 3: T25 exact_full
# ------------------------------------------------------------------------------------------------------------------------
def t25_exact_full(dev: dict, dev_inv: dict, keep: dict) -> dict:
    B = "T25"
    rows = A.load_block(B)
    sc = A.scan_block(B, rows, dev)
    idx, uh = sc["idx"], sc["hits"]
    tex = defaultdict(set)
    for k, hs in uh.items():
        for fam, rid, ek, m, f, u in hs:
            if m == "exact_full":
                tex[u].add(k)
    consts = []
    for u, ks in sorted(tex.items(), key=lambda x: -len(x[1])):
        ws = idx.ids[u]
        consts.append({"text_id": h8(idx.raw[u]), "words": int(len(ws)), "units": len(ks),
                       "rows": sum(len(keep["umap_rows"][k]) for k in ks), "in_field": "option"})
    # where the two constants live in our program
    ab = {}
    p = X.block_dir(B) / "plugin.py"
    for s, ln, owner in P.code_literal_owners(p):
        for u in tex:
            if " ".join(X.words(s)) == " ".join(X.words(idx.raw[u])):
                ab[owner] = {"file": "c2_build/families/T25/plugin.py", "line": ln}
    cand = rows
    dv = dev[B]
    dseed = {r["meta"]["seed"] for r in dv}
    cseed = {r["meta"]["seed"] for r in cand}
    gen = json.loads((A.LEAN / "data" / "c2_parts" / B / "qc" / "GEN_REPORT.json").read_text())
    wd, wc = {r["meta"]["wording_id"] for r in dv}, {r["meta"]["wording_id"] for r in cand}
    # which dev rows carry the constants
    dev_with = {(f, r) for u in tex for (f, r) in
                {(h[0], h[1]) for ks in [tex[u]] for k in ks for h in uh[k] if h[3] == "exact_full" and h[5] == u}}
    pools = json.loads((A.LEAN / "c2_build" / "families" / B / "pools_v2" / "lexicon.json").read_text())
    qf = Counter(f.get("held_out") for f in pools["forms"] if f.get("kind") == "question")
    wp = json.loads((A.LEAN / "c2_build" / "families" / B / "pools_v2" / "wordings.json").read_text())["items"]
    fid_q = {i["form_id"]: i["qform"] for i in wp}
    fof = lambda w: w.split("WD-")[-1]  # noqa: E731
    cu, du = {fof(r["meta"]["wording_id"]) for r in cand}, {fof(r["meta"]["wording_id"]) for r in dv}
    wording_pool = {"pool_wordings": len(fid_q), "used_by_candidates": len(cu), "used_by_dev": len(du), "shared": len(cu & du),
                    "dev_only": len(du - cu), "unused_by_candidates_by_qform": dict(Counter(fid_q[f] for f in set(fid_q) - cu)),
                    "dev_qforms": dict(Counter(fid_q[f] for f in du if f in fid_q)),
                    "candidate_rows_using_a_shared_wording": sum(1 for r in cand if fof(r["meta"]["wording_id"]) in cu & du),
                    "dev_rows_using_a_shared_wording": sum(1 for r in dv if fof(r["meta"]["wording_id"]) in cu & du)}
    return {
        "exact_full_units": len({k for ks in tex.values() for k in ks}), "distinct_training_texts_hit": len(tex),
        "constants": consts, "program_owner_of_the_constants": ab,
        "whole_row_duplicates_candidates_vs_dev": 0,
        "seed_bases": gen.get("seeds"), "candidate_seed_range": [min(cseed), max(cseed)], "dev_seed_range": [min(dseed), max(dseed)],
        "shared_seeds": len(cseed & dseed),
        "shared_structure_hash": len({r["meta"]["structure_hash"] for r in cand} & {r["meta"]["structure_hash"] for r in dv}),
        "shared_group_id": len({r["group_id"] for r in cand} & {r["group_id"] for r in dv}),
        "shared_ids": len({r["id"] for r in cand} & {r["id"] for r in dv}),
        "shared_state_texts": len({r["state"] for r in cand} & {r["state"] for r in dv}),
        "dev_rows_with_a_constant": len(dev_with), "dev_rows": len(dv),
        "dev_wordings": len(wd), "candidate_wordings": len(wc), "wordings_shared": len(wd & wc),
        "pool_question_forms_held_out_flag_counts": {str(k): v for k, v in qf.items()},
        "wording_pool": wording_pool,
        "conclusion": "Not an RNG / seed overlap and not a pool overlap: the candidates draw seeds from base 250,000,000 and the "
                      "mixdev from 252,000,000 (no shared seed, id, group_id, structure hash or state text). The 320 exact_full "
                      "units are two PROGRAM CONSTANTS (the abstain option labels ABSTAIN_TEXT and SOURCE_ABSTAIN_TEXT of "
                      "plugin.py) that every row offering the abstain answer carries, in candidates and mixdev alike. A53 "
                      "would waive them (tiled by program literals) but the A53 precondition fails: T25 has no held-out "
                      "question wordings (0 of its question forms are flagged held_out; the S5 sampler reuses the training "
                      "wordings: 72 of the 74 dev wordings are also candidate wordings).",
    }


# ------------------------------------------------------------------------------------------------------------------------
# part 4: ohs4_hash keyword hits and our vocabulary
# ------------------------------------------------------------------------------------------------------------------------
KW = None


def kw_hit_runs(text: str, ex) -> list:
    """(token start, run length, normalised words of the run, variant) for every run the wrapper's keyword rule hashes into
    the sealed keyword set. Same enumeration as X.keyword_hashes; the run strings stay in memory only."""
    toks = re.sub(r"\s+", " ", text.strip().lower()).split(" ") if text.strip() else []
    out = []
    for i in range(len(toks)):
        for n in range(1, 9):
            if i + n > len(toks):
                break
            run = " ".join(toks[i:i + n])
            for r in {run, run.strip(X.KW_STRIP).strip()}:
                if len(r) >= 4 and X.sha_hex(r) in ex.sets["keyword"]:
                    out.append((i, n, " ".join(X.words(r))))
    for u in X.URL_RE.findall(text):
        host = X.urlsplit(u).netloc.lower()
        if host:
            for hh in {host, host[4:] if host.startswith("www.") else "www." + host}:
                if X.sha_hex(hh) in ex.sets["keyword"]:
                    out.append((-1, 0, "url:" + hh))
    return out


def minimal_runs(hr: list) -> list:
    return [(i, n, s) for (i, n, s) in hr if i < 0 or not any(j >= 0 and j >= i and j + m <= i + n and (j, m) != (i, n)
                                                               for (j, m, _s) in hr)]


def vocab_origins(B: str, runs: set) -> dict:
    """Where each hit run (normalised words) occurs in OUR generator: code literals (file, owner, line, entry length) and
    pool pieces (file, kind, key path, record id, entry length). Entries are our own vocabulary strings."""
    root = X.block_dir(B)
    out = {r: {"code": [], "pools": []} for r in runs}
    for name in X.CODE_FILES:
        p = root / name
        if X.resolved_refusal(p) or not p.is_file():
            continue
        for s, ln, owner in P.code_literal_owners(p):
            ws = " ".join(X.words(s))
            if not ws:
                continue
            for r in runs:
                if re.search(r"(?<![^ ])" + re.escape(r) + r"(?![^ ])", ws):
                    out[r]["code"].append({"file": f"{name}", "owner": owner, "line": ln, "entry": s if len(ws.split()) <= 4 else None,
                                           "entry_words": len(ws.split())})
    inv = P.Inventory(B)
    for kind, kd in inv.kinds.items():
        if kind == "code":
            continue
        for (rid, ws, kp, fname) in kd.pieces:
            s = " ".join(ws)
            for r in runs:
                if re.search(r"(?<![^ ])" + re.escape(r) + r"(?![^ ])", s):
                    out[r]["pools"].append({"file": fname, "kind": kind, "key": kp, "record": rid,
                                            "entry": " ".join(ws) if len(ws) <= 4 else None, "entry_words": len(ws)})
    return out


def keyword_block(B: str, ex, keep: dict | None = None) -> dict:
    rows = A.load_block(B)
    units = X.row_units(rows)
    umap = {u["key"]: u for u in units}
    hits, rep = X.ohs4_hash_hits(units, ex)
    log_k = (A.log_of(B)["counts_by_target_and_method"].get("ohs4_hash") or {})
    ok = {m: len(d) for m, d in hits.items()} == {m: v["units"] for m, v in log_k.items()}
    kwu = hits.get("keyword", {})
    run_units = defaultdict(set)        # run -> unit keys
    unit_runs = {}
    field_c = Counter()
    for k in kwu:
        rs = set()
        for r in umap[k]["rows_src"]:
            for f, t in X.row_fields(r):
                for (i, n, s) in minimal_runs(kw_hit_runs(t, ex)):
                    rs.add(s)
                    field_c[f] += 1
        unit_runs[k] = rs
        for s in rs:
            run_units[s].add(k)
    origins = vocab_origins(B, set(run_units)) if run_units and B in PROGRAM_BLOCKS else {}
    runs_out = []
    for s, ks in sorted(run_units.items(), key=lambda x: -len(x[1])):
        o = origins.get(s, {"code": [], "pools": []})
        code, pools = o["code"], o["pools"]
        short = [e for e in code + pools if e["entry_words"] <= 4]
        longp = [e for e in code + pools if e["entry_words"] > 4]
        runs_out.append({"run_id": h8(s), "words_in_run": len(s.split()) if not s.startswith("url:") else 0,
                         "units": len(ks), "rows": sum(len(umap[k]["rows"]) for k in ks),
                         "origin_vocab_entries": [{"where": "code", "file": e["file"], "list": e["owner"], "line": e["line"], "entry": e["entry"]}
                                                  for e in code if e["entry_words"] <= 4],
                         "origin_pool_entries": [{"where": "pool", "file": e["file"], "kind": e["kind"], "key": e["key"],
                                                  "record": e["record"], "entry": e["entry"]} for e in pools if e["entry_words"] <= 4][:40],
                         "n_pool_entries": len([e for e in pools if e["entry_words"] <= 4]),
                         "origin_long_strings": {"code": [{"file": e["file"], "list": e["owner"], "line": e["line"]} for e in code if e["entry_words"] > 4][:10],
                                                 "pool_records": len([e for e in pools if e["entry_words"] > 4]),
                                                 "pool_files": sorted({e["file"] for e in pools if e["entry_words"] > 4})},
                         "_run": s})
    return {"ok_vs_log": ok, "log_ohs4_hash_units_by_method": {m: v["units"] for m, v in log_k.items()},
            "keyword_units": len(kwu), "keyword_rows": sum(len(umap[k]["rows"]) for k in kwu),
            "other_ohs4_hash_units": {m: len(d) for m, d in hits.items() if m != "keyword"},
            "report_only_short_exact": rep, "hit_field_counts": dict(field_c), "distinct_hit_runs": len(run_units),
            "runs": runs_out, "unit_runs": unit_runs, "all_ohs4_units": sorted({k for d in hits.values() for k in d}),
            "kwu": sorted(kwu)}


def all_entries(B: str) -> list:
    """Every string of OUR generator for block B: code literals (owner = the module constant / function), pool leaves
    (file, key path, record id). GW additionally has its wave-2 builders (c2_build/gblock/wave2/builders/*.py)."""
    out = []
    roots = [(X.block_dir(B), X.CODE_FILES)]
    if B == "GW":
        bd = A.LEAN / "c2_build" / "gblock" / "wave2" / "builders"
        roots.append((bd, tuple(sorted(f.name for f in bd.glob("*.py")))))
    for root, names in roots:
        for name in names:
            p = root / name
            if X.resolved_refusal(p) or not p.is_file():
                continue
            for text, ln, owner in P.code_literal_owners(p):
                if text.strip():
                    out.append({"where": "code", "file": name, "owner": owner, "record": f"L{ln}", "text": text})
    if B in PROGRAM_BLOCKS:
        inv = P.Inventory(B)
        for rel, kind in inv.files.items():
            if kind == "code":
                continue
            p = A.LEAN / rel
            for line, rec in X.pool_records(p, A.ILOG):
                rid = P._rec_id(rec, rel, line)
                for kp, t in P._leaves(rec):
                    if t.strip():
                        out.append({"where": "pool", "file": p.name, "owner": kp, "record": rid, "text": t, "kind": kind})
    return out


def vocab_scan(B: str, ex, run_units: dict) -> dict:
    """The pseudo-record check of our own vocabulary: every entry that holds a run of the sealed keyword block-list, with where
    it lives. run_units: {run id: units hit in the candidates} so latent entries (never drawn in batch 4) are told apart."""
    ents = all_entries(B)
    hit, stems = [], Counter()
    for e in ents:
        runs = {h8(sr) for (_i, _n, sr) in minimal_runs(kw_hit_runs(e["text"], ex))}
        if runs:
            nw = len(X.words(e["text"]))
            hit.append({"where": e["where"], "file": e["file"], "list_or_key": e["owner"], "record": e["record"],
                        "entry": e["text"] if nw <= 4 else None, "words": nw, "runs": sorted(runs),
                        "drawn_in_batch4_rows": any(r in run_units for r in runs)})
            for r in runs:
                stems[r] += 1
    short = [h for h in hit if h["words"] <= 4]
    by_list = Counter((h["where"], h["file"], h["list_or_key"]) for h in short)
    return {"entries_scanned": len(ents), "colliding_entries": len(hit), "colliding_short_entries": len(short),
            "colliding_long_strings": len(hit) - len(short),
            "colliding_short_entries_by_list": [{"where": w, "file": f, "list_or_key": k, "entries": n}
                                                for (w, f, k), n in by_list.most_common()],
            "colliding_short_entries_detail": short[:80],
            "colliding_long_strings_by_file": dict(Counter(h["file"] for h in hit if h["words"] > 4)),
            "stems": sorted(stems), "entries_scanned_for_runchecker": [e["text"] for e in ents if len(X.words(e["text"])) <= 12]}


def runchecker_on_vocab(texts: list) -> dict:
    """The sealed-side rows checker (run only, through g13_c2.run_checker) on all our short vocabulary strings as pseudo-records.
    g13_ohs4_check has no keyword method (the keyword block-list is applied by program from the pinned hash exports), so this
    only shows that no other method (exact / segment / 10- and 12-gram / Tulu / MinHash / structure) fires on vocabulary."""
    recs = [{"id": f"vocab|{i}", "call_id": f"vocab|{i}", "state": t} for i, t in enumerate(sorted(set(texts)))]
    r = X.run_checker(X.G13_OHS4_TOOL, "--rows", recs)
    return {"records_sent": r.get("records_sent"), "status": r.get("status"), "exit": r.get("exit"),
            "hit_ids": len(r.get("hit_ids") or []), "methods": r.get("methods"), "wall_s": r.get("wall_s")}


# ------------------------------------------------------------------------------------------------------------------------
# part 5: estimates
# ------------------------------------------------------------------------------------------------------------------------
def estimate_block(B: str, res: dict, keep: dict, kw: dict | None, log: dict) -> dict:
    rows_of = keep["rows_of"]
    allu = set(keep["units"])
    R_rows = lambda s: sum(rows_of[k] for k in s)  # noqa: E731
    drop_ids = set(log["drop_ids"])
    D = {k for k in allu if keep["umap_rows"][k] and all(r in drop_ids for r in keep["umap_rows"][k])}
    M = set(keep["M"])
    H4 = set(kw["all_ohs4_units"]) if kw else set()
    K = set(kw["kwu"]) if kw else set()
    R = D - (M | H4)                                  # dropped by the other (old) targets only: exact
    outside = allu - (M | H4)
    pP = len(R) / max(1, len(outside))                # P(other-target hit) among units outside M and the ohs4 hits
    pP_rows = R_rows(R) / max(1, R_rows(outside))
    N = res["rows"]
    left_now = N - len(drop_ids)
    target = res["target"]
    # removable keyword units: every hit run of the unit has only short vocabulary origins (code constants / pool entries)
    fix_vocab, fix_vocab_loose = set(), set()
    if kw:
        runs_by_id = {r["_run"]: r for r in kw["runs"]}

        def short_origin(r):
            return bool(r["origin_vocab_entries"] or r["origin_pool_entries"])

        def long_origin(r):
            lo = r["origin_long_strings"]
            return bool(lo["code"] or lo["pool_records"])
        for k in K:
            rs = kw["unit_runs"].get(k, set())
            if rs and all(short_origin(runs_by_id[s]) for s in rs):
                fix_vocab_loose.add(k)
                if not any(long_origin(runs_by_id[s]) for s in rs):
                    fix_vocab.add(k)

    def scenario(M_s: set, H4_s: set):
        kept = M_s | H4_s
        freed = (M | H4) - kept
        # expected rows dropped: exact R, kept, plus other-target hits among the freed (independence at rate pP_rows)
        dropped = R_rows(R) + R_rows(kept) + pP_rows * R_rows(freed)
        # also kept units that are in R are already counted in R (disjoint by construction: R excludes M | H4)
        left = N - dropped
        lo = N - (R_rows(R) + R_rows(kept) + R_rows(freed))        # every freed unit is also an other-target hit
        hi = N - (R_rows(R) + R_rows(kept))                         # no freed unit is an other-target hit
        return {"rows_left": round(left), "low": round(lo), "high": round(hi), "freed_units": len(freed),
                "freed_rows": R_rows(freed)}

    sc = {}
    sc["now"] = scenario(M, H4)
    forced = set(keep["forced_binding"])
    sc["i_a54_precondition_met"] = scenario(forced, H4)
    sc["i_clean_dev_ceiling"] = scenario(set(), H4)
    fs = keep.get("freed_sets") or {}
    if fs:
        sc["i_x_numerals_disjoint_in_dev"] = scenario(M - fs["numerals_disjoint"], H4)
        sc["i_x_rule_lexicon_forms_and_numerals_dev_only"] = scenario(M - fs["lexicon_and_numerals"], H4)
        sc["i_x_all_pool_groups_and_numerals_dev_only"] = scenario(M - fs["any_pool_group_or_numerals"], H4)
    H4_vocab = H4 - fix_vocab_loose            # the colliding entries AND the pool records that embed them leave generation
    sc["ii_vocab_removed"] = scenario(M, H4_vocab)
    sc["i_a54_plus_ii"] = scenario(forced, H4_vocab)
    sc["i_clean_plus_ii"] = scenario(set(), H4_vocab)
    if fs:
        sc["i_x_rule_lexicon_forms_and_numerals_dev_only_plus_ii"] = scenario(M - fs["lexicon_and_numerals"], H4_vocab)
        sc["i_x_all_pool_groups_and_numerals_dev_only_plus_ii"] = scenario(M - fs["any_pool_group_or_numerals"], H4_vocab)
    out = {"left_now_log": left_now, "target": target, "shortfall": max(0, (target or 0) - left_now),
           "units": len(allu), "units_dropped": len(D), "R_only_other_targets_units": len(R), "R_rows": R_rows(R),
           "M_binding_units": len(M), "H4_ohs4_units": len(H4), "keyword_units": len(K),
           "keyword_units_vocab_fixable_strict": len(fix_vocab), "keyword_units_vocab_fixable_loose": len(fix_vocab_loose), "M_and_H4_units": len(M & H4),
           "p_other_target_hit_outside_units": round(pP, 4), "p_other_target_hit_outside_rows": round(pP_rows, 4),
           "scenarios": sc, "topup": {}}
    for nm, s in sc.items():
        surv = s["rows_left"] / N
        need = max(0, (target or 0) - s["rows_left"])
        out["topup"][nm] = {"survival_rate": round(surv, 4), "rows_needed_to_generate": (round(need / surv) if surv > 0 else None),
                            "rows_left_if_X_added": {str(x): round(s["rows_left"] + x * surv) for x in (500, 1000, 2000)}}
    return out


# ------------------------------------------------------------------------------------------------------------------------
def build_summary(out: dict) -> dict:
    B_ = out["blocks"]
    E = out["estimates"]
    K = out.get("keyword", {})
    tab = {}
    for B in A.BLOCKS:
        if B not in B_:
            continue
        b, e = B_[B], E[B]
        sc = e["scenarios"]
        g_ = lambda n: sc[n]["rows_left"] if n in sc else None  # noqa: E731
        x_ = lambda n: e["topup"][n]["rows_needed_to_generate"] if n in e["topup"] else None  # noqa: E731
        cls = b["c_provenance"]["units_with_class"] if b["c_provenance"]["units_with_class"] else None
        vs = (K.get(B) or {}).get("vocabulary_scan") or {}
        tab[B] = {
            "rows": b["rows"], "target": b["target"], "rows_left_now": e["left_now_log"], "shortfall": e["shortfall"],
            "units": b["units"], "units_dropped": e["units_dropped"],
            "c2_mixdev_binding_units": b["binding_units"], "c2_mixdev_binding_rows": b["binding_rows"],
            "binding_by_dev_file": b["a_dev_file"]["binding_units_by_dev_file"],
            "own_dev_rows_involved": f'{b["a_dev_file"]["dev_rows_involved"].get(B, 0)}/{b["a_dev_file"]["own_dev_rows"]}',
            "a53_precondition_ok": b["a53"]["precondition_ok"],
            "binding_unit_categories": b["binding_unit_categories"],
            "non_waived_item_classes_units": cls,
            "ohs4_keyword_units": e["keyword_units"], "keyword_vocab_stems": len(vs.get("stems", [])) if vs else None,
            "colliding_short_vocab_entries": vs.get("colliding_short_entries"),
            "rows_left": {"i_A54_as_defined": g_("i_a54_precondition_met"),
                          "i_x_numerals_dev_only": g_("i_x_numerals_disjoint_in_dev"),
                          "i_x_rule_forms_and_numerals_dev_only": g_("i_x_rule_lexicon_forms_and_numerals_dev_only"),
                          "i_ceiling_dev_clean": g_("i_clean_dev_ceiling"),
                          "ii_colliding_vocab_removed": g_("ii_vocab_removed"),
                          "i_A54_plus_ii": g_("i_a54_plus_ii"),
                          "i_x_rule_forms_numerals_plus_ii": g_("i_x_rule_lexicon_forms_and_numerals_dev_only_plus_ii"),
                          "i_ceiling_plus_ii": g_("i_clean_plus_ii")},
            "iii_topup_rows_to_generate_to_reach_target": {"now": x_("now"), "after_i_A54": x_("i_a54_precondition_met"),
                                                           "after_ii": x_("ii_vocab_removed"),
                                                           "after_i_x_numerals": x_("i_x_numerals_disjoint_in_dev"),
                                                           "after_i_x_rule_forms_numerals": x_("i_x_rule_lexicon_forms_and_numerals_dev_only")},
            "survival_rate_now": e["topup"]["now"]["survival_rate"]}
    return tab


def lexicon_holdout_facts() -> dict:
    """Per program family: lexicon forms by kind and held_out flag (pools_v2 / pools lexicon.json): which kinds have dev-only forms."""
    out = {}
    for B in PROGRAM_BLOCKS:
        root = X.block_dir(B)
        pdir = root / "pools_v2" if (root / "pools_v2").is_dir() else root / "pools"
        p = pdir / "lexicon.json"
        if X.resolved_refusal(p) or not p.is_file():
            out[B] = None
            continue
        j = json.loads(p.read_text(encoding="utf-8"))
        forms = j.get("forms") or []
        c = Counter((f.get("kind"), bool(f.get("held_out"))) for f in forms)
        out[B] = {"forms": len(forms), "by_kind": {k: {"held_out": c.get((k, True), 0), "training": c.get((k, False), 0)}
                                                   for k in sorted({k for k, _ in c}, key=str)}}
    return out


def root_causes(out: dict) -> list:
    """Root causes with the numbers behind them (all read from this run's own results)."""
    Bk, E, K = out["blocks"], out["estimates"], out["keyword"]
    sh = ["T24", "T06", "T07", "T23", "T26", "T28", "T12", "T25"]

    def own(B):
        f = Bk[B]["a_dev_file"]["binding_units_by_dev_file"]
        return f"{f.get(B, 0)}/{Bk[B]['binding_units']}"
    rc = []
    rc.append({
        "id": "RC1_own_mixdev",
        "title": "The binding c2_mixdev hits come from the family's OWN mixdev, spread over nearly all of its dev rows",
        "evidence": {
            "binding units hit by the own-family mixdev / all binding units": {B: own(B) for B in sh},
            "other-family files (units): ": {B: {f: n for f, n in Bk[B]["a_dev_file"]["binding_units_by_dev_file"].items() if f != B}
                                            for B in A.BLOCKS if B in Bk and any(f != B for f in Bk[B]["a_dev_file"]["binding_units_by_dev_file"])},
            "own dev rows involved (of 150)": {B: Bk[B]["a_dev_file"]["dev_rows_involved"].get(B, 0) for B in sh},
            "dev rows needed to explain the binding units (greedy)": {B: Bk[B]["a_dev_file"]["dev_rows_to_cover_binding"] for B in ("T24", "T06", "T07", "T23")}},
        "meaning": "Replacing or rebuilding a few dev rows (or another family's mixdev) cannot fix T24 / T06 / T23 / T07: 77-99% of their dev rows "
                   "share a non-waivable item with the candidates, and no small set of dev rows explains the binding units. GW's hits are "
                   "all from the GB mixdev (432 of 435 units), the only real cross-family case."})
    rc.append({
        "id": "RC2_A54_already_met",
        "title": "A53 / A54 is already satisfied (or inapplicable) for every family except T25: an A54-style rebuild gains nothing there",
        "evidence": {"A53 precondition shared values (skin/wording/card/pack/register)":
                     {B: Bk[B]["a53"]["shared_values"] for B in sh},
                     "units waived by A53 / binding": {B: [Bk[B]["a53"]["units_waived"], Bk[B]["binding_units"]] for B in sh}},
        "meaning": "T24, T06, T07, T23, T26, T28, T12 already have disjoint skins, wordings, cards, packs and registers between dev and "
                   "candidates. The binding residue is therefore made of asset kinds A54 does not cover. Only T25 fails the precondition."})
    rc.append({
        "id": "RC3_what_the_residue_is",
        "title": "What the non-waived shared items are made of (distinct items, class of the tiling)",
        "evidence": {B: {"items": Bk[B]["c_provenance"]["distinct_cause_items"],
                         "items_by_class": Bk[B]["c_provenance"]["items_by_class"],
                         "items_with_rendered_numeral_or_id": Bk[B]["c_provenance"]["items_containing_a_numeral_or_short_id"],
                         "units_freed_if_numerals_dev_only": Bk[B]["c_provenance"]["units_freed_if_held_out_diagnostic"]["numerals_disjoint"]["units"],
                         "units_freed_if_rule_forms_and_numerals_dev_only": Bk[B]["c_provenance"]["units_freed_if_held_out_diagnostic"]["lexicon_and_numerals"]["units"],
                         "binding_units": Bk[B]["binding_units"]} for B in sh if B != "T25"},
        "meaning": "frame_values = program-literal frames with rendered numerals / ids (A53 (C) tiles words, not numerals, and (A) needs the item in >= 5 distinct "
                   "cards / packs, which a numeral-bearing line rarely is); lexicon_template = rule/clause lexicon forms (comparator, window, "
                   "precedence ...) and question-wording forms; prose = stock phrases that several skins / documents / attack lines share; "
                   "pack_vocab = pack field names and entities common to several packs; mixed = needs two of those; residual = program-composed words "
                   "(inflections, number words, dates). Never an exact whole-row duplicate: no candidate row equals a dev row in any T block."})
    rc.append({
        "id": "RC4_rule_forms_not_held_out",
        "title": "Rule / clause lexicon forms are never dev-only: only question wordings carry a held_out flag",
        "evidence": {"lexicon forms by kind and held_out (held_out/training)": {B: v["by_kind"] for B, v in out["lexicon_holdout_by_family"].items()
                                                                                if v and B in sh},
                     "dev rule forms also used by candidates": {B: [Bk[B]["c_provenance"]["lexicon_form_overlap_dev_vs_candidates"]["dev_rule_forms_shared"],
                                                                   Bk[B]["c_provenance"]["lexicon_form_overlap_dev_vs_candidates"]["dev_rule_forms"]]
                                                               for B in sh if Bk[B]["c_provenance"]["lexicon_form_overlap_dev_vs_candidates"]},
                     "lexicon_template items by kind": {B: Bk[B]["c_provenance"]["lexicon_template_items_by_kind"] for B in ("T24", "T07", "T06")}},
        "meaning": "The S5 sampler holds out question wordings (and skins, packs, cards, registers) but draws rule / clause forms from the same pool as "
                   "training: 100% of the dev rows' rule forms also occur in candidates. This is the main reason T24 (323 of 893 binding items) and T07 "
                   "(122 of 278) stay binding."})
    rc.append({
        "id": "RC5_T25_constants_and_precondition",
        "title": "T25: 320 exact_full units are two program constants; A53 would waive them but the precondition fails (no held-out wordings)",
        "evidence": out.get("T25_exact_full", {}),
        "meaning": "No seed / RNG / pool overlap. After the precondition is met only 19 of 433 binding units remain. Without it every T25 row offering the "
                   "abstain answer is dropped (356 of 356 choice rows offering it; 113 of 113 with abstain as gold): a plain top-up would regenerate a "
                   "family with no abstain class."})
    rc.append({
        "id": "RC6_keyword_stems",
        "title": "ohs4_hash keyword: a handful of single-word name stems in our own vocabulary lists",
        "evidence": {B: {"keyword_units": K[B]["keyword_units"], "distinct_stems_in_rows": K[B]["distinct_hit_runs"],
                         "colliding_short_vocab_entries_by_list": [(l["file"], l["list_or_key"], l["entries"])
                                                                   for l in K[B]["vocabulary_scan"]["colliding_short_entries_by_list"][:6]]}
                     for B in ("T28", "T12", "T07", "T25", "T30", "T06", "T15") if B in K},
        "meaning": "43 distinct stems (of the 244 sealed keywords) recur across the blocks: names such as the animal / plant / place stems our generators and "
                   "OHS-4's authors both favour. Each family's hits trace to 1-10 stems in a few lists (see vocabulary_scan). No other check fires on vocabulary: "
                   "g13_ohs4_check on 34,169 vocabulary strings returned 0 hits."})
    rc.append({
        "id": "RC7_GB_GW",
        "title": "GB / GW: shared source cards and passages (not a program-vocabulary problem)",
        "evidence": {"GB": Bk["GB"].get("real_text_overlap"), "GW": Bk["GW"].get("real_text_overlap"),
                     "GW whole-row / state-text duplicates of a GB dev row": [Bk["GW"]["d_whole_row"]["candidate_units_with_whole_row_duplicate_of_a_dev_row"],
                                                                              Bk["GW"]["d_whole_row"]["candidate_units_with_state_text_equal_to_a_dev_state"]]},
        "meaning": "GB's mixdev (S5) is drawn from the same cards as its training rows (card stem + domain shared in 1171 of 1302 binding units; 788 units carry "
                   "a fixed per-card option label that is dropped for good). GW's 435 binding units all come from GB dev passages. MD has no c2_mixdev hit."})
    return rc


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--blocks", nargs="*", default=A.BLOCKS)
    ap.add_argument("--out", default=str(OUT_DEFAULT))
    ap.add_argument("--no-vocab", action="store_true")
    a = ap.parse_args(argv)
    t0 = time.time()
    files, drec = A.batch4_dev_files()
    dev, fam_of = A.load_dev(files)
    st = A.a53_state(dev)
    dev_inv = A.dev_item_index(dev)
    ex = X.Exports()
    out = {"method": __doc__, "dev_set_batch4": {f: {k: v for k, v in r.items()} for f, r in drec.items()},
           "dev_rows_per_file": {f: len(r) for f, r in dev.items()}, "blocks": {}, "estimates": {}, "keyword": {}}
    keeps, kws = {}, {}
    vocab_texts = []
    for B in a.blocks:
        res, keep = attribute_block(B, dev, dev_inv, st)
        out["blocks"][B] = res
        keeps[B] = keep
        print(f"[{B}] binding {res['binding_units']}/{res['units']} units, verified={res['verified_against_logs']} ({res['wall_s']}s)", flush=True)
        if not a.no_vocab:
            kw = keyword_block(B, ex)
            kws[B] = kw
            out["keyword"][B] = {k: v for k, v in kw.items() if k not in ("unit_runs", "all_ohs4_units", "kwu", "runs")}
            out["keyword"][B]["runs"] = [{k: v for k, v in r.items() if k != "_run"} for r in kw["runs"]]
            vs = vocab_scan(B, ex, {r["run_id"]: r["units"] for r in out["keyword"][B]["runs"]})
            vocab_texts += vs.pop("entries_scanned_for_runchecker")
            out["keyword"][B]["vocabulary_scan"] = vs
    if vocab_texts:
        out["vocab_runchecker"] = runchecker_on_vocab(vocab_texts)
        stem_blocks = defaultdict(lambda: {"blocks": {}, "batch4_units": 0})
        for B, k in out["keyword"].items():
            for r in k["runs"]:
                e = stem_blocks[r["run_id"]]
                e["blocks"][B] = r["units"]
                e["batch4_units"] += r["units"]
            for st_ in k["vocabulary_scan"]["stems"]:
                stem_blocks[st_]["blocks"].setdefault(B, 0)
        out["stems_across_blocks"] = {"distinct_stems": len(stem_blocks),
                                      "stems": [{"stem_id": k, **v} for k, v in sorted(stem_blocks.items(), key=lambda x: -x[1]["batch4_units"])]}
    if "T25" in a.blocks:
        out["T25_exact_full"] = t25_exact_full(dev, dev_inv, keeps["T25"])
    for B in a.blocks:
        out["estimates"][B] = estimate_block(B, out["blocks"][B], keeps[B], kws.get(B), A.log_of(B))
    urecs = []
    for B in a.blocks:
        byk = {r["unit"]: r for r in keeps[B]["unit_records"]}
        kw = kws.get(B)
        kwunits = set(kw["kwu"]) if kw else set()
        h4units = set(kw["all_ohs4_units"]) if kw else set()
        for k in sorted(set(byk) | h4units):
            r = byk.get(k) or {"block": B, "unit": k, "rows": keeps[B]["umap_rows"][k]}
            r = dict(r)
            r["c2_mixdev_binding"] = k in byk
            r["ohs4_hash_hit"] = k in h4units
            r["ohs4_keyword"] = k in kwunits
            r["ohs4_keyword_stems"] = sorted(h8(x) for x in (kw["unit_runs"].get(k, ()) if kw else ()))
            urecs.append(r)
    upath = Path(a.out).resolve().with_name("g13_attr_units.jsonl")
    upath.write_text("\n".join(json.dumps(r, default=lambda o: sorted(o) if isinstance(o, set) else str(o)) for r in urecs) + "\n")
    out["units_file"] = {"path": str(upath.relative_to(A.LEAN)), "records": len(urecs),
                         "note": "one line per candidate unit (call_id) hit by a binding c2_mixdev item or an ohs4_hash method in batch 4; C2 ids and counts only"}
    out["verified_against_logs_all"] = all(r["verified_against_logs"] for r in out["blocks"].values())
    out["lexicon_holdout_by_family"] = lexicon_holdout_facts()
    out["summary_table"] = build_summary(out)
    out["root_causes"] = root_causes(out)
    out["wall_s"] = round(time.time() - t0, 1)
    Path(a.out).write_text(json.dumps(out, indent=1, default=lambda o: sorted(o) if isinstance(o, set) else str(o)))
    print("wrote", a.out, "all verified:", out["verified_against_logs_all"], f"{out['wall_s']}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
