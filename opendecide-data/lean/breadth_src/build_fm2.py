"""v0.13 breadth corpus: raw rows for "fm2" (Fool Me Twice, Eisenschlos et al., NAACL 2021).

Source: tasksource/fool-me-twice @ c7bc95f5e7693dcfa1e03517d14e37d959072f32, train.jsonl ONLY (dev.jsonl and
test.jsonl are never downloaded or read). A byte snapshot is kept under breadth_src/cache/fm2/ and its sha256 is checked.
Licence: Apache-2.0 (HF card `license: apache-2.0`; GitHub google-research/fool-me-twice LICENSE). Evidence sentences
are Wikipedia text (CC BY-SA). Claims were written by human players; labels are the claim author's SUPPORTS/REFUTES
against the gold evidence they wrote the claim from (human). No model-written text or labels.

Row: state = "Wikipedia article: <page>\nEvidence: <gold evidence sentence(s), verbatim>\nClaim: <claim, verbatim>",
yes/no question "Does the evidence support the claim?"; SUPPORTS -> yes, REFUTES -> no.
NO soft labels (verifier fix, 2026-09-27). FM2 correct_votes/total_votes count game players who, under time pressure
and often after revealing only some (paid) clues, picked which of TWO claims was the false one. That measures how hard
the claim is to guess, not how annotators read this evidence: in the first build 48/600 rows had p(gold) < 0.5 while the
gold was plainly right given the evidence (e.g. "Carlton Fisk was a professional soccer player..." REFUTES, 2/5).
Votes stay in meta only; rows with >= 3 votes are still picked first (selection only, never a label).

Filters: state 15-4,000 chars; every gold evidence sentence must end in terminal punctuation (the source has
sentences cut mid-sentence, e.g. "His mother was Elizabeth Kīnaʻu and father", which can drop the fact the label rests on); dedup on normalised claim and on normalised state; 13-word-run decontamination against
every non-held-out jsonl we have (lean/data, lean/*_src, lean/pg, opendecide-data/data, JevBench public, other v13 raw
parts), plus 13-word-run decontamination against the full Wikipedia-text SOURCE splits behind held-out tasks
(VitaminC test [OHS-1], FewRel train_wiki+val_wiki and Few-NERD supervised test [OHS-3]); these are downloaded to
cache/heldout_decon/ and used only to drop FM2 rows. Held-out item files (ohs*, preds_*, results_*) are deliberately NOT opened (project rule).
Selection: seeded shuffle, rows with a soft label first, round-robin over labels (50/50), at most MAX_ROWS.

  ../.venv/bin/python breadth_src/build_fm2.py
"""
import hashlib
import json
import random
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent            # lean/breadth_src
LEAN = HERE.parent
ROOT = LEAN.parent                                # opendecide-data
JEV = ROOT.parent
CACHE = HERE / "cache" / "fm2"
OUT_RAW = LEAN / "data" / "v13_parts" / "raw" / "fm2.jsonl"
OUT_DEFS = LEAN / "data" / "v13_parts" / "defs" / "fm2.json"

KEY = "fm2"
REPO = "tasksource/fool-me-twice"
REVISION = "c7bc95f5e7693dcfa1e03517d14e37d959072f32"
TRAIN_SHA256 = "1f47e035650aa5734301afb36a94afa610af73ac908fd4c4009e281b9956a311"
LICENCE = ("Apache-2.0 (HF dataset card 'license: apache-2.0'; GitHub google-research/fool-me-twice LICENSE); "
           "evidence text from Wikipedia, CC BY-SA")
SEED = 20261101
MAX_ROWS = 600
LEN_RANGE = (15, 4000)
GRAM = 13
MIN_VOTES = 3
HELDOUT_DECON = CACHE.parent / "heldout_decon"
HELDOUT_SRC = [  # (repo_type/where, repo, revision, path) -- source splits of held-out tasks, decontamination only
    ("hf", "tals/vitaminc", "be6febb761b0b2807687e61e0b5282e459df2fa0", "test.jsonl"),
    ("gh", "thunlp/FewRel", "278a2315d2138810a379cd8d5718914dc56e2582", "data/train_wiki.json"),
    ("gh", "thunlp/FewRel", "278a2315d2138810a379cd8d5718914dc56e2582", "data/val_wiki.json"),
    ("hf", "DFKI-SLT/few-nerd", "205f3e9c9f3577ea2561d43f2f62dc249ab92d5b", "supervised/test-00000-of-00001.parquet"),
]
TERMINAL = re.compile(r"[.!?\"'\u201d\u2019)\]]\s*$")

