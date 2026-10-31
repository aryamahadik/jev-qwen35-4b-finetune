"""Shared helpers for the G-block wave-2 builders (PREREG_FINAL Ruling A40 b; A37 b-c, A39 b-e apply).

Row (decoder_io raw row, cygnet layout):
  {id, group_id, task, state, instructions, qtype ("noul" | "choice"), options (choice: 2-8 one-line texts; noul: None),
   card ("- label: definition" lines; noul: "- yes: ..." and "- no: ..."), gold (noul 1/0; choice: the gold option text),
   meta {gold_method ("program" | "construction"), construction {...}, type, wave, gen_version, licence, source, ...}}
Render check: decoder_io (sha-pinned A16 readout, imported read-only) in style cygnet + layout schema_branch_mark,
formats-1 loader_check with the row's own gold (option block, card lines, train_decoder.check_rows), the untrusted-text
markers, and the pinned Qwen3.5-4B token count (CYGNET_SYSTEM + "\\n" + user_msg) <= 2,000.
Writes go through c2_kit.paths (A38 guard, never-open guard, lean/ only). Nothing here opens a never-open path.
"""
from __future__ import annotations

import hashlib
import json
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

WAVE2 = Path(__file__).resolve().parents[1]                  # .../c2_build/gblock/wave2
GB = WAVE2.parent                                             # .../c2_build/gblock
C2 = GB.parent                                                # .../c2_build
LEAN = C2.parent                                              # .../lean
TEXTS = GB / "texts"
AUTHOR = WAVE2 / "author"
TASKS_DIR = AUTHOR / "tasks"
ANSWERS_DIR = AUTHOR / "answers"
TASKS_KEY = AUTHOR / "tasks_key.json"
CAND_DIR = WAVE2 / "candidates"
RAW = WAVE2 / "raw"

