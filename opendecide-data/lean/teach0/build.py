"""TEACH-0 (owner GO 13 Oct): can Claude be a teacher that is clearly better than Jev? Dev rows only, report-only.

Builds the 2,000-row sample T = S (the 660 SPEED-2 rows Jev already answered) + U (1,340 more gate dev rows, uniform
without replacement, seed 3), the gold-free question chunks the Claude agents answer (40 x 50, order seed 4, opaque
qids), and the key (qid -> row id). `--jev` also sends U to Jev through speed_bench.run_jev (OpenRouter, ~$0.04).
  ../.venv/bin/python teach0/build.py            (sample + chunks + key; deterministic)
  ../.venv/bin/python teach0/build.py --jev      (then Jev on U)
"""
import hashlib, json, random, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parent
sys.path.insert(0, str(LEAN / "hosting"))
import speed_bench as sb  # noqa: E402  (dev rows, API v1 items, Jev client; read-only)

N_U, SEED_U, SEED_ORDER, CHUNK = 1340, 3, 4, 50


def main(jev=False):
    rows = {r["id"]: r for r in sb.dev_rows()}
    s_ids = [json.loads(l)["id"] for l in open(LEAN / "speed/workloads/S.jsonl")]
    rest = sorted(set(rows) - set(s_ids))
    u_ids = random.Random(SEED_U).sample(rest, N_U)
    t_ids = s_ids + u_ids
    assert len(set(t_ids)) == 2000
    sha = hashlib.sha256("\n".join(t_ids).encode()).hexdigest()
    (HERE / "sample.json").write_text(json.dumps({"S": s_ids, "U": u_ids, "T_sha256": sha}, indent=1))
    order = t_ids[:]
    random.Random(SEED_ORDER).shuffle(order)
    (HERE / "chunks").mkdir(exist_ok=True)
    (HERE / "key").mkdir(exist_ok=True)
    key = {}
    for c in range(0, len(order), CHUNK):
        qs = []
        for k, rid in enumerate(order[c:c + CHUNK]):
            r, qid = rows[rid], f"q{c + k:04d}"
            key[qid] = {"id": rid, "split": r["split"], "qtype": r["qtype"]}
            q = {"qid": qid, "kind": "yes/no" if r["qtype"] == "noul" else "choice", "text": r["state"],
                 "question": r["instructions"]}
            if r["qtype"] == "choice":
                q["options"] = list(r["options"])
            if r.get("card"):
                q["definitions"] = r["card"]
            qs.append(q)
        (HERE / "chunks" / f"chunk_{c // CHUNK:02d}.json").write_text(json.dumps(qs, ensure_ascii=False, indent=1))
    (HERE / "key" / "key.json").write_text(json.dumps(key, indent=1))
    print(f"T 2000 (S 660 + U {N_U}) sha {sha[:16]}; {len(order) // CHUNK} chunks of {CHUNK}")
    if jev:
        items = [sb.make_item(rows[i]) for i in u_ids]
        sb.run_jev(HERE / "jev_U", items, go=True, noul_card="instructions")


if __name__ == "__main__":
    main(jev="--jev" in sys.argv)
