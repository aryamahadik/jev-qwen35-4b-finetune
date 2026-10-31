#!/usr/bin/env python3
"""G-block card lint, dedup and G-LEX extraction chunks (PREREG_FINAL A39 c; A37 b; A38 freeze).

Subcommands:
  lint     load cards/answers/*.json, lint every card, dedup the passing ones, write
           cards/lint_report.json and cards/survivors.json.
  extract  build two independent G-LEX read sets (rA, rB) from survivors.json. Each read is its own set of
           chunk files (<= 25 cards each) under cards/extract/, with its own answer path, its own opaque qids and
           its own card and option order. Writes cards/extract_key/ (keys and manifest; never sent to Haiku).

Haiku only restates options and writes example texts for them. Nothing here sets, edits or chooses a label.
Writes go through c2_kit.paths (A38 guard, never-open guard, lean/ only).
"""
import hashlib
import hmac
import json
import re
import sys
from collections import Counter
from pathlib import Path

C2 = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build")
GB = C2 / "gblock"
CARDS = GB / "cards"
ANS = CARDS / "answers"
EXT = CARDS / "extract"
EXT_ANS = EXT / "answers"
KEYS = CARDS / "extract_key"
sys.path.insert(0, str(C2))
from c2_kit import paths as kp      # write_json, never_open, require_a38
from c2_kit import chunker as kc    # _walk_keys, _strings, _PATHISH (the kit's own item guards)

CHUNK = 25
STOP = set(("a an the and or of to in on for with at by from is it be as that this your their its do does are was "
            "were been being into than then so if when while which who what whom whose how there here these those "
            "such each any all some very can could would should will shall may might must just also only").split())
DENY = {"positive", "negative", "neutral", "entailment", "contradiction", "joy", "sadness", "anger", "fear",
        "surprise", "disgust"}
TRAIT = re.compile(r"\b(age|gender|race|ethnic\w*|religio\w*|disabilit\w*|pregnan\w*|sexual\w*|orientation|health|"
                   r"medical|diagnos\w*|immigra\w*|nationality|marital)\b", re.I)
OVERLAP_MAX = 0.5      # definition content-word Jaccard at or above this counts as overlapping
NEAR_DUP = 0.8         # question content-word Jaccard at or above this counts as a near duplicate


def stem(t):
    return t[:-1] if len(t) > 3 and t.endswith("s") and not t.endswith("ss") else t


def toks(s):
    return [stem(t) for t in re.findall(r"[a-z0-9]+", s.lower()) if t not in STOP]


def wc(s):
    return len(re.findall(r"[A-Za-z0-9']+", s))


