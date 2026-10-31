"""assemble_yn2b.py: raw yn2b rows -> the golden row format the trainer reads (SPEC.md sections 4.4, 4.5, 4.9, 4.10, 9).

The raw format and the row conversion belong to golden_src/gen3/mv_core.py (builder A): this tool finds the raw files
where mv_core.FamilyBuilder.write() puts them (mv_core.raw_paths: yn2b_raw/<key>.jsonl + relations/<key>.jsonl,
yn2b_raw/dev/<key>.jsonl, yn2b_raw/dev/<key>__devx.jsonl and their relations), converts them with mv_core.assemble()
(ids, group / call ids, qtype noul with options null and gold 1/0, cards by card_style, option-line cards for choice
rows, no card on score / JB-letter rows, no teacher) and adds the file-level checks mv_core cannot make on one family:
  - --drop (check_yn2b.py's drop list: salted hashes of source:latent_id): those latent units are left out, with
    their relations;
  - --drop-views key:view,... : every raw row of that family with meta.view == view is left out, with its relations
    (a whole template view that fails a gate, e.g. 1 Oct: F3's 'ladder' view fails the SPEC 7.3 cue-share rule; the
    labels of the other rows do not depend on it). Reported per family as dropped_view_rows;
  - F4(a) rows (meta.derived_from): the golden base row exists in golden_train, shares the state, its group_id is
    meta.derived_group, and the row keeps the base row's dataset and licence (R1);
  - every card round-trips through decoder_io.card_defs (so no card line is silently dropped, SPEC F2), the marker rule
    (SPEC 4.8), relation golds per type, one complement per row, no latent on both sides of the train/dev split,
    unique ids across families, SPEC 4.9 unit sizes, train_decoder.check_rows(rows, kd=0.5).
Writes NEW files (SPEC 9): data/v14_parts/yn2b_train.jsonl, data/v14_parts/yn2b_relations.jsonl, data/yn2b_dev.jsonl,
data/yn2b_dev_relations.jsonl, data/yn2b_devx.jsonl (+ yn2b_devx_relations.jsonl when devx has relations), and their
sha256 in golden_src/gen3/MANIFEST_yn2b.jsonl. Every path is a flag. With --out-dev '' --out-dev-iid ...
--out-dev-holdout ... the dev rows are written as two files split by meta.dev_kind (owner decision on wave-1a issue 6:
top level only data/yn2b_dev_iid.jsonl, data/yn2b_dev_holdout.jsonl and data/yn2b_devx.jsonl; the train file, its
relations and the dev relations then go under data/v14_parts/yn2b_ab/, see the 1 Oct run below).

  ../.venv/bin/python yn2b/assemble_yn2b.py --drop data/v14_parts/yn2b_raw/yn2b_drop.json \
        --out-train v14_parts/yn2b_ab/yn2b_train.jsonl --out-rel v14_parts/yn2b_ab/yn2b_relations.jsonl \
        --out-dev '' --out-dev-iid yn2b_dev_iid.jsonl --out-dev-holdout yn2b_dev_holdout.jsonl \
        --out-dev-rel v14_parts/yn2b_ab/yn2b_dev_relations.jsonl --out-devx yn2b_devx.jsonl \
        --out-devx-rel v14_parts/yn2b_ab/yn2b_devx_relations.jsonl

  ../.venv/bin/python yn2b/assemble_yn2b.py --dry-run
  ../.venv/bin/python yn2b/assemble_yn2b.py --drop data/v14_parts/yn2b_raw/yn2b_drop.json [--families gen3_tool_guard,...]
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yn2b_common as yc  # noqa: E402

GEN3 = yc.GEN3
if str(GEN3) not in sys.path:
    sys.path.insert(0, str(GEN3))

REL_TYPES = ("complement", "equiv", "inv")
UNIT_MAX_CHARS, BIG_STATE, BIG_UNIT_MAX_ROWS = 24000, 6000, 3
PARTS = ("train", "dev", "devx")


def mv():
    import mv_core
    return mv_core


def discover(raw_dir, families=None):
    """{(key, part): (rows path, relations path)} for every raw file present."""
    raw_dir = Path(raw_dir)
    keys = {p.stem for p in raw_dir.glob("gen3_*.jsonl")}
    keys |= {p.stem.split("__")[0] for p in (raw_dir / "dev").glob("gen3_*.jsonl")} if (raw_dir / "dev").exists() else set()
    out = {}
    for key in sorted(keys):
        if families is not None and key not in families:
            continue
        for part in PARTS:
            rp, lp = mv().raw_paths(key, part, raw_dir)
            if rp.exists():
                out[(key, part)] = (rp, lp)
    return out


def unit_key_raw(r):
    return f"gd_{r['key']}:{r['meta'].get('latent_id')}"


def golden_bases(golden_path, ids):
    out, want = {}, set(ids)
    if not want or not golden_path or not Path(golden_path).exists():
        return out
    for r in yc.iter_jsonl(golden_path):
        if r["id"] in want:
            out[r["id"]] = r
            if len(out) == len(want):
                break
    return out


def check_f4a(raw_rows, bases):
    bad = []
    for r in raw_rows:
        m = r["meta"]
        b = m.get("derived_from")
        if not b:
            continue
        base = bases.get(b)
        if base is None:
            bad.append((r["rid"], "base row not in golden_train"))
        elif base["state"] != r["state"]:
            bad.append((r["rid"], "state differs from the base row"))
        elif m.get("derived_group") != base["group_id"]:
            bad.append((r["rid"], "derived_group is not the base row's group_id"))
        elif (m.get("dataset"), m.get("licence")) != ((base.get("meta") or {}).get("dataset"), (base.get("meta") or {}).get("licence")):
            bad.append((r["rid"], "dataset / licence differ from the base row (R1)"))
    if bad:
        raise AssertionError(f"{len(bad)} F4(a) row(s) fail the base-row checks: {bad[:5]}")


def noul_card_ok(keys) -> bool:
    """SPEC 2.3 / 4.4: decoder_io prints a yes/no row's card WHOLE as the trusted "Definitions:" block, so lines keyed
    by other names (F6's operative definition, F3's reference rules, F1b's rounding rules, F4's label bundle) are shown,
    not dropped. The card must define what yes AND no mean, in one case style only: lowercase `- yes:` / `- no:`, or
    `- Yes:` / `- No:` (which decoder_io also attaches to the Yes / No option lines; a lowercase card with a stray
    `Yes` / `No` key would attach a definition to one option only)."""
    keys = set(keys)
    lower, upper = {"yes", "no"}, {"Yes", "No"}
    return (lower <= keys and not keys & upper) or (upper <= keys and not keys & lower)


def check_cards(rows):
    import decoder_io
    bad = []
    for r in rows:
        c = r.get("card")
        if not c:
            continue
        got = decoder_io.card_defs(c)
        lines = [ln for ln in c.splitlines() if ln.strip()]
        if len(got) != len(lines):
            bad.append((r["id"], "a card line is not '- key: definition'"))
        elif r["qtype"] == "choice" and not set(got) <= set(r["options"]):
            bad.append((r["id"], "a choice card line keys no option"))
        elif r["qtype"] == "noul" and not noul_card_ok(got):
            bad.append((r["id"], "a yes/no card must define yes and no (one case style)"))
    if bad:
        raise AssertionError(f"{len(bad)} card(s) would lose lines in decoder_io: {bad[:5]}")


def check_relations(rows, rels):
    by = {r["id"]: r for r in rows}
    comp = Counter()
    for x in rels:
        a, b = by.get(x["a"]), by.get(x["b"])
        if x["type"] not in REL_TYPES:
            raise AssertionError(f"relation type {x['type']!r}")
        if a is None or b is None:
            raise AssertionError(f"relation {x} has a missing end")
        if a["call_id"] != b["call_id"]:
            raise AssertionError(f"relation {a['id']}/{b['id']} crosses units")
        if x["type"] == "complement":
            if a["qtype"] != "noul" or b["qtype"] != "noul" or a["gold"] + b["gold"] != 1:
                raise AssertionError(f"complement {a['id']}/{b['id']}: not a yes/no pair with golds summing to 1")
            comp[a["id"]] += 1
            comp[b["id"]] += 1
        elif a["qtype"] != b["qtype"] or a["gold"] != b["gold"]:
            raise AssertionError(f"{x['type']} {a['id']}/{b['id']}: qtype or gold differs")
        elif x["type"] == "inv" and b["role"] != "attacked":
            raise AssertionError(f"inv {a['id']}/{b['id']}: b must be the attacked row")
    multi = [i for i, n in comp.items() if n > 1]
    if multi:
        raise AssertionError(f"{len(multi)} row(s) in more than one complement relation: {multi[:5]}")


def check_units(rows):
    """SPEC 4.9 for the yn2b-only units (F4(a) rows join golden units: merge_yn2b checks those)."""
    units = defaultdict(list)
    for r in rows:
        if not r["meta"].get("derived_from"):
            units[r["call_id"]].append(r)
    bad = []
    for k, u in units.items():
        tot = sum(len(r["state"]) for r in u)
        if tot > UNIT_MAX_CHARS or (any(len(r["state"]) > BIG_STATE for r in u) and len(u) > BIG_UNIT_MAX_ROWS):
            bad.append((k, len(u), tot))
    if bad:
        raise AssertionError(f"{len(bad)} unit(s) break SPEC 4.9 (<= 24K state chars; > 6K state -> <= 3 rows): {bad[:3]}")


def parse_drop_views(text):
    """'gen3_state_track:ladder,gen3_x:jb' -> {("gen3_state_track", "ladder"), ...} (keys with or without gd_)."""
    out = set()
    for x in [y for y in (text or "").split(",") if y.strip()]:
        k, _, v = x.strip().partition(":")
        if not k or not v:
            raise ValueError(f"--drop-views takes key:view, got {x!r}")
        out.add((k[3:] if k.startswith("gd_") else k, v))
    return frozenset(out)


def assemble(raw_dir, defs_dir, drop=frozenset(), families=None, golden=None, drop_views=frozenset()):
    """Returns {"train", "train_rel", "dev", "dev_rel", "devx", "devx_rel", "report"}."""
    import check_yn2b
    m = mv()
    files = discover(raw_dir, families)
    out = {p: [] for p in PARTS}
    rels = {p: [] for p in PARTS}
    report = defaultdict(dict)
    raw_all = []
    for (key, part), (rp, lp) in files.items():
        raw = yc.read_jsonl(rp)
        rrel = yc.read_jsonl(lp) if lp.exists() else []
        keep = [r for r in raw if check_yn2b.drop_hash(unit_key_raw(r)) not in drop]
        n_unit = len(keep)
        keep = [r for r in keep if (key, r["meta"].get("view")) not in drop_views]
        raw_all += keep
        g_rows, g_rels = m.assemble(keep, rrel, lambda r: m.load_defs(r["key"], r["meta"].get("defs"), defs_dir))
        out[part] += g_rows
        rels[part] += g_rels
        yn = [r for r in g_rows if r["qtype"] == "noul"]
        report[part][f"gd_{key}"] = {"raw": len(raw), "dropped": len(raw) - len(keep),
                                     "dropped_view_rows": n_unit - len(keep), "rows": len(g_rows),
                                     "noul": len(yn), "choice": len(g_rows) - len(yn),
                                     "yes_share": round(sum(r["gold"] for r in yn) / len(yn), 4) if yn else None,
                                     "latents": len({r["meta"]["latent_id"] for r in g_rows}),
                                     "relations": dict(Counter(x["type"] for x in g_rels))}
    f4 = {r["meta"].get("derived_from") for r in raw_all} - {None}
    check_f4a(raw_all, golden_bases(golden, f4))
    allr = out["train"] + out["dev"] + out["devx"]
    ids = [r["id"] for r in allr]
    if len(ids) != len(set(ids)):
        raise AssertionError("duplicate assembled ids across files")
    lat = lambda rs: {(r["source"], r["meta"]["latent_id"]) for r in rs}  # noqa: E731
    both = lat(out["train"]) & (lat(out["dev"]) | lat(out["devx"]))
    if both or lat(out["dev"]) & lat(out["devx"]):
        raise AssertionError(f"latent(s) on both sides of a split: {sorted(both)[:3]}")
    for p in PARTS:
        check_relations(out[p], rels[p])
    check_cards(allr)
    test_fams = tuple(f"gd_{k}" for k in getattr(m, "_TEST_FAMILIES", {}))  # mv_core test families only (tests)
    mk = check_yn2b.marker_rule(allr, check_yn2b.SPOOF_FAMILIES + test_fams)
    if mk:
        raise AssertionError(f"marker rule (SPEC 4.8) broken: {mk[:5]}")
    check_units(out["train"])
    import train_decoder
    train_decoder.check_rows(allr, 0.5)
    return {"train": out["train"], "train_rel": rels["train"], "dev": out["dev"], "dev_rel": rels["dev"],
            "devx": out["devx"], "devx_rel": rels["devx"], "report": dict(report)}


def split_dev(dev_rows):
    """{"iid": rows, "holdout": rows} by meta.dev_kind (owner decision on wave-1a issue 6: the small dev files may be
    written at top level as data/yn2b_dev_iid.jsonl and data/yn2b_dev_holdout.jsonl). Every dev row must be one of the
    two; relations never cross them (a relation stays inside one latent unit, and a latent has one dev_kind)."""
    out = {"iid": [], "holdout": []}
    for r in dev_rows:
        k = (r.get("meta") or {}).get("dev_kind")
        if k not in out:
            raise AssertionError(f"dev row {r['id']} has dev_kind {k!r} (expected iid or holdout)")
        out[k].append(r)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--data-dir", default=str(yc.DATA))
    ap.add_argument("--raw-dir", default="v14_parts/yn2b_raw")
    ap.add_argument("--defs-dir", default="v14_parts/yn2b_defs")
    ap.add_argument("--golden", default="v14_parts/golden_train.jsonl", help="for F4(a) base rows ('' = none)")
    ap.add_argument("--drop", default="", help="check_yn2b.py drop list")
    ap.add_argument("--families", default="", help="comma list of keys (gen3_<name>) to include; default all")
    ap.add_argument("--drop-views", default="", help="comma list key:view of whole views to leave out (reported)")
    ap.add_argument("--out-train", default="v14_parts/yn2b_train.jsonl")
    ap.add_argument("--out-rel", default="v14_parts/yn2b_relations.jsonl")
    ap.add_argument("--out-dev", default="yn2b_dev.jsonl", help="all dev rows in one file ('' = not written)")
    ap.add_argument("--out-dev-iid", default="", help="dev rows with meta.dev_kind iid only ('' = not written)")
    ap.add_argument("--out-dev-holdout", default="", help="dev rows with meta.dev_kind holdout only ('' = not written)")
    ap.add_argument("--out-dev-rel", default="yn2b_dev_relations.jsonl")
    ap.add_argument("--out-devx", default="yn2b_devx.jsonl")
    ap.add_argument("--out-devx-rel", default="yn2b_devx_relations.jsonl", help="written only when devx has relations")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--overwrite", action="store_true")
    a = ap.parse_args(argv)
    dd = Path(a.data_dir)
    drop = frozenset(json.loads(Path(a.drop).read_text())["keys"]) if a.drop else frozenset()
    fams = {x for x in a.families.split(",") if x} or None
    dv = parse_drop_views(a.drop_views)
    res = assemble(dd / a.raw_dir, dd / a.defs_dir, drop, fams, dd / a.golden if a.golden else None, dv)
    split = split_dev(res["dev"])
    res["dev_iid"], res["dev_holdout"] = split["iid"], split["holdout"]
    print(json.dumps(res["report"], indent=1))
    print(json.dumps({k: len(v) for k, v in res.items() if k != "report"}))
    if a.dry_run:
        return res
    if bool(a.out_dev_iid) != bool(a.out_dev_holdout):
        ap.error("--out-dev-iid and --out-dev-holdout go together")
    if not (a.out_dev or a.out_dev_iid):
        ap.error("the dev rows need --out-dev, or both --out-dev-iid and --out-dev-holdout")
    outs = [("train", a.out_train), ("train_rel", a.out_rel)]
    outs += [("dev", a.out_dev)] if a.out_dev else []
    outs += [("dev_iid", a.out_dev_iid), ("dev_holdout", a.out_dev_holdout)] if a.out_dev_iid and a.out_dev_holdout else []
    outs += [("dev_rel", a.out_dev_rel), ("devx", a.out_devx)] + ([("devx_rel", a.out_devx_rel)] if res["devx_rel"] else [])
    paths = [(k, yc.guard_out(dd / p, overwrite=a.overwrite)) for k, p in outs]
    for k, path in paths:
        yc.write_rows(path, res[k])
    yc.manifest_outputs("yn2b/assemble_yn2b.py", [p for _, p in paths],
                        {"drop_units": len(drop), "drop_views": sorted(f"{k}:{v}" for k, v in dv) or None})
    for _, p in paths:
        print(f"wrote {yc._rel(p)}  sha256 {yc.sha256_file(p)}")
    return res


if __name__ == "__main__":
    main()