INSTRUCTIONS = "Does the evidence support the claim?"
LABEL2OPT = {"SUPPORTS": "yes", "REFUTES": "no"}
OPTIONS = ["yes", "no"]
DEFS = {
    "yes": "The evidence supports the claim: read together, the evidence sentences back up everything the claim states, "
           "directly or by simple inference (dates, numbers, paraphrase), and nothing in them contradicts it.",
    "no": "The evidence refutes the claim: the evidence sentences contradict the claim or at least one detail in it, "
          "directly or by simple inference (dates, numbers, paraphrase), showing it is false.",
}

words = lambda t: re.sub(r"[\W_]+", " ", t.casefold()).split()
norm = lambda t: " ".join(words(t))


def grams(w, n=GRAM):
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


def load_train():
    p = CACHE / "train.jsonl"
    if not p.exists():
        import shutil
        from huggingface_hub import hf_hub_download
        CACHE.mkdir(parents=True, exist_ok=True)
        for f in ("train.jsonl", "README.md"):  # train only; dev/test are never fetched
            shutil.copy(hf_hub_download(REPO, f, repo_type="dataset", revision=REVISION), CACHE / f)
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    assert h == TRAIN_SHA256, f"snapshot sha256 mismatch: {h}"
    return [json.loads(l) for l in open(p, encoding="utf-8")]


def make_state(r):
    ev = "\n".join(e["text"].strip() for e in r["gold_evidence"])
    return f"Wikipedia article: {r['wikipedia_page']}\nEvidence: {ev}\nClaim: {r['text'].strip()}"


def evidence_complete(r):
    return all(TERMINAL.search(e["text"].strip()) for e in r["gold_evidence"])


def heldout_texts():
    """Yield texts of held-out SOURCE splits (decontamination only; nothing from here enters the output)."""
    HELDOUT_DECON.mkdir(parents=True, exist_ok=True)
    for kind, repo, rev, path in HELDOUT_SRC:
        local = HELDOUT_DECON / repo.replace("/", "__") / rev[:12] / path
        if not local.exists():
            local.parent.mkdir(parents=True, exist_ok=True)
            if kind == "hf":
                import shutil
                from huggingface_hub import hf_hub_download
                shutil.copy(hf_hub_download(repo, path, repo_type="dataset", revision=rev), local)
            else:
                import requests  # certifi-backed TLS (plain urllib fails on this machine)
                resp = requests.get(f"https://raw.githubusercontent.com/{repo}/{rev}/{path}", timeout=300)
                resp.raise_for_status()
                local.write_bytes(resp.content)
        if path.endswith(".jsonl"):
            for line in open(local, encoding="utf-8"):
                yield from strings(json.loads(line))
        elif path.endswith(".json"):
            for insts in json.load(open(local, encoding="utf-8")).values():
                for x in insts:
                    yield " ".join(x["tokens"])
        else:
            import pyarrow.parquet as pq
            for toks in pq.read_table(local, columns=["tokens"]).column("tokens").to_pylist():
                yield " ".join(toks)


def is_heldout(p: Path) -> bool:
    parts = [x.lower() for x in p.parts]
    return any(x.startswith(("ohs", "preds", "results")) for x in parts)


def scan_files():
    fs = set()
    for base in (LEAN, ROOT / "data"):
        for p in base.rglob("*.jsonl"):
            rel = p.relative_to(base)
            if is_heldout(rel) or "cache" in rel.parts or ".venv" in rel.parts or p.resolve() == OUT_RAW.resolve():
                continue
            fs.add(p)
    fs |= set((JEV / "bench/jevbench/datasets/public").glob("*.jsonl"))
    return sorted(fs)


def strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values():
            yield from strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from strings(v)


