"""families/T40/haiku/author.py: Haiku authoring task files and the admission checker for T40 surface text.

NOT RUN by the build agent. `python -B families/T40/haiku/author.py write` only writes task files (tasks/*.md and
manifest.json); the orchestrator runs one fresh Haiku agent per task file (it may read only its task file and write only its
answer file) and then calls `check_answers(task_id, answers)`. Haiku never sees a gold label, an option or a registry: header
items carry only a register and a {USER} placeholder, wording items only the meaning of one question form. Claude text is never
gold; a Haiku text can only be admitted or rejected here, and an admitted wording still needs the two blind G-LEX reads
(lexicon_items) before the pilot may use it.
Task ids: T40-H-skin-<register>-<n> (header skins, Mode T, one {USER} each) and T40-H-wording-<qform>-<n> (question wordings).
Answer format (both): a JSON array [{"qid": "<item id>", "texts": ["...", ...]}].
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

TASKS = HERE / "tasks"
ANSWER_DIR = HERE.parents[2] / "a57_pool_quarantine" / "T40"   # A57 (d): answers go to the quarantine folder only
PER_ITEM = 6
REGISTERS = ("chat", "ticket", "log", "email", "terminal", "notebook", "transcript", "form")
HELD_OUT_REGISTERS = ("transcript", "form")
ITEMS_PER_REGISTER = 6
N_SKIN_HELD = 0   # A57 (c): held-out-role items are never authored on the C2 side after the freeze
ITEMS_PER_QFORM = 3
BANS = ("Outside the {USER} placeholder never use: digits, number words, dates, times, month or weekday names, URLs, e-mail "
        "addresses, time words (today, now, soon, last, next, earlier, later ...), quantity or quantifier words (all, every, "
        "each, some, any, no, none, only, always, never, several, many, more ...), modal words (must, may, can, should, will, "
        "would, need, allowed, required ...), hedges (maybe, probably, likely, seems ...), status words (done, finished, "
        "approved, open, closed, valid, failed, pending, blocked ...), condition words (if, unless, except, otherwise) and any "
        "negation. Do not name anyone: the only name is {USER}. Every text is one short line of at most twelve words.")
PROMPTS = {
    "skin": ("You write short header lines for a dataset about checking an AI agent's tool calls. Each line only sets the "
             "scene in a given register (who is talking to the agent, in which medium); it states no fact and mentions no tool, "
             "call, request or outcome. Use the placeholder {USER} exactly once in every line, spelled exactly like that. "
             + BANS + " Make the lines of one item clearly different from each other. Read this file only."),
    "wording": ("You write questions for a dataset about checking an AI agent's tool calls and file edits. Each item gives the "
                "meaning of one question and the number of negations it must contain. Write plain English questions that ask "
                "exactly that, each one a single sentence ending with a question mark, without numbers or names, with the "
                "stated number of negation words (not) and no other negative wording (no contractions, no 'fail', 'lack', "
                "'without', 'never'). Make the questions of one item clearly different from each other. Read this file only."),
}
ANSWER = ('Write a JSON array to the answer file, one entry per item, in item order: {"qid": "<the item qid>", "texts": '
          '["<text 1>", "<text 2>", ...]}. Write nothing else in the file.')
# qform -> (meaning shown to Haiku, (k_all, k_syn) the wording must have, regex it must match)
# A63: forms whose meaning text needs a held-out keyword (registry, case) are dropped, not reworded: ya_valid, ya_dneg, ya_reject, ya_notvalid, yb_bdneg, yc_cdneg.
WORDINGS = {
    "yb_call": ("asks whether the agent should make a tool call at once for the request", (0, 0), r"agent|call"),
    "yb_hold": ("asks whether the agent should hold off on a tool call (reply to the user instead)", (0, 0), r"agent"),
    "yb_notcall": ("asks whether the agent should not call a tool at once (one 'not')", (1, 1), r"\bnot\b"),
    "yc_applies": ("asks whether a proposed text edit applies cleanly to a file", (0, 0), r"edit"),
    "yc_fails": ("asks whether the tool refuses or spoils a proposed text edit (no 'not', no 'fail')", (0, 0), r"refuse|spoil|turn"),
    "yc_notapplies": ("asks whether a proposed text edit does not apply cleanly (one 'not')", (1, 1), r"\bnot\b"),
    "ca_diag": ("asks which verdict a proposed tool call deserves", (0, 0), r"verdict|label|judge"),
    "cb_action": ("asks what the agent should do with a request", (0, 0), r"agent"),
    "cc_edit": ("asks what happens when a proposed edit runs", (0, 0), r"edit"),
}
BAN_WORDING = re.compile(r"\b(?:valid|invalid|nonexistent|ambiguous|borrowed|ungrounded|followup|n't|fail\w*|lack\w*|without|never)\b", re.I)


def skin_items() -> list:
    out = []
    for reg in REGISTERS:
        for j in range(ITEMS_PER_REGISTER if reg not in HELD_OUT_REGISTERS else N_SKIN_HELD):
            out.append((f"T40-H-skin-{reg}-{j}", reg, {
                "brief": f"Write {PER_ITEM} different one-line headers for a {reg} (register: {reg}) in which {{USER}} is talking to "
                         f"an assistant agent. Use {{USER}} exactly once in every line."}))
    return out


def wording_items() -> list:
    out = []
    for qf, (meaning, neg, _rx) in WORDINGS.items():
        for j in range(ITEMS_PER_QFORM):
            out.append((f"T40-H-wording-{qf}-{j}", qf, {
                "brief": f"Write {PER_ITEM} different questions. Meaning: it {meaning}. Negation words (not) required: {neg[1]}."}))
    return out


def write_tasks() -> list:
    TASKS.mkdir(exist_ok=True)
    manifest = []
    for kind, items in (("skin", skin_items()), ("wording", wording_items())):
        chunk = [items[i:i + 12] for i in range(0, len(items), 12)]
        for n, ch in enumerate(chunk):
            tid = f"T40-H-{kind}-chunk{n:02d}"
            body = [f"# Task {tid}", "", PROMPTS[kind], "", ANSWER, "", "Answer file: " + str(ANSWER_DIR / (tid + ".json")), "", "## Items"]
            for qid, _key, it in ch:
                body += [f"- qid `{qid}`: {it['brief']}"]
            (TASKS / f"{tid}.md").write_text("\n".join(body) + "\n", encoding="utf-8")
            manifest.append({"task_id": tid, "kind": kind, "items": [c[0] for c in ch]})
    (TASKS / "manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    return manifest


# ------------------------------------------------------------------------------------------------ admission checks

def admit_skin(text: str, register: str, label_words: tuple = ()) -> list:
    """Problems of one header text (empty = admitted): the kit's G-SL template lint and exactly one {USER}."""
    from c2_kit.skin import make_skin
    from c2_kit import gsl
    if text.count("{USER}") != 1:
        return ["needs exactly one {USER}"]
    try:
        sk = make_skin("check", "T40", text, {"USER": "name"}, register=register)
    except Exception as e:  # noqa: BLE001
        return [f"not a skin: {e}"]
    probs = [f"{v.rule}: {v.detail}" for v in gsl.lint_template(sk, label_words=label_words)]
    if len(text.split()) > 12:
        probs.append("more than twelve words")
    return probs