for _p in (str(GB / "tools"), str(C2), str(LEAN), str(LEAN / "c_src" / "formats" / "formats-1")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import build_candidates as B  # noqa: E402  (pinned Renderer: decoder_io sha, tokenizer sha, formats-1 card)
from c2_kit import paths as kp  # noqa: E402  (never-open guard + A38 write guard)

SEED = 20261013
TOK_MAX = 2000
MAX_OPTIONS = 8                      # A39 c: choice label sets of 2-8 options
GEN_VERSION = "gblock-wave2 1.0 (13 Oct 2026)"
WAVE = "C2 G-block wave 2 (PREREG_FINAL A40)"
LICENCE_AUTHORED = "CC0 1.0 (program-generated; Claude/Haiku-authored wording)"
TYPES = {
    "W1": "injection", "W2": "pii", "W3": "rag_faithfulness", "W4": "off_topic", "W5": "search_relevance",
    "W6": "commit_type", "W7": "tool_routing",
}
OPTION_BAD = re.compile(r"(: |\n|\r)")


# ------------------------------------------------------------------------------------------------------ small io

def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sha256_file(p) -> str:
    return hashlib.sha256(kp.check_path(p).read_bytes()).hexdigest()


def read_jsonl(p) -> list:
    with open(kp.check_path(p), encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def read_json(p):
    return json.loads(kp.check_path(p).read_text(encoding="utf-8"))


def _gb_tools_common():
    """gblock/tools/common.py (the G-block text helpers: PII screen, English check), loaded under its own name."""
    import importlib.util
    name = "gblock_tools_common"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, kp.check_path(GB / "tools" / "common.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def pii_reason(s: str):
    """The G-block PII screen: 'email' / 'phone' / 'user_path' / 'ip' or None."""
    return _gb_tools_common().pii_reason(s)


def norm_ws(s: str) -> str:
    """Collapse runs of spaces and tabs, trim lines, and at most one blank line (formatting only, never meaning)."""
    s = (s or "").replace("\r\n", "\n").replace("\r", "\n").replace(" ", " ").replace("​", "")
    s = re.sub(r"[ \t\f\v]+", " ", s)
    s = re.sub(r" *\n *", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def one_line(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def nwords(s: str) -> int:
    return len((s or "").split())


def key_hash(*parts) -> int:
    return int.from_bytes(hashlib.sha256("|".join(str(p) for p in parts).encode()).digest()[:8], "big")


def rng_for(*parts) -> random.Random:
    return random.Random(key_hash(SEED, *parts))


def pick_wording(options: list, *parts) -> int:
    """Seeded choice of a wording index (so a row's question wording is fixed by its id, not by build order)."""
    return key_hash(SEED, "wording", *parts) % len(options)


def load_answer(path) -> tuple:
    """(object or None, problems) for a Haiku answer file: plain JSON, tolerating a ```json fence around it."""
    p = kp.check_path(path)
    if not p.exists():
        return None, ["missing"]
    raw = p.read_text(encoding="utf-8").strip()
    m = re.match(r"^```(?:json)?\s*\n(.*)\n```\s*$", raw, re.S)
    if m:
        raw = m.group(1)
    try:
        return json.loads(raw), []
    except json.JSONDecodeError as e:
        return None, [f"json: {e}"]


# ------------------------------------------------------------------------------------------------------- rows

def card_lines(pairs) -> str:
    """'- label: definition' lines; labels and definitions are one line, labels hold no ': '."""
    out = []
    for lab, d in pairs:
        assert lab and not OPTION_BAD.search(lab) and not lab.startswith("- "), lab
        d = one_line(d)
        assert d, lab
        out.append(f"- {lab}: {d}")
    return "\n".join(out)


def yesno_card(yes_def: str, no_def: str) -> str:
    return card_lines([("yes", yes_def), ("no", no_def)])


def make_row(T: str, key: str, group_id: str, state: str, instructions: str, *, qtype: str, gold, card: str,
             options=None, gold_method: str, construction: dict, extra_meta: dict | None = None) -> dict:
    assert T in TYPES and gold_method in ("program", "construction")
    meta = {"gold_method": gold_method, "construction": dict(construction), "type": T, "task_name": TYPES[T],
            "wave": WAVE, "gen_version": GEN_VERSION, "seed": SEED}
    meta.update(extra_meta or {})
    return {"id": f"c2_wave2:{T}:{key}", "group_id": group_id, "task": f"{T}_{TYPES[T]}", "state": state,
            "instructions": instructions, "qtype": qtype, "options": None if qtype == "noul" else list(options),
            "card": card, "gold": gold, "meta": meta}


def schema_problems(row: dict) -> list:
    p = []
    for k in ("id", "group_id", "task", "state", "instructions", "qtype", "options", "card", "gold", "meta"):
        if k not in row:
            p.append(f"missing {k}")
    if p:
        return p
    if not row["state"].strip() or not row["instructions"].strip():
        p.append("empty state or instructions")
    if "\n" in row["instructions"]:
        p.append("instructions hold a line break")
    m = row["meta"]
    if m.get("gold_method") not in ("program", "construction") or not isinstance(m.get("construction"), dict):
        p.append("meta.gold_method / meta.construction")
    defs = {}
    for line in (row["card"] or "").split("\n"):
        if not line.startswith("- ") or ": " not in line:
            p.append(f"card line {line[:40]!r} is not '- label: definition'")
            continue
        k, v = line[2:].split(": ", 1)
        if k in defs:
            p.append(f"card label {k!r} twice")
        defs[k] = v
    if row["qtype"] == "noul":
        if row["options"] is not None or row["gold"] not in (0, 1) or isinstance(row["gold"], bool):
            p.append("yes/no row: options None and gold 1 / 0")
        if sorted(defs) != ["no", "yes"]:
            p.append("yes/no card must define exactly yes and no (lower case)")
    elif row["qtype"] == "choice":
        o = row["options"]
        if not isinstance(o, list) or not 2 <= len(o) <= MAX_OPTIONS:
            p.append(f"choice row: 2-{MAX_OPTIONS} options")
        elif len(set(o)) != len(o) or any(not isinstance(x, str) or not x or OPTION_BAD.search(x)
                                           or x.startswith("- ") or x.strip() != x for x in o):
            p.append("options: distinct one-line texts without ': '")
        elif row["gold"] not in o:
            p.append("gold is not an option")
        elif sorted(defs) != sorted(o):
            p.append("card labels != options")
    else:
        p.append(f"qtype {row['qtype']!r}")
    return p


class Checker:
    """decoder_io cygnet + schema_branch_mark render, formats-1 loader_check (real gold), markers, token cap."""

    def __init__(self):
        self.R = B.Renderer()
        self.dio = self.R.dio

    def tokens_and_msg(self, row: dict) -> tuple:
        dio = self.dio
        saved = (dio.STYLE, dio.LAYOUT, dio.WIDE)
        dio.STYLE, dio.LAYOUT = B.STYLE, B.LAYOUT
        dio.WIDE = list(dio.LETTERS) + self.R.wide[: dio.MAX_OPTIONS - 26]
        try:
            msg = dio.user_msg(row)
            ntok = len(self.R.tok.encode(dio.CYGNET_SYSTEM + "\n" + msg).ids)
        finally:
            dio.STYLE, dio.LAYOUT, dio.WIDE = saved
        return ntok, msg

    def check(self, row: dict) -> tuple:
        """(problems, tokens, prompt_sha256)."""
        probs = schema_problems(row)
        if probs:
            return probs, None, None
        dio = self.dio
        ntok, msg = self.tokens_and_msg(row)
        st = row["state"].rstrip()
        if any(m in row["state"] or m in row["instructions"] or m in (row["card"] or "") for m in dio.UNTRUSTED):
            probs.append("a field holds a marker string")
        elif f"{dio.UNTRUSTED[0]}\n{st}\n{dio.UNTRUSTED[1]}" not in msg:
            probs.append("text not shown whole between the markers")
        if msg.count(row["instructions"].rstrip()) < 2:
            probs.append("question not shown in schema and branch")
        res = self.R.fcard.loader_check(row, check_rows=True)
        probs += res["problems"]
        if row["qtype"] == "choice":
            defs = dio.card_defs(row["card"])
            for o in row["options"]:
                if f"{o}: {defs[o]}" not in msg:
                    probs.append(f"option {o!r} shown without its definition")
        if ntok > TOK_MAX:
            probs.append(f"{ntok} tokens > {TOK_MAX}")
        return probs, ntok, hashlib.sha256(msg.encode()).hexdigest()


def check_all(rows: list, checker: Checker | None = None) -> tuple:
    """(kept rows, dropped [{id, problems}], token list). Ids must be unique."""
    checker = checker or Checker()
    ids = Counter(r["id"] for r in rows)
    dup = [i for i, c in ids.items() if c > 1]
    if dup:
        raise ValueError(f"duplicate row ids, e.g. {dup[:3]}")
    kept, drops, toks = [], [], []
    for r in rows:
        probs, ntok, _ = checker.check(r)
        if probs:
            drops.append({"id": r["id"], "problems": probs[:4], "tokens": ntok})
        else:
            kept.append(r)
            toks.append(ntok)
    return kept, drops, toks


# ------------------------------------------------------------------------------------------------------ balance

def gold_key(r: dict):
    return r["gold"]


def balance(rows: list, keyfn=gold_key, *, seed_tag: str, cap_ratio: float = 1.0, max_total: int | None = None,
            group_hint=None) -> list:
    """Seeded down-sampling so no label exceeds cap_ratio x the smallest label count (1.0 = equal counts), then
    (optionally) an even cut to max_total keeping the label shares. Rows are never edited."""
    by = defaultdict(list)
    for r in rows:
        by[keyfn(r)].append(r)
    if not by:
        return []
    for k in by:
        by[k].sort(key=lambda r: key_hash(SEED, seed_tag, r["id"]))
    lo = min(len(v) for v in by.values())
    cap = max(lo, int(lo * cap_ratio))
    out = {k: v[:cap] for k, v in by.items()}
    if max_total is not None and sum(len(v) for v in out.values()) > max_total:
        tot = sum(len(v) for v in out.values())
        f = max_total / tot
        out = {k: v[: int(len(v) * f)] for k, v in out.items()}
    res = [r for v in out.values() for r in v]
    res.sort(key=lambda r: r["id"])
    return res


def label_stats(rows: list) -> dict:
    c = Counter(str(r["gold"]) for r in rows)
    n = len(rows)
    return {"n": n, "labels": dict(sorted(c.items())), "shares": {k: round(v / n, 4) for k, v in sorted(c.items())}
            if n else {}}


def token_stats(toks: list) -> list | None:
    if not toks:
        return None
    t = sorted(toks)
    return [t[0], t[len(t) // 2], t[-1], round(sum(t) / len(t), 1)]


def write_outputs(T: str, rows: list, stats: dict) -> dict:
    """candidates/<T>.jsonl + candidates/<T>_stats.json (guarded writers)."""
    out = CAND_DIR / f"{T}.jsonl"
    kp.write_jsonl(out, rows)
    stats = dict(stats, output=str(out), output_sha256=sha256_file(out), n_rows=len(rows))
    kp.write_json(CAND_DIR / f"{T}_stats.json", stats)
    return stats


# ------------------------------------------------------------------------------------------------- G-block texts

POOL_TYPES = ("W2", "W3", "W5")


def load_texts() -> dict:
    """{text_id: text row} over every G-block domain (texts/<domain>/texts.jsonl, read-only)."""
    out = {}
    for d in sorted(x for x in TEXTS.iterdir() if x.is_dir()):
        for t in read_jsonl(d / "texts.jsonl"):
            assert t["text_id"] not in out, t["text_id"]
            out[t["text_id"]] = t
    return out


def pool_of(text_id: str) -> str:
    """Seeded, disjoint split of the G-block texts between W2, W3 and W5 (a text feeds at most one wave-2 type)."""
    return POOL_TYPES[key_hash(SEED, "wave2", "pool", text_id) % 3]


def pick_texts(texts: dict, T: str, n: int, *, min_w: int, max_w: int, ok=None, tag: str = "") -> list:
    """n texts of type T's pool, as even across domains as the pool allows (water-fill), seeded; `ok(text)` filters."""
    by = defaultdict(list)
    for t in texts.values():
        if pool_of(t["text_id"]) != T or not min_w <= nwords(t["text"]) <= max_w:
            continue
        if ok is not None and not ok(t):
            continue
        by[t["domain"]].append(t)
    for d in by:
        by[d].sort(key=lambda t: key_hash(SEED, T, tag, "text", t["text_id"]))
    sizes = {d: len(v) for d, v in by.items()}
    if not sizes:
        return []
    lo, hi = 0, max(sizes.values())
    while lo < hi:
        mid = (lo + hi) // 2
        if sum(min(s, mid) for s in sizes.values()) >= n:
            hi = mid
        else:
            lo = mid + 1
    picked = [t for d in sorted(by) for t in by[d][:min(sizes[d], lo)]]
    picked.sort(key=lambda t: key_hash(SEED, T, tag, "order", t["text_id"]))
    return picked[:n]


def text_meta(t: dict) -> dict:
    return {"text_id": t["text_id"], "domain": t["domain"], "text_source": t["source"],
            "text_licence": t.get("licence_url")}


# --------------------------------------------------------------------------------------------- Haiku-authored input

AUTHOR_MODEL = "Haiku 5.5"


def task_key() -> dict:
    return read_json(TASKS_KEY) if TASKS_KEY.exists() else {"tasks": {}}


def iter_answers(T: str, key: dict | None = None, answers: dict | None = None):
    """Yield (task_id, key entry, answer object or None, problems, provenance) for every type-T task, in order.
    `answers` ({task_id: object}) replaces the files (tests). A task file whose sha256 differs from tasks_key.json
    (the brief changed after the key was written) is refused, so an answer is only read against its own brief."""
    key = key or task_key()
    for tid, kk in sorted(key["tasks"].items()):
        if kk["type"] != T:
            continue
        prov = {"haiku_task_id": tid, "author_model": AUTHOR_MODEL, "haiku_task_sha256": kk.get("task_sha256"),
                "haiku_answer_sha256": None}
        if answers is not None:
            obj, probs = (answers.get(tid), []) if tid in answers else (None, ["missing"])
        else:
            tp = Path(kk["task_file"])
            if kk.get("task_sha256") and (not tp.exists() or sha256_file(tp) != kk["task_sha256"]):
                yield tid, kk, None, ["task file changed since tasks_key.json"], prov
                continue
            obj, probs = load_answer(kk["answer_file"])
            if obj is not None:
                prov["haiku_answer_sha256"] = sha256_file(kk["answer_file"])
        if obj is not None and (not isinstance(obj, dict) or obj.get("task_id") != tid):
            probs = probs + ["task_id missing or wrong"]
            obj = None
        yield tid, kk, obj, probs, prov


def text_field(x, *, min_w: int = 1, max_w: int = 300, single_line: bool = False):
    """(normalised text, None) or (None, reason). Formatting is normalised; wording is never changed."""
    if not isinstance(x, str):
        return None, "not a string"
    s = one_line(x) if single_line else norm_ws(x)
    if not s:
        return None, "empty"
    if any(m in s for m in ("<<<UNTRUSTED TEXT START>>>", "<<<UNTRUSTED TEXT END>>>")):
        return None, "marker string"
    if not min_w <= nwords(s) <= max_w:
        return None, f"{nwords(s)} words (allowed {min_w}-{max_w})"
    return s, None


class Dedup:
    """Exact duplicate filter on normalised text (case, spacing and punctuation ignored)."""

    def __init__(self):
        self.seen = set()

    def new(self, *parts) -> bool:
        k = "|".join(re.sub(r"\W+", " ", p.lower()).strip() for p in parts)
        if k in self.seen:
            return False
        self.seen.add(k)
        return True


def authored_stats(T: str, tasks_seen: dict, item_drops: Counter, rows: list, kept: list, rdrops: list,
                   toks: list, extra: dict | None = None) -> dict:
    s = {"type": T, "gold_method": "construction", "author_model": AUTHOR_MODEL, "tasks": tasks_seen,
         "item_drops": dict(item_drops), "candidates": len(rows), "kept_after_render": len(kept),
         "n_render_drops": len(rdrops), "render_drops": rdrops[:50], "labels": label_stats(kept),
         "tokens_min_med_max_mean": token_stats(toks)}
    s.update(extra or {})
    return s


def finish_authored(T: str, rows: list, stats: dict, argv: list) -> tuple:
    """Print a one-line summary; write candidates unless --dry-run or nothing was built."""
    print(f"{T} rows {len(rows)} labels {stats['labels'].get('labels')} tasks answered "
          f"{sum(1 for v in stats['tasks'].values() if v.get('answered'))}/{len(stats['tasks'])} "
          f"tokens {stats.get('tokens_min_med_max_mean')} render drops {stats.get('n_render_drops')}")
    if "--dry-run" not in argv and rows:
        write_outputs(T, rows, stats)
    elif not rows:
        print(f"{T}: no rows (no usable answers yet); nothing written")
    return rows, stats