def decontaminate(cands):
    """Index the FM2 side (claim + evidence), stream our files; returns {rid: source file of first hit}."""
    owner = defaultdict(set)
    for c in cands:
        for g in grams(words(c["state"])):
            owner[g].add(c["rid"])
    hit, seen, nfiles = {}, set(), 0
    for t in heldout_texts():
        w = words(t)
        for i in range(len(w) - GRAM + 1):
            for rid in owner.get(" ".join(w[i:i + GRAM]), ()):
                hit.setdefault(rid, "HELDOUT_SOURCE")
    for p in scan_files():
        nfiles += 1
        with open(p, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    x = json.loads(line)
                except Exception:  # noqa: BLE001
                    continue
                for t in strings(x):
                    if len(t) < 40:
                        continue
                    h = hash(t)
                    if h in seen:
                        continue
                    seen.add(h)
                    w = words(t)
                    for i in range(len(w) - GRAM + 1):
                        for rid in owner.get(" ".join(w[i:i + GRAM]), ()):
                            hit.setdefault(rid, str(p))
    return hit, nfiles


def main():
    src = load_train()
    cands, seen_claim, seen_state, drop = [], set(), set(), Counter()
    for r in src:
        if r["label"] not in LABEL2OPT or not r.get("gold_evidence"):
            drop["bad label/evidence"] += 1
            continue
        if not evidence_complete(r):
            drop["truncated evidence"] += 1
            continue
        state = make_state(r)
        if not (LEN_RANGE[0] <= len(state) <= LEN_RANGE[1]):
            drop["length"] += 1
            continue
        nc, ns = norm(r["text"]), norm(state)
        if nc in seen_claim or ns in seen_state:
            drop["duplicate"] += 1
            continue
        seen_claim.add(nc); seen_state.add(ns)
        cands.append({
            "key": KEY, "rid": r["id"], "state": state, "instructions": INSTRUCTIONS, "options": list(OPTIONS),
            "gold": LABEL2OPT[r["label"]], "soft": None,
            "meta": {"dataset": REPO, "config": "default", "revision": REVISION, "licence": LICENCE, "split": "train",
                     "orig_label": r["label"], "category": r.get("category"),
                     "votes": [r.get("correct_votes"), r.get("total_votes")]},
        })
    hit, nfiles = decontaminate(cands)
    drop["13-gram overlap"] = sum(1 for c in cands if c["rid"] in hit)
    cands = [c for c in cands if c["rid"] not in hit]

    rng = random.Random(SEED)
    rng.shuffle(cands)
    by_label = {o: [c for c in cands if c["gold"] == o] for o in OPTIONS}
    for o in OPTIONS:  # stable: rows with >= MIN_VOTES game votes first (selection only), shuffle order otherwise
        by_label[o].sort(key=lambda c: (c["meta"]["votes"][1] or 0) < MIN_VOTES)
    out, i = [], 0
    while len(out) < MAX_ROWS and any(i < len(v) for v in by_label.values()):
        for o in OPTIONS:
            if i < len(by_label[o]) and len(out) < MAX_ROWS:
                out.append(by_label[o][i])
        i += 1

    OUT_RAW.parent.mkdir(parents=True, exist_ok=True)
    OUT_DEFS.parent.mkdir(parents=True, exist_ok=True)
    OUT_RAW.write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in out), encoding="utf-8")
    OUT_DEFS.write_text(json.dumps(DEFS, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    L = [len(c["state"]) for c in out]
    voted = [c for c in out if (c["meta"]["votes"][1] or 0) >= MIN_VOTES]
    print(f"source train rows {len(src)}; candidates {len(cands) + drop['13-gram overlap']}; drops {dict(drop)}")
    print(f"decontam: scanned {nfiles} files; hit files {Counter(hit.values()).most_common(5)}")
    print(f"wrote {len(out)} rows -> {OUT_RAW}")
    print("labels", dict(Counter(c["gold"] for c in out)))
    print(f"no soft labels; rows with >= {MIN_VOTES} votes {len(voted)}/{len(out)}")
    print(f"state chars min {min(L)} median {statistics.median(L)} mean {statistics.mean(L):.0f} max {max(L)}")
    print("categories", dict(Counter(c["meta"]["category"] for c in out)))
    print("defs", {k: len(v.split()) for k, v in DEFS.items()}, "words")


if __name__ == "__main__":
    main()