def admit_wording(qform: str, text: str) -> list:
    """Problems of one question wording (empty = admitted): negation profile, meaning cue, no label word, G-SL lint."""
    import negcount
    from c2_kit.skin import make_skin
    from c2_kit import gsl
    meaning, (k_all, k_syn), rx = WORDINGS[qform]
    probs = []
    c = negcount.count(text)
    if (c.k_all, c.k_syn) != (k_all, k_syn):
        probs.append(f"negation profile {(c.k_all, c.k_syn)} != {(k_all, k_syn)}")
    if not re.search(rx, text, re.I):
        probs.append("meaning cue missing")
    if BAN_WORDING.search(text):
        probs.append("banned word")
    end = "?" if qform.startswith("y") else "?."
    if text[-1:] not in end or text.count("?") + text.count(".") != 1:
        probs.append("one sentence ending with ? (choice forms may be an instruction ending with .)")
    try:
        sk = make_skin("check", "T40", text, {}, kind="wording", register="question", qform=qform)
        probs += [f"{v.rule}: {v.detail}" for v in gsl.lint_template(sk)]
    except Exception as e:  # noqa: BLE001
        probs.append(f"not a wording: {e}")
    return probs


def check_answers(task_id: str, answers: list) -> dict:
    """{qid: {"admitted": [texts], "rejected": [(text, problems)]}} for one answer file."""
    res = {}
    for a in answers:
        qid = a["qid"]
        parts = qid.split("-")
        kind, key = parts[2], parts[3]
        ok, bad, seen = [], [], set()
        for t in a["texts"]:
            probs = admit_skin(t, key) if kind == "skin" else admit_wording(key, t)
            if t.lower() in seen:
                probs = probs + ["duplicate"]
            seen.add(t.lower())
            (bad if probs else ok).append(t if not probs else (t, probs))
        res[qid] = {"admitted": ok, "rejected": bad}
    return res


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "write":
        print(len(write_tasks()), "task files written to", TASKS)
    else:
        print(__doc__)
