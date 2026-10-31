"""Synthetic fixtures for the l1_look tests: an OHS-4-SHAPED suite made of generic fake items (never a real item), its request file, a manifest
with the pins, the frozen scorer / Jev runner CODE copied from the sealed folder (code only, no data), and a fake mixdev. Nothing here reads the
real suite, the real request file or any real answer; the real looks.jsonl is never touched."""
from __future__ import annotations

import hashlib
import json
import random
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[3]
REAL_SCORER_DIR = LEAN / "ohs4_sealed" / "scorer"             # code only: score_ohs4.py and run_jev_ohs4.py
LOGS = LEAN / "c2_build" / "logs"
MARK = "SYNTHETIC-ITEM-TEXT"                                    # every fake state / instruction carries it, so a leak test can look for it


def sha(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def have_scorer_code() -> bool:
    return (REAL_SCORER_DIR / "score_ohs4.py").exists() and (REAL_SCORER_DIR / "run_jev_ohs4.py").exists()


def _opts(rng, k):
    return [f"opt{chr(65 + i)}{rng.randint(0, 9)}" for i in range(k)]


def _item(i, part, qtype, slice_, group, domain, rng, card=False, meta=None):
    it = {"id": f"syn-{part}-{i:04d}", "part": part, "qtype": qtype, "slice": slice_, "group_id": group, "domain": f"dom{domain}",
          "domain_index": f"d{domain}", "kind": f"kind{domain}", "state": f"{MARK} state {part}{i} " + "lorem " * rng.randint(3, 12),
          "instructions": f"{MARK} question {part}{i}?", "meta": dict(meta or {}), "card": None}
    if qtype == "noul":
        it.update({"options": None, "gold": rng.randint(0, 1)})
        if card:
            it["card"] = "Definitions:\n- yes: the rule applies\n- no: it does not"
    else:
        opts = _opts(rng, rng.randint(2, 4))
        it.update({"options": opts, "gold": rng.choice(opts)})
        if card:
            it["card"] = {o: f"definition of {o}" for o in opts} if rng.random() < 0.5 else "\n".join(f"- {o}: definition of {o}" for o in opts)
    return it


def make_suite(seed: int = 0, n_g: int = 90, n_r: int = 70, n_u: int = 24, n_x: int = 30, n_comp: int = 24, n_edit: int = 12, n_ord: int = 12) -> list:
    rng = random.Random(seed)
    suite = []
    for i in range(n_g):
        suite.append(_item(i, "G", "noul" if i % 2 == 0 else "choice", "card" if i % 3 == 0 else "nocard", f"G{i // 2:04d}", i % 5, rng, card=i % 3 == 0))
    for i in range(n_r):
        it = _item(i, "R", "noul" if i % 3 else "choice", f"agent.c{1 + i % 3}" if i % 2 else f"everyday.c{4 + i % 3}", f"R{i // 2:04d}", i % 4, rng)
        it["domain_index"] = "r20" if i % 5 == 0 else f"r{1 + i % 4}"                   # the real suite carries r1..r20 here; r20 is the A38 sensitivity kind
        suite.append(it)
    for i in range(n_u):
        suite.append(_item(i, "U", "choice" if i % 2 else "noul", f"k{1 + i % 3}", f"U{i // 2:04d}", i % 3, rng))
    for i in range(n_x):
        qt = "noul" if i % 3 else "choice"
        a = _item(i, "X", qt, "attacked", f"X{i:04d}", i % 2, rng)
        c = _item(i, "X", qt, "clean", f"X{i:04d}", i % 2, rng)
        c["id"], a["id"] = f"syn-X-{i:04d}-c", f"syn-X-{i:04d}-a"
        c["gold"], a["gold"] = a["gold"], a["gold"]
        c["options"], c["card"] = a["options"], None
        if qt == "choice":
            c["gold"] = a["gold"]
            push = next(o for o in a["options"] if o != a["gold"])
        else:
            push = 1 - a["gold"]
        c["meta"] = {"x_pair": f"xp{i:04d}", "x_role": "clean"}
        a["meta"] = {"x_pair": f"xp{i:04d}", "x_role": "attacked", "attack_pushes_toward": push, "attack_type": "t"}
        suite += [c, a]
    noul_gr = [it for it in suite if it["part"] in ("G", "R") and it["qtype"] == "noul"]
    choice_g = [it for it in suite if it["part"] == "G" and it["qtype"] == "choice"]
    for k in range(n_comp):
        b = noul_gr[k % len(noul_gr)]
        suite.append({**{x: b[x] for x in ("state", "domain", "domain_index", "kind", "group_id", "options", "card", "meta")},
                      "id": b["id"] + f"~neg{k}", "part": "C", "qtype": "noul", "slice": "complement", "gold": 1 - b["gold"],
                      "instructions": b["instructions"] + " (negated)", "base_part": b["part"],
                      "consistency": {"type": "complement", "base_id": b["id"], "pair_id": f"cp{k}", "relation": "gold_flips"}})
    r_noul = [it for it in suite if it["part"] == "R" and it["qtype"] == "noul"]
    for k in range(n_edit):
        b = r_noul[k % len(r_noul)]
        suite.append({**{x: b[x] for x in ("state", "domain", "domain_index", "kind", "group_id", "options", "card", "meta")},
                      "id": b["id"] + f"~edit{k}", "part": "C", "qtype": "noul", "slice": "minimal_edit", "gold": 1 - b["gold"],
                      "instructions": b["instructions"], "base_part": b["part"],
                      "consistency": {"type": "minimal_edit", "base_id": b["id"], "pair_id": f"me{k}", "relation": "gold_flips"}})
    for k in range(n_ord):
        b = choice_g[k % len(choice_g)]
        suite.append({**{x: b[x] for x in ("state", "domain", "domain_index", "kind", "group_id", "card", "meta", "gold")},
                      "id": b["id"] + f"~ord{k}", "part": "C", "qtype": "choice", "slice": "option_order", "options": list(reversed(b["options"])),
                      "instructions": b["instructions"], "base_part": b["part"],
                      "consistency": {"type": "option_order", "base_id": b["id"], "pair_id": f"oo{k}", "relation": "same_gold"}})
    rng.shuffle(suite)
    return suite


def card_text(c):
    if not c:
        return None
    if isinstance(c, str):
        return c
    return "\n".join(f"- {k}: {v}" for k, v in c.items())


def to_request(it) -> dict:
    """The sealed builder's final/scripts/requests_ohs4.py::to_request (re-typed: the sealed script is not imported)."""
    q = {"type": it["qtype"], "instructions": it["instructions"]}
    if it["qtype"] == "choice":
        q["options"] = list(it["options"])
    c = card_text(it.get("card"))
    if c:
        q["card"] = c
    return {"id": it["id"], "state": it["state"], "questions": {"q0": q}}


def make_mixdev(seed: int = 1, n_fam: int = 6, per: int = 50) -> list:
    rng = random.Random(seed)
    rows = []
    for f in range(n_fam):
        for i in range(per):
            qt = "noul" if i % 2 == 0 else "choice"
            opts = _opts(rng, rng.randint(2, 4)) if qt == "choice" else None
            rows.append({"id": f"mx-F{f}-{i:03d}", "group_id": f"mxg{f}{i // 2}", "call_id": f"c{f}{i}", "source": "syn", "role": "base",
                         "state": f"{MARK} mixdev state F{f} {i}", "qtype": qt, "instructions": f"{MARK} mixdev question?", "options": opts,
                         "gold": rng.randint(0, 1) if qt == "noul" else rng.choice(opts), "card": None,
                         "meta": {"family": f"T{f:02d}", "domain_pack": f"pk{f}{i % 4}", "format_style": f"fs{i % 3}", "sampler": "S5"}})
    return rows


def write_jsonl(p, rows):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("".join(json.dumps(r) + "\n" for r in rows))


def write_tree(root: Path, suite: list, mixdev: list | None = None, copy_prompt_record: bool = True):
    """root/lean/... (data, c2_build) and root/synthetic_suite/... (the sealed-shaped folder). Returns (L1Paths, pins)."""
    from l1_look import l1common as L
    lean, sealed = Path(root) / "lean", Path(root) / "synthetic_suite"
    write_jsonl(sealed / "suite" / "ohs4_suite.jsonl", suite)
    write_jsonl(sealed / "requests" / "ohs4_requests.jsonl", [to_request(it) for it in sorted(suite, key=lambda x: hashlib.sha256(x["id"].encode()).hexdigest())])
    (sealed / "scorer").mkdir(parents=True, exist_ok=True)
    for n in ("score_ohs4.py", "run_jev_ohs4.py"):
        shutil.copyfile(REAL_SCORER_DIR / n, sealed / "scorer" / n)
    table = {"suite": {"suite/ohs4_suite.jsonl": sha(sealed / "suite/ohs4_suite.jsonl")},
             "requests": {"requests/ohs4_requests.jsonl": sha(sealed / "requests/ohs4_requests.jsonl")},
             "scorer": {"scorer/score_ohs4.py": sha(sealed / "scorer/score_ohs4.py")},
             "runner": {"scorer/run_jev_ohs4.py": sha(sealed / "scorer/run_jev_ohs4.py")}}
    (sealed / "MANIFEST.json").write_text(json.dumps({"sha256": table}))
    write_jsonl(lean / "data" / "c2_mixdev.jsonl", mixdev if mixdev is not None else make_mixdev())
    (lean / "c2_build" / "logs").mkdir(parents=True, exist_ok=True)
    (lean / "c2_build" / "train").mkdir(parents=True, exist_ok=True)
    if copy_prompt_record and (LOGS / "p7_prompt_sha_check.json").exists():
        shutil.copyfile(LOGS / "p7_prompt_sha_check.json", lean / "c2_build" / "logs" / "p7_prompt_sha_check.json")
    pins = {"MANIFEST.json": sha(sealed / "MANIFEST.json"), "suite/ohs4_suite.jsonl": table["suite"]["suite/ohs4_suite.jsonl"],
            "requests/ohs4_requests.jsonl": table["requests"]["requests/ohs4_requests.jsonl"][:8],
            "scorer/run_jev_ohs4.py": table["runner"]["scorer/run_jev_ohs4.py"][:8]}
    return L.L1Paths(lean, sealed), pins


def write_gate_files(p, grid_candidate: str, adapter_sha: str, grid_sha: str, pass_: bool = True, decision: str = "PASS", go: bool = True,
                     time_cand: float = 100.0, time_pg: float = 200.0, candidates: dict | None = None, rules: list | None = None):
    """GRID_RECORD.json, CANDIDATE_C2.json, the pre-gate result and the owner's GO #2 record, in the formats the real tools write."""
    rec = {"grid_sha256": grid_sha, "candidates": candidates or {grid_candidate: adapter_sha}}
    (p.grid_record).write_text(json.dumps(rec))
    (p.candidate).write_text(json.dumps({"name": "q35_4b_c2", "grid_candidate": grid_candidate, "adapter_sha256": adapter_sha, "grid_sha256": grid_sha,
                                         "rule": "PREREG A42-D 9.5", "written_unix": time_cand}))
    pg = {"pass": pass_, "decision": decision, "cand": "q35_4b_c2", "time_unix": time_pg, "checks": {"candidate": {"adapter_sha256": adapter_sha}}}
    if rules is not None:
        pg["rules"] = rules
    p.pregate.write_text(json.dumps(pg))
    if go:
        p.owner_go.write_text(json.dumps({"owner_words": "synthetic test words for the dry run", "go": "GO #2 (test)", "written_utc": "2026-10-19T12:00:00Z"}))


def rules_with(failed=()):
    """A pre-gate rules list in gate_c2's format ({id, name, status, detail}); `failed` ids are FAIL."""
    ids = ["a", "b", "c1", "c2", "c3", "c4", "c5", "c6", "c7", "d"]
    return [{"id": i, "name": i, "status": "FAIL" if i in failed else "PASS", "detail": "synthetic"} for i in ids]


def write_waiver(p, record="A100", waived_rule="b", waives=None, quote=None, prereg=True, owner_go=True, prereg_text=None, **extra):
    """c2_build/train/WAIVER_B_A100.json in the format of the real record, the owner's words file, and the PREREG Record A100 (a stub in the synthetic tree);
    `waiver_a100.waiver_active` (the orchestrator's own module) judges them."""
    wa = L_waiver_module()
    q = wa.A100_QUOTE if quote is None else quote
    p.waiver_b.write_text(json.dumps({"record": record, "quote": q, "owner_words_utc": "2026-10-18T19:20Z", "prereg": "PREREG_FINAL.md Record A100",
                                      "waives": ["b_transfer"] if waives is None else waives, "waived_rule": waived_rule, **extra}))
    go = p.train / "OWNER_GO_C2.txt"
    if owner_go:
        go.write_text("GO #1 words ...\n" + wa.A100_QUOTE + "\n")
    elif go.exists():
        go.unlink()
    if prereg:
        p.prereg.write_text(prereg_text or ("> **Record A100 (18 Oct 2026 ~19:20 UTC; OWNER words, verbatim; an OWNER OVERRIDE of a pre-registered gate AFTER the\n> result): \"" + wa.A100_QUOTE + "\"**\n"))
    elif p.prereg.exists():
        p.prereg.unlink()


def L_waiver_module():
    import sys
    d = str(LEAN / "c2_build")
    if d not in sys.path:
        sys.path.insert(0, d)
    import waiver_a100
    return waiver_a100


TRAINED = [f"T{f:02d}" for f in range(5)]        # the synthetic mixdev has families T00..T05; T05 plays the part of a family that is NOT trained (A80 c)


def trained_fn(p):
    return list(TRAINED)


def write_parity(p, cand_name, sha, *, where="canonical", agree=0.9985, n=2000, gpu="NVIDIA H100 80GB HBM3, 81559 MiB", **over):
    """A parity record in the format modal_app_grid.py::parity / grid_h100.parity writes (PARITY_<cand>.json)."""
    rec = {"cand": cand_name, "adapter_sha256": sha, "bar": {"PASS": True, "PASS_gate": True, "PASS_strict": True},
           "all": {"n": n, "argmax_agree": agree}, "gpu": gpu, "utc": "2026-10-19T12:00:00Z", "run_id": "parity_test"}
    rec.update(over)
    f = p.train / f"PARITY_{cand_name}.json" if where == "canonical" else p.train / "grid_h100" / "results" / "parity_test" / "parity" / cand_name / f"PARITY_{cand_name}.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(rec))
    return f


def write_chosen(p, cand, sha, a98_text="the A98 NO CANDIDATE record (synthetic stand-in)\n"):
    """CHOSEN_A98_NOCANDIDATE.json (kept for audit) and the NEW CHOSEN.json of the A100 re-selection; returns the 8-hex prefix of the A98 record."""
    p.chosen_a98.write_text(a98_text)
    p.chosen.write_text(json.dumps({"chosen": cand, "status": "A100 re-selection", "chosen_adapter_sha256": sha}))
    return sha_text(a98_text)[:8]


def sha_text(t: str) -> str:
    return hashlib.sha256(t.encode()).hexdigest()


def write_grid_plan(p, mixdev_sha):
    f = p.train / "grid_h100" / "results" / "grid_x" / "grid_x" / "plan.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps({"data_manifest": {"c2_mixdev.jsonl": {"sha256": mixdev_sha, "rows": 1}}}))
    return f
