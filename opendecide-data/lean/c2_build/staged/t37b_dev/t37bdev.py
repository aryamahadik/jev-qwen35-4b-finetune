"""staged/t37b_dev/t37bdev.py: T37b-dev build for C2 (draft ruling A70; spec 3.18 / 7.1 / 7.2 (d)).

Everything is written under c2_build/staged/t37b_dev/. Nothing is written into data/. No G13 job is run or touched.

State machine (each stage is a CLI command, `python -B staged/t37b_dev/t37bdev.py <stage>` from c2_build, HF_HUB_OFFLINE=1):

  stage1   pool + plan order frozen + frame-authoring tasks (Haiku) + subject-decomposition tasks (Haiku, two reads)
  frames2  read the authoring answers, lint (A70 c), decontamination scan, write the G-LEX probe tasks (round A)
  frames3  read both G-LEX rounds, admit 2/2, freeze the frames (sha256 logged), complete the plan (frame per entry)
  ...      (pairs, polarity, solver, review, finish: see README.md in this folder)

Design notes (A70):
  * Bases are the rows of the 9 gate dev splits that pass the (d) filters (program only, counts logged in POOL_REPORT).
  * The partner differs from the base in id, role, gold, instructions and meta only; the instructions are
    pre + partner span + post, where the partner span is  "<frame>[, <lead>,] <subject> <aux> not <rest>?"
    (polarity programs A and B of t37b/ both read it on the question span, with a pseudo entry whose subject rule is the
    Haiku-read subject). The subject comes from two independent Haiku reads that must agree exactly.
  * Order of the plan is frozen (hash logged) before any Haiku read of a base; the frame per entry is a hash of the plan key
    and the base id over the frozen frames, fixed when the frames are frozen (before any partner exists).
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent                  # c2_build/staged/t37b_dev
C2_BUILD = HERE.parents[1]                              # c2_build
LEAN = C2_BUILD.parent
for _p in (str(C2_BUILD), str(LEAN)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from c2_kit import chunker, paths  # noqa: E402
import negcount  # noqa: E402
from negtwins import core as C  # noqa: E402
from negtwins import lexicon as L  # noqa: E402
from negtwins import frozen as FZ  # noqa: E402
from negtwins import heldout as H  # noqa: E402
from negtwins import probe_bank as PB  # noqa: E402
from t37b import polarity as PA  # noqa: E402
from t37b import polarity_b as PB_  # noqa: E402
from t37b import sources as SRC  # noqa: E402

KEY = "t37b-dev-a70-v1"
FAMILY = "T37BDEV"
SPLITS9 = "dev_nc,taskbank_dev,hard_dev,dev_negwords,dev_claims,pg_dev,devzs,devp_card,dev".split(",")
N0 = 350                      # initial plan entries (A70 e: first 300 survivors in plan order are kept)
N_EXT = 150                   # the one allowed extension
N_KEEP = 300
SOURCE_CAP = 45               # 15% of 300
FRAME_CAP = 120               # 40% of 300
MIN_FRAMES = 3
CHUNK = 50
PREREG_N_TRAINED = 379
SHA_TRAINED = "c6045501940af817aecd5bb239579bd02460e8d60dee17769aa35eceeca62a67"
SHA_HELDOUT = "92aff6e0475d7628796c7be6c136c659a3c26336eda99006575951b7a0adf039"
SHA_GPROXY_REPORT_PREFIX = "f229e75925a07ab3"

# ------------------------------------------------------------------------------------------------ small helpers


def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def now_utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def file_sha(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def jdump(obj) -> str:
    return json.dumps(obj, indent=1, sort_keys=True, ensure_ascii=False) + "\n"


def write_here(rel: str, text: str) -> Path:
    """Write a file under staged/t37b_dev/ only (never data/, never a never-open path)."""
    p = (HERE / rel).resolve()
    if not str(p).startswith(str(HERE) + os.sep):
        raise PermissionError(f"outside staged/t37b_dev: {p}")
    paths.check_path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def read_here(rel: str):
    return json.loads((HERE / rel).read_text(encoding="utf-8"))


def refuse_overwrite(rel: str) -> None:
    if (HERE / rel).exists():
        raise FileExistsError(f"{rel} is frozen; never re-written")


# ------------------------------------------------------------------------------------------------ (d) bases: pool

# Source classes (A70 d). Natively 2-class, one-vs-rest over a nominal label set, or a program-defined predicate.
# Never a neutral / middle / ordinal / polar label set, never LLM-written gold; an unclear source is excluded.
SOURCE_CLASS = {
    "rotten_tomatoes": "native_2class", "irony": "native_2class", "spam": "native_2class", "hate": "native_2class",
    "clinc150": "nominal_one_vs_rest", "banking77": "nominal_one_vs_rest", "bbc": "nominal_one_vs_rest",
    "ag_news": "nominal_one_vs_rest", "emotion": "nominal_one_vs_rest", "tb_mixtral": "nominal_one_vs_rest",
    "tb_label_nli": "nominal_one_vs_rest",
    "pg_temporal": "program_defined", "pg_numeric": "program_defined", "pg_policy": "program_defined",
    "pg_multihop": "program_defined", "pg_evidence": "program_defined", "pg_routing": "program_defined",
    "pg_conflict": "program_defined",
}
SOURCE_EXCLUDED = {"climate": "neutral label in its card (risk / opportunity / neutral)",
                   "cb": "neutral label (3-class NLI); its cards also name yes/no"}
HARD_PREFIX_EXCLUDED = "hard_"          # hard_dev rows: Claude-written gold (97 aff rows)
YESNO_RE = re.compile(r"\b(yes|no)\b", re.I)
_BOUND = re.compile(r"[.!?;:][\"”)\]]?\s+|\n")
PRONOUN_SUBJECTS = frozenset({"that", "this", "it", "he", "she", "they", "these", "those", "there", "one", "we", "you",
                              "i", "who", "which", "what"})
CLS_OF_AUX = {**{a: "DO" for a in ("does", "do", "did")}, **{a: "COP" for a in ("is", "are", "was", "were")},
              **{a: "HAVE" for a in ("has", "have", "had")}}


def load_split(split: str) -> list:
    """[(row dict, raw line)] of data/<split>.jsonl (never data/ohs*; the 9 gate dev splits only)."""
    if split not in SPLITS9:
        raise ValueError(split)
    p = LEAN / "data" / f"{split}.jsonl"
    paths.check_path(p)
    out = []
    for line in p.read_text(encoding="utf-8").split("\n"):
        if line.strip():
            out.append((json.loads(line), line))
    return out


def question_span(instr: str):
    """(pre, span, post): the sentence that holds the one '?' (boundaries inside double quotes do not split)."""
    q = instr.index("?")
    st = 0
    for m in _BOUND.finditer(instr[:q]):
        if instr[:m.end()].rstrip().count('"') % 2 == 1:
            continue
        st = m.end()
    return instr[:st], instr[st:q + 1], instr[q + 1:]


def split_span(span: str):
    """(prefix, aux as written, after) by program A's rule (first auxiliary; a fronted prefix ends with ', ' and starts
    upper case) or None. `after` is the text after the auxiliary, without the final '?'."""
    m = PA._FIRST_AUX.search(span)
    if not m or not span.endswith("?") or span.count("?") != 1:
        return None
    prefix, aux = span[:m.start()], m.group(0)
    if prefix and (not prefix.endswith(", ") or not prefix[0].isupper()):
        return None
    if not prefix and not aux[0].isupper():
        return None
    after = span[m.end():]
    if not after.startswith(" "):
        return None
    return prefix, aux, after[1:-1]


def base_filters(r: dict, split: str) -> tuple:
    """(reason or None, info). Program filters of A70 (d) in a fixed order; the first failing filter names the row."""
    m = r.get("meta") or {}
    if r.get("qtype") != "noul" or r.get("gold") not in (0, 1) or isinstance(r.get("gold"), bool):
        return "not_yes_no_hard_gold", None
    if "gold_probs" in r or any(k in m for k in ("teacher", "gold_probs", "attack_target")):
        return "soft_gold", None
    if r.get("role") != "aff":
        return "role_not_aff", None
    ins = r.get("instructions") or ""
    if ins.count("?") != 1:
        return "not_one_question_mark", None
    if YESNO_RE.search(r.get("card") or ""):
        return "card_mentions_yes_no", None
    src = r.get("source") or ""
    if src.startswith(HARD_PREFIX_EXCLUDED):
        return "llm_written_gold", None
    if src in SOURCE_EXCLUDED:
        return "source_neutral_label", None
    if src not in SOURCE_CLASS:
        return "source_unclear", None
    pre, span, post = question_span(ins)
    if pre + span + post != ins or "\n" in span or not span[:1].isupper() or span.endswith('"?'):
        return "span_not_clean", None
    sp = split_span(span)
    if sp is None:
        return "no_aux_split", None
    prefix, aux, after = sp
    cls = CLS_OF_AUX.get(aux.lower())
    if cls is None:
        return "class_not_do_cop_have", None
    if negcount.count(span).k_all:
        return "question_negcount_not_0", None
    return None, {"pre": pre, "span": span, "post": post, "prefix": prefix, "aux": aux.lower(), "cls": cls,
                  "after": after}


def build_pool() -> tuple:
    """(pool entries, report). A pool entry per candidate row; one pair per group_id happens in the plan."""
    pool, rep = [], {"splits": {}, "filters": Counter(), "n_rows_total": 0}
    for sp in SPLITS9:
        rows = load_split(sp)
        rep["splits"][sp] = len(rows)
        for r, raw in rows:
            rep["n_rows_total"] += 1
            why, info = base_filters(r, sp)
            rep["filters"][why or "PASS"] += 1
            if why is None:
                pool.append({"base_id": r["id"], "split": sp, "source": r["source"], "group_id": r["group_id"],
                             "gold": r["gold"], "raw_sha": sha(raw), **info})
    rep["filters"] = dict(rep["filters"])
    rep["n_pool_rows"] = len(pool)
    rep["n_pool_groups"] = len({e["group_id"] for e in pool})
    rep["pool_by_source"] = dict(Counter(e["source"] for e in pool))
    rep["pool_by_class"] = dict(Counter(e["cls"] for e in pool))
    rep["pool_by_split"] = dict(Counter(e["split"] for e in pool))
    ids = [e["base_id"] for e in pool]
    rep["n_unique_ids"] = len(set(ids))
    return pool, rep


def make_plan(pool: list, key: str = KEY) -> list:
    """The seeded plan order: one entry per group_id (the member with the smallest hash), all groups sorted by the hash of
    (key, base id). No gold, no frame, no model read is used."""
    best = {}
    for e in pool:
        h = sha(f"{key}|{e['base_id']}")
        g = e["group_id"]
        if g not in best or h < best[g][0]:
            best[g] = (h, e)
    ordered = sorted(best.values(), key=lambda x: x[0])
    return [{"pos": i, "base_id": e["base_id"], "split": e["split"], "source": e["source"], "group_id": e["group_id"],
             "cls": e["cls"], "span_sha": sha(e["span"]), "order_hash": h[:16]} for i, (h, e) in enumerate(ordered)]


# ------------------------------------------------------------------------------------------------ frames (A70 c)

OPENERS_A = ("Is it", "Would it be", "Does it", "Would it")
# the 12 item-7 truth words (6 positive, 6 negative) and their listed variants: a tier-A frame holds none of them
TRUTH_EXACT = frozenset({"true", "truth", "truly", "truthful", "truthfully", "untrue", "untruth", "correct", "correctly",
                         "correctness", "incorrect", "incorrectly", "accurate", "accurately", "accuracy", "inaccurate",
                         "inaccurately", "inaccuracy", "right", "rightly", "rights", "wrong", "wrongly", "wrongful",
                         "false", "falsely", "falsehood", "mistaken", "mistakenly", "mistake", "so", "case", "cases"})
# closed epistemic / evidential / source / inference list (A48 h iii): none of these words, as whole words or stems
EPISTEMIC_STEMS = ("establish", "show", "prov", "demonstrat", "indicat", "suggest", "impl", "evid", "clear", "obvious",
                   "apparent", "certain", "sure", "know", "believ", "think", "thought", "assum", "likel", "probab",
                   "possib", "plausib", "credib", "reasonabl", "confirm", "verif", "report", "record", "sourc",
                   "claim", "statement", "document", "text", "passage", "author", "review", "agree", "argu", "assert",
                   "state", "reveal", "seem", "appear", "guess", "suppos", "expect", "presum", "realis", "recogn",
                   "accept", "admit", "mean", "follow", "entail", "necessar", "lead", "result", "turn", "emerg",
                   "transpir", "surely", "doubt", "uncertain", "opinion", "view", "judg", "consider", "regard",
                   "deem", "told", "tell", "hear", "heard", "rumo", "publish", "witness", "found", "find",
                   "discover", "learn", "determin", "accord", "reportedly", "allegedly", "safe", "trust", "perceiv")
PRONOUNS_A = frozenset({"he", "she", "they", "we", "you", "i", "one", "someone", "anyone", "everyone", "people",
                        "reviewer", "reader", "analyst", "expert", "judge", "court", "experts", "everybody", "somebody",
                        "anybody", "me", "us", "them", "him", "her", "his", "their", "our", "your", "my", "its"})
FILLER_OK = frozenset({"it", "that", "to", "be", "a", "an", "the", "of", "on", "in", "as", "for", "at", "by", "with", "up"})


def surfaces_44_exact() -> set:
    """The enumeration the ruling counts as 44: 4 positive words x (plain, 'to say') + so + 'the case' = 10 per opener
    and 6 negative words x (plain, 'to say') = 12 per opener, two openers. 'so' and 'the case' take no 'to say'."""
    pos = ["true", "correct", "accurate", "right"]
    neg = ["false", "untrue", "incorrect", "wrong", "mistaken", "inaccurate"]
    out = set()
    for op in ("Is it", "Would it be"):
        for w in pos + neg:
            out.add(f"{op} {w} that")
            out.add(f"{op} {w} to say that")
        out.add(f"{op} so that")
        out.add(f"{op} the case that")
    return {" ".join(C.tokens(s)) for s in out}


def known_surfaces() -> set:
    """Every normalised frame a T37b-dev frame must differ from: the 44 surfaces, FRAMES_TRAIN, the seed positive and
    negative frames, the 3 FRAMES_DEV, the admitted training lexicon, the realised held-out frames and the frames of the
    379 trained patterns."""
    s = set(surfaces_44_exact())
    for f in tuple(C.SEED_POS_FRAMES) + tuple(C.SEED_NEG_FRAMES) + tuple(C.DEV_FRAMES):
        s.add(" ".join(C.tokens(f)))
    lex = L.load_admitted()
    for f in lex.get("pos_frames", []) + lex.get("neg_frames", []):
        s.add(" ".join(C.tokens(f)))
    try:
        for v in json.loads(H.REALISED_FILE.read_text(encoding="utf-8")).values():
            if isinstance(v, str):
                s.add(" ".join(C.tokens(v)))
    except FileNotFoundError:
        pass
    try:
        pats, _ = FZ.load_trained()
        for p in pats:
            if p.frame:
                s.add(" ".join(C.tokens(p.frame)))
    except Exception:       # noqa: BLE001  (the tests may run without the frozen files)
        pass
    return s


def _banned_word(tok: str, tier: str) -> str | None:
    if tier == "A" and tok in TRUTH_EXACT:
        return f"truth word {tok!r}"
    if tier == "A" and (tok.startswith("right") or tok.startswith("correct") or tok.startswith("accura") or
                        tok.startswith("true") or tok.startswith("truth") or tok.startswith("fals") or
                        tok.startswith("wrong") or tok.startswith("mistak")):
        return f"truth word variant {tok!r}"
    for st in EPISTEMIC_STEMS:
        if tok == st or (len(st) >= 4 and tok.startswith(st)):
            return f"closed epistemic / evidential / source list: {tok!r}"
    return None


def a70_frame_problems(frame: str, tier: str = "A", taken: set | None = None) -> list:
    """A70 (c): the rules checked by program. [] = admitted to G-LEX."""
    if not isinstance(frame, str) or not frame.strip() or frame != frame.strip() or "\n" in frame:
        return ["not a clean one-line string"]
    probs = []
    w = frame.split(" ")
    opener = next((o for o in sorted(OPENERS_A, key=len, reverse=True) if frame.startswith(o + " ")), None)
    if opener is None:
        probs.append("opener is not one of Is it / Would it be / Does it / Would it")
    if not frame.endswith(" that") or w[-1] != "that":
        probs.append("must end with the word 'that'")
    if not 3 <= len(w) <= 8:
        probs.append("3-8 words")
    if "?" in frame or "," in frame or "n't" in frame or "’" in frame or "'" in frame or '"' in frame:
        probs.append("no '?', ',', apostrophe, quote or n't")
    if re.search(r"[0-9]", frame):
        probs.append("no digits")
    toks = C.tokens(frame)
    if "not" in toks or {"no", "never", "nor", "neither", "without", "none", "nothing", "nobody"} & set(toks):
        probs.append("A48h (i): the frame holds a negation word")
    if {"can", "could"} & set(toks):
        probs.append("A48h (ii): 'can' / 'could'")
    if negcount.count(frame).k_all:
        probs.append("negcount > 0")
    if any(re.search(b, frame, re.I) for b in L.LOCAL_BANS):
        probs.append("local ban hit")
    if set(toks) & PRONOUNS_A:
        probs.append("A48h (iii): a subject other than the expletive 'it'")
    # the only 'say' allowed is the final 'to say that'
    for i, t in enumerate(toks):
        if t in ("say", "says", "said", "saying") and not (i >= 1 and toks[i - 1] == "to" and toks[i + 1:] == ["that"]):
            probs.append("'say' only as 'to say that'")
    body = toks[len(C.tokens(opener or "")):-1] if opener else toks
    if not body:
        probs.append("nothing between the opener and 'that'")
    for t in toks:
        if t in FILLER_OK or t in ("is", "would", "does", "it", "be", "that"):
            continue
        why = _banned_word(t, tier)
        if why:
            probs.append(why)
    if taken is not None and " ".join(toks) in taken:
        probs.append("normalised surface is among the 44 surfaces, FRAMES_TRAIN, the seeds or another known frame")
    return probs


FRAME_AUTHOR_PROMPT = (
    "You write question openers for a reading test. Each item gives a brief and rules. Write exactly what the brief and "
    "rules ask for and nothing else. Never answer a question and never add facts. Reply with JSON only: a list with one "
    "object per item, {\"qid\": <the item's qid>, \"frames\": [<string>, ...]}. Every string is plain text on one line.")

_FRAME_RULES = [
    "Each opener is a plain string of 3 to 8 words, with no comma, no question mark, no apostrophe, no quote mark and no digit.",
    "The only subject of an opener is the word 'it'. An opener never names a person, a document, a reviewer, a report or a claim.",
    "Each opener asks whether the clause that will follow it holds as stated; a yes would mean that clause holds. It does not "
    "change the meaning of that clause, add doubt, or add anyone's opinion, evidence, knowledge or source.",
    "An opener never contains a negation word (not, no, never, without) and never contains 'can' or 'could'.",
    "Do not use any of these words or their forms: true, truth, truly, correct, accurate, right, wrong, false, untrue, incorrect, "
    "mistaken, inaccurate, so, case.",
    "Do not use words about evidence, knowledge, belief, reports or sources (show, prove, establish, indicate, suggest, evidence, "
    "certain, sure, known, think, believe, likely, possible, clear, obvious, report, record, source, claim, statement, text, review).",
    "An opener must be grammatical when a full clause is put right after it, for example: '<opener> the notice lists a fee' and "
    "'<opener> the shop is open on Sundays'.",
    "The openers of one item use different middle words; do not only swap one synonym.",
]
_FRAME_STYLES = ("plain everyday words", "formal register", "short and direct", "as used in notices and forms")


def frame_author_items() -> list:
    """12 items: 4 openers x 3 styles. Each asks for 6 openers (72 candidates before lint, G-LEX and decontamination)."""
    items = []
    for oi, op in enumerate(OPENERS_A):
        for si, st in enumerate(_FRAME_STYLES[:3]):
            brief = (f"Write 6 different question openers. Each one starts with the words '{op}' and ends with the word 'that', "
                     f"with 1 to 5 other words in between. Style: {st}.")
            items.append((f"a70|frames|{oi}|{si}", {"brief": brief,
                                                     "meaning": "asks whether the clause that follows holds as stated, and nothing else",
                                                     "slots": [], "rules": _FRAME_RULES}))
    return items


# ------------------------------------------------------------------------------------------------ decomposition (subject)

DECOMP_PROMPT = (
    "Each item holds one yes/no question. Find its grammatical subject: the words right after the question's first "
    "auxiliary verb (is, are, was, were, does, do, did, has, have, had; any introductory phrase before that verb is "
    "skipped), up to the predicate (the main verb, or the word or phrase the auxiliary links the subject to). Copy the "
    "subject exactly as written, letters and punctuation included, and give next_word, the single word that follows the "
    "subject in the question. If the question has no subject of this kind (for example it starts with 'there', has no "
    "auxiliary, or you are not sure where the subject ends), reply with an empty subject and an empty next_word. Reply "
    "with JSON only: a list of objects {\"qid\": <qid>, \"subject\": \"<exact words>\", \"next_word\": \"<one word>\"}.")
DECOMP_FORMAT = '[{"qid": "q...", "subject": "the exact words", "next_word": "word"}, ...]'
chunker.TASK_KINDS.setdefault("t37bdev_decompose", ("question",))


def subject_check(span: str, subject: str, next_word: str):
    """(problems, parts). parts = (prefix, aux as written, subject, rest) when the Haiku subject sits right after the first
    auxiliary and the next word matches; else None."""
    sp = split_span(span)
    if sp is None:
        return ["no auxiliary split"], None
    prefix, aux, after = sp
    if not isinstance(subject, str) or not subject or subject != subject.strip() or not isinstance(next_word, str):
        return ["empty or unclean subject"], None
    if not after.startswith(subject + " "):
        return ["the subject does not sit right after the auxiliary"], None
    rest = after[len(subject) + 1:]
    if not rest.strip():
        return ["nothing after the subject"], None
    first = rest.split(" ")[0]
    if next_word.strip().strip(".,;:!?\"'()").lower() != first.strip(".,;:!?\"'()").lower():
        return ["next_word does not match"], None
    if subject.lower() in PRONOUN_SUBJECTS:
        return ["bare pronoun / deictic subject"], None
    if len(subject.split(" ")) > 14:
        return ["subject longer than 14 words"], None
    return [], (prefix, aux, subject, rest)


def partner_span(frame: str, parts: tuple) -> str:
    prefix, aux, subject, rest = parts
    lead = f", {prefix[0].lower()}{prefix[1:-2]}," if prefix else ""
    return f"{frame}{lead} {subject} {aux.lower()} not {rest}?"


def pseudo_entry(span: str, subject: str):
    return SRC.Entry(source="t37bdev", qid=sha(span)[:10], pattern=re.escape(span), kinds=("syntactic",),
                     subject=re.escape(subject))


def program_readings(span: str, subject: str, frame: str, partner: str) -> tuple:
    """Both independent polarity programs (A: negcount based, B: token edit script) on the question span. Returns
    (a, b, problems); a pair passes only when both say 'opposite'."""
    e = pseudo_entry(span, subject)
    a, pa = PA.classify_a(span, partner, "syntactic", e, frames=(frame,))
    b, pb = PB_.classify_b(span, partner, "syntactic", e, frames=(frame,))
    return a, b, pa + pb


# ------------------------------------------------------------------------------------------------ task writing

def task_text(batch, chunk: dict, root: Path, *, title: str, answer_format: str) -> str:
    ans = root / batch.answer_path(chunk["task_id"])
    n = len(chunk["items"])
    return "\n".join([
        f"# {title} {chunk['task_id']} (family {FAMILY}, kind {chunk['kind']})", "",
        "Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool "
        "to exactly this path (nothing else, no other file):", "", f"    {ans}", "",
        f"The answer is one JSON list with exactly {n} objects, one per item below, each carrying that item's qid.", "",
        "## Instructions", "", batch.prompt, "", "## Answer format", "", answer_format, "",
        f"## Items ({n}; one JSON object per line)", "", "```json", "[",
        ",\n".join(json.dumps(it, ensure_ascii=False) for it in chunk["items"]), "]", "```", ""])


def write_batch(rel_root: str, batch, *, title: str, answer_format: str, kind_label: str, model: str,
                extra: dict | None = None) -> dict:
    """Write the chunks, prompt, manifest, key and one task file per chunk under staged/t37b_dev/<rel_root>/; returns the
    TASKS manifest (also written as TASKS.json)."""
    root = (HERE / rel_root).resolve()
    paths.check_path(root)
    files = dict(batch.files())
    rows = []
    for c in batch.chunks:
        rel = f"tasks/{c['task_id']}.md"
        files[rel] = task_text(batch, c, root, title=title, answer_format=answer_format)
        read, write = batch.allowed(str(root), c["task_id"])
        rows.append({"task_file": str(root / rel), "answer_file": str(root / batch.answer_path(c["task_id"])),
                     "kind": kind_label, "model": model, "batch_id": batch.batch_id, "task_id": c["task_id"],
                     "n_items": len(c["items"]), "prompt_sha": batch.prompt_sha,
                     "audit_allowed_read": sorted(read | {str(root / rel)}), "audit_allowed_write": sorted(write)})
    man = {"family": FAMILY, "stage": kind_label, "batch_id": batch.batch_id, "prompt_sha": batch.prompt_sha,
           "seed": batch.seed, "n_tasks": len(rows), "n_items": len(batch.key), "model": model, "tasks": rows,
           **(extra or {})}
    files["TASKS.json"] = json.dumps(man, indent=1, ensure_ascii=False) + "\n"
    paths.write_files(root, files)
    (root / "answers").mkdir(parents=True, exist_ok=True)
    return man


def load_batch_answers(rel_root: str) -> tuple:
    """(answers {internal id: answer dict}, problems) from the answer files under staged/t37b_dev/<rel_root>/answers/,
    rebuilt with the stored chunks and key (the key is read from key/, orchestrator side)."""
    root = HERE / rel_root
    man = json.loads((root / "TASKS.json").read_text())
    keyd = json.loads((root / "key" / f"{man['batch_id']}.json").read_text())["key"]
    out, probs = {}, []
    task_of = {}
    for t in man["tasks"]:
        ch = json.loads((root / "chunks" / f"{t['task_id']}.json").read_text())
        for it in ch["items"]:
            task_of[it["qid"]] = t["task_id"]
    for t in man["tasks"]:
        ap = Path(t["answer_file"])
        if not ap.exists():
            probs.append(f"{t['task_id']}: no answer file")
            continue
        try:
            ans = json.loads(ap.read_text())
        except Exception as e:      # noqa: BLE001
            probs.append(f"{t['task_id']}: unreadable answer ({type(e).__name__})")
            continue
        if not isinstance(ans, list):
            probs.append(f"{t['task_id']}: answer is not a list")
            continue
        for a in ans:
            if not isinstance(a, dict) or "qid" not in a:
                probs.append(f"{t['task_id']}: an answer without qid")
                continue
            q = a["qid"]
            if q not in keyd:
                probs.append(f"{t['task_id']}: unknown qid {q}")
            elif task_of.get(q) != t["task_id"]:
                probs.append(f"{t['task_id']}: qid {q} belongs to another task")
            elif keyd[q] in out:
                probs.append(f"{t['task_id']}: qid {q} answered twice")
            else:
                out[keyd[q]] = {k: v for k, v in a.items() if k != "qid"}
    miss = sorted(set(keyd.values()) - set(out))
    if miss:
        probs.append(f"{len(miss)} item(s) unanswered")
    return out, probs


# ------------------------------------------------------------------------------------------------ stage 1

def stage1() -> dict:
    refuse_overwrite("PLAN_FREEZE.json")
    pool, rep = build_pool()
    plan = make_plan(pool)
    rep["n_plan_groups"] = len(plan)
    rep["plan_initial"] = min(N0, len(plan))
    rep["plan_extension"] = min(N_EXT, max(0, len(plan) - N0))
    write_here("POOL.json", jdump(pool))
    write_here("POOL_REPORT.json", jdump(rep))
    plan_obj = {"key": KEY, "n0": N0, "n_ext": N_EXT, "n_keep": N_KEEP, "source_cap": SOURCE_CAP, "frame_cap": FRAME_CAP,
                "order": "sorted by sha256(key|base_id); one entry per group_id (smallest hash); no gold, frame or model read used",
                "entries": plan}
    ptxt = jdump(plan_obj)
    write_here("PLAN.json", ptxt)
    freeze = {"file": "PLAN.json", "sha256": sha(ptxt), "n_entries": len(plan), "n0": N0, "n_ext": N_EXT, "key": KEY,
              "frozen_utc": now_utc(), "pool_report_sha256": sha(jdump(rep)),
              "note": "plan order frozen before any Haiku read of a base or a frame; the frame per entry is fixed later "
                      "(frames3) as a hash of the key and the base id over the frozen frames"}
    write_here("PLAN_FREEZE.json", jdump(freeze))

    out = {"pool": rep, "plan_freeze": freeze, "tasks": []}
    # frame authoring (Haiku)
    fb = chunker.make_batch("author_lexicon", FAMILY, frame_author_items(), seed=f"{KEY}|frames-r1", prompt=FRAME_AUTHOR_PROMPT,
                            max_items=6)
    man = write_batch("frames_r1", fb, title="T37b-dev frame authoring",
                      answer_format='[{"qid": "q...", "frames": ["Does it ... that", "..."]}, ...]',
                      kind_label="author:t37bdev_frames", model="haiku")
    out["tasks"] += man["tasks"]
    # subject decomposition, two independent reads (Haiku)
    pool_by_id = {e["base_id"]: e for e in pool}
    items = [(p["base_id"], {"question": pool_by_id[p["base_id"]]["span"]}) for p in plan[:N0]]
    for tag in ("a", "b"):
        b = chunker.make_batch("t37bdev_decompose", FAMILY, items, seed=f"{KEY}|decomp-{tag}", prompt=DECOMP_PROMPT,
                               max_items=CHUNK)
        m = write_batch(f"decomp_{tag}", b, title="T37b-dev subject read", answer_format=DECOMP_FORMAT,
                        kind_label=f"decompose:t37bdev:{tag}", model="haiku")
        out["tasks"] += m["tasks"]
    write_here("STAGE1_TASKS.json", jdump(out["tasks"]))
    return out


# ------------------------------------------------------------------------------------------------ stage frames2 (round 2)

import subprocess  # noqa: E402
from negtwins import lexicon as _LX  # noqa: E402

GLEX_FORMAT = '[{"qid": "q...", "relation": "same" | "opposite" | "unclear"}, ...]'
chunker.TASK_KINDS.setdefault("polarity", ("question_a", "question_b"))
PROBES = 3


def authored_frames(rel_root: str) -> tuple:
    """([frames in answer order, deduplicated], problems) from the authoring answers under staged/t37b_dev/<rel_root>/."""
    ans, probs = load_batch_answers(rel_root)
    out = []
    for k in sorted(ans):
        fr = ans[k].get("frames")
        if not isinstance(fr, list):
            probs.append(f"{k}: frames is not a list")
            continue
        out += [f for f in fr if isinstance(f, str)]
    return list(dict.fromkeys(out)), probs


def decontam_scan(frames: list, tag: str) -> dict:
    """Occurrences of each frame (case-insensitive, whole words) in ALL text files under lean/data/ except the never-open
    paths (any path part with 'ohs', 'sealed' or 'jev'). That covers every training-side file and every existing dev or eval
    row. ripgrep -o, counts per frame. The pattern file and the raw command are logged."""
    pats = [f.lower() for f in frames]
    pf = HERE / f"decontam_{tag}.patterns.txt"
    write_here(pf.name, "\n".join(pats) + "\n")
    cmd = ["rg", "-o", "-i", "-w", "-F", "--no-ignore", "--hidden", "-I", "--no-filename", "--iglob", "!*ohs*", "--iglob",
           "!*sealed*", "--iglob", "!*jev*", "-f", str(pf), str(LEAN / "data")]
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(LEAN / "data"))
    if res.returncode not in (0, 1):
        raise RuntimeError(f"rg failed: {res.stderr[:300]}")
    cnt = Counter(" ".join(ln.lower().split()) for ln in res.stdout.split("\n") if ln.strip())
    return {"command": " ".join(cmd[:-1]) + " <lean/data>", "n_frames": len(frames), "counts": {f: cnt.get(" ".join(f.lower().split()), 0)
                                                                                                       for f in frames}}


def _frame_not_probe_items(frames: list) -> list:
    items = []
    for f in frames:
        cores = _LX._pick(_LX.PB.DO + _LX.PB.COP, f + "|frame_not", PROBES * 3)
        got = 0
        for c in cores:
            q = C.parse(c)
            if q is None or got >= PROBES:
                continue
            p = C.make_pattern("FRAME_NOT", q.cls, frame=f, contr="not", source="lex")
            t, _ = C.apply(c, p)
            if t:
                items.append((f"glex|frame_not|{C.sha(f)[:10]}|p{got}", {"question_a": c, "question_b": t}))
                got += 1
    return items


def glex_items(frames: list) -> list:
    """3 frame-over-core probes (expected 'same') and 3 FRAME_NOT probes (expected 'opposite') per frame."""
    return _LX.frame_probe_items(frames, "pos_frame") + _frame_not_probe_items(frames)


def glex_expected(internal_id: str) -> str:
    return "same" if internal_id.split("|")[1] == "pos_frame" else "opposite"


def write_glex(frames: list, tag: str, rounds=("A", "B")) -> dict:
    out = {}
    items = glex_items(frames)
    for r in rounds:
        b = chunker.make_batch("polarity", FAMILY, items, seed=f"{KEY}|glex-{tag}-{r}", prompt=_TP.POLARITY_PROMPT, max_items=CHUNK)
        m = write_batch(f"glex_{tag}_{r.lower()}", b, title="T37b-dev G-LEX read", answer_format=GLEX_FORMAT,
                        kind_label=f"polarity:t37bdev_glex:{r}", model="haiku")
        out[r] = m
    return out


from t37b import builder as _TP  # noqa: E402  (POLARITY_PROMPT, BLIND_PROMPT)


def decomp_tasks(entries: list, pool_by_id: dict, tag: str) -> list:
    items = [(p["base_id"], {"question": pool_by_id[p["base_id"]]["span"]}) for p in entries]
    tasks = []
    for t in ("a", "b"):
        b = chunker.make_batch("t37bdev_decompose", FAMILY, items, seed=f"{KEY}|decomp-{tag}-{t}", prompt=DECOMP_PROMPT,
                               max_items=CHUNK)
        m = write_batch(f"decomp_{tag}_{t}", b, title="T37b-dev subject read", answer_format=DECOMP_FORMAT,
                        kind_label=f"decompose:t37bdev:{tag}:{t}", model="haiku")
        tasks += m["tasks"]
    return tasks


def frames2() -> dict:
    refuse_overwrite("FRAMES_R1.json")
    cands, probs = authored_frames("frames_r1")
    taken = known_surfaces()
    lint = {c: a70_frame_problems(c, "A", taken) for c in cands}
    passed = [c for c, p in lint.items() if not p]
    dec = decontam_scan(passed, "r1")
    clean = [c for c in passed if dec["counts"][c] == 0]
    rep = {"n_authored_unique": len(cands), "load_problems": probs, "n_lint_pass": len(passed),
           "lint_fail": {c: p for c, p in lint.items() if p}, "decontam": dec,
           "n_decontam_dropped": len(passed) - len(clean), "decontam_dropped": [c for c in passed if dec["counts"][c]],
           "candidates_to_glex": clean, "n_known_surfaces": len(taken)}
    write_here("FRAMES_R1.json", jdump(rep))
    glex = write_glex(clean, "r1")
    out = {"report": {k: v for k, v in rep.items() if k not in ("lint_fail", "decontam")}, "glex": {r: m["n_tasks"] for r, m in glex.items()},
           "tasks": [t for m in glex.values() for t in m["tasks"]]}
    return out


def ext_decomp() -> dict:
    refuse_overwrite("EXT_DECOMP_WRITTEN.json")
    pool_by_id = {e["base_id"]: e for e in read_here("POOL.json")}
    plan = read_here("PLAN.json")["entries"]
    tasks = decomp_tasks(plan[N0:N0 + N_EXT], pool_by_id, "ext")
    write_here("EXT_DECOMP_WRITTEN.json", jdump({"n_entries": len(plan[N0:N0 + N_EXT]), "n_tasks": len(tasks), "utc": now_utc()}))
    return {"tasks": tasks}


# ------------------------------------------------------------------------------------------------ stage round3
# frames3 (admit 2/2, freeze) + pair candidates for ALL plan entries (the extension is a read-only precomputation: which
# entries count is decided in `finish`, in plan order) + the Haiku reads that need only the candidates.

SOLVER_PROMPT = (
    "Each item is a text, a yes/no question and, when given, the definitions for that question. Read the text and answer "
    "the question by the definitions. Reply 'yes' or 'no'; reply 'unsure' only if the text and definitions do not settle "
    "the answer or the question is not clear or not grammatical. Reply with JSON: a list of objects {\"qid\": <qid>, "
    "\"answer\": \"yes\" | \"no\" | \"unsure\"}.")
SOLVER_FORMAT = '[{"qid": "q...", "answer": "yes" | "no" | "unsure"}, ...]'
REVIEW_PROMPT = (
    "Each item has a text, optional definitions, and two yes/no questions about that text: question_a and question_b. "
    "question_b is meant to be the exact logical complement of question_a for any text: a correct yes to one must always "
    "be a correct no to the other, and a correct no to one a correct yes to the other. Judge only the wording of the two "
    "questions (do not answer them and do not use any answer key). Reply 'exact' if question_b is certainly the exact "
    "complement of question_a with no change of meaning other than the negation; reply 'not exact' if a text could make "
    "both answers yes or both no, or if question_b changes anything else; reply 'unsure' if you cannot tell for certain. "
    "Reply with JSON: a list of objects {\"qid\": <qid>, \"verdict\": \"exact\" | \"not exact\" | \"unsure\", "
    "\"reason\": \"<one short sentence>\"}.")
REVIEW_FORMAT = '[{"qid": "q...", "verdict": "exact" | "not exact" | "unsure", "reason": "..."}, ...]'
chunker.TASK_KINDS.setdefault("t37bdev_review", ("text", "definitions", "question_a", "question_b", "solver_a", "solver_b"))
SOLVER_CHUNK = 20
SHA_CAND_NOTE = "candidates are pure functions of the frozen plan, frozen frames, subject reads and the base rows"


def norm_rel(a):
    if isinstance(a, dict):
        a = a.get("relation")
    a = str(a or "").strip().lower()
    return a if a in ("same", "opposite", "unclear") else None


def glex_decide(frames: list, reads_a: dict, reads_b: dict) -> dict:
    """{frame: (admitted, detail)}: all 6 probes read in both rounds, every read the expected relation."""
    out = {}
    for f in frames:
        pre = [f"glex|pos_frame|{C.sha(f)[:10]}|", f"glex|frame_not|{C.sha(f)[:10]}|"]
        ids = sorted(i for i in reads_a if any(i.startswith(p) for p in pre))
        ra = {i: norm_rel(reads_a.get(i)) for i in ids}
        rb = {i: norm_rel(reads_b.get(i)) for i in ids}
        n_pos = sum(1 for i in ids if "|pos_frame|" in i)
        n_not = sum(1 for i in ids if "|frame_not|" in i)
        ok = n_pos == PROBES and n_not == PROBES and all(ra[i] == rb[i] == glex_expected(i) for i in ids)
        out[f] = (ok, {"n_pos": n_pos, "n_not": n_not, "reads_a": ra, "reads_b": rb})
    return out


def order_frames(frames: list) -> list:
    return sorted(frames, key=lambda f: sha(f"{KEY}|frame|{f}"))


def trained_and_heldout_patterns():
    """(patterns, pair dict) = the 379 trained patterns (sha checked) and the 33 realised held-out patterns."""
    if file_sha(C2_BUILD / "negtwins/TRAINED_CATALOGUE.json") != SHA_TRAINED:
        raise RuntimeError("TRAINED_CATALOGUE.json sha changed")
    if file_sha(H.REALISED_FILE) != SHA_HELDOUT:
        raise RuntimeError("HELDOUT_REALISED.json sha changed")
    tp, pairs = FZ.load_trained()
    adm = json.loads(H.REALISED_FILE.read_text(encoding="utf-8"))
    hp, _missing = H.realise(adm)
    pm = dict(pairs)
    for v in adm.values():
        if isinstance(v, dict):
            pm[v["pair_id"]] = v
    C.register_verbs(pm.values())
    if len(tp) != PREREG_N_TRAINED or len(hp) != 33:
        raise RuntimeError(f"pattern counts {len(tp)}/{len(hp)}")
    return list(tp) + list(hp), pm


def _tok(s: str) -> Counter:
    return Counter(w.strip(",?").lower() for w in s.split() if w.strip(",?"))


def construction_check(span: str, partner: str, frame: str) -> list:
    """A70 (e): the partner span = frame + the base span with exactly one added 'not' (token multiset), and negcount finds
    no cue in the base span and exactly one in the body after the frame."""
    probs = []
    if not partner.startswith(frame + " ") and not partner.startswith(frame + ","):
        return ["partner does not start with the frame"]
    body = partner[len(frame):].lstrip(" ,")
    if _tok(body) - Counter({"not": 1}) != _tok(span) or _tok(span) - _tok(body):
        probs.append("token multiset: the body is not the base span plus exactly one 'not'")
    if body.count("?") != 1 or not partner.endswith("?") or "\n" in partner:
        probs.append("not one question on one line")
    if negcount.count(span).k_all != 0:
        probs.append("negcount of the base span is not 0")
    nb = negcount.count(body)
    if nb.k_all != 1 or nb.k_syn != 1 or [m.surface.lower() for m in nb.matches] != ["not"]:
        probs.append(f"negcount of the body: k_all {nb.k_all}, k_syn {nb.k_syn}, cues {[m.surface for m in nb.matches]}")
    return probs


def pattern_yields_partner(span: str, partner: str, pats: list, pm: dict) -> list:
    """The pids of trained / held-out patterns that, applied to the base span, give the partner span (must be none)."""
    hit = []
    target = " ".join(C.tokens(partner))
    for p in pats:
        try:
            t, _ = C.apply(span, p, pm)
        except Exception:       # noqa: BLE001
            t = None
        if t and " ".join(C.tokens(t)) == target:
            hit.append(p.pid)
    return hit


def partner_row(base_row: dict, partner_instr: str, frame: str, subject: str, pos: int, readings: dict) -> dict:
    """The partner: the base row with only id, role, gold, instructions and meta changed (A70 e)."""
    r = dict(base_row)
    r["id"] = "r_t37bdev_" + sha(f"{KEY}|{base_row['id']}")[:12]
    r["role"] = "complement"
    r["gold"] = 1 - base_row["gold"]
    r["instructions"] = partner_instr
    r["meta"] = {"twin_of": base_row["id"], "twin_kind": "complement", "dev_only": True, "qform": "FRAME_NOT",
                 "text_source": base_row.get("source"),
                 "t37bdev": {"key": KEY, "frame": frame, "subject": subject, "plan_pos": pos, "base_id": base_row["id"],
                             "base_gold": base_row["gold"], "polarity_programs": readings}}
    return r


def make_candidates(frames_ordered: list) -> list:
    """One candidate per plan entry (all 497), program-only: subject consensus, partner span, both polarity programs,
    construction, trained / held-out pattern check. status 'ok' or the first failing reason."""
    pool = {e["base_id"]: e for e in read_here("POOL.json")}
    plan = read_here("PLAN.json")["entries"]
    reads = {}
    for tag in ("", "_ext"):
        for t in ("a", "b"):
            ans, probs = load_batch_answers(f"decomp{tag}_{t}")
            reads[(tag, t)] = (ans, probs)
    rows = {}
    for sp in {e["split"] for e in pool.values()}:
        for r, raw in load_split(sp):
            rows[r["id"]] = (r, raw)
    pats, pm = trained_and_heldout_patterns()
    cands = []
    n = len(frames_ordered)
    for p in plan:
        i, pos = p["base_id"], p["pos"]
        e = pool[i]
        tag = "" if pos < N0 else "_ext"
        a, b = reads[(tag, "a")][0].get(i), reads[(tag, "b")][0].get(i)
        frame = frames_ordered[pos % n]
        c = {"pos": pos, "base_id": i, "source": e["source"], "split": e["split"], "frame": frame, "status": "ok",
             "span": e["span"], "cls": e["cls"]}
        cands.append(c)
        if not a or not b:
            c["status"] = "no subject read"
            continue
        if (a.get("subject"), a.get("next_word")) != (b.get("subject"), b.get("next_word")):
            c["status"] = "subject reads disagree"
            continue
        pr, parts = subject_check(e["span"], a["subject"], a["next_word"])
        if pr:
            c["status"] = "subject_check: " + pr[0]
            continue
        c["subject"] = a["subject"]
        part = partner_span(frame, parts)
        c["partner_span"] = part
        ra, rb, probs = program_readings(e["span"], a["subject"], frame, part)
        c["prog"] = [ra, rb]
        if (ra, rb) != ("opposite", "opposite"):
            c["status"] = "polarity programs: " + str(probs[:2])
            continue
        cp = construction_check(e["span"], part, frame)
        if cp:
            c["status"] = "construction: " + cp[0]
            continue
        hit = pattern_yields_partner(e["span"], part, pats, pm)
        if hit:
            c["status"] = f"a trained / held-out pattern yields the partner ({len(hit)})"
            continue
        c["partner_instr"] = e["pre"] + part + e["post"]
        if c["partner_instr"].count("?") != 1:
            c["status"] = "partner instructions: not exactly one '?'"
    return cands, rows


def solver_item(row: dict) -> dict:
    it = {"kind": "yes/no", "text": row["state"], "question": row["instructions"]}
    if row.get("card"):
        it["definitions"] = row["card"]
    return it


def round3_tasks(cands: list, rows: dict, tag: str = "r3") -> dict:
    ok = [c for c in cands if c["status"] == "ok"]
    out = {}
    pol_items = [(c["base_id"], {"question_a": c["span"], "question_b": c["partner_span"]}) for c in ok]
    for t in ("a", "b"):
        b = chunker.make_batch("polarity", FAMILY, pol_items, seed=f"{KEY}|pol-{tag}-{t}", prompt=_TP.POLARITY_PROMPT, max_items=CHUNK)
        out[f"pol_{tag}_{t}"] = write_batch(f"pol_{tag}_{t}", b, title="T37b-dev polarity read", answer_format=GLEX_FORMAT,
                                            kind_label=f"polarity:t37bdev:{t}", model="haiku")
    base_items = [(c["base_id"], solver_item(rows[c["base_id"]][0])) for c in ok]
    part_items = [(c["base_id"], solver_item({**rows[c["base_id"]][0], "instructions": c["partner_instr"]})) for c in ok]
    for nm, items in (("base", base_items), ("partner", part_items)):
        b = chunker.make_batch("blind_read", FAMILY, items, seed=f"{KEY}|solve-{tag}-{nm}", prompt=SOLVER_PROMPT, max_items=SOLVER_CHUNK)
        out[f"solve_{tag}_{nm}"] = write_batch(f"solve_{tag}_{nm}", b, title="T37b-dev blind solve", answer_format=SOLVER_FORMAT,
                                               kind_label=f"blind:t37bdev:{nm}", model="haiku")
    return out


def round3() -> dict:
    refuse_overwrite("FRAMES_FREEZE.json")
    fr = read_here("FRAMES_R1.json")
    cands_f = fr["candidates_to_glex"]
    ra, pa = load_batch_answers("glex_r1_a")
    rb, pb = load_batch_answers("glex_r1_b")
    if pa or pb:
        raise RuntimeError(f"G-LEX answers incomplete: {pa[:3]} {pb[:3]}")
    dec = glex_decide(cands_f, ra, rb)
    admitted = [f for f in cands_f if dec[f][0]]
    res = {"n_candidates": len(cands_f), "n_admitted": len(admitted), "admitted": admitted,
           "rejected": [f for f in cands_f if not dec[f][0]], "detail": {f: dec[f][1] for f in cands_f}}
    write_here("GLEX_R1_RESULT.json", jdump(res))
    if len(admitted) < MIN_FRAMES:
        return {"stopped": "fewer than 3 tier-A frames admitted; a second authoring round is needed", "result": res}
    ordered = order_frames(admitted)
    ftext = jdump({"key": KEY, "tier": "A", "frames": ordered, "n": len(ordered), "assignment": "frame of plan entry pos = frames[pos % n]",
                   "glex": "2/2: 3 frame-over-core probes (same) + 3 FRAME_NOT probes (opposite), two independent rounds"})
    write_here("FRAMES_FROZEN.json", ftext)
    write_here("FRAMES_FREEZE.json", jdump({"file": "FRAMES_FROZEN.json", "sha256": sha(ftext), "n_frames": len(ordered),
                                             "frozen_utc": now_utc(), "note": "frozen before any base is paired with a frame"}))
    cands, rows = make_candidates(ordered)
    write_here("CANDIDATES.json", jdump(cands))
    st = Counter(c["status"].split(":")[0] for c in cands)
    tasks = round3_tasks(cands, rows)
    allt = [t for m in tasks.values() for t in m["tasks"]]
    write_here("ROUND3_TASKS.json", jdump(allt))
    return {"result": {k: v for k, v in res.items() if k != "detail"}, "frames_sha": sha(ftext), "n_cand_ok": sum(1 for c in cands if c["status"] == "ok"),
            "status_counts": dict(st), "n_tasks": len(allt), "by_batch": {k: m["n_tasks"] for k, m in tasks.items()}}


# ------------------------------------------------------------------------------------------------ stage round4 (review queue)

def norm_yn(a):
    if isinstance(a, dict):
        a = a.get("answer")
    a = str(a or "").strip().lower().rstrip(".")
    return a if a in ("yes", "no", "unsure") else None


def norm_verdict(a):
    if isinstance(a, dict):
        a = a.get("verdict")
    a = str(a or "").strip().lower()
    return a if a in ("exact", "not exact", "unsure") else None


def read_round3():
    """(candidates, per-base reads {base_id: {...}}, problems) from CANDIDATES.json and the four round-3 batches."""
    cands = read_here("CANDIDATES.json")
    pa, e1 = load_batch_answers("pol_r3_a")
    pb, e2 = load_batch_answers("pol_r3_b")
    sb, e3 = load_batch_answers("solve_r3_base")
    sp, e4 = load_batch_answers("solve_r3_partner")
    reads = {}
    for c in cands:
        i = c["base_id"]
        if c["status"] != "ok":
            continue
        reads[i] = {"pol_a": norm_rel(pa.get(i)), "pol_b": norm_rel(pb.get(i)), "solve_base": norm_yn(sb.get(i)),
                    "solve_partner": norm_yn(sp.get(i))}
    return cands, reads, e1 + e2 + e3 + e4


def first_decision(r: dict) -> tuple:
    """(verdict, reason) before any review: drop | keep | review."""
    if r["pol_a"] != "opposite" or r["pol_b"] != "opposite":
        return "drop", f"polarity reads {r['pol_a']!r} / {r['pol_b']!r}"
    yb, yp = r["solve_base"], r["solve_partner"]
    if yb in ("yes", "no") and yp in ("yes", "no") and yb != yp:
        return "keep", "polarity reads and blind solver agree"
    return "review", "blind solver inconsistent or unsure"


def round4() -> dict:
    refuse_overwrite("REVIEW_QUEUE.json")
    cands, reads, probs = read_round3()
    if probs:
        raise RuntimeError(f"round-3 answers incomplete: {probs[:4]}")
    pool = {e["base_id"]: e for e in read_here("POOL.json")}
    rows = {}
    for sp in {e["split"] for e in pool.values()}:
        for r, raw in load_split(sp):
            rows[r["id"]] = r
    dec = {c["base_id"]: first_decision(reads[c["base_id"]]) for c in cands if c["status"] == "ok"}
    queue = [c for c in cands if c["status"] == "ok" and dec[c["base_id"]][0] == "review"]
    items = []
    for c in queue:
        b = rows[c["base_id"]]
        it = {"text": b["state"], "question_a": b["instructions"], "question_b": c["partner_instr"]}
        if b.get("card"):
            it["definitions"] = b["card"]
        items.append((c["base_id"], it))
    summ = {"n_ok_candidates": len(dec), "first_decision": dict(Counter(v[0] for v in dec.values())),
            "drop_reasons": dict(Counter(v[1].split(" '")[0] for v in dec.values() if v[0] == "drop")), "n_review": len(items),
            "blind_vs_gold_report_only": {
                "base_agrees_with_gold": sum(1 for c in cands if c["status"] == "ok" and reads[c["base_id"]]["solve_base"] ==
                                              ("yes" if rows[c["base_id"]]["gold"] == 1 else "no")),
                "base_unsure_or_missing": sum(1 for c in cands if c["status"] == "ok" and reads[c["base_id"]]["solve_base"] in (None, "unsure"))}}
    write_here("REVIEW_QUEUE.json", jdump({"queue": [c["base_id"] for c in queue], "summary": summ}))
    out = {"summary": summ, "tasks": []}
    if items:
        b = chunker.make_batch("t37bdev_review", FAMILY, items, seed=f"{KEY}|review", prompt=REVIEW_PROMPT, max_items=10)
        m = write_batch("review_r4", b, title="T37b-dev gold-free pair review", answer_format=REVIEW_FORMAT,
                        kind_label="review:t37bdev", model="sonnet")
        out["tasks"] = m["tasks"]
    write_here("ROUND4_TASKS.json", jdump(out["tasks"]))
    return out


# ------------------------------------------------------------------------------------------------ finish

def select_survivors(cands: list, final: dict, n0: int = N0) -> dict:
    """First 300 survivors in plan order under the caps (45 per source, 120 per frame). The extension (plan entries n0 ..
    n0 + N_EXT) is used only when the first n0 entries give fewer than 300."""
    def run(limit):
        kept, src, frm, capped = [], Counter(), Counter(), Counter()
        for c in cands:
            if c["pos"] >= limit or len(kept) >= N_KEEP or final.get(c["base_id"], ("drop",))[0] != "keep":
                continue
            if src[c["source"]] >= SOURCE_CAP:
                capped["source"] += 1
                continue
            if frm[c["frame"]] >= FRAME_CAP:
                capped["frame"] += 1
                continue
            kept.append(c)
            src[c["source"]] += 1
            frm[c["frame"]] += 1
        return kept, dict(capped)
    kept0, cap0 = run(n0)
    if len(kept0) >= N_KEEP:
        return {"kept": kept0, "extension_used": False, "n_survivors_first_n0": len(kept0), "capped": cap0}
    kept1, cap1 = run(n0 + N_EXT)
    return {"kept": kept1, "extension_used": True, "n_survivors_first_n0": len(kept0), "capped": cap1,
            "n_survivors_with_extension": len(kept1)}


def finish() -> dict:
    refuse_overwrite("T37BDEV_FREEZE.json")
    cands, reads, probs = read_round3()
    if probs:
        raise RuntimeError(f"round-3 answers incomplete: {probs[:4]}")
    q = read_here("REVIEW_QUEUE.json")["queue"]
    rev, rprobs = ({}, [])
    if q:
        rev, rprobs = load_batch_answers("review_r4")
        if rprobs:
            raise RuntimeError(f"review answers incomplete: {rprobs[:4]}")
    final, reasons = {}, Counter()
    for c in cands:
        if c["status"] != "ok":
            reasons[c["status"].split(":")[0]] += 1
            continue
        i = c["base_id"]
        d, why = first_decision(reads[i])
        if d == "review":
            v = norm_verdict(rev.get(i))
            d, why = ("keep", "gold-free Sonnet review: exact") if v == "exact" else ("drop", f"review {v!r}")
        final[i] = (d, why)
        reasons[("kept: " if d == "keep" else "dropped: ") + why.split(" '")[0]] += 1
    sel = select_survivors(cands, final)
    report = {"key": KEY, "extension_used": sel["extension_used"], "n_survivors_first_n0": sel["n_survivors_first_n0"],
              "n_kept": len(sel["kept"]), "capped": sel["capped"], "reasons": dict(reasons)}
    if len(sel["kept"]) < N_KEEP:
        report["verdict"] = "STOP: fewer than 300 survivors after the one allowed extension; nothing frozen (A70 e)"
        write_here("FINISH_FAILED.json", jdump(report))
        return report
    pool = {e["base_id"]: e for e in read_here("POOL.json")}
    rows = {}
    for sp in {e["split"] for e in pool.values()}:
        for r, raw in load_split(sp):
            rows[r["id"]] = (r, raw)
    lines, rels, pids = [], [], []
    for c in sel["kept"]:
        b, raw = rows[c["base_id"]]
        pr = partner_row(b, c["partner_instr"], c["frame"], c["subject"], c["pos"], {"a": c["prog"][0], "b": c["prog"][1]})
        lines += [raw, json.dumps(pr, ensure_ascii=False)]
        rels.append(json.dumps({"a": b["id"], "b": pr["id"], "type": "complement"}, ensure_ascii=False))
        pids.append(pr["id"])
    if len(set(pids)) != len(pids):
        raise RuntimeError("duplicate partner ids")
    t_dev = "\n".join(lines) + "\n"
    t_rel = "\n".join(rels) + "\n"
    write_here("c2_t37b_dev.jsonl", t_dev)
    write_here("c2_t37b_dev_relations.jsonl", t_rel)
    report["files"] = {"c2_t37b_dev.jsonl": {"sha256": sha(t_dev), "n_rows": len(lines)},
                       "c2_t37b_dev_relations.jsonl": {"sha256": sha(t_rel), "n_rel": len(rels)}}
    report["by_source"] = dict(Counter(c["source"] for c in sel["kept"]))
    report["by_frame"] = dict(Counter(c["frame"] for c in sel["kept"]))
    report["by_split"] = dict(Counter(c["split"] for c in sel["kept"]))
    report["by_class"] = dict(Counter(c["cls"] for c in sel["kept"]))
    report["base_gold_1"] = sum(1 for c in sel["kept"] if rows[c["base_id"]][0]["gold"] == 1)
    report["frozen_utc"] = now_utc()
    write_here("T37BDEV_FREEZE.json", jdump(report))
    return report


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "stage1":
        res = stage1()
        print(json.dumps({"pool": res["pool"], "plan_freeze": res["plan_freeze"], "n_tasks": len(res["tasks"])}, indent=1))
    elif cmd == "frames2":
        res = frames2()
        print(json.dumps({"report": res["report"], "glex": res["glex"], "n_tasks": len(res["tasks"])}, indent=1))
        write_here("FRAMES2_TASKS.json", jdump(res["tasks"]))
    elif cmd == "round3":
        print(json.dumps(round3(), indent=1)[:6000])
    elif cmd == "round4":
        r = round4()
        print(json.dumps({"summary": r["summary"], "n_tasks": len(r["tasks"])}, indent=1))
    elif cmd == "finish":
        print(json.dumps(finish(), indent=1)[:6000])
    elif cmd == "ext_decomp":
        res = ext_decomp()
        write_here("EXT_DECOMP_TASKS.json", jdump(res["tasks"]))
        print(len(res["tasks"]))
    else:
        print(__doc__)