def jacc(a, b):
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def load_answers():
    cards, problems = [], []
    for p in sorted(ANS.glob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:                       # noqa: BLE001 - reported, not hidden
            problems.append(f"{p.name}: unreadable ({e})")
            continue
        if d.get("task_id") != p.stem:
            problems.append(f"{p.name}: task_id {d.get('task_id')!r} does not match the file name")
        cl = d.get("cards")
        if not isinstance(cl, list) or len(cl) != 2:
            problems.append(f"{p.name}: expected 2 cards, found {len(cl) if isinstance(cl, list) else 'none'}")
        domain = re.sub(r"_\d+$", "", p.stem)
        for i, c in enumerate(cl or []):
            cards.append({"src": f"{p.stem}#{i}", "task_id": p.stem, "domain": domain, "card": c})
    return cards, problems


def lint_card(c):
    """(reasons, details). An empty reasons list passes."""
    fails, det = [], {}
    kind = c.get("kind")
    q = (c.get("question") or "").strip()
    who = (c.get("who_decides") or "").strip()
    opts = c.get("options")
    if kind not in ("yes/no", "choice"):
        fails.append("kind")
    if not (q.endswith("?") and q.count("?") == 1):
        fails.append("question_form")
    if wc(who) < 4:
        fails.append("who_decides_missing")
    if not isinstance(opts, list):
        return fails + ["options_not_list"], det
    if not (2 <= len(opts) <= 8):
        fails.append("option_count")
    names, defs = [], []
    for o in opts:
        if not isinstance(o, dict):
            fails.append("option_not_object")
            names.append("")
            defs.append("")
            continue
        names.append((o.get("label") or "").strip())
        defs.append((o.get("definition") or "").strip())
    if kind == "yes/no" and sorted(x.lower() for x in names) != ["no", "yes"]:
        fails.append("yesno_labels")
    if any(not x for x in names):
        fails.append("label_empty")
    if len({x.lower() for x in names}) != len(names):
        fails.append("labels_not_distinct")
    if any(not (1 <= wc(x) <= 5) for x in names):
        fails.append("label_length")
    if any(wc(d) < 6 for d in defs):
        fails.append("definition_missing")
    if len({" ".join(d.lower().split()) for d in defs}) != len(defs):
        fails.append("definitions_identical")
    ds = [set(toks(d)) for d in defs]
    worst, pair = 0.0, None
    for i in range(len(ds)):
        for j in range(i + 1, len(ds)):
            v = jacc(ds[i], ds[j])
            if v > worst:
                worst, pair = v, (names[i], names[j])
    det["max_definition_jaccard"] = round(worst, 3)
    det["max_definition_pair"] = pair
    if worst >= OVERLAP_MAX:
        fails.append("definitions_overlap")
    qt = set(toks(q))
    leak = sorted({t for x in names for t in toks(x)} & qt)
    det["label_words_in_question"] = leak
    if leak:
        fails.append("label_word_in_question")
    if any(x.lower() in DENY for x in names):
        fails.append("public_label_set")
    if TRAIT.search(q):
        fails.append("personal_trait_question")
    return fails, det


def cmd_lint():
    cards, problems = load_answers()
    report, passing = [], []
    reason_ct = Counter()
    for s in cards:
        reasons, det = lint_card(s["card"])
        for r in reasons:
            reason_ct[r] += 1
        report.append({"src": s["src"], "domain": s["domain"], "kind": s["card"].get("kind"),
                       "status": "lint_fail" if reasons else "lint_pass", "reasons": reasons, "details": det})
        if not reasons:
            passing.append(s)
    # dedup among lint-passing cards, first occurrence kept (sorted task order)
    seen_exact, kept, dedup_ct = {}, [], Counter()
    by_src = {r["src"]: r for r in report}
    for s in passing:
        qn = " ".join(toks(s["card"]["question"]))
        if qn in seen_exact:
            by_src[s["src"]]["status"] = "dedup_drop"
            by_src[s["src"]]["reasons"] = [f"duplicate of {seen_exact[qn]}"]
            dedup_ct["duplicate_question"] += 1
            continue
        qs = set(toks(s["card"]["question"]))
        near = None
        for k in kept:
            if k["card"].get("kind") == s["card"].get("kind") and jacc(qs, set(toks(k["card"]["question"]))) >= NEAR_DUP:
                near = k["src"]
                break
        if near:
            by_src[s["src"]]["status"] = "dedup_drop"
            by_src[s["src"]]["reasons"] = [f"near duplicate of {near}"]
            dedup_ct["near_duplicate_question"] += 1
            continue
        seen_exact[qn] = s["src"]
        kept.append(s)
    survivors = [{"src": s["src"], "domain": s["domain"], "card": s["card"]} for s in kept]
    summary = {
        "answer_files": len(list(ANS.glob("*.json"))),
        "problems": problems,
        "cards_loaded": len(cards),
        "by_kind": dict(Counter(s["card"].get("kind") for s in cards)),
        "lint_pass": len(passing),
        "lint_fail": len(cards) - len(passing),
        "lint_fail_reasons": dict(reason_ct),
        "dedup_drops": dict(dedup_ct),
        "survivors": len(survivors),
        "survivors_by_kind": dict(Counter(s["card"].get("kind") for s in survivors)),
        "survivors_by_domain": dict(Counter(s["domain"] for s in survivors)),
    }
    kp.write_json(CARDS / "lint_report.json", {"summary": summary, "cards": list(by_src.values())})
    kp.write_json(CARDS / "survivors.json", survivors)
    print(json.dumps(summary, indent=1, ensure_ascii=False))


PROMPT = """You are checking how clearly the options on a decision card are written. The card asks one question about a short text. Each option has a short name and a one-sentence definition. You will not see any real text to classify.

Do this for EVERY card in this file, and for EVERY option on each card:
1. "meaning": restate, in ONE line of at most 25 words and in your own words, what the option means. Do not copy the definition word for word.
2. "example": write ONE short example text of one or two plain sentences (at most 40 words) that clearly belongs to that option under its definition. It should read like a passage a reader could really see, fit this option, and not fit the other options on the card. Do not repeat the option name inside the example.

Rules:
- Use plain everyday English. Do not use outside facts about real people, places or organisations.
- Do not change, add or drop option names or cards. Do not say which option a card's question should be answered with.
- Your restatements and examples are only checked. They are never labels and never training data.

Write ONE JSON object, and nothing else, to this exact file path:
@ANSWER_PATH@

JSON shape (task_id must be "@TASK_ID@"):
{"task_id": "@TASK_ID@",
 "answers": [
   {"qid": "<the qid of a card>",
    "options": [
      {"name": "<option name exactly as given>", "meaning": "one line", "example": "one short example text"}
    ]}
 ]}

Give one entry in "answers" for every card in this file, and one entry in "options" for every option of that card. Copy each qid and each option name exactly as given.

Access rules: read only this task file; write only the answer file named above. Do not open any other file, do not run programs, do not use the web."""


def _opt_key(seed, src, name):
    return hashlib.sha256(f"{seed}|opt|{src}|{name}".encode()).hexdigest()


def build_read(read, survivors):
    """One independent read set. Different seed, order, qids and option order from every other read set."""
    seed = f"gblock-g-lex-A39|{read}"
    secret = hashlib.sha256(seed.encode()).digest()
    order = sorted(survivors, key=lambda s: hashlib.sha256(f"{seed}|order|{s['src']}".encode()).hexdigest())
    tasks, keymap = [], {}
    for k in range(0, len(order), CHUNK):
        tid = f"{read}_{k // CHUNK + 1:03d}"
        ans_path = str(EXT_ANS / f"{tid}.json")
        cards_out, keys_here = [], {}
        for s in order[k:k + CHUNK]:
            c = s["card"]
            qid = "q" + hmac.new(secret, s["src"].encode(), hashlib.sha256).hexdigest()[:10]
            if qid in keys_here:
                raise SystemExit(f"qid collision in {tid}")
            keys_here[qid] = s["src"]
            opts = [{"name": o["label"].strip(), "definition": o["definition"].strip()} for o in c["options"]]
            opts.sort(key=lambda o: _opt_key(seed, s["src"], o["name"]))
            cards_out.append({"qid": qid, "kind": c["kind"], "who_decides": c["who_decides"].strip(),
                              "question": c["question"].strip(), "options": opts})
        prompt = PROMPT.replace("@ANSWER_PATH@", ans_path).replace("@TASK_ID@", tid)
        chunk = {
            "task_id": tid,
            "kind": "gblock_card_extraction_glex",
            "binding": ("PREREG_FINAL.md Ruling A39 (c): G-LEX-style extraction of card options, blind. Restatements "
                        "and examples are checked only; never a label, never a training target."),
            "read": read,
            "instructions": prompt,
            "instructions_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
            "answer_path": ans_path,
            "allowed_read": [str(EXT / f"{tid}.json")],
            "allowed_write": [ans_path],
            "cards": cards_out,
        }
        # the kit's item guards: no forbidden keys, no never-open path, no internal ids (src) in the text
        kc._walk_keys(chunk, where=tid)
        for sstr in kc._strings(chunk):
            for m in kc._PATHISH.finditer(sstr):
                if kp.never_open(m.group()):
                    raise SystemExit(f"never-open path in {tid}: {m.group()}")
        blob = json.dumps(chunk, ensure_ascii=False)
        leaked = [src for src in keys_here.values() if src in blob]
        if leaked:
            raise SystemExit(f"internal id leaked into {tid}: {leaked[:2]}")
        tasks.append({"task_id": tid, "chunk": chunk, "keys": keys_here})
        keymap[tid] = keys_here
    return tasks


def cmd_extract():
    survivors = json.loads((CARDS / "survivors.json").read_text(encoding="utf-8"))
    if not survivors:
        raise SystemExit("no survivors")
    kp.require_a38()
    EXT_ANS.mkdir(parents=True, exist_ok=True)
    reads = {r: build_read(r, survivors) for r in ("rA", "rB")}
    # independence checks: disjoint qids and disjoint task files across the two reads
    qa = {q for t in reads["rA"] for q in t["keys"]}
    qb = {q for t in reads["rB"] for q in t["keys"]}
    if qa & qb:
        raise SystemExit("qids overlap across the two reads")
    manifest = {"batch": "gblock-g-lex-A39", "n_survivor_cards": len(survivors), "chunk_size": CHUNK,
                "reads": {}, "tasks": []}
    keys_out = {}
    for r, tasks in reads.items():
        manifest["reads"][r] = {"n_cards": sum(len(t["keys"]) for t in tasks), "n_files": len(tasks)}
        for t in tasks:
            path = EXT / f"{t['task_id']}.json"
            kp.write_json(path, t["chunk"])
            manifest["tasks"].append({"task_id": t["task_id"], "read": r, "n_cards": len(t["keys"]),
                                      "task_file": str(path), "answer_file": t["chunk"]["answer_path"],
                                      "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
            keys_out[t["task_id"]] = t["keys"]
    kp.write_json(KEYS / "keys.json", keys_out)
    kp.write_json(KEYS / "manifest.json", manifest)
    print(json.dumps({"reads": manifest["reads"], "n_survivor_cards": len(survivors),
                      "task_files": [t["task_file"] for t in manifest["tasks"]]}, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "lint":
        cmd_lint()
    elif cmd == "extract":
        cmd_extract()
    else:
        raise SystemExit("usage: gcards.py lint | extract")
