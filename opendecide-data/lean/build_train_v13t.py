"""v0.13 teacher round mix (4B, warm start from q35_4b_v11c): BREADTH + Claude items + a large clean replay.
  breadth   data/v13_parts/breadth_train.jsonl (23 public human-labelled datasets; annotator soft labels in meta.teacher)
  v12       data/v12_parts/{hard,proc,planted}12_train.jsonl (Claude-written, blind-verified)
  replay    data/train_2b.jsonl minus the bigger-model rows (lah_*, meta*, Mixtral-text task bank), Claude card
            definitions swapped in (data/v12_parts/card_swap.json), about 20,000 rows sampled by unit across families
            (the v12 teacher round showed that about 48% replay let the model forget; here replay is about half the mix)
  claude    Claude teacher probabilities (data/v13_parts/relabel/passA/*.jsonl, blind pass) attached as meta.teacher to
            the replay rows they cover
Overlap filter: any shared 12-word run with a held-out test (OHS-1/2/3, eval*) or an exact dev state drops the unit.
Writes data/train_v13t.jsonl + data/train_v13t_relations.jsonl, and copies breadth_dev to data/breadth_dev.jsonl.
"""
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE / "data"
rj = lambda p: [json.loads(l) for l in open(p)] if Path(p).exists() else []
rng = random.Random(20261110)


def legacy(r):
    s = r["source"]
    return s.startswith(("lah_", "meta")) or (s.startswith("tb") and str((r.get("meta") or {}).get("task_source", "")).startswith("mixtral"))


def take_units(rows, n):
    u = defaultdict(list)
    for r in rows:
        u[r["call_id"]].append(r)
    us = list(u.values())
    rng.shuffle(us)
    out = []
    for x in us:
        if len(out) >= n:
            break
        out.extend(x)
    return out


def swap_cards(r, swap):
    if not r.get("card"):
        return r
    lines, n = [], 0
    for ln in r["card"].split("\n"):
        if ln.startswith("- ") and ": " in ln:
            lab, d = ln[2:].split(": ", 1)
            if d in swap:
                ln, n = f"- {lab}: {swap[d]}", n + 1
        lines.append(ln)
    return {**r, "card": "\n".join(lines)} if n else r


def fam(s):
    for p in ("hard_", "std_", "pg_", "judge", "binj", "tb", "wiki", "br_", "proc_", "planted_"):
        if s.startswith(p):
            return p.rstrip("_")
    return "other"


def main():
    swap = json.load(open(D / "v12_parts/card_swap.json"))
    clean = [swap_cards(r, swap) for r in rj(D / "train_2b.jsonl") if not legacy(r)]
    claude = {}
    for f in sorted((D / "v13_parts/relabel/passA").glob("*.jsonl")):
        for l in open(f):
            x = json.loads(l)
            if isinstance(x.get("probs"), dict) and x["probs"]:
                claude[x["id"]] = x["probs"]
    by = defaultdict(list)
    for r in clean:
        by[fam(r["source"])].append(r)
    replay = (take_units(by["other"], 8000) + take_units(by["tb"], 1400) + take_units(by["hard"], 2500)
              + take_units(by["pg"], 2600) + take_units(by["judge"], 2200) + take_units(by["std"], 1000)
              + take_units(by["binj"], 900) + take_units(by["wiki"], 700))
    n_claude = 0
    for i, r in enumerate(replay):
        p = claude.get(r["id"])
        if p is None:
            continue
        t = {"yes": float(p.get("yes", 0.5))} if r["qtype"] == "noul" else {o: float(p.get(o, 0.0)) for o in r["options"]}
        replay[i] = {**r, "meta": {**(r.get("meta") or {}), "teacher": t, "teacher_src": "claude_passA"}}
        n_claude += 1
    breadth = rj(D / "v13_parts/breadth_train.jsonl")
    v12 = rj(D / "v12_parts/hard12_train.jsonl") + rj(D / "v12_parts/proc12_train.jsonl") + rj(D / "v12_parts/planted12_train.jsonl")
    rows = list({r["id"]: r for r in breadth + v12 + replay}.values())
    words = lambda t: re.sub(r"[^a-z0-9]+", " ", t.lower()).split()

    def grams(t):
        w = words(t)
        return {" ".join(w[i:i + 12]) for i in range(max(0, len(w) - 11))}
    held = set()
    for f in ["ohs", "ohs2", "ohs3", "eval", "eval_card", "eval_jagged", "eval_opi", "eval_long", "eval_multi"]:
        for x in rj(D / f"{f}.jsonl"):
            held |= grams(x["state"])
    devs = ["dev", "devzs", "devzs2", "devp_card", "pg_dev", "debate_dev", "dev_nc", "taskbank_dev", "hard_dev", "dev_negwords",
            "dev_claims", "hard12_dev", "proc12_dev", "planted12_dev"]
    dev_exact = {" ".join(words(x["state"])) for f in devs for x in rj(D / f"{f}.jsonl")}
    bdev = rj(D / "v13_parts/breadth_dev.jsonl")
    (D / "breadth_dev.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in bdev))
    dev_exact |= {" ".join(words(x["state"])) for x in bdev}
    bad = {r["call_id"] for r in rows if (grams(r["state"]) & held) or " ".join(words(r["state"])) in dev_exact}
    print("dropped for overlap:", Counter(r["source"] for r in rows if r["call_id"] in bad))
    rows = [r for r in rows if r["call_id"] not in bad]
    rng.shuffle(rows)
    ids = {r["id"] for r in rows}
    rels = (rj(D / "train_2b_relations.jsonl") + rj(D / "v13_parts/breadth_relations.jsonl")
            + [x for k in ("hard", "proc", "planted") for x in rj(D / f"v12_parts/{k}12_relations.jsonl")])
    rels = [x for x in {(x["type"], x["a"], x["b"]): x for x in rels}.values() if x["a"] in ids and x["b"] in ids]
    (D / "train_v13t.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    (D / "train_v13t_relations.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rels))
    fams = Counter(fam(r["source"]) for r in rows)
    print(json.dumps({"rows": len(rows), "breadth": len(breadth), "v12": len(v12), "replay": len(replay),
                      "claude_teacher_rows": n_claude, "soft_rows": sum(isinstance((r.get("meta") or {}).get("teacher"), dict) for r in rows),
                      "legacy_left": sum(legacy(r) for r in rows), "relations": dict(Counter(x["type"] for x in rels)),
                      "families": fams.most_common(), "breadth_dev": len(bdev)}, indent=1))


if __name__ == "__main__":
    main()
