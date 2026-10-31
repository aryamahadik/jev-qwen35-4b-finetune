"""label_audit.py: SPEC.md section 8.6 (FINETUNE_PLAN 3.4 applied to the exact-label generators) on the 4B-E teacher
labels in data/v14_parts/train_2b_golden_kd.jsonl (built by build_2b_kd.py from the merged
data/v14_label_shards/labels_q35_4b_pxE). Read only; writes yn2b/label_audit.json (numbers) and, with --samples, a
JSONL of the audited rows for the reviewer (put it in a scratch folder: it holds golden_train text).

1. Per generator source (the teacher_gate_2b scope): teacher error rate of the raw 4B-E read (meta.teacher4b) and of
   the trained-on teacher (meta.teacher, after complement symmetrisation), and the share of the 2B's yes/no kd-0.5
   targets inside JevBench's abstain zone (0.2, 0.8) before and after the gate.
2. The 30-row audit: per generator, 30 teacher-vs-gold disagreements (20 yes/no + 10 choice, seeded; base rows only:
   roles aff / choice with the raw-row id r_gd_<key>_<k>, so near-miss bundles, definition swaps and attacked twins
   stay out, FINETUNE_PLAN 3.4). Each row is traced back to its raw row (data/v14_parts/raw/<key>.jsonl line k): the
   golden text and gold must match the raw row, and the gold is RE-DERIVED with the generator's own second
   implementation:
     gen_numeric_dates      nd schema preds / preds2 / val2 / catv2 from meta.orig_label.facts (gen_numeric_dates.recheck)
     gen_evidence_conflict  ec_verify.independent_gold + check_text from meta.orig_label.case
     gen_tables             the generator is replayed in memory (seed 20261140) up to the sampled pairs; every replayed
                            row must equal the raw row, then tab_verify.check_row re-parses the rendered table
     gen_policy_exceptions  replayed in memory the same way (seed of the module), then its recheck() (outcomes2)
   Nothing is written by the generator modules: only their functions are called (never main()).

  ../.venv/bin/python yn2b/label_audit.py --samples /path/to/scratch/label_audit_samples.jsonl
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yn2b_common as yc  # noqa: E402
from build_2b_kd import gives_gold  # noqa: E402
from teacher_gate_2b import in_scope, mid, source_in_scope, yn_target  # noqa: E402

GEN = yc.LEAN / "golden_src" / "gen"
RAW = yc.DATA / "v14_parts" / "raw"
AUDIT = ("gen_numeric_dates", "gen_evidence_conflict", "gen_tables", "gen_policy_exceptions")  # 8.6's 3 + 2.6's 4th
SEED = 20261001


# ------------------------------------------------------------------------------------------------ 1. statistics
def teacher_stats(rows_iter, teacher_src=yc.TEACHER_SRC, kd=0.5):
    by = defaultdict(Counter)
    for r in rows_iter:
        s, q = r["source"], r["qtype"]
        if not source_in_scope(s, q) and not s.startswith("gd_gen"):
            continue
        m = r.get("meta") or {}
        b = by[(s, q)]
        b["rows"] += 1
        if q == "noul":
            b["mid_all_rows"] += mid(yn_target(r, kd, True))
        if not in_scope(r, teacher_src):
            continue
        t, t4 = yc.kd_target(r), m.get("teacher4b")
        b["fresh"] += 1
        wrong = not gives_gold(r, t)
        b["wrong_final"] += wrong
        b["wrong_raw"] += (t4 is not None) and not gives_gold(r, t4)
        if q == "noul":
            y0 = yn_target(r, kd, True)
            y1 = yn_target(r, kd, not wrong)
            b["mid_before"] += mid(y0)
            b["mid_after"] += mid(y1)
            b["mid_after_all_rows"] += mid(y1)
    for (s, q), b in by.items():
        if q == "noul":
            b["mid_after_all_rows"] += b["mid_all_rows"] - b["mid_before"]  # rows outside the scope do not change
    out = {}
    for (s, q), b in sorted(by.items()):
        f = b["fresh"] or 1
        d = {"rows": b["rows"], "fresh_teacher": b["fresh"], "teacher_wrong_raw": round(b["wrong_raw"] / f, 4),
             "teacher_wrong_trained": round(b["wrong_final"] / f, 4), "n_wrong_trained": b["wrong_final"]}
        if q == "noul":
            d.update({"mid_before": round(b["mid_before"] / f, 4), "mid_after": round(b["mid_after"] / f, 4),
                      "mid_all_rows_before": round(b["mid_all_rows"] / (b["rows"] or 1), 4),
                      "mid_all_rows_after": round(b["mid_after_all_rows"] / (b["rows"] or 1), 4)})
        out[f"{s}|{q}"] = d
    return out, by


def pooled(by, pred):
    t = Counter()
    for (s, q), b in by.items():
        if pred(s, q):
            t.update(b)
    f = t["fresh"] or 1
    return {"rows": t["rows"], "fresh_teacher": t["fresh"], "teacher_wrong_raw": round(t["wrong_raw"] / f, 4),
            "teacher_wrong_trained": round(t["wrong_final"] / f, 4),
            **({"mid_before": round(t["mid_before"] / f, 4), "mid_after": round(t["mid_after"] / f, 4),
                "mid_all_rows_before": round(t["mid_all_rows"] / (t["rows"] or 1), 4),
                "mid_all_rows_after": round(t["mid_after_all_rows"] / (t["rows"] or 1), 4)} if t["mid_all_rows"] else {})}


# ------------------------------------------------------------------------------------------------ 2. sample
def base_index(r, key):
    """k of a base golden row r_gd_<key>_<k> (None for bundles, swaps, attacks)."""
    pre = f"r_gd_{key}_"
    tail = r["id"][len(pre):] if r["id"].startswith(pre) else ""
    return int(tail) if tail.isdigit() and r.get("role") in ("aff", "choice") else None


def sample(rows_iter, keys=AUDIT, n_yn=20, n_ch=10, seed=SEED, teacher_src=yc.TEACHER_SRC):
    pool = defaultdict(list)
    for r in rows_iter:
        key = r["source"][3:] if r["source"].startswith("gd_") else None
        if key not in keys or not in_scope(r, teacher_src) or base_index(r, key) is None:
            continue
        if not gives_gold(r, yc.kd_target(r)):
            pool[(key, r["qtype"])].append(r)
    out = {}
    for key in keys:
        rng = random.Random(f"{seed}:{key}")
        yn = sorted(pool[(key, "noul")], key=lambda r: r["id"])
        ch = sorted(pool[(key, "choice")], key=lambda r: r["id"])
        k_ch = min(n_ch, len(ch))
        k_yn = min(n_yn + n_ch - k_ch, len(yn))
        out[key] = {"pool_yes_no": len(yn), "pool_choice": len(ch),
                    "rows": rng.sample(yn, k_yn) + rng.sample(ch, k_ch)}
    return out


# ------------------------------------------------------------------------------------------------ 3. re-derivation
def raw_rows(key, idx):
    want, got = set(idx), {}
    with open(RAW / f"{key}.jsonl", encoding="utf-8") as f:
        for k, line in enumerate(f):
            if k in want:
                got[k] = json.loads(line)
    return got


def golden_matches_raw(g, raw):
    """The golden row is the raw row as assembled by build_v14_golden (text unchanged, gold mapped)."""
    if g["state"] != raw["state"] or g["instructions"] != raw["instructions"]:
        return False, "text differs from the raw row"
    if g["qtype"] == "noul":
        return (g["gold"] == 1) == (str(raw["gold"]).lower() == "yes"), "yes/no gold differs from the raw gold"
    ro = list(raw["options"])
    if len(ro) != len(g["options"]) or raw["gold"] not in ro:
        return False, "options differ from the raw row"
    return g["options"].index(g["gold"]) == ro.index(raw["gold"]), "choice gold differs from the raw gold"


def _gen_path():
    for p in (str(GEN), str(yc.LEAN / "golden_src" / "moral_social_norms")):
        if p not in sys.path:
            sys.path.insert(0, p)


def rederive_numeric_dates(raws):
    _gen_path()
    import gen_numeric_dates as g
    out = {}
    for k, r in raws.items():
        try:
            o = r["meta"]["orig_label"]
            s = g.SCHEMA_BY_NAME[o["schema"]]
            f = o["facts"]
            g.Builder.agree(s, f)
            assert r["state"].startswith(s.render(f)), "facts do not re-render to the state"
            q = o["qid"]
            if q in ("pos", "neg", "est", "claim"):
                v, v2 = s.preds(f)[o["pred"]], s.preds2(f)[o["pred"]]
                assert v == v2, "the two implementations disagree"
                exp = {"pos": v is True, "neg": v is False, "est": v is True,
                       "claim": v is not None and v == o.get("claim_pol")}[q]
                want = "yes" if exp else "no"
            elif q == "letter":
                w1, w2 = s.fmtv(f, s.val(f)), s.fmtv(f, s.val2(f))
                assert w1 == w2, "the two implementations disagree"
                assert o["options"].count(w1) == 1
                want = g.LETTERS[o["options"].index(w1)]
            else:
                w1, w2 = s.catv(f), s.catv2(f)
                assert w1 == w2, "the two implementations disagree"
                want = w1
            out[k] = ("ok" if want == r["gold"] else "MISMATCH", f"re-derived {want!r}, raw gold {r['gold']!r}")
        except Exception as e:  # noqa: BLE001
            out[k] = ("ERROR", repr(e)[:200])
    return out


def rederive_evidence_conflict(raws):
    _gen_path()
    import ec_verify as v
    out = {}
    for k, r in raws.items():
        try:
            case = v.restore_case(r["meta"]["orig_label"]["case"])
            want = v.independent_gold(case)
            v.check_text(case, r)
            out[k] = ("ok" if want == r["gold"] else "MISMATCH", f"re-derived {want!r}, raw gold {r['gold']!r}")
        except Exception as e:  # noqa: BLE001
            out[k] = ("ERROR", repr(e)[:200])
    return out


def _same(a, b):
    return all(a[x] == b[x] for x in ("rid", "state", "instructions", "options", "gold"))


def replay_tables(need_rids, raw_by_rid, limit_pairs=None):
    """gen_tables.main()'s loop without any write; stops once every needed rid is replayed. Returns ({rid: (P, j)},
    rows compared, first mismatch or None)."""
    _gen_path()
    import gen_tables as g
    rng = random.Random(g.SEED)
    qids = list(g.QID_W)
    seen_state, seen_key = set(), set()
    need, found, compared, idx = set(need_rids), {}, 0, 0
    raw_list = raw_by_rid["__list__"]
    while need - set(found) and idx < (limit_pairs or g.N_PAIRS):
        qid = rng.choices(qids, weights=[g.QID_W[q] for q in qids])[0]
        dom = g.choose_domain(rng, qid)
        if qid == "pick":
            P = g.pick_pair(rng, dom)
        elif qid in ("answer", "answer_wrong"):
            P = g.answer_pair(rng, qid, dom)
        else:
            P = g.claim_pair(rng, qid, dom)
        if P is None:
            continue
        g.recheck(P)
        rr = g.render_pair(P, rng, idx)
        ks = [g.norm(r["state"]) + "||" + g.norm(r["instructions"]) for r in rr]
        if rr[0]["state"] == rr[1]["state"] and rr[0]["instructions"] == rr[1]["instructions"]:
            continue
        if any(k in seen_key for k in ks) or any(g.norm(r["state"]) in seen_state for r in rr):
            continue
        seen_key.update(ks)
        seen_state.update(g.norm(r["state"]) for r in rr)
        P["rows"] = rr
        for j, r in enumerate(rr):
            ref = raw_list[2 * idx + j]
            compared += 1
            if not _same(r, ref):
                return found, compared, f"replayed row {r['rid']} differs from raw line {2 * idx + j}"
            if r["rid"] in need:
                found[r["rid"]] = (P, j)
        idx += 1
    return found, compared, None


def rederive_tables(raws):
    _gen_path()
    import tab_verify as tv
    raw_list = [json.loads(l) for l in open(RAW / "gen_tables.jsonl", encoding="utf-8")]
    rid_of = {k: r["rid"] for k, r in raws.items()}
    found, compared, err = replay_tables(set(rid_of.values()), {"__list__": raw_list})
    out = {}
    for k, r in raws.items():
        if err:
            out[k] = ("ERROR", f"replay stopped: {err}")
            continue
        if r["rid"] not in found:
            out[k] = ("ERROR", "not reached by the replay")
            continue
        P, j = found[r["rid"]]
        try:
            ok, v = tv.check_row(P, j)
            out[k] = ("ok" if ok else "MISMATCH", f"tab_verify verdict {v!r}, raw gold {r['gold']!r}")
        except Exception as e:  # noqa: BLE001
            out[k] = ("ERROR", repr(e)[:200])
    return out, {"replayed_rows_compared_to_raw": compared, "replay_error": err}


def replay_policy_exceptions(need_rids, raw_list):
    _gen_path()
    import gen_policy_exceptions as g
    rng = random.Random(g.SEED)
    bal = g.Balancer()
    seen, found, compared, pos = set(), {}, 0, 0
    need = set(need_rids)
    per_dom = g.N_PAIRS // len(g.DOMAINS)
    extra = g.N_PAIRS - per_dom * len(g.DOMAINS)
    idx = 0
    for di, D in enumerate(g.DOMAINS):
        if not need - set(found):
            break
        quota = per_dom + (1 if di < extra else 0)
        made = 0
        while made < quota:
            multi = rng.random() < 0.45
            qid = g.wchoice(rng, g.MUL_Q if multi else g.BIN_Q)
            pr = g.make_pair(D, rng, multi, qid, bal, idx)
            if pr is None:
                continue
            k0 = g.norm(pr[0]["state"]) + "||" + g.norm(pr[0]["instructions"])
            k1 = g.norm(pr[1]["state"]) + "||" + g.norm(pr[1]["instructions"])
            if k0 in seen or k1 in seen or k0 == k1:
                continue
            seen.update({k0, k1})
            for r in pr:
                ref = raw_list[pos]
                compared += 1
                if not _same(r, ref):
                    return found, compared, f"replayed row {r['rid']} differs from raw line {pos}", g
                if r["rid"] in need:
                    found[r["rid"]] = r
                pos += 1
            made += 1
            idx += 1
    return found, compared, None, g


def rederive_policy_exceptions(raws):
    raw_list = [json.loads(l) for l in open(RAW / "gen_policy_exceptions.jsonl", encoding="utf-8")]
    found, compared, err, g = replay_policy_exceptions({r["rid"] for r in raws.values()}, raw_list)
    out = {}
    for k, r in raws.items():
        if err:
            out[k] = ("ERROR", f"replay stopped: {err}")
        elif r["rid"] not in found:
            out[k] = ("ERROR", "not reached by the replay")
        else:
            try:
                g.recheck(found[r["rid"]])
                out[k] = ("ok", "outcomes2 re-derives the raw gold; shown facts verified in the text")
            except AssertionError as e:
                out[k] = ("MISMATCH", repr(e)[:200])
            except Exception as e:  # noqa: BLE001
                out[k] = ("ERROR", repr(e)[:200])
    return out, {"replayed_rows_compared_to_raw": compared, "replay_error": err}


REDERIVE = {"gen_numeric_dates": rederive_numeric_dates, "gen_evidence_conflict": rederive_evidence_conflict,
            "gen_tables": rederive_tables, "gen_policy_exceptions": rederive_policy_exceptions}


def audit_key(key, rows):
    idx = {base_index(r, key): r for r in rows}
    raws = raw_rows(key, idx)
    res = REDERIVE[key](raws)
    info = {}
    if isinstance(res, tuple):
        res, info = res
    items = []
    for k, g in sorted(idx.items()):
        raw = raws.get(k)
        match, why = golden_matches_raw(g, raw) if raw else (False, "raw row missing")
        st, detail = res.get(k, ("ERROR", "no result"))
        t, t4 = yc.kd_target(g), (g.get("meta") or {}).get("teacher4b")
        p_gold = (float(t["yes"]) if g["gold"] == 1 else 1 - float(t["yes"])) if g["qtype"] == "noul" \
            else float(t.get(g["gold"], 0.0))
        items.append({"id": g["id"], "raw_line": k, "rid": raw["rid"] if raw else None,
                      "config": (raw or {}).get("meta", {}).get("config"), "qtype": g["qtype"], "gold": g["gold"],
                      "teacher_p_gold": round(p_gold, 4), "teacher4b": t4, "golden_equals_raw": match,
                      "golden_check": None if match else why, "rederive": st, "rederive_detail": detail})
    n_ok = sum(x["rederive"] == "ok" and x["golden_equals_raw"] for x in items)
    return {"n": len(items), "program_correct": n_ok, "items": items, **info}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--kd-file", default=str(yc.DATA / "v14_parts/train_2b_golden_kd.jsonl"))
    ap.add_argument("--teacher-src", default=yc.TEACHER_SRC)
    ap.add_argument("--out", default=str(yc.YN2B / "label_audit.json"))
    ap.add_argument("--samples", default="", help="also write the audited rows (golden text) here, e.g. a scratch path")
    ap.add_argument("--keys", default=",".join(AUDIT))
    ap.add_argument("--overwrite", action="store_true")
    a = ap.parse_args(argv)
    keys = tuple(k for k in a.keys.split(",") if k)
    out = yc.guard_out(a.out, inputs=(a.kd_file,), overwrite=a.overwrite)
    stats, by = teacher_stats(yc.iter_jsonl(a.kd_file), a.teacher_src)
    res = {"kd_file": yc._rel(Path(a.kd_file)), "kd_file_sha256": yc.sha256_file(a.kd_file),
           "teacher_src": a.teacher_src, "by_source": stats,
           "pooled_gate_scope_yes_no": pooled(by, lambda s, q: q == "noul" and source_in_scope(s, q)),
           "pooled_gate_scope_choice": pooled(by, lambda s, q: q == "choice" and source_in_scope(s, q)),
           "pooled_gd_gen_yes_no": pooled(by, lambda s, q: q == "noul" and s.startswith("gd_gen_")),
           "audit": {}}
    smp = sample(yc.iter_jsonl(a.kd_file), keys, teacher_src=a.teacher_src)
    for key in keys:
        r = audit_key(key, smp[key]["rows"])
        r.update(pool_yes_no=smp[key]["pool_yes_no"], pool_choice=smp[key]["pool_choice"])
        res["audit"][key] = r
        print(f"{key}: {r['program_correct']}/{r['n']} program-verified "
              f"(pool {r['pool_yes_no']} yes/no + {r['pool_choice']} choice disagreements)", flush=True)
    yc.write_json(out, res)
    if a.samples:
        sp = yc.guard_out(a.samples, overwrite=a.overwrite)
        yc.write_rows(sp, [dict(r, _audit_key=k) for k in keys for r in smp[k]["rows"]])
    print(json.dumps({k: v for k, v in res.items() if k.startswith("pooled")}, indent=1))
    return res


if __name__ == "__main__":
    main()
