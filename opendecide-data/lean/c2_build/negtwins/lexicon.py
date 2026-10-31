"""negtwins/lexicon.py: Haiku-drafted lexicon entries (truth frames, negative frames, lexical complement pairs), their
static lint and their G-LEX 2/2 admission (like the other families: c2_kit/lexicon.py).

Drafted entry kinds
  pos_frame   an opener that asks whether the clause after it is TRUE ("Is it the case that"); probe relation 'same'
  neg_frame   an opener that asks whether the clause after it is FALSE ("Is it untrue that"); probe 'opposite'
  pair        {pair_id, pos: verb|adj, a: forms, b: forms, cores_a, cores_b}: b is the EXACT complement of a for the
              predicate slot of the cores ("is allowed" / "is prohibited": exactly one holds of any rule); probes:
              LEX_PAIR 'opposite' and DNEG_PAIR 'same'
Forms: verb pairs a / b = {base, s3, past, pp}; adjective pairs a / b = {base, adj} with base == adj.

Admission (G-LEX): the static lint passes AND two independent Haiku reads (separate seeds and chunks) pick the expected
relation on every probe (3 probes per frame, 2 per pair direction + 1 double-negation probe). Any other pick REJECTS the
entry for good (no re-vote). The program rewrites every probe with core.rewrite, so the reader sees exactly the
wording the catalogue would produce.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from . import core as C
from . import probe_bank as PB

HERE = Path(__file__).resolve().parent
ADMITTED_FILE = HERE / "lexicon" / "admitted.json"
PROBES_PER_FRAME = 3
PROBES_PER_DIRECTION = 2
N_CORES_PER_SIDE = 10
LOCAL_BANS = (r"\bbe rejected\b", r"\bIs it wrong to answer\b", r"\bonly non-", r"\bShould the statement that\b",
              r"\bIs the correct answer\b")
NEG_FRAME_WORDS = ("false", "untrue", "incorrect", "wrong", "mistaken", "not the case", "inaccurate", "unfounded")
OPENERS = ("Is", "Would", "Does", "Could", "Can")


_POS_OK = re.compile(r"^(?:Is it|Would it be) (?:(?:true|correct|accurate|right)(?: to say)?|so|the case) that$")
_NEG_OK = re.compile(r"^(?:Is it|Would it be) (?:false|untrue|incorrect|wrong|mistaken|inaccurate)(?: to say)? that$")
_NP_ADJ = re.compile(r"^(?:Is|Would|Does|Can|Could) (?:the|a|an|this|that|these|those)\b.* (?:true|correct|accurate|right|false|"
                     r"untrue|incorrect|wrong|mistaken|inaccurate) that$")


def a48h_frame_problems(frame: str, kind: str) -> list:
    """Ruling A48 (h): a frame is "(Is it | Would it be) <truth word> [to say] that" and nothing else. The subject is 'it' (no
    reviewer, report, record, claim: (iii) subject change), no evidential or source word (show, establish, bear out, ...: (iii)),
    no negation of the interrogative (i), and the sentence must be grammatical (iv: "Is the claim wrong that")."""
    if "not" in C.tokens(frame):
        return ["A48h (i): the frame negates the interrogative"]
    ok = _POS_OK if kind == "pos_frame" else _NEG_OK
    if ok.match(frame):
        return []
    if _NP_ADJ.match(frame):
        return ["A48h (iv): ungrammatical frame (noun-phrase subject + truth word + 'that')"]
    return ["A48h (iii): the frame changes the claim's subject or adds an epistemic / source layer"]


def norm_frame(f: str) -> str:
    return " ".join(C.tokens(f))


def lint_frame(frame: str, kind: str, taken: set = frozenset()) -> list:
    probs = []
    if not isinstance(frame, str) or not frame.strip() or frame != frame.strip():
        return ["not a clean string"]
    w = frame.split(" ")
    if w[0] not in OPENERS or not frame.endswith("that") or not 3 <= len(w) <= 8 or "?" in frame or "," in frame:
        probs.append("a frame starts with Is / Would / Does / Could / Can, ends with 'that', has 3-8 words, no ',' or '?'")
    if "n't" in frame:
        probs.append("contracted negative opener (P3)")
    probs += a48h_frame_problems(frame, kind)
    if any(re.search(b, frame, re.I) for b in LOCAL_BANS):
        probs.append("local ban hit")
    k = C.negcount.count(frame).k_all
    if kind == "pos_frame" and k:
        probs.append("a positive frame holds a negation cue")
    if kind == "neg_frame" and not any(n in frame.lower() for n in NEG_FRAME_WORDS):
        probs.append("a negative frame names its negation (false / untrue / incorrect / wrong / mistaken / not the case ...)")
    if kind == "neg_frame" and k > 1:
        probs.append("more than one negation cue in a frame")
    if norm_frame(frame) in taken:
        probs.append("duplicate of a seed, dev or earlier frame")
    return probs


def seed_taken() -> set:
    return {norm_frame(f) for f in C.SEED_POS_FRAMES + C.SEED_NEG_FRAMES + C.DEV_FRAMES}


def lint_pair(pr: dict) -> list:
    probs = []
    try:
        pos, a, b, pid = pr["pos"], pr["a"], pr["b"], pr["pair_id"]
    except KeyError as e:
        return [f"missing {e}"]
    need = ("base", "s3", "past", "pp") if pos == "verb" else ("base", "adj")
    for side, f in (("a", a), ("b", b)):
        if not all(isinstance(f.get(k), str) and f.get(k) and f[k] == f[k].strip().lower() and " " not in f[k]
                   for k in need):
            probs.append(f"side {side} lacks single lower-case words for {need}")
    if probs:
        return probs
    if pos == "adj" and (a["base"] != a["adj"] or b["base"] != b["adj"]):
        probs.append("for an adjective pair base == adj")
    if a["base"] == b["base"] or set(C.tokens(a["base"])) & set(C.tokens(b["base"])):
        probs.append("a and b must be different words")
    C.register_verbs([pr])
    ca, cb = pr.get("cores_a", []), pr.get("cores_b", [])
    if len(ca) < N_CORES_PER_SIDE or len(cb) < N_CORES_PER_SIDE:
        probs.append(f"{N_CORES_PER_SIDE} cores per side are required for the exactness probes")
    cls = "DO" if pos == "verb" else "COP"
    for side, cores in (("a", ca), ("b", cb)):
        for c in cores:
            q = C.parse(c)
            if q is None or q.cls != cls:
                probs.append(f"core {c!r} does not parse as {cls}")
            elif cls == "DO" and q.verb != pr[side]["base"]:
                probs.append(f"core {c!r}: the verb is not {pr[side]['base']!r}")
            elif cls == "COP" and q.rest.split(" ")[0].lower() != pr[side]["adj"]:
                probs.append(f"core {c!r}: the predicate word is not {pr[side]['adj']!r}")
    return probs[:6]


def pair_patterns(pr: dict) -> list:
    """The patterns a pair yields (a>b, b>a, double negation): the directions whose cores all rewrite."""
    cls = "DO" if pr["pos"] == "verb" else "COP"
    out = []
    for d, side in (("a>b", "cores_a"), ("b>a", "cores_b")):
        p = C.make_pattern("LEX_PAIR", cls, pair=pr["pair_id"], direction=d, source="lex")
        if sum(1 for c in pr.get(side, []) if C.apply(c, p, {pr["pair_id"]: pr})[0]) >= N_CORES_PER_SIDE:
            out.append(p)
    return out


# ------------------------------------------------------------------------------------------------ probes (G-LEX)

def _pick(cores: list, key: str, k: int) -> list:
    return sorted(cores, key=lambda c: C.sha(key + "|" + c))[:k]


def frame_probe_items(frames: list, kind: str) -> list:
    """[(internal id, polarity item)]: the frame over a bank core, vs the core itself."""
    items = []
    op = "POS_FRAME" if kind == "pos_frame" else "NEG_FRAME"
    for f in frames:
        cores = _pick(PB.DO + PB.COP, f, PROBES_PER_FRAME * 3)
        got = 0
        for c in cores:
            q = C.parse(c)
            p = C.make_pattern(op, q.cls if q else "DO", frame=f, source="lex")
            t, _ = C.apply(c, p)
            if t and got < PROBES_PER_FRAME:
                items.append((f"glex|{kind}|{C.sha(f)[:10]}|p{got}", {"question_a": c, "question_b": t}))
                got += 1
    return items


def pair_probe_items(pairs: list) -> list:
    items = []
    for pr in pairs:
        pm = {pr["pair_id"]: pr}
        for p in pair_patterns(pr):
            side = "cores_a" if p.direction == "a>b" else "cores_b"
            for i, c in enumerate(_pick(pr[side], pr["pair_id"] + p.direction, PROBES_PER_DIRECTION)):
                t, _ = C.apply(c, p, pm)
                items.append((f"glex|pair|{pr['pair_id']}|{p.direction}|p{i}", {"question_a": c, "question_b": t}))
        cls = "DO" if pr["pos"] == "verb" else "COP"
        dp = C.make_pattern("DNEG_PAIR", cls, frame=C.SEED_POS_FRAMES[0], pair=pr["pair_id"], source="lex")
        c = _pick(pr["cores_a"], pr["pair_id"] + "dneg", 1)[0]
        t, _ = C.apply(c, dp, pm)
        if t:
            items.append((f"glex|pair|{pr['pair_id']}|dneg|p0", {"question_a": c, "question_b": t}))
    return items


EXPECT = {"pos_frame": "same", "neg_frame": "opposite"}


def expected_relation(internal_id: str) -> str:
    parts = internal_id.split("|")
    if parts[1] in EXPECT:
        return EXPECT[parts[1]]
    return "same" if parts[3] == "dneg" else "opposite"


def admit(cands: dict, reads_1: dict, reads_2: dict) -> tuple:
    """cands = {"pos_frames": [...], "neg_frames": [...], "pairs": [...]} (after lint). reads_i = {internal id: relation}
    from the two independent rounds. 2/2 on every probe or the entry is rejected. Returns (admitted, rejected)."""
    adm = {"pos_frames": [], "neg_frames": [], "pairs": []}
    rej = []

    def ok(prefix: str) -> bool:
        ids = [i for i in reads_1 if i.startswith(prefix)]
        return bool(ids) and all(i in reads_2 and reads_1[i] == reads_2[i] == expected_relation(i) for i in ids)
    for key, kind in (("pos_frames", "pos_frame"), ("neg_frames", "neg_frame")):
        for f in cands.get(key, []):
            if ok(f"glex|{kind}|{C.sha(f)[:10]}|"):
                adm[key].append(f)
            else:
                rej.append(f)
    for pr in cands.get("pairs", []):
        if ok(f"glex|pair|{pr['pair_id']}|"):
            adm["pairs"].append(pr)
        else:
            rej.append(pr["pair_id"])
    return adm, rej


def load_admitted(path: Path = ADMITTED_FILE) -> dict:
    if not path.exists():
        return {"pos_frames": [], "neg_frames": [], "pairs": []}
    return json.loads(path.read_text(encoding="utf-8"))


def save_admitted(lex: dict, path: Path = ADMITTED_FILE) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(lex, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
    path.write_text(text, encoding="utf-8")
    return C.sha(text)
