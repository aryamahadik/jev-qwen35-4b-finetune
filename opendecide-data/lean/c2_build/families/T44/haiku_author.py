"""families/T44/haiku_author.py: the T44 SEQ-CHECK Haiku wording pool (Ruling A57; C2_DATA_SPEC 3.0: at least 30 wordings
per family, A57 (f): at least 50 admitted wordings; each wording <= 2% of the family).

T44's only Haiku-authored text is the question wording of its two heads (ch_verdict, ch_next). Rules, tool-block layouts,
section headers and the tool / predicate / object vocabularies are program text (texts.py, world.py): no skin, no tool
description and no pack is authored. Held-out roles (A57 c): T44 has NO held-out wording, skin or header. Its held-out
material (domains registry / observatory / bakery, layouts hoare / colon, plan lengths 7-8) is program text, so every
held-out authoring quota is 0 (HELD_OUT_QUOTAS below; asserted by build_batches). Nothing here is dev-only either.

  build_batches()   {head: TaskBatch}: opaque qids, gold-free, no option / label / rule text, 20 items per chunk
  write_tasks()     task files under families/T44/haiku/a57/tasks/ (that folder is on the sealed never-open list);
                    the ANSWER file of each task is c2_build/a57_pool_quarantine/T44/answers/<task_id>.json (A57 d)
  check_wording()   program admission of ONE authored wording (drops only, never a rewrite)
  Stage 4 (admission needing no sealed text) is a57_t44_stage4.py.

Run (from lean/c2_build):  ../.venv/bin/python -B -m families.T44.haiku_author plan | write
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, gsl, paths  # noqa: E402
from c2_kit import skin as K  # noqa: E402
import negcount  # noqa: E402  (c_src/common, put on sys.path by c2_kit.paths)
from families.T44 import texts as TX  # noqa: E402

FAMILY = "T44"
SEED = "t44-a57-v1"
TASK_ROOT = HERE / "haiku" / "a57"                       # tasks, chunks, key, plan, manifests (never goes to Haiku but tasks)
QUARANTINE = C2_BUILD / "a57_pool_quarantine" / FAMILY   # answers ONLY (A57 d)
N_PER_HEAD = 60                                          # authored per head; >= 25 per head must survive (>= 50 total)
MIN_ADMITTED_PER_HEAD = 25
CHUNK = 20
# A57 (c): every held-out-role quota of T44's Haiku pool is 0 (it has no held-out Haiku role at all)
HELD_OUT_QUOTAS = {"N_WORDING_HELD": 0, "N_SKIN_HELD": 0, "N_DELEG_HELD": 0, "N_HELD_OUT_REGISTER_SKINS": 0,
                   "N_HELD_OUT_ATTACK_LINES": 0, "N_DEV_ONLY_WORDING": 0}
HEADS = (TX.HEAD_VERDICT, TX.HEAD_NEXT)
QFORM = {TX.HEAD_VERDICT: "verdict", TX.HEAD_NEXT: "next"}

# ---- words the line must not contain (the task says so; check_wording enforces it by program)
LABEL_RX = re.compile(r"\b(?:invalid|valid\w*|applicable|applicab\w*|appl(?:y|ies|ied|ying)|reach\w*|step\w*)\b", re.I)
VERDICT_LEAK_RX = re.compile(
    r"\b(?:fail\w*|succe\w*|work\w*|error\w*|break\w*|broke\w*|stuck|stop\w*|halt\w*|malform\w*|legal|illegal|correct\w*|"
    r"incorrect|wrong|flaw\w*|bug\w*|problem\w*|issue\w*|finish\w*|achiev\w*|satisf\w*|accomplish\w*|miss\w*|pass\w*|"
    r"sound|safe\w*|ok|okay|fine|good|bad|reach\w*|complete\w*|fulfil\w*|meet\w*|hit\w*|ready|clean|broken)\b", re.I)
YESNO_START_RX = re.compile(r"^\s*(?:is|are|does|do|did|can|could|will|would|should|was|were|has|have|had|may|might)\b", re.I)
EXTRA_BAN_RX = re.compile(r"\b(?:one|ones|first|second|third|next|last|now|then|later|earlier|before|after|once|again|"
                          r"all|every|each|some|any|only|both|either|always|never|just|even|also|too|very|best|"
                          r"most|more|less|least|few|fewer|many|much|half|twice|whether|if|unless|except|otherwise)\b", re.I)
CUE = {
    TX.HEAD_VERDICT: re.compile(r"\bplans?\b", re.I),
    TX.HEAD_NEXT: re.compile(r"\bshortest\b", re.I),
}
CUE2 = {
    TX.HEAD_VERDICT: re.compile(r"\b(?:run|runs|ran|running|execut\w*|outcome|outcomes|result|results|verdict|happen\w*|fare|fares|"
                                r"carried|check\w*|play\w*|follow\w*|go|goes|fit|fits|describe\w*|label\w*|call\w*|tool\w*|"
                                r"turn\w*|end\w*|trace\w*|simulat\w*|walk\w*)\b", re.I),
    TX.HEAD_NEXT: re.compile(r"\b(?:call|calls|move|moves|action|actions|tool|tools|option|options|choice|route|path|"
                             r"sequence|way|agent|make|take|pick|choose|select|start\w*|begin\w*|open\w*|lead\w*)\b", re.I),
}
MIN_WORDS, MAX_WORDS = 5, 22

BASE_RULES = [
    "Write exactly ONE sentence of 5 to 22 words. It ends with a question mark. It is a question that asks the reader to "
    "pick from options shown beneath it: it opens with a question word such as Which, What or How, or with a short lead-in "
    "before such a word. It is never a yes or no question (never open with Is, Are, Does, Do, Can, Should, Will, Was).",
    "Plain English, every letter in lowercase except the first letter of the sentence. No digits, no number words (one, two, first, "
    "second, half, ...), no names, no quotation marks, no brackets, no braces, no placeholders, no emoji.",
    "Never use any negation (not, no, none, never, nothing, without, n't ...), and never use these words: if, unless, "
    "except, otherwise, whether, all, every, each, some, any, only, both, either, always, just, even, also, too, very, "
    "best, most, more, less, least, few, many, much, once, again, then, now, next, last, first, later, earlier, before, after.",
    "Never use these words or any variant of them: valid, invalid, applicable, apply, reach, step. Never name or list the possible "
    "answers.",
    "Do not use a modal hint of possibility or doubt (maybe, perhaps, likely, seems, think, guess).",
]
VERDICT_RULES = BASE_RULES + [
    "The line must mention a plan (use the word plan or plans) and must not reveal, hint at or rank any outcome: never use "
    "words of success, failure, error, breaking, stopping, being stuck, being correct, wrong, good, bad, fine, safe, ready, "
    "complete, finished, passing, missing or meeting a goal.",
]
NEXT_RULES = BASE_RULES + [
    "The line must contain the word 'shortest' (for example 'shortest route', 'shortest sequence', 'shortest way') in "
    "connection with getting to the goal. Refer to the choices as calls (or moves, or actions) of the agent.",
]
MEANING = {
    TX.HEAD_VERDICT: ("A question line about a brief plan of tool calls. The reader has the tools' rules, a start state and "
                      "a goal, and must pick from a list of verdict options shown beneath the line. The line asks which "
                      "verdict describes what comes of the plan when it is checked and run against those rules. It names "
                      "no verdict."),
    TX.HEAD_NEXT: ("A question line about an agent that has already made some tool calls. The reader has the tools' rules "
                   "and a goal, and must pick one call from a set of calls shown beneath the line. The line asks which "
                   "call the agent should make from this point: the call that can be made right away and starts a "
                   "shortest possible sequence of calls that makes the whole goal true."),
}
STYLES = {
    TX.HEAD_VERDICT: [
        "open with the word Which", "open with the word What", "open with the word How", "open with a verb such as Pick, "
        "Select, Choose, Name, Decide or State, then a question word", "address a reviewer with a short lead-in before the "
        "question word", "speak of a dry run of the plan", "speak of auditing or checking the plan against the tools' rules",
        "speak of simulating the plan from the start state", "formal register, one longer clause", "casual short register, "
        "eight words or fewer", "speak of what the plan comes to", "speak of how the plan turns out when carried out",
        "speak of tracing the plan call by call", "speak of the verdicts shown beneath the line", "speak of a planner "
        "handing over the plan for a check", "speak of a runner executing the plan"],
    TX.HEAD_NEXT: [
        "open with the word Which", "open with the word What", "open with the word How", "open with a verb such as Pick, "
        "Select, Choose, Name, Decide or State, then a question word", "address the agent with a short lead-in before the "
        "question word", "speak of a route to the goal", "speak of a sequence of calls", "speak of the way to the goal",
        "formal register, one longer clause", "casual short register, ten words or fewer", "speak of the state the "
        "agent is in at this point", "speak of calls the agent has made so far", "speak of a planner choosing a move",
        "speak of the calls shown beneath the line", "speak of a scheduler picking a call", "speak of a controller "
        "deciding what to run"],
}
PROMPT = (
    "You write short question lines for a test of workflow checking. In the test an AI agent sees a compact toolbox "
    "(each tool lists what it needs, adds and removes), a start state, a goal, and then a plan or a list of calls made so "
    "far. One question line sits under that material and a list of answer options sits under the line. You see none of the "
    "test items and no options. Each item below gives the exact meaning one line must have, its rules and a style hint. "
    "Write ONE line per item, following that item's meaning, rules and style hint. Every line you write must differ from "
    "every other line you write in its words and in its sentence pattern, not only in a swapped synonym. Do not copy the "
    "wording of the brief. Do not open, read or look for any other file. Write the answer file with the Write tool and "
    "nothing else.")
ANSWER_FORMAT = ('The answer is ONE JSON list with exactly N entries, one per item, in any order, each carrying that item\'s '
                 'qid: [{"qid": "<the item qid>", "text": "<the question line>"}, ...]. Write nothing else in the file. '
                 'The lines contain no quotation marks.')


def _items(head: str) -> list:
    out = []
    styles = STYLES[head]
    rules = VERDICT_RULES if head == TX.HEAD_VERDICT else NEXT_RULES
    for i in range(N_PER_HEAD):
        iid = f"t44.wording.{QFORM[head]}.{i:03d}"
        out.append((iid, {"brief": MEANING[head], "slots": [], "rules": rules + [f"Style hint: {styles[i % len(styles)]}."]}))
    return out


def build_batches() -> dict:
    """{head: (TaskBatch, plan)} in memory. Asserts every held-out quota is 0 (A57 c)."""
    assert all(v == 0 for v in HELD_OUT_QUOTAS.values()), HELD_OUT_QUOTAS
    forbid = tuple(w for ws in TX.WORDINGS.values() for w in ws)
    out = {}
    for head in HEADS:
        items = _items(head)
        plan = {iid: {"role": "wording", "head": head, "held_out": False, "dev_only": False} for iid, _ in items}
        b = chunker.make_batch("author_wording", FAMILY, items, seed=f"{SEED}|{QFORM[head]}", prompt=PROMPT,
                               max_items=CHUNK, forbid_strings=forbid)
        out[head] = (b, plan)
    return out


# ---------------------------------------------------------------------------------------------- admission (drops only)
def check_wording(head: str, text, seen_norm=None, seen_sets=None) -> list:
    """Problems of one authored wording (empty = admitted by program). Nothing is rewritten."""
    if not isinstance(text, str):
        return ["not a string"]
    probs = []
    t = text.strip()
    if t != text or "\n" in t or "  " in t:
        probs.append("whitespace or line break")
    t = " ".join(t.split())
    ws = re.findall(r"[A-Za-z']+", t)
    if not (MIN_WORDS <= len(ws) <= MAX_WORDS):
        probs.append(f"{len(ws)} words (need {MIN_WORDS}-{MAX_WORDS})")
    if not t.endswith("?") or t.count("?") != 1 or re.search(r"[.!;:]", t):
        probs.append("not one sentence ending with one question mark")
    if re.search(r"[\d{}\[\]()\"`<>_/\\|@#$%&*=+~^]", t) or "'" in t.replace("'s", "") or "’" in t:
        probs.append("digit, bracket, quote or symbol")
    if t[:1].islower() or re.search(r"(?<!^)\b[A-Z]", t[1:]):
        probs.append("capital letter outside the first")
    if YESNO_START_RX.search(t):
        probs.append("yes/no opening")
    if LABEL_RX.search(t):
        probs.append("label word")
    if head == TX.HEAD_VERDICT and VERDICT_LEAK_RX.search(t):
        probs.append("outcome-hinting word")
    if EXTRA_BAN_RX.search(t):
        probs.append("banned word")
    if not CUE[head].search(t):
        probs.append("meaning cue missing")
    if not CUE2[head].search(t):
        probs.append("meaning cue 2 missing")
    c = negcount.count(t)
    if (c.k_all, c.k_syn) != (0, 0):
        probs.append(f"negation profile {(c.k_all, c.k_syn)}")
    try:
        sk = K.make_skin("chk", FAMILY, t, {}, kind="wording", register="question", qform=QFORM[head])
        probs += [f"G-SL {v.rule}: {v.detail}" for v in gsl.lint_template(sk, label_words=TX.LABEL_WORDS)]
    except Exception as e:  # noqa: BLE001
        probs.append(f"not a wording: {str(e)[:80]}")
    low = " ".join(ws).lower()
    if low in {" ".join(re.findall(r"[A-Za-z']+", w)).lower() for v in TX.WORDINGS.values() for w in v}:
        probs.append("copy of a program wording")
    if seen_norm is not None:
        if low in seen_norm:
            probs.append("duplicate")
        else:
            wset = set(low.split())
            if seen_sets is not None and any(len(wset & s) / max(1, len(wset | s)) >= 0.85 for s in seen_sets):
                probs.append("near duplicate (word-set Jaccard >= 0.85)")
    if not probs and seen_norm is not None:
        seen_norm.add(low)
        if seen_sets is not None:
            seen_sets.append(set(low.split()))
    return probs


# ---------------------------------------------------------------------------------------------- task files
def task_file_text(b, chunk: dict, answer_abs: str) -> str:
    n = len(chunk["items"])
    return "\n".join([
        f"# Haiku authoring task {chunk['task_id']} (family {FAMILY}, kind {b.kind})", "",
        "Read this whole file. Do not open any other file, list no folder and use no other tool than Read and Write. "
        "When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):", "",
        f"    {answer_abs}", "", f"The answer is one JSON list with exactly {n} entries, one per item below, each carrying "
        "that item's qid.", "", "## Instructions", "", b.prompt, "", "## Answer format", "",
        ANSWER_FORMAT.replace("N entries", f"{n} entries"), "", f"## Items ({n}; one record per line)", "", "```json",
        "[\n" + ",\n".join(json.dumps(it, ensure_ascii=False) for it in chunk["items"]) + "\n]", "```", ""])


def write_tasks(task_root: Path = TASK_ROOT, quarantine: Path = QUARANTINE) -> list:
    tasks = []
    for head, (b, plan) in build_batches().items():
        files = dict(b.files())
        files[f"plan/{b.batch_id}.json"] = json.dumps({"batch_id": b.batch_id, "head": head, "kind": b.kind, "plan": plan},
                                                      indent=1, sort_keys=True) + "\n"
        for c in b.chunks:
            tid = c["task_id"]
            ans = str(quarantine / b.answer_path(tid))
            files[f"tasks/{tid}.md"] = task_file_text(b, c, ans)
            tasks.append({"task_file": str(task_root / f"tasks/{tid}.md"), "answer_file": ans, "kind": b.kind, "head": head,
                          "batch_id": b.batch_id, "task_id": tid, "n_items": len(c["items"]), "prompt_sha": b.prompt_sha,
                          "audit_allowed_read": [str(task_root / f"tasks/{tid}.md")], "audit_allowed_write": [ans]})
        paths.write_files(task_root, files)
    (quarantine / "answers").mkdir(parents=True, exist_ok=True)
    paths.write_json(task_root / "TASKS.json", {"family": FAMILY, "seed": SEED, "n_tasks": len(tasks), "tasks": tasks,
                                                "held_out_quotas": HELD_OUT_QUOTAS, "per_head": N_PER_HEAD,
                                                "round": "a57-round1-wordings"})
    return tasks


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=("plan", "write"))
    a = ap.parse_args(argv)
    if a.cmd == "plan":
        out = {h: {"n_items": len(b.key), "chunks": [len(c["items"]) for c in b.chunks], "prompt_sha": b.prompt_sha}
               for h, (b, _p) in build_batches().items()}
        print(json.dumps(out, indent=1))
        return 0
    t = write_tasks()
    print(json.dumps([{k: x[k] for k in ("task_id", "head", "n_items")} for x in t], indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
