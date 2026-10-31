"""replay_screen/pool.py: the A46 replay pool map and the screening population.

Inputs (all read-only): pool/draw_<r1>.json (from draw.py: the exact replay_sample.py draw at the C2 seed), the
golden_train pool (data/v14_parts/golden_train.jsonl), golden_src/MANIFEST.jsonl (label notes per golden source),
lean/build_*.py + golden_src/**/*.py (builders), data/v14_parts/raw/ (raw provenance files), c_spec/tools/make_replay_
register.py (read with ast by replay_sample.py: not re-read here).

Gold origin classes
  human    an upstream human label (annotators, exam-board answer keys, official record codes, crowd votes). Rows of
           tatqa / tathqa / finqa are mixed (yes rows = human gold answer, no rows = program-built wrong answers from
           the human derivation); they stay in scope because the human answer defines both labels.
  program  exact program or execution gold (this repo's generators, procedural pg_ rows, upstream synthetic benchmarks
           whose labels a program computes). Out of scope (their gates already ran).
  claude   Claude-written gold (binj_, std_, hard_, planted_, proc_). replay_sample.py drops these sources whole, so
           none is in the eligible pool; the class is kept so the map shows it.
Classification is by explicit rule (below) and the evidence is printed per source: MANIFEST note, meta.dataset, builder
files, raw file. replay_sample.PROGRAM_LABELLED (gd_gen*, pg_, judge_mathderiv, gd_babi_logic, gd_prontoqa,
gd_logicinference) is a subset of the program class; gd_boardgameqa is added from its MANIFEST note ("Program-generated
defeasible reasoning with exact labels") and listed in PROGRAM_EXTRA so the orchestrator can flip it.

  nice -n 10 ../../../.venv/bin/python -B pool.py map --draw pool/draw_75000.json
Writes POOL_MAP.json, POOL_MAP.md and pool/population.jsonl.gz (the human-label rows of the draw, with their text).
"""
from __future__ import annotations

import argparse
import glob
import gzip
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[1]
DATA = LEAN / "data"
GOLDEN = DATA / "v14_parts/golden_train.jsonl"
RAW = DATA / "v14_parts/raw"
MANIFEST = LEAN / "golden_src/MANIFEST.jsonl"
POOL_DIR = HERE / "pool"
POPULATION = POOL_DIR / "population.jsonl.gz"

PROGRAM_PREFIX = ("gd_gen", "pg_")                      # gd_gen2_* is covered
PROGRAM_EXACT = {"judge_mathderiv", "gd_babi_logic", "gd_prontoqa", "gd_logicinference"}   # = replay_sample.py's list
PROGRAM_EXTRA = {"gd_boardgameqa": "MANIFEST: 'Program-generated defeasible reasoning with exact labels' "
                                   "(upstream synthetic benchmark; labels from a program)"}
CLAUDE_PREFIX = ("binj_", "std_", "hard_", "planted_", "proc_")
MIXED_HUMAN = {"gd_tatqa", "gd_tathqa", "gd_finqa"}     # yes rows human gold, no rows program-built wrong answers
NEVER = re.compile(r"ohs|sealed_nd|sealed_brief|preread|external_quarantine|longbench_v2|jev", re.I)


def classify(source: str) -> tuple[str, str]:
    """(origin, rule) for one source name."""
    if source.startswith(CLAUDE_PREFIX):
        return "claude", "Claude-written golds (replay_sample CLAUDE_GOLD prefixes; dropped whole by the sampler)"
    if source.startswith("gd_gen"):
        return "program", "program-generated in this repo (golden_src/gen/*.py, exact labels)"
    if source.startswith("pg_"):
        return "program", "procedural generator rows (build_pg.py, exact labels)"
    if source == "judge_mathderiv":
        return "program", "procedural (build_judge.py, exact labels)"
    if source in PROGRAM_EXACT:
        return "program", "upstream synthetic generator with exact program labels (replay_sample PROGRAM_LABELLED_EXACT)"
    if source in PROGRAM_EXTRA:
        return "program", PROGRAM_EXTRA[source]
    if source in MIXED_HUMAN:
        return "human", "upstream human answer; no rows are program-built wrong answers of that human derivation (kept in scope)"
    return "human", "upstream human, crowd, expert or official-record label (golden_src MANIFEST / source licence note)"


def answer_format(qtypes: Counter, soft: int, n: int) -> str:
    parts = []
    if qtypes.get("noul"):
        parts.append(f"yes/no {qtypes['noul']:,}")
    if qtypes.get("choice"):
        parts.append(f"choice {qtypes['choice']:,}")
    s = " + ".join(parts) or "none"
    return s + (f"; {soft:,} rows carry human vote shares (meta.teacher)" if soft else "")


def read_manifest() -> dict:
    out = {}
    if MANIFEST.exists():
        for line in MANIFEST.read_text().splitlines():
            if line.strip():
                d = json.loads(line)
                out[d["key"]] = d
    return out


def builder_files(sources) -> dict:
    """source -> builder files (lean/build_*.py, golden_src/**/*.py) naming the source or its key. Files whose name
    or path hits the never-open list are skipped, never read."""
    files = [f for f in glob.glob(str(LEAN / "*.py")) + glob.glob(str(LEAN / "golden_src/**/*.py"), recursive=True)
             if not NEVER.search(os.path.relpath(f, LEAN.parent.parent)) and
             re.search(r"(^|/)(build|make|gen|fetch)[^/]*\.py$|golden_src/", f)]
    text = {}
    for f in files:
        try:
            text[f] = Path(f).read_text(errors="ignore")
        except OSError:
            pass
    raw = {p[:-6] for p in os.listdir(RAW)} if RAW.exists() else set()
    out = {}
    for s in sources:
        key = re.sub(r"^(gd_|br_|judge_|pg_|tb_)", "", s)
        pat = re.compile(r"\b(?:" + re.escape(s) + "|" + re.escape(key) + r")\b")
        hits = sorted(os.path.relpath(f, LEAN) for f, t in text.items() if pat.search(t))
        # prefer the files that carry the source's own name, and builders over mixers
        own = [h for h in hits if re.search(re.escape(key), os.path.basename(h))]
        out[s] = {"key": key, "builder_files": (own or hits)[:4], "raw_file": f"data/v14_parts/raw/{key}.jsonl"
                  if key in raw else None}
    return out


def is_human(source: str) -> bool:
    return classify(source)[0] == "human"


def stream_pool(draw: dict, pool_drop_units: set, want_ids: set, out_path: Path):
    """One pass over golden_train: per-source stats for the map and the text of the screened population rows."""
    st = defaultdict(lambda: {"n": 0, "qtype": Counter(), "soft": 0, "ds": Counter(), "lic": Counter(),
                              "attacked": 0, "ex": None})
    POOL_DIR.mkdir(exist_ok=True)
    n_out = 0
    with gzip.open(out_path, "wt", encoding="utf-8") as fo, open(GOLDEN) as f:
        for line in f:
            r = json.loads(line)
            m = r.get("meta") or {}
            s = st[r["source"]]
            s["n"] += 1
            s["qtype"][r["qtype"]] += 1
            teach = m.get("teacher")
            soft = isinstance(teach, dict) and m.get("teacher_src") != "blend50"
            s["soft"] += bool(soft)
            s["attacked"] += bool(m.get("attack_target")) or r["role"] == "attacked"
            s["ds"][str(m.get("dataset", ""))[:90]] += 1
            s["lic"][str(m.get("licence", ""))[:90]] += 1
            if r["id"] in want_ids and is_human(r["source"]) and draw["unit_of"].get(r["id"]) not in pool_drop_units:
                row = {"id": r["id"], "source": r["source"], "group": r["group_id"], "qtype": r["qtype"],
                       "role": r["role"], "state": r.get("state") or "", "instructions": r.get("instructions") or "",
                       "options": r.get("options") or [], "card": r.get("card") or "", "gold": r["gold"],
                       "soft": bool(soft), "attacked": bool(m.get("attack_target")) or r["role"] == "attacked",
                       "unit": draw["unit_of"].get(r["id"])}
                fo.write(json.dumps(row, ensure_ascii=False) + "\n")
                n_out += 1
    return st, n_out


def build_map(draw_path: Path, out_dir: Path = HERE) -> dict:
    draw = json.loads(draw_path.read_text())
    el_pre, el_post = draw["eligible_by_source_before_old_slice"], draw["eligible_by_source"]
    drawn = draw["draw_r1_by_source"]
    sources = sorted(set(el_pre) | set(el_post) | set(drawn))
    pd_units = set(draw.get("pool_drop_units_in_draw", []))
    # the screening population = human-origin rows of the draw, minus units the mixer drops anyway (pool_drops_r1)
    st, kept = stream_pool(draw, pd_units, set(draw["draw_r1_ids"]), POPULATION)
    by_src_pop = Counter()
    with gzip.open(POPULATION, "rt", encoding="utf-8") as fi:
        for line in fi:
            by_src_pop[json.loads(line)["source"]] += 1
    man = read_manifest()
    bf = builder_files(sources)
    out_src = {}
    for s in sources:
        origin, rule = classify(s)
        key = bf[s]["key"]
        mn = man.get(key) or man.get(s) or {}
        x = st.get(s)
        out_src[s] = {
            "gold_origin": origin, "origin_rule": rule,
            "evidence": {"manifest_note": (mn.get("notes") or "")[:400] or None,
                         "manifest_dataset": mn.get("dataset"),
                         "meta_dataset": ([d for d, _ in x["ds"].most_common(2)] if x else None),
                         "meta_licence": ([d for d, _ in x["lic"].most_common(1)] if x else None),
                         "builder_files": bf[s]["builder_files"], "raw_file": bf[s]["raw_file"],
                         "legacy_note": (None if bf[s]["builder_files"] or not s.startswith(("br_", "judge_", "pg_"))
                                         else "legacy replay pool (GOLDEN_CARD.md 'replay (v13 clean pool)', "
                                              "build_train_v13t.py prefixes); no build_*.py names this source: "
                                              "provenance = meta.dataset / meta.licence / meta.teacher")},
            "answer_format": answer_format(x["qtype"], x["soft"], x["n"]) if x else None,
            "pool_rows": x["n"] if x else 0,
            "eligible_rows_before_old_slice": el_pre.get(s, 0), "eligible_rows": el_post.get(s, 0),
            "draw_rows": drawn.get(s, 0), "attacked_rows_in_pool": x["attacked"] if x else 0,
            "screened_population_rows": by_src_pop.get(s, 0), "in_screen_scope": origin == "human"}
    tot = lambda k, o: sum(v[k] for v in out_src.values() if v["gold_origin"] == o)  # noqa: E731
    summary = {
        "eligible_rows_before_old_slice": {o: tot("eligible_rows_before_old_slice", o) for o in ("human", "program", "claude")},
        "eligible_rows": {o: tot("eligible_rows", o) for o in ("human", "program", "claude")},
        "eligible_human_rows_above_40000": tot("eligible_rows", "human") > 40000,
        "draw_rows": {o: tot("draw_rows", o) for o in ("human", "program", "claude")},
        "draw_rows_total": len(draw["draw_r1_ids"]),
        "pool_drop_units_in_draw": len(pd_units),
        "screened_population_rows": kept, "screened_sources": sum(1 for v in out_src.values() if v["screened_population_rows"]),
        "population_attacked_rows": None}
    rep = {"spec": "PREREG_FINAL.md Ruling A46; C2_DATA_SPEC 5.4", "seed": draw["seed"], "r1": draw["r1"],
           "r2": draw["r2"], "margin": draw["margin"], "draw_file": os.path.relpath(draw_path, HERE),
           "sampler_args": f"--dry-run --r1 {draw['r1']} --r2 {draw['r2']} --margin {draw['margin']} (SEED patched to "
                           f"{draw['seed']} in-process; replay_sample.py unchanged)",
           "summary": summary, "sources": out_src}
    (out_dir / "POOL_MAP.json").write_text(json.dumps(rep, indent=1))
    (out_dir / "POOL_MAP.md").write_text(map_md(rep))
    return rep


def map_md(rep: dict) -> str:
    sm = rep["summary"]
    L = ["# Replay pool map (A46)", "",
         f"Draw: replay_sample.py unchanged, seed {rep['seed']}, r1 = {rep['r1']:,}, r2 = {rep['r2']:,}, margin "
         f"{rep['margin']:.0%} ({rep['sampler_args']}).", "",
         "| | human | program | claude |", "|---|---|---|---|",
         "| eligible rows (before the old slice) | " + " | ".join(f"{sm['eligible_rows_before_old_slice'][o]:,}"
                                                              for o in ("human", "program", "claude")) + " |",
         "| eligible rows (after the old slice) | " + " | ".join(f"{sm['eligible_rows'][o]:,}"
                                                               for o in ("human", "program", "claude")) + " |",
         "| rows in the draw | " + " | ".join(f"{sm['draw_rows'][o]:,}" for o in ("human", "program", "claude")) + " |",
         "", f"Eligible human rows above 40,000: {sm['eligible_human_rows_above_40000']} (A46 size fallback "
             f"{'applies' if sm['eligible_human_rows_above_40000'] else 'does not apply'}).",
         f"Screening population (human rows of the draw, minus {sm['pool_drop_units_in_draw']} pool_drops_r1 units): "
         f"{sm['screened_population_rows']:,} rows in {sm['screened_sources']} sources.", "",
         "| source | origin | eligible | draw | screened | answer format | evidence |", "|---|---|---|---|---|---|---|"]
    for s, v in sorted(rep["sources"].items(), key=lambda kv: (kv[1]["gold_origin"] != "human", -kv[1]["eligible_rows"])):
        ev = v["evidence"]
        note = (ev["manifest_note"] or "")[:110].replace("|", "/")
        src = ev["meta_dataset"][0][:60].replace("|", "/") if ev["meta_dataset"] else ""
        b = ",".join(os.path.basename(x) for x in ev["builder_files"][:2])
        L.append(f"| {s} | {v['gold_origin']} | {v['eligible_rows']:,} | {v['draw_rows']:,} | "
                 f"{v['screened_population_rows']:,} | {v['answer_format'] or ''} | {note or src}; builder {b or 'legacy (see POOL_MAP.json)'}; "
                 f"raw {'yes' if ev['raw_file'] else 'no'} |")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["map"])
    ap.add_argument("--draw", default=str(POOL_DIR / "draw_75000.json"))
    a = ap.parse_args()
    r = build_map(Path(a.draw))
    print(json.dumps(r["summary"], indent=1))
